"""Phase 3: the full pipeline. Question -> spec -> executed result -> LLM answer -> verified answer.

The answer generator is the local Qwen3-32B (port 8000). The spec comes from QUERY_BACKEND (student
on :8001 by default here, teacher on :8000). Every verifier catch is appended to
logs/verifier_catches.jsonl with the raw answer, the issues and the corrected answer.

Usage: python -m query.answer "Who made the most progressive carries per 90 among wingers?"
"""
import asyncio
import datetime as dt
import json
import os
import sys
from pathlib import Path

from openai import AsyncOpenAI

from query import llm
from query.executor import ExecutionError, NameNotResolved, execute
from query.verify import correct, verify

ROOT = Path(__file__).resolve().parents[1]
CATCH_LOG = ROOT / "logs" / "verifier_catches.jsonl"
ANSWER_URL = os.environ.get("ANSWER_URL", "http://localhost:8000/v1")

ANSWER_PROMPT = """You are a football analyst answering questions about the 2022 World Cup.
You are given the question, how it was interpreted, and the verified result of a database query.
Answer using only the result: state each player or team in rank order with its exact value.
Do not compute new numbers and do not add statistics, players or teams that are not in the result.
Keep it short: one to three sentences, or a short list for five or more rows. Mention ties if any."""


def log_catch(record: dict) -> None:
    CATCH_LOG.parent.mkdir(exist_ok=True)
    with open(CATCH_LOG, "a") as fh:
        fh.write(json.dumps({"ts": dt.datetime.now().isoformat(timespec="seconds"), **record}, ensure_ascii=False) + "\n")


async def generate_answer(client: AsyncOpenAI, question: str, result: dict, temperature: float = 0.7) -> str:
    rows = [{k: v for k, v in r.items() if k != "position_group"} for r in result["rows"]]
    content = (f"Question: {question}\nInterpretation: {result['interpretation']}\n"
               f"Result ({result['metric_label']}):\n{json.dumps(rows, ensure_ascii=False)}")
    resp = await client.chat.completions.create(
        model=llm._model("teacher"),
        messages=[{"role": "system", "content": ANSWER_PROMPT}, {"role": "user", "content": content}],
        temperature=temperature, max_tokens=400, seed=0,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    return resp.choices[0].message.content.strip()


async def aanswer(question: str, backend: str | None = None, source: str = "pipeline",
                  answer_client: AsyncOpenAI | None = None, query_client: AsyncOpenAI | None = None) -> dict:
    backend = backend or os.environ.get("QUERY_BACKEND", "student")
    answer_client = answer_client or AsyncOpenAI(base_url=ANSWER_URL, api_key="local", timeout=300)
    query_client = query_client or AsyncOpenAI(base_url=llm.BACKENDS[backend], api_key="local", timeout=300)

    t = await llm.atranslate(query_client, question, backend)
    if t.spec is None:
        return {"type": "error", "question": question, "message": f"Could not parse the question ({t.error})."}
    try:
        result = execute(t.spec)
    except NameNotResolved as e:
        return {"type": "did_you_mean", "question": question, "message": str(e), "suggestions": e.suggestions,
                "spec": t.spec.canonical()}
    except ExecutionError as e:
        return {"type": "error", "question": question, "message": str(e), "spec": t.spec.canonical()}
    if not result["rows"]:
        return {"type": "empty", "question": question, "result": result,
                "answer": f"No matching data. Interpretation: {result['interpretation']}"}

    raw = await generate_answer(answer_client, question, result)
    v = verify(raw, result, question)
    final = correct(raw, v, result)
    out = {"type": "answer", "question": question, "spec": result["spec"], "interpretation": result["interpretation"],
           "result": result, "raw_answer": raw, "verification": v.to_dict(), "answer": final,
           "response": f"Interpretation: {result['interpretation']}\n\n{final}"}
    if not v.ok:
        log_catch({"source": source, "question": question, "spec": result["spec"],
                   "interpretation": result["interpretation"], "rows": result["rows"], "raw_answer": raw,
                   "issues": v.to_dict()["issues"], "corrected_answer": final})
    return out


def answer(question: str, backend: str | None = None) -> dict:
    return asyncio.run(aanswer(question, backend))


if __name__ == "__main__":
    out = answer(" ".join(sys.argv[1:]))
    print(out.get("response") or out.get("message"))
