# Band Manager

Sovelluksen avulla bändi voi hallinnoida keikkakalenteria, biisien back-katalogia ja uusien biisien tekemistä.
Tämän lisäksi bändi voi sovelluksen avulla pitää kirjaa ns. backlinesta eli bändillä olevasta äänentoisto ym. kalustosta.
Sovelluksessa on peruskäyttäjiä ja ylläpitäjiä, jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

**Sovelluksen ominaisuuksia:**
- Käyttäjä voi kirjautua sisään ja luoda uuden tunnuksen
- Käyttäjä voi listata menneet keikat ja tulevat keikat
- Keikkojen osalta käyttäjä voi nähdä keikkojen aikataulut, keikkapaikan tiedot (yhteystiedot, osoite,...), ja keikalla esiintyneet muut bändit
- Käyttäjä voi listata keikkojen biisilistat
- Käyttäjä voi lisätä ja muokata keikka tietoja
- Esitettyjen biisien osalta voi listata erikseen omat biisit ja coverit (esim. Teostoa varten)
- Käyttäjä voi listata bändin biisit tietoineen: tekijät, onko jo levytetty / työn alla, esitykset keikoilla
- Käyttäjä voi tallentaa/hakea treeneissä treenattuja, erityisesti työn alla olevia, biisejä
- Biisin osalta käyttäjä voi listata/muokata biisissä käytettyjä instrumenttiefektejä esim. kitaran käytetyt soundit
- Käyttäjä voi listata/muokata bändin backlinen: kaapita, XLR piuhat, mikrofonit yms.

Sovelluksen aihepiirissä on huomattava määrä erilaisia laajennusmahdollisuuksia. Keskeistä on, että aktiivisesti keikkaileva ja omaa musiikkia tekevä bändi pystyy hallinoimaan bändin arkea.

**Sovelluksen tila 22.9.2024:**
- Käyttäjä voi kirjautua sisään ja luoda uuden tunnuksen
- Käyttäjä voi luoda uuden bändin
- Käyttäjä voi luoda biisin
- Käyttäjä voi listata menneet keikat ja tulevat keikat
- Käyttäjä voi luoda uuden keikan. Sen lisäksi käyttäjä voi lisätä keikkaan, joko jo olemassa olevan keikkapaikan tai luoda uuden keikkapaikan
- Keikkojen osalta käyttäjä voi nähdä keikkojen aikataulut ja keikkapaikan tiedot
- Käyttäjä voi listata keikkojen biisilistat
- Käyttäjä voi luoda uudelle keikalle biisilistan

Sovellusta voi testata lokaalisti. Repositorio sisältää testaamista varten vaadittavat kirjastot tiedostossa "requirements.txt" ja sen lisäksi repositoriossa on PostgreSQL -tietokantataulujen muodostusta varten "schema.sql" tiedoston.

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

`DATABASE_URL=\<tietokannan-paikallinen-osoite\>`

`SECRET_KEY=\<salainen-avain\>`

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r ./requirements.txt`

Määritä vielä tietokannan skeema komennolla

`psql < schema.sql`

Nyt voit käynnistää sovelluksen komennolla

`flask run`

Testaaminen tulee aloittaa seuraavasti:
- Luo uusi käyttäjä
- Luo uusi bändi
- Luo uusia biisejä (tällä hetkellä sovelluksessa biiseistä puuttuu id bändiin, joka tullaan päivittämään)
- Luo uusi keikka ja keikkapaikka
- Luo keikalle settilista

Seuraavaksi tarkoituksena on lisätä vielä puuttuvat määritellyt ominaisuudet ja parannella toiminnallisuutta ja ulkoasua. Tällä hetkellä funktiot ovat app -tiedostossa ja sovelluksen rakennetta on syytä selkeyttää eri toiminnallisuuksiin.

