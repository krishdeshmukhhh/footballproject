"""Phase 3 step 3: hallucinated-number rate, naive LLM vs the full pipeline, on the same questions.

naive     Qwen3-32B with the whole player table (players with 90+ minutes, ~31k tokens of CSV) and the
          pipeline's conventions in its prompt, answering directly. No query layer, no verification.
pipeline  student spec -> executed result -> Qwen3-32B answer -> verifier/corrector (query/answer.py).

Both are scored against the GROUND-TRUTH result (the expected spec, executed), with the same verifier.
A number counts as hallucinated if it matches neither the ground-truth rows nor any true tournament stat
of the entity it is attached to (so citing other true numbers is not penalised).

Questions: generated test split + dev/hard (never the hand-written set), restricted for the comparison
to what the naive model can fairly answer from its table: player questions with no stage/opponent filter
whose ground-truth players all have 90+ minutes.

Requires the teacher on :8000 with MAX_LEN=32768 and the student on :8001 (they can share one GPU).
Usage: python -m eval.hallucination
"""
import asyncio
import json
from pathlib import Path

from openai import AsyncOpenAI

from query import llm
from query.answer import ANSWER_URL, aanswer, log_catch
from query.compare import spec_key
from query.executor import DEFAULT_MIN_MINUTES, execute, load_tables
from query.schema import parse_spec
from query.verify import correct, verify

ROOT = Path(__file__).resolve().parents[1]
DATASETS = [ROOT / "data" / "test.jsonl", ROOT / "eval" / "dev_hard.jsonl"]
OUT = ROOT / "eval" / "hallucination.json"
TABLE_MIN_MINUTES = 90
COLUMNS = ["player", "team", "position_group", "matches", "minutes", "goals", "non_penalty_goals", "assists", "shots",
           "xg", "npxg", "key_passes", "passes_attempted", "passes_completed", "progressive_passes",
           "progressive_carries", "pressures", "pressured_passes_attempted", "pressured_passes_completed",
           "shot_creating_actions", "xt_added"]


def naive_system_prompt() -> str:
    _, players = load_tables()
    table = players[players["minutes"] >= TABLE_MIN_MINUTES][COLUMNS].round({"minutes": 1, "xg": 2, "npxg": 2,
                                                                            "xt_added": 3})
    return f"""You are a football analyst. Answer questions about the 2022 World Cup using ONLY the table below
(tournament totals per player, players with at least {TABLE_MIN_MINUTES} minutes). Give exact numbers.

Conventions: per-90 = total / minutes * 90, rounded to 2 decimals. Pass completion % = completed / attempted * 100.
Rankings that are per-90, percentages or "fewest" only include players with at least {DEFAULT_MIN_MINUTES} minutes
unless the question sets a threshold. Position groups: GK goalkeepers, CB centre-backs, FB full-backs/wing-backs,
DM/CM/AM defensive/central/attacking midfielders, W wingers, ST strikers; defenders = CB+FB, midfielders = DM+CM+AM,
forwards = W+ST. Team totals are the sum of their players. Answer in one to three sentences or a short list.

{table.to_csv(index=False)}"""


def naive_answerable(spec: dict, rows: list[dict]) -> bool:
    """Player questions with tournament-wide scope whose answer rows are all in the naive model's table.
    Team questions are excluded: the table omits players under 90 minutes, so even a perfectly summed
    team total could come out short, which would be the table's fault, not the model's."""
    f = spec["filters"]
    if f["stages"] or f["opponents"] or spec["group_by"] == "team":
        return False
    return all(r["minutes"] >= TABLE_MIN_MINUTES for r in rows)


def extra_truth(answer_entities: list[str]) -> dict:
    """Every true tournament number for each player mentioned, so true-but-unasked stats are not hallucinations."""
    _, players = load_tables()
    by_name = players.set_index("player")
    out = {}
    for key in answer_entities:
        kind, name = key.split(":", 1)
        if kind == "player" and name in by_name.index:
            p = by_name.loc[name]
            exact = [float(p[c]) for c in COLUMNS[3:]]  # stored totals
            exact += [float(p[c]) / p["minutes"] * 90 for c in COLUMNS[5:] if p["minutes"] > 0]  # unrounded per-90
            for num, den in [("passes_completed", "passes_attempted"),
                             ("pressured_passes_completed", "pressured_passes_attempted")]:
                if p[den] > 0:
                    exact.append(100 * p[num] / p[den])  # unrounded percentages
            out[key] = exact
    return out


def score(answer: str, gold: dict, question: str):
    first = verify(answer, gold, question)
    return verify(answer, gold, question, extra_truth=extra_truth(first.entities_found))


async def run_naive(rows, client, sem, system):
    async def one(r):
        async with sem:
            resp = await client.chat.completions.create(
                model=llm._model("teacher"), temperature=0.7, max_tokens=400, seed=0,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": r["question"]}],
                extra_body={"chat_template_kwargs": {"enable_thinking": False}})
        return resp.choices[0].message.content.strip()
    return await asyncio.gather(*(one(r) for r in rows))


