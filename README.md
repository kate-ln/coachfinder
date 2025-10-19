   # Sovellus valmentajan ja valmennettavien hakuun

   Sovelluksessa voidaan hakea valmentajia tai valmennettavia. Sovelluksen kohderyhmät ovat siten
   1) nuoret ja aikuiset oppilaat, jotka haluavat löytää henkilökohtaisen valmentajan tiettyyn yksilö- tai pariurheiluun, esimerkiksi tennikseen tai pikajuoksuun, sekä
   2) valmentajat, jotka etsivät uusia valmennettavia omaan lajiinsa.
   Oppilaan ilmoituksessa selviää henkilön ikäryhmä, paikkakunta, laji ja taitotaso, jonka harjoitteluun haetaan valmentajaa, ja valmentajan ilmoituksessa tämän paikkakunta, laji sekä kokemustaso.

   Sovelluksen ominaisuuksia ovat:
   1. Käyttäjät, sekä oppilaat että valmentajat, voivat luoda uuden tunnuksen ja kirjautua sillä sisään ja ulos.
   2. Oppilaskäyttäjä näkee aiemmin luodut valmentajailmoitukset listana ja voi hakea niitä paikkakunnittain ja lajeittain; vastaavasti valmentajakäyttäjä näkee aiemmat oppilasilmoitukset listana ja voi hakea niitä lajin ja muiden ominaisuuksien mukaan.
   3. Molemmat käyttäjät voivat lisätä uuden ilmoituksen ja muokata tai poistaa aiemmin luodun ilmoituksen.
   4. Kun sopiva valmentaja tai valmennettava löytyy, nämä sopivat yksityiskohdista viestitse. Mikäli uutta valmentajaa tai valmennettavaa ei enää tarvita, molemmat käyttäjät voivat siirtää ilmoituksen joko "toistaiseksi löydetty" -ryhmään tai poistaa ilmoituksensa.
   Tässä pääasiallinen tietokohde on ilmoitus ja toissijainen tietokohde on viestihistoria.

   Sovelluksen tämänhetkinen vaihe sisältää seuraavat toiminnot:
   ### Toteutetut ominaisuudet
   **Käyttäjähallinta**:
   - Käyttäjärekisteröinti ja kirjautuminen
   - Salasanojen hashaus (Werkzeug)
   - Käyttäjäsessiot ja autentikointi
   - Käyttäjien näyttönimet
   - Käyttäjäprofiilit (oma ja muiden käyttäjien profiilit)
   - Uloskirjautuminen

   **Oppilasilmoitukset**:
   - Ilmoitusten luominen, muokkaaminen ja poistaminen
   - Ilmoitusten listaus etusivulla
   - Ilmoitusten haku vapaalla hakusanalla
   - Ilmoitusten yksityiskohtainen katselu
   - Oikeuksien tarkastaminen (vain omien ilmoitusten muokkaus/poisto)
   - Valintalistojen hallinta (ikäryhmä, taitotaso, laji, paikkakunta)
   - Ilmoitusten tilan hallinta (aktiivinen/löydetty)
   - Parannettu haku (ilmoitustyypin valinta, aktiivisten suodatus)
   - **"Valmentaja löydetty" -toiminto**: Ilmoituksen omistaja voi merkitä ilmoituksen löydetyksi, jolloin se näkyy "Valmentaja löydetty" -merkillä kaikissa listoissa ja hauissa

   **Viestitys**:
   - Yksityisviestien lähettäminen käyttäjien välillä
   - Viestiketjujen hallinta ja luominen
   - Viestiketjujen listaus
   - Viestien lukeminen ja vastaaminen
   - Viestien pituuden validaatio (max 2000 merkkiä)

   **Profiilikuvien hallinta**:
   - Kuvien lataaminen (.jpg-tiedostot, max 100KB)
   - Kuvien näyttäminen
   - Kuvien muokkaaminen (korvaaminen)
   - Kuvien poistaminen vahvistussivulla
   - BLOB-tallennus tietokantaan

   **Turvallisuusominaisuudet**:
   - CSRF-suojaus kaikille POST-pyynnöille
   - Palvelinpuolen validaatio valintalistojen arvoille
   - XSS-suojaus (MarkupSafe)
   - SQL-injektion esto (parametrisoidut kyselyt)
   - Salasanojen hashaus
   - Sessioiden hallinta
   - Käyttöoikeuksien tarkastaminen

   **Käyttöliittymä**:
   - Yhtenäinen CSS-tyylitysjärjestelmä (layout.html + main.css)
   - Responsiivinen design
   - Keskitetty virheenkäsittely (ui.py)
   - Flash-viestit käyttäjälle
   - Navigaatiojärjestelmä
   - Lomakkeiden validaatio ja virheenkäsittely
   - Visuaaliset ilmoitustilan indikaattorit (löydetty/aktiivinen)

   **Valmentajailmoitukset**:
   - Valmentajailmoitusten luominen, muokkaaminen ja poistaminen
   - Valmentajailmoitusten listaus etusivulla
   - Valmentajailmoitusten haku vapaalla hakusanalla
   - Valmentajailmoitusten yksityiskohtainen katselu
   - Oikeuksien tarkastaminen (vain omien ilmoitusten muokkaus/poisto)
   - Kokemustason valintalistojen hallinta
   - Ilmoitustyypin valinta (oppilas vs valmentaja)
   - Ilmoitusten tilan hallinta (aktiivinen/löydetty)

   **Tilastot profiilisivulla**
   - Ilmoitusten määrä kategorioittain (oppilasilmoitukset ja valmentajailmoituket)
   - Opplilaiden ikäryhmien jakauma ja maininta oman ikäryhmän osuudesta, mikäli käyttäjällä on       oppilasilmoituksia
     
   ## Yhteenveto
   Sovellus sisältää:
   - **Käyttäjähallinnan** rekisteröinnistä profiilien hallintaan
   - **Viestijärjestelmän** käyttäjien väliseen turvalliseen kommunikointiin
   - **Ilmoitusjärjestelmän** oppilaiden valmentajahakuun
   - **Profiilikuvien hallinnan** käyttäjäkokemuksen parantamiseksi
   - **Turvallisuusmallin** CSRF-, XSS- ja SQL-injektion suojauksella
   - **Yhtenäisen käyttöliittymän** responsiivisella suunnittelulla
   - **Ilmoitustilan hallinnan** aktiivisten ja löydettyjen ilmoitusten seurantaan
   - **Parannetun hakutoiminnon** ilmoitustyypin valinnalla ja aktiivisten suodatuksella

   ## Tietokannan rakenne
   ### Taulut
   1. **users**
      - `id` (PRIMARY KEY)
      - `username` (UNIQUE, max 16 merkkiä)
      - `password_hash` (Werkzeug hash)
      - `display_name` (näyttönimi, max 50 merkkiä)
      - `image` (BLOB - profiilikuva, max 100KB)

   2. **announcements_student**
      - `id` (PRIMARY KEY)
      - `sport` (laji)
      - `city` (paikkakunta)
      - `age_group` (ikäryhmä)
      - `skill_level` (taitotaso)
      - `description` (kuvaus)
      - `user_id` (viittaus users-tauluun)
      - `found` (löydetty-status, 0=aktiivinen, 1=löydetty)

   3. **threads**
      - `id` (PRIMARY KEY)
      - `user_a_id`, `user_b_id` (viittaukset users-tauluun)
      - `created_at` (datetime)
      - UNIQUE(user_a_id, user_b_id) - estää duplikaattiketjut

   4. **messages**
      - `id` (PRIMARY KEY)
      - `thread_id` (viittaus threads-tauluun, CASCADE DELETE)
      - `sender_id` (viittaus users-tauluun)
      - `body` (viestin sisältö, max 2000 merkkiä)
      - `created_at` (datetime)

   5. **classes**
      - `id` (PRIMARY KEY)
      - `title` (esim. "Ikäryhmä", "Taitotaso", "Laji", "Paikkakunta")
      - `value` (esim. "10-15 vuotta", "Aloittelija", "Tennis", "Helsinki")

   6. **announcements_coach**
      - `id` (PRIMARY KEY)
      - `sport` (laji)
      - `city` (paikkakunta)
      - `experience_level` (kokemustaso)
      - `description` (kuvaus)
      - `user_id` (viittaus users-tauluun)
      - `found` (löydetty-status, 0=aktiivinen, 1=löydetty)

   7. **announcement_classes**
      - `id` (PRIMARY KEY)
      - `announcement_id` (viittaus announcements_student-tauluun)
      - `title` (esim. "Ikäryhmä")
      - `value` (esim. "10-15 vuotta")

   8. **announcement_classes_coach**
      - `id` (PRIMARY KEY)
      - `announcement_id` (viittaus announcements_coach-tauluun)
      - `title` (esim. "Kokemus")
      - `value` (esim. "Ammattilainen")
        
   ## Asennus ja käynnistys
   ### 1. Ympäristön valmistelu

   ```bash
   # Kloonaa repositorio
   git clone <repository-url>
   cd coachfinder

   # Luo virtual environment
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # tai Windows:
   # venv\Scripts\activate
   ```

   ### 2. Tietokannan alustus
   
   **Suositeltu tapa (automaattinen):**
   ```bash
   # Luo tietokanta ja täytä se alkuperäisellä datalla
   python3 setup_database.py
   ```
   
   Tämä skripti:
   - Luo tietokannan rakenteen (`schema.sql`)
   - Täyttää `classes`-taulun pudotusvalikkojen tiedoilla
   - Sisältää ikäryhmät, taitotasot ja kokemustasot
   - Tarkistaa onko data jo olemassa (ei ylikirjoita)
   
   **Vaihtoehtoinen tapa (manuaalinen):**
   ```bash
   # Luo tietokanta schema.sql-tiedoston perusteella
   sqlite3 database.db < schema.sql
   # Täytä classes-taulun tiedot (Tärkeää)
   sqlite3 database.db < init.sql
   ```
   
   **HUOM:** Ilman `init.sql`-tiedoston suorittamista pudotusvalikot (ikäryhmä, taitotaso, kokemustaso) ovat tyhjät

   ### 3. Sovelluksen käynnistys
   ```bash
   # Aktivoi virtual environment (jos ei jo aktivoitu)
   source venv/bin/activate
   # Asenna Flask-kirjasto
   pip install flask
   # Käynnistä Flask-sovellus
   flask run
   ```
   Sovellus käynnistyy osoitteessa: `http://localhost:5000`

   ## Vianmääritys
   
   ### Pudotusvalikot ovat tyhjät
   Jos ilmoituslomakkeiden pudotusvalikot (ikäryhmä, taitotaso, kokemustaso) näkyvät tyhjänä:
   
   ```bash
   # Suorita setup-skripti uudelleen
   python3 setup_database.py
   ```
   
   Tai manuaalisesti:
   ```bash
   # Täytä classes-taulun tiedot
   sqlite3 database.db < init.sql
   ```

   ## Käytettävissä olevat ominaisuudet
   ### Käyttäjähallinta
   - **Rekisteröityminen**: `/register` (GET/POST)
   - **Tunnuksen luominen**: `/create` (POST) - ohjaa rekisteröintiin
   - **Kirjautuminen**: `/login` (GET/POST) - tukee next_page parametria
   - **Oma profiili**: `/profile` (GET/POST) - näyttönimen asettaminen ja profiilikuvien hallinta
   - **Muiden käyttäjien profiilit**: `/profile/<user_id>` (GET)
   - **Profiilikuvan lisääminen**: `/add_image` (GET/POST)
   - **Profiilikuvan poistaminen**: `/confirm_delete_image` (GET) → `/delete_image` (POST)
   - **Profiilikuvan näyttäminen**: `/image/<user_id>` (GET)
   - **Uloskirjautuminen**: `/logout` (GET)

   ### Ilmoitukset (Oppilaat)
   - **Etusivu**: `/` (GET) - Näyttää kaikki oppilasilmoitukset
   - **Uusi ilmoitus**: `/create_announcement_student` (GET/POST)
   - **Ilmoituksen katselu**: `/announcement/<id>` (GET)
   - **Ilmoituksen muokkaus**: `/edit_announcement/<id>` (GET)
   - **Ilmoituksen päivitys**: `/update_announcement_student` (POST)
   - **Ilmoituksen poisto**: `/remove_announcement/<id>` (GET/POST)
   - **Haku**: `/find_announcement` (GET) - tukee query, search_type ja active_only parametreja

   ### Viestijärjestelmä
   - **Viestiketjut**: `/messages` (GET) - listaa käyttäjän viestiketjut
   - **Uusi viesti**: `/messages/new` (GET/POST) - uuden viestiketjun luominen
   - **Keskustelu**: `/messages/<thread_id>` (GET/POST) - viestiketjun lukeminen ja vastaaminen
   - 
   ### Parannettu hakutoiminto
   - **Hakutyyppi**: Valitse haku oppilasilmoituksista tai valmentajailmoituksista
   - **Aktiivisten suodatus**: Näytä vain aktiiviset ilmoitukset (ei löydettyjä)
   - **Visuaaliset indikaattorit**: Löydetyt ilmoitukset merkitty vihreällä "Löydetty" -merkillä
     
   ### Koodin Rakenne
   - **`app.py`**: Flask-reitit ja sovelluslogiikka, CSRF-suojaus, autentikointi
   - **`db.py`**: Tietokantayhteydet ja peruskyselyoperaatiot
   - **`announcements_student.py`**: Oppilasilmoitusten CRUD-operaatiot
   - **`users.py`**: Käyttäjien tietokantaoperaatiot (profiilit, autentikointi, kuvat)
   - **`messages.py`**: Viestien ja viestiketjujen tietokantaoperaatiot
   - **`ui.py`**: UI-apufunktiot, virheenkäsittely ja sivujen renderöinti
   - **`config.py`**: Sovelluksen konfiguraatio (secret key)
   - **`templates/layout.html`**: Yhteinen sivupohja kaikille sivuille
   - **`static/main.css`**: Yhtenäinen CSS-tyylitysjärjestelmä
   - **`schema.sql`**: Tietokannan rakenne
   - **`init.sql`**: Tietokannan alustusdata

   ### Tekninen arkkitehtuuri
   - **Backend**: Flask (Python web framework)
   - **Tietokanta**: SQLite3 (tiedostopohjainen)
   - **Templating**: Jinja2 (Flask:n mukana)
   - **Turvallisuus**:
      - Werkzeug salasanojen hashaukseen
      - MarkupSafe XSS-suojaukseen
      - CSRF-tokenit Cross-Site Request Forgery -hyökkäyksiä vastaan
   - **Sessiot**: Flask-sessiot (cookies)
   - **Staattiset tiedostot**: CSS-tyylitiedostot
   - **Tiedostojen käsittely**: BLOB-tallennus tietokantaan
     
   ### Testaus
   #### Perustoiminnot
   1. **Käyttäjähallinta**:
      - Rekisteröidy ainakin kolmena eri käyttäjänä
      - Kirjaudu sisään eri käyttäjinä, testaa väärät tunnukset
      - Aseta näyttönimi profiilissa
      - Testaa uloskirjautuminen

   2. **Ilmoitukset**:
      - Luo muutama erilainen oppilasilmoitus ja valmentajailmoitus
      - Hae ilmoituksia hakusanalla (testaa sekä oppilas- että valmentajailmoituksia)
      - Testaa hakutyypin valintaa (oppilas vs valmentaja)
      - Testaa aktiivisten suodatusta (näytä vain aktiiviset)
      - Muokkaa ja poista omia ilmoituksia
      - Testaa toisen käyttäjän ilmoitusten muokkausyritysta (403 virhe)

   3. **Viestijärjestelmä**:
      - Lähetä viesti toiselle käyttäjälle
      - Testaa että vastaanottaja näkee viestin
      - Testaa että viestiketjut eri käyttäjien kanssa näkyvät listana
      - Testaa virheellisiä viestejä (tyhjä viesti, olematon käyttäjä)

   4. **Profiilikuvat**:
      - Lataa profiilikuva (.jpg)
      - Testaa väärä tiedostomuoto (.png) → virhe
      - Testaa liian suuri tiedosto → virhe
      - Muokkaa kuvaa (korvaa uudella)
      - Poista kuva vahvistussivulla

   #### Turvallisuustestaus
   5. **CSRF-suojaus**:
      - Poista CSRF-token lomakkeesta kehittäjätyökaluilla
      - Lähetä lomake → 403 Forbidden virhe

   6. **Valintalistojen validaatio**:
      - Muokkaa `<select>` elementtiä lisäämällä uusi `<option>`
      - Lähetä lomake → "VIRHE: virheellinen ikäryhmä"

   7. **Käyttöoikeuksien testaus**:
      - Yritä muokata toisen käyttäjän ilmoitusta → 403 virhe
      - Yritä päästä toisen käyttäjän viestiketjuun → 403 virhe

   8. **XSS- ja SQL-injektion testaus**:
      - Syötä `<script>alert('XSS')</script>` kenttiin
      - Syötä `'; DROP TABLE users; --` kenttiin
      - Tarkista, että kaikki syötteet koodataan oikein kontekstissaan ja että SQL:ssa käytetään parametrisoituja kyselyjä.
        
   #### Parannettu hakutoiminto
   9. **Hakutyypin valinta**:
      - Testaa "Etsin valmennettavia" -valintaa
      - Testaa "Etsin valmentajaa" -valintaa
      - Varmista että hakutulokset vastaavat valittua tyyppiä

   10. **Aktiivisten suodatus**:
       - Merkitse jokin ilmoitus löydetyksi
       - Testaa "Näytä vain aktiiviset" -valintaa
       - Varmista että löydetyt ilmoitukset eivät näy suodatetussa haussa

   11. **Visuaaliset indikaattorit**:
        - Tarkista että löydetyt ilmoitukset näkyvät vihreällä "Löydetty" -merkillä
        - Testaa että aktiiviset ilmoitukset eivät näytä merkintää
          
   ## Turvallisuusominaisuudet
   ### CSRF-suojaus
   - **CSRF-tokenit**: Kaikki POST-pyynnöt vaativat voimassa olevan CSRF-tokenin
   - **Token-generointi**: Uusi token luodaan kirjautumisen yhteydessä
   - **Token-validaatio**: `check_csrf()` funktio tarkistaa tokenin oikeellisuuden
   - **Suojatut reitit**: Kaikki lomakkeet (ilmoitukset, viestit, profiilit, kuvat) suojattu

   ### Palvelinpuolen validaatio
   - **Valintalistojen validaatio**: `age_group` ja `skill_level` arvot tarkistetaan tietokannasta
   - **Tiedostomuodon validaatio**: Profiilikuvat vain .jpg-tiedostoja
   - **Tiedostokoon validaatio**: Kuvat max 100KB
   - **Tekstikenttien validaatio**:
   - Käyttäjätunnus max 16 merkkiä
   - Näyttönimi max 50 merkkiä
   - Viestit max 2000 merkkiä

   ### Autentikointi ja autorisointi
   - **Salasanojen hashaus**: Werkzeug-kirjaston `generate_password_hash()` ja `check_password_hash()`
   - **Sessioiden hallinta**: Flask-sessiot käyttäjätunnistukseen
   - **Käyttöoikeuksien tarkastaminen**:
   - Vain omien ilmoitusten muokkaus/poisto
   - Vain viestiketjun osallistujien pääsy keskusteluihin
   - Vain kirjautuneiden käyttäjien pääsy suojattuihin sivuihin

   ### XSS- ja SQL-injektion esto
   - **XSS-suojaus**: MarkupSafe-kirjasto automaattiselle HTML-escape:lle
   - **SQL-injektion esto**: Parametrisoidut kyselyt kaikissa tietokantaoperaatioissa
   - **Input-sanitointi**: Kaikki käyttäjäsyötteet puhdistetaan (`strip()`)

   ### Estetyt hyökkäykset
   - **XSS-injektio**: `<script>alert('XSS')</script>` ikäryhmänä
   - **SQL-injektio**: `'; DROP TABLE users; --` taitotasona
   - **CSRF-hyökkäykset**: Väärennettyjen lomakkeiden lähettäminen
   - **Tietojen korruptio**: Virheellisten valintalistojen arvojen syöttäminen
   - **Tiedostojärjestelmän hyökkäykset**: Vain sallittujen tiedostomuotojen lataaminen

   ### Testaus
   1. **CSRF-suojaus**:
      - Poista CSRF-token lomakkeesta kehittäjätyökaluilla
      - Lähetä lomake → 403 Forbidden virhe

   2. **Valintalistojen validaatio**:
      - Muokkaa `<select>` elementtiä lisäämällä uusi `<option>`
      - Lähetä lomake → "VIRHE: virheellinen ikäryhmä"

   3. **Käyttöoikeuksien testaus**:
      - Yritä muokata toisen käyttäjän ilmoitusta → 403 virhe
      - Yritä päästä toisen käyttäjän viestiketjuun → 403 virhe

   4. **Tiedostojen validaatio**:
      - Lataa .png-kuva → "VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto"
      - Lataa liian suuri kuva → "VIRHE: Lähettämäsi tiedosto on liian suuri"

   ## Profiilikuvien hallinta
   ### Yleiskuvaus
   Sovellus tukee käyttäjien profiilikuvien lataamista, näyttämistä, muokkaamista ja poistamista. Kuvat tallennetaan tietokantaan BLOB-muodossa ja näytetään JPEG-kuvina.

   ### Tietokantamuutokset
   #### Users-taulun päivitys
   Lisätty `image` sarake BLOB-tyyppinä profiilikuvien tallentamista varten.

   ### Backend-toteutus
   #### 1. Tietokantafunktiot (`users.py`)
   Lisätty funktiot: `get_user()` (hakee käyttäjätiedot ja tiedon kuvien olemassaolosta), `update_image()` (päivittää profiilikuvan), `get_image()` (hakee profiilikuvan) ja `delete_image()` (poistaa profiilikuvan).

   #### 2. Flask-reitit (`app.py`)
   Lisätty reitit: `/add_image` (kuvan lataaminen), `/image/<user_id>` (kuvan näyttäminen), `/confirm_delete_image` (vahvistussivu) ja `/delete_image` (kuvan poistaminen). Kuvien validaatio tarkistaa tiedostomuodon (.jpg) ja koon (max 100KB).

   ### Frontend-toteutus
   #### 1. Kuvan lataussivu (`templates/add_image.html`)
   Lomake tiedostovalitsimella .jpg-tiedostoille, ohjeistus koolle ja muodolle, sekä takaisin-profiiliin -linkki.

   #### 2. Profiilisivun päivitys (`templates/profile.html`)
   Ehdollinen näyttö: jos kuva on olemassa, näytetään kuva "Muuta kuvaa" ja "Poista kuva" -linkkeineen. Jos kuvaa ei ole, näytetään "Lisää profiilikuva" -linkki. "Poista kuva" -linkki vie vahvistussivulle.

   #### 3. Vahvistussivu (`templates/confirm_delete_image.html`)
   Vahvistussivu kuvan poistamiseen, joka sisältää vahvistuslomakkeen ja peruuta-linkin.

   #### 4. Muiden käyttäjien profiilisivun päivitys (`templates/user_profile.html`)
   Ehdollinen näyttö: jos käyttäjällä on profiilikuva, se näytetään responsiivisena kuvana pyöristetyillä kulmilla.

   ### Ominaisuudet
   #### Kuvan lataaminen
   - **Tiedostomuoto**: Vain .jpg-tiedostot hyväksytään
   - **Koko**: Enintään 100KB
   - **Validaatio**: Server-side tarkistus tiedostomuodolle ja koolla
   - **Tallennus**: BLOB-muodossa tietokantaan

   #### Kuvan näyttäminen
   - **URL-muoto**: `/image/<user_id>`
   - **Content-Type**: `image/jpeg`
   - **Käsittely**: 404-virhe jos kuvaa ei ole
   - **Styling**: Responsiivinen, pyöristetyt kulmat

   #### Kuvan hallinta
   - **Muokkaaminen**: "Muuta kuvaa" -linkki vie lataussivulle
   - **Poistaminen**: "Poista kuva" -linkki vie vahvistussivulle
   - **Vahvistus**: Erillinen vahvistussivu estää vahingolliset poistot

   ### Turvallisuusominaisuudet
   #### Validaatio
   - Tiedostomuodon tarkistus (.jpg)
   - Tiedostokoon rajoitus (100KB)
   - Palvelinpuolen validaatio (ei voi ohittaa)

   #### Käyttöoikeudet
   - Vain kirjautuneet käyttäjät voivat ladata kuvia
   - Käyttäjät voivat muokata vain omia kuviaan
   - Kuvien näyttäminen kaikille käyttäjille

   #### Tietoturvallisuus
   - BLOB-tallennus (ei tiedostojärjestelmää)
   - Sisältötyyppi oikein asetettu
   - 404-virhe olemattomille kuville

   ### Testaus
   #### Perustoiminnot
   1. **Kuvan lataaminen**:
      - Lataa .jpg-kuva profiiliin
      - Tarkista että kuva näkyy profiilisivulla
      - Testaa väärä tiedostomuoto (.png) → virhe
      - Testaa liian suuri kuva → virhe

   2. **Kuvan muokkaaminen**:
      - Klikkaa "Muuta kuvaa" -linkkiä
      - Lataa uusi kuva
      - Tarkista että vanha kuva korvautuu

   3. **Kuvan poistaminen**:
      - Klikkaa "Poista kuva" -linkkiä
      - Vahvista poisto vahvistussivulla
      - Tarkista että kuva poistuu profiilisivulta

   4. **Kuvan näyttäminen**:
      - Mene toisen käyttäjän profiilisivulle
      - Tarkista että kuva näkyy oikein
      - Testaa suora URL `/image/<user_id>`

   #### Virhetilanteet
   - Väärä tiedostomuoto
   - Liian suuri tiedosto
   - Olemattoman käyttäjän kuva
   - Vahvistussivun toiminta

   ### Käyttöliittymä
   #### Profiilisivu (oma)
   - **Ei kuvaa**: "Ei profiilikuvia | Lisää profiilikuva"
   - **On kuva**: Kuva + "Muuta kuvaa | Poista kuva"

   #### Profiilisivu (muut)
   - **Ei kuvaa**: Ei näytetä mitään
   - **On kuva**: Kuva näytetään

   #### Lataussivu
   - Tiedostovalitsin (.jpg)
   - Ohjeistus koolle ja muodolle
   - Lähetä-painike
   - Takaisin-profiiliin -linkki

   #### Vahvistussivu
   - Vahvistusteksti
   - Vahvista-painike
   - Peruuta-linkki
   - **Kuvan poisto**: `/confirm_delete_image` -sivu vahvistuslomakkeineen
   - **Ilmoituksen poisto**: `/remove_announcement/<id>` -sivu vahvistuslomakkeineen

   #### Käyttöliittymä
   - Lomakkeet lähetetään suoraan palvelimelle
   - Vahvistukset tehdään erillisillä sivuilla
   - Navigaatio toimii pelkästään linkeillä

   ## Yhtenäinen CSS-tyylitysjärjestelmä
   ### Tiedostorakenne
   #### 1. Layout-sivupohja (`templates/layout.html`)
   Yhteinen sivupohja kaikille sivuille, joka sisältää header-osion (otsikko), nav-osion (navigaatio) ja content-osion (sivun sisältö). CSS-tiedosto linkitetty head-osiossa.

   #### 2. CSS-tyylitiedosto (`static/main.css`)
   Yhtenäinen tyylitysjärjestelmä, joka määrittelee sivun asettelun (keskitys, maksimileveys), värit ja fontin (sans-serif).

   ### Sivurakenne
   #### Kolme pääosiota
   1. **Otsikko** (`.header`)
   2. **Navigaatio** (`.nav`)
   3. **Sisältö** (`.content`)

   #### Navigaatio
   - Keskitytetty asettelu
   - Riviin asetellut elementit
   - Pystyviivat erottimina
   - Ehdollinen sisältö kirjautumisen mukaan

   ### Tyylitetyt komponentit
   - Ilmoitukset (`.announcement`)
   - Viestiketjut (`.thread`)
   - Viestit (`.message`)
   - Profiilitiedot (`.profile-info`)

   ### Lomakkeiden tyylitys
   - Syöttökentät: Responsiivinen leveys (max 30em), pyöristetyt kulmat, sopiva sisennys.
   - Painikkeet: Pyöristetyt kulmat, osoitin päällä -efekti.

   ### Template-päivitykset
   #### Kaikki sivut käyttävät layout.html:ia
   - `{% extends "layout.html" %}`
   - `{% block title %}Sivun otsikko{% endblock %}`
   - `{% block content %}Sivun sisältö{% endblock %}`

   #### Poistettu vanha navigaatio
   - `_nav.html` poistettu
   - Navigaatio integroitu layout.html:iin

   ### Responsiivisuus
   #### Keskitys ja leveys
   - `margin: auto` keskittää sisällön
   - `max-width: 50em` rajoittaa maksimileveyden
   - `font-family: sans-serif` moderni fontti

   #### Navigaatio
   - `text-align: center` keskittää navigaation
   - `display: inline-block` vierekkäiset linkit
   - Negatiivinen marginaali korjaa välit

   ### Värit ja ulkoasu
   - **Tausta**: Vaaleanvihreä (`#f0f8f0`)
   - **Otsikko**: Tummanharmaa tausta (`#2c3e50`), vaaleanharmaa teksti (`#ecf0f1`)
   - **Navigaatio**: Vaaleansininen tausta (`#e6f7ff`), tummanharmaa reunus (`#2c3e50`)
   - **Sisältö**: Valkoinen tausta, harmaa reunus (`#bdc3c7`)
   - **Reunukset**: Harmaan sävyjä (`#95a5a6`, `#7f8c8d`)
   - **Painikkeet**: Vihreä (`#27ae60`)
   - **Korostukset**: Vihreä (`#27ae60`, `#2ecc71`)

