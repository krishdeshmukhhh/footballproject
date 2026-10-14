"""Phase 3 step 4: error-injection test for the verifier.

Base answers: the pipeline's answers from eval/hallucination.py whose spec was correct and that verify clean
against ground truth (eval/runs/hallucination_records.json). Into each, inject one error of every applicable type,
then run the runtime verifier (no extra truth) and measure:

  caught        the verifier reports any issue
  right kind    it reports an issue of the expected kind
  restored      for number errors on a known row, correct() puts back exactly the original text

Types:
  number_perturb   one row value changed by 10-40% (or +-1..3 for small integers)
  value_swap       the values of two rows swapped
  name_swap        a row player replaced by a same-position player who is not in the result
  team_swap        a team mention replaced by a team not involved in the question or result
  order_swap       in a numbered list, the contents of two adjacent lines swapped
  fabricated_stat  an extra sentence giving a row player a number that is not in the result

Every catch is appended to logs/verifier_catches.jsonl with source "error_injection" (unless --no-log).
Usage: python -m eval.verifier_injection --seed N
"""
import difflib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from query.answer import log_catch
from query.executor import load_tables
from query.schema import TEAMS
from query.verify import LIST_MARKER_RE, NUMBER_RE, _matches, correct, find_entities, verify

HELD_OUT_SEED = 2  # seeds 0 and 1 were used while fixing the verifier

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "eval" / "runs" / "hallucination_records.json"
OUT = Path(__file__).parent / "verifier_injection.json"
EXPECTED_KIND = {"number_perturb": {"number", "attribution"}, "value_swap": {"attribution"}, "name_swap": {"name"},
                 "team_swap": {"team"}, "order_swap": {"order"}, "fabricated_stat": {"number", "attribution"}}


def fmt_like(value: float, template: str) -> str:
    decimals = len(template.split(".")[1]) if "." in template else 0
    return f"{value:.{decimals}f}" if decimals else str(int(round(value)))


def value_spans(answer: str, rows: list[dict]):
    """(start, end, row index) for numbers in the answer that are some row's value."""
    out = []
    markers = {m.start(1) for m in LIST_MARKER_RE.finditer(answer)}
    for m in NUMBER_RE.finditer(answer):
        if m.start(1) in markers:  # "1." list numbering is structure, not a value
            continue
        text = m.group(1)
        num, dec = float(text.replace(",", "")), (len(text.split(".")[1]) if "." in text else 0)
        hits = [i for i, r in enumerate(rows) if _matches(num, dec, r["value"])]
        if len(hits) == 1:
            out.append((m.start(1), m.end(1), hits[0]))
    return out


def allowed_numbers(rows, spec, min_minutes):
    vals = [r["value"] for r in rows] + [r["minutes"] for r in rows] + [r["matches"] for r in rows]
    return vals + [90, 2022, spec["limit"], len(rows), min_minutes, 270, 90] + list(range(1, len(rows) + 1))


