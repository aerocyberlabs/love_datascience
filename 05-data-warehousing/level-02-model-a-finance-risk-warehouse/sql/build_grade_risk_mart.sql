DROP TABLE IF EXISTS mart_grade_risk;

CREATE TABLE mart_grade_risk AS
SELECT
    d.grade,
    COUNT(*) AS loan_count,
    SUM(f.is_delinquent) AS delinquent_loans,
    ROUND(AVG(f.debt_to_income), 3) AS avg_debt_to_income
FROM fact_loans AS f
JOIN dim_grade AS d
    ON f.grade_key = d.grade_key
GROUP BY d.grade
ORDER BY d.grade;