## Saavutettavuus ja tekstipohjaiset selaimet
### Lynx-yhteensopivuus
Sovellus on suunniteltu toimimaan tekstipohjaisilla selaimilla kuten Lynx:lla. Kaikki toiminnot ovat käytettävissä ilman JavaScriptiä tai CSS:ää.

#### Lynx-testaus
```bash
# Asenna Lynx (Ubuntu/Debian)
sudo apt-get install lynx

# Käynnistä sovellus
flask run

# Testaa Lynx:lla toisessa terminaalissa
lynx http://localhost:5000
```
#### Lynx-yhteensopivat ominaisuudet
- **Navigaatio**: Kaikki linkit toimivat Lynx:lla
- **Lomakkeet**: Kaikki lomakkeet toimivat tekstipohjaisesti
- **Viestit**: Viestien lähettäminen ja lukeminen toimii
- **Haku**: Hakutoiminto toimii tekstipohjaisesti
- **Profiilit**: Käyttäjäprofiilien katselu toimii (kuvat näkyvät linkkeinä)

### Saavutettavuusominaisuudet
#### Semanttinen HTML-rakenne
- **Otsikot**: Hierarkkinen otsikkorakenne (h1, h2, h3)
- **Navigaatio**: `<nav>` elementti päävalikolle
- **Lomakkeet**: Oikeat `<label>` elementit syöttökentille
- **Listat**: `<ul>` ja `<li>` elementit navigaatiolle
- **Pääsisältö**: `<main>` elementti sivun sisällölle

