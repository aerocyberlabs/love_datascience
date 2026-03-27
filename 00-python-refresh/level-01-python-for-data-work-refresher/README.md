# PY-01: Python for Data Work Refresher

Level: `level-01`

Dependency type: `standalone`

Dataset type: `synthetic`

## Problem Statement

This refresher is for learners who know some Python already but need a short ramp back into the mechanics used across the main curriculum. It covers:

- reading CSV files
- normalizing strings and numeric values
- working with lists of dictionaries
- computing simple summary statistics
- writing a small text report

## Learning Outcomes

- use `pathlib`, `csv`, and basic Python data structures
- practice list and set operations on tabular rows
- compute simple summary metrics without pandas first
- prepare for the more involved workflows in the main projects

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.python_refresh.cli data/shipments.csv summary.txt
```

