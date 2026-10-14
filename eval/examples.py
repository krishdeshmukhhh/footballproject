"""Render eval/examples.md: real verifier catches from the final naive-baseline run.

Each example is picked by question and an exact excerpt of the saved naive answer. The true values, the
issues and the corrections are all recomputed from the data and the current verifier, so the file
regenerates with everything else (python -m eval.report runs this).

Usage: python -m eval.examples
"""
import json
from pathlib import Path

from query.executor import execute, load_tables
from query.schema import METRICS, parse_spec
from query.verify import _fmt, verify

from eval.hallucination import DATASETS, RECORDS, extra_truth

OUT = Path(__file__).parent / "examples.md"

# (headline, question, excerpt of the naive answer, true values to show: column names, or "a/b" for a ratio as %)
EXAMPLES = [
    ("A percentage that contradicts the model's own fraction",
     "lowest pass completion % among strikers",
     "the lowest pass completion % is **-0.069** by Robert Lewandowski (Poland) with 92.4% pass completion "
     "(91 attempted, 65 completed)",
     [("Robert Lewandowski", "passes_completed/passes_attempted")]),
    ("A wrong fraction, for a player outside the position group",
     "Which three central midfielders had the highest pass completion percentages in the 2022 World Cup?",
     "**Rodri (Spain)** - 98.3% (644/655)",
     [("Rodri", "passes_completed/passes_attempted"), ("Rodri", "position_group")]),
    ("Wrong arithmetic on true inputs",
     "Who were the most aggressive pressers among defenders per 90, at least 200 minutes?",
     "**Christian Pulisic (USA, W)** - 44 pressures in 315 minutes = **12.98 per 90**",
     [("Christian Pulisic", "pressures"), ("Christian Pulisic", "minutes"), ("Christian Pulisic", "pressures_p90"),
      ("Christian Pulisic", "position_group")]),
    ("Another player's number (attribution), rewritten in place",
     "Which 5 Canada players had the most non-penalty xG?",
     "2. **Cyle Larin** (ST) - 0.81",
     [("Cyle Larin", "npxg"), ("Jonathan David", "npxg")]),
    ("Right numbers in the wrong order, plus players who are not in the top 5",
     "Who were the top 5 players for progressive carries in the 2022 World Cup?",
     "1. **Lionel Messi (Argentina, ST)** - 61 progressive carries  \n2. **Hakim Ziyech (Morocco, W)** - 28  \n"
     "3. **Lautaro Martínez (Argentina, ST)** - 6  \n4. **Álvaro Morata (Spain, ST)** - 7  \n"
     "5. **Kylian Mbappé (France, W)** - 71",
     [("Hakim Ziyech", "progressive_carries"), ("Lautaro Martínez", "progressive_carries"),
      ("Álvaro Morata", "progressive_carries")]),
    ("A player who was not at the tournament",
     "Which 3 central midfielders had the highest pass completion percentage?",
     "1. **Péter Gulácsi** (Hungary) - 97.1% (27/28)\n2. **Andreas Christensen** (Denmark) - 96.7% (236/244)",
     [("Andreas Christensen", "passes_completed/passes_attempted"), ("Andreas Christensen", "position_group")]),
    ("Players from the wrong country",
     "Who were the 5 Canadian players with the least number of shots per 90 minutes in the 2022 World Cup?",
     "1. **Nico Schlotterbeck** - 0.00 shots/90  \n2. **Joe Allen** - 0.00 shots/90",
     [("Nico Schlotterbeck", "team"), ("Joe Allen", "team")]),
    ("Partly caught: totals presented as per-90 values",
     "Which 5 Denmark players had the most progressive passes per 90?",
     "1. **Pierre-Emile Højbjerg** - 43.00 progressive passes/90  \n2. **Kasper Schmeichel** - 1.00 progressive passes/90  \n"
     "3. **Andreas Christensen** - 32.00 progressive passes/90",
     [("Pierre-Emile Højbjerg", "progressive_passes"), ("Pierre-Emile Højbjerg", "progressive_passes_p90"),
      ("Andreas Christensen", "progressive_passes"), ("Andreas Christensen", "progressive_passes_p90")]),
]
NOTES = {  # what the example shows that the issue list alone does not
    "A player who was not at the tournament": "Péter Gulácsi is not in the dataset, so the name check cannot see him "
                                              "(names are matched against tournament players). His invented numbers "
                                              "are still flagged.",
    "Players from the wrong country": "The verifier matched \"Joshua\" in a later line to Joshua Kimmich, the only "
                                      "Joshua in the data, so one of the issues names the wrong player. The answer is "
                                      "still correctly flagged.",
    "Partly caught: totals presented as per-90 values": "Missed: 43.00 and 32.00 are the players' tournament totals, "
                                                        "not per-90 values. A number counts as hallucinated only if it "
                                                        "is not any true stat of its player, so these pass. Only the "
                                                        "order is caught.",
}


