from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_finance_capstone


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the finance risk monitoring capstone."
    )
    parser.add_argument("output_dir", type=Path, help="Directory for capstone outputs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = run_finance_capstone(output_dir=args.output_dir)
    print(
        "Finance capstone complete: "
        f"{summary['wrangling_rows']} cleaned loans, "
        f"{summary['warehouse_mart_rows']} warehouse mart rows, "
        f"model feature={summary['model_feature']}."
    )


if __name__ == "__main__":
    main()
