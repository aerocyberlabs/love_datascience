from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.shipment_wrangling.pipeline import clean_shipments, summarize_routes  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ShipmentWranglingTests(unittest.TestCase):
    def test_clean_shipments_normalizes_rows_and_computes_delay_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            raw_path = base / "raw_shipments.csv"

            write_csv(
                raw_path,
                [
                    {
                        "shipment_id": " shp-100 ",
                        "origin": "Monterrey",
                        "destination": "Austin",
                        "status": " Delivered ",
                        "promised_date": "2026-01-12",
                        "delivered_date": "2026-01-13",
                        "carrier": "Northwind",
                        "weight_kg": "10.5",
                    },
                    {
                        "shipment_id": "SHP-200",
                        "origin": "Guadalajara",
                        "destination": "Dallas",
                        "status": "in_transit",
                        "promised_date": "2026-01-15",
                        "delivered_date": "",
                        "carrier": "BlueFreight",
                        "weight_kg": "7.0",
                    },
                ],
            )

            cleaned_rows = clean_shipments(raw_path)

            self.assertEqual(
                cleaned_rows,
                [
                    {
                        "shipment_id": "SHP-100",
                        "route": "Monterrey->Austin",
                        "status": "delivered",
                        "carrier": "Northwind",
                        "weight_kg": 10.5,
                        "promised_date": "2026-01-12",
                        "delivered_date": "2026-01-13",
                        "delay_days": 1,
                        "is_late": 1,
                    },
                    {
                        "shipment_id": "SHP-200",
                        "route": "Guadalajara->Dallas",
                        "status": "in_transit",
                        "carrier": "BlueFreight",
                        "weight_kg": 7.0,
                        "promised_date": "2026-01-15",
                        "delivered_date": "",
                        "delay_days": 0,
                        "is_late": 0,
                    },
                ],
            )

    def test_summarize_routes_groups_cleaned_rows(self) -> None:
        cleaned_rows = [
            {
                "shipment_id": "SHP-100",
                "route": "Monterrey->Austin",
                "status": "delivered",
                "carrier": "Northwind",
                "weight_kg": 10.5,
                "promised_date": "2026-01-12",
                "delivered_date": "2026-01-13",
                "delay_days": 1,
                "is_late": 1,
            },
            {
                "shipment_id": "SHP-101",
                "route": "Monterrey->Austin",
                "status": "delivered",
                "carrier": "Northwind",
                "weight_kg": 8.0,
                "promised_date": "2026-01-12",
                "delivered_date": "2026-01-12",
                "delay_days": 0,
                "is_late": 0,
            },
            {
                "shipment_id": "SHP-200",
                "route": "Guadalajara->Dallas",
                "status": "in_transit",
                "carrier": "BlueFreight",
                "weight_kg": 7.0,
                "promised_date": "2026-01-15",
                "delivered_date": "",
                "delay_days": 0,
                "is_late": 0,
            },
        ]

        summary = summarize_routes(cleaned_rows)

        self.assertEqual(
            summary,
            [
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
            ],
        )


if __name__ == "__main__":
    unittest.main()
