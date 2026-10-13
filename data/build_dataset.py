"""Phase 2.5 step A5-A7: turn questions_raw.jsonl into train/val/test JSONL, split by spec.

Each line: {"question", "spec", "result", "spec_id", "source": "template" | "paraphrase"}.
For paraphrases the target spec keeps player names as the paraphrase wrote them (taken from the
teacher's round-trip, which resolved them to the right players).

Usage: python data/build_dataset.py   -> data/{train,val,test}.jsonl
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from query.manual_test import load_cases  # noqa: E402
from query.prompt import FEW_SHOT  # noqa: E402

DATA = ROOT / "data"


def norm(q: str) -> str:
    return " ".join(q.lower().split())


def main():
    results = {r["spec_id"]: r["result"] for r in map(json.loads, (DATA / "specs.jsonl").read_text().splitlines())}
    raw = [json.loads(line) for line in (DATA / "questions_raw.jsonl").read_text().splitlines()]
    held_out = {norm(q) for q, _ in load_cases()} | {norm(q) for q, _ in FEW_SHOT}

    splits = {"train": [], "val": [], "test": []}
    seen, stats = set(), Counter()
    for r in sorted(raw, key=lambda r: r["spec_id"]):
        candidates = [(r["template"]["text"], r["spec"], "template")]
        for p in r["paraphrases"]:
            if p["kept"]:
                spec = json.loads(json.dumps(r["spec"]))
                spec["filters"]["players"] = p["teacher_spec"]["filters"]["players"]
                candidates.append((p["text"], spec, "paraphrase"))
            else:
                stats["paraphrase_dropped_drift"] += 1
        for question, spec, source in candidates:
            key = norm(question)
            if key in held_out:
                stats["dropped_held_out"] += 1
                continue
            if key in seen:
                stats["dropped_duplicate"] += 1
                continue
            seen.add(key)
            splits[r["split"]].append({"question": question, "spec": spec, "result": results[r["spec_id"]],
                                       "spec_id": r["spec_id"], "source": source})
        stats["template_teacher_wrong"] += not r["template"]["kept"]

    for name, rows in splits.items():
        with open(DATA / f"{name}.jsonl", "w") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    spec_sets = {k: {r["spec_id"] for r in v} for k, v in splits.items()}
    assert not (spec_sets["train"] & spec_sets["test"]) and not (spec_sets["train"] & spec_sets["val"]) \
        and not (spec_sets["val"] & spec_sets["test"]), "a spec straddles splits"
    total = sum(map(len, splits.values()))
    print(f"{total} pairs from {len(raw)} specs | " + " | ".join(
        f"{k}: {len(v)} pairs / {len(spec_sets[k])} specs" for k, v in splits.items()))
    print(dict(stats))


if __name__ == "__main__":
    main()
