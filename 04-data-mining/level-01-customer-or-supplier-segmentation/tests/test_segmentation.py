from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.supplier_segmentation.pipeline import (  # noqa: E402
    assign_segments,
    load_supplier_metrics,
    summarize_segments,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class SupplierSegmentationTests(unittest.TestCase):
    def test_load_supplier_metrics_parses_numeric_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "suppliers.csv"
            write_csv(
                csv_path,
                [
                    {
                        "supplier_id": "SUP-100",
                        "on_time_rate": "0.95",
                        "monthly_shipments": "120",
                        "avg_delay_days": "0.5",
                    }
                ],
            )

            rows = load_supplier_metrics(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "supplier_id": "SUP-100",
                        "on_time_rate": 0.95,
                        "monthly_shipments": 120,
                        "avg_delay_days": 0.5,
                    }
                ],
            )

    def test_assign_segments_labels_suppliers_by_risk_and_volume(self) -> None:
        rows = [
            {
                "supplier_id": "SUP-100",
                "on_time_rate": 0.95,
                "monthly_shipments": 120,
                "avg_delay_days": 0.5,
            },
            {
                "supplier_id": "SUP-200",
                "on_time_rate": 0.72,
                "monthly_shipments": 110,
                "avg_delay_days": 2.8,
            },
            {
                "supplier_id": "SUP-300",
                "on_time_rate": 0.88,
                "monthly_shipments": 40,
                "avg_delay_days": 1.0,
            },
        ]

        segmented = assign_segments(rows)

        self.assertEqual(
            segmented,
            [
                {
                    "supplier_id": "SUP-100",
                    "on_time_rate": 0.95,
                    "monthly_shipments": 120,
                    "avg_delay_days": 0.5,
                    "segment": "high_volume_reliable",
                },
                {
                    "supplier_id": "SUP-200",
                    "on_time_rate": 0.72,
                    "monthly_shipments": 110,
                    "avg_delay_days": 2.8,
                    "segment": "high_volume_risky",
                },
                {
                    "supplier_id": "SUP-300",
                    "on_time_rate": 0.88,
                    "monthly_shipments": 40,
                    "avg_delay_days": 1.0,
                    "segment": "low_volume_stable",
                },
            ],
        )

    def test_summarize_segments_counts_each_segment(self) -> None:
        rows = [
            {
                "supplier_id": "SUP-100",
                "on_time_rate": 0.95,
                "monthly_shipments": 120,
                "avg_delay_days": 0.5,
                "segment": "high_volume_reliable",
            },
            {
                "supplier_id": "SUP-200",
                "on_time_rate": 0.72,
                "monthly_shipments": 110,
                "avg_delay_days": 2.8,
                "segment": "high_volume_risky",
            },
            {
                "supplier_id": "SUP-300",
                "on_time_rate": 0.88,
                "monthly_shipments": 40,
                "avg_delay_days": 1.0,
                "segment": "low_volume_stable",
            },
            {
                "supplier_id": "SUP-301",
                "on_time_rate": 0.9,
                "monthly_shipments": 45,
                "avg_delay_days": 0.9,
                "segment": "low_volume_stable",
            },
        ]

        summary = summarize_segments(rows)

        self.assertEqual(
            summary,
            [
                {"segment": "high_volume_reliable", "supplier_count": 1},
                {"segment": "high_volume_risky", "supplier_count": 1},
                {"segment": "low_volume_stable", "supplier_count": 2},
            ],
        )


if __name__ == "__main__":
    unittest.main()
