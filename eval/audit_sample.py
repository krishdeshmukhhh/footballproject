"""Hand-audit sample of naive-baseline answers: 20 the verifier flagged and 20 it passed, shuffled together,
with the verifier's verdicts left out of the file. (An earlier 100-item version, 50 and 50, is kept unmarked as
eval/audit_sample_100.md; --score reads only eval/audit_sample.md.)

The verdicts are not stored anywhere else either: --score recomputes them from
eval/runs/hallucination_records.json by question, after you have marked the file.

Usage:
  python -m eval.audit_sample                    write eval/audit_sample.md (refuses to overwrite marked boxes)
  python -m eval.audit_sample --lookup "name"    print a player's true tournament stats
  python -m eval.audit_sample --score            compare your marks with the verifier -> eval/audit_results.json
"""
import argparse
import json
import random
import re
from pathlib import Path

from query.executor import execute, load_tables
from query.schema import METRICS, parse_spec
from query.verify import _fmt, find_entities

from eval.hallucination import COLUMNS, DATASETS, RECORDS, rate

OUT = Path(__file__).parent / "audit_sample.md"
RESULTS = Path(__file__).parent / "audit_results.json"
N_PER_STRATUM = 20
SEED = 0
BOXES = ["no error", "has an error", "wrong number", "wrong player or team", "wrong order"]
INSTRUCTIONS = f"""# Hand audit: naive-baseline answers

{2 * N_PER_STRATUM} answers from the final naive-baseline run (Qwen3-32B with the stats table in its context, no query
layer), on the same question set as the comparison in `eval/README.md`. Half were flagged by the verifier and half were
not; they are shuffled, and the verifier's verdicts are not in this file.

**How to mark.** Tick exactly one of `no error` / `has an error` by changing `[ ]` to `[x]`. If there is an error,
also tick the kinds that apply. Then run `python -m eval.audit_sample --score`.

- **Has an error** means the answer states something false: a wrong number, a player or team that does not belong in
  the answer (or the wrong team for a player), or the wrong order for a ranking. Judge against the ground truth shown,
  which uses the project's conventions (for example, per-90, percentage and "fewest" rankings only count players with
  at least 270 minutes unless the question sets a threshold).
- **Not an error:** extra context that is true (for example, also naming the runner-up with his correct value),
  rounding, and harmless formatting.
- **Reference stats** are listed for every dataset player whose name was matched in the answer, plus the
  ground-truth players. Names are matched automatically, so a name with no line may still be a real player: check it
  with `python -m eval.audit_sample --lookup "name"`.
"""


def stat_line(p, metric: str) -> str:
    """True tournament line for one player (row of players.parquet): the question's metric first, then the rest."""
    head = f"{p['team']}, {p['position_group']}, {p['minutes']:.1f} min, {int(p['matches'])} matches"
    pct = {"pass_completion_pct": ("passes_completed", "passes_attempted"),
           "pressured_pass_completion_pct": ("pressured_passes_completed", "pressured_passes_attempted")}
    if metric in pct:
        num, den = pct[metric]
        focus = f"{metric} {100 * p[num] / p[den]:.1f}" if p[den] else f"{metric} n/a (no attempts)"
    else:
        decimals = max(2, METRICS[metric]["decimals"])
        per90 = f"{p[metric] / p['minutes'] * 90:.{decimals}f}" if p["minutes"] else "n/a"
        focus = f"{metric} {_num(p[metric], metric)}, per 90 {per90}"
    rest = [f"{col} {_num(p[col], col)}" for col in COLUMNS[5:] if col != metric]
    for name, (num, den) in pct.items():
        if p[den] and name != metric:
            rest.append(f"{name} {100 * p[num] / p[den]:.1f}")
    return f"{head}: **{focus}**. Other: " + "; ".join(rest)


def _num(v, col: str) -> str:
    return f"{float(v):.3f}".rstrip("0").rstrip(".") if col in ("xg", "npxg", "xt_added") else str(int(v))


def sample(records: list[dict]) -> list[dict]:
    sub = [r for r in records if r["in_subset"]]
    flagged = [r for r in sub if r["naive_issues"]]
    clean = [r for r in sub if not r["naive_issues"]]
    rng = random.Random(SEED)
    picked = rng.sample(flagged, min(N_PER_STRATUM, len(flagged))) + rng.sample(clean, min(N_PER_STRATUM, len(clean)))
    rng.shuffle(picked)
    return picked


