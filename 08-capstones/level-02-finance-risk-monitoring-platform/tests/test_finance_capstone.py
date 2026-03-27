from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.finance_capstone.pipeline import run_finance_capstone  # noqa: E402


class FinanceCapstoneTests(unittest.TestCase):
    def test_run_finance_capstone_builds_linked_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "finance_capstone_outputs"

            summary = run_finance_capstone(output_dir=output_dir)

            self.assertEqual(summary["harvest_pages_processed"], 2)
            self.assertEqual(summary["wrangling_rows"], 3)
            self.assertEqual(summary["grade_summary_rows"], 2)
            self.assertEqual(summary["warehouse_mart_rows"], 2)
            self.assertEqual(summary["model_feature"], "days_past_due")
            self.assertEqual(summary["pipeline_files_registered"], 1)

            expected_paths = [
                output_dir / "harvest" / "market.db",
                output_dir / "wrangling" / "cleaned_loans.csv",
                output_dir / "reporting" / "finance_dashboard_report.md",
                output_dir / "warehouse" / "finance_warehouse.db",
                output_dir / "ml" / "default_rule.json",
                output_dir / "cloud" / "runs" / "loan_grade_summary_2026-02-10.json",
                output_dir / "capstone_summary.json",
            ]

            for path in expected_paths:
                self.assertTrue(path.exists(), f"missing expected artifact: {path}")

            manifest = json.loads(
                (output_dir / "capstone_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["grade_summary_rows"], 2)
            self.assertEqual(manifest["model_feature"], "days_past_due")


if __name__ == "__main__":
    unittest.main()
