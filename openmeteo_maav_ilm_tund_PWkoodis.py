import requests
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Laeme .env faili
load_dotenv()

# -----------------------------
# 1) Kõik Open-Meteo hourly veerud
# -----------------------------
hourly_params = [
    "temperature_2m","relativehumidity_2m","dewpoint_2m","apparent_temperature",
    "pressure_msl","surface_pressure","cloudcover","cloudcover_low","cloudcover_mid",
    "cloudcover_high","windspeed_10m","windspeed_80m","windspeed_120m","windspeed_180m",
    "winddirection_10m","winddirection_80m","winddirection_120m","winddirection_180m",
    "windgusts_10m","shortwave_radiation","direct_radiation","diffuse_radiation",
    "direct_normal_irradiance","terrestrial_radiation","weathercode","precipitation",
    "rain","showers","snowfall","snow_depth","freezinglevel_height","visibility",
    "evapotranspiration","soil_temperature_0cm","soil_temperature_6cm",
    "soil_temperature_18cm","soil_temperature_54cm","soil_moisture_0_1cm",
    "soil_moisture_1_3cm","soil_moisture_3_9cm","soil_moisture_9_27cm",
    "soil_moisture_27_81cm"
]

# -----------------------------
# 2) Open-Meteo päring 36h enne + 36h pärast
# -----------------------------
def fetch_weather_72h(lat, lon, event_time):
    dt = pd.to_datetime(event_time).to_pydatetime()

    start = (dt - timedelta(hours=36)).strftime("%Y-%m-%d")
    end   = (dt + timedelta(hours=36)).strftime("%Y-%m-%d")

    BASE_URL = os.getenv("OPENMETEO_BASE_URL")

    url = (
        f"{BASE_URL}"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        f"&hourly={','.join(hourly_params)}"
        "&timezone=UTC"
    )

    r = requests.get(url)
    data = r.json()

    if "hourly" not in data:
        return None

    return pd.DataFrame(data["hourly"])

# -----------------------------
# 3) PostgreSQL ühendus
# -----------------------------
conn = psycopg2.connect(
    dbname="MAAVARIN_PG",
    user="meiegrupp",
    password="meieparool",
    host="localhost",
    port=55432
)
cur = conn.cursor()

# -----------------------------
# 3.1) Kustutame vanad read, et vältida duplikaate
# -----------------------------
cur.execute("DELETE FROM openmeteo_maav_ilm_tund;")
conn.commit()
print("🧹 Puhastatud: openmeteo_maav_ilm_tund (vanad read kustutatud)")

# -----------------------------
# 4) Loo tabel, kui seda pole
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS openmeteo_maav_ilm_tund (
    id TEXT,
    weather_time TIMESTAMP,
    temperature_2m REAL,
    relativehumidity_2m REAL,
    dewpoint_2m REAL,
    apparent_temperature REAL,
    pressure_msl REAL,
    surface_pressure REAL,
    cloudcover REAL,
    cloudcover_low REAL,
    cloudcover_mid REAL,
    cloudcover_high REAL,
    windspeed_10m REAL,
    windspeed_80m REAL,
    windspeed_120m REAL,
    windspeed_180m REAL,
    winddirection_10m REAL,
    winddirection_80m REAL,
    winddirection_120m REAL,
    winddirection_180m REAL,
    windgusts_10m REAL,
    shortwave_radiation REAL,
    direct_radiation REAL,
    diffuse_radiation REAL,
    direct_normal_irradiance REAL,
    terrestrial_radiation REAL,
    weathercode INT,
    precipitation REAL,
    rain REAL,
    showers REAL,
    snowfall REAL,
    snow_depth REAL,
    freezinglevel_height REAL,
    visibility REAL,
    evapotranspiration REAL,
    soil_temperature_0cm REAL,
    soil_temperature_6cm REAL,
    soil_temperature_18cm REAL,
    soil_temperature_54cm REAL,
    soil_moisture_0_1cm REAL,
    soil_moisture_1_3cm REAL,
    soil_moisture_3_9cm REAL,
    soil_moisture_9_27cm REAL,
    soil_moisture_27_81cm REAL
);
""")
conn.commit()

# -----------------------------
# 5) Võta 5 suurimat alert-quake'i
# -----------------------------
df_eq = pd.read_sql("""
    SELECT e.id, e.time, e.latitude, e.longitude
    FROM earthquakes e
    JOIN earthquakes_alert_week w ON e.id = w.id
    WHERE e.magnitude >= 5
      AND e.time >= NOW() - INTERVAL '7 days'
    ORDER BY e.magnitude DESC
    LIMIT 5;
""", conn)

# -----------------------------
# 6) ETL: dünaamiline INSERT (turvaline)
# -----------------------------
columns = ["id", "weather_time"] + hourly_params
placeholders = ", ".join(["%s"] * len(columns))
colnames = ", ".join(columns)

insert_sql = f"INSERT INTO openmeteo_maav_ilm_tund ({colnames}) VALUES ({placeholders})"

for _, row in df_eq.iterrows():
    df_weather = fetch_weather_72h(row["latitude"], row["longitude"], row["time"])
    if df_weather is None:
        continue

    for _, r in df_weather.iterrows():
        values = [row["id"], r["time"]] + [r.get(col) for col in hourly_params]
        cur.execute(insert_sql, values)

conn.commit()
cur.close()
conn.close()

print("✔ ETL valmis — andmed salvestatud tabelisse openmeteo_maav_ilm_tund")
