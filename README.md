# love_datascience

Hands-on data science with Python, organized by domain and increasing difficulty.

This repository is designed as a self-study curriculum for learners who already have some Python familiarity and want to build practical depth across modern data work. The structure is hybrid by design:

- concept-first enough to learn systematically
- project-first enough to feel like real work
- local-first enough to run on a laptop
- modern-stack enough to map to current team environments

The curriculum treats Python and SQL as first-class skills throughout. Many projects include:

- notebooks for exploration and explanation
- reusable Python modules and scripts
- SQL transformations and analysis
- lightweight Docker from the beginning
- optional AWS extensions for cloud-oriented practice

## Learning Goals

The repo is built to support three goals at once:

- learn core data science and analytics concepts in a structured order
- build credible hands-on projects across realistic domains
- grow toward production-style workflows without requiring cloud complexity on day one

## Curriculum Map

| Domain | Focus | Status |
| --- | --- | --- |
| `00-python-refresh` | Quick Python and tooling refresher for rusty learners | scaffolded |
| `00-sql-refresh` | SQL refresher for learners who need a ramp before the main path | scaffolded |
| `01-data-harvesting` | files, APIs, scraping, ingestion reliability | scaffolded |
| `02-data-wrangling-analysis` | cleaning, joins, missing data, business analysis | scaffolded |
| `03-data-visualization-reporting` | charts, KPI reporting, narrative analysis, dashboards | scaffolded |
| `04-data-mining` | clustering, association rules, anomaly detection, text mining | scaffolded |
| `05-data-warehousing` | dimensional modeling, marts, dbt-style transformation thinking | scaffolded |
| `06-machine-learning` | regression, classification, pipelines, evaluation, experiment discipline | scaffolded |
| `07-cloud-data-platforms` | AWS-oriented storage, orchestration, warehouse patterns | scaffolded |
| `08-capstones` | end-to-end multi-domain projects | scaffolded |

The first version of the project registry lives in [docs/project-registry.md](docs/project-registry.md).

## Design Principles

- organize by domain, with increasing difficulty inside each domain
- keep many projects standalone, but link selected projects into larger pipelines
- use public datasets when possible and synthetic datasets when structure matters more
- teach Docker early, but do not make it the only path
- require SQL regularly, not only in warehousing sections
- keep AWS as the primary cloud target without making cloud spend mandatory

## Repo Standards

Each project should eventually follow the same shape:

- `README.md`: problem, skills, tools, expected outcomes, stretch goals
- `notebooks/`: guided analysis and walkthroughs
- `src/`: reusable Python code and scripts
- `sql/`: analysis queries, transformations, marts, or models
- `tests/`: data and logic checks
- `configs/`: tunable settings and environment-aware parameters
- `docker-compose.yml` or `docker/`: when services are involved

Each project should also identify its dependency type:

- `standalone`
- `recommended predecessor`
- `pipeline-linked`

## Recommended Stack

The base stack for the curriculum is intentionally modern but still approachable:

- Python
- SQL
- pandas
- DuckDB
- Postgres
- Jupyter
- matplotlib / seaborn / plotly
- scikit-learn
- dbt concepts and SQL transformation patterns
- Prefect or similar orchestration patterns later in the path
- Docker Compose
- AWS-oriented extensions where they add practical value

## Suggested Use

If you want a guided path:

1. Start with the refreshers only if you need them.
2. Pick a domain that matches your goal.
3. Complete projects in difficulty order inside that domain.
4. Revisit linked downstream projects to see how outputs feed later workflows.
5. Finish with one or two capstones that combine harvesting, warehousing, reporting, and ML.

If you want a portfolio path later, use the same projects and add:

- cleaner visual polish
- stronger business framing
- more explicit metrics and outcomes
- CI, tests, packaging, deployment, and cloud variants

## Current State

This repository currently contains:

- the curriculum scaffold
- the first design document
- a draft project registry
- domain-level placeholders that will become concrete projects

The next step is to populate the first project in each domain and establish the shared project template in practice.