def label(col: str) -> str:
    if col.endswith("_p90"):
        return METRICS[col[:-4]]["label"] + " per 90"
    return METRICS[col]["label"] if col in METRICS else col.replace("_", " ")


def true_value(players, player: str, col: str) -> str:
    p = players.set_index("player").loc[player]
    if "/" in col:
        a, b = col.split("/")
        return f"{label(a)} / {label(b)} = {int(p[a])}/{int(p[b])} = {100 * p[a] / p[b]:.1f}%"
    v = p[col]
    if isinstance(v, float):
        v = round(v, 2) if col.endswith("_p90") or col == "npxg" else (int(v) if v == int(v) else round(v, 1))
    return f"{label(col)}: {_fmt(v)}"


def render() -> str:
    records = {r["question"]: r for r in json.loads(RECORDS.read_text())}
    gold_specs = {json.loads(line)["question"]: json.loads(line)["spec"]
                  for p in DATASETS for line in p.read_text().splitlines()}
    _, players = load_tables()
    out = ["# Verifier catches: real examples", "",
           "Answers from the final naive-baseline run (Qwen3-32B with the stats table in its context, no query layer),",
           "scored against the ground-truth result exactly as `eval/hallucination.py` scores them. The pipeline's own",
           "answers produced no catches against ground truth apart from the one mislabelled question described in",
           "`eval/README.md`, so all of these are naive answers.", "",
           "Generated by `python -m eval.examples` (also run by `python -m eval.report`). Each excerpt is quoted",
           "verbatim; the true values, the issues and the corrections are recomputed from the data and the current",
           "verifier. In every case, whatever the verifier cannot rewrite is flagged, and the verified result is",
           "appended to the answer.", ""]
    for n, (headline, question, excerpt, truths) in enumerate(EXAMPLES, 1):
        r = records[question]
        answer = r["naive"]
        start = answer.index(excerpt)
        end = start + len(excerpt)
        gold = execute(parse_spec(gold_specs[question]))
        first = verify(answer, gold, question)
        v = verify(answer, gold, question, extra_truth=extra_truth(first.entities_found))
        inside = [i for i in v.issues if i.span and start <= i.span[0] < end]
        outside = len({i.detail for i in v.issues} - {i.detail for i in inside})
        rows = "; ".join(f"{g['rank']}. {g['player']} ({g['team']}) {_fmt(g['value'])}" for g in gold["rows"])

        out += [f"## {n}. {headline}", "", f"**Question:** {question}", "",
                "**Bad text** (excerpt of the naive answer):", ""]
        out += ["> " + line for line in excerpt.split("\n")]
        out += ["", "**True values:**", ""]
        out += [f"- {player}: {true_value(players, player, col)}" for player, col in truths]
        out += [f"- Ground truth: {rows}", f"- Ground-truth spec, in words: {gold['interpretation']}",
                "", "**What the verifier did:**", ""]
        seen = set()
        for i in sorted(inside, key=lambda i: i.span):
            if i.detail in seen:
                continue
            seen.add(i.detail)
            action = f"rewrote `{i.claim}` to `{i.expected}`" if i.expected else "flagged"
            out.append(f"- {i.kind}: \"{i.claim}\": {i.detail}. **{action.capitalize()}.**")
        if outside:
            out.append(f"- Plus {outside} other issue{'s' if outside > 1 else ''} elsewhere in the same answer.")
        fixed = excerpt
        for i in sorted((i for i in inside if i.expected), key=lambda i: -i.span[0]):
            a, b = i.span[0] - start, i.span[1] - start
            fixed = fixed[:a] + i.expected + fixed[b:]
        if fixed != excerpt:
            out += ["", "Corrected excerpt:", ""] + ["> " + line for line in fixed.split("\n")]
        if headline in NOTES:
            out += ["", f"**Note:** {NOTES[headline]}"]
        out.append("")
    return "\n".join(out)


def main():
    OUT.write_text(render())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
