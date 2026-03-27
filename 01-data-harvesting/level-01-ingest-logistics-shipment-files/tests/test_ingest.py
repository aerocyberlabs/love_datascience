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

from src.shipment_ingest.pipeline import SchemaError, ingest_shipments  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ShipmentIngestTests(unittest.TestCase):
    def test_ingest_shipments_merges_files_and_keeps_latest_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            raw_dir = base / "raw"
            raw_dir.mkdir()
            db_path = base / "warehouse.db"

            write_csv(
                raw_dir / "shipments_jan.csv",
                [
                    {
                        "shipment_id": "SHP-100",
                        "order_id": "ORD-1",
                        "origin": "Monterrey",
                        "destination": "Austin",
                        "status": "in_transit",
                        "event_ts": "2026-01-10T08:00:00",
                        "carrier": "Northwind",
                        "weight_kg": "10.5",
                    },
                    {
                        "shipment_id": "SHP-200",
                        "order_id": "ORD-2",
                        "origin": "Guadalajara",
                        "destination": "Dallas",
                        "status": "delayed",
                        "event_ts": "2026-01-12T11:30:00",
                        "carrier": "BlueFreight",
                        "weight_kg": "7.0",
                    },
                ],
            )
            write_csv(
                raw_dir / "shipments_feb.csv",
                [
                    {
                        "shipment_id": "SHP-100",
                        "order_id": "ORD-1",
                        "origin": "Monterrey",
                        "destination": "Austin",
                        "status": "delivered",
                        "event_ts": "2026-01-10T18:15:00",
                        "carrier": "Northwind",
                        "weight_kg": "10.5",
                    }
                ],
            )

            summary = ingest_shipments(raw_dir=raw_dir, db_path=db_path)

            self.assertEqual(summary.files_processed, 2)
            self.assertEqual(summary.rows_seen, 3)
            self.assertEqual(summary.rows_upserted, 2)

            with sqlite3.connect(db_path) as connection:
                rows = connection.execute(
                    """
                    SELECT shipment_id, status, event_ts
                    FROM shipments
                    ORDER BY shipment_id
                    """
                ).fetchall()

            self.assertEqual(
                rows,
                [
                    ("SHP-100", "delivered", "2026-01-10T18:15:00"),
                    ("SHP-200", "delayed", "2026-01-12T11:30:00"),
                ],
            )

    def test_ingest_shipments_rejects_invalid_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            raw_dir = base / "raw"
            raw_dir.mkdir()

            write_csv(
                raw_dir / "broken_shipments.csv",
                [
                    {
                        "shipment_id": "SHP-999",
                        "origin": "Monterrey",
                        "destination": "Austin",
                        "status": "lost",
                        "event_ts": "2026-01-10T18:15:00",
                        "carrier": "Northwind",
                        "weight_kg": "10.5",
                    }
                ],
            )

            with self.assertRaises(SchemaError):
                ingest_shipments(raw_dir=raw_dir, db_path=base / "warehouse.db")


if __name__ == "__main__":
    unittest.main()
