from __future__ import annotations

import csv
from pathlib import Path


FEATURES = ["route_risk_score", "carrier_delay_rate", "weight_kg"]


def load_training_rows(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "shipment_id": row["shipment_id"],
                    "weight_kg": float(row["weight_kg"]),
                    "route_risk_score": float(row["route_risk_score"]),
                    "carrier_delay_rate": float(row["carrier_delay_rate"]),
                    "is_late": int(row["is_late"]),
                }
            )
    return rows


def train_delay_rule(rows: list[dict[str, object]]) -> dict[str, object]:
    best_rule: dict[str, object] | None = None

    for feature in FEATURES:
        thresholds = sorted({float(row[feature]) for row in rows}, reverse=True)
        for threshold in thresholds:
            predictions = _predict(feature, threshold, rows)
            accuracy = _accuracy(predictions, rows)
            candidate = {
                "feature": feature,
                "threshold": threshold,
                "accuracy": accuracy,
            }
            if best_rule is None or candidate["accuracy"] > best_rule["accuracy"]:
                best_rule = candidate

    assert best_rule is not None
    return best_rule


def evaluate_threshold_rule(
    rule: dict[str, object], rows: list[dict[str, object]]
) -> dict[str, object]:
    predictions = _predict(str(rule["feature"]), float(rule["threshold"]), rows)
    accuracy = _accuracy(predictions, rows)
    return {"accuracy": accuracy, "predictions": predictions}


def _predict(
    feature: str, threshold: float, rows: list[dict[str, object]]
) -> list[int]:
    return [1 if float(row[feature]) >= threshold else 0 for row in rows]


def _accuracy(predictions: list[int], rows: list[dict[str, object]]) -> float:
    matches = sum(
        1 for prediction, row in zip(predictions, rows) if prediction == int(row["is_late"])
    )
    return matches / len(rows) if rows else 0.0

