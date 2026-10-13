"""Render eval/results.json as the markdown table for eval/README.md.

Usage: python -m eval.make_table
"""
import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results.json"
ROWS = [("teacher", "Qwen3-32B few-shot (teacher)"), ("base8b", "Base Qwen3-8B few-shot"),
        ("sft", "SFT Qwen3-8B (LoRA)"), ("grpo", "SFT + GRPO Qwen3-8B")]
DATASETS = [("test", "generated test"), ("dev_hard", "dev/hard"), ("handwritten_test", "hand-written")]


def main():
    res = json.loads(RESULTS.read_text())
    head = ["System", "Valid JSON %"] + [f"Exec acc % ({label})" for _, label in DATASETS] + \
           ["Hallucinated-number rate", "Latency p50 / p95 (s)", "Weights in GPU memory (GiB)"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for key, label in ROWS:
        r = res.get(key)
        if not r:
            lines.append(f"| {label} | " + " | ".join(["not run"] * (len(head) - 1)) + " |")
            continue
        main_ds = r.get("test") or next(iter(r.values()))
        accs = [f"{r[d]['exec_acc']} (n={r[d]['n']})" if d in r else "pending" for d, _ in DATASETS]
        mem = main_ds.get("weights_gib") or "?"
        lines.append(f"| {label} | {main_ds['valid_json']} | " + " | ".join(accs) +
                     f" | pending Phase 3 | {main_ds['latency_p50_s']} / {main_ds['latency_p95_s']} | {mem} |")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
