"""Independent test set, step 1: sample new specs in code, execute them, keep the non-empty ones.

The specs are drawn like data/gen_specs.py, but from cycling decks so that every metric, position group (single
and family), stage (including the third-place match on its own), opponent and team appears, and team-level
questions get a fixed share. A spec is excluded if its canonical key equals any spec already in use:
data/specs.jsonl (every sampled spec, including ones whose questions were dropped), data/{train,val,test}.jsonl,
eval/dev_hard.jsonl and the few-shot examples. So no spec overlaps with training, validation, the generated test
split, dev/hard or the prompt.

Dropped at sampling time, before any model sees the spec: duplicates, excluded specs, specs that fail to execute,
specs with an empty result, and player specs where a named player did not play in the filtered matches.

Usage: python -m eval.independent_specs [--n 300] [--seed 2026]   -> eval/independent_specs.jsonl
"""
import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

from data.gen_specs import FAMILIES, GK_OK, KNOCKOUT, MIN_MINUTES, SINGLE_GROUPS, surface_name
from query.compare import spec_key
from query.executor import ExecutionError, execute, load_tables
from query.manual_test import load_cases
from query.prompt import FEW_SHOT
from query.schema import METRICS, STAGES, TEAMS, parse_spec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "eval" / "independent_specs.jsonl"
STAGE_CHOICES = [[s] for s in STAGES] + [KNOCKOUT]
POSITION_CHOICES = [[g] for g in SINGLE_GROUPS] + FAMILIES
LIMITS = [1, 3, 5, 10, 2, 4, 6, 8, 15, 20]
LIMIT_WEIGHTS = [0.3, 0.2, 0.25, 0.13, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]


class Deck:
    """Draws items in a shuffled order and reshuffles when empty, so every item comes up evenly. Draws for a
    spec that is then dropped go back into the deck (`rollback`), so a dropped spec costs no coverage."""

    def __init__(self, rng: random.Random, items: list):
        self.rng, self.items, self.left, self.pending = rng, list(items), [], []

    def draw(self):
        if not self.left:
            self.left = list(self.items)
            self.rng.shuffle(self.left)
        self.pending.append(self.left.pop())
        return self.pending[-1]

    def commit(self):
        self.pending = []

    def rollback(self):
        self.left = self.left + self.pending[::-1]
        self.pending = []


def used_spec_keys() -> set[str]:
    keys = {spec_key(s) for _, s in load_cases()} | {spec_key(s) for _, s in FEW_SHOT}
    for path in [ROOT / "data" / "specs.jsonl"] + [ROOT / "data" / f"{s}.jsonl" for s in ("train", "val", "test")]:
        keys |= {spec_key(json.loads(line)["spec"]) for line in path.read_text().splitlines() if line.strip()}
    return keys


def sample_spec(rng: random.Random, decks: dict, players) -> dict:
    metric = decks["metric"].draw()
    count = METRICS[metric]["kind"] == "count"
    f = {"players": None, "teams": None, "position_groups": None, "stages": None, "opponents": None,
         "min_minutes": None}
    spec = {"metric": metric, "per90": False, "group_by": "player", "filters": f, "sort": "desc", "limit": 5}

    mode = decks["mode"].draw()
    if mode == "players":
        regulars = players[players["minutes"] >= 180]
        ids = regulars.sample(rng.choice([1, 1, 1, 2, 2, 3]), weights="minutes", random_state=rng.randrange(1 << 30))
        f["players"] = [surface_name(rng, pid, players) for pid in ids["player_id"]]
        spec["limit"] = len(f["players"])
        spec["per90"] = count and rng.random() < 0.25
        if rng.random() < 0.3:
            f["stages"] = decks["stage"].draw()
        elif rng.random() < 0.2:
            f["opponents"] = [decks["opponent"].draw()]
        return spec

    if mode == "team":
        spec["group_by"] = "team"
    spec["per90"] = count and rng.random() < 0.35
    spec["sort"] = "asc" if rng.random() < 0.15 else "desc"
    spec["limit"] = rng.choices(LIMITS, weights=LIMIT_WEIGHTS)[0]
    if rng.random() < 0.45:
        f["position_groups"] = decks["position"].draw()
        if f["position_groups"] == ["GK"] and metric not in GK_OK:
            f["position_groups"] = None
    if mode == "ranking" and rng.random() < 0.3:
        f["teams"] = [decks["team"].draw()]
    if rng.random() < 0.25:
        f["stages"] = decks["stage"].draw()
    if rng.random() < 0.15:
        f["opponents"] = [decks["opponent"].draw()]
    if mode == "ranking" and rng.random() < 0.12:
        f["min_minutes"] = rng.choice(MIN_MINUTES)
    return spec


