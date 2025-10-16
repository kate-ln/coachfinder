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
- Käyttäjärekisteröinti ja kirjautuminen
- Oppilasilmoitusten luominen, muokkaaminen ja poistaminen
- Ilmoitusten listaus ja haku vapaalla hakusanalla
- Yksityisviestien lähettäminen käyttäjien välillä
- Viestiketjujen hallinta
- Tietokantarakenne käyttäjille, ilmoituksille ja viesteille
- Oikeuksien tarkastaminen ilmoitusten muokkaamisen ja poistamisen yhdeydessä
- Käyttäjäprofiili nimen asettamiselle ja nimen näyttäminen ilmoituksissa ja viesteissä
- Keskitetty virheenkäsittely (ui.py)
- Palvelinpuolen validointi valintalistojen arvoille (estää selaimen kehittäjätyökaluilla tehdyt HTML-muokkaukset)
- Profiilikuvien hallinta (lisää, muokkaa, poista)
- Yhtenäinen CSS-tyylitysjärjestelmä (layout.html + main.css)

### Keskeneräiset/puuttuvat ominaisuudet
- Valmentajailmoitukset (vain oppilasilmoitukset toteutettu)
- Hakusuodattimet (paikkakunta, laji)
- Ilmoitusten tilan hallinta ("löydetty" -ryhmä)
- Laaja käyttäjäprofiili (kuvaukset, yhteystiedot)

### Vaihtoehtoiset lisäominaisuudet
- Valikoi lomakkeiden syötteitä

## Tietokannan rakenne
### Taulut
1. **users**
   - `id` (PRIMARY KEY)
   - `username` (UNIQUE)
   - `password_hash`
   - `display_name`(näyttönimi)
   - `image` (BLOB - profiilikuva)
2. **announcements_student**
   - `id` (PRIMARY KEY)
   - `sport` (laji)
   - `city` (paikkakunta)
   - `age_group` (ikäryhmä)
   - `skill_level` (taitotaso)
   - `description` (kuvaus)
   - `user_id` (viittaus users-tauluun)
3. **threads**
   - `id` (PRIMARY KEY)
   - `user_a_id`, `user_b_id` (viittaukset users-tauluun)
   - `created_at`
4. **messages**
   - `id` (PRIMARY KEY)
   - `thread_id` (viittaus threads-tauluun)
   - `sender_id` (viittaus users-tauluun)
   - `body` (viestin sisältö)
   - `created_at`
5. **classes**
   - `id` (PRIMARY KEY)
   - `title` (esim. "Ikäryhmä", "Taitotaso")
   - `value` (esim. "10-15 vuotta", "Aloittelija")
6. **announcement_classes**
   - `id` (PRIMARY KEY)
   - `announcement_id` (viittaus announcements_student-tauluun)
   - `title` (esim. "Ikäryhmä")
   - `value` (esim. "10-15 vuotta")

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

```bash
# Luo tietokanta schema.sql-tiedoston perusteella
sqlite3 database.db < schema.sql
```

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

## Käytettävissä olevat ominaisuudet
### Käyttäjähallinta
- **Rekisteröityminen**: `/register`
- **Kirjautuminen**: `/login`
- **Profiili**: `/profile` - Näyttönimen asettaminen ja profiilikuvien hallinta
- **Profiilikuvan lisääminen**: `/add_image`
- **Profiilikuvan poistaminen**: `/confirm_delete_image` → `/delete_image` (POST)
- **Profiilikuvan näyttäminen**: `/image/<user_id>`
- **Uloskirjautuminen**: `/logout`

### Ilmoitukset (Oppilaat)
- **Etusivu**: `/` - Näyttää kaikki oppilasilmoitukset
- **Uusi ilmoitus**: `/create_announcement_student`
- **Ilmoituksen katselu**: `/announcement/<id>`
- **Ilmoituksen muokkaus**: `/edit_announcement/<id>`
- **Ilmoituksen poisto**: `/remove_announcement/<id>`
- **Haku**: `/find_announcement`

### Viestit
- **Viestiketjut**: `/messages`
- **Uusi viesti**: `/messages/new`
- **Keskustelu**: `/messages/<thread_id>`

### Koodin Rakenne
- `app.py`: Flask-reitit ja sovelluslogiikka
- `db.py`: Tietokantayhteydet ja peruskyselyoperaatiot
- `announcements_student.py`: Oppilasilmoitusten CRUD-operaatiot
- `users.py`: Käyttäjien tietokantaoperaatiot (profiilit, autentikointi)
- `messages.py`: Viestien ja viestiketjujen tietokantaoperaatiot
- `ui.py`: UI-apufunktiot, virheenkäsittely ja sivujen renderöinti
- `templates/layout.html`: Yhteinen sivupohja kaikille sivuille
- `static/main.css`: Yhtenäinen CSS-tyylitysjärjestelmä 
  
