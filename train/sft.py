"""Phase 2.5 step B: LoRA SFT of Qwen3-8B for NL -> QuerySpec.

Prompt = the student chat prompt (system prompt with the schema description + question, thinking
off), exactly what vLLM renders at inference. Completion = the spec JSON. Loss on completion only.

Run on ONE GPU from 4-7, with the teacher stopped:
  CUDA_VISIBLE_DEVICES=4 python train/sft.py --out models/sft-pilot --epochs 2
"""
import argparse
import json
import sys
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from query.prompt import build_messages  # noqa: E402

BASE = "Qwen/Qwen3-8B"


def load(path: Path, tok) -> Dataset:
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    return Dataset.from_list([{
        "prompt": tok.apply_chat_template(build_messages(r["question"], few_shot=False), tokenize=False,
                                          add_generation_prompt=True, enable_thinking=False),
        "completion": json.dumps(r["spec"]) + tok.eos_token,
    } for r in rows])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default=str(ROOT / "data" / "train.jsonl"))
    parser.add_argument("--val", default=str(ROOT / "data" / "val.jsonl"))
    parser.add_argument("--out", required=True)
    parser.add_argument("--epochs", type=float, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch", type=int, default=16)
    args = parser.parse_args()

    tok = AutoTokenizer.from_pretrained(BASE)
    assert tok.eos_token == "<|im_end|>", tok.eos_token
    train, val = load(Path(args.train), tok), load(Path(args.val), tok)
    print(f"train {len(train)} | val {len(val)}")

    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16, attn_implementation="sdpa")
    config = SFTConfig(
        output_dir=args.out,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=0.05,  # a float in [0, 1) is a ratio of total steps
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        bf16=True,
        max_length=1024,
        completion_only_loss=True,
        logging_steps=5,
        eval_strategy="steps",
        eval_steps=25,
        save_strategy="no",
        report_to="tensorboard",
        seed=0,
    )
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM")
    trainer = SFTTrainer(model=model, args=config, train_dataset=train, eval_dataset=val,
                         processing_class=tok, peft_config=lora)
    trainer.train()
    trainer.save_model(args.out)
    tok.save_pretrained(args.out)
    metrics = trainer.evaluate()
    print("final eval:", metrics)
    (Path(args.out) / "train_summary.json").write_text(json.dumps(
        {"args": vars(args), "final_eval": metrics, "log_history": trainer.state.log_history}, indent=1))


if __name__ == "__main__":
    main()
