"""NL -> QuerySpec via a local vLLM server (OpenAI-compatible API, guided JSON, thinking off).

QUERY_BACKEND=teacher (Qwen3-32B, port 8000, default) or student (fine-tuned 8B, port 8001).
Both use the same schema and system prompt; the teacher also gets the few-shot examples, the
student (trained without them) does not.
"""
import os
import time
from dataclasses import dataclass, field
from functools import lru_cache

from openai import AsyncOpenAI, OpenAI
from pydantic import ValidationError

from query.prompt import build_messages
from query.schema import QuerySpec, json_schema, parse_spec

BACKENDS = {
    "teacher": os.environ.get("TEACHER_URL", "http://localhost:8000/v1"),
    "student": os.environ.get("STUDENT_URL", "http://localhost:8001/v1"),
}


@dataclass
class Translation:
    question: str
    backend: str
    raw: str
    latency_s: float
    spec: QuerySpec | None = None
    error: str | None = None
    usage: dict = field(default_factory=dict)


@lru_cache(maxsize=None)
def _model(backend: str) -> str:
    return OpenAI(base_url=BACKENDS[backend], api_key="local").models.list().data[0].id


def _request(question: str, backend: str, few_shot: bool | None) -> dict:
    few_shot = backend != "student" if few_shot is None else few_shot
    return dict(
        model=_model(backend),
        messages=build_messages(question, few_shot=few_shot),
        temperature=0,
        max_tokens=256,
        response_format={"type": "json_schema", "json_schema": {"name": "query_spec", "schema": json_schema()}},
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )


def _finish(question, backend, resp, latency) -> Translation:
    raw = resp.choices[0].message.content or ""
    t = Translation(question, backend, raw, latency, usage=resp.usage.model_dump() if resp.usage else {})
    try:
        t.spec = parse_spec(raw)
    except ValidationError as e:
        t.error = f"invalid spec: {e.errors()[0]['msg']}"
    return t


def translate(question: str, backend: str | None = None, few_shot: bool | None = None) -> Translation:
    backend = backend or os.environ.get("QUERY_BACKEND", "teacher")
    client = OpenAI(base_url=BACKENDS[backend], api_key="local")
    start = time.perf_counter()
    resp = client.chat.completions.create(**_request(question, backend, few_shot))
    return _finish(question, backend, resp, time.perf_counter() - start)


async def atranslate(client: AsyncOpenAI, question: str, backend: str, few_shot: bool | None = None) -> Translation:
    start = time.perf_counter()
    resp = await client.chat.completions.create(**_request(question, backend, few_shot))
    return _finish(question, backend, resp, time.perf_counter() - start)
