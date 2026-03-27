SELECT COUNT(*) AS shipment_count
FROM shipments;

SELECT shipment_id, COUNT(*) AS duplicate_count
FROM shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS null_status_rows
FROM shipments
WHERE status IS NULL OR TRIM(status) = '';

