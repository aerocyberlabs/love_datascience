# HARV-01: Ingest Logistics Shipment Files

Level: `level-01`

Dependency type: `standalone`

Dataset type: `synthetic`

Industry: supply chain / logistics

## Problem Statement

A logistics operations team receives shipment status files from multiple carriers. The files arrive as CSV extracts with the same schema, but the same shipment can appear in more than one file as its status changes over time. The goal is to ingest the raw files, validate the schema, and build a clean table that keeps the latest status for each shipment.

This project introduces the first harvesting workflow in the repo:

- read multiple raw files from a directory
- validate the expected schema
- load records into a local SQLite warehouse
- deduplicate shipments by latest `event_ts`
- run simple SQL quality checks after ingestion

## Learning Outcomes

- file-based ingestion patterns
- schema validation
- local warehouse loading with SQLite
- upsert logic for slowly changing shipment status
- local-first execution plus a Docker path

## Project Layout

```text
level-01-ingest-logistics-shipment-files/
  README.md
  configs/
  data/
    raw/
  notebooks/
  sql/
  src/
    shipment_ingest/
  tests/
```

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.shipment_ingest.cli data/raw shipments.db
```

## Docker Run

This project includes a lightweight Docker path for a Postgres-backed practice environment. The first implementation uses SQLite locally so the ingestion logic stays simple, but the compose file sets the direction for later projects.

```bash
docker compose up -d
```

## Deliverables

- a validated shipment table in SQLite
- reproducible tests for the ingest behavior
- sample raw files for local experimentation
- starter SQL quality checks

## Production Upgrade Ideas

- add structured logging
- add manifest files and file hashes
- capture rejected rows separately
- load into Postgres as an alternate sink
- schedule ingestion with Prefect in a later project

