from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RESULTS_FILE = Path("docs/copilot_okf_benchmark_results.json")

PROMPTS = [
    {
        "scenario": "architecture",
        "prompt_name": "app-dependencies",
        "without_okf": "Explain how the application component depends on the network and security layers.",
        "with_okf": "Read .okf/generated/index.md, .okf/generated/components/app/index.md, .okf/generated/components/network/index.md, .okf/generated/components/security/index.md, and .okf/knowledge/architecture.md first. Then explain how the application component depends on the network and security layers.",
        "okf_context": ".okf/generated/index.md,.okf/generated/components/app/index.md,.okf/generated/components/network/index.md,.okf/generated/components/security/index.md,.okf/knowledge/architecture.md",
    },
    {
        "scenario": "inputs",
        "prompt_name": "app-inputs",
        "without_okf": "Which inputs are required to deploy the app component, and what do they mean?",
        "with_okf": "Read .okf/generated/components/app/inputs.md first. Then explain which inputs are required to deploy the app component and what each one means.",
        "okf_context": ".okf/generated/components/app/inputs.md",
    },
    {
        "scenario": "module-summary",
        "prompt_name": "ecs-service-summary",
        "without_okf": "Summarize the shared ecs-service module and list the main AWS resources it creates.",
        "with_okf": "Read .okf/generated/shared-modules/ecs-service/index.md and the resource pages under .okf/generated/shared-modules/ecs-service/resources/ first. Then summarize the shared ecs-service module and list the main AWS resources it creates.",
        "okf_context": ".okf/generated/shared-modules/ecs-service/index.md,.okf/generated/shared-modules/ecs-service/resources/",
    },
    {
        "scenario": "design-change",
        "prompt_name": "https-termination",
        "without_okf": "What would need to change in this example to support HTTPS termination at the load balancer?",
        "with_okf": "Read .okf/generated/components/app/index.md, .okf/generated/shared-modules/ecs-service/index.md, .okf/generated/shared-modules/ecs-service/resources/aws_lb_listener.http.md, and .okf/knowledge/architecture.md first. Then explain what would need to change in this example to support HTTPS termination at the load balancer.",
        "okf_context": ".okf/generated/components/app/index.md,.okf/generated/shared-modules/ecs-service/index.md,.okf/generated/shared-modules/ecs-service/resources/aws_lb_listener.http.md,.okf/knowledge/architecture.md",
    },
    {
        "scenario": "onboarding",
        "prompt_name": "new-engineer-read-order",
        "without_okf": "If a new engineer joins the project, how should they read this repository to understand the stack quickly?",
        "with_okf": "Read .okf/index.md, .okf/generated/index.md, .okf/generated/environments.md, and .okf/knowledge/architecture.md first. Then explain how a new engineer should read this repository to understand the stack quickly.",
        "okf_context": ".okf/index.md,.okf/generated/index.md,.okf/generated/environments.md,.okf/knowledge/architecture.md",
    },
]


@dataclass
class ResultEntry:
    timestamp: str
    scenario: str
    prompt_name: str
    used_okf: bool
    prompt_text: str
    okf_context: str
    response_quality: int
    credits_spent: float
    answer_summary: str
    notes: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_results() -> list[dict[str, Any]]:
    if not RESULTS_FILE.exists():
        return []
    return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))


def save_results(results: list[dict[str, Any]]) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_float(prompt: str) -> float:
    while True:
        raw = ask(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Enter a number, for example 12.5")


def ask_quality(prompt: str) -> int:
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Enter a whole number from 1 to 5")
            continue
        if 1 <= value <= 5:
            return value
        print("Enter a whole number from 1 to 5")


def get_credits_spent(result: dict[str, Any]) -> float:
    if "credits_spent" in result:
        return float(result["credits_spent"])
    if "response_time_seconds" in result:
        return float(result["response_time_seconds"])
    return 0.0


def record_run(results: list[dict[str, Any]], prompt: dict[str, str], used_okf: bool) -> None:
    label = "WITH OKF" if used_okf else "WITHOUT OKF"
    prompt_text = prompt["with_okf"] if used_okf else prompt["without_okf"]
    print("\n" + "=" * 80)
    print(f"Prompt: {prompt['prompt_name']} [{label}]")
    print("-" * 80)
    print(prompt_text)
    print("=" * 80)
    print("1. Paste this prompt into Copilot Chat.")
    print("2. Wait for the answer.")
    print("3. Come back here and record the result.\n")

    credits_spent = ask_float("Credits spent: ")
    response_quality = ask_quality("Quality score (1-5): ")
    answer_summary = ask("Short answer summary: ")
    notes = ask("Notes (optional): ")

    entry = ResultEntry(
        timestamp=utc_now(),
        scenario=prompt["scenario"],
        prompt_name=prompt["prompt_name"],
        used_okf=used_okf,
        prompt_text=prompt_text,
        okf_context=prompt["okf_context"] if used_okf else "",
        response_quality=response_quality,
        credits_spent=credits_spent,
        answer_summary=answer_summary,
        notes=notes,
    )
    results.append(asdict(entry))
    save_results(results)
    print("Saved result.\n")


def print_summary(results: list[dict[str, Any]]) -> None:
    print("\nSummary")
    print("-" * 80)
    groups = {"with_okf": [], "without_okf": []}
    for result in results:
        groups["with_okf" if result["used_okf"] else "without_okf"].append(result)

    for label, items in groups.items():
        if not items:
            print(f"{label}: no entries")
            continue
        avg_quality = sum(int(item["response_quality"]) for item in items) / len(items)
        avg_credits_spent = sum(get_credits_spent(item) for item in items) / len(items)
        print(
            f"{label}: count={len(items)} avg_quality={avg_quality:.2f} "
            f"avg_credits_spent={avg_credits_spent:.2f}"
        )

    print("\nPer prompt")
    print("-" * 80)
    for prompt in PROMPTS:
        relevant = [r for r in results if r["prompt_name"] == prompt["prompt_name"]]
        if not relevant:
            continue
        print(f"{prompt['prompt_name']}:")
        for item in relevant:
            kind = "with_okf" if item["used_okf"] else "without_okf"
            print(
                f"  - {kind}: quality={item['response_quality']} "
                f"credits_spent={get_credits_spent(item)} summary={item['answer_summary']}"
            )


def main() -> None:
    print("Copilot OKF benchmark runner")
    print("This script walks you through 5 A/B prompts and records the results.")
    print(f"Results file: {RESULTS_FILE}\n")

    results = load_results()
    reset = ask("Start fresh and overwrite existing results? [y/N]: ").lower()
    if reset == "y":
        results = []
        save_results(results)
        print("Cleared previous results.\n")

    print("Recommended order:")
    print("- Run all prompts WITHOUT OKF first")
    print("- Then run the same prompts WITH OKF")
    print()

    for prompt in PROMPTS:
        record_run(results, prompt, used_okf=False)

    print("Now generate OKF or keep your generated OKF ready before continuing.")
    ask("Press Enter when you are ready to run the WITH OKF prompts... ")

    results = load_results()
    for prompt in PROMPTS:
        record_run(results, prompt, used_okf=True)

    results = load_results()
    print_summary(results)
    print("\nDone. You can inspect the raw results JSON if needed.")


if __name__ == "__main__":
    main()
