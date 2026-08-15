from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class BenchmarkEntry:
    timestamp: str
    scenario: str
    prompt_name: str
    prompt_text: str
    used_okf: bool
    okf_context: str
    response_quality: int
    response_time_seconds: float
    answer_summary: str
    notes: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_entries(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def append_entry(args: argparse.Namespace) -> None:
    path = Path(args.file)
    entries = load_entries(path)
    entry = BenchmarkEntry(
        timestamp=utc_now(),
        scenario=args.scenario,
        prompt_name=args.prompt_name,
        prompt_text=args.prompt_text,
        used_okf=args.used_okf,
        okf_context=args.okf_context,
        response_quality=args.response_quality,
        response_time_seconds=args.response_time_seconds,
        answer_summary=args.answer_summary,
        notes=args.notes,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        total_tokens=args.total_tokens,
    )
    entries.append(asdict(entry))
    save_entries(path, entries)
    print(f"Saved benchmark entry to {path}")


def print_summary(args: argparse.Namespace) -> None:
    path = Path(args.file)
    entries = load_entries(path)
    if not entries:
        print("No benchmark entries found.")
        return

    grouped: dict[str, list[dict[str, Any]]] = {"with_okf": [], "without_okf": []}
    for entry in entries:
        grouped["with_okf" if entry.get("used_okf") else "without_okf"].append(entry)

    for label, items in grouped.items():
        if not items:
            print(f"{label}: no entries")
            continue
        avg_quality = sum(int(x["response_quality"]) for x in items) / len(items)
        avg_time = sum(float(x["response_time_seconds"]) for x in items) / len(items)
        token_values = [x.get("total_tokens") for x in items if x.get("total_tokens") is not None]
        avg_tokens = (sum(int(x) for x in token_values) / len(token_values)) if token_values else None
        print(f"{label}: count={len(items)} avg_quality={avg_quality:.2f} avg_time={avg_time:.2f}s avg_total_tokens={avg_tokens if avg_tokens is not None else 'n/a'}")


def export_csv(args: argparse.Namespace) -> None:
    src = Path(args.file)
    dst = Path(args.csv_file)
    entries = load_entries(src)
    if not entries:
        print("No benchmark entries found.")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(entries[0].keys())
    with dst.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    print(f"Exported CSV to {dst}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track manual GitHub Copilot OKF vs non-OKF benchmark runs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Record one benchmark result")
    add_parser.add_argument("--file", default="docs/copilot_okf_benchmark.json", help="JSON file that stores results")
    add_parser.add_argument("--scenario", required=True, help="Short scenario label, for example 'architecture-question'")
    add_parser.add_argument("--prompt-name", required=True, help="Short prompt identifier")
    add_parser.add_argument("--prompt-text", required=True, help="Exact prompt used with Copilot")
    add_parser.add_argument("--used-okf", action="store_true", help="Mark this run as using OKF context")
    add_parser.add_argument("--okf-context", default="", help="Comma-separated OKF files or summary of context used")
    add_parser.add_argument("--response-quality", type=int, required=True, help="Manual quality score from 1 to 5")
    add_parser.add_argument("--response-time-seconds", type=float, required=True, help="Elapsed response time in seconds")
    add_parser.add_argument("--answer-summary", required=True, help="Short summary of the answer quality")
    add_parser.add_argument("--notes", default="", help="Any extra notes")
    add_parser.add_argument("--input-tokens", type=int, default=None, help="Optional token count if available")
    add_parser.add_argument("--output-tokens", type=int, default=None, help="Optional token count if available")
    add_parser.add_argument("--total-tokens", type=int, default=None, help="Optional total token count if available")
    add_parser.set_defaults(func=append_entry)

    summary_parser = subparsers.add_parser("summary", help="Print aggregate summary")
    summary_parser.add_argument("--file", default="docs/copilot_okf_benchmark.json", help="JSON file that stores results")
    summary_parser.set_defaults(func=print_summary)

    csv_parser = subparsers.add_parser("export-csv", help="Export results as CSV")
    csv_parser.add_argument("--file", default="docs/copilot_okf_benchmark.json", help="JSON file that stores results")
    csv_parser.add_argument("--csv-file", default="docs/copilot_okf_benchmark.csv", help="CSV destination path")
    csv_parser.set_defaults(func=export_csv)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
