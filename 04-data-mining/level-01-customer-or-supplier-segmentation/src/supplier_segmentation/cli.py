from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .pipeline import assign_segments, load_supplier_metrics, summarize_segments


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the supplier segmentation mining project."
    )
    parser.add_argument("input_csv", type=Path, help="Input supplier metrics CSV")
    parser.add_argument("output_dir", type=Path, help="Directory for output CSV files")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_supplier_metrics(args.input_csv)
    segmented = assign_segments(rows)
    summary = summarize_segments(segmented)

    _write_csv(args.output_dir / "segmented_suppliers.csv", segmented)
    _write_csv(args.output_dir / "segment_summary.csv", summary)
    print(
        f"Wrote {len(segmented)} segmented suppliers and "
        f"{len(summary)} segment summary rows to {args.output_dir}."
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
