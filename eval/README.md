# Evaluation: NL to query spec

All systems run locally under vLLM on one H200 (GPU 4), with guided JSON decoding and thinking off. "Exec acc" means
executing the predicted spec returns the same rows as the expected spec (ties order-insensitive, `query/compare.py`).
Regenerate the table with `python -m eval.make_table`; raw numbers are in `results.json`.

| System | Valid JSON % | Exec acc % (generated test) | Exec acc % (dev/hard) | Exec acc % (hand-written) | Hallucinated-number rate | Latency p50 / p95 (s) | Weights in GPU memory (GiB) |
|---|---|---|---|---|---|---|---|
| Qwen3-32B few-shot (teacher) | 100.0 | 99.8 (n=443) | 94.4 (n=18) | pending | not measured | 1.473 / 1.571 | 61.03 |
| Base Qwen3-8B few-shot | 100.0 | 96.8 (n=443) | 94.4 (n=18) | pending | not measured | 0.439 / 0.469 | 15.27 |
| SFT Qwen3-8B (LoRA) | 100.0 | 99.8 (n=443) | 100.0 (n=18) | pending | 0.0% (n=461) | 0.433 / 0.461 | 15.27 |
| SFT + GRPO Qwen3-8B | not run | not run | not run | not run | not run | not run | not run |

Naive vs pipeline, same 290 player questions:

| System | Hallucinated-number rate | Any verified error |
|---|---|---|
| Naive: Qwen3-32B + full stats table in context | 14.1% | 72.8% |
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

`python -m eval.hallucination` (results in `hallucination.json`; per-question records in
`logs/hallucination_records.json`).

- **Naive:** Qwen3-32B with the whole player table in its context (players with 90+ minutes, about 31k tokens of
  CSV) and the pipeline's conventions in its prompt, answering directly.
- **Pipeline:** SFT 8B spec, then executed result, then Qwen3-32B answer from the rows, then the verifier.
- **Scoring:** both are checked against the ground-truth result with the same verifier (`query/verify.py`).
- **Questions:** the generated test split plus dev/hard (never the hand-written set). The comparison uses the 290
  player questions the naive model can fairly answer: no stage or opponent filter, and every ground-truth player
  is in its table. Team questions are excluded because the table omits players under 90 minutes, so a team sum could
  be short through no fault of the model.

| | Hallucinated-number rate | Any verified error (numbers, wrong players/teams, order) |
|---|---|---|
| Naive Qwen3-32B | **14.1%** | 72.8% |
| Pipeline (raw LLM answer, before correction) | **0.0%** | 0.0% |

Over all 461 questions the pipeline's answers had 0 hallucinated numbers (specs correct 99.8%).

The hallucinated-number rate is a **lower bound**. A number only counts as hallucinated if it is not *any* true
stat of the player it is attached to, so wrong numbers that happen to equal another true stat slip through.
Examples from the final run:

- "Mbappé – 8" shot-creating actions (true: 41) passes, because 8 is his goal total. The answer is still caught for
  listing the wrong players.
- Veljković's 7 progressive passes in 221.8 minutes given as "2.89 per 90" (true: 2.84) passes, because another of
  his per-90 stats rounds to 2.89.

Naive catches from the final run (all 211 naive catches are in `logs/verifier_catches.jsonl` with
`source: naive_baseline`):

- **Invented numbers:** "Modrić had 115 pressures, while Schmeichel had **35**". The goalkeeper's true count is 0.
  Similarly, "Costa completed **53** progressive passes"; Diogo Costa's true count is 0.
- **Arithmetic:** "Varane … **99.64%** pass completion (251 out of 280)". The model's own fraction is 89.6%, and
  the true leader is Marquinhos at 96.1%.
- **Wrong rows:** Wales' Joe Allen and Joe Rodon listed among "Canada players with the fewest shots per 90".

**Scorer audit.** Two scorer bugs surfaced during development and were fixed before the reported run:

- **Precision:** true percentages were stored rounded, so a correctly computed "65.38%" was counted wrong. This
  inflated the naive rate to 41.9%.
- **Team questions:** these were counted at first; see the scope note above.

Samples of the remaining catches were checked by hand.

## Training

- **Data:** 3,096 train pairs from 697 specs (3,925 total, split 80/10/10 by spec).
- **Config:** LoRA r=16, alpha=32, all linear layers; lr 2e-4 cosine; 3 epochs; bf16; max length 1,024;
  completion-only loss.
- **Run:** 582 steps, about 25 min on one H200. Final val loss 0.0019. TensorBoard logs are in `models/sft-v1/runs/`.
- **Pilot:** 1,112 pairs, 2 epochs, 6.5 min. Val 98.3, dev/hard 83.3.

GRPO (stretch goal) has not been run. On these sets the SFT student has little headroom left. Decide once the
hand-written set exists.
