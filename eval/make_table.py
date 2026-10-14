"""Render eval/results.json as the markdown table for eval/README.md.

Usage: python -m eval.make_table
"""
import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results.json"
HALLUCINATION = Path(__file__).parent / "hallucination.json"
ROWS = [("teacher", "Qwen3-32B few-shot (teacher)"), ("base8b", "Base Qwen3-8B few-shot"),
        ("sft", "SFT Qwen3-8B (LoRA)"), ("grpo", "SFT + GRPO Qwen3-8B")]
DATASETS = [("test", "generated test"), ("dev_hard", "dev/hard"), ("handwritten_test", "hand-written")]


def main():
    res = json.loads(RESULTS.read_text())
    hall = json.loads(HALLUCINATION.read_text()) if HALLUCINATION.exists() else None
    # End-to-end hallucination is measured for the deployed pipeline (SFT student + 32B answers + verifier).
    halluc_col = {"sft": f"{hall['pipeline_all_questions']['raw_hallucinated_number_rate']}% "
                         f"(n={hall['pipeline_all_questions']['answered']})"} if hall else {}
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
                     f" | {halluc_col.get(key, 'not measured')} | {main_ds['latency_p50_s']} / {main_ds['latency_p95_s']} | {mem} |")
    if hall:
        sub = hall["pipeline_on_subset"]
        lines += ["", f"Naive vs pipeline, same {hall['n_naive_answerable']} player questions:", "",
                  "| System | Hallucinated-number rate | Any verified error |", "|---|---|---|",
                  f"| Naive: Qwen3-32B + full stats table in context | {hall['naive']['hallucinated_number_rate']}% "
                  f"| {hall['naive']['any_issue_rate']}% |",
                  f"| Pipeline: SFT 8B query + Qwen3-32B answer, raw | {sub['raw_hallucinated_number_rate']}% "
                  f"| {sub['self_check_flag_rate']}% |"]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
