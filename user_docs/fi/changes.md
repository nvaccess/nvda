# Mitä uutta NVDA:ssa


## 2024.2

Lisätty äänijakotoiminto.
Se mahdollistaa NVDA:n äänien jakamisen yhteen kanavaan (esim. vasempaan), kun taas muiden sovellusten äänet ohjataan toiseen (esim. oikeaan).

Lisätty syntetisaattorin asetusrenkaan komentoja, jotka mahdollistavat ensimmäiseen tai viimeiseen asetukseen siirtymisen sekä aktiivisen asetuksen suurentamisen tai pienentämisen  enemmän kerrallaan.
Lisätty uusia pikanavigointikomentoja: tekstikappale, pystysuunnassa tasattu kappale, samantyylinen teksti, eri tyylinen teksti, valikkokohde, vaihtopainike, edistymispalkki, kuva sekä matemaattinen kaava.

Useita uusia pistekirjoitusominaisuuksia sekä bugikorjauksia.
Lisätty "näytä puhetuloste" -pistekirjoitustila.
Kun se on käytössä, pistenäytöllä näytetään, mitä NVDA puhuu.
Lisätty tuki Braille Edge S2- ja Braille Edge S3 -pistenäytöille.
Päivitetty LibLouis, johon on lisätty uudet yksityiskohtaiset valkovenäläiset ja ukrainalaiset pistetaulukot (isot kirjaimet näytetään), laosilainen sekä espanjalainen taulukko kreikkalaisten tekstien lukemista varten.

Päivitetty eSpeak, johon on lisätty tigrinjan kieli.

Tehty useita pieniä bugikorjauksia sovelluksille, kuten Thunderbirdille, Adobe Readerille, verkkoselaimille, Nudille sekä Geekbenchille.

### Uudet ominaisuudet

* Uusia näppäinkomentoja:
  * Uusi pikanavigointikomento `P` seuraavaan ja `Vaihto+P` edelliseen tekstikappaleeseen siirtymistä varten selaustilassa. (#15998, @mltony)
  * Uusia määrittämättömiä pikanavigointikomentoja, joita käyttäen voidaan siirtyä seuraavaan/edelliseen:
    * kuvaan (#10826)
    * pystysuunnassa tasattuun kappaleeseen (#15999, @mltony)
    * valikkokohteeseen (#16001, @mltony)
    * vaihtopainikkeeseen (#16001, @mltony)
    * edistymispalkkiin (#16001, @mltony)
    * matemaattiseen kaavaan (#16001, @mltony)
    * samantyyliseen tekstiin (#16000, @mltony)
    * eri tyyliseen tekstiin (#16000, @mltony)
    * Lisätty komennot syntetisaattorin asetusrenkaan ensimmäiseen ja viimeiseen asetukseen sekä eteen- ja taaksepäin siirtymistä varten. (#13768, #16095, @rmcpantoja)
    * Ensimmäiseen ja viimeiseen asetukseen siirtymiselle ei ole määritetty näppäinkomentoa. (#13768)
    * Pienennä ja suurenna syntetisaattorin asetusrenkaan aktiivista asetusta enemmän kerrallaan (#13768):
      * Pöytäkone: `NVDA+Ctrl+Page up` tai `NVDA+Ctrl+Page down`.
      * Kannettava: `NVDA+Ctrl+Vaihto+Page up` tai `NVDA+Ctrl+Vaihto+Page down`.
  * Lisätty uusi määrittämätön näppäinkomento kuvien ja kuvatekstien puhumisen käyttöönottamista tai käytöstä poistamista varten. (#10826, #14349)
* Pistekirjoitus:
  * Lisätty tuki Braille Edge S2- ja Braille Edge S3 -pistenäytöille. (#16033, #16279, @EdKweon)
  * Lisätty uusi "näytä puhetuloste" -pistekirjoitustila. (#15898, @Emil-18)
    * Kun se on käytössä, pistenäytöllä näytetään, mitä NVDA puhuu.
    * Asetuksen tilaa voidaan vaihtaa painamalla `NVDA+Alt+T` tai pistekirjoitusasetusten paneelista.
* Äänijako: (#12985, @mltony)
  * Mahdollistaa NVDA:n äänien jakamisen yhteen kanavaan (esim. vasempaan), kun taas kaikkien muiden sovellusten äänet ohjataan toiseen (esim. oikeaan).
  * Otetaan käyttöön tai poistetaan käytöstä näppäinkomennolla `NVDA+Alt+S`.
* Rivi- ja sarakeotsikoiden puhumista tuetaan nyt contenteditable-HTML-elementeissä. (#14113)
* Lisätty asiakirjojen muotoiluasetuksiin asetus kuvien ja kuvatekstien puhumisen käytöstä poistamiselle. (#10826, #14349)
* NVDA puhuu Windows 11:n 2022 Update -versiossa ja sitä uudemmissa puheentunnistuksen ja ehdotettujen toimintojen ilmoitukset, paras ehdotus mukaan lukien, kun leikepöydälle kopioidaan esim. puhelinnumeroita. (#16009, @josephsl)
* NVDA pitää äänilaitteen (esim. Bluetooth-kuulokkeet) hereillä puheen loppumisen jälkeen estääkseen seuraavan puhutun asian alun leikkautumisen. (#14386, @jcsteh, @mltony)
* HP Secure Browser -verkkoselainta tuetaan. (#16377)

### Muutokset

* Lisäosakauppa:
  * Lisäosan tiedot NVDA:n vähimmäis- ja viimeisimmästä testatusta versiosta näytetään nyt "Muita tietoja" -osiossa. (#15776, @Nael-Sayegh)
  * Lisäosan arviointitoiminto on käytettävissä ja arviointien verkkosivu näytetään Tiedot-paneelissa lisäosakaupan kaikissa välilehdissä. (#16179, @nvdaes)
* Päivitetyt komponentit:
  * Päivitetty LibLouis-pistekääntäjä versioksi [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Uudet yksityiskohtaiset valkovenäläiset ja ukrainalaiset pistetaulukot (isot kirjaimet näytetään).
    * Espanjalainen pistetaulukko kreikkalaisten tekstien lukemista varten.
    * Uusi laosilainen tason 1 pistetaulukko. (#16470)
  * eSpeak NG on päivitetty versioksi 1.52-dev muutos `cb62d93fd7`. (#15913)
    * Lisätty tigrinjan kieli. 
* Muutettu useita BrailleSense-pistenäyttöjen komentoja, jotta vältetään ristiriidat ranskalaisten pistekirjoitusmerkkien kanssa. (#15306)
  * `Alt+Nuoli vasemmalle` on nyt `pisteet 2 ja 7+väli`
  * `Alt+Nuoli oikealle` on nyt `pisteet 5 ja 7+väli`
  * `Alt+Nuoli ylös` on nyt `pisteet 2, 3 ja 7+väli`
  * `Alt+Nuoli alas` on nyt `pisteet 5, 6 ja 7+väli`
* Täytepisteitä, joita yleisesti käytetään sisällysluetteloissa, ei enää puhuta alhaisilla välimerkkitasoilla. (#15845, @CyrilleB79)

### Bugikorjaukset

* Windows 11:n korjaukset:
  * NVDA puhuu jälleen fyysisen näppäimistön syöttöehdotukset. (#16283, @josephsl)
  * Hiirtä ja kosketusvuorovaikutusta voidaan käyttää pika-asetuksissa versiossa 24H2 (2024 Update ja Windows Server 2025). (#16348, @josephsl)
* Lisäosakauppa:
  * Kohdistus siirtyy asianmukaisesti uuteen senhetkiseen välilehden otsikkoon painettaessa `Ctrl+Sarkain`. (#14986, @ABuffEr)
  * NVDA ei käynnisty enää uudelleen, jos välimuistitiedostot ovat virheellisiä. (#16362, @nvdaes)
* Korjaukset Chromium-pohjaisille selaimille UIA:ta käytettäessä:
  * Korjattu NVDA:n jumiutumisen aiheuttaneet bugit. (#16393, #16394)
  * Askelpalautin-näppäin toimii nyt oikein Gmailin kirjautumiskentissä. (#16395)
* Askelpalautin toimii nyt oikein käytettäessä Nudi 6.1:tä NVDA:n "Käsittele muiden sovellusten näppäinpainallukset" -asetuksen ollessa käytössä. (#15822, @jcsteh)
* Korjattu bugi, joka aiheutti sen, että äänikoordinaatit ilmaistiin sovelluksen ollessa lepotilassa ja "Ilmaise hiiren koordinaatit äänimerkeillä" -asetuksen ollessa käytössä. (#8059, @hwf1324)
* NVDA ei enää ohita Adobe Readerissa kaavoihin lisättyä vaihtoehtoista tekstiä PDF:issä. (#12715)
* Korjattu bugi, joka aiheutti sen, ettei NVDA lukenut Geekbenchin valintanauhaa ja asetuksia. (#16251, @mzanm)
* Korjattu harvinainen tilanne, jossa asetusten tallentaminen ei saattanut tallentaa kaikkia profiileja. (#16343, @CyrilleB79)
* NVDA siirtyy Firefoxissa ja Chromium-pohjaisissa selaimissa asianmukaisesti vuorovaikutustilaan painettaessa Enteriä oltaessa esitysmuotoisen luettelon kohdalla (ul / ol) muokattavassa sisällössä. (#16325)
* Sarakkeen tilanmuutos puhutaan automaattisesti valittaessa näytettäviä sarakkeita Thunderbirdin viestiluettelossa. (#16323)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta](../en/changes.html).

## 2024.1

Lisätty uusi "pyydettäessä"-puhetila.
Kun se on käytössä,  NVDA ei puhu automaattisesti (esim. kohdistinta siirrettäessä), mutta puhuu kuitenkin käytettäessä komentoja, joiden tarkoitus on nimenomaan puhua jotain (esim. ikkunan nimen).
NVDA:n asetusten Puhe-kategoriassa on nyt mahdollista jättää pois tarpeettomat puhetilat Vaihda puhetilaa -komennosta (`NVDA+S`).

Uusi alkuperäinen valintatila (otetaan käyttöön ja poistetaan käytöstä näppäinkomennolla `NVDA+Vaihto+F10`) on nyt käytettävissä  NVDA:n selaustilassa Mozilla Firefoxissa.
Kun se on käytössä, tekstin valitseminen selaustilassa vaikuttaa myös Firefoxin omaan, alkuperäiseen valintaan.
Tekstinkopiointikomento `Ctrl+C` välitetään suoraan Firefoxille, jolloin muotoilutkin kopioidaan pelkän NVDA:n tekstiesityksen sijaan.

Lisäosakauppa tukee nyt joukkotoimintoja (esim. asentamista ja käyttöönottoa) valitsemalla useita lisäosia.
Lisätty uusi toiminto arvostelusivun avaamiseen valitulle lisäosalle.

Äänen ulostulolaitteen ja äänenvaimennustilan valinnat on poistettu Valitse syntetisaattori -valintaikkunasta.
Ne löytyvät nyt Ääni-asetuspaneelista, joka voidaan avata näppäinkomennolla `NVDA+Ctrl+U`.

eSpeak NG, LibLouis-pistekääntäjä ja Unicode CLDR on päivitetty.
Uudet thain-, filipinon- ja romaniankieliset pistetaulukot ovat käytettävissä.

Tehty useita erityisesti lisäosakauppaan, pistekirjoitukseen, LibreOfficeen, Microsoft Officeen ja ääneen liittyviä bugikorjauksia.

### Tärkeitä huomautuksia

* Tämä julkaisu rikkoo olemassa olevien lisäosien yhteensopivuuden.
* Windows 7:ää ja 8:aa ei enää tueta.
Windows 8.1 on vanhin tuettava versio.

### Uudet ominaisuudet

* Lisäosakauppa:
  * Lisäosakauppa tukee nyt joukkotoimintoja (esim. asentamista ja käyttöönottamista) useita lisäosia valittaessa. (#15350, #15623, @CyrilleB79)
  * Lisätty uusi toiminto, jolla on mahdollista avata verkkosivu palautteen lukemista tai antamista varten valitusta lisäosasta. (#15576, @nvdaes)
* Lisätty tuki Bluetooth Low Energy -yhteyttä hyödyntäville HID-pistenäytöille. (#15470)
* Uusi alkuperäinen valintatila (otetaan käyttöön ja poistetaan käytöstä näppäinkomennolla `NVDA+Vaihto+F10`) on nyt käytettävissä  NVDA:n selaustilassa Mozilla Firefoxissa
Kun se on käytössä, tekstin valitseminen selaustilassa vaikuttaa myös Firefoxin omaan, alkuperäiseen valintaan.
Tekstinkopiointikomento `Ctrl+C` välitetään suoraan Firefoxille, jolloin muotoilutkin kopioidaan pelkän NVDA:n tekstiesityksen sijaan.
Huomaa kuitenkin, että koska Firefox käsittelee varsinaisen kopioinnin, NVDA ei sano tässä tilassa "kopioitu leikepöydälle". (#15830)
* Muotoilut säilyvät nyt kopioitaessa tekstiä Microsoft Wordissa NVDA:n selaustilassa.
Sivuvaikutuksena on, että NVDA ei enää sano "kopioitu leikepöydälle" painettaessa `Ctrl+C` Microsoft Wordin/Outlookin selaustilassa, koska kopioinnin käsittelee nyt sovellus eikä NVDA. (#16129)
* Lisätty uusi "pyydettäessä"-puhetila.
Kun se on käytössä, NVDA ei puhu automaattisesti (esim. kohdistinta siirrettäessä), mutta puhuu kuitenkin käytettäessä komentoja, joiden tarkoituksena on nimenomaan puhua jotain (esim. ikkunan nimen). (#481, @CyrilleB79)
* NVDA:n asetusten Puhe-kategoriassa on nyt mahdollista jättää pois tarpeettomat puhetilat Vaihda puhetilaa -komennosta (`NVDA+S`). (#15806, @lukaszgo1)
  * Mikäli käytät Ei äänimerkit-puhetilaa -lisäosaa, harkitse sen poistamista ja "äänimerkit"- sekä "pyydettäessä"-tilojen käytöstä poistamista.

### Muutokset

* NVDA ei enää tue Windows 7:ää tai 8:aa.
Windows 8.1 on vanhin tuettava versio. (#15544)
* Komponenttipäivitykset:
  * LibLouis-pistekääntäjä päivitetty versioksi [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Lisätty uudet thain-, romanian- ja filipinonkieliset pistetaulukot.
  * eSpeak NG päivitetty versioksi 1.52-dev muutos `530bf0abf`. (#15036)
  * Emoji- ja symboliselitteet (CLDR) päivitetty versioksi 44.0. (#15712, @OzancanKaratas)
  * Java Access Bridge päivitetty versioksi 17.0.9+8Zulu (17.46.19). (#15744)
* Näppäinkomennot:
  * Seuraavat komennot tukevat nyt kahta painallusta puhutun tiedon tavaamiseen normaalisti ja kolmea tavaamiseen merkkikuvauksia käyttäen: puhu valinta, puhu leikepöydän teksti sekä puhu aktiivinen objekti. (#15449, @CyrilleB79)
  * Näyttöverhon tilan vaihtamiselle on nyt oletusarvoinen näppäinkomento: `NVDA+Ctrl+Esc`. (#10560, @CyrilleB79)
  * Puhu valinta -komento näyttää nyt neljästi painettaessa valinnan selaustilassa. (#15858, @Emil-18)
* Microsoft Office:
  * Kun muotoilutietoja pyydetään Excel-soluissa, reunat ja tausta puhutaan vain, jos kyseisiä muotoiluja on. (#15560, @CyrilleB79)
  * NVDA ei enää puhu nimettömiä ryhmiä esim. uusimpien Microsoft Office 365 -versioiden valikoissa. (#15638)
* Äänen ulostulolaitteen ja äänenvaimennuksen valinnat on poistettu "Valitse syntetisaattori" -valintaikkunasta.
Ne löytyvät Ääni-asetuspaneelista, joka voidaan avata näppäinkomennolla `NVDA+Ctrl+U`. (#15512, @codeofdusk)
* NVDA-asetusten Hiiri-kategorian "Ilmoita hiiren alla olevan objektin rooli" -asetuksen uusi nimi on "Puhu objekti hiiren siirtyessä siihen".
Tätä asetusta käytettäessä objektista puhutaan nyt lisää olennaista tietoa, kuten tilat (valittu/painettu) tai taulukon solujen koordinaatit. (#15420, @LeonarddeR)
* Ohje-valikkoon on lisätty vaihtoehdot NV Accessin "Hanki ohjeita" -sivun ja kaupan avaamiseen. (#14631)
* NVDA:n [Poedit](https://poedit.net)-tuki on uudistettu Poedit 3:lle ja sitä uudemmille.
Poedit 1:n käyttäjiä kannustetaan päivittämään versioon 3, mikäli haluavat hyödyntää parannettua saavutettavuutta, kuten huomautukset kääntäjille- ja kommenttiosioiden lukemista pikanäppäimiä käyttäen. (#15313, #7303, @LeonarddeR)
* Pistekirjoituksen tarkastelu- ja puheen tarkastelu -toiminnot eivät ole käytössä suojatussa tilassa. (#15680)
* Objekteja, jotka eivät ole käytettävissä, ei enää ohiteta objektinavigointia käytettäessä. (#15477, @CyrilleB79)
* Lisätty sisällysluettelo näppäinkomentojen pikaoppaaseen. (#16106)

### Bugikorjaukset

* Lisäosakauppa:
  * Päivitetty kohde puhutaan nyt oikein, kun lisäosan tila muuttuu sen ollessa aktiivisena, esim. tilasta "ladataan" tilaksi "ladattu". (#15859, @LeonarddeR)
  * Uudelleenkäynnistysvalintaikkuna ei enää peitä Asennusilmoituksia lisäosia asennettaessa. (#15613, @lukaszgo1)
  * Yhteensopimatonta lisäosaa ei enää poisteta väkisin käytöstä uudelleenasennettaessa. (#15584, @lukaszgo1)
  * Käytöstä poistetut ja yhteensopimattomat lisäosat voidaan nyt päivittää. (#15568, #15029)
  * NVDA palautuu nyt normaaliksi ja näyttää virheilmoituksen, jos lisäosan lataus epäonnistuu. (#15796)
  * NVDA:n uudelleenkäynnistys ei enää satunnaisesti epäonnistu, kun lisäosakauppa on avattu ja suljettu. (#16019, @lukaszgo1)
* Ääni:
  * NVDA ei enää jäädy hetkeksi, kun useita ääniä toistetaan nopeasti peräkkäin. (#15311, #15757, @jcsteh)
  * Jos äänen ulostulolaitteeksi on määritetty jokin muu kuin oletuslaite ja kyseinen laite on taas käytettävissä sen oltua aiemmin poissa käytöstä, NVDA vaihtaa nyt takaisin määritettyyn laitteeseen sen sijaan, että jatkaisi oletuslaitteen käyttöä. (#15759, @jcsteh)
  * NVDA jatkaa nyt äänentoistoa, jos ulostulolaite muuttuu tai toinen sovellus vapauttaa laitteen yksinomaisesta hallinnasta. (#15758, #15775, @jcsteh)
* Pistekirjoitus:
  * Moniriviset pistenäytöt eivät enää kaada BRLTTY-ajuria, ja niitä käsitellään yhtenä jatkuvana näyttönä. (#15386)
  * Nyt havaitaan enemmän hyödyllistä tekstiä sisältäviä objekteja, ja tekstisisältö näytetään pistekirjoituksella. (#15605)
  * Lyhennepistekirjoituksen syöttö toimii taas asianmukaisesti. (#15773, @aaclause)
  * Pistenäyttöä päivitetään nyt useammissa tilanteissa siirrettäessä navigointiobjektia taulukon solujen välillä. (#15755, @Emil-18)
  * Nykyisen kohdistuksen, navigointiobjektin ja valinnan puhumisen tulos näytetään nyt pistekirjoituksella. (#15844, @Emil-18)
  * Albatross-pistenäyttöajuri ei enää käsittele ESP32-mikro-ohjainta Albatross-näyttönä. (#15671)
* LibreOffice:
  * Sanat, jotka poistetaan `Ctrl+Askelpalautin`-näppäinyhdistelmää käyttäen, ilmoitetaan nyt asianmukaisesti myös silloin, kun poistettua sanaa seuraa tyhjätilamerkki (kuten välilyönti tai sarkain). (#15436, @michaelweghorn)
  * Tilarivin puhuminen `NVDA+End`-pikanäppäintä käyttäen toimii nyt myös LibreOffice 24.2:n ja uudempien valintaikkunoissa. (#15591, @michaelweghorn)
  * Kaikkia odotettuja tekstiattribuutteja tuetaan nyt LibreOffice 24.2:ssa ja sitä uudemmissa versioissa.
  Tämä mahdollistaa kirjoitusvirheiden ilmoittamisen Writerissa riviä puhuttaessa. (#15648, @michaelweghorn)
  * Otsikkotasojen puhuminen toimii nyt myös LibreOffice 24.2:ssa ja sitä uudemmissa versioissa. (#15881, @michaelweghorn)
* Microsoft Office:
  * Kun UIA on poistettu käytöstä Excelissä, pistenäyttöä päivitetään ja aktiivisen solun sisältö puhutaan painettaessa `Ctrl+Y`, `Ctrl+Z` tai `Alt+Askelpalautin`. (#15547)
  * Kun UIA on poistettu käytöstä Wordissa, pistenäyttöä päivitetään painettaessa `Ctrl+V`, `Ctrl+X`, `Ctrl+Y`, `Ctrl+Z`, `Alt+Askelpalautin`, `Askelpalautin` tai `Ctrl+Askelpalautin`.
  Sitä päivitetään myös tekstiä kirjoitettaessa UIA:n ollessa käytössä, kun pistenäyttö seuraa tarkastelukohdistinta ja tarkastelukohdistin seuraa järjestelmäkohdistinta. (#3276)
  * Solu, johon siirrytään, ilmoitetaan nyt oikein Wordissa käytettäessä Wordin sisäisiä taulukkonavigointikomentoja, kuten `Alt+Home`, `Alt+End`, `Alt+Page up` ja `Alt+Page down`. (#15805, @CyrilleB79)
* Objektien pikanäppäinten puhumista on paranneltu. (#10807, #15816, @CyrilleB79)
* SAPI4-syntetisaattoriajuri tukee nyt asianmukaisesti puhuttuun tekstiin sisällytettyjä äänenvoimakkuuden, nopeuden ja korkeuden muutoksia. (#15271, @LeonarddeR)
* Monirivinen tila puhutaan nyt oikein Java Access Bridgeä käyttävissä sovelluksissa. (#14609)
* NVDA puhuu sisällön useammissa Windows 10:n ja 11:n valintaikkunoissa. (#15729, @josephsl)
* Äskettäin ladatun sivun lukeminen ei enää epäonnistu Microsoft Edgessä UI Automation -rajapintaa käytettäessä. (#15736)
* Kun käytetään "jatkuva luku" -toimintoa tai tekstiä tavaavia komentoja, lauseiden tai merkkien väliset tauot eivät enää vähene asteittain ajan myötä. (#15739, @jcsteh)
* NVDA ei enää toisinaan jäädy puhuttaessa suurta tekstimäärää. (#15752, @jcsteh)
* Kun Microsoft Edgeä käytetään UI Automation -rajapinnan avulla, NVDA pystyy aktivoimaan selaustilassa useampia säätimiä. (#14612)
* NVDA:n käynnistys ei enää epäonnistu, kun asetustiedosto on vioittunut, vaan palauttaa oletusasetukset kuten aiemmin. (#15690, @CyrilleB79)
* Korjattu järjestelmän luettelonäkymä (`SysListView32`) -säädinten tuki Windows Forms -sovelluksissa. (#15283, @LeonarddeR)
* NVDA:n Python-konsolin historiaa ei voi enää ylikirjoittaa. (#15792, @CyrilleB79)
* NVDA:n pitäisi  reagoida nopeasti komentoihin, vaikka se vastaanottaisi runsaasti UI Automation -tapahtumia, esim. kun päätteeseen tulostuu paljon tekstiä tai kuunneltaessa ääniviestejä WhatsAppissa. (#14888, #15169)
  * Tämä uusi toiminnallisuus voidaan poistaa käytöstä NVDA:n lisäasetuksista löytyvällä "Käytä laajennettua tapahtumienkäsittelyä" -asetuksella.
* NVDA pystyy taas seuraamaan kohdistusta sovelluksissa, jotka toimivat Windows Defender Application Guard (WDAG) -ympäristössä. (#15164)
* Puhuttua tekstiä  ei enää päivitetä hiiren siirtyessä puheentarkasteluikkunaan. (#15952, @hwf1324)
* NVDA siirtyy taas takaisin selaustilaan Firefoxissa ja Chromessa, kun yhdistelmäruudut suljetaan painamalla `Esc` tai `Alt+Nuoli ylös`. (#15653)
* iTunesissa ei enää virheellisesti siirrytä takaisin selaustilaan liikuttaessa yhdistelmäruuduissa nuolinäppäimillä ylös ja alas. (#15653)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta](../en/changes.html).

## 2023.3.4

Tämä versio korjaa tietoturva- ja asennusohjelmassa ilmenneen ongelman.
Ilmoita tietoturvaongelmista vastuullisesti noudattaen NVDA:n [tietoturvakäytäntöä](https://github.com/nvaccess/nvda/blob/master/security.md).

### Tietoturvakorjaukset

* Estetty mukautettujen asetusten lataaminen suojatun tilan ollessa pakotettuna käyttöön.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Bugikorjaukset

* Korjattu ongelma, joka aiheutti sen, ettei NVDA-prosessi sulkeutunut oikein. (#16123)
* Korjattu bugi, joka aiheutti sen, että jos aiempi NVDA-prosessi ei sulkeutunut oikein, NVDA:n asennus saattoi epäonnistua ja joutua palautumattomaan tilaan. (#16122)

## 2023.3.3

Tämä on korjausversio tietoturvaongelman korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti noudattaen NVDA:n [tietoturvakäytäntöä](https://github.com/nvaccess/nvda/blob/master/security.md).

### Tietoturvakorjaukset

* Estää mahdollista muokatusta sisällöstä heijastunutta XSS-hyökkäystä aiheuttamasta mielivaltaista koodin suorittamista.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Tämä on korjausversio tietoturvaongelman korjaamiseksi.
Version 2023.3.1 tietoturvaongelmaa ei korjattu asianmukaisesti.
Ilmoita tietoturvaongelmista vastuullisesti noudattaen NVDA:n [tietoturvakäytäntöä](https://github.com/nvaccess/nvda/blob/master/security.md).

### Tietoturvakorjaukset

* Version 2023.3.1 tietoturvaongelmaa ei ratkaistu asianmukaisesti.
Estää tunnistamattomia käyttäjiä  pääsemästä järjestelmään ja suorittamasta mielivaltaista koodia järjestelmätason  oikeuksin.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Tämä on korjausversio tietoturvaongelman korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti noudattaen NVDA:n [tietoturvakäytäntöä](https://github.com/nvaccess/nvda/blob/master/security.md).

### Tietoturvakorjaukset

* Estää tunnistamattomia käyttäjiä  pääsemästä järjestelmään ja suorittamasta mielivaltaista koodia järjestelmätason  oikeuksin.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Tämä versio sisältää suoritus- ja reagointikyvyn sekä äänentoiston vakauden parannuksia.
Lisätty asetukset NVDA-äänien ja piippausten voimakkuuden säätämiseen tai käytettävän puheäänen voimakkuuteen mukautumiseen.

NVDA voi nyt päivittää tekstintunnistuksen tulokset automaattisesti ja puhua uuden tekstin sen ilmestyessä.
Tämä voidaan määrittää NVDA:n asetusvalintaikkunan Windowsin tekstintunnistus -kategoriasta.

Useita pistenäyttöjen korjauksia, jotka parantavat laitteiden tunnistusta ja kohdistimen siirtämistä.
Pistenäyttöajureita on nyt mahdollista jättää pois automaattisesta tunnistuksesta, mikä parantaa sen suorituskykyä.
Uusia BRLTTY-komentoja on myös lisätty.

Bugikorjauksia lisäosakauppaan, Microsoft Officeen, Edgen pikavalikoihin sekä Windowsin laskimeen.

### Uudet ominaisuudet

* Paranneltu äänenhallinta:
  * Uusi ääniasetuspaneeli:
    * Se voidaan avata painamalla `NVDA+Ctrl+U`. (#15497)
    * Asetus, jolla NVDA:n äänet ja piippaukset saadaan mukautumaan käytettävän puheäänen voimakkuuteen. (#1409)
    * Asetus, jolla NVDA-äänien voimakkuus voidaan määrittää erikseen. (#1409, #15038)
    * Äänen ulostulolaitteen ja äänenvaimennuksen muuttamiseen tarkoitetut asetukset on siirretty Valitse syntetisaattori -valintaikkunasta uuteen Ääni-asetuspaneeliin.
    Nämä asetukset poistetaan Valitse syntetisaattori -valintaikkunasta NVDA:n 2024.1-versiossa. (#15486, #8711)
  * NVDA toistaa nyt ääntä Windows Audio Session APIn (WASAPI) kautta, mikä saattaa parantaa puheen ja äänien reagointi- ja suorituskykyä sekä vakautta. (#14697, #11169, #11615, #5096, #10185, #11061)
  * Huom: WASAPI ei ole yhteensopiva joidenkin lisäosien kanssa.
  Näille lisäosille on saatavilla yhteensopivat päivitykset. Asenna ne ennen NVDA:n päivittämistä.
  Näiden lisäosien yhteensopimattomat versiot poistetaan käytöstä NVDA:ta päivitettäessä:
    * Tony's Enhancements 1.15 tai vanhempi. (#15402)
    * NVDA global commands extension 12.0.8 tai vanhempi. (#15443)
* NVDA pystyy nyt päivittämään jatkuvasti tunnistuksen tulosta suorittaessaan tekstintunnistusta ja puhumaan uuden tekstin sitä mukaa, kun se ilmestyy. (#2797)
  * Ota tämä toiminto käyttöön "Päivitä tunnistuksen tulos automaattisesti" -asetuksella, joka löytyy NVDA:n asetusvalintaikkunan Windowsin tekstintunnistus -kategoriasta.
  * Kun toiminto on käytössä, voit ottaa käyttöön tai poistaa käytöstä uuden tekstin puhumisen muuttamalla Puhu dynaamisen sisällön muutokset -asetusta (painamalla `NVDA+5`).
* Pistenäyttöjen automaattista tunnistusta käytettäessä on nyt mahdollista jättää ajureita tunnistuksen ulkopuolelle Valitse pistenäyttö -valintaikkunasta. (#15196)
* Lisätty asetusvalintaikkunan Asiakirjojen muotoilu -kategoriaan "Ohita tyhjät rivit rivien sisennystä ilmoitettaessa" -asetus. (#13394)
* Lisätty komento välilehtien välillä liikkumiseen selaustilassa. Pikanavigointinäppäintä ei ole määritetty. (#15046)

### Muutokset

* Pistekirjoitus:
  * Pistenäytöllä näkyvä teksti päivittyy nyt oikein oltaessa muuttuneella rivillä, kun Teksti muuttuu päätteessä ilman, että kohdistinta päivitetään.
  Näihin sisältyvät tilanteet, joissa pistenäyttö seuraa tarkastelukohdistinta. (#15115)
  * Määritetty NVDA-komennot useampiin BRLTTYn näppäinsidoksiin (#6483):
    * `learn`: NVDA:n näppäinohje
    * `prefmenu`: Avaa NVDA-valikko
    * `prefload`/`prefsave`: Lataa/tallenna NVDA:n asetukset
    * `time`: Näytä kellonaika
    * `say_line`: Puhu tarkastelukohdistimen kohdalla oleva rivi
    * `say_below`: Jatkuva luku
  * BRLTTY-ajuri on käytettävissä vain, kun käynnissä on BRLTTY-kopio, jossa BrlAPI on käytössä. (#15335)
  * HID Braille -protokollan käyttöönottava lisäasetus on korvattu uudella asetuksella.
  Automaattinen tunnistus on nyt mahdollista poistaa käytöstä määrätyiltä pistenäyttöajureilta Valitse pistenäyttö -valintaikkunassa. (#15196)
* Asennetut lisäosat näytetään nyt lisäosakaupan Saatavilla-välilehdellä, mikäli ne ovat saatavilla. (#15374)
* Jotkut NVDA-valikossa olevien kohteiden pikanäppäimistä on päivitetty. Tämä koskee vain käyttäjiä, joilla NVDA:n kielenä on englanti. (#15364)

### Bugikorjaukset

* Microsoft Office:
  * Korjattu kaatuminen Microsoft Wordissa, kun otsikoiden sekä kommenttien ja muistiinpanojen ilmoittaminen eivät olleet käytössä. (#15019)
  * Tekstin tasaus ilmoitetaan oikein useammissa tilanteissa Wordissa ja Excelissä. (#15206, #15220)
  * Korjattu joidenkin solunmuotoilupikanäppäinten puhuminen Excelissä. (#15527)
* Microsoft Edge:
  * NVDA ei enää siirry takaisin edelliseen selaustilasijaintiin Microsoft Edgessä pikavalikkoa avattaessa. (#15309)
  * NVDA pystyy taas lukemaan latausten pikavalikon Microsoft Edgessä. (#14916)
* Pistekirjoitus:
  * Pistekohdistin ja valinnanilmaisin päivittyvät nyt oikein aina, kun ne näytetään tai piilotetaan näppäinkomentoa käyttäen. (#15115)
  * Korjattu bugi, jossa Albatross-pistenäytöt yrittävät alustaa itsensä, vaikka toinen pistenäyttö on kytkettynä. (#15226)
* Lisäosakauppa:
  * Korjattu bugi, joka aiheutti yhteensopimattomien lisäosien näyttämisen, vaikka "Näytä yhteensopimattomat lisäosat" -valintaruudun valinta oli poistettu. (#15411)
  * Yhteensopivuussyistä estetyt lisäosat suodatetaan nyt asianmukaisesti, kun Käytössä/ei käytössä -suodattimen tilaa vaihdetaan. (#15416)
  * Korjattu bugi, joka esti käytössä olevien yhteensopivuusohitettujen lisäosien päivittämisen tai korvaamisen ulkoisesta lähteestä asennetulla versiolla. (#15417)
  * Korjattu bugi, joka aiheutti sen, ettei NVDA puhunut mitään lisäosan asennuksen jälkeen ennen kuin se käynnistettiin uudelleen. (#14525)
  * Korjattu bugi, joka aiheutti sen, ettei lisäosia voitu asentaa, jos aiempi lataus epäonnistui tai peruutettiin. (#15469)
  * Korjattu NVDA:ta päivitettäessä ilmenneitä yhteensopimattomien lisäosien käsittelyyn liittyviä ongelmia. (#15414, #15412, #15437)
* NVDA ilmoittaa jälleen laskutoimitusten tulokset 32-bittisessä laskimessa Windowsin Server-, LTSC- ja LTSB-versioissa. (#15230)
* NVDA ei enää ohita kohdistusmuutoksia, kun sisäkkäinen ikkuna tulee aktiiviseksi. (#15432)
* Korjattu NVDA:n käynnistyksen aikanailmenevän kaatumisen mahdollinen aiheuttaja. (#15517)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta](../en/changes.html).

## 2023.2

Tässä versiossa esitellään lisäosakauppa, joka korvaa lisäosien hallinnan.
Lisäosakaupassa on mahdollista selata, etsiä, asentaa ja päivittää yhteisön lisäosia.
Vanhentuneiden lisäosien yhteensopivuusongelmat voidaan nyt ohittaa omalla vastuulla.

Lisätty pistekirjoitusominaisuuksia ja -komentoja sekä tuki uusille näytöille.
Lisäksi uusia näppäinkomentoja tekstintunnistukselle sekä tasatulle objektinavigoinnille.
Liikkumista ja muotoilun ilmoittamista on paranneltu Microsoft Officessa.

Useita erityisesti pistekirjoitukseen, Microsoft Officeen, verkkoselaimiin ja Windows 11:een liittyviä bugikorjauksia.

eSpeak-NG, LibLouis-pistekääntäjä ja Unicode-CLDR on päivitetty.

### Uudet ominaisuudet

* NVDA:han on lisätty lisäosakauppa. (#13985)
  * Selaa, etsi, asenna ja päivitä yhteisön lisäosia.
  * Ohita manuaalisesti vanhentuneiden lisäosien yhteensopimattomuusongelmat.
  * Lisäosien hallinta on poistettu ja korvattu lisäosakaupalla.
  * Katso lisätietoja päivitetystä käyttöoppaasta.
* Uusia komentoja:
  * Komento Windowsin tekstintunnistuksen kielen vaihtamiseen. Oletusarvoista näppäinkomentoa ei ole määritetty. (#13036)
  * Komento Näytä ilmoitukset pistenäytöllä -asetuksen muuttamiseen. Oletusarvoista näppäinkomentoa ei ole määritetty. (#14864)
  * Komento, joka ottaa käyttöön tai poistaa käytöstä valinnanilmaisimen näyttämisen pistenäytöllä. Oletusarvoista näppäinkomentoa ei ole määritetty. (#14948)
  * Lisätty oletusarvoiset näppäinkomentomääritykset seuraavaan ja edelliseen objektiin siirtymiseen objektihierarkian tasatussa näkymässä. (#15053)
    * Pöytäkone: `NVDA+Laskinnäppäimistön 9` ja `NVDA+Laskinnäppäimistön 3` siirtävät edelliseen ja seuraavaan objektiin.
    * Kannettava: `Vaihto+NVDA+[` ja `Vaihto+NVDA+]` siirtävät edelliseen ja seuraavaan objektiin.
* Uusia pistekirjoitusominaisuuksia:
  * Lisätty tuki Help Techin Activator-pistenäytölle. (#14917)
  * Uusi asetus, jolla voidaan ottaa käyttöön tai poistaa käytöstä valinnanilmaisimen (pisteet 7 ja 8) näyttäminen. (#14948)
  * Uusi asetus, joka siirtää valinnaisesti järjestelmäkohdistinta tai kohdistusta, kun tarkastelukohdistimen paikkaa vaihdetaan pistenäytön kosketuskohdistinnäppäimillä. (#14885, #3166)
  * Kun tarkastelukohdistimen kohdalla olevan merkin numeerinen arvo puhutetaan painamalla kolmesti `Laskinnäppäimistön 2`, arvo näytetään nyt myös pistenäytöllä. (#14826)
  * Lisätty tuki ARIA 1.3:n `aria-brailleroledescription`-attribuutille, jonka avulla verkkosivujen tekijät voivat ohittaa pistenäytöllä näytettävän elementin tyypin. (#14748)
  * Lisätty Baum-pistenäyttöjen ajuriin useita moniosaisia näppäinkomentoja yleisten näppäinkomentojen, kuten `Win+D` ja `Alt+Sarkain`, suorittamista varten.
  Katso kaikki komennot NVDA:n käyttöoppaasta. (#14714)
* Lisätty Unicode-symbolien lausuminen:
  * Pistekirjoitussymbolit, kuten `⠐⠣⠃⠗⠇⠐⠜`. (#13778)
  * Macin Option-näppäimen symboli `⌥`. (#14682)
* Lisätty näppäinkomentoja Tivomaticin Caiku Albatross -pistenäytöille. (#14844, #15002)
  * Pistekirjoitusasetusten valintaikkunan näyttäminen
  * Tilariville siirtyminen
  * Pistekohdistimen muodon vaihtaminen
  * Näytä ilmoitukset pistenäytöllä -asetuksen tilan vaihtaminen
  * Pistekohdistimen käyttöönotto/käytöstä poistaminen
  * Valinnanilmaisimen käyttöönotto tai käytöstä poistaminen
  * "Siirrä järjestelmäkohdistin tarkastelukohdistimen kohdalle pistenäytön kosketuskohdistinnäppäimillä" -asetuksen tilan vaihtaminen. (#15122)
* Microsoft Office -ominaisuudet:
  * Korostusvärit puhutaan nyt Microsoft Wordissa, kun korostetun tekstin ilmaiseminen on otettu käyttöön asiakirjojen muotoiluasetuksissa. (#7396, #12101, #5866)
  * Taustavärit puhutaan nyt Microsoft Wordissa, kun värien ilmaiseminen on otettu käyttöön asiakirjojen muotoiluasetuksissa. (#5866)
  * Näppäinkomentojen tulokset puhutaan nyt Excelissä vaihdettaessa solun muotoilun, kuten lihavoinnin, kursiivin tai alle- ja yliviivauksen tilaa. (#14923)
* Paranneltu kokeellinen äänenhallinta:
  * NVDA voi nyt toistaa ääntä Windows Audio Session APIn (WASAPI) kautta, joka saattaa parantaa puheen ja äänien reagoivuutta, suorituskykyä ja vakautta. (#14697)
  * WASAPI voidaan ottaa käyttöön Lisäasetukset-paneelista.
  Jos WASAPI on otettu käyttöön, myös seuraavat lisäasetukset on mahdollista määrittää.
    * Asetus, joka saa NVDA:n äänet ja piippaukset mukautumaan käyttämäsi puheäänen voimakkuuteen. (#1409)
    * Asetus, jonka avulla NVDA-äänien voimakkuutta on mahdollista säätää erikseen. (#1409, #15038)
  * Tiedossa on ongelma, joka aiheuttaa satunnaisia kaatumisia WASAPIn ollessa käytössä. (#15150)
* NVDA ilmoittaa nyt Mozilla Firefoxissa ja Google Chromessa, kun säädin avaa valintaikkunan, ruudukon, luettelon tai puunäkymän, mikäli sivuston tekijä on määrittänyt sen aria-haspopup-attribuuttia käyttäen. (#8235)
* Polkumäärityksessä on nyt mahdollista käyttää järjestelmän ympäristömuuttujia (kuten `%temp%` tai `%homepath%`) NVDA:n massamuistiversiota luotaessa. (#14680)
* Kun virtuaalityöpöytiä avataan, vaihdetaan tai suljetaan, NVDA ilmoittaa niiden nimet Windows 10:n toukokuun 2019 päivityksessä ja sitä uudemmissa. (#5641)
* Lisätty järjestelmänlaajuinen parametri, jolla tavalliset käyttäjät ja järjestelmänvalvojat voivat pakottaa NVDA:n käynnistymään suojatussa tilassa. (#10018)

### Muutokset

* Päivitetyt osat:
  * eSpeak NG päivitetty versioksi 1.52-dev muutos `ed9a7bcf`. (#15036)
  * LibLouis-pistekääntäjä päivitetty versioksi [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR päivitetty versioksi 43.0. (#14918)
* LibreOfficen muutokset:
  * Kohdistimen sijainti ilmoitetaan tarkastelukohdistimen sijaintia ilmoitettaessa nyt LibreOffice Writerissa suhteessa nykyiseen sivuun (LibreOfficen versiot 7.6 ja sitä uudemmat) samalla tavalla kuin Microsoft Wordissa. (#11696)
  * Tilarivin lukeminen (esim. painamalla `NVDA+End`) toimii LibreOfficessa. (#11698)
  * Aiemman solun koordinaatteja ei enää virheellisesti puhuta siirryttäessä LibreOffice Calcissa eri soluun, kun solun koordinaattien ilmoittaminen on poistettu käytöstä NVDA:n asetuksissa. (#15098)
* Pistekirjoitus:
  * Kun pistenäyttöä käytetään standardinmukaisella HID-ajurilla, dpadia voidaan käyttää nuolinäppäinten ja Enterin jäljittelemiseen.
  Lisäksi Väli+piste 1 ja Väli+piste 4 on nyt määritetty ylä- ja alanuolinäppäimiksi. (#14713)
  * Dynaamisen verkkosisällön päivitykset (ARIAn aktiiviset alueet) näytetään nyt pistenäytöllä.
  Tämä voidaan poistaa käytöstä Lisäasetukset-paneelista. (#7756)
   -
* Viivan ja pitkän ajatusviivan symbolit lähetetään aina syntetisaattorille. (#13830)
* Microsoft Wordissa ilmoitetut etäisyydet noudattavat nyt Wordin lisäasetuksissa määriteltyä yksikköä myös käytettäessä UIA:ta Word-asiakirjoille. (#14542)
* NVDA reagoi nopeammin, kun kohdistinta siirretään muokkaussäätimissä. (#14708)
* Linkin kohteen ilmoittava komento ilmoittaa nyt navigointiobjektin sijaan kohdistimen tai kohdistuksen sijainnista. (#14659)
* Massamuistiversiota luotaessa ei enää tarvitse antaa asemakirjainta osana absoluuttista polkumääritystä. (#14680)
* Jos Windows on määritetty näyttämään sekunnit tehtäväpalkin kellossa, kellonajan ilmoittava `NVDA+F12`-näppäinkomento noudattaa nyt tätä asetusta. (#14742)
* NVDA ilmoittaa nyt nimeämättömät ryhmät, joissa on hyödyllistä sijaintitietoa, kuten uusimmissa Microsoft Office 365 -versioiden valikoissa. (#14878)

### Bugikorjaukset

* Pistekirjoitus:
  * Useita korjauksia pistekirjoituksen syötön/tulostuksen vakauteen, josta on seurauksena vähemmän virheitä ja NVDA:n kaatumisia. (#14627)
  * NVDA ei enää vaihda tarpeettomasti Ei pistenäyttöä -ajuriin useasti automaattisen tunnistuksen aikana, mistä on seurauksena puhtaampi loki ja pienempi muistin käyttö. (#14524)
  * NVDA vaihtaa nyt takaisin USB:hen, mikäli HID Bluetooth -laite (kuten HumanWare Brailliant tai APH Mantis) tunnistetaan automaattisesti ja USB-yhteys tulee saataville.
  Tämä toimi aiemmin vain Bluetooth-sarjaporteilla. (#14524)
  * Pistekirjoitusalijärjestelmän näytön koko nollataan taas siten, ettei pistesoluja ole, kun pistenäyttöä ei ole yhdistetty ja pistekirjoituksen tarkastelu suljetaan painamalla `Alt+F4` tai napsauttamalla Sulje-painiketta. (#15214)
* Verkkoselaimet:
  * NVDA ei enää aiheuta toisinaan Mozilla Firefoxin kaatumista tai vastaamasta lakkaamista. (#14647)
  * Kirjoitettuja merkkejä ei enää puhuta Mozilla Firefoxissa ja Google Chromessa joissakin tekstikentissä, kun kirjoitettujen merkkien puhuminen on poistettu käytöstä. (#8442)
  * Selaustilaa on nyt mahdollista käyttää sellaisissa upotetuissa Chromium-säätimissä, joissa se ei ollut aiemmin mahdollista. (#13493, #8553)
  * Linkin jälkeinen teksti luetaan nyt luotettavasti, kun hiiri siirretään sen päälle Mozilla Firefoxissa. (#9235)
  * Graafisten linkkien kohteet ilmoitetaan nyt tarkasti useammissa tapauksissa Chromessa ja Edgessä. (#14783)
  * NVDA ei ole enää hiljaa yritettäessä ilmoittaa URLia sellaiselle linkille, jossa ei ole href-attribuuttia.
  Sen sijaan ilmoitetaan, ettei linkillä ole kohdetta. (#14723)
  * NVDA ei enää ohita virheellisesti selaustilassa kohdistuksen siirtymistä ylemmän tai alemman tason säätimeen, esim. siirryttäessä säätimestä luettelokohteeseen tai ruudukkosoluun. (#14611)
    * Huom: Tämä korjaus koskee vain tilannetta, jossa "Siirrä kohdistus automaattisesti kohdistettaviin elementteihin" -asetus on poistettu käytöstä (oletusarvoisesti on) selaustilan asetuksista.
   -
* Windows 11:n korjaukset:
  * NVDA lukee taas Muistion tilarivin sisällön. (#14573)
  * Uuden välilehden nimi ja sijainti puhutaan Muistiossa ja resurssienhallinnassa välilehteä vaihdettaessa. (#14587, #14388)
  * NVDA puhuu taas ehdotuskohteet kirjoitettaessa tekstiä sellaisilla kielillä kuin kiina ja japani. (#14509)
* NVDA:n Ohje-valikon Tekijät- ja Käyttöoikeussopimus-kohteiden avaaminen on taas mahdollista. (#14725)
  -
* Microsoft Officen korjaukset:
  * NVDA ilmoittaa nyt Excelissä epätodennäköisemmin väärän solun tai valinnan, kun solujen välillä siirrytään nopeasti. (#14983, #12200, #12108)
  * Kun Excelissä siirrytään soluun työkirjan ulkopuolelta, pistenäyttö ja kohdistuksen korostin eivät enää tarpeettomasti päivity objektiin, jossa kohdistus oli aiemmin. (#15136)
  * Aktivoituvien salasanakenttien puhuminen ei enää epäonnistu Microsoft Excelissä ja Outlookissa. (#14839)
* Symboleille, joille ei ole kuvausta nykyisellä kielellä, käytetään oletusarvoista englannin kielen symbolitasoa. (#14558, #14417)
* Kenoviivamerkkiä on nyt mahdollista käyttää puhesanastomäärityksen Korvaava-kentässä, kun tyyppinä ei ole sääntölauseke. (#14556)
* NVDA:n massamuistiversio ei tee enää mitään tai toista virheääniä kirjoitettaessa laskukaavoja nelilaskintilassa Windows 10:n ja 11:n laskimessa sen ollessa päällimmäisenä. (#14679)
* NVDA palautuu taas useammista tilanteista, kuten sovelluksista, jotka lakkaavat vastaamasta, mikä aiheutti aiemmin sen täydellisen jumiutumisen. (#14759) 
* Korjattu bugi, joka aiheutti NVDA:n jumiutumisen ja lokitiedoston täyttymisen, kun UIA-tuki pakotettiin käyttöön tietyissä päätteissä ja konsoleissa. (#14689)
* NVDA ei enää kieltäydy tallentamasta asetuksiaan asetusten palauttamisen jälkeen. (#13187)
* Kun käytetään asennusohjelmasta käynnistettyä NVDA:n tilapäisversiota, käyttäjiä ei johdeta enää harhaan saamalla heidät luulemaan, että asetusten tallentaminen on mahdollista. (#14914)
* NVDA reagoi hieman nopeammin komentoihin ja kohdistusmuutoksiin. (#14928)
* Tekstintunnistusasetusten näyttäminen ei enää epäonnistu joissakin järjestelmissä. (#15017)
* Korjattu NVDA:n asetusten tallentamiseen ja lataamiseen, syntetisaattorien vaihtaminen mukaan lukien, liittyvä bugi. (#14760)
* Korjattu bugi, joka sai tekstintarkastelun "pyyhkäise ylös" -kosketuseleen vaihtamaan sivua sen sijaan, että olisi siirtänyt edelliselle riville. (#15127)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta](../en/changes.html).

## 2023.1

Lisätty uusi "Kappaletyyli"-asetus "Asiakirjan selaus"-kategoriaan.
Tätä voidaan käyttää sellaisissa tekstieditoreissa, jotka eivät tue kappaleittain liikkumista, kuten Muistio ja Notepad++.

Lisätty uusi linkin kohteen ilmoittava komento, jolle on määritetty näppäinkomento `NVDA+K`.

Merkityn verkkosisällön (kuten kommenttien ja alaviitteiden) tukea on paranneltu.
Vaihda yhteenvetojen välillä painamalla `NVDA+D`, kun merkinnöistä ilmoitetaan (esim. "sisältää tiedon kommentti, sisältää tiedon alaviite").

Tivomaticin Caiku Albatross 46/80 -pistenäyttöjä tuetaan.

Tukea Windowsin ARM64- ja AMD64-versioille on paranneltu.

Useita erityisesti Windows 11:een liittyviä bugikorjauksia.

eSpeak, LibLouis, Sonic-nopeudenlisäyskirjasto sekä Unicode-CLDR on päivitetty.
Uusia georgialaisia, swahililaisia (Kenia) sekä njandžalaisia (Malawi) pistetaulukoita.

Huom:

* Tämä versio rikkoo olemassa olevien lisäosien yhteensopivuuden.

### Uudet ominaisuudet

* Microsoft Excel UI Automation -rajapinnan kautta: Automaattinen sarake- ja riviotsikoiden lukeminen taulukoissa. (#14228)
  * Huom: Tämä tarkoittaa taulukoita, jotka on muotoiltu valintanauhan Lisää-ruudun "Taulukko"-painikkeella.
  Taulukkotyyliasetuksissa "Ensimmäinen sarake" ja "Otsikkorivi" vastaavat sarake- ja riviotsikoita.
  * Tämä ei tarkoita ruudunlukijakohtaisia otsikoita nimettyjen alueiden kautta, joita UI Automation ei tällä hetkellä tue.
* Lisätty määrittämätön komento viivästettyjen merkkikuvausten käyttöön ottamiseen ja käytöstä poistamiseen. (#14267)
* Lisätty kokeellinen asetus UIA-ilmoitustuen hyödyntämiseen Windows-päätteessä uuden tai muuttuneen tekstin lukemista varten, mikä parantaa vakautta ja reagointikykyä. (#13781)
  * Katso tämän asetuksen rajoitukset käyttöoppaasta.
* Selaustila on nyt käytettävissä Windows 11 ARM64:ssä AMD64-sovelluksissa, kuten Firefox, Google Chrome ja 1Password. (#14397)
* Lisätty uusi "Kappaletyyli"-asetus Asiakirjan selaus -kategoriaan.
Tämä lisää tuen yhdellä (normaali) ja usealla rivinvaihdolla (lohko) eroteltujen kappaleiden välillä liikkumiseen.
Tätä voidaan käyttää sellaisissa tekstieditoreissa, jotka eivät tue natiivisti kappaleittain liikkumista, kuten Notepad ja Notepad++. (#13797)
* Useat merkinnät ilmoitetaan.
`NVDA+D` vaihtaa nyt kunkin merkintäkohteen yhteenvedon ilmoittamisen välillä useiden merkintäkohteiden alkuperän osalta.
Esimerkiksi kun tekstiin liittyy kommentti ja alaviite. (#14507, #14480)
* Lisätty tuki Tivomaticin Caiku Albatross 46/80 -pistenäytöille. (#13045)
* Uusi komento: Ilmoita linkin kohde (`NVDA+K`).
Kerran painettaessa puhuu/näyttää pistekirjoituksella navigointiobjektissa olevan linkin kohteen.
Kahdesti painettaessa se näytetään erillisessä ikkunassa yksityiskohtaisempaa tarkastelua varten. (#14583)
* Uusi määrittämätön komento (Työkalut-kategoria): Ilmoita linkin kohde ikkunassa.
Sama kuin `NVDA+K`:n kahdesti painaminen, mutta hyödyllisempi pistenäyttöjen käyttäjille. (#14583)

### Muutokset

* Päivitetty LibLouis-pistekääntäjä versioksi [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Merkittäviä päivityksiä unkarilaiseen, UEB- ja kiinalaiseen bopomofopistekirjoitukseen.
  * Tuki tanskalaiselle 2022-pistekirjoitusstandardille.
  * Uusia pistetaulukoita georgialaiselle kaunokirjalliselle pistekirjoitukselle, swahilille (Kenia) sekä njandžalle (Malawi).
* Päivitetty Sonic-nopeudenlisäyskirjasto muutokseen `1d70513`. (#14180)
* CLDR on päivitetty versioksi 42.0. (#14273)
* eSpeak NG on päivitetty versioksi 1.52-dev muutos `f520fecb`. (#14281, #14675)
  * Korjattu suurten lukujen puhuminen. (#14241)
* Java-sovellukset, joissa käytetään valittavissa-tilan sisältäviä säätimiä, ilmoittavat nyt, kun kohde ei ole valittavissa  sen sijaan, että ilmoittaisivat, kun se on valittu. (#14336)

### Bugikorjaukset

* Windows 11 -korjaukset:
  * NVDA ilmoittaa hakuehdotukset Käynnistä-valikkoa avattaessa. (#13841)
  * ARM-pohjaisissa järjestelmissä ei enää tunnisteta x64-sovelluksia ARM64-sovelluksiksi. (#14403)
  * Leikepöydän historian valikkokohteita, kuten "Kiinnitä kohde", voidaan nyt käyttää. (#14508)
  * Windows 11 22H2:ssa ja uudemmissa on jälleen mahdollista käyttää hiirtä ja kosketusvuorovaikutusta vuorovaikutukseen sellaisissa alueissa kuten ilmaisinalueen ylivuotoikkuna ja "Avaa sovelluksessa" -valintaikkuna. (#14538, #14539)
* Ehdotukset puhutaan, kun Microsoft Excelin kommentteihin kirjoitetaan @mention. (#13764)
* Ehdotussäätimet (Siirry välilehteen, Poista ehdotus jne.) puhutaan valittaessa Google Chromen sijaintipalkissa. (#13522)
* Värit ilmoitetaan nyt selkeästi "oletusvärin" asemesta Wordpadissa tai Näytä loki -sovelluksessa muotoilutietoja pyydettäessä. (#13959)
* GitHubin ongelmasivujen "Show options" -painikkeen painaminen toimii nyt luotettavasti Firefoxissa. (#14269)
* Päivämäärän valitsinsäätimet ilmoittavat nyt nimensä ja arvonsa Outlook 2016:n / 365:n Edistynyt haku -valintaikkunassa. (#12726)
* ARIA-valitsinsäätimet ilmoitetaan nyt Firefoxissa, Chromessa ja Edgessä valintaruutujen asemesta valitsimina. (#11310)
* NVDA ilmoittaa automaattisesti HTML -taulukon sarakeotsikon lajittelutilan, kun sitä muutetaan sisäpainiketta painamalla. (#10890)
* Kiintopiste tai alueen nimi puhutaan aina automaattisesti siirryttäessä ulkopuolelta sisään pikanavigointia tai selaustilassa kohdistusta käyttäen. (#13307)
* NVDA ei enää anna äänimerkkiä tai sano kahdesti "iso", kun Ilmaise isot kirjaimet äänimerkillä- tai Ilmaise isot kirjaimet sanomalla "iso" -asetukset ovat käytössä samanaikaisesti viivästettyjen merkkikuvausten kanssa. (#14239)
* NVDA puhuu nyt tarkemmin taulukoiden säätimet Java-sovelluksissa. (#14347)
* Jotkut asetukset eivät enää ole odottamattomasti erilaisia, kun niitä käytetään useissa profiileissa. (#14170)
  * Seuraavien asetusten toiminta on korjattu:
    * Rivien sisennykset asiakirjojen muotoiluasetuksissa
    * Solun reunat asiakirjojen muotoiluasetuksissa.
    * Näytä ilmoitukset pistekirjoitusasetuksissa
    * Pistenäyttö seuraa pistekirjoitusasetuksissa
  * Joissakin harvinaisissa tapauksissa näitä profiileissa käytettyjä asetuksia voidaan muuttaa yllättäen tätä NVDA-versiota asennettaessa.
  * Tarkista nämä asetukset profiileissasi päivitettyäsi tähän NVDA-versioon.
* Emojit puhutaan nyt useammalla kielellä. (#14433)
* Merkinnän olemassaoloa ei enää puutu pistekirjoituksella joistakin elementeistä. (#13815)
* Korjattu ongelma, jossa asetusmuutokset eivät tallennu oikein vaihdettaessa "Oletus"-vaihtoehdon ja "Oletus"-vaihtoehdon arvon välillä. (#14133)
* Kun NVDA:n asetuksia määritetään, NVDA-näppäimeksi on nyt aina määritettynä vähintään yksi näppäin. (#14527)
* Kun NVDA-valikko avataan ilmoitusalueen kautta, NVDA ei enää ehdota odottavaa päivitystä, kun päivitystä ei ole saatavilla. (#14523)
* Yli päivän pituisten äänitiedostojen jäljellä oleva, kulunut ja  kokonaisaika ilmoitetaan nyt oikein foobar2000:ssa. (#14127)
* Ilmoitukset, kuten tiedostolataukset, näytetään verkkoselaimissa kuten Chromessa ja Firefoxissa pistekirjoituksella sen lisäksi että ne puhutaan. (#14562)
* Korjattu bugi, joka ilmeni siirryttäessä Firefoxissa taulukon ensimmäiseen ja viimeiseen sarakkeeseen. (#14554)
* Yleiset asetukset -valintaikkunan avaaminen on jälleen mahdollista, kun NVDA on käynnistetty `--lang=Windows`-parametrilla. (#14407)
* NVDA ei enää lopeta lukemista Kindle for PC:ssä sivun kääntämisen jälkeen. (#14390)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2022.4

Tämä versio sisältää useita uusia näppäinkomentoja, mukaan lukien taulukon jatkuva luku.
Käyttöoppaaseen on lisätty "Pika-aloitusopas"-osio.
Useita bugikorjauksia on myös tehty.

eSpeak ja LibLouis on päivitetty.
Lisätty uusia kiinalaisia, ruotsalaisia, gandalaisia ja ruandalaisia pistetaulukoita.

### Uudet ominaisuudet

* Käyttöoppaaseen lisätty "Pika-aloitusopas"-osio. (#13934)
* Lisätty uusi komento aktiivisen kohdan näppäinkomennon tarkistamiseen. (#13960)
  * Pöytäkone: `Vaihto+Laskinnäppäimistön 2`.
  * Kannettava: `NVDA+Ctrl+Vaihto+.`.
* Lisätty uudet komennot tarkastelukohdistimen siirtämiseen sivu kerrallaan sellaisissa sovelluksissa, jotka sitä tukevat. (#14021)
  * Siirry edelliselle sivulle:
    * Pöytäkone: `NVDA+Page up`.
    * Kannettava: `NVDA+Vaihto+Page up`.
  * Siirry seuraavalle sivulle:
    * Pöytäkone: `NVDA+Page down`.
    * Kannettava: `NVDA+Vaihto+Page down`.
* Lisätty seuraavat taulukkokomennot. (#14070)
  * Sarakkeen jatkuva luku: `NVDA+Ctrl+Alt+Nuoli alas`
  * Rivin jatkuva luku: `NVDA+Ctrl+Alt+Nuoli oikealle`
  * Lue koko sarake: `NVDA+Ctrl+Alt+Nuoli ylös`
  * Lue koko rivi: `NVDA+Ctrl+Alt+Nuoli vasemmalle`
* NVDA ilmoittaa nyt Microsoft Excelissä, kun laskentataulukossa olevasta taulukosta siirrytään pois UI Automation -rajapinnan ollessa käytössä. (#14165)
* Taulukko-otsikoiden lukeminen voidaan nyt määrittää erikseen riveille ja sarakkeille. (#14075)

### Muutokset

* eSpeak NG on päivitetty versioksi 1.52-dev muutos `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Korjattu latinalaisten kirjainten lukeminen mandariinikiinaa käytettäessä. (#12952, #13572, #14197)
* Päivitetty LibLouis-pistekääntäjä versioksi [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Lisätty pistetaulukoita:
    * Kiinalainen yleinen pistekirjoitus (yksinkertaistetut merkit)
    * Ruandalainen kaunokirjallinen pistekirjoitus
    * Gandalainen kaunokirjallinen pistekirjoitus
    * Ruotsalainen lyhentämätön pistekirjoitus
    * Ruotsalainen osittainen lyhennekirjoitus
    * Ruotsalainen lyhennekirjoitus
    * Kiinalainen (Kiina, mandariini), nykyinen pistekirjoitusjärjestelmä (ei tooneja) (#14138)
* NVDA sisältää nyt käyttöjärjestelmän arkkitehtuurin osana käyttäjätilastojen seurantaa. (#14019)

### Bugikorjaukset

* - Kun NVDA päivitetään Windows Package Managerin komentoriviversion (winget) avulla, julkaistua NVDA:n versiota ei enää aina käsitellä uudempana kuin mitä tahansa asennettua alfaversiota. (#12469)
* NVDA ilmoittaa nyt asianmukaisesti ryhmäruudut Java-sovelluksissa. (#13962)
* Kohdistin seuraa asianmukaisesti puhuttua tekstiä jatkuvan luvun aikana sellaisissa sovelluksissa kuin Bookworm, WordPad tai NVDA:n lokintarkastelu. (#13420, #9179)
* Osittain valitut valintaruudut ilmoitetaan oikein UI Automation -rajapintaa käyttävissä ohjelmissa. (#13975)
* Suorituskykyä ja vakautta paranneltu Microsoft Visual Studiossa, Windows-päätteessä sekä muissa UI Automation -pohjaisissa sovelluksissa. (#11077, #11209)
  * Nämä korjaukset koskevat Windows 11 Sun Valley 2:ta (versio 22H2) ja sitä uudempia.
  * UI Automation -tapahtumien ja ominaisuusmuutosten valikoiva rekisteröinti on nyt oletusarvoisesti käytössä.
* Tekstin lukeminen, pistekirjoituksen tulostus sekä salasanan lukemisen estäminen toimivat nyt odotetusti Visual Studio 2022:n upotetussa Windows-pääte-säätimessä. (#14194)
* NVDA on nyt DPI-tietoinen useita näyttöjä käytettäessä.
Tehty useita korjauksia korkeampaa kuin 100 %:n DPI-asetusta tai useita näyttöjä käytettäessä.
Ongelmia saattaa edelleen esiintyä Windows 10 1809:ää vanhemmissa versioissa.
Jotta nämä korjaukset toimisivat, sovellusten, joiden kanssa NVDA on vuorovaikutuksessa, on myös oltava DPI-tietoisia.
Huomaa, että Chromessa ja Edgessä on edelleen tunnettuja ongelmia. (#13254)
  * Visuaalisten korostuskehysten sijoittamisen pitäisi nyt onnistua asianmukaisesti useimmissa sovelluksissa. (#13370, #3875, #12070)
  * Kosketusnäyttövuorovaikutuksen pitäisi nyt olla tarkkaa useimmissa sovelluksissa. (#7083)
  * Hiiren seurannan pitäisi nyt toimia useimmissa sovelluksissa. (#6722)
* Suuntatilan (vaaka/pysty) muutokset ohitetaan nyt oikein, kun muutosta ei tapahdu (esim. näytön muutokset). (#14035)
* NVDA ilmoittaa kohteiden vetämisestä näytöllä esim. uudelleenjärjesteltäessä Windows 10:n Käynnistä-valikon ruutuja ja virtuaalisia työpöytiä Windows 11:ssä. (#12271, #14081)
* Lisäasetusten "Ilmaise lokiin tallennetut virheet toistamalla ääni" -asetus palautetaan nyt asianmukaisesti oletusarvoonsa painettaessa "Palauta oletukset" -painiketta. (#14149)
* NVDA voi nyt valita tekstiä Java-sovelluksissa `NVDA+F10`-pikanäppäintä käyttäen. (#14163)
* NVDA ei enää juutu valikkoon liikuttaessa nuolilla ylös ja alas Microsoft Teamsin ketjutetuissa keskusteluissa. (#14355)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2022.3.3

Tämä on pieni julkaisu, joka korjaa 2022.3.2:ssa, 2022.3.1:ssä ja 2022.3:ssa ilmenneitä ongelmia.
Tämä versio korjaa myös tietoturvaongelman.

### Tietoturvakorjaukset

* Estää todentamattomien käyttäjien mahdollisen pääsyn järjestelmään (esim. NVDA:n Python-konsolin avulla). ([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Bugikorjaukset

* Korjattu bugi, joka aiheutti sen, että jos NVDA jää jumiin järjestelmää lukittaessa, NVDA sallii pääsyn työpöydälle Windowsin lukitusnäytöllä oltaessa. (#14416)
* Korjattu bugi, joka aiheutti sen, että jos NVDA jää jumiin järjestelmää lukittaessa, NVDA ei toimi oikein, ikään kuin laite olisi edelleen lukittu. (#14416)
* Korjattu Windowsin "unohdin PIN-koodini" -prosessin sekä päivitys/asennuskokemuksen saavutettavuusongelmia. (#14368)
* Korjattu bugi yritettäessä asentaa NVDA:ta joissakin Windows-ympäristöissä, esim. palvelinversiossa. (#14379)

### Muutokset kehittäjille

## 2022.3.2

Tämä on pieni julkaisu, joka korjaa 2022.3.1:n regressioita ja ratkaisee tietoturvaongelman.

### Tietoturvakorjaukset

* Estää todentamattomilta käyttäjiltä mahdollisen järjestelmätason pääsyn. ([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Bugikorjaukset

* Korjaa regression versiosta 2022.3.1, jossa tietyt toiminnot poistettiin käytöstä suojatuilla ruuduilla. (#14286)
* Korjaa regression versiosta 2022.3.1, jossa tietyt toiminnot poistettiin käytöstä sisäänkirjautumisen jälkeen, jos NVDA käynnistyi lukitusnäytöltä. (#14301)
 -

## 2022.3.1

Tämä on pieni julkaisu, joka korjaa useita tietoturvaongelmia.
Ilmoita tietoturvaongelmista vastuullisesti osoitteeseen <info@nvaccess.org>.

### Tietoturvakorjaukset

* Korjattu haavoittuvuus, jota hyväksikäyttäen käyttäjän oikeudet oli mahdollista nostaa järjestelmän oikeuksiksi. ([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Korjattu tietoturvaongelma, joka salli pääsyn Python-konsoliin lukitusnäytöllä kilpailutilanteen kautta NVDA:n käynnistyessä. ([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Korjattu ongelma, joka aiheutti puheentarkastelun tekstin tallentamisen välimuistiin, kun Windows lukitaan. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Bugikorjaukset

* Estä todentamatonta käyttäjää päivittämästä puheen- ja pistekirjoituksen tarkastelun asetuksia lukitusnäytöllä. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

NVDA:n kehitysyhteisö on antanut panoksensa merkittävään osaan tästä versiosta.
Se sisältää viivästetyt merkkikuvaukset ja parannetun Windows-konsolin tuen.

Tämä versio sisältää myös useita bugikorjauksia.
Erityisesti Adobe Acrobatin/Readerin uusimmat versiot eivät enää kaadu PDF-asiakirjaa luettaessa.

eSpeak on päivitetty, ja se sisältää 3 uutta kieltä: valkovenäjä, luxemburgi ja Pohjois-Ylämaan sekoitus.

### Uudet ominaisuudet

* Windows-konsoli-isäntä, jota käyttävät Komentokehote, PowerShell ja Windows-alijärjestelmä Linuxille Windows 11:n versiossa 22H2 (Sun Valley 2) ja uudemmissa:
  * Huomattavasti parantunut suorituskyky ja vakaus. (#10964)
  * Kun painetaan `Ctrl+F` tekstin etsimiseksi, tarkastelukohdistimen sijainti päivitetään seuraamaan löydettyä termiä. (#11172)
  * Sellaisen kirjoitetun tekstin puhuminen, joka ei näy ruudulla (esim. salasanat), on oletusarvoisesti pois käytöstä.
Se voidaan ottaa uudelleen käyttöön NVDA:n lisäasetusten paneelista. (#11554)
  * Ruudun ulkopuolelle vierittynyttä tekstiä voidaan tarkastella vierittämättä konsoli-ikkunaa. (#12669)
  * Yksityiskohtaisempia tekstin muotoilutietoja on käytettävissä. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Lisätty uusi puheasetus merkkikuvausten lukemiseksi viipeen jälkeen. (#13509)
* Lisätty uusi pistekirjoitusasetus, joka määrittää, keskeytyykö puhe vieritettäessä pistenäyttöä eteen/taaksepäin. (#2124)

### Muutokset

* eSpeak NG on päivitetty versioksi 1.52-dev muutos `9de65fcb`. (#13295)
  * Lisätty kieliä:
    * valkovenäjä
    * luxemburgi
    * Pohjois-Ylämaan sekoitus
* NVDA voi nyt ilmoittaa, kun solu on yhdistetty käytettäessä UI Automation -rajapintaa Microsoft Excelin laskentataulukon ohjausobjektien käyttämiseen. (#12843)
* Ilmoituksen "sisältää lisätietoja" sijaan sisällytetään nyt mahdollisuuksien mukaan tietojen tarkoitus, esim. "sisältää lisätiedon kommentti". (#13649)
* NVDA:n asennuskoko näkyy nyt Windowsin Ohjelmat ja toiminnot -osiossa. (#13909)

### Bugikorjaukset

* 64-bittinen Adobe Acrobat / Reader ei enää kaadu PDF-asiakirjaa luettaessa. (#12920)
  * Huomaa, että kaatumisen välttämiseksi tarvitaan myös Adobe Acrobatin / Readerin uusin versio.
* Fonttikoon mitat ovat nyt käännettävissä eri kielille. (#13573)
* Ohita Java Access Bridge -tapahtumat, joissa Java-sovelluksille ei löydy ikkunakahvaa.
Tämä parantaa joidenkin Java-sovellusten, mukaan lukien IntelliJ IDEA, suorituskykyä. (#13039)
* LibreOffice Calcin valittujen solujen ilmoittaminen on tehokkaampaa, eikä se enää johda Calcin jumiutumiseen useita soluja valittaessa. (#13232)
* Microsoft Edge ei ole enää käyttökelvoton toisena käyttäjänä suoritettaessa. (#13032)
* Kun nopeuden lisäys ei ole käytössä, eSpeakin puhenopeus ei enää putoa 99 %:n ja 100 %:n välille. (#13876)
* Korjattu bugi, joka mahdollisti kahden samanaikaisen Näppäinkomennot-valintaikkunan avautumisen. (#13854)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2022.2.4

Tämä versio korjaa tietoturvaongelman.

### Bugikorjaukset

* Korjattu hyökkäyskeino, jota hyväksi käyttäen oli mahdollista avata NVDA:n Python-konsoli lokintarkastelun kautta lukitusnäytössä. ([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Tämä julkaisu korjaa versiossa 2022.2.1 ilmenneen rajapinnan rikkoutumisen.

### Bugikorjaukset

* Korjattu bugi, jonka vuoksi NVDA ei ilmoittanut "Suojattu työpöytä" suojatulle työpöydälle siirryttäessä.
Tämä aiheutti sen, ettei Etäkäyttö-lisäosa tunnistanut suojattuja työpöytiä. (#14094)

## 2022.2.2

Tämä julkaisu korjaa versiossa 2022.2.1 ilmenneen näppäinkomentoihin liittyvän ongelman.

### Bugikorjaukset

* Korjattu bugi, joka aiheutti sen, etteivät näppäinkomennot aina toimineet. (#14065)

## 2022.2.1

Tämä on pieni julkaisu tietoturvaongelman korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti osoitteeseen <info@nvaccess.org>.

### Tietoturvakorjaukset

* Korjattu haavoittuvuus, jota hyväksikäyttäen Python-konsolia oli mahdollista ajaa lukitusnäytöltä. (GHSA-rmq3-vvhq-gp32)
* Korjattu haavoittuvuus, jota hyväksikäyttäen lukitusnäytöltä oli mahdollista poistua objektinavigoinnin avulla. (GHSA-rmq3-vvhq-gp32)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2022.2

Tämä versio sisältää useita bugikorjauksia.
Erityisesti Java-pohjaisiin sovelluksiin, pistenäyttöihin ja Windows-ominaisuuksiin on tehty merkittäviä parannuksia.

Uusia taulukkonavigointikomentoja on otettu käyttöön.
Unicode-CLDR on päivitetty.
LibLouis on päivitetty, joka sisältää uuden pistetaulukon.

### Uudet ominaisuudet

* Tuki vuorovaikutukselle Microsoftin silmukkakomponenttien kanssa Office-tuotteissa. (#13617)
* Uusia taulukkonavigointikomentoja on lisätty. (#957)
 * `Ctrl+Alt+Home/End` siirtää ensimmäiseen/viimeiseen sarakkeeseen.
 * `Ctrl+Alt+Page up/Page down` siirtää ensimmäiselle/viimeiselle riville.
* Lisätty ilman näppäinkomentoa oleva skripti, joka vaihtaa automaattisen kielen ja murteen vaihtamisen tilaa. (#10253)

### Muutokset

* NSIS on päivitetty versioksi 3.08. (#9134)
* Yhteinen Unicode-kielitietovarasto (CLDR) on päivitetty versioksi 41.0. (#13582)
* Päivitetty liblouis-pistekääntäjä versioksi [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Uusi pistetaulukko: saksa, taso 2 (yksityiskohtainen)
* Lisätty uusi rooli "varattu"-ilmaisinsäätimille. (#10644)
* NVDA ilmoittaa nyt, kun sen omaa toimintoa ei voi suorittaa. (#13500)
  * Tällaisia tilanteita ovat:
    * NVDA:n Microsoft Store -version käyttäminen.
    * Suojattu tila.
    * Vastauksen odottaminen modaalissa valintaikkunassa.

### Bugikorjaukset

* Korjauksia Java-pohjaisille sovelluksille:
  * NVDA ilmoittaa nyt vain luku -tyyppisen tilan. (#13692)
  * NVDA ilmoittaa nyt oikein ei käytössä/käytössä-tilan. (#10993)
  * NVDA ilmoittaa nyt funktionäppäimiä sisältävät pikanäppäimet. (#13643)
  * NVDA voi nyt ilmaista edistymispalkkien päivitykset äänimerkillä tai puhumalla. (#13594)
  * NVDA ei enää virheellisesti poista tekstiä widgeteistä näyttäessään niitä käyttäjälle. (#13102)
  * NVDA ilmoittaa nyt tilanvaihtopainikkeiden tilan. (#9728)
  * NVDA tunnistaa nyt ikkunan Java-sovelluksessa, jossa on useita ikkunoita. (#9184)
  * NVDA ilmoittaa nyt välilehtisäädinten sijaintitiedot. (#13744)
* Korjauksia pistekirjoitukseen:
  * Korjattu pistekirjoituksen tulostus liikuttaessa tietyssä tekstissä Mozillan monipuolisissa muokkaussäätimissä, kuten Thunderbirdin viestinkirjoitusikkunassa. (#12542)
  * Tekstintarkastelukomennot päivittävät nyt pistenäyttöä puhutulla sisällöllä, kun Pistenäyttö seuraa -asetukseksi on määritetty "automaattinen" ja hiirtä siirretään hiiren seurannan ollessa käytössä. (#11519)
  * Pistenäytöllä on nyt mahdollista siirtyä sisällössä tekstintarkastelukomentojen käytön jälkeen. (#8682)
* NVDA:n asennusohjelma toimii nyt erikoismerkkejä sisältävistä hakemistoista käynnistettynä. (#13270)
* Verkkosivujen kohteiden puhuminen ei enää epäonnistu Firefoxissa, kun aria-rowindex-, aria-colindex-, aria-rowcount- tai aria-colcount-attribuutit ovat virheellisiä. (#13405)
* Kohdistin ei enää vaihda riviä tai saraketta, kun käytetään taulukkonavigointia yhdistetyissä soluissa liikkumiseen. (#7278)
* Lomakekenttien (kuten valintaruutujen ja valintapainikkeiden) tyyppi ja tila ilmoitetaan nyt luettaessa ei-vuorovaikutteisia PDF:iä Adobe Readerissa. (#13285)
* "Palauta oletusasetukset" -toiminto on nyt käytettävissä NVDA-valikossa suojatussa tilassa. (#13547)
* Kaikkien lukittujen hiirinäppäinten lukitus avataan, kun NVDA sulkeutuu. Aiemmin ne pysyivät lukittuina. (#13410)
* Visual Studio ilmoittaa nyt rivinumerot. (#13604)
  * Huomaa, että ilmoittamisen toimimiseksi  rivinumeroiden näyttäminen on otettava käyttöön Visual Studiossa ja NVDA:ssa.
* Visual Studio ilmoittaa nyt oikein rivien sisennyksen. (#13574)
* NVDA ilmoittaa taas Käynnistä-valikon hakutuloksen tiedot uusimmissa Windows 10:n ja 11:n versioissa. (#13544)
* Windows 10:n ja 11:n Laskimen versiossa 10.1908 ja uudemmissa NVDA ilmoittaa tulokset useampia komentoja painettaessa, kuten esim. funktiotilassa. (#13383)
* Windows 11:ssä on taas mahdollista liikkua käyttöliittymäelementeissä, kuten Tehtäväpalkissa ja Tehtävänäkymässä, ja olla vuorovaikutuksessa niiden kanssa hiirtä ja kosketusvuorovaikutusta käyttäen. (#13506)
* NVDA ilmoittaa tilarivin sisällön Windows 11:n Muistiossa. (#13688)
* Navigointiobjektin korostus näkyy nyt heti ominaisuuden käyttöönoton jälkeen. (#13641)
* Korjattu yksisarakkeisten luettelonäkymäkohteiden lukeminen. (#13659, #13735)
* Korjattu ongelma, joka aiheutti sen, että eSpeakin automaattinen kielenvaihto otti käyttöön englantia ja ranskaa käytettäessä brittienglannin ja Ranskassa puhuttavan ranskan. (#13727)
* Korjattu OneCoren automaattinen kielenvaihto yritettäessä vaihtaa aiemmin asennettuun kieleen. (#13732)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2022.1

Tämä versio sisältää merkittäviä parannuksia MS Officen UIA-tukeen.
NVDA käyttää Windows 11:ssä oletusarvoisesti UI Automation -rajapintaa Microsoft Word -asiakirjoille Microsoft Office 16.0.15000:ssä ja uudemmissa.
Tämä parantaa merkittävästi suorituskykyä vanhaan objektimalliin verrattuna.

Parannuksia tehty pistenäyttöajureihin, Seika Notetaker, Papenmeier ja HID Braille mukaan lukien.
Lisäksi on erilaisia Windows 11:n bugikorjauksia laskin-, konsoli-, pääte- ja Sähköposti-sovelluksiin sekä emojipaneeliin.

ESpeak-NG ja LibLouis on päivitetty lisäten uuden japanilaisen, saksalaisen ja katalonialaisen pistetaulukon.

Huom:

 * Tämä versio rikkoo yhteensopivuuden olemassa olevien lisäosien kanssa.

### Uudet ominaisuudet

* Tuki muistiinpanojen ilmoittamiselle MS Excelissä UI Automation -rajapinnan ollessa käytössä Windows 11:ssä. (#12861)
* Kirjanmerkit, luonnoskommentit ja ratkaistut kommentit ilmoitetaan nyt sekä puheella että pistekirjoituksella Windows 11:ssä Microsoft Wordin uusimmissa koontikäännösversioissa UI Automation -rajapinnan välityksellä. (#12861)
* Uusi `--lang`-komentoriviparametri mahdollistaa NVDA:n asetuksissa määritetyn kielen ohittamisen. (#10044)
* NVDA varoittaa nyt komentoriviparametreista, jotka ovat tuntemattomia ja joita mitkään lisäosat eivät käytä. (#12795)
* NVDA käyttää nyt UI Automation -rajapinnan kautta käytettävässä Wordissa mathPlayeria Officen matemaattisten yhtälöiden lukemiseen ja niissä liikkumiseen. (#12946)
  * Jotta tämä toimisi, käytössä on oltava Microsoft Word 365:n/2016:n koontikäännösversio 14326 tai uudempi.
  * MathType-yhtälöt on myös muutettava manuaalisesti Office Mathiksi valitsemalla  ne ja valitsemalla sitten pikavalikosta Yhtälön valinnat -> Muunna Office Mathiksi.
* "Lisätietoja saatavilla" -ilmoitus ja siihen liittyvä yhteenvedon antava komento on päivitetty toimimaan vuorovaikutustilassa. (#13106)
* Seika Notetaker voidaan nyt tunnistaa automaattisesti USB:llä ja Bluetoothilla yhdistettäessä. (#13191, #13142)
  * Tämä vaikuttaa seuraaviin laitteisiin: MiniSeika (16 tai 24 solua), V6 sekä V6Pro (40 solua)
  * Nyt tuetaan myös Bluetooth-COM-portin manuaalista valitsemista.
* Lisätty komento Pistekirjoituksen tarkastelun käyttöön ottamiseen ja käytöstä poistamiseen. Oletusarvoista näppäinkomentoa ei ole määritetty. (#13258)
* Lisätty komennot pistenäytön useiden muokkausnäppäinten samanaikaiseen käyttöönottoon ja käytöstä poistamiseen. (#13152)
* Puhesanastovalintaikkunassa on nyt Poista kaikki -painike, jonka avulla koko sanaston tyhjentäminen on mahdollista. (#11802)
* Lisätty tuki Windows 11:n Laskin-sovellukselle. (#13212)
* Rivi- ja osanumeroiden lukeminen on nyt mahdollista Microsoft Wordissa UI Automation -rajapinnan ollessa käytössä Windows 11:ssä. (#13283, #13515)
* Microsoft Office 16.0.15000:ssa ja uudemmissa NVDA käyttää Windows 11:ssä oletusarvoisesti UI Automation -rajapintaa Word-asiakirjoissa, mikä parantaa merkittävästi suorituskykyä vanhaan objektimalliin verrattuna. (#13437)
 * Näitä ovat itsensä Wordin asiakirjat sekä myös Outlookin viestinluku- ja kirjoitusikkunat.

### Muutokset

* ESpeak-NG on päivitetty versioksi 1.51-dev muutos `7e5457f91e10`. (#12950)
* Liblouis-pistekääntäjä päivitetty versioksi [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Lisätty uusi pistetaulukko: japanilainen kaunokirjallinen pistekirjoitus (kantenji).
  * Lisätty uusi pistetaulukko: saksalainen 6 pisteen tietokonemerkistö.
  * Lisätty katalonialainen tason 1 pistetaulukko. (#13408)
* NVDA ilmoittaa valinnan ja yhdistetyt solut LibreOffice Calc 7.3:ssa ja uudemmissa. (#9310, #6897)
* Yhteinen Unicode-kielitietovarasto (CLDR) päivitetty versioksi 40.0. (#12999)
* `NVDA+Laskinnäppäimistön Del` -näppäinkomento ilmoittaa oletusarvoisesti järjestelmäkohdistimen tai aktiivisen objektin sijainnin. (#13060)
* `NVDA+Vaihto+Laskinnäppäimistön Del` ilmoittaa tarkastelukohdistimen sijainnin. (#13060)
* Lisätty  Freedom Scientificin pistenäytöille oletusnäppäinkomennot muokkausnäppäimien käyttöönottoon ja käytöstä poistamiseen. (#13152)
* Lue tekstin muotoilutiedot -komentoa (`NVDA+F`) käytettäessä ei enää ilmoiteta "perusviiva". (#11815)
* Pitkän kuvauksen näyttävällä komennolla ei enää ole määritettyä oletusarvoista näppäinkomentoa. (#13380)
* Lue lisätietojen yhteenveto -komennolla on nyt oletusarvoinen näppäinkomento (`NVDA+D`). (#13380)
* NVDA on käynnistettävä uudelleen MathPlayerin asennuksen jälkeen. (#13486)

### Bugikorjaukset

* Kohdistuksen ei pitäisi enää siirtyä virheellisesti leikepöydän hallinnan ruutuun joitakin Office-ohjelmia avattaessa. (#12736)
* NVDA ei enää tietyissä sovelluksissa, kuten verkkoselaimissa, kohteen aktivoimisen asemesta avaa vahingossa pikavalikkoa Järjestelmässä, jossa käyttäjä on vaihtanut ensisijaisen hiiripainikkeen vasemmasta oikeaksi. (#12642)
* "Alareuna" ilmoitetaan asianmukaisesti useammissa tilanteissa, kun tarkastelukohdistin siirretään tekstisäätimien lopun ohi esim. Microsoft Wordissa UI Automation -rajapinnan ollessa käytössä. (#12808)
* NVDA voi ilmoittaa system32-kansioon sijoitettujen binäärien sovellusnimen ja versionumeron 64-bittistä Windowsia käytettäessä. (#12943)
* Pääteohjelmien tulosteen lukemisen johdonmukaisuutta parannettu. (#12974)
  * Huomaa, että kohdistimen jälkeiset merkit saatetaan jälleen lukea joissakin tilanteissa, kun merkkejä lisätään rivin keskelle tai poistetaan niitä siitä.
* MS word, jossa on käytössä UIA: Otsikoiden pikanavigointi ei jää enää jumiin selaustilassa asiakirjan viimeiseen otsikkoon, eikä sitä näytetä kahdesti NVDA:n elementtilistassa. (#9540)
* Resurssienhallinnan tilapalkki voidaan nyt lukea Windows 8:ssa ja uudemmissa näppäinkomentoa NVDA+End (pöytäkoneet) / NVDA+Vaihto+End (kannettavat) käyttäen. (#12845)
* Skype for Businessin keskustelun saapuvat viestit luetaan jälleen. (#9295)
* NVDA voi jälleen vaimentaa ääntä Windows 11:ssä SAPI 5 -syntetisaattoria käytettäessä. (#12913)
* NVDA lukee historia- ja muisti-luettelokohteiden selitteet Windows 10:n Laskin-sovelluksessa. (#11858)
* Sellaiset näppäinkomennot kuten vierittäminen ja kohdistimen siirto kosketuskohdistinnäppäimillä toimivat jälleen HID Braille -protokollaa käyttävillä laitteilla. (#13228)
* Windows 11:n Sähköposti-sovellus: Kun sovellusten välillä vaihdetaan pitkää viestiä luettaessa, NVDA ei jää enää jumiin kyseisen viestin jollekin riville. (#13050)
* Moniosaiset näppäinkomennot (esim. `väli+piste 4`) voidaan suorittaa onnistuneesti HID Braille -protokollaa käyttävissä pistenäytöissä. (#13326)
* Korjattu ongelma, joka aiheutti sen, että  useiden asetusvalintaikkunoiden avaaminen samanaikaisesti oli mahdollista. (#12818)
* Korjattu ongelma, joka aiheutti sen, että jotkin Focus Blue -pistenäytöt lakkasivat toimimasta sen jälkeen kun tietokone herätettiin lepotilasta. (#9830)
* "Perusviiva"-ilmoitusta ei tapahdu enää asiaankuulumattomasti, kun "Ilmaise ylä- ja alaindeksit" -asetus on käytössä. (#11078)
* NVDA ei enää estä Windows 11:ssä emojipaneelissa liikkumista emojeita valittaessa. (#13104)
* Estetty bugi, joka aiheutti tekstin lukemista kahteen kertaan Windows-konsolia ja -päätettä käytettäessä. (#13261)
* Korjattu useita tapauksia, joissa luettelokohteita ei voitu lukea 64-bittisissä sovelluksissa, kuten REAPERissa. (#8175)
* NVDA vaihtaa nyt automaattisesti vuorovaikutustilaan Microsoft Edgen lataustenhallinnassa, kun kohdistus siirtyy uusimman latauksen sisältävään luettelokohteeseen. (#13221)
* NVDA ei enää aiheuta 64-bittisen Notepad++ 8.3:n ja uudempien kaatumista. (#13311)
* Adobe Reader ei enää kaadu käynnistettäessä, mikäli sen suojattu tila on käytössä. (#11568)
* Korjattu bugi, joka aiheutti NVDA:n kaatumisen Papenmeier-pistenäyttöajuria valittaessa. (#13348)
* Sivunumeroa ja muuta muotoilua ei enää puhuta asiaankuulumattomasti Microsoft wordissa UIA:n ollessa käytössä siirryttäessä tyhjästä taulukon solusta sellaiseen soluun, jossa on sisältöä, tai asiakirjan lopusta olemassa olevaan sisältöön. (#13458, #13459)
* NVDA ei jätä enää ilmoittamatta sivun otsikkoa ja käynnistämättä automaattista lukemista sivun latautuessa Google chrome 100:ssa. (#13571)
* NVDA ei enää kaadu, kun sen oletusasetukset palautetaan "Puhu komentonäppäimet" -asetuksen ollessa käytössä. (#13634)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2021.3.5

Tämä on pieni julkaisu tietoturvaongelman korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti osoitteeseen <info@nvaccess.org>.

### Tietoturvakorjaukset

* Ratkaistu tietoturvavaroitus `GHSA-xc5m-v23f-pgr7`.
  * Välimerkkien ja symbolien puhumisen valintaikkuna on nyt poissa käytöstä suojatussa tilassa.

## 2021.3.4

Tämä on pieni julkaisu useiden esiin tulleiden tietoturvaongelmien korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti osoitteeseen <info@nvaccess.org>.

### Tietoturvakorjaukset

* Ratkaistu tietoturvavaroitus `GHSA-354r-wr4v-cx28`. (#13488)
  * Poistettu mahdollisuus NVDA:n käynnistämiseen ja virheenkorjauslokin käyttöönottamiseen, kun NVDA on käynnissä suojatussa tilassa.
  * Poistettu mahdollisuus NVDA:n päivittämiseen, kun se on käynnissä suojatussa tilassa.
* Ratkaistu tietoturvavaroitus `GHSA-wg65-7r23-h6p9`. (#13489)
  * Poistettu mahdollisuus Näppäinkomennot-valintaikkunan avaamiseen suojatussa tilassa.
  * Poistettu mahdollisuus oletus-, tilapäis- ja äänikohtaisten puhesanastovalintaikkunoiden avaamiseen suojatussa tilassa.
* Ratkaistu tietoturvavaroitus `GHSA-mvc8-5rv9-w3hx`. (#13487)
  * WX-käyttöliittymän tarkastelutyökalu on nyt poissa käytöstä suojatussa tilassa.

## 2021.3.3

Tämä julkaisu on identtinen 2021.3.2:n kanssa.
NVDA 2021.3.2:ssa oli bugi, joka sai sen tunnistamaan itsensä virheellisesti 2021.3.1:ksi.
Tämä julkaisu ilmoittaa oikein olevansa 2021.3.3.

## 2021.3.2

Tämä on pieni julkaisu useiden esiin tulleiden tietoturvaongelmien korjaamiseksi.
Ilmoita tietoturvaongelmista vastuullisesti osoitteeseen <info@nvaccess.org>.

### Bugikorjaukset

* - Tietosuojakorjaus: Objektinavigointi estetään lukitusnäytön ulkopuolella Windows 10:ssä ja 11:ssä. (#13328)
* Tietosuojakorjaus: Lisäosien hallinnan valintaikkuna on nyt poissa käytöstä suojatuissa ruuduissa. (#13059)
* Tietosuojakorjaus: NVDA:n tilannekohtainen ohje ei enää ole käytettävissä suojatuissa ruuduissa. (#13353)
 -

## 2021.3.1

Tämä on pieni päivitys, joka korjaa useita  version 2021.3 ongelmia.

### Muutokset

* Uutta HID Braille -protokollaa ei enää aseteta etusijalle, jos muutakin pistenäyttöajuria voidaan käyttää. (#13153)
* Uusi HID Braille -protokolla voidaan poistaa käytöstä Lisäasetukset-paneelin asetuksella. (#13180)

### Bugikorjaukset

* Kiintopiste näytetään taas pistekirjoituksella lyhennettynä. #13158
* Korjattu Humanware Brailliant- ja APH Mantis Q40 -pistenäyttöjen epävakaa automaattinen tunnistus Bluetoothia käytettäessä. (#13153)

## 2021.3

Tämä versio lisää tuen uudelle HID Braille -protokollalle.
Sen tarkoituksena on standardoida pistenäyttöjen tuki, jossa ei tarvita valmistajakohtaisia ajureita.
Päivityksiä eSpeak-NG:hen ja LibLouis-pistekääntäjään, mukaan lukien uusi venäläinen ja vendalainen taulukko.
Virheäänet voidaan ottaa käyttöön NVDA:n vakaissa versioissa uudella Lisäasetukset-paneelin asetuksella.
Jatkuva luku vierittää nyt näkymää Wordissa pitääkseen nykyisen sijainnin näkyvissä.
Paljon parannuksia käytettäessä Officea UIA:n kanssa.
Eräs UIA-korjaus on, että Outlook jättää nyt huomiotta viesteissä useammantyyppisiä asettelutaulukoita.

Tärkeitä huomautuksia:

Suojausvarmenteemme päivityksen vuoksi pieni määrä käyttäjiä saa virheilmoituksen, kun NVDA 2021.2 tarkistaa päivityksiä.
NVDA pyytää nyt Windowsia päivittämään suojausvarmenteet, mikä estää tämän virheen tulevaisuudessa.
Asianomaisten käyttäjien on ladattava tämä päivitys manuaalisesti.

### Uudet ominaisuudet

* Lisätty näppäinkomento solun reunojen tyylin ilmaisemisasetuksen vaihtamiseen. (#10408)
* Tuki uudelle HID Braille -määritykselle, jonka tarkoituksena on pistenäyttötuen standardointi. (#12523)
 * NVDA tunnistaa Tätä määritystä tukevat laitteet automaattisesti.
 * Tekniset tiedot tämän määrityksen NVDA-toteutuksesta ovat osoitteessa https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Lisätty tuki VisioBraille Vario 4 -pistenäytölle. (#12607)
* Virheilmoitukset voidaan ottaa käyttöön lisäasetuksista mitä tahansa NVDA:n versiota käytettäessä. (#12672)
* NVDA puhuu Windows 10:ssä ja uudemmissa ehdotusten määrän kirjoitettaessa hakuehtoja sellaisissa sovelluksissa kuin Asetukset ja Microsoft Store. (#7330, #12758, #12790)
* Taulukossa liikkumista tuetaan nyt ruudukkosäätimissä, jotka on luotu PowerShellin Out-GridView-cmdlet-komentoa käyttäen. (#12928)

### Muutokset

* Espeak-NG on päivitetty versioksi 1.51-dev muutos `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* NVDA käyttää oletusarvoisesti eSpeakia, mikäli asennetut OneCore-äänet eivät tue NVDA:n käyttämää kieltä. (#10451)
* Mikäli OneCore-äänet eivät johdonmukaisesti puhu mitään, palataan käyttämään eSpeak-syntetisaattoria. (#11544)
* Kun tilarivi luetaan `NVDA+End`-näppäinkomennolla, tarkastelukohdistinta ei enää siirretä sen kohdalle.
Mikäli tarvitset tätä toiminnallisuutta, määritä näppäinkomento asianmukaiselle skriptille Näppäinkomennot-valintaikkunan Objektinavigointi-kategoriassa. (#8600)
* Kun avaat jo avatun valintaikkunan, NVDA ei näytä enää virhettä vaan siirtää kohdistuksen avoimeen valintaikkunaan. (#5383)
* Päivitetty liblouis-pistekääntäjä versioksi [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
 * Uusia pistetaulukoita: venäläinen taso 1, venda taso 1, venda taso 2
* "Merkitty sisältö" tai "mrkt" -ilmoitusten asemesta sanotaan "korostus" tai näytetään pistenäytöllä "krt". (#12892)
* NVDA ei enää yritä sulkeutua, kun valintaikkunat odottavat vaadittua toimenpidettä (esim. OK/Peruuta). (#12984)

### Bugikorjaukset

* Kun NVDA palautuu virheestä, näppäimistön muokkausnäppäinten (kuten Ctrl tai Ins) seuranta on vikasietoisempaa. (#12609)
* NVDA-päivitysten tarkistaminen on jälleen mahdollista tietyissä järjestelmissä, esim. puhtaissa Windows-asennuksissa. (#12729)
* NVDA ilmaisee asianmukaisesti tyhjät taulukon solut Microsoft Wordissa UI automation -rajapintaa käytettäessä. (#11043)
* Verkon ARIA-tietoruudukon soluissa Esc-näppäimen painallus välitetään nyt kyseiselle ruudukolle, eikä enää poista kohdistustilaa ehdottomasti käytöstä. (#12413)
* Korjattu sarakenimen kahdesti puhuminen Chromessa taulukon otsikkosolua luettaessa. (#10840)
* NVDA ei enää ilmoita numeerista arvoa UIA-liukusäätimissä, joiden arvo on määritetty tekstinä. (UIA:n ValuePattern asetetaan nyt etusijalle RangeValuePattern:in asemesta). (#12724)
* NVDA ei enää käsittele UIA-liukusäätimien arvoa aina prosentteina.
* Solun sijainnin ilmoittaminen Microsoft Excelissä toimii taas oikein Windows 11:ssä UI Automation -rajapintaa käytettäessä. (#12782)
* NVDA ei enää määritä virheellisiä Pythonin kieliasetuksia. (#12753)
* Jos käytöstä poistettu lisäosa poistetaan ja asennetaan sitten uudelleen, se otetaan uudelleen käyttöön. (#12792)
* Korjattu bugeja lisäosien päivittämisessä ja poistamisessa, jos lisäosakansio on nimetty uudelleen tai sisältää avoimia tiedostoja. (#12792, #12629)
* Kun Microsoft Excel -laskentataulukon säätimissä käytetään UI Automation -rajapintaa, NVDA ei enää ilmoita tarpeettomasti valittuna olevaa yksittäistä solua. (#12530)
* LibreOffice Writerin valintaikkunoissa (esim. vahvistusta kysyvissä) luetaan automaattisesti enemmän tekstiä. (#11687)
* Microsoft Wordin Selaustilassa luettaessa/navigoitaessa UI automation -rajapintaa käytettäessä varmistetaan, että asiakirjaa vieritetään aina siten, että nykyinen selaustilakohdistimen sijainti on näkyvissä ja että kohdistimen sijainti kohdistustilassa vastaa asianmukaisesti selaustilakohdistimen sijaintia. (#9611)
* Asiakirjaa vieritetään nyt automaattisesti ja kohdistimen sijainti päivitetään asianmukaisesti Microsoft Wordissa jatkuvaa lukua käytettäessä UI automation -rajapinnan ollessa käytössä. (#9611)
* Kun NVDA käyttää Outlookissa sähköposteja luettaessa UI Automation -rajapintaa, tiyetyt taulukot merkitään nyt asettelutaulukoiksi, mikä tarkoittaa, ettei niitä ilmaista oletusarvoisesti. (#11430)
* Korjattu harvinainen virhe äänilaitteiden vaihdossa. (#12620)
* Pistekirjoituksen syötön  pitäisi toimia luotettavammin muokkauskentissä kaunokirjallisia pistetaulukkoja käytettäessä. (#12667)
* NVDA ilmoittaa nyt viikonpäivän kokonaisuudessaan Windowsin ilmoitusalueen kalenterissa liikuttaessa. (#12757)
* Pistenäytön vierittäminen eteen- ja taaksepäin ei enää siirrä virheellisesti takaisin kohdistimen alkuperäiseen sijaintiin Microsoft Wordissa käytettäessä kiinalaista syöttömenetelmää, kuten Taiwan - Microsoft Quick. (#12855)
* Kun Microsoft Word -asiakirjojen lukemiseen käytetään UIA:ta, virkkeittäin liikkuminen (Alt+Alanuoli / Alt+Ylänuoli) on taas mahdollista. (#9254)
* Kappalesisennykset ilmoitetaan, kun MS Wordia käytetään UIA:n kautta. (#12899(
* Muutostenjäljityskomento ja jotkin muut lokalisoidut komennot puhutaan, kun MS Wordia käytetään UIA:n kautta. (#12904)
* Korjattu kaksinkertainen pistekirjoituksen ja puheen tuottaminen, kun "kuvaus" on sama kuin "sisältö" tai "nimi". (#12888)
* Kirjoitusvirheäänien toistaminen on nyt tarkempaa kirjoitettaessa MS Wordissa UIA:n ollessa käytössä. (#12161)
* NVDA ei enää sano "ruutu" Windows 11:ssä vaihdettaessa ohjelmien välillä Alt+Sarkain-näppäinyhdistelmällä. (#12648)
* Modernien kommenttien sivupaneelia tuetaan nyt MS Wordissa, kun UIA ei ole käytössä. Siirry sivupaneelin ja asiakirjan välillä painamalla Alt+F12. (#12982)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2021.2

Tämä versio esittelee alustavan Windows 11 -tuen.
Testaus on suoritettu käyttöjärjestelmän esiversioilla, koska lopullista versiota ei ole vielä julkaistu.
Tähän sisältyy tärkeä näyttöverhon korjaus (katso tärkeät huomautukset).
COM-rekisteröintien korjaustyökalu voi ratkaista useampia NVDA:n käytössä ilmeneviä ongelmia.
eSpeak-syntetisaattoria ja LibLouis-pistekääntäjää on päivitetty.
Lisäksi useita bugikorjauksia ja parannuksia erityisesti pistekirjoitustukeen, Windows-päätteisiin, laskimeen, emojipaneeliin sekä leikepöydän historiaan.

### Tärkeitä huomautuksia

Windowsin suurennusrajapintaan tehdyn muutoksen takia näyttöverho oli päivitettävä tukemaan uusimpia Windows-versioita.
Käytä NVDA 2021.2:ta aktivoidaksesi näyttöverhon Windows 10:n versiossa 21H2 (10.0.19044) tai uudemmissa.
Näihin kuuluvat Windows 10:n Insider-versiot sekä Windows 11.
Turvallisuussyistä uutta Windows-versiota käytettäessä näytetäänvahvistusviesti siitä, että näyttöverho pimentää ruudun kokonaan.

### Uudet ominaisuudet

* Kokeellinen tuki ARIA-merkinnöille:
 * Lisää komennon objektin ARIA-lisätietojen yhteenvedon lukemiseen. (#12364)
 * Lisää Lisäasetukset-paneeliin asetuksen objektin lisätietojen ilmoittamiseen selaustilassa. (#12439)
* NVDA kertoo ehdotusten lukumäärän resurssienhallinnassa hakuja suoritettaessa Windows 10:n versiossa 1909 ja uudemmissa (Windows 11 mukaan lukien). (#10341, #12628)
* NVDA kertoo nyt painettaessa tavallisen ja riippuvan sisennyksen näppäinkomentojen tulokset Microsoft Wordissa. (#6269)

### Muutokset

* eSpeak-NG on päivitetty versioksi 1.51-dev muutos `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* NVDA sanoo "artikkeli" sisällön jälkeen, jos artikkeli-valintaruutu on valittu asetusvalintaikkunan Asiakirjojen muotoilu -paneelissa. (#11103)
* Päivitetty liblouis-pistekääntäjä versioksi [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
 * Uusia pistetaulukoita: bulgarialainen taso 1, burmalainen taso 1, burmalainen taso 2, kazakkilainen taso 1, khmeriläinen taso 1, pohjoiskurdilainen taso 0, sepediläinen taso 1, sepediläinen taso 2, sesotholainen taso 1, sesotholainen taso 2, setswanalainen taso 1, setswanalainen taso 2, tataarilainen taso 1, vietnamilainen taso 0, vietnamilainen taso 2, etelävietnamilainen taso 1, xhosalainen taso 1, xhosalainen taso 2, jakuuttilainen taso 1, zululainen taso 1, zululainen taso 2.
* Windows 10:n tekstintunnistus nimettiin uudelleen Windowsin tekstintunnistukseksi. (#12690)

### Bugikorjaukset

* NVDA näyttää laskutoimitukset pistenäytöllä Windows 10:n Laskimessa. (#12268)
* Kun pääteohjelmissa lisätään tai poistetaan merkkejä rivin keskellä, kohdistimen oikealla puolella olevia merkkejä ei enää lueta Windows 10:n versiossa 1607 ja uudemmissa. (#3200)
 * Diff Match Patch on nyt käytössä oletusarvoisesti. (#12485)
* Pistekirjoituksen syöttö toimii oikein seuraavilla lyhennepistetaulukoilla: arabialainen taso 2, espanjalainen taso 2, urdulainen taso 2, mandariinikiina (Kiina) taso 2. (#12541)
* COM-rekisteröintien korjaustyökalu ratkaisee nyt useampia ongelmia, erityisesti 64-bittisessä Windowsissa. (#12560)
* Parannuksia Nippon Telesoftin Seika Notetaker -pistenäytön näppäinten käsittelyyn. (#12598)
* Parannuksia Windowsin emojipaneelin ja leikepöydän historian puhumiseen. (#11485)
* Päivitetty bengalilaisten aakkosten merkkikuvaukset. (#12502)
* NVDA sulkeutuu turvallisesti, kun uusi prosessi käynnistetään. (#12605)
* Handy Tech -pistenäyttöajurin uudelleenvalitseminen Valitse pistenäyttö -valintaikkunasta ei aiheuta enää virheitä. (#12618)
* Windowsin versio 10.0.22000 ja uudemmat tunnistetaan Windows 11:ksi, ei Windows 10:ksi. (#12626)
* Näyttöverhon tuki on korjattu ja testattu Windowsin versioon 10.0.22000 asti. (#12684)
* Näppäinkomentojen valintaikkuna toimii odotetusti, mikäli hakutuloksia ei näytetä näppäinkomentoja suodatettaessa. (#12673)
* Korjattu bugi, jossa alivalikon ensimmäistä kohdetta ei puhuta joissakin tilanteissa. (#12624)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2021.1

Tämä versio sisältää valinnaisen kokeellisen UIA-tuen Excelille ja Chromium-pohjaisille selaimille.
Korjauksia useille kielille sekä linkkien käyttämiseen pistenäytöltä.
Päivityksiä Unicode-CLDR:ään, matemaattisiin symboleihin ja LibLouis-pistekääntäjään.
Lisäksi useita bugikorjauksia ja parannuksia esim. Officeen, Visual Studioon sekä useisiin kieliin.

Huom:

* Tämä versio rikkoo olemassa olevien lisäosien yhteensopivuuden.
* Adobe Flashia ei myöskään enää tueta.

### Uudet ominaisuudet

* Alkeellinen tuki UIA:lle Chromium-pohjaisissa selaimissa (kuten Edge). (#12025)
* Valinnainen kokeellinen UI Automation -tuki Microsoft Excelille. Suositellaan vain Excelin versiolle 16.0.13522.10000 tai uudemmalle. (#12210)
* Helpompi liikkuminen NVDA:n Python-konsolin tulosteessa. (#9784)
 * Alt+ylä/alanuoli siirtää edelliseen/seuraavaan tulokseen (lisää komentoon Vaihto valitaksesi).
 * Ctrl+L tyhjentää tulosteruudun.
* NVDA ilmoittaa nyt Microsoft Outlookissa tapaamiseen liitetyt kategoriat, mikäli sellaisia on. (#11598)
* Tuki Nippon Telesoftin Seika Notetaker -pistenäytölle. (#11514)

### Muutokset

* Säätimiä on nyt mahdollista aktivoida niiden kuvauksen kohdalta (esim. "lnk" linkillä) selaustilassa pistenäytön kosketuskohdistinnäppäimillä. Tämä on erityisen hyödyllistä esim. nimettömiä valintaruutuja aktivoitaessa. (#7447)
* NVDA estää nyt käyttäjää suorittamasta Windows 10:n tekstintunnistusta, jos näyttöverho on käytössä. (#11911)
* Päivitetty Yhteinen Unicode-kielitietovarasto (CLDR) versioksi 39.0. (#11943, #12314)
* Matemaattisia merkkejä lisätty symbolisanastoon. (#11467)
* Käyttöoppaan, mitä uutta -dokumentin ja näppäinkomentojen pikaoppaan ulkoasu on päivitetty. (#12027)
* "Ei tueta" ilmoitetaan nyt yritettäessä vaihtaa ruutuasettelun tilaa sovelluksissa (kuten Microsoft Word), jotka eivät tue sitä. (#7297)
* Lisäasetukset-paneelin "Yritä perua vanhentuneiden kohdistustapahtumien puhe" -asetus on nyt oletusarvoisesti käytössä. (#10885)
 * Toiminto voidaan poistaa käytöstä määrittämällä tämän asetuksen arvoksi "Ei".
 * Verkkopohjaisissa sovelluksissa (esim. Gmail) ei enää puhuta vanhentunutta tietoa siirrettäessä kohdistusta nopeasti.
* Liblouis-pistekääntäjä päivitetty versioksi [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
 * Uusia pistetaulukoita: valkovenäläinen kaunokirjallisuuden pistekirjoitus, valkovenäläinen tietokonemerkistö, urdu taso 1, urdu taso 2.
* Adobe Flash -sisällön tuki on poistettu NVDA:sta, koska Adobe on aktiivisesti varoittanut Flashin käytöstä. (#11131)
* NVDA sulkeutuu, vaikka sen ikkunoita olisi avoinna. Sulkeutumisprosessi sulkee nyt kaikki NVDA:n ikkunat ja valintaikkunat. (#1740)
* Puheen tarkastelu -ikkuna voidaan nyt sulkea Alt+F4-näppäinyhdistelmällä, ja siinä on tavallinen Sulje-painike, joka helpottaa vuorovaikutusta osoitinlaitteiden käyttäjille. (#12330)
* Pistekirjoituksen tarkastelu -ikkunassa on tavallinen Sulje-painike, joka helpottaa vuorovaikutusta osoitinlaitteiden käyttäjille. (#12328)
* Elementtilista-valintaikkunan Aktivoi-painikkeen pikanäppäin on poistettu joistakin kielistä, jotta vältetään yhteentörmäys elementtityyppivalintapainikkeen nimen kanssa. Kun painike on käytettävissä, se on edelleen valintaikkunan oletuspainike ja voidaan aktivoida painamalla Enteriä kuten ennenkin. (#6167)

### Bugikorjaukset

* Viestiluettelo on taas luettavissa Outlook 2010:ssä. (#12241)
* Kun pääteohjelmissa poistetaan tai lisätään merkkejä keskellä riviä Windows 10:n versiossa 1607 ja uudemmissa, kohdistimen oikealla puolella olevia merkkejä ei enää lueta. (#3200)
 * Tämä kokeellinen korjaus on otettava käyttöön manuaalisesti NVDA:n Lisäasetukset-paneelista muuttamalla Muutosten havaitsemismenetelmä -asetuksen arvoksi Diff Match Patch.
* Virheellisiä etäisyysilmoituksia ei pitäisi enää tapahtua MS Outlookissa siirryttäessä Vaihto+Sarkain-näppäinyhdistelmällä viestirungosta aihekenttään. (#10254)
* Python-konsolissa tuetaan nyt sarkainsisennyksen lisäämistä sellaisen syöttörivin alkuun, joka ei ole tyhjä, ja sarkaintäydennyksen suorittamista syöttörivin keskellä. (#11532)
* Muotoilutiedoissa ja  muissa selaustilassa näytettävissä ilmoituksissa ei enää näytetä odottamattomia tyhjiä rivejä, kun ruutuasettelu on poistettu käytöstä. (#12004)
* MS Wordissa on nyt mahdollista lukea kommentteja UIA:n ollessa käytössä. (#9285)
* Vuorovaikutuksen suorituskykyä Visual Studiossa on parannettu. (#12171)
* Korjattu graafisia bugeja, kuten puuttuvia elementtejä käytettäessä NVDA:ta oikealta vasemmalle luettavalla kielellä. (#8859)
* Noudattaa graafisen käyttöliittymän ulkoasun suuntaa NVDA:n kielen mukaisesti, ei järjestelmäkielen. (#638)
 * Tunnettu ongelma oikealta vasemmalle luettavissa kielissä: Selitteet/säätimet katkaisevat ryhmien oikean reunan. (#12181)
* Pythonin kielialue asetetaan samaksi kuin NVDA:n asetuksissa määritetty kieli, ja tämä tapahtuu oletuskieltä käytettäessä. (#12214)
* TextInfo.getTextInChunks ei enää jumiudu kutsuttaessa Rich Edit -säätimissä, kuten NVDA:n lokin tarkastelussa. (#11613)
* NVDA:ta on taas mahdollista käyttää Windows 10:n versioissa 1803 ja 1809 kielillä, joiden nimissä on alaviivoja, kuten de_CH. (#12250)
* Ylä/alaindeksin ilmoittaminen toimii WordPadissa odotetulla tavalla. (#12262)
* NVDA ei jätä enää ilmoittamatta vasta kohdistettua sisältöä verkkosivulla, mikäli entinen kohdistus katoaa ja korvataan uudella samassa sijainnissa. (#12147)
* Kokonaisten Excel-solujen yliviivaus, yläindeksi ja alaindeksi-muotoilut ilmoitetaan, mikäli vastaava asetus on käytössä. (#12264)
* Korjattu asetusten kopiointi massamuistiversiosta asentamisen aikana, kun oletusarvoinen asetusten kohdehakemisto on tyhjä. (#12071, #12205)
* Korjattu joidenkin aksentillisten tai diakriittisten kirjainten virheellinen sanominen, kun Ilmaise isot kirjaimet sanomalla "iso" -asetus on käytössä. (#11948)
* Korjattu virhe SAPI 4 -puhesyntetisaattorin äänenkorkeutta muutettaessa. (#12311)
* Nyt myös NVDA:n asennusohjelma huomioi `--minimal`-komentoriviparametrin, eikä soita käynnistysääntä noudattaen samaa dokumentoitua käyttäytymistä kuin asennetun tai massamuistiversion nvda.exe. (#12289)
* Taulukkoon siirtävä pikanavigointikomento voi nyt siirtää asettelutaulukkoon MS Wordissa tai Outlookissa, mikäli "Sisällytä asettelutaulukot" -asetus on otettu käyttöön selaustilan asetuksista. (#11899)
* NVDA ei enää sano tietyissä kielissä emojien kohdalla "↑↑↑". (#11963)
* eSpeak tukee taas kantonin- ja mandariinikiinaa. (#10418)
* Tekstikentät, kuten osoitepalkki puhutaan nyt uudessa Chromium-pohjaisessa Microsoft Edgessä, kun ne ovat tyhjiä. (#12474)
* Seika-pistenäyttöjen ajuri korjattu. (#10787)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2020.4

Tämä versio sisältää uusia kiinalaisia syöttömenetelmiä ja päivitetyn Liblouis-pistekääntäjän sekä elementtilistan.
Tilannekohtainen ohje on nyt käytettävissä painettaessa F1 NVDA:n valintaikkunoissa.
Parannuksia symbolien lausumissääntöihin, puhesanastoihin, pistekirjoitusilmoituksiin ja pikalukuun.
Bugikorjauksia ja parannuksia Sähköposti-sovellukseen, Outlookiin, Teamsiin, Visual Studioon, Azure Data Studioon sekä Foobar2000:een.
Verkkosivujen käyttöön liittyen on parannuksia Google Docsiin sekä parempi tuki ARIAlle.
Lisäksi monia muita tärkeitä bugikorjauksia ja parannuksia.

### Uudet ominaisuudet

* F1:n painaminen NVDA:n valintaikkunoissa avaa nyt käyttöoppaan asianmukaisimman osion kohdalta. (#7757)
* Automaattisen täydennyksen ehdotuksia (IntelliSense) tuetaan Microsoft SQL Server Management Studiossa sekä Visual Studio 2017:ssä ja sitä uudemmissa. (#7504)
* Merkkien lausuminen: Tuki monimutkaisten merkkimääritysten ryhmittelylle ja korvaussääntöjen ryhmäviittauksille, mikä tekee niistä yksinkertaisempia ja tehokkaampia. (#11107)
* Käyttäjille ilmoitetaan nyt heidän yrittäessään luoda puhesanastomerkintöjä virheellisillä sääntölausekkeen korvauksilla. (#11407)
 * Erityisesti ryhmittelyvirheet havaitaan.
* Lisätty tuki Windows 10:n uusille perinteisen kiinan pika- ja Pinyin-syöttömenetelmille. (#11562)
* Välilehtien otsakkeet käsitellään nyt lomakekenttinä f-pikanavigointinäppäintä käytettäessä. (#10432)
* Lisätty komento merkityn (korostetun) tekstin ilmaisemisen käyttöön ottamiselle ja käytöstä poistamiselle. Oletusarvoista näppäinkomentoa ei ole määritetty. (#11807)
* Lisätty --copy-portable-config-komentoriviparametri, jonka avulla voit kopioida antamasi asetukset automaattisesti nykyiseen käyttäjätiliin suorittaessasi NVDA:n hiljaista asennusta. (#9676)
* Pistesoluun siirtämistä tuetaan nyt hiiren käyttäjille Pistekirjoituksen tarkastelu -toiminnossa. Vie hiiri merkin päälle siirtyäksesi kyseiseen soluun. (#11804)
* NVDA tunnistaa nyt automaattisesti Humanware Brailliant BI 40X- ja 20X-pistenäytöt sekä USB:llä että Bluetoothilla. (#11819)

### Muutokset

* Päivitetty liblouis-pistekääntäjä versioksi 3.16.1:
 * Korjaa useita kaatumisia
 * Lisää baškiirinkielisen tason 1 pistetaulukon.
 * Lisää taulukon koptinkieliselle 8 pisteen tietokonemerkistölle.
 * Lisää taulukot venäläiselle kaunokirjallisuuden pistekirjoitukselle sekä venäläiselle yksityiskohtaiselle kaunokirjallisuuden pistekirjoitukselle.
 * Poistaa venäläisen tason 1 pistetaulukon
* Etsi seuraava- ja Etsi edellinen -komennot eivät keskeytä lukemista selaustilassa jatkuvaa lukua käytettäessä, jos Salli pikaluku jatkuvassa luvussa -asetus on käytössä. Jatkuva luku jatkaa sen sijaan seuraavan tai edellisen löytyneen hakusanan jälkeen. (#11563)
* F3 on uudelleenmääritelty HIMS-pistenäytöissä komennoksi Väli+pisteet 1, 4 ja 8. (#11710)
* Parannuksia pistekirjoituksen "Ilmoitusten aikakatkaisu"- ja "Näytä ilmoitukset pysyvästi" -asetusten käyttöliittymään. (#11602)
* Elementtilista-valintaikkuna (NVDA+F7) voidaan nyt avata vuorovaikutustilassa verkkoselaimissa ja muissa selaustilaa tukevissa sovelluksissa. (#10453)
* Aktiivisten ARIA-alueiden päivitykset estetään, kun dynaamisen sisällön muutosten puhuminen on poistettu käytöstä. (#9077)
* NVDA sanoo nyt "Kopioitu leikepöydälle" ennen kopioitua tekstiä. (#6757)
* Levynhallinnan graafisen näkymän taulukon näyttämistä on paranneltu. (#10048)
* Säätimien selitteet poistetaan nyt käytöstä (näytetään harmaana), kun säädin ei ole käytössä. (#11809)
* CLDR-emojiselitteet päivitetty versioksi 38. (#11817)
* Sisäänrakennettu "Kohdistuksen korostus"-ominaisuus on uudelleennimetty "Visuaaliseksi korostukseksi". (#11700)

### Bugikorjaukset

* NVDA toimii taas oikein muokkauskentissä Fast Log Entry -sovellusta käytettäessä. (#8996)
* Foobar2000:ssa ilmoitetaan kulunut aika, jos kokonaisaikaa ei ole saatavilla (esim. live-suoratoistolähetystä soitettaessa). (#11337)
* NVDA noudattaa nyt verkkosivuilla aria-roledescription-attribuuttia muokattavan sisällön elementeissä. (#11607)
* Luettelon jokaisella rivillä ei enää sanota "luettelo" Google Docsissa tai muussa muokattavassa sisällössä Google Chromessa. (#7562)
* Uuteen listakohteeseen siirtyminen ilmoitetaan nyt, kun verkkosivun muokattavassa sisällössä liikutaan nuolinäppäimillä merkki tai sana kerrallaan luettelokohteesta toiseen. (#11569)
* NVDA lukee nyt oikean rivin, kun kohdistin siirretään linkin loppuun luettelokohteen lopussa Google Docsissa tai muussa verkon muokattavassa sisällössä. (#11606)
* Käynnistä-valikon avaaminen ja sulkeminen työpöydältä Windows 7:ssä asettaa nyt kohdistuksen asianmukaisesti. (#10567)
* Kun "Yritä perua vanhentuneiden kohdistustapahtumien puhe" -asetus on käytössä, välilehden otsikko puhutaan taas Firefoxissa välilehteä vaihdettaessa. (#11397)
* Luettelokohteen, puhuminen ei enää epäonnistu, kun luetteloon on kirjoitettu merkki  ja kun puhumiseen käytetään Ivona-SAPI5-ääniä. (#11651)
* Selaustilan käyttäminen on taas mahdollista luettaessa sähköposteja Windows 10:n Sähköposti-sovelluksen versiolla 16005.13110 ja sitä uudemmalla. (#11439)
* Kun käytetään harposoftware.comin Ivona-SAPI5-ääniä, NVDA voi nyt tallentaa asetuksensa, vaihtaa syntetisaattoria, eikä se myöskään enää hiljene uudelleenkäynnistyksen jälkeen. (#11650)
* HIMS-pistenäytöissä on nyt mahdollista syöttää numero 6 pistekirjoitusnäppäimistöllä tietokonemerkistöä käyttäen. (#11710)
* Merkittäviä suorituskyvyn parannuksia Azure Data Studiossa. (#11533, #11715)
* NVDA:n Etsi-valintaikkunan nimi puhutaan jälleen, kun "Yritä perua vanhentuneiden kohdistustapahtumien puhe" -asetus on käytössä. (#11632)
* NVDA:n ei pitäisi enää jumiutua, kun tietokone herätetään lepotilasta ja kun kohdistus siirtyy Microsoft Edge -dokumenttiin. (#11576)
* Enää ei tarvitse painaa Sarkain-näppäintä tai siirtää kohdistusta pikavalikon sulkemisen jälkeen MS Edgessä, jotta selaustila toimii jälleen. (#11202)
* Luettelonäkymien kohteiden lukeminen ei enää epäonnistu 64-bittisessä sovelluksessa kuten Tortoise SVN:ssä. (#8175)
* ARIA-puuruudukot näkyvät nyt normaalina taulukkona selaustilassa sekä Firefoxissa että Chromessa. (#9715)
* Käänteinen haku voidaan nyt suorittaa Etsi edellinen -toiminnolla painamalla NVDA+Vaihto+F3. (#11770)
* NVDA-skriptiä ei enää pidetä toistuvana, jos kahden suorituksen välissä painetaan skriptiin kuulumatonta näppäintä. (#11388) 
* Strong- ja emphasis-tagien ilmaiseminen voidaan jälleen estää Internet Explorerissa poistamalla käytöstä korostuksen ilmaiseminen NVDA:n asiakirjojen muotoiluasetuksista. (#11808)
* Useiden sekuntien jumiutumista, jota pieni määrä käyttäjiä kokee Excelissä liikuttaessa nuolinäppäimillä solujen välillä, ei pitäisi enää tapahtua. (#11818)
* Keskusteluviestien tai Teams-kanavien lukeminen ei enää epäonnistu väärin kohdistetun valikon takia Microsoft Teamsin koontiversioissa, joiden versionumero on 1.3.00.28xxx. (#11821)
* Teksti, joka on merkitty sekä kirjoitus- että kielioppivirheeksi Google Chromessa, ilmaistaan nyt NVDA:n toimesta asianmukaisesti sellaisiksi. (#11787)
* Vastaa kaikille -toiminnon pikanäppäin (Ctrl+Vaihto+R) toimii taas Outlookin ranskankielistä versiota käytettäessä. (#11196)
* Visual Studion IntelliSense-työkaluvihjeet, jotka tarjoavat lisätietoja valittuna olevasta IntelliSense-kohteesta, Ilmoitetaan nyt vain kerran. (#11611)
* NVDA ei puhu laskutoimitusten edistymistä Windows 10:n Laskimessa, jos kirjoitettujen merkkien puhuminen ei ole käytössä. (#9428)
* NVDA ei enää kaadu käytettäessä englanti (Yhdysvallat), taso 2 -pistetaulukkoa Laajenna kohdistimen kohdalla oleva sana -asetuksen ollessa käytössä näytettäessä tiettyä sisältöä, kuten URL:ää pistekirjoituksella. (#11754)
* Kohdistetun Excel-solun muotoilutietojen ilmoittaminen on taas mahdollista NVDA+F-näppäinkomentoa käyttäen. (#11914)
* QWERTY-syöttö toimii taas sitä tukevissa Papenmeier-pistenäytöissä, eikä se enää aiheuta NVDA:n satunnaista jumiutumista. (#11944)
* Ratkaistu Chromium-pohjaisissa selaimissa useita tapauksia, joissa taulukossa liikkuminen ei toiminut eikä NVDA ilmoittanut taulukon rivien/sarakkeiden määrää. (#12359)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2020.3

Tämä versio sisältää useita huomattavia parannuksia  vakauteen ja suorituskykyyn erityisesti Microsoft Office -sovelluksissa. Kosketusnäyttötuen ja grafiikoiden lukemisen käyttöön ottamiseen tai käytöstä poistamiseen on uudet asetukset.
Merkitty (korostettu) sisältö voidaan ilmoittaa selaimissa, ja on myös uusia saksalaisia pistetaulukoita.

### Uudet ominaisuudet

* Grafiikoiden lukeminen on nyt mahdollista ottaa käyttöön tai poistaa käytöstä NVDA:n asiakirjojen muotoiluasetuksista. Huom: Grafiikoiden vaihtoehtoiset tekstit luetaan, vaikka tämä asetus on poistettu käytöstä. (#4837)
* NVDA:n kosketusnäyttötuki voidaan nyt ottaa käyttöön tai poistaa käytöstä asetusvalintaikkunan Kosketuksen vuorovaikutus -paneeliin lisätyllä asetuksella. Oletusarvoinen näppäinkomento on NVDA+Ctrl+Alt+T. (#9682)
* Lisätty uusia saksalaisia pistetaulukoita. (#11268)
* NVDA tunnistaa nyt vain luku -tyyppiset UIA-tekstisäätimet. (#10494)
* Merkitty (korostettu) sisältö ilmoitetaan sekä puheena että pistekirjoituksella kaikissa verkkoselaimissa. (#11436)
 * Tämä voidaan ottaa käyttöön tai poistaa käytöstä uudella asiakirjojen muotoiluasetuksiin lisätyllä asetuksella.
* Uusia emuloitavia järjestelmän näppäimiä voidaan lisätä NVDA:n Näppäinkomennot-valintaikkunasta. (#6060)
 * Tämä tehdään valitsemalla ensin Emuloitavat järjestelmänäppäimistön näppäimet -kategoria ja painamalla sitten Lisää-painiketta.
* Ohjaussauvallista Handy Tech Active Braille -pistenäyttöä tuetaan. (#11655)
* "Automaattinen vuorovaikutustila kohdistinta sirrettäessä" -asetus on nyt yhteensopiva "Siirrä kohdistus automaattisesti kohdistettaviin elementteihin" -asetuksen käytöstä poistamisen kanssa. (#11663)

### Muutokset

* Lue muotoilutiedot -skripti (NVDA+F) on nyt muutettu ilmoittamaan muotoilutiedot järjestelmäkohdistimen kohdalta tarkastelukohdistimen sijainnin asemesta. Käytä muotoilutietojen lukemiseen tarkastelukohdistimen sijainnista näppäinkomentoa NVDA+Vaihto+F. (#9505)
* NVDA ei oletusarvoisesti enää siirrä kohdistusta automaattisesti selaustilassa kohdistettaviin elementteihin, mikä parantaa suorituskykyä ja vakautta. (#11190)
* Yhteinen Unicode-kielitietovarasto (CLDR) päivitetty versiosta 36.1 versioksi 37. (#11303)
* Päivitetty eSpeak-NG versioksi 1.51-dev, muutos 1fb68ffffea4.
* Taulukkonavigointia voidaan nyt hyödyntää listaruuduissa, joissa on valittavia kohteita, kun kyseinen lista sisältää useita sarakkeita. (#8857)
* Ei-vaihtoehto on nyt oletusarvoisesti valittuna, kun lisäosien hallinnassa pyydetään vahvistusta lisäosan poistolle. (#10015)
* Elementtilista-valintaikkuna näyttää nyt kaavat Microsoft Excelissä lokalisoiduissa muodoissaan. (#9144)
* NVDA käyttää nyt oikeaa terminologiaa muistiinpanoille MS Excelissä. (#11311)
* Kun "Siirrä tarkastelukohdistin kohdistukseen" -komentoa käytetään selaustilassa, tarkastelukohdistin siirretään nyt virtuaalikohdistimen kohdalle. (#9622)
* Selaustilassa ilmoitettavat tiedot, kuten muotoilut NVDA+F:llä, näytetään nyt hieman isommassa ikkunassa ruudun keskellä. (#9910)

### Bugikorjaukset

* NVDA puhuu nyt aina välimerkkitasosta riippumatta sanoittain liikuttaessa ja tultaessa minkä tahansa yksittäisen merkin kohdalle, jota seuraa tyhjätila. (#5133)
* Objektien kuvaukset puhutaan taas QT 5.11:tä tai uudempaa käyttävissä sovelluksissa. (#8604)
* NVDA ei ole enää hiljaa poistettaessa sanaa Ctrl+Del -näppäimillä #11029)
 * Poistetun sanan oikealla puolella olevaa sanaa ei myöskään enää puhuta.
* Kieliluettelo lajitellaan nyt oikein Yleiset asetukset -paneelissa. (#10348)
* Suorituskykyä parannettu merkittävästi Näppäinkomennot-valintaikkunassa suodattamisen aikana. (#10307)
* U+FFFF:n yli meneviä Unicode-merkkejä voidaan nyt lähettää pistenäytöltä. (#10796)
* NVDA puhuu Avaa sovelluksessa -valintaikkunan sisällön Windows 10:n toukokuun 2020 päivityksessä. (#11335)
* Lisäasetukset-paneelin uusi kokeellinen asetus (Ota käyttöön UI Automation -tapahtumien ja ominaisuusmuutosten valikoiva rekisteröinti) voi käytössä ollessaan tarjota huomattavia suorituskyvyn parannuksia Microsoft Visual Studiossa sekä muissa UIAutomation-pohjaisissa sovelluksissa. (#11077, #11209)
* Valittavien listakohteiden valittu-tilaa ei enää sanota tarpeettomasti, ja tarvittaessa sen sijaan sanotaan ei valittu. (#8554)
* NVDA näyttää nyt Windows 10:n toukokuun 2020 päivityksessä Microsoft Sound Mapper -vaihtoehdon Syntetisaattori-valintaikkunan Äänen ulostulolaite -yhdistelmäruudussa. (#11349)
* Numeroitujen listojen numerot sanotaan nyt oikein Internet Explorerissa, mikäli lista ei ala 1:llä. (#8438)
* NVDA sanoo nyt Google Chromessa "ei valittu" kaikista valittavista säätimistä, jotka eivät ole valittuina (ei pelkästään valintaruuduista). (#11377)
* Useissa säätimissä liikkuminen on taas mahdollista, kun NVDA:n kieleksi on määritetty aragonia. (#11384)
* NVDA:n ei pitäisi enää jäätyä ajoittain Microsoft Wordissa siirryttäessä nopeasti nuolinäppäimillä ylös ja alas tai merkkejä kirjoitettaessa pistenäytön ollessa käytössä. (#11431, #11425, #11414)
* NVDA ei enää lisää olematonta välilyöntiä tekstin loppuun kopioitaessa nykyisen navigointiobjektin sisältöä leikepöydälle. (#11438)
* NVDA ei ota enää käyttöön Jatkuva luku -profiilia, jos mitään luettavaa ei ole. (#10899, #9947)
* NVDA voi taas lukea Internet Information Services (IIS) Managerin ominaisuuslistaa. (#11468)
* NVDA pitää nyt äänilaitteen avoimena, mikä parantaa  suorituskykyä joillakin äänikorteilla. (#5172, #10721)
* NVDA ei enää jumiudu tai sulkeudu pidettäessä alhaalla Ctrl+Vaihto+Alanuolta Microsoft Wordissa. (#9463)
* NVDA ilmoittaa nyt aina siirtymispuunäkymän hakemistojen laajennettu/kutistettu-tilan drive.google.comissa. (#11520)
* NVDA tunnistaa automaattisesti Humanwaren NLS eReader -pistenäytön Bluetoothin kautta, koska sen Bluetooth-nimi on nyt "NLS eReader Humanware". (#11561)
* Suuria suorituskyvyn parannuksia  Visual Studio Codessa. (#11533)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2020.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. tuki uudelle Nattiqin pistenäytölle, parempi tuki ESET Antivirus -ohjelmiston graafiselle käyttöliittymälle ja Windows-päätteelle, suorituskyvyn parannuksia 1Passwordille ja Windows OneCore -syntetisaattorille sekä monia muita tärkeitä bugikorjauksia ja parannuksia.

### Uudet ominaisuudet

* Tuki Nattiq nBraille -pistenäytöille. (#10778)
* Lisätty skripti NVDA:n asetushakemiston avaamiseen (oletusarvoista näppäinkomentoa ei ole määritetty). (#2214)
* Parempi tuki ESET Antivirus -ohjelmiston graafiselle käyttöliittymälle. (#10894)
* Lisätty tuki Windows-päätteelle. (#10305)
* Lisätty komento aktiivisen asetusprofiilin ilmoittamiselle (oletusarvoista näppäinkomentoa ei ole määritetty). (#9325)
* Lisätty komento ala- ja yläindeksien ilmaisemisen käyttöön ottamiselle ja käytöstä poistamiselle (oletusarvoista näppäinkomentoa ei ole määritetty). (#10985)
* Verkkosovelluksissa (esim. Gmailissa) ei enää puhuta vanhentunutta tietoa, kun kohdistusta siirretään nopeasti. (#10885)
 * Tämä kokeellinen korjaus on otettava käyttöön manuaalisesti Lisäasetukset-paneelin "Yritä perua vanhentuneiden kohdistustapahtumien puhe" -asetuksella.
* Lisätty oletussymbolisanastoon paljon uusia symboleita. (#11105)

### Muutokset

* Päivitetty liblouis-pistekääntäjä versiosta 3.12 versioksi [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Ylä- ja alaindeksien ilmaisemista säädetään nyt omalla erillisellä asetuksellaan, eikä fonttimääreiden ilmaiseminen vaikuta enää niihin. (#10919)
* VS Codeen tehtyjen muutosten takia NVDA ei enää poista oletusarvoisesti selaustilaa käytöstä tässä sovelluksessa. (#10888)
* NVDA ei enää sano "yläreuna" ja "alareuna", kun tarkastelukohdistin siirretään suoraan nykyisen navigointiobjektin ensimmäiselle tai viimeiselle riville Siirrä ylimmälle riville- ja Siirrä alimmalle riville -komentoja käyttäen. (#9551)
* NVDA ei enää sano "vasen" ja "oikea", kun tarkastelukohdistin siirretään suoraan rivin ensimmäiseen tai viimeiseen merkkiin nykyisessä navigointiobjektissa  Siirrä rivin alkuun- ja Siirrä rivin loppuun -komentoja käyttäen. (#9551)

### Bugikorjaukset

* NVDA käynnistyy nyt oikein, kun lokitiedostoa ei voi luoda. (#6330)
* NVDA ei enää sano Microsoft Word 365:n uusimmissa versioissa asiakirjaa muokattaessa "poista edellinen sana" Ctrl+Askelpalautin-näppäinyhdistelmää painettaessa. (#10851)
* NVDA kertoo taas Winampissa sekoituksen ja jatkuvan toiston tilan. (#10945)
* NVDA ei enää ole erittäin hidas liikuttaessa kohteiden luettelossa 1Passwordissa. (#10508)
* Windows OneCore -puhesyntetisaattori ei enää hidastele sanojen välillä. (#10721)
* NVDA ei jää enää jumiin, kun 1Passwordin pikavalikko avataan järjestelmän ilmoitusalueelta. (#11017)
* Office 2013:ssa ja sitä vanhemmissa:
 * Valintanauhat puhutaan, kun kohdistus siirtyy niihin ensimmäisen kerran. (#4207)
 * Pikavalikon kohteet puhutaan taas oikein. (#9252)
 * Valintanauhan osat puhutaan yhdenmukaisesti Ctrl+nuolinäppäimillä liikuttaessa. (#7067)
* Teksti ei enää näy virheellisesti eri rivillä selaustilassa Mozilla Firefoxissa ja Google Chromessa, kun verkkosisällössä käytetään CSS:n display: inline-flex -määrettä. (#11075)
* Elementtejä, joihin ei voi siirtää kohdistusta selaustilassa, on nyt mahdollista aktivoida, kun Siirrä kohdistus automaattisesti kohdistettaviin elementteihin -asetus on poistettu käytöstä.
* Elementtejä, joihin on siirrytty selaustilassa Sarkain-näppäimellä, on nyt mahdollista aktivoida, kun Siirrä kohdistus automaattisesti kohdistettaviin elementteihin -asetus on poistettu käytöstä. (#8528)
* Tiettyjen elementtien aktivoiminen selaustilassa ei enää napsauta väärässä kohdassa, kun Siirrä kohdistus automaattisesti kohdistettaviin elementteihin -asetus on poistettu käytöstä. (#9886)
* NVDA:n virheääniä ei enää kuulu käytettäessä DevExpressin tekstisäätimiä. (#10918)
* Kahdesti puhumisen välttämiseksi ilmoitusalueen kuvakkeiden työkaluvihjeitä ei enää puhuta näppäimistön avulla liikuttaessa, mikäli niiden teksti on sama kuin kuvakkeiden nimet. (#6656)
* Vuorovaikutustilaan vaihtaminen selaustilassa NVDA+Väli-näppäinyhdistelmällä siirtää nyt kohdistuksen kohdistimen alla olevaan elementtiin, kun Siirrä kohdistus automaattisesti kohdistettaviin elementteihin -asetus on poistettu käytöstä. (#11206)
* NVDA-päivitysten tarkistaminen on taas mahdollista tietyissä järjestelmissä, esim. puhtaissa Windows-asennuksissa. (#11253)
* Kohdistus ei siirry Java-sovelluksessa, kun valinta muuttuu ei-kohdistetussa puunäkymässä, taulukossa tai luettelossa. (#5989)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2020.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. tuki useille uusille HumanWaren ja APH:n pistenäytöille, sekä monet tärkeät bugikorjaukset, kuten mahdollisuus lukea jälleen matemaattisia yhtälöitä Microsoft Wordissa MathPlayeria / MathTypea käyttäen.

### Uudet ominaisuudet

* Listaruuduissa valittuna oleva kohde näytetään jälleen selaustilassa Chromessa samalla tavoin kuin NVDA 2019.1:ssä. (#10713)
* Voit nyt suorittaa kosketusnäyttölaitteissa oikean hiirinäppäimen napsautuksen napauttamalla ja pitämällä yhtä sormea näytöllä. (#3886)
* Tuki uusille pistenäytöille: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2 ja NLS eReader. (#10830)

### Muutokset

* NVDA estää järjestelmää lukittumasta tai siirtymästä lepotilaan, kun jatkuva luku on käynnissä. (#10643)
* Tuki prosessin ulkopuolisille tekstikehyksille Mozilla Firefoxissa. (#10707)
* Päivitetty liblouis-pistekääntäjä versioksi 3.12. (#10161)

### Bugikorjaukset

* Unicode-miinusmerkkiä (U+2212) ei puhuttu. (#10633)
* Kun lisäosa asennetaan lisäosien hallinnasta, tiedostojen ja kansioiden nimiä ei enää puhuta Selaa-ikkunassa kahdesti. (#10620, #2395)
* Kun Mastodon ladataan Firefoxissa edistyneen web-käyttöliittymän ollessa käytössä, kaikki aikajanat näytetään nyt oikein selaustilassa. (#10776)
* NVDA ilmoittaa nyt selaustilassa "ei valittu" sellaisille ei-valituille valintaruuduille, joista sitä ei aiemmin ilmoitettu. (#10781)
* ARIA-kytkinsäätimistä ei enää puhuta sekavaa tietoa, kuten "ei painettu valittu" tai "painettu valittu". (#9187)
* SAPI 4 -äänien ei pitäisi enää kieltäytyä puhumasta tiettyä tekstiä. (#10792)
* NVDA voi jälleen lukea matemaattisia yhtälöitä Microsoft Wordissa ja olla vuorovaikutuksessa niiden kanssa. (#10803)
* NVDA puhuu jälleen selaustilassa tekstin, jonka valinta perutaan, mikäli nuolinäppäintä painetaan tekstin ollessa valittuna. (#10731).
* NVDA ei enää sulkeudu, mikäli eSpeakin alustuksessa tapahtuu virhe. (#10607)
* Unicoden aiheuttamat virheet pikakuvakkeiden nimien käännöksissä eivät enää pysäytä asentajaa, ja niitä lievennetään palaamalla takaisin englanninkieliseen tekstiin. (#5166, #6326)
* Kun luetteloista ja taulukoista siirrytään pois nuolinäppäimillä jatkuvassa luvussa pikaluvun ollessa käytössä, luettelosta tai taulukosta poistumisesta ei enää ilmoiteta jatkuvasti. (#10706)
* Hiiren seuranta korjattu joissakin MSHTML-elementeissä Internet Explorerissa. (#10736)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2019.3

NVDA 2019.3 on erittäin merkittävä julkaisu, joka sisältää monia konepellin alla tapahtuneita muutoksia, mukaan lukien Python 2:n päivittäminen Python 3:ksi sekä NVDA:n puhealijärjestelmän huomattava uudelleenkirjoittaminen.
Vaikka nämä muutokset rikkovat yhteensopivuuden vanhempien NVDA-lisäosien kanssa, päivitys Python 3:een on turvallisuuden kannalta välttämätön, ja puhemuutokset mahdollistavat lähitulevaisuudessa jännittäviä innovaatioita.
Muita merkittäviä muutoksia tässä versiossa ovat mm. 64-bittinen tuki Java-virtuaalikoneille, näyttöverho sekä kohdistuksen korostustoiminnallisuus, tuki useammille pistenäytöille, uusi pistekirjoituksen tarkastelutoiminto sekä useita virhekorjauksia.

### Uudet ominaisuudet

* Siirrä hiiri navigointiobjektiin -komennon  tarkkuutta parannettu Java-sovellusten tekstikentissä. (#10157)
* Lisätty tuki seuraaville Handy Tech -pistenäytöille (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Kaikki käyttäjän määrittelemät näppäinkomennot voidaan nyt poistaa uudella Näppäinkomennot-valintaikkunan Palauta oletukset -painikkeella. (#10293)
* Microsoft Wordissa kerrotaan nyt fonttia ilmaistaessa, onko teksti piilotettu. (#8713)
* Lisätty komento  tarkastelukohdistimen siirtämiseksi aiemmin asetetun, valittavaksi tai kopioitavaksi merkityn tekstin alkukohdan sijaintiin. (#1969)
* Kiintopisteet ilmaistaan nyt Internet Explorerissa, Microsoft Edgessä sekä Firefoxin ja Chromen uusimmissa versioissa vuorovaikutustilassa ja objektinavigointia käytettäessä. (#10101)
* Pikanavigointikomennoilla on nyt mahdollista liikkua artikkeleittain ja ryhmittäin Internet Explorerissa, Google Chromessa sekä Mozilla Firefoxissa. Näihin komentoihin ei oletusarvoisesti ole liitetty näppäimiä, mutta ne voidaan määrittää Näppäinkomennot-valintaikkunasta, kun se avataan selaustila-asiakirjan ollessa avoimena. (#9485, #9227)
 * Myös kuvat ilmaistaan. Niitä käsitellään objekteina, ja ovat siksi navigoitavissa O-pikanavigointinäppäimellä.
* Artikkelielementit ilmaistaan nyt Internet Explorerissa, Google Chromessa ja Mozilla Firefoxissa objektinavigointia käytettäessä ja vaihtoehtoisesti selaustilassa, mikäli kyseinen asetus on otettu käyttöön asiakirjojen muotoiluasetuksista. (#10424)
* Lisätty näyttöverho, joka käytössä ollessaan pimentää koko ruudun Windows 8:ssa ja uudemmissa. (#7857)
 * Lisätty skripti näyttöverhon käyttöön ottamiselle (yhdellä painalluksella seuraavaan uudelleenkäynnistykseen saakka tai kahdella painalluksella aina NVDA:n ollessa käynnissä), oletusarvoista näppäinkomentoa ei ole määritelty.
 * Voidaan ottaa käyttöön ja määrittää NVDA:n asetusvalintaikkunan Näkö-kategoriasta.
* Lisätty ruudun korostustoiminnallisuus. (#971, #9064)
 * Kohdistuksen, navigointiobjektin ja selaustilakohdistimen sijainnin korostaminen voidaan ottaa käyttöön ja määrittää NVDA:n asetusvalintaikkunan Näkö-kategoriasta.
 * Huom: Tämä toiminto ei ole yhteensopiva Kohdistuksen korostus -lisäosan kanssa, mutta sen käyttäminen on edelleen mahdollista, kun sisäänrakennettu korostaja on poistettu käytöstä.
* Lisätty Pistekirjoituksen tarkastelu -työkalu, jonka avulla voi tarkastella pistekirjoitustulostetta ruudulla näkyvässä ikkunassa. (#7788)

### Muutokset

* Käyttöoppaassa selitetään nyt, miten NVDA:ta käytetään Windows-konsolissa. (#9957)
* Nvda.exe:n suorittaminen korvaa nyt oletusarvoisesti jo käynnissä olevan NVDA-version. Komentoriviparametri -r|--replace hyväksytään edelleen, mutta se ohitetaan. (#8320)
* NVDA ilmaisee nyt Windows 8:ssa ja uudemmissa isännöityjen sovellusten, kuten Microsoft Storesta ladattujen, tuotteen nimen ja versiotiedot sovelluksen tarjoamia tietoja käyttäen. (#4259, #10108)
* Kun muutosten jäljittäminen otetaan käyttöön tai poistetaan käytöstä Microsoft Wordissa näppäimistöä käyttäen, NVDA kertoo asetuksen tilan. (#942)
* NVDA:n versionumero tallennetaan nyt lokiin ensimmäisenä ilmoituksena. Näin tapahtuu, vaikka lokin tallennus olisi poistettu käytöstä yleisistä asetuksista. (#9803)
* Asetukset-valintaikkuna ei enää salli lokitason muuttamista, mikäli se on ohitettu komentorivivalitsimella. (#10209)
* NVDA kertoo nyt Microsoft Wordissa tulostumattomien merkkien näyttötilan painettaessa tilanvaihtopikanäppäintä Ctrl+Vaihto+8. (#10241)
* Päivitetty Liblouis-pistekääntäjä muutoksella 58d67e63. (#10094)
* Kun emojien puhuminen on käytössä, ne sanotaan kaikilla välimerkkitasoilla. (#8826)
* NVDA:han sisältyvät kolmannen osapuolen Python-paketit, kuten comtypes, tallentavat nyt varoituksensa ja virheensä NVDA:n lokiin. (#10393)
* Päivitetty Unicode Common Locale Data -tietokannan emojiselitteet versioksi 36.0. (#10426)
* Kun kohdistus siirretään selaustilassa ryhmän kohdalle, nyt luetaan lisäksi sen kuvaus. (#10095)
* Java Access Bridge sisältyy nyt NVDA:han, jotta Java-sovellusten (mukaan lukien 64-bittiset Java-virtuaalikoneet) käyttäminen olisi mahdollista. (#7724)
* Mikäli Java Access Bridgeä ei ole otettu käyttöön nykyiselle käyttäjälle, se otetaan automaattisesti käyttöön NVDA:ta käynnistettäessä. (#7952)
* Päivitetty eSpeak-NG versioksi 1.51-dev, muutos ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Bugikorjaukset

* Emojit ja muut 32-bittiset Unicode-merkit vievät nyt vähemmän tilaa pistenäytöllä, kun ne näytetään heksadesimaaliarvoina. (#6695)
* NVDA puhuu Windows 10:ssä universaalien sovellusten työkaluvihjeet, mikäli työkaluvihjeiden ilmaiseminen on otettu käyttöön asetusvalintaikkunan Objektien lukeminen -kategoriassa. (#8118)
* Kirjoitettu teksti puhutaan nyt Mintty:ssä Windows 10:n Anniversary-päivityksessä ja uudemmissa. (#1348)
* Windows-konsolissa kohdistimen lähelle ilmestyvää tulostetta ei enää tavata Windows 10:n Anniversary-päivityksessä ja uudemmissa. (#513)
* Audacityn kompressorivalintaikkunan säätimet puhutaan nyt valintaikkunassa liikuttaessa . (#10103)
* NVDA ei enää käsittele välilyöntejä sanoina objektintarkastelussa Scintilla-pohjaisissa editoreissa, kuten Notepad++:ssa. (#8295)
* NVDA estää järjestelmää siirtymästä lepotilaan, kun tekstiä vieritetään pistenäytön näppäimillä. (#9175)
* Pistenäyttö seuraa nyt Windows 10:ssä, kun solun sisältöä muokataan Microsoft Excelissä sekä muissa UIA-tekstisäätimissä, joissa se jäi aiemmin jälkeen. (#9749)
* NVDA puhuu jälleen kerran ehdotukset Microsoft Edgen osoitepalkissa. (#7554)
* NVDA ei enää hiljene, kun kohdistus siirtyy Internet Explorerissa HTML-välilehtisäätimen otsakkeeseen. (#8898)
* NVDA ei enää toista hakuehdotusääntä EdgeHTML-pohjaisessa Microsoft Edgessä, kun ikkuna suurennetaan. (#9110, #10002)
* ARIA 1.1 -yhdistelmäruutuja tuetaan nyt Mozilla Firefoxissa ja Google Chromessa. (#9616)
* NVDA ei enää puhu luettelokohteiden visuaalisesti piilossa olevia sarakkeita SysListView32-säätimissä. (#8268)
* Asetusvalintaikkuna ei enää näytä suojatussa tilassa nykyisenä lokitasona "tiedot". (#10209)
* NVDA puhuu Käynnistä-valikossa hakutulosten tiedot Windows 10:n Anniversary-päivityksessä ja uudemmissa. (#10340)
* Mikäli kohdistimen siirtäminen tai pikanavigoinnin käyttäminen aiheuttaa selaustilassa asiakirjan muuttumisen, NVDA ei enää puhu joissakin tapauksissa virheellistä sisältöä. (#8831, #10343)
* Joitakin Microsoft Wordin luettelomerkkien nimiä on korjattu. (#10399)
* NVDA sanoo jälleen kerran Windows 10:n toukokuun 2019 päivityksessä ja uudemmissa ensimmäisen valitun emojin tai leikepöydän kohteen, kun emojipaneeli ja leikepöydän historia avautuvat. (#9204)
* Poeditissä on jälleen kerran mahdollista tarkastella oikealta vasemmalle luettavien kielten käännöksiä. (#9931)
* NVDA ei enää puhu edistymispalkin tietoja Järjestelmä/Ääni-sivun äänenvoimakkuusmittareille Windows 10:n huhtikuun 2018 päivityksen ja uudempien Asetukset-sovelluksessa. (#10412)
* Puhesanastojen virheelliset säännölliset lausekkeet eivät enää mykistä täysin NVDA:n puhetta. (#10334)
* Kun Microsoft Wordissa luetaan luettelomerkillisiä kohteita UIA:n ollessa käytössä, seuraavan luettelokohteen luettelomerkkiä ei enää virheellisesti puhuta. (#9613)
* Ratkaistu joitakin harvinaisia pistekirjoituskäännöksen ongelmia ja liblouis-virheitä. (#9982)
* Ennen NVDA:ta käynnistetyt Java-sovellukset ovat nyt saavutettavia ilman sovelluksen uudelleenkäynnistystä. (#10296)
* Kun kohdistettu elementti merkitään Mozilla Firefoxissa nykyiseksi (aria-current), muutosta ei enää puhuta useita kertoja. (#8960)
* NVDA käsittelee nyt tekstissä liikuttaessa tiettyjä Unicode-yhdistelmämerkkejä, kuten e-akuutti, yhtenä merkkinä. (#10550)
* Spring Tool Suiten versio 4 on nyt tuettu. (#10001)
* Nimeä ei puhuta kahdesti, kun aria-labelledby-relaatiokohde on sisempi elementti. (#10552)
* Pistekirjoitusnäppäimistöllä kirjoitetut merkit puhutaan useammissa tapauksissa Windows 10:n versiossa 1607 ja uudemmissa. (#10569)
* Kun äänen ulostulolaitetta vaihdetaan, NVDA:n äänimerkit toistetaaan nyt juuri valitun laitteen kautta. (#2167)
* Kohdistuksen siirtäminen selaustilassa on nopeampaa Mozilla Firefoxissa. Tämä tekee kohdistimen siirtämisestä responsiivisempaa. (#10584)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2019.2.1

Tämä versio korjaa useita 2019.2:ssa olevia kaatumisia. Muun muassa seuraavat ongelmat on korjattu:

* Ratkaistu useita Gmailin kaatumisia, joita on esiintynyt sekä Firefoxissa että Chromessa oltaessa vuorovaikutuksessa ponnahdusvalikoiden kanssa, kuten esim. luotaessa suodattimia tai muutettaessa tiettyjä Gmailin asetuksia. (#10175, #9402, #8924)
* NVDA ei enää aiheuta Resurssienhallinnan kaatumista Windows 7:ssä, kun hiirtä käytetään Käynnistä-valikossa. (#9435) 
* Resurssienhallinta ei enää kaadu Windows 7:ssä metatietojen muokkauskenttiä käytettäessä. (#5337) 
* NVDA ei jää enää jumiin Mozilla Firefoxissa tai Google Chromessa oltaessa vuorovaikutuksessa sellaisten kuvien kanssa, joiden URI-tietotunniste sisältää Base64-koodattua tietoa. (#10227)

## 2019.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat Freedom Scientificin pistenäyttöjen automaattinen tunnistus, Lisäasetukset-paneelin kokeellinen asetus, jolla selaustila ei siirrä kohdistusta automaattisesti (mikä saattaa parantaa suorituskykyä), nopeudenlisäysasetus Windows OneCore -syntetisaattorille hyvin suurten nopeuksien saavuttamiseksi, sekä useita ohjelmavirheiden korjauksia.

### Uudet ominaisuudet

* NVDA:n Miranda NG -tuki toimii asiakasohjelman uudempien versioiden kanssa. (#9053) 
* Selaustilan oletusarvoinen käytöstä poistaminen on nyt mahdollista poistamalla käytöstä uusi "Ota selaustila käyttöön sivun latautuessa" -asetus NVDA:n selaustilan asetuksista. (#8716) 
 * Huom: Selaustila voidaan edelleen ottaa käyttöön manuaalisesti painamalla NVDA+Väli, vaikka tämä asetus olisi poistettu käytöstä.
* Symbolien suodattaminen on nyt mahdollista Välimerkkien ja symbolien puhuminen -valintaikkunassa samaan tapaan kuin elementtilistassa ja Näppäinkomennot-valintaikkunassa. (#5761)
* Lisätty komento hiiren tekstiyksikön tarkkuuden muuttamiseen (paljonko tekstiä puhutaan hiiren liikkuessa). Oletusnäppäinkomentoa ei ole määritetty. (#9056)
* Windows OneCore -syntetisaattorilla on nyt nopeudenlisäysasetus, joka mahdollistaa aiempaa merkittävästi suuremmat nopeudet. (#7498)
* Nopeuden lisäys -asetus on nyt määritettävissä syntetisaattorin asetusrenkaasta tuetuille puhesyntetisaattoreille. (Tällä hetkellä eSpeak-NG sekä Windows OneCore). (#8934)
* Asetusprofiilit voidaan nyt ottaa käyttöön manuaalisesti näppäinkomentoa käyttäen. (#4209)
 * Näppäinkomento on määritettävä Näppäinkomennot-valintaikkunassa.
* Lisätty tuki Eclipsen koodieditorin automaattiselle täydennykselle. (#5667)
 * Editorissa voidaan lisäksi lukea Javadoc-tiedot NVDA+D-näppäinkomennolla, mikäli niitä on saatavilla.
* Lisätty asetuspaneelin Lisäasetukset-kategoriaan kokeellinen asetus, joka saa järjestelmäkohdistuksen olemaan seuraamatta selaustilakohdistinta (Siirrä kohdistus automaattisesti kohdistettaviin elementteihin). (#2039) Vaikka tämän käytöstä poistaminen ei ehkä sovikaan kaikille verkkosivustoille, se saattaa silti korjata seuraavat ongelmat:
 * Kuminauhaefekti: NVDA peruu satunnaisesti viimeisimmän selaustilan näppäinkomennon hyppäämällä edelliseen sijaintiin.
 * Kohdistus siirtyy joillakin verkkosivuilla väkisin muokkauskenttiin, kun niiden välillä siirrytään Nuoli alas -näppäimellä.
 * Hidas reagointi selaustilan näppäinkomentoihin.
* Tuettujen pistenäyttöajureiden asetuksia on nyt mahdollista muuttaa NVDA:n asetusvalintaikkunan Pistekirjoitus-kategoriasta. (#7452)
* Pistenäyttöjen automaattinen tunnistus tukee nyt Freedom Scientificin pistenäyttöjä. (#7727)
* Lisätty komento tarkastelukohdistimen kohdalla olevan symbolin korvauksen näyttämiseen. (#9286)
* Lisäasetukset-paneeliin lisätty kokeellinen asetus, jolla voi testata uutta NVDA:n työn alla olevaa Microsoft UI Automation -rajapintaa käyttävää Windows-konsolin tukea. (#9614)
* Python-konsolin syöttökenttä tukee nyt usean rivin liittämistä leikepöydältä. (#9776)

### Muutokset

* Syntetisaattorin äänenvoimakkuutta lisätään ja vähennetään nyt 10:n asemesta 5:llä asetusrengasta käytettäessä. (#6754)
* Selvennetty lisäosien hallinnan tekstiä, joka näytetään kun NVDA on käynnistetty --disable-addons-komentoriviparametrilla. (#9473)
* Unicode Common Locale Data -tietokannan emojiselitteet päivitetty versioksi 35.0. (#9445)
* Selaustilan elementtilistan suodatuskentän pikanäppäin on muutettu englanninkielisessä käyttöliittymässä Alt+Y:ksi. (#8728)
* Kun automaattisesti tunnistettu pistenäyttö kytketään bluetoothin kautta, NVDA jatkaa saman ajurin tukemien USB-näyttöjen etsimistä ja vaihtaa USB-yhteyteen, mikäli sellainen tulee saataville. (#8853)
* eSpeak-NG päivitetty muutoksella 67324cc.
* Liblouis-pistekääntäjä päivitetty versioksi 3.10.0. (#9439)
* NVDA sanoo nyt "valittu" ilmoitettuaan ensin käyttäjän valitseman tekstin. (#9028, #9909)
* Vuorovaikutustila on oletusarvoisesti käytössä Microsoft Visual Studio Codessa. (#9828)

### Bugikorjaukset

* NVDA ei enää kaadu, kun lisäosan hakemisto on tyhjä. (#7686)
* Vasemmalta oikealle ja oikealta vasemmalle osoittavia nuolimerkkejä ei enää näytetä pistenäytöllä tai puhuta merkeittäin liikuttaessa Ominaisuudet-ikkunassa. (#8361)
* Kun lomakekenttiin siirrytään selaustilan pikanavigointinäppäimillä, koko kenttä puhutaan nyt pelkän ensimmäisen rivin asemesta. (#9388)
* NVDA ei enää hiljene, kun Windows 10:n Sähköposti-sovellus on suljettu. (#9341)
* NVDA:n käynnistyminen ei enää epäonnistu, kun Windowsin alue- ja kieliasetuksissa on määritettynä NVDA:lle tuntematon kieli, kuten esim. Englanti (Alankomaat). (#8726)
* Kun Microsoft Excelissä vaihdetaan selaustilaa käytettäessä selaimeen, jossa on käytössä vuorovaikutustila tai päinvastoin, selaustilan tila ilmoitetaan nyt asianmukaisesti. (#8846)
* NVDA ilmoittaa nyt asianmukaisesti hiirikohdistimen alla olevan rivin Notepad++:ssa ja muissa Scintilla-pohjaisissa editoreissa. (#5450)
* Pistenäytöllä ei enää näytetä toisinaan virheellisesti kohdistimen edessä "ltl lop" luettelokohteen keskellä Google Docsissa ja muissa verkkopohjaisissa editoreissa. (#9477)
* NVDA ei enää puhu Windows 10:n May 2019 -päivityksessä useita ilmoituksia, jos äänenvoimakkuutta muutetaan fyysisillä painikkeilla Resurssienhallinnan ollessa aktiivisena. (#9466)
* Välimerkkien ja symbolien puhuminen -valintaikkuna avautuu nyt paljon nopeammin, kun käytössä on yli 1000 symbolia sisältäviä symbolisanastoja. (#8790)
* NVDA lukee  asianmukaisen rivin, kun automaattinen rivitys on käytössä Scintilla-säätimissä, kuten Notepad++:ssa. (#9424)
* Solun sijainti ilmoitetaan Microsoft Excelissä sen muuttuessa Vaihto+Enter- tai Vaihto+Laskinnäppäimistön Enter -näppäinkomentojen takia. (#9499)
* Objects Explorer -ikkunan valittu kohde ilmoitetaan nyt asianmukaisesti kategorioita sisältävissä olio- ja alkiopuunäkymissä Visual Studio 2017:ssä ja uudemmissa. (#9311)
* Lisäosia, joiden nimet eroavat toisistaan vain kirjainkoon osalta, ei enää käsitellä erillisinä. (#9334)
* Windows 10:n teksti puheeksi -asetuksissa määritetty nopeus ei enää vaikuta Windows OneCore -ääniä käytettäessä NVDA:ssa määritettyyn nopeuteen. (#7498)
* Lokin voi nyt avata painamalla NVDA+F1, kun nykyisestä navigointiobjektista ei ole saatavilla kehittäjätietoja. (#8613)
* NVDA:n taulukkonavigointikomentojen käyttäminen on jälleen mahdollista Google Docsissa, Firefoxissa ja Chromessa. (#9494)
* Freedom Scientific -pistenäyttöjen vieritysnäppäimet toimivat nyt asianmukaisesti. (#8849)
* NVDA ei enää hjyydy enimillään 10 sekunniksi luettaessa asiakirjan ensimmäistä merkkiä 64-bittisessä Notepad++ 7.7:ssä. (#9609)
* NVDA:ssa voidaan nyt käyttää HTComia Handy Tech -pistenäytön kanssa. (#9691)
* Taustavälilehdellä olevan Aktiivisen alueen päivityksiä ei enää puhuta Mozilla Firefoxissa. (#1318)
* Selaustilan Etsi-valintaikkuna ei enää lakkaa toimimasta, jos NVDA:n Tietoja-valintaikkuna on avoimena taustalla. (#8566)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2019.1.1

Tässä versiossa on korjattu seuraavat bugit:

* NVDA ei enää aiheuta Excel 2007:n kaatumista tai kieltäydy ilmaisemasta solussa olevaa kaavaa. (#9431)
* Google Chrome ei enää kaadu oltaessa vuorovaikutuksessa tiettyjen luetteloruutujen kanssa. (#9364)
* Korjattu ongelma, joka esti käyttäjän asetusten kopioinnin järjestelmän asetusprofiiliin. (#9448)
* NVDA käyttää jälleen Microsoft Excelissä paikalliselle kielelle käännettyä ilmoitusta yhdistettyjen solujen sijaintia ilmoittaessaan. (#9471)

## 2019.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat suorituskyvyn parannukset sekä Microsoft wordia että Exceliä käytettäessä, vakauden ja tietoturvan parannukset, kuten tuki versioyhteensopivuustietoja sisältäville lisäosille, sekä monet muut ohjelmavirheiden korjaukset.

Huom: Tästä versiosta alkaen käyttäjän omia sovellusmoduuleita, yleisliitännäisiä tai pistenäyttö- ja syntetisaattoriajureita ei enää ladata automaattisesti NVDA:n asetushakemistosta. 
Ne tulisi asentaa osana NVDA:n lisäosaa. Lisäosien kehittäjät voivat testata koodiaan sijoittamalla sen scratchpad-hakemistoon, joka löytyy NVDA:n asetushakemistosta, jos Lataa käyttäjän oma koodi kehittäjien scratchpad-hakemistosta -asetus on otettu käyttöön NVDA:n uudesta Lisäasetukset-asetuspaneelista.
Nämä muutokset ovat välttämättömiä mukautetun koodin yhteensopivuuden varmistamiseksi, jotta NVDA ei lakkaa toimimasta, kun tällainen koodi ei ole enää yhteensopivaa uudempien versioiden kanssa.
Saat lisätietoja tästä sekä lisäosien paremmasta versioinnista lukemalla alta tehdyistä muutoksista.

### Uudet ominaisuudet

* Uusia pistetaulukoita: afrikaans, arabialainen 8 pisteen tietokonemerkistö, arabialainen taso 2, espanjalainen taso 2. (#4435, #9186)
* Hiiriasetuksiin lisätty asetus, jolla NVDA:n saa käsittelemään tilanteita, joissa jokin toinen sovellus hallitsee hiirtä. (#8452) 
 * Tämä mahdollistaa hiiren seurannan, kun järjestelmää etähallitaan TeamViewerillä tai muilla etähallintaohjelmistoilla.
* Lisätty komentoriviparametri `--enable-start-on-logon`, jonka avulla voidaan säätää, määrittääkö hiljainen asennus NVDA:n käynnistymään Windowsiin kirjauduttaessa. Määritä arvoksi true, jos haluat ottaa käyttöön kirjauduttaessa käynnistämisen tai false, jos et halua ottaa sitä käyttöön. Mikäli `--enable-start-on-logon`-parametria ei määritetä, NVDA käynnistyy oletusarvoisesti kirjauduttaessa, ellei sitä ole poistettu käytöstä aiemmassa asennuksessa. (#8574)
* NVDA:n loki on mahdollista poistaa käytöstä määrittämällä Yleiset asetukset -paneelista lokitasoksi "ei käytössä". (#8516)
* Kaavat ilmoitetaan nyt LibreOfficen ja Apache OpenOfficen laskentataulukoissa. (#860)
* Valittu kohde ilmoitetaan nyt listaruuduissa ja puunäkymissä selaustilassa oltaessa Mozilla Firefoxissa ja Google Chromessa.
 * Toimii Firefox 66:ssa ja uudemmissa.
 * Ei toimi Chromessa tietyissä listaruuduissa (HTML-valintasäätimet).
* Alustava tuki sovelluksille, kuten Mozilla Firefox, tietokoneissa, joissa on ARM64--pohjainen prosessori (esim. Qualcom Snapdragon). (#9216)
* Lisätty NVDA:n asetusvalintaikkunaan Lisäasetukset-kategoria, jossa on esim. asetus, jolla voi kokeilla NVDA:n uutta UI Automation -rajapintaa hyödyntävää Microsoft Word -tukea. (#9200)
* Lisätty tuki Windowsin Levynhallinnan graafiselle näkymälle. (#1486)
* Lisätty tuki Handy Techin Connect Braille- ja Basic Braille 84 -pistenäytöille. (#9249)

### Muutokset

* Päivitetty liblouis-pistekääntäjä versioksi 3.8.0. (#9013)
* Lisäosien tekijät voivat nyt pakottaa lisäosilleen NVDA:n vähimmäisversion. NVDA ei asenna eikä lataa lisäosaa, jonka NVDA-vähimmäisversio on nykyistä uudempi. (#6275)
* Tekijät voivat nyt määrittää viimeisimmän NVDA-version, jolla heidän lisäosansa on testattu. Mikäli lisäosa on testattu vain nykyistä vanhemmalla NVDA-versiolla, NVDA ei asenna eikä lataa sitä. (#6275)
* Tämä NVDA:n versio sallii sellaisten lisäosien asentamisen, jotka eivät vielä sisällä tietoa vähimmäis- ja viimeisimmästä testatusta versiosta, mutta tuleviin versioihin (esim. 2019.2) päivittäminen voi poistaa ne käytöstä automaattisesti.
* Siirrä hiiri navigointiobjektiin -komento on nyt käytettävissä Microsoft Wordissa sekä  UIA-säätimissä, erityisesti Microsoft Edgessä. (#7916, #8371)
* Hiiren alla olevan tekstin puhumista on paranneltu Microsoft Edgessä sekä muissa UIA-sovelluksissa. (#8370)
* Kun NVDA käynnistetään `--portable-path`-komentoriviparametrilla ja massamuistiversion luonti aloitetaan NVDA-valikosta, annettu hakemistopolku täytetään nyt automaattisesti massamuistiversion hakemistoksi. (#8623)
* Norjalaisen pistetaulukon tiedostopolku päivitetty vuoden 2015 standardin mukaiseksi. (#9170)
* Kirjoitusvirheitä ei enää ilmoiteta kappaleittain (Ctrl+Nuoli ylös/alas) tai taulukon soluissa (Ctrl+Alt+Nuolinäppäimet) liikuttaessa, vaikka NVDA olisi määritetty tekemään niin automaattisesti. Tämä johtuu siitä, että kappaleet ja taulukon solut voivat olla varsin suuria, ja kirjoitusvirheiden tunnistaminen voi kestää joissakin sovelluksissa kauan. (#9217)
* NVDA ei enää lataa käyttäjän omia sovellusmoduuleita, yleisliitännäisiä tai pistenäyttö- ja syntetisaattoriajureita käyttäjän asetushakemistosta. Tällainen koodi tulee sen sijaan pakata lisäosaksi, jossa on oikeat versiotiedot, jotta varmistetaan, ettei yhteensopimatonta koodia suoriteta NVDA:n nykyisillä versioilla. (#9238)
 * Kehittäjien, jotka haluavat testata koodiaan, tulee ottaa käyttöön NVDA:n kehittäjän leikepöytähakemisto NVDA:n asetusten Lisäasetukset-kategoriasta, ja sijoittaa koodinsa 'scratchpad'-hakemistoon, joka löytyy käyttäjän NVDA-asetusten hakemistosta, kun tämä asetus on otettu käyttöön.

### Bugikorjaukset

* Puheen väliin ei enää lisätä suurta määrää hiljaisuutta OneCore-puhesyntetisaattoria käytettäessä Windows 10:n April 2018 Update -versiossa tai uudemmissa. (#8985)
* 32-bittiset emoji-merkit, jotka koostuvat kahdesta UTF-16-koodipisteestä (kuten 🤦), luetaan nyt oikein liikuttaessa merkki kerrallaan pelkkä teksti -säätimissä (kuten Muistiossa) tai selaustilassa. (#8782)
* Paranneltu uudelleenkäynnistysvahvistuksen valintaikkunaa, joka näytetään, kun käyttöliittymän kieltä on vaihdettu. Teksti ja painikkeiden nimet  ovat nyt tiiviimpiä ja selkeämpiä. (#6416)
* Mikäli kolmannen osapuolen puhesyntetisaattorin lataaminen ei onnistu, NVDA ottaa Windows 10:ssä käyttöön eSpeakin sijaan Windows OneCore -syntetisaattorin. (#9025)
* Poistettu "Tervetuloa-ikkuna"-kohde NVDA-valikosta suojatuissa ruuduissa oltaessa. (#8520)
* Välilehtipaneelien selitteet ilmoitetaan nyt johdonmukaisemmin selaustilassa Sarkain-näppäimellä liikuttaessa tai pikanavigointikomentoja käytettäessä. (#709)
* NVDA ilmoittaa nyt valinnan muutokset tietyissä ajanvalitsimissa, kuten Windows 10:n Hälytykset ja kello -sovelluksessa. (#5231)
* NVDA puhuu tilailmoitukset vaihdettaessa pikatoimintojen, kuten kirkkauden ja keskittymisavustajan tilaa Windows 10:n Toimintokeskuksessa. (#8954)
* NVDA tunnistaa kirkkaus-pikatoimintosäätimen tilanvaihtopainikkeen sijaan painikkeeksi Windows 10 October 2018 Updaten ja aiempien Toimintokeskuksessa. (#8845)
* NVDA seuraa jälleen kohdistinta sekä puhuu poistetut merkit Microsoft Excelin Siirry- ja Etsi-valintaikkunoiden muokkauskentissä. (#9042)
* Korjattu harvinainen selaustilan kaatuminen Firefoxissa. (#9152)
* NVDA ilmoittaa asianmukaisesti kohdistuksen joissakin Microsoft Office 2016:n valintanauhan säätimissä, kun ne ovat supistettuina.
* NVDA puhuu asianmukaisesti ehdotetun yhteystiedon Outlook 2016:ssa kirjoitettaessa osoitteita uusiin viesteihin. (#8502)
* 80-merkkisten EuroBraille-pistenäyttöjen muutamat viimeiset pisterivin kosketuskohdistinnäppäimet eivät enää siirrä kohdistinta pisterivin alkuun tai juuri sen jälkeiseen sijaintiin. (#9160)
* Korjattu taulukossa liikkuminen Mozilla Thunderbirdin viestiketjunäkymässä. (#8396)
* Vuorovaikutustilaan siirtyminen toimii nyt asianmukaisesti Mozilla Firefoxissa ja Google Chromessa tietyissä listaruuduissa ja puunäkymissä, joissa kohdistusta ei voi siirtää niihin itseensä, mutta niiden sisältämiin kohteisiin voi. (#3573, #9157)
* Selaustila otetaan nyt oletuksena asianmukaisesti käyttöön luettaessa viestejä Outlook 2016:ssa/365:ssä, mikäli käytetään NVDA:n kokeellista Word -asiakirjojen UI Automation -tukea. (#9188)
* NVDA:n  jumiutuminen on nyt epätodennäköisempää siten, että ainoa keino palauttaa tilanne normaaliksi on kirjautua ulos nykyisestä Windows-istunnosta. (#6291)
* NVDA ilmoittaa leikepöydän tilan Windows 10:n October 2018 Update -versiossa ja uudemmissa, kun pilvileikepöydän historia avataan leikepöydän ollessa tyhjä. (#9103)
* NVDA puhuu ylimmän hakutuloksen etsittäessä emojeita emojipaneelissa Windows 10:n October 2018 Update -versiossa ja uudemmissa. (#9105)
* NVDA ei enää jumiudu VirtualBox 5.2:n ja uudempien pääikkunassa. (#9202)
* Näppäinkomentoihin vastaaminen on voinut parantua huomattavasti Microsoft Wordissa joissakin asiakirjoissa rivi, kappale tai taulukon solu kerrallaan liikuttaessa. Parhaan suorituskyvyn varmistamiseksi Microsoft Word on määritettävä käyttämään luonnosnäkymää näppäinkomennolla Alt+Ctrl+N asiakirjan avaamisen jälkeen. (#9217) 
* Tyhjiä ilmoituksia ei enää puhuta Mozilla Firefoxissa tai Google Chromessa. (#5657)
* Huomattavia suorituskyvyn parannuksia liikuttaessa solujen välillä Microsoft Excelissä, erityisesti kun soluissa on kommentteja tai oikeellisuuden tarkistavia pudotusluetteloita. (#7348)
* Solunsisäisen muokkauksen käytöstä poistamisen ei pitäisi olla enää tarpeen Microsoft Excelin asetuksista solunmuokkaussäätimen käyttämiseksi NVDA:lla Excel 2016:ssa/365:ssä. (#8146).
* Korjattu Firefoxin jumiutuminen, jota esiintyi toisinaan liikuttaessa kiintopisteiden välillä pikanavigointikomennoilla Paranneltu Aria -lisäosan ollessa käytössä. (#8980)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2018.4.1

Tämä versio korjaa ongelman, joka aiheutti kaatumisen käynnistettäessä, mikäli NVDA:n käyttöliittymän kieleksi oli määritetty aragonia. (#9089)

## 2018.4

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. suorituskyvyn parannukset uusimmissa Mozilla Firefoxin versioissa, emojien puhuminen kaikilla syntetisaattoreilla, vastattu/välitetty-tilan ilmoittaminen Outlookissa, Kohdistimen etäisyyden ilmoittaminen sivun reunasta Microsoft Wordissa, sekä useat ohjelmavirheiden korjaukset.

### Uudet ominaisuudet

* Uusia pistetaulukoita: mandariinikiina (Kiina) tasot 1 ja 2. (#5553)
* Viestien vastattu/välitetty-tila ilmoitetaan nyt Microsoft Outlookin viestiluettelossa. (#6911)
* NVDA voi nyt lukea emojien sekä muiden Unicode Common Locale Data -tietokantaan kuuluvien merkkien kuvaukset. (#6523)
* Kohdistimen etäisyys sivun ylä- ja vasemmasta reunasta voidaan lukea Microsoft Wordissa painamalla NVDA+Laskinnäppäimistön Del. (#1939)
* NVDA ei enää ilmoita Google Sheetsissä jokaisen solun kohdalla "valittu" siirrettäessä kohdistusta niiden välillä pistenäyttötilan ollessa käytössä. (#8879)
* Lisätty tuki Foxit Readerille ja Foxit Phantom PDF:lle. (#8944)
* Lisätty tuki DBeaver-tietokantatyökalulle. (#8905)

### Muutokset

* Objektien lukeminen -valintaikkunan "Lue ohjeselitteet" -asetuksen uusi nimi on "Lue ilmoitukset", jotta siihen sisältyy ilmoitusruutujen lukeminen Windows 8:ssa ja uudemmissa. (#5789)
* NVDA-toimintonäppäimiä käyttöön ottavat tai käytöstä poistavat valintaruudut  näytetään nyt näppäimistöasetuksissa erillisten sijaan luettelona.
* NVDA ei enää näytä tarpeetonta tietoa luettaessa kelloa ilmoitusalueelta joissakin Windows-versioissa. (#4364)
* Päivitetty liblouis-pistekääntäjä versioksi 3.7.0. (#8697)
* Päivitetty eSpeak-NG muutoksella 919f3240cbb.

### Bugikorjaukset

* Viestien luokka ja lipun tila luetaan Outlook 2016:ssa/365:ssä. (#8603)
* Kun NVDA:n kieleksi on asetettu esim. kirgiisi, mongoli tai makedonia, se ei näytä enää käynnistyessään valintaikkunaa, jossa varoitetaan, ettei käyttöjärjestelmä tue kyseistä kieltä. (#8064)
* Hiiren siirtäminen navigointiobjektiin siirtää nyt hiiren paljon tarkemmin selaustilan sijaintiin Mozilla Firefoxissa, Google Chromessa ja Acrobat Reader DC:ssä. (#6460)
* Vuorovaikutusta verkkosivuilla olevien yhdistelmäruutujen kanssa on parannettu Firefoxissa, Chromessa ja Internet Explorerissa. (#8664)
* Jos käytössä on Windows XP:n tai Vistan japaninkielinen versio, NVDA näyttää nyt odotetusti ilmoituksen käyttöjärjestelmävaatimuksista. (#8771)
* Suorituskykyä parannettu Mozilla Firefoxissa selattaessa suuria sivuja, joilla on paljon dynaamisia muutoksia. (#8678)
* Fontin määreitä ei enää näytetä pistenäytöllä, mikäli ne on poistettu käytöstä Asiakirjojen muotoiluasetuksista. (#7615)
* NVDA seuraa nyt kohdistusta asianmukaisesti Resurssienhallinnassa ja muissa UI Automation -rajapintaa käyttävissä sovelluksissa, kun jokin toinen sovellus on varattuna (esim. äänen eräajo). (#7345)
* Esc-näppäin välitetään  nyt verkkosivujen ARIA-valikoissa oltaessa suoraan kyseiselle valikolle, eikä vuorovaikutustilaa poisteta käytöstä. (#3215)
* Kun pikanavigointinäppäimiä käytetään uudessa Gmailissa viestejä luettaessa, koko viestin sisältöä ei enää lueta sen elementin jälkeen, johon siirryttiin. (#8887)
* Kun NVDA on päivitetty, selaimien, kuten Firefox ja google Chrome, ei pitäisi enää kaatua, ja kaikkien sillä hetkellä ladattuina olevien sivujen päivitysten pitäisi edelleen näkyä selaustilassa. (#7641) 
* NVDA ei enää ilmoita selaustilassa "napsautettava" useita kertoja peräkkäin liikuttaessa napsautettavassa sisällössä. (#7430)
* Baum Vario 40 -pistenäyttöjen näppäinkomentojen suorittaminen onnistuu nyt asianmukaisesti. (#8894)
* NVDA ei enää ilmoita Google Slidesissa jokaisen aktiivisen säätimen valittua tekstiä Mozilla Firefoxia käytettäessä. (#8964)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2018.3.2

Tämä versio kiertää ongelman, jossa Google Chrome kaatui selatessa twiittejä osoitteessa [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Tämä versio korjaa kriittisen ohjelmavirheen, joka aiheutti Mozilla Firefoxin 32-bittisten versioiden kaatumisen. (#8759)

## 2018.3

Tämän version merkittävimpiä uusia ominaisuuksia ovat useiden pistenäyttöjen automaattinen tunnistaminen, tuki uusille Windows 10:n ominaisuuksille kuten emojinsyöttöpaneelille, sekä monet muut bugikorjaukset.

== Uudet ominaisuudet =

* NVDA ilmoittaa Mozilla Firefoxissa ja Google Chromessa kielioppivirheistä, kun tieto niistä välitetään verkkosivuilla asianmukaisesti. (#8280)
* Verkkosivujen lisättäväksi tai poistettavaksi merkitty sisältö ilmoitetaan nyt Google Chromessa. (#8558)
* Lisätty tuki BrailleNote QT:n ja Apex BT:n vieritysrullalle, kun BrailleNotea käytetään pistenäyttönä NVDA:n kanssa. (#5992, #5993)
* Lisätty komennot nykyisen kappaleen kuluneen ajan ja kokonaiskeston ilmoittamiseen Foobar2000:ssa. (#6596)
* Mac-komentonäppäimen symboli (⌘) puhutaan nyt luettaessa tekstiä mitä tahansa syntetisaattoria käytettäessä. (#8366)
* Mukautettuja rooleja tuetaan nyt aria-roledescription-attribuutin välityksellä kaikissa verkkoselaimissa. (#8448)
* Uusia pistetaulukoita: tšekkiläinen 8 pisteen tietokonemerkistö, keski-kurdi, esperanto, unkarilainen, ruotsalainen 8 pisteen tietokonemerkistö. (#8226, #8437)
* Lisätty tuki automaattiselle pistenäytön tunnistukselle. (#1271)
 * Tällä hetkellä tuetaan ALVA-, Baum/HumanWare/APH/Orbit-, Eurobraille-, Handy Tech-, Hims-, SuperBraille- ja HumanWare BrailleNote- sekä Brailliant BI/B -näyttöjä.
 * Toiminto voidaan ottaa käyttöön valitsemalla vaihtoehto "automaattinen" pistenäyttöluettelosta NVDA:n Valitse pistenäyttö -valintaikkunasta.
 * Lisätietoja löytyy käyttöoppaasta.
* Lisätty tuki useille Windows 10:n viimeisimmissä versioissa esitellyille moderneille syöttöominaisuuksille. Näitä ovat emojipaneeli (Fall Creators -päivitys), sanelu (Fall Creators -päivitys), fyysisen näppäimistön syöttöehdotukset (April 2018 -päivitys) sekä pilvileikepöydän liittäminen (October 2018 -päivitys). (#7273)
* Sisältöä, joka on merkitty sisennetyksi kappaleeksi ARIAn blockquote-roolimääritystä käyttäen, tuetaan nyt Mozilla Firefox 63:ssa. (#8577)

### Muutokset

* NVDA:n Yleiset asetukset -valintaikkunan käytettävissä olevien kielten luettelo  lajitellaan nyt ISO 639 -koodien asemesta kielen nimen perusteella. (#7284)
* Lisätty oletusnäppäinkomentoja Alt+Vaihto+Sarkain- ja Windows+Sarkain-näppäinyhdistelmille kaikille tuetuille Freedom Scientificin pistenäytöille. (#7387)
* ALVA BC680- ja protokollamuunninta käyttävissä pistenäytöissä on nyt mahdollista liittää eri toimintoja vasempaan ja oikeaan älynäppäimistöön sekä peukalo- ja etouch-näppäimiin. (#8230)
* ALVA BC6 -näytöissä näppäinyhdistelmä sp2+sp3 puhuu päivämäärän ja kellonajan, kun taas sp1+sp2 jäljittelee Windows-näppäintä. (#8230)
* Käyttäjältä kysytään nyt kerran NVDA:n käynnistyessä, sallitaanko käyttötilastojen lähettäminen NV Accessille automaattisen päivitystarkistuksen yhteydessä. (#8217)
* Jos käyttäjä on sallinut käyttötilastojen lähettämisen, NVDA lähettää nyt päivitystä tarkistettaessa nykyisen syntetisaattorin ja käytössä olevan pistenäytön nimen, jotta niiden ajurien tulevaa kehitystä voidaan priorisoida paremmin. (#8217)
* Päivitetty liblouis-pistekääntäjä versioksi 3.6.0. (#8365)
* Venäläisen 8 pisteen pistetaulukon tiedostopolku korjattu. (#8446)
* Päivitetty eSpeak-ng versioksi 1.49.3dev muutos 910f4c2. (#8561)

### Bugikorjaukset

* Saavutettavat selitteet  ilmoitetaan nyt herkemmin Google Chromessa selaustilassa oltaessa, kun selite ei näy sisällön osana. (#4773)
* Zoomissa tuetaan nyt ilmoituksia. Niitä ovat esim. mykistyksen/mykistyksen poiston tila sekä saapuvat viestit.(#7754)
* Pistekirjoitustuloste ei enää lakkaa seuraamasta selaustilakohdistinta, kun Kohdistuskontekstin näyttämisasetusta vaihdetaan selaustilassa oltaessa. (#7741)
* Korjattu ALVA BC680 -pistenäyttöjen alustuksen ajoittainen epäonnistuminen. (#8106)
* ALVA BC6 -näytöt eivät enää oletusarvoisesti suorita emuloitujen näppäimien painalluksia painettaessa sp2+sp3-näppäimiä sisältäviä  näppäinkomentoja sisäisen toiminnallisuuden käynnistämiseksi. (#8230)
* Alt-näppäimen emulointi ALVA BC6 -näytön sp2-näppäintä painamalla toimii nyt, kuten on ilmoitettu. (#8360)
* NVDA ei enää puhu tarpeettomia näppäinasettelun muutoksia. (#7383, #8419)
* Hiiren seuranta on nyt paljon tarkempaa Muistiossa sekä muissa pelkkäteksti-muokkaussäätimissä oltaessa asiakirjassa, jossa on enemmän kuin 65535 merkkiä. (#8397)
* NVDA tunnistaa enemmän valintaikkunoita Windows 10:ssä ja muissa moderneissa sovelluksissa. (#8405)
* Järjestelmäkohdistuksen seuraaminen ei enää epäonnistu Windows 10:n October 2018 -päivityksessä ja Server 2019:ssä ja uudemmissa sovelluksen jäädessä jumiin tai ryöpyttäessä järjestelmää tapahtumilla. (#7345, #8535)
* Käyttäjille ilmoitetaan heidän yrittäessään lukea tai kopioida tyhjää tilariviä. (#7789)
* Korjattu ongelma, jossa säätimien "ei valittu" -tilaa ei ilmoiteta puheella, mikäli kyseinen säädin oli aiemmin osittain valittuna. (#6946)
* Kielen nimi näytetään burmalle asianmukaisesti NVDA:n yleisten asetusten kieliluettelossa Windows 7:ssä. (#8544)
* NVDA puhuu Microsoft Edgessä ilmoitukset, kuten lukunäkymän saatavuuden ja sivun lataamisen edistymisen. (#8423)
* Kun pistenäytöllä ollaan asiakirjan alussa, teksti näkyy nyt näytöllä siten, että asiakirjan ensimmäinen merkki on näytön vasemmassa reunassa kuten muissakin monirivisissä tekstikentissä. (#8406)
* Kun verkkosivulla siirrytään luetteloon, NVDA ilmoittaa nyt sen selitteen, mikäli sivun tekijä on sen määrittänyt. (#7652)
* Kun tietyn pistenäytön toimintoja liitetään näppäinkomentoihin, kyseiset näppäinkomennot näkyvät määriteltyinä juuri sille näytölle. Aiemmin ne näkyivät ikään kuin ne olisi määritelty sillä hetkellä käytössä olevalle näytölle. (#8108)
* Lisätty tuki Media Player Classicin 64-bittiselle versiolle. (#6066)
* Useita parannuksia Microsoft Wordin pistenäyttötukeen UI Automationin ollessa käytössä:
 * Vähennetty kohdistuksen näyttämisen puheliaisuutta sekä puheella että pistekirjoituksella, kun kohdistus siirretään Word-asiakirjaan. (#8407)
 * Kohdistimen siirtäminen pistenäytön kosketuskohdistinnäppäimillä toimii nyt asianmukaisesti oltaessa luettelossa Word-asiakirjassa. (#7971)
 * Äskettäin Word-asiakirjaan lisätyt luettelomerkit/numerot ilmaistaan asianmukaisesti sekä puheella että pistenäytöllä. (#7970)
* Lisäosien asentaminen on nyt mahdollista Windows 10:n versiossa 1803 ja uudemmissa, jos "Käytä Unicode UTF-8 -merkistöä maailmanlaajuista kielitukea varten" -ominaisuus on käytössä. (#8599)
* NVDA ei enää tee iTunes 12.9:stä ja uudemmista täysin käyttökelvotonta. (#8744)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2018.2.1

Tämä versio sisältää päivitettyjä käännöksiä, jotka johtuivat ongelmia aiheuttaneen ominaisuuden viime hetken poistosta.

## 2018.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat tuki taulukoille Kindle for PC:ssä, tuki HumanWare BrailleNote Touch- ja BI14-pistenäytöille, parannukset sekä OneCore- että SAPI5-puhesyntetisaattoreihin, parannukset Microsoft Outlookiin sekä paljon muuta.

### Uudet ominaisuudet

* Taulukon solujen rivien ja sarakkeiden jakaantuminen useammalle riville ilmaistaan nyt puheella ja pistekirjoituksella. (#2642)
* NVDA:n taulukonselauskomentoja tuetaan nyt Google Docsissa pistekirjoitustilan ollessa käytössä. (#7946)
* Taulukoiden lukeminen ja niissä liikkuminen on nyt mahdollista Kindle for PC:ssä. (#7977)
* Tuki BrailleNote Touch- ja Brailliant BI 14 -pistenäytöille sekä USB:llä että bluetoothilla liitettäessä. (#6524)
* NVDA voi puhua sovellusten (esim. Laskin ja Kauppa) ilmoitukset Windows 10:n Fall Creators -päivityksessä ja uudemmissa. (#7984)
* Uusia pistetaulukkoja: liettualainen 8 pisteen merkistö, ukrainalainen, mongolilainen taso 2. (#7839)
* Lisätty komento määrätyssä pistesolussa olevan tekstin muotoilutietojen ilmoittamiseen. (#7106)
* NVDA-päivityksen asentamista on nyt mahdollista lykätä myöhemmäksi. (#4263) 
* Uusia kieliä: mongoli ja sveitsinsaksa.
* Voit nyt vaihtaa Ctrl-, Vaihto-, Alt-, Windows- ja NVDA-näppäinten tilaa pistekirjoitusnäppäimistöltä sekä käyttää niitä yhdessä pistekirjoitussyötteen kanssa (esim. painaa Ctrl+S). (#7306) 
 * Näiden tilanvaihtonäppäinten uudelleenmäärittäminen on mahdollista Näppäinkomennot-valintaikkunan Emuloidut näppäimet -kategorian alta löytyviä komentoja käyttäen.
* Palautettu tuki Handy Techin Braillino- sekä Modular (vanha laiteohjelmisto) -pistenäytöille. (#8016)
* Päivämäärää ja aikaa tukevat Handy Tech -laitteet (kuten Active Braille ja Active Star) synkronoidaan nyt automaattisesti NVDA:n toimesta, kun ero järjestelmän kelloon on enemmän kuin viisi sekuntia. (#8016)
* Asetusprofiilien tilapäiseen käytöstä poistamiseen on nyt mahdollista määrittää näppäinkomento. (#4935)

### Muutokset

* Lisäosien hallinnan Tila-saraketta on muutettu siten, että se ilmaisee käynnissä- tai pysäytetty-tilojen sijaan, onko lisäosa "käytössä" vai poistettu käytöstä ("ei käytössä"). (#7929)
* Päivitetty liblouis-pistekääntäjä versioksi 3.5.0. (#7839)
* Liettualaisen pistetaulukon uusi nimi on nyt "liettua, 6 pisteen merkistö", jotta vältetään sekaannus uuden 8 pisteen taulukon kanssa. (#7839)
* Kanadanranskalaiset tason 1 ja 2 taulukot on poistettu. Niiden asemesta käytetään ranskalaista yhdenmukaistettua 6 pisteen tietokonemerkistön ja tason 2 taulukoita. (#7839)
* Alva BC6-, EuroBraille- ja Papenmeier-pistenäyttöjen toissijaiset kosketuskohdistinnäppäimet ilmoittavat nyt pistesolussa olevan tekstin muotoilutiedot. (#7106)
* Lyhennepistekirjoituksen syöttötaulukot vaihtavat automaattisesti takaisin lyhentämättömään tilaan ei-muokattavissa paikoissa (ts. säätimissä, joissa ei ole kohdistinta, tai selaustilassa). (#7306)
* NVDA:n puheliaisuutta on vähennetty Outlookin kalenterissa, kun tapaaminen tai aikaväli käsittää koko päivän. (#7949)
* Kaikki NVDA:n asetukset löytyvät nyt  yhdestä asetusvalintaikkunasta, johon pääsee kohdasta NVDA-valikko -> Asetukset -> Asetukset, sen sijaan, että ne olisivat ripoteltuina useisiin eri ikkunoihin. (#577)
* Oletussyntetisaattori on nyt Windows 10:tä käytettäessä eSpeakin asemesta Windows OneCore. (#8176)

### Bugikorjaukset

* NVDA lukee nyt Asetukset-sovelluksen Microsoft-tilin kirjautumisnäytön aktiiviset säätimet sähköpostiosoitteen syöttämisen jälkeen. (#7997)
* NVDA lukee nyt asianmukaisesti edellisen sivun palattaessa sille Microsoft Edgessä. (#7997)
* NVDA ei enää virheellisesti puhu windows 10:n kirjautumisen PIN-koodin viimeistä merkkiä koneen lukitusta avattaessa. (#7908)
* Valintaruutujen ja -painikkeiden selitteitä ei enää puhuta kahdesti Chromessa ja Firefoxissa selaustilassa Sarkaimella siirryttäessä tai pikanavigointikomentoja käytettäessä. (#7960)
* Aria-current-attribuutti, jonka arvo on false, ilmoitetaan nyt asianmukaisesti falsena truen asemesta. (#7892)
* Windows OneCore -äänien lataaminen ei enää epäonnistu, jos käytössä oleva ääni on poistettu. (#7553)
* Windows OneCore -äänien vaihtaminen on nyt paljon nopeampaa. (#7999)
* Korjattu väärin muotoiltu pistekirjoituksen tulostus useista pistetaulukoista, mukaan lukien isojen kirjainten merkit tanskalaisessa 8 pisteen lyhennekirjoituksessa. (#7526, #7693)
* NVDA voi nyt puhua Microsoft Wordissa useammantyyppisiä luettelomerkkejä. (#6778)
* Lue muotoilutiedot -komennon painaminen ei enää siirrä virheellisesti tarkastelukohtaa, ja näin ollen useasti painaminen ei myöskään anna enää eri tuloksia. (#7869)
* Pistekirjoituksen syöttö ei enää salli lyhennepistekirjoitusta paikoissa, joissa sitä ei tueta (ts. kokonaisia sanoja ei enää lähetetä järjestelmälle muualla kuin tekstisisällössä ja selaustilassa). (#7306)
* Korjattu Handy Techin Easy Braille- ja Braille Wave -pistenäyttöjen yhteyden vakauteen liittyviä ongelmia. (#8016)
* NVDA ei enää ilmoita Windows 8:ssa ja uudemmissa  "tuntematon" pikalinkkivalikkoa (Windows+X) avattaessa ja valittaessa sen kohteita. (#8137)
* HIMS-pistenäyttöjen mallikohtaiset painikkeiden näppäinkomennot toimivat nyt kuten käyttöohjeessa ilmoitetaan. (#8096)
* NVDA yrittää nyt korjata järjestelmän COM-rekisteröintien ongelmia, jotka aiheuttavat ohjelmien (kuten Firefox ja Internet Explorer) muuttumista esteellisiksi sekä NVDA:n "tuntematon"-ilmoituksia. (#2807)
* Kierretty Tehtävienhallinnan ongelma, joka esti NVDA:n käyttäjiä lukemasta prosessien yksityiskohtaisia tietoja. (#8147)
* Uudet Microsoft SAPI5 -äänet reagoivat nyt nopeammin, mikä tekee niiden käyttämisestä sujuvampaa. (#8174)
* NVDA ei enää puhu tai näytä pistenäytöllä vasemmalta oikealle ja oikealta vasemmalle osoittavia nuolimerkkejä käytettäessä kelloa Windowsin uusimmissa versioissa. (#5729)
* HIMS Smart Beetle -pistenäyttöjen vieritysnäppäinten tunnistaminen ei ole enää epäluotettavaa. (#6086)
* Muokkausta ja navigointia koskevat tiedot ovat nyt paljon luotettavampia joissakin tekstisäätimissä, erityisesti Delphi-sovelluksissa. (#636, #8102)
* NVDA ei enää puhu tarpeetonta tietoa vaihdettaessa sovellusta Alt+Sarkain-näppäimillä Windows 10 RS5:ssä. (#8258)

## 2018.1.1

Tämä on erikoisversio, joka ratkaisee Windowsin OneCoreSpeech-syntetisaattoriajurissa olevan bugin,  jonka vuoksi NVDA puhui korkeammalla äänellä ja nopeammin Windows 10:n Redstone 4 (1803) -versiossa. (#8082)  

## 2018.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat tuki kaavioille Microsoft Wordissa ja PowerPointissa, tuki uusille Eurobraille-pistenäytöille ja Optelecin protokollamuuntimelle, paranneltu tuki Hims- ja Optelec-pistenäytöille, suorituskyvyn parannukset Mozilla Firefox 58:lle ja uudemmille, sekä monet muut.

### Uudet ominaisuudet

* Vuorovaikutus Microsoft Wordin ja PowerPointin kaavioiden kanssa on nyt mahdollista samalla tavoin kuin Excelissä. (#7046)
 * Wordissa: Siirry selaustilassa ollessasi nuolinäppäimillä upotetun kaavion kohdalle ja paina Enter ollaksesi vuorovaikutuksessa sen kanssa.
 * PowerPointissa diaa muokattaessa: Siirry Sarkain-näppäimellä kaavio-objektiin ja paina Enter tai Välilyöntiä ollaksesi vuorovaikutuksessa kaavion kanssa.
 * Lopeta vuorovaikutus painamalla Esc-näppäintä.
* Uusi kieli: kirgiisi.
* Lisätty tuki VitalSource Bookshelf -ePUB-lukijalle. (#7155)
* Lisätty tuki Optelecin protokollamuunninlaitteelle, joka mahdollistaa Braille Voyager- ja Satellite-näyttöjen käytön ALVA BC6:n kommunikointiprotokollan avulla. (#6731)
* Pistekirjoituksen syöttäminen on nyt mahdollista ALVA 640 Comfort -pistenäytöllä. (#7733) 
 * NVDA:n pistekirjoituksensyöttötoimintoa voidaan käyttää tällä laitteella sekä muilla BC6-näytöillä, joissa on laiteohjelmiston versio 3.0.0 tai uudempi.
* Varhainen tuki Google Sheetsille pistekirjoitustilan ollessa käytössä. (#7935)
* Tuki Eurobraille Esys-, Esytime- ja Iris-pistenäytöille. (#7488)

### Muutokset

* HIMS Braille Sense/Braille EDGE/Smart Beetle- ja Sync Braille -pistenäyttöjen ajurit on korvattu yhdellä ajurilla. Uusi ajuri otetaan automaattisesti käyttöön aiemman Sync Braille -ajurin käyttäjillä. (#7459)
 * Jotkin näppäimet, erityisesti vieritykseen käytettävät, on uudelleenmääritelty seuraamaan HIMS-tuotteiden käytäntöjä. Katso lisätietoja käyttöoppaasta.
* Kun näyttönäppäimistöllä kirjoitetaan kosketusvuorovaikutuksen avulla, kutakin näppäintä on oletusarvoisesti kaksoisnapautettava samalla tavoin kuin mitä tahansa muutakin säädintä aktivoitaessa.
 * Kosketuskirjoitustila, jossa sormen nostaminen näppäimeltä riittää sen painamiseen, otetaan käyttöön uudessa Kosketuksen vuorovaikutus -valintaikkunassa, joka löytyy Asetukset-valikosta. (#7309)
* Pistenäyttöä ei ole enää tarpeen määrittää seuraamaan erikseen kohdistusta tai tarkastelukohdistinta, sillä se tapahtuu nyt oletuksena automaattisesti. (#2385) 
 * Huomaa, että tarkastelukohdistinta seurataan automaattisesti vain tekstintarkastelu- tai objektinavigointikomentoa käytettäessä. Näytön vierittäminen ei aktivoi tätä ominaisuutta.

### Bugikorjaukset

* Selattavat ilmoitukset, kuten nykyisten muotoilutietojen näyttäminen painettaessa kaksi kertaa nopeasti NVDA+F, eivät enää epäonnistu, kun NVDA on asennettu hakemistopolkuun, jonka nimessä on muita kuin ASCII-merkkejä. (#7474)
* Kohdistus palautetaan taas asianmukaisesti palattaessa Spotifyhin toisesta sovelluksesta. (#7689)
* NVDA:n päivittäminen ei enää epäonnistu Windows 10:n Fall Creators -päivityksessä, kun hallittu kansion käyttö on otettu käyttöön Windows Defender Security Centeristä. (#7696)
* Hims Smart Beetle -pistenäyttöjen vieritysnäppäinten havaitseminen ei enää ole epäluotettavaa. (#6086)
* Pieni suorituskyvyn parannus ladattaessa suurta määrää sisältöä Mozilla Firefox 58:ssa ja uudemmissa. (#7719)
* Taulukoita sisältävien sähköpostien lukeminen ei enää aiheuta virheitä Microsoft Outlookissa. (#6827)
* Pistenäyttöjen näppäinkomentoja, jotka emuloivat näppäimistön Alt-, Ctrl-, Shift- ja Windows-näppäimiä, voi nyt käyttää myös yhdessä muiden emuloitujen näppäimistön näppäinten kanssa, mikäli yksi tai useampi käytetyistä näytön näppäinkomennoista on mallikohtaisia. (#7783)
* Selaustila toimii nyt asianmukaisesti Mozilla Firefoxissa lisäosien, kuten LastPass ja bitwarden, luomissa ponnahdusikkunoissa. (#7809)
* NVDA ei jää enää ajoittain jumiin jokaisesta kohdistusmuutoksesta, mikäli Firefox tai Chrome on lakannut vastaamasta esim. jumiutumisen tai kaatumisen vuoksi. (#7818)
* NVDA ei enää ohita viimeistä 20 merkkiä 280 merkin mittaisista twiiteistä luettaessa niitä Twitter-asiakasohjelmissa, kuten Chicken Nuggetissa. (#7828)
* NVDA käyttää nyt asianmukaista kieltä symboleita puhuttaessa tekstin ollessa valittuna. (#7687)
* Excel-kaavioissa liikkuminen on jälleen mahdollista nuolinäppäimillä Office 365:n viimeisimmissä versioissa. (#7046)
* Säätimien tilat ilmoitetaan nyt puheella ja pistekirjoituksella aina samassa järjestyksessä riippumatta siitä, ovatko ne positiivisia vai negatiivisia. (#7076)
* Kirjoitettujen merkkien puhuminen ei enää epäonnistu askelpalautinta painettaessa tietyissä sovelluksissa, kuten esim. Windows 10:n Sähköposti. (#7456)
* Kaikki Hims Braille Sense Polaris -pistenäyttöjen näppäimet toimivat nyt odotetusti. (#7865)
* NVDA:n käynnistyminen ei enää epäonnistu Windows 7:ssä virheilmoitukseen puuttuvasta api-ms-DLL-tiedostosta, kun jokin toinen sovellus on asentanut tietyn version Visual Studio 2017:n edelleenjaettavista osista. (#7975)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2017.4

Tämän version merkittävimpiä ominaisuuksia ovat mm. useat verkkoselauksen tuen korjaukset ja parannukset, mukaan lukien oletusarvoinen selaustila verkkopohjaisille valintaikkunoille ja parempi lomakekenttäryhmien nimien ilmaiseminen selaustilassa, tuki uusille Windows 10:n teknologioille, kuten Windows Defenderin sovellussuojalle ja ARM64-alustalle, sekä automaattinen ruudun suunnan ja akun tilan ilmoittaminen.  
Huomaa, että tämä versio ei enää tue Windows XP:tä tai Vistaa. Vähimmäisvaatimus on nyt Windows 7 Service Pack 1-päivityksellä.

### Uudet ominaisuudet

* Selaustilassa on nyt mahdollista siirtyä kiintopisteiden alkuun tai niiden ohi säilön loppuun/alkuun siirtäviä komentoja (pilkku/Shift+pilkku) käyttäen. (#5482)
* Muokkaus- ja lomakekenttiin siirtävillä pikanavigointikomennoilla on nyt Firefoxissa, Chromessa ja Internet Explorerissa mahdollista siirtyä muokattavaan monimuotoiseen tekstisisältöön (esim. contentEditable). (#5534)
* Elementtilista voi nyt näyttää verkkoselaimissa  luettelon lomakekentistä ja painikkeista. (#588)
* Perustuki Windows 10:lle ARM64-alustalla. (#7508)
* Varhainen tuki Kindle-kirjojen saavutettavan matemaattisen sisällön lukemiselle ja vuorovaikutteiselle selaamiselle. (#7536)
* Lisätty tuki Azardi-e-kirjalukijalle. (#5848)
* Lisäosien versiotiedot ilmoitetaan nyt päivitettäessä. (#5324)
* Lisätty uusia komentoriviparametreja NVDA:n massamuistiversion luomiseen. (#6329)
* Tuki Windows Defenderin sovellussuojassa ajettavalle Microsoft Edgelle Windows 10:n Fall Creators -päivityksessä. (#7600)
* NVDA ilmoittaa nyt kannettavaa tai tablettia käytettäessä, kun laturi kytketään/irrotetaan ja kun näytön suunta muuttuu. (#4574, #4612)
* Uusi kieli: makedonia.
* Uusia pistetaulukoita: kroatialainen taso 1, vietnamilainen taso 1. (#7518, #7565)
* Lisätty tuki Handy Techin Actilino-pistenäytölle. (#7590)
* Pistekirjoituksen syöttöä tuetaan nyt Handy Techin pistenäytöissä. (#7590)

### Muutokset

* Vanhin NVDA:n tukema käyttöjärjestelmä on nyt Windows 7 Service Pack 1 -päivityksellä tai Windows Server 2008 R2 Service Pack 1 -päivityksellä. (#7546)
* Verkkopohjaiset valintaikkunat käyttävät nyt Firefoxissa ja Chromessa automaattisesti selaustilaa, ellei olla verkkosovelluksessa. (#4493)
* Sarkaimella ja pikanavigointinäppäimillä siirtyminen ei enää ilmoita selaustilassa siirtymistä pois säilöistä, kuten luetteloista ja taulukoista, mikä tekee navigoinnista tehokkaampaa. (#2591)
* Lomakekenttäryhmien nimi ilmoitetaan nyt selaustilassa, kun niihin siirrytään pikanavigointikomennoilla tai sarkaimella Firefoxissa ja Chromessa. (#3321)
* Upotettuihin objekteihin selaustilassa siirtävä pikanavigointikomento (O ja Shift+O) siirtää nyt ääni- ja videoelementteihin sekä sellaisiin, jotka on merkitty application- ja dialog-ARIA-rooleilla. (#7239)
* Espeak-ng on päivitetty versioksi 1.49.2, jossa on korjattu joitakin virallisen version tuottamisessa olleita ongelmia. (#7385)
* Tilarivin teksti kopioidaan leikepöydälle kolmannella Lue tilarivi -komennon painalluksella. (#1785)
* Kun näppäinkomentoja liitetään Baum-pistenäytön näppäimiin, ne voidaan rajoittaa vain käytössä olevaan näyttöön (esim. VarioUltra tai Pronto). (#7517)
* Selaustilan elementtilistan Suodata-kentän pikanäppäin on muutettu englanninkielisessä käyttöliittymässä Alt+F:stä Alt+E:ksi. (#7569)
* Lisätty selaustilaan määrittämätön näppäinkomento, jolla asettelutaulukoiden ilmaiseminen voidaan ottaa lennossa käyttöön tai poistaa se käytöstä. Komento löytyy Näppäinkomennot-valintaikkunan Selaustila-kategoriasta. (#7634)
* Päivitetty liblouis-pistekääntäjä versioksi 3.3.0. (#7565)
* Puhesanastovalintaikkunan säännöllisen lausekkeen valintapainikkeen pikanäppäin on vaihdettu englanninkielisessä käyttöliittymässä Alt+R:stä Alt+E:ksi. (#6782)
* Puhesanastotiedostot on nyt versioitu ja siirretty speechDicts/voiceDicts.v1-hakemistoon. (#7592)
* Versioitujen tiedostojen (käyttäjän asetukset ja puhesanastot) muutoksia ei enää tallenneta, kun NVDA:ta ajetaan käynnistimestään. (#7688)
* Handy Techin Braillino- ja Bookworm- sekä vanhalla laiteohjelmistolla varustettuja Modular-pistenäyttöjä ei enää tueta suoraan asennuksen jälkeen. Asenna Handy Techin yleisajuri ja NVDA:n lisäosa käyttääksesi niitä. (#7590)

### Bugikorjaukset

* Linkit ilmaistaan nyt pistekirjoituksella sellaisissa sovelluksissa kuin Microsoft Word. (#6780)
* NVDA ei muutu enää huomattavasti hitaammaksi, kun Firefox- tai Chrome-verkkoselaimissa on avoinna useita välilehtiä. (#3138)
* MDV Lilli -pistenäytön kohdistimensiirtonäppäimet eivät enää virheellisesti siirrä yhtä pistesolua edemmäs kuin pitäisi. (#7469)
* HTML5:n required-attribuuttia tuetaan nyt ilmaisemaan lomakekentän pakollisuutta. (#7321)
* Pistenäyttö päivittyy nyt kirjoitettaessa arabialaisia merkkejä vasemmalle tasattuun WordPad-asiakirjaan. (#511)
* Säätimien saavutettavat selitteet ilmoitetaan nyt herkemmin selaustilassa Mozilla Firefoxissa, kun selite ei näy sisältönä. (#4773)
* Firefoxia on taas mahdollista käyttää NVDA:lla sen uudelleenkäynnistyksen jälkeen windows 10:n Creators-päivityksessä. (#7269)
* Selaustila on taas käytettävissä, kun NVDA käynnistetään uudelleen Mozilla Firefoxin ollessa aktiivisena. Saatat tosin joutua siirtymään Alt+Sarkain-näppäinyhdistelmällä pois Firefoxista ja taas takaisin. (#5758)
* Matemaattisen sisällön käyttäminen on mahdollista Google Chromessa järjestelmissä, joissa ei ole asennettuna Mozilla Firefoxia. (#7308)
* Käyttöjärjestelmän ja muiden sovellusten pitäisi olla vakaampia heti NVDA:n asennuksen jälkeen ennen uudelleenkäynnistystä verrattaessa aiempien NVDA-versioiden asennuksiin. (#7563)
* Mikäli navigointiobjekti on hävinnyt sisällöntunnistuskomentoa (esim. NVDA+R) käytettäessä, NVDA antaa nyt virheilmoituksen sen sijaan, että asiasta ei ilmoiteta lainkaan. (#7567)
* Korjattu taaksepäin vierittämisen toiminnallisuus Freedom Scientificin pistenäytöissä, joissa on pitkä vasemmanpuoleinen vieritysnäppäin. (#7713)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2017.3

Tämän version merkittävimpiä uusia ominaisuuksia ovat lyhennepistekirjoituksen syöttäminen, tuki uusille Windows 10:n OneCore-äänille, sisäänrakennettu tuki Windows 10:n tekstintunnistukselle sekä useat merkittävät pistekirjoitukseen ja verkon selaamiseen liittyvät parannukset.

### Uudet ominaisuudet

* Lisätty pistekirjoitusasetus, joka näyttää ilmoitukset pysyvästi. (#6669)
* NVDA ilmoittaa nyt Microsoft Outlookin viestiluettelossa, mikäli viesti on liputettu. (#6374)
* Tarkka muodon tyyppi ilmoitetaan nyt Microsoft Powerpointissa diaa muokattaessa (esim. kolmio, ympyrä, video, nuoli) pelkän yleisen "muoto"-tyypin sijaan. (#7111)
* MathML-tyyppistä matemaattista sisältöä tuetaan nyt Google Chromessa. (#7184)
* NVDA voi nyt puhua uusia Windows 10:n OneCore-ääniä käyttäen (tunnetaan myös matkapuhelinääninä). Äänet otetaan käyttöön valitsemalla Windows OneCore -vaihtoehto NVDA:n Syntetisaattorin asetukset -valintaikkunasta. (#6159)
* NVDA:n asetustiedostot on nyt mahdollista tallentaa käyttäjän paikallisten sovellustietojen kansioon. Tämä otetaan käyttöön muokkaamalla asetusta Windowsin rekisterissä. Katso lisätietoja käyttöoppaan "Järjestelmänlaajuiset parametrit" -kappaleesta. (#6812)
* NVDA ilmoittaa nyt verkkoselaimissa paikkamerkkien arvot lomakekentissä oltaessa (erityisesti aria-placeholder-attribuuttia tuetaan). (#7004)
* Microsoft Wordissa on nyt selaustilassa oltaessa mahdollista siirtyä kirjoitusvirheisiin pikanavigointikomentoja W ja Shift+W käyttäen. (#6942)
* Lisätty tuki Microsoft Outlookin tapaamisenluontivalintaikkunoiden päivämääränvalitsinsäätimelle. (#7217)
* Valittuna oleva ehdotus ilmoitetaan nyt Windows 10:n Sähköposti-sovelluksen vastaanottaja/kopio-kentissä ja Asetukset-sovelluksen haussa. (#6241)
* Windows 10:ssä toistetaan nyt ääni, joka ilmaisee ehdotusten ilmestymisen tietyissä hakukentissä (esim. aloitusnäytössä, asetushaussa tai Sähköposti-sovelluksen vastaanottaja/kopio-kentissä). (#6241)
* Ilmoitukset luetaan automaattisesti Skype for Businessin työpöytäversiossa esim. tilanteessa, jossa joku aloittaa keskustelun kanssasi.  (#7281)
* Saapuvat viestit luetaan automaattisesti Skype for Businessin keskusteluissa. (#7286)
* Ilmoitukset luetaan automaattisesti Microsoft Edgessä esim. latauksen käynnistyessä.  (#7281)
* Voit nyt kirjoittaa sekä lyhenne- että tavallista pistekirjoitusta pistenäytöillä, joissa on pistekirjoitusnäppäimistö. Katso lisätietoja käyttöoppaan Pistekirjoituksen syöttäminen -kappaleesta. (#2439)
* Voit nyt syöttää Unicode-pistekirjoitusmerkkejä pistenäytön pistekirjoitusnäppäimistöltä valitsemalla Pistekirjoitusasetukset-valintaikkunassa syöttötaulukoksi Unicode-pistekirjoitus. (#6449)
* Lisätty tuki Taiwanissa käytettävälle SuperBraille-pistenäytölle. (#7352)
* Uusia pistetaulukoita: tanskalainen 8 pisteen tietokonemerkistö, liettualainen, persialainen 8 pisteen tietokonemerkistö, persialainen taso 1, slovenialainen 8 pisteen tietokonemerkistö. (#6188, #6550, #6773, #7367)
* Paranneltu "englanti (Yhdysvallat), 8 pisteen tietokonemerkistö" -pistetaulukkoa, luettelomerkkien, euromerkin ja aksentillisten kirjainten tuki mukaan lukien. (#6836)
* NVDA voi nyt käyttää Windows 10:n tekstintunnistustoimintoa kuvien tai esteellisten sovellusten tekstin tunnistamiseen. (#7361)
 * Kieli voidaan määrittää uudesta Windows 10:n tekstintunnistus -valintaikkunasta, johon pääsee NVDA:n Asetukset-valikosta.
 * Tunnista nykyisen navigointiobjektin sisältö painamalla NVDA+R.
 * Katso lisätietoja käyttöoppaan Sisällöntunnistus-kappaleesta.
* Uudella Pistekirjoitusasetukset-valintaikkunan "Kohdistuskontekstin näyttäminen" -asetuksella voit nyt valita, mitä kontekstitietoja pistenäytöllä näytetään kohdistuksen siirtyessä objektiin. (#217)
 * Esim. "täytä näyttö kontekstin muuttuessa"- ja "vain taaksepäin vieritettäessä" -vaihtoehdot voivat tehdä luetteloiden ja valikkojen käytöstä tehokkaampaa, koska kohteiden sijainti näytöllä ei jatkuvasti muutu.
 * Katso lisätietoja ja esimerkkejä käyttöoppaan "Kohdistuskontekstin näyttäminen" -kappaleesta.
* NVDA tukee nyt Firefoxissa ja Chromessa monimuotoisia dynaamisia ruudukoita, kuten laskentataulukoita, joissa saatetaan ladata tai näyttää vain osa sisällöstä (erityisesti tuetaan ARIA 1.1:ssä esiteltyjä aria-rowcount-, aria-colcount-, aria-rowindex- ja aria-colindex-attribuutteja). (#7410)
* Kohdistimen muoto voidaan määrittää pistenäyttöä käytettäessä erilaiseksi riippuen siitä, seurataanko kohdistusta vai tarkastelukohdistinta. (#7122)
* NVDA-logo on päivitetty. Uusi logo on tyylitelty sekoitus valkoisista kirjaimista N, V, D ja A yhtenäisellä, violetilla taustalla. Tämä varmistaa, että se näkyy kaikenvärisillä taustoilla, ja siinä käytetään NV Accessin logon violettia väriä. (#7446)

### Muutokset

* Lisätty oletuksena ilman pikanäppäintä oleva syöte-ele, jolla NVDA voidaan käynnistää nopeasti uudelleen. (#6396)
* Näppäinasettelun määrittäminen on nyt mahdollista NVDA:n Tervetuloa-valintaikkunasta. (#6863)
* Entistä useampia säädintyyppejä ja -tiloja sekä kiintopisteitä on lyhennetty pistekirjoituksella. Katso täydellinen luettelo käyttöoppaan "Säädintyyppien ja -tilojen sekä kiintopisteiden lyhenteet" -kappaleesta, joka löytyy Pistekirjoitus-kohdan alta. (#7188, #3975)
* eSpeak NG on päivitetty versioksi 1.49.1 (#7280).
* Pistekirjoitusasetukset-valintaikkunan tulostus- ja syöttötaulukkoluettelot lajitellaan nyt aakkosjärjestykseen. (#6113)
* Päivitetty liblouis-pistekääntäjä versioksi 3.2.0. (#6935)
* Oletusarvoinen pistetaulukko on nyt "englanti (yhdenmukaistettu), taso 1". (#6952)
* NVDA näyttää nyt pistenäytöllä oletusarvoisesti vain osan muuttuneista kontekstitiedoista kohdistuksen siirtyessä objektiin. (#217)
 * Ennen tietoja näytettiin mahdollisimman paljon riippumatta siitä, onko ne näytetty aiemmin.
 * Voit palauttaa aiemman toiminnallisuuden muuttamalla Pistekirjoitusasetukset-valintaikkunasta uuden "Kohdistuskontekstin näyttäminen" -asetuksen arvoksi "täytä näyttö aina".

### Bugikorjaukset

* Muokattavien div-elementtien selitteitä ei enää ilmoiteta arvoiksi selaustilassa Google Chromessa. (#7153)
* End-näppäimen painaminen ei enää aiheuta ajonaikaista virhettä selaustilassa oltaessa tyhjässä Microsoft Word -asiakirjassa. (#7009)
* Selaustilaa tuetaan nyt asianmukaisesti Microsoft Edgessä, kun asiakirjalle on annettu document-ARIA-rooli. (#6998)
* Valitseminen tai valinnan peruminen Shift+Endillä rivin loppuun saakka on nyt mahdollista selaustilassa, vaikka kohdistin on rivin viimeisen merkin kohdalla. (#7157)
* Jos valintaikkuna sisältää edistymispalkin, ikkunan teksti päivittyy nyt pistenäytöllä edistymispalkin muuttuessa. Tämä tarkoittaa, että esim. jäljellä olevan ajan lukeminen on nyt mahdollista NVDA:n "Ladataan päivitystä" -valintaikkunassa. (#6862)
* NVDA ilmoittaa nyt valinnan muutokset tietyissä Windows 10:n yhdistelmäruuduissa, kuten Asetukset-sovelluksen Automaattisessa toistossa. (#6337).
* Hyödytöntä tietoa ei enää puhuta Microsoft Outlookissa siirryttäessä kokouksen/tapaamisenluontivalintaikkunoihin. (#7216)
* Äänimerkit toistetaan epäsäännöllisille edistymispalkkivalintaikkunoille (kuten NVDA:n päivitystarkistus), vain, kun edistymispalkit on määritetty ilmaistavaksi äänimerkein. (#6759)
* Solut luetaan taas Microsoft Excel 2003:n ja 2007:n työkirjoissa nuolinäppäimillä liikuttaessa. (#7243)
* Windows 10 Creators-päivityksessä ja uudemmissa varmistetaan, että selaustila otetaan automaattisesti käyttöön luettaessa sähköposteja Sähköposti-sovelluksessa. (#7289)
* Piste 7 poistaa nyt viimeksi syötetyn pistesolun tai -merkin ja piste 8 painaa Enter-näppäintä useimmissa pistekirjoitusnäppäimistöllisissä pistenäytöissä. (#6054)
* NVDA:n puhepalaute on nyt useimmissa tapauksissa tarkempaa (erityisesti Chromessa ja päätesovelluksissa) siirrettäessä kohdistinta muokattavassa tekstissä (esim. nuolinäppäimillä tai askelpalauttimella). (#6424)
* Microsoft Outlook 2016:n allekirjoitusmuokkaimen sisällön lukeminen on nyt mahdollista. (#7253)
* NVDA ei enää aiheuta ajoittain Java Swing -sovellusten kaatumista liikuttaessa niiden sisältämissä taulukoissa. (#6992)
* NVDA ei enää puhu ilmoitusruutuja useita kertoja Windows 10:n Creators-päivityksessä. (#7128)
* NVDA ei enää puhu haettua tekstiä, kun Windows 10:n Käynnistä-valikko suljetaan haun jälkeen painamalla Enteriä. (#7370)
* Otsikoihin siirtyminen pikanavigointia käyttäen on nyt Microsoft Edgessä huomattavasti nopeampaa. (#7343)
* Selaustilassa navigoiminen ei enää ohita Microsoft Edgessä suurta osaa tiettyjen verkkosivujen sisällöstä (esim. sivuilla, joilla käytetään WordPress 2015 -teemaa). (#7143)
* Kiintopisteet lokalisoidaan Microsoft Edgessä asianmukaisesti eri kielille. (#7328)
* Pistenäyttö seuraa nyt asianmukaisesti valintaa valittaessa tekstiä näytön leveyttä enemmän. Jos esim. valitset useita rivejä Shift+Nuoli alas -komennolla, pistenäytöllä näytetään viimeisin valitsemasi rivi. (#5770)
* NVDA ei ilmoita enää Firefoxissa asiaankuulumattomasti "osa" useaan kertaan avattaessa twiitin tietoja twitter.com:issa. (#5741)
* Taulukkonavigointikomennot eivät ole enää käytettävissä asettelutaulukoissa selaustilassa oltaessa, ellei asettelutaulukoiden ilmoittaminen ole käytössä. (#7382)
* Piilotetut taulukon solut ohitetaan nyt Firefoxissa ja Chromessa selaustilan taulukkonavigointikomentoja käytettäessä. (#6652, #5655)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2017.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat täysi tuki äänenvaimennukselle Windows 10:n Creators-päivityksessä; useat selaustilan tekstinvalitsemisongelmien korjaukset, valitse kaikki -komento mukaan lukien; Microsoft Edge -tuen merkittävät parannukset; sekä verkkoselauksen parannukset, kuten nykyisiksi merkittyjen elementtien ilmaiseminen (aria-current-attribuuttia käyttäen).

### Uudet ominaisuudet

* Solun reunojen tiedot on nyt mahdollista selvittää Microsoft Excelissä käyttäen näppäinkomentoa NVDA+F. (#3044)
* NVDA ilmaisee nyt verkkoselaimissa, kun elementti on merkitty nykyiseksi (aria-current-attribuuttia käyttäen). (#6358)
* Automaattista kielen vaihtamista tuetaan nyt Microsoft Edgessä. (#6852)
* Tuki Laskin-sovellukselle Windows 10 Enterprisen LTSB- (Long-Term Servicing Branch) ja Server-versioissa. (#6914)
* Lue nykyinen rivi -komennon suorittaminen kolme kertaa nopeasti peräkkäin tavaa rivin merkkikuvauksia käyttäen. (#6893)
* Uusi kieli: burma.
* Unicode-merkistöstandardin nuoli ylös ja alas- sekä murtolukusymbolit puhutaan nyt asianmukaisesti. (#3805)

### Muutokset

* Yksinkertaisessa tarkastelutilassa jätetään nyt huomiotta entistä enemmän ylimääräisiä objekteja UI Automation -rajapintaa käyttävissä sovelluksissa. (#6948, #6950)

### Bugikorjaukset

* Verkkosivun valikkokohteiden aktivoiminen on nyt mahdollista selaustilassa oltaessa. (#6735)
* Esc-näppäimen painaminen asetusprofiilin "Vahvista poistaminen" -kehotteen ollessa aktiivisena sulkee nyt valintaikkunan. (#6851)
* Korjattu joitakin kaatumisia Mozilla Firefoxissa ja muissa Gecko-sovelluksissa, joissa usean prosessin toiminto on otettu käyttöön. (#6885)
* Taustavärin ilmoittaminen ruuduntarkastelussa on nyt tarkempaa, kun teksti on piirretty läpinäkyvällä taustalla. (#6467) 
* Paranneltu verkkosivujen säädinkuvausten tukea Internet Explorer 11:ssä (erityisesti aria-describedby-attribuutille kehyksissä ja kun useita tunnuksia on saatavilla). (#5784)
* NVDA:n äänenvaimennus toimii Windows 10:n Creators-päivityksessä taas kuten aiemmissa versioissa (ts. vaimennuksen vaihtoehdot "Puhuttaessa ja ääntä toistettaessa", "Aina" sekä "Ei käytössä" ovat kaikki käytettävissä). (#6933)
* Tiettyihin UIA-säätimiin siirtyminen tai niiden ilmoittaminen ei enää epäonnistu NVDA:ta käyttäen, kun niihin ei ole määritetty pikanäppäintä. (#6779)
* Pikanäppäintietoihin ei enää lisätä kahta välilyöntiä tietyissä UIA-säätimissä. (#6790)
* Tietyt HIMS-pistenäyttöjen näppäinyhdistelmät (esim. välilyönti+piste 4) eivät enää lakkaa ajoittain toimimasta. (#3157)
* Korjattu ongelma avattaessa sarjaporttia tietyn muun kuin englanninkielisissä järjestelmissä, mikä aiheutti joissakin tapauksissa sen, ettei pistenäyttöjen kytkeminen onnistunut. (#6845)
* Asetustiedoston vahingoittuminen on epätodennäköisempää Windowsia sammutettaessa. Asetukset kirjoitetaan nyt väliaikaistiedostoon ennen varsinaisen asetustiedoston korvaamista. (#3165)
* Kun lue nykyinen rivi -komento suoritetaan kaksi kertaa nopeasti peräkkäin rivin tavaamiseksi, merkit tavataan nyt asianmukaista kieltä käyttäen. (#6726)
* Riveittäin liikkuminen on nyt jopa kolme kertaa nopeampaa Microsoft Edgessä Windows 10 Creators -päivityksessä. (#6994)
* NVDA ei enää ilmoita "Web Runtime -ryhmä", kun kohdistus siirretään Microsoft Edge -asiakirjoihin Windows 10 Creators -päivityksessä. (#6948)
* Kaikkia SecureCRT:n nykyisiä versioita tuetaan. (#6302)
* Tietyt PDF-asiakirjat (erityisesti tyhjiä ActualText-attribuutteja sisältävät) eivät enää kaada Adobe Acrobat Readeria. (#7021, #7034)
* Vuorovaikutteisia taulukoita (ARIA-ruudukoita) ei enää ohiteta siirryttäessä taulukoihin T:llä ja Shift+T:llä selaustilassa Microsoft Edgessä. (#6977)
* Shift+Homen painaminen selaustilassa peruu nyt odotetusti valinnan rivin alkuun saakka, kun tekstiä on ensin valittu rivin loppua kohti. (#5746)
* Koko tekstin valitseminen selaustilassa valitse kaikki -komennolla (Ctrl+A) ei enää epäonnistu, jos kohdistin ei ole tekstin alussa. (#6909)
* Korjattu muita harvinaisia selaustilassa ilmenneitä tekstinvalitsemisongelmia. (#7131)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2017.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. osien ja tekstipalstojen ilmoittaminen Microsoft Wordissa; tuki kirjojen lukemiselle ja kommentoinnille sekä niissä liikkumiselle Kindle for PC:ssä; sekä paranneltu Microsoft Edgen tuki.

### Uudet ominaisuudet

* Osanvaihdon tyypin ja osan numeron ilmoittaminen on nyt mahdollista Microsoft Wordissa. Toiminto otetaan käyttöön Asiakirjojen muotoilu -valintaikkunan "Ilmoita sivunumerot" -asetuksella. (#5946)
* Tekstipalstojen ilmoittaminen on nyt mahdollista Microsoft Wordissa. Toiminto otetaan käyttöön Asiakirjojen muotoilu -valintaikkunan "Ilmoita sivunumerot" -asetuksella. (#5946)
* WordPadissa tuetaan nyt automaattista kielen vaihtamista. (#6555)
* NVDA:n Etsi-komentoa (NVDA+Ctrl+F) tuetaan nyt selaustilassa Microsoft Edgessä. (#6580)
* Selaustilassa painikkeisiin siirtäviä pikanavigointinäppäimiä (B ja Shift+B) tuetaan nyt Microsoft Edgessä. (#6577)
* Sarake- ja riviotsikot säilytetään Microsoft Excelissä laskentataulukkoa kopioitaessa. (#6628)
* Tuki kirjojen lukemiselle ja niissä liikkumiselle Kindle for PC:n 1.19-versiossa, linkkeihin, alaviitteisiin, grafiikoihin, korostettuun tekstiin sekä käyttäjän huomautuksiin pääsy mukaan lukien. Katso lisätietoja NVDA:n käyttöoppaan Kindle for PC -kappaleesta. (#6247, #6638)
* Selaustilan taulukkonavigointia tuetaan nyt Microsoft Edgessä. (#6594)
* Tarkastelukohdistimen sijainnin ilmoittava komento (pöytäkoneissa NVDA+numeroryhmän Delete, kannettavissa NVDA+Delete) ilmoittaa nyt Microsoft Excelissä laskentataulukon nimen ja solun sijainnin. (#6613)
* Lopetusvalintaikkunaan lisätty vaihtoehto uudelleenkäynnistämiselle virheenkorjaus-lokitasolla. (#6689)

### Muutokset

* Pienin sallittu pistekohdistimen vilkkumisnopeus on nyt 200 ms. Mikäli nopeus on aiemmin määritetty tätä pienemmäksi, arvoksi muutetaan uusi pienin sallittu arvo. (#6470)
* Pistekirjoitusasetusten valintaikkunaan on lisätty valintaruutu, jonka avulla on mahdollista ottaa pistekohdistimen vilkkuminen käyttöön tai poistaa se käytöstä. Aiemmin vilkkuminen poistettiin käytöstä määrittämällä arvoksi 0. (#6470)
* eSpeak NG päivitetty (e095f008, 10. tammikuuta 2017). (#6717)
* "Aina"-vaihtoehto ei ole enää käytettävissä NVDA:n äänenvaimennuksen asetuksissa Windows 10 Creators -päivitykseen tehtyjen muutosten vuoksi. Asetus on edelleen käytettävissä Windows 10:n vanhemmissa versioissa. (#6684)
* "Puhuttaessa ja ääntä toistettaessa" -asetus ei voi enää varmistaa, että ääni on vaimennettu kokonaan ennen puhumisen aloittamista, eikä myöskään pitää sen jälkeen vaimennusta käytössä tarpeeksi kauan estääkseen äänenvoimakkuuden nopean vaihtelun. Nämä muutokset eivät vaikuta Windows 10:n vanhempiin versioihin. (#6684)

### Bugikorjaukset

* Korjattu jumiutuminen Microsoft Wordissa liikuttaessa kappaleittain suuressa asiakirjassa selaustilan ollessa käytössä. (#6368)
* Microsoft Wordin taulukoita, jotka on kopioitu Microsoft Excelistä, ei enää käsitellä asettelutaulukoina, jonka vuoksi niitä ei enää ohiteta. (#5927)
* NVDA antaa äänimerkin yritettäessä kirjoittaa Microsoft Excelin suojatussa näkymässä sen sijaan, että puhuisi merkkejä, joita ei todellisuudessa kirjoitettu. (#6570)
* Esc-näppäimen painaminen Microsoft Excelissä ei enää virheellisesti vaihda selaustilaan, ellei käyttäjä ole aiemmin nimenomaisesti vaihtanut selaustilaan näppäinkomennolla NVDA+Välilyönti ja siirtynyt sitten vuorovaikutustilaan painamalla Enteriä lomakekentän kohdalla. (#6569) 
* NVDA ei enää jumiudu Microsoft Excelin laskentataulukoissa, joissa koko rivi tai sarake on yhdistetty. (#6216)
* Rajatun/ylivuotavan tekstin ilmoittaminen Microsoft Excelin soluissa pitäisi olla nyt tarkempaa. (#6472)
* NVDA ilmoittaa nyt, kun valintaruutu on vain luku -tyyppiä. (#6563)
* Kun NVDA:n käynnistinohjelma ei voi toistaa tunnusääntä, näkyviin ei pitäisi enää tulla varoitusikkunaa puuttuvasta äänilaitteesta. (#6289)
* Microsoft Excelin valintanauhan säätimet, jotka eivät ole käytettävissä, ilmoitetaan nyt sellaisina. (#6430)
* NVDA ei enää sano "ruutu" ikkunoita pienennettäessä. (#6671)
* Kirjoitettujen merkkien puhumista tuetaan Universal Windows Platform (UWP) -sovelluksissa (Microsoft Edge mukaan lukien) Windows 10:n Creators -päivityksessä. (#6017)
* Hiiren seuranta toimii nyt kaikilla ruuduilla tietokoneissa, joissa käytetään useita näyttöjä. (#6598)
* NVDA ei muutu enää käyttökelvottomaksi Windows Media Playerin sulkemisen jälkeen kohdistuksen ollessa liukusäätimessä. (#5467)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2016.4

Tämän version merkittävimpiä uusia ominaisuuksia ovat paranneltu Microsoft Edgen tuki; selaustila Windows 10:n Sähköposti-sovelluksessa; sekä NVDA:n valintaikkunoiden merkittävät parannukset.

### Uudet ominaisuudet

* NVDA voi nyt ilmaista rivien sisennykset äänimerkeillä. Asetus on mahdollista määrittää Ilmoita rivien sisennykset -yhdistelmäruudusta Asiakirjojen muotoiluasetukset -valintaikkunasta. (#5906)
* Tuki Orbit Reader 20 -pistenäytölle. (#6007)
* Lisätty asetus puheentarkasteluikkunan avaamiseen NVDA:n käynnistyessä. Se voidaan ottaa käyttöön puheentarkasteluikkunassa olevalla valintaruudulla. (#5050)
* Kun puheentarkasteluikkuna avataan uudelleen, sen sijainti ja mitat palautetaan. (#5050)
* Microsoft Wordin ristiviittauskentät käsitellään nyt hyperlinkkeinä. Kentät ilmoitetaan linkkeinä, ja ne on mahdollista avata. (#6102)
* Tuki Baum SuperVario2-, Baum Vario 340- ja HumanWare Brailliant2 -pistenäytöille. (#6116)
* Alustava tuki Microsoft Edgen Anniversary-päivitykselle. (#6271)
* Selaustilaa käytetään nyt viestien lukemiseen Windows 10:n sähköpostisovelluksessa. (#6271)
* Uusi kieli: liettua.

### Muutokset

* Liblouis-pistekääntäjä päivitetty versioksi 3.0.0, joka sisältää merkittäviä laajennuksia yhdenmukaistettuun englantilaiseen pistekirjoitusmerkistöön (UEB). (#6109, #4194, #6220, #6140)
* Lisäosien hallinnan Poista käytöstä- ja Ota käyttöön -painikkeilla on nyt pikanäppäimet (Alt+P ja Alt+O). (#6388)
* Useita NVDA:n valintaikkunoiden täyte- ja tasausongelmia on ratkaistu. (#6317, #5548, #6342, #6343, #6349)
* Asiakirjojen muotoiluasetukset -valintaikkunaa on muutettu siten, että sen sisältöä on mahdollista vierittää. (#6348)
* Symbolien puhuminen -valintaikkunan ulkoasua on muutettu siten, että sen koko leveyttä käytetään symboliluettelolle. (#6101)
* Selaustilan pikanavigointikomentoja E ja Shift+E (muokkauskentät) sekä F ja Shift+F (lomakekentät) voidaan nyt käyttää verkkoselaimissa vain luku -tyyppisiin muokkauskenttiin siirtymiseen. (#4164)
* NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunan "Lue kohdistimen jälkeiset muotoilumuutokset" -asetus on nimetty uudelleen muotoon "Ilmoita kohdistimen jälkeiset muotoilumuutokset", sillä se vaikuttaa puheen lisäksi myös pistekirjoitukseen. (#6336)
* NVDA:n Tervetuloa-valintaikkunan ulkoasua on korjattu. (#6350)
* NVDA:n valintaikkunoiden  OK- ja Peruuta-painikkeet tasataan nyt ikkunoiden oikeaan reunaan. (#6333)
* Numeeristen arvojen syöttökentissä, kuten Puheäänen asetukset -valintaikkunan "Äänenkorkeuden muutos prosentteina isoille kirjaimille" -asetuksessa, käytetään nyt kiertosäätimiä. Voit kirjoittaa haluamasi arvon tai käyttää nuoli ylös- ja nuoli alas -näppäimiä sen muuttamiseen. (#6099)
* Sisäiset kehykset (asiakirjoihin upotetut asiakirjat) ilmoitetaan yhdenmukaisemmin eri selaimissa. Firefoxissa ne ilmoitetaan nyt "kehyksinä". (#6047)

### Bugikorjaukset

* Korjattu harvinainen virhe NVDA:ta suljettaessa puheentarkastelun ollessa aktiivisena. (#5050)
* Kuvakartat hahmontuvat nyt odotetusti selaustilassa Mozilla Firefoxissa. (#6051)
* Enter-näppäimen painaminen puhesanastovalintaikkunassa tallentaa nyt tekemäsi muutokset ja sulkee ikkunan. Aiemmin Enterin painaminen ei tehnyt mitään. (#6206)
* Pistenäytöllä näytetään nyt ilmoitus syöttömenetelmän tilaa vaihdettaessa (natiivi syöte/aakkosnumeerinen, kokonaiset/puolikkaat merkit jne.). (#5892, #5893)
* Lisäosan edellinen tila palautetaan asianmukaisesti, kun se poistetaan käytöstä ja otetaan heti uudelleen käyttöön tai päinvastoin. (#6299)
* Ylätunnisteiden sivunumerokentät voidaan nyt lukea Microsoft Wordia käytettäessä. (#6004)
* Hiirtä on nyt mahdollista käyttää kohdistuksen siirtämiseen Symbolien puhuminen -valintaikkunan symboliluettelon ja muokkauskenttien välillä. (#6312)
* Korjattu ongelma, joka esti elementtilistan avautumisen selaustilassa Microsoft Wordissa, jos asiakirja sisälsi virheellisen hyperlinkin. (#5886)
* Kun  puheentarkasteluikkuna on suljettu tehtäväpalkista tai Alt+F4-näppäinyhdistelmällä, NVDA-valikon Puheentarkastelu-valintaruutu vaikuttaa nyt ikkunan näkymiseen. (#6340)
* Lataa liitännäiset uudelleen -komento ei enää aiheuta ongelmia käynnistimillä käyttöön otettavissa profiileissa, uusissa asiakirjoissa verkkoselaimissa tai ruuduntarkastelussa. (#2892, #5380)
* Jotkin kielet, kuten aragonia, näytetään nyt oikein NVDA:n Yleiset asetukset -valintaikkunan kieliluettelossa Windows 10:ssä. (#6259)
* Emuloidut näppäimet (esim. pistenäytön painike, joka emuloi Sarkain-näppäimen painamista) ilmaistaan nyt näppäinohjeessa ja Syöte-eleet-valintaikkunassa NVDA:ssa määritetyllä kielellä. Aiemmin ne näytettiin englanniksi. (#6212)
* Kielen  vaihtamisella (Yleiset asetukset -valintaikkunasta) ei ole nyt vaikutusta ennen kuin NVDA käynnistetään uudelleen. (#4561)
* Uuden puhesanastomäärityksen "Korvattava teksti" -kenttää ei ole enää mahdollista jättää tyhjäksi. (#6412)
* Korjattu harvinainen ongelma, jossa sarjaporttien tutkiminen teki joissakin järjestelmissä pistenäyttöajureista käyttökelvottomia. (#6462)
* Numeroitujen luetteloiden numerot luetaan nyt taulukon soluista Microsoft Wordissa solu kerrallaan liikuttaessa. (#6446)
* Handy Tech -pistenäyttöjen ajurin komentoihin on nyt mahdollista määrittää eleitä Syöte-eleet-valintaikkunassa. (#6461)
* Seuraavaan soluun siirtyminen ilmoitetaan nyt asianmukaisesti Microsoft Excelissä tavallista tai  numeroryhmän Enteriä painettaessa laskentataulukossa liikuttaessa. (#6500)
* iTunes ei jää enää ajoittain loputtomasti jumiin käytettäessä selaustilaa Storessa, Apple Musicissa jne. (#6502)
* Korjattu kaatumisia 64-bittisissä Mozilla- ja Chrome-pohjaisissa sovelluksissa. (#6497)
* Selaustila ja muokattavat tekstikentät toimivat nyt oikein, kun usean prosessin ikkunat on otettu Firefoxissa käyttöön. (#6380)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2016.3

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. yksittäisten lisäosien käytöstä poistaminen, tuki lomakekentille Microsoft Excelissä, huomattavat parannukset värien ilmoittamiseen, useisiin pistenäyttöihin liittyvät korjaukset ja parannukset, sekä korjaukset ja parannukset Microsoft Wordin tukeen.

### Uudet ominaisuudet

* Selaustilaa on nyt mahdollista käyttää PDF-asiakirjojen lukemiseen Microsoft Edgessä Windows 10:n Anniversary-päivityksessä. (#5740)
* Tavallinen ja kaksinkertainen yliviivaus ilmoitetaan nyt Microsoft Wordissa. (#5800)
* Jos taulukolla on otsikko, se luetaan nyt Microsoft Wordissa. Mikäli kuvaus on lisätty, se voidaan lukea selaustilassa avaa pitkä kuvaus -komennolla (NVDA+D). (#5943)
* NVDA ilmoittaa nyt Microsoft Wordissa sijaintitiedot kappaleita siirrettäessä (Alt+Shift+nuoli alas ja Alt+Shift+nuoli ylös). (#5945)
* Jos Ilmoita rivivälit -asetus on otettu käyttöön NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunasta, riviväli ilmoitetaan nyt Microsoft Wordissa NVDA:n muotoilutietojen lukukomennolla, Wordin pikanäppäimillä muutettaessa sekä siirryttäessä sellaisen tekstin kohdalle, jonka riviväli eroaa aiemmasta. (#2961)
* HTML5:n rakenteelliset elementit tunnistetaan nyt Internet Explorerissa. (#5591)
* Kommenttien lukeminen (esim. Microsoft Wordissa) voidaan nyt poistaa käytöstä NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunan Lue kommentit -asetusta käyttäen. (#5108)
* Yksittäisten lisäosien käytöstä poistaminen on nyt mahdollista lisäosien hallinnassa. (#3090)
* ALVA BC640/680 -pistenäytöille on lisätty näppäinmäärityksiä. (#5206)
* Pistenäytttö on nyt mahdollista siirtää nykyiseen kohdistukseen. Komennolle on määritelty näppäin Tällä hetkellä vain ALVA BC640/680 -pistenäytöille, mutta se on mahdollista määrittää tarvittaessa muillekin Syöte-eleet-valintaikkunassa. (#5250)
* Microsoft Excelissä on nyt mahdollista olla vuorovaikutuksessa lomakekenttien kanssa. Kenttiin siirrytään elementtilistaa tai selaustilassa navigointinäppäimiä käyttäen. (#4953)
* Yksinkertaiselle tarkastelutilalle voidaan nyt määrittää syöte-ele Syöte-eleet-valintaikkunaa käyttäen. (#6173)

### Muutokset

* NVDA ilmoittaa nyt värit käyttäen paremmin ymmärrettävää 9 sävyn ja 3 voimakkuuden perussarjaa kirkkaus- ja haaleusmuunnelmineen. Aiemmin käytettiin subjektiivisempia ja vähemmän ymmärrettäviä värien nimiä. (#6029)
* NVDA+F9- ja NVDA+F10-toiminnallisuus on muutettu valitsemaan tekstiä ensimmäisellä F10:n painalluksella. Kun F10:tä painetaan kahdesti (nopeasti peräkkäin), teksti kopioidaan leikepöydälle. (#4636)
* eSpeak NG päivitetty versioksi Master 11b1a7b (22. kesäkuuta 2016). (#6037)

### Bugikorjaukset

* Leikepöydälle kopioiminen selaustilassa Microsoft Wordissa säilyttää nyt muotoilun. (#5956)
* NVDA ilmoittaa nyt asianmukaisesti Microsoft Wordissa sen omia  taulukkonavigointikomentoja (Alt+Home, Alt+End, Alt+Page up ja Alt+Page down) sekä taulukonvalitsemiskomentoja (Shift lisättynä navigointikomentoihin) käytettäessä. (#5961)
* NVDA:n objektinavigointia on paranneltu huomattavasti Microsoft Wordin valintaikkunoissa. (#6036)
* Pikanäppäimet (esim. Ctrl+C kopiointia varten) ilmoitetaan nyt odotetusti joissakin sovelluksissa, kuten esim. Visual Studio 2015. (#6021)
* Korjattu muutamissa järjestelmissä sarjaportteja etsittäessä ilmennyt harvinainen ongelma, joka teki joistakin pistenäyttöajureista käyttökelvottomia. (#6015)
* Värien ilmoittaminen on Microsoft Wordissa tarkempaa, sillä Office-teemojen muutokset otetaan nyt huomioon. (#5997)
* Microsoft Edgen selaustila ja Käynnistä-valikon hakukentän ehdotusten tuki ovat taas käytettävissä Windows 10:n koontiversioissa, jotka on julkaistu huhtikuun 2016 jälkeen. (#5955)
* Automaattinen taulukko-otsikoiden lukeminen toimii paremmin Microsoft Wordissa yhdistettyjä soluja käsiteltäessä. (#5926)
* Viestien sisällön lukeminen onnistuu nyt NVDA:lla Windows 10:n Sähköposti-sovelluksessa. (#5635) 
* Lukitusnäppäimiä, kuten Caps Lock, ei enää ilmoiteta kahdesti komentonäppäinten lukemisen ollessa käytössä. (#5490)
* Käyttäjätilien valvonnan valintaikkunat luetaan taas oikein Windows 10:n Anniversary-päivityksessä. (#5942)
* NVDA ei enää anna äänimerkkejä ja ilmoita mikrofonisyötteeseen liittyviä edistymispalkkien päivityksiä Web Conference -lisäosassa (käytetään esim. out-of-sight.netissä). (#5888)
* Etsi seuraava- tai Etsi edellinen -komennon suorittaminen selaustilassa suorittaa nyt asianmukaisesti kirjainkoon huomioivan haun, mikäli alkuperäinen haku oli sellainen. (#5522)
* Virheellisistä sääntölausekkeista annetaan nyt palautetta sanastomäärityksiä muokattaessa. NVDA ei enää kaadu, mikäli sanastotiedosto sisältää virheellisen sääntölausekkeen. (#4834)
* Mikäli NVDA ei pysty kommunikoimaan pistenäytön kanssa (esim. koska se on irrotettu), näyttö poistetaan automaattisesti käytöstä. (#1555)
* Selaustilan elementtilistan suodattamisen suorituskykyä paranneltu hieman joissakin tilanteissa. (#6126)
* NVDA:n Microsoft Excelissä ilmoittamat taustakuvion nimet vastaavat nyt Excelin käyttämiä. (#6092)
* Windows 10:n kirjautumisruudun tukea paranneltu (mukaan lukien ilmoitusten lukeminen ja salasanakentän aktivoiminen kosketusnäytöllä). (#6010)
* NVDA tunnistaa nyt asianmukaisesti ALVA BC640/680 -pistenäyttöjen toissijaiset kosketuskohdistinnäppäimet. (#5206)
* NVDA lukee taas ilmoitusruudut uusimmissa Windows 10:n koontiversioissa. (#6096)
* NVDA ei lakkaa enää ajoittain tunnistamasta Baum-yhteensopivien ja HumanWaren Brailliant B -pistenäyttöjen näppäinpainalluksia. (#6035)
* Rivinumerot näytetään nyt pistenäytöllä, mikäli niiden ilmoittaminen on otettu käyttöön NVDA:N asiakirjojen muotoiluasetuksista. (#5941)
* Objektien ilmoittaminen (kuten kohdistuksen NVDA+Sarkain -näppäinyhdistelmää painettaessa) näkyy nyt odotetusti puheentarkastelussa, kun puhetilana on "ei puhetta". (#6049)
* Luonnostietoja ei enää lueta Outlook 2016:n viestiluettelossa. (#6219)
* Korjattu ongelma, jossa selaustila ei toiminut useissa asiakirjoissa muun kuin englanninkielisessä Google Chromessa ja Chrome-pohjaisissa selaimissa. (#6249)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2016.2.1

Tämä versio korjaa Microsoft Wordin kaatumisia:

* NVDA ei enää aiheuta Windows XP:ssä Microsoft Wordin kaatumista heti sen käynnistyttyä. (#6033)
* Poistettu kielioppivirheiden ilmoittaminen, sillä se aiheutti Microsoft Wordin kaatumisia. (#5954, #5877)

## 2016.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat mahdollisuus kirjoitusvirheiden ilmaisemiseen kirjoitettaessa, tuki kielioppivirheiden ilmoittamiselle Microsoft Wordissa sekä korjauksia ja parannuksia Microsoft Office -tukeen.

### Uudet ominaisuudet

* Pikanavigointinäppäimillä selitteisiin siirtyminen (A ja Shift+A) siirtää nyt lisättyyn ja poistettuun tekstiin selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä. (#5691)
* NVDA ilmoittaa nyt Microsoft Excelissä soluryhmän tason ja lisäksi sen, onko ryhmä suljettu vai avattu. (#5690)
* Tekstin muotoilutiedot lukevan komennon (NVDA+F) kahdesti painaminen näyttää tiedot selaustilassa, jotta niitä voidaan tarkastella. (#4908)
* Solun sävytys ja liukuväritäyttö ilmoitetaan nyt Microsoft Excel 2010:ssä ja uudemmissa. Automaattista ilmoittamista säädetään Lue värit -asetuksella NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunasta. (#3683)
* Uusi pistetaulukko: koinee-kreikka. (#5393)
* Lokin tallentaminen on nyt mahdollista lokintarkastelussa pikanäppäimellä Ctrl+S. (#4532)
* Jos kirjoitusvirheiden ilmoittaminen on käytössä ja sitä tuetaan aktiivisessa säätimessä, NVDA toistaa kirjoitettaessa äänen ilmoittaakseen kirjoitusvirheestä. Tämä voidaan poistaa käytöstä uudella "Ilmaise kirjoitusvirheet kirjoitettaessa toistamalla ääni" -asetuksella NVDA:n Näppäimistöasetukset-valintaikkunassa. (#2024)
* Kielioppivirheet ilmoitetaan nyt Microsoft Wordissa. Tämä voidaan poistaa käytöstä NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunan uutta "Ilmoita kielioppivirheet" -asetusta käyttäen. (#5877)

### Muutokset

* NVDA käsittelee selaustilassa ja muokattavissa tekstikentissä laskinnäppäimistön Enteriä samalla tavoin kuin tavallista Enter-näppäintä. (#5385)
* NVDA:n puhesyntetisaattoriksi on vaihdettu eSpeak NG. (#5651)
* NVDA ei jätä enää Microsoft Excelissä huomiotta solun sarakeotsikkoa, kun solun ja otsikon välissä on tyhjä rivi. (#5396)
* Koordinaatit puhutaan Microsoft Excelissä ennen otsikoita epäselvyyksien välttämiseksi otsikoiden ja sisällön välillä. (#5396)

### Bugikorjaukset

* Kun selaustilassa yritetään siirtyä pikanavigointinäppäimillä elementtiin, jota ei tueta nykyisessä asiakirjassa, NVDA ilmoittaa, ettei sitä tueta sen sijaan, että ilmoittaisi, ettei elementtiä ole. (#5691)
* Pelkkiä kaavioita sisältävät laskentataulukot sisällytetään nyt elementtilistaan Microsoft Excelissä, kun näytettävän elementin tyypiksi on valittu laskentataulukot. (#5698)
* NVDA ei enää puhu epäolennaista tietoa vaihdettaessa ikkunaa moni-ikkunaisessa Java-sovelluksessa, kuten IntelliJ:ssä tai Android Studiossa. (#5732)
* Pistekirjoitusta päivitetään nyt oikein Scintilla-pohjaisissa tekstieditoreissa (kuten Notepad++), kun kohdistinta siirretään pistenäyttöä käyttäen. (#5678)
* NVDA ei enää kaadu ajoittain otettaessa käyttöön pistenäyttöä. (#4457)
* Kappaleen sisennys ilmoitetaan Microsoft Wordissa nyt aina käyttäjän valitsemaa mittayksikköä käyttäen (esim. senttimetri tai tuuma). (#5804)
* Useat NVDA:n ilmoitukset, jotka aiemmin pistenäyttöä käytettäessä vain puhuttiin, näytetään nyt myös pistekirjoituksena. (#5557)
* Puunäkymäkohteiden taso ilmoitetaan nyt saavutettavissa Java-sovelluksissa. (#5766)
* Korjattu Adobe Flashin kaatuminen Mozilla Firefoxissa joissakin tilanteissa. (#5367)
* Valintaikkunoiden tai sovellusten sisällä olevia asiakirjoja voidaan nyt lukea selaustilassa Google Chromessa ja Chrome-pohjaisissa selaimissa. (#5818)
* NVDA:n voi nyt pakottaa Google Chromessa ja Chrome-pohjaisissa selaimissa selaustilaan verkkopohjaisissa valintaikkunoissa tai -sovelluksissa oltaessa. (#5818)
* Kohdistuksen siirtäminen tiettyihin säätimiin (erityisesti sellaisiin, joissa käytetään aria-activedescendant-attribuuttia) ei vaihda enää virheellisesti selaustilaan Internet Explorerissa ja muissa MSHTML-säätimissä. Tätä ilmeni esim. Gmailissa siirryttäessä viestiä kirjoitettaessa  osoitekenttien ehdotuksiin. (#5676)
* NVDA ei jää enää jumiin Microsoft Wordissa suurissa taulukoissa taulukon rivi- ja sarakeotsikoiden lukemisen ollessa käytössä. (#5878)
* NVDA ei enää virheellisesti ilmoita Microsoft wordissa jäsennystasolla olevaa tekstiä (ei sisäisellä otsikkotyylillä) otsikoksi. (#5186)
* Säilöelementin loppuun/alkuun siirtävät komennot (pilkku ja Shift+pilkku) toimivat nyt taulukoille selaustilassa Microsoft Wordissa. (#5883)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2016.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat mahdollisuus valinnaiseen muiden äänien voimakkuuden alentamiseen, parannukset pistekirjoituksen näyttämiseen ja pistenäyttötukeen, useat merkittävät korjaukset Microsoft Office -tukeen sekä korjaukset iTunesin selaustilaan.

### Uudet ominaisuudet

* Uusia pistetaulukoita: puolalainen 8 pisteen tietokonemerkistö, mongoli. (#5537, #5574)
* Voit poistaa pistekohdistimen käytöstä ja muuttaa sen muotoa uusia Pistekirjoitusasetukset-valintaikkunan Näytä kohdistin- ja Kohdistimen muoto -asetuksia käyttäen. (#5198)
* NVDA voi nyt yhdistää HIMS Smart Beetle -pistenäyttöön bluetoothin kautta. (#5607)
* NVDA voi valinnaisesti pienentää muiden sovellusten äänenvoimakkuutta, kun se on asennettu Windows 8:aan tai uudempaan käyttöjärjestelmään. Tämä voidaan määrittää Syntetisaattorin asetukset -valintaikkunan Äänenvaimennus -asetusta käyttäen tai painamalla NVDA+Vaihto+D. (#3830, #5575)
* Tuki APH Refreshabraille -pistenäytölle HID-tilassa ja Baum VarioUltralle sekä Pronto!:lle USB:n kautta yhdistettäessä. (#5609)
* Tuki HumanWare Brailliant BI/B -pistenäytöille, kun protokollaksi on määritetty OpenBraille. (#5612)

### Muutokset

* Korostuksen ilmoittaminen ei ole nyt oletusarvoisesti käytössä. (#4920)
* Microsoft Excelissä käytettävän elementtilistan Kaavat-vaihtoehdon pikanäppäimeksi on NVDA:n englanninkielisessä käyttöliittymässä muutettu Alt+R, jotta se ei ole sama kuin Filter-muokkauskentällä. (#5527)
* Liblouis-pistekääntäjä päivitetty versioksi 2.6.5. (#5574)
* Teksti-sanaa ei enää puhuta siirrettäessä kohdistusta tai tarkastelukohdistinta tekstiobjekteihin. (#5452)

### Bugikorjaukset

* Selaustila päivittyy nyt asianmukaisesti iTunes 12:ssa uuden sivun latautuessa iTunes Storessa. (#5191)
* Tiettyihin otsikkotasoihin siirtyminen pikanavigointinäppäimillä toimii nyt odotetusti Internet Explorerissa ja muissa MSHTML-säätimissä, kun otsikon taso ohitetaan saavutettavuustarkoituksessa (erityisesti, kun aria-level ohittaa h-tagin tason). (#5434)
* Kohdistus ei enää siirry säännöllisesti Spotifyssa "tuntemattomiin" objekteihin. (#5439)
* Kohdistus palautetaan nyt asianmukaisesti siirryttäessä toisesta sovelluksesta takaisin Spotifyhin. (#5439)
* Kun selaus- ja vuorovaikutustilojen välillä vaihdetaan, tila ilmoitetaan nyt puheen lisäksi myös pistekirjoituksella. (#5239)
* Tehtäväpalkin Käynnistä-painiketta ei enää ilmoiteta luettelona ja/tai valituksi joissakin Windows-versioissa. (#5178)
* Sellaisia ilmoituksia kuin esim. "lisätty" ei enää puhuta kirjoitettaessa viestejä Microsoft Outlookissa. (#5486)
* Kun pistenäyttöä käytettäessä on tekstiä valittuna nykyisellä rivillä (esim. etsittäessä tekstieditorissa samalla rivillä esiintyvää tekstiä), pistenäyttöä vieritetään, mikäli se on tarpeen. (#5410)
* NVDA ei enää sulkeudu hiljaisesti Windowsin komentokonsolia Alt+F4:llä suljettaessa Windows 10:ssä. (#5343)
* Kun elementtiä muutetaan selaustilan elementtilistassa, Suodata-kenttä tyhjennetään. (#5511)
* Hiiren liikuttaminen lukee odotetusti koko sisällön sijasta jälleen asianmukaisen rivin, sanan jne. Mozilla-sovellusten muokattavissa tekstikentissä. (#5535)
* Lukeminen ei enää pysähdy sanan tai rivin sisällä olevien elementtien, kuten linkkien, kohdalla liikutettaessa hiirtä Mozilla-sovellusten muokattavissa tekstikentissä. (#2160, #5535)
* Shoprite.com-verkkosivua on nyt mahdollista lukea selaustilassa Internet Explorerissa sen sijaan, että sivu ilmoitettaisiin tyhjäksi. (Erityisesti väärin muotoillut lang-attribuutit käsitellään nyt sulavasti.) (#5569)
* Jäljitettäviä muutoksia, kuten lisäyksiä, ei enää ilmoiteta Microsoft Wordissa, kun niiden merkintöjä ei näytetä. (#5566)
* Kun kohdistus on vaihtopainikkeen kohdalla, NVDA ilmoittaa, kun sen tila muuttuu painetusta ei-painetuksi. (#5441)
* Hiiren muodon muutosten ilmoittaminen toimii taas odotetusti. (#5595)
* Sitovat välilyönnit käsitellään nyt tavallisina välilyönteinä rivin sisennystä puhuttaessa. Tämä saattoi aiemmin aiheuttaa sen, että "3 väli" -ilmoituksen asemesta sanottiin jotain sellaista kuin "väli väli väli". (#5610)
* Kun moderni Microsoftin syöttömenetelmän ehdotuslista suljetaan , kohdistus palautetaan asianmukaisesti joko syöttömenetelmään tai kohdeasiakirjaan. (#4145)
* Kun Microsoft Office 2013:n ja uudempien valintanauha on määritetty näyttämään pelkät välilehdet, valintanauhan kohteet luetaan taas odotetusti välilehteä aktivoitaessa. (#5504)
* Korjauksia ja parannuksia kosketusnäyttöeleiden tunnistamiseen ja komentoihin liittämiseen. (#5652)
* Kosketuseleitä, joissa sormea painetaan ja pidetään näytöllä, ei puhuta näppäinohjeessa. (#5652)
* Kommenttilistan näyttäminen Excelin elementtilistassa ei enää epäonnistu, jos kommentti on yhdistetyssä solussa. (#5704)
* Laskentataulukon sisällön lukeminen ei enää epäonnistu hyvin harvoissa tilanteissa, kun rivi- ja sarakeotsikoiden ilmoittaminen on käytössä. (#5705)
* Syöttömenetelmässä liikkuminen toimii nyt odotetusti Google Chromessa Itä-Aasialaisia merkkejä kirjoitettaessa. (#4080)
* Hakutulosten selaustila-asiakirja päivitetään nyt odotetusti etsittäessä Apple Music -palvelusta iTunesissa. (#5659)
* Shift+F11-näppäinyhdistelmän painaminen Microsoft Excelissä uuden laskentataulukon luomiseksi ilmoittaa nyt uuden sijainnin; aiemmin ei ilmoitettu mitään. (#5689)
* Korjattu pistenäyttötulostuksen ongelmia korealaisia merkkejä kirjoitettaessa. (#5640)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2015.4

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. suorituskyvyn parannukset Windows 10:ssä, sisällyttäminen Windows 8:n ja uudempien Helppokäyttökeskukseen, parannukset Microsoft Exceliin (mukaan lukien laskentataulukoiden näyttäminen ja uudelleennimeäminen elementtilistassa) sekä pääsy suojattujen laskentataulukoiden lukittuihin soluihin, ja muotoiluja tukevan tekstin muokkaaminen Mozilla Firefoxissa, Google Chromessa ja Mozilla Thunderbirdissä.

### Uudet ominaisuudet

* NVDA näkyy nyt Windows 8:n ja uudempien Helppokäyttökeskuksessa. (#308)
* Kun soluja siirretään Excelissä, muotoilumuutokset ilmoitetaan nyt automaattisesti, mikäli asianmukaiset asetukset on otettu käyttöön NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunassa. (#4878)
* NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunaan on lisätty Ilmoita korostus -asetus. Tämän asetuksen avulla, joka on oletusarvoisesti käytössä, NVDA ilmoittaa automaattisesti asiakirjojen korostetun tekstin. Tätä tuetaan toistaiseksi vain em- ja strong-tageille selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä. (#4920)
* Lisätty ja poistettu teksti ilmoitetaan nyt selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä, jos NVDA:n Lue muokkaajan merkinnät -asetus on käytössä. (#4920)
* Kun jäljitettäviä muutoksia katsotaan Microsoft Wordissa NVDA:n elementtilistassa, tietoja näytetään nyt enemmän, kuten esim. muutetut muotoilut. (#4920)
* Microsoft Excel: laskentataulukoiden näyttäminen ja uudelleennimeäminen on nyt mahdollista NVDA:n elementtilistasta (NVDA+F7). (#4630, #4414)
* Symbolien puhuminen -valintaikkunassa on nyt mahdollista määrittää, välitetäänkö merkit syntetisaattoreille (esim. tauon pitämiseksi tai äänensävyn muuttamiseksi). (#5234)
* NVDA lukee nyt Microsoft Excelissä laskentataulukon tekijän soluihin määrittämät syöttöilmoitukset. (#5051)
* Tuki Baum Pronto! V4- ja VarioUltra -pistenäytöille bluetoothin kautta kytkettäessä. (#3717)
* Tuki muotoilut mahdollistavan tekstin muokkaamiselle Mozilla-sovelluksissa, kuten Firefoxissa Google Docsille pistenäyttötuen ollessa käytössä sekä Thunderbirdissä HTML-viestien luomiselle. (#1668)
* Tuki muotoilut mahdollistavan tekstin muokkaamiselle Google Chromessa ja muissa Chrome-pohjaisissa selaimissa esim. Google Docsia käytettäessä pistenäyttötuen ollessa käytössä. (#2634)
 * Tämä edellyttää Chromen versiota 47 tai uudempaa.
* Microsoft Excelissä on nyt mahdollista siirtyä selaustilassa suojattujen laskentataulukoiden lukittuihin soluihin. (#4952)

### Muutokset

* NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunan Lue muokkaajan merkinnät -asetus on nyt oletusarvoisesti käytössä. (#4920)
* Kun Microsoft Wordissa liikutaan merkki kerrallaan NVDA:n Lue muokkaajan merkinnät -asetuksen ollessa käytössä, tietoja luetaan nyt vähemmän muutoksia jäljitettäessä, mikä tekee tekstissä liikkumisesta sujuvampaa. Käytä elementtilistaa lisätietojen näyttämiseen. (#4920)
* Liblouis-pistekääntäjä päivitetty versioksi 2.6.4. (#5341)

* Useat symbolit (matemaattiset perusmerkit mukaan lukien) on siirretty jotain-tasolle, jotta ne puhutaan oletusarvoisesti. (#3799)
* Puheessa pitäisi nyt kuulua tauko alku- ja loppusulkujen sekä lyhyen ajatusviivan (–) kohdalla, mikäli syntetisaattori tukee tätä ominaisuutta. (#3799)
* Valittua tekstiä ei enää lueta valinnan ilmaisemisen jälkeen, vaan sitä ennen. (#1707)

### Bugikorjaukset

* Suorituskykyä paranneltu merkittävästi Outlook 2010:n/2013:n viestiluettelossa liikuttaessa. (#5268)
* Tietyillä näppäimillä liikkuminen (kuten laskentataulukon vaihtaminen Ctrl+Page up- ja Ctrl+Page down -näppäimillä) toimii nyt oikein Microsoft Excel -kaavioissa. (#5336)
* Korjattu painikkeiden visuaalinen ulkoasu varoitusvalintaikkunassa, joka näytetään yritettäessä päivittää NVDA:ta alaspäin. (#5325)
* Kun NVDA on määritetty käynnistymään Windowsiin kirjautumisen jälkeen, se käynnistyy nyt paljon aiemmin Windows 8:ssa ja uudemmissa. (#308)
 * Jos olet ottanut tämän asetuksen käyttöön aiemmassa NVDA:n versiossa, sinun on poistettava se käytöstä ja otettava sitten uudelleen käyttöön Yleiset asetukset -valintaikkunassa, jotta muutos tulee voimaan. Tee seuraavasti:
  1. Avaa Yleiset asetukset -valintaikkuna.
  1. Poista valinta Käynnistä automaattisesti sisäänkirjautumisen jälkeen -valintaruudusta.
  1. Paina OK-painiketta.
  1. Avaa Yleiset asetukset -valintaikkuna uudestaan.
  1. Valitse Käynnistä automaattisesti sisäänkirjautumisen jälkeen -valintaruutu.
  1. Paina OK-painiketta.
* UI Automation -rajapinnan suorituskykyä paranneltu mm. Resurssienhallinnassa ja Tehtävienhallinnassa. (#5293)
* NVDA siirtyy nyt asianmukaisesti vuorovaikutustilaan liikuttaessa selaustilassa Sarkain-näppäimellä vain luku -tyyppisten ARIA-ruudukkosäädinten kohdalle Mozilla Firefoxissa ja muissa Gecko-pohjaisissa sovelluksissa. (#5118)
* NVDA ilmoittaa nyt asianmukaisesti "ei edellistä" virheellisen "ei seuraavaa" sijaan, kun objekteja ei ole enempää pyyhkäistäessä vasemmalle kosketusnäytöllä.
* Korjattu ongelmia, joita ilmeni kirjoitettaessa useita sanoja Syöte-eleet-valintaikkunan Suodata-muokkauskenttään. (#5426)
* NVDA ei jää enää jumiin joissakin tilanteissa yhdistettäessä uudelleen HumanWare Brailliant BI/B -pistenäyttöä USB:n kautta. (#5406)
* Merkkikuvaukset toimivat nyt odotetusti latinalaisille suuraakkosille kielissä, joissa käytetään yhdistelmämerkkejä. (#5375)
* NVDA:n ei pitäisi enää jäädä välillä jumiin Windows 10:n Käynnistä-valikkoa avattaessa. (#5417)
* Ilmoitukset, jotka näytetään ennen edellisen ilmoituksen häviämistä, luetaan nyt Skypen työpöytäversiossa. (#4841)
* Ilmoitukset luetaan nyt asianmukaisesti Skype 7.12:n työpöytäversiossa ja uudemmissa. (#5405)
* NVDA ilmoittaa nyt kohdistuksen asianmukaisesti pikavalikosta poistuttaessa joissakin sovelluksissa, kuten Jartessa. (#5302)
* Väri ilmoitetaan jälleen Windows 7:ssä ja uudemmissa tietyissä sovelluksissa, kuten WordPadissa. (#5352)
* Enterin painaminen  Microsoft PowerPointissa diaesitystä muokattaessa lukee nyt automaattisen tekstin, kuten luettelomerkin tai numeron. (#5360)

## 2015.3

Tämän version merkittävimpiä uusia ominaisuuksia ovat alustava tuki Windows 10:lle; mahdollisuus pikanavigointinäppäimien käytöstä poistamiseen (hyödyllistä joissakin verkkopohjaisissa sovelluksissa); parannuksia Internet Exploreriin sekä korjauksia ongelmaan, joka aiheutti sekaisin menevää tekstiä kirjoitettaessa joissakin sovelluksissa pistenäyttöä käytettäessä.

### Uudet ominaisuudet

* Kirjoitusvirheet ilmoitetaan muokkauskentissä Internet Explorerissa ja muissa MSHTML-säätimissä. (#4174)
* Entistä useampia matemaattisia unicode-symboleita puhutaan nyt niiden esiintyessä tekstissä. (#3805)
* Windows 10:n aloitusnäytön Hakuehdotukset luetaan automaattisesti. (#5049)
* Tuki EcoBraille 20-, 40-, 80- ja Plus -pistenäytöille. (#4078)
* Voit nyt ottaa pikanavigointinäppäimet käyttöön tai poistaa ne käytöstä selaustilassa painamalla NVDA+Shift+välilyönti. Kun pikanavigointinäppäimet eivät ole käytössä, kirjainnäppäinten painallukset välitetään suoraan sovellukselle, josta on hyötyä joissakin verkkopohjaisissa sovelluksissa, kuten Gmailissa, Twitterissä ja Facebookissa. (#3203)
* Uusia pistetaulukoita: suomi (6 pistettä), iiri (tasot 1 ja 2), korea (tasot 1 ja 2 (2006)). (#5137, #5074, #5097)
* Papenmeier BRAILLEX Live Plus -pistenäytön QWERTY-näppäimistö on nyt tuettu. (#5181)
* Kokeellinen tuki Windows 10:n Microsoft Edge -verkkoselaimelle ja selainmoottorille. (#5212)
* Uusi kieli: kannada.

### Muutokset

* Liblouis-pistekääntäjä päivitetty versioksi 2.6.3. (#5137)
* Kun nykyistä vanhempaa NVDA:n versiota yritetään asentaa, tästä varoitetaan nyt, ettei se ole suositeltavaa ja että NVDA tulisi poistaa ensin kokonaan ennen jatkamista. (#5037)

### Bugikorjaukset

* Lomakekenttiin siirtyminen pikanavigoinnilla selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä ei enää siirrä virheellisesti esitystarkoituksiin käytettäviin luettelokohteisiin. (#4204)
* NVDA ei virheellisesti enää lue Firefoxissa ARIA-välilehtipaneelin sisältöä, kun kohdistus siirtyy sen sisään. (#4638)
* Sarkaimella siirtyminen osiin, artikkeleihin tai valintaikkunoihin Internet Explorerissa ja muissa MSHTML-säätimissä ei enää virheellisesti lue kaikkea säilön sisältöä. (#5021, #5025)
* Pistekirjoituksen syöttö ei lakkaa enää toimimasta sellaisia Baum/HumanWare/APH-pistenäyttöjä käytettäessä, joissa on pistekirjoitusnäppäimistö, kun jotain muuta näytön näppäintä on painettu. (#3541)
* Windows 10:ssä ei enää puhuta epäolennaista tietoa liikuttaessa sovellusten välillä Alt+sarkain- tai Alt+Shift+sarkain -näppäinkomennoilla. (#5116)
* Kirjoitettu teksti ei mene enää sekaisin pistenäyttöä käytettäessä tietyissä sovelluksissa, kuten Microsoft Outlookissa. (#2953)
* Asianmukainen sisältö luetaan nyt Internet Explorerissa ja muissa MSHTML-säätimissä, kun elementti tulee näkyviin tai muuttuu, ja kohdistus siirretään heti sen kohdalle. (#5040)
* Pikanavigointinäppäimillä liikkuminen selaustilassa Microsoft Wordissa päivittää nyt odotetusti pistenäyttöä ja tarkastelukohdistinta. (#4968)
* Pistenäytöllä ei enää näytetä ylimääräisiä välilyöntejä säädin- ja muotoiluilmaisimien välissä tai niiden jälkeen. (#5043)
* Kun siirryt pois hitaasti vastaavasta sovelluksesta, NVDA reagoi nyt useimmiten muissa sovelluksissa paljon nopeammin. (#3831)
* Windows 10:n ilmoitusruudut luetaan nyt odotetusti. (#5136)
* Arvo luetaan nyt sen muuttuessa sellaisissa UI Automation -yhdistelmäruuduissa, joissa sitä ei aiemmin luettu.
* Sarkaimella siirtyminen toimii nyt odotetusti selaustilassa verkkoselaimissa, kun on siirrytty samalla tavalla kehysasiakirjaan. (#5227)
* Windows 10:n lukitusnäytön hylkääminen on nyt mahdollista kosketusnäyttöä käyttäen. (#5220)
* Teksti ei enää mene sekaisin pistenäyttöä käytettäessä Windows 7:ssä ja uudemmissa kirjoitettaessa tietyissä sovelluksissa, kuten WordPadissa ja Skypessä. (#4291)
* Leikepöydän sisällön lukeminen, käynnissä olevien sovellusten selvittäminen tarkastelukohdistimen avulla, NVDA:n asetusten muuttaminen jne ei enää ole mahdollista Windows 10:n lukitusnäytössä. (#5269)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2015.2

Tämän version keskeisimpiä ominaisuuksia ovat mm. kaavioiden lukeminen Microsoft Excelissä sekä tuki matemaattisen sisällön lukemiselle ja vuorovaikutteiselle liikkumiselle.

### Uudet ominaisuudet

* Eteen- ja taaksepäin siirtyminen virkkeittäin on nyt mahdollista Microsoft Wordissa ja Outlookissa näppäinkomennoilla Alt+Nuoli alas ja Alt+Nuoli ylös. (#3288)
* Uusia pistetaulukoita useille intialaisille kielille. (#4778)
* NVDA ilmoittaa Microsoft Excelissä, kun solussa on ylivuotavaa tai rajattua sisältöä. (#3040)
* Elementtilistaa (NVDA+F7) voidaan nyt käyttää Microsoft Excelissä kaavioiden, kommenttien ja kaavojen näyttämiseen. (#1987)
* Tuki kaavioiden lukemiselle Microsoft Excelissä. Tätä käytetään valitsemalla ensin kaava elementtilistasta (NVDA+F7) ja käyttämällä sitten nuolinäppäimiä arvopisteiden välillä liikkumiseen. (#1987)
* NVDA:lla on nyt mahdollista lukea matemaattista sisältöä ja liikkua siinä vuorovaikutteisesti verkkoselaimissa sekä Microsoft Wordissa ja PowerPointissa Design Sciencen MathPlayer 4:ää käyttäen. Katso lisätietoja käyttöoppaan "Matemaattisen sisällön lukeminen" -kappaleesta. (#4673)
* Kaikille NVDA:n asetusvalintaikkunoille ja asiakirjaen muotoiluasetuksille on nyt mahdollista määrittää syöte-eleitä (näppäinkomentoja, kosketuseleitä jne) Syöte-eleet-valintaikkunaa käyttäen. (#4898)

== Muutokset ==
* Asiakirjojen muotoiluasetukset -valintaikkunan Ilmoita luettelot-, Lue linkit-, Lue rivinumerot- ja Lue fontti -valintaruutujen näppäinkomentoja on muutettu NVDA:n englanninkielisessä käyttöliittymässä. (#4650)
* NVDA:n Hiiriasetukset-valintaikkunan Ilmaise hiiren koordinaatit äänimerkeillä- ja Äänikoordinaattien voimakkuutta säädetään ruudun kirkkauden mukaan -asetuksille on lisätty näppäinkomennot. (#4916)
* Värien nimien lukemista paranneltu merkittävästi. (#4984)
* Liblouis-pistekääntäjä päivitetty versioksi 2.6.2. (#4777)

== Bugikorjaukset ==
* Merkkien kuvaukset käsitellään nyt asianmukaisesti tiettyjen intialaisten kielten yhdistelmämerkeille. (#4582)
* Jos "Käytä puheäänen kieltä merkkejä ja symboleita käsiteltäessä" -asetus on käytössä, Välimerkkien ja symbolien puhuminen -valintaikkunassa käytetään nyt asianmukaisesti puheäänen kieltä. Lisäksi valintaikkunan otsikossa näytetään kieli, jonka merkkien puhumista muokataan. (#4930)
* Kirjoitettuja merkkejä ei enää virheellisesti puhuta muokattavissa yhdistelmäruuduissa, kuten Googlen kotisivulla olevassa hakukentässä Internet Explorerissa ja muissa MSHTML-säätimissä. (#4976)
* Värien nimet luetaan Microsoft Office -sovelluksissa värejä valittaessa. (#3045)
* Tanskalaisen pistekirjoituksen näyttäminen toimii taas. (#4986)
* Page up- ja Page down -näppäimiä voidaan taas käyttää diojen vaihtamiseen PowerPoint-diaesityksessä. (#4850)
* Kirjoitusilmoitukset luetaan nyt Skypen työpöytäversio 7.2:ssa ja uudemmissa, ja ongelmat, joita esiintyi välittömästi siirrettäessä kohdistusta pois keskustelusta, on korjattu. (#4972)
* Korjattu ongelmia tiettyjä välimerkkejä/symboleita (kuten  hakasulkuja) kirjoitettaessa  Syöte-eleet-valintaikkunan suodatuskenttään. (#5060)
* G:n tai Vaihto+G:n painaminen Internet Explorerissa ja muissa MSHTML-säätimissä grafiikoihin siirtymiseksi ottaa nyt huomioon myös saavutettavuustarkoituksessa kuviksi nimetyt elementit (esim. ARIA-roolin img). (#5062)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2015.1

Tämän version merkittävimpiä uusia ominaisuuksia ovat mm. selaustila Microsoft Word -asiakirjoille ja Outlookin HTML-viesteille, huomattavat parannukset Skypen työpöytäversion tukeen sekä merkittävät Internet Explorerin käyttöön vaikuttavat korjaukset.

### Uudet ominaisuudet

* Uusia symboleita on nyt mahdollista lisätä Symbolien puhuminen -valintaikkunassa. (#4354)
* Syöte-eleet-valintaikkunassa on nyt uusi Suodata-kenttä, jonka avulla on mahdollista näyttää vain tiettyjä sanoja sisältävät eleet. (#4458)
* NVDA lukee nyt automaattisesti uuden tekstin mintty-komentotulkissa. (#4588)
* Selaustilan Etsi-valintaikkunassa on nyt asetus, joka mahdollistaa kirjainkoon huomioivan haun suorittamisen. (#4584)
* Pikanavigointi (esim. H otsikoihin siirtymiseen jne.) sekä elementtilista (NVDA+F7) ovat nyt käytettävissä Microsoft Word -asiakirjoissa selaustilassa, joka voidaan ottaa käyttöön näppäinkomennolla NVDA+Väli. (#2975)
* HTML-viestien lukemista on paranneltu huomattavasti Microsoft Outlook 2007:ssä ja uudemmissa, sillä selaustila otetaan nyt automaattisesti käyttöön tällaisia viestejä luettaessa. Mikäli selaustilaa ei oteta käyttöön joissakin harvoissa tapauksissa, voit pakottaa sen käyttöön näppäinkomennolla NVDA+välilyönti. (#2975) 
* Riviotsikot luetaan nyt automaattisesti Microsoft wordissa sellaisissa taulukoissa, joiden otsikkosolun tekijä on nimenomaisesti määritellyt taulukon ominaisuuksissa. (#4510) 
 * Tämä ei kuitenkaan toimi yhdistettyjä soluja sisältävissä taulukoissa. Tällaisissa tapauksissa voit silti määrittää sarakeotsikot manuaalisesti näppäinkomennolla NVDA+Shift+C.
* Ilmoitukset luetaan nyt Skypen työpöytäversiossa. (#4741)
* Uusimpien viestien lukeminen ja tarkastelukohdistimen siirtäminen niihin on nyt mahdollista Skypen työpöytäversiossa näppäinkomentoja NVDA+Ctrl+1 - NVDA+Ctrl+0 käyttäen (esim. NVDA+Ctrl+1 uusimman ja NVDA+Ctrl+0 kymmenenneksi uusimman viestin lukemiseen). (#3210)
* NVDA ilmoittaa Skypen työpöytäversiossa, kun kontakti kirjoittaa keskustelussa oltaessa. (#3506)
* NVDA:n hiljainen asennus on nyt mahdollista suorittaa komentoriviltä ilman, että asennettu kopio käynnistetään asennuksen jälkeen. Tämä tehdään --install-silent-parametria käyttäen. (#4206)
* Tuki Papenmeierin BRAILLEX Live 20-, BRAILLEX Live- ja BRAILLEX Live Plus -pistenäytöille. (#4614)

### Muutokset

* Asiakirjojen muotoiluasetukset -valintaikkunassa olevalla kirjoitusvirheiden lukemisen käyttöönottavalla asetuksella on nyt pikanäppäin (Alt+R), kun NVDA:ta käytetään englanninkielisenä. (#793)
* NVDA käyttää nyt syntetisaattorin/puheäänen kieltä merkkien ja symbolien käsittelyyn (välimerkkien nimet mukaan lukien) riippumatta siitä, onko automaattinen kielen vaihtaminen käytössä vai ei. Jotta NVDA käyttäisi taas käyttöliittymänsä kieltä, poista käytöstä uusi Puheäänen asetukset -valintaikkunan Käytä puheäänen kieltä merkkejä ja symboleita käsiteltäessä -asetus. (#4210)
* Newfon-syntetisaattorin tuki on poistettu. Newfon on nyt saatavilla NVDA:n lisäosana. (#3184)
* Skypen käyttämiseen NVDA:n kanssa tarvitaan nyt Skypen työpöytäversio 7.0 tai uudempi; aiempia versioita ei tueta. (#4218)
* NVDA:n päivitysten lataaminen on nyt turvallisempaa. (päivityksen tiedot haetaan HTTPS-protokollalla ja tiedoston tarkistussumma tarkistetaan latauksen jälkeen.) (#4716)
* eSpeak on päivitetty versioksi 1.48.04. (#4325)

### Bugikorjaukset

* Yhdistetyt rivi- ja sarakeotsikkosolut käsitellään nyt oikein Microsoft Excelissä. Esim. jos A1 ja B1 yhdistetään, solut A1 ja B1 luetaan solun B2 sarakeotsikkona. Aiemmin tällaisissa tapauksissa ei luettu mitään. (#4617)
* Kun Microsoft PowerPoint 2003:ssa muokataan tekstikentän sisältöä, NVDA lukee nyt oikein joka rivin sisällön. Aiemmin riveiltä jäi pois yksi merkki lisää aina jokaista uutta kappaletta kohti. (#4619)
* Kaikki NVDA:n valintaikkunat ovat nyt näytöllä keskitettyinä, mikä parantaa visuaalista ulkoasua ja käytettävyyttä. (#3148)
* Kun Skypen työpöytäversiossa kontaktia lisättäessä kirjoitetaan esittelyviestiä, kirjoittaminen ja tekstissä liikkuminen toimii nyt oikein. (#3661)
* Jos Eclipse-kehitysympäristön puunäkymissä aiemmin aktiivisena ollut kohde on valintaruutu, sitä ei enää virheellisesti lueta kohdistuksen siirtyessä uuteen kohteeseen. (#4586)
* Seuraava väärin kirjoitettu sana luetaan automaattisesti Microsoft Wordin kieliasun tarkistuksen valintaikkunassa, kun edellistä sanaa muutetaan tai kun se ohitetaan pikanäppäintä käyttäen. (#1938)
* Tekstin lukeminen onnistuu taas moitteettomasti esim. Tera Term Pro:n pääteikkunassa ja Balabolka-asiakirjoissa. (#4229)
* Kun tekstiä muokataan Internet Explorerissa ja muissa MSHTML-asiakirjoissa kehyksessä oltaessa, kohdistus palaa nyt asianmukaisesti muokattavana olevaan asiakirjaan viimeisteltäessä korean ja muiden itäaasialaisten kielten syöttämistä. (#4045)
* Kun Syöte-eleet-valintaikkunassa valitaan lisättävälle näppäineleelle näppäinasettelua, Esc-näppäimen painaminen sulkee nyt odotetusti vain kyseisen valikon koko valintaikkunan sijasta. (#3617)
* Kun lisäosa poistetaan, sen hakemisto poistetaan nyt oikein NVDA:n uudelleenkäynnistyksen jälkeen. Aiemmin NVDA piti käynnistää uudelleen kahdesti. (#3461)
* Korjattu merkittäviä ongelmia käytettäessä Skype 7.0:n työpöytäversiota. (#4218)
* Viestiä ei lueta enää kahdesti, kun se lähetetään Skypen työpöytäversiossa. (#3616)
* NVDA:n ei pitäisi enää satunnaisesti ja virheellisesti lukea Skypen työpöytäversiossa suurta määrää viestejä (ehkä jopa koko keskustelua). (#4644)
* Korjattu ongelma, joka aiheutti sen, että NVDA:n Lue päiväys/aika -komento ei joissakin tapauksissa noudattanut käyttäjän määrittämiä alue- ja kieliasetuksia. (#2987)
* Tarpeetonta, joskus useammalle riville jakaantuvaa tekstiä ei enää näytetä selaustilassa tietyille grafiikoille (esim. Google-ryhmistä löytyville). (Tätä tapahtui erityisesti base64-koodatuille kuville.) (#4793)
* NVDA:n ei pitäisi enää jäädä jumiin muutama sekunti sen jälkeen, kun kohdistus siirretään pois Windows 8:n Metro-sovelluksesta, sillä sen suoritus keskeytetään. (#4572)
* Aktiivisten alueiden aria-atomic-attribuuttia noudatetaan nyt Mozilla Firefoxissa, vaikka itse atomic-elementti muuttuu. Tämä vaikutti aiemmin vain alempiin elementteihin. (#4794) 
* Päivitykset näytetään selaustilassa, ja aktiiviset alueet ilmoitetaan asiakirjaan upotettujen ARIA-sovellusten sisällä olevissa selaustila-asiakirjoissa Internet Explorerissa tai muissa MSHTML-säätimissä. (#4798)
* Kun teksti muuttuu tai sitä lisätään text-relevant -tyyppisiin aktiivisiin alueisiin Internet Explorerissa ja muissa MSHTML-säätimissä, vain muutettu tai lisätty teksti puhutaan säilöelementin kaiken tekstin sijasta. (#4800)
* Internet Explorerissa ja muissa MSHTML-säätimissä aria-labeledby-attribuutilla ilmaistava elementtien sisältö korvaa oikein alkuperäisen sisällön, jos se on tarkoituksenmukaista. (#4575)
* Väärin kirjoitettu sana luetaan nyt Microsoft Outlook 2013:ssa oikeinkirjoitusta tarkistettaessa. (#4848)
* Visibility:hidden-attribuutilla piilotetuissa elementeissä olevaa sisältöä ei enää näytetä asiaankuulumattomasti selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä. #3776)
* Lomakesäätimien title-attribuutti ei enää ole asiaankuulumattomasti etusijalla muihin seliteliitoksiin nähden Internet Explorerissa ja muissa MSHTML-säätimissä. (#4491)
* NVDA ei jätä enää huomiotta kohdistuksen siirtymistä elementteihin aria-activedescendant-attribuutin vuoksi Internet Explorerissa ja muissa MSHTML-säätimissä. (#4667)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2014.4

### Uudet ominaisuudet

* Uusia kieliä: kolumbianespanja, punjabi
* NVDA on nyt mahdollista käynnistää uudelleen normaalisti sekä ilman lisäosia sulkemisvalintaikkunasta. (#4057)
 * Käynnistäminen ilman lisäosia on myös mahdollista --disable-addons-komentorivivalitsinta käyttäen.
* Puhesanastoissa on nyt mahdollista määrittää, että korvattava merkkijono täsmää vain, jos se on kokonainen sana, ts. se ei esiinny pidemmän sanan osana. (#1704)

### Muutokset

* Asiakirjan tarkastelu otetaan automaattisesti käyttöön, jos objekti, johon siirryit objektinavigoinnilla, on selaustila-asiakirjassa mutta objekti, jossa olit aiemmin, ei ollut. Tätä tapahtui aiemmin vain, jos navigointiobjektia siirrettiin kohdistuksen muuttumisen vuoksi. (#4369)
* Pistenäyttö- ja Syntetisaattori-yhdistelmäruutujen sisältö näkyy nyt aakkosjärjestyksessä omissa valintaikkunoissaan Ei pistenäyttöä/Ei puhetta -vaihtoehtoja lukuun ottamatta, jotka ovat alimmaisina. (#2724)
* Liblouis-pistekääntäjä päivitetty versioksi 2.6.0. (#4434, #3835)
* E:n ja Shift+E:n painaminen selaustilassa muokkauskenttiin siirtymiseksi siirtää nyt myös muokattaviin yhdistelmäruutuihin. Tällaisia ovat esim. Google-haun uusimman version hakukenttä. (#4436)
* NVDA-kuvakkeen napsauttaminen vasemmalla hiiren painikkeella tehtäväpalkin ilmoitusalueella avaa nyt NVDA-valikon sen sijaan, ettei tee mitään. (#4459)

### Bugikorjaukset

* Kun kohdistus siirretään takaisin selaustila-asiakirjaan (esim. siirtymällä Alt+sarkain-näppäinyhdistelmällä jo avoimelle verkkosivulle), tarkastelukohdistin sijoitetaan oikein näennäiskohdistimen kohdalle aktiivisen säätimen (esim. lähellä olevan linkin) sijasta. (#4369)
* Tarkastelukohdistin seuraa nyt asianmukaisesti näennäiskohdistinta PowerPoint-diaesityksissä. (#4370)
* Aktiivisen alueen uusi sisältö luetaan Mozilla Firefoxissa ja muissa Gecko-pohjaisissa selaimissa, vaikka sisällöllä on käyttökelpoinen ARIA-live-attribuutti, joka eroaa ylemmän tason aktiivisen alueen attribuutista. Esim. assertive-attribuutilla merkitty sisältö lisätään polite-attribuutilla merkittyyn aktiiviseen alueeseen. (#4169).
* Tapaukset, joissa asiakirjan sisällä on toinen asiakirja, eivät enää estä osan sisällön käyttöä (tarkemmin sanottuna sisäkkäisiä kehyksiä) Internet Explorerissa ja muissa MSHTML-säätimissä. (#4418)
* NVDA ei enää kaadu yritettäessä käyttää joissakin tapauksissa Handy Tech -pistenäyttöä. (#3709)
* Virheellistä "Latauskohtaa ei löydy" -valintaikkunaa ei enää näytetä useissa tapauksissa, kuten käynnistettäessä NVDA:ta työpöydän pikakuvakkeesta tai pikanäppäimellä Windows Vistassa. (#4235)
* Vakavia Eclipsen uusimpien versioiden valintaikkunoissa käytettävien muokattavien tekstisäädinten ongelmia korjattu. (#3872)
* Kohdistimen siirtäminen toimii nyt odotetusti Outlook 2010:n tapaamisten ja kokouspyyntöjen sijaintikentissä. (#4126)
* Sisältö, joka on merkitty aktiivisen alueen sisällä ei-aktiiviseksi (esim. aria-live="off"), ohitetaan nyt asianmukaisesti. (#4405)
* Kun tekstiä luetaan sellaisesta tilarivistä, jolla on nimi, se erotetaan nyt oikein tilarivin tekstin ensimmäisestä sanasta. (#4430)
* Useita tähtiä ei enää lueta turhaan uusien sanojen aluissa salasanojen syöttökentissä kirjoitettujen sanojen lukemisen ollessa käytössä. (#4402)
* Microsoft Outlookin viestiluettelon kohteita ei enää ilmoiteta turhaan tietokohteiksi. (#4439)
* Kun tekstiä valitaan Eclipse-kehitysympäristön koodinmuokkaussäätimessä, Kaikkea valittua tekstiä ei enää lueta joka kerta valinnan muuttuessa. (#2314)
* Eri Eclipse-kehitysympäristön versiot, kuten Spring Tool Suite ja Android Developer Tools -paketin mukana tuleva, tunnistetaan ja käsitellään nyt asianmukaisesti. (#4360, #4454)
* Hiiren seuranta ja kosketuksella tutkiminen on nyt paljon tarkempaa suuren DPI-tarkkuuden näytöillä tai kun asiakirjan zoomaus muuttuu Internet Explorerissa ja muissa MSHTML-säätimissä (useat Windows 8 -sovellukset mukaan lukien). (#3494) 
* Entistä useampien painikkeiden selitteet luetaan nyt Internet Explorerissa ja muissa MSHTML-säätimissä hiiren seurantaa ja kosketuksella tutkimista käytettäessä. (#4173)
* Papenmeier BRAILLEX -pistenäytön näppäimet toimivat nyt odotetusti, kun sitä käytetään BrxComin kanssa. (#4614)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2014.3

### Uudet ominaisuudet

* NVDA:ta käynnistettäessä ja suljettaessa toistettava ääni voidaan poistaa käytöstä uudella Yleiset asetukset -valintaikkunassa olevalla asetuksella. (#834)
* Jos lisäosalle on saatavilla ohje, se voidaan avata Lisäosien hallinnasta. (#2694)
* Tuki Microsoft Outlook 2007:n ja sitä uudempien versioiden kalenterille (#2943) mukaan lukien:
 * Nykyisen ajan ilmoittaminen nuolinäppäimillä liikuttaessa,
 * Ilmoitus, jos valittuna ajankohtana on tapaamisia.
 * Valitun tapaamisen lukeminen sarkainta painettaessa.
 * Päiväyksen älykäs suodatus, jotta se luetaan vain, jos uusi valittuna oleva ajankohta tai tapaaminen on eri päivänä kuin edellinen.
* Paranneltu tuki Outlook 2010:n ja sitä uudempien versioiden Saapuneet- sekä muiden kansioiden viestiluetteloille (#3834) mukaan lukien:
 * Mahdollisuus sarakeotsikoiden (lähettäjä, aihe jne.) hiljentämiseen poistamalla käytöstä Lue taulukon rivi- ja sarakeotsikot -asetuksen asiakirjaen muotoiluasetuksista.
 * Mahdollisuus sarakkeiden välillä liikkumiseen taulukkonavigointikomentoja (Ctrl+Alt+nuolet) käyttäen.
* Microsoft word: Jos kuvalle ei ole lisätty vaihtoehtoista tekstiä, NVDA lukee sen sijaan kuvan nimen, jos asiakirjan tekijä on sen määrittänyt. (#4193)
* Microsoft Word: Kappalesisennykset luetaan Lue muotoilut -komennolla (NVDA+F) sekä automaattisesti, kun uusi Lue kappalesisennykset -asetus on otettu käyttöön Asiakirjojen muotoiluasetukset -valintaikkunasta. (#4165).
* Automaattisesti lisätty teksti, kuten uusi luettelomerkki, numero tai sarkainsisennys, luetaan nyt painettaessa Enteriä muokattavissa asiakirjoissa ja tekstikentissä. (#4185)
* Microsoft Word: Kommentin teksti luetaan painettaessa NVDA+Alt+C, jos kohdistin on sen kohdalla. (#3528)
* Paranneltu tuki sarakkeiden ja rivien otsikoiden automaattiselle lukemiselle Microsoft Excelissä (#3568) mukaan lukien:
 * Tuki Excelin nimetyille alueille JAWS-ruudunlukuohjelman kanssa yhteensopivien otsikkosolujen tunnistamiseksi.
 * Määritä sarakeotsikot (NVDA+Shift+C)- ja Määritä riviotsikot (NVDA+Shift+R) -komennot tallentavat nyt asetuksensa laskentataulukkoon, jotta ne ovat käytettävissä seuraavan kerran taulukkoa avattaessa. Muut nimettyjen alueiden järjestelmää tukevat ruudunlukuohjelmat voivat myös hyödyntää näitä otsikoita.
 * Näitä komentoja voidaan käyttää nyt useita kertoja taulukkoa kohti eri otsikoiden määrittämiseen eri alueille.
* Tuki sarake- ja riviotsikoiden automaattiselle lukemiselle Microsoft Wordissa (#3110) mukaan lukien:
 * Tuki Wordin kirjanmerkeille JAWS-ruudunlukuohjelman kanssa yhteensopivien otsikkosolujen tunnistamiseksi.
 * Määritä sarakeotsikot (NVDA+Shift+C)- ja Määritä riviotsikot (NVDA+Shift+R) -komennot kertovat NVDA:lle taulukon ensimmäisessä otsikkosolussa oltaessa, että kyseiset otsikot luetaan automaattisesti. Asetukset tallennetaan asiakirjaan, jotta ne ovat käytettävissä, kun se avataan seuraavan kerran. Muut kirjanmerkkijärjestelmää tukevat ruudunlukuohjelmat voivat myös hyödyntää näitä otsikoita.
* Microsoft Word: Etäisyys sivun vasemmasta reunasta luetaan sarkain-näppäintä painettaessa. (#1353)
* Microsoft Word: Useimmille käytettävissä oleville muotoilupikanäppäimille (lihavointi, kursivointi, alleviivaus, tasaus ja jäsennystaso) annetaan palautetta sekä puheena että pistekirjoituksella. (#1353)
* Microsoft Excel: Jos valittu solu sisältää kommentteja, ne voidaan lukea nyt painamalla NVDA+Alt+C (#2920)
* Microsoft Excel: Nykyisen solun kommenttien muokkausta varten avataan erityinen valintaikkuna painettaessa Excelin Shift+F2-komentoa kommentin muokkaustilaan siirtymiseksi. (#2920)
* Microsoft Excel: Entistä useammat valinnan siirtämiskomennot antavat palautetta sekä puheena että pistekirjoituksella (#4211) mukaan lukien:
 * Sivun siirtäminen pystysuunnassa (Page up ja Page down)
 * Sivun siirtäminen vaakasuunnassa (Alt+Page up ja Alt+Page down)
 * Valinnan laajentaminen (edellämainitut näppäimet yhdessä Shiftin kanssa).
 * Nykyisen alueen valitseminen (Ctrl+Shift+8)
* Microsoft Excel: Solujen pysty- ja vaakasuuntainen tasaus luetaan nyt muotoilutietojen lukukomennolla (NVDA+F) sekä automaattisesti, jos Asiakirjojen muotoiluasetukset -valintaikkunan Lue tasaus -asetus on käytössä. (#4212)
* Microsoft Excel: Solun tyyli luetaan nyt muotoilutietojen lukukomennolla (NVDA+F) sekä automaattisesti, jos Asiakirjojen muotoiluasetukset -valintaikkunan Lue tyyli -asetus on käytössä. (#4213)
* Microsoft PowerPoint: Muodon nykyinen sijainti luetaan siirrettäessä sitä diassa nuolinäppäimillä (#4214) mukaan lukien:
 * Muodon ja dian jokaisen reunan etäisyys luetaan.
 * Jos muoto peittää tai on toisen muodon peitossa, tällöin luetaan sekä päällekkäisyyden määrä että kyseessä oleva toinen muoto.
 * Nämä tiedot voidaan lukea koska tahansa ilman muodon siirtämistä käyttämällä Lue sijainti -komentoa (NVDA+Delete).
 * Jos muoto on sitä valittaessa toisen muodon peitossa, siitä ilmoitetaan.
* Lue sijainti -komento (NVDA+Delete) on joissakin tapauksissa tilannekohtaisempi. (#4219):
 * Kohdistimen sijainti ilmoitetaan standardinmukaisissa muokkauskentissä ja selaustilassa prosentteina sisällöstä sekä ruudun koordinaatteina.
 * Muodon sijainti luetaan PowerPoint-esityksissä suhteessa diaan sekä muihin muotoihin.
 * Kahdesti painettaessa komento toimii entiseen tapaan lukemalla koko säätimen sijaintitiedot.
* Uusi kieli: katalaani.

### Muutokset

* Liblouis-pistekääntäjä päivitetty versioksi 2.5.4. (#4103)

### Bugikorjaukset

* Tiettyjä tekstiosuuksia, (kuten esim. korostusta sisältäviä) ei enää toisteta Google Chromessa tai muissa Chrome-pohjaisissa selaimissa ilmoituksen tai valintaikkunan tekstiä luettaessa. (#4066)
* Painikkeen tms. aktivoiminen Enteriä painamalla ei enää epäonnistu (eikä väärää säädintä aktivoida) joissakin tapauksissa, kuten esim. Facebookin sivun yläosan painikkeiden kohdalla selaustilassa Mozilla-sovelluksissa. (#4106)
* iTunesissa ei enää lueta tarpeetonta tietoa sarkaimella liikuttaessa. (#4128)
* Seuraavaan kohteeseen siirtyminen objektinavigointia käyttäen toimii nyt oikein tietyissä iTunesin osissa, kuten esim. Musiikki-luettelossa. (#4129)
* WAI ARIA -muotoilujen vuoksi otsikoiksi laskettavat HTML-elementit sisällytetään nyt Internet Explorer -asiakirjoissa selaustilan elementtilistaan sekä pikanavigointiin. (#4140)
* Sivun sisäisten linkkien seuraaminen siirtää nyt kohdesijaintiin sekä lukee sen asianmukaisesti selaustila-asiakirjoissa viimeisimmissä Internet Explorerin versioissa. (#4134)
* Microsoft Outlook 2010 ja uudemmat:  suojattujen valintaikkunoiden, kuten esim. Uusi profiili- ja sähköpostitilin lisäysvalintaikkunoiden yleistä käytettävyyttä paranneltu. (#4090, #4091, #4095)
* Microsoft Outlook: komentotyökalurivien tarpeetonta puheliaisuutta vähennetty tietyissä valintaikkunoissa liikuttaessa. (#4096, #3407)
* Microsoft word: taulukosta poistumista ei enää ilmoiteta virheellisesti siirryttäessä sarkaimella taulukon tyhjään soluun. (#4151)
* Microsoft Word: Ensimmäisen taulukon jälkeisen merkin (tyhjä rivi mukaan lukien) ei enää virheellisesti katsota olevan taulukon sisällä. (#4152)
* Microsoft Word 2010:n kieliasun tarkistuksen valintaikkuna: Todellinen väärin kirjoitettu sana luetaan nyt asianmukaisesti ensimmäisen lihavoidun sanan asemesta. (#3431) 
* Kun selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä siirrytään sarkaimella tai pikanavigointinäppäimiä käyttäen lomakekenttiin, niiden selitteet luetaan taas tilanteissa, joissa niitä ei aiemmin luettu (erityisesti sellaisissa, joissa käytetään HTML-label-elementtejä). (#4170)
* Microsoft Word: Kommenttien olemassaolon ja niiden sijainnin ilmoittaminen on nyt tarkempaa. (#3528)
* Tiettyjen Microsoft Office -ohjelmien, kuten Wordin, Excelin ja Outlookin valintaikkunoissa navigointia paranneltu estämällä sellaisten säädinsäilötyökalurivien lukeminen, joista ei ole hyötyä käyttäjälle. (#4198) 
* Kohdistus ei enää siirry virheellisesti esim. Microsoft Wordia tai Exceliä avattaessa sellaisiin tehtäväruutuihin kuin Leikepöydän hallinta tai Tiedoston palautus, joka aiheutti sen, että käyttäjän tarvitsi asiakirjan tai laskentataulukon käyttämiseksi siirtyä pois kulloisestakin sovelluksesta ja taas takaisin. (#4199)
* NVDA käynnistyy nyt asianmukaisesti uusimmissa Windowsin versioissa, jos käyttöjärjestelmän kieleksi on määritetty serbia (latinalainen). (#4203)
* Numlockin painaminen näppäinohjetilassa oltaessa vaihtaa nyt näppäimen tilaa sen sijaan, että näppäimistö ja käyttöjärjestelmä muuttuisivat epäsynkronisiksi tämän näppäimen tilan suhteen. (#4226)
* Asiakirjan otsikko luetaan taas Google Chromessa välilehteä vaihdettaessa. Otsikkoa ei luettu joissakin tapauksissa NVDA 2014.2:ssa. (#4222)
* Kun asiakirjasta ilmoitetaan, sen URL-osoitetta ei enää lueta Google Chromessa tai muissa Chrome-pohjaisissa selaimissa. (#4223)
* Kun jatkuva luku -toimintoa käytetään Ei puhetta -syntetisaattorin ollessa valittuna (hyödyllistä automaattisessa testauksessa), toiminto suoritetaan nyt loppuun sen sijaan, että pysähdyttäisiin muutamien ensimmäisten rivien jälkeen. (#4225)
* Microsoft Outlookin Allekirjoitus-valintaikkuna: Allekirjoitus-muokkauskenttä on nyt saavutettava, mikä mahdollistaa tarkan kohdistimen seurannan ja muotoilun havaitsemisen. (#3833) 
* Microsoft Word: Taulukon koko solua ei enää lueta solun viimeistä riviä luettaessa. (#3421)
* Microsoft Word: Koko sisällysluetteloa ei enää lueta sen ensimmäistä tai viimeistä riviä luettaessa. (#3421)
* Sanoja ei enää katkaista virheellisesti esim. vokaalimerkin tai intialaisissa kielissä käytettävän virama-tarkkeen kohdalla kirjoitettuja sanoja luettaessa sekä muutamissa muissa tapauksissa. (#4254)
* Numeeriset muokattavat tekstikentät käsitellään nyt oikein GoldWave-äänieditorissa. (#670)
* Microsoft Word: Kun liikutaan kappaleittain Ctrl+ala- tai Ctrl+ylänuolella, niitä ei tarvitse enää painaa  kahdesti luettelomerkkejä sisältävissä tai numeroiduissa luetteloissa oltaessa. (#3290)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2014.2

### Uudet ominaisuudet

* Tekstin valitsemisen ilmoittaminen on nyt mahdollista joissakin sellaisissa muokkauskentissä, joissa käytetään näytöllä olevaa tietoa. (#770)
* Sijaintitiedot luetaan nyt saavutettavissa Java -sovelluksissa valintapainikkeille ja muille säätimille, jotka välittävät ryhmätietoja. (#3754)
* Pikanäppäimet luetaan nyt saavutettavissa Java -sovelluksissa sellaisille säätimille, joilla niitä on. (#3881)
* Kiintopisteiden selitteet luetaan nyt selaustilassa. Ne näytetään myös Elementtilista-valintaikkunassa. (#1195)
* Nimetyt alueet käsitellään nyt selaustilassa kiintopisteinä. (#3741)
* W3C:n ARIA -standardiin kuuluvia aktiivisia alueita tuetaan nyt Internet Explorer -asiakirjoissa ja -sovelluksissa, mikä mahdollistaa sen, että verkkosivujen tekijät voivat merkitä tietyn sisällön automaattisesti puhuttavaksi sen muuttuessa. (#1846)

= Muutokset ==

* Kun selaustila-asiakirjassa olevasta valintaikkunasta tai sovelluksesta poistutaan, kyseisen asiakirjan nimeä ja tyyppiä ei enää lueta. (#4069)

### Bugikorjaukset

* Standardia Windowsin  järjestelmävalikkoa ei enää vahingossa hiljennetä Java-sovelluksissa. (#3882)
* Rivinvaihtoja ei enää sivuuteta kopioitaessa tekstiä ruuduntarkastelusta. (#3900)
* Tarpeettomia tyhjätilaobjekteja ei enää lueta joissakin sovelluksissa kohdistuksen muuttuessa tai käytettäessä objektinavigointia Yksinkertaisen tarkastelutilan ollessa käytössä. (#3839)
* Ilmoitusruudut ja muut NVDA:n tuottamat valintaikkunat aiheuttavat taas aiemman puheen keskeyttämisen ennen kyseisen valintaikkunan lukemista.
* Säädinten, kuten  linkkien ja painikkeiden, selitteet hahmonnetaan nyt oikein selaustilassa, jos sivun tekijä on korvannut selitteen saavutettavuustarkoituksessa (erityisesti aria-label- tai aria-labeledby-ominaisuuksia käyttäen). (#1354)
* Elementin sisällä olevaa esitykselliseksi  (ARIA role="presentation") merkittyä tekstiä ei enää jätetä virheellisesti huomiotta selaustilassa Internet Explorerissa. (#4031)
* Vietnaminkielisen tekstin kirjoittaminen on taas mahdollista Unikey-ohjelmistoa käytettäessä. Tee tämä poistamalla valinta Käsittele muiden sovellusten näppäinpainallukset -valintaruudusta, joka on lisätty NVDA:n Näppäimistöasetukset-valintaikkunaan. (#4043) 
* Valikkokohteina olevat valintapainikkeet tai -ruudut ilmoitetaan selaustilassa pelkän napsautettavan tekstin sijaan nyt säätimiksi. (#4092)
* NVDA ei enää siirry automaattisesti kohdistustilasta selaustilaan valikkokohteena olevan valintapainikkeen tai valintaruudun ollessa aktiivisena. (#4092)
* Askelpalauttimella poistettuja merkkejä ei enää lueta kirjoitetun sanan osana Microsoft PowerPointissa kirjoitettujen sanojen lukemisen ollessa käytössä. (#3231)
* Yhdistelmäruutujen selitteet luetaan nyt oikein Microsoft Office 2010:n asetusvalintaikkunoissa. (#4056)
* Edelliseen tai seuraavaan painikkeeseen tai lomakekenttään siirtävillä komennoilla voidaan liikkua nyt myös tilanvaihtopainikkeiden välillä selaustilassa Mozilla-sovelluksissa. (#4098)
* Ilmoitusten sisältöä ei enää lueta kahdesti Mozilla-sovelluksissa. (#3481)
* Säilöjä tai kiintopisteitä ei enää virheellisesti toisteta selaustilassa liikuttaessa niissä samaan aikaan sivun sisällön muuttuessa (esim. Facebookin ja Twitterin verkkosivuilla). (#2199)
* NVDA palautuu nyt useammissa tilanteissa siirryttäessä pois sovelluksista, jotka lakkaavat vastaamasta. (#3825)
* Kohdistimen lisäyskohta päivittyy taas asianmukaisesti jatkuva luku -komentoa käytettäessä suoraan näytölle tulostetussa muokattavassa tekstissä oltaessa. (#4125)

## 2014.1

### Uudet ominaisuudet

* Tuki Microsoft PowerPoint 2013:lle. Huomaa, että suojattua näkymää ei tueta. (#3578)
* NVDA lukee nyt valitun symbolin valittaessa niitä Lisää merkkejä -valintaikkunasta Microsoft wordissa ja Excelissä. (#3538)
* Asiakirjojen muotoiluasetukset -valintaikkunassa olevalla uudella asetuksella on nyt mahdollista valita, tunnistetaanko asiakirjaen sisältö napsautettavaksi. Asetus on oletusarvoisesti käytössä (toimii kuten aiemmin). (#3556)
* Tuki Bluetoothin kautta Yhdistettäville pistenäytöille Widcomm Bluetooth -ohjelmistoa käyttävissä tietokoneissa. (#2418)
* Hyperlinkit luetaan nyt muokattaessa tekstiä PowerPointissa. (#3416)
* NVDA on nyt mahdollista pakottaa vaihtamaan verkkosivulla selaustilaan NVDA+välilyönti-näppäinyhdistelmällä ARIA-sovelluksissa tai -valintaikkunoissa oltaessa, mikä mahdollistaa niissä liikkumisen kuten tavallisessa asiakirjassa. (#2023)
* NVDA ilmoittaa nyt Outlook Expressissä, Windows Mailissa ja Windows Live Mailissa, jos viestissä on liite tai jos viesti on merkitty. (#1594)
* Rivien ja sarakkeiden koordinaatit ilmoitetaan nyt saavutettavien Java-sovellusten taulukoissa liikuttaessa. Myös mahdolliset taulukon sarake- ja riviotsikot luetaan. (#3756)

### Muutokset

* Siirrä kokonaistarkasteluun/kohdistukseen -komento on poistettu Papenmeier-pistenäytöistä. Käyttäjät voivat Määrittää omat näppäimensä Syöte-eleet-valintaikkunaa käyttäen. (#3652)
* NVDA käyttää nyt Microsoft VC -ajonaikaisten kirjastojen versiota 11, mikä tarkoittaa, että sitä ei voi käyttää Windows XP Service Pack 2:ta tai Windows Server 2003 Service Pack 1:tä vanhemmissa käyttöjärjestelmissä.
* Tähti (*)- ja plus (+)-merkit puhutaan nyt jotain-välimerkkitasolla, jos NVDA:ta käytetään englanninkielisenä. (#3614)
* eSpeak päivitetty versioksi 1.48.04, joka sisältää korjauksia moniin kieliin sekä useisiin kaatumisiin. (#3842, #3739, #3860)

### Bugikorjaukset

* NVDA:n ei pitäisi enää lukea Microsoft Excelissä uuden solun sijasta aiempaa liikuttaessa soluissa tai valittaessa niitä, kun Excel on hidas siirtämään valintaa. (#3558)
* NVDA käsittelee oikein Microsoft Excelissä solun pudotuslistan avaamisen pikavalikon kautta. (#3586)
* Uusi sisältö näytetään nyt oikein iTunes 11 storen sivuilla selaustilassa seurattaessa storessa olevaa linkkiä tai avattaessa storea ensimmäistä kertaa. (#3625)
* iTunes 11 storen kappaleiden  esikuuntelupainikkeiden selitteet näkyvät nyt  selaustilassa. (#3638)
* Valintaruutujen ja valintapainikkeiden selitteet hahmonnetaan nyt oikein selaustilassa Google Chromessa. (#1562)
* NVDA ei enää lue tarpeetonta tietoa Instantbirdissä joka kerran siirtyessäsi yhteystiedon kohdalle yhteystietoluettelossa. (#2667)
* Sellaisten painikkeiden jne. teksti, joiden selitteet on korvattu työkaluvihjeellä tai muilla keinoin, hahmonnetaan nyt oikein selaustilassa Adobe Readerissa. (#3640)
* Ylimääräisiä "mc-ref"-tekstiä sisältäviä grafiikoita ei enää hahmonneta selaustilassa Adobe Readerissa. (#3645)
* NVDA ei enää ilmoita Microsoft Excelissä kaikkia soluja alleviivatuiksi niiden muotoilutiedoissa. (#3669)
* Selaustila-asiakirjoissa ei enää näytetä tarkoituksettomia merkkejä, kuten esim. Unicode-yksityiskäyttöalueella olevia. Nämä estivät joissakin tapauksissa hyödyllisempien selitteiden näyttämisen. (#2963).
* Itäaasialaisten merkkien syöttämiseen tarkoitettu syöttömenetelmä toimii nyt PuTTY:ssä. (#3432)
* Asiakirjassa liikkumisesta ei enää ole peruutetun jatkuva luku -toiminnon jälkeen seurauksena ajoittain NVDA:n virheellinen ilmoitus kentästä poistumisesta (kuten alempana asiakirjassa olevasta taulukosta, jota jatkuva luku ei ehtinyt puhua). (#3688)
* Kun selaustilan pikanavigointikomentoja käytetään jatkuva luku -toiminnon aikana pikaluvun ollessa käytössä, NVDA ilmoittaa nyt tarkemmin uuden kentän, (ts. sanoo otsikkoa otsikoksi sen sijaan, että lukisi vain sen tekstin). (#3689)
* Säilön loppuun tai alkuun siirtävät pikanavigointikomennot noudattavat nyt Salli pikaluku jatkuvassa luvussa -asetusta (ts. ne eivät enää keskeytä käynnissä olevaa jatkuvaa lukua. (#3675)
* NVDA:n Syöte-eleet-valintaikkunassa lueteltujen kosketuseleiden nimet ovat nyt käyttäjäystävällisiä ja lokalisoituja. (#3624)
* NVDA ei enää aiheuta tiettyjen ohjelmien kaatumista siirrettäessä hiiri niiden rich edit (TRichEdit) -säädinten päälle. Tällaisia ohjelmia ovat mm. Jarte 5.1 sekä BRfácil. (#3693, #3603, #3581)
* Tiettyjä säilöjä (kuten esim. ARIA:n esittelyattribuutilla merkittyjä taulukoita) ei enää lueta Internet Explorerissa ja muissa MSHTML-säätimissä. (#3713)
* NVDA ei enää toista virheellisesti rivien ja sarakkeiden tietoja taulukon solusta useita kertoja Microsoft Wordissa. (#3702)
* Erillisissä tekstilohkoissa olevia numeroita ei enää lueta yhtenä lukuna sellaisissa kielissä, joissa käytetään välilyöntiä numeroiden ryhmittelyyn/tuhaterottimena (kuten esim. ranska ja saksa). Tämä oli erityisen ongelmallista numeroita sisältävissä taulukon soluissa. (#3698)
* Pistenäytön päivittäminen ei enää toisinaan epäonnistu, kun järjestelmäkohdistinta liikutetaan Microsoft Word 2013:ssa. (#3784)
* Kun Microsoft Wordissa ollaan otsikon ensimmäisen merkin kohdalla, otsikkoa ja sen tasoa ilmaiseva teksti ei enää katoa pistenäytöltä. (#3701)
* NVDA poistaa nyt asetusprofiilin käytöstä oikein, kun se on otettu käyttöön sovellukselle, joka suljettiin. (#3732)
* Ehdotuksen sijasta ei enää virheellisesti lueta "NVDA"-sanaa syötettäessä aasialaisia merkkejä NVDA:n omaan säätimeen (esim. selaustilan Etsi-valintaikkunaan). (#3726)
* Outlook 2013:n asetusvalintaikkunan välilehdet luetaan. (#3826)
* ARIA:n aktiivisten alueiden tukea paranneltu Firefoxissa ja muissa Mozilla Gecko -sovelluksissa:
 * Tuki aria-atomic-päivityksille ja aria-busy-päivitysten suodattamiselle. (#2640)
 * Vaihtoehtoinen teksti (kuten alt-attribuutti tai aria-label) näytetään nyt, mikäli muuta tekstiä ei ole käytettävissä. (#3329)
 * Aktiivisten alueiden päivityksiä ei enää hylätä, mikäli ne tapahtuvat samaan aikaan kohdistuksen liikkuessa. (#3777)
* Tiettyjä esityselementtejä ei enää virheellisesti näytetä selaustilassa Firefoxissa ja muissa Mozilla Gecko -sovelluksissa (erityisesti, kun elementti on merkitty aria-presentation-attribuutilla, mutta sen kohdalle on myös mahdollista siirtyä järjestelmäkohdistimella). (#3781)
* Suorituskykyä paranneltu liikuttaessa Microsoft Word -asiakirjassa kirjoitusvirheiden lukemisen ollessa käytössä. (#3785)
* Useita korjauksia saavutettavien Java-sovellusten tukeen:
 * Kehyksen tai valintaikkunan ensimmäinen aktiivinen säädin luetaan nyt oikein kyseisen kehyksen tai valintaikkunan tullessa etualalle. (#3753)
 * Valintapainikkeille ei enää lueta tarpeetonta sijaintitietoa (esim. 1 / 1). (#3754)
 * JComboBox-säätimet luetaan paremmin (enää ei lueta HTML-koodia, avattu- ja suljettu-tilat ilmoitetaan paremmin). (#3755)
 * Teksti, joka aiemmin puuttui valintaikkunoista niitä luettaessa, sisällytetään nyt niihin. (#3757)
 * Aktiivisen säätimen nimen, arvon tai kuvauksen muutokset luetaan nyt tarkemmin. (#3770)
* Korjattu Windows 8:ssa havaittu NVDA:n kaatuminen, kun kohdistus siirretään tiettyihin paljon tekstiä sisältäviin RichEdit-säätimiin (esim. NVDA:n lokintarkastelutoiminto ja Windbg). (#3867)
* NVDA ei enää siirrä hiirtä väärään paikkaan joissakin sovelluksissa sellaisissa järjestelmissä, joiden näytöissä on korkea DPI-tarkkuus (koskee oletusarvoisesti useita uusia näyttöjä). (#3758, #3703)
* Korjattu verkkosivuja selattaessa ongelma, jossa NVDA lakkasi toimimasta kunnolla ellei sitä käynnistetty uudelleen, vaikkei se kaatunutkaan tai jäänytkään jumiin. (#3804)
* Papenmeier-pistenäyttöä  voidaan nyt käyttää, vaikkei sellaista ole aiemmin kytketty koneeseen USB:n kautta. (#3712)
* NVDA ei jää enää jumiin, kun Papenmeier BRAILLEX:n vanhempi malli on valittu pistenäytöksi ja jos sitä ei ole kytketty koneeseen.

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2013.3

### Uudet ominaisuudet

* Lomakekentät luetaan nyt Microsoft word -asiakirjoissa. (#2295)
* NVDA lukee nyt muokkaustiedot Microsoft Wordissa, kun muutosten jäljittäminen on käytössä. Huomaa, että NVDA:n Asiakirjojen muotoiluasetukset -valintaikkunan Lue muokkaajan merkinnät -asetuksen on myös oltava käytössä näiden tietojen lukemiseksi (oletusarvoisesti poissa käytöstä). (#1670)
* Microsoft Excel 2003-2010:n pudotuslistat luetaan nyt avattaessa ja niissä liikuttaessa. (#3382)
* Näppäimistöasetukset-valintaikkunan uusi "Salli pikaluku jatkuvassa luvussa" -asetus mahdollistaa asiakirjassa liikkumisen selaustilan pikanavigointia sekä riveittäin/kappaleittain siirtäviä komentoja käyttäen jatkuvan luvun aikana. Asetus on oletusarvoisesti poissa käytöstä. (#2766)
* Syöte-eleet-valintaikkuna mahdollistaa helpomman NVDA-komennoissa käytettävien syöte-eleiden (kuten näppäimistön näppäinten) mukauttamisen. (#1532)
* Asetusprofiilit mahdollistavat eri asetukset eri tilanteissa. Profiilit voidaan ottaa käyttöön manuaalisesti tai automaattisesti (esim. tietyssä sovelluksessa). (#87, #667, #1913)
* Linkkkejä sisältävät solut ilmaistaan nyt linkkeinä Microsoft Excelissä. (#3042)
* Solussa olevista kommenteista ilmoitetaan nyt käyttäjälle Microsoft Excelissä. (#2921)

### Bugikorjaukset

* Zend Studio toimii nyt samalla tavalla kuin Eclipse. (#3420)
* Tiettyjen valintaruutujen muuttunut tila luetaan nyt automaattisesti Microsoft Outlook 2010:n viestisääntöjen valintaikkunassa. (#3063)
* NVDA lukee nyt kiinnitettyjen säädinten kuten esim. Mozilla Firefoxin välilehtien tilan. (#3372)
* Skriptejä on nyt mahdollista liittää Alt- ja/tai Windows-näppäimiä sisältäviin näppäinkomentoihin. Aiemmin tämä olisi aiheuttanut  skriptiä suoritettaessa Käynnistä-valikon tai valikkorivin avaamisen. (#3472)
* Tekstin valitseminen selaustila-asiakirjoissa (esim. Ctrl+Shift+End-näppäimiä käyttäen) ei enää aiheuta näppäinasettelun vaihtumista järjestelmissä, joissa on asennettuna useita näppäinasetteluja. (#3472)
* Internet Explorerin ei pitäisi enää kaatua tai muuttua käyttökelvottomaksi, kun NVDA suljetaan. (#3397)
* Fyysisiä liikkeitä ja muita tapahtumia ei enää käsitellä väärinä näppäinpainalluksina joissakin uudemmissa tietokoneissa. Aiemmin tämä vaiensi puheen sekä suoritti toisinaan NVDA-komentoja. (#3468)
* NVDA toimii nyt odotetusti Poedit 1.5.7:ssä. Aiempia versioita käyttävien on päivitettävä. (#3485)
* NVDA lukee nyt suojattuja asiakirjoja Microsoft Word 2010:ssä, eikä aiheuta enää Wordin kaatumista. (#1686)
* Mikäli NVDA:n jakelupakettia käynnistettäessä annetaan tuntematon komentorivivalitsin, se ei enää aiheuta virheilmoitusvalintaikkunoita päättymättömänä silmukkana. (#3463)
* Grafiikoiden ja objektien alt-tekstin lukeminen ei enää epäonnistu Microsoft Wordissa, jos alt-teksti sisältää lainaus- tai muita epästandardeja merkkejä. (#3579)
* Vaakasuuntaisissa luetteloissa olevien kohteiden määrä on nyt oikein selaustilassa. Aiemmin todellinen määrä saattoi kaksinkertaistua. (#2151)
* Päivitetty valinta luetaan nyt painettaessa Ctrl+A-näppäinyhdistelmää Microsoft Excel -työkirjassa. (#3043)
* NVDA lukee nyt XHTML-asiakirjat oikein Internet Explorerissa ja muissa MSHTML-säätimissä. (#3542)
* Näppäimistöasetukset-valintaikkuna: mikäli NVDA-näppäimenä käytettävää näppäintä ei ole valittu, käyttäjälle näytetään virheilmoitus valintaikkunaa suljettaessa. Vähintään yksi näppäin on valittava NVDA:n asianmukaisen käytön varmistamiseksi. (#2871)
* NVDA ilmaisee nyt Microsoft Excelissä yhdistetyt solut eri tavalla kuin useat valitut solut. (#3567)
* Selaustilakohdistinta ei sijoiteta enää virheellisesti poistuttaessa asiakirjan sisäisestä valintaikkunasta tai sovelluksesta. (#3145)
* Korjattu ongelma, joka aiheutti sen, että joissakin järjestelmissä HumanWare Brailliant BI/B -sarjan pistenäytön ajuria ei näytetty Pistekirjoitusasetukset-valintaikkunassa, vaikka sellainen näyttö oli liitettynä USB:n kautta.
* NVDA:n vaihtaminen ruuduntarkasteluun ei enää epäonnistu, mikäli navigointiobjektilla ei ole ruudulla todellista sijaintia. Tarkastelukohdistin sijoitetaan nyt tällaisessa tapauksessa ruudun yläreunaan. (#3454)
* Korjattu ongelma, joka aiheutti joissakin tapauksissa Freedom Scientificin pistenäyttöajurin toimimattomuutta, kun portiksi oli määritetty USB. (#3509, #3662)
* Korjattu ongelma, joka aiheutti joissakin tapauksissa sen, että Freedom Scientificin pistenäyttöjen näppäimiä ei tunnistettu. (#3401, #3662)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2013.2

### Uudet ominaisuudet

* Tuki sisäänrakennetulle Chromium-sovelluskehykselle, joka on useissa sovelluksissa käytettävä verkkoselainsäädin. (#3108)
* Uusi eSpeakin puheäänimuunnelma: Iven3.
* Uudet chattiviestit luetaan Skypessä automaattisesti keskustelun ollessa aktiivisena. (#2298)
* Lisätty twitter-asiakasohjelma Tweenin tuki, johon sisältyy välilehtien nimien lukeminen ja vähemmän puheliaisuutta twiittejä luettaessa.
* NVDA:n ilmoitusten näyttäminen pistenäytöllä voidaan poistaa nyt käytöstä määrittämällä Pistekirjoitusasetukset-valintaikkunassa ilmoitusten aikakatkaisun arvoksi 0. (#2482)
* Lisäosien hallinnassa on nyt Hae lisäosia -painike, joka avaa verkkosivun, josta lisäosia on mahdollista selata ja ladata. (#3209)
* Tervetuloa-valintaikkunassa, joka tulee näkyviin aina ensimmäisellä NVDA:n käynnistyksellä, voidaan nyt määrittää, käynnistyykö NVDA automaattisesti Windowsiin kirjautumisen jälkeen. (#2234)
* Lepotila otetaan nyt automaattisesti käyttöön Dolphin Cicero -ohjelmistoa käytettäessä. (#2055)
* Lisätty tuki Miranda IM:n/Miranda NG:n 64-bittiselle versiolle. (#3296)
* Haun ehdotukset luetaan nyt automaattisesti Windows 8.1:n aloitusnäytössä. (#3322)
* Tuki laskentataulukoissa liikkumiselle ja niiden muokkaamiselle Microsoft Excel 2013:ssa. (#3360)
* Freedom Scientificin Focus 14 Blue-, Focus 80 Blue- sekä tietyissä kokoonpanoissa myös Focus 40 Blue -pistenä'yttöjä, joita ei aiemmin tuettu, tuetaan nyt Bluetoothin kautta yhdistettäessä. (#3307)
* Automaattisen täydennyksen ehdotukset luetaan nyt Outlook 2010:ssä. (#2816)
* Uusia pistetaulukoita: englannin (Iso-Britannia) tietokonemerkistö, korealainen taso 2, venäläinen tietokonemerkistö.
* Uusi kieli: farsi. (#1427)

### Muutokset

* Kosketusnäytöllä vasemmalle tai oikealle pyyhkäiseminen yhdellä sormella objektitilassa oltaessa siirtää nyt edelliseen tai seuraavaan kaikissa objekteissa, ei pelkästään nykyisessä säilössä. Alkuperäinen nykyisessä säilössä edelliseen tai seuraavaan objektiin siirtäminen suoritetaan pyyhkäisemällä vasemmalle tai oikealle kahdella sormella.
* Selaustilan asetukset -valintaikkunasta löytyvän Lue asettelutaulukot -valintaruudun uudeksi nimeksi on nyt muutettu Sisällytä asettelutaulukot, jotta se kuvastaisi sitä, että jos tämä valintaruutu ei ole valittuna, niin asettelutaulukoita ei löydy myöskään pikanavigointikomennoilla. (#3140)
* Kokonaistarkastelu on korvattu objektin-, asiakirjan- ja ruuduntarkastelutiloilla. (#2996)
 * Objektintarkastelu lukee vain navigointiobjektissa olevaa tekstiä, asiakirjantarkastelu kaikkea mahdollisesti selaustila-asiakirjassa olevaa tekstiä ja ruuduntarkastelu ruudulla olevaa tekstiä nykyisessä sovelluksessa.
 * Aiemmin kokonaistarkasteluun ja siitä pois siirtäneet komennot vaihtavat nyt näiden uusien tarkastelutilojen välillä.
 * Navigointiobjekti seuraa automaattisesti tarkastelukohdistinta niin, että se pysyy tarkastelukohdistimen kohdalla asiakirjan- tai ruuduntarkastelutiloissa oltaessa.
 * NVDA pysyy ruuduntarkastelutilassa siihen vaihtamisen jälkeen kunnes vaihdetaan takaisin asiakirja- tai objektintarkastelutilaan.
 * NVDA voi vaihtaa automaattisesti asiakirjan- tai objektintarkastelutilassa oltaessa näiden kahden tilan välillä riippuen siitä, liikutaanko selaustila-asiakirjassa vai ei.
* Liblouis-pistekääntäjä päivitetty  versioksi 2.5.3. (#3371)

### Bugikorjaukset

* Toiminto luetaan nyt objektia aktivoitaessa ennen aktivointia sen sijaan, että toiminto luettaisiin aktivoinnin jälkeen (esim. puunäkymää avattaessa ilmoitetaan "avaa" sen sijaan, että ilmoitettaisiin sulje). (#2982)
* Eri syöttökenttien, kuten chatti- ja haku, tarkempi lukeminen ja kohdistimen seuranta Skypen uusimmissa versioissa. (#1601, #3036)
* Uusien tapahtumien määrä luetaan nyt Skypen uusimpien keskustelujen luettelossa jokaiselle keskustelulle, mikäli tarpeen. (#1446)
* Parannuksia kohdistimen seurantaan ja lukemisjärjestykseen ruudulla olevalle oikealta vasemmalle luettavalle tekstille, esim. muokattaessa arabialaista tekstiä Microsoft Excelissä. (#1601)
* Saavutettavuustarkoituksessa painikkeiksi merkityt linkit löytyvät nyt Internet Explorerissa painikkeisiin ja lomakekenttiin siirryttäessä pikanavigointia käyttäen. (#2750)
* Puunäkymien sisältöä ei enää näytetä selaustilassa, sillä kokonaisesityksestä ei ole hyötyä. Puunäkymän kanssa voidaan olla vuorovaikutuksessa vuorovaikutustilassa painamalla Enteriä sen kohdalla. (#3023)
* Alt+ala- tai ylänuolen painaminen vuorovaikutustilassa yhdistelmäruudun avaamiseksi ei enää vaihda virheellisesti selaustilaan. (#2340)
* Taulukon solut eivät enää aktivoi Internet Explorer 10:ssä vuorovaikutustilaa, ellei verkkosivun tekijä ole nimenomaan tehnyt niistä aktivoitavia. (#3248)
* NVDA:n käynnistäminen ei enää epäonnistu, mikäli järjestelmän päiväys tai kellonaika on aikaisempi kuin viimeisin päivitysten tarkistus. (#3260)
* Jos pistenäytöllä näytetään edistymispalkki, näyttöä päivitetään palkin muuttuessa. (#3258)
* Taulukon otsikoita ei enää näytetä kahdesti selaustilassa Mozilla-sovelluksissa. Lisäksi näytetään yhteenveto, mikäli taulukossa on otsikko. (#3196)
* NVDA ilmoittaa nyt oikean kielen aiemmin käytössä olleen sijasta Windows 8:ssa syöttökieltä vaihdettaessa.
* NVDA ilmoittaa nyt IME-muunnostilan vaihdokset Windows 8:ssa.
* NVDA ei enää lue ylimääräistä työpöydällä Google Japanese tai Atok IME -syöttömenetelmiä käytettäessä. (#3234)
* NVDA ei enää ilmoita virheellisesti puheentunnistusta tai kosketussyötettä näppäimistön kielen vaihdokseksi Windows 7:ssä ja uudemmissa.
* NVDA ei enää lue tiettyä erikoismerkkiä (0x7f) painettaessa Ctrl+askelpalautin-näppäinyhdistelmää joissakin tekstieditoreissa Puhu kirjoitetut merkit -asetuksen ollessa käytössä. (#3315)
* espeak ei enää vaihda virheellisesti äänenkorkeuttaan, voimakkuuttaan jne NVDA:n lukiessa tiettyjä ohjausmerkkejä tai XML-koodia sisältävää tekstiä. (#3334) (#437:n paluu)
* Aktiivisen säätimen selitteen tai arvon muutokset luetaan nyt Java-sovelluksissa automaattisesti sekä hyödynnetään myöhemmin kyseistä säädintä kyseltäessä. (#3119)
* Rivit luetaan nyt oikein Scintilla-säätimissä automaattisen rivityksen ollessa käytössä. (#885)
* Vain luku -tyyppiä olevien luettelokohteiden nimi luetaan nyt oikein Mozilla-sovelluksissa, esim. liikuttaessa vuorovaikutustilassa twiiteissä twitter.com-sivulla. (#3327)
* Microsoft Office 2013:n vahvistusvalintaikkunoiden sisältö luetaan nyt automaattisesti niiden tullessa näkyviin.
* Suorituskyvyn parannuksia liikuttaessa tietyissä taulukoissa Microsoft Wordissa. (#3326)
* NVDA:n taulukkonavigointikomennot (Ctrl+Alt+nuolet) toimivat paremmin sellaisissa Microsoft Word -taulukoissa, joissa solu jakaantuu usealle riville.
* Mikäli Lisäosien hallinta on jo avoimena, sen uudelleen avaaminen (joko Työkalut-valikosta tai lisäosatiedoston avaamalla) ei enää epäonnistu tai tee mahdottomaksi sen sulkemista. (#3351)
* NVDA ei enää jumiudu tietyissä valintaikkunoissa japanin- tai kiinankielisen Office 2010:n IME:n ollessa käytössä. (#3064)
* Useita välilyöntejä ei enää tiivistetä pistenäytöillä yhdeksi. (#1366)
* Zend Eclipse PHP Developer Tools toimii nyt samalla tavalla kuin Eclipse. (#3353)
* Sarkaimen painaminen ei ole tarpeen Internet Explorerissa vuorovaikutukseen upotettujen objektien (kuten Flash-sisällön) kanssa kun sen kohdalla on painettu Enteriä. (#3364)
* Mikäli viimeinen rivi on tyhjä, sitä ei enää lueta Microsoft PowerPointissa tekstiä muokattaessa sen yläpuolella olevana rivinä. (#3403)
* Objekteja ei enää lueta Microsoft PowerPointissa ajoittain kahdesti niitä valittaessa tai muokattaessa. (#3394)
* NVDA ei enää aiheuta Adobe Readerin kaatumista tai jumiutumista tietyissä väärin muotoilluissa PDF-asiakirjoissa, jotka sisältävät taulukoiden ulkopuolisia rivejä. (#3399)
* NVDA tunnistaa nyt asianmukaisesti seuraavan aktiivisen dian poistettaessa niitä Microsoft PowerPointin pikkukuvanäkymässä. (#3415)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2013.1.1

Tämä versio korjaa ongelman, joka aiheutti sen, että NVDA kaatui käynnistettäessä, mikäli käytettäväksi kieleksi oli määritetty iiri. Lisäksi tämä versio sisältää käännösten päivityksiä sekä joitakin muita ohjelmavirheiden korjauksia.

### Bugikorjaukset

* Nyt tuotetaan asianmukaisia merkkejä kirjoitettaessa NVDA:n omassa käyttöliittymässä käytettäessä korealaista tai japanilaista syöttömenetelmää jommankumman ollessa oletusmenetelmänä. (#2909)
* Kentät, jotka on merkitty virheellisen syötteen sisältäviksi, käsitellään nyt oikein Internet Explorerissa ja muissa MSHTML-säätimissä. (#3256)
* NVDA ei enää kaadu käynnistettäessä, mikäli käytettäväksi kieleksi on määritetty iiri.

## 2013.1

Tämän version tärkeimpiä uusia ominaisuuksia ovat intuitiivisempi ja johdonmukaisempi kannettavien tietokoneiden näppäinasettelu, alkeellinen tuki Microsoft PowerPointille, pitkien kuvausten tuki verkkoselaimissa sekä tuki pistekirjoituksen syöttämiselle pistenäytöissä, joissa on pistenäppäimistö.

### Tärkeää

#### Uusi kannettavien tietokoneiden näppäinasettelu

Kannettavien tietokoneiden näppäinasettelu on suunniteltu täysin uudelleen, jotta se olisi intuitiivisempi ja johdonmukaisempi.
Uudessa asettelussa käytetään nuolinäppäimiä yhdessä NVDA-näppäimen kanssa sekä tekstintarkastelukomennoissa myös muita muokkausnäppäimiä.

Huomaa seuraavat yleisimmin käytettyihin komentoihin tehdyt muutokset:

| Nimi |Näppäinkomento|
|---|---|
|Jatkuva luku |NVDA+A|
|Lue nykyinen rivi |NVDA+L|
|Lue valittu teksti |NVDA+Shift+S|
|Lue tilarivi |NVDA+Shift+End|

Lisäksi mm. kaikki objektinavigointi-, tekstintarkastelu-, hiiren napsautus- sekä syntetisaattorin asetusrenkaan komennot ovat muuttuneet.
Katso uudet näppäinkomennot [komentojen pikaoppaasta.](keyCommands.html)

### Uudet ominaisuudet

* Alkeellinen tuki Microsoft PowerPoint -esitysten muokkaamiselle ja lukemiselle. (#501)
* Alkeellinen tuki viestien lukemiselle ja kirjoittamiselle Lotus Notes 8.5:ssä. (#543)
* Tuki automaattiselle kielen vaihtamiselle luettaessa asiakirjoja Microsoft Wordissa. (#2047) 
* Pitkät kuvaukset ilmoitetaan nyt selaustilassa MSHTML- ja Gecko-sovelluksissa (esim. Internet Explorerissa ja Firefoxissa). Ne on lisäksi mahdollista avata uuteen ikkunaan painamalla NVDA+D. (#809)
* Ilmoitukset, kuten sisällön estäminen tai tiedostolataukset, luetaan nyt Internet Explorer 9:ssä ja uudemmissa. (#2343)
* Automaattista taulukon rivien ja sarakkeiden otsikoiden lukemista tuetaan nyt selaustila-asiakirjoissa Internet Explorerissa ja muissa MSHTML-säätimissä. (#778)
* Uusia kieliä: aragonia, iiri
* Uusia pistetaulukoita: tanskalainen taso 2, korealainen taso 1.
* Tuki bluetoothin kautta yhdistettäville pistenäytöille Toshiban bluetooth-pinoa käyttävissä tietokoneissa. (#2419)
* Portin valitseminen on nyt mahdollista Freedom Scientificin pistenäyttöjä käytettäessä (Automaattinen, USB tai Bluetooth).
* Tuki Humanwaren BrailleNote-tuoteperheen muistiinpanolaitteille käytettäessä niitä ruudunlukuohjelman pistenäyttönä. (#2012)
* Tuki Papenmeier BRAILLEX -pistenäyttöjen vanhoille malleille. (#2679)
* Tuki pistekirjoituksen syöttämiselle tietokonemerkistöä käyttäen pistenäytöissä, joissa on pistenäppäimistö. (#808)
* Lisätty uusia näppäimistöasetuksia, joilla voidaan valita, keskeyttääkö NVDA puhumisen merkkejä kirjoitettaessa ja/tai Enteriä painettaessa. (#698)
* Tuki useille Google Chrome -pohjaisille selaimille: Rockmelt, BlackHawk, Comodo Dragon ja SRWare Iron. (#2236, #2813, #2814, #2815)

### Muutokset

* Liblouis-pistekääntäjä päivitetty versioksi 2.5.2. (#2737)
* Kannettavien tietokoneiden näppäinasettelu on suunniteltu täysin uudelleen, jotta se olisi intuitiivisempi ja johdonmukaisempi. (#804)
* eSpeak-puhesyntetisaattori päivitetty versioksi 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Bugikorjaukset

* Seuraavaan tai edelliseen erottimeen siirtävät Pikanavigointinäppäimet toimivat nyt selaustilassa Internet Explorerissa ja muissa MSHTML-säätimissä. (#2781)
* Mikäli NVDA turvautuu käynnistyessään eSpeakiin tai Ei puhetta -syntetisaattoriin käyttöön määritetyn puhesyntetisaattorin lataamisen epäonnistumisen vuoksi, varmistussyntetisaattoria ei enää muuteta oletukseksi. Tämä tarkoittaa, että alkuperäinen syntetisaattori yritetään nyt ladata uudelleen seuraavalla NVDA:n käynnistyskerralla. (#2589)
* Mikäli NVDA turvautuu käynnistyessään Ei pistenäyttöä -vaihtoehtoon käyttöön määritetyn pistenäytön lataamisen epäonnistumisen vuoksi, käytettäväksi näytöksi ei enää automaattisesti määritetä Ei pistenäyttöä. Tämä tarkoittaa, että alkuperäinen pistenäyttö yritetään nyt ladata uudelleen seuraavalla NVDA:n käynnistyskerralla. (#2264)
* Taulukoiden päivitykset näytetään nyt oikein selaustilassa Mozilla-sovelluksissa. Esim. rivien ja sarakkeiden koordinaatit luetaan päivitetyissä soluissa ja taulukossa liikkuminen toimii kuten pitääkin. (#2784)
* Tietyt napsautettavat nimeämättömät grafiikat, joita ei aiemmin näytetty, näytetään nyt asianmukaisesti selaustilassa verkkoselaimissa. (#2838)
* Vanhempia ja uudempia SecureCRT:n versioita tuetaan. (#2800)
* Lukumerkkijono luetaan nyt oikein Windows XP:ssä Sellaisilla syöttömenetelmillä kuin Easy Dots IME.
* Yksinkertaistetun kiinan Microsoft Pinyin -syöttömenetelmän ehdotuslista luetaan nyt oikein vaihdettaessa sivuja vasemmalla ja oikealla nuolella ja avattaessa sitä ensimmäistä kertaa Home-näppäimellä Windows 7:ssä.
* Edistynyttä "preserve"-kenttää ei enää poisteta omia symbolinpuhumissääntöjä tallennettaessa. (#2852)
* Kun automaattinen päivitysten tarkistus poistetaan käytöstä, NVDA:ta ei tarvitse enää käynnistää uudelleen muutoksen käyttöönottamiseksi.
* NVDA käynnistyy nyt oikein, jos lisäosaa ei voida poistaa siksi, että sen hakemisto on jonkin toisen sovelluksen käytössä. (#2860)
* DropBoxin asetusvalintaikkunan välilehtien nimet näkyvät nyt kokonaistarkastelussa.
* NVDA tunnistaa nyt oikein komennoissa käytettävät ja näppäinohjetilassa painettavat näppäimet, jos syöttökieleksi on määritetty jokin muu kuin oletuskieli.
* Sellaisissa kielissä, joissa +-merkki on yksittäinen näppäin (kuten esim. saksa), siihen on nyt mahdollista liittää komentoja käyttämällä sanaa "plus". (#2898)
* Sisennetyt lainaukset luetaan nyt Internet Explorerissa ja muissa MSHTML-säätimissä. (#2888)
* HumanWare Brailliant BI/B -pistenäyttöajuri on nyt mahdollista valita, kun näyttö on liitetty tietokoneeseen bluetoothilla, mutta ei vielä kertaakaan USB:llä.
* Elementtien suodattaminen isoilla kirjaimilla kirjoitetulla tekstillä selaustilan elementtilistassa näyttää nyt tuloksia, joiden kirjainkoolla ei ole väliä, aivan kuten pienellä kirjoitetuilla. Aiemmin ei näytetty mitään. (#2951)
* Selaustilan käyttäminen on taas mahdollista Mozilla-sovelluksissa Flash-sisällön ollessa aktiivisena. (#2546)
* Pistekohdistin sijoitetaan nyt oikein, kun se on  sellaisen sanan jäljessä, jonka merkki esitetään useassa pistesolussa (esim. ison alkukirjaimen merkki, kirjainmerkki, numeromerkki jne) lyhennepistekirjoitustaulukkoa käytettäessä ja Laajenna kohdistimen kohdalla oleva sana -asetuksen ollessa käytössä. (#2947)
* Tekstin valitseminen näytetään nyt oikein pistenäytöllä sellaisissa sovelluksissa kuin Microsoft word 2003 ja Internet Explorerin muokkaussäätimet.
* Tekstin taaksepäin valitseminen on taas mahdollista Microsoft Wordissa pistenäytön ollessa käytössä.
* NVDA lukee monitavuiset merkit oikein Scintilla-muokkaussäätimissä tekstiä luettaessa, askelpalautinta käytettäessä tai merkkejä poistettaessa. (#2855)
* NVDA:n asennus ei enää epäonnistu, kun käyttäjäprofiilin hakemistopolku sisältää tiettyjä monitavuisia merkkejä. (#2729)
* Luettelonäkymäsäädinten (SysListview32) ryhmien ilmoittaminen ei aiheuta enää virhettä 64-bittisissä sovelluksissa.
* Tekstisisältöä ei enää joissakin harvoissa tapauksissa käsitellä Mozilla-sovelluksissa virheellisesti selaustilassa muokattavana. (#2959)
* Järjestelmäkohdistimen siirtäminen IBM Lotus Symphonyssa ja OpenOfficessa siirtää nyt tarvittaessa tarkastelukohdistinta.
* Flash-sisältö on nyt saavutettavaa Internet Explorerissa Windows 8:ssa. (#2454)
* Korjattu Papenmeier Braillex Trio -pistenäytön Bluetooth-tuki. (#2995)
* Korjattu ongelma, joka aiheutti sen, että tiettyjen Microsoft Speech API versio 5 -puheäänten, kuten Koba Speech 2, käyttäminen ei ollut mahdollista. (#2629)
* Pistenäyttö päivittyy nyt oikein Java Access Bridgeä käyttävissä sovelluksissa liikutettaessa kohdistinta muokattavissa tekstikentissä. (#3107)
* Lomake-kiintopistettä tuetaan nyt kiintopisteitä tukevissa selaustila-asiakirjoissa. (#2997)
* eSpeak-syntetisaattoriajuri käsittelee nyt merkeittäin lukemista asianmukaisemmin (esim. lukee vierasperäisen kirjaimen nimen tai arvon sen äänen tai yleisnimen sijaan). (#3106)
* Käyttäjän asetusten kopiointi kirjautumisikkunassa ja muissa suojatuissa ruuduissa käytettäväksi ei enää epäonnistu, kun käyttäjäprofiilin hakemistopolku sisältää muita kuin ASCII-merkkejä. (#3092)
* NVDA ei jää enää jumiin joissakin .NET-sovelluksissa aasialaisten kielten merkkejä syötettäessä. (#3005)
* Selaustilan käyttäminen on nyt mahdollista Internet Explorer 10:ssä (esim. [www.gmail.com](http://www.gmail.com) -kirjautumissivulla) yhteensopivuustilassa oltaessa. (#3151)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2012.3

Tämän version uusia ominaisuuksia ovat mm. tuki aasialaisten kielten merkkien syöttämiselle, kokeellinen tuki kosketusnäytöille Windows 8:ssa, sivunumeroiden lukeminen ja paranneltu taulukoiden tuki Adobe Readerissa, taulukkokomennot aktiivisille taulukon riveille ja Windowsin luettelonäkymäsäätimille, tuki usealle uudelle pistenäytölle sekä rivien ja sarakkeiden otsikoiden lukeminen Microsoft Excelissä.

### Uudet ominaisuudet

* NVDA tukee nyt aasialaisten kielten merkkien kirjoittamista IME- ja Tekstipalvelu-syöttömenetelmillä kaikissa sovelluksissa. Lisäksi on mahdollista:
 * Ehdotuslistojen lukeminen ja niissä liikkuminen.
 * Merkkiyhdistelmien lukeminen ja niissä liikkuminen.
  * Lukumerkkijonon ilmoittaminen.
* Alle- ja yliviivaus ilmoitetaan nyt Adobe Reader -asiakirjoissa. (#2410)
* NVDA-näppäin toimii nyt kuin muutkin toimintonäppäimet Windowsin alasjäävien näppäinten ollessa käytössä. Tämä mahdollistaa NVDA-näppäimen käytön tarvitsematta pitää sitä alhaalla painettaessa samaan aikaan muita näppäimiä. (#230)
* Sarakkeiden ja rivien otsikoiden automaattista lukemista tuetaan nyt Microsoft Excelissä. Sarakkeiden otsikot sisältävä rivi määritetään painamalla NVDA+Shift+C ja rivien otsikot sisältävä sarake painamalla NVDA+Shift+R. Asetukset nollataan painamalla näitä komentoja kahdesti. (#1519)
* Tuki HIMS Braille Sense-, Braille EDGE- ja SyncBraille -pistenäytöille. (#1266, #1267)
* NVDA lukee Windows 8:n ilmoitusruudut niiden tullessa näkyviin, jos ohjeselitteiden lukeminen on käytössä. (#2143)
* Kokeellinen tuki kosketusnäytöille Windows 8:ssa, mukaan lukien:
 * Sormen alla olevan tekstin lukeminen sitä liikutettaessa
 * Useita objektinavigointiin, tekstin lukemiseen ja muihin NVDA-komentoihin tarkoitettuja eleitä.
* Tuki VIP Mudille. (#1728)
* Jos taulukossa on yhteenveto, se luetaan nyt Adobe Readerissa. (#2465)
* Taulukon rivien ja sarakkeiden otsikot luetaan nyt Adobe Readerissa. (#2193, #2527, #2528)
* Uusia kieliä: amhara, korea, nepali ja slovenia.
* NVDA lukee nyt automaattisen täydennyksen ehdotukset Microsoft Outlook 2007:ssä sähköpostiosoitteita syötettäessä. (#689)
* Uusia eSpeakin puheäänimuunnelmia: Gene, Gene2. (#2512)
* Sivunumerot luetaan nyt Adobe Readerissa. (#2534)
 * Sivujen nimet luetaan Reader XI:ssä aina kun ne ovat saatavilla eri osien sivunumerointia noudattaen jne. Tämä ei ole mahdollista vanhemmissa versioissa, ja lisäksi vain peräkkäiset sivunumerot luetaan.
* NVDA:n oletusasetukset on nyt mahdollista palauttaa joko painamalla kolme kertaa nopeasti NVDA+Ctrl+R tai valitsemalla NVDA -valikosta Palauta oletusasetukset. (#2086)
* Tuki Nippon Telesoftin Seika (versioille 3, 4 ja 5)- sekä Seika80-pistenäytöille. (#2452)
* Freedom Scientificin PAC Mate- ja Focus-pistenäyttöjen ensimmäistä ja viimeistä ylintä kosketuskohdistinnäppäintä voidaan nyt käyttää taakse- ja eteenpäin vierittämiseen. (#2556)
* Freedom Scientificin Focus--pistenäytöissä tuetaan entistä useampia ominaisuuksia, kuten eteenpäin siirtävät näppäimet, keinunäppäimet sekä tietyt pisteyhdistelmät yleisille toiminnoille. (#2516)
* Taulukon rivien ja sarakkeiden otsikot on nyt mahdollista lukea selaustilan ulkopuolella IAccessible2-rajapintaa käyttävissä sovelluksissa, kuten Mozilla Firefoxissa. (#926)
* Alustava tuki Microsoft Word 2013:n asiakirjasäätimelle. (#2543)
* Tekstin tasauksen ilmoittaminen on nyt  mahdollista IAccessible2-rajapintaa käyttävissä sovelluksissa, kuten Mozilla Firefoxissa. (#2612)
* Kun taulukon rivi tai normaali Windowsin useita sarakkeita sisältävä luettelonäkymäsäädin  on aktiivisena, taulukossa liikkumiseen tarkoitettuja komentoja voidaan nyt käyttää yksittäisiin soluihin pääsemiseen. (#828)
* Uusia pistetaulukoita: virolainen taso 0, portugalilainen 8 pisteen tietokonemerkistö, italialainen 6 pisteen tietokonemerkistö. (#2319, #2662)
* Jos NVDA on asennettu tietokoneelle, lisäosapaketin avaaminen suoraan (esim. Resurssienhallinnasta tai verkkoselaimesta lataamisen jälkeen) asentaa sen NVDA:han. (#2306)
* Tuki uusille Papenmeier BRAILLEX -pistenäytöille. (#1265)
* Sijaintitiedot (esim. 1 / 4) luetaan nyt Resurssienhallinnan luettelokohteille Windows 7:ssä ja uudemmissa käyttöjärjestelmissä. Tähän sisältyvät myös kaikki mukautettuja itemIndex- ja itemCount-ominaisuuksia tukevat UIAutomation-säätimet. (#2643)

### Muutokset

* Tarkastelukohdistimen asetukset -valintaikkunassa oleva Seuraa näppäimistökohdistusta -asetuksen uusi nimi on Seuraa järjestelmän kohdistusta, jotta se olisi yhdenmukainen muualla NVDA:ssa käytetyn terminologian kanssa.
* Kun pistenäyttö on asetettu seuraamaan tarkastelukohdistinta ja kun kohdistin on sellaisessa objektissa, joka ei ole tekstiobjekti (esim. muokattava tekstikenttä), kosketuskohdistinnäppäimet aktivoivat kyseisen objektin. (#2386)
* Tallenna asetukset suljettaessa -asetus on nyt oletusarvoisesti käytössä uusissa kokoonpanoissa.
* Kun aiemmin asennettua NVDA:n versiota päivitetään, työpöydän pikakuvakkeen pikanäppäintä ei pakoteta enää takaisin Ctrl+Alt+N:ksi, mikäli käyttäjä on muuttanut sen joksikin muuksi. (#2572)
* Lisäosien hallinnan lisäosaluettelo näyttää nyt paketin nimen ennen sen tilaa. (#2548)
* Jos nykyisestä asennetusta lisäosasta asennetaan sama tai jokin toinen versio, virheen näyttämisen ja asennuksen keskeyttämisen sijaan NVDA kysyy nyt, halutaanko se päivittää. (#2501)
* Objektinavigointikomennot (kaikki paitsi Lue nykyinen objekti) ovat nyt vähemmän puheliaita. Lisätiedot saadaan edelleen Lue nykyinen objekti -komennolla. (#2560)
* liblouis-pistekääntäjä päivitetty versioksi 2.5.1. (#2319, #2480, #2662, #2672)
* NVDA:n näppäinkomentojen pikaopas -asiakirja on nimetty uudelleen komentojen pikaoppaaksi, sillä se sisältää nyt sekä kosketuseleitä että näppäinkomentoja.
* Selaustilan elementtilista muistaa nyt viimeksi näytetyn elementtityypin (esim. linkit, otsikot tai kiintopisteet) samassa NVDA-istunnossa jokaisella valintaikkunan näyttökerralla. (#365)
* Useimmat Windows 8:n Metro-sovellukset (esim. Sähköposti tai Kalenteri) eivät enää aktivoi selaustilaa sovelluksen kaikissa osissa, vaan pelkästään niissä, joissa sitä tarvitaan.
* Handy Techin pistenäyttöajurin COM-palvelin päivitetty versioksi 1.4.2.0.

### Bugikorjaukset

* NVDA ei enää käsittele Windows-näppäintä virheellisesti alas painettuna, kun Windowsin lukitus avataan Windows+L-näppäinyhdistelmällä lukitsemisen jälkeen Windows Vistassa ja uudemmissa. (#1856)
* Riviotsikot tunnistetaan nyt asianmukaisesti taulukon soluiksi Adobe Readerissa, ts. koordinaatit luetaan ja niihin päästään taulukkonavigointikomennoilla. (#2444)
* Useampaan sarakkeeseen ja/tai riviin jakaantuvat taulukon solut käsitellään nyt oikein Adobe Readerissa. (#2437, #2438, #2450)
* NVDA:n jakelupaketti tarkistaa nyt eheytensä ennen suorittamista. (#2475)
* Tilapäiset lataustiedostot poistetaan, jos NVDA-päivityksen lataaminen epäonnistuu. (#2477)
* NVDA ei järjestelmänvalvojana käytettäessä enää jumiudu XP:ssä kopioitaessa käyttäjän asetuksia järjestelmäasetuksiksi (Windowsin kirjautumisikkunaa ja muita suojattuja ruutuja varten). (#2485)
* Windows 8:n aloitusnäytön ruudut esitetään nyt paremmin sekä puheena että pistenäytöllä. Nimeä ei enää toisteta, ei valittu -ilmoitusta ei enää esiinny, ja muuttuvat tilatiedot luetaan ruudun kuvauksena (esim. nykyinen lämpötila Sää-ruudulle).
* Salasanoja ei enää puhuta luettaessa salasanakenttiä Microsoft Outlookissa ja muissa normaaleissa muokkaussäätimissä, jotka on merkitty suojatuiksi. (#2021)
* Lomakekenttien muutokset näytetään nyt oikein selaustilassa Adobe Readerissa. (#2529)
* Parannuksia Microsoft Wordin kieliasun tarkistukseen, mukaan lukien kohdalla olevan kirjoitusvirheen tarkempi lukeminen sekä tuki kieliasun tarkistukselle käytettäessä NVDA:n asennettua versiota Windows Vistassa tai uudemmassa käyttöjärjestelmässä.
* Sellaiset lisäosat, jotka sisältävät tiedostoja, joiden nimissä on muita kuin ASCII-merkkejä, voidaan nyt useimmissa tapauksissa asentaa oikein. (#2505)
* Kun tekstiä päivitetään tai vieritetään, sen kieltä ei enää menetetä Adobe Readerissa. (#2544)
* Vahvistusvalintaikkuna näyttää nyt lisäosaa asennettaessa oikein sen lokalisoidun nimen, mikäli sellainen on käytettävissä. (#2422)
* Säädinten (esim. liukusäädinten) numeeristen arvojen laskeminen  on nyt korjattu UI Automation -rajapintaa käyttävissä sovelluksissa (esim. sellaisissa kuin .NET ja Silverlight). (#2417)
* Edistymispalkkien lukuasetusta noudatetaan nyt määrittelemättömille edistymispalkeille, joita NVDA näyttää asennettaessa, massamuistiversiota luotaessa jne. (#2574)
* NVDA-komentoja ei ole enää mahdollista suorittaa pistenäytöltä Windowsin suojatun ruudun (kuten lukitusruudun) ollessa aktiivisena. (#2449)
* Pistenäyttöä päivitetään nyt selaustilassa, mikäli näytettävä teksti muuttuu. (#2074)
* Suoraan NVDA:n kautta puhuvien tai pistenäytöllä tekstiä näyttävien sovellusten viestit ohitetaan oltaessa Windowsin suojatussa ruudussa, kuten lukitusnäytössä.
* Selaustilassa ei ole enää mahdollista siirtyä pois asiakirjan lopusta oikealla nuolinäppäimellä oltaessa viimeisen merkin kohdalla tai siirtymällä säilöelementin loppuun sen ollessa viimeinen kohde kyseisessä asiakirjassa. (#2463)
* Ylimääräistä sisältöä ei enää virheellisesti puhuta luettaessa valintaikkunoiden tekstiä verkkosovelluksissa (erityisesti ARIA-valintaikkunoissa, joissa ei ole aria-describedby-attribuuttia). (#2390)
* NVDA ei enää virheellisesti lue tai paikanna tiettyjä muokkauskenttiä MSHTML-asiakirjoissa (esim. Internet Explorerissa), jos verkkosivun tekijä on käyttänyt ARIA-roolia. (#2435)
* Askelpalautin-näppäin käsitellään nyt oikein Windowsin komentokonsoleissa kirjoitettuja sanoja luettaessa. (#2586)
* Solujen koordinaatit näytetään taas pistenäytöllä Microsoft Excelissä.
* NVDA ei jää enää jumiin Microsoft Wordissa luettelomuotoiluja sisältävään kappaleeseen yritettäessä liikkua vasemmalla nuolinäppäimellä tai Ctrl+Nuoli vasemmalle -näppäinyhdistelmällä luettelomerkin tai numeron päälle. (#2402)
* Tiettyjen luetteloruutujen (erityisesti ARIA-tyyppisten) kohteita ei näytetä enää virheellisesti selaustilassa Mozilla-sovelluksissa.
* Sellaiset säätimet, jotka näytettiin virheellisillä nimillä tai vain tyhjänä tilana, näytetään nyt asianmukaisilla nimillä selaustilassa Mozilla-sovelluksissa.
* Tyhjää tilaa jätetty jonkin verran huomiotta selaustilassa Mozilla-sovelluksissa.
* Sellaiset grafiikat, jotka on selkeästi merkitty esityksellisiksi alt=""-attribuutilla, ohitetaan nyt asianmukaisesti selaustilassa verkkoselaimissa.
* NVDA piilottaa nyt verkkoselaimissa sisällön, joka on merkitty ruudunlukuohjelmilta piilotetuksi (erityisesti aria-hidden-attribuuttia käytettäessä). (#2117)
* Negatiiviset rahasummat (esim. -123 $) luetaan nyt oikein miinusmerkkisinä symbolitasosta riippumatta. (#2625)
* NVDA ei enää ala jatkuva luku -toiminnon aikana käyttää oletuskieltä tilanteissa, joissa lause ei pääty pisteeseen. (#2630)
* Fontin tiedot tunnistetaan nyt oikein Adobe Reader 10.1:ssä ja uudemmissa. (#2175)
* Jos Adobe Readerissa on vaihtoehtoinen teksti saatavilla, vain se näytetään. Aiemmin näytettiin toisinaan ylimääräistä tekstiä. (#2174)
* Kun verkkosivu sisältää sovelluksen, sen sisältöä ei enää näytetä selaustilassa. Tämä estää odottamattoman sovellukseen siirtymisen sivulla liikuttaessa. Sovelluksen kanssa voidaan olla vuorovaikutuksessa samalla tavalla kuin upotetuissa objekteissa. (#990)
* Kiertopainikkeiden arvo luetaan nyt oikein sen muuttuessa Mozilla-sovelluksissa. (#2653)
* Adobe Digital Editionsin tuki päivitetty toimimaan 2.0-versiossa. (#2688)
* yhdistelmäruudussa oltaessa sen kaikkia kohteita ei enää lueta virheellisesti NVDA+Nuoli alas -näppäinyhdistelmää painettaessa Internet Explorerissa ja muissa MSHTML-asiakirjoissa. Nyt vain aktiivinen kohde luetaan. (#2337)
* Puhesanastot tallentuvat nyt oikein käytettäessä Korvattava- ja Korvaava-kentissä #-merkkiä. (#961)
* Piilotetussa sisällössä oleva näkyvä sisältö näytetään nyt oikein selaustilassa MSHTML-asiakirjoissa (esim. Internet Explorerissa). Erityisesti elementit, joissa on tyylinä visibility:visible sellaisen elementin sisässä, jossa on tyylinä visibility:hidden. (#2097)
* Windows XP:n tietoturvakeskuksen linkkien kohdalla ei enää niiden nimien jälkeen lueta satunnaista roskaa. (#1331)
* UI Automation -tekstisäätimet (esim. Windows 7:n Käynnistä-valikon hakukenttä) luetaan nyt oikein siirrettäessä hiiri niiden päälle.
* Näppäinasettelun vaihtumista ei enää ilmoiteta jatkuva luku -toiminnon aikana, mikä oli erityisen ongelmallista monikielisissä asiakirjoissa, arabialainen teksti mukaan lukien. (#1676)
* Joidenkin muokattavien UI Automation -tekstisäädinten (esim. Windows 7:n/8:n Käynnistä-valikon hakuruudun) koko sisältöä ei enää lueta joka kerta sen muuttuessa.
* Nimeämättömien ryhmien ensimmäisen ruudun nimeä ei enää lueta ryhmän nimenä liikuttaessa Windows 8:n aloitusnäytössä ryhmien välillä, mikä nopeuttaa navigointia. (#2658)
* Kohdistus sijoitetaan Windows 8:n aloitusnäyttöä avattaessa asianmukaisesti ensimmäisen ruudun kohdalle aloitusnäytön juureen siirtämisen sijasta, mikä voi sekoittaa navigointia. (#2720)
* NVDA käynnistyy nyt oikein, kun käyttäjäprofiilin hakemistopolku sisältää tiettyjä ASCII-merkistöön kuulumattomia merkkejä. (#2729)
* Välilehtien teksti näytetään nyt oikein selaustilassa Google Chromessa.
* Valikkopainikkeet luetaan nyt oikein selaustilassa.
* Laskentataulukon solujen lukeminen toimii nyt oikein OpenOffice.org/LibreOffice Calcissa. (#2765)
* NVDA toimii taas Yahoo! Mailin viestilistassa Internet Explorerista käytettäessä. (#2780)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2012.2.1

Tämä versio ratkaisee useita mahdollisia tietoturvaongelmia (päivittämällä Python versioksi 2.7.3).

## 2012.2

Tämän version tärkeimpiä uusia ominaisuuksia ovat sisäänrakennettu asennusohjelma ja massamuistiversion luonti, automaattiset päivitykset, uusien lisäosien helppo hallinta, grafiikoiden lukeminen Microsoft Wordissa, tuki Windows 8:n Metro-sovelluksille sekä useat tärkeät ohjelmavirheiden korjaukset. 

### Uudet ominaisuudet

* NVDA voi nyt tarkistaa, ladata ja asentaa päivitykset automaattisesti. (#73)
* NVDA:n toiminnallisuuden laajentaminen on tehty helpommaksi lisäosien hallinnalla (löytyy NVDA-valikosta Työkalut-valikon alta), joka mahdollistaa liitännäisiä ja ajureita sisältävien lisäosapakettien (.nvda-addon-tiedostojen) asentamisen ja poistamisen. Huomaa, että manuaalisesti asetushakemistoon kopioidut vanhemmat liitännäiset ja ajurit eivät näy lisäosien hallinnassa. (#213)
* Entistä useammat NVDA:n ominaisuudet, kuten kirjoitettujen merkkien lukeminen ja verkkosivujen selaustila, toimivat nyt Windows 8:n Metro-sovelluksissa (Internet Explorer 10:n Metro-version tuki mukaan lukien). Näiden sovellusten käyttäminen ei ole mahdollista NVDA:n massamuistiversioilla. (#1801) 
* Selaustila-asiakirjoissa (Internet Explorerissa, Firefoxissa jne) voidaan nyt siirtyä tiettyjen säilöelementtien alkuun tai loppuun (listat ja taulukot mukaan lukien) näppäimillä Shift+, (pilkku) ja , (pilkku). (#123)
* Uusi kieli: kreikka.
* Grafiikat ja alt-tekstit luetaan nyt Microsoft Word -asiakirjoissa. (#2282, #1541)

### Muutokset

* Solujen koordinaatit luetaan nyt Microsoft Excelissä solujen sisällön jälkeen vain, jos Lue taulukot ja Lue taulukon solujen koordinaatit -asetukset on otettu käyttöön Asiakirjojen muotoiluasetukset -valintaikkunassa. (#320)
* NVDA:ta jaetaan nyt yhtenä pakettina. Erillisen massamuistiversion ja asennusohjelman sijaan on vain yksi tiedosto, joka käynnistää suoritettaessa NVDA:n väliaikaisen kopion ja mahdollistaa asentamisen tai massamuistijakelun luomisen. (#1715)
* NVDA asennetaan nyt kaikissa järjestelmissä aina Program Files -hakemistoon. Myös aiempi asennus siirretään päivitettäessä automaattisesti kyseiseen hakemistoon, mikäli se on asennettu jonnekin muualle.

### Bugikorjaukset

* Kun automaattinen kielen vaihtaminen on käytössä, sellainen sisältö kuin grafiikoiden alt-teksti ja tiettyjen muiden säädinten nimet luetaan nyt Mozilla Gecko -sovelluksissa (esim. Firefoxissa) asianmukaisella kielellä, mikäli se on merkitty oikein.
* Jatkuva luku -toiminto ei enää keskeydy kappaleen keskellä BibleSeeker-sovelluksessa eikä muissa TRxRichEdit-säätimissä.
* Resurssienhallinnan tiedoston ominaisuudet -valintaikkunan Oikeudet-välilehdellä ja Windows Updatessa olevat luettelot luetaan nyt oikein Windows 8:ssa.
* Korjattu mahdollisia jumiutumisia MS Wordissa, jotka aiheutuvat siitä, kun asiakirjan tekstin (hyvin pitkien rivien tai sisällysluettelon) noutamiseen kuluu kauemmin kuin kaksi sekuntia. (#2191)
* Sanavälit tunnistetaan nyt oikein, kun tyhjätilamerkin jälkeen on tiettyjä välimerkkejä. (#1656)
* Adobe Readerissa on nyt mahdollista siirtyä selaustilassa ilman tasoja oleviin otsikoihin pikanavigointinäppäimiä ja elementtilistaa käyttäen. (#2181)
* Pistenäyttöä päivitetään nyt Winampissa asianmukaisesti, kun soittolistaeditorissa siirrytään eri kohteeseen. (#1912)
* Elementtilistan puunäkymän kokoa muutetaan nyt oikein, jotta jokaisen elementin teksti näkyy kokonaan. (#2276)
* Muokattavat tekstikentät näytetään nyt oikein pistenäytöllä Java Access Bridgeä käyttävissä sovelluksissa. (#2284)
* Muokattavissa tekstikentissä ei enää tietyissä tilanteissa lueta outoja merkkejä Java Access Bridgeä käyttävissä sovelluksissa. (#1892)
* Nykyinen rivi luetaan nyt oikein oltaessa muokattavan tekstikentän lopussa Java Access Bridgeä käyttävissä sovelluksissa. (#1892)
* Pikanavigointi toimii nyt sisennetyille lainauksille ja upotetuille objekteille selaustilassa Mozilla Gecko 14:ää ja uudempaa käyttävissä sovelluksissa (esim. Firefox 14:ssä). (#2287)
* NVDA ei enää lue häiritsevää sisältöä Internet Explorer 9:ssä kohdistuksen siirtyessä tiettyjen kiintopisteiden tai kohdistettavien elementtien sisään (erityisesti kohdistettavaan tai ARIA-kiintopisteroolin sisältävään div-elementtiin).
* NVDA:n kuvake näytetään nyt oikein työpöydän ja Käynnistä-valikon pikakuvakkeissa 64-bittisissä Windows-versioissa. (#354)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2012.1

Tämän version tärkeimpiä uusia ominaisuuksia ovat pistenäytön sujuvampi lukeminen, asiakirjan muotoilutietojen ilmaiseminen pistenäytöllä, entistä useampien muotoilutietojen lukeminen ja paranneltu suorituskykyMicrosoft Wordissa sekä tuki iTunes Storelle.

### Uudet ominaisuudet

* NVDA voi kertoa järjestyksessä nykyisen rivin alussa olevien sisennysten ja välilyöntien määrän. Asetus voidaan ottaa käyttöön Lue rivien sisennykset -valintaruudulla Asiakirjojen muotoiluasetukset -valintaikkunasta. (#373)
* NVDA havaitsee nyt vaihtoehtoisen näppäimistösyöte-emulaation, kuten ruutunäppäimistöjen ja puheentunnistusohjelmistojen tuottamat näppäinpainallukset.
* NVDA havaitsee nyt värit Windowsin komentokonsoleissa.
* Lihavointi, kursivointi ja alleviivaus ilmaistaan nyt pistenäytöllä käytettävässä pistetaulukossa määritetyillä merkeillä. (#538)
* Microsoft Word -asiakirjoissa luetaan nyt paljon enemmän tietoja, mukaan lukien:
 * Ala- ja loppuviitteiden numerot, otsikkotasot, kommentit, taulukon sisäkkäiset tasot, linkit sekä tekstin väri
 * Ilmoitus tultaessa asiakirjan eri osiin, kuten kommenttiselitteeseen, ala- ja loppuviite- sekä ylä- ja alatunnisteselitteisiin.
* Valittu teksti ilmaistaan nyt pistenäytöllä pisteillä 7 ja 8. (#889)
* Pistenäytöllä näytetään nyt tiedot asiakirjoissa olevista säätimistä, kuten linkeistä, painikkeista ja otsikoista. (#202)
* Tuki hedo ProfiLine- ja MobilLine USB -pistenäytöille. (#1863, #1897)
* NVDA välttää nyt oletusarvoisesti sanojen katkaisemista pistenäytöllä aina kun mahdollista. Asetus voidaan poistaa käytöstä Pistekirjoitusasetukset-valintaikkunassa. (#1890, #1946)
* Tekstin näyttäminen pistenäytöllä on nyt mahdollista kappaleittain, mikä mahdollistaa suurten tekstimäärien sujuvamman lukemisen. Tämä on määritettävissä Lue kappaleittain -asetuksella Pistekirjoitusasetukset-valintaikkunassa. (#1891)
* Kohdistimen alla oleva objekti voidaan aktivoida selaustilassa pistenäytöltä. Tämä tehdään painamalla kosketuskohdistinnäppäintä kohdistimen kohdalla (mikä tarkoittaa sen kahdesti painamista, mikäli kohdistin ei jo ole siinä). (#1893)
* Alkeellinen tuki iTunesin web-osioille, kuten Storelle. Mahdollisesti myös muita WebKit 1:tä käyttäviä sovelluksia tuetaan. (#734)
* Kirjojen sivuja käännetään nyt automaattisesti Adobe Digital Editions 1.8.1:ssä ja uudemmissa jatkuva luku -toimintoa käytettäessä. (#1978)
* Uusia pistetaulukoita: portugalilainen taso 2, islantilainen 8 pisteen tietokonemerkistö, tamililainen taso 1, espanjalainen 8 pisteen tietokonemerkistö, farsilainen taso 1. (#2014)
* Asiakirjojen muotoiluasetukset -valintaikkunasta on nyt mahdollista määrittää, luetaanko asiakirjaen kehykset. (#1900)
* Lepotila otetaan automaattisesti käyttöön OpenBook-sovellusta käytettäessä. (#1209)
* Kääntäjät voivat nyt Poedit-sovelluksessa lukea heitä varten lisättyjä ja automaattisesti purettuja kommentteja. Kääntämättömät tai epämääräiset ilmoitukset merkitään tähdellä sekä ilmaistaan äänimerkillä niiden kohdalle tultaessa. (#1811).
* Tuki HumanWare Brailliant BI- ja B -sarjan pistenäytöille. (#1990)
* Uusi kieli: kirjanorja.

### Muutokset

* Nykyisen merkin kuvailu- ja sanan tai rivin tavauskomennot tavaavat nyt tekstin kielen mukaisesti, mikäli automaattinen kielen vaihtaminen on käytössä ja asianmukainen kielimääritys on käytettävissä.
* eSpeak-puhesyntetisaattori päivitetty versioksi 1.46.02.
* NVDA lyhentää nyt hyvin pitkät grafiikoiden ja linkkien URL-osoitteista arvatut nimet (30 merkkiä tai enemmän), sillä ne ovat todennäköisimmin turhia ja vain haittaavat tekstin lukemista. (#1989)
* Joitakin pistenäytöllä näytettäviä tietoja on lyhennetty. (#1955, #2043)
* Kun järjestelmä- tai tarkastelukohdistin liikkuu, pistenäyttöä vieritetään nyt samalla tavalla kuin manuaalisesti vieritettäessä. Tämä on tarkoituksenmukaisempaa, kun pistenäyttö on määritetty lukemaan kappaleittain ja/tai välttämään sanojen katkaisua. (#1996)
* Päivitetty uuteen espanjalaiseen tason 1 pistetaulukkoon.
* Liblouis-pistekääntäjä päivitetty versioksi 2.4.1.

### Bugikorjaukset

* Kohdistusta ei enää siirretä Windows 8:ssa virheellisesti pois Resurssienhallinnan hakukentästä, mikä esti kyseisen kentän käytön NVDA:lla.
* Merkittäviä suorituskyvyn parannuksia luettaessa ja liikuttaessa Microsoft word -asiakirjoissa automaattisen muotoilutietojen lukemisen ollessa käytössä, ts. muotoilujen oikolukeminen on nyt jokseenkin vaivatonta. Joillakin käyttäjillä myös yleinen suorituskyky voi parantua.
* Selaustilaa käytetään nyt koko ruudun Adobe Flash -sisällölle.
* Korjattu huono äänenlaatu joissakin tapauksissa käytettäessä Microsoft Speech API version 5 puheääniä, kun äänilaitteeksi on määritetty jokin muu kuin oletusarvoisesti käytettävä Microsoft Sound Mapper. (#749)
* NVDA:n käyttäminen "Ei puhetta" -syntetisaattorilla on jälleen mahdollista. (#1963)
* Objektinavigointikomentoja käytettäessä ei enää ilmoiteta "Ei alemman tason objekteja" tai "Ei ylemmän tason objekteja", vaan käytetään ilmoituksia, jotka ovat yhdenmukaisia käyttöoppaassa mainittujen termien kanssa.
* Kun NVDA on määritetty käyttämään muuta kieltä kuin englantia, sarkain-näppäimen nimi sanotaan nyt asianmukaisesti kyseisellä kielellä.
* NVDA ei vaihda enää ajoittain selaustilaan Mozilla Gecko -sovelluksissa (esim. Firefoxissa) asiakirjan valikoissa liikuttaessa. (#2025)
* Päivitetty tulos luetaan nyt Laskin-sovelluksessa askelpalautinta painettaessa; aiemmin ei luettu mitään. (#2030)
* Siirrä hiiri navigointiobjektiin -komento siirtää nyt selaustilassa tarkastelukohdistimen kohdassa keskelle objektia vasemman yläreunan sijasta, mikä tekee siitä joissakin tilanteissa tarkemman. (#2029)
* Kohdistuksen siirtäminen työkaluriville selaustilassa vaihtaa nyt vuorovaikutustilaan, kun Automaattinen vuorovaikutustila kohdistuksen muuttuessa -asetus on käytössä. (#1339)
* Lue ikkunan nimi -komento toimii taas oikein Adobe Readerissa.
* Kun Automaattinen vuorovaikutustila kohdistuksen muuttuessa -asetus on käytössä, vuorovaikutustilaa käytetään nyt asianmukaisesti aktiivisille taulukon soluille esim. ARIA-ruudukoissa. (#1763)
* Sijaintitiedot ilmoitetaan nyt oikein tietyissä iTunesin luetteloissa.
* Joitakin linkkejä ei enää käsitellä Adobe Readerissa vain luku -tyyppisiä muokattavia tekstikenttiä sisältävinä.
* Joidenkin muokattavien tekstikenttien nimiä ei enää virheellisesti sanota  luettaessa valintaikkunassa olevaa tekstiä. (#1960)
* Ryhmien kuvaukset luetaan taas asianmukaisesti, jos objektien kuvausten lukeminen on käytössä.
* Järkevät luettavissa olevat koot sisällytetään nyt aseman ominaisuusvalintaikkunan tekstiin Resurssienhallinnassa.
* Ominaisuussivujen tekstin useaan kertaan lukeminen on estetty joissakin tilanteissa. (#218)
* Paranneltu kohdistimen seurantaa muokattavissa tekstikentissä, jotka luottavat ruudulle kirjoitettuun tekstiin. Tämä parantaa muokkaamista erityisesti Microsoft Excelin solueditorissa ja Eudoran viestimuokkaimessa. (#1658)
* Upotetuista objekteista poistuminen Siirrä selaustila-asiakirjaan -komennolla (NVDA+Ctrl+välilyönti) toimii nyt Firefox 11:ssä kuten pitääkin.
* Kun NVDA on hakemistossa, jonka nimessä on muita kuin ASCII-merkkejä, se käynnistää nyt itsensä uudelleen asianmukaisesti (esim. käytettävän kielen vaihtamisen jälkeen). (#2079)
* Pistenäyttö noudattaa oikein objektien pikanäppäinten, sijaintitietojen ja kuvausten lukuasetuksia.
* Selaus- ja vuorovaikutustilojen välillä vaihtaminen ei ole enää hidasta Mozilla-sovelluksissa pistenäyttöä käytettäessä. (#2095)
* Kohdistimen siirtäminen rivin/kappaleen lopussa olevan välilyönnin kohdalle joissakin muokattavissa tekstikentissä pistenäytön kosketuskohdistinnäppäimiä käyttäen toimii nyt oikein sen sijaan, että siirtäisi tekstin alkuun. (#2096)
* NVDA toimii taas oikein Audiologic Tts3 -syntetisaattorilla. (#2109)
* Microsoft Word -asiakirjoja käsitellään asianmukaisesti monirivisinä. Tämä saa pistenäytön toimimaan paremmin, kun asiakirja on aktiivisena.
* Internet Explorerissa ei enää ilmene virheitä siirrettäessä kohdistusta tiettyjen harvojen säädinten kohdalle. (#2121)
* Käyttäjän tekemät muutokset välimerkkien ja symbolien puhumiseen otetaan heti käyttöön sen sijaan, että tarvitsisi käynnistää NVDA uudelleen tai poistaa automaattinen kielen vaihtaminen käytöstä.
* Puhe ei enää mykisty joissakin tapauksissa NVDA:n Lokintarkastelu-sovelluksen Tallenna nimellä -valintaikkunassa eSpeakia käytettäessä. (#2145)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2011.3

Tämän version tärkeimpiä uusia ominaisuuksia ovat automaattinen puhesyntetisaattorin kielen vaihtaminen luettaessa asianmukaisen kielimäärityksen sisältäviä asiakirjoja, tuki 64-bittisille ajonaikaisille Java-ympäristöille, tekstin muotoilutietojen lukeminen selaustilassa Mozilla-sovelluksissa, parempi sovellusten kaatumisten ja jumittumisten käsittely ja alustavat Windows 8:n käyttöön liittyvät korjaukset.

### Uudet ominaisuudet

* NVDA voi nyt vaihtaa eSpeak-syntetisaattorin kieltä lennossa luettaessa tiettyjä verkkosivuja tai PDF-asiakirjoja, joissa on asianmukainen kielimääritys. Automaattinen kielen/murteen vaihtaminen voidaan ottaa käyttöön ja poistaa käytöstä Ääniasetukset-valintaikkunasta. (#845)
* NVDA tukee nyt Java Access Bridgen 2.0.2-versiota, johon sisältyy 64-bittisten ajonaikaisten Java-ympäristöjen tuki.
* Otsikkotasot sanotaan nyt objektinavigointia käytettäessä Mozilla Gecko -sovelluksissa (esim. Firefoxissa).
* Tekstin muotoilutietojen lukeminen on nyt mahdollista käytettäessä selaustilaa Mozilla Gecko -sovelluksissa (esim. Firefoxissa ja Thunderbirdissä). (#394)
* Alle- ja/tai yliviivatun tekstin havaitseminen ja ilmoittaminen on nyt mahdollista standardinmukaisissa IAccessible2-tekstisäätimissä, esim. Mozilla-sovelluksissa.
* Taulukon rivien ja sarakkeiden määrä ilmoitetaan nyt selaustilassa Adobe Readerissa.
* Lisätty tuki Microsoft Speech Platform -syntetisaattorille. (#1735)
* Sivu- ja rivinumerot ilmoitetaan nyt järjestelmäkohdistimen sijainnista IBM Lotus Symphonyssa. (#1632)
* Äänenkorkeuden muutoksen prosenttiarvo isoja kirjaimia luettaessa on nyt määritettävissä Ääniasetukset-valintaikkunasta. Tämä korvaa aiemman "Nosta äänenkorkeutta isojen kirjainten kohdalla" -asetuksen, joten jos asetus halutaan poistaa käytöstä, arvoksi on asetettava 0. (#255)
* Tekstin ja taustan väri kerrotaan nyt luettaessa solujen muotoilutietoja Microsoft Excelissä. (#1655)
* Aktivoi nykyinen navigointiobjekti -komento toimii nyt sellaisissa Java Access Bridgeä käyttävien sovellusten  säätimissä, joissa sitä on mahdollista käyttää. (#1744)
* Lisätty uusi käännös: Tamil.
* Alkeellinen tuki Design Science MathPlayerille.

### Muutokset

* NVDA käynnistää nyt itsensä uudelleen, mikäli se kaatuu.
* Joitakin pistenäytöllä näytettäviä tietoja on lyhennetty. (#1288)
* Lue aktiivinen ikkuna -skriptiä (NVDA+b) on paranneltu suodattamaan tarpeettomia säätimiä, ja lisäksi sen mykistäminen on nyt paljon helpompaa. (#1499)
* Automaattinen jatkuva luku -toiminto selaustila-asiakirjan avautuessa on nyt mahdollista poistaa käytöstä Selaustilan asetukset -valintaikkunasta löytyvällä asetuksella. (#414)
* Jos aktiivisen sovelluksen tilariviä luettaessa (pöytäkoneissa NVDA+end) ei löydy todellista tilariviobjektia, NVDA turvautuu sen sijaan näytön alimmalla rivillä olevaan tekstiin. (#649)
* NVDA pitää nyt tauon otsikoiden ja muiden lohkoelementtien lopussa sen sijaan, että lukisi ne seuraavana olevan tekstin kanssa yhtenä pitkänä lauseena luettaessa asiakirjoja selaustilassa jatkuva luku -toiminnolla.
* Kun selaustilassa painetaan Enteriä tai välilyöntiä välilehden kohdalla, se aktivoidaan sen sijaan, että siirryttäisiin vuorovaikutustilaan. (#1760)
* eSpeak-puhesyntetisaattori päivitetty versioksi 1.45.47.

### Bugikorjaukset

* NVDA  ei näytä enää luettelomerkkejä tai numerointia luetteloissa Internet Explorerissa ja muissa MSHTML-säätimissä, kun sivun tekijä on määrittänyt, ettei niitä näytetä (ts. luettelotyyli on "none"). (#1671)
* Kun NVDA jää jumiin, sen uudelleenkäynnistäminen (esim. painamalla Ctrl+Alt+n) ei enää sulje aiempaa kopiota käynnistämättä uutta.
* Askelpalauttimen tai nuolinäppäinten painaminen Windowsin komentokonsolissa ei enää aiheuta joissakin tapauksissa kummallisia tuloksia. (#1612)
* WPF- ja mahdollisesti muidenkin UI Automation -rajapintaa hyödyntävien yhdistelmäruutujen, joissa tekstin muokkaaminen ei ole mahdollista, valittu kohde ilmoitetaan nyt oikein.
* Siirtyminen taulukon otsikkoriviltä seuraavalle riville ja päinvastoin on nyt aina mahdollista selaustilassa käytettäessä siirrä seuraavalle riville- ja siirrä edelliselle riville -komentoja Adobe Readerissa. Lisäksi otsikkoriviä ei enää ilmoiteta rivi 0:ksi. (#1731)
* Selaustilassa on nyt mahdollista siirtyä taulukon tyhjiin soluihin ja niistä pois Adobe Readerissa.
* Pistenäytöllä ei enää näytetä turhia sijaintitietoja (esim. 0 / 0 taso 0).
* Kokonaistarkastelun sisältö näytetään nyt pistenäytöllä, kun se on asetettu seuraamaan tarkastelukohdistinta. (#1711)
* Tekstisäätimen tekstiä ei enää näytetä pistenäytöllä kahta kertaa joissakin tapauksissa, esim. vieritettäessä taaksepäin WordPad-asiakirjaen alusta.
* Enterin painaminen tiedostonlähetyspainikkeen kohdalla selaustilassa näyttää nyt asianmukaisesti valintaikkunan tiedoston valitsemiseksi vuorovaikutustilaan siirtymisen sijaan Internet Explorerissa. (#1720)
* Dynaamisen sisällön muutoksia, kuten esim. DOS-konsoleissa, ei enää puhuta, jos lepotila on käytössä kyseisessä sovelluksessa. (#1662)
* Alt+Nuoli ylös- ja alt+Nuoli alas -näppäinyhdistelmien käyttäytymistä paranneltu selaustilassa yhdistelmäruutuja suljettaessa ja avattaessa. (#1630)
* NVDA palautuu nyt useammista tilanteista, kuten esim. vastaamasta lakanneista sovelluksista, jotka aiemmin aiheuttivat täydellisen jumiutumisen. (#1408)
* NVDA lukee nyt Mozilla Gecko -moottoria käyttävien sovellusten (esim. Firefoxin) selaustila-asiakirjaen tietyt osat sellaisessa tilanteessa, jossa elementin tyyli on display:table. (#1373)
* NVDA ei enää lue nimisäätimiä kohdistuksen siirtyessä niiden sisään. Tämä saa loppumaan joidenkin lomakekenttien nimien kahteen kertaan lukemisen Firefoxissa (Gecko) ja Internet Explorerissa (MSHTML). (#1650)
* NVDA lukee nyt Microsoft Excelissä solun, kun siihen  on liitetty tietoa Ctrl+v:llä. (#1781)
* Adobe Readerissa ei enää lueta asiakirjasta epäolennaista tietoa siirryttäessä vuorovaikutustilassa eri sivulla olevaan säätimeen. (#1659)
* Tilanvaihtopainikkeet havaitaan ja luetaan nyt oikein selaustilassa Mozilla Gecko -sovelluksissa (esim. Firefoxissa). (#1757)
* NVDA lukee nyt oikein Resurssienhallinnan osoiterivin Windows 8:n kehittäjille tarkoitetussa esiversiossa.
* NVDA ei enää kaada Windows 8:n kehittäjille tarkoitetussa esiversiossa sellaisia sovelluksia kuin winver ja WordPad virheellisten merkkihahmokäännösten vuoksi.
* Mozilla Gecko 10 -moottoria ja uudempaa käyttävissä sovelluksissa (esim. Firefox 10:ssä) kohdistin sijoitetaan nyt selaustilassa oikein useammin ladattaessa sivua, jolla on kohdeankkuri. (#360)
* Kuvakarttojen nimet luetaan nyt selaustilassa Mozilla Gecko -sovelluksissa (esim. Firefoxissa).
* Hiiren siirtäminen tiettyjen tekstikenttien päälle (sellaisien kuin Synaptics-osoitinlaitteen asetuksissa ja SpeechLab SpeakTextissä) ei enää aiheuta sovelluksen kaatumista hiiren seurannan ollessa käytössä. (#672)
* NVDA toimii nyt oikein useiden Windows XP:n mukana toimitettujen sovellusten Tietoja-valintaikkunoissa, mukaan lukien Muistion Tietoja Muistiosta ja Tietoja Windowsista. (#1853, #1855)
* Korjattu sanoittain lukeminen Windowsin muokkaussäätimissä. (#1877)
* Muokattavasta tekstikentästä pois Siirtyminen vasemmalla/oikealla nuolella tai Page up -näppäimellä vuorovaikutustilassa oltaessa vaihtaa nyt asianmukaisesti selaustilaan, kun Automaattinen vuorovaikutustila kohdistinta siirrettäessä -asetus on käytössä. (#1733)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2011.2

Tämän version tärkeimpiä uusia ominaisuuksia ovat merkittävät välimerkkejä ja muita symboleita koskevat parannukset, mukaan lukien tasojen määrittäminen, omat nimet sekä merkkien kuvaukset, ei taukoja rivien lopussa jatkuva luku -toiminnon aikana, paranneltu ARIA-tuki Internet Explorerissa, parempi tuki XFA- ja LiveCycle PDF -asiakirjoille Adobe Readerissa, mahdollisuus lukea ruudulla olevaa tekstiä useammassa sovelluksessa sekä mahdollisuus lukea muotoilutiedot ja värit ruudulla olevasta tekstistä.

### Uudet ominaisuudet

* Nyt on mahdollista kuulla minkä tahansa merkin kuvaus painamalla kaksi kertaa nopeasti peräkkäin Lue nykyinen merkki -komentoa. Kuvakirjoituskielille, kuten perinteinen kiina, on yksi tai useampia kyseessä olevan symbolin sisältäviä esimerkkilauseita. Lisäksi Lue nykyinen sana- tai Lue nykyinen rivi -komennon kolmesti painaminen tavaa sanan/rivin käyttäen ensimmäistä näistä kuvauksista. (#55)
* Kokonaistarkastelussa näkyy nyt enemmän tekstiä sellaisissa sovelluksissa, jotka tulostavat tekstiä merkkihahmoina suoraan näytölle (esim. Mozilla Thunderbirdissä).
* Nyt on mahdollista valita välimerkkien ja muiden symbolien puhumisen taso. (#332)
* Kun välimerkkejä tai muita symboleita on useampi kuin neljä peräkkäin, niiden määrä ilmoitetaan nyt sen sijaan, että merkit luettaisiin. (#43)
* Lisätty uusia pistetaulukoita: norjalainen 8 pisteen tietokonemerkistö, etiopialainen taso 1, slovenialainen taso 1, serbialainen taso 1. (#1456)
* Puheessa ei kuulu enää epänormaalia taukoa joka rivin lopussa jatkuva luku -komentoa käytettäessä. (#149)
* NVDA kertoo nyt verkkoselaimissa, onko jokin lajiteltu (aria-sort-ominaisuuden mukaan). (#1500)
* Unicode-merkkiyhdistelmät näytetään nyt oikein pistenäytöllä. (#1505)
* Kun kohdistus siirtyy kenttäjoukon ympäröimän säädinryhmän sisään Internet Explorerissa ja muissa MSHTML-säätimissä, NVDA ilmoittaa nyt kyseisen ryhmän nimen (selitteen). (#535)
* Aria-labeledBy- ja aria-describedBy-ominaisuuksia noudatetaan nyt Internet Explorerissa ja muissa MSHTML-säätimissä.
* ARIA- ja ruudukkolistojen sekä liukusäädinten ja edistymispalkkisäädinten tukea on paranneltu Internet Explorerissa ja muissa MSHTML-sovelluksissa.
* Käyttäjät voivat nyt muuttaa välimerkkien ja muiden symbolien lukutapaa sekä tasoa, jolla ne puhutaan. (#271, #1516)
* Aktiivisen Excel-taulukon nimi ilmoitetaan nyt vaihdettaessa sitä Ctrl+Page up- tai Ctrl+Page down -näppäimillä. (#760)
* NVDA kertoo nyt Microsoft Wordissa nykyisen solun liikuttaessa taulukossa sarkain-näppäimellä. (#159)
* Asiakirjojen muotoiluasetukset-valintaikkunasta on nyt mahdollista määrittää, ilmoitetaanko taulukon solujen koordinaatit. (#719)
* NVDA havaitsee nyt ruudulla olevan tekstin muotoilun ja värin.
* NVDA kertoo nyt lukemattomat viestit Outlook Expressin, Windows Mailin ja Windows Live Mailin viestilistassa ja ilmoittaa myös, onko viestiketju suljettu tai avattu. (#868)
* eSpeakissa on nyt nopeuden tehostusasetus,  joka kolminkertaistaa puhenopeuden.
* Tuki Windows 7:n kellon päivämäärä ja aika -valintaikkunan kalenterisäätimelle. (#1637)
* Lisänäppäinyhdistelmiä MDV Lilli -pistenäytölle. (#241)
* Uusia käännöksiä: bulgaria ja albania.

### Muutokset

* Järjestelmäkohdistin siirretään nyt tarkastelukohdistimen kohdalle painamalla Siirrä kohdistus navigointiobjektiin -komentoa (pöytäkoneissa NVDA+Shift+Laskinnäppäimistön miinus, kannettavissa NVDA+Shift+askelpalautin) kaksi kertaa nopeasti peräkkäin. Tämä vapauttaa lisää näppäimiä muuhun käyttöön. (#837)
* Tarkastelukohdistimen alla olevan merkin desimaali- ja heksadesimaaliarvot luetaan nyt painamalla Lue nykyinen merkki -komentoa kolme kertaa kahden sijasta, koska kahdesti painaminen lukee merkin kuvauksen.
* eSpeak-puhesyntetisaattori päivitetty versioksi 1.45.03. (#1465)
* Asettelutaulukoita ei enää lueta Mozilla Gecko -sovelluksissa siirrettäessä kohdistusta vuorovaikutustilassa tai pois asiakirjasta.
* Selaustila toimii nyt ARIA-sovellusten sisällä olevissa asiakirjoissa Internet Explorerissa ja muissa MSHTML-säätimissä. (#1452)
* liblouis-pistekääntäjä päivitetty versioksi 2.3.0.
* Jos säätimellä on kuvaus, se luetaan nyt siirryttäessä selaustilassa sen kohdalle pikanavigoinnilla tai kohdistuksella.
* Edistymispalkit ilmoitetaan nyt selaustilassa.
* ARIA-esitysroolilla merkityt alkiot jätetään nyt pois yksinkertaisesta tarkastelutilasta ja kohdistuksesta.
* NVDA:n käyttöliittymässä ja ohjeessa viitataan näennäispuskureihin nyt selaustilana, koska suurimmalle osalle käyttäjistä "näennäispuskuri"-termi on melko mitäänsanomaton. (#1509)
* Kun omia liitännäisiä sisältäviä asetuksia kopioidaan järjestelmäprofiiliin kirjautumisikkunassa käytettäväksi jne, käyttäjää varoitetaan nyt, että se voi olla tietoturvariski. (#1426)
* NVDA:n järjestelmäpalvelu ei enää käynnistä ja sulje NVDA:ta käyttäjäsyötetyöpöydillä (esim. virtuaalityöpöydillä).
* NVDA ei enää käytä Windows XP:ssä tai Vistassa UI Automation -rajapintaa, vaikka se olisi käytettävissä. Tämän rajapinnan käyttäminen voi parantaa joidenkin uusien sovellusten saavutettavuutta, mutta XP:ssä ja Vistassa oli liian monia jumiutumisia, kaatumisia sekä yleisen suorituskyvyn heikkenemistä sitä käytettäessä. (#1437)
* Mozilla Gecko 2-moottoria tai uudempaa käyttävissä sovelluksissa (kuten Firefox 4 ja uudemmat) sivua on nyt mahdollista lukea selaustilassa ennen kuin se on latautunut kokonaan.
* NVDA kertoo nyt säilön tilan kohdistuksen siirtyessä sen sisällä olevaan säätimeen (esim. jos kohdistus siirtyy sivulla, joka yhä latautuu, NVDA ilmoittaa nyt, että se on varattu).
* NVDA:n käyttöliittymässä ja käyttöohjeessa ei objektinavigoinnista käytetä enää termejä "ensimmäinen alemman tason objekti" ja "ylemmän tason objekti", koska ne ovat sekavia monille käyttäjille.
* Joitakin alivalikon sisältäviä valikkokohteita ei enää ilmoiteta suljetuiksi.
* Lue muotoilut -skripti (NVDA+f) lukee nyt muotoilut järjestelmäkohdistimen tai -kohdistuksen sijainnin asemesta tarkastelukohdistimen sijainnista. Useimmat eivät huomaa eroa, koska tarkastelukohdistin seuraa oletusarvoisesti järjestelmäkohdistinta. Tämä antaa nyt kuitenkin käyttäjälle mahdollisuuden selvittää muotoilut tarkastelukohdistinta liikutettaessa, kuten esim. kokonaistarkastelussa.

### Bugikorjaukset

* Yhdistelmäruutujen sulkeminen selaustila-asiakirjoissa ei vaihda enää automaattisesti takaisin selaustilaan, kun vuorovaikutustila on pakotettu käyttöön näppäinyhdistelmällä NVDA+välilyönti. (#1386)
* NVDA näyttää nyt Gecko- ja MSHTML-asiakirjoissa (eli Firefoxissa ja Internet Explorerissa) oikein samalla rivillä sellaisen tekstin, joka näytettiin aiemmin eri riveillä. (#1378)
* Kun navigointiobjekti siirretään selaustila-asiakirjaan (verkkosivulle, PDF-asiakirjaan, HTML-sähköpostiviestiin) joko manuaalisesti tai kohdistusmuutoksen vuoksi pistenäytön seuratessa tarkastelukohdistinta, asiakirjan sisältö näytetään asianmukaisesti pistenäytöllä. (#1406, #1407)
* Kun välimerkkien lukeminen on poistettu käytöstä, tiettyjä välimerkkejä ei enää virheellisesti puhuta joitakin syntetisaattoreita käytettäessä. (#332)
* Sellaisten puhesyntetisaattoreiden asetusten lataaminen, jotka eivät tue puheääniasetusta (kuten Audiologic TTS 3), on jälleen mahdollista. (#1347)
* Skypen Ekstrat-valikko luetaan nyt oikein. (#648)
* Äänikoordinaattien voimakkuutta säädetään ruudun kirkkauden mukaan -valintaruudun valitsemisen Hiiriasetukset-valintaikkunasta ei pitäisi enää aiheuttaa äänimerkkien huomattavaa hidastumista liikutettaessa hiirtä ruudulla Windows Vistassa ja Windows 7:ssä, kun Aero-tehosteet ovat käytössä. (#1183)
* Kun NVDA on määritetty käyttämään kannettaville tarkoitettua näppäinasettelua, NVDA+delete-komento toimii nyt kuten käyttöohjeessa on mainittu nykyisen navigointiobjektin mittojen lukemiseen. (#1498)
* NVDA noudattaa nyt asianmukaisesti aria-selected-attribuuttia Internet Explorer -asiakirjoissa.
* Kohdistuksen tilannekohtaiset tiedot luetaan nyt NVDA:n siirtyessä selaustila-asiakirjoissa automaattisesti vuorovaikutustilaan. Jos esimerkiksi luetteloruutu tulee aktiiviseksi, se ilmoitetaan ensin ennen muita tietoja. (#1491)
* ARIA-luetteloruudut käsitellään nyt luettelokohteiden sijasta luetteloina Internet Explorerissa ja muissa MSHTML-säätimissä.
* Kun kohdistus siirtyy vain luku -tyyppiä olevaan muokattavaan tekstisäätimeen, NVDA ilmoittaa nyt sen olevan sellainen. (#1436)
* NVDA toimii nyt oikein selaustila-asiakirjoissa vain luku -tyyppiä olevissa muokattavissa tekstikentissä.
* NVDA ei enää virheellisesti siirry pois vuorovaikutustilasta, kun aria-activedescendant-ominaisuus on asetettu, esim. täydennyslistan tullessa näkyviin joissakin automaattisen täydennyksen sisältävissä säätimissä.
* Säädinten nimet ilmoitetaan nyt Adobe Readerissa kohdistusta siirrettäessä tai selaustilassa pikanavigointia käytettäessä.
* Painikkeet, linkit ja grafiikat hahmonnetaan nyt oikein XFA PDF -asiakirjoissa Adobe Readerissa.
* Kaikki elementit näytetään nyt omilla riveillään XFA PDF -asiakirjoissa Adobe Readerissa. Tämä muutos tehtiin, koska suuria osia (toisinaan jopa koko asiakirja) näytettiin ilman välejä yleisen rakenteen puutteen vuoksi.
* Korjattu ongelmia siirrettäessä kohdistusta muokattaviin tekstikenttiin tai niistä pois XFA PDF -asiakirjoissa Adobe Readerissa.
* Aktiivisen yhdistelmäruudun arvon muutokset ilmoitetaan nyt XFA PDF -asiakirjoissa Adobe Readerissa.
* Ei-standardinmukaiset yhdistelmäruudut kuten sellaiset, joilla valitaan värit Outlook Expressissä, ovat nyt saavutettavia. (#1340)
* Kielissä, joissa käytetään välilyöntiä numeroiden ryhmittelyyn ja tuhaterottimena (kuten ranska ja saksa), eri tekstiosissa olevia numeroita ei enää lueta yksittäisenä numerona. Tämä oli erityisen ongelmallista numeroita sisältävissä taulukon soluissa. (#555)
* Alkiot, joissa on ARIA-kuvausrooli, luokitellaan nyt Internet Explorerissa ja muissa MSHTML-säätimissä muuttumattomaksi tekstiksi, ei muokkauskentiksi.
* Korjattu erilaisia ongelmia painettaessa sarkainta kohdistuksen ollessa selaustila-asiakirjassa (esim. virheellinen siirtäminen osoiteriville Internet Explorerissa). (#720, #1367)
* Syöte-eleet  kirjataan lokiin näppäinohjeessa, vaikka niiden skriptit ohittaisivat sen, kuten komennot pistenäytön eteen- ja taaksepäin vierittämiseksi.
* Kun toimintonäppäintä pidetään alhaalla näppäinohjetilassa, NVDA ei enää ilmoita ikään kuin se olisi itsensä toimintonäppäin, esim. NVDA+NVDA.
* Yhdistelmäruutuihin siirtyminen toimii nyt Adobe Reader -asiakirjoissa C- ja Shift+C-pikanavigointikomennoilla.
* Valittavissa olevien taulukon rivien tila ilmoitetaan nyt samalla tavalla kuin luettelo- ja puunäkymäkohteissa.
* Firefoxin ja muiden Gecko-sovellusten säädinten aktivoiminen on nyt mahdollista selaustilassa, vaikka niiden sisältö olisi osittain poissa näytöltä. (#801)
* Asetusvalintaikkunoita ei voida enää avata niiden jumiutumisen vuoksi Kun jokin NVDA:n ilmoitus on näkyvissä. (#1451)
* Microsoft Excelissä ei ole enää viivettä pidettäessä alhaalla tai painettaessa nopeasti näppäimiä solujen välillä liikkumiseksi tai niiden valitsemiseksi.
* Korjattu NVDA:n järjestelmäpalvelun ajoittaisia kaatumisia, mikä tarkoitti, että NVDA lakkasi toimimasta suojatuissa Windows-ruuduissa.
* Korjattu ongelmia, joita ilmeni toisinaan pistenäytöillä kun jokin muutos aiheutti näytettävän tekstin katoamisen. (#1377)
* Internet Explorer 9:n latausikkunassa liikkuminen ja sen lukeminen on nyt mahdollista. (#1280)
* Useiden NVDA:n kopioiden yhtaikainen käynnistäminen  vahingossa ei ole enää mahdollista. (#507)
* NVDA ei enää virheellisesti näytä pääikkunaansa hitaissa järjestelmissä koko ajan käynnissä ollessaan. (#726)
* NVDA ei enää kaadu Windows xP:ssä WPF-sovellusta käynnistettäessä. (#1437)
* Jatkuva luku -komennot  toimivat nyt joissakin UI automation -tekstisäätimissä, jotka tukevat kaikkia tarvittavia toimintoja. (esim. tarkastelukohdistimen nykyisestä kohdasta aloittavaa jatkuva luku -komentoa on nyt mahdollista käyttää XPS-katseluohjelmassa).
* NVDA ei enää luokittele virheellisesti  joitakin Outlook Expressin ja Windows Live Mailin viestisääntöjen Käytä-valintaikkunan luettelokohteita valintaruuduiksi. (#576)
* Yhdistelmäruuduissa ei enää ilmoiteta olevan alivalikoita.
* NVDA voi nyt lukea vastaanottajat Microsoft Outlookin Vastaanottaja-, Kopio- ja Piilokopio-kentissä. (#421)
* Korjattu NVDA:n Puheäänen asetukset -valintaikkunan ongelma, joka aiheutti sen, ettei liukusäädinten arvoa aina ilmoitettu muutettaessa. (#1411)
* NVDA lukee nyt uuden solun liikuttaessa Excel-taulukossa leikkaamisen ja liittämisen jälkeen. (#1567)
* NVDA ei enää arvaa värejä sitä huonommin, mitä enemmän niitä luetaan.
* Korjattu ARIA-esitysroolilla merkittyjä upotettuja kehyksiä sisältävien sivujen lukeminen Internet Explorerissa ja muissa MSHTML-säätimissä. (#1569)
* Korjattu harvinainen ongelma, joka aiheutti loputtomasti kohdistuksen hyppimistä asiakirjan ja monirivisen muokattavan tekstikentän välillä vuorovaikutustilassa Internet Explorerissa ja muissa MSHTML-säätimissä. (#1566)
* NVDA lukee nyt vahvistusvalintaikkunat automaattisesti Microsoft Word 2010:ssä. (#1538)
* Valinta ilmoitetaan nyt oikein Internet Explorerin ja muiden MSHTML-säädinten muokattavissa monirivisissä tekstikentissä muillakin riveillä kuin ensimmäisellä. (#1590)
* Sana kerrallaan liikkumista paranneltu monissa tilanteissa, selaustila ja Windowsin muokkaussäätimet mukaan lukien. (#1580)
* NVDA:n asennusohjelma ei näytä enää lukukelvotonta tekstiä Windows Vistan ja Windows 7:n hongkongilaisissa versioissa. (#1596)
* SAPI 5 -syntetisaattorin lataaminen ei enää epäonnistu, jos asetukset sisältävät sen määrityksiä, mutta joista puheääniasetus puuttuu. (#1599)
* NVDA ei enää hidastu tai jää jumiin Internet Explorerin ja muiden MSHTML-säädinten muokattavissa tekstikentissä, kun pistenäyttö on käytössä.
* NVDA ei enää jätä huomiotta Firefoxin selaustilassa sisältöä, joka on kohdistettavan alkion sisässä, jossa on ARIA-esitysrooli.
* Ensimmäisen sivun jälkeisillä sivuilla olevat rivit luetaan nyt oikein Microsoft Wordissa, kun pistenäyttö on käytössä. (#1603)
* Oikealta vasemmalle luettavaa tekstiä sisältäviä rivejä on jälleen mahdollista lukea Microsoft Word 2003:ssa, kun pistenäyttö on käytössä. (#627)
* Jatkuva luku -komento toimii nyt oikein Microsoft Wordissa, kun asiakirjan lopussa ei ole lauseen päättävää merkkiä.
* Kun pelkkää tekstiä sisältävä viesti avataan Windows Live Mail 2011:ssä, NVDA siirtää kohdistuksen asianmukaisesti siihen, mikä mahdollistaa sen lukemisen.
* NVDA ei enää jumiudu tai lakkaa puhumasta tilapäisesti Windows Live Mailin Siirrä- tai Kopioi-valintaikkunassa. (#574)
* NVDA SEURAA NYT KOHDISTUSTA ASIANMUKAISESTI Outlook 2010:N viestilistassa. (#1285)
* Ratkaistu joitakin MDV Lilli -pistenäytön USB-yhteyden ongelmia. (#241)
* Selaustilassa ei jätetä enää tietyissä tapauksissa välilyöntejä huomiotta (esim. linkin jälkeen) Internet explorerissa ja muissa MSHTML-säätimissä.
* Jätetty huomiotta joitakin ylimääräisiä rivinvaihtoja selaustilassa internet Explorerissa ja muissa MSHTML-säätimissä. Erityisesti HTML-elementit, joissa on None-näyttötyyli, eivät enää aiheuta pakotettua rivinvaihtoa. (#1685)
* Jos NVDA ei pysty käynnistymään, Windowsin kriittisen pysähdyksen äänen toistaminen ei enää aiheuta lokitiedostoon kriittisen virheen ilmoitusta.

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2011.1.1

Tämä versio korjaa muutamia versiosta 2011.1 löydettyjä tietoturva- ja muita merkittäviä ongelmia.

### Bugikorjaukset

* NVDA-valikon Lahjoita-vaihtoehto on nyt poissa käytöstä kirjautumisikkunassa ja muissa suojatuissa ruuduissa, sillä se on tietoturvariski. (#1419)
* Kopioiminen, leikkaaminen ja liittäminen on nyt estetty suojatulla työpöydällä (kirjautumisikkunassa ja muissa suojatuissa ruuduissa), sillä se on tietoturvariski. (#1421)
* Siirrä näennäispuskuriin -komento (NVDA+Ctrl+välilyönti) toimii nyt Firefox 4:ssa kuten pitääkin poistuttaessa upotetuista objekteista, kuten Flash-sisällöstä. (#1429)
* Kun komentonäppäinten lukeminen on otettu käyttöön, Shift-näppäimen kanssa painettuja merkkejä ei enää virheellisesti  sanota komentonäppäimiksi. (#1422)
* Kun komentonäppäinten lukeminen on otettu käyttöön, välilyönnin painaminen yhdessä muiden muokkausnäppäinten kuin Vaihdon kanssa (kuten Ctrl ja Alt) ilmoitetaan nyt komentonäppäimeksi. (#1424)
* Lokiin tallentaminen on nyt kokonaan poissa käytöstä kirjautumisikkunassa ja muissa suojatuissa ruuduissa, koska se on tietoturvariski. (#1435)
* Syöte-eleet kirjataan nyt käyttöohjeen mukaisesti lokiin näppäinohjetilassa, vaikka niitä ei olisikaan määritelty mihinkään komentoon. (#1425)

## 2011.1

Tämän version tärkeimpiä uusia ominaisuuksia ovat automaattinen uuden tekstin lukeminen mIRC-, PuTTY-, Tera Term- ja SecureCRT-sovelluksissa, tuki yleisliitännäisille, luettelomerkkien ja numeroinnin lukeminen Microsoft Wordissa, lisänäppäinkomennot pistenäytöille, mukaan lukien näppäimet seuraavalle ja edelliselle riville siirtymiseksi, tuki useille Baum-, HumanWare- ja APH-pistenäytöille sekä joidenkin säädinten värien ilmoittaminen, esim. IBM Lotus Symphonyn tekstisäätimissä.

### Uudet ominaisuudet

* Värien ilmoittaminen on nyt mahdollista joissakin säätimissä. Automaattinen lukeminen voidaan määrittää Asiakirjojen muotoiluasetukset -valintaikkunasta. Värit on mahdollista lukea myös tekstin muotoilutietojen lukukomennolla (NVDA+f).
 * Tätä tuetaan alustavasti standardinmukaisissa muokattavissa IAccessible2-tekstisäätimissä (sellaisissa kuin Mozilla-sovelluksissa), RichEdit-säätimissä (sellaisissa kuin WordPadissa) ja IBM Lotus Symphonyn tekstisäätimissä.
* Näennäispuskureissa on nyt mahdollista valita tekstiä sivu kerrallaan (näppäimillä Shift+Page down ja Shift+Page up) sekä kappale kerrallaan (näppäimillä Shift+Ctrl+Nuoli alas ja Shift+Ctrl+Nuoli ylös). (#639)
* NVDA lukee nyt automaattisesti näytölle tulevan uuden tekstin mIRC:issä, PuTTY:ssä, Tera Termissä ja SecureCRT:ssä. (#936)
* Uusien näppäinkomentojen lisääminen tai  olemassa olevien muuttaminen on nyt mahdollista  kaikille NVDA:n komennoille käyttäjän syöte-elekartan avulla. (#194)
* Tuki yleisliitännäisille, joiden avulla NVDA:han on mahdollista  lisätä toimintoja, jotka ovat käytettävissä kaikissa sovelluksissa. (#281)
* Pieniä kirjaimia kirjoitettaessa Shift-näppäin pohjassa kuuluu nyt äänimerkki Capslockin ollessa käytössä. Tämä asetus voidaan poistaa käytöstä Näppäimistöasetukset-valintaikkunasta. (#663)
* Pakotetut sivunvaihdot luetaan nyt Microsoft Wordissa rivi kerrallaan liikuttaessa. (#758)
* Luettelomerkit ja numeroinnit luetaan nyt Microsoft Wordissa rivi kerrallaan liikuttaessa. (#208)  
* Lisätty komento NVDA+Shift+s, joka ottaa käyttöön tai poistaa käytöstä lepotilan nykyisessä sovelluksessa. Tämä toiminto, joka  tunnettiin aiemmin puhuvan sovelluksen tilana, poistaa käytöstä kaikki NVDA:n ruudunlukutoiminnot aktiivisessa sovelluksessa. Tästä on hyötyä sellaisissa sovelluksissa, joissa on oma puhe- tai ruudunlukuominaisuus. Unitila poistetaan käytöstä painamalla samaa näppäinkomentoa uudelleen.
* Joitakin uusia pistenäyttöjen näppäinkomentoja on lisätty. Katso tarkempia tietoja käyttöohjeen Tuetut pistenäytöt -kappaleesta. (#209)
* Kolmannen osapuolen kehittäjien mukavuuden vuoksi sovellusmoduulit sekä yleisliitännäiset on nyt mahdollista ladata uudelleen ilman NVDA:n uudelleenkäynnistystä. Tähän käytetään NVDA-valikon Työkalut-alivalikosta löytyvää Lataa liitännäiset uudelleen -vaihtoehtoa tai näppäinkomentoa NVDA+Ctrl+f3. (#544)
* NVDA muistaa nyt kohdan, jossa oltiin aiemmin vieraillulle verkkosivulle palattaessa. Tämä pätee siihen asti kunnes joko selain tai NVDA suljetaan. (#132)
* Handy Tech -pistenäyttöjä on nyt mahdollista käyttää asentamatta yleisajuria. (#854)
* Tuki useille Baum-, HumanWare- ja APH-pistenäytöille. (#937)
* NVDA tunnistaa nyt Media Player Classic Home Cinema -mediasoittimen tilarivin.
* Freedom Scientificin Focus 40 Blue -pistenäytön käyttäminen bluetooth-yhteydellä on nyt mahdollista. (#1345)

### Muutokset

* Sijaintitietoja ei enää oletusarvoisesti lueta  joissakin sellaisissa tapauksissa, joissa ne ovat yleensä virheellisiä, esim. useimmissa valikoissa, käynnissä olevien sovellusten palkissa, ilmoitusalueella jne. Toiminto voidaan ottaa kuitenkin uudelleen käyttöön Objektien lukuasetukset -valintaikkunassa olevalla asetuksella.
* Näppäinohjeen uusi nimi on englanninkielisessä käyttöliittymässä syöteohje, koska se käsittelee muistakin syötelaitteista kuin näppäimistöltä annettavia komentoja.
* Komennon sijaintia NVDA:n koodissa ei enää sanota näppäinohjeessa, koska se ei ole tärkeää käyttäjälle. Tieto tästä kirjataan kuitenkin lokiin kehittäjiä ja edistyneitä käyttäjiä varten.
* Kun NVDA havaitsee jääneensä jumiin, NVDA-näppäinten käsittelyä jatketaan, vaikka kaikki muut näppäimet välitetäänkin suoraan Windowsin käsiteltäväksi. Tämä estää käyttäjää NVDA-näppäintä painaessaan ottamasta tahattomasti käyttöön esim. Caps Lockia. (#939)
* Jos näppäimiä pidetään alhaalla Ohita seuraava näppäinpainallus -komennon jälkeen, kaikki näppäimet (toistuvat painallukset mukaan lukien) välitetään Windowsille, kunnes viimeinen näppäin vapautetaan.
* Myös kaikki toistuvat näppäinpainallukset välitetään nyt Windowsin käsiteltäväksi, mikäli NVDA-näppäintä painetaan nopeasti kaksi kertaa peräkkäin ja kun sitä pidetään alhaalla toisella painalluksella.
* Äänenvoimakkuuden lisäys ja vähennys- sekä mykistysnäppäimet  ilmoitetaan nyt näppäinohjeessa.

### Bugikorjaukset

* Kun puhesanastoon lisätään uusi merkintä, valintaikkunan nimi on nyt "Lisää sanastomerkintä" aiemman "Muokkaa sanastomerkintää" -nimen sijasta. (#924)
* Puhesanastovalintaikkunoiden sanastomerkintälistan Sääntölauseke - ja Sama kirjainkoko-sarakkeiden sisältö  näytetään nyt NVDA:ssa määritetyllä kielellä sen sijaan, että ne näytettäisiin aina englanniksi.
* Sijaintitiedot luetaan nyt AIM-pikaviestimen puunäkymissä.
* Ääniasetukset-valintaikkunan liukusäätimissä Nuoli ylös/Page up/Home suurentavat nyt asetusta ja Nuoli alas/Page down/End pienentävät. Aiemmin tapahtui juuri päinvastoin, mikä ei ollut loogista ja oli lisäksi ristiriidassa syntetisaattorin asetusrenkaan kanssa. (#221)
* Näennäispuskureissa ei enää näytetä ylimääräisiä tyhjiä rivejä, kun ruutuasettelu on poistettu käytöstä.
* Jos NVDA-näppäintä painetaan kaksi kertaa nopeasti, mutta mitään muuta näppäintä ei paineta sen jälkeen, sen toista painallusta ei enää huomioida.
* Välimerkkinäppäimet sanotaan nyt näppäinohjeessa, vaikka välimerkkien puhuminen on poistettu käytöstä. (#977)
-  Näppäinasetteluiden nimet näppäimistöasetukset-valintaikkunassa näytetään nyt NVDA:ssa määritetyllä kielellä sen sijaan, että ne näytettäisiin aina englanniksi. (#558)
* Korjattu ongelma, joka aiheutti sen, että jotkin kohteet näytettiin tyhjinä Adobe Reader -asiakirjoissa, esim. sisällysluettelon linkit Apple iPhone iOS 4.1 -käyttöohjeessa.
* NVDA:n Yleiset asetukset -valintaikkunan "Käytä tallennettuja asetuksia kirjautumisikkunassa ja muissa suojatuissa ruuduissa" -painike toimii nyt, mikäli sitä on käytetty heti NVDA:n asennuksen jälkeen, mutta ennen kuin mikään suojattu ruutu on tullut näkyviin. NVDA ilmoitti aiemmin, että asetusten kopiointi onnistui, vaikka tosiasiassa ei tapahtunut mitään. (#1194)
* Kahta NVDA:n asetusvalintaikkunaa ei voi enää olla auki samanaikaisesti. Tämä korjaa ongelmia, jotka aiheuttivat yhden avoimen valintaikkunan riippuvuutta toisesta, esim. syntetisaattorin vaihtaminen samaan aikaan kun Ääniasetukset-valintaikkuna on auki. (#603)
* NVDA:n Yleiset asetukset -valintaikkunan "Käytä tallennettuja asetuksia kirjautumisikkunassa ja muissa suojatuissa ruuduissa" -painike ei enää toimi virheellisesti Käyttäjätilien valvonnan kehotteen ilmestymisen jälkeen järjestelmissä, joissa Käyttäjätilien valvonta on käytössä, mikälikäyttäjätilin nimessä on välilyönti. (#918)
* NVDA käyttää nyt Internet Explorerissa ja muissa MSHTML-säätimissä  linkin nimen selvittämiseen viimeisenä keinona URL-osoitetta sen sijaan, että näyttäisi tyhjiä linkkejä. (#633)
* NVDA ei enää ohita  kohdistusta AOL Instant Messenger 7:n valikoissa. (#655)
* Virheiden asianmukaiset nimet luetaan nyt Microsoft Wordin Kieliasun tarkistus -valintaikkunassa (esim. ei ole sanastossa, kielioppivirhe, välimerkit). Aiemmin kaikkia sanottiin kielioppivirheiksi. (#883)
* Microsoft Wordissa kirjoittamisen ei pitäisi enää aiheuttaa tekstisotkua pistenäyttöä käytettäessä. Lisäksi on korjattu harvinainen jumiutuminen painettaessa pistenäytön kosketuskohdistinnäppäintä Word-asiakirjoissa. (#1212) Rajoituksena kuitenkin on, että pistenäyttöä käytettäessä ei voida enää lukea arabiankielistä tekstiä Word 2003:ssa ja sitä vanhemmissa. (#627)
* Kun muokkauskentässä painetaan Delete-näppäintä, tekstin/kohdistimen pitäisi nyt aina päivittyä asianmukaisesti näyttääkseen muutoksen. (#947)
* Dynaamisten sivujen muutokset käsitellään nyt oikein NVDA:ssa Gecko 2 -asiakirjoissa (eli Firefox 4:ssa) useiden välilehtien ollessa avoimina. Aiemmin vain ensimmäisen välilehden muutokset käsiteltiin. (Mozillan virhe 610985)
* NVDA lukee nyt oikein kielioppi- ja välimerkkivirheiden ehdotukset Microsoft Wordin Kieliasun tarkistus -valintaikkunassa. (#704)
* NVDA ei enää näytä Internet Explorerissa ja muissa MSHTML-säätimissä ankkurin kohteita tyhjinä linkkeinä näennäispuskurissaan, vaan ne ovat piilotettuja kuten pitääkin. (#1326)
* Objektinavigointi toimii nyt oikein ryhmäruuduissa ja niiden välillä.
* NVDA ei jää Firefoxissa ja muissa Gecko-pohjaisissa asiakirjoissa enää jumiin alikehykseen, mikäli sen lataaminen päättyy ennen sen asiakirjan lataamista, jossa ollaan.
* NVDA  lukee nyt oikein seuraavana olevan merkin, kun kohdalla oleva merkki poistetaan laskinnäppäimistön Delete-näppäimellä. (#286)
* Käyttäjänimi luetaan jälleen Windows XP:n kirjautumisikkunassa valittua käyttäjää vaihdettaessa.
* Korjattu ongelmia luettaessa tekstiä Windowsin komentokonsoleissa  rivinumeroiden lukemisen ollessa käytössä.
* Elementtilista-valintaikkuna on nyt näkevien käytettävissä. Kaikki säätimet näkyvät ruudulla. (#1321)
* Puhesanasto-valintaikkunan sanastomerkinnät  ovat nyt luettavampia näkeville käyttäjille. Luettelo on nyt riittävän suuri, jotta kaikki sen sarakkeet näkyvät ruudulla. (#90)
* NVDA ei enää jätä huomiotta ALVA BC640- ja BC680-pistenäytön näppäimiä, joita painetaan edelleen jonkin muun näppäimen vapauttamisen jälkeen.
* Adobe Reader 10 ei enää kaadu sen jälkeen, kun koodattujen asiakirjaen asetuksista poistutaan ennen käsittelyvalintaikkunan ilmestymistä. (#1218)
* NVDA vaihtaa nyt asianmukaiseen pistenäyttöajuriin tallennettuja asetuksia palautettaessa. (#1346)
* Visual Studio 2008:n ohjattu projektin luontitoiminto luetaan taas oikein. (#974)
* NVDA ei enää lakkaa täysin toimimasta sovelluksissa, joiden tiedostonimissä on muita kuin ASCII-merkkejä. (#1352)
* NVDA ei enää lue seuraavan rivin ensimmäistä merkkiä nykyisen rivin lopussa luettaessa tekstiä rivi kerrallaan AkelPad-tekstieditorissa automaattisen rivityksen ollessa käytössä.
* NVDA ei enää lue koko tekstiä jokaisen kirjoitetun merkin jälkeen Visual Studio 2005:n ja 2008:n koodieditorissa. (#975)
* Korjattu ongelma, joka aiheutti sen, että joitakin pistenäyttöjä ei tyhjennetty asianmukaisesti kun NVDA suljettiin tai käytettävää pistenäyttöä vaihdettiin.
* Alkuperäistä kohdistusta ei enää lueta ajoittain kahta kertaa NVDA:n käynnistyessä. (#1359)

### Muutokset kehittäjille

Katso muutokset tämän dokumentin [englanninkielisestä versiosta.](../en/changes.html)

## 2010.2

Tämän version merkittävimpiä uusia ominaisuuksia ovat huomattavasti yksinkertaistettu objektinavigointi, näennäispuskurit Flash-sisällölle, monien aiemmin esteellisten säädinten käyttäminen ruudun tekstiä kaappaamalla, kokonaistarkastelu ruudulla olevalle tekstille, tuki IBM Lotus Symphony -asiakirjoille, taulukon rivien ja sarakkeiden otsikoiden lukeminen Mozilla Firefoxissa sekä huomattavasti parannellut käyttöohjeet.

### Uudet ominaisuudet

* Tarkastelukohdistimella liikkumista objekteissa on yksinkertaistettu huomattavasti. Tarkastelukohdistin jättää nyt pois objektit, joista ei ole hyötyä käyttäjälle, esim. vain asettelutarkoituksiin käytettävät ja sellaiset, jotka eivät ole käytettävissä.
* Tekstisäädinten muotoilutietojen lukeminen on nyt mahdollista Java Access Bridgeä käyttävissä sovelluksissa, openOffice mukaan lukien. (#358, #463)
* NVDA lukee Solut oikein Microsoft Excelissä, kun hiiri siirretään niiden päälle.
* Java Access Bridgeä käyttävien sovellusten valintaikkunoiden teksti luetaan nyt automaattisesti valintaikkunoiden tullessa näkyviin. (#554)
* Näennäispuskurin käyttäminen Flash -sisällössä liikkumiseen on nyt mahdollista. Objektinavigointia ja suoraa vuorovaikutusta säädinten kanssa vuorovaikutustilaa käyttäen tuetaan edelleen. (#453)
* Eclipse-kehitysympäristön muokattavat tekstisäätimet koodieditori mukaan lukien ovat nyt saavutettavia. Käytössä on oltava Eclipse 3.6 tai uudempi. (#256, #641)
* NVDA voi nyt lukea suurimman osan näytöllä olevasta tekstistä. (#40, #643)
 * Tämä mahdollistaa sellaisten säädinten lukemisen, jotka eivät välitä tietoja suoremmilla ja luotettavammilla tavoilla.
 * Tämä ominaisuus tekee saavutettaviksi mm. jotkin kuvakkeita sisältävät valikkokohteet (esim. Windows XP:n Avaa sovelluksessa -valikko) (#151), Windows Live -sovellusten muokattavat tekstikentät (#200), Outlook Expressin virheluettelo (#582), TextPadin muokattava tekstisäädin (#605), Eudoran luettelot, monet Australian E-tax:in säädint ja Microsoft Excelin kaavarivi.
* Tuki Microsoft Visual Studio 2005:n ja 2008:n koodieditorille. Vaaditaan vähintään Visual Studio Standard, ei toimi Express-versioissa. (#457)
* Tuki IBM Lotus Symphony -asiakirjoille.
* Kokeellinen tuki Google Chromelle. Huomaa, ettei Chromen ruudunlukuohjelmatuki ole läheskään valmis, ja että NVDA:ssakin saattavat lisätoimet olla tarpeen. Tämän kokeilemiseksi tarvitaan Chromen uusin kehitysversio.
* Caps lock-, num lock- ja scroll lock -näppäinten tila näytetään nyt pistenäytöllä niitä painettaessa. (#620)
* Ohjeselitteet näytetään nyt pistenäytöllä niiden tullessa näkyviin. (#652)
* Lisätty ajuri MDV Lilli -pistenäytölle. (#241)
* Uusi valinta luetaan nyt Microsoft Excelissä, kun koko rivi tai sarake valitaan pikanäppäimillä Shift+välilyönti tai Ctrl+välilyönti. (#759)
* Taulukon rivien ja sarakkeiden otsikoiden lukeminen on nyt mahdollista. Asetus on määritettävissä Asiakirjojen muotoiluasetukset -valintaikkunasta.
 * Tätä tuetaan toistaiseksi vain Mozilla-sovelluksissa (Firefox 3.6.11 tai uudempi ja Thunderbird 3.1.5 tai uudempi). (#361)
* Otettu käyttöön kokonaistarkastelun komennot: (#58)
 * NVDA+Laskinnäppäimistön 7: siirtää kokonaistarkasteluun ja sijoittaa tarkastelukohdistimen nykyisen objektin kohdalle, mikä mahdollistaa koko ruudun tai asiakirjan lukemisen tekstintarkastelukomennoilla.
 * NVDA+Laskinnäppäimistön 1: siirtää tarkastelukohdistimen sen kohdalla olevan tekstin sisältävään objektiin, mikä mahdollistaa objekti kerrallaan liikkumisen kyseisestä kohdasta lähtien.
* NVDA:n nykyiset asetukset voidaan kopioida suojatuissa ruuduissa käytettäväksi (esim. kirjautumisikkuna ja käyttäjätilien valvonnan kehotteet) painamalla Yleiset asetukset -valintaikkunassa olevaa painiketta.
* Tuki Mozilla Firefox 4:lle.
* Tuki Internet Explorer 9:lle.

### Muutokset

* Navigointiobjektia käyttävä jatkuva luku -komento (NVDA+Laskinnäppäimistön plus) sekä seuraavaan ja edelliseen objektipuun objektiin siirtävät komennot (NVDA+Shift+Laskinnäppäimistön 6, NVDA+Shift+Laskinnäppäimistön 4) on poistettu virheiden vuoksi ja näppäinten vapauttamiseksi muita ominaisuuksia varten.
* NVDA:n Syntetisaattori-valintaikkunassa näytetään nyt vain syntetisaattorin näyttönimi. Aiemmin etuliitteenä näytettiin käytettävän ajurin nimi, josta ei ole hyötyä normaalikäyttäjälle.
* Upotetuista sovelluksista ja sisäkkäisistä näennäispuskureista (esim. Flash) voidaan nyt siirtyä pois ja takaisin asiakirjaan (esim. verkkosivulle), jossa ne ovat painamalla NVDA+Ctrl+välilyönti. Aiemmin tähän käytettiin näppäinyhdistelmää NVDA+välilyönti, jota käytetään nyt vain näennäispuskureiden selaus- ja vuorovaikutustilojen välillä vaihtamiseen.
* Jos kohdistus siirtyy puheentarkasteluikkunaan (otetaan käyttöön Työkalut-valikosta) esim. siksi, että sitä napsautettiin hiirellä, ikkunaan ei ilmesty uutta tekstiä ennen kuin kohdistus siirtyy siitä pois. Tämä mahdollistaa helpomman tekstin valitsemisen esim. kopiointia varten.
* Lokinkatselu- ja Python-konsoli-ikkunat suurennetaan avattaessa.
* Kun Microsoft Excelissä on työkirja aktiivisena ja kun useampi kuin yksi solu on valittuna, valinnan alue luetaan, eikä vain aktiivista solua. (#763)
* NVDA:n asetusten tallentaminen ja tiettyjen asetusten muuttaminen on nyt estetty kirjautumisikkunassa, käyttäjätilien valvonnan kehotteissa ja muissa suojatuissa ruuduissa.
* eSpeak-puhesyntetisaattori päivitetty versioksi 1.44.03.
* Jos NVDA on jo käynnissä, työpöydällä olevan NVDA-pikakuvakkeen avaaminen (Ctrl+Alt+N-näppäinyhdistelmän painaminen mukaan lukien) käynnistää sen uudelleen.
* Hiiriasetukset-valintaikkunan Lue hiiren alla oleva teksti -valintaruutu korvattu Käytä hiiren seurantaa -valintaruudulla, joka sopii paremmin yhteen hiiren seurannan päälle ja pois kytkevän NVDA+M-komennon kanssa.
* Päivitetty kannettavien tietokoneiden näppäinasettelua niin, että se sisältää kaikki pöytäkoneilla käytettävissä olevat komennot ja että se toimii oikein muillakin kuin englanninkielisillä näppäimistöillä. (#798, #800)
* Merkittäviä parannuksia ja päivityksiä käyttöohjeisiin, mukaan lukien kannettavien tietokoneiden komentojen kuvailu ja näppäinkomentojen pikaoppaan päivittäminen niin, että se sisältää samat komennot kuin käyttöohjekin. (#455)
* Liblouis-pistekääntäjä päivitetty versioksi 2.1.1. Tämä päivitys korjaa joitakin kiinalaiseen pistekirjoitukseen sekä käännöstaulukossa määrittelemättömiin merkkeihin liittyviä ongelmia. (#484, #499)

### Bugikorjaukset

* µTorrentin torrent-luettelon aktiivista kohtaa ei enää lueta toistuvasti eikä kohdistus enää siirry siihen valikon ollessa auki.
* Torrentin sisältölistan tiedostojen nimet luetaan nyt µTorrentissa.
* Kohdistus tunnistetaan nyt oikein Mozilla-sovelluksissa siirryttäessä tyhjään taulukkoon tai puunäkymään.
* Valittavissa olevien säädinten, kuten valittavien taulukon solujen, ei valittu -tila ilmoitetaan nyt oikein Mozilla-sovelluksissa. (#571)
* Asianmukaisesti toteutettujen ARIA-valintaikkunoiden tekstiä ei enää ohiteta Mozilla-sovelluksissa, vaan se luetaan kyseisten valintaikkunoiden tullessa näkyviin. (#630)
* ARIA:n taso-attribuuttia noudatetaan nyt oikein Internet Explorerissa ja muissa MSHTML-säätimissä.
* ARIA:n rooli valitaan nyt muiden tyyppitietojen sijasta virheettömämmän ja odotustenmukaisemman ARIA-kokemuksen antamiseksi Internet Explorerissa ja muissa MSHTML-säätimissä.
* Korjattu harvinainen kaatuminen Internet Explorerissa liikuttaessa tavallisten tai sisäisten kehysten välillä.
* Oikealta vasemmalle luettavia rivejä (kuten arabialaista tekstiä) voidaan jälleen lukea Microsoft Word -asiakirjoissa. (#627)
* Vähennetty merkittävästi hidastumista 64-bittisissä järjestelmissä, kun Windowsin komentokonsolissa näytetään suurta määrää tekstiä. (#622)
* Jos Skype on jo käynnissä, sitä ei enää tarvitse käynnistää uudelleen saavutettavuustuen käyttöönottamiseksi, kun NVDA käynnistyy. Tämä saattaa päteä myös muihin järjestelmän ruudunlukijalipun tarkistaviin sovelluksiin.
* NVDA ei enää kaadu Microsoft Office -sovelluksissa painettaessa NVDA+B (lue aktiivinen ikkuna) tai liikuttaessa joissakin työkalurivien objekteissa. (#616)
* Korjattu sellaisten lukujen väärin lukeminen, joissa on erottimen jälkeinen 0, esim. 1,023. (#593)
* Adobe Acrobat Pro ja Reader 9 eivät enää kaadu tiedostoa suljettaessa tai tiettyjä muita tehtäviä suoritettaessa. (#613)
* Kaiken tekstin valitseminen ilmoitetaan nyt painettaessa Ctrl+A joissakin muokattavissa tekstisäätimissä kuten Microsoft Wordissa. (#761)
* Tekstiä ei enää virheellisesti valita Scintilla-säätimissä (esim. Notepad++:ssa) NVDA:n siirtäessä järjestelmäkohdistinta esim. jatkuva luku -toiminnon aikana tai siirrettäessä kohdistinta samaan paikkaan, jossa pistenäytöllä ollaan. (#746)
* Microsoft Excelin solujen sisällön tarkasteleminen tarkastelukohdistimella on jälleen mahdollista.
* NVDA voi jälleen lukea riveittäin tiettyjä ongelmallisia tekstikenttiä Internet Explorer 8:ssa. (#467)
* Windows Live Messenger 2009 ei enää sulkeudu heti käynnistyttyään NVDA:n ollessa käynnissä. (#677)
* Sarkaimen painaminen ei ole enää tarpeen internet-selaimissa  upotettuun objektiin siirtymiseksi (esim. Flash), kun on painettu Enteriä kyseisen objektin kohdalla tai palattu toisesta sovelluksesta. (#775)
* Pitkien rivien alkua ei enää katkaista Scintilla-säätimissä (esim. Notepad++:ssa), jos ne eivät sovi kokonaan ruudulle. Lisäksi tällaiset rivit näytetään nyt oikein pistenäytöllä, kun ne valitaan.
* Yhteystietoluettelon käyttäminen on nyt mahdollista Loudtalksissa.
* URL-osoitetta ja "MSAAHTML Rekisteröityä Käsittelijää" ei enää turhaan ilmoiteta Internet Explorerissa ja muissa MSHTML-säätimissä. (#811)
* Eclipse-kehitysympäristön puunäkymäsäätimissä ei enää virheellisesti lueta aiempaa aktiivista kohtaa kohdistuksen siirtyessä uuteen.
* NVDA toimii nyt oikein järjestelmässä, jossa nykyinen työhakemisto on poistettu DLL-hakupolusta (asettamalla CWDIllegalInDllSearch-rekisterimerkinnän arvoksi 0xFFFFFFFF). Huomaa, että useimmille käyttäjille tällä ei ole merkitystä. (#907)
* Kun taulukossa liikkumiseen tarkoitettuja komentoja käytetään Microsoft Wordissa muualla kuin taulukossa, "ei taulukossa" -ilmoituksen jälkeen ei enää sanota "taulukon reuna". (#921)
* Kun Microsoft Wordissa ollaan taulukon reunassa, eivätkä taulukossa liikkumiseen tarkoitetut komennot voi siirtää mihinkään, "taulukon reuna" -ilmoitus sanotaan nyt NVDA:ssa määritetyllä kielellä sen sijaan, että se sanottaisiin aina englanniksi. (#921)
* Viestisääntöluetteloiden valintaruutujen tilat luetaan nyt Outlook Expressissä, Windows Mailissa ja Windows Live Mailissa. (#576)
* Viestisääntöjen kuvausten lukeminen on nyt mahdollista Windows Live Mail 2010:ssä.

### 2010.1

Tämä versio keskittyy pääasiassa virheiden korjaamiseen ja käyttökokemuksen parantamiseen, mukaan lukien muutamia huomattavia vakauteen liittyviä korjauksia.

#### Uudet ominaisuudet

* NVDA käynnistyy nyt järjestelmissä, joissa ei ole äänilaitteita. Tietojen tulostamiseen on tällöin käytettävä pistenäyttöä tai Silence-syntetisaattoria yhdessä puheentarkastelutoiminnon kanssa. (#425)
* Asiakirjojen muotoilu -valintaikkunaan on lisätty "Lue kiintopisteet" -valintaruutu, jolla voidaan määrittää, lukeeko NVDA verkkosivuilla olevat kiintopisteet. Asetus on oletusarvoisesti käytössä edellisen NVDA-version yhteensopivuuden säilyttämiseksi.
* Jos Puhu komentonäppäimet -asetus on käytössä, NVDA kertoo useiden näppäimistöjen multimedianäppäinten nimet niitä painettaessa (esim. toista, pysäytä, kotisivu jne). (#472)
* NVDA lukee nyt sanan, joka poistetaan painettaessa Ctrl+askelpalautin säätimissä, jotka tukevat sitä. (#491)
* Tekstiä voidaan nyt selata ja lukea nuolinäppäimillä Web Formator -sovelluksessa. (#452)
* NVDA:ssa on nyt tuki Microsoft Office Outlookin osoitekirjan yhteystietoluettelolle.
* Paranneltu tuki upotetuille muokattaville asiakirjoille Internet Explorerissa. (#402)
* Lisätty komento NVDA+Shift+Laskinnäppäimistön miinus, joka siirtää kohdistuksen nykyiseen navigointiobjektiin.
* Lisätty komennot vasemman ja oikean hiiripainikkeen lukitsemiseksi ja lukituksen vapauttamiseksi. Näistä  on hyötyä esim. vedä ja pudota -toiminnoissa. Shift+Laskinnäppäimistön / lukitsee tai vapauttaa vasemman hiiripainikkeen ja Shift+Laskinnäppäimistön - oikean.
* Lisätty uusia pistetaulukkoja: saksalainen 8 pisteen tietokonemerkistö, saksalainen taso 2, suomalainen 8 pisteen tietokonemerkistö, kiinalaiset (kantoni, Hong Kong ja mandariini, Taiwan). (#344, #369, #415, #450)
* NVDA:ta asennettaessa on nyt mahdollista valita, luodaanko työpöydälle kuvake vai ei. Jos kuvaketta ei luoda, NVDA:n käynnistävä pikanäppäinkään ei ole käytettävissä. (#518)
* NVDA voi nyt käyttää IAccessible2-rajapintaa 64-bittisissä sovelluksissa. (#479)
* Paranneltu aktiivisten alueiden tukea Mozilla-sovelluksissa. (#246)
* Lisätty liitäntäkirjasto, jolla sovellukset voivat ohjata NVDA:ta, esim. puhua tekstiä, mykistää puheen, näyttää ilmoituksia pistenäytöllä jne.
* Virheilmoitukset ja muut viestit luetaan nyt Windows Vistan ja Windows 7:n kirjautumisikkunassa. (#506)
* Adobe LiveCyclellä tehtyjä vuorovaikutteisia PDF-lomakkeita tuetaan nyt Adobe Readerissa. (#475)
* NVDA voi nyt lukea saapuvat viestit automaattisesti Miranda IM:n chatti-ikkunoissa, jos dynaamisen sisällön muutosten puhuminen on käytössä. Lisätty myös komennot kolmen viimeisimmän viestin lukemiseen (NVDA+Ctrl+numero). (#546)
* Lisätty tuki Flashin tekstinsyöttökentille. (#461)

#### Muutokset

* Hyvin pitkää näppäimistökäytöstä kertovaa ohjeviestiä ei enää lueta Windows 7:n Käynnistä-valikossa.
* Display-syntetisaattori on korvattu uudella puheentarkastelutoiminnolla. Sitä voidaan käyttää itsenäisesti minkä tahansa puhesyntetisaattorin kanssa, ja se avataan valitsemalla Työkalut-valikosta Puheentarkastelu. (#44)
* Pistenäytöllä näkyvät ilmoitukset hylätään automaattisesti jos painetaan näppäintä, joka aiheuttaa muutoksen, kuten esimerkiksi kohdistuksen siirtymisen. Aiemmin ilmoitukset pysyivät näkyvillä koko niille määritetyn ajan.
* Asetusta, joka määrittää, seuraako pistenäyttö kohdistusta vai tarkastelukohdistinta (NVDA+Ctrl+T), voidaan nyt muuttaa Pistekirjoitusasetukset-valintaikkunasta. Asetus tallennetaan myös käyttäjän asetustiedostoon.
* eSpeak päivitetty versioksi 1.43.03.
* Liblouis-pistekääntäjä päivitetty versioksi 1.8.0.
* Elementtien ilmoittamista näennäispuskureissa merkeittäin tai sanoittain siirryttäessä on paranneltu huomattavasti. Aiemmin luettiin paljon epäolennaisia tietoja, ja ilmoitustapa oli hyvin erilainen kuin riveittäin siirryttäessä. (#490)
* Ctrl-näppäin ei enää tauota puhetta, vaan keskeyttää sen. Puheen tauottamiseen ja jatkamiseen käytetään nyt Shift-näppäintä.
* Taulukon rivien ja sarakkeiden määrää ei enää lueta kohdistusmuutoksia ilmoitettaessa, koska kyseinen ilmoitus oli melko pitkä ja siitä ei useinkaan ollut hyötyä.

#### Bugikorjaukset

* NVDA käynnistyy nyt tilanteessa, jossa UI Automation -tuki on käytettävissä, mutta sen alustus ei jostakin syystä onnistu. (#483)
* Taulukon rivin koko sisältöä ei enää lueta Mozilla-sovelluksissa siirrettäessä kohdistusta taulukon solussa. (#482)
* Paljon alakohtia sisältävien puunäkymien laajentaminen ei enää aiheuta pitkää viivettä.
* Virheen palauttavia puheääniä ei huomioida käytettävissä olevien SAPI 5 -puheäänten luetteloa ladattaessa. Aiemmin yksi viallinen puheääni saattoi joissakin tapauksissa aiheuttaa sen, ettei mitään SAPI 5 -puheääniä voitu käyttää.
* Objektien lukuasetukset -valintaikkunan "Lue objektien pikanäppäimet" -asetus vaikuttaa nyt näennäispuskureihin. (#486)
* Rivi- ja sarakeotsikoiden koordinaatteja ei enää virheellisesti lueta näennäispuskureissa, kun taulukoiden ilmoittaminen on poistettu käytöstä.
* Rivien ja sarakkeiden koordinaatit luetaan nyt näennäispuskureissa oikein taulukosta poistuttaessa ja palattaessa saman taulukon soluun käymättä ensin jossain toisessa solussa (esim. painamalla Nuoli ylös- ja Nuoli alas -näppäimiä taulukon ensimmäisessä solussa). (#378)
* Word-asiakirjaen ja  HTML-muokkaussäädinten tyhjät rivit näytetään nyt asianmukaisesti pistenäytöllä. NVDA näytti aiemmin vain nykyisen virkkeen. (#420)
* Useita tietoturvakorjauksia käytettäessä NVDA:ta Windowsiin kirjauduttaessa ja muilla suojatuilla työpöydillä. (#515)
* Järjestelmäkohdistimen sijainti päivitetään nyt oikein standardinmukaisissa Windowsin muokkauskentissä ja Word-asiakirjoissa käytettäessä ruudun alareunan ulkopuolelle siirtävää jatkuva luku -komentoa. (#418)
* Näennäispuskureissa ei enää lueta linkki- ja napsautettava-tagien sisässä olevia kuvia, joilla ei ole merkitystä ruudunlukuohjelmille. (#423)
* Tehty korjauksia kannettaville tarkoitettuun näppäinasetteluun. (#517)
* Kun pistenäyttö on asetettu seuraamaan tarkastelukohdistinta, ja kun kohdistus siirretään DOS-konsoli-ikkunaan, sen tekstissä voidaan nyt  liikkua kunnolla tarkastelukohdistimella.
* VU meter -edistymispalkkia ei enää lueta sen päivittyessä TeamTalk 3 ja TeamTalk 4 Classicin pääikkunassa. Lisäksi erikoismerkkejä voidaan nyt lukea kunnolla saapuvien keskustelujen ikkunassa.
* Windows 7:n Käynnistä-valikon kohteita ei enää lueta kahteen kertaan. (#474)
* Sivun sisäisten linkkien aktivoiminen Firefox 3.6:ssa siirtää nyt kohdistimen oikeaan kohtaan sivua.
* Korjattu ongelma, joka aiheutti sen, että osaa tiettyjen PDF-asiakirjaen tekstistä ei voitu lukea.
* NVDA ei enää lue väärin tiettyjä viivalla erotettuja numeroita, esim. 500-1000. (#547)
* NVDA ei enää aiheuta Windows XP:ssä Internet Explorerin jumiutumista muutettaessa valintaruutujen tilaa Windows Updatessa. (#477)
* Samanaikainen puhe ja äänimerkit eivät  enää aiheuta ajoittaisia jumiutumisia käytettäessä sisäänrakennettua eSpeak-puhesyntetisaattoria. Eniten tätä tapahtui esim. kopioitaessa suurta määrää tiedostoja resurssienhallinnassa.
* NVDA ei enää ilmoita, että taustalla Firefoxissa avoinna oleva sivu on varattu esim. sisällön päivittymisen vuoksi. Tämä aiheutti myös aktiivisen sovelluksen tilarivin asiaankuulumatonta ilmoittamista.
* Kun Windowsin näppäinasettelua vaihdetaan Ctrl+Shift- tai Alt+Shift-näppäimillä, sen koko nimi ilmoitetaan puheena ja näytetään pistenäytöllä. Aiemmin näppäinasettelu ilmoitettiin vain puheena, ja vaihtoehtoisia asetteluja, kuten esim. Dvorak, ei ilmoitettu lainkaan.
* Taulukoiden tietoja ei enää lueta kohdistuksen muuttuessa, jos taulukoiden ilmoittaminen on poistettu käytöstä.
* Tietyt standardit 64-bittisten sovellusten puunäkymäsäädint, esim. Microsoft HTML-ohjeen Sisällys-puunäkymä, ovat nyt saavutettavia. (#473)
* Korjattu joitakin ongelmia muita kuin ASCII-merkkejä sisältävien ilmoitusten lokiin kirjaamisessa. Tämä saattoi joissakin tapauksissa aiheuttaa satunnaisia virheitä muissa kuin englanninkielisissä järjestelmissä. (#581)
* Tietoja NVDA:sta -valintaikkunan tiedot näkyvät nyt valitulla kielellä. Aiemmin ne näytettiin englanniksi. (#586)
* Puhesyntetisaattorin asetusrenkaan käyttäminen ei enää aiheuta ongelmia, kun puheääntä vaihdetaan johonkin sellaiseen, jolla on vähemmän asetuksia kuin edellisellä.
* Yhteyshenkilöiden nimiä ei enää lueta kahteen kertaan Skype 4.2:n yhteystietoluettelossa.
* Korjattu joitakin mahdollisesti merkittäviä käyttöliittymän ja näennäispuskureiden muistivuotoja. (#590, #591)
* Kierretty paha ongelma joissakin SAPI 4 -syntetisaattoreissa, joka  aiheutti usein virheitä ja NVDA:n kaatumisia. (#597)

### 2009.1

Tämän version tärkeimpiä uusia ominaisuuksia ovat tuki 64-bittisille Windows-versioille, huomattavasti paranneltu tuki Internet Explorerille ja Adobe Readerille, tuki Windows 7:lle, Windowsin kirjautumisikkunan ja Ctrl+Alt+Delete-ruutujen sekä Käyttäjätilien valvonnan (UAC) kehotteiden lukeminen sekä mahdollisuus käyttää verkkosivujen Flash- ja Java-sisältöä. Lisäksi on useita merkittäviä korjauksia NVDA:n vakauteen ja parannuksia yleiseen käyttökokemukseen.

#### Uudet ominaisuudet

* Virallinen tuki Windowsin 64-bittisille versioille. (#309)
* Lisätty ajuri venäjänkieliselle Newfon-puhesyntetisaattorille. (Edellyttää Newfonin erikoisversiota). (#206)
* Näennäispuskureiden kohdistus- ja selaustila voidaan nyt ilmoittaa puheen sijasta äänimerkeillä. Tämä on oletusarvoisesti käytössä. Asetusta voidaan muuttaa näennäispuskureiden asetusvalintaikkunasta. (#244)
* NVDA ei enää keskeytä puhetta näppäimistön äänenvoimakkuusnäppäimiä painettaessa, mikä mahdollistaa äänenvoimakkuuden muuttamisen ja puheen kuuntelemisen välittömästi uudella voimakkuudella. (#287)
* Kokonaan uudelleenkirjoitettu tuki Internet Explorerille ja Adobe Readerille, joka on yhdenmukaistettu  Mozilla Geckon käyttämän ydintuen kanssa, joten esim. nopea sivun lataaminen, kattava pikanavigointi, elementtilista, tekstin valitseminen, automaattinen vuorovaikutustila ja pistenäyttötuki ovat nyt käytettävissä.
* Päivämäärän valintasäätimen tukea paranneltu Windows Vistan Päivämäärän ja ajan ominaisuudet -valintaikkunassa
* Windows XP:n ja Vistan uuden Käynnistä-valikon tukea paranneltu (erityisesti Kaikki ohjelmat- ja Sijainnit-valikoiden osalta). Nyt asianmukaiset tasotiedot ilmoitetaan.
* Hiirtä liikutettaessa luettavan tekstin määrä on nyt määritettävissä Hiiriasetukset-valintaikkunasta. Vaihtoehtoina ovat kappale, rivi, sana tai merkki.
* Kohdistimen kohdalla olevat kirjoitusvirheet luetaan nyt Wordissa.
* Tuki Word 2007:n oikeinkirjoituksen tarkistukselle. Osittainen tuki saattaa olla käytettävissä myös aiemmissa Wordin versioissa.
* Tuki Windows Live Mailille (pelkkää tekstiä sisältävät viestit voidaan nyt lukea).
* Jos käyttäjä siirtyy Windows Vistassa suojatulle työpöydälle (joko siksi, että Käyttäjätilien valvonnan valintaikkuna tuli näkyviin tai koska painettiin Ctrl+Alt+Delete), NVDA ilmoittaa, että suojattu työpöytä on aktiivisena.
* NVDA voi lukea hiiren alla olevan tekstin komentorivi-ikkunoissa.
* Lisätty UI Automation -tuki Windows 7:ään sisältyvän UI Automation -asiakasrajapinnan kautta ja tehty korjauksia NVDA:n käyttökokemuksen parantamiseksi Windows 7:ssä.
* NVDA voidaan määrittää käynnistymään automaattisesti Windowsiin kirjautumisen jälkeen. Asetus löytyy Yleiset asetukset -valintaikkunasta.
* NVDA voi nyt lukea Windowsin suojatut ruudut, kuten kirjautumisikkunan ja Ctrl+Alt+Delete-ruudun sekä Windows Vistan ja uudempien Käyttäjätilien valvonnan kehotteet. Windowsin kirjautumisikkunan lukeminen voidaan määrittää Yleiset asetukset -valintaikkunasta. (#97)
* Lisätty ajuri Optelec ALVA BC6 -sarjan pistenäytöille
* Linkkilohkojen jälkeen ja niitä ennen olevaan tekstiin voidaan nyt verkkosivuja selattaessa siirtyä painamalla n ja Shift+n.
* ARIA-kiintopisteet luetaan nyt verkkosivuja selattaessa , ja niiden välillä voidaan liikkua eteen- ja taaksepäin painamalla d ja Shift+d. (#192)
* Linkkiluettelo-valintaikkuna, joka on käytettävissä verkkosivuja selattaessa, on korvattu Elementtilista-valintaikkunalla, joka näyttää luettelon linkeistä, otsikoista ja kiintopisteistä. Otsikot ja kiintopisteet näytetään hierarkisesti. (#363)
* Uudessa Elementtilista-valintaikkunassa on "Suodata"-kenttä, jonka avulla luetteloa voidaan suodattaa näyttämään vain ne kohteet, joissa annettu teksti esiintyy. (#173)
* Mukana kuljetettava NVDA:n versio etsii asetustiedostoaan NVDA-kansiossa olevasta 'userConfig'-kansiosta. Kuten asennettavassakin versiossa, tämä pitää käyttäjän asetukset erillään NVDA:sta itsestään.
* Mukautetut sovellusmoduulit sekä pistenäyttö- ja puhesyntetisaattoriajurit tallennetaan nyt käyttäjän asetushakemistoon. (#337)
* Näennäispuskurit ladataan nyt taustalla, mikä mahdollistaa sen, että järjestelmää voidaan käyttää jossain määrin latausprosessin aikana. Käyttäjälle ilmoitetaan, jos lataaminen kestää sekuntia kauemmin.
* Jos NVDA havaitsee lakanneensa toimimasta jostakin syystä, kaikki näppäilyt välitetään eteenpäin, jotta käyttäjällä on parempi mahdollisuus järjestelmän elvyttämiseen.
* Tuki ARIA:n vedä ja pudota -toiminnolle Mozillan Gecko-moottoria käyttävissä sovelluksissa. (#239)
* Verkkosivun nimi ja nykyinen rivi tai valinta luetaan nyt näennäispuskurissa kohdistusta siirrettäessä. (#210)
* Näennäispuskureissa voidaan nyt olla vuorovaikutuksessa upotettujen objektien kanssa painamalla Enter niiden kohdalla (voivat olla esim. Flash- ja Java-sisältöä). Jos objekti on saavutettava, siinä voidaan liikkua sarkaimella kuten missä muussa sovelluksessa tahansa. Kohdistus palautetaan sivulle painamalla NVDA+välilyönti. (#431)
* Näennäispuskureissa o ja Shift+o siirtävät seuraavan ja edellisen upotetun objektin kohdalle.
* NVDA:n asennusohjelmalla asennetuilla virallisilla versioilla voidaan nyt Windows Vistassa ja uudemmissa käyttää sovelluksia, jotka ovat käynnissä järjestelmänvalvojan oikeuksin. Tätä mahdollisuutta ei ole mukana kuljetettavissa eikä kehitysversioissa. (#397)

#### Muutokset

* NVDA ei enää käynnistyessään ilmoita "NVDA käynnissä".
* Käynnistys- ja lopetusäänet toistetaan nyt käyttäen NVDA:n asetuksissa määritettyä äänilaitetta Windowsin oletuslaitteen sijaan. (#164)
* Edistymispalkkien ilmoittamista on paranneltu. NVDA voidaan nyt määrittää ilmaisemaan muutokset samaan aikaan sekä puheena että äänimerkeillä.
* Joitakin yleisiä rooleja, kuten ruutu, sovellus ja kehys, ei enää lueta kohdistettaessa, ellei säädinlla ole nimeä.
* Tekstin kopiointikomento (NVDA+F10) ottaa nyt huomioon myös loppumerkin kohdalla olevan merkin. Tämä mahdollistaa rivin viimeisen merkin kopioimisen, mikä ei aiemmin ollut mahdollista. (#430)
* Missä olen -komento (Ctrl+NVDA+Laskinnäppäimistön 5) on poistettu. Tämä näppäinyhdistelmä ei toiminut joillakin näppäimistöillä, eikä komento ollut edes kovin hyödyllinen.
* Navigointiobjektin sijainnin ilmoittava komento on uudelleenmääritelty näppäimiin NVDA+Laskinnäppäimistön delete. Entinen näppäinyhdistelmä ei toiminut joillakin näppäimistöillä. Tämä komento ilmoittaa nyt objektin oikean reunan ja alareunan koordinaattien sijasta objektin leveyden ja korkeuden.
* Suorituskykyä paranneltu erityisesti minikannettavissa, kun useita äänimerkkejä esiintyy peräkkäin, esim.  liikutettaessa hiirtä nopeasti äänikoordinaattien ilmaisemisen ollessa käytössä. (#396)
* Virheestä ilmoittavaa ääntä ei enää toisteta NVDA:n release candidate- ja lopullisissa versioissa. Virheiden tiedot kirjataan edelleen lokiin.

#### Bugikorjaukset

* Kun NVDA käynnistetään 8+3-DOS-polusta, mutta se on asennettu saman kansion pitkään polkuun (esim. progra~1 verrattuna program files), NVDA tunnistaa oikein, että se on asennettu ja lataa käyttäjän asetukset asianmukaisesti.
* Nykyisen ikkunan nimen puhuttaminen NVDA+t:llä toimii nyt valikoissa oikein.
* Pistenäytöllä ei enää kohdistuksessa näytetä hyödytöntä tietoa, kuten nimettömiä paneeleita.
* Java- ja Lotus-sovelluksissa ei enää kohdistuksen muuttuessa lueta hyödytöntä tietoa, kuten  juuri-, kerros- tai vierityspaneeleita.
* Windowsin ohjeen Avainsana-hakukentästä tehty paljon käyttökelpoisempi. Kyseisen säädinn viallisuuden vuoksi nykyistä avainsanaa ei voitu lukea, koska se muuttuu jatkuvasti.
* Oikeat sivunumerot  luetaan Wordissa, jos asiakirjan sivunumerointi on erikseen asetettu.
* Parempi tuki Wordin valintaikkunoiden muokkauskentille (esim. Fontti-valintaikkuna). Näissä säätimissä on nyt mahdollista liikkua nuolinäppäimillä.
* Parempi tuki konsoli-ikkunoille. NVDA voi nyt erityisesti lukea tiettyjen konsoleiden sisällön, joiden se aiemmin ilmoitti olevan tyhjiä. Ctrl+Pause-näppäinyhdistelmän painaminen ei enää sulje NVDA:ta.
* Asennusohjelma käynnistää NVDA:n normaalein käyttäjän oikeuksin Windows Vistassa ja uudemmissa, kun sen käynnistäminen on valittuna asennuksen viimeisessä vaiheessa.
* Askelpalauttimen painaminen käsitellään nyt oikein kirjoitettuja sanoja luettaessa. (#306)
* Tietyistä Resurssienhallinnan ja Windowsin käyttöliittymän tilannekohtaisista valikoista ei enää virheellisesti ilmoiteta, että ne ovat Käynnistä-valikkoja. (#257)
* NVDA käsittelee nyt oikein Mozilla Geckon ARIA-luokat, kun muuta käyttökelpoista sisältöä ei ole saatavilla. (#156)
* NVDA ei enää virheellisesti ota käyttöön automaattista vuorovaikutustilaa muokattaville tekstikentille, jotka päivittävätsisältöään kohdistuksen muuttuessa (esim. osoitteessa https://tigerdirect.com/). (#220)
* NVDA yrittää nyt palautua joistakin tilanteista, jotka ennen aiheuttivat sen täydellisen jumittumisen. Tällaisen tilanteen havaitseminen ja siitä palautuminen voi kestää jopa 10 sekuntia.
* Käyttäjän näyttökieliasetusta käytetään Windowsin maa-asetuksen sijaan, kun NVDA:n kieleksi on asetettu "User default". (#353)
* NVDA tunnistaa nyt AOL Instant Messenger 7:n säädint.
* Seuraavan näppäinpainalluksen suoraan ohjelmalle välittävä komento (NVDA+F2) ei enää jää jumiin jos näppäintä pidetään alhaalla. Aikaisemmin NVDA lakkasi hyväksymästä komentoja jos tätä tapahtui, ja se piti käynnistää uudelleen. (#413)
* Tehtäväpalkkia ei enää ohiteta, kun kohdistus siirtyy sen kohdalle, mikä sattuu usein sovellusta suljettaessa. Aiemmin NVDA käyttäytyi kuin kohdistus ei olisi muuttunut lainkaan.
* NVDA toimii nyt oikein luettaessa tekstikenttiä sellaisissa Java Access Bridgeä käyttävissä sovelluksissa kuten OpenOffice, kun rivinumeroiden lukeminen on käytössä.
* Tekstin kopiointikomento (NVDA+F10) ei enää aiheuta virhettä tilanteessa, jossa loppumerkki asetetaan ennen alkumerkkiä olevaan sijaintiin. Aiemmin tämä saattoi aiheuttaa ongelmia, kuten esim. kaatumisia Notepad++:ssa.
* Tietty ohjausmerkki (0x1) ei enää aiheuta outoa eSpeakin käyttäytymistä (kuten äääänenvoimakkuuden ja -korkeuden muutoksia), kun kyseinen merkki esiintyy tekstissä. (#437)
* Valitun tekstin puhutuskomento (NVDA+Shift+Nuoli ylös) ilmoittaa nyt, ettei valintaa ole, jos objekti ei tue tekstin valitsemista.
* Korjattu ongelma, jossa Enterin painaminen Miranda IM:n tietyissä painikkeissa tai linkeissä aiheutti NDA:n jumiutumisen. (#440)
* Korjattu ongelma, jossa tämänhetkistä riviä tai valintaa ei noudatettu asianmukaisesti nykyisen navigointiobjektin nimeä tavattaessa tai kopioitaessa.
* Korjattu Windowsin bugi, joka aiheutti roskatiedon lukemista Resurssienhallinnan ja Internet Explorerin valintaikkunoiden linkkisäätimissä. (#451)
* Korjattu päiväyksen ja ajan puhutuskomennon (NVDA+F12) ongelma, joka aiheutti päiväysilmoituksen katkeamista joissakin järjestelmissä. (#471)
* Korjattu ongelma, joka aiheutti järjestelmän ruudunlukijalipun ajoittaisen nollaamisen Windowsin suojattujen ruutujen käytön jälkeen. Tämä saattoi aiheuttaa ongelmia sovelluksissa, jotka tarkistavat ruudunlukijalipun, mukaan lukien Skype, Adobe Reader ja Jarte. (#462)
* Internet Explorer 6:n yhdistelmäruutujen aktiivinen kohde luetaan nyt sen muuttuessa. (#342)

### 0.6p3

#### Uudet ominaisuudet

* Koska Excelin kaavarivi on NVDA:lle esteellinen, käyttäjälle tarjotaan erityinen valintaikkuna kaavan muokkausta varten, kun solussa painetaan F2-näppäintä.
* Tuki muotoilulle IAccessible2-tekstisäätimissä, Mozilla-sovellukset mukaan lukien.
* Kirjoitusvirheet voidaan nyt lukea, missä se vain on mahdollista. Asetus on määritettävissä Asiakirjojen muotoilu -valintaikkunasta.
* NVDA voidaan määrittää ilmaisemaan äänimerkeillä joko kaikki tai vain näkyvät edistymispalkit. Edistymispalkkien arvot voidaan vaihtoehtoisesti määrittää puhuttaviksi joka 10 prosentin välein.
* Linkit tunnistetaan nyt RichEdit-säätimissä.
* Hiiri voidaan nyt siirtää tarkastelukohdistimen alla olevaan merkkiin useimmissa muokattavissa tekstisäätimissä. Aiemmin hiiri voitiin siirtää vain keskelle säädina.
* Näennäispuskureissa tarkastelukohdistin lukee nyt puskurin tekstiä pelkän navigointiobjektin sisäisen tekstin sijaan (josta ei useinkaan ole hyötyä). Tämä tarkoittaa, että näennäispuskurissa voidaan liikkua hierarkisesti objektinavigointia käyttäen, ja tarkastelukohdistin siirtyy myös samaan kohtaan.
* Lisätty tuki muutamille uusille Java-säädinten tiloille.
* Jos ikkunan nimen puhutuskomentoa (NVDA+T) painetaan kahdesti, ikkunan nimi tavataan. Kolmesti painettaessa nimi kopioidaan leikepöydälle.
* Toimintonäppäinten nimet luetaan niitä painettaessa näppäinohjeen ollessa käytössä.
* Näppäinohjeen ilmoittamat näppäinten nimet ovat nyt käännettävissä eri kielille.
* Lisätty tuki  SiRecognizerin tunnistetun tekstin kentälle. (#198)
* Tuki pistenäytöille.
* Lisätty komento NVDA+C, joka lukee leikepöydällä olevan tekstin. (#193)
* Jos NVDA vaihtaa näennäispuskureissa automaattisesti vuorovaikutustilaan, voidaan takaisin selaustilaan vaihtaa painamalla Esc. Näppäimiä NVDA+välilyönti voidaan myös edelleen käyttää.
* Kun kohdistus muuttuu tai kohdistinta liikutetaan näennäispuskureissa, NVDA voi automaattisesti vaihtaa kohdistus- tai selaustilaan kohdistimen alla olevasta säädinsta riippuen. Asetus määritetään Näennäispuskureiden asetukset -valintaikkunasta. (#157)
* Uudelleenkirjoitettu SAPI 4 -puhesyntetisaattoriajuri, joka korvaa sapi4serotek- ja sapi4activeVoice-ajurit, sekä korjaa niiden kanssa ilmenneitä ongelmia.
* NVDA:ssa on nyt manifesti, mikä tarkoittaa, ettei sitä enää Windows Vistassa ajeta yhteensopivuustilassa.
* Asetustiedosto ja puhesanastot tallennetaan nyt käyttäjän Application Data -hakemistoon jos NVDA on asennettu asennusohjelmalla. Tämä on välttämätöntä Windows Vistassa ja mahdollistaa myös useiden käyttäjien yksilölliset asetukset.
* Lisätty tuki IAccessible2-säädinten sijaintitiedoille.
* Lisätty mahdollisuus tekstin kopioimiseen leikepöydälle tarkastelukohdistinta käyttäen. NVDA+F9 asettaa alkumerkin tarkastelukohdistimen nykyiseen sijaintiin, NVDA+F10 hakee alkumerkin ja tarkastelukohdistimen nykyisen sijainnin välisen tekstin ja kopioi sen leikepöydälle. (#240)
* Lisätty tuki joillekin Pinnacle TV -ohjelmiston muokkaussäätimille.
* Pitkien valintojen tekstiä luettaessa (512 merkkiä tai enemmän), NVDA lukee nyt valittujen merkkien lukumäärän koko valitun tekstin sijaan. (#249)

#### Muutokset

* Jos käytettäväksi äänilaitteeksi on asetettu Windowsin oletuslaite (Microsoft Sound Mapper), NVDA vaihtaa uuden oletuslaitteen eSpeakille ja äänille, kun oletuslaite muuttuu. NVDA esim. siirtyy käyttämään USB-äänilaitetta, jos siitä tulee automaattisesti oletuslaite sen ollessa kytkettynä.
* Paranneltu eSpeakin suorituskykyä joidenkin Windows Vistan ääniajureiden kanssa.
* Linkkien, otsikoiden, taulukoiden, luetteloiden ja sisennettyjen lainausten ilmoittaminen määritetään nyt Asiakirjojen muotoiluasetukset -valintaikkunasta. Näitä asetuksia käytetään nyt kaikissa asiakirjoissa.
* Nopeus on nyt oletusasetuksena puhesyntetisaattorin asetusrenkaassa.
* Sovellusmoduulien lataamista ja muistista poistoa paranneltu.
* Nykyisen ikkunan nimen puhutuskomento (NVDA+t) lukee nyt vain nimen koko objektin sijasta. Jos objektilla ei ole nimeä, käytetään sovelluksen prosessinimeä.
* Näennäispuskurin läpivientitila päällä ja pois -ilmoituksen sijaan NVDA ilmoittaa nyt vuorovaikutustila (läpivienti päällä) ja selaustila (läpivienti pois).
* Puheäänet tallennetaan asetustiedostoon nyt tunnuksen mukaan indeksin sijasta. Tämä tekee ääniasetuksista ja asetusten muutoksista luotettavampia eri järjestelmissä. Puheääniasetusta ei säilytetä vanhoissa asetustiedostoissa, ja lokiin kirjataan virhe ensimmäisellä puhesyntetisaattorin käyttökerralla. (#19)
* Kaikkien puunäkymien kohdan taso ilmoitetaan nyt ensin, jos se on muuttunut aiemmin kohdistetusta. Tämä koski aiemmin vain Windowsin natiiveja (SysTreeView32) puunäkymiä.

#### Bugikorjaukset

* Puheen loppuosa ei enää jää pois käytettäessä NVDA:ta eSpeakin kanssa etäyhteydellä.
* Korjattu puhesanastojen tallennuksessa ilmenneitä ongelmia tietyillä puheäänillä.
* Viive poistettu Mozilla Gecko -näennäispuskureista siirryttäessä tekstiasiakirjaen loppua kohti muuten kuin merkki kerrallaan (sana, rivi jne). (#155)
* Jos kirjoitettujen sanojen lukeminen on käytössä, sana luetaan Enteriä painettaessa.
* Korjattu joitakin richedit-asiakirjaen merkistöongelmia.
* NVDA:n lokintarkastelutoiminto käyttää nyt  lokin näyttämiseen richeditiä pelkän muokkaussäätimen sijasta. Tämä parantaa sana kerrallaan lukemista.
* Korjattu joitakin upotettuihin objekteihin liittyviä ongelmia richedit-säätimissä.
* NVDA lukee nyt sivunumerot Microsoft Wordissa. (#120)
* Korjattu ongelma Mozilla Gecko -näennäispuskurissa, jossa sarkaimella siirtyminen valitun valintaruudun kohdalle ja välilyönnin painaminen ei ilmoittanut, että sen valinta poistettiin.
* Osittain valitut valintaruudut ilmoitetaan oikein Mozilla-sovelluksissa.
* Jos tekstivalinta laajentuu ja kutistuu molempiin suuntiin, se luetaan yhdessä osassa kahden sijasta.
* NVDA:n pitäisi nyt lukea Mozilla Geckon muokkauskentät hiirellä liikuttaessa.
* Jatkuva luku -toiminnon ei pitäisi enää aiheuttaa kaatumista tietyillä SAPI 5 -syntetisaattoreilla.
* Korjattu ongelma, jossa tekstivalinnan muutoksia ei luettu Windowsin standardeissa muokkaussäätimissä ennen ensimmäistä NVDA:n käynnistyksen jälkeistä kohdistusmuutosta.
* Korjattu hiiren seuranta Java-objekteissa. (#185)
* NVDA ei enää ilmoita kutistetuiksi sellaisia Java-puunäkymäkohteita, joilla ei ole alempaa tasoa.
* Kohdistettu objekti ilmoitetaan, kun Java-ikkuna tulee etualalle. Aiemmin vain ylimmän tason objekti ilmoitettiin.
* eSpeak-puhesyntetisaattoriajuri ei enää lakkaa kokonaan puhumasta yksittäisen virheen jälkeen.
* Korjattu ongelma, jossa päivitettyjä puheäänen parametreja (nopeus, korkeus jne) ei tallennettu, kun puheääntä vaihdettiin syntetisaattorin asetusrenkaasta.
* Kirjoitettujen merkkien ja sanojen lukemista paranneltu.
* Konsolisovelluksissa (esim. joissakin tekstiseikkailupeleissä) luetaannyt tekstiä, jota ei aiemmin luettu.
* NVDA ei huomioi taustalla olevien ikkunoiden kohdistusmuutoksia. NVDA saattoi aiemmin pitää niitä aktiivisen ikkunan kohdistusmuutoksina.
* Paranneltu kohdistuksen havaitsemista tilannekohtaisista valikoista poistuttaessa. Aikaisemmin NVDA ei usein reagoinut mitenkään.
* NVDA ilmoittaa, kun tilannekohtainen valikko avataan Käynnistä-valikossa.
* NVDA sanoo perinteistä Käynnistä-valikkoa avatessa "Käynnistä-valikko" sen sijaan, että se sanoisi "Sovellusvalikko", kuten aiemmin.
* Paranneltu ilmoitusten lukemista esim. Firefoxissa. NVDA:n ei pitäisi enää lukea niitä useita kertoja, eikä muutakaan ylimääräistä. (#248)
* Kohdistettavien vain luku -muokkauskenttien tekstiä ei enää lasketa mukaan haettaessa valintaikkunoiden tekstiä. Tämä korjaa esim. automaattisen lisenssiehtojen lukemisen asennusohjelmissa.
* NVDA ei enää ilmoita valitun tekstin perumista poistuttaessa joistakin muokkaussäätimistä (esim. Internet Explorerin osoiterivi ja Thunderbird 3:n sähköpostiosoitekentät).
* Avattaessa pelkkää tekstiä sisältäviä viestejä Outlook Expressissä ja Windows Mailissa, kohdistus sijoitetaan oikein viestiin, jotta se on valmiina luettavaksi. Aiemmin viestiin täytyi siirtyä sarkaimella tai napsauttaa hiirellä, jotta sitä saattoi lukea nuolinäppäimillä.
* Korjattu useita suuria "Puhu komentonäppäimet" -toiminnon ongelmia.
* NVDA voi nyt lukea standardeissa muokkaussäätimissä tekstiä, jossa on enemmän kuin 65535 merkkiä (esim. iso tiedosto Muistiossa).
* Paranneltu rivin lukemista MSHTML-muokkauskentissä (Outlook Expressin viestinkirjoitusikkuna ja Internet Explorerin tekstinsyöttökentät).
* NVDA ei enää jää ajoittain jumiin muokattaessa tekstiä OpenOfficessa. (#148, #180)

### 0.6p2

* eSpeakin oletuspuheääntä paranneltu.
* Lisätty näppäinasettelu kannettaville tietokoneille. Näppäinasettelu määritetään NVDA:n Näppäimistöasetukset-valintaikkunasta. (#60)
* Tuki SysListView32-säädinten ryhmäkohdille, joita on pääasiassa Windows Vistassa. (#27)
* Puunäkymäkohteiden valinnan tila ilmoitetaan SysTreeview32-säätimissä.
* Lisätty pikanäppäimet monille NVDA:n asetusvalintaikkunoille.
* Tuki IAccessible2-rajapintaa käyttäville sovelluksille, kuten Firefoxille käytettäessä NVDA:ta siirrettävältä medialta.
* Korjattu näennäispuskurin linkkiluettelon kaatumisongelma Gecko-sovelluksissa. (#48)
* NVDA:n ei pitäisi enää kaataa Mozilla Gecko -sovelluksia, kuten Firefoxia ja Thunderbirdiä, jos NVDA on käynnissä suuremmilla oikeuksilla kuin kyseessä oleva sovellus.
* Puhesanastot (aiemmin käyttäjän sanastot) voivat nyt olla joko kirjainkoon huomioivia tai sellaisia, joissa kirjainkoolla ei ole väliä, ja korvattavat merkkijonot voivat olla valinnaisesti sääntölausekkeita. (#39)
* Ruutuasettelun käyttäminen näennäispuskureissa voidaan nyt määrittää asetusvalintaikkunasta.
* Ilman href-viittausta olevia anchor-tageja ei enää ilmoiteta linkkeinä Gecko-näennäispuskureissa. (#47)
* NVDA:n Etsi-komento muistaa nyt viimeisimmän haun kaikkien sovellusten välillä. (#53)
* Korjattu näennäispuskureiden ongelmia, joissa joidenkin valintaruutujen ja -painikkeiden valittu-määritettä ei ilmoitettu.
* Näennäispuskurin läpivientitila on nyt verkkosivukohtainen sen sijaan, että se olisi sama kaikille. (#33)
* Korjattu kohdistusmuutosten hitautta sekä virheellisiä puheen keskeytyksiä, joita esiintyi käytettäessä NVDA:ta järjestelmässä, joka oli ollut valmiustilassa, tai joka oli hidas.
* Paranneltu yhdistelmäruutujen tukea Firefoxissa.
* Paranneltu tilarivin havaitsemisen tarkkuutta monissa sovelluksissa. (#8)
* Lisätty vuorovaikutteinen NVDA Python -konsoli, jonka avulla kehittäjät voivat tarkastella ja käsitellä NVDA:n sisäistä toimintaa sen ollessa käynnissä.
* Jatkuva luku- sekä valinnan ja nykyisen rivin lukukomennot toimivat nyt oikein näennäispuskurin läpivientitilassa. (#52)
* Puheen nopeutus- ja hidastuskomennot poistettu. Näiden asetusten muuttamiseen tulisi käyttää puhesyntetisaattorin asetusrengasta (Ctrl+NVDA+Nuoli ylös/alas) tai ääniasetusten valintaikkunaa.
* Paranneltu edistymispalkkeja ilmaisevien äänimerkkien äänialaa ja skaalausta.
* Uuteen näennäispuskuriin lisätty pikanavigointinäppäimiä: l=lista, i=listan kohde, e=muokkauskenttä, b=painike, x=valintaruutu, r=valintapainike, g=grafiikka, q=sisennetty lainaus, c=yhdistelmäruutu, numerot 1 - 6=niitä vastaavat otsikkotasot, s=erotin, m=kehys. (#67, #102, #108)
* Uuden verkkosivun latauksen peruuttaminen Firefoxissa mahdollistaa aiemman sivun sisältävän näennäispuskurin käytön, mikäli sitä ei ole vielä tuhottu. (#63)
* Näennäispuskureissa sana kerrallaan liikkuminen on nyt tarkempaa, koska sanat eivät enää satunnaisesti sisällä tekstiä useammasta kuin yhdestä kentästä. (#70)
* Kohdistuksen seurannan ja päivityksen tarkkuutta paranneltu Mozilla Gecko -näennäispuskureissa.
* Uuteen näennäispuskuriin lisätty Etsi edellinen -komento (Shift+NVDA+F3)
* Nopeutettu NVDA:n toimintaa Mozilla Gecko -valintaikkunoissa (Firefoxissa ja Thunderbirdissä). (#66)
* Lisätty mahdollisuus NVDA:n lokitiedoston tarkasteluun (löytyy NVDA-valikon Työkalut-alivalikosta).
* Ajan ja päiväyksen puhutuskomennot ottavat käytettävän kielen huomioon. Välimerkit ja sanojen järjestys vastaavat nyt kyseistä kieltä.
* NVDA:n Yleiset asetukset -valintaikkunan Kieli-yhdistelmäruutu näyttää nyt kielten koko nimet käytön helpottamiseksi
* Luettaessa tekstiä nykyisessä navigointiobjektissa, teksti on aina ajan tasalla, jos se muuttuu dynaamisesti (esim. luettelokohteen teksti Windowsin Tehtävienhallinnassa). (#15)
* Hiirikohdistimen alla oleva kappale luetaan nyt hiirellä liikuttaessa objektin kaiken tekstin tai nykyisen sanan sijasta. Lisäksi äänikoordinaattien ja objektien roolien ilmoittaminen on valinnaista, ne ovat oletusarvoisesti poissa käytöstä.
* Tuki tekstin lukemiseen Wordissa hiiren avulla.
* Korjattu bugi, joka aiheutti sen, ettei valittua tekstiä enää luettu sovellusten valikkoriveiltä poistuttaessa (esim. WordPadissa)
* Kappaleen nimeä ei enää lueta uudestaan ja uudestaan Winampissa kappaletta vaihdettaessa, toistoa pysäytettäessä, jatkettaessa tai keskeytettäessä.
* Lisätty mahdollisuus satunnaissoitto- ja toistosäädinten tilan lukemiseen Winampissa. Toimii pääikkunassa ja soittolistamuokkaimessa.
* Paranneltu tiettyjen kohteiden aktivoimista Mozilla Gecko -näennäispuskureissa. Näitä kohteita voivat olla esim. napsautettavat grafiikat, kappaleita sisältävät linkit sekä muut oudot rakenteet.
* Korjattu viive avattaessa NVDA:n asetusvalintaikkunoita joissakin järjestelmissä. (#65)
* Lisätty tuki Total Commander -tiedostojenhallintasovellukselle.
* Korjattu sapi4serotek-ajurin bugi, jossa äänenkorkeus saattoi lukittua johonkin tiettyyn arvoon, ts. jäi korkeaksi ison kirjaimen jälkeen. (#89)
* Napsautettava teksti ja muut kentät, joissa on OnClick-HTML-määrite, ilmaistaan napsautettavina Mozilla Gecko -näennäispuskureissa. (#91)
* Nykyinen kohta näkyy ruudulla selattaessa verkkosivuja Mozilla Gecko -näennäispuskureissa, jotta näkevät saavat käsityksen siitä, missä kohtaa sivua käyttäjä on. (#57)
* Lisätty alkeellinen tuki ARIA:n aktiivisten alueiden näkyville tapahtumille IAccessible2-rajapintaa hyödyntävissä sovelluksissa. Tästä on hyötyä esim. ChatZilla-IRC-sovelluksessa, jossa uudet viestit luetaan nyt automaattisesti.
* Tehty jonkin verran parannuksia, jotka auttavat käyttämään ARIA:ta hyödyntäviä verkkosovelluksia, kuten Google Docs:ia
* Näennäispuskurista kopioitavaan tekstiin ei enää lisätä ylimääräisiä tyhjiä rivejä
* Välilyöntinäppäin ei enää avaa linkkiluettelon linkkejä. Sitä voidaan nyt käyttää kuten muitakin merkkejä jonkin tietyn linkin kohdalle siirtymiseen kirjoittamalla osa sen nimestä.
* Hiiren navigointiobjektiin siirtävä komento (NVDA+Laskinnäppäimistön /) siirtää nyt hiiren navigointiobjektin keskelle vasemman yläreunan sijasta.
* Lisätty komennot hiiren vasemman ja oikean painikkeen napsautukselle (laskinnäppäimistön / ja laskinnäppäimistön *)
* Windowsin ilmoitusalueen käyttöä paranneltu. Kohdistuksen ei enää pitäisi hypätä takaisin johonkin tiettyyn kohtaan. (#10)
* Suorituskykyä paranneltu sekä estetty NVDA:ta lukemasta Ylimääräistä tekstiä pidettäessä nuolinäppäintä alhaalla ja tultaessa tekstin loppuun muokkauskentässä.
* Poistettu mahdollisuus, joka pakottaa odottamaan sen aikaa kun tiettyjä ilmoituksia luetaan. Tämä korjaa joitakin kaatumisia ja jumiutumisia erinäisillä puhesyntetisaattoreilla. (#117)
* Lisätty tuki italiankieliselle Audiologic TTS 3 -puhesyntetisaattorille. (#105)
* Mahdollinen suorituskyvyn parannus liikuttaessa Word-asiakirjoissa.
* Paranneltu ilmoitusten tekstin lukemisen tarkkuutta Mozilla Gecko -sovelluksissa.
* Korjattu mahdollisia kaatumisia yritettäessä tallentaa NVDA:n asetuksia muissa kuin englannninkielisissä Windows-versioissa. (#114)
* Lisätty Tervetuloa-valintaikkuna. Tämä valintaikkuna on suunniteltu antamaan olennaisia tietoja uusille NVDA:n käyttäjille ja mahdollistamaan Capslockin määrittämisen NVDA-näppäimeksi. Valintaikkuna näytetään oletusarvoisesti NVDA:n käynnistyessä, kunnes se poistetaan käytöstä.
* Korjattu Adobe Reader -versioiden 8 ja 9 alkeellinen tuki, jotta PDF-asiakirjaen lukeminen on mahdollista.
* Korjattu joitakin ongelmia, joita saattoi esiintyä pidettäessä näppäimiä alhaalla ennen kuin NVDA oli kunnolla käynnistynyt.
* Jos NVDA on määritetty tallentamaan asetuksensa suljettaessa, varmistetaan, että ne tallennetaan oikein windowsia sammutettaessa tai ulos kirjauduttaessa.
* Asennusohjelman alkuun lisätty NVDA-tunnusääni.
* NVDA:n pitäisi asennusohjelman käynnistämänä ja muutenkin sulkeutuessaan siivota kuvakkeensa asianmukaisesti ilmoitusalueelta.
* NVDA:n valintaikkunoiden standardisäädinten nimien (kuten OK ja Peruuta-painikkeet) pitäisi nyt näkyä samalla kielellä, jota NVDA on asetettu käyttämään.
* Sovelluksen oletuskuvakkeen sijaan NVDA:n Käynnistä-valikon ja työpöydän pikakuvakkeessa käytetään nyt NVDA:n omaa ohjelmakuvaketta.
* Solut luetaan Microsoft Excelissä sarkain- ja Shift+sarkain-näppäimillä liikuttaessa. (#146)
* Tiettyjä luetteloita ei enää lueta moneen kertaan Skypessä.
* Paranneltu kohdistimen seurantaa IAccessible2- ja Java-sovelluksissa kuten OpenOfficessa ja Lotus Symphonyssa. NVDA odottaa asianmukaisesti kohdistimen siirtymistä asiakirjassa sen sijaan, että lukisi vahingossa joidenkin kappaleiden lopusta väärän sanan tai rivin. (#119)
* Tuki AkelPad 4.0:n AkelEdit-säätimille.
* NVDA ei enää lukkiudu Lotus Synphonyssa siirryttäessä asiakirjasta valikkoriville.
* NVDA ei jää enää jumiin Windows XP:n Lisää tai poista sovellus -sovelmassa jonkin ohjelman asennuksen poistoa käynnistettäessä. (#30)
* NVDA ei jää enää jumiin Spybot Search & Destroy -ohjelmaa  avattaessa.

### 0.6p1

#### Verkkosisällön käyttäminen uusilla näennäispuskureilla (toistaiseksi vain Mozilla Gecko 1.9 -sovelluksissa kuten Firefox 3 ja Thunderbird 3)

* Verkkosivujen lataus on lähes 30 kertaa nopeampaa (useimpien sivujen latautumista ei tarvitse odottaa enää lainkaan).
* Lisätty linkkiluettelo (NVDA+F7)
* Paranneltu Etsi-valintaikkunaa (Ctrl+NVDA+F) niin, että haku ei ota kirjainkokoa huomioon, sekä korjattu muutamia kohdistusongelmia.
* Tekstin valitseminen ja kopiointi on nyt mahdollista.
* Uudet näennäispuskurit näyttävät verkkosivun ruutuasettelussa (linkit ja säädint eivät ole omilla riveillään, elleivät ne ole niin visuaalisesti). Asetus voidaan ottaa käyttöön ja poistaa käytöstä painamalla NVDA+V.
* Nyt on mahdollista siirtyä kappale kerrallaan painamalla Ctrl+Nuoli ylös ja Ctrl+Nuoli alas.
* Dynaamisen sisällön tukea paranneltu
* Paranneltu rivien ja kenttien lukemisen tarkkuutta siirryttäessä nuolinäppäimillä ylös ja alas.

#### Kansainvälisyys

* Nyt on mahdollista kirjoittaa ns. "kuollutta merkkiä" edellyttäviä aksenttimerkkejä.
* NVDA ilmoittaa, kun näppäinasettelu vaihtuu (painettaessa Alt+Shift).
* Päiväyksen ja ajan puhutustoiminto ottaa nyt huomioon järjestelmän nykyiset alue- ja kieliasetukset.
* Lisätty tshekinkielinen käännös.
* Lisätty vietnaminkielinen käännös.
* Lisätty afrikaansinkielinen käännös.
* Lisätty venäjänkielinen käännös.
* Lisätty puolankielinen käännös.
* Lisätty japaninkielinen käännös.
* Lisätty thainkielinen käännös.
* Lisätty kroatiankielinen käännös.
* Lisätty galiciankielinen käännös.
* Lisätty ukrainankielinen käännös.

#### Puhe

* NVDA:ssa on nyt eSpeakin 1.33-versio, jossa on useita parannuksia, joita ovat mm. paranneltu kielituki, nimetyt puheäänimuunnelmat ja mahdollisuus puhua nopeammin.
* Ääniasetukset-valintaikkunasta on nyt mahdollista vaihtaa käytettävän syntetisaattorin puheäänimuunnelmaa, jos sellaisia tuetaan. Muunnelma on yleensä muunnos nykyisestä puheäänestä. (eSpeak tukee muunnelmia).
* Ääniasetukset-valintaikkunaan lisätty mahdollisuus muuttaa käytettävän puhesyntetisaattorin äänensävyä, jos tätä tuetaan. (eSpeak tukee äänensävyn muuttamista).
* Lisätty mahdollisuus objektin sijaintitietojen lukemisen (esim. 1 / 4) käytöstä poistamiseen. Asetus löytyy Objektien lukuasetukset -valintaikkunasta.
* NVDA voi antaa nyt äänimerkin isoa kirjainta luettaessa. Asetus voidaan ottaa käyttöön ja poistaa käytöstä Ääniasetukset-valintaikkunasta. Lisätty myös "Nosta äänenkorkeutta isojen kirjainten kohdalla" -valintaruutu, jolla voidaan määrittää, tulisiko NVDA:n nostaa äänenkorkeutta isojen kirjainten kohdalla. Joten NVDA voi nyt joko nostaa äänenkorkeutta, sanoa "iso" tai antaa äänimerkin.
* NVDA:han lisätty mahdollisuus puheen keskeyttämiseen (sama toiminto kuin Mac-käyttöjärjestelmän VoiceOver-ruudunlukuohjelmassa). Kun NVDA puhuu jotakin, voidaan puhe keskeyttää painamalla Ctrl- tai Shift-näppäintä kuten tavallisesti, mutta jos tämän jälkeen painetaan uudestaan Shift-näppäintä (kunhan mitään muita näppäimiä ei ole painettu), puhe jatkuu täsmälleen siitä kohdasta, mihin se jäi.
* Lisätty virtuaalipuhesyntetisaattori, joka tulostaa tekstin ikkunaan sen puhumisen sijasta. Tämä on miellyttävämpää näkeville kehittäjille, jotka eivät ole tottuneet puhesynteesiin, mutta jotka haluavat tietää, mitä NVDA puhuu. Vikoja vielä luultavasti on, joten palaute on ehdottomasti tervetullutta.
* NVDA ei enää oletusarvoisesti lue välimerkkejä, niiden lukeminen voidaan ottaa käyttöön painamalla NVDA+P.
* eSpeak puhuu nyt oletusarvoisesti hiukan hitaammin, mikä pitäisi olla helpompaa sitä ensi kertaa käyttäville.
* Lisätty käyttäjäsanastoja, joiden avulla NVDA saadaan lukemaan tietyt sanat eri tavalla. Sanastoja on kolmea eri tyyppiä: oletus, puheäänikohtainen ja tilapäinen. Oletussanastoon lisätyt sanat vaikuttavat NVDA:han jatkuvasti ja puheäänikohtaiset sanastot vain nykyiseen puheääneen. Tilapäissanasto on sellaisia tilanteita varten, joissa halutaan nopeasti lisätä sana jotakin tiettyä tehtävää varten, mutta sitä ei haluta pysyväksi (se häviää kun NVDA suljetaan). Sanastoihin lisättävät säännöt ovat toistaiseksi sääntölausekkeita.
* Puhesyntetisaattorin käyttämä äänilaite voidaan nyt valita Syntetisaattori-valintaikkunasta.

#### Suorituskyky

* NVDA ei vie enää paljon muistia muokattaessa viestejä MSHTML-muokkaussäätimissä
* Suorituskykyä paranneltu tarkasteltaessa tekstiä monissa säätimissä, joissa ei ole todellista kohdistinta, esim. MSN Messengerin historiaikkuna, puu- ja luettelonäkymän kohdat jne.
* Suorituskykyä paranneltu richedit-asiakirjoissa.
* NVDA:n viemän järjestelmämuistin määrän ei pitäisi enää hitaasti kasvaa ilman syytä
* Korjattu vikoja, joita esiintyi yritettäessä siirtää kohdistusta DOS-konsoli-ikkunaan toistuvia kertoja. NVDA:lla oli taipumus kaatua tällaisissa tilanteissa.

#### Näppäinkomennot

* Näppäimet NVDA+Shift+Laskinnäppäimistön 6 ja NVDA+Shift+Laskinnäppäimistön 4 mahdollistavat siirtymisen eteen- ja taaksepäin koko objektihierarkiassa. Tämä tarkoittaa, että sovelluksen ikkunan kaikkia osia voidaan selata tarvitsematta siirtyä ylempään tai ensimmäiseen alemman tason objektiin. Jos hierarkian taso vaihtuu näitä komentoja käytettäessä, siitä ilmoitetaan äänimerkeillä.
* Ääniasetukset voidaan nyt määrittää myös avaamatta Ääniasetukset-valintaikkunaa puhesyntetisaattorin asetusrenkaan avulla. Haluttu asetus (puheääni, äänenkorkeus jne).) valitaan painamalla Ctrl+NVDA+Nuoli oikealle tai Ctrl+NVDA+Nuoli vasemmalle, ja valitun asetuksen arvoa muutetaan painamalla Ctrl+NVDA+Nuoli ylös tai Ctrl+NVDA+Nuoli alas.
* Lisätty komento nykyisen valinnan lukemiseen muokkauskentissä (NVDA+shift+Nuoli ylös).
* Melko monet jotain tekstiä puhuttavat NVDA:n komennot (sellaiset kuin nykyisen rivin lukeminen jne.) voivat nyt tavata tekstin, jos niitä painetaan kolme kertaa nopeasti.
* NVDA-näppäimenä voidaan käyttää sekä laskinnäppäimistön että laajennettua Insertiä ja Capslockia. Lisäksi, jos jotain näistä näppäimistä painetaan kahdesti ilman mitään muuta näppäintä sen ollessa käytössä, välitetään kyseinen näppäinpainallus käyttöjärjestelmälle aivan kuin sitä olisi painettu silloin, kun NVDA ei ollut käynnissä. NVDA-näppäin voidaan määrittää näppäimistöasetusten valintaikkunasta.

#### Sovellustuki

* Firefox 3:n ja Thunderbird 3:n tukea paranneltu. Latausajat ovat lähes 30 kertaa nopeampia, ruutuasettelua käytetään oletusarvoisesti (asetusta voidaan vaihtaa painamalla NVDA+V), lisätty linkkiluettelo (NVDA+F7), Etsi-valintaikkunassa (Ctrl+NVDA+F) kirjainkoolla ei ole väliä, paljon parempi dynaamisen sisällön tuki, tekstin valitseminen ja kopioiminen on nyt mahdollista.
* Tekstin valitseminen ja kopioiminen on nyt mahdollista MSN Messengerin ja Windows Live Messengerin historialuetteloissa.
* Audacity-äänieditorin tukea paranneltu.
* Lisätty tuki muutamille Skypen muokkaus- ja tekstisäätimille.
* Miranda-IM:n tukea paranneltu.
* Korjattu joitakin kohdistusongelmia avattaessa HTML- ja pelkkää tekstiä sisältäviä viestejä Outlook Expressissä.
* Outlook expressin uutisryhmien viestikentät nimetään nyt oikein.
* NVDA voi nyt lukea osoitteet Outlook Expressin viestikentissä (vastaanottaja/lähettäjä/kopio jne.)
* Poistettaessa viestiä Outlook Expressin viestiluettelosta, NVDA:n pitäisi olla nyt tarkempi ilmoittaessaan seuraavaa viestiä, jonka kohdalle kohdistus siirtyy.

#### Sovellusrajapinnat

* Paranneltu objektinavigointia MSAA-objekteissa. Jos ikkunassa on järjestelmävalikko, otsikkorivi tai vierityspalkkeja, niihin voidaan nyt siirtyä objektinavigoinnilla.
* Lisätty tuki IAccessible2-saavutettavuusrajapinnalle. Entistä useampien säädintyyppien tunnistamisen lisäksi NVDA voi tämän avulla käyttää kohdistinta myös sellaisissa sovelluksissa kuin Firefox 3 ja Thunderbird 3 mahdollistaen tekstissä liikkumisen sekä tekstin valitsemisen ja muokkaamisen.
* Lisätty tuki Scintilla-muokkaussäätimille, joita on esim. Notepad++:ssa ja TortoiseSVN:ssä.
* Lisätty tuki Java-sovelluksille Java Access Bridgen avulla. Tämä tarjoaa alkeellisen tuen Open Officelle ja muille Java-sovelluksille, Jos Java on asennettu. Verkkoselaimessa toimivat Java-sovelmat eivät vielä toimi.

#### Hiiri

* Paranneltu hiiren alla olevan tekstin lukemista. Se on nyt paljon nopeampaa, ja lisäksi joissakin säätimissä, kuten standardeissa muokkauskentissä sekä Java- ja IAccessible2-säätimissä, on mahdollista lukea myös nykyinen sana, eikä vain nykyistä objektia. Tästä voi olla hyötyä joillekin heikkonäköisille käyttäjille, jotka haluavat lukea hiiren avulla vain jonkin tietyn osan tekstistä.
* Hiiriasetukset-valintaikkunaan on lisätty asetus "Ilmaise hiiren koordinaatit äänimerkeillä". Kun tämä asetus on käytössä, aina hiirtä liikutettaessa toistetaan 40 millisekunnin mittainen äänimerkki, jonka korkeus (väliltä 220 - 1760 Hz) ilmaisee y-akselia ja vasemman- sekä oikeanpuoleinen äänenvoimakkuus x-akselia. Tämän avulla sokea henkilö saa jonkinlaisen käsityksen siitä, missä kohtaa ruutua hiiri on. Toiminto on riippuvainen "Lue hiiren alla oleva objekti" -asetuksesta, joten sen on oltava myös käytössä. Tämä tarkoittaa, että jos sekä äänikoordinaatit että hiiren alla olevan objektin lukeminen halutaan poistaa nopeasti käytöstä, tarvitsee vain painaa NVDA+M. Äänimerkit ovat myös voimakkaampia tai hiljaisempia riippuen siitä, miten kirkas hiiren alla oleva ruudun kohta on.

#### Objektien lukeminen ja vuorovaikutus

* Paranneltu tuki yleisimmille puunäkymäsäätimille. NVDA kertoo nyt puunäkymän haaraa laajennettaessa, montako kohtaa siinä on. Myös puunäkymän taso ilmoitetaan siirryttäessä haaraan ja siitä pois. Lisäksi nykyisen kohdan numero ja kohtien lukumäärä ilmoitetaan nykyisen haaran mukaan koko puunäkymän sijasta.
* Paranneltu sitä, mitä kohdistuksen muuttuessa luetaan. Sen sijaan että vain nykyinen säädin luetaan, nyt luetaan myös tiedot kaikista sisäkkäin olevista säätimistä. Jos esimerkiksi siirrytään sarkaimella ja tullaan ryhmäruudussa olevan painikkeen kohdalle, myös kyseinen ryhmäruutu luetaan.
* NVDA yrittää nyt lukea monien valintaikkunoiden tekstin sellaisena kuin se näkyy. Enimmän aikaa tämä on tarkkaa , vaikka vielä on useita valintaikkunoita, joita ei lueta niin hyvin kuin pitäisi.
* Objektien lukuasetukset -valintaikkunaan lisätty Lue objektien kuvaukset -valintaruutu. Tehokäyttäjät saattavat haluta poistaa käytöstä tämän asetuksen estääkseen NVDA:ta lukemasta paljon  ylimääräisiä kuvauksia erinäisissä esim. Java-sovelluksissa.
* NVDA lukee automaattisesti valitun tekstin muokkaussäätimissä, kun kohdistus siirtyy niihin. Jos yhtään tekstiä ei ole valittuna, tällöin vain nykyinen rivi luetaan kuten tavallisesti.
* NVDA on nyt paljon tarkempi toistaessaan sovellusten edistymispalkkeja ilmaisevia äänimerkkejä. Se ei mene enää sekaisin sellaisissa Eclipse-sovelluksissa Kuten Lotus Notes, Symphony tai Accessibility Probe.

#### Käyttöliittymä

* NVDA:n käyttöliittymäikkuna on korvattu NVDA-valikolla.
* NVDA:n käyttöliittymän asetukset -valintaikkuna on nyt nimeltään Yleiset asetukset, johon on myös lisätty yhdistelmäruutu lokitason asettamiseksi. Lokitaso määrittää, mitä tietoja NVDA:n lokitiedostoon tallennetaan. Lokitiedoston nimi on nyt nvda.log.
* "Ilmoita objektiryhmien nimet" -valintaruutu poistettu Objektien lukeminen -valintaikkunasta. Objektiryhmiä käsitellään nyt eri tavalla.

### 0.5

* NVDA:ssa on nyt sisäänrakennettu eSpeak-puhesyntetisaattori, joka tukee useita kieliä ja on erittäin herkkä ja kevyt. SAPI-syntetisaattoreita voidaan edelleen käyttää, mutta eSpeakia käytetään oletusarvoisesti.
eSpeak ei ole riippuvainen mistään erikoisohjelmistoista, joten sitä voidaan käyttää NVDA:ssa millä tahansa tietokoneella, muistitikulla jne.
Saadaksesi lisätietoja eSpeakista tai ladataksesi sen muita versioita, käy osoitteessa https://espeak.sourceforge.net/.
* Korjattu bugi, joka aiheutti  väärän merkin lukemisen painettaessa Delete-näppäintä Internet Explorerin ja Outlook Expressin muokkausruuduissa.
* Lisätty tuki useimmille Skypen muokkauskentille.
* Näennäispuskurit ladataan vain, kun kohdistus on ikkunassa, joka tarvitsee niitä. Korjaa joitakin ongelmia Outlook Expressin esikatseluruudun ollessa käytössä.
* NVDA:han on lisätty komentoriviparametreja:
-m, --minimal: käynnistys- ja lopetusääniä ei toisteta eikä käyttöliittymää näytetä käynnistettäessä, jos niin on määritelty
-q, --quit: Sulkee käynnissä olevan NVDA:n
-s, --stderr-file tiedostonimi: määrittää, minne NVDA tallentaa tiedot kohdatuista virheistä ja poikkeuksista
-d, --debug-file tiedostonimi: määrittää, minne NVDA:n virheenkorjausilmoitukset tallennetaan
-c, --config-file: määritttää vaihtoehtoisen asetustiedoston
-h, -help: näyttää ohjeen, joka luettelee kaikki komentoriviparametrit
* Korjattu bugi, joka aiheutti sen, ettei välimerkkien nimiä käännetty asianmukaiselle kielelle käytettäessä NVDA:ta muuna kuin englanninkielisenä ja kirjoitettujen merkkien lukemisen ollessa käytössä.
* Lisätty  slovakinkielinen käännös.
* Lisätty asetusvalintaikkunat näennäispuskureille ja asiakirjaen muotoilulle.
* Lisätty ranskankielinen käännös.
* Lisätty komento Insert+U, joka ottaa käyttöön ja poistaa käytöstä edistymispalkkien ilmaisemisen äänimerkeillä.
* Useampien NVDA:n ilmoitusten kääntäminen eri kielille on nyt mahdollista. Näihin kuuluvat näppäinohjeen komentojen kuvaukset.
* Lisätty Internet Explorerin ja Firefoxin näennäispuskureihin Etsi-valintaikkuna. Verkkosivulla Ctrl+F:n painaminen avaa valintaikkunan, johon voidaan kirjoittaa haettava teksti. Enterin painaminen aloittaa haun ja sijoittaa kohdistimen riville, jolta haettu teksti löytyy. Annetun tekstin seuraavaa esiintymää voidaan etsiä painamalla F3.
* Kun "Puhu kirjoitetut merkit" -asetus on käytössä, useampien merkkien puhuminen pitäisi nyt olla mahdollista. Teknisesti ottaen ASCII-merkit väliltä 32 - 255 voidaan nyt puhua.
* Uudelleennimetty joitakin säädintyyppejä luettavuuden parantamiseksi. Muokattava teksti on nyt muokattava, runko on nyt puunäkymä ja painonappi on nyt painike.
* Nuolinäppäimillä liikkumisen nopeuttamiseksi luettelon tai puunäkymän kohteissa säädinn tyyppiä (luettelon tai puunäkymän kohdetta) ei enää lueta.
* Ilmoitus "sisältää ponnahdusvalikon", joka ilmaisee, että valikossa on alivalikko, ilmoitetaan nyt alivalikkona.
* NVDA voi nyt lukea joissakin kielissä Ctrl- ja Alt (tai AltGr) -näppäimien avulla tehtävät erikoismerkit kirjoitettujen merkkien lukemisen ollessa käytössä.
* Korjattu joitakin ongelmia staattisten tekstisäädinten tarkastelussa.
* Lisätty perinteisen Kiinan käännös.
* Uudelleenjärjestetty tärkeä osa NVDA:n koodista, jonka pitäisi korjata useita NVDA:n käyttöliittymän ongelmia (asetusvalintaikkunat mukaan lukien).
* Lisätty SAPI4-tuki. Ajureita on kaksi, yksi Serotek Corporationin lahjoittamaan koodiin perustuva ja yksi ActiveVoice.ActiveVoice-COM-rajapintaa käyttävä ajuri. Molemmissa on ongelmia, joten kannattaa kokeilla, kumpi toimii kenelläkin parhaiten.
* NVDA:n uuden kopion käynnistäminen vanhan ollessa vielä käynnissä sulkee uuden kopion. Tämä korjaa suuren ongelman, jossa usean NVDA-kopion käyttäminen tekee järjestelmästä käyttökelvottoman.
* NVDA-käyttöliittymän nimi on nyt pelkkä NVDA.
* Korjattu Ongelma Outlook Expressissä, jossa askelpalauttimen painaminen muokattavan viestin alussa aiheutti virheen.
* Lisätty komento kannettavien akun tilan lukemiseen (Insert+Shift+B).
* Lisätty Ei puhetta -syntetisaattoriajuri. Tällä ajurilla NVDA:n saa pysymään koko ajan täysin hiljaa. Tätä voidaan käyttää yhdessä pistenäyttötuen kanssa, kunhan sellainen tulee.
* Puhesyntetisaattoreille lisätty asetus "Nosta äänenkorkeutta isojen kirjainten kohdalla"
* Lue hiiren alla oleva objekti -komento on nyt enemmän muiden asetuskomentojen kaltainen (ilmoittaa päällä/pois sen sijaan, että koko ilmoitus muuttuu).
* Lisätty espanjankielinen käännös.
* Lisätty unkarinkielinen käännös.
* Lisätty portugalinkielinen käännös.
* Puheäänen vaihtaminen Ääniasetukset-valintaikkunasta asettaa nyt nopeus-, korkeus- ja voimakkuus-liukusäätimet vanhojen arvojen sijasta puhesyntetisaattorin mukaisiin uusiin arvoihin. Tämä korjaa ongelmia, jotka saivat esimerkiksi IBM ViaVoice -syntetisaattorin puhumaan paljon muita nopeammin.
* Korjattu bugi, joka aiheutti konsoli-ikkunoissa puheen keskeytymisen tai NVDA:n täydellisen kaatumisen.
* NVDA:n käyttöliittymä voidaan näyttää ja ilmoitukset puhua automaattisesti Windowsin käyttämällä kielellä, jos NVDA:ssa vain on tuki kyseiselle kielelle. Kieli voidaan myös edelleen valita manuaalisesti Käyttöliittymän asetukset -valintaikkunasta.
* Lisätty komento "Puhu dynaamisen sisällön muutokset" (Insert+5). Tämä asetus määrittää, luetaanko ruudulle tuleva uusi teksti tai muut dynaamiset muutokset automaattisesti. Toimii toistaiseksi vain konsoli-ikkunoissa.
* Lisätty Komento "järjestelmäkohdistin siirtää tarkastelukohdistinta" (Insert+6). Tämä asetus määrittää, siirretäänkö tarkastelukohdistinta automaattisesti järjestelmäkohdistimen mukana. Tästä on hyötyä luettaessa tietoja päivittyvältä ruudulta konsoli-ikkunoissa.
* Lisätty komento "kohdistus siirtää navigointiobjektia" (Insert+7). Tämä asetus määrittää, siirretäänkö navigointiobjektia kohdistuksen mukana.
* Lisätty eri kielille käännettyjä ohjeita, tähän mennessä ranskaksi, espanjaksi ja suomeksi.
* Kehittäjille tarkoitettu dokumentaatio poistettu NVDA:n binääriversioista.
* Korjattu Windows Live Messengerin ja MSN Messengerin bugi, joka aiheutti virheitä liikuttaessa yhteystietoluettelossa nuolinäppäimillä ylös ja alas.
* Uudet viestit luetaan nyt automaattisesti Windows Live Messengerissä. Toimii toistaiseksi vain englanninkielisissä versioissa.
* Windows Live Messengerin keskusteluhistoriaikkunaa voidaan nyt lukea nuolinäppäimillä. Toimii toistaiseksi vain englanninkielisissä versioissa.
* Lisätty komento "Ohita seuraava näppäinpainallus" (Insert+F2). Kun tätä näppäinyhdistelmää painetaan, seuraavaksi painettu näppäin välitetään suoraan Windowsin käsiteltäväksi. Tästä on hyötyä sovelluksissa, joissa on painettava jotain sellaista näppäinyhdistelmää, joka on NVDA:n käytössä.
* NVDA ei enää jumiudu yli minuutiksi avattaessa suuria asiakirjoja Wordissa.
* Korjattu ongelma, joka aiheutti Wordissa pois taulukosta ja takaisin siirryttäessä sen, ettei nykyistä rivin ja sarakkeen numeroa luettu, jos siirryttiin takaisin samaan soluun.
* Jos NVDA:ta käynnistettäessä on käytössä puhesyntetisaattori, jota ei ole tai joka ei toimi, jokin SAPI 5 -syntetisaattori yritetään ladata sen sijaan. Jos sellaisen lataaminen ei onnistu, käytettäväksi syntetisaattoriksi asetetaan "ei puhetta".
* Puheen nopeutus- ja hidastuskomennot eivät voi enää  muuttaa nopeutta arvoihin, jotka ovat yli 100 tai alle 0.
* Käyttäjälle ilmoitetaan, jos käyttöliittymän asetusvalintaikkunasta valitun kielen kielitiedostossa on virheitä.
* Jos kieltä on vaihdettu käyttöliittymän asetusvalintaikkunassa, käyttäjältä kysytään, tallennetaanko asetukset ja käynnistetäänkö NVDA uudelleen. NVDA on käynnistettävä uudelleen, jotta uusi kieli voidaan ottaa käyttöön.
* Jos puhesyntetisaattoria ei voida ladata, kun se valitaan Syntetisaattori-valintaikkunasta, siitä ilmoittava viestiruutu näytetään.
* Kun puhesyntetisaattori ladataan ensimmäistä kertaa, NVDA antaa sen valita sopivimmat puheääni-, nopeus- ja korkeusparametrit sen sijaan, että se pakotetaan NVDA:n valitsemiin oletuksiin. Tämä korjaa ongelman, jossa Eloquence- ja ViaVoice SAPI 4 -syntetisaattorit alkavat puhua aivan liian nopeasti.
