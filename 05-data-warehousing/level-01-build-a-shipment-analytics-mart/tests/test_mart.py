from __future__ import annotations

import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.shipment_mart.pipeline import build_shipment_analytics_mart  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ShipmentMartTests(unittest.TestCase):
    def test_build_mart_creates_dim_route_and_fact_shipments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            cleaned_path = base / "cleaned_shipments.csv"
            db_path = base / "warehouse.db"

            write_csv(
                cleaned_path,
                [
                    {
                        "shipment_id": "SHP-100",
                        "route": "Monterrey->Austin",
                        "status": "delivered",
                        "carrier": "Northwind",
                        "weight_kg": "10.5",
                        "promised_date": "2026-01-12",
                        "delivered_date": "2026-01-13",
                        "delay_days": "1",
                        "is_late": "1",
                    },
                    {
                        "shipment_id": "SHP-101",
                        "route": "Monterrey->Austin",
                        "status": "delivered",
                        "carrier": "Northwind",
                        "weight_kg": "8.0",
                        "promised_date": "2026-01-12",
                        "delivered_date": "2026-01-12",
                        "delay_days": "0",
                        "is_late": "0",
                    },
                    {
                        "shipment_id": "SHP-200",
                        "route": "Guadalajara->Dallas",
                        "status": "in_transit",
                        "carrier": "BlueFreight",
                        "weight_kg": "7.0",
                        "promised_date": "2026-01-15",
                        "delivered_date": "",
                        "delay_days": "0",
                        "is_late": "0",
                    },
                ],
            )

            summary = build_shipment_analytics_mart(cleaned_path=cleaned_path, db_path=db_path)

            self.assertEqual(summary.routes_loaded, 2)
            self.assertEqual(summary.shipments_loaded, 3)
            self.assertEqual(summary.mart_rows, 2)

            with sqlite3.connect(db_path) as connection:
                dim_routes = connection.execute(
                    "SELECT route_key, route_name FROM dim_route ORDER BY route_key"
                ).fetchall()
                mart_rows = connection.execute(
                    """
                    SELECT route_name, shipment_count, late_shipments, avg_delay_days
                    FROM mart_route_kpis
                    ORDER BY route_name
                    """
                ).fetchall()

            self.assertEqual(
                dim_routes,
                [
                    (1, "Guadalajara->Dallas"),
                    (2, "Monterrey->Austin"),
                ],
            )
            self.assertEqual(
                mart_rows,
                [
                    ("Guadalajara->Dallas", 1, 0, 0.0),
                    ("Monterrey->Austin", 2, 1, 0.5),
                ],
            )


if __name__ == "__main__":
    unittest.main()
