from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_finance_batch_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a local finance batch pipeline layout and manifest."
    )
    parser.add_argument("source_dir", type=Path, help="Directory with source batch files")
    parser.add_argument("pipeline_dir", type=Path, help="Target pipeline directory")
    parser.add_argument("dataset_name", help="Dataset name")
    parser.add_argument("run_date", help="Run date in YYYY-MM-DD format")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = build_finance_batch_pipeline(
        source_dir=args.source_dir,
        pipeline_dir=args.pipeline_dir,
        dataset_name=args.dataset_name,
        run_date=args.run_date,
    )
    print(
        f"Registered {summary['files_registered']} files for "
        f"{summary['job_name']} and wrote manifest to {summary['manifest_path']}."
    )


if __name__ == "__main__":
    main()
