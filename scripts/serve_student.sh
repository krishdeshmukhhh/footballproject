#!/usr/bin/env bash
# Serve an 8B model (base Qwen3-8B or a merged fine-tune) on port 8001, on ONE GPU from 4-7.
# Usage: GPU=4 scripts/serve_student.sh models/sft-v1-merged    (default model: Qwen/Qwen3-8B)
set -euo pipefail
GPU="${GPU:-4}"
MODEL="${1:-Qwen/Qwen3-8B}"
[[ "$GPU" =~ ^[4-7]$ ]] || { echo "GPU must be one of 4-7, got $GPU" >&2; exit 1; }

busy=$(nvidia-smi -i "$GPU" --query-compute-apps=pid --format=csv,noheader | wc -l)
[[ "$busy" -eq 0 ]] || { echo "GPU $GPU already has $busy process(es); pick another" >&2; exit 1; }

cd "$(dirname "$0")/.."
export CUDA_VISIBLE_DEVICES="$GPU"
# See serve_teacher.sh: FlashInfer's JIT sampler does not build on this box.
export VLLM_USE_FLASHINFER_SAMPLER=0
export PATH="$PWD/.venv/bin:$PATH"
exec vllm serve "$MODEL" \
  --port "${PORT:-8001}" \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.85
