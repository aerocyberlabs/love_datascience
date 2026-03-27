from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


def clean_shipments(raw_path: Path) -> list[dict[str, object]]:
    cleaned_rows: list[dict[str, object]] = []

    with raw_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            shipment_id = row["shipment_id"].strip().upper()
            origin = row["origin"].strip()
            destination = row["destination"].strip()
            status = row["status"].strip().lower()
            carrier = row["carrier"].strip()
            promised_date = row["promised_date"].strip()
            delivered_date = row["delivered_date"].strip()
            weight_kg = float(row["weight_kg"])

            delay_days = _compute_delay_days(
                promised_date=promised_date, delivered_date=delivered_date
            )
            is_late = 1 if delay_days > 0 else 0

            cleaned_rows.append(
                {
                    "shipment_id": shipment_id,
                    "route": f"{origin}->{destination}",
                    "status": status,
                    "carrier": carrier,
                    "weight_kg": weight_kg,
                    "promised_date": promised_date,
                    "delivered_date": delivered_date,
                    "delay_days": delay_days,
                    "is_late": is_late,
                }
            )

    return cleaned_rows


def summarize_routes(cleaned_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "shipment_count": 0.0,
            "late_shipments": 0.0,
            "delay_days_total": 0.0,
            "total_weight_kg": 0.0,
        }
    )

    for row in cleaned_rows:
        route = str(row["route"])
        grouped[route]["shipment_count"] += 1
        grouped[route]["late_shipments"] += float(row["is_late"])
        grouped[route]["delay_days_total"] += float(row["delay_days"])
        grouped[route]["total_weight_kg"] += float(row["weight_kg"])

    summary: list[dict[str, object]] = []
    for route in sorted(grouped):
        shipment_count = int(grouped[route]["shipment_count"])
        late_shipments = int(grouped[route]["late_shipments"])
        late_ratio = late_shipments / shipment_count if shipment_count else 0.0
        avg_delay_days = (
            grouped[route]["delay_days_total"] / shipment_count if shipment_count else 0.0
        )

        summary.append(
            {
                "route": route,
                "shipment_count": shipment_count,
                "late_shipments": late_shipments,
                "late_ratio": late_ratio,
                "avg_delay_days": avg_delay_days,
                "total_weight_kg": grouped[route]["total_weight_kg"],
            }
        )

    return summary


def _compute_delay_days(promised_date: str, delivered_date: str) -> int:
    if not delivered_date:
        return 0

    promised = date.fromisoformat(promised_date)
    delivered = date.fromisoformat(delivered_date)
    return max((delivered - promised).days, 0)

