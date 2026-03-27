# CAP-02: Finance Risk Monitoring Platform

Level: `level-02`

Dependency type: `pipeline-linked`

Dataset type: `hybrid`

Industry: finance

## Problem Statement

This capstone connects the finance projects into a single local-first workflow. It simulates a risk monitoring platform by running the finance harvester, wrangling logic, reporting, warehouse build, model training, and cloud-style batch manifesting in sequence.

The goal is not infrastructure realism yet. The goal is to prove that the finance path forms a coherent end-to-end system in the repository.

## Learning Outcomes

- connect multiple finance projects into one workflow
- understand how analytics and modeling artifacts relate across stages
- emit a final run summary that can serve as orchestration metadata

## Local Run

```bash
python -m unittest discover -s tests -v
python -m src.finance_capstone.cli finance_capstone_outputs
```

