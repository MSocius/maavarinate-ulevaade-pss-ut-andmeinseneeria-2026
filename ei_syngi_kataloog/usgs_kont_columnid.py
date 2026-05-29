import requests
import csv

# USGS GeoJSON feed (võid muuta all_day → all_week jne)
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

# Lae andmed
data = requests.get(url).json()

# Võta esimese kirje properties võtmed (column nimed)
columns = list(data["features"][0]["properties"].keys())

# Salvesta CSV faili
with open("usgs_kont_columnid.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["column_name"])  # header
    for col in columns:
        writer.writerow([col])

print("Column nimed salvestatud faili: usgs_kont_columnid.csv")
