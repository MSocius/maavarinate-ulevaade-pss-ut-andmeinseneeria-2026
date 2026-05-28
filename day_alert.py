import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="MAAVARIN_PG",
    user="meiegrupp",
    password="meieparool",
    host="localhost",
    port=55432
)

df = pd.read_sql("SELECT * FROM earthquakes_alert_week ORDER BY day", conn)

plt.figure(figsize=(10,5))
plt.bar(df['day'], df['alert_quakes'], color='red')
plt.title("Reageerimist vajava ohutasemega maavärinate arv viimasel nädalal")
plt.xlabel("Päev")
plt.ylabel("Maavärinate arv (mag ≥ 5.0)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()
