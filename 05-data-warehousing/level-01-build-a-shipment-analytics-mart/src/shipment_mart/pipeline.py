from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MartSummary:
    routes_loaded: int
    shipments_loaded: int
    mart_rows: int


def build_shipment_analytics_mart(cleaned_path: Path, db_path: Path) -> MartSummary:
    rows = _load_cleaned_rows(cleaned_path)
    routes = sorted({row["route"] for row in rows})
    route_keys = {route: index for index, route in enumerate(routes, start=1)}

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        _create_schema(connection)
        connection.executemany(
            "INSERT INTO dim_route (route_key, route_name) VALUES (?, ?)",
            [(route_keys[route], route) for route in routes],
        )
        connection.executemany(
            """
            INSERT INTO fact_shipments (
                shipment_id,
                route_key,
                status,
                carrier,
                weight_kg,
                promised_date,
                delivered_date,
                delay_days,
                is_late
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["shipment_id"],
                    route_keys[row["route"]],
                    row["status"],
                    row["carrier"],
                    row["weight_kg"],
                    row["promised_date"],
                    row["delivered_date"],
                    row["delay_days"],
                    row["is_late"],
                )
                for row in rows
            ],
        )

        mart_sql = (
            Path(__file__).resolve().parents[2] / "sql" / "build_mart_route_kpis.sql"
        ).read_text(encoding="utf-8")
        connection.executescript(mart_sql)

        mart_rows = connection.execute(
            "SELECT COUNT(*) FROM mart_route_kpis"
        ).fetchone()[0]

    return MartSummary(
        routes_loaded=len(routes),
        shipments_loaded=len(rows),
        mart_rows=mart_rows,
    )


def _load_cleaned_rows(cleaned_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with cleaned_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "shipment_id": row["shipment_id"],
                    "route": row["route"],
                    "status": row["status"],
                    "carrier": row["carrier"],
                    "weight_kg": float(row["weight_kg"]),
                    "promised_date": row["promised_date"],
                    "delivered_date": row["delivered_date"],
                    "delay_days": int(row["delay_days"]),
                    "is_late": int(row["is_late"]),
                }
            )
    return rows


def _create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        DROP TABLE IF EXISTS mart_route_kpis;
        DROP TABLE IF EXISTS fact_shipments;
        DROP TABLE IF EXISTS dim_route;

        CREATE TABLE dim_route (
            route_key INTEGER PRIMARY KEY,
            route_name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE fact_shipments (
            shipment_id TEXT PRIMARY KEY,
            route_key INTEGER NOT NULL,
            status TEXT NOT NULL,
            carrier TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            promised_date TEXT NOT NULL,
            delivered_date TEXT,
            delay_days INTEGER NOT NULL,
            is_late INTEGER NOT NULL,
            FOREIGN KEY(route_key) REFERENCES dim_route(route_key)
        );
        """
    )

