# ML-01: Predict Shipment Delay Risk

Level: `level-01`

Dependency type: `recommended predecessor`

Dataset type: `synthetic`

Industry: supply chain / logistics

## Problem Statement

Operations teams want an early risk signal before a shipment is officially marked late. This project trains a simple rule-based classifier on shipment features and evaluates how well it predicts `is_late`.

The goal is not model sophistication yet. The goal is to teach the end-to-end machine learning workflow with a minimal implementation that learners can inspect directly:

- load training data
- choose a predictive feature and threshold
- evaluate the resulting classifier
- inspect the resulting predictions

## Learning Outcomes

- frame a binary classification problem
- separate features from target labels
- evaluate accuracy on a small labeled dataset
- understand why feature choice matters

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.delay_risk.cli data/training_shipments.csv
```

