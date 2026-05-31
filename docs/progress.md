# Edenemisraport
## Mis on valmis

- [x] Docker Compose käivitab kõik teenused
- [x] Andmeid saadakse allikast kätte
- [x] Andmed laetakse `staging` kihti
- [x] Vähemalt üks transformatsioon toimib
- [x] Vähemalt üks näidikulaud on nähtaval
- [x] Vähemalt üks andmekvaliteedi test läbib

Lühidalt, mis on valmis:  
* USGS API andmed salvestatakse PostgreSQL andmebaasi tabelisse earthquakes, mis asub  projekti staging kihis. See on järgmiste transformatsioonide ja vaadete sisend tabel (kood: pg_ingest_usgs.py);  
  >usgs_kont_columnid.py kontrollib, mis veerud tabelis on. Väljund csv fail veergude metadataga
  >usgs_kont_earhquakes_20rida.py, mis andmed tabelis on. Väljund csv 20 rida dataga  
* transformatsioon ehk sql päring (earthquakes_alert_week.sql) kuvab graafiku (day_alert.py);
* kontroll st ühe reaga mitu maavärinat kvalifitseerus;
* lisatud andmeallikas https://open-meteo.com - kood openmeteo_maav_ilm_tund.py toob amdmed PostgreSQL andmebaasi tabelisse openmeteo_maav_ilm_tund
  > päring lisab ilmaandmed kui maaväirina magmituud on minimaalselt 5,0 vastavalt maavärina koordinaatidele
* aa_koik_jarjest.py käivitab kõik sammud järjest


## Järgmised sammud

- Opem Meteo parooli vaja env faili viia
- py daytime teek "unix to UTC" - kas seda on vaja??
- Kontroll
- cron job käivitab xx.py:
- > USGS päring - olemas
  > kui leeiab maavärina siis milline oli ilm? - puudub
  > SQL - trasformatsioon sma baasi sees - 
  > testid 

## Mis takistab
- "Praegu pole blokeerivaid probleeme"
- oskused ja piiratud aeg 
  
## Kontrollpunkt
Käsk, millega saab kontrollida, et töövoog töötab:

```bash
01_käsk,  mis näitab, et andmed liiguvad allikast näidikulauani
python day_alert.py

kontroll_02
docker compose exec db psql -U meiegrupp -d MAAVARIN_PG -c "SELECT COUNT(*) FROM earthquakes_alert_week;"

Oodatav tulemus: PostgreSQL tagastab ühe rea, mis näitab viimase 7 päeva ≥5.0 magnituudiga maavärinate arvu
 count
-------
     6

