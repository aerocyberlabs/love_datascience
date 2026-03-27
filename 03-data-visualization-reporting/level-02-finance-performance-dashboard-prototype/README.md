# VIZ-02: Finance Performance Dashboard Prototype

Level: `level-02`

Dependency type: `recommended predecessor`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Portfolio and risk teams need a compact view of loan quality across grades. This project turns a grade-level loan performance summary into a reproducible dashboard-style report with core KPIs and a simple grade table.

## Learning Outcomes

- load summarized finance metrics
- compute portfolio-level KPIs
- identify the riskiest credit grade
- render a compact reporting artifact suitable for later dashboard work

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.finance_reporting.cli data/loan_grade_summary.csv reports
```

