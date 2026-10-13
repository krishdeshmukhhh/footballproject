"""Run the dev/hard questions (eval/dev_hard.jsonl) through the NL -> spec -> execute pipeline.

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
from query.schema import parse_spec

DEV_HARD = Path(__file__).resolve().parents[1] / "eval" / "dev_hard.jsonl"


def load_cases(path=DEV_HARD) -> list[tuple[str, dict]]:
    """Dev/hard questions with hand-written expected specs. Never used for training or testing."""
    return [(r["question"], r["spec"]) for r in map(json.loads, Path(path).read_text().splitlines()) if r]


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
    for question, expected in load_cases():
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
        if got is not None:
            try:
                print(f"    reads:  {execute(t.spec)['interpretation']}")
            except ExecutionError:
                pass
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
