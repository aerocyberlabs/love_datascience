# WH-02: Model a Finance Risk Warehouse

Level: `level-02`

Dependency type: `recommended predecessor`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Risk and portfolio teams need a warehouse layer that separates cleaned loan records from reusable analytical marts. This project loads cleaned loans into a grade dimension, a loan fact table, and a grade-level risk mart.

## Learning Outcomes

- model a small finance warehouse
- separate dimensions, facts, and marts
- materialize grade-level delinquency and debt-to-income metrics
- prepare the finance path for cloud and capstone work later

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.finance_warehouse.cli data/cleaned_loans_sample.csv finance_warehouse.db
```

