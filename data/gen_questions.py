"""Phase 2.5 step A3-A4: questions for each spec, via template + teacher paraphrases + drift filter.

For each spec (in data/specs.jsonl order):
  1. Render one plain template question (correct by construction, always kept).
  2. Ask the teacher (Qwen3-32B, thinking off, guided JSON) for 4 paraphrases in different styles.
  3. Re-translate every paraphrase with the teacher; keep it only if the spec it produces is the
     original spec (player names compared after resolution). The training target keeps the player
     names as the paraphrase wrote them.

Caveat: step 3 keeps only paraphrases the teacher already translates correctly, so the teacher's
accuracy on the generated test split is inflated by construction. Use eval/dev_hard.jsonl and the
hand-written set for an unbiased teacher-vs-student comparison.

Resumable: specs already in the output file are skipped, so `--specs 900` after `--specs 350`
only does the new 550.

Usage: python data/gen_questions.py --specs 350 [--concurrency 48]   -> data/questions_raw.jsonl
"""
import argparse
import asyncio
import hashlib
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from openai import AsyncOpenAI  # noqa: E402

from query.compare import spec_key  # noqa: E402
from query.llm import BACKENDS, _model, atranslate  # noqa: E402
from query.schema import STAGES  # noqa: E402

SPECS = ROOT / "data" / "specs.jsonl"
OUT = ROOT / "data" / "questions_raw.jsonl"

METRIC_PHRASES = {
    "goals": "goals", "non_penalty_goals": "non-penalty goals", "assists": "assists", "shots": "shots",
    "xg": "xG", "npxg": "non-penalty xG", "key_passes": "key passes", "passes_attempted": "passes attempted",
    "passes_completed": "completed passes", "pass_completion_pct": "pass completion percentage",
    "progressive_passes": "progressive passes", "progressive_carries": "progressive carries",
    "pressures": "pressures", "pressured_passes_attempted": "passes attempted under pressure",
    "pressured_passes_completed": "passes completed under pressure",
    "pressured_pass_completion_pct": "pass completion percentage under pressure",
    "shot_creating_actions": "shot-creating actions", "xt_added": "xT added", "minutes": "minutes played",
}
RATES = {"pass_completion_pct", "pressured_pass_completion_pct"}
GROUP_PLURAL = {"GK": "goalkeepers", "CB": "centre-backs", "FB": "full-backs", "DM": "defensive midfielders",
                "CM": "central midfielders", "AM": "attacking midfielders", "W": "wingers", "ST": "strikers"}
FAMILY_PLURAL = {("CB", "FB"): "defenders", ("AM", "CM", "DM"): "midfielders", ("ST", "W"): "forwards"}
KNOCKOUT = sorted(s for s in STAGES if s != "Group Stage")
STAGE_PHRASES = {"Group Stage": "the group stage", "Round of 16": "the round of 16", "Quarter-finals": "the quarter-finals",
                 "Semi-finals": "the semi-finals", "3rd Place Final": "the third-place match", "Final": "the final"}

PARAPHRASE_SCHEMA = {
    "type": "object",
    "properties": {"paraphrases": {"type": "array", "minItems": 4, "maxItems": 4,
                                   "items": {"type": "string", "minLength": 8, "maxLength": 220}}},
    "required": ["paraphrases"], "additionalProperties": False,
}
PARAPHRASE_PROMPT = """You rewrite football statistics questions about the 2022 World Cup.
Write 4 paraphrases of the question that ask for exactly the same thing.

Keep every constraint: the statistic, total vs per 90, positions, team, opponent, tournament stage,
minutes threshold, how many results, and most vs fewest. Do not add, drop or loosen anything.
Keep player names exactly as written. Team names may become nationalities (France -> French).

Styles, one each:
1. natural and fluent
2. short and casual, like a chat message
3. phrased the way a football analyst or fan would say it (synonyms are fine if the meaning is identical)
4. casual, all lowercase, with one or two small typos (never in player names)"""


