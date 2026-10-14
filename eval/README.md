# Evaluation: NL to query spec

All systems run locally under vLLM on one H200 (GPU 4), with guided JSON decoding and thinking off. "Exec acc" means
executing the predicted spec returns the same rows as the expected spec (ties order-insensitive, `query/compare.py`).
Regenerate the table with `python -m eval.make_table`; raw numbers are in `results.json`.

| System | Valid JSON % | Exec acc % (generated test) | Exec acc % (dev/hard) | Exec acc % (hand-written) | Hallucinated-number rate | Latency p50 / p95 (s) | Weights in GPU memory (GiB) |
|---|---|---|---|---|---|---|---|
| Qwen3-32B few-shot (teacher) | 100.0 | 99.8 (n=443) | 94.4 (n=18) | pending | not measured | 1.473 / 1.571 | 61.03 |
| Base Qwen3-8B few-shot | 100.0 | 96.8 (n=443) | 94.4 (n=18) | pending | not measured | 0.439 / 0.469 | 15.27 |
| SFT Qwen3-8B (LoRA) | 100.0 | 99.8 (n=443) | 100.0 (n=18) | pending | 0.0% (n=460) | 0.433 / 0.461 | 15.27 |
| SFT + GRPO Qwen3-8B | not run | not run | not run | not run | not run | not run | not run |

Naive vs pipeline, same 290 player questions:

| System | Hallucinated-number rate | Any verified error |
|---|---|---|
| Naive: Qwen3-32B + full stats table in context | 33.1% | 78.6% |
| Pipeline: SFT 8B query + Qwen3-32B answer, raw | 0.0% | 0.0% |

Validation split (n=386): teacher 98.7, base 8B 93.0, SFT 98.2. Throughput at 48 concurrent requests: teacher
~21 q/s, both 8B models ~40 q/s. Latency is single sequential requests.

## How to read this

- **The generated test split flatters the teacher.** A paraphrase was kept only if the teacher translated it back
  to the original spec, so on paraphrases the teacher is right by construction. Only template questions can catch
  it out. The SFT student matching it there (99.8 vs 99.8) is the meaningful part.
- **Dev/hard is small (n=18), and it is not untouched.** The pilot's dev/hard misses (limit=1 on plural questions
  with no number) led to a template fix before the full run. Treat it as a dev set. The hand-written set is the real
  test.
- **The base 8B is a strong baseline.** Its spec accuracy is lower than its execution accuracy (test 94.8 vs 96.8,
  dev/hard 83.3 vs 94.4): many of its specs differ from the expected one but return the same rows.

## What fine-tuning fixed

The teacher's systematic error is reading a position family as a single group. 27 of its 36 misses on
correct-by-construction template questions were this ("Which midfielder ..." to `[CM]`, "Which forward ..." to
`[ST]`). The same error drops Brozović from "Which Croatian midfielders completed the most passes under pressure?".
The SFT student, trained on templates that use the documented convention, gets these right, including the
Brozović question.

## Known issues

- **Teacher bias leaks into a few labels.** 4 of 3,925 pairs (3 train, 1 test) have a paraphrase that turned
  "striker" into "forward" while keeping the label `[ST]`, because the teacher's round-trip accepted it. The student's
  single test miss is one of these: it answered `[ST, W]`, which is the documented convention. Left as measured, not
  relabelled after the fact.
- **Name copying.** The student sometimes "corrects" a misspelled or accented name instead of copying it
  ("Theo Hernédez", "Firas Albirkan"). Resolution then fails and the question errors out instead of answering.
- **Ambiguous paraphrases** account for most of the rest (passes "managed" under pressure: attempted or completed?).

## Hallucinated numbers: naive LLM vs the pipeline (Phase 3)

Run with `python -m eval.hallucination`. Results are in `hallucination.json`, per-question records in
`logs/hallucination_records.json`. `--rescore` re-scores the saved answers with the current verifier.

- **Naive:** Qwen3-32B with the whole player table in its context (players with 90+ minutes, about 31k tokens of
  CSV) and the pipeline's conventions in its prompt, answering directly.
- **Pipeline:** SFT 8B spec, then executed result, then Qwen3-32B answer from the rows, then the verifier.
- **Scoring:** both are checked against the ground-truth result with the same frozen verifier (`query/verify.py`).
- **Questions:** the generated test split plus dev/hard (never the hand-written set). The comparison uses the
  290 player questions the naive model can fairly answer: no stage or opponent filter, and every
  ground-truth player is in its table. Team questions are excluded because the table omits players under 90 minutes.

| | Hallucinated-number rate | Any verified error (numbers, wrong players/teams, order) |
|---|---|---|
| Naive Qwen3-32B | **33.1%** | 78.6% |
| Pipeline (raw LLM answer, before correction) | **0.0%** | 0.0% |

