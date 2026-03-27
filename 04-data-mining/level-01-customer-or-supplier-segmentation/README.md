# MINE-01: Customer or Supplier Segmentation

Level: `level-01`

Dependency type: `standalone`

Dataset type: `synthetic`

Industry: supply chain / logistics

## Problem Statement

Operations teams often need a fast way to group suppliers into meaningful buckets before they get to more formal clustering methods. This first mining project uses simple, transparent segmentation rules to categorize suppliers by reliability and shipping volume.

The emphasis is on the data mining mindset:

- identify useful variables
- discover operationally meaningful groups
- summarize the groups for decision-making

## Learning Outcomes

- load and profile supplier metrics
- assign segment labels from business-oriented rules
- summarize discovered groups
- prepare for later clustering and anomaly-detection projects

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.supplier_segmentation.cli data/supplier_metrics.csv outputs
```

