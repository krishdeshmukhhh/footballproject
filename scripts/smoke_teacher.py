"""One guided-JSON request to the local vLLM teacher, to confirm the serving setup works.

Usage: python scripts/smoke_teacher.py [--port 8000]
"""
import argparse
import json
import time

from openai import OpenAI

SCHEMA = {
    "type": "object",
    "properties": {
        "metric": {"type": "string", "enum": ["progressive_passes", "pressures", "xt_added"]},
        "position_group": {"type": "string", "enum": ["GK", "CB", "FB", "DM", "CM", "AM", "W", "ST"]},
        "limit": {"type": "integer", "minimum": 1, "maximum": 20},
    },
    "required": ["metric", "position_group", "limit"],
    "additionalProperties": False,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    client = OpenAI(base_url=f"http://localhost:{args.port}/v1", api_key="local")
    model = client.models.list().data[0].id
    start = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Translate to a query spec: which 5 centre-backs pressed the most?"}],
        temperature=0,
        max_tokens=128,
        response_format={"type": "json_schema", "json_schema": {"name": "query_spec", "schema": SCHEMA}},
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    text = resp.choices[0].message.content
    print(f"model: {model}\nlatency: {time.perf_counter() - start:.2f}s\nraw: {text}")
    print("parsed:", json.loads(text))


if __name__ == "__main__":
    main()
