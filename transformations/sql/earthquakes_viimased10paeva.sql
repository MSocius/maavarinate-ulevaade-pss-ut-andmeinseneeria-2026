CREATE OR REPLACE VIEW earthquakes_viimased10paeva AS
SELECT *
FROM earthquakes
WHERE time >= NOW() - INTERVAL '10 days'
ORDER BY time DESC;
