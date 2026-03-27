from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_weight_summary, load_shipments, write_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Python refresher workflow.")
    parser.add_argument("input_csv", type=Path, help="Input shipments CSV")
    parser.add_argument("output_report", type=Path, help="Output report path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = load_shipments(args.input_csv)
    summary = build_weight_summary(rows)
    write_summary(summary, args.output_report)
    print(f"Wrote refresher summary to {args.output_report}.")


if __name__ == "__main__":
    main()
