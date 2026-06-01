import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Laeme .env
load_dotenv()

DB_USER = os.getenv("MAAVARIN_USER")
DB_PASSWORD = os.getenv("MAAVARIN_PW")
DB_NAME = os.getenv("PGRES_MAAVARIN_DB")
DB_PORT = int(os.getenv("DB_PORT_HOST"))
DB_HOST = "localhost"

# Ühendus PostgreSQL-iga
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME
)

# SQL duplikaatide leidmiseks
query = """
SELECT id, COUNT(*) AS kordusi
FROM earthquakes
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY kordusi DESC;
"""

df = pd.read_sql(query, conn)

if df.empty:
    print("✔ Duplikaate ei ole — kõik id väärtused on unikaalsed.")
else:
    print("❗ Leitud duplikaadid:")
    print(df)

    # Kokku mitu duplikaat-ID-d
    print(f"\nDuplikaat-ID-sid kokku: {len(df)}")

    # Kokku mitu rida on duplikaatidest üleliigsed
    df['üleliigseid'] = df['kordusi'] - 1
    print(f"Üleliigseid ridu kokku: {df['üleliigseid'].sum()}")

conn.close()