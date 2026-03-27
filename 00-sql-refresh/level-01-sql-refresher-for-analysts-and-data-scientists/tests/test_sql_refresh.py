from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sql_refresh.setup import initialize_database, run_query_file  # noqa: E402


class SqlRefreshTests(unittest.TestCase):
    def test_initialize_database_creates_seeded_tables(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sql_refresh.db"

            initialize_database(db_path)

            with sqlite3.connect(db_path) as connection:
                shipment_count = connection.execute(
                    "SELECT COUNT(*) FROM shipments"
                ).fetchone()[0]
                route_count = connection.execute(
                    "SELECT COUNT(*) FROM routes"
                ).fetchone()[0]

            self.assertEqual(shipment_count, 5)
            self.assertEqual(route_count, 3)

    def test_run_query_file_executes_aggregation_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sql_refresh.db"
            initialize_database(db_path)

            query_path = (
                PROJECT_ROOT
                / "sql"
                / "02_aggregation_route_metrics.sql"
            )

            rows = run_query_file(db_path, query_path)

            self.assertEqual(
                rows,
                [
                    ("Guadalajara->Dallas", 1, 0),
                    ("Monterrey->Austin", 2, 1),
                    ("Tijuana->Houston", 2, 1),
                ],
            )

    def test_run_query_file_executes_window_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sql_refresh.db"
            initialize_database(db_path)

            query_path = PROJECT_ROOT / "sql" / "03_window_rank_routes.sql"

            rows = run_query_file(db_path, query_path)

            self.assertEqual(
                rows,
                [
                    ("Monterrey->Austin", 18.5, 1),
                    ("Tijuana->Houston", 11.4, 2),
                    ("Guadalajara->Dallas", 7.0, 3),
                ],
            )


if __name__ == "__main__":
    unittest.main()
