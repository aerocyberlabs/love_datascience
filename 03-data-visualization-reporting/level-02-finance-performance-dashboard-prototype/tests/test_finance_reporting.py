from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.finance_reporting.pipeline import (  # noqa: E402
    build_finance_kpis,
    load_grade_summary,
    render_markdown_report,
)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class FinanceReportingTests(unittest.TestCase):
    def test_load_grade_summary_parses_numeric_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "grade_summary.csv"
            write_csv(
                csv_path,
                [
                    {
                        "grade": "A",
                        "loan_count": "1",
                        "delinquent_loans": "0",
                        "delinquency_rate": "0.0",
                        "avg_debt_to_income": "0.1",
                    }
                ],
            )

            rows = load_grade_summary(csv_path)

            self.assertEqual(
                rows,
                [
                    {
                        "grade": "A",
                        "loan_count": 1,
                        "delinquent_loans": 0,
                        "delinquency_rate": 0.0,
                        "avg_debt_to_income": 0.1,
                    }
                ],
            )

    def test_build_finance_kpis_returns_portfolio_metrics(self) -> None:
        rows = [
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
        ]

        kpis = build_finance_kpis(rows)

        self.assertEqual(
            kpis,
            {
                "portfolio_loans": 3,
                "portfolio_delinquency_rate": 0.333,
                "highest_risk_grade": "B",
                "highest_dti_grade": "B",
            },
        )

    def test_render_markdown_report_includes_snapshot_and_table(self) -> None:
        rows = [
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
        ]
        kpis = {
            "portfolio_loans": 3,
            "portfolio_delinquency_rate": 0.333,
            "highest_risk_grade": "B",
            "highest_dti_grade": "B",
        }

        report = render_markdown_report(kpis, rows)

        self.assertIn("# Finance Performance Dashboard Prototype", report)
        self.assertIn("- Portfolio loans: 3", report)
        self.assertIn("- Portfolio delinquency rate: 0.333", report)
        self.assertIn("| Grade | Loans | Delinquent Loans | Delinquency Rate | Avg Debt-to-Income |", report)
        self.assertIn("| B | 2 | 1 | 0.5 | 0.25 |", report)


if __name__ == "__main__":
    unittest.main()
