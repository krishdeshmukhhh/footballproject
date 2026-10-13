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
