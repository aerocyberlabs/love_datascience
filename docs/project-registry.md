# Project Registry

This is the first-pass registry for version 1 of the curriculum. Project names can still change, but the progression and domain balance are the current working plan.

## Refreshers

| ID | Project | Domain | Difficulty | Industry | Type |
| --- | --- | --- | --- | --- | --- |
| `PY-01` | Python for Data Work Refresher | `00-python-refresh` | level-01 | neutral | standalone |
| `SQL-01` | SQL Refresher for Analysts and Data Scientists | `00-sql-refresh` | level-01 | neutral | standalone |

## Data Harvesting

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `HARV-01` | Ingest Logistics Shipment Files | level-01 | supply chain | standalone | public or synthetic flat files |
| `HARV-02` | Build a Finance Market Data API Harvester | level-02 | finance | standalone | pagination, retries, schema checks |
| `HARV-03` | Scrape a Practice Healthcare Directory | level-03 | healthcare | standalone | scrape-friendly site, respectful scraping patterns |

## Data Wrangling and Analysis

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `WRAN-01` | Clean Delayed Shipment Data | level-01 | supply chain | standalone | missing values, joins, type fixes |
| `WRAN-02` | Analyze Consumer Loan Performance | level-02 | finance | standalone | cohort and risk analysis |
| `WRAN-03` | Public Health Resource Access Analysis | level-03 | healthcare | standalone | multi-table joins and summary narratives |

## Data Visualization and Reporting

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `VIZ-01` | Logistics KPI Notebook Report | level-01 | supply chain | recommended predecessor | natural follow-up to `WRAN-01` |
| `VIZ-02` | Finance Performance Dashboard Prototype | level-02 | finance | standalone | static-first, interactive extension later |
| `VIZ-03` | Public Health Operations Storytelling Report | level-03 | healthcare | recommended predecessor | narrative notebook plus summary outputs |

## Data Mining

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `MINE-01` | Customer or Supplier Segmentation | level-01 | supply chain | standalone | clustering |
| `MINE-02` | Fraud-Like Pattern Discovery | level-02 | finance | standalone | anomaly detection |
| `MINE-03` | Clinical Text Theme Mining | level-03 | healthcare | standalone | text mining |

## Data Warehousing

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `WH-01` | Build a Shipment Analytics Mart | level-01 | supply chain | pipeline-linked | can consume `HARV-01` or `WRAN-01` outputs |
| `WH-02` | Model a Finance Risk Warehouse | level-02 | finance | standalone | star schema and marts |
| `WH-03` | Public Health Reporting Warehouse | level-03 | healthcare | standalone | dimensional design and quality checks |

## Machine Learning

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `ML-01` | Predict Shipment Delay Risk | level-01 | supply chain | recommended predecessor | regression or classification |
| `ML-02` | Credit Default Prediction Pipeline | level-02 | finance | standalone | preprocessing, evaluation, leakage prevention |
| `ML-03` | Hospital Readmission Risk Modeling | level-03 | healthcare | standalone | feature engineering and fairness discussion |

## Cloud Data Platforms

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `CLOUD-01` | AWS-Style Raw and Processed Data Lake Layout | level-01 | supply chain | recommended predecessor | local-first with S3-style extension |
| `CLOUD-02` | Finance Batch Pipeline with Orchestration | level-02 | finance | pipeline-linked | orchestration plus warehouse loading |
| `CLOUD-03` | Healthcare Reporting Pipeline on AWS Patterns | level-03 | healthcare | pipeline-linked | storage, transformation, reporting handoff |

## Capstones

| ID | Project | Difficulty | Industry | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `CAP-01` | End-to-End Logistics Intelligence Platform | level-04 | supply chain | pipeline-linked | harvesting to mart to reporting to ML |
| `CAP-02` | Finance Risk Monitoring Platform | level-04 | finance | pipeline-linked | ingestion, warehouse, BI, anomaly detection |

