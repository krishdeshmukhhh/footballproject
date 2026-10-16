"""Markdown tables for eval/README.md, from results.json, hallucination.json and verifier_injection*.json.

Usage: python -m eval.make_table   (prints the spec-accuracy table and the naive-vs-pipeline table)
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results.json"
HALLUCINATION = HERE / "hallucination.json"
ROWS = [("teacher", "Qwen3-32B few-shot (teacher)"), ("base8b", "Base Qwen3-8B few-shot"),
        ("sft", "SFT Qwen3-8B (LoRA)"), ("grpo", "SFT + GRPO Qwen3-8B")]
DATASETS = [("test", "generated test"), ("dev_hard", "dev/hard"), ("independent_test", "independent"),
            ("handwritten_test", "hand-written")]
INDEPENDENT_SYSTEMS = [("teacher", "Qwen3-32B teacher"), ("base8b", "Base Qwen3-8B"), ("sft", "SFT Qwen3-8B")]
INJECTION_TYPES = ["number_perturb", "value_swap", "name_swap", "team_swap", "order_swap", "fabricated_stat"]


def main_table(res: dict, hall: dict | None) -> str:
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
    return "\n".join(lines)


def independent_table(res: dict) -> str:
    """Independent test set, one column per system. The misspelled-name subset is its own row, never mixed in."""
    systems = [(k, label) for k, label in INDEPENDENT_SYSTEMS if "independent_test" in res.get(k, {})]
    ind = {k: res[k]["independent_test"] for k, _ in systems}
    mis = {k: res[k].get("independent_misspelled") for k, _ in systems}
    n, n_mis = ind[systems[0][0]]["n"], (mis[systems[0][0]] or {}).get("n")
    rows = [(f"Valid JSON % (n={n})", lambda k: ind[k]["valid_json"]),
            (f"**Exec acc %** (n={n})", lambda k: f"**{ind[k]['exec_acc']}**"),
            (f"Spec acc % (n={n})", lambda k: ind[k]["spec_acc"]),
            ("Latency p50 (s)", lambda k: ind[k]["latency_p50_s"])]
    if n_mis:
        rows.append((f"**Misspelled-name pass %** (n={n_mis}, separate subset)",
                     lambda k: f"**{mis[k]['misspelling_pass']}** ({mis[k]['resolved_correct']} fixed the name, "
                               f"{mis[k]['did_you_mean_correct']} \"Did you mean\" with the right player)"))
    lines = ["| | " + " | ".join(label for _, label in systems) + " |", "|---|" + "---|" * len(systems)]
    lines += [f"| {name} | " + " | ".join(str(f(k)) for k, _ in systems) + " |" for name, f in rows]
    return "\n".join(lines)


def comparison_table(hall: dict) -> str:
    """Naive vs pipeline on the same questions: one row per system, counts with every rate, and a one-line
    definition per column. Rates are over answers scored (the pipeline's "Did you mean" replies have no claims)."""
    naive, pipe = hall["naive"]["breakdown"], hall["pipeline_on_subset"]["breakdown"]
    n = hall["n_naive_answerable"]

    def cell(b, key):
        return f"{b[key]['rate']}% ({b[key]['count']})"
    head = "| System | Answers scored | Hallucinated number | Wrong player or team | Order error | Any verified error |"
    rows = [("Naive: Qwen3-32B + full stats table in context", naive),
            ("Pipeline: SFT 8B spec + executor + Qwen3-32B answer (raw, before correction)", pipe)]
    lines = [head, "|---|---|---|---|---|---|"]
    for label, b in rows:
        lines.append(f"| {label} | {b['n']} of {n} | {cell(b, 'hallucinated_number')} | {cell(b, 'wrong_entity')} | "
                     f"{cell(b, 'order')} | **{cell(b, 'any_issue')}** |")
    dym = hall["pipeline_on_subset"]["did_you_mean_or_error"]
    lines += ["", "Rates are % of answers scored, with the count in brackets. Columns:", "",
              f"- **Answers scored:** questions that got an answer. The naive model answers everything; the pipeline "
              f"replied \"Did you mean ...?\" to {dym} misspelled name{'s' if dym != 1 else ''} instead of answering.",
              "- **Hallucinated number:** at least one number that is neither in the ground-truth result nor any true "
              "tournament stat of the player it is attached to (verifier issue kinds `number` and `attribution`).",
              "- **Wrong player or team:** names at least one player or team that is not in the ground-truth result "
              "or the question's filters (kinds `name` and `team`).",
              "- **Order error:** lists result players out of rank order, or gives one a wrong ordinal (kind `order`).",
              "- **Any verified error:** at least one of the three. The columns overlap, so they do not add up."]
    return "\n".join(lines)


def injection_table(inj: dict) -> str:
    lines = ["| Injected error | n | Caught % | Right issue kind % | Restored exactly by auto-correction % |",
             "|---|---|---|---|---|"]
    for kind in INJECTION_TYPES:
        s = inj["by_type"].get(kind)
        if s:
            lines.append(f"| {kind} | {s['n']} | {s['catch_rate']} | {s['right_kind_rate']} | "
                         f"{s.get('restored_by_correction', 'n/a')} |")
    o = inj["overall"]
    lines.append(f"| **Overall** | {o['n']} | **{o['catch_rate']}** | {o['right_kind_rate']} | |")
    return "\n".join(lines)


def main():
    res = json.loads(RESULTS.read_text())
    hall = json.loads(HALLUCINATION.read_text()) if HALLUCINATION.exists() else None
    print(main_table(res, hall))
    if hall:
        print(f"\nNaive vs pipeline, same {hall['n_naive_answerable']} player questions:\n")
        print(comparison_table(hall))


if __name__ == "__main__":
    main()
