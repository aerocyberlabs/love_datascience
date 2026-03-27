from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .pipeline import clean_shipments, summarize_routes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean shipment data and create a route-level summary."
    )
    parser.add_argument("raw_path", type=Path, help="Path to the raw shipment CSV")
    parser.add_argument("output_dir", type=Path, help="Directory for cleaned outputs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cleaned_rows = clean_shipments(args.raw_path)
    route_summary = summarize_routes(cleaned_rows)

    _write_csv(args.output_dir / "cleaned_shipments.csv", cleaned_rows)
    _write_csv(args.output_dir / "route_summary.csv", route_summary)

    print(
        f"Wrote {len(cleaned_rows)} cleaned rows and "
        f"{len(route_summary)} route summaries to {args.output_dir}."
    )


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
