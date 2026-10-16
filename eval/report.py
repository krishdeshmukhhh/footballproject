"""Regenerate every number in eval/README.md (and eval/examples.md) from the saved outputs. No GPU needed.

  1. Re-score the saved naive and pipeline answers (eval/runs/hallucination_records.json) -> hallucination.json
  2. Re-run the verifier error-injection test, seed 0 and the held-out seed -> verifier_injection*.json
  3. Recompute the spec-accuracy, dataset and training facts from results.json, data/ and eval/runs/
  4. Render eval/README.md from eval/README.template.md, and eval/examples.md
  5. Fail if the template holds a number that is not a {{placeholder}} (identifiers such as Qwen3-32B excepted)

Nothing is appended to logs/verifier_catches.jsonl. Numbers that cannot be recomputed (superseded development runs,
manual judgements) come from eval/static_numbers.json and are marked with a dagger.

Usage: python -m eval.report               (everything, a few minutes)
       python -m eval.report --skip-rerun  (steps 3-5 only, from the existing JSON files)
"""
import argparse
import json
import re
from pathlib import Path

from query.describe import FAMILIES

from eval import examples, hallucination, verifier_injection
from eval.make_table import comparison_table, injection_table, main_table
from eval.run_eval import CONCURRENCY

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "eval"
RUNS = HERE / "runs"
TEMPLATE = HERE / "README.template.md"
README = HERE / "README.md"
STATIC = HERE / "static_numbers.json"
AUDIT_RESULTS = HERE / "audit_results.json"
PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")
# Digits that are names, not results: model sizes, the GPU, seeds, and references to numbered examples.
IDENTIFIERS = re.compile(r"Qwen3-\d+B|bf16|sft-v1|\b\d+B\b|H200|GPU \d|[Ss]eeds? \d+(?: and \d+)?|example \d+|per[- ]90")
DAGGER = "†"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def spec_facts(res: dict) -> dict:
    f = {}
    for system in ("teacher", "base8b", "sft"):
        for ds in ("test", "val", "dev_hard"):
            f[f"{system}_{ds}"] = res[system][ds]["exec_acc"]
            f[f"{system}_spec_{ds}"] = res[system][ds]["spec_acc"]
        f[f"{system}_qps"] = round(res[system]["test"]["throughput_qps"], 1)
    f["val_n"], f["dev_n"] = res["sft"]["val"]["n"], res["sft"]["dev_hard"]["n"]
    f["pilot_val"], f["pilot_dev"] = res["sft-pilot"]["val"]["exec_acc"], res["sft-pilot"]["dev_hard"]["exec_acc"]
    f["concurrency"] = CONCURRENCY
    return f


def independent_facts() -> dict:
    """How the independent test set was built, recomputed from its files (no GPU, no model)."""
    from query.schema import METRICS, parse_spec

    from eval import independent_name_check, independent_questions, independent_specs
    from eval.run_eval import top_suggestion
    test = load_jsonl(HERE / "independent_test.jsonl")
    dropped = load_jsonl(HERE / "independent_dropped.jsonl")
    miss = load_jsonl(HERE / "independent_misspelled.jsonl")
    written = test + dropped
    checks = json.loads((RUNS / "independent_name_check.json").read_text())

    # Ceiling: copy the misspelled name verbatim into the gold spec; does it resolve, or is the right player suggested?
    ceiling_misses = []
    for r in miss:
        spec = json.loads(json.dumps(r["spec"]))
        spec["filters"]["players"] = [r["misspelled_name"]]
        spec = parse_spec(spec)
        top = top_suggestion(spec)
        if top is None:
            ok = run_ok(spec)
        else:
            ok = top == r["player"]
        if not ok:
            ceiling_misses.append(f"for \"{r['misspelled_name']}\" ({r['player']}) the first suggestion is {top}.")
    kinds = {k: sum(r["misspelling"] == k for r in miss) for k in independent_specs.MISSPELLINGS}
    return {
        "ind_n": len(test), "ind_written": len(written), "ind_dropped_n": len(dropped),
        "ind_dropped_list": "\n".join(f"  - \"{r['question']}\": {r['drop_reason']}." for r in dropped),
        "ind_seed": independent_specs.SEED,
        "ind_metrics": len({r["spec"]["metric"] for r in written}), "n_metrics": len(METRICS),
        "ind_team_q": sum(r["spec"]["group_by"] == "team" for r in test),
        "ind_player_q": sum(bool(r["spec"]["filters"]["players"]) for r in test),
        "ind_excluded": len(independent_specs.used_spec_keys()),
        "ind_generator": written[0]["generator"], "ind_temperature": independent_questions.TEMPERATURE,
        "ind_typos": sum(r["style"] == "typos_slang" for r in written),
        "ind_fuzzy": sum(bool(c["fuzzy"]) and not c["mismatch"] for c in checks
                         if c["spec_id"] not in independent_name_check.DROPS),
        "mis_n": len(miss), "mis_kinds": ", ".join(f"{n} {k.replace('_', ' ')}" for k, n in kinds.items()),
        "mis_ceiling": len(miss) - len(ceiling_misses), "mis_ceiling_misses": " ".join(ceiling_misses) or "none.",
    }


