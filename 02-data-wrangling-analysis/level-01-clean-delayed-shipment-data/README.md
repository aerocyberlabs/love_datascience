# WRAN-01: Clean Delayed Shipment Data

Level: `level-01`

Dependency type: `recommended predecessor`

Dataset type: `hybrid`

Industry: supply chain / logistics

## Problem Statement

Operations teams often get shipment extracts with inconsistent casing, extra whitespace, and mixed delivery states. Before anyone can trust reporting or train a model, the shipment records need to be cleaned into a consistent analytical table with derived delay metrics.

This project turns messy shipment rows into a route-level operations summary. It can run on its own with the bundled CSV file, or it can be adapted to consume output from `HARV-01`.

## Learning Outcomes

- normalize categorical values
- trim and standardize identifiers
- derive route and delay metrics
- aggregate route-level KPIs
- use both Python and SQL in a simple wrangling workflow

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.shipment_wrangling.cli data/raw/messy_shipments.csv outputs
```

## Suggested Upstream Link

If you completed `HARV-01`, point this project at a CSV export of the latest shipment table or adapt the pipeline to read from SQLite directly.

## Deliverables

- cleaned shipment dataset
- route-level summary dataset
- starter SQL checks for late-shipment analysis

