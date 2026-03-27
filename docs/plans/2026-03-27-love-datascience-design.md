# love_datascience Design

Date: 2026-03-27

## Overview

`love_datascience` is a hybrid self-study curriculum for hands-on data science using Python. It is not meant to be a notebook dump and it is not meant to be a purely production-oriented template repository. The design goal is to combine structured progression with realistic project conventions.

The repository is organized by domain, and difficulty increases within each domain. Learners should be able to:

- study one domain deeply without being forced through the entire repo
- follow linked projects when they want fuller system context
- develop Python and SQL together
- work locally first and then extend selected projects into AWS-oriented workflows

## Educational Positioning

The primary audience is self-study learners who already have some Python familiarity. Python is treated as a prerequisite with a refresher layer rather than a full beginner course. SQL is treated as a first-class skill and appears throughout the curriculum.

The repository is optimized first for learning depth and hands-on repetition. Recruiter-facing polish can be layered on later, but the initial design favors:

- clarity of project purpose
- reusable structure
- concept progression
- realistic tooling
- modest operational discipline from the beginning

## Curriculum Structure

The top-level curriculum is:

- `00-python-refresh`
- `00-sql-refresh`
- `01-data-harvesting`
- `02-data-wrangling-analysis`
- `03-data-visualization-reporting`
- `04-data-mining`
- `05-data-warehousing`
- `06-machine-learning`
- `07-cloud-data-platforms`
- `08-capstones`

Each domain should contain progressively harder projects, typically `level-01` through `level-03`, with optional `level-04` work where a domain benefits from a heavier end-to-end project.

## Project Design Rules

Every project should eventually expose the same learning contract:

- a concrete problem statement
- domain and difficulty labels
- datasets or sources clearly labeled as public, synthetic, or hybrid
- notebooks for guided exploration
- scripts and modules for reusable execution
- SQL assets where relevant
- tests or validation checks
- optional Docker path
- optional AWS extension
- optional production upgrade path

Projects should be labeled as one of:

- `standalone`
- `recommended predecessor`
- `pipeline-linked`

This keeps the repo flexible while still rewarding learners who follow project chains.

## Domain Emphasis

The primary industry lenses are:

1. supply chain / operations / logistics
2. finance
3. healthcare / public health

Other industries may appear occasionally where they better fit a domain, but these three should anchor most examples.

## Tooling Philosophy

The stack should feel modern without becoming infrastructure-heavy too early. The intended progression is:

- local analysis with Python, pandas, and SQL
- lightweight storage with DuckDB and Postgres
- Docker from the beginning as a second execution path
- warehousing and transformation patterns later
- orchestration and AWS-oriented workflows later still

Spark and heavier cloud tooling should be used where they add conceptual value, not as defaults.

## Dataset Philosophy

The curriculum should mix:

- public datasets for realism and sourcing discipline
- synthetic datasets for warehouse design, repeatable business workflows, and controlled scenarios

Synthetic data is especially useful for:

- multi-table operational systems
- dimensional models
- event pipelines
- KPI reporting and dashboarding

## Next Implementation Phase

The first implementation milestone is:

- scaffold the repository
- create the project registry
- add shared project conventions
- implement one concrete project in each major domain

Later milestones can expand level coverage, capstones, recruiter polish, and cloud-heavy variants.

