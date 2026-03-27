from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .pipeline import clean_loans, summarize_by_grade


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean and summarize consumer loan performance data."
    )
    parser.add_argument("input_csv", type=Path, help="Input consumer loans CSV")
    parser.add_argument("output_dir", type=Path, help="Directory for cleaned outputs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cleaned = clean_loans(args.input_csv)
    summary = summarize_by_grade(cleaned)

    _write_csv(args.output_dir / "cleaned_loans.csv", cleaned)
    _write_csv(args.output_dir / "loan_grade_summary.csv", summary)
    print(
        f"Wrote {len(cleaned)} cleaned loans and "
        f"{len(summary)} grade summary rows to {args.output_dir}."
    )


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
