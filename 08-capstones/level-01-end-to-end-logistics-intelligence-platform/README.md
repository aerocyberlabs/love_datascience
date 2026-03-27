# CAP-01: End-to-End Logistics Intelligence Platform

Level: `level-01`

Dependency type: `pipeline-linked`

Dataset type: `hybrid`

Industry: supply chain / logistics

## Problem Statement

This capstone ties together the first logistics projects in the repo into a single runnable workflow. It is meant to show learners how the pieces relate in practice:

- harvesting raw shipment extracts
- wrangling operational records into clean analytical data
- producing a stakeholder-facing KPI report
- loading an analytics mart
- training a simple delay-risk model
- organizing a local AWS-style lake layout

The capstone is still local-first, but its structure mirrors the way a small production analytics workflow is often broken into stages.

## Learning Outcomes

- connect projects instead of treating them as isolated exercises
- understand where each artifact belongs in a larger workflow
- produce a final summary manifest across multiple pipeline stages

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.logistics_capstone.cli capstone_outputs
```

