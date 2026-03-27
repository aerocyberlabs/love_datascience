SELECT
    grade,
    COUNT(*) AS loan_count,
    SUM(is_delinquent) AS delinquent_loans,
    ROUND(AVG(is_delinquent), 3) AS delinquency_rate,
    ROUND(AVG(debt_to_income), 3) AS avg_debt_to_income
FROM cleaned_loans
GROUP BY grade
ORDER BY grade;