def inject(kind: str, answer: str, rows: list[dict], spec: dict, rng: random.Random, players):
    """Return the corrupted answer, or None if this error type does not apply to this answer."""
    if kind == "number_perturb":
        spans = value_spans(answer, rows)
        if not spans:
            return None
        a, b, i = rng.choice(spans)
        old = float(answer[a:b].replace(",", ""))
        allowed = allowed_numbers(rows, spec, 0)
        for _ in range(20):
            new = old + rng.choice([-1, 1]) * rng.randint(1, 3) if old < 10 and "." not in answer[a:b] \
                else old * (1 + rng.choice([-1, 1]) * rng.uniform(0.1, 0.4))
            text = fmt_like(new, answer[a:b])
            if float(text) != old and not any(_matches(float(text), 0 if "." not in text else len(text.split(".")[1]), t)
                                              for t in allowed) and float(text) >= 0:
                return answer[:a] + text + answer[b:]
        return None

    if kind == "value_swap":
        spans = value_spans(answer, rows)
        firsts = {}
        for a, b, i in spans:
            firsts.setdefault(i, (a, b))
        pairs = [(x, y) for x in firsts for y in firsts if x < y and rows[x]["value"] != rows[y]["value"]]
        if not pairs:
            return None
        x, y = rng.choice(pairs)
        (a1, b1), (a2, b2) = sorted([firsts[x], firsts[y]])
        return answer[:a1] + answer[a2:b2] + answer[b1:a2] + answer[a1:b1] + answer[b2:]

    mentions = find_entities(answer)
    if kind == "name_swap":
        row_players = {r["player"] for r in rows if "player" in r}
        cands = [(a, b, k) for a, b, k in mentions if k.startswith("player:") and k[7:] in row_players]
        if not cands:
            return None
        a, b, k = rng.choice(cands)
        group = players.set_index("player").loc[k[7:], "position_group"]
        pool = players[(players["position_group"] == group) & ~players["player"].isin(row_players)
                       & (players["minutes"] >= 90)]["player"].tolist()
        return answer[:a] + rng.choice(pool) + answer[b:]

    if kind == "team_swap":
        involved = set((spec["filters"]["teams"] or []) + (spec["filters"]["opponents"] or []))
        involved |= {r["team"] for r in rows}
        cands = [(a, b, k) for a, b, k in mentions if k.startswith("team:") and answer[a:b] == k[5:]]
        if not cands:
            return None
        a, b, _ = rng.choice(cands)
        return answer[:a] + rng.choice([t for t in TEAMS if t not in involved]) + answer[b:]

    if kind == "order_swap":
        if spec["filters"]["players"] or len(rows) < 2:
            return None
        lines = answer.split("\n")
        items = [(i, m) for i, l in enumerate(lines) if (m := re.match(r"^(\s*\d+[.)]\s*)(.*)$", l))]
        pairs = [(p, q) for p, q in zip(items, items[1:]) if q[0] == p[0] + 1]
        rank_of = {f"player:{r['player']}" if "player" in r else f"team:{r['team']}": r["rank"] for r in rows}

        def line_rank(line):
            ks = [k for _, _, k in find_entities(line) if k in rank_of]
            return rank_of[ks[0]] if ks else None
        pairs = [(p, q) for p, q in pairs if line_rank(p[1].group(2)) and line_rank(q[1].group(2))
                 and line_rank(p[1].group(2)) < line_rank(q[1].group(2))]
        if not pairs:
            return None
        (i, m1), (j, m2) = rng.choice(pairs)
        lines[i], lines[j] = m1.group(1) + m2.group(2), m2.group(1) + m1.group(2)
        return "\n".join(lines)

    if kind == "fabricated_stat":
        row = rng.choice([r for r in rows if "player" in r] or [None])
        if row is None:
            return None
        allowed = allowed_numbers(rows, spec, 0)
        n = rng.choice([x for x in range(3, 60) if not any(_matches(x, 0, t) for t in allowed)])
        stat = rng.choice(["shots", "pressures", "key passes", "progressive carries", "completed passes"])
        return answer + f" {row['player'].split()[-1]} also recorded {n} {stat}."
    raise ValueError(kind)


def inserted_text(original: str, injected: str) -> str:
    """Words of `injected` that are not in `original` (inserted or replaced), joined by spaces."""
    a, b = original.split(), injected.split()
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    return " ".join(" ".join(b[j1:j2]) for op, _, _, j1, j2 in ops if op in ("insert", "replace"))


def numbers_in(text: str) -> set[str]:
    return {m.group(1) for m in NUMBER_RE.finditer(text)}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0, help="seed 0 was used while refining the verifier; "
                                                            f"seed {HELD_OUT_SEED} is the held-out run")
    parser.add_argument("--no-log", action="store_true", help="do not append catches to logs/verifier_catches.jsonl")
    args = parser.parse_args()
    print(json.dumps(run(args.seed, log=not args.no_log), indent=1))


