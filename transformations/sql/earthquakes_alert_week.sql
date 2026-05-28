CREATE OR REPLACE VIEW earthquakes_alert_week AS
SELECT
    DATE(time) AS day,
    COUNT(*) AS alert_quakes
FROM earthquakes_raw
WHERE mag >= 5.0
  AND time >= NOW() - INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;
