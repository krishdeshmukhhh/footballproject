"""Independent test set, step 2: a non-Qwen model writes one casual fan question per spec.

The writer (Mistral Small 24B Instruct, scripts/serve_generator.sh, port 8002) gets a plain-English brief of each
spec: what is ranked or looked up, the statistic in everyday words, and each filter. It never sees the QuerySpec
schema, field names, position codes, the translation prompt, or any model's output. There is no teacher round-trip
filter: every question is kept as written (specs with an empty result were already dropped at sampling).

About a third of the questions (fixed in code per spec, before generation) ask for typos and slang. Player names are
always to be written exactly as given. Misspelled names are tested separately: for the misspelled subset the writer
gets the correct name, and the code then replaces it in the question with the planned misspelling.

Revision history (before any system was run on the set): in the first generation (kept in logs/, git-ignored) the
single-player brief read like a ranking prompt, so several lookups came back as rankings with no name, and the
misspelled subset, whose brief then carried the misspelled name, came back garbled. The single-player and comparison
briefs were made explicit and the misspelling moved into code; the second generation is final and kept in full.

Usage: python -m eval.independent_questions   -> eval/independent_test.jsonl, eval/independent_misspelled.jsonl
"""
import argparse
import asyncio
import json
import random
from pathlib import Path

from openai import AsyncOpenAI

from query.schema import STAGES

from eval.independent_specs import OUT as SPECS, OUT_MISSPELLED as MISSPELLED_SPECS, strip_accents

HERE = Path(__file__).parent
OUT = HERE / "independent_test.jsonl"
OUT_MISSPELLED = HERE / "independent_misspelled.jsonl"
URL = "http://localhost:8002/v1"
SEED = 2026
TYPO_SHARE = 1 / 3
TEMPERATURE = 0.8

STAT_WORDS = {
    "goals": "goals scored",
    "non_penalty_goals": "goals scored, not counting penalties",
    "assists": "assists",
    "shots": "shots taken",
    "xg": "expected goals (xG)",
    "npxg": "expected goals not counting penalties (non-penalty xG)",
    "key_passes": "key passes (passes straight before a teammate's shot)",
    "passes_attempted": "passes attempted",
    "passes_completed": "passes completed",
    "pass_completion_pct": "pass completion percentage",
    "progressive_passes": "progressive passes (completed passes that move the ball a good way up the pitch)",
    "progressive_carries": "progressive carries (running with the ball a good way up the pitch)",
    "pressures": "pressures applied to opponents on the ball (pressing)",
    "pressured_passes_attempted": "passes attempted while under pressure from an opponent",
    "pressured_passes_completed": "passes completed while under pressure from an opponent",
    "pressured_pass_completion_pct": "pass completion percentage while under pressure from an opponent",
    "shot_creating_actions": "shot-creating actions (the actions that lead to a shot)",
    "xt_added": "expected threat (xT) added by passing and carrying the ball",
    "minutes": "minutes played",
}
PCT = {"pass_completion_pct", "pressured_pass_completion_pct"}
POSITION_WORDS = {
    "GK": "goalkeepers", "CB": "centre-backs", "FB": "full-backs", "DM": "defensive midfielders",
    "CM": "central midfielders", "AM": "attacking midfielders", "W": "wingers", "ST": "strikers",
    "CB,FB": "defenders (centre-backs and full-backs together)",
    "AM,CM,DM": "midfielders (defensive, central and attacking midfielders together)",
    "ST,W": "forwards (strikers and wingers together)",
}
KNOCKOUT = sorted(s for s in STAGES if s != "Group Stage")
STAGE_WORDS = {"Group Stage": "the group stage", "Round of 16": "the round of 16",
               "Quarter-finals": "the quarter-finals", "Semi-finals": "the semi-finals",
               "3rd Place Final": "the third-place match", "Final": "the final"}

SYSTEM = """You write questions that football fans would type into a stats chatbot about the 2022 World Cup in Qatar.
You get a brief describing exactly what the fan wants to know. Write ONE question that asks for exactly that.

- Keep every detail of the brief: the statistic, whether it is a per-90 rate or a total, most vs fewest, how many
  results, positions, team, opponent, stage of the tournament, and any minimum minutes. Do not add or drop anything.
- Write player names exactly as they appear in the brief, letter for letter.
- Sound like a real fan, not a database query. Vary the wording.
- Reply with the question only: no quotes, no preamble, no answer."""
STYLE_PLAIN = "Style: casual, like a fan messaging a friend or posting online. Spell everything correctly."
STYLE_TYPOS = ("Style: very casual chat message with football slang, and include one or two typos or sloppy "
               "spellings in ordinary words (never in player names).")


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def brief(spec: dict, names: list[str] | None = None) -> str:
    """Plain-English description of a spec, in everyday words (no field names or codes)."""
    f, m = spec["filters"], spec["metric"]
    rate = spec["per90"] and m not in PCT and m != "minutes"
    stat = STAT_WORDS[m] + (", as a rate per 90 minutes played (not the total)" if rate else "")
    lines = []
    if f["players"]:
        names = names or f["players"]
        if len(names) == 1:
            lines.append(f"About: one named player, {names[0]}. The fan wants this player's own figure for the "
                         "statistic below (a lookup about this player, not a ranking). Name the player.")
        else:
            lines.append(f"About: comparing the named players {_join(names)}. The fan wants their figures for the "
                         "statistic below, side by side. Name every one of them.")
        lines.append(f"Statistic: {stat}")
    else:
        unit = "national teams as a whole (not individual players)" if spec["group_by"] == "team" else "players"
        lines.append(f"About: a ranking of {unit}")
        lines.append(f"Statistic: {stat}")
        high = spec["sort"] == "desc"
        lines.append("Order: " + ("highest / most" if high else "lowest / fewest"))
        lines.append("How many results: " + ("just the single top one" if spec["limit"] == 1 else
                                             f"the top {spec['limit']}"))
        if f["position_groups"]:
            pos = POSITION_WORDS[",".join(f["position_groups"])]
            lines.append(("Count only each team's " if spec["group_by"] == "team" else "Only ") + pos)
        if f["teams"]:
            lines.append(f"Only players from {_join(f['teams'])}")
        if f["min_minutes"] is not None:
            lines.append(f"Only players with at least {f['min_minutes']} minutes played")
    if f["stages"]:
        stage = "the knockout rounds (round of 16 onwards)" if sorted(f["stages"]) == KNOCKOUT \
            else _join([STAGE_WORDS[s] for s in f["stages"]])
        lines.append(f"Only matches in {stage}")
    if f["opponents"]:
        lines.append(f"Only matches against {_join(f['opponents'])}")
    return "\n".join(lines)


