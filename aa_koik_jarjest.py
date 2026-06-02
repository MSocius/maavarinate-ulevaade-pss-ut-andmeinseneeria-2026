import subprocess

scripts = [
    "pg_ingest_usgs.py",
    "openmeteo_maav_ilm_tund.py",
    "openmeteo_maav_ilm_tund_tabel.py"
    "day_alert.py"
]

for script in scripts:
    print(f"\n▶ Käivitan: {script}")
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"❌ Viga skriptis: {script}. Peatan ETL-i.")
        break

    print(f"✔ Valmis: {script}")

print("\n🎉 Kõik skriptid edukalt käivitatud!")
