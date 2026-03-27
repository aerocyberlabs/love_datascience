from __future__ import annotations

import csv
from pathlib import Path


def load_route_summary(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "route": row["route"],
                    "shipment_count": int(row["shipment_count"]),
                    "late_shipments": int(row["late_shipments"]),
                    "late_ratio": float(row["late_ratio"]),
                    "avg_delay_days": float(row["avg_delay_days"]),
                    "total_weight_kg": float(row["total_weight_kg"]),
                }
            )
    return rows


def build_kpi_snapshot(rows: list[dict[str, object]]) -> dict[str, object]:
    total_shipments = sum(int(row["shipment_count"]) for row in rows)
    total_late_shipments = sum(int(row["late_shipments"]) for row in rows)
    overall_late_ratio = round(
        total_late_shipments / total_shipments if total_shipments else 0.0, 3
    )
    heaviest_route = max(rows, key=lambda row: float(row["total_weight_kg"]))["route"]
    worst_late_route = max(rows, key=lambda row: float(row["late_ratio"]))["route"]

    return {
        "total_shipments": total_shipments,
        "total_late_shipments": total_late_shipments,
        "overall_late_ratio": overall_late_ratio,
        "heaviest_route": heaviest_route,
        "worst_late_route": worst_late_route,
    }


def render_markdown_report(
    snapshot: dict[str, object], rows: list[dict[str, object]]
) -> str:
    lines = [
        "# Logistics KPI Report",
        "",
        "## Snapshot",
        "",
        f"- Total shipments: {snapshot['total_shipments']}",
        f"- Total late shipments: {snapshot['total_late_shipments']}",
        f"- Overall late ratio: {snapshot['overall_late_ratio']}",
        f"- Heaviest route: {snapshot['heaviest_route']}",
        f"- Worst late route: {snapshot['worst_late_route']}",
        "",
        "## Route Summary",
        "",
        "| Route | Shipments | Late Shipments | Late Ratio | Avg Delay Days | Total Weight (kg) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in rows:
        lines.append(
            "| "
            f"{row['route']} | "
            f"{row['shipment_count']} | "
            f"{row['late_shipments']} | "
            f"{row['late_ratio']} | "
            f"{row['avg_delay_days']} | "
            f"{row['total_weight_kg']} |"
        )

    return "\n".join(lines) + "\n"