def run_ok(spec) -> bool:
    from query.executor import ExecutionError, execute
    try:
        return bool(execute(spec)["rows"])
    except ExecutionError:
        return False


def contaminated(pair: dict) -> bool:
    """A paraphrase that says "forward" while the label is strikers only (the teacher's round-trip accepted it)."""
    q = pair["question"].lower()
    return pair["spec"]["filters"]["position_groups"] == ["ST"] and "forward" in q and "striker" not in q


def data_facts() -> dict:
    splits = {s: load_jsonl(ROOT / "data" / f"{s}.jsonl") for s in ("train", "val", "test")}
    specs = {s: len({p["spec_id"] for p in pairs}) for s, pairs in splits.items()}
    contam = {s: [p["question"] for p in pairs if contaminated(p)] for s, pairs in splits.items()}

    # Teacher misses on template questions (correct by construction), and how many read a family as one group.
    raw = load_jsonl(ROOT / "data" / "questions_raw.jsonl")
    misses = [r for r in raw if not r["template"]["kept"]]
    families = [set(f) for f in FAMILIES]

    def family_miss(r):
        gold = set(r["spec"]["filters"]["position_groups"] or [])
        got = set(((r["template"]["teacher_spec"] or {}).get("filters") or {}).get("position_groups") or [])
        return gold in families and got and got < gold

    sft_misses = json.loads((RUNS / "eval_sft_test.json").read_text())
    return {
        "train_pairs": f"{len(splits['train']):,}", "n_pairs": f"{sum(len(p) for p in splits.values()):,}",
        "train_specs": specs["train"], "val_specs": specs["val"], "test_specs": specs["test"],
        "n_specs": sum(specs.values()),
        "contam_train": len(contam["train"]), "contam_val": len(contam["val"]), "contam_test": len(contam["test"]),
        "contam_total": sum(len(c) for c in contam.values()),
        "template_misses": len(misses), "family_misses": sum(bool(family_miss(r)) for r in misses),
        "sft_test_misses": len(sft_misses),
        "sft_test_misses_contam": sum(m["question"] in contam["test"] for m in sft_misses),
        "_contaminated_questions": [q for c in contam.values() for q in c],
    }


def naive_prompt_ktokens() -> int:
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-32B", local_files_only=True)
    return round(len(tok(hallucination.naive_system_prompt())["input_ids"]) / 1000)


