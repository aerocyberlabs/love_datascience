# VIZ-01: Logistics KPI Notebook Report

Level: `level-01`

Dependency type: `recommended predecessor`

Dataset type: `hybrid`

Industry: supply chain / logistics

## Problem Statement

An operations manager needs a compact daily report showing overall shipment volume, how many shipments were late, and which routes are carrying the most weight or showing the worst lateness. This project turns route-level wrangling output into a reproducible Markdown report that can later become a notebook, dashboard, or scheduled report.

The intended upstream dependency is `WRAN-01`, but the project also includes a sample route summary file so learners can run it independently.

## Learning Outcomes

- consume downstream outputs from a previous project
- compute operational KPI snapshots
- turn summary data into a stakeholder-facing report
- establish a bridge from analysis outputs to reporting artifacts

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.logistics_reporting.cli data/route_summary_sample.csv reports
```

## Deliverables

- parsed route summary data
- KPI snapshot
- Markdown report for logistics stakeholders

