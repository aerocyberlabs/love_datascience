# WH-01: Build a Shipment Analytics Mart

Level: `level-01`

Dependency type: `pipeline-linked`

Dataset type: `hybrid`

Industry: supply chain / logistics

## Problem Statement

Analysts and operators need a reliable warehouse layer instead of repeatedly recomputing metrics from raw or semi-clean data. This project takes cleaned shipment records and loads them into a small dimensional model with a route dimension, a shipment fact table, and a route KPI mart.

It is designed to follow `WRAN-01`, but it also ships with a sample cleaned dataset so learners can run it independently.

## Learning Outcomes

- move from cleaned files into dimensional warehouse tables
- separate dimensions, facts, and marts
- materialize route-level KPI outputs in SQL-friendly form
- establish a bridge from wrangling to warehousing

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.shipment_mart.cli data/cleaned_shipments_sample.csv shipment_mart.db
```

## Deliverables

- `dim_route`
- `fact_shipments`
- `mart_route_kpis`

