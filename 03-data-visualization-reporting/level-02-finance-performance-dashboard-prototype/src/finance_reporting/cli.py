from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_finance_kpis, load_grade_summary, render_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a finance performance dashboard report."
    )
    parser.add_argument("input_csv", type=Path, help="Input loan grade summary CSV")
    parser.add_argument("output_dir", type=Path, help="Directory for report output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_grade_summary(args.input_csv)
    kpis = build_finance_kpis(rows)
    report = render_markdown_report(kpis, rows)

    report_path = args.output_dir / "finance_dashboard_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Wrote report to {report_path}.")


if __name__ == "__main__":
    main()
