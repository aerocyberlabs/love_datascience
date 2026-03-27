from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_lake_layout.pipeline import build_data_lake_layout  # noqa: E402


class DataLakeLayoutTests(unittest.TestCase):
    def test_build_data_lake_layout_creates_manifest_and_expected_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            source_dir = base / "source"
            source_dir.mkdir()
            (source_dir / "shipments_2026-01-13.csv").write_text(
                "shipment_id,weight_kg\nSHP-100,10.5\n",
                encoding="utf-8",
            )

            target_dir = base / "lake"

            summary = build_data_lake_layout(
                source_dir=source_dir,
                target_dir=target_dir,
                dataset_name="shipments",
                ingest_date="2026-01-13",
            )

            self.assertEqual(summary["files_registered"], 1)

            manifest_path = target_dir / "manifests" / "shipments_2026-01-13.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertEqual(
                manifest["raw_keys"],
                ["raw/shipments/ingest_date=2026-01-13/shipments_2026-01-13.csv"],
            )
            self.assertEqual(
                manifest["processed_key"],
                "processed/shipments/ingest_date=2026-01-13/shipments.parquet",
            )


if __name__ == "__main__":
    unittest.main()
