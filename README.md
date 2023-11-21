Sovellus on tarkoitettu omien lempi(ruoka)reseptien tallentamiseen ja muokkaamiseen, sekä muiden käyttäjien lisäämien reseptien tarkastelemiseen. Käyttäjä pystyy tallentamaan hyväksi havaitsemansa reseptin tiedot sovelluksen tietokantaan,
muokkaamaan niitä, sekä etsimään sopivia reseptejä sekä omiensa että muiden tallentamien reseptien joukosta. 

Sovelluksen ominaisuuksia:
- Käyttäjä voi kirjautua sisään ja ulos, sekä luoda tunnuksen.
- Käyttäjä pystyy lisäämään uuden reseptin, josta tallennetaan mm. tarvittavat raaka-aineet, valmistus-aika, valmistusohje sekä tieto siitä, onko resepti yksityinen, eli saavatko muut käyttäjät nähdä sen.
- Käyttäjä pystyy tarkastelemaan omia reseptejään ja muokkaamaan niitä, esimerkiksi poistamaan tietyn raaka-aineen.
- Käyttäjä pystyy poistamaan omia reseptejään.
- Käyttäjä pystyy etsimään reseptejä esimerkiksi yksittäisten raaka-aineiden perusteella sekä omiensa, että muiden julkisten reseptien joukosta.
- Käyttäjä pystyy antamaan arvosteluja omille sekä muiden julkisille resepteille, sekä tarkastelemaan reseptiensä saamia arvosteluja.
- Ylläpitäjäkäyttäjä pystyy poistamaan reseptejä, jotka ovat jollain tavalla sopimattomia.

Tällä hetkellä:
- Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos, mutta salasanoja ei tallenneta tietokantaan tietoturvallisesti.
- Käyttäjä voi lisätä uuden reseptin
- Käyttäjä näkee omat reseptinsä listana ja voi poistaa niitä
- Käyttäjä voi muokata reseptejä, mutta raaka-aineen poistaminen ei vielä toimi ja vajaat syötteet aiheuttavat virheitä.

Ohje käynnistämiseen paikallisesti:
Kopio tämä repositorio koneellesi ja siirry sen juurikansioon. Luo kansioon .env-niminen tiedosto ja määritä sen sisältö seuraavanalaiseksi: 

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