def run(seed: int, log: bool = True) -> dict:
    records = json.loads(RECORDS.read_text())
    base = [r for r in records if r["pipeline_type"] == "answer" and r["spec_correct"] and not r["pipeline_raw_issues"]]
    gold = {json.loads(line)["question"]: json.loads(line)["spec"]
            for p in [ROOT / "data" / "test.jsonl", ROOT / "eval" / "dev_hard.jsonl"] for line in p.read_text().splitlines()}
    _, players = load_tables()
    rng = random.Random(seed)
    from query.executor import execute
    from query.schema import parse_spec

    stats = defaultdict(lambda: defaultdict(int))
    misses, unrestored = [], []
    clean_flags = 0
    for r in base:
        result = execute(parse_spec(gold[r["question"]]))
        clean_flags += not verify(r["pipeline_raw"], result, r["question"]).ok
        for kind in EXPECTED_KIND:
            bad = inject(kind, r["pipeline_raw"], result["rows"], result["spec"], rng, players)
            if bad is None or bad == r["pipeline_raw"]:
                continue
            v = verify(bad, result, r["question"])
            kinds = {i.kind for i in v.issues}
            s = stats[kind]
            s["n"] += 1
            s["caught"] += not v.ok
            s["right_kind"] += bool(kinds & EXPECTED_KIND[kind])
            if kind in ("number_perturb", "value_swap"):
                fixed = correct(bad, v, result).split("\n\n⚠ Verification")[0]
                s["restored"] += fixed == r["pipeline_raw"]
                if fixed != r["pipeline_raw"]:
                    unrestored.append({"type": kind, "original": r["pipeline_raw"], "injected": bad, "fixed": fixed,
                                       "issues": [(i.kind, i.detail, bool(i.expected)) for i in v.issues]})
            if v.ok:
                misses.append({"type": kind, "question": r["question"], "original": r["pipeline_raw"], "injected": bad,
                               "change": inserted_text(r["pipeline_raw"], bad),
                               "new_number_in_question": bool(numbers_in(inserted_text(r["pipeline_raw"], bad))
                                                              & numbers_in(r["question"]))})
            elif log:
                log_catch({"source": "error_injection", "injection": kind, "question": r["question"],
                           "spec": result["spec"], "interpretation": result["interpretation"], "rows": result["rows"],
                           "raw_answer": bad, "issues": [i.__dict__ for i in v.issues],
                           "corrected_answer": correct(bad, v, result)})

    def pct(a, b):
        return round(100 * a / b, 1) if b else None
    summary = {"seed": seed, "base_answers": len(base), "false_positives_on_clean": clean_flags, "by_type": {},
               "misses": len(misses), "misses_with_injected_number_in_question": sum(m["new_number_in_question"]
                                                                                      for m in misses),
               "miss_examples": [{"type": m["type"], "question": m["question"], "change": m["change"]} for m in misses]}
    tot = defaultdict(int)
    for kind, s in stats.items():
        summary["by_type"][kind] = {"n": s["n"], "catch_rate": pct(s["caught"], s["n"]),
                                    "right_kind_rate": pct(s["right_kind"], s["n"])}
        if kind in ("number_perturb", "value_swap"):
            summary["by_type"][kind]["restored_by_correction"] = pct(s["restored"], s["n"])
        for k in ("n", "caught", "right_kind"):
            tot[k] += s[k]
    summary["overall"] = {"n": tot["n"], "catch_rate": pct(tot["caught"], tot["n"]),
                          "right_kind_rate": pct(tot["right_kind"], tot["n"])}
    out = OUT if seed == 0 else OUT.with_name(f"verifier_injection_seed{seed}.json")
    out.write_text(json.dumps(summary, indent=1))
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / f"injection_unrestored_seed{seed}.json").write_text(json.dumps(unrestored, indent=1, ensure_ascii=False))
    (ROOT / "logs" / f"injection_misses_seed{seed}.json").write_text(json.dumps(misses, indent=1, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    main()
