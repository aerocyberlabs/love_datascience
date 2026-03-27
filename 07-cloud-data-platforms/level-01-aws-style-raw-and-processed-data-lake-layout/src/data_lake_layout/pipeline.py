from __future__ import annotations

import json
import shutil
from pathlib import Path


def build_data_lake_layout(
    source_dir: Path,
    target_dir: Path,
    dataset_name: str,
    ingest_date: str,
) -> dict[str, object]:
    raw_partition = target_dir / "raw" / dataset_name / f"ingest_date={ingest_date}"
    processed_partition = (
        target_dir / "processed" / dataset_name / f"ingest_date={ingest_date}"
    )
    manifests_dir = target_dir / "manifests"

    raw_partition.mkdir(parents=True, exist_ok=True)
    processed_partition.mkdir(parents=True, exist_ok=True)
    manifests_dir.mkdir(parents=True, exist_ok=True)

    raw_keys: list[str] = []
    for source_file in sorted(source_dir.glob("*")):
        if source_file.is_file():
            destination = raw_partition / source_file.name
            shutil.copy2(source_file, destination)
            raw_keys.append(
                f"raw/{dataset_name}/ingest_date={ingest_date}/{source_file.name}"
            )

    processed_key = (
        f"processed/{dataset_name}/ingest_date={ingest_date}/{dataset_name}.parquet"
    )
    manifest = {
        "dataset_name": dataset_name,
        "ingest_date": ingest_date,
        "raw_keys": raw_keys,
        "processed_key": processed_key,
    }
    manifest_path = manifests_dir / f"{dataset_name}_{ingest_date}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {"files_registered": len(raw_keys), "manifest_path": str(manifest_path)}

