SELECT
    route,
    shipment_count,
    late_shipments,
    late_ratio,
    avg_delay_days,
    total_weight_kg
FROM route_summary
ORDER BY late_ratio DESC, total_weight_kg DESC;

