# Project Template

Use this structure for new projects so the curriculum remains consistent.

## Required Sections

### 1. Project Summary

- project title
- domain
- difficulty level
- dependency type: `standalone`, `recommended predecessor`, or `pipeline-linked`
- dataset type: `public`, `synthetic`, or `hybrid`

### 2. Problem Statement

Explain the real-world problem in one short paragraph.

### 3. Learning Outcomes

List the key technical and analytical skills the learner should gain.

### 4. Tools and Stack

Identify the main tools used, including Python libraries, SQL engines, Docker services, and optional AWS components.

### 5. Repo Layout

Suggested shape:

```text
project-name/
  README.md
  configs/
  data/
    raw/
    interim/
    processed/
  notebooks/
  sql/
  src/
  tests/
  docker/
```

### 6. Execution Paths

Document both:

- local-first path
- Docker path

If applicable, also add:

- optional AWS extension

### 7. Deliverables

Examples:

- cleaned dataset
- analytical report
- feature set
- trained model
- dashboard
- transformed warehouse tables

### 8. Production Upgrade Ideas

List practical next steps such as:

- tests
- logging
- retries
- orchestration
- deployment
- CI
- monitoring