#### Näyttöluettavien ominaisuudet
- **Alt-tekstit**: Profiilikuville alt-tekstit (jos kuvaa ei voi näyttää)
- **Linkkitekstit**: Kuvaavat linkkitekstit ("Muokkaa ilmoitusta", "Poista kuva")
- **Lomakkeiden ohjeistus**: Selkeät ohjeet lomakkeiden täyttämiseen
- **Virheviestit**: Selkeät virheviestit käyttäjälle

#### Näppäimistönavigaatio
- **Tab-navigaatio**: Kaikki interaktiiviset elementit saavutettavissa Tab-näppäimellä
- **Enter-näppäin**: Lomakkeiden lähettäminen Enter-näppäimellä
- **Linkkien aktivointi**: Kaikki linkit aktivoidaan Enter-näppäimellä

#### Värikontrasti ja visuaalinen saavutettavuus
- **Korkea kontrasti**: Tummat tekstit vaalealla taustalla
- **Värisokeus**: Ei riipu pelkästään väreistä (teksti + väri)
- **Fonttikoko**: Luettava fonttikoko (sans-serif)
- **Riviväli**: Sopiva riviväli lukemisen helpottamiseksi

### Tekstipohjaisten selaimien testaus
#### Lynx-komennot
- **Navigointi**: Nuolinäppäimet, Enter, q (poistu)
- **Linkkien valinta**: Nuolinäppäimet linkkien välillä
- **Takaisin**: Left-nuoli tai Backspace
- **Haku**: / (hakukenttään)

