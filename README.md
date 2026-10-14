# footballproject

Football tactics Q&A over StatsBomb event data: natural language goes to a structured query, which runs against
ground-truth tables, and every number in the answer is verified against them. Fully local (vLLM, no API keys).
See `PROJECT_SPEC.md`.

## Setup (H200 server)

```bash
# Python 3.11 env at ./.venv (conda-created, since the system Python is 3.10)
conda create -y -p ./.venv python=3.11 pip
./.venv/bin/pip install uv
./.venv/bin/uv pip install --python ./.venv/bin/python -r requirements.txt

# Weights go to the default HF cache (~/.cache/huggingface, on /home NFS, since /local/scratch is nearly full)
./.venv/bin/hf download Qwen/Qwen3-8B
./.venv/bin/hf download Qwen/Qwen3-32B

# Serve the teacher on ONE GPU from 4-7 (the script refuses others and busy GPUs). Weights take ~4.5 min to load from NFS.
tmux new -s teacher 'GPU=4 scripts/serve_teacher.sh'
./.venv/bin/python scripts/smoke_teacher.py   # one guided-JSON request, thinking off
```

Everything (vLLM, torch, transformers, trl, peft) lives in one env with no conflicts; versions are pinned in
`requirements.txt`.

## Phase 1: data pipeline

Competition: **FIFA World Cup 2022** (StatsBomb `competition_id=43`, `season_id=106`), 64 matches, 234k events.

```bash
./.venv/bin/python data/pull_statsbomb.py   # -> data/raw/{matches,events,spells}.parquet  (~20 s)
./.venv/bin/python data/metrics.py          # -> data/players.parquet, data/player_match.parquet, data/xt_grid.npy
cd data && ../.venv/bin/python sanity_check.py   # known facts + invariants; exits 1 on any failure
./.venv/bin/python -m pytest tests/         # boundary tests for each metric definition
```

### Tables

- `players.parquet`: one row per player (680), with tournament totals, a `_p90` column for every metric,
  `minutes`, `matches`, `team`, `primary_position` and `position_group` (GK, CB, FB, DM, CM, AM, W, ST).
- `player_match.parquet`: the same metrics per (match, player), plus `opponent`, `stage`, `match_date`, `sent_off`.

### Metric definitions

StatsBomb pitch is 120 x 80 yards, and every team attacks toward x = 120. Penalty-shootout events are dropped.

| Metric | Definition |
|---|---|
| `minutes` | From the event stream (Starting XI, Substitution, red card / second yellow). Stoppage time is clamped into its period, so a full match is 90 (120 with extra time). Time off the pitch for treatment counts as played. |
| `progressive_passes` (labelled **"Progressive passes (simplified)"** everywhere it is shown) | Completed open-play pass starting at x >= 48 (outside own 40%) that moves the ball >= 10 yards forward, or enters the penalty area from outside it. A simplified FBref definition (no "furthest point in last six passes" lookback). |
| `progressive_carries` | Carry ending at x >= 60 that moves >= 10 yards forward, or enters the penalty area from outside it. |
| `pressures` | StatsBomb Pressure events. |
| `pressured_passes_completed` / `_attempted` | Passes with `under_pressure = True`; also `pressured_pass_completion_pct`. |
| `shot_creating_actions` | For each shot, the last two offensive actions by the shooting team in the same possession: completed passes, completed dribbles, shots (rebounds), fouls won. |
| `xt_added` | Sum of xT(end) - xT(start) over completed open-play passes and carries. Zone xT (Singh 2018, 16 x 12 grid) fitted on this tournament; a zone's scoring probability is its mean StatsBomb xG, to cut small-sample noise. |
| `goals`, `non_penalty_goals`, `assists`, `shots`, `xg`, `npxg`, `key_passes`, `passes_*` | Straight from StatsBomb's flags. |

### Data-quality notes

- **Lineup position spells are unreliable for timing.** In several matches they run backwards in time
  (`120:05` p4 to `81:37` p2) or give subbed-off players a phantom spell to the final whistle, and they don't
  end at red cards. Minutes therefore come from events. A match's position is the mode of the `position`
  field on the player's own events.
- StatsBomb open data has no birth dates, so **age is deliberately out of scope** (no age filter in the query spec).
- Two harmless orphans: an unused sub booked on the bench (events but no minutes) and a 94:52 sub with no events.

## Phase 2: NL to structured query

```bash
tmux new -s teacher 'GPU=4 scripts/serve_teacher.sh'      # Qwen3-32B on port 8000
./.venv/bin/python -m query.manual_test                     # 18 hand-checked questions -> logs/phase2_manual.json
```

- `query/schema.py`: the `QuerySpec` pydantic model. Its JSON schema drives vLLM guided decoding, and the same
  model validates and canonicalises the output. Fields: `metric` (19, enum), `per90`, `group_by` (player | team),
  `filters` (players, teams, position_groups, stages, opponents, min_minutes), `sort`, `limit` (1-20).
  The LLM never writes pandas.
