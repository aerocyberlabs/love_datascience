from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_logistics_capstone


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the end-to-end logistics intelligence capstone."
    )
    parser.add_argument("output_dir", type=Path, help="Directory for capstone outputs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = run_logistics_capstone(output_dir=args.output_dir)
    print(
        "Capstone complete: "
        f"{summary['wrangling_rows']} cleaned rows, "
        f"{summary['mart_rows']} mart rows, "
        f"model feature={summary['model_feature']}."
    )


if __name__ == "__main__":
    main()
