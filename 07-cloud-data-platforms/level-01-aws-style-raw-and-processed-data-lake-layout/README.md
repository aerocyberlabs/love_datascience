# CLOUD-01: AWS-Style Raw and Processed Data Lake Layout

Level: `level-01`

Dependency type: `recommended predecessor`

Dataset type: `hybrid`

Industry: supply chain / logistics

## Problem Statement

Before teams stand up real cloud infrastructure, they still need to understand how object storage layouts, partitions, and manifests are organized. This project models an AWS-style lake layout locally so learners can practice raw-zone, processed-zone, and manifest conventions without needing an AWS account.

## Learning Outcomes

- model S3-style object keys locally
- separate raw and processed zones
- partition data by ingest date
- generate a manifest for downstream jobs

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.data_lake_layout.cli sample_source local_lake shipments 2026-01-13
```