#### Testattavat toiminnot Lynx:lla
1. **Rekisteröityminen ja kirjautuminen**
2. **Ilmoitusten luominen ja muokkaaminen**
3. **Viestien lähettäminen**
4. **Hakutoiminto**
5. **Profiilien katselu**
6. **Navigaatio sivujen välillä**

### Saavutettavuusstandardit
Sovellus noudattaa WCAG 2.1 AA -tason suosituksia:
- **Perceptible**: Sisältö on havaittavissa eri tavoilla
- **Operable**: Käyttöliittymä on käytettävissä eri tavoilla
- **Understandable**: Sisältö ja käyttöliittymä ovat ymmärrettäviä
- **Robust**: Sisältö on yhteensopiva eri teknologioiden kanssa

### Testaus
#### Visuaalinen tarkistus

1. **Yhtenäisyys**: Kaikki sivut noudattavat samaa tyyliä
2. **Navigaatio**: Toimii kaikilla sivuilla
3. **Responsiivisuus**: Toimii eri näytöillä
4. **Komponentit**: Ilmoitukset, viestit, lomakkeet tyylitetty

#### Lisätyylit
- Virheviestit (`.error`, `.success`)
- Profiilikuvat (`.profile-image`)
- Metatiedot (`.meta`)
  
## Suorituskykytestaus suurella tietomäärällä
### Testausasetus
Sovelluksen suorituskykyä testattiin suurella tietomäärällä seuraavalla konfiguraatiolla:
- **Käyttäjät**: 1,000
- **Viestiketjut**: 100,000  
- **Viestit**: 1,000,000
- **Oppilasilmoitukset**: 1,000
- **Valmentajailmoitukset**: 1,000

