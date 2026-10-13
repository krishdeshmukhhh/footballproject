"""NL -> QuerySpec via a local vLLM server (OpenAI-compatible API, guided JSON, thinking off).

QUERY_BACKEND=teacher (Qwen3-32B, port 8000, default) or student (fine-tuned 8B, port 8001).
Both use the same prompt and schema; only the endpoint differs.
"""
import os
import time
from dataclasses import dataclass, field
from functools import lru_cache

from openai import OpenAI
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
def _client(backend: str) -> tuple[OpenAI, str]:
    client = OpenAI(base_url=BACKENDS[backend], api_key="local")
    return client, client.models.list().data[0].id


def translate(question: str, backend: str | None = None) -> Translation:
    backend = backend or os.environ.get("QUERY_BACKEND", "teacher")
    client, model = _client(backend)
    start = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=build_messages(question),
        temperature=0,
        max_tokens=256,
        response_format={"type": "json_schema", "json_schema": {"name": "query_spec", "schema": json_schema()}},
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    latency = time.perf_counter() - start
    raw = resp.choices[0].message.content or ""
    t = Translation(question, backend, raw, latency, usage=resp.usage.model_dump() if resp.usage else {})
    try:
        t.spec = parse_spec(raw)
    except ValidationError as e:
        t.error = f"invalid spec: {e.errors()[0]['msg']}"
    return t
