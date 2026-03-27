from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.finance_pipeline.pipeline import build_finance_batch_pipeline  # noqa: E402


class FinanceBatchPipelineTests(unittest.TestCase):
    def test_build_finance_batch_pipeline_creates_manifest_and_layer_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source_dir = base / "source"
            source_dir.mkdir()
            (source_dir / "loan_grade_summary.csv").write_text(
                "grade,loan_count,delinquent_loans,delinquency_rate,avg_debt_to_income\n"
                "A,1,0,0.0,0.1\n",
                encoding="utf-8",
            )

            pipeline_dir = base / "pipeline"

            summary = build_finance_batch_pipeline(
                source_dir=source_dir,
                pipeline_dir=pipeline_dir,
                dataset_name="loan_grade_summary",
                run_date="2026-02-10",
            )

            self.assertEqual(summary["files_registered"], 1)
            self.assertEqual(summary["job_name"], "finance-batch-pipeline")

            manifest_path = pipeline_dir / "runs" / "loan_grade_summary_2026-02-10.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertEqual(
                manifest["raw_keys"],
                [
                    "raw/finance/loan_grade_summary/run_date=2026-02-10/loan_grade_summary.csv"
                ],
            )
            self.assertEqual(
                manifest["staging_key"],
                "staging/finance/loan_grade_summary/run_date=2026-02-10/loan_grade_summary.parquet",
            )
            self.assertEqual(
                manifest["mart_target"],
                "mart/finance/loan_grade_summary",
            )


if __name__ == "__main__":
    unittest.main()