### Testatut skenaariot
#### 1. Sivutus (Pagination)
Sivutuksen toteutus estää sovelluksen jumiutumisen suurella tietomäärällä. Ilman sivutusta sovellus yrittäisi näyttää kaikki 100,000+ ilmoitusta kerralla.

**Toteutus:**
- Sivukoko: 10 ilmoitusta per sivu
- URL-muoto: `/` (sivu 1) ja `/<page>` (muut sivut)
- SQL-kyselyt käyttävät `LIMIT` ja `OFFSET` -lauseita

#### 2. Tietokannan indeksit
Suorituskykytestauksessa testattiin sovelluksen toimintaa ilman ja tietokannan indeksien kanssa.
**Lisätyt indeksit:**
```sql
CREATE INDEX idx_messages_thread_id ON messages (thread_id);
CREATE INDEX idx_messages_sender_id ON messages (sender_id);
CREATE INDEX idx_threads_user_a_id ON threads (user_a_id);
CREATE INDEX idx_threads_user_b_id ON threads (user_b_id);
CREATE INDEX idx_announcements_student_user_id ON announcements_student (user_id);
CREATE INDEX idx_announcements_coach_user_id ON announcements_coach (user_id);
CREATE INDEX idx_announcements_student_found ON announcements_student (found);
CREATE INDEX idx_announcements_coach_found ON announcements_coach (found);
```
#### 3. Suorituskykymittaukset
**Ilman indeksejä:**
- Etusivu (keskiarvo): 0.007s
- Sivutus (keskiarvo): 0.006s  
- Haku (keskiarvo): 0.018s
- **Kokonaiskeskiarvo: 0.010s**

