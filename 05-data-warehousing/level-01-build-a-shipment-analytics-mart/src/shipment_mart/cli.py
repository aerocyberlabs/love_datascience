from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_shipment_analytics_mart


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a shipment analytics mart from cleaned shipment data."
    )
    parser.add_argument("cleaned_csv", type=Path, help="Path to cleaned shipment CSV")
    parser.add_argument("db_path", type=Path, help="SQLite database path for the mart")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = build_shipment_analytics_mart(
        cleaned_path=args.cleaned_csv,
        db_path=args.db_path,
    )
    print(
        f"Loaded {summary.routes_loaded} routes, "
        f"{summary.shipments_loaded} shipments, "
        f"and built {summary.mart_rows} mart rows."
    )


if __name__ == "__main__":
    main()
