import os
import requests
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Laeme .env failist muutujad
load_dotenv()

DB_USER = os.getenv("MAAVARIN_USER")
DB_PASSWORD = os.getenv("MAAVARIN_PW")
DB_NAME = os.getenv("PGRES_MAAVARIN_DB")
DB_PORT = int(os.getenv("DB_PORT_HOST"))
USGS_URL = os.getenv("USGS_URL")

DB_HOST = "localhost"   # Dockeris PostgreSQL töötab sinu masinas sellel hostil

# Ajaperiood USGS päringuks
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=30)

params = {
    "format": "geojson",
    "starttime": start_time.strftime("%Y-%m-%d"),
    "endtime": end_time.strftime("%Y-%m-%d"),
    "limit": 20000
}

print("Laen USGS andmeid...")
response = requests.get(USGS_URL, params=params)
data = response.json()

earthquakes = data.get("features", [])
print(f"Leitud {len(earthquakes)} maavärinat.")

# Ühendus päris PostgreSQL andmebaasiga
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME
)
cur = conn.cursor()

# Loome tabeli, kui seda pole
cur.execute("""
CREATE TABLE IF NOT EXISTS earthquakes (
    id TEXT PRIMARY KEY,
    time TIMESTAMP,
    place TEXT,
    magnitude REAL,
    longitude REAL,
    latitude REAL,
    depth REAL
)
""")
conn.commit()

# Lisame andmed
insert_sql = """
INSERT INTO earthquakes (id, time, place, magnitude, longitude, latitude, depth)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING
"""

count = 0

for eq in earthquakes:
    props = eq["properties"]
    geom = eq["geometry"]

    eq_id = eq["id"]
    eq_time = datetime.utcfromtimestamp(props["time"] / 1000)
    eq_place = props["place"]
    eq_mag = props["mag"]
    lon, lat, depth = geom["coordinates"]

    cur.execute(insert_sql, (eq_id, eq_time, eq_place, eq_mag, lon, lat, depth))
    count += 1

conn.commit()

print(f"Lisatud {count} rida andmebaasi.")

cur.close()
conn.close()

print("Valmis.")
