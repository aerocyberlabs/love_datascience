DROP TABLE IF EXISTS mart_route_kpis;

CREATE TABLE mart_route_kpis AS
SELECT
    d.route_name,
    COUNT(*) AS shipment_count,
    SUM(f.is_late) AS late_shipments,
    ROUND(AVG(f.delay_days), 3) AS avg_delay_days,
    ROUND(SUM(f.weight_kg), 3) AS total_weight_kg
FROM fact_shipments AS f
JOIN dim_route AS d
    ON f.route_key = d.route_key
GROUP BY d.route_name
ORDER BY d.route_name;