**Indekseillä:**
- Etusivu (keskiarvo): 0.010s
- Sivutus (keskiarvo): 0.006s
- Haku (keskiarvo): 0.017s
- **Kokonaiskeskiarvo: 0.011s**

#### 4. Havainnot
**Positiiviset tulokset:**
- Sovellus toimii hyvin suurella tietomäärällä
- Sivutus estää käyttöliittymän jumiutumisen
- Kaikki sivupyynnöt vastaavat alle 0.1 sekunnissa
- Hakutoiminto toimii tehokkaasti

**Yllättävät tulokset:**
- Indeksien vaikutus oli minimaalinen tässä testissä
- Sovellus oli jo hyvin optimoitu ilman indeksejä
- SQLite3 käsittelee pieniä kyselyjä tehokkaasti

**Suorituskykyn parannukset:**
- Sivutuksen lisääminen estää sovelluksen jumiutumisen
- Indeksit parantavat suorituskykyä suuremmilla kyselyillä
- Tehokkaat SQL-kyselyt ovat kriittisiä suorituskyvylle

### Testausskriptit
**Testidatan luominen:**
```bash
python3 generate_large_test_data.py
```
**Indeksien lisääminen:**
```bash
python3 add_indexes.py
```
**Indeksien poistaminen:**
```bash
python3 remove_indexes.py
```
**Suorituskykytestaus:**
```bash
python3 test_detailed_performance.py
```
### Yhteenveto
Sovellus toimii erinomaisesti suurella tietomäärällä. Sivutuksen toteutus on kriittinen ominaisuus, joka estää käyttöliittymän jumiutumisen. Tietokannan indeksit parantavat suorituskykyä, vaikka vaikutus oli tässä testissä minimaalinen. Sovellus on valmis tuotantokäyttöön suurella käyttäjäkunnalla.

