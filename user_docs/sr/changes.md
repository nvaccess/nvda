# NVDA šta je novo


## 2024.2

Dodata je nova opcija razdvajanje zvuka.
Ovo vam dozvoljava da odvojite  NVDA na jednom kanalu (na primer levom) a zvukove svih ostalih aplikacija  prebacite na drugi (na primer desni).

Dodate su nove komande za menjanje vrednosti u krugu podešavanja govora, koje dozvoljavaju korisnicima da skoče na prvo ili poslednje podešavanje, ili da povećaju ili smanje trenutno podešavanje većim skokom.
Dodate su takođe nove komande brze navigacije, one dozvoljavaju korisnicima da dodaju prečice kako bi brzo skakali između: Pasusa, vertikalno poravnatih pasusa, teksta istog stila, teksta različitog stila, stavki menija, dugmadi prekidača, traka napredovanja, figura i matematičkih formula.

Dodate su brojne nove karakteristike za brajeve redove i ispravljene greške.
Dodat je novi brajev režim "Prikaži govor".
Kada je aktivan, brajev red će prikazati tačno ono što NVDA izgovara.
Takođe je dodata podrška za BrailleEdgeS2 i BrailleEdgeS3 brajeve uređaje.
LibLouis je ažuriran, dodajući nove detaljne (uz indikaciju velikih slova) beloruske i ukrajinske brajeve tabele, lao  tabelu i  špansku tabelu za čitanje grčkih tekstova.

eSpeak je ažuriran, dodajući novi tigrinjski jezik.

Postoje brojne ispravke za sitne greške u aplikacijama, kao što su Thunderbird, Adobe Reader, Web pretraživači, Nudi i Geekbench.

### Nove karakteristike

* Nove prečice:
  * Nova komanda brze navigacije `p` za skakanje na sledeći ili prethodni pasus teksta u režimu pretraživanja. (#15998, @mltony)
  * Nove komande brze navigacije bez dodeljene prečice, koje se mogu koristiti za skakanje na sledeće ili prethodne:
    * Figure (#10826)
    * Vertikalno poravnate pasuse (#15999, @mltony)
    * Stavke menija (#16001, @mltony)
    * Dugmadi prekidača (#16001, @mltony)
    * Trake napredovanja (#16001, @mltony)
    * Matematičke formule (#16001, @mltony)
    * Tekst istog stila (#16000, @mltony)
    * Tekst različitog stila (#16000, @mltony)
  * Dodate komande za skakanje na prvu ili poslednju vrednost, ili za veći skok pri menjanju podešavanja u krugu podešavanja govora. (#13768, #16095, @rmcpantoja)
    * Podešavanje prve ili poslednje vrednosti u krugu podešavanja govora nema dodeljenu prečicu. (#13768)
    * Smanji ili povećaj trenutno podešavanje u krugu podešavanja govora većim skokom (#13768):
      * Desktop: `NVDA+kontrol+pageUp` ili `NVDA+kontrol+pageDown`.
      * Laptop: `NVDA+kontrol+šift+pageUp` ili `NVDA+kontrol+šift+pageDown`.
  * Dodata nova komanda bez dodeljene prečice za uključivanje ili isključivanje prijavljivanja figura i naslova slika. (#10826, #14349)
* Brajevi redovi:
  * Dodata podrška za BrailleEdgeS2 i BrailleEdgeS3 brajeve redove. (#16033, #16279, @EdKweon)
  * Dodat je novi brajev režim "Prikaži govor". (#15898, @Emil-18)
    * Kada je aktivan, na brajevom redu će se prikazati ono što NVDA izgovara.
    * Može se uključiti ili isključiti prečicom `NVDA+alt+t`, ili iz dijaloga brajevih podešavanja.
* Razdvajanje zvuka: (#12985, @mltony)
  * Dozvoljava da odvojite NVDA zvukove na jednom kanalu (na primer levom) dok su zvukovi drugih aplikacija na drugom kanalu (na primer desnom).
  * Uključuje se ili isključuje prečicom `NVDA+alt+s`.
* Prijavljivanje zaglavlja redova i kolona je sada podržano u contenteditable HTML elementima. (#14113)
* Dodata opcija kako biste onemogućili prijavljivanje figura i naslova slika u podešavanjima formatiranja dokumenta. (#10826, #14349)
* U Windowsu 11, NVDA će izgovarati upozorenja glasovnog unosa i predloženih radnji uključujući predlog na vrhu kada kopirate podatke kao što su brojevi telefona u privremenu memoriju (Windows 11 2022 ažuriranje i novija). (#16009, @josephsl)
* NVDA će održavati zvučni uređaj budnim nakon što se govor zaustavi, kako bi sprečio da početak sledećeg izgovorenog teksta bude isprekidan sa nekim zvučnim uređajima kao što su Bluetooth slušalice. (#14386, @jcsteh, @mltony)
* HP Secure pretraživač je sada podržan. (#16377)

### Promene

* Prodavnica dodataka:
  * Minimalna i poslednja testirana NVDA verzija za dodatak se sada prikazuju u sekciji "Drugi detalji". (#15776, @Nael-Sayegh)
  * Radnja za recenzije zajednice će biti dostupna na svim karticama prodavnice. (#16179, @nvdaes)
* Ažurirane komponente:
  * Ažuriran LibLouis brajev prevodilac na [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Nove detaljne (uz indikaciju velikih slova) beloruske i ukrajinske brajeve tabele.
    * Nova španska tabela za čitanje grčkih tekstova.
    * Nova tabela za lao stepen 1. (#16470)
  * eSpeak NG je ažuriran na 1.52-dev commit `cb62d93fd7`. (#15913)
    * Dodat novi tigrinjski jezik. 
* Promenjeno nekoliko prečica za BrailleSense uređaje kako bi se sprečili konflikti sa znakovima francuske brajeve tabele. (#15306)
  * `alt+strelicaLevo` je sada  `tačka2+tačka7+razmak`
  * `alt+strelicaDesno` je sada `tačka5+tačka7+razmak`
  * `alt+strelicaGore` je sada `tačka2+tačka3+tačka7+razmak`
  * `alt+strelicaDole` je sada `tačka5+tačka6+tačka7+razmak`
* Nizovi tačaka koji se često koriste u sadržaju teksta se više ne prijavljuju na nivoima izgovora manje interpunkcije. (#15845, @CyrilleB79)

### Ispravljene greške

* Windows 11 ispravke:
  * NVDA će ponovo izgovarati predloge za unos sa hardverske tastature. (#16283, @josephsl)
  * U verziji 24H2 (2024 ažuriranje i Windows Server 2025), interakcija mišem ili ekranom osetljivim na dodir se može koristiti u brzim podešavanjima. (#16348, @josephsl)
* Prodavnica dodataka:
  * Kada pritisnete `ctrl+tab`, fokus se ispravno prebacuje na novi naziv trenutne kartice. (#14986, @ABuffEr)
  * Ako datoteke keša nisu ispravne, NVDA se neće neprekidno restartovati. (#16362, @nvdaes)
* Ispravke za pretraživače zasnovane na Chromiumu kada se koriste uz UIA:
  * Ispravljene greške koje su izazvale da se NVDA zamrzne. (#16393, #16394)
  * Backspace taster sada ispravno radi u Gmail poljima za prijavljivanje. (#16395)
* Taster Backspace sada ispravno radi kada koristite Nudi 6.1 uz omogućeno NVDA podešavanje  "Kontroliši tastere iz drugih aplikacija". (#15822, @jcsteh)
* Ispravljena greška koja je izazivala da se zvučni koordinati reprodukuju dok je aplikacija u režimu spavanja kada je omogućeno podešavanje "Reprodukuj zvučne koordinate kada se miš pomera". (#8059, @hwf1324)
* U Adobe Readeru, NVDA više ne ignoriše alternativni tekst koji je podešen za formule u PDF datotekama. (#12715)
* Ispravljena greška koja je izazvala da NVDA ne može da pročita traku menija i opcije u programu Geekbench. (#16251, @mzanm)
* Ispravljena retka situacija u kojoj čuvanje podešavanja ne uspe da sačuva sve profile. (#16343, @CyrilleB79)
* U Firefoxu i pretraživačima zasnovanim na Chromiumu, NVDA će ispravno ući u režim fokusiranja kada se pritisne enter u prezentacionoj listi (ul / ol) u sadržaju koji se može uređivati. (#16325)
* Promena stanja kolona se ispravno prijavljuje kada se biraju kolone za prikazivanje u listi poruka programa Thunderbird. (#16323)
* Opcija komandne linije `-h`/`--help` ponovo ispravno radi. (#16522, @XLTechie)
* NVDA podrška za Poedit program za prevođenje u verziji 3.4 ili novijim ispravno funkcioniše kada se prevodi na jezike koji imaju jednu ili više od dve množine (na primer kineski, poljski, srpski). (#16318)

### Promene za programere (engleski)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Added a how-to document, explaining the process of building NVDA forks on AppVeyor. (#16293, @XLTechie)

## 2024.1

Dodat je novi režim govora "Na zahtev".
Kada je govor podešen na zahtev, NVDA ne govori automatski (na primer pri pomeranju kursora) ali govori kada se koriste komande koje imaju za cilj da nešto prijave (na primer komanda za prijavljivanje naslova prozora). 
U kategoriji govor NVDA podešavanja, sada je moguće izuzeti neželjene režime govora iz komande koja kruži kroz režime govora (`NVDA+s`).

U NVDA režimu pretraživanja programa Mozilla Firefox Dostupan je novi režim ugrađenog izbora (uključuje se i isključuje prečicom  `NVDA+šift+f10`).
Kada se uključi, izbor teksta u režimu pretraživanja će takođe menjati izbor teksta ugrađen u program Mozilla Firefox.
Kopiranje teksta prečicom  `kontrol+c` će se proslediti u Firefox, što će kopirati formatiranje sadržaja, a ne običan tekst koji NVDA prikazuje.

Prodavnica dodataka sada podržava istovremene radnje za više dodataka (na primer instalacija, omogućavanje dodataka) tako što izaberete više dodataka
Dodata je nova radnja za otvaranje Web stranice sa recenzijama za izabrani dodatak.

Opcije za izbor izlaznog uređaja reprodukcije zvukova i režima stišavanja pozadinskih zvukova su uklonjene iz dijaloga "Izaberi sintetizator".
Ove opcije se mogu pronaći u panelu podešavanja zvuka koji se može otvoriti prečicom `NVDA+kontrol+u`.

eSpeak-NG, LibLouis brajev prevodilac i Unicode CLDR su ažurirani.
Dostupne su nove tajlandske, filipinske i rumunske brajeve tabele.

Ispravljene su mnoge greške, posebno vezane za prodavnicu dodataka, brajeve redove, Libre Office, Microsoft Office i zvuk.

### Važne napomene

* Postojeći dodaci nisu kompatibilni uz ovu verziju.
* Windows 7 i Windows 8 više nisu podržani.
Windows 8.1 je minimalna podržana verzija Windowsa.

### Nove karakteristike

* Prodavnica dodataka:
  * Prodavnica dodataka sada podržava istovremeno izvršavanje radnji (na primer instalaciju, omogućavanje dodataka) biranjem više dodataka. (#15350, #15623, @CyrilleB79)
  * Dodata je nova radnja koja otvara Web stranicu na kojoj možete videti ili pružati povratne informacije za izabrani dodatak. (#15576, @nvdaes)
* Dodata podrška za Bluetooth Low Energy HID brajeve redove. (#15470)
* U NVDA režimu pretraživanja programa Mozilla Firefox Dostupan je novi režim ugrađenog izbora (uključuje se i isključuje prečicom  `NVDA+šift+f10`).
Kada se uključi, izbor teksta u režimu pretraživanja će takođe menjati izbor teksta ugrađen u program Mozilla Firefox.
Kopiranje teksta prečicom  `kontrol+c` će se proslediti u Firefox, što će kopirati formatiranje sadržaja, a ne običan tekst koji NVDA prikazuje.
Međutim, imajte na umu da budući da će Firefox obrađivati samo kopiranje, NVDA neće prijavljivati poruku "Kopirano u privremenu memoriju" u ovom režimu. (#15830)
* Kada kopirate tekst u programu Microsoft Word uz omogućen NVDA režim pretraživanja, tekst sada uključuje formatiranje.
Kao rezultat ovoga NVDA više neće prijavljivati poruku "Kopirano u privremenu memoriju" kada se pritisne `kontrol+c` u programima Microsoft Word / Outlook u režimu pretraživanja, budući da aplikacija sada obrađuje kopiranje, ne NVDA. (#16129)
* Dodat je novi režim govora "Na zahtev".
Kada je režim govora podešen na zahtev, NVDA ne govori automatski (na primer pri pomeranju kursora) ali govori kada se koriste komande koje za cilj imaju da nešto prijave (na primer prijavi naslov prozora). (#481, @CyrilleB79)
* U kategoriji govor NVDA podešavanja, sada je moguće da izuzmete neželjene režime govora iz komande koja kruži kroz režime govora (`NVDA+s`). (#15806, @lukaszgo1)
  * Ako trenutno koristite dodatak NoBeepsSpeechMode možete razmotriti njegovu deinstalaciju, a umesto toga možete onemogućiti režime "Pištanja" i "Na zahtev"  u podešavanjima.

### Promene

* NVDA više ne podržava Windows 7 i Windows 8.
Windows 8.1 je minimalna podržana verzija Windowsa. (#15544)
* Ažurirane komponente:
  * Ažuriran LibLouis brajev prevodilac na [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Dodate nove tajlandske, rumunske i filipinske brajeve tabele.
  * eSpeak NG je ažuriran na 1.52-dev commit `530bf0abf`. (#15036)
  * CLDR definicije emoji znakova i simbola su ažurirane na verziju 44.0. (#15712, @OzancanKaratas)
  * Ažuriran Java Access Bridge na 17.0.9+8Zulu (17.46.19). (#15744)
* Tasterske prečice:
  * Sledeće komande sada podržavaju mogućnost pritiskanja dva ili tri puta za sricanje prijavljenih informacija i sricanje uz opise znakova: Prijavljivanje izbora, prijavljivanje teksta u privremenoj memoriji i prijavljivanje trenutno fokusiranog objekta. (#15449, @CyrilleB79)
  * Komanda za uključivanje ili isključivanje zatamnjivanja ekrana sada ima podrazumevanu prečicu: `NVDA+kontrol+escape`. (#10560, @CyrilleB79)
  * Kada se pritisne četiri puta, komanda za prijavljivanje izbora sada prikazuje izbor u poruci režima pretraživanja. (#15858, @Emil-18)
* Microsoft Office:
  * Kada se zahtevaju informacije o formatiranju Excel ćelija, granice i pozadina će se prijavljivati samo ako postoji takvo formatiranje. (#15560, @CyrilleB79)
  * NVDA ponovo neće više prijavljivati grupisanja bez oznake kakva se mogu pronaći u najnovijim verzijama Microsoft Office 365 menija. (#15638)
* Opcije za izlazni uređaj reprodukcije zvukova i režim stišavanja pozadinskih zvukova su uklonjene iz dijaloga "Izaberi sintetizator".
Mogu se pronaći u panelu podešavanja zvuka koji se može otvoriti prečicom `NVDA+kontrol+u`. (#15512, @codeofdusk)
* Opcija "Prijavi funkciju kada miš uđe u objekat" u NVDA podešavanjima miša je preimenovana u "Prijavi objekat kada miš uđe u njega".
Ova opcija sada izgovara dodatne bitne informacije o objektu kada miš uđe u njega, kao što su stanja (označeno/pritisnuto) ili koordinate ćelija u tabeli. (#15420, @LeonarddeR)
* Dodate su nove stavke u meni pomoći za NV Access "Get Help" stranicu i prodavnicu. (#14631)
* NVDA podrška za [Poedit](https://poedit.net) je redizajnirana za Poedit verziju 3 i novije.
Korisnicima Poedita 1 preporučuje se ažuriranje na Poedit 3 ako žele da se oslanjaju na poboljšanu pristupačnost u Poeditu, kao što su prečice za čitanje napomena za prevodioce i komentara. (#15313, #7303, @LeonarddeR)
* Pregled govora i pregled brajevog reda su sada onemogućeni u bezbednom režimu. (#15680)
* Tokom navigacije objekata, onemogućeni (nedostupni) objekti više neće biti ignorisani. (#15477, @CyrilleB79)
* Dodat sadržaj u dokument kratkih napomena o komandama. (#16106)

### Ispravljene greške

* Prodavnica dodataka:
  * Kada se status dodatka promeni dok je fokusiran, na primer promena iz "Preuzimanje" u "Preuzeto", ažurirana stavka se sada ispravno izgovara. (#15859, @LeonarddeR)
  * Kada se instaliraju dodaci zahtevi za instalaciju više neće biti preklopljeni dijalogom za ponovno pokretanje. (#15613, @lukaszgo1)
  * Kada se ponovo instalira nekompatibilan dodatak on više neće biti prisilno onemogućen. (#15584, @lukaszgo1)
  * Onemogućeni i nekompatibilni dodaci se sada mogu ažurirati. (#15568, #15029)
  * NVDA se sada oporavlja i prikazuje grešku u slučaju u kojem se dodatak ne preuzme ispravno. (#15796)
  * NVDA više neće imati povremenih problema da se ponovo pokrene nakon što se prodavnica dodataka otvori i zatvori. (#16019, @lukaszgo1)
* Zvuk:
  * NVDA se više ne zamrzava kratkotrajno kada se više zvukova reprodukuje jedan nakon drugog u kratkom vremenskom periodu. (#15311, #15757, @jcsteh)
  * Ako se izlazni uređaj za reprodukciju zvukova podesi na neki uređaj koji nije podrazumevani i taj uređaj ponovo postane dostupan nakon što je bio nedostupan, NVDA će se sada vratiti na podešeni uređaj umesto da nastavi da koristi podrazumevani uređaj. (#15759, @jcsteh)
  * NVDA sada nastavlja da reprodukuje zvukove ako se podešavanje izlaznog uređaja promeni ili neka druga aplikacija oslobodi uređaj od ekskluzivne kontrole uređaja. (#15758, #15775, @jcsteh)
* Brajevi redovi:
  * Brajevi redovi sa više redova više neće rušiti BRLTTY drajver i tretiraju se kao jedan neprekidan brajev red. (#15386)
  * Više objekata koji sadrže koristan tekst se prepoznaje, a tekstualni sadržaj se prikazuje na brajevom redu. (#15605)
  * Skraćeni brajev unos ponovo ispravno radi. (#15773, @aaclause)
  * Brajev red će se sada ažurirati kada se navigacioni objekat pomera između ćelija tabele u većem broju slučajeva (#15755, @Emil-18)
  * Rezultat prijavljivanja trenutnog fokusa, trenutnog navigacionog objekta i komandi za prijavljivanje trenutnog izbora se sada prikazuje na brajevom redu. (#15844, @Emil-18)
  * Albatross brajev drajver više ne obrađuje Esp32 mikrokontroler kao Albatross brajev red. (#15671)
* LibreOffice:
  * Reči koje se obrišu prečicom `kontrol+backspace` se sada takođe ispravno izgovaraju kada obrisanu reč prati prazan prostor (kao što su razmaci ili tabulatori). (#15436, @michaelweghorn)
  * Izgovor statusne trake korišćenjem prečice `NVDA+end` sada takođe radi u dijalozima LibreOffice verzije 24.2 i novijih. (#15591, @michaelweghorn)
  * Svi očekivani atributi teksta su sada podržani uz LibreOffice verzije 24.2 i novije.
  Ovo znači da će izgovor pravopisnih grešaka sada raditi kada se izgovara red u pisaču/Writeru. (#15648, @michaelweghorn)
  * Izgovor nivoa naslova sada takođe radi za LibreOffice verzije 24.2 i novije. (#15881, @michaelweghorn)
* Microsoft Office:
  * U Excelu uz UIA onemogućen, brajev red će se ažurirati i  sadržaj aktivne ćelije će se izgovarati kada se pritisnu prečice `kontrol+y`, `kontrol+z` ili `alt+backspace`. (#15547)
  * U Wordu uz UIA onemogućen brajev red će se ažurirati kada se pritisnu prečice `kontrol+v`, `kontrol+x`, `kontrol+y`, `kontrol+z`, `alt+backspace`, `backspace` ili `kontrol+backspace`.
  Takođe će se ažurirati uz UIA omogućen kada pišete tekst a brajev je vezan za pregled i pregled prati sistemski kursor. (#3276)
  * U Wordu, ćelija na koju stanete će se sada ispravno prijavljivati kada koristite ugrađene Word komande za navigaciju po tabeli `alt+home`, `alt+end`, `alt+pageUp` i `alt+pageDown`. (#15805, @CyrilleB79)
* Prijavljivanje tasterskih prečica za objekte je poboljšano. (#10807, #15816, @CyrilleB79)
* SAPI4 sintetizator sada ispravno podržava promene jačine, brzine i visine koje su umetnute u govoru. (#15271, @LeonarddeR)
* Mogućnost višelinijskog uređivanja se sada ispravno prijavljuje u aplikacijama koje koriste Java Access Bridge. (#14609)
* NVDA će izgovarati sadržaj dijaloga u većem broju dijaloga na Windowsu 10 i 11. (#15729, @josephsl)
* NVDA više neće imati problema sa čitanjem novo učitane stranice u programu Microsoft edge kada se koristi UI Automation. (#15736)
* Kada se koristi režim izgovori sve ili komande koje sriču tekst, pauze između rečenica ili znakova se više neće postepeno smanjivati kako vreme protiče. (#15739, @jcsteh)
* NVDA se više neće ponekad rušiti kada izgovara veliku količinu teksta. (#15752, @jcsteh)
* Kada pristupate programu Microsoft Edge uz UI Automation, NVDA može da aktivira više kontrola u režimu pretraživanja. (#14612)
* NVDA više neće imati problema da se pokrene kada je datoteka sa podešavanjima oštećena, ali vratiće podešavanja na podrazumevana što je i ranije bio slučaj. (#15690, @CyrilleB79)
* Popravljena podrška za kontrole sistemskog prikazivanja liste (`SysListView32`) u Windows Forms aplikacijama. (#15283, @LeonarddeR)
* Više nije moguće da zamenite istoriju NVDA Python konzole. (#15792, @CyrilleB79)
* NVDA bi trebao da zadrži svoj odziv kada je preplavljen mnogim UI Automation događajima, na primer kada se u Terminalu pojavljuju veliki delovi teksta ili kada slušate glasovne poruke u programu WhatsApp messenger. (#14888, #15169)
  * Ovo novo ponašanje se može onemogućiti opcijom "Koristi poboljšano obrađivanje događaja" u naprednim NVDA podešavanjima.
* NVDA ponovo može da prati fokus u aplikacijama koje su pokrenute iz Windows Defender zaštitnika aplikacija (Windows defender application guard WDAG). (#15164)
* Izgovoreni tekst se više ne ažurira kada se miš pomera u prozoru pregleda govora. (#15952, @hwf1324)
* NVDA će se ponovo vratiti u režim pretraživanja kada zatvorite izborne okvire tasterom `escape` ili prečicom `alt+strelicaGore` u programima Firefox ili Chrome. (#15653)
* Kretanje strelicama gore ili dole u izbornim okvirima u programu iTunes se više neće bespotrebno vraćati u režim pretraživanja. (#15653)

### Promene za programere (engleski)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Note: this is an Add-on API compatibility breaking release.
Add-ons will need to be re-tested and have their manifest updated.
* Building NVDA now requires Visual Studio 2022.
Please refer to the [NVDA docs](https://github.com/nvaccess/nvda/blob/release-2024.1/projectDocs/dev/createDevEnvironment.md) for the specific list of Visual Studio components. (#14313)
* Added the following extension points:
  * `treeInterceptorHandler.post_browseModeStateChange`. (#14969, @nvdaes)
  * `speech.speechCanceled`. (#15700, @LeonarddeR)
  * `_onErrorSoundRequested` (should be retrieved calling `logHandler.getOnErrorSoundRequested()`) (#15691, @CyrilleB79)
* It is now possible to use plural forms in an add-on's translations. (#15661, @beqabeqa473)
* Included python3.dll in the binary distribution for use by add-ons with external libraries utilizing the [stable ABI](https://docs.python.org/3.11/c-api/stable.html). (#15674, @mzanm)
* The `BrailleDisplayDriver` base class now has `numRows` and `numCols` properties to provide information about multi line braille displays.
Setting `numCells` is still supported for single line braille displays and `numCells` will return the total number of cells for multi line braille displays. (#15386)
* Updated BrlAPI for BRLTTY to version 0.8.5, and its corresponding python module to a Python 3.11 compatible build. (#15652, @LeonarddeR)
* Added the `speech.speakSsml` function, which allows you to write NVDA speech sequences using [SSML](https://www.w3.org/TR/speech-synthesis11/). (#15699, @LeonarddeR)
  * The following tags are currently supported and translated to appropriate NVDA speech commands:
    * `Prosody` (`pitch`, `rate` and `volume`). Only multiplication (e.g. `200%` are supported.
    * `say-as` with the `interpret` attribute set to `characters`
    * `voice` with the `xml:lang` set to an XML language
    * `break` with the `time` attribute set to a value in milliseconds, e.g. `200ms`
    * `mark` with the `name` attribute set to a mark name, e.g. `mark1`, requires providing a callback
  * Example: `speech.speakSsml('<speak><prosody pitch="200%">hello</prosody><break time="500ms" /><prosody rate="50%">John</prosody></speak>')`
  * The SSML parsing capabilities are backed by the `SsmlParser` class in the `speechXml` module.
* Changes to the NVDA Controller Client library:
  * The file names of the library no longer contain a suffix denoting the architecture, i.e. `nvdaControllerClient32/64.dll` are now called `nvdaControllerClient.dll`. (#15718, #15717, @LeonarddeR)
  * Added an example to demonstrate using nvdaControllerClient.dll from Rust. (#15771, @LeonarddeR)
  * Added the following functions to the controller client: (#15734, #11028, #5638, @LeonarddeR)
    * `nvdaController_getProcessId`: To get the process id (PID) of the current instance of NVDA the controller client is using.
    * `nvdaController_speakSsml`: To instruct NVDA to speak according to the given SSML. This function also supports:
      * Providing the symbol level.
      * Providing the priority of speech to be spoken.
      * Speaking both synchronously (blocking) and asynchronously (instant return).
    * `nvdaController_setOnSsmlMarkReachedCallback`: To register a callback of type `onSsmlMarkReachedFuncType` that is called in synchronous mode for every `<mark />` tag encountered in the SSML sequence provided to `nvdaController_speakSsml`.
  * Note: the new functions in the controller client only support NVDA 2024.1 and above.
* Updated `include` dependencies:
  * detours to `4b8c659f549b0ab21cf649377c7a84eb708f5e68`. (#15695)
  * ia2 to `3d8c7f0b833453f761ded6b12d8be431507bfe0b`. (#15695)
  * sonic to `8694c596378c24e340c09ff2cd47c065494233f1`. (#15695)
  * w3c-aria-practices to `9a5e55ccbeb0f1bf92b6127c9865da8426d1c864`. (#15695)
  * wil to `5e9be7b2d2fe3834a7107f430f7d4c0631f69833`. (#15695)
* Device info yielded by `hwPortUtils.listUsbDevices` now contain the bus reported description of the USB device (key `busReportedDeviceDescription`). (#15764, @LeonarddeR)
* For USB serial devices, `bdDetect.getConnectedUsbDevicesForDriver` and `bdDetect.getDriversForConnectedUsbDevices` now yield device matches containing a `deviceInfo` dictionary enriched with data about the USB device, such as `busReportedDeviceDescription`. (#15764, @LeonarddeR)
* When the configuration file `nvda.ini` is corrupted, a backup copy is saved before it is reinitialized. (#15779, @CyrilleB79)
* When defining a script with the script decorator, the `speakOnDemand` boolean argument can be specified to control if a script should speak while in "on-demand" speech mode. (#481, @CyrilleB79)
  * Scripts that provide information (e.g. say window title, report time/date) should speak in the "on-demand" mode.
  * Scripts that perform an action (e.g. move the cursor, change a parameter) should not speak in the "on-demand" mode.
* Fixed bug where deleting git-tracked files during `scons -c` resulted in missing UIA COM interfaces on rebuild. (#7070, #10833, @hwf1324)
* Fix a bug where some code changes were not detected when building `dist`, that prevented a new build from being triggered.
Now `dist` always rebuilds. (#13372, @hwf1324)
* A `gui.nvdaControls.MessageDialog` with default type of standard, no longer throws a None conversion exception because no sound is assigned. (#16223, @XLTechie)

#### API Breaking Changes

These are breaking API changes.
Please open a GitHub issue if your Add-on has an issue with updating to the new API.

* NVDA is now built with Python 3.11. (#12064)
* Updated pip dependencies:
  * configobj to 5.1.0dev commit `e2ba4457c4651fa54f8d59d8dcdd3da950e956b8`. (#15544)
  * Comtypes to 1.2.0. (#15513, @codeofdusk)
  * Flake8 to 4.0.1. (#15636, @lukaszgo1)
  * py2exe to 0.13.0.1dev commit `4e7b2b2c60face592e67cb1bc935172a20fa371d`. (#15544) 
  * robotframework to 6.1.1. (#15544)
  * SCons to 4.5.2. (#15529, @LeonarddeR)
  * sphinx to 7.2.6. (#15544)
  * wxPython to 4.2.2a commit `0205c7c1b9022a5de3e3543f9304cfe53a32b488`. (#12551, #16257)
* Removed pip dependencies:
  * typing_extensions, these should be supported natively in Python 3.11 (#15544)
  * nose, instead unittest-xml-reporting is used to generate XML reports. (#15544)
* `IAccessibleHandler.SecureDesktopNVDAObject` has been removed.
Instead, when NVDA is running on the user profile, track the existence of the secure desktop with the extension point: `winAPI.secureDesktop.post_secureDesktopStateChange`. (#14488)
* `braille.BrailleHandler.handlePendingCaretUpdate` has been removed with no public replacement. (#15163, @LeonarddeR)
* `bdDetect.addUsbDevices and bdDetect.addBluetoothDevices` have been removed.
Braille display drivers should implement the `registerAutomaticDetection` class method instead.
That method receives a `DriverRegistrar` object on which the `addUsbDevices` and `addBluetoothDevices` methods can be used. (#15200, @LeonarddeR)
* The default implementation of the check method on `BrailleDisplayDriver` now requires both the `threadSafe` and `supportsAutomaticDetection` attributes to be set to `True`. (#15200, @LeonarddeR)
* Passing lambda functions to `hwIo.ioThread.IoThread.queueAsApc` is no longer possible, as functions should be weakly referenceable. (#14627, @LeonarddeR)
* `IoThread.autoDeleteApcReference` has been removed. (#14924, @LeonarddeR)
* To support capital pitch changes, synthesizers must now explicitly declare their support for the `PitchCommand` in the `supportedCommands` attribute on the driver. (#15433, @LeonarddeR)
* `speechDictHandler.speechDictVars` has been removed. Use `NVDAState.WritePaths.speechDictsDir` instead of `speechDictHandler.speechDictVars.speechDictsPath`. (#15614, @lukaszgo1)
* `languageHandler.makeNpgettext` and `languageHandler.makePgettext` have been removed.
`npgettext` and `pgettext` are supported natively now. (#15546)
* The app module for [Poedit](https://poedit.net) has been changed significantly. The `fetchObject` function has been removed. (#15313, #7303, @LeonarddeR)
* The following redundant types and constants have been removed from `hwPortUtils`: (#15764, @LeonarddeR)
  * `PCWSTR`
  * `HWND` (replaced by `ctypes.wintypes.HWND`)
  * `ULONG_PTR`
  * `ULONGLONG`
  * `NULL`
  * `GUID` (replaced by `comtypes.GUID`)
* `gui.addonGui.AddonsDialog` has been removed. (#15834)
* `touchHandler.TouchInputGesture.multiFingerActionLabel` has been removed with no replacement. (#15864, @CyrilleB79)
* `NVDAObjects.IAccessible.winword.WordDocument.script_reportCurrentHeaders` has been removed with no replacement. (#15904, @CyrilleB79)
* The following app modules are removed.
Code which imports from one of them, should instead import from the replacement module. (#15618, @lukaszgo1)

| Removed module name |Replacement module|
|---|---|
|`azardi-2.0` |`azardi20`|
|`azuredatastudio` |`code`|
|`azuredatastudio-insiders` |`code`|
|`calculatorapp` |`calculator`|
|`code - insiders` |`code`|
|`commsapps` |`hxmail`|
|`dbeaver` |`eclipse`|
|`digitaleditionspreview` |`digitaleditions`|
|`esybraille` |`esysuite`|
|`hxoutlook` |`hxmail`|
|`miranda64` |`miranda32`|
|`mpc-hc` |`mplayerc`|
|`mpc-hc64` |`mplayerc`|
|`notepad++` |`notepadPlusPlus`|
|`searchapp` |`searchui`|
|`searchhost` |`searchui`|
|`springtoolsuite4` |`eclipse`|
|`sts` |`eclipse`|
|`teamtalk3` |`teamtalk4classic`|
|`textinputhost` |`windowsinternal_composableshell_experiences_textinput_inputapp`|
|`totalcmd64` |`totalcmd`|
|`win32calc` |`calc`|
|`winmail` |`msimn`|
|`zend-eclipse-php` |`eclipse`|
|`zendstudio` |`eclipse`|

#### Deprecations

* Using `watchdog.getFormattedStacksForAllThreads` is deprecated - please use `logHandler.getFormattedStacksForAllThreads` instead. (#15616, @lukaszgo1)
* `easeOfAccess.canConfigTerminateOnDesktopSwitch` has been deprecated, as it became obsolete since Windows 7 is no longer supported. (#15644, @LeonarddeR)
* `winVersion.isFullScreenMagnificationAvailable` has been deprecated - use `visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart` instead. (#15664, @josephsl)
* The following Windows release constants has been deprecated from winVersion module (#15647, @josephsl):
  * `winVersion.WIN7`
  * `winVersion.WIN7_SP1`
  * `winVersion.WIN8`
* The `bdDetect.KEY_*` constants have been deprecated.
Use `bdDetect.DeviceType.*` instead. (#15772, @LeonarddeR).
* The `bdDetect.DETECT_USB` and `bdDetect.DETECT_BLUETOOTH` constants have been deprecated with no public replacement. (#15772, @LeonarddeR).
* Using `gui.ExecAndPump` is deprecated - please use `systemUtils.ExecAndPump` instead. (#15852, @lukaszgo1)

## 2023.3.4

Ovo je manje ažuriranje za ispravku bezbednosnog problema i problema sa instalacijom.
Molimo odgovorno prijavite bezbednosne probleme tako što ćete pratiti [politiku bezbednosti programa NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Bezbednosne ispravke

* Sprečava učitavanje prilagođene konfiguracije kada je prisiljen bezbedni režim.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Ispravljene greške

* Ispravljena greška koja je izazvala da NVDA proces ne izađe ispravno. (#16123)
* Ispravljena greška koja je izazvala da ako prethodni NVDA proces nije uspeo da se ispravno zatvori, NVDA instalacija je mogla da bude neuspešna bez oporavka. (#16122)

## 2023.3.3

Ovo je manje ažuriranje za ispravljanje bezbednosnog problema.
Molimo odgovorno prijavite bezbednosne probleme tako što ćete pratiti [politiku bezbednosti programa NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Bezbednosne ispravke

* Sprečavanje da mogući reflektovani XSS napad iz  prilagođenog sadržaja izazove izvršavanje koda.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Ovo je manje ažuriranje za ispravljanje bezbednosnog problema.
Bezbednosna ispravka u verziji 2023.3.1 nije ispravno rešila problem.
Molimo odgovorno prijavite bezbednosne probleme tako što ćete pratiti [politiku bezbednosti programa NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Bezbednosne ispravke

* Bezbednosna ispravka u verziji 2023.3.1 nije ispravno rešila problem.
Sprečava mogući pristup sistemu i izvršavanje koda sa sistemskim privilegijama za korisnike koji nisu autorizovani.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Ovo je manje ažuriranje za ispravljanje bezbednosnog problema.
Molimo odgovorno prijavite bezbednosne probleme tako što ćete pratiti [politiku bezbednosti programa NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Bezbednosne ispravke

* Sprečava mogući pristup sistemu i izvršavanje koda sa sistemskim privilegijama za korisnike koji nisu autorizovani.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Ova verzija uključuje poboljšanja u performansama, odzivu i stabilnosti zvukova.
Dodate su opcije za kontrolisanje jačine NVDA zvukova i pištanja, ili da ove jačine prate jačinu glasa kojeg koristite.

NVDA sada može povremeno da osvežava OCR rezultate, izgovarajući novi tekst kada se pojavi.
Ovo se može podesiti u Windows OCR kategoriji NVDA dijaloga podešavanja.

Sadrži nekoliko ispravki za brajeve redove, koje poboljšavaju prepoznavanje uređaja i pomeranje kursora.
Sada je moguće izuzeti neželjene drajvere iz automatskog prepoznavanja, kako biste poboljšali performanse automatskog prepoznavanja.
Dodate su takođe nove BRLTTY komande.

Takođe sadrži ispravljene greške za prodavnicu dodataka, Microsoft Office, Microsoft Edge kontekstne menije, i Windows Kalkulator.

### Nove karakteristike

* Poboljšano upravljanje zvukovima:
  * Novi panel podešavanja zvuka:
    * Može se otvoriti prečicom `NVDA+kontrol+u`. (#15497)
    * Opcija u podešavanjima zvuka da jačina NVDA zvukova i pištanja prati podešavanje jačine glasa kojeg koristite. (#1409)
    * Opcija u podešavanjima zvuka da odvojeno podesite jačinu NVDA zvukova. (#1409, #15038)
    * Podešavanja da promenite izlazni uređaj zvukova i režim stišavanja pozadinskih zvukova su premeštena u novi panel podešavanja zvuka iz dijaloga za izbor sintetizatora.
    Ove opcije će biti uklonjene iz dijaloga "Izaberi sintetizator" u verziji 2024.1. (#15486, #8711)
  * NVDA će sada reprodukovati zvukove korišćenjem Windows Audio Session API-a (WASAPI), što može poboljšati odziv, performanse i stabilnost NVDA govora i zvukova. (#14697, #11169, #11615, #5096, #10185, #11061)
  * Napomena: WASAPI je nekompatibilan sa nekim dodacima.
  Kompatibilna ažuriranja su dostupna za ove dodatke, molimo ažurirajte ih pre nego što ažurirate NVDA.
  Nekompatibilne verzije ovih dodataka će biti onemogućene kada ažurirate NVDA:
    * Tony's Enhancements verzija 1.15 ili starija. (#15402)
    * NVDA global commands extension 12.0.8 ili starija. (#15443)
* NVDA sada može stalno da ažurira rezultat kada se vrši optičko prepoznavanje teksta (OCR), a zatim da izgovara novi tekst kada se pojavi. (#2797)
  * Da biste omogućili ovu funkciju, omogućite opciju "Povremeno osvežavaj prepoznat sadržaj" u Windows OCR kategoriji dijaloga NVDA podešavanja.
  * Nakon što je omogućena, možete uključiti ili isključiti izgovor novog teksta tako što ćete uključiti ili isključiti opciju prijavljivanja dinamičkih promena sadržaja (pritiskanjem `NVDA+5`).
* Kada se koristi automatsko prepoznavanje brajevih redova, sada je moguće izuzeti drajvere iz prepoznavanja u dijalogu za izbor brajevog reda. (#15196)
* Nova opcija u podešavanjima formatiranja dokumenta, "Zanemari prazne redove za prijavljivanje uvlačenja redova". (#13394)
* Dodata nedodeljena komanda za navigaciju po grupama kartica u režimu pretraživanja. (#15046)

### Promene

* Brajevi redovi:
  * Kada se tekst u Terminalu promeni bez ažuriranja kursora, tekst na brajevom redu će se sada ispravno ažurirati kada se nalazi na promenjenom redu.
  Ovo uključuje situacije u kojima je brajev red vezan za pregled. (#15115)
  * Još BRLTTY tasterskih kombinacija sada imaju dodeljene NVDA komande (#6483):
    * `learn`: Uključuje ili isključuje NVDA pomoć za unos
    * `prefmenu`: Otvara NVDA meni
    * `prefload`/`prefsave`: Učitava ili čuva NVDA podešavanja
    * `time`: Prikazuje vreme
    * `say_line`: Izgovara trenutni red u kojem se nalazi pregledni kursor
    * `say_below`: Izgovara sve korišćenjem preglednog kursora
  * BRLTTY drajver je dostupan samo kada je BRLTTY instanca uz BrlAPI omogućen pokrenuta. (#15335)
  * Napredno podešavanje da omogućite podršku za HID brajeve redove je uklonjeno uz zamenu novom opcijom.
  Sada možete da onemogućite određene drajvere za automatsko prepoznavanje u dijalogu za izbor brajevog reda. (#15196)
* Prodavnica dodataka: Instalirani dodaci će sada biti prikazani na kartici za dostupne dodatke, ako su dostupni u prodavnici. (#15374)
* Neke prečice u NVDA meniju su ažurirane. (#15364)

### Ispravljene greške

* Microsoft Office:
  * Ispravljeno rušenje u programu Microsoft Word kada opcije formatiranja dokumenta "Prijavi naslove" i "Prijavi komentare i napomene" nisu omogućene. (#15019)
  * U Wordu i Excelu, poravnavanje teksta će biti ispravno prijavljeno u više situacija. (#15206, #15220)
  * Ispravljen izgovor nekih prečica formatiranja ćelije u Excelu. (#15527)
* Microsoft Edge:
  * NVDA se više neće vraćati nazad na poslednju poziciju u režimu pretraživanja kada se otvori kontekstni meni u programu Microsoft Edge. (#15309)
  * NVDA ponovo može da čita kontekstne menije preuzimanja u programu Microsoft Edge. (#14916)
* Brajevi redovi:
  * Pokazivači brajevog kursora i izbora će se sada uvek ispravno ažurirati nakon što prikažete ili sakrijete odgovarajuće pokazivače komandom. (#15115)
  * Ispravljena greška u kojoj su Albatross brajevi redovi pokušavali da se učitaju iako je drugi brajev red povezan. (#15226)
* Prodavnica dodataka:
  * Ispravljena greška koja je izazivala da kada se onemogući opcija "Uključi nekompatibilne dodatke" nekompatibilni dodaci bi i dalje bili prikazani u prodavnici. (#15411)
  * Dodaci koji su blokirani zbog kompatibilnosti će se sada ispravno filtrirati kada se uključi ili isključi izdvajanje omogućenih ili onemogućenih dodataka. (#15416)
  * Ispravljena greška koja je sprečavala da nekompatibilni dodaci koji su instalirani i omogućeni budu ažurirani ili zamenjeni korišćenjem alatke za eksternu instalaciju. (#15417)
  * Ispravljena greška koja je izazivala da NVDA ne govori dok se  ponovo ne pokrene nakon instalacije dodatka. (#14525)
  * Ispravljena greška koja je izazivala da dodaci ne mogu da se instaliraju ako je prethodno preuzimanje bilo neuspešno ili je otkazano. (#15469)
  * Ispravljene greške sa obrađivanjem nekompatibilnih dodataka kada se ažurira NVDA. (#15414, #15412, #15437)
* NVDA ponovo izgovara rezultate računanja u Windows 32bitnom Kalkulatoru na serverskim, LTSC i LTSB verzijama Windowsa. (#15230)
* NVDA više ne ignoriše promene fokusa kada se nizani prozor fokusira. (#15432)
* Ispravljen mogući uzrok rušenja pri pokretanju programa NVDA. (#15517)

### Promene za programere (engleski)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* `braille.handler.handleUpdate` and `braille.handler.handleReviewMove` have been changed in order not to update instantly.
Before this change, when either of these methods was called very often, this would drain many resources.
These methods now queue an update at the end of every core cycle instead.
They should also be thread safe, making it possible to call them from background threads. (#15163)
* Added official support to register custom braille display drivers in the automatic braille display detection process.
Consult the `braille.BrailleDisplayDriver` class documentation for more details.
Most notably, the `supportsAutomaticDetection` attribute must be set to `True` and the `registerAutomaticDetection` `classmethod` must be implemented.  (#15196)

#### Deprecations

* `braille.BrailleHandler.handlePendingCaretUpdate` is now deprecated with no public replacement.
It will be removed in 2024.1. (#15163)
* Importing the constants `xlCenter`, `xlJustify`, `xlLeft`, `xlRight`, `xlDistributed`, `xlBottom`, `xlTop` from `NVDAObjects.window.excel` is deprecated.
Use `XlHAlign` or `XlVAlign` enumerations instead. (#15205)
* The mapping `NVDAObjects.window.excel.alignmentLabels` is deprecated.
Use the `displayString` methods of `XlHAlign` or `XlVAlign` enumerations instead. (#15205)
* `bdDetect.addUsbDevices` and `bdDetect.addBluetoothDevices` have been deprecated.
Braille display drivers should implement the `registerAutomaticDetection` classmethod instead.
That method receives a `DriverRegistrar` object on which the `addUsbDevices` and `addBluetoothDevices` methods can be used. (#15200)
* The default implementation of the check method on `BrailleDisplayDriver` uses `bdDetect.driverHasPossibleDevices` for devices that are marked as thread safe.
Starting from NVDA 2024.1, in order for the base method to use `bdDetect.driverHasPossibleDevices`, the `supportsAutomaticDetection` attribute must be set to `True` as well. (#15200)

## 2023.2

Ova verzija dodaje prodavnicu dodataka koja menja upravljača dodacima.
U  prodavnici dodataka možete da istražujete, pretražujete, instalirate i ažurirate dodatke zajednice.
Sada možete ručno da ignorišete probleme kompatibilnosti sa zastarelim dodacima na sopstvenu odgovornost.

Dodate su nove funkcije za brajeve redove, komande i novi podržani brajevi redovi.
Takođe su dodate nove prečice za OCR i ravnu navigaciju kroz objekte.
Navigacija i prijavljivanje formatiranja u Microsoft Office paketu je poboljšana.

Puno grešaka je ispravljeno, posebno za brajeve redove, Microsoft Office, web pretraživače i Windows 11.

eSpeak-NG, LibLouis braille translator, i Unicode CLDR su ažurirani.

### Nove karakteristike

* Prodavnica dodataka je dodata u NVDA. (#13985)
  * Istraživanje, pretraga, instalacija i ažuriranje dodataka zajednice.
  * Ručno učitajte nekompatibilne NVDA dodatke.
  * Upravljač dodataka je uklonjen i zamenjen prodavnicom dodataka.
  * za više informacija molimo pročitajte ažurirano korisničko uputstvo.
* Nove ulazne komande:
  * Komanda bez dodeljene prečice kako biste kružili kroz dostupne jezike za Windows OCR. (#13036)
  * Komanda bez dodeljene prečice kako biste kružili kroz režime prikazivanja poruka na brajevom redu. (#14864)
  * Komanda bez dodeljene prečice kako biste uključili ili isključili pokazivač izbora na brajevom redu. (#14948)
  * Dodate podrazumevane prečice na tastaturi za pomeranje na sledeći ili prethodni objekat u ravnom prikazu hierarhije objekata. (#15053)
    * Desktop: `NVDA+numeričko9` i `NVDA+numeričko3` da se pomerite na sledeći ili prethodni objekat.
    * Laptop: `šift+NVDA+[` i `šift+NVDA+]` da se pomerite na prethodni i sledeći objekat.
* Nove funkcije za brajeve redove:
  * Dodata podrška za Help Tech Activator brajev red. (#14917)
  * Nova opcija za uključivanje ili isključivanje prikazivanja pokazivača izbora (tačkice 7 i 8). (#14948)
  * Nova opcija za pomeranje sistemskog kursora ili fokusa kada se menja pozicija preglednog kursora brajevim tasterima. (#14885, #3166)
  * Kada se pritisne `numeričko2` tri puta da bi se prijavila brojčana vrednost znaka na poziciji preglednog kursora, informacija se takođe pruža na brajevom redu. (#14826)
  * Dodata podrška za `aria-brailleroledescription` ARIA 1.3 atribut, koji će dozvoliti autorima sajtova da zamene vrstu elementa koja će se prikazati na brajevom redu. (#14748)
  * Baum brajev drajver: Dodato nekoliko vezanih brajevih komandi za izvršavanje čestih prečica na tastaturi kao što su `windows+d` i `alt+tab`.
  Molimo pogledajte NVDA korisničko uputstvo za potpunu listu. (#14714)
* Dodat izgovor unikodnih simbola:
  * Brajevi simboli kao što su `⠐⠣⠃⠗⠇⠐⠜`. (#14548)
  * Simbol za Mac taster opcije `⌥`. (#14682)
* Dodate komande za Tivomatic Caiku Albatross brajeve redove. (#14844, #15002)
  * Prikazivanje dijaloga brajevih podešavanja
  * Pristup statusnoj traci
  * Menjanje oblika brajevog kursora
  * Menjanje režima prikazivanja poruka
  * Uključivanje i isključivanje brajevog kursora
  * Uključivanje i isključivanje pokazivača izbora na brajevom redu
  * Menjanje opcije "Brajevo pomeranje kursora kada se prebacuje pregledni kursor". (#15122)
* Microsoft Office funkcije:
  * Kada se omogući prijavljivanje obeleženog teksta u opcijama formatiranja dokumenta, obeležene boje se sada prijavljuju u Microsoft Wordu. (#7396, #12101, #5866)
  * Kada se omoguće boje u opcijama formatiranja dokumenta, boje pozadine se sada prijavljuju u Microsoft Wordu. (#5866)
  * Kada se koriste Excel prečice da uključite ili isključite opcije formatiranja kao što su podebljano, iskošeno, podvučeno i precrtano za ćeliju u Excelu, rezultat se sada prijavljuje. (#14923)
* Eksperimentalno poboljšano upravljanje zvukovima:
  * NVDA sada može da reprodukuje zvukove korišćenjem standarda Windows Audio Session API (WASAPI), što može poboljšati brzinu, performanse i stabilnost NVDA govora i zvukova.
  * WASAPI korišćenje se može omogućiti u naprednim podešavanjima.
  Takođe, ako je WASAPI omogućen, sledeća napredna podešavanja se mogu podesiti.
    * Opcija koja će izazvati da jačina NVDA zvukova i pištanja prati podešavanje jačine glasa kojeg koristite. (#1409)
    * Opcija da odvojeno podesite jačinu NVDA zvukova. (#1409, #15038)
  * Postoji poznat problem sa povremenim rušenjem kada je WASAPI omogućen. (#15150)
* U pretraživačima Mozilla Firefox i Google Chrome, NVDA sada prijavljuje ako kontrola otvara dijalog, mrežu, listu ili stablo ako je autor ovo označio korišćenjem `aria-haspopup`. (#14709)
* Sada je moguće koristiti sistemske varijable  (kao što su  `%temp%` ili  `%homepath%`) pri određivanju putanje kada se pravi NVDA prenosna kopija. (#14680)
* u ažuriranju Windowsa 10 iz maja 2019 i novijim, NVDA može izgovarati imena virtuelnih radnih površina kada se otvaraju, menjaju ili zatvaraju. (#5641)
* Sistemski parametar je dodat koji će dozvoliti korisnicima i administratorima sistema da nateraju NVDA da se pokrene u bezbednom režimu. (#10018)

### Promene

* Ažurirane komponente:
  * eSpeak NG je ažuriran na 1.52-dev commit `ed9a7bcf`. (#15036)
  * Ažuriran LibLouis brajev prevodilac na [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR je ažuriran na verziju 43.0. (#14918)
* LibreOffice promene:
  * Kada se prijavljuje lokacija preglednog kursora, trenutna lokacija kursora se sada prijavljuje u odnosu na trenutnu stranicu u programu LibreOffice Writer za LibreOffice verzije 7.6 i novije, slično prijavljivanju u programu Microsoft Word. (#11696)
  * Kada se prebacite na neku drugu ćeliju u programu LibreOffice Calc, NVDA više neće neispravno izgovarati koordinate prethodno fokusirane ćelije kada se izgovor koordinata ćelija onemogući u NVDA podešavanjima. (#15098)
  * Izgovor statusne trake (na primer kada se pritisne `NVDA+end`) radi u paketu LibreOffice. (#11698)
* Brajeve promene:
  * Kada se koristi brajev red uz drajver za HID brajev standard, strelice se sada mogu koristiti za emuliranje strelica tastature i entera.
  Takođe,  `razmak+tačkica1` i `razmak+tačkica4` su sada podešene kao strelice dole i gore. (#14713)
  * Ažuriranja dinamičkog sadržaja na Webu (ARIA živi regioni) se sada prikazuju na brajevom redu.
  Ovo se može onemogućiti u panelu naprednih podešavanja. (#7756)
* Simboli crtica i em- će uvek biti poslati sintetizatoru. (#13830)
* Distanca koju Microsoft Word prijavljuje će sada poštovati mernu jedinicu koja je podešena u naprednim podešavanjima Worda čak i kada se koristi UIA za pristup Word dokumentima. (#14542)
* NVDA brže reaguje kada se pomera kursor u kontrolama za uređivanje. (#14708)
* Skripta za prijavljivanje odredišta linka sada prijavljuje sa pozicije kursora ili fokusa umesto navigacionog objekta. (#14659)
* Pravljenje prenosne kopije više ne zahteva da upišete slovo diska kao deo apsolutne putanje. (#14680)
* Ako je Windows podešen da prijavljuje sekunde na satu sistemske trake, korišćenje prečice `NVDA+f12` za prijavljivanje vremena sada prati ovo podešavanje. (#14742)
* NVDA će sada prijavljivati grupe bez oznake koje imaju korisne informacijje o poziciji, kakve se mogu pronaći u novijim  verzijama Microsoft Office 365 menija. (#14878) 

### Ispravljene greške

* Brajevi redovi:
  * Nekoliko poboljšanja u stabilnosti unosa/izlaza na brajevom redu, što će smanjiti učestalost grešaka i rušenja programa NVDA. (#14627)
  * NVDA se više neće bespotrebno prebacivati na opciju bez brajevog reda više puta u toku automatskog prepoznavanja, što donosi čistije dnevnike evidencije i manje opterećenje. (#14524)
  * NVDA će se sada vratiti na USB ako HID Bluetooth uređaj (kao što je HumanWare Brailliant ili APH Mantis) automatski bude prepoznat i USB veza postane dostupna.
  Ovo je ranije radilo samo za Bluetooth serijske portove. (#14524)
  * Kada nijedan brajev red nije povezan i preglednik brajevog reda se zatvori pritiskanjem `alt+f4` ili klikom na dugme zatvori, veličina brajevog podsistema će ponovo biti vraćena na bez ćelija. (#15214)
* Web pretraživači:
  * NVDA više neće ponekad izazivati rušenje ili prestanak rada programa Mozilla Firefox. (#14647)
  * U pretraživačima Mozilla Firefox i Google Chrome, ukucani znakovi se više ne prijavljuju u nekim poljima za unos teksta čak i kada je izgovor ukucanih znakova onemogućen. (#8442)
  * Sada možete da koristite režim pretraživanja u Chromium umetnutim kontrolama u kojima to ranije nije bilo moguće. (#13493, #8553)
  * U Mozilli Firefox, pomeranje miša do teksta nakon linka sada ispravno prijavljuje tekst. (#9235)
  * Odredište linkova na slikama se sada preciznije ispravno prijavljuje u većini slučajeva u programima Chrome i Edge. (#14779)
  * Kada pokušavate da čitate adresu linka bez href atributa NVDA više neće biti bez govora.
  Umesto togag NVDA će prijaviti da link  nema odredište. (#14723)
  * U režimu pretraživanja, NVDA neće neispravno ignorisati pomeranje fokusa na glavnu kontrolu ili kontrolu unutar nje na primer pomeranje sa kontrole na njenu unutrašnju stavku liste ili ćeliju mreže. (#14611)
   * Napomena međutim da se ova ispravka primenjuje samo kada je opcija "Automatsko postavljanje fokusa na elemente koji se mogu fokusirati" u podešavanjima režima pretraživanja isključena (što je podrazumevano podešavanje).
    -
-
* Ispravke za Windows 11:
  * NVDA ponovo može da izgovara sadržaj statusne trake u beležnici. (#14573)
  * Prebacivanje između kartica će izgovoriti ime i poziciju nove kartice u beležnici i istraživaču datoteka. (#14587, #14388)
  * NVDA će ponovo izgovarati dostupne unose kada se tekst piše na jezicima kao što su Kineski i Japanski. (#14509)
  * Ponovo je moguće otvoriti listu saradnika ili licencu iz menija NVDA pomoći. (#14725)
* Microsoft Office ispravke:
  * Kada se brzo krećete kroz ćelije u Excelu, manja je verovatnoća da će NVDA prijaviti pogrešnu ćeliju ili pogrešan izbor. (#14983, #12200, #12108)
  * Kada stanete na Excel ćeliju van radnog lista, brajev red i označavanje fokusa se više neće bespotrebno ažurirati na objekat koji je ranije bio fokusiran. (#15136)
  * NVDA sada uspešno izgovara fokusiranje na polja za lozinke u programima Microsoft Excel i Outlook. (#14839)
* Za simbole koji nemaju opis na trenutnom jeziku, podrazumevani Engleski nivo simbola će se koristiti. (#14558, #14417)
* Sada je moguće koristiti znak obrnuta kosa crta u polju zamene unosa rečnika, kada vrsta nije podešena kao regularni izraz. (#14556)
* In Windows 10 and 11 Calculator, a portable copy of NVDA will no longer do nothing or play error tones when entering expressions in standard calculator in compact overlay mode. (#14679)
* NVDA se ponovo oporavlja u brojnim slučajevima kao što su aplikacije koje više ne reaguju, što je ranije izazivalo da NVDA u potpunosti prestane da radi. (#14759) 
* Kada naterate korišćenje UIA podrške u određenim Terminalima i konzolama, ispravljena je greška koja je izazivala rušenje i neprestano pisanje podataka  u dnevniku. (#14689)
* NVDA više neće odbijati da sačuva podešavanja nakon vraćanja podešavanja na podrazumevana. (#13187)
* Kada se pokreće privremena verzija iz instalacije, NVDA neće korisnicima davati pogrešne informacije da podešavanja mogu biti sačuvana. (#14914)
* NVDA sada nešto brže reaguje na komande i promene fokusa. (#14928)
* Prikazivanje OCR podešavanja više neće biti neuspešno na nekim sistemima. (#15017)
* Ispravljena greška vezana za čuvanje i učitavanje NVDA podešavanja, uključujući menjanje sintetizatora. (#14760)
* Ispravljena greška koja je izazvala da u pregledu teksta pokret "Povlačenje gore" pomera stranice umesto da pređe na prethodni red. (#15127)

### Promene za programere (engleski)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Suggested conventions have been added to the add-on manifest specification.
These are optional for NVDA compatibility, but are encouraged or required for submitting to the Add-on Store. (#14754)
  * Use `lowerCamelCase` for the name field.
  * Use `<major>.<minor>.<patch>` format for the version field (required for add-on datastore).
  * Use `https://` as the schema for the url field (required for add-on datastore).
* Added a new extension point type called `Chain`, which can be used to iterate over iterables returned by registered handlers. (#14531)
* Added the `bdDetect.scanForDevices` extension point.
Handlers can be registered that yield `BrailleDisplayDriver/DeviceMatch` pairs that don't fit in existing categories, like USB or Bluetooth. (#14531)
* Added extension point: `synthDriverHandler.synthChanged`. (#14618)
* The NVDA Synth Settings Ring now caches available setting values the first time they're needed, rather than when loading the synthesizer. (#14704)
* You can now call the export method on a gesture map to export it to a dictionary.
This dictionary can be imported in another gesture by passing it either to the constructor of `GlobalGestureMap` or to the update method on an existing map. (#14582)
* `hwIo.base.IoBase` and its derivatives now have a new constructor parameter to take a `hwIo.ioThread.IoThread`.
If not provided, the default thread is used. (#14627)
* `hwIo.ioThread.IoThread` now has a `setWaitableTimer` method to set a waitable timer using a python function.
Similarly, the new `getCompletionRoutine` method allows you to convert a python method into a completion routine safely. (#14627)
* `offsets.OffsetsTextInfo._get_boundingRects` should now always return `List[locationHelper.rectLTWH]` as expected for a subclass of `textInfos.TextInfo`. (#12424)
* `highlight-color` is now a format field attribute. (#14610)
* NVDA should more accurately determine if a logged message is coming from NVDA core. (#14812)
* NVDA will no longer log inaccurate warnings or errors about deprecated appModules. (#14806)
* All NVDA extension points are now briefly described in a new, dedicated chapter in the Developer Guide. (#14648)
* `scons checkpot` will no longer check the `userConfig` subfolder anymore. (#14820)
* Translatable strings can now be defined with a singular and a plural form using `ngettext` and `npgettext`. (#12445)

#### Deprecations

* Passing lambda functions to `hwIo.ioThread.IoThread.queueAsApc` is deprecated.
Instead, functions should be weakly referenceable. (#14627)
* Importing `LPOVERLAPPED_COMPLETION_ROUTINE` from `hwIo.base` is deprecated.
Instead import from `hwIo.ioThread`. (#14627)
* `IoThread.autoDeleteApcReference` is deprecated.
It was introduced in NVDA 2023.1 and was never meant to be part of the public API.
Until removal, it behaves as a no-op, i.e. a context manager yielding nothing. (#14924)
* `gui.MainFrame.onAddonsManagerCommand` is deprecated, use `gui.MainFrame.onAddonStoreCommand` instead. (#13985)
* `speechDictHandler.speechDictVars.speechDictsPath` is deprecated, use `NVDAState.WritePaths.speechDictsDir` instead. (#15021)
* Importing `voiceDictsPath` and `voiceDictsBackupPath` from `speechDictHandler.dictFormatUpgrade` is deprecated.
Instead use `WritePaths.voiceDictsDir` and `WritePaths.voiceDictsBackupDir` from `NVDAState`. (#15048)
* `config.CONFIG_IN_LOCAL_APPDATA_SUBKEY` is deprecated.
Instead use `config.RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY`. (#15049)

## 2023.1

Dodata je nova opcija, "Stil pasusa" u "Navigaciji kroz dokument".
Može se koristiti sa uređivačima teksta koji ne podržavaju navigaciju po pasusima, kao što su Notepad i Notepad++.

Dodata je nova komanda za prijavljivanje odredišta linka, sa prečicom `NVDA+k`.

Poboljšana podrška za anotiran Web sadržaj (kao što su komentari i fusnote).
Pritisnite `NVDA+d` da kružite kroz kratke opise kada se prijave napomene (na primer  "Ima komentar, ima fusnotu").

Tivomatic Caiku Albatross 46/80 brajevi redovi su sada podržani.

Poboljšana podrška za ARM64 verziju Windowsa.

Ispravljene su brojne greške, posebno u Windowsu 11.

eSpeak, LibLouis, Sonic povećanje brzine i Unicode CLDR su ažurirani.
Dodate su nove Gruzijske, Swahili (Kenija) i Chichewa (Malawi) brajeve tabele.

Napomena:

* Postojeći dodaci nisu kompatibilni sa ovom verzijom.

### Nove karakteristike

* Microsoft Excel uz UI Automation: automatsko prijavljivanje zaglavlja kolona i redova u tabelama. (#14228)
  * Napomena: ovo važi za tabele koje su formatirane korišćenjem dugmeta "Tabela" u oknu trake ubacivanja .
  "Prva kolona" i "red zaglavlja" u "opcijama stila tabele" su zaglavlja kolona i redova.
  * Ovo ne utiče na zaglavlja koja su označena putem čitača ekrana kroz imenovane opsege, što trenutno nije podržano uz UI Automation.
* Dodata je nedodeljena skripta za uključivanje i isključivanje odloženih opisa znakova. (#14267)
* Dodata eksperimentalna opcija za korišćenje UIA podrške za obaveštenja u Windows Terminalu za prijavljivanje novog ili promenjenog teksta, što će doneti poboljšanu stabilnost i brzinu. (#13781)
  * Pogledajte korisničko uputstvo za ograničenja ove eksperimentalne opcije.
* Na Windowsu 11 ARM64, režim pretraživanja je sada dostupan u AMD64 aplikacijama kao što su Firefox, Google Chrome i 1Password. (#14397)
* Dodata je nova opcija, "Stil pasusa" u "navigaciji kroz dokument".
Ovo dodaje podršku za navigaciju po pasusima u pojedinačnim novim redovima (standardna) i duplim novim redovima (blokovi).
Ovo se može koristiti u uređivačima teksta koji ne podržavaju ugrađenu navigaciju po pasusima, kao što su Notepad i Notepad++. (#13797)
* Ako postoji više napomena, sada će biti prijavljene.
`NVDA+d` sada kruži kroz prijavljivanja kratkog opisa odredišta svake napomene za izvore koji imaju više odredišta napomena.
Na primer, kada tekst ima komentar i fusnotu. (#14507, #14480)
* Dodata podrška za Tivomatic Caiku Albatross 46/80 brajeve redove. (#13045)
* Nova globalna komanda: prijavi odredište linka (`NVDA+k`).
Ako se pritisne jednom, izgovara ili prikazuje na brajevom redu odredište linka u navigacionom objektu.
Ako se pritisne dva puta, biće prikazano u prozoru, za detaljniji pregled. (#14583)
* Nova nedodeljena globalna komanda (kategorija alati): prikaži odredište linka u prozoru.
Isto kao i kada se dva puta pritisne `NVDA+k`, ali može biti korisnije za korisnike brajevih redova. (#14583)

### Promene

* Ažuriran LibLouis brajev prevodilac na [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Značajna ažuriranja za Mađarske, unificirane Engleske i Kineske bopomofo brajeve kodove.
  * Podrška za Danski brajev standard 2022.
  * Nove brajeve tabele za Gruzijski književni brajev kod, Swahili (Kenija) i Chichewa (Malawi).
* Ažurirana Sonic biblioteka za povećanje brzine na commit `1d70513`. (#14180)
* CLDR je ažuriran na verziju 42.0. (#14273)
* eSpeak NG je ažuriran na 1.52-dev commit `f520fecb`. (#14281, #14675)
  * Ispravljeno prijavljivanje velikih brojeva. (#14241)
* Java aplikacije sa kontrolama koje se mogu izabrati će sada izgovoriti kada stavka nije izabrana, umesto kada je izabrana. (#14336)

### Ispravljene greške

* Windows 11 ispravke:
  * NVDA će izgovoriti istaknute pretrage kada se otvori start meni. (#13841)
  * na ARM verziji, x64 aplikacije se više ne označavaju kao ARM64 aplikacije. (#14403)
  * Sada možete pristupiti opcijama menija istorije privremene memorije kao što su "Zakači stavku". (#14508)
  * Na Windowsu 11 22H2 i novijim, ponovo je moguće koristiti miš i ekran osetljiv na dodir za interakciju sa delovima kao što su prozor sistemske trake i dijalog "Otvori". (#14538, #14539)
-
* Predlozi se sada prijavljuju kada upišete @spominjanje u Microsoft Excel komentarima. (#13764)
* U Google Chrome adresnoj traci, kontrole predloga (prebaci se na karticu, ukloni predlog i tako dalje) se sada prijavljuju kada se izaberu. (#13522)
* Kada zahtevate informacije o formatiranju, boje se sada prijavljuju u Wordpadu ili pregledniku dnevnika, umesto da samo čujete "Podrazumevana boja". (#13959)
* U Firefoxu, aktiviranje dugmeta "Show options" na GitHub issues stranici sada ispravno radi. (#14269)
* Kontrole birača datuma u dijalogu napredne pretrage  programa Outlook 2016 / 365 sada prijavljuju svoju oznaku i vrednost. (#12726)
* ARIA kontrole prekidača se sada prijavljuju kao prekidači u pretraživačima Firefox, Chrome i Edge, umesto kao izborna polja. (#11310)
* NVDA će automatski izgovoriti stanje sortiranja u zaglavlju kolone HTML tabele  kada se promeni pritiskanjem unutrašnjeg tastera. (#10890)
* Ime orjentira ili regiona će uvek automatski biti izgovoreno kada skočite do njega a pre toga ste bili van njega korišćenjem brze navigacije ili fokusiranja u režimu pretraživanja. (#13307)
* Kada je omogućeno pištanje ili izgovor velikih slova uz odložene opise znakova, NVDA više neće reprodukovati pištanja ili izgovarati reč veliko dva puta. (#14239)
* NVDA će sada preciznije izgovarati Kontrole tabela u Java aplikacijama. (#14347)
* Neka podešavanja se više neće neočekivano razlikovati kada se koriste uz različite profile. (#14170)
  * Sledeća podešavanja su ispravljena:
    * Uvlačenje redova u podešavanjima formatiranja dokumenta.
    * Granice ćelija u podešavanjima formatiranja dokumenta
    * Prikazivanje poruka u brajevim podešavanjima
    * Vezivanje brajevog reda u brajevim podešavanjima
  * U nekim retkim slučajevima, ova podešavanja koja se koriste u profilima će možda biti neočekivano promenjena kada se instalira ova NVDA verzija.
  * Molimo proverite ova podešavanja u vašim profilima nakon što ažurirate NVDA na ovu verziju.
* Emoji znakovi će sada biti prijavljeni na više jezika. (#14433)
* Postojanje napomena više neće nedostajati na brajevom redu za neke elemente. (#13815)
* Ispravljen problem koji je izazvao da se promene podešavanja ne čuvaju ispravno kada se menja između opcije koja je podrazumevana i vrednosti podrazumevane opcije. (#14133)
* Kada se podešava NVDA, bar jedan taster će uvek biti podešen kao NVDA taster. (#14527)
* Kada pristupate NVDA meniju iz sistemske trake, NVDA više neće nuditi odloženo ažuriranje kada nema odloženog ažuriranja. (#14523)
* Preostalo, proteklo i ukupno vreme se sada ispravno prijavljuje za zvučne zapise koje su duže od jednog dana u foobaru2000. (#14127)
* U Web pretraživačima kao što su Chrome i Firefox, upozorenja kao što su preuzimanja datoteke se prikazuju na brajevom redu uz izgovor. (#14562)
* Ispravljena greška kada se pomerate na prvu ili poslednju kolonu tabele u Firefoxu (#14554)
* Kada se NVDA pokrene sa parametrom `--lang=Windows`, ponovo je moguće otvoriti NVDA dijalog opštih podešavanja. (#14407)
* NVDA će sada ponovo nastaviti čitanje u programu Kindle za računare nakon što se promeni stranica. (#14390)

### Promene za programere (engleski)

Note: this is an Add-on API compatibility breaking release.
Add-ons will need to be re-tested and have their manifest updated.
Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* System tests should now pass when run locally on non-English systems. (#13362)
* In Windows 11 on ARM, x64 apps are no longer identified as ARM64 applications. (#14403)
* It is no longer necessary to use `SearchField` and `SuggestionListItem` `UIA` `NVDAObjects` in new UI Automation scenarios, where automatic reporting of search suggestions, and where typing has been exposed via UI Automation with the `controllerFor` pattern.
This functionality is now available generically via `behaviours.EditableText` and the base `NVDAObject` respectively. (#14222)
* The UIA debug logging category when enabled now produces significantly more logging for UIA event handlers and utilities. (#14256)
* NVDAHelper build standards updated. (#13072)
  * Now uses the C++20 standard, was C++17.
  * Now uses the `/permissive-` compiler flag which disables permissive behaviors, and sets the `/Zc` compiler options for strict conformance.
* Some plugin objects (e.g. drivers and add-ons) now have a more informative description in the NVDA python console. (#14463)
* NVDA can now be fully compiled with Visual Studio 2022, no longer requiring the Visual Studio 2019 build tools. (#14326)
* More detailed logging for NVDA freezes to aid debugging. (#14309)
* The singleton `braille._BgThread` class has been replaced with `hwIo.ioThread.IoThread`. (#14130)
  * A single instance `hwIo.bgThread` (in NVDA core) of this class provides background i/o for thread safe braille display drivers.
  * This new class is not a singleton by design, add-on authors are encouraged to use their own instance when doing hardware i/o.
* The processor architecture for the computer can be queried from `winVersion.WinVersion.processorArchitecture attribute.` (#14439)
* New extension points have been added. (#14503)
  * `inputCore.decide_executeGesture`
  * `tones.decide_beep`
  * `nvwave.decide_playWaveFile`
  * `braille.pre_writeCells`
  * `braille.filter_displaySize`
  * `braille.decide_enabled`
  * `braille.displayChanged`
  * `braille.displaySizeChanged`
* It is possible to set useConfig to False on supported settings for a synthesizer driver. (#14601)

#### API Breaking Changes

These are breaking API changes.
Please open a GitHub issue if your Add-on has an issue with updating to the new API.

* The configuration specification has been altered, keys have been removed or modified:
  * In `[documentFormatting]` section (#14233):
    * `reportLineIndentation` stores an int value (0 to 3) instead of a boolean
    * `reportLineIndentationWithTones` has been removed.
    * `reportBorderStyle` and `reportBorderColor` have been removed and are replaced by `reportCellBorders`.
  * In `[braille]` section (#14233):
    * `noMessageTimeout` has been removed, replaced by a value for `showMessages`.
    * `messageTimeout` cannot take the value 0 anymore, replaced by a value for `showMessages`.
    * `autoTether` has been removed; `tetherTo` can now take the value "auto" instead.
  * In `[keyboard]` section  (#14528):
    * `useCapsLockAsNVDAModifierKey`, `useNumpadInsertAsNVDAModifierKey`, `useExtendedInsertAsNVDAModifierKey` have been removed.
    They are replaced by `NVDAModifierKeys`.
* The `NVDAHelper.RemoteLoader64` class has been removed with no replacement. (#14449)
* The following functions in `winAPI.sessionTracking` are removed with no replacement. (#14416, #14490)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`
* It is no longer possible to enable/disable the braille handler by setting `braille.handler.enabled`.
To disable the braille handler programatically, register a handler to `braille.handler.decide_enabled`. (#14503)
* It is no longer possible to update the display size of the handler by setting `braille.handler.displaySize`.
To update the displaySize programatically, register a handler to `braille.handler.filter_displaySize`.
Refer to `brailleViewer` for an example on how to do this. (#14503)
* There have been changes to the usage of `addonHandler.Addon.loadModule`. (#14481)
  * `loadModule` now expects dot as a separator, rather than backslash.
  For example "lib.example" instead of "lib\example".
  * `loadModule` now raises an exception when a module can't be loaded or has errors, instead of silently returning `None` without giving information about the cause.
* The following symbols have been removed from `appModules.foobar2000` with no direct replacement. (#14570)
  * `statusBarTimes`
  * `parseIntervalToTimestamp`
  * `getOutputFormat`
  * `getParsingFormat`
* The following are no longer singletons - their get method has been removed.
Usage of `Example.get()` is now `Example()`. (#14248)
  * `UIAHandler.customAnnotations.CustomAnnotationTypesCommon`
  * `UIAHandler.customProps.CustomPropertiesCommon`
  * `NVDAObjects.UIA.excel.ExcelCustomProperties`
  * `NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes`

#### Deprecations

* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA` is deprecated and usage is discouraged. (#14047)
* `config.addConfigDirsToPythonPackagePath` has been moved.
Use `addonHandler.packaging.addDirsToPythonPackagePath` instead. (#14350)
* `braille.BrailleHandler.TETHER_*` are deprecated.
Use `configFlags.TetherTo.*.value` instead. (#14233)
* `utils.security.postSessionLockStateChanged` is deprecated.
Use `utils.security.post_sessionLockStateChanged` instead. (#14486)
* `NVDAObject.hasDetails`, `NVDAObject.detailsSummary`, `NVDAObject.detailsRole` has been deprecated.
Use `NVDAObject.annotations` instead. (#14507)
* `keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS` is deprecated with no direct replacement.
Consider using the class `config.configFlags.NVDAKey` instead. (#14528)
* `gui.MainFrame.evaluateUpdatePendingUpdateMenuItemCommand` has been deprecated.
Use `gui.MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand` instead. (#14523)

## 2022.4

Ova verzija uključuje nekoliko novih ključnih komandi, uključujući komande za režim izgovori sve u tabelama.
Sekcija "vodič za brz početak" je dodata u korisničko uputstvo.
Ispravljeno je takođe nekoliko grešaka.

eSpeak i LibLouis su ažurirani.
Dodate su nove Kineske, Švedske, Luganda i Kinyarwanda brajeve tabele.

### Nove karakteristike

* Dodata sekcija "vodič za brz početak" u korisničko uputstvo. (#13934)
* Dodata nova komanda za proveru tasterske prečice trenutnog fokusa. (#13960)
  * Desktop: `šift+numeričko2`.
  * Laptop: `NVDA+ctrl+šift+.`.
* Dodate nove komande za pomeranje preglednog kursora po stranicama kada je podržano od aplikacije. (#14021)
  * Pomeri se na prethodnu stranicu:
    * Desktop: `NVDA+pageUp`.
    * Laptop: `NVDA+šift+pageUp`.
  * Pomeri se na sledeću stranicu:
    * Desktop: `NVDA+pageDown`.
    * Laptop: `NVDA+šift+pageDown`.
* Dodate sledeće komande za tabele. (#14070)
  * Izgovori sve u koloni: `NVDA+kontrol+alt+strelicaDole`
  * Izgovori sve u redu: `NVDA+kontrol+alt+strelicaDesno`
  * Pročitaj celu kolonu: `NVDA+kontrol+alt+strelicaGore`
  * Pročitaj ceo red: `NVDA+kontrol+alt+strelicaLevo`
* Microsoft Excel uz UI Automation: NVDA sada izgovara kada izađete iz tabele u okviru radnog lista. (#14165)
* Prijavljivanje zaglavlja u tabeli se sada može podesiti odvojeno za redove i kolone. (#14075)

### Promene

* eSpeak NG je ažuriran na 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Ispravljeno prijavljivanje latiničnih znakova kada se koristi Mandarinski. (#12952, #13572, #14197)
* Ažuriran LibLouis brajev prevodilac na [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Dodate brajeve tabele:
    * Kineski zajednički brajev kod (znakovi pojednostavljenog Kineskog)
    * Kinyarwanda književni brajev kod
    * Luganda književni brajev kod
    * Švedski brajev kod
    * Švedski polovičan kratkopis
    * Švedski kratkopis
    * Kineski (Kina, Mandarinski) trenutni brajev sistem (bez tonova) (#14138)
* NVDA sada uključuje arhitekturu operativnog sistema kao deo praćenja statistika korišćenja. (#14019)

### Ispravljene greške

* Kada se NVDA ažurira korišćenjem interfejsa komandne linije Windows menadžera paketa (winget), stabilna NVDA verzija neće uvek biti tretirana kao novija od bilo koje alfa verzije koja je instalirana. (#12469)
* NVDA će sada ispravno izgovarati grupisana polja u Java aplikacijama. (#13962)
* Kursor ispravno prati izgovoreni tekst kada se koristi režim "izgovori sve" u aplikacijama kao što su Bookworm, WordPad, ili u NVDA pregledniku dnevnika. (#13420, #9179)
* U programima koji koriste UI Automation, izborna polja koja su polovično označena biće ispravno prijavljena. (#13975)
* Poboljšane performanse i stabilnost u  Microsoft Visual Studiju, Windows Terminalu, i drugim  aplikacijama zasnovanim na UI Automation. (#11077, #11209)
  * Ove ispravke se primenjuju na Windowsu 11 Sun Valley 2 (verzija 22H2) i novijim.
  * Selektivna registracija za promene UI Automation  događaja i svojstava je sada podrazumevano omogućena.
* Prijavljivanje teksta, brajev izlaz i sprečavanje izgovora lozinki sada rade kako je očekivano u umetnutoj kontroli Windows terminala u Visual Studiju 2022. (#14194)
* NVDA sada obraća pažnju na DPI podešavanje kada se koristi na više monitora.
Ispravljeno je nekoliko grešaka kada se koristi DPI podešavanje veće od 100% ili kada se koristi više monitora.
Problemi još uvek mogu postojati kada se koriste Windows verzije starije od Windowsa 10 1809.
Kako bi ove ispravke radile, aplikacije sa kojima NVDA vrši interakciju takođe moraju da obraćaju pažnju na DPI.
Napomena da još uvek postoje poznati problemi sa Chromeom i Edgeom. (#13254)
  * Vizuelni okviri za označavanje bi  trebali da se postavljaju ispravno u većini aplikacija. (#13370, #3875, #12070)
  * Interakcija sa ekranom osetljivim na dodir bi trebala da bude precizna u većini aplikacija. (#7083)
  * Praćenje miša bi trebalo da radi u većini aplikacija. (#6722)
* Promene orijentacije (horizontalno/uspravno) se sada ispravno ignorišu kada nema promene (na primer prilikom promene monitora). (#14035)
* NVDA će izgovarati prevlačenje stavki na ekranu na mestima kao što su premeštanje pločica start menija Windowsa 10 i virtuelnih radnih površina u Windowsu 11. (#12271, #14081)
* U naprednim podešavanjima, podešavanje "Reprodukuj zvuk za evidentirane greške" se sada ispravno vraća na svoju podrazumevanu vrednost kada pritisnete dugme "Vrati na podrazumevana". (#14149)
* NVDA sada može da izabere tekst korišćenjem prečice `NVDA+f10` u Java aplikacijama. (#14163)
* NVDA se više neće zaglavljivati u meniju kada se strelicama gore i dole krećete po  konverzacijama u nizu u Microsoft Teamsu. (#14355)

### Promene za programere (engleski)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* The [NVDA API Announcement mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) was created. (#13999)
* NVDA no longer processes `textChange` events for most UI Automation applications due to their extreme negative performance impact. (#11002, #14067)

#### Deprecations

* `core.post_windowMessageReceipt` is deprecated, use `winAPI.messageWindow.pre_handleWindowMessage` instead.
* `winKernel.SYSTEM_POWER_STATUS` is deprecated and usage is discouraged, this has been moved to `winAPI._powerTracking.SystemPowerStatus`.
* `winUser.SM_*` constants are deprecated, use `winAPI.winUser.constants.SystemMetrics` instead.

## 2022.3.3

Ovo je manje ažuriranje kako bi se ispravili problemi u verzijama 2022.3.2, 2022.3.1 i 2022.3.
Takođe ispravlja bezbednosni problem.

### Bezbednosne ispravke

* Sprečava mogućnost sistemskog pristupa (na primer NVDA Python konzolu) za neprijavljene korisnike.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Ispravljene greške

* Ispravljena greška u kojoj ako se NVDA zamrzne prilikom zaključavanja, NVDA dozvoljava pristup korisničkoj radnoj površini sa zaključanog ekrana. (#14416)
* Ispravljena greška u kojoj ako se NVDA zamrzne prilikom zaključavanja, NVDA se ne ponaša ispravno, kao da je uređaj još uvek zaključan. (#14416)
* Ispravljeni problemi u pristupačnosti Windows ekrana zaboravljenog PIN-a kao i u korišćenju instalacije Windows ažuriranja. (#14368)
* Ispravljena greška sa NVDA instalacijom na određenim Windows okruženjima, na primer Windows Server. (#14379)

### Promene za programere (engleski)

#### Deprecations

* `utils.security.isObjectAboveLockScreen(obj)` is deprecated, instead use `obj.isBelowLockScreen`. (#14416)
* The following functions in `winAPI.sessionTracking` are deprecated for removal in 2023.1. (#14416)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`

## 2022.3.2

Ovo je manje ažuriranje kako bi se ispravila pogoršanja koja je izazvala verzija 2022.3.1 i kako bi se ispravio bezbednosni problem.

### Bezbednosne ispravke

* Sprečava mogućnost pristupa na sistemskom nivou za korisnike koji nemaju autentikaciju.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Ispravljene greške

* Ispravljeno pogoršanje iz verzije 2022.3.1 koje je izazvalo onemogućavanje određenih funkcija na bezbednim ekranima. (#14286)
* Ispravljeno pogoršanje iz verzije 2022.3.1 koje je izazvalo onemogućavanje određenih funkcija nakon prijave, ako je NVDA pokrenut na zaključanom ekranu. (#14301)

## 2022.3.1

Ovo je manje ažuriranje kako bi se ispravilo nekoliko bezbednosnih problema.
Molimo odgovorno prijavite bezbednosne probleme na <info@nvaccess.org>.

### Bezbednosne ispravke

* Ispravljen propust koji je dozvoljavao da dobijete sistemske privilegije umesto korisničkih.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Ispravljen bezbednosni problem koji je dozvoljavao pristup Python konzoli na zaključanom ekranu uz posebni uslov pri NVDA pokretanju.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Ispravljen problem koji je izazvao keširanje teksta preglednika govora kada se zaključa Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Ispravljene greške

* Sprečavanje korisnika bez autentikacije da ažurira podešavanja za preglednike govora i brajevih redova na zaključanom ekranu. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Ogroman deo ove verzije je doprinela zajednica NVDA programera.
Ovo uključuje odložene opise znakova i poboljšanu podršku za Windows konzolu.

Ova verzija takođe uključuje nekoliko ispravljenih grešaka.
Od važnijih, najnovije verzije programa Adobe Acrobat/Reader se više neće rušiti pri čitanju PDF dokumenata.

eSpeak je ažuriran, i sada uključuje 3 nova jezika: Beloruski, Luksemburški i Totontepec Mixe.

### Nove karakteristike

* U Windows Console Hostu kojeg koriste komandna linija, PowerShell, i Windows podsistem za Linux na Windowsu 11 verzija 22H2 (Sun Valley 2) i novije:
  * Značajno poboljšana brzina i stabilnost. (#10964)
  * Kada se pritisne `kontrol+f` da pretražite tekst, pozicija preglednog kursora će biti ažurirana kako bi pratila pronađeni termin. (#11172)
  * Prijavljivanje upisanog teksta koji se ne pojavljuje na ekranu (kao što su lozinke) je podrazumevano onemogućeno.
Može se ponovo omogućiti u NVDA panelu naprednih podešavanja. (#11554)
  * Tekst koji je van ekrana se može pregledati bez potrebe za pomeranjem prozora konzole. (#12669)
  * Dostupne su detaljnije informacije o formatiranju teksta. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Dodata je nova opcija u podešavanjima govora za čitanje opisa znakova uz odlaganje. (#13509)
* Dodata je nova opcija za brajeve redove koja određuje da li će pomeranje brajevog reda napred i nazad prekinuti govor. (#2124)

### Promene

* eSpeak NG je ažuriran na 1.52-dev commit `9de65fcb`. (#13295)
  * Dodati jezici:
    * Beloruski
    * Luksemburški
    * Totontepec Mixe
* Kada se koristi UI Automation za pristup kontrolama u programu Microsoft Excel, NVDA sada može da prijavi kada je ćelija spojena. (#12843)
* Umesto prijavljivanja "ima detalje" biće prijavljena svrha detalja kada je moguće, na primer "ima komentar". (#13649)
* Veličina instalacije programa NVDA se sada prikazuje u Windows programima i funkcijama. (#13909)

### Ispravljene greške

* Adobe Acrobat / Reader 64 bitni se više neće rušiti pri čitanju PDF dokumenata. (#12920)
  * Napomena da je najnovija verzija programa Adobe Acrobat / Reader takođe neophodna kako bi se izbeglo rušenje.
* Java access bridge događaji će biti ignorisani kada se ne može pronaći window handle u Java aplikacijama.
Ovo će poboljšati brzinu u nekim Java aplikacijama kao što je IntelliJ IDEA. (#13039)
* Izgovor izabranih ćelija u programu LibreOffice Calc je efikasniji i više neće smrzavati Calc kada je puno ćelija izabrano. (#13232)
* Kada je pokrenut od strane drugog korisnika, Microsoft Edge više nije nepristupačan. (#13032)
* Kada je povećanje brzine isključeno, brzina sintetizatora ESpeak više ne pada između brzina 99% i 100%. (#13876)
* Ispravljena greška koja je dozvoljavala otvaranje dva dijaloga ulaznih komandi. (#13854)

### Promene za programere (engleski)

* Updated Comtypes to version 1.1.11. (#12953)
* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * This can be overridden by changing the "Windows Console support" setting in NVDA's advanced settings panel.
  * To find your Windows Console's NVDA API level, set "Windows Console support" to "UIA when available", then check the NVDA+F1 log opened from a running Windows Console instance.
* The Chromium virtual buffer is now loaded even when the document object has the MSAA `STATE_SYSTEM_BUSY` exposed via IA2. (#13306)
* A config spec type `featureFlag` has been created for use with experimental features in NVDA. See `devDocs/featureFlag.md` for more information. (#13859)

#### Deprecations

There are no deprecations proposed in 2022.3.

## 2022.2.4

Ovo je manje ažuriranje kako bi se ispravio bezbednosni problem.

### Ispravljene greške

* Ispravljen propust koji je dozvoljavao da otvorite NVDA python konzolu putem preglednika dnevnika na zaključanom ekranu.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Ovo je manje ažuriranje kako bi se ispravio API problem u verziji 2022.2.1.

### Ispravljene greške

* Ispravljena greška koja je izazvala da NVDA ne izgovori "Bezbedna radna površina" kada uđe na bezbednu radnu površinu.
Ovo je izazvalo da NVDA Remote ne prepoznaje bezbedne radne površine. (#14094)

## 2022.2.2

Ova verzija ispravlja grešku iz verzije 2022.2.1 sa ulaznim komandama.

### Ispravljene greške

* Ispravljena greška koja je izazvala da ulazne komande ne rade uvek. (#14065)

## 2022.2.1

Ovo je manje ažuriranje kako bi se ispravio bezbednosni problem.
Molimo odgovorno prijavite bezbednosne probleme na <info@nvaccess.org>.

### Bezbednosne ispravke

* Ispravljen propust koji je dozvoljavao pokretanje Python konzole sa zaključanog ekrana. (GHSA-rmq3-vvhq-gp32)
* Ispravljen propust koji je dozvoljavao da napustite zaključani ekran objektnom navigacijom. (GHSA-rmq3-vvhq-gp32)

### Promene za programere (engleski)

#### Deprecations

These deprecations are currently not scheduled for removal.
The deprecated aliases will remain until further notice.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModules.lockapp.LockAppObject` should be replaced with `NVDAObjects.lockscreen.LockScreenObject`. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS` should be replaced with `utils.security.getSafeScripts()`. (GHSA-rmq3-vvhq-gp32)

## 2022.2

Mnoge greške su ispravljene u ovoj verziji.
Od važnijih, dodata su brojna poboljšanja u Java aplikacijama, za brajeve redove i Windows opcije.

Dodate su nove komande za navigaciju kroz tabele.
Unicode CLDR je ažuriran.
LibLouis je ažuriran, što uključuje novu Nemačku brajevu tabelu.

### Nove karakteristike

* Podrška za interakciju sa Microsoft Loop komponentama u Microsoft Office proizvodima. (#13617)
* Dodate su nove komande za navigaciju kroz tabele. (#957)
 * `kontrol+alt+home/end` da biste se prebacili na prvu/poslednju kolonu.
 * `kontrol+alt+pageUp/pageDown` da biste se prebacili na prvi/poslednji red.
* Dodata je skripta bez podrazumevane komande za prebacivanje između različitih nivoa automatskog menanja jezika i dijalekta. (#10253)

### Promene

* NSIS je ažuriran na verziju 3.08. (#9134)
* CLDR je ažuriran na verziju 41.0. (#13582)
* Ažuriran LibLouis brajev prevodilac na [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nova brajeva tabela: Nemački stepen 2 (detailed)
* Dodato novo ime za kontrole "Zauzet pokazivač". (#10644)
* NVDA sada izgovara kada neka NVDA radnja ne može biti izvršena. (#13500)
  * Ovo uključuje sledeće:
    * Korišćenje NVDA verzije iz Windows prodavnice.
    * Na bezbednim ekranima.
    * Kada dijalog čeka odgovor.

### Ispravljene greške

* Ispravljene greške u Java aplikacijama:
  * NVDA će sada izgovoriti ako je kontrola samo za čitanje. (#13692)
  * NVDA će sada ispravno izgovoriti ako je kontrola onemogućena/omogućena. (#10993)
  * NVDA će sada izgovoriti prečice funkcijskih tastera. (#13643)
  * NVDA sada može da pišti i izgovara trake napredovanja. (#13594)
  * NVDA više neće neispravno uklanjati tekst iz vidžeta kada se oni prikazuju korisnicima. (#13102)
    * NVDA će sada izgovoriti stanje za dugme prekidača. (#9728)
  * NVDA će sada prepoznati prozor u Java aplikaciji sa više prozora. (#9184)
  * NVDA će sada izgovoriti informacije o poziciji za kontrole kartica. (#13744)
-
* Ispravljene greške za brajeve redove:
  * Ispravljen brajev izlaz kada se krećete kroz određene tekstove u Mozilla obogaćenim kontrolama za pisanje, kao što su čuvanje poruke kao nacrt u programu Thunderbird. (#12542)
  * Kada je vezivanje brajevog reda podešeno na automatski i miš se pomera uz omogućeno praćenje miša,
  komande pregleda teksta sada ažuriraju brajev red sa izgovorenim sadržajem. (#11519)
  * Sada je moguće pomerati brajev red kroz sadržaja nakon korišćenja komandi za pregled teksta. (#8682)
* NVDA instalacija se sada može pokrenuti iz foldera koji imaju posebne znakove. (#13270)
* U pretraživaču Firefox, NVDA više ne greši u čitanju stavki na Web stranicama kada su aria-rowindex, aria-colindex, aria-rowcount ili aria-colcount atributi neispravni. (#13405)
* Kursor više ne menja red ili kolonu kada se koriste komande za navigaciju kroz tabele kako biste se kretali kroz spojene ćelije. (#7278)
* Kada se čitaju PDF datoteke sa kojima nije moguća interakcija u programu Adobe Reader, vrsta i stanje polja za unos (kao što su izborna polja i radio dugmad) sada se prijavljuju. (#13285)
* Sada je moguće pristupiti opciji "Vrati podešavanja na fabričke vrednosti" u bezbednom načinu rada. (#13547)
* Bilo koji zaključani tasteri miša će biti otključani kada se izađe iz programa NVDA, ranije je taster na mišu ostao zaključan. (#13410)
* Visual Studio sada prijavljuje brojeve redova. (#13604)
  * Napomena da kako bi prijavljivanje broja redova radilo, prikazivanje brojeva redova mora biti omogućeno u programu Visual Studio kao i u programu  NVDA.
* Visual Studio sada ispravno prijavljuje uvlačenje redova. (#13574)
* NVDA će ponovo izgovarati detalje rezultata pretrage u start meniju na novijim Windows 10 i 11 verzijama. (#13544)
* U Windows 10 i 11 Kalkulatoru verziji 10.1908 i novijim,
NVDA će izgovarati rezultate kada se koristi više komandi, kao što su komande iz naučnog režima. (#13383)
* Na Windowsu 11, ponovo je moguće kretati se i vršiti interakciju sa elementima korisničkog interfejsa,
kao što su programska traka ili prikaz zadataka korišćenjem miša ili ekrana osetljivog na dodir. (#13506)
* NVDA će izgovarati sadržaj statusne trake u Windows 11 verziji programa Notepad. (#13688)
* Označavanje navigacionog objekta se sada prikazuje odmah nakon aktiviranja ove opcije. (#13641)
* Ispravljeno čitanje stavki liste koje imaju samo jednu kolonu. (#13659, #13735)
* Ispravljena eSpeak automatska promena jezika za Engleski i Francuski vraćanjem na Britanski Engleski i Francuski (Francuska). (#13727)
* Ispravljena OneCore automatska promena jezika pri pokušaju promene na jezik koji je ranije bio instaliran. (#13732)

### Promene za programere (engleski)

* Compiling NVDA dependencies with Visual Studio 2022 (17.0) is now supported.
For development and release builds, Visual Studio 2019 is still used. (#13033)
* When retrieving the count of selected children via accSelection,
the case where a negative child ID or an IDispatch is returned by `IAccessible::get_accSelection` is now handled properly. (#13277)
* New convenience functions `registerExecutableWithAppModule` and `unregisterExecutable` were added to the `appModuleHandler` module.
They can be used to use a single App Module with multiple executables. (#13366)

#### Deprecations

These are proposed API breaking changes.
The deprecated part of the API will continue to be available until the specified release.
If no release is specified, the plan for removal has not been determined.
Note, the roadmap for removals is 'best effort' and may be subject to change.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModuleHandler.NVDAProcessID` is deprecated, use `globalVars.appPid` instead. (#13646)
* `gui.quit` is deprecated, use `wx.CallAfter(mainFrame.onExitCommand, None)` instead. (#13498)
  -
* Some alias appModules are marked as deprecated.
Code which imports from one of them, should instead import from the replacement module.  (#13366)

| Removed module name |Replacement module|
|---|---|
|azuredatastudio |code|
|azuredatastudio-insiders |code|
|calculatorapp |calculator|
|code - insiders |code|
|commsapps |hxmail|
|dbeaver |eclipse|
|digitaleditionspreview |digitaleditions|
|esybraille |esysuite|
|hxoutlook |hxmail|
|miranda64 |miranda32|
|mpc-hc |mplayerc|
|mpc-hc64 |mplayerc|
|notepad++ |notepadPlusPlus|
|searchapp |searchui|
|searchhost |searchui|
|springtoolsuite4 |eclipse|
|sts |eclipse|
|teamtalk3 |teamtalk4classic|
|textinputhost |windowsinternal_composableshell_experiences_textinput_inputapp|
|totalcmd64 |totalcmd|
|win32calc |calc|
|winmail |msimn|
|zend-eclipse-php |eclipse|
|zendstudio |eclipse|

## 2022.1

Ova verzija uključuje veća poboljšanja za UIA podršku u paketu MS Office.
Za Microsoft Office 16.0.15000 i novije verzije na Windowsu 11, NVDA će podrazumevano koristiti UI Automation za pristup dokumentima programa Microsoft Word.
Ovo pruža značajno poboljšanje brzine u odnosu na stariji način pristupa.

Postoje poboljšanja za drajvere za brajeve redove kao što su Seika beležnica, Papenmeier i  HID brajev standard. 
Takođe su uključene razne ispravke grešaka za Windows 11, u aplikacijama kao što su Kalkulator, konzola, Terminal, Mail i Emoji panel.

Ažurirani su eSpeak-NG  i LibLouis, dodajući nove Japanske, Nemačke i Katalonske tabele.

Napomena:

 * Ova verzija čini postojeće dodatke nekompatibilnim.

### nove karakteristike

* Podrška za prijavljivanje napomena u programu MS Excel uz  UI Automation omogućen na Windowsu 11. (#12861)
* U novijim verzijama programa Microsoft Word uz  UI Automation na  Windowsu 11, postojanje markera, nacrta komentara kao i rešenih komentara se sada prijavljuje izgovorom kao i na brajevom redu. (#12861)
* Novi parametar komandne linije `--lang` dozvoljava menjanje podešenog NVDA jezika. (#10044)
* NVDA će sada upozoriti o parametrima komandne linije koji su nepoznati i ne koriste se od strane dodataka. (#12795)
* Kada se pristupa programu Microsoft Word uz UI Automation, NVDA će sada koristiti mathPlayer za navigaciju i čitanje Office matematičkih zadataka. (#12946)
  * Kako bi ovo  radilo, morate koristiti Microsoft Word 365/2016 verziju 14326 ili novije. 
    * MathType zadaci se takođe moraju ručno pretvoriti u Office Math izborom svakog od njih, otvaranjem kontekstnog menija, izborom stavke opcije jednačina, pretvori u  Office Math.
-
* Prijavljivanje kada objekat  "ima detalje " kao i odgovarajuća komanda za prijavljivanje odnosa detalja sada mogu da se koriste u režimu fokusiranja. (#13106)
* Seika beležnica se sada može automatski prepoznati putem USB i Bluetooth veze. (#13191, #13142)
  * Ovo utiče na sledeće uređaje: MiniSeika (16, 24 ćelija), V6, i V6Pro (40 ćelija)
  * Ručno biranje bluetooth COM porta je sada takođe podržano.
* Dodata komanda za uključivanje i isključivanje preglednika brajevog reda; nema podrazumevane pridružene prečice. (#13258)
* Dodate komande za uključivanje ili isključivanje više modifikatorskih tastera u isto vreme  na brajevom redu (#13152)
* Dijalog za govorne rečnike sada sadrži dugme "Ukloni sve" koje vam pomože da očistite ceo rečnik. (#11802)
* Dodata podrška za Windows 11 kalkulator. (#13212)
* U programu Microsoft Word uz UI Automation omogućen na Windowsu 11, brojevi redova i sekcija se sada mogu prijaviti. (#13283, #13515)
* Za  Microsoft Office 16.0.15000 i novije na Windowsu 11, NVDA će podrazumevano koristiti UI Automation za pristup Microsoft Word dokumentima, što pruža značajna poboljšanja u brzini u odnosu na stariji način pristupa. (#13437)
 * Ovo uključuje dokumente u samom programu Microsoft Word, kao i čitanje i pisanje poruka u programu Microsoft Outlook. 

### Promene

* Espeak-ng je ažuriran na 1.51-dev commit `7e5457f91e10`. (#12950)
* Ažuriran liblouis brajev prevodilac na [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Dodata nova brajeva tabela: Japanski (Kantenji) književni brajev kod.
  * Dodata nova Nemačka šestotačkasta kompjuterska brajeva tabela.
  * Dodata brajeva tabela Katalonski stepen 1. (#13408)
* NVDA će prijaviti izbor i spajanje ćelija u programu LibreOffice Calc 7.3 i novijim. (#9310, #6897)
* Ažuriran Unicode Common Locale Data Repository (CLDR) na 40.0. (#12999)
* ``NVDA+numerički taster za brisanje `` podrazumevano prijavljuje lokaciju kursora ili fokusiranog objekta. (#13060)
* `NVDA+šift+numerički taster za brisanje` prijavljuje lokaciju preglednog kursora. (#13060)
* Dodate podrazumevane prečice za uključivanje i isključivanje modifikatorskih tastera na Freedom Scientific brajevim redovima (#13152)
* "Osnovna linija " se više neće izgovarati kada se koristi komanda za prijavljivanje formatiranja  (`NVDA+f`). (#11815)
* Prijavljivanje dugog opisa više nema podešenu podrazumevanu komandu. (#13380)
* Prijavljivanje kratkog opisa detalja sada ima podrazumevanu prečicu (`NVDA+d`). (#13380)
* NVDA mora ponovo biti pokrenut nakon što se instalira MathPlayer. (#13486)

### Ispravljene greške

* Okno upravljača privremene memorije više neće neispravno biti fokusirano kada se otvaraju određeni Office programi. (#12736)
* Na sistemima na kojima je korisnik odredio da zameni primarno dugme na mišu tako da desni klik aktivira stavke, NVDA više neće otvarati kontekstni meni umesto da aktivira stavku, u aplikacijama kao što su Web pretraživači. (#12642)
* Kada se pregledni kursor pomera od dna tekstualnih kontrola, kao što su u programu Microsoft Word uz UI Automation, "dno" se ispravno izgovara u više situacija. (#12808)
* NVDA može da pruži ime aplikacije i verziju za binarne datoteke koje se nalaze u system32 kada je pokrenut na 64-bitnoj verziji Windowsa. (#12943)
* Poboljšana doslednost u čitanju u terminal programima. (#12974)
  * Napomena da će se u određenim situacijama, kada ubacujete ili brišete znakove u sredini reda, znakovi nakon kursora  možda ponovo pročitati.
* MS word uz UIA: Brza navigacija kroz naslove se neće više zaglavljivati na poslednjem naslovu, niti će taj naslov biti prikazan dva puta u listi elemenata. (#9540)
* Na Windowsu 8 i novijim, statusna traka istraživača datoteka se sada može pročitati korišćenjem standardnih prečica NVDA+end (desktop) / NVDA+šift+end (laptop). (#12845)
* Dolazne poruke u ćaskanjima aplikacije Skype za biznis se ponovo prijavljuju. (#9295)
* NVDA ponovo može da stišava pozadinske zvukove kada  se koristi SAPI5 sintetizator na Windowsu 11. (#12913)
* U Kalkulatoru Windowsa 10, NVDA će izgovarati oznake za istoriju i stavke liste memorije. (#11858)
* Prečice kao što su pomeranje brajevog reda i prebacivanje ponovo rade na HID brajevim uređajima. (#13228)
* Windows 11 Mail: Nakon prebacivanja fokusa između aplikacija, dok se čita duža EMail poruka, NVDA se više neće zaglavljivati na jednom redu poruke. (#13050)
* HID brajevi uređaji: Vezane komande  (na primer  `razmak+Tačka4`) se mogu uspešno izvršiti sa brajevog reda. (#13326)
* Ispravljena greška koja je dozvoljavala da se otvori više dijaloga sa podešavanjima u isto vreme. (#12818)
* Ispravljen problem koji je izazvao da određeni Focus Blue brajevi redovi prestanu da rade nakon što probudite računar iz stanja spavanja. (#9830)
* "Osnovna linija " se više ne izgovara bespotrebno kada je opcija "prijavi indekse i eksponente" omogućena. (#11078)
* U Windowsu 11, NVDA više neće sprečavati navigaciju kroz Emoji panel kada se bira emoji. (#13104)
* Sprečena greška koja izaziva dvostruko prijavljivanje kada se koristi Windows konzola i terminal. (#13261)
* Ispravljeno nekoliko slučajeva u kojima stavke liste nisu mogle biti prijavljene u 64 bitnim aplikacijama, kao što je REAPER. (#8175)
* U upravljaču preuzimanja programa Microsoft Edge, NVDA će se automatski prebaciti u režim fokusiranja kada stavka liste sa najnovijim preuzimanjem postane fokusirana. (#13221)
* NVDA više neće izazvati rušenje 64-bitnih verzija programa Notepad++ 8.3 i novijih. (#13311)
* Adobe Reader se više ne ruši pri pokretanju ako je njegov zaštićen režim omogućen. (#11568)
* Ispravljena greška koja je izazivala rušenje programa NVDA kada se izabere  Papenmeier drajver brajevog reda. (#13348)
* Microsoft word uz UIA: Broj stranice i druge informacije o formatiranju se više ne izgovaraju bespotrebno kada se prebacite iz prazne ćelije tabele u ćeliju sa sadržajem, ili sa kraja dokumenta na postojeći sadržaj. (#13458, #13459)
* NVDA više neće imati problema sa prijavljivanjem naslova stranice i početka automatskog čitanja, kada se stranica učita u programu Google chrome 100. (#13571)
* NVDA se više ne ruši kada se podešavanja vrate na fabričke vrednosti uz uključen izgovor komandnih tastera. (#13634)

### Promene za programere (engleski)

* Note: this is a Add-on API compatibility breaking release. Add-ons will need to be re-tested and have their manifest updated.
* Although NVDA still requires Visual Studio 2019, Builds should no longer fail if a newer version of Visual Studio (E.g. 2022) is installed along side 2019. (#13033, #13387)
* Updated SCons to version 4.3.0. (#13033)
* Updated py2exe to version 0.11.1.0. (#13510)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` has been removed. Use `apiLevel` instead. (#12955, #12660)
* `TVItemStruct` has been removed from `sysTreeView32`. (#12935)
* `MessageItem` has been removed from the Outlook appModule. (#12935)
* `audioDucking.AUDIODUCKINGMODE_*` constants are now a `DisplayStringIntEnum`. (#12926)
  * usages should be replaced with `AudioDuckingMode.*`
  * usages of `audioDucking.audioDuckingModes` should be replaced with `AudioDuckingMode.*.displayString`
* `audioDucking.ANRUS_ducking_*` constants usages should be replaced with `ANRUSDucking.*`. (#12926)
* `synthDrivers.sapi5` changes (#12927):
  * `SPAS_*` usages should be replaced with `SPAudioState.*`
  * `constants.SVSF*` usages should be replaced with `SpeechVoiceSpeakFlags.*`
    * Note: `SVSFlagsAsync` should be replaced with `SpeechVoiceSpeakFlags.Async` not `SpeechVoiceSpeakFlags.lagsAsync`
  * `constants.SVE*` usages should be replaced with `SpeechVoiceEvents.*`
* The `soffice` appModule has the following classes and functions removed `JAB_OOTableCell`, `JAB_OOTable`, `gridCoordStringToNumbers`. (#12849)
* `core.CallCancelled` is now `exceptions.CallCancelled`. (#12940)
* All constants starting with RPC from `core` and `logHandler` are moved into `RPCConstants.RPC` enum. (#12940)
* It is recommended that `mouseHandler.doPrimaryClick` and `mouseHandler.doSecondaryClick` functions should be used to click the mouse to perform a logical action such as activating (primary) or secondary (show context menu),
rather than using `executeMouseEvent` and specifying the left or right mouse button specifically.
This ensures code will honor the Windows user setting for swapping the primary mouse button. (#12642)
* `config.getSystemConfigPath` has been removed - there is no replacement. (#12943)
* `shlobj.SHGetFolderPath` has been removed - please use `shlobj.SHGetKnownFolderPath` instead. (#12943)
* `shlobj` constants have been removed. A new enum has been created, `shlobj.FolderId` for usage with `SHGetKnownFolderPath`. (#12943)
* `diffHandler.get_dmp_algo` and `diffHandler.get_difflib_algo` have been replaced with `diffHandler.prefer_dmp` and `diffHandler.prefer_difflib` respectively. (#12974)
* `languageHandler.curLang` has been removed - to get the current NVDA language use `languageHandler.getLanguage()`. (#13082)
* A `getStatusBarText` method can be implemented on an appModule to customize the way NVDA fetches the text from the status bar. (#12845)
* `globalVars.appArgsExtra` has been removed. (#13087)
  * If your add-on need to process additional command line arguments see the documentation of `addonHandler.isCLIParamKnown` and the developer guide for details.
* The UIA handler module and other UIA support modules are now part of a UIAHandler package. (#10916)
  * `UIAUtils` is now `UIAHandler.utils`
  * `UIABrowseMode` is now `UIAHandler.browseMode`
  * `_UIAConstants` is now `UIAHandler.constants`
  * `_UIACustomProps` is now `UIAHandler.customProps`
  * `_UIACustomAnnotations` is now `UIAHandler.customAnnotations`
* The `IAccessibleHandler` `IA2_RELATION_*` constants have been replaced with the `IAccessibleHandler.RelationType` enum. (#13096)
  * Removed `IA2_RELATION_FLOWS_FROM`
  * Removed `IA2_RELATION_FLOWS_TO`
  * Removed `IA2_RELATION_CONTAINING_DOCUMENT`
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` and `LOCALE_SLANGDISPLAYNAME` are removed from `languageHandler` - use members of `languageHandler.LOCALE` instead. (#12753)
* Switched from Minhook to Microsoft Detours as a hooking library for NVDA. Hooking with this library is mainly used to aid the display model. (#12964)
* `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` is removed. (#13211)
* SCons now warns to build with a number of jobs that is equal to the number of logical processors in the system.
This can dramatically decrease build times on multi core systems. (#13226, #13371)
* `characterProcessing.SYMLVL_*` constants are removed - please use `characterProcessing.SymbolLevel.*` instead. (#13248)
* Functions `loadState` and `saveState` are removed from addonHandler - please use `addonHandler.state.load` and `addonHandler.state.save` instead. (#13245)
* Moved the UWP/OneCore interaction layer of NVDAHelper [from C++/CX to C++/Winrt](https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx). (#10662)
* It is now mandatory to subclass `DictionaryDialog` to use it. (#13268)
* `config.RUN_REGKEY`, `config.NVDA_REGKEY` are deprecated, please use `config.RegistryKey.RUN`, `config.RegistryKey.NVDA` instead. These will be removed in 2023. (#13242)
* `easeOfAccess.ROOT_KEY`, `easeOfAccess.APP_KEY_PATH` are deprecated, please use`easeOfAccess.RegistryKey.ROOT`, `easeOfAccess.RegistryKey.APP` instead. These will be removed in 2023. (#13242)
* `easeOfAccess.APP_KEY_NAME` has been deprecated, to be removed in 2023. (#13242)
* `DictionaryDialog` and `DictionaryEntryDialog` are moved from `gui.settingsDialogs` to `gui.speechDict`. (#13294)
* IAccessible2 relations are now shown in developer info for IAccessible2 objects. (#13315)
* `languageHandler.windowsPrimaryLCIDsToLocaleNames` has been removed, instead use `languageHandler.windowsLCIDToLocaleName` or `winKernel.LCIDToLocaleName`. (#13342)
* `UIAAutomationId` property for UIA objects should be preferred over `cachedAutomationId`. (#13125, #11447)
  * `cachedAutomationId` can be used if obtained directly from the element.
* `NVDAObjects.window.scintilla.CharacterRangeStruct` has moved to `NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct`. (#13364)
* Boolean `gui.isInMessageBox` is removed, please use the function `gui.message.isModalMessageBoxActive` instead. (#12984, #13376)
* `controlTypes` has been split up into various submodules. (#12510, #13588)
  * `ROLE_*` and `STATE_*` have been replaced with `Role.*` and `State.*`.
  * Although still available, the following should be considered deprecated:
    * `ROLE_*` and `STATE_*`, use `Role.*` and `State.*` instead.
    * `roleLabels`, `stateLabels` and `negativeStateLabels`, usages like `roleLabels[ROLE_*]` should be replaced with their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
    * `processPositiveStates` and `processNegativeStates` should use `processAndLabelStates` instead.
* Excel cell state constants (`NVSTATE_*`) are now values in the `NvCellState` enum, mirrored in the `NvCellState` enum in `NVDAObjects/window/excel.py` and mapped to `controlTypes.State` via _nvCellStatesToStates. (#13465)
* `EXCEL_CELLINFO` struct member `state` is now `nvCellStates`.
* `mathPres.ensureInit` has been removed, MathPlayer is now initialized when NVDA starts. (#13486)

## 2021.3.5

Ovo je manje ažuriranje kako bi se ispravio bezbednosni problem.
Molimo odgovorno prijavite bezbednosne probleme na adresu <info@nvaccess.org>.

### Bezbednosne ispravke

* Ispravljena bezbednosna preporuka `GHSA-xc5m-v23f-pgr7`.
  * Dijalog izgovora znakova interpunkcije i simbola je sada onemogućen u bezbednom načinu rada.

## 2021.3.4

Ovo je manje ažuriranje kako bi se ispravilo nekoliko prijavljenih bezbednosnih problema.
Molimo odgovorno prijavite bezbednosne probleme na adresu  <info@nvaccess.org>.

### Bezbednosne ispravke

* Ispravljena bezbednosna preporuka `GHSA-354r-wr4v-cx28`. (#13488)
  * Uklonjena mogućnost da se NVDA pokrene uz omogućene dnevnike za otklanjanje grešaka kada je NVDA pokrenut u bezbednom načinu rada.
  * Uklonjena mogućnost da se NVDA ažurira kada je pokrenut u bezbednom načinu rada.
* Ispravljena bezbednosna preporuka `GHSA-wg65-7r23-h6p9`. (#13489)
  * Uklonjena mogućnost otvaranja dijaloga ulaznih komandi u bezbednom načinu rada.
  * Uklonjena mogućnost otvaranja podrazumevanog, privremenog i govornog rečnika u bezbednom načinu rada.
* Ispravljena bezbednosna preporuka `GHSA-mvc8-5rv9-w3hx`. (#13487)
  *  wx GUI inspection alatka je sada onemogućena u bezbednom načinu rada.

## 2021.3.3

Ova verzija je identična verziji 2021.3.2.
Došlo je do greške u verziji NVDA 2021.3.2 pa se ona identifikovala kao 2021.3.1.
Ova verzija se ispravno identifikuje kao 2021.3.3.

## 2021.3.2

Ovo je manje ažuriranje kako bi se ispravilo nekoliko prijavljenih bezbednosnih problema.
Molimo odgovorno prijavite bezbednosne probleme na adresu  <info@nvaccess.org>.

### Ispravljene greške

* Bezbednosna ispravka: Sprečavanje objektne navigacije van zaključanog ekrana na Windowsu 10 i Windowsu 11. (#13328)
* Bezbednosna ispravka: Ekran upravljača dodacima je sada onemogućen na bezbednim ekranima. (#13059)
* Bezbednosna ispravka: NVDA kontekstna pomoć više nije dostupna na bezbednim ekranima. (#13353)

## 2021.3.1

Ovo je manje ažuriranje kako bi se ispravilo nekoliko grešaka u verziji 2021.3.

### Promene

* Novi HID brajev protokol više nije izabran u situacijama kada postoji drugi drajver za brajev red koji se može koristiti. (#13153)
* Novi HID brajev protokol se može onemogućiti korišćenjem opcije u panelu naprednih podešavanja. (#13180)

### Ispravljene greške

* Orjentiri će ponovo imati skraćenice na brajevom redu. #13158
* Ispravljjena nestabilnost u automatskom prepoznavanju brajevih redova Humanware Brailliant i  APH Mantis Q40 kada se koriste putem  Bluetooth veze. (#13153)

## 2021.3

Ova verzija uključuje podršku za novi brajev HID standard.
Ovaj standard ima za cilj da standardizuje podršku za različite brajeve redove bez potrebe da se instaliraju različiti drajveri.
Ažurirani su eSpeak-NG i LibLouis, koji sada uključuje nove Ruske i Tshivenda tabele.
Zvukovi za greške se sada mogu omogućiti u stabilnim NVDA verzijama novom opcijom u naprednim podešavanjima.
Režim izgovori sve sada pomera dokument kako bi trenutna pozicija bila vidljiva.
Brojna poboljšanja kada se koristi Office uz UIA.
Jedno od ovih UIA poboljšanja je da Outlook ignoriše veći broj tabela koje služe samo za izgled u porukama.

Važne napomene:

Zbog ažuriranja naših bezbednosnih sertifikata, manji broj korisnika dobija grešku kada NVDA 2021.2 proverava ažuriranja.
NVDA će sada zahtevati da Windows ažurira bezbednosne sertifikate, što će u budućnosti sprečiti ovu grešku.
Korisnici koji su dobili ovu grešku moraju ručno da preuzmu ovo ažuriranje.

### Nove karakteristike

* Dodata ulazna komanda za uključivanje i isključivanje prijavljivanja stilova granica ćelija. (#10408)
* Podrška za novi HID brajev standard koji za cilj ima standardizaciju podrške za brajeve redove. (#12523)
  * NVDA će automatski prepoznati uređaje koji podržavaju ovaj standard.
  * Za tehničke napomene o implementaciji ovog standarda od strane programa NVDA, pogledajte https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Dodata podrška za VisioBraille Vario 4 brajev uređaj. (#12607)
* Obaveštenja o greškama se mogu omogućiti (iz naprednih podešavanja) u bilo kojoj NVDA verziji. (#12672)
* U Windowsu 10 i novijim, NVDA će izgovoriti broj predloga kada upisujete termine pretrage u aplikacijama kao što su podešavanja i Microsoft prodavnica. (#7330, #12758, #12790)
* Navigacija kroz tabele je sada podržana u kontrolama koje su napravljene korišćenjem Out-GridView cmdlet u  PowerShell. (#12928)

### Promene

* Espeak-ng je ažuriran na 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* NVDA će podrazumevano koristiti eSpeak ako nijedan instaliran OneCore glas ne podržava željeni NVDA jezik. (#10451)
* Ako OneCore ne govore nakon više pokušaja, ESpeak će biti korišćen kao sintetizator. (#11544)
* Kada čitate statusnu traku prečicom `NVDA+end`, pregledni kursor se više ne prebacuje na njenu lokaciju.
Ako vam je ova funkcija potrebna molimo dodelite prečicu odgovarajućoj komandi u kategoriji objektne navigacije dijaloga ulaznih komandi. (#8600)
* Kada otvarate dijalog sa podešavanjima koji je već otvoren, NVDA će postaviti fokus na postojeći dijalog umesto da izbacuje grešku. (#5383)
* Ažuriran liblouis brajev prevodilac na [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Nove brajeve tabele: Ruski stepen 1, Tshivenda stepen 1, Tshivenda stepen 2
  * NVDA neće više pokušavati da se zatvori kada su otvoreni dijalozi koji zahtevaju potvrdu (na primer uz dostupne opcije potvrdi / otkaži). (#12984)
--

### Ispravljene greške

* Praćenje modifikatorskih tastera na tastaturi (kao što su Kontrol, ili Insert) bolje radi u situacijama u kojima se watchdog oporavlja. (#12609)
* Provera NVDA ažuriranja na određenim sistemima je ponovo moguća; na primer nove Windows instalacije. (#12729)
* NVDA ispravno izgovara prazne ćelije tabele u programu Microsoft Word kada koristite UI automation. (#11043)
* U ćelijama ARIA mreža podataka na Webu, taster Escape će sada biti prosleđen i neće izlaziti iz režima fokusiranja. (#12413)
* Kada se čitaju zaglavlja ćelija u tabelama u programu Chrome, ispravljeno dvostruko izgovaranje naziva kolone. (#10840)
* NVDA više ne izgovara brojčanu vrednost za UIA klizače koji imaju tekstualnu oznaku. (UIA ValuePattern se sada preferira u odnosu na RangeValuePattern). (#12724)
* NVDA više ne smatra da UIA klizači uvek imaju procentualnu vrednost.
* Prijavljivanje lokacije ćelija u programu Microsoft Excel kada se koristi UI Automation ponovo ispravno radi uz Windows 11. (#12782)
* NVDA više ne postavlja neispravne Python lokalizacije. (#12753)
* Ako se onemogućeni dodatak deinstalira a zatim ponovo instalira biće omogućen. (#12792)
* Ispravljene greške sa ažuriranjem i uklanjanjem dodataka kada folder sa dodatkom promeni svoj naziv ili ostane otvoren. (#12792, #12629)
* Kada se koristi UI Automation za pristup Microsoft Excel kontrolama ćelija, NVDA više neće bespotrebno izgovarati da je jedna ćelija izabrana. (#12530)
* Više tekstualnih informacija će biti pročitano u dijalozima programa LibreOffice Writer, na primer u potvrdnim dijalozima. (#11687)
* Čitanje i navigacija u režimu pretraživanja programa Microsoft Word kada se koristi UI automation sada uvek proverava da je trenutna pozicija u režimu pretraživanja uvek vidljiva, kao i da pozicija kursora u režimu fokusiranja odgovara poziciji režima pretraživanja. (#9611)
* Kada koristite komandu izgovori sve u programu Microsoft Word uz UI automation, dokument se sada automatski pomera, i pozicija kursora se ispravno ažurira. (#9611)
* Kada čitate EMail poruke u programu Outlook i NVDA pristupa poruci uz UI Automation, određene tabele su sada označene kao tabele za izgled, što znači da podrazumevano neće biti prijavljene. (#11430)
* Retka greška kada se menjaju zvučni uređaji je ispravljena. (#12620)
* Unos u književnim brajevim tabelama bi trebao da radi stabilnije u poljima za uređivanje. (#12667)
* Kada se krećete kroz Windows kalendar u sistemskoj traci, NVDA sada prijavljuje ceo dan u nedelji. (#12757)
* Kada koristite Kineski metod unosa kao što je Tajvanski - Microsoft Quick u programu Microsoft Word, pomeranje brajevog reda napred i nazad više neće neispravno vraćati kursor na prethodnu poziciju. (#12855)
* Kada pristupate dokumentima u programu Microsoft Word uz UIA, navigacija po rečenicama (alt+StrelicaDole / alt+StrelicaGore) ponovo radi ispravno. (#9254)
* Kada se pristupa programu MS Word uz UIA, uvlačenje pasusa se ponovo prijavljuje. (#12899)
* Kada se pristupa programu MS Word uz UIA, komanda za praćenje izmena kao i određene druge lokalizovane komande biće ispravno prijavljene . (#12904)
* Ispravljena dupla izgovaranja ili informacije na brajevom redu kada se 'opis' podudara sa  'sadržajem' ili 'nazivom'. (#12888)
* U programu MS Word sa omogućenom UIA podrškom, preciznija reprodukcija zvukova za pravopisne greške u toku pisanja. (#12161)
* U Windowsu 11, NVDA više neće izgovarati "Okno" kada pritiskate alt plus tab da se prebacujete između otvorenih programa. (#12648)
* Novo moderno okno za praćenje komentara je sada podržano u programu MS Word kada se dokumentu ne pristupa uz UIA. Pritisnite alt+f12 da se prebacujete između okna i dokumenta. (#12982)

### Promene za programere (engleski)

* Building NVDA now requires Visual Studio 2019 16.10.4 or later.
To match the production build environment, update Visual Studio to keep in sync with the [current version AppVeyor is using](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019). (#12728)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` has been deprecated for removal in 2022.1. (#12660)
  * Instead use `apiLevel` (see the comments at `_UIAConstants.WinConsoleAPILevel` for details).
* Transparency of text background color sourced from GDI applications (via the display model), is now exposed for add-ons or appModules. (#12658)
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` and `LOCALE_SLANGDISPLAYNAME` are moved to the `LOCALE` enum in languageHandler.
They are still available at the module level but are deprecated and to be removed in NVDA 2022.1. (#12753)
* The usage of functions `addonHandler.loadState` and `addonHandler.saveState` should be replaced with their equivalents `addonHandler.state.save` and `addonHandler.state.load` before 2022.1. (#12792)
* Braille output can now be checked in system tests. (#12917)

## 2021.2

Ova verzija uključuje preliminarnu Windows 11 podršku.
Iako Windows 11 još uvek nije zvanično dostupan, ova verzija je testirana na insajderskim verzijama Windowsa 11.
Ovo uključuje važne popravljene probleme sa zatamnjivanjem ekrana (pročitajte važne napomene ).
COM Registration Fixing alatka sada može da ispravi više problema.
Ažurirani su sintetizator eSpeak i brajev prevodilac LibLouis.
Takođe su ispravljeni važni problemi, posebno vezani za brajevu podršku i Windows terminal, Kalkulator, emoji panel i istoriju privremene memorije.

### Važne napomene

Zbog promene u API-u za Windows lupu, zatamnjivanje ekrana je ažurirano kako bi podržavalo najnovije Windows verzije.
Koristite  NVDA 2021.2 da biste aktivirali zatamnjivanje ekrana na Windowsu 10 21H2 (10.0.19044) ili novijim.
Ovo uključuje insajderske verzije Windowsa 10 kao i Windows 11.
Kako biste se uverili u svoju privatnost, kada koristite noviju Windows verziju, vizuelno potvrdite da zatamnjivanje ekrana čini da ekran bude potpuno crn.

### Nove karakteristike

* Eksperimentalna podrška za ARIA napomene:
  * Dodata komanda za čitanje detalja objekta koji ima aria-details. (#12364)
  * Dodata opcija u naprednim podešavanjima za prijavljivanje kada objekat sadrži detalje u režimu pretraživanja. (#12439) 
* U  Windowsu 10 na verziji 1909 i novijim (što uključuje Windows 11), NVDA će izgovarati broj predloga kada pretražujete datoteke u istraživaču datoteka. (#10341, #12628)
* U programu Microsoft Word, NVDA će sada izgovarati rezultate uvlačenja kao i hanging uvlačenja kada se koriste prečice za ove opcije. (#6269)

### Promene

* Espeak-ng je ažuriran na 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Ako je prijavljivanje članaka omogućeno u podešavanjima formatiranja dokumenta, NVDA će izgovoriti  "članak" nakon sadržaja. (#11103)
* Ažuriran liblouis brajev prevodilac na  [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Nove brajeve tabele: Bugarski stepen 1, Burmese stepen 1, Burmese stepen 2, Kazakh stepen 1, Khmer stepen 1, Severni Kurdiški  stepen 0, Sepedi stepen 1, Sepedi stepen 2, Sesotho stepen 1, Sesotho stepen 2, Setswana stepen 1, Setswana stepen 2, Tatar stepen 1, Vijetnamski  stepen 0, Vijetnamski  stepen 2, Južni vijetnamski  stepen 1, Xhosa stepen 1, Xhosa stepen 2, Yakut stepen 1, Zulu stepen 1, Zulu stepen 2
* Windows 10 OCR je preimenovan u Windows OCR. (#12690)

### Ispravljene greške

* U Windows 10 kalkulatoru, NVDA će prikazivati izraze računanja na brajevom redu. (#12268)
* U terminal programima na Windowsu 10 verziji 1607 i novijim, kada se ubacuju ili brišu znakovi u sredini reda, znakovi desno od kursora se više ne čitaju. (#3200)
  * Diff Match Patch je  sada podrazumevano omogućen. (#12485)
* Brajev unos ispravno radi sa sledećim tabelama kratkopisa: Arapski stepen 2, Španski stepen 2, Urdu stepen 2, Kineski  (Kina, Mandarinski) stepen 2. (#12541)
* COM Registration Fixing alatka sada ispravlja više problema, posebno na 64 bitnim verzijama Windowsa. (#1256)
* Poboljšanja u podršci za tastere na Seika brajevoj beležnici kompanije Nippon Telesoft. (#12598)
* Poboljšanja u izgovaranju Windows Emoji panela i istorije privremene memorije. (#11485)
* Ažurirani opisi znakova alfabeta za Bengali. (#12502)
* NVDA će bezbedno izaći kada se pokrene novi proces. (#12605)
* Ponovno biranje Handy Tech drajvera za brajev red u dijalogu za izbor brajevog reda više ne izaziva greške. (#12618)
* Windows verzija 10.0.22000 i novije se sada prepoznaju kao Windows 11, ne Windows 10. (#12626)
* Ako nema prikazanih rezultata kada se pretražuju ulazne komande, dijalog ulaznih komandi nastavlja da radi kako treba. (#12673)
* Podrška za zatamnjivanje ekrana je ispravljena i testirana na Windows verzijama do  10.0.22000. (#12684)
* Ispravljena greška koja je izazivala da se prva stavka podmenija u nekim situacijama ne izgovara. (#12624)

### Promene za programere (engleski)

* `characterProcessing.SYMLVL_*` constants should be replaced using their equivalent `SymbolLevel.*` before 2022.1. (#11856, #12636)
* `controlTypes` has been split up into various submodules, symbols marked for deprecation must be replaced before 2022.1. (#12510)
  * `ROLE_*` and `STATE_*` constants should be replaced to their equivalent `Role.*` and `State.*`.
  * `roleLabels`, `stateLabels` and `negativeStateLabels` have been deprecated, usages such as `roleLabels[ROLE_*]` should be replaced to their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
  * `processPositiveStates` and `processNegativeStates` have been deprecated for removal.
* On Windows 10 Version 1511 and later (including Insider Preview builds), the current Windows feature update release name is obtained from Windows Registry. (#12509)
* Deprecated: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` will be removed in 2022.1, there is no direct replacement. (#12544)

## 2021.1

Ova verzija sadrži opciju koja se može omogućiti za UIA podršku u programu Excel i Chromium pretraživačima.
Ispravljeni su problemi vezani za određene jezike, kao i  pristup linkovima na brajevom redu.
Ažurirane su baze Unicode CLDR,  matematički simboli i LibLouis.
Kao i puno ispravljenih grešaka i poboljšanja, uključujući u Office paketima, Visual Studiu, i nekoliko jezika.

Napomena:

 * Za ovu verziju, neophodno je ažuriranje dodataka kako bi bili kompatibilni.
 * Ova verzija takođe ukida podršku za Adobe Flash.

### Nove karakteristike

* Prva faza podrške za UIA sa pretraživačima baziranim na Chromiumu  (kao što su Edge). (#12025)
* Opciona eksperimentalna podrška za Microsoft Excel korišćenjem UI Automation. Preporučuje se samo uz Microsoft Excel verziju 16.0.13522.10000 ili novije. (#12210)
* Lakša navigacija kroz izlazne rezultate NVDA Python konzole. (#9784)
  * alt+strelice gore i dole  vas  pomeraju na prethodni i sledeći rezultat (dodajte šift da biste izabrali).
  * control+l će obrisati okno sa izlazom.
* NVDA će sada prijaviti kategorije koje su obeležene za obaveze u aplikaciji Microsoft Outlook, ako postoje. (#11598)
* Podrška za Seika beležnicu kompanije Nippon Telesoft. (#11514)

### Promene

* U režimu pretraživanja, kontrole se sada mogu aktivirati prebacivanjem kursora brajeve ćelije na njihov opis (na primer  "lnk" za link). Ovo je posebno korisno  za aktivaciju izbornih polja koja nemaju oznaku. (#7447)
* NVDA će sada sprečiti korisnika da izvrši Windows 10 OCR ako je zatamnjivanje ekrana omogućeno. (#11911)
* Ažurirana Unicode Common Locale  baza (CLDR) na verziju  39.0. (#11943)
* Dodato još matematičkih simbola u rečnik sa simbolima. (#11467)
* Korisničko uputstvo, datoteka sa listom promena, kao i lista komandi sada imaju osvežen izgled. (#12027)
* "Nije podržano" će sada biti izgovoreno ako pokušate da promenite opciju koristi izgled ekrana u aplikacijama u kojima ovo nije moguće, kao što je Microsoft Word. (#7297)
* Opcija "Pokušavanje otkazivanja govora za kontrole koje više nisu fokusirane" u panelu naprednih podešavanja sada je podrazumevano omogućena. (#10885)
  * Ovakav način rada se može onemogućiti promenom ove opcije u "Ne".
  * Sa ovom opcijom omogućenom, Web aplikacije (na primer Gmail) više ne izgovaraju nevažeće informacije kada brzo pomerate fokus.
* Ažuriran liblouis brajev prevodilac na [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Nove brajeve tabele: Beloruski književni brajev kod, Beloruski kompjuterski kod, Urdu stepen 1, Urdu stepen 2.
* Podrška za Adobe Flash sadržaj je uklonjena iz  NVDA budući da se korišćenje  Flash tehnologije ne preporučuje od strane  kompanije Adobe. (#11131)
* NVDA će uspešno izaći čak i ako postoje otvoreni prozori, proces izlaska će sada zatvoriti sve druge NVDA procese i prozore. (#1740)
* Preglednik govora se sada može zatvoriti prečicom `alt+F4` i ima standardno dugme za zatvaranje za lakšu interakciju korisnika sa uređajima sa prekidačem. (#12330)
* Preglednik brajevog reda sada ima standardno dugme za zatvaranje za lakšu interakciju korisnika sa uređajima sa prekidačem. (#12328)
* U dijalogu liste elemenata, prečica koja aktivira taster "Aktiviraj" je uklonjena u određenim  jezicima kako bi sprečila sukob sa oznakom radio dugmeta za tip elementa. Kada je dostupno, ovo dugme ostaje podrazumevano dugme u dijalogu i može se jednostavno aktivirati tasterom Enter iz liste elemenata. (#6167)

### Ispravljene greške

* Lista poruka u programu Outlook 2010 se ponovo može čitati. (#12241)
* U Terminal aplikacijama na Windowsu 10 verziji 1607 i novijim, kada ubacujete ili brišete znakove u sredini reda, znakovi desno od kursora se više ne čitaju. (#3200)
  * Ova eksperimentalna ispravljena opcija se mora ručno omogućiti u naprednim NVDA podešavanjima menjanjem opcije algoritam za razlikovanje teksta na Diff Match Patch.
* U programu MS Outlook, beskorisno prijavljivanje udaljenosti kada koristite šift plus tab da se vratite iz polja poruke na polje predmeta više ne bi trebalo da bude izgovarano. (#10254)
* U Python konzoli, opcije ubacivanja tabulatora za uvlačenje početka već popunjenog reda kao i izvršavanje automatskog dopunjavanja tasterom tab su sada podržane. (#11532)
* Informacije o formatiranju kao i druge poruke u režimu pretraživanja više ne prikazuju neočekivane prazne redove kada je korišćenje izgleda ekrana omogućeno. (#12004)
* Sada je moguće čitanje komentara u aplikaciji MS Word sa omogućenom UIA podrškom. (#9285)
* Brzina interakcije u aplikaciji Visual Studio je poboljšana. (#12171)
* Ispravljene grafičke greške kao što su nedostaci elemenata kada se NVDA koristi uz jezike koji se čitaju s desna na levo. (#8859)
* Orijentacija grafičkog interfejsa je sada bazirana na NVDA jeziku, a ne sistemskom. (#638)
  * Poznat je problem za ove jezike: Desna granica se spaja sa oznakama i kontrolama. (#12181)
* Python lokalizacija će se sada uvek podudarati sa jezikom podešenim u podešavanjima, i takođe će raditi sa podrazumevanim jezikom. (#12214)
* TextInfo.getTextInChunks neće više prestajati kada se primenjuje na obogaćene kontrole za uređivanje kao što je preglednik NVDA dnevnika. (#11613)
* Ponovo je moguće koristiti NVDA na jezicima koji u svojim imenima sadrže donje crte kao što je de_CH na Windowsu 10 verziji  1803 i 1809. (#12250)
* U programu WordPad, podešavanje prijavljivanja indeksa i eksponenata radi kako treba. (#12262)
* NVDA više neće grešiti u izgovaranju novo fokusiranog sadržaja na Web stranicama ako se stari sadržaj ukloni i zameni novo fokusiranim na istoj poziciji. (#12147)
* Precrtan sadržaj, formatiranje indeksa i eksponenata za celu Excel ćeliju će se sada prijaviti ako se omogući odgovarajuća opcija. (#12264)
* Ispravljeno kopiranje podešavanja iz prenosne kopije u instalaciju kada je podrazumevani folder za podešavanja prazan. (#12071, #12205)
* Ispravljeno neispravno izgovaranje nekih slova sa akcentom ili dijakritičkih znakova kada se omogući opcija "Izgovori reč veliko pre velikog slova ". (#11948)
* Ispravljeno menjanje visine u sintetizatoru Sapi4. (#12311)
* NVDA instalacija sada takođe uzima u obzir opciju `--minimal` na komandnoj liniji i neće reprodukovati zvuk za pokretanje, što prati opisan način rada u dokumentaciji za instalirane i prenosne kopije programa NVDA. (#12289)
* U programima MS Word ili Outlook, taster za brzu navigaciju kroz tabele može da fokusira tabele za izgled ako je opcija "Uključi tabele za izgled" omogućena u podešavanjima režima pretraživanja. (#11899)
* NVDA neće više izgovarati znakove "↑↑↑" za Emoji znakove na određenim jezicima. (#11963)
* Espeak Sada ponovo podržava Cantonese i Mandarinski. (#10418)
* U novom pretraživaču Microsoft Edge baziranom na Chromium tehnologiji, polja za unos teksta kao što je traka za adresu se sada izgovaraju i kada su prazna. (#12474)
* Ispravljen Seika brajev drajver. (#10787)

### Promene za programere (engleski)

* Note: this is an Add-on API compatibility breaking release. Add-ons will need to be re-tested and have their manifest updated.
* NVDA's build system now fetches all Python dependencies with pip and stores them in a Python virtual environment. This is all done transparently.
  * To build NVDA, SCons should continue to be used in the usual way. E.g. executing scons.bat in the root of the repository. Running `py -m SCons` is no longer supported, and `scons.py` has also been removed.
  * To run NVDA from source, rather than executing `source/nvda.pyw` directly, the developer should now use `runnvda.bat` in the root of the repository. If you do try to execute `source/nvda.pyw`, a message box will alert you this is no longer supported.
  * To perform unit tests, execute `rununittests.bat [<extra unittest discover options>]`
  * To perform system tests: execute `runsystemtests.bat [<extra robot options>]`
  * To perform linting, execute `runlint.bat <base branch>`
  * Please refer to readme.md for more details.
* The following Python dependencies have also been upgraded:
  * comtypes updated to 1.1.8.
  * pySerial updated to 3.5.
  * wxPython updated to 4.1.1.
  * Py2exe updated to 0.10.1.0.
* `LiveText._getTextLines` has been removed. (#11639)
  * Instead, override `_getText` which returns a string of all text in the object.
* `LiveText` objects can now calculate diffs by character. (#11639)
  * To alter the diff behaviour for some object, override the `diffAlgo` property (see the docstring for details).
* When defining a script with the script decorator, the 'allowInSleepMode' boolean argument can be specified to control if a script is available in sleep mode or not. (#11979)
* The following functions are removed from the config module. (#11935)
  * canStartOnSecureScreens - use config.isInstalledCopy instead.
  * hasUiAccess and execElevated - use them from the systemUtils module.
  * getConfigDirs - use globalVars.appArgs.configPath instead.
* Module level REASON_* constants are removed from controlTypes - please use controlTypes.OutputReason instead. (#11969)
* REASON_QUICKNAV has been removed from browseMode - use controlTypes.OutputReason.QUICKNAV instead. (#11969)
* `NVDAObject` (and derivatives) property `isCurrent` now strictly returns Enum class `controlTypes.IsCurrent`. (#11782)
  * `isCurrent` is no longer Optional, and thus will not return None.
    * When an object is not current `controlTypes.IsCurrent.NO` is returned.
* The `controlTypes.isCurrentLabels` mapping has been removed. (#11782)
  * Instead use the `displayString` property on a `controlTypes.IsCurrent` enum value.
    * For example: `controlTypes.IsCurrent.YES.displayString`.
* `winKernel.GetTimeFormat` has been removed - use `winKernel.GetTimeFormatEx` instead. (#12139)
* `winKernel.GetDateFormat` has been removed - use `winKernel.GetDateFormatEx` instead. (#12139)
* `gui.DriverSettingsMixin` has been removed - use `gui.AutoSettingsMixin`. (#12144)
* `speech.getSpeechForSpelling` has been removed - use `speech.getSpellingSpeech`. (#12145)
* Commands cannot be directly imported from speech as `import speech; speech.ExampleCommand()` or `import speech.manager; speech.manager.ExampleCommand()` - use `from speech.commands import ExampleCommand` instead. (#12126)
* `speakTextInfo` will no longer send speech through `speakWithoutPauses` if reason is `SAYALL`, as `SayAllHandler` does this manually now. (#12150)
* The `synthDriverHandler` module is no longer star imported into `globalCommands` and `gui.settingsDialogs` - use `from synthDriverHandler import synthFunctionExample` instead. (#12172)
* `ROLE_EQUATION` has been removed from controlTypes - use `ROLE_MATH` instead. (#12164)
* `autoSettingsUtils.driverSetting` classes are removed from `driverHandler` - please use them from `autoSettingsUtils.driverSetting`. (#12168)
* `autoSettingsUtils.utils` classes are removed from `driverHandler` - please use them from `autoSettingsUtils.utils`. (#12168)
* Support of `TextInfo`s that do not inherit from `contentRecog.BaseContentRecogTextInfo` is removed. (#12157)
* `speech.speakWithoutPauses` has been removed - please use `speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses` instead. (#12195, #12251)
* `speech.re_last_pause` has been removed - please use `speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause` instead. (#12195, #12251)
* `WelcomeDialog`, `LauncherDialog` and `AskAllowUsageStatsDialog` are moved to the `gui.startupDialogs`. (#12105)
* `getDocFilePath` has been moved from `gui` to the `documentationUtils` module. (#12105)
* The gui.accPropServer module as well as the AccPropertyOverride and ListCtrlAccPropServer classes from the gui.nvdaControls module have been removed in favor of WX native support for overriding accessibility properties. When enhancing accessibility of WX controls, implement wx.Accessible instead. (#12215)
* Files in `source/comInterfaces/` are now more easily consumable by developer tools such as IDEs. (#12201)
* Convenience methods and types have been added to the winVersion module for getting and comparing Windows versions. (#11909)
  * isWin10 function found in winVersion module has been removed.
  * class winVersion.WinVersion is a comparable and order-able type encapsulating Windows version information.
  * Function winVersion.getWinVer has been added to get a winVersion.WinVersion representing the currently running OS.
  * Convenience constants have been added for known Windows releases, see winVersion.WIN* constants.
* IAccessibleHandler no longer star imports everything from IAccessible and IA2 COM interfaces - please use them directly. (#12232)
* TextInfo objects now have start and end properties which can be compared mathematically with operators such as < <= == != >= >. (#11613)
  * E.g. ti1.start <= ti2.end
  * This usage is now prefered instead of ti1.compareEndPoints(ti2,"startToEnd") <= 0
* TextInfo start and end properties can also be set to each other. (#11613)
  * E.g. ti1.start = ti2.end
  * This usage is prefered instead of ti1.SetEndPoint(ti2,"startToEnd")
* `wx.CENTRE_ON_SCREEN` and `wx.CENTER_ON_SCREEN` are removed, use `self.CentreOnScreen()` instead. (#12309)
* `easeOfAccess.isSupported` has been removed, NVDA only supports versions of Windows where this evaluates to `True`. (#12222)
* `sayAllHandler` has been moved to `speech.sayAll`. (#12251)
  * `speech.sayAll.SayAllHandler` exposes the functions `stop`, `isRunning`, `readObjects`, `readText`, `lastSayAllMode`.
  * `SayAllHandler.stop` also resets the `SayAllHandler` `SpeechWithoutPauses` instance.
  * `CURSOR_REVIEW` and `CURSOR_CARET` has been replaced with `CURSOR.REVIEW` and `CURSOR.CARET`.
* `speech.SpeechWithoutPauses` has been moved to `speech.speechWithoutPauses.SpeechWithoutPauses`. (#12251)
* `speech.curWordChars` has been renamed `speech._curWordChars`. (#12395)
* the following have been removed from `speech` and can be accessed through `speech.getState()`. These are readonly values now. (#12395)
  * speechMode
  * speechMode_beeps_ms
  * beenCanceled
  * isPaused
* to update `speech.speechMode` use `speech.setSpeechMode`. (#12395)
* the following have been moved to `speech.SpeechMode`. (#12395)
  * `speech.speechMode_off` becomes `speech.SpeechMode.off`
  * `speech.speechMode_beeps` becomes `speech.SpeechMode.beeps`
  * `speech.speechMode_talk` becomes `speech.SpeechMode.talk`
* `IAccessibleHandler.IAccessibleObjectIdentifierType` is now `IAccessibleHandler.types.IAccessibleObjectIdentifierType`. (#12367)
* The following in `NVDAObjects.UIA.WinConsoleUIA` have been changed (#12094)
  * `NVDAObjects.UIA.winConsoleUIA.is21H1Plus` renamed `NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable`.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo` renamed to start class name with upper case.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1` renamed `NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive`
    * The implementation works around both end points being inclusive (in text ranges) before [microsoft/terminal PR 4018](https://github.com/microsoft/terminal/pull/4018)
    * Workarounds for `expand`, `collapse`, `compareEndPoints`, `setEndPoint`, etc

## 2020.4

Ova verzija uključuje podršku za nove Kineske metode unosa, ažuriranje za Liblouis i lista elemenata (NVDA+f7) sada radi u režimu fokusiranja.
Pomoć vezana za sadržaj je sada dostupna kada se pritisne F1 u NVDA dijalozima.
Poboljšanja za pravila izgovaranja simbola, govorne rečnike, brajeve poruke i površno čitanje.
Ispravljene greške i poboljšanja u aplikacijama Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
Na Webu, poboljšanja u aplikaciji Google Docs, i bolja podrška za ARIA standard.
Takođe puno drugih poboljšanja i ispravljenih grešaka.

### Nove karakteristike

* Pritiskanjem tastera F1 u NVDA dijalozima otvoriće se relevantna sekcija pomoći. (#7757)
* Podrška za predloge automatskog dopunjavanja (IntelliSense) u programima Microsoft SQL Server Management Studio plus Visual Studio 2017 i novijim. (#7504)
* Izgovor simbola interpunkcije: Podrška za grupisanja u definisanju kompleksnih simbola i podrška za prikazivanje ovih grupa u zamenama što ih čini jednostavnijim i korisnijim. (#11107)
* Korisnici će biti obavešteni ako prave zamene u govornim rečnicima sa neispravnim regularnim izrazima. (#11407)
  * Tačnije, greške u grupisanju se sada prepoznaju.
* Dodata podrška za nove brzi Kineski tradicionalni i Pinyin metode unosa u Windowsu 10. (#11562)
* Zaglavlja kartica se sada smatraju kao polja za unos u brzoj navigaciji tasterom F. (#10432)
* Dodata skripta za prijavljivanje obeleženog (markiranog) teksta; nema podrazumevano podešene komande. (#11807)
* Dodat --copy-portable-config parametar komandne linije koji vam omogućava da kopirate podešavanja u tihoj instalaciji programa NVDA. (#9676)
* Prebacivanje na brajevu ćeliju je sada moguće za korisnike miša u pregledniku brajevog reda, prevlačite za prebacivanje na ćeliju. (#11804)
* NVDA će sada automatski prepoznati brajeve redove Humanware Brailliant BI 40X i 20X preko USB i Bluetooth veze. (#11819)

### Promene

* Ažuriran liblouis brajev prevodilac na verziju 3.16.1:
 * Rešava različita rušenja
 * Dodaje brajevu tabelu Baškir stepen 1
 * Dodaje brajevu tablu Koptski osmotačkasti brajev kod
 * Dodaje tabele Ruski književni i Ruski književni (detaljniji)
  * Dodaje brajevu tabelu Afrikanski stepen 2
* Uklanja brajevu tabelu Ruski stepen 1
* Kada čitate u režimu izgovori sve režima pretraživanja komande za pronalaženje sledeće i prethodne stavke više ne zaustavljaju čitanje ako je opcija dozvoli površno čitanje omogućena; režim izgovori sve će umesto toga nastaviti od pronađenog rezultata. (#11563)
* Za HIMS brajeve redove F3 je promenjen u  razmak + tačke 148. (#11710)
* Poboljšanja u korisničkom iskustvu opcija  "vreme isteka poruke" i "prikaži poruke". (#11602)
* U Web pretraživačima i drugim aplikacijama koje podržavaju režim pretraživanja, dijalog liste elemenata (NVDA+F7) sada se može aktivirati iz režima fokusiranja. (#10453)
* Ažuriranja ARIA live regiona se sada ne izgovaraju kada je prijavljivanje dinamičkih promena sadržaja onemogućeno. (#9077)
* NVDA će sada izgovoriti "Kopirano u privremenu memoriju" pre kopiranog teksta. (#6757)
* Predstavljanje grafičkog prikaza tabele u upravljaču diskovima je poboljšano. (#10048)
* Oznake za kontrole su sada onemogućene (zatamnjene) kada je kontrola onemogućena. (#11809)
* Ažurirana CLDR Emoji baza na verziju 38. (#11817)
* Ugrađena opcija "Označavanje fokusa" je preimenovana u "vizuelno označavanje". (#11700)

### Ispravljene greške

* NVDA ponovo ispravno radi sa poljima za uređivanje kada se koristi aplikacija Fast Log Entry. (#8996)
* Preostalo vreme u aplikaciji Foobar2000 će se prijaviti kada nema ukupnog vremena trajanja  (na primer kada se reprodukuje stream uživo). (#11337)
* NVDA sada poštuje atribut aria-roledescription na elementima sa sadržajem koji se može urediti u Web pretraživačima. (#11607)
* "Lista " se sada neće izgovarati na svakom redu liste u aplikaciji Google docs ili nekom drugom sadržaju koji se može urediti u pretraživaču Google chrome. (#7562)
* Kada se strelicama krećete znak po znak ili reč po reč od jedne stavke liste ka drugoj u sadržaju koji se može urediti u Web pretraživačima, ulazak u novu stavku liste se sada izgovara. (#11569)
* NVDA sada čita ispravan red kada se kursor postavi na kraj linka koji je na kraju stavke liste u aplikaciji Google docs ili drugom sadržaju koji se može urediti na Webu. (#11606)
* Na Windowsu 7, otvaranje i zatvaranje start menija sa radne površine sada ispravno postavlja fokus. (#10567)
* Kada je opcija " Pokušavanje otkazivanja govora za kontrole koje više nisu fokusirane " omogućena, naslov kartice se ponovo izgovara kada se menjaju kartice u programu Firefox. (#11397)
* NVDA ponovo izgovara stavku liste kada pišete ime stavke korišćenjem  SAPI5 Ivona glasova. (#11651)
* Ponovo je moguće koristiti režim pretraživanja kada se čitaju mailovi u aplikaciji Windows 10 Mail 16005.13110 i novijim. (#11439)
* Kada koristite SAPI5 Ivona glasove sa lokacije harposoftware.com, NVDA sada može da čuva podešavanja, menja sintetizatore, i više neće gubiti govor nakon ponovnog pokretanja. (#11650)
* Sada je moguće upisati broj 6 u kompjuterskom brajevom kodu sa brajeve tastature HIMS redova. (#11710)
* Ogromna poboljšanja u brzini korišćenja aplikacije Azure Data Studio. (#11533, #11715)
* Uz omogućenu opciju  "Pokušavanje otkazivanja govora za kontrole koje više nisu fokusirane " naslov NVDA dijaloga za pretragu se ponovo izgovara. (#11632)
* NVDA više nebi trebao da prestaje sa radom kada se računar probudi i fokusira na Microsoft edge dokument. (#11576)
* Više nije neophodno pritiskanje tastera Tab ili pomeranje fokusa nakon zatvaranja kontekstnog menija u pretraživaču Edge da bi režim pretraživanja ponovo radio. (#11202)
* NVDA sada ispravno čita stavke liste u 64-bitnim aplikacijama kao što su Tortoise SVN. (#8175)
* ARIA treegrids se sada prikazuju kao standardne tabele u režimu pretraživanja programa Firefox i Chrome. (#9715)
* Obrnuta pretraga se sada može pokrenuti komandom "pronađi prethodnu stavku" prečicom NVDA+šift+F3 (#11770)
* NVDA skripta se više neće ponašati kao da je ponovljena ako se neki drugi taster nevezan za tu skriptu pritisne pre pokretanja skripte. (#11388) 
* Oznake naglašenog teksta se ponovo mogu onemogućiti u programu Internet explorer kada  se onemogući opcija naglašavanja u dijalogu formatiranja dokumenta NVDA podešavanja. (#11808)
* Prestanak rada od nekoliko sekundi za neke korisnike više nebi trebalo da se dešava kada se krećete strelicama kroz ćelije u programu Excel. (#11818)
* U aplikaciji Microsoft Teams sa verzijama kao što su 1.3.00.28xxx, NVDA više neće biti onemogućen da čita poruke ćaskanja zbog neispravno fokusiranog menija. (#11821)
* Tekst koji je u isto vreme označen i kao pravopisna i kao gramatička greška u programu Google Chrome će ispravno biti prijavljen od strane programa NVDA kao pravopisna i gramatička greška. (#11787)
* Kada koristite Outlook (Francuski jezik), prečica za opciju "Odgovori svima" (control+šift+R) ponovo radi. (#11196)
* U aplikaciji Visual Studio, IntelliSense opisi alata koji pružaju dodatne detalje o trenutno izabranoj IntelliSense stavci se sada prijavljuju samo jednom. (#11611)
* U aplikaciji Windows 10 Kalkulator, NVDA neće izgovarati napredak računanja ako je opcija izgovori ukucane znakove onemogućena. (#9428)
* NVDA se više ne ruši kada se koristi tabela Engleski američki stepen 2 i opcija Proširi na kompjuterski brajev kod za reč na poziciji kursora je uključena, kada se prikazuje određen sadržaj kao što je Internet adresa. (#11754)
* Ponovo je moguće prijaviti informacije o formatiranju za fokusiranu Excel ćeliju komandom NVDA+F. (#11914)
* QWERTY unos na Papenmeier brajevim redovima koji ga podržavaju ponovo radi i više ne izaziva nasumična smrzavanja programa NVDA. (#11944)

### Promene za programere (engleski)

* System tests can now send keys using spy.emulateKeyPress, which takes a key identifier that conforms to NVDA's own key names, and by default also blocks until the action is executed. (#11581)
* NVDA no longer requires the current directory to be the NVDA application directory in order to function. (#6491)
* The aria live politeness setting for live regions can now be found on NVDA Objects using the liveRegionPoliteness property. (#11596)
* It is now possible to define separate gestures for Outlook and Word document. (#11196)

## 2020.3

Ova verzija uključuje značajna poboljšanja u stabilnosti i brzini posebno u Microsoft Office aplikacijama. Takođe su dodata nova podešavanja za podršku ekrana osetljivog na dodir i prijavljivanje slika.
Postojanje obeleženog (markiranog) sadržaja se može prijaviti u pretraživačima, i takođe su dodate nove Nemačke brajeve tabele.

### Nove karakteristike

* Sada možete da omogućite ili onemogućite prijavljivanje  slika u panelu podešavanja formatiranja dokumenta. Napomena da čak i kada je ova opcija onemogućena, alternativni tekstovi za slike će se čitati. (#4837)
* Sada možete da omogućite ili onemogućite NVDA podršku za ekrane osetljive na dodir. Dodata je opcija u panel za interakciju sa ekranima osetljivim na dodir u NVDA podešavanjima. Podrazumevana komanda je NVDA+control+alt+t. (#9682)
* Dodate nove Nemačke brajeve tabele. (#11268)
* NVDA sada prepoznaje tekstualne UIA kontrole koje se samo mogu čitati. (#10494)
* Postojanje markiranog (obeleženog) sadržaja se sada izgovara i prijavljuje na brajevom redu u svim Web pretraživačima. (#11436)
 * Ovo se može omogućiti ili onemogućiti novom opcijom za obeležen sadržaj u panelu formatiranja dokumenta.
* Novi emulirani sistemski tasteri se mogu dodati u NVDA dijalogu za ulazne komande. (#6060)
  * Da biste ovo uradili, pritisnite dugme dodaj nakon što ste izabrali kategoriju emulirani tasteri sistemske tastature.
* Brajev red Handy Tech Active Braille sa džojstikom je sada podržan. (#11655)
* Opcija "Automatski režim fokusiranja za pomeranje kursora" sada se može koristiti kada je onemogućena opcija "Automatski postavi sistemski fokus na elemente koji se mogu fokusirati". (#11663)

### Promene

* Skripta za prijavljivanje formatiranja (NVDA+f) je sada promenjena kako bi prijavljivala formatiranje na poziciji sistemskog kursora umesto preglednog kursora programa NVDA. Da biste dobili formatiranje za poziciju preglednog kursora sada koristite NVDA+šift+f. (#9505)
* NVDA sada po podrazumevanim podešavanjima ne pomera sistemski  fokus na elemente koji se mogu fokusirati u režimu pretraživanja, što poboljšava brzinu i stabilnost. (#11190)
* CLDR ažuriran sa verzije 36.1 na verziju 37. (#11303)
* Ažuriran eSpeak-NG na 1.51-dev, commit 1fb68ffffea4
* Sada možete da koristite navigaciju kroz tabele u listama sa elementima koji se mogu čekirati ako lista ima više kolona. (#8857)
* U dijalogu za upravljanje dodacima, kada je neophodno da potvrdite uklanjanje dodatka, "ne" je sada podrazumevano dugme. (#10015)
* U programu Microsoft Excel, lista elemenata sada prikazuje ispravno lokalizovane formule. (#9144)
* NVDA sada prijavljuje ispravne termine za napomene u programu Excel. (#11311)
* Kada koristite komandu "Prebaci pregledni kursor na fokus " u režimu pretraživanja, pregledni kursor se sada postavlja na poziciju virtuelnog kursora. (#9622)
* Informacije koje se prijavljuju u režimu pretraživanja, kao što su informacije o formatiranju komandom NVDA+F, sada su prikazane u malo većem prozoru i centrirane su na ekranu. (#9910)

### Ispravljene greške

* NVDA sada uvek govori kada se krećete reč po reč i dođete do simbola koji je odvojen razmakom bez obzira na podešavanja. (#5133)
* U aplikacijama koje koriste QT 5.11 ili noviji, opisi objekata se ponovo prijavljuju. (#8604)
* Kada brišete reč prečicom control+delete, NVDA više neće biti bez izgovora. (#3298, #11029)
  * Sada se reč desno od obrisane reči izgovara.
* U panelu opštih podešavanja, lista jezika se sada ispravno sortira. (#10348)
* U dijalogu za ulazne komande, bitno poboljšana brzina kada se komande filtriraju. (#10307)
* Sada možete slati unikodne znakove veće od U+FFFF sa brajevog reda. (#10796)
* NVDA će ispravno izgovarati dijaloge za otvaranje datoteka u Windows 10 May 2020 ažuriranju. (#11335)
* Nova eksperimentalna opcija u naprednim podešavanjima (Omogući selektivno registrovanje za UI Automation događaje i promene svojstava) može da pruži ogromna poboljšanja u brzini programa Microsoft Visual Studio i drugim UIAutomation aplikacijama ako je omogućena. (#11077, #11209)
* Za stavke u listama koje se mogu čekirati, status opcije koja je izabrana se više ne izgovara bespotrebno, i ako je to slučaj, umesto toga izgovoriće se kada stavka nije izabrana. (#8554)
* Na Windows 10 May 2020 ažuriranju, NVDA sada prikazuje Microsoft Sound Mapper kada se prikazuju izlazni uređaji u dijalogu za izbor sintetizatora. (#11349)
* U programu Internet Explorer, brojevi se ispravno izgovaraju za liste sa nabrajanjem ako lista ne počinje brojem 1. (#8438)
* U programu Google chrome, NVDA će sada prijaviti nije označeno za sve kontrole koje se mogu označiti (ne samo izborna polja) koje trenutno nisu označene. (#11377)
* Ponovo je moguće kretanje kroz različite kontrole kada je NVDA jezik podešen na Aragonski. (#11384)
* NVDA više neće ponekad prestajati sa radom u programu Microsoft Word kada se brzo krećete strelicama ili pišete znakove uz brajev red. (#11431, #11425, #11414)
* NVDA više ne dodaje nepostojeće razmake kada se navigacioni objekat kopira. (#11438)
* NVDA više ne aktivira profil izgovori sve ako nema šta da se pročita. (#10899, #9947)
* NVDA sada može da čita listu opcija u Internet Information Services (IIS) menadžeru. (#11468)
* NVDA sada ne zatvara izlazni zvučni uređaj što će poboljšati brzinu na određenim zvučnim kartama (#5172, #10721)
* NVDA više neće izlaziti ili prestajati sa radom kada držite control+šift+strelicu dole u programu Microsoft Word. (#9463)
* Prošireno ili skupljeno stanje foldera u prikazu stabla navigacije na sajtu drive.google.com se sada uvek prijavljuje od strane NVDA. (#11520)
* NVDA će automatski prepoznati NLS eReader Humanware brajev red putem Bluetooth veze budući da je njegovo Bluetooth ime sada "NLS eReader Humanware". (#11561)
* Značajno poboljšana brzina korišćenja aplikacije Visual Studio Code. (#11533)

### Promene za programere (engleski)

* The GUI Helper's BoxSizerHelper.addDialogDismissButtons supports a new "separated" keyword argument, for adding a standard horizontal separator to dialogs (other than messages and single input dialogs). (#6468)
* Additional properties were added to app modules, including path for the executable (appPath), is a Windows Store app (isWindowsStoreApp), and machine architecture for the app (appArchitecture). (#7894)
* It is now possible to create app modules for apps hosted inside wwahost.exe on Windows 8 and later. (#4569)
* A fragment of the log can now be delimited and then copied to clipboard using NVDA+control+shift+F1. (#9280)
* NVDA-specific objects that are found by Python's cyclic garbage collector are now logged when being deleted by the collector to aide in removing reference cycles from NVDA. (#11499)
 * The majority of NVDA's classes are tracked including NVDAObjects, appModules, GlobalPlugins, SynthDrivers, and TreeInterceptors.
 * A class that needs to be tracked should inherit from garbageHandler.TrackedObject.
* Significant debug logging for MSAA events can be now enabled in NVDA's Advanced settings. (#11521)
* MSAA winEvents for the currently focused object are no longer filtered out along with other events if the event count for a given thread is exceeded. (#11520)

## 2020.2

Glavne karakteristike ove verzije uključuju podršku za novi brajev red kompanije Nattiq, bolju podršku za ESET antivirus interfejs i Windows Terminal, poboljšanja u brzini korišćenja aplikacije 1Password, kao i uz Windows OneCore sintetizator. Uz puno dodatnih ispravljenih grešaka i poboljšanja.

### Nove karakteristike

* Podrška za nove brajeve redove:
  * Nattiq nBraille (#10778)
* Dodata skripta za otvaranje NVDA foldera sa podešavanjima (bez podrazumevane komande). (#2214)
* Bolja podrška za interfejs programa ESET antivirus. (#10894)
* Dodata podrška za Windows Terminal. (#10305)
* Dodata skripta za prijavljivanje aktivnog profila podešavanja (bez podrazumevane komande). (#9325)
* Dodata skripta za menjanje statusa prijavljivanja indeksa i eksponenata (bez podrazumevane komande). (#10985)
* Web aplikacije (na primer Gmail) više ne izgovaraju nevažeće informacije kada se fokus menja brzo. (#10885)
  * Ovo eksperimentalno podešavanje se mora ručno omogućiti korišćenjem opcije "Pokušavanje otkazivanja govora za kontrole koje više nisu fokusirane " u panelu sa naprednim podešavanjima.
* Puno novih simbola je dodato u rečnik sa simbolima. (#11105)

### Promene

* Ažuriran liblouis brajev prevodilac sa 3.12 na [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Prijavljivanje indeksa i eksponenata se sada može podesiti posebno od ostalih atributa fonta. (#10919)
* Zbog promena u aplikaciji VS Code, NVDA više neće onemogućiti režim pretraživanja u Code po podrazumevanim podešavanjima. (#10888)
* NVDA više ne izgovara "Vrh" i "Dno" kada se pregledni kursor direktno pomera na početak ili kraj  reda navigacionog objekta. (#9551)
* NVDA više ne izgovara "Levo" i "Desno" kada se pregledni kursor direktno pomera na prvi ili poslednji znak reda navigacionog objekta. (#9551)

### Ispravljene greške

* NVDA se sada ispravno pokreće kada datoteka sa dnevnikom ne može da se kreira. (#6330)
* U novijim verzijama aplikacije Microsoft Word 365, NVDA više neće izgovarati "obrisana reč u nazad" kada se pritisne ctrl plus backspace u toku uređivanja dokumenta. (#10851)
* U programu Winamp, NVDA će ponovo izgovarati menjanje statusa funkcija nasumične reprodukcije i ponavljanja. (#10945)
* NVDA više nije veoma spor kada se pomerate u listi stavki programa 1Password. (#10508)
* Windows OneCore sintetizator govora više nema duže pauze između izgovorenih rečenica. (#10721)
* NVDA više neće prestati sa radom kada otvorite kontekstni meni  za 1Password u sistemskoj traci za obaveštenja. (#11017)
* U  Office paketu 2013 i starijim verzijama:
  * Trake menija se izgovaraju kada se prvi put fokusirate na njih. (#4207)
  * Stavke kontekstnog menija se ponovo ispravno prijavljuju. (#9252)
  * Sekcije traka menija se ispravno prijavljuju kada se krećete kroz njih korišćenjem kombinacije ctrl plus strelice. (#7067)
* U režimu pretraživanja aplikacija Mozilla Firefox i Google Chrome, sadržaj se neće neispravno prikazivati na posebnim redovima kada web autori koriste CSS display: inline-flex. (#11075)
* U režimu pretraživanja sa onemogućenom opcijom  automatsko postavljanje fokusa na elemente koji se mogu fokusirati, moguće je aktivirati elemente koji se ne mogu fokusirati.
* U režimu pretraživanja sa onemogućenom opcijom  automatsko postavljanje fokusa na elemente koji se mogu fokusirati, moguće je aktivirati elemente do kojih se dolazi tasterom tab. (#8528)
* U režimu pretraživanja sa onemogućenom opcijom  automatsko postavljanje fokusa na elemente koji se mogu fokusirati, aktiviranje određenih elemenata više neće izazivati klik na neispravnoj lokaciji. (#9886)
* NVDA neće više reprodukovati zvukove za grešku kada se pristupa tekstualnim DevExpress kontrolama. (#10918)
* Opisi alata za ikonice na sistemskoj traci se više ne izgovaraju u toku navigacije ako je njihovo ime jednako imenu ikonice, kako bi se izbeglo dvostruko izgovaranje. (#6656)
* U režimu pretraživanja sa onemogućenom opcijom "Automatsko postavljanje fokusa na elemente koji se mogu fokusirati", prebacivanje u režim fokusiranja komandom NVDA plus razmak fokusira element na poziciji kursora. (#11206)
* Ponovo je moguće da proverite nova NVDA ažuriranja na nekim sistemima gde ovo nije ispravno radilo; na primer nove Windows instalacije. (#11253)
* Fokus u Java aplikacijama se neće menjati kada se izbor promeni u tabelama, listama ili prikazima stabla koji nisu fokusirani. (#5989)

### Promene za programere (engleski)

* execElevated and hasUiAccess have moved from config module to systemUtils module. Usage via config module is deprecated. (#10493)
* Updated configobj to 5.1.0dev commit f9a265c4. (#10939)
* Automated testing of NVDA with Chrome and a HTML sample is now possible. (#10553)
* IAccessibleHandler has been converted into a package, OrderedWinEventLimiter has been extracted to a module and unit tests added (#10934)
* Updated BrlApi to version 0.8 (BRLTTY 6.1). (#11065)
* Status bar retrieval may now be customized by an AppModule. (#2125, #4640)
* NVDA no longer listens for IAccessible EVENT_OBJECT_REORDER. (#11076)
* A broken ScriptableObject (such as a GlobalPlugin missing a call to its base class' init method) no longer breaks NVDA's script handling. (#5446)

## 2020.1

Glavne karakteristike ove verzije uključuju podršku za nove brajeve redove proizvođača HumanWare i APH, kao i puno drugih važnih ispravljenih grešaka kao što su mogućnost čitanja matematičkih izraza u programu Microsoft Word korišćenjem programa MathPlayer / MathType.

### Nove karakteristike

* Trenutno izabrana stavka liste se ponovo izgovara u režimu pretraživanja programa Chrome, slično kao u verziji NVDA 2019.1. (#10713)
* Sada možete da izvršite desni klik miša ekranom osetljivim na dodir tako što jednim prstom dodirnete i zadržite. (#3886)
* Podrška za nove brajeve redove: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, i NLS eReader. (#10830)

### Promene

* NVDA će sprečiti sistem da se zaključa ili ode u stanje spavanja u režimu izgovori sve. (#10643)
* Podrška za okvire van procesa u programu Mozilla Firefox. (#10707)
* Ažuriran liblouis brajev prevodilac na verziju 3.12. (#10161)

### Ispravljene greške

* Unikodni simbol za minus se sada ponovo izgovara (U+2212) (#10633)
* Kada se instalira dodatak iz menadžera dodataka, imena datoteka i foldera u prozoru za pretragu se više ne izgovaraju dva puta. (#10620, #2395)
* U programu Firefox, kada se učitava sajt Mastodon sa omogućenim naprednim Web interfejsom, sve vremenske linije se ispravno učitavaju u režimu pretraživanja. (#10776)
* U režimu pretraživanja, NVDA sada ispravno prijavljuje "Nije označeno" za izborna polja koja nisu označena u situacijama u kojima se ovo nije izgovaralo. (#10781)
* ARIA kontrole za prekidače Eng. Switch više ne prijavljuju zbunjujuće informacije kao što su "nije pritisnuto označeno" ili "pritisnuto označeno". (#9187)
* SAPI4 glasovi više nebi trebalo da odbijaju da izgovaraju određene tekstove. (#10792)
* NVDA ponovo može da čita i vrši interakciju sa matematičkim izrazima u programu Microsoft Word. (#10803)
* NVDA će ponovo izgovoriti tekst koji više nije označen u režimu pretraživanja ako se pritisne neka od strelica nakon što se tekst označi. (#10731).
* NVDA se više neće zatvarati ako je došlo do greške u inicijalizaciji sintetizatora eSpeak. (#10607)
* Greške u prečicama koje su izazvane unikodnim prevodima više ne zaustavljaju instalaciju, ovo se rešava tako što se tekst prečica vraća na Engleski. (#5166, #6326)
* Izlazak ili pomeranje iz liste i tabele u režimu pretraživanja  uz opciju izgovori sve i površno čitanje više neće neprekidno izgovarati izlazak iz tabele i liste. (#10706)
* Ispravljeno praćenje miša za neke MSHTML elemente u  programu Internet Explorer. (#10736)

### Promene za programere (engleski)

* Developer documentation is now build using sphinx. (#9840)
* Several speech functions have been split into two. (#10593)
  The speakX version remains, but now depends on a getXSpeech function which returns a speech sequence.
  * speakObjectProperties now relies on getObjectPropertiesSpeech
  * speakObject now relies on getObjectSpeech
  * speakTextInfo now relies on getTextInfoSpeech
  * speakWithoutPauses has been converted into a class, and refactored, but should not break compatibility.
  * getSpeechForSpelling is deprecated (though still available) use getSpellingSpeech instead.
  Private changes that should not affect addon developers:
  * _speakPlaceholderIfEmpty is now _getPlaceholderSpeechIfTextEmpty
  * _speakTextInfo_addMath is now _extendSpeechSequence_addMathForTextInfo
* Speech 'reason' has been converted to an Enum, see controlTypes.OutputReason class. (#10703)
  * Module level 'REASON_*' constants are deprecated.
* Compiling NVDA dependencies now requires Visual Studio 2019 (16.2 or newer). (#10169)
* Updated SCons to version 3.1.1. (#10169)
* Again allow behaviors._FakeTableCell to have no location defined (#10864)

## 2019.3

NVDA 2019.3 je veoma značajno ažuriranje koje uključuje puno promena u strukturi kao što su prelazak sa Python 2 na Python 3, kao i nove mogućnosti u kodu za govor programa NVDA.
Iako ove promene izazivaju nekompatibilnosti starijih NVDA dodataka, ažuriranje na Python 3 je neophodno zbog bolje bezbednosti, a promene u govoru dozvoljavaju vrlo uzbudljive inovacije u bliskoj budućnosti.
 Druge prednosti ove verzije uključuju podršku za 64 bitne Java aplikacije, funkcije zatamnjivanja ekrana i označavanja fokusa, podršku za nove brajeve redove i novi preglednik brajevog reda, i puno drugih ispravljenih grešaka.

### Nove karakteristike

* Preciznost komande postavi miš na navigacioni objekat je značajno poboljšana u tekstualnim poljima u Java aplikacijama. (#10157)
* Dodata podrška za sledeće  Handy Tech brajeve redove (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Sve korisnički definisane komande se sada mogu ukloniti korišćenjem novog dugmeta "vrati na fabričke vrednosti"  u dijalogu ulazne komande. (#10293)
* Prijavljivanje fonta u aplikaciji Microsoft Word sada uključuje da li je tekst označen kao skriven. (#8713)
* Dodata komanda za premeštanje preglednog kursora na poziciju koja je prethodno označena za izbor ili kopiranje: NVDA+šift+F9. (#1969)
* U  programima Internet Explorer, Microsoft Edge i novijim verzijama pretraživača Firefox i Chrome, orjentiri se sada prijavljuju u režimu fokusiranja i objektnoj navigaciji. (#10101)
* U programima Internet Explorer, Google Chrome i Mozilla Firefox, možete se kretati kroz članke ili grupisanja korišćenjem komandi brze navigacije. Ove komande su podrazumevano nedodeljene i može im se dodeliti prečica ako se dijalog ulazne komande otvori kada ste u dokumentu režima pretraživanja. (#9485, #9227)
 * Figure se takođe prijavljuju. One se smatraju objektima i samim tim se koristi slovo o za kretanje kroz njih.
* U programima Internet Explorer, Google Chrome i Mozilla Firefox, elementi označeni kao  članak se sada prijavljuju u objektnoj navigaciji i režimu fokusiranja, i u režimu pretraživanja ako su uključeni u podešavanjima formatiranja dokumenta. (#10424)
* Dodato zatamnjivanje ekrana, koje kada je omogućeno, čini da ceo ekran bude crn na Windowsu 8 i novijim. (#7857)
 * Dodata komanda da se omogući zatamnjen ekran (do sledećeg ponovnog pokretanja kada se pritisne jednom, ili uvek dok je NVDA pokrenut ako se pritisne dva puta), nijedna prečica nije podrazumevano podešena.
 * može se omogućiti i podesiti u novoj 'vid' kategoriji u dijalogu NVDA podešavanja.
* Dodata funkcija oznake ekrana u program NVDA. (#971, #9064)
 * Označavanje fokusa, navigacionog objekta, i kursora režima pretraživanja može se omogućiti i podesiti u kategoriji "vid" u dijalogu za NVDA podešavanja.
 * Napomena: Ova opcija nije kompatibilna sa dodatkom  focus highlight, ali, dodatak se može koristiti dok je ugrađena funkcija onemogućena.
* Dodat alat za pregled brajevog reda, dozvoljava pregled teksta brajevog reda putem prozora na ekranu. (#7788)

### Promene

* Korisničko uputstvo sada opisuje kako da koristite NVDA u Windows konzoli. (#9957)
* Pokretanje  nvda.exe sada podrazumevano menja već pokrenutu kopiju programa NVDA. -r|--replace parametar komandne linije se i dalje prihvata, ali  se ignoriše. (#8320)
* Na Windowsu 8 i novijim, NVDA će prijaviti ime proizvoda i verziju za aplikacije iz Microsoft prodavnice korišćenjem informacija koje pruža aplikacija. (#4259, #10108)
* Kada se uključuje ili isključuje praćenje izmena u programu  Microsoft Word, NVDA će izgovoriti stanje podešavanja. (#942) 
* Broj NVDA verzije se sada evidentira kao prva poruka u dnevniku. Ovo se dešava čak iako je evidentiranje onemogućeno u interfejsu. (#9803)
* Dijalog za podešavanja više ne dozvoljava menjanje nivoa evidentiranja u dnevniku ako je promenjen iz komandne linije. (#10209)
* U programu Microsoft Word, NVDA sada izgovara stanje prikaza znakova koji se štampaju kada koristite prečicu za menjanje statusa Ctrl+šift+8 . (#10241)
* Ažuriran Liblouis brajev prevodilac na commit 58d67e63. (#10094)
* Kada je omogućeno prijavljivanje CLDR znakova (što uključuje emoji), izgovaraju se u svim nivoima izgovora interpunkcije. (#8826)
* Paketi drugih proizvođača koji su uključeni u NVDA, kao što su comtypes, sada evidentiraju svoja upozorenja i greške u NVDA dnevniku. (#10393)
* Ažurirana baza Unicode znakova i emoji znakova na verziju  36.0. (#10426)
* Kada se fokusira grupisanje u režimu pretraživanja, opis se sada takođe čita. (#10095)
* Java Access Bridge se sada uključuje uz NVDA kako bi se omogućio pristup Java aplikacijama, uključujući 64 bitne java aplikacije. (#7724)
* Ako Java Access Bridge nije omogućen za korisnika, NVDA će ga automatski omogućiti pri pokretanju. (#7952)
* Ažuriran eSpeak-NG na 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Ispravljene greške

* Emoji i drugi 32 bit unicode znakovi sada zauzimaju manje mesta na brajevom redu kada se prikazuju  kao heksadecimalne vrednosti. (#6695)
* U Windowsu 10, NVDA će izgovarati opise alata u univerzalnim aplikacijama ako je podešen da prijavi opise alata u dijalogu predstavljanje objekata. (#8118)
* U Windowsu 10 Anniversary ažuriranju i novijim, ukucan tekst se sada prijavljuje u aplikaciji Mintty. (#1348)
* Na Windowsu 10 Anniversary ažuriranje i novijim, izlazni tekst iz konzole koji se pojavljuje blizu kursora se više neće sricati. (#513)
* Kontrole u Audacity dijalogu za kompresovanje se sada izgovaraju u toku navigacije. (#10103)
* NVDA više neće smatrati razmake novim rečima u Scintilla uređivačima kao što je  Notepad++. (#8295)
* NVDA će sprečiti sistem da uđe u režim spavanja kada se tekst pomera komandama na brajevom redu. (#9175)
* Na Windowsu 10, brajev red će sada ispravno pratiti uređivanje ćelija u programu Microsoft Excel i drugim UIA tekstualnim kontrolama gde je često kasnio. (#9749)
* NVDA će ponovo prijavljivati predloge u adresnoj traci programa  Microsoft Edge. (#7554)
* NVDA više neće prestati sa govorom kada se fokusira HTML zaglavlje kontrola kartica u programu Internet explorer. (#8898)
* U programu Microsoft Edge baziranom na tehnologiji EdgeHTML, NVDA više neće reprodukovati zvuk predloga za pretraživanje kada se prozor uveća. (#9110, #10002)
* ARIA 1.1 izborni okviri su sada podržani u pretraživačima Mozilla Firefox i Google Chrome. (#9616)
* NVDA više neće prijavljivati vizuelno skriven sadržaj u kolonama za stavke liste u kontrolama SysListView32. (#8268)
* Dijalog za podešavanja više ne prikazuje "info" kao trenutni nivo evidentiranja u dnevniku kada ste na sigurnim ekranima. (#10209)
* U start meniju Windowsa 10 Anniversary ažuriranje i novijim, NVDA će izgovarati detalje rezultata pretrage. (#10340)
* U režimu pretraživanja, ako pomeranje kursora ili korišćenje brze navigacije izaziva promenu sadržaja, NVDA neće više neispravno izgovarati sadržaj u nekim slučajevima. (#8831, #10343)
* Neka imena nabrajanja u programu Microsoft Word su ispravljena. (#10399)
* U Windowsu 10 ažuriranje iz maja 2019 i novijim, NVDA će ponovo izgovarati prvu stavku istorije privremene memorije ili emoji panela kada se otvore. (#9204)
* U programu Poedit, ponovo je moguće videti neke prevode za jezike koji se pišu s desna na levo. (#9931)
* U aplikaciji za podešavanja Windowsa 10 ažuriranje iz aprila 2018 i novijim, NVDA više neće prijavljivati informacije o traci napredovanja za metar jačine u delu sistem/zvuk. (#10412)
* Neispravni regularni izrazi u govornim rečnicima neće više potpuno eliminisati NVDA govor. (#10334)
* Kada se čitaju stavke nabrajanja u programu Microsoft Word sa omogućenim UIA, nabrajanje iz sledeće liste se neće više neispravno izgovarati. (#9613)
* Neke retke greške u prevođenju brajevog pisma sa alatom liblouis su ispravljene. (#9982)
* Java aplikacije koje su pokrenute pre programa NVDA sada su pristupačne bez potrebe da ponovo pokrećete Java aplikaciju. (#10296)
* U programu Mozilla Firefox, kada fokusirani element postane označen kao trenutni (aria-current), ova promena se više ne izgovara više puta. (#8960)
* NVDA će sada smatrati određene unikodne znakove kao što su e-acute kao jedan znak kada se krećete kroz tekst. (#10550)
* Spring Tool Suite verzija 4 je sada podržana. (#10001)
* Sada se više neće dva puta izgovarati kada je aria-labelledby relation target   inner element. (#10552)
* Na Windowsu 10 verziji 1607 i novijim, ukucani znakovi sa brajeve tastature se izgovaraju u više situacija. (#10569)
* Kada se menja zvučni izlazni uređaj, tonovi koje NVDA reprodukuje će se reprodukovati na uređaju koji je izabran. (#2167)
* U programu Mozilla Firefox, pomeranje fokusa u režimu pretraživanja je brže. Ovo čini pomeranje kursora u režimu pretraživanja brže u više slučajeva. (#10584)

### Promene za programere (engleski)

* Updated Python to 3.7. (#7105)
* Updated pySerial to version 3.4. (#8815)
* Updated wxPython to 4.0.3 to support Python 3.5 and later. (#9630)
* Updated six to version 1.12.0. (#9630)
* Updated py2exe to version 0.9.3.2 (in development, commit b372a8e from albertosottile/py2exe#13). (#9856)
* Updated UIAutomationCore.dll comtypes module to version 10.0.18362. (#9829)
* The tab-completion in the Python console only suggests attributes starting with an underscore if the underscore is first typed. (#9918)
* Flake8 linting tool has been integrated with SCons reflecting code requirements for Pull Requests. (#5918)
* As NVDA no longer depends on pyWin32, modules such as win32api and win32con are no longer available to add-ons. (#9639)
 * win32api calls can be replaced with direct calls to win32 dll functions via ctypes.
 * win32con constants should be defined in your files.
* The "async" argument in nvwave.playWaveFile has been renamed to "asynchronous". (#8607)
* speakText and speakCharacter methods on synthDriver objects are no longer supported.
 * This functionality is handled by SynthDriver.speak.
* SynthSetting classes in synthDriverHandler have been removed. Now use driverHandler.DriverSetting classes instead.
* SynthDriver classes should no longer expose index via the lastIndex property.
 * Instead, they should notify the synthDriverHandler.synthIndexReached action with the index, once all previous audio has finished playing before that index.
* SynthDriver classes must now notify the synthDriverHandler.synthDoneSpeaking action, once all audio from a SynthDriver.speak call has completed playing.
* SynthDriver classes must support the speech.PitchCommand in their speak method, as changes in pitch for speak spelling now depends on this functionality.
* The speech function getSpeechTextForProperties has been renamed to getPropertiesSpeech. (#10098)
* The braille function getBrailleTextForProperties has been renamed to getPropertiesBraille. (#10469)
* Several speech functions have been changed to return speech sequences. (#10098)
 * getControlFieldSpeech
 * getFormatFieldSpeech
 * getSpeechTextForProperties now called getPropertiesSpeech
 * getIndentationSpeech
 * getTableInfoSpeech
* Added a textUtils module to simplify string differences between Python 3 strings and Windows unicode strings. (#9545)
 * See the module documentation and textInfos.offsets module for example implementations.
* Deprecated functionality now removed. (#9548)
 * AppModules removed:
  * Windows XP sound recorder.
  * Klango Player, which is abandoned software.
 * configobj.validate wrapper removed.
  * New code should use from configobj import validate instead of import validate
 * textInfos.Point and textInfos.Rect replaced by locationHelper.Point and locationHelper.RectLTRB respectively.
 * braille.BrailleHandler._get_tether and braille.BrailleHandler.set_tether have been removed.
 * config.getConfigDirs has been removed.
 * config.ConfigManager.getConfigValidationParameter has been replaced by getConfigValidation
 * inputCore.InputGesture.logIdentifier property has been removed.
   * Use _get_identifiers in inputCore.InputGesture instead.
 * synthDriverHandler.SynthDriver.speakText/speakCharacter have been removed.
 * Removed several synthDriverHandler.SynthSetting classes.
   * Previously kept for backwards compatibility (#8214), now considered obsolete.
   * Drivers that used the SynthSetting classes should be updated to use the DriverSetting classes.
 * Some legacy code has been removed, particularly:
  * Support for the Outlook pre 2003 message list.
  * An overlay class for the classic start menu, only found in Windows Vista and earlier.
  * Dropped support for Skype 7, as it is definitely not working any more.
* Added a framework to create vision enhancement providers; modules that can change screen contents, optionally based on input from NVDA about object locations. (#9064)
 * Add-ons can bundle their own providers in a visionEnhancementProviders folder.
 * See the vision and visionEnhancementProviders modules for the implementation of the framework and examples, respectively.
 * Vision enhancement providers are enabled and configured via the 'vision' category in NVDA's settings dialog.
* Abstract class properties are now supported on objects that inherit from baseObject.AutoPropertyObject (e.g. NVDAObjects and TextInfos). (#10102)
* Introduced displayModel.UNIT_DISPLAYCHUNK as a textInfos unit constant specific to DisplayModelTextInfo. (#10165)
 * This new constant allows walking over the text in a DisplayModelTextInfo in a way that more closely resembles how the text chunks are saved in the underlying model.
* displayModel.getCaretRect now returns an instance of locationHelper.RectLTRB. (#10233)
* The UNIT_CONTROLFIELD and UNIT_FORMATFIELD constants have been moved from virtualBuffers.VirtualBufferTextInfo to the textInfos package. (#10396)
* For every entry in the NVDA log, information about the originating thread is now included. (#10259)
* UIA TextInfo objects can now be moved/expanded by the page, story and formatField text units. (#10396)
* External modules (appModules and globalPlugins) are now less likely to be able to break the creation of NVDAObjects. 
 * Exceptions caused by the "chooseNVDAObjectOverlayClasses" and "event_NVDAObject_init" methods are now properly caught and logged.
* The aria.htmlNodeNameToAriaLandmarkRoles dictionary has been renamed to aria.htmlNodeNameToAriaRoles. It now also contains roles that aren't landmarks.
* scriptHandler.isCurrentScript has been removed due to lack of use. There is no replacement. (#8677)

## 2019.2.1

Ovo je manje ažuriranje kako bi se ispravile neke nestabilnosti u verziji 2019.2. Ispravke uključuju:

* Windows Explorer na  Windowsu 7 se više ne ruši kada se pristupa  poljima sa detaljima o podacima. (#5337) 
* U  Windowsu 7, NVDA više neće izazvati rušenje Windows Explorera kada se miš koristi u start meniju. (#9435) 
* Ispravljeno nekoliko grešaka u Gmailu u pretraživačima Firefox i Chrome prilikom interakcije sa određenim iskačujućim menijima, na primer menjanje filtera ili nekih Gmail podešavanja. (#10175, #9402, #8924)
* NVDA više neće prestajati sa radom kada pristupate slikama  sa base64 URI u aplikaciji Mozilla Firefox ili Google Chrome. (#10227)

## 2019.2

Glavne karakteristike ove verzije uključuju automatsko prepoznavanje brajevih redova kompanije Freedom Scientific , eksperimentalno podešavanje u naprednim podešavanjima koje zaustavlja pomeranje sistemskog fokusa u režimu pretraživanja (što može doneti ubrzanja u radu ), opcija povećanja brzine za Windows OneCore sintetizator kako bi se dostigao veoma brz govor, i puno drugih ispravljenih grešaka.

### Nove karakteristike

* Podrška za program Miranda NG radi sa novijim verzijama klijenta. (#9053) 
* Sada možete onemogućiti režim pretraživanja onemogućavanjem nove opcije "Omogući režim pretraživanja kada se stranica učita" u podešavanjima režima pretraživanja programa NVDA. (#8716) 
 * Napomena da kada je ova opcija onemogućena, možete ručno omogućiti režim pretraživanja komandom NVDA plus razmak.
* Sada možete filtrirati simbole u dijalogu za izgovor znakova interpunkcije i simbola, što radi slično filtriranju u dijalozima za listu elemenata ili ulazne komande. (#5761)
* Nova komanda je dodata za menjanje jedinice rezolucije teksta (koliko teksta će biti pročitano kada se miš pomera), ona nema podrazumevanu prečicu. (#9056)
* windows OneCore sintetizator govora sada ima opciju povećanja brzine, koja dozvoljava znatno brži govor. (#7498)
* Opcija povećanja brzine se sada može podesiti iz kruga menjanja podešavanja sintetizatora za sve podržane sintetizatore. (Trenutno eSpeak-NG i  Windows OneCore). (#8934)
* Profili podešavanja se sada mogu ručno aktivirati prečicama. (#4209)
 * Prečica se mora podesiti u dijalogu "ulazne komande".
* U programu  Eclipse, dodata podrška za automatsko dopunjavanje u uređivaču koda. (#5667)
 * Takođe, Javadoc informacije se mogu pročitati iz uređivača kada su dostupne korišćenjem komande NVDA+d.
* Dodata eksperimentalna opcija u panel naprednih podešavanja koja sprečava da sistemski fokus prati kursor u režimu pretraživanja   (automatski postavi sistemski fokus na elemente koji se mogu fokusirati). (#2039) 
 * Iako možda ovo nije odgovarajuća opcija za sve sajtove, ovo može popraviti sledeće probleme: 
 * Efekat vraćanja fokusa: NVDA ponekad poništava poslednju prečicu režima pretraživanja vraćanjem na prethodnu lokaciju.
 * Polja za unos preuzimaju sistemski fokus kada se krećete strelicama na nekim sajtovima.
 * Prečice režima pretraživanja sporo odgovaraju.
* Za podržane brajeve redove, podešavanja drajvera se mogu promeniti iz kategorije brajevih podešavanja dijaloga NVDA podešavanja. (#7452)
* Brajevi redovi kompanije Freedom Scientific su sada podržani od strane automatskog prepoznavanja brajevih redova. (#7727)
* Dodata komanda za prikazivanje izgovorene zamene za simbol na trenutnoj poziciji preglednog kursora. (#9286)
* Dodata eksperimentalna opcija u panel sa naprednim podešavanjima koja vam  dozvoljava da probate novu, napisanu iz početka NVDA podršku za Windows konzole korišćenjem Microsoft UI Automation API-a. (#9614)
* U Python konzoli, polje za unos sada podržava lepljenje više redova iz privremene memorije. (#9776)

### Promene

* Jačina sintetizatora se sada smanjuje za 5 umesto 10 procenata kada se koristi krug sintetizatora. (#6754)
* Pojašnjen tekst u upravljaču dodataka kada je NVDA pokrenut uz opciju --disable-addons. (#9473)
* Ažurirani Emoji   znakovi iz baze Unicode Common Locale  na verziju  35.0. (#9445)
* Kada je automatski prepoznat brajev red povezan putem  Bluetooth veze, NVDA će nastaviti pretragu za USB redove podržane od strane istog drajvera i prebaciće se na USB vezu ako postane dostupna. (#8853)
* Ažuriran  eSpeak-NG na verziju 67324cc.
* Updated liblouis braille translator to version 3.10.0. (#9439, #9678)
* NVDA će sada izgovoriti reč 'izabrano' nakon izgovaranja teksta koji je korisnik izabrao. (#9028, #9909)
* U programu Microsoft Visual Studio Code, NVDA će podrazumevano biti u režimu fokusiranja. (#9828)

### Ispravljene greške

* NVDA se više ne ruši kada je folder dodatka prazan. (#7686)
* LTR i  RTL znakovi se više ne izgovaraju u toku navigacije slovo po slovo ili prikazuju na brajevom redu kada  se pristupa prozoru  za svojstva. (#8361)
* Kada skačete po poljima za unos u brzoj navigaciji režima pretraživanja, celo polje za unos se izgovara umesto izgovaranja samo prvog reda. (#9388)
* NVDA neće više gubiti govor nakon izlaska iz Windows 10 Mail aplikacije. (#9341)
* NVDA više neće imati grešku u pokretanju kada su regionalna podešavanja podešena na region nepoznat za NVDA, kao što je Engleski (Holandija). (#8726)
* Kada je režim pretraživanja omogućen u programu  Microsoft Excel i prebacite se na pretraživač u režimu fokusiranja i obrnuto, stanje režima pretraživanja se sada ispravno prijavljuje. (#8846)
* NVDA sada ispravno prijavljuje red ispod miša u programu Notepad++ i drugim uređivačima bazirani na tehnologiji Scintilla. (#5450)
* U Web aplikaciji Google Docs (i drugim Web uređivačima), brajev red neće više neispravno prikazivati "lst end" pre kursora u sredini stavke liste. (#9477)
* U Windows 10 ažuriranju iz maja 2019, NVDA više neće izgovarati puno obaveštenja o menjanju jačine hardverskim tasterima ako istraživač datoteka ima fokus. (#9466)
* Učitavanje dijaloga za izgovor simbola i znakova interpunkcije je sada znatno brže ako se koriste rečnici sa preko 1000 unosa. (#8790)
* U  Scintilla kontrolama kao što je Notepad++, NVDA može da pročita ispravan red kada je odvajanje reči uključeno. (#9424)
* U programu  Microsoft Excel, lokacija ćelije se izgovara nakon što se promeni komandom šift enter ili šift numeričko enter. (#9499)
* U programu  Visual Studio 2017 i novijim, u prozoru istraživača objekata, izabran objekat u stablu objekata ili izabrana kategorija se sada ispravno prijavljuje. (#9311)
* Dodaci čija se imena razlikuju samo u veličini slova više neće biti posmatrani kao posebni dodaci. (#9334)
* Za  Windows OneCore Glasove, brzina koja je podešena u programu NVDA više nije određena brzinom podešenom u Windows 10 podešavanjima govora. (#7498)
* Dnevnik se sada može otvoriti prečicom NVDA+F1 kada nema informacija za programere o trenutnom navigacionom objektu. (#8613)
* Ponovo je moguće koristiti komande za kretanje kroz tabele u  Google Docs, u programima Firefox i Chrome. (#9494)
* Bumper tasteri sada rade ispravno na Freedom Scientific brajevim redovima. (#8849)
* Kada se čita prvi znak dokumenta u programu Notepad++ 7.7 X64, NVDA više ne prestaje sa radom do 10 sekundi. (#9609)
* HTCom se može koristiti sa Handy Tech brajevim redom u kombinaciji sa NVDA. (#9691)
* U programu  Mozilla Firefox, ažuriranja za live region se više ne prijavljuju ako je live region u kartici koja je u pozadini. (#1318)
* NVDA dijalog za pretragu u režimu pretraživanja više neće neispravno funkcionisati ako je dijalog o programu NVDA otvoren u pozadini. (#8566)

### Promene za programere (engleski)

* You can now set the "disableBrowseModeByDefault" property on app modules to leave browse mode off by default. (#8846)
* The extended window style of a window is now exposed using the `extendedWindowStyle` property on Window objects and their derivatives. (#9136)
* Updated comtypes package to 1.1.7. (#9440, #8522)
* When using the report module info command, the order of information has changed to present the module first. (#7338)
* Added an example to demonstrate using nvdaControllerClient.dll from C#. (#9600)
* Added a new isWin10 function to the winVersion module which returns whether or not this copy of NVDA is running on (at least) the supplied release version of Windows 10 (such as 1903). (#9761)
* The NVDA Python console now  contains more useful modules in its namespace (such as appModules, globalPlugins, config and textInfos). (#9789)
* The result of the last executed command in the NVDA Python console is now accessible from the _ (line) variable. (#9782)
 * Note that this shadows the gettext translation function also called "_". To access the translation function: del _

## 2019.1.1

Ova manja verzija ispravlja sledeće greške:

* NVDA više ne izaziva rušenje programa Excel 2007 ili odbija da prijavi da li ćelija ima formule. (#9431)
* Google Chrome se više ne ruši prilikom interakcije sa određenim listama. (#9364)
* Greška je ispravljena koja je sprečavala kopiranje korisničkih podešavanja u profil sistemskih podešavanja. (#9448)
* U programu Microsoft Excel, NVDA ponovo koristi prevedenu poruku kada prijavljuje lokacije spojenih ćelija. (#9471)

## 2019.1

Glavne karakteristike ove verzije uključuju poboljšanja u brzini kada koristite programe Microsoft word i Excel, poboljšanja u stabilnosti i sigurnosti kao što su podrška za dodatke koji mogu označiti informacije o kompatibilnosti sa različitim verzijama programa NVDA, i brojne druge ispravljene greške.

Molimo imajte na umu da od ove verzije programa NVDA, prilagođeni moduli za aplikacije (eng. AppModules), globalni dodaci (ENG. GlobalPlugins), drajveri za brajeve redove (ENG. Braille display drivers) i  drajveri za sintetizatore (ENG. Synth drivers) neće biti automatski učitani iz vašeg foldera sa podešavanjima. 
Umesto toga oni se trebaju instalirati kao NVDA dodatak. Za one koji programiraju kod za NVDA dodatak, kod za njih se može kopirati u novi razvojni scratchpad folder u folderu sa korisničkim podešavanjima,  ako je razvojni scratchpad folder omogućen u novom panelu za napredna NVDA podešavanja.
Ove promene su neophodne kako bi se bolje osigurala kompatibilnost prilagođenog koda, kako nebi dolazilo do grešaka u programu NVDA kada ovaj kod postane nekompatibilan sa budućim NVDA verzijama.
Molimo pogledajte listu promena ispod kako biste videli kako dodaci mogu osigurati bolju kompatibilnost.

### Nove karakteristike

* Nove brajeve tabele: Afrikanski, Arapski osmotačkasti brajev kod, Arapski stepen 2, Španski stepen 2. (#4435, #9186)
* Dodata opcija u podešavanjima miša programa NVDA za situacije  u kojima je miš kontrolisan od strane druge aplikacije. (#8452) 
 * Ovo će dozvoliti programu NVDA da prati miš kada kontrolišete sistem programima kao što su  TeamViewer.
* Dodat `--enable-start-on-logon` parametar komandne linije koji dozvoljava da podesite da li će tihe NVDA instalacije podesiti NVDA da se pokreće na Windows ekranu za prijavljivanje ili ne. Označite true da se pokreće pri prijavljivanju ili false da se ne pokreće pri prijavljivanju. Ako --enable-start-on-logon opcija uopšte nije određena onda će se NVDA podrazumevano pokretati pri prijavljivanju, osim ako je već podešen da se ne pokreće u prethodnoj instalaciji. (#8574)
* Moguće je onemogućiti karakteristike evidentiranja u dnevniku programa NVDA izborom opcije "onemogućeno" iz panela opštih podešavanja. (#8516)
* Postojanje formula u radnim listovima programa  LibreOffice i Apache OpenOffice se sada prijavljuje. (#860)
* U programima Mozilla Firefox i  Google Chrome, režim pretraživanja sada prijavljuje izabranu stavku u listama i prikazima stabla.
 * Ovo radi u Firefox verziji 66 i novijim.
 * Ovo ne radi za određene liste (HTML select controls) u programu Chrome.
* Početna podrška za aplikacije kao što su Mozilla Firefox na računarima sa ARM64 (na primer Qualcom Snapdragon) procesorima. (#9216)
* Nova kategorija za napredna podešavanja je dodata u NVDA panel sa podešavanjima, koja uključuje opciju za testiranje podrške u programu Microsoft Word korišćenjem Microsoft UI Automation API-a. (#9200)
* Dodata podrška za tabelu grafičkog prikaza u programu Windows upravljač diska (eng. Windows disk management). (#1486)
* Dodata podrška za Handy Tech Connect Braille i  Basic Braille 84. (#9249)

### Promene

* Ažuriran liblouis brajev prevodilac na verziju 3.8.0. (#9013)
* Autori dodataka sada mogu da označe minimalnu neophodnu verziju programa NVDA za korišćenje njihovih dodataka. NVDA će odbiti instalaciju ili učitavanje dodataka u kojima je minimalna verzija označena kao novija verzija od verzije koja se trenutno koristi. (#6275)
* Autori dodataka sada mogu označiti poslednju verziju programa NVDA sa kojom je njihov dodatak testiran. Ako je dodatak testiran uz verziju koja je starija od trenutne, NVDA će odbiti instalaciju ili učitavanje tog dodatka. (#6275)
* Ova verzija programa NVDA će dozvoliti učitavanje i instalaciju dodataka koji ne sadrže informacije o minimalnoj i poslednjoj testiranoj verziji, ali ažuriranje na buduće verzije programa NVDA (na primer 2019.2) može izazvati automatsko onemogućavanje ovih dodataka.
* Komanda za pomeranje miša na navigacioni objekat je sada dostupna za Microsoft Word kao i za UIA kontrole, posebno Microsoft Edge. (#7916, #8371)
* Prijavljivanje teksta ispod miša je poboljšano za Microsoft Edge i druge UIA aplikacije. (#8370)
* Kada se NVDA pokrene sa `--portable-path` parametrom komandne linije, upisana adresa se automatski popunjava kada pokušate da napravite prenosnu kopiju iz NVDA menija. (#8623)
* Ažurirana adresa za Norvešku brajevu tabelu kako bi se koristio standard iz 2015 godine. (#9170)
* Kada se krećete po pasusima (control+strelice gore ili dole) ili po ćelijama tabele (control+alt+strelice), postojanje pravopisnih grešaka se više neće prijavljivati, čak iako je NVDA podešen da ih automatski prijavi. Ovo je urađeno zbog toga što pasusi i ćelije u tabeli često mogu imati velik sadržaj, i računanje pravopisnih grešaka može izazivati usporavanja u nekim aplikacijama. (#9217)
* NVDA više ne učitava prilagođene module za aplikacije, globalne dodatke ili drajvere za brajeve redove i sintetizatore govora iz foldera korisničkih podešavanja. Ovaj kod se treba upakovati kao NVDA dodatak sa ispravnim informacijama o verziji, što će osigurati da nekompatibilan kod neće biti pokrenut sa trenutnom NVDA verzijom. (#9238)
 * Za programere koji žele da testiraju kod dok se razvija,  omogućite NVDA scratchpad folder iz napredne kategorije NVDA podešavanja, i kopirajte vaš kod u 'scratchpad' folder koji se nalazi u folderu korisničkih podešavanja kada je ova opcija omogućena.

### Ispravljene greške

* Kada koristite OneCore sintetizator govora na Windowsu 10 ažuriranje iz aprila 2018 i novijim, velike pauze se više ne ubacuju nakon izgovaranja. (#8985)
* Kada se krećete između znakova u tekstualnim kontrolama (na primer Notepad) ili režim pretraživanja, 32 bitni emoji znakovi koji sadrže 2  UTF-16 karaktera (kao što su ðŸ¤¦) će se ispravno čitati. (#8782)
* Poboljšan dijalog za potvrdu ponovnog pokretanja kada se promeni jezik interfejsa. Tekst i dugmad u dijalogu su jasniji i manje zbunjujući. (#6416)
* Ako drugi sintetizator ima grešku pri učitavanju, NVDA  će se vratiti na Windows OneCore na Windowsu 10, umesto na ESpeak. (#9025)
* Uklonjena stavka "dijalog dobrodošlice" iz NVDA menija kada ste na sigurnim ekranima. (#8520)
* Kada koristite tab ili brzu navigaciju u režimu pretraživanja, legende na kontrolama kartica se sada preciznije prijavljuju. (#709)
* NVDA će sada izgovarati promene u izboru za određene birače vremena, na primer u aplikaciji alarmi i sat u Windowsu 10. (#5231)
* U centru za obaveštenja Windowsa 10, NVDA će izgovarati promene statusa kada menjate brze akcije kao što su osvetljenje ili asistent fokusa. (#8954)
* U centru za obaveštenja Windowsa 10 ažuriranje iz oktobra 2018 i novijim, NVDA će prepoznati akciju za osvetljenje kao dugme umesto ranijeg prepoznavanja kao dugme prekidača. (#8845)
* NVDA će ponovo pratiti kursor i izgovarati obrisane znakove u poljima za unos pretrage ili pomeranja na određenu ćeliju u programu Microsoft Excel. (#9042)
* Ispravljena retka greška u režimu pretraživanja programa Firefox. (#9152)
* NVDA više ne greši u prijavljivanju fokusa za neke kontrole na traci programa Microsoft Office 2016 kada su skupljene.
* NVDA više ne greši u prijavljivanju predloženih kontakata kada pišete novu poruku u programu Outlook 2016. (#8502)
* Nekoliko poslednjih tastera za prebacivanje kursora na brajevim redovima  kompanije eurobraille sa 80 ćelija više ne pomeraju kursor na početak ili nekoliko znakova nakon početka brajevog reda. (#9160)
* Ispravljena navigacija kroz tabele u pregledu konverzacija programa Mozilla Thunderbird. (#8396)
* U programima Mozilla Firefox i Google Chrome, prebacivanje u režim fokusiranja ispravno radi za određene liste (u kojima se lista/stablo ne može fokusirati ali same stavke u njima mogu). (#3573, #9157)
* Režim pretraživanja se sada ispravno uključuje podrazumevano kada čitate poruke u  Outlooku 2016/365 ako koristite eksperimentalnu NVDA podršku za korišćenje "UI Automation" za čitanje Word dokumenata. (#9188)
* NVDA ima manju verovatnoću da prestane sa radom tako da je jedini način vraćanja da se odjavite iz vašeg trenutnog Windowsa. (#6291)
* U Windowsu 10 ažuriranje iz oktobra 2018 i novijim, kada otvarate istoriju privremene memorije u oblaku a privremena memorija je prazna, NVDA će izgovoriti status privremene memorije. (#9103)
* U Windowsu 10 ažuriranje iz oktobra 2018 i novijim, kada tražite emoji znakove iz panela sa emoji znakovima, NVDA će izgovoriti prvi rezultat pretrage. (#9105)
* NVDA više ne prestaje sa radom u glavnom prozoru programa Oracle VirtualBox  5.2 i novijim. (#9202)
* Odziv u programu Microsoft Word kada se krećete po redovima, pasusima ili po ćelijama tabele može biti znatno poboljšana u nekim dokumentima. Potsećamo da za najbolje performanse, potrebno je podesiti Word u draft prikaz komandom alt+w,e nakon otvaranja dokumenta. (#9217) 
* U programima Mozilla Firefox i Google Chrome, prazna upozorenja se više ne prijavljuju. (#5657)
* Ogromna poboljšanja  brzine kada koristite program Microsoft Excel, posebno kada radni list sadrži komentare. (#7348)
* Više nema potrebe da onemogućite uređivanje u ćelijama u Microsoft Excel podešavanjima da biste pristupili kontroli za uređivanje ćelije sa programom NVDA u Excel 2016/365. (#8146).
* Ispravljena greška u programu Firefox koja se nekada pojaljuje u navigaciji kroz regione, ako se koristi dodatak enhanced ARIA. (#8980)

### Promene za programere (engleski)

* NVDA can now  be built with all editions of Microsoft Visual Studio 2017 (not just the Community edition). (#8939)
* You can now include log output from liblouis into the NVDA log by setting the louis boolean flag in the debugLogging section of the NVDA configuration. (#4554)
* Add-on authors are now able to provide NVDA version compatibility information in add-on manifests. (#6275, #9055)
 * minimumNVDAVersion: The minimum required version of NVDA for an add-on to work properly.
 * lastTestedNVDAVersion: The last version of NVDA an add-on has been tested with.
* OffsetsTextInfo objects can now implement the _getBoundingRectFromOffset method to allow retrieval of bounding rectangles per characters instead of points. (#8572)
* Added a boundingRect property to TextInfo objects to retrieve the bounding rectangle of a range of text. (#8371)
* Properties and methods within classes can now be marked as abstract in NVDA. These classes will raise an error if instantiated. (#8294, #8652, #8658)
* NVDA can log the time since input when text is spoken, which helps in measuring perceived responsiveness. This can be enabled by setting the timeSinceInput setting to True in the debugLog section of the NVDA configuration. (#9167)

## 2018.4.1

Ova verzija ispravlja grešku pri pokretanju programa NVDA ako je jezik podešen na Aragoneski. (#9089)

## 2018.4

Glavne karakteristike ove verzije uključuju poboljšanja brzine u novijim verzijama programa Mozilla Firefox, izgovor Emoji znakova sa svim sintetizatorima, izgovor statusa odgovora/prosleđivanja poruke u programu Outlook, prijavljivanje pozicije kursora od ivice strane u Wordu, i puno ispravljenih grešaka.

### Nove karakteristike

* Nove brajeve tabele: Kineska(Kina, Mandarinski) stepen 1 i stepen 2. (#5553)
* Status odgovora/prosleđivanja  se sada prijavljuje  za mailove u listi poruka programa  Microsoft Outlook. (#6911)
* NVDA sada može da čita opise za Emoji znakove  kao i druge znakove koji su deo  Unicode Common Locale baze podataka. (#6523)
* U programu Microsoft Word, udaljenost kursora od leve ivice i vrha strane se sada može prijaviti  komandom NVDA+NumeričkiTasterZaBrisanje. (#1939)
* U aplikaciji  Google Sheets sa omogućenim brajevim režimom, NVDA više ne izgovara "izabrano" za svaku ćeliju kada se fokus pomera između ćelija. (#8879)
* Dodata podrška za programe Foxit Reader i  Foxit Phantom PDF (#8944)
* Dodata podrška za DBeaver alat za baze podataka. (#8905)

### Promene

* U dijalogu podešavanja tastature, izborna polja za izbor NVDA tastera su sada u listi, i više nisu prikazana kao posebno izborno polje za svaki taster.
* NVDA više neće prikazivati bespotrebne informacije kada se čita sat u sistemskoj traci na određenim verzijama Windowsa. (#4364)
* Ažuriran liblouis brajev prevodilac  na verziju 3.7.0. (#8697)
* Ažuriran  eSpeak-NG na verziju 919f3240cbb

### Ispravljene greške

* U programu Outlook 2016/365, kategorija i status zastave se prijavljuju za poruke. (#8603)
* Kada je NVDA podešen da koristi jezike kao što su Kirgijški, Mongolski ili Makedonski, više ne prikazuje dijalog pri pokretanju koji obaveštava da operativni sistem ne podržava trenutni jezik. (#8064)
* Pomeranje miša na navigacioni objekat će sada puno preciznije pomerati miš u režimu pretraživanja programa Mozilla Firefox, Google Chrome i Acrobat Reader DC. (#6460)
* Interakcija sa izbornim okvirima na Webu u programima Firefox, Chrome i Internet Explorer je poboljšana. (#8664)
* Ako je pokrenut na Japanskoj verziji Windowsa XP ili Vista, NVDA sada ispravno prikazuje upozorenje o sistemskim zahtevima. (#8771)
* Poboljšanja u brzini u programu Mozilla Firefox u toku navigacije velikih stranica sa puno dinamičkih promena. (#8678)
* Brajev red više ne prikazuje promene fonta ako su onemogućene u podešavanjima formatiranja dokumenta. (#7615)
* NVDA više ne greši u praćenju fokusa  u istraživaču datoteka  i drugim aplikacijama koje koriste UI Automation kada je neka druga aplikacija zauzeta (na primer obrada više zvučnih materijala). (#7345)
* U ARIA menijima na Webu, taster escape će biti prosleđen u meni i neće više isključivati režim fokusiranja. (#3215)
* U novom Gmail Web interfejsu, kada koristite brzu navigaciju unutar poruka tokom čitanja, celokupan tekst poruke se više ne prijavljuje nakon elementa na koji ste došli. (#8887)
* Nakon ažuriranja programa  NVDA, pretraživači kao što su Firefox i  google Chrome više neće prestajati sa radom, i režim pretraživanja bi trebalo da ispravno prati ažuriranja na svim učitanim Web stranicama. (#7641) 
* NVDA više ne izgovara klikabilno  više puta  u toku navigacije klikabilnog sadržaja u režimu pretraživanja. (#7430)
* Prečice na baum Vario 40 brajevim redovima  više neće imati problema sa pokretanjem. (#8894)
* U Web aplikaciji Google Slides sa programom Mozilla Firefox, NVDA više ne prijavljuje izabran tekst nakon fokusiranja na svaku kontrolu. (#8964)

### Promene za programere (engleski)

* gui.nvdaControls now contains two classes to create accessible lists with check boxes. (#7325)
 * CustomCheckListBox is an accessible subclass of wx.CheckListBox.
 * AutoWidthColumnCheckListCtrl adds accessible check boxes to an AutoWidthColumnListCtrl, which itself is based on wx.ListCtrl.
* If you need to make a wx widget accessible which isn't already, it is possible to do so by using an instance of gui.accPropServer.IAccPropServer_impl. (#7491)
 * See the implementation of gui.nvdaControls.ListCtrlAccPropServer for more info.
* Updated configobj to 5.1.0dev commit 5b5de48a. (#4470)
* The config.post_configProfileSwitch action now takes the optional prevConf keyword argument, allowing handlers to take action based on differences between configuration before and after the profile switch. (#8758)

## 2018.3.2

Ovo je manje ažuriranje koje ispravlja grešku u programu Google Chrome u toku navigacije tvitova na sajtu  [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Ovo je manje ažuriranje koje ispravlja  NVDA grešku koja izaziva da  32 bitne verzije programa Mozilla Firefox prestaju sa radom. (#8759)

## 2018.3

Glavne karakteristike ove verzije uključuju automatsko prepoznavanje puno brajevih redova, podrška za nove Windows 10 karakteristike uključujući Windows 10 panel za unos emotikona, i puno ispravljenih grešaka.

### Nove karakteristike

* NVDA će prijavljivati gramatičke greške kada su ispravno prikazane na Web stranicama u programu Mozilla Firefox. (#8280)
* Sadržaj koji je označen kao ubačen ili obrisan na Web stranicama se sada prijavljuje u programu  Google Chrome. (#8558)
* Dodata podržka za BrailleNote QT i  Apex BT scroll wheel kada se BrailleNote koristi kao brajev red sa programom NVDA. (#5992, #5993)
* Dodate skripte za prijavljivanje proteklog i ukupnog trajanja  trenutnog zapisa u programu Foobar2000. (#6596)
* Simbol za Mac komandni taster   (⌘) se sada izgovara kada se čitaju tekstovi sa bilo kojim sintetizatorom. (#8366)
* Prilagođeni elementi koji koriste aria-roledescription atribut su sada podržani u svim Web pretraživačima. (#8448)
* Nove brajeve tabele: Češki osmotačkasti, Centralni Kurdiški, Esperanto, Mađarski, Švedski osmotačkasti kompjuterski brajev kod. (#8226, #8437)
* Dodata podrška za automatsko prepoznavanje brajevih redova u pozadini. (#1271)
 * ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille i HumanWare BrailleNote i Brailliant BI/B redovi su trenutno podržani.
 * Možete omogućiti ovu opciju u dijalogu za izbor brajevog reda, izborom opcije automatski.
 * Molimo pogledajte dokumentaciju za dodatne detalje.
* Dodata podrška za različite moderne načine unosa u verzijama Windowsa 10. One uključuju panel emotikona (jesenje  Creators ažuriranje), diktiranje (jesenje creators ažuriranje), predlozi za unos teksta na hardverskoj tastaturi (aprilsko ažuriranje 2018), i privremena memorija u oblaku (oktobarsko ažuriranje 2018). (#7273)
* Sadržaj označen kao citat korišćenjem ARIA (role blockquote) je sada podržan u programu Mozilla Firefox 63. (#8577)

### Promene

* Lista jezika u dijalogu opštih podešavanja je sada sortirana po imenima jezika umesto po ISO 639 kodovima. (#7284)
* Dodate podrazumevane komande za alt šift tab i  windows tab za sve podržane Freedom Scientific brajeve redove. (#7387)
* Za ALVA BC680 i  protocol converter redove, moguće je odrediti različite funkcije za left i  right smart pad, thumb i  etouch tastere. (#8230)
* Za ALVA BC6 redove, kombinacija sp2+sp3 će sada izgovarati trenutni datum i vreme, a sp1+sp2 emulira taster Windows. (#8230)
* Korisnik će jednom biti upitan kada se NVDA pokrene  da li se slažu sa slanjem podataka o korišćenju kompaniji  NV Access kada se proveravaju ažuriranja. (#8217)
* Kada se proveravaju ažuriranja, ako je korisnik dozvolio slanje podataka o korišćenju, NVDA će poslati ime trenutnog sintetizatora i brajevog reda koji se trenutno koriste, kako bi pomogli u određivanju prioriteta za rad na njihovim drajverima. (#8217)
* Ažuriran  liblouis brajev prevodilac na verziju 3.6.0. (#8365)
* Ažurirana adresa za ispravnu Rusku  osmotačkastu brajevu tabelu. (#8446)
* Ažuriran  eSpeak-ng na 1.49.3dev commit 910f4c2. (#8561)

### Ispravljene greške

* Pristupačne oznake za kontrole u programu  Google Chrome se sada češće prijavljuju u režimu pretraživanja   kada se oznaka  ne pojavljuje kao deo sadržaja. (#4773)
* Obaveštenja su sada podržana u aplikaciji  Zoom. Na primer, ovo uključuje status mikrofona, i primljene poruke. (#7754)
* Menjanje predstavljanja sadržaja na brajevom redu u režimu pretraživanja više ne izaziva prestanak praćenja kursora. (#7741)
* ALVA BC680 brajevi redovi se sada ispravno inicializuju. (#8106)
* Po podrazumevanim podešavanjima, ALVA BC6 redovi više neće koristiti emulirane sistemske tastere kada se pritiskaju kombinacije sa tasterima sp2+sp3. (#8230)
* Taster sp2 na ALVA BC6 brajevom redu za emuliranje alt tastera sada radi ispravno. (#8360)
* NVDA više ne izgovara bespotrebne promene izgleda tastature. (#7383, #8419)
* Praćenje miša je sada puno preciznije u programu Notepad i drugim kontrolama za uređivanje teksta kada ste u dokumentu sa više od 65535 znakova. (#8397)
* NVDA će prepoznati više dijaloga u Windowsu 10 i drugim modernim aplikacijama. (#8405)
* Na Windows 10 oktobarskom ažuriranju 2018, Server 2019 i novijim verzijama, NVDA više ne greši u praćenju sistemskog fokusa kada neka aplikacija prestane sa radom ili  izbacuje previše događaja. (#7345, #8535)
* Korisnik sada dobija informaciju kada pokuša da pročita ili kopira praznu statusnu traku. (#7789)
* Ispravljena greška  kada izborni okvir koji "nije označen" nije ispravno izgovoren ako je kontrola ranije bila polovično označena. (#6946)
* U listi jezika opštih podešavanja programa NVDA, ime jezika za Burmese se ispravno prikazuje na Windowsu 7. (#8544)
* U programu  Microsoft Edge, NVDA će izgovarati obaveštenja kao što su dostupnost čitača i napredak učitavanja stranice. (#8423)
* Kada se nalazite na Web listi, NVDA će prijaviti njenu oznaku ako je Web autor odredio oznaku. (#7652)
* Kada ručno određujete funkcije za komande na brajevom redu, te komande se sada ispravno uvek prikazuju za taj red. Ranije, one su se prikazivale kao određene za trenutni brajev red. (#8108)
* 64-bitna verzija programa   Media Player Classic je sada podržana. (#6066)
* Nekoliko poboljšanja za podršku sa brajevim redom u programu  Microsoft Word sa UI Automation omogućenom:
 * Slično kao i u drugim višelinijskim poljima za uređivanje, kada se nalazite na početku dokumenta na brajevom redu, red se pomera tako da  je prvi znak dokumenta na  početku reda. (#8406)
 * Smanjena količina sadržaja  predstavljanja fokusa kada se fokusirate  na Word dokument. (#8407)
 * Prebacivanje kursora sada ispravno radi kada ste u listi u Word dokumentu. (#7971)
 * Novo ubačena nabrajanja /brojevi u Word dokumentu se sada ispravno izgovaraju i prikazuju na brajevom redu. (#7970)
* Na  Windowsu 10 1803 i novijim, moguće je instalirati dodatke ako je opcija "Koristi Unicode UTF-8 za podršku jezika širom sveta" omogućena. (#8599)
* ITunes 12.9 i novije verzije se  ponovo mogu koristiti. (#8744)

### Promene za programere (engleski)

* Added scriptHandler.script, which can function as a decorator for scripts on scriptable objects. (#6266)
* A system test framework has been introduced for NVDA. (#708)
* Some changes have been made to the hwPortUtils module: (#1271)
 * listUsbDevices now yields dictionaries with device information including hardwareID and devicePath.
 * Dictionaries yielded by listComPorts now also contain a usbID entry for COM ports with USB VID/PID information in their hardware ID.
* Updated wxPython to 4.0.3. (#7077)
* As NVDA now only supports Windows 7 SP1 and later, the key "minWindowsVersion" used to check if UIA should be enabled for a particular release of Windows has been removed. (#8422)
* You can now register to be notified about configuration saves/reset actions via new config.pre_configSave, config.post_configSave, config.pre_configReset, and config.post_configReset actions. (#7598)
 * config.pre_configSave is used to be notified when NVDA's configuration is about to be saved, and config.post_configSave is called after configuration has been saved.
 * config.pre_configReset and config.post_configReset includes a factory defaults flag to specify if settings are reloaded from disk (false) or reset to defaults (true).
* config.configProfileSwitch has been renamed to config.post_configProfileSwitch to reflect the fact that this action is called after profile switch takes place. (#7598)
* UI Automation interfaces updated to Windows 10 October 2018 Update and Server 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)

## 2018.2.1

Ova verzija sadrži ažurirane prevode zbog uklonjene karakteristike u poslednjem trenutku koja je izazvala probleme.

## 2018.2

Glavne karakteristike ove verzije uključuju podršku za tabele u programu Kindle za  PC, podrška za Humanware BrailleNote Touch i  BI14 brajeve redove, poboljšanja za Onecore i Sapi5 sintetizatore govora, poboljšanja u programu Microsoft Outlook i još puno toga.

### Nove karakteristike

* NVDA komande za navigaciju kroz tabele su  sada podržane u servisu  Google Docs (sa omogućenim brajevim režimom). (#7946)
* Dodata sposobnost čitanja i navigacije kroz tabele u programu Kindle za  PC. (#7977)
* Podrška za  BrailleNote touch i  Brailliant BI 14 brajeve redove putem USB i  bluetooth veze. (#6524)
* U Windows 10 jesenjem Creators ažuriranju i novijim, NVDA će  izgovarati obaveštenja u aplikacijama kao što su  kalkulator i  Windows prodavnica. (#8045)
* Nove tabele za brajev prevod: Litvanski osmotačkasti, Ukrajinski, Mongolski. (#7839)
* Kada ažurirate  NVDA, moguće je odložiti instalaciju ažuriranja za kasnije. (#4263) 
* Novi jezici: Mongolski, Švajcarski.
* Sada možete pritisnuti Kontrol, šift, alt, windows i  NVDA sa vaše brajeve tastature i kombinovati ih sa brajevim unosom (na primer kombinacijom Kontrol+s). (#7306) 
 * Možete podesiti ove tastere korišćenjem kategorije emulirani sistemski tasteri u dijalogu ulazne komande.
* Vraćena podrška za brajeve redove Handy Tech Braillino i  Modular (sa starijom verzijom softvera ). (#8016)
* Vreme i datum za podržane Handy Tech uređaje (na primer Active Braille i  Active Star) će sada automatski biti sinhronizovano sa programom  NVDA kada se razlikuje više od 5 sekundi. (#8016)
* Ulazna komanda se može dodeliti za deaktiviranje svih aktivatora profila podešavanja. (#4935)

### Promene

* Kolone statusa u upravljaču dodataka su promenjene kako bi označile da je dodatak  onemogućen ili omogućen umesto pokrenut i suspendovan. (#7929)
* Ažuriran liblouis brajev prevodilac  na verziju 3.5.0. (#7839)
* Litvanska brajeva tabela je preimenovana  u Litvanski šestotačkasti da bi se izbeglo mešanje sa novom osmotačkastom tabelom. (#7839)
* Francuske  (Kanadske) brajeve tabele stepen 1 i stepen 2 su uklonjene. Umesto toga, Francuska (unificirana) šestotačkasta i tabela stepena 2 će se koristiti. (#7839)
* Sekundarni tasteri za prebacivanje kursora na brajevim redovima  Alva BC6, EuroBraille i  Papenmeier  sada prijavljuju informacije o formatiranju teksta trenutne ćelije. (#7106)
* Brajeve tabele  koje podržavaju skraćen unos brajevog pisma će se automatski vratiti na standardan unos u slučajevima kada uređivanje nije moguće (na primer kod kontrola koje nemaju kursor ili u režimu pretraživanja). (#7306)
* NVDA sada izgovara manje suvišnih informacija kada napomena u kalendaru programa Outlook  važi za ceo dan. (#7949)
* Sva podešavanja programa NVDA se sada mogu pronaći u jednom dijalogu za podešavanja kada se ode u  NVDA meni-> Opcije-> podešavanja, i više nisu u puno posebnih dijaloga. (#7302)
* Podrazumevani sintetizator govora kada se NVDA pokrene na Windowsu 10 je sada oneCore i više to nije ESpeak. (#8176)

### Ispravljene greške

* NVDA sada ispravno čita fokusirane kontrole pri unosu informacija Microsoft naloga u podešavanjima nakon unosa Email adrese. (#7997)
* NVDA sada ispravno čita Web stranicu nakon vraćanja nazad u programu Microsoft Edge. (#7997)
* NVDA neće više neispravno izgovarati poslednji znak  windows 10 PIN koda za prijavu  dok se računar otključava. (#7908)
* Oznake za radio dugmiće i izborna polja u programima Chrome i  Firefox se više ne prijavljuju dva puta kada se koristi taster tab ili brza navigacija u režimu pretraživanja. (#7960)
* aria-current koji ima vrednost false će se sada izgovarati kao false  umesto  true (#7892).
* Windows Onecore drajver više nema greške kada  je podešen glas uklonjen. (#7999)
* Menjanje glasova u Windows Onecore sintetizatoru je sada puno brže. (#7999)
* Ispravljen pogrešan prikaz brajevog unosa za nekoliko brajevih tabela, uključujući velika slova u skraćenom unosu osmotačkaste Danske brajeve tabele. (#7526, #7693)
* NVDA sada može  prijaviti više vrsta nabrajanja u programu  Microsoft Word. (#6778)
* Dodata komanda za prijavljivanje formatiranja teksta ispod trenutne brajeve ćelije. (#7106)
* Pritiskanje komande za prijavljivanje formatiranja više ne pomera poziciju pregleda, pa s time pritiskanje komande više puta ne daje različite rezultate. (#7869)
* Brajev unos više ne dozvoljava unos skraćenog brajevog pisma u slučajevima u kojima to nije podržano (cele reči neće više biti poslane sistemu i neće raditi u režimu pretraživanja ). (#7306)
* Ispravljeni problemi sa povezivanjem redova Handy Tech Easy Braille i  Braille Wave. (#8016)
* Na  Windowsu 8 i novijim, NVDA više neće izgovarati "nepoznato" kada otvarate brzi meni (Windows+X) i kada  izaberete  neku od ponuđenih  opcija iz ovog menija. (#8137)
* Komande koje su posebne za model brajevog reda Hims  sada rade kao što je to objašnjeno u korisničkom vodiču. (#8096)
* NVDA će sada pokušati da popravi  sistemske greške u  COM registraciji koje često dovode do toga da programi kao što su Firefox i  Internet Explorer postanu nepristupačni i prijavljuju "nepoznato" od strane programa  NVDA. (#2807)
* Ispravljena greška u menadžeru zadataka  koja dovodi do toga da NVDA ne dozvoljava korisnicima da prikažu više detalja o određenim procesima. (#8147)
* Noviji Microsoft SAPI5 glasovi više ne usporavaju rad na kraju izgovora, što čini navigaciju dosta bržom sa ovim glasovima. (#8174)
* NVDA više ne prijavljuje (Oznake s leva na desno i  oznake s desna na levo ) na brajevom redu ili kada se izgovara slovo po slovo sat u Windows traci obaveštenja u novijim verzijama Windowsa. (#5729)
* Prepoznavanje tastera za pomeranje Hims Smart Beetle brajevih redova  ponovo radi ispravno. (#6086)
* U određenim tekstualnim kontrolama, posebno u  Delphi aplikacijama, informacije koje se pružaju o navigaciji i uređivanju su sada dosta preciznije. (#636, #8102)
* U Windowsu 10 verzija RS5, NVDA više ne prijavljuje suvišne informacije kada menjate aplikacije komandom alt+tab. (#8258)

### Promene za programere (engleski)

* The developer info for UIA objects now contains a list of the UIA patterns available. (#5712)
* App modules can now force certain windows to always use UIA by implementing the isGoodUIAWindow method. (#7961)
* The hidden boolean flag "outputPass1Only" in the braille section of the configuration has again been removed. Liblouis no longer supports pass 1 only output. (#7839)

## 2018.1.1

Ovo je posebna verzija programa NVDA koja ispravlja grešku u drajveru za Onecore Windows sintetizator govora, koji je zvučao kao da ima povećanu visinu i brzinu u Windows 10 Redstone 4 (1803). (#8082)  

## 2018.1

Glavne karakteristike ove verzije uključuju podršku za grafikone u programima  Microsoft word i  Powerpoint, podrška za nove brajeve redove: Eurobraille i Optelec pretvarač protokola, poboljšana podrška za Hims i Optelec brajeve redove, poboljšanja u brzini rada sa programom Mozilla Firefox 58 i novijim verzijama, i još puno toga.

### Nove karakteristike

* Sada je moguća interakcija sa grafikonima u programima Microsoft Word i  Microsoft Powerpoint, slično kao u postojećoj podršci u programu Microsoft Excel. (#7046)
 * U programu Microsoft Word:  Kada ste u režimu pretraživanja, postavite kursor na grafikon i pritisnite enter za interakciju.
 * U programu Microsoft Powerpoint dok uređujete slajd: Tasterom tab pronađite objekat grafikona, a zatim pritisnite Enter ili razmak za interakciju sa grafikonom.
 * Da zaustavite interakciju sa grafikonom, pritisnite taster escape.
* Novi jezik: Kirgijški.
* Dodata podrška za  VitalSource Bookshelf. (#7155)
* Dodata podrška za Optelec pretvarač protokola, uređaj koji vam dozvoljava da koristite Braille Voyager i  Satellite brajeve redove korišćenjem ALVA BC6 komunikacionog protokola. (#6731)
* Sada je moguće koristiti brajev unos na ALVA 640 Comfort brajevom redu. (#7733) 
 * Brajev unos programa NVDA se može koristiti sa ovim kao i drugim  BC6 redovima sa verzijom softvera  3.0.0 i novijom.
* Rana podrška za Google tabele sa omogućenim brajevim režimom. (#7935)
* Podrška za  Eurobraille Esys, Esytime i  Iris brajeve redove. (#7488)

### Promene

* Drajveri za HIMS Braille Sense/Braille EDGE/Smart Beetle i  Hims Sync su zamenjeni jednim drajverom. Novi drajver će automatski biti korišćen  za bivše syncBraille korisnike. (#7459) 
 * Neke komande, na primer komande za pomeranje, su promenjene kako bi pratile standarde koje Hims proizvodi koriste. Proverite korisničko uputstvo za više detalja.
* Kada pišete na tastaturi na ekranu korišćenjem ekrana osetljivog na dodir, po podrazumevanim podešavanjima morate pritisnuti svaki taster dva puta kao što biste aktivirali svaku drugu kontrolu na ekranu (#7309).
 * Da biste koristili stari način pisanja "unos tastera jednim dodirom" gde je jednostavno dovoljno podići prst sa slova za njegovu aktivaciju, omogućite ovu opciju u novom dijalogu interakcija sa ekranom osetljivim na dodir koji se nalazi u meniju podešavanja. (#7309)
* Nije više neophodno vezivati brajev red za fokus ili pregled, budući da će se ovo dešavati automatski po podrazumevanim podešavanjima. (#2385) 
 * Napomena da će do automatskog vezivanja za pregled doći samo kada koristite komande objektne navigacije ili preglednog kursora. Pomeranje brajevog reda neće aktivirati vezivanje za pregled.

### Ispravljene greške

* Poruke režima pretraživanja kao što su korišćenje komande NVDA+f dva puta za prikazivanje formatiranja više ne prikazuju grešku kada je NVDA instaliran u folderu koji sadrži znakove koji nisu ASCII. (#7474)
* Fokus se sada ponovo ispravno vraća kada se vratite u aplikaciju Spotify iz neke druge aplikacije. (#7689)
* Na Windows 10 jesenjem creators ažuriranju, NVDA više nema grešaka pri ažuriranju gde je omogućen kontrolisan pristup folderima iz sigurnosnog  centra Windows defendera. (#7696)
* Prepoznavanje komandi za pomeranje   Hims Smart Beetle brajevih redova više nije nestabilno. (#6086)
* Određena poboljšanja brzine pri učitavanju sadržaja u programu Mozilla Firefox 58 i novijim. (#7719)
* U programu Microsoft Outlook, čitanje Email poruka koje sadrže tabele više ne izaziva greške. (#6827)
* Komande brajevih redova koje simuliraju sistemske tastere  se sada mogu kombinovati sa drugim simuliranim sistemskim tasterima ako je jedna ili više komandi specifična za model. (#7783)
* U programu Mozilla Firefox, režim pretraživanja sada ispravno radi u iskačućim prozorima koje otvaraju dodaci kao što su LastPass i  bitwarden. (#7809)
* NVDA se više ne zaustavlja pri svakoj promeni fokusa ako su Firefox ili  Chrome prestali da reaguju na primer zbog greške. (#7818)
* U Twitter programima kao što su Chicken Nugget, NVDA više neće zanemariti poslednjih 20 znakova u tvitovima koji imaju 280 znakova pri čitanju. (#7828)
* NVDA sada koristi ispravan jezik pri izgovoru simbola u izboru teksta. (#7687)
* U novijim verzijama usluge  Office 365, ponovo je moguća navigacija kroz Excel grafikone korišćenjem strelica. (#7046)
* Kada se koristi govor ili brajev red, stanja kontrola će se uvek prijavljivati u istom redosledu, bez obzira da li su pozitivna ili negativna. (#7076)
* U aplikacijama kao što je  Windows 10 Mail, NVDA će uvek izgovarati obrisane znakove kada se pritisne Backspace. (#7456)
* Svi tasteri  na Hims Braille Sense Polaris redovima sada rade kako je predviđeno. (#7865)
* NVDA više nema problema sa pokretanjem na Windowsu 7 uz grešku o internoj  api-ms dll datoteci, kada je određena verzija Visual Studio 2017 redistributables instalirana od strane neke druge aplikacije. (#7975)

### Promene za programere (engleski)

* Added a hidden boolean flag to the braille section in the configuration: "outputPass1Only". (#7301, #7693, #7702) 
 * This flag defaults to true. If false, liblouis multi pass rules will be used for braille output.
* A new dictionary (braille.RENAMED_DRIVERS) has been added to allow for smooth transition for users using drivers that have been superseded by others. (#7459)
* Updated comtypes package to 1.1.3. (#7831)
* Implemented a generic system in braille.BrailleDisplayDriver to deal with displays which send confirmation/acknowledgement packets. See the handyTech braille display driver as an example. (#7590, #7721)
* A new "isAppX" variable in the config module can be used to detect if NVDA is running as a Windows Desktop Bridge Store app. (#7851)
* For document implementations such as NVDAObjects or browseMode that have a textInfo, there is now a new documentBase.documentWithTableNavigation class that can be inherited from to gain standard table navigation scripts. Please refer to this class to see which helper methods must be provided by your implementation for table navigation to work. (#7849)
* The scons batch file now better handles when  Python 3 is also installed, making use of the launcher to specifically launch python 2.7 32 bit. (#7541)
* hwIo.Hid now takes an additional parameter exclusive, which defaults to True. If set to False, other applications are allowed to communicate with a device while it is connected to NVDA. (#7859)

## 2017.4

Glavne karakteristike ove verzije uključuju puno ispravki za web podršku uključujući automatsko aktiviranje režima  pretraživanja za Web dijaloge, bolje prijavljivanje oznaka grupa za polja na Webu, Podrška za nove Windows 10 tehnologije kao što su Windows Defender zaštitnik aplikacija i Windows 10 na  ARM64, i automatsko prijavljivanje orijentacije ekrana i statusa baterije.  
Molimo imajte na umu da ova verzija programa  NVDA više ne podržava Windows XP ili  Windows Vista. Najmanja zahtevana verzija Windowsa za NVDA je sada windows 7 sa Service Packom 1.

### Nove karakteristike

* U režimu  pretraživanja, sada je moguće doći do kraja ili početka orjentira komandama za prelazak na početak ili kraj sadrživača (zarez/šift+zarez). (#5482)
* U programima Firefox, Internet explorer i Chrome, brza navigacija po poljima za uređivanje ili unos teksta sada uključuje obogaćena tekstualna polja označena kao contentEditable. (#5534)
* U web pretraživačima, lista elemenata sada može prikazati polja za uređivanje i dugmiće. (#588)
* Početna podrška za  Windows 10 na  ARM64 procesorima. (#7508)
* Rana podrška za čitanje i interakciju sa matematičkim sadržajem u programu Kindle books sa  accessible math. (#7536)
* Dodata podrška za Azardi čitač elektronskih knjiga. (#5848)
* Informacije o verziji dodatka se sada prikazuju kada ažurirate dodatak. (#5324)
* Dodata podrška za nove parametre za pravljenje prenosne kopije programa NVDA iz komandne linije. (#6329)
* Podrška za  Microsoft Edge kada se pokrene iz Windows Defender zaštitnika  aplikacija na jesenjem ažuriranju Windowsa 10. (#7600)
* Ako je pokrenut na laptop ili tablet računaru, NVDA će sada prijaviti kada se punjač uključi ili isključi, i kada se orijentacija ekrana promeni . (#4574, #4612)
* Novi jezik: Makedonski.
* Nove tablice za brajev prevod: Hrvatski stepen 1, Vietnamski stepen 1. (#7518, #7565)
* Rečnici glasova sada imaju svoju verziju i prebačeni su u folder "speechDicts/voiceDicts.v1". (#7592)
* Datoteke koje imaju verziju (korisnička podešavanja, glasovni rečnici) se više ne čuvaju kada se privremena kopija programa NVDA pokrene. (#7688)
* Podrška za Actilino brajev red kompanije Handy Tech je dodata. (#7590)
* Brajev unos za  Handy Tech brajeve redove je sada podržan. (#7590)

### Promene

* Minimalni zahtevan operativni sistem za  NVDA je sada  Windows 7 sa  Service Packom 1, ili Windows Server 2008 R2 sa  Service Packom 1. (#7546)
* Web dijalozi u pretraživačima Firefox i Chrome sada automatski koriste režim pretraživanja, osim ako se radi u Web aplikaciji. (#4493)
* U režimu pretraživanja, korišćenje tastera tab ili brze navigacije više ne izgovara početak i kraj sadrživača na primer liste, što čini navigaciju jednostavnijom. (#2591)
* U režimu pretraživanja programa Firefox i Chrome, imena grupa polja za uređivanje se sada izgovaraju kada koristite brzu navigaciju ili taster tab. (#3321)
* U režimu pretraživanja, komanda brze navigacije za umetnute objekte (o i  šift+o) sada uključuje elemente za zvuk i video kao i elemente sa ARIA vrednostima aplikacije i dijaloga. (#7239)
* Espeak-ng je ažuriran na verziju 1.49.2, ova verzija ispravlja određene probleme sa objavljivanjem  novih verzija. (#7385, #7583)
* Nakon što tri puta koristite komandu "pročitaj statusnu traku", njen sadržaj se kopira u privremenu memoriju. (#1785)
* Kada podešavate prečice za korišćenje na Baum brajevom redu, možete ih ograničiti na model koji koristite (na primer VarioUltra ili  Pronto). (#7517)
* Nedodeljena prečica je dodata za režim pretraživanja koja vam omogućava da brzo uključite i isključite tabele za izgled. Možete je pronaći u kategoriji režim pretraživanja ulaznih komandi. (#7634)
* Ažuriran  liblouis brajev prevodilac na verziju 3.3.0. (#7565)
* brajevi redovi Braillino, Bookworm i  Modular (sa starijim softverom) kompanije Handy Tech više nisu podržani. Instalirajte Handy Tech univerzalni driver i NVDA dodatak kako biste ih koristili. (#7590)

### Ispravljene greške

* Linkovi se sada ispravno prepoznaju na brajevom redu u aplikacijama kao što je Microsoft Word. (#6780)
* NVDA više ne postaje znatno sporiji kada imate puno otvorenih kartica u programima Firefox i Chrome. (#3138)
* Prebacivanje kursora za  MDV Lilli brajev red više ne pomera kursor za jednu ćeliju unapred od očekivane pozicije. (#7469)
* U programu  Internet Explorer i drugim  MSHTML dokumentima, HTML5 potreban atribut je sada podržan za izgovor stanja polja za uređivanje. (#7321)
* Brajev red se sada ispravno ažurira kada pišete dokumente na Arapskom u programu word pad sa poravnanjem na levoj strani. (#511).
* Imena za kontrole u programu Mozilla firefox u režimu pretraživanja se sada bolje prijavljuju kada ime nije deo sadržaja. (#4773)
* Na Windows 10 creators ažuriranju, NVDA može ponovo pristupiti programu Firefox čak i kada se NVDA ponovo pokrene. (#7269)
* Kada ponovo pokrenete program NVDA dok je program Mozilla firefox fokusiran, režim pretraživanja će ponovo biti dostupan, ali možda ćete morati da koristite komandu alt+tab da se prebacite na neki drugi prozor a nakon toga vratite u Firefox. (#5758)
* Sada je moguće pristupiti matematičkom sadržaju u programu Google Chrome čak i na sistemima gde program Mozilla Firefox nije instaliran. (#7308)
* Druge aplikacije i sam operativni sistem bi trebalo da budu stabilniji nakon instalacije programa NVDA bez ponovnog pokretanja, u poređenju sa instalacijom prethodnih verzija. (#7563)
* Kada se koristi komanda za prepoznavanje sadržaja (na primer NVDA+r), NVDA sada prijavljuje grešku umesto ničega ako navigacioni objekat nestane. (#7567)
* Pomeranje brajevih redova unazad je popravljeno za Freedom scientific brajeve redove koji poseduju levu liniju za pomeranje. (#7713)

### Promene za programere (engleski)

* "scons tests" now checks that translatable strings have translator comments. You can also run this alone with "scons checkPot". (#7492)
* There is now a new extensionPoints module which provides a generic framework to enable code extensibility at specific points in the code. This allows interested parties to register to be notified when some action occurs (extensionPoints.Action), to modify a specific kind of data (extensionPoints.Filter) or to participate in deciding whether something will be done (extensionPoints.Decider). (#3393)
* You can now register to be notified about configuration profile switches via the config.configProfileSwitched Action. (#3393)
* Braille display gestures that emulate system keyboard key modifiers (such as control and alt) can now be combined with other emulated system keyboard keys without explicit definition. (#6213) 
 * For example, if you have a key on your display bound to the alt key and another display key to downArrow, combining these keys will result in the emulation of alt+downArrow.
* The braille.BrailleDisplayGesture class now has an extra model property. If provided, pressing a key will generate an additional, model specific gesture identifier. This allows a user to bind gestures limited to a specific braille display model. 
 * See the baum driver as an example for this new functionality.
* NVDA is now compiled with Visual Studio 2017 and the Windows 10 SDK. (#7568)

## 2017.3

Glavne karakteristike ove verzije uključuju unos skraćenog brajevog pisma, podrška za nove Windows OneCore glasove dostupne na Windowsu 10, ugrađena podrška za Windows 10 OCR, i puno značajnih poboljšanja za brajev red i Web.

### Nove karakteristike

* Podešavanje za brajev red je dodato na opciju"beskonačni prikaz poruka". (#6669)
* U listi poruka programa Microsoft Outlook, NVDA izgovara označenu poruku. (#6374)
* U programu Microsoft Powerpoint, precizna vrsta oblika se sada prijavljuje u toku uređivanja slajdova (primeri uključuju: Trougao, krug, video, strelica), umesto ranijeg izgovora " Oblik". (#7111)
* Matematički sadržaj (ponuđen kao MathML) je sada podržan u programu  Google Chrome. (#7184)
* NVDA sada može da govori koristeći  nove Windows OneCore glasove  (takođe poznati kao mobilni glasovi) koji su uključeni u Windows 10. Pristupate im izborom opcije Windows OneCore glasovi  u NVDA dijalogu za izbor sintetizatora. (#6159)
* NVDA Datoteke sa korisničkim podešavanjima se sada mogu čuvati u korisničkom local  folderu foldera app data. Ovo se uključuje menjanjem podešavanja u registry bazi. Pogledajte "Sistemski parametri" u korisničkom uputstvu za više detalja. (#6812)
* U Web pretraživačima, NVDA sada prijavljuje vrednosti sadrživača mesta   za polja(konkretno, aria-placeholder je sada podržan). (#7004)
* U režimu pretraživanja programa Microsoft Word, moguća je brza navigacija između pravopisnih grešaka (w i  šift+w) (#6942)
* Dodata podrška za kontrole izbora datuma u dijalogu za dodavanje podsetnika u programu Microsoft Outlook . (#7217)
* Trenutno izabran predlog se sada prijavljuje u Windows 10 mail aplikaciji u poljima za izbor primaoca i u polju pretrage Windows 10 aplikacije za podešavanja. (#6241)
* Zvuk koji obaveštava o dostupnim predlozima se sada reprodukuje u određenim poljima pretrage Windows 10 sistema (Na primer Start ekran, polje pretrage aplikacije podešavanja, polja za unos primaoca u Windows 10 mail aplikaciji). (#6241)
* NVDA sada automatski prijavljuje Obaveštenja  u aplikaciji Skype za  biznis korisnike, na primer kada neko započne razgovor sa vama.  (#7281)
* NVDA sada automatski prijavljuje poruke dok ste u prozoru nekog razgovora aplikacije Skype za biznis korisnike. (#7286)
* Automatsko prijavljivanje obaveštenja u programu Microsoft Edge, na primer kada preuzimanje počne.  (#7281)
* Sada možete pisati u skraćenom unosu na brajevoj tastaturi brajevog reda. Pogledajte deo brajev unos korisničkog uputstva za više detalja. (#2439)
* Možete upisati unikodne brajeve znakove sa brajeve tastature izborom unikodne brajeve tabele. (#6449)
* Dodata podrška za SuperBraille brajev red koji se koristi u Tajvanu. (#7352)
* Nove brajeve tabele: Danski osmotačkasti kompjuterski brajev kod, Litvanski, Persijski osmotačkasti kompjuterski brajev kod, Persijski stepen 1, Slovenski osmotačkasti kompjuterski brajev kod. (#6188, #6550, #6773, #7367)
* Poboljšana Engleska(Sjedinjene američke države.) osmotačkasta kompjuterska brajeva tabela, uključujući podršku za nabrajanja, znak za evro i akcentovana slova. (#6836)
* NVDA sada može koristiti  OCR funkciju koja je uključena u Windows 10 da prepozna tekst slika ili nepristupačnih aplikacija. (#7361)
 * Jezik možete podesiti iz  novog  Windows 10 OCR dijaloga u meniju podešavanja NVDA menija.
 * Da prepoznate sadržaj trenutnog navigacionog objekta, pritisnite NVDA+r.
 * Pogledajte deo prepoznavanje sadržaja u korisničkom uputstvu za više detalja.
* Sada možete izabrati informacije o sadržaju fokusa koje će se prikazati na brajevom redu korišćenjem nove opcije "Predstavljanje sadržaja fokusa" u dijalogu brajeva podešavanja. (#217)
 * Na primer, opcije "prikazuj promene sadržaja na brajevom redu" i "samo kada se red pomera unazad" mogu učiniti rad sa menijima i listama lakšim, budući da stavke neće stalno menjati njihovu poziciju na brajevom redu.
 * Pogledajte deo "Predstavljanje sadržaja fokusa" u korisničkom uputstvu za dodatne primere i detalje.
* U programima Firefox i  Chrome, NVDA sada podržava dinamičke prikaze mreža kao što su tabele u kojima  se može učitati ili prikazati samo deo sadržaja (konkretno,  aria-rowcount, aria-colcount, aria-rowindex i  aria-colindex atributi koji su ubačeni u  ARIA 1.1). (#7410)

### Promene

* Nedodeljena komanda je dodata za ponovno pokretanje programa NVDA. Možete je pronaći u kategoriji razno dijaloga ulazne komande. (#6396)
* Raspored tastature se sada može podesiti iz dijaloga dobrodošlice. (#6863)
* Puno novih vrsta kontrola je dobilo svoje skraćenice za brajev red. Orjentiri su takođe dobili skraćenice. Molimo pročitajte "Skraćenice za vrste, stanje kontrola i orjentire" u korisničkom uputstvu za potpunu listu. (#7188, #3975)
* Espeak-ng je ažuriran na verziju 1.49.1 (#7280).
* Ulazne i izlazne tabele u dijalogu brajevih podešavanja su sada poređane po abecedi. (#6113)
* Ažuriran liblouis brajev prevodilac  na verziju 3.2.0. (#6935)
* Podrazumevana brajeva tabela je sada Engleski brajev kod stepen 1. (#6952)
* Po podrazumevanim podešavanjima, NVDA sada prikazuje samo deo sadržaja na brajevom redu koji je promenjen kada neki objekat dobije fokus. (#217)
 * Ranije, informacije o promenama su bile prikazivane kad god je to moguće, bez obzira da li ste videli te informacije ranije.
 * Možete se vratiti na stariji prikaz menjanjem opcije "Predstavljanje sadržaja fokusa" u dijalogu brajeva podešavanja na opciju "Uvek prikazuj promene sadržaja".
* Kada koristite brajev red, kursor se može podesiti za drugačiji oblik kada je brajev red vezan za fokus ili pregled. (#7122)
* NVDA logo je ažuriran. Ažuriran logo su slova NVDA u belom, na ljubičastoj pozadini. Ovo omogućava da bude vidljiv na bilo kojoj pozadini, i koristi ljubičastu boju iz NV Access logoa. (#7446)

### Ispravljene greške

* Uređivački div elementi u programu Chrome više ne prijavljuju svoju oznaku kao vrednost u režimu pretraživanja. (#7153)
* Pritiskanje tastera end dok ste u režimu pretraživanja praznog Microsoft Word dokumenta više ne izaziva grešku. (#7009)
* Režim pretraživanja je sada ispravno podržan u dokumentima programa Microsoft Edge gde dokument ima posebnu ARIA vrednost document. (#6998)
* U režimu pretraživanja, možete birati ili poništavati izbor znaka  na kraju reda korišćenjem komande šift+end čak i kada je kursor na poslednjem znaku reda. (#7157)
* Ako dijalog sadrži traku napredovanja, tekst dijaloga se ažurira kada se traka napredovanja promeni. Ovo znači, na primer, da sada možete čitati preostalo vreme u NVDA-ovom dijalogu"preuzimanje ažuriranja". (#6862)
* NVDA će sada izgovarati promene izbora u određenim izbornim okvirima sistema Windows 10 na primer automatska reprodukcija u podešavanjima. (#6337).
* Bespotrebne informacije sada se neće izgovarati kada ulazite u dijalog za dodavanje sastanka/podsetnika programa Microsoft Outlook. (#7216)
* Pištanja za trake napredovanja koje su beskonačne kao što je provera ažuriranja programa NVDA se sada reprodukuju samo kada su omogućena. (#6759)
* U programu  Microsoft Excel 2007 i  2003, ćelije se ponovo prijavljuju kada se krećete kroz radni list. (#7243)
* U Windows 10 Creators ažuriranju i novijim ažuriranjima, režim pretraživanja će ponovo automatski biti omogućen tokom čitanja poruka u Windows 10 Mail aplikaciji. (#7289)
* Na većini brajevih redova sa brajevom tastaturom, tačka 7 sada briše poslednju dodatu brajevu ćeliju ili znak, a tačka 8 pritiska taster enter. (#6054)
* Kada se uređuje tekst, dok pomerate kursor(npr. sa kursorskim tasterima ili tasterom backspace), NVDAovo čitanje je preciznije u puno slučajeva, posebno u Chromeu i terminal aplikacijama. (#6424)
* Sadržaj uređivača opisa programa Microsoft Outlook 2016 sada može da se čita. (#7253)
* U  Java Swing aplikacijama, NVDA više ne zaustavlja aplikaciju u određenim situacijama navigacije kroz tabele. (#6992)
* U Windows 10 Creators ažuriranju, NVDA više neće izgovarati obaveštenja više puta. (#7128)
* U start meniju Windowsa 10, pritiskanje tastera enter nakon pretrage više ne izaziva NVDA da ponovi upisan tekst. (#7370)
* Brza navigacija kroz naslove u programu Microsoft Edge je sada znatno ubrzana. (#7343)
* U programu Microsoft Edge, navigacija u režimu pretraživanja više ne preskače delove stranica kao što su Wordpress 2015 tema. (#7143)
* U programu  Microsoft Edge, obeleživači  se ispravno prijavljuju na drugim jezicima. (#7328)
* Brajev red sada ispravno prati izbor teksta čak i kada birate tekst koji je veći od brajevog reda. Na primer, Ako birate više redova teksta komandom Šift+ strelica dole, brajev red sada prikazuje poslednji red izabranog teksta. (#5770)
* U Firefoxu, NVDA više ne izgovara "Sekcija" više puta kada otvarate detalje za tweet na sajtu twitter.com. (#5741)
* Komande za navigaciju kroz tabele više nisu dostupne za table koje služe samo za izgled osim ako prijavljivanje takvih tabela nije omogućeno. (#7382)
* U programima  Firefox i  Chrome, komande za navigaciju kroz tabele sada preskaču skrivene ćelije u tabelama. (#6652, #5655)

### Promene za programere (engleski)

* Timestamps in the log now include milliseconds. (#7163)
* NVDA must now be built with Visual Studio Community 2015. Visual Studio Express is no longer supported. (#7110)
 * The Windows 10 Tools and SDK are now also required, which can be enabled when installing Visual Studio.
 * See the Installed Dependencies section of the readme for additional details.
* Support for content recognizers such as OCR and image description tools can be easily implemented using the new contentRecog package. (#7361)
* The Python json package is now included in NVDA binary builds. (#3050)

## 2017.2

Glavne karakteristike ove verzije uključuju podršku za stišavanje pozadinskih zvukova u Windows 10 creators ažuriranju; ispravljeni problemi sa izborom teksta u režimu pretraživanja, uključujući probleme sa komandom izaberi sve; velika poboljšanja za Microsoft Edge podršku; i poboljšanja Web podrške što uključuje izgovor elemenata koji su označeni kao trenutni(koristeći aria-current).

### Nove karakteristike

* Informacije o granicama ćelija sada mogu biti izgovorene u programu Microsoft Excel koristeći komandu `NVDA+f`. (#3044)
* U Web pretraživačima, NVDA sada izgovara kada se element označi kao trenutni(konkretno, koristeći aria-current svojstvo). (#6358)
* Podrška za automatsku promenu jezika u programu Microsoft Edge. (#6852)
* Podrška za Windows kalkulator na Windows 10 Enterprise LTSB (Long-Term Servicing Branch) i Server verzijama. (#6914)
* Kada se koristi komanda za čitanje trenutnog reda tri puta trenutni red se sriče koristeći fonetsko sricanje. (#6893)
* Novi jezik: Bermudski.
* Simboli za strelice gore i dole i ostali unikod simboli se sada ispravno čitaju. (#3805)

### Promene

* Kada se koristi jednostavan pregled u aplikacijama koje koriste UI automaciju, više stavki koje nemaju sadržaj se ignorišu kako bi navigacija bila olakšana. (#6948, #6950) 

### Ispravljene greške

* Stavke menija na web stranicama(stavka menija za potvrdu i radio dugme) se sada mogu aktivirati u režimu pretraživanja. (#6735)
* Prijavljivanje imena listova u programu Excel je sada prevedeno. (#6848)
* Ako se pritisne  ESC dok je dijalog u konfiguracionim profilima"potvrdi brisanje" aktivan dialog se zatvara. (#6851)
* Popravljene određene nestabilnosti u programu Mozilla Firefox i drugim Gecko aplikacijama gde je multi-process stavka omogućena. (#6885)
* Prijavljivanje boja u režimu pregleda ekrana je sada preciznije kada je tekst preslikan transparentnom pozadinom(#6467) 
* Poboljšana podrška za  aria-describedby u programu Internet Explorer 11, uključujući podršku u okvirima i kada je više imena ponuđeno. (#5784)
* U Windows Creators ažuriranju, NVDA stišavanje pozadinskih zvukova ponovo radi kao i u prethodnim verzijama(to jest stišavaj u toku izgovaranja, uvek stišavaj, i bez stišavanja su dostupni). (#6933)
* NVDA neće više grešiti u prijavljivanju ili navigaciji do određenih (UIA) kontrola gde ne postoji tastaturna prečica. (#6779)
* Dva razmaka neće više biti dodata za određene (UIA) kontrole. (#6790)
* Određene kombinacije tastera na HIMS brajevim redovima(na primer razmak+tačka 4) više neće biti neuspešne. (#3157)
* Popravljena greška gde otvaranje serijskog porta na jezicima koji nisu engleski dovodi do neuspešne veze sa brajevim redom u određenim slučajevima. (#6845)
* Smanjena šansa oštećenja datoteke sa podešavanjima kada se Windows isključi. Datoteka sa podešavanjima se sada prvo čuva u privremenoj datoteci pre promene trenutne datoteke. (#3165)
* Kada se koristi komanda za čitanje trenutnog reda dva puta za sricanje, ispravan jezik se koristi za slova. (#6726)
* Kretanje po redovima u programu Microsoft Edge je do 3 puta brže u Windows 10 Creators ažuriranju. (#6994)
* NVDA više ne izgovara"Web Runtime grouping" kada je fokus na Microsoft Edge dokumentima u Windows 10 Creators ažuriranju (#6948)
* Sve postojeće verzije SecureCRT su sada podržane. (#6302)
* Adobe Acrobat Reader ne prestaje da radi u određenim dokumentima(specifično, u onim koji sadrže prazne atribute teksta). (#7021, #7034)
* U režimu pretraživanja programa Microsoft Edge, interaktivne tabele(ARIA mreže) se više ne preskaču u toku navigacije kroz tabele tasterima t i šift+t. (#6977)
* U režimu pretraživanja, komanda šift+home nakon biranja teksta napred ispravno poništava izbor do početka reda. (#5746)
* U režimu pretraživanja, izaberi sve(kontrol+a) više neće neispravno birati tekst ako kursor nije na početku teksta. (#6909)
* Popravljeni ostali retki problemi sa izborom teksta u režimu pretraživanja. (#7131)

### Promene za programere (engleski)

* Commandline arguments are now processed with Python's argparse module, rather than optparse. This allows certain options such as -r and -q to be handled exclusively. (#6865)
* core.callLater now queues the callback to NVDA's main queue after the given delay, rather than waking the core and executing it directly. This stops possible freezes due to the  core accidentally going to sleep after processing a callback, in the midle of  a modal call such as the desplaying of a message box. (#6797)
* The InputGesture.identifiers property has been changed so that it is no longer normalized. (#6945)
 * Subclasses no longer need to normalize identifiers before returning them from this property.
 * If you want normalized identifiers, there is now an InputGesture.normalizedIdentifiers property which normalizes the identifiers returned by the identifiers property .
* The InputGesture.logIdentifier property is now deprecated. Callers should use InputGesture.identifiers[0] instead. (#6945)
* Removed some deprecated code:
 * `speech.REASON_*` constants: `controlTypes.REASON_*` should be used instead. (#6846)
 * `i18nName` for synth settings: `displayName` and `displayNameWithAccelerator` should be used instead. (#6846, #5185)
 * `config.validateConfig`. (#6846, #667)
 * `config.save`: `config.conf.save` should be used instead. (#6846, #667)
* The list of completions in the autocomplete context menu of the Python Console no longer shows  any object path leading up to the final symbol being completed. (#7023)
* There is now a unit testing framework for NVDA. (#7026)
 * Unit tests and infrastructure are located in the tests/unit directory. See the docstring in the tests\unit\init.py file for details.
 * You can run tests using "scons tests". See the "Running Tests" section of readme.md for details.
 * If you are submitting a pull request for NVDA, you should first run the tests and ensure they pass.

## 2017.1 (promene za starije verzije su na engleskom)

Highlights of this release include reporting of sections and text columns in Microsoft Word; Support for reading, navigating and annotating books in Kindle for PC; and improved support for Microsoft Edge.

### New Features

* In Microsoft Word, the types of section breaks and section numbers can now be reported. This is enabled with the "Report page numbers" option in the Document Formatting dialog. (#5946)
* In Microsoft Word, text columns can now be reported. This is enabled with the "Report page numbers" option in the document formatting dialog. (#5946)
* Automatic language switching is now supported in WordPad. (#6555)
* The NVDA find command (NVDA+control+f) is now supported in browse mode in Microsoft Edge. (#6580)
* Quick navigation for buttons in browse mode (b and shift+b) is now supported in Microsoft Edge. (#6577)
* When copying a sheet in Microsoft Excel, column and row headers are remembered. (#6628)
* Support for reading and navigating books in Kindle for PC version 1.19, including access to links, footnotes, graphics, highlighted text and user notes. Please see the Kindle for PC section of the NVDA User Guide for further information. (#6247, #6638)
* Browse mode table navigation is now supported in Microsoft Edge. (#6594)
* In Microsoft Excel, the report review cursor location command (desktop: NVDA+numpadDelete, laptop: NVDA+delete) now reports the name of the worksheet and the cell location. (#6613)
* Added an option to the exit dialog to restart with debug level logging. (#6689)

### Changes

* The minimum braille cursor blink rate is now 200 ms. If this was previously set lower, it will be increased to 200 ms. (#6470)
* A check box has been added to the braille settings dialog to allow enabling/disabling braille cursor blinking. Previously a value of zero was used to achieve this. (#6470)
* Updated eSpeak NG (commit e095f008, 10 January 2017). (#6717)
* Due to changes In the Windows 10 Creators Update, the "Always duck" mode is no longer available in NVDA's Audio ducking settings. It is still available on older windows 10 releases. (#6684)
* Due to changes in the  Windows 10 Creators Update, the "Duck when outputting speech and sounds" mode can no longer ensure audio has ducked fully before starting to speak, nor will it keep audio ducked long enough after speaking to stop rappid bouncing in volume. These changes do not   affect older windows 10 releases. (#6684)

### Bug Fixes

* Fixed freeze in Microsoft Word when moving by paragraph through a large document while in browse mode. (#6368)
* Tables in Microsoft Word that have been copied from Microsoft Excel are no longer treeted as layout tables and therefore are no longer ignored. (#5927)
* When trying to type in Microsoft Excel while in protected view, NVDA now makes a sound rather than speaking characters that were not actually typed. (#6570)
* Pressing escape in Microsoft Excel no longer incorrectly switches to browse mode, unless the user has previously switched to browse mode explicitly with NVDA+space and then entered focus mode by pressing enter on a form field. (#6569) 
* NVDA no longer freezes in Microsoft Excel spreadsheets where an entire row or column is merged. (#6216)
* Reporting of cropped/overflowed text in Microsoft Excel cells should now be more accurate. (#6472)
* NVDA now reports when a check box is read-only. (#6563)
* The NVDA launcher will no longer show a warning dialog when it can't play the logo sound due to no audio device being available. (#6289)
* Controls in the Microsoft Excel Ribbon that are unavailable are now reported as such. (#6430)
* NVDA will no longer announce "pane" when minimizing windows. (#6671)
* Typed characters are now spoken in Universal Windows Platform (UWP) apps (including Microsoft Edge) in the Windows 10 Creators Update. (#6017)
* Mouse tracking now works across all screens on computers with multiple monitors. (#6598)
* NVDA no longer becomes unusable after exiting Windows Media Player while focused on a slider control. (#5467)

### Promene za programere (engleski)

* Profiles and configuration files are now automatically upgraded to meet the requirements of schema modifications. If there is an error during upgrade, a notification is shown, the configuration is reset and the old configuration file is available in the NVDA log at 'Info' level. (#6470)

## 2016.4

Highlights of this release include improved support for Microsoft Edge; browse mode in the Windows 10 Mail app; and significant improvements to NVDA's dialogs.

### New Features

* NVDA can now indicate line indentation using tones. This can be configured using the "Line indentation reporting" combo box in NVDA's Document Formatting preferences dialog. (#5906)
* Support for the Orbit Reader 20 braille display. (#6007)
* An option to open the speech viewer window on startup has been added. This can be enabled via a check box in the speech viewer window. (#5050)
* When re-opening the speech viewer window, the location and dimensions will now be restored. (#5050)
* Cross-reference fields in Microsoft Word are now treated like hyperlinks. They are reported as links and can be activated. (#6102)
* Support for the Baum SuperVario2, Baum Vario 340 and HumanWare Brailliant2 braille displays. (#6116)
* Initial support for the Anniversary update of Microsoft Edge. (#6271)
* Browse mode is now used when reading emails in the Windows 10 mail app. (#6271)
* New language: Lithuanian.

### Changes

* Updated liblouis braille translator to 3.0.0. This includes significant enhancements to Unified English Braille. (#6109, #4194, #6220, #6140)
* In the Add-ons Manager, the Disable add-on and Enable add-on buttons now have keyboard shortcuts (alt+d and alt+e, respectively). (#6388)
* Various padding and alignment issues in NVDA's dialogs have been resolved. (#6317, #5548, #6342, #6343, #6349)
* The document formatting dialog has been adjusted so that the contents scrolls. (#6348)
* Adjusted the layout of the Symbol Pronunciation dialog so the full width of the dialog is used for the symbols list. (#6101)
* In browse mode in web browsers, the edit field (e and shift+e) and form field (f and shift+f) single letter navigation commands can now be used to move to read-only edit fields. (#4164)
* In NVDA's Document Formatting settings, "Announce formatting changes after the cursor" has been renamed to "Report formatting changes after the cursor", as it affects braille as well as speech. (#6336)
* Adjusted the appearance of the NVDA "Welcome dialog". (#6350)
* NVDA dialog boxes now have their "ok" and "cancel" buttons aligned to the right of the dialog. (#6333)
* Spin Controls are now used for numeric input fields such as the "Capital pitch change percentage" setting  in the Voice Settings dialog. You can enter the desired value or use the up and down arrow keys to adjust the value. (#6099)
* The way IFrames (documents embedded within documents) are reported has been made more consistent across web browsers. IFrames are now reported as "frame" in Firefox. (#6047)

### Bug Fixes

* Fixed a rare error when exiting NVDA while the speech viewer is open. (#5050)
* Image maps now render as expected in browse mode in Mozilla Firefox. (#6051)
* While in the dictionary dialog, pressing the enter key now saves any changes you have made and closes the dialog. Previously, pressing enter did nothing. (#6206)
* Messages are now displayed in braille when changing input modes for an input method (native input/alphanumeric, full shaped/half shaped, etc.). (#5892, #5893)
* When disabling and then immediately re-enabling an add-on or vice versa, the add-on status now correctly reverts to what it was previously. (#6299)
* When using Microsoft Word, page number fields in headers can now be read. (#6004)
* The mouse can now be used to move focus between the symbol list and the edit fields in the symbol pronunciation dialog. (#6312)
* In browse mode in Microsoft Word, Fixed an issue that stops the elements list from appearing when a document contains an invalid hyperlink. (#5886)
* After being closed via the task bar or the alt+F4 shortcut, the speech viewer check box in the NVDA menu will now reflect the actual visibility of the window. (#6340)
* The reload plugins command no longer causes problems for triggered configuration profiles, new documents in web browsers and screen review. (#2892, #5380)
* In the list of languages in NVDA's General Settings dialog, languages such as Aragonese are now displayed correctly on Windows 10. (#6259)
* Emulated system keyboard keys (e.g. a button on a braille display which emulates pressing the tab key) are now presented in the configured NVDA language in input help and the Input Gestures dialog. Previously, they were always presented in English. (#6212)
* Changing the NVDA language (from the General Settings dialog) now has no effect until NVDA is restarted. (#4561)
* It is no longer possible to leave the Pattern field blank for a new speech dictionary entry. (#6412)
* Fixed a rare issue when scanning for serial ports on some systems which made some braille display drivers unusable. (#6462)
* In Microsoft Word, Numbered bullets in table cells are now read  when moving by cell. (#6446)
* It is now possible to assign gestures to commands for the Handy Tech braille display driver in the NVDA Input Gestures dialog. (#6461)
* In Microsoft Excel, pressing enter or numpadEnter when navigating a spreadsheet now correctly reports navigation to the next row. (#6500)
* iTunes no longer intermittently freezes forever when using browse mode for the iTunes Store, Apple Music, etc. (#6502)
* Fixed crashes in 64 bit Mozilla and Chrome-based applications. (#6497)
* In Firefox with multi-process enabled, browse mode and editable text fields now function correctly. (#6380)

### Promene za programere (engleski)

* It is now possible to provide app modules for executables containing a dot (.) in their names. Dots are replaced with underscores (_). (#5323)
* The new gui.guiHelper module includes utilities to simplify the creation of wxPython GUIs, including automatic management of spacing. This facilitates better visual appearance and consistency, as well as easing creation of new GUIs for blind developers. (#6287)

## 2016.3

Highlights of this release include the ability to disable individual add-ons; support for form fields in Microsoft Excel; significant improvements to reporting of colors; fixes and improvements related to several braille displays; and fixes and improvements to support for Microsoft Word.

### New Features

* Browse mode can now be used to read PDF documents in Microsoft Edge in the Windows 10 Anniversary Update. (#5740)
* Strikethrough and double-strikethrough are now reported if appropriate in Microsoft Word. (#5800)
* In Microsoft Word, the title of a table is now reported if one has been provided. If there is a description, it can be accessed using the open long description command (NVDA+d) in browse mode. (#5943)
* In Microsoft Word, NVDA now reports position information when moving paragraphs (alt+shift+downArrow and alt+shift+upArrow). (#5945)
* In Microsoft Word, line spacing is now reported via NVDA's report formatting command, when changing it with various Microsoft word shortcut keys, and when moving to text with different line spacing if Report Line Spacing is turned on in NVDA's Document Formatting Settings. (#2961)
* In Internet Explorer, HTML5 structural elements are now recognised. (#5591)
* Reporting of comments (such as in Microsoft Word) can now be disabled via a Report Comments checkbox in NVDA's Document Formatting settings dialog. (#5108)
* It is now possible to disable individual add-ons in the Add-ons Manager. (#3090)
* Additional key assignments have been added for ALVA BC640/680 series braille displays. (#5206)
* There is now a command to move the braille display to the current focus. Currently, only the ALVA BC640/680 series has a key assigned to this command, but it can be assigned manually for other displays in the Input Gestures dialog if desired. (#5250)
* In Microsoft Excel, you can now interact with form fields. You move to form fields using the Elements List or single letter navigation in browse mode. (#4953)
* You can now assign an input gesture to toggle simple review mode using the Input Gestures dialog. (#6173)

### Changes

* NVDA now reports colors using a basic well-understood set of 9 color hues and 3 shades, with brightness and paleness variations. This is rather than using more subjective and less understood color names. (#6029)
* The existing NVDA+F9 then NVDA+F10 behavior has been modified to select text on the first press of F10. When F10 is pressed twice (in quick succession) the text is copied to the clipboard. (#4636)
* Updated eSpeak NG to version Master 11b1a7b (22 June 2016). (#6037)

### Bug Fixes

* In browse mode in Microsoft Word, copying to the clipboard now preserves formatting. (#5956)
* In Microsoft Word, NVDA now reports appropriately when using Word's own table navigation commands (alt+home, alt+end, alt+pageUp and alt+pageDown) and table selection commands (shift added to the navigation commands). (#5961)
* In Microsoft Word dialog boxes, NVDA's object navigation has been greatly improved. (#6036)
* In some applications such as Visual Studio 2015, shortcut keys (e.g. control+c for Copy) are now reported as expected. (#6021)
* Fixed a rare issue when scanning for serial ports on some systems which made some braille display drivers unusable. (#6015)
* Reporting colors in Microsoft Word is now more accurate as changes in Microsoft Office Themes are now taken into account. (#5997)
* Browse mode for Microsoft Edge and support for Start Menu search suggestions is again available on Windows 10 builds after April 2016. (#5955)
* In Microsoft Word, automatic table header reading works better when dealing with merged cells. (#5926)
* In the Windows 10 Mail app, NVDA no longer fails to read the content of messages. (#5635) 
* When speak command keys is on, lock keys such as caps lock are no longer announced twice. (#5490)
* Windows User Account Control dialogs are again read correctly in the Windows 10 Anniversary update. (#5942)
* In the Web Conference Plugin (such as used on out-of-sight.net) NVDA no longer beeps and speaks progress bar updates related to microphone input. (#5888)
* Performing a Find Next or Find Previous command in Browse Mode will now correctly do a  case sensitive search if the original Find was case sensitive. (#5522)
* When editing dictionary entries, feedback is now given for invalid regular expressions. NVDA no longer crashes if a dictionary file contains an invalid regular expression. (#4834)
* If NVDA is unable to communicate with a braille display (e.g. because it has been disconnected), it will automatically disable use of the display. (#1555)
* Slightly improved performance of filtering in the Browse Mode Elements List in some cases. (#6126)
* In Microsoft Excel, the background pattern names reported by NVDA now match those used by Excel. (#6092)
* Improved support for the Windows 10 logon screen, including announcement of alerts and activating of the password field with touch. (#6010)
* NVDA now correctly detects the secondary routing buttons on ALVA BC640/680 series braille displays. (#5206)
* NVDA can again report Windows Toast notifications in recent builds of Windows 10. (#6096)
* NVDA no longer occasionally stops recognising key presses on Baum compatible and HumanWare Brailliant B braille displays. (#6035)
* If reporting of line numbers is enabled in NVDA's Document Formatting preferences, line numbers are now shown on a braille display. (#5941)
* When speech mode is off, reporting objects (such as pressing NVDA+tab to report the focus) now appears in the Speech Viewer as expected. (#6049)
* In the Outlook 2016 message list,  associated draft information is no longer reported. (#6219)
* In Google Chrome and Chrome-based browsers in a language other than English, browse mode no longer fails to work in many documents. (#6249)

### Promene za programere (engleski)

* Logging information directly from a property no longer results in the property  being called recursively over and over again. (#6122)

## 2016.2.1

This release fixes crashes in Microsoft Word:

* NVDA no longer causes Microsoft Word to crash immediately after it starts in Windows XP. (#6033)
* Removed reporting of grammar errors, as this causes crashes in Microsoft Word. (#5954, #5877)

## 2016.2

Highlights of this release include the ability to indicate spelling errors while typing; support for reporting grammar errors in Microsoft Word; and improvements and fixes to Microsoft Office support.

### New Features

* In browse mode in Internet Explorer and other MSHTML controls, using first letter navigation to move by annotation (a and shift+a) now moves to inserted and deleted text. (#5691)
* In Microsoft Excel, NVDA now reports the level of a group of cells, as well as whether it is collapsed or expanded. (#5690)
* Pressing the Report text formatting command (NVDA+f) twice presents the information in browse mode so it can be reviewed. (#4908)
* In Microsoft Excel 2010 and later, cell shading and gradient fill is now reported. Automatic reporting is controlled by the Report colors option in NVDA's Document Formatting preferences. (#3683)
* New braille translation table: Koine Greek. (#5393)
* In the Log Viewer, you can now save the log using the shortcut key control+s. (#4532)
* If reporting of spelling errors is enabled and supported in the focused control, NVDA will play a sound to alert you of a spelling error made while typing. This can be disabled using the new "Play sound for spelling errors while typing" option in NVDA's Keyboard Settings dialog. (#2024)
* Grammar errors are now reported in Microsoft Word. This can be disabled using the new "Report grammar errors" option in NVDA's Document Formatting preferences dialog. (#5877)

### Changes

* In browse mode and editable text fields, NVDA now treats numpadEnter the same as the main enter key. (#5385)
* NVDA has switched to the eSpeak NG speech synthesizer. (#5651)
* In Microsoft Excel, NVDA no longer ignores a column header for a cell when there is a blank row between the cell and the header. (#5396)
* In Microsoft Excel, coordinates are now announced before headers to eliminate ambiguity between headers and content. (#5396)

### Bug Fixes

* In browse mode, when attempting to use single letter navigation to move to an element which isn't supported for the document, NVDA reports that this isn't supported rather than reporting that there is no element in that direction. (#5691)
* When listing sheets in the Elements List in Microsoft Excel, sheets containing only charts are now included. (#5698)
* NVDA no longer reports extraneous information when switching windows in a Java application with multiple windows such as IntelliJ or Android Studio. (#5732)
* In Scintilla based editors such as Notepad++, braille is now updated correctly when moving the cursor using a braille display. (#5678)
* NVDA no longer sometimes crashes when enabling braille output. (#4457)
* In Microsoft Word, paragraph indentation is now always reported in the measurement unit chosen by the user (e.g. centimeters or inches). (#5804)
* When using a braille display, many NVDA messages that were previously only spoken are now brailled as well. (#5557)
* In accessible Java applications, the level of tree view items is now reported. (#5766)
* Fixed crashes in Adobe Flash in Mozilla Firefox in some cases. (#5367)
* In Google Chrome and Chrome-based browsers, documents within dialogs or applications can now be read in browse mode. (#5818)
* In Google Chrome and Chrome-based browsers, you can now force NVDA to switch to browse mode in web dialogs or applications. (#5818)
* In Internet Explorer and other MSHTML controls, moving focus to certain controls (specifically, where aria-activedescendant is used) no longer incorrectly switches to browse mode. This occurred, for example, when moving to suggestions in address fields when composing a message in Gmail. (#5676)
* In Microsoft Word, NVDA no longer freezes in large tables when reporting of table row/column headers is enabled. (#5878)
* In Microsoft word, NVDA no longer incorrectly reports text with an outline level (but not a built-in heading style) as a heading. (#5186)
* In browse mode in Microsoft Word, the Move past end/to start of container commands (comma and shift+comma) now work for tables. (#5883)

### Promene za programere (engleski)

* NVDA's C++ components are now built with Microsoft Visual Studio 2015. (#5592)
* You can now present a text or HTML message to the user in browse mode using ui.browseableMessage. (#4908)
* In the User Guide, when a <!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) -->

## 2016.1

Highlights of this release include the ability to optionally lower the volume of other sounds; improvements to braille output and braille display support; several significant fixes to Microsoft Office support; and fixes to browse mode in iTunes.

### New Features

* New braille translation tables: Polish 8 dot computer braille, Mongolian. (#5537, #5574)
* You can turn off the braille cursor and change its shape using the new Show cursor and Cursor shape options in the Braille Settings dialog. (#5198)
* NVDA can now connect to a HIMS Smart Beetle braille display via Bluetooth. (#5607)
* NVDA can optionally lower the volume of other sounds when installed on Windows 8 and later. This can be configured using the Audio ducking mode option in the NVDA Synthesizer dialog or by pressing NVDA+shift+d. (#3830, #5575)
* Support for the APH Refreshabraille in HID mode and the Baum VarioUltra and Pronto! when connected via USB. (#5609)
* Support for HumanWare Brailliant BI/B braille displays when the protocol is set to OpenBraille. (#5612)

### Changes

* Reporting of emphasis is now disabled by default. (#4920)
* In the Elements List dialog in Microsoft Excel, the shortcut for Formulas has been changed to alt+r so that it is different to the shortcut for the Filter field. (#5527)
* Updated liblouis braille translator to 2.6.5. (#5574)
* The word "text" is no longer reported when moving the focus or review cursor to text objects. (#5452)

### Bug Fixes

* In iTunes 12, browse mode now updates correctly when a new page loads in the iTunes Store. (#5191)
* In Internet Explorer and other MSHTML controls, moving to specific heading levels with single letter navigation now behaves as expected when the level of a heading is overridden for accessibility purposes (specifically, when aria-level overrides the level of an h tag). (#5434)
* In Spotify, focus no longer frequently lands on "unknown" objects. (#5439)
* Focus is now restored correctly when returning to Spotify from another application. (#5439)
* When toggling between browse mode and focus mode, the mode is reported in braille as well as speech. (#5239)
* The Start buttn on the Taskbar is no longer reported as a list and/or as selected in some versions of Windows. (#5178)
* Messages such as "inserted" are no longer reported when composing messages in Microsoft Outlook. (#5486)
* When using a braille display and text is selected on the current line (e.g. when searching in a text editor for text which occurs on the same line), the braille display will be scrolled if appropriate. (#5410)
* NVDA no longer silently exits when closing a Windows command console with alt+f4 in Windows 10. (#5343)
* In the Elements List in browse mode, when you change the type of element, the Filter by field is now cleared. (#5511)
* In editable text in Mozilla applications, moving the mouse again reads the appropriate line, word, etc. as expected instead of the entire content. (#5535)
* When moving the mouse in editable text in Mozilla applications, reading no longer stops at elements such as links within the word or line being read. (#2160, #5535)
* In Internet Explorer, the shoprite.com website can now be read in browse mode instead of reporting as blank. (Specifically, malformed lang attributes are now handled gracefully.) (#5569)
* In Microsoft Word, tracked changes such as "inserted" are no longer reported when track changes markup is not displayed. (#5566)
* When a toggle button is focused, NVDA now reports when it is changed from pressed to not pressed. (#5441)
* Reporting of mouse shape changes again works as expected. (#5595)
* When speaking line indentation, non-breaking spaces are now treated as normal spaces. Previously, this could cause announcements such as "space space space" instead  of "3 space". (#5610)
* When closing a modern Microsoft input method candidate list, focus is correctly restored to either the input composition or the underlying document. (#4145)
* In Microsoft Office 2013 and later, when the ribbon is set to show only tabs, items in the ribbon are again reported as expected when a tab is activated. (#5504)
* Fixes and improvements to touch screen gesture detection and binding. (#5652)
* Touch screen hovers are no longer reported in input help. (#5652)
* NVDA no longer fails to list comments in the Elements List for Microsoft Excel if a comment is  on a merged cell. (#5704)
* In a very rare case, NVDA no longer fails to read sheet content in Microsoft Excel with reporting of row and column headers enabled. (#5705)
* In Google Chrome, navigating within an Input composition when entering east Asian characters now works as expected. (#4080)
* When searching Apple Music in iTunes, browse mode for the search results document is now updated as expected. (#5659)
* In Microsoft Excel, pressing shift+f11 to create a new sheet now reports your new position instead of reporting nothing. (#5689)
* Fixed problems with braille display output when entering Korean characters. (#5640)

### Promene za programere (engleski)

* The new audioDucking.AudioDucker class allows code which outputs audio to indicate when background audio should be ducked. (#3830)
* nvwave.WavePlayer's constructor now has a wantDucking keyword argument which specifies whether background audio should be ducked while audio is playing. (#3830)
 * When this is enabled (which is the default), it is essential that WavePlayer.idle be called when appropriate.
* Enhanced I/O for braille displays: (#5609)
 * Thread-safe braille display drivers can declare themselves as such using the BrailleDisplayDriver.isThreadSafe attribute. A driver must be thread-safe to benefit from the following features.
 * Data is written to thread-safe braille display drivers in the background, thus improving performance.
 * hwIo.Serial extends pyserial to call a callable when data is received instead of drivers having to poll.
 * hwIo.Hid provides support for braille displays communicating via USB HID.
 * hwPortUtils and hwIo can optionally provide detailed debug logging, including devices found and all data sent and received.
* There are several new properties accessible from touch screen gestures: (#5652)
 * MultitouchTracker objects now contain a childTrackers property which contains the MultiTouchTrackers the tracker was composed of. For example, 2 finger double tap has child trackers for two 2-finger taps. The 2-finger taps themselves have child trackers for two taps.
 * MultiTouchTracker objects now also contain a rawSingleTouchTracker property if the tracker was the result of one single finger doing a tap, flick or hover. The SingleTouchTracker allows access to the underlying ID assigned to the finger by the operating system and whether or not the finger is still in contact at the current time.
 * TouchInputGestures now have x and y properties, removing the need to access the tracker for trivial cases.
 * TouchInputGesturs now contain a preheldTracker property, which is a MultitouchTracker object representing the other fingers held while this action was being performed.
* Two new touch screen gestures can be emitted: (#5652)
 * Plural tap and holds (e.g. double tap and hold)
 * A generalized identifier with finger count removed for holds (e.g. hold+hover for 1finger_hold+hover).

## 2015.4

Highlights of this release include performance improvements in Windows 10; inclusion in the Ease of Access Center in Windows 8 and later; enhancements for Microsoft Excel, including listing and renaming of sheets and access to locked cells in protected sheets; and support for editing of rich text in Mozilla Firefox, Google Chrome and Mozilla Thunderbird.

### New Features

* NVDA now appears in the Ease of Access Center in Windows 8 and later. (#308)
* When moving around cells in Excel, formatting changes are now automatically reported if the appropriate options are turned on in NVDA's Document Formatting Settings dialog. (#4878)
* A Report Emphasis option has been added to NVDA's Document formatting settings dialog. On by default, this option allows NVDA to automatically report the existence of emphasised text in documents. So far, this is only supported for em and strong tags in Browse Mode for Internet Explorer and other MSHTML controls. (#4920)
* The existence of inserted and deleted text is now reported in Browse Mode for Internet Explorer and other MSHTML controls if NVDA's Report Editor Revisions option is enabled. (#4920)
* When viewing track changes in NVDA's Elements List for Microsoft Word, more information such as what formatting properties were changed is now displayed. (#4920)
* Microsoft Excel: listing and renaming of sheets is now possible from NVDA's Elements List (NVDA+f7). (#4630, #4414)
* It is now possible to configure whether actual symbols are sent to speech synthesizers (e.g. to cause a pause or change in inflection) in the Symbol Pronunciation dialog. (#5234)
* In Microsoft Excel, NVDA now reports any input messages set by the sheet author on cells. (#5051)
* Support for the Baum Pronto! V4 and VarioUltra braille displays when connected via Bluetooth. (#3717)
* Support for editing of rich text in Mozilla applications such as Google Docs with braille support enabled in Mozilla Firefox and HTML composition in Mozilla Thunderbird. (#1668)
* Support for editing of rich text in Google Chrome and Chrome-based browsers such as Google Docs with braille support enabled. (#2634)
 * This requires Chrome version 47 or later.
* In browse mode in Microsoft Excel, you can navigate to locked cells in protected sheets. (#4952)

### Changes

* The Report Editor Revisions option in NVDA's Document formatting settings dialog is now turned on by default. (#4920)
* When moving by character in Microsoft Word with NVDA's Report Editor Revisions option enabled, less information is now reported for track changes, which makes navigation more efficient. To view the extra information, use the Elements List. (#4920)
* Updated liblouis braille translator to 2.6.4. (#5341)
* Several symbols (including basic mathematical symbols) have been moved to level some so that they are spoken by default. (#3799)
* If the synthesizer supports it, speech should now pause for parentheses and the en dash (–). (#3799)
* When selecting text, the text is reported before the indication of selection instead of after. (#1707)

### Bug Fixes

* Major performance improvements when navigating the Outlook 2010/2013 message list. (#5268)
* In a chart in Microsoft Excel, navigating with certain keys (such as changing sheets with control+pageUp and control+pageDown) now works correctly. (#5336)
* Fixed the visual appearance of the buttons in the warning dialog which is displayed when you attempt to downgrade NVDA. (#5325)
* In Windows 8 and later, NVDA now starts a lot earlier when configured to start after logging on to Windows. (#308)
 * If you enabled this using a previous version of NVDA, you will need to disable it and enable it again in order for the change to take effect. Follow this procedure:
  1. Open the General Settings dialog.
  1. Uncheck the Automatically start NVDA after I log on to Windows checkbox.
  1. Press the OK button.
  1. Open the General Settings dialog again.
  1. Check the Automatically start NVDA after I log on to Windows checkbox.
  1. Press the OK button.
* Performance enhancements for UI Automation including  File Explorer and Task Viewer. (#5293)
* NVDA now correctly switches to focus mode when tabbing to read-only ARIA grid controls in Browse Mode for Mozilla Firefox and other Gecko-based controls. (#5118)
* NVDA now correctly reports "no previous" instead of "no next" when there are no more objects when flicking left on a touch screen.
* Fixed problems when typing multiple words into the filter field in the Input Gestures dialog. (#5426)
* NVDA no longer freezes in some cases when reconnecting to a HumanWare Brailliant BI/B series display via USB. (#5406)
* In languages with conjunct characters, character descriptions now work as expected for upper case English characters. (#5375)
* NVDA should no longer occasionally freeze when bringing up the Start Menu in Windows 10. (#5417)
* In Skype for Desktop, notifications which are displayed before a previous notification disappears are now reported. (#4841)
* Notifications are now reported correctly in Skype for Desktop 7.12 and later. (#5405)
* NVDA now correctly reports the focus when dismissing a context menu in some applications such as Jart. (#5302)
* In Windows 7 and later, Color is again reported in certain applications such as Wordpad. (#5352)
* When editing in Microsoft PowerPoint, pressing enter now reports automatically entered text such as a bullet or number. (#5360)

## 2015.3

Highlights of this release include initial support for Windows 10; the ability to disable single letter navigation in browse mode (useful for some web apps); improvements in Internet Explorer; and fixes for garbled text when typing in certain applications with braille enabled.

### New Features

* The existence of spelling errors is announced in editable fields for Internet Explorer and other MSHTML controls. (#4174)
* Many more Unicode math symbols are now spoken when they appear in text. (#3805)
* Search suggestions in the Windows 10 start screen are automatically reported. (#5049)
* Support for the EcoBraille 20, EcoBraille 40, EcoBraille 80 and EcoBraille Plus braille displays. (#4078)
* In browse mode, you can now toggle single letter navigation on and off by pressing NVDA+shift+space. When off, single letter keys are passed to the application, which is useful for some web applications such as Gmail, Twitter and Facebook. (#3203)
* New braille translation tables: Finnish 6 dot, Irish grade 1, Irish grade 2, Korean grade 1 (2006), Korean grade 2 (2006). (#5137, #5074, #5097)
* The QWERTY keyboard on the Papenmeier BRAILLEX Live Plus braille display is now supported. (#5181)
* Experimental support for the Microsoft Edge web browser and browsing engine in Windows 10. (#5212)
* New language: Kannada.

### Changes

* Updated liblouis braille translator to 2.6.3. (#5137)
* When attempting to install an earlier version of NVDA than is currently installed, you will now be warned that this is not recommended and that NVDA should be completely uninstalled before proceeding. (#5037)

### Bug Fixes

* In browse mode for Internet Explorer and other MSHTML controls, quick navigation by form field no longer incorrectly includes presentational list items. (#4204)
* In Firefox, NVDA no longer inappropriately reports the content of an ARIA tab panel when focus moves inside it. (#4638)
* In Internet Explorer and other MSHTML controls, tabbing into sections, articles or dialogs  no longer inappropriately reports all content in the container. (#5021, #5025)
* When using Baum/HumanWare/APH braille displays with a braille keyboard, braille input no longer stops functioning after pressing another type of key on the display. (#3541)
* In Windows 10, extraneous information is no longer reported when pressing alt+tab or alt+shift+tab to switch between applications. (#5116)
* Typed text is no longer garbled when using certain applications such as Microsoft Outlook with a braille display. (#2953)
* In browse mode in Internet Explorer and other MSHTML controls, the correct content is now reported when an element appears or changes and is immediately focused. (#5040)
* In browse mode in Microsoft Word, single letter navigation now updates the braille display and the review cursor as expected. (#4968)
* In braille, extraneous spaces are no longer displayed between or after indicators for controls and formatting. (#5043)
* When an application is responding slowly and you switch away from that application, NVDA is now much more responsive in other applications in most cases. (#3831)
* Windows 10 Toast notifications are now reported as expected. (#5136)
* The value is now reported as it changes in certain (UI Automation) combo boxes where this was not working previously.
* In browse mode in web browsers, tabbing now behaves as expected after tabbing to a frame document. (#5227)
* The Windows 10 lock screen can now be dismissed using a touch screen. (#5220)
* In Windows 7 and later, text is no longer garbled when typing in certain applications such as Wordpad and Skype with a braille display. (#4291)
* On the Windows 10 lock screen, it is no longer possible to read the clipboard, access running applications with the review cursor, change NVDA configuration, etc. (#5269)

### Promene za programere (engleski)

* You can now inject raw input from a system keyboard that is not handled natively by Windows (e.g. a QWERTY keyboard on a braille display) using the new keyboardHandler.injectRawKeyboardInput function. (#4576)
* eventHandler.requestEvents has been added to request particular events that are blocked by default; e.g. show events from a specific control or certain events even when in the background. (#3831)
* Rather than a single i18nName attribute, synthDriverHandler.SynthSetting now has separate displayNameWithAccelerator and displayName attributes to avoid reporting of the accelerator in the synth settings ring in some languages.
 * For backwards compatibility, in the constructor, displayName is optional and will be derived from displayNameWithAccelerator if not provided. However, if you intend to have an accelerator for a setting, both should be provided.
 * The i18nName attribute is deprecated and may be removed in a future release.

## 2015.2

Highlights of this release include the ability to read charts in Microsoft Excel and support for reading and interactive navigation of mathematical content.

### New Features

* Moving forward and backward by sentence in Microsoft Word and Outlook is now possible with alt+downArrow and alt+upArrow respectively. (#3288)
* New braille translation tables for several Indian languages. (#4778)
* In Microsoft Excel, NVDA now reports when a cell has overflowing or cropped content. (#3040)
* In Microsoft Excel, you can now use the Elements List (NVDA+f7) to allow listing of charts, comments and formulas. (#1987)
* Support for reading charts in Microsoft Excel. To use this, select the chart using the Elements List (NVDA+f7) and then use the arrow keys to move between the data points. (#1987)
* Using MathPlayer 4 from Design Science, NVDA can now read and interactively navigate mathematical content in web browsers and in Microsoft Word and PowerPoint. See the "Reading Mathematical Content" section in the User Guide for details. (#4673)
* It is now possible to assign input gestures (keyboard commands, touch gestures, etc.) for all NVDA preferences dialogs and document formatting options using the Input Gestures dialog. (#4898)

### Changes

* In NVDA's Document Formatting dialog, the keyboard shortcuts for Report lists, Report links, Report line numbers and Report font name have been changed. (#4650)
* In NVDA's Mouse Settings dialog, keyboard shortcuts have been added for play audio coordinates when mouse moves and brightness controls audio coordinates volume. (#4916)
* Significantly improved reporting of color names. (#4984)
* Updated liblouis braille translator to 2.6.2. (#4777)

### Bug Fixes

* Character descriptions are now handled correctly for conjunct characters in certain Indian languages. (#4582)
* If the "Trust voice's language when processing characters and symbols" option is enabled, the Punctuation/Symbol pronunciation dialog now correctly uses the voice language. Also, the language for which pronunciation is being edited is shown in the dialog's title. (#4930)
* In Internet Explorer and other MSHTML controls, typed characters are no longer inappropriately announced in editable combo boxes such as the Google search field on the Google home page. (#4976)
* When selecting colors in Microsoft Office applications, color names are now reported. (#3045)
* Danish braille output now works again. (#4986)
* PageUp/pageDown can again be used to change slides within a PowerPoint slide show. (#4850)
* In Skype for Desktop 7.2 and later, typing notifications are now reported and problems immediately after moving focus out of a conversation have been fixed. (#4972)
* Fixed problems when typing certain punctuation/symbols such as brackets into the filter field in the Input Gestures dialog. (#5060)
* In Internet Explorer and other MSHTML controls, pressing g or shift+g to navigate to graphics now includes elements marked as images for accessibility purposes (i.e. ARIA role img). (#5062)

### Promene za programere (engleski)

* brailleInput.handler.sendChars(mychar) will no longer filter out a character if it is equal to the previous character by ensuring that the key sent is correctly released. (#4139)
* Scripts for changing touch modes will now honor new labeles added to touchHandler.touchModeLabels. (#4699)
* Add-ons can provide their own math presentation implementations. See the mathPres package for details. (#4509)
* Speech commands have been implemented to insert a break between words and to change the pitch, volume and rate. See BreakCommand, PitchCommand, VolumeCommand and RateCommand in the speech module. (#4674)
 * There is also speech.PhonemeCommand to insert specific pronunciation, but the current implementations only support a very limited number of phonemes.

## 2015.1

Highlights of this release include browse mode for documents in Microsoft Word and Outlook; major enhancements to support for Skype for Desktop; and significant fixes for Microsoft Internet Explorer.

### New Features

* You can now add new symbols in the Symbol Pronunciation dialog. (#4354)
* In the Input Gestures dialog, you can use the new "Filter by" field to show only gestures containing specific words. (#4458)
* NVDA now automatically reports new text in mintty. (#4588)
* In the browse mode Find dialog, there is now an option to perform a case sensitive search. (#4584)
* Quick navigation (pressing h to move by heading, etc.) and Elements List (NVDA+f7) are now available in Microsoft Word documents by turning on browse mode with NVDA+space. (#2975)
* Reading HTML messages in Microsoft Outlook 2007 and later has been majorly improved as Browse mode is automatically enabled for these messages. If browse mode is not enabled in some rare situations, you can force it on with NVDA+space. (#2975)
* Table column headers in Microsoft word are automatically reported for tables where a header row has been explicitly specified by the author via Microsoft word's table properties. (#4510)
 * However, For tables where rows have been merged, this will not work automatically. In this situation, you can still set column headers manually in NVDA with NVDA+shift+c.
* In Skype for Desktop, notifications are now reported. (#4741)
* In Skype for Desktop, you can now report and review recent messages using NVDA+control+1 through NVDA+control+0; e.g. NVDA+control+1 for the most recent message and NVDA+control+0 for the tenth most recent. (#3210)
* In a conversation in Skype for Desktop, NVDA now reports when a contact is typing. (#3506)
* NVDA can now be installed silently via the command line without starting the installed copy after installation. To do this, use the --install-silent option. (#4206)
* Support for the Papenmeier BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus braille displays. (#4614)

### Changes

* In NVDA's Document Formatting settings dialog, the option to report spelling errors now has a shortcut key (alt+r). (#793)
* NVDA will now use the synthesizer/voice's language for character and symbol processing (including punctuation/symbol names), regardless of whether automatic language switching is turned on. To turn off this feature so that NVDA again uses its interface language, uncheck the new option in Voice settings called Trust Voice's language when processing characters and symbols. (#4210)
* Support for the Newfon synthesizer has been removed. Newfon is now available as an NVDA add-on. (#3184)
* Skype for Desktop 7 or later is now required for use with NVDA; earlier versions are not supported. (#4218)
* Downloading of NVDA updates is now more secure. (Specifically, the update information is retrieved via https and the hash of the file is verified after it is downloaded.) (#4716)
* eSpeak has been upgraded to version 1.48.04 (#4325)

### Bug Fixes

* In Microsoft Excel, merged row and column header cells are now handled correctly. For example, if A1 and B1 are merged, then B2 will now have A1 and B1 reported as its column header rather than nothing at all. (#4617)
* When editing the content of a text box in Microsoft PowerPoint 2003, NVDA will correctly report the content of each line. Previously, in each paragraph, lines would increasingly be off by one character. (#4619)
* All of NVDA's dialogs are now centred on the screen, improving visual presentation and usability. (#3148)
* In Skype for desktop, when entering an introductory message to add a contact, entering and moving through the text now works correctly. (#3661)
* When focus moves to a new item in tree views in the Eclipse IDE, if the previously focused item is a check box, it is no longer incorrectly announced. (#4586)
* In the Microsoft Word spell check dialog, the next error will be automatically reported when the last one has been changed or ignored using respective shortcut keys. (#1938)
* Text can again be read correctly in places such as Tera Term Pro's terminal window and documents in Balabolka. (#4229)
* Focus now correctly returns to the document being edited When finishing input composition of text in Korean and other east Asian languages while editing within a frame in Internet Explorer and other MSHTML documents. (#4045)
* In the Input Gestures dialog, when selecting a keyboard layout for a keyboard gesture being added, pressing escape now closes the menu as expected instead of closing the dialog. (#3617)
* When removing an add-on, the add-on directory is now correctly deleted after restarting NVDA. Previously, you had to restart twice. (#3461)
* Major problems have been fixed when using Skype for Desktop 7. (#4218)
* When you send a message in Skype for Desktop, it is no longer read twice. (#3616)
* In Skype for Desktop, NVDA should no longer occasionally spuriously read a large flood of messages (perhaps even an entire conversation). (#4644)
* fixed a problem where NVDA's Report date/time command did not honor the regional settings specified by the user in some cases. (#2987)
* In browse mode, nonsensical text (sometimes spanning several lines) is no longer presented for certain graphics such as found on Google Groups. (Specifically, this occurred with base64 encoded images.) (#4793)
* NVDA should no longer freeze after a few seconds when moving focus away from a Windows Store app as it becomes suspended. (#4572)
* The aria-atomic attribute on live regions in Mozilla Firefox is now honored even when the atomic element itself changes. Previously, it only affected descendant elements. (#4794)
* Browse mode will reflect updates, and live regions will be announced, for   browse mode documents within ARIA applications embedded in a document in Internet Explorer or other MSHTML controls. (#4798)
* When text is changed or added in live regions in Internet Explorer and other MSHTML controls where the author has specified that text is relevant, only the changed or added text is announced, rather than all of the text in the containing element. (#4800)
* Content indicated by the aria-labelledby attribute on elements in Internet Explorer and other MSHTML controls correctly replaces the original content  where it is appropriate to do so. (#4575)
* When checking spelling in Microsoft Outlook 2013, the misspelled word is now announced. (#4848)
* In Internet Explorer and other MSHTML controls, content inside elements hidden with visibility:hidden is no longer inappropriately presented in browse mode. (#4839, #3776)
* In Internet Explorer and other MSHTML controls, the title attribute on form controls no longer inappropriately takes preference over other label associations. (#4491)
* In Internet Explorer and other MSHTML controls, NVDA no longer ignores focusing  of elements  due to the aria-activedescendant attribute. (#4667)

### Promene za programere (engleski)

* Updated wxPython to 3.0.2.0. (#3763)
* Updated Python to 2.7.9. (#4715)
* NVDA no longer crashes when restarting after removing or updating an add-on which imports speechDictHandler in its installTasks module. (#4496)

## 2014.4

### New Features

* New languages: Colombian Spanish, Punjabi.
* It is now possible to restart NVDA or restart NVDA with add-ons disabled from NVDA's exit dialog. (#4057)
 * NVDA can also be started with add-ons disabled by using the --disable-addons command line option.
* In speech dictionaries, it is now possible to specify that a pattern should only match if it is a whole word; i.e. it does not occur as part of a larger word. (#1704)

### Changes

* If an object you have moved to with object navigation is inside a browse mode document, but the object you were on previously was not, the review mode is automatically set to document. Previously, this only happened if the navigator object was moved due to the focus changing. (#4369)
* The Braille display and Synthesizer lists in the respective settings dialogs are now alphabetically sorted except for No braille/No speech, which are now at the bottom. (#2724)
* Updated liblouis braille translator to 2.6.0. (#4434, #3835)
* In browse mode, pressing e and shift+e to navigate to edit fields now includes editable combo boxes. This includes the search box in the latest version of Google Search. (#4436)
* Clicking the NVDA icon in the Notification Area with the left mouse button now opens the NVDA menu instead of doing nothing. (#4459)

### Bug Fixes

* When moving focus back to a browse mode document (e.g. alt+tabbing to an already opened web page), the review cursor is properly positioned at the virtual caret, rather than the focused control (e.g. a nearby link). (#4369)
* In PowerPoint slide shows, the review cursor correctly follows the virtual caret. (#4370)
* In Mozilla Firefox and other Gecko-based browsers, new content within a live region will be announced even if the new content has a usable ARIA live type different to the parent live region; e.g. when content marked as assertive is added to a live region marked as polite. (#4169)
* In Internet Explorer and other MSHTML controls, some cases where a document is contained within another document no longer prevent the user from accessing some of the content (specifically, framesets inside framesets). (#4418)
* NVDA no longer crashes when attempting to use a Handy Tech braille display in some cases. (#3709)
* In Windows Vista, a spurious "Entry Point Not Found" dialog is no longer displayed in several cases such as when starting NVDA from the Desktop shortcut or via the shortcut key. (#4235)
* Serious problems with editable text controls in dialogs in recent versions of Eclipse have been fixed. (#3872)
* In Outlook 2010, moving the caret now works as expected in the location field of appointments and meeting requests. (#4126)
* Inside a live region, content which is marked as not being live (e.g. aria-live="off") is now correctly ignored. (#4405)
* When reporting the text of a status bar that has a name, the name is now correctly separated from the first word of the status bar text. (#4430)
* In password entry fields with speaking of typed words enabled, multiple asterisks are no longer pointlessly reported when beginning new words. (#4402)
* In the Microsoft Outlook message list, items are no longer pointlessly announced as Data Items. (#4439)
* When selecting text in the code editing control in the Eclipse IDE, the entire selection is no longer announced every time the selection changes. (#2314)
* Various versions of Eclipse, such as Spring Tool Suite and the version included in the Android Developer Tools bundle, are now recognised as Eclipse and handled appropriately. (#4360, #4454)
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls (including many Windows 8 applications) is now much more accurate  on high DPI displays or when document zoom is changed. (#3494) 
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls will now announce the label of more buttons. (#4173)
* When using a Papenmeier BRAILLEX braille display with BrxCom, keys on the display now work as expected. (#4614)

### Promene za programere (engleski)

* For executables which host many different apps (e.g. javaw.exe), code can now be provided to load specific app modules for each app instead of loading the same app module for all hosted apps. (#4360)
 * See the code documentation for appModuleHandler.AppModule for details.
 * Support for javaw.exe is implemented.

## 2014.3

### New Features

* The sounds played when NVDA starts and exits can be disabled via a new option in the General Settings dialog. (#834)
* Help for add-ons can be accessed from the Add-ons Manager for add-ons which support this. (#2694)
* Support for the Calendar in Microsoft Outlook 2007 and above (#2943) including:
 * Announcement of the current time when moving around with the arrow keys.
 * Indication if the selected time is within any appointments.
 * announcement of the selected appointment when pressing tab.
 * Smart filtering of the date so as to only announce the date if the new selected time or appointment is on a different day to the last.
* Enhanced support for the Inbox and other message lists in Microsoft Outlook 2010 and above (#3834) including:
 * The ability to silence column headers (from, subject, etc.) by turning off the Report Table row and column headers option in Document Formatting settings.
 * The ability to use table navigation commands (control + alt + arrows) to move through the individual columns. 
* Microsoft word: If an inline image has no alternative text set, NVDA will instead report the title of the image if the author has provided one. (#4193)
* Microsoft Word: NVDA can now report paragraph indenting with  the report formatting command (NVDA+f). It can also be reported automatically when the new Report Paragraph indenting option is enabled in Document Formatting settings. (#4165)
* Report automatically inserted text such as a new bullet, number or tab indent when pressing enter in editable documents and text fields. (#4185)
* Microsoft word: Pressing NVDA+alt+c will report  the text of a comment if the cursor is within one. (#3528)
* Improved support for automatic column and row header reading in Microsoft Excel (#3568) including:
 * Support of Excel defined name ranges to identify header cells (compatible with Jaws screen reader) .
 * The set column header (NVDA+shift+c) and set row header (NVDA+shift+r) commands now store the settings in the worksheet so that they are available the next time the sheet is opened, and will be available to other screen readers that support the defined name range scheme.
 * These commands can also now be used multiple times per sheet to set different headers for different regions.
* Support for automatic column and row header reading in Microsoft Word (#3110) including:
 * Support of Microsoft Word bookmarks to identify header cells (compatible with Jaws screen reader).
 -  set column header (NVDA+shift+c) and set row header (NVDA+shift+r) commands  while on the first header cell in a table allow you to tell NVDA that these headers should be reported automatically.  Settings are stored in the document so that they are available the next time the document is opened, and will be available to other screen readers that support the bookmark scheme.
* Microsoft Word: Report the distance from the left edge of the page when the tab key is pressed. (#1353)
* Microsoft Word: provide feedback in speech and braille for most available formatting shortcut keys (bold, italic, underline, alignment, outline level, superscript, subscript and font size). (#1353)
* Microsoft Excel: If the selected cell contains comments, they can be now reported by pressing NVDA+alt+c. (#2920)
* Microsoft Excel: Provide an NVDA-specific dialog to edit the comments on the currently selected cell when pressing Excel's shift+f2 command to enter comment editing mode. (#2920)
* Microsoft Excel: speech and braille feedback for many more selection movement shortcuts (#4211) including:
 * Vertical page movement (pageUp and pageDown);
 * Horizontal page movement (alt+pageUp and alt+pageDown);
 * Extend selection (the above keys with Shift added); and
 * Selecting the current region (control+shift+8).
* Microsoft Excel: The vertical and horizontal  alignment for cells can now be reported with the report formatting command (NVDA+f). It can also be reported automatically if the Report alignment option in Document Formatting settings is enabled. (#4212)
* Microsoft Excel: The style of a cell can now be reported with the report formatting command (NVDA+f). It can also be reported automatically if the Report Style option in Document formatting settings is enabled. (#4213)
* Microsoft PowerPoint: when moving shapes around a slide with the arrow keys, the shape's current location is now reported (#4214) including:
 * The distance between the shape and each of the  slide edges is reported.
 * If the shape covers or is covered by another shape, then the distance overlapped and the overlapped shape are reported.
 * To report this information at any time without moving a shape, press the report location command (NVDA+delete).
 * When selecting a shape, if it is covered by another shape, NVDA will report that it is obscured.
* The report location command (NVDA+delete) is more context specific in some situations. (#4219)
 * In standard edit fields and browse mode, the cursor position as a percentage through the content and its screen coordinates are reported.
 * On shapes in PowerPoint Presentations, position of the shape relative to the slide and other shapes is reported.
 * Pressing this command twice will produce the previous behaviour of reporting the location information for the entire control.
* New language: Catalan.

### Changes

* Updated liblouis braille translator to 2.5.4. (#4103)

### Bug Fixes

* In Google Chrome and Chrome-based browsers, certain chunks of text (such as those with emphasis) are no longer repeated when reporting the text of an alert or dialog. (#4066)
* In browse mode in Mozilla applications, pressing enter on a button, etc. no longer fails to activate it (or activates the wrong control) in certain cases such as the buttons at the top of Facebook. (#4106)
* Useless information is no longer announced when tabbing in iTunes. (#4128)
* In certain lists in iTunes such as the Music list, moving to the next item using object navigation now works correctly. (#4129)
* HTML elements considered headings because of WAI ARIA markup are now included in the Browse mode Elements list and quick navigation for Internet Explorer documents. (#4140)
* Following same-page links in recent versions of Internet Explorer now correctly moves to and reports the destination position in browse mode  documents. (#4134)
* Microsoft Outlook 2010 and above: Overall access to secure dialogs such as the New profiles and mail setup dialogs has been improved. (#4090, #4091, #4095)
* Microsoft Outlook: Useless verbosity has been decreased in command toolbars when navigating through  certain dialogs. (#4096, #3407)
* Microsoft word: Tabbing to a blank cell in a table no longer incorrectly announces exiting the table. (#4151)
* Microsoft Word: The first character past the end of a table (including a new blank line) is no longer incorrectly considered to be inside the table. (#4152)
* Microsoft Word 2010 spell check dialog: The actual misspelled word is reported rather than  inappropriately reporting just the first bold word. (#3431)
* In browse mode in Internet Explorer and other MSHTML controls, tabbing or using single letter navigation to move to form fields again reports the label in many cases where it didn't (specifically, where HTML label elements are used). (#4170)
* Microsoft Word: Reporting the existence and placement of comments is more accurate. (#3528)
* Navigation of certain dialogs in MS Office products such as Word, Excel and Outlook has been improved by no longer reporting particular control container toolbars which are not useful to the user. (#4198) 
* Task panes such as clipboard manager or File recovery no longer accidentilly seem to gain focus when opening an application such as Microsoft Word or Excel, which was sometimes causing the user to have to switch away from and back to the application to use the document or spreadsheet.  (#4199)
* NVDA no longer fails to run on recent Windows Operating Systems if the user's Windows language is set to Serbian (Latin). (#4203)
* Pressing numlock while in input help mode now correctly toggles numlock, rather than causing the keyboard and the Operating System to become out of sync in regards to the state of this key. (#4226)
* In Google Chrome, the title of the document is again reported when switching tabs. In NVDA 2014.2, this did not occur in some cases. (#4222)
* In Google Chrome and Chrome-based browsers, the URL of the document is no longer reported when reporting the document. (#4223)
* When running say all with the No speech synthesizer selected (useful for automated testing), say all will now complete instead of stopping after the first few lines. (#4225)
* Microsoft Outlook's Signature dialog: The Signature editing field is now accessible, allowing for full cursor tracking and format detection. (#3833)
* Microsoft Word: When reading the last line of a table cell, the entire table cell is no longer read. (#3421)
* Microsoft Word: When reading the first or last line of a table of contents, the entire table of contents is no longer read. (#3421)
* When speaking typed words and in some other cases, words are no longer incorrectly broken at marks such as vowel signs and virama in Indic languages. (#4254)
* Numeric editable text fields in GoldWave are now handled correctly. (#670)
* Microsoft Word: when moving by paragraph with control+downArrow / control+upArrow, it is no longer necessary to press them twice if moving through bulleted or numbered lists. (#3290)

### Promene za programere (engleski)

* NVDA now has unified support for add-on documentation. See the Add-on Documentation section of the Developer Guide for details. (#2694)
* When providing gesture bindings on a ScriptableObject via __gestures, it is now possible to provide the None keyword as the script. This unbinds the gesture in any base classes. (#4240)
* It is now possible to change the shortcut key used to start NVDA for locales where the normal shortcut causes problems. (#2209)
 * This is done via gettext.
 * Note that the text for the Create desktop shortcut option in the Install NVDA dialog, as well as the shortcut key in the User Guide, must also be updated.

## 2014.2

### New Features

* Announcement of text selection is now possible in some custom edit fields where display information is used. (#770)
* In accessible Java applications, position information is now announced for radio buttons and other controls that expose group information. (#3754)
* In accessible Java applications, keyboard shortcuts are now announced for controls that have them. (#3881)
* In browse mode, labels on landmarks are now reported. They are also included in the Elements List dialog. (#1195)
* In browse mode, labelled regions are now treated as landmarks. (#3741)
* In Internet Explorer documents and applications, Live Regions (part of the W3c ARIA standard) are now supported, thus allowing web authors to mark particular content to be automatically spoken as it changes. (#1846)

### Changes

* When exiting a dialog or application within a browse mode document, the browse mode document's name and type is no longer announced. (#4069)

### Bug Fixes

* The standard Windows System menu is no longer accidentally silenced in Java applications. (#3882)
* When copying text from screen review, line breaks are no longer ignored. (#3900)
* Pointless whitespace objects are no longer reported in some applications when the focus changes or when using object navigation with simple review enabled. (#3839)
* Message boxes and other dialogs produced by NVDA again cause previous speech to be canceled before announcing the dialog.
* In browse mode, the labels of controls such as links and buttons are now rendered correctly where the label has been overridden by the author for accessibility purposes (specifically, using aria-label or aria-labelledby). (#1354)
* In Browse mode in Internet Explorer, text contained within an element marked as presentational (ARIA role="presentation") is no longer inappropriately ignored. (#4031)
* It is now again possible to type Vietnamese text using the Unikey software. To do this, uncheck the new Handle keys from other applications checkbox in NVDA's Keyboard settings dialog. (#4043)
* In browse mode, radio and check menu items are reported as controls instead of just clickable text. (#4092)
* NVDA no longer incorrectly switches from focus mode to browse mode when a radio or check menu item is focused. (#4092)
* In Microsoft PowerPoint with speaking of typed words enabled, characters erased with backspace are no longer announced as part of the typed word. (#3231)
* In Microsoft Office 2010 Options dialogs, the labels of combo boxes are reported correctly. (#4056)
* In browse mode in Mozilla applications, using quick navigation commands to move to the next or previous button or form field now includes toggle buttons as expected. (#4098)
* The content of alerts in Mozilla applications is no longer reported twice. (#3481)
* In browse mode, containers and landmarks are no longer inappropriately repeated while navigating within them at the same time as page content is changing (e.g. navigating the Facebook and Twitter websites). (#2199)
* NVDA recovers in more cases when switching away from applications that stop responding. (#3825)
* The caret (insertion point) again correctly updates when doing a sayAll command while in editable text drawn directly to the screen. (#4125)

## 2014.1

### New Features

* Support for Microsoft PowerPoint 2013. Note that protected view is not supported. (#3578)
* In Microsoft word and Excel, NVDA can now read the selected symbol when choosing symbols using the Insert Symbols dialog. (#3538)
* It is now possible to choose if content in documents should be identified as clickable via a new option in the Document Formatting settings dialog. This option is on by default in accordance with the previous behavior. (#3556)
* Support for braille displays connected via Bluetooth on a computer running the Widcomm Bluetooth Software. (#2418)
* When editing text in PowerPoint, hyperlinks are now reported. (#3416)
* When in ARIA applications or dialogs on the web, it is now possible to force NVDA to switch to browse mode with NVDA+space allowing document-style navigation of the application or dialog. (#2023)
* In Outlook Express / Windows Mail / Windows Live Mail, NVDA now reports if a message has an attachment or is flagged. (#1594)
* When navigating tables in accessible Java applications, row and column coordinates are now reported, including  column and  row headers if they exist. (#3756)

### Changes

* For Papenmeier braille displays, the move to flat review/focus command has been removed. Users can assign their own keys using the Input Gestures dialog. (#3652)
* NVDA now relies  on the Microsoft VC runtime version 11, which means it can no longer be run on Operating systems older than Windows XP Service Pack 2 or Windows Server 2003 Service Pack 1.
* Punctuation level Some will now speak star (*) and plus (+) characters. (#3614)
* Upgraded eSpeak to version 1.48.04 which includes many language fixes and fixes several crashes. (#3842, #3739, #3860)

### Bug Fixes

* When moving around or selecting cells in Microsoft Excel, NVDA should no longer inappropriately announce the old cell rather than the new cell when Microsoft Excel is slow to move the selection. (#3558)
* NVDA properly handles opening a dropdown list for a cell in Microsoft Excel via the context menu. (#3586)
* New page content in iTunes 11 store pages is now shown properly in browse mode when following a link in the store or when opening the store initially. (#3625)
* Buttons for previewing songs in the iTunes 11 store now show their label in browse mode. (#3638)
* In browse mode in Google Chrome, the labels of check boxes and radio buttons are now rendered correctly. (#1562)
* In Instantbird, NVDA no longer reports useless information every time you move to a contact in the Contacts list. (#2667)
* In browse mode in Adobe Reader, the correct text is now rendered for buttons, etc. where the label has been overridden using a tooltip or other means. (#3640)
* In browse mode in Adobe Reader, extraneous graphics containing the text "mc-ref" will no longer be rendered. (#3645)
* NVDA no longer reports all cells in Microsoft Excel as underlined in their formatting information. (#3669)
* No longer show meaningless characters in browse mode documents such as those found in the Unicode private usage range. In some cases these were stopping more useful labels from being shown. (#2963)
* Input composition for entering east-asian characters no longer fails in PuTTY. (#3432)
* Navigating in a document after a canceled say all no longer results in NVDA sometimes incorrectly announcing that you have left a field (such as a table) lower in the document that the say all never actually spoke. (#3688)
* When using browse mode quick navigation commands  while in say all with skim reading enabled, NVDA more accurately announces the new field; e.g. it now says a heading is a heading, rather than just its text. (#3689)
* The jump to end or start of container quick navigation commands now honor the skim reading during say all setting; i.e. they will no longer cancel the current say all. (#3675)
* Touch gesture names listed in NVDA's Input Gestures dialog are now friendly and localized. (#3624)
* NVDA no longer causes certain programs to crash when moving the mouse over their rich edit (TRichEdit) controls. Programs include Jarte 5.1 and BRfácil. (#3693, #3603, #3581)
* In Internet Explorer and other MSHTML controls, containers such as tables marked as presentation by ARIA are no longer reported to the user. (#3713)
* in Microsoft Word, NVDA no longer inappropriately repeats table row and column information for a cell on a braille display multiple times. (#3702)
* In languages which use a space as a digit group/thousands separator such as French and German, numbers from separate chunks of text are no longer pronounced as a single number. This was particularly problematic for table cells containing numbers. (#3698)
* Braille no longer sometimes fails to update when the system caret is moved in Microsoft Word 2013. (#3784)
* When positioned on the first character of a heading in Microsoft Word, the text communicating it is a heading (including the level) no longer disappears off a braille display. (#3701)
* When a configuration profile is triggered for an application and that application is exited, NVDA no longer sometimes fails to deactivate the profile. (#3732)
* When entering Asian input into a control within NVDA itself (e.g. the browse mode Find dialog), "NVDA" is no longer incorrectly reported in place of the candidate. (#3726)
* The tabs in the Outlook 2013 options dialog are now reported. (#3826)
* Improved support for ARIA live regions in Firefox and other Mozilla Gecko applications:
 * Support for aria-atomic updates and filtering of aria-busy updates. (#2640)
 * Alternative text (such as alt attribute or aria-label) is included if there is no other useful text. (#3329)
 * Live region updates are no longer silenced if they occur at the same time as the focus moves. (#3777)
* Certain presentation elements in Firefox and other Mozilla Gecko applications are no longer inappropriately shown in browse mode (specifically, when the element is marked with aria-presentation but it is also focusable). (#3781)
* A performance improvement when navigating a document in Microsoft Word with spelling errors enabled. (#3785)
* Several fixes to the support for accessible Java applications:
 * The initially focused control in a frame or dialog no longer fails to be reported when the frame or dialog comes to the foreground. (#3753)
 * Unuseful position information is no longer announced for radio buttons (e.g. 1 of 1). (#3754)
 * Better reporting of JComboBox controls (html no longer reported, better reporting of expanded and collapsed states). (#3755)
 * When reporting the text of dialogs, some text that was previously missing is now included. (#3757)
 * Changes to the name, value or description of the focused control is now reported more accurately. (#3770)
* Fix a crash in NVDA seen in Windows 8 when focusing on certain RichEdit controls containing large amounts of text (e.g. NVDA's log viewer, windbg). (#3867)
* On systems with a high DPI display setting (which occurs by default for many modern screens), NVDA no longer routes the mouse to the wrong location in some applications. (#3758, #3703)
* Fixed an occasional problem when browsing the web where NVDA would stop working correctly until restarted, even though it didn't crash or freeze. (#3804)
* A Papenmeier braille display can now be used even if a Papenmeier display has never been connected via USB. (#3712)
* NVDA no longer freezes when the Papenmeier BRAILLEX older models braille display is selected without a display connected.

### Promene za programere (engleski)

* AppModules now contain productName and productVersion properties. This info is also now included in Developer Info (NVDA+f1). (#1625)
* In the Python Console, you can now press the tab key to complete the current identifier. (#433)
 * If there are multiple possibilities, you can press tab a second time to choose from a list.

## 2013.3

### New Features

* Form fields are now reported in Microsoft word documents. (#2295)
* NVDA can now announce revision information in Microsoft Word when Track Changes is enabled. Note that Report editor revisions in NVDA's document settings dialog (off by default) must be enabled also for them to be announced. (#1670)
* Dropdown lists in Microsoft Excel 2003 through 2010 are now announced when opened and navigated around. (#3382)
* a new 'Allow Skim Reading in Say All' option in the Keyboard settings dialog allows navigating through a document with browse mode quick navigation and line / paragraph movement commands, while remaining in say all. This option is off by default. (#2766) 
* There is now an Input Gestures dialog to allow simpler customization of the input gestures (such as keys on the keyboard) for NVDA commands. (#1532)
* You can now have different settings for different situations using configuration profiles. Profiles can be activated manually or automatically (e.g. for a particular application). (#87, #667, #1913)
* In Microsoft Excel, cells that are links are now announced as links. (#3042)
* In Microsoft Excel, the existence of comments on a cell is now reported to the user. (#2921)

### Bug Fixes

* Zend Studio now functions the same as Eclipse. (#3420)
* The changed state of certain checkboxes in the Microsoft Outlook 2010 message rules dialog are now reported automatically. (#3063)
* NVDA will now report the pinned state for pinned controls such as tabs in Mozilla Firefox. (#3372)
* It is now possible to bind scripts to keyboard gestures containing Alt and/or Windows keys as modifiers. Previously, if this was done, performing the script would cause the Start Menu or menu bar to be activated. (#3472)
* Selecting text in browse mode documents (e.g. using control+shift+end) no longer causes the keyboard layout to be switched on systems with multiple keyboard layouts installed. (#3472)
* Internet Explorer should no longer crash or become unusable when closing NVDA. (#3397)
* Physical movement and other events on some newer computers are no longer treated as inappropriate key presses. Previously, this silenced speech and sometimes triggered NVDA commands. (#3468)
* NVDA now behaves as expected in Poedit 1.5.7. Users using earlier versions will need to update. (#3485)
* NVDA can now read protected documents in Microsoft Word 2010,  no longer causing Microsoft Word to crash. (#1686)
* If an unknown command line switch is given when launching the NVDA distribution package, it no longer causes an endless loop of error message dialogs. (#3463)
* NVDA no longer fails to report alt text of graphics and objects in Microsoft Word if the alt text contains quotes or other non-standard characters. (#3579)
* The number of items for certain horizontal lists in Browse mode is now correct. Previously it may have been double the actual amount. (#2151)
* When pressing control+a in a Microsoft Excel worksheet, the updated selection will now be reported. (#3043)
* NVDA can now correctly read XHTML documents in Microsoft Internet Explorer and other MSHTML controls. (#3542)
* Keyboard settings dialog: if no key has been chosen to be used as the NVDA key, an error is presented to the user when dismissing the dialog. At least one key must be chosen for proper usage of NVDA. (#2871)
* In Microsoft Excel, NVDA now announces merged cells differently to multiple selected cells. (#3567)
* The browse mode cursor is no longer positioned incorrectly when leaving a dialog or application inside the document. (#3145)
* Fixed an issue where the HumanWare Brailliant BI/B series braille display driver wasn't presented as an option in the Braille Settings dialog on some systems, even though such a display was connected via USB.
* NVDA no longer fails  to switch to screen review when the navigator object has no actual screen location. In this case the review cursor is now placed at the top of the screen. (#3454)
* Fixed an issue which caused the Freedom Scientific braille display driver to fail when the port was set to USB in some circumstances. (#3509, #3662)
* Fixed an issue where keys on Freedom Scientific braille displays weren't detected in some circumstances. (#3401, #3662)

### Promene za programere (engleski)

* You can specify the category to be displayed to the user for scripts using the scriptCategory attribute on ScriptableObject classes and the category attribute on script methods. See the documentation for baseObject.ScriptableObject for more details. (#1532)
* config.save is deprecated and may be removed in a future release. Use config.conf.save instead. (#667)
* config.validateConfig is deprecated and may be removed in a future release. Add-ons which need this should provide their own implementation. (#667, #3632)

## 2013.2

### New Features

* Support for the Chromium Embedded Framework, which is a web browser control used in several applications. (#3108)
* New eSpeak voice variant: Iven3.
* In Skype, new chat messages are reported automatically while the conversation is focused. (#2298)
* Support for Tween, including reporting of tab names and less verbosity when reading tweets.
* You can now disable displaying of NVDA messages on a braille display by setting the message timeout to 0 in the Braille Settings dialog. (#2482)
* In the Add-ons Manager, there is now a Get Add-ons button to open the NVDA Add-ons web site where you can browse and download available add-ons. (#3209)
* In the NVDA Welcome dialog which always appears the first time you run NVDA, you can now specify whether NVDA starts automatically after you log on to Windows. (#2234)
* Sleep mode is automatically enabled when using Dolphin Cicero. (#2055)
* The Windows x64 version of Miranda IM/Miranda NG is now supported. (#3296)
* Search suggestions in the Windows 8.1 Start Screen are automatically reported. (#3322)
* Support for navigating and editing spreadsheets in Microsoft Excel 2013. (#3360)
* The Freedom Scientific Focus 14 Blue and Focus 80 Blue braille displays, as well as the Focus 40 Blue in certain configurations that weren't supported previously, are now supported when connected via Bluetooth. (#3307)
* Auto complete suggestions are now reported in Outlook 2010. (#2816)
* New braille translation tables: English (U.K.) computer braille, Korean grade 2, Russian braille for computer code.
* New language: Farsi. (#1427)

### Changes

* On a touch screen, performing a single finger flick left or right when in object mode now moves previous or next through all objects, not just those in the current container. Use 2-finger flick left or right to perform the original action of moving to the previous or next object in the current container.
* the Report layout tables checkbox found in the Browse Mode settings dialog has now been renamed to Include layout tables to reflect that quick navigation also will not locate them if the checkbox is unchecked. (#3140)
* Flat review has been replaced with object, document and screen review modes. (#2996)
 * Object review reviews text just within the navigator object, document review reviews all text in a browse mode document (if any) and screen review reviews text on the screen for the current application.
 * The commands that previously move to/from flat review now toggle between these new review modes.
 * The navigator object automatically follows the review cursor such that it remains the deepest object at the position of the review cursor when in document or screen review modes.
 * After switching to screen review mode, NVDA will stay in this mode until you explicitly switch back to document or object review mode.
 * When in document or object review mode, NVDA may automatically switch between these two modes depending on whether you are moving around a browse mode document or not.
* Updated liblouis braille translator to 2.5.3. (#3371)

### Bug Fixes

* Activating an object now announces the action before the activation, rather than the action after the activation (e.g. expand when expanding rather than collapse). (#2982)
* More accurate reading and cursor tracking in  various input fields for recent versions of Skype, such as chat and search fields. (#1601, #3036)
* In the Skype recent conversations list, the number of new events is now read for each conversation if relevant. (#1446)
* Improvements to cursor tracking and reading order for right-to-left text written to the screen; e.g. editing Arabic text in  Microsoft Excel. (#1601) 
* Quick navigation to buttons and form fields will now locate links marked as buttons for accessibility purposes in Internet Explorer. (#2750)
* In browse mode, the content inside tree views is no longer rendered, as a flattened representation isn't useful. You can press enter on a tree view to interact with it in focus mode. (#3023)
* Pressing alt+downArrow or alt+upArrow to expand a combo box while in focus mode no longer incorrectly switches to browse mode. (#2340)
* In Internet Explorer 10, table cells no longer activate focus mode, unless they have been explicitly made focusable by the web author. (#3248)
* NVDA no longer fails to start if the system time is earlier than the last check for an update. (#3260)
* If a progress bar is shown on a braille display, the braille display is updated when the progress bar changes. (#3258)
* In browse mode in Mozilla applications, table captions are no longer rendered twice. In addition, the summary is rendered when there is also a caption. (#3196)
* When changing input languages in Windows 8, NVDA now speaks the correct language rather than the previous one.
* NVDA now announces IME conversion mode changes in Windows 8.
* NVDA no longer announces garbage on the Desktop when the Google Japanese or Atok IME input methods are in use. (#3234)
* In Windows 7 and above, NVDA no longer inappropriately announces speech recognition or touch input as a keyboard language change.
* NVDA no longer announces a particular special character (0x7f) when pressing control+backspace in some editors when speak typed characters is enabled. (#3315)
* eSpeak no longer inappropriately changes in pitch, volume, etc. when NVDA reads text containing certain control characters or XML. (#3334) (regression of #437)
* In Java applications, changes to the label or value of the focused control are now announced automatically, and are reflected when subsequently querying the control. (#3119)
* In Scintilla controls, lines are now reported correctly when word wrap is enabled. (#885)
* In Mozilla applications, the name of read-only list items is now correctly reported; e.g. when navigating tweets in focus mode on twitter.com. (#3327)
* Confirmation dialogs in Microsoft Office 2013 now have their content automatically read when they appear. 
* Performance improvements when navigating certain tables in Microsoft Word. (#3326)
* NVDA's table navigation commands (control+alt+arrows) function better in certain Microsoft Word tables where a cell spans multiple rows.
* If the Add-ons Manager is already open, activating it again (either from the Tools menu or by opening an add-on file) no longer fails or makes it impossible to close the Add-ons Manager. (#3351)
* NVDA no longer freezes in certain dialogs when Japanese or Chinese Office 2010 IME is in use. (#3064)
* Multiple spaces are no longer compressed to just one space on braille displays. (#1366)
* Zend Eclipse PHP Developer Tools now functions the same as Eclipse. (#3353)
* In Internet Explorer, It is again not necessary to press tab to interact with an embedded object (such as Flash content) after pressing enter on it. (#3364)
* When editing text in Microsoft PowerPoint, the last line is no longer reported as the line above, if the final line is blank. (#3403)
* In Microsoft PowerPoint, objects are no longer sometimes spoken twice when you select them or choose to edit them. (#3394)
* NVDA no longer causes Adobe Reader to crash or freeze for certain badly formed PDF documents containing rows outside of tables. (#3399)
* NVDA now correctly detects the next slide with focus when deleting a slide in Microsoft PowerPoint's thumbnails view. (#3415)

### Promene za programere (engleski)

* windowUtils.findDescendantWindow has been added to search for a descendant window (HWND) matching the specified visibility, control ID and/or class name.
* The remote Python console no longer times out after 10 seconds while waiting for input. (#3126)
* Inclusion of the bisect module in binary builds is deprecated and may be removed in a future release. (#3368)
 * Add-ons which depend on bisect (including the urllib2 module) should be updated to include this module.

## 2013.1.1

This release fixes the problem where NVDA crashed when started if configured to use the Irish language, as well as including updates to translations and some other bug fixes.

### Bug Fixes

* Correct characters are produced when typing in NVDA's own user interface while using a Korean or Japanese input method while it is the default method. (#2909)
* In Internet Explorer and other MSHTML controls, fields marked as containing an invalid entry are now handled correctly. (#3256)
* NVDA no longer crashes when started if it is configured to use the Irish language.

## 2013.1

Highlights of this release include a more intuitive and consistent laptop keyboard layout; basic support for Microsoft PowerPoint; support for long descriptions in web browsers; and support for input of computer braille for braille displays which have a braille keyboard.

### Important

#### New Laptop Keyboard Layout

The laptop keyboard layout has been completely redesigned in order to make it more intuitive and consistent.
The new layout uses the arrow keys in combination with the NVDA key and other modifiers for review commands.

Please note the following changes to commonly used commands:

| Name |Key|
|---|---|
|Say all |NVDA+a|
|Read current line |NVDA+l|
|Read current text selection |NVDA+shift+s|
|Report status bar |NVDA+shift+end|

In addition, among other changes, all of the object navigation, text review, mouse click and synth settings ring commands have changed.
Please see the [Commands Quick Reference](keyCommands.html) document for the new keys.

### New Features

* Basic support for editing and reading Microsoft PowerPoint presentations. (#501)
* Basic support for reading and writing messages in Lotus Notes 8.5. (#543)
* Support for automatic language switching when reading documents in Microsoft Word. (#2047) 
* In Browse mode for MSHTML (e.g. Internet Explorer) and Gecko (e.g. Firefox), the existence of long descriptions are now announced. It's also possible to open the long description in a new window by pressing NVDA+d. (#809)
* Notifications in Internet Explorer 9 and above are now spoken (such as content blocking or file downloads). (#2343)
* Automatic reporting of table row and column headers is now supported for browse mode documents in Internet Explorer and other MSHTML controls. (#778)
* New language: Aragonese, Irish
* New braille translation tables: Danish grade 2, Korean grade 1. (#2737)
* Support for braille displays connected via bluetooth on a computer running the Bluetooth Stack for Windows by Toshiba. (#2419)
* Support for port selection when using Freedom Scientific displays (Automatic, USB or Bluetooth).
* Support for the BrailleNote family of notetakers from HumanWare when acting as a braille terminal for a screen reader. (#2012)
* Support for older models of Papenmeier BRAILLEX braille displays. (#2679)
* Support for input of computer braille for braille displays which have a braille keyboard. (#808)
* New keyboard settings that allow  the choice for whether NVDA should interrupt speech for typed characters and/or the Enter key. (#698)
* Support for several browsers based on Google Chrome: Rockmelt, BlackHawk, Comodo Dragon and SRWare Iron. (#2236, #2813, #2814, #2815)

### Changes

* Updated liblouis braille translator to 2.5.2. (#2737)
* The laptop keyboard layout has been completely redesigned in order to make it more intuitive and consistent. (#804)
* Updated eSpeak speech synthesizer to 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Bug Fixes

* The quick navigation keys for jumping to the next or previous separator in Browse Mode now work in Internet Explorer and other MSHTML controls. (#2781)
* If NVDA falls back to eSpeak or no speech due to the configured speech synthesizer failing when NVDA starts, the configured choice is no longer automatically set to the fallback synthesizer. This means that now, the original synthesizer will be tried again next time NVDA starts. (#2589)
* If NVDA falls back to no braille due to the configured braille display failing when NVDA starts, the configured display is no longer automatically set to no braille. This means that now, the original display will be tried again next time NVDA starts. (#2264)
* In browse mode in Mozilla applications, updates to tables are now rendered correctly. For example, in updated cells, row and column coordinates are reported and table navigation works as it should. (#2784)
* In browse mode in web browsers, certain clickable unlabelled graphics which weren't previously rendered are now rendered correctly. (#2838)
* Earlier and newer versions of SecureCRT are now supported. (#2800)
* For input  methods such as Easy Dots IME under XP, the reading string is now correctly reported.
* The candidate list in the Chinese Simplified Microsoft Pinyin input method under Windows 7 is now correctly read when changing pages with left and right arrow, and when first opening it with Home.
* When custom symbol pronunciation information is saved, the advanced "preserve" field is no longer removed. (#2852)
* When disabling automatic checking for updates, NVDA no longer has to be restarted in order for the change to fully take effect.
* NVDA no longer fails to start if an add-on cannot be removed due to its directory currently being in use by another application. (#2860)
* Tab labels in DropBox's preferences dialog can now be seen with Flat Review.
* If the input language is changed to something other than the default, NVDA now detects keys correctly for commands and input help mode.
* For languages such as German where the + (plus) sign is a single key on the keyboard, it is now possible to bind commands to it by using the word "plus". (#2898)
* In Internet Explorer and other MSHTML controls, block quotes are now reported where appropriate. (#2888)
* The HumanWare Brailliant BI/B series braille display driver can now be selected when the display is connected via Bluetooth but has never been connected via USB.
* Filtering elements in the Browse Mode Elements list with uppercase filter text now returns case-insensitive results just like lowercase rather than nothing at all. (#2951)
* In Mozilla browsers, browse mode can again be used when Flash content is focused. (#2546)
* When using a contracted braille table and expand to computer braille for the word at the cursor is enabled, the braille cursor is now positioned correctly when located after a word wherein a character is represented by multiple braille cells (e.g. capital sign, letter sign, number sign, etc.). (#2947)
* Text selection is now correctly shown on a braille display in applications such as Microsoft word 2003 and Internet Explorer edit controls.
* It is again possible to select text in a backward direction in Microsoft Word while Braille is enabled.
* When reviewing,  backspacing or deleting characters  In Scintilla edit controls, NVDA correctly announces multibyte characters. (#2855)
* NVDA will no longer fail to install when the user's profile path contains certain multibyte characters. (#2729)
* Reporting of groups for List View controls (SysListview32) in 64-bit applications no longer causes an error.
* In browse mode in Mozilla applications, text content is no longer incorrectly treated as editable in some rare cases. (#2959)
* In IBM Lotus Symphony and OpenOffice, moving the caret now moves the review cursor if appropriate.
* Adobe Flash content is now accessible in Internet Explorer in Windows 8. (#2454)
* Fixed Bluetooth support for Papenmeier Braillex Trio. (#2995)
* Fixed inability to use certain Microsoft Speech API version 5 voices such as Koba Speech 2 voices. (#2629)
* In applications using the Java Access Bridge, braille displays are now updated correctly when the caret moves in editable text fields . (#3107)
* Support the form landmark in browse mode documents that support landmarks. (#2997) 
* The eSpeak synthesizer driver now handles reading by character more appropriately (e.g. announcing a foreign letter's name or value rather than just its sound or generic name). (#3106)
* NVDA no longer fails to copy user settings for use on logon and other secure screens when the user's profile path contains non-ASCII characters. (#3092)
* NVDA no longer freezes when using Asian character input in some .NET applications. (#3005)
* it is now possible to use browse mode for pages in Internet Explorer 10 when in standards mode; e.g. [www.gmail.com](http://www.gmail.com) login page. (#3151)

### Promene za programere (engleski)

* Braille display drivers can now support manual port selection. (#426)
 * This is most useful for braille displays which support connection via a legacy serial port.
 * This is done using the getPossiblePorts class method on the BrailleDisplayDriver class.
* Braille input from braille keyboards is now supported. (#808)
 * Braille input is encompassed by the brailleInput.BrailleInputGesture class or a subclass thereof.
 * Subclasses of braille.BrailleDisplayGesture (as implemented in braille display drivers) can also inherit from brailleInput.BrailleInputGesture. This allows display commands and braille input to be handled by the same gesture class.
* You can now use comHelper.getActiveObject to get an active COM object from a normal process when NVDA is running with the UIAccess privilege. (#2483)

## 2012.3

Highlights of this release include support for Asian character input; experimental support for touch screens on Windows 8; reporting of page numbers and improved support for tables in Adobe Reader; table navigation commands in focused table rows and Windows list-view controls; support for several more braille displays; and reporting of row and column headers in Microsoft Excel.

### New Features

* NVDA can now support Asian character input using IME and text service input methods in all applications, Including:
 * Reporting and navigation of candidate lists;
 * Reporting and navigation of composition strings; and
 * Reporting of reading strings.
* The presence of underline and strikethrough is now reported in Adobe Reader documents. (#2410)
* When the Windows Sticky Keys function is enabled, the NVDA modifier key will now behave like other modifier keys. This allows you to use the NVDA modifier key without needing to hold it down while you press other keys. (#230)
* Automatic reporting of column and row headers is now supported in Microsoft Excel. Press NVDA+shift+c to set the row containing column headers and NVDA+shift+r to set the column containing row headers. Press either command twice in quick succession to clear the setting. (#1519)
* Support for HIMS Braille Sense, Braille EDGE and SyncBraille braille displays. (#1266, #1267)
* When Windows 8 Toast notifications appear, NVDA will report them if reporting of help balloons is enabled. (#2143)
* Experimental support for Touch screens on Windows 8, including:
 * Reading text directly under your finger while moving it around
 * Many gestures for performing object navigation, text review, and other NVDA commands.
* Support for VIP Mud. (#1728)
* In Adobe Reader, if a table has a summary, it is now presented. (#2465)
* In Adobe Reader, table row and column headers can now be reported. (#2193, #2527, #2528)
* New languages: Amharic, Korean, Nepali, Slovenian.
* NVDA can now read auto complete suggestions when entering email addresses in Microsoft Outlook 2007. (#689)
* New eSpeak voice variants: Gene, Gene2. (#2512)
* In Adobe Reader, page numbers can now be reported. (#2534)
 * In Reader XI, page labels are reported where present, reflecting changes to page numbering in different sections, etc. In earlier versions, this is not possible and only sequential page numbers are reported.
* It is now possible to reset NVDA's configuration to factory defaults either by pressing NVDA+control+r three times quickly or by choosing Reset to Factory Defaults from the NVDA menu. (#2086)
* Support for the Seika Version 3, 4 and 5 and Seika80 braille displays from Nippon Telesoft. (#2452)
* The first and last top routing buttons on Freedom Scientific PAC Mate and Focus Braille displays can now be used to scroll  backward and forward. (#2556)
* Many more features are supported on Freedom Scientific Focus Braille displays such as advance bars, rocker bars and certain dot combinations for common actions. (#2516)
* In applications using IAccessible2 such as Mozilla applications, table row and column headers can now be reported outside of browse mode. (#926)
* Preliminary support for the document control in Microsoft Word 2013. (#2543)
* Text alignment can now be reported in applications using IAccessible2 such as Mozilla applications. (#2612)
* When a table row or standard Windows list-view control with multiple columns is focused, you can now use the table navigation commands to access individual cells. (#828)
* New braille translation tables: Estonian grade 0, Portuguese 8 dot computer braille, Italian 6 dot computer braille. (#2319, #2662)
* If NVDA is installed on the system, directly opening an NVDA add-on package (e.g. from Windows Explorer or after downloading in a web browser) will install it into NVDA. (#2306)
* Support for newer models of Papenmeier BRAILLEX braille displays. (#1265)
* Position information (e.g. 1 of 4) is now reported for Windows Explorer list items on Windows 7 and above. This also includes any UIAutomation controls that support the itemIndex and itemCount custom properties. (#2643)

### Changes

* In the NVDA Review Cursor preferences dialog, the Follow keyboard focus option has been renamed to Follow system focus for consistency with terminology used elsewhere in NVDA.
* When braille is tethered to review and the cursor is on an object which is not a text object (e.g. an editable text field), cursor routing keys will now activate the object. (#2386)
* The Save Settings On Exit option is now on by default for new configurations.
* When updating a previously installed copy of NVDA, the desktop shortcut key is no longer forced back to control+alt+n if it was manually changed to something different by the user. (#2572)
* The add-ons list in the Add-ons Manager now shows the package name before its status. (#2548)
* If installing the same or another version of a currently installed add-on, NVDA will ask if you wish to update the add-on, rather than just showing an error and aborting installation. (#2501)
* Object navigation commands (except the report current object command) now report with less verbosity. You can still obtain the extra information by using the report current object command. (#2560)
* Updated liblouis braille translator to 2.5.1. (#2319, #2480, #2662, #2672)
* The NVDA Key Commands Quick Reference document has been renamed to Commands Quick Reference, as it now includes touch commands as well as keyboard commands.
* The Elements list in Browse mode will now remember the last element type shown (e.g. links, headings or landmarks) each time the dialog is shown within the same session of NVDA. (#365)
* Most Metro apps in Windows 8 (e.g. Mail, Calendar) no longer activate Browse Mode for the entire app.
* Updated Handy Tech BrailleDriver COM-Server to 1.4.2.0.

### Bug Fixes

* In Windows Vista and later, NVDA no longer incorrectly treats the Windows key as being held down when unlocking Windows after locking it by pressing Windows+l. (#1856)
* In Adobe Reader, row headers are now correctly recognised as table cells; i.e. coordinates are reported and they can be accessed using table navigation commands. (#2444)
* In Adobe Reader, table cells spanning more than one column and/or row are now handled correctly. (#2437, #2438, #2450)
* The NVDA distribution package now checks its integrity before executing. (#2475)
* Temporary download files are now removed if downloading of an NVDA update fails. (#2477)
* NVDA will no longer freeze when it is running as an administrator while copying the user configuration to the system configuration (for use on Windows logon and other secure screens). (#2485)
* Tiles on the Windows 8 Start Screen are now presented better in speech and braille. The name is no longer repeated, unselected is no longer reported on all tiles, and live status information is presented  as the description of the tile (e.g. current temperature for the Weather tile).
* Passwords are no longer announced when reading password fields in Microsoft Outlook and other standard edit controls that are marked as protected. (#2021)
* In Adobe Reader, changes to form fields are now correctly reflected in browse mode. (#2529)
* Improvements to support for the Microsoft Word Spell Checker, including more accurate reading of the current spelling error, and the ability to support the spell checker when running an Installed copy of NVDA on Windows Vista or higher.
* Add-ons which include files containing non-English characters can now be installed correctly in most cases. (#2505)
* In Adobe Reader, the language of text is no longer lost when it is updated or scrolled to. (#2544)
* When installing an add-on, the confirmation dialog now correctly shows the localized name of the add-on if available. (#2422)
* In applications using UI Automation (such as .net and Silverlight applications), the calculation of numeric values for controls such as sliders has been corrected. (#2417)
* The configuration for reporting of progress bars is now honoured for the indeterminate progress bars displayed by NVDA when installing, creating a portable copy, etc. (#2574)
* NVDA commands can no longer be executed from a braille display while a secure Windows screen (such as the Lock screen) is active. (#2449)
* In browse mode, braille is now updated if the text being displayed changes. (#2074)
* When on a secure Windows screen such as the Lock screen, messages from applications speaking or displaying braille directly via NVDA are now ignored.
* In Browse mode, it is no longer possible to  fall off the bottom of the document with the right arrow key when on the final character, or by jumping to the end of a container when that container is the last item in the document. (#2463)
* Extraneous content is no longer incorrectly included when reporting the text of dialogs in web applications (specifically, ARIA dialogs with no aria-describedby attribute). (#2390)
* NVDA no longer incorrectly reports or locates certain edit fields in MSHTML documents (e.g. Internet Explorer), specifically where an explicit ARIA role has been used by the web page author. (#2435)
* The backspace key is now handled correctly when speaking typed words in Windows command consoles. (#2586)
* Cell coordinates in Microsoft Excel are now shown again in Braille.
* In Microsoft Word, NVDA no longer leaves you stuck on a paragraph with list formatting when trying to navigate out over a bullet or number with left arrow or control + left arrow. (#2402)
* In browse mode in Mozilla applications, the items in certain list boxes (specifically, ARIA list boxes) are no longer incorrectly rendered.
* In browse mode in Mozilla applications, certain controls that were rendered with an incorrect label or just whitespace are now rendered with the correct label.
* In browse mode in Mozilla applications, some extraneous whitespace has been eliminated.
* In browse mode in web browsers, certain graphics that are explicitly marked as presentational (specifically, with an alt="" attribute) are now correctly ignored.
* In web browsers, NVDA now hides content which is marked as hidden from screen readers (specifically, using the aria-hidden attribute). (#2117)
* Negative currency amounts (e.g. -$123) are now correctly spoken as negative, regardless of symbol level. (#2625)
* During say all, NVDA will no longer incorrectly revert to the default language where a line does not end a sentence. (#2630)
* Font information is now correctly detected in Adobe Reader 10.1 and later. (#2175)
* In Adobe Reader, if alternate text is provided, only that text will be rendered. Previously, extraneous text was sometimes included. (#2174)
* Where a document contains an application, the content of the application is no longer included in browse mode. This prevents unexpectedly moving inside the application when navigating. You can interact with the application in the same way as for embedded objects. (#990)
* In Mozilla applications, the value of spin buttons is now correctly reported when it changes. (#2653)
* Updated support for Adobe Digital Editions so that it works in version 2.0. (#2688)
* Pressing NVDA+upArrow while on a combo box in Internet Explorer and other MSHTML documents will no longer incorrectly read all items. Rather, just the active item will be read. (#2337)
* Speech dictionaries will now properly save when using a number (#) sign within the pattern or replacement fields. (#961)
* Browse mode for MSHTML documents (e.g. Internet Explorer) now correctly displays visible content contained within hidden content (specifically, elements with a style of visibility:visible inside an element with style visibility:hidden). (#2097)
* Links in Windows XP's Security Center no longer report random junk after their names. (#1331)
* UI Automation text controls (e.g.  the search field in the Windows 7 Start Menu) are now  correctly announced when moving the mouse over them rather than staying silent.
* Keyboard layout changes are no longer reported during say all, which was particularly problematic for multilingual documents including Arabic text. (#1676)
* The entire content of some UI Automation editable text controls (e.g. the Search Box in the Windows 7/8 Start Menu) is no longer announced every time it changes.
* When moving between groups on the Windows 8 start screen, unlabeled groups no longer announce their first tile as the name of the group. (#2658)
* When opening the Windows 8 start screen, the focus is correctly placed on the first tile, rather than jumping to the root of the start screen which can confuse navigation. (#2720)
* NVDA will no longer fail to start when the user's profile path contains certain multibyte characters. (#2729)
* In browse mode in Google Chrome, the text of tabs is now rendered correctly.
* In browse mode, menu buttons are now reported correctly.
* In OpenOffice.org/LibreOffice Calc, reading spreadsheet cells now works correctly. (#2765)
* NVDA can again function in the Yahoo! Mail message list when used from Internet Explorer. (#2780)

### Promene za programere (engleski)

* Previous log file is now copied to nvda-old.log on NVDA initialization. Therefore, if NVDA crashes or is restarted, logging information from that session is still accessible for inspection. (#916)
* Fetching the role property in chooseNVDAObjectOverlayClasses no longer causes the role to be incorrect and thus not reported on focus for certain objects such as Windows command consoles and Scintilla controls. (#2569)
* The NVDA Preferences, Tools and Help menus are now accessible as attributes on gui.mainFrame.sysTrayIcon named preferencesMenu, toolsMenu and helpMenu, respectively. This allows plugins to more easily add items to these menus.
* The navigatorObject_doDefaultAction script in globalCommands has been renamed to review_activate.
* Gettext message contexts are now supported. This allows multiple translations to be defined for a single English message depending on the context. (#1524)
 * This is done using the pgettext(context, message) function.
 * This is supported for both NVDA itself and add-ons.
 * xgettext and msgfmt from GNU gettext must be used to create any PO and MO files. The Python tools do not support message contexts.
 * For xgettext, pass the --keyword=pgettext:1c,2 command line argument to enable inclusion of message contexts.
 * See http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts for more information.
* It is now possible to access built-in NVDA modules where they have been overridden by third party modules. See the nvdaBuiltin module for details.
* Add-on translation support can now be used within the add-on installTasks module. (#2715)

## 2012.2.1

This release addresses  several potential security issues (by upgrading Python to 2.7.3).

## 2012.2

Highlights of this release include an in-built installer and  portable  creation feature, automatic updates, easy management of new NVDA add-ons, announcement of graphics in Microsoft Word, support for Windows 8 Metro style apps, and several important bug fixes. 

### New Features

* NVDA can now automatically check for, download and install updates. (#73)
* Extending NVDA's functionality  has been made easier with the addition of an Add-ons Manager (found under Tools in the NVDA menu) allowing you to install and uninstall new NVDA add-on packages (.nvda-addon files) containing plugins and drivers. Note the Add-on manager does not show older custom plugins and drivers manually copied in to your configuration directory. (#213)
* Many more common NVDA features now work in Windows 8 Metro style apps when using an installed release  of NVDA, including speaking of typed characters, and browse mode for web documents (includes support for metro version of Internet Explorer 10). Portable copies of NVDA cannot access metro style apps. (#1801) 
* In browse mode documents (Internet Explorer, Firefox, etc.), you can now  jump to the start and past the end of certain containing elements (such as lists and tables) with shift+, and , respectively. (#123)
* New language: Greek.
* Graphics and alt text are now reported in Microsoft Word Documents. (#2282, #1541)

### Changes

* Announcement of cell coordinates in Microsoft Excel is now after the content rather than before, and is now only included   if the report tables and report table cell coordinates settings are enabled in the Document formatting settings dialog. (#320)
* NVDA is now distributed in one package. Rather than separate portable and installer versions, there is now just one file that, when run, will start a temporary copy of NVDA and will allow you to install or generate a portable distribution. (#1715)
* NVDA is now always installed in to Program Files on all systems. Updating a previous install will also automatically move it if it was not previously installed there.

### Bug Fixes

* With auto language switching enabled, Content such as alt text for graphics and labels for other certain controls in Mozilla Gecko (e.g. Firefox) are now reported in the correct language if marked up appropriately.
* SayAll in BibleSeeker (and other TRxRichEdit controls) no longer stops in the middle of a passage.
* Lists found in the Windows 8 Explorer file properties (permitions tab) and in Windows 8 Windows Update now read correctly.
* Fixed possible freezes in MS Word which would result when it took more than 2 seconds to fetch text from a document (extremely long lines or tables of contents). (#2191)
* Detection of word breaks now works correctly where whitespace is followed by certain punctuation. (#1656)
* In browse mode in Adobe Reader, it is now possible to navigate to headings without a level using quick navigation and the Elements List. (#2181)
* In Winamp, braille is now correctly updated when you move to a different item in the Playlist Editor. (#1912)
* The tree in the Elements List (available for browse mode documents) is now properly sized to show  the text of each element. (#2276)
* In applications using the Java Access Bridge, editable text fields are now presented correctly in braille. (#2284)
* In applications using the java Access Bridge, editable text fields no longer report strange characters in certain circumstances. (#1892)
* In applications using the Java Access Bridge, when at the end of an editable text field, the current line is now reported correctly. (#1892)
* In browse mode in applications using Mozilla Gecko 14 and later (e.g. Firefox 14), quick navigation now works for block quotes and embedded objects. (#2287)
* In Internet Explorer 9, NVDA no longer reads unwanted content when focus moves inside certain landmarks or focusable elements (specifically, a div element which is focusable or has an ARIA landmark role).
* The NVDA icon for the NVDA Desktop and Start Menu shortcuts is now displayed correctly on 64 bit editions of Windows. (#354)

### Promene za programere (engleski)

* Due to the replacement of the previous NSIS installer for NVDA with a built-in installer in Python, it is no longer necessary for translaters to maintain a langstrings.txt file for the installer. All localization strings are now managed by gettext po files.

## 2012.1

Highlights of this release include features for more fluent reading of braille; indication of document formatting in braille; access to much more formatting information and improved performance in Microsoft Word; and support for the iTunes Store.

### New Features

* NVDA can announce the number of leading tabs and spaces of the current line in the order that they are entered. This can be enabled by selecting report line indentation in the document formatting dialogue. (#373)
* NVDA can now detect key presses generated from alternative keyboard input emulation such as on-screen keyboards and speech recognition software.
* NVDA can now detect colors in Windows command consoles.
* Bold, italic and underline are now indicated in braille using signs appropriate to the configured translation table. (#538)
* Much more information is now reported in Microsoft Word documents, including:
 * Inline information such as footnote and endnote numbers, heading levels, the existence of comments, table nesting levels, links, and text color;
 * Reporting when entering document sections such as the comments story, footnotes and endnotes stories, and header and footer stories.
* Braille now indicates selected text using dots 7 and 8. (#889)
* Braille now reports information about controls within documents such as links, buttons and headings. (#202)
* Support for the hedo ProfiLine and MobilLine USB braille displays. (#1863, #1897)
* NVDA now avoids splitting words in braille when possible by default. This can be disabled in the Braille Settings dialog. (#1890, #1946)
* It is now possible to have braille displayed by paragraphs instead of lines, which may allow for more fluent reading of large amounts of text. This is configurable using the Read by paragraphs option in the Braille Settings dialog. (#1891)
* In browse mode, you can activate the object under the cursor using a braille display. This is done by pressing the cursor routing key where the cursor is located (which means pressing it twice if the cursor is not already there). (#1893)
* Basic support for web areas in iTunes such as the Store. Other applications using WebKit 1 may also be supported. (#734)
* In books in Adobe Digital Editions 1.8.1 and later, pages are now turned automatically when using say all. (#1978)
* New braille translation tables: Portuguese grade 2, Icelandic 8 dot computer braille, Tamil grade 1, Spanish 8 dot computer braille, Farsi grade 1. (#2014)
* You can now configure whether frames in documents are reported from the Document Formatting preferences dialog. (#1900)
* Sleep mode is automatically enabled when using OpenBook. (#1209)
* In Poedit, translators can now read translator added and automatically extracted comments. Messages that are untranslated or fuzzy are marked with a star and a beep is heard when you navigate onto them. (#1811)
* Support for the HumanWare Brailliant BI and B series displays. (#1990)
* New languages: Norwegian Bokmål, Traditional Chinese (Hong Kong).

### Changes

* Commands to describe the current character or to spell the current word or line now will spell in the appropriate language according to the text, if auto language switching is turned on and the appropriate language information is available.
* Updated eSpeak speech synthesizer to 1.46.02.
* NVDA will now truncate extremely long (30 characters or greater) names guessed from graphic and link URLs as they are most likely garbage that gets in the way of reading. (#1989)
* Some information displayed in braille has been abbreviated. (#1955, #2043)
* When the caret or review cursor moves, braille is now scrolled in the same way as when it is manually scrolled. This makes it more appropriate when braille is configured to read by paragraphs and/or avoid splitting words. (#1996)
* Updated to new Spanish grade 1 braille translation table.
* Updated liblouis braille translator to 2.4.1.

### Bug Fixes

* In Windows 8, focus is no longer incorrectly moved away from the Windows Explorer search field, which was not allowing NVDA to interact with it.
* Major performance improvements when reading and navigating Microsoft Word documents while automatic reporting of formatting is enabled, thus now making it quite comfortable to proof read formatting etc. Performance may be also improved over all for some users.
* Browse mode is now used for full screen Adobe Flash content.
* Fixed poor audio quality in some cases when using Microsoft Speech API version 5 voices with the audio output device set to something other than the default (Microsoft Sound Mapper). (#749)
* Again allow NVDA to be used with the "no speech" synthesizer, relying purely on braille or the speech viewer. (#1963)
* Object navigation commands no longer report "No children" and "No parents", but instead report messages consistent with the documentation.
* When NVDA is configured to use a language other than English, the name of the tab key is now reported in the correct language.
* In Mozilla Gecko (e.g. Firefox), NVDA no longer intermittently switches to browse mode while navigating menus in documents. (#2025)
* In Calculator, the backspace key now reports the updated result instead of reporting nothing. (#2030)
* In browse mode, the move mouse to current navigator object command now routes to the center of the object at the review cursor instead of the top left, making it more accurate it some cases. (#2029)
* In browse mode with automatic focus mode for focus changes enabled, focusing on a toolbar will now switch to focus mode. (#1339)
* The report title command works correctly again in Adobe Reader.
* With automatic focus mode for focus changes enabled, focus mode is now correctly used for focused table cells; e.g. in ARIA grids. (#1763)
* In iTunes, position information in certain lists is now reported correctly.
* In Adobe Reader, some links are no longer treated as containing read-only editable text fields.
* The labels of some editable text fields are no longer incorrectly included when reporting the text of a dialog. (#1960)
* The description of groupings is once again reported if reporting of object descriptions is enabled.
* The human readable sizes are now included in the text of the Windows Explorer drive properties dialog.
* Double reporting of property page text has been suppressed in some cases. (#218)
* Improved tracking of the caret in editable text fields which rely on text written to the screen. In particular, this improves editing in the Microsoft Excel cell editor and the Eudora message editor. (#1658)
* In Firefox 11, the move to containing virtual buffer command (NVDA+control+space) now works as it should to escape embedded objects such as Flash content.
* NVDA now restarts itself correctly (e.g. after changing the configured language) when it is located in a directory which contains non-ASCII characters. (#2079)
* Braille correctly respects the settings for reporting of object shortcut keys, position information and descriptions.
* In Mozilla applications, switching between browse and focus modes is no longer slow with braille enabled. (#2095)
* Routing the cursor to the space at the end of the line/paragraph using braille cursor routing keys in some editable text fields now works correctly instead of routing to the start of the text. (#2096)
* NVDA again works correctly with the Audiologic Tts3 synthesizer. (#2109)
* Microsoft Word documents are correctly treated as multi-line. This causes braille to behave more appropriately when a document is focused.
* In Microsoft Internet Explorer, errors no longer occur when focusing on certain rare controls. (#2121)
* Changing the pronunciation of punctuation/symbols by the user will now take effect straight away, rather than requiring NVDA to be restarted or auto language switching to be disabled.
* When using eSpeak, speech no longer goes silent in some cases in the Save As dialog of the NVDA Log Viewer. (#2145)

### Promene za programere (engleski)

* There is now a remote Python console for situations where remote debugging is useful. See the Developer Guide for details.
* The base path of NVDA's code is now stripped from tracebacks in the log to improve readability. (#1880)
* TextInfo objects now have an activate() method to activate the position represented by the TextInfo.
 * This is used by braille to activate the position using cursor routing keys on a braille display. However, there may be other callers in future.
* TreeInterceptors and NVDAObjects which only expose one page of text at a time can support automatic page turns during say all by using the textInfos.DocumentWithPageTurns mix-in. (#1978)
* Several control and output constants have been renamed or moved. (#228)
 * speech.REASON_* constants have been moved to controlTypes.
 * In controlTypes, speechRoleLabels and speechStateLabels have been renamed to just roleLabels and stateLabels, respectively.
* Braille output is now logged at level input/output. First, the untranslated text of all regions is logged, followed by the braille cells of the window being displayed. (#2102)
* subclasses of the sapi5 synthDriver can now override _getVoiceTokens and extend init to support custom voice tokens such as with sapi.spObjectTokenCategory to get tokens from a custom registry location.

## 2011.3

Highlights of this release include automatic speech language switching when reading documents with appropriate language information; support for 64 bit Java Runtime Environments; reporting of text formatting in browse mode in Mozilla applications; better handling of application crashes and freezes; and initial fixes for Windows 8.

### New Features

* NVDA can now change the eSpeak synthesizer language on the fly when reading certain web/pdf documents with appropriate language information. Automatic language/dialect switching can be toggled on and off from the Voice Settings dialog. (#845) 
* Java Access Bridge 2.0.2 is now supported, which includes support for 64 bit Java Runtime Environments.
* In Mozilla Gecko (e.g. Firefox) Heading levels are now announced  when using object navigation.
* Text formatting can now be reported when using browse mode in Mozilla Gecko (e.g. Firefox and Thunderbird). (#394)
* Text with underline and/or strikethrough can now be detected and reported in standard IAccessible2 text controls such as in Mozilla applications.
* In browse mode in Adobe Reader, table row and column counts are now reported.
* Added support for the Microsoft Speech Platform synthesizer. (#1735)
* Page and line numbers are now reported for the caret in IBM Lotus Symphony. (#1632)
* The percentage of how much the pitch changes when speaking a capital letter is now configurable from the voice settings dialog. However, this does replace the older raise pitch for capitals checkbox (therefore to turn off this feature set the percentage to 0). (#255)
* Text and background color is now included in the reporting of formatting for cells in Microsoft Excel. (#1655)
* In applications using the Java Access Bridge, the activate current navigator object command now works on controls where appropriate. (#1744)
* New language: Tamil.
* Basic support for Design Science MathPlayer.

### Changes

* NVDA will now restart itself if it crashes.
* Some information displayed in braille has been abbreviated. (#1288)
* the Read active window script (NVDA+b) has been improved to filter out unuseful controls   and also is now much more easy to silence. (#1499)
* Automatic say all when a browse mode document loads is now optional via a setting in the Browse Mode settings dialog. (#414)  
* When trying to read the status bar (Desktop NVDA+end), If a real status bar object cannot be located, NVDA will instead resort to using the bottom line of text written to the display for the active application. (#649)
* When reading with say all in browse mode documents, NVDA will now pause at the end of headings and other block-level elements, rather than speaking the text together with the next lot of text as one long sentence.
* In browse mode, pressing enter or space on a tab now activates it instead of switching to focus mode. (#1760)
* Updated eSpeak speech synthesizer to 1.45.47.

### Bug Fixes

* NVDA  no longer shows bullets or numbering for lists in Internet Explorer and other MSHTML controls when the author has indicated that these should not be shown (i.e. the list style is "none"). (#1671)
* Restarting NVDA when it has frozen (e.g. by pressing control+alt+n) no longer exits the previous copy without starting a new one.
* Pressing backspace or arrow keys in a Windows command console no longer causes strange results in some cases. (#1612)
* The selected item in WPF combo boxes (and possibly some other combo boxes exposed using UI Automation) which do not allow text editing is now reported correctly.
* In browse mode in Adobe Reader, it is now always possible to move to the next row from the header row and vice versa using the move to next row and move to previous row commands. Also, the header row is no longer reported as row 0. (#1731)
* In browse mode in Adobe Reader, it is now possible to move to (and therefore past) empty cells in a table.
* Pointless position information (e.g. 0 of 0 level 0) is no longer reported in braille.
* When braille is tethered to review, it is now able to show  content in flat review. (#1711)
* A text control's text is no longer presented twice on a braille display in some cases, e.g. scrolling back from the start of Wordpad documents.
* In browse mode in Internet Explorer, pressing enter on a file upload button now correctly presents the dialog to choose a file to upload instead of switching to focus mode. (#1720)
* Dynamic content changes such as in Dos consoles are no longer announced if  sleep mode for that application is currently on. (#1662)
* In browse mode, the behaviour of alt+upArrow and alt+downArrow to collapse and expand combo boxes has been improved. (#1630)
* NVDA now recovers from many more situations such as applications that stop responding which previously caused it to freeze completely. (#1408)
* For Mozilla Gecko (Firefox etc) browse mode documents NVDA will no longer fail to render text in a very specific situation where an element is styled as display:table. (#1373)
* NVDA will no longer announce label controls when focus moves inside of them. Stops double announcements of labels for some form fields in Firefox (Gecko) and Internet Explorer (MSHTML). (#1650)
* NVDA no longer fails to read a cell in Microsoft Excel after pasting in to it with control+v. (#1781)
* In Adobe Reader, extraneous information about the document is no longer announced when moving to a control on a different page in focus mode. (#1659)
* In browse mode in Mozilla Gecko applications (e.g. Firefox), toggle buttons are now detected and reported correctly. (#1757)
* NVDA can now   correctly read the Windows Explorer Address Bar in Windows 8 developer preview.
* NVDA will no longer crash apps such as winver and wordpad in Windows 8 developer preview due to bad glyph translations.
* In browse mode in applications using Mozilla Gecko 10 and later (e.g. Firefox 10), the cursor is more often positioned correctly when loading a page with a target anchor. (#360)
* In browse mode in Mozilla Gecko applications (e.g. Firefox), labels for image maps are now rendered.
* With mouse tracking enabled, moving the mouse over certain editable text fields (such as in Synaptics Pointing Device Settings and SpeechLab SpeakText) no longer causes the application to crash. (#672)
* NVDA now functions correctly in several about dialogs in applications distributed with Windows XP, including the About dialog in Notepad and the About Windows dialog. (#1853, #1855)
* Fixed reviewing by word in Windows Edit controls. (#1877)
* Moving out of an editable text field with leftArrow, upArrow or pageUp while in focus mode now correctly switches to browse mode when automatic focus mode for caret movement is enabled. (#1733)

### Promene za programere (engleski)

* NVDA can now instruct speech synthesizers to switch languages for particular sections of speech.
 * To support this, drivers must handle speech.LangChangeCommand in sequences past to SynthDriver.speak().
 * SynthDriver objects should also provide the language argument to VoiceInfo objects (or override the language attribute to retrieve the current language). Otherwise, NVDA's user interface language will be used.

## 2011.2

Highlights of this release include major improvements concerning punctuation and symbols, including configurable levels, custom labelling and character descriptions; no pauses at the end of lines during say all; improved support for ARIA in Internet Explorer; better support for XFA/LiveCycle PDF documents in Adobe Reader; access to text written to the screen in more applications; and access to formatting and color information for text written to the screen.

### New Features

* It is now possible to hear the description for any given character by pressing the review current character script twice in quick succession.  For English characters this is the standard English phonetic alphabet. For pictographic languages such as traditional Chinese, one or more example phrases using the given symbol are provided. Also pressing review current word or review current line three times will spell the word/line using the first of these descriptions. (#55)
* More text can be seen in flat review for applications such as Mozilla Thunderbird that write their text directly to the display as glyphs.
* It is now possible to choose from several levels of punctuation and symbol announcement. (#332)
* When punctuation or other symbols are repeated more than four times, the number of repetitions is now announced instead of speaking the repeated symbols. (#43)
* New braille translation tables: Norwegian 8 dot computer braille, Ethiopic grade 1, Slovene grade 1, Serbian grade 1. (#1456)
* Speech no longer unnaturally pauses at the end of each line when using the say all command. (#149)
* NVDA will now announce whether something is sorted (according to the aria-sort property) in web browsers. (#1500)
* Unicode Braille Patterns are now displayed correctly on braille displays. (#1505)
* In Internet Explorer and other MSHTML controls when focus moves inside a group of controls (surrounded by a fieldset), NVDA will now announce the name of the group (the legend). (#535)
* In Internet Explorer and other MSHTML controls, the aria-labelledBy and aria-describedBy properties are now honoured.
* in Internet Explorer and other MSHTML controls, support for ARIA list, gridcell, slider and progressbar controls has been improved.
* Users can now change the pronunciation of punctuation and other symbols, as well as the symbol level at which they are spoken. (#271, #1516)
* In Microsoft Excel, the name of the active sheet is now reported when switching sheets with control+pageUp or control+pageDown. (#760)
* When navigating a table in Microsoft Word with the tab key NVDA will now announce the current cell as you move. (#159)
* You can now configure whether table cell coordinates are reported from the Document Formatting preferences dialog. (#719)
* NVDA can now detect formatting and color for text written to the screen.
* In the Outlook Express/Windows Mail/Windows Live Mail message list, NVDA will now announce the fact that a message is unread and also if it's expanded or collapsed in the case of conversation threads. (#868)
* eSpeak now has a rate boost setting which triples the speaking rate.
* Support for the  calendar control found in the Date and Time Information dialog accessed from the  Windows 7 clock. (#1637)
* Additional key bindings have been added for the MDV Lilli braille display. (#241)
* New languages: Bulgarian, Albanian.

### Changes

* To move the caret to the review cursor, now press the move focus to navigator object script (desktop NVDA+shift+numpadMinus, laptop NVDA+shift+backspace) twice in quick succession. This frees up more keys on the keyboard. (#837)
* To hear the  decimal and hexadecimal representation of the character under the review cursor, now press review current character three times rather than twice, as twice now speaks the character description.
* Updated eSpeak speech synthesiser to 1.45.03. (#1465)
* Layout tables are no longer announced in Mozilla Gecko applications while moving the focus when in focus mode or outside of a document.
* In Internet Explorer and other MSHTML controls, browse mode now works for documents inside ARIA applications. (#1452)
* Updated liblouis braille translator to 2.3.0.
* When in browse mode  and jumping to a control with quicknav or focus, the description of the control is now announced if it has one.
* Progress bars are now announced in brows mode.
* Nodes marked with an ARIA role of presentation in Internet Explorer and other MSHTML controls are now filtered out of simple review and the focus ancestry.
* NVDA's user interface and documentation now refer to virtual buffers as browse mode, as the term "virtual buffer" is rather meaningless to most users. (#1509)
* When the user wishes to copy their user settings to the system profile for use on the logon screen, etc., and their settings contain custom plugins, they are now warned that this could be a security risk. (#1426)
* The NVDA service no longer starts and stops NVDA on user input desktops.
* On Windows XP and Windows Vista, NVDA no longer makes use of UI Automation even if it is available via the platform update. Although using UI Automation can improve the accessibility of some modern applications, on XP and Vista there were too many freezes, crashes and over all performance loss while using it. (#1437)
* In applications using Mozilla Gecko 2 and later (such as Firefox 4 and later), a document can now be read in browse mode before it is fully finished loading.
* NVDA now announces the state of a container when focus moves to a control inside it (e.g. if focus moves inside a document that is still loading it will report it as busy).
* NVDA's user interface and documentation no longer use the terms "first child" and "parent" with respect to object navigation, as these terms are confusing for many users.
* Collapsed is no longer reported for some menu items which have sub-menus.
* The reportCurrentFormatting script (NVDA+f) now reports the formatting at the position of the review cursor rather than the system caret / focus. As  by default the review cursor follows the caret, most people should not notice a difference. However this now enables the user to find out the formatting when moving the review cursor, such as in flat review.

### Bug Fixes

* Collapsing combo boxes in browse mode documents when focus mode has been forced with NVDA+space no longer auto-switches back to browse mode. (#1386)
* In Gecko (e.g. Firefox) and MSHTML (e.g. Internet Explorer) documents, NVDA now correctly renders certain text on the same line which was previously rendered on separate lines. (#1378)
* When Braille is tethered to review and the navigator object is moved to a browse mode document, either manually or due to a focus change, braille will appropriately show the browse mode content. (#1406, #1407)
* When speaking of punctuation is disabled, certain punctuation is no longer incorrectly spoken when using some synthesisers. (#332)
* Problems no longer occur when loading configuration for synthesisers which do not support the voice setting such as Audiologic Tts3. (#1347)
* The Skype Extras menu is now read correctly. (#648)
* Checking the Brightness controls volume checkbox in the Mouse Settings dialog should no longer cause a major lag for beeps when moving the mouse around the screen on Windows Vista/Windows 7 with Aero enabled. (#1183)
* When NVDA is configured to use the laptop keyboard layout, NVDA+delete now works as documented to report the dimensions of the current navigator object. (#1498)
* NVDA now Appropriately honours the aria-selected attribute in Internet Explorer documents.
* When NVDA automatically switches to focus mode in browse mode documents, it now announces information about the context of the focus. For example, if a list box item receives focus, the list box will be announced first. (#1491)
* In Internet Explorer and other MSHTML controls, ARIA listbox controls are now treeted as lists, rather than list items.
* When a read-only editable text control receives focus, NVDA now reports that it is read-only. (#1436)
* In browse mode, NVDA now behaves correctly with respect to read-only editable text fields.
* In browse mode documents, NVDA no longer incorrectly switches out of focus mode when aria-activedescendant is set; e.g. when the completion list appeared in some auto complete controls.
* In Adobe Reader, the name of controls is now reported when moving focus or using quick navigation in browse mode.
* In XFA PDF documents in Adobe Reader, buttons, links and graphics are now rendered correctly.
* In XFA PDF documents in Adobe Reader, all elements are now rendered on separate lines. This change was made because large sections (sometimes even the entire document) were being rendered without breaks due to the general lack of structure in these documents.
* Fixed problems when moving focus to or away from editable text fields in XFA PDF documents in Adobe Reader.
* In XFA PDF documents in Adobe Reader, changes to the value of a focused combo box will now be reported.
* Owner-drawn Combo boxes such as the ones to choose colors in Outlook Express are now accessible with NVDA. (#1340)
* In languages which use a space as a digit group/thousands separator such as French and German, numbers from separate chunks of text are no longer pronounced as a single number. This was particularly problematic for table cells containing numbers. (#555)
* nodes with an ARIA role of description in Internet Explorer and other MSHTML controls now are classed as static text, not edit fields.
* Fixed various issues when pressing tab while focus is on a document in browse mode (e.g. tab inappropriately moving to the address bar in Internet Explorer). (#720, #1367)
* When entering lists while reading text, NVDA now says, for example, "list with 5 items" instead of "listwith 5 items". (#1515)
* In input help mode, gestures are logged even if their scripts bypass input help such as the scroll braille display forward and back commands.
* In input help mode, when a modifier is held down on the keyboard, NVDA no longer reports the modifier as if it is modifying itself; e.g. NVDA+NVDA.
* In Adobe Reader documents, pressing c or shift+c to navigate to a combo box now works.
* The selected state of selectable table rows is now reported the same way it is for list and tree view items.
* Controls in Firefox and other Gecko applications can now be activated while in browse mode even if their content has been floated off-screen. (#801)
* You can no longer show an NVDA settings dialog while a message dialog is being shown, as the settings dialog was frozen in this case. (#1451)
* In Microsoft Excel, there is no longer a lag when holding down or rapidly pressing keys to move between or select cells.
* Fixed intermittent crashes of the NVDA service which meant that NVDA stopped running on secure Windows screens.
* Fixed problems that sometimes occurred with braille displays when a change caused text that was being displayed to disappear. (#1377)
* The downloads window in Internet Explorer 9 can now be navigated and read with NVDA. (#1280)
* It is no longer possible to accidentally start multiple copies of NVDA at the same time. (#507)
* On slow systems, NVDA no longer inappropriately causes its main window to be shown all the time while running. (#726)
* NVDA no longer crashes on Windows xP when starting a WPF application. (#1437)
* Say all and say all with review are now able to work in UI automation text controls that support all required functionality. For example, you can now use say all with review on XPS Viewer documents.
* NVDA no longer inappropriately classes some list items in the Outlook Express / Windows Live Mail message rules Apply Now dialog as being checkboxes. (#576)
* Combo boxes are no longer reported as having a sub-menu.
* NVDA is  now able to read the recipiants in the To, CC and BCC fields in Microsoft Outlook. (#421)
* Fixed the issue in NVDA's Voice Settings dialog where the value of sliders was sometimes not reported when changed. (#1411)
* NVDA no longer fails to announce the new cell when moving in an Excel spreadsheet after cutting and pasting. (#1567)
* NVDA no longer becomes worse at guessing color names the more colors it announces.
* In Internet Explorer and other MSHTML controls, fixed the inability to read parts of rare pages which contain iframes marked with an ARIA role of presentation. (#1569)
* In Internet Explorer and other MSHTML controls, fixed a rare problem where the focus kept bouncing infinitely between the document and a multi-line editable text field in focus mode. (#1566)
* In Microsoft Word 2010 NVDA will now automatically read confirmation dialogs. (#1538)
* In multi-line editable text fields in Internet Explorer and other MSHTML controls, selection on lines after the first is now reported correctly. (#1590)
* Improved moving by word in many cases, including browse mode and Windows Edit controls. (#1580)
* The NVDA installer no longer shows garbled text for Hong Kong versions of Windows Vista and Windows 7. (#1596)
* NVDA no longer fails to load the Microsoft Speech API version 5 synthesizer if the configuration contains settings for that synthesizer but is missing the voice setting. (#1599)
* In editable text fields in Internet Explorer and other MSHTML controls, NVDA no longer lags or freezes when braille is enabled.
* In firefox brows mode, NVDA no longer refuses to include content that is inside a focusable node with an ARIA role of presentation.
* In Microsoft Word with braille enabled, lines on pages after the first page are now reported correctly. (#1603)
* In Microsoft Word 2003, lines of right-to-left text can once again be read with braille enabled. (#627)
* In Microsoft Word, say all now works correctly when the document does not end with a sentence ending.
* When opening a plain text message in Windows Live Mail 2011, NVDA will correctly focus on the message document allowing it to be read.
* NVDA no longer temporarily freezes or refuses to speak when in the Move to / Copy to dialogs in Windows Live Mail. (#574)
* In Outlook 2010, NVDA will now correctly track the focus in the message list. (#1285)
* Some USB connection issues have been resolved with the MDV Lilli braille display. (#241)
* In Internet explorer and other MSHTML controls, spaces are no longer ignored in browse mode in certain cases (e.g. after a link).
* In Internet Explorer and other MSHTML controls, some extraneous line breaks have been eliminated in browse mode. specifically, HTML elements with a display style of None no longer force a line break. (#1685)
* If NVDA is unable to start, failure to play the Windows critical stop sound no longer clobbers the critical error message in the log file.

### Promene za programere (engleski)

* Developer documentation can now be generated using SCons. See readme.txt at the root of the source distribution for details, including associated dependencies.
* Locales can now provide descriptions for characters. See the Character Descriptions section of the Developer Guide for details. (#55)
* Locales can now provide information about the pronunciation of specific punctuation and other symbols. See the Symbol Pronunciation section of the Developer Guide for details. (#332)
* You can now build NVDAHelper with several debugging options using the nvdaHelperDebugFlags SCons variable. See readme.txt at the root of the source distribution for details. (#1390)
* Synth drivers are now passed a sequence of text and speech commands to speak, instead of just text and an index.
 * This allows for embedded indexes, parameter changes, etc.
 * Drivers should implement SynthDriver.speak() instead of SynthDriver.speakText() and SynthDriver.speakCharacter().
 * The old methods will be used if SynthDriver.speak() is not implemented, but they are deprecated and will be removed in a future release.
* gui.execute() has been removed. wx.CallAfter() should be used instead.
* gui.scriptUI has been removed.
 * For message dialogs, use wx.CallAfter(gui.messageBox, ...).
 * For all other dialogs, real wx dialogs should be used instead.
 * A new gui.runScriptModalDialog() function simplifies using modal dialogs from scripts.
* Synth drivers can now support boolean settings. See SynthDriverHandler.BooleanSynthSetting.
* SCons now accepts a certTimestampServer variable specifying the URL of a timestamping server to use to timestamp authenticode signatures. (#1644)

## 2011.1.1

This release fixes several security and other important issues found in NVDA 2011.1.

### Bug Fixes

* The Donate item in the NVDA menu is now disabled when running on the logon, lock, UAC and other secure Windows screens, as this is a security risk. (#1419)
* It is now impossible to copy or paste within NVDA's user interface while on secure desktops (lock screen, UAC screen and windows logon) as this is a security risk. (#1421)
* In Firefox 4, the move to containing virtual buffer command (NVDA+control+space) now works as it should to escape embedded objects such as Flash content. (#1429)
* When speaking of command keys is enabled, shifted characters are no longer incorrectly spoken as command keys. (#1422)
* When speaking of command keys is enabled, pressing space with modifiers other than shift (such as control and alt) is now reported as a command key. (#1424)
* Logging is now completely disabled when running on the logon, lock, UAC and other secure Windows screens, as this is a security risk. (#1435)
* In input help mode, Gestures are now logged even if they are not bound to a script (in accordance with the user guide). (#1425)

## 2011.1

Highlights of this release include automatic reporting of new text output in mIRC, PuTTY, Tera Term and SecureCRT; support for global plugins; announcement of bullets and numbering in Microsoft Word; additional key bindings for braille displays, including keys to move to the next and previous line; support for several Baum, HumanWare and APH braille displays; and reporting of colors for some controls, including IBM Lotus Symphony text controls.

### New Features

* Colors can now be reported for some controls. Automatic announcement can be configured in the Document Formatting preferences dialog. It can also be reported on demand using the report text formatting command (NVDA+f).
 * Initially, this is supported in standard IAccessible2 editable text controls (such as in Mozilla applications), RichEdit controls (such as in Wordpad) and IBM Lotus Symphony text controls.
* In virtual buffers, you can now select by page (using shift+pageDown and shift+pageUp) and paragraph (using shift+control+downArrow and shift+control+upArrow). (#639)
* NVDA now automatically reports new text output in mIRC, PuTTY, Tera Term and SecureCRT. (#936)
* Users can now add new key bindings or override existing ones for any script in NVDA by providing a single user input gesture map. (#194)
* Support for global plugins. Global plugins can add new functionality to NVDA which works across all applications. (#281)
* A small beep is now heard when typing characters with the shift key while capslock is on. This can be turned off by unchecking the related new option in the Keyboard settings dialog. (#663)
* hard page breaks are now announced when moving by line in Microsoft Word. (#758)
* Bullets and numbering are now spoken in Microsoft Word when moving by line. (#208)  
* A command to toggle Sleep mode for the current application (NVDA+shift+s) is now available. Sleep mode (previously known as self voicing mode) disables all screen reading functionality in NVDA for a particular application. Very useful for applications that provide their own speech and or screen reading features. Press this command again to disable Sleep mode.
* Some additional braille display key bindings have been added. See the Supported Braille Displays section of the User Guide for details. (#209)
* For the convenience of third party developers, app modules as well as global plugins can now be reloaded without restarting NVDA. Use tools -> Reload plugins in the NVDA menu or NVDA+control+f3. (#544)
* NVDA now remembers the position you were at when returning to a previously visited web page. This applies until either the browser or NVDA is exited. (#132)
* Handy Tech braille displays can now be used without installing the Handy Tech universal driver. (#854)
* Support for several Baum, HumanWare and APH braille displays. (#937)
* The status bar in Media Player Classic Home Cinema is now recognised.
* The Freedom Scientific Focus 40 Blue braille display can now be used when connected via bluetooth. (#1345)

### Changes

* Position information is no longer reported by default in some cases where it was usually incorrect; e.g. most menus, the Running Applications bar, the Notification Area, etc. However, this can be turned on again by an added option in the Object Presentation settings dialog.
* Keyboard help has been renamed to input help to reflect that it handles input from sources other than the keyboard.
* Input Help no longer reports a script's code location via speech and braille as it is cryptic and irrelevant to the user. However, it is now logged for developers and advanced users.
* When NVDA detects that it has frozen, it continues to intercept NVDA modifier keys, even though it passes all other keys through to the system. This prevents the user from unintentionally toggling caps lock, etc. if they press an NVDA modifier key without realising NVDA has frozen. (#939)
* If keys are held down after using the pass next key through command, all keys (including key repeats) are now passed through until the last key is released.
* If an NVDA modifier key is pressed twice in quick succession to pass it through and the second press is held down, all key repeats will now be passed through as well.
* The volume up, down and mute keys are now reported in input help. This could be helpful if the user is uncertain as to what these keys are.
* The hotkey for the Review Cursor item in the NVDA Preferences menu has been changed from r to c to eliminate the conflict with the Braille Settings item.

### Bug Fixes

* When adding a new speech dictionary entry, the title of the dialog is now "Add dictionary entry" instead of "Edit dictionary entry". (#924)
* In speech dictionary dialogs, the content of the Regular expression and Case sensitive columns of the Dictionary entries list is now presented in the configured NVDA language instead of always in English.
* In AIM, position information is now announced in tree views.
* On sliders in the Voice Settings dialog, up arrow/page up/home now increase the setting and down arrow/page down/end decrease it. Previously, the opposite occurred, which is not logical and is inconsistent with the synth settings ring. (#221)
* In virtual buffers with screen layout disabled, some extraneous blank lines no longer appear.
* If an NVDA modifier key is pressed twice quickly but there is an intervening key press, the NVDA modifier key is no longer passed through on the second press.
* Punctuation keys are now spoken in input help even when speaking of punctuation is disabled. (#977)
* In the Keyboard Settings dialog, the keyboard layout names are now presented in the configured NVDA language instead of always in English. (#558)
* Fixed an issue where some items were rendered as empty in Adobe Reader documents; e.g. the links in the table of contents of the Apple iPhone IOS 4.1 User Guide.
* The "Use currently saved settings on the logon and other secure screens" button in NVDA's General Settings dialog now works if used immediately after NVDA is newly installed but before a secure screen has appeared. Previously, NVDA reported that copying was successful, but it actually had no effect. (#1194)
* It is no longer possible to have two NVDA settings dialogs open simultaneously. This fixes issues where one open dialog depends on another open dialog; e.g. changing the synthesiser while the Voice Settings dialog is open. (#603)
* On systems with UAC enabled, the "Use currently saved settings on the logon and other secure screens" button in NVDA's General Settings dialog no longer fails after the UAC prompt if the user's account name contains a space. (#918)
* In Internet Explorer and other MSHTML controls, NVDA now uses the URL as a last resort to determine the name of a link, rather than presenting empty links. (#633)
* NVDA no longer ignores the focus  in AOL Instant Messenger 7 menus. (#655)
* Announce the correct label for errors in the Microsoft Word Spell Check dialog (e.g. Not in dictionary, Grammar error, punctuation). Previously  they were all announced as grammar error. (#883)
* Typing in Microsoft Word while using a braille display should no longer cause garbled text to be typed, and a rare freeze when pressing a braille routing key in Word documents has been fixed. (#1212) However a limitation is that Arabic text can no longer be read in Word 2003 and below, while using a braille display. (#627)
* When pressing the delete key in an edit field, the text/cursor on a braille display should now always be updated appropriately to reflect the change. (#947)
* Changes on dynamic pages in Gecko2 documents (E.g. Firefox 4) while multiple tabs are open are now properly reflected by NVDA. Previously only changes in the first tab were reflected. (Mozilla bug 610985)
* NVDA can now properly announce the suggestions for grammar and punctuation errors in Microsoft Word spell check dialog. (#704)
* In Internet Explorer and other MSHTML controls, NVDA no longer presents destination anchors as empty links in its virtual buffer. Instead, these anchors are hidden as they should be. (#1326)
* Object navigation around and within standard groupbox windows is no longer broken and asymmetrical.
* In Firefox and other Gecko-based controls, NVDA will no longer get stuck in a subframe if it finishes loading before the outer document.
* NVDA  now appropriately announces the next character when deleting a character with numpadDelete. (#286)
* On the Windows XP logon screen, the user name is once again reported when the selected user is changed.
* Fixed problems when reading text in Windows command consoles with reporting of line numbers enabled.
* The Elements List dialog for virtual buffers is now usable by sighted users. All controls are visible on screen. (#1321)
* The list of entries in the Speech Dictionary dialog is now more readable by sighted users. The list is now large enough to show all of its columns on screen. (#90)
* On ALVA BC640/BC680 braille displays, NVDA no longer disregards display keys that are still held down after another key is released.
* Adobe Reader X no longer crashes after leaving the untagged document options before the processing dialog appears. (#1218)
* NVDA now switches to the appropriate braille display driver when you revert to saved configuration. (#1346)
* The Visual Studio 2008 Project Wizard is read correctly again. (#974)
* NVDA no longer completely fails to work in applications which contain non-ASCII characters in their executable name. (#1352)
* When reading by line in AkelPad with word wrap enabled, NVDA no longer reads the first character of the following line at the end of the current line.
* In the Visual Studio 2005/2008 code editor, NVDA no longer reads the entire text after every typed character. (#975)
* Fixed the issue where some braille displays weren't cleared properly when NVDA was exited or the display was changed.
* The initial focus is no longer sometimes spoken twice when NVDA starts. (#1359)

### Promene za programere (engleski)

* SCons is now used to prepare the source tree and create binary builds, portable archives, installers, etc. See readme.txt at the root of the source distribution for details.
* The key names used by NVDA (including key maps) have been made more friendly/logical; e.g. upArrow instead of extendedUp and numpadPageUp instead of prior. See the vkCodes module for a list.
* All input from the user is now represented by an inputCore.InputGesture instance. (#601)
 * Each source of input subclasses the base InputGesture class.
 * Key presses on the system keyboard are encompassed by the keyboardHandler.KeyboardInputGesture class.
 * Presses of buttons, wheels and other controls on a braille display are encompassed by subclasses of the braille.BrailleDisplayGesture class. These subclasses are provided by each braille display driver.
* Input gestures are bound to ScriptableObjects using the ScriptableObject.bindGesture() method on an instance or an __gestures dict on the class which maps gesture identifiers to script names. See baseObject.ScriptableObject for details.
* App modules no longer have key map files. All input gesture bindings must be done in the app module itself.
* All scripts now take an InputGesture instance instead of a key press.
 * KeyboardInputGestures can be sent on to the OS using the send() method of the gesture.
* To send an arbitrary key press, you must now create a KeyboardInputGesture using KeyboardInputGesture.fromName() and then use its send() method.
* Locales may now provide an input gesture map file to add new bindings or override existing bindings for scripts anywhere in NVDA. (#810)
 * Locale gesture maps should be placed in locale\LANG\gestures.ini, where LANG is the language code.
 * See inputCore.GlobalGestureMap for details of the file format.
* The new LiveText and Terminal NVDAObject behaviors facilitate automatic reporting of new text. See those classes in NVDAObjects.behaviors for details. (#936)
 * The NVDAObjects.window.DisplayModelLiveText overlay class can be used for objects which must retrieve text written to the display.
 * See the mirc and putty app modules for usage examples.
* There is no longer an _default app module. App modules should instead subclass appModuleHandler.AppModule (the base AppModule class).
* Support for global plugins which can globally bind scripts, handle NVDAObject events and choose NVDAObject overlay classes. (#281) See globalPluginHandler.GlobalPlugin for details.
* On SynthDriver objects, the available* attributes for string settings (e.g. availableVoices and availableVariants)  are now OrderedDicts keyed by ID instead of lists.
* synthDriverHandler.VoiceInfo now takes an optional language argument which specifies the language of the voice.
* SynthDriver objects now provide a language attribute which specifies the language of the current voice.
 * The base implementation uses the language specified on the VoiceInfo objects in availableVoices. This is suitable for most synthesisers which support one language per voice.
* Braille display drivers have been enhanced to allow buttons, wheels and other controls to be bound to NVDA scripts:
 * Drivers can provide a global input gesture map to add bindings for scripts anywhere in NVDA.
 * They can also provide their own scripts to perform display specific functions.
 * See braille.BrailleDisplayDriver for details and existing braille display drivers for examples.
* The 'selfVoicing' property on AppModule classes has now been renamed to 'sleepMode'.
* The app module events event_appLoseFocus and event_appGainFocus have now been renamed to event_appModule_loseFocus and event_appModule_gainFocus, respectivly, in order to make the naming convention consistent with app modules and tree interceptors.
* All braille display drivers should now use braille.BrailleDisplayDriver instead of braille.BrailleDisplayDriverWithCursor.
 * The cursor is now managed outside of the driver.
 * Existing drivers need only change their class statement accordingly and rename their _display method to display.

## 2010.2

Notable features of this release include greatly simplified object navigation; virtual buffers for Adobe Flash content; access to many previously inaccessible controls by retrieving text written to the screen; flat review of screen text; support for IBM Lotus Symphony documents; reporting of table row and column headers in Mozilla Firefox; and significantly improved user documentation.

### New Features

* Navigating through objects with the review cursor has been greatly simplified. The review cursor now excludes objects which aren't useful to the user; i.e. objects only used for layout purposes and unavailable objects.
* In applications using the Java Access Bridge (including OpenOffice.org), formatting can now be reported in text controls. (#358, #463)
* When moving the mouse over cells in Microsoft Excel, NVDA will appropriately announce them.
* In applications using the Java Access Bridge, the text of a dialog is now reported when the dialog appears. (#554)
* A virtualBuffer can now be used to navigate adobe Flash content. Object navigation and interacting with the controls directly (by turning on focus mode) is still supported. (#453)
* Editable text controls in the Eclipse IDE, including the code editor, are now accessible. You must be using Eclipse 3.6 or later. (#256, #641)
* NVDA can now retrieve most text written to the screen. (#40, #643)
 * This allows for reading of controls which do not expose information in more direct/reliable ways.
 * Controls made accessible by this feature include: some menu items which display icons (e.g. the Open With menu on files in Windows XP) (#151), editable text fields in Windows Live applications (#200), the errors list in Outlook Express (#582), the editable text control in TextPad (#605), lists in Eudora, many controls in Australian E-tax and the formula bar in Microsoft Excel.
* Support for the code editor in Microsoft Visual Studio 2005 and 2008. At least Visual Studio Standard is required; this does not work in the Express editions. (#457)
* Support for IBM Lotus Symphony documents.
* Early experimental support for Google Chrome. Please note that Chrome's screen reader support is far from complete and additional work may also be required in NVDA. You will need a recent development build of Chrome to try this.
* The state of toggle keys (caps lock, num lock and scroll lock) is now displayed in braille when they are pressed. (#620)
* Help balloons are now displayed in braille when they appear. (#652)
* Added a driver for the MDV Lilli braille display. (#241)
* When selecting an entire row or column in Microsoft Excel with the shortcut keys shift+space and control+space, the new selection is now reported. (#759)
* Table row and column headers can now be reported. This is configurable from the Document Formatting preferences dialog.
 * Currently, this is supported in documents in Mozilla applications such as Firefox (version 3.6.11 and later) and Thunderbird (version 3.1.5 and later). (#361)
* Introduced commands for flat review: (#58)
 * NVDA+numpad7  switches to flat review, placing the review cursor at the position of the current object, allowing you  to review the screen (or a document if within one) with the text review commands.
 * NVDA+numpad1 moves the review cursor into the object represented by the text at  the position of the review cursor, allowing you to navigate by object from that point.
* Current NVDA user settings can be  copied to be used on secure Windows screens such as the logon and UAC screens by pressing a button in the General Settings dialog. (#730)
* Support for Mozilla Firefox 4.
* Support for Microsoft Internet Explorer 9.

### Changes

* The sayAll by Navigator object (NVDA+numpadAdd), navigator object next in flow (NVDA+shift+numpad6) and navigator object previous in flow (NVDA+shift+numpad4) commands have been removed for the time being, due to bugginess and to free up the keys for other possible features.
* In the NVDA Synthesizer dialog, only the display name of the synthesizer is now listed. Previously, it was prefixed by the driver's name, which is only relevant internally.
* When in embedded applications or virtual buffers inside another virtualBuffer (e.g. Flash), you can now  press nvda+control+space to move out of the embedded application or virtual buffer to the containing document. Previously nvda+space  was used for this. Now nvda+space is specifically only for toggling brows/focus modes on virtualBuffers.
* If the speech viewer (enabled under the tools menu) is given the focus (e.g. it was clicked in) new text will not appear in the control until focus is moved away. This allows for selecting the text with greater ease (e.g. for copying).
* The Log Viewer and Python Console are maximised when activated.
* When focusing on a worksheet in Microsoft Excel and there is more than one cell selected, the selection range is announced, rather than just the active cell. (#763)
* Saving configuration and changing of particular sensitive options is now disabled when running on the logon, UAC and other secure Windows screens.
* Updated eSpeak speech synthesiser to 1.44.03.
* If NVDA is already running, activating the NVDA shortcut on the desktop (which includes pressing control+alt+n) will restart NVDA.
* Removed the report text under the mouse checkbox from the Mouse settings dialog and replaced it with an Enable mouse tracking checkbox, which better matches the toggle mouse tracking script (NVDA+m). 
* Updates to the laptop keyboard layout so that it includes all commands available in the desktop layout and works correctly on non-English keyboards. (#798, #800)
* Significant improvements and updates to the user documentation, including documentation of the laptop keyboard commands and synchronisation of the Keyboard Commands Quick Reference with the User Guide. (#455)
* Updated liblouis braille translator to 2.1.1. Notably, this fixes some issues related to Chinese braille as well as characters which are undefined in the translation table. (#484, #499)

### Bug Fixes

* In µTorrent, the focused item in the torrents list no longer reports repeatedly or steals focus when a menu is open.
* In µTorrent, the names of the files in the Torrent Contents list are now reported.
* In Mozilla applications, focus is now correctly detected when it lands on an empty table or tree.
* In Mozilla applications, "not checked" is now correctly reported for checkable controls such as checkable table cells. (#571)
* In Mozilla applications, the text of correctly implemented ARIA dialogs is no longer ignored and will now be reported when the dialog appears. (#630)
* in Internet Explorer and other MSHTML controls, the ARIA level attribute is now  honoured correctly.
* In Internet Explorer and other MSHTML controls, the ARIA role is now chosen over other type information to give a much more correct and predictable ARIA experience.
* Stopped a rare crash in Internet Explorer when navigating through frames or iFrames.
* In Microsoft Word documents, right-to-left lines (such as Arabic text) can be read again. (#627)
* Greatly reduced lag when large amounts of text are displayed in a Windows command console on 64-bit systems. (#622)
* If Skype is already started when NVDA starts, it is no longer necessary to restart Skype to enable accessibility. This may also be true for other applications which check the system screen reader flag.
* In Microsoft Office applications, NVDA no longer crashes when speak foreground (NVDA+b) is pressed or when navigating some objects on toolbars. (#616)
* Fixed incorrect speaking of numbers containing a 0 after a separator; e.g. 1,023. (#593)
* Adobe Acrobat Pro and Reader 9 no longer crash when closing a file or performing certain other tasks. (#613)
* The selection is now announced when control+a is pressed to select all text in some editable text controls such as in Microsoft Word. (#761)
* In Scintilla controls (e.g. Notepad++), text is no longer incorrectly selected when NVDA moves the caret such as during say all. (#746)
* It is again possible to review the contents of cells in Microsoft Excel with the review cursor.
* NVDA can again read by line in certain problematic textArea fields in Internet Explorer 8. (#467)
* Windows Live Messenger 2009 no longer exits immediately after it is started while NVDA is running. (#677)
* In web browsers, It is no longer necessary to press tab to interact with an embedded object (such as Flash content) after pressing enter on the embedded object or returning from another application. (#775)
* In Scintilla controls (e.g. Notepad++), the beginning of long lines is no longer truncated when it scrolls off the screen. Also, these long lines will be correctly displayed in braille when they are selected.
* In Loudtalks, it is now possible to access the contact list.
* The URL of the document and "MSAAHTML Registered Handler" are no longer sometimes spuriously reported in Internet Explorer and other MSHTML controls. (#811)
* In tree views in the Eclipse IDE, the previously focused item is no longer incorrectly announced when focus moves to a new item.
* NVDA now functions correctly on a system where the current working directory has been removed from the DLL search path (by setting the CWDIllegalInDllSearch registry entry to 0xFFFFFFFF). Note that this is not relevant to most users. (#907)
* When the table navigation commands are used outside of a table in Microsoft Word, "edge of table" is no longer spoken after "not in table". (#921)
* When the table navigation commands cannot move due to being at the edge of a table in Microsoft Word, "edge of table" is now spoken in the configured NVDA language rather than always in English. (#921)
* In Outlook Express, Windows Mail and Windows Live Mail, the state of the checkboxes in message rules lists is now reported. (#576)
* The description of message rules can now be read in Windows Live Mail 2010.

## 2010.1

This release focuses primarily on bug fixes and improvements to the user experience, including some significant stability fixes.

### New Features

* NVDA no longer fails to start on a system with no audio output devices. Obviously, a braille display or the Silence synthesiser in conjunction with the Speech Viewer will need to be used for output in this case. (#425)
* A report landmarks checkbox has been added to the Document Formatting settings dialog which allows you to configure whether NVDA should announce landmarks in web documents. For compatibility with the previous release, the option is on by default.
* If speak command keys is enabled, NVDA will now announce the names of multimedia keys (e.g. play, stop, home page, etc.) on many keyboards when they are pressed. (#472)
* NVDA now announces the word being deleted when pressing control+backspace in controls that support it. (#491)
* Arrow keys can now be used in the Web formator window to navigate and read the text. (#452)
* The entry list in the Microsoft Office Outlook address book is now supported.
* NVDA better supports embedded editable (design mode) documents in Internet Explorer. (#402)
* a new script (nvda+shift+numpadMinus) allows you to move the system focus to the current navigator object.
* New scripts to lock and unlock the left and right mouse buttons. Useful for performing drag and drop operations. shift+numpadDivide to lock/unlock the left, shift+numpadMultiply to lock/unlock the right.
* New braille translation tables: German 8 dot computer braille, German grade 2, Finnish 8 dot computer braille, Chinese (Hong Kong, Cantonese), Chinese (Taiwan, Manderin). (#344, #369, #415, #450)
* It is now possible to disable the creation of the desktop shortcut (and thus the shortcut key) when installing NVDA. (#518)
* NVDA can now use IAccessible2 when present in 64 bit applications. (#479)
* Improved support for live regions in Mozilla applications. (#246)
* The NVDA Controller Client API is now provided to allow applications to control NVDA; e.g. to speak text, silence speech, display a message in Braille, etc.
* Information and error messages are now read in the logon screen in Windows Vista and Windows 7. (#506)
* In Adobe Reader, PDF interactive forms developed with Adobe LiveCycle are now supported. (#475)
* In Miranda IM, NVDA now automatically reads incoming messages in chat windows if reporting of dynamic content changes is enabled. Also, commands have been added to report the three most recent messages (NVDA+control+number). (#546)
* Input text fields are now supported in Adobe Flash content. (#461)

### Changes

* The extremely verbose keyboard help message in the Windows 7 Start menu is no longer reported.
* The Display synth has now been replaced with a new Speech Viewer. To activate it, choose Speech Viewer from the Tools menu. The speech viewer can be used independently of what ever speech synthesizer you are using. (#44)
* Messages on the braille display will automatically be dismissed if the user presses a key that results in a change such as the focus moving. Previously the message would always stay around for its configured time.
* Setting whether braille should be tethered to the focus or the review cursor (NVDA+control+t) can now be also set from the braille settings dialog, and is also now saved in the user's configuration.
* Updated eSpeak speech synthesiser to 1.43.
* Updated liblouis braille translator to 1.8.0.
* In virtual buffers, the reporting of elements when moving by character or word has been greatly improved. Previously, a lot of irrelevant information was reported and the reporting was very different to that when moving by line. (#490)
* The Control key now simply stops speech like other keys, rather than pausing speech. To pause/resume speech, use the shift key.
* Table row and column counts are no longer announced when reporting focus changes, as this announcement is rather verbose and usually not useful.

### Bug Fixes

* NVDA no longer fails to start if UI Automation support appears to be available but fails to initialise for some reason. (#483)
* The entire contents of a table row is no longer sometimes reported when moving focus inside a cell  in Mozilla applications. (#482)
* NVDA no longer lags for a long time when expanding tree view items that contain a very large amount of sub-items.
* When listing SAPI 5 voices, NVDA now tries to detect buggy voices and excludes them from the Voice Settings dialog and synthesiser settings ring. Previously, when there was just one problematic voice, NVDA's SAPI 5 driver would sometimes fail to start.
* Virtual buffers now honour the report object shortcut keys setting found in the Object Presentation dialog. (#486)
* In virtual buffers, row/column coordinates are no longer incorrectly read for row and column headers when reporting of tables is disabled.
* In virtual buffers, row/column coordinates are now correctly read when you leave a table and then re-enter the same table cell without visiting another cell first; e.g. pressing upArrow then downArrow on the first cell of a table. (#378)
* Blank lines in Microsoft Word documents and  Microsoft HTML edit controls are now shown appropriately on braille displays. Previously NVDA was displaying the current sentence on the display, not the current line for these situations. (#420)
* Multiple security fixes when running NVDA at Windows logon and on other secure desktops. (#515)
* The cursor position (caret) is now correctly updated when performing a Say All that goes off the bottom of the screen, in standard Windows edit fields and Microsoft Word documents. (#418)
* In virtual buffers, text is no longer incorrectly included for images inside links and clickables that are marked as being irrelevant to screen readers. (#423)
* Fixes to the laptop keyboard layout. (#517)
* When Braille is tethered to review when you focus on a Dos console window, the review cursor can now properly navigate the text in the console.
* While working with TeamTalk3 or TeamTalk4 Classic, the VU meter progress bar in the main window is no longer announced as it updates. Also, special characters can be read properly in the incoming chat window.
* Items are no longer spoken twice in the Windows 7 Start Menu. (#474)
* Activating same-page links in Firefox 3.6 appropriately moves the cursor in the virtualBuffer to the correct place on the page.
* Fixed the issue where some text was not rendered in Adobe Reader in certain PDF documents.
* NVDA no longer incorrectly speaks certain numbers separated by a dash; e.g. 500-1000. (#547)
* In Windows XP, NVDA no longer causes Internet Explorer to freeze when toggling checkboxes in Windows Update. (#477)
* When using the in-built eSpeak synthesiser, simultaneous speech and beeps no longer intermittently cause freezes on some systems. This was most noticeable, for example, when copying large amounts of data in Windows Explorer.
* NVDA no longer announces that a Firefox document has become busy (e.g. due to an update or refresh) when that document is in the background. This also caused the status bar of the foreground application to be spuriously announced.
* When switching Windows keyboard layouts (with control+shift or alt+shift), the full name of the layout is reported in both speech and braille. Previously it was only reported in speech, and alternative layouts (e.g. Dvorak) were not reported at all.
* If reporting of tables is disabled, table information is no longer announced when the focus changes.
* Certain standard tree view controls in 64 bit applications (e.g. the Contents tree view in Microsoft HTML Help) are now accessible. (#473)
* Fixed some problems with logging of messages containing non-ASCII characters. This could cause spurious errors in some cases on non-English systems. (#581)
* The information in the About NVDA dialog now appears in the user's configured language instead of always appearing in English. (#586)
* Problems are no longer encountered when using the synthesiser settings ring after the voice is changed to one which has less settings than the previous voice.
* In Skype 4.2, contact names are no longer spoken twice in the contact list.
* Fixed some potentially major memory leaks in the GUI and in virtual buffers. (#590, #591)
* Work around a nasty bug in some SAPI 4 synthesisers which was causing frequent errors and crashes in NVDA. (#597)

## 2009.1

Major highlights of this release include support for 64 bit editions of Windows; greatly improved support for Microsoft Internet Explorer and Adobe Reader documents; support for Windows 7; reading of the Windows logon, control+alt+delete and User Account Control (UAC) screens; and the ability to interact with Adobe Flash and Sun Java content on web pages. There have also been several significant stability fixes and improvements to the general user experience.

### New Features

* Official support for 64 bit editions of Windows! (#309)
* Added a synthesizer driver for the Newfon synthesizer. Note that this requires a special version of Newfon. (#206)
* In virtual buffers, focus mode and browse mode can now be reported using sounds instead of speech. This is enabled by default. It can be configured from the Virtual buffers dialog. (#244)
* NVDA no longer cancels speech when volume control keys are pressed on the keyboard, allowing the user to change the volume and listen to actual results immediately. (#287)
* Completely rewritten support for Microsoft Internet Explorer and Adobe Reader documents. This support has been unified with the core support used for Mozilla Gecko, so features such as fast page rendering, extensive quick navigation, links list, text selection, auto focus mode and braille support are now available with these documents.
* Improved support for the date selection control found in the Windows Vista Date / Time properties dialog.
* improved support for the Modern XP/Vista start menu (specifically the all programs, and places menus). Appropriate level information is now announced.
* The amount of text that is announced when moving the mouse is now configurable from the Mouse settings dialog. A choice of paragraph, line, word or character can be made.
* announce spelling errors under the cursor in Microsoft Word.
* support for the Microsoft Word 2007 spell checker. Partial support may be available for prior Microsoft Word versions.
* Better support for Windows Live Mail. Plain text messages can now be read and both the plain text and HTML message composers are useable.
* In Windows Vista, if the user moves to the secure desktop (either because a UAC control dialog appeared, or because control+alt+delete was pressed), NVDA will announce the fact that the user is now on the secure desktop.
* NVDA can announce text under the mouse within dos console windows.
* Support for UI Automation via the UI Automation client API available in Windows 7, as well as fixes to improve the experience of NVDA in Windows 7.
* NVDA can be configured to start automatically after you log on to Windows. The option is in the General Settings dialog.
* NVDA can read secure Windows screens such as the Windows logon, control+alt+delete and User Account Control (UAC) screens in Windows XP and above. Reading of the Windows logon screen can be configured from the General Settings dialog. (#97)
* Added a driver for the Optelec ALVA BC6 series braille displays.
* When browsing web documents, you can now press n and shift+n to skip forward and backward past blocks of links, respectively.
* When browsing web documents, ARIA landmarks are now reported, and you can move forward and backward through them using d and shift+d, respectively. (#192)
* The Links List dialog available when browsing web documents has now become an Elements List dialog which can list links, headings and landmarks. Headings and landmarks are presented hierarchically. (#363)
* The new Elements List dialog contains a "Filter by" field which allows you to filter the list to contain only those items including the text that was typed. (#173)
* Portable versions of NVDA now look in the 'userConfig' directory inside the NVDA directory, for the user's configuration. Like for the installer version, this keeps the user's configuration separate from NVDA itself.
* Custom app modules, braille display drivers and synth drivers can now be stored in the user's configuration  directory. (#337)
* Virtual buffers are now rendered in the background, allowing the user to interact with the system to some extent during the rendering process. The user will be notified that the document is being rendered if it takes longer than a second.
* If NVDA detects that it has frozen for some reason, it will automatically pass all keystrokes through so that the user has a better chance of recovering the system.
* Support for ARIA drag and drop in Mozilla Gecko. (#239)
* The document title and current line or selection is now spoken when you move focus inside a virtual buffer. This makes the behaviour when moving focus into virtual buffers consistent with that for normal document objects. (#210)
* In virtual buffers, you can now interact with embedded objects (such as Adobe Flash and Sun Java content) by pressing enter on the object. If it is accessible, you can then tab around it like any other application. To return focus to the document, press NVDA+space. (#431)
* In virtual buffers, o and shift+o move to the next and previous embedded object, respectively.
* NVDA can now fully access applications running as administrator in Windows Vista and later. You must install an official release of NVDA for this to work. This does not work for portable versions and snapshots. (#397)

### Changes

* NVDA no longer announces "NVDA started" when it starts.
* The startup and exit sounds are now played using NVDA's configured audio output device instead of the Windows default audio output device. (#164)
* Progress bar reporting has been improved. Most notably you can now configure NVDA to announce via both speech and beeps at the same time.
* Some generic roles, such as pane, application and frame, are no longer reported on focus unless the control is unnamed.
* The review copy command (NVDA+f10) copies the text from the start marker up to and including the current review position, rather than excluding the current position. This allows the last character of a line to be copied, which was not previously possible. (#430)
* the navigatorObject_where script (ctrl+NVDA+numpad5) has been removed. This key combination did not work on some keyboards, nore was the script found to be that useful.
* the navigatorObject_currentDimentions script has been remapped to NVDA+numpadDelete. The old key combination did not work on some keyboards. This script also now reports the width and height of the object instead of the right/bottom coordinates.
* Improved performance (especially on netbooks) when many beeps occur in quick succession; e.g. fast mouse movement with audio coordinates enabled. (#396)
* The NVDA error sound is no longer played in release candidates and final releases. Note that errors are still logged.

### Bug Fixes

* When NVDA is run from an 8.3 dos path, but it is installed in the related long path (e.g. progra~1 verses program files) NVDA will correctly  identify that it is an installed copy and properly load the user's settings.
* speaking the title of the current foreground window with nvda+t now works correctly when in menus.
* braille no longer shows useless information in its focus context such as unlabeled panes.
* stop announcing some useless information when the focus changes such as root panes, layered panes and scroll panes in Java or Lotus applications.
* Make the  keyword search field in Windows Help (CHM) viewer much more usable. Due to buggyness in that control, the current keyword could not be read as it would be continually changing.
* report correct page numbers in Microsoft Word if the page numbering has been specifically offset in the document.
* Better support for edit fields found in Microsoft Word dialogs (e.g. the Font dialog). It is now possible  to navigate these controls with the arrow keys.
* better support for Dos consoles. specifically: NVDA can now read the content of particular consoles it always used to think were blank. Pressing control+break no longer terminates NVDA.
* On Windows Vista and above, the NVDA installer now starts NVDA with normal user privileges when requested to run NVDA on the finish screen.
* Backspace is now handled correctly when speaking typed words. (#306)
* Don't incorrectly report "Start menu" for certain context menus in Windows Explorer/the Windows shell. (#257)
* NVDA now correctly handles ARIA labels in Mozilla Gecko when there is no other useful content. (#156)
* NVDA no longer incorrectly enables focus mode automatically for editable text fields which update their value when the focus changes; e.g. http://tigerdirect.com/. (#220)
* NVDA will now attempt to recover from some situations which would previously cause it to freeze completely. It may take up to 10 seconds for NVDA to detect and recover from such a freeze.
* When the NVDA language is set to "User default", use the user's Windows  display language setting instead of the Windows locale setting. (#353)
* NVDA now recognises the existence of controls in AIM 7.
* The pass key through command no longer gets stuck if a key is held down. Previously, NVDA stopped accepting commands if this occurred and had to be restarted. (#413)
* The taskbar is no longer ignored when it receives focus, which often occurs when exiting an application. Previously, NVDA behaved as if the focus had not changed at all.
* When reading text fields in applications which use the Java Access Bridge (including OpenOffice.org), NVDA now functions correctly when reporting of line numbers is enabled.
* The review copy command (NVDA+f10) gracefully handles the case where it is used on a position before the start marker. Previously, this could cause problems such as crashes in Notepad++.
* A certain control character (0x1) no longer causes strange eSpeak behaviour (such as changes in volume and pitch) when it is encountered in text. (#437)
* The report text selection command (NVDA+shift+upArrow) now gracefully reports that there is no selection in objects which do not support text selection.
* Fixed the issue where pressing the enter key on certain Miranda-IM buttons or links was causing NVDA to freeze. (#440)
* The current line or selection is now properly respected when spelling or copying the current navigator object.
* Worked around a Windows bug which was causing garbage to be spoken after the name of link controls in Windows Explorer and Internet Explorer dialogs. (#451)
* Fixed a problem with the report date and time command (NVDA+f12). Previously, date reporting was truncated on some systems. (#471)
* Fixed the issue where the system screen reader flag was sometimes inappropriately cleared after interacting with secure Windows screens. This could cause problems in applications which check the screen reader flag, including Skype, Adobe Reader and Jart. (#462)
* In an Internet Explorer 6 combo box, the active item is now reported when it is changed. (#342)

## 0.6p3

### New Features

* As Microsoft Excel's formula bar is inaccessible to NVDA, provide an NVDA specific dialog box for editing when the user presses f2 on a cell.
* Support for formatting in IAccessible2 text controls, including Mozilla applications.
* Spelling errors can now be reported where possible. This is configurable from the Document Formatting preferences dialog.
* NVDA can be configured to beep for either all or only visible progress bars. Alternatively, it can be configured to speak progress bar values every 10%.
* Links can now be identified in richedit controls.
* The mouse can now be moved to the character under the review cursor in most editable text controls. Previously, the mouse could only be moved to the center of the control.
* In virtual buffers, the review cursor now reviews the text of the buffer, rather than just the internal text of the navigator object (which is often not useful to the user). This means that you can navigate the virtual buffer hierarchically using object navigation and the review cursor will move to that point in the buffer.
* Handle some additional states on Java controls.
* If the title command (NVDA+t) is pressed twice, it spells the title. If pressed thrice, it is copied to the clipboard.
* Keyboard help now reads the names of modifier keys when pressed alone.
* Key names announced by keyboard help are now translatable.
* Added support for the recognized text field in SiRecognizer. (#198)
* Support for braille displays!
* Added a command (NVDA+c) to report the text on the Windows clipboard. (#193)
* In virtualBuffers, if NVDA automatically switches to focus mode, you can use the escape key to switch back to browse mode. NVDA+space can still also be used.
* In virtual buffers, when the focus changes or the caret is moved, NVDA can automatically switch to focus mode or browse mode as appropriate for the control under the caret. This is configured from the Virtual Buffers dialog. (#157)
* Rewritten SAPI4 synthesizer driver which replaces the sapi4serotek and sapi4activeVoice drivers and should fix the problems encountered with these drivers.
* The NVDA application now includes a manifest, which means that it no longer runs in compatibility mode in Windows Vista.
* The configuration file and speech dictionaries are now saved in the user's application data directory if NVDA was installed using the installer. This is necessary for Windows Vista and also allows multiple users to have individual NVDA configurations.
* Added support for position information for IAccessible2 controls.
* Added the ability to copy text to the clipboard using the review cursor. NVDA+f9 sets the start marker to the current position of the review cursor. NVDA+f10 retrieves the text between the start marker and the current position of the review cursor and copies it to the clipboard. (#240)
* Added support for some edit controls in pinacle tv software.
* When announcing selected text for long selections (512 characters or more), NVDA now speaks the number of selected characters, rather than speaking the entire selection. (#249)

### Changes

* If the audio output device is set to use the Windows default device (Microsoft Sound Mapper), NVDA will now switch to the new default device for eSpeak and tones when the default device changes. For example, NVDA will switch to a USB audio device if it automatically becomes the default device when it is connected.
* Improve performance of eSpeak with some Windows Vista audio drivers.
* reporting of links, headings, tables, lists and block quotes can now be configured from the Document Formatting settings dialog. Previously to configure these settings for virtual buffers, the virtual buffer settings dialog would have been used. Now all documents share this configuration.
* Rate is now the default setting in the speech synthesizer settings ring.
* Improve the loading and unloading of appModules.
* The title command (NVDA+t) now only reports the title instead of the entire object. If the foreground object has no name, the application's process name is used.
* Instead of virtual buffer pass through on and off, NVDA now reports focus mode (pass through on) and browse mode (pass through off).
* Voices are now stored in the configuration file by ID instead of by index. This makes voice settings more reliable across systems and configuration changes. The voice setting will not be preserved in old configurations and an error may be logged the first time a synthesizer is used. (#19)
* The level of a tree view item is now announced first if it has changed from the previously focused item for all tree views. Previously, this was only occurring for native Windows (SysTreeView32) tree views.

### Bug Fixes

* The last chunk of audio is no longer cut off when using NVDA with eSpeak on a remote desktop server.
* Fix problems with saving speech dictionaries for certain voices.
* Eliminate the lag when moving by units other than character (word, line, etc.) towards the bottom of large plain text documents in Mozilla Gecko virtual buffers. (#155)
* If speak typed words is enabled, announce the word when enter is pressed.
* Fix some character set issues in richedit documents.
* The NVDA log viewer now uses richedit instead of just edit to display the log. This improves reading by word with NVDA.
* Fix some issues related to embedded objects in richedit controls.
* NVDA now reads page numbers in Microsoft Word. (#120)
* Fix the issue where tabbing to a checked checkbox in a Mozilla Gecko virtual buffer and pressing space would not announce that the checkbox was being unchecked.
* Correctly report partially checked checkboxes in Mozilla applications.
* If the text selection expands or shrinks in both directions, read the selection as one chunk instead of two.
* When reading with the mouse, text in Mozilla Gecko edit fields should now be read.
* Say all should no longer cause certain SAPI5 synthesizers to crash.
* Fixed an issue which meant that text selection changes were not being read in Windows standard edit controls before the first focus change after NVDA was started.
* Fix mouse tracking in Java objects. (#185)
* NVDA no longer reports Java tree view items with no children as being collapsed.
* Announce the object with focus when a Java window comes to the foreground. Previously, only the top-level Java object was announced.
* The eSpeak synthesizer driver no longer stops speaking completely after a single error.
* Fix the issue whereby updated voice parameters (rate, pitch, etc.) were not saved when the voice was changed from the synthesizer settings ring.
* Improved the speaking of typed characters and words.
* Some new text that was previously not spoken in text console applications (such as some text adventure games) is now spoken.
* NVDA now ignores focus changes in background windows. Previously, a background focus change could be treated as if the real focus changed.
* Improved the detection of the focus when leaving context menus. Previously, NVDA often didn't react at all when leaving a context menu.
* NVDA now announces when the context menu is activated in the Start menu.
* The classic Start menu is now announced as Start menu instead of Application menu.
* Improved the reading of alerts such as those encountered in Mozilla Firefox. The text should no longer be read multiple times and other extraneous information will no longer be read. (#248)
* The text of focusable, read-only edit fields will no longer be included when retrieving the text of dialogs. This fixes, for example, the automatic reading of the entire license agreement in installers.
* NVDA no longer announces the unselection of text when leaving some edit controls (example: Internet Explorer address bar, Thunderbird 3 email address fields).
* When opening plain text emails in Outlook Express and Windows Mail, focus is correctly placed in the message ready for the user to read it. Previously the user had to press tab or click on the message in order to use cursor keys to read it.
* Fixed several major issues with the "Speak command keys" functionality.
* NVDA can now read text past 65535 characters in standard edit controls (e.g. a large file in Notepad).
* Improved line reading in MSHTML edit fields (Outlook Express editable messages and Internet Explorer text input fields).
* NVDA no longer sometimes freezes completely when editing text in OpenOffice. (#148, #180)

## 0.6p2

* Improved the default ESpeak voice in NVDA
* Added a laptop keyboard layout. Keyboard layouts can be configured from NVDA's  Keyboard settings dialog. (#60)
* Support for grouping items in SysListView32 controls, mainly found in Windows Vista. (#27)
* Report the checked state of treeview items in SysTreeview32 controls.
* Added shortcut keys for many of NVDA's configuration dialogs
* Support for IAccessible2 enabled applications such as Mozilla Firefox when running NVDA from portable media, with out having to register any special Dll files
* Fix a crash with the virtualBuffers Links List in Gecko applications. (#48)
* NVDA should no longer crash Mozilla Gecko applications such as Firefox and Thunderbird if NVDA is running with higher privilages than the Mozilla Gecko application. E.g. NVDA is  running as Administrator.
* Speech dictionaries (previously User dictionaries) now can be either case sensitive or insensitive, and the patterns can optionally be regular expressions. (#39)
* Whether or not NVDA uses a 'screen layout' mode for virtual buffer documents can now be configured from a settings dialog
* No longer report anchor tags with no href in Gecko documents as links. (#47)
* The NVDA find command now remembers what you last searched for, across all applications. (#53)
* Fix issues where the checked state would not be announced for some checkboxes and radio buttons in virtualBuffers
* VirtualBuffer pass-through mode is now specific to each document, rather than NVDA globally. (#33)
* Fixed some sluggishness with focus changes and incorrect speech interuption which sometimes occured when using NVDA on a system that had been on standby or was rather slow
* Improve support for combo boxes in Mozilla Firefox. Specifically when arrowing around them text isn't repeated, and when jumping out of them, ancestor controls are not announced unnecessarily. Also virtualBuffer commands now work when focused on one  when you are in a virtualBuffer.
* Improve accuracy of finding the statusbar in many applications. (#8)
* Added the NVDA interactive Python console tool, to enable developers to look at and manipulate NVDA's internals as it is running
* sayAll, reportSelection and reportCurrentLine scripts now work properly when in virtualBuffer pass-through mode. (#52)
* The increase rate and decrease rate scripts have been removed. Users should use the synth settings ring scripts (control+nvda+arrows) or the Voice settings dialog
* Improve the range and scale of the progress bar beeps
* Added more quick keys to the new virtualBuffers:  l for list, i for list item, e for edit field, b for button, x for checkbox, r for radio button, g for graphic, q for blockquote, c for combo box, 1 through 6 for respective heading levels, s for separator, m for frame. (#67, #102, #108)
* Canceling the loading of a new document in Mozilla Firefox now allows the user to keep using the old document's virtualBuffer if the old document hadn't yet really been destroyed. (#63)
* Navigating by words in virtualBuffers is now more accurate as  words do not accidentally contain text from more than one field. (#70)
* Improved accuracy of focus tracking and focus updating when navigating in Mozilla Gecko virtualBuffers.
* Added a findPrevious script (shift+NVDA+f3) for use in new virtualBuffers
* Improved sluggishness in Mozilla Gecko dialogs (in Firefox and Thunderbird). (#66)
* Add the ability to view the current log file for NVDA. it can be found in the NVDA menu -> Tools
* Scripts such as say time and date now take the current language in to account; punctuation and ordering of words now reflects the language
* The language combo box in NVDA's General settings dialog now shows full language names for ease of use
* When reviewing text in the current navigator object, the text is always up to date if it changes dynamically. E.g. reviewing the text of a list item in Task Manager. (#15)
* When moving with the mouse, the current paragraph of text under the mouse is now announced, rather than either all the text in that particular object or just the current word. Also audio coordinates, and announcement of object roles is optional, they are turned off by default
* Support for reading text with the mouse in Microsoft Word
* Fixed bug where leaving the menu bar in applications such as Wordpad would cause text selection to not be announced anymore
* In Winamp, the title of the track is no longer announced again and again when switching tracks, or pausing/resuming/stopping playback.
* In Winamp,  Added ability to announce state of the shuffle and repeat controls as they are switched. Works in the main window and in the playlist editor
* Improve the ability to activate particular fields in Mozilla Gecko virtualBuffers. May include clickable graphics, links containing paragraphs, and other weird structures
* Fixed an initial lag when opening NVDA dialogs on some systems. (#65)
* Add specific support for the Total Commander application
* Fix bug in the sapi4serotek driver where the pitch could get locked at a particular value, i.e. stays high after reading a capital letter. (#89)
* Announce clickable text and other fields as clickable in Mozilla Gecko VirtualBuffers. e.g.  a field which has an onclick HTML attribute. (#91)
* When moving around Mozilla Gecko virtualBuffers, scroll the current field in to view -- useful so sighted peers have an idea of where the user is up to in the document. (#57)
* Add basic support for ARIA live region show events in IAccessible2 enabled applications. Useful in the Chatzilla IRC application, new messages will now be read automatically
* Some slight improvements to help use ARIA enabled web applications,  e.g. Google Docs
* Stop adding extra blank lines to text when copying it from a virtualBuffer
* Stop the space key from activating a link in the Links List. Now it can be used like other letters in order to  start typing the name of a particular link you wish to go to
* The moveMouseToNavigator script (NVDA+numpadSlash) now moves the mouse to the centre of the navigator object, rather than the top left
* Added scripts to click the left and right mouse buttons (numpadSlash and numpadStar respectively)
* Improve access to the Windows System Tray. Focus hopefully should no longer seem to keep jumping back to one particular item. Reminder: to get to the System Tray use the Windows command WindowsKey+b. (#10)
* Improve performance and stop announcing extra text when holding down a cursor key in an edit field and it hits the end
* Stop the ability for NVDA to make the user wait while particular messages are spoken. Fixes some crashes/freezes with particular speech synthesizers. (#117)
* Added support for the Audiologic Tts3 speech synthesizer, contribution by Gianluca Casalino. (#105)
* Possibly improve performance when navigating around documents in Microsoft Word
* Improved accuracy when reading text of alerts in Mozilla Gecko applications
* Stop possible crashes when trying to save configuration on non-English versions of Windows. (#114)
* Add an NVDA welcome dialog. This dialog is designed to provide essential information for new users and allows CapsLock to be configured as an NVDA modifier key. This dialog will be displayed when NVDA is started by default until it is disabled.
* Fix basic support for Adobe Reader so it is possible to read documents  in  versions 8 and 9
* Fix some errors that may have occured when holding down keys before NVDA is properly initialized
* If the user has configured NVDA to save configuration on exit, make sure the configuration is properly saved when shutting down or logging out of  Windows.
* Added an NVDA logo sound to the beginning of the installer, contributed by Victer Tsaran
* NVDA, both running in the installer and otherwise, should properly clean up its system tray icon when it exits
* Labels for standard controls in NVDA's dialogs (such as Ok and cancel buttons) should now show in the language NVDA is set to, rather than just staying in English.
* NVDA's icon should now be  used for  the NVDA shortcuts in the start menu and on the Desktop, rather than a default application icon.
* Read cells in MS Excel when moving with tab and shift+tab. (#146)
* Fix some double speaking in particular lists in Skype.
* Improved caret tracking in IAccessible2 and Java applications; e.g. in Open Office and Lotus Symphony, NVDA properly waits for the caret to move in documents rather than accidentally reading the wrong word or line at the end of some paragraphs. (#119)
* Support for AkelEdit controls found in Akelpad 4.0
* NVDA no longer locks up in Lotus Synphony when moving from the document to the menu bar.
* NVDA no longer freezes in the Windows XP Add/Remove programs applet when launching an uninstaller. (#30)
* NVDA no longer freezes when opening Spybot Search and Destroy

## 0.6p1

### Access to web content with new in-process virtualBuffers (so far for Mozilla Gecko applications including Firefox3 and Thunderbird3)

* Load times have been improved almost by a factor of thirty (you no longer have to wait at all for most web pages to load in to the buffer)
* Added a links list (NVDA+f7)
* Improved the find dialog (control+nvda+f) so that it performs a case-insencitive search, plus fixed a few focus issues with that dialog box.
* It is now possible to select and copy text in the new virtualBuffers
* By default the new virtualBuffers represent the document in a screen layout (links and controls are not on separate lines unless they really are visually). You can toggle this feature with NVDA+v.
* It is possible to move by paragraph with control+upArrow and control+downArrow.
* Improved support for dynamic content
* Improved over all accuracy of reading lines and fields when arrowing up and down.

### Internationalization

* It is now possible to type accented characters that rely on a "dead character", while NVDA is running.
* NVDA now announces when the keyboard layout is changed (when pressing alt+shift).
* The announce date and time feature now takes the system's current regional and language options in to account.
* added czech translation (by Tomas Valusek with help from Jaromir Vit)
* added vietnamese translation by Dang Hoai Phuc
* Added Africaans (af_ZA) translation, by Willem van der Walt.
* Added russian translation by Dmitry Kaslin 
* Added polish translation by DOROTA CZAJKA and friends.
* Added Japanese translation by Katsutoshi Tsuji.
* added Thai translation by Amorn Kiattikhunrat
* added croatian translation by Mario Percinic and Hrvoje Katic  
* Added galician translation by Juan C. buno 
* added ukrainian translation by Aleksey Sadovoy 

### Speech

* NVDA now comes packaged with eSpeak 1.33 which contains many improvements, among those are improved languages, named variants, ability to speak faster.
* The voice settings dialog now allows you to change the variant of a synthesizer if it supports one. Variant is usually a slight variation on the current voice. (eSpeak supports variants).
* Added the ability to change the inflection of a voice in the voice settings dialog if the current synthesizer supports this. (eSpeak supports inflection).
* Added the ability to turn off speaking of object position information(e.g. 1 of 4). This option can be found in the Object presentation settings dialog.
* NVDA can now beep when speaking a capital letter. This can be turned on and off with a check box in the voice settings dialog. Also added a raise pitch for capitals check box to configure whether NVDA should actually do its normal pitch raise for capitals. So now you can have either raise pitch, say cap, or beep, for capitals.
* Added the ability to pause speech in NVDA (like found in Voice Over for the Mac). When NVDA is speaking something, you can press the control or shift keys to silence speech just like normal, but if you then tap the shift key again (as long as you havn't pressed any other keys) speech will continue from exactly where it left off.
* Added a virtual synthDriver which outputs text to a window instead of speaking via a speech synthesiser. This should be more pleasant for sighted developers who are not used to speech synthesis but want to know what is spoken by NVDA. There are probably still some bugs, so feedback is most definitely welcome.
* NVDA no longer by default speaks punctuation, you can enable speaking of punctuation with NVDA+p.
* eSpeak by default now speaks quite a bit slower, which should make it easier for people who are using eSpeak for the first time, when installing or starting to use NVDA.
* Added user dictionaries to NVDA. These allow you to make NVDA speak certain text differently. There are three dictionaries: default, voice, and temporary. Entries you add to the default dictionary will happen all the time in NVDA. Voice dictionaries are specific to the current synthesizer and voice you currently have set. And temporary dictionary is  for those times you quickly want to set a rule while you are doing a particular task, but you don't want it to be perminant (it will disappear if you close NVDA). For now the rules are regular expressions, not just normal text.
* Synthesizers can now use any audio output device on your system, by setting the output device combo box in the Synthesizer dialog before selecting the synthesizer you want.

### Performance

* NVDA no longer takes up a huge amount of system memory , when editing messages in mshtml edit controls
* Improved performance when reviewing text inside many controls that do not actually have a real cursor. e.g. MSN Messenger history window, treeview items, listview items etc.
* Improved performance in rich edit documents.
* NVDA should no longer slowly creep up in system memory size for no reason
* Fixed bugs when  trying to focus on a dos console window more than three or so times. NVDA did have a tendency to completely crash.

### Key commands

* NVDA+shift+numpad6 and NVDA+shift+numpad4 allow you to navigate to the next or previous object in flow respectively. This means that you can navigate in an application by only using these two keys with out having to worry about going up by parent, or down to first child as you move around the object hyerarchy. For instance in a web browser such as firefox, you could navigate the document by object, by just using these two keys. If next in flow or previous in flow takes you up and out of an object, or down in to an object, ordered beeps indicate the direction.
* You can now configure voice settings with out opening the voice settings dialog, by using the Synth Settings Ring. The synth settings ring is a group of voice settings you can toggle through by pressing control+NVDA+right and control+NVDA+left. To change a setting use control+NVDA+up and control+NVDA+down.
* Added a command to report the current selection in edit fields (NVDA+shift+upArrow).
* Quite a few NVDA commands that speak text (such as report current line etc) now can spell the text if pressed twice quickly.
* the capslock, numpad insert and extended insert can all be used as the NVDA modifier key. Also if one of these keys is used, pressing the key twice with out pressing any other keys will send the key through to the operating system, just like you'd pressed the key with out NVDA running. To make one of these keys be the NVDA modifier key, check its checkbox in the Keyboard settings dialog (used to be called the keyboard echo dialog).

### Application support

* Improved support for Firefox3 and Thunderbird3 documents. Load times have been improved by almost a factor of thirty, a screen layout is used by default (press nvda+v to toggle between this and no screen layout), a links list (nvda+f7 has been added), the find dialog (control+nvda+f) is now case-insensitive, much better support for dynamic content, selecting and copying text is now possible.
* In the MSN Messenger and Windows Live Messenger history windows, it is now possible to select and copy text.
* Improved support for the audacity application
* Added support for a few edit/text controls in Skype
* Improved support for Miranda instant messenger application
* Fixed some focus issues when opening html and plain text messages in Outlook Express. 
* Outlook express newsgroup message fields are now labeled correctly
* NVDA can now read the addresses in the Outlook Express message fields (to/from/cc etc)
* NVDA should be now more accurate at announcing the next message in out look express when deleting a message from the message list.

### APIs and toolkits

* Improved object navigation for MSAA objects. If a window has a system menu, title bar, or scroll bars, you can now navigate to them.
* Added support for the IAccessible2 accessibility API. A part from the ability to announce more control types, this also allows NVDA to access the cursor in applications such as Firefox 3 and Thunderbird 3, allowing you to navigate, select or edit text.
* Added support for Scintilla edit controls (such controls can be found in Notepad++ or Tortoise SVN).
* Added support for Java applications (via the Java Access Bridge). This can provide basic support for Open Office (if Java is enabled), and any other stand-alone Java application. Note that java applets with in a web browser may not work yet.

### Mouse

* Improved support for reading what is under the mouse pointer as it moves. It is now much faster, and it also now has the ability in some controls such as standard edit fields, Java and IAccessible2 controls, to read the current word, not just the current object. This may be of some used to vision impared people who just want to read a specific bit of text with the mouse.
* Added a new config option, found in the mouse settings dialog. Play audio when mouse moves, when checked, plays a 40 ms beep each time the mouse moves, with its pitch (between 220 and 1760 hz) representing the y axis, and left/right volume, representing the x axis. This enables a blind person to get a rough idea of where the mouse is on the screen as its being moved. This feature also depends on reportObjectUnderMouse also being turned on. So this means that if you quickly need to disable both beeps and announcing of objects, then just press NVDA+m. The beeps are also louder or softer depending on how bright the screen is at that point.

### Object presentation and interaction

* Improved support for most common treeview controls. NVDA now tells you how many items are in the branch when you expand it. It also announces the level when moving in and out of branches. And, it announces the current item number and number of items, according to the current branch, not the entire treeview.
* Improved what is announced when focus changes as you move around applications or the operating system. Now instead of just hearing the control you land on, you hear information about any controls this control is positioned inside of. For instance if you tab and land on a button inside a groupbox, the groupbox will also get announced.
* NVDA now tries to speak the message inside many dialog boxes as they appear. This is accurate most of the time, though there are still many dialogs that arn't as good as they could be.
* Added a report object descriptions checkbox to the object presentation settings dialog. Power users may wish to sometimes uncheck this to stop NVDA announcing a lot of extra descriptions on particular controls,  such as in Java applications.
* NVDA automatically announces selected text in edit controls when focus moves to them. If there isn't any selected text, then it just announces the current line like usual.
* NVDA is a lot more careful now when it plays beeps to indicate progress bar changes in applications. It no longer goes crazy in Eclipse applications such as Lotus Notes/Symphony, and Accessibility Probe.

### User Interface

* Removed the NVDA interface window, and replaced it with a simple NVDA popup menu.
* NVDA's user interface settings dialog is now called General Settings. It also contains an extra setting: a combo box to set the log level, for what messages should go to NVDA's log file. Note that NVDA's log file is now called nvda.log not debug.log.
* Removed the report object group names checkBox from the object presentation settings dialog, reporting of group names now is handled differently.

## 0.5

* NVDA now has a built-in synthesizer called eSpeak, developed by Jonathan Duddington.It is very responsive and lite-weight, and has support for many different languages. Sapi synthesizers can still be used, but eSpeak will be used by default.
 * eSpeak does not depend on any special software to be installed, so it can be used with NVDA on any computer, on a USB thumb drive, or anywhere. 
 * For more info on eSpeak, or to find other versions, go to http://espeak.sourceforge.net/.
* Fix bug where the wrong character was being announced when pressing delete in Internet Explorer / Outlook Express editable panes.
* Added support for more edit fields in Skype.
* VirtualBuffers only get loaded when focus is on the window that needs to be loaded. This fixes some problems when the preview pane is turned on in Outlook Express.
* Added commandline arguments to NVDA:
 * -m, --minimal: do not play startup/exit sounds and do not show the interface on startup if set to do so.
 * -q, --quit: quit any other already running instance of NVDA and then exit
 * -s, --stderr-file fileName: specify where NVDA should place uncaught errors and exceptions
 * -d, --debug-file fileName: specify where NVDA should place debug messages
 * -c, --config-file: specify an alternative configuration file  
 * -h, -help: show a help message listing commandline arguments
* Fixed bug where punctuation symbols would not be translated to the appropriate language, when using a language other than english, and when speak typed characters was turned on.
* Added Slovak language files thanks to Peter Vagner 
* Added a Virtual Buffer settings dialog and a Document Formatting settings dialog, from Peter Vagner.
* Added French translation thanks to Michel Such 
* Added a script to toggle beeping of progress bars on and off (insert+u). Contributed by Peter Vagner.
* Made more messages in NVDA be translatable for other languages. This includes script descriptions when in keyboard help.
* Added a find dialog to the virtualBuffers (internet Explorer and Firefox). Pressing control+f when on a page brings up a dialog in which you can type some text to find. Pressing enter will then search for this text and place the virtualBuffer cursor on this line. Pressing f3 will also search for the next occurance of the text.
* When speak typed characters is turned on, more characters should be now spoken. Technically, now ascii characters from 32 to 255 can now be spoken.
* Renamed some control types for better readability. Editable text is now edit, outline is now tree view and push button is now button.
* When arrowing around list items in a list, or tree view items in a tree view, the control type (list item, tree view item) is no longer spoken, to speed up navigation.
* Has Popup (to indicate that a menu has a submenu) is now spoken as submenu.
* Where some language use control and alt (or altGR) to enter a special character, NVDA now will speak these characters when speak typed characters is on.
* Fixed some problems with reviewing static text controls.
* Added Translation for Traditional Chinese, thanks to Coscell Kao.
* Re-structured an important part of the NVDA code, which should now fix many issues with NVDA's user interface (including settings dialogs).
* Added Sapi4 support to NVDA. Currently there are two sapi4 drivers, one based on code contributed by Serotek Corporation, and one using the ActiveVoice.ActiveVoice com Interface. Both these drivers have issues, see which one works best for you.
* Now when trying to run a new copy of NVDA while an older copy is still running will cause the new copy to just exit. This fixes a major problem where running multiple copies of NVDA makes your system very unusable.
* Renamed the title of the NVDA user interface from NVDA Interface to NVDA. 
* Fixed a bug in Outlook Express where pressing backspace at the start of an editable message would cause an error.
* Added patch from Rui Batista that adds a script to report the current battery status on laptops (insert+shift+b).
* Added a synth driver called Silence. This is a synth driver that does not speak anything, allowing NVDA to stay completely silent at all times. Eventually this could be used along with Braille support, when we have it.
* Added capitalPitchChange setting for synthesizers thanks to J.J. Meddaugh
* Added patch from J.J. Meddaugh that makes the toggle report objects under mouse script more like the other toggle scripts (saying on/off rather than changing the whole statement).
* Added spanish translation (es) contributed by Juan C. buo.
* Added Hungarian language file from Tamas Gczy.
* Added Portuguese language file from Rui Batista.
* Changing the voice in the voice settings dialog now sets the rate, pitch and volume sliders to the new values according to the synthesizer, rather than forcing the synthesizer to be set to the old values. This fixes issues where a synth like eloquence or viavoice seems to speek at a much faster rate than all other synths.
* Fixed a bug where either speech would stop, or NVDA would entirely crash, when in a Dos console window.
* If support for a particular language exists, NVDA now automatically can show its interface and speak its messages in the language Windows is set to. A particular language can still be chosen manualy from the user interface settings dialog as well.
* Added script 'toggleReportDynamicContentChanges' (insert+5). This toggles whether new text, or other dynamic changes should be automatically announced. So far this only works in Dos Console Windows.
* Added script 'toggleCaretMovesReviewCursor' (insert+6). This toggles whether the review cursor should be automatically repositioned when the system caret moves. This is useful in Dos console windows when trying to read information as the screen is updating.
* Added script 'toggleFocusMovesNavigatorObject' (insert+7). This toggles whether the navigator object is repositioned on the object with focus as it changes.
* Added some documentation translated in to various languages. So far there is French, Spannish and Finish.
* Removed some developer documentation from the binary distribution of NVDA, it is only now in the source version.
* Fixed a possible bug in Windows Live Messanger and MSN Messenger where arrowing up and down the contact list would cause errors.
* New messages are now automatically spoken when in a conversation using Windows Live Messenger. (only works for English versions so far)
* The history window in a Windows Live Messenger conversation can now be read by using the arrow keys. (Only works for English versions so far) 
* Added script 'passNextKeyThrough' (insert+f2). Press this key, and then the next key pressed will be passed straight through to Windows. This is useful if you have to press a certain key in an application but NVDA uses that key for something else.
* NVDA no longer freezes up for more than a minute when opening very large documents in MS Word.
* Fixed a bug where moving out of a table in MS Word, and then moving back in, caused the current row/column numbers not to be spoken if moving back in to exactly the same cell.
* When starting NVDA with a synthesizer that doesn't exist, or is not working, the sapi5 synth will try and be loaded in stead, or if sapi5 isn't working, then speech will be set to silence.
* Increasing and decreasing rate scripts can no longer take the rate above 100 or below 0.
* If there is an error with a language when choosing it in the User Interface Settings dialog, a message box will alert the user to the fact.
* NVDA now asks if it should save configuration and restart if the user has just changed the language in the User Interface Settings Dialog. NVDA must be restarted for the language change to fully take effect.
* If a synthesizer can not be loaded, when choosing it from the synthesizer dialog, a message box alerts the user to the fact.
* When loading a synthesizer for the first time, NVDA lets the synthesizer choose the most suitable voice, rate and pitch parameters, rather than forcing it to defaults it thinks are ok. This fixes a problem where Eloquence and Viavoice sapi4 synths start speaking way too fast for the first time.