Over all 461 questions the pipeline answered 460 with 0
hallucinated numbers (specs correct 99.8%). The other one is a
"Did you mean Hakim Ziyech (Morocco)?" for "ziyechs".

**How much to trust the naive number:**

- **Precision (hand audit):** of 15 randomly sampled flagged naive numbers, 13 are clear hallucinations, 1 was
  truncation ("271 minutes" for 271.7; now accepted), and 1 is unclear (correct arithmetic, "135/153 = 88.23%",
  for an unidentified player).
- **A lower bound in another sense:** a number only counts as hallucinated if it is not *any* true stat of the
  player it is attached to, so a wrong number that equals another of his true stats slips through.
- **Unknown names:** names outside the dataset (e.g. "Péter Gulácsi (Hungary)", who was not at the tournament) are
  invisible to the name check. Their invented numbers are still flagged.
- **Sensitivity:** naive answers are sampled at temperature 0.7, and the rate moved between development runs as the
  verifier was fixed (see the audit trail below). Treat it as "roughly a third of naive answers contain a false
  number, and about four in five contain some verified error", not as a precise figure.

Naive catches from the final run (in `logs/verifier_catches.jsonl` with `source: naive_baseline`):

- **Wrong numbers:** "Robert Lewandowski … 92.4% pass completion" (true 71.4%).
- **Inconsistent fractions:** "Rodri … 98.3% (644/655)" (true 644/679 = 94.8%); "Varane … 99.64% (251/252)"
  (true 251/280).
- **Arithmetic:** "Pulisic, 44 pressures in 315 minutes = 12.98 per 90" (correct: 12.57).
- **Invented players:** "Péter Gulácsi (Hungary)" listed as a top central midfielder; Hungary did not qualify.

## Verifier error-injection test

Run with `python -m eval.verifier_injection --seed N`. Results are in `verifier_injection*.json`.

- **Base answers:** the pipeline's 459 answers that are correct and verify clean against ground
  truth.
- **Method:** one programmatic error of each applicable type is injected into each answer, and the runtime verifier
  (no extra truth) is run on the result.
- **Logging:** every catch is logged with `source: error_injection`.

Seed 0 (and seed 1) were used while fixing the verifier, so the held-out figures below are **seed 2**, run once on
the final answers with the verifier frozen.

| Injected error | n | Caught % | Right issue kind % | Restored exactly by auto-correction % |
|---|---|---|---|---|
| number_perturb | 400 | 100.0 | 100.0 | 97.8 |
| value_swap | 236 | 100.0 | 100.0 | 97.5 |
| name_swap | 400 | 100.0 | 100.0 | n/a |
| team_swap | 373 | 100.0 | 100.0 | n/a |
| order_swap | 227 | 100.0 | 100.0 | n/a |
| fabricated_stat | 400 | 99.5 | 99.5 | n/a |
| **Overall** | 2036 | **99.9** | 99.9 | |

- **False positives:** 0 of the 459 clean answers were flagged.
  Seed 0 gives 100.0% caught and 0 false positives.
- **The 2 held-out misses** are fabricated stats whose number also appears in the question ("Gakpo also recorded
  16 key passes" on a Round-of-16 question). Numbers quoted from the question are allowed by design.
- **When the correction fails to restore the original text,** the number is still flagged; it just is not
  rewritten. This happens when the verifier cannot safely tell which player the number belongs to.

**Audit trail.** The injection test found real verifier bugs, all fixed before the held-out run:

- Decimal claims matched integer truths ("1.5" counted as rank 2).
- Sums and differences of row values were accepted anywhere ("Netherlands – 8" when 8 = 5 + 3).
- "followed by" counted as comparison wording.
- "World Cup" blocked attributing a number to the player before it.

The naive-baseline scorer had two more bugs:

- **Rounding:** rounded stored truths made correct "65.38%" claims count as wrong, which inflated an early run to
  41.9%.
- **Team questions:** these were included at first.

## Training

- **Data:** 3,096 train pairs from 697 specs (3,925 total, split 80/10/10 by spec).
- **Config:** LoRA r=16, alpha=32, all linear layers; lr 2e-4 cosine; 3 epochs; bf16; max length 1,024;
  completion-only loss.
- **Run:** 582 steps, about 25 min on one H200. Final val loss 0.0019. TensorBoard logs are in `models/sft-v1/runs/`.
- **Pilot:** 1,112 pairs, 2 epochs, 6.5 min. Val 98.3, dev/hard 83.3.

GRPO (stretch goal) has not been run. On these sets the SFT student has little headroom left. Decide once the
hand-written set exists.
