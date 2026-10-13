# Project: Football Tactics Q&A - Grounded RAG over Match Event Data

## One-line pitch
A chat assistant that answers football tactics/scouting questions using real match event data, converts natural language into structured queries, and verifies every stat it states against ground truth before responding (catching and flagging hallucinations instead of confidently stating wrong numbers).

## Constraint: fully local, no API keys
Everything runs on one H200 server. No Claude API, no OpenAI API, no paid services. All LLM calls go to local models served with vLLM through its OpenAI-compatible endpoint. Do not add the `anthropic` package or any API key requirement.

- **Teacher model**: `Qwen/Qwen3-32B` (bf16, about 65 GB). Used for question paraphrasing, few-shot baseline, and final answer generation during development.
- **Student model**: `Qwen/Qwen3-8B`, fine-tuned for NL to query translation.
- Alternative teacher if setup time allows: `openai/gpt-oss-120b` (fits on one H200).
- For all JSON generation, disable thinking mode (`enable_thinking=False` in the chat template) and use vLLM guided JSON decoding with the query spec schema.

## Why this is the interesting part (read before building)
The naive version of this project is "dump football stats into an LLM's context and let it answer questions." That's a toy - LLMs are bad at exact arithmetic/aggregation over tabular data and will confidently hallucinate numbers.

The actual idea has three layers:
1. **NL → structured query**: convert a natural language question into a pandas filter/aggregation over event data, not free-text retrieval.
2. **Execute against ground truth**: run that query against the real DataFrame to get an exact, correct number.
3. **Verify before responding**: have the LLM generate a natural-language answer, then cross-check any numeric claims in that answer against the ground-truth result from step 2. If they don't match, flag or correct it.

This "generate then verify against computed ground truth" pattern is the whole point of the project. Do not skip step 3 - it's the hook for the writeup (before/after example of a caught hallucination).