def hallucination_facts(hall: dict, contaminated_questions: list[str]) -> dict:
    nb = hall["naive"]["breakdown"]
    pipe = hall["pipeline_on_subset"]
    pb = pipe["breakdown"]
    gap = nb["issue_without_hallucinated_number"]
    errors = pipe["issues_vs_ground_truth"]
    # The README explains the pipeline's errors as label contamination; refuse to render if that stops being true.
    assert all(not e["spec_correct"] and e["question"] in contaminated_questions for e in errors), \
        f"pipeline errors vs ground truth changed, update the template: {errors}"
    pipe_error_text = " ".join(
        f"asked \"{e['question']}\", it answered \"{e['answer']}\" ({'; '.join(i['detail'] for i in e['issues'])})."
        for e in errors) or "none."
    return {
        "n_questions": hall["n_questions"], "n_sub": hall["n_naive_answerable"],
        "naive_halluc_k": nb["hallucinated_number"]["count"], "naive_halluc": nb["hallucinated_number"]["rate"],
        "naive_any_k": nb["any_issue"]["count"], "naive_any": nb["any_issue"]["rate"],
        "naive_gap_k": gap["count"], "naive_gap": gap["rate"], "naive_gap_entity": gap["with_wrong_entity"],
        "pipe_answered": pb["n"], "pipe_any_k": pb["any_issue"]["count"], "pipe_any": pb["any_issue"]["rate"],
        "pipe_self_check": pipe["self_check_flag_rate"], "pipe_error_text": pipe_error_text,
        "table_min_minutes": hallucination.TABLE_MIN_MINUTES, "naive_temperature": hallucination.NAIVE_TEMPERATURE,
    }


def injection_facts(inj0: dict, inj: dict) -> dict:
    ex = min(inj["miss_examples"], key=lambda m: len(m["question"]), default=None)
    return {
        "held_out_seed": verifier_injection.HELD_OUT_SEED, "inj_base": inj["base_answers"],
        "inj_fp": inj["false_positives_on_clean"], "inj0_catch": inj0["overall"]["catch_rate"],
        "inj0_fp": inj0["false_positives_on_clean"], "inj_misses": inj["misses"],
        "inj_misses_in_question": inj["misses_with_injected_number_in_question"],
        "inj_miss_example": f"\"{ex['change']}\" added to the answer for \"{ex['question']}\"" if ex else "none",
    }


def training_facts() -> dict:
    def run(name):
        summary = json.loads((RUNS / name / "train_summary.json").read_text())
        targs = json.loads((RUNS / name / "training_args.json").read_text())
        end = next(h for h in summary["log_history"] if "train_runtime" in h)
        # Runs before n_train was recorded: samples/s x runtime / epochs recovers it exactly at this precision.
        n_train = summary.get("n_train") or round(end["train_samples_per_second"] * end["train_runtime"]
                                                 / summary["args"]["epochs"])
        return summary, targs, end, n_train

    summary, targs, end, _ = run("sft-v1")
    adapter = json.loads((RUNS / "sft-v1" / "adapter_config.json").read_text())
    linear = {"q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"}
    targets = adapter["target_modules"]
    mantissa, exponent = f"{summary['args']['lr']:.0e}".split("e")
    p_summary, _, p_end, p_n = run("sft-pilot")
    return {
        "lora_r": adapter["r"], "lora_alpha": adapter["lora_alpha"],
        "lora_targets": "all linear" if set(targets) == linear else ", ".join(sorted(targets)),
        "lr": f"{mantissa}e{int(exponent)}", "scheduler": targs["lr_scheduler_type"],
        "epochs": int(summary["args"]["epochs"]), "batch": targs["per_device_train_batch_size"],
        "max_length": f"{targs['max_length']:,}", "steps": end["step"],
        "runtime_min": round(end["train_runtime"] / 60), "val_loss": round(summary["final_eval"]["eval_loss"], 4),
        "pilot_pairs": f"{p_n:,}", "pilot_epochs": int(p_summary["args"]["epochs"]),
        "pilot_runtime_min": round(p_end["train_runtime"] / 60, 1),
    }


