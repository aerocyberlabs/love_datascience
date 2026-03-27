from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_finance_risk_warehouse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a finance risk warehouse from cleaned loan data."
    )
    parser.add_argument("cleaned_csv", type=Path, help="Path to cleaned loans CSV")
    parser.add_argument("db_path", type=Path, help="SQLite database path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = build_finance_risk_warehouse(
        cleaned_path=args.cleaned_csv,
        db_path=args.db_path,
    )
    print(
        f"Loaded {summary.grades_loaded} grades, "
        f"{summary.loans_loaded} loans, "
        f"and built {summary.mart_rows} mart rows."
    )


if __name__ == "__main__":
    main()
