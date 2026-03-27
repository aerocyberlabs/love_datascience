SELECT
    r.route_name,
    COUNT(*) AS shipment_count,
    SUM(s.is_late) AS late_shipments
FROM shipments AS s
JOIN routes AS r
    ON s.route_id = r.route_id
GROUP BY r.route_name
ORDER BY r.route_name;