def _join(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _positions(groups, singular=False):
    phrase = FAMILY_PLURAL.get(tuple(sorted(groups))) or _join([GROUP_PLURAL[g] for g in groups])
    return phrase[:-1] if singular and phrase.endswith("s") else phrase


def _context(f) -> str:
    out = ""
    if f["stages"]:
        out += " in " + ("the knockout rounds" if sorted(f["stages"]) == KNOCKOUT
                         else _join([STAGE_PHRASES[s] for s in f["stages"]]))
    if f["opponents"]:
        out += " against " + _join(f["opponents"])
    if f["min_minutes"]:
        out += f" (minimum {f['min_minutes']} minutes)"
    return out


def template_question(spec: dict) -> str:
    f, m = spec["filters"], spec["metric"]
    metric = METRIC_PHRASES[m] + (" per 90" if spec["per90"] else "")
    if f["players"]:
        names = _join(f["players"])
        if len(f["players"]) > 1:
            return f"Compare {names} on {metric}{_context(f)}."
        if m == "minutes":
            return f"How many minutes did {names} play{_context(f)}?"
        if m in RATES or spec["per90"]:
            return f"What was {names}'s {metric}{_context(f)}?"
        return f"How many {metric} did {names} have{_context(f)}?"

    high = spec["sort"] == "desc"
    order = ("highest" if high else "lowest") if m in RATES else ("most" if high else "fewest")
    n = spec["limit"]
    # Half of the limit-5 specs leave the number out ("Which players had the most ..."), which is what
    # teaches the default of 5 for plural questions. Deterministic per spec.
    digest = int(hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest(), 16)
    count = "" if n == 5 and digest % 2 == 0 else f"{n} "
    if spec["group_by"] == "team":
        subject = "team" if n == 1 else f"{count}teams"
        whose = f" from their {_positions(f['position_groups'])}" if f["position_groups"] else ""
        return f"Which {subject} had the {order} {metric}{whose}{_context(f)}?"

    team = f"{f['teams'][0]} " if f["teams"] else ""
    if n == 1:
        who = _positions(f["position_groups"], singular=True) if f["position_groups"] else "player"
        return f"Which {team}{who} had the {order} {metric}{_context(f)}?"
    who = _positions(f["position_groups"]) if f["position_groups"] else "players"
    return f"Which {count}{team}{who} had the {order} {metric}{_context(f)}?"


async def paraphrase(client, model, question: str) -> list[str]:
    resp = await client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": PARAPHRASE_PROMPT}, {"role": "user", "content": question}],
        temperature=0.9, top_p=0.95, max_tokens=400,
        response_format={"type": "json_schema", "json_schema": {"name": "paraphrases", "schema": PARAPHRASE_SCHEMA}},
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    return json.loads(resp.choices[0].message.content)["paraphrases"]


async def process(rec: dict, client, model, sem) -> dict:
    target_key = spec_key(rec["spec"])
    template = template_question(rec["spec"])
    async with sem:
        try:
            texts = await paraphrase(client, model, template)
        except Exception as e:  # noqa: BLE001 - one bad generation should not stop the run
            texts, rec["paraphrase_error"] = [], repr(e)

    async def check(text):
        async with sem:
            t = await atranslate(client, text, "teacher")
        ok = t.spec is not None and spec_key(t.spec) == target_key
        return {"text": text, "teacher_spec": t.spec.canonical() if t.spec else None, "kept": ok}

    checks = await asyncio.gather(*(check(x) for x in [template, *texts]))
    return {"spec_id": rec["spec_id"], "split": rec["split"], "spec": rec["spec"],
            "template": checks[0], "paraphrases": checks[1:]}


async def main_async(args):
    specs = [json.loads(line) for line in SPECS.read_text().splitlines()][: args.specs]
    done = {json.loads(line)["spec_id"] for line in OUT.read_text().splitlines()} if OUT.exists() else set()
    todo = [r for r in specs if r["spec_id"] not in done]
    print(f"{len(done)} specs already done, {len(todo)} to go (concurrency {args.concurrency})")

    client = AsyncOpenAI(base_url=BACKENDS["teacher"], api_key="local", timeout=300)
    model = _model("teacher")
    sem = asyncio.Semaphore(args.concurrency)
    start, n_done, kept = time.time(), 0, 0
    with open(OUT, "a") as fh:
        for coro in asyncio.as_completed([process(r, client, model, sem) for r in todo]):
            res = await coro
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            n_done += 1
            kept += sum(p["kept"] for p in res["paraphrases"])
            if n_done % 50 == 0 or n_done == len(todo):
                print(f"  {n_done}/{len(todo)} specs, {kept} paraphrases kept, {time.time() - start:.0f}s", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--specs", type=int, required=True, help="process the first N specs of data/specs.jsonl")
    parser.add_argument("--concurrency", type=int, default=48)
    args = parser.parse_args()
    random.seed(0)
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
