from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def clean_loans(csv_path: Path) -> list[dict[str, object]]:
    cleaned_rows: list[dict[str, object]] = []

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            loan_id = row["loan_id"].strip().upper()
            grade = row["grade"].strip().upper()
            annual_income = float(row["annual_income"])
            debt = float(row["debt"])
            days_past_due = int(row["days_past_due"])
            loan_amount = float(row["loan_amount"])
            debt_to_income = round(debt / annual_income, 3)
            is_delinquent = 1 if days_past_due >= 30 else 0
            dti_band = _band_debt_to_income(debt_to_income)

            cleaned_rows.append(
                {
                    "loan_id": loan_id,
                    "grade": grade,
                    "annual_income": annual_income,
                    "debt": debt,
                    "days_past_due": days_past_due,
                    "loan_amount": loan_amount,
                    "debt_to_income": debt_to_income,
                    "is_delinquent": is_delinquent,
                    "dti_band": dti_band,
                }
            )

    return cleaned_rows


def summarize_by_grade(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "loan_count": 0.0,
            "delinquent_loans": 0.0,
            "debt_to_income_total": 0.0,
        }
    )

    for row in rows:
        grade = str(row["grade"])
        grouped[grade]["loan_count"] += 1
        grouped[grade]["delinquent_loans"] += float(row["is_delinquent"])
        grouped[grade]["debt_to_income_total"] += float(row["debt_to_income"])

    summary: list[dict[str, object]] = []
    for grade in sorted(grouped):
        loan_count = int(grouped[grade]["loan_count"])
        delinquent_loans = int(grouped[grade]["delinquent_loans"])
        summary.append(
            {
                "grade": grade,
                "loan_count": loan_count,
                "delinquent_loans": delinquent_loans,
                "delinquency_rate": delinquent_loans / loan_count if loan_count else 0.0,
                "avg_debt_to_income": grouped[grade]["debt_to_income_total"] / loan_count
                if loan_count
                else 0.0,
            }
        )

    return summary


def _band_debt_to_income(debt_to_income: float) -> str:
    if debt_to_income < 0.2:
        return "low"
    if debt_to_income <= 0.35:
        return "moderate"
    return "high"

