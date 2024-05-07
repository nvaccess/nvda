# ﻿Što je novo u NVDA


### Obavijest za programere

Informacije za programere nisu prevedene, molimo ’pogledajte [englesku inačicu ovog dokumenta](../en/changes.html).

## 2024.2

Dodana nova značajka način podjeljenog zvuka.
Ta značajka omogućuje postavljanje zvuka NVDA u jedan kanal (npr. lijevi), dok su zvukovi drugih programa u drugom kanalu (na primjer desnom).

Dodani su novi prečaci za promjenu postavki prstena govorne jedinice, koje omogućuju premještanje od prve do zadnje postavke, te njihovo mijenjanje u većim koracima.
Dodani su novi prečaci brze navigacije, koji omogućuju korisnicima kretanje po: odlomcima, okomito poravnatim odlomcima, tekstu istog stila, tekstu različitog stila, stavkama izbornika, preklopnim gumbima, trakama napredovanja, figurama, te matematičkim formulama.

Dodano je puno novih značajki vezanih uz brajicu, te je ispravljeno puno pogrešaka.
Dodan je novi modus brajice "prikaz govora".
Kada je aktivan, na brajičnom se redku prikazuje točno ono što NVDA izgovara.
Također je dodana podrška za brajične redke BrailleEdgeS2, BrailleEdgeS3.
LibLouis je nadograđen sa dodanim novim brajičnim tablicama sa označavanjem velikih slova za bjeloruski i ukrajinski jezik, te brajična tablica za španjolski jezik, predviđena za čitanje starogrčkog teksta.

eSpeak je nadograđensa dodanim novim jezikom Tigrinja.

Ispravljeno je puno pogrešaka u programima, poput Thunderbirda, Adobe Readera, web preglednika, Nudija te Geekbench-a.

### Nove značajke

