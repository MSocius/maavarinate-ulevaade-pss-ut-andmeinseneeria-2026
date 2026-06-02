import subprocess

scripts = [
    "pg_ingest_usgs.py",
    "usgs_kont_earthquakes_viimased10paeva.py",
    "usgs_kont_nodup_notnull_id.py",
    "usgs_kont_magnituud_vaartusele.py",
    "day_alert.py",  # leiab maavärinad
    "openmeteo_maav_ilm_tund.py",   # "openmeteo_maav_ilm_tund_PWkoodis.py", ¤ leiab ilmastiku vastavalt maavärina koordinaadile
    "openmeteo_maav_ilm_tund_tabel.py",
]

for script in scripts:
    print(f"\n▶ Käivitan: {script}")
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"❌ Viga skriptis: {script}. Peatan ETL-i.")
        break

    print(f"✔ Valmis: {script}")

print("\n🎉 Kõik skriptid edukalt käivitatud!")
