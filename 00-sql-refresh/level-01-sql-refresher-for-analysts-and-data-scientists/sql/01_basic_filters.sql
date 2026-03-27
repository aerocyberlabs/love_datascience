SELECT shipment_id, route_id, status
FROM shipments
WHERE status = 'delivered'
ORDER BY shipment_id;

