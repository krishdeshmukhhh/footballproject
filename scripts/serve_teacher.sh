#!/usr/bin/env bash
# Serve the Qwen3-32B teacher on ONE GPU (cluster allows only GPUs 4-7, one at a time).
# Usage: GPU=5 scripts/serve_teacher.sh   (default GPU=4)
set -euo pipefail
GPU="${GPU:-4}"
[[ "$GPU" =~ ^[4-7]$ ]] || { echo "GPU must be one of 4-7, got $GPU" >&2; exit 1; }

# A busy GPU is refused, unless SHARE=1 and every process on it is ours (e.g. teacher + student on
# one GPU, with GPU_MEM fractions that add up to < 0.9).
for pid in $(nvidia-smi -i "$GPU" --query-compute-apps=pid --format=csv,noheader); do
  owner=$(ps -o user= -p "$pid" 2>/dev/null || echo "?")
  if [[ "${SHARE:-0}" != 1 || "$owner" != "$USER" ]]; then
    echo "GPU $GPU is in use (pid $pid, user $owner); pick another or set SHARE=1 for your own processes" >&2; exit 1
  fi
done

cd "$(dirname "$0")/.."
export CUDA_VISIBLE_DEVICES="$GPU"
# vLLM's optional FlashInfer sampler JIT-compiles CUDA at startup and fails here (nvcc/header
# mismatch); the default sampler needs no compilation. Attention uses precompiled FlashAttention.
export VLLM_USE_FLASHINFER_SAMPLER=0
export PATH="$PWD/.venv/bin:$PATH"
exec vllm serve Qwen/Qwen3-32B \
  --port "${PORT:-8000}" \
  --max-model-len "${MAX_LEN:-8192}" \
  --gpu-memory-utilization "${GPU_MEM:-0.85}"
