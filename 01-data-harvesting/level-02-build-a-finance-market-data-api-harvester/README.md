# HARV-02: Build a Finance Market Data API Harvester

Level: `level-02`

Dependency type: `standalone`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Finance data teams often need to ingest paginated market data feeds, validate the records, and load them into a durable store for downstream analysis. This project simulates that workflow locally with JSON fixtures that behave like a paginated API.

The first version focuses on:

- following pagination links
- validating record schema
- loading price data into SQLite
- preserving a realistic harvester structure before adding real HTTP calls later

## Learning Outcomes

- understand paginated API ingestion
- validate record shape before loading
- store time-series market data in a relational table
- prepare for retries, rate limiting, and live APIs in later work

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.market_harvest.cli fixtures page_1.json market.db
```

