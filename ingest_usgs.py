import requests
import duckdb
import pandas as pd
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os

# -----------------------------------------
# LOAD ENV VARIABLES
# -----------------------------------------
load_dotenv()

DB_PATH = os.getenv("DB_PATH")
TABLE_NAME = os.getenv("TABLE_NAME")
USGS_URL = os.getenv("USGS_URL")
DAYS = int(os.getenv("DAYS"))

# -----------------------------------------
# DATE RANGE
# -----------------------------------------
END_DATE = datetime.now(UTC).date()
START_DATE = END_DATE - timedelta(days=DAYS)

# -----------------------------------------
# FETCH DATA FROM USGS
# -----------------------------------------
def fetch_usgs_data(start_date, end_date):
    params = {
        "format": "geojson",
        "starttime": start_date.isoformat(),
        "endtime": end_date.isoformat(),
        "limit": 20000
    }

    print(f"📡 Fetching USGS data {start_date} → {end_date}")

    response = requests.get(USGS_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"USGS API error: {response.status_code}")

    data = response.json()
    features = data.get("features", [])
    print(f"✔ Received {len(features)} earthquake records")

    rows = []
    for f in features:
        props = f["properties"]
        geom = f["geometry"]

        rows.append({
            "id": f.get("id"),
            "time": datetime.fromtimestamp(props["time"] / 1000, UTC),
            "updated": datetime.fromtimestamp(props["updated"] / 1000, UTC),
            "mag": props.get("mag"),
            "place": props.get("place"),
            "type": props.get("type"),
            "status": props.get("status"),
            "tsunami": props.get("tsunami"),
            "sig": props.get("sig"),
            "longitude": geom["coordinates"][0],
            "latitude": geom["coordinates"][1],
            "depth": geom["coordinates"][2]
        })

    df = pd.DataFrame(rows)
    return df

# -----------------------------------------
# SAVE TO DUCKDB
# -----------------------------------------
def save_to_duckdb(df):
    con = duckdb.connect(DB_PATH)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} AS
        SELECT * FROM df LIMIT 0;
    """)

    con.execute(f"INSERT INTO {TABLE_NAME} SELECT * FROM df")

    con.close()
    print(f"💾 Saved {len(df)} rows into {DB_PATH}:{TABLE_NAME}")

# -----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":
    df = fetch_usgs_data(START_DATE, END_DATE)
    save_to_duckdb(df)
    print("🎉 Ingestion complete!")
