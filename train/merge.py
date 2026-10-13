"""Merge a LoRA adapter into Qwen3-8B so vLLM can serve it as a plain model (step D1).

Usage: python train/merge.py models/sft-pilot models/sft-pilot-merged   (CPU is fine; ~2 min)
"""
import sys

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE = "Qwen/Qwen3-8B"


def main():
    adapter, out = sys.argv[1], sys.argv[2]
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16)
    model = PeftModel.from_pretrained(model, adapter).merge_and_unload()
    model.save_pretrained(out, safe_serialization=True)
    AutoTokenizer.from_pretrained(adapter).save_pretrained(out)
    print(f"merged {adapter} -> {out}")


if __name__ == "__main__":
    main()
