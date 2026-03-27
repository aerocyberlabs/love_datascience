from __future__ import annotations

import csv
from pathlib import Path


def load_grade_summary(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "grade": row["grade"],
                    "loan_count": int(row["loan_count"]),
                    "delinquent_loans": int(row["delinquent_loans"]),
                    "delinquency_rate": float(row["delinquency_rate"]),
                    "avg_debt_to_income": float(row["avg_debt_to_income"]),
                }
            )
    return rows


def build_finance_kpis(rows: list[dict[str, object]]) -> dict[str, object]:
    portfolio_loans = sum(int(row["loan_count"]) for row in rows)
    delinquent_loans = sum(int(row["delinquent_loans"]) for row in rows)
    portfolio_delinquency_rate = round(
        delinquent_loans / portfolio_loans if portfolio_loans else 0.0, 3
    )
    highest_risk_grade = max(rows, key=lambda row: float(row["delinquency_rate"]))["grade"]
    highest_dti_grade = max(rows, key=lambda row: float(row["avg_debt_to_income"]))["grade"]
    return {
        "portfolio_loans": portfolio_loans,
        "portfolio_delinquency_rate": portfolio_delinquency_rate,
        "highest_risk_grade": highest_risk_grade,
        "highest_dti_grade": highest_dti_grade,
    }


def render_markdown_report(
    kpis: dict[str, object], rows: list[dict[str, object]]
) -> str:
    lines = [
        "# Finance Performance Dashboard Prototype",
        "",
        "## Snapshot",
        "",
        f"- Portfolio loans: {kpis['portfolio_loans']}",
        f"- Portfolio delinquency rate: {kpis['portfolio_delinquency_rate']}",
        f"- Highest risk grade: {kpis['highest_risk_grade']}",
        f"- Highest debt-to-income grade: {kpis['highest_dti_grade']}",
        "",
        "## Grade Summary",
        "",
        "| Grade | Loans | Delinquent Loans | Delinquency Rate | Avg Debt-to-Income |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for row in rows:
        lines.append(
            "| "
            f"{row['grade']} | "
            f"{row['loan_count']} | "
            f"{row['delinquent_loans']} | "
            f"{row['delinquency_rate']} | "
            f"{row['avg_debt_to_income']} |"
        )

    return "\n".join(lines) + "\n"