## Valmentajailmoitusten toteutus
### Yleiskuvaus
Sovellus tukee nyt valmentajailmoitusten luomista, muokkaamista, poistamista ja katselua. Valmentajat voivat ilmoittaa etsivänsä valmennettavia omaan lajiinsa.

### Tietokantamuutokset
#### Uudet taulut
1. **announcements_coach**: Valmentajailmoitusten päätaulu
2. **announcement_classes_coach**: Valmentajailmoitusten luokittelutiedot

### Backend-toteutus
#### 1. Tietokantafunktiot (`announcements_coach.py`)
- `get_all_classes()`: Hakee kaikki luokittelutiedot
- `add_announcement()`: Luo uuden valmentajailmoituksen
- `get_announcements()`: Hakee kaikki valmentajailmoitukset
- `get_announcement()`: Hakee yksittäisen valmentajailmoituksen
- `update_announcement()`: Päivittää valmentajailmoituksen
- `remove_announcement()`: Poistaa valmentajailmoituksen
- `find_announcements()`: Hakee valmentajailmoituksia hakusanalla
- `get_announcements_by_user()`: Hakee käyttäjän valmentajailmoitukset

#### 2. Flask-reitit (`app.py`)
- `/choose_announcement_type` (GET): Ilmoitustyypin valinta
- `/create_announcement_coach` (GET/POST): Valmentajailmoituksen luominen
- `/announcement_coach/<id>` (GET): Valmentajailmoituksen katselu
- `/edit_announcement_coach/<id>` (GET): Valmentajailmoituksen muokkaus
- `/update_announcement_coach` (POST): Valmentajailmoituksen päivitys
- `/remove_announcement_coach/<id>` (GET/POST): Valmentajailmoituksen poisto

