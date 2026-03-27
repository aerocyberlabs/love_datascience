# SQL-01: SQL Refresher for Analysts and Data Scientists

Level: `level-01`

Dependency type: `standalone`

Dataset type: `synthetic`

Industry: supply chain / logistics

## Problem Statement

This refresher gives learners a compact SQL baseline before they move into wrangling, warehousing, and analytics projects. The project seeds a small logistics dataset into SQLite and includes query files that practice filtering, aggregation, and window functions.

## Learning Outcomes

- build and inspect tables in SQLite
- write grouped route-level metrics
- use window functions for ranking
- connect SQL refresh practice to later logistics projects

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.sql_refresh.setup sql_refresh.db
```

Then run the SQL in any SQLite client or use the helper functions from `src/sql_refresh/setup.py`.