### Testaus
Testaa seuraavat toiminnot:
1. Rekisteröidy ainakin kolmena eri käyttäjänä
2. Kirjaudu sisään eri käyttäjinä, testaa väärät tunnukset
3. Aseta näyttönimi profiilissa
4. Luo muutama erilainen oppilasilmoitus
5. Hae ilmoituksia hakusanalla
6. Muokkaa ja poista omia ilmoituksia
7. Testaa toisen käyttäjän ilmoitusten muokkausyritysta (403 virhe)
8. Lähetä viesti toiselle käyttäjälle
9. Testaa että vastaanottaja näkee viestin
10. Testaa että viestiketjut eri käyttäjien kanssa näkyvät listana
11. Testaa virheellisiä viestejä (tyhjä viesti, olematon käyttäjä)
12. Testaa kehittäjätyökalulla HTML-muokkauksen estäminen

## Turvallisuusominaisuudet
### Selainpuolen HTML-muokkauksen estäminen
Lisätty palvelinpuolen validaatio, joka varmistaa että `age_group` ja `skill_level` arvot vastaavat tietokannassa määriteltyjä sallittuja vaihtoehtoja.

**Toteutetut muutokset**:
#### 1. Virheenkäsittelijä (`ui.py`)
Lisätty `handle_invalid_selector_error()` funktio, joka palauttaa virheviestin virheellisistä valintakentän arvoista.

#### 2. Ilmoituksen luomisen validaatio (`app.py`)
Lisätty palvelinpuolen validaatio, joka tarkistaa että `age_group` ja `skill_level` arvot vastaavat tietokannassa määriteltyjä sallittuja vaihtoehtoja.

#### 3. Ilmoituksen muokkauksen validaatio (`app.py`)
Sama validaatio lisätty myös `update_announcement_student()` funktioon.

**Estetyt hyökkäykset**:
- XSS-injektio: `<script>alert('XSS')</script>` ikäryhmänä
- SQL-injektio: `'; DROP TABLE users; --` taitotasona
- Tietojen korruptio: `ADMIN_OVERRIDE` tai muut virheelliset arvot

**Testaus**:
1. Avaa selaimen kehittäjätyökalut (F12)
2. Mene ilmoituksen luomissivulle
3. Muokkaa `<select name="age_group">` elementtiä lisäämällä uusi `<option>` arvo
4. Lähetä lomake - pitäisi näkyä virhe: "VIRHE: virheellinen ikäryhmä"
5. Toista sama testi ilmoituksen muokkaussivulla

**Turvallisuus**:
- Estää selainpuolen muokkaukset
- Palvelinpuolen validaatio (ei voi ohittaa)
- Tietokannan eheys säilyy
- XSS-esto
- SQL-injektion esto
- Johdonmukainen virheenkäsittely

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
#### Ilmoitukset (`.announcement`)

#### Viestiketjut (`.thread`)

#### Viestit (`.message`)

#### Profiilitiedot (`.profile-info`)

### Lomakkeiden tyylitys
#### Syöttökentät
Responsiivinen leveys (max 30em), harmaa reunus, pyöristetyt kulmat, sopiva sisennys.

#### Painikkeet
Sininen tausta, valkoinen teksti, pyöristetyt kulmat, hiiren päällä -efekti.

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
#### Väripaletti
- **Tausta**: Vaaleanvihreä (`#f0f8f0`)
- **Otsikko**: Tummanharmaa tausta (`#2c3e50`), vaaleanharmaa teksti (`#ecf0f1`)
- **Navigaatio**: Tummanvihreä (`#52c41a`)
- **Sisältö**: Valkoinen tausta, harmaa reunus (`#bdc3c7`)
- **Reunukset**: Harmaan sävyjä (`#95a5a6`, `#7f8c8d`)
- **Painikkeet**: Vihreä (`#27ae60`)
- **Korostukset**: Vihreä (`#27ae60`, `#2ecc71`)

### Testaus
#### Visuaalinen tarkistus

1. **Yhtenäisyys**: Kaikki sivut noudattavat samaa tyyliä
2. **Navigaatio**: Toimii kaikilla sivuilla
3. **Responsiivisuus**: Toimii eri näytöillä
4. **Komponentit**: Ilmoitukset, viestit, lomakkeet tyylitetty

### Kehitys
#### Lisätyylit
- Virheviestit (`.error`, `.success`)
- Profiilikuvat (`.profile-image`)
- Metatiedot (`.meta`)