def render(records: list[dict]) -> str:
    gold_specs = {json.loads(line)["question"]: json.loads(line)["spec"]
                  for p in DATASETS for line in p.read_text().splitlines() if line.strip()}
    _, players = load_tables()
    by_name = players.set_index("player")
    out = [INSTRUCTIONS]
    for n, r in enumerate(sample(records), 1):
        gold = execute(parse_spec(gold_specs[r["question"]]))
        metric = gold["spec"]["metric"]
        named = [k.split(":", 1)[1] for _, _, k in find_entities(r["naive"]) if k.startswith("player:")]
        refs = list(dict.fromkeys([g["player"] for g in gold["rows"]] + named))
        out += [f"## A{n:03d}", "", f"**Question:** {r['question']}", "",
                f"**Ground truth** ({gold['interpretation']}):", "",
                "| Rank | Player | Team | Value | Minutes | Matches |", "|---|---|---|---|---|---|"]
        out += [f"| {g['rank']} | {g['player']} | {g['team']} | {_fmt(g['value'])} | {g['minutes']} | {g['matches']} |"
                for g in gold["rows"]]
        out += ["", "**Naive answer:**", ""] + ["> " + line for line in r["naive"].split("\n")]
        out += ["", "**Reference stats** (true tournament totals):", ""]
        out += [f"- {name}: {stat_line(by_name.loc[name], metric)}" for name in refs]
        out += ["", "**Your verdict:** " + "  ".join(f"[ ] {b}" for b in BOXES[:2]),
                "", "If an error: " + "  ".join(f"[ ] {b}" for b in BOXES[2:]), "", "**Notes:** ", "", "---", ""]
    return "\n".join(out)


def parse_marks(text: str) -> dict[str, dict]:
    """{item id: {"question": ..., "marks": set of ticked boxes}} from a marked audit_sample.md."""
    items = {}
    for block in re.split(r"^## (?=A\d{3}$)", text, flags=re.M)[1:]:
        item_id = block.split("\n", 1)[0].strip()
        question = re.search(r"^\*\*Question:\*\* (.*)$", block, re.M).group(1)
        marks = {b for b in BOXES if re.search(r"\[[xX]\] " + re.escape(b) + r"(?!\w)", block)}
        items[item_id] = {"question": question, "marks": marks}
    return items


def score(records: list[dict]) -> dict:
    items = parse_marks(OUT.read_text())
    by_q = {r["question"]: r for r in records if r["in_subset"]}
    sub = list(by_q.values())
    n_flagged_pop = sum(bool(r["naive_issues"]) for r in sub)
    rows, unmarked, conflicting = [], [], []
    for item_id, it in items.items():
        if not it["marks"] & {"no error", "has an error"}:
            unmarked.append(item_id)
            continue
        if {"no error", "has an error"} <= it["marks"]:
            conflicting.append(item_id)
            continue
        r = by_q[it["question"]]
        kinds = {i["kind"] for i in r["naive_issues"]}
        rows.append({"id": item_id, "human_error": "has an error" in it["marks"],
                     "human_number": "wrong number" in it["marks"], "flagged": bool(kinds),
                     "flagged_number": bool(kinds & {"number", "attribution"})})
    flagged = [x for x in rows if x["flagged"]]
    passed = [x for x in rows if not x["flagged"]]
    numf = [x for x in rows if x["flagged_number"]]
    res = {
        "marked": len(rows), "unmarked": unmarked, "conflicting": conflicting,
        "flagged_audited": len(flagged), "passed_audited": len(passed),
        "flag_precision": rate(x["human_error"] for x in flagged),          # flagged and the human agrees
        "pass_miss_rate": rate(x["human_error"] for x in passed),           # passed but the human found an error
        "number_flag_audited": len(numf),
        "number_flag_precision": rate(x["human_number"] for x in numf),
        "human_number_errors_without_number_flag": sum(x["human_number"] and not x["flagged_number"] for x in rows),
        "population": {"n": len(sub), "flagged": n_flagged_pop},
    }
    if flagged and passed:  # re-weight the two strata to the population of naive answers
        p = n_flagged_pop / len(sub)
        res["estimated_naive_error_rate"] = round(p * res["flag_precision"] + (1 - p) * res["pass_miss_rate"], 1)
    RESULTS.write_text(json.dumps(res, indent=1))
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--lookup")
    args = parser.parse_args()
    records = json.loads(RECORDS.read_text())
    if args.lookup:
        _, players = load_tables()
        hits = players[players["player"].str.contains(args.lookup, case=False)]
        for _, p in hits.iterrows():
            print(f"{p['player']}: {stat_line(p, 'goals')}")
        if hits.empty:
            print("no player in the dataset matches", repr(args.lookup))
        return
    if args.score:
        print(json.dumps(score(records), indent=1))
        return
    if OUT.exists() and any(it["marks"] for it in parse_marks(OUT.read_text()).values()):
        raise SystemExit(f"{OUT} already has marks; not overwriting")
    OUT.write_text(render(records))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
