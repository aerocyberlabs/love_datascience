from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_kpi_snapshot, load_route_summary, render_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a logistics KPI markdown report from route summary data."
    )
    parser.add_argument("route_summary_csv", type=Path, help="Path to route summary CSV")
    parser.add_argument("output_dir", type=Path, help="Directory to write the report into")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_route_summary(args.route_summary_csv)
    snapshot = build_kpi_snapshot(rows)
    report = render_markdown_report(snapshot, rows)

    report_path = args.output_dir / "logistics_kpi_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Wrote report to {report_path}.")


if __name__ == "__main__":
    main()
