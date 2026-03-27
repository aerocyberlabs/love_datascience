from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROUTES = [
    ("RT-1", "Monterrey->Austin"),
    ("RT-2", "Guadalajara->Dallas"),
    ("RT-3", "Tijuana->Houston"),
]


SHIPMENTS = [
    ("SHP-100", "RT-1", "delivered", 1, 10.5),
    ("SHP-101", "RT-1", "delivered", 0, 8.0),
    ("SHP-200", "RT-2", "in_transit", 0, 7.0),
    ("SHP-300", "RT-3", "delivered", 1, 4.2),
    ("SHP-301", "RT-3", "delivered", 0, 7.2),
]


def initialize_database(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.executescript(
            """
            DROP TABLE IF EXISTS shipments;
            DROP TABLE IF EXISTS routes;

            CREATE TABLE routes (
                route_id TEXT PRIMARY KEY,
                route_name TEXT NOT NULL
            );

            CREATE TABLE shipments (
                shipment_id TEXT PRIMARY KEY,
                route_id TEXT NOT NULL,
                status TEXT NOT NULL,
                is_late INTEGER NOT NULL,
                weight_kg REAL NOT NULL,
                FOREIGN KEY(route_id) REFERENCES routes(route_id)
            );
            """
        )
        connection.executemany(
            "INSERT INTO routes (route_id, route_name) VALUES (?, ?)", ROUTES
        )
        connection.executemany(
            """
            INSERT INTO shipments (
                shipment_id,
                route_id,
                status,
                is_late,
                weight_kg
            ) VALUES (?, ?, ?, ?, ?)
            """,
            SHIPMENTS,
        )


def run_query_file(db_path: Path, query_path: Path) -> list[tuple]:
    query = query_path.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as connection:
        return connection.execute(query).fetchall()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize the SQL refresher SQLite database."
    )
    parser.add_argument("db_path", type=Path, help="Path to the SQLite database file")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    initialize_database(args.db_path)
    print(f"Initialized SQL refresher database at {args.db_path}.")


if __name__ == "__main__":
    main()
