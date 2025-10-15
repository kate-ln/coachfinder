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
- **Profiilikuvan poistaminen**: `/delete_image` (POST)
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

**Estetyt hyökkäykset**:

- XSS-injektio: `<script>alert('XSS')</script>` ikäryhmänä
- SQL-injektio: `'; DROP TABLE users; --` taitotasona
- Tietojen korruptio: `ADMIN_OVERRIDE` tai muut virheelliset arvot

**Turvallisuus**:

- Estää Inspector-muokkaukset
- Palvelinpuolen validaatio (ei voi ohittaa)
- Tietokannan eheys säilyy
- XSS-esto
- SQL-injektion esto
- Johdonmukainen virheenkäsittely
