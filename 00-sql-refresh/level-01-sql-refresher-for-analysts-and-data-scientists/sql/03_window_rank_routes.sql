WITH route_weights AS (
    SELECT
        r.route_name,
        ROUND(SUM(s.weight_kg), 1) AS total_weight_kg
    FROM shipments AS s
    JOIN routes AS r
        ON s.route_id = r.route_id
    GROUP BY r.route_name
)
SELECT
    route_name,
    total_weight_kg,
    RANK() OVER (ORDER BY total_weight_kg DESC) AS weight_rank
FROM route_weights
ORDER BY weight_rank, route_name;

