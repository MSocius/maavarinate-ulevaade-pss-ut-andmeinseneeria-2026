# Edenemisraport
## Mis on valmis

- [x] Docker Compose käivitab kõik teenused
- [x] Andmeid saadakse allikast kätte
- [x] Andmed laetakse `staging` kihti
- [x] Vähemalt üks transformatsioon toimib
- [x] Vähemalt üks näidikulaud on nähtaval
- [x] Vähemalt üks andmekvaliteedi test läbib

### Lühidalt, mis on valmis:  
* USGS API andmed salvestatakse PostgreSQL andmebaasi tabelisse earthquakes, mis asub  projekti staging kihis. See on järgmiste transformatsioonide ja vaadete sisend tabel
  > pg_ingest_usgs.py loob tabeli ja laeb tabelisse andmed. Väljund PostgreSQL tabel eartquakes MAAVARIN_PG public skeemis; 
  > usgs_kont_columnid.py kontrollib, mis veerud tabelis on. Väljund csv fail veergude metadataga;
  > usgs_kont_earthquakes_viimased10paeva.py leiab 10 eelneva päeva maavärinad. Väljund csv.
  > Unikaalsuse kontroll: usgs_kont_dup_id.py kontrollib kas PostgreSQL tabel eartquakes on duplikaate id veerus.
* transformatsioon ehk sql päring (earthquakes_alert_week.sql) kuvab graafiku (day_alert.py);
* kontroll ühe reaga mitu maavärinat kvalifitseerus;
* lisatud andmeallikas https://open-meteo.com
  > openmeteo_maav_ilm_tund.py toob amdmed PostgreSQL tabelisse openmeteo_maav_ilm_tund MAAVARIN_PG public skeemis;
  > päring lisab ilmaandmed kui maaväirina magmituud on minimaalselt 5,0 vastavalt maavärina koordinaatidele;
* kood aa_koik_jarjest.py käivitab kõik andmevoo sammud järjest


## Järgmised sammud
* Open Meteo parooli vaja env faili viia
* py daytime teek "unix to UTC" - kas seda on vaja??
* andmekontrollide ja transformatsioonide täiendamine
  > välja filtreerida kirjed, mis ei ole maavärinad (type not equal to "earthquake");
  > välja filtreerida kirjed ilma magnituudita (kontroll: kirjete arv, kus magnituudi info puudu);
  > välja filtreerida kirjed ilma koordinaatideta (kontroll: kirjete arv, kus koordinaate ei ole);
  > kas kõikide väljavalitud maavärinate koordinaatidele leiab open-meteo-st ilmastiku info (kontroll: kirjete arv, millele ei saanud openmeteost vastet);
* lisada andmeväljadele juurde metaandmed näiteks tunnuse "sig" selgitus: "A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum MMI, felt reports, and estimated impact. Typical values [0, 1000]" 
* cron job käivitab xx.py:
  > USGS päring - olemas;
  > kui leiab maavärina, siis milline oli ilm? - puudu;
  > SQL - trasformatsioon sama baasi sees;
  > testid.

## Mis takistab
- praegu pole blokeerivaid probleeme (peale selle, et aeg on piiratud ja oskused ei ole nii head kui saaksid olla)  
  
## Kontrollpunkt
Käsk, millega saab kontrollida, et töövoog töötab:

```bash
# 01_käsk,  mis näitab, et andmed liiguvad allikast näidikulauani
python day_alert.py

# kontroll_02
docker compose exec db psql -U meiegrupp -d MAAVARIN_PG -c "SELECT COUNT(*) FROM earthquakes_alert_week;"

#Oodatav tulemus: PostgreSQL tagastab ühe rea, mis näitab viimase 7 päeva ≥5.0 magnituudiga maavärinate arvu
# count
# -------
#     6

