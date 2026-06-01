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

# --- 1) Duplikaatide kontroll ---
dupes_query = """
SELECT id, COUNT(*) AS kordusi
FROM earthquakes
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY kordusi DESC;
"""

dupes_df = pd.read_sql(dupes_query, conn)

print("\n=== DUPLIKAATIDE KONTROLL (id veerg) ===")
if dupes_df.empty:
    print("✔ Duplikaate ei ole — kõik id väärtused on unikaalsed.")
else:
    print("❗ Leitud duplikaadid:")
    print(dupes_df)
    dupes_df["üleliigseid"] = dupes_df["kordusi"] - 1
    print(f"\nDuplikaat-ID-sid kokku: {len(dupes_df)}")
    print(f"Üleliigseid ridu kokku: {dupes_df['üleliigseid'].sum()}")

# --- 2) NOT NULL kontroll ---
notnull_query = """
SELECT COUNT(*) AS null_ridu
FROM earthquakes
WHERE id IS NULL;
"""

null_df = pd.read_sql(notnull_query, conn)
null_count = null_df["null_ridu"].iloc[0]

print("\n=== NOT NULL KONTROLL (id veerg) ===")
if null_count == 0:
    print("✔ Ühtegi NULL väärtust ei ole — id veerg on täielikult täidetud.")
else:
    print(f"❗ Leitud {null_count} rida, kus id = NULL.")

conn.close()
