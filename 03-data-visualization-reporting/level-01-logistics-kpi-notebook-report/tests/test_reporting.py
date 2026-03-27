from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logistics_reporting.pipeline import (  # noqa: E402
    build_kpi_snapshot,
    load_route_summary,
    render_markdown_report,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class LogisticsReportingTests(unittest.TestCase):
    def test_load_route_summary_parses_numeric_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "route_summary.csv"
            write_csv(
                csv_path,
                [
                    {
                        "route": "Guadalajara->Dallas",
                        "shipment_count": "1",
                        "late_shipments": "0",
                        "late_ratio": "0.0",
                        "avg_delay_days": "0.0",
                        "total_weight_kg": "7.0",
                    }
                ],
            )

            rows = load_route_summary(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "route": "Guadalajara->Dallas",
                        "shipment_count": 1,
                        "late_shipments": 0,
                        "late_ratio": 0.0,
                        "avg_delay_days": 0.0,
                        "total_weight_kg": 7.0,
                    }
                ],
            )

    def test_build_kpi_snapshot_returns_core_metrics(self) -> None:
        rows = [
            {
                "route": "Guadalajara->Dallas",
                "shipment_count": 1,
                "late_shipments": 0,
                "late_ratio": 0.0,
                "avg_delay_days": 0.0,
                "total_weight_kg": 7.0,
            },
            {
                "route": "Monterrey->Austin",
                "shipment_count": 2,
                "late_shipments": 1,
                "late_ratio": 0.5,
                "avg_delay_days": 0.5,
                "total_weight_kg": 18.5,
            },
        ]

        snapshot = build_kpi_snapshot(rows)

        self.assertEqual(
            snapshot,
            {
                "total_shipments": 3,
                "total_late_shipments": 1,
                "overall_late_ratio": 0.333,
                "heaviest_route": "Monterrey->Austin",
                "worst_late_route": "Monterrey->Austin",
            },
        )

    def test_render_markdown_report_includes_summary_and_table(self) -> None:
        rows = [
            {
                "route": "Guadalajara->Dallas",
                "shipment_count": 1,
                "late_shipments": 0,
                "late_ratio": 0.0,
                "avg_delay_days": 0.0,
                "total_weight_kg": 7.0,
            },
            {
                "route": "Monterrey->Austin",
                "shipment_count": 2,
                "late_shipments": 1,
                "late_ratio": 0.5,
                "avg_delay_days": 0.5,
                "total_weight_kg": 18.5,
            },
        ]
        snapshot = {
            "total_shipments": 3,
            "total_late_shipments": 1,
            "overall_late_ratio": 0.333,
            "heaviest_route": "Monterrey->Austin",
            "worst_late_route": "Monterrey->Austin",
        }

        report = render_markdown_report(snapshot, rows)

        self.assertIn("# Logistics KPI Report", report)
        self.assertIn("- Total shipments: 3", report)
        self.assertIn("- Overall late ratio: 0.333", report)
        self.assertIn("| Route | Shipments | Late Shipments | Late Ratio | Avg Delay Days | Total Weight (kg) |", report)
        self.assertIn("| Monterrey->Austin | 2 | 1 | 0.5 | 0.5 | 18.5 |", report)


if __name__ == "__main__":
    unittest.main()
