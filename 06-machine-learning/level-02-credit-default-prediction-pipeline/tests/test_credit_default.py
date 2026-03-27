from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.credit_default.pipeline import (  # noqa: E402
    evaluate_default_rule,
    load_credit_rows,
    train_default_rule,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class CreditDefaultTests(unittest.TestCase):
    def test_load_credit_rows_parses_numeric_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "credit.csv"
            write_csv(
                csv_path,
                [
                    {
                        "loan_id": "LN-100",
                        "grade_score": "0.55",
                        "debt_to_income": "0.40",
                        "days_past_due": "45",
                        "defaulted": "1",
                    }
                ],
            )

            rows = load_credit_rows(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "loan_id": "LN-100",
                        "grade_score": 0.55,
                        "debt_to_income": 0.40,
                        "days_past_due": 45,
                        "defaulted": 1,
                    }
                ],
            )

    def test_train_default_rule_finds_best_threshold(self) -> None:
        rows = [
            {
                "loan_id": "LN-100",
                "grade_score": 0.55,
                "debt_to_income": 0.40,
                "days_past_due": 45,
                "defaulted": 1,
            },
            {
                "loan_id": "LN-101",
                "grade_score": 0.50,
                "debt_to_income": 0.38,
                "days_past_due": 35,
                "defaulted": 1,
            },
            {
                "loan_id": "LN-200",
                "grade_score": 0.90,
                "debt_to_income": 0.12,
                "days_past_due": 0,
                "defaulted": 0,
            },
            {
                "loan_id": "LN-201",
                "grade_score": 0.85,
                "debt_to_income": 0.18,
                "days_past_due": 5,
                "defaulted": 0,
            },
        ]

        rule = train_default_rule(rows)

        self.assertEqual(rule["feature"], "days_past_due")
        self.assertEqual(rule["threshold"], 35)
        self.assertEqual(rule["direction"], "ge")
        self.assertEqual(rule["accuracy"], 1.0)

    def test_evaluate_default_rule_reports_accuracy_precision_and_recall(self) -> None:
        rows = [
            {
                "loan_id": "LN-100",
                "grade_score": 0.55,
                "debt_to_income": 0.40,
                "days_past_due": 45,
                "defaulted": 1,
            },
            {
                "loan_id": "LN-200",
                "grade_score": 0.90,
                "debt_to_income": 0.12,
                "days_past_due": 0,
                "defaulted": 0,
            },
        ]
        rule = {
            "feature": "days_past_due",
            "threshold": 35,
            "direction": "ge",
            "accuracy": 1.0,
        }

        metrics = evaluate_default_rule(rule, rows)

        self.assertEqual(metrics["accuracy"], 1.0)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)
        self.assertEqual(metrics["predictions"], [1, 0])


if __name__ == "__main__":
    unittest.main()