* Novi tipkovnički prečaci:
  * Novi prečac za brzo kretanje `p` za premještanje na sljedeći/prethodni odlomak teksta u modusu čitanja. (#15998, @mltony)
  * Novi nedodijeljeni prečaci, koji se mogu koristiti za kretanje po slijedećim/prethodnim:
    * figurama (#10826)
    * okomito poravnatim odlomcima (#15999, @mltony)
    * stavkama izbornika (#16001, @mltony)
    * preklopnim gumbima (#16001, @mltony)
    * trakama napredka (#16001, @mltony)
    * matematičkim formulama (#16001, @mltony)
    * tekstovima istog stila (#16000, @mltony)
    * tekstovima različitog stila (#16000, @mltony)
    * Dodan prečac za premještanje između prve postavke, posljednje postavke, za kretanje u naprijed te za kretanje u nazad unutar postavki prstena govorne jedinice. (#13768, #16095, @rmcpantoja)
    * Postavljanje prve ili posljednje postavke prstena govorne jedinice nema dodijeljen prečac. (#13768)
    * Povećavanje ili smanjivanje postavki govorne jedinice u većim koracima (#13768):
      * Prečac za stolna računala: `NVDA+control+pageUp` odnosno `NVDA+control+pageDown`.
      * prečac za prijenosna računala: `NVDA+control+shift+pageUp` ili `NVDA+control+shift+pageDown`.
  * Dodan novi nedodijeljeni prečac za uključivanje ili isključivanje izgovora figura i potpisa. (#10826, #14349)
* brajica:
  * Dodana podrška za brajični redak BrailleEdgeS2, BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * Novi modus brajice "prikaz govora" je dodan. (#15898, @Emil-18)
    * Kada je aktivan, na brajičnom se redku prikazuje točno ono što NVDA izgovara.
    * Može se uključiti pritiskom `NVDA+alt+t`, ili u dijaloškom okviru postavki brajice.
* Način podijeljenog zvuka: (#12985, @mltony)
  * Omogućuje postavljanje NVDA u jednom kanalu (na primjer lijevom) dok su zvukovi drugih programa u drugom kanalu (na primjer desnom).
  * Regulira se uz pomoć prečaca `NVDA+alt+s`.
  * Glasnoća drugih programa može se podešavati prečacima `NVDA+alt+pageUp` i `NVDA+alt+pageDown`. (#16052, @mltony)
  * Zvukovi drugih programa mogu se utišati uz pomoć prečaca `NVDA+alt+delete`. (#16052, @mltony)
* Izgovaranje zaglavlja redaka i stupaca u ContentEditable html elementima. (#14113)
* Dodana opcija za isključivanje čitanja figura i potpisa u postavkama oblikovanja dokumenata. (#10826, #14349)
* U Windowsima 11, NVDA će izgovarati upozorenja glasovnog upisivanja i preporučene radnje uključujući glavnu preporučenu radnju prilikom kopiranja podataka poput telefonskih brojeva u međuspremnik (Windows 11 nadogradnja 2022 i novije inačice). (#16009, @josephsl)
* NVDA će držati audiouređaj budnim poslije zaustavljanja govora, kako bi se izbjeglo rezanje sljedeće izgovorene fraze na nekim audiouređajima poput Bluetooth slušalica. (#14386, @jcsteh, @mltony)
* HP Secure Browser je sada podržan. (#16377)

### Izmjene

* Add-on Store:
  * Minimalna verzija i posljednja testirana verzija dodatka sada se prikazuju u području "više detalja". (#15776, @Nael-Sayegh)
  * Radnja "recenzije zajednice" biti će dostupna, a web stranica će se prikazati u pojedinostima u svim karticama svojstava u Add-on storeu. (#16179, @nvdaes)
* Nadogradnje komponenti:
  * Nadograđen LibLouis brajični prevoditelj na inačicu [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Dodane nove tablice sa prikazanim znakovima za velika slova za bjeloruski i ukrajinski, kao i brajična tablica za španjolski sa podrškom za čitanje grčkog teksta.
  * eSpeak NG je nadograđen  na inačicu 1.52-dev commit `cb62d93fd7`. (#15913)
    * Dodan je novi jezik: tigrinya. 
* Promijenjeno je nekoliko prečaca za brajični redke BrailleSense kako bi se izbjegli konflikti sa znakovima francuske brajične tablice. (#15306)
  * `alt+strelicaLijevo` sada je promijenjen na prečac `točkica2+točkica7+razmak`
  * `alt+strelicaDesno` sada je promijenjen u `točkica5+točkica7+razmaknica`
  * `alt+strelicaGore` sada je promijenjen u `točkica2+točkica3+točkica7+razmaknica`
  * `alt+StrelicaDolje` sada je promijenjen u `točkica5+točkica6+točkica7+razmaknica`
* Višetočja koja se često koriste u tablicama sadržaja više se ne čitaju pri niskim razinama interpunkcije. (#15845, @CyrilleB79)

### Ispravke grešaka

* Ispravke vezane uz Windows 11:
  * NVDA će opet izgovarati prijedloge za upisivanje kada se koristi hardverska tipkovnica. (#16283, @josephsl)
  * U inačici 24H2 (nadogradnji za 2024 godinu te Windows Server 2025), miš i dodirnik mogu se koristiti u brzim postavkama. (#16348, @josephsl)
* Add-on Store:
  * Kada se pritisne `ctrl+tab`, fokus se ispravno prebacuje na novi aktualni naslov kartice svojstva. (#14986, @ABuffEr)
* Ispravke za  preglednike bazirane na Chromiumu kada se korise uz pomoć Uia:
  * Ispravljene greške koje su prouzrokovale zaglavljivanje NVDA. (#16393, #16394)
  * Tipka Backspace sada ispravno radi U poljima za prijavu Gmail a. (#16395)
* Tipka backspace sada ispravno radi kada se koristi program Nudi 6.1 sa postavkom "rukuj tipkama iz drugih programa". (#15822, @jcsteh)
* Ispravljena je pogreška kada se reproduciraju zvučne koordinate kada se program nalazi u stanju mirovanja kada je opcija "Reproduciraj zvučne signale prilikom pomicanja miša" uključena. (#8059, @hwf1324)
* U Adobe Readeru, više se ne ignorira alternativni tekst na formulama u PDF datotekama. (#12715)
* Ispravljena je pogreška koja je onemogućavala čitanje opcija i ribbona u  Geekbenchu. (#16251, @mzanm)
* Ispravljen je rijedak slučaj nemogućnosti spremanja konfiguracije, kada se nisu spremali i konfiguracijski profili. (#16343, @CyrilleB79)
* U Firefoxu i preglednicima baziranima na Chromiumu, NVDA će ispravno aktivirati modus fokusa prilikom pritiska entera kad je fokus na prezentacijskom popisu (ul / ol) unutar sadržaja za uređivanje. (#16325)
* Stanje promjena stupaca kada se označuju stupci za prikaz u popisu poruka u Thunderbirdu sada se ispravno čitaju. (#16323)

## 2024.1

Dodan je novi modus govora čitanja informacija na zahtjev.
Kada je modus govora postavljen da izgovara informacije na zahtjev, NVDA ne čita informacije automatski na primjer prilikom pomicanja kursora, ali još uvijek izgovara informacije i koje se dobivaju uz pomoć prečaca, čiji je cilj izgovaranja određenih informacija na primjer, izgovaranje naslovne trake.
U kategoriji "govor" NVDA postavki, sada je moguće izostavljanje neželjenih modusa govora iz odabira modusa govora (`NVDA+s`).

Novi način kopiranja sa sačuvanim oblikovanjem, koji se poziva uz pomoć prečaca NVDA+f10 dostupan je na web stranicama u Mozilla Firefoxu.
Kada se uključi, koristit će se izvorno označavanje u Mozilli firefoxu.
Kopiranje teksta uz pomoć prečaca `control+c` biti će proslijeđeno direktno Mozilli firefoxu što znači da će tekst biti kopiran sa sačuvanim oblikovanjem, umjesto čistog teksta bez oblikovanja.

NVDA store sada podržava višestruke radnje na primjer: instaliranje ili uključivanje dodataka tako da se označi više dodataka
Dodana je nova radnja za otvaranje web stranice recenzija za bilo koji označeni dodatak.

Opcije odabira zvučne kartice i načina stišavanja govora su uklonjene iz dijaloškog okvira "odabir govorne jedinice".
Ove se opcije mogu pronaći u novom dijaloškom okviru postavki zvuka koji se poziva prečacem `NVDA+control+u`.

Nadograđeni su eSpeak-NG, LibLouis braille translator, i Unicode CLDR.
Dodane su nove brajične tablice za tajski, filipinski i rumunjski jezik.

Ispravljeno je puno pogrešaka, uglavnom u Add-on Storeu, podršci za brajicu, Libre Officeu, Microsoft Officeu i podršci za zvuk.

### Važne napomene

* Ova inačica narušava kompatibilnost sa postojećim dodacima.
* Windows 7, i Windows 8 više nisu podržani operacijski sustavi.
Windows 8.1 je minimalna verzija operacijskog sustava Windows.

### Nove značajke

* Add-on Store:
  * Add-on Store sada podržava višestruke radnje na primjer instaliranje, uključivanje više dodataka) tako da se odabere više dodataka. (#15350, #15623, @CyrilleB79)
  * Dodana je opcija koja služi za davanje povratne informacije o dodacima putem posebne web stranice za svaki dodatak. (#15576, @nvdaes)
* Dodana podrška za Bluetooth niskonaponske brajične redke. (#15470)
* Dodano je kopiranje sa sačuvanim oblikovanjem (koje se uključuje ili isključuje uz pomoć prečaca `NVDA+shift+f10`) na web stranicama u Mozilla firefoxu.
Kada je uključeno, koristit će se izvorno označavanje u Mozilla firefoxu.
Prilikom kopiranja teksta uz pomoć prečaca `control+c` biti će proslijeđeno izravno Firefoxu, što će kopirati i formatiranje, a ne samo oblikovanje.
Imajte na umu da prilikom kopiranja teksta i njegovim rukovanjem od strane Firefoxa, NVDA neće izgovoriti poruku "kopirano u međuspremnik". (#15830)
* Prilikom kopiranja teksta u Microsoft Wordu sa uključenim načinom čitanja, oblikovanje će se također kopirati.
Posljedica ovoga je da NVDA neće izgovarati poruku "kopirano u međuspremnik" kada se pritisne `control+c` u Microsoft wordu ili Outlooku, zbog toga što aplikacija upravlja kopiranjem., umjesto NVDA. (#16129)
* Dodan je novi modus govora "na zahtjev".
Kada je govor podešen na zahtjev, NVDA neće govoriti automatski (na primjer, prilikom pomicanja kursora) ali govori kada se pozivaju prečaci čiji je cilj čitanje određene informacije (na primjer izgovaranje naslovne trake). (#481, @CyrilleB79)
* U kategoriji govor postavki NVDA, sada je moguće isključiti neželjene moduse govora iz odabira prečacem odabira modusa govora (`NVDA+s`). (#15806, @lukaszgo1)
  * Ako koristite dodatak NoBeepsSpeechMode razmislite o njegovom uklanjanju, i onemogućavanjem "zvučnih signala" "i načina na zahtjev" u postavkama.

### Izmjene

* NVDA više ne podržava Windows 7 i Windows 8.
Windows 8.1 je minimalna podržana verzija sustava Windows. (#15544)
* Nadogradnje komponenata:
  * Nadograđen LibLouis brajični prevoditelj na inačicu [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Dodane nove brajične tablice za Tajski, Rumunjski i Filipinski.
  * eSpeak NG je nadograđen na 1.52-dev commit `530bf0abf`. (#15036)
  * Prijevodi simbola i Emoji znakova su nadograđeni na verziju 44.0. (#15712, @OzancanKaratas)
  * Nadograđena Java Access Bridge na 17.0.9+8Zulu (17.46.19). (#15744)
* Tipkovnički prečaci:
  * Slijedeći tipkovnički prečaci od sada podržavaju dvostruke i trostruke pritiske za slovkanje informacije, te sricanje uz pomoć fonetskog opisa znakova: čitaj označeni tekst, čitaj tekst u međuspremniku i čitaj fokusirani objekt. (#15449, @CyrilleB79)
  * Prečac za uključivanje i isključivanje zaslonske zavjese sada ima podrazumjevani tipkovnički prečac: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * Kada se pritisne četiri puta, prečac za čitanje označenog teksta sada prikazuje označeni tekst u poruci koja se može pročitati. (#15858, @Emil-18)
* Microsoft Office:
  * Kada treba pročitati oblikovanje ćelije u Excelu pozadina i rubovi biti će pročitani samo ako takvo oblikovanje postoji. (#15560, @CyrilleB79)
  * NVDA više neće čitati neoznačene grupe kao što su to u posljednjim inačicama Microsoft Office 365 izbornicima. (#15638)
* Opcija za odabir zvučne kartice i opcije načina stišavanja govora uklonjene su iz dijaloškog okvira "Odabir govorne jedinice".
Možete ih pronaći u panelu postavki zvuka koji se može otvoriti pritiskom prečaca `NVDA+control+u`. (#15512, @codeofdusk)
* Opcija "Izgovori tip objekta kada se nađe pod mišem" u postavkama miša je preimenovan u "Pročitaj objekt kada se nađe pod mišem".
Ova opcija izgovara više relevantnih informacija kada se objekt nađe pod mišem poput stanja: označeno ili pritisnuto ili koordinate ćelija u tablici. (#15420, @LeonarddeR)
* Nove stavke su dodane u izbornik pomoć Pomoć obuka i podrška i NV acces trgovina. (#14631)
* Podrška NVDA za [Poedit](https://poedit.net) je kompletno prepisana za inačicu 3 i novije.
Korisnicima Poedita  1 se preporučuje nadogradnja na Poedit 3 ako žele koristiti unapređenu pristupačnost Poedita, kao što su to prečaci za čitanje bilježaka za prevoditelje i komentara. (#15313, #7303, @LeonarddeR)
* Preglednik brajice i preglednik govora od sada su isključeni u Sigurnom načinu. (#15680)
* Prilikom korištenja objektne navigacije, onemogućeni (nedostupni) objekti više neće biti ignorirani. (#15477, @CyrilleB79)
* Dodan sadržaj u dokument "popis tipkovničkih prečaca". (#16106)

### Ispravke grešaka

* Add-on Store:
  * Ako je status dodatka promijenjen kada se nalazi u fokusu, na primjer promjena iz "preuzimanje" u "preuzeto", osvježena se stavka sada potpuno izgovara. (#15859, @LeonarddeR)
  * Prilikom instalacije dodataka instalacijska pitanja se više ne prekrivaju dijaloškim okvirom ponovnog pokretanja. (#15613, @lukaszgo1)
  * Prilikom reinstalacije nekompatibilnog dodatka isti se neće nasilno onemogućavati. (#15584, @lukaszgo1)
  * Onemogućeni i nekompatibilni dodaci se sada mogu ažurirati. (#15568, #15029)
  * NVDA se sada obnavlja i pokazuje grešku u slučaju neuspješnog preuzimanja dodatka. (#15796)
  * NVDA se više ne pokreće ponovno poslije ponovnog otvaranja i zatvaranja Add'on storea. (#16019, @lukaszgo1)
* Zvuk:
  * NVDA se više ne smrzava kada se zvukovi reproduciraju brzo. (#15311, #15757, @jcsteh)
  * Ako je zvučna kartica postavljena na jednu od onih koja nije podrazumijevana a ta kartica postane dostupna, NVDA će se prebaciti na tu zvučnu karticu. (#15759, @jcsteh)
  * NVDA će sada ponovno reproducirati zvuk ako konfiguracija zvučne kartice bude promijenjena ili druga aplikacija prestane ekskluzivno koristiti zvučnu karticu. (#15758, #15775, @jcsteh)
* Brajica:
  * Višeredni brajični redci više neće dovesti upravljački program BRLTTY do rušenja, te su tretirani kao jedan kontinuirani brajični redak. (#15386)
  * Od sada se na brajičnom redku prikazuju objekti koji sadrže koristan tekst. (#15605)
  * Sada ponovno radi upisivanje brajičnih znakova kada se koristi kratkopis. (#15773, @aaclause)
  * Od sada se brajica osvježava prilikom pomicanja objekta navigatora u više situacija (#15755, @Emil-18)
  * Rezultati izgovora trenutnog fokusa, trenutnog objekta navigatora i trenutnog označavanja sada se prikazuju na brajičnom redku. (#15844, @Emil-18)
  * Albatross upravljački program više ne prepoznaje Esp32 mikrokontroler kao Albatross brajični redak. (#15671)
* LibreOffice:
  * Riječi izbrisane uz pomoć prečaca `control+backspace` sada se također ispravno izgovaraju kada nakon izbrisane riječi slijedi bjelina (razmaci i tabulatori). (#15436, @michaelweghorn)
  * Čitanje trake stanja koristeći tipkovnički prečac `NVDA+end` sada također radi u Libre office dialoškim okvirima u inačicama 24.2 i novijim. (#15591, @michaelweghorn)
  * Svi očekivani atributi teksta sada su podržani U Libreoffice inačicama 24.2 i novijim.
  Ova ispravka omogućuje čitanje pravopisnih pogrešaka prilikom čitanja redaka u Writeru. (#15648, @michaelweghorn)
  * Čitanje razine naslova sada također radi u LibreOfficeu inačicama 24.2 i novijim. (#15881, @michaelweghorn)
* Microsoft Office:
  * U Excelu sa isključenim UIA, brajica se osvježava, a aktivni sadržaj ćelije se izgovara, kada se pritisne `control+y`, `control+z` ili `alt+backspace`. (#15547)
  * U Wordu sa isključenim Uia brajica se osvježava kada se pritisnu `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace` ili `control+backspace`.
  Također se osvježava kada je UIA omogućen, kada se  upisuje tekst, a brajica je povezana na pregled a pregled prati kursor sustava. (#3276)
  * U Wordu, trenutna ćelija će se izgovoriti koristeći izvorne prečace Worda za navigaciju po tablicama `alt+home`, `alt+end`, `alt+pageUp` and `alt+pageDown`. (#15805, @CyrilleB79)
* Izgovaranje tipkovničkih prečaca je unapređeno. (#10807, #15816, @CyrilleB79)
* SAPI4 govorne jedinice sada pravilno podržavaju promjene glasnoće, brzine i visine ugrađene u govor. (#15271, @LeonarddeR)
* Stanje višerednog objekta sada se pravilno čita u aplikacijama koje koriste Java Access Bridge. (#14609)
* NVDA će sada čitati više sadržaja dijaloških okvira za više Windows 10 i 11 dijaloških okvira. (#15729, @josephsl)
* NVDA će sada čitati novu učitanu stranicu u Microsoft Edgeu prilikom korištenja UI automation. (#15736)
* Prilikom korištenja prečaca za čitanje cijelog teksta ili slovkanja teksta, pauze između rečenica ili znakova više se ne smanjuju postupno tokom vremena. (#15739, @jcsteh)
* NVDA više se ne smrzava prilikom čitanja velike količine teksta. (#15752, @jcsteh)
* Prilikom pristupanja Microsoft Edgeu koristeći UI automation, NVDA sada može aktivirati više kontrola u modusu čitanja. (#14612)
* NVDA će se sada pokretati ispravno kada je konfiguracijska datoteka oštećena, ali će se konfiguracija vratiti na zadane vrijednosti kao što je to bilo i u prošlosti. (#15690, @CyrilleB79)
* Ispravljena podrška za System List view (`SysListView32`) kontrole U Windows forms aplikacijama. (#15283, @LeonarddeR)
* Sada nije više moguće nadpisivanje NVDA povijesti Python konzole. (#15792, @CyrilleB79)
* NVDA će ostati brz i stabilan kada postane preopterećen sa UI automation događajima, na primjer prilikom prikazivanja velike količine teksta u Windows terminalu ili prilikom slušanja glasovnih poruka u  WhatsAppu. (#14888, #15169)
  * Ovo novo ponašanje može se isključiti koristeći opciju "Koristi unapređeno procesuiranje događaja" u NVDA naprednim postavkama.
* NVDA sada ponovno može slijediti fokus u aplikacijama unutar Windows defender application guarda (WDAG). (#15164)
* Izgovoreni tekst se više ne ažurira prilikom pomicanja miša u Pregledniku govora. (#15952, @hwf1324)
* NVDA će se opet prebaciti u modus čitanja prilikom zatvaranja odabirnih okvira koristeći tipku `escape` ili `alt+strelicu gore` u Firefox ili Chrome. (#15653)
* Kretanje strelicama gore ili dolje u iTunesu više se neće prebacivati nazad u modus čitanja. (#15653)

## 2023.3.4

Ovo je verzija zakrpe koja ispravlja problem s instalacijom i jedan skgurnosni prropust.
Molimo odgovorno izvještavajte o sigurnosnim propustima prateći [NVDA politiku sigurnosti](https://github.com/nvaccess/nvda/blob/master/security.md).

### Ispravke sigurnosti

* Onemogućeno učitavanje koda prilikom prisilnog uključivanja sigurnog načina.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Ispravke grešaka

* Ispravljena greška prilikom koje NVDA proces se nije mogao ispravno prekinuti. (#16123)
* Ispravljena pogreška, prilikom koje ako prethodni NVDA proces NVDA se neuspješno prekine, NVDA instalacija može završiti i stanju neoporavljivosti. (#16122)

## 2023.3.3

Ovo je verzija zakrpe koja ispravlja sigurnosni propust.
Molimo odgovorno prijavljujte probleme sigurnosti u skladu sa NVDA [politikom sigurnosti](https://github.com/nvaccess/nvda/blob/master/security.md).

### Ispravke sigurnosnih propusta

* Prevencija mogućeg povratnog XSS izgrađenog koda koji prouzrokuje arbitrarno izvršavanje koda.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Ovo je verzija zakrpe koja ispravlja sigurnosni propust.
Sigurnosni propust iz verzije 2023.3.1 nije bio implementiran ispravno.
Molimo odgovorno prijavljujte probleme sigurnosti u skladu sa NVDA [politikom sigurnosti](https://github.com/nvaccess/nvda/blob/master/security.md).

### Ispravke sigurnosti

* Sigurnosni propust iz verzije 2023.3.1 nije bio implementiran ispravno.
Prevenira mogući pristup sustavu i arbitrarno pokretanje koda sa privilegijama sustava za neautentificirane korisnike.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Ovo je verzija zakrpe koja ispravlja sigurnosni propust.
Molimo odgovorno prijavljujte probleme sigurnosti u skladu sa NVDA [politikom sigurnosti](https://github.com/nvaccess/nvda/blob/master/security.md).

### Ispravke sigurnosti

* Prevenira mogući pristup sustavu i arbitrarno pokretanje koda sa privilegijama sustava za neautentificirane korisnike.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Ova inačica uključuje poboljšanja stabilnosti i performansi pri izlazu zvuka.
Dodane su opcije za kontrolu glasnoće NVDA zvukova i zvučnih signala, ili ujednačavanja sa glasnoćom glasa koji koristite.

NVDA može s vremena na vrijeme osvježavati rezultate prepoznavanja teksta kada se pojave.
Ovo se može konfigurirati u Windows OCR kategoriji u dijaloškom okviru postavki NVDA.

Dodane su ispravke za brajične redke, uključujući automatsko otkrivanje.
Sada je moguće isključiti upravljačke programe iz procesa automatskog otkrivanjau cilju poboljšanja performansi.
Dodane su također nove komande za Brltty.

Ispravljene su greške u Add-on Storeu, Microsoft Officeu, Microsoft Edge kontekstnim izbornicima i u Windows kalkulatoru.

### Nove značajke

* Unapređeno upravljanje zvukom:
  * Novi panel postavki zvuka:
    * Može se otvoriti tipkovničkim prečacom `NVDA+control+u`. (#15497)
    * Opcija koja omogućuje ujednačavanje glasnoće zvukova sa glasnoćom govorne jedinice koju koristite. (#1409)
    * Opcija za odvojenu konfiguraciju glasnoće NVDA zvukova. (#1409, #15038)
    * Opcije za promjenu zvučne kartice i utišavanje zvukova premještene su u novu kategoriju postavki zvuka iz dijaloškog okvira odabira govorne jedinice.
Ove će opcije biti uklonjene iz dijaloškog okvira  "odaberi govornu jedinicu" u inačici 2024.1. (#15486, #8711)
   -
  * Upozorenje: WASAPI je nekompatibilan sa nekim dodacima.
  Dostupne su kompatibilne nadogradnje tih dodataka, Nadogradite ih prije nadogradnje NVDA.
  Nekompatibilne verzije tih dodataka bit će isključene prilikom nadogradnje NVDA:
    * Tony's Enhancements inačica 1.15 ili starija. (#15402)
    * NVDA global commands extension 12.0.8 ili starija. (#15443)
* NVDA sada može kontinuirano osvježavati rezultat prepoznavanja teksta kada se pojavi novi tekst. (#2797)
  * Kako biste uključili ovu opciju, molimo uključite opciju "S vremena na vrijeme osvježavaj sadržaj prepoznavanja" u kategoriji Windows Ocr u NVDA postavkama.
  * Kada je ova opcija uključena, možete uključiti ili isključiti izgovor novog teksta tako da uključite ili isključite čitanje dinamičkog sadržaja (pritiskom `NVDA+5`).
* Prilikom korištenja automatskog otkrivanja brajičnih redaka, sada je moguće onemogućiti upravljačke programe sa popisa automatski otkrivanih u dijaloškom okviru izbora brajičnog redka. (#15196)
* Nova opcija u opcijama oblikovanja dokumenta, "Ignoriraj prazne redke prilikom čitanja uvlačenja". (#13394)
* Dodana nedodijeljena gesta za kretanje po grupiranjima kartica svojstva u načinu pregleda. (#15046)

### izmjene

* Brajica:
  * Kada se tekst u naredbenom redku promijeni bez promjene fokusa, tekst na brajičnom redku će se također obnoviti kada se nalazite na tom redku.
  Ovo uključuje situacije kada je brajica povezana na pregled. (#15115)
  * Više Brltty prečaca je povezana sa NVDA prečacima (#6483):
    * `learn`: uključi isključi pomoć pri unosu
    * `prefmenu`: otvori nVDA izbornik
    * `prefload`/`prefsave`: učitaj spremi NVDA konfiguraciju
    * `time`: pokaži vrijeme
    * `say_line`: Izgovori redak na kojem se nalazi pregledni kursor
    * `say_below`: Čitaj sve koristeći pregledni kursor
  * BRLTTY upravljački program je dostupan samo kada je Brltty pokrenut sa BRL api. (#15335)
  * Napredna postavka za isključivanje HID brajičnog redka  sada je uklonjena i zamijenjena novom opcijom.
  Sada možete isključiti određene upravljačke programe za automatsko prepoznavanje u dijaloškom okviru brajičnih postavki. (#15196)
* Add-on Store: dodaci će sada biti dostupni na kartici svojstva dostupnih dodataka, ako su dostupni u Add-on storeu. (#15374)
* Osvježeni su neki prečaci u NVDA izborniku. (#15364)

### Ispravke grešaka

* Microsoft Office:
  * Ispravljeno rušenje u Microsoft Word Kada su opcije u postavkama oblikovanja "čitaj naslove" i "čitaj komentare i bilješke" isključene. (#15019)
  * U Wordu i Excelu, poravnanje će biti ispravno pročitano u više situacija. (#15206, #15220)
    * Ispravljeno čitanje nekih prečaca oblikovanja u Excelu. (#15527)
  -
* Microsoft Edge:
  * NVDA se više neće vraćati na prethodnu poziciju u modusu čitanja pri otvaranju kontekstnog izbornika u Microsoft Edgeu. (#15309)
  * NVDA opet može čitati kontekstni izbornik preuzimanja u Microsoft Edgeu. (#14916)
* Brajica:
  * Brajični kursor i pokazivač označenosti bit će ispravno osvježeni poslije uključenja ili isključenja gestom. (#15115)
  * Ispravljena pogreška prilikom koje su se Albatros brajični redci pokušali inicijalizirati čak iako je drugi brajični redak bio spojen. (#15226)
* Add-on Store:
  * Ispravljena greška poslije odznačavanja "uključi nekompatibilne dodatke" koja je prouzrokovala vidljivost nekompatibilnih dodataka. (#15411)
  * Dodaci blokirani zbog nekompatibilnosti bi se sada trebali pravilno osvježavati prilikom sortiranja po statusu uključenosti ili isključenosti. (#15416)
  * Ispravljena pogreška nadpisivanja ili nadogradnje dodataka koristeći ručnu instalaciju. (#15417)
* Ispravljena pogreška prilikom koje NVDA neće govoriti poslije ponovnog pokretanja i završetka NVDA instalacije. (#14525)
  * Ispravljena pogreška  pri instalaciji dodataka ako je prethodna instalacija ili preuzimanje prekinuto. (#15469)
* Ispravljene pogreške s rukovanjem nekompatibilnim dodacima pri nadogradnji NVDA. (#15414, #15412, #15437)
  -
* NVDA opet izgovara rezultate računskih operacija u 32-bitnom kalkulatoru za Windows u operacijskim sustavima Server, LTSC and LTSB. (#15230)

* NVDA više ne ignorira izmjene fokusa kada višeslojni prozor (prozor koji se nalazi iznad drugog prozora) postane fokusiran. (#15432)
* Ispravljeno moguće rušenje prilikom pokretanja NVDA. (#15517)

## 2023.2

Ova verzija dodaje add-on store koja Zamjenjuje upravljanje dodacima.
U  dAdd-on storeu možete pregledavati, pretraživati, instalirati i ažurirati dodatke zajednice.
Sada možete ručno ignorirati probleme kompatibilnosti sa zastarjelim dodacima na vlastitu odgovornost.

Dodane su nove funkcije za brajične redke, prečice i novi podržani brajični redci.
Također su dodate nove prečice za OCR i rasklopljeni prikaz kroz objekte.
Navigacija i čitanje oblikovanja u Microsoft Office paketu je poboljšana.

Puno grešaka je ispravljeno, posebno za brajične redke, Microsoft Office, web preglednike i Windows 11.

eSpeak-NG, LibLouis braille translator, i Unicode CLDR su ažurirani.

### Nove značajke

* Add-on store je dodan u NVDA. (#13985)
  * Pregled, pretraga, instalacija i ažuriranje dodataka zajednice.
  * Ručno učitajte nekompatibilne NVDA dodatke.
  * upravitelj dodacima je uklonjen i zamenjen add-on store.
  * za više informacija molimo pročitajte ažurirani korisnički priručnik.
* Nove Novi prečaci:
  * Nova ulazna gesta bez dodijeljenog prečaca za kruženje kroz dostupne jezike za Windows OCR. (#13036)
  * nova ulazna gesta bez dodijeljenog prečaca za kruženje kroz moduse prikazivanja poruka na brajičnom redku. (#14864)
  * Ulazna gesta bez dodijeljenog prečaca za uključivanje ili isključivanje indikacije označavanja. (#14948)
  * Dodani podrazumjevani prečaci na tipkovnice za kretanje na sljedeći ili prethodni objekt u raskropljenom prikazu hierarhije objekata. (#15053)
    * stolno računalo: `NVDA+numerički9` i `NVDA+numerički3` za kretanje na slijedeći ili prethodni objekt.
    * prijenosno računalo: `šift+NVDA+[` i `šift+NVDA+]` za kretanje na prethodni i slijedeći objekt.
  -
  -
* Nove funkcije za brajične retke:
  * Dodana podrška za Help Tech Activator brajični redak. (#14917)
  * Nova opcija za uključivanje ili isključivanje prikazivanja indikacije označenosti (točkice 7 i 8). (#14948)
  * Nova opcija za pomicanje kursora sustava ili fokusa pri promjeni pozicije preglednog kursora gumbima na brajičnom redku. (#14885, #3166)
  * Kada se pritisne `numerički2` tri puta za čitanje brojčane vrijednosti znaka na poziciji preglednog kursora, informacija se također pruža na brajičnom redku. (#14826)
  * Dodata podrška za `aria-brailleroledescription` ARIA 1.3 atribut, koji će dozvoliti autorima web stranica zamjenu vrste elementa koja će se prikazati na brajičnom redku. (#14748)
  * Upravljački program za Baum brajične redke: Dodano nekoliko vezanih brajičnih prečaca za izvršavanje čestih prečica na tastaturi kao što su `windows+d` i `alt+tab`.
  Molimo pogledajte NVDA korisničko uputstvo za potpun popis. (#14714)
* Dodan izgovor Unicode znakova:
  * brajični znakovi kao što su `⠐⠣⠃⠗⠇⠐⠜`. (#14548)
  * Znak za Mac tipku opcije `⌥`. (#14682)
-
* Dodani prečaci za Tivomatic Caiku Albatross brajične redke. (#14844, #15002)
  * prikaz dijaloškog okvira brajičnih postavki
  * Pristup traci stanja
  * promjena oblika brajičnog kursora
  * promjena modusa prikazivanja poruka
  * Uključivanje i isključivanje brajičnog kursora
  * Uključivanje i isključivanje kursora označavanja na brajičnom redku
  * Promjena opcije "Pomakni kursor sustava prilikom usmjeravanja kursora pregleda ". (#15122)
* Značajke Microsoft Office:
  * Kada se omogući čitanje istaknutog teksta u opcijama oblikovanja dokumenta, boje isticanja se sada čitaju u Microsoft Wordu. (#7396, #12101, #5866)
  * Kada se uključi čitanje boja u opcijama oblikovanja dokumenta, boje pozadine se sada čitaju u Microsoft Wordu. (#5866)
  * Kada se koriste Excel prečaci za uključivanje ili isključivanje opcija oblikovanja poput podebljanih, kosih, podcrtanih i prekriženih slova za ćeliju u Excelu, rezultat se sada čita. (#14923)
-
* Eksperimentalno poboljšano upravljanje zvukom:
  * NVDA sada može reproducirati zvukove putem standarda Windows Audio Session API (WASAPI), što može poboljšati brzinu, performanse i stabilnost NVDA govora i zvukova.
  * Korištenje WASAPI se može omogućiti u naprednim postavkama.
  Također, ako je WASAPI omogućen, sljedeće napredne postavke se mogu regulirati.
    * Opcija koja prouzrokuje praćenje glasnoće NVDA govornog izlaza i zvučnih signala. (#1409)
    * Opcija za odvojeno postavljanje glasnoće NVDA zvukova. (#1409, #15038)
  * Postoji poznat problem sa povremenim rušenjem kada je WASAPI omogućen. (#15150)
* U preglednicima Mozilla Firefox i Google Chrome, NVDA sada čita ako kontrola otvara dijaloški okvir, mrežu, popis ili stablasti prikaz ako je autor ovo označio uz pomoć `aria-haspopup` atributa . (#14709)
* Sada je moguće koristiti varijable  sustava (poput  `%temp%` ili  `%homepath%`) pri određivanju putanje pri stvaranju NVDA prijenosne kopije. (#14680)
* Dodana podrška za brajični redak Help Tech Activator. (#14917)
* u ažuriranju Windowsa 10 za svibanj 2019 i novijim, NVDA može izgovarati imena virtualnih radnih površina kada se otvaraju, mijenjaju ili zatvaraju. (#5641)
* Dodan je sveopći parametar sustava koji će dozvoliti korisnicima i administratorima sustava prisilno pokretanje NVDA u sigurnom modusu. (#10018)

### Izmjene

* Ažurirane komponente:
  * eSpeak NG je ažuriran na inačicu 1.52-dev commit `ed9a7bcf`. (#15036)
  * Ažuriran LibLouis brajični prevoditelj na inačicu [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR je ažuriran na inačicu 43.0. (#14918)
* Izmjene u LibreOffice paketu:
  * Kada se čita pozicija preglednog kursora, trenutna pozicija kursora se sada čita u odnosu na trenutnu stranicu u programu LibreOffice Writer za LibreOffice inačicu 7.6 i novije, slično čitanju u programu Microsoft Word. (#11696)
  * Kada se prebacite na neku drugu ćeliju u programu LibreOffice Calc, NVDA više neće neispravno izgovarati koordinate prethodno fokusirane ćelije kada se izgovor koordinata ćelija onemogući u NVDA postavkama. (#15098)
  * Izgovor trake stanja (na primjer kada se pritisne `NVDA+end`) radi u paketu LibreOffice. (#11698)
* Promjene za brajične redke:
  * Kada se koristi brajični redak uz pomoć za Hid brajični standard, dpad se sada može koristiti za emuliranje strelica tipkovnice i entera.
Takođe,  `razmaknica+točka1` i `razmaknica+točka4` sada se koriste kao strelice dole i gore. (#14713)
  * Ažuriranja dinamičkog sadržaja na Web stranicama (ARIA žive regije) se sada prikazuju na brajičnom redku.
Ovo se može onemogućiti na panelu naprednih postavki. (#7756)
-
* Simboli crtica i spojnica će uvijek biti poslani sintetizatoru. (#13830)
* Udaljenost koju Microsoft Word čita će sada poštovati mjernu jedinicu koja je postavljena u naprednim postavkama Worda čak i kada se koristi UIA za pristup Word dokumentima. (#14542)
* NVDA brže reagira kada se pomiće kursor u kontrolama za uređivanje. (#14708)
* Skripta za prijavljivanje odredišta poveznice sada čita sa pozicije kursora ili fokusa umesto objekta navigatora. (#14659)
* Stvaranje prenosne kopije više ne zahtijeva upisivanje slova diska kao dio apsolutne putanje. (#14680)
* Ako je Windows postavljen da prikazuje sekunde na satu područja obavijesti, korištenje prečaca `NVDA+f12` za čitanje vremena sada prati ovo podešavanje. (#14742)
* NVDA će sada prijavljivati grupe bez oznake koje imaju korisne informacijje o poziciji, kakve se mogu pronaći u novijim  inačicama Microsoft Office 365 izbornika. (#14878) 

### Ispravke grešaka

* Brajični redci:
  * Nekoliko poboljšanja u stabilnosti unosa/prikaza na brajičnom redku, što će smanjiti učestalost grešaka i rušenja programa NVDA. (#14627)
  * NVDA se više neće bespotrebno prebacivati na opciju bez brajice više puta u toku automatskog prepoznavanja, što donosi zapisnike i manje opterećenje. (#14524)
  * NVDA će se sada prebacivati na USB ako HID Bluetooth uređaj (kao što je HumanWare Brailliant ili APH Mantis) automatski bude prepoznat i USB veza postane dostupna.
  Ovo je ranije radilo samo za Bluetooth serijske portove. (#14524)
  * Kada nijedan brajični redak nije povezan i preglednik brajičnog redka se zatvori pritiskanjem `alt+f4` ili klikom na gumb zatvori, veličina brajevog podsistema će ponovo biti vraćena na bez ćelija. (#15214)
* Web preglednici:
  * NVDA više neće ponekad izazivati rušenje ili prestanak rada programa Mozilla Firefox. (#14647)
  * U pretraživačima Mozilla Firefox i Google Chrome, upisani znakovi se više ne prijavljuju u nekim poljima za unos teksta čak i kada je izgovor upisanih znakova isključen. (#8442)
  * Sada možete koristiti modus pretraživanja u Chromium umetnutim kontrolama u kojima to ranije nije bilo moguće. (#13493, #8553)
  * U Mozilli Firefox, pomicanje miša do teksta nakon linka sada ispravno čita tekst. (#9235)
  * Odredište linkova na slikama se sada preciznije ispravno čita u većini slučajeva u programima Chrome i Edge. (#14779)
  * Kada pokušavate čitati adresu poveznice bez href atributa NVDA više neće biti bez govora.
  Umesto toga NVDA će prijaviti da poveznica  nema odredište. (#14723)
  * U modusu pretraživanja, NVDA neće neispravno ignorirati pomeranje fokusa na glavnu kontrolu ili kontrolu unutar nje na primer pomicanje sa kontrole na njenu unutrašnju stavku popisa ili ćeliju mreže. (#14611)
   * Napomena međutim da se ova ispravka primenjuje samo kada je opcija "Automatsko postavljanje fokusa na stavke koje se mogu fokusirati" u postavkama modusa pretraživanja isključena (što je podrazumevano postaka).
    -
-
* Ispravke za Windows 11:
  * NVDA ponovo može izgovarati sadržaj trake stanja u bloku za pisanje. (#14573)
  * Prebacivanje između kartica će izgovoriti ime i poziciju nove kartice u bloku za pisanje i upravitelju datoteka. (#14587, #14388)
  * NVDA će ponovo izgovarati dostupne unose kada se tekst piše na jezicima kao što su Kineski i Japanski. (#14509)
  * Ponovo je moguće otvoriti popis doprinositelja ili licencu iz menija NVDA pomoći. (#14725)
* Microsoft Office ispravke:
  * Kada se brzo krećete kroz ćelije u Excelu, manja je vjerojatnost prijavljivanja pogrešne ćelije ili pogrešnog odabira. (#14983, #12200, #12108)
  * Kada stanete na Excel ćeliju van radnog lista, brajični redak i označavanje fokusa se više neće bespotrebno ažurirati na objekt koji je ranije bio fokusiran. (#15136)
  * NVDA sada uspješno izgovara fokusiranje na polja za lozinke u programima Microsoft Excel i Outlook. (#14839)
* Za simbole koji nemaju opis na trenutnom jeziku, podrazumjevana Engleska razina simbola će se koristiti. (#14558, #14417)
* Sada je moguće koristiti znak obrnuta kosa crta u polju zamjene unosa rječnika, kada tip nije postavljen kao pravilni izraz. (#14556)
* U kalkulatoru u  Windowsima 10 i 11, a prijenosna kopija NVDA će pravilno čitati izraze u kompaktnom načinu. (#14679)
* NVDA se ponovo oporavlja u brojnim slučajevima kao što su aplikacije koje više ne reagiraju, što je ranije izazivalo da NVDA u potpunosti prestane raditi. (#14759) 
* Kada želite prisilno koristitiUIA podršku u određenim Terminalima i konzolama, ispravljena je greška koja je izazivala rušenje i neprestano pisanje podataka  u zapisniku. (#14689)
* NVDA više neće odbijati spremanje konfiguracije nakon vraćanja postavki na tvorničke. (#13187)
* Kada se pokreće privremena kopija iz instalacije, NVDA neće korisnicima davati pogrešne informacije da postavke mogu biti spremljena. (#14914)
* NVDA sada brže reagira na prečace i promjene fokusa. (#14928)
* Prikazivanje OCR postavki više neće biti neuspješno na nekim sistemima. (#15017)
* Ispravljena greška vezana za spremanje i vraćanje NVDA postavki, uključujući promjenu sintetizatora. (#14760)
* Ispravljena greška koja je izazvala da u pregledu teksta pokret "Povlačenje gore" pomiće stranice umjesto prelaska na prethodni redak. (#15127)
 - 

## 2023.1

Dodana je nova opcija, "stil odlomka" u kategoriji "kretanje po dokumentu".
Ona se može koristiti u tekstualnim editorima koji ne podržavaju nativno kretanje po odlomcima, kao što su to Notepad i Notepad++.

Dodan je novi prečac za čitanje odredišta na koje vodi poveznica, određen kao `NVDA+k`.

Podrška za anotiran web sadržaj (poput komentara i rubnih bilježaka) je unaprijeđena.
Pritišćite `NVDA+d` kako biste se kretali po sadržajima (na primjer "ima komentar, ima rubnu bilješku").

Tivomatic Caiku Albatross 46/80 brajični redci su sada podržani.

Podrška za ARM64 i AMD64 inačica sustava Windows je unapređena.

Ispravljeno je mnoštvo grešaka, među kojima ispravke za Windows 11 čine većinu.

eSpeak, LibLouis, Sonic povećivač brzine i Unicode su ažurirani.
Dodane su nove brajične tablice za gruzijski, Swahili (Kenija) i Chichewa (Malawi).

Upozorenje:
U ovoj inačici narušena je kompatibilnost s postojećim dodacima.
-

### Nove značajke

* Microsoft Excel s sučeljem UI automation: automatsko čitanje zaglavlja i stupaca tablica. (#14228)
  * Upozorenje: ovo se odnosi na tablice oblikovane uz pomoć gumba "tablica" na kratici umetanje na ribbonu.
  "prvi stupac" i "zaglavlje redka" u "opcijama stila tablice" odnose se na zaglavlja redaka i stupaca.
  * Ovo se ne odnosi na specifična zaglavlja čitača zaslona  uz pomoć imenovanih raspona, koje se ne podržavaju uz pomoć UI automation.
* Dodan je nedodijeljen prečac za uključivanje i isključivanje opisa znakova poslije kursora. (#14267)
* Dodana je podrška za čitanje sadržaja naredbenog redka uz pomoć UIA obavijesti, što ima za cilj unađređenje stabilnosti i responsivnosti. (#13781)
  * Kako biste saznali koja su ograničenja ove opcije, molimo pogledajte korisnički vodič za više informacija.
* U Windowsima 11 ARM64, modus pregleda je sada dostupan u AMD64 aplikacijama poput Firefoxa, Google Chromea i 1Passworda. (#14397)
* Nova opcija je dodana, "Stil odlomaka" u kategoriji "kretanje po dokumentu".
Ovo dodaje podršku za kretanje po pojedinačnim prijelomima redka (normalnim) i višerednim prijelomima redka (blokovnim). 
Ovo se može koristiti sa editorima teksta koji ne podržavaju kretanje po odlomcima nativno, kao što su to Notepad i Notepad++. (#13797)
* Izgovarana je prisutnost više anotacija.
`NVDA+d` sada prebacuje između izgovora sadržaja svake ciljne anotacije za izvore sa višestrukim ciljnim anotacijama.
Na primjer, kada tekst sadrži komentar i fusnotu. (#14507, #14480)
* Dodana je podrška za Tivomatic Caiku Albatross 46/80 brajične redke. (#13045)
* Novi globalni prečac: Čitaj odredište poveznice (`NVDA+k`).
Kada se pritisne jednom odredište linka koje se nalazi u objektu navigatora će biti izgovoreno i i prikazano na brajičnom redku.
Kada se pritisne dvaput, poveznica će biti prikazana u prozoru u svrhu detaljnijeg pregleda. (#14583)
* Nova nedodijeljena gesta (u kategoriji alati): je dodana prikaži odredište poveznice u prozoru.
Isto kao pritisak `NVDA+k` dvaput, ali može biti korisnije za korisnike brajice. (#14583)

### Izmjene

* nadograđen LibLouis brajični prevoditelj na  inačicu [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Drastično su osvježene Mađarska, univerzalna engleska, i kineska bopomofo brajična tablica.
  * Podržan je danski brajični standard, koji se promijenio u  2022 godini.
  * Nove brajične tablice za gruzijsku literarnu brajicu, Swahili (Kenija) i Chichewa (Malawi).
* Nadograđena biblioteka Sonic za ubrzanje govora na inačicu `1d70513`. (#14180)
* CLDR je nadograđen na inačicu 42.0. (#14273)
* eSpeak NG je nadograđen na inačicu 1.52-dev commit `f520fecb`. (#14281, #14675)
  * Ispravljeno čitanje velikih brojeva. (#14241)
* Java aplikacije sa kontrolama koje koriste status označenosti će izgovarati kada stavka nije označena umjesto obrnutog. (#14336)

### Ispravke grešaka

* Ispravke koje se primjenjuju u Windowsima 11:
  * NVDA će izgovarati rezultate pretrage prilikom otvaranja izbornika start. (#13841)
  * Na arhitekturi ARM, x64 aplikacije više nisu pogrešno identificirane kao ARM64 aplikacije. (#14403)
  * Stavkama izbornika povijesti međuspremnika poput "prikvači stavku" može se ponovno pristupiti. (#14508)
  * U Windowsima 11 22H2 i novijima, moguće je opet koristiti miš i interakciju dodirom kako bi se moglo koristiti područje obavijesti i dijaloški okvir "otvori sa". (#14538, #14539)
* Izgovaraju se prijedlozi prilikom upisivanja znaka @osvrta u Microsoft Excel komentarima. (#13764)
* U Google Chrome adresnoj traci, kontrole prijedloga (prebaci se na karticu, ukloni prijedlog itd) sada se izgovaraju kada su označene. (#13522)
* Prilikom dohvaćanja informacija o oblikovanju, boje su sada eksplicitno čitane u Wordpadu ili pregledniku zapisnika, umjesto  "podrazumjevana boja". (#13959)
* U  Firefoxu, aktiviranje opcije "Show options" na stranici za github probleme sada pouzdano radi. (#14269)
* Kontroke za odabir datuma u Outlooku 2016 / 365 dijaloškom okviru napredne pretrage sada se izgovaraju zajedno sa svojim vrijednostima. (#12726)
* ARIA switch kontrole sada se točnije izgovaraju kao preklopnici u Firefoxu, Chromeu i Edgeu, umjesto potvrdnih okvira. (#11310)
* NVDA će automatski izgovoriti status razvrstavanja na HTML zaglavlju stupca tablice kada se promjeni, prilikom pritiska unutrašnjeg gumba. (#10890)
* Naziv Orijentira i regije sada će se automatski čitati prilikom skananja u kontrolu ili fokusiranjem kontrole u modusu pregleda. (#13307)
* Kada je uključena opcija reproduciraj zvučni signal ili izgovori  'veliko' za velika slova, sa uključenim opisima znakova poslije kursora, NVDA više ne reproducira zvučni signal, niti ne izgovara  'veliko' dvaput. (#14239)
* Kontrole u tablicama u Java aplikacijama biti će pročitane točnije. (#14347)
* Neke postavke više neće biti neočekivano drugaćije kada se koristi više konfiguracijskih profila. (#14170)
  * Slijedeće postavke su ispravljene:
    * Uvlačenje redka u postavkama oblikovanja dokumenta.
    * Rubovi ćelija u postavkama oblikovanja dokumenta
    * Prikaz poruka u postavkama brajice
    * Povezivanje brajice u postavkama brajice
  * U nekim rijedkim slučajevima, ove postavke korištene u profilima mogu biti neočekivano izmijenjene kada se instalira iva inačica NVDA.
  * Molimo provjerite ove postavke u vašem profilu poslije nadogradnje na ovu inačicu.
* Emoji će se moći čitati na više jezika. (#14433)
* Prisutnost anotacija više ne nedostaje kada se prikazuju na brajičnom redku za neke elemente. (#13815)
* Ispravljena je pogreška u kojoj se izmjene ne spremaju ispravno prilikom izmjene "podrazumjevane" opcije i i vrijednosti "podrazumjevane" opcije. (#14133)
* Prilikom konfiguriranja NVDA uvijek će biti definirana barem jedna tipka kao NVDA modifikacijaka tipka. (#14527)
* Prilikom pristupanja NVDA izborniku preko popisa obavijesti, NVDA neće predložiti nadogradnju koja se očekuje kada isto nije dostupno. (#14523)
* Preostalo, proteklo i ukupno vrijeme sada se točno izgovara za audio datoteke čije trajanje prekoračuje jedan dan u foobar2000 programu. (#14127)
* U preglednicima poput Chromea i Firefoxa, upozorenja kao što su to preuzimanja biti će prikazana i na brajičnom redku. (#14562)
* Ispravljena je greška prilikom kretanja između prvog i zadnjeg stupca u tablici u Firefoxu (#14554)
* Kada je NVDA pokrenut sa parametrom naredbenog redka `--lang=Windows`, sada je ponovo moguće otvoriti prozor općenitih postavki.. (#14407)
* NVDA sada ponovno nastavlja čitanje u programu Kindle for PC poslije okretanja stranice. (#14390)

## 2022.4

U ovoj je inačici dodano nekoliko novih tipkovničkih prečaca, uključujući i prečace za čitanje cijele tablice.
Dodan je odjeljak "Vodič za brzo upoznavanje sa NVDA" u korisnički priručnik.
Ispravljene su također neke pogreške.

Espeak i LibLouis su nadograđeni.
Dodane su nove brajične tablice za jezike: kineski, švedski, Luganda i Kinyarwanda.

### Nove značajke

* Dodan je odlomak "Vodič za brzo upoznavanje" u vodič za korisnike. (#13934)
* Dodan je novi prečac za provjeru tipkovničkog prečaca trenutno fokusirane stavke. (#13960)
  * Za stolna računala: `shift+numerički2`.
  * za prijenosna računala: `NVDA+ctrl+shift+.`.
* Dodani su novi prečaci preglednog kursora za kretanje po stranici gdje to aplikacija podržava. (#14021)
  * Idi na prethodnu stranicu:
    * za stolna računala: `NVDA+pageUp`.
    * Za prijenosna računala: `NVDA+shift+pageUp`.
  * Idi na slijedeću stranicu:
    * Za stolna računala: `NVDA+pageDown`.
    * Za prijenosna računala: `NVDA+shift+pageDown`.
* Dodani su slijedeći prečaci za kretanje po tablicama. (#14070)
  * Čitaj sve u stupcu: `NVDA+control+alt+downArrow`
  * Čitaj sve u redku: `NVDA+control+alt+rightArrow`
  * Čitaj cijeli stupac: `NVDA+control+alt+upArrow`
  * Čitaj cijeli redak: `NVDA+control+alt+leftArrow`
* Microsoft Excel koji se koristi sa UI automation: NVDA sada obavještava o izlazku iz tablice u radnoj knjizi. (#14165)
* Čitanje zaglavlja tablica sada može biti konfigurirano odvojeno redci od stupaca. (#14075)

### Izmjene

* eSpeak NG je nadograđen  na inačicu 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Ispravljeno je čitanje latinice pri korištenju mandarinskog kineskog. (#12952, #13572, #14197)
* Nadograđen je LibLouis brajični prevoditelj na inačicu [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Dodane brajične tablice:
    * Kineska opća brajica (pojednostavljeni kineski znakovi)
    * Kinyarwanda puno pismo
    * Luganda puno pismo
    * švedsko osnovno pismo
    * švedsko puno pismo
    * švedski kratkopis
    * Kineski (Kina, mandarinski) Trenutačni brajični sustav (bez tonova) (#14138)
* NVDA sada uključuje arhitekturu operacijskog sustava kao dio sakupljane korisničke statistike. (#14019)

### Ispravke grešaka

* Prilikom nadogradnje NVDA uz pomoć Windows upravitelja paketa CLI (to jest winget), stabilna inačica se više ne tretira kao novija od bilo koje alpha inačice. (#12469)
* NVDA će sada ispravno čitati grupiranja u java aplikacijama. (#13962)
* Kursor sustava sada točno slijedi tijek "prečaca čitaj sve" u programima poput Bookworm-a, WordPada ili NVDA preglednika zapisnika. (#13420, #9179)
* U programima koji koriste UI automation, polovično odabrani potvrdni okviri sada će biti ispravno pročitani. (#13975)
* Unapređene su performanse i stabilnost u Microsoft Visual Studiu, Windows Terminalu, i drugim programima baziranim na UIA. (#11077, #11209)
  * Ove ispravke se primjenjuju na Windows 11 Sun Valley 2 (inačica 22H2) i novije.
  * Selektivna registracija za događaje UI automation i izmjene svojstava sada je uključena podrazumjevano.
* Čitanje teksta, brajični izlaz i neizgovaranje lozinki sada rade kako je to očekivano u ugrađenoj Windows terminal kontroli u Visual Studiu 2022. (#14194)
* NVDA je sada DPI svjestan pri korištenju više monitora.
Dodano je nekoliko ispravaka za korištenje DPI postavke više od 100% ili pri korištenju više monitora.
Još mogu postojati problemi sa inačicama operacijskog sustava Windows starijih od Windows 10 1809.
Kako bi ove ispravke radile, aplikacije s kojima NVDA ulazi u interakciju  također moraju biti DPI svjesne.
Imajte na umu da postoje problemi sa Chrome i Edge preglednicima. (#13254)
  * Okviri vizualnog označavanja sada će se postavljati ispravno u većini aplikacija. (#13370, #3875, #12070)
  * Interakcija putem dodirnika sada će biti točnija za većinu aplikacija. (#7083)
  * Praćenje miša će sada raditi ispravno za neke aplikacije. (#6722)
* Stanje orijentacije zaslona (okomito/vodoravno) sada se ispravno ignoriraju kada ne postoji izmjena (npr. promjene monitora). (#14035)
* NVDA će obavještavati o spuštanju stavaka na zaslonu kao što su to mjesta premještanja Windows 10 ploćica u izborniku start i virtualnim radnim površinama u Windows 11. (#12271, #14081)
* U naprednim postavkama, opcija opcija "reproduciraj zvuk za zapisane greške" sada se ispravno vraća na svoje podrazumjevane vrijednsti prilikom pritiska gumba "vrati na zadano". (#14149)
* NVDA sada može označavati tekst koristeći `NVDA+f10` tipkovnički prečac u java aplikacijama. (#14163)
* NVDA se više neće zaglavljivati u izborniku pri kretanju strelicama u тематским раѕговорима. (#14355)

## 2022.3.3

Ovo je mala inačica u kojoj su ispravljeni problemi iz inačica 2022.3.2, 2022.3.1 i 2022.3.
Ova verzija također ispravlja sigurnosnu ranjivost.

### Ispravke sigurnosti

* Onemogućuje pristup za neautentificirane korisnike (npr. NVDA Python konzoli).
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Ispravke grešaka

* Ispravljena je pogreška, u kojoj je bilo moguće pristupiti korisničkoj radnoj površini kada  se fokus nalazi na zaslonu zaključavanja. (#14416)
* Ispravljena je pogreška u kojoj prilikom smrzavanja NVDA isti se neće ispravno ponašatikao da je uređaj još uvijek zaključan. (#14416)
* Ispravljeni problemi s pristupačnošću s procesima "zaboravio sam pin" i Windows update/iskustvom instalacije. (#14368)
* Ispravljena je pogreška prilikom instalacije NVDA u nekim okruženjima, npr: Windows Server. (#14379)

## 2022.3.2

Ova inačica ispravlja regresije u inačici 2022.3.1 te ispravlja sigurnosnu ranjivost.

### Ispravke sigurnosti

* Onemogućen je mogući pristup na razini sustava za neautorizirane korisnike.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Ispravke grešaka

* Ispravljena regresija iz inačice 2022.3.1 u kojoj su neke funkcionalnosti bile isključene na sigurnim zaslonima. (#14286)
* Ispravljena regresija iz inačice 2022.3.1 u kojoj su neke funkcije poslije prijave, bile nedostupne ako se NVDA pokrenuo sa zaslona zaključavanja. (#14301)

## 2022.3.1

Ovo je podverzija koja ispravlja nekoliko sigurnosnih propusta.
Molimo odgovorno izvještavajte o sigurnosnim problemima na adresu <info@nvaccess.org>.

### Sigurnosne ispravke

* Ispravljena ranjivost putem koje je bilo moguće podizanja prava sa korisnika na sustav.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Ispravljen je sigurnosni propust koji je omogućavao pristpu python konzoli na zaključanom zaslonu preko rizične situacije NVDA pokretanja.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Ispravljena pogreška u kojej je tekst pregledniak govora bio zadržavan prilikom zaključavanja operacijskog sustava Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Ispravke grešaka

* Neautorizirani korisnik biti će spriječen u namjeri spremanja postavki preglednika govora i brajice na zaslonu zaključavanja. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Velikom dijelu ove inačice je doprinijela zajednica NVDA doprinositelja.
Ovo uključuje opise znakove poslije slovkanja i unapređenu podršku Windowsovog naredbenog redka.

Ova inačica uključuje nekoliko ispravaka grešaka.
Primjetno, posljednje inačice Adobe Acrobata/Readera neće se rušiti prilikom čitanja pdf dokumenta.

eSpeak je nadograđen, što znaći da su dodana tri nova jezika: bjeloruski, Luksenburški i Totontepec Mixe.

### Nove značajke

* U hostu Windows naredbenog redka kojeg koristi naredbeni redak, PowerShell i windows podsustav za sustava Linux u Windowsima 11 inačica 22H2 (Sun Valley 2) i novijim:
  * značajno su unapređene performanse i stabilnost. (#10964)
  * Prilikom pritiska prečaca `ctrl+f` za traženje teksta, pozicija preglednog kursora će se obnoviti kako bi pregledni kursor pratio pronađeni pojam. (#11172)
  * Izgovor upisanog teksta koji se ne pojavljuje na zaslonu poput lozinki je podrazumjevano isključen.
Može se uključiti u panelu NVDA Naprednih postavki. (#11554)
  * Tekst koji se pomaknuo izvan zaslona može se pregledavati bez potrebe za pomicanjem prozora naredbenog redka. (#12669)
  * Detaljnije informacije o oblikovanju teksta su dostupne. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Dodana je nova opcija za govor koja omogućuje čitanje opisa znaka poslije zadrške. (#13509)
* Dodana je nova brajična opcija koja regulira dali će pomicanje teksta na brajičnom redku naprijed ili nazad prekidati govor. (#2124)

### Izmjene

* eSpeak NG je nadograđen na inačicu 1.52-dev commit `9de65fcb`. (#13295)
  * Dodani jezici:
    * Bjeloruski
    * Luksenburški
    * Totontepec Mixe
* Prilikom korištenja UI Automation za pristup Microsoft Excel proračunskim tablicama, NVDA sada može izgovarati spojene ćelije. (#12843)
* Umjesto izgovora "sadrži detalje" uključen je tip detalja, gdje je to moguće, na primjer "sadrži komentar". (#13649)
* Veličina instalacije NVDA sada se prikazuje u odjeljku programi i funkcije operativnog sustava Windows. (#13909)

### Ispravke grešaka

* Adobe Acrobat / Reader 64 bitne inačice više se neće rušiti prilikom čitanja PDF dokumenata. (#12920)
  * Imajte na umu da je potrebna posljednja inačica Adobe/acrobat readera kako bi se izbjeglo rušenje.
* Mjere veličine fonta su od sada prevedene u  NVDA. (#13573)
* Ignorirani su događaji Java Access Bridge gdje se ne može pronaći uloga prozora za java aplikacije.
Ovo će unaprediti performanse za neke java aplikacije uključujući IntelliJ IDEA. (#13039)
* Izgovor označenih ćelija za LibreOffice Calc je točniji i ne rezultira rušenjem aplikacije Calc prilikom označavanja više ćelija. (#13232)
* Kada se pokreće od drugug korisnika, Microsoft Edge više nije nepristupačan. (#13032)
* Kada je dopojačanje brzine uključeno,, eSpeakova brzina ne pada u međuvrijednost između brzina 99% i 100%. (#13876)
* Ispravljena je greška koja je dozvoljavala dva otvorena dijaloška okvira ulaznih gesti.. (#13854)

## 2022.2.4

Ovo je inačica koja ispravlja sigurnosnu ranjivost.

### Ispravke grešaka

* Ispravljena ranjivost putem koje je bilo moguće otvoriti Python konzolu preko pregledniak zapisnika na sigurnom zaslonu.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Ovo je verzija koja je izdana u svrhu ispravljanja nekompatibilnosti API sučelja do koje je došlo u inačici 2022.2.1.

### Ispravke grešaka

* Ispravljena greška zbog koje NVDA nije izgovarao "sigurni zaslon" prilikom ulaza u sigurnu radnu površinu.
Ovo je prouzrokovalo nemogućnost NVDA remote da prepoznaje sigurne radne površine. (#14094)

## 2022.2.2

Ovo je verzija sa zakrpom koja ispravlja grešku iz verzije  2022.2.1 sa ulaznim gestama.

### Ispravke grešaka

* Ispravljena greška sa ulaznim gestama koje nisu ispravno radile. (#14065)

## 2022.2.1

Ovo je mala verzija koja ispravlja sigurnosni propust.
Molimo odgovorno prijavljujte sigurnosne propuste na adresu <info@nvaccess.org>.

### Ispravke sigurnosnih propusta

* Ispravljena ranjivost  u kojoj je bilo moguće pokrenuti python konzolu sa zaključanog zaslona. (GHSA-rmq3-vvhq-gp32)
* Ispravljena ranjivost pomoću koje je bilo moguće izaći iz zaključanog zaslona koristeći objektnu navigaciju. (GHSA-rmq3-vvhq-gp32)

## 2022.2

Ova inačica uključuje puno ispravaka grešaka.
Prije svega, značajno je unapređena suradnja sa aplikacijama baziranim na java sučelju, brajičnim redcima i značajkama operacijskog sustava Windows.

Uvedeni su novi prečaci za kretanje po tablicama.
Unicode CLDR je nadograđen.
LibLouis je nadograđen, sa novom dodanom njemačkom brajičnom tablicom.

### Nove značajke

* Podrška za interakciju s Microsoft Loop komponentama u proizvodima Microsoft Officea. (#13617)
* Dodane su nove naredbe za navigaciju u tablicama. (#957)
 * `control+alt+home/end` za skakanje na prvi/zadnji stupac.
 * `control+alt+pageUp/pageDown` za skakanje na prvi/zadnji redak.
* Dodana je nedodijeljena skripta za mijenjanje jezika i dijalekta. (#10253)

### Izmjene

* NSIS je nadograđen na verziju 3.08. (#9134)
* CLDR je nadograđen na verziju 41.0. (#13582)
* Nadograđen LibLouis brajični prevoditelj na verziju [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nova brajična tablica: Njemački kratkopis (eksperimentalan)
* • Dodana je nova uloga za kontrole "indikatora zauzetosti". (#10644)
* NVDA sada najavljuje kad se NVDA radnja ne može izvesti. (#13500)
  * Ovo uključuje sljedeće:
    * kad se koristi NVDA Windows Store verzija.
    * kad se računalo nalazi na sigurnom zaslonu.
    * kad se čeka na odgovor u modalnom dijaloškom okviru. - - -

### Ispravke grešaka

* Ispravke za aplikacije napisane u java programskom jeziku:
  * NVDAće sada izgovarati status samo za čitanje. (#13692)
  * NVDA će sada ispravno izgovarati stanje uključenosti/isključenosti. (#10993)
  * NVDA će sada izgovarati prečace funkcijskih tipki. (#13643)
  * NVDA sada može reproducirati zvučne signale ili izgovarati trake napredka. (#13594)
  * NVDA više neće neispravno uklanjati tekst sa widgeta kada se isti prikazuje korisniku. (#13102)
  * NVDA će sada izgovarati stanje preklopnih gumbi. (#9728)
  * NVDA će sada prepoznavati prozore u java aplikacijama sa više prozora. (#9184)
  * NVDA će sada izgovarati informacije o poziciji za kontrole kartica. (#13744)
* Ispravke brajice:
  * Ispravljen brajični izlaz u mozillinim kontrolama obogaćenog teksta, kao što je to skiciranje poruka u Mozilla thunderbirdu. (#12542)
  * Kada je brajica povezana automatski a miš se kreće s uključenim praćenjem miša,
   brajični će redak biti obnovljen. (#11519)
  * Sada je moguće pomicati brajični redak po sadržaju poslije korištenja prečaca pregleda teksta. (#8682)
* • NVDA instalacijski program se sada može pokrenuti iz direktorija s posebnim znakovima. (#13270)
* U Firefoxu, NVDA sada uspijeva prijaviti stavke na web stranicama kad su atributi aria-rowindex, aria-colindex, aria-rowcount ili aria-colcount nevažeći. (#13405)
* Kursor više ne mijenja redak ili stupac kad se koristi tablična navigacija za kretanje kroz spojene ćelije. (#7278)
* Prilikom čitanja neinteraktivnih PDF-ova u Adobe Readeru, sada se izvještavaju vrsta i stanje polja obrasca (kao što su potvrdni okviri i izborni gumbi). (#13285)
* "Resetiraj konfiguraciju na tvorničke vrijednosti" sada je dostupno u NVDA izborniku tijekom sigurnog načina rada. (#13547)
* Sve zaključane tipke miša otključat će se kad se NVDA čitač zatvori. Prije je tipka miša ostala zaključana. (#13410)
* Visual Studio sada izvještava o brojevima redaka. (#13604)
  * Da bi izvještavanje o brojevima redaka funkcioniralo, prikazivanje brojeva redaka mora biti aktivirano u Visual Studiju i NVDA-u.
* Visual Studio sada ispravno izvještava o uvlačenju retka. (#13574)
* NVDA će još jednom najaviti detalje rezultata pretraživanja izbornika Start u nedavnim izdanjima sustava Windows 10 i 11. (#13544)
* U kalkulatoru u  Windowsima 10 u inačici 10.1908 i novijim,
NVDA će izgovarati rezultate za više pritisnutih naredbi, poput naredaba iz znanstvenog načina. (#13383)
* U Windowsima 11, sada je opet moguće kretanje i interakcija s elementima korisničkog sučelja ,
poput trake zadataka i pregleda zadataka uz pomoć miša i dodirnika. (#13506)
* NVDA će sada čitati traku stanja u Windows 11 bloku za pisanje. (#13688)
* Označavanje objekta navigatora pokazuje se trenutno poslije aktivacije značajke. (#13641)
* Ispravljeno čitanje jednostupčastih popisa. (#13659, #13735)
* Ispravljeno automatsko prebacivanje jezika prilikom korištenja Espeaka za engleski i francuski vraćajući se na britanski engleski i francuski (Francuska). (#13727)
* Ispravljeno OneCore automatsko prepoznavanje jezika prilikom pokušaja prebacivanja na jezik koji je bio prije instaliran. (#13732)

## 2022.1

Ova verzija uključuje veća poboljšanja za UIA podršku u paketu MS Office.
Za Microsoft Office 16.0.15000 i novije verzije na Windowsu 11, NVDA će podrazumevano koristiti UI Automation za pristup dokumentima programa Microsoft Word.
Ovo pruža značajno poboljšanje brzine u odnosu na stariji način pristupa.

Postoje poboljšanja za upravljačke programe za brajične redke kao što su Seika brajična bilježnica, Papenmeier i  HID brajični standard. 
Takođe su uključene razne ispravke grešaka za Windows 11, u aplikacijama kao što su Kalkulator, naredbeni redak, Terminal, Mail i Emoji panel.

Ažurirani su eSpeak-NG  i LibLouis, tako da su dodane nove Japanske, Nemačke i Katalonske brajične tablice.

Napomena:

 * Ova verzija čini postojeće dodatke nekompatibilnim.

### nove značajke

* Podrška za prijavljivanje napomena u programu MS Excel uz  UI Automation omogućen na Windowsu 11. (#12861)
* U novijim verzijama programa Microsoft Word uz  UI Automation na  Windowsu 11, postojanje markera, nacrta komentara kao i rješenih komentara se sada prijavljuje izgovorom kao i na brajevom redu. (#12861)
* Novi parametar naredbenog redka `--lang` dozvoljava mijenjanje podešenog NVDA jezika. (#10044)
* NVDA će sada upozoriti o parametrima komandne linije koji su nepoznati i a dodaci ih ne koriste. (#12795)
* Kada se pristupa programu Microsoft Word uz UI Automation, NVDA će sada koristiti mathPlayer za kretanje  po matematičkim zadacima i čitanje. (#12946)
  * Kako bi ovo  radilo, morate koristiti Microsoft Word 365/2016 verziju 14326 ili novije. 
    * MathType zadaci se takođe moraju ručno pretvoriti u Office Math izborom svakog od njih, otvaranjem kontekstnog menija, izborom stavke opcije jednadžba, pretvori u  Office Math.
-
* Prijavljivanje kada objekat  "ima detalje " kao i odgovarajuća komanda za prijavljivanje odnosa detalja sada se mogu koristiti u režimu fokusiranja. (#13106)
* Seika brajična bilježnica se sada može automatski prepoznati putem USB i Bluetooth veze. (#13191, #13142)
  * Ovo utiče na sliedeće uređaje: MiniSeika (16, 24 znakova), V6, i V6Pro (40 znakova)
  * Ručno biranje bluetooth COM porta je sada takođe podržano.
* Dodana komanda za uključivanje i isključivanje preglednika brajičnog redka; nema podrazumijevane pridružene prečice. (#13258)
* Dodate komande za uključivanje ili isključivanje više modifikatora u isto vrieme  na brajičnom redku (#13152)
* Dijalog za govorne rečnike sada sadrži gumb "Ukloni sve" koji vam pomaže da očistite cijeli riječnik. (#11802)
* Dodana podrška za Windows 11 kalkulator. (#13212)
* U programu Microsoft Word uz UI Automation omogućen na Windowsu 11, brojevi redaka i sekcija se sada mogu prijaviti. (#13283, #13515)
* Za  Microsoft Office 16.0.15000 i novije na Windowsu 11, NVDA će podrazumijevano koristiti UI Automation za pristup Microsoft Word dokumentima, što pruža značajna poboljšanja u brzini u odnosu na stariji način pristupa. (#13437)
 * Ovo uključuje dokumente u samom programu Microsoft Word, kao i čitanje i pisanje poruka u programu Microsoft Outlook. 

### izmijene

* Espeak-ng je ažuriran na 1.51-dev commit `7e5457f91e10`. (#12950)
* Ažuriran liblouis brajični prevoditelj na [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Dodana nova brajična tablica: Japanski (Kantenji) literarna brajica.
  * Dodata nova Njemačka šestotočkasta kompjuterska brajična tablica.
  * Dodana brajična tablica Katalonsko puno pismo. (#13408)
* NVDA će izgovarati označavanje i spajanje ćelija u programu LibreOffice Calc 7.3 i novijim. (#9310, #6897)
* Ažuriran Unicode Common Locale Data Repository (CLDR) na 40.0. (#12999)
* ``NVDA+numerička tipka za brisanje `` podrazumjevano prijavljuje lokaciju kursora ili fokusiranog objekta. (#13060)
* `NVDA+šift+numerička tipka za brisanje` prijavljuje lokaciju preglednog kursora. (#13060)
* Dodani podrazumjevani prečaci za uključivanje i isključivanje modifikatorskih tastera na Freedom Scientific brajevim redovima (#13152)
* "Osnovna linija " se više neće izgovarati kada se koristi prečac za prijavljivanje oblikovanja  (`NVDA+f`). (#11815)
* Prijavljivanje dugog opisa više nema postavljenu podrazumjevan prečac. (#13380)
* Prijavljivanje kratkog opisa detalja sada ima podrazumjevan prečac (`NVDA+d`). (#13380)
* NVDA mora ponovo biti pokrenut nakon što se instalira MathPlayer. (#13486)

### Ispravke grešaka

* Okno upravljača privremene memorije više neće neispravno biti fokusirano kada se otvaraju određeni Office programi. (#12736)
* Na sustavima na kojima je korisnik odredio da zamijeni primarni gumb na mišu tako da desni klik aktivira stavke, NVDA više neće otvarati kontekstni meni umesto da aktivira stavku, u aplikacijama kao što su Web pretraživači. (#12642)
* Kada se pregledni kursor pomjera od dna tekstualnih kontrola, kao što su u programu Microsoft Word uz UI Automation, "dno" se ispravno izgovara u više situacija. (#12808)
* NVDA može da pruži ime aplikacije i verziju za binarne datoteke koje se nalaze u system32 kada je pokrenut na 64-bitnoj verziji Windowsa. (#12943)
* Poboljšana dosliednost u čitanju u terminal programima. (#12974)
  * Napomena da će se u određenim situacijama, kada ubacujete ili brišete znakove u sredini redka, znakovi nakon kursora  možda ponovo pročitati.
* MS word uz UIA: Brza navigacija kroz naslove se neće više zaglavljivati na posljednjem naslovu, niti će taj naslov biti prikazan dva puta u listi elemenata. (#9540)
* Na Windowsu 8 i novijim, statusna traka istraživača datoteka se sada može pročitati korištenjem standardnih prečica NVDA+end (desktop) / NVDA+šift+end (laptop). (#12845)
* Dolazne poruke u čavrljanjima aplikacije Skype za biznis se ponovo prijavljuju. (#9295)
* NVDA ponovo može stišavati pozadinske zvukove kada  se koristi SAPI5 sintetizator na Windowsu 11. (#12913)
* U Kalkulatoru Windowsa 10, NVDA će izgovarati oznake za istoriju i stavke popisa memorije. (#11858)
* Prečaci kao što su pomeranje brajevog reda i prebacivanje ponovo rade na HID brajevim uređajima. (#13228)
* Windows 11 Mail: Nakon prebacivanja fokusa između aplikacija, dok se čita duža EMail poruka, NVDA se više neće zaglavljivati na jednom redu poruke. (#13050)
* HID brajevi uređaji: Vezane komande  (na primer  `razmak+točkica4`) se mogu uspešno izvršiti sa brajevog reda. (#13326)
* Ispravljena greška koja je dozvoljavala da se otvori više dijaloga sa postavkama u isto vrieme. (#12818)
* Ispravljen problem koji je izazvao da određeni Focus Blue brajični redci prestanu raditi nakon što probudite računalo iz stanja spavanja. (#9830)
* "Osnovna linija " se više ne izgovara bespotrebno kada je opcija "prijavi indekse i eksponente" omogućena. (#11078)
* U Windowsu 11, NVDA više neće sprečavati navigaciju kroz Emoji panel kada se bira emoji. (#13104)
* Spriječena greška koja izaziva dvostruko prijavljivanje kada se koristi Windows konzola i terminal. (#13261)
* Ispravljeno nekoliko slučajeva u kojima stavke popisa nisu mogle biti prijavljene u 64 bitnim aplikacijama, kao što je REAPER. (#8175)
* U upravljaču preuzimanja programa Microsoft Edge, NVDA će se automatski prebaciti u režim fokusiranja kada stavka liste sa najnovijim preuzimanjem postane fokusirana. (#13221)
* NVDA više neće izazvati rušenje 64-bitnih verzija programa Notepad++ 8.3 i novijih. (#13311)
* Adobe Reader se više ne ruši pri pokretanju ako je njegov zaštićen režim omogućen. (#11568)
* Ispravljena greška koja je izazivala rušenje programa NVDA kada se izabere  Papenmeier upravljački program. (#13348)
* Microsoft word uz UIA: Broj stranice i druge informacije o formatiranju se više ne izgovaraju bespotrebno kada se prebacite iz prazne ćelije tabele u ćeliju sa sadržajem, ili sa kraja dokumenta na postojeći sadržaj. (#13458, #13459)
* NVDA više neće imati problema sa prijavljivanjem naslova stranice i početka automatskog čitanja, kada se stranica učita u programu Google chrome 100. (#13571)
* NVDA se više ne ruši kada se podešavanja vrate na tvorničke vrijednosti uz uključen izgovor komandnih tastera. (#13634)

## 2021.3.5

Ovo je manje ažuriranje kako bi se ispravio sigurnosni problem.
Molimo odgovorno prijavite sigurnosne probleme na adresu <info@nvaccess.org>.

### Ispravci sigurnosti

* Ispravljena sigurnosna preporuka `GHSA-xc5m-v23f-pgr7`.
  * Dijalog izgovora znakova interpunkcije i simbola je sada onemogućen u sigurnom načinu rada.

## 2021.3.4

Ovo je manje ažuriranje kako bi se ispravilo nekoliko prijavljenih sigurnosnih problema.
Molimo odgovorno prijavite sigurnosne probleme na adresu  <info@nvaccess.org>.

### Sigurnosni ispravci

* Ispravljena sigurnosna preporuka `GHSA-354r-wr4v-cx28`. (#13488)
  * Uklonjena mogućnost da se NVDA pokrene uz omogućene zapisnike za otklanjanje grešaka kada je NVDA pokrenut u bezbednom načinu rada.
  * Uklonjena mogućnost da se NVDA ažurira kada je pokrenut u sigurnom načinu rada.
* Ispravljena sigurnosna preporuka `GHSA-wg65-7r23-h6p9`. (#13489)
  * Uklonjena mogućnost otvaranja dijaloga ulaznih gesti u bezbednom načinu rada.
  * Uklonjena mogućnost otvaranja podrazumijevanog, privremenog i govornog rječnika u sigurnosnom načinu rada.
* Ispravljena sigurnosna preporuka `GHSA-mvc8-5rv9-w3hx`. (#13487)
  -  wx GUI inspection alat je sada onemogućena u sigurnom načinu rada.
  -

## 2021.3.3

Ova verzija je identična verziji 2021.3.2.
Došlo je do greške u verziji NVDA 2021.3.2 pa se ona identificirala kao 2021.3.1.
Ova verzija se ispravno identificira kao 2021.3.3.

## 2021.3.2

Ovo je manje ažuriranje kako bi se ispravilo nekoliko prijavljenih sigurnosnih problema.
Molimo odgovorno prijavite sigurnosne probleme na adresu  <info@nvaccess.org>.

### Ispravke grešaka

* Sigurnosna ispravka: Sprečavanje objektne navigacije van zaključanog ekrana na Windowsu 10 i Windowsu 11. (#13328)
* Sigurnosna ispravka: Ekran upravljača dodacima je sada onemogućen na sigurnim zaslonima. (#13059)
* Sigurnosna ispravka: NVDA kontekstna pomoć više nije dostupna na sigurnim zaslonima. (#13353)

## 2021.3.1

Ovo je manje ažuriranje kako bi se ispravilo nekoliko grešaka u verziji 2021.3.

### Izmjene

* Novi HID brajični protokol više nije izabran u situacijama kada postoji drugi upravljački program za brajični redak koji se može koristiti. (#13153)
* Novi HID brajični protokol se može onemogućiti korištenjem opcije u panelu naprednih postavki. (#13180)

### Ispravke grešaka

* Orjentiri će ponovo imati skraćenice na brajičnom redku. #13158
* Ispravljjena nestabilnost u automatskom prepoznavanju brajičnih redaka Humanware Brailliant i  APH Mantis Q40 kada se koriste putem  Bluetooth veze. (#13153)

## 2021.3

Ova inačica uvodi podršku za novu HID specifikaciju za brajične retke.
Ova specifikacija ima za cilj standardizaciju podrške za brajične retke bez potrebe za pojedinačnim upravljačkim programima.
Nadograđeni su eSpeak-NG i LibLouis, uključujući nove tablice za ruski i Tshivenda jezike.
Zvuci pogrešaka mogu biti omogućeni u stabilnim inačicama NVDA koristeći novu opciju u naprednim postavkama.
Prečac čitaj sve u Wordu sada prebacuje kako bi trenutna pozicija bila vidljiva.
Učinjeno je mnoštvo poboljšanja pri korištenju Office paketa sa UIA.
Jedna ispravka za UIA je ta da Outlook ignorira više tablica izgleda u porukama.

Važna upozorenja:

Zbog nadogradnje našeg sigurnosnog certifikata, mali broj korisnika dobijaju pogrešku kada NVDA 2021.2 provjerava nadogradnje.
NVDA sada pita operacijski sustav Windows treba li nadograditi sigurnosni certifikat, što znači da će takve greške u budućnosti biti izbjegnute.
Korisnici koji su se susreli sa tom greškom će trebati ručno preuzeti ovu nadogradnju.

### Nove značajke

* Dodan prečac za uključivanje ili isključivanje izgovoraa stila granice rubova. (#10408)
* Podrška nove HID specifikacije za brajične redke koja ima za cilj standardizaciju podrške brajičnih redaka. (#12523)
 * NVDA će automatski prepoznavati uređaje koji podržavaju ovu specifikaciju.
 * Za tehničke detalje o NVDA implementaciji ove specifikacije, pogledajte https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Dodana podrška za  VisioBraille Vario 4 brajični redak. (#12607)
* Obavijesti o pogreškama mogu biti uključene (napredne postavkew) kada se koristi bilo koja inačica NVDA. (#12672)
* Pri korištenju Windowsa 10 i novijih inačica, NVDA će izgovarati broj sugestija prilikom upisivanja upita pretrage u programima poput postavki i Microsoft Storea. (#7330, #12758, #12790)
* Kretanje po tablicama je sada podržana u mrežastim kontrolama koje su stvorene koristeći Out-GridView cmdlet u PowerShellu. (#12928)

### Izmjene

* Espeak-ng je nadograđen na inačicu 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* NVDA  će podrazumjevano koristiti eSpeak'ng ako ne postoji niti jedan OneCore glas koji podržava podrazumijevani jezik NVDA. (#10451)
* Ako OneCore glasovi  se ne učitavaju, koristit će se Espeak kao govorna jedinica. (#11544)
* Prilikom čitanja statusne trake koristeći `NVDA+end`, pregledni kursor se neće pomicati na statusnu traku.
Ako vam je ta značajka potrebna molimo dodijelite odgovarajući tipkovnički prečac u kategoriji objektna navigacija u dijaloškom okviru ulazne geste. (#8600)
* Prilikom otvaranja postavki koje su već otvorene, NVDA će postaviti fokus na dijaloški okvir koji je već otvoren što je bolje od prikazivanja pogreške. (#5383)
* Nadograđen liblouis brajični prevoditelj na inačicu [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
 * Nove brajične tablice: ruski kratkopis, Tshivenda puno pismo, Tshivenda kratkopis
* Umjesto "označeni sadržaj" ili "mrkd", "istaknuto" ili "istk." biti će prikazano na brajičnom retku. (#12892)
* NVDA više se neće pokušati isključiti kada se očekuje konkretna izvršena akcija u dijaloškom okviru (eg Confirm/Cancel). (#12984)

### Ispravke grešaka

* Praćenje modifikacijskih tipki poput tipaka Control, ili Insert je robusnije prilikom vraćanja glavnih komponenti u radnu spremnost. (#12609)
* Sada je ponovno moguće provjeravati za nadogradnje na nekim verzijama operacijskog sustava Windows npr. na čistim instalacijama operacijskog sustava Windows. (#12729)
* NVDA ispravno izgovara prazne ćelije tablice u Microsoft Wordu prilikom korištenja sučelja UI automation. (#11043)
* U ARIA ćelijama podatkovne tablice na web stranicama, tipka escape biti će preusmjerena na tablicu a način fokusa se neće bezuvjetno isključiti. (#12413)
* Prilikom čitanja zaglavlja ćelije tablice u Chromeu, ispravljeno je dvostruko čitanje naziva stupca. (#10840)
* NVDA više ne izgovara uzorak numeričke vrijednosti za UIA klizače koji imaju definiranu svoju tekstualnu vrijednost. (UIA ValuePattern je preferiraniji od RangeValuePattern). (#12724)
* NVDA više ne tretira vrijednost UIA klizača kao da su uvijek bazirani na postotcima.
* Izgovaranje pozicije ćelije u Microsoft Excelu kada se koristi sučelje UI Automation ponovno ispravno radi u Windowsima 11. (#12782)
* NVDA više ne postavlja netočne python lokalizacije. (#12753)
* Ako je onemogućeni dodatak deinstaliran a potom ponovno instaliran isti će ponovno biti omogućen. (#12792)
* Ispravljene su pogreške vezane uz nadogradnju i deinstalaciju dodataka gdje je mapa dodatka preimenovana ili su datoteke bile otvorene. (#12792, #12629)
* Prilikom korištenja sučelja UI Automation za pristup  Microsoft Excel kontrolama proračunskih tablica, NVDA više ne izgovara izlišna označavanja ćelija. (#12530)
* Više tekstova dijaloških okvira sada će se čitati u  LibreOffice Writeru, poput dijaloških okvira potvrde. (#11687)
* Kretanje  po dokumentima u Microsoft Wordu koristeći sučelje UI automation sada provjerava vidljivost trenutne pozicije, te da pozicija dokumenta u načinu fokusa je istovjetna sa onom u načinu pregleda. (#9611)
* Prilikom izvođenja prečaca za čitanje cijelog dokumenta u Microsoft Wordu koristeći sučelje UI automation, dokument se sada automatski prebacuje, i pozicija kursora sada se automatski osvježava. (#9611)
* Prilikom čitanja poruka elektroničke pošte u Outlooku kojima NVDA pristupa koristeći sučelje UI automation, neke vrste tablica sada se tretiraju kao tablice izgleda, što znaći da se one neće podrazumjevano izgovarati. (#11430)
* Ispravljena je rijetka pogreška prilikom mijenjanja zvučnih kartica. (#12620)
* Unos koristeći literarne brajične tablice, odnosno tablice punog pisma sada bi trebao biti pouzdaniji prilikom upisivanja u poljima za uređivanje. (#12667)
* Prilikom kretanja po kalendaru u području obavijesti, NVDA izgovara dan u tijednu u potpunosti. (#12757)
* Prilikom korištenja metoda unosa za kineski poput Tajvanski - Microsoft Quick u Microsoft Wordu, prebacivanje brajičnog retka u naprijed ili nazad više ne preskaće neispravno nazad na na izvornu poziciju. (#12855)
* Prilikom pristupanja dokumentima u Microsoft Wordu uz pomoć sučelja UIA, sada je moguće ponovno kretati se po rečenicama koristeći prečace alt+strelica dolje / alt+strelica gore. (#9254)
* Prilikom pristupa MS Wordu koristeći UIA, sad se izgovaraju uvlaćenja odlomaka. (#12899(
* Prilikom pristupa MS Wordu uz pomoć UIA, prečaci za praćenje izmjena i drugi lokalizirani prečaci sada se izgovaraju . (#12904)
* Ispravljena pogreška dvostrukog izgovora i prikaza na brajičnom redku kada se poklapao  'opis' sa 'sadržajem' ili 'nazivom'. (#12888)
* U MS Wordu sa uključenim UIA sučeljem, sada se točnije reproduciraju zvukovi koji označavaju pravopisnu ili gramatičku pogrešku prilikom pisanja. (#12161)
* U Windowsima 11, NVDA više neće izgovarati "prozor" prilikom pritiska Alt+Tab kada se prebacujete između programa. (#12648)
* Nova suvremena  prozor-stranica za komentare sada je podržana u MS Wordu kada se dokumentu ne pristupa koristeći UIA. Press alt+f12 to move between the side track pane and the document. (#12982)

## 2021.2

Ova inačica sadrži ranu podršku za  Windowse 11.
Iako bi sustav Windows 11 tek trebao biti objavljen, ova je inačica NVDA testirana na predpreglednim inačicama operacijskog sustava Windows 11.
Ovo uključuje važnu ispravku za zaslonsku zavjesu (molimo pogledajte važna upozorenja).
Alat za ispravljanje Com pogrešaka sada može ispraviti više pogrešaka kada je NVDA pokrenut.
Nadograđeni su govorna jedinica eSpeak i brajični prevoditelj LibLouis.
Ova inačica također dolazi sa jako puno poboljšanja, od kojih su najvažnija poboljšanja podrške za brajicu i Windows terminalne programe, kalkulator, emoji panel i povijest međuspremnika.

### Važna upozorenja

Zbog izmjena u Windows API-ju za uvećavanje, funkcija zaslonske zavjese trebala je biti nadograđena kako bi novije inačice operacijskog sustava Windows bile podržane.
Kako biste koristili zaslonsku zavjesu, koristite NVDA 2021.2 sa Windowsima 10 21H2 (10.0.19044) iliji novije inačice operacijskog sustava.
Ovo uključuje Windows 10 insidere i Windows 11.
Iz sigurnosnih razloga, prilikom korištenja novije inačice operacijskog sustava Windows, provjerite radi li zaslonska zavjesa.

### Nove značajke

* Eksperimentalna podrška Aria zabilješki:
  * Dodaje prečac za čitanje detalja objekta koji sadrži aria-details. (#12364)
  * Dodana opcija u naprednim postavkama za izvještavanje o detaljima u načinu pregleda. (#12439) 
* U Windowsima 10 verziji 1909 i novijim (uključujući Windows 11), NVDA će izgovarati broj prijedloga prilikom izvođenja pretrage u eksploreru za datoteke. (#10341, #12628)
* U Microsoft Wordu, NVDA sada čita rezultat prečaca za normalnu i viseću uvlaku pri izvršavanju. (#6269)

### Izmjene

* Espeak-ng je nadograđen na inačicu 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Ako je članak uključen u korisničkim postavkama oblikovanja dokumenata, NVDA izgovara "članak" poslje sadržaja. (#11103)
* Nadograđen liblouis brajični prevoditelj na inačicu [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Nove brajične tablice: Bugarski puno pismo, Burmansko puno pismo, Burmanski kratkopis, Kazaško puno pismo, Khmersko puno pismo, Sjevernokurdsko osnovno pismo, Sjeverni sotho puno pismo, Sjeverni sotho kratkopis, Južni sotho puno pismo, južni sotho kratkopis, Setswana puno pismo, Setswana kratkopis, tatarsko puno pismo, Vijetnamsko puno pismo, Vijetnamski kratkopis, Južni vijetnamski kratkopis, Xhosa puno pismo, Xhosa kratkopis, Jakutsko puno pismo, Zulu puno pismo, Zulu kratkopis
* Windows 10 OCR je preimenovan u Windows OCR. (#12690)

### Ispravke grešaka

* U Windows 10 kalkulatoru, NVDA će prikazivati izraze kalkulatora na brajičnom redku. (#12268)
* U programima terminala u Windowsima 10 inačica 1607 i novijim, prilikom umetanja ili brisanja teksta u sredini redka, znakovi desno od brisanog znaka nisu više čitani. (#3200)
  * Diff Match Patch sada je uključn podrazumijevano. (#12485)
* Unos brajičnih znakova ponovno radi sa sljedećim tablicama: Arapski kratkopis, Španjolski kratkopis, urdski kratkopis, Kineski (Kina, mandarinski) kratkopis. (#12541)
* Alat za ispravljanje pogrešaka com registracija sada ispravlja više pogrešaka, posebno na 64-bitnim Windowsima. (#12560)
* Ispravke upravljanja gumbima za Seika brajične bilježnice braille tvrtke Nippon Telesoft. (#12598)
* Unapređenja u čitanju  Windows panela emoji i povijesti međuspremnika. (#11485)
* Nadograđeni opisi znakova bengalske abecede. (#12502)
* NVDA izlazi sigurno kada se pokreće novi proces. (#12605)
* Ponovno označavanje Handy Tech upravljačkog progama za brajične redke iz dijaloškog okvira odabira brajičnog redka više ne prouzrokuje greške. (#12618)
* Inačice Windowsa 10.0.22000 ili novije sada se prepoznaju kao Windows 11, a ne kao Windows 10. (#12626)
* Ispravljena je podrška zaslonske zavjese te je ista testirana sa inačicama do 10.0.22000. (#12684)
* Ako nema rezultata ulaznih gesti, dijaloški okvir konfiguracije i dalje radi kako je to očekivano. (#12673)
* Ispravljena pogreška gdje je prva stavka izbornika nije izgovorena u nekim situacijama. (#12624)

## 2021.1

Ova inačica sadrži opcionalnu eksperimentalnu podršku za UIA u Excelu i preglednicima baziranima na Chromium platformi.
Dodane su ispravke za neke jezike, te je popravljen način interakciej sa poveznicama koristeći brajični redak.
Nadograđeni su Unicode CLDR, matematički simboli i LibLouis.
Kao i puno ispravaka grešaka i unapređenja, uključujući ispravke grešaka u  Officeu, Visual Studio, te u nekim jezicima.

Upozorenje:

* Ova inačica zahtjeva nadogradnju na novije inačice dodataka.
* Ova inačica također ukida podršku za tehnologiju Adobe flash.

### Nove značajke

* Rana podrška za UIA u preglednicima baziranim na Chromium platformi. (such as Edge). (#12025)
* Rana eksperimentalna podrška za Microsoft Excel koristeći UI Automation. Preporučuje se samo sa Microsoft Excel inačicom 16.0.13522.10000 ili novijom. (#12210)
* Lakše kretanje po rezultatima u NVDA Python konzoli. (#9784)
  * alt+strelice gore/dolje skače na prethodni odnosno sljedeći rezultat (add shift for selecting).
  * control+l briše okno rezultata.
* NVDA sada izgovara kategorije zadataka u Microsoft Outlooku, ako postoje. (#11598)

### Izmjene

* U modusu čitanja, kontrole se mogu aktivirati uz pomoć brajičnog kursora koji se nalazi na opisu kontrole (na primjer. "pvz" za poveznicu). To je korisno za aktivaciju na primjer potvrdnih okvira bez oznaka. (#7447)
* NVDA sada sprječava izvođenje prepoznavanja teksta uz pomoć Windows 10 OCR, ako je zaslonska zavjesa uključena. (#11911)
* Nadograđen repozitorij zajedničkih podataka o lokalizaciju  (CLDR) na inačicu 39.0. (#11943)
* Dodano više matematičkih simbola u rječnik simbola. (#11467)
* Vodič za korisnike, datoteka sa popisom izmjena, i popis tipkovničkih prečaca sada imaju osvježen izgled. (#12027)
* Sada NVDA izgovara"nije podržano" prilikom pokušaja izmjene izgleda u aplikacijama koje to ne podržavaju, kao što je to Microsoft Word. (#7297)
* 'Pokušaj ignoriranja događaja govora koji su istekli' u naprednom panelu postavki je sada podrazumjevano omogućena. (#10885)
  * Ta se opcija može onemogučiti tako da se vrijednost postavi na "Ne".
  * Web aplikacije (npr. Gmail) više ne izgovaraju informacije koje su istekle pri brzom premještanju fokusa.
* Nadograđen Liblouis brajični prevoditelj na inačicu [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Nove brajične tablice: bjeloruska literarna brajica, bjeloruska kompjutorska brajica, Urdsko puno pismo, urdski kratkopis.
* Podrška za Flash sadržaj je uklonjena iz NVDA zbog toga što Adobe ne preporučuje korištenje te tehnologije. (#11131)
* NVDA će se isključiti čak iako su prozori otvoreni, u procesu izlazka iz NVDA zatvaraju se svi prozori NVDA sa njihovim pripadajućim dijaloškim okvirima. (#1740)
* Preglednik govora može biti zatvoren uz pomoć `alt+F4` te sadrži gumb zatvori za lakšu interakciju sa pokazivačkim uređajima. (#12330)
* Preglednik brajice sada posjeduje standardnu tipku zatvori za lakšu interakciju sa pokazivačkim uređajima. (#12328)
* U popisu elemenata, prečac na gumbu "aktiviraj" je uklonjen kako bise izbjegle kolizije za neke jezike sa oznakom izbornog gumba tip elementa. Kada je dostupan, gumb je podrazumjevani u dijaloškom okviru i kao takav se može aktivirati jednostavnim pritiskom tipke enter iz samog popisa elemenata. (#6167)

### Ispravke grešaka

* Popis poruka u Outlooku 2010 je ponovno čitljiv. (#12241)
* U terminalnim programima u  Windows 10 inačici 1607 i novijim, prilikom umetanja ili brisanja znakova usred redka, znakovi sa desne strane se više ne čitaju. (#3200)
  * Ova ispravka treba biti ručno uključena u naprednim korisnicima NVDA tako da se promjeni način čitanja izmjena u terminalnih programima na Diff Match Patch.
* U MS Outlooku, nepotrebno izgovaranje daljine prilikom prelazka iz polja za uređivanje poruke u u polje za upisivanje naslova više se ne bi smjelo događati. (#10254)
* U Python konzoli, sada je podržano unošenje znaka znaka tab za uvlačenje redka, i automatsko dovršavanje. (#11532)
* Informacije o oblikovanju teksta i druge poruke u modusu čitanja više ne pokazuju neočekivane prazne redke kada se isključi izlged ekrana. (#12004)
* Sada je moguće pročitati komentare u MS Wordu sa uključenom podrškom za UIA. (#9285)
* Unapređene su performanse prilikom interakcije sa Visual studio. (#12171)
* Ispravljene su grafičke pogreške kao što su to na primjer izostavljeni elementi kada se NVDA koristi sa jezikom koji se piše s desna na lijevo. (#8859)
* Poštuje se izgled prozora i njegov smjer baziran na jeziku NVDA, umjesto na jeziku sustava. (#638)
  * Poznata pogreška za jezike koji su pisani s desna na lijevo: desni graničnik grupiranja poklapa se sa oznakama/kontrolama. (#12181)
* Jezik pythona sada poštuje jezik namješten u postavkama, te će se isti koristiti prilikom korištenja podrazumjevanog jezika sustava. (#12214)
* TextInfo.getTextInChunks više se ne ruši kada se poziva na kontrolu obogaćenog teksta kao što je to NVAD preglednik zapisnika. (#11613)
* Sada je ponovno moguće koristiti NVDA sa jezicima koji u sebi sadrže znak podvlaka u nazivu jezika kao na primjer de_CH u verzijama operacijskog sustava Windows 10 1803 i 1809. (#12250)
* U WordPadu, podešavanje izgovora indeksa i eksponenata radi kao što je to i očekivano. (#12262)
* NVDA više ne neuspijeva izgovoriti novofokusirani sadržaj na web stranici ako stari fokus nestane i bude zamijenjen novim u na toj istoj poziciji. (#12147)
* Podcrtano, eksponent i indeks sada se izgovaraju za  cijele ćelije u Excelu ako je odgovarajuća opcija uključena. (#12264)
* Ispravljeno je kopiranje konfiguracije tijekom instalacije iz prijenosne kopije kada je odredišna putanja prazna. (#12071, #12205)
* Ispravljen je neispravan izgovor nekih slova sa akcentima ili dijakritičkih znakova kada je opcija 'izgovori veliko prije velikih slova' uključena. (#11948)
* Ispravljena je nemogućnost izmjene visine pri pisanju velikih slova koristeći  SAPI4 govornu jedinicu. (#12311)
* Instalacijski program NVDA sada također poštuje `--minimal` opciju naredbenog redka te ne reproducira zvuk pokretanja, ponašajući se kao prijenosna kopija NVDA izvršne datoteke. (#12289)
* U MS Wordu ili Outlooku, tipke za kretanje poi tablicama sada mogu se koristiti za kretanej po tablicama izgleda ako ej opcija  "uključi tablce izgleda" uključena u postavkama modusa čitanja. (#11899)
* više neće izgovarati "↑↑↑" za emoji znakove u određenim jezicima. (#11963)
* Espeak sada podržava kantonski i mandarinski kineski. (#10418)
* U novom Microsoft Edge pregledniku baziranom na Chromium platformi, tekstualna polja poput adresne trake sada se izgovaraju kada su prazna. (#12474)
* Ispravljen upravljački program za Seika brajične redke. (#10787)

## 2020.4

Ova inačica uključuje novu metodu unosa za kineski, nadogradnja Liblouisa te popis elemenata (NVDA+f7) u modusu fokusa.
Kontekstualna pomoć od sada je dostupna prilikom pritiska F1 u NVDA dijaloškim okvirima.
Unapređenje pravila čitanja simbola, govornih rječnika, brajičnih poruka i letimičnog čitanja.
Ispravke grešaka i unapređenja za Mail u windowsima 10, outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
Na web stranicama, unapređenja u Google docs, i veća podrška za ARIA.
te puno drugih važnih ispravaka grešaka  i unapređenja.

### Nove značajke

* Pritiskom tipkovničkog prečaca f1 u dijaloškim okvirima, otvorit će se dio dokumentacije za za određeni dijaloški okvir. (#7757)
* Podrška samodovršavanja (IntelliSense) u Microsoft SQL Server Management Studio i Visual Studio 2017 i novijim inačicama. (#7504)
* Izgovor simbola i interpunkcije: podrška grupiranja u definiciji kompleksnih simbola te podrška za grupne reference u zamjenama čineći ih tako jednostavnijim i moćnijim alatom. (#11107)
* Od sada se korisnik obavještava prilikom pokušaja stvaranja zapisa sa netočnom zamjenom regularnog izraza. (#11407)
  * Točnije otkrivaju se greške prilikom grupiranja.
* Dodana podrška za nove metode unosa Kineski tradicionalni Quick i Pinyin U Windowsima 10. (#11562)
* Zaglavlje kartica od sada se tretiraju kao formulari po kojima se može kretati uz pomoć prečaca "f" za brzu navigaciju. (#10432)
* Dodan prečac za uključivanje ili isključivanje označenog (istaknutog) teksta; Ne postoji podrazumjevana pridjeljena gesta. (#11807)
* Dodan parametar --copy-portable-config koji omogućuje kopiranje konfiguracije u NVDA prijenosnu kopiju. (#9676)
* Za korisnike miša koji koriste brajični preglednik, od sada su dostupne virtualne routing tipke, prijeđite preko ćelije kako biste se na nju usmjerili. (#11804)
* NVDA od sada može automatski otkrivati Humanware Brailliant BI 40X and 20X brajične redke kada su spojeni preko USB ili bluetoth portova. (#11819)

### Izmjene

* Nadograđen liblouis brajični prevoditelj na inačicu 3.16.1:
 * Ispravljena višestruka rušenja
 * Dodana brajična tablica za baškirsko puno pismo
 * Dodana koptska kompjutorska brajična tablica
 * Dodana ruska literarna i ruska literarna sa prikazom velikih slova.
 * Dodana brajična tablica za afrikanersko puno pismo
 * Izbrisana je brajična tablica za rusko staro puno pismo
* Prilikom čitanja cijelog dokumenta u modusu pregleda, prečaci traži sljedeće i traži prethodno više ne zaustavljaju čitanje ako je opcija omogući letimično čitanje uključena; umjesto toga čitanje svega se nastavlja prije prethodnog ili sljedećeg pronađenog termina. (#11563)
* Za HIMS brajične retke kombinacija tipaka F3 je promijenjena u razmaknica + točkice 148. (#11710)
* Unapređenje izgleda opcija "stanka za poruke u milisekundama" i "Pokazuj poruke beskonačno". (#11602)
* U internetskim preglednicima i ostalim aplikacijama koje podržavaju modus čitanja, dijaloški okvir popis elemenata (NVDA+F7) može se otvoriti kada se nalazite u modusu fokusa. (#10453)
* Osvježavanje aria živih regija od sada je utišavano kada je izvještavanje o promjenama dinamičkog sadržaja isključeno. (#9077)
* NVDA će sada izgovoriti "kopirano u međuspremnik" prije kopiranog teksta. (#6757)
* Unapređeno čitanje tablice grafičkog pregleda u upravljanju tvrdim diskovima. (#10048)
* Oznake kontrola su od sada onemogućene (posivljene) kada je kontrola onemogućena. (#11809)
* Nadograđena CLDR anotacija Emoji na inačicu 38. (#11817)
* Ugrađena funkcija "praćenje fokusa" preimenovana je u "vizualno praćenje". (#11700)

### Ispravke grešaka

* NVDA sada ponovno radi u poljima za uređivanje pri korištenju Fast Log Entry programa. (#8996)
* Izgovaranje preostalog vremena u Foobar2000 ako ne postoji ukupno trajanje (NPR. prilikom reproduciranja streama u živo). (#11337)
* NVDA sada poštuje aria-roledescription atribut na elementima u sadržaju koji se može uređivati na web stranicama. (#11607)
* 'popis' se više ne izgovara za svaki redak popisa u Google Docs u otvorenom sadržaju koji se uređuje u Google Chromeu. (#7562)
* Prilikom kretanja kursorskim tipkama po znakovima ili slovima od jedne stavke popisa do druge u sadržaju koji se može uređivati na web stranicama, izgovara se ulazak u novi popis. (#11569)
* NVDA sada čita ispravni redak prilikom izmještanja kursora na kraj poveznice na kraju popisa u Google Docsu ili drugom sadržaju koji se može uređivati na web stranicama. (#11606)
* U Windowsima 7, otvaranje i zatvaranje start izbornika sa radne površine sada postavlja fokus pravilno. (#10567)
* Kada je opcija "pokušaj otkloniti događaje fokusa koji su istekli" omogućena, naslov kartice se sada izgovara ponovno prilikom prebacivanja kartica u Firefoxu. (#11397)
* NVDA više nema probleme poslije upisivanja znakova u popisu prilikom korištenja SAPI5 Ivona glasova. (#11651)
* Sada je ponovno moguće korištenje modusa čitanja prilikom čitanja elektroničke pošte u  Windows 10 Mailu 16005.13110 and later. (#11439)
* Prilikom korištenja SAPI5 Ivona glasova sa stranice harposoftware.com, NVDA sada može spremati svoju konfiguraciju, prebacivati govorne jedinice, te više te se neće utišavati poslije ponovnog pokretanja. (#11650)
* Sada je moguće upisati znamenku  6 koristeći kompjutorsku brajicu sa brajične tipkovnice na Himsovim brajičnim redcima. (#11710)
* Drastično poboljšanje performansi u Azure Data Studiu. (#11533, #11715)
* Sa uključenom opcijom "pokušaj ignoriranja događaja fokusa koji su istekli"  naslov dijaloškog okvira NVDA pretrage ponovno se čita. (#11632)
* NVDA više se ne bi trebao rušiti prilikom buđenja računala i premještanja fokusa u Microsoft edge dokumentu. (#11576)
* Više nije potrebno pritiskati tabulator ili premještati fokus poslije zatvaranja kontekstnog izbornika  kako bi način pregleda bio funkcionalan u MS edgeu. (#11202)
* NVDA sada čita stavke popisa unutar 64-bitnih aplikacija poput Tortoise SVN-a. (#8175)
* Aria mrežaste strukture sada se pokazuju kao normalne tablice u modusu čitanja u Firefoxu i Chromeu. (#9715)
* Obratna pretraga sada može biti započeta uz pomoć komande 'traži prethodno'  NVDA+shift+F3 (#11770)
* NVDA skripta se više ne tretira kao ponovljena ako se dogodi nerelevantni pritisak između dva izvršavanja skripte. (#11388) 
* Strong i emphasis tagovi u Internet exploreru opet mogu biti utišani tako da se isključi opcija izvještavaj o isticanju u postavkama oblikovanja. (#11808)
* Zastoj od nekoliko sekundi koji je iskusio mali broj korisnika a koji se događao prilikom kretanja po ćelijama u Excel više se ne bi trebao događati. (#11818)
* U Microsoft Teams kompilacijama sa brojevima verzija poput 1.3.00.28xxx, NVDA više neće odbijati čitati poruke u čavrljanjima ili kanalima skupine zbog nekorektno fokusiranog izbornika. (#11821)
* Tekst koji je u   Google Chrome označen istovremeno kao pravopisna i gramatička pogreška tako će biti i izgovoren. (#11787)
* Prilikom korištenja Microsoft outlooka na francuskom jeziku, prečac za  akciju 'odgovori svima' (control+shift+R) radi ponovno. (#11196)
* U Visual Studio, IntelliSense alatni savjetnici koji daju više detalja o trenutnoj stavci IntelliSense sada se izgovaraju samo jednom. (#11611)
* U Windows 10 kalkulatoru, NVDA više neće izgovarati tijek izračuna ako je opcija izgovor upisanih znakova isključena. (#9428)
* NVDA više se ne ruši prilikom korištenja Engleskog kratkopisa  za sjedinjene države te proširi riječ na kompjutorsku brajicu pod kursorom , prilikom prikazivanja određenog sadržaja kao pto je to internetska adresa. (#11754)
* Od sada je ponovno moguće čitati informacije o oblikovanju za fokusiranu ćeliju u Excelu koristeći prečac NVDA+F. (#11914)
* Unos sa qwerty tipkovnice na papenmeierovim brajičnim redcima, koji to podržavaju ponovno radi, a NVDA se više ne smrzava u slučajnim situacijama. (#11944)

## 2020.3

Ova inačica uključuje nekoliko velikih unapređenja stabilnosti i performansi u Microsoft Office aplikacijama. Dodane su nove postavke za uključivanje izgovora grafičkih elemenata i podrške ekrana osjetljivih na dodir.
U preglednicima sada se može izgovarati postojanje označenog (obilježenog sadržaja), te dodane su i nove brajične tablice za njemački jezik.

### Nove značajke

* Sada možete uključivati ili isključivati izgovor grafičkih elemenata u postavkama oblikovanja dokumenta. Imajte na umu da isključivanjem ove opcije alternativni tekst će se i dalje čitati. (#4837)
* Sada možete uključivati ili isključivati podršku ekrana osjetljivih na dodir. Dodana je opcija na panel interakcije s ekranima osjetljivim na dodir. Podrazumjevani prečac za ovu opciju je NVDA+control+alt+t. (#9682)
* Dodane nove brajične tablice za njemački jezik. (#11268)
* NVDA sada izvještava o UIA kontrolama UIA koje su samo za čitanje. (#10494)
* Postojanje obilježenog teksta ili sadržaja sada se izgovara i pokazuje na brajičnom retku u web preglednicima. (#11436)
 * Ovo se može uključiti ili isključiti u postavkama oblikovanja dokumenta pomoću nove opcije za obilježavanje.
* Novi emulirani tipkovnički prečaci sada se mogu dadavati koristeći dijaloški okvir ulaznih gesti. (#6060)
  * Kako biste dodali takav prečac, pritisnite gumb dodaj poslje označavanja kategorije emulirani tipkovnički prečaci.
* Sada je podržan Handy Tech Active Braille sa joistickom. (#11655)
* Opcija "automatski način fokusa pri kretanju kursora" sada je kompatibilna sa onemogućavanjem o opcijom "automatski postavi fokus na elemente koji se mogu fokusirati". (#11663)

### Izmjene

* Prečac za izvještavanje o oblikovanju dokumenta (NVDA+f) je izmijenjen tako da izgovara izmjene pod kursorom sustava umjesto preglednog kursora. Kako biste čuli izmjene oblikovanja dokumenta pod preglednim kursorom Sada trebate koristiti prečac NVDA+shift+f. (#9505)
* NVDA više ne postavlja fokus na elemente koji se mogu fokusirati u web preglednicima, što unapređuje stabilnost i brzinu. (#11190)
* CLDR je nadograđen s inačice 36.1 na inačicu 37. (#11303)
* Nadograđen eSpeak-NG na inačicu 1.51-dev, commit 1fb68ffffea4
* Sada možete koristiti tabličnu navigaciju za popise sa označivim stavkama kada taj određen popis ima više stupaca. (#8857)
* U upravitelju dodataka, kada se pojavi pitanje o uklanjanju dodatka, gumb "ne" sada je podrazumjevana opcija. (#10015)
* U Microsoft Excelu, popis elemenata sada pokazuje formule u njihovom prevedenom obliku. (#9144)
* NVDA sada izgovara ispravnu terminologiju za bilješke u MS Excelu. (#11311)
* Kada se koristi prečac "premjesti pregledni kursor na fokus" u načinu pregleda, pregledni se kursor premješta na poziciju virtualnog kursora. (#9622)
* Informacije prikazane u modusu pregleda poput informacija o oblikovanju dokumenata koje se dobiju pritiskom NVDA+F, sada se prikazuju u malo većem prozoru koji se nalazi na sredini zaslona. (#9910)

### Ispravke grešaka

* NVDA sada izgovara simbol prilikom stajanja na riječi i kada znak slijedi poslije bijelog razmaka neovisno od postavke izgovora. (#5133)
* U aplikacijama koje koriste QT 5.11 ili noviji, opisi objekta sada ponovno izgovaraju. (#8604)
* Prilikom brisanja riječi kraticom control+delete, NVDA više ne ostaje tih. (#3298, #11029)
  * sada se izgovara rijeć koja slijedi poslije izbrisane riječi.
* U panelu općih postavki, popis jezika se sada ispravno sortira. (#10348)
* Značajno unapređene performanse u dijaloškom okviru ulaznih gesti prilikom filtriranja. (#10307)(
* Sada možete sa brajičnog retka upisivati Unicode znakove iznad vrijednosti  U+FFFF. (#10796)
* NVDA će sada ispravno čitati sadržaj dijaloškog okvira otvori sa u nadogradnji Windows 10 za svibanj 2020. (#11335)
* Dodana je nova eksperimentalna opcija u  naprednim postavkama (Uključi selektivnu registraciju UIA događaja i izmjena svojstava) koja može unaprijediti performance u Visual studio i drugim UIA automation aplikacijama ako je uključena. (#11077, #11209)
* Za stavke popisa koje se mogu odabrati, stanje označenosti se ne izgovara izlišno, te ako je moguće, umjesto njega se izgovara status neoznačenosti. (#8554)
* U Windowsima 10 nadogradnji za svibanj 2020, NVDA saa prikazuje Microsoft zvučni enumerator u dijaloškom okviru govorna jedinica. (#11349)
* U Internet Exploreru, brojevi se sada točno izgovaraju za parne popise ako popis ne počinje brojem 1. (#8438)
* U Google chromeu, NVDA će sada izgovarati "nije odabrano"  za sve kontrole koje su označive (ne samo za potvrdne okvire) koji su trenutno neoznačeni. (#11377)
* Sada je ponovno moguće kretati se po raznim kontrolama ako je jezik NVDA postavljen na Aragonski. (#11384)
* NVDA više se neće zaglavljivati u Microsoft Wordu prilikom brzog kretanja strelicama ili upisivanja znakova. (#11431, #11425, #11414)
* NVDA više ne dodaje nepostojeći dupli razmak prilikom kopiranja trenutnog objekta navigatora u međuspremnik. (#11438)
* NVDA više ne aktivira profil za čitanje cijelog sadržaja ako ne postoji ništa za čitanje. (#10899, #9947)
* NVDA sada čita popis funkcija u upravitelju internetskih servisa informacija (IIS). (#11468)
* NVDA sada ostavlja otvorenu zvučnu karticu takvim načinom poboljšavajući performanse (#5172, #10721)
* NVDA više se neće smrznuti ili srušiti prilikom pritiska i držanja ctrl+shift+strelica dolje u Microsoft Wordu. (#9463)
* Stanje skupljenosti ili raširenosti mapa na stranici drive.google.com sada je pravilno izgovarano. (#11520)
* Veliko unaprjeđenje performansi u Visual Studio Code. (#11533)

## 2020.2

Novosti u ovoj inačici uključuju podršku za novi brajični redak tvrtke Nattiq, poboljšanu podršku za antivirus eset nod32 te winodws naredbeni redak, unapređenje performanis u programu 1Password, poboljšanja sa sintetizatorom govora One core. Također, u ovu inačicu uvršteni su i puno drugih popravaka grešaka.

### Nove značajke

* Podrška za nove brajične retke:
  * Nattiq nBraille (#10778)
* Dodana mogučnost pridjeljivanja prečaca naredbi otvaranja konfiguracijske mape NVDA (Nema dodjeljene podrazumjevane geste). (#2214)
* Poboljšana podrška za dijaloške okvire ESET antivirusa. (#10894)
* Dodana podrška za Windows terminal. (#10305)
* Dodan prečac za izgovaranje trenutnog konfiguracijskog profila (nije dodjeljen podrazumjevano). (#9325)
* Dodan prečac za uključivanje i isključivanje izgovora eksponenata i indekasa (nema podrazumjevane geste). (#10985)
* Web aplikacije (npr. Gmail) više ne izgovaraju zastarjele informacije prilikom brzog kretanja. (#10885)
  * Ova eksperimentalna ispravka grešaka mora biti ručno uključena uz pomoć opcije 'pokušaj zaustavljanja govora za zastarjele događeje fokusa' na naprednom panelu postavki.
* Puno simbola je dodano u podrazumjevani rječnik simbola. (#11105)

### Izmjene

* Nadograđen liblouis brajični prevoditelj s inačice 3.12 Na inačicu [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Izgovaranje indekasa i eksponenata sada se regulira odvojeno od izgovaranja atributa fonta. (#10919)
* Zbog promjena nastalih u VS Code, NVDA više podrazumjevano je isključuje modus pregleda. (#10888)
* NVDA više ne izgovara "početak" i "kraj" prilikom izravnog kretanja preglednim kursorom na prvi ili zadnji redak objekta navigatora uz pomoć prečaca premjesti se na početak i premjesti se na kraj. (#9551)
* NVDA više ne izgovara  "lijevo" i "desno" prilikom izravnog kretanja kursora pregleda na prvi ili zadnji znak u retku za trenutni objekt navigatora uz pomoć prečaca pomakni se na početak retka i pomoakni se na kraj retka. (#9551)

### Ispravke grešaka

* NVDA se sada ispravno pokreće kada nije moguće stvoriti datoteku zapisnika. (#6330)
* U posljednjim inačicama Microsoft Word 365, NVDA više neće izgovarati "brisanje posljednie riječi" kada je pritisnut prečac ctrl+bacpspace prilikom uređivanja dokumenta. (#10851)
* NVDA će opet izgovarati status uključenosti izmješanosti ili ponavljanja popisa za reprodukciju. (#10945)
* NVDA više nije ekstremno usporen prilikom kretanja po stavkama popisa u 1Passwordu. (#10508)
* Windows OneCore govorna jedinica više ne zastajkuje između izričaja. (#10721)
* NVDA više se ne smrzava prilimom otvaranja kontekstnog izbornika za 1Password u području obavijesti. (#11017)
* U Officeu 2013 i starijim:
  * Riboni se izgovaraju kada se fokus na njima nađe prvi put. (#4207)
  * Stavke kontekstnog izbornika sada se ponovno točno izgovaraju. (#9252)
  * Sekcije ribona sada su točno najavljivane prilikom kretanja po njima uz pomoć prečaca ctrl+strelica lijevo ili desno. (#7067)
* U načinu pregleda u Mozilla firefoxu I Google chromeu, tekst se više ne pojavljuje u jednom retku kada web sadržaj koristi CSS display: inline-flex. (#11075)
* U načinu pregleda sa opcijom Automatsko postavljanje fokusa na fokusirane elemente onemogućenom, sada je moguće aktivirati elemente koje nije moguće fokusirati.
* U načinu pregleda sa isključenom opcijom automatski postavi fokus na fokusirene elemente, sada je moguće aktivirati elemente koji se nalaze pod tabulatorom. (#8528)
* U načinu pregleda sa isključenom opcijom automatski postavi fokus na fokusirane elemente, više se ne događa klikanje na pogrešnu lokaciju. (#9886)
* NVDA zvuci pogreške više se ne reproduciraju prilikom pristupa kontrolama DevExpress. (#10918)
* Alatni savjetnici ikona u polju obavijesti više se ne izgovaraju prilikom kretanja tipkovnicom ako je njihov tekst jednak nazivu ikone, kako bi se izbjeglo duplo izgovaranje. (#6656)
* U načinu pregleda sa isključenom opcijom automatski postavi fokus na fokusirane elemente, prebacivanje modusa fokusa uz pomoć prečaca insert+razmak, sada fokusira element pod kursorom. (#11206)
* Sada je pomovno moguće provjeravati nadogradnje NVDA na nekim sustavima; NPR. čise instalacije Windowsa. (#11253)
* Fokus se ne premješta u Java aplikacijama kada se fokus mijenja u stablu prikaza, tablici ili popisu. (#5989)

## 2020.1

Novosti u ovoj inačici uključuju podrška novih brajičnih redaka firmi HumanWare i APH, te puno važnih ispravaka grešaka poput ponovnog omogućavanja čitanja matematičkog sadržaja u Microsoft Wordu koristeći MathPlayer / MathType.

### Nove značajke

* Označena stavka se sada ponovno pokazuje u načinu pregleda u Chromeu, slično kao u  NVDA 2019.1. (#10713)
* Sada možete izvoditi desni klik miša na dodirnim uređajima tako da dodirnete i držite jedan prst na ekranu. (#3886)
* Podrška za nove brajične retke: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, and NLS eReader. (#10830)

### Izmjene

* NVDA će spriječiti sustav u pokušaju odlaska u status mirovanja prilikom izvršavanja naredbe čitaj sve. (#10643)
* Podrška za izvanprocesne okvire u Mozilla Firefoxu. (#10707)
* Nadograđen liblouis brajični prevoditelj na inačicu 3.12. (#10161)

### Ispravke grešaka

* Ispravljena pogreška, koja je onemogućavala čitanje znaka za minus (U+2212) (#10633)
* Prilikom instalacije dodataka iz upravitelja dodataka, Imena datoteka i mapa se ne izgovaraju dva puta. (#10620, #2395)
* U Firefoxu, prilikom učitavanja Mastodona sa uključenim naprednim web sučeljem, sve se vremenske osi prikazuju pravilno u načinu čitanja. (#10776)
* U načinu pregleda, NVDA sada izgovara "nije odabrano" za potvrdne okvire u kojima to prethodno nije bilo činjeno. (#10781)
* ARIA kontrole preklopnika više ne izgovaraju zbunjujuće informacije kao što su to "nije pritisnuto odabrano" ili "pritisnuto odabrano". (#9187)
* SAPI4 glasovi više ne odbijaju izgovarati većinu teksta. Bilješka prevoditelja: To se tiče sintetizatora govora koji ne stignu poslati informaciju čitaču zaslona da su primili informaciju o izgovorenom tekstu. (#10792)
* NVDA može ponovno čitati i ulaziti u interakciju sa matematičkim jednadžbama u Microsoft Wordu. (#10803)
* NVDA će od sada izgovarati neoznačeni tekst u modusu pregleda prilikom pritiska strelice kada je tekst označen. (#10731).
* NVDA se više ne isključuje ako postoji greška inicijalizacije Espeaka. (#10607)
* Greške prouzročeneUnicode kodnom stranicom pri prevedenom tipkovničkom prečacu više ne onemogućavaju stvaranje prečaca radne površine, Rješeno tako da će se instalacijski program vratiti na engleski tekst. (#5166, #6326)
* Ulazeći i izlazeći iz popisa i tablica prilikom čitanja svega ili letimičnog čitanja više ne izgovara činjenicu o izlazu iz tablice ili popisa. (#10706)
* Ispravljeno praćenje miša na nekim MSHTML elementima u Internet Exploreru. (#10736)

## 2019.3

NVDA 2019.3 je inačica koja sadrži puno značajnih promjena uključujući nadogradnju Pythona 2 na Python 3, te veliko prepisivanje podsistema govora.
Iako ove izmjene stare dodatke čine nekompatibilnima, Nadogradnja na Python 3 bila je nužna radi sigurnosti, a izmjene u podsistemu govora će otvoriti put za nove inovativne mogućnosti u bliskoj budućnosti.
 Ostale izmjene uključuju 64 bitnu podršku za Java virtualne mašine, zaslonsku zavjesu i označitelja fokusa, podrška za puno više brajičnih redaka te novi brajični preglednik, te puno drugih ispravaka grešaka.

### Nove značajke

* Točnost komande "premjesti miš na objekt navigatora", sada je unapređena u tekstualnim poljima u Java aplikacijama. (#10157)
* Dodana podrška za sljedeće Handy Techove brajične retke (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Sve korisnički definirane opcije sada mogu biti uklonjene uz pomoć novog gumba "Vrati na zadane vrijednosti" u dijaloškom okviru ulazne geste. (#10293)
* Izvještavanje o fontu u Microsoft Wordu sada uključuje informaciju o tome jeli tekst skriven. (#8713)
* Dodana komanda za premještavanje kursora pregleda na poziciju označenu kao početni marker za označavanje ili kopiranje: NVDA+shift+F9. (#1969)
* U Internet Exploreru, Microsoft Edgeu i posljednjim inačicama Firefoxa i Chromea, orjentiri su sada izgovoreni u načinu fokusate uz pomoć objektne navigacije. (#10101)
* U Internet Exploreru, Google Chromeu i Mozilla Firefoxu, sada se možete kretati po člancima i grupama koristeći prečace za brzo kretanje. Podrazumjevano ovi prečaci nisu pridjeljeni i mogu se pridjeliti u dijaloškom okviru ulaznih gesti kada je dijaloški okvir otvoren u dokumentu koji koristi način pregleda. (#9227)
 * Figure se također izgovaraju. Iste se smatraju objektima i stoga se po njima može kretati koristeći kraticu brzog kretanja "o".
* U Internet Exploreru, Google Chromeu i Mozilla Firefoxu, članci se sada izgovaraju koristeći objektnu navigaciju, te neobavezno u načinu pregleda ako je opcija uključena u postavkama oblikovanja dokumenta. (#10424)
* Dodana zaslonska zavjesa, koja kada je uključena, zatamnjuje zaslon u Windowsima 8 i novijim. (#7857)
 * Dodan prečac za omogućavanje zaslonske zavjese (do sljedećeg ponovnog pokretanja sa jednim pritiskom, ili uvijek kada je NVDA pokrenut sa dva pritiska). Ovaj prečac nije dodijeljen.
 * Može biti uključeno preko kategorije 'vid' u dijaloškom okviru NVDA postavki.
* Dodana značajka označavanja zaslona u NVDA. (#971, #9064)
 * Označavanje fokusa, objekta navigatora, i kursora u modusu pregleda može biti omogućeno i podešeno preko kategorije vid u dijaloškom okviru NVDA postavki.
 * Napomena: ova je značajka nekompatibilna s dodatkom Focus highlight, međutim, dodatak se moš uvjek može koristiti kada je ugrađeni označivač uključen.
* Dodan brajični preglednik, koji omogućuje prikaz brajice na zaslonu. (#7788)

### Izmjene

* Vodič za korisnike sada opisuje kako koristiti Windowsov naredbeni redak s NVDA. (#9957)
* Pokretanje nvda.exe sada podrazumjevano zamjenjuje već pokrenutu kopiju NVDA. Parametar -r|--replace se još uvijek prihvaća, ali je isti ignoriran. (#8320)
* U Windowsima 8 i novijim, NVDA će sada izgovoriti nazim aplikacije i inačicu za hostane aplikacije poput aplikacija u Microsoft Store-u koristeći informaciju koju je NVDA dobio od aplikacije. (#4259, #10108)
* Prilikom uključivanja praćenja izmjena u Microsoft Wordu putem tipkovnice, NVDA će izgovarati stanje postavke. (#942) 
* NVDA inačica je prva zapisivana u zapisniku. Ovo se događa kada je vođenje zapisnika isključeno u postavkama. (#9803)
* Iz dijaloškog okvira postavki više nije moguće mijenjati razinu vođenja zapisnika, ako je parametar nadpisan preko naredbenog retka. (#10209)
* U Microsoft Wordu, NVDA sada izgovara status pokazivanja znakova koji se ne pokazuju prilikom ispisa kada se pritisne prečac za uključivanje ili isključivanje ove opcije Ctrl+Shift+8. (#10241)
* Nadograđen Liblouis brajični prevoditelj na inačicu 58d67e63. (#10094)
* Kada je uključeno izgovaranje CLDR znakova, uključujući emoji,, oni se izgovaraju neovisno od razine interpunkcije. (#8826)
* Pythonovski paketi treće strane, kao što je to comtypes, sada zapisuju svoje greške i upozorenja u NVDA zapisnik. (#10393)
* Nadograđen opći repozitorij Unicode znakova na inačicu 36.0. (#10426)
* Prilikom fokusiranja grupe u modusu pregleda, sada se izgovara i opis. (#10095)
* Java Access Bridge se sada isporučuje sa NVDA kako bi se omogućio pristup java aplikacijama, uključujući i 64-bitne Java virtualne mašine. (#7724)
* Ako Java Access Bridge nije uključen za korisnika, NVDA automatski ga uključuje pri pokretanju. (#7952)
* Nadograđen eSpeak-NG na inačicu 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Ispravci Grešaka

* Emoji i ostali 32-bitni unicode znakovi sada zauzimaju manje mjesta na brajičnom retku kada se pokazuju kao heksadecimalne vrijednosti. (#6695)
* U Windowsima 10, NVDA će izgovarati alatne savjetnike iz univerzalnih aplikacija ako je NVDA podešen da ih izgovara putem dijaloškog okvira prezentacija objekta. (#8118)
* U Windows 10 jubilejnoj nadogradnji i novijim, upisani se tekst izgovara u Mintty. (#1348)
* U Windowsima 10 jubilejnoj nadogradnji i novijim, izlazna informacija u Windows naredbenom retku koja se pojavljuje blizu kursora više se ne slovka. (#513)
* Sada se izgovaraju kontrole kompresora u dijaloškom okviru kompresora u Audacity prilikom kretanja po dijaloškom okviru. (#10103)
* NVDA više ne tretira razmake kao riječi s objektnom navigacijom u Scintilla uređivačima teksta poput Notepadd++. (#8295)
* NVDA će spriječiti sustav da uspava računalo kada se krećemo po tekstu uz pomoć brajičnog retka. (#9175)
* U Windowsima 10, brajica će pratiti uređivanje sadržaja ćelije i drugim UIA kontrolama teksta kada je isti zaostajao. (#9749)
* NVDA će opet izgovarati prijedloge u Microsoft Edge adresnoj traci. (#7554)
* NVDA više nije tih prilikom fokusiranja zaglavlja HTML kontrolne kartice u Internet Exploreru. (#8898)
* U Microsoft Edge baziranom na EdgeHTML, NVDA više neće reproducirati zvuk prijedloga pretrage kada prozor postane maksimiziran. (#9110, #10002)
* ARIA 1.1 odabirni okviri sada su podržani u Mozilla Firefoxu i Google Chromeu. (#9616)
* NVDA više neće izgovarati vizualno skriveni sadržaj stupaca za popise u SysListView32 kontrolama. (#8268)
* Dijaloški okvir postavki više ne pokazuje "info" kao trenutnu razinu zapisnika kada se nalazi u sigurnom načinu. (#10209)
* U izborniku start Windowsa 10 jubilejne nadogradnje i novijim, NVDA će izgovarati detalje rezultata pretrage. (#10232)
* U načinu pregleda, ako kretnja kursora ili brzo kretanje prouzrokuju promjenu dokumenta, NVDA više ne izgovara neispravan sadržaj u nekim situacijama. (#8831, #10343)
* Neka imena točaka su ispravljena u Microsoft Wordu. (#10399)
* U Windowsima 10 nadogradnji za svibanj 2019 i novijoj, NVDA će opet izgovarati prvu stavku na popisu emoji ili element međuspremnika kada se otvori povijest međuspremnika ili emoji panel. (#9204)
* U Poeditu, opet je moguće čitati prijevode za jezike koji se pišu s desna na lijevo. (#9931)
* U postavkama u Windowsima 10 nadogradnji za travanj 2018 i novijim, NVDA više neće izgovarati informaciju o postotcima za metre glasnoće koji se nalaze na stranici zvuk. (#10284)
* Nepravilni regularni izrazi više ne zaustavljaju govor u NVDA. (#10334)
* Prilikom čitanja liste nabrajanja u Microsoft Wordu sa uključenim UIA, sljedeća stavka popisa više se ne izgovara na neželjen način. (#9613)
* Nekoliko rijetkih grešaka sa brajičnim prevođenjem i Liblouis brajičnim prevoditeljem je ispravljeno. (#9982)
* Java aplikacije pokrenute prije NVDA sada se pokreću bez potrebe za ponovnim pokretanjem Java aplikacije. (#10296)
* U Mozilla Firefoxu, kada je fokusirani element označen kao trenutan (aria-current), više se ne izgovara više puta uzastopce. (#8960)
* NVDA će sada tretirati neke sastavne unicode znakove poput e s naglaskom kao jedan znak prilikom kretanja po tekstu. (#10550)
* Spring Tool Suite inačica 4 sada je podržana. (#10001)
* Kada je Aria-labellz unutrašnji element, ozgovor se neće dublirati. (#10552)
* U Windowsima 10 inačici 1607 i novijim, upisani znakovi na brajičnim tipkovnicama sada su izgovoreni u većini situacija ispravno. (#10569)
* Prilikom izmjene izlaznog audio uređaja, zvukovi koje reproducira NVDA sada će se reproducirati na novom uređaju. (#2167)
* U Mozilla Firefoxu, kretanje u modusu pregleda je sada brže. Ovo omogućuje brže kretanje kursorom u puno slučajeva. (#10584)

## 2019.2.1

Ovo je mala inačica koja ispravlja nekoliko rušenja u inačici 2019.2. Ispravci uključuju:

* Ispravljeno nekoliko rušenja u Gmail-u uočeno u  Firefoxu i Chromeu prilikom interakcije sa nekim skočnim izbornicima, kao što je to stvaranje filtera ili mijenjanje nekih postavki Gmail-a. (#10175, #9402, #8924)
* U Windowsima 7, NVDA više neće prouzrokovati rušenje Windows upravitelja za datoteke kada se miš koristi u start izborniku. (#9435) 
* Windows Explorer u Windowsima 7 se više ne ruši prilikom pristupa metapodatcima. (#5337) 
* NVDA se više ne ruši prilikom interakcije sa slikama koje sadrže base64 URI u Mozilla Firefoxu ili Google Chromeu. (#10227)

## 2019.2

Novosti u ovoj inačici uključuju  automatsko otkrivanje Freedom Scientific brajičnih redaka, eksperimentalnu postavku u panelu naprednih postavki koja zaustavlja način pregleda da pomiće fokus (što može doprinijeti unapređenim performansama), opciju dodatne vrzine za  Windows OneCore govornu jedinicu kako bise postigle velike brzine govora, i mnogo drugih ispravaka grešaka.

### Nove značajke

* NVDA podrška za Miranda NG radi s novijim inačicama klijenta. (#9053) 
* Sada podrazumjevano možete isključiti način pregleda isključujući opciju "uključi način pregleda pri učitavanju stranice" u postavkama načina pregleda NVDA. (#8716) 
 * Imajte na umu da kada je ova opcija isključena, Još uvjek možete ručno uključiti način pregleda pritiščući tipkovnički prečac nvda+razmak.
* Sada možete filtrirati simbole u dijaloškom okviru izgovora simbola, na sličan način na koji filtriranje radi u popisu elemenata i dijaloškom okviru ulaznih gesti. (#5761)
* Dodana je komanda uz pomoć koje može se promjeniti razlučivost jedinice miša (to jest, kako će tekst biti izgovaran pri pomicanju miša), Ta komanda nema pridjeljen prečac. (#9056)
* windows OneCore govorna jedinica sada podržava opciju dodatne brzine, što omogućava veću regulaciju brzine. (#7498)
* Opcija dodatne brzine sada se može podešavati koristeći prsten govornih jedinica za podržane govorne jedinice. (trenutno su to eSpeak-NG i Windows OneCore). (#8934)
* Konfiguracijski profili sada mogu biti ručno aktivirani uz pomoć gesti. (#4209)
 * Geste mogu biti konfigurirane u dijaloškom okviru "ulazne geste".
* Dodana podrška samodovršavanja u Eclipse uređivaču izvornog koda. (#5667)
 * Dodatno, Javadoc informacija može se pročitati iz uređivača kada ista postoji koristeći NVDA+d.
* Dodana eksperimentalna opcija на panel naprednih postavki koja zaustavlja praćenje fokusa sustava u načinu pregleda (Automatski postavi  način pregleda na elemente fokusa). (#2039) Although this may not be suitable to turn off for all websites, this may fix: 
 * Efekt postranosti: NVDA sporadično poništava posljednih prečac u načinu pregleda preskačući na prethodnu poziciju.
 * Polja za uređivanje uzimaju fokus sustava prilikom kretanja po njima na nekim web stranicama.
 * Prečaci načina pregleda su sporoodzivni.
* Za brajične retke koji to podržavaju, postavke upravljačkog programa se mogu izmjeniti iz kategorije brajičnih postavki U NVDA postavkama. (#7452)
* Automatsko otkrivanje brajičnih redaka sada podržava i Freedom Scientific brajične retke. (#7727)
* Dodana komanda koja prikazuje zamjenu za simbol pod preglednim kursorom. (#9286)
* Dodana eksperimentalna funkcija na panel postavki "napredno", koja omogućuje isprobavanje nove podrške za Windows naredbene retke, koja je još u izradi, koja koristi novi UI Automation API. (#9614)
* U Python konzoli, polje za uređivanje sada podržava ljepljenje više redaka iz međuspremnika. (#9776)

### Izmjene

* Glasnoća govorne jedinice sada se može pojačavati ili smanjivati po svakih pet posto umjesto po svakih deset, koristeći prsten govorne jedinice. (#6754)
* Objašnjen test u NVDA upravitelju dodataka kada je NVDA pokrenut sa zastavicom --disable-add-ons. (#9473)
* Nadograđen repozitorij djeljenog repozitorija anotacija za emoji na inačicu 35.0. (#9445)
* Prečac za polje filtriranja u popisu elemenata u načinu pregleda je promjenjen na alt+y. Bilješka prevoditelja: ista se promjena ne odnosi na hrvatski prijevod NVDA! (#8728)
* Kada je automatski otkriven brajični redak spojen preko Bluetooth veze, NVDA će i dalje tražiti retke povezane preko USB priključka, a koji su podržani od strane istog upravljačkog programa, te će se prebaciti na USB vezu, ako je ista podržana. (#8853)
* Nadograđen eSpeak-NG na inačicu 67324cc.
* Nadograđen liblouis brajični prevoditelj na inačicu 3.10.0. (#9439, #9678)
* NVDA će sada izgovarati riječ  'označeno' poslije trenutnog označenog teksta.(#9028, #9909)
* U Microsoft Visual Studio Code, NVDA se sada podrazumjevano nalazi u načinu fokusa. (#9828)

### Ispravci grešaka

* NVDA se više ne ruši kada je mapa s dodacima prazna. (#7686)
* LTR i RTL znakovi sada se e pokazuju na brajičnom retku ili izgovaraju kada pristupate svojstvima u upravitelju datoteka. (#8361)
* Prilikom preskakanja po formularima u načinu pregleda brzim kretanjem,sada se izgovara cijeli formular umjesto cjijelog retka. (#9388)
* NVDA više se neće utišavati prilikom zatvaranja Windows 10 aplikacije pošta. (#9341)
* NVDA više neće odbijati pokretanje kada su korisničke regionalne postavke podešene na lokalnu postavku koju NVDA ne prepoznaje, poput engleskog (Nizozemska). (#8726)
* Kada je način pregleda uključen u Microsoft excelu i kada se prebacujete između načina pregleda i obratno, status načina pregleda se sada izgovara u skladu sa stvarnim stanjem. (#8846)
* NVDA sada pravilno izzgovara redak pod kursorom u  Notepad++ i drugim Scintilla uređivačima teksta. (#5450)
* U Google Docs (i drugim web baziranim uređivačima teksta), brajica više ne pokazuje sporadično "kr pop" ispred kursora usred stavke popisa. (#9477)
* U Windows 10 nadogradnji za svibanj 2019, NVDA više ne izgovara puno obavijesti o smanjivanju ili povećavanju glasnoće ako se glasnoća mjenja sa hardverskim gumbima kada upravitelj za datoteke je u fokusu. (#9466)
* Pokretanje dijaloškog okvira izgovora simbola i interpunkcije sada je puno brže kada se koriste rječnici simbola koji sadrže preko 1000 zapisa. (#8790)
* U Scintilla kontrolama kao što je to Notepad++, NVDA može sada čitati točan broj retka kada je rastavljanje riječi uključeno. (#9424)
* U Microsoft Excelu, izgovara se pozicija ćelije kada se ista promjeni zbog prečaca shift+enter ili shift+numEnter. (#9499)
* U Visual Studio 2017 novijim, u pregledniku objekata, označena stavka u drvu objekta ili drvu članova sa kategorijama sada se izgovara točno. (#9311)
* Nazivi dodataka koji se razlikuju samo u velikom slovu više se ne tretiraju kao zasebni dodaci. (#9334)
* Za Windows OneCore glasove, brzina koja se postavi u NVDA više ne utjeće na brzinu u Windows 10 uppostavkama govora. (#7498)
* Zapisnik se sada može otvoriti uz pomoć prečaca NVDA+F1 kada ne postoji informacija za razvojne programere za trenutni objekt navigatora. (#8613)
* Sada je opet moguće koristiti NVDA prečace za navigaciju po tablicama u Google Docs, u Firefoxu i Chromeu. (#9494)
* Bumper tipke sada rade ispravno na Freedom Scientific brajičnim recima. (#8849)
* HTCom se sada može koristiti u kombinaciji sa HandyTech brajičnim retcima i NVDA. (#9691)
* U Mozilla Firefoxu, nadogradnje živih regija se ne izgovaraju ako je živa regija u pozadinskoj kartici. (#1318)
* NVDA dijaloški okvir traženja u načinu pregleda više ne odbija poslušnost ako je otvoren dijaloški okvir "o NVDA" u pozadini. (#8566)

## 2019.1

Novosti u ovoj inačici uključuju unapređene performanse u pristupu Microsoft Wordu i Excelu, Poboljšanja u stabilnosti i sigurnosti poput dodataka sa informacijama o inačici, I mnogo drugih ispravaka grešaka.

Imajte na umu, da od ove inačice NVDA, Prilagođeni moduli aplikacija, upravljački programi za brajične retke, te upravljački programi govornih jedinica više se neće pokretati iz vaše mape korisničkih postavki NVDA. 
Isti bi se trebali umjesto načina iznad, instalirati kao NVDA dodaci. Za one, koji razvijaju kod za dodatak, Kod se može razmjestiti u Pješčanik za razvojne programere, specijalnu mapu u mapi NVDA konfiguracije, ako je uključena opcija NVDA scratchpad u naprednom panelu NVDA postavki.
Ove su izmjene nužne, kako NVDA ne bi prestao raditi kada taj novi kod postane nekompatibilan.
Molimo pogledajte izmjene ispod za informacije, kako su bolje označene inačice dodataka.

### Nove značajke

* Nove brajične tablice: Afrikanerski, Arapska kompjutorska brajica, Arapski kratkopis, Španjolski kratkopis. (#4435, #9186)
* Dodana opcija U NVDA postavke miša, koja omogućava kontroliranje aplikacija uz pomoć miša. (#8452) 
 * To će omogućiti kontrolu nad udaljenim računalom uz pomoć aplikacija kao što je to Team viewer.
* Dodana postavka naredbenog retka `--enable-start-on-logon` koja omogućuje tihu instalaciju NVDA sa uključenom ili isključenom podrškom za sigurne zaslone. Ako želite da se poslije tihe instalacije NVDA pokreće na zaslonu za prijavu dodajte argument true  ili false ako ne želite da se pokreće na zaslonima za prijavu. Ako --enable-start-on-logon argument nije specificiran NVDA će se pokretati na zaslonu za prijavu, osim ako u prijašnjoj instalaciji isti nije tako konfiguriran. (#8574)
* Sada je moguće isključiti značajku zapisivanja dnevnika NVDA tako da se razina zapisivanja postavi na "onemogućeno" iz panele općenitih postavki. (#8516)
* Prisutstvo formula u LibreOfficeu i Apache OpenOffice proračunskim tablicama sada se izgovara. (#860)
* U Mozilla firefoxu i Google Chromeu, sada izgovara označeni element u popisima i stablima popisa.
 * Ovo radi u Firefoxu 66 i novijem.
 * Ovo ne radi za neke popise (HTML kontrole označavanja) u Chromeu.
* Rana podrška za aplikacije poput Mozilla Firefoxa na računalima sa ARM64 arhitekturom (na primjer, Qualcomm snapdragon) procesorima. (#9216)
* Nova kategorija naprednih postavki je dodana u NVDA dijaloški okvir postavki, uključujući opciju, koja omogućava isprobavanje pristupa do Word dokumenata uz pomoć Microsoft UI Automation API'ja. (#9200)
* Dodana podrška za grafički pregled u Windows upravljanju diskovima. (#1486)
* Dodana podrška za Handy Tech Connect Braille i Basic Braille 84. (#9249)

### Izmjene

* Nadograđen liblouis brajični prevoditelj na inačicu 3.8.0. (#9013)
* Autori NVDA dodataka sada mogu specificirati minimalnu NVDA inačicu na kojoj će se njihovi dodaci pokretati. NVDA će odbiti pokrenuti ili instalirati dodatak, u čijoj je specifikaciji NVDA inačica viša od predviđene. (#6275)
* Autori dodataka mogu specificirati zadnju testiranu NVDA inačicu u svojim dodacima. Ako je NVDA dodatak testiran sa nižom NVDA inačicom, u tom će trenutku NVDA odbiti instalaciju ili pokretanje dodatka. (#6275)
* Ova će inačica NVDA dopuštati instalaciju i pokretanje NVDA dodataka  koji ne sadrže informacije o minimalnoj i posljednjoj testiranoj inačici ali nadogradnja na novu inačicu NVDA NPR. 2019.2 može izmjeniti tu situaciju.
* Komanda "premjesti miš na objekt navigatora" je dostupna u Microsoft Wordu, kao i u drugim UIA kontrolama, osobito u Microsoft edteu. (#7916, #8371)
* Izvještavanje o tekstu pod mišem radi u Microsoft edgeu i drugim UIA aplikacijama. (#8370)
* Kada je NVDA pokrenut s parametrom naredbenog retka `--portable-path`, dodani put se popunjava prilikom stvaranja prijenosne kopije koristeći NVDA izbornik. (#8623)
* Osvježen put do Norveške kompjutorske brajične tablice, kako bi ista bila aktualna sa standardom iz 2015. godine. (#9170)
* Prilikom kretanja po odlomcima (ctrl+strelica gore ili dolje) ili prilikom kretanja po ćelijama tablice (ctrl+alt+strelice), postojanje pravopisnih grešaka više neće biti najavljivano, pa čak ako je NVDA podešena da iste automatski izgovara. Ovo je zato što odlomci i tablice mogu biti veliki, i otkrivanje pravopisnih grešaka može usporavati rad. (#9217)
* NVDA više ne pokreće prilagođene module aplikacija, globalne dodatke i upravljačke programe brajičnih redaka i govornih jedinica iz mape postavki NVDA. Umjesto toga, taj kod mora biti pakiran kao NVDA dodatak sa ispravnom informacijom o inačici, osiguravajući da se nekompatibilan kod neće pokretati sa trenutnom inačicom NVDA. (#9238)
 * Za razvojne programere koji trebaju testirati kod za vrijeme njegova razvoja,  omogućite mapu bilježnica NVDA razvojnog programera u NVDA postavkama , i kopirajte vaš kod u mapu 'scratchpad' koja se nalazi u NVDA mapi postavki kada je ista uključena.

### Ispravci grešaka

* Prilikom korištenja glasova OneCore u Windowsima 10, nadogradnji za travanj 2018 i novijim, velike pauze se više ne umeću između izričaja. (#8985)
* Prilikom kretanja po znakovima u kontrolama čistog teksta poput bloka za pisanje, ili načinu pregleda, 32'bitni znakovi koji se sastoje od dve kodne točke u utf-16 (poput ðŸ¤¦) sada će se čitati ispravno. (#8782)
* Unapređen dijaloški okvir potvrde o ponovnom pokretanju prilikom promjene jezika. Oznake i gumbi su sada kraći i manje zbunjujući. (#6416)
* Ako se sintetizator treće strane ne uspije pokrenuti, NVDA će se vratiti na Windows OneCore sintetizator govora na windowsima 10, umjesto na Espeak. (#9025)
* Uklonjen upis "dijaloškog okvira dobrodošlice", u NVDA izborniku, kada je NVDA pokrenut na sigurnim zaslonima. (#8520)
* Prilikom tabanja ili korištenja načina pregleda, legende na karticama svojstva sada se dosljednije izgovaraju. (#709)
* NVDA će sada izgovarati izmjene u odabiru za većinu kontrola odabira vremena kao što su to Alarm i sat u Windowsima 10. (#5231)
* U akcijskom centru Windowsa 10, NVDA će izgovarati poruke prilikom uključivanja svjetline zaslona ili focus assist. (#8954)
* U akcijskom centru u Windowsima 10 nadogradnji za listopad 2018 i ranijim, NVDA će prepoznavati gumb svjetline poput gumba umjesto preklopnog gumba. (#8845)
* NVDA će ponovno slijediti pokazivač i izvještavati o izmjenama u Micosoft excel poljima "idi na", i "traži". (#9042)
* Ispravljeno rijetko rušenje u Načinu pregleda u Firefoxu. (#9152)
* NVDA više ne neuspjeva izgovarati neke kontrole u Ribbonima u Microsoft Officeu 2016, kada su isti skupljeni.
* NVDA više ne neuspjeva izgovarati predložene kontakte u  prilikom upisivanje adrese u novim porukama u Outlooku 2016. (#8502)
* Zadnjih nekoliko kursorskih Routing tipki na 80 znakovnim eurobraille brajičnim recima više ne usmjeravaju redak na početak retka ili usred početka retka. (#9160)
* Ispravljena navigacija po tablici u pregledu razgovora u Mozilla Thunderbirdu. (#8396)
* U Mozilla Firefoxu i Google Chromeu, prebacivanje sada radi za većinu popisa i prikaza stabla (kada popis ili drvo nije fokusirajuće ali elementi istih jesu) . (#3573, #9157)
* Način pregleda sada je podrazumijevano uključen pri čitanju poruka u Outlooku 2016/365 kada se koristi Automatska podrška za UIA u Microsoft word dokumentima. (#9188)
* NVDA sada će se rijetko zamrzavati na način koji podrazumijeva samo odjavu iz vaše korisničke sesije. (#6291)
* U Windowsima 10 nadogradnji za listopad 2018 i novijim, prilikom otvaranja oblačnog međuspremnika sa praznim međuspremnikom, NVDA će izgovoriti stanje međuspremnika. (#9103)
* U Windowsima 10 nadogranji za listopad i novijim, prilikom traženja emoji u panelu za emoji, NVDA će izgovarati prvi rezultat pretrage. (#9105)
* NVDA se više ne smrzava u glavnom prozoru Oracle VirtualBox 5.2 i novijima. (#9202)
* Ispravljene performanse u Microsoft excelu  pri kretanju po ćelijama. Podsjetnik: poslje pokretanja Microsoft Worda u dokumentu, isti postavite na izgled predloška. (#9217) 
* U mozilla Firefoxu i Google chromeu, prazne obavjesti se više ne čitaju. (#5657)
* Značajna ubrzanja pri kretanju po ćelijama u Microsoft excelu, osobito u radnim knjigama koje sadrže komentare ili validacijske popise. (#7348)
* Više ne bi smjelo biti potreno isključivati opciju unutarćelijskog uređivanja u opcijama Mocrosoft officea 2016/365, ako se želi uređivati pojedinačna ćelija. (#8146).
* ispravljeno zamrzavanje u Firefoxu ponekad viđeno pri navigaciji po orjentirima, ako se koristi dodatak Enhanced aria. (#8980)

## 2018.4.1

Ova inačica NVDA ispravlja rušenje pri pokretanju, kada je jezik NVDA postavljen na aragonski. (#9089)

## 2018.4

Novosti u ovoj inačici uključuju poboljšanja performansi u zadnjim inačicama Mozilla firefox-a, izgovor emoji sa svim govornim jedinicama, čitanje statusa poruke (prosljeđeno/odgovoreno), u Outlook-u, čitanje udaljenosti od ruba stranice od pokazivača u Microsoft Wordu, te puno ispravaka grešaka.

### Nove značajke

* Nove brajične tablice: Kineski (Kina, Mandarinski) s tonovima i bez tonova. (#5553)
* U popisu poruka, sada se izgovara status poruke odgovoren/proslijeđen. (#6911)
* NVDA sada može čitati opise znakova poput emoji, kao i druge znakove koji su dio općeg Unicode repozitorija znakova. (#6523)
* U Microsoft Wordu, udaljenost kursora od lijevog i gornjeg ruba stranice može se čitati uz pomoć tipkovničkog prečaca insert+delete. (#1939)
* U Google Sheets sa uključenim brajičnim načinom, NVDA više ne izgovara 'označeno' na svakoj ćeliji prilikom pomicanja fokusa. (#8879)
* Dodana podrška za Foxit Reader i Foxit Phantom PDF (#8944)
* Dodana podrška za DBeaver alat za baze podataka. (#8905)

### Izmjene

* Opcija "izvijesti o pomoćnim balončićima" u dijaloškom okviru prezentacija objekta preimenovana je "izgovaraj obavijesti" kako bi uključivala obavijesti u windowsima 8 i novijim. (#5789)
* U NVDA postavkama tipkovnice, potvrdni okviri za izbor NVDA modifikacijskih tipki sada su prikazani u jednom popisu umjesto odvojenog prikaza.
* NVDA više neće prikazivati izlišne informacije pri prikazivanju sata u nekim inačicama Windowsa. (#4364)
* Nadograđen liblouis brajični prevoditelj na inačicu 3.7.0. (#8697)
* Nadograđen eSpeak-NG na commit 919f3240cbb

### Ispravke grešaka

* U Outlooku 2016/365, kategorija i status zastavice sada se izgovaraju za poruke. (#8603)
* Kada je NVDA postavljen na jezike kao što su to  Kirgizijski, Mongolski ili Makedonski, više se ne pojavljuje upozorenje o nepodržanosti jezika od strane operativnog sustava. (#8064)
* Pomičući miš, sada će se isti pomicati točnije u poziciju načina fokusa u Mozilla Firefoxu, Google Chromeu i Acrobat Reader DC. (#6460)
* Interakcija sa odabirnim okvirima na web stranicama u  Firefoxu, Chromeu i Internet Exploreru je poboljšana. (#8664)
* Ako se NVDA pokreće na Japanskoj inačici Windowsa XP ili Viste, upozorenje o nekompatibilnosti sada se prikazuje kako valja. (#8771)
* Povećanje performansi u Mozilla Firefoxu prilikom kretanja po velikim web stranicama sa puno dinamičkog sadržaja. (#8678)
* Karakteristike fonta se više ne pokazuju na brajičnom retku,  ako su iste onemogućene u postavkama oblikovanja dokumenta. (#7615)
* NVDA sada uspjeva pratiti fokus u upravitelju datoteka i drugim aplikacijama koje koriste UI Automation prilikom zauzetosti aplikacije (kao što je to simultana obrada zvuka). (#7345)
* U ARIA izbornicima na webu, tipka escape će biti proslijeđena izborniku kao kontroli i neće više isključivati način fokusa. (#3215)
* U novom Gmailu, kada se koriste tipke brze navigacije u porukama prilikom čitanja, čitavo tijepo poruke više se ne čita poslije elementa do kojeg ste došli. (#8887)
* Poslije nadogradnje NVDA, Preglednici poput Firefoxa i google Chromea više se ne bi trebali rušiti, i način pregleda će ponovo prikazivati osvježavanja u svakom trenutno učitanom dokumentu. (#7641) 
* Prilikom kretanja po klikabilnom sadržaju u načinu pregleda, NVDA više ne čita "klikajući", više puta u jednom retku. (#7430)
* Komande koje su pritisnute na baum Vario 40 brajičnim retcima sada će se normalno izvoditi. (#8894)
* U Google Prezentacijama kada se koristi Mozilla Firefox, NVDA više ne izgovara označeni tekst pri pomicanju na svaku kontrolu fokusa. (#8964)

## 2018.3.2

Ovo je mala ispravka, koja ispravlja rušenje u Google Chromeu pri kretanju po tweetovima na [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Ovo je ispravka pogreške, koja je prouzrokovala rušenje NVDA, pri pokrenutom pregledniku Mozilla firefox u 32 bitnoj inačici. (#8759)

## 2018.3

Novosti u ovoj inačici uključuju automatsko otkrivanje nekoliko brajičnih redaka, podrška za nove značajke u Windowsima 10, uključujući emoji panel, te mnogo drugih ispravaka grešaka.

### Nove značajke

* NVDA će izvještavati o pravopisnim pogreškama, kada je to točno određeno u Mozilla Firefoxu i Google Chromeu. (#8280)
* Sadržaj koji je označen kao umetnut ili izbrisan na web stranicama sada se čita u Google Chromeu. (#8558)
* Dodana podrška za BrailleNote QT i Apex BT navigacijski kotačić kada se BrailleNote koristi kao brajični redak sa NVDA. (#5992, #5993)
* Dodann prečac za čitanjepreostalog i cjelokupnog vremena trenutne pjesme u Foobar2000. (#6596)
* Simbol Mac komandne tipke (⌘) sada se čita sa bilo kojim sintetizatorom govora prilikom čitanja teksta. (#8366)
* Prilagođene uloge preko aria-roledescription atributa sada su podržane u svim web preglednicima. (#8448)
* Nove brajične tablice: Češki osmotočkasta brajica, Centralni Kurdski, Esperanto, Mađarski, Švedski osmotočkasta kompjutorska brajica. (#8226, #8437)
* Dodana podrška za automatsko otkrivanje brajičnih redaka u pozadini. (#1271)
 * ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille i HumanWare BrailleNote i Brailliant BI/B brajični retci su trenutno podržani.
 * Ovu značajku možete uključiti ako da označite opciju automatski u spisku brajičnih redaka u NVDA dijaloškom okviru za odabir brajičnih redaka.
 * Za više informacija, molimo pročitajte korisnički priručnik.
* Dodana podrška za moderne značajke unosa u posljednjim inačicama Windows 10. Iste uključuju emoji panel (zimska nadogradnja za tvorce), diktiranje (zimska nadogradnja za tvorce), prijedlozi unosa na hardverskoj tipkovnici (nadogradnja za travanj 2018), i lijepljenje u oblačnom međuspremniku (nadogradnja za listopad 2018). (#7273)
* Sadržaj označen kao citat koristeći (role blockquote) sada je podržan u Mozilla Firefox 63. (#8577)

### Izmjene

* Spisak dostupnih jezika u NVDA općim postavkama, sada je sortiran po imenima jezika umjesto po iso639 kodovima. (#7284)
* Dodane podrazumijevane geste za Alt+Shift+Tab i Windows+Tab za sve podržane Freedom Scientific brajične redke. (#7387)
* Za ALVA BC680 i pretvornik protokola brajične redke, sada je moguće dodijeliti razne funkcije za lijevi i desni pametni pad, palčane te etouch tipke. (#8230)
* Za ALVA BC6 retke, kombinacija tipaka sp2+sp3 sada će izgovarati trenutni datum i vrijeme, gdje će sp1+sp2 oponašati windows tipku. (#8230)
* Korisnik će biti pitan, jednom kada se NVDA pokrene želi li slati povratne informacije u NV Access prilikom provjere NVDA nadogradnje. (#8217)
* Prilikom provjere nadogradnje, ako je korisnik pristao na slanje statistika u NV Access, NVDA će slati naziv trenutnog brajičnog retka i govorne jedinice, kako bi sam korisnik pomogao u razvoju tih komponenti. (#8217)
* Nadograđen liblouis brajični prevoditelj na inačicu 3.6.0. (#8365)
* Osvježen put do točne ruske osmotočkaste brajične tablice. (#8446)
* Nadograđen eSpeak-ng na 1.49.3dev commit 910f4c2. (#8561)

### Ispravke grešaka

* Dostupne oznake u Google Chromeu sada se isčitavaju u načinu pregleda, kada oznaka se ne pojavljuje kao sadržaj. (#4773)
* Obavijesti su podržane u Zoomu. Na primjer, to uključuje status utišavanja ili ottišavanja zvuka, te izgovaranje pristiglih poruka. (#7754)
* Prebacivanje brajične prezentacije konteksta kada se nalazi u načinu pregleda više ne prouzrokuje prekid izlaza u istom sa pozicije praćenja kursora. (#7741)
* ALVA BC680 brajični redci više ne neuspjevaju se inicijalizirati. (#8106)
* Podrazumijevano, ALVA BC6 brajični redci više ne pokreću tipke na emuliranoj sustavskoj tipkovnici  prilikom pritiska kombinacija koje uključuju sp2+sp3 kako bi se mogle pozivati unutrašnje funkcije. (#8230)
* pritisak sp2 na ALVA BC6 redku kako bi se emulirala tipka alt sada radi kako je i napisano. (#8360)
* NVDA više ne izgovara nepotrebne izmjene tipkovnice. (#7383, #8419)
* Praćenje miša sada je točnije u Notepadu i drugim poljima za uređivanje kada se nalazite u dokumentu koji sadrži više od 65535 znakova. (#8397)
* NVDA će prepoznavati više dijaloških okvira u Windowsima 10 i drugim modernim aplikacijama. (#8405)
* U Windowsima 10 nadogradnji za listopad 2018 te Server 2019 i novijim, NVDA više ne ne uspjeva pratiti fokus sustava kada se program zamrzne ili zablokira sustav sa događajima. (#7345, #8535)
* Korisnik je sada informiran porukom o nemogučnosti kopiranja prazne statusne trake. (#7789)
* Ispravljena pogreška u kojoj stanje "nije označeno" na kontrolama nije izgovoreno govorom ako je ista bila polovično odabrana. (#6946)
* U popisu jezika u NVDA općim postavkama, naziv jezika za burmeški sada se ispravno prikazuje u Windowsima 7. (#8544)
* U Microsoft Edgeu, NVDA će izgovarati obavijesti poput čidostupnog pregleda čitanja te stanja učitavanja stranice. (#8423)
* Pri navigaciji lista na stranici, NVDA će izgovoriti oznaku ako je autor dao istu. (#7652)
* Prilikom pridjeljivanja gesti funkcijama na određenom brajičnom redku, sada se prikazuju kao geste pridjeljene tom brajičnom redku. U prijašnjem stanju, iste su se pokazivale kao geste koje su bile pripisane aktivnom brajičnom redku. (#8108)
* 64-bitna inačica Media Player Classic sada je podržana. (#6066)
* Nekoliko poboljšanja u brajičnoj podršci za Microsoft Word sa uključenim UI Automation:
 * Slično kao u drugim tekstualnim poljima sa više redaka, kada ste pozicionirani na početku dokumenta pomiću brajice, Prvi je znak pozicioniran tako da se nalazi na početku samog brajičnog retka. (#8406)
 * Smanjena prevelika govorna prezentacija fokusa pri otvaranju Wordovih dokumenata. (#8407)
 * Routing tipke sadda ponovno rade u Word dokumentima kada se nalazite u spisku nabrajanja. (#7971)
 * Novoumetnute točkice ili brojevi sada se točno izgovaraju ili prenose u brajicu. (#7970)
* U Windowsima 10 1803 i novijim, sada je moguće instalirati dodatke, ako je značajka "koristi unicode UTF'8 za međunarodnu jezičnu podršku" uključena. (#8599)

## 2018.2

Novosti u ovoj inačici uključuju Podršku tablica u Kindle za osobna računala, podršku za Humanware Braillenote touch i BI14 Braille brajične retke, unapređenja za OneCore, kao i za sapi5 govorne jedinice, unapređenja u outlooku, i još puno toga.

### Nove značajke

* Širina redka i dužina stupca sada se mogu isčitati uz pomić govora i brajice. (#2642)
* NVDA prečaci za navigaciju u tablicama sada su podržani u  Google Dokumentima (sa uključenim brajičnim načinom). (#7946)
* Mogućnost navigacije po tablicama u Kindleu za osobna računala. (#7977)
* Podrška za BrailleNote touch i Brailliant BI 14 brajične retke preko USB i bluetooth veze. (#6524)
* U Windows 10 zimskoj nadogradnji za tvorce i novijim, NVDA može izgovarati obavijesti iz aplikacija kao što je to KalKulator i Windows Store. (#8045)
* Nove brajične tablice: litavska osmotočkasta, Ukrajinska, Mongolska sa podrškom engleskog kratkopisa. (#7839)
* Dodana skripta za izvještavanje o oblikovanju za tekst koji se nalazi ispod određene brajične ćelije. (#7106)
* Prilikom nadograđivanja NVDA, sada je moguće odgoditi instalaciju nadogradnje za kasnije vrijeme po vašem izboru. (#4263) 
* Novi jezici: Mongolski, Švicarski njemački.
* Sada možete uključivati ili isključivati control, shift, alt, windows i NVDA tipke sa vaše brajične tipkovnice te ih je moguće kombinirati uz brajični ulaz (e.g. press control+s). (#7306) 
 * Možete dodijeliti te modifikatore  koje možete pronaći u kategoriji emulirane tipke sustava u dijaloškom okviru ulazne geste.
* Vraćena podrška za Handy Tech Braillino i Modular brajične retke (sa starim firmwareom). (#8016)
* Datum i vrijeme za podržane Handy Techove uređaje (poput Active Braille i Active Star) će biti automatski sinkronizirano kada nije sinkronizirano više od 5 sekundi. (#8016)
* Sada se može pridijeliti gesta, koja služi za privremeno omogućavanje svih konfiguracijskih profila. (#4935)

### Izmjene

* Stupac statusa je promijenjen tako da će pokazivati je li dodatak omogućen ili onemogućen puno bolje od prijašnjeg obavještenja pokrenut ili suspendiran. (#7929)
* Nadograđen liblouis brajični prevoditelj na inačicu 3.5.0. (#7839)
* Preimenovana je Litavska brajična tablica te sada se zove litavska šestotočkasta, kako bi se izbjegla zbrka sa litavskom osmotočkastom tablicom. (#7839)
* Kanadske francuske brajične tablice su sada uklonjene. Sada će se umjesto kanadskih tablica, koristiti šestotočkasta, te unificirani francuski kratkopis. (#7839)
* Sekundarne routing tipke na Alva BC6, EuroBraille i Papenmeier brajičnim retcima sada izvještavaju o formatiranju teksta pritiskom na routing tipku nad brajičnom ćelijom. (#7106)
* Kratkopisne brajične ulazne tablice vratit će se u punopisni način u slučajevima, kada nije moguće uređivati tekst (npr. pri kontrolama gdje kursor ne postoji ili u načinu pregleda). (#7306)
* NVDA je sada manje pričljiv kada kalendarski termin pokriva cijeli dan. (#7949)
* Sve postavke NVDA sada se nalaze u jednom dijaloškom okviru postavke u istoimenom podizborniku, što znači da dijalozi više nisu raspršeni. (#7302)
* Podrazumijevani sintetizator govora sada je one core, bolje nego espeak. (#8176)

### ispravke grešaka

* NVDA sada uspijeva pročitati fokusirane kontrole u zaslonu za prijavu Microsoft naloga u postavkama poslije upisivanja e-mail adrese. (#7997)
* NVDA sada uspijeva pročitati stranicu kada se vraćate na prethodnu stranicu u  Microsoft Edge. (#7997)
* NVDA više neće pogrešno izgovarati zadnji znak windows 10 pina za prijavu kada se računalo otključava. (#7908)
* Oznake odabirnih okvira i izbornih gumba u Chromeu i Firefoxu više se ne izgovaraju dva put prilikom pritiska tipke tab ili pomicanjem sa strelicama. (#7960)
* Rukovanje aria-current sa vrijednošću false kao false umjesto true (#7892).
* Windows Onecore glasovi više se ne pokreću s greškom ako je prethodni glas bio uklonjem. (#7999)
* Izmjena glasova u Windows Onecore glasovima sada je puno brža. (#7999)
* Ispravljen izobličen brajični prikaz u nekim brajičnim tablicama, uključujući znakove za velika slova u danskom osmotočkastom kratkopisu. (#7526, #7693)
* NVDA sada može izgovarati više vrsta znakova za nabrajanje u Microsoft Wordu. (#6778)
* Pritiskom prečaca za izvještavanje formatiranja više ne premještava reviewPosition te također kada se pritisne više puta, ne nosi neželjene rezultate. (#7869)
* Brajični ulaz više ne dozvoljava korištenje kratkopisa u slučajevima u kojima isti nije podržan (NPR. cijele riječi neće biti poslane u sustav izvan tekstualnog sadržaja te u načinu pregleda). (#7306)
* Ispravljene nestabilnosti u povezivanju za Handy Tech Easy Braille i Braille Wave brajične retke. (#8016)
* U Windowsima 8 i novijim, NVDA više neće izgovarati "nepoznato" prilikom otvaranja izbornika brzog povezivanja )Windows+X) i označavanju stavaka iz tog izbornika. (#8137)
* Specifične geste za modele Na Himsovim retcima sada rade onako, kako su opisane u korisničkom priručniku. (#8096)
* NVDA će sada pokušati ispraviti greške povezane sa sistemskom COM registracijom koje su prouzrokovale da Internet explorer i firefox postanu nepristupačni, pri tom izgovarajući "nepoznato". (#2807)
* Ispravljena greška u upravitelju zadataka, koja je onemogućavala prikaz detaljnog prikaza zadataka. (#8147)
* Noviji Microsoft sapi5 glasovi više ne zaostaju na kraju izgovorene riječi, što ih čini brzim pri kretanju. (#8174)
* NVDA više niti ne izgovara, niti ne prikazuje (LTR i RTL znakove) prilikom pristupanja satu u windowsima 10. (#5729)
* Otkrivanje tipki za pomicanje na Hims Smart Beetle brajičnim retcima sada više nije nepouzdano. (#6086)
* U nekim tekstnim kontrolama, pogotovo u delphi aplikacijama, informacije koje su dane prilikom uređivanja ili kretanja sada su pouzdanije. (#636, #8102)
* U Windowsima 10 RS5, NVDA više ne izgovara suvišne informacije pri prebacivanju aplikacija uz pomoč alt+tab. (#8258)

## 2018.1.1

Ovo je specijalna stabilna inačica NVDA koja otklanja grešku u OneCore Windows sintetizatoru govora, koja je prouzrokovala da isto govori sa povišenim glasom i povišenom brzinom u Windows 10 Redstone 4 (1803). (#8082)  

## 2018.1

Novosti u ovoj inačici uključuju podršku grafova u Microsoft wordu i Powerpointu, novopodržani brajični retci: Eurobraille i Optelec protocol converter, unapređena podrška za Hims i Optelec brajične retke, poboljšanje performansi u Mozilla Firefox 58 i novijim, i puno više.

### Nove značajke

* Sada je moguće ulaziti u interakciju sa grafovima u Microsoft Wordu i Microsoft PowerPointu, slično kao i kod podrške grafova u Microsoft Excelu. (#7046)
 * U Microsoft Wordu:  kada se nalazite u načinu pregleda, kursorom dođite do grafa i pritisnite enter.
 * U Microsoft PowerPointu prilikom uređivanja slajda: pritišćite tabulator do objekta grafa, i pritisnite enter ili razmak kako biste ušli u interakciju s grafom.
 * Kako biste prestali biti u interakciji s grafom, Pritisnite escape.
* Novi jezik: kirgizki.
* Dodana podrška za VitalSource Bookshelf čitač elektronskih knjiga. (#7155)
* Dodana podrška za Optelec pretvarač protokola, Uređaj koji omogućava korištenje Alvinih Voyager i Satellite brajičnih redaka koristeći noviji ALVA BC6 protokol. (#6731)
* Sada je moguće koristiti brajični unos teksta sa brajičnim retkom ALVA 640 Comfort. (#7733) 
 * NVDA brajični unos može se koristiti sa istim brajičnim retcima, kao i sa  BC6 sa firmware-om 3.0.0 ili novijim.
* Rana podrška za Google Sheets sa uključenim brajičnim načinom. (#7935)
* Podrška za Eurobraille Esys, Esytime i Iris brajične retke. (#7488)

### Izmjene

* upravljački programi za HIMS Braille Sense/Braille EDGE/Smart Beetle i Hims Sync sada su zamijenjeni jednim upravljačkim programom. Ovaj upravljački program bit će automatski aktiviran za stare korisnike syncBraille upravljačkog programa. (#7459) 
 * Neke tipke, točnije tipke za premještanje po redovima su izmijenjene, kako bi pratile konvencije Himsovih proizvoda. Za više detalja, pročitajte vodič za korisnike.
* Prilikom tipkanja na zaslonskoj tipkovnici sa uključenom dodirnom interakcijom, podrazumjevano trebate svaku tipku stisnuti dva puta, kao što aktivirate i druge kontrole. (#7309)
 * Kako biste koristili postojeći način dodirnog unosa, gdje je jedan dodir dovoljan za aktivaciju pojedinačne tipke, omogućite tu opciju u dijaloškom okviru dodirna interakcija kojeg možete naći u izborniku postavke.
* Više nije potrebno ručno prebacivati brajicu na fokus ili pregled, jer će se to događati automatski. (#2385) 
 * imajte na umu, da će se prebacivanje na pregled događati samo kada se koristi pregledni kursor ili prečac objektne navigacije. pomicanje po redovima neće aktivirati ovakav način.

### Ispravke grešaka

* pregledne poruke poput izgovora formatiranja pri pritisku NVDA+f dva puta brzo više neće rezultirati pogreškom, kada je NVDA instaliran na sustavu sa nelatiničnim znakovima. (#7474)
* Fokus se sada vraća ispravno, prilikom vraćanja u Spotify iz drugih aplikacija. (#7689)
* U Windows 10 jesenskoj nadogradnji za tvorce, NVDA će se sada uspjevati nadograditi, kada je uključena opcija kontroliranog pristupa folderima u Windows defenderu. (#7696)
* otkrivanje tipaka za pomicanje napred ' nazad po redku kod hims brajičnih redaka sada više nije nestabilno. (#6086)
* Malo poboljšanje performansi prilikom učitavanja velikog sadržaja u Mozilla Firefox 58 i novijim. (#7719)
* U Microsoft Outlooku, čitanje e-mailova koji sadrže tablice, više ne prouzrokuje greške. (#6827)
* geste brajičnog redka koje emuliraju modifikatore tipki sustava mogu biti kombinirane sa drugim tipkama sustava ako jedna ili više uključenih gesti ovise o modelu. (#7783)
* U Mozilla Firefoxu, način pregleda sada ponovno radi u iskočnim prozorima dodataka poput LastPass i bitwarden. (#7809)
* NVDA se više ne smrzava na svakoj promijeni fokusa u mozilla firefox i chrome preglednicima poput smrzavanja ili rušenja. (#7818)
* U twitter klijentima poput Chicken Nuggeta, NVDA više neće ignorirati zadnjih 20 znakova od 280 znakovnog tweeta prilikom čitanja istog. (#7828)
* NVDA sada koristi ispravan jezik pri označavanju teksta. (#7687)
* U posljednjim inačicama Office 365, sada je moguće ponovo čitati excel grafove sa strelicama gore dole. (#7046)
-  Radi li se o brajičnom ili govornom izlazu, status i tip kontrole bit će predstavljen u istom poredku, neovisno je li pozitivan ili negativan. Ispravlja #7076
* u aplikacijama poput Windows 10 Pošte, NVDA će sada izgovarati izbrisane znakove pritiskom na backspace. (#7456)
* Sve tipke na Hims Braille Sense Polaris brajičnim retcima sada rade kako treba. (#7865)
* NVDA se sada uspješno pokreće na Windows 7 kada se prije pojavljivala greška o unutrašnjem api-ms dll, kada je u aplikaciji instalirana konkretna inačica Visual Studio 2017 redistributivnog paketa. (#7975)

## 2017.4

Novosti u ovoj inačici uključuju poboljšanja u web podršci, uključujući podrazumijevani način pregleda za web dijaloge bolje izgovaranje grupa polja u načinu pregleda, Podrška za nove Windows 10 tehnologije Windows 10 zaštitnik aplikacija i windows 10 za ARM64, te automatsko čitanje statusa baterije i orijentacije ekrana.  
Imajte na umu, da ova inačica NVDA ne podržava windows xp ili Windows Vistu. Minimalna podržana inačica operativnog sustava windows je windows 7 sa servisnim paketom 1.

### Nove značajke

* U načinu pregleda, sada je moguće preskakati orjentire koristeći prečac prebacivanja između sadrživaća (zarez/shift+zarez). (#5482)
* U Firefoxu, Chromeu i u Internet Exploreru, brza navigacija do uređivačkih polja i obrazaca sada uključuje tekstualna polja bogatog uređivanja (NPR. contentEditable). (#5534)
* U internet preglednicima, popis elemenata može izlistavati obrasce i gumbe. (#588)
* Prvobitna podrška za Windows 10 na ARM64 platformama. (#7508)
* Rana podrška za čitanje i kretanje po matematičkom sadržaju za Kindle knjige sa pristupačnom matematikom. (#7536)
* Dodana podrška za Azardi čitač elektronskih knjiga. (#5848)
* Prilikom ažuriranja dodataka, sada se izgovara i njihova inačica. (#5324)
* Dodani parametri naredbenog retka koji omogućuju stvaranje prijenosne inačice NVDA. (#6329)
* Podrška za Microsoft edge u windows zaštitniku aplikacija u Windows defenderu, koristeći windows 10 jesensko ažuriranje za tvorce. (#7600)
* Ako je pokrenut na prijenosnom ili tablet računalu, NVDA će sada izgovarati dali je punjač spojen ili odspojen, te promjenu položaja zaslona. (#4574, #4612)
* Novi jezik: Makedonski.
* Nove brajične tablice: Hrvatski puno pismo, Vijetnamski puno pismo. (#7518, #7565)
* Dodana podrška za Handy Tech Actilino brajični redak. (#7590)
* Sada je podržan unos znakova sa brajičnih tipkovnica Handytechovih brajičnih redaka. (#7590)

### Izmjene

* Minimalna podržana inačica operativnih sustava za NVDA sada je Windows 7 sa servisnim paketom 1, ili Windows Server 2008 R2 sa servisnim paketom 1. (#7546)
* Web dijaloški okviri u Firefox i Chrome web preglednicima sada automatski koriste način pregleda, osim ako to nije web aplikacija. (#4493)
* U načinu pregleda, pritiskanje tabulatora i kretanje prečicama za brzo kretanje ne izgovaraju prebacivanje izvan sadrživaća poput popisa i tablica, što čini kretanje bržim. (#2591)
* U načinu pregleda za Firefox i Chrome, Imena grupa polja obrazaca prilikom premještanja po njima sa prečicama za brzo kretanje ili prilikom pritiskanja taba. (#3321)
* U načinu pregleda, prečac za brzo kretanje po ugrađenim objektima (o i shift+o) sada uključuje audio i video playere, kao i elemente s aria atributima application i dialog. (#7239)
* Espeak-ng je nadograđen na inačicu 1.49.2, koja rješava probleme sa kompiliranjem novih verzija. (#7385, #7583)
* prilikom treće aktivacije prečaca 'čitaj statusnu traku', sadržaj izgovoren putem te komande je kopiran u međuspremnik. (#1785)
* Prilikom dodjele prečaca na Baumovom brajičnom redku, sada je moguče ograničiti iste za model na kojem se koriste (npr. VarioUltra ili Pronto). (#7517)
* tipkovni prečac u popisu elemenata u načinu pregleda promijenjen je sa  alt+f na kombinaciju alt+e. Bilješka prevoditelja: ovo ne važi za hrvatsku inačicu NVDA. (#7569)
* Dodana je nedodijeljena gesta koja omogućuje uključivanje / isključivanje tablica izgleda u letu. Ovu komandu možete pronaći u kategoriji način pregleda u dijaloškom okviru ulazne geste. (#7634)
* Nadograđen Liblouis brajični prevoditelj na inačicu 3.3.0. (#7565)
* Tipkovnički prečac za izborni gumb pravilni izrazi u dijaloškom okviru govorni rječnici je zamjenjen sa alt+r na alt+e. Bilješka prevoditelja: ovo ne vrijedi za hrvatsku inačicu čitača zaslona NVDA. (#6782)
* Datoteke glasovnih rječnika su sada verzijonirani i premještene su u mapu 'speechDicts/voiceDicts.v1'. (#7592)
* verzijonirane datoteke (user configuration, voice dictionaries) izmjene nisu spremljene u pokretaču. (#7688)
* Braillino, Bookworm i Modular Handy tech brajični retci (sa starim pogonskim softverom) više nisu podržani direktno. Koristite Handytechov univerzalni pogonski softver i NVDA dodatak kako biste mogli koristiti ove brajične retke s NVDA. (#7590)

### Ispravke grešaka

* Linkovi se sada ispravno prikazuju u aplikacijama poput Microsoft Worda. (#6780)
* NVDA više ne postaje značajno sporiji prilikom otvaranja više kartica u Firefox ili Chrome web preglednicima. (#3138)
* Routing tipka na MDV Lilli brajičnom retku više se ne pomiće neispravno za jednu brajičnu ćeliju u naprijed od one, na kojoj bi kursor trebao stajati. (#7469)
* U Internet Exploreru i drugim MSHTML dokumentima, HTML5 required atribut sada je podržan kako bi slao povratnu informaciju da je polje za upis obvezno. (#7321)
* Brajični retci se sada osvježuju prilikom upisivanja arapskih znakova u lijevo poravnatom WordPad dokumentu (#511).
* Pristupačne oznake za kontrole u Mozilla Firefoxu sada su više izgovarane u načinu pregleda kada oznaka nije prikazana kao sadržaj. (#4773)
* U windows 10 nadogradnji za tvorce, NVDA može ponovno pristupiti Firefoxu poslije ponovnog pokretanja NVDA. (#7269)
* Prilikom ponovnog pokretanja NVDA sa Mozilla Firefox u fokusu, način pregleda će ponovno biti dostupan, međutim, trebalo bi pritisnuti alt tab, da se prebaci na drugu aplikaciju, te ponovno da se vratimo na Firefox. (#5758)
* Sada je moguć pristup matematičkom Sadržaju u Google Chromeu na sustavu bez instaliranog Mozilla Firefox web preglednika. (#7308)
* Operacijski sustav i druge aplikacije trebale bi biti stabilnije neposredno poslije instalacije NVDA prije ponovnog pokretanja, usporedno sa prijašnjim inačicama NVDA čitača zaslona. (#7563)
* Prilikom korištenja prečaca za prepoznavanje sadržaja (npr. NVDA+r), ako objekt navigatora nestane, NVDA izgovara poruku o pogrešci umjesto nikakve poruke. (#7567)
* Popravljeno klizanje unatrag za  freedom Scientific brajične retke kiji imaju lijevi bumper bar. (#7713)

## 2017.3

Novosti u ovoj inačici uključuju unos brajevog kratkopisa, podrška za nove Windows OneCore glasove dostupne u Windowsima 10, ugrađenu podršku za Windows 10 OCR, i puno značajnih poboljšanja koje se tiču brajice i weba.

### Nove značajke

* Dodana je postavka u brajičnim postavkama za "vječno prikazivanje poruka". (#6669)
* U Microsoft Outlook popisu poruka, NVDA sada izgovara ako poruka ima zastavicu. (#6374)
* U Microsoft Powerpointu, sada se izgovara točan tip oblika prilikom uređivanja slajda (primjeri uključuju: trokut, krug, video, strelica), bolje nego samo 'oblik'. (#7111)
* Matematički sadržaj (dostupan kao MathML) sada je podržan u Google Chromeu. (#7184)
* NVDA sada može govoriti uz pomoć Windows OneCore glasova (znanih kao mobile glasovi), koji su uključeni u Windowse 10. Pristupate im označavanjem opcije Windows OneCore glasovi u NVDA dijaloškom okviru Govorna jedinica. (#6159)
* NVDA konfiguracijske datoteke sada mogu biti pospremljene korisničkoj mapi application data. To se uključuje u registru. Za više detalja, pogledajte poglavlje 'sistemski parametri' u korisničkom priručniku. (#6812)
* U web preglednicima, NVDA izgovara vrijednosti sadrživača za polja (točnije, aria-placeholder sada je podržan). (#7004)
* U načinu pregleda u Microsoft Wordu, sada je moguće kretati se po pravopisnim pogreškama uz pomoć brze navigacije (w i shift+w) (#6942)
* Dodana podrška za kontrolu odabirnika datuma koja se može pronaći u Microsoft Outlookovom dijaloškom okviru za termine. (#7217)
* Trenutno označeni prijedlog sada se izgovara u Windows 10 pošti u poljima to/cc te u Windows 10 polju uređivanja u Postavkama. (#6241)
* Sada se reproducira zvučni signal, koji izvještava o prisutnosti prijedloga u većini polja za pretragu u Windowsima 10 (NPR. početni zaslon, pretraga u postavkama, polja to/CC u Windows 10 pošti). (#6241)
* NVDA sada automatski čita obavijesti u Skype for Business Desktop, kao kada netko hoće započeti razgovor s vama. (#7281)
* Automatski čita dolazne poruke prilikom Skype for Business razgovora. (#7286)
* Automatsko čitanje obavijesti u Microsoft Edgeu, poput početka preuzimanja.  (#7281)
* Sada možete pisati kratkopisom i punim pismom na brajičnoj tipkovnici vašeg brajevog redka. Pogledajte poglavlje brajični unos u korisničkom vodiču. (#2439)
* Sada možete upisivati Unicode brajične znakove na brajičnoj tipkovnici, označujući Unicode braille kao brajičnu tablicu. (#6449)
* Dodana podrška za SuperBraille brajični redak koji se koristi na Tajwanu. (#7352)
* Nove brajične tablice: danski osmotočkasta kompjutorska brajica, litavski, farsi 8 točkasta kompjutorska brajica, Farsi punno pismo, slovenski osmotočkasta brajica. (#6188, #6550, #6773, #7367)
* Unapređena brajična tablica za engleski (SAD) osmotočkastu kompjutersku brajicu, podrška za znakove nabrajanja, znak za euro i slova sa naglascima. (#6836)
* NVDA sada može koristiti funkcionalnost prepoznavanja teksta uključenu u  Windowse 10 kako bi se mogao prepoznavati tekst sa slika ili iz nepristupačnih aplikacija. (#7361)
 * Jezik može biti postavljen u novom dijalogu windows 10 OCR, koji se nalazi u postavkama, u NVDA izborniku.
 * Kako biste prepoznali tekst u trenutnom objektu navigatora, pritisnite NVDA+r.
 * Za više detalja, pogledajte poglavlje o prepoznavanju teksta u vodiču za korisnike.
* Sada možete izabrati koja će se kontekstna informacija prikazati  kada je objekt u fokusu koristeći novu opciju "prezentacija konteksta fokusa" u dijaloškom okviru brajične postavke. (#217)
 * Na primjer, opcije "popuni redak promjenama konteksta" i "samo kada se redak pomiće u nazad" mogu učiniti kretanje po izbornicima bržim, jer stavke neće mijenjati svoju poziciju na retku.
 * Pogledajte poglavlje o "prezentaciji konteksta fokusa", u korisničkom vodiču za više informacija.
* U Firefoxu i Chromeu, NVDA sada podržava kompleksne dinamičke mreže poput radnih listova u kojima samo neki sadržaj može biti učitan ili prikazan (točnije,  aria-rowcount, aria-colcount, aria-rowindex and aria-colindex atribute uvedene u ARIA 1.1). (#7410)

### Izmjene

* Nedodijeljena komanda (script_restart) je dodana kako bi NVDA mogao biti brzo pokrenut. (#6396)
* Izgled tipkovnice sada može biti odabran iz dijaloškog okvira dobrodošlice. (#6863)
* Puno je više kontrola i stanja skraćeno na brajičnom retku. Orjentiri su također skraćeni. Molimo pogledajte poglavlje "kratice za tipove i stanja kontrola te orjentire" za kompletan popis. (#7188, #3975)
* Espeak-ng je nadograđen na verziju 1.49.1 (#7280).
* Popisi ulaznih i izlaznih brajičnih tablica u dijaloškom okviru brajičnih postavki, sada su sortirani po abecednom redu. (#6113)
* Obnovljen liblouis brajični prevoditelj na verziju 3.2.0. (#6935)
* Podrazumjevana brajična tablica je sada unificirani engleski brajični kod puno pismo. (#6952)
* Podrazumjevano, NVDA prikazuje sada samo djelove kontekstne informacije koja se promjenila na brajičnom retku kada objekt je fokusiran. (#217)
 * Prije je prikazivana cjelovita kontekstna informacija, nezavisno jeste li istu vidjeli prije.
 * Možete vratiti staru postavku  mjenjajući "prezentaciju fokusa konteksta" u brajičnim postavkama kako bi  "uvjek popunjavala redak".
* Prečaci za tablice više nisu dostupni tablice izgleda u načinu pregleda osim ako izgovaranje istih nije uključeno. (#7382)
* U Firefoxu i Chromeu prečaci za brzo kretanje po tablicama sada preskaću skrivene ćelije tablica. (#6652, #5655)
* NVDA logo je nadograđen. NVDA logo je stilizirana mješavina slova NVDA na bijelom, na čvrstoj ljubičastoj podlozi. To osigurava prikaz na svim pozadinskim bojama, i koristi ljubičastu boju iz loga NV Accessa. (#7446)

== Ispravke grešaka ==
* Div elementi koji se uređivaju, u Chromeu kao njihova vrijednost, ne izgovara se njihova oznaka prilikom čitanja u načinu pregleda. (#7153)
* Prilikom pritiska tipke end u načinu pregleda u praznom dokumentu u Microsoft wordu, više ne prouzrokuje runtime pogrešku. (#7009)
* Način pregleda je sada ispravno podržan u Microsoft Edgeu gdje je dokumentu dodijeljen atribut dokumenta. (#6998)
* U načinu pregleda, može se označavati ili odznačavati do kraja retka uz pomoć shift+end čak i ako je znak ili redak na kraju. (#7157)
* Ako dijaloški okvir sadrži traku napredka, tekst dijaloškog okvira je ažuriran kada se traka napredka promijeni. to sada znači, da se preostalo vrijeme iz dijaloškog okvira preuzimanja nadogradnje može isčitati. (#6862)
* NVDA će sada izgovarati promjenu označenog za većinu Windows 10 odabirnih okvira kao što je to automatska reprodukcija u postavkama. (#6337).
* Više se ne izgovaraju nepotrebne informacije pri upisu susreta / termina u dijaloškim okvirima za stvaranje u Microsoft Outlooku. (#7216)
* Zvučni signali za vječne trake napredovanja u dijaloškim okvirima kao što su to provjere nadogradnje čuju se samo kada je izlaz postavljen na zvučne signale. (#6759)
* U Microsoft Excelu 2007 i 2003, ćelije se ponovno izgovaraju prilikom kretanja po radnom listu. (#8243)
* U Windowsima 10 nadogradnji za tvorce i novijim, način pregleda se automatski omogućuje pri čitanju pošte u Windows 10 Pošti. (#7289)
* Na većini brajičnih redaka sa brajičnom tipkovnicom, Točkica 7 briše zadnju brajičnu ćeliju ili znak, a točkica 8 pritišće enter. (#6054)
* U tekstu za uređivanje, prilikom premještanja kursora (npr. sa strelicama ili tipkom backspace), NVDAova izgovorena povratna informacija je sada točnija u većini slučajeva, točnije u Google chrome i terminalnim aplikacijama. (#6424)
* Sadržaj uređivača potpisa u Microsoft Outlooku 2016 sada se može čitati. (#7253)
* U Java Swing aplikacijama, NVDA više ne prouzrokuje rušenje pri navigaciji u tablicama. (#6992)
* U Windows 10 nadogradnji za tvorce, NVDA više neće čitati obavijesti više puta. (#7128)
* U izborniku start Windowsa 10, prilikom zatvaranja izbornika ne prouzrokuje da NVDA izgovara traženi tekst. (#7370)
* Kretanje po naslovima u Microsoft Edgeu sada je značajno brže. (#7343)
* U Microsoft Edgeu, u načinu pregleda ne preskaće velik dio web stranice, kao što je to slučaj sa Wordpress 2015 temom. (#7143)
* U Microsoft Edgeu, orjentiri su ispravno prevedeni na jezike, koji ne spadaju pod engleski. (#7328)
* Brajica sada ispravno prati tekst koji se označava, a prekoraćuje širinu redka. For example, if you select multiple lines with shift+downArrow, braille now shows the last line you selected. (#5770)
* U Firefoxu, NVDA više ne izgovara višestruko "sekcija" prilikom otvaranja detalja tweeta na twitter.com. (#5741)
* Podrška za prepoznavače sadržaja poput opisivača slika ili ocr sada se lako mogu implementirati koristeći paket contentRecog. (#7361)
* Paket Python json package sada je uključen u binarnim kompilacijama NVDA. (#3050)

## 2017.2

Novosti u ovoj inačici uključuju punu podršku stišavanja zvuka u Windows 10 nadogradnji za tvorce; ispravke za neke greške pri označavanju u načinu pregleda, uključujući probleme sa prečacom označi sve; značajna unaprjeđenja u podršci za Microsoft edge; i unaprjeđenja na webu kao što su to izvještavanja elemenata koji su označeni kao trenutni (koristeći aria-current).

### Nove značajke

* U Microsoft Excelu sada se mogu izgovarati granice ćelija koristeći `NVDA+f`. (#3044)
* Dodana podrška za aria-current attribute. (#6358)
* Automatsko prebacivanje jezika sada je podržano u Microsoft Edge-u. (#6852)
* Dodana podrška za Windows Kalkulator u Windows 10 Enterprise LTSB (Long-Term Servicing Branch) i Server. (#6914)
* Izvodeći prečicu "čitaj trenutni redak", tri puta brzo sriče redak fonetski. (#6893)
* Novi jezik: Burmanski /Mjanmarski.
* Unicode strelice gore i dolje, te znakovi za razlomke, sada se izgovaraju onako kako bi trebalo. (#3805)

### Izmjene

* Prilikom kretanja uz pomoć jednostavne navigacije u programima koji koriste UI Automation, ignoriraju se bezsadržajni sadržitelji, čineći tako kretanje lakšim. (#6948, #6950) 

### Ispravke grešaka

* Stavke izbornika na web stranicama (stavka izbornika potvrdni okvir i izborni gumbi) sada se mogu aktivirati kada se nalazite u načinu pregleda. (#6735)
* Izgovaranje imena radnog lista je prevedeno. (#6848)
* Pritisak tipke escape, kada je aktivan dijaloški okvir za potvrdu brisanja profila sada zatvara dijaloški okvir. (#6851)
* Ispravljena su neka rušenja u Mozilla Firefoxu i drugim Gecko aplikacijama gdje je uključena značajka višezadačnosti. (#6885)
* Izgovaranje pozadinskih boja u pregledu zaslona sada je točnije kada je tekst crtan sa transparentnom pozadinom. (#6467)
* Unapređena podrška za aria-describedby u Internet Exploreru 11, uključujući podršku u okvirima, te kada su omogućeni višestruki identifikatori. (#5784)
* U Windows 10 nadogradnji za tvorce, NVDA-ovo prigušivanje glasnoće ponovno radi kao i u prijašnjim inačicama NVDA, (TJ. utišavanje sa govorom i zvukom, uvijek utišaj, i bez utišavanja su sve dostupne). (#6933)
* NVDA više neće neuspjevati kretnje ili izgovor većine (UIA) kontrola tamo, gdje tipkovnički prečac nije definiran. (#6779)
* Više se ne dodavaju dva prazna razmaka u informaciji o tipkovničkom prečacu u većini (UIA) kontrola. (#6790)
* Većina kombinacija tipaka na HIMS brajičnim retcima (NPR. razmaknica+točkica4) ne neuspjevaju se izvoditi, tj. ponovno funkcioniraju. (#3157)
* Otklonjena greška, u kojoj je spajanje brajičnih redaka na nekim sustavima i jezicima bilo nemoguće. (#6845)
* Smanjena je šansa oštećenja konfiguracijske datoteke prilikom isključivanja Windowsa. Konfiguracija se zapisuje u privremenu datoteku, prije zamjene iste. (#3165)
* Prilikom pritiska prečaca "slovkaj trenutni redak", tri puta, kako bi se slovkao redak, koristi se ispravan jezik za slovkane znakove. (#6726)
* Kretanje po redku u Microsoft Edgeu sada je tri puta brže u Windows 10 Nadogradnji za tvorce. (#6994)
* NVDA više ne izgovara "Web Runtime grupiranje" kada se fokusiraju Microsoft Edge dokumenti u Windows 10 nadogradnji za tvorce. (#6948)
* Adobe Acrobat Reader se više ne ruši u većini PDF dokumenata, (točnije, dokumente, koji sadrže prazne atribute ActualText). (#7021, #7034)
* Sve postojeće inačice SecureCRT sada su podržane. (#6302)
* U načinu pregleda u Microsoft Edgeu, interaktivne tablice (ARIA grids) više se ne preskaću prilikom kretanja po tablicama pomoću prečaca t i shift+t. (#6977)
* U načinu pregleda, prilikom pritiska shift+home prilikom označavanja u naprijed sada odznačava početak redka kako je to očekivano. (#5746)
* U načinu pregleda, prečac "označi sve", (ctrl+a) više ne neuspjeva označiti cijeli tekst ako kursor nije na početku teksta. (#6909)
* Ispravljeni drugi manji rijetki problemi u načinu pregleda. (#7131)

## 2017.1

Novosti u ovoj inačici uključuju Izvještavanje o poglavljima i tekstnim stupcima u Microsoft wordu; podrška za čitanje, kretanje i označavanje knjiga u Kindlu za osobna računala; i unaprjeđena podrška za microsoft edge.

### Nove značajke

* U Microsoft Wordu, vrsta prijeloma poglavlja i brojeva istih sada se izgovara. ovo je omogućeno uz pomoć opcije "izvijesti o brojevima stranica" u dijaloškom okviru oblikovanje dokumenata. (#5946)
* U Microsoft Wordu, tekstni stupci sada se izgovaraju. Ovo je omogućeno uz pomoć opcije "izvijesti o brojevima stranica" u postavkama oblikovanja dokumenata. (#5946)
* Automatsko prebacivanje jezika sada je podržano u  WordPadu. (#6555)
* Prečac za pretragu (NVDA+control+f) sada je podržan u načinu pregleda u Microsoft Edgeu. (#6580)
* Brzo kretanje po gumbima u načinu pregleda (b i shift+b) sada je podržana u Microsoft Edgeu. (#6577)
* Prilikom kopiranja radnog lista u Microsoft Excelu, zaglavlja redaka i stupaca su zapamćena. (#6628)
* Podrška za čitanje i kretanje po knjigama u  Kindlu za osobna računala inačica 1.19, uključujući pristup linkovima, fusnotama, slikama, označenom tekstu i korisničkim bilješkama. Please see the Kindle for PC section of the NVDA User Guide for further information. (#6247, #6638)
* Kretanje po tablicama sada je moguće u  Microsoft Edgeu. (#6594)
* U Microsoft Excelu, prečac izgovori lokaciju preglednog kursora (desktop: NVDA+numDelete, laptop: NVDA+delete) sada izgovara ime radnog lista i poziciju u ćeliji. (#6613)
* Dodana opcija u dijaloški okvir izađi koja omogućuje ponovno pokretanje sa uključenom dijagnostikom. (#6689)

### Izmjene

* Minimalna brzina titranja kursora sada je 200 MS. Ako je ovo prije bilo postavljeno na manju vrijednost, ta vrijednost će se povećati na 200 MS. (#6470)
* U brajične postavke, Dodan je potvrdni okvir koji omogućuje - onemogućuje titranje kursora. Prije je to omogućavala vrijednost 0. (#6470)
* Nadograđen eSpeak NG (commit e095f008, 10 Veljače 2017). (#6717)
* Zbog izmjena u Windows 10 creators nadogradnji, opcija "uvijek stišavaj" više nije dostupna u NVDA glasovnim postavkama. Ali, još uvijek je dostupna u starijim inačicama Windowsa 10. (#6684)
* zbog promjena u   Windows 10 Creators nadogradnji, način "stišavanja zvuka prilikom proizvodnje zvuka i govora" više se ne može uvjeravati u punu stišanost zvuka prije nego što počne govoriti, niti ne može ostaviti audiokanal otvoren  poslije zaustavljanja naglog stišavanja glasnoće. Ove izmjene ne utjeću na starije inačice windows 10 operacijskog sustava. (#6684)

### Ispravke grešaka

* Ispravljeno smrzavanje prilikom kretanje po odlomcima u načinu pregleda. (#6368)
* Tablice koje su kopirane iz Microsoft excela u microsoft word, sada se ne tretiraju kao tablice izgleda i time više se ne ignoriraju. (#5927)
* Prilikom pokušaja pisanja u microsoft excelu u zaštićenom prikazu, NVDA sada takvu situaciju oglašava zvukom, što je bolje od izgovaranja znakova koji nisu upisani. (#6570)
* pritisak escape tipke u Microsoft Excelu Više ne prebacuje korisnika u način pregleda, osiim ako se korisnik izričito nije prebacio u isti sa NVDA+razmak i potom ušao u način fokusa sa enterom na polju obrasca. (#6569) 
* NVDA se više ne smrzava u Microsoft Excelovim gdje se cijeli redak ili stupac spajaju. (#6216)
* Izvještavanje o izrezanom, odnosno tekstu koji ne stane u cijeli redak /stupac sada je točnije u Microsoft Excelu. (#6472)
* NVDA sada izvještava o potvrdnim okvirima koji su samo za čitanje. (#6563)
* NVDA pokretač više neće prikazivati dijaloški okvir upozorenja kada ne može reproducirati zvuk logotipa zbog nedostupnosti audio uređaja. (#6289)
* Kontrole u Microsoft Excel ribbonu koje su nedostupne sada se izvještavaju kao takve. (#6430)
* NVDA više neće izgovarati "ploha" prilikom minimiziranja prozora. (#6671)
* Upisani znakovi sada se izgovaraju u aplikacijama univerzalne windowsowe platforme (UWP) (uključujući Microsoft Edge) u windows 10 Creator nadogradnji. (#6017)
* Praćenje miša sada radi na svim zaslonima na računalima koja imaju više monitora. (#6598)
* NVDA više ne postaje beskoristan poslije isključivanja windows media playera prilikom fokusiranja na kontrolu klizača. (#5467)

## 2016.4

Poboljšanja u ovoj inačici uključuju unaprjeđenu podršku za Microsoft edge; način pregleda u windows mail e-mail klijentu (windows 10); i značajna poboljšanja u NVDA dijaloškim okvirima.

### Nove značajke

* NVDA sada može izvještavati o poravnanju /uvlaci redka koristeći zvučne signale. Ovo se može konfigurirati koristeći "Izvještavanje o uvlačenju redka" odabirni okvir u NVDA's postavkama oblikovanja dokumenta. (#5906)
* Podrška za Orbit Reader 20 brajični redak. (#6007)
* Opcija koja omogućuje otvaranje preglednika govora pri pokretanju je dodana. Ovo se može uključiti pomoću odabirnog okvira u pregledniku govora. (#5050)
* Prilikom ponovnog otvaranja dijaloškog okvira preglednika govora, Sada će dimenzije biti vrećene. (#5050)
* Polja unakrsnih referenci u Microsoft Word sada se tretiraju poput linkova. One se izgovaraju kao linkovi i mogu se aktivirati. (#6102)
* Podrška za Baum SuperVario2, Baum Vario 340 i HumanWare Brailliant2 brajične retke. (#6116)
* Početna podrška za jubilarnu inačicu Microsoft Edgea. (#6271)
* Način pregleda se sada koristi prilikom čitanja poruka u windows 10 Mail aplikaciji. (#6271)
* Novi jezik: Litavski.

### Izmjene

* Nadograđen liblouis braille translator na inačicu 3.0.0. Ovo uključuje podršku za unificiranu englesku brajicu. (#6109, #4194, #6220, #6140)
* U upravitelju dodataka, gumbi "onemogući dodatak" i omogući dodatak sada imaju tipkovničke prečace (alt+o i alt+m ). (#6388)
* Razni vizualni konflikti su ispravljeni. (#6317, #5548, #6342, #6343, #6349)
* Dijaloški okvir oblikovanje dokumenta sada je prilagođen tako da se sadržaj istog može pomicati. (#6348)
* Prilagođen izgled dijaloškog okvira za izgovor simbola tako da se puna širina dijaloškog okvira koristi za popis simbola. (#6101)
* U načinu pregleda u web preglednicima, komande za polje uređivanja (e i shift+e) i formular (f and shift+f) sada se mogu koristiti kako biste se mogli premještati između uređivačkih polja samo za čitanje. (#4164)
* U postavkama oblikovanja dokumenta, "izvjesti o promjenama oblikovanja poslije kursora" preimenovano je u "izgovori izmjene oblikovanja poslije kursora", zato što ova opcija utjeće kako na govor, tako i na brajicu. (#6336)
* Prilagođen izgled NVDA dijaloškog okvira dobrodošlice. (#6350)
* NVDA dijaloški okviri sada imaju poravnane svoje gumbe "U redu" i "odustani" na desnoj strani  zaslona. (#6333)
* pokretne kontrole sada se koriste za uređivačka polja poput "postotka izmjene visine za velika slova" postavku u dijaloškom okviru glasovnih postavki. You can enter the desired value or use the up and down arrow keys to adjust the value. (#6099)

### Ispravke grešaka

* Ispravljena rijetka greška prilikom isključivanja NVDA kada je preglednik govora otvoren. (#5050)
* Grafički linkovi se sada prikazuju u načinu pregleda u Mozilla Firefoxu. (#6051)
+- Nalazeći se u dijaloškom okviru uređivača rječnika, prilikom pritiska na gumb enter sada se spremaju sve izmjene napravljene tokom uređivanja i zatvara dijaloški okvir. Prije, enter nije radio ništa. (#6206)
* Sada se prikazuju poruke na brajičnom retku prilikom izmjene načina unosa za azijske metode unosa (izvorni unos /alfanumerički, puni oblik/polovičan, itd.). (#5892, #5893)
* Prilikom onemogućavanja a potom ponovnog omogućavanja dodatka, status dodatka sada se ponovno vraća na onu vrijednost na koju je bio postavnjen prije. (#6299)
* Prilikom korištenja Microsoft Worda, brojevi stranica u zaglavjima sada se mogu čitati. (#6004)
* Miš se sada može koristiti za pomicanje fokusa između popisa znakova  i uređivačkih polja u dijaloškom okviru izgovora simbola. (#6312)
* Ispravljena greška koja onemogućuje prikazivanje popisa elemenata kada microsoft wordow dokument sadrži neispravnu hipervezu. (#5886)
* Bio on zatvoren sa alatne trake ili pomoću prečaca alt+f4, stanje odabirnog okvira preglednika govora u nvda izborniku će sada odražavati trenutnu vidljivost prozora. (#6340)
* Komanda za ponovno učitavanje dodataka više ne prouzrokuje probleme  za konfiguracijske profile koji se okidaju, nove dokumente u internetskom pregledniku i pregled zaslona. (#2892, #5380)
* U popisu jezika, u nvda dijaloškom okviru "opće postavke",, jezici poput Aragonskog sada se prikazuju ispravno  u Windowsima 10. (#6259)
* Tipke na tipkovnici koje su emulirane, (npr. gumbi na brajičnom retku koji oponašaju tipku tab) sada se prikazuju u podešenom NVDA jeziku u pomoći ri unosu i u dijaloškom okviru "Ulazne geste". Prije su iste bile prikazane samo na engleskom. (#6212)
* Promjena NVDA jezika (iz dijaloškog okvira za odabir jezika) više se ne primjenjuje sve dok se NVDA ponovno ne pokrene. (#4561)
* Više nije moguće ostavljanje polja za uzorak praznim u novom unosu govornog rječnika. (#6412)
* Ispravljena rijetka greška prilikom skeniranja serijskih priključaka na nekim sustavima koja je rezultirala u neiskoristivosti nekih brajičnih redaka. (#6462)
* U Microsoft Word-u, numerirane liste u ćelijama tablica sada se čitaju prilikom pomicanja po ćeliji. (#6446)
* Way IFrames (dokumenti ugrađeni unutar dokumenata) se sada izgovaraju što je učinilo preciznost između preglednika. IFrames sada se izgovaraju kao "okvir" u Firefox-u. (#6047)
* Sada je moguće dodjeljivati ulazne geste za komande na Handy Tech brajičnom retku u NVDA dijaloškom okviru "ulazne geste. (#6461)
* U Microsoft Excelu, pritisak entera ili numeričkog entera prilikom navigacije u tablici sada se korektno vrši navigacija na slijedeći redak. (#6500)
* iTunes više se ne smrzava prilikom korištenja internetskog preglednika za iTunes trgovinu, Apple glazbu, ITD. (#6502)
* ispravljenja rušenja u 64 bitnim Mozilla i Chrome-baziranim aplikacijama. (#6497)
* u Firefoxu sa uključenom višeprocesnošću, način pregleda i tekstualna polja za uređivanje sada funkcioniraju korektno. (#6380)

## 2016.3

Novosti u ovoj inačici uključuju mogučnost onemogučavanja pojedinačnih dodataka; podršku za polja obrazaca u Microsoft excelu; drastična poboljšanja u izvještavanju boja; popravke i unaprjeđenja pri korištenju nekih brajičnih redaka; a također popravci i unaprjeđenja u Microsoft wordu.

### nove značajke

* Način pregleda se sada može koristiti za čitanje PDF dokumenata u Microsoft edge. (#5740)
* Podcrtavanje i dvostruko podcrtavanje se sada izgovara ako je to moguće u Microsoft Wordu. (#5800)
* U Microsoft Wordu, naslov tablice se sada izgovara ako je isti omogućen. Ako postoji opis, istom se može pristupiti koristeći prečac "otvori dugi opis", (Insert+d) in browse mode. (#5943)
* U Microsoft Wordu, NVDA sada izgovara informaciju o poziciji prilikom premještanja između odlomaka (alt+shift+StrelicaDolje i alt+shift+StrelicaGore). (#5945)
* U Microsoft Wordu, proredi se sada izgovaraju preko nvda izprečaca za izvještavanje o oblikovanju, priliko mijenjanja istih uz pomoć raznih pračaca u microsoft wordu, i prilikom premještanja na tekst sa drukčijim proredom ako je uključena opcija izvjesti o proredima u nvda postavkama oblikovanja dokumenata. (#2961)
* U Internet Exploreru, HTML5 strukturni elementi se sada prepoznaju. (#5591)
* Izvještavanje o komentarima, (kao na primjer u Microsoft Wordu) sada se mogu onemogućiti pomoću potvrdnog okvira u nvda  dijaloškom okviru oblikovanje dokumenta. (#5108)
* Sada je moguće onemogućivanje pojedinačnih dodataka. (#3090)
* Dodatni tipkovnički prečaci su dodani za ALVA BC640/680 series brajeve retke. (#5206)
* Sada postoji prečac za premještanje brajičnog retka na trenutan fokus. Trenutno , ALVA BC640/680 series ima prečac pridjeljen toj komandi, ali on se može ručno pridijeliti ručno za druge brajične retke u dijaloškom okviru ulazne geste ako želite. (#5250)
* U Microsoft Excelu, sada možete se koristiti polja obrazaca. You move to form fields using the Elements List or single letter navigation in browse mode. (#4953)
* Sada možete pridijeliti prečac za jednostavan način kretanja koristeći dijaloški obkvir ulazne geste. (#6173)

### Izmjene

* NVDA sada izgovara boje koristeći osnovne dobro razumljive boje koje se sastoje od 9 varijacija boja i 3 sjene, sa svjetlim i tamnim varijacijama. Ovo je bolje od korištenja subjektivnih i malo razumljivih imena boja. (#6029)
* postojeća reakcija NVDA+F9 potom NVDA+F10 je izmjenjena kako bi se mogao označiti tekst na prvi pritisak na F10. kada je F10 pritisnut dva put tekst se kopira u međuspremnik. (#4636)
* Nadograđen eSpeakNG na inačicu Master 11b1a7b (22 lipnja 2016). (#6037)

### Ispravke grešaka

* U načinu pregleda u Microsoft Wordu, kopiranje u međuspremnik sada čuva oblikovanje teksta. (#5956)
* U Microsoft Wordu, nvda sada pravilno čita koristeći wordove prečace za kretanje po tablicama (alt+home, alt+end, alt+pageUp i alt+pageDown) i prečace za označavanje tablica (shift pritisnut sa prečacom za kretanje). (#5961)
* U Microsoft word dijaloškim okvirima, NVDA objektna navigacija je drastično poboljšana. (#6036)
* U nekim aplikacijama poput Visual Studio 2015, prečaci (npr control+c za kopiranje) sada se izgovaraju onako kako se to očekuje. (#6021)
* ispravljena rijetka greška prilikom skeniranja serijskih portova na nekim sustavima, što je činilo večinu brajičnih redaka neupotrebljivim. (#6015)
* Izgovaranje boja u microsoft wordu sada je točnije, jer se i teme u microsoft officeu uzimaju u obzir. (#5997)
* Način pregleda u  Microsoft Edgeu i podrška za prijedloge pretrage u start izborniku, su sada dostupne na Windows 10 verzijama izdanim poslije travnja 2016. (#5955)
* U Microsoft Wordu, automatsko čitanje zaglavlja tablica sada radi bolje pri radu sa spojenim ćelijama. (#5926)
* U Windows 10 aplikaciji "pošta", NVDA više nema problema sa čitanjem sadržaja poruka. (#5635) 
* kada je uključen izgovor tipkovničkih prečaca, tipke poput caps locka, više se ne izgovaraju dva puta. (#5490)
* Dijaloški okviri kontrole korisničkog računa sada se ponovno ispravno čitaju U Windows 10 anniversary nadogradnji. (#5942)
* U Web Conference dodatku (koristi se na out-of-sight.net) NVDA više ne signalizira zvukom i govorom izmjene trake napredovanja koje se odnose na mikrofonski ulaz. (#5888)
* Izvodeći komandu traži prethodno ili traži slijedeće u načinu pregleda će sada ispravno pokretati pretragu osjetljivu na velika slova ako je izvorna pretraga osjetljiva na velika slova. (#5522)
* Prilikom uređivanja upisa u riječnik, sada ćete dobivati povratnu informaciju o nepravilnom regularnom izrazu. NVDA se više ne urušava, ako u datoteci postoji nepravilan regularni izraz. (#4834)
* Ako NVDA ne može komunicirati sa brajičnim retkom (npr. ako je odspojen), automatski će se onemogućiti korištenje istog. (#1555)
* znatno unapređene performanse u popisu elemenata u načinu pregleda u većini slučajeva. (#6126)
* U Microsoft Excelu, imena pozadinskih uzoraka, koje izgovara NVDA sada se poklapaju sa imenima koja se koriste u excelu. (#6092)
* Unaprjeđena podrška za Windows 10 zaslon prijave, uključujući obavještenja o upozorenjima i aktiviranja polja za lozinku uz pomoć dodira. (#6010)
* NVDA sada ispravno detektira sekundarne routing tipke na ALVA BC640/680 series brajičnim redcima. (#5206)
* NVDA može ponovno čitati windowsove obavijesti u posljednjim inačicama windows 10. (#6096)
* NVDA više slučajno ne zaustavlja pritiske tipaka na Baum kompatibilnim i HumanWare Brailliant B brajičnim redcima. (#6035)
* Ako je izgovaranje brojeva redaka uključeno u postavkama oblikovanja dokumenta, isti se sada prikazuju na brajičnom redku. (#5941)
* Kada je način govora isključen, izgovoreni objekti (poput pritiska NVDA+tab za izgovaranje fokusa) sada se pojavljuje u pregledniku govora, kako se to očekuje. (#6049)
* U Outlook 2016 popisu poruka,  pridružena informacija o predlošku više se ne izgovara. (#6219)
* U Google Chrome-u i web preglednicima baziranima na njemu, na jezicima drukćijima od engleskog, način pregleda više ne odbija poslušnost u većini dokumenata. (#6249)

## 2016.2.1

Ova inačica ispravlja rušenja u Microsoft wordu:

* NVDA više ne prouzrokuje rušenje microsoft worda poslije pokretanja istog. (#6033)
* Uklonjena mogućnost izgovaranja gramatičkih pogrešaka, zato što je to uzrok rušenja Microsoft worda.(#5954, #5877)

## 2016.2

Novosti u ovoj inačici uključuju mogučnost izvještavanja o pravopisnim pogreškama pri pisanju; podrška za izgovaranje gramatičkih pogrešaka u Microsoft Wordu; i unaprjeđenja  i ispravke u podršci za Microsoft office paket.

### Nove značajke

* U načinu pregleda u Internet Exploreru i drugim MSHTML kontrolama, koristeći brzu navigaciju za kretanje po anotacijama (a i shift+a) sada se koristi i za kretanje po umetnutom i izbrisanom tekstu. (#5691)
* U Microsoft Excelu, NVDA sada izgovara razinu grupe ćelija, kao i njihovu proširivost ili skupljivost. (#5690)
* Pritiskom prečaca za izgovor formatiranja teksta (NVDA+f) dva puta, prezentira informaciju u načinu pregleda kako bi se mogla pregledati. (#4908)
* U Microsoft Excelu 2010 i novijem, sjenćanje čelija i njihovo popunjavanje se izgovara. Automatsko izgovaranje možete uključiti u postavkama oblikovanja dokumenta. (#3683)
* Nova brajična tablica: Starogrčki. (#5393)
* u pregledniku zapisnika, sada možete pospremiti zapisnik koristeći prečac ctrl+s. (#4532)
* Ako je izgovor pravopisnih grešaka uključen i podržan u određenoj kontroli, NVDA će reproducirati zvuk kako bi vas upozorio na pravopisnu pogrešku koja je napravljena prilikom pisanja. to se može onemogućiti koristeći "reproduciraj zvuk pri pravopisnim pogreškama" opciju u nvda postavkama tipkovnice. (#2024)
* Gramatičke pogreške se sada izgovaraju u microsoft wordu.. Ovo se može onemogućiti uz pomoć nove opcije "izgovori gramatičke pogreške" u dijaloškom okviru za oblikovanje teksta. (#5877)

### Izmjene

* U načinu pregleda i poljima za uređivanje, NVDA tretira numerički Enter na isti način kao i enter na glavnom dijelu tipkovnice. (#5385)
* NVDA sada koristi eSpeak NG sintetizator govora. (#5651)
* U Microsoft Excelu, NVDA više ne ignorira zaglavlje stupca za ćeliju kada postoji prazan redak između ćelije i zaglavlja. (#5396)
* U Microsoft Excelu, koordinate se sada izgovaraju prije zaglavlja, kako bi se  spriječila višeznačnost zaglavlja i sadržaja. (#5396)

### Ispravke grešaka

* u načinu pregleda, prilikom pokušaja korištenja brzog kretanja kako bi ste se pomakli na element koji nije podržan u dokumentu, nvda izgovara da to nije podržano bolje nego izgovaranje pogrešne informacije o nepostojećem elementu u tom smjeru. (#5691)
* prilikom popisivanja radnih listova u popisu elemenata U Microsoft Excelu, radni listovi koji sadrže samo grafove sada su uključeni. (#5698)
* NVDA više ne izgovara nepotrebne informacije prilikom prebacivanja prozora u java aplikacijama koje imaju višesstruke prozore kao što su to IntelliJ ili Android Studio. (#5732)
* U scintilla'baziranim uređivaćima teksta kao što je to Notepad++, brajica se sada osvježava pravilno pri pomicanju kursora koristeći brajični redak. (#5678)
* NVDA se više ne ruši prilikom odabira brajičnog izlaza. (#4457)
* U Microsoft Wordu, Poravnanje odlomaka sada se izgovara u mjernoj jedinici koju odabire korisnik (NPR. centimetri ili inči). (#5804)
* Pri korištenju brajičnog redka, puno više NVDA poruka koje su se prije samo izgovarale, sada su također ispisane i na brajici. (#5557)
* U pristupačnim Java aplikacijama, razina stavaka stabla sada se izgovara. (#5766)
* Popravljena urušavanja pri korištenju adobe flash'a u nekim slučajevima, koristeći mozilla firefox. (#5367)
* U Google chromeu i chrome-baziranim preglednicima, dokumenti unutar dijaloga ili aplikacije sada se mogu čitati u načinu pregleda. (#5818)
* U Google chromeu i chrome baziranim preglednicima, sada možete prisiliti NVDA da se prebaci u način pregleda u dijaloškim okvirima web sučelja ili aplikacija. (#5818)
* U internet exploreru i drugim MSHTML kontrolama, pomičući fokus do pojedinih kontrola (specifično pri korištenju elementa aria-activedescendant) više se ne prebacuje pogrešno u način pregleda. Ovo se događalo, na primjer, prilikom pomicanja na prijedloge u adresnoj traci prilikom pisanja poruke u gmailu. (#5676)
* U Microsoft Wordu, NVDA se više ne smrzava u velikim tablicama kada je izgovaranje zaglavlja redaka i stupaca uključeno. (#5878)
* U Microsoft wordu, NVDA više ne izgovara pogrešno redak sa uvučenom razinom (ali ne ugrađeni stil razine) kao naslov. (#5186)
* U načinu pregleda u microsoft wordu, pomicanje sa kraja na početak sadrživača (zarez i šift+zarez) sada radi i u tablicama. (#5883)

## 2016.1

Najvažnije novosti u ovoj inačici uključuju mogućnost neobaveznog smanjivanja glasnoće drugih zvukova; unaprjeđenje brajičnog izlaza i podrške za brajične retke; nekoliko značajnih poboljšanja podrške za Microsoft office; i poboljšanja u načinu pregleda za Itunes.

### Nove značajke

* Nove brajične tablice: poljska kompjutorska brajica, mongolski. (#5537, #5574)
* Možete isključiti brajični pokazivač i izmjeniti njegov oblik koristeći novu opcije prikaži brajični pokazivač i promjeni izgled kursora u dijaloškom okviru brajične postavke. (#5198)
* NVDA se sada može povezati sa  HIMS Smart Beetle brajičnim retkom putem bluetooth veze. (#5607)
* podrška za HumanWare Brailliant BI/B brajične retke kada je protokol postavljen na OpenBraille. (#5612)

### Izmjene

* Sada je zadano isključeno izgovaranje isticanja. (#4920)
* u listi elemenata  u Microsoft excelu, prečac za formule promjenjen je na alt+r tako da je sada različit od prečaca od polja filter (ne važi za hrvatski prijevod). (#5527)
* nadograđen liblouis brajični prevoditelj na inačicu 2.6.5. (#5574)
* Riječ "text" više se ne izgovara kada se pomiće fokus ili ili pregledni kursor na tekstualne objekte. (#5452)

### ispravke grešaka

* U iTunes inačici 12, način pregleda se ispravno osvježava kada se nova stranica otvara u Itunes trgovini. (#5191)
* U Internet Exploreru i drugim MSHTML kontrolama, premještanje do specificirane razine naslova  sa jednoslovnom prečicom ponaša se kako je to očekivano kada je specificirana razina naslova za potrebe pristupačnosti (specifično, kada aria-level nadpisuje razinu h oznake). (#5434)
* U Spotifyju, fokus se više često ne premještava na "nepoznati" objekt. (#5439)
* Fokus je ispravno povraćen prilikom prebacivanja u drugu aplikaciju. (#5439)
* Prilikom prebacivanja iz načina formulara u način pregleda, izmjena načina se izgovara i istovremeno prikazuje na brajičnom retku. (#5239)
* Start gumb na traci zadataka više se ne izgovara kao popis  i/ili) ili kao označen u nekim inačicama sustava windows. (#5178)
* Poruke poput "umetnuto" više se ne izgovaraju prilikom sastavljanja poruka u Microsoft Outlooku. (#5486)
* Pri korištenju brajičnog retka kada je tekst označen na trenutnom retku (npr. prilikom traženja u uređivaću teksta za tekstom koji se pojavljuje u istom retku), brajični redak će se također pomaknuti ako je to potrebno. (#5410)
* NVDA se više ne gasi podmuklo prilikom zatvaranja windows komandne konzole uz pomoć alt+f4 u windowsima 10. (#5343)
* u popisu elemenata u načinu pregleda, prilikom izmjene vrste elementa, polje za filtriranje se sada automatski čisti. (#5511)
* u tekstu koji se može uređivati u Mozilla aplikacijama, pomicanje miša ponovno čita potrebni redak, riječ, itd. Kao što se i očekuje umjesto čitanja cijelog sadržaja. (#5535)
* prilikom pomicanja miša u poljima za uređivanje u mozilla aplikacijama, čitanje se ne zaustavlja na elementima poput linkova u riječi ili retku koji je čitan. (#2160, #5535)
* U internet exploreru, shoprite.com web stranica može se ponovo čitati u načinu pregleda umjesto izgovaranja praznih redova. (točnije, lang atributi se korektno interpretiraju).) (#5569)
* U Microsoft Wordu, lista promjena poput "umetnuto" više se ne izgovara ako oznaka izmjene nije prikazana. (#5566)
* kada je preklopni gumb pritisnut, nvda izgovara izmjenu istog od njegova pritiska do otpuštanja pritiska. (#5441)
* izgovor izgleda pokazivaća miša ponovno radi kako je očekivano. (#5595)
* kada se izgovara poravnanje teksta, nerazdjeljujući razmaci su sada tretirani kao normalni razmaci. Previously, this could cause announcements such as "space space space" instead  of "3 space". (#5610)
* NVDA sada može neobavezno smanjivati glasnoću drugih zvukova kada je instaliran na windowsima 8 i novijim. To može biti konfigurirano koristeći koristeći način manjivanja glasnoće u dijaloškom okviru govorna jedinica ili pritiskom  nvda+shift+d. (#3830, #5575)
* Prilikom zatvaranja moderne liste za upis istočnoazijskih znakova, fokus se vraća na sastavljanje unosa ili na određeni dokument. (#4145)
* U microsoft office 2013 i novijem, kada je ribbon prikazan tako da se prikazuju samo kartice, stavke u ribbonu se izgovaraju ponovno kako je to očekivano kada je kartica aktivirana. (#5504)
-Ispravke u otkrivanju gesti zaslona osjetljivog na dodir. (#5652)
* prelasci po ekranu osjetljivom na dodir više se ne izgovaraju u pomoći pri unosu. (#5652)
* Nvda više ne griješi prilikom izlistavanja komentara u listi elemenata za excel ako je komentar na spojenoj ćeliji. (#5704)
* U vrlo rijetkim slučajevima, nvda više ne neuspjeva čitati sadržaje ćelija u Excelu sa uključenom opcijom izgovaraj zaglavlja redaka i stupaca (#5705)
* U Google chrome, navigacija unutar sastava unosa za istočnoazijske znakove više ne završava greškom. (#4080)
* prilikom pretrage Apple music u iTunesu, način pregleda za rezultate pretrage se sada osvježava kako je to očekivano. (#5659)
* u Microsoft Excelu, pritisak kombinacije shift+f11 za kreiranje nove ćelije sada izgovara vašu novu poziciju umjesto da ne izgovori ništa. (#5689)
* Ispravljeni problemi sa brajičnim izlazom  prilikom upisivanja korejskih znakova.. (#5640)

## 2015.4

Novosti u ovoj inačici ukljućuju unaprjeđivanje performansi u windows 10; uključivanje u centar za olakšani pristup u windowsima 8 i novijim; unaprjeđenja za microsoft excel, ukljućujući popisivanje i preimenovanje radnih listova te pristup zaključanim ćelijama u zaštićenim radnim listovima; i podrška za uređivanje teksta u obogaćenog teksta u firefoxu, google chromeu i mozilli thunderbird.

### nove značajke

* NVDA se sada prikazuje u centru za olakšani pristup u windowsima8 i novijim. (#308)
* kada se krećete po ćelijama u excelu, izmjene oblikovanja se sada čitaju ako su odgovarajuće opcije ukljućene u dijaloškom okviru oblikovanje dokumenta. (#4878)
* Opcija izvijesti o isticanju je dodana u NVDA dijaloški okvir oblikovanje dokumenta. podrazumjevano ukljućena, omogućuje nvda  čitanje naglašenog teksta u dokumentima. To je podržano samo u internet exploreru. (#4920)
* Postojanje umetnutog ili izbrisanog teksta sada se izvještava u načinu pregleda za Internet explorer ako je nvda opcija izvijesti o revizijama urednika uključena. (#4920)
* Prilikom pregleda izmjena u nvda popisu elemenata za microsoft word, više informacija poput tog što je brisano ili označenois sada se prikazuje. (#4920)
* Microsoft Excel: popisivanje i preimenovanje radnih listova je moguće iz nvda popisa elemenata (NVDA+f7). (#4630, #4414)
* Sada je moguće podesiti hoće li se trenutni simbol slati govornoj jedinici (npr kako bi prouzročio pauzu - ili promijenio intonaciju) u dijaloškom okviru izgovor simbola. (#5234)
* u microsoft excelu, NVDA izvještava bilo koju ulaznu poruku postavljenu na radni list koju je postavio autor na ćeliju. (#5051)
* podrška za Baum Pronto! V4 i VarioUltra brajične retke preko bluetooth veze. (#3717)
* podrška za uređivanje obogaćenog teksta u mozilla aplikacijama kao što su google dokumenti sa ukljućenom brajičnom podrškom u mozila firefoxu i i html sastavljanju u mozilla thunderbirdu. (#1668)
* podrška za uređivanje obogaćenog teksta u google chrome i Chromepreglednicima baziranim na chromeu poput google docs sa ukljućenom brajičnom podrškom. (#2634)
 * to zahtjeva chrome inačicu 47 i noviju.
* U načinu pregleda u microsoft excelu, Možete se kretati po zakljućanim čelijama u zaštićenim radnim listovima. (#4952)

### Izmjene

* Opcija izvjesti o revizijama urednika u oblikovanju dokumenta sada je uključena zadano. (#4920)
* Premještajući se po znakovima u microsoft wordu sa uključenom opcijom izvjesti o izmjenama urednika, manje se informacija izgovara za izmjene, što olakšava navigaciju i čini je bržom. Kako biste pogledali dodatne informacije, koristite listu izmjena. (#4920)
* Nadograđen liblouis brajični prevoditelj na inačicu 2.6.4. (#5341)
* neki simboli ukljućujući osnovne matematičke simbole, ) premješteni su na razinu ponešto kako bi se zadano izgovarali. (#3799)
* Ako govorna jedinica to podržava, govor će biti zaustavljan za simbole zagrada i en dash (–). (#3799)
* Kada se označava tekst, tekst je čitan prije obavjesti označavanja umjesto poslije. (#1707)

### Ispravke grešaka

* Drastično unaprjeđenje performansi pri navigaciji Outlook 2010/2013 popisa sa porukama. (#5268)
* u grafu u microsoft excelu, kretanje uz pomoć nekih tipaka (poput promjena radnog lista uz pomoć kontrol+page up i kontrol+pageDown) sada ispravno funkcionira. (#5336)
* Ispravljen vizualni izgled  gumbi u dijaloškom okviru upozorenja koji se prikazuje kada želite pregaziti stariju inačicu nvda novijom i obratno. (#5325)
* U windowsima 8 i novijim, NVDA se pokreće puno ranije se kada se prijavljujete u windows. (#308)
* ako ste to omogućili u prijašnjoj inačici nvda, trebate to ponovo iskljućiti i ukljućiti kako bi promjena stupila na snagu. Ispratite slijedeće korake:
Otvorite dijaloški okvir opće postavke.
odznačite odabirni okvir pokreni nvda poslije prijave u windows.
Pritisnite gumb u redu.
Ponovno otvorite dijaloški okvir opće postavke.

1. Odaberite odabirni okvir pokreni nvda prilikom prijave u windows .
1. Pritisnite ok gumb.

* Unaprjeđenja performansi u ui automation uključujući eksplorer za datoteke i task manager. (#5293)
* nvda sada korektno čita kada se dolazi tabom do aria grid kontrola samo za čitanje u načinu pregleda za mozilla firefox i drugim gecko-baziranim kontrolama. (#5118)
* nvda sada korektno izvještava o  "nema prethodnog" umjesto "nema slijedećeg" kada ne postoji više objekata prilikom klizanja u lijevo na zaslonu osjetlijvom na dodir.
* ispravljen problem pri pisanju više rijeći u polju za filtriranje u  dijaloškom okviru ulaznih gesti. (#5426)
* NVDA se više ne smrzava u nekim slućajevima prilikom ponovnog spajanja na humanware BI/B series redak putem usb-a. (#5406)
* u jezicima sa dvojnim znakovima, opisi znakova rade kako treba za engleska velika slova. (#5375)
* nvda se više neće često smrzavati prilikom otvaranja windows 10 izbornika start. (#5417)
* U Skypeu za radnu površinu, obavijesti koje su prikazane prije prethodne obavijesti se sada čitaju. (#4841)
* sada se čitaju obavijesti u  Skypeu za radnu površinu 7.12 i novijim. (#5405)
* NVDA sada ispravno čita fokusiranu stavku prilikom napuštanja kontekstnog izbornika u nekim aplikacijama poput Jart. (#5302)
* U Windowsima 7 i novijim, boja se ponovo čita u većini aplikacija popud Wordpada. (#5352)
* Prilikom uređivanja u  Microsoft PowerPointu, pritiskom entera nvda sada izgovara automatski unešen tekst popud  točkice ili broja. (#5360)

## 2015.3

Novosti u ovoj inačici uključuju početnu podršku za windows 10 operacijski sustav; mogućnost onemogučavanja brzog kretanja u načinu pregleda (korisno za neke web aplikacije); unapređenja u internet exploreru; i popravke grešaka tzv. izmješanog teksta prilikom upisivanja znakova koristeći neke aplikacije sa uključenom brajicom.

### Nove Značajke

* Sada se izgovara postojanje pravopisnih pogrešaka u poljima za uređivanje u internet exploreru i drugim MSHTML kontrolama. (#4174)
* Kada se pojave u tekstu, puno više matematičkih simbola je sada izgovoreno. (#3805)
* Prijedlozi pretrage na početnom zaslonu windowsa 10, sada se izgovaraju (#5049)
* podrška za EcoBraille 20, EcoBraille 40, EcoBraille 80 i EcoBraille Plus brajične retke. (#4078)
* U načinu pregleda sada možete uključivati brzo kretanje pomoću navigacijskih tipki pritiskom kombinacije tipaka NVDA+shift+razmak. Kada je Ova opcija isključena, navigacijske tipke za brzo kretanje počinju se prosljeđivati drugoj aplikaciji /programu, što je korisno za neke web aplikacije poput gmaila, twittera i Facebooka. (#3203)
* Nove brajične tablice: Finski šestotočkasta brajica, irski puno pismo, irski kratkopis, korejsko puno pismo (2006), korejski kratkopis (2006). (#5137, #5074, #5097)
* Sada je podržana qwerty tipkovnica na  Papenmeier BRAILLEX Live Plus brajičnom retku. (#5181)
* Eksperimentalna podrška za Microsoft Edge web preglednik i pregledački mehanizam u Windowsima 10. (#5212)
* Novi jezik: Kanadaški.

### Izmjene

* Nadograđen LibLouis brajični prevoditelj na inačicu 2.6.3. (#5137)
* Prilikom pokušaja instalacije starije inačice NVDA od one koja je trenutno instalirana, sada ćete biti upozoreni da to nije preporučljivo, i da biste trebali ukloniti prethodnu inačicu NVDA prije nastavka instalacije starije inačice. (#5037)

### Ispravke Grešaka

* U načinu pregleda za  Internet Explorer i druge MSHTML kontrole, brza navigacija po poljima obrazaca više ne uključuje prezentacijske stavke popisa. (#4204)
* U firefoxu, NVDA više ne pokušava stvoriti opis za  ARIA tab panele bazirane na all text inside atributu. (#4638)
* U Internet Exploreru i drugim MSHTML kontrolama, tabiranjem u sekcijama, člancima ili dijalozima  više ne izgovara sadržaj nadređenog objekta kao njegovo ime. (#5021, #5025) 
* Pri korištenju Baum/HumanWare/APH brajičnih redaka sa brajičnom tipkovnicom, brajični unos znakova više neće prestati funkcionirati nakon pritiska neke druge tipke  na brajičnom retku. (#3541)
* U windowsima 10, više se ne izgovaraju nepotrebne informacije pri pritisku alt+tab i alt+shift+tab prilikom prebacivanja između aplikacija. (#5116)
* Upisani tekst više nije izmješan pri korištenju nekih aplikacija  poput Microsoft Outlook sa brajičnim retkom. (#2953)
* U načinu pregleda u Internet Exploreru i drugim MSHTML kontrolama, sada se izgovara trenutni sadržaj koji je fokusiran i odma je prebačen fokus. (#5040)
* U načinu pregleda u Microsoft Wordu, brza navigacija osvježava sadržaj na brajičnom retku i pregledni kursor kako je i očekivano. (#4968)
* Pri prikazu brajice, više se ne prikazuju nepotrebni razmaci /bjeline /prazni prostori prije ili poslije oznaka za kontrole i oblikovanje teksta. (#5043)
* Kada program reagira sporo, i kada se prebacujete sa tog programa, NVDA NVDA puno bolje reagira u drugim aplikacijama u većini slučajeva. (#3831)
* Sada se izgovaraju pozadinske obavijesti u windowsima 10. (#5136)
* Sada se izgovara vrijednost koja se mijenja  u nekim (UI Automation) odabirnim okvirima gdje to prije nije radilo.
* u načinu pregleda u internetskim preglednicima, pritiskanje taba se sada ponaša kako je to očekivano poslije tabanja do okvira dokumenta. (#5227)
* windows 10 zaslon zaključavanja može se zatvoriti koristeći zaslon osjetljiv na dodir. (#5220)
* U windowsima 7 i novijim, tekst više nije izmješan kada upisujete tekst u većini aplikacija poput Wordpada i Skypea sa brajičnim retkom. (#4291)
* Na windows 10 zaslonu zaključavanja, više nije moguće čitanje međuspremnika, pristup pokrenutim programima uz pomoć preglednog kursora, izmjena nvda konfiguracije, itd. (#5269)

## 2015.2

Nove značajke u ovoj inačici uključuju mogućnost čitanja grafova u microsoft excelu i podršku koja omogućuje čitanje matematičkog sadržaja.

### Nove značajke

* Sada je moguće pomicanje po rečenicama koristeći tipkovničke prečace alt+strelicaGore i alt+strelicaDolje u Microsoft wordu. (#3288)
* Nove brajične tablice za nekoliko indijskih jezika. (#4778)
* U microsoft excelu, NVDA sada izgovara kada je u čeliji sadržaj koji prelazi preko ćelije ili koji je izrezan. (#3040)
* Sada u excelu možete pritisnuti insert f7 kako bi ste se kretali između formula i grafova. (#1987)
* Podrška za čitanje grafova u Microsoft excelu. da biste ovo koristili, pritisnite (NVDA+f7) potom koristite strelice kako biste se kretali između podatkovnih točaka. (#1987)
* koristeći MathPlayer 4 firme Design Science, nvda sada može čitati i biti u interakciji sa matematičkim sadržajem u web preglednicima, microsoft wordu i powerpointu. Molimo pogledajte poglavlje "čitanje matematičkog sadržaja" u korisničkom priručniku". (#4673)
* Sada je moguće pridjeljivanje dodirne geste, tipkovničkog prečaca, ili tipke na brajičnom retku bilo kojem nvda dijaloškom okviru pomoću dijaloškog okvira "ulazne geste". (#4898)

### izmjene

* U NVDA dijaloškom okviru oblikovanje dokumenta, promjenjeni su tipkovnički prečaci za opcije  izvijesti o popisima, izvijesti o linkovima, izvijesti o brojevima redaka i izvijesti o imenu fonta. (#4650)
* U NVDA dijaloškom okviru postavke miša, dodani su tipkovnički prečaci za slijedeće opcije: reproduciraj zvučne koordinate prilikom pomicanja miša i svjetlina kontrolira glasnoću zvuka. (#4916)
* Značajno poboljšano izgovaranje boja. (#4984)
* nadograđen liblouis brajični prevoditelj na inačicu 2.6.2. (#4777)

### Ispravke grešaka

* Opisima znakova se sada ispravno rukuje u slučajevima kada postoje spojni znakovi u nekim jezicima indijskog podkontinenta. (#4582)
* ako je opcija "vjeruj jeziku trenutnog glasa prilikom procesiranja simbola" uključena, dijaloški okvir izgovor simbola interpunkcije sada poštuje taj jezik. također, izgovor za jezik koji se uređuje, sada se prikazuje u naslovnoj traci. (#4930)
-U internet exploreru i drugim mshtml kontrolama, upisani znakovi se više ne izgovaraju nepotrebno u odabirnim okvirima za uređivanje poput google pretrage na Googleovoj web stranici. (#4976)
* kada se označuju boje u aplikacijama Microsoft office uredskog paketa, Imena boja se sada ispravno čitaju. (#3045)
* Danska brajična tablica sada ponovno radi. (#4986)
* Tipke pageUp / pageDown sada se ponovno mogu koristiti kako bi se mijenjali slajdovi u powerpointowom prikazu slajdova. (#4850)
* U Skypeu za radnu površinu 7.2 i novijem, ispravno se izgovaraju obavjesti prilikom pisanja poruke, a također, riješeni su problemi prilikom pomicanja fokusa sa skypeovog prozora čavrljanja. (#4972)
* Ispravljene greške prilikom upisivanja nekih simbola poput zagrada u polje filtriranja u dijaloškom okviru ulazne geste. (#5060)
* u Internet Exploreru i drugim MSHTML kontrolama, pritisak tipkovničkih kombinacija G i shift+G koja služi za kretanje po grafikama sada prikazuje i slike u svrhu pristupačnosti (tj. ARIA role img). (#5062)

## 2015.1

Unapređenja u ovoj inačici uključuju način pregleda za dokumente u Microsoft Wordu i Outlooku; velika poboljšanja u podršci za Skype za Radnu površinu; i nezamjetne popravke grešaka u Microsoft Internet Exploreru.

### Nove značajke

* Sad možete dodavati nove simbole u dijaloškom okviru za dodavanje novih simbola. (#4354)
* U dijaloškom okviru ulazne geste možete koristiti novu značajku "filtriraj po" da biste prikazali geste koje sadrže samo određene riječi. (#4458)
* NVDA sad automatski čita tekst u aplikaciji mintty. (#4588)
* U dijaloškom okviru načina pregleda moguće je koristiti pretragu osjetljivu na velika slova. (#4584)
* Brzo kretanje (H za naslove itd.) i popis elemenata (NVDA+f7) su sada dostupni i u dokumentima programa Microsoft Word kad uključite način pregleda pomoću prečaca NVDA+razmak. (#2975)
* Čitanje HTML poruka u Microsoft Outlooku 2007 i višim vidno se poboljšalo jer je način pregleda automatski uključen za te poruke. Ako način pregleda nije uključen, što se zna dogoditi u rijetkim situacijama, možete ga prisilno uključiti koristeći prečac NVDA+razmak. (#2975) 
* Zaglavlja stupaca u Microsoft wordu su automatski čitana u tablicama gdje je autor strogo odredio zaglavlje retka pomoću svojstava tablice u microsoft wordu. (#4510) 
 * Međutim, za tablice u kojima su redovi spojeni ovo neće raditi automatski. U tom slučaju još uvijek možete namjestiti zaglavlja stupaca ručno unutar NVDA pomoću prečaca NVDA+shift+c.
* Obavijesti se čitaju uobičajeno u Skypeu za radnu površinu. (#4741)
* U Skypeu za radnu površinu, sada možete čitati i pregledavati zadnje pristigle poruke koristeći prečace NVDA+control+1 do NVDA+control+0; npr. NVDA+control+1 za posljednju poruku i NVDA+control+0 za desetu posljednju. (#3210)
* U razgovoru u programu Skype za radnu površinu, NVDA sada izvještava kada kontakt piše tekst. (#3506)
* NVDA se sada može tiho instalirati preko naredbenog retka bez da se pokreće instalirana kopija nakon instalacije. Kako biste to učinili koristite komandu --install-silent. (#4206)
* Podrška za Papenmeier BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus brajične retke. (#4614)

### Izmjene

* U dijaloškom okviru oblikovanje dokumenta, opcija izvijesti o pravopisnim pogreškama sada ima tipkovnički prečac (alt+p). (#793)
* NVDA će sad koristiti jezik sintetizatora/glasa za procesiranje znakova i simbola (uključujući imena simbola interpunkcije) u zavisnosti od toga je li automatsko prepoznavanje jezika uključeno. Da biste isključili ovu značajku tako da NVDA ponovno koristi svoj jezik sučelja, odznačite novu opciju u glasovnim postavkama koja se zove Vjeruj jeziku trenutnog glasa kad se procesiraju simboli i znakovi. (#4210)
* Podrška sintetizatora govora Newfon je uklonjena. Newfon je sad dostupan kao dodatak za NVDA. (#3184)
* Za korištenje uz pomoć NVDA zahtjeva se Skype za Radnu površinu 7 ili noviji; Ranije inačice nisu podržane. (#4218)
* Preuzimanje NVDA nadogradnji je sada više sigurnije. (Točnije, informacije o nadogradnjama sada se dobivaju putem https protokola i kontrolni zbroj datoteke se provjerava poslije preuzimanja.) (#4716)
* eSpeak je nadograđen tako da je njegova najnovija inačica 1.48.04 (#4325)

### Ispravke grešaka

* U Microsoft Excelu, rješavanje statusa izgovora kad su ćelije stupaca i redaka spojene. Npr, ako su A1 i B1 spojene, ćelija B2 će pod sobom imati  A1 i  B1 izgovorene kao zaglavlje stupca, bolje nego uopće neizgovoren. (#4617)
* Prilikom uređivanja sadržaja unutar tekstualnog okvira u Microsoft PowerPointu 2003, NVDA će ispravno prikazivati sadržaj u svakom od redaka. U prethodnim inačicama prvi znak unutar svakog retka na početku odlomka nebi bio izgovoren. (#4619)
* Svi se NVDA dijaloški okviri prikazuju na sredini zaslona, povećana urednost vizualne prezentacije i lakše snalaženje (#3148)
* U inačici Skype aplikacije za desktop, prilikom unosa poruke upoznavanja kod dodavanja novog kontakta, kretanje i unos poruke sad rade korektno. (#3661)
* Kad se fokus prebaci na novi element unutar prikaza stabla u aplikacijama kao što su Eclipse ili IDE, ako prethodni element predstavlja potvrdni okvir, isti će sad biti ispravno izgovoren. (#4586)
* U Microsoft Wordu, unutar dijaloškog okvira za provjeru pravopisa, sljedeća greška automatski će biti izgovorena nakon unešenih izmjena na posljednjoj grešci ili u slučaju ignoriranja greške primjenom odgovarajućeg tipkovničkog prečaca.(#1938)
* Tekst se ponovno ispravno može čitati na mjestima kao što su terminal programa Tera Term Pro i dokumenti u Balabolci. (#4229)
* Fokus se ponovno postavlja u dokumentu koji se trenutno uređuje kad se dovršava unos korejskog ili drugih istočnoazijskih jezika, kad se uređuje unutar okvira u INTERNET EXPLORERU i drugim MSHTML dokumentima. (#4045)
* U dijaloškom okviru ulazne geste, kad se označava izgled tipkovnice za tipkovničku gestu koja se dodaje, pritiskom escape tipke, izbornik se zatvara onako kako je očekivano umjesto zatvaranja dijaloškog okvira. (#3617)
* Kad se dodatak uklanja, Mapa koja sadrži određeni dodatak se sada pravilno uklanja. Prije ste NVDA trebali pokretati dva puta. (#3461)
* Ispravljene su velike greške pri korištenju Skype za Radnu površinu 7. (#4218)
* Kada šaljete poruku u skypeu za radnu površinu, ista se više ne čita dvaput. (#3616)
* U Skypeu za Radnu površinu, NVDA više neće sporadično nepravilno čitati više poruka (čak i cijeli razgovor). (#4644)
* Ispravljen problem u kojem NVDA prečac Izgovori datum/vrijeme nije poštivao regionalnu postavku koju je odredio korisnik u nekim slučajevima. (#2987)
* U načinu pregleda, besmisleni tekst (koji ponekada sadrži nekoliko redaka) više se ne prikazuje za većinu slika Kao što se može pronaći na Google grupama. (Specifično, ovo se događalo sa base64 enkodiranim slikama.) (#4793)
* NVDA se više neće smrzavati nakon nekoliko sekundi kad premještate fokus sa metro aplikacija u windowsu 8 kad se suspendiraju. (#4572)
* Atribut aria-atomic na živim regijama u Mozilla Firefoxu je sada uvažen, čak iako se element atomic promijeni. Prije je to utjecalo samo na elemente koji su slijedeći. (#4794) 
* Način pregleda će se osvježavati, žive regije će biti pročitane, za dokumente u načinu pregleda unutar aria aplikacija koje su ugrađene u dokument u Internet Exploreru ili drugim MSHTML kontrolama (#4798)
* Kada je tekst izmijenjen ili dodan u tekstualno relevantnim živim regijama u Internet Exploreru i drugim MSHTML kontrolama, Čita se samo dodan ili pročitan tekst, bolje nego sav tekst koji se nalazi u tom elementu. (#4800)
* Sadržaj koji je označen atributom aria-labelledby na elementima u Internet Exploreru i drugim MSHTML kontrolama ispravno zamjenjuje izvorni sadržaj gdje je to tako dozvoljeno. (#4575)
* Kad se provjerava pravopis u Microsoft Outlooku 2013, neispravno napisana riječ se sada ispravno čita. (#4848)
* U Internet Exploreru i drugim MSHTML kontrolama, sadržaj unutar elemenata koji je skriven sa visibility:hidden više se nepoželjno ne prikazuje u načinu pregleda. (#4839, #3776)
* U Internet Exploreru i drugim MSHTML kontrolama, atribut naslova na kontrolama obrasca više ne uzima prevlast nad drugim pridruženim natpisima]. (#4491)
* U Internet Exploreru i drugim MSHTML kontrolama, NVDA više ne izbjegava fokusiranje na elemente zbog aria-activedescendant attributa. (#4667)

## 2014.4

### Nove mogućnosti

* Novi jezici: Kolumbijski španjolski, Pendžabski.
* Sad je moguće ponovno pokrenuti NVDA, ili ponovno pokrenuti NVDA s isključenim dodacima u NVDA dijaloškom okviru za izlaz. (#4057)
 * NVDA je također moguće pokrenuti s isključenim dodacima uporabom opcije --disable-addons u naredbenom retku.
* U govornim rječnicima sad je moguće odrediti hoće li se uzorak slagati samo ako se radi o cijeloj riječi; npr. ne pojavljuje se kao dio veće riječi. (#1704)

### Promjene

* Ako je objekt na koji ste se pomaknuli uporabom objektne navigacije unutar dokumenta koji radi u načinu pregleda, ali objekt na kojem ste se prethodno nalazili nije bio, način pregleda je automatski postavljen na dokument. Ranije se ovo događalo samo ako je objekt navigatora pomaknut zbog promjene fokusa. (#4369)
* Popisi brajičnih redaka i govornih jedinica u njihovim odgovarajućim dijaloškim okvirima postavki su sad sortirani abecednim redom, svi osim stavke Bez brajice/Bez govora koje se sada nalaze na kraju popisa. (#2724)
* Brajični prevoditelj liblouis je ažuriran na inačicu 2.6.0. (#4434, #3835)
* U načinu pregleda, pritisak na e i shift+e za kretanje po poljima za uređivanje sada uključuje i uređivajuče odabirne okvire. Ovo se odnosi i na okvir za pretraživanje u zadnjoj inačici Google tražilice. (#4436)
* Klik na NVDA ikonu u području obavijesti uporabom lijeve tipke miša sada otvara NVDA izbornik, umjesto da ne napravi ništa. (#4459)

### Ispravke grešaka

* Prilikom premještanja fokusa natrag u dokument koji radi u načinu pregleda (npr. ponavljanja alt+tab naredbe za dolazak do već otvorene web stranice), pregledni kursor je ispravno pozicioniran na virtualnu točku umetanja, a ne više na fokusiranu kontrolu (npr. na obližnji link). (#4369)
* U Powerpoint dijaprojekcijama, pregledni kursor ispravno slijedi virtualnu točku umetanja. (#4370)
* U Mozilla Firefox-u i ostalim preglednicima zasnovanim na Gecko-u, novi sadržaj unutar žive regije će se najaviti čak i ako novi sadržaj ima upotrebljiv ARIA živi tip koji je drugačiji od matične žive regije; npr. kada je sadržaj označen kao pouzdan dodan u živu regiju označenu kao uglađenu. (#4169)
* U Internet Explorer-u i drugim MSHTML kontrolama, neki slućajevi gdje je dokument sadržan unutar drugog dokumenta više ne sprječavaju korisnika da pristupi nekom sadržaju (naročito okviri unutar okvira). (#4418)
* NVDA se više ne ruši prilikom pokušaja korištenja Handy Tech brajičnog retka u nekim slučajevima. (#3709)
* U Windows Vista sustavu, lažan dijaloški okvir "Ulazna točka nije pronađena" više se ne prikazuje u nekoliko slučajeva kao što su pokretanje NVDA preko prečaca na radnoj površini ili putem tipkovnog prečaca. (#4235)
* Ozbiljni problemi sa kontrolama uređivanja teksta unutar dijaloških okvira u nedavnim inačicama Eclipse-a su ispravljeni. (#3872)
* U Outlook-u 2010, premještanje točke umetanja sada funkcionira kako treba u polju za lokaciju kod zahtjeva za sastanke. (#4126)
* Unutar žive regije, sadržaj koji je označen kao neživ (npr. aria-live="off") će se sada ispravno ignorirati. (#4405)
* Prilikom izgovaranja teksta statusne trake koja ima naziv, naziv je sada ispravno odvojen od prve riječi teksta statusne trake. (#4430)
* U poljima za unos lozinke sa omogućenom opcijom za izgovaranje utipkanih riječi, višestruke zvjezdice se neće irelevantno najavljivati kod započinjanja novih riječi. (#4402)
* U Microsoft Outlook popisu poruka, stavke se više neće irelevantno najavljivati kao podatkovne stavke. (#4439)
* Prilikom odabira teksta unutar kontrole za uređivanje koda u Eclipse razvojnom okruženju, više se neće najaviti cjelokupan odabir svaki put kada se odabir promijeni. (#2314)
* Različite inačice Eclipse-a, poput Spring Tool Suite-a i inačice uključene u Android Developer Tools paketu se sada prepoznaju kao Eclipse i njima se postupa na odgovarajući način. (#4360, #4454)
* Praćenje miša i istraživanje dodirom u Internet Explorer-u i drugim MSHTML kontrolama (uključujući mnoge Windows 8 aplikacije) sada je puno preciznije na zaslonima visoke rezolucije ili kada se mijenja uvećanje dokumenta. (#3494) 
* Praćenje miša i istraživanje dodirom u Internet Explorer-u i drugim MSHTML kontrolama će sada najaviti naziv za više gumbi. (#4173)
* Pri korištenju Papenmeier BRAILLEX brajičnog retka sa BrxCom-om, tipke na retku sada rade kako treba. (#4614)

## Starije verzije

Informacije o starijim inačicama nisu prevedene, molimo ’pogledajte [englesku inačicu ovog dokumenta](../en/changes.html).