- `query/executor.py`: plain pandas over `player_match.parquet`, so stage and opponent filters re-aggregate just
  those matches. Rules worth knowing:
  - Per-90 rankings, rate metrics and "fewest" sorts default to at least 270 minutes (90 under a stage or opponent
    filter), unless the question names players or sets its own threshold.
  - Descending count rankings drop zero values.
  - Ties share a rank.
  - Player names resolve accent-insensitively against display names. Ambiguous names ("Hernández", "de Jong")
    raise an error rather than guess.
- `query/prompt.py`: system prompt plus 10 hand-written few-shot examples (keep them out of any test split).
- `query/llm.py`: `translate(question)`. `QUERY_BACKEND=teacher|student` switches between port 8000 and 8001.

Teacher on the manual set: 18/18 valid, 17/18 correct specs, ~1.5 s each. Known miss: "Croatian midfielders"
becomes `[CM]` and silently drops Brozović (DM). Similar phrasings that were not tuned on work.

Every executed spec also returns an **interpretation echo** (`query/describe.py`): a deterministic plain-English
reading of what was actually run, e.g. "The 5 players with the most passes completed under pressure, among
central midfielders (CM), playing for Croatia, World Cup 2022." Answers will show it, so a misread question is
visible.

## Phase 2.5: fine-tuned 8B student for NL to query

```bash
python data/gen_specs.py --n 2000                 # sample + execute specs; split = hash(spec) 80/10/10
GPU=4 scripts/serve_teacher.sh                    # in tmux
python data/gen_questions.py --specs 880          # template + 4 paraphrases per spec, drift filter (48 parallel)
python data/build_dataset.py                      # -> data/{train,val,test}.jsonl
# stop the teacher, then (one GPU):
CUDA_VISIBLE_DEVICES=4 python train/sft.py --out models/sft-v1 --epochs 3
python train/merge.py models/sft-v1 models/sft-v1-merged
GPU=4 scripts/serve_student.sh models/sft-v1-merged   # in tmux
python -m eval.run_eval --system sft --data data/test.jsonl data/val.jsonl eval/dev_hard.jsonl \
    --serve-log logs/student.log
python -m eval.make_table
```

- **Held out from all generated data:** the 18 dev/hard questions (`eval/dev_hard.jsonl`) and the 10 few-shot
  examples. Their specs are excluded at sampling time.
- **Split by spec:** a spec's split is a hash of its canonical form, so paraphrases never straddle splits, and the
  pilot was a strict subset of the full set with the same splits.
- **Hand-written test set:** `eval/handwritten_test.jsonl` is an empty placeholder for 50-100 questions written by
  hand (see `eval/HANDWRITTEN.md`). It is the unbiased teacher-vs-student benchmark.
- **Known bias:** the drift filter keeps only paraphrases the teacher round-trips correctly, so the teacher's
  accuracy on the generated splits is inflated by construction. Compare systems on dev/hard and hand-written.

Results are in `eval/README.md`.

## Phase 3: answers, verification, and the naive baseline

```bash
# Teacher (answers) and student (specs) share ONE GPU. Start the teacher first and wait until it is up.
GPU=4 GPU_MEM=0.60 MAX_LEN=32768 scripts/serve_teacher.sh            # tmux; 32k context for the naive baseline
SHARE=1 GPU=4 GPU_MEM=0.25 scripts/serve_student.sh models/sft-v1-merged
python -m query.answer "Which Croatian midfielders completed the most passes under pressure?"
python -m eval.hallucination            # naive vs pipeline, hallucinated-number rate
python -m eval.verifier_injection --seed 2   # error-injection catch rate (no GPU needed)

# No GPU: regenerate every number in eval/README.md (and eval/examples.md) from the saved outputs in eval/runs/
python -m eval.report
python -m eval.audit_sample --score     # after marking eval/audit_sample.md by hand
```

- `query/answer.py` runs the whole flow:
  1. Question to spec (`QUERY_BACKEND=student|teacher`).
  2. Execute the spec. An unknown or ambiguous name returns "Did you mean X (Team)?" and never guesses.
  3. Qwen3-32B writes the answer from the rows.
  4. `query/verify.py` checks it, corrects what it can, and flags the rest.

  The response leads with the interpretation echo. Every catch goes to `logs/verifier_catches.jsonl`.
- `query/verify.py` checks every number against the result (tied to the nearest player or team mention, so a
  correct value on the wrong player is caught), every player or team named, and ranking order and ordinals. It
  rewrites only numbers it can safely attribute to a known row; everything else is flagged with the verified rows.

Results (details in `eval/README.md`):

- **Hallucinated numbers:** the naive Qwen3-32B with the stats table in context put one in about a third of answers,
  and about four in five had some verified error (mostly naming the wrong players). The pipeline put no false number
  in any of its 460 answers.
- **Real catches:** `eval/examples.md`. **Blind hand audit** of 100 naive answers: `eval/audit_sample.md`.
- **Verifier on held-out injected errors:** it caught 99.9% with 0 false positives.
