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

# Loeme 20 rida
query = """
SELECT *
FROM earthquakes
ORDER BY time DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)

# Salvestame CSV
output_file = "usgs_kont_earthquakes_20rida.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"CSV loodud: {output_file}")

conn.close()
