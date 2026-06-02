import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from dotenv import load_dotenv
import os

# -----------------------------
# Laeme .env failist muutujad
# -----------------------------
load_dotenv()

PG_USER = os.getenv("MAAVARIN_USER")
PG_PASSWORD = os.getenv("MAAVARIN_PW")
PG_DB = os.getenv("PGRES_MAAVARIN_DB")
PG_PORT = os.getenv("DB_PORT_HOST", 5432)
PG_HOST = "localhost"   # kui Docker Compose, siis "postgres"

AUTOREFRESH = int(os.getenv("DASHBOARD_AUTOREFRESH_SECONDS", 60))

# -----------------------------
# PostgreSQL ühendus
# -----------------------------
def get_connection():
    return psycopg2.connect(
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )

# -----------------------------
# Andmete lugemine
# -----------------------------
@st.cache_data(ttl=60)
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM earthquakes_daily ORDER BY day", conn)
    conn.close()
    return df

df = load_data()

# -----------------------------
# Pealkiri
# -----------------------------
st.title("🌍 Maavärinate ülevaade (PostgreSQL + Streamlit + .env)")

st.write(f"⏱ Auto-refresh: iga {AUTOREFRESH} sekundi järel")

# -----------------------------
# KPI-d
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Kokku maavärinaid", int(df["total_quakes"].sum()))
col2.metric("Keskmine päevas", round(df["total_quakes"].mean(), 2))
col3.metric("Viimase päeva arv", int(df["total_quakes"].iloc[-1]))

# -----------------------------
# Trendigraafik
# -----------------------------
fig = px.line(
    df,
    x="day",
    y="total_quakes",
    markers=True,
    title="Maavärinate arv päevas"
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Magnituudi histogramm (kui olemas)
# -----------------------------
if "avg_magnitude" in df.columns:
    fig2 = px.histogram(
        df,
        x="avg_magnitude",
        nbins=20,
        title="Magnituudi jaotus"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Toorandmete tabel
# -----------------------------
with st.expander("Vaata toorandmeid"):
    st.dataframe(df)
