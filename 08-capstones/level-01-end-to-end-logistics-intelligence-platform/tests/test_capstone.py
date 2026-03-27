from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logistics_capstone.pipeline import run_logistics_capstone  # noqa: E402


class LogisticsCapstoneTests(unittest.TestCase):
    def test_run_logistics_capstone_builds_linked_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "capstone_outputs"

            summary = run_logistics_capstone(output_dir=output_dir)

            self.assertEqual(summary["harvest_files_processed"], 2)
            self.assertEqual(summary["wrangling_rows"], 3)
            self.assertEqual(summary["route_summary_rows"], 2)
            self.assertEqual(summary["mart_rows"], 2)
            self.assertEqual(summary["model_feature"], "route_risk_score")
            self.assertEqual(summary["lake_files_registered"], 1)

            expected_paths = [
                output_dir / "harvest" / "harvest.db",
                output_dir / "wrangling" / "cleaned_shipments.csv",
                output_dir / "reporting" / "logistics_kpi_report.md",
                output_dir / "warehouse" / "shipment_mart.db",
                output_dir / "ml" / "delay_rule.json",
                output_dir / "lake" / "manifests" / "shipments_2026-01-13.json",
                output_dir / "capstone_summary.json",
            ]

            for path in expected_paths:
                self.assertTrue(path.exists(), f"missing expected artifact: {path}")

            manifest = json.loads(
                (output_dir / "capstone_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["route_summary_rows"], 2)
            self.assertEqual(manifest["model_feature"], "route_risk_score")


if __name__ == "__main__":
    unittest.main()
