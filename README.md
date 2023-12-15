Sovellus on tarkoitettu omien lempi(ruoka)reseptien tallentamiseen ja muokkaamiseen, sekä muiden käyttäjien lisäämien reseptien tarkastelemiseen. Käyttäjä pystyy tallentamaan hyväksi havaitsemansa reseptin tiedot sovelluksen tietokantaan,
muokkaamaan niitä, sekä etsimään sopivia reseptejä hakutoiminnolla. 

Sovelluksen ominaisuuksia:
- Käyttäjä voi kirjautua sisään ja ulos, sekä luoda tunnuksen.
- Käyttäjä pystyy lisäämään uuden reseptin, josta tallennetaan mm. tarvittavat raaka-aineet, valmistus-aika, valmistusohje sekä tieto siitä, onko resepti yksityinen, eli saavatko muut käyttäjät nähdä sen.
- Käyttäjä pystyy tarkastelemaan omia reseptejään ja muokkaamaan niitä, esimerkiksi poistamaan tietyn raaka-aineen.
- Käyttäjä pystyy poistamaan omia reseptejään.
- Käyttäjä pystyy etsimään julkisia reseptejä yksittäisten raaka-aineiden, maksimivalmistusajan ja nimen perusteella.
- Käyttäjä pystyy antamaan arvosteluja julkisille resepteille, 1 arvostelu/resepti, sekä poistamaan antamansa arvostelun.
- Arvostelut eivät poistu, vaikka reseptistä muokattaisiin yksityinen, ne vain piilotetaan.
- Käyttäjä pystyy tallentamaan muiden julkisia reseptejä suosikeikseen.
- Ylläpitäjäkäyttäjä pystyy poistamaan reseptejä ja arvosteluja.
HUOM.
Ylläpitäjäoikeuksia ei voi antaa sovelluksessa, vaan tämä täytyy tehdä suoraan tietokantaan esim. komennolla UPDATE Users SET admin = TRUE WHERE id = (käyttäjän id);

Ohje käynnistämiseen paikallisesti:
Kopioi tämä repositorio koneellesi ja siirry sen juurikansioon. Luo kansioon .env-niminen tiedosto ja määritä sen sisältö seuraavanalaiseksi: 

- DATABASE_URL= tietokannan-paikallinen-osoite
- SECRET_KEY= salainen-avain

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla:
- $ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla:
- $ flask run
