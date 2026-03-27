from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.delay_risk.pipeline import (  # noqa: E402
    evaluate_threshold_rule,
    load_training_rows,
    train_delay_rule,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class DelayRiskTests(unittest.TestCase):
    def test_load_training_rows_parses_numeric_features(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "training.csv"
            write_csv(
                csv_path,
                [
                    {
                        "shipment_id": "SHP-100",
                        "weight_kg": "10.5",
                        "route_risk_score": "0.9",
                        "carrier_delay_rate": "0.6",
                        "is_late": "1",
                    }
                ],
            )

            rows = load_training_rows(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "shipment_id": "SHP-100",
                        "weight_kg": 10.5,
                        "route_risk_score": 0.9,
                        "carrier_delay_rate": 0.6,
                        "is_late": 1,
                    }
                ],
            )

    def test_train_delay_rule_finds_best_threshold(self) -> None:
        rows = [
            {
                "shipment_id": "SHP-100",
                "weight_kg": 12.0,
                "route_risk_score": 0.9,
                "carrier_delay_rate": 0.8,
                "is_late": 1,
            },
            {
                "shipment_id": "SHP-101",
                "weight_kg": 11.5,
                "route_risk_score": 0.8,
                "carrier_delay_rate": 0.7,
                "is_late": 1,
            },
            {
                "shipment_id": "SHP-200",
                "weight_kg": 7.0,
                "route_risk_score": 0.2,
                "carrier_delay_rate": 0.3,
                "is_late": 0,
            },
            {
                "shipment_id": "SHP-201",
                "weight_kg": 6.5,
                "route_risk_score": 0.1,
                "carrier_delay_rate": 0.2,
                "is_late": 0,
            },
        ]

        rule = train_delay_rule(rows)

        self.assertEqual(rule["feature"], "route_risk_score")
        self.assertEqual(rule["threshold"], 0.8)
        self.assertEqual(rule["accuracy"], 1.0)

    def test_evaluate_threshold_rule_reports_accuracy_and_predictions(self) -> None:
        rows = [
            {
                "shipment_id": "SHP-100",
                "weight_kg": 12.0,
                "route_risk_score": 0.9,
                "carrier_delay_rate": 0.8,
                "is_late": 1,
            },
            {
                "shipment_id": "SHP-200",
                "weight_kg": 7.0,
                "route_risk_score": 0.2,
                "carrier_delay_rate": 0.3,
                "is_late": 0,
            },
        ]
        rule = {"feature": "route_risk_score", "threshold": 0.8, "accuracy": 1.0}

        metrics = evaluate_threshold_rule(rule, rows)

        self.assertEqual(metrics["accuracy"], 1.0)
        self.assertEqual(metrics["predictions"], [1, 0])


if __name__ == "__main__":
    unittest.main()
