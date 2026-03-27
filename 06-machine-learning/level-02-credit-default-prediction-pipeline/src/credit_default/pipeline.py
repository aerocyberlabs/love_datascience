from __future__ import annotations

import csv
from pathlib import Path


FEATURE_DIRECTIONS = [
    ("days_past_due", "ge"),
    ("debt_to_income", "ge"),
    ("grade_score", "le"),
]


def load_credit_rows(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "loan_id": row["loan_id"],
                    "grade_score": float(row["grade_score"]),
                    "debt_to_income": float(row["debt_to_income"]),
                    "days_past_due": int(row["days_past_due"]),
                    "defaulted": int(row["defaulted"]),
                }
            )
    return rows


def train_default_rule(rows: list[dict[str, object]]) -> dict[str, object]:
    best_rule: dict[str, object] | None = None

    for feature, direction in FEATURE_DIRECTIONS:
        thresholds = sorted({float(row[feature]) for row in rows})
        for threshold in thresholds:
            predictions = _predict(rows, feature, threshold, direction)
            metrics = _compute_metrics(predictions, rows)
            candidate = {
                "feature": feature,
                "threshold": int(threshold) if feature == "days_past_due" else threshold,
                "direction": direction,
                "accuracy": metrics["accuracy"],
            }
            if best_rule is None or candidate["accuracy"] > best_rule["accuracy"]:
                best_rule = candidate

    assert best_rule is not None
    return best_rule


def evaluate_default_rule(
    rule: dict[str, object], rows: list[dict[str, object]]
) -> dict[str, object]:
    predictions = _predict(
        rows,
        str(rule["feature"]),
        float(rule["threshold"]),
        str(rule["direction"]),
    )
    metrics = _compute_metrics(predictions, rows)
    metrics["predictions"] = predictions
    return metrics


def _predict(
    rows: list[dict[str, object]],
    feature: str,
    threshold: float,
    direction: str,
) -> list[int]:
    if direction == "ge":
        return [1 if float(row[feature]) >= threshold else 0 for row in rows]
    return [1 if float(row[feature]) <= threshold else 0 for row in rows]


def _compute_metrics(
    predictions: list[int], rows: list[dict[str, object]]
) -> dict[str, float]:
    actuals = [int(row["defaulted"]) for row in rows]
    tp = sum(1 for pred, act in zip(predictions, actuals) if pred == 1 and act == 1)
    tn = sum(1 for pred, act in zip(predictions, actuals) if pred == 0 and act == 0)
    fp = sum(1 for pred, act in zip(predictions, actuals) if pred == 1 and act == 0)
    fn = sum(1 for pred, act in zip(predictions, actuals) if pred == 0 and act == 1)
    total = len(actuals)

    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {"accuracy": accuracy, "precision": precision, "recall": recall}
