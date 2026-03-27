from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path


EXPECTED_COLUMNS = [
    "shipment_id",
    "order_id",
    "origin",
    "destination",
    "status",
    "event_ts",
    "carrier",
    "weight_kg",
]


class SchemaError(ValueError):
    """Raised when a shipment CSV file does not match the expected schema."""


@dataclass(frozen=True)
class IngestSummary:
    files_processed: int
    rows_seen: int
    rows_upserted: int


def ingest_shipments(raw_dir: Path, db_path: Path) -> IngestSummary:
    csv_paths = sorted(raw_dir.glob("*.csv"))
    if not csv_paths:
        return IngestSummary(files_processed=0, rows_seen=0, rows_upserted=0)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    rows_seen = 0
    with sqlite3.connect(db_path) as connection:
        _create_table(connection)
        for csv_path in csv_paths:
            rows_seen += _load_csv(connection, csv_path)
        rows_upserted = connection.execute(
            "SELECT COUNT(*) FROM shipments"
        ).fetchone()[0]

    return IngestSummary(
        files_processed=len(csv_paths),
        rows_seen=rows_seen,
        rows_upserted=rows_upserted,
    )


def _create_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS shipments (
            shipment_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            status TEXT NOT NULL,
            event_ts TEXT NOT NULL,
            carrier TEXT NOT NULL,
            weight_kg REAL NOT NULL
        )
        """
    )


def _load_csv(connection: sqlite3.Connection, csv_path: Path) -> int:
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise SchemaError(
                f"{csv_path.name} has schema {reader.fieldnames}, expected {EXPECTED_COLUMNS}"
            )

        rows_loaded = 0
        for row in reader:
            connection.execute(
                """
                INSERT INTO shipments (
                    shipment_id,
                    order_id,
                    origin,
                    destination,
                    status,
                    event_ts,
                    carrier,
                    weight_kg
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(shipment_id) DO UPDATE SET
                    order_id = excluded.order_id,
                    origin = excluded.origin,
                    destination = excluded.destination,
                    status = excluded.status,
                    event_ts = excluded.event_ts,
                    carrier = excluded.carrier,
                    weight_kg = excluded.weight_kg
                WHERE excluded.event_ts > shipments.event_ts
                """,
                (
                    row["shipment_id"],
                    row["order_id"],
                    row["origin"],
                    row["destination"],
                    row["status"],
                    row["event_ts"],
                    row["carrier"],
                    float(row["weight_kg"]),
                ),
            )
            rows_loaded += 1

    return rows_loaded

