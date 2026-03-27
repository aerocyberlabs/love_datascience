from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path


CAPSTONE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = CAPSTONE_ROOT.parents[1]


def run_logistics_capstone(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    harvest_pipeline = _load_module(
        "harvest_pipeline",
        REPO_ROOT
        / "01-data-harvesting"
        / "level-01-ingest-logistics-shipment-files"
        / "src"
        / "shipment_ingest"
        / "pipeline.py",
    )
    wrangling_pipeline = _load_module(
        "wrangling_pipeline",
        REPO_ROOT
        / "02-data-wrangling-analysis"
        / "level-01-clean-delayed-shipment-data"
        / "src"
        / "shipment_wrangling"
        / "pipeline.py",
    )
    reporting_pipeline = _load_module(
        "reporting_pipeline",
        REPO_ROOT
        / "03-data-visualization-reporting"
        / "level-01-logistics-kpi-notebook-report"
        / "src"
        / "logistics_reporting"
        / "pipeline.py",
    )
    mart_pipeline = _load_module(
        "mart_pipeline",
        REPO_ROOT
        / "05-data-warehousing"
        / "level-01-build-a-shipment-analytics-mart"
        / "src"
        / "shipment_mart"
        / "pipeline.py",
    )
    ml_pipeline = _load_module(
        "ml_pipeline",
        REPO_ROOT
        / "06-machine-learning"
        / "level-01-predict-shipment-delay-risk"
        / "src"
        / "delay_risk"
        / "pipeline.py",
    )
    lake_pipeline = _load_module(
        "lake_pipeline",
        REPO_ROOT
        / "07-cloud-data-platforms"
        / "level-01-aws-style-raw-and-processed-data-lake-layout"
        / "src"
        / "data_lake_layout"
        / "pipeline.py",
    )

    harvest_output = output_dir / "harvest"
    wrangling_output = output_dir / "wrangling"
    reporting_output = output_dir / "reporting"
    warehouse_output = output_dir / "warehouse"
    ml_output = output_dir / "ml"
    lake_output = output_dir / "lake"

    harvest_output.mkdir(exist_ok=True)
    wrangling_output.mkdir(exist_ok=True)
    reporting_output.mkdir(exist_ok=True)
    warehouse_output.mkdir(exist_ok=True)
    ml_output.mkdir(exist_ok=True)

    harvest_summary = harvest_pipeline.ingest_shipments(
        raw_dir=REPO_ROOT
        / "01-data-harvesting"
        / "level-01-ingest-logistics-shipment-files"
        / "data"
        / "raw",
        db_path=harvest_output / "harvest.db",
    )

    cleaned_rows = wrangling_pipeline.clean_shipments(
        REPO_ROOT
        / "02-data-wrangling-analysis"
        / "level-01-clean-delayed-shipment-data"
        / "data"
        / "raw"
        / "messy_shipments.csv"
    )
    route_summary = wrangling_pipeline.summarize_routes(cleaned_rows)
    cleaned_path = wrangling_output / "cleaned_shipments.csv"
    route_summary_path = wrangling_output / "route_summary.csv"
    _write_csv(cleaned_path, cleaned_rows)
    _write_csv(route_summary_path, route_summary)

    loaded_route_summary = reporting_pipeline.load_route_summary(route_summary_path)
    snapshot = reporting_pipeline.build_kpi_snapshot(loaded_route_summary)
    report = reporting_pipeline.render_markdown_report(snapshot, loaded_route_summary)
    (reporting_output / "logistics_kpi_report.md").write_text(report, encoding="utf-8")

    mart_summary = mart_pipeline.build_shipment_analytics_mart(
        cleaned_path=cleaned_path,
        db_path=warehouse_output / "shipment_mart.db",
    )

    training_rows = ml_pipeline.load_training_rows(
        REPO_ROOT
        / "06-machine-learning"
        / "level-01-predict-shipment-delay-risk"
        / "data"
        / "training_shipments.csv"
    )
    rule = ml_pipeline.train_delay_rule(training_rows)
    metrics = ml_pipeline.evaluate_threshold_rule(rule, training_rows)
    (ml_output / "delay_rule.json").write_text(
        json.dumps({"rule": rule, "metrics": metrics}, indent=2),
        encoding="utf-8",
    )

    lake_summary = lake_pipeline.build_data_lake_layout(
        source_dir=REPO_ROOT
        / "07-cloud-data-platforms"
        / "level-01-aws-style-raw-and-processed-data-lake-layout"
        / "sample_source",
        target_dir=lake_output,
        dataset_name="shipments",
        ingest_date="2026-01-13",
    )

    summary = {
        "harvest_files_processed": harvest_summary.files_processed,
        "wrangling_rows": len(cleaned_rows),
        "route_summary_rows": len(route_summary),
        "mart_rows": mart_summary.mart_rows,
        "model_feature": rule["feature"],
        "model_accuracy": metrics["accuracy"],
        "lake_files_registered": lake_summary["files_registered"],
    }
    (output_dir / "capstone_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
