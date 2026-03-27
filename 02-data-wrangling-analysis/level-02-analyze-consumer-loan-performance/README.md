# WRAN-02: Analyze Consumer Loan Performance

Level: `level-02`

Dependency type: `standalone`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Loan performance datasets often arrive with inconsistent categorical values and raw numeric fields that are hard to use directly in analysis. This project cleans consumer loan records, derives debt-to-income and delinquency indicators, and summarizes risk by loan grade.

## Learning Outcomes

- normalize finance-oriented tabular data
- derive risk features such as debt-to-income
- turn row-level loan data into grade-level performance summaries
- prepare the finance path for downstream reporting and modeling work

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.loan_analysis.cli data/consumer_loans.csv outputs
```

