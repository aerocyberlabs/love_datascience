from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.market_harvest.pipeline import (  # noqa: E402
    MarketSchemaError,
    harvest_market_pages,
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


class MarketHarvestTests(unittest.TestCase):
    def test_harvest_market_pages_loads_paginated_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            fixture_dir = base / "fixtures"
            fixture_dir.mkdir()
            db_path = base / "market.db"

            write_json(
                fixture_dir / "page_1.json",
                {
                    "next_page": "page_2.json",
                    "results": [
                        {
                            "symbol": "AERO",
                            "trade_date": "2026-02-01",
                            "close_price": 102.5,
                            "volume": 1250000,
                        },
                        {
                            "symbol": "NOVA",
                            "trade_date": "2026-02-01",
                            "close_price": 44.2,
                            "volume": 880000,
                        },
                    ],
                },
            )
            write_json(
                fixture_dir / "page_2.json",
                {
                    "next_page": None,
                    "results": [
                        {
                            "symbol": "AERO",
                            "trade_date": "2026-02-02",
                            "close_price": 104.1,
                            "volume": 1310000,
                        }
                    ],
                },
            )

            summary = harvest_market_pages(
                fixture_dir=fixture_dir,
                first_page="page_1.json",
                db_path=db_path,
            )

            self.assertEqual(summary.pages_processed, 2)
            self.assertEqual(summary.records_seen, 3)
            self.assertEqual(summary.records_loaded, 3)

            with sqlite3.connect(db_path) as connection:
                rows = connection.execute(
                    """
                    SELECT symbol, trade_date, close_price, volume
                    FROM market_prices
                    ORDER BY trade_date, symbol
                    """
                ).fetchall()

            self.assertEqual(
                rows,
                [
                    ("AERO", "2026-02-01", 102.5, 1250000),
                    ("NOVA", "2026-02-01", 44.2, 880000),
                    ("AERO", "2026-02-02", 104.1, 1310000),
                ],
            )

    def test_harvest_market_pages_rejects_invalid_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            fixture_dir = base / "fixtures"
            fixture_dir.mkdir()

            write_json(
                fixture_dir / "page_1.json",
                {
                    "next_page": None,
                    "results": [
                        {
                            "symbol": "AERO",
                            "trade_date": "2026-02-01",
                            "volume": 1250000,
                        }
                    ],
                },
            )

            with self.assertRaises(MarketSchemaError):
                harvest_market_pages(
                    fixture_dir=fixture_dir,
                    first_page="page_1.json",
                    db_path=base / "market.db",
                )


if __name__ == "__main__":
    unittest.main()
