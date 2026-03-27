from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.loan_analysis.pipeline import clean_loans, summarize_by_grade  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class LoanAnalysisTests(unittest.TestCase):
    def test_clean_loans_normalizes_grade_and_derives_risk_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "loans.csv"
            write_csv(
                csv_path,
                [
                    {
                        "loan_id": " LN-100 ",
                        "grade": " b ",
                        "annual_income": "60000",
                        "debt": "18000",
                        "days_past_due": "35",
                        "loan_amount": "12000",
                    },
                    {
                        "loan_id": "LN-200",
                        "grade": "A",
                        "annual_income": "90000",
                        "debt": "9000",
                        "days_past_due": "0",
                        "loan_amount": "15000",
                    },
                ],
            )

            cleaned = clean_loans(csv_path)

            self.assertEqual(
                cleaned,
                [
                    {
                        "loan_id": "LN-100",
                        "grade": "B",
                        "annual_income": 60000.0,
                        "debt": 18000.0,
                        "days_past_due": 35,
                        "loan_amount": 12000.0,
                        "debt_to_income": 0.3,
                        "is_delinquent": 1,
                        "dti_band": "moderate",
                    },
                    {
                        "loan_id": "LN-200",
                        "grade": "A",
                        "annual_income": 90000.0,
                        "debt": 9000.0,
                        "days_past_due": 0,
                        "loan_amount": 15000.0,
                        "debt_to_income": 0.1,
                        "is_delinquent": 0,
                        "dti_band": "low",
                    },
                ],
            )

    def test_summarize_by_grade_aggregates_delinquency_and_dti(self) -> None:
        cleaned = [
            {
                "loan_id": "LN-100",
                "grade": "B",
                "annual_income": 60000.0,
                "debt": 18000.0,
                "days_past_due": 35,
                "loan_amount": 12000.0,
                "debt_to_income": 0.3,
                "is_delinquent": 1,
                "dti_band": "moderate",
            },
            {
                "loan_id": "LN-101",
                "grade": "B",
                "annual_income": 70000.0,
                "debt": 14000.0,
                "days_past_due": 0,
                "loan_amount": 10000.0,
                "debt_to_income": 0.2,
                "is_delinquent": 0,
                "dti_band": "moderate",
            },
            {
                "loan_id": "LN-200",
                "grade": "A",
                "annual_income": 90000.0,
                "debt": 9000.0,
                "days_past_due": 0,
                "loan_amount": 15000.0,
                "debt_to_income": 0.1,
                "is_delinquent": 0,
                "dti_band": "low",
            },
        ]

        summary = summarize_by_grade(cleaned)

        self.assertEqual(
            summary,
            [
                {
                    "grade": "A",
                    "loan_count": 1,
                    "delinquent_loans": 0,
                    "delinquency_rate": 0.0,
                    "avg_debt_to_income": 0.1,
                },
                {
                    "grade": "B",
                    "loan_count": 2,
                    "delinquent_loans": 1,
                    "delinquency_rate": 0.5,
                    "avg_debt_to_income": 0.25,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