async def run_pipeline(rows, sem):
    answer_client = AsyncOpenAI(base_url=ANSWER_URL, api_key="local", timeout=600)
    query_client = AsyncOpenAI(base_url=llm.BACKENDS["student"], api_key="local", timeout=600)

    async def one(r):
        async with sem:
            return await aanswer(r["question"], "student", source="pipeline_eval",
                                 answer_client=answer_client, query_client=query_client)
    return await asyncio.gather(*(one(r) for r in rows))


def rate(flags) -> float:
    flags = list(flags)
    return round(100 * sum(flags) / len(flags), 1) if flags else None


async def main_async():
    rows = [json.loads(line) for p in DATASETS for line in p.read_text().splitlines() if line.strip()]
    gold = [execute(parse_spec(r["spec"])) for r in rows]
    subset = [i for i, (r, g) in enumerate(zip(rows, gold)) if naive_answerable(g["spec"], g["rows"])]
    print(f"{len(rows)} questions, {len(subset)} answerable from the naive model's table")

    sem = asyncio.Semaphore(48)
    client = AsyncOpenAI(base_url=ANSWER_URL, api_key="local", timeout=600)
    naive_answers = await run_naive([rows[i] for i in subset], client, sem, naive_system_prompt())
    pipeline_out = await run_pipeline(rows, sem)

    records = []
    for i, (r, g, p) in enumerate(zip(rows, gold, pipeline_out)):
        rec = {"question": r["question"], "in_subset": i in subset, "gold_rows": g["rows"], "pipeline_type": p["type"]}
        if p["type"] == "answer":
            raw_gold = score(p["raw_answer"], g, r["question"])
            body = p["answer"].split("\n\n⚠ Verification")[0]  # corrected text, without the flag note
            final_gold = score(body, g, r["question"])
            rec |= {"pipeline_raw": p["raw_answer"], "pipeline_final": p["answer"],
                    "spec_correct": spec_key(p["spec"]) == spec_key(r["spec"]),
                    "pipeline_self_check_ok": p["verification"]["ok"],
                    "pipeline_raw_halluc": raw_gold.hallucinated_number,
                    "pipeline_raw_issues": [i.__dict__ for i in raw_gold.issues],
                    "pipeline_final_halluc": final_gold.hallucinated_number,
                    "pipeline_final_flagged": "⚠ Verification" in p["answer"]}
        else:
            rec["pipeline_message"] = p.get("message")
        records.append(rec)
    for i, ans in zip(subset, naive_answers):
        v = score(ans, gold[i], rows[i]["question"])
        records[i] |= {"naive": ans, "naive_halluc": v.hallucinated_number, "naive_issues": [x.__dict__ for x in v.issues]}
        if not v.ok:
            log_catch({"source": "naive_baseline", "question": rows[i]["question"], "spec": gold[i]["spec"],
                       "interpretation": gold[i]["interpretation"], "rows": gold[i]["rows"], "raw_answer": ans,
                       "issues": [x.__dict__ for x in v.issues], "corrected_answer": correct(ans, v, gold[i])})

    sub = [records[i] for i in subset]
    answered = [r for r in sub if r["pipeline_type"] == "answer"]
    summary = {
        "n_questions": len(rows), "n_naive_answerable": len(subset),
        "naive": {"hallucinated_number_rate": rate(r["naive_halluc"] for r in sub),
                  "any_issue_rate": rate(bool(r["naive_issues"]) for r in sub)},
        "pipeline_on_subset": {
            "answered": len(answered), "did_you_mean_or_error": len(sub) - len(answered),
            "spec_correct_rate": rate(r["spec_correct"] for r in answered),
            "raw_hallucinated_number_rate": rate(r["pipeline_raw_halluc"] for r in answered),
            "raw_hallucinated_number_rate_when_spec_correct": rate(
                r["pipeline_raw_halluc"] for r in answered if r["spec_correct"]),
            "final_hallucinated_number_rate": rate(r["pipeline_final_halluc"] for r in answered),
            "final_unflagged_hallucination_rate": rate(
                r["pipeline_final_halluc"] and not r["pipeline_final_flagged"] for r in answered),
            "self_check_flag_rate": rate(not r["pipeline_self_check_ok"] for r in answered)},
        "pipeline_all_questions": {
            "answered": sum(r["pipeline_type"] == "answer" for r in records),
            "spec_correct_rate": rate(r["spec_correct"] for r in records if r["pipeline_type"] == "answer"),
            "raw_hallucinated_number_rate": rate(r["pipeline_raw_halluc"] for r in records if r["pipeline_type"] == "answer"),
            "self_check_flag_rate": rate(not r["pipeline_self_check_ok"] for r in records if r["pipeline_type"] == "answer")},
    }
    OUT.write_text(json.dumps(summary, indent=1))
    (ROOT / "logs" / "hallucination_records.json").write_text(json.dumps(records, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main_async())
