# Hand-written test set (placeholder)

`eval/handwritten_test.jsonl` is deliberately empty. It is for 50 to 100 questions written by hand, never
generated or paraphrased by a model. It is the unbiased benchmark for the eval table: the generated test split
only keeps paraphrases the teacher itself translated correctly, so it flatters the teacher by construction.

One JSON object per line:

```json
{"question": "Which Croatian midfielders completed the most passes under pressure?", "spec": {"metric": "pressured_passes_completed", "filters": {"teams": ["Croatia"], "position_groups": ["DM", "CM", "AM"]}, "limit": 5}, "notes": "optional"}
```

- `spec` follows `query/schema.py`. Omitted fields take their defaults (`per90: false`, `group_by: "player"`,
  `sort: "desc"`, `limit: 5`, all filters null).
- Write the question first and the spec second, the way a careful analyst would read the question.
- Don't copy questions from `eval/dev_hard.jsonl` or the few-shot examples in `query/prompt.py`.

Check the file (it parses, executes, and prints the interpretation echo so you can confirm each spec says what
you meant):

```bash
./.venv/bin/python -m eval.check_handwritten
```
