from __future__ import annotations

import csv
from pathlib import Path


def load_shipments(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "shipment_id": row["shipment_id"].strip().upper(),
                    "route": row["route"].strip(),
                    "weight_kg": float(row["weight_kg"]),
                }
            )
    return rows


def build_weight_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    shipment_count = len(rows)
    unique_routes = len({str(row["route"]) for row in rows})
    average_weight = sum(float(row["weight_kg"]) for row in rows) / shipment_count

    route_weights: dict[str, float] = {}
    for row in rows:
        route = str(row["route"])
        route_weights[route] = route_weights.get(route, 0.0) + float(row["weight_kg"])

    heaviest_route = max(route_weights, key=route_weights.get)

    return {
        "shipment_count": shipment_count,
        "unique_routes": unique_routes,
        "average_weight_kg": round(average_weight, 1),
        "heaviest_route": heaviest_route,
    }


def write_summary(summary: dict[str, object], report_path: Path) -> None:
    report = (
        "Python Data Work Refresher Summary\n"
        f"Shipment count: {summary['shipment_count']}\n"
        f"Unique routes: {summary['unique_routes']}\n"
        f"Average weight (kg): {summary['average_weight_kg']}\n"
        f"Heaviest route: {summary['heaviest_route']}\n"
    )
    report_path.write_text(report, encoding="utf-8")

