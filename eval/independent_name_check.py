"""Deterministic name check for the independent test set: do the players and teams a question names match its gold spec?

For each question in eval/independent_test.jsonl (and the dropped file, so the check can be re-run after a drop):
  - every gold player (filters.players) must appear: by any token of the display name or the name as written in the
    spec (ignoring case and accents), else by a fuzzy match to a question word (typos), else it is "missing";
  - every gold team (filters.teams and filters.opponents) must appear: by name or demonym (the verifier's alias list),
    else fuzzily, else "missing";
  - any other dataset player the question names (query.verify.find_entities, read-only use) is "extra";
  - any other team the question names is "extra", unless it is the own team of a gold player ("Ronaldo for Portugal").
Fuzzy matches are listed but are not mismatches: typos were requested. Nothing here calls a model.
Not counted as mentions: Qatar as the host ("in Qatar 2022", "the Qatar World Cup"), and a player hit whose matched
text is a team name or demonym ("German players" is not Germán Pezzella). Demonyms beyond the verifier's list:
EXTRA_ALIASES.

Drops: the questions in DROPS were removed before any system was run on the set (`--apply` moves them from
independent_test.jsonl to independent_dropped.jsonl with the reason). Nothing is dropped after seeing results.

Usage: python -m eval.independent_name_check           (prints the mismatches; writes eval/runs/independent_name_check.json)
       python -m eval.independent_name_check --apply   (apply DROPS)
"""
import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from query.executor import load_tables, resolve_player
from query.schema import TEAMS
from query.verify import TEAM_ALIASES, find_entities

from eval.independent_specs import strip_accents

HERE = Path(__file__).parent
SETS = [HERE / "independent_test.jsonl", HERE / "independent_dropped.jsonl"]
OUT = HERE / "runs" / "independent_name_check.json"
FUZZY = 0.75
# Decided from this check's output, before any system was run. Kept despite a flag: f2d567f80437 (a ranking question
# that adds "I'm guessing it was someone like Messi or Neymar"; the ask itself is clear), and the fuzzy matches.
DROPS = {
    "8bf22acf2d04": "writer error: the spec compares Cody Gakpo and Achraf Dari (written \"Dari\"); the question names "
                    "Darwin Núñez instead of Dari",
    "22b9b9552ed6": "writer error: the spec is about Diogo Costa, Riley McGree and Rodrigo De Paul (written \"Costa\", "
                    "\"McGree\", \"Paul\"); the question names Christian Pulisic, Aaron Mooy and Gonçalo Guedes",
    "ba1315cc8d45": "writer error: the spec is about Guillermo Varela (written \"Varela\"); the question calls him "
                    "\"Ederson Varela\", borrowing the first name of another player (Ederson, Brazil)",
}
EXTRA_ALIASES = {"Aussie": "Australia", "Aussies": "Australia", "Croat": "Croatia", "Croats": "Croatia"}
ALIASES = TEAM_ALIASES | EXTRA_ALIASES
TEAM_WORDS = {t: [t] + [a for a, team in ALIASES.items() if team == t] for t in TEAMS}
HOST = re.compile(r"\b(?:in|at)\s+(?:the\s+)?(?:2022\s+)?Qatar\b|\bQatar\s+(?:2022|World Cup|WC)\b|"
                  r"\bWorld Cup\s+(?:in\s+|of\s+)?Qatar\b", re.I)


def fold(s: str) -> str:
    return " ".join(re.sub(r"[^\w\s-]", " ", strip_accents(s).lower()).replace("-", " ").split())


def _words(text: str) -> list[str]:
    return fold(text).split()


def find(phrases: list[str], question: str) -> str:
    """'exact' if any phrase occurs as whole words, 'fuzzy' if a run of question words is close to one, else 'missing'."""
    q = f" {fold(question)} "
    if any(f" {fold(p)} " in q for p in phrases if fold(p)):
        return "exact"
    words = _words(question)
    for p in phrases:
        k = len(fold(p).split())
        if len(fold(p)) < 4:
            continue
        runs = [" ".join(words[i:i + k]) for i in range(len(words) - k + 1)]
        if any(SequenceMatcher(None, fold(p), r).ratio() >= FUZZY for r in runs):
            return "fuzzy"
    return "missing"


def check(rec: dict, players) -> dict:
    f = rec["spec"]["filters"]
    by_id = players.set_index("player_id")
    gold_players, own_teams = {}, set()
    for name in f["players"] or []:
        display = by_id.loc[resolve_player(name, players), "player"]
        own_teams.add(by_id.loc[resolve_player(name, players), "team"])
        tokens = [w for w in display.split() if len(fold(w)) >= 3]
        gold_players[display] = find([name, display] + tokens, rec["question"])
    gold_teams = {t: find(TEAM_WORDS[t], rec["question"]) for t in (f["teams"] or []) + (f["opponents"] or [])}
    text = HOST.sub(lambda m: " " * len(m.group(0)), rec["question"]) if "Qatar" not in gold_teams else rec["question"]
    team_text = {fold(w) for words in TEAM_WORDS.values() for w in words}
    mentioned = [k for a, b, k in find_entities(text)
                 if not (k.startswith("player:") and fold(text[a:b]) in team_text)]
    extra_players = sorted({k.split(":", 1)[1] for k in mentioned if k.startswith("player:")} - set(gold_players))
    extra_teams = sorted({k.split(":", 1)[1] for k in mentioned if k.startswith("team:")} - set(gold_teams) - own_teams)
    missing = [f"player {p}" for p, s in gold_players.items() if s == "missing"] + \
              [f"team {t}" for t, s in gold_teams.items() if s == "missing"]
    extra = [f"player {p}" for p in extra_players] + [f"team {t}" for t in extra_teams]
    fuzzy = [p for p, s in {**gold_players, **gold_teams}.items() if s == "fuzzy"]
    return {"spec_id": rec["spec_id"], "question": rec["question"], "gold_players": list(gold_players),
            "gold_teams": list(gold_teams), "missing": missing, "extra": extra, "fuzzy": fuzzy,
            "mismatch": bool(missing or extra)}


def apply_drops():
    test, dropped = SETS
    keep, out = [], [json.loads(line) for line in dropped.read_text().splitlines()] if dropped.exists() else []
    for line in test.read_text().splitlines():
        rec = json.loads(line)
        if rec["spec_id"] in DROPS:
            out.append(rec | {"drop_reason": DROPS[rec["spec_id"]]})
        else:
            keep.append(rec)
    test.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep))
    dropped.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    print(f"{len(keep)} questions kept in {test.name}, {len(out)} in {dropped.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    if parser.parse_args().apply:
        return apply_drops()
    _, players = load_tables()
    recs = [json.loads(line) for p in SETS if p.exists() for line in p.read_text().splitlines() if line.strip()]
    results = [check(r, players) for r in recs]
    OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    bad = [r for r in results if r["mismatch"]]
    print(f"{len(results)} questions checked, {len(bad)} mismatches, "
          f"{sum(bool(r['fuzzy']) and not r['mismatch'] for r in results)} more with fuzzy (typo) matches only\n")
    for r in bad:
        print(f"[{r['spec_id']}] {r['question']}\n    gold players {r['gold_players']} teams {r['gold_teams']}"
              f" | missing {r['missing']} | extra {r['extra']}")
    print("\nFuzzy matches (kept, typos were requested):")
    for r in results:
        if r["fuzzy"] and not r["mismatch"]:
            print(f"  [{r['spec_id']}] {r['fuzzy']}: {r['question']}")


if __name__ == "__main__":
    main()
