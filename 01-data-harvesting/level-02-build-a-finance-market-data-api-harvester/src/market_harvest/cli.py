from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import harvest_market_pages


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Harvest paginated market data fixtures into SQLite."
    )
    parser.add_argument("fixture_dir", type=Path, help="Directory containing page fixtures")
    parser.add_argument("first_page", help="First page filename to load")
    parser.add_argument("db_path", type=Path, help="SQLite database path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = harvest_market_pages(
        fixture_dir=args.fixture_dir,
        first_page=args.first_page,
        db_path=args.db_path,
    )
    print(
        f"Processed {summary.pages_processed} pages, "
        f"saw {summary.records_seen} records, "
        f"loaded {summary.records_loaded} market rows."
    )


if __name__ == "__main__":
    main()
