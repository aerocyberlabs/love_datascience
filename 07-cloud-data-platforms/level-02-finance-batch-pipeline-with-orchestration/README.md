# CLOUD-02: Finance Batch Pipeline with Orchestration

Level: `level-02`

Dependency type: `pipeline-linked`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Finance teams often move batch datasets through raw, staging, and mart layers under scheduled orchestration. This project models that workflow locally by registering a batch run, laying out raw and staging keys, and writing a run manifest that points to the mart target.

## Learning Outcomes

- model a finance batch pipeline lifecycle
- separate raw, staging, and mart targets
- track pipeline metadata in a run manifest
- prepare for real orchestration tools and cloud storage later

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.finance_pipeline.cli sample_source finance_pipeline loan_grade_summary 2026-02-10
```

