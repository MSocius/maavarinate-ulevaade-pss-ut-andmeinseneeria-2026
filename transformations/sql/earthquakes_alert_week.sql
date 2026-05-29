CREATE VIEW earthquakes_alert_week AS
SELECT
    id,
    time,
    updated,
    place,
    magnitude,
    longitude,
    latitude,
    depth,
    tsunami,
    date(time) AS day,
    COUNT(*) OVER (PARTITION BY date(time)) AS alert_quakes
FROM earthquakes
WHERE magnitude >= 5
  AND time >= NOW() - INTERVAL '7 days'
ORDER BY time;
