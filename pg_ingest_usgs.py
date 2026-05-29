import os
import requests
import psycopg2
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv

# Laeme .env failist muutujad
load_dotenv()

DB_USER = os.getenv("MAAVARIN_USER")
DB_PASSWORD = os.getenv("MAAVARIN_PW")
DB_NAME = os.getenv("PGRES_MAAVARIN_DB")
DB_PORT = int(os.getenv("DB_PORT_HOST"))
USGS_URL = os.getenv("USGS_URL")

DB_HOST = "localhost"

# Ajaperiood USGS päringuks
end_time = datetime.now(UTC)
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

# Ühendus PostgreSQL andmebaasiga
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME
)
cur = conn.cursor()

# --- LOOME TÄIELIKU TABELI ---
cur.execute("""
CREATE TABLE IF NOT EXISTS earthquakes (
    id TEXT PRIMARY KEY,
    time TIMESTAMP,
    updated TIMESTAMP,
    place TEXT,
    magnitude REAL,
    tz INTEGER,
    url TEXT,
    detail TEXT,
    felt INTEGER,
    cdi REAL,
    mmi REAL,
    alert TEXT,
    status TEXT,
    tsunami INTEGER,
    sig INTEGER,
    net TEXT,
    code TEXT,
    ids TEXT,
    sources TEXT,
    types TEXT,
    nst INTEGER,
    dmin REAL,
    rms REAL,
    gap REAL,
    magType TEXT,
    type TEXT,
    longitude REAL,
    latitude REAL,
    depth REAL
)
""")
conn.commit()

# --- AUTOMAATNE INSERT ---
columns = [
    "id", "time", "updated", "place", "magnitude", "tz", "url", "detail",
    "felt", "cdi", "mmi", "alert", "status", "tsunami", "sig", "net",
    "code", "ids", "sources", "types", "nst", "dmin", "rms", "gap",
    "magType", "type", "longitude", "latitude", "depth"
]

insert_sql = f"""
INSERT INTO earthquakes ({",".join(columns)})
VALUES ({",".join(["%s"] * len(columns))})
ON CONFLICT (id) DO NOTHING
"""

count = 0

for eq in earthquakes:
    props = eq["properties"]
    geom = eq["geometry"]

    row = [
        eq["id"],
        datetime.fromtimestamp(props["time"] / 1000, UTC) if props.get("time") else None,
        datetime.fromtimestamp(props["updated"] / 1000, UTC) if props.get("updated") else None,
        props.get("place"),
        props.get("mag"),
        props.get("tz"),
        props.get("url"),
        props.get("detail"),
        props.get("felt"),
        props.get("cdi"),
        props.get("mmi"),
        props.get("alert"),
        props.get("status"),
        props.get("tsunami"),
        props.get("sig"),
        props.get("net"),
        props.get("code"),
        props.get("ids"),
        props.get("sources"),
        props.get("types"),
        props.get("nst"),
        props.get("dmin"),
        props.get("rms"),
        props.get("gap"),
        props.get("magType"),
        props.get("type"),
        geom["coordinates"][0],
        geom["coordinates"][1],
        geom["coordinates"][2]
    ]

    cur.execute(insert_sql, row)
    count += 1

conn.commit()

print(f"Lisatud {count} rida andmebaasi.")

cur.close()
conn.close()

print("Valmis.")