## Data
- Source: [StatsBomb open data](https://github.com/statsbomb/open-data) via the `statsbombpy` Python package (free, no auth required).
- Scope to ONE competition/season to keep things fast and demoable (e.g., a single World Cup or league season - check `statsbombpy`'s `sb.competitions()` for what's available and pick one with rich data).
- Pull event-level data: passes, shots, pressures, carries, with x/y coordinates and player/team metadata.

## Derived metrics to precompute per player (store in a clean parquet/DataFrame)
- Progressive passes (passes that move the ball meaningfully closer to goal)
- Progressive carries
- Pressures applied
- Pressure-resistant passes (passes completed while under pressure)
- Shot-creating actions
- xT (expected threat) added, if feasible - simplify with a basic zone-based xT model if a full model is too much for scope
- Basic per-90 normalization for all of the above

Keep this layer simple and correct over comprehensive. A few well-defined metrics beat ten shaky ones.

## Architecture

```
[Next.js chat UI] → [API route / FastAPI backend]
                          ↓
                  [NL → Query layer] - local LLM (vLLM) translates question → pandas
                  filter/aggregation spec (guided JSON decoding)
                          ↓
                  [Execution layer] - runs the query against precomputed
                  DataFrame, returns exact numeric result(s)
                          ↓
                  [Answer generation] - local LLM (vLLM) turns the raw result into
                  a natural-language answer
                          ↓
                  [Verification layer] - extract numeric claims from the
                  generated answer, diff against the ground-truth result from
                  the execution layer, flag/correct mismatches
                          ↓
                  [Response] → returned to UI, optionally with a pass map /
                  heatmap image (matplotlib) if the question is spatial
```

## Tech stack
- **Backend**: Python, FastAPI, pandas, `statsbombpy`
- **LLM**: all local via vLLM. Qwen3-32B as teacher and answer generator, then a fine-tuned Qwen3-8B for NL to query translation (see Phase 2.5). No external APIs
- **Training**: PyTorch, transformers, peft, trl (SFT + GRPO) on 1x H200
- **Frontend**: Next.js + Tailwind, simple chat interface
- **Visuals**: matplotlib for pass maps/heatmaps, rendered as images served to the frontend
- **Deploy**: Vercel (frontend) + Railway or Render (backend), or serverless functions if kept lightweight

## Build order (weekend scope)

### Phase 1 - Data pipeline
1. Install `statsbombpy`, pull one competition's event data.
2. Explore schema, confirm data quality (some matches have gaps).
3. Compute the derived metrics table above, save as parquet.
4. Sanity-check numbers against known facts (e.g., a well-known player's known stat) to confirm the pipeline isn't silently wrong.

### Phase 2 - NL → structured query layer
1. Define a constrained query spec (JSON schema) the LLM must output: e.g., `{"metric": "progressive_passes", "filters": {"position": "fullback", "age_max": 23}, "sort": "desc", "limit": 5}`.
2. Serve Qwen3-32B with vLLM and few-shot prompt it with the schema + ~8-10 example (question → query spec) pairs. Use guided JSON decoding.
3. Parse the LLM's JSON output, execute it against the DataFrame with pandas.
4. Test against ~15 varied questions manually, check the query spec produced makes sense before trusting it.

### Phase 2.5 - Fine-tune a small model for NL → query (runs on the H200)

Goal: train an 8B student for the NL to query step and show it matches or beats its 32B teacher on accuracy, at a fraction of the latency and compute. The 32B model stays as the answer generator.

Hardware: 1x H200 (141 GB). An 8B model with LoRA fits easily in bf16, no quantization needed.

GPU memory rule: run one heavy job at a time. Serve the 32B teacher for data generation, shut it down, then train the 8B student. Do not train while the teacher is loaded.

**Step A: Build the dataset (template-first, so no strong external teacher is needed)**
1. Write `data/gen_specs.py`. Programmatically sample query specs from the schema: pick a metric, filters (position, age, team, minutes), sort, and limit. Specs are correct by construction.
2. Execute every spec against the DataFrame. Drop any spec that errors or returns an empty result. Store the ground-truth result with each one.
3. Write `data/gen_questions.py`. For each spec, render a plain template question ("Who has the most progressive passes among fullbacks under 23?"). Then use the local Qwen3-32B (vLLM, thinking off) to paraphrase each into 3 to 5 natural variants, including casual phrasing and typos.
4. Check each paraphrase for meaning drift: ask the 32B model to re-translate the paraphrase into a spec, and keep it only if the spec matches the original. Drop the rest.
5. Target 3,000 to 5,000 final (question, spec) pairs.
6. Split: 80% train, 10% val, 10% test. Split by underlying spec, not by question, so paraphrases of the same spec never leak across splits. The test set must never be used in training or prompt examples.
7. Save as JSONL: `{"question", "spec", "result"}`.

**Step B: SFT with LoRA**
1. Base model: `Qwen/Qwen3-8B` (fallback: `meta-llama/Llama-3.1-8B-Instruct`).
2. Use `trl` SFTTrainer + `peft`. Suggested config: LoRA r=16, alpha=32, all linear layers, lr 2e-4, 2 to 3 epochs, bf16, max length 1024.
3. Train on prompt = schema + question, completion = spec JSON only.
4. Save the adapter to `models/sft-v1/`. Expect about an hour or less.

**Step C: GRPO with execution reward (stretch goal)**
1. Start from the SFT adapter. Use `trl` GRPOTrainer (verl is fine too).
2. Reward function (in `train/rewards.py`):
   - 0.0 if the output is not valid JSON or fails schema validation
   - 0.2 if valid but execution errors or returns empty
   - 1.0 if execution result matches the stored ground truth (compare with a tolerance for floats and order-insensitive for ties)
3. Sample 8 completions per prompt, small KL penalty, lr around 1e-5. Run on the train split only.
4. Save to `models/grpo-v1/`.
5. If this is unstable after a few hours, drop it. SFT alone is a complete result.

**Step D: Serve and integrate**
1. Merge the LoRA adapter and serve with vLLM: `vllm serve <merged_model_path> --port 8001`.
2. Add a config flag `QUERY_BACKEND=teacher|student` so the NL → query layer can call either the 32B teacher (port 8000) or the fine-tuned 8B (port 8001). Same prompt, same JSON schema, same OpenAI-compatible client.
3. Use constrained or JSON-schema guided decoding in vLLM so outputs always parse.

**Step E: Evaluation (this becomes the writeup table)**
Run all four systems (all local) on the held-out test set:

| System | Valid JSON % | Execution accuracy % | Hallucinated-number rate (end to end) |
|---|---|---|---|
| Qwen3-32B few-shot (teacher) | | | |
| Base 8B few-shot | | | |
| SFT 8B | | | |
| SFT + GRPO 8B | | | |

Also report latency per query and GPU memory used per system. Write results to `eval/results.json` and a short `eval/README.md`.

### Phase 3 - Answer generation + verification
1. Feed the raw query result to the local Qwen3-32B, ask it to produce a natural-language answer.
2. Extract numeric claims from the generated answer (regex for numbers is fine here, doesn't need to be fancy).
3. Diff extracted numbers against the ground-truth result from Phase 2.
4. If mismatch: either auto-correct the response with the true number, or append a flagged correction. Log every case where this catches something - this is your writeup evidence.

### Phase 4 - UI + polish
1. Simple chat interface, reused patterns from prior projects where possible.
2. Pre-load 5-6 example questions so the input isn't a blank box.
3. Optional: render a pass map/heatmap image when the question is spatial (e.g., "show me X's passing zones").
4. Deploy, test end-to-end.

## Definition of done for the weekend
- Working end-to-end: user asks a tactics question in the UI, gets a grounded answer.
- At least one concrete logged example where the verification layer caught a hallucinated number from the raw LLM answer - this is the centerpiece of the LinkedIn/Substack post.
- Deployed and shareable via a link.

## H200 server setup (do this first)

```bash
# 1. Check the GPU and drivers
nvidia-smi

# 2. Project env (Python 3.11 recommended)
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip

# 3. Core deps
pip install statsbombpy pandas pyarrow fastapi uvicorn matplotlib openai
pip install torch transformers datasets peft trl accelerate
pip install vllm

# 4. Cache and model downloads (no API keys needed)
export HF_HOME=/path/with/space/hf_cache   # Qwen3-32B is ~65 GB, Qwen3-8B is ~16 GB
huggingface-cli download Qwen/Qwen3-32B
huggingface-cli download Qwen/Qwen3-8B

# 5. Serve the teacher (used for data gen and baselines)
tmux new -s teacher
vllm serve Qwen/Qwen3-32B --port 8000 --max-model-len 8192 --gpu-memory-utilization 0.85
# detach with Ctrl-b d. Stop it before training the student.

# 6. Run long jobs in tmux so they survive disconnects
tmux new -s train
```

Notes:
- The `openai` package is only used as a client for the local vLLM endpoint. Point it at `http://localhost:8000/v1` with any dummy API key string.
- Install `vllm` in its own venv if it conflicts with the `trl` stack.
- Log training with `wandb` or just TensorBoard. Screenshots of loss and reward curves go in the post.
- Pin versions in `requirements.txt` once things work.

## Suggested repo layout

```
data/        # pull_statsbomb.py, metrics.py, gen_specs.py, gen_questions.py, *.parquet, *.jsonl
query/       # spec schema, validator, executor, teacher + student backends
train/       # sft.py, grpo.py, rewards.py
eval/        # run_eval.py, results.json
api/         # FastAPI app
web/         # Next.js frontend
models/      # adapters and merged models (gitignored)
```

## Revised weekend timeline (with H200)

- **Friday night or Saturday morning**: server setup, Phase 1 data pipeline
- **Saturday afternoon**: Phase 2 (teacher-based query layer, spec schema, executor)
- **Saturday evening**: Step A dataset generation with the teacher, then shut the teacher down and start SFT before bed
- **Sunday morning**: restart the teacher, eval SFT, wire up both vLLM backends, Phase 3 verification layer
- **Sunday afternoon**: UI, deploy, fill in the eval table. Start GRPO only if time remains.
- **Sunday night**: write the post

Cut order if time runs short: GRPO first, then the pass map visual, then extra UI polish. Never cut the verification layer or the eval table.

## Post-weekend stretch goals (not required for v1)
- Multimodal: feed pass-network images into the model alongside text for spatial reasoning questions.
- Small eval set (30-50 Q&A pairs with known answers) to report an accuracy/hallucination-rate number before vs. after the verification layer.
- Expand beyond one competition.

## Notes for whoever is building this (Claude Code)
- Never add a dependency on an external paid API. Everything must run offline on this server once models are downloaded.
- Check `nvidia-smi` before starting any GPU job. Never run the teacher server and a training job at the same time.
- Prioritize correctness of Phase 1 metrics over breadth - a small set of trustworthy numbers beats a large set of shaky ones.
- Keep the query spec schema constrained and validated; don't let the LLM emit arbitrary pandas code (injection risk, and hard to verify).
- Log every verification-layer catch to a file during development - needed for the writeup.
- Favor plain, readable pandas over cleverness; this needs to be debuggable fast within a weekend.