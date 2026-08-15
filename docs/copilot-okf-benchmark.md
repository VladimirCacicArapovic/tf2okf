# Copilot OKF Benchmark

This guide helps you compare GitHub Copilot answers with and without OKF context.

## Goal

Measure whether `.okf/` improves answer quality, response time, or token usage for the same repository questions.

## Important limitation

GitHub Copilot usually does not expose exact token counts in the IDE UI. Because of that, this benchmark script supports token fields, but you will often leave them empty and compare:

- answer quality
- response time
- number of follow-up questions
- subjective usefulness

If you do have token counts from another integration or log, you can record them too.

## Recommended test method

For each question, run two Copilot chats:

1. without OKF context
2. with OKF context

Keep these the same across both runs:

- same repo state
- same prompt text
- same model/settings if available
- same task

Only change whether Copilot is pointed at `.okf/generated/` and `.okf/knowledge/`.

## Example prompts

- Explain how the application component depends on the network and security layers.
- Which inputs are required to deploy the app component?
- Summarize the shared ECS module and its main AWS resources.
- What would need to change to add HTTPS termination?
- Which generated files should an engineer read first to understand the example stack?

## Recording results

Use `docs/copilot_okf_benchmark.py` to store your observations.

### Add a run without OKF

```bash
python3 docs/copilot_okf_benchmark.py add \
  --scenario architecture \
  --prompt-name app-dependencies \
  --prompt-text "Explain how the application component depends on the network and security layers." \
  --response-quality 3 \
  --response-time-seconds 18 \
  --answer-summary "Mostly correct but had to explore files manually." \
  --notes "No .okf files referenced"
```

### Add a run with OKF

```bash
python3 docs/copilot_okf_benchmark.py add \
  --scenario architecture \
  --prompt-name app-dependencies \
  --prompt-text "Explain how the application component depends on the network and security layers." \
  --used-okf \
  --okf-context ".okf/generated/index.md,.okf/generated/components/app/index.md,.okf/knowledge/architecture.md" \
  --response-quality 5 \
  --response-time-seconds 10 \
  --answer-summary "Clear answer with correct dependency flow and less exploration." \
  --notes "Asked Copilot to read OKF first"
```

### Optional token fields

If you have token counts from another tool, add:

- `--input-tokens 1234`
- `--output-tokens 456`
- `--total-tokens 1690`

## View summary

```bash
python3 docs/copilot_okf_benchmark.py summary
```

## Export CSV

```bash
python3 docs/copilot_okf_benchmark.py export-csv
```

## Suggested scoring rubric

Use a 1-5 quality score:

- `1` = incorrect or unhelpful
- `2` = partly correct, large gaps
- `3` = mostly correct, needed follow-up
- `4` = strong answer, minor gaps
- `5` = accurate, concise, and actionable

## What to look for

OKF is useful even if raw token usage does not go down. Watch for:

- fewer follow-up prompts
- less repo exploration
- clearer architecture explanations
- more accurate dependency summaries
- faster time to useful answer

## Suggested workflow

1. run `tf2okf generate .`
2. prepare 5-10 fixed prompts
3. ask Copilot each prompt without OKF
4. ask Copilot the same prompt with OKF
5. record both runs with the script
6. compare the summary after several trials
