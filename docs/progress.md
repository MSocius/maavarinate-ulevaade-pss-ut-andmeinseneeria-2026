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
* USGS API andmed salvestatakse PostgreSQL andmebaasi tabelisse earthquakes, mis toimib projekti staging kihina ja see on järgmiste transformatsioonide ja vaadete sisend tabel (pg_ingest_usgs.py);  
* transformatsioon ehk sql päring (earthquakes_alert_week.sql);  
* kuvab graafiku (day_alert.py);
* kontroll st ühe reaga mitu maavärinat kvalifitseerus;


## Järgmised sammud

- Milline on USGS andmete kogu laius? kõik col pealkirjad? Ilmselt peaks meile päringu mõõdet kavatama.
- > py daytime teek "unix to UTC"?
- https://open-meteo.com/en/docs uurida uue andmeallika lisamist;
- > kas õnnestub meteo päringut teha vastavalt maavärina koordinaatidele?
- Kontroll
- cron job käivitab xx.py:
- > USGS päring - olemas
  >  
- Esimene tegevus, mis ees ootab]
- [Teine tegevus]
- [Kolmas tegevus]

## Mis takistab

- "Praegu pole blokeerivaid probleeme"
-  [Probleem 1 — näiteks: API tagastab vigaseid väärtusi ühes linnas]
- [Probleem 2 — või: "Praegu pole blokeerivaid probleeme"]

## Kontrollpunkt

Käsk, millega saab kontrollida, et töövoog töötab:


```bash



```bash



```bash
01_käsk,  mis näitab, et andmed liiguvad allikast näidikulauani
python day_alert.py

kontroll_02
docker compose exec db psql -U meiegrupp -d MAAVARIN_PG -c "SELECT COUNT(*) FROM earthquakes_alert_week;"

Oodatav tulemus: PostgreSQL tagastab ühe rea, mis näitab viimase 7 päeva ≥5.0 magnituudiga maavärinate arvu
 count
-------
     6

