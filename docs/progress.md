# Edenemisraport

> **Juhend:** See fail on projektitöö teise nädala väljund. Uuenda lühidalt iga esitamise eel. Kustuta see juhendrida.

## Mis on valmis

- [x] Docker Compose käivitab kõik teenused
- [x] Andmeid saadakse allikast kätte
- [x] Andmed laetakse `staging` kihti
- [x] Vähemalt üks transformatsioon toimib
- [x] Vähemalt üks näidikulaud on nähtaval
- [x] Vähemalt üks andmekvaliteedi test läbib

Lühidalt, mis on valmis:  
pg_ingest_usgs.py = USGS API andmed salvestatakse PostgreSQL andmebaasi tabelisse earthquakes, mis toimib projekti staging kihina ja see on järgmiste transformatsioonide ja vaadete sisend tabel;  
earthquakes_alert_week.sql = transformatsioon;
day_alert.py = kuvab graafiku;
kontroll = ühe reaga mitu maavärinat kvalifitseerus;


## Järgmised sammud

- [Esimene tegevus, mis ees ootab]
- [Teine tegevus]
- [Kolmas tegevus]

## Mis takistab

- [Probleem 1 — näiteks: API tagastab vigaseid väärtusi ühes linnas]
- [Probleem 2 — või: "Praegu pole blokeerivaid probleeme"]

## Kontrollpunkt

Käsk, millega saab kontrollida, et töövoog töötab:

```bash
# [Lisa siia käsk, mis näitab, et andmed liiguvad allikast näidikulauani]

#  näide 1
docker compose exec db psql -U meiegrupp -d MAAVARIN_PG -c "SELECT COUNT(*) FROM earthquakes_alert_week;"

Oodatav tulemus: PostgreSQL tagastab ühe rea, mis näitab viimase 7 päeva ≥5.0 magnituudiga maavärinate arvu
 count
-------
     6

