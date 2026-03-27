from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import ingest_shipments


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest shipment CSV files into a local SQLite database."
    )
    parser.add_argument("raw_dir", type=Path, help="Directory containing shipment CSV files")
    parser.add_argument("db_path", type=Path, help="SQLite database path to create or update")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = ingest_shipments(raw_dir=args.raw_dir, db_path=args.db_path)
    print(
        f"Processed {summary.files_processed} files, "
        f"saw {summary.rows_seen} rows, "
        f"upserted {summary.rows_upserted} shipments."
    )


if __name__ == "__main__":
    main()
