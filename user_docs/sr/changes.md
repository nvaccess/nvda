# NVDA šta je novo


## 2024.2

Dodata je nova opcija razdvajanje zvuka.
Ovo vam dozvoljava da odvojite  NVDA na jednom kanalu (na primer levom) a zvukove svih ostalih aplikacija  prebacite na drugi (na primer desni).

Dodate su nove komande za menjanje vrednosti u krugu podešavanja govora, koje dozvoljavaju korisnicima da skoče na prvo ili poslednje podešavanje, ili da povećaju ili smanje trenutno podešavanje većim skokom.
Dodate su takođe nove komande brze navigacije, one dozvoljavaju korisnicima da dodaju prečice kako bi brzo skakali između: Pasusa, vertikalno poravnatih pasusa, teksta istog stila, teksta različitog stila, stavki menija, dugmadi prekidača, traka napredovanja, figura i matematičkih formula.

Dodate su brojne nove karakteristike za brajeve redove i ispravljene greške.
Dodat je novi brajev režim "Prikaži govor".
Kada je aktivan, brajev red će prikazati tačno ono što NVDA priprema za izgovor.
Takođe je dodata podrška za BrailleEdgeS2, BrailleEdgeS3 brajeve uređaje.
LibLouis je ažuriran, dodajući nove detaljne (uz indikaciju velikih slova) beloruske i ukrajinske brajeve tabele, uz špansku tabelu za čitanje grčkih tekstova.

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
  * Dodata podrška za BrailleEdgeS2, BrailleEdgeS3 brajeve uređaje. (#16033, #16279, @EdKweon)
  * Dodat je novi brajev režim "Prikaži govor". (#15898, @Emil-18)
    * Kada je aktivan, na brajevom redu će se prikazati ono što NVDA priprema za izgovor.
    * Može se uključiti ili isključiti prečicom `NVDA+alt+t`, ili iz dijaloga brajevih podešavanja.
* Razdvajanje zvuka: (#12985, @mltony)
  * Dozvoljava da odvojite NVDA zvukove na jednom kanalu (na primer levom) dok su zvukovi drugih aplikacija na drugom kanalu (na primer desnom).
  * Uključuje se ili isključuje prečicom `NVDA+alt+s`.
  * Jačina drugih aplikacija se može menjati prečicama `NVDA+alt+pageUp` i `NVDA+alt+pageDown`. (#16052, @mltony)
  * Zvuk drugih aplikacija se može isključiti prečicom `NVDA+alt+delete`. (#16052, @mltony)
* Prijavljivanje zaglavlja redova i kolona je sada podržano u contenteditable HTML elementima. (#14113)
* Dodata opcija kako biste onemogućili prijavljivanje figura i naslova slika u podešavanjima formatiranja dokumenta. (#10826, #14349)
* U Windowsu 11, NVDA će izgovarati upozorenja glasovnog unosa i predloženih radnji uključujući predlog na vrhu kada kopirate podatke kao što su brojevi telefona u privremenu memoriju (Windows 11 2022 ažuriranje i novija). (#16009, @josephsl)
* NVDA će održavati zvučni uređaj budnim nakon što se govor zaustavi, kako bi sprečio da početak sledećeg izgovorenog teksta bude isprekidan sa nekim zvučnim uređajima kao što su Bluetooth slušalice. (#14386, @jcsteh, @mltony)
* HP Secure pretraživač je sada podržan. (#16377)

### Promene

* Prodavnica dodataka:
  * Minimalna i poslednja testirana NVDA verzija za dodatak se sada prikazuju u sekciji "Drugi detalji". (#15776, @Nael-Sayegh)
  * Radnja za recenzije zajednice će biti dostupna i Web stranica za recenzije će se prikazivati u panelu sa detaljima, na svim karticama prodavnice. (#16179, @nvdaes)
* Ažurirane komponente:
  * Ažuriran LibLouis brajev prevodilac na [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Dodate nove detaljne (uz indikaciju velikih slova) beloruske i ukrajinske brajeve tabele, uz špansku tabelu za čitanje grčkih tekstova.
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
* Ispravke za pretraživače zasnovane na Chromiumu kada se koriste uz UIA:
  * Ispravljene greške koje su izazvale da se NVDA zamrzne. (#16393, #16394)
  * Backspace taster sada ispravno radi u Gmail poljima za prijavljivanje. (#16395)
* Taster Backspace sada ispravno radi kada koristite Nudi 6.1 uz omogućeno NVDA podešavanje  "Kontroliši tastere iz drugih aplikacija". (#15822, @jcsteh)
* Ispravljena greška koja je izazivala da se zvučni koordinati reprodukuju dok je aplikacija u režimu spavanja kada je omogućeno podešavanje "Reprodukuj zvučne koordinate kada se miš pomera". (#8059, @hwf1324)
* U Adobe Readeru, NVDA više ne ignoriše alternativni tekst koji je podešen za formule u PDF datotekama. (#12715)
* Ispravljena greška koja je izazvala da NVDA ne može da pročita traku menija i opcije u programu Geekbench. (#16251, @mzanm)
* Ispravljena retka situacija u kojoj čuvanje podešavanja ne uspe da sačuva sve profile. (#16343, @CyrilleB79)
* U Firefoxu i pretraživačima zasnovanim na Chromiumu, NVDA će ispravno ući u režim fokusiranja kada se pritisne enter u prezentacionoj listi (ul / ol) u sadržaju koji se može uređivati. (#16325)
* Promena stanja kolona se automatski prijavljuje kada se biraju kolone za prikazivanje u listi poruka programa Thunderbird. (#16323)

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
    * `prefload/prefsave`: Učitava ili čuva NVDA podešavanja
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
  -
  -
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
-
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
-
* Eksperimentalno poboljšano upravljanje zvukovima:
  * NVDA sada može da reprodukuje zvukove korišćenjem standarda Windows Audio Session API (WASAPI), što može poboljšati brzinu, performanse i stabilnost NVDA govora i zvukova.
  * WASAPI korišćenje se može omogućiti u naprednim podešavanjima.
  Takođe, ako je WASAPI omogućen, sledeća napredna podešavanja se mogu podesiti.
    * Opcija koja će izazvati da jačina NVDA zvukova i pištanja prati podešavanje jačine glasa kojeg koristite. (#1409)
    * Opcija da odvojeno podesite jačinu NVDA zvukova. (#1409, #15038)
  * Postoji poznat problem sa povremenim rušenjem kada je WASAPI omogućen. (#15150)
* U pretraživačima Mozilla Firefox i Google Chrome, NVDA sada prijavljuje ako kontrola otvara dijalog, mrežu, listu ili stablo ako je autor ovo označio korišćenjem `aria-haspopup`. (#14709)
* Sada je moguće koristiti sistemske varijable  (kao što su  `%temp%` ili  `%homepath%`) pri određivanju putanje kada se pravi NVDA prenosna kopija. (#14680)
* Dodata podrška za brajev red Help Tech Activator. (#14917)
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
-
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
 - 

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

## 2022.3.2

Ovo je manje ažuriranje kako bi se ispravila pogoršanja koja je izazvala verzija 2022.3.1 i kako bi se ispravio bezbednosni problem.

### Bezbednosne ispravke

* Sprečava mogućnost pristupa na sistemskom nivou za korisnike koji nemaju autentikaciju.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Ispravljene greške

* Ispravljeno pogoršanje iz verzije 2022.3.1 koje je izazvalo onemogućavanje određenih funkcija na bezbednim ekranima. (#14286)
* Ispravljeno pogoršanje iz verzije 2022.3.1 koje je izazvalo onemogućavanje određenih funkcija nakon prijave, ako je NVDA pokrenut na zaključanom ekranu. (#14301)
 -

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
  -  wx GUI inspection alatka je sada onemogućena u bezbednom načinu rada.
  -

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
-
-

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
-   aria-current koji ima vrednost false će se sada izgovarati kao false  umesto  true (#7892).
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

## Starije verzije

Za starije verzije, pogledajte[Englesku verziju ovog dokumenta](../en/changes.html).

