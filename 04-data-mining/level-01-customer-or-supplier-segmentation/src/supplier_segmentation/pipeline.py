from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


def load_supplier_metrics(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "supplier_id": row["supplier_id"],
                    "on_time_rate": float(row["on_time_rate"]),
                    "monthly_shipments": int(row["monthly_shipments"]),
                    "avg_delay_days": float(row["avg_delay_days"]),
                }
            )
    return rows


def assign_segments(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    segmented_rows: list[dict[str, object]] = []

    for row in rows:
        monthly_shipments = int(row["monthly_shipments"])
        on_time_rate = float(row["on_time_rate"])
        avg_delay_days = float(row["avg_delay_days"])

        if monthly_shipments >= 100 and (on_time_rate < 0.8 or avg_delay_days >= 2.0):
            segment = "high_volume_risky"
        elif monthly_shipments >= 100:
            segment = "high_volume_reliable"
        else:
            segment = "low_volume_stable"

        segmented_rows.append({**row, "segment": segment})

    return segmented_rows


def summarize_segments(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts = Counter(str(row["segment"]) for row in rows)
    return [
        {"segment": segment, "supplier_count": counts[segment]}
        for segment in sorted(counts)
    ]