### Frontend-toteutus
#### 1. Ilmoitustyypin valinta (`templates/choose_announcement_type.html`)
Käyttäjä voi valita luodaanko oppilas- vai valmentajailmoitus. Sivulla on kaksi painiketta:
- "Etsin valmentajaa" → `/create_announcement_student`
- "Etsin valmennettavaa" → `/create_announcement_coach`
  
#### 2. Valmentajailmoituksen luomislomake (`templates/create_announcement_coach.html`)
Lomake sisältää kentät:
- Laji (vapaateksti)
- Paikkakunta (vapaateksti)
- Kokemustaso (valintalista)
- Kuvaus (vapaateksti)

#### 3. Valmentajailmoituksen näyttämissivu (`templates/show_announcement_coach.html`)
Näyttää valmentajailmoituksen tiedot ja mahdollisuuden muokata/poistaa (jos omistaja).

#### 4. Valmentajailmoituksen muokkaussivu (`templates/edit_announcement_coach.html`)
Sama lomake kuin luomisessa, mutta täytettynä olemassa olevilla tiedoilla.

#### 5. Valmentajailmoituksen poistamissivu (`templates/remove_announcement_coach.html`)
Vahvistussivu valmentajailmoituksen poistamiseen.

### Ominaisuudet
#### Valmentajailmoituksen luominen
- **Laji**: Vapaateksti (esim. "Tennis", "Uinti")
- **Paikkakunta**: Vapaateksti (esim. "Helsinki", "Tampere")
- **Kokemustaso**: Valintalista (esim. "Aloittelija", "Ammattilainen")
- **Kuvaus**: Vapaateksti, max 2000 merkkiä

#### Valmentajailmoituksen hallinta
- **Muokkaaminen**: Vain omistaja voi muokata
- **Poistaminen**: Vain omistaja voi poistaa
- **Katselu**: Kaikki käyttäjät voivat katsoa
- **Haku**: Vapaalla hakusanalla lajin, paikkakunnan, kokemustason tai kuvauksen perusteella

#### Turvallisuusominaisuudet
- **CSRF-suojaus**: Kaikki lomakkeet suojattu
- **Käyttöoikeudet**: Vain omistaja voi muokata/poistaa
- **Validaatio**: Kokemustaso tarkistetaan valintalistasta
- **XSS-suojaus**: Kaikki syötteet escapataan

### Testaus
#### Perustoiminnot

1. **Valmentajailmoituksen luominen**:
   - Mene `/choose_announcement_type`
   - Valitse "Etsin valmennettavaa"
   - Täytä lomake ja lähetä
   - Tarkista että ilmoitus näkyy etusivulla

2. **Valmentajailmoituksen muokkaaminen**:
   - Mene oman valmentajailmoituksen sivulle
   - Klikkaa "Muokkaa ilmoitusta"
   - Muokkaa tietoja ja tallenna
   - Tarkista että muutokset näkyvät

3. **Valmentajailmoituksen poistaminen**:
   - Mene oman valmentajailmoituksen sivulle
   - Klikkaa "Poista ilmoitus"
   - Vahvista poisto
   - Tarkista että ilmoitus poistuu etusivulta

4. **Hakutoiminto**:
   - Käytä hakutoimintoa etusivulla
   - Testaa eri hakusanoilla
   - Tarkista että valmentajailmoitukset löytyvät

#### Virhetilanteet
- Väärä kokemustaso valintalistasta
- Tyhjä laji tai paikkakunta
- Toisen käyttäjän ilmoituksen muokkausyritys
- CSRF-tokenin puuttuminen