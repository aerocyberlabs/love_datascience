from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.python_refresh.pipeline import (  # noqa: E402
    build_weight_summary,
    load_shipments,
    write_summary,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class PythonRefreshTests(unittest.TestCase):
    def test_load_shipments_normalizes_ids_and_weight(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "shipments.csv"
            write_csv(
                csv_path,
                [
                    {
                        "shipment_id": " shp-100 ",
                        "route": "Monterrey->Austin",
                        "weight_kg": "10.5",
                    }
                ],
            )

            rows = load_shipments(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "shipment_id": "SHP-100",
                        "route": "Monterrey->Austin",
                        "weight_kg": 10.5,
                    }
                ],
            )

    def test_build_weight_summary_returns_counts_and_average(self) -> None:
        rows = [
            {"shipment_id": "SHP-100", "route": "Monterrey->Austin", "weight_kg": 10.5},
            {"shipment_id": "SHP-101", "route": "Monterrey->Austin", "weight_kg": 8.0},
            {"shipment_id": "SHP-200", "route": "Guadalajara->Dallas", "weight_kg": 7.0},
        ]

        summary = build_weight_summary(rows)

        self.assertEqual(
            summary,
            {
                "shipment_count": 3,
                "unique_routes": 2,
                "average_weight_kg": 8.5,
                "heaviest_route": "Monterrey->Austin",
            },
        )

    def test_write_summary_outputs_readable_report(self) -> None:
        summary = {
            "shipment_count": 3,
            "unique_routes": 2,
            "average_weight_kg": 8.5,
            "heaviest_route": "Monterrey->Austin",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "summary.txt"

            write_summary(summary, report_path)

            report = report_path.read_text(encoding="utf-8")

        self.assertIn("Shipment count: 3", report)
        self.assertIn("Unique routes: 2", report)
        self.assertIn("Average weight (kg): 8.5", report)
        self.assertIn("Heaviest route: Monterrey->Austin", report)


if __name__ == "__main__":
    unittest.main()
