# ﻿NVDA NVDA_VERSION - käyttöopas

[TOC]

<!-- KC:title: NVDA NVDA_VERSION - komentojen pikaopas -->



## Johdanto {#Introduction}

Tervetuloa käyttämään NVDA:ta!

Non-Visual Desktop Access (NVDA) on ilmainen ja avoimen lähdekoodin ruudunlukuohjelma Microsoft Windows -käyttöjärjestelmälle.
Synteettisenä puheena ja pistekirjoituksella annettava palaute mahdollistaa sen, että sokeat ja heikkonäköiset voivat käyttää Windows-tietokoneita samoin kustannuksin kuin näkevät henkilöt.
NVDA:ta kehittää [NV Access](https://www.nvaccess.org/) yhteisön jäsenten avustuksella.

### Yleiset ominaisuudet {#GeneralFeatures}

NVDA:n avulla sokeat ja heikkonäköiset voivat käyttää Windows-käyttöjärjestelmää ja monia kolmannen osapuolen sovelluksia.

Lyhyt englanninkielinen videoesittely, ["What is NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) on saatavilla NV Accessin YouTube-kanavalta.

Tärkeimpiä ominaisuuksia ovat:

* Tuki yleisille sovelluksille, internet-selaimet sekä sähköpostiasiakas-, internet-keskustelu- ja toimisto-ohjelmat mukaan lukien
* Yli 80 kieltä tukeva sisäänrakennettu puhesyntetisaattori
* Tekstin muotoilutietojen, kuten fontin nimen ja koon, tyylin sekä kirjoitusvirheiden puhuminen
* Automaattinen hiiren alla olevan tekstin puhuminen ja valinnainen hiiren sijainnin ilmaiseminen äänimerkeillä
* Tuki useille pistenäytöille, mukaan lukien mahdollisuus monen eri mallin automaattiseen tunnistamiseen sekä pistekirjoituksen syöttäminen tietokonemerkistöä käyttäen näytöissä, joissa on pistenäppäimistö
* Mahdollisuus käyttää USB-muistitikulta tai muulta siirrettävältä tallennusvälineeltä ilman asennusta
* Helppokäyttöinen puhuva asennusohjelma
* Käännökset 54 kielelle
* Tuki moderneille Windows-käyttöjärjestelmille, mukaan lukien sekä 32- että 64-bittiset versiot
* Mahdollisuus käyttää Windowsin sisäänkirjautumisen aikana sekä [muissa suojatuissa ruuduissa](#SecureScreens).
* Säätimien ja tekstin puhuminen kosketuseleitä käytettäessä
* Tuki yleisille saavutettavuusrajapinnoille, kuten Microsoft Active Accessibility, Java Access Bridge, IAccessible2 ja UI Automation
* Tuki Windowsin komentokehotteelle ja konsolisovelluksille
* Mahdollisuus kohdistuksen korostamiseen

### Järjestelmävaatimukset {#SystemRequirements}

* Käyttöjärjestelmät: kaikki 32- ja 64-bittiset Windows 8.1:n, 10:n ja 11:n versiot sekä palvelinversiot Windows Server 2012 R2:sta alkaen.
  * Sekä AMD64- että ARM64-versioita tuetaan.
* Vähintään 150 Mt tallennustilaa.

### Kansainvälisyys {#Internationalization}

On tärkeää, että ihmiset kaikkialla maailmassa voivat käyttää samoja teknologioita riippumatta siitä, mitä kieltä he puhuvat.
NVDA on käännetty englannin lisäksi seuraaville 54 kielelle: afrikaans, albania, amhara, arabia, aragonia, bulgaria, burma, espanja (Espanja ja Kolumbia), farsi, galego, georgia, heprea, hindi, hollanti, iiri, islanti, italia, japani, kannada, katalaani, kiina (mandariini ja perinteinen), kirgiisi, korea, kreikka, kroatia, liettua, makedonia, mongoli, nepali, norja, portugali (Brasilia ja Portugali), punjabi, puola, ranska, romania, ruotsi, saksa (Saksa ja Sveitsi), serbia, slovakki, sloveeni, suomi, tamili, tanska, thai, tšekki, turkki, ukraina, unkari, venäjä ja vietnam.

### Puhesyntetisaattorituki {#SpeechSynthesizerSupport}

Sen lisäksi, että NVDA:n ilmoitukset ja käyttöliittymä on käännetty useille kielille, käyttäjä voi myös lukea sisältöä millä tahansa kielellä, kunhan sitä tukeva puhesyntetisaattori on asennettu.

NVDA:n mukana toimitetaan [eSpeak NG](https://github.com/espeak-ng/espeak-ng), monikielinen, ilmainen ja avoimen lähdekoodin puhesyntetisaattori.

Tietoja muista NVDA:n tukemista puhesyntetisaattoreista löytyy [Tuetut puhesyntetisaattorit](#SupportedSpeechSynths) -luvusta.

### Pistenäyttötuki {#BrailleSupport}

NVDA voi antaa palautteen pistekirjoituksella käyttäjille, joilla on käytössään pistenäyttö.
NVDA käyttää avoimen lähdekoodin [LibLouis](https://liblouis.io/)-pistekääntäjää tekstin muuntamiseen pistekirjoitukseksi.
Lisäksi tuetaan sekä lyhenne- että tavallisen pistekirjoituksen syöttämistä pistekirjoitusnäppäimistöltä.
NVDA tunnistaa myös oletuksena automaattisesti useita pistenäyttöjä.
Tietoja tuetuista pistenäytöistä löytyy [Tuetut pistenäytöt](#SupportedBrailleDisplays) -luvusta.

NVDA tukee useiden kielten pistekirjoitusjärjestelmiä, lyhennekirjoitus ja tavallinen sekä tietokonemerkistö mukaan lukien.

### Käyttöoikeussopimus ja tekijänoikeustiedot {#LicenseAndCopyright}

NVDA on copyright NVDA_COPYRIGHT_YEARS NVDA:n tekijät.

NVDA on saatavilla GNU GPL 2.0 -lisenssin alaisena, mutta tähän on kaksi poikkeusta.
Poikkeukset on esitelty käyttöoikeusdokumentin luvuissa "Non-GPL Components in Plugins and Drivers" ja "Microsoft Distributable Code".
NVDA sisältää ja käyttää myös komponentteja, jotka ovat saatavilla eri vapaiden ja avoimen lähdekoodin lisenssien alaisina.
Voit vapaasti jakaa tai muuttaa tätä ohjelmistoa, kunhan toimitat lisenssin sen mukana ja pidät lähdekoodin kaikkien saatavilla.
Tämä koskee sekä alkuperäisiä että muokattuja ohjelmistokopioita ja kaikkia johdannaisia.

Voit [tarkastella koko käyttöoikeussopimusta](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) saadaksesi lisätietoja.
Saat lisätietoja poikkeuksista käyttöoikeussopimusdokumentista, jonka voit avata NVDA-valikon Ohje-alivalikosta.

## Pikaopas {#NVDAQuickStartGuide}

Tämä pika-aloitusopas sisältää kolme pääosaa: NVDA:n lataaminen, asentaminen ja käyttäminen.
Näiden jälkeen on tietoja asetusten muuttamisesta, yhteisöön osallistumisesta ja avun hankkimisesta.
Tämän oppaan tiedot on tiivistetty NVDA:n käyttöoppaan muista osista.
Katso täydellisestä käyttöoppaasta lisätietoja kustakin aiheesta.

### NVDA:n lataaminen {#GettingAndSettingUpNVDA}

NVDA on täysin ilmainen kenen tahansa käytettäväksi.
Lisenssiavaimesta ei tarvitse huolehtia tai maksaa kalliista tilauksesta.
NVDA:ta päivitetään keskimäärin neljä kertaa vuodessa.
NVDA:n uusin versio on aina saatavilla [NV Accessin kotisivun](NVDA_URL) "Download"-sivulta.

NVDA toimii kaikkien uusimpien Windows-versioiden kanssa.
Katso tarkemmat tiedot kohdasta [Järjestelmävaatimukset](#SystemRequirements).

#### Lataamisen vaiheet {#StepsForDownloadingNVDA}

Nämä vaiheet edellyttävät jonkin verran perehtymistä verkkosivulla liikkumiseen.

* Avaa verkkoselain (paina `Windows`-näppäintä, kirjoita sana "internet" ilman lainausmerkkejä ja paina `Enter`)
* Avaa NV Accessin lataussivu (paina `Alt+D`, kirjoita seuraava osoite ja paina `Enter`):
https://www.nvaccess.org/download
* Paina "Download"-painiketta
* Selain saattaa kysyä suoritettavaa toimintoa lataamisen jälkeen ja käynnistää sitten ladatun tiedoston
* Selaimesta riippuen tiedosto saatetaan suorittaa automaattisesti latauksen jälkeen
* Jos tiedosto on käynnistettävä manuaalisesti, siirry selaimen ilmoituksiin painamalla `F6` ja sitten `Alt+S` suorittaaksesi tiedoston (tehtävät vaiheet riippuvat käytettävästä selaimesta)

### NVDA:n asentaminen {#SettingUpNVDA}

Lataamasi tiedoston suorittaminen käynnistää NVDA:n tilapäisversion.
Seuraavaksi sinulta kysytään, haluatko asentaa sen, luoda massamuistiversion vai jatkaa tilapäisversion käyttöä.

NVDA ei tarvitse internet-yhteyttä käynnistymiseen tai asentamiseen asennusohjelman lataamisen jälkeen.
Mikäli internet-yhteys on käytettävissä, NVDA voi suorittaa säännöllisesti päivitystarkistuksen.

#### Asennusohjelman suorittamisen vaiheet {#StepsForRunningTheDownloadLauncher}

Asennustiedoston nimi on "nvda_2022.1.exe" tai vastaava.
Vuosi ja versio muuttuvat päivitysten välillä vastaamaan nykyistä versiota.

1. Suorita ladattu tiedosto.
Tunnusmusiikki soi NVDA:n tilapäisversion käynnistyessä.
Kun se on käynnistynyt, NVDA puhuu koko prosessin ajan.
1. Näyttöön tulee NVDA:n asennusohjelman ikkuna, jossa näytetään käyttöoikeussopimus.
Lue sopimus halutessasi painamalla `Nuoli alas`.
1. Siirry "Hyväksyn"-valintaruudun kohdalle painamalla `Sarkainta` ja valitse se painamalla `Välilyöntiä`.
1. Liiku vaihtoehtojen välillä painamalla `Sarkainta` ja valitse haluamasi painamalla `Enter`.

Vaihtoehdot ovat:

* "Asenna": Useimmat käyttäjät valitsevat tämän vaihtoehdon helpottaakseen NVDA:n käyttöä.
* "Luo massamuistiversio": Tämän avulla NVDA:n tiedostot voidaan kopioida mihin tahansa kansioon ilman asennusta.
Tästä on hyötyä tietokoneissa, joissa ei ole järjestelmänvalvojan oikeuksia, tai jos haluat NVDA:n muistitikulle mukana kuljetettavaksi.
Kun tämä on valittu, NVDA käy läpi massamuistiversion luomisen vaiheet.
Tärkein asia, joka NVDA:n on tiedettävä, on kansio, johon massamuistiversio kopioidaan.
* "Jatka käyttöä": Tämä pitää NVDA:n tilapäisversion käynnissä.
Tästä on hyötyä kokeiltaessa uuden version ominaisuuksia ennen sen asentamista.
Kun tämä valitaan, asennusohjelman ikkuna sulkeutuu ja NVDA:n tilapäisversio pysyy käynnissä, kunnes se suljetaan tai tietokone sammutetaan.
Huom: Asetusten muutoksia ei tallenneta.
* "Peruuta": Tämä sulkee NVDA:n suorittamatta mitään toimintoa.

Mikäli aiot käyttää NVDA:ta aina samassa tietokoneessa, sinun kannattaa valita asennusvaihtoehto.
NVDA:n asentaminen mahdollistaa lisätoimintoja, kuten automaattisen käynnistyksen sisäänkirjautumisen jälkeen sekä Windowsin kirjautumisikkunan ja [suojattujen ruutujen](#SecureScreens) lukemisen.
Nämä toiminnot eivät ole käytettävissä massamuisti- tai tilapäisversioissa.
Katso täydelliset tiedot massamuisti- ja tilapäisversioiden käytön rajoituksista luvusta [Massamuisti- ja tilapäisversioiden rajoitukset](#PortableAndTemporaryCopyRestrictions).

Asennus tarjoaa myös Käynnistä-valikon ja työpöydän pikakuvakkeiden luomisen sekä mahdollistaa NVDA:n käynnistämisen pikanäppäimellä `Ctrl+Alt+N`.

#### NVDA:n asentamisen vaiheet asennusohjelmalla {#StepsForInstallingNVDAFromTheLauncher}

Näissä vaiheissa käydään läpi yleisimmät asennusvaihtoehdot.
Lisätietoja käytettävissä olevista vaihtoehdoista on kohdassa [Asennusvaihtoehdot](#InstallingNVDA).

1. Varmista, että käyttöoikeussopimuksen hyväksymisvalintaruutu on valittuna asennusohjelmassa.
1. Siirry `Sarkaimella` "Asenna"-painikkeen kohdalle ja paina sitä.
1. Seuraavana ovat asetukset NVDA:n käyttämiseen Windowsin sisäänkirjautumisen aikana ja työpöydän pikakuvakkeen luomiseen.
Ne ovat oletusarvoisesti valittuina.
Voit halutessasi Muuttaa näitä asetuksia painamalla `Sarkainta` ja `Välilyöntiä` tai jättää ne oletusarvoihinsa.
1. Jatka painamalla `Enter`.
1. Näkyviin tulee Windowsin käyttäjätilien valvonnan valintaikkuna, jossa kysytään, haluatko sallia tämän sovelluksen tehdä muutoksia tietokoneeseesi.
1. Hyväksy muutosten tekeminen painamalla `Alt+Ä`.
1. Edistymispalkki täyttyy NVDA:n asentuessa.
Asennuksen aikana NVDA antaa yhä korkeammaksi muuttuvan äänimerkin.
Tämä prosessi on usein nopea, eikä sitä välttämättä huomaa.
1. Näyttöön tulee valintaikkuna, joka vahvistaa, että NVDA:n asennus on onnistunut.
Ilmoitus neuvoo käynnistämään asennetun version painamalla OK.
Käynnistä asennettu versio painamalla `Enter`.
1. "Tervetuloa NVDA:han" -valintaikkuna tulee näkyviin, ja NVDA lukee tervetuloviestin.
Kohdistus on "Näppäinasettelu"-alasvetovalikossa.
"Pöytäkone"-näppäinasettelussa käytetään oletusarvoisesti laskinnäppäimistöä joihinkin toimintoihin.
Voit halutessasi määrittää laskinnäppäimistön toiminnot muille näppäimille painamalla `Nuoli alas`, joka valitsee "kannettava"-näppäinasettelun.
1. Siirry kohtaan "Käytä `Caps Lockia` NVDA-näppäimenä" painamalla `Sarkainta`.
Oletusnäppäimenä käytetään `Insertiä`.
Valitse `Caps Lock` vaihtoehtoiseksi painamalla `Välilyöntiä`.
Huom: Näppäinasettelu määritetään erillään NVDA-näppäimestä.
NVDA-näppäin ja näppäinasettelu voidaan vaihtaa myöhemmin NVDA:n asetusten Näppäimistö-kategoriasta.
1. Käytä `Sarkainta` ja `Välilyöntiä` muiden tässä näytössä olevien asetusten säätämiseen.
Niiden avulla määritetään, käynnistyykö NVDA automaattisesti.
Sulje valintaikkuna painamalla `Enter`, kun NVDA on nyt käynnissä.

### NVDA:n käyttäminen {#RunningNVDA}

Täydellinen käyttöopas sisältää kaikki NVDA-komennot, jotka on jaettu eri lukuihin.
Komentotaulukot ovat saatavilla myös komentojen pikaoppaassa.
Englanninkielisessä "Basic Training for NVDA" -opetusmateriaalimoduulissa jokainen komento on kuvailtu perusteellisemmin vaiheittaisten tehtävien avulla.
"Basic Training for NVDA" -moduuli on saatavilla [NV Access Shopista](https://www.nvaccess.org/shop).

Tässä on joitakin usein käytettyjä peruskomentoja.
Kaikki komennot ovat käyttäjän määritettävissä, joten nämä ovat toimintojen oletusarvoiset näppäinmäärittelyt.

#### NVDA-näppäin {#NVDAModifierKey}

Oletusarvoinen NVDA-näppäin on joko `Laskinnäppäimistön 0` (`Num Lock` pois päältä) tai lähellä `Delete`-, `Home`- ja `End`-näppäimiä oleva `Insert`-näppäin.
`Caps Lock` voidaan myös määrittää NVDA-näppäimeksi.

#### Näppäinohje {#InputHelp}

Voit opetella ja harjoitella näppäinten sijainteja painamalla `NVDA+1`, joka ottaa käyttöön näppäinohjeen.
Näppäinohjetilassa minkä tahansa komennon (kuten näppäinkomennon tai kosketuseleen) suorittaminen ilmoittaa kyseiseen komentoon määritetyn toiminnon ja kuvailee, mitä se tekee.
Varsinaisia komentoja ei suoriteta.

#### NVDA:n käynnistäminen ja sulkeminen {#StartingAndStoppingNVDA}

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Käynnistä NVDA |`Ctrl+Alt+N` |`Ctrl+Alt+N` |Käynnistää tai uudelleenkäynnistää NVDA:n.|
|Sulje NVDA |`NVDA+Q` ja sitten `Enter` |`NVDA+Q` ja sitten `Enter` |Sulkee NVDA:n.|
|Tauota tai jatka puhetta |`Vaihto` |`Vaihto` |Tauottaa puheen välittömästi. Uudelleen painaminen jatkaa puhetta kohdasta, jossa se tauotettiin.|
|Keskeytä puhe |`Ctrl` |`Ctrl` |Keskeyttää puheen välittömästi.|

#### Tekstin lukeminen {#ReadingText}

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Jatkuva luku |`NVDA+Nuoli alas` |`NVDA+A` |Alkaa lukea nykyisestä sijainnista lähtien siirtäen samalla kohdistinta.|
|Puhu nykyinen rivi |`NVDA+Nuoli ylös` |`NVDA+L` |Puhuu nykyisen rivin. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen (Antti, Bertta, Celsius, jne.).|
|Puhu valinta |`NVDA+Vaihto+Nuoli ylös` |`NVDA+Vaihto+S` |Puhuu valitun tekstin. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|
|Puhu leikepöydän teksti |`NVDA+C` |`NVDA+C` |Puhuu leikepöydällä olevan tekstin. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|

#### Sijainti- ja muiden tietojen puhuminen {#ReportingLocation}

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Ikkunan nimi |`NVDA+T` |`NVDA+T` |Lukee aktiivisen ikkunan nimen. Kahdesti painettaessa se tavataan ja kolmesti painettaessa kopioidaan leikepöydälle.|
|Puhu kohdistus |`NVDA+Sarkain` |`NVDA+Sarkain` |Puhuu säätimen, jossa järjestelmän kohdistus on. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|
|Puhu ikkuna |`NVDA+B` |`NVDA+B` |Puhuu koko nykyisen ikkunan (hyödyllinen valintaikkunoissa).|
|Puhu tilarivi |`NVDA+End` |`NVDA+Vaihto+End` |Puhuu tilarivin, mikäli sellainen löytyy. Kahdesti painettaessa se tavataan ja kolmesti painettaessa kopioidaan leikepöydälle.|
|Puhu kellonaika |`NVDA+F12` |`NVDA+F12` |Puhuu kerran painettaessa kellonajan ja kahdesti painettaessa päivämäärän. Ajan ja päivämäärän muoto vastaa Windowsin asetuksissa tehtäväpalkin kellolle määriteltyä muotoa.|
|Puhu tekstin muotoilut |`NVDA+F` |`NVDA+F` |Puhuu tekstin muotoilutiedot. Kahdesti painettaessa ne näytetään selaustilassa.|
|Puhu linkin kohde |`NVDA+K` |`NVDA+K` |Puhuu kerran painettaessa kohdistimen tai kohdistuksen kohdalla olevan linkin kohteen URLin. Kahdesti painettaessa se näytetään erillisessä ikkunassa.|

#### Valitse, mitä tietoja NVDA puhuu {#ToggleWhichInformationNVDAReads}

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Puhu kirjoitetut merkit |`NVDA+2` |`NVDA+2` |Kun tämä on käytössä, NVDA puhuu kaikki kirjoitetut merkit.|
|Puhu kirjoitetut sanat |`NVDA+3` |`NVDA+3` |Kun tämä on käytössä, NVDA puhuu kaikki kirjoitetut sanat.|
|Puhu komentonäppäimet |`NVDA+4` |`NVDA+4` |Kun tämä on käytössä, NVDA puhuu kaikki painetut näppäimet, jotka eivät ole kirjaimia. Näitä ovat esim. näppäinyhdistelmät Ctrl+jokin kirjain.|
|Käytä hiiren seurantaa |`NVDA+M` |`NVDA+M` |Kun tämä on käytössä, NVDA puhuu hiiriosoittimen alla olevan tekstin. Tällä tavalla on mahdollista löytää asioita ruudulta hiirtä liikuttamalla sen sijaan, että käytettäisiin objektinavigointia.|

#### Syntetisaattorin asetusrengas {#TheSynthSettingsRing}

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Siirrä seuraavaan syntetisaattorin asetukseen |`NVDA+Ctrl+Nuoli oikealle` |`NVDA+Vaihto+Ctrl+Nuoli oikealle` |Siirtää seuraavaan käytettävissä olevaan nykyisen jälkeiseen puheasetukseen palaten viimeisen jälkeen takaisin ensimmäiseen.|
|Siirrä edelliseen syntetisaattorin asetukseen |`NVDA+Ctrl+Nuoli vasemmalle` |`NVDA+Vaihto+Ctrl+Nuoli vasemmalle` |Siirtää seuraavaan käytettävissä olevaan nykyistä edeltävään puheasetukseen palaten ensimmäisen jälkeen takaisin viimeiseen.|
|Suurenna aktiivista syntetisaattorin asetusta |`NVDA+Ctrl+Nuoli ylös` |`NVDA+Vaihto+Ctrl+Nuoli ylös` |Suurentaa valittua puheasetusta, esim. lisää nopeutta, valitsee seuraavan puheäänen tai lisää äänenvoimakkuutta.|
|Suurenna aktiivista syntetisaattorin asetusta enemmän |`NVDA+Ctrl+Page up` |`NVDA+Vaihto+Ctrl+Page up` |Suurentaa nykyisen puheasetuksen arvoa enemmän kerrallaan. Kun esim. puheääniasetus on valittuna, tämä komento siirtää kerralla eteenpäin 20 äänen yli. Liukusäädinasetusten kohdalla (nopeus, korkeus jne.) se suurentaa arvoa jopa 20 %.|

|Pienennä aktiivista syntetisaattorin asetusta |`NVDA+Ctrl+Nuoli alas` |`NVDA+Vaihto+Ctrl+Nuoli alas` |Pienentää valittua puheasetusta, esim. vähentää nopeutta, valitsee edellisen puheäänen tai vähentää äänenvoimakkuutta.|
|Pienennä aktiivista syntetisaattorin asetusta enemmän |`NVDA+Ctrl+Page down` |`NVDA+Vaihto+Ctrl+Page down` |Pienentää aktiivisen puheasetuksen arvoa enemmän kerrallaan. Kun esim. puheääniasetus on valittuna, tämä komento siirtää kerralla taaksepäin 20 äänen yli. Liukusäädinasetusten kohdalla se pienentää arvoa jopa 20 %.|

Aktiivisen syntetisaattoriasetuksen ensimmäiseen tai viimeiseen arvoon on myös mahdollista siirtyä määrittämällä kyseisille toiminnoille mukautetut näppäinkomennot [Näppäinkomennot-valintaikkunan](#InputGestures) Puhe-kategoriassa.
Tämä tarkoittaa esimerkiksi sitä, että kun nopeusasetus on valittuna, nopeudeksi määritetään joko 0 tai 100.
Kun puheääniasetus on aktiivisena, ääneksi määritetään ensimmäinen tai viimeinen vaihtoehto.

#### Verkon selaaminen {#WebNavigation}

Täydellinen luettelo pikanavigointinäppäimistä on käyttöoppaan [Selaustila](#BrowseMode)-luvussa.

| Komento |Näppäin |Kuvaus|
|---|---|---|
|Otsikko |`H` |Siirrä seuraavaan otsikkoon.|
|Otsikkotaso 1, 2 tai 3 |`1`, `2`, `3` |Siirrä seuraavaan otsikkoon määritetyllä tasolla.|
|Lomakekenttä |`F` |Siirrä seuraavaan lomakekenttään (muokkausruutu, painike jne.).|
|Linkki |`K` |Siirrä seuraavaan linkkiin.|
|Kiintopiste |`D` |Siirrä seuraavaan kiintopisteeseen.|
|Luettelo |`L` |Siirrä seuraavaan luetteloon.|
|Taulukko |`T` |Siirrä seuraavaan taulukkoon.|
|Siirrä taaksepäin |`Vaihto+Kirjain` |Paina `Vaihto` ja mitä tahansa yllä olevista kirjaimista siirtyäksesi edelliseen kyseisen tyypin elementtiin.|
|Elementtilista |`NVDA+F7` |Näyttää luettelon erityyppisistä elementeistä, kuten linkeistä ja otsikoista.|

### Asetukset {#Preferences}

Useimmat NVDA:n toiminnot voidaan ottaa käyttöön tai muuttaa NVDA:n asetusten kautta.
Asetukset ja muut vaihtoehdot ovat käytettävissä NVDA-valikon kautta.
Avaa NVDA-valikko painamalla `NVDA+N`.
Avaa NVDA:n yleisten asetusten valintaikkuna suoraan painamalla `NVDA+Ctrl+G`.
Monilla asetusvalintaikkunoilla on pikanäppäin niiden avaamiseksi suoraan, kuten `NVDA+Ctrl+S` syntetisaattorille tai `NVDA+Ctrl+V` muille puheäänen asetuksille.

### Yhteisö {#Community}

NVDA:lla on vilkas käyttäjäyhteisö.
Käytettävissä on iso [englanninkielinen sähköpostilista](https://nvda.groups.io/g/nvda) sekä sivu, jossa on luettelo [paikallisten kielten ryhmistä](https://github.com/nvaccess/nvda/wiki/Connect).
NV Access, NVDA:n kehittäjät, ovat aktiivisia [X:ssä](https://twitter.com/nvaccess) sekä [Facebookissa](https://www.facebook.com/NVAccess).
NV Accessilla on myös tavallinen [In-Process-blogi](https://www.nvaccess.org/category/in-process/).

Lisäksi on [NVDA Certified Expert](https://certification.nvaccess.org/) -ohjelma.
Se on online-koe, jonka voit suorittaa osoittaaksesi NVDA:n käyttötaitosi.
[NVDA-sertifioidut asiantuntijat](https://certification.nvaccess.org/) voivat luetella yhteys- ja asiaankuuluvat yritystietonsa.

### Avun hankkiminen {#GettingHelp}

Saat ohjeita NVDA:ssa painamalla `NVDA+N` avataksesi NVDA-valikon ja sitten `O` avataksesi Ohje-valikon.
Tästä alivalikosta voit avata käyttöoppaan, komentojen pikaoppaan, uusien ominaisuuksien historian sekä paljon muuta.
Nämä kolme ensimmäistä vaihtoehtoa avautuvat oletusselaimessa.
Kattavampaa opetusmateriaalia on saatavilla [NV Access Shopista](https://www.nvaccess.org/shop).

Suosittelemme aloittamaan "Basic Training for NVDA" -moduulista.
Se kattaa käsitteet alkuun pääsemisestä verkon selaamiseen ja objektinavigoinnin käyttöön.
Moduuli on saatavana seuraavissa muodoissa:

* [E-kirja](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), joka sisältää Wordin DOCX-, HTML-, ePub-e-kirjan sekä Kindlen KFX-muodot.
* [Ihmisen lukema MP3-äänikirja](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Paperiversio UEB-pistekirjoituksella](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) sisältäen toimituksen minne tahansa maailmassa.

Muut moduulit sekä alehintainen [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/) ovat saatavilla [NV Access Shopista](https://www.nvaccess.org/shop/).

NV Access tarjoaa lisäksi [puhelintukea](https://www.nvaccess.org/product/nvda-telephone-support/) joko erikseen tai osana [NVDA Productivity Bundlea](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Puhelintuki sisältää paikalliset numerot Australiassa ja Yhdysvalloissa.

[Käyttäjien sähköpostiryhmät](https://github.com/nvaccess/nvda/wiki/Connect) ovat suuri yhteisön avun lähde samoin kuin [sertifioidut NVDA-asiantuntijat](https://certification.nvaccess.org/).

Voit tehdä virheraportteja tai ominaisuusehdotuksia [GitHubissa](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
[Osallistumisohjeet](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) sisältävät arvokasta tietoa yhteisöön osallistumisesta.

## Lisää asennusvaihtoehtoja {#MoreSetupOptions}
### Asennusvaihtoehdot {#InstallingNVDA}

Mikäli asennat suoraan ladatusta NVDA:n asennusohjelmasta, paina Asenna-painiketta.
Jos olet jo sulkenut tämän valintaikkunan tai haluat asentaa massamuistiversiosta, valitse Asenna NVDA -vaihtoehto, joka löytyy NVDA-valikon Työkalut-alivalikosta.

Näkyviin tuleva valintaikkuna kysyy vahvistuksen NVDA:n asentamiselle ja kertoo myös, päivittääkö asennusohjelma aiemman version.
Asennus käynnistyy painamalla Jatka-painiketta.
Tässä valintaikkunassa on myös muutama vaihtoehto, jotka on selitetty alla.
Kun asennus on suoritettu, näkyviin tulee ilmoitus onnistumisesta.
Käynnistä asennettu versio painamalla OK.

#### Varoitus yhteensopimattomista lisäosista {#InstallWithIncompatibleAddons}

Jos lisäosia on jo asennettuna, asennusohjelmassa saatetaan myös näyttää varoitus, että yhteensopimattomat lisäosat poistetaan käytöstä.
Ennen kuin voit painaa Jatka-painiketta, sinun on vahvistettava, että olet ymmärtänyt lisäosien käytöstä poistamisen valitsemalla kyseisen valintaruudun.
Käytettävissä on myös painike, joka näyttää luettelon käytöstä poistettavista lisäosista.
Katso lisätietoja tästä painikkeesta [Yhteensopimattomien lisäosien valintaikkuna -luvusta](#incompatibleAddonsManager).
Asennuksen jälkeen voit omalla vastuullasi ottaa yhteensopimattomat lisäosat uudelleen käyttöön [lisäosakaupasta](#AddonsManager).

#### Käytä sisäänkirjautumisen aikana {#StartAtWindowsLogon}

Tällä asetuksella voit valita, käynnistyykö NVDA automaattisesti Windowsin kirjautumisikkunassa ennen kuin olet syöttänyt salasanan.
Asetus vaikuttaa myös käyttäjätilien valvontaan sekä [muihin suojattuihin ruutuihin](#SecureScreens).
Se on oletusarvoisesti käytössä uusissa asennuksissa.

#### Luo pikakuvake työpöydälle (Ctrl+Alt+N) {#CreateDesktopShortcut}

Tällä asetuksella voit valita, luodaanko työpöydälle NVDA:n pikakuvake.
Jos pikakuvake luodaan, sille määritetään myös pikanäppäin `Ctrl+Alt+N`, jota painamalla NVDA voidaan käynnistää.

#### Kopioi massamuistiversion asetukset nykyiseen käyttäjätiliin {#CopyPortableConfigurationToCurrentUserAccount}

Tällä asetuksella voit valita, kopioidaanko käynnissä olevan NVDA:n asetukset asennettuun versioon nykyiselle sisäänkirjautuneelle käyttäjälle.
Asetuksia ei kopioida tietokoneen muille käyttäjille eikä Windowsin sisäänkirjautumisen aikana tai [muissa suojatuissa](ruuduissa)(#SecureScreens) käytettäväksi.
Tämä vaihtoehto on käytettävissä vain massamuistiversiosta asennettaessa.

### Massamuistiversion luominen {#CreatingAPortableCopy}

Jos luot massamuistiversion suoraan ladatusta NVDA:n asennuspaketista, paina Luo massamuistiversio -painiketta.
Mikäli olet jo sulkenut tämän valintaikkunan tai käytät NVDA:n asennettua versiota, valitse Luo massamuistiversio -vaihtoehto, joka löytyy NVDA-valikosta Työkalut-valikon alta.

Valitse näkyviin tulevassa valintaikkunassa sijainti, jonne massamuistiversio luodaan.
Sijainti voi olla kiintolevyllä, USB-muistitikulla tai muulla siirrettävällä tallennusvälineellä oleva hakemisto.
Tässä valintaikkunassa on myös vaihtoehto, jolla voit valita, kopioidaanko kirjautuneen käyttäjän asetukset massamuistiversiossa käytettäviksi.
Vaihtoehto on käytettävissä vain luotaessa massamuistiversiota asennetusta versiosta.
Aloita massamuistiversion luonti painamalla Jatka.
Kun luonti on valmis, näkyviin tulee ilmoitus onnistumisesta.
Sulje valintaikkuna painamalla OK.

### Massamuisti- ja tilapäisversioiden rajoitukset {#PortableAndTemporaryCopyRestrictions}

Jos haluat ottaa NVDA:n mukaasi USB-muistitikulla tai muulla tallennusvälineellä, sinun tulee valita massamuistiversion luonti.
Asennetusta versiosta voidaan myös milloin tahansa luoda massamuistiversio.
Massamuistiversion asentaminen on lisäksi mahdollista myöhemmin mihin tahansa tietokoneeseen.
Jos kuitenkin haluat kopioida NVDA:n vain luku -tyyppiselle tallennusvälineelle, kuten CD-levylle, sinun tulee kopioida vain asennuspaketti.
massamuistiversion suorittamista suoraan vain luku -tyyppiseltä tietovälineeltä ei tällä hetkellä tueta.

[NVDA:n asennusohjelmaa](#StepsForRunningTheDownloadLauncher) voidaan käyttää tilapäisversiona.
Asetusten tallentaminen on estetty tilapäisversioissa.
Myös [lisäosakauppa](#AddonsManager) on poissa käytöstä.

NVDA:n massamuisti- ja tilapäisversioissa on seuraavia rajoituksia:

* Kirjautumisen aikana ja/tai jälkeen käynnistyminen ei ole mahdollista.
* Vuorovaikutus järjestelmänvalvojan oikeuksin käynnissä olevien sovellusten kanssa ei ole mahdollista, ellei NVDA:ta ole käynnistetty samoin oikeuksin (ei suositella).
* Käyttäjätilien valvonnan kehotteiden lukeminen ei ole mahdollista yritettäessä käynnistää sovellusta järjestelmänvalvojan oikeuksin.
* Kosketusnäyttösyötettä ei tueta.
* Selaustila ja kirjoitettujen merkkien puhuminen eivät toimi Microsoft Storesta ladatuissa sovelluksissa.
* Äänenvaimennusta ei tueta.

## NVDA:n käyttäminen {#GettingStartedWithNVDA}
### Käynnistäminen {#LaunchingNVDA}

Jos olet asentanut NVDA:n omalla asennusohjelmallaan, voit käynnistää sen joko painamalla `Ctrl+Alt+N` tai valitsemalla Käynnistä-valikosta Ohjelmat -> NVDA -> NVDA.
Käynnistäminen on mahdollista myös kirjoittamalla Suorita-valintaikkunaan NVDA ja painamalla `Enter`.
Mikäli NVDA on jo käynnissä, se käynnistetään uudelleen.
Lisäksi on mahdollista käyttää [komentorivivalitsimia](#CommandLineOptions), joilla NVDA voidaan sulkea (-q), poistaa lisäosat käytöstä (--disable-addons) jne.

NVDA:n asennettu versio tallentaa asetuksensa oletusarvoisesti nykyisen käyttäjän sovellustietojen Roaming-kansioon (esim. "`C:\Users\<Käyttäjä>\AppData\Roaming`").
Tämä on mahdollista muuttaa myös niin, että asetukset ladataan em. sijainnin asemesta paikallisten sovellustietojen kansiosta.
Lisätietoja on [Järjestelmänlaajuiset parametrit](#SystemWideParameters) -luvussa.

Käynnistä massamuistiversio menemällä hakemistoon, johon se on purettu ja painamalla `Enter` nvda.exe-tiedoston kohdalla tai kaksoisnapsauttamalla sitä hiiren vasemmalla painikkeella.
Mikäli NVDA oli jo käynnissä, se suljetaan automaattisesti ennen massamuistiversion käynnistämistä.

NVDA:n käynnistyessä kuuluu joukko nousevia ääniä.
Käynnistyminen saattaa kestää jonkin aikaa riippuen tietokoneesi nopeudesta tai jos käytät NVDA:ta USB-muistitikulta tai muulta hitaammalta tallennusvälineeltä.
Jos käynnistyminen kestää erityisen kauan, NVDA:n pitäisi sanoa "NVDA käynnistetään, odota..."

Mikäli et kuule mitään tällaista tai jos kuulet Windowsin virheäänen tai joukon laskevia ääniä, NVDA:ssa on mahdollisesti bugi, josta on ilmoitettava kehittäjille.
Ohjeet bugien ilmoittamiseen voit tarkistaa NVDA:n verkkosivustolta.

#### Tervetuloa-valintaikkuna {#WelcomeDialog}

Kun NVDA käynnistyy ensimmäistä kertaa, näkyviin tulee valintaikkuna, jossa on joitakin perustietoja NVDA-näppäimestä ja -valikosta.
Katso edempänä olevia lukuja saadaksesi tietoja näistä aiheista.
Valintaikkunassa on lisäksi yhdistelmäruutu sekä kolme valintaruutua.
Yhdistelmäruudusta valitaan näppäinasettelu.
Ensimmäisellä valintaruudulla määritetään, käytetäänkö Caps Lockia NVDA-näppäimenä.
Toisella, joka on käytettävissä vain asennetuissa versioissa, valitaan, käynnistyykö NVDA automaattisesti Windowsiin kirjautumisen jälkeen.
Kolmannella määritetään, tuleeko Tervetuloa-valintaikkuna näkyviin AINA NVDA:n käynnistyessä.

#### Käyttötilastojen keräämisen valintaikkuna {#UsageStatsDialog}

NVDA 2018.3:sta lähtien käyttäjältä kysytään, haluaako hän sallia käyttötietojen lähettämisen NV Accessille NVDA:n parantamiseksi tulevaisuudessa.
Kun NVDA käynnistetään ensimmäistä kertaa, näkyviin tulee valintaikkuna, jossa kysytään, hyväksytkö tietojen lähettämisen.
Voit lukea lisätietoja NV Accessin keräämistä tiedoista yleisten asetusten kohdasta [Salli NV Accessin kerätä NVDA:n käyttötilastoja](#GeneralSettingsGatherUsageStats).
Huom: Asetus tallennetaan painaessasi "Kyllä" tai "Ei", eikä valintaikkunaa enää näytetä, ellet asenna NVDA:ta uudelleen.
Voit kuitenkin ottaa käyttöön tai poistaa käytöstä tiedonkeruun manuaalisesti NVDA:n yleisten asetusten paneelista. Muuta asetusta valitsemalla tai poistamalla valinta [Salli NV Accessin kerätä NVDA:n käyttötilastoja](#GeneralSettingsGatherUsageStats) -valintaruudusta.

### Tietoja näppäinkomennoista {#AboutNVDAKeyboardCommands}
#### NVDA-näppäin {#TheNVDAModifierKey}

Useimmat NVDA:n näppäinkomennot koostuvat yleensä tietyn NVDA-näppäimeksi kutsutun näppäimen painamisesta yhdessä yhden tai useamman muun näppäimen kanssa.
Poikkeuksia ovat pöytäkoneissa käytettävän näppäinasettelun tekstintarkastelukomennot sekä muutamat muut, joissa käytetään pelkkiä laskinnäppäimistön näppäimiä.

NVDA on mahdollista määrittää käyttämään sekä laskinnäppäimistön että laajennettua Insertiä ja/tai Caps Lockia NVDA-näppäimenä.
Oletusarvoisesti käytetään sekä laajennettua että laskinnäppäimistön Insertiä.

Mikäli haluat jonkin NVDA-näppäimen toimivan samalla tavalla kuin silloin, kun NVDA ei ole käynnissä (haluat esim. ottaa Caps Lockin käyttöön, kun se on määritetty NVDA-näppäimeksi), paina sitä kaksi kertaa nopeasti peräkkäin.

#### Näppäinasettelut {#KeyboardLayouts}

NVDA:n mukana tulee tällä hetkellä kaksi erilaista näppäinasetteluiksi kutsuttua näppäinkomentojen määritystä: pöytäkoneille ja kannettaville tarkoitetut.
NVDA käyttää oletusarvoisesti pöytäkoneiden näppäinasettelua, mutta kannettaville tarkoitettuun asetteluun voidaan vaihtaa Näppäimistö-kategoriasta [NVDA:n asetukset](#NVDASettings) -valintaikkunasta, johon pääsee NVDA-valikon Asetukset-alivalikosta.

Pöytäkoneiden näppäinasettelussa käytetään runsaasti laskinnäppäimistön näppäimiä (Num Lockin on oltava pois käytöstä).
Vaikka useimmissa kannettavissa tietokoneissa ei ole fyysistä laskinnäppäimistöä, joissakin sellaista voidaan kuitenkin jäljitellä pitämällä `FN`-näppäintä alhaalla ja painamalla kirjaimia ja numeroita näppäimistön oikeanpuoleisesta osasta (7, 8, 9, U, I, O, J, K, L jne).
Mikäli tämä ei ole mahdollista käyttämässäsi kannettavassa tai jos `Num Lockia` ei voi poistaa käytöstä, käyttöön voidaan ottaa kannettavien näppäinasettelu.

### NVDA:n kosketuseleet {#NVDATouchGestures}

NVDA:ta on mahdollista ohjata myös kosketuskomentojen avulla, mikäli käytettävässä laitteessa on kosketusnäyttö.
Kaikki kosketussyötteet välitetään suoraan NVDA:lle sen ollessa käynnissä, ellei kosketusvuorovaikutuksen tukea ole poistettu käytöstä.
Tämän vuoksi sellaisia toimintoja ei voi suorittaa, jotka toimivat normaalisti ilman NVDA:ta.
<!-- KC:beginInclude -->
Ota kosketuksen vuorovaikutus käyttöön tai poista se käytöstä painamalla `NVDA+Ctrl+Alt+T`.
<!-- KC:endInclude -->
Voit ottaa käyttöön [kosketusvuorovaikutuksen tuen](#TouchSupportEnable) tai poistaa sen käytöstä myös NVDA:n asetusten Kosketuksen vuorovaikutus -kategoriasta.

#### Ruudun tutkiminen {#ExploringTheScreen}

Kaikkein alkeellisin toiminto, joka voidaan suorittaa kosketusnäytöllä, on säätimen tai tekstin lukeminen mistä tahansa kohdasta.
Tämä tehdään sijoittamalla sormi mihin tahansa kohtaan näytöllä.
Muita säätimiä ja tekstiä voidaan lukea myös pitämällä ja siirtämällä sormea näytöllä.

#### Kosketuseleet {#TouchGestures}

Kun NVDA-komentoja kuvaillaan edempänä tässä käyttöoppaassa, niissä saatetaan mainita kosketusele, jota voidaan käyttää kosketusnäytöllä kyseisen komennon suorittamiseen.
Seuraavassa on ohjeita eri kosketuseleiden suorittamiseen.

##### Napautukset {#toc45}

Napauta näyttöä nopeasti yhdellä tai useammalla sormella.

Kerran napauttamista yhdellä sormella kutsutaan napautukseksi.
Kahdella sormella napauttaminen yhtaikaa on napautus kahdella sormella jne.

Mikäli sama napautus suoritetaan kerran tai useammin nopeasti peräkkäin, NVDA käsittelee sitä moninapautuseleenä.
Kahdesti napauttamisesta on seurauksena kaksoisnapautus.
Kolmesti napauttamisesta seuraa kolmoisnapautus jne.
Moninapautuseleet tunnistavat myös, montaako sormea käytettiin, joten esim. kolmoisnapautus kahdella sormella tai napautus neljällä sormella jne. ovat mahdollisia.

##### Pyyhkäisyt {#toc46}

Liu'uta sormea nopeasti näytöllä.

Pyyhkäisyeleitä on neljä suunnasta riippuen: pyyhkäisy vasemmalle, oikealle, ylös ja alas.

Eleen suorittamiseen voidaan käyttää useampaa kuin yhtä sormea, aivan kuten napautustenkin kohdalla.
Tämän vuoksi esim. pyyhkäisy ylös kahdella sormella tai pyyhkäisy vasemmalle neljällä sormella ovat mahdollisia.

#### Kosketustilat {#TouchModes}

Koska NVDA-komentoja on enemmän kuin mahdollisia kosketuseleitä, NVDA:ssa on tämän vuoksi useita kosketustiloja, joita vaihtamalla saadaan käyttöön tiettyyn alaluokkaan kuuluvia komentoja.
Käytettävissä olevat tilat ovat tekstitila ja objektitila.
Tietyissä tässä asiakirjassa luetelluissa komennoissa saattaa olla kosketuseleen jälkeen suluissa maininta kosketustilasta.
Esimerkiksi pyyhkäisy ylös (tekstitila) tarkoittaa, että komento suoritetaan pyyhkäistäessä ylös, mutta vain tekstitilassa.
Mikäli komennon kohdalla ei ole mainintaa kosketustilasta, se toimii kaikissa tiloissa.

<!-- KC:beginInclude -->
Vaihda kosketustilaa napauttamalla kolmella sormella.
<!-- KC:endInclude -->

#### Kosketusnäppäimistö {#TouchKeyboard}

Kosketusnäppäimistöä käytetään kosketusnäytöllä tekstin ja komentojen syöttämiseen.
Kun muokkauskenttä on aktiivisena, tuo kosketusnäppäimistö näkyviin kaksoisnapauttamalla näytön alareunassa olevaa kosketusnäppäimistökuvaketta.
Kosketusnäppäimistö on aina käytettävissä tableteissa, kuten Microsoft Surface Pro:ssa, kun näppäimistö on irrotettu.
Piilota kosketusnäppäimistö kaksoisnapauttamalla kosketusnäppäimistökuvaketta tai siirtymällä pois muokkauskentästä.

Kun kosketusnäppäimistö on aktiivisena, etsi halutut näppäimet siirtämällä sormi kosketusnäppäimistön sijaintipaikkaan (tyypillisesti näytön alareunassa), ja liikkumalla sitten näppäimistössä yhdellä sormella.
Kun haluttu näppäin on löytynyt, kaksoisnapauta sitä tai nosta sormi näytöltä, riippuen NVDA:n asetusten [Kosketuksen vuorovaikutus -kategoriassa](#TouchInteraction) valituista asetuksista.

### Näppäinohjetila {#InputHelpMode}

Tässä käyttöoppaassa mainitaan useita näppäinkomentoja, mutta helpoin tapa tutkia niitä kaikkia on käyttää näppäinohjetta.

Ota näppäinohje käyttöön painamalla `NVDA+1`.
Poista se käytöstä painamalla uudelleen `NVDA+1`.
Kun näppäinohje on käytössä, NVDA kertoo mitä tahansa komentoa suoritettaessa, kuten näppäintä painettaessa tai kosketuselettä käytettäessä sen suorittaman toiminnon, mikäli kyseiseen komentoon on sellainen määritelty.
Komentojen toimintoja ei suoriteta.

### NVDA-valikko {#TheNVDAMenu}

NVDA-valikosta voit säätää NVDA:n asetuksia, lukea ohjetta, tallentaa ja palauttaa asetukset, muokata puhesanastoja, käyttää lisätyökaluja sekä sulkea NVDA:n.

NVDA-valikkoon pääsee seuraavasti kaikkialta Windowsista NVDA:n ollessa käynnissä:

* Painamalla näppäimistöltä `NVDA+N`.
* Kaksoisnapauttamalla kosketusnäyttöä kahdella sormella.
* Siirtymällä ilmoitusalueelle painamalla `Windows+B`, `Nuoli alas` -näppäimellä NVDA-kuvakkeen kohdalle ja painamalla `Enter`.
* Siirtymällä vaihtoehtoisesti ilmoitusalueelle painamalla `Windows+B`, `Nuoli alas` -näppäimellä NVDA-kuvakkeen kohdalle ja avaamalla pikavalikon painamalla `sovellusnäppäintä`, joka löytyy useimmista näppäimistöistä oikeanpuoleisen Ctrl-näppäimen vierestä.
Näppäimistöissä, joissa ei ole `sovellusnäppäintä`, käytetään sen sijaan `Vaihto+F10`-näppäinyhdistelmää.
* Napsauttamalla hiiren oikealla painikkeella ilmoitusalueella olevaa NVDA:n kuvaketta.

Kun valikko tulee näkyviin, voit käyttää nuolinäppäimiä siinä liikkumiseen ja `Enter`-näppäintä kohteen valitsemiseen.

### Peruskomennot {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kosketusele |Kuvaus|
|---|---|---|---|---|
|Käynnistä tai käynnistä uudelleen NVDA |`Ctrl+Alt+N` |`Ctrl+Alt+N` |Ei mitään |Käynnistää tai käynnistää uudelleen NVDA:n työpöydältä, mikäli tämä pikanäppäin on otettu käyttöön NVDA:n asennuksen aikana. Tämä on Windowsin pikanäppäin, eikä sitä siksi voida uudelleenmäärittää Näppäinkomennot-valintaikkunassa.|
|Keskeytä puhe |`Ctrl` |`Ctrl` |Napautus kahdella sormella |Keskeyttää puheen välittömästi.|
|Tauota puhe |`Vaihto` |`Vaihto` |Ei mitään |Tauottaa puheen välittömästi. Uudelleen painaminen jatkaa puhetta kohdasta, jossa se tauotettiin (mikäli käytössä oleva puhesyntetisaattori tukee puheen tauottamista).|
|NVDA-valikko |`NVDA+N` |`NVDA+N` |Kaksoisnapautus kahdella sormella |Avaa NVDA-valikon, josta voidaan säätää asetuksia, käyttää työkaluja ja lukea ohjetta jne.|
|Ota käyttöön tai poista käytöstä näppäinohjetila |`NVDA+1` |`NVDA+1` |Ei mitään |Tässä tilassa minkä tahansa näppäimen painaminen kertoo sen nimen ja kaikki siihen määritellyt NVDA-komennot.|
|Sulje NVDA |`NVDA+Q` |`NVDA+Q` |Ei mitään |Sulkee NVDA:n.|
|Ohita seuraava näppäinpainallus |`NVDA+F2` |`NVDA+F2` |Ei mitään |Välittää seuraavan näppäinpainalluksen suoraan aktiiviselle sovellukselle suorittamatta sen mahdollista NVDA-komentoa.|
|Ota käyttöön tai poista käytöstä lepotila |`NVDA+Vaihto+S` |`NVDA+Vaihto+Z` |Ei mitään |Lepotila poistaa käytöstä kaikki NVDA:n komennot sekä puheen ja pistekirjoituksen tuottamisen nykyisessä sovelluksessa. Tästä on eniten hyötyä sovelluksissa, joissa on sisäänrakennettu puhe- tai ruudunlukutoiminto. Lepotila poistetaan käytöstä painamalla uudelleen tätä näppäinyhdistelmää. Huom: Asetus säilyy vain seuraavaan NVDA:n uudelleenkäynnistykseen saakka.|

<!-- KC:endInclude -->

### Järjestelmätietojen puhuminen {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Puhu päivämäärä/kellonaika |`NVDA+F12` |Puhuu kerran painettaessa kellonajan ja kahdesti painettaessa päivämäärän.|
|Puhu akun tila |`NVDA+Vaihto+B` |Puhuu akun tilan, ts. onko verkkovirta käytössä, tai kertoo nykyisen varauksen tason prosentteina.|
|Puhu leikepöydällä oleva teksti |`NVDA+C` |Puhuu leikepöydällä olevan tekstin.|

<!-- KC:endInclude -->

### Puhetilat {#SpeechModes}

Puhetila säätelee, miten näytön sisältö, ilmoitukset, komentojen vastaukset ja muu tuloste puhutaan NVDA:n käytön aikana.
Oletustila on "puhe käytössä", jota käytettäessä NVDA puhuu tilanteissa, joissa ruudunlukijan odotetaan puhuvan.
Tietyissä tapauksissa tai tiettyjä ohjelmia käytettäessä saatat kuitenkin huomata, että jokin muu puhetila on sopivampi.

Käytettävissä on neljä puhetilaa:

* Puhe käytössä (oletus): NVDA puhuu normaalisti reagoidessaan näytön muutoksiin, ilmoituksiin ja toimintoihin, kuten kohdistuksen siirtämiseen tai komentojen antamiseen.
* Pyydettäessä: NVDA puhuu vain, kun käytät komentoja, jotka puhuvat jotain (esim. ikkunan nimen), mutta ei puhu reagoidessaan esim. kohdistuksen tai kohdistimen siirtämiseen.
* Ei puhetta: NVDA ei puhu mitään. Toisin kuin lepotilassa, se reagoi kuitenkin komentoihin puhumatta mitään.
* Äänimerkit: NVDA korvaa normaalin puheen lyhyillä äänimerkeillä.

Äänimerkit-tilasta voi olla hyötyä, kun päätteessä tulostuu jonkin komennon seurauksena paljon tekstiä, mutta et ole kiinnostunut sen sisällöstä vaan pelkästään siitä, että tekstin tulostuminen ruudulle jatkuu, tai muissa tilanteissa, joissa tieto tekstin ilmestymisestä ruudulle on tärkeämpää kuin itse sisältö.

Pyydettäessä-tila voi olla hyödyllinen, kun et tarvitse jatkuvaa palautetta esim. ruudun tapahtumista, mutta sinun on kuitenkin ajoittain tarkistettava tiettyjä asioita puhutuskomentoja käyttäen yms.
Esimerkkeinä tällaisista voisivat olla äänen nauhoittaminen, näytön suurennuksen käyttäminen, kokous, puhelu tai vaihtoehto Äänimerkit-tilalle.

Näppäinkomento mahdollistaa puhetilan vaihtamisen:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vaihda puhetilaa |`NVDA+S` |Vaihtaa puhetilojen välillä.|

<!-- KC:endInclude -->

Jos tarvitset vaihtamista vain tiettyjen puhetilojen välillä, katso tarpeettomien puhetilojen käytöstä poistaminen kohdasta [Puhetilakomennon valinnat](#SpeechModesDisabling).

## NVDA:lla liikkuminen {#NavigatingWithNVDA}

NVDA:n avulla voidaan tutkia järjestelmää ja liikkua siinä useilla tavoilla sekä normaali vuorovaikutus että tekstin tarkastelu mukaan lukien.

### Objektit {#Objects}

Jokainen sovellus ja itse käyttöjärjestelmä koostuvat useista objekteista.
Objekti on yksittäinen kohde, kuten tekstinpätkä, painike, valintaruutu, liukusäädin, luettelo tai muokattava tekstikenttä.

### Järjestelmäkohdistuksella liikkuminen {#SystemFocus}

Järjestelmäkohdistus, kutsutaan myös kohdistukseksi, on [objekti](#Objects), joka vastaanottaa näppäimistön näppäinpainallukset.
Jos esimerkiksi kirjoitat muokattavaan tekstikenttään, kohdistus on kyseisessä kentässä.

Yleisin tapa liikkua NVDA:lla Windowsissa on käyttää tavallisia näppäinkomentoja, kuten Sarkain ja Vaihto+Sarkain eteen- ja taaksepäin säädinten välillä liikkumiseen, painamalla Alt valikkoriville siirtymiseen, käyttämällä nuolinäppäimiä valikoissa liikkumiseen ja Alt+Sarkainta avointen sovellusten välillä siirtymiseen.
Näin tehtäessä NVDA kertoo tietoja objektista, jossa kohdistus on, kuten nimen, tyypin, tilan, arvon, kuvauksen, pikanäppäimen ja sijainnin.
Kun [visuaalinen korostus](#VisionFocusHighlight) on käytössä, järjestelmäkohdistuksen nykyinen sijainti näytetään visuaalisesti.

Järjestelmäkohdistuksella liikkumista varten on joitakin hyödyllisiä näppäinkomentoja:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Puhu nykyinen kohdistus |`NVDA+Sarkain` |`NVDA+Sarkain` |Puhuu nykyisen objektin tai säätimen, jossa järjestelmän kohdistus on. Kahdesti painettaessa se tavataan.|
|Puhu ikkunan nimi |`NVDA+T` |`NVDA+T` |Puhuu aktiivisen ikkunan nimen. Kahdesti painettaessa se tavataan ja kolmesti painettaessa kopioidaan leikepöydälle.|
|Puhu aktiivinen ikkuna |`NVDA+B` |`NVDA+B` |Puhuu kaikki aktiivisen ikkunan säätimet (hyödyllinen valintaikkunoissa).|
|Puhu tilarivi |`NVDA+End` |`NVDA+Vaihto+End` |Puhuu tilarivin, mikäli sellainen löytyy. Kahdesti painettaessa se tavataan ja kolmesti painettaessa kopioidaan leikepöydälle.|
|Puhu pikanäppäin |`Vaihto+Laskinnäppäimistön 2` |`NVDA+Ctrl+Vaihto+.` |Puhuu aktiivisen objektin pikanäppäimen.|

<!-- KC:endInclude -->

### Järjestelmäkohdistimella liikkuminen {#SystemCaret}

Kun [kohdistus](#SystemFocus) on navigoinnin ja/tai tekstin muokkaamisen mahdollistavassa [objektissa](#Objects), tekstissä voidaan liikkua järjestelmäkohdistinta käyttäen (kutsutaan myös muokkauskohdistimeksi).

Kun kohdistus on järjestelmäkohdistimen sisältävässä objektissa, tekstissä liikkumiseen voidaan käyttää nuoli-, Page up-, Page down-, Home- sekä End-näppäimiä jne.
Tekstiä on myös mahdollista muokata, mikäli säädin tukee sitä.
NVDA puhuu kaiken merkki, sana ja rivi kerrallaan liikuttaessa ja ilmoittaa myös, kun tekstiä on tai ei ole valittu.

NVDA:ssa on seuraavat järjestelmäkohdistimeen liittyvät näppäinkomennot:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Jatkuva luku |`NVDA+Nuoli alas` |`NVDA+A` |Aloittaa lukemisen järjestelmäkohdistimen nykyisestä sijainnista lähtien siirtäen samalla sitä.|
|Puhu nykyinen rivi |`NVDA+Nuoli ylös` |`NVDA+L` |Puhuu järjestelmäkohdistimen kohdalla olevan rivin. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|
|Puhu valittu teksti |`NVDA+Vaihto+Nuoli ylös` |`NVDA+Vaihto+S` |Puhuu valittuna olevan tekstin.|
|Puhu tekstin muotoilutiedot |`NVDA+F` |`NVDA+F` |Puhuu kohdistimen kohdalla olevan tekstin muotoilutiedot. Kahdesti painettaessa ne näytetään selaustilassa.|
|Puhu linkin kohde |`NVDA+K` |`NVDA+K` |Puhuu kerran painettaessa kohdistimen tai kohdistuksen kohdalla olevan linkin kohteen URLin. Kahdesti painettaessa se näytetään erillisessä ikkunassa.|
|Puhu kohdistimen sijainti |`NVDA+Laskinnäppäimistön Delete` |`NVDA+Delete` |Puhuu järjestelmäkohdistimen kohdalla olevan tekstin tai objektin sijaintitiedot. Näitä tietoja voivat olla esim. asiakirjan luettu osuus prosentteina, etäisyys sivun reunasta tai tarkka paikka ruudulla. Kahdesti painaminen saattaa antaa lisätietoja.|
|Seuraava lause |`Alt+Nuoli alas` |`Alt+Nuoli alas` |Siirtää kohdistimen seuraavaan lauseeseen ja puhuu sen (tuetaan vain Microsoft Wordissa ja Outlookissa).|
|Edellinen lause |`Alt+Nuoli ylös` |`Alt+Nuoli ylös` |Siirtää kohdistimen edelliseen lauseeseen ja puhuu sen (tuetaan vain Microsoft Wordissa ja Outlookissa).|

Taulukoissa ovat käytettävissä lisäksi seuraavat näppäinkomennot:

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Siirrä edelliseen sarakkeeseen |`Ctrl+Alt+Nuoli vasemmalle` |Siirtää järjestelmäkohdistimen edelliseen sarakkeeseen pysyen samalla rivillä.|
|Siirrä seuraavaan sarakkeeseen |`Ctrl+Alt+Nuoli oikealle` |Siirtää järjestelmäkohdistimen seuraavaan sarakkeeseen pysyen samalla rivillä.|
|Siirrä edelliselle riville |`Ctrl+Alt+Nuoli ylös` |Siirtää järjestelmäkohdistimen edelliselle riville pysyen samassa sarakkeessa.|
|Siirrä seuraavalle riville |`Ctrl+Alt+Nuoli alas` |Siirtää järjestelmäkohdistimen seuraavalle riville pysyen samassa sarakkeessa.|
|Siirrä ensimmäiseen sarakkeeseen |`Ctrl+Alt+Home` |Siirtää järjestelmäkohdistimen ensimmäiseen sarakkeeseen pysyen samalla rivillä.|
|Siirrä viimeiseen sarakkeeseen |`Ctrl+Alt+End` |Siirtää järjestelmäkohdistimen viimeiseen sarakkeeseen pysyen samalla rivillä.|
|Siirrä ensimmäiselle riville |`Ctrl+Alt+Page up` |Siirtää järjestelmäkohdistimen ensimmäiselle riville pysyen samassa sarakkeessa.|
|Siirrä viimeiselle riville |`Ctrl+Alt+Page down` |Siirtää järjestelmäkohdistimen viimeiselle riville pysyen samassa sarakkeessa.|
|Sarakkeen jatkuva luku |`NVDA+Ctrl+Alt+Nuoli alas` |Lukee sarakkeen pystysuunnassa alaspäin nykyisestä solusta viimeiseen.|
|Rivin jatkuva luku |`NVDA+Ctrl+Alt+Nuoli oikealle` |Lukee rivin vaakasuunnassa oikealle nykyisestä solusta viimeiseen.|
|Lue koko sarake |`NVDA+Ctrl+Alt+Nuoli ylös` |Lukee nykyisen sarakkeen pystysuunnassa ylhäältä alas siirtämättä järjestelmäkohdistinta.|
|Lue koko rivi |`NVDA+Ctrl+Alt+Nuoli vasemmalle` |Lukee nykyisen rivin vaakasuunnassa vasemmalta oikealle siirtämättä järjestelmäkohdistinta.|

<!-- KC:endInclude -->

### Objektinavigointi {#ObjectNavigation}

Sovelluksia käytetään enimmäkseen komennoilla, jotka siirtävät [kohdistusta](#SystemFocus) ja [kohdistinta](#SystemCaret).
Toisinaan voi kuitenkin olla tarpeen tutkia nykyistä sovellusta tai käyttöjärjestelmää ilman, että kohdistus tai kohdistin liikkuu.
Saatat myös haluta siirtyä [objekteihin](#Objects), joihin ei ole mahdollista päästä tavalliseen tapaan näppäimistöä käyttäen.
Tällaisissa tapauksissa voidaan käyttää objektinavigointia.

Objektinavigoinnin avulla on mahdollista liikkua yksittäisten [objektien](#Objects) välillä ja saada niistä tietoja.
Kun objektiin siirrytään, NVDA lukee sen samalla tavalla kuin järjestelmäkohdistuksen.
Tekstin tarkastelemiseen sellaisena kuin se näkyy ruudulla voidaan käyttää [ruudun tarkastelua.](#ScreenReview)

Objektit on ryhmitelty hierarkkisesti sen sijaan, että niiden välillä liikuttaisiin edestakaisin.
Tämä tarkoittaa, että jotkin objektit sisältävät muita objekteja, ja että niiden sisään on siirryttävä, jotta päästäisiin edelleen niiden sisältämiin objekteihin.
Esimerkiksi luettelo sisältää kohteita, joten niihin pääsemiseksi on siirryttävä luettelon sisään.
Jos on siirrytty luettelokohteeseen, saman luettelon muihin kohteisiin päästään siirtymällä seuraavaan tai edelliseen objektiin.
Takaisin luetteloon pääsee siirtymällä luettelokohteen säilöobjektiin.
Tämän jälkeen voidaan siirtyä luettelosta pois, mikäli halutaan päästä muihin objekteihin.
Myös työkalupalkki sisältää säätimiä, joten niihin pääsemiseksi on siirryttävä kyseisen työkalupalkin sisään.

Jos haluat mieluummin liikkua järjestelmässä jokaisen yksittäisen objektin välillä, voit käyttää edelliseen tai seuraavaan objektiinn tasatussa näkymässä siirtäviä komentoja.
Jos esimerkiksi siirryt tasatussa näkymässä seuraavaan objektiin ja nykyinen objekti sisältää muita objekteja, NVDA siirtyy automaattisesti ensimmäiseen nykyisen objektin sisältämään objektiin.
Vaihtoehtoisesti, jos nykyinen objekti ei sisällä muita objekteja, NVDA siirtyy seuraavaan objektiin nykyisellä hierarkiatasolla.
Mikäli tällaista objektia ei ole, NVDA yrittää löytää seuraavan objektinn hierarkiassa sen sisältämien objektien perusteella, kunnes ei ole enää objekteja, joihin siirtyä.
Samat säännöt pätevät myös hierarkiassa taaksepäin liikkumiseen.

Nykyistä tarkasteltavaa objektia kutsutaan navigointiobjektiksi.
Kun objektiin siirrytään, sitä voidaan tarkastella [tekstintarkastelukomennoilla](#ReviewingText) [objektintarkastelutilassa](#ObjectReview) oltaessa.
Kun [visuaalinen korostus](#VisionFocusHighlight) on käytössä, nykyisen navigointiobjektin sijainti näytetään myös visuaalisesti.
Navigointiobjekti liikkuu oletusarvoisesti järjestelmäkohdistuksen mukana, mutta tämä asetus voidaan poistaa myös käytöstä.

Huom: Pistenäyttö voidaan määrittää seuraamaan objektinavigointia [Pistenäyttö seuraa -asetuksella.](#BrailleTether)

Seuraavia komentoja käytetään objekteittain liikkumiseen:

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kosketusele |Kuvaus|
|---|---|---|---|---|
|Puhu nykyinen objekti |`NVDA+Laskinnäppäimistön 5` |`NVDA+Vaihto+O` |Ei mitään |Puhuu nykyisen navigointiobjektin. Kahdesti painettaessa se tavataan ja kolmesti painettaessa objektin nimi ja arvo kopioidaan leikepöydälle.|
|Siirrä säilöobjektiin |`NVDA+Laskinnäppäimistön 8` |`NVDA+Vaihto+Nuoli ylös` |Pyyhkäisy ylös (objektitila) |Siirtää objektiin, joka sisältää nykyisen navigointiobjektin.|
|Siirrä edelliseen objektiin |`NVDA+Laskinnäppäimistön 4` |`NVDA+Vaihto+Nuoli vasemmalle` |Ei mitään |Siirtää nykyistä navigointiobjektia edeltävään objektiin.|
|Siirrä edelliseen objektiin tasatussa näkymässä |`NVDA+Laskinnäppäimistön 9` |`NVDA+Vaihto+I` |Pyyhkäisy vasemmalle (objektitila) |Siirtää edelliseen objektiin objektinavigointihierarkian tasatussa näkymässä.|
|Siirrä seuraavaan objektiin |`NVDA+Laskinnäppäimistön 6` |`NVDA+Vaihto+Nuoli oikealle` |Ei mitään |Siirtää nykyisen navigointiobjektin jälkeiseen objektiin.|
|Siirrä seuraavaan objektiin tasatussa näkymässä |`NVDA+Laskinnäppäimistön 3` |`NVDA+Vaihto+O` |Pyyhkäisy oikealle (objektitila) |Siirtää seuraavaan objektiin objektinavigointihierarkian tasatussa näkymässä.|
|Siirrä ensimmäiseen sisältöobjektiin |`NVDA+Laskinnäppäimistön 2` |`NVDA+Vaihto+Nuoli alas` |Pyyhkäisy alas (objektitila) |Siirtää ensimmäiseen navigointiobjektin sisällä olevaan objektiin.|
|Siirrä aktiiviseen objektiin |`NVDA+Laskinnäppäimistön miinus` |`NVDA+Askelpalautin` |Ei mitään |Siirtää objektiin, jossa järjestelmän kohdistus on tällä hetkellä ja sijoittaa tarkastelukohdistimen järjestelmäkohdistimen kohdalle, mikäli se on näkyvissä.|
|Aktivoi nykyinen navigointiobjekti |`NVDA+Laskinnäppäimistön Enter` |`NVDA+Enter` |Kaksoisnapautus |Aktivoi nykyisen navigointiobjektin (vastaa hiiren napsauttamista tai `Välilyönnin` painamista, kun järjestelmän kohdistus on siinä).|
|Siirrä kohdistus tai kohdistin tarkastelukohtaan |`NVDA+Vaihto+Laskinnäppäimistön miinus` |`NVDA+Vaihto+Askelpalautin` |Ei mitään |Siirtää kerran painettaessa järjestelmän kohdistuksen nykyiseen navigointiobjektiin tai kahdesti painettaessa järjestelmäkohdistimen tarkastelukohdistimen kohdalle.|
|Puhu tarkastelukohdistimen sijainti |`NVDA+Vaihto+Laskinnäppäimistön Delete` |`NVDA+Vaihto+Delete` |Ei mitään |Lukee tarkastelukohdistimen kohdalla olevan tekstin tai objektin sijaintitiedot. Näitä tietoja voivat olla esim. asiakirjan luettu osuus prosentteina, etäisyys sivun reunasta tai tarkka paikka ruudulla. Kahdesti painaminen saattaa antaa lisätietoja.|
|Siirrä tarkastelukohdistin tilariville |Ei mitään |Ei mitään |Ei mitään |Puhuu tilarivin, mikäli sellainen löytyy. Lisäksi navigointiobjekti siirretään sen kohdalle.|

<!-- KC:endInclude -->

Huom: `Num Lockin` on oltava pois käytöstä, jotta laskinnäppäimistön näppäimet toimivat oikein.

### Tekstin tarkasteleminen {#ReviewingText}

NVDA:n avulla on mahdollista lukea [ruutua](#ScreenReview), nykyistä [asiakirjaa](#DocumentReview) tai [objektia](#ObjectReview) merkeittäin, sanoittain tai riveittäin.
Tästä on eniten hyötyä paikoissa, joissa ei ole [järjestelmäkohdistinta](#SystemCaret) (Windowsin komentokonsolit mukaan lukien).
Tätä voidaan käyttää esim. valintaikkunassa olevan ilmoituksen lukemiseen.

Kun tarkastelukohdistinta siirretään, järjestelmäkohdistin ei seuraa mukana, joten tekstin tarkastelu onnistuu muokkauskohtaa menettämättä.
Kun järjestelmäkohdistin liikkuu, tarkastelukohdistin seuraa kuitenkin oletusarvoisesti mukana.
Tätä asetusta on mahdollista muuttaa.

Huom: Pistenäyttö voidaan määrittää seuraamaan tarkastelukohdistinta [Pistenäyttö seuraa -asetuksella.](#BrailleTether)

Seuraavat tekstintarkastelukomennot ovat käytettävissä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kosketusele |Kuvaus|
|---|---|---|---|---|
|Siirrä tarkastelukohdistin ylimmälle riville |`Vaihto+Laskinnäppäimistön 7` |`NVDA+Ctrl+Home` |Ei mitään |Siirtää tarkastelukohdistimen ylimmälle riville.|
|Siirrä tarkastelukohdistin edelliselle riville |`Laskinnäppäimistön 7` |`NVDA+Nuoli ylös` |Pyyhkäisy ylös (tekstitila) |Siirtää tarkastelukohdistimen edelliselle riville.|
|Puhu tarkastelukohdistimen kohdalla oleva rivi |`Laskinnäppäimistön 8` |`NVDA+Vaihto+.` |Ei mitään |Puhuu tarkastelukohdistimen kohdalla olevan rivin. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|
|Siirrä tarkastelukohdistin seuraavalle riville |`Laskinnäppäimistön 9` |`NVDA+Nuoli alas` |Pyyhkäisy alas (tekstitila) |Siirtää tarkastelukohdistimen seuraavalle riville.|
|Siirrä tarkastelukohdistin alimmalle riville |`Vaihto+Laskinnäppäimistön 9` |`NVDA+Ctrl+End` |Ei mitään |Siirtää tarkastelukohdistimen alimmalle riville.|
|Siirrä tarkastelukohdistin edelliseen sanaan |`Laskinnäppäimistön 4` |`NVDA+Ctrl+Nuoli vasemmalle` |Pyyhkäisy vasemmalle kahdella sormella (tekstitila) |Siirtää tarkastelukohdistimen edellisen sanan kohdalle.|
|Puhu tarkastelukohdistimen kohdalla oleva sana |`Laskinnäppäimistön 5` |`NVDA+Ctrl+.` |Ei mitään |Puhuu tarkastelukohdistimen kohdalla olevan sanan. Kahdesti painettaessa se tavataan normaalisti ja kolmesti painettaessa merkkikuvauksia käyttäen.|
|Siirrä tarkastelukohdistin seuraavaan sanaan |`Laskinnäppäimistön 6` |`NVDA+Ctrl+Nuoli oikealle` |Pyyhkäisy oikealle kahdella sormella (tekstitila) |Siirtää tarkastelukohdistimen seuraavan sanan kohdalle.|
|Siirrä tarkastelukohdistin rivin alkuun |`Vaihto+Laskinnäppäimistön 1` |`NVDA+Home` |Ei mitään |Siirtää tarkastelukohdistimen nykyisen rivin alkuun.|
|Siirrä tarkastelukohdistin edelliseen merkkiin |`Laskinnäppäimistön 1` |`NVDA+Nuoli vasemmalle` |Pyyhkäisy vasemmalle (tekstitila) |Siirtää tarkastelukohdistimen seuraavan merkin kohdalle nykyisellä rivillä.|
|Puhu tarkastelukohdistimen kohdalla oleva merkki |`Laskinnäppäimistön 2` |`NVDA+.` |Ei mitään |Puhuu nykyisen merkin tarkastelukohdistimen kohdalla olevalta riviltä. Kahdesti painettaessa luetaan merkin kuvaus tai esimerkki sen käytöstä. Kolmesti painettaessa luetaan sen numeerinen arvo desimaaleina ja heksadesimaaleina.|
|Siirrä tarkastelukohdistin seuraavaan merkkiin |`Laskinnäppäimistön 3` |`NVDA+Nuoli oikealle` |Pyyhkäisy oikealle (tekstitila) |Siirtää tarkastelukohdistimen seuraavan merkin kohdalle nykyisellä rivillä.|
|Siirrä tarkastelukohdistin rivin loppuun |`Vaihto+Laskinnäppäimistön 3` |`NVDA+End` |Ei mitään |Siirtää tarkastelukohdistimen nykyisen rivin loppuun.|
|Siirrä tarkastelukohdistin edelliselle sivulle |`NVDA+Page up` |`NVDA+Vaihto+Page up` |Ei mitään |Siirtää tarkastelukohdistimen edelliselle sivulle, mikäli sovellus tukee sitä.|
|Siirrä tarkastelukohdistin seuraavalle sivulle |`NVDA+Page down` |`NVDA+Vaihto+Page down` |Ei mitään |Siirtää tarkastelukohdistimen seuraavalle sivulle, mikäli sovellus tukee sitä.|
|Jatkuva luku tarkastelukohdistimella |`Laskinnäppäimistön plus` |`NVDA+Vaihto+A` |Pyyhkäisy alas kolmella sormella (tekstitila) |Lukee tarkastelukohdistimen nykyisestä kohdasta alkaen siirtäen samalla tarkastelukohdistinta.|
|Valitse ja kopioi tarkastelukohdistimesta |`NVDA+F9` |`NVDA+F9` |Ei mitään |Aloittaa tekstin valitsemisen ja kopioinnin tarkastelukohdistimen nykyisestä kohdasta. Kopiointia ei suoriteta ennen kuin NVDA:lle kerrotaan, missä tekstilohkon loppu on.|
|Valitse ja kopioi tarkastelukohdistimeen |`NVDA+F10` |`NVDA+F10` |Ei mitään |Valitsee ensimmäisellä painalluksella aiemmin asetetusta tekstilohkon alkukohdasta lähtien tarkastelukohdistimen nykyiseen sijaintiin saakka. Järjestelmäkohdistin siirretään valittuun tekstiin, mikäli se on mahdollista. Toisen kerran painettaessa teksti kopioidaan leikepöydälle.|
|Siirrä tarkastelukohdistin kopioitavaksi merkityn tekstin alkukohtaan |`NVDA+Vaihto+F9` |`NVDA+Vaihto+F9` |Ei mitään |Siirtää tarkastelukohdistimen aiemmin kopioitavaksi merkityn tekstin alkukohtaan.|
|Puhu tekstin muotoilutiedot |`NVDA+Vaihto+F` |`NVDA+Vaihto+F` |Ei mitään |Puhuu tarkastelukohdistimen nykyisessä sijainnissa olevan tekstin muotoilutiedot. Kahdesti painettaessa ne näytetään selaustilassa.|
|Puhu nykyisen symbolin korvaava teksti |Ei mitään |Ei mitään |Ei mitään |Puhuu tarkastelukohdistimen kohdalla olevan symbolin ja näyttää kahdesti painettaessa selaustilassa sekä symbolin että sen korvaavan tekstin.|

<!-- KC:endInclude -->

Huom: `Num Lockin` on oltava pois käytöstä, jotta laskinnäppäimistön näppäimet toimivat oikein.

Hyvä keino tekstin tarkastelun peruskomentojen muistamiseen pöytäkoneen näppäinasettelua käytettäessä on ajatella niitä kolme kertaa kolme ruudukkona, jossa on ylhäältä alas rivi, sana ja merkki sekä vasemmalta oikealle edellinen, nykyinen ja seuraava.
Asettelua havainnollistetaan seuraavasti:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Edellinen rivi |Nykyinen rivi |Seuraava rivi|
|Edellinen sana |Nykyinen sana |Seuraava sana|
|Edellinen merkki |Nykyinen merkki |Seuraava merkki|

### Tarkastelutilat {#ReviewModes}

NVDA:n [tekstintarkastelukomennot](#ReviewingText) lukevat tekstiä valitusta tarkastelutilasta riippuen joko nykyisessä navigointiobjektissa, asiakirjassa tai ruudussa.

Seuraavat komennot vaihtavat tarkastelutilojen välillä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kosketusele |Kuvaus|
|---|---|---|---|---|
|Vaihda seuraavaan tarkastelutilaan |`NVDA+Laskinnäppäimistön 7` |`NVDA+Page up` |Pyyhkäisy ylös kahdella sormella |Vaihtaa seuraavaan käytettävissä olevaan tarkastelutilaan.|
|Vaihda edelliseen tarkastelutilaan |`NVDA+Laskinnäppäimistön 1` |`NVDA+Page down` |Pyyhkäisy alas kahdella sormella |Vaihtaa edelliseen käytettävissä olevaan tarkastelutilaan.|

<!-- KC:endInclude -->

#### Objektintarkastelu {#ObjectReview}

Objektintarkastelutilassa on mahdollista tarkastella vain nykyisen [navigointiobjektin](#ObjectNavigation) sisältöä.
Se on yleensä tekstiä sellaisissa objekteissa kuin muokattavat tekstikentät tai muut perustekstisäätimet.
Muissa objekteissa sisältöä voivat olla kyseisten objektien nimi ja/tai arvo.

#### Asiakirjan tarkastelu {#DocumentReview}

Asiakirjan tarkastelutilaan on mahdollista vaihtaa [Navigointiobjektin](#ObjectNavigation) ollessa selaustila-asiakirjassa (esim. verkkosivulla) tai muussa monisisältöisessä asiakirjassa (esim. Lotus Symphonyssa).
Tässä tilassa voidaan tarkastella koko asiakirjan sisältöä.

Tarkastelukohdistin sijoitetaan asiakirjassa navigointiobjektin kohdalle vaihdettaessa objektin tarkastelusta asiakirjan tarkasteluun.
Kun asiakirjassa liikutaan tarkastelukomennoilla, navigointiobjekti siirretään automaattisesti tarkastelukohdistimen nykyisessä kohdassa olevaan objektiin.

Huom: NVDA vaihtaa automaattisesti objektin tarkastelusta asiakirjan tarkasteluun selaustila-asiakirjoissa liikuttaessa.

#### Ruudun tarkastelu {#ScreenReview}

Ruuduntarkastelutilan avulla voidaan tarkastella ruudulla olevaa tekstiä sellaisena kuin se näkyy visuaalisesti nykyisessä sovelluksessa.
Tämä muistuttaa useiden muiden Windows-ruudunlukuohjelmien ruuduntarkastelu- tai hiirikohdistintoimintoa.

Tarkastelukohdistin sijoitetaan ruuduntarkastelutilaan vaihdettaessa ruudulla nykyisen [navigointiobjektin](#ObjectNavigation) kohdalle.
Kun ruudulla liikutaan tarkastelukomennoilla, navigointiobjekti siirretään automaattisesti tarkastelukohdistimen kohdalla olevaan objektiin.

Huom: NVDA ei ehkä pysty lukemaan kaikkea tai mitään ruudulla olevaa tekstiä joissakin uudemmissa sovelluksissa edistyneempien ruudunpiirtomenetelmien vuoksi, joita ei toistaiseksi tueta.

### Hiirellä liikkuminen {#NavigatingWithTheMouse}

Kun hiirtä liikutetaan, NVDA puhuu oletusarvoisesti suoraan sen alla olevan tekstin.
NVDA lukee myös hiirikohdistinta ympäröivän tekstikappaleen mikäli se on mahdollista, vaikka joissakin säätimissä lukeminen on mahdollista vain riveittäin.

NVDA voidaan määrittää puhumaan myös hiiren alla olevan [objektin](#Objects) tyypin (esim. luettelo, painike jne).
Tästä voi olla hyötyä täysin sokeille käyttäjille, sillä joskus pelkän tekstin lukeminen ei riitä.

NVDA tarjoaa käyttäjille tavan ymmärtää, missä hiiri on ruudun mittojen suhteen toistamalla hiiren nykyiset koordinaatit äänimerkkeinä.
Mitä ylempänä hiiri on ruudulla, sitä korkeampia äänimerkit ovat.
Mitä enemmän vasemmalla tai oikealla hiiri on ruudulla, sitä enemmän vasemmalta tai oikealta ääni kuuluu (mikäli käytössä on stereokaiuttimet tai kuulokkeet).

Nämä lisäominaisuudet eivät ole oletusarvoisesti käytössä.
Voit halutessasi ottaa ne käyttöön [Hiiri](#MouseSettings)-kategoriasta [Asetukset](#NVDASettings)-valintaikkunasta, johon pääsee NVDA:n Asetukset-valikosta.

Vaikka hiiren avulla liikkumiseen tulisikin käyttää fyysistä hiirtä tai kosketuslevyä, on NVDA:ssa joitakin hiiren käyttöön tarkoitettuja näppäinkomentoja:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kosketusele |Kuvaus|
|---|---|---|---|---|
|Vasemman hiiripainikkeen napsautus |`Laskinnäppäimistön jakomerkki (/)` |`NVDA+Ö` |Ei mitään |Napsauttaa kerran hiiren vasenta painiketta. Kaksoisnapsautus tehdään painamalla tätä näppäinkomentoa kaksi kertaa nopeasti peräkkäin.|
|Vasemman hiiripainikkeen lukitus |`Vaihto+Laskinnäppäimistön jakomerkki (/)` |`NVDA+Ctrl+Ö` |Ei mitään |Lukitsee vasemman hiiripainikkeen alas. Lukitus vapautetaan painamalla tätä näppäinkomentoa uudelleen. Hiirellä vetäminen tehdään painamalla tätä näppäinkomentoa vasemman painikkeen lukitsemiseksi ja siirtämällä sitten hiirtä joko fyysisesti tai käyttämällä jotakin muista hiiren siirtämiskomennoista.|
|Oikean hiiripainikkeen napsautus |`Laskinnäppäimistön kertomerkki (*)` |`NVDA+Ä` |Napauta ja pidä |Napsauttaa kerran hiiren oikeaa painiketta. Käytetään useimmiten pikavalikon avaamiseen hiiren sijainnissa.|
|Oikean hiiripainikkeen lukitus |`Vaihto+Laskinnäppäimistön kertomerkki (*)` |`NVDA+Ctrl+Ä` |Ei mitään |Lukitsee oikean hiiripainikkeen alas. Lukitus vapautetaan painamalla tätä näppäinkomentoa uudelleen. Hiirellä vetäminen tehdään painamalla tätä komentoa oikean painikkeen lukitsemiseksi ja siirtämällä sitten hiirtä joko fyysisesti tai käyttämällä jotakin muista hiiren siirtämiskomennoista.|
|Siirrä hiiri nykyiseen navigointiobjektiin |`NVDA+Laskinnäppäimistön jakomerkki (/)` |`NVDA+Vaihto+M` |Ei mitään |Siirtää hiiren nykyisen navigointiobjektin ja tarkastelukohdistimen sijaintiin.|
|Siirrä hiiren alla olevaan objektiin |`NVDA+Laskinnäppäimistön kertomerkki (*)` |`NVDA+Vaihto+N` |Ei mitään |Siirtää navigointiobjektin hiiren alla olevaan objektiin.|

<!-- KC:endInclude -->

## Selaustila {#BrowseMode}

Monisisältöisiä, ei-muokattavia asiakirjoja kuten verkkosivuja luetaan NVDA:lla selaustilaa käyttäen.
Tällaisia asiakirjoja voidaan lukea seuraavissa sovelluksissa:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Microsoft Outlook (HTML-viestit)
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Amazon Kindle for PC (tuetut kirjat)

Selaustila on käytettävissä valinnaisesti myös Microsoft Wordissa.

Selaustilassa asiakirjan sisältö on käytettävissä kokonaisesityksenä, jossa voidaan liikkua nuolinäppäimillä, aivan kuin se olisi tavallinen tekstiasiakirja.
Kaikki NVDA:n [järjestelmäkohdistimen](#SystemCaret) näppäinkomennot, kuten esim. jatkuva luku ja lue muotoilut, taulukoissa liikkumiseen käytettävät komennot jne, toimivat tässä tilassa.
Kun [visuaalinen korostus](#VisionFocusHighlight) on käytössä, virtuaalisen selaustilakohdistimen sijainti näytetään myös visuaalisesti.
Asiakirjassa liikuttaessa luetaan siinä olevan tekstin lisäksi myös muita tietoja, kuten linkit, otsikot jne.

Toisinaan on oltava suorassa vuorovaikutuksessa tällaisissa asiakirjoissa olevien säädinten kanssa.
Tämä on tarpeen esimerkiksi muokattavissa tekstikentissä ja luetteloissa, jotta voidaan syöttää merkkejä ja käyttää nuolinäppäimiä säätimessä liikkumiseen.
Tämä tehdään siirtymällä vuorovaikutustilaan, jossa lähes kaikki näppäilyt välitetään kyseessä olevalle säätimelle.
NVDA siirtyy oletusarvoisesti selaustilasta vuorovaikutustilaan automaattisesti liikuttaessa tätä tilaa edellyttävän objektin kohdalle `Sarkain`-näppäimellä tai napsautettaessa sitä hiirellä.
Vastaavasti `Sarkaimella` siirtyminen tai sellaisen säätimen napsauttaminen, joka ei edellytä vuorovaikutustilaa, siirtää takaisin selaustilaan.
Vuorovaikutustilaan voidaan siirtyä myös painamalla sitä edellyttävien säädinten kohdalla `Enteriä` tai `Välilyöntiä`.
Takaisin selaustilaan siirrytään painamalla `Esc`-näppäintä.
Vuorovaikutustila voidaan lisäksi ottaa käyttöön manuaalisesti, jolloin se pysyy toiminnassa siihen asti kunnes se poistetaan käytöstä.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vaihda selaus- ja vuorovaikutustilojen välillä |`NVDA+Väli` |Vaihtaa vuorovaikutus- ja selaustilojen välillä.|
|Poistu vuorovaikutustilasta |`Esc` |Siirtää takaisin selaustilaan, mikäli NVDA siirtyi aiemmin automaattisesti vuorovaikutustilaan.|
|Päivitä selaustila-asiakirja |`NVDA+F5` tai `NVDA+Esc` |Lataa uudelleen nykyisen asiakirjan sisällön. (Hyödyllinen, jos sivulta vaikuttaa puuttuvan jotakin. Komento ei ole käytettävissä Microsoft Wordissa tai Outlookissa.)|
|Etsi |`NVDA+Ctrl+F` tai `Ctrl+F` |Avaa valintaikkunan, jossa voidaan etsiä tekstiä nykyisestä asiakirjasta. Katso lisätietoja [Tekstin etsiminen](#SearchingForText) -osiosta.|
|Etsi seuraava |`NVDA+F3` tai `F3` |Etsii asiakirjasta aiemmin haetun tekstin seuraavan esiintymän.|
|Etsi edellinen |`NVDA+Vaihto+F3` tai `Vaihto+F3` |Etsii asiakirjasta aiemmin haetun tekstin edellisen esiintymän.|

<!-- KC:endInclude -->

### Pikanavigointinäppäimet {#SingleLetterNavigation}

NVDA:ssa on selaustilaa käytettäessä liikkumisen nopeuttamiseksi myös pikanavigointikomentoja, joilla voidaan siirtyä asiakirjan eri elementteihin.
HUOM: Kaikkia komentoja ei tueta joissakin asiakirjatyypeissä.

<!-- KC:beginInclude -->
Sellaisinaan nämä komennot siirtävät seuraavan ja `Vaihto`-näppäimen kanssa painettuna edellisen elementin kohdalle:

* `H`: otsikko
* `L`: luettelo
* `I`: luettelokohde
* `T`: taulukko
* `K`: linkki
* `N`: teksti, joka ei ole linkki
* `F`: lomakekenttä
* `U`: vierailematon linkki
* `V`: vierailtu linkki
* `E`: muokkauskenttä
* `B`: painike
* `X`: valintaruutu
* `C`: yhdistelmäruutu
* `R`: valintapainike
* `Q`: sisennetty lainaus
* `S`: erotin
* `M`: kehys
* `G`: grafiikka
* `D`: kiintopiste
* `O`: upotettu objekti (ääni- ja videosoitin, sovellus, valintaikkuna jne.)
* Numerot `1–6`: otsikot tasoilla 1–6
* `A`: merkintä (kommentti, muokkaajan muutokset jne.)
* `P`: kappale
* `W`: kirjoitusvirhe

Säilöelementtien, kuten luetteloiden ja taulukoiden alkuun tai loppuun siirtymiseen:

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Siirrä säilöelementin alkuun |`Vaihto+pilkku` |Siirtää sen säilöelementin alkuun, jossa kohdistin on (luettelo, taulukko jne).|
|Siirrä säilöelementin loppuun |`Pilkku` |Siirtää sen säilöelementin loppuun, jossa kohdistin on (luettelo, taulukko jne).|

<!-- KC:endInclude -->

Joissakin uusissa verkkopohjaisissa sovelluksissa, kuten Gmail, Twitter ja Facebook, käytetään yksikirjaimisia pikanäppäimiä.
Mikäli halutaan samaan aikaan käyttää sekä niitä että nuolinäppäimiä selaustilassa lukemiseen, NVDA:n pikanavigointinäppäimet voidaan poistaa tilapäisesti käytöstä.
<!-- KC:beginInclude -->
Ota käyttöön tai poista käytöstä pikanavigointinäppäimet nykyisessä asiakirjassa painamalla `NVDA+Vaihto+Väli`.
<!-- KC:endInclude -->

#### Tekstikappaleiden navigointikomento {#TextNavigationCommand}

Voit siirtyä seuraavaan tai edelliseen tekstikappaleeseen painamalla `P` tai `Vaihto+P`.
Tekstikappaleet määritellään tekstiryhmiksi, jotka näyttävät kokonaisin lausein kirjoitetuilta.
Tästä voi olla hyötyä luettavan sisällön alun löytämisessä erilaisilla verkkosivuilla, kuten:

* Uutissivustot
* Foorumit
* Blogikirjoitukset

Nämä komennot voivat myös auttaa ohittamaan tiettyjä häiriötekijöitä, kuten:

* Mainokset
* Valikot
* Otsikot

Huomaa kuitenkin, että vaikka NVDA pyrkii parhaansa mukaan tunnistamaan tekstikappaleet, algoritmi ei ole täydellinen ja saattaa joskus tehdä virheitä.
Lisäksi tämä komento eroaa kappalenavigointikomennoista `Ctrl+Nuoli alas/ylös`.
Tekstikappalenavigointi siirtää vain tekstikappaleiden välillä, kun taas kappalenavigointikomennot siirtävät kohdistimen edelliseen/seuraavaan kappaleeseen riippumatta siitä, sisältävätkö ne tekstiä vai ei.

#### Muut navigointikomennot {#OtherNavigationCommands}

NVDA:ssa on yllä lueteltujen pikanavigointikomentojen lisäksi komentoja, joille ei ole määritetty oletusnäppäimiä.
Käytä näitä komentoja määrittämällä niille ensin näppäimet [Näppäinkomennot-valintaikkunan](#InputGestures) avulla.
Tässä on luettelo käytettävissä olevista komennoista:

* Artikkeli
* Kuva
* Ryhmä
* Välilehti
* Valikkokohde
* Vaihtopainike
* Edistymispalkki
* Matemaattinen kaava
* Pystysuunnassa tasattu kappale
* Samantyylinen teksti
* Eri tyylinen teksti

Muista, että kullekin elementtityypille on komennot eteen- ja taaksepäin siirtymistä varten, ja sinun on määritettävä näppäimet molemmille, jotta voit siirtyä nopeasti molempiin suuntiin.
Jos esimerkiksi haluat käyttää `Y`- ja `Vaihto+Y`-näppäimiä välilehtien välillä siirtymiseen, sinun tulee tehdä seuraavasti:

1. Avaa Näppäinkomennot-valintaikkuna selaustilan ollessa aktiivisena.
1. Etsi Selaustila-osiosta "Siirtää seuraavan välilehden kohdalle" -komento.
1. Määritä löytyneelle komennolle `Y`-näppäin.
1. Etsi "Siirtää edellisen välilehden kohdalle" -komento.
1. Määritä löytyneelle komennolle `Vaihto+Y`-näppäimet.

### Elementtilista {#ElementsList}

Elementtilista mahdollistaa pääsyn asiakirjassa oleviin eri elementteihin, joita sovellus tukee.
Esimerkiksi verkkoselaimissa voidaan näyttää luettelo linkeistä, otsikoista, lomakekentistä, painikkeista tai kiintopisteistä.
Valintapainikkeilla voidaan valita eri elementtityyppien väliltä.
Valintaikkunassa on myös muokkauskenttä, jonka avulla luetteloa on mahdollista suodattaa jonkin tietyn kohteen etsimiseksi asiakirjasta.
Kun haluttu kohde on valittu, sen kohdalle voidaan siirtyä tai se voidaan avata käyttämällä valintaikkunassa olevia painikkeita.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Selaustilan elementtilista |`NVDA+F7` |Näyttää luettelon nykyisen asiakirjan sisältämistä eri tyyppisistä elementeistä.|

<!-- KC:endInclude -->

### Tekstin etsiminen {#SearchingForText}

Tämän valintaikkunan avulla voidaan etsiä tekstiä nykyisestä asiakirjasta.
Teksti kirjoitetaan "Kirjoita etsittävä teksti" -kenttään.
"Sama kirjainkoko" -valintaruutu saa haun käsittelemään isoja ja pieniä kirjaimia eri tavalla.
Esim. kun tämä on valittuna, teksti "NV Access" löytyy, muttei tekstiä "nv access".
hakujen suorittamiseen käytetään seuraavia näppäimiä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |kuvaus|
|---|---|---|
|Etsi tekstiä |`NVDA+Ctrl+F` tai `Ctrl+F` |Avaa Etsi-valintaikkunan.|
|Etsi seuraava |`NVDA+F3` tai `F3` |Etsii asiakirjasta aiemmin haetun tekstin seuraavan esiintymän.|
|Etsi edellinen |`NVDA+Vaihto+F3` tai `Vaihto+F3` |Etsii asiakirjasta aiemmin haetun tekstin edellisen esiintymän.|

<!-- KC:endInclude -->

### Upotetut objektit {#ImbeddedObjects}

Sivut voivat sisältää monipuolista sisältöä, jossa käytetään sellaisia tekniikoita kuin Java, HTML5, kuten myös sovelluksia ja valintaikkunoita.
Kun selaustilassa tullaan niiden kohdalle, NVDA ilmoittaa "upotettu objekti", "sovellus" tai "valintaikkuna".
Niihin voidaan siirtyä nopeasti käyttäen upotettuihin objekteihin siirtäviä pikanavigointinäppäimiä `O` ja `Vaihto+O`.
Näiden objektien kanssa voidaan olla vuorovaikutuksessa painamalla `Enteriä` niiden kohdalla.
Jos objekti on saavutettava, siinä voidaan liikkua `Sarkain-näppäimellä` ja olla sen kanssa vuorovaikutuksessa kuten missä tahansa muussakin sovelluksessa.
Seuraavalla näppäinkomennolla voidaan palata alkuperäiselle upotetun objektin sisältävälle sivulle:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Siirrä upotetun objektin sisältävään selaustila-asiakirjaan |`NVDA+Ctrl+Väli` |Siirtää kohdistuksen pois nykyisestä upotetusta objektista asiakirjaan, jossa se on.|

<!-- KC:endInclude -->

### Alkuperäinen valintatila {#NativeSelectionMode}

Kun tekstiä valitaan selaustilassa `Vaihto+Nuolinäppäimillä`, valinta tehdään oletusarvoisesti vain NVDA:n muodostamassa asiakirjan selaustilaesityksessä eikä sovelluksen sisällä.
Tämä tarkoittaa, että valinta ei näy näytöllä, ja tekstin kopiointi `Ctrl+C`-näppäinyhdistelmällä kopioi vain NVDA:n tekstiesityksen sisällöstä. Eli taulukoiden muotoilu tai linkit eivät välity kopioitaessa.
NVDA:ssa on kuitenkin alkuperäinen valintatila, joka voidaan ottaa käyttöön tietyissä selaustila-asiakirjoissa (tällä hetkellä vain Mozilla Firefoxissa), mikä saa asiakirjan alkuperäisen valinnan seuraamaan NVDA:n selaustilan valintaa.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Ota käyttöön tai poista käytöstä alkuperäinen valintatila |`NVDA+Vaihto+F10` |Ottaa käyttöön tai poistaa käytöstä alkuperäisen valintatilan.|

<!-- KC:endInclude -->

Kun alkuperäinen valintatila on käytössä, valinnan kopioiminen `Ctrl+C`-näppäinyhdistelmällä käyttää myös sovelluksen omaa kopiointitoimintoa, mikä merkitsee, että rikas sisältö kopioituu leikepöydälle pelkän tekstin sijaan.
Tämä tarkoittaa, että muotoilu, kuten taulukot tai linkit, säilytetään, kun sisältö liitetään johonkin ohjelmaan, kuten Microsoft Wordiin tai Exceliin.
Huomaa kuitenkin, että jotkin NVDA:n selaustilassa luomat saavutettavuusselitteet tai muut tiedot menetetään.
Lisäksi, vaikka sovellus pyrkii parhaansa mukaan säilyttämään alkuperäisen valinnan sisällön NVDA:n selaustilan valintaa vastaavana, lopputulos ei välttämättä aina ole täysin tarkka.
Tämä toiminto voi Kuitenkin olla hyödyllinen tilanteissa, joissa haluat kopioida koko taulukon tai kappaleen sisällön muotoiluineen.

## Matemaattisen sisällön lukeminen {#ReadingMath}

NVDA:n avulla on mahdollista lukea ja liikkua verkossa ja muissa soveluksissa olevassa matemaattisessa sisällössä tarjoten pääsyn sekä puheella että pistekirjoituksella.
Jotta matemaattista sisältöä voidaan lukea ja olla vuorovaikutuksessa sen kanssa, NVDA:han on ensin asennettava matemaattisen sisällön komponentti.
NVDA:n lisäosakaupasta löytyy useita matemaattisen sisällön tuen tarjoavia lisäosia, kuten [MathCAT](https://nsoiffer.github.io/MathCAT/) ja [Access8Math](https://github.com/tsengwoody/Access8Math).
Katso [Lisäosakauppa-luvusta](#AddonsManager) tietoja lisäosien selaamisesta ja asentamisesta.
Mikäli Wirisin [MathPlayer](https://info.wiris.com/mathplayer-info)-ohjelmisto on asennettuna, NVDA voi käyttää myös sitä, vaikka sitä ei enää ylläpidetä.

### Tuettu matemaattinen sisältö {#SupportedMathContent}

Sopivan matematiikkakomponentin asennuksen jälkeen NVDA tukee seuraavia matemaattisen sisällön tyyppejä:

* MathML Mozilla Firefoxissa, Internet Explorerissa ja Google Chromessa.
* Microsoft Word 365:n uudet matemaattiset yhtälöt UI Automationin välityksellä:
NVDA pystyy lukemaan ja olemaan vuorovaikutuksessa matemaattisten yhtälöiden kanssa Microsoft Word 365:n/2016:n koontikäännösversiossa 14326 ja uudemmissa.
Huomaa kuitenkin, että kaikki aiemmin luodut MathType-yhtälöt on ensin muunnettava Office Mathiksi.
Tämä tehdään valitsemalla muunnettavat yhtälöt ja valitsemalla sitten pikavalikosta Yhtälön asetukset -> Muunna Office Mathiksi.
Varmista ennen muunnoksen suorittamista, että käytössäsi on viimeisin MathType-versio.
Microsoft Word tarjoaa nyt myös lineaarisen, symbolipohjaisen yhtälöissä liikkumisen, ja tukee matemaattisten merkkien syöttämistä useita syntakseja käyttäen, LateX mukaan lukien.
Katso lisätietoja artikkelista [Lineaarisen muodon kaavat UnicodeMathin ja LaTeXin avulla Wordissa](https://support.microsoft.com/fi-fi/office/lineaarisen-muodon-kaavat-unicodemathin-ja-latexin-avulla-wordissa-2e00618d-b1fd-49d8-8cb4-8d17f25754f8).
* Microsoft Powerpoint ja vanhemmat Microsoft Wordin versiot:
NVDA voi lukea MathType-yhtälöitä ja liikkua niissä sekä Microsoft Powerpointissa että Microsoft Wordissa.
MathTypen on oltava asennettuna.
Kokeiluversio riittää.
Sen voi ladata [MathTypen esittelysivulta](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Huom: Tämä ei ole vielä virallinen standardi, joten sisältöä tuottavaa ohjelmistoa ei ole julkisesti saatavilla.
* Kindle Reader for PC:
NVDA voi lukea kirjojen saavutettavaa matemaattista sisältöä Kindle for PC:ssä.

NVDA puhuu aina asiakirjaa luettaessa kaiken siinä mahdollisesti olevan tuetun matemaattisen sisällön.
Mikäli käytät pistenäyttöä, sisältö näytetään myös pistekirjoituksena.

### Vuorovaikutteinen liikkuminen {#InteractiveNavigation}

Jos käytät pääasiassa pelkkää puhetta, haluat useimmiten luultavasti tutkia lauseketta pienemmissä osissa sen sijaan, että kuuntelisit sen kerralla kokonaan.

Tämä tehdään selaustilassa oltaessa siirtämällä kohdistin matemaattiseen sisältöön ja painamalla Enter.

Mikäli et ole selaustilassa:

1. Siirrä tarkastelukohdistin matemaattiseen sisältöön.
Tarkastelukohdistin seuraa oletusarvoisesti järjestelmäkohdistinta, joten voit yleensä käyttää jälkimmäistä haluttuun sisältöön siirtymiseen.
1. Aktivoi sitten seuraava komento:

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vuorovaikutus matemaattisen sisällön kanssa |NVDA+Alt+M |Aloittaa vuorovaikutuksen matemaattisen sisällön kanssa.|

<!-- KC:endInclude -->

Tässä vaiheessa NVDA siirtyy matematiikkatilaan, jossa voit käyttää tiettyjä komentoja, kuten nuolinäppäimiä lausekkeen tutkimiseen.
Lausekkeessa voit liikkua vasemmalla ja oikealla nuolinäppäimellä sekä zoomata johonkin tiettyyn osaan kuten murtolukuun Nuoli alas -näppäintä käyttäen.

Palaa takaisin asiakirjaan painamalla Esc-näppäintä.

Lisätietoja matemaattisen sisällön lukemiseen ja siinä liikkumiseen käytettävissä olevista komennoista ja asetuksista saat asentamasi matematiikkakomponentin dokumentaatiosta.

* [MathCATin dokumentaatio](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Mathin dokumentaatio](https://github.com/tsengwoody/Access8Math)
* [MathPlayerin dokumentaatio](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Toisinaan matemaattinen sisältö saatetaan näyttää painikkeena tai muuntyyppisenä elementtinä, joka voi näyttää aktivoitaessa valintaikkunan tai lisätietoja kaavasta.
Aktivoi kaavan sisältävä painike tai elementti painamalla Ctrl+Enter.

### MathPlayerin asentaminen {#InstallingMathPlayer}

Vaikka yleensä NVDA:n kanssa suositellaankin käytettäväksi uudempia lisäosia matemaattisen sisällön tukemiseen, tietyissä rajoitetuissa skenaarioissa MathPlayer voi silti olla parempi valinta.
Esimerkiksi MathPlayer saattaa tukea jotain tiettyä kieltä tai pistekirjoitusmerkistöä, jota uudemmat lisäosat eivät tue.
MathPlayer on saatavilla ilmaiseksi Wirisin verkkosivustolta.
[Lataa MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Asennuksen jälkeen sinun täytyy käynnistää NVDA uudelleen.
Huomaa, että MathPlayerin tiedoissa saattaa olla maininta, että se on tarkoitettu vain vanhemmille selaimille, kuten Internet Explorer 8.
Tämä viittaa vain siihen, jos MathPlayeria käytetään matemaattisen sisällön visuaaliseen näyttämiseen, eikä NVDA-käyttäjien tarvitse välittää siitä.

## Pistekirjoitus {#Braille}

NVDA voi antaa palautteen pistekirjoituksella, mikäli käytössä on pistenäyttö.
Jos näytössä on Perkins-tyylinen näppäimistö, lisäksi on mahdollista syöttää lyhenne- ja tavallista pistekirjoitusta.
Pistekirjoitus voidaan näyttää fyysisen pistenäytön asemesta tai sen lisäksi myös ruudulla [pistekirjoituksen tarkastelua](#BrailleViewer) käyttäen.

Tietoja tuetuista pistenäytöistä on [Tuetut pistenäytöt](#SupportedBrailleDisplays) -osiossa.
Tässä kappaleessa on tietoja myös NVDA:n automaattista pistenäytön tunnistusta tukevista näytöistä.
Pistekirjoituksen asetukset määritetään [Asetukset](#NVDASettings)-valintaikkunan [Pistekirjoitus-kategoriasta](#BrailleSettings).

### Säädintyyppien ja -tilojen sekä kiintopisteiden lyhenteet {#BrailleAbbreviations}

Jotta pistenäytölle mahtuisi mahdollisimman paljon tietoa, seuraavat lyhenteet on määritetty ilmaisemaan säätimen tyyppiä ja tilaa sekä kiintopisteitä.

| Lyhenne |Säätimen tyyppi|
|---|---|
|sov |sovellus|
|art |artikkeli|
|sln |sisennetty lainaus|
|pnk |painike|
|avpnk |avattava painike|
|askpnk |askelluspainike|
|jtupnk |jaettu painike|
|vtpnk |vaihtopainike|
|kvt |kuvateksti|
|yhd |yhdistelmäruutu|
|vlr |valintaruutu|
|vli |valintaikkuna|
|asi |asiakirja|
|muo |muokattava tekstikenttä|
|slsmuo |salasanan muokkauskenttä|
|upotettu |upotettu objekti|
|lvt |loppuviite|
|kuv |kuva|
|avt |alaviite|
|gra |grafiikka|
|rhm |ryhmä|
|oN |otsikko tasolla n, esim. o1, o2.|
|ohj |ohjeselite|
|kp |kiintopiste|
|lnk |linkki|
|vlnk |vierailtu linkki|
|lto |luettelo|
|vko |valikko|
|vkorvi |valikkorivi|
|vkopnk |valikkopainike|
|vkokhde |valikkokohde|
|pnl |paneeli|
|edplk |edistymispalkki|
|vrtilm |varattu-ilmaisin|
|vpnk |valintapainike|
|vrtsplk |vierityspalkki|
|osa |osa|
|tlrvi |tilarivi|
|vlsdn |välilehtisäädin|
|tlk |taulukko|
|sN |Taulukon sarakenumero n, esim. s1, s2.|
|rN |Taulukon rivinumero n, esim. r1, r2.|
|pte |pääte|
|tkplk |työkalupalkki|
|tkvhj |työkaluvihje|
|pn |puunäkymä|
|pnpnk |puunäkymäpainike|
|pnkhde |puunäkymän kohde|
|ts N |puunäkymän kohteella on hierarkkinen taso N|
|ikk |ikkuna|
|⠤⠤⠤⠤⠤ |erotin|
|merk |merkitty sisältö|

Seuraavat tilanilmaisimet on myös määritetty:

| Lyhenne |Säätimen tila|
|---|---|
|... |Näytetään, kun objekti tukee automaattista täydennystä.|
|⢎⣿⡱ |Näytetään, kun objektia (esim. vaihtopainiketta) on painettu.|
|⢎⣀⡱ |Näytetään, kun objektia (esim. vaihtopainiketta) ei ole painettu.|
|⣏⣿⣹ |Näytetään, kun objekti (esim. valintaruutu) on valittuna.|
|⣏⣸⣹ |Näytetään, kun objekti (esim. valintaruutu) on osittain valittuna.|
|⣏⣀⣹ |Näytetään, kun objekti (esim. valintaruutu) ei ole valittuna.|
|- |Näytetään, kun objekti (esim. puunäkymän kohde) on tiivistettävissä.|
|+ |Näytetään, kun objekti (esim. puunäkymän kohde) on laajennettavissa.|
|*** |Näytetään, kun suojattu säädin tai asiakirja havaitaan.|
|nps |Näytetään, kun objekti on napsautettava.|
|kmnt |Näytetään, kun laskentataulukon solussa on kommentti tai asiakirjassa tekstiä.|
|kaav |Näytetään, kun laskentataulukon solussa on kaava.|
|virhe |Näytetään, kun virheellinen syöte on annettu.|
|ptkvs |Näytetään, kun objektista (yleensä grafiikka) on saatavilla pitkä kuvaus.|
|mnr |Näytetään, kun muokkauskenttä mahdollistaa useiden tekstirivien kirjoittamisen (esim. verkkosivujen kommenttikentät).|
|pak |Näytetään, kun pakollinen lomakekenttä havaitaan.|
|vl |Näytetään, kun objekti (esim. muokattava tekstikenttä) on vain luku -tyyppiä.|
|val |Näytetään, kun objekti on valittuna.|
|eval |Näytetään, kun objektia ei ole valittu.|
|laj nou |Näytetään, kun objekti on lajiteltu nousevasti.|
|laj lask |Näytetään, kun objekti on lajiteltu laskevasti.|
|avko |Näytetään, kun objektilla on ponnahdusvalikko (yleensä alivalikko).|

Kiintopisteille on määritetty seuraavat lyhenteet:

| Lyhenne |Kiintopiste|
|---|---|
|mplk |mainospalkki|
|stie |sisältötiedot|
|täyd |täydentävä|
|lom |lomake|
|pää |pääsisältö|
|nav |navigaatio|
|hku |haku|
|alu |alue|

### Pistekirjoituksen syöttäminen {#BrailleInput}

NVDA tukee sekä tavallisen että lyhennepistekirjoituksen syöttämistä pistekirjoitusnäppäimistöllä.
Käännöstaulukko, jota käytetään pistekirjoituksen kääntämiseen tekstiksi, voidaan valita [Asetukset](#NVDASettings)-valintaikkunan Pistekirjoitus-kategorian [Syöttötaulukko](#BrailleSettingsInputTable)-asetusta käyttäen.

Kun käytetään tavallista pistekirjoitusta, teksti syötetään heti sitä kirjoitettaessa.
Lyhennekirjoitusta käytettäessä teksti syötetään painettaessa sanan lopussa Välilyöntiä tai Enteriä.
Huom: Käännös vaikuttaa vain kirjoitettuun sanaan, ei olemassa olevaan tekstiin.
Jos esim. käytetään pistekirjoitusmerkistöä, jossa numerot alkavat numeromerkillä, ja painetaan Askelpalautinta numeron loppuun siirtymiseksi, numeromerkki on syötettävä uudelleen, jotta voidaan kirjoittaa lisää numeroita.

<!-- KC:beginInclude -->
Pisteen 7 painaminen poistaa viimeksi syötetyn pistesolun tai -merkin.
Piste 8 kääntää minkä tahansa pistekirjoitussyötteen ja painaa Enter-näppäintä.
Pisteiden 7 ja 8 painaminen kääntää minkä tahansa pistekirjoitussyötteen lisäämättä välilyöntiä tai painamatta Enteriä.
<!-- KC:endInclude -->

#### Pikanäppäinten syöttäminen {#BrailleKeyboardShortcuts}

NVDA tukee pikanäppäinten syöttämistä ja näppäinpainallusten jäljittelyä pistenäyttöä käyttäen.
Tätä jäljittelyä on kahdessa muodossa: pistesyötteen liittäminen suoraan johonkin näppäinpainallukseen ja virtuaalisten muokkausnäppäinten käyttäminen.

Yleisesti käytetyt näppäimet, kuten nuolinäppäimet tai Alt-näppäimen painaminen valikoiden avaamiseksi, voidaan liittää suoraan pistesyötteisiin.
Kunkin pistenäytön ajuri on valmiiksi varustettu joillakin näistä määrityksistä.
Voit muuttaa niitä tai lisätä uusia jäljiteltyjä näppäimiä [Näppäinkomennot-valintaikkunasta.](#InputGestures)

Vaikka tämä lähestymistapa on hyödyllinen usein painetuille tai yksilöllisille näppäimille (kuten Sarkain), et ehkä halua määrittää yksilöllistä näppäinsarjaa kullekin pikanäppäimelle.
NVDA tarjoaa komennot Ctrl-, Alt-, Vaihto-, Win- ja NVDA-näppäinten tilan vaihtamiseen sekä komennot joillekin näiden näppäinten yhdistelmille, mikä mahdollistaa sellaisten näppäinpainallusten jäljittelyn, joissa muokkausnäppäimiä pidetään alhaalla.
Käytä näitä tilanvaihtokomentoja painamalla ensin haluamiesi muokkausnäppäinten komentoa (tai komentosarjaa).
Syötä sitten merkki, joka on osa pikanäppäintä, jonka haluat suorittaa.
Tuota esim. Ctrl+F-pikanäppäin käyttämällä "Vaihda Ctrl-näppäimen tilaa" -komentoa ja kirjoittamalla F,
ja syötä Ctrl+Alt+T käyttäen joko "Vaihda Ctrl-näppäimen tilaa"- ja "Vaihda Alt-näppäimen tilaa" -komentoja kummassa tahansa järjestyksessä tai "Vaihda Ctrl- ja Alt-näppäinten tilaa" -komentoa ja kirjoittamalla T.

Jos vaihdat vahingossa muokkausnäppäinten tilaa, tilanvaihtokomennon uudelleen suorittaminen poistaa ne käytöstä.

Lyhennepistekirjoitusta syötettäessä muokkausnäppäinten tilanvaihtonäppäimien käyttäminen aiheuttaa syötteesi kääntämisen ikään kuin olisit painanut pisteitä 7 ja 8.
Lisäksi jäljitelty näppäinpainallus ei voi tuottaa pistekirjoitusta, joka on kirjoitettu ennen muokkausnäppäimen painamista.
Tämä tarkoittaa, että jos haluat antaa Alt+2-näppäinkomennon pistekirjoitusmerkistöllä, jossa käytetään numeromerkkiä, sinun on ensin vaihdettava Altin tilaa ja kirjoitettava sen jälkeen numeromerkki.

## Näkö {#Vision}

Vaikka NVDA on suunnattu ensisijaisesti sokeille tai heikkonäköisille, jotka käyttävät tietokonetta puheen/pistenäytön avulla, se tarjoaa myös sisäänrakennettuja palveluja ruudun sisällön muuttamiseen.
NVDA:ssa tällaista näön apuvälinettä kutsutaan näönparannuksen tarjoajaksi.

NVDA:han sisältyy useita sisäänrakennettuja näönparannuksen tarjoajia, jotka kuvaillaan alla.
Muita näönparannuksen tarjoajia on mahdollista lisätä [lisäosina.](#AddonsManager)

NVDA:n näön asetuksia voidaan muuttaa [asetusvalintaikkunan](#NVDASettings) [Näkö-kategoriasta.](#VisionSettings)

### Kohdistuksen korostus {#VisionFocusHighlight}

Kohdistuksen korostus voi auttaa tunnistamaan [kohdistuksen](#SystemFocus), [navigointiobjektin](#ObjectNavigation) ja virtuaalisen [selaustilakohdistimen](#BrowseMode) sijainnin.
Sijainnit korostetaan värillisellä, suorakulmaisella ääriviivalla.

* Kiinteä sininen korostaa yhdistetyn navigointiobjektin ja kohdistuksen sijainnin (esim. koska [navigointiobjekti seuraa kohdistusta.](#ReviewCursorFollowFocus))
* Sininen katkoviiva korostaa pelkän objektin, jossa kohdistus on.
* Kiinteä pinkki korostaa pelkän navigointiobjektin.
* Kiinteä keltainen korostaa virtuaalikohdistimen, jota käytetään selaustilassa (kuten verkkoselaimissa, joissa ei ole fyysistä kohdistinta).

Kun kohdistuksen korostus on otettu käyttöön [NVDA:n asetusvalintaikkunan](#NVDASettings) [Näkö-kategoriassa](#VisionSettings), voit [muuttaa, korostetaanko kohdistus, navigointiobjekti vai selaustilakohdistin.](#VisionSettingsFocusHighlight)

### Näyttöverho {#VisionScreenCurtain}

Sokeana tai heikkonäköisenä käyttäjänä ruudun sisältöä ei ole usein mahdollista tai tarpeellista nähdä.
Lisäksi voi olla vaikea varmistaa, ettei joku katso olkasi yli.
Tällaisia tilanteita varten NVDA:ssa on ominaisuus nimeltä näyttöverho, jonka käyttöön ottaminen pimentää ruudun.

Voit ottaa näyttöverhon käyttöön [NVDA:n asetusvalintaikkunan](#NVDASettings) [Näkö-kategoriassa](#VisionSettings).

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vaihda näyttöverhon tilaa |`NVDA+Ctrl+Esc` |Ottaa käyttöön tai poistaa käytöstä näyttöverhon. Pimennä näyttö ottamalla näyttöverho käyttöön tai näytä näytön sisältö poistamalla se käytöstä. Kerran painettaessa näyttöverho on käytössä, kunnes NVDA käynnistetään uudelleen. Kahdesti painettaessa se on käytössä, kunnes se poistetaan käytöstä.|

<!-- KC:endInclude -->

Kun näyttöverho on aktiivisena, jotkin näytöllä näkyvään tietoon perustuvat tehtävät, kuten [tekstintunnistuksen](#Win10Ocr) suorittaminen tai kuvakaappauksen ottaminen, eivät onnistu.

Windowsin suurennusrajapintaan tehdyn muutoksen takia näyttöverho oli päivitettävä tukemaan uusimpia Windows-versioita.
Käytä NVDA 2021.2:ta ottaaksesi näyttöverhon käyttöön Windows 10:n versiossa 21H2 (10.0.19044) tai sitä uudemmissa.
Varmista tietoturvasyistä visuaalisesti uutta Windows-versiota käytettäessä, että näyttöverho pimentää ruudun kokonaan.

Huom: Näyttöverhoa ei voida ottaa käyttöön, jos Windowsin suurennuslasia ja käänteisiä värejä käytetään samaan aikaan.

## Sisällöntunnistus {#ContentRecognition}

Kun tekijät eivät tarjoa riittävästi tietoa ruudunlukuohjelman käyttäjälle sisällön määrittämiseen, sitä voidaan yrittää tunnistaa kuvasta eri työkaluja käyttäen.
NVDA tukee Windowsin sisäänrakennettua tekstintunnistustoimintoa kuvissa olevan tekstin tunnistamiseen.
Lisää sisällöntunnistimia voidaan tarjota NVDA:n lisäosina.

Kun sisällöntunnistuskomentoa käytetään, NVDA tunnistaa nykyisen [navigointiobjektin](#ObjectNavigation) sisällön.
Navigointiobjekti seuraa oletusarvoisesti järjestelmän kohdistusta tai selaustilakohdistinta, joten yleensä kohdistus tai selaustilakohdistin voidaan siirtää haluttuun kohtaan.
Jos esim. siirrät selaustilakohdistimen grafiikan kohdalle, sen sisältö tunnistetaan.
Saatat kuitenkin haluta käyttää suoraan Objektinavigointia esim. koko sovellusikkunan tunnistamiseen.

Kun tunnistus on suoritettu, tulos näytetään selaustilaa vastaavassa asiakirjassa, joka mahdollistaa tietojen lukemisen nuolinäppäimillä jne.
Enterin tai Väli-näppäimen painaminen aktivoi (yleensä napsauttaa) kohdistimen kohdalla olevan tekstin, mikäli mahdollista.
Esc-näppäimen painaminen hylkää tunnistuksen tuloksen.

### Windowsin tekstintunnistus {#Win10Ocr}

Windows 10 ja uudemmat sisältävät tekstintunnistuksen useille kielille.
NVDA voi käyttää sitä kuvissa olevan tekstin tai esteellisten sovellusten tunnistamiseen.

Tekstintunnistuksen kieli Voidaan määrittää [Asetukset](#NVDASettings)-valintaikkunan [Windowsin tekstintunnistus -kategoriasta](#Win10OcrSettings).
Lisäkieliä on mahdollista asentaa avaamalla Käynnistä-valikko, valitsemalla Asetukset -> Aika ja kieli -> Alue ja kieli ja valitsemalla sitten Lisää kieli.

Kun haluat seurata jatkuvasti muuttuvaa sisältöä, kuten tekstityksiä videota katsellessasi, voit ottaa valinnaisesti käyttöön tunnistetun sisällön automaattisen päivittämisen.
Tämä onnistuu myös [Windowsin tekstintunnistus -kategorian](#Win10OcrSettings) kautta [NVDA:n asetukset](#NVDASettings) -valintaikkunassa.

Windowsin tekstintunnistus voi olla osittain tai täysin yhteensopimaton [NVDA:n näönparannusten](#Vision) tai muiden ulkoisten aputoimintojen kanssa. Sinun on poistettava käytöstä tällaiset aputoiminnot ennen tunnistuksen suorittamista.

<!-- KC:beginInclude -->
Tunnista nykyisen navigointiobjektin teksti Windowsin tekstintunnistusta käyttäen painamalla NVDA+R.
<!-- KC:endInclude -->

## Sovelluskohtaiset ominaisuudet {#ApplicationSpecificFeatures}

NVDA:ssa on joillekin sovelluksille omia lisäkomentoja tiettyjen tehtävien helpottamiseksi tai mahdollistamaan pääsyn sellaisiin toimintoihin, joiden käyttäminen ei ole ruudunlukuohjelman käyttäjille muilla tavoin mahdollista.

### Microsoft Word {#MicrosoftWord}
#### Sarake- ja riviotsikoiden automaattinen lukeminen {#WordAutomaticColumnAndRowHeaderReading}

NVDA voi ilmoittaa automaattisesti asianmukaiset rivi- ja sarakeotsikot Microsoft Wordissa taulukoissa liikuttaessa.
Tämä edellyttää, että Puhu taulukon rivi- ja sarakeotsikot -asetus on otettu käyttöön [NVDA:n Asetukset](#NVDASettings) -valintaikkunan Asiakirjojen muotoilu -kategoriasta.

Mikäli käytät [UIA:ta Word-asiakirjoille](#MSWordUIA), mikä on oletus uusimmissa Word- ja Windows-versioissa, ensimmäisen rivin solut tulkitaan automaattisesti sarakeotsikoiksi. Samoin ensimmäisen sarakkeen solut tulkitaan automaattisesti riviotsikoiksi.

Jos et käytä [UIA:ta Word-asiakirjoille](#MSWordUIA), NVDA:lle on ilmoitettava, mikä rivi tai sarake sisältää otsikot kulloisessakin taulukossa.
Kun olet siirtynyt ensimmäiseen soluun otsikoita sisältävässä sarakkeessa tai rivissä, käytä jotakin seuraavista komennoista:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Määritä sarakeotsikot |NVDA+Vaihto+C |Tämän komennon kerran painaminen kertoo NVDA:lle, että nykyinen solu on ensimmäinen otsikkosolu rivillä, joka sisältää sarakeotsikoita, jotka luetaan automaattisesti liikuttaessa sarakkeiden välillä kyseisen rivin alapuolella. Kahdesti painaminen nollaa tämän asetuksen.|
|Määritä riviotsikot |NVDA+Vaihto+R |Tämän komennon kerran painaminen kertoo NVDA:lle, että nykyinen solu on ensimmäinen otsikkosolu sarakkeessa, joka sisältää riviotsikoita, jotka luetaan automaattisesti liikuttaessa rivien välillä kyseisen sarakkeen oikealla puolella. Kahdesti painaminen nollaa tämän asetuksen.|

<!-- KC:endInclude -->
Asetukset tallennetaan asiakirjan kirjanmerkkeinä, jotka ovat yhteensopivia myös muiden ruudunlukuohjelmien, kuten JAWSin, kanssa.
Tämä tarkoittaa, että rivi- ja sarakeotsikot on jo valmiiksi määritelty muiden ruudunlukuohjelmien käyttäjille, jotka avaavat kyseisen asiakirjan.

#### Selaustila {#BrowseModeInMicrosoftWord}

Samoin kuin verkkosivuilla, myös Microsoft Wordissa selaustilaa voidaan käyttää pikanavigointiin ja elementtilistan hyödyntämiseen.
<!-- KC:beginInclude -->
Selaustila otetaan käyttöön tai poistetaan käytöstä painamalla NVDA+Väli.
<!-- KC:endInclude -->
Lisätietoja selaustilasta ja pikanavigoinnista on [Selaustila](#BrowseMode)-osiossa.

##### Elementtilista {#WordElementsList}

<!-- KC:beginInclude -->
Elementtilista avataan Microsoft Wordissa selaustilassa oltaessa painamalla NVDA+F7.
<!-- KC:endInclude -->
Elementtilista voi näyttää otsikot, linkit ja merkinnät (joita ovat kommentit ja jäljitettävät muutokset) sekä virheet (toistaiseksi vain kirjoitusvirheet).

#### Kommenttien lukeminen {#WordReportingComments}

<!-- KC:beginInclude -->
Kaikki kommentit luetaan järjestelmäkohdistimen nykyisestä kohdasta painamalla NVDA+Alt+C.
<!-- KC:endInclude -->
Kaikki asiakirjan kommentit muiden jäljitettävien muutosten ohella voidaan myös näyttää elementtilistassa, kun tyypiksi valitaan Merkinnät.

### Microsoft Excel {#MicrosoftExcel}
#### Sarake- ja riviotsikoiden automaattinen lukeminen {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA voi lukea automaattisesti asianmukaiset rivi- ja sarakeotsikot Excel-laskentataulukoissa liikuttaessa.
Tämä edellyttää ensinnäkin, että Lue taulukon rivi- ja sarakeotsikot -asetus on otettu käyttöön Asiakirjojen muotoiluasetuksista [Asetukset](#NVDASettings)-valintaikkunasta.
Toiseksi NVDA:n on tiedettävä, mikä rivi tai sarake sisältää otsikoita.
Kun on siirrytty ensimmäiseen soluun otsikoita sisältävässä sarakkeessa tai rivissä, käytetään jotakin seuraavista komennoista:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Määritä sarakeotsikot |NVDA+Vaihto+C |Tämän komennon kerran painaminen kertoo NVDA:lle, että nykyinen solu on ensimmäinen otsikkosolu rivillä, joka sisältää sarakeotsikoita, jotka luetaan automaattisesti liikuttaessa sarakkeiden välillä kyseisen rivin alapuolella. Kahdesti painaminen nollaa tämän asetuksen.|
|Määritä riviotsikot |NVDA+Vaihto+R |Tämän komennon kerran painaminen kertoo NVDA:lle, että nykyinen solu on ensimmäinen otsikkosolu sarakkeessa, joka sisältää riviotsikoita, jotka luetaan automaattisesti liikuttaessa rivien välillä kyseisen sarakkeen oikealla puolella. Kahdesti painaminen nollaa tämän asetuksen.|

<!-- KC:endInclude -->
Asetukset tallennetaan työkirjaan nimettyinä alueina, jotka ovat yhteensopivia myös muiden ruudunlukuohjelmien, kuten JAWSin, kanssa.
Tämä tarkoittaa, että rivi- ja sarakeotsikot on jo valmiiksi määritelty muiden ruudunlukuohjelmien käyttäjille, jotka avaavat kyseisen työkirjan.

#### Elementtilista {#ExcelElementsList}

Samoin kuin verkkosivuilla, myös Microsoft Exceliä varten on elementtilista, jonka avulla voidaan näyttää useita eri tyyppisiä tietoja.
<!-- KC:beginInclude -->
Elementtilista avataan painamalla NVDA+F7.
<!-- KC:endInclude -->
Elementtilistassa ovat käytettävissä seuraavat tiedot:

* Kaaviot: Näyttää luettelon kaikista aktiivisen laskentataulukon kaavioista.
Kaavion valitseminen ja Enterin tai Siirry-painikkeen painaminen siirtää kohdistuksen kyseiseen kaavioon, jolloin sitä on mahdollista selata ja lukea nuolinäppäimillä.
* Kommentit: Näyttää luettelon kaikista aktiivisen laskentataulukon soluista, joissa on kommentti.
Kustakin solusta näytetään osoitteen ohella sen sisältämät kommentit.
Enterin tai Siirry-painikkeen painaminen luettelossa olevan kommentin kohdalla siirtää suoraan kyseiseen soluun.
* Kaavat: Näyttää luettelon kaikista aktiivisen laskentataulukon soluista, joissa on kaava.
Kustakin solusta näytetään osoitteen ohella sen sisältämät kaavat.
Enterin tai Siirry-painikkeen painaminen luettelossa olevan kaavan kohdalla siirtää suoraan kyseiseen soluun.
* Laskentataulukot: Näyttää luettelon kaikista työkirjassa olevista laskentataulukoista.
Laskentataulukko voidaan nimetä uudelleen painamalla luettelossa sen kohdalla F2.
Enterin tai Siirry-painikkeen painaminen luettelossa olevan laskentataulukon kohdalla siirtää kyseiseen taulukkoon.
* Lomakekentät: Näyttää luettelon kaikista aktiivisen laskentataulukon lomakekentistä.
Kustakin lomakekentästä näytetään sen vaihtoehtoisen tekstin ohella peitossa olevien solujen osoitteet.
Lomakekentän valitseminen ja Enterin tai Siirry-painikkeen painaminen siirtää kyseiseen kenttään selaustilassa.

#### Muistiinpanojen lukeminen {#ExcelReportingComments}

<!-- KC:beginInclude -->
Lue mikä tahansa muistiinpano aktiivisesta solusta painamalla NVDA+Alt+C.
Excelin perinteiset kommentit on nimetty uudelleen "muistiinpanoiksi" Microsoft 2016:ssa, 365:ssä ja uudemmissa.
<!-- KC:endInclude -->
Kaikki laskentataulukossa olevat muistiinpanot voidaan näyttää myös elementtilistassa painamalla NVDA+F7.

NVDA voi myös näyttää erityisen muistiinpanojen lisäämiseen tai muokkaamiseen tarkoitetun valintaikkunan.
NVDA korvaa natiivin MS Excelin muistiinpanojen muokkausalueen saavutettavuusrajoitteiden takia, mutta valintaikkunan näyttämisen näppäinkomento periytyy Exceliltä, joten se toimii myös ilman NVDA:ta.
<!-- KC:beginInclude -->
Voit lisätä tai muokata muistiinpanoa aktiivisessa solussa painamalla Vaihto+F2.
<!-- KC:endInclude -->

Tämä komento ei näy eikä sitä voi muuttaa NVDA:n Näppäinkomennot-valintaikkunassa.

Huom: Muistiinpanojen muokkausalue on mahdollista avata Excelissä myös laskentataulukon solun pikavalikosta.
Tämä avaa kuitenkin esteellisen muokkausalueen eikä NVDA:n erityistä muokkausvalintaikkunaa.

Microsoft Office 2016:een, 365:een ja uudempiin on lisätty uudentyylinen kommenttivalintaikkuna.
Se on saavutettava ja tarjoaa enemmän ominaisuuksia, kuten kommentteihin vastaamisen jne.
Se voidaan avata myös solun pikavalikosta.
Uuden kommenttivalintaikkunan avulla soluihin lisätyt kommentit eivät liity muistiinpanoihin.

#### Suojattujen solujen lukeminen {#ExcelReadingProtectedCells}

Mikäli työkirja on suojattu, kohdistuksen siirtäminen ei ehkä ole mahdollista sellaisiin soluihin, joiden muokkaaminen on estetty.
<!-- KC:beginInclude -->
Lukittuihin soluihin siirtyminen on mahdollista selaustilassa, joka otetaan käyttöön painamalla NVDA+Väli, ja käyttämällä standardinmukaisia Excel-komentoja, kuten nuolinäppäimiä nykyisen laskentataulukon soluissa liikkumiseen.
<!-- KC:endInclude -->

#### Lomakekentät {#ExcelFormFields}

Excelin laskentataulukot voivat sisältää lomakekenttiä.
Niihin päästään elementtilistaa tai pikanavigointinäppäimiä F ja Vaihto+F käyttäen.
Kun selaustilassa siirrytään lomakekentän kohdalle, säätimestä riippuen voidaan joko aktivoida se tai vaihtaa vuorovaikutustilaan painamalla Enteriä tai välilyöntiä, jotta sen kanssa on mahdollista olla vuorovaikutuksessa.
Lisätietoja selaustilasta ja pikanavigointinäppäimistä on [Selaustila](#BrowseMode)-osiossa.

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Muuta esittäjän muistiinpanojen lukemista |Ctrl+Vaihto+S |Tämä komento vaihtaa esittäjän muistiinpanojen ja dian sisällön lukemisen välillä meneillään olevassa diaesityksessä oltaessa. Asetus ei vaikuta siihen, mitä näytöllä näkyy, vaan pelkästään siihen, mitä NVDA lukee.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Ilmoita jäljellä oleva aika |Ctrl+Vaihto+R |Ilmoittaa toistettavan kappaleen jäljellä olevan ajan.|
|Ilmoita kulunut aika |Ctrl+Vaihto+E |Ilmoittaa toistettavan kappaleen kuluneen ajan.|
|Ilmoita kappaleen kesto |Ctrl+Vaihto+T |Ilmoittaa toistettavan kappaleen keston.|

<!-- KC:endInclude -->

Huom: Yllä olevat näppäinkomennot toimivat vain foobar2000:n tilarivin muotoilun oletusmerkkijonolla.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Lue uusin viesti |NVDA+Ctrl+1-4 |Lukee jonkin uusimmista, painettua numeroa vastaavista viesteistä, esim. NVDA+Ctrl+2 lukee toiseksi uusimman.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA tarjoaa parannetun tuen Poedit 3.4:lle tai sitä uudemmille versioille.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Puhu huomautukset kääntäjille |`Ctrl+Vaihto+A` |Puhuu kääntäjille tarkoitetut huomautukset. Kahdesti painettaessa ne näytetään selaustilassa.|
|Puhu kommentti |`Ctrl+Vaihto+C` |Puhuu kommentti-ikkunassa olevan kommentin. Kahdesti painettaessa se näytetään selaustilassa.|
|Puhu vanha lähdeteksti |`Ctrl+Vaihto+O` |Puhuu vanhan lähdetekstin, mikäli sellainen löytyy. Kahdesti painettaessa se näytetään selaustilassa.|
|Puhu käännösvaroitus |`Ctrl+Vaihto+W` |Puhuu käännösvaroituksen, mikäli sellainen löytyy. Kahdesti painettaessa se näytetään selaustilassa.|

<!-- KC:endInclude -->

### Kindle for PC {#Kindle}

NVDA tukee kirjojen lukemista ja niissä liikkumista Amazonin Kindle for PC -sovelluksessa.
Tämä toiminnallisuus on käytettävissä vain kirjoissa, joihin on merkitty "Screen Reader: Supported", minkä voi tarkistaa kirjan Tiedot-sivulta (Details).

Kirjojen lukemiseen käytetään selaustilaa.
Se otetaan käyttöön automaattisesti kirjaa avattaessa tai kun kohdistus siirretään kirja-alueelle.
Sivua käännetään automaattisesti aina tarvittaessa kohdistinta siirrettäessä tai jatkuvaa lukua käytettäessä.
<!-- KC:beginInclude -->
Seuraavalle sivulle voidaan kääntää manuaalisesti painamalla Page down- ja edelliselle painamalla Page up -näppäintä.
<!-- KC:endInclude -->

Pikanavigointia tuetaan linkeille ja grafiikoille, mutta vain nykyisellä sivulla.
Linkkeihin siirtyminen sisältää myös alaviitteet.

NVDA tarjoaa alkeellisen tuen kirjojen saavutettavan matemaattisen sisällön lukemiselle ja vuorovaikutteiselle selaukselle.
Lisätietoja on [Matemaattisen sisällön lukeminen](#ReadingMath) -osiossa.

#### Tekstin valitseminen {#KindleTextSelection}

Kindlessä voidaan suorittaa valitulle tekstille eri toimintoja, mukaan lukien sanastomääritelmän hakeminen, huomautusten ja korostusten lisääminen, leikepöydälle kopioiminen sekä verkosta etsiminen.
Tämä tehdään valitsemalla ensin tekstiä kuten tavallisesti selaustilassa, esim. Vaihto- ja nuolinäppäimiä käyttäen.
<!-- KC:beginInclude -->
Kun teksti on valittu, painetaan sovellusnäppäintä tai Vaihto+F10 valinnan käsittelyyn käytettävissä olevien vaihtoehtojen näyttämiseksi.
<!-- KC:endInclude -->
Mikäli tekstiä ei ole valittuna, vaihtoehdot näytetään kohdistimen kohdalla olevalle sanalle.

#### Käyttäjän muistiinpanot {#KindleUserNotes}

Sanaan tai tekstin kohtaan voidaan lisätä muistiinpano.
Tämä tehdään valitsemalla ensin haluttu teksti ja avaamalla valinnan vaihtoehdot, kuten yllä on kuvailtu.
Valitaan sitten Add note.

NVDA viittaa selaustilassa luettaessa muistiinpanoihin kommentteina.

Muistiinpano luetaan, muokataan tai poistetaan seuraavasti:

1. Siirretään kohdistin kommentin sisältävään tekstiin.
1. Avataan valinnan vaihtoehdot, kuten yllä on kuvailtu.
1. Valitaan Edit note.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Lisättyjen kirjojen taulukkonäkymässä:

| Name |Key |Description|
|---|---|---|
|Enter |Enter |Avaa valitun kirjan.|
|Pikavalikko |Sovellusnäppäin |Avaa pikavalikon valitulle kirjalle.|

<!-- KC:endInclude -->

### Windows-konsoli {#WinConsole}

NVDA tarjoaa tuen Windowsin komentokonsolille, jota komentokehote, PowerShell ja Windows-alijärjestelmä Linuxille käyttävät.
Konsoli-ikkunan koko on kiinteä, tyypillisesti paljon pienempi kuin puskuri, joka sisältää komentojen palauttaman tulosteen.
Kun uutta tekstiä tulostuu näytölle, sisältöä vieritetään ylöspäin, eikä aiempi teksti ole enää näkyvissä.
Tekstiä, jota ei näy ikkunassa, ei voi tarkastella NVDA:n tekstintarkastelukomennoilla Windows 11 22H2:ta vanhemmissa käyttöjärjestelmissä.
Konsoli-ikkunan vierittäminen on siksi tarpeen, jotta aiempaa tekstiä voidaan lukea.
Uudemmissa konsolin versioissa ja Windows-päätteessä on mahdollista tarkastella koko tekstipuskuria vapaasti ilman ikkunan vierittämistä.
<!-- KC:beginInclude -->
Seuraavat sisäänrakennetut Windows-konsolin pikanäppäimet voivat olla hyödyllisiä [tarkasteltaessa tekstiä](#ReviewingText) NVDA:lla vanhemmissa Windows-konsolin versioissa:

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vieritä ylös |Ctrl+Nuoli ylös |Vierittää konsoli-ikkunaa ylöspäin, jotta aiempaa tekstiä voidaan lukea.|
|Vieritä alas |Ctrl+Nuoli alas |Vierittää konsoli-ikkunaa alaspäin, jotta uudempaa tekstiä voidaan lukea.|
|Vieritä alkuun |Ctrl+Home |Vierittää konsoli-ikkunan puskurin alkuun.|
|Vieritä loppuun |Ctrl+End |Vierittää konsoli-ikkunan puskurin loppuun.|

<!-- KC:endInclude -->

## Asetusten määrittäminen {#ConfiguringNVDA}

Useimpia asetuksia voidaan muuttaa valintaikkunoista, joihin pääsee NVDA-valikon Asetukset-alivalikosta.
Monet näistä asetuksista löytyvät usean kategorian [Asetukset-valintaikkunasta](#NVDASettings).
Hyväksy valintaikkunoissa tekemäsi muutokset painamalla OK-painiketta.
Peruuta muutokset painamalla Peruuta-painiketta tai Esc-näppäintä.
Tietyissä valintaikkunoissa voit ottaa asetukset heti käyttöön painamalla Käytä-painiketta sulkematta valintaikkunaa.
Useimmissa NVDA:n valintaikkunoissa on käytettävissä tilannekohtainen ohje.
<!-- KC:beginInclude -->
Kun valintaikkunassa painetaan `F1`, käyttöopas avataan kohdasta, joka liittyy kyseiseen asetukseen tai senhetkiseen valintaikkunaan.
<!-- KC:endInclude -->
Joitakin asetuksia on mahdollista muuttaa myös pikanäppäimillä, jotka on lueteltu alla olevissa kappaleissa.

### Asetukset {#NVDASettings}

<!-- KC:settingsSection: || Nimi | Näppäinkomento pöytäkoneissa | Näppäinkomento kannettavissa | Kuvaus | -->
NVDA sisältää useita asetuksia, joita voidaan muuttaa asetusvalintaikkunan avulla.
Valintaikkunassa on luettelo valittavissa olevista asetuskategorioista, jotta muutettavien asetusten löytäminen olisi helpompaa.
Kun valitset kategorian, kaikki siihen liittyvät asetukset näytetään.
Liiku kategorioiden välillä siirtymällä `Sarkain`- tai `Vaihto+Sarkain`-näppäimillä kategorialuetteloon ja käytä sitten ylä- ja alanuolinäppäimiä siinä liikkumiseen.
Lisäksi voit siirtyä missä tahansa valintaikkunan kohdassa yhden kategorian eteenpäin painamalla `Ctrl+Sarkain` tai taaksepäin painamalla `Vaihto+Ctrl+Sarkain`.

Kun olet muuttanut yhtä tai useampaa asetusta, muutokset voidaan ottaa käyttöön painamalla Käytä-painiketta, jolloin valintaikkuna pysyy avoimena, mikä mahdollistaa muiden asetusten muuttamisen tai toisen kategorian valitsemisen.
Paina OK-painiketta, jos haluat tallentaa asetukset ja sulkea valintaikkunan.

Joillakin asetuskategorioilla on oma pikanäppäin.
Kun sitä painetaan, Asetukset-valintaikkuna avataan kyseisen kategorian kohdalta.
Kaikkiin kategorioihin ei oletusarvoisesti pääse näppäinkomennoilla.
Jos käytät usein kategorioita, joilla ei ole omia pikanäppäimiä, voit halutessasi lisätä niille näppäinkomennon tai kosketuseleen [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

Valintaikkunan asetuskategoriat on kuvailtu alla.

#### Yleiset {#GeneralSettings}

<!-- KC:setting -->

##### Avaa yleiset asetukset {#toc110}

Pikanäppäin: `NVDA+Ctrl+G`

Yleiset-kategoriassa määritetään NVDA:n yleinen toiminta, kuten käyttöliittymän kieli ja automaattinen päivitysten tarkistus.
Se sisältää seuraavat asetukset:

##### Kieli {#GeneralSettingsLanguage}

Tämä on yhdistelmäruutu, josta voidaan valita kieli, jolla NVDA:n käyttöliittymä ja ilmoitukset näytetään.
Kieliä on useita.
Oletusarvoisesti on valittuna vaihtoehto "Windows", mikä tarkoittaa, että NVDA käyttää Windowsin maakohtaisissa asetuksissa määritettyä kieltä.

Huom: NVDA on käynnistettävä uudelleen kieltä vaihdettaessa.
Kun vahvistusvalintaikkuna tulee näkyviin, valitse "Käynnistä uudelleen nyt", jos haluat käyttää uutta kieltä heti, tai "Käynnistä uudelleen myöhemmin", jos otat sen käyttöön myöhemmin. Jos valitset "Käynnistä uudelleen myöhemmin", asetukset on tallennettava (joko manuaalisesti tai Tallenna asetukset suljettaessa -toiminnallisuutta käyttäen).

##### Tallenna asetukset suljettaessa {#GeneralSettingsSaveConfig}

Jos tämä valintaruutu on valittuna, nykyiset asetukset tallennetaan, kun NVDA suljetaan.

##### Näytä sulkemisvaihtoehdot {#GeneralSettingsShowExitOptions}

Tällä valintaruudulla voidaan määrittää, tuleeko NVDA:ta suljettaessa näkyviin valintaikkuna, jossa kysytään suoritettavaa toimintoa.
Kun tämä asetus on käytössä, NVDA:ta suljettaessa tulee näkyviin valintaikkuna, jossa kysytään, haluatko sulkea, käynnistää uudelleen, käynnistää uudelleen poistaen lisäosat käytöstä vai asentaa odottavat päivitykset (mikäli sellaisia on).
Kun asetus ei ole käytössä, NVDA sulkeutuu heti.

##### Toista ääni käynnistettäessä ja suljettaessa {#GeneralSettingsPlaySounds}

Kun tämä valintaruutu on valittuna, NVDA toistaa äänen käynnistyessään ja sulkeutuessaan.

##### Lokitaso {#GeneralSettingsLogLevel}

Tästä yhdistelmäruudusta voidaan valita, paljonko NVDA tallentaa tietoja lokiin käynnissä ollessaan.
Tätä ei yleensä tarvitse muuttaa.
Asetuksesta voi kuitenkin olla hyötyä, jos tarvitaan tietoja esimerkiksi vikaraporttia varten tai halutaan poistaa loki kokonaan käytöstä.

Käytettävissä ovat seuraavat lokitasot:

* Ei käytössä: NVDA ei tallenna lokiin mitään käynnissä ollessaan lyhyttä käynnistysilmoitusta lukuun ottamatta.
* Tiedot: NVDA tallentaa lokiin perustietoja, kuten käynnistysilmoituksia ja kehittäjille hyödyllistä tietoa.
* Virheenkorjausvaroitus: Lokiin tallennetaan varoituksia, jotka eivät ole vakavien virheiden aiheuttamia.
* Syöttö/tulostus: Lokiin tallennetaan näppäimistön ja pistenäyttöjen syöte sekä puhe- ja pistekirjoitustuloste.
Jos olet huolissasi yksityisyydestäsi, älä määritä lokitasoksi tätä vaihtoehtoa.
* Virheenkorjaus: Lokiin tallennetaan tiedot-, varoitukset- ja syöttö/tulostus-ilmoitusten lisäksi virheenkorjauksen lisäilmoituksia.
Kuten syöttö/tulostus-tasolla, älä määritä lokitasoksi tätä vaihtoehtoa, mikäli olet huolissasi yksityisyydestäsi.

##### Käynnistä automaattisesti sisäänkirjautumisen jälkeen {#GeneralSettingsStartAfterLogOn}

Jos tämä asetus on käytössä, NVDA käynnistyy automaattisesti heti kirjautuessasi sisään Windowsiin.
Asetus on käytettävissä vain NVDA:n asennetuissa versioissa.

##### Käytä sisäänkirjautumisen aikana (edellyttää järjestelmänvalvojan oikeuksia) {#GeneralSettingsStartOnLogOnScreen}

Jos kirjaudut Windowsiin käyttäjänimellä ja salasanalla, tämä asetus saa NVDA:n käynnistymään automaattisesti kirjautumisikkunassa aina käyttöjärjestelmän käynnistyessä.
Asetus on käytettävissä vain NVDA:n asennetuissa versioissa.

##### Käytä tallennettuja asetuksia sisäänkirjautumisen aikana ja suojatuissa ruuduissa (edellyttää järjestelmänvalvojan oikeuksia) {#GeneralSettingsCopySettings}

Tämän painikkeen painaminen kopioi nykyiset tallennetut asetukset NVDA:n järjestelmäasetusten hakemistoon, jotta niitä käytetään sisäänkirjautumisen aikana ja käyttäjätilien valvonnassa sekä muissa [suojatuissa ruuduissa](#SecureScreens).
Voit varmistaa asetusten siirtämisen tallentamalla ne ensin painamalla Ctrl+NVDA+C tai valitsemalla NVDA-valikosta Tallenna asetukset.
Tämä painike on käytettävissä vain NVDA:n asennetuissa versioissa.

##### Tarkista päivitykset automaattisesti {#GeneralSettingsCheckForUpdates}

Jos tämä asetus on käytössä, NVDA etsii automaattisesti uusia versioita ja ilmoittaa, kun päivitys on saatavilla.
Päivitysten manuaalinen tarkistaminen on myös mahdollista valitsemalla Tarkista päivitykset -vaihtoehto NVDA-valikosta Ohje-valikon alta.
Kun päivitykset tarkistetaan manuaalisesti tai automaattisesti, NVDA:n on lähetettävä joitakin tietoja päivityspalvelimelle asianmukaisen version vastaanottamiseksi.
Seuraavat tiedot lähetetään aina:

* Nykyinen NVDA:n versio
* Käyttöjärjestelmän versio
* Onko käyttöjärjestelmä 64- vai 32-bittinen

##### Salli NV Accessin kerätä NVDA:n käyttötilastoja {#GeneralSettingsGatherUsageStats}

Jos tämä on käytössä, NV Access käyttää päivitystarkistusten tietoja NVDA-käyttäjien määrän seuraamiseen, mukaan lukien tietyt väestötilastolliset tiedot kuten käyttöjärjestelmä sekä alkuperämaa.
Huom: IP-osoitetta ei säilytetä, vaikka sitä käytetäänkin päivitystarkistuksen aikana käyttäjän maan selvittämiseen.
Päivitysten tarkistamiseen tarvittavien pakollisten tietojen lisäksi lähetetään tällä hetkellä myös seuraavat lisätiedot:

* NVDA:n käyttöliittymän kieli
* Käytetäänkö NVDA:n asennettua vai massamuistiversiota
* Käytössä olevan puhesyntetisaattorin nimi (mukaan lukien lisäosan nimi, johon ajuri kuuluu)
* Käytössä olevan pistenäytön nimi (mukaan lukien lisäosan nimi, johon ajuri kuuluu)
* Nykyinen pistekirjoituksen tulostustaulukko (jos pistenäyttö on käytössä)

Nämä tiedot auttavat huomattavasti NV Accessia priorisoimaan NVDA:n tulevaa kehitystä.

##### Ilmoita käynnistettäessä odottavasta päivityksestä {#GeneralSettingsNotifyPendingUpdates}

Jos tämä on valittuna, NVDA ilmoittaa käynnistyessään odottavasta päivityksestä ja tarjoaa mahdollisuutta sen asentamiseen.
Päivitys voidaan asentaa myös manuaalisesti Sulje NVDA -valintaikkunasta (mikäli se on käytössä), NVDA-valikosta tai suoritettaessa päivitystarkistusta Ohje-valikosta.

#### Puhe {#SpeechSettings}

<!-- KC:setting -->

##### Avaa puheasetukset {#toc123}

Pikanäppäin: `NVDA+Ctrl+V`

Puhe-kategoria sisältää asetuksia, joilla muutetaan sekä käytettävää puhesyntetisaattoria että sen puheäänen ominaisuuksia.
Tietoja nopeammasta vaihtoehtoisesta tavasta puheparametrien säätämiseen mistä tahansa on [Syntetisaattorin asetusrengas](#SynthSettingsRing) -osiossa.

Tämä kategoria sisältää seuraavat asetukset:

##### Muuta syntetisaattoria {#SpeechSettingsChange}

Puhe-asetuskategorian ensimmäinen vaihtoehto on Muuta...-painike. Tämä painike avaa [Valitse syntetisaattori](#SelectSynthesizer) -valintaikkunan, josta valitaan käytettävä puhesyntetisaattori ja äänilaite.
Valintaikkuna avautuu Asetukset-valintaikkunan päälle.
Valitse syntetisaattori -valintaikkunassa muutettujen asetusten tallentaminen tai hylkääminen palauttaa takaisin Asetukset-valintaikkunaan.

##### Puheääni {#SpeechSettingsVoice}

Puheääni-vaihtoehto on yhdistelmäruutu, jossa on luettelo kaikista käytössä olevan syntetisaattorin puheäänistä.
Vaihtoehtoja voi selata nuolinäppäimillä.
Nuoli vasemmalle ja Nuoli ylös siirtävät ylöspäin luettelossa, kun taas Nuoli oikealle ja Nuoli alas siirtävät alas.

##### Muunnelma {#SpeechSettingsVariant}

Jos käytetään NVDA:n mukana tulevaa eSpeak NG -puhesyntetisaattoria, tästä yhdistelmäruudusta voidaan valita käytettävä muunnelma.
Muunnelmat ovat ikään kuin puheääniä, koska jokainen antaa äänille hieman eri määreitä.
Jotkin muunnelmat kuulostavat mieheltä, jotkin naiselta, ja jotkin jopa kuin sammakolta.
Mikäli käytät kolmannen osapuolen syntetisaattoria, saatat myös pystyä ehkä muuttamaan tätä arvoa, jos valitsemasi ääni tukee sitä.

##### Nopeus {#SpeechSettingsRate}

Tällä liukusäätimellä voit muuttaa puheen nopeutta.
Arvot 0 - 100 ovat mahdollisia (0=hitain ja 100=nopein).

##### Nopeuden lisäys {#SpeechSettingsRateBoost}

Tämän asetuksen käyttöön ottaminen lisää huomattavasti puhenopeutta, jos nykyinen syntetisaattori tukee sitä.

##### Korkeus {#SpeechSettingsPitch}

Tällä liukusäätimellä muutetaan puheen korkeutta.
Arvot 0 - 100 ovat mahdollisia (0=matalin ja 100=korkein).

##### Voimakkuus {#SpeechSettingsVolume}

Tällä liukusäätimellä muutetaan puheen voimakkuutta – arvot 0 - 100 ovat mahdollisia (0=hiljaisin ja 100=voimakkain).

##### Sävy {#SpeechSettingsInflection}

Tällä liukusäätimellä muutetaan äänensävyä (korkeuden nousuja ja laskuja), jolla puhesyntetisaattori puhuu.

##### Vaihda kieltä automaattisesti {#VoiceSettingsLanguageSwitching}

Tällä valintaruudulla voidaan vaikuttaa siihen, vaihtaako NVDA puhesyntetisaattorin kieltä automaattisesti, jos luettavan tekstin kieli on määritetty asianmukaisesti.
Asetus on oletusarvoisesti käytössä.

##### Vaihda murretta automaattisesti {#SpeechSettingsDialectSwitching}

Tällä valintaruudulla määritetään, vaihdetaanko pelkän kielen lisäksi myös murretta.
Jos esim. amerikanenglantia puhuvalla äänellä luetaan asiakirjaa, jonka kielimäärityksen mukaan osa tekstistä on englanninenglantia, silloin tämän asetuksen ollessa käytössä syntetisaattori vaihtaa aksenttiaan.
Asetus ei ole oletusarvoisesti käytössä.

<!-- KC:setting -->

##### Välimerkki- ja symbolitaso {#SpeechSettingsSymbolLevel}

Pikanäppäin: `NVDA+P`

Tästä valitaan sanoina luettavien välimerkkien ja muiden symbolien määrä.
Esim. kun tasoksi on valittu kaikki, kaikki merkit luetaan sanoina.
Tämä asetus vaikuttaa kaikkiin syntetisaattoreihin.

##### Käytä puheäänen kieltä merkkejä ja symboleita käsiteltäessä {#SpeechSettingsTrust}

Tämä asetus, joka on oletusarvoisesti käytössä, määrittää, että NVDA käyttää puheäänen kieltä merkkien ja symbolien puhumiseen.
Mikäli välimerkit luetaan väärällä kielellä tiettyä syntetisaattoria tai puheääntä käytettäessä, tämän asetuksen käytöstä poistaminen pakottaa NVDA:n käyttämään yleistä kieliasetusta.

##### Käytä Unicode-konsortion dataa (emojit mukaan lukien) merkkejä ja symboleita käsiteltäessä {#SpeechSettingsCLDR}

Kun tämä valintaruutu on valittuna, NVDA käyttää symbolien lisäsanastoja merkkejä ja symboleita puhuttaessa.
Nämä sanastot sisältävät merkkien kuvauksia (erityisesti emojeille), jotka tarjoaa [Unicode-konsortio](https://www.unicode.org/consortium/) osana [Common Locale Data -tietokantaa](http://cldr.unicode.org/).
Mikäli NVDA:n halutaan puhuvan emoji-merkkien kuvaukset tähän dataan perustuen, tämän valintaruudun tulee olla valittuna.
Jos kuitenkin käytössä on puhesyntetisaattori, joka jo valmiiksi tukee emojien puhumista, tämä asetus kannattaa ehkä poistaa käytöstä.

Huom: Manuaalisesti lisätyt tai muokatut merkkikuvaukset tallennetaan osana käyttäjän asetuksia.
Mikäli siis jonkin emojin kuvausta muutetaan, kyseiselle emojille käytetään muokattua kuvausta riippumatta siitä, onko tämä asetus käytössä vai ei.
Symbolien kuvauksia on mahdollista lisätä, muokata ja poistaa NVDA:n [Välimerkkien ja symbolien puhuminen -valintaikkunassa.](#SymbolPronunciation)

Unicode-konsortion datan sisällyttämistä voi vaihtaa mistä tahansa lisäämällä mukautettu näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Äänenkorkeuden muutos prosentteina isoille kirjaimille {#SpeechSettingsCapPitchChange}

Tähän muokkauskenttään syötetään prosenttiluku, jonka verran puheäänen korkeus muuttuu isoja kirjaimia luettaessa.
Negatiivinen arvo laskee ja positiivinen nostaa äänenkorkeutta.
Mikäli äänenkorkeuden ei haluta muuttuvan, tulee arvoksi antaa 0.
Tavallisesti NVDA nostaa hieman äänenkorkeutta jokaisen ison kirjaimen kohdalla, mutta jotkin puhesyntetisaattorit eivät ehkä tue sitä kunnolla.
Jos isojen kirjainten äänenkorkeuden muuttamista ei tueta, harkitse sen sijaan asetusten [Ilmaise isot kirjaimet sanomalla "iso"](#SpeechSettingsSayCapBefore) ja/tai [Ilmaise isot kirjaimet äänimerkillä](#SpeechSettingsBeepForCaps) käyttämistä.

##### Ilmaise isot kirjaimet sanomalla "iso" {#SpeechSettingsSayCapBefore}

Kun tämä asetus on käytössä, NVDA sanoo "iso" ennen jokaista yksittäisenä merkkinä puhuttua isoa kirjainta (kuten esim. tavattaessa).

##### Ilmaise isot kirjaimet äänimerkillä {#SpeechSettingsBeepForCaps}

Jos tämä valintaruutu on valittuna, NVDA antaa pienen äänimerkin aina isoa kirjainta luettaessa.

##### Käytä tavaustoimintoa (jos mahdollista) {#SpeechSettingsUseSpelling}

Jotkin sanat koostuvat vain yhdestä kirjaimesta, mutta se lausutaan eri tavalla riippuen siitä, puhutaanko se yksittäisenä merkkinä (kuten tavattaessa) vai sanana.
Esim. englanninkielessä "a" on sekä kirjain että sana, mutta se lausutaan kussakin tilanteessa eri tavalla.
Tämän asetuksen avulla syntetisaattori pystyy erottamaan nämä tilanteet toisistaan, mikäli se vain tukee toimintoa.
Useimmat syntetisaattorit tukevat asetusta.

Tämä asetus tulisi tavallisesti ottaa käyttöön.
Jotkin SAPI-syntetisaattorit toimivat kuitenkin kummallisesti tämän ollessa käytössä, koska ominaisuutta ei ole toteutettu niissä kunnolla.
Asetus kannattaa poistaa käytöstä, jos yksittäisten kirjainten lausumisessa on ongelmia.

##### Viivästetyt merkkien kuvaukset kohdistinta siirrettäessä {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Käytössä, Ei käytössä|
|Oletus |Ei käytössä|

Kun tämä asetus on käytössä, NVDA sanoo merkin kuvauksen liikkuessasi tekstissä merkki kerrallaan.

Esimerkiksi kun kirjain "b" luetaan tarkasteltaessa riviä merkeittäin, NVDA sanoo "Bertta" yhden sekunnin viipeen jälkeen.
Tästä voi olla hyötyä, mikäli symbolien ääntämistä on vaikea erottaa toisistaan, tai kuulovammaisille käyttäjille.

Viivästetty merkin kuvaus peruuntuu, jos tuona aikana puhutaan muuta tekstiä tai jos painat `Ctrl`-näppäintä.

##### Puhetilakomennon valinnat {#SpeechModesDisabling}

Tästä valintaluettelosta on mahdollista valita, mitkä [puhetilat](#SpeechModes) ovat käytettävissä vaihdettaessa niiden välillä `NVDA+S`-näppäinkomennolla.
Valitsemattomat tilat jätetään pois komennosta.
Oletusarvoisesti kaikki tilat ovat käytettävissä.

Esimerkiksi jos et tarvitse "äänimerkit"- ja "ei puhetta" -tiloja, sinun tulisi poistaa niiden valinta ja pitää sekä "puhe käytössä" että "pyydettäessä" valittuina.
Huom: Vähintään kaksi tilaa on oltava valittuna.

#### Valitse syntetisaattori {#SelectSynthesizer}

<!-- KC:setting -->

##### Avaa Valitse syntetisaattori -valintaikkuna {#toc144}

Pikanäppäin: `NVDA+Ctrl+S`

Valitse 	syntetisaattori -valintaikkunassa, joka voidaan avata painamalla "Muuta..."-painiketta Asetukset-valintaikkunan Puhe-kategoriassa, valitaan, mitä syntetisaattoria NVDA käyttää.
Kun haluttu syntetisaattori on valittu, NVDA ottaa sen käyttöön OK-painikkeen painamisen jälkeen.
Jos syntetisaattorin lataamisessa ilmenee virhe, siitä ilmoittava viesti näytetään, eikä käytettävää syntetisaattoria vaihdeta.

##### Syntetisaattori {#SelectSynthesizerSynthesizer}

Tästä yhdistelmäruudusta valitaan, mitä puhesyntetisaattoria NVDA käyttää puheen tuottamiseen.

Luettelo NVDA:n tukemista syntetisaattoreista on [Tuetut puhesyntetisaattorit](#SupportedSpeechSynths) -osiossa.

Eräs tässä luettelossa aina näkyvä vaihtoehto on "Ei puhetta", joka mahdollistaa NVDA:n käytön täysin ilman puhetta.
Tästä voi olla hyötyä NVDA:ta pelkän pistenäytön varassa käyttävälle tai näkeville kehittäjille, jotka käyttävät pelkkää puheen tarkastelu -toimintoa.

#### Syntetisaattorin asetusrengas {#SynthSettingsRing}

NVDA:ssa on joitakin näppäinkomentoja, joiden avulla voidaan siirtyä missä tahansa yleisimpien puheasetusten välillä, mikäli niitä halutaan muuttaa nopeasti menemättä Asetukset-valintaikkunan Puhe-kategoriaan:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Siirrä seuraavaan syntetisaattorin asetukseen |NVDA+Ctrl+Nuoli oikealle |NVDA+Vaihto+Ctrl+Nuoli oikealle |Siirtää nykyisen puheasetuksen jälkeen seuraavana käytettävissä olevaan asetukseen, siirtyen viimeisen jälkeen takaisin ensimmäiseen.|
|Siirrä edelliseen syntetisaattorin asetukseen |NVDA+Ctrl+Nuoli vasemmalle |NVDA+Vaihto+Ctrl+Nuoli vasemmalle |Siirtää nykyistä puheasetusta edeltävään käytettävissä olevaan asetukseen, siirtyen ensimmäisen jälkeen takaisin viimeiseen.|
|Suurenna nykyistä syntetisaattorin asetusta |NVDA+Ctrl+Nuoli ylös |NVDA+Vaihto+Ctrl+Nuoli ylös |Suurentaa valittua puheasetusta, esim. lisää nopeutta, valitsee seuraavan puheäänen tai lisää äänenvoimakkuutta.|
|Suurenna aktiivista syntetisaattorin asetusta enemmän |`NVDA+Ctrl+Page up` |`NVDA+Vaihto+Ctrl+Page up` |Suurentaa nykyisen puheasetuksen arvoa enemmän kerrallaan. Kun esim. puheääniasetus on valittuna, tämä komento siirtää kerralla eteenpäin 20 äänen yli. Liukusäädinasetusten kohdalla (nopeus, korkeus jne.) se suurentaa arvoa jopa 20 %.|
|Pienennä nykyistä syntetisaattorin asetusta |NVDA+Ctrl+Nuoli alas |NVDA+Vaihto+Ctrl+Nuoli alas |Pienentää valittua puheasetusta, esim. vähentää nopeutta, valitsee edellisen puheäänen tai vähentää äänenvoimakkuutta.|
|Pienennä aktiivista syntetisaattorin asetusta enemmän |`NVDA+Ctrl+Page down` |`NVDA+Vaihto+Ctrl+Page down` |Pienentää aktiivisen puheasetuksen arvoa enemmän kerrallaan. Kun esim. puheääniasetus on valittuna, tämä komento siirtää kerralla taaksepäin 20 äänen yli. Liukusäädinasetusten kohdalla se pienentää arvoa jopa 20 %.|

<!-- KC:endInclude -->

#### Pistekirjoitus {#BrailleSettings}

Pistekirjoitus-kategoria sisältää vaihtoehtoja, joilla voidaan muuttaa useita pistekirjoituksen syöttö- ja tulostusasetuksia.
Seuraavat vaihtoehdot ovat käytettävissä:

##### Muuta pistenäyttöä {#BrailleSettingsChange}

Asetukset-valintaikkunan Pistekirjoitus-kategorian Muuta...-painike avaa [Valitse pistenäyttö](#SelectBrailleDisplay) -valintaikkunan, josta valitaan käytettävä pistenäyttö.
Tämä valintaikkuna avautuu Asetukset-valintaikkunan päälle.
Valitse pistenäyttö -valintaikkunassa muutettujen asetusten tallentaminen tai hylkääminen palauttaa takaisin Asetukset-valintaikkunaan.

##### Tulostustaulukko {#BrailleSettingsOutputTable}

Tämän kategorian seuraava vaihtoehto on "Tulostustaulukko"-yhdistelmäruutu.
Se sisältää pistetaulukoita eri kielille ja pistekirjoitusstandardeille sekä -tasoille.
Valittua taulukkoa käytetään tekstin kääntämiseen pistenäytöllä näytettäväksi pistekirjoitukseksi.
Vaihtoehtojen välillä liikutaan nuolinäppäimillä.

##### Syöttötaulukko {#BrailleSettingsInputTable}

Edellistä vaihtoehtoa täydentää Syöttötaulukko-yhdistelmäruutu.
Valittua taulukkoa käytetään pistenäytön Perkins-tyylisellä pistenäppäimistöllä syötetyn pistekirjoituksen kääntämiseen tekstiksi.
Vaihtoehtojen välillä liikutaan nuolinäppäimillä.

Huom: Tästä vaihtoehdosta on hyötyä vain, jos pistenäytössä on Perkins-tyylinen -näppäimistö ja mikäli näytön ajuri tukee tätä ominaisuutta.
Jos pistenäppäimistön sisältävä pistenäyttö ei tue syöttöä, siitä huomautetaan [Tuetut pistenäytöt](#SupportedBrailleDisplays) -osiossa.

<!-- KC:setting -->

##### Pistekirjoitustila {#BrailleMode}

Pikanäppäin: `NVDA+Alt+T`

Tällä asetuksella voit valita käytettävän pistekirjoitustilan.

Tuetut pistekirjoitustilat ovat tällä hetkellä "seuraa kohdistimia" ja "näytä puhetuloste".

Kun valittuna on "seuraa kohdistimia", pistenäyttö seuraa joko järjestelmän kohdistusta/kohdistinta tai navigointiobjektia/tarkastelukohdistinta riippuen siitä, mitä pistenäyttö on määritetty seuraamaan.

Kun valittuna on "näytä puhetuloste", pistenäytöllä näytetään, mitä NVDA puhuu tai olisi puhunut, jos puhetilana olisi ollut "puhe käytössä".

##### Laajenna kohdistimen kohdalla oleva sana {#BrailleSettingsExpandToComputerBraille}

Kun tämä asetus on käytössä, kohdistimen alla oleva sana näytetääntavallisella tietokonemerkistöllä.

##### Näytä kohdistin {#BrailleSettingsShowCursor}

Tällä asetuksella voidaan ottaa pistekohdistin käyttöön tai poistaa se käytöstä.
Asetus vaikuttaa järjestelmä- ja tarkastelukohdistimeen, mutta ei valinnanilmaisimeen.

##### Vilkkuva kohdistin {#BrailleSettingsBlinkCursor}

Tämä asetus saa pistekohdistimen vilkkumaan.
Mikäli vilkkuminen poistetaan käytöstä, kohdistin on aina ylhäällä.
Tämä asetus ei vaikuta valinnanilmaisimeen, sillä se koostuu pisteistä 7 ja 8, ja on vilkkumaton.

##### Kohdistimen vilkkumisnopeus (ms) {#BrailleSettingsBlinkRate}

Tällä asetuksella muutetaan kohdistimen vilkkumisnopeutta millisekunteina.

##### Kohdistimen muoto kohdistukselle {#BrailleSettingsCursorShapeForFocus}

Tällä asetuksella voit valita pistekohdistimen muodon (käytettävät pisteet), kun pistenäyttö on määritetty seuraamaan kohdistusta.
Asetus ei vaikuta valinnanilmaisimeen, sillä se koostuu aina pisteistä 7 ja 8, ja on vilkkumaton.

##### Kohdistimen muoto tarkastelukohdistimelle {#BrailleSettingsCursorShapeForReview}

Tällä asetuksella voit valita pistekohdistimen muodon (käytettävät pisteet), kun pistenäyttö on määritetty seuraamaan tarkastelukohdistinta.
Asetus ei vaikuta valinnanilmaisimeen, sillä se koostuu aina pisteistä 7 ja 8, ja on vilkkumaton.

##### Näytä ilmoitukset {#BrailleSettingsShowMessages}

Tästä yhdistelmäruudusta voit valita, näyttääkö NVDA ilmoitukset pistenäytöllä ja milloin ne katoavat automaattisesti näkyvistä.

Voit ottaa ilmoitusten näyttämisen käyttöön tai poistaa sen käytöstä mistä tahansa määrittämällä sille pikanäppäimen [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Ilmoitusten aikakatkaisu (sek) {#BrailleSettingsMessageTimeout}

Tämä asetus määrittää, kuinka kauan NVDA:n ilmoitukset näkyvät pistenäytöllä.
Ilmoitus hylätään heti painettaessa pistenäytön kosketuskohdistinnäppäintä, mutta tulee uudestaan näkyviin painettaessa sellaista näppäintä, joka aiheuttaa ilmoituksen näyttämisen.
Tämä asetus näytetään vain, jos "Näytä ilmoitukset" -asetukseksi on määritetty "Käytä aikakatkaisua".

<!-- KC:setting -->

##### Pistenäyttö seuraa {#BrailleTether}

Pikanäppäin: `NVDA+Ctrl+T`

Tällä asetuksella voit valita, seuraako pistenäyttö järjestelmän kohdistusta/kohdistinta, navigointiobjektia/tarkastelukohdistinta vai molempia.
NVDA seuraa oletusarvoisesti kohdistusta ja kohdistinta, kun "automaattisesti"-vaihtoehto on valittuna.
Kun navigointiobjektin tai tarkastelukohdistimen sijainti muuttuu käyttäjän toimesta, NVDA seuraa tällöin tilapäisesti tarkastelukohdistinta, kunnes kohdistuksen tai kohdistimen sijainti muuttuu.
Jos haluat sen seuraavan vain kohdistusta ja kohdistinta, pistenäyttö on [määritettävä seuraamaan](#BrailleTether) kohdistusta.
Tällöin näyttö ei seuraa navigointiobjektia objektinavigointia käytettäessä tai tarkastelukohdistinta tekstiä tarkasteltaessa.
Jos sen sijaan haluat pistenäytön seuraavan objektinavigointia ja tarkastelukohdistinta, näyttö on määritettävä seuraamaan tarkastelukohdistinta.
Tällöin pistenäyttö ei seuraa järjestelmän kohdistusta eikä kohdistinta.

##### Siirrä järjestelmäkohdistin tarkastelukohdistimen kohdalle {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Ei koskaan), Ei koskaan, Vain kun pistenäyttö seuraa automaattisesti, Aina|
|Oletus |Ei koskaan|

Tämä asetus määrittää, siirretäänkö järjestelmäkohdistinta kosketuskohdistinnäppäimen painalluksella.
Asetuksen oletusarvo on Ei koskaan, mikä tarkoittaa, että kosketuskohdistinnäppäimen painaminen ei siirrä järjestelmäkohdistinta tarkastelukohdistimen kohdalle.

Kun asetukseksi on määritetty "Aina" ja [pistenäyttö seuraa](#BrailleTether) "automaattisesti" tai "tarkastelukohdistinta", kosketuskohdistinnäppäimen painaminen siirtää myös järjestelmäkohdistinta tai kohdistusta, mikäli se on mahdollista.
Fyysistä kohdistinta ei ole, kun nykyisenä tarkastelutilana on [ruudun tarkastelu](#ScreenReview).
Tällaisissa tilanteissa NVDA yrittää siirtää kohdistuksen objektiin, joka on sen tekstin alla, johon olet siirtymässä.
Sama pätee myös [objektin tarkasteluun](#ObjectReview).

Voit myös määrittää tämän asetuksen siirtämään järjestelmäkohdistinta vain, kun Pistenäyttö seuraa -asetuksena on "automaattisesti".
Tällöin kosketuskohdistinnäppäimen painallus siirtää järjestelmäkohdistinta tai kohdistusta vain, kun NVDA seuraa tarkastelukohdistinta automaattisesti, kun taas manuaalisesti tarkastelukohdistinta seurattaessa siirtämistä ei tapahdu.

Tämä asetus näytetään vain, jos [pistenäyttö seuraa](#BrailleTether) -asetukseksi on määritetty "automaattisesti" tai "tarkastelukohdistinta".

Muuta "Siirrä järjestelmäkohdistin tarkastelukohdistimen kohdalle" -asetusta mistä tahansa määrittämällä sille oma näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Lue kappaleittain {#BrailleSettingsReadByParagraph}

Jos tämä asetus on käytössä, teksti näytetään pistenäytöllä kappaleittain.
Seuraavalle ja edelliselle riville siirtävät komennot siirtävät myös kappale kerrallaan.
Pistenäyttöä ei siis tarvitse vierittää jokaisen rivin lopussa, vaikka siihen mahtuisikin enemmän tekstiä.
Tämä mahdollistaa suurten tekstimäärien sujuvamman lukemisen.
Asetus ei ole oletusarvoisesti käytössä.

##### Vältä sanojen katkaisua {#BrailleSettingsWordWrap}

Jos tämä asetus on käytössä, sanaa, joka on liian pitkä mahtuakseen pistenäytölle, ei katkaista.
Pisterivin lopussa näytetään sen sijaan tyhjää.
Koko sana luetaan vierittämällä näyttöä.
Tätä kutsutaan joskus automaattiseksi rivitykseksi.
Huom: Mikäli yksittäinen sana on liian pitkä mahtuakseen näytölle, se on silti katkaistava.

Jos tämä asetus ei ole käytössä, sanasta näytetään niin paljon kuin mahdollista, mutta sen loppuosa katkaistaan.
Sanan loppuosa luetaan vierittämällä näyttöä.

Asetuksen käyttöön ottaminen saattaa mahdollistaa sujuvamman lukemisen, mutta vaatii yleensä enemmän näytön vierittämistä.

##### Kohdistuskontekstin näyttäminen {#BrailleSettingsFocusContextPresentation}

Tällä asetuksella voidaan valita, mitä kontekstitietoja NVDA näyttää pistenäytöllä kohdistuksen siirtyessä objektiin.
Kontekstitiedot tarkoittavat kohdistuksen sisältävän objektin hierarkiaa.
Kun esim. kohdistus siirretään luettelon kohteeseen, se on osa luetteloa.
Luettelo puolestaan saattaa olla osa valintaikkunaa jne.
Lisätietoja NVDA:n objektien hierarkiasta on [objektinavigointia](#ObjectNavigation) käsittelevässä kappaleessa.

Kun asetukseksi on määritetty "täytä näyttö kontekstin muuttuessa", NVDA yrittää näyttää pistenäytöllä mahdollisimman paljon kontekstitietoja, mutta vain kontekstin muuttuneesta osasta.
Edellä olevassa esimerkissä tämä tarkoittaa, että kun kohdistus siirtyy luetteloon, NVDA näyttää sen kohteen pistenäytöllä.
Lisäksi, jos pistenäytöllä on tarpeeksi tilaa jäljellä, NVDA yrittää näyttää, että kyseinen kohde on osa luetteloa.
Mikäli luettelossa aletaan liikkua nuolinäppäimillä, NVDA olettaa, että käyttäjä tietää olevansa edelleen luettelossa.
Joten kaikista jäljellä olevista luettelon kohteista, joihin siirrytään, NVDA näyttää pistenäytöllä vain aktiivisena olevan.
Konteksti voidaan lukea uudelleen (ts. että ollaan luettelossa ja että se on osa valintaikkunaa) vierittämällä näyttöä taaksepäin.

Kun asetukseksi on määritetty "täytä näyttö aina", NVDA yrittää näyttää pistenäytöllä mahdollisimman paljon kontekstitietoja riippumatta siitä, onko samat tiedot nähty aiemmin.
Tällä on se etu, että NVDA mahduttaa näytölle mahdollisimman paljon tietoa.
Haittapuolena on kuitenkin, että kohdistus alkaa pistenäytöllä aina eri kohdasta.
Tämä voi vaikeuttaa esim. pitkän luettelon kohteiden selaamista, sillä sormea on siirrettävä jatkuvasti kohteen alun löytämiseksi.
NVDA 2017.2 ja aiemmat toimivat oletuksena tällä tavoin.

Kun kohdistuskontekstin näyttäminen -asetus on määritetty näyttämään kontekstitiedot vain taaksepäin vieritettäessä, NVDA ei koskaan näytä oletusarvoisesti kontekstitietoja pistenäytöllä.
Joten NVDA näyttää edellä olevassa esimerkissä, että kohdistus on luettelon kohteessa.
Konteksti voidaan lukea (ts. että ollaan luettelossa ja että se on osa valintaikkunaa) vierittämällä pistenäyttöä taaksepäin.

Kohdistuskontekstin näyttäminen -asetusta voidaan vaihtaa mistä tahansa liittämällä siihen oma näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Keskeytä puhe vieritettäessä {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Käytössä), Käytössä, Ei käytössä|
|Oletus |Käytössä|

Tämä asetus määrittää, keskeytetäänkö puhe vieritettäessä pistenäyttöä eteen/taaksepäin.
Edelliselle/seuraavalle riville siirtävät komennot keskeyttävät puheen aina.

Jatkuva puhe saattaa häiritä pistekirjoitusta luettaessa.
Tästä syystä asetus on oletusarvoisesti käytössä, jolloin puhe keskeytetään pistenäyttöä vieritettäessä.

Tämän asetuksen poistaminen käytöstä sallii puheen kuulumisen samalla, kun pistekirjoitusta luetaan.

##### Näytä valinta {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Käytössä), Käytössä, Ei käytössä|
|Oletus |Käytössä|

Tämä asetus määrittää, näytetäänkö valinnan ilmaisin (pisteet 7 ja 8) pistenäytöllä.
Asetus on oletusarvoisesti käytössä, jolloin ilmaisin näytetään.
Valinnanilmaisin saattaa häiritä lukemista.
Tämän asetuksen käytöstä poistaminen saattaa parantaa luettavuutta.

Voit ottaa valinnan näyttämisen käyttöön tai poistaa sen käytöstä mistä tahansa määrittämällä sille pikanäppäimen [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

#### Valitse pistenäyttö {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Avaa Valitse pistenäyttö -valintaikkuna {#toc168}

Pikanäppäin: `NVDA+Ctrl+A`

Valitse pistenäyttö -valintaikkunasta, joka voidaan avata painamalla "Muuta..."-painiketta Asetukset-valintaikkunan Pistekirjoitus-kategoriassa, valitaan, mitä pistenäyttöä NVDA käyttää pistekirjoituksen tulostamiseen.
Kun haluttu pistenäyttö on valittu, NVDA ottaa sen käyttöön OK-painikkeen painamisen jälkeen.
Mikäli näytön ajurin lataamisessa ilmenee virheitä, NVDA ilmoittaa siitä, eikä mahdollisesti käytössä olevaa pistenäyttöä vaihdeta.

##### Pistenäyttö {#SelectBrailleDisplayDisplay}

Tämä yhdistelmäruutu sisältää useita vaihtoehtoja riippuen järjestelmään asennetuista pistenäyttöajureista.
Vaihtoehtojen välillä liikutaan nuolinäppäimillä.

Vaihtoehto "automaattinen" saa NVDA:n etsimään useita tuettuja pistenäyttöjä taustalla.
Kun tämä ominaisuus on käytössä ja tietokoneeseen liitetään tuettu pistenäyttö USB:tä tai Bluetoothia käyttäen, NVDA ottaa kyseisen näytön käyttöön.

"Ei pistenäyttöä" tarkoittaa, että pistenäyttöä ei käytetä.

Lisätietoja tuetuista pistenäytöistä sekä siitä, mitkä niistä tukevat automaattista tunnistusta, on [Tuetut pistenäytöt](#SupportedBrailleDisplays) -osiossa.

##### Automaattisesti tunnistettavat pistenäytöt {#SelectBrailleDisplayAutoDetect}

Kun pistenäytöksi on määritetty "Automaattinen", tämän luettelon valintaruuduilla voit ottaa käyttöön ja poistaa käytöstä pistenäyttöajurit, jotka ovat mukana automaattisessa tunnistuksessa.
Tämä mahdollistaa sellaisten pistenäyttöajureiden käytöstä poistamisen, joita et käytä säännöllisesti.
Mikäli sinulla on esimerkiksi vain pistenäyttö, joka vaatii toimiakseen Baum-ajurin, voit jättää sen käyttöön ja poistaa muut ajurit käytöstä.

Kaikki automaattista tunnistusta tukevat ajurit ovat oletusarvoisesti käytössä.
Mahdolliset NVDA:n tulevissa versioissa tai lisäosina lisätyt ajurit ovat myös oletusarvoisesti käytössä.

Voit tarkistaa pistenäyttösi ohjeesta [Tuetut pistenäytöt -osiosta](#SupportedBrailleDisplays), tukeeko kyseinen ajuri näytön automaattista tunnistusta.

##### Portti {#SelectBrailleDisplayPort}

Tällä asetuksella, mikäli se on käytettävissä, valitaan, mitä porttia tai yhteystyyppiä valitun pistenäytön kanssa käytetään.
Se on yhdistelmäruutu, joka sisältää käytettävissä olevat vaihtoehdot valitulle pistenäytölle.

NVDA käyttää oletusarvoisesti automaattista portintunnistusta, mikä tarkoittaa, että pistenäyttöön muodostetaan yhteys automaattisesti skannaamalla järjestelmän käytettävissä olevia USB- ja Bluetooth-laitteita.
Joillekin pistenäytöille voidaan kuitenkin itse valita käytettävä portti.
Vaihtoehtoina ovat "Automaattinen" (joka määrää NVDA:n käyttämään oletusarvoista automaattista portintunnistusta), "USB", "Bluetooth" sekä "sarjaportti", mikäli pistenäyttö tukee sarjaporttiliitäntää.

Tämä vaihtoehto ei ole käytettävissä, jos pistenäyttö tukee vain automaattista portintunnistusta.

Lisätietoja pistenäyttöjen tukemista kommunikointityypeistä ja käytettävissä olevista porteista on [Tuetut pistenäytöt](#SupportedBrailleDisplays) -osiossa.

Huom: Jos kytket koneeseesi samanaikaisesti useita samaa ajuria käyttäviä pistenäyttöjä (esim. kaksi Seikaa),
NVDA:ssa ei ole tällä hetkellä mahdollista määrittää, mitä näyttöä sen tulisi käyttää.
Siksi on suositeltavaa kytkeä koneeseen vain yksi tietyn tyyppinen/valmistajan pistenäyttö kerrallaan.

#### Ääni {#AudioSettings}

<!-- KC:setting -->

##### Avaa ääniasetukset {#toc173}

Pikanäppäin: `NVDA+Ctrl+U`

NVDA:n asetusvalintaikkunan Ääni-kategoriasta voidaan muuttaa useita äänen ulostuloon liittyviä asetuksia.

##### Äänen ulostulolaite {#SelectSynthesizerOutputDevice}

Tästä valitaan, mitä äänilaitetta NVDA:ssa valittuna oleva puhesyntetisaattori käyttää.

<!-- KC:setting -->

##### Äänenvaimennus {#SelectSynthesizerDuckingMode}

Näppäinkomento: `NVDA+Vaihto+D`

Tällä asetuksella voit valita, pienentääkö NVDA muiden sovellusten äänenvoimakkuutta puhuessaan vai koko ajan käynnissä ollessaan.

* Ei käytössä: NVDA ei koskaan pienennä muiden sovellusten äänenvoimakkuutta.
* Puhuttaessa ja ääntä toistettaessa: NVDA pienentää muiden sovellusten äänenvoimakkuutta vain puhuessaan tai ääniä toistaessaan. Tämä ei välttämättä toimi kaikilla puhesyntetisaattoreilla.
* Aina: NVDA pienentää muiden sovellusten äänenvoimakkuutta koko ajan käynnissä ollessaan.

Tämä asetus on käytettävissä vain NVDA:n asennetussa versiossa.
Massamuisti- ja tilapäisversiot eivät tue äänenvaimennusta.

##### NVDA-äänien voimakkuus mukautuu puheäänen voimakkuuteen {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Ei käytössä, Käytössä|
|Oletus |Ei käytössä|

Kun tämä asetus on käytössä, NVDA:n äänien ja piippausten voimakkuus mukautuu käytettävän puheäänen voimakkuusasetukseen.
Jos puheäänen voimakkuutta vähennetään, äänien voimakkuus vähenee.
Jos puheäänen voimakkuutta lisätään, äänien voimakkuus vastaavasti kasvaa.
Tämä asetus ei ole käytettävissä, jos [Käytä WASAPIa äänen toistamiseen](#WASAPI) on poistettu käytöstä lisäasetuksista.

##### NVDA-äänien voimakkuus {#SoundVolume}

Tällä liukusäätimellä voidaan määrittää NVDA:n äänien ja piippausten äänenvoimakkuus.
Tämä asetus on käytettävissä vain, kun "NVDA-äänien voimakkuus mukautuu puheäänen voimakkuuteen" ei ole käytössä.
Tämä asetus ei ole käytettävissä, jos [Käytä WASAPIa äänen toistamiseen](#WASAPI) on poistettu käytöstä lisäasetuksissa.

##### Äänilaitteen hereilläpitoaika puheen jälkeen {#AudioAwakeTime}

Tässä muokkausruudussa määritetään, kuinka kauan NVDA pitää äänilaitteen hereillä puheen loputtua.
Se mahdollistaa tiettyjen puheen häiriöiden, kuten puuttuvien sanojen osien, välttämisen.
Tämä voi johtua äänilaitteiden (erityisesti Bluetooth- ja muiden langattomien laitteiden) valmiustilaan siirtymisestä.
Tästä voi olla hyötyä myös muissa käyttötarkoituksissa, kuten käytettäessä NVDA:ta virtuaalikoneessa (esim. Citrix Virtual Desktopissa) tai tietyissä kannettavissa tietokoneissa.

Pienempien arvojen käyttö voi aiheuttaa useammin äänen katkeamista, koska laite saattaa siirtyä valmiustilaan liian aikaisin, mistä on seurauksena seuraavan puhuttavan asian alun katkeaminen.
Liian suuren arvon käyttö saattaa tyhjentää äänilaitteen akun nopeammin, koska laite pysyy aktiivisena pidempään, vaikka ääntä ei lähetetä.

Poista tämä toiminto käytöstä määrittämällä ajaksi 0.

##### Äänijako {#SelectSoundSplitMode}

Äänijako-toiminto mahdollistaa stereoäänilaitteiden, kuten kuulokkeiden ja kaiuttimien, hyödyntämisen.
Sen avulla on mahdollista saada NVDA:n puhe toiseen kanavaan (esim. vasempaan) ja muiden sovellusten äänet toiseen (esim. oikeaan).
Oletuksena äänijako ei ole käytössä, mikä tarkoittaa, että kaikki sovellukset NVDA mukaan lukien toistavat ääntä sekä vasemmassa että oikeassa kanavassa.
Näppäinkomento mahdollistaa vaihtamisen eri äänijakotilojen välillä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vaihda äänijakotilaa |`NVDA+Alt+S` |Vaihtaa äänijakotilojen välillä.|

<!-- KC:endInclude -->

Oletuksena tämä komento vaihtaa seuraavien tilojen välillä:

* Ei käytössä: NVDA ja muut sovellukset toistavat ääntä sekä vasemmassa että oikeassa kanavassa.
* NVDA vasemmalla ja sovellukset oikealla: NVDA puhuu vasemmassa kanavassa, kun taas muut sovellukset toistavat ääntä oikeassa.
* NVDA oikealla ja sovellukset vasemmalla: NVDA puhuu oikeassa kanavassa, kun taas muut sovellukset toistavat ääntä vasemmassa.

NVDA:n asetusyhdistelmäruudussa on käytettävissä myös edistyneempiä äänijakotiloja.
Jos haluat säätää muiden sovellusten paitsi NVDA:n äänenvoimakkuutta, harkitse [siihen tarkoitettujen komentojen](#OtherAppVolume) käyttöä.
Huom: Äänijako ei toimi mikserinä.
Jos esimerkiksi sovellus toistaa stereoääniraitaa, kun äänijaon tilaksi on määritetty "NVDA vasemmalla ja sovellukset oikealla", kuulet vain ääniraidan oikean kanavan, kun taas raidan vasen kanava mykistetään.

Tämä asetus ei ole käytettävissä, jos olet [poistanut WASAPIn käytöstä](#WASAPI) NVDA:n lisäasetuksissa.

Huom: Jos NVDA kaatuu, se ei pysty palauttamaan sovellusten äänenvoimakkuutta, jolloin ne saattavat edelleen toistaa ääntä vain yhdessä kanavassa.
Käynnistä NVDA uudelleen tämän vähentämiseksi.

##### Äänijakotilojen mukauttaminen {#CustomizeSoundSplitModes}

Tästä valintaruutuluettelosta voit valita äänijakotilat, jotka ovat käytettävissä vaihdettaessa eri tilojen välillä näppäinkomentoa `NVDA+Alt+S` käyttäen.
Valitsemattomat tilat eivät ole käytettävissä.
Oletuksena vain kolme tilaa on valittuna.

* Ei käytössä: NVDA ja muut sovellukset toistavat ääntä sekä vasemmassa että oikeasssa kanavassa.
* NVDA vasemmalla ja muut sovellukset oikealla.
* NVDA oikealla ja muut sovellukset vasemmalla.

Huom: Vähintään yksi tila on oltava valittuna.
Tämä asetus ei ole käytettävissä, jos olet [poistanut WASAPIn käytöstä](#WASAPI) NVDA:n lisäasetuksissa.

##### Muiden sovellusten äänenvoimakkuus {#OtherAppVolume}

Tämä liukusäädin mahdollistaa kaikkien tällä hetkellä käynnissä olevien sovellusten paitsi NVDA:n äänenvoimakkuuden säätämisen.
Asetus vaikuttaa kaikkien muiden sovellusten äänentoistoon, vaikka ne käynnistettäisiin tämän asetuksen muuttamisen jälkeen.
Tätä äänenvoimakkuutta voi lisäksi säätää mistä tahansa seuraavia näppäinkomentoja käyttäen:

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Lisää sovellusten äänenvoimakkuutta |`NVDA+Alt+Page up` |Lisää kaikkien sovellusten paitsi NVDA:n äänenvoimakkuutta.|
|Vähennä sovellusten äänenvoimakkuutta |`NVDA+Alt+Page down` |Vähentää kaikkien sovellusten paitsi NVDA:n äänenvoimakkuutta.|

<!-- KC:endInclude -->

Tämä asetus ei ole käytettävissä, jos olet [poistanut WASAPIn käytöstä](#WASAPI) NVDA:n lisäasetuksissa.

##### Mykistä muut sovellukset {#MuteApplications}

Tämä valintaruutu mahdollistaa kaikkien muiden sovellusten paitsi NVDA:n mykistämisen.
Asetus vaikuttaa kaikkien muiden sovellusten äänentoistoon, vaikka ne käynnistettäisiin tämän asetuksen muuttamisen jälkeen.
Lisäksi seuraavaa näppäinkomentoa voidaan käyttää mistä tahansa:

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Vaihda muiden sovellusten mykistyksen tilaa |`NVDA+Alt+Delete` |Mykistää tai poistaa mykistyksen kaikista muista sovelluksista paitsi NVDA:sta.|

<!-- KC:endInclude -->

Tämä asetus ei ole käytettävissä, jos olet [poistanut WASAPIn käytöstä](#WASAPI) NVDA:n lisäasetuksissa.

#### Näkö {#VisionSettings}

NVDA:n asetusvalintaikkunan Näkö-kategoriassa voit ottaa käyttöön ja poistaa käytöstä [näköapuja.](#Vision) sekä muuttaa niiden asetuksia.

Huom: Käytettävissä olevia vaihtoehtoja voidaan laajentaa [lisäosien](#AddonsManager) avulla.
Tämä asetuskategoria sisältää oletusarvoisesti seuraavat vaihtoehdot:

##### Visuaalinen korostus {#VisionSettingsFocusHighlight}

Visuaalinen korostus -ryhmäsäätimessä olevat valintaruudut säätävät NVDA:n sisäänrakennetun [visuaalinen korostus](#VisionFocusHighlight) -ominaisuuden toimintaa.

* Ota korostus käyttöön: Ottaa visuaalisen korostuksen käyttöön tai poistaa sen käytöstä.
* Korosta kohdistus: Määrittää, korostetaanko [kohdistus.](#SystemFocus)
* Korosta navigointiobjekti: Määrittää, korostetaanko [navigointiobjekti.](#ObjectNavigation)
* Korosta selaustilakohdistin: Määrittää, korostetaanko [selaustilan virtuaalikohdistin.](#BrowseMode)

Huom: Ota korostus käyttöön -valintaruudun valitseminen tai valinnan poistaminen muuttaa vastaavasti myös kolmen muun valintaruudun tilaa.
Joten, jos Kohdistuksen korostus -valintaruutu ei ole valittuna, mutta valitset sen, kolme muuta valintaruutua valitaan myös automaattisesti.
Mikäli haluat korostaa pelkän kohdistuksen ja jättää navigointiobjektin sekä selaustilan valintaruudut valitsematta, Ota korostus käyttöön -valintaruudun tila muuttuu osittain valituksi.

##### Näyttöverho {#VisionSettingsScreenCurtain}

Voit ottaa [näyttöverhon](#VisionScreenCurtain) käyttöön valitsemalla Pimennä näyttö (vaikuttaa välittömästi) -valintaruudun.
Varoitus näytön pimentymisestä näytetään.
Ennen kuin jatkat valitsemalla "Kyllä", varmista, että puhe/pistekirjoitus on käytössä ja että pystyt käyttämään tietokonetta ilman näyttöä.
Valitse "Ei", jos et halua ottaa näyttöverhoa käyttöön.
Mikäli olet varma, voit ottaa näyttöverhon käyttöön valitsemalla Kyllä-painikkeen.
Jos et halua enää nähdä tätä varoitusta, voit poistaa sen käytöstä samassa valintaikkunassa.
Voit milloin tahansa palauttaa varoituksen käyttöön valitsemalla "Näytä varoitus aina, kun näyttöverho otetaan käyttöön" -valintaruudun.

NVDA toistaa oletusarvoisesti äänen, kun näyttöverho otetaan käyttöön tai poistetaan käytöstä.
 Jos haluat muuttaa tätä, voit poistaa valinnan "Toista ääni, kun näyttöverho otetaan käyttöön tai poistetaan käytöstä" -valintaruudusta.

##### Kolmannen osapuolen näön apuvälineiden asetukset {#VisionSettingsThirdPartyVisualAids}

Muita näönparannuksen tarjoajia voidaan asentaa [lisäosina.](#AddonsManager)
Mikäli näillä tarjoajilla on säädettäviä asetuksia, ne näytetään erillisissä ryhmissä tässä asetuskategoriassa.
Katso tietoja kunkin tarjoajan tukemista asetuksista kyseisen tarjoajan ohjeesta.

#### Näppäimistö {#KeyboardSettings}

<!-- KC:setting -->

##### Avaa näppäimistöasetukset {#toc188}

Pikanäppäin: `NVDA+Ctrl+K`

Näppäimistö-kategoria sisältää asetuksia, jotka määrittävät, miten NVDA käyttäytyy kirjoitettaessa ja käytettäessä näppäimistöä muilla tavoin.
Tämä asetuskategoria sisältää seuraavat asetukset:

##### Näppäinasettelu {#KeyboardSettingsLayout}

Tästä yhdistelmäruudusta valitaan, mitä näppäinasettelua NVDA käyttää. Tällä hetkellä käytettävissä olevat kaksi vaihtoehtoaovat Pöytäkone ja Kannettava.

##### Valitse NVDA-toimintonäppäimet {#KeyboardSettingsModifiers}

Tämän luettelon valintaruuduilla on mahdollista määrittää, mitä näppäimiä käytetään [NVDA-näppäiminä](#TheNVDAModifierKey). Valittavissa ovat seuraavat näppäimet:

* Caps Lock
* laskinnäppäimistön Insert
* laajennettu Insert (löytyy tavallisesti nuolinäppäinten yläpuolelta, Home- ja End-näppäinten läheltä)

Jos mitään näppäintä ei ole valittu, monien NVDA-komentojen käyttäminen voi olla mahdotonta, joten sinun on valittava vähintään yksi toimintonäppäin.

<!-- KC:setting -->

##### Puhu kirjoitetut merkit {#KeyboardSettingsSpeakTypedCharacters}

Pikanäppäin: `NVDA+2`

Kun tämä valintaruutu on valittuna, NVDA lukee kaikki kirjoitetut merkit.

<!-- KC:setting -->

##### Puhu kirjoitetut sanat {#KeyboardSettingsSpeakTypedWords}

Pikanäppäin: `NVDA+3`

Kun tämä valintaruutu on valittuna, NVDA lukee kaikki kirjoitetut sanat.

##### Keskeytä puhe merkkejä kirjoitettaessa {#KeyboardSettingsSpeechInteruptForCharacters}

Jos tämä valintaruutu on valittuna, puhe keskeytetään aina, kun näppäimistöltä syötetään jokin merkki. Asetus on oletusarvoisesti käytössä.

##### Keskeytä puhe Enter-näppäintä painettaessa {#KeyboardSettingsSpeechInteruptForEnter}

Jos tämä valintaruutu on valittuna, puhe keskeytetään aina Enter-näppäintä painettaessa. Asetus on oletusarvoisesti käytössä.

##### Salli pikaluku jatkuvassa luvussa {#KeyboardSettingsSkimReading}

Jos tämä asetus on käytössä, tietyt navigointikomennot (kuten selaustilan pikanavigointi tai riveittäin/kappaleittain liikkuminen) eivät keskeytä jatkuvaa lukua, vaan siirtävät uuteen sijaintiin, jonka jälkeen lukemista jatketaan.

##### Anna äänimerkki kirjoitettaessa pieniä kirjaimia Caps Lockin ollessa käytössä {#KeyboardSettingsBeepLowercase}

Kun tämä asetus on käytössä, kirjoitettaessa kirjaimia Vaihto-näppäin pohjassa kuuluu varoitusäänimerkki, Jos Caps Lock on päällä.
Vaihto-näppäin pohjassa kirjoittaminen Caps Lockin ollessa päällä on yleensä tahatonta ja johtuu tavallisesti siitä, ettei sen tajua olevan käytössä.
Tämän vuoksi siitä varoittaminen voi olla varsin hyödyllistä.

<!-- KC:setting -->

##### Puhu komentonäppäimet {#KeyboardSettingsSpeakCommandKeys}

Pikanäppäin: `NVDA+4`

Kun tämä valintaruutu on valittuna, NVDA puhuu kaikki painetut näppäimet, jotka eivät ole merkkejä. Näitä ovat sellaiset näppäinyhdistelmät kuin Ctrl+jokin muu kirjain.

##### Ilmaise kirjoitusvirheet kirjoitettaessa toistamalla ääni {#KeyboardSettingsAlertForSpellingErrors}

Tämän asetuksen ollessa käytössä toistetaan lyhyt summeriääni, kun kirjoitetussa sanassa on kirjoitusvirhe.
Asetus on käytettävissä vain, jos kirjoitusvirheiden ilmoittaminen on otettu käyttöön Asetukset-valintaikkunan [Asiakirjojen muotoilu -kategoriasta](#DocumentFormattingSettings).

##### Käsittele muiden sovellusten näppäinpainallukset {#KeyboardSettingsHandleKeys}

Tällä asetuksella käyttäjä voi määrittää, käsitteleekö NVDA esim. näyttönäppäimistöjen ja puheentunnistusohjelmistojen tuottamat näppäinpainallukset.
Asetus on oletusarvoisesti käytössä, mutta esim. vietnaminkielistä tekstiä UniKey-kirjoitusohjelmistolla kirjoittavat käyttäjät saattavat haluta poistaa sen käytöstä, sillä se aiheuttaa väärien merkkien syöttämistä.

#### Hiiri {#MouseSettings}

<!-- KC:setting -->

##### Avaa hiiriasetukset {#toc201}

Pikanäppäin: `NVDA+Ctrl+M`

Hiiri-kategoriassa NVDA:n voi määrittää seuraamaan hiirtä, ilmaisemaan hiiren koordinaatit äänimerkeillä sekä muuttaa muita hiiren käyttöön liittyviä asetuksia.
Tämä kategoria sisältää seuraavat asetukset:

##### Ilmoita hiirikohdistimen muodon muutokset {#MouseSettingsShape}

Kun tämä valintaruutu on valittuna, NVDA ilmoittaa joka kerta, kun hiiriosoittimen muoto muuttuu.
Windowsissa hiirikohdistin muuttaa muotoaan ilmaistakseen tiettyjä asioita, kuten että jokin on muokattava tai että jokin latautuu jne.

<!-- KC:setting -->

##### Käytä hiiren seurantaa {#MouseSettingsTracking}

Näppäinkomento: NVDA+M

Kun tämä valintaruutu on valittuna, NVDA lukee hiiriosoittimen alla olevan tekstin. Tällä tavalla on mahdollista löytää asioita ruudulta hiirtä liikuttamalla sen sijaan, että käytettäisiin objektinavigointia.

##### Tekstiyksikön tarkkuus {#MouseSettingsTextUnit}

Jos NVDA on asetettu lukemaan hiiren alla oleva teksti, Tämän asetuksen avulla voidaan määrittää tarkasti, minkä verran tekstiä luetaan.
Vaihtoehtoina ovat merkki, sana, rivi ja kappale.

Tekstiyksikön tarkkuutta voidaan muuttaa mistä tahansa liittämällä toimintoon näppäinkomento [Näppäinkomennot-valintaikkunassa](#InputGestures).

##### Puhu objekti hiiren siirtyessä siihen {#MouseSettingsRole}

Jos tämä valintaruutu on valittuna, NVDA puhuu objektien tiedot hiiren siirtyessä niihin.
Näitä tietoja ovat esim. objektin rooli (tyyppi) sekä tilat (valittu/painettu), taulukon solujen koordinaatit jne.
Huom: Joidenkin tietojen puhuminen voi olla riippuvaista siitä, miten muut asetukset on määritetty esim. [objektien lukeminen-](#ObjectPresentationSettings) tai [asiakirjojen muotoilu](#DocumentFormattingSettings) -kategorioissa.

##### Ilmaise hiiren koordinaatit äänimerkeillä {#MouseSettingsAudio}

Kun tämä valintaruutu on valittuna, NVDA antaa äänimerkkejä hiiren liikkuessa, jotta käyttäjä saa selville, missä hiiri on suhteessa ruudun kokoon.
Äänimerkit ovat sitä korkeampia, mitä ylempänä ruudulla hiiri on.
Mitä enemmän vasemmalla tai oikealla hiiri on, sitä enemmän vasemmalta tai oikealta ääni kuuluu (olettaen, että käytössä on stereokaiuttimet tai kuulokkeet).

##### Äänikoordinaatttien voimakkuutta säädetään ruudun kirkkauden mukaan {#MouseSettingsBrightness}

Jos Ilmaise hiiren koordinaatit äänimerkeillä -asetus on käytössä, tämän valintaruudun valitseminen tarkoittaa, että äänikoordinaattien voimakkuutta säädetään sen mukaan, miten kirkas ruutu on hiirikohdistimen alla.
Tämä asetus ei ole oletusarvoisesti käytössä.

##### Ohita hiirisyöte muista sovelluksista {#MouseSettingsHandleMouseControl}

Kun tämä asetus on käytössä, NVDA ohittaa hiiritapahtumat (liikuttaminen ja painikkeiden painallukset mukaan lukien), jotka ovat muiden sovellusten, kuten TeamViewerin ja muiden etähallintaohjelmistojen luomia.
Asetus ei ole käytössä oletusarvoisesti.
Jos tämä vaihtoehto on valittuna ja "Käytä hiiren seurantaa" -asetus on käytössä, NVDA ei puhu, mitä hiiren alla on, mikäli jokin toinen sovellus liikuttaa sitä.

#### Kosketuksen vuorovaikutus {#TouchInteraction}

Tästä asetuskategoriasta, joka on käytettävissä vain kosketusnäytöllisissä tietokoneissa, voidaan määrittää, miten NVDA on vuorovaikutuksessa kosketusnäyttöjen kanssa.
Kategoriassa on seuraavat asetukset:

##### Ota käyttöön kosketusvuorovaikutuksen tuki {#TouchSupportEnable}

Tämä valintaruutu ottaa käyttöön NVDA:n kosketusvuorovaikutuksen tuen.
Jos se on valittuna, voit käyttää sormiasi kosketusnäyttölaitteen näytöllä olevissa kohteissa liikkumiseen sekä vuorovaikutukseen niiden kanssa.
Jos valintaruutu ei ole valittuna, kosketusnäytön tuki on poissa käytöstä ikään kuin NVDA ei olisi käynnissä.
Tätä asetusta voidaan vaihtaa myös painamalla NVDA+Ctrl+Alt+T.

##### Kosketuskirjoitustila {#TouchTypingMode}

Tällä valintaruudulla määritetään menetelmä, jota halutaan käyttää kirjoitettaessa tekstiä kosketusnäppäimistöllä.
Kun valintaruutu on valittuna, haluttua näppäintä painetaan etsimällä se näppäimistöltä ja nostamalla sormi näytöltä.
Mikäli valintaruutu ei ole valittuna, näppäintä on painettava kaksoisnapauttamalla.

#### Tarkastelukohdistin {#ReviewCursorSettings}

Tarkastelukohdistin-kategoriaa käytetään NVDA:n tarkastelukohdistimen toimintaan vaikuttavien asetusten määrittämiseen.
Kategoria sisältää seuraavat asetukset:

<!-- KC:setting -->

##### Seuraa järjestelmän kohdistusta {#ReviewCursorFollowFocus}

Näppäinkomento: NVDA+7

Kun tämä asetus on käytössä, tarkastelukohdistin sijoitetaan aina samaan objektiin kuin nykyinen järjestelmän kohdistus sen muuttuessa.

<!-- KC:setting -->

##### Seuraa kohdistinta {#ReviewCursorFollowCaret}

Pikanäppäin: `NVDA+6`

Kun tämä asetus on käytössä, tarkastelukohdistin siirretään automaattisesti kohdistimen kohdalle aina sen liikkuessa.

##### Seuraa hiirikohdistinta {#ReviewCursorFollowMouse}

Kun tämä asetus on käytössä, tarkastelukohdistin seuraa hiirtä sen liikkuessa.

##### Yksinkertainen objektinavigointi {#ReviewCursorSimple}

Kun tämä asetus on käytössä, NVDA suodattaa objektihierarkiasta pois sellaiset objektit, joilla ei ole merkitystä käyttäjälle, esim. näkymättömät tai asettelutarkoituksiin käytettävät.

Yksinkertainen tarkastelutila otetaan käyttöön tai poistetaan käytöstä mistä tahansa määrittämällä sille oma näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

#### Objektien lukeminen {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Avaa objektien lukemisen asetukset {#toc218}

Pikanäppäin: `NVDA+Ctrl+O`

Objektien lukeminen -kategoriaa käytetään määrittämään, kuinka paljon säädinten tietoja, kuten kuvaus, sijaintitiedot jne., NVDA lukee.
Nämä asetukset eivät yleensä koske selaustilaa.
Ne koskevat tyypillisesti kohdistuksen ilmaisemista ja NVDA:n objektinavigointia, mutta ei tekstin lukemista esim. selaustilassa.

##### Lue työkaluvihjeet {#ObjectPresentationReportToolTips}

Kun tämä valintaruutu on valittuna, NVDA lukee työkaluvihjeet niiden tullessa näkyviin.
Monet ikkunat ja säätimet näyttävät pienen ilmoituksen (tai työkaluvihjeen), kun hiiri siirretään niiden päälle tai toisinaan kun kohdistus siirretään niihin.

##### Lue ilmoitukset {#ObjectPresentationReportNotifications}

Kun tämä valintaruutu on valittuna, NVDA lukee ohjeselitteet ja ilmoitusruudut niiden tullessa näkyviin.

* Ohjeselitteet ovat työkaluvihjeiden kaltaisia, mutta yleensä suurempia ja liittyvät järjestelmätapahtumiin, kuten verkkokaapelin irrottamiseen tai ilmoituksiin Windowsin suojausongelmista.
* Ilmoitusruudut on esitelty Windows 10:ssä, ja ne ilmestyvät toimintokeskukseen ilmaisinalueella ilmoittaen useista eri tapahtumista (esim. ladatusta päivityksestä, Saapuneet-kansioosi tulleesta uudesta sähköpostiviestistä jne.).

##### Lue objektien pikanäppäimet {#ObjectPresentationShortcutKeys}

Kun tämä valintaruutu on valittuna, NVDA kertoo objektiin tai säätimeen liitetyn pikanäppäimen.
Valikkorivin Tiedosto-valikolla voi esimerkiksi olla pikanäppäin Alt+t.

##### Lue objektien sijaintitiedot {#ObjectPresentationPositionInfo}

Tällä asetuksella voidaan määrittää, luetaanko objektin sijainti (esim. 1 / 4) siirryttäessä siihen kohdistuksella tai objektinavigoinnilla.

##### Arvaa objektien sijaintitiedot, kun niitä ei ole käytettävissä {#ObjectPresentationGuessPositionInfo}

Jos objektien sijaintitietojen lukeminen on käytössä, tämän asetuksen avulla NVDA voi arvata objektien sijaintitiedot silloin, kun niitä ei ole saatavilla jostakin säätimestä muilla tavoin.

Kun tämä asetus on käytössä, NVDA lukee sijaintitiedot entistä useammissa säätimissä, kuten valikoissa ja työkaluriveissä. Tiedot voivat kuitenkin olla hieman epätarkkoja.

##### Lue objektien kuvaukset {#ObjectPresentationReportDescriptions}

Poista tämän valintaruudun valinta, mikäli et halua kuulla objektien kuvauksia (esim. hakuehdotuksia, koko valintaikkunan lukemista heti sen avauduttua jne.).

<!-- KC:setting -->

##### Edistymispalkkien päivitykset {#ObjectPresentationProgressBarOutput}

Näppäinkomento: NVDA+U

Tämä asetus määrittää, miten NVDA ilmaisee edistymispalkkien päivittymisen.

Seuraavat vaihtoehdot ovat käytettävissä:

* Pois: Edistymispalkkeja ei lueta.
* Puhu: Edistymispalkit puhutaan prosentteina. NVDA puhuu uuden arvon aina edistymispalkin muuttuessa.
* Anna äänimerkki: NVDA antaa äänimerkin aina edistymispalkin muuttuessa. Mitä korkeampi äänimerkki, sitä lähempänä loppua edistymispalkki on.
* Puhu ja anna äänimerkki: NVDA sekä antaa äänimerkin että puhuu edistymispalkin arvon.

##### Ilmaise taustalla olevat edistymispalkit {#ObjectPresentationReportBackgroundProgressBars}

Kun tämä asetus on käytössä, NVDA ilmaisee edistymispalkin päivitykset, vaikkei se ole edustalla (aktiivisena).
Jos edistymispalkin sisältävä ikkuna pienennetään tai siirrytään pois sellaisesta, NVDA seuraa edistymispalkkia, jolloin voidaan tehdä samalla jotain muuta.

<!-- KC:setting -->

##### Puhu dynaamisen sisällön muutokset {#ObjectPresentationReportDynamicContent}

Pikanäppäin: `NVDA+5`

Ottaa käyttöön tai poistaa käytöstä uuden sisällön puhumisen tietyissä objekteissa, kuten pääteohjelmissa ja pikaviestiohjelmien historiasäätimissä.

##### Toista ääni automaattisten ehdotusten tullessa näkyviin {#ObjectPresentationSuggestionSounds}

Ottaa käyttöön tai poistaa käytöstä automaattisten ehdotusten ilmoittamisen niiden tullessa näkyviin, ja mikäli asetus on käytössä, NVDA toistaa äänen, joka ilmaisee tämän.
Automaattiset ehdotukset ovat luetteloita ehdotetuista kohteista, jotka perustuvat tiettyihin hakukenttiin ja asiakirjoihin syötettyyn tekstiin.
Kun esim. kirjoitetaan Windows Vistan ja uudempien Käynnistä-valikon hakukenttään, Windows näyttää luettelon kirjoitettuun tekstiin perustuvista ehdotuksista.
Joissakin muokkauskentissä, kuten useissa Windows 10:n sovellusten hakukentissä, NVDA voi ilmoittaa kirjoitettaessa ehdotusluettelon ilmestymisestä.
Automaattisten ehdotusten luettelo sulkeutuu, kun on siirrytty pois muokkauskentästä, ja NVDA voi joissakin kentissä myös ilmoittaa siitä.

#### Syöttömenetelmä {#InputCompositionSettings}

Syöttömenetelmä-kategoriasta voidaan säätää, miten NVDA ilmoittaa aasialaisten kielten merkit niitä syötettäessä, esim. IME- tai Tekstipalvelu-syöttömenetelmiä käytettäessä.
Huom: Koska syöttömenetelmät poikkeavat toisistaan suuresti ominaisuuksiltaan ja tiedonvälitystavoiltaan, nämä asetukset on todennäköisesti tarpeen määrittää eri tavalla kullekin menetelmälle tehokkaimman kirjoituskokemuksen varmistamiseksi.

##### Lue kaikki ehdotukset automaattisesti {#InputCompositionReportAllCandidates}

Tällä asetuksella, joka on oletusarvoisesti käytössä, voidaan valita, luetaanko kaikki näkyvissä olevat ehdotukset automaattisesti niiden luettelon tullessa näkyviin tai sen sivua vaihdettaessa.
Tämän käyttäminen kuvakirjoituksen syöttömenetelmille, kuten kiinalainen uusi ChangJie tai Boshiami, on hyödyllistä, koska kaikki symbolit ja niiden numerot on mahdollista kuulla automaattisesti ja niistä voidaan valita heti haluttu vaihtoehto.
Foneettisille syöttömenetelmille, kuten uusi foneettinen kiina, saattaa kuitenkin olla hyödyllisempää poistaa asetus käytöstä, sillä kaikki symbolit kuulostavat samalta, ja luettelokohteissa on liikuttava yksitellen lisätietojen saamiseksi kunkin ehdotuksen merkkikuvauksista.

##### Lue valittu ehdotus {#InputCompositionAnnounceSelectedCandidate}

Tällä asetuksella, joka on oletusarvoisesti käytössä, voidaan valita, lukeeko NVDA valitun ehdotuksen ehdotusluettelon tullessa näkyviin tai valintaa muutettaessa.
Tämä on tarpeen sellaisissa syöttömenetelmissä, joissa valintaa voidaan muuttaa nuolinäppäimillä (kuten esim. uusi foneettinen kiina), mutta joissakin kirjoittaminen saattaa olla tehokkaampaa, kun asetus on poistettu käytöstä.
Huomaa, että vaikka tämä asetus ei ole käytössä, tarkastelukohdistin sijoitetaan silti valitun ehdotuksen kohdalle, mikä mahdollistaa objektinavigoinnin tai tekstintarkastelukomentojen käyttämisen kyseessä olevan tai muiden ehdotusten lukemiseen.

##### Ilmoita lyhyet merkkikuvaukset aina ehdotuksia luettaessa {#InputCompositionCandidateIncludesShortCharacterDescription}

Tällä asetuksella, joka on oletusarvoisesti käytössä, voidaan valita, lukeeko NVDA lyhyen kuvauksen kustakin ehdotuksen merkistä joko ehdotusta valittaessa tai automaattisesti luettaessa ehdotusluettelon tullessa näkyviin.
Huomaa, että asetus ei vaikuta valitun ehdotuksen lisämerkkikuvausten lukemiseen sellaisissa kielissä kuin kiina.
Tästä saattaa olla hyötyä korean ja japanin syöttömenetelmiä käytettäessä.

##### Ilmoita lukumerkkijonon muutokset {#InputCompositionReadingStringChanges}

Joillakin syöttömenetelmillä, kuten uudella foneettisella kiinalla ja uudella ChangJiella, on lukumerkkijono (tunnetaan joskus myös esiyhdistelmän merkkijonona).
Tällä asetuksella voidaan valita, ilmoittaako NVDA lukumerkkijonoon kirjoitettavat uudet merkit.
Asetus on oletusarvoisesti käytössä.
Huomaa, että jotkin vanhemmat syöttömenetelmät, kuten kiinalainen ChangJie, eivät ehkä käytä lukumerkkijonoa esiyhdistelmän merkkien säilyttämiseen, vaan käyttävät niiden sijaan suoraan merkkiyhdistelmää. Katso seuraavaa asetusta merkkiyhdistelmän lukemisen määrittämiseksi.

##### Lue merkkiyhdistelmän muutokset {#InputCompositionCompositionStringChanges}

Kun luku- tai esiyhdistelmätiedot on yhdistetty kelvolliseksi kuvakirjoitussymboliksi, useimmat syöttömenetelmät sijoittavat sen tilapäisesti talteen merkkiyhdistelmään muiden yhdistettyjen symbolien kanssa ennen niiden lopullista asiakirjaan lisäämistä.
Tällä asetuksella voidaan valita, lukeeko NVDA uudet symbolit niiden tullessa näkyviin merkkiyhdistelmässä.
Asetus on oletusarvoisesti käytössä.

#### Selaustila {#BrowseModeSettings}

<!-- KC:setting -->

##### Avaa selaustilan asetukset {#toc236}

Pikanäppäin: `NVDA+Ctrl+B`

NVDA:n asetusvalintaikkunan Selaustila-kategoriaa käytetään määrittämään NVDA:n toimintaa luettaessa ja liikuttaessa monisisältöisissä asiakirjoissa, kuten verkkosivuilla.
Kategoria sisältää seuraavat asetukset:

##### Merkkien enimmäismäärä rivillä {#BrowseModeSettingsMaxLength}

Tämä asettaa selaustilan rivin enimmäispituuden merkkeinä.

##### Rivien enimmäismäärä sivulla {#BrowseModeSettingsPageLines}

Tämä asettaa rivimäärän, joka selaustilassa siirrytään painettaessa Page up- tai Page down -näppäintä.

<!-- KC:setting -->

##### Käytä ruutuasettelua {#BrowseModeSettingsScreenLayout}

Pikanäppäin: `NVDA+V`

Tällä asetuksella voidaan määrittää, sijoitetaanko napsautettava sisältö (linkit, painikkeet ja kentät) selaustilassa omille riveilleen vai säilytetäänkö ne sellaisina kuin ne ruudulla näytetään.
Huom: Tämä asetus ei koske Microsoft Office -sovelluksia kuten Outlookia tai Wordia, joissa käytetään aina ruutuasettelua.
Kun ruutuasettelu on käytössä, sivun elementit pysyvät sellaisina kuin ne visuaalisesti näytetään.
Esimerkiksi useita linkkejä sisältävä visuaalinen rivi puhutaan ja näytetään pistenäytöllä samalla rivillä olevina useina linkkeinä.
Jos asetus ei ole käytössä, sivun elementit sijoitetaan omille riveilleen.
Tätä voi olla helpompi ymmärtää sivua riveittäin selattaessa, ja vuorovaikutus kohteiden kanssa saattaa olla joillekin käyttäjille helpompaa.

##### Ota selaustila käyttöön sivua ladattaessa {#BrowseModeSettingsEnableOnPageLoad}

Tällä valintaruudulla voidaan määrittää, otetaanko selaustila käyttöön automaattisesti sivua ladattaessa.
Kun asetus ei ole käytössä, selaustila voidaan edelleen ottaa käyttöön manuaalisesti verkkosivuilla tai asiakirjoissa, joissa selaustilaa tuetaan.
Luettelo selaustilaa tukevista sovelluksista on [Selaustila](#BrowseMode)-osiossa.
Huom: Tämä asetus ei koske sovelluksia, joissa selaustila on aina valinnainen, kuten esim. Microsoft Wordissa.
Asetus on oletusarvoisesti käytössä.

##### Lue sivu automaattisesti sen avauduttua {#BrowseModeSettingsAutoSayAll}

Tämä asetus määrittää, luetaanko sivu selaustilassa automaattisesti sen avauduttua.
Asetus on oletusarvoisesti käytössä.

##### Sisällytä asettelutaulukot {#BrowseModeSettingsIncludeLayoutTables}

Tämä asetus vaikuttaa siihen, miten NVDA käsittelee puhtaasti visuaaliseen esittämiseen käytettäviä taulukoita.
Kun asetus on käytössä, NVDA käsittelee niitä normaaleina taulukoina (ts. lukee [asiakirjojen muotoiluasetusten](#DocumentFormattingSettings) mukaisesti sekä löytää ne pikanavigointikomennoilla).
Kun asetus on poistettu käytöstä, asettelutaulukoita ei lueta eikä löydetä pikanavigointikomennoilla.
Taulukoiden sisältö näytetään kuitenkin tavallisena tekstinä.
Asetus on oletusarvoisesti poissa käytöstä.

Asettelutaulukoiden ilmaiseminen otetaan käyttöön tai poistetaan käytöstä mistä tahansa määrittämällä näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Elementtien ilmoittamisen määrittäminen {#BrowseModeLinksAndHeadings}

Ilmoitettavat elementit, kuten linkit, otsikot ja taulukot, määritetään [Asetukset](#NVDASettings)-valintaikkunan [Asiakirjojen muotoilu -kategoriassa](#DocumentFormattingSettings) olevia asetuksia käyttäen.

##### Automaattinen vuorovaikutustila kohdistuksen muuttuessa {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Kun tämä valintaruutu on valittuna, vuorovaikutustila otetaan käyttöön, jos kohdistus muuttuu.
Kun esim. verkkosivulla siirryt sarkaimella lomakkeen kohdalle tämän asetuksen ollessa käytössä, vuorovaikutustila otetaan käyttöön automaattisesti.
Mikäli siirryt nuolinäppäimillä pois muokkauskentästä, NVDA vaihtaa takaisin selaustilaan.

##### Automaattinen vuorovaikutustila kohdistinta siirrettäessä {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Kun tämä asetus on käytössä, NVDA siirtyy automaattisesti vuorovaikutustilaan ja siitä pois nuolinäppäimillä liikuttaessa.
Jos esim. verkkosivua nuolinäppäimillä selattaessa tullaan muokkauskentän kohdalle, NVDA ottaa vuorovaikutustilan käyttöön automaattisesti. Jos kentästä siirrytään pois nuolinäppäimillä, palataan takaisin selaustilaan.

##### Ilmaise vuorovaikutus- ja selaustilat äänimerkillä {#BrowseModeSettingsPassThroughAudioIndication}

Jos tämä asetus on käytössä, NVDA toistaa äänimerkin vaihtaessaan selaus- ja vuorovaikutustilojen välillä sen sijaan, että siitä ilmoitettaisiin puheella.

##### Estä muiden kuin näppäinkomentojen pääsy asiakirjaan {#BrowseModeSettingsTrapNonCommandGestures}

Tällä oletusarvoisesti käytössä olevalla asetuksella voidaan valita, estetäänkö näppäinkomentojen (kuten näppäinpainallusten), jotka eivät suorita NVDA-komentoa tai joita ei pidetä yleisinä komentonäppäiminä, pääsy aktiivisena olevaan asiakirjaan.
Esim. jos asetuksen ollessa käytössä painetaan J-kirjainta, sen tulostuminen asiakirjaan estetään, sillä se ei ole pikanavigointinäppäin, tai koska on epätodennäköistä, että se olisi sovelluksen käytössä oleva näppäinkomento.
NVDA käskee Windowsia toistamaan oletusäänen, kun estettyä näppäintä painetaan.

<!-- KC:setting -->

##### Siirrä kohdistus automaattisesti kohdistettaviin elementteihin {#BrowseModeSettingsAutoFocusFocusableElements}

Näppäin: NVDA+8

Tällä asetuksella, joka on oletusarvoisesti poissa käytöstä, voit valita, siirretäänkö kohdistus automaattisesti sellaisiin elementteihin, joihin kohdistuksen on mahdollista siirtyä (linkit, lomakekentät jne.) liikuttaessa sisällössä selaustilakohdistimella.
Asetuksen ollessa poissa käytöstä kohdistusta ei siirretä automaattisesti kohdistettaviin elementteihin, kun ne valitaan selaustilakohdistimella.
Tästä voi olla seurauksena nopeampi selauskokemus sekä parempi reagointi selaustilassa.
Kohdistus päivitetään kuitenkin elementin kohdalle, kun sen kanssa ollaan vuorovaikutuksessa (esim. painetaan painiketta tai valitaan valintaruutu).
Tämän asetuksen käyttöön ottaminen voi parantaa joidenkin verkkosivustojen tukea suorituskyvyn ja vakauden kustannuksella.

#### Asiakirjojen muotoilu {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Avaa asiakirjojen muotoiluasetukset {#toc250}

Pikanäppäin: `NVDA+Ctrl+D`

Useimmilla tämän kategorian valintaruuduilla voidaan määrittää, minkä tyyppisiä muotoilutietoja halutaan automaattisesti kuulla siirrettäessä kohdistinta asiakirjoissa.
Jos esim. valitaan Lue fontti -valintaruutu, NVDA kertoo fontin nimen aina kun siirrytään nuolinäppäimillä sellaisen tekstin kohdalle, jonka fontti eroaa aikaisemmasta.

Asiakirjojen muotoiluasetukset on järjestetty ryhmiin.
Seuraavien tietojen lukeminen voidaan määrittää:

* Fontti
  * Fontin nimi
  * Fontin koko
  * Fontin määreet
  * Ylä- ja alaindeksit
  * Korostus
  * Korostettu (merkitty) teksti
  * Tyyli
  * Värit
* Asiakirjan tiedot
  * Kommentit
  * Kirjanmerkit
  * Muokkausmerkinnät
  * Kirjoitusvirheet
* Sivut ja välit
  * Sivunumerot
  * Rivinumerot
  * Rivien sisennysten ilmoittaminen [(ei käytössä, puheella, äänimerkeillä, puheella ja äänimerkeillä)](#DocumentFormattingSettingsLineIndentation)
  * Tyhjien rivien ohittaminen rivien sisennyksiä ilmoitettaessa
  * Kappalesisennykset (esim. riippuva ja ensimmäisen rivin sisennys)
  * Rivivälit (yksin- ja kaksinkertainen jne.)
  * Tasaus
* Taulukon tiedot
  * Taulukot
  * Rivi- ja sarakeotsikot (Ei käytössä, Rivit, Sarakkeet, Rivit ja sarakkeet)
  * Solun koordinaatit
  * Solun reunat (ei käytössä, tyylit, värit ja tyylit)
* Elementit
  * Otsikot
  * Linkit
  * Grafiikat
  * Luettelot
  * Sisennetyt lainaukset
  * Ryhmät
  * Kiintopisteet
  * Artikkelit
  * Kehykset
  * Kuvat ja kuvatekstit
  * Napsautettavat kohteet

Nämä asetukset voidaan ottaa käyttöön tai poistaa käytöstä mistä tahansa Määrittämällä niille omat näppäinkomennot [Näppäinkomennot-valintaikkunaa käyttäen.](#InputGestures)

##### Ilmoita kohdistimen jälkeiset muotoilumuutokset {#DocumentFormattingDetectFormatAfterCursor}

Jos tämä asetus on käytössä, NVDA yrittää havaita kaikki rivillä olevat muotoilumuutokset sitä lukiessaan, vaikka se voikin hidastaa NVDA:n suorituskykyä.

NVDA havaitsee oletusarvoisesti järjestelmä- ja tarkastelukohdistimen kohdalla olevat muotoilut, ja joissakin tapauksissa lopunkin rivin, mutta vain, jos se ei aiheuta suorituskyvyn heikkenemistä.

Tämä asetus kannattaa ottaa käyttöön oikoluettaessa asiakirjoja esim. WordPadissa, kun muotoilut ovat tärkeitä.

##### Rivien sisennysten ilmoittaminen {#DocumentFormattingSettingsLineIndentation}

Tällä asetuksella määritetään, miten rivien alussa olevat sisennykset ilmoitetaan.
Rivien sisennysten ilmoittaminen -yhdistelmäruudussa on neljä vaihtoehtoa.

* ei käytössä: NVDA ei käsittele sisennyksiä.
* puheella: Jos tämä on valittuna, NVDA sanoo sisennysten määrän muuttuessa jotain sellaista kuin "12 väli" tai "neljä sarkain".
* äänimerkeillä: Jos tämä on valittuna, äänimerkit ilmaisevat sisennysten määrän sen muuttuessa.
Äänimerkin korkeus nousee jokaisen välilyönnin kohdalla, ja sarkainmerkki vastaa neljää välilyöntiä.
* puheella ja äänimerkeillä: Tämän ollessa valittuna sisennykset ilmoitetaan molempia yllä olevia vaihtoehtoja käyttäen.

Jos valitset "Ohita tyhjät rivit rivien sisennystä ilmoitettaessa" -valintaruudun, sisennyksen muutoksia ei ilmoiteta tyhjillä riveillä.
Tästä voi olla hyötyä luettaessa asiakirjaa, jossa tyhjiä rivejä käytetään sisennettyjen tekstilohkojen erottamiseen, kuten esim. lähdekoodissa.

#### Asiakirjan selaus {#DocumentNavigation}

Tästä kategoriasta voit säätää asiakirjan selauksen asetuksia.

##### Kappaletyyli {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Sovelluksen määrittämä), Sovelluksen määrittämä, Yksi rivinvaihto, Useita rivinvaihtoja|
|Oletus |Sovelluksen määrittämä|

Tästä yhdistelmäruudusta voit valita kappaletyylin, jota käytetään kappaleittain liikuttaessa näppäinkomennoilla `Ctrl+Nuoli ylös` ja `Ctrl+Nuoli alas`.
Seuraavat kappaletyylit ovat käytettävissä:

* Sovelluksen määrittämä: NVDA antaa sovelluksen määrittää edellisen tai seuraavan kappaleen, ja lukee uuden kappaleen siirryttäessä siihen.
Tämä tyyli, joka on käytössä oletusarvoisesti, toimii parhaiten, kun sovellus tukee kappaleittain liikkumista.
* Yksi rivinvaihto: NVDA yrittää määrittää edellisen tai seuraavan kappaleen käyttäen yhtä rivinvaihtoa kappaleenilmaisimena.
Tämä tyyli toimii parhaiten, kun asiakirjoja luetaan sovelluksessa, joka ei tue kappaleittain liikkumista ja asiakirjan kappaleet on merkitty yhdellä Enter-näppäimen painalluksella.
* Useita rivinvaihtoja: NVDA yrittää määrittää edellisen tai seuraavan kappaleen käyttäen ainakin yhtä tyhjää riviä (kaksi `Enter`-näppäimen painallusta) kappaleenilmaisimena.
Tämä tyyli toimii parhaiten asiakirjoissa, joissa käytetään lohkokappaleita.
Huom: Tätä tyyliä ei voi käyttää Microsoft Wordissa eikä Outlookissa, ellei "Käytä UI Automation -rajapintaa Microsoft Wordin asiakirjasäätimissä" -asetus ole käytössä.

Voit vaihtaa käytettävissä olevien kappaletyylien välillä mistä tahansa määrittämällä näppäinkomennon [Näppäinkomennot-valintaikkunassa](#InputGestures).

#### Windowsin tekstintunnistusasetukset {#Win10OcrSettings}

Tämän kategorian asetuksilla voit vaikuttaa [Windowsin tekstintunnistuksen](#Win10Ocr) toimintaan.
Kategoria sisältää seuraavat asetukset:

##### Tunnistuksen kieli {#Win10OcrSettingsRecognitionLanguage}

Tästä yhdistelmäruudusta voit valita tekstintunnistuksen käyttämän kielen.
Voit vaihtaa käytettävissä olevien kielten välillä mistä tahansa määrittämällä kyseiselle komennolle oman pikanäppäimen [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

##### Päivitä tunnistettu sisältö automaattisesti {#Win10OcrSettingsAutoRefresh}

Kun tämä valintaruutu on valittuna, NVDA päivittää tunnistetun sisällön automaattisesti, kun tunnistuksen tulos on aktiivisena.
Tämä voi olla erittäin hyödyllistä silloin, kun haluat seurata jatkuvasti muuttuvaa sisältöä, kuten esim. katsoessasi videota tekstitysten kanssa.
Sisältöä päivitetään puolentoista sekunnin välein.
Tämä asetus on oletusarvoisesti poissa käytöstä.

#### Lisäasetukset {#AdvancedSettings}

Varoitus! Tämän kategorian asetukset on tarkoitettu vain edistyneille käyttäjille, ja voivat saada väärin muutettuina NVDA:n toimimaan virheellisesti.
Näihin asetuksiin tulee tehdä muutoksia vain, jos olet varma, mitä teet tai jos NVDA:n kehittäjä on neuvonut tekemään niin.

##### Muutosten tekeminen {#AdvancedSettingsMakingChanges}

Jotta lisäasetuksiin voidaan tehdä muutoksia, säätimet on ensin otettava käyttöön valintaruudulla, jolla vahvistetaan, että näiden asetusten muuttamisen riskit ymmärretään.

##### Oletusasetusten palauttaminen {#AdvancedSettingsRestoringDefaults}

Palauta oletukset -painike palauttaa asetusten oletusarvot, vaikka vahvistusvalintaruutua ei ole valittu.
Oletusarvojen palauttaminen voi olla joskus tarpeen, kun asetuksia on muutettu.
Näin voi tehdä myös silloin, jos ei ole varma, onko asetuksia muutettu.

##### Lataa käyttäjän oma koodi kehittäjien scratchpad-hakemistosta {#AdvancedSettingsEnableScratchpad}

Koodin testaaminen on hyödyllistä NVDA:n lisäosia kehitettäessä.
Tämä asetus sallii käytössä ollessaan NVDA:n ladata mukautettuja sovellusmoduuleita, yleisliitännäisiä, pistenäyttö- ja syntetisaattoriajureita sekä näönparannuksen tarjoajia erityisestä kehittäjille tarkoitetusta scratchpad-nimisestä hakemistosta, joka sijaitsee NVDA:n käyttäjän asetushakemistossa.
Kuten niiden vastineet lisäosissa, nämä moduulit ladataan NVDA:ta käynnistettäessä tai sovellusmoduulien ja yleisliitännäisten tapauksessa [liitännäisiä uudelleenladattaessa](#ReloadPlugins).
Tämä asetus on oletusarvoisesti poissa käytöstä, mikä varmistaa, ettei NVDA suorita testaamatonta koodia käyttäjän tietämättä.
Jos haluat jakaa koodiasi muille käyttäjille, se tulee paketoida NVDA:n lisäosaksi.

##### Avaa kehittäjien scratchpad-hakemisto {#AdvancedSettingsOpenScratchpadDir}

Tämä painike avaa hakemiston, johon kehittäjä voi sijoittaa koodiaan.
Se on käytettävissä vain, jos NVDA on määritetty lataamaan mukautettua koodia kehittäjien scratchpad-hakemistosta.

##### UI Automation -tapahtumien ja ominaisuusmuutosten rekisteröinti {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Automaattinen, Valikoiva, Yleinen|
|Oletus |Automaattinen|

Tä	mä asetus muuttaa tapaa, jolla NVDA rekisteröi Microsoft UI Automation -saavutettavuusrajapinnan käynnistämiä tapahtumia.
UI Automation -tapahtumien ja ominaisuusmuutosten rekisteröinti -yhdistelmäruudussa on kolme vaihtoehtoa:

* Automaattinen: "valikoiva" Windows 11 Sun Valley 2:ssa (versio 22H2) ja sitä uudemmissa, muutoin "yleinen".
* Valikoiva: NVDA rajoittaa useimpien tapahtumien rekisteröinnin järjestelmän kohdistukseen.
Mikäli sinulla on suorituskykyongelmia yhdessä tai useammassa sovelluksessa, suosittelemme, että kokeilet tätä toimintoa nähdäksesi, paraneeko suorituskyky.
Vanhemmissa Windows-versioissa NVDA:lla saattaa kuitenkin olla vaikeuksia seurata kohdistusta joissakin säätimissä (kuten tehtävienhallinnassa ja emojipaneelissa).
* Yleinen: NVDA rekisteröi useita UIA-tapahtumia, jotka se on käsitellyt ja hylännyt prosessinsa sisällä.
Vaikka kohdistuksen seuranta on luotettavampaa useammissa tilanteissa, suorituskyky heikkenee merkittävästi tietyissä sovelluksissa, erityisesti Microsoft Visual Studiossa.

##### Käytä UI automation -rajapintaa Microsoft Wordin asiakirjasäätimissä {#MSWordUIA}

Tämä asetus määrittää, käyttääkö NVDA UI Automation -saavutettavuusrajapintaa Microsoft Word -asiakirjoissa vanhemman objektimallin asemesta.
Tämä koskee Microsoft wordin asiakirjojen lisäksi Microsoft Outlookin viestejä.
Asetus sisältää seuraavat arvot:

* Oletus (kun käytettävissä)
* Vain tarvittaessa: Kun Microsoft Wordin objektimalli ei ole käytettävissä.
* Kun käytettävissä: Microsoft Wordin versio 16.0.15000 tai uudempi, tai kun Wordin objektimalli ei ole käytettävissä.
* Aina: Aina kun UI automation -rajapinta on käytettävissä Microsoft wordissa (riippumatta siitä, miten valmis se on).

##### Käytä UI Automation -rajapintaa Microsoft Excelin laskentataulukkosäätimissä, kun käytettävissä {#UseUiaForExcel}

Kun tämä asetus on otettu käyttöön, NVDA yrittää käyttää Microsoftin UI Automation -saavutettavuusrajapintaa tietojen hakemiseen Microsoft Excelin laskentatauluKkosäätimistä.
Tämä on kokeellinen ominaisuus, eivätkä kaikki Excelin ominaisuudet ole välttämättä käytettävissä tässä tilassa.
Tällaisia ovat esim. NVDA:n elementtilista kaavojen ja kommenttien näyttämiseen sekä laskentataulukon lomakekenttiin siirtävät selaustilan pikanavigointikomennot.
Laskentataulukon perusnavigointiin/muokkaukseen tämä asetus saattaa kuitenkin tarjota merkittävän suorituskyvyn parannuksen.
Emme vielä suosittele tämän asetuksen oletusarvoista käyttöön ottoa suurimmalle osalle käyttäjistä, mutta Excel 16.0.13522.10000 tai uudemman käyttäjiltä palaute on tervetullutta.
Excelin UI automation -rajapinnan toteutus muuttuu jatkuvasti, eivätkä Microsoft Officen 16.0.13522.10000:ta vanhemmat versiot välttämättä tarjoa tarpeeksi tietoja tämän asetuksen hyödyntämiseen.

##### Käytä laajennettua tapahtumienkäsittelyä {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Käytössä), Ei käytössä, Käytössä|
|Oletus |Käytössä|

Kun tämä asetus on käytössä, NVDA:n pitäisi reagoida nopeasti komentoihin, vaikka se vastaanottaisi runsaasti UI Automation -tapahtumia, kuten paljon tekstiä päätteessä.
Kun asetusta on muutettu, NVDA on käynnistettävä uudelleen, jotta muutos tulee voimaan.

##### Windows-konsolin tuki {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Automaattinen, UIA kun käytettävissä, Vanha|
|Oletus |Automaattinen|

Tämä asetus määrittää, miten NVDA toimii vuorovaikutuksessa Windows-konsolin kanssa, jota Komentokehote, PowerShell ja Windowsin Linux-alijärjestelmä käyttävät.
Se ei vaikuta moderniin Windows-päätteeseen.
Windows 10:n versiossa 1709 Microsoft [lisäsi konsoliin tuen UI Automation -rajapinnalle](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), mikä parantaa huomattavasti sitä tukevien näytönlukuohjelmien suorituskykyä ja vakautta.
NVDA:n vanha konsolituki on käytettävissä varavaihtoehtona tilanteissa, joissa UI Automation -rajapinta ei ole käytettävissä tai sen tiedetään johtavan huonompaan käyttökokemukseen.
Windows-konsolituen yhdistelmäruudussa on kolme vaihtoehtoa:

* Automaattinen: Käyttää UI Automation -rajapintaa Windows 11 -version 22H2 ja uudempien mukana toimitetussa Windows-konsolin versiossa.
Tätä vaihtoehtoa suositellaan ja se on määritetty oletukseksi.
* UIA, kun käytettävissä: Käyttää UI Automation -rajapintaa konsoleissa, mikäli se on käytettävissä, jopa versioissa, joissa on epätäydellisiä tai virheellisiä toteutuksia.
Vaikka tällainen rajoitettu toiminnallisuus saattaa olla hyödyllinen ja jopa riittävä käyttöösi, tämän asetuksen käyttö on täysin omalla vastuullasi, eikä sille tarjota tukea.
* Vanha: Windows-konsolin UI Automation -rajapinta poistetaan kokonaan käytöstä.
Vanhaa varavaihtoehtoa käytetään aina myös tilanteissa, joissa UI Automation -rajapinta tarjoaisi ylivertaisen käyttökokemuksen.
Siksi tämän vaihtoehdon valitsemista ei suositella, ellet tiedä mitä olet tekemässä.

##### Käytä UIA:ta Microsoft Edgessä ja muissa Chromium-pohjaisissa selaimissa, kun käytettävissä {#ChromiumUIA}

Tämän asetuksen avulla voit määrittää, milloin UIA:ta käytetään (mikäli se on käytettävissä) Chromium-pohjaisissa selaimissa, kuten Microsoft Edgessä.
Chromium-pohjaisten selainten UIA-tuki on alkuvaiheessa, eikä välttämättä tarjoa samantasoista käyttökokemusta kuin IA2.
Yhdistelmäruudussa on seuraavat vaihtoehdot:

* Oletus (vain tarvittaessa): NVDA:n oletusasetus, joka on tällä hetkellä "Vain tarvittaessa". Tämä voi muuttua tulevaisuudessa tekniikan kehittyessä.
* Vain tarvittaessa: Kun NVDA ei pysty toimimaan selainprosessin sisällä IA2:n käyttämiseksi ja kun UIA on käytettävissä, NVDA siirtyy käyttämään UIA:ta.
* Kyllä: Jos UIA on käytettävissä selaimessa, NVDA käyttää sitä.
* Ei: Älä käytä UIA:ta, vaikka NVDA ei pysty toimimaan selainprosessin sisällä. Tästä voi olla hyötyä kehittäjille, jotka selvittävät IA2:n ongelmia ja haluavat varmistaa, ettei NVDA ala käyttää UIA:ta.

##### Merkinnät {#Annotations}

Näillä asetuksilla otetaan käyttöön ominaisuudet, jotka lisäävät kokeellisen tuen ARIA-merkinnöille.
Jotkin näistä ominaisuuksista voivat olla keskeneräisiä.

<!-- KC:beginInclude -->
Ilmoita järjestelmäkohdistimen kohdalla olevan merkinnän kaikkien tietojen yhteenveto painamalla NVDA+D.
<!-- KC:endInclude -->

Seuraavat vaihtoehdot ovat käytettävissä:

* Ilmoita rakenteellisten merkintöjen lisätiedoista: ilmoittaa, mikäli tekstillä tai säätimellä on lisätietoja.
* Puhu aina ARIA-kuvaukset:
  Kuvaus puhutaan, kun `accDescription`-attribuutin lähteenä on aria-description.
  Tästä on hyötyä verkkosivuilla olevissa merkinnöissä.
  Huom:
  * `accDescription`-attribuutille on monia lähteitä, joista useilla on sekava tai epäluotettava semantiikka.
    Historiallisesti apuvälineteknologia ei ole kyennyt erottamaan `accDescription`-attribuutin lähteitä toisistaan. Tyypillisesti sitä ei puhuttu sekalaisen semantiikan vuoksi.
  * Tämän asetuksen kehitys on vasta alkuvaiheessa. Se perustuu sellaisiin selaimen ominaisuuksiin, joita ei ole vielä laajasti saatavilla.
  * Odotetaan toimivan Chromium 92.0.4479.0:n ja sitä uudempien kanssa.

##### Ilmaise aktiiviset alueet {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Käytössä), Ei käytössä, Käytössä|
|Oletus |Käytössä|

Tällä asetuksella voidaan valita, näyttääkö NVDA tietyt verkkosivulla tapahtuvat dynaamiset muutokset pistenäytöllä.
Asetuksen käytöstä poistaminen vastaa NVDA:n toiminnallisuutta versiossa 2023.1 ja sitä vanhemmissa, joissa tällaisen sisällön muutokset ilmoitettiin vain puheella.

##### Puhu salasanat kaikissa laajennetuissa päätteissä {#AdvancedSettingsWinConsoleSpeakPasswords}

Tämä asetus säätää, puhutaanko merkit [Puhu kirjoitetut merkit-](#KeyboardSettingsSpeakTypedCharacters) tai [Puhu kirjoitetut sanat](#KeyboardSettingsSpeakTypedWords) -asetusta käytettäessä tilanteissa, joissa ruutu ei päivity (kuten salasanaa syötettäessä) Windows-konsolissa UI automation -tuen ollessa käytössä ja Mintty:ssä.
Tietoturvasyistä tämä asetus tulisi pitää poissa käytöstä.
Voit kuitenkin halutessasi ottaa sen käyttöön, mikäli sinulla on konsoleissa suorituskykyongelmia tai epävakautta kirjoitettujen merkkien ja/tai sanojen puhumisessa, tai työskentelet luotetuissa ympäristöissä ja haluat, että salasanat puhutaan.

##### Käytä laajennettua kirjoitettujen merkkien tukea vanhassa Windows-konsolissa, kun käytettävissä {#AdvancedSettingsKeyboardSupportInLegacy}

Tämä asetus ottaa käyttöön vaihtoehtoisen menetelmän kirjoitettujen merkkien tunnistamiseen vanhoissa Windows-konsoleissa.
Vaikka se parantaa suorituskykyä ja estää konsolitulosteen tavaamista, se ei ehkä ole yhteensopiva joidenkin pääteohjelmien kanssa.
Tämä ominaisuus on käytettävissä ja käytössä oletusarvoisesti Windows 10:n versiossa 1607 ja sitä uudemmissa, kun UI Automation -rajapinta ei ole käytettävissä tai se on poistettu käytöstä.
Varoitus: Kun tämä asetus on käytössä, ruudulla näkymättömät kirjoitetut merkit, kuten salasanat, puhutaan.
Epäluotettavissa ympäristöissä voit salasanoja kirjoittaessasi poistaa väliaikaisesti käytöstä [Puhu kirjoitetut merkit-](#KeyboardSettingsSpeakTypedCharacters) ja [Puhu kirjoitetut sanat](#KeyboardSettingsSpeakTypedWords) -asetukset.

##### Muutosten havaitsemismenetelmä {#DiffAlgo}

Tämä asetus määrittää, miten NVDA havaitsee uuden puhuttavan tekstin päätteissä.
Tässä yhdistelmäruudussa on kolme vaihtoehtoa:

* Automaattinen: Tämä saa NVDA:n suosimaan Diff Match Patchia useimmissa tilanteissa, mutta palaa takaisin Difflibiin ongelmallisissa sovelluksissa, kuten Windows-konsolin ja Mintty:n vanhemmissa versioissa.
* Diff Match Patch: Tätä asetusta käytettäessä NVDA laskee päätteen tekstimuutokset merkeittäin, jopa sellaisissa tilanteissa, joissa sitä ei suositella.
Tämä saattaa parantaa suorituskykyä, kun konsoliin kirjoitetaan suuria tekstimääriä, sekä mahdollistaa rivien keskellä tehtyjen muutosten tarkemman ilmoittamisen.
Joissakin sovelluksissa uuden tekstin lukeminen voi kuitenkin olla nykivää tai epäjohdonmukaista.
* Difflib: Tätä asetusta käytettäessä NVDA laskee päätteen tekstimuutokset riveittäin, jopa sellaisissa tilanteissa, joissa sitä ei suositella.
Tämä vastaa NVDA:n toiminnallisuutta versiossa 2020.4 ja sitä vanhemmissa.
Tämä asetus saattaa vakauttaa saapuvan tekstin lukemista joissakin sovelluksissa.
Kohdistimen jälkeinen teksti kuitenkin luetaan päätteissä, kun rivin keskelle lisätään tai siitä poistetaan merkki.

##### Uuden tekstin puhumismenetelmä Windows-päätteessä {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Muutosten havaitseminen), Muutosten havaitseminen, UIA-ilmoitukset|
|Oletus |Muutosten havaitseminen|

Tämä asetus valitsee, miten NVDA määrittää "uuden" tekstin (ja näin ollen sen, mitä puhutaan "Puhu dynaamisen sisällön muutokset" -asetuksen ollessa käytössä) Windows-päätteessä sekä sen WPF-säätimessä, jota käytetään Visual Studio 2022:ssa.
Asetus ei vaikuta Windows-konsoliin (`conhost.exe`).
Uuden tekstin puhumismenetelmä Windows-päätteessä -yhdistelmäruudussa on kolme vaihtoehtoa:

* Oletus: Tämä asetus vastaa tällä hetkellä "muutosten havaitsemista", mutta sen odotetaan muuttuvan, kun UIA-ilmoitusten tukea kehitetään edelleen.
* Muutosten havaitseminen: Tämä asetus käyttää valittua muutostenhavaitsemismenetelmää muutosten laskemiseen joka kerta, kun päätteeseen ilmestyy uutta tekstiä.
Tämä toimii samoin kuin NVDA 2022.4:ssä ja sitä vanhemmissa versioissa.
* UIA-ilmoitukset: Tämä asetus siirtää vastuun puhuttavan tekstin määrittämisestä Windows-päätteelle itselleen, mikä tarkoittaa, että NVDA:n ei enää tarvitse määrittää, mikä ruudulla oleva teksti on "uutta".
Tämän pitäisi parantaa huomattavasti Windows-päätteen suorituskykyä ja vakautta, mutta ominaisuus ei ole vielä valmis.
Erityisesti kirjoitetut merkit, joita ei näytetä ruudulla, esim. salasanat, puhutaan tämän ollessa valittuna.
Lisäksi yhtenäisiä yli 1000 merkin mittaisia tekstijaksoja ei välttämättä puhuta tarkasti.

##### Yritä perua vanhentuneiden kohdistustapahtumien puhe {#CancelExpiredFocusSpeech}

Tämä asetus ottaa käyttöön toiminnallisuuden, joka yrittää perua vanhentuneiden kohdistustapahtumien puheen.
Erityisesti nopea siirtyminen viestien välillä Gmailissa voi Chromea käytettäessä aiheuttaa NVDA:ssa vanhentuneen tiedon puhumista.
Tämä toiminnallisuus on oletusarvoisesti käytössä NVDA 2021.1:stä alkaen.

##### Kohdistimen siirtämisen aikakatkaisu (ms) {#AdvancedSettingsCaretMoveTimeout}

Tällä asetuksella voidaan määrittää, montako millisekuntia NVDA odottaa kohdistimen (lisäyskohdan) siirtämistä muokattavissa tekstisäätimissä.
Mikäli NVDA näyttää seuraavan kohdistinta virheellisesti, esim. on aina yhden merkin jäljessä tai toistaa rivejä, Tämän arvon suurentamisesta voi olla apua.

##### Ilmoita läpinäkyvien värien arvot {#ReportTransparentColors}

Tämä ottaa käyttöön värien läpinäkyvyyden ilmaisemisen, josta on hyötyä lisäosien/sovellusmoduulien kehittäjille tiedon keräämisessä kolmannen osapuolen sovellusten käyttökokemuksen parantamiseksi.
Jotkin GDI-sovellukset korostavat tekstiä taustavärillä, jonka NVDA yrittää ilmaista.
Joissakin tilanteissa tekstin tausta voi olla täysin läpinäkyvä, ja teksti on kerrostettu johonkin muuhun graafisen käyttöliittymän elementtiin.
Useiden historiallisesti suosittujen käyttöliittymärajapintojen avulla teksti voidaan esittää läpinäkyvällä taustalla, mutta visuaalisesti taustaväri on tarkka.

##### Käytä WASAPIa äänentoistoon {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Vaihtoehdot |Oletus (Käytössä), Ei käytössä, Käytössä|
|Oletus |Käytössä|

Tämä asetus mahdollistaa äänentoiston Windowsin äänentoistorajapinnan (WASAPI) kautta.
WASAPI on nykyaikaisempi äänikehys, joka saattaa parantaa NVDA:n ääniulostulon reagointia, suorituskykyä ja vakautta sekä puheen että äänien toiston osalta.
Kun asetusta on muutettu, NVDA on käynnistettävä uudelleen, jotta muutos tulee voimaan.
WASAPIn käytöstä poistaminen poistaa käytöstä seuraavat asetukset:

* [NVDA-äänien voimakkuus mukautuu puheäänen voimakkuuteen](#SoundVolumeFollowsVoice)
* [NVDA-äänien voimakkuus](#SoundVolume)

##### Virheenkorjauslokin kategoriat {#AdvancedSettingsDebugLoggingCategories}

Tämän luettelon valintaruuduilla voidaan ottaa käyttöön tiettyjen kategorioiden virheenkorjausilmoituksia NVDA:n lokissa.
Näiden ilmoitusten tallentamisesta lokiin voi olla seurauksena suorituskyvyn huonontumista sekä suurikokoisia lokitiedostoja.
Ota jokin näistä käyttöön vain, jos NVDA:n kehittäjä on neuvonut tekemään niin, esim. sen selvittämiseksi, miksi pistenäytön ajuri ei toimi oikein.

##### Ilmaise lokiin tallentuvat virheet toistamalla ääni {#PlayErrorSound}

Tämän asetuksen avulla voit määrittää, toistaako NVDA äänen, jos lokiin tallentuu virhe.
Jos valitset "Vain testiversioissa (oletus) virheääniä toistetaan vain, mikäli käytössä on NVDA:n testiversio (alfa, beeta tai lähdekoodista suoritettava).
Jos valitset Kyllä, virheäänet otetaan käyttöön nykyisestä NVDA-versiostasi riippumatta.

##### Tekstikappalenavigoinnin sääntölauseke {#TextParagraphRegexEdit}

Tämä kenttä mahdollistaa sääntölausekkeen mukauttamisen tekstikappaleiden tunnistamiseksi selaustilassa.
[Tekstikappaleiden navigointikomento](#TextNavigationCommand) etsii tämän sääntölausekkeen mukaisia kappaleita.

### Sekalaiset asetukset {#MiscSettings}

[Asetukset](#NVDASettings)-valintaikkunan lisäksi NVDA-valikosta löytyvä Asetukset-alivalikko sisältää myös useita muita kohteita, jotka on kuvailtu alla.

#### Puhesanastot {#SpeechDictionaries}

Asetukset-valikosta löytyvä Puhesanastot-valikko sisältää valintaikkunoita, joista voidaan muuttaa tapaa, jolla NVDA lausuu tietyt sanat tai ilmaisut.
Puhesanastoja on kolmea eri tyyppiä.
Ne ovat:

* Oletus: tämän sanaston säännöt vaikuttavat kaikkeen NVDA:n puhumaan tekstiin.
* Puheäänikohtainen: sanasto, jonka säännöt vaikuttavat käytössä olevan syntetisaattorin puheääneen.
* Tilapäinen: tämän sanaston säännöt vaikuttavat kaikkeen NVDA:n puhumaan tekstiin, mutta vain nykyisessä istunnossa. Säännöt ovat tilapäisiä ja ne menetetään, jos NVDA käynnistetään uudelleen.

Mikäli jokin näistä sanastovalintaikkunoista halutaan avata mistä tahansa, niille on määritettävä omat näppäinkomennot [Näppäinkomennot-valintaikkunaa käyttäen](#InputGestures).

Kaikissa sanastovalintaikkunoissa on luettelo säännöistä, joita käytetään puhutun tekstin käsittelyyn.
Valintaikkunoissa on myös Lisää-, Muokkaa-, Poista- ja Poista kaikki -painikkeet.

Sanastoon lisätään uusi sääntö painamalla Lisää-painiketta, täyttämällä esiin tulevan valintaikkunan kentät ja painamalla OK.
Lisätty sääntö näkyy tämän jälkeen sääntöluettelossa.
Tehtyjen muutosten tallentaminen varmistetaan poistumalla sanastovalintaikkunasta painamalla OK.

Puhesanastosääntöjen avulla merkkijono voidaan muuttaa joksikin muuksi.
Yksinkertaisena esimerkkinä tästä voisi olla, että NVDA saadaan sanomaan "sammakko" jokaisen lintu-sanan kohdalla.
Helpointa tämä on tehdä kirjoittamalla säännönlisäysvalintaikkunassa Korvattava teksti -kenttään lintu ja Korvaava teksti -kenttään sammakko.
Kommentti-kenttään kirjoitetaan säännön kuvaus (esim. muuttaa linnun sammakoksi).

Puhesanastoja on mahdollista käyttää paljon muuhunkin kuin yksinkertaiseen sanojen korvaamiseen.
Säännönlisäysvalintaikkunassa on myös valintaruutu, jolla voidaan määrittää, onko isoilla ja pienillä kirjaimilla merkitystä säännön toiminnan kannalta.
Oletusarvoisesti kirjainkokoa ei huomioida.

Viimeisenä on joukko valintapainikkeita, joiden avulla on mahdollista määrittää, täsmääkö korvattava merkkijono kaikkialla, vain kokonaisena sanana vai käsitelläänkö sitä sääntölausekkeena.
Korvattavan tekstin määrittäminen kokonaiseksi sanaksi tarkoittaa, että se korvataan vain, jos se ei esiinny pidemmän sanan osana.
Tämä ehto täyttyy, jos heti ennen sanaa ja sen jälkeen olevat merkit ovat jotain muita kuin kirjaimia, numeroita tai alaviivoja, tai jos merkkejä ei ole ollenkaan.
Eli käyttääksemme aiempaa esimerkkiä lintu-sanan korvaamisesta sanalla sammakko, jos siitä tehtäisiin koko sanan korvaus, se ei täsmäisi "lintuja"- tai "sinilintu"-sanoihin.

Sääntölauseke on erikoismerkkejä sisältävä merkkiyhdistelmä, jonka avulla voidaan täsmätä useampaan kuin yhteen merkkiin kerrallaan, pelkkiin numeroihin tai pelkkiin kirjaimiin.
Sääntölausekkeita ei käsitellä tässä käyttöoppaassa.
Voit tutustua aiheeseen [Pythonin sääntölausekkeiden oppaassa](https://docs.python.org/3.11/howto/regex.html).

#### Välimerkkien ja symbolien puhuminen {#SymbolPronunciation}

Tässä valintaikkunassa voit muuttaa välimerkkien ja muiden symbolien lukutapaa sekä tasoa, jolla ne puhutaan.

Kieli, jonka symbolien puhumista muokataan, näytetään valintaikkunan otsikossa.
Huom: Tässä noudatetaan [Asetukset](#NVDASettings)-valintaikkunan [Puhe-kategorian](#SpeechSettings) "Käytä puheäänen kieltä merkkejä ja symboleita käsiteltäessä" -asetusta, ts. kun asetus on käytössä, puheäänen kieltä käytetään NVDA:n käyttämän kielen asemesta.

Symbolia muutetaan valitsemalla se Symbolit-luettelosta.
Symboleita voidaan suodattaa kirjoittamalla Suodata-muokkauskenttään haluttu symboli tai osa sen korvaavasta tekstistä.

* Korvaava teksti -muokkauskentässä voidaan muuttaa tekstiä, joka puhutaan kyseisen symbolin asemesta.
* Taso-yhdistelmäruudusta valitaan alin taso, jolla symboli puhutaan (ei mitään, jotain, useimmat tai kaikki).
Tasoksi voidaan määrittää myös merkki, jolloin symbolia ei puhuta käytössä olevasta symbolitasosta riippumatta kahta seuraavaa poikkeusta lukuun ottamatta:
  * Merkeittäin liikuttaessa.
  * Kun NVDA tavaa tekstiä, joka sisältää kyseisen symbolin.
* Välitä merkki syntetisaattorille -yhdistelmäruudusta voit määrittää, milloin itse symboli (vastakohtana sen korvaavalle tekstille) välitetään syntetisaattorille.
Tästä on hyötyä, jos symboli saa syntetisaattorin pitämään tauon tai muuttamaan äänensävyä.
Esimerkiksi pilkku saa syntetisaattorin pitämään tauon.
Vaihtoehtoja on kolme:
  * ei koskaan: Merkkiä ei koskaan välitetä syntetisaattorille.
  * aina: Merkki välitetään aina syntetisaattorille.
  * vain jos symbolitaso on alempi: Merkki välitetään syntetisaattorille vain, jos määritetty puheen symbolitaso on alempi kuin kyseiselle symbolille määritetty.
  Tätä voidaan käyttää esim. siten, että symbolin korvaava teksti puhutaan korkeammilla tasoilla ilman taukoja, mutta alemmilla tasoilla tauot kuitenkin kuuluvat.

Lisää uusia symboleita painamalla Lisää-painiketta.
Kirjoita symboli avautuvaan valintaikkunaan ja paina OK.
Muuta tämän jälkeen korvaava teksti ja taso haluamiksesi kuten muillekin symboleille.

Poista aiemmin lisätty symboli painamalla Poista-painiketta.

Kun olet valmis, tallenna muutokset painamalla OK-painiketta tai kumoa ne painamalla Peruuta.

Monimutkaisten symbolien tapauksessa Korvaava-kentässä on ehkä oltava joitakin ryhmäviittauksia täsmättävään tekstiin. Esim. koko päivämäärää vastaavan korvattavan tekstin \1, \2 ja \3 tulisi näkyä kentässä, jotta ne korvataan päivämäärän vastaavilla osilla.
Korvaava teksti -kentässä olevat normaalit kenoviivat tulisi siis kahdentaa (esim. kirjoita "a\\b" saadaksesi aikaan korvauksen "a\b".

#### Näppäinkomennot {#InputGestures}

Tässä valintaikkunassa voit mukauttaa NVDA-komennoissa käytettäviä näppäinkomentoja (näppäimistön näppäimiä, pistenäytön painikkeita jne.).

Vain sellaiset komennot näytetään, jotka ovat käytettävissä valintaikkunaa avattaessa.
Jos esim. haluat mukauttaa selaustilan komentoja, sinun on avattava Näppäinkomennot-valintaikkuna selaustilassa ollessasi.

Tämän valintaikkunan puunäkymässä näytetään kaikki käytettävissä olevat NVDA-komennot omiin kategorioihinsa ryhmiteltyinä.
Voit suodattaa komentoja kirjoittamalla Suodata-muokkauskenttään komennon nimestä yhden tai useamman sanan missä tahansa järjestyksessä.
Kaikki komentoon liitetyt näppäinkomennot näytetään kyseisen komennon alapuolella.

Lisää komentoon näppäinkomento valitsemalla se luettelosta ja painamalla Lisää-painiketta.
Suorita tämän jälkeen haluamasi näppäinkomento (ts. paina näppäimistön tai pistenäytön näppäimiä).
Näppäinkomento voidaan usein tulkita useammalla kuin yhdellä tavalla.
Jos esim. painoit näppäimistön näppäimiä, saatat haluta niiden toimivan jossain tietyssä näppäinasettelussa (esim. pöytäkone tai kannettava) tai kaikissa asetteluissa.
Tällöin näkyviin tulee valikko, josta voit valita haluamasi vaihtoehdon.

Poista näppäinkomento komennosta valitsemalla se ja painamalla Poista-painiketta.

Jäljiteltävät järjestelmänäppäimistön näppäimet -kategoria sisältää NVDA-komentoja, jotka jäljittelevät järjestelmänäppäimistön näppäimiä.
Näitä näppäimiä voidaan käyttää järjestelmänäppäimistön ohjaamiseen suoraan pistenäytöltä.
Lisää jäljiteltävä näppäinkomento valitsemalla Jäljiteltävät järjestelmänäppäimistön näppäimet -kategoria ja painamalla Lisää-painiketta.
Paina sitten näppäimistöltä sitä näppäintä, jota haluat jäljitellä.
Tämän jälkeen näppäin näkyy Jäljiteltävät järjestelmänäppäimistön näppäimet -kategoriassa, ja voit määrittää sille näppäinkomennon yllä kuvatulla tavalla.

Huom:

* Jäljiteltävillä näppäimillä täytyy olla näppäinkomennot määritettyinä, jotta ne säilyvät tallennettaessa/valintaikkunaa suljettaessa.
* Näppäinkomentoa, jossa käytetään muokkausnäppäimiä, ei välttämättä voi liittää jäljiteltävään näppäinkomentoon, jossa ei muokkaus
näppäimiä ole. Kun esim. jäljiteltäväksi syötteeksi määritetään "a" ja näppäinkomennoksi Ctrl+M, saattaa siitä seurata,
että sovellus vastaanottaa näppäinyhdistelmän Ctrl+A.

Tehdyt muutokset tallennetaan painamalla OK-painiketta tai hylätään painamalla Peruuta.

### Asetusten tallentaminen ja palauttaminen {#SavingAndReloading}

Asetukset tallennetaan automaattisesti, kun NVDA suljetaan.
Tätä asetusta voidaan kuitenkin myös muuttaa Yleiset asetukset -valintaikkunassa, joka löytyy Asetukset-valikosta.
Asetukset on mahdollista tallentaa manuaalisesti milloin tahansa valitsemalla NVDA-valikosta Tallenna asetukset -vaihtoehto.

Mikäli asetuksia muutettaessa sattuu erehdys, tallennetut asetukset voidaan palauttaa valitsemalla NVDA-valikosta Palauta tallennetut asetukset.
Asetukset voidaan lisäksi palauttaa alkuperäisiin oletusarvoihin valitsemalla vaihtoehto Palauta oletusasetukset, joka myös löytyy NVDA-valikosta.

Seuraavista näppäinkomennoista voi myös olla hyötyä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento pöytäkoneissa |Näppäinkomento kannettavissa |Kuvaus|
|---|---|---|---|
|Tallenna asetukset |NVDA+Ctrl+C |NVDA+Ctrl+C |Tallentaa nykyiset asetukset, jotta ne eivät häviä, kun NVDA suljetaan|
|Palauta asetukset |NVDA+Ctrl+R |NVDA+Ctrl+R |Palauttaa kerran painettaessa viimeksi tallennetut asetukset. Kolmesti painaminen palauttaa oletusasetukset.|

<!-- KC:endInclude -->

### Asetusprofiilit {#ConfigurationProfiles}

Saatat joskus tarvita eri tilanteissa eri asetuksia.
Esimerkiksi siten, että sisennysten lukeminen on käytössä tekstiä muokatessasi tai että fonttimääreiden lukeminen on käytössä asiakirjaa oikolukiessasi.
Tämä on mahdollista NVDA:n asetusprofiileja käyttäen.

Asetusprofiili sisältää vain ne asetukset, joita profiilia muokattaessa muutetaan.
Useimpien asetusten muuttaminen on profiileissa mahdollista, paitsi [Asetukset](#NVDASettings)-valintaikkunan Yleiset-kategoriassa olevien, joita käytetään kaikkialla.

Asetusprofiilit voidaan ottaa käyttöön manuaalisesti joko valintaikkunasta tai itse määritetyillä näppäinkomennoilla.
Ne voidaan ottaa käyttöön myös automaattisesti käynnistimien avulla, kuten tiettyyn sovellukseen siirryttäessä.

#### Perushallinta {#ProfilesBasicManagement}

Asetusprofiileja hallitaan valitsemalla NVDA-valikosta "Asetusprofiilit..."-vaihtoehto.
Voit käyttää myös näppäinkomentoa:
<!-- KC:beginInclude -->

* NVDA+Ctrl+P: Näyttää Asetusprofiilit-valintaikkunan.

<!-- KC:endInclude -->

Tämän valintaikkunan ensimmäinen säädin on profiililuettelo, josta voit valita jonkin käytettävissä olevista profiileista.
Tällä hetkellä muokkaamasi profiili on valittuna valintaikkunaa avatessasi.
Käytössä olevista profiileista näytetään myös lisätietoa, joka ilmaisee, ovatko ne manuaalisesti tai käynnistimellä käyttöönotettavia ja/tai muokattavia.

Uudelleennimeä tai poista profiili painamalla Nimeä uudelleen- tai Poista-painikkeita.

Sulje valintaikkuna painamalla Sulje-painiketta.

#### Profiilin luominen {#ProfilesCreating}

Luo profiili painamalla Uusi-painiketta.

Uusi profiili -valintaikkunassa voit antaa profiilille nimen.
Voit myös valita, miten profiilia käytetään.
Mikäli haluat käyttää profiilia vain manuaalisesti, valitse Ota käyttöön manuaalisesti, joka on oletusarvoisesti valittuna.
Muussa tapauksessa valitse käynnistin, joka ottaa profiilin automaattisesti käyttöön.
Jos et ole antanut profiilille nimeä, käynnistimen valitseminen täyttää sen automaattisesti.
Katso [alta](#ConfigProfileTriggers) lisätietoja käynnistimistä .

Profiili luodaan ja valintaikkuna suljetaan painamalla OK, jonka jälkeen voit muokata kyseistä profiilia.

#### Manuaalinen käyttöönotto {#ConfigProfileManual}

Voit ottaa profiilin käyttöön manuaalisesti valitsemalla sen ja painamalla Ota käyttöön manuaalisesti -painiketta.
Muita profiileja voidaan edelleen ottaa käyttöön käynnistimien avulla, mutta manuaalisesti käyttöönotetun profiilin asetukset ovat etusijalla.
Jos esim. linkkien lukeminen on käytössä nykyiselle sovellukselle käynnistimellä käyttöönotettavassa profiilissa mutta poissa käytöstä manuaalisesti käyttöönotettavassa, linkkejä ei tällöin lueta.
Jos kuitenkin olet vaihtanut puheääntä käynnistimellä käyttöönotettavassa profiilissa mutta et manuaalisesti käyttöönotetussa, tällöin käytetään käynnistimellä käyttöönotettavan profiilin puheääntä.
Kaikki muokkaamasi asetukset tallennetaan manuaalisesti käyttöönotettuun profiiliin.
Poista manuaalisesti käyttöönotettu profiili käytöstä valitsemalla se Asetusprofiilit-valintaikkunasta ja painamalla Poista käytöstä manuaalisesti -painiketta.

#### ´Käynnistimet {#ConfigProfileTriggers}

Voit vaihtaa käynnistimillä käyttöönotettavia profiileja painamalla Asetusprofiilit-valintaikkunassa Käynnistimet-painiketta.

Käynnistimet-luettelo näyttää käytettävissä olevat käynnistimet, joita ovat:

* Nykyinen sovellus: Käytetään siirtyessäsi nykyiseen sovellukseen.
* Jatkuva luku: Käytetään jatkuva luku -komennolla luettaessa.

Vaihda käynnistimellä automaattisesti käyttöönotettavaa profiilia valitsemalla ensin käynnistin ja sitten Profiili-yhdistelmäruudusta haluamasi profiili.
Mikäli et halua käyttää profiilia, valitse (normaalit asetukset) -vaihtoehto.

Palaa Asetusprofiilit-valintaikkunaan painamalla Sulje.

#### Profiilin muokkaaminen {#ConfigProfileEditing}

Jos olet ottanut profiilin käyttöön manuaalisesti, kaikki muuttamasi asetukset tallennetaan siihen.
Muussa tapauksessa asetukset tallennetaan viimeisimpään käynnistimellä käyttöönotettuun profiiliin.
Jos esim. olet liittänyt profiilin Muistio-sovellukseen, kaikki muuttamasi asetukset tallennetaan siihen Muistion ollessa aktiivisena.
Lopuksi, mikäli manuaalisesti tai käynnistimellä käyttöönotettavaa profiilia ei ole, asetukset tallennetaan normaaleihin asetuksiisi.

Muokkaa Jatkuva luku -toimintoon liitettyä profiilia [ottamalla se käyttöön manuaalisesti.](#ConfigProfileManual)

#### Käynnistimien tilapäinen käytöstä poistaminen {#ConfigProfileDisablingTriggers}

Kaikkien käynnistimien käytöstä poistaminen voi joskus olla tarpeen.
Saatat esim. haluta muokata manuaalisesti käyttöönotettua profiilia tai normaaleja asetuksiasi ilman, että käynnistimillä käyttöönotettavat profiilit häiritsevät.
Voit tehdä tämän valitsemalla Asetusprofiilit-valintaikkunassa Poista kaikki käynnistimet käytöstä tilapäisesti -valintaruudun.

Poista käynnistimet käytöstä tai ota ne uudelleen käyttöön mistä tahansa liittämällä asetukseen oma näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

#### Profiilin käyttöönotto näppäinkomentoja käyttäen {#ConfigProfileGestures}

Voit liittää jokaiseen lisäämääsi profiiliin sen käyttöön ottamiseksi yhden tai useamman näppäinkomennon.
Asetusprofiileilla ei oletusarvoisesti ole näppäinkomentoja.
Lisää näppäinkomennot [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.
Kullakin profiililla on oma kohtansa Asetusprofiilit-kategoriassa.
Kun uudelleennimeät profiilin, kaikki aiemmin lisäämäsi näppäinkomennot ovat edelleen käytettävissä.
Profiilin poistaminen poistaa automaattisesti myös siihen liitetyt näppäinkomennot.

### Asetustiedostojen sijainti {#LocationOfConfigurationFiles}

NVDA:n massamuistiversio tallentaa kaikki asetukset ja lisäosat hakemistossaan olevaan userConfig-nimiseen alihakemistoon.

Asennettu NVDA:n versio tallentaa asetukset ja lisäosat erityiseen Windowsin käyttäjäprofiilissasi olevaan NVDA-hakemistoon.
Tämä tarkoittaa, että jokaisella järjestelmän käyttäjällä voi olla omat NVDA-asetukset.
Voit avata asetushakemistosi mistä tahansa lisäämällä oman näppäinkomennon [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.
Asennetussa NVDA:ssa pääset asetushakemistoon lisäksi valitsemalla Käynnistä-valikosta Ohjelmat -> NVDA -> Selaa käyttäjän asetushakemistoa.

Sisäänkirjautumisen aikana ja käyttäjätilien valvonnan ruuduissa käytettävät asetukset tallennetaan NVDA:n asennushakemistossa olevaan systemConfig-hakemistoon.
Näihin ei tulisi yleensä koskea.
Sisäänkirjautumisen aikana ja käyttäjätilien valvonnan ruuduissa käytettävät asetukset voit määrittää muuttamalla ensin asetukset haluamiksesi ollessasi kirjautuneena Windowsiin, tallentamalla asetukset ja painamalla sitten [Asetukset](#NVDASettings)-valintaikkunan Yleiset-kategoriassa olevaa "Käytä tallennettuja asetuksia sisäänkirjautumisen aikana ja suojatuissa ruuduissa" -painiketta.

## Lisäosat ja lisäosakauppa {#AddonsManager}

Lisäosat ovat ohjelmistopaketteja, jotka tarjoavat uusia tai muokattuja toiminnallisuuksia NVDA:lle.
Niitä kehittävät NVDA-yhteisö ja ulkoiset organisaatiot, kuten kaupalliset toimittajat.
Lisäosat voivat tehdä seuraavia asioita:

* Lisätä tai parantaa tiettyjen sovellusten tukea.
* Lisätä tuen pistenäytöille tai puhesyntetisaattoreille.
* Lisätä tai muuttaa NVDA:n ominaisuuksia.

NVDA:n lisäosakauppa mahdollistaa lisäosapakettien selaamisen ja hallinnan.
Kaikki lisäosat, jotka ovat saatavilla lisäosakaupassa, voidaan ladata ilmaiseksi.
Jotkut niistä saattavat kuitenkin vaatia lisenssin tai lisäohjelmiston ostamista ennen niiden käyttöä.
Tällaisia ovat esim. kaupalliset puhesyntetisaattorit.
Jos asennat maksullisia osia sisältävän lisäosan, mutta muutat mielesi sen käytön suhteen, se voidaan helposti poistaa.

Lisäosakauppaan pääsee NVDA-valikon Työkalut-alivalikosta.
Sen voi myös avata mistä tahansa määrittämällä sille oman näppäinkomennon [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

### Lisäosien selaaminen {#AddonStoreBrowsing}

Lisäosakauppa näyttää avautuessaan lisäosien luettelon.
Mikäli et ole aiemmin asentanut lisäosia, lisäosakauppa näyttää luettelon asennettavissa olevista lisäosista.
Jos lisäosia on asennettuna, luettelo näyttää tällä hetkellä asennettuina olevat lisäosat.

Lisäosan tiedot näytetään, kun sen kohdalle siirrytään nuolinäppäimillä ylös ja alas.
Lisäosilla on niihin liittyviä toimintoja, kuten asenna, ohje, poista käytöstä ja poista, joihin pääsee käsiksi [toimintovalikosta](#AddonStoreActions).
Käytettävissä olevat toiminnot muuttuvat sen mukaan, onko lisäosa asennettu vai ei ja onko se käytössä vai poistettu käytöstä.

#### Lisäosaluettelon näkymät {#AddonStoreFilterStatus}

Asennetuille, päivitettäville ja saatavilla oleville sekä yhteensopimattomille lisäosille on eri näkymät.
Voit vaihtaa näkymää painamalla `Ctrl+Sarkain`, joka vaihtaa lisäosaluettelon aktiivista välilehteä.
Voit myös siirtyä näkymäluetteloon painamalla `Sarkain`-näppäintä ja liikkua näkymien välillä painamalla `Nuoli vasemmalle`- ja `Nuoli oikealle` -näppäimiä.

#### Suodatus käytössä olevien tai käytöstä poistettujen lisäosien perusteella {#AddonStoreFilterEnabled}

Normaalisti asennettu lisäosa on "käytössä", mikä tarkoittaa, että se toimii ja on käytettävissä NVDA:ssa.
Joidenkin asennettujen lisäosien tilana saattaa kuitenkin olla "ei käytössä".
Tämä tarkoittaa, ettei niitä käytetä eivätkä niiden toiminnot ole käytettävissä nykyisen NVDA-istunnon aikana.
Olet saattanut poistaa lisäosan käytöstä, mikäli se aiheutti ristiriitoja toisen lisäosan tai tietyn sovelluksen kanssa.
NVDA saattaa myös poistaa tietyt lisäosat käytöstä, jos ne havaitaan yhteensopimattomiksi NVDA:n päivityksen yhteydessä, mutta tästä varoitetaan etukäteen.
Lisäosat voidaan myös poistaa käytöstä, jos et tarvitse niitä pitkään aikaan, mutta et kuitenkaan halua poistaa niitä, koska odotat tarvitsevasi niitä uudelleen tulevaisuudessa.

Asennettujen ja yhteensopimattomien lisäosien luetteloita voidaan suodattaa niiden "käytössä" ja "ei käytössä" -tilan perusteella.
Oletusarvoisesti näytetään sekä käytössä olevat että käytöstä poistetut lisäosat.

#### Yhteensopimattomien lisäosien näyttäminen {#AddonStoreFilterIncompatible}

Saatavilla olevia ja päivitettäviä lisäosia voidaan suodattaa sisältämään asennettavat [yhteensopimattomat lisäosat](#incompatibleAddonsManager).

#### Lisäosien suodattaminen kanavan perusteella {#AddonStoreFilterChannel}

Lisäosia voidaan jakaa jopa neljän eri kanavan kautta:

* Vakaa: Kehittäjä on julkaissut tämän testatun lisäosan NVDA:n vakaassa versiossa käytettäväksi.
* Beeta: Tämä lisäosa saattaa tarvita lisätestausta, mutta se on julkaistu käyttäjäpalautteen saamiseksi.
Suositellaan varhaisille käyttäjille.
* Kehitys: Tätä kanavaa suositellaan lisäosakehittäjille julkaisemattomien rajapintamuutosten testaamiseen.
NVDA:n alfatestaajien on ehkä käytettävä lisäosiensa kehitysversioita.
* Ulkoinen: Lisäosat, jotka on asennettu ulkoisista lähteistä, lisäosakaupan ulkopuolelta.

Saat luettelon johonkin tiettyyn kanavaan kuuluvista lisäosista muuttamalla "Kanava"-suodattimen valintaa.

#### Lisäosien etsiminen {#AddonStoreFilterSearch}

Voit etsiä lisäosia käyttämällä "Etsi"-tekstikenttää.
Pääset siihen painamalla lisäosaluettelossa `Vaihto+Sarkain`.
Kirjoita avainsana tai pari etsimästäsi lisäosasta ja siirry sitten lisäosaluetteloon painamalla `Sarkain`-näppäintä.
Lisäosat näytetään, jos etsittävä teksti löytyy lisäosan tunnuksesta, näyttönimestä, julkaisijasta, tekijästä tai kuvauksesta.

### Lisäosien toiminnot {#AddonStoreActions}

Lisäosilla on niihin liittyviä toimintoja, kuten asenna, ohje, poista käytöstä ja poista.
Saat toimintovalikon näkyviin painamalla `Sovellus`- tai `Enter`-näppäintä, napsauttamalla hiiren oikealla painikkeella tai kaksoisnapsauttamalla lisäosaa.
Tämä valikko voidaan avata myös Valitun lisäosan tietojen kohdassa olevalla Toiminnot-painikkeella.

#### Lisäosien asentaminen {#AddonStoreInstalling}

Pelkästään se, että lisäosa on saatavilla NVDA:n Lisäosakaupassa, ei tarkoita, että se olisi hyväksytty tai tarkastettu NV Accessin tai minkään muun tahon toimesta.
On erittäin tärkeää, että lisäosia asennetaan vain luotettavista lähteistä.
Lisäosien toiminnallisuus on NVDA:ssa rajoittamatonta.
Tämä voi ainakin teoriassa tarkoittaa pääsyä henkilökohtaisiin tietoihisi tai jopa koko järjestelmään.

Voit asentaa ja päivittää lisäosia [selaamalla saatavilla olevia lisäosia](#AddonStoreBrowsing).
Valitse lisäosa Saatavilla olevat lisäosat- tai Päivitettävät lisäosat -välilehdeltä.
Käytä sitten päivitä-, asenna- tai korvaa-toimintoa aloittaaksesi asennuksen.

Voit myös asentaa useita lisäosia kerralla.
Tämä tehdään valitsemalla useita lisäosia saatavilla olevien lisäosien välilehdellä, avaamalla valinnan pikavalikko ja valitsemalla sitten "Asenna valitut lisäosat" -toiminto.

Jos haluat asentaa lisäosan, jonka olet hankkinut lisäosakaupan ulkopuolelta, paina "Asenna ulkoisesta lähteestä" -painiketta.
Tämä mahdollistaa lisäosapaketin (`.nvda-addon`-tiedosto) etsimisen tietokoneeltasi tai verkosta.
Asennus käynnistyy, kun avaat lisäosapaketin.

Jos NVDA on asennettu ja käynnissä, voit myös aloittaa asennuksen avaamalla lisäosatiedoston suoraan selaimesta tai resurssienhallinnasta.

Kun lisäosa asennetaan ulkoisesta lähteestä, NVDA pyytää vahvistamaan asennuksen.
Kun asennus on suoritettu, NVDA on käynnistettävä uudelleen, jotta lisäosa alkaa toimia, tai voit lykätä uudelleenkäynnistystä, mikäli sinulla on muita lisäosia asennettavana tai päivitettävänä.

#### Lisäosien poistaminen {#AddonStoreRemoving}

Poista lisäosa valitsemalla se luettelosta ja käyttämällä Poista-toimintoa.
NVDA pyytää vahvistamaan poiston.
Samoin kuin asennuksen yhteydessä, NVDA on käynnistettävä uudelleen, jotta lisäosa poistetaan kokonaan.
Siihen asti lisäosan tilana näkyy luettelossa "Odottaa poistoa".
Samoin kuin asennuksen yhteydessä, voit myös poistaa useita lisäosia kerralla.

#### Lisäosien käytöstä poistaminen ja käyttöön ottaminen {#AddonStoreDisablingEnabling}

Poista lisäosa käytöstä "Poista käytöstä" -toiminnolla.
Ota aiemmin käytöstä poistettu lisäosa uudelleen käyttöön "Ota käyttöön" -toiminnolla.
Voit poistaa lisäosan käytöstä, mikäli sen tila ilmaisee sen olevan "Käytössä", tai ottaa sen käyttöön, mikäli tilana on "Ei käytössä".
Jokainen "Ota käyttöön"- ja "Poista käytöstä" -toiminnon käyttökerta muuttaa lisäosan tilaa, joka ilmaisee, mitä tapahtuu, kun NVDA käynnistetään uudelleen.
Jos lisäosan tilana oli aiemmin "Ei käytössä", tilaksi muuttuu "Käytössä uudelleenkäynnistyksen jälkeen".
Jos tilana oli "Käytössä", tilaksi muuttuu "Ei käytössä uudelleenkäynnistyksen jälkeen".
Aivan kuten lisäosia asennettaessa tai poistettaessa, NVDA on käynnistettävä uudelleen, jotta muutokset tulevat voimaan.
Voit myös ottaa käyttöön tai poistaa käytöstä useita lisäosia kerralla valitsemalla useita lisäosia saatavilla olevien lisäosien välilehdeltä, avaamalla valinnan pikavalikon ja valitsemalla sitten sopivan toiminnon.

#### Lisäosien arvosteleminen ja arvostelujen lukeminen {#AddonStoreReviews}

Saatat haluta lukea muiden käyttäjien arvosteluja lisäosasta, esimerkiksi ennen sen asentamista tai kun opettelet käyttämään sitä.
On myös hyödyllistä antaa palautetta kokeilemistasi lisäosista.
Lue arvosteluja valitsemalla lisäosa ja käyttämällä "Yhteisön arvostelut" -toimintoa.
Toiminnon avaama linkki johtaa GitHub-keskustelusivulle, jossa voit lukea ja kirjoittaa lisäosan arvosteluja.
On syytä pitää mielessä, että tämä ei korvaa suoraa kommunikointia lisäosakehittäjien kanssa.
Sen sijaan tämän ominaisuuden tarkoituksena on jakaa palautetta, joka auttaa käyttäjiä päättämään, onko lisäosa heille hyödyllinen.

### Yhteensopimattomat lisäosat {#incompatibleAddonsManager}

Jotkin vanhemmat lisäosat eivät ehkä enää ole yhteensopivia käyttämäsi NVDA-version kanssa.
Mikäli käytät vanhempaa NVDA-versiota, jotkin uudemmatkaan lisäosat eivät välttämättä ole yhteensopivia.
Yhteensopimattoman lisäosan asennuksen yrittäminen aiheuttaa virheilmoituksen, jossa selitetään, miksi kyseistä lisäosaa pidetään yhteensopimattomana.

Voit ohittaa yhteensopimattomuuden vanhempien lisäosien osalta omalla vastuullasi.
Yhteensopimattomat lisäosat eivät välttämättä toimi käyttämäsi NVDA-version kanssa ja voivat aiheuttaa epävakautta tai odottamatonta toimintaa, kuten kaatuilua.
Voit ohittaa yhteensopivuuden ottaessasi lisäosan käyttöön tai asentaessasi sen.
Mikäli yhteensopimaton lisäosa aiheuttaa myöhemmin ongelmia, voit poistaa sen käytöstä tai poistaa kokonaan.

Jos sinulla on vaikeuksia NVDA:n käytössä ja olet äskettäin päivittänyt tai asentanut lisäosan, erityisesti mikäli se on yhteensopimaton, kannattaa kokeilla käyttää NVDA:ta tilapäisesti kaikki lisäosat käytöstä poistettuina.
Käynnistä NVDA uudelleen ja poista kaikki lisäosat käytöstä valitsemalla asianmukainen vaihtoehto NVDA:n sulkemisvalintaikkunasta.
Vaihtoehtoisesti voit käyttää [komentorivivalitsinta](#CommandLineOptions) `--disable-addons`.

Voit selata yhteensopimattomia lisäosia [saatavilla olevien ja päivitettävien lisäosien välilehtiä](#AddonStoreFilterStatus) käyttäen.
Asennettuina olevia yhteensopimattomia lisäosia voit selata [asennettujen yhteensopimattomien lisäosien välilehteä](#AddonStoreFilterStatus) käyttäen.

## Lisätyökalut {#ExtraTools}
### Lokintarkastelu {#LogViewer}

Lokintarkastelulla, joka löytyy NVDA-valikon Työkalut-alivalikosta, voidaan tutkia kaikkia NVDA:n edellisen käynnistyksen jälkeen tulleita lokimerkintöjä.

Loki voidaan myös tallentaa tiedostoon tai ikkunan sisältö päivittää, jotta uusimmat lokin avaamisen jälkeen tulleet merkinnät näytetään.
Nämä toiminnot ovat käytettävissä lokintarkastelun Loki-valikossa.

Tiedosto, joka näytetään lokintarkastelua avattaessa, tallennetaan sijaintiin `%temp%\nvda.log`.
Jokaisella NVDA:n käynnistyskerralla luodaan uusi lokitiedosto.
Kun näin tapahtuu, edellisen NVDA-istunnon lokitiedosto siirretään nimelle `%temp%\nvda-old.log`.

Voit myös kopioida osan nykyisestä lokitiedostosta leikepöydälle avaamatta lokintarkastelua.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Avaa lokintarkastelu |`NVDA+F1` |Avaa lokintarkastelun ja näyttää kehittäjille tarkoitettua tietoa nykyisestä navigointiobjektista.|
|Kopioi osa lokista leikepöydälle |`NVDA+Ctrl+Vaihto+F1` |Kerran painaminen asettaa tallennettavan lokisisällön aloituspisteen. Toisen kerran painaminen kopioi lokin sisällön leikepöydälle aloituspisteestä lähtien.|

<!-- KC:endInclude -->

### Puheen tarkastelu {#SpeechViewer}

Näkeville ohjelmistokehittäjille tai NVDA:ta näkevälle yleisölle esitteleville on käytettävissä kelluva ikkuna, jonka avulla on mahdolista näyttää kaikki NVDA:n puhuma teksti.

Puheen tarkastelu otetaan käyttöön valitsemalla Puheen tarkastelu -vaihtoehto NVDA-valikon Työkalut-alivalikosta.
Toiminto poistetaan käytöstä poistamalla vaihtoehdon valinta.

Puheen tarkastelu -ikkunassa on "Näytä Puheen tarkastelu käynnistettäessä" -valintaruutu.
Mikäli se on valittuna, Puheen tarkastelu avataan, kun NVDA käynnistetään.
Ikkuna yrittää aina avautua uudelleen samoilla mitoilla ja samassa sijainnissa, mitkä sillä olivat sitä suljettaessa.

Kun Puheen tarkastelu -toiminto on käytössä, sen ikkuna päivittyy ajoittain näyttääkseen uusimman puhutun tekstin.
Jos kuitenkin viet hiiren ikkunan päälle tai siirrät kohdistuksen siihen, NVDA keskeyttää tilapäisesti tekstin päivittämisen, jotta olemassa olevaa sisältöä voidaan helposti valita ja kopioida.

Puheen tarkastelu -toiminto otetaan käyttöön mistä tahansa määrittämällä sille oma näppäinkomento [Näppäinkomennot-valintaikkunaa käyttäen.](#InputGestures)

### Pistekirjoituksen tarkastelu {#BrailleViewer}

Näkeville ohjelmistokehittäjille tai NVDA:ta näkevälle yleisölle esitteleville henkilöille on käytettävissä kelluva ikkuna, jonka avulla voidaan tarkastella pistekirjoitustulostetta sekä pistekirjoitusmerkkejä vastaavaa tekstiä.
Pistekirjoituksen tarkastelua voidaan käyttää samanaikaisesti fyysisen pistenäytön kanssa, jolloin ikkunassa näkyvien solujen määrä vastaa fyysisen laitteen solumäärää.
Kun pistekirjoituksen tarkastelu on käytössä, se päivittyy jatkuvasti näyttämään pistekirjoitusta, joka näytettäisiin fyysisellä pistenäytöllä.

Ota pistekirjoituksen tarkastelu käyttöön valitsemalla "Pistekirjoituksen tarkastelu" -vaihtoehto, joka löytyy NVDA-valikon Työkalut-alivalikosta.
Poista toiminto käytöstä poistamalla valikkokohteen valinta.

Fyysisissä pistenäytöissä on tyypillisesti painikkeita, jotka vierittävät näyttöä eteen- tai taaksepäin. Ota vierittäminen käyttöön pistekirjoituksen tarkastelu -työkalussa määrittämällä [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen pikanäppäimet, jotka vierittävät pistenäyttöä eteen- ja taaksepäin.

Pistekirjoituksen tarkastelu -ikkunassa on "Näytä pistekirjoituksen tarkastelu käynnistettäessä" -valintaruutu.
Mikäli se on valittuna, pistekirjoituksen tarkastelu -ikkuna avautuu, kun NVDA käynnistetään.
Ikkuna yrittää avautua uudelleen aina samoilla mitoilla ja sijainnilla, jotka sillä oli suljettaessa.

Pistekirjoituksen tarkastelu -ikkunassa on "Vie hiiri merkin päälle siirtääksesi kyseiseen soluun"-valintaruutu, joka ei ole oletusarvoisesti valittuna.
Jos se on valittuna, hiiren vieminen pistesolun päälle suorittaa Siirrä pistesoluun -komennon kyseiselle solulle.
Tätä käytetään usein kohdistimen siirtämiseen tai toiminnon suorittamiseen säätimelle.
Tästä voi olla hyötyä testattaessa, että NVDA pystyy asianmukaisesti kääntämään merkin pistesolusta.
Komentoa viivästetään, jotta tahaton soluihin siirtäminen estetään.
Hiiren on oltava solun päällä kunnes se muuttuu vihreäksi.
Solu on aluksi vaaleankeltainen, muuttuu sitten oranssiksi ja äkkiä vihreäksi.

Ota pistekirjoituksen tarkastelu käyttöön tai poista se käytöstä mistä tahansa määrittämällä sille oma näppäinkomento [Näppäinkomennot-valintaikkunaa](#InputGestures) käyttäen.

### Python-konsoli {#PythonConsole}

NVDA:n Python-konsoli, joka löytyy NVDA-valikon Työkalut-alivalikosta, on kehitystyökalu, joka on hyödyllinen virheiden etsinnässä, yleisessä NVDA:n sisäisen toiminnan tai sovelluksen saavutettavuushierarkian tutkimisessa.
Lisätietoja on [NVDA-kehittäjän oppaassa.](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html)

### Lisäosakauppa {#toc314}

Tämä avaa [NVDA:n lisäosakaupan](#AddonsManager).
Lisätietoja saat lukemalla yksityiskohtaisen [Lisäosat ja lisäosakauppa](#AddonsManager) -luvun.

### Luo massamuistiversio {#CreatePortableCopy}

Tämä vaihtoehto avaa valintaikkunan, jossa voit luoda NVDA:n asennetusta versiosta massamuistiversion.
Massamuistiversiota käytettäessä Työkalut-alivalikossa on "Luo massamuistiversio" -valikkokohteen sijaan vaihtoehto "Asenna NVDA".

Massamuistiversion luomisen tai NVDA:n asentava valintaikkuna kehottaa valitsemaan kansiopolun, johon massamuistiversio luodaan tai asennettava versio asennetaan.

Tässä valintaikkunassa voit ottaa käyttöön tai poistaa käytöstä seuraavat vaihtoehdot:

* Kopioi nykyisen käyttäjän asetukset (tämä sisältää tiedostot sijainnista %appdata%\roaming\NVDA tai massamuistiversion asetushakemistosta, ja sisältää lisäosat sekä muut moduulit)
* Käynnistä uusi massamuistiversio luonnin jälkeen tai käynnistä NVDA asennuksen jälkeen (käynnistää NVDA:n automaattisesti massamuistiversion luonnin tai asennuksen jälkeen)

### Suorita COM-rekisteröintien korjaustyökalu... {#RunCOMRegistrationFixingTool}

Ohjelmien asentaminen ja poistaminen voi tietyissä tapauksissa aiheuttaa COM DLL -tiedostojen rekisteröintien poistamisen.
Koska COM-liitännät, kuten IAccessible, ovat riippuvaisia oikeista COM DLL -rekisteröinneistä, ongelmia saattaa ilmetä, mikäli oikea rekisteröinti puuttuu.

Näin voi käydä esim. Adobe Readerin, Math Playerin ja muiden ohjelmien asennuksen ja poiston jälkeen.

Puuttuvat rekisteröinnit voivat aiheuttaa ongelmia selaimissa, työpöytäsovelluksissa, tehtäväpalkissa sekä muissa käyttöliittymissä.

Erityisesti seuraavat ongelmat voidaan ratkaista suorittamalla tämä työkalu:

* NVDA ilmoittaa "tuntematon" selaimia, kuten Firefoxia, Thunderbirdiä jne. käytettäessä
* NVDA ei vaihda kohdistus- ja selaustilojen välillä
* NVDA on erittäin hidas selaimissa navigoitaessa selaustilaa käytettäessä
* Ja mahdollisesti muita ongelmia

### Lataa liitännäiset uudelleen {#ReloadPlugins}

Tällä voidaan ladata uudelleen sovellusmoduulit ja yleisliitännäiset ilman NVDA:n uudelleenkäynnistystä, mistä voi olla hyötyä kehittäjille.
Sovellusmoduulit hallitsevat sitä, miten NVDA on vuorovaikutuksessa määrättyjen sovellusten kanssa.
Yleisliitännäiset puolestaan hallitsevat sitä, miten NVDA on vuorovaikutuksessa kaikkien sovellusten kanssa.

Seuraavista näppäinkomennoista voi myös olla hyötyä:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento |Kuvaus|
|---|---|---|
|Lataa liitännäiset uudelleen |`NVDA+Ctrl+F3` |Lataa uudelleen NVDA:n yleisliitännäiset ja sovellusmoduulit.|
|Puhu ladattu sovellusmoduuli ja sovelluksen tiedostonimi |`NVDA+Ctrl+F1` |Puhuu sovellusmoduulin nimen, mikäli sellainen on käytössä, ja aktiivisen sovelluksen tiedostonimen.|

<!-- KC:endInclude -->

## Tuetut puhesyntetisaattorit {#SupportedSpeechSynths}

Tässä kappaleessa on tietoja NVDA:n tukemista puhesyntetisaattoreista.
Kattavampi luettelo ilmaisista ja kaupallisista syntetisaattoreista, joita on mahdollista ostaa ja ladata NVDA:lla käytettäväksi, on [lisä-äänien sivulla.](https://github.com/nvaccess/nvda/wiki/ExtraVoices)

### eSpeak NG {#eSpeakNG}

[ESpeak NG](https://github.com/espeak-ng/espeak-ng) -puhesyntetisaattori on sisäänrakennettu NVDA:han, joten sen asentamiseksi ja käyttämiseksi ei tarvita muita erikoisajureita tai komponentteja.
NVDA käyttää oletusarvoisesti tätä syntetisaattoria Windows 8.1:ssä (Windows 10:ssä ja uudemmissa [Windows OneCorea](#OneCore)).
Tämä on hyvä valinta käytettäessä NVDA:ta USB-muistitikulta.

Jokainen eSpeak NG:n mukana tuleva ääni puhuu eri kieltä.
Tuettuja kieliä on yli 43.

Valittavissa on myös useita muunnelmia, jotka saavat puheäänen kuulostamaan erilaiselta.

### Microsoft Speech API versio 4 (SAPI 4) {#SAPI4}

SAPI4 on Microsoftin vanha ohjelmistopuhesyntetisaattoreiden standardi.
NVDA tukee tätä edelleen käyttäjillä, joilla on jo SAPI 4 -syntetisaattoreita asennettuna.
Microsoft ei kuitenkaan enää tue tätä, eikä tarvittavia komponentteja ole enää saatavilla.

Kun NVDA:ssa käytetään tätä syntetisaattoria, käytettävissä olevien puheäänten luettelo, johon pääsee [Asetukset](#NVDASettings)-valintaikkunan [Puhe-kategoriasta](#SpeechSettings) tai [Syntetisaattorin asetusrenkaasta](#SynthSettingsRing), sisältää kaikkien asennettujen SAPI4-syntetisaattoreiden puheäänet.

### Microsoft Speech API versio 5 (SAPI 5) {#SAPI5}

SAPI 5 on Microsoftin standardi ohjelmistopuhesyntetisaattoreille.
Monia tätä standardia noudattavia puhesyntetisaattoreita on mahdollista ostaa tai ladata ilmaiseksi eri yrityksiltä ja verkkosivustoilta. Tietokoneellasi on myös luultavasti esiasennettuna vähintään yksi SAPI 5 -ääni.
Kun NVDA:ssa käytetään tätä syntetisaattoria, käytettävissä olevien äänien luettelo, johon pääsee [Asetukset](#NVDASettings)-valintaikkunan [Puhe-kategoriasta](#SpeechSettings) tai [Syntetisaattorin asetusrenkaasta](#SynthSettingsRing), sisältää kaikkien asennettujen SAPI 5 -syntetisaattoreiden äänet.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Microsoft Speech Platform tarjoaa useille kielille ääniä, joita käytetään tavallisesti palvelinpohjaisten puhesovellusten kehittämiseeen.
Näitä ääniä voidaan käyttää myös NVDA:lla.

Niiden käyttämiseksi on asennettava seuraavat kaksi osaa:

* [Microsoft Speech Platform - Runtime (versio 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (versio 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Tällä sivulla on useita tiedostoja sekä puheentunnistusta että teksti puheeksi -käyttöä varten.
 Valitse haluttujen äänien/kielien teksti puheeksi -datan sisältävät tiedostot.
 Esimerkiksi tiedosto MSSpeech_TTS_en-US_ZiraPro.msi on amerikanenglantia puhuva ääni.

### Windows OneCore {#OneCore}

Windows 10 ja uudemmat sisältävät uusia ääniä, jotka tunnetaan OneCore- tai matkapuhelinääninä.
Ääniä on saatavilla useille kielille, ja ne reagoivat nopeammin kuin Microsoftin Speech API 5 -rajapinnan kautta käytettävät.
NVDA käyttää Windows 10:ssä ja uudemmissa oletusarvoisesti OneCore-ääniä ( muissa versioissa [eSpeak NG:tä](#eSpeakNG)).

Lisää uusia OneCore-ääniä menemällä Windowsin järjestelmäasetuksiin (Windows+I) ja valitsemalla sieltä ensin "Aika ja kieli" ja sitten "Puhe".
Paina "Lisää ääniä" -painiketta ja etsi haluamaasi kieltä kirjoittamalla se avautuvaan hakukenttään.
Monilla kielillä on useita muunnelmia.
"Yhdistynyt kuningaskunta" ja "Australia" ovat kaksi esimerkkiä englannin muunnelmista.
"Ranska", "Kanada" ja "Sveitsi" ovat käytettävissä olevat ranskankielen muunnelmat.
Etsi ensin laajempaa kieltä (kuten englanti tai ranska) ja etsi sitten muunnelma luettelosta.
Valitse kaikki haluamasi kielet ja lisää ne painamalla "Lisää"-painiketta.
Kun kielet on lisätty, käynnistä NVDA uudelleen.

Katso luettelo saatavilla olevista äänistä [tuetut kielet ja äänet](https://support.microsoft.com/fi-fi/windows/liite-a-tuetut-kielet-ja-%C3%A4%C3%A4net-4486e345-7730-53da-fcfe-55cc64300f01) -artikkelista.

## Tuetut pistenäytöt {#SupportedBrailleDisplays}

Tässä kappaleessa on tietoja NVDA:n tukemista pistenäytöistä.

### Automaattista tunnistusta tukevat pistenäytöt {#AutomaticDetection}

NVDA:n on mahdollista tunnistaa useita pistenäyttöjä automaattisesti joko USB:tä tai Bluetoothia käyttäen.
Automaattinen tunnistus otetaan käyttöön valitsemalla käytettäväksi pistenäytöksi Automaattinen NVDA:n [Pistekirjoituksen asetukset -valintaikkunasta.](#BrailleSettings)
Tämä vaihtoehto on oletusarvoisesti valittuna.

Seuraavat näytöt tukevat automaattista tunnistusta.

* Handy Tech
* Baum/Humanware/APH/Orbit
* HumanWare Brailliant BI/B
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille
* Eurobraille Esys/Esytime/Iris
* Nattiq nBraille
* Seika Notetaker: MiniSeika (16 tai 24 solua), V6 ja V6Pro (40 solua)
* Tivomatic Caiku Albatross 46/80
* Mikä tahansa HID Braille -protokollaa tukeva näyttö

### Freedom Scientific Focus/PAC Mate {#FreedomScientificFocus}

Kaikkia [Freedom Scientificin](https://www.freedomscientific.com/) Focus- ja PAC Mate -pistenäyttöjä tuetaan sekä USB-liitännällä että Bluetoothilla.
Näiden näyttöjen käyttämiseksi on asennettava ajurit.
Voit ladata ne [Focus Blue Braille Display Driver -sivulta](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Ajurit tukevat kaikkia Freedom Scientificin Focus- ja Pacmate-pistenäyttöjä, vaikka sivulla mainitaankin vain Focus 40 Blue.

NVDA tunnistaa oletusarvoisesti pistenäytöt automaattisesti ja voi yhdistää niihin joko USB:llä tai Bluetoothilla.
Näytön asetuksia määritettäessä voidaan kuitenkin myös itse valita USB-portti tai Bluetooth yhteystyypin rajoittamiseksi.
Tästä voi olla hyötyä, jos Focus-näyttö halutaan yhdistää NVDA:han Bluetoothilla ja silti ladata sitä tietokoneen USB-virralla.
Myös NVDA:n automaattinen pistenäytön tunnistus tunnistaa tämän näytön USB:tä tai Bluetoothia käytettäessä.

Seuraavassa on näiden pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |ylin kosketuskohdistinnäppäin 1 (ensimmäinen pistesolu)|
|Vieritä eteenpäin |ylin kosketuskohdistinnäppäin 20/40/80 (viimeinen pistesolu)|
|Vieritä taaksepäin |vasen eteenpäin siirtävä näppäin|
|Vieritä eteenpäin |oikea eteenpäin siirtävä näppäin|
|Vaihda Pistenäyttö seuraa -asetusta |leftGDFButton+rightGDFButton|
|Vaihda vasemman säätörullan toimintoa |vasemman säätörullan painallus|
|Siirrä taaksepäin vasenta säätörullaa käyttäen |vasen säätörulla ylös|
|Siirrä eteenpäin vasenta säätörullaa käyttäen |vasen säätörulla alas|
|Vaihda oikean säätörullan toimintoa |oikean säätörullan painallus|
|Siirrä taaksepäin oikeaa säätörullaa käyttäen |oikea säätörulla ylös|
|Siirrä eteenpäin oikeaa säätörullaa käyttäen |oikea säätörulla alas|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihto+Sarkain-näppäinyhdistelmä |väli+pisteet 1 ja 2|
|Sarkain-näppäin |väli+pisteet 4 ja 5|
|Nuoli ylös -näppäin |väli+piste 1|
|Nuoli alas -näppäin |väli+piste 4|
|Ctrl+Nuoli vasemmalle -näppäinyhdistelmä |väli+piste 2|
|Ctrl+Nuoli oikealle -näppäinyhdistelmä |väli+piste 5|
|Nuoli vasemmalle -näppäin |väli+piste 3|
|Nuoli oikealle -näppäin |väli+piste 6|
|Home-näppäin |väli+pisteet 1 ja 3|
|End-näppäin |väli+pisteet 4 ja 6|
|Ctrl+Home-näppäinyhdistelmä |väli+pisteet 1, 2 ja 3|
|Ctrl+End-näppäinyhdistelmä |väli+pisteet 4, 5 ja 6|
|Alt-näppäin |väli+pisteet 1, 3 ja 4|
|Alt+Sarkain-näppäinyhdistelmä |väli+pisteet 2, 3, 4 ja 5|
|Alt+Vaihto+Sarkain-näppäinyhdistelmä |väli+pisteet 1, 2, 5 ja 6|
|Windows+Sarkain-näppäinyhdistelmä |väli+pisteet 2, 3 ja 4|
|Esc-näppäin |väli+pisteet 1 ja 5|
|Windows-näppäin |väli+pisteet 2, 4, 5 ja 6|
|Väli |väli|
|Vaihda Ctrl-näppäimen tilaa |väli+pisteet 3 ja 8|
|Vaihda Alt-näppäimen tilaa |väli+pisteet 6 ja 8|
|Vaihda Win-näppäimen tilaa |väli+pisteet 4 ja 8|
|Vaihda NVDA-näppäimen tilaa |väli+pisteet 5 ja 8|
|Vaihda Vaihto-näppäimen tilaa |väli+pisteet 7 ja 8|
|Vaihda Ctrl- ja Vaihto-näppäinten tilaa |väli+pisteet 3, 7 ja 8|
|Vaihda Alt- ja Vaihto-näppäinten tilaa |väli+pisteet 6, 7 ja 8|
|Vaihda Win- ja Vaihto-näppäinten tilaa |väli+pisteet 4, 7 ja 8|
|Vaihda NVDA- ja Vaihto-näppäinten tilaa |väli+pisteet 5, 7 ja 8|
|Vaihda Ctrl- ja Alt-näppäinten tilaa |väli+pisteet 3, 6 ja 8|
|Vaihda Ctrl-, Alt- ja Vaihto-näppäinten tilaa |väli+pisteet 3, 6, 7 ja 8|
|Windows+D-näppäinyhdistelmä (pienennä kaikki sovellukset) |väli+pisteet 1, 2, 3, 4, 5 ja 6|
|Lue nykyinen rivi |väli+pisteet 1 ja 4|
|NVDA-valikko |väli+pisteet 1, 3, 4 ja 5|

Uudet Focus-mallit, joissa on keinunäppäimiä (Focus 40, 80 ja Blue):

| Nimi |Näppäinkomento|
|---|---|
|Siirrä edelliselle riville |vasen keinunäppäin alas, oikea keinunäppäin ylös|
|Siirrä seuraavalle riville |vasen keinunäppäin alas, oikea keinunäppäin alas|

Vain Focus 80:

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |leftBumperBarUp, rightBumperBarUp|
|Vieritä eteenpäin |leftBumperBarDown, rightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA 6/protokollamuunnin {#OptelecALVA}

[Optelecin](https://www.optelec.com/) ALVA BC640- ja BC680 -pistenäyttöjä tuetaan sekä USB-liitäntää että Bluetooth-yhteyttä käytettäessä.
Vaihtoehtoisesti voit liittää vanhemman näytön, kuten Braille Voyagerin, käyttämällä Optelecin toimittamaa protokollamuunninta.
Näiden näyttöjen käyttämiseksi ei tarvitse asentaa ajureita.
Riittää, että pistenäyttö kytketään tietokoneeseen ja määritetään NVDA käyttämään sitä.

Huom: NVDA ei välttämättä pysty käyttämään ALVA BC6 -näyttöä Bluetoothin kautta, kun sen ja tietokoneen välinen laitepari on muodostettu ALVA:n Bluetooth-apuohjelmalla.
Kun pariliitos on luotu tätä apuohjelmaa käyttäen ja NVDA ei tunnista laitettasi, suosittelemme käyttämään laiteparin muodostamiseen Windowsin Bluetooth-asetuksia.

Vaikka joissakin näistä pistenäytöistä onkin pistenäppäimistö, ne huolehtivat itse pistekirjoituksen kääntämisestä tekstiksi.
Tämä tarkoittaa, että oletusarvoisesti NVDA:n pistekirjoituksen syöttöjärjestelmää ei käytetä (ts. pistesyöttötaulukkoasetuksella ei ole vaikutusta).
HID-näppäimistösimulointi on mahdollista poistaa käytöstä näppäinkomennolla ALVA-näytöissä, joissa on viimeisin laiteohjelmisto.

Seuraavassa on näiden pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso laitteen käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |t1, etouch1|
|Siirrä edelliselle riville |t2|
|Siirrä nykyiseen kohdistukseen |t3|
|Siirrä seuraavalle riville |t4|
|Vieritä eteenpäin |t5, etouch3|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Ilmoita muotoilutiedot pistesolusta |toissijainen kosketuskohdistinnäppäin|
|Vaihda HID-näppäimistösyötteen simuloinnin asetusta |t1+spEnter|
|Siirrä ylimmälle riville |t1+t2|
|Siirrä alimmalle riville |t4+t5|
|Vaihda Pistenäyttö seuraa -asetusta |t1+t3|
|Lue ikkunan nimi |etouch2|
|Lue tilarivi |etouch4|
|Vaihto+Sarkain-näppäinyhdistelmä |sp1|
|Alt-näppäin |sp2, alt|
|Esc-näppäin |sp3|
|Sarkain-näppäin |sp4|
|Nuoli ylös -näppäin |spUp|
|Nuoli alas -näppäin |spDown|
|Nuoli vasemmalle -näppäin |spLeft|
|Nuoli oikealle -näppäin |spRight|
|Enter-näppäin |spEnter, enter|
|Lue päivämäärä/aika |sp2+sp3|
|NVDA-valikko |sp1+sp3|
|Windows+D-näppäinyhdistelmä (pienennä kaikki sovellukset) |sp1+sp4|
|Windows+B-näppäinyhdistelmä (siirrä kohdistus järjestelmätarjottimelle) |sp3+sp4|
|Windows-näppäin |sp1+sp2, windows|
|Alt+Sarkain-näppäinyhdistelmä |sp2+sp4|
|Ctrl+Home-näppäinyhdistelmä |t3+spUp|
|Ctrl+End-näppäinyhdistelmä |t3+spDown|
|Home-näppäin |t3+spLeft|
|End-näppäin |t3+spRight|
|Ctrl-näppäin |control|

<!-- KC:endInclude -->

### Handy Tech {#HandyTech}

NVDA tukee useimpia [Handy Techin](https://www.handytech.de/) pistenäyttöjä, joissa on USB/sarjaporttiliitäntä tai Bluetooth-yhteys.
Vanhempia USB-malleja varten tietokoneelle on asennettava Handy Techin USB-ajurit.

Seuraavia näyttöjä ei tueta oletusarvoisesti, mutta niitä voidaan käyttää [Handy Techin yleisajurin](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) ja NVDA-lisäosan avulla:

* Braillino
* Bookworm
* Modular-mallit, joissa on laiteohjelmiston versio 1.13 tai vanhempi. Huomaa, että näiden näyttöjen laiteohjelmisto on mahdollista päivittää.

Seuraavassa on lueteltu Handy Tech -pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |vasen, ylös, b3|
|Vieritä eteenpäin |oikea, alas, b6|
|Siirrä edelliselle riville |b4|
|Siirrä seuraavalle riville |b5|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihto+Sarkain-näppäinyhdistelmä |esc, vasen kolmitoimintonäppäin ylös+alas|
|Alt-näppäin |b2+b4+b5|
|Esc-näppäin |b4+b6|
|Sarkain-näppäin |enter, oikea kolmitoimintonäppäin ylös+alas|
|Enter-näppäin |esc+enter, vasen+oikea kolmitoimintonäppäin ylös+alas, ohjaussauvatoiminto|
|Nuoli ylös -näppäin |ohjaussauva ylös|
|Nuoli alas -näppäin |ohjaussauva alas|
|Nuoli vasemmalle -näppäin |ohjaussauva vasemmalle|
|Nuoli oikealle -näppäin |ohjaussauva oikealle|
|NVDA-valikko |b2+b4+b5+b6|
|Vaihda Pistenäyttö seuraa -asetusta |b2|
|Vaihda pistekohdistinta |b1|
|Vaihda kohdistuskontekstin näyttämisen asetusta |b7|
|Ota pistekirjoituksen syöttö käyttöön tai poista se käytöstä |väli+b1+b3+b4 (väli+iso b)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

[MDV:n](https://www.mdvbologna.it/) Lilli-pistenäyttöä tuetaan.
Sen käyttämiseksi ei tarvitse asentaa ajureita.
Riittää, että pistenäyttö kytketään tietokoneeseen ja määritetään NVDA käyttämään sitä.

Tämä näyttö ei tue NVDA:n automaattista pistenäytön tunnistusta.

Seuraavassa on lueteltu tämän pistenäytön näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |LF|
|Vieritä eteenpäin |RG|
|Siirrä edelliselle riville |UP|
|Siirrä seuraavalle riville |DN|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihto+Sarkain-näppäinyhdistelmä |SLF|
|Sarkain-näppäin |SRG|
|Alt+Sarkain-näppäinyhdistelmä |SDN|
|Alt+Vaihto+Sarkain-näppäinyhdistelmä |SUP|

<!-- KC:endInclude -->

### Baum/Humanware/APH/Orbit {#Baum}

Useita [Baum](https://www.visiobraille.de/index.php?article_id=1&clang=2)-, [HumanWare](https://www.humanware.com/)-, [APH](https://www.aph.org/)- ja [Orbit](https://www.orbitresearch.com/)-pistenäyttöjä tuetaan USB:llä, Bluetoothilla tai sarjaportin kautta yhdistettäessä.
Näitä ovat:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Muutkin Baumin valmistamat pistenäytöt voivat toimia, vaikkei niitä olekaan testattu.

Mikäli tietokoneeseen yhdistetään USB:llä pistenäyttö, joka ei käytä HID:tä, valmistajan toimittamat ajurit on asennettava ensin.
VarioUltra ja Pronto! käyttävät HID:tä.
Refreshabraille ja Orbit Reader 20 voivat käyttää HID:tä, mikäli ne on siten määritelty.

Orbit Reader 20:n USB-sarjaporttitilaa tuetaan tällä hetkellä vain Windows 10:ssä ja uudemmissa.
Sen asemesta tulisi useimmiten käyttää USB-HID:tä.

Seuraavassa on näiden pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |`d2`|
|Vieritä eteenpäin |`d5`|
|Siirrä edelliselle riville |`d1`|
|Siirrä seuraavalle riville |`d3`|
|Siirrä pistesoluun |`kosketuskohdistinnäppäin`|
|`Vaihto+Sarkain`-näppäinyhdistelmä |`väli+pisteet 1 ja 3`|
|`Sarkain`-näppäin |`väli+pisteet 4 ja 6`|
|`Alt`-näppäin |`väli+pisteet 1, 3 ja 4` (`väli+m`)|
|`Esc`-näppäin |`väli+pisteet 1 ja 5` (`väli+e`)|
|`Windows`-näppäin |`väli+pisteet 3 ja 4`|
|`Alt+Sarkain`-näppäinyhdistelmä |`väli+pisteet 2, 3, 4 ja 5` (`väli+t`)|
|NVDA-valikko |`väli+pisteet 1, 3, 4 ja 5` (`väli+n`)|
|`Windows+D`-näppäinyhdistelmä (pienennä kaikki sovellukset) |`väli+pisteet 1, 4 ja 5` (`väli+d`)|
|Jatkuva luku |`väli+pisteet 1, 2, 3, 4, 5 ja 6`|

Malleissa, joissa on ohjaustappi:

| Nimi |Näppäinkomento|
|---|---|
|Nuoli ylös -näppäin |ylös|
|Nuoli alas -näppäin |alas|
|Nuoli vasemmalle -näppäin |vasen|
|Nuoli oikealle -näppäin |oikea|
|Enter-näppäin |valitse|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

[Hedo Reha-Technikin](https://www.hedo.de/) hedo ProfiLine USB -pistenäyttöä tuetaan.
Sen käyttämiseksi on asennettava valmistajan toimittamat USB-ajurit.

Tämä näyttö ei vielä tue NVDA:n automaattista pistenäytön tunnistusta.

Seuraavassa on tämän pistenäytön näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |K1|
|Vieritä eteenpäin |K3|
|Siirrä edelliselle riville |B2|
|Siirrä seuraavalle riville |B5|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihda Pistenäyttö seuraa -asetusta |K2|
|Jatkuva luku |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

[Hedo Reha-Technikin](https://www.hedo.de/) hedo MobilLine USB -pistenäyttöä tuetaan.
Sen käyttämiseksi on asennettava valmistajan toimittamat USB-ajurit.

Tämä näyttö ei vielä tue NVDA:n automaattista pistenäytön tunnistusta.

Seuraavassa on tämän pistenäytön näppäinkomennot NVDA:ta käytettäessä.
Katso näytön käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |K1|
|Vieritä eteenpäin |K3|
|Siirrä edelliselle riville |B2|
|Siirrä seuraavalle riville |B5|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihda Pistenäyttö seuraa -asetusta |K2|
|Jatkuva luku |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B / BrailleNote Touch {#HumanWareBrailliant}

[HumanWaren](https://www.humanware.com/) Brailliant BI- ja B -sarjan pistenäyttöjä tuetaan, BI 14, BI 32, BI 20X, BI 40, BI 40X ja B 80 mukaan lukien, kun ne liitetään tietokoneeseen USB:llä tai Bluetoothilla.
Mikäli käytetään USB-liitäntää ja protokollaksi on määritetty HumanWare, valmistajan toimittamat ajurit on asennettava ensin.
OpenBraille-protokollaa käytettäessä ajureita ei tarvita.

Myös seuraavia laitteita tuetaan, eikä niitä varten tarvitse asentaa ajureita.

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Seuraavassa on Brailliant BI/B- ja BrailleNote Touch -näyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso laitteiden käyttöohjeista kuvaukset näppäinten paikoista.

#### Kaikki mallit {#toc334}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |vasen|
|Vieritä eteenpäin |oikea|
|Siirrä edelliselle riville |ylös|
|Siirrä seuraavalle riville |alas|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihda Pistenäyttö seuraa -asetusta |ylös+alas|
|Nuoli ylös -näppäin |väli+piste 1|
|Nuoli alas -näppäin |väli+piste 4|
|Nuoli vasemmalle -näppäin |väli+piste 3|
|Nuoli oikealle -näppäin |väli+piste 6|
|Vaihto+Sarkain-näppäinyhdistelmä |väli+pisteet 1 ja 3|
|Sarkain-näppäin |väli+pisteet 4 ja 6|
|Alt-näppäin |väli+pisteet 1, 3 ja 4 (väli+m)|
|Esc-näppäin |väli+pisteet 1 ja 5 (väli+e)|
|Enter-näppäin |piste 8|
|Windows-näppäin |väli+pisteet 3 ja 4|
|Alt+Sarkain-näppäinyhdistelmä |väli+pisteet 2, 3, 4 ja 5 (väli+t)|
|NVDA-valikko |väli+pisteet 1, 3, 4 ja 5 (väli+n)|
|Windows+D-näppäinyhdistelmä (pienennä kaikki sovellukset) |väli+pisteet 1, 4 ja 5 (väli+d)|
|Jatkuva luku |väli+pisteet 1, 2, 3, 4, 5 ja 6|

<!-- KC:endInclude -->

#### Brailliant BI 32, BI 40 ja B 80 {#toc335}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|NVDA-valikko |c1, c3, c4 ja c5 (komento n)|
|Windows+D-näppäinyhdistelmä (pienennä kaikki sovellukset) |c1, c4 ja c5 (komento d)|
|Jatkuva luku |c1, c2, c3, c4, c5 ja c6|

<!-- KC:endInclude -->

#### Brailliant BI 14 {#toc336}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Nuoli ylös -näppäin |ohjaussauva ylös|
|Nuoli alas -näppäin |ohjaussauva alas|
|Vasen nuoli -näppäin |ohjaussauva vasemmalle|
|Oikea nuoli -näppäin |ohjaussauva oikealle|
|Enter-näppäin |ohjaussauvan toiminto|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille {#Hims}

NVDA tukee [HIMSin](https://www.hims-inc.com/) Braille Sense-, Braille EDGE-, Smart Beetle- ja Sync Braille -pistenäyttöjä USB-liitäntää tai Bluetooth-yhteyttä käytettäessä.
USB-liitäntää käytettäessä tietokoneelle on asennettava [HIMSin USB-ajurit](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip).

Seuraavassa on näiden pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso laitteen käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Siirrä pistesoluun |kosketuskohdistin|
|Vieritä taaksepäin |vasemmanpuoleinen vieritä ylös, oikeanpuoleinen vieritä ylös, vasemmanpuoleinen vieritä|
|Vieritä eteenpäin |vasemmanpuoleinen vieritä alas, oikeanpuoleinen vieritä alas, oikeanpuoleinen vieritä|
|Siirrä edelliselle riville |vasemmanpuoleinen vieritä ylös+oikeanpuoleinen vieritä ylös|
|Siirrä seuraavalle riville |vasemmanpuoleinen vieritä alas+oikeanpuoleinen vieritä alas|
|Siirrä edelliselle riville tarkastelutilassa |oikeanpuoleinen nuoli ylös|
|Siirrä seuraavalle riville tarkastelutilassa |oikeanpuoleinen nuoli alas|
|Siirrä edelliseen merkkiin tarkastelutilassa |oikeanpuoleinen nuoli vasemmalle|
|Siirrä seuraavaan merkkiin tarkastelutilassa |oikeanpuoleinen nuoli oikealle|
|Siirrä kohdistukseen |vasemman puoleinen vieritä ylös+vasemmanpuoleinen vieritä alas, oikeanpuoleinen vieritä ylös+oikeanpuoleinen vieritä alas, vasemmanpuoleinen vieritä+oikeanpuoleinen vieritä|
|Ctrl-näppäin |smartbeetle: f1, Braille EDGE: f3|
|Windows-näppäin |f7, Smart Beetle: f2|
|Alt-näppäin |pisteet 1, 3 ja 4+väli, f2, Smart Beetle: f3, Braille EDGE: f4|
|Vaihto-näppäin |f5|
|Insert-näppäin |pisteet 2 ja 4+väli, f6|
|Sovellusnäppäin |pisteet 1, 2, 3 ja 4+väli, f8|
|Caps Lock -näppäin |pisteet 1, 3 ja 6+väli|
|Sarkain-näppäin |pisteet 4 ja 5+väli, f3, Braille EDGE: f2|
|Vaihto+Alt+Sarkain-näppäinyhdistelmä |f2+f3+f1|
|Alt+Sarkain-näppäinyhdistelmä |f2+f3|
|Vaihto+Sarkain-näppäinyhdistelmä |pisteet 1 ja 2+väli|
|End-näppäin |pisteet 4 ja 6+väli|
|Ctrl+End-näppäinyhdistelmä |pisteet 4, 5 ja 6+väli|
|Home-näppäin |pisteet 1 ja 3+väli, Smart Beetle: f4|
|Ctrl+Home-näppäinyhdistelmä |pisteet 1, 2 ja 3+väli|
|Alt+F4-näppäinyhdistelmä |pisteet 1, 3, 5 ja 6+väli|
|Nuoli vasemmalle -näppäin |piste 3+väli, vasemmanpuoleinen nuoli vasemmalle|
|Ctrl+Vaihto+Nuoli vasemmalle -näppäinyhdistelmä |pisteet 2 ja 8+väli+f1|
|Ctrl+Nuoli vasemmalle -näppäinyhdistelmä |piste 2+väli|
|Vaihto+Alt+Nuoli vasemmalle -näppäinyhdistelmä |pisteet 2 ja 7+f1|
|Alt+Nuoli vasemmalle -näppäinyhdistelmä |pisteet 2 ja 7+väli|
|Nuoli oikealle -näppäin |piste 6+väli, vasemmanpuoleinen nuoli oikealle|
|Ctrl+Vaihto+Nuoli oikealle -näppäinyhdistelmä |pisteet 5 ja 8+väli+f1|
|Ctrl+Nuoli oikealle -näppäinyhdistelmä |piste 5+väli|
|Vaihto+Alt+Nuoli oikealle -näppäinyhdistelmä |pisteet 5 ja 7+f1|
|Alt+Nuoli oikealle -näppäinyhdistelmä |pisteet 5 ja 7+väli|
|Page up -näppäin |pisteet 1, 2 ja 6+väli|
|Ctrl+Page up -näppäinyhdistelmä |pisteet 1, 2, 6 ja 8+väli|
|Nuoli ylös -näppäin |piste 1+väli, vasemmanpuoleinen nuoli ylös|
|Ctrl+Vaihto+Nuoli ylös -näppäinyhdistelmä |pisteet 2, 3 ja 8+väli+f1|
|Ctrl+Nuoli ylös -näppäinyhdistelmä |pisteet 2 ja 3+väli|
|Vaihto+Alt+Nuoli ylös -näppäinyhdistelmä |pisteet 2, 3 ja 7+f1|
|Alt+Nuoli ylös -näppäinyhdistelmä |pisteet 2, 3 ja 7+väli|
|Vaihto+Nuoli ylös -näppäinyhdistelmä |vasemmanpuoleinen vieritä alas+väli|
|Page down -näppäin |pisteet 3, 4 ja 5+väli|
|Ctrl+Page down -näppäinyhdistelmä |pisteet 3, 4, 5 ja 8+väli|
|Nuoli alas -näppäin |piste 4+väli, vasemmanpuoleinen nuoli alas|
|Ctrl+Vaihto+Nuoli alas -näppäinyhdistelmä |pisteet 5, 6 ja 8+väli+f1|
|Ctrl+Nuoli alas -näppäinyhdistelmä |pisteet 5 ja 6+väli|
|Vaihto+Alt+Nuoli alas -näppäinyhdistelmä |pisteet 5, 6 ja 7+f1|
|Alt+Nuoli alas -näppäinyhdistelmä |pisteet 5, 6 ja 7+väli|
|Vaihto+Nuoli alas -näppäinyhdistelmä |väli+oikeanpuoleinen vieritä alas|
|Esc-näppäin |pisteet 1 ja 5+väli, f4, Braille EDGE: f1|
|Delete-näppäin |pisteet 1, 3 ja 5+väli, pisteet 1, 4 ja 5+väli|
|F1-näppäin |pisteet 1, 2 ja 5+väli|
|F3-näppäin |pisteet 1, 4 ja 8+väli|
|F4-näppäin |piste 7+f3|
|Windows+B-näppäinyhdistelmä |pisteet 1 ja 2+f1|
|Windows+D-näppäinyhdistelmä |pisteet 1, 4 ja 5+f1|
|Ctrl+Insert-näppäimet |Smart Beetle: f1+oikeanpuoleinen vieritä|
|Alt+Insert-näppäimet |Smart Beetle: f3+oikeanpuoleinen vieritä|

<!-- KC:endInclude -->

### Seika {#Seika}

Seuraavia Nippon Telesoftin Seika-pistenäyttöjä tuetaan kahdessa ryhmässä eri toiminnallisuuksilla:

* [Seika-versiot 3, 4 ja 5 (40 solua), Seika80 (80 solua)](#SeikaBrailleDisplays)
* [MiniSeika (16 tai 24 solua), V6 ja V6Pro (40 solua)](#SeikaNotetaker)

Lisätietoa löytyy näyttöjen [Demo and Driver Download -sivulta](https://en.seika-braille.com/down/index.html).

#### Seika-versiot 3, 4 ja 5 (40 solua), Seika80 (80 solua) {#SeikaBrailleDisplays}

* Nämä näytöt eivät vielä tue NVDA:n automaattista pistenäytön tunnistusta.
* Ota ne käyttöön manuaalisesti valitsemalla "Seika"
* Laiteajurit on asennettava ennen Seika v3/4/5/80-näyttöjen käyttämistä.
Ajurit toimittaa [valmistaja.](https://en.seika-braille.com/down/index.html)

> -

Seuraavassa ovat näiden pistenäyttöjen näppäinmääritykset.
Katso laitteen käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |vasen|
|Vieritä eteenpäin |oikea|
|Siirrä edelliselle riville |b3|
|Siirrä seuraavalle riville |b4|
|Vaihda Pistenäyttö seuraa -asetusta |b5|
|Jatkuva luku |b6|
|Sarkain-näppäin |b1|
|Vaihto+Sarkain-näppäinyhdistelmä |b2|
|Alt+Sarkain-näppäinyhdistelmä |b1+b2|
|NVDA-valikko |vasen+oikea|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|

<!-- KC:endInclude -->

#### MiniSeika (16 tai 24 solua), V6 ja V6Pro (40 solua) {#SeikaNotetaker}

* NVDA:n automaattista pistenäytön tunnistusta tuetaan USB- ja Bluetooth-yhteydellä.
* Määritä valitsemalla "Seika Notetaker" tai "Automaattinen".
* Seika Notetaker -pistenäytön käyttämiseen ei tarvita ylimääräisiä ajureita.

Seuraavassa ovat näiden näyttöjen näppäinmääritykset.
Katso laitteen käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäin|
|---|---|
|Vieritä taaksepäin |vasen|
|Vieritä eteenpäin |oikea|
|Jatkuva luku |väli+askelpalautin|
|NVDA-valikko |vasen+oikea|
|Siirrä edelliselle riville |LJ ylös|
|Siirrä seuraavalle riville |LJ alas|
|Vaihda Pistenäyttö seuraa -asetusta |LJ keskikohta|
|Sarkain |LJ oikea|
|Vaihto+Sarkain |LJ vasen|
|Nuoli ylös -näppäin |RJ ylös|
|Nuoli alas -näppäin |RJ alas|
|Nuoli vasemmalle -näppäin |RJ vasen|
|Nuoli oikealle -näppäin |RJ oikea|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Vaihto+Nuoli ylös -näppäinyhdistelmä |väli+RJ ylös, askelpalautin+RJ ylös|
|Vaihto+Nuoli alas -näppäinyhdistelmä |väli+RJ alas, askelpalautin+RJ alas|
|Vaihto+Nuoli vasemmalle -näppäinyhdistelmä |väli+RJ vasen, askelpalautin+RJ vasen|
|Vaihto+Nuoli oikealle -näppäinyhdistelmä |väli+RJ oikea, askelpalautin+RJ oikea|
|Enter-näppäin |RJ keskikohta, piste 8|
|Esc-näppäin |väli+RJ keskikohta|
|Win-näppäin |askelpalautin+RJ keskikohta|
|Väli-näppäin |väli, askelpalautin|
|Askelpalautin-näppäin |piste 7|
|Page up -näppäin |väli+LJ oikea|
|Page down -näppäin |väli+LJ vasen|
|Home-näppäin |väli+LJ ylös|
|End-näppäin |väli+LJ alas|
|Ctrl+Home-näppäinyhdistelmä |askelpalautin+LJ ylös|
|Ctrl+End-näppäinyhdistelmä |askelpalautin+LJ alas|

### Papenmeier BRAILLEX (uudet mallit) {#Papenmeier}

Seuraavia pistenäyttöjä tuetaan:

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB ja Bluetooth)
* BRAILLEX Live 20, BRAILLEX Live sekä BRAILLEX Live Plus (USB ja Bluetooth)

Nämä näytöt eivät tue NVDA:n automaattista pistenäytön tunnistusta.
Laitteen USB-ajurissa on asetus, joka voi aiheuttaa ongelmia näytön käyttöönotossa.
Kokeile seuraavaa:

1. Varmista, että olet asentanut [uusimman ajurin](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Avaa Windowsin laitehallinta.
1. Selaa luetteloa alaspäin kohtaan "USB-ohjaimet" tai "USB-laitteet".
1. Valitse "Papenmeier Braillex USB Device".
1. Avaa ominaisuudet ja vaihda "Lisäasetukset"-välilehdelle.
Toisinaan se ei kuitenkaan tule näkyviin.
Jos näin käy, irrota pistenäyttö tietokoneesta, sulje NVDA, odota hetki ja yhdistä pistenäyttö uudelleen.
Toista tämä tarvittaessa 4-5 kertaa.
Jos "Lisäasetukset"-välilehteä ei vieläkään näytetä, käynnistä tietokone uudelleen.
1. Poista "Load VCP" -asetus käytöstä.

Useimmissa laitteissa on intuitiivisen ja nopean käytön mahdollistava Easy Access Bar (EAB).
Sitä voidaan siirtää neljään suuntaan, joissa kussakin on yleensä kaksi kytkintä.
C- ja Live-sarjan näytöt ovat ainoa poikkeus.

C-mallin näytöissä ja muutamassa muussakin on kaksi kosketuskohdistinriviä, joista ylempää käytetään muotoilutietojen lukemiseen.
C-sarjan laitteissa ylärivin jonkin näppäimen alhaalla pitäminen ja EAB:n painaminen jäljittelee toisen kytkimen tilaa.
Live-sarjan näytöissä on vain yksi kosketuskohdistinrivi, ja EAB:ssä on yksi vaihe kutakin suuntaa kohti.
Toista vaihetta jäljitellään painamalla jotakin kosketuskohdistinnäppäintä ja EAB:tä vastaavaan suuntaan.
Ylös-, alas-, oikea- ja vasen-näppäinten (tai EAB:n) painaminen ja alhaalla pitäminen toistaa kyseessä olevan toiminnon.

Näissä pistenäytöissä on käytettävissä yleensä seuraavat näppäimet:

| Nimi |Näppäinkomento|
|---|---|
|l1 |Vasen etunäppäin|
|l2 |Vasen takanäppäin|
|r1 |Oikea etunäppäin|
|r2 |Oikea takanäppäin|
|up |Yksi askel ylös|
|up2 |Kaksi askelta ylös|
|left |Yksi askel vasemmalle|
|left2 |Kaksi askelta vasemmalle|
|right |Yksi askel oikealle|
|right2 |Kaksi askelta oikealle|
|dn |Yksi askel alas|
|dn2 |Kaksi askelta alas|

Seuraavassa on Papenmeierin näppäinmääritykset NVDA:lle:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |left|
|Vieritä eteenpäin |right|
|Siirrä edelliselle riville |up|
|Siirrä edelliselle riville |dn|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Lue nykyinen merkki |l1|
|Aktivoi nykyinen navigointiobjekti |l2|
|Vaihda Pistenäyttö seuraa -asetusta |r2|
|Lue ikkunan nimi |l1+up|
|Lue tilarivi |l2+down|
|Siirrä säilöobjektiin |up2|
|Siirrä ensimmäiseen sisältöobjektiin |dn2|
|Siirrä edelliseen objektiin |left2|
|Siirrä seuraavaan objektiin |right2|
|Ilmoita tekstin muotoilutiedot pistesolusta |ylärivin kosketuskohdistinnäppäimet|

<!-- KC:endInclude -->

Trio-mallissa on neljä lisänäppäintä, jotka ovat pistenäppäimistön edessä.
Ne ovat järjestyksessä vasemmalta oikealle:

* vasen peukalonäppäin (lt)
* väli-näppäin
* väli-näppäin
* oikea peukalonäppäin (rt)

Oikea peukalonäppäin ei ole toistaiseksi käytössä.
Molemmat sisemmät näppäimet on määritelty Väli-näppäimeksi.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Esc-näppäin |väli ja piste 7|
|Nuoli ylös -näppäin |väli ja piste 2|
|Nuoli vasemmalle -näppäin |väli ja piste 1|
|Nuoli oikealle -näppäin |väli ja piste 4|
|Nuoli alas -näppäin |väli ja piste 5|
|Ctrl-näppäin |lt ja piste 2|
|Alt-näppäin |lt ja piste 3|
|Ctrl+Esc-näppäinyhdistelmä |väli+pisteet 1, 2, 3, 4, 5 ja 6|
|Sarkain-näppäin |väli+pisteet 3 ja 7|

<!-- KC:endInclude -->

### Papenmeier BRAILLEX (vanhat mallit) {#PapenmeierOld}

Seuraavia pistenäyttöjä tuetaan:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Huom: Nämä pistenäytöt voidaan liittää vain sarjaportin kautta.
Tämän vuoksi Nämä näytöt eivät tue NVDA:n automaattista pistenäytön tunnistusta.
Portti, johon laite on liitetty, tulee valita sen jälkeen, kun pistenäytön ajuri on valittu [Valitse pistenäyttö](#SelectBrailleDisplay) -valintaikkunasta.

Joissakin laitteissa on intuitiivisen ja nopean käytön mahdollistava Easy Access Bar (EAB).
Sitä voidaan liikuttaa neljään suuntaan, joissa kussakin on yleensä kaksi kytkintä.
Ylös-, alas-, oikea- ja vasen-näppäinten (tai EAB:n) painaminen ja alhaalla pitäminen toistaa kyseessä olevan toiminnon.
Vanhoissa laitteissa ei ole EAB:tä; sen sijaan käytetään etupaneelin näppäimiä.

Näissä pistenäytöissä on yleensä käytettävissä seuraavat näppäimet:

| Nimi |Näppäinkomento|
|---|---|
|l1 |Vasen etunäppäin|
|l2 |Vasen takanäppäin|
|r1 |Oikea etunäppäin|
|r2 |Oikea takanäppäin|
|up |1 askel ylöspäin|
|up2 |2 askelta ylöspäin|
|left |1 askel vasemmalle|
|left2 |2 askelta vasemmalle|
|right |1 askel oikealle|
|right2 |2 askelta oikealle|
|dn |1 askel alaspäin|
|dn2 |2 askelta alaspäin|

Seuraaavassa on Papenmeierin komentomääritykset NVDA:lle:

<!-- KC:beginInclude -->
Laitteet, joissa on EAB:

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |left|
|Vieritä eteenpäin |right|
|Siirrä edelliselle riville |up|
|Siirrä seuraavalle riville |dn|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Lue nykyinen merkki |l1|
|Aktivoi nykyinen navigointiobjekti |l2|
|Lue ikkunan nimi |l1up|
|Lue tilarivi |l2down|
|Siirrä säilöobjektiin |up2|
|Siirrä ensimmäiseen sisältöobjektiin |dn2|
|Siirrä seuraavaan objektiin |right2|
|Siirrä edelliseen objektiin |left2|
|Ilmoita tekstin muotoilutiedot pistesolusta |Ylärivin kosketuskohdistinnäppäimet|

BRAILLEX Tiny:

| Nimi |Näppäinkomento|
|---|---|
|Lue nykyinen merkki |l1|
|Aktivoi nykyinen navigointiobjekti |l2|
|Vieritä taaksepäin |left|
|Vieritä eteenpäin |right|
|Siirrä edelliselle riville |up|
|Siirrä seuraavalle riville |dn|
|Vaihda Pistenäyttö seuraa -asetusta |r2|
|Siirrä säilöobjektiin |r1+up|
|Siirrä ensimmäiseen sisältöobjektiin |r1+dn|
|Siirrä edelliseen objektiin |r1+left|
|Siirrä seuraavaan objektiin |r1+right|
|Lue tekstin muotoilutiedot pistesolusta |ylärivin kosketuskohdistinnäppäimet|
|Lue ikkunan nimi |l1+up|
|Lue tilarivi |l2+down|

BRAILLEX 2D Screen:

| Nimi |Näppäinkomento|
|---|---|
|Lue nykyinen merkki |l1|
|Aktivoi nykyinen navigointiobjekti |l2|
|Vaihda Pistenäyttö seuraa -asetusta |r2|
|Lue tekstin muotoilutiedot pistesolusta |ylärivin kosketuskohdistinnäppäimet|
|Siirrä edelliselle riville |up|
|Vieritä taaksepäin |left|
|Vieritä eteenpäin |right|
|Siirrä seuraavalle riville |dn|
|Siirrä seuraavaan objektiin |left2|
|Siirrä säilöobjektiin |up2|
|Siirrä ensimmäiseen sisältöobjektiin |dn2|
|Siirrä edelliseen objektiin |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA tukee [Humanwaren](https://www.humanware.com) BrailleNote-muistiinpanolaitteita, kun ne toimivat ruudunlukuohjelman pistenäyttönä.
Seuraavia malleja tuetaan:

* BrailleNote Classic (vain sarjaporttiliitäntä)
* BrailleNote PK (sarjaportti- ja Bluetooth-liitännät)
* BrailleNote MPower (sarjaportti- ja Bluetooth-liitännät)
* BrailleNote Apex (USB- ja Bluetooth-liitännät)

Katso BrailleNote Touchin näppäinkomennot [Brailliant BI/B / BrailleNote Touch](#HumanWareBrailliant) -osiosta.

BrailleNote PK:ta lukuun ottamatta sekä pistekirjoitus- (BT) että QWERTY (QT) -näppäimistöä tuetaan.
PC-näppäimistön emulointia ei tueta BrailleNote QT:ssä.
Voit syöttää pistekirjoitusta myös QT-näppäimistöä käyttäen.
Katso lisätietoja BrailleNote-käyttöoppaan pistenäyttökappaleesta.

Käytettävä portti on määritettävä pistenäytön omista asetuksista, jos laitteesi tukee useampaa kuin yhtä liitäntätyyppiä.
Katso lisätietoja BrailleNoten käsikirjasta.
Portin määrittäminen voi olla tarpeen myös NVDA:n [Valitse pistenäyttö](#SelectBrailleDisplay) -valintaikkunassa.
Mikäli laite on liitetty USB:llä tai Bluetoothilla, voidaan portiksi määrittää käytettävissä olevista vaihtoehdoista riippuen "Automaattinen", "USB" tai "Bluetooth".
Jos liitäntänä käytetään sarjaporttia (tai USB-sarjaporttisovitinta) tai jos mikään edellisistä vaihtoehdoista ei ole käytettävissä, on käytettävä yhteysportti valittava sarjaporttiluettelosta.

HumanWaren toimittamat ajurit on asennettava ennen kuin BrailleNote Apex kytketään sen USB-asiakasliitännällä.

BrailleNote Apex BT:ssä voit käyttää pisteiden 1 ja 4 välissä olevaa vieritysrullaa useiden NVDA-komentojen suorittamiseen.
Rulla koostuu neljästä suuntapisteestä, keskellä olevasta napsautuspainikkeesta sekä myötä- ja vastapäivään pyörivästä rullasta.

Seuraavassa on BrailleNoten komentomääritykset NVDA:ta käytettäessä.
Katso laitteen käyttöohjeesta tarkat kuvaukset näppäinten paikoista.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |takaisin|
|Vieritä eteenpäin |eteenpäin|
|Siirrä edelliselle riville |edellinen|
|Siirrä seuraavalle riville |seuraava|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|NVDA-valikko |väli+pisteet 1, 3, 4 ja 5 (väli+n)|
|Vaihda Pistenäyttö seuraa -asetusta |edellinen+seuraava|
|Nuoli ylös -näppäin |väli+piste1|
|Nuoli alas -näppäin |väli+piste4|
|Nuoli vasemmalle -näppäin |väli+piste3|
|Nuoli oikealle -näppäin |väli+piste6|
|Page up -näppäin |väli+piste1+piste3|
|Page down -näppäin |väli+piste4+piste6|
|Home-näppäin |väli+piste1+piste2|
|End-näppäin |väli+piste4+piste5|
|Ctrl+Home-näppäinyhdistelmä |väli+piste1+piste2+piste3|
|Ctrl+End-näppäinyhdistelmä |väli+piste4+piste5+piste6|
|Väli |väli|
|Enter-näppäin |väli+piste8|
|Askelpalautin-näppäin |väli+piste7|
|Sarkain-näppäin |väli+piste2+piste3+piste4+piste5 (väli+t)|
|Vaihto+Sarkain-näppäinyhdistelmä |väli+piste1+piste2+piste5+piste6|
|Windows-näppäin |väli+piste2+piste4+piste5+piste6 (väli+w)|
|Alt-näppäin |väli+piste1+piste3+piste4 (väli+m)|
|Ota näppäinohje käyttöön tai poista se käytöstä |väli+piste2+piste3+piste6 (väli+alempi h)|

Seuraavassa on BrailleNote QT:lle määritellyt komennot, kun se ei ole pistekirjoituksen syöttötilassa.

| Nimi |Näppäinkomento|
|---|---|
|NVDA-valikko |read+n|
|Nuoli ylös -näppäin |nuoli ylös|
|Nuoli alas -näppäin |nuoli alas|
|Nuoli vasemmalle -näppäin |nuoli vasemmalle|
|Nuoli oikealle -näppäin |Nuoli oikealle|
|Page up -näppäinyhdistelmä |function+nuoli ylös|
|Page down -näppäinyhdistelmä |function+nuoli alas|
|Home-näppäin |function+nuoli vasemmalle|
|End-näppäin |function+nuoli oikealle|
|Ctrl+Home-näppäinyhdistelmä |read+t|
|Ctrl+End-näppäinyhdistelmä |read+b|
|Enter-näppäin |enter|
|Askelpalautin-näppäin |backspace|
|Sarkain-näppäin |tab|
|Vaihto+Sarkain-näppäinyhdistelmä |shift+tab|
|Win-näppäin |read+w|
|Alt-näppäin |read+m|
|Ota näppäinohje käyttöön tai poista se käytöstä |read+1|

Seuraavassa on vieritysrullaan määritellyt komennot:

| Nimi |Näppäinkomento|
|---|---|
|Nuoli ylös -näppäin |nuoli ylös|
|Nuoli alas -näppäin |nuoli alas|
|Nuoli vasemmalle -näppäin |nuoli vasemmalle|
|Nuoli oikealle -näppäin |nuoli oikealle|
|Enter-näppäin |keskipainike|
|Sarkain-näppäin |vieritysrulla myötäpäivään|
|Vaihto+Sarkain-näppäinyhdistelmä |vieritysrulla vastapäivään|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA tukee [ONCEn](https://www.once.es/) EcoBraille-pistenäyttöjä.
Seuraavia malleja tuetaan:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

Voit määrittää näytön käyttämän sarjaportin [Valitse pistenäyttö](#SelectBrailleDisplay) -valintaikkunasta.
Nämä näytöt eivät tue NVDA:n automaattista pistenäytön tunnistusta.

Seuraavassa on näiden pistenäyttöjen näppäinmääritykset.
Katso [EcoBraillen käyttöohjeesta](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) kuvaukset näppäinten paikoista.

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |T2|
|Vieritä eteenpäin |T4|
|Siirrä edelliselle riville |T1|
|Siirrä seuraavalle riville |T5|
|Siirrä pistesoluun |kosketuskohdistinnäppäin|
|Aktivoi nykyinen navigointiobjekti |T3|
|Vaihda seuraavaan tarkastelutilaan |F1|
|Siirrä säilöobjektiin |F2|
|Vaihda edelliseen tarkastelutilaan |F3|
|Siirrä edelliseen objektiin |F4|
|Lue nykyinen objekti |F5|
|Siirrä seuraavaan objektiin |F6|
|Siirrä aktiiviseen objektiin |F7|
|Siirrä ensimmäiseen sisältöobjektiin |F8|
|Siirrä järjestelmän kohdistus tai -kohdistin nykyiseen tarkastelukohtaan |F9|
|Lue tarkastelukohdistimen sijainti |F0|
|Vaihda Pistenäyttö seuraa -asetusta |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

SuperBraille-pistenäyttö, jota käytetään enimmäkseen Taiwanissa, voidaan kytkeä tietokoneeseen joko USB:n tai sarjaportin kautta.
Koska laitteessa ei ole fyysisiä kirjoitus- tai vieritysnäppäimiä, kaikki komennot on annettava tietokoneen näppäimistöltä.
Tämän takia, ja jotta säilytetään yhteensopivuus muiden taiwanilaisten ruudunlukuohjelmien kanssa, pistenäytön vierittämistä varten on käytettävissä kaksi komentoa:
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |Laskinnäppäimistön miinus|
|Vieritä eteenpäin |Laskinnäppäimistön plus|

<!-- KC:endInclude -->

### Eurobraille {#Eurobraille}

NVDA tukee Eurobraillen b.book-, b.note-, Esys-, Esytime- ja Iris-pistenäyttöjä.
Näissä laitteissa on 10-näppäiminen pistekirjoitusnäppäimistö.
Katso näppäinten kuvaukset laitteen käyttöohjeesta.
Kahdesta Väli-näppäimen tavoin sijoitellusta näppäimestä vasemmanpuoleinen vastaa Askelpalautinta ja oikea Väli-näppäintä.

Nämä laitteet kytketään USB-liitäntään, janiissä on itsenäinen USB-näppäimistö.
Se voidaan ottaa käyttöön tai poistaa käytöstä vaihtamalla "HID-näppäimistösyötteen simulointi" -asetusta näppäinkomentoa käyttäen.
Alla kuvaillut pistekirjoitusnäppäimistön toiminnot ovat käytettävissä vain, kun "HID-näppäimistösyötteen simulointi" on poistettu käytöstä.

#### Pistekirjoitusnäppäimistön toiminnot {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Poista viimeksi syötetty pistesolu tai merkki |`askelpalautin`|
|Käännä mikä tahansa pistekirjoitussyöte ja paina Enter-näppäintä |`askelpalautin+väli`|
|Vaihda `NVDA`-näppäimen tilaa |`piste 3+piste 5+väli`|
|`Insert`-näppäin |`pisteet 1, 3 ja 5+väli`, `pisteet 3, 4 ja 5+väli`|
|`Delete`-näppäin |`pisteet 3 ja 6+väli`|
|`Home`-näppäin |`pisteet 1, 2, 3+väli`|
|`End`-näppäin |`pisteet 4, 5 ja 6+väli`|
|`Vasen nuolinäppäin` |`piste 2+väli`|
|`Oikea nuolinäppäin` |`piste 5+väli`|
|`Ylänuolinäppäin` |`piste 1+väli`|
|`Alanuolinäppäin` |`piste 6+väli`|
|`Page up` -näppäin |`pisteet 1 ja 3+väli`|
|`Page down` -näppäin |`pisteet 4 ja 6+väli`|
|`Laskinnäppäimistön 1` |`pisteet 1 ja 6+askelpalautin`|
|`Laskinnäppäimistön 2` |`pisteet 1, 2 ja 6+askelpalautin`|
|`Laskinnäppäimistön 3` |`pisteet 1, 4 ja 6+askelpalautin`|
|`Laskinnäppäimistön 4` |`pisteet 1, 4, 5 ja 6+askelpalautin`|
|`Laskinnäppäimistön 5` |`pisteet 1, 5 ja 6+askelpalautin`|
|`Laskinnäppäimistön 6` |`pisteet 1, 2, 4 ja 6+askelpalautin`|
|`Laskinnäppäimistön 7` |`pisteet 1, 2, 4, 5 ja 6+askelpalautin`|
|`Laskinnäppäimistön 8` |`pisteet 1, 2, 5 ja 6+askelpalautin`|
|`Laskinnäppäimistön 9` |`pisteet 2, 4 ja 6+askelpalautin`|
|`Laskinnäppäimistön Insert` |`pisteet 3, 4, 5 ja 6+askelpalautin`|
|`Laskinnäppäimistön pilkku` |`piste 2+askelpalautin`|
|`Laskinnäppäimistön jakomerkki` |`pisteet 3 ja 4+askelpalautin`|
|`Laskinnäppäimistön kertomerkki` |`pisteet 3 ja 5+askelpalautin`|
|`Laskinnäppäimistön miinus` |`pisteet 3 ja 6+askelpalautin`|
|`Laskinnäppäimistön plus` |`pisteet 2, 3 ja 5+askelpalautin`|
|`Laskinnäppäimistön Enter` |`pisteet 3, 4 ja 5+askelpalautin`|
|`Esc`-näppäin |`pisteet 1, 2, 4 ja 5+väli`, `l2`|
|`Sarkain`-näppäin |`pisteet 2, 5 ja 6+väli`, `l3`|
|`Vaihto+Sarkain`-näppäinyhdistelmä |`pisteet 2, 3 ja 5+väli`|
|`PrintScreen`-näppäin |`pisteet 1, 3, 4 ja 6+väli`|
|`Pause`-näppäin |`pisteet 1 ja 4+väli`|
|`Sovellusnäppäin` |`pisteet 5 ja 6+askelpalautin`|
|`F1`-näppäin |`piste 1+askelpalautin`|
|`F2`-näppäin |`pisteet 1 ja 2+askelpalautin`|
|`F3`-näppäin |`pisteet 1 ja 4+askelpalautin`|
|`F4`-näppäin |`pisteet 1, 4 ja 5+askelpalautin`|
|`F5`-näppäin |`pisteet 1 ja 5+askelpalautin`|
|`F6`-näppäin |`pisteet 1, 2 ja 4+askelpalautin`|
|`F7`-näppäin |`pisteet 1, 2, 4 ja 5+askelpalautin`|
|`F8`-näppäin |`pisteet 1, 2 ja 5+askelpalautin`|
|`F9`-näppäin |`pisteet 2 ja 4+askelpalautin`|
|`F10`-näppäin |`pisteet 2, 4 ja 5+askelpalautin`|
|`F11`-näppäin |`pisteet 1 ja 3+askelpalautin`|
|`F12`-näppäin |`pisteet 1, 2 ja 3+askelpalautin`|
|`Windows`-näppäin |`pisteet 1, 2, 4, 5 ja 6+väli`|
|Vaihda `Windows`-näppäimen tilaa |`pisteet 1, 2, 3 ja 4+askelpalautin`, `pisteet 2, 4, 5 ja 6+väli`|
|`CapsLock`-näppäin |`piste 7+askelpalautin`, `piste 8+askelpalautin`|
|`NumLock`-näppäin |`piste 3+askelpalautin`, `piste 6+askelpalautin`|
|`Vaihto`-näppäin |`piste 7+väli`|
|Vaihda `Vaihto`-näppäimen tilaa |`pisteet 1 ja 7+väli`, `pisteet 4 ja 7+väli`|
|`Ctrl`-näppäin |`pisteet 7 ja 8+väli`|
|Vaihda `Ctrl`-näppäimen tilaa |`pisteet 1, 7 ja 8+väli`, `pisteet 4, 7 ja 8+väli`|
|`Alt`-näppäin |`piste 8+väli`|
|Vaihda `Alt`-näppäimen tilaa |`pisteet 1 ja 8+väli`, `pisteet 4 ja 8+väli`|
|Vaihda HID-näppäimistösyötteen simuloinnin asetusta |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### B.bookin näppäinkomennot {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |`backward`|
|Vieritä eteenpäin |`forward`|
|Siirrä nykyiseen kohdistukseen |`backward+forward`|
|Siirrä pistesoluun |`kosketuskohdistinnäppäin`|
|`Vasen nuolinäppäin` |`joystick2Left`|
|`Oikea nuolinäppäin` |`joystick2Right`|
|`Ylänuolinäppäin` |`joystick2Up`|
|`Alanuolinäppäin` |`joystick2Down`|
|`Enter`-näppäin |`joystick2Center`|
|`Esc`-näppäin |`c1`|
|`Sarkain`-näppäin |`c2`|
|Vaihda `Vaihto`-näppäimen tilaa |`c3`|
|Vaihda `Ctrl`-näppäimen tilaa |`c4`|
|Vaihda `Alt`-näppäimen tilaa |`c5`|
|Vaihda `NVDA`-näppäimen tilaa |`c6`|
|`Ctrl+Home`-näppäinyhdistelmä |`c1+c2+c3`|
|`Ctrl+End`-näppäinyhdistelmä |`c4+c5+c6`|

<!-- KC:endInclude -->

#### B.noten näppäinkomennot {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |`leftKeypadLeft`|
|Vieritä eteenpäin |`leftKeypadRight`|
|Siirrä pistesoluun |`routing`|
|Lue tekstin muotoilutiedot pistesolusta |`doubleRouting`|
|Siirrä seuraavalle riville |`leftKeypadDown`|
|Vaihda edelliseen tarkastelutilaan |`leftKeypadLeft+leftKeypadUp`|
|Vaihda seuraavaan tarkastelutilaan |`leftKeypadRight+leftKeypadDown`|
|`Vasen nuolinäppäin` |`rightKeypadLeft`|
|`Oikea nuolinäppäin` |`rightKeypadRight`|
|`Ylänuolinäppäin` |`rightKeypadUp`|
|`Alanuolinäppäin` |`rightKeypadDown`|
|`Ctrl+Home`-näppäinyhdistelmä |`rightKeypadLeft+rightKeypadUp`|
|`Ctrl+End`-näppäinyhdistelmä |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Esysin näppäinkomennot {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |`switch1Left`|
|Vieritä eteenpäin |`switch1Right`|
|Siirrä nykyiseen kohdistukseen |`switch1Center`|
|Siirrä pistesoluun |`routing`|
|Lue tekstin muotoilutiedot pistesolusta |`doubleRouting`|
|Siirrä edelliselle riville |`joystick1Up`|
|Siirrä seuraavalle riville |`joystick1Down`|
|Siirrä edelliseen merkkiin |`joystick1Left`|
|Siirrä seuraavaan merkkiin |`joystick1Right`|
|`Vasen nuolinäppäin` |`joystick2Left`|
|`Oikea nuolinäppäin` |`joystick2Right`|
|`Ylänuolinäppäin` |`joystick2Up`|
|`Alanuolinäppäin` |`joystick2Down`|
|`Enter`-näppäin |`joystick2Center`|

<!-- KC:endInclude -->

#### Esytimen näppäinkomennot {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |`l1`|
|Vieritä eteenpäin |`l8`|
|Siirrä nykyiseen kohdistukseen |`l1+l8`|
|Siirrä pistesoluun |`routing`|
|Lue tekstin muotoilutiedot pistesolusta |`doubleRouting`|
|Siirrä edelliselle riville |`joystick1Up`|
|Siirrä seuraavalle riville |`joystick1Down`|
|Siirrä edelliseen merkkiin |`joystick1Left`|
|Siirrä seuraavaan merkkiin |`joystick1Right`|
|`Vasen nuolinäppäin` |`joystick2Left`|
|`Oikea nuolinäppäin` |`joystick2Right`|
|`Ylänuolinäppäin` |`joystick2Up`|
|`Alanuolinäppäin` |`joystick2Down`|
|`Enter`-näppäin |`joystick2Center`|
|`Esc`-näppäin |`l2`|
|`Sarkain`-näppäin |`l3`|
|Vaihda `Vaihto`-näppäimen tilaa |`l4`|
|Vaihda `Ctrl`-näppäimen tilaa |`l5`|
|Vaihda `Alt`-näppäimen tilaa |`l6`|
|Vaihda `NVDA`-näppäimen tilaa |`l7`|
|`Ctrl+Home`-näppäinyhdistelmä |`l1+l2+l3`, `l2+l3+l4`|
|`Ctrl+End`-näppäinyhdistelmä |`l6+l7+l8`, `l5+l6+l7`|
|Vaihda HID-näppäimistösyötteen simuloinnin asetusta |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Nattiq nBraille {#NattiqTechnologies}

NVDA tukee [Nattiq Technologiesin](https://www.nattiq.com/) pistenäyttöjä USB-liitäntää käytettäessä.
Windows 10 ja uudemmat tunnistavat näytön tietokoneeseen yhdistettäessä, mutta vanhempia Windows-versioita käytettäessä saatat joutua asentamaan USB-ajurit.
Voit hakea ne valmistajan kotisivulta.

Seuraavassa ovat Nattiq Technologiesin pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso kuvaukset näppäinten paikoista laitteen käyttöohjeesta.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |ylös|
|Vieritä eteenpäin |alas|
|Siirrä edelliselle riville |vasen|
|Siirrä seuraavalle riville |oikea|
|Siirrä pistesoluun |kosketuskohdistinnäppäimet|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) on erillinen ohjelma, jonka avulla on mahdollista käyttää entistä useampia pistenäyttöjä.
Sen käyttämiseksi on asennettava [BRLTTY:n Windows-versio](https://www.brltty.app/download.html).
On suositeltavaa asentaa uusin versio, jonka tiedostonimi on esimerkiksi brltty-win-4.2-2.exe.
Käytettävää pistenäyttöä ja porttia määritettäessä on syytä kiinnittää tarkasti huomiota ohjeisiin, erityisesti jos käytetään USB-pistenäyttöä ja mikäli valmistajan ajurit on jo asennettu.

BRLTTY huolehtii tällä hetkellä itse pistesyötöstä näytöissä, joissa on pistenäppäimistö.
Tämän takia NVDA:n syöttötaulukkoasetuksella ei ole merkitystä.

BRLTTY ei tue NVDA:n automaattista pistenäytön tunnistusta.

Seuraavassa on BRLTTY:n näppäinkomennot NVDA:ta käytettäessä.
Katso [BRLTTY:n näppäinsidosluetteloista](https://brltty.app/doc/KeyBindings/) tietoja BRLTTY:n komentojen määrittämisestä pistenäyttöjen näppäimiin.
<!-- KC:beginInclude -->

| Nimi |BRLTTY-komento|
|---|---|
|Vieritä taaksepäin |`fwinlt` (siirry yksi ikkuna vasemmalle)|
|Vieritä eteenpäin |`fwinrt` (siirry yksi ikkuna oikealle)|
|Siirrä edelliselle riville |`lnup` (siirry yksi rivi ylöspäin)|
|Siirrä seuraavalle riville |`lndn` (siirry yksi rivi alaspäin)|
|siirrä pistesoluun |`route` (siirrä kohdistin merkin kohdalle)|
|Ota näppäinohje käyttöön tai poista se käytöstä |`learn` (siirry näppäinohjetilaan tai poistu siitä)|
|Avaa NVDA-valikko |`prefmenu` (avaa NVDA-valikko tai poistu siitä)|
|Palauta asetukset |`prefload` (palauta asetukset levyltä)|
|Tallenna asetukset |`prefsave` (tallenna asetukset levylle)|
|Ilmoita kellonaika |`time` (näytä nykyinen päivämäärä ja kellonaika)|
|Lue rivi, jolla tarkastelukohdistin on |`say_line` (puhu nykyinen rivi)|
|Jatkuva luku |`say_below` (puhu nykyiseltä riviltä lähtien näytön alareunaan saakka)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Suomalaisia Tivomaticin Caiku Albatross -pistenäyttöjä voidaan käyttää joko USB:n tai sarjaportin kautta.
Laitteita varten ei tarvitse asentaa ajureita.
Yhdistä vain laite tietokoneeseen ja määritä NVDA käyttämään sitä.

Huom: Siirtonopeuden 19200 käyttöä suositellaan vahvasti.
Vaihda tarvittaessa siirtonopeudeksi 19200 pistenäytön valikosta.
Vaikka ajuri tukee 9600 baudin siirtonopeutta, se ei voi vaikuttaa pistenäytön käyttämään siirtonopeuteen.
Koska 19200 on pistenäytön oletussiirtonopeus, ajuri kokeilee sitä ensin.
Jos siirtonopeudet eivät ole samat, ajuri voi käyttäytyä odottamattomasti.

Seuraavassa on näiden pistenäyttöjen näppäinkomennot NVDA:ta käytettäessä.
Katso laitteen käyttöohjeesta kuvaukset näppäinten paikoista.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Siirrä ylimmälle riville |`home1`, `home2`|
|Siirrä alimmalle riville |`end1`, `end2`|
|Siirrä aktiiviseen objektiin |`eCursor1`, `eCursor2`|
|Siirrä nykyiseen kohdistukseen |`cursor1`, `cursor2`|
|Siirtää hiiren nykyiseen navigointiobjektiin |`home1+home2`|
|Siirtää navigointiobjektin hiiren alla olevaan objektiin ja lukee sen |`end1+end2`|
|Siirrä järjestelmän kohdistus tai -kohdistin tarkastelukohtaan |`eCursor1+eCursor2`|
|Vaihda Pistenäyttö seuraa -asetusta |`cursor1+cursor2`|
|Siirrä edelliselle riville |`up1`, `up2`, `up3`|
|Siirrä seuraavalle riville |`down1`, `down2`, `down3`|
|Vieritä taaksepäin |`left`, `lWheelLeft`, `rWheelLeft`|
|Vieritä eteenpäin |`right`, `lWheelRight`, `rWheelRight`|
|Siirrä pistesoluun |`kosketuskohdistinnäppäin`|
|Ilmoita muotoilutiedot pistesolusta |`toissijainen kosketuskohdistinnäppäin`|
|Vaihda tapaa, jolla kontekstitiedot näytetään pistenäytöllä |`attribute1+attribute3`|
|Vaihda puhetilaa |`attribute2+attribute4`|
|Vaihda edelliseen tarkastelutilaan |`f1`|
|Vaihda seuraavaan tarkastelutilaan |`f2`|
|Siirrä säilöobjektiin |`f3`|
|Siirrä ensimmäiseen sisältöobjektiin |`f4`|
|Siirrä edelliseen objektiin |`f5`|
|Siirrä seuraavaan objektiin |`f6`|
|Lue nykyinen objekti |`f7`|
|Lue tarkastelukohdistimen kohdalla olevan tekstin tai objektin sijaintitiedot |`f8`|
|Näytä pistekirjoituksen asetukset |`f1+home1`, `f9+home2`|
|Lue tilarivi ja siirrä navigointiobjekti siihen |`f1+end1`, `f9+end2`|
|Vaihda pistekohdistimen muotoa |`f1+eCursor1`, `f9+eCursor2`|
|Ota pistekohdistin käyttöön tai poista se käytöstä |`f1+cursor1`, `f9+cursor2`|
|Vaihda Näytä ilmoitukset -asetusta |`f1+f2`, `f9+f10`|
|Vaihda Näytä valinnan tila -asetusta |`f1+f5`, `f9+f14`|
|Vaihda "Siirrä järjestelmäkohdistin tarkastelukohdistimen kohdalle pistenäytön kosketuskohdistinnäppäimillä" -asetuksen tilaa |`f1+f3`, `f9+f11`|
|Aktivoi nykyinen navigointiobjekti |`f7+f8`|
|Lue päiväys/aika |`f9`|
|Ilmoittaa akun tilan ja jäljellä olevan ajan, jos verkkovirta ei ole käytössä |`f10`|
|Lue ikkunan nimi |`f11`|
|Lue tilarivi |`f12`|
|Lue nykyinen rivi |`f13`|
|Lue nykyinen teksti loppuun saakka järjestelmäkohdistimesta lähtien siirtäen samalla sitä |`f14`|
|Lue merkki, jonka kohdalla tarkastelukohdistin on nykyisessä navigointiobjektissa |`f15`|
|Lue nykyisen navigointiobjektin rivi, jolla tarkastelukohdistin on |`f16`|
|Lue nykyisen navigointiobjektin sana, jonka kohdalla tarkastelukohdistin on |`f15+f16`|
|Siirrä tarkastelukohdistin nykyisen navigointiobjektin edelliselle riville ja lue se |`lWheelUp`, `rWheelUp`|
|Siirrä tarkastelukohdistin nykyisen navigointiobjektin seuraavalle riville ja lue se |`lWheelDown`, `rWheelDown`|
|`Windows+D` (pienennä kaikki sovellukset) |`attribute1`|
|`Windows+E` (tämä tietokone) |`attribute2`|
|`Windows+B` (siirrä kohdistus ilmaisinalueelle) |`attribute3`|
|`Windows+I` (Windowsin asetukset) |`attribute4`|

<!-- KC:endInclude -->

### HID Braille -pistenäytöt {#HIDBraille}

Tämä on kokeellinen ajuri uudelle HID Braille -protokollalle, josta Microsoft, Google, Apple ja useat avustavan teknologian yritykset, mukaan lukien NV Access, sopivat vuonna 2018.
Toiveissa on, että kaikkien valmistajien tulevat pistenäyttömallit käyttäisivät tätä vakioprotokollaa, joka poistaisi valmistajakohtaisten pistenäyttöajureiden tarpeen.

NVDA:n automaattinen pistenäytön tunnistus tunnistaa myös kaikki tätä protokollaa tukevat näytöt.

Seuraavassa ovat näiden näyttöjen näppäinkomennot NVDA:ta käytettäessä.
<!-- KC:beginInclude -->

| Nimi |Näppäinkomento|
|---|---|
|Vieritä taaksepäin |panoroi vasemmalle tai keinunäppäin ylös|
|Vieritä eteenpäin |panoroi oikealle tai keinunäppäin alas|
|Siirrä pistesoluun |kohdistimensiirtonäppäinsarja 1|
|Vaihda Piste näyttö seuraa -asetusta |ylös+alas|
|Ylänuolinäppäin |ohjaussauva ylös, dpad ylös tai väli+piste 1|
|Alanuolinäppäin |ohjaussauva alas, dpad alas tai väli+piste 4|
|Vasen nuolinäppäin |väli+piste 3, ohjaussauva vasemmalle tai dpad vasemmalle|
|Oikea nuolinäppäin |väli+piste 6, ohjaussauva oikealle tai dpad oikealle|
|Vaihto+Sarkain-näppäinyhdistelmä |väli+pisteet 1ja 3|
|Sarkain-näppäin |väli+pisteet 4 ja 6|
|Alt-näppäin |väli+pisteet 1, 3 ja 4 (väli+m)|
|Esc-näppäin |väli+pisteet 1 ja 5 (väli+e)|
|Enter-näppäin |piste 8, ohjaussauvan keskikohta tai dpadin keskikohta|
|Windows-näppäin |väli+pisteet 3 ja 4|
|Alt+Sarkain-näppäinyhdistelmä |väli+pisteet 2, 3, 4 ja 5 (väli+t)|
|NVDA-valikko |väli+pisteet 1, 3, 4 ja 5 (väli+n)|
|Windows+D-näppäinyhdistelmä (pienennä kaikki sovellukset) |väli+pisteet 1, 4 ja 5 (väli+d)|
|Jatkuva luku |väli+pisteet 1, 2, 3, 4, 5 ja 6|

<!-- KC:endInclude -->

## Edistyneet aiheet {#AdvancedTopics}
### Suojattu tila {#SecureMode}

Järjestelmänvalvojat voivat halutessaan määrittää NVDA:n rajoittamaan luvatonta järjestelmän käyttöä.
NVDA sallii mukautettujen lisäosien asentamisen, jotka voivat suorittaa mielivaltaista koodia, mukaan lukien silloin kun NVDA:lla on järjestelmänvalvojan oikeudet.
NVDA sallii myös käyttäjien suorittaa mielivaltaista koodia Python-konsolin kautta.
Suojattu tila estää käyttäjiä muokkaamasta NVDA:n asetuksia ja rajoittaa muutenkin luvatonta järjestelmän käyttöä.

NVDA on käynnissä suojatussa tilassa, kun se suoritetaan [suojatuissa ruuduissa](#SecureScreens), ellei [järjestelmänlaajuista parametria](#SystemWideParameters) `serviceDebug` ole otettu käyttöön.
Käynnistä NVDA aina suojatussa tilassa määrittämällä [järjestelmänlaajuinen parametri](#SystemWideParameters) `forceSecureMode`.
NVDA voidaan käynnistää suojatussa tilassa myös `-s`-[komentorivivalitsimella](#CommandLineOptions).

Suojattu tila poistaa käytöstä:

* NVDA:n omien ja muiden asetusten tallentamisen levylle
* Näppäinkomentokartan tallentamisen levylle
* [Asetusprofiilien](#ConfigurationProfiles) ominaisuudet, kuten luonnin, poiston, uudelleennimeämisen jne.
* Mukautettujen asetuskansioiden lataaminen [`-c`-komentorivivalitsinta](#CommandLineOptions) käyttäen
* NVDA:n päivittämisen ja massamuistiversion luonnin
* [Lisäosakaupan](#AddonsManager)
* [Python-konsolin](#PythonConsole)
* [Lokintarkastelun](#LogViewer) ja lokiin tallentamisen
* [Pistekirjoituksen tarkastelun](#BrailleViewer) ja [Puheen tarkastelun](#SpeechViewer)
* Ulkoisten asiakirjojen, kuten käyttöoppaan tai tekijät-tiedoston avaamisen NVDA-valikosta

NVDA:n asennetut versiot tallentavat asetuksensa, lisäosat mukaan lukien, hakemistoon `%APPDATA%\nvda`.
Estä NVDA-käyttäjiä muokkaamasta asetuksiaan tai lisäosiaan rajoittamalla heidän käyttöoikeuksiaan tähän kansioon.

Suojattu tila ei ole tehokas NVDA:n massamuistiversioissa.
Tämä rajoitus koskee myös tilapäisversiota, joka käynnistyy NVDA:n asennusohjelman käynnistyessä.
Mahdollisuus massamuistiversion käynnistämiseen turvallisissa ympäristöissä muodostaa saman turvallisuusriskin riippumatta siitä, onko suojattu tila käytössä.
Järjestelmänvalvojien odotetaan rajoittavan luvattomien ohjelmien suorittamista järjestelmissään, NVDA:n massamuistiversiot mukaan lukien.

NVDA-käyttäjät luottavat usein siihen, että voivat mukauttaa NVDA-profiiliaan omiin tarpeisiinsa sopivaksi.
Tähän saattaa sisältyä mukautettujen lisäosien asentaminen ja asetusten määritys, jotka tulisi tarkistaa erikseen NVDA:sta.
Suojattu tila jäädyttää NVDA:n asetuksiin tehdyt muutokset, joten varmista, että NVDA on määritetty asianmukaisesti ennen suojatun tilan käyttöönottoa.

### Suojatut ruudut {#SecureScreens}

NVDA on käynnissä [suojatussa tilassa](#SecureMode), kun se suoritetaan suojatuissa ruuduissa, ellei [järjestelmänlaajuista parametria](#SystemWideParameters) `serviceDebug` ole otettu käyttöön.

NVDA käyttää järjestelmäprofiilia asetuksia varten ollessaan käynnissä suojatussa ruudussa.
NVDA:n käyttäjäasetukset voidaan kopioida [suojatuissa ruuduissa käytettäväksi](#GeneralSettingsCopySettings).

Suojattuja ruutuja ovat:

* Windowsin kirjautumisruutu
* Käyttäjätilien valvonnan valintaikkuna, (aktiivinen suoritettaessa toimintoa järjestelmänvalvojana)
  * Tämä sisältää ohjelmien asentamisen

### Komentorivivalitsimet {#CommandLineOptions}

NVDA hyväksyy käynnistyessään yhden tai useamman toimintaansa vaikuttavan komentorivivalitsimen.
Voit käyttää kerralla niin monta valitsinta kuin tarvitset.
Valitsimet voidaan antaa pikakuvakkeesta käynnistettäessä (syötetään kuvakkeen Ominaisuudet-valintaikkunassa olevaan Kohde-kenttään), Suorita-valintaikkunasta (Käynnistä-valikko -> Suorita tai Windows+R) tai Windowsin komentokonsolista.
Valitsimet erotetaan NVDA:n ohjelmatiedoston nimestä ja toisistaan välilyönnillä.
Hyödyllinen valitsin on esim. `--disable-addons`, joka poistaa kaikki lisäosat käytöstä.
Sen avulla voit selvittää, aiheuttaako jokin lisäosa ongelmia.

Voit esimerkiksi sulkea NVDA:n nykyisen version kirjoittamalla seuraavan komennon Suorita-valintaikkunaan:

    nvda -q

Joistakin komentorivivalitsimista on sekä lyhyt että pitkä muoto, kun taas joistakin on vain pitkä.
Voit yhdistellä lyhyitä valitsimia näin:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc ASETUSPOLKU` |Tämä käynnistää NVDA:n poistaen käytöstä sekä käynnistysäänen että -ilmoituksen, ja käyttää määritetyssä hakemistossa olevia asetuksia.|
|`nvda -mc ASETUSPOLKU --disable-addons` |Muuten sama kuin edellä, mutta poistaa myös lisäosat käytöstä.|

Jotkin valitsimet hyväksyvät lisäparametreja, esim. miten yksityiskohtaisia tietoja lokiin tallennetaan tai käyttäjän asetushakemiston polkumäärityksen.
Parametrit annetaan valitsimen jälkeen ja erotetaan sen lyhyestä muodosta välilyönnillä tai pitkää muotoa käytettäessä yhtä suuri kuin -merkillä (`=`), esim.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Käynnistää NVDA:n virheenkorjaus-lokitasolla.|
|`nvda --log-file=c:\nvda.log` |NVDA tallentaa lokin tiedostoon c:\nvda.log.|
|`nvda --log-level=20 -f c:\nvda.log` |Käynnistää NVDA:n tiedot-lokitasolla ja tallentaa lokin tiedostoon c:\nvda.log.|

Seuraavassa on luettelo NVDA:n komentorivivalitsimista:

| Lyhyt |Pitkä |Kuvaus|
|---|---|---|
|`-h` |`--help` |Näyttää komentorivivalitsimien ohjeen.|
|`-q` |`--quit` |Sulkee jo käynnissä olevan NVDA:n version.|
|`-k` |`--check-running` |Ilmoittaa lopetuskoodilla, onko NVDA käynnissä, 0 = jos käynnissä tai 1 = jos ei käynnissä.|
|`-f LOKITIEDOSTO` |`--log-file=LOKITIEDOSTO` |Tiedosto, johon lokiviestit tallennetaan. Lokin tallennus on aina poissa käytöstä, jos suojattu tila on käytössä.|
|`-l LOKITASO` |`--log-level=LOKITASO` |Alin taso, jonka viestit tallennetaan lokiin (virheenkorjaus = 10, syöttö/tulostus = 12, virheenkorjausvaroitus = 15, tiedot = 20, ei käytössä = 100). Lokin tallennus on aina poissa käytöstä, jos suojattu tila on käytössä.|
|`-c ASETUSPOLKU` |`--config-path=ASETUSPOLKU` |Hakemistopolku, johon kaikki NVDA:n asetukset tallennetaan. Oletusarvo pakotetaan, jos suojattu tila on käytössä.|
|Ei mitään |`--lang=KIELI` |Ohita NVDA:n asetuksissa määritetty kieli. Määritä kieleksi "Windows" käyttääksesi nykyistä käyttäjän oletusarvoa, "en" englantia jne.|
|`-m` |`--minimal` |Ei ääniä, käyttöliittymää tai käynnistysilmoitusta jne.|
|`-s` |`--secure` |Käynnistää NVDA:n [suojatussa tilassa](#SecureMode).|
|Ei mitään |`--disable-addons` |Poistaa lisäosat käytöstä.|
|Ei mitään |`--debug-logging` |Ottaa käyttöön virheenkorjaus-lokitason vain nykyisessä istunnossa. Tämä asetus korvaa minkä tahansa muun annetun lokitason argumentin (`--loglevel`, `-l`), lokin käytöstä poistava valitsin mukaan lukien.|
|Ei mitään |`--no-logging` |Poistaa lokin kokonaan käytöstä NVDA:ta käytettäessä. Tämä asetus voidaan ohittaa, mikäli lokitaso (`--loglevel`, `-l`) määritetään komentoriviparametrilla tai jos virheenkorjauslokin tallennus otetaan käyttöön.|
|Ei mitään |`--no-sr-flag` |Ei muuta järjestelmänlaajuista ruudunlukijalippua.|
|Ei mitään |`--install` |Asentaa NVDA:n ja käynnistää asennetun kopion.|
|Ei mitään |`--install-silent` |Asentaa NVDA:n ilman kehotteita ja asennetun kopion käynnistämistä.|
|Ei mitään |`--enable-start-on-logon=True|False` |Ottaa asennettaessa käyttöön NVDA:n [Käytä sisäänkirjautumisen aikana -asetuksen.](#StartAtWindowsLogon)|
|Ei mitään |`--copy-portable-config` |Kopioi asennettaessa massamuistiversion asetukset annetusta hakemistopolusta (`--config-path`, `-c`) nykyiseen käyttäjätiliin.|
|Ei mitään |`--create-portable` |Luo ja käynnistää NVDA:n massamuistiversion. Parametri `--portable-path` on myös määritettävä.|
|Ei mitään |`--create-portable-silent` |Luo NVDA:n massamuistiversion eikä käynnistä sitä luonnin jälkeen. Parametri `--portable-path` on myös määritettävä.|
|Ei mitään |`--portable-path=POLKU` |Hakemistopolku, johon massamuistiversio luodaan.|

### Järjestelmänlaajuiset parametrit {#SystemWideParameters}

Windowsin rekisterissä on mahdollista muuttaa joitakin arvoja, jotka vaikuttavat NVDA:n järjestelmänlaajuiseen toimintaan.
Arvot tallennetaan johonkin seuraavista rekisteriavaimista:

* 32-bittiset järjestelmät: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* 64-bittiset järjestelmät: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

Seuraavien rekisteriavainten määrittäminen on mahdollista:

| Nimi |Tyyppi |Mahdolliset arvot |Kuvaus|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 = ei käytössä (oletus), 1 = käytössä |Jos tämä otetaan käyttöön, NVDA:n asetukset tallennetaan paikallisen sovellusdatan hakemistoon roaming-hakemistossa sijaitsevan sovellusdatakansion asemesta.|
|`serviceDebug` |DWORD |0 = ei käytössä (oletus), 1 = käytössä |Jos tämä asetus otetaan käyttöön, [suojattu tila](#SecureMode) poistetaan käytöstä [suojatuissa ruuduissa](#SecureScreens). Tämän asetuksen käyttöä ei suositella tietoturvan merkittävän heikkenemisen vuoksi.|
|`forceSecureMode` |DWORD |0 = ei käytössä (oletus), 1 = käytössä |Jos tämä otetaan käyttöön, [suojattu tila](#SecureMode) pakotetaan käyttöön NVDA:ta käytettäessä.|

## Lisätietoja {#FurtherInformation}

Mikäli tarvitset lisätietoja tai neuvoja NVDA:han liittyen, vieraile [projektin verkkosivulla](NVDA_URL).
Löydät sieltä lisäohjeita sekä teknistä tukea ja yhteisöresursseja.
Sivustolla on myös NVDA:n kehitykseen liittyvää tietoa.