def clean(text: str) -> str:
    """The reply on one line, without wrapping quotes. The wording itself is never edited."""
    line = " ".join(x.strip() for x in text.strip().splitlines() if x.strip())
    if len(line) > 1 and line[0] == line[-1] and line[0] in "\"'":
        line = line[1:-1].strip()
    return line


def _replace_folded(question: str, old: str, new: str) -> str | None:
    """Replace `old` in the question, ignoring case and accents; None if it is not there. Character offsets carry
    over because stripping accents keeps one letter per letter (checked)."""
    if old in question:
        return question.replace(old, new, 1)
    folded_q, folded_o = strip_accents(question).lower(), strip_accents(old).lower()
    if len(folded_q) != len(question) or folded_o not in folded_q:
        return None
    i = folded_q.index(folded_o)
    return question[:i] + new + question[i + len(folded_o):]


def substitute(question: str, name: str, wrong: str) -> str:
    """Put the planned misspelling into the question: the whole name if the writer used it, else the misspelled
    word(s) alone (the writer may have used only the surname). Unchanged if the name is not there."""
    out = _replace_folded(question, name, wrong)
    if out is not None:
        return out
    out = question
    for right_w, wrong_w in zip(name.split(), wrong.split()):
        if right_w != wrong_w:
            out = _replace_folded(out, right_w, wrong_w) or out
    return out


def carries_misspelling(rec: dict) -> bool:
    """The question now holds the misspelled name, or (missing accents) the writer had already written it so."""
    return rec["question"] != rec["question_as_written"] or rec["misspelled_name"].lower() in rec["question"].lower()


async def write(client, model, sem, rec: dict, typos: bool, names=None) -> dict:
    user = brief(rec["spec"], names) + "\n\n" + (STYLE_TYPOS if typos else STYLE_PLAIN)
    async with sem:
        resp = await client.chat.completions.create(
            model=model, messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            temperature=TEMPERATURE, max_tokens=120, seed=SEED)
    raw = resp.choices[0].message.content or ""
    return {"question": clean(raw), "spec": rec["spec"], "result": rec["result"], "spec_id": rec["spec_id"],
            "style": "typos_slang" if typos else "casual", "brief": user, "raw": raw, "generator": model}


async def main_async(args):
    if args.resubstitute:  # re-apply the misspelling to the saved questions, without calling the model
        miss = [json.loads(line) for line in OUT_MISSPELLED.read_text().splitlines() if line.strip()]
        for rec in miss:
            rec["question"] = substitute(rec["question_as_written"], rec["name_in_spec"], rec["misspelled_name"])
            rec["name_copied"] = carries_misspelling(rec)
        OUT_MISSPELLED.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in miss))
        print(f"{sum(r['name_copied'] for r in miss)} of {len(miss)} carry the misspelling")
        return
    specs = [json.loads(line) for line in SPECS.read_text().splitlines() if line.strip()]
    misspelled = [json.loads(line) for line in MISSPELLED_SPECS.read_text().splitlines() if line.strip()]
    rng = random.Random(SEED)
    typo_flags = [rng.random() < TYPO_SHARE for _ in specs]

    client = AsyncOpenAI(base_url=URL, api_key="local", timeout=300)
    model = (await client.models.list()).data[0].id
    sem = asyncio.Semaphore(args.concurrency)
    main = await asyncio.gather(*(write(client, model, sem, r, t) for r, t in zip(specs, typo_flags)))
    # Misspelled subset: the writer gets the correct name (as in the main set), then the code swaps in its own
    # misspelling, so every question carries exactly the planned misspelling.
    miss = await asyncio.gather(*(write(client, model, sem, r, False) for r in misspelled))
    for rec, src in zip(miss, misspelled):
        rec |= {k: src[k] for k in ("player", "name_in_spec", "misspelled_name", "misspelling")}
        rec["question_as_written"] = rec["question"]
        rec["question"] = substitute(rec["question"], src["name_in_spec"], src["misspelled_name"])
        rec["name_copied"] = carries_misspelling(rec)

    for path, recs in ((OUT, main), (OUT_MISSPELLED, miss)):
        with open(path, "w") as fh:
            for rec in recs:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"{len(main)} questions -> {OUT} ({sum(typo_flags)} with typos and slang)")
    print(f"{len(miss)} questions -> {OUT_MISSPELLED} ({sum(r['name_copied'] for r in miss)} copy the misspelling)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=64)
    parser.add_argument("--resubstitute", action="store_true", help="re-apply misspellings to saved questions only")
    asyncio.run(main_async(parser.parse_args()))


if __name__ == "__main__":
    main()
