"""Phase 2.5 step E: score one served system on one or more question sets.

Systems: teacher (Qwen3-32B few-shot, :8000), base8b (Qwen3-8B few-shot, :8001),
sft / grpo (fine-tuned 8B, no few-shot, :8001). Serve the system first (one GPU at a time).

Metrics per dataset:
  valid_json     output parses and validates as a QuerySpec (guided decoding should make this ~100%)
  spec_acc       canonical spec equals the expected one (player names compared after resolution)
  exec_acc       executing it returns the same rows as the expected spec (ties order-insensitive)
  latency        p50/p95 of single sequential requests (on up to --latency-n questions)
Results merge into eval/results.json under results[system][dataset].

Usage: python -m eval.run_eval --system teacher --data data/test.jsonl eval/dev_hard.jsonl --gpu 4
"""
import argparse
import asyncio
import json
import statistics
import subprocess
import time
from pathlib import Path

from openai import AsyncOpenAI

from query import llm
from query.compare import results_match, spec_key
from query.executor import ExecutionError, execute
from query.schema import parse_spec

RESULTS = Path(__file__).parent / "results.json"
SYSTEMS = {  # name: (backend url key, few-shot prompt?)
    "teacher": ("teacher", True),
    "base8b": ("student", True),
    "sft": ("student", False),
    "grpo": ("student", False),
}


def gpu_memory_mib(gpu: int | None) -> int | None:
    if gpu is None:
        return None
    out = subprocess.run(["nvidia-smi", "-i", str(gpu), "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True)
    return int(out.stdout.strip()) if out.returncode == 0 else None


def run_rows(spec):
    try:
        return execute(spec)["rows"]
    except ExecutionError:
        return None


async def score(system: str, rows: list[dict], concurrency: int) -> tuple[dict, list[dict]]:
    backend, few_shot = SYSTEMS[system]
    client = AsyncOpenAI(base_url=llm.BACKENDS[backend], api_key="local", timeout=300)
    sem = asyncio.Semaphore(concurrency)

    async def one(r):
        async with sem:
            t = await llm.atranslate(client, r["question"], backend, few_shot=few_shot)
        expected = parse_spec(r["spec"])
        rec = {"question": r["question"], "raw": t.raw, "valid": t.spec is not None,
               "spec_ok": False, "exec_ok": False}
        if t.spec is not None:
            rec["spec_ok"] = spec_key(t.spec) == spec_key(expected)
            got, want = run_rows(t.spec), run_rows(expected)
            rec["exec_ok"] = got is not None and want is not None and results_match(got, want)
        return rec

    start = time.time()
    recs = await asyncio.gather(*(one(r) for r in rows))
    n = len(recs)
    return {
        "n": n,
        "valid_json": round(100 * sum(r["valid"] for r in recs) / n, 1),
        "spec_acc": round(100 * sum(r["spec_ok"] for r in recs) / n, 1),
        "exec_acc": round(100 * sum(r["exec_ok"] for r in recs) / n, 1),
        "throughput_qps": round(n / (time.time() - start), 2),
    }, recs


def latency(system: str, questions: list[str]) -> dict:
    backend, few_shot = SYSTEMS[system]
    times = [llm.translate(q, backend, few_shot=few_shot).latency_s for q in questions]
    return {"latency_p50_s": round(statistics.median(times), 3),
            "latency_p95_s": round(sorted(times)[int(0.95 * (len(times) - 1))], 3)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", required=True, choices=SYSTEMS)
    parser.add_argument("--data", nargs="+", required=True)
    parser.add_argument("--tag", default="", help="suffix for the system name, e.g. -pilot")
    parser.add_argument("--gpu", type=int, help="GPU the system is served on, to record memory use")
    parser.add_argument("--concurrency", type=int, default=48)
    parser.add_argument("--latency-n", type=int, default=50)
    args = parser.parse_args()

    results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    name = args.system + args.tag
    out = results.setdefault(name, {})
    for path in args.data:
        rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        if not rows:
            print(f"{path}: empty, skipped")
            continue
        summary, recs = asyncio.run(score(args.system, rows, args.concurrency))
        summary |= latency(args.system, [r["question"] for r in rows[: args.latency_n]])
        summary["gpu_memory_mib"] = gpu_memory_mib(args.gpu)
        out[Path(path).stem] = summary
        errors = [r for r in recs if not r["exec_ok"]]
        Path(f"logs/eval_{name}_{Path(path).stem}.json").write_text(json.dumps(errors, indent=1, ensure_ascii=False))
        print(f"{name:14} {Path(path).stem:12} {json.dumps(summary)}")
    RESULTS.write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
