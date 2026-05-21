import requests
import duckdb
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------------------
# CONFIG
# -----------------------------------------
DB_PATH = "earthquakes.duckdb"
TABLE_NAME = "raw_usgs_earthquakes"

# USGS API endpoint
USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Default: viimased 30 päeva
END_DATE = datetime.utcnow().date()
START_DATE = END_DATE - timedelta(days=30)


# -----------------------------------------
# FETCH DATA FROM USGS
# -----------------------------------------
def fetch_usgs_data(start_date, end_date):
    params = {
        "format": "geojson",
        "starttime": start_date.isoformat(),
        "endtime": end_date.isoformat(),
        "limit": 20000  # USGS max per request
    }

    print(f"📡 Fetching USGS data {start_date} → {end_date}")

    response = requests.get(USGS_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"USGS API error: {response.status_code}")

    data = response.json()

    # Extract features
    features = data.get("features", [])
    print(f"✔ Received {len(features)} earthquake records")

    # Convert to DataFrame
    rows = []
    for f in features:
        props = f["properties"]
        geom = f["geometry"]

        rows.append({
            "id": f.get("id"),
            "time": datetime.utcfromtimestamp(props["time"] / 1000),
            "updated": datetime.utcfromtimestamp(props["updated"] / 1000),
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
