"""Phase 2.5 step A1-A2: sample query specs from the schema, execute them, keep the ones that work.

Specs are correct by construction; their results are the ground truth. Specs equal to a dev/hard
case or a few-shot example are excluded, so neither can leak into train/val/test.

The split is a deterministic function of the spec (hash of its canonical key), so it is fixed per
spec no matter how many are generated: the pilot is a subset of the full set with the same splits,
and paraphrases of one spec can never straddle splits.

Usage: python data/gen_specs.py --n 2000      -> data/specs.jsonl
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from query.compare import spec_key  # noqa: E402
from query.executor import ExecutionError, execute, load_tables, resolve_player  # noqa: E402
from query.manual_test import load_cases  # noqa: E402
from query.prompt import FEW_SHOT  # noqa: E402
from query.schema import METRICS, STAGES, TEAMS, parse_spec  # noqa: E402

OUT = ROOT / "data" / "specs.jsonl"

FAMILIES = [["CB", "FB"], ["AM", "CM", "DM"], ["ST", "W"]]
SINGLE_GROUPS = ["GK", "CB", "FB", "DM", "CM", "AM", "W", "ST"]
KNOCKOUT = [s for s in STAGES if s != "Group Stage"]
STAGE_CHOICES = [["Group Stage"], KNOCKOUT, ["Round of 16"], ["Quarter-finals"], ["Semi-finals"], ["Final"]]
MIN_MINUTES = [90, 180, 200, 270, 300, 360, 450]
# Metrics that make no sense for some position groups are still fine to ask about; we only skip
# goalkeeper rankings of attacking metrics, which are all zeros and teach nothing.
GK_OK = {"passes_attempted", "passes_completed", "pass_completion_pct", "pressured_passes_attempted",
         "pressured_passes_completed", "pressured_pass_completion_pct", "minutes", "progressive_passes"}


def split_of(key: str) -> str:
    bucket = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 10
    return "train" if bucket < 8 else ("val" if bucket == 8 else "test")


def surface_name(rng: random.Random, player_id: int, players) -> str:
    """How a question refers to a player: full display name or, when unambiguous, the surname."""
    display = players.set_index("player_id").loc[player_id, "player"]
    surname = display.split()[-1]
    if len(display.split()) > 1 and rng.random() < 0.5:
        try:
            if resolve_player(surname, players) == player_id:
                return surname
        except ExecutionError:
            pass
    return display


def sample_spec(rng: random.Random, players) -> dict:
    metric = "minutes" if rng.random() < 0.04 else rng.choice([m for m in METRICS if m != "minutes"])
    count = METRICS[metric]["kind"] == "count"
    f = {"players": None, "teams": None, "position_groups": None, "stages": None, "opponents": None,
         "min_minutes": None}
    spec = {"metric": metric, "per90": False, "group_by": "player", "filters": f, "sort": "desc", "limit": 5}

    mode = rng.choices(["ranking", "players", "team"], weights=[0.62, 0.23, 0.15])[0]
    if mode == "players":
        regulars = players[players["minutes"] >= 180]
        ids = regulars.sample(rng.choice([1, 1, 1, 2, 2, 3]), weights="minutes", random_state=rng.randrange(1 << 30))
        f["players"] = [surface_name(rng, pid, players) for pid in ids["player_id"]]
        spec["limit"] = len(f["players"])
        spec["per90"] = count and rng.random() < 0.25
        if rng.random() < 0.3:
            f["stages"] = rng.choice(STAGE_CHOICES)
        elif rng.random() < 0.15:
            f["opponents"] = [rng.choice(TEAMS)]
        return spec

    if mode == "team":
        spec["group_by"] = "team"
    spec["per90"] = count and rng.random() < 0.35
    spec["sort"] = "asc" if rng.random() < 0.15 else "desc"
    spec["limit"] = rng.choices([1, 3, 5, 10], weights=[0.35, 0.2, 0.3, 0.15])[0]
    if rng.random() < 0.45:
        f["position_groups"] = rng.choice(FAMILIES) if rng.random() < 0.4 else [rng.choice(SINGLE_GROUPS)]
        if f["position_groups"] == ["GK"] and metric not in GK_OK:
            f["position_groups"] = None
    if mode == "ranking" and rng.random() < 0.25:
        f["teams"] = [rng.choice(TEAMS)]
    if rng.random() < 0.2:
        f["stages"] = rng.choice(STAGE_CHOICES)
    if rng.random() < 0.1:
        f["opponents"] = [rng.choice(TEAMS)]
    if mode == "ranking" and rng.random() < 0.12:
        f["min_minutes"] = rng.choice(MIN_MINUTES)
    return spec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=2000, help="number of valid specs to keep")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    _, players = load_tables()
    excluded = {spec_key(s) for _, s in load_cases()} | {spec_key(s) for _, s in FEW_SHOT}

    seen, kept, dropped = set(), [], {"duplicate": 0, "excluded": 0, "error": 0, "empty": 0, "missing_player": 0}
    while len(kept) < args.n:
        raw = sample_spec(rng, players)
        spec = parse_spec(raw)
        key = spec_key(spec)
        if key in seen:
            dropped["duplicate"] += 1
            continue
        seen.add(key)
        if key in excluded:
            dropped["excluded"] += 1
            continue
        try:
            result = execute(spec)
        except ExecutionError:
            dropped["error"] += 1
            continue
        if not result["rows"]:
            dropped["empty"] += 1
            continue
        if spec.filters.players and len(result["rows"]) < len(spec.filters.players):
            dropped["missing_player"] += 1  # a named player did not play in the filtered matches
            continue
        kept.append({"spec_id": hashlib.sha256(key.encode()).hexdigest()[:12], "split": split_of(key),
                     "spec": spec.canonical(), "result": result})

    with open(OUT, "w") as fh:
        for rec in kept:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    splits = {s: sum(r["split"] == s for r in kept) for s in ("train", "val", "test")}
    print(f"kept {len(kept)} specs -> {OUT} | splits {splits} | dropped {dropped}")


if __name__ == "__main__":
    main()