def static_facts() -> dict:
    s = json.loads(STATIC.read_text())
    a, t = s["my_audit"], s["audit_trail"]
    mine = (f"of {a['n']}{DAGGER} randomly sampled flagged naive numbers (my audit during development), "
            f"{a['real']}{DAGGER} are clear hallucinations, {a['truncation']}{DAGGER} was truncation "
            f"({a['truncation_example']}; now accepted), and {a['unclear']}{DAGGER} is unclear ({a['unclear_example']}).")
    audit = json.loads(AUDIT_RESULTS.read_text()) if AUDIT_RESULTS.exists() else {}
    if audit.get("marked"):
        audit_text = (f"blind audit of {audit['marked']} naive answers ({audit['flagged_audited']} flagged, "
                      f"{audit['passed_audited']} passed; `audit_sample.md`). Of the flagged answers, "
                      f"{audit['flag_precision']}% have a real error; of the passed ones, {audit['pass_miss_rate']}% "
                      f"have an error the verifier missed. Number flags: {audit['number_flag_precision']}% precision "
                      f"on {audit['number_flag_audited']}. Re-weighted to all {audit['population']['n']} answers, "
                      f"about {audit.get('estimated_naive_error_rate')}% of naive answers contain an error. "
                      f"Earlier, {mine}")
    else:
        audit_text = (f"{mine[0].upper()}{mine[1:]} A blind audit of 100 answers (50 flagged, 50 passed, verdicts "
                      f"hidden) is in `audit_sample.md`, waiting to be marked.")
    return {"audit_text": audit_text,
            "audit_trail": "\n".join(f"- {b}{DAGGER}" for b in t["injection_bugs"]),
            "rounding_example": t["scorer_rounding_example"] + DAGGER,
            "rounding_rate": t["scorer_rounding_inflated_rate"]}


def check_template(template: str) -> None:
    stripped = IDENTIFIERS.sub("", PLACEHOLDER.sub("", template))
    stray = [(n + 1, line.strip()) for n, line in enumerate(stripped.split("\n")) if re.search(r"\d", line)]
    if stray:
        raise SystemExit("README.template.md has hard-coded numbers; use placeholders:\n" +
                         "\n".join(f"  line {n}: {line}" for n, line in stray))


def render(facts: dict) -> str:
    template = TEMPLATE.read_text()
    check_template(template)
    missing = sorted(set(PLACEHOLDER.findall(template)) - set(facts))
    if missing:
        raise SystemExit(f"no value for placeholders: {missing}")
    return PLACEHOLDER.sub(lambda m: str(facts[m.group(1)]), template)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-rerun", action="store_true", help="render from the existing JSON files")
    args = parser.parse_args()
    if not args.skip_rerun:
        print("1/4 re-scoring saved answers ...")
        hallucination.run(rescore=True, log=False)
        print("2/4 error injection, seeds 0 and", verifier_injection.HELD_OUT_SEED, "...")
        verifier_injection.run(0, log=False)
        verifier_injection.run(verifier_injection.HELD_OUT_SEED, log=False)
    print("3/4 recomputing facts ...")
    res = json.loads((HERE / "results.json").read_text())
    hall = json.loads((HERE / "hallucination.json").read_text())
    inj0 = json.loads((HERE / "verifier_injection.json").read_text())
    inj = json.loads((HERE / f"verifier_injection_seed{verifier_injection.HELD_OUT_SEED}.json").read_text())
    facts = spec_facts(res) | data_facts() | training_facts() | static_facts() | injection_facts(inj0, inj)
    facts |= independent_facts()
    facts |= hallucination_facts(hall, facts.pop("_contaminated_questions"))
    facts |= {"naive_prompt_ktokens": naive_prompt_ktokens(), "main_table": main_table(res, hall),
              "comparison_table": comparison_table(hall), "injection_table": injection_table(inj)}
    print("4/4 rendering ...")
    README.write_text(render(facts))
    examples.main()
    print(f"wrote {README}\n\nNaive vs pipeline, same {hall['n_naive_answerable']} questions:\n")
    print(comparison_table(hall))
    print(f"\nStatic ({DAGGER}) numbers, from {STATIC.name}: hand audit during development, development-run audit trail.")


if __name__ == "__main__":
    main()
