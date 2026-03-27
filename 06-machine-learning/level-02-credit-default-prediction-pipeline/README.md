# ML-02: Credit Default Prediction Pipeline

Level: `level-02`

Dependency type: `recommended predecessor`

Dataset type: `synthetic`

Industry: finance

## Problem Statement

Risk teams want an interpretable way to flag loans likely to default. This project trains a simple threshold-based default rule on finance features and evaluates it with basic classification metrics.

The point is to make the modeling process easy to inspect:

- load labeled credit data
- test candidate threshold rules
- pick the best rule by accuracy
- report accuracy, precision, and recall

## Learning Outcomes

- frame default prediction as binary classification
- compare candidate predictive features
- understand threshold-based decision rules
- report multiple evaluation metrics, not just accuracy

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.credit_default.cli data/credit_default_training.csv
```

