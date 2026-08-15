# Run the Copilot OKF benchmark

Use this script to compare GitHub Copilot answers with and without OKF context for the same repository questions.

## Run it

From the repository root:

```bash
python3 docs/run_copilot_okf_benchmark.py
```

## What it does

The script walks you through 5 benchmark prompts in two phases:

1. without OKF
2. with OKF

For each run, it asks you to record:

- response time in seconds
- quality score from 1 to 5
- short answer summary
- optional notes

It stores results in:

```bash
docs/copilot_okf_benchmark_results.json
```

## Suggested workflow

1. open Copilot Chat in your IDE
2. run the script
3. for each prompt, copy the displayed text into Copilot
4. wait for the answer
5. come back to the terminal and record the result
6. after the first 5 prompts, continue with the OKF-assisted versions
7. review the printed summary

## Before the WITH OKF phase

Make sure OKF exists for the repo you are testing. For example:

```bash
.venv/bin/tf2okf generate examples/tfscaffold
```

## Quality rubric

- `1` = incorrect or not useful
- `2` = partly correct, large gaps
- `3` = mostly correct, but needs follow-up
- `4` = strong answer with small gaps
- `5` = clear, accurate, and actionable

## Notes

GitHub Copilot usually does not expose exact token counts in the IDE, so this benchmark focuses on answer quality and response time.
