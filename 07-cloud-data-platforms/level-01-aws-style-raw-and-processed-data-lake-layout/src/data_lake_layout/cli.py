from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_data_lake_layout


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a local AWS-style raw and processed lake layout."
    )
    parser.add_argument("source_dir", type=Path, help="Directory with source files")
    parser.add_argument("target_dir", type=Path, help="Target lake directory")
    parser.add_argument("dataset_name", help="Dataset name for the lake path")
    parser.add_argument("ingest_date", help="Partition date in YYYY-MM-DD format")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = build_data_lake_layout(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        dataset_name=args.dataset_name,
        ingest_date=args.ingest_date,
    )
    print(
        f"Registered {summary['files_registered']} files and wrote manifest to "
        f"{summary['manifest_path']}."
    )


if __name__ == "__main__":
    main()
