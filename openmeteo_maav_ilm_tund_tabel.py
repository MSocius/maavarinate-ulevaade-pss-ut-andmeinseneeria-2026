import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="MAAVARIN_PG",
    user="meiegrupp",
    password="meieparool",
    host="localhost",
    port=55432
)

df = pd.read_sql("SELECT * FROM openmeteo_maav_ilm_tund;", conn)
df.to_csv("openmeteo_export.csv", index=False, encoding="utf-8")

conn.close()

print("✔ CSV salvestatud: openmeteo_export.csv")
