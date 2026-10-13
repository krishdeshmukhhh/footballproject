"""Validate eval/handwritten_test.jsonl: every spec parses, executes, and is echoed back in plain English.

Usage: python -m eval.check_handwritten [path]
"""
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from query.executor import ExecutionError, execute
from query.schema import parse_spec

PATH = Path(__file__).parent / "handwritten_test.jsonl"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else PATH
    lines = [line for line in path.read_text().splitlines() if line.strip()]
    if not lines:
        print(f"{path} is empty: add 50-100 hand-written questions (see eval/HANDWRITTEN.md).")
        return
    bad = 0
    for i, line in enumerate(lines, 1):
        try:
            rec = json.loads(line)
            result = execute(parse_spec(rec["spec"]))
            top = result["rows"][:3]
            print(f"{i:3}. {rec['question']}\n     reads as: {result['interpretation']}\n     top: "
                  + ", ".join(f"{r.get('player', r.get('team'))} {r['value']}" for r in top))
            if not result["rows"]:
                print("     WARNING: empty result")
        except (json.JSONDecodeError, KeyError, ValidationError, ExecutionError) as e:
            bad += 1
            print(f"{i:3}. ERROR: {type(e).__name__}: {e}")
    print(f"\n{len(lines)} questions, {bad} invalid")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
