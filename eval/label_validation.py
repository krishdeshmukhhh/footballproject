"""Label validation for the independent test set: does each question ask for exactly what its gold spec says?

Post hoc (run after the frozen results), and blind to every system's output: the checker sees only the question and
the plain-English reading of its gold spec (the interpretation echo from query/describe.py, as stored with the spec),
never the JSON spec or any model's translation. The checker is Mistral Small 24B Instruct, the same model that wrote
the questions, so its mistakes may be correlated with the writer's.

The rule and the prompt below were fixed and committed before the checker was run on any question. The validated
subset is the questions with verdict "yes". The 3 questions dropped before the frozen runs are checked too, as
known-bad controls; they are reported apart and never enter the subset.

Usage (generator served on port 8002, scripts/serve_generator.sh): python -m eval.label_validation
  -> eval/label_validation.json
"""
import asyncio
import json
from pathlib import Path

from openai import AsyncOpenAI

HERE = Path(__file__).parent
TEST = HERE / "independent_test.jsonl"
DROPPED = HERE / "independent_dropped.jsonl"
OUT = HERE / "label_validation.json"
URL = "http://localhost:8002/v1"
SEED = 2026
CONCURRENCY = 64

RULE = ("A question is validated if and only if the checker answers \"yes\": a careful analyst would turn the question "
        "into exactly the reading, under the conventions in the prompt. Anything ambiguous is \"no\". Decided before "
        "any question was checked; the subset is used as is.")

SYSTEM = """You check labels for a football statistics benchmark about the 2022 World Cup.
You get a fan's QUESTION and a READING: a plain-English description of exactly what the question is labelled as asking.
Decide whether the question asks for exactly what the reading says. Answer "yes" only if a careful analyst would turn
the question into exactly this reading. If the question is ambiguous between this reading and another, answer "no".

Check each of these:
1. Statistic: the same statistic. Synonyms are fine ("chances created" = key passes, "pass accuracy" = pass
   completion %, "pressing" = pressures). Completed and attempted passes are different statistics. A percentage is
   different from a count. "(simplified)" after progressive passes is only a label.
2. Total or per 90: "per 90", "per game", "per match", "on average" and similar mean a per-90 rate. Without such a
   word the question asks for a total.
3. Direction: most / highest versus fewest / lowest.
4. Players or teams: a reading about teams needs a question that ranks teams or countries as a whole. A reading
   about players needs a question about individual players.
5. How many: "The N players (or teams) with ..." needs a question asking for N of them. When N is 5 the question may
   give no number, as long as it asks for several (plural). "The player (or team) with ..." needs a question asking
   for a single one ("who had the most ...", "which team ..."). A reading of the form "<statistic> for <named
   players>" asks for those players' own figures (a lookup, or a comparison when there are several): no count applies.
6. Filters: the same positions, team ("playing for X" = the players' own team), opponent ("against X"), stage of the
   tournament and minutes threshold. A threshold marked "(default threshold)" is applied automatically: the question
   need not mention it. A question that adds or drops any other filter is a "no".
7. Positions: GK goalkeepers, CB centre-backs, FB full-backs, DM defensive midfielders, CM central midfielders, AM
   attacking midfielders, W wingers, ST strikers. "Defenders" = CB and FB; "midfielders" = DM, CM and AM;
   "forwards" or "attackers" = ST and W. "Counting only X" in a team reading means the team's total from its X.
8. Named players: the same players. A surname alone, a common short form, or a small misspelling is fine if it is
   clearly the same person; a different person is a "no".
9. Ignore "World Cup 2022", "Qatar", typos, slang and chatter: the whole dataset is that tournament.

Reply with JSON only: {"reason": "<one short sentence>", "verdict": "yes" or "no"}."""

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["reason", "verdict"],
          "properties": {"reason": {"type": "string", "maxLength": 300}, "verdict": {"enum": ["yes", "no"]}}}


def reading(rec: dict) -> str:
    return rec["result"]["interpretation"]


async def check(client, model, sem, rec: dict) -> dict:
    user = f"QUESTION: {rec['question']}\nREADING: {reading(rec)}"
    async with sem:
        resp = await client.chat.completions.create(
            model=model, messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            temperature=0, seed=SEED, max_tokens=200,
            response_format={"type": "json_schema", "json_schema": {"name": "verdict", "schema": SCHEMA}})
    raw = resp.choices[0].message.content or ""
    try:
        out = json.loads(raw)
        verdict, reason = out["verdict"], out["reason"]
    except (json.JSONDecodeError, KeyError):
        verdict, reason = "no", f"unparseable checker output: {raw[:200]}"
    return {"spec_id": rec["spec_id"], "question": rec["question"], "reading": reading(rec), "verdict": verdict,
            "reason": reason}


async def main_async():
    test = [json.loads(line) for line in TEST.read_text().splitlines() if line.strip()]
    dropped = [json.loads(line) for line in DROPPED.read_text().splitlines() if line.strip()]
    client = AsyncOpenAI(base_url=URL, api_key="local", timeout=300)
    model = (await client.models.list()).data[0].id
    sem = asyncio.Semaphore(CONCURRENCY)
    verdicts = await asyncio.gather(*(check(client, model, sem, r) for r in test))
    controls = await asyncio.gather(*(check(client, model, sem, r) for r in dropped))
    OUT.write_text(json.dumps({"checker": model, "rule": RULE, "prompt": SYSTEM, "temperature": 0, "seed": SEED,
                               "verdicts": verdicts, "controls_dropped": controls}, indent=1, ensure_ascii=False))
    yes = sum(v["verdict"] == "yes" for v in verdicts)
    print(f"{yes} of {len(verdicts)} validated -> {OUT} | dropped controls: "
          f"{[c['verdict'] for c in controls]}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
