from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FinanceWarehouseSummary:
    grades_loaded: int
    loans_loaded: int
    mart_rows: int


def build_finance_risk_warehouse(
    cleaned_path: Path,
    db_path: Path,
) -> FinanceWarehouseSummary:
    rows = _load_cleaned_rows(cleaned_path)
    grades = sorted({row["grade"] for row in rows})
    grade_keys = {grade: index for index, grade in enumerate(grades, start=1)}

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        _create_schema(connection)
        connection.executemany(
            "INSERT INTO dim_grade (grade_key, grade) VALUES (?, ?)",
            [(grade_keys[grade], grade) for grade in grades],
        )
        connection.executemany(
            """
            INSERT INTO fact_loans (
                loan_id,
                grade_key,
                annual_income,
                debt,
                days_past_due,
                loan_amount,
                debt_to_income,
                is_delinquent,
                dti_band
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["loan_id"],
                    grade_keys[row["grade"]],
                    row["annual_income"],
                    row["debt"],
                    row["days_past_due"],
                    row["loan_amount"],
                    row["debt_to_income"],
                    row["is_delinquent"],
                    row["dti_band"],
                )
                for row in rows
            ],
        )

        mart_sql = (
            Path(__file__).resolve().parents[2] / "sql" / "build_grade_risk_mart.sql"
        ).read_text(encoding="utf-8")
        connection.executescript(mart_sql)

        mart_rows = connection.execute(
            "SELECT COUNT(*) FROM mart_grade_risk"
        ).fetchone()[0]

    return FinanceWarehouseSummary(
        grades_loaded=len(grades),
        loans_loaded=len(rows),
        mart_rows=mart_rows,
    )


def _load_cleaned_rows(cleaned_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with cleaned_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "loan_id": row["loan_id"],
                    "grade": row["grade"],
                    "annual_income": float(row["annual_income"]),
                    "debt": float(row["debt"]),
                    "days_past_due": int(row["days_past_due"]),
                    "loan_amount": float(row["loan_amount"]),
                    "debt_to_income": float(row["debt_to_income"]),
                    "is_delinquent": int(row["is_delinquent"]),
                    "dti_band": row["dti_band"],
                }
            )
    return rows


def _create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        DROP TABLE IF EXISTS mart_grade_risk;
        DROP TABLE IF EXISTS fact_loans;
        DROP TABLE IF EXISTS dim_grade;

        CREATE TABLE dim_grade (
            grade_key INTEGER PRIMARY KEY,
            grade TEXT NOT NULL UNIQUE
        );

        CREATE TABLE fact_loans (
            loan_id TEXT PRIMARY KEY,
            grade_key INTEGER NOT NULL,
            annual_income REAL NOT NULL,
            debt REAL NOT NULL,
            days_past_due INTEGER NOT NULL,
            loan_amount REAL NOT NULL,
            debt_to_income REAL NOT NULL,
            is_delinquent INTEGER NOT NULL,
            dti_band TEXT NOT NULL,
            FOREIGN KEY(grade_key) REFERENCES dim_grade(grade_key)
        );
        """
    )

