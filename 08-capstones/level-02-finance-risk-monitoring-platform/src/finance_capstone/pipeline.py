from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path


CAPSTONE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = CAPSTONE_ROOT.parents[1]


def run_finance_capstone(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    harvest_pipeline = _load_module(
        "finance_harvest_pipeline",
        REPO_ROOT
        / "01-data-harvesting"
        / "level-02-build-a-finance-market-data-api-harvester"
        / "src"
        / "market_harvest"
        / "pipeline.py",
    )
    wrangling_pipeline = _load_module(
        "finance_wrangling_pipeline",
        REPO_ROOT
        / "02-data-wrangling-analysis"
        / "level-02-analyze-consumer-loan-performance"
        / "src"
        / "loan_analysis"
        / "pipeline.py",
    )
    reporting_pipeline = _load_module(
        "finance_reporting_pipeline",
        REPO_ROOT
        / "03-data-visualization-reporting"
        / "level-02-finance-performance-dashboard-prototype"
        / "src"
        / "finance_reporting"
        / "pipeline.py",
    )
    warehouse_pipeline = _load_module(
        "finance_warehouse_pipeline",
        REPO_ROOT
        / "05-data-warehousing"
        / "level-02-model-a-finance-risk-warehouse"
        / "src"
        / "finance_warehouse"
        / "pipeline.py",
    )
    ml_pipeline = _load_module(
        "finance_ml_pipeline",
        REPO_ROOT
        / "06-machine-learning"
        / "level-02-credit-default-prediction-pipeline"
        / "src"
        / "credit_default"
        / "pipeline.py",
    )
    cloud_pipeline = _load_module(
        "finance_cloud_pipeline",
        REPO_ROOT
        / "07-cloud-data-platforms"
        / "level-02-finance-batch-pipeline-with-orchestration"
        / "src"
        / "finance_pipeline"
        / "pipeline.py",
    )

    harvest_output = output_dir / "harvest"
    wrangling_output = output_dir / "wrangling"
    reporting_output = output_dir / "reporting"
    warehouse_output = output_dir / "warehouse"
    ml_output = output_dir / "ml"
    cloud_output = output_dir / "cloud"

    for directory in [
        harvest_output,
        wrangling_output,
        reporting_output,
        warehouse_output,
        ml_output,
    ]:
        directory.mkdir(exist_ok=True)

    harvest_summary = harvest_pipeline.harvest_market_pages(
        fixture_dir=REPO_ROOT
        / "01-data-harvesting"
        / "level-02-build-a-finance-market-data-api-harvester"
        / "fixtures",
        first_page="page_1.json",
        db_path=harvest_output / "market.db",
    )

    cleaned_rows = wrangling_pipeline.clean_loans(
        REPO_ROOT
        / "02-data-wrangling-analysis"
        / "level-02-analyze-consumer-loan-performance"
        / "data"
        / "consumer_loans.csv"
    )
    grade_summary = wrangling_pipeline.summarize_by_grade(cleaned_rows)
    cleaned_path = wrangling_output / "cleaned_loans.csv"
    grade_summary_path = wrangling_output / "loan_grade_summary.csv"
    _write_csv(cleaned_path, cleaned_rows)
    _write_csv(grade_summary_path, grade_summary)

    loaded_grade_summary = reporting_pipeline.load_grade_summary(grade_summary_path)
    kpis = reporting_pipeline.build_finance_kpis(loaded_grade_summary)
    report = reporting_pipeline.render_markdown_report(kpis, loaded_grade_summary)
    (reporting_output / "finance_dashboard_report.md").write_text(
        report, encoding="utf-8"
    )

    warehouse_summary = warehouse_pipeline.build_finance_risk_warehouse(
        cleaned_path=cleaned_path,
        db_path=warehouse_output / "finance_warehouse.db",
    )

    training_rows = ml_pipeline.load_credit_rows(
        REPO_ROOT
        / "06-machine-learning"
        / "level-02-credit-default-prediction-pipeline"
        / "data"
        / "credit_default_training.csv"
    )
    rule = ml_pipeline.train_default_rule(training_rows)
    metrics = ml_pipeline.evaluate_default_rule(rule, training_rows)
    (ml_output / "default_rule.json").write_text(
        json.dumps({"rule": rule, "metrics": metrics}, indent=2),
        encoding="utf-8",
    )

    cloud_summary = cloud_pipeline.build_finance_batch_pipeline(
        source_dir=REPO_ROOT
        / "07-cloud-data-platforms"
        / "level-02-finance-batch-pipeline-with-orchestration"
        / "sample_source",
        pipeline_dir=cloud_output,
        dataset_name="loan_grade_summary",
        run_date="2026-02-10",
    )

    summary = {
        "harvest_pages_processed": harvest_summary.pages_processed,
        "wrangling_rows": len(cleaned_rows),
        "grade_summary_rows": len(grade_summary),
        "warehouse_mart_rows": warehouse_summary.mart_rows,
        "model_feature": rule["feature"],
        "model_accuracy": metrics["accuracy"],
        "pipeline_files_registered": cloud_summary["files_registered"],
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

