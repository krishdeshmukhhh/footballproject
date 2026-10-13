"""Run the dev/hard questions (eval/dev_hard.jsonl) through the NL -> spec -> execute pipeline.

Each question has a hand-written expected spec. A translation counts as correct on the spec if the
canonical specs match (player names compared after resolution), and on execution if both specs
produce the same result rows (query/compare.py).

Usage: python -m query.manual_test [--backend teacher|student]
"""
import argparse
import json
from pathlib import Path

from query.compare import results_match, rows_key, spec_key
from query.executor import ExecutionError, execute
from query.llm import translate
from query.schema import parse_spec

DEV_HARD = Path(__file__).resolve().parents[1] / "eval" / "dev_hard.jsonl"


def load_cases(path=DEV_HARD) -> list[tuple[str, dict]]:
    """Dev/hard questions with hand-written expected specs. Never used for training or testing."""
    return [(r["question"], r["spec"]) for r in map(json.loads, Path(path).read_text().splitlines()) if r]


def result_rows(spec_dict: dict):
    try:
        return execute(parse_spec(spec_dict))["rows"]
    except ExecutionError as e:
        return f"ExecutionError: {e}"


def exec_equal(a, b) -> bool:
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    return results_match(a, b)


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
            "spec_match": got is not None and spec_key(got) == spec_key(expected),
            "exec_match": got is not None and exec_equal(result_rows(got), result_rows(expected)),
            "result": rows_key(result_rows(got)) if got and not isinstance(result_rows(got), str) else None,
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
