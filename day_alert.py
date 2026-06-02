import os

from dotenv import load_dotenv
load_dotenv()
SQL_KAUSTA_URL = os.getenv("SQL_KAUSTA_URL")

import pandas as pd
import psycopg2
import matplotlib.pyplot as plt


# Laeme .env failist muutujad
load_dotenv()

DB_USER = os.getenv("MAAVARIN_USER")
DB_PASSWORD = os.getenv("MAAVARIN_PW")
DB_NAME = os.getenv("PGRES_MAAVARIN_DB")
DB_PORT = int(os.getenv("DB_PORT_HOST"))
USGS_URL = os.getenv("USGS_URL")

# PostgreSQL ühendus
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host="localhost",
    port=DB_PORT
)

cur = conn.cursor()


# --- 1) Laeme SQL-faili ja loome/uuendame vaate ---
# SQL_KAUSTA_URL = os.getenv("SQL_KAUSTA_URL")
path = f"{SQL_KAUSTA_URL}earthquakes_alert_week.sql"

with open(path, "r", encoding="utf-8") as f:
    sql = f.read()

cur.execute(sql)
conn.commit()

# --- 2) Loeme andmed VAATEST ---
df = pd.read_sql("SELECT * FROM earthquakes_alert_week ORDER BY day", conn)


# --- 3) Kuvame terminalis ---
print("Vaate 'earthquakes_alert_week' sisu:")
print(df)
print("\nRidu kokku:", len(df))

# --- 4) Graafik ---
plt.figure(figsize=(10,5))
plt.bar(df['day'], df['alert_quakes'], color='red')
plt.title("Reageerimist vajava ohutasemega maavärinate arv viimasel nädalal")
plt.xlabel("Päev")
plt.ylabel("Maavärinate arv (mag ≥ 5.0)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

cur.close()
conn.close()

