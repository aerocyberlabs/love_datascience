SELECT
    route,
    COUNT(*) AS shipment_count,
    SUM(is_late) AS late_shipments,
    ROUND(AVG(is_late), 3) AS late_ratio,
    ROUND(AVG(delay_days), 3) AS avg_delay_days,
    ROUND(SUM(weight_kg), 3) AS total_weight_kg
FROM cleaned_shipments
GROUP BY route
ORDER BY route;

