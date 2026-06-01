import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Laeme .env
load_dotenv()

# Andmebaasi ühenduse seaded
DB_USER = os.getenv("MAAVARIN_USER")
DB_PASSWORD = os.getenv("MAAVARIN_PW")
DB_NAME = os.getenv("PGRES_MAAVARIN_DB")
DB_PORT = int(os.getenv("DB_PORT_HOST"))
DB_HOST = "localhost"

# Magnituudi vahemik .env failist
MIN_MAG = float(os.getenv("MAG_MIN"))
MAX_MAG = float(os.getenv("MAG_MAX"))

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

    # --- 1) NULL väärtused ---
    null_df = pd.read_sql("""
        SELECT id, time, magnitude
        FROM earthquakes
        WHERE magnitude IS NULL
        ORDER BY time DESC;
    """, conn)

    # --- 2) Väärtused väiksemad kui MIN ---
    low_df = pd.read_sql(f"""
        SELECT id, time, magnitude
        FROM earthquakes
        WHERE magnitude < {MIN_MAG}
        ORDER BY time DESC;
    """, conn)

    # --- 3) Väärtused suuremad kui MAX ---
    high_df = pd.read_sql(f"""
        SELECT id, time, magnitude
        FROM earthquakes
        WHERE magnitude > {MAX_MAG}
        ORDER BY time DESC;
    """, conn)

    print("\n=== MAGNITUUDI KVALITEEDIKONTROLL ===")
    print(f"Lubatud vahemik: {MIN_MAG} … {MAX_MAG}\n")

    # --- Tulemused ---
    if null_df.empty:
        print("✔ NULL väärtusi ei leitud.")
    else:
        print("❗ Leitud NULL väärtusi:")
        print(null_df)
        print(f"Kokku: {len(null_df)}\n")

    if low_df.empty:
        print(f"✔ Väärtusi väiksemaid kui {MIN_MAG} ei leitud.")
    else:
        print(f"❗ Leitud väärtusi väiksemaid kui {MIN_MAG}:")
        print(low_df)
        print(f"Kokku: {len(low_df)}\n")

    if high_df.empty:
        print(f"✔ Väärtusi suuremaid kui {MAX_MAG} ei leitud.")
    else:
        print(f"❗ Leitud väärtusi suuremaid kui {MAX_MAG}:")
        print(high_df)
        print(f"Kokku: {len(high_df)}\n")

    conn.close()

if __name__ == "__main__":
    main()
