from __future__ import annotations

import json
import shutil
from pathlib import Path


def build_finance_batch_pipeline(
    source_dir: Path,
    pipeline_dir: Path,
    dataset_name: str,
    run_date: str,
) -> dict[str, object]:
    raw_partition = (
        pipeline_dir / "raw" / "finance" / dataset_name / f"run_date={run_date}"
    )
    staging_partition = (
        pipeline_dir / "staging" / "finance" / dataset_name / f"run_date={run_date}"
    )
    runs_dir = pipeline_dir / "runs"

    raw_partition.mkdir(parents=True, exist_ok=True)
    staging_partition.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)

    raw_keys: list[str] = []
    for source_file in sorted(source_dir.glob("*")):
        if source_file.is_file():
            destination = raw_partition / source_file.name
            shutil.copy2(source_file, destination)
            raw_keys.append(
                f"raw/finance/{dataset_name}/run_date={run_date}/{source_file.name}"
            )

    staging_key = (
        f"staging/finance/{dataset_name}/run_date={run_date}/{dataset_name}.parquet"
    )
    mart_target = f"mart/finance/{dataset_name}"

    manifest = {
        "job_name": "finance-batch-pipeline",
        "run_date": run_date,
        "dataset_name": dataset_name,
        "raw_keys": raw_keys,
        "staging_key": staging_key,
        "mart_target": mart_target,
    }
    manifest_path = runs_dir / f"{dataset_name}_{run_date}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "job_name": "finance-batch-pipeline",
        "files_registered": len(raw_keys),
        "manifest_path": str(manifest_path),
    }

