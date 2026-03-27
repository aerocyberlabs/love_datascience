from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path


EXPECTED_FIELDS = {"symbol", "trade_date", "close_price", "volume"}


class MarketSchemaError(ValueError):
    """Raised when a market record is missing expected fields."""


@dataclass(frozen=True)
class MarketHarvestSummary:
    pages_processed: int
    records_seen: int
    records_loaded: int


def harvest_market_pages(
    fixture_dir: Path,
    first_page: str,
    db_path: Path,
) -> MarketHarvestSummary:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    page_name: str | None = first_page
    pages_processed = 0
    records_seen = 0

    with sqlite3.connect(db_path) as connection:
        _create_table(connection)

        while page_name is not None:
            payload = json.loads((fixture_dir / page_name).read_text(encoding="utf-8"))
            pages_processed += 1

            for record in payload["results"]:
                if set(record) != EXPECTED_FIELDS:
                    raise MarketSchemaError(
                        f"Record fields {sorted(record)} do not match expected {sorted(EXPECTED_FIELDS)}"
                    )

                connection.execute(
                    """
                    INSERT OR REPLACE INTO market_prices (
                        symbol,
                        trade_date,
                        close_price,
                        volume
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        record["symbol"],
                        record["trade_date"],
                        float(record["close_price"]),
                        int(record["volume"]),
                    ),
                )
                records_seen += 1

            page_name = payload["next_page"]

        records_loaded = connection.execute(
            "SELECT COUNT(*) FROM market_prices"
        ).fetchone()[0]

    return MarketHarvestSummary(
        pages_processed=pages_processed,
        records_seen=records_seen,
        records_loaded=records_loaded,
    )


def _create_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS market_prices (
            symbol TEXT NOT NULL,
            trade_date TEXT NOT NULL,
            close_price REAL NOT NULL,
            volume INTEGER NOT NULL,
            PRIMARY KEY (symbol, trade_date)
        )
        """
    )

