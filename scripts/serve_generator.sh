#!/usr/bin/env bash
# Serve the independent question writer (a non-Qwen model) on port 8002, on ONE GPU from 4-7.
# It only writes questions for eval/independent_test.jsonl; it never sees the schema or any system's output.
# Usage: GPU=4 scripts/serve_generator.sh    (default model: mistralai/Mistral-Small-24B-Instruct-2501)
set -euo pipefail
GPU="${GPU:-4}"
MODEL="${1:-mistralai/Mistral-Small-24B-Instruct-2501}"
[[ "$GPU" =~ ^[4-7]$ ]] || { echo "GPU must be one of 4-7, got $GPU" >&2; exit 1; }

# A busy GPU is refused, unless SHARE=1 and every process on it is ours.
for pid in $(nvidia-smi -i "$GPU" --query-compute-apps=pid --format=csv,noheader); do
  owner=$(ps -o user= -p "$pid" 2>/dev/null || echo "?")
  if [[ "${SHARE:-0}" != 1 || "$owner" != "$USER" ]]; then
    echo "GPU $GPU is in use (pid $pid, user $owner); pick another or set SHARE=1 for your own processes" >&2; exit 1
  fi
done

cd "$(dirname "$0")/.."
export CUDA_VISIBLE_DEVICES="$GPU"
# See serve_teacher.sh: FlashInfer's JIT sampler does not build on this box.
export VLLM_USE_FLASHINFER_SAMPLER=0
export PATH="$PWD/.venv/bin:$PATH"
# HF-format weights only (the duplicate consolidated.safetensors is not downloaded).
exec vllm serve "$MODEL" \
  --port "${PORT:-8002}" \
  --tokenizer-mode "${TOKENIZER_MODE:-mistral}" \
  --config-format hf --load-format safetensors \
  --max-model-len "${MAX_LEN:-4096}" \
  --gpu-memory-utilization "${GPU_MEM:-0.85}"
