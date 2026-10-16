# CLAUDE.md

Grounded football Q&A over StatsBomb FIFA World Cup 2022 event data. A question becomes a constrained QuerySpec
(vLLM guided JSON), pandas executes it, Qwen3-32B writes the answer from the rows, and a verifier checks every
number, name and ranking against the result. The goal is answers that never state a false number. Full plan in
`PROJECT_SPEC.md`, commands in `README.md`, results in `eval/README.md`.

## Rules (all still in force)

- **Fully local.** No external or paid APIs, no API keys, no `anthropic` package. All LLMs are served by vLLM here.
- **GPUs: only 4, 5, 6, 7, and only ONE GPU job at a time.** Other users (e.g. tan.1422) often hold 5 and 6.
  Use `scripts/serve_teacher.sh` / `serve_student.sh`: they refuse GPUs outside 4-7 and any GPU with a process
  you don't own (`SHARE=1` allows sharing with your own server). Set `CUDA_VISIBLE_DEVICES` to one GPU for training.
- **Shut servers down after use** (kill the tmux session). Stop the teacher before any training.
- **Checkpoints and weights go on /home** (NFS, HF cache at `~/.cache/huggingface`). `/local/scratch` is full.
  The existing `models/sft-*` dirs are on scratch and git-ignored.
- **Commit and push after each step.** Author is the user only: no Claude mention, no Co-Authored-By, no
  "Generated with" lines, in commits or PRs. If `git push` hangs on a credential prompt, ask the user to push.
- **No em dashes** in anything written (docs, commits, answers).
- **Never run anything on `eval/handwritten_test.jsonl`** unless the user asks. The user writes it.
- Python is `./.venv/bin/python` (3.11). There is no system `python`.

## Status

- **Phase 1 (data): done.** `data/pull_statsbomb.py`, `data/metrics.py` give `players.parquet` (680 players) and
  `player_match.parquet`. Checks: `cd data && ../.venv/bin/python sanity_check.py`, `pytest tests/`.
- **Phase 2 (NL to spec): done.** `query/schema.py` (QuerySpec), `executor.py`, `describe.py` (interpretation
  echo), `prompt.py` (10 few-shot), `llm.py` (`QUERY_BACKEND=teacher|student`, ports 8000 / 8001).
- **Phase 2.5 (student): done.** Qwen3-8B LoRA (`train/sft.py`, `train/merge.py`), merged at
  `models/sft-v1-merged`. Exec accuracy test / val / dev-hard: teacher 99.8 / 98.7 / 94.4, base 8B 96.8 / 93.0 /
  94.4, SFT 99.8 / 98.2 / 100. SFT is 0.43 s per query vs 1.47 s for the teacher.
- **Phase 3 (answers + verifier): done.** `query/answer.py` (full flow), `query/verify.py` (verifier).
  On the same 290 player questions, naive Qwen3-32B with the stats table in context: 33.1% hallucinated number,
  78.6% any verified error (the first is a subset of the second). Pipeline: 0.0% and 0.3% (1 answer, a
  contaminated label). Error injection, held-out seed 2: 99.9% caught, 0 false positives.
- **Independent test set: done.** `eval/independent_test.jsonl` (297 questions by Mistral Small 24B from specs
  sampled in code, no round-trip filter, 3 writer errors dropped before any run) and
  `eval/independent_misspelled.jsonl` (20, scored separately). Exec accuracy teacher / base 8B / SFT 80.5 / 75.1 /
  80.8; misspelled-name pass 90 / 90 / 90 (ceiling 19 of 20). 41 questions fail on all three systems, most of them
  writer errors (`eval/runs/independent_all_failed.json`), left as labelled.
- **Phase 4: not started.** Waiting on the open items below.

## Key commands and files

- `python -m eval.report`: regenerates every number in `eval/README.md` and `eval/examples.md` from saved outputs
  in `eval/runs/` (CPU, about 12 min; `--skip-rerun` for 5 s). Edit `eval/README.template.md`, never the README;
  the template may hold no literal numbers. Non-recomputable numbers live in `eval/static_numbers.json` (marked †).
- `python -m eval.check_handwritten`: validates the hand-written set (parses, executes, prints the echo).
- `python -m eval.audit_sample --score` scores the marked `eval/audit_sample.md`; `--lookup "name"` prints a
  player's true stats. Generation refuses to overwrite a marked file.
- `GPU=4 scripts/serve_teacher.sh` (Qwen3-32B, port 8000, about 4.5 min to load) and
  `GPU=4 scripts/serve_student.sh models/sft-v1-merged` (port 8001). Phase 3 runs both on one GPU: see README.
- GPU runs that produce saved outputs: `eval.run_eval`, `eval.hallucination` (without `--rescore`), `train/sft.py`.
- `eval/examples.md`: 8 real catches. Catch log: `logs/verifier_catches.jsonl` (local, git-ignored).

## Frozen (do not change without asking)

- **Verifier (`query/verify.py`).** The injection result is a held-out number (seed 2, run once after the fix
  rounds on seeds 0 and 1). Any change needs a fresh unseen seed and a re-run of `eval.report`.
- **Existing eval sets** (`data/{train,val,test}.jsonl`, `eval/dev_hard.jsonl`, `eval/independent_*.jsonl`, the
  naive answers in `eval/runs/hallucination_records.json`). The naive answers were sampled at temperature 0.7 and are under hand
  audit, so regenerating them would change what is being audited. Known label problems are reported, not relabelled.

## Known issues, not fixed

- **Minus signs:** the verifier's number regex drops the sign, so a correct negative xT would be flagged. No
  ground-truth value in the eval sets is negative, so no score changed.
- **First-name matching:** a first name unique in the dataset can match the wrong player ("Joshua" matched Kimmich,
  "Joakim" matched Maehle). The answer is still flagged, but the issue names the wrong player.
- **Surname step picks the wrong player:** "Woo-Young Jun" resolves silently to Son Jun-Ho ("Jun" is a token unique
  to him), which breaks the never-guess rule. "Neymar Jr" does not resolve. Found on the independent set, not fixed.
- Contaminated labels: a few paraphrases say "forward" with label `[ST]` (teacher bias passed the round-trip).

## Decisions and why

- **Age dropped:** StatsBomb open data has no birth dates, so there is no age filter in the spec.
- **Progressive passes are simplified** (no "furthest point in last six passes" lookback) and labelled
  "Progressive passes (simplified)" wherever shown, so nobody mistakes them for FBref's.
- **Interpretation echo:** every result carries a deterministic plain-English reading of the executed spec, and
  answers lead with it, so a misread question is visible instead of silently answered.
- **Template test set favors the teacher:** paraphrases were kept only if the teacher round-tripped them to the
  original spec, so the teacher is right on them by construction. Compare systems on dev-hard and the new sets.
- Position families follow a documented convention ("midfielder" = DM, CM, AM; "forward" = ST, W). Per-90 and rate
  rankings default to at least 270 minutes. Unknown or ambiguous names get "Did you mean ...?", never a guess.

## Open items (in order)

1. **40-answer hand audit** by the user in `eval/audit_sample.md` (20 flagged, 20 passed; the old 100-item file is
   `eval/audit_sample_100.md`, not scored). Then `python -m eval.report` picks up `eval/audit_results.json`.
2. **10 stress questions the user writes**, plus the hand-written set (`eval/HANDWRITTEN.md`). Do not draft them.
3. **Phase 4:** a small demo (chat UI with preloaded example questions, interpretation echo and verifier flags).
4. **GRPO only if a test set shows a gap** between the SFT student and the teacher. The independent set shows none.
