from __future__ import annotations

import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.finance_warehouse.pipeline import build_finance_risk_warehouse  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class FinanceWarehouseTests(unittest.TestCase):
    def test_build_finance_risk_warehouse_creates_dim_fact_and_mart(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            cleaned_path = base / "cleaned_loans.csv"
            db_path = base / "finance_warehouse.db"

            write_csv(
                cleaned_path,
                [
                    {
                        "loan_id": "LN-100",
                        "grade": "B",
                        "annual_income": "60000.0",
                        "debt": "18000.0",
                        "days_past_due": "35",
                        "loan_amount": "12000.0",
                        "debt_to_income": "0.3",
                        "is_delinquent": "1",
                        "dti_band": "moderate",
                    },
                    {
                        "loan_id": "LN-101",
                        "grade": "B",
                        "annual_income": "70000.0",
                        "debt": "14000.0",
                        "days_past_due": "0",
                        "loan_amount": "10000.0",
                        "debt_to_income": "0.2",
                        "is_delinquent": "0",
                        "dti_band": "moderate",
                    },
                    {
                        "loan_id": "LN-200",
                        "grade": "A",
                        "annual_income": "90000.0",
                        "debt": "9000.0",
                        "days_past_due": "0",
                        "loan_amount": "15000.0",
                        "debt_to_income": "0.1",
                        "is_delinquent": "0",
                        "dti_band": "low",
                    },
                ],
            )

            summary = build_finance_risk_warehouse(cleaned_path=cleaned_path, db_path=db_path)

            self.assertEqual(summary.grades_loaded, 2)
            self.assertEqual(summary.loans_loaded, 3)
            self.assertEqual(summary.mart_rows, 2)

            with sqlite3.connect(db_path) as connection:
                dim_grades = connection.execute(
                    "SELECT grade_key, grade FROM dim_grade ORDER BY grade_key"
                ).fetchall()
                mart_rows = connection.execute(
                    """
                    SELECT grade, loan_count, delinquent_loans, avg_debt_to_income
                    FROM mart_grade_risk
                    ORDER BY grade
                    """
                ).fetchall()

            self.assertEqual(dim_grades, [(1, "A"), (2, "B")])
            self.assertEqual(
                mart_rows,
                [
                    ("A", 1, 0, 0.1),
                    ("B", 2, 1, 0.25),
                ],
            )


if __name__ == "__main__":
    unittest.main()
