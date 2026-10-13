"""Phase 2 step 4: run hand-written questions through the NL -> spec -> execute pipeline.

Each question has a hand-written expected spec. A translation counts as correct on the spec if the
canonical specs match (player names compared after resolution), and on execution if both specs
produce the same result rows.

Usage: python -m query.manual_test [--backend teacher|student]
"""
import argparse
import json
from pathlib import Path

from query.executor import ExecutionError, execute, load_tables, resolve_player
from query.llm import translate
from query.prompt import KNOCKOUT, _spec
from query.schema import parse_spec

CASES = [
    ("Who scored the most goals in the World Cup?", _spec("goals", limit=1)),
    ("top 5 wingers for progressive carries per 90", _spec("progressive_carries", per90=True, position_groups=["W"])),
    ("How many pressures did Julián Álvarez make?", _spec("pressures", limit=1, players=["Julián Álvarez"])),
    ("Which Croatian midfielders completed the most passes under pressure?",
     _spec("pressured_passes_completed", teams=["Croatia"], position_groups=["AM", "CM", "DM"])),
    ("which team had the most xG in the group stage", _spec("xg", group_by="team", limit=1, stages=["Group Stage"])),
    ("Messi vs Mbappe xT added", _spec("xt_added", limit=2, players=["Messi", "Mbappe"])),
    ("Who had the most shot-creating actions against France?",
     _spec("shot_creating_actions", limit=1, opponents=["France"])),
    ("lowest pass completion % among strikers", _spec("pass_completion_pct", sort="asc", position_groups=["ST"])),
    ("Which centre backs made the most progressive passes in the knockout stage? top 3",
     _spec("progressive_passes", limit=3, position_groups=["CB"], stages=KNOCKOUT)),
    ("How many minutes did Bellingham play?", _spec("minutes", limit=1, players=["Bellingham"])),
    ("best goalkeepers by pass accuracy under pressure, min 270 mins",
     _spec("pressured_pass_completion_pct", position_groups=["GK"], min_minutes=270)),
    ("Who got the most assists for England?", _spec("assists", limit=1, teams=["England"])),
    ("which countries' forwards had the most non-penalty xG per game",
     _spec("npxg", per90=True, group_by="team", position_groups=["ST", "W"])),
    ("how many key passes did de bruyne make vs Morocco",
     _spec("key_passes", limit=1, players=["de bruyne"], opponents=["Morocco"])),
    ("Who were the most aggressive pressers among defenders per 90, at least 200 minutes?",
     _spec("pressures", per90=True, position_groups=["CB", "FB"], min_minutes=200)),
    ("most progresive pases by a japanese player", _spec("progressive_passes", limit=1, teams=["Japan"])),
    # Added after the prompt fix for position families, to check it generalises.
    ("Which Spanish midfield players made the most progressive passes per 90?",
     _spec("progressive_passes", per90=True, teams=["Spain"], position_groups=["AM", "CM", "DM"])),
    ("attackers with the most shots against Argentina", _spec("shots", opponents=["Argentina"], position_groups=["ST", "W"])),
]


def comparable(spec_dict: dict) -> dict:
    """Canonical spec with player names replaced by resolved ids, so 'Mbappe' == 'Kylian Mbappé'."""
    spec = parse_spec(spec_dict).canonical()
    if spec["filters"]["players"]:
        _, players = load_tables()
        ids = []
        for name in spec["filters"]["players"]:
            try:
                ids.append(resolve_player(name, players))
            except ExecutionError:
                ids.append(name)
        spec["filters"]["players"] = sorted(map(str, ids))
    return spec


def result_rows(spec_dict: dict):
    try:
        return [(r.get("player", r.get("team")), r["value"]) for r in execute(parse_spec(spec_dict))["rows"]]
    except ExecutionError as e:
        return f"ExecutionError: {e}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="teacher")
    parser.add_argument("--out", default="logs/phase2_manual.json")
    args = parser.parse_args()

    records = []
    for question, expected in CASES:
        t = translate(question, args.backend)
        got = t.spec.canonical() if t.spec else None
        rec = {
            "question": question, "raw": t.raw, "latency_s": round(t.latency_s, 3), "error": t.error,
            "spec_match": got is not None and comparable(got) == comparable(expected),
            "exec_match": got is not None and result_rows(got) == result_rows(expected),
            "result": result_rows(got) if got else None,
            "expected_spec": expected,
        }
        records.append(rec)
        mark = "OK " if rec["spec_match"] else ("~  " if rec["exec_match"] else "XX ")
        print(f"{mark}{question}\n    spec:   {t.raw}")
        if not rec["spec_match"]:
            print(f"    wanted: {json.dumps(expected)}")
        print(f"    result: {rec['result']}  ({t.latency_s:.2f}s)\n")

    n = len(records)
    summary = {
        "backend": args.backend, "n": n,
        "valid_json": sum(r["error"] is None for r in records),
        "spec_match": sum(r["spec_match"] for r in records),
        "exec_match": sum(r["exec_match"] for r in records),
        "mean_latency_s": round(sum(r["latency_s"] for r in records) / n, 3),
    }
    print(json.dumps(summary))
    Path(args.out).parent.mkdir(exist_ok=True)
    Path(args.out).write_text(json.dumps({"summary": summary, "records": records}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