def coverage(kept: list[dict]) -> dict:
    specs = [r["spec"] for r in kept]
    flt = [s["filters"] for s in specs]
    return {
        "metrics": Counter(s["metric"] for s in specs),
        "position_groups": Counter(g for f in flt for g in f["position_groups"] or []),
        "position_choices": Counter(",".join(f["position_groups"]) for f in flt if f["position_groups"]),
        "stages": Counter(s for f in flt for s in f["stages"] or []),
        "stage_choices": Counter(",".join(f["stages"]) for f in flt if f["stages"]),
        "opponents": Counter(o for f in flt for o in f["opponents"] or []),
        "teams": Counter(t for f in flt for t in f["teams"] or []),
        "group_by": Counter(s["group_by"] for s in specs),
        "player_specs": sum(bool(f["players"]) for f in flt),
        "per90": sum(s["per90"] for s in specs), "asc": sum(s["sort"] == "asc" for s in specs),
        "min_minutes": sum(f["min_minutes"] is not None for f in flt),
    }


def check_coverage(cov: dict) -> list[str]:
    gaps = [f"metric {m}" for m in METRICS if not cov["metrics"][m]]
    gaps += [f"position {g}" for g in SINGLE_GROUPS if not cov["position_choices"][g]]
    gaps += [f"family {','.join(g)}" for g in FAMILIES if not cov["position_choices"][",".join(g)]]
    gaps += [f"stage {s}" for s in STAGES if not cov["stage_choices"][s]]
    gaps += ["stage knockout"] if not cov["stage_choices"][",".join(sorted(KNOCKOUT))] else []
    gaps += [f"opponent {t}" for t in TEAMS if not cov["opponents"][t]]
    gaps += [f"team {t}" for t in TEAMS if not cov["teams"][t]]
    gaps += ["team questions"] if not cov["group_by"]["team"] else []
    return gaps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    _, players = load_tables()
    decks = {"metric": Deck(rng, list(METRICS)), "stage": Deck(rng, STAGE_CHOICES),
             "position": Deck(rng, POSITION_CHOICES), "opponent": Deck(rng, TEAMS), "team": Deck(rng, TEAMS),
             "mode": Deck(rng, ["ranking"] * 11 + ["players"] * 5 + ["team"] * 4)}
    excluded = used_spec_keys()

    def rollback():
        for deck in decks.values():
            deck.rollback()

    seen, kept, dropped = set(), [], Counter()
    while len(kept) < args.n:
        spec = parse_spec(sample_spec(rng, decks, players))
        key = spec_key(spec)
        if key in seen:
            dropped["duplicate"] += 1
            rollback()
            continue
        seen.add(key)
        if key in excluded:
            dropped["already_used"] += 1
            rollback()
            continue
        try:
            result = execute(spec)
        except ExecutionError:
            dropped["error"] += 1
            rollback()
            continue
        if not result["rows"]:
            dropped["empty"] += 1
            rollback()
            continue
        if spec.filters.players and len(result["rows"]) < len(spec.filters.players):
            dropped["missing_player"] += 1
            rollback()
            continue
        for deck in decks.values():
            deck.commit()
        kept.append({"spec_id": hashlib.sha256(key.encode()).hexdigest()[:12], "spec": spec.canonical(),
                     "result": result})

    cov = coverage(kept)
    gaps = check_coverage(cov)
    if gaps:
        raise SystemExit(f"coverage gaps with seed {args.seed}: {gaps}")
    with open(OUT, "w") as fh:
        for rec in kept:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"kept {len(kept)} specs -> {OUT} | excluded {len(excluded)} used specs | dropped {dict(dropped)}")
    for k, v in cov.items():
        print(f"  {k}: {dict(v) if isinstance(v, Counter) else v}")


if __name__ == "__main__":
    main()
