# NVDA NVDA_VERSION korisničko uputstvo

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Kratka napomena za komande -->



## Uvod {#Introduction}

Dobrodošli u NVDA!

NonVisual Desktop Access (NVDA) je besplatan čitač ekrana otvorenog koda za Microsoft Windows.
Pružajući informacije koristeći sintetizatore govora i brajev red, omogućava slepim korisnicima pristup Windows operativnom sistemu uz jednake troškove videćim osobama.
NVDA razvija[NV Access](https://www.nvaccess.org/), uz saradnju zajednice.

### Opšte karakteristike {#GeneralFeatures}

NVDA omogućava interakciju sa Windows operativnim sistemom i puno drugih aplikacija.

Kratak video demonstracije na Engleskom, ["šta je NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) dostupan je na NV Access YouTube kanalu.

Glavne karakteristike su:

* Podrška za popularne aplikacije uključujući web preglednike, email klijente, programe za internet ćaskanje i Office pakete
* Ugrađen sintetizator govora koji podržava preko 80 jezika
* Prijavljivanje informacija o formatiranju teksta gde je to moguće uključujući ime fonta i veličina, stil i greške u pravopisu
* Automatski izgovor teksta ispod miša i korišćenje zvučnih informacija o poziciji miša
* Podrška za puno brajevih redova, uključujući sposobnost automatskog prepoznavanja puno redova kao i unos teksta za brajeve redove koji imaju tastaturu
* Sposobnost da se u potpunosti pokrene sa USB memorije bez potrebe za instalacijom
* Govorna instalacija koja je laka za korišćenje
* Preveden na 54 jezika
* Podrška za moderne Windows operativne sisteme uključujući 32 bitne i 64 bitne verzije
* Sposobnost da se pokrene na Windows ekranu za prijavljivanje i [drugim bezbednim ekranima](#SecureScreens).
* Izgovaranje teksta i kontrola prilikom korišćenja ekrana osetljivog na dodir
* Podrška za standardne interfejse pristupačnosti kao što su Microsoft Active Accessibility, Java Access Bridge, IAccessible2 i UI Automation
* Podrška za Windows komandnu liniju i druge konzolne aplikacije
* Sposobnost da označi sistemski fokus

### Sistemski zahtevi {#SystemRequirements}

* Operativni sistemi: Sve 32-bitne i 64-bitne verzije Windowsa 8.1, Windowsa 10, Windowsa 11 i sve serverske operativne sisteme počevši od Windows Servera 2012 R2.
    * AMD64 i ARM64 Windows verzije su podržane.
* Barem 150 MB memorijskog prostora.

### Internacionalizacija {#Internationalization}

Važno je da ljudi gde god da se nalaze na svetu, bez obzira koji jezik govore, dobiju jednak pristup tehnologiji.
Pored Engleskog, NVDA je preveden na 54 jezika uključujući: Afrikanski, Albanski, Amharski, Arapski, Aragoneski, Bugarski, Burmese, Katalonski, Kineski (pojednostavljen i tradicionalni), Hrvatski, Češki, Danski, Holandski, Farsi, Finski, Francuski, Galski, Gruzijski, Nemački (Nemačka i Švajcarska), Grčki, Hebrejski, Indijski, Mađarski, Islandski, Irski, Italijanski, Japanski, Kannada, Korejski, Kirgijški, Litvanski, Makedonski, Mongolski, Nepali, Norveški, Poljski, Portugalski (Brazil i Portugal), Pundžabi, Rumunski, Ruski, Srpski, Slovački, Slovenački, Španski (Kolumbija i Španija), Švedski, Tamil, Tajvanski, Turski, Ukrajinski i Vijetnamski.

### Podrška za sintetizatore govora {#SpeechSynthesizerSupport}

Pored pružanja svojih poruka i interfejsa na jednom od podržanih jezika, NVDA takođe dozvoljava korisnicima da čitaju tekst na bilo kom jeziku, dokle god imaju sintetizator koji podržava taj jezik.

Uz NVDA dolazi [eSpeak NG](https://github.com/espeak-ng/espeak-ng), besplatan, višejezičan i sintetizator otvorenog koda.

Informacije o sintezama koje NVDA podržava možete pronaći u delu [Podržani sintetizatori govora](#SupportedSpeechSynths).

### Podrška za brajeve redove {#BrailleSupport}

Za korisnike koji imaju brajev red, NVDA može pružati informacije na brajevom pismu.
NVDA koristi brajev prevodilac otvorenog koda [LibLouis](https://liblouis.io/) da bi pravio niz brajevih znakova na osnovu teksta.
Skraćen i standardan unos brajevih znakova je podržan.
Takođe, po podrazumevanim podešavanjima NVDA će automatski prepoznati puno brajevih redova.
Molimo vas da pogledate deo [Podržani brajevi redovi](#SupportedBrailleDisplays) za informacije o podržanim brajevim redovima.

NVDA podržava brajeve kodove za puno jezika, uključujući skraćene, standardne i kompjuterske brajeve kodove.

### Licenca i autorska prava {#LicenseAndCopyright}

NVDA je pod autorskim pravima NVDA_COPYRIGHT_YEARS NVDA saradnici.

NVDA je dostupan pod GNU opštom javnom licencom verzije 2, uz dva posebna izuzetka.
Izuzeci su označeni u dokumentu sa licencom u sekcijama "Non-GPL Components in Plugins and Drivers" i "Microsoft Distributable Code".
NVDA takođe koristi komponente koje su dostupne pod različitim slobodnim licencama otvorenog koda.
Možete menjati ovaj program dok god date izvorni kod onima koji to žele i dok je pod zaštitom ove licence.
Ovo važi za originalne i različite verzije ovog programa, plus bilo koji drugi rad.

Za više detalja, možete[videti celu licencu.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Za detalje o izuzecima, pristupite dokumentu licence u NVDA meniju u sekciji "pomoć".

## NVDA vodič za brz početak {#NVDAQuickStartGuide}

Ovaj vodič za brz početak sadrži tri glavne sekcije: preuzimanje, početna podešavanja i pokretanje NVDA.
Njih prate informacije o menjanju podešavanja, učestvovanju u zajednici i dobijanju pomoći.
Informacije u ovom vodiču su sažeti delovi ostatka korisničkog uputstva.
Molimo pogledajte potpuno korisničko uputstvo za detaljnije informacije o svakoj temi.

### Preuzimanje NVDA {#GettingAndSettingUpNVDA}

NVDA je u potpunosti besplatan za korišćenje.
Nema licencnih ključeva o kojima morate da brinete ili skupe pretplate koju morate da platite.
NVDA se ažurira, u proseku, četiri puta godišnje.
Najnovija verzija programa NVDA je uvek dostupna na "Download" stranici [NV Access websajta](NVDA_URL).

NVDA radi sa svim novijim verzijama Microsoft Windowsa.
Proverite [sistemske zahteve](#SystemRequirements) za potpune detalje.

#### Koraci za preuzimanje NVDA-a {#StepsForDownloadingNVDA}

Ovi koraci pretpostavljaju snalaženje u navigaciji na Web stranicama.

* Otvorite vaš Web pretraživač (pritisnite taster `Windows`, upišite reč "internet" bez navodnika, i pritisnite `enter`)
* Učitajte NV Access download stranicu (pritisnite `alt+d`, upišite sledeću adresu i pritisnite `enter`): 
https://www.nvaccess.org/download 
* Aktivirajte "download" dugme
* Pretraživač će možda zahtevati određenu radnju nakon preuzimanja, a zatim će započeti preuzimanje
* U zavisnosti od pretraživača, datoteka će se možda automatski pokrenuti nakon što se preuzme
* Ako datoteka mora ručno da se pokrene, pritisnite `alt+n` da se prebacite na prostor obaveštenja, zatim `alt+r` da pokrenete datoteku (ili neke druge korake za vaš pretraživač)

### Podešavanje programa NVDA {#SettingUpNVDA}

Pokretanje datoteke koja je preuzeta započeće privremenu kopiju programa NVDA.
Zatim ćete biti upitani da li želite da instalirate NVDA, napravite prenosnu kopiju ili da samo nastavite korišćenje privremene kopije.

NVDA ne zahteva pristup Internetu da bi se instalirao nakon što se pokretač preuzme.
Ako je dostupna, veza sa internetom dozvoljava da NVDA periodično proveri dostupna ažuriranja.

#### Koraci za pokretanje preuzetog pokretača {#StepsForRunningTheDownloadLauncher}

Instalaciona datoteka se zove "nvda_2022.1.exe" ili slično.
Godina i verzija se menjaju u toku ažuriranja kako bi se označila trenutna verzija.

1. Pokrenite preuzetu datoteku.
Muzika će se reprodukovati dok se privremena NVDA kopija učitava.
Nakon što se učita, NVDA će govoriti kroz ostatak procesa.
1. Prozor NVDA pokretača se pojavljuje sa licencnim ugovorom.
Pritisnite `strelicuDole` da pročitate licencni ugovor ako želite.
1. Pritisnite `tab` da se prebacite na izborno polje "Slažem se", a zatim pritisnite `razmak` da ga označite.
1. Pritisnite `tab` da se krećete kroz opcije, zatim pritisnite `enter` na željenoj opciji.

Opcije su: 

* "Instaliraj NVDA na ovaj računar": ovo je glavna opcija koju će većina korisnika želeti za lakše korišćenje programa NVDA. 
* "Napravi prenosnu kopiju": ovo dozvoljava programu NVDA da bude podešen u bilo kom folderu bez instalacije.
Ovo je korisno na računarima bez administratorskih prava, ili na memorijskim uređajima kako biste NVDA nosili sa sobom.
Kada je ova opcija izabrana, NVDA vas vodi kroz korake za pravljenje prenosne kopije.
Glavna stvar koju NVDA mora da zna je folder u kojem treba napraviti prenosnu kopiju. 
* "Nastavi sa korišćenjem": ovo ostavlja privremenu NVDA kopiju pokrenutu.
Ovo je korisno kako biste testirali karakteristike nove verzije pre nego što je instalirate.
Kada je ova opcija izabrana, prozor pokretača se zatvara i privremena NVDA kopija ostaje pokrenuta dok se ne zatvori ili se računar isključi.
Napomena da se promene podešavanja ne čuvaju. 
* "Otkaži": ovo zatvara NVDA bez izvršavanja bilo koje radnje.

Ako planirate da uvek koristite NVDA na ovom računaru, izabraćete opciju da instalirate NVDA.
Instaliranje NVDA-a će vam omogućiti dodatne funkcije kao što su automatsko pokretanje nakon prijave i mogućnost čitanja ekrana za prijavu i drugih [bezbednih ekrana](#SecureScreens).
Ovo nije moguće sa prenosnim i privremenim kopijama.
Za potpune detalje o ograničenjima korišćenja prenosnih i privremenih kopija programa NVDA, molimo pročitajte [ograničenja prenosnih i privremenih kopija](#PortableAndTemporaryCopyRestrictions).

Instaliranje vam takođe dozvoljava pravljenje prečica na radnoj površini i u start meniju, i dozvoljava programu NVDA da se pokrene prečicom `control+alt+n`.

#### Koraci za NVDA instalaciju iz pokretača {#StepsForInstallingNVDAFromTheLauncher}

Ovi koraci vas vode kroz najčešće opcije instalacije.
Za više detalja o dostupnim opcijama, molimo pogledajte [opcije instalacije](#InstallingNVDA).

1. Iz pokretača, uverite se da je izborno polje slaganja sa licencnim ugovorom označeno.
1. Krećite se `Tabom` do, i aktivirajte dugme "Instaliraj NVDA na ovaj računar".
1. Slede opcije korišćenja programa NVDA na Windows ekranu za prijavljivanje i da napravite prečicu na radnoj površini.
One su podrazumevano označene.
Ako želite, pritisnite `tab` i `razmak` da promenite bilo koju od ovih opcija, ili ih ostavite na podrazumevanim vrednostima.
1. Pritisnite `enter` da nastavite.
1. Windows dijalog "Kontrole korisničkog naloga (KKN)" će se pojaviti i upitaće vas "Da li želite da dozvolite ovoj aplikaciji da izvrši promene na vašem računaru?".
1. Pritisnite `alt+D` na Srpskoj ili `Alt+Y` na Engleskoj verziji Windowsa da dozvolite promene.
1. Traka napredovanja će se popunjavati dok se NVDA instalira.
U toku ovog procesa NVDA će reprodukovati zvučne signale koji povećavaju visinu.
Ovaj proces je često brz i možda se neće ni primetiti.
1. Dijalog će se pojaviti i potvrditi da je NVDA instalacija uspešna.
Poruka će vas savetovati da "pritisnete u redu da pokrenete instaliranu kopiju".
Pritisnite `enter` da pokrenete instaliranu kopiju.
1. Dijalog "Dobrodošli u NVDA" će se pojaviti, i NVDA čita poruku dobrodošlice.
Fokus je na izbornom okviru "Raspored tastature".
Po podrazumevanim podešavanjima, "Desktop" raspored tastature koristi numeričku tastaturu za neke funkcije.
Ako želite, pritisnite `strelicuDole` da izaberete "Laptop" raspored tastature kako bi se prečice koje koriste numeričku tastaturu prebacile na druge tastere.
1. Pritisnite `tab` da se prebacite na izborno polje "Koristite `capsLock` kao NVDA taster".
`Insert` je podrazumevano podešen kao NVDA taster.
Pritisnite `razmak` da izaberete `capsLock` kao alternativan modifikatorski taster.
Napomena da se raspored tastature podešava odvojeno od NVDA tastera.
NVDA taster i raspored tastature se naknadno mogu promeniti iz podešavanja tastature.
1. Koristite `tab` i `razmak` da podesite druge opcije na ovom ekranu.
One određuju da li se NVDA automatski pokreće.
1. Pritisnite `enter` da zatvorite ovaj dijalog uz pokrenut NVDA.

### Pokretanje programa NVDA {#RunningNVDA}

Potpuno NVDA korisničko uputstvo sadrži sve NVDA komande, odvojene u različite sekcije.
Tabele komandi su takođe dostupne iz "Kratkih napomena o komandama".
Modul "Osnovnih NVDA vežbi" sadrži duži opis svake komande uz obavljanje aktivnosti korak po korak.
"Osnovne NVDA vežbe" su dostupne iz [NV Access prodavnice](http://www.nvaccess.org/shop). Trenutno, ova knjiga nije prevedena.

Evo nekih osnovnih komandi koje se često koriste.
Sve komande se mogu podesiti, pa su ovo podrazumevane prečice za ove funkcije.

#### NVDA modifikatorski taster {#NVDAModifierKey}

Podrazumevani NVDA taster je ili `NumeričkaNula`, (kada je `numLock` isključen), ili `insert` taster, koji je blizu tastera `delete`, `home` i `end`.
NVDA modifikatorski taster može takođe biti podešen kao `capsLock` taster.

#### Pomoć za unos {#InputHelp}

Kako biste naučili i vežbali lokacije tastera, pritisnite `NVDA+1` da uključite pomoć za unos.
Dok ste u režimu pomoći za unos, izvršavanje bilo koje ulazne komande (kao što je pritiskanje tastera ili vršenje pokreta na ekranu osetljivom na dodir) će prijaviti radnju i reći šta radi (ako nešto radi).
Same komande neće biti izvršene dok ste u režimu pomoći za unos. 

#### Pokretanje i zaustavljanje NVDA-a {#StartingAndStoppingNVDA}

| Ime |Desktop taster |Laptop taster |opis|
|---|---|---|---|
|Pokreni NVDA |`control+alt+n` |`control+alt+n` |Pokreće ili restartuje NVDA|
|Zaustavi NVDA |`NVDA+q`, zatim `enter` |`NVDA+q`, zatim `enter` |Zatvara NVDA|
|Pauziraj ili nastavi govor |`šift` |`šift` |Odmah pauzira govor. Ako se pritisne ponovo govor će nastaviti tamo gde je stao|
|Zaustavi govor |`kontrol` |`kontrol` |Odmah zaustavlja govor|

#### Čitanje teksta {#ReadingText}

| Ime |Desktop taster |Laptop taster |opis|
|---|---|---|---|
|Izgovori sve |`NVDA+strelicaDole` |`NVDA+a` |Počinje čitanje od trenutne pozicije, pomerajući kursor dok čita|
|Pročitaj trenutni red |`NVDA+strelicaGore` |`NVDA+l` |Čita red. Pritiskanje dva puta sriče red. Pritiskanje tri puta sriče red korišćenjem opisa znakova (Avala, Beograd, Cetinje, i tako dalje)|
|Pročitaj izbor |`NVDA+šift+strelicaGore` |`NVDA+šift+s` |Čita bilo koji tekst koji je izabran. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta sriče se uz opise znakova|
|Pročitaj tekst privremene memorije |`NVDA+c` |`NVDA+c` |Čita bilo koji tekst u privremenoj memoriji. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta sriče se uz opise znakova|

#### Prijavljivanje lokacije i drugih informacija {#ReportingLocation}

| Ime |Desktop taster |Laptop taster |opis|
|---|---|---|---|
|Naslov prozora |`NVDA+t` |`NVDA+t` |Prijavljuje naslov trenutno aktivnog prozora. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta kopiraće se u privremenu memoriju|
|Prijavi fokus |`NVDA+tab` |`NVDA+tab` |Prijavljuje trenutnu kontrolu koja ima fokus. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta sriče se uz opise znakova|
|Čita prozor |`NVDA+b` |`NVDA+b` |Čita trenutni prozor u celini (korisno za dijaloge)|
|Čitaj statusnu traku |`NVDA+end` |`NVDA+šift+end` |Prijavljuje statusnu traku ako je NVDA pronađe. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta informacija se kopira u privremenu memoriju|
|Čitaj vreme |`NVDA+f12` |`NVDA+f12` |Ako se pritisne jednom prijavljuje se trenutno vreme, ako se pritisne dva puta prijavljuje se datum. Vreme i  datum se prijavljuju u  formatu datuma i vremena podešenom za sat na sistemskoj traci.|
|Prijavi formatiranje teksta |`NVDA+f` |`NVDA+f` |Prijavljuje formatiranje teksta. Ako se pritisne dva puta innformacija se prikazuje u prozoru|
|Prijavi odredište linka |`NVDA+k` |`NVDA+k` |Ako se pritisne jednom, prijavljuje odredišnu adresu linka na trenutnoj poziciji kursora ili fokusa. Ako se pritisne dva puta, prikazuje se u prozoru radi pažljivijeg pregleda|

#### Menjanje informacija koje NVDA čita {#ToggleWhichInformationNVDAReads}

| Ime |Desktop taster |Laptop taster |opis|
|---|---|---|---|
|Izgovori ukucane znakove |`NVDA+2` |`NVDA+2` |Kada je omogućeno, NVDA će izgovoriti sve znakove koje upisujete na tastaturi.|
|Izgovori ukucane reči |`NVDA+3` |`NVDA+3` |Kada je omogućeno, NVDA će izgovarati reči koje upisujete na tastaturi.|
|Izgovori komandne tastere |`NVDA+4` |`NVDA+4` |Kada je omogućeno, NVDA će izgovarati sve tastere na tastaturi koji nisu znakovi. Ovo uključuje kombinacije tastera kao što su kontrol plus neko drugo slovo.|
|Omogući praćenje miša |`NVDA+m` |`NVDA+m` |Kada je omogućeno, NVDA će izgovarati tekst ispod pokazivača miša, dok ga pomerate po ekranu. Ovo vam dozvoljava da pronađete stvari na ekranu, fizičkim pomeranjem miša, umesto da ih tražite objektnom navigacijom.|

#### Krug podešavanja sintetizatora {#TheSynthSettingsRing}

| Ime |Desktop taster |Laptop taster |Opis|
|---|---|---|---|
|Pomeri se na sledeće podešavanje sintetizatora |`NVDA+kontrol+strelicaDesno` |`NVDA+šift+kontrol+strelicaDesno` |Pomera se na sledeće dostupno podešavanje govora nakon trenutnog, vraćajući se na prvo podešavanje nakon što dođe do poslednjeg|
|Pomeri se na prethodno podešavanje sintetizatora |`NVDA+kontrol+strelicaLevo` |`NVDA+šift+kontrol+strelicaLevo` |Pomera se na sledeće dostupno podešavanje govora pre trenutnog, vraćajući se na poslednje podešavanje nakon što dođe do prvog|
|Povećaj trenutno podešavanje sintetizatora |`NVDA+kontrol+strelicaGore` |`NVDA+šift+kontrol+strelicaGore` |Povećava podešavanje sintetizatora na kojem se trenutno nalazite. Na primer povećava brzinu, bira sledeći glas, pojačava jačinu|
|Povećaj trenutno podešavanje govora većim skokom |`NVDA+kontrol+pageUp` |`NVDA+šift+kontrol+pageUp` |Povećava vrednost trenutnog podešavanja govora na kojem se nalazite većim skokom. Na primer kada ste na podešavanju glasa, skočiće napred za dvadeset glasova; kada ste na podešavanjima klizača (brzina, visina, i tako dalje) povećaće vrednost za 20%.|
|Smanji trenutno podešavanje sintetizatora |`NVDA+kontrol+strelicaDole` |`NVDA+šift+kontrol+strelicaDole` |Smanjuje podešavanje sintetizatora na kojem se trenutno nalazite. Na primer smanjuje brzinu, bira prethodni glas, smanjuje jačinu|
|Smanji trenutno podešavanje govora većim skokom |`NVDA+kontrol+pageDown` |`NVDA+šift+kontrol+pageDown` |Smanjuje vrednost trenutnog podešavanja govora na kojem se nalazite većim skokom. Na primer kada ste na podešavanju glasa, skočiće nazad za dvadeset glasova; kada ste na podešavanjima klizača (brzina, visina, i tako dalje) smanjiće vrednost za 20%.|

Takođe je moguće podesiti vrednost na prvu ili poslednju u krugu govornih podešavanja tako što ćete dodati prilagođene prečice u [dialogu ulaznih komandi](#InputGestures), u kategoriji govor.
Ovo znači, na primer, kada ste na podešavanju brzine, podesiće brzinu na 0 ili 100.
+When you're on a voice setting, it will set the first or last voice.

#### Web navigacija {#WebNavigation}

Potpuna lista pojedinačnih slova za navigaciju je u sekciji [režim pretraživanja](#BrowseMode) korisničkog uputstva.

| Komanda |Prečica |Opis|
|---|---|---|
|Naslov |`h` |Premešta se na sledeći naslov|
|Naslov nivoa 1, 2, ili 3 |`1`, `2`, `3` |Premešta se na sledeći naslov određenog nivoa|
|Polje za unos |`f` |Premešta se na sledeće polje za unos (polje za uređivanje, dugme, i slično)|
|Link |`k` |Premešta se na sledeći link|
|Orjentir |`d` |Premešta se na sledeći orjentir|
|Lista |`l` |Premešta se na sledeću listu|
|Tabela |`t` |Premešta se na sledeću tabelu|
|Premeštaj se u nazad |`šift+slovo` |Pritisnite `šift` i bilo koje od slova iznad da se premestite na prethodni element te vrste|
|Lista elemenata |`NVDA+f7` |Prikazuje listu različitih vrsta elemenata, kao što su linkovi i naslovi|

### Opcije {#Preferences}

Većina NVDA funkcija se može promeniti ili omogućiti iz NVDA podešavanja.
Podešavanja, i druge opcije, dostupne su iz NVDA menija.
Da otvorite NVDA meni, pritisnite `NVDA+n`.
Da direktno otvorite NVDA dijalog opštih podešavanja, pritisnite `NVDA+kontrol+g`.
Mnogi ekrani za podešavanja imaju prečice da ih direktno otvorite, kao što su `NVDA+control+s` za sintetizatore, ili `NVDA+control+v` za druga podešavanja glasa.

### Zajednica {#Community}

NVDA ima aktivnu zajednicu korisnika.
Postoji glavna [mejling lista na Engleskom jeziku](https://nvda.groups.io/g/nvda) i stranica puna [lokalnih grupa na drugim jezicima](https://github.com/nvaccess/nvda-community/wiki/Connect).
NV Access, stvaraoci programa NVDA, su aktivni na [Twitteru](https://twitter.com/nvaccess) i [Facebooku](https://www.facebook.com/NVAccess).
NV Access takođe ima aktivan [blog u toku](https://www.nvaccess.org/category/in-process/).

Takođe je dostupan [program za NVDA sertifikovane eksperte](https://certification.nvaccess.org/).
Ovo je online ispit koji možete da položite kako biste demonstrirali vaše veštine u korišćenju programa NVDA.
[NVDA sertifikovani eksperti](https://certification.nvaccess.org/) mogu da objave svoje detalje za kontakt i druge relevantne poslovne detalje.

### Dobijanje pomoći {#GettingHelp}

Da biste dobili pomoć za NVDA, pritisnite `NVDA+n` da otvorite meni, a zatim `p` za pomoć.
Iz ovog podmenija možete pristupiti korisničkom uputstvu, kratkoj napomeni za komande, istoriji novih karakteristika i ostalim opcijama.
Ove prve tri opcije se otvaraju u podrazumevanom Web pretraživaču.
Opširniji materijali za vežbanje su dostupni u [NV Access prodavnici](https://www.nvaccess.org/shop).

Preporučujemo vam da počnete sa modulom "Osnovne NVDA vežbe".
Ovaj modul pokriva početne korake sve do korišćenja Weba i objektne navigacije.
Dostupan je u:

* [Elektronskoj verziji](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), što uključuje Word DOCX, Web stranicu HTML, eKnjigu ePub i Kindle KFX formate.
* [MP3 zvučnoj datoteci pročitanoj ljudskim glasom](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Štampanoj kopiji na UEB brajevom pismu](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) uz dostavu bilo gde u svetu.

Drugi moduli, uključujući i [NVDA paket za produktivnost sa popustom](https://www.nvaccess.org/product/nvda-productivity-bundle/), su dostupni u [NV Access prodavnici](https://www.nvaccess.org/shop/).

NV Access takođe prodaje [telefonsku podršku](https://www.nvaccess.org/product/nvda-telephone-support/), ili zasebno, ili kao deo [NVDA paketa za produktivnost](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Telefonska podrška uključuje lokalne brojeve u Australiji i SAD-u.

[Imejl grupe korisnika](https://github.com/nvaccess/nvda-community/wiki/Connect) su odličan izvor pomoći zajednice, kao i [sertifikovani NVDA eksperti](https://certification.nvaccess.org/).

Možete prijaviti greške ili predlagati nove funkcije koristeći [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
[Pravila za saradnike](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) sadrže bitne informacije za doprinos zajednici.

## Dodatne opcije podešavanja {#MoreSetupOptions}
### Opcije instalacije {#InstallingNVDA}

Ako instalirate NVDA direktno iz preuzetog pokretača, pritisnite dugme instaliraj NVDA.
Ako ste zatvorili ovaj dijalog ili želite da instalirate NVDA iz prenosne kopije, izaberite instaliraj NVDA u NVDA meniju iz podmenija alati.

Dijalog za instalaciju će zatražiti potvrdu i takođe reći da li ova instalacija ažurira neku postojeću instalaciju.
Aktiviranjem dugmeta nastavi počinje instalacija NVDA.
Ovde takođe imate nekoliko opcija koje su objašnjene u nastavku.
Kada se instalacija završi, pojaviće se poruka koja će vam reći da li je instalacija uspela.
Aktiviranje dugmeta OK će pokrenuti novu kopiju NVDA.

#### Upozorenje o nekompatibilnim dodacima {#InstallWithIncompatibleAddons}

Ako već imate instalirane dodatke moguće je da ćete dobiti upozorenje da će nekompatibilni dodaci biti onemogućeni.
Pre nego što možete da pritisnete dugme za nastavak morate da označite izborno polje kojim potvrđujete da razumete da će ovi dodaci biti onemogućeni.
Takođe ćete imati dugme kojim možete da pregledate listu dodataka koji će biti onemogućeni.
Pogledajte deo [dijalog sa nekompatibilnim dodacima](#incompatibleAddonsManager) za dodatnu pomoć za ovo dugme.
Nakon instalacije, možete ponovo omogućiti nekompatibilne dodatke na sopstvenu odgovornost iz [prodavnice dodataka](#AddonsManager).

#### Pokreni na Windows ekranu za prijavu {#StartAtWindowsLogon}

Ova opcija odlučuje da li NVDA treba biti pokrenut na Windows ekranu za prijavljivanje, pre nego što unesete vašu lozinku.
Ovo takođe uključuje kontrolu korisničkog naloga i [druge bezbedne ekrane](#SecureScreens).
Ova opcija je podrazumevano omogućena za nove instalacije.

#### Napravi prečicu na radnoj površini (ctrl+alt+n) {#CreateDesktopShortcut}

Ova opcija određuje da li NVDA treba da napravi prečicu za pokretanje na radnoj površini. 
Ako je napravljena, ona takođe dobija prečicu sa tastature `control+alt+n`, kako biste mogli da pokrenete NVDA u bilo kom trenutku sa ovom prečicom.

#### Kopiraj podešavanja prenosne kopije u trenutni nalog {#CopyPortableConfigurationToCurrentUserAccount}

Ova opcija bira da li konfiguracija trenutno pokrenute kopije NVDA treba da se kopira za korisnika koji je trenutno prijavljen, za instaliranu kopiju NVDA. 
Ovo neće kopirati podešavanja za druge korisnike ni za korišćenje na Windows ekranu za prijavljivanje i [drugim bezbednim ekranima](#SecureScreens).
Ova opcija je dostupna samo kada se instalira iz prenosne kopije, ne i kada se instalira iz preuzete datoteke.

### Pravljenje prenosne kopije {#CreatingAPortableCopy}

Ako pravite prenosnu kopiju iz preuzete datoteke, jednostavno aktivirajte dugme napravi prenosnu kopiju.
Ako ste zatvorili ovaj dijalog ili ste instalirali NVDA, Izaberite opciju napravi prenosnu kopiju u NVDA meniju a zatim u podmeniju alati.

Dijalog koji se otvori nakon toga vam omogućava izbor gde prenosna kopija treba da bude napravljena.
Ovo može biti lokacija na hard disku ili nekim drugim prenosnim medijima.
Tu takođe imate opciju koja bira da li treba kopirati trenutna podešavanja u prenosnu kopiju.
 Ova opcija je dostupna samo kada se pravi prenosna kopija iz instalirane kopije, ne i kada se pravi iz preuzete datoteke.
Aktiviranje dugmeta nastavi pravi prenosnu kopiju.
Nakon što se pravljenje završi, poruka će se pojaviti koja će vas obavestiti da je bilo uspešno.
Pritisnite u redu da zatvorite ovaj dijalog.

### Ograničenja prenosnih i privremenih kopija {#PortableAndTemporaryCopyRestrictions}

Ako želite da nosite NVDA sa sobom na USB disku ili drugom mediju koji podržava pisanje, onda izaberite da napravite prenosnu kopiju.
Instalirana kopija takođe može da napravi prenosnu kopiju u bilo kom trenutku. 
Prenosna kopija takođe ima mogućnost da se instalira na računaru u bilo kom trenutku.
Ali, ako želite da kopirate NVDA na medijima koji podržavaju samo čitanje kao što je CD, onda samo kopirajte preuzetu datoteku.
Pokretanje prenosne kopije direktno sa medija koji podržavaju samo čitanje trenutno nije podržano.

[NVDA instalacija](#StepsForRunningTheDownloadLauncher) se može koristiti kao privremena kopija programa NVDA.
Privremene kopije sprečavaju čuvanje NVDA podešavanja.
Ovo uključuje nemogućnost korišćenja [prodavnice dodataka](#AddonsManager).

Prenosne i privremene kopije programa NVDA imaju sledeća ograničenja:

* Nemogućnost automatskog pokretanja u toku ili nakon prijave.
* Nemogućnost interakcije sa aplikacijama koje su pokrenute sa administratorskim privilegijama, osim ako se NVDA ne pokrene sa administratorskim privilegijama(nije preporučeno).
* Nemogućnost čitanja ekrana kontrole korisničkog naloga(KKN) kada pokušate da pokrenete neku aplikaciju sa administratorskim privilegijama.
* Nemogućnost podrške unosa uz pomoć ekrana osetljivog na dodir.
* Nemogućnost pružanja režima pretraživanja i izgovora unetih znakova u aplikacijama iz Windows prodavnice.
* Stišavanje pozadinskih zvukova nije podržano.

## Korišćenje NVDA-a {#GettingStartedWithNVDA}
### Pokretanje programa NVDA {#LaunchingNVDA}

Ako ste instalirali NVDA, pokretanje NVDA možete ostvariti prečicom control+alt+n, ili izborom NVDA u start meniju.
Takođe možete upisati NVDA u dialog za pokretanje i pritisnuti enter.
Ako je NVDA već pokrenut, biće zaustavljen a zatim ponovo pokrenut.
Takođe možete dodati [opcije komandne linije](#CommandLineOptions) koje vam dozvoljavaju da izađete(-q), onemogućite dodatke(--disable-addons), i tako dalje.

Za instalirane kopije, NVDA čuva podešavanja u roaming application data folderu trenutnog korisnika po podrazumevanim podešavanjima(Na primer "`C:\Users\<korisnik>\AppData\Roaming`").
Moguće je promeniti ovo tako da NVDA učitava svoja podešavanja iz foldera local u folderu app data.
Pogledajte deo o [sistemskim parametrima](#SystemWideParameters) za više detalja.

Da pokrenete prenosnu kopiju, potrebno je ući u folder u kojem ste napravili prenosnu kopiju, i pritisnuti enter ili kliknuti dva puta na datoteku nvda.exe.
Ako je NVDA već pokrenut, automatski će biti zaustavljen pre pokretanja prenosne verzije.

Dok se NVDA pokreće, čućete niz tonova(koji vam govore da se NVDA učitava).
U zavisnosti od brzine vašeg računara, ili ako pokrećete NVDA sa sporijeg medija, možda će ovo malo duže trajati.
Ako traje duže, NVDA će reći"Učitavanje NVDA. Molimo sačekajte..."

Ako ne čujete ništa od ovoga, ili čujete Windows zvuk za grešku, ili silazne tonove, to znači da NVDA ima grešku, i možda ćete morati da prijavite grešku programerima.
Molimo proverite NVDA sajt da saznate kako to da uradite.

#### Dijalog dobrodošlice {#WelcomeDialog}

Kada se NVDA pokrene po prvi put, dobićete dijalog sa osnovnim informacijama o NVDA tasteru i NVDA meniju.
(Molimo pogledajte naredne sekcije o ovim temama.)
Dijalog takođe sadrži izborni okvir i tri izborna polja.
Izborni okvir vam omogućava da izaberete raspored tastature.
Prvo izborno polje vam dozvoljava da izaberete da li NVDA treba da koristi Capslock kao njegov taster.
Drugo vam omogućava da podesite da li NVDA treba automatski da se pokrene nakon prijave u Windows i dostupno je samo za instalirane kopije.
Treće vam dozvoljava da podesite da li ovaj dijalog dobrodošlice treba da se prikaže svaki put kada se NVDA pokrene.

#### Dijalog o prikupljanju statistika o korišćenju {#UsageStatsDialog}

Od NVDA verzije 2018.3, korisnik će biti upitan da li želi da dozvoli slanje podataka o korišćenju kompaniji NV Access kako bi pomogli u poboljšanju programa NVDA u budućnosti. 
Kada prvi put pokrenete NVDA, dijalog će se pojaviti koji će vas upitati da li želite da šaljete podatke o korišćenju kompaniji NV Access dok koristite NVDA.
Možete pročitati više informacija o podacima koje sakuplja NV Access u sekciji opštih podešavanja, [Dozvoli organizaciji NV Access prikupljanje statistika korišćenja programa NVDA](#GeneralSettingsGatherUsageStats).
Napomena: Aktiviranje opcije "Da" ili "Ne" će sačuvati ovo podešavanje i dijalog se nikada neće ponovo pojaviti osim ako ponovo ne instalirate NVDA.
Ali, možete ručno omogućiti ili onemogućiti ovo podešavanje u panelu opštih podešavanja programa NVDA. Da biste ručno promenili ovo podešavanje, možete promeniti opciju [Dozvoli NVDA projektu prikupljanje statistika korišćenja programa NVDA](#GeneralSettingsGatherUsageStats).

### O NVDA prečicama {#AboutNVDAKeyboardCommands}
#### NVDA taster {#TheNVDAModifierKey}

Većina prečica koje NVDA koristi zahteva od vas da pritisnete određen taster koji se zove NVDA taster zajedno sa jednim ili više tastera.
Bitni izuzeci ovome su komande za pregled teksta u desktop rasporedu koje koriste tastere sa numeričke tastature samostalno, ali postoje i drugi izuzeci.

NVDA može biti podešen tako da numerički insert, prošireni insert ili caps lock mogu da se koriste kao NVDA tasteri.
Po podrazumevanim podešavanjima, numerički insert i prošireni insert su podešeni kao NVDA tasteri.

Ako želite da koristite neki od ovih tastera kao da NVDA nije pokrenut(na primer želite da uključite caps lock kada ste podesili ovaj taster kao NVDA taster), možete pritisnuti taster dva puta za redom.

#### Rasporedi tastature {#KeyboardLayouts}

NVDA dolazi sa dva rasporeda komandi (poznati kao rasporedi tastature): Desktop raspored i laptop raspored.
Po podrazumevanim podešavanjima, NVDA koristi desktop raspored tastature, međutim možete lako prebaciti NVDA na laptop raspored tastature u kategoriji tastatura [dijaloga NVDA podešavanja](#NVDASettings), koji se dobija izborom stavke opcije iz NVDA menija.

Desktop raspored koristi numeričku tastaturu(sa numlock tasterom isključenim).
Iako većina laptopova nema numeričku tastaturu, neki laptopovi mogu da koriste FN taster zajedno sa brojevima na desnoj strani tastature(7, 8, 9, u, i, o, j, k, l, i tako dalje.).
Ako vaš laptop ne može da uradi ovo ili vam ne dozvoljava da isključite numlock, možda ćete želeti da pređete na laptop raspored.

### NVDA prečice za ekrane osetljive na dodir {#NVDATouchGestures}

Ako koristite NVDA sa ekranom osetljivim na dodir, možete da koristite NVDA putem prečica na ekranu.
Dok je NVDA pokrenut, osim ako je podrška za interakciju sa ekranom onemogućena, sve akcije sa ekrana preuzima NVDA. 
Tako da, radnje koje normalno funkcionišu bez NVDA-a neće raditi.
<!-- KC:beginInclude -->
Da omogućite ili onemogućite podršku interakcije sa ekranom osetljivim na dodir, pritisnite NVDA+control+alt+t.
<!-- KC:endInclude -->
Takođe možete da omogućite ili onemogućite [podršku interakcije sa ekranom](#TouchSupportEnable) iz kategorije interakcija sa ekranom osetljivim na dodir u NVDA podešavanjima.

#### Istraživanje ekrana {#ExploringTheScreen}

Osnovna radnja sa ekrana osetljivog na dodir je izgovor teksta bilo gde na ekranu.
Da biste to uradili, stavite vaš prst bilo gde na ekranu.
Takođe možete držati prst na ekranu i kretati se po njemu kako bi NVDA izgovarao tekst ispod vašeg prsta.

#### Pokreti {#TouchGestures}

Kada NVDA komande budu kasnije opisane u ovom vodiču, mogu da sadrže pokret koji možete da koristite sa ekrana osetljivog na dodir kako biste aktivirali tu komandu.
U nastavku su uputstva kako uspešno izvesti neke pokrete na ekranu.

##### Dodiri {#toc45}

Dodirnite ekran brzo sa jednim ili više prsta.

Jednostruki dodir jednim prstom se jednostavnije zove dodir.
Istovremeni dodir sa dva prsta je dodir sa dva prsta i tako dalje.

Ako se ekran dodirne više puta za redom, NVDA će tretirati ovo kao pokret sa više dodira.
Dodirivanje dva puta je dvostruki dodir.
Dodirivanje tri puta je trostruki dodir i tako dalje.
Naravno, ovi dvostruki dodiri takođe prepoznaju koliko prsta je na ekranu, tako da je moguće imati pokrete kao što su dvostruki dodir sa dva prsta, dodir sa četiri prsta, i tako dalje. 

##### Prevlačenja {#toc46}

Brzo prevucite prst preko ekrana.

Postoje četiri ovakva pokreta u zavisnosti od pravca prevlačenja: Prevlačenje levo, Prevlačenje desno, Prevlačenje gore I prevlačenje dole.

Kao i dodiri, više od jednog prsta se mogu koristiti za pokrete.
Tako da, pokreti kao što su prevlačenje sa četiri prsta gore ili dva prsta dole su mogući.

#### Režimi dodira {#TouchModes}

Budući da postoji mnogo više NVDA prečica nego pokreta sa ekrana, NVDA ima više režima koji omogućavaju više različitih komandi.
Dva režima su režim teksta i režim objekata. 
Određene komande u ovom dokumentu će možda imati režim dodira u zagradama nakon pokreta.
Na primer, prevlačenje gore(režim teksta) znači da će komanda biti izvršena ako prevučete gore, ali samo kada ste u režimu teksta.
Ako komanda nema režim, radiće u bilo kom režimu.

<!-- KC:beginInclude -->
Da se prebacite između različitih režima dodira, dodirnite jednom sa tri prsta
<!-- KC:endInclude -->

#### Tastatura na ekranu {#TouchKeyboard}

Tastatura na ekranu se koristi za unos teksta i komandi na ekranu osetljivom na dodir.
Kada ste fokusirani na polje za unos teksta, možete uključiti tastaturu tako što ćete dva puta dodirnuti ikonicu tastature na ekranu koja se nalazi na dnu ekrana.
Za tablet računare kao što su Microsoft Surface Pro, tastatura na ekranu je uvek dostupna kada je tastatura izvučena.
Da biste odbacili tastaturu, dodirnite ikonicu tastature na ekranu ili se pomerite dalje od polja za unos teksta.

Dok je tastatura na ekranu aktivna, da biste pronašli tastere na tastaturi, prebacite vaš prst na lokaciju tastature (obično na dnu ekrana ), a zatim se krećite po tastaturi jednim prstom.
Kada pronađete taster koji želite da pritisnete, dodirnite taster 2 puta ili otpustite prst, u zavisnosti od podešavanja izabranih u [kategoriji podešavanja ekrana osetljivog na dodir](#TouchInteraction) NVDA podešavanja.

### Režim pomoći za unos {#InputHelpMode}

Puno komandi je spomenuto kroz ovaj vodič, ali lak način da saznate šta svaka komanda radi je da uključite pomoć za unos.

Da uključite pomoć za unos, pritisnite NVDA+1.
Da je isključite, pritisnite NVDA+1 ponovo.
Dok ste u režimu pomoći za unos, korišćenje bilo koje komande(kao što su pritiskanje tastera ili pokreti sa ekrana) će prijaviti komandu i šta ona radi(ako radi nešto).
Komande neće ništa uraditi dok ste u režimu pomoći za unos.

### NVDA meni {#TheNVDAMenu}

NVDA meni vam dozvoljava da kontrolišete NVDA podešavanja, Dobijete pomoć, Sačuvate/vratite se na sačuvana podešavanja, menjate govorne rečnike, pristupite dodatnim alatima i izađete iz programa NVDA.

Da biste ušli u NVDA meni bilo gde u Windowsu dok je NVDA pokrenut, možete izvzršiti bilo koju od sledećih radnji:

* Pritiskanje `NVDA+n` na tastaturi.
* Dvostruki dodir sa dva prsta na ekranu osetljivom na dodir.
* Pristup sistemskoj traci pritiskanjem prečice `Windows+b`, kretanje `strelicomDole` do NVDA ikonice, a zatim pritiskanje tastera `enter`.
* Kao alternativa, pristupite sistemskoj traci prečicom `Windows+b`, krećite se `strelicomDole` do NVDA ikonice, i otvorite kontekstni meni pritiskanjem `aplikacionog` tastera koji se nalazi pored desnog kontrol tastera na većem broju tastatura.
Na tastaturi bez `aplikacionog` tastera, umesto toga pritisnite `šift+f10`.
* Desni klik na NVDA ikonici na Windows sistemskoj traci

Kada se meni otvori, možete koristiti strelice da se krećete po meniju, i taster `enter` da aktivirate stavku.

### Osnovne NVDA komande {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Ekran osetljiv na dodir |Opis|
|---|---|---|---|---|
|Pokreće ili restartuje NVDA |Control+alt+n |Control+alt+n |Nema |Pokreće ili restartuje NVDA sa radne površine, ako je ova Windows prečica omogućena u procesu instalacije programa NVDA. Ovo je Windows prečica i zato se ne može promeniti u dijalogu ulazne komande.|
|Zaustavi govor |Kontrol |Kontrol |dodir sa dva prsta |govor prestaje|
|Pauziraj govor |Šift |Šift |Nema komande |pauzira govor. Ako se pritisne ponovo govor se nastavlja gde je stao(ako trenutni sintetizator podržava pauziranje)|
|NVDA meni |NVDA+n |NVDA+n |dvostruki dodir sa dva prsta |otvara NVDA meni kako biste pristupili podešavanjima, alatima, dobili pomoć, i tako dalje.|
|Uključuje i isključuje pomoć za unos |NVDA+1 |NVDA+1 |Nema komande |pritiskanje bilo kog tastera u ovom režimu prijavljuje ime tastera, i opis komande koju NVDA koristi|
|Izlaz iz NVDA |NVDA+q |NVDA+q |Nema komande |izlazi iz NVDA|
|Ignoriši sledeći taster |NVDA+f2 |NVDA+f2 |Nema komande |govori NVDA-u da sledeći taster pošalje kroz aplikaciju, čak i ako je to NVDA komanda|
|Uključuje i isključuje režim spavanja za trenutnu aplikaciju |NVDA+šift+s |NVDA+šift+z |Nema komande |Režim spavanja isključuje sav govor ili brajev izlaz za trenutnu aplikaciju. Ovo je najkorisnije u aplikacijama koje već imaju karakteristike čitanja ekrana. Ponovo pritisnite ovu komandu da isključite režim spavanja.|

<!-- KC:endInclude -->

### Prijavljivanje sistemskih informacija {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Prijavi datum/vreme |NVDA+f12 |Ako se pritisne jednom prijavljuje trenutni datum, ako se pritisne dva puta prijavljuje trenutno vreme|
|Prijavi stanje baterije |NVDA+šift+b |prijavljuje stanje baterije, da li je punjač uključen i trenutni procenat.|
|Prijavi tekst privremene memorije |NVDA+c |prijavljuje tekst privremene memorije ako ima teksta.|

<!-- KC:endInclude -->

### Režimi govora {#SpeechModes}

Režim govora određuje kako će se sadržaj ekrana, obaveštenja, odgovori na komande i drugi izlaz izgovarati dok koristite NVDA.
Podrazumevani režim je "sa pričom", koji će govoriti u  svim situacijama u kojima očekujete govor kada se koristi čitač ekrana.
Ali, u nekim slučajevima, ili kada koristite određene programe, možda će vam neki od drugih režima govora biti značajniji.

Četiri dostupna režima govora su:

* Sa pričom (podrazumevani): NVDA će normalno govoriti kada se menjaju ekrani, obaveštenja i radnje kao što su pomeranje fokusa ili izvršavanje komandi.
* Na zahtev: NVDA će govoriti samo kada koristite komande koje imaju funkciju da nešto prijave (na primer prijavi naslov prozora); ali neće govoriti za radnje kao što su pomeranje fokusa ili kursora.
* Isključen: NVDA neće izgovarati ništa, ali suprotno režimu spavanja, u tišini će reagovati na komande.
* Sa pištanjem: NVDA će zameniti standardni govor pištanjima.

Režim sa pištanjem može biti koristan kada se stalno pojavljuje detaljni tekst u prozoru terminala, ali ne zanima vas sadržaj, već samo da nastavlja da se dodaje novi tekst; ili drugim rečima kada vas više zanima da se pojavljuje novi tekst od sadržaja.

Režim na zahtev može biti koristan kada vam ne trebaju stalne povratne  informacije o tome šta se dešava na ekranu ili na računaru, ali vam povremeno treba da proverite određene stavke korišćenjem komandi pregleda, i slično.
Primeri uključuju snimanje zvuka, korišćenje lupe, sastanci ili pozivi ili kao druga alternativa režimu pištanja.

Komanda vam dozvoljava da kružite kroz različite režime govora:
<!-- KC:beginInclude -->

| Ime |Prečica |Opis|
|---|---|---|
|Kruži kroz režime govora |`NVDA+s` |Kruži kroz režime govora.|

<!-- KC:endInclude -->

Ako vam treba da kružite samo kroz određene režime govora, pogledajte [Dostupni režimi za komandu koja kruži kroz režime govora](#SpeechModesDisabling) kako biste onemogućili neželjene režime.

## Navigacija sa NVDA-om {#NavigatingWithNVDA}

NVDA vam dozvoljava navigaciju sistemom na nekoliko načina, uključujući standardnu interakciju i pregled.

### Objekti {#Objects}

Svaka aplikacija i operativni sistem se sastoji iz puno objekata.
Objekat je jedna stavka kao što je deo teksta, dugme, polje za potvrdu, klizač, lista ili polje za unos teksta.

### Navigacija sa sistemskim fokusom {#SystemFocus}

Sistemski fokus, takođe poznat kao fokus, je [objekat](#Objects) koji prima tastere sa tastature.
Na primer, ako pišete u polju za unos teksta, polje za unos teksta ima fokus.

Najčešći način navigacije kroz Windows sa programom NVDA je pomeranje sistemskog fokusa standardnim komandama sa tastature, kao što je pritiskanje tastera tab ili šift+tab da se krećete napred i nazad kroz kontrole, pritiskanje tastera alt da uđete u traku menija a zatim korišćenje strelica za kretanje kroz meni, i korišćenje kombinacije alt+tab da se krećete kroz otvorene programe.
Dok to radite, NVDA će prijavljivati informacije o objektima, kao što su njegovo ime, tip, vrednost, stanje, opis, tastersku prečicu i informacije o poziciji.
Kada je [Vizuelno označavanje](#VisionFocusHighlight) omogućeno, lokacija sistemskog fokusa je takođe vizuelno označena.

Postoje određene komande koje mogu biti korisne u navigaciji sa sistemskim fokusom:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Opis|
|---|---|---|---|
|Prijavi trenutni fokus |NVDA+tab |NVDA+tab |Izgovara trenutni objekat ili kontrolu koja ima sistemski fokus. Ako se pritisne dva puta informacija se sriče|
|Prijavi naslov |NVDA+t |NVDA+t |Prijavi naslov trenutno aktivnog prozora. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta informacija se kopira u privremenu memoriju|
|Čitaj aktivan prozor |NVDA+b |NVDA+b |Čita sve kontrole u trenutnom prozoru(korisno za dijaloge)|
|Prijavi statusnu traku |NVDA+end |NVDA+Šift+end |Prijavljuje statusnu traku ako je NVDA pronađe. Ako se pritisne dva puta informacija se sriče. Ako se pritisne tri puta kopira se u privremenu memoriju|
|Prijavi tastersku prečicu |`šift+numeričko2` |`NVDA+kontrol+šift+.` |Prijavljuje tastersku prečicu trenutno fokusiranog objekta|

<!-- KC:endInclude -->

### Navigacija sa sistemskim kursorom {#SystemCaret}

Kada je neki [objekat](#Objects) koji dozvoljava navigaciju ili uređivanje [fokusiran](#SystemFocus), možete se kretati kroz tekst koristeći sistemski kursor, takođe poznat kao kursor za uređivanje.

Kada je fokus na objektu koji ima sistemski kursor, možete koristiti strelice, page up, page down, home, end, i tako dalje. Da se krećete kroz tekst.
Možete takođe uređivati tekst ako kontrola podržava uređivanje.
NVDA će izgovarati kada se krećete znak po znak, reč i red, i takođe će izgovarati dok birate ili uklanjate izbor teksta.

NVDA Pruža sledeće komande za sistemski kursor:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |opis|
|---|---|---|---|
|Izgovori sve |NVDA+Strelica dole |NVDA+a |Počinje čitanje od trenutne pozicije sistemskog kursora, pomerajući ga dok čita|
|Pročitaj trenutni red |NVDA+Strelica gore |NVDA+l |Čita red na kom se sistemski kursor nalazi. Ako se pritisne dva puta red se sriče. Ako se pritisne tri puta sriče red koristeći opise znakova.|
|Pročitaj trenutni izbor teksta |NVDA+šift+strelica gore |NVDA+šift+s |Čita trenutno odabran tekst|
|Prijavi formatiranje teksta |NVDA+f |NVDA+f |Prijavljuje formatiranje teksta na trenutnoj poziciji kursora. Ako se pritisne dva puta prikazuje informaciju u režimu pretraživanja|
|Prijavi odredište linka |`NVDA+k` |`NVDA+k` |Ako se pritisne jednom prijavljuje se odredišna adresa linka na trenutnoj poziciji kursora ili fokusa. Ako se pritisne dva puta prikazuje se u prozoru radi lakšeg pregleda|
|Prijavi lokaciju kursora |NVDA+Numerički taster za brisanje |NVDA+taster za brisanje |Prijavljuje informacije o lokaciji objekta ili teksta na poziciji sistemskog kursora. Na primer, ovo može uključiti poziciju dokumenta u procentima, udaljenost od ivica stranica ili tačnu poziciju na ekranu. Pritiskanje dva puta može pružiti dodatne detalje.|
|Sledeća rečenica |alt+strelica dole |alt+strelica dole |Pomera kursor na sledeću rečenicu i izgovara je. (Podržano samo u Microsoft Wordu i Outlooku)|
|Prethodna rečenica |alt+strelica gore |alt+Strelica gore |Pomera kursor na prethodnu rečenicu i izgovara je. (Podržano samo u Microsoft Wordu i Outlooku)|

Kada ste u tabeli, Sledeće komande su takođe dostupne:

| Ime |Komanda |Opis|
|---|---|---|
|Pomeri na prethodnu kolonu |Kontrol+alt+strelica levo |Pomera sistemski kursor na prethodnu kolonu(ostajete u istom redu)|
|Pomeri na sledeću kolonu |Kontrol+alt+strelica desno |Pomera sistemski kursor na sledeću kolonu(ostajete u istom redu)|
|Pomeri na prethodni red |kontrol+alt+strelica gore |Pomera sistemski kursor na prethodni red(ostajete u istoj koloni)|
|Pomeri na sledeći red |kontrol+alt+strelica dole |Pomera sistemski kursor na sledeći red(ostajete u istoj koloni)|
|Pomeri na prvu kolonu |kontrol+alt+home |Pomera sistemski kursor na prvu kolonu (ostajete u istom redu)|
|Pomeri na poslednju kolonu |kontrol+alt+end |Pomera sistemski kursor na poslednju kolonu (ostajete u istom redu)|
|Pomeri na prvi red |kontrol+alt+pageUp |Pomera sistemski kursor na prvi red (ostajete u istoj koloni)|
|Pomeri na poslednji red |kontrol+alt+pageDown |Pomera sistemski kursor na poslednji red (ostajete u istoj koloni)|
|Izgovori sve u koloni |`NVDA+kontrol+alt+strelicaDole` |Čita kolonu vertikalno od trenutne ćelije dole do poslednje ćelije u koloni.|
|Izgovori sve u redu |`NVDA+kontrol+alt+strelicaDesno` |Čita red horizontalno od trenutne ćelije desno do poslednje ćelije u redu.|
|Pročitaj celu kolonu |`NVDA+kontrol+alt+strelicaGore` |Čita trenutnu kolonu vertikalno od vrha do dna bez pomeranja sistemskog kursora.|
|Pročitaj ceo red |`NVDA+kontrol+alt+strelicaLevo` |Čita trenutni red horizontalno s leva na desno bez pomeranja sistemskog kursora.|

<!-- KC:endInclude -->

### Navigacija objekata {#ObjectNavigation}

Obično, radićete u aplikacijama koristeći komande koje pomeraju [fokus](#SystemFocus) i [kursor](#SystemCaret).
Ali, nekada, možda ćete želeti da istražite aplikaciju ili operativni sistem bez pomeranja fokusa ili kursora.
Možda ćete takođe želeti da radite sa [objektima](#Objects) kojima se ne može pristupiti pomoću tastature.
U tim slučajevima, možete da koristite navigaciju objekata.

Navigacija objekata vam omogućava da dobijate informacije o pojedinačnim [objektima](#Objects).
Kada dođete do objekta, NVDA će ga izgovoriti slično kao što izgovara sistemski fokus.
Za pregled teksta kao što se pojavljuje na ekranu, možete da koristite [pregled ekrana](#ScreenReview).

Umesto da se pomerate po svakom objektu na sistemu, objekti su organizovani hierarhiski.
Ovo znači da neki objekti sadrže dodatne objekte i morate ući u objekat da bi ste pristupili objektima koje taj objekat sadrži.
Na primer, lista sadrži stavke te liste, pa morate da uđete u listu kako biste pristupili njenim stavkama.
Ako ste se pomerili na stavku liste, komande za sledeći i prethodni objekat će ići kroz stavke te iste liste.
Ako se pomerite na objekat u kojem je stavka liste sadržana vratićete se na listu.
Nakon toga se možete kretati dalje od liste da biste pristupili drugim objektima.
Slično tome, alatna traka sadrži kontrole, pa morate ući u alatnu traku da pristupite kontrolama.

Ako ipak želite da se krećete između svakog pojedinačnog objekta na sistemu, možete koristiti komande da se pomerite na prethodni ili sledeći objekat u  ravnom prikazu.
Na primer, ako se krećete do sledećeg objekta u ovom ravnom prikazu a trenutni objekat u sebi sadrži druge objekte, NVDA će se automatski prebaciti na prvij unutrašnji objekat.
U suprotnom, ako trenutni objekat ne sadrži objekte, NVDA će se prebaciti na sledeći objekat u trenutnom nivou hierarhije.
Ako nema takvog sledećeg objekta, NVDA će pokušati da pronađe sledeći objekat u hierarhiji u zavisnosti od unutrašnjih objekata dok više nema objekata na koje se možete prebaciti.
Ista pravila se primenjuju i kada se krećete nazad u hierarhiji.

Objekat koji se trenutno pregleda se zove navigacioni objekat.
Kada stignete do nekog objekta, možete pregledati njegov sadržaj koristeći [komande za pregled teksta](#ReviewingText) dok ste u [režimu pregleda objekata](#ObjectReview).
Kada je [Vizuelno označavanje](#VisionFocusHighlight) omogućeno, lokacija trenutnog navigacionog objekta je takođe vizuelno označena.
Po podrazumevanim podešavanjima, navigacioni objekat se pomera zajedno sa sistemskim fokusom, ali ovo se može promeniti.

Napomena: Praćenje objektne navigacije brajevim redom može se podesiti korišćenjem [vezivanja brajevog reda](#BrailleTether).

Za navigaciju između objekata, koristite sledeće komande:

<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Pokret |Opis|
|---|---|---|---|---|
|Prijavi trenutni objekat |NVDA+numeričko5 |NVDA+šift+o |Nema komande |Prijavljuje trenutni navigacioni objekat. Ako se pritisne dva puta informacija se sriče, a pritiskanjem 3 puta informacija i vrednost se kopiraju u privremenu memoriju.|
|Premesti se na sadržani objekat |NVDA+numeričko8 |NVDA+šift+strelica gore |prevuci nagore(režim objekata) |premešta se na objekat koji sadrži trenutni navigacioni objekat|
|Premesti se na prethodni objekat |NVDA+numeričko4 |NVDA+šift+strelica levo |nema |pomera se na objekat pre trenutnog navigacionog objekta|
|Premesti se na prethodni objekat u ravnom prikazu |NVDA+numeričko9 |NVDA+šift+[ |prevlačenje levo (režim objekata) |Premešta se na prethodni objekat u ravnom prikazu hierarhije navigacije objekata|
|Premesti se na sledeći objekat |NVDA+numeričko6 |NVDA+šift+strelica desno |nema |premešta se na objekat posle trenutnog navigacionog objekta|
|Premesti se na sledeći objekat u ravnom prikazu |NVDA+numeričko3 |NVDA+šift+] |prevlačenje desno (režim objekata) |Premešta se na sledeći objekat u ravnom prikazu hierarhije navigacije objekata|
|Premesti se na prvi sadržan objekat |NVDA+numeričko2 |NVDA+šift+strelica dole |prevlačenje dole (režim objekata) |Premešta se na prvi objekat sadržan od strane navigacionog objekta|
|Premesti se na fokusiran objekat |NVDA+numerički minus |NVDA+taster za brisanje unazad |Nema komande |Premešta se na objekat koji trenutno ima sistemski fokus, i takođe postavlja pregledni kursor na poziciju sistemskog kursora, ako je prikazan|
|Aktiviraj trenutni navigacioni objekat |NVDA+numerički enter |NVDA+enter |dupli dodir |aktivira trenutni navigacioni objekat(slično kliku mišem ili pritiskanju tastera razmak kada ima sistemski fokus)|
|Premesti sistemski fokus ili kursor na poziciju pregleda |NVDA+šift+numerički minus |NVDA+šift+taster za brisanje unazad |Nema komande |Ako se pritisne jednom pomera sistemski fokus na mesto navigacionog objekta, ako se pritisne dva puta pomera sistemski kursor na poziciju preglednog kursora|
|Prijavi lokaciju kursora |NVDA+numerički taster za brisanje |NVDA+taster za brisanje |nema komande |Prijavljuje informacije o poziciji objekta ili teksta na poziciji sistemskog kursora. Na primer, ovo može uključiti procenat trenutne pozicije u dokumentu, udaljenost od ivica stranica ili tačnu poziciju na ekranu. Pritiskanje dva puta može pružiti dodatne detalje.|
|Pomera pregledni kursor na statusnu traku |Nema komande |Nema komande |Nema komande |Prijavljuje statusnu traku ako je NVDA pronađe. Takođe pomera navigacioni objekat na ovu lokaciju.|

<!-- KC:endInclude -->

Napomena: Komande sa numeričke tastature zahtevaju da num lock taster bude isključen kako bi ispravno radile.

### Pregled teksta {#ReviewingText}

NVDA Vam dozvoljava da čitate sadržaj [ekrana](#ScreenReview), trenutnog [dokumenta](#DocumentReview) ili trenutnog [objekta](#ObjectReview) znak po znak, reč po reč ili red po red.
Ovo je veoma korisno u mestima kao što su(Windows komandna linija) gde ne postoji [sistemski kursor](#SystemCaret).
Na primer, možete ovo da koristite da pročitate tekst duge informacije u dijalogu.

Kada pomerate pregledni kursor, sistemski kursor se ne pomera, pa možete da pregledate tekst bez gubljenja vaše pozicije uređivanja teksta.
Ali, po podrazumevanim podešavanjima, kada se sistemski kursor pomera, pregledni kursor ga prati.
Ovo se može uključiti i isključiti.

Napomena: Praćenje objektne navigacije brajevim redom može se podesiti korišćenjem [vezivanja brajevog reda](#BrailleTether).

Sledeće komande su dostupne za pregled teksta:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Pokret |Opis|
|---|---|---|---|---|
|Premesti na prvi red pregleda |Šift+numeričko7 |NVDA+control+home |Nema komande |Premešta pregledni kursor na prvi red teksta|
|Premesti na prethodni red pregleda |Numeričko7 |NVDA+strelica gore |Prevlačenje gore(režim teksta) |Pomera pregledni kursor na prethodni red teksta|
|Prijavi trenutni red pregleda |numpad8 |NVDA+šift+. |Nema komande |Izgovara trenutni red na kom se nalazi pregledni kursor. Ako se pritisne dva puta red se sriče. Ako se pritisne tri puta red se sriče koristeći opise znakova.|
|Prebaci se na sledeći red pregleda |Numeričko9 |NVDA+strelica dole |Prevlačenje dole(režim teksta) |Premesti pregledni kursor na sledeći red teksta|
|Premesti se na poslednji red pregleda |Šift+numeričko9 |NVDA+control+end |Nema komande |Pomera pregledni kursor na poslednji red u dokumentu|
|Premesti se na prethodnu reč pregleda |Numeričko4 |NVDA+control+strelica levo |Prevlačenje sa 2 prsta levo(Režim teksta) |Pomera pregledni kursor na prethodnu reč u tekstu|
|Prijavi trenutnu reč pregleda |Numeričko5 |NVDA+control+. |Nema komande |Izgovara trenutnu reč teksta na kojoj se nalazi pregledni kursor. Ako se pritisne dva puta reč se sriče. Ako se pritisne tri puta reč se sriče koristeći opise znakova.|
|Premesti se na sledeću reč pregleda |Numeričko6 |NVDA+control+strelica desno |Prevlačenje sa dva prsta desno(režim teksta) |Premešta pregledni kursor na sledeću reč|
|Premesti se na početak reda u pregledu |Šift+numeričko1 |NVDA+home |Nema komande |Premešta pregledni kursor na početak reda|
|Premesti se na prethodni znak pregleda |Numeričko1 |NVDA+strelica levo |Prevlačenje levo(režim teksta) |Premešta pregledni kursor na prethodno slovo u trenutnom redu teksta|
|Prijavi trenutni znak pregleda |Numeričko2 |NVDA+. |Nema komande |Izgovara trenutni znak u redu na kom se pregledni kursor nalazi. Ako se pritisne dva puta pruža se opis ili primer tog znaka. Ako se pritisne tri puta izgovara se decimalna i hexadecimalna vrednost tog znaka.|
|Premesti se na sledeći znak pregleda |Numeričko3 |NVDA+strelica desno |Prevlačenje desno(režim teksta) |Premešta pregledni kursor na sledeći znak u trenutnom redu teksta|
|Premesti se na kraj reda pregleda |Šift+numeričko3 |NVDA+end |Nema komande |Premešta pregledni kursor na kraj trenutnog reda u tekstu|
|Premesti se na prethodnu stranicu u pregledu |`NVDA+pageUp` |`NVDA+šift+pageUp` |nema komande |Premešta pregledni kursor na prethodnu stranicu teksta ako je podržano od aplikacije|
|Premesti se na sledeću stranicu u pregledu |`NVDA+pageDown` |`NVDA+šift+pageDown` |Nema komande |Premešta pregledni kursor na sledeću stranicu teksta ako je podržano od aplikacije|
|Izgovori sve uz pregled |Numerički plus |NVDA+šift+a |Prevlačenje dole sa 3 prsta(režim teksta) |Čita od trenutne pozicije preglednog kursora, pomerajući ga u toku čitanja|
|Izaberi a zatim kopiraj iz preglednog kursora |NVDA+f9 |NVDA+f9 |Nema komande |Počinje izbor teksta koji treba da se kopira iz preglednog kursora. Kopiranje nije odrađeno dok ne kažete programu NVDA gde se nalazi kraj vašeg odabira|
|Izaberi a zatim kopiraj pregledni kursor |NVDA+f10 |NVDA+f10 |Nema komande |Ako se pritisne jednom, tekst od početnog markera pa sve do kraja uključujući i trenutnu poziciju preglednog kursora je odabran. Ako je moguće, sistemski kursor će se pomeriti na odabran tekst. Nakon što se ova komanda pritisne drugi put, tekst se kopira u Windows privremenu memoriju|
|Pomeri se na označen početak za kopiranje u pregledu |NVDA+šift+f9 |NVDA+šift+f9 |nema |Pomera pregledni kursor na poziciju koja je prethodno označena kao početak za kopiranje|
|Prijavi formatiranje teksta |NVDA+šift+f |NVDA+šift+f |Nema |Prijavljuje formatiranje teksta na poziciji preglednog kursora. Ako se pritisne dva puta prikazuje informacije u režimu pretraživanja|
|Prijavi zamenu za trenutni simbol |nema |Nema |Nema |Izgovara simbol na poziciji preglednog kursora. Ako se pritisne 2 puta, prikazuje simbol i tekst koji se izgovara u režimu pretraživanja.|

<!-- KC:endInclude -->

Napomena: Tasteri sa numeričke tastature zahtevaju da taster numlock bude isključen kako bi ispravno radili.

Dobar način da zapamtite desktop raspored ovih prečica je da ih zamislite kao mrežu 3 sa 3, koja od vrha ka dnu pregleda redove, reči i znakove a s leva na desno pomera kursor na prethodni, izgovara trenutni ili sledeći.
Izgled je ovako ilustrovan:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|prethodni red |Trenutni red |Sledeći red|
|Prethodna reč |Trenutna reč |Sledeća reč|
|Prethodni znak |trenutni znak |Sledeći znak|

### Režimi pregleda {#ReviewModes}

Komande programa NVDA [za pregled teksta](#ReviewingText) mogu pregledati sadržaj trenutnog navigacionog objekta, trenutnog dokumenta ili ekrana, u zavisnosti od toga koji je režim pregleda odabran.

Sledeće komande menjaju režime pregleda:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Pokret |Opis|
|---|---|---|---|---|
|Prebaci se na sledeći režim pregleda |NVDA+numeričko7 |NVDA+pageUp |Prevlačenje gore sa dva prsta |Prelazi na sledeći dostupan režim pregleda|
|Prebaci se na prethodni režim pregleda |NVDA+numeričko1 |NVDA+pageDown |Prevlačenje dole sa dva prsta |Prelazi na prethodni dostupan režim pregleda|

<!-- KC:endInclude -->

#### Pregled objekata {#ObjectReview}

Dok ste u režimu pregleda objekata, možete pregledati samo sadržaj trenutnog [navigacionog objekta](#ObjectNavigation).
Za objekte kao što su polja za unos teksta ili druge osnovne tekstualne kontrole, ovo će obično biti tekstualni sadržaj.
Za druge objekte, ovo može biti ime ili vrednost.

#### Pregled dokumenta {#DocumentReview}

Kada je [navigacioni objekat](#ObjectNavigation) u dokumentu koji je u režimu pretraživanja(na primer Web stranica) ili drugom obimnijem dokumentu(na primer dokument programa Lotus Symphony ), moguće je prebaciti se na režim pregleda dokumenta.
Režim pregleda dokumenta vam dozvoljava da pregledate tekst celog dokumenta.

Kada pređete iz režima pregled objekata u pregled dokumenta, pregledni kursor je postavljen u dokument na poziciji navigacionog objekta.
Kada se krećete kroz dokument koristeći komande za pregled, navigacioni objekat se ažurira kako bi bio na trenutnoj poziciji preglednog kursora u dokumentu.

Napomena da će NVDA preći iz režima pregleda objekata u pregled dokumenta kada ste u dokumentima koji su u režimu pretraživanja.

#### Pregled ekrana {#ScreenReview}

Pregled ekrana vam dozvoljava da pregledate tekst kao što izgleda na ekranu u jednoj aplikaciji.
Ovo je slično funkciji pregleda ekrana ili kursora miša u drugim Windows čitačima ekrana.

Kada pređete u režim pregleda ekrana, pregledni kursor je na mestu trenutnog [navigacionog objekta](#ObjectNavigation).
Kada se krećete po ekranu koristeći komande pregleda, navigacioni objekat ažurira svoju poziciju kako bi bio na mestu trenutnog objekta na ekranu.

Napomena da u nekim novijim aplikacijama, NVDA možda neće videti deo teksta ili čitav tekst zbog novijih tehnologija slikanja ekrana koje nisu trenutno podržane.

### Navigacija sa mišem {#NavigatingWithTheMouse}

Kada pomerate miš, NVDA po podrazumevanim podešavanjima prijavljuje tekst koji je ispod pokazivača miša dok pomerate miš.
Gde je to podržano, NVDA će pročitati blizak pasus teksta, ali neke kontrole se mogu čitati samo po redovima.

NVDA takođe može biti podešen da izgovori vrstu [objekta](#Objects) ispod miša dok se pomera(na primer lista, dugme, i tako dalje.).
Ovo može biti korisno za potpuno slepe korisnike, zbog toga što ponekad, tekst nije dovoljan.

NVDA pruža način da saznate gde se miš nalazi tako što reprodukuje zvučne signale u zavisnosti od dimenzije ekrana.
Što je miš visočije na ekranu, visočija je visina signala.
Što je miš dalje od leve ili desne strane, signal će biti reprodukovan sa leve ili desne strane(ukoliko korisnik ima stereo zvučnike ili slušalice).

Ove dodatne karakteristike miša nisu uključene po podrazumevanim podešavanjima u programu NVDA.
Ako želite da iskoristite njihove prednosti, možete ih podesiti iz kategorije [podešavanja miša](#MouseSettings) [NVDA podešavanja](#NVDASettings), koja se nalaze u NVDA meniju izborom stavke opcije.

Iako bi trebalo koristiti fizički miš za navigaciju sa mišem, NVDA ima nekoliko glavnih komandi koje su vezane za miš:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Ekran osetljiv na dodir |Opis|
|---|---|---|---|---|
|Klik levog tastera miša |Numeričko podeljeno |NVDA+[ |Nema |Izvršava levi klik tastera miša jednom. Dvostruki klik se može izvršiti brzim pritiskanjem ove komande dva puta|
|Zaključavanje levog tastera miša |Šift+numeričko podeljeno |NVDA+control+[ |Nema |Zaključava levi taster miša. Pritisnite ponovo da ga otpustite. Da vučete miš, pritisnite ovu komandu a zatim ili pomerajte miš fizički ili koristite jednu od dostupnih komandi za prebacivanje miša|
|Desni klik miša |Numeričko puta |NVDA+] |Dodirnite i zadržite |Izvršava desni klik miša.|
|Zaključavanje desnog tastera miša |Šift+numeričko puta |NVDA+control+] |Nema |Zaključava desni taster miša. Pritisnite ponovo da ga otpustite. Da vučete miš, pritisnite ovu komandu a zatim ili pomerajte miš fizički ili koristite jednu od dostupnih komandi za prebacivanje miša|
|Prebaci miš na trenutni navigacioni objekat |NVDA+numeričko podeljeno |NVDA+šift+m |Nema |Pomera miš na lokaciju trenutnog navigacionog objekta i preglednog kursora|
|Navigacija do objekta ispod miša |NVDA+Numeričko puta |NVDA+šift+n |Nema |Postavlja navigacioni objekat na trenutnu lokaciju miša|

<!-- KC:endInclude -->

## Režim pretraživanja {#BrowseMode}

Veći dokumenti koji su samo za čitanje kao što su Web stranice se pregledaju koristeći režim pretraživanja programa NVDA.
Ovo uključuje dokumente u sledećim aplikacijama:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML poruke u programu Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Podržane knjige u programu Amazon Kindle za PC

Režim pretraživanja je takođe dostupan u Microsoft Word dokumentima.

U režimu pretraživanja, tekst je predstavljen jednostavnije tako da možete da se krećete standardnim komandama kursora kao da koristite standardan tekstualni dokument.
Sve komande programa NVDA [za sistemski kursor](#SystemCaret) će raditi u ovom režimu; na primer izgovori sve, prijavi formatiranje, komande za kretanje kroz tabelu, i tako dalje.
Kada je [Vizuelno označavanje](#VisionFocusHighlight) omogućeno, lokacija virtuelnog kursora režima pretraživanja je takođe vizuelno označena.
Informacije o tome da li je tekst link, naslov, i tako dalje. Se prijavljuju zajedno sa tekstom u toku kretanja.

Ponekad, moraćete da koristite određene komande direktno u dokumentu.
Na primer, ovo morate da radite u poljima za unos teksta i listama kako biste mogli da upisujete tekst i da koristite komande kursora.
Ovo radite prebacivanjem u režim fokusiranja, gde su skoro svi tasteri prebačeni do kontrole.
Kada ste u režimu pretraživanja, po podrazumevanim podešavanjima, NVDA će automatski preći u režim fokusiranja kada tasterom tab dođete do kontrole koja to zahteva.
Slično tome, ako se koristi taster tab ili se aktivira kontrola koja ne zahteva režim fokusiranja bićete prebačeni u režim pretraživanja.
Takođe možete pritisnuti enter ili razmak na kontrolama da se prebacujete između ovih režima.
Ako se pritisne escape vratićete se u režim pretraživanja.
Takođe, možete ručno ući u režim fokusiranja, kada će on ostati omogućen dok ga vi ne onemogućite.

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Prebacivanje režima |NVDA+razmak |Prebacuje se između režima fokusiranja i režima pretraživanja|
|Izlaz iz režima fokusiranja |escape |Vraća se u režim pretraživanja ako ste automatski ušli u režim fokusiranja|
|Osvežava dokument režima pretraživanja |NVDA+f5 |Ponavlja učitavanje trenutnog dokumenta(korisno ako određen sadržaj nedostaje u dokumentu. nije dostupno u programima Microsoft Word i Outlook.)|
|Pronađi |NVDA+control+f |Otvara dijalog u kome možete da upišete tekst koji želite da pronađete u dokumentu. Pogledajte sekciju [pretraga teksta](#SearchingForText) za dodatne informacije.|
|Pronađi sledeće |NVDA+f3 |Pretražuje sledeću pojavu teksta kojeg ste prethodno pretražili u dokumentu|
|Pronađi prethodno |NVDA+šift+f3 |Pretražuje prethodnu pojavu teksta kojeg ste prethodno pretražili u dokumentu|

<!-- KC:endInclude -->

### Navigacija jednim slovom {#SingleLetterNavigation}

Dok ste u režimu pretraživanja, za bržu navigaciju, NVDA takođe pruža prečice navigacije jednim slovom kako biste došli do posebnih elemenata.
Napomena da nisu sve komande podržane u svim vrstama dokumenata.

<!-- KC:beginInclude -->
Sledeći tasteri skaču na sledeći dostupan element, dok dodavanje šift tastera skače na prethodni element:

* h: Naslov
* l: Lista
* i: Stavka liste
* t: Tabela
* k: link
* n: Tekst koji nije link
* f: Polje unosa
* u: Neposećen link
* v: Posećen link
* e: Polje za unos teksta
* b: Dugme
* x: Izborno polje
* c: Izborni okvir
* r: radio dugme
* q: Citat
* s: separator
* m: Okvir
* g: Slika
* d: Region
* o: Umetnuti objekat (audio i video playeri, aplikacije, dijalozi, etc.)
* 1 do 6: Naslovi nivoa 1 do 6
* a: Napomena (komentar, revizija autora, i tako dalje.)
* `p`: Pasus teksta
* w: Greška u pravopisu

Da se pomerate na početak i kraj elemenata kao što su liste i tabele:

| Ime |Komanda |Opis|
|---|---|---|
|Pomeri se na početak sadržaja |Šift+zarez |Premešta se na početak sadržaja(listi, tabela, i tako dalje.) Gde se nalazi kursor|
|Pomeri se na kraj sadržaja |Zarez |Pomera se na kraj sadržaja(listi, tabela, i tako dalje.) Gde se nalazi kursor|

<!-- KC:endInclude -->

Neke Web aplikacije kao što su Gmail, Twitter i Facebook koriste slova kao prečice.
Ako želite da ih koristite i da u isto vreme koristite vaš kursor da čitate sadržaj u režimu pretraživanja, možete privremeno onemogućiti navigaciju slovima programa NVDA.
<!-- KC:beginInclude -->
Da isključite i uključite navigaciju slovima za trenutni dokument, pritisnite NVDA+šift+razmak.
<!-- KC:endInclude -->

#### Komanda za navigaciju po pasusima teksta {#TextNavigationCommand}

Možete skočiti na naredni ili prethodni pasus teksta pritiskanjem slova `p` ili `šift+p`.
Pasusi teksta se definišu skupom teksta koji izgleda kao da je cela rečenica.
Ovo može biti korisno kako biste pronašli početak sadržaja koji se može pročitati na raznim Web stranicama, kao što su:

* Sajtovi novina
* Forumi
* Članci na blogovima

Ove komande vam takođe mogu pomoći da preskočite neke vrste suvišnog sadržaja, kao što su:

* Oglasi
* Meniji
* zaglavlja

Molimo imajte na umu da iako NVDA pokušava da prepozna pasuse teksta što je bolje moguće, algoritam nije savršen i s vremena na vreme može da pogreši.
Slično tome, ova komanda se razlikuje u odnosu na komande za navigaciju po pasusima `kontrol+strelicaDole ili strelicaGore`.
Navigacija po pasusima teksta skače po pasusima teksta, dok komande za navigaciju po pasusima pomeraju kursor na prethodne ili sledeće pasuse bez obzira na to da li oni sadrže tekst ili ne.

#### Druge komande navigacije {#OtherNavigationCommands}

Uz komande brze navigacije koje su prikazane iznad, NVDA takođe ima komande koje nemaju podrazumevane podešene prečice.
Da biste koristili ove komande, prvo morate da podesite prečice za njih korišćenjem [dijaloga ulaznih komandi](#InputGestures).
Ovo je lista dostupnih komandi:

* Članci
* Figure
* Grupisanja
* Kartice
* Stavke menija
* Dugmadi prekidača
* Trake napredovanja
* Matematičke formule
* Vertikalno poravnati pasusi
* Tekst istog stila
* Tekst različitog stila

Imajte na umu da postoje dve komande za svaku vrstu elementa, da biste se kretali napred ili nazad u dokumentu, i morate da podesite prečice za obe komande kako biste mogli brzo da se krećete u oba pravca.
Na primer, ako želite da koristite `y` / `šift+y` tastere da se brzo krećete po karticama, uradite sledeće:

1. Otvorite dijalog ulaznih komandi iz režima pretraživanja.
1. Pronađite stavku "premešta se na narednu karticu" u sekciji režim pretraživanja.
1. Dodelite taster `y` pronađenoj komandi.
1. Pronađite stavku "premešta se na prethodnu karticu".
1. Dodelite `šift+y` pronađenoj komandi.

### Lista elemenata {#ElementsList}

Lista elemenata pruža listu različitih vrsta elemenata dokumenta u zavisnosti od trenutne aplikacije.
Na primer, u Web pretraživačima, Lista elemenata može prikazati listu linkova, naslova, dugmića, polja za unos ili orjentira.
Radio dugme vam dozvoljava da menjate vrstu elementa.
U dijalogu takođe postoji polje za unos teksta uz pomoć kojeg možete da pretražujete stranicu.
Nakon što izaberete stavku, možete koristiti dva dugmeta u dijalogu da dođete do stavke ili da je aktivirate.
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Lista elemenata u režimu pretraživanja |NVDA+f7 |Prikazuje listu različitih vrsta elemenata u dokumentu|

<!-- KC:endInclude -->

### Pretraga teksta {#SearchingForText}

Ovaj dijalog vam dozvoljava da pretražujete termine u trenutnom dokumentu.
U polje "upišite tekst koji želite da pronađete", tekst koji treba da bude pronađen se može upisati.
Izborno polje "osetljivo na velika i mala slova" uzima u obzir veličinu slova u tekstu.
Na primer, uz opciju "osetljivo na velika i mala slova" možete pronaći "NV Access" ali ne "nv access".
Koristite sledeće tastere za izvršavanje pretrage:
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Pronađi tekst |NVDA+control+f |Otvara dijalog za pretragu|
|Pronađi sledeće |NVDA+f3 |Traži sledeće pojavljivanje trenutnog termina pretrage|
|Pronađi prethodno |NVDA+šift+f3 |Pretražuje prethodno pojavljivanje trenutnog termina pretrage|

<!-- KC:endInclude -->

### Umetnuti objekti {#ImbeddedObjects}

Stranice mogu uključiti obogaćene elemente koristeći tehnologije kao što su Oracle Java i HTML5, kao i aplikacije i dijaloge.
Kada naiđete na njih u dokumentu režima pretraživanja, NVDA će izgovoriti"Umetnuti objekat", "Aplikacija" ili"Dijalog".
Možete se brzo kretati između njih koristeći o i šift+o tastere za brzu navigaciju kroz umetnute objekte.
Za interakciju sa ovim objektima, možete pritisnuti enter na njih.
Ako je pristupačan, možete koristiti taster tab za interakciju kao i u drugim aplikacijama.
Postoji komanda za vraćanje na stranicu koja sadrži ovakav objekat:
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Premesti se na sadržan dokument režima pretraživanja |NVDA+kontrol+razmak |Prebacuje fokus van umetnutog objekta i vraća ga na dokument koji ga sadrži|

<!-- KC:endInclude -->

### Režim ugrađenog izbora {#NativeSelectionMode}

Po podrazumevanim podešavanjima kada birate tekst koristeći `šift+strelice` u režimu pretraživanja, tekst se bira samo u tekstu koji NVDA predstavlja u dokumentu, a ne u samoj aplikaciji.
Ovo znači da se izbor ne vidi na ekranu, a kopiranje teksta prečicom  `kontrol+c` kopira samo obično tekstualno predstavljanje od strane programa NVDA, što znači da se formatiranje tabela, ili da li je nešto link neće kopirati.
Ali, NVDA ima režim ugrađenog izbora koji se može uključiti u određenim dokumentima režima pretraživanja (trenutno samo u programu Mozilla Firefox) što izaziva da ugrađeni izbor dokumenta prati izbor u NVDA režimu pretraživanja.

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Uključuje ili isključuje režim ugrađenog izbora |`NVDA+šift+f10` |Uključuje ili isključuje režim ugrađenog izbora|

<!-- KC:endInclude -->

Kada je uključen ugrađen izbor, kopiranje izbora prečicom `kontrol+c` će takođe koristiti funkcije kopiranja aplikacije, što znači da će formatiranje sadržaja biti kopirano u privremenu memoriju umesto običnog teksta.
Ovo znači da ako nalepite taj sadržaj u program kao što je Microsoft Word ili Excel, biće uključeno formatiranje kao što su tabele, ili da li je nešto link.
Imajte međutim na umu da u režimu ugrađenog izbora, neke oznake pristupačnosti ili druge informacije koje NVDA generiše u režimu pretraživanja neće biti uključene.
Takođe, iako će aplikacija pokušati što je bolje moguće da se ugrađeni izbor podudara sa izborom u režimu pretraživanja programa NVDA, možda neće biti u potpunosti precizno.
Ali, u situacijama u kojima želite da kopirate celu tabelu ili pasus formatiranog sadržaja, ova funkcija bi trebala da bude korisna.

## Čitanje matematičkog sadržaja {#ReadingMath}

NVDA može da čita i da se kreće kroz matematički sadržaj na Webu i u drugim aplikacijama, pružajući govorni pristup i pristup na brajevom redu. 
Ali, kako bi NVDA čitao i vršio interakciju sa matematičkim sadržajem, moraćete prvo da instalirate matematičku komponentu za NVDA.
Postoji nekoliko dodataka koji su dostupni u NVDA prodavnici dodataka koji nude podršku za matematiku, uključujući [MathCAT NVDA dodatak](https://nsoiffer.github.io/MathCAT/) i [Access8Math](https://github.com/tsengwoody/Access8Math). 
Molimo pogledajte poglavlje [Prodavnica dodataka](#AddonsManager) da biste saznali kako da istražujete i instalirate NVDA dodatke.
NVDA takođe može da koristi stariji [MathPlayer](https://info.wiris.com/mathplayer-info) program kompanije Wiris ako je pronađen na vašem sistemu, ali se ovaj program više ne održava.

### Podržani matematički sadržaj {#SupportedMathContent}

Uz odgovarajuću matematičku komponentu instaliranu, NVDA podržava sledeće vrste matematičkog sadržaja:

* MathML u programima Mozilla Firefox, Microsoft Internet Explorer i Google Chrome.
* Microsoft Word 365 moderne matematičke jednačine uz UI automation:
NVDA može da čita i vrši interakciju sa matematičkim zadacima u programu Microsoft Word 365/2016 verziji 14326 i novijim.
Međutim imajte na umu da sve prethodno napravljene MathType jednačine prvo moraju biti pretvorene u Office Math.
Ovo se može uraditi izborom svake a zatim izborom stavke "opcije jednačina", a zatim "pretvori u Office math" u kontekstnom meniju.
Uverite se da je vaša verzija programa MathType najnovija pre nego što ovo uradite.
Microsoft Word takođe sada pruža linearnu navigaciju simbola jednačine, i podržava unos matematike putem nekoliko različitih sintaksi, uključujući LateX.
Za dodatne detalje, molimo pogledajte [Jednačine linearnog formata pomoću UnicodeMath-a i LaTeX-a u programu Word](https://support.microsoft.com/sr-latn-rs/office/jedna%C4%8Dine-linearnog-formata-pomo%C4%87u-unicodemath-a-i-latex-a-u-programu-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint, i starije verzije programa Microsoft Word: 
NVDA može da čita i da se kreće kroz MathType jednačine i u Microsoft Powerpoint-u kao i Microsoft word-u.
MathType mora prvo da bude instaliran da bi ovo radilo.
Probna verzija je dovoljna.
Može se preuzeti sa [MathType presentation stranice](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Napomena da ovo još uvek nije zvaničan standard, tako da trenutno nema javno dostupnog programa koji može praviti ovakav sadržaj.
* Kindle čitač za PC:
NVDA može da čita i da se kreće kroz matematičke sadržaje knjiga programa Kindle za PC u knjigama sa pristupačnom matematikom.

Kada čitate dokument, NVDA će izgovoriti sav podržan matematički sadržaj na mestima na kojima se pojavi.
Ako koristite brajev red, takođe će biti prikazan na brajevom pismu.

### Interaktivna navigacija {#InteractiveNavigation}

Ako obično radite uz govor, u većini slučajeva, želećete da pročitate izraz u manjim delovima, umesto da čujete ceo izraz odjednom.

Ako ste u režimu pretraživanja, ovo možete uraditi tako što ćete pomeriti kursor na matematički sadržaj i pritisnuti enter.

Ako niste u režimu pretraživanja:

1. Prebacite kursor na matematički sadržaj.
Podrazumevano, pregledni kursor prati sistemski kursor, tako da obično možete da koristite sistemski kursor da dođete do sadržaja.
1. Zatim, aktivirajte sledeću komandu:

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Interakcija sa matematičkim sadržajem |NVDA+alt+m |Počinje interakciju sa matematičkim sadržajem.|

<!-- KC:endInclude -->

Nakon toga, NVDA će ući u matematički režim, u kojem možete da koristite komande kao što su strelice da istražujete sadržaj.
Na primer, možete se pomerati kroz izraz koristeći strelice levo i desno kao i uveličati deo izraza strelicom dole.

Kada želite da se vratite u dokument, jednostavno pritisnite taster escape.

Za više informacijama o dostupnim komandama i podešavanjima za čitanje i navigaciju kroz matematički sadržaj, molimo pogledajte dokumentaciju matematičke komponente koju ste instalirali.

* [MathCAT dokumentacija](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math dokumentacija](https://github.com/tsengwoody/Access8Math)
* [MathPlayer dokumentacija](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Ponekad matematički sadržaj može biti prikazan kao dugme koje, kada se aktivira, može da prikaže više informacija ili dijalog vezan za formulu.
Da aktivirate dugme ili element koji sadrži formulu, pritisnite ctrl+enter.

### Instaliranje programa MathPlayer {#InstallingMathPlayer}

Iako se obično preporučuje da koristite jedan od novijih NVDA dodataka za podršku matematike u programu NVDA, u određenim ograničenim uslovima MathPlayer će možda još uvek biti prihvatljiviji izbor.
Na primer MathPlayer može podržavati određeni jezik ili kod brajevog pisma koji nije podržan u novijim dodacima.
MathPlayer je besplatno dostupan sa Wiris websajta.
[Preuzmite  MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Nakon što instalirate MathPlayer, morate ponovo da pokrenete NVDA. 
Molimo imajte na umu da informacije o MathPlayer mogu napomenuti da je samo za starije pretraživače kao što su Internet Explorer 8.
Ovo važi samo za korisnike koji koriste MathPlayer za vizuelno prikazivanje matematičkog sadržaja, a može se zanemariti za korisnike koji čitaju i kreću se kroz matematički sadržaj uz NVDA.

## Brajevo pismo {#Braille}

Ako koristite brajev red, NVDA može prikazati informacije na brajevom pismu.
Ako vaš brajev red ima tastaturu, takođe možete pisati u skraćenom i standardnom brajevom pismu.
Brajev unos se takođe može prikazati na ekranu korišćenjem [Preglednika brajevog reda](#BrailleViewer) umesto, ili uz korišćenje brajevog reda.

Molimo pročitajte [podržani brajevi redovi](#SupportedBrailleDisplays) deo za informacije o posebnim komandama za brajeve redove.
Ovaj deo takođe sadrži informacije o redovima koji podržavaju automatsko pozadinsko prepoznavanje programa NVDA.
Možete podesiti brajev red korišćenjem kategorije [brajev red](#BrailleSettings) [NVDA podešavanja](#NVDASettings).

### Skraćenice za vrste kontrola, stanje i orjentire {#BrailleAbbreviations}

Kako bi što je više informacija moguće stalo na brajev red, sledeće skraćenice su dodate za vrste kontrola stanje kao i orjentire.

| Skraćenica |Vrsta kontrole|
|---|---|
|app |Aplikacija|
|art |članak|
|bqt |Citat|
|btn |Dugme|
|drbtn |Dugme padajućeg menija|
|spnbtn |Kružno dugme|
|splbtn |Dugme za razdvajanje|
|tgbtn |Dugme prekidača|
|cap |naslov|
|cbo |Izborni okvir|
|chk |Izborno polje|
|dlg |dialog|
|doc |Dokument|
|edt |Polje za unos teksta|
|pwdedt |Polje za unos lozinke|
|Umetnuti |Umetnuti objekat|
|enote |Završna napomena|
|fig |Figura|
|fnote |Fusnote|
|gra |Slika|
|grp |Grupisanje|
|hN |Naslov na nivou n, na primer h1, h2.|
|hlp |Pomoćni balon|
|lmk |Orjentir|
|lnk |link|
|lst |Lista|
|vlnk |Posećen link|
|mnu |Meni|
|mnubar |Traka menija|
|mnubtn |Dugme menija|
|mnuitem |Stavka menija|
|pnl |panel|
|prgbar |Traka napredovanja|
|bsyind |Zauzet pokazivač|
|rbtn |radio dugme|
|scrlbar |Klizna traka|
|sect |Sekcija|
|stbar |Statusna traka|
|tabctl |Kontrola kartice|
|tbl |Tabela|
|cN |kolona tabele sa brojem n, na primer c1, c2.|
|rN |Red tabele sa brojem n, na primer r1, r2.|
|term |terminal|
|tlbar |Traka sa alatima|
|tltip |Opis alata|
|tv |Prikaz stabla|
|tvbtn |Dugme prikaza stabla|
|tvitem |Stavka prikaza stabla|
|lv N |Stavka prikaza stabla na nivou N|
|wnd |Prozor|
|⠤⠤⠤⠤⠤ |separator|
|mrkd |Obeležen sadržaj|

Sledeći pokazivači stanja su takođe definisani:

| Skraćenica |Stanje kontrole|
|---|---|
|... |Prikazuje se kada objekat podržava automatsko dopunjavanje|
|⢎⣿⡱ |Prikazano kada je objekat (Na primer dugme prekidača) pritisnut|
|⢎⣀⡱ |Prikazano kada objekat (na primer dugme prekidača) nije pritisnut|
|⣏⣿⣹ |Prikazano kada je objekat (na primer izborno polje ) označen|
|⣏⣸⣹ |Prikazano kada je objekat (na primer izborno polje ) polovično označen|
|⣏⣀⣹ |Prikazano kada objekat (na primer izborno polje ) nije označen|
|- |Prikazano kada se objekat(na primer stavka prikaza stabla) može skupiti|
|+ |Prikazano kada se objekat(na primer stavka prikaza stabla) može proširiti|
|*** |Prikazano kada naiđete na zaštićen dokument ili kontrolu|
|clk |Prikazano kada se na objekat može kliknuti|
|cmnt |Prikazano kada postoji komentar za ćeliju u tabeli ili deo teksta u dokumentu|
|frml |Prikazano kada postoji formula u ćeliji tabele|
|Neispravan |Prikazano kada dođe do neispravnog unosa|
|ldesc |Prikazano kada objekat (obično slika) ima dug opis|
|mln |Prikazano kada polje za unos teksta dozvoljava unos više redova na primer polja za unos komentara na sajtovima|
|req |Prikazano kada je polje za unos obavezno|
|ro |Prikazano kada je objekat(na primer polje za unos teksta) samo za čitanje|
|sel |Prikazano kada je objekat izabran|
|nsel |Prikazano kada objekat nije izabran|
|sorted asc |Prikazano kada je objekat sortiran uzlazno|
|sorted desc |Prikazano kada je objekat sortiran silazno|
|submnu |Prikazano kada objekat ima dodatni prozor(obično podmeni)|

Takođe, sledeće skraćenice za orjentire su definisane:

| Skraćenica |Orjentir|
|---|---|
|bnnr |baner|
|cinf |Informacije o sadržaju|
|cmpl |Dodatni|
|form |Formular|
|main |Glavni|
|navi |Navigacija|
|srch |Pretraga|
|rgn |region|

### Brajev unos {#BrailleInput}

NVDA podržava unos skraćenog i standardnog brajevog pisma.
Možete izabrati tabelu koja će se koristiti za prevod teksta korišćenjem opcije [ulazna tabela](#BrailleSettingsInputTable) u kategoriji brajeva podešavanja [NVDA podešavanja](#NVDASettings).

Kada se koristi standardan brajev unos, tekst se ubacuje čim se napiše.
Kada se koristi skraćen brajev unos, tekst se ubacuje kada pritisnete razmak ili enter na kraju reči.
Napomena da brajev prevod uzima u obzir samo reč koju upišete i ne može zavisiti od prethodnih reči.
Na primer, ako koristite brajev kod u kojem brojevi počinju sa znakom za broj i ako pritisnete taster za brisanje da dođete do kraja broja, moraćete ponovo da upišete znak za broj za dodatne brojeve.

<!-- KC:beginInclude -->
Pritiskanje tačke 7 briše zadnji upisan znak.
Tačka 8 prevodi bilo koji brajev unos i pritiska enter.
Pritiskanje tačke7 i 8 prevodi brajev unos, bez pritiskanja tastera enter.
<!-- KC:endInclude -->

#### Unos prečica tastature {#BrailleKeyboardShortcuts}

NVDA podržava unos prečica kao i emuliranje pritiskanja tastera na tastaturi korišćenjem brajevog reda.
Ovo emuliranje se može izvršiti na dva načina: Direktno podešavanje brajevog unosa kao taster na tastaturi kao i korišćenje virtuelnih modifikatorskih tastera.

Tasteri koji se često koriste, kao što su strelice ili taster alt da se otvori meni, mogu se direktno podesiti kao unos na brajevom redu.
Drajveri za svaki brajev red već imaju unapred podešene neke od ovih komandi.
Možete promeniti ove komande ili dodati nove emulacije iz [dijaloga ulaznih komandi](#InputGestures).

Iako je ovaj način koristan za tastere koji se često koriste (kao što je tab), možda ne želite da pridružite jedinstvenu kombinaciju tastera za svaku prečicu na tastaturi.
Da bi se dozvolilo emuliranje pritiskanje prečica u kojima se neki tasteri drže, NVDA pruža komande za zaključavanje tastera kontrol, alt, šift, windows, i tastera NVDA, kao i komande za kombinaciju nekih od ovih tastera.
Da biste koristili ova zaključavanja tastera, prvo pritisnite komandu (ili niz komandi) za modifikatorske tastere koje želite da pritisnete.
Zatim pritisnite tastere koji su deo kombinacije koju želite da izvršite.
Na primer, da biste izvršili kombinaciju kontrol + f, koristite komandu "Virtuelno uključuje ili isključuje taster kontrol" a zatim upišite f,
A da biste upisali kontrol+alt+t, koristite ili komandu "virtuelno uključuje i isključuje taster kontrol" i "virtuelno uključuje ili isključuje taster alt", u bilo kom redosledu, ili komandu "virtuelno uključuje ili isključuje tastere kontrol i alt", a nakon toga upišite t.

Ako greškom uključite modifikatorske tastere, ponovno pokretanje komande će ih isključiti.

Kada pišete u brajevom kratkopisu, korišćenje modifikatorskih tastera će izazvati da vaš unos bude preveden odmah kao i da ste pritisnuli tačke 7 i 8.
Takođe, emulacija pritisnutih tastera ne može da uzme u obzir brajev unos koji je upisan pre nego što je modifikatorski taster pritisnut.
Ovo znači da, kako biste upisali alt plus 2 uz brajev kod koji koristi predznak za broj, prvo morate da uključite alt a zatim da upišete predznak za broj.

## Vid {#Vision}

Iako su primarni korisnici programa NVDA slepe osobe koje obično koriste govor ili brajev red, NVDA takođe pruža ugrađene funkcije za promenu sadržaja ekrana.
U programu NVDA, takvi vizuelni pomoćnici zovu se usluge vizuelne pomoći.

NVDA pruža nekoliko ovakvih usluga koje su opisane ispod.
Dodatne usluge se mogu uključiti u [NVDA dodacima](#AddonsManager).

NVDA podešavanja vida se mogu promeniti u [kategoriji vid](#VisionSettings) dijaloga [NVDA podešavanja](#NVDASettings).

### Vizuelno označavanje {#VisionFocusHighlight}

Vizuelno označavanje može pomoći da pronađete pozicije [sistemskog fokusa](#SystemFocus), [navigacionog objekta](#ObjectNavigation) i [režima pretraživanja](#BrowseMode).
Ove pozicije su označene obojenim pravougaonikom.

* Čista plava boja označava kombinovano lokaciju sistemskog fokusa i navigacionog objekta (na primer zato što [navigacioni objekat prati sistemski fokus](#ReviewCursorFollowFocus)).
* Tamno plava boja označava objekat sistemskog fokusa.
* Ružičasta boja označava poziciju navigacionog objekta.
* Žuta boja označava poziciju virtuelnog kursora u režimu pretraživanja (gde nema fizičkog kursora na primer u Web pretraživačima).

Kada je Vizuelno označavanje omogućeno u [kategoriji vid](#VisionSettings) dijaloga [NVDA podešavanja](#NVDASettings), možete podesiti [da li treba označiti fokus, navigacioni objekat ili kursor režima pretraživanja](#VisionSettingsFocusHighlight).

### Zatamnjivanje ekrana {#VisionScreenCurtain}

Kao slep ili slabovid korisnik, često nije moguće ili potrebno da vidite sadržaj ekrana.
Takođe, može biti teško da budete sigurni da niko ne gleda u vaš sadržaj.
Za ovu situaciju, NVDA sadrži opciju koja se zove "zatamnjivanje ekrana" koja može biti omogućena da ekran bude crn.

Možete omogućiti zatamnjivanje ekrana u [kategoriji vid](#VisionSettings) dijaloga [NVDA podešavanja](#NVDASettings).

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Menja stanje zatamnjivanja ekrana |`NVDA+kontrol+escape` |Omogućite kako bi ekran postao crn ili onemogućite da prikažete sadržaj ekrana. Ako se pritisne jednom, zatamnjivanje ekrana će biti omogućeno dok ponovo ne pokrenete NVDA. Ako se pritisne dva puta, zatamnjivanje ekrana je omogućeno dok ga ne onemogućite.|

<!-- KC:endInclude -->

Kada je zatamnjivanje ekrana omogućeno neki zadaci koji zavise od sadržaja vidljivog na ekranu kao što su izvršavanje funkcije [OCR](#Win10Ocr) ili slikanje ekrana nisu mogući.

Zbog promene u API-u za Windows lupu, zatamnjivanje ekrana je ažurirano kako bi podržavalo najnovije Windows verzije.
Koristite NVDA 2021.2 da aktivirate zatamnjivanje ekrana na Windowsu 10 21H2 (10.0.19044) ili novijim.
Kako biste se uverili u vašu privatnost, kada koristite novu verziju Windowsa, vizuelno potvrdite da zatamnjivanje ekrana čini ekran potpuno crnim.

Imajte na umu da dok god je pokrenuta Windows lupa i koriste se obrnute boje ekrana, zatamnjivanje ekrana se ne može omogućiti.

## Prepoznavanje sadržaja {#ContentRecognition}

Kada autori ne pruže dovoljno informacija za korisnike čitača ekrana o sadržaju, razni alati se mogu koristiti za pokušaj prepoznavanja sadržaja sa slike.
NVDA podržava optičko prepoznavanje znakova (eng. OCR) funkciju koja je ugrađena u Windows 10 i noviji za prepoznavanje teksta sa slike.
Dodatni pružaoci prepoznavanja se mogu dobiti instaliranjem NVDA dodataka.

Kada koristite komandu za prepoznavanje sadržaja, NVDA prepoznaje sadržaj trenutnog [navigacionog objekta](#ObjectNavigation).
Po podrazumevanim podešavanjima, navigacioni objekat prati sistemski fokus ili kursor režima pretraživanja, tako da obično možete jednostavno da pomerite kursor na mesto na koje je potrebno.
Na primer, ako pomerite kursor režima pretraživanja na sliku, prepoznavanje će prepoznati tekst te slike po podrazumevanim podešavanjima.
Ali, možda ćete takođe želeti da koristite navigaciju objekata, da na primer, prepoznate sadržaj prozora cele aplikacije.

Kada je prepoznavanje završeno, rezultat će biti prikazan u dokumentu koji je sličan režimu pretraživanja, kako biste mogli da čitate informacije pomeranjem kursora, i drugim komandama.
Pritiskanje tastera enter aktivira (izvršava klik miša ) tekst na poziciji kursora ako je moguće.
Pritiskanje tastera ESC odbacuje rezultat prepoznavanja.

### Windows OCR {#Win10Ocr}

Windows 10 i novije verzije uključuju OCR za puno jezika.
NVDA može da koristi ovo za prepoznavanje teksta sa slika ili nepristupačnih aplikacija.

Možete podesiti jezik koji ćese koristiti za prepoznavanje u [Windows OCR kategoriji](#Win10OcrSettings) [NVDA podešavanja](#NVDASettings).
Dodatni jezici se mogu instalirati otvaranjem start menija, biranjem opcije podešavanja, zatim opcije vreme i jezik -> region i jezik a nakon toga izabrati opciju dodaj jezik.

Kada želite da gledate sadržaj koji se stalno menja, na primer gledanje videa sa titlovima, možete omogućiti automatsko osvežavanje prepoznatog sadržaja.
Ovo se takođe može uraditi u [Windows OCR kategoriji](#Win10OcrSettings) dijaloga [NVDA podešavanja](#NVDASettings).

Windows OCR može biti delimično ili potpuno nekompatibilan sa [NVDA vizuelnim poboljšanjima](#Vision) ili drugim vizuelnim pomoćnim alatima. Morate onemogućiti ove alate pre nego što započnete proces prepoznavanja.

<!-- KC:beginInclude -->
Da prepoznate tekst trenutnog navigacionog objekta koristeći Windows OCR, pritisnite NVDA+r.
<!-- KC:endInclude -->

## Posebne karakteristike za aplikacije {#ApplicationSpecificFeatures}

NVDA pruža određene dodatne karakteristike za neke aplikacije koje ili omogućavaju lakše izvršavanje određenog zadatka ili čine delove koji nisu bili pristupačni korisnicima čitača ekrana aplikacije pristupačnim.

### Microsoft Word {#MicrosoftWord}
#### Automatsko čitanje zaglavlja kolona i redova {#WordAutomaticColumnAndRowHeaderReading}

NVDA može automatski čitati zaglavlja redova i kolona tabela u programu Microsoft Word.
 Ovo zahteva da opcija prijavi zaglavlja redova/kolona iz kategorije formatiranje dokumenta, koja se nalazi u [NVDA podešavanjima](#NVDASettings) bude uključena.

Ako koristite [UIA za pristup Word dokumentima](#MSWordUIA), što je podrazumevano podešavanje u novijim Word i Windows verzijama, ćelije prvog reda će automatski biti smatrane zaglavljima kolone; slično tome, ćelije prve kolone će automatski biti smatrane zaglavljima redova.

Sa druge strane, ako ne koristite [UIA za pristup Word dokumentima](#MSWordUIA), moraćete da označite programu NVDA koji red ili kolona sadrži zaglavlja u svakoj tabeli.
Nakon što dođete do prve ćelije koja sadrži zaglavlja redova i kolona, koristite jednu od sledećih komandi:
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Postavi zaglavlja kolona |NVDA+šift+c |Ako se pritisne jednom govori programu NVDA da je ovo prva ćelija koja sadrži red sa zaglavljem kolona, koja treba automatski biti izgovorena kada se pomerate ispod kolona ovog reda. Pritiskanje dva puta briše podešavanje.|
|Podesi zaglavlje redova |NVDA+šift+r |Ako se pritisne jednom govori programu NVDA da je ovo prva ćelija koja sadrži kolone zaglavlja redova, Što treba automatski biti izgovoreno kada se krećete između kolona ovog reda. Pritiskanje dva puta briše podešavanje.|

<!-- KC:endInclude -->
Ova podešavanja se čuvaju u dokumentu kao markeri i kompatibilna su sa drugim čitačima ekrana kao što je Jaws.
Ovo znači da korisnici drugih čitača ekrana koji kasnije otvore ovaj dokument već imaju podešena zaglavlja redova i kolona.

#### Režim pretraživanja u programu Microsoft Word {#BrowseModeInMicrosoftWord}

Slično Webu, režim pretraživanja može da se koristi u programu Microsoft Word u cilju brze navigacije i pristupu liste elemenata.
<!-- KC:beginInclude -->
Da uključite ili isključite režim pretraživanja u programu Microsoft Word, pritisnite NVDA+razmak.
<!-- KC:endInclude -->
Za dodatne informacije o režimu pretraživanja i brzoj navigaciji, pogledajte [deo režim pretraživanja](#BrowseMode).

##### Lista elemenata {#WordElementsList}

<!-- KC:beginInclude -->
Dok ste u režimu pretraživanja u programu Microsoft Word, možete pristupiti listi elemenata komandom NVDA+f7.
Lista elemenata može prikazati naslove, linkove, napomene (što uključuje komentare i praćenje izmena) i greške(trenutno ograničeno na greške u pravopisu).
<!-- KC:endInclude -->

#### Prijavljivanje komentara {#WordReportingComments}

<!-- KC:beginInclude -->
Da čujete bilo koji komentar na trenutnoj poziciji kursora, pritisnite NVDA+alt+c.
<!-- KC:endInclude -->
Svi komentari za dokument, zajedno sa drugim ispraćenim promenama, mogu se takođe prikazati u listi elemenata kada izaberete napomene kao tip elemenata.

### Microsoft Excel {#MicrosoftExcel}
#### Automatsko čitanje zaglavlja redova i kolona {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA može automatski izgovarati ispravna zaglavlja redova i kolona kada se krećete kroz Excel radne listove.
Kao prvo, ovo zahteva da opcija prijavi zaglavlja redova/kolona u kategoriji formatiranje dokumenta, koja se nalazi u [NVDA podešavanjima](#NVDASettings) bude uključena.
Takođe, NVDA mora da zna koje kolone ili redovi sadrže zaglavlje tabele.
Nakon što dođete do prve ćelije koja sadrži zaglavlja redova i kolona, koristite jednu od sledećih komandi:
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Postavi zaglavlja kolona |NVDA+šift+c |Ako se pritisne jednom govori programu NVDA da je ovo prva ćelija koja sadrži red sa zaglavljem kolona, koja treba automatski biti izgovorena kada se pomerate ispod kolona ovog reda. Pritiskanje dva puta briše podešavanje.|
|Podesi zaglavlje redova |NVDA+šift+r |Ako se pritisne jednom govori programu NVDA da je ovo prva ćelija koja sadrži kolone zaglavlja redova, Što treba automatski biti izgovoreno kada se krećete između kolona ovog reda. Pritiskanje dva puta briše podešavanje.|

<!-- KC:endInclude -->
Ova podešavanja će biti upisana u radnu svesku i biti kompatibilna sa drugim čitačima ekrana kao što je Jaws.
Ovo znači da korisnici drugih čitača ekrana koji kasnije otvore ovu radnu svesku automatski imaju zaglavlja redova i kolona podešena. 

#### Lista elemenata {#ExcelElementsList}

Slično Webu, NVDA ima listu elemenata za Microsoft excel koja vam dozvoljava pristup različitim vrstama informacija.
<!-- KC:beginInclude -->
Da pristupite listi elemenata u programu Excel, pritisnite NVDA+f7.
<!-- KC:endInclude -->
Različite vrste informacija u listi elemenata su:

* Grafikoni: Ovo prikazuje sve grafikone na aktivnom radnom listu. 
Izbor grafikona i pritiskanje tastera enter ili aktiviranje dugmeta za pomeranje na element fokusira grafikon za čitanje i navigaciju sa strelicama.
* Komentari: Ovo prikazuje sve ćelije na aktivnom radnom listu koje sadrže komentare. 
Adresa ćelije je prikazana zajedno sa njenim komentarom. 
Pritiskanje entera ili dugmeta za pomeranje na element će vas prebaciti na tu ćeliju.
* Formule: Ovo prikazuje sve ćelije na trenutnom radnom listu koje sadrže formule. 
Adresa ćelije je prikazana zajedno sa formulom za svaku ćeliju.
Pritiskanje entera ili dugmeta za pomeranje na element će vas prebaciti na tu ćeliju. 
* Listovi: Ovo prikazuje sve listove u trenutnoj radnoj svesci. 
Pritiskanje tastera f2 na nekom od listova vam dozvoljava da preimenujete list. 
Pritiskanje entera ili dugmeta za pomeranje na element vam dozvoljava da pređete na taj list.
* Polja za unos: Ovo prikazuje sva polja za unos na trenutnom listu.
Za svako polje, lista elemenata prikazuje alternativan tekst polja zajedno sa adresama ćelija koje pokriva.
Pritiskanje entera ili dugmeta za pomeranje na element vas prebacuje na to polje u režimu pretraživanja.

#### Prijavljivanje napomena {#ExcelReportingComments}

<!-- KC:beginInclude -->
Da čujete sve napomene za trenutno fokusiranu ćeliju, pritisnite NVDA+alt+c.
U Microsoft 2016, 365 i novijim office verzijama, komentari u programu Microsoft Excel su preimenovani u "napomene".
<!-- KC:endInclude -->
Sve napomene za radni list se takođe mogu prikazati u NVDA listi elemenata nakon što pritisnete NVDA plus f7.

NVDA može takođe da prikaže poseban dijalog za dodavanje ili uređivanje određene napomene.
NVDA menja podrazumevani Excel dijalog zbog problema u pristupačnosti, ali je prečica za prikazivanje dijaloga preuzeta iz Excela što znači da takođe radi bez programa NVDA.
<!-- KC:beginInclude -->
Da biste dodali ili uredili određenu napomenu, u fokusiranoj ćeliji, pritisnite šift+f2.
<!-- KC:endInclude -->

Ova prečica se ne pojavljuje i ne može se promeniti u NVDA dijalogu za ulazne komande.

Napomena: Moguće je takođe otvoriti region za uređivanje napomena iz kontekstnog menija Excela u bilo kojoj ćeliji.
Ali, ovo će otvoriti nepristupačan region za uređivanje a ne dijalog programa NVDA.

U Microsoft Office 2016, 365 i novijim verzijama, novi stil dijaloga za komentare je dodat.
Ovaj dijalog je pristupačan i nudi dodatne opcije kao što su odgovaranje na komentare, i slično.
Takođe se može otvoriti iz kontekstnog menija određene ćelije.
Komentari koji se dodaju iz novog dijaloga nisu vezani za "napomene".

#### Čitanje zaštićenih ćelija {#ExcelReadingProtectedCells}

Ako je radna sveska zaštićena, neće biti moguće pomeranje fokusa na ćelije koje su zaključane za uređivanje.
<!-- KC:beginInclude -->
Da biste dozvolili pomeranje na zaključane ćelije, prebacite se u režim pretraživanja pritiskajući NVDA+space, a zatim koristite standardne Excel komande za kretanje kao što su strelice za pomeranje na sve ćelije na trenutnom radnom listu.
<!-- KC:endInclude -->

#### Polja za unos {#ExcelFormFields}

Excel radni listovi mogu da sadrže polja za unos.
Možete da im pristupite iz liste elemenata ili tasterima f i šift+f u navigaciji jednim slovom.
Nakon što dođete do polja za unos u režimu pretraživanja, možete da pritisnete enter ili razmak da aktivirate kontrolu ili pređete u režim fokusiranja, u zavisnosti od kontrole.
Za dodatne informacije o režimu pretraživanja i navigaciji jednim slovom, pročitajte [deo režim pretraživanja](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Uključi i isključi čitanje napomena za predavača |kontrol+šift+s |Kada ste u slajd šou koji je pokrenut, ova komanda prebacuje između čitanja napomena za predavača i čitanja slajdova. Ovo uključuje samo šta NVDA čita, a ne šta je prikazano na ekranu.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Prijavi preostalo vreme |Kontrol+šift+r |Prijavljuje preostalo vreme zapisa koji se trenutno reprodukuje, ukoliko se nešto reprodukuje.|
|Prijavi proteklo vreme |Kontrol+Šift+e |Prijavljuje proteklo vreme zapisa koji se trenutno reprodukuje, ako se neki zapis reprodukuje.|
|Prijavi trajanje zapisa |Kontrol+šift+t |Prijavljuje ukupno trajanje zapisa koji se trenutno reprodukuje, ako se neki zapis reprodukuje.|

<!-- KC:endInclude -->

Napomena: Prečice opisane iznad rade samo sa podrazumevanim formatom statusne trake programa Foobar2000.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Prijavi jednu od poslednjih poruka |NVDA+kontrol+1-4 |Prijavljuje jednu od poslednjih poruka, u zavisnosti od pritisnutog broja; Na primer NVDA+kontrol+2 čita drugu najnoviju poruku.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA nudi poboljšanu podršku za Poedit 3.4 ili noviji.

<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Prijavi napomene za prevodioce |`Kontrol+šift+a` |Prijavljuje sve napomene za prevodioce. Ako se pritisne dva puta, prikazuje napomene u režimu pretraživanja|
|Prijavi komentar |`Kontrol+šift+c` |Prijavljuje bilo koji komentar u prozoru sa komentarima. Ako se pritisne dva puta, prikazuje komentar u režimu pretraživanja|
|Prijavi stari izvorni tekst |`kontrol+šift+o` |Prijavljuje stari izvorni tekst, ako postoji. Ako se pritisne dva puta, prikazuje tekst u režimu pretraživanja|
|Prijavi upozorenje za prevod |`kontrol+šift+w` |Prijavljuje upozorenje za prevod, ako postoji. Ako se pritisne dva puta, prikazuje upozorenje u režimu pretraživanja|

<!-- KC:endInclude -->

### Kindle za PC {#Kindle}

NVDA Podržava čitanje knjiga u programu Amazon Kindle za PC.
Ovo je dostupno samo za knjige sa oznakom "čitač ekrana: Podržan" što možete da proverite na stranici sa detaljima knjige.

Režim pretraživanja se koristi za čitanje knjiga.
Automatski je omogućen kada otvorite knjigu ili se fokusirate na prostor knjige.
Stranice se automatski menjaju kada pomerate kursor ili koristite komandu izgovori sve.
<!-- KC:beginInclude -->
Možete ručno preći na prethodnu stranicu tasterom page up ili na sledeću tasterom page down.
<!-- KC:endInclude -->

Navigacija jednim slovom je podržana za slike i linkove, ali samo na trenutnoj stranici.
Navigacija linkovima takođe uključuje fusnote.

NVDA pruža ranu podršku za čitanje i interakciju sa matematičkim sadržajem u knjigama sa pristupačnom matematikom.
Molimo pogledajte deo [čitanje matematičkog sadržaja](#ReadingMath) za dodatne informacije.

#### Izbor teksta {#KindleTextSelection}

Kindle vam dozvoljava više različitih funkcija sa izabranim tekstom, uključujući pretragu definicije iz rečnika, dodavanje napomena i obeležavanje, kopiranje teksta u privremenu memoriju i pretraga Weba.
Da to uradite, izaberite tekst kao i obično u režimu pretraživanja korišćenjem tastera šift i tastera za pomeranje kursora.
<!-- KC:beginInclude -->
Kada izaberete tekst, pritisnite aplikacioni taster ili šift+f10 kako biste prikazali opcije za rad sa odabranim tekstom.
<!-- KC:endInclude -->
Ako uradite ovo kada nema izabranog teksta, opcije će biti prikazane za reč na kojoj se nalazi kursor.

#### Korisničke napomene {#KindleUserNotes}

Možete dodati napomenu za reč ili deo teksta.
Da uradite ovo, prvo izaberite željen tekst i pristupite opcijama izbora koje su opisane iznad.
Zatim, izaberite dodaj napomenu.

Kada čitate u režimu pretraživanja, NVDA smatra ove napomene kao komentare.

Da prikažete, uredite ili obrišete napomenu:

1. Prebacite kursor na tekst koji sadrži napomenu.
1. Pristupite opcijama izbora koje su opisane iznad.
1. Izaberite uredi napomenu.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Kada ste u prikazu tabele dodatih knjiga:

| Ime |Komanda |Opis|
|---|---|---|
|Enter |enter |Otvara izabranu knjigu.|
|Kontekstni meni |Aplikacioni taster |Otvara kontekstni meni za izabranu knjigu.|

<!-- KC:endInclude -->

### Windows konzola {#WinConsole}

NVDA pruža podršku za Windows komandne konzole koje koriste Windows komandna linija, PowerShell, i Windows podsistem za Linux.
Prozor konzole je fiksne veličine, obično mnogo manji od dela koji sadrži izlaz.
Dok se novi tekst piše, sadržaj se pomera i prethodni tekst postaje nevidljiv. 
Na Windows verzijama starijim od Windowsa 11 22H2, tekst koji nije vidljiv u prozoru nije dostupan kada se koriste komande NVDA pregleda.
Zbog toga, neophodno je da pomerite prozor konzole kako biste videli raniji tekst.
U novijim verzijama konzole i Windows terminala, moguće je u potpunosti pregledati tekst bez potrebe za pomeranjem prozora.
<!-- KC:beginInclude -->
Sledeće ugrađene prečice u Windows konzoli mogu biti korisne kada se [pregleda tekst](#ReviewingText) uz NVDA u starijim verzijama Windows konzole:

| Ime |Komanda |Opis|
|---|---|---|
|Pomeri gore |kontrol+StrelicaGore |Pomera prozor konzole gore, kako bi stariji tekst mogao da se pročita.|
|Pomeri dole |kontrol+StrelicaDole |Pomera prozor konzole dole, kako bi noviji tekst mogao da se pročita.|
|Pomeri na početak |kontrol+home |Pomera prozor konzole na početak teksta.|
|Pomeri na kraj |kontrol+end |Pomera prozor konzole na kraj teksta.|

<!-- KC:endInclude -->

## Podešavanje programa NVDA {#ConfiguringNVDA}

Većina podešavanja programa NVDA može se menjati kroz dijaloge kojima se pristupa iz pod menija opcije iz NVDA menija.
Puno ovih podešavanja se može pronaći u [dijalogu NVDA podešavanja sa više kartica](#NVDASettings).
U svim dijalozima, pritisnite dugme u redu da prihvatite promene koje ste izvršili.
Da otkažete promene, pritisnite dugme otkaži ili taster escape.
Za određene dijaloge, možete pritisnuti dugme primeni kako bi podešavanja bila primenjena odmah bez zatvaranja dijaloga.
Većina NVDA dijaloga podržava pomoć osetljivu na trenutni sadržaj.
<!-- KC:beginInclude -->
Kada ste u dijalogu, pritiskanje tastera  `f1` otvara korisničko uputstvo na pasusu koji je vezan za fokusirano podešavanje ili trenutni dijalog.
<!-- KC:endInclude -->
Neka podešavanja takođe mogu biti promenjena korišćenjem prečica, koje su prikazane u sekcijama ispod.

### NVDA podešavanja {#NVDASettings}

<!-- KC:settingsSection: || Ime | Desktop komanda | Laptop komanda | opis | -->
NVDA nudi puno parametara za podešavanje koji se mogu promeniti iz dijaloga podešavanja.
Kako biste lakše pronašli vrstu podešavanja koju želite da promenite, dijalog prikazuje listu sa kategorijama podešavanja iz koje možete izabrati neku od njih .
Kada izaberete kategoriju, sva podešavanja vezana za tu kategoriju će se prikazati u dijalogu.
Da biste se kretali između kategorija, koristite `tab` ili `šift+tab` da dođete do liste kategorija, a zatim koristite strelice gore i dole da se krećete po listi.
Bilo gde iz dijaloga, možete takođe da pređete na sledeću kategoriju prečicom `ctrl+tab`, ili na prethodnu prečicom `šift+ctrl+tab`.

Nakon što promenite jedno ili više podešavanja, podešavanja se mogu  primeniti aktiviranjem dugmeta primeni, u tom slučaju će dijalog ostati otvoren, što će vam dozvoliti da promenite druga podešavanja ili pređete na drugu kategoriju.
Ako želite da sačuvate podešavanja i zatvorite dijalog, možete koristiti taster u redu.

Neke kategorije podešavanja imaju dodeljenu prečicu.
Ako se pritisne, ta prečica će otvoriti NVDA dijalog za podešavanja direktno u  toj kategoriji.
Po podrazumevanim podešavanjima, ne možete pristupiti svim kategorijama korišćenjem prečica.
Ako često pristupate kategorijama podešavanja koje nemaju dodeljenu prečicu, možda ćete želeti da iskoristite [dijalog ulaznih komandi](#InputGestures) da biste dodali prilagođenu prečicu kao što je prečica na tastaturi ili pokret na ekranu osetljivom na dodir za tu kategoriju.

Kategorije koje su dostupne u dijalogu NVDA podešavanja će biti opisane ispod.

#### Opšta {#GeneralSettings}

<!-- KC:setting -->

##### Otvori opšta podešavanja {#toc110}

Prečica: `NVDA+kontrol+g`

Opšta kategorija NVDA dijaloga podešavanja podešava celokupno ponašanje programa NVDA kao što je jezik interfejsa i da li treba da proverava ažuriranja.
Ova kategorija sadrži sledeće opcije:

##### Jezik {#GeneralSettingsLanguage}

Ovo je izborni okvir koji vam dozvoljava da izaberete jezik interfejsa i poruka programa NVDA.
Postoji puno jezika, ali podrazumevana opcija je"Korisnički podrazumevani, Windows".
Ova opcija govori programu NVDA da koristi onaj jezik na kojem je Windows trenutno.

Napomena da NVDA mora biti ponovo pokrenut kada menjate jezik.
Kada se pojavi dijalog za potvrdu, izaberite "ponovo pokreni odmah" ili "ponovo pokreni kasnije" ako želite da koristite novi jezik odmah ili kasnije. Ako je opcija "ponovo pokreni kasnije" izabrana, podešavanja moraju biti sačuvana (ili ručno ili tako što će opcija sačuvaj podešavanja pri izlazu biti omogućena).

##### Sačuvaj podešavanja pri izlazu {#GeneralSettingsSaveConfig}

Ova opcija je izborno polje koje, kada je označeno, govori programu NVDA da automatski sačuva podešavanja pri izlazu.

##### Prikazivanje dodatnih opcija kada izađete iz programa NVDA {#GeneralSettingsShowExitOptions}

Ova opcija je izborno polje koje kontroliše da li pri izlazu treba da se pokaže dijalog koji vas pita šta želite da uradite.
Kada je označeno, dijalog će se pojaviti kada izađete iz programa NVDA koji vas pita da li želite da izađete, ponovo pokrenete program, ponovo pokrenete program bez dodataka ili instalirate odložena ažuriranja (ako postoje).
Kada nije označeno, NVDA će odmah izaći.

##### Reprodukuj zvukove kada se NVDA zaustavlja i pokreće {#GeneralSettingsPlaySounds}

Ova opcija je izborno polje koje, kada je označeno, govori programu NVDA da reprodukuje zvukove kada se pokreće ili zaustavlja.

##### Nivo evidentiranja u dnevniku {#GeneralSettingsLogLevel}

Ovo je izborni okvir koji vam dozvoljava da izaberete koliko će evidencije NVDA voditi u svom dnevniku dok je pokrenut.
Obično korisnici ovo ne treba da menjaju kako se nebi evidentiralo previše informacija.
Ali, ako želite da pružite dodatne informacije kada prijavljujete grešku, ili omogućite i u potpunosti onemogućite evidentiranje, može biti korisna opcija.

Dostupni nivoi evidentiranja su:

* Onemogućeno: Osim kratke poruke o pokretanju, NVDA neće ništa evidentirati dok je pokrenut.
* Info: NVDA će evidentirati osnovne informacije kao što su poruke o pokretanju i ostale informacije korisne za programere.
* Upozorenja o otklanjanju grešaka: Poruke upozorenja koje nisu izazvane velikim greškama će biti evidentirane.
* Ulaz/ izlaz: Unos sa tastature i brajevog reda, kao i govorni i brajev izlaz će biti evidentirani.
Ako ste zabrinuti za vašu privatnost, ne podešavajte nivo evidentiranja na ovu opciju.
* Ispravljanje greške: Uz informacije, upozorenja, ulazne i izlazne poruke, dodatne poruke o otklanjanju grešaka će biti evidentirane.
Kao i ulaz/izlaz, ako vas brine privatnost, nebi trebalo da podešavate evidentiranje na ovu opciju.

##### Automatski pokreni NVDA nakon što se prijavim u Windows {#GeneralSettingsStartAfterLogOn}

Ako je ova opcija omogućena, NVDA će se pokrenuti odmah nakon što se prijavite u Windows.
Ova opcija je dostupna samo za instalirane kopije programa NVDA.

##### Koristi NVDA na Windows ekranu za prijavljivanje (zahteva administratorske privilegije) {#GeneralSettingsStartOnLogOnScreen}

Ako se prijavljujete u Windows upisivanjem korisničkog imena i lozinke, omogućavanjem ove opcije NVDA će se pokrenuti na ekranu za prijavljivanje.
Ova opcija je dostupna samo za instalirane kopije programa NVDA.

##### Koristi trenutno sačuvana podešavanja na ekranu za prijavljivanje i drugim bezbednosnim ekranima (zahteva administratorske privilegije ) {#GeneralSettingsCopySettings}

Pritiskanje ovog dugmeta kopira trenutno sačuvana podešavanja programa NVDA u folder sistemskih podešavanja, tako da NVDA može da ih koristi kada je pokrenut na ekranu za prijavljivanje, ekranu kontrole korisničkog naloga(UAC) i drugim [bezbednim ekranima](#SecureScreens).
Da se uverite da su sva vaša podešavanja uspešno prebačena, prvo sačuvajte vaša podešavanja prečicom kontrol+NVDA+c ili opciom sačuvaj podešavanja u NVDA meniju.
Ova opcija je dostupna samo za instalirane kopije programa NVDA.

##### Automatski proveri dostupna ažuriranja za NVDA {#GeneralSettingsCheckForUpdates}

Ako je ovo omogućeno, NVDA će automatski proveravati novija ažuriranja i obavestiće vas ako je novije ažuriranje dostupno.
Možete takođe ručno proveriti ažuriranja izborom opcije proveri ažuriranja u meniju pomoć NVDA menija.
Kada ručno ili automatski proveravate ažuriranja, neophodno je poslati određene informacije NVDA serverima za ažuriranje kako biste dobili ispravno ažuriranje za vaš sistem.
Sledeće informacije se uvek šalju: 

* Trenutna NVDA verzija
* Verzija operativnog sistema
* Da li je operativni sistem 64 ili 32 bitni

##### Dozvoli organizaciji NV Access prikupljanje statistika korišćenja programa NVDA {#GeneralSettingsGatherUsageStats}

Ako je ova opcija omogućena, NV Access će koristiti informacije iz provera ažuriranja za praćenje broja NVDA korisnika uključujući određena svojstva kao što su verzije operativnih sistema ili država iz kojih dolaze.
Napomena da iako će vaša IP adresa biti poslata za određivanje države u toku provere ažuriranja, IP adresa se nikada ne čuva.
Pored osnovnih informacija neophodnih za proveru ažuriranja, sledeće dodatne informacije se takođe trenutno šalju:

* Jezik NVDA interfejsa
* Da li je ova kopija programa NVDA prenosna ili instalirana
* Ime sintetizatora koji se trenutno koristi (uključujući ime dodatka od kog dolazi drajver)
* Ime brajevog reda koji se trenutno koristi (uključujući ime dodatka od kog dolazi drajver)
* Trenutna izlazna brajeva tabela (ako se koristi brajev red)

Ove informacije puno pomažu organizaciji NV Access da odredi buduće prioritete u razvoju programa NVDA.

##### Obavesti za odložena ažuriranja pri pokretanju {#GeneralSettingsNotifyPendingUpdates}

Ako je ova opcija omogućena, NVDA će vas obavestiti kada imate odloženo ažuriranje pri pokretanju, i ponuditi vam mogućnost instalacije.
Takođe možete ručno instalirati ažuriranje iz dijaloga izlaza (ako je omogućen ), iz NVDA menija, ili kada izvršite novu proveru iz menija pomoći.

#### Podešavanja govora {#SpeechSettings}

<!-- KC:setting -->

##### Otvori podešavanja govora {#toc123}

Prečica: `NVDA+kontrol+v`

Kategorija govor dijaloga NVDA podešavanja sadrži opcije koje vam dozvoljavaju da promenite sintetizatora govora kao i karakteristike glasa izabranog sintetizatora.
Za brži način menjanja opcija govora bilo gde da se nalazite, pročitajte deo [brže menjanje podešavanja sintetizatora](#SynthSettingsRing) .

Kategorija govor sadrži sledeće opcije:

##### Promena sintetizatora {#SpeechSettingsChange}

Prva opcija u kategoriji govor je dugme promeni... Ovo dugme aktivira [dijalog za izbor sintetizatora](#SelectSynthesizer), koji vam dozvoljava da izaberete aktivnog sintetizatora i izlazni uređaj.
Ovaj dijalog se otvara iznad postojećeg NVDA dijaloga podešavanja.
Čuvanje ili odbacivanje podešavanja u dijalogu za izbor sintetizatora vas vraća u dijalog NVDA podešavanja.

##### Glas {#SpeechSettingsVoice}

Opcija glas je izborni okvir koji prikazuje sve glasove trenutno instaliranog i podešenog sintetizatora.
Možete koristiti strelice da čujete različite glasove.
Strelice levo i gore vas pomeraju gore u listi, dok vas strelice desno i dole pomeraju dole u listi.

##### Varijanta {#SpeechSettingsVariant}

Ako koristite sintetizator Espeak NG koji dolazi uz NVDA, ovo je izborni okvir uz pomoć kojeg birate varijantu kojom sintetizator treba da govori.
Varijante sintetizatora Espeak NG su više kao glasovi, zbog toga što oni pružaju izmenjene atribute Espeak NG glasu.
Neke varijante će zvučati kao muškarac, neke kao žena, a neke čak i kao žaba.
Ako koristite neki drugi sintetizator, možda ćete takođe moći da promenite ovu vrednost ako je izabrani glas podržava.

##### Brzina {#SpeechSettingsRate}

Ova opcija vam dozvoljava da promenite brzinu glasa.
Ovo je klizač koji ide od 0 do 100 - 0 najsporije, a 100 je najbrže.

##### Povećanje brzine {#SpeechSettingsRateBoost}

Kada je ova opcija omogućena značajno će povećati brzinu glasa, ako je podržana od strane trenutnog sintetizatora.

##### Visina {#SpeechSettingsPitch}

Ova opcija vam dozvoljava da promenite visinu trenutnog glasa.
To je klizač koji ide od 0 do 100 - 0 najniža visina a 100 je najviša.

##### Jačina {#SpeechSettingsVolume}

Ova opcija je klizač koji ide od 0 do 100 - 0 minimalna jačina a 100 maksimalna jačina.

##### Modulacija {#SpeechSettingsInflection}

Ova opcija je klizač koji vam dozvoljava da izaberete sa kojom modulacijom(menjanje intonacije) sintetizator treba da govori.

##### Automatska promena jezika {#SpeechSettingsLanguageSwitching}

Ova opcija je izborno polje koje kontroliše da li izabrani sintetizator treba da menja svoj jezik kada se čita tekst koji je prikazao jezik.
Ova opcija je omogućena po podrazumevanim podešavanjima.

##### Automatska promena dijalekta {#SpeechSettingsDialectSwitching}

Ovo izborno polje vam dozvoljava da kontrolišete da li se dijalekt treba menjati, a ne samo jezik.
Na primer, ako čitate tekst na Američkom Engleskom ali dokument je na Britanskom Engleskom, sintetizator će promeniti akcenat ako je ova opcija omogućena.
Ova opcija je onemogućena po podrazumevanim podešavanjima.

<!-- KC:setting -->

##### Nivo izgovora znakova interpunkcije/simbola {#SpeechSettingsSymbolLevel}

Komanda: NVDA+p

Ovo vam dozvoljava da izaberete količinu simbola koji trebaju biti izgovoreni kao reči.
Na primer, kada je opcija podešena na sve simbole, svi simboli će biti izgovoreni kao reči.
Ova opcija se primenjuje na sve sintetizatore, ne samo na trenutno aktivnog sintetizatora.

##### Koristi jezik glasa za obradu znakova i simbola {#SpeechSettingsTrust}

Uključena po podrazumevanim podešavanjima, ova opcija govori programu NVDA da li treba koristiti jezik trenutnog glasa za izgovor simbola.
Ako primetite da NVDA čita simbole na pogrešnom jeziku za trenutni glas, možda ćete želeti da isključite ovu opciju kako bi NVDA koristio svoj podrazumevani jezik.

##### Koristi podatke iz baze podataka Unicode Consortium data (uključujući emoji znakove) kada se obrađuju znakovi i simboli {#SpeechSettingsCLDR}

Kada je ovo izborno polje označeno, NVDA će uključiti dodatne rečnike prilikom izgovaranja znakova i simbola.
Ovi rečnici sadrže opise za simbole (posebno Emoji znakove) koje pruža [Unicode Consortium](https://www.unicode.org/consortium/) kao deo njihove [baze podataka](http://cldr.unicode.org/).
Ako želite da NVDA izgovara opise emoji znakova iz ove baze, omogućite ovu opciju.
Ali, ako koristite sintetizator govora koji već podržava opise emoji znakova, možda ćete želeti da isključite ovu opciju.

Napomena da se ručno dodani ili uređeni simboli čuvaju kao korisnička podešavanja.
Zbog toga, ako promenite opis određenog emoji znaka, vaš opis će se čitati bez obzira na to da li je ova opcija omogućena ili ne.
Možete dodati, urediti ili ukloniti opise simbola u [dijalogu izgovor znakova interpunkcije/simbola](#SymbolPronunciation).

Da uključite ili isključite korišćenje Unicode Consortium podataka bilo gde, molimo podesite prilagođenu prečicu korišćenjem [dijaloga ulazne komande](#InputGestures).

##### Procenat promene visine za velika slova {#SpeechSettingsCapPitchChange}

Ovo polje za unos teksta vam dozvoljava da upišete vrednost u kojoj visina glasa treba da se menja za velika slova.
Ova vrednost je procenat, gde negativna vrednost smanjuje visinu a pozitivna je povećava.
Ako ne želite promene u visini možete upisati 0.
Obično, NVDA malo poveća visinu za svako veliko slovo, ali neki sintetizatori možda ovo ne podržavaju.
U slučaju da menjanje visine nije podržano, možete koristiti [Izgovori reč veliko pre velikog slova](#SpeechSettingsSayCapBefore) ili [ Pišti za velika slova](#SpeechSettingsBeepForCaps) umesto ovoga.

##### Izgovori "Veliko" pre velikog slova {#SpeechSettingsSayCapBefore}

Ovo podešavanje je izborno polje koje, kada je označeno, govori programu NVDA da izgovori reč"veliko" pre svakog velikog slova kada se čita kao samostalan znak na primer u toku sricanja.

##### Pišti za velika slova {#SpeechSettingsBeepForCaps}

Ako je ovo izborno polje označeno, NVDA će reprodukovati zvučni signal kada naiđe na veliko slovo.

##### Iskoristi funkciju sricanja ako je podržana {#SpeechSettingsUseSpelling}

Neke reči sadrže samo jedno slovo, ali izgovor se razlikuje u zavisnosti od toga da li se znak izgovara kao jedan znak(kao u toku sricanja) ili reč.
Na primer, na Engleskom, "a" je reč i slovo i izgovara se različito u oba slučaja.
Ova opcija dozvoljava sintetizatoru da razlikuje ova dva slučaja ako sintetizator to podržava.
Većina sintetizatora ovo podržava.

Ova opcija bi obično trebala da bude omogućena.
Ali, neki Microsoft Speech API sintetizatori ne podržavaju ovo i čudno se ponašaju kada je opcija omogućena.
Ako imate probleme sa izgovorom pojedinačnih slova, pokušajte da onemogućite ovu opciju.

##### Odloženi opisi znakova pri pomeranju kursora {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Omogućeno, onemogućeno|
|Podrazumevano |Onemogućeno|

Kada je ovo podešavanje označeno, NVDA će izgovarati opise znakova kada se krećete znak po znak.

Na primer, kada se red čita znak po znak, kada se slovo "b" pročita NVDA će izgovoriti "Beograd" nakon odlaganja od jedne sekunde.
Ovo može biti korisno ako je teško razlikovati izgovor određenih simbola, ili za korisnike oštećenog sluha.

Odloženi opisi znakova će biti otkazani ako je drugi tekst izgovoren u toku ovog vremena, ili ako pritisnete taster `kontrol`.

##### Dostupni režimi za komandu koja kruži kroz režime govora {#SpeechModesDisabling}

Ova lista u kojoj se opcije mogu označiti dozvoljava da izaberete koji su [režimi govora](#SpeechModes) uključeni kada kružite kroz njih prečicom `NVDA+s`.
Režimi koji nisu označeni biće izuzeti.
Po podrazumevanim podešavanjima uključeni su svi režimi.

Na primer ako ne koristite režime  "sa pištanjem" i "isključen" možete onemogućiti ova dva, a zadržati "sa pričom" i "na zahtev" označenim.
Imajte na umu da je neophodno označiti bar dva režima.

#### Izbor sintetizatora {#SelectSynthesizer}

<!-- KC:setting -->

##### Otvori dijalog za izbor sintetizatora {#toc144}

Prečica: `NVDA+kontrol+s`

Dijalog izbor sintetizatora, koji se može otvoriti aktiviranjem dugmeta promeni... u kategoriji govor NVDA podešavanja, dozvoljava vam da izaberete kojeg sintetizatora NVDA treba da koristi za izgovaranje.
Nakon što izaberete vašeg sintetizatora, možete pritisnuti u redu i NVDA će učitati izabranog sintetizatora.
Ako dođe do greške prilikom učitavanja sintetizatora, NVDA će vas obavestiti porukom, i nastaviće da koristi prethodnog sintetizatora.

##### Sintetizator {#SelectSynthesizerSynthesizer}

Ova opcija vam dozvoljava da izaberete sintetizatora kojeg će NVDA koristiti za izgovor.

Za listu sintetizatora koje NVDA podržava, molimo pročitajte [sekciju podržani sintetizatori govora](#SupportedSpeechSynths).

Jedna posebna stavka koja će uvek biti u ovoj listi je "nema govora", koja vam dozvoljava da koristite NVDA bez govora.
Ovo može biti korisno za nekoga ko želi da koristi NVDA samo uz pomoć brajevog reda, ili za programere bez oštećenja vida koji žele da koriste samo preglednik govora.

#### Krug sintetizatora {#SynthSettingsRing}

Ako želite brzo da menjate podešavanja govora bez ulaza u kategoriju govor podešavanja programa NVDA, NVDA ima nekoliko komandi za pomeranje kroz neka od često korišćenih podešavanja govora:
<!-- KC:beginInclude -->

| Ime |Desktop komanda |Laptop komanda |Opis|
|---|---|---|---|
|Premesti se na naredno podešavanje govora |NVDA+kontrol+strelica desno |NVDA+šift+kontrol+strelica desno |Premešta se na naredno dostupno podešavanje govora, vraćajući se na prvo podešavanje nakon poslednjeg|
|Premesti se na prethodno podešavanje govora |NVDA+kontrol+strelica levo |NVDA+šift+kontrol+strelica levo |Premešta se na prethodno podešavanje govora, vraćajući se na poslednje podešavanje nakon prvog|
|Povećaj trenutno podešavanje govora |NVDA+kontrol+strelica gore |NVDA+šift+kontrol+strelica gore |Povećava trenutno podešavanje govora na kojem se nalazite. Na primer povećava brzinu, bira sledeći glas, pojačava ton|
|Povećaj trenutno podešavanje govora većim skokom |`NVDA+kontrol+pageUp` |`NVDA+šift+kontrol+pageUp` |Povećava vrednost trenutnog podešavanja govora na kojem se nalazite većim skokom. Na primer kada ste na podešavanju glasa, skočiće napred za dvadeset glasova; kada ste na podešavanjima klizača (brzina, visina, i tako dalje) povećaće vrednost za 20%.|
|Smanji trenutno podešavanje govora |NVDA+kontrol+strelica dole |NVDA+šift+kontrol+strelica dole |Smanjuje trenutno podešavanje govora na kojem se nalazite. Na primer smanjuje brzinu, bira prethodni glas, smanjuje ton|
|Smanji trenutno podešavanje govora većim skokom |`NVDA+kontrol+pageDown` |`NVDA+šift+kontrol+pageDown` |Smanjuje vrednost trenutnog podešavanja govora na kojem se nalazite većim skokom. Na primer kada ste na podešavanju glasa, skočiće nazad za dvadeset glasova; kada ste na podešavanjima klizača (brzina, visina, i tako dalje) smanjiće vrednost za 20%.|

<!-- KC:endInclude -->

#### Brajeva podešavanja {#BrailleSettings}

Kategorija brajeva podešavanja NVDA dijaloga za podešavanja sadrži nekoliko opcija koje vam dozvoljavaju da menjate izlazne i ulazne opcije prilikom korišćenja brajevog reda.
Ova kategorija sadrži sledeće opcije:

##### Promeni brajev red {#BrailleSettingsChange}

Dugme Promeni... u kategoriji brajeva podešavanja dijaloga NVDA podešavanja aktivira dijalog [izbor brajevog reda](#SelectBrailleDisplay), koji vam dozvoljava da izaberete aktivan brajev red.
Ovaj dijalog se otvara iznad već postojećeg NVDA dijaloga za podešavanja.
Čuvanje ili odbacivanje podešavanja u ovom dijalogu vas vraća u dijalog NVDA podešavanja.

##### Izlazna tabela {#BrailleSettingsOutputTable}

Sledeća opcija u ovoj kategoriji je izborni okvir izlazna tabela.
U ovom izbornom okviru, pronaćićete različite brajeve tabele za različite jezike, brajeve standarde i stepene.
Izabrana tabela će se koristiti za prevod teksta na brajevo pismo za prikazivanje na vašem brajevom redu.
Možete se pomerati po tabelama koristeći strelice.

##### Ulazna tabela {#BrailleSettingsInputTable}

Nakon prethodne opcije, sledeća opcija na koju ćete naići je izborni okvir za izbor ulazne tabele.
Izabrana tabela će se koristiti za prevođenje unetog teksta na brajevoj tastaturi u tekst.
Možete se pomerati kroz tabele sa strelicama.

Napomena da je ova opcija korisna samo ako vaš brajev red ima brajevu tastaturu i ako je ona podržana od strane odgovarajućeg drajvera.
Ako unos nije podržan na brajevom redu koji ima tastaturu, ovo će biti napomenuto u [delu podržani brajevi redovi](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Brajev režim {#BrailleMode}

Prečica: `NVDA+alt+t`

Ova opcija vam dozvoljava da izaberete brajev režim.

Trenutno, dostupna su dva brajeva režima, "Prati kursore" i "Prikaži govor".

Kada izaberete da brajev red prati kursore, brajev red će pratiti ili sistemski fokus/kursor ili navigacioni objekat/pregledni kursor, u zavisnosti od toga za šta je brajev red vezan.

Kada se izabere da brajev red prikazuje govor, brajev red će prikazati šta NVDA govori, ili šta bi govorio da je režim govora podešen na "Sa pričom".

##### Proširi na kompjuterski brajev kod za reč na poziciji kursora {#BrailleSettingsExpandToComputerBraille}

Ova opcija dozvoljava da reč na poziciji kursora bude prikazana na kompjuterskom brajevom kodu.

##### Prikaži kursor {#BrailleSettingsShowCursor}

Ova opcija dozvoljava da isključite i uključite brajev kursor.
Primenjuje se na sistemski i pregledni kursor, ali ne i na pokazivač izabranog teksta.

##### Treperenje kursora {#BrailleSettingsBlinkCursor}

Ova opcija dozvoljava brajevom kursoru da treperi.
Ako je treperenje isključeno, brajev kursor će uvek biti na"gornjoj" poziciji.
Ova opcija ne utiče na pokazivač izbora, uvek izbor pokazuju tačke 7 i 8 bez treperenja.

##### Brzina treperenja kursora(milisekunde) {#BrailleSettingsBlinkRate}

Ova opcija je brojčano polje koje vam dozvoljava da promenite brzinu treperenja kursora.

##### Oblik kursora za fokus {#BrailleSettingsCursorShapeForFocus}

Ova opcija vam dozvoljava da izaberete oblik(raspored tačaka) brajevog kursora kada brajev red prati fokus.
Ova opcija ne utiče na pokazivač izbora, uvek izbor pokazuju tačke 7 i 8 bez treperenja.

##### Oblik kursora za pregled {#BrailleSettingsCursorShapeForReview}

Ova opcija vam dozvoljava da izaberete oblik(raspored tačaka) brajevog kursora kada brajev red prati pregled.
Ova opcija ne utiče na pokazivač izbora, uvek izbor pokazuju tačke 7 i 8 bez treperenja.

##### Prikaži poruke {#BrailleSettingsShowMessages}

Ovo je izborni okvir koji vam omogućava da odredite da li će NVDA prikazivati brajeve poruke i kada će one nestati.

Da biste uključili ili isključili prikazivanje poruka bilo gde da se nalazite, molimo podesite prilagođenu prečicu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

##### Vreme isteka poruke (u sekundama) {#BrailleSettingsMessageTimeout}

Ova opcija je brojčano polje koje bira koliko dugo se poruke zadržavaju na brajevom redu.
NVDA poruka se odbacuje kada se pritisne dugme na brajevom redu koje prebacuje kursor, ali se ponovo pojavljuje kada se pritisne odgovarajući taster koji prikazuje poruku ponovo.
Ova opcija se prikazuje samo ako je opcija "Prikaži poruke" podešena na "Koristi vreme isteka".

<!-- KC:setting -->

##### Veži brajev red za {#BrailleTether}

Komanda: NVDA+control+t

Ova opcija vam dozvoljava da izaberete da li brajev red treba da prati sistemski fokus, navigacioni objekat/ pregledni kursor, ili oba.
Kada je opcija "Automatski" izabrana, NVDA će podrazumevano pratiti sistemski kursor.
U ovom slučaju, kada se pozicija preglednog kursora ili objektne navigacije promeni od strane korisnika, NVDA će privremeno vezati brajev red za pregled, dok fokus ili sistemski kursor ne promene poziciju.
Ako želite da samo prati fokus i sistemski kursor, morate da podesite brajev red da bude vezan za fokus.
U tom slučaju, brajev red neće pratiti NVDA pregledni kursor u toku objektne navigacije ili pregleda teksta.
Ako želite da umesto toga brajev red prati objektnu navigaciju i pregled teksta, morate da podesite brajev red da bude vezan za pregled.
U ovom slučaju, brajev red neće pratiti sistemski fokus i kursor.

##### Pomeranje sistemskog kursora kada se prebacuje pregledni kursor {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (nikada), nikada, samo pri automatskom vezivanju, uvek|
|Podrazumevano |Nikada|

Ovo podešavanje određuje da li sistemski kursor takođe treba da se pomera pritiskanjem tastera za prebacivanje.
Ova opcija je podrazumevano podešena na nikada, što znači da prebacivanje nikada neće pomerati kursor kada se prebacuje pregledni kursor.

Kada je ova opcija podešena na uvek, i [vezivanje brajevog reda](#BrailleTether) je podešeno na "automatski" ili "za pregled", pritiskanje tastera za prebacivanje kursora će takođe pomeriti sistemski kursor ili fokus kada je podržano.
Kada je trenutni režim pregleda [pregled ekrana](#ScreenReview), nema fizičkog kursora.
U tom slučaju, NVDA pokušava da se fokusira na objekat ispod teksta na koji se prebacujete.
Isto se primenjuje i na [pregled objekata](#ObjectReview).

Takođe možete da podesite ovu opciju da pomera kursor pri automatskom vezivanju.
U tom slučaju, pritiskanje tastera za prebacivanje kursora će pomeriti sistemski kursor ili fokus kada je NVDA vezan za pregledni kursor automatski, a do pomeranja neće doći kada je ručno vezan za pregledni kursor.

Ova opcija se prikazuje samo ako je "[Brajev red vezan](#BrailleTether)" "Automatski" ili "za pregled".

Da biste uključili pomeranje sistemskog kursora kada se prebacuje pregledni kursor bilo gde da se nalazite, molimo podesite prilagođenu komandu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

##### Čitaj po pasusima {#BrailleSettingsReadByParagraph}

Ako je omogućeno, brajevo pismo će se prikazivati po pasusima umesto po redovima.
Takođe, komande za sledeći i prethodni red će se pomerati po pasusima.
Ovo znači da ne morate da pomerate brajev red na kraju reda svaki put čak i kada više teksta može da stane na njemu.
Ovo može poboljšati čitanje dužih tekstova.
Onemogućeno je po podrazumevanim opcijama.

##### Izbegavaj razdvajanje reči kada je moguće {#BrailleSettingsWordWrap}

Ako je ovo omogućeno, reč koja je prevelika da stane na kraju brajevog reda se neće odvajati.
Umesto toga, ostaće određen prazan prostor na kraju reda.
Kada pomerite red, moćićete da pročitate celu reč.
Ovo se takođe zove"vraćanje reči".
Napomena da ako je reč prevelika da sama stane na brajev red, reč mora da se odvoji.

Ako je ovo onemogućeno, onoliko koliko je moguće će biti prikazano, ali ostatak će biti odvojen.
Kada pomerite red, moćićete da pročitate celu reč.

Uključivanje ove opcije može dozvoliti lepše čitanje, ali obično zahteva više pomeranja brajevog reda.

##### Predstavljanje sadržaja fokusa {#BrailleSettingsFocusContextPresentation}

Ova opcija vam dozvoljava da izaberete koje informacije NVDA treba da prikaže na brajevom redu kada neki objekat dobije fokus.
u informacije o sadržaju spada hierarhija objekata sa fokusom.
Na primer, kada se fokusirate na stavku liste, ova stavka liste je deo liste.
Ova lista može biti u dijalogu, i tako dalje.
Molimo pogledajte deo o [navigaciji objekata](#ObjectNavigation) za više informacija o hierarhiji koja važi za objekte u programu NVDA.

Kada je podešen da prikaže promene na brajevom redu, NVDA će pokušati da prikaže što je više informacija moguće na brajevom redu, ali samo za delove sadržaja koji su promenjeni.
Za primer iznad, ovo znači da kada prebacite fokus na listu, NVDA će prikazati stavku liste na brajevom redu.
Takođe, ako ima dovoljno prostora na brajevom redu, NVDA će pokazati da je stavka liste deo liste.
Ako nakon toga počnete da se krećete kroz listu koristeći strelice, podrazumeva se da znate da ste i dalje u listi.
Zbog toga, za preostale stavke na koje se fokusirate, NVDA će prikazati samo fokusiranu stavku na brajevom redu.
Kako biste mogli da pročitate sadržaj ponovo(npr. da ste u listi i da je lista deo dijaloga), morate da pomerite vaš brajev red nazad.

Kada je ova opcija podešena da uvek popuni brajev red, NVDA će pokušati da prikaže što je više informacija moguće na brajevom redu, bez obzira na to da li ste videli ove informacije ranije.
Ovo ima prednost da će NVDA uvek popuniti brajev red.
Ali, mana je da je mesto na kome je prikazan fokus na brajevom redu uvek različito.
Ovo može učiniti težim prelazak kroz veliku listu, na primer, budući da ćete stalno morati da pomerate prst da biste našli stavku.
Ovo je bilo podrazumevano podešavanje za NVDA 2017.2 i starije verzije.

Kada podesite opciju predstavljanja sadržaja fokusa da prikaže informacije o sadržaju samo kada pomerate brajev red unazad, NVDA nikada ne prikazuje informacije o sadržaju na brajevom redu.
Zbog toga, u primeru iznad, NVDA će prikazati da ste se fokusirali na stavku liste.
Ali, da biste pročitali sadržaj (npr. da ste u listi i da je lista deo dijaloga), moraćete da vratite brajev red unazad.

Da biste menjali opcije predstavljanja sadržaja fokusa bilo gde, molimo podesite komandu koristeći [dijalog ulazne komande](#InputGestures).

##### Prekini izgovor u toku pomeranja {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (omogućeno), omogućeno, onemogućeno|
|Podrazumevano |Omogućeno|

Ovo podešavanje određuje da li treba prekinuti govor kada se brajev red pomera napred ili nazad.
Komande pomeranja na prethodni ili sledeći red uvek prekidaju govor.

Dolazni govor može predstavljati ometanje pri čitanju brajevog pisma.
Zbog toga je opcija podrazumevano omogućena, što će prekinuti govor pri pomeranju brajevog reda.

Kada se ova opcija onemogući moguće je čuti govor i u isto vreme čitati brajevo pismo.

##### Prikaži izbor {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (omogućeno), omogućeno, onemogućeno|
|Podrazumevano |Omogućeno|

Ovo podešavanje određuje da li će se pokazivač izbora (tačke 7 i 8) prikazivati na brajevom redu.
Opcija je podrazumevano omogućena, pa će se pokazivač izbora prikazivati.
Pokazivač izbora može ometati u toku čitanja.
Isključivanje ove opcije može poboljšati iskustvo pri čitanju.

Da biste uključili ili isključili prikazivanje izbora bilo gde da se nalazite, molimo podesite prilagođenu prečicu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

#### Izaberi brajev red {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Otvori dijalog za izbor brajevog reda {#toc168}

Prečica: `NVDA+kontrol+a`

Dijalog za izbor brajevog reda, koji se može otvoriti aktiviranjem dugmeta promeni... u kategoriji brajeva podešavanja dijaloga NVDA podešavanja, dozvoljava vam da izaberete koji brajev red NVDA treba da koristi.
Kada izaberete vaš red, možete pritisnuti u redu i NVDA će učitati izabrani red.
Ako dođe do greške prilikom učitavanja, NVDA će vas obavestiti i nastaviće korišćenje prethodnog reda.

##### Brajev red {#SelectBrailleDisplayDisplay}

Ovaj izborni okvir vam pruža nekoliko opcija u zavisnosti od instaliranih drajvera na vašem sistemu.
Krećite se kroz ove opcije korišćenjem strelica.

Opcija automatski će dozvoliti programu NVDA da u pozadini pretražuje puno podržanih brajevih redova.
Kada je ova stavka omogućena i povežete podržan brajev red putem USB ili bluetooth veze, NVDA će automatski ostvariti vezu sa ovim brajevim redom.

Nema brajevog reda znači da ne koristite brajev red.

Molimo pročitajte deo [podržani brajevi redovi](#SupportedBrailleDisplays) za dodatne informacije o podržanim brajevim redovima kao i koji od njih podržavaju pozadinsko automatsko prepoznavanje.

##### Redovi koje treba automatski prepoznati {#SelectBrailleDisplayAutoDetect}

Kada je brajev red podešen na "Automatski", izborna polja u ovoj listi vam dozvoljavaju da omogućite ili onemogućite drajvere za brajeve redove koji će biti uključeni u proces automatskog prepoznavanja.
Ovo vam dozvoljava da onemogućite drajvere za brajeve redove koje ne koristite stalno.
Na primer, ako imate red koji zahteva samo Baum drajver kako bi radio, možete ostaviti Baum drajver omogućen dok se drugi drajveri mogu onemogućiti.

Po podrazumevanim podešavanjima, svi drajveri koji podržavaju automatsko prepoznavanje su omogućeni.
Bilo koji drajver koji se doda, na primer u novijoj NVDA verziji ili dodatkom, takođe će biti podrazumevano omogućen.

Možete pogledati dokumentaciju za vaš brajev red u sekciji [podržani brajevi redovi](#SupportedBrailleDisplays) da biste proverili da li drajver podržava automatsko prepoznavanje redova.

##### Port {#SelectBrailleDisplayPort}

Ova opcija, ako je dostupna, dozvoljava vam da izaberete koji port ili koja vrsta veze će se koristiti sa aktivnim brajevim redom.
To je izborni okvir koji sadrži moguće opcije.

Po podrazumevanim podešavanjima, NVDA koristi automatsko prepoznavanje portova, što znači da će USB ili BlueTooth veza biti automatski prepoznata.
Ali, za neke brajeve redove, možete izabrati koji port će biti korišćen.
Česte opcije su "automatski" (ova opcija govori programu NVDA da koristi proceduru automatskog izbora porta), "USB", "Bluetooth" i serijski portovi ako vaš brajev red podržava ovu vrstu komunikacije.

Ova opcija neće biti dostupna ako vaš brajev red podržava samo automatsko prepoznavanje portova.

Možete pogledati dokumentaciju za vaš brajev red u delu [podržani brajevi redovi](#SupportedBrailleDisplays) da proverite vrste komunikacije i dostupne portove.

Molimo imajte na umu sledeće: Ako povežete više brajevih redova na vaš računar koji koriste isti drajver u isto vreme (na primer povezivanjem dva Seika uređaja),
trenutno je nemoguće da kažete programu NVDA koji red da koristi.
Tako da je preporučeno da povežete jedan brajev red jednog proizvođača / vrste u datom trenutku.

#### Zvuk {#AudioSettings}

<!-- KC:setting -->

##### Otvori podešavanja zvuka {#toc173}

Prečica: `NVDA+kontrol+u`

Kategorija zvuk u NVDA podešavanjima sadrži opcije koje vam dozvoljavaju da promenite neke opcije zvučnog izlaza.

##### Izlazni uređaj {#SelectSynthesizerOutputDevice}

Ova opcija vam dozvoljava da izaberete zvučnu kartu na koju će NVDA slati sav govor izabranog sintetizatora.

<!-- KC:setting -->

##### Režim stišavanja pozadinskih zvukova {#SelectSynthesizerDuckingMode}

Komanda: `NVDA+šift+d`

Ova opcija vam dozvoljava da izaberete da li NVDA treba da smanjuje glasnoću drugih aplikacija u toku izgovaranja, ili sve vreme dok je NVDA pokrenut.

* Bez stišavanja: NVDA nikada neće stišavati druge zvukove. 
* Utišaj u toku izgovaranja: NVDA će stišati druge zvukove dok izgovara ili reprodukuje svoje zvukove. Ovo možda neće raditi sa svim sintetizatorima. 
* Uvek utišaj: NVDA će utišati druge zvukove sve vreme dok je pokrenut.

Ova opcija je dostupna samo ako je NVDA instaliran.
Nije moguće podržati stišavanje pozadinskih zvukova za prenosne i privremene kopije programa NVDA.

##### Jačina NVDA zvukova prati jačinu glasa {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Onemogućeno, omogućeno|
|Podrazumevano |Onemogućeno|

Kada se ova opcija omogući, jačina NVDA zvukova i pištanja će pratiti podešavanje jačine glasa kojeg koristite.
Ako utišate jačinu glasa kojeg koristite, jačina NVDA zvukova će se takođe utišati.
Slično tome, ako pojačate glas, jačina zvukova će se pojačati.
Ova opcija nije dostupna ako je NVDA pokrenut sa onemogućenom [WASAPI opcijom za zvučni izlaz](#WASAPI) u naprednim podešavanjima.

##### Jačina NVDA zvukova {#SoundVolume}

Ovaj klizač vam dozvoljava da podesite jačinu NVDA zvukova i  pištanja.
Ovo podešavanje se primenjuje samo kada je opcija "Jačina NVDA zvukova prati jačinu glasa" onemogućena.
Ova opcija nije dostupna ako je NVDA pokrenut sa onemogućenom [WASAPI opcijom za zvučni izlaz](#WASAPI) u naprednim podešavanjima.

##### Vreme tokom kojeg treba održavati zvučnu kartu budnom nakon govora {#AudioAwakeTime}

Ovo polje za uređivanje određuje koliko dugo će NVDA održavati zvučnu kartu budnom nakon što se govor završi.
Ovo vam dozvoljava da NVDA izbegne određene greške u govoru kao što su odsečeni delovi reči.
Ovo se može desiti usled toga što zvučne karte (posebno Bluetooth i bežični uređaji) ulaze u stendbaj režim.
Ovo takođe može pomoći u drugim situacijama, kao što su korišćenje programa NVDA u virtuelnoj mašini (nna primer Citrix Virtual Desktop), ili na nekim laptop računarima.

Niske vrednosti će možda izazvati da se početak zvuka iseče češće, budući da će uređaj možda prebrzo ući u stendbaj režim, što će izazvati da se početak sledećeg izgovorenog teksta iseče.
Podešavanje previsoke vrednosti će možda izazvati da se baterija zvučne karte brže potroši, budući da uređaj ostaje aktivan duže a ne reprodukuje nikakve zvukove.

Možete podesiti vreme na nula kako biste onemogućili ovu funkciju.

##### Razdvajanje zvuka {#SelectSoundSplitMode}

Funkcija razdvajanja zvuka dozvoljava korisnicima da iskoriste stereo mogućnosti zvučnih uređaja, kao što su slušalice ili zvučnici.
Razdvajanje zvuka dozvoljava da NVDA zvukovi pređu na jedan kanal (na primer levi) a sve druge aplikacije reprodukuju zvukove na drugom kanalu (na primer desnom).
Razdvajanje zvukova je podrazumevano onemogućeno, što znači da će sve aplikacije uključujući NVDA reprodukovati zvukove na levom i desnom kanalu.
Prečica dozvoljava da kružite kroz različite režime razdvajanja zvuka:
<!-- KC:beginInclude -->

| Ime |Prečica |Opis|
|---|---|---|
|Kruži kroz režime razdvajanja zvuka |`NVDA+alt+s` |Kruži kroz režime razdvajanja zvuka.|

<!-- KC:endInclude -->

Podrazumevano, ova komanda će kružiti kroz sledeće režime:

* Razdvajanje zvuka onemogućeno: NVDA i druge aplikacije reprodukuju zvukove na oba kanala.
* NVDA na levoj strani a aplikacije na desnoj: NVDA će govoriti na levom kanalu, dok će druge aplikacije reprodukovati zvukove na desnom.
* NVDA na desnoj strani a aplikacije na levoj: NVDA će govoriti na desnom kanalu, dok će druge aplikacije reprodukovati zvukove na levom.

Napredniji režimi razdvajanja zvuka su dostupni u izbornom okviru podešavanja razdvajanja zvuka.
Imajte na umu da razdvajanje zvukova ne funkcioniše kao mikser.

Na primer, ako aplikacija reprodukuje stereo zvučni zapis dok je razdvajanje zvukova podešeno na "NVDA na levoj strani a aplikacije na desnoj", čućete samo desni kanal zvučnog zapisa, dok će levi kanal zvučnog zapisa biti utišan.
Ova opcija nije dostupna ako je NVDA pokrenut uz [WASAPI onemogućen za zvučni izlaz](#WASAPI) u naprednim podešavanjima.

Imajte na umu da ako se NVDA sruši, neće biti u stanju da vrati jačinu aplikacija, a te aplikacije će možda još uvek reprodukovati zvuk samo na jednom kanalu nakon rušenja programa NVDA.
Kako biste ovo rešili, molimo ponovo pokrenite NVDA.

##### Prilagođavanje režima razdvajanja zvuka {#CustomizeSoundSplitModes}

Ova lista sa kontrolama koje se mogu označiti dozvoljava da izaberete koji će režimi razdvajanja zvuka biti uključeni kada kružite kroz njih prečicom `NVDA+alt+s`.
Režimi koji nisu označeni neće biti uključeni.
Podrazumevano, omogućena su samo tri režima.

* Razdvajanje zvukova onemogućeno: I NVDA i aplikacije reprodukuju zvukove i na levom i na desnom kanalu.
* NVDA na levom kanalu a sve druge aplikacije na desnom kanalu.
* NVDA na desnom  a sve druge aplikacije na levom kanalu.

Imajte na umu da je neophodno označiti bar jedan režim.
Ova opcija nije dostupna ako je NVDA pokrenut uz [WASAPI onemogućen za zvučni izlaz](#WASAPI) u naprednim podešavanjima.

#### Vid {#VisionSettings}

Kategorija vid u NVDA podešavanjima vam dozvoljava da omogućite, onemogućite i podesite [vizuelne pomoćnike](#Vision).

Napomena da se dostupne opcije u ovom dijalogu mogu proširiti [NVDA dodacima](#AddonsManager).
Podrazumevano, ova kategorija podešavanja sadrži sledeće opcije:

##### Vizuelno označavanje {#VisionSettingsFocusHighlight}

Izborna polja vizuelnog označavanja kontrolišu ponašanje ugrađene funkcije [vizuelno označavanje](#VisionFocusHighlight).

* Omogući označavanje: Uključuje i isključuje vizuelno označavanje.
* Označi sistemski fokus: Bira da li će [sistemski fokus](#SystemFocus) biti označen.
* Označi navigacioni objekat: Bira da li će [navigacioni objekat](#ObjectNavigation) biti označen.
* Označi kursor režima pretraživanja: Bira da li će [virtuelni kursor režima pretraživanja](#BrowseMode) biti označen.

Napomena da će menjanje opcije "omogući označavanje" takođe promeniti stanje 3 ostale opcije.
Zato, ako se opcija "omogući označavanje" isključi i nakon toga označite ovu opciju, ostale tri opcije će se takođe označiti.
Ako želite samo da označite sistemski fokus a onemogućite navigacioni objekat i režim pretraživanja, stanje opcije "omogući označavanje" biće polovično označeno.

##### Zatamnjivanje ekrana {#VisionSettingsScreenCurtain}

Možete omogućiti [zatamnjivanje ekrana](#VisionScreenCurtain) tako što će te označiti opciju "Učini da ekran bude crn(primenjuje se odmah)".
Upozorenje da će vaš ekran postati crn nakon aktivacije će se prikazati.
Pre nastavka (opcijom "da"), uverite se da ste omogućili govor ili brajev red i da možete da kontrolišete vaš računar bez ekrana.
Izaberite "Ne" ako više ne želite da omogućite zatamnjivanje ekrana.
Ako ste sigurni, možete aktivirati dugme da kako biste omogućili zatamnjivanje ekrana.
Ako više ne želite da vidite ovo upozorenje, možete ovo da promenite u dijalogu koji prikazuje tu poruku.
Uvek možete da vratite upozorenje tako što ćete označiti opciju "Uvek prikaži upozorenje kada se omogući zatamnjivanje ekrana" koja se nalazi pored opcije "učini da ekran bude crn".

Po podrazumevanim podešavanjima, zvukovi se reprodukuju kada se menja zatamnjivanje ekrana.
Kada želite ovo da promenite, možete onemogućiti opciju "Reprodukuj zvuk kada se zatamnjivanje ekrana omogući ili onemogući".

##### Podešavanja za pomoćnike trećih strana {#VisionSettingsThirdPartyVisualAids}

Dodatni vizuelni pomoćnici mogu se instalirati u [NVDA dodacima](#AddonsManager).
Kada ovi pomoćnici imaju podešavanja koja se mogu menjati, biće prikazana u ovoj kategoriji podešavanja u posebnim grupama.
Za podržana podešavanja po pomoćnicima, molimo proverite dokumentaciju tog pomoćnika.

#### Tastatura {#KeyboardSettings}

<!-- KC:setting -->

##### Otvori podešavanja tastature {#toc188}

Prečica: `NVDA+kontrol+k`

Kategorija tastatura u dijalogu NVDA podešavanja sadrži podešavanja koja kontrolišu kako se NVDA ponaša dok koristite vašu tastaturu i unosite znakove na njoj.
Ova kategorija podešavanja sadrži sledeće opcije:

##### Raspored tastature {#KeyboardSettingsLayout}

Ovaj izborni okvir vam dozvoljava da izaberete koji raspored tastature NVDA treba da koristi. Trenutno dva rasporeda koji dolaze uz NVDA su desktop i laptop.

##### Izaberi NVDA modifikatorske tastere {#KeyboardSettingsModifiers}

Izborni okviri u ovoj listi kontrolišu koji tasteri ćese koristiti kao [NVDA modifikatorski tasteri](#TheNVDAModifierKey). Sledeći tasteri su dostupni za izbor:

* Taster velika slova
* Insert taster na numeričkoj tastaturi
* Prošireni taster insert (obično se nalazi iznad strelica, blizu home i end tastera)

Ako nijedan taster nije izabran kao NVDA taster biće nemoguće da pristupite mnogim NVDA komandama, pa je zbog toga neophodno označiti barem jedan modifikator.

<!-- KC:setting -->

##### Izgovaraj ukucane znakove {#KeyboardSettingsSpeakTypedCharacters}

Komanda: NVDA+2

Kada je omogućeno, NVDA će izgovoriti sve znakove koje upišete na tastaturi.

<!-- KC:setting -->

##### Izgovaraj ukucane reči {#KeyboardSettingsSpeakTypedWords}

Komanda: NVDA+3

Kada je omogućeno, NVDA će izgovoriti sve reči koje upišete na tastaturi.

##### Prekid u izgovoru ukucanih znakova {#KeyboardSettingsSpeechInteruptForCharacters}

Ako je uključena, ova opcija će izazvati prekid govora uvek kada se upiše novi znak. Uključena je po podrazumevanim podešavanjima.

##### Prekid izgovora za taster Enter {#KeyboardSettingsSpeechInteruptForEnter}

Ako je uključena, ova opcija će izazvati prekid govora kada se pritisne taster Enter. Uključena je po podrazumevanim podešavanjima.

##### Dozvoli površno čitanje u Izgovori sve režimu {#KeyboardSettingsSkimReading}

Ako je uključeno, određene komande navigacije(kao što je brza navigacija u režimu pretraživanja i kretanje po redovima i pasusima) ne zaustavljaju režim izgovori sve, već ovaj režim nastavlja čitanje i skače na novu poziciju.

##### Pišti ako se kucaju mala slova kada je uključen taster za velika slova {#KeyboardSettingsBeepLowercase}

Kada je omogućeno, pištanje upozorenja će se čuti kada se slova pišu dok se drži taster šift i taster caps lock je uključen.
Obično, pisanje ovakvih slova je nenamerno i dešava se kada ne znamo da je caps lock uključen.
Zbog toga, može biti veoma korisno da dobijete upozorenje o tome.

<!-- KC:setting -->

##### Izgovaraj komandne tastere {#KeyboardSettingsSpeakCommandKeys}

Komanda: NVDA+4

Kada je omogućeno, NVDA će izgovoriti sve tastere koji nisu znakovi na tastaturi. Ovo uključuje kombinacije kao što su kontrol+ dodatno slovo.

##### reprodukuj zvukove za greške u pravopisu u toku pisanja {#KeyboardSettingsAlertForSpellingErrors}

Kada je omogućeno, kratak zvučni signal će biti reprodukovan kada napravite grešku u toku pisanja.
Ova opcija je dostupna samo ako je opcija prijavi greške u pravopisu omogućena u [kategoriji formatiranje dokumenta](#DocumentFormattingSettings) dijaloga NVDA podešavanja.

##### Kontroliši tastere iz drugih aplikacija {#KeyboardSettingsHandleKeys}

Ova opcija vam dozvoljava da kontrolišete da li tasteri pritisnuti od strane drugih aplikacija kao što su aplikacije za prepoznavanje govora i tastature na ekranu NVDA treba da koristi. 
Ova opcija je uključena po podrazumevanim podešavanjima, ali određeni korisnici će možda želeti da je isključe, na primer oni koji pišu Vijetnamski sa programom UniKey kako nebi dobili neispravne znakove.

#### Miš {#MouseSettings}

<!-- KC:setting -->

##### Otvori podešavanja miša {#toc201}

Prečica: `NVDA+kontrol+m`

Kategorija miš u dijalogu NVDA podešavanja dozvoljava programu NVDA da prati miš, reprodukuje zvučne koordinate miša i podešava druge opcije korišćenja miša.
Ova kategorija sadrži sledeće opcije:

##### Izveštavaj o promenama oblika miša {#MouseSettingsShape}

Izborno polje, koje kada je označeno izaziva da NVDA izgovori oblik miša kada se promeni.
miš u Windowsu menja oblik da prikaže određene informacije kao što su kada nešto može da se uredi, ili kada se nešto učitava.

<!-- KC:setting -->

##### Omogući praćenje miša {#MouseSettingsTracking}

Komanda: NVDA+m

Kada je omogućeno, NVDA će izgovoriti tekst ispod miša, dok ga pomerate po ekranu. Ovo vam dozvoljava da pronađete stvari na ekranu, fizičkim pomeranjem miša, umesto da ih tražite navigaciom objekata.

##### Rezolucija jedinice teksta {#MouseSettingsTextUnit}

Ako je NVDA podešen da izgovori tekst ispod miša dok ga pomerate, ova opcija vam dozvoljava da izaberete koliko teksta će biti izgovoreno.
Opcije su znak, reč, red i pasus.

Kako biste menjali jedinicu rezolucije teksta bilo gde, molimo podesite prilagođenu prečicu korišćenjem dijaloga [ulazne komande](#InputGestures).

##### Prijavi objekat kada miš uđe u njega {#MouseSettingsRole}

Ako je ovo izborno polje označeno, NVDA će izgovarati informacije o objektima kada miš uđe u njih.
Ovo uključuje vrstu (tip) objekta kao i stanja (označeno/pritisnuto), koordinate ćelija u tabelama, i slično.
Imajte na umu da izgovor nekih detalja objekta može zavisiti od toga kako su podešena druga podešavanja, kao što su podešavanja u kategorijama  [Predstavljanje objekata](#ObjectPresentationSettings) ili [Formatiranje dokumenta](#DocumentFormattingSettings).

##### Reprodukuj zvučne koordinate kada se miš pomera {#MouseSettingsAudio}

Kada je ovo izborno polje označeno NVDA reprodukuje zvučne signale u toku pomeranja miša, kako bi korisnik mogao da zna gde se miš nalazi na ekranu.
Što je miš više na ekranu, viša je visina pištanja.
Što je miš više udaljen od leve ili desne strane, signal će biti reprodukovan na levoj ili desnoj strani(ako korisnik ima stereo zvučnike ili slušalice).

##### Osvetljenje kontroliše jačinu zvučnih koordinata {#MouseSettingsBrightness}

Ako je izborno polje"reprodukuj zvučne koordinate dok se miš pomera" označeno, onda kada se označi ovo polje jačina zvučnih koordinata zavisi od svetline ekrana na delu ispod miša.
Ovo polje nije označeno po podrazumevanim podešavanjima.

##### Ignoriši unos miša iz drugih aplikacija {#MouseSettingsHandleMouseControl}

Ova opcija dozvoljava korisniku da podesi program NVDA da ignoriše događaje pomeranja miša (uključujući klikove) proizvedene od strane drugih aplikacija kao što su TeamViewer i drugih programa za daljinsko kontrolisanje.
Ova opcija je onemogućena po podrazumevanim podešavanjima.
Ako omogućite ovu opciju i opciju "Omogući praćenje miša", NVDA neće izgovarati šta je ispod miša ako je miš kontrolisan od strane druge aplikacije.

#### Interakcija sa ekranom osetljivim na dodir {#TouchInteraction}

Ova kategorija podešavanja, dostupna samo na računarima sa ekranima osetljivim na dodir, vam dozvoljava da podesite kako se NVDA ponaša pri radu na ekranu.
Ova kategorija sadrži sledeće opcije:

##### Omogući podršku interakcije sa ekranom {#TouchSupportEnable}

Ovo izborno polje će omogućiti podršku interakcije programa NVDA sa ekranom.
Ako je omogućena, možete da koristite vaš prst da se krećete i aktivirate stavke na ekranu osetljivom na dodir.
Ako je onemogućena, podrška za ekran osetljiv na dodir biće potpuno onemogućena kao da NVDA nije pokrenut.
Ovo podešavavnje se takođe može menjati korišćenjem prečice NVDA+kontrol+alt+t. 

##### Režim pisanja na ekranu {#TouchTypingMode}

Ovo izborno polje vam dozvoljava da izaberete način unosa na tastaturi na ekranu.
Ako je ovo izborno polje označeno, kada pronađete taster na tastaturi na ekranu, možete podići vaš prst i izabrani taster će biti pritisnut.
Ako ovo nije označeno, morate izvršiti dvostruki dodir na tasteru za njegovu aktivaciju.

#### Pregledni kursor {#ReviewCursorSettings}

Kategorija pregledni kursor u dijalogu podešavanja programa NVDA se koristi za podešavanje ponašanja preglednog kursora programa NVDA.
Ova kategorija sadrži sledeće opcije:

<!-- KC:setting -->

##### Prati sistemski fokus {#ReviewCursorFollowFocus}

Komanda: NVDA+7

Kada je omogućeno, pregledni kursor će uvek biti postavljen na objekat sistemskog fokusa kada se fokus promeni.

<!-- KC:setting -->

##### Prati sistemski kursor {#ReviewCursorFollowCaret}

Komanda: NVDA+6

Kada je omogućeno, pregledni kursor će uvek biti postavljen na poziciju sistemskog kursora kada kursor promeni poziciju.

##### Prati kursor miša {#ReviewCursorFollowMouse}

Kada je omogućeno, pregledni kursor prati miš u toku pomeranja.

##### Jednostavan režim pregleda {#ReviewCursorSimple}

Kada je omogućeno, NVDA će filtrirati objekte u toku pregleda kako bi isključio objekte koji nisu bitni za korisnika; na primer nevidljivi objekti i objekti koji se koriste samo u svrhu izgleda.

Da isključite i uključite režim jednostavnog pregleda bilo gde, dodajte prilagođenu komandu koristeći [dijalog za ulazne komande](#InputGestures).

#### Predstavljanje objekata {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Otvori podešavanja predstavljanja objekata {#toc218}

Prečica: `NVDA+kontrol+o`

Kategorija predstavljanje objekata u dijalogu NVDA podešavanja se koristi za podešavanje koliko informacija će NVDA prijavljivati o kontrolama kao što su opis, informacije o poziciji i tako dalje.
Ove opcije se obično ne primenjuju u režimu pretraživanja.
Ove opcije obično važe za prijavljivanje fokusa i objektnu navigaciju, ali ne i za čitanje tekstualnog sadržaja na primer u režimu pretraživanja.

##### Prijavi opise alata {#ObjectPresentationReportToolTips}

Izborno polje koje kada je označeno govori programu NVDA da čita opise alata kada se pojave.
Puno prozora i kontrola prikazuju male poruke(ili opise alata) Kada pomerite miš preko njih, ili nekada kada se fokusirate na njih.

##### Prijavi obaveštenja {#ObjectPresentationReportNotifications}

Ova opcija, kada je označena, govori programu NVDA da prijavljuje balone za pomoć i obaveštenja kada se pojave.

* Baloni za pomoć su kao opisi alata, ali su obično veći, i obaveštavaju o sistemskim događajima kao što su isključivanje mrežnog kabla, ili vas upozoravaju o Windows sigurnosnim problemima.
* Obaveštenja se pojavljuju od Windowsa 10 i nalaze se u centru za obaveštenja na sistemskoj traci, informišu nas o određenim događajima (na primer da je ažuriranje preuzeto, novi mail je stigao u naše sanduče, i slično).

##### Prijavi prečice sa tastature za objekte {#ObjectPresentationShortcutKeys}

Kada je ovo izborno polje označeno, NVDA će uključiti prečicu koju neka kontrola poseduje kada čita tu kontrolu.
Na primer meni datoteka na traci menija može imati prečicu alt+f.

##### Prijavi informacije o poziciji objekta {#ObjectPresentationPositionInfo}

Ova opcija vam dozvoljava da izaberete da li želite da čujete poziciju objekta(na primer 1 od 4) kada se krećete po objektima fokusiranjem ili objektnom navigaciom.

##### Pogodi poziciju objekta kada nije dostupna {#ObjectPresentationGuessPositionInfo}

Ako je prijavljivanje informacija o poziciji uključeno, ova opcija govori programu NVDA da pogodi informacije o poziciji kada nisu dostupne za neku kontrolu.

Kada je uključena, NVDA će prijaviti informacije o poziciji za više kontrola kao što su meniji i alatne trake, ali ove informacije mogu biti neprecizne.

##### Prijavi opis objekta {#ObjectPresentationReportDescriptions}

Nemojte označiti ovo polje ako ne želite da čujete opis zajedno sa objektom (na primer predlozi pretrage, prijavljivanje celog dijaloga nakon što se otvori, i slično).

<!-- KC:setting -->

##### Informacije o traci napredovanja {#ObjectPresentationProgressBarOutput}

Komanda: NVDA+u

Ova opcija kontroliše kako NVDA prijavljuje ažuriranja trake napredovanja.

Ima sledeće opcije:

* Isključeno: Promene trake napredovanja neće biti prijavljene.
* Izgovaranje: Ova opcija govori programu NVDA da izgovara promene trake napredovanja. Svaki put kada se traka napredovanja promeni, NVDA će izgovoriti novu vrednost.
* Pištanja: Ova opcija govori programu NVDA da reprodukuje pištanja kada se traka napredovanja promeni. Što su pištanja viša, traka napredovanja je bliža kraju.
* Pištanja i izgovaranje: Ova opcija govori programu NVDA da izgovara i reprodukuje pištanja za promene trake napredovanja.

##### Obaveštavaj o pozadinskim trakama napredovanja {#ObjectPresentationReportBackgroundProgressBars}

Ovo je opcija koja, kada je označena, govori programu NVDA da obaveštava o traci napredovanja, čak i kada je u pozadini.
Ako umanjite ili izađete iz prozora koji sadrži traku napredovanja, NVDA će nastaviti da je prati, što vam dozvoljava da radite druge stvari dok vas NVDA obaveštava o trakama napredovanja.

<!-- KC:setting -->

##### Obaveštavaj o dinamičkim promenama sadržaja {#ObjectPresentationReportDynamicContent}

Komanda: NVDA+5

Uključuje i isključuje izgovor novog sadržaja a posebno objekata kao što su terminali i istorije ćaskanja.

##### Reprodukuj zvuk kada se pojave automatski predlozi {#ObjectPresentationSuggestionSounds}

Uključuje i isključuje prijavu pojave automatskih predloga, i ako je omogućeno, NVDA će reprodukovati zvuk.
Automatski predlozi su liste predloga na osnovu teksta koji je upisan u određenim poljima pretrage ili dokumentima.
Na primer, kada upišete tekst u start meni Windowsa Vista ili novijeg, Windows prikazuje listu predloga na osnovu upisanog teksta.
Za određena polja pretrage u Windowsu 10, NVDA vas može obavestiti da se lista predloga pojavila kada upišete tekst u polje.
Lista automatskih predloga će se zatvoriti kada izađete iz polja za unos, i za neka polja, NVDA vas može obavestiti o tome.

#### Ulazni sastav {#InputCompositionSettings}

Kategorija ulazni sastav vam dozvoljava da podesite kako NVDA izgovara unos azijskih znakova, kao što je unos sa IME ili unos tekstualnih servisa.
Napomena da zbog toga što se metodi unosa razlikuju u zavisnosti od toga koje informacije pružaju, najverovatnije će biti potrebno da podesite ulazna podešavanja za svaku vrstu unosa posebno za najbolje pisanje.

##### Automatski izvesti o svim dostupnim kandidatima {#InputCompositionReportAllCandidates}

Ova opcija, koja je podrazumevano uključena, vam dozvoljava da izaberete da li treba prijaviti sve kandidate kada se pojave ili kada se promeni stranica.
Ova opcija je korisna za unose kao što su Kineski novi ChangJie ili Boshiami, kako biste mogli odmah da čujete sve simbole i brojeve i možete odmah da ih izaberete.
Ali, za fonetske unose kao što su Kineski novi fonetski, možda će biti korisnije da isključite ovu opciju, budući da će sve informacije zvučati isto i moraćete da proverite svaki kandidat ručno kako biste čuli opise znakova.

##### Izgovori izabran kandidat {#InputCompositionAnnounceSelectedCandidate}

Ova opcija, uključena po podrazumevanim podešavanjima, kontroliše da li NVDA treba da izgovara izabran kandidat kada se izbor menja ili kada pristupite listi kandidata.
Za unose gde se izbor može menjati sa strelicama(kao što su Kineski novi fonetski) ovo je potrebno, ali za neke unose pisanje će biti efikasnije sa ovom opcijom isključenom.
Napomena da i kada je ova opcija isključena, pregledni kursor će biti postavljen na izabran kandidat kako biste mogli da koristite pregledni kursor/navigaciju objekata kako biste mogli da pregledate kandidate.

##### Uvek uključi kratke opise za dostupne kandidate {#InputCompositionCandidateIncludesShortCharacterDescription}

Ova opcija, koja je omogućena po podrazumevanim podešavanjima, vam dozvoljava da izaberete da li NVDA treba da pruži kratak opis za kandidate, ili kada je izabran ili kada se lista kandidata pojavi.
Napomena da za jezike kao što je Kineski, izgovor opisa za dodatne kandidate se ne menja.
Ova opcija može biti korisna za Korejski i Japanski.

##### Prijavi izmene u nizu karaktera koji se čita {#InputCompositionReadingStringChanges}

Neki metodi unosa kao što su Chinese novi fonetski i novi ChangJie imaju niz čitanja(takođe zvan niz pre sastava).
Možete izabrati da li se ove promene prijavljuju.
Ova opcija je uključena po podrazumevanim podešavanjima.
Napomena da neki stariji metodi unosa kao što su Kineski ChangJie možda neće imati niz čitanja, ali će koristiti niz sastava. Molimo pogledajte sledeću opciju za podešavanje niza sastava.

##### Prijavi promene u nizu sastava {#InputCompositionCompositionStringChanges}

Nakon što se podaci povežu u ispravan simbol, većina metoda unosa to čuva u niz sastava.
Ova opcija bira da li će NVDA prijaviti ovakve simbole.
Uključena je po podrazumevanim podešavanjima.

#### Režim pretraživanja {#BrowseModeSettings}

<!-- KC:setting -->

##### Otvori podešavanja režima pretraživanja {#toc236}

Prečica: `NVDA+kontrol+b`

Kategorija režim pretraživanja u dijalogu NVDA podešavanja se koristi za podešavanje ponašanja programa NVDA kada čitate i krećete se kroz veće dokumente kao što su Web stranice.
Ova kategorija sadrži sledeće opcije:

##### Maksimalan broj znakova u jednom redu {#BrowseModeSettingsMaxLength}

Ovo polje postavlja maksimalnu dužinu reda u režimu pretraživanja(u znakovima).

##### Broj redova po stranici {#BrowseModeSettingsPageLines}

Ovo polje podešava za koliko redova ćete se pomeriti tasterima page up i page down u režimu pretraživanja.

<!-- KC:setting -->

##### Koristi izgled ekrana {#BrowseModeSettingsScreenLayout}

Komanda: NVDA+v

Ova opcija vam dozvoljava da odredite da li će režim pretraživanja staviti klikabilne elemente (linkove, dugmad i polja za unos) na posebnom redu, ili da ostanu u tekstu kako su vizuelno prikazani.
Napomena da se ova opcija ne primenjuje na Microsoft Office aplikacije kao što su Outlook i Word, koje uvek koriste izgled ekrana.
Kada je izgled ekrana omogućen, elementi stranice će ostati onakvi kakvi su vizuelno prikazani.
Na primer, Vizuelni red sa više linkova će se izgovarati i biti prikazan na brajevom redu kao red sa više linkova.
Ako se onemogući, elementi stranice će biti na posebnim redovima.
Ovo može biti lakše za razumevanje kada se kroz stranicu krećete red po red i može učiniti interakciju sa stavkama lakšom za neke korisnike.

##### Omogući režim pretraživanja kada se stranica učita {#BrowseModeSettingsEnableOnPageLoad}

Ovo izborno polje kontroliše da li će se režim pretraživanja aktivirati učitavanjem stranica.
Kada je ova opcija onemogućena, režim pretraživanja se ručno može aktivirati na stranicama ili u dokumentima u kojima je režim pretraživanja podržan.
Pogledajte deo [režim pretraživanja](#BrowseMode) za listu aplikacija podržanih od strane režima pretraživanja.
Napomena da se ova opcija ne primenjuje u situacijama u kojima je režim pretraživanja uvek ručno aktiviran, na primer u programu Microsoft Word.
Ova opcija je omogućena po podrazumevanim podešavanjima.

##### Automatski Izgovori sve režim kada se učita stranica {#BrowseModeSettingsAutoSayAll}

Ovo izborno polje uključuje i isključuje automatsko čitanje stranice u režimu pretraživanja kada se učita.
Ova opcija je omogućena po podrazumevanim podešavanjima.

##### Uključi tabele za izgled {#BrowseModeSettingsIncludeLayoutTables}

Ova opcija menja kako NVDA učitava tabele koje se koriste za izgled.
Kada je uključena, NVDA će ih smatrati kao normalne tabele, i prijavljivaće ih na osnovu [podešavanja formatiranja dokumenta](#DocumentFormattingSettings) i dolazak na njih uz pomoć brze navigacije je moguć.
Kada je isključena, neće biti izgovorene niti ih je moguće naći brzom navigacijom.
Ali, sadržaj tabela će biti uključen kao normalan tekst.
Ova opcija je isključena po podrazumevanim podešavanjima.

Da uključite i isključite tabele za izgled bilo gde da se nalazite, molimo podesite komandu koristeći [dijalog za ulazne komande](#InputGestures).

##### Podešavanje prijavljivanja elemenata kao što su linkovi i naslovi {#BrowseModeLinksAndHeadings}

Molimo pogledajte opcije u [kategoriji formatiranje dokumenta](#DocumentFormattingSettings) [NVDA podešavanja](#NVDASettings) kako biste podesili polja koja se prijavljuju u toku navigacije, na primer linkovi, naslovi i tabele.

##### Automatski režim fokusiranja za promene fokusa {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Ova opcija dozvoljava aktiviranje režima fokusiranja ako se fokus promeni.
Na primer, kada ste na Web stranici, ako pritisnete tab i dođete do polja za unos, ako je ova opcija omogućena, režim fokusiranja će automatski biti aktiviran.

##### Automatski režim fokusiranja za pomeranje kursora {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Ova opcija, kada je omogućena, dozvoljava programu NVDA da uđe i izađe iz režima fokusiranja kada koristite strelice.
Na primer, ako koristite strelice da se krećete po Web stranici i dođete do polja za unos teksta, NVDA će automatski ući u režim fokusiranja.
Ako izađete iz polja sa strelicama, NVDA će se vratiti u režim pretraživanja.

##### Zvučna potvrda za režime fokusiranja i pretraživanja {#BrowseModeSettingsPassThroughAudioIndication}

Ako je ova opcija omogućena, NVDA će reprodukovati posebne zvukove kada se prebacuje između režima fokusiranja i pretraživanja, umesto da izgovori promenu.

##### Spreči sve prečice koje nisu komande da dođu u susret sa dokumentom {#BrowseModeSettingsTrapNonCommandGestures}

Omogućena po podrazumevanim podešavanjima, ova opcija vam dozvoljava da izaberete da li tasteri(koji nisu komande), trebaju biti sprečeni da dođu do dokumenta na kome ste trenutno fokusirani. 
Kao primer, ako je omogućena, ako se pritisne slovo j, neće doći do dokumenta, čak iako nije komanda brze navigacije i verovatno da nije komanda aplikacije.
U ovom slučaju NVDA će reći Windowsu da reprodukuje zvuk kada se pritisne taster koji nije deo brze navigacije.

<!-- KC:setting -->

##### Automatski postavi sistemski fokus na elemente koji se mogu fokusirati u režimu pretraživanja {#BrowseModeSettingsAutoFocusFocusableElements}

Komanda: NVDA+8

Onemogućena po podrazumevanim podešavanjima, ova opcija vam omogućava da izaberete da li će sistemski fokus automatski biti postavljen na elemente koji se mogu fokusirati (linkovi, polja za unos, i tako dalje.) u toku navigacije kroz sadržaj kursorom režima pretraživanja.
Ako ostavite ovu opciju onemogućenu elementi izabrani kursorom režima pretraživanja se neće automatski fokusirati.
Ovo može omogućiti brže pretraživanje i bolji odziv u režimu pretraživanja.
Fokus će ipak biti ažuriran kada vršite interakciju sa elementom (na primer pritiskanje dugmeta, označavanje izbornog polja).
Ako se ova opcija omogući može poboljšati podršku za neke sajtove uz sporiji odziv i manju stabilnost.

#### Formatiranje dokumenta {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Otvori  podešavanja formatiranja dokumenta {#toc250}

Prečica: `NVDA+kontrol+d`

Većina opcija u ovoj kategoriji vam dozvoljava da izaberete informacije koje trebaju biti prijavljivane dok pomerate kursor kroz dokument.
Na primer, ako označite polje prijavi ime fonta, kada dođete do teksta sa različitim fontom, ime fonta će biti izgovoreno.

Opcije formatiranja dokumenta su organizovane po grupama.
Možete podesiti prijavljivanje sledećih elemenata:

* Font
  * Ime fonta
  * Veličina fonta
  * Karakteristike fonta
  * Indeksi i eksponenti
  * Naglašenost teksta
  * Markiran (obeležen tekst)
  * Stil
  * Boje
* Informacije o dokumentu
  * Komentari
  * Markeri
  * Uređivačke izmene
  * Greške u pravopisu
* Strane i odvajanja
  * Brojevi strana
  * Brojevi redova
  * Prijavljivanje uvlačenja redova [(isključeno, govor, tonovi, govor i tonovi)](#DocumentFormattingSettingsLineIndentation)
  * Zanemarivanje praznih redova za prijavljivanje uvlačenja
  * Uvlačenja pasusa(na primer puno uvlačenje, uvučen prvi red)
  * Odvajanje redova (Pojedinačno, dvostruko i tako dalje)
  * Poravnavanje
* Informacije o tabelama
  * Tabele
  * Zaglavlja redova/kolona (isključeno, redovi, kolone, redovi i kolone)
  * Koordinati ćelija
  * Granice ćelija (isključeno, stilovi, boje i stilovi)
* Elementi
  * Naslovi
  * Linkovi
  * Slike
  * Liste
  * Citati
  * Grupisanja
  * Orjentiri
  * članci
  * Okviri
    * Figure i naslovi slika
* Klikabilnost
  -

Da uključite i isključite ova podešavanja bilo gde, podesite prilagođene komande koristeći [dijalog ulazne komande](#InputGestures).

##### Prijavi promene formatiranja nakon pomeranja kursora {#DocumentFormattingDetectFormatAfterCursor}

Ako je omogućena, ova opcija govori programu NVDA da pokuša da prepozna sve promene u formatiranju u toku izgovaranja redova, čak iako će to usporiti NVDA.

Po podrazumevanim podešavanjima, NVDA će prepoznati formatiranje na poziciji sistemskog i preglednog kursora, i u nekim slučajevima može prepoznati formatiranje na ostatku reda, samo ako to neće usporiti program.

Omogućite ovu opciju kada proveravate izgled dokumenata u programima kao što je WordPad, gde je formatiranje važno.

##### Prijavljivanje uvlačenja redova {#DocumentFormattingSettingsLineIndentation}

Ova opcija vam dozvoljava da podesite kako se uvlačenje na početku redova prijavljuje.
Izborni okvir prijavi uvlačenje redova ima četiri opcije.

* Isključeno: NVDA neće obraćati pažnju na uvlačenje redova.
* Govor: Ako je govor izabran, kada se količina uvlačenja promeni, NVDA će reći"dvanaest razmaka" ili"Četiri tabulatora."
* Tonovi: Ako su tonovi izabrani, kada se količina uvlačenja promeni, tonovi označavaju količinu uvlačenja.
Ton će povećati visinu za svaki razmak, a za tabulator, povećaće visinu jednakoj četiri razmaka.
* Govor i tonovi: Ova opcija čita uvlačenja koristeći obe opcije.

Ako označite izborno polje "Zanemari prazne redove za prijavljivanje uvlačenja", onda se promene u uvlačenju neće prijavljivati u praznim redovima.
Ovo može biti korisno kada čitate dokument u kojem se prazni redovi koriste da se odvoje uvučeni blokovi teksta, na primer u izvornom kodu programa.

#### Navigacija kroz dokument {#DocumentNavigation}

Ova kategorija vam dozvoljava da promenite različite aspekte navigacije kroz dokument.

##### Stil pasusa {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevani (kontrolisan od strane aplikacije), kontrolisan od strane aplikacije, jedan novi red, više novih redova|
|Podrazumevani |Kontrolisan od strane aplikacije|

Ovaj izborni okvir vam dozvoljava da izaberete stil pasusa koji će se koristiti kada se krećete po pasusima prečicama `kontrol+strelicaGore` i `kontrol+strelicaDole`.
Dostupni stilovi pasusa su:

* Kontrolisan od strane aplikacije: NVDA će dozvoliti aplikaciji da odredi prethodni i sledeći pasus, i pročitaće novi pasus u toku navigacije.
Ovaj stil najbolje radi kada aplikacija podržava ugrađenu navigaciju po pasusima, i ovo je podrazumevana opcija.
* Jedan novi red: NVDA će pokušati da odredi prethodni ili sledeći pasus korišćenjem jednog novog reda kao pokazivača pasusa.
Ovaj stil najbolje radi kada se čitaju dokumenti u aplikaciji koja ne podržava ugrađenu navigaciju po pasusima, a pasusi u dokumentu su označeni jednim pritiskom tastera `enter`.
* Više novih redova: NVDA će pokušati da odredi prethodni ili sledeći pasus korišćenjem bar jednog praznog reda (dva puta pritisnut taster `enter`) kao pokazivača pasusa.
Ovaj stil najbolje radi sa dokumentima koji koriste blok pasuse.
Napomena da se ovaj stil pasusa ne može koristiti u Microsoft Wordu ili Microsoft Outlooku, osim ako koristite UIA za pristup Microsoft Word kontrolama.

Možete se prebacivati između različitih stilova pasusa bilo gde tako što ćete podesiti prečicu u [dijalogu ulaznih komandi](#InputGestures).

#### Windows OCR podešavanja {#Win10OcrSettings}

Podešavanja u ovoj kategoriji vam dozvoljavaju da podesite [Windows OCR](#Win10Ocr).
Ova kategorija sadrži sledeće opcije:

##### Jezik prepoznavanja {#Win10OcrSettingsRecognitionLanguage}

Ovaj izborni okvir vam dozvoljava da izaberete jezik za prepoznavanje teksta.
Kako biste kružili kroz dostupne jezike bilo gde da se nalazite, molimo podesite prilagođenu prečicu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

##### Povremeno osvežavaj prepoznat sadržaj {#Win10OcrSettingsAutoRefresh}

Kada je ovo izborno polje označeno, NVDA će automatski osvežiti prepoznat sadržaj kada je rezultat prepoznavanja fokusiran.
Ovo može biti veoma korisno kada gledate sadržaj koji se stalno menja, na primer kada gledate video sa titlovima.
Osvežavanje se izvršava svake jedne ipo sekunde.
Ova opcija je podrazumevano onemogućena.

#### Napredna podešavanja {#AdvancedSettings}

Upozorenje! Ova podešavanja su samo za napredne korisnike i mogu izazvati neispravno funkcionisanje programa NVDA ako se pogrešno podese.
Menjajte ova podešavanja samo ako znate šta radite ili ako vam je neko od NVDA programera dao određena uputstva.

##### Menjanje naprednih podešavanja {#AdvancedSettingsMakingChanges}

Kako biste menjali napredna podešavanja, kontrole moraju biti omogućene tako što ćete potvrditi, aktiviranjem izbornog polja, da razumete rizike menjanja ovih podešavanja

##### Vraćanje podrazumevanih podešavanja {#AdvancedSettingsRestoringDefaults}

Ovo dugme vraća podrazumevane vrednosti za ova podešavanja, čak iako izborno polje nije označeno.
Nakon menjanja podešavanja koje želite da vratite na podrazumevane vrednosti.
Ovo takođe može biti korisno kada niste sigurni da li su podešavanja promenjena.

##### Omogući učitavanje prilagođenog koda iz Scratchpad foldera {#AdvancedSettingsEnableScratchpad}

Kada programirate dodatke za NVDA, korisno je da možete da testirate kod dok ga pišete.
Kada je ova opcija omogućena, dozvoljava programu NVDA učitavanje prilagođenih modula za aplikacije, globalnih dodataka, drajvera za brajeve redove, drajvera za sintetizatore i usluga vizuelne pomoći iz specijalnog Scratchpad foldera u vašem folderu za NVDA podešavanja.
Kao i njihovi ekvivalenti u dodacima, ovi moduli se učitavaju kada se NVDA pokrene, ili u slučaju modula za aplikacije i globalnih dodataka, kada se  [ponovo učitaju dodaci](#ReloadPlugins).
Ova opcija je sada podrazumevano onemogućena, što osigurava da kod koji nije testiran neće biti pokrenut bez znanja korisnika.
Ako želite da delite prilagođen kod sa drugima, morate ga upakovati kao NVDA dodatak.

##### Otvori razvojni Scratchpad folder {#AdvancedSettingsOpenScratchpadDir}

Ovo dugme otvara folder u koji možete da kopirate prilagođen kod dok ga razvijate.
Ovo dugme je omogućeno samo ako je NVDA podešen da učitava kod iz Scratchpad foldera.

##### Registracija za promene UI automation događaja i svojstava {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Automatska, selektivna, globalna|
|Podrazumevano |Automatska|

Ova opcija menja kako će NVDA registrovati događaje Microsoft UI Automation accessibility API-a.
Izborni okvir registracije za promene UI automation događaja i svojstava ima tri opcije:

* Automatska: "selektivna" na Windowsu 11 Sun Valley 2 (verzija 22H2) i novijim, "globalna" u suprotnom.
* Selektivna: NVDA će ograničiti registraciju događaja na sistemski fokus za većinu događaja.
Ako imate probleme u brzini jedne ili više aplikacija, preporučujemo da probate ovu opciju i proverite da li se brzina poboljšala.
Ali, na starijim Windows verzijama, NVDA će možda imati probleme u praćenju fokusa sa određenim kontrolama (kao što je upravljač zadacima ili emoji panel).
* Globalna: NVDA vrši registraciju mnogih UI automation događaja koji se obrađuju a zatim odbacuju u samom NVDA-u.
Iako je praćenje fokusa pouzdanije u većini situacija, performanse su dosta lošije, posebno u aplikacijama kao što je Microsoft Visual Studio.

##### Koristi UI Automation za pristup kontrolama dokumenata u programu Microsoft Word {#MSWordUIA}

Podešava da li će NVDA koristiti UI Automation API pristupačnosti za pristup Microsoft Word dokumentima, umesto starijeg objektnog Microsoft Word modela.
Ovo se primenjuje na Microsoft Word dokumente, kao i poruke u programu Microsoft Outlook.
Ovo podešavanje sadrži sledeće vrednosti:

* Podrazumevano (kada je moguće)
* Samo kada je neophodno: Kada Microsoft Word objektni model uopšte nije dostupan
* Kada je moguće: Microsoft Word verzija 16.0.15000 ili novije, ili kada Microsoft Word objektni model nije dostupan
* Uvek: Kad god je UI automation dostupan u Microsoft word-u (bez obzira koliko je ova podrška kompletna).

##### Koristi UI automation za pristup Microsoft Excel kontrolama ćelija kada je dostupan {#UseUiaForExcel}

Kada je ova opcija omogućena, NVDA će pokušati da koristi informacije iz Microsoft UI Automation accessibility API-a kako bi preuzeo informacije iz kontrola za Microsoft Excel ćelije.
Ovo je eksperimentalna opcija, i neke opcije programa Excel možda neće biti dostupne u ovom modu.
Na primer, lista elemenata programa NVDA za listanje formula u ćeliji, kao i brza navigacija u režimu pretraživanja za skakanje sa jednog polja za unos na drugo nisu dostupne.
Ali, za osnovnu navigaciju i uređivanje ćelija, ova opcija će možda doneti značajna poboljšanja u brzini.
Mi još uvek ne preporučujemo da većina korisnika ovaj način koristi kao podrazumevani, ali korisnici programa Microsoft Excel verzije 16.0.13522.10000 ili novijih su dobrodošli da testiraju ovu opciju i pruže svoje povratne informacije.
Microsoft Excel UI automation podrška se uvek menja, i starije Microsoft Office verzije od 16.0.13522.10000 možda ne pružaju dovoljno informacija da ova opcija bude uopšte korisna.

##### Koristi poboljšano obrađivanje događaja {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (omogućeno), onemogućeno, omogućeno|
|Podrazumevano |Omogućeno|

Kada je ova opcija omogućena, NVDA bi trebao da zadrži svoj odziv kada je preplavljen mnogim UI Automation događajima, na primer velike količine teksta u terminalu.
Nakon što promenite ovu opciju, morate ponovo da pokrenete NVDA kako bi promena stupila na snagu.

##### Podrška za Windows konzolu {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Automatski, UIA kada je dostupan, zastarela|
|Podrazumevano |Automatski|

Ova opcija određuje kako će NVDA vršiti interakciju sa Windows konzolom koju koriste komandna linija, PowerShell, i Windows podsistem za Linux.
Ne utiče na moderni Windows terminal.
U Windowsu 10 verziji 1709, Microsoft je [dodao podršku za svoj UI Automation API u konzolu](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), što je donelo ogromna poboljšanja u brzini i stabilnosti za čitače ekrana koji ga podržavaju.
U situacijama u kojima UI Automation nije dostupan ili je poznato da pruža lošije iskustvo, starija NVDA podrška za konzole je dostupna.
Izborni okvir za podršku za Windows konzole ima tri opcije:

* Automatski: Koristi UI Automation u verziji Windows konzole koja je uključena u Windows 11 verziju 22H2 i novije.
Ova opcija je preporučena i podrazumevano je podešena.
* UIA kada je dostupan: Koristi UI Automation u konzolama ako je dostupan, čak i za verzije sa nepotpunom podrškom ili sa greškama.
Iako ova ograničena podrška može biti korisna (čak i dovoljna za vaš način korišćenja), ovu opciju koristite u potpunosti na sopstveni rizik i podrška za nju neće biti pružana.
* Zastarela: UI Automation u Windows konzoli će u potpunosti biti onemogućen.
Zastarela podrška će se uvek koristiti čak i u situacijama u kojima bi UI Automation pružao bolje korisničko iskustvo.
Zbog toga, izbor ove opcije se ne preporučuje osim ako znate šta radite.

##### Koristi UIA podršku za Microsoft Edge i druge Chromium pretraživače kada je dostupna {#ChromiumUIA}

Dozvoljava da odredite kada će se koristiti UIA u Chromium pretraživačima kao što je Microsoft Edge.
UIA podrška za Chromium pretraživače je u ranoj fazi razvoja i možda neće pružati isti nivo pristupačnosti kao IA2.
Izborni okvir ima sledeće opcije:

* Podrazumevano (samo kada je neophodna): NVDA podrazumevano podešavanje, trenutno ovo je "samo kada je neophodna". Ovo podrazumevano podešavanje će možda biti promenjeno u budućnosti kako tehnologija bude razvijenija.
* Samo kada je neophodna: Kada NVDA ne može da ima direktan pristup procesu pretraživača i koristi IA2 a UIA podrška je dostupna, NVDA će koristiti ovu podršku.
* Da: Ako pretraživač učini da UIA podrška bude dostupna, NVDA će je koristiti.
* Ne: Ne koristi UIA podršku, čak iako NVDA nema pristup procesu. Ovo može biti korisno za programere koji žele da otkriju problem u podršci IA2 i žele da budu sigurni da NVDA neće koristiti UIA podršku.

##### Napomene {#Annotations}

Ova grupa se koristi da bi se omogućile opcije koje dodaju eksperimentalnu podršku za ARIA napomene.
Neke od ovih opcija mogu biti nepotpune.

<!-- KC:beginInclude -->
Da biste prijavili kratak opis svih detalja na poziciji kursora, pritisnite NVDA+d.
<!-- KC:endInclude -->

Sledeće opcije su dostupne: 

* "Prijavi 'ima detalje ' za strukture napomena": Omogućava prijavljivanje ako tekst ili kontrola imaju dodatne detalje.
* "Uvek prijavi aria-description opis":
  Kada je izvor `accDescription` aria-description, opis će biti prijavljen.
  Ovo je korisno za napomene na Webu.
  Napomena:
  * Postoji puno izvora za `accDescription` mnogi su simantički neispravni.
    Ranije asistivne tehnologije nisu mogle da razlikuju izvore za `accDescription` i obično nisu bili korišćeni zbog semantičkih neispravnosti.
  * Ova opcija je u veoma ranom razvoju, zavisi od opcija pretraživača koje još nisu u širokoj primeni.
  * Očekuje se da radi uz Chromium 92.0.4479.0+

##### Prijavi žive regione {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (omogućeno), onemogućeno, omogućeno|
|Podrazumevano |Omogućeno|

Ova opcija bira da li će NVDA prijaviti promene u određenom dinamičkom Web sadržaju na brajevom redu.
Onemogućavanje ove opcije je jednako ponašanju programa NVDA u verziji 2023.1 i starijim, koja je ove promene prijavljivala samo govorom.

##### Izgovaraj lozinke u svim poboljšanim terminalima {#AdvancedSettingsWinConsoleSpeakPasswords}

Ovo podešavanje kontroliše da li će se znakovi izgovarati uz podešene opcije [izgovor ukucanih znakova](#KeyboardSettingsSpeakTypedCharacters) ili [izgovor ukucanih reči](#KeyboardSettingsSpeakTypedWords) u situacijama u kojima se ekran ne ažurira (kao što su unosi lozinki) u nekim terminal programima, kao što su Windows konzola uz omogućenu UI automation podršku i Mintty.
Zbog bezbednosti, ovo podešavanje bi trebalo da ostane onemogućeno.
Ali, možda ćete želeti da ga omogućite ako primetite nestabilnosti u prijavljivanju ukucanih znakova i reči u konzolama, ili radite u sigurnim okruženjima i želite da se lozinke izgovaraju.

##### Koristi poboljšanu podršku za unos znakova u starijim Windows konzolama kada je dostupna {#AdvancedSettingsKeyboardSupportInLegacy}

Ova opcija omogućava alternativan metod za prepoznavanje ukucanih znakova u starijim Windows konzolama.
Iako poboljšava brzinu i sprečava sricanje određenih unosa u terminalu, može biti nekompatibilna sa nekim terminal aplikacijama.
Ova opcija je dostupna i podrazumevano omogućena na Windowsu 10 verzijama 1607 i novijim kada UI Automation nije dostupan ili je onemogućen.
Upozorenje: Kada je ova opcija omogućena, ukucani znakovi koji se ne pojavljuju na ekranu, kao što su lozinke, neće biti skriveni.
U nesigurnim okruženjima, možete privremeno onemogućiti [izgovor ukucanih znakova](#KeyboardSettingsSpeakTypedCharacters) i [izgovor ukucanih reči](#KeyboardSettingsSpeakTypedWords) kada kucate lozinke.

##### Algoritam razlikovanja teksta {#DiffAlgo}

Ovo podešavanje određuje kako će NVDA razlikovati novi tekst koji treba da se izgovori u Terminalu.
Ovaj izborni okvir ima sledeće opcije:

* Automatski: Ova opcija izaziva da NVDA preferira Diff Match Patch u većini situacija, ali da se vrati na Difflib u problematičnim aplikacijama, kao što su starije verzije Windows konzole i Mintty.
* Diff Match Patch: Ova opcija izaziva da NVDA računa promene u tekstu na osnovu broja znakova, čak i u situacijama u kojima to nije preporučeno.
Možda će poboljšati brzinu kada se veći delovi teksta pojavljuju u konzoli kao i poboljšati preciznost prijavljivanja promenjenih znakova u sredini reda.
Ali, u nekim aplikacijama, čitanje novog teksta može postati isprekidano ili nedosledno.
* Difflib: Ova opcija izaziva da NVDA računa promene u tekstu na osnovu redova, čak i u situacijama u kojima to nije preporučeno.
Identična je ponašanju programa NVDA u verziji 2020.4 i starijim.
Ovo podešavanje može stabilizovati čitanje teksta u nekim aplikacijama.
Ali, u terminalima, kada se znakovi ubacuju ili brišu u sredini reda, tekst nakon kursora će se pročitati.

##### Izgovaraj novi tekst u Windows terminalu koristeći {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (prepoznavanje razlika), prepoznavanje razlika, UIA obaveštenja|
|Podrazumevano |Prepoznavanje razlika|

Ova opcija kontroliše kako NVDA određuje koji tekst je "nov" (i samim tim šta da izgovara kada je "Prijavljivanje dinamičkih promena sadržaja" omogućeno) u Windows terminalu i WPF Windows terminal kontroli koja se koristi u Visual Studiju 2022.
Ne utiče na Windows konzolu (`conhost.exe`).
Izborni okvir izgovor teksta u Windows terminalu ima tri opcije:

* Podrazumevano: ova opcija je trenutno ekvivalentna opciji "Prepoznavanje razlika", ali se očekuje promena nakon što se podrška za UIA obaveštenja dodatno razvije.
* Prepoznavanje razlika: ova opcija koristi izabrani algoritam prepoznavanja razlika da izračuna promene svaki put kada terminal obradi novi tekst.
Ovo je identično ponašanju programa NVDA u verziji 2022.4 i starijim.
* UIA obaveštenja: ova opcija prenosi odgovornost određivanja koji tekst treba izgovoriti samom Windows terminalu, što znači da NVDA ne mora da odredi koji tekst trenutno na ekranu je "novi".
Ovo će značajno poboljšati stabilnost i brzinu Windows terminala, ali ova opcija još uvek nije potpuna.
Od posebne važnosti, upisani znakovi koji se ne prikazuju na ekranu, kao što su lozinke, biće prijavljeni kada se izabere ova opcija.
Takođe, neprekidni redovi izlaznog teksta dužeg od 1,000 znakova možda neće biti ispravno prijavljeni.

##### Pokušavanje otkazivanja govora za kontrole koje više nisu fokusirane {#CancelExpiredFocusSpeech}

Ova opcija će omogućiti ponašanje koje pokušava da otkaže govor za događaje koji više nisu fokusirani.
Na primer brzo pomeranje kroz poruke na lokaciji Gmail može izgovarati informacije koje više nisu tačne.
Ova funkcija je podrazumevano omogućena od NVDA verzije 2021.1.

##### Vreme pomeranja kursora (u milisekundama) {#AdvancedSettingsCaretMoveTimeout}

Ova opcija vam dozvoljava da podesite vreme za koje će NVDA čekati na kursor da se pomeri u kontrolama za uređivanje teksta.
Ako primetite da NVDA neispravno prati kursor, na primer često je iza jednog znaka ili se redovi ponavljaju, možda će pomoći povećanje ove vrednosti.

##### Prijavi transparentnost boja {#ReportTransparentColors}

Ova opcija omogućava prijavljivanje transparentnosti boja, korisno za programere dodataka za aplikacije kako bi poboljšali iskustvo korisnika uz neku aplikaciju.
Neke GDI će obeležiti tekst pozadinskom bojom, NVDA (uz display model) pokušava da prijavi ovu boju.
U nekim situacijama, pozadina teksta može da bude potpuno transparentna, a tekst da bude na nekom drugom elementu interfejsa.
Uz nekoliko istorijski popularnih API-a za interfejse, tekst može biti sa transparentnom pozadinom, ali je vizuelno pozadinska boja precizna.

##### Koristi WASAPI za zvučni izlaz {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumevano (Omogućeno), Onemogućeno, omogućeno|
|Podrazumevano |Omogućeno|

Ova opcija će omogućiti reprodukciju zvukova korišćenjem standarda Windows Audio Session API (WASAPI).
WASAPI je moderniji standard zvuka koji može poboljšati brzinu, performanse i stabilnost NVDA zvukova, što uključuje govor i NVDA zvukove.
Nakon što promenite ovu opciju, moraćete ponovo da pokrenete NVDA kako bi se promene primenile.
Ako onemogućite WASAPI sledeće opcije će takođe biti onemogućene:

* [Jačina NVDA zvukova prati jačinu glasa](#SoundVolumeFollowsVoice)
* [Jačina NVDA zvukova](#SoundVolume)

##### Kategorije za evidentiranje otklanjanja grešaka {#AdvancedSettingsDebugLoggingCategories}

Izborna polja u ovoj listi dozvoljavaju vam da omogućite određene vrste poruka u NVDA dnevniku za otklanjanje grešaka.
Evidentiranje ovih poruka može dovesti do velikih dnevnika i smanjenja brzine.
Omogućite ih samo ako ste dobili uputstva od NVDA programera, na primer za otklanjanje grešaka u radu određenih drajvera za brajev red.

##### Reprodukuj zvuk za evidentirane greške {#PlayErrorSound}

Ova opcija vam dozvoljava da odredite da li će NVDA reprodukovati zvuk kada se evidentira greška.
Izborom opcije samo u verzijama za testiranje (koja je podrazumevana) NVDA će reprodukovati zvukove za greške samo ako je trenutna verzija za testiranje (alpha, beta ili pokrenuta iz izvornog koda).
Opcija da će omogućiti zvukove za greške bez obzira na to koja je verzija.

##### Regularni izraz za navigaciju po pasusima teksta {#TextParagraphRegexEdit}

Ovo polje dozvoljava korisnicima da promene regularni izraz za prepoznavanje pasusa teksta u režimu pretraživanja.
Komanda [navigacije po pasusima teksta](#TextNavigationCommand) traži pasuse koji odgovaraju ovom izrazu.

### Razna podešavanja {#MiscSettings}

Osim dijaloga [NVDA podešavanja](#NVDASettings), podmeni opcije NVDA menija sadrži nekoliko dodatnih stavki koje su opisane ispod.

#### Govorni rečnici {#SpeechDictionaries}

Meni govornog rečnika(koji se nalazi u meniju podešavanja) sadrži dijaloge koji vam dozvoljavaju da promenite kako NVDA izgovara reči ili fraze.
Trenutno postoje tri vrste govornih rečnika.
One su:

* Podrazumevani: Pravila u ovom rečniku važe za celokupan izgovor programa NVDA.
* Glasovni: Pravila u ovom rečniku važe za glas koji se trenutno koristi.
* Privremeni: Pravila u ovom rečniku se primenjuju za celokupan govor u programu NVDA, ali samo za trenutno pokretanje. Ova pravila su privremena i biće izgubljena ako se NVDA ponovo pokrene.

Morate podesiti prilagođenu komandu koristeći [dijalog ulazne komande](#InputGestures) ako želite da otvorite neki od ovih dijaloga bilo gde.

Svi dijalozi sadrže listu pravila koja se koriste za izgovor.
Dijalog takođe sadrži tastere dodaj, uredi, ukloni i ukloni sve.

Da dodate novo pravilo u rečnik, aktivirajte dugme dodaj, popunite polja u dijalogu koji se pojavi i aktivirajte dugme u redu.
Videćete novo pravilo u listi pravila.
Ali, kako biste bili sigurni da se vaše pravilo sačuvalo, aktivirajte dugme u redu da izađete iz dijaloga rečnika kada završite sa uređivanjem i dodavanjem pravila.

Pravila za NVDA govorne rečnike vam dozvoljavaju da promenite izgovor teksta.
Na primer, možete napraviti pravilo koje govori da NVDA treba da izgovori reč"Žaba" umesto reči"Ptica" kada naiđete na reč"Ptica".
U dijalogu za dodavanje pravila, najlakši način da uradite ovo je da upišete reč ptica u polju trenutni oblik, i reč žaba u polju zamene.
Možda želite takođe da upišete opis pravila u polju za komentar(na primer: menja reč žaba u ptica).

NVDA govorni rečnici su mnogo korisniji od jednostavne zamene reči.
Dijalog za dodavanje pravila takođe sadrži izborno polje koje određuje da li pravilo treba da bude osetljivo na velika i mala slova(što znači da će NVDA obraćati pažnju na to da li su znakovi upisani velikim ili malim slovima.
NVDA ignoriše veličinu po podrazumevanim podešavanjima).

Takođe, različiti radio dugmići određuju da li će se vaš oblik primenjivati bilo gde, samo ako je cela reč ili kao"standardan izraz".
Ako podesite oblik zamene kao cela reč, ovo znači da će se oblik zameniti samo ako nije deo neke druge veće reči.
Ovaj uslov je ispunjen ako znakovi pre i posle reči nisu slova, brojevi, ili donja crta, ili ako uopšte nema znakova.
Zbog toga, ako koristimo prethodni primer menjanja reči"Ptica" sa"Žaba", ako učinite ovo zamenom celih reči, neće zameniti reči"Ptice" ili "Ptici".

Standardan izraz je poseban znak koji vam dozvoljava da promenite više znakova odjednom, ili promena svih brojeva, ili svih slova, kao nekoliko primera.
Standardni izrazi nisu uključeni u ovo uputstvo.
Za uvodni tutorijal na engleskom jeziku, molimo pročitajte [Python vodič za regularne izraze](https://docs.python.org/3.11/howto/regex.html).

#### Izgovor znakova interpunkcije/simbola {#SymbolPronunciation}

Ovaj dijalog vam dozvoljava da promenite način na koji se znakovi interpunkcije izgovaraju, kao i nivo simbola na kojem se izgovaraju.

Jezik na kome uređujete simbole će biti prikazan u naslovu dijaloga.
Napomena da ovaj dijalog poštuje opciju"Koristi jezik glasa za izgovor znakova" koja se nalazi u [kategoriji govor](#SpeechSettings) [dijaloga NVDA podešavanja](#NVDASettings); to jest koristi jezik glasa umesto jezika programa NVDA kada je ova opcija omogućena.

Da promenite znak, prvo ga izaberite u listi simbola.
Možete filtrirati simbole unosom simbola ili zamene za simbol u polje izdvoji po.

* Polje zamene vam dozvoljava da promenite tekst koji se izgovara za ovaj znak.
* Koristeći polje nivoa, možete promeniti najniži nivo na kojem se ovaj simbol izgovara (Nijedan, neki, većina ili svi).
Možete takođe da podesite nivo na znak; u tom slučaju simbol se neće izgovarati bez obzira na nivo simbola koji se koristi, uz sledeća dva izuzetka:
  * Kada se krećete znak po znak.
  * Kada NVDA sriče bilo koji tekst koji sadrži taj simbol.
* Polje za slanje simbola sintetizatoru podešava kada treba poslati simbol(umesto zamenskog teksta) sintetizatoru.
Ovo je korisno ako simbol izaziva pauzu u čitanju ili menjanje intonacije.
Na primer, zarez izaziva pauzu u čitanju.
Postoje tri opcije:
  * Nikada: Nikada ne šalji simbol sintetizatoru.
  * Uvek: Uvek šalji simbol sintetizatoru.
  * Samo ispod nivoa simbola: Pošalji simbol sintetizatoru samo ako je trenutno podešen nivo simbola niži od nivoa za ovaj simbol.
  Na primer, možda ćete koristiti ovo da simbol bude pročitan bez pauze na višim nivoima, dok se pauza koristi na nižim nivoima.

Možete dodati nove simbole koristeći dugme dodaj.
U dijalogu koji se pojavi, upišite simbol i pritisnite dugme u redu.
Zatim, promenite polja za simbol kao i za druge simbole.

Možete ukloniti znak koji ste prethodno dodali koristeći dugme ukloni.

Kada završite, pritisnite dugme u redu da sačuvate vaše promene ili otkaži da ih odbacite.

U slučaju kompleksnih simbola, polje za zamenu će možda morati da sadrži određene grupne reference ka tekstu. Na primer, za unos koji se odnosi na ceo datum, \1, \2, i \3 će morati da se pojave u polju, kako bi se zamenili odgovarajućim delovima datuma.
Zato će standardne obrnute kose crte u polju zamene morati da se dupliraju, na primer "a\\b" treba da se unese kako bi dobili "a\b" zamenu.

#### Ulazne komande {#InputGestures}

U ovom dijalogu, možete prilagoditi ulazne komande(tastere na tastaturi, tastere na brajevom реду, итд.) За НВДА команде.

Само команде које су доступне када се дијалог отвори су приказане.
На пример, ако желите да прилагодите команде режима претраживанја, отворите дијалог за улазне команде када сте у режиму претраживанја.

Приказ стабла приказује све команде груписане по категоријама.
Можете да их филтрирате уписиванјем једне или више речи имена команде у полје издвоји по.
Све команде подешене за одређену функцију су приказане поред функције.

Да додате улазну команду за неку функцију, изаберите команду и притисните дугме додај.
Затим, извршите команду коју желите да подесите; на пример притисните тастер на тастатури или брајевом реду.
Често, команда се може извршити на више начина.
На пример, ако притиснете тастер на тастатури, можда ћете желети да важи само за тренутни распоред(на пример Десктоп или Лаптоп) или ћете можда желети да буде применјен за све распореде.
У овом случају, мени ће се појавити за избор желјене опције.

Да уклоните команду са функције, изаберите функцију и притисните дугме уклони.

Kategorija emulirani tasteri sistemske tastature sadrži komande za emulaciju sistemskih tastera na tastaturi.
Ovi emulirani tasteri se mogu koristiti kako biste kontrolisali vašu tastaturu sa brajevog reda.
Da biste dodali emuliranu komandu, izaberite kategoriju emulirani tasteri sistemske tastature a zatim pritisnite dugme dodaj.
Zatim, pritisnite taster na tastaturi koji želite da emulirate.
Nakon toga, taster će biti dostupan u kategoriji emulirani sistemski tasteri i moćićete da podesite komandu za taj taster kao što je i opisano iznad.

Napomena:

* Emulirani tasteri moraju da sadrže komandu kako bi ostali sačuvani kada se dijalog zatvori.
* Ulazna komanda sa modifikatorskim tasterima možda neće moći da se podesi kao emulirana komanda bez modifikatorskih tastera.
Na primer, podešavanje emuliranog unosa 'a' i podešavanje komande 'ctrl+m', će možda izazvati
da aplikacija primi komandu 'ctrl+a'.

Када завршите са променама, притисните дугме у реду да их сачувате или откажи да их одбаците.

### Чуванје и поновно учитаванје подешаванја {#SavingAndReloading}

По подразумеваним подешаванјима НВДА ће аутоматски сачувати ваша подешаванја при излазу.
Напомена, да ова опција може бити променјена у општим подешаванјима у НВДА менију.
Да сачувате подешаванја ручно било када, изаберите ставку сачувај подешаванја у НВДА менију.

Ако некада направите грешку са вашим подешаванјима и желите да се вратите на сачувана подешаванја, изаберите ставку"врати се на сачувана подешаванја" у НВДА менију.
Такође можете вратити подешаванја на подразумевана избором опције врати подешаванја на подразумевана, која се такође налази у НВДА менију.

Следеће команде су такође корисне:
<!-- KC:beginInclude -->

| Име |Desktop команда |Laptop команда |Опис|
|---|---|---|---|
|Сачувај подешаванја |NVDA+контрол+c |NVDA+контрол+c |Чува ваша тренутна подешаванја тако да нису изгублјена када изађете из програма НВДА|
|Врати подешаванја |NVDA+контрол+r |NVDA+контрол+r |Ако се притисне једном подешаванја се враћају на сачувана. Ако се притисне 3 пута подешаванја се враћају на подразумевана.|

<!-- KC:endInclude -->

### Профили подешаванја {#ConfigurationProfiles}

Некада, можда ћете желети да имате различита подешаванја за различите ситуације.
На пример, можда ћете желети пријавлјиванје увлаченја редова уклјучено када уређујете документе или име и величину фонта када проверавате изглед докумената.
NVDA вам дозволјава да урадите ово користећи профиле подешаванја.

Профил подешаванја садржи само она подешаванја која се менјају док је профил активан.
Већина подешаванја се може променити у профилима подешаванја осим оних у kategoriji општих подешаванја dijaloga [NVDA podešavanja](#NVDASettings), која су применјена кроз цео НВДА.

Профили подешаванја могу бити ручно активирани iz dijaloga ili korišćenjem prilagođenih prečica.
Они такође могу бити активирани користећи активаторе као што су прелазак на одређену апликацију.

#### Основно управлјанје {#ProfilesBasicManagement}

Управлјате профилима избором опције"профили подешаванја" у НВДА менију.
Такође можете то урадити користећи команду:
<!-- KC:beginInclude -->

* NVDA+контрол+p: Прикажи дијалог за профиле подешаванја.

<!-- KC:endInclude -->

Прва контрола у овом дијалогу је листа профила из које можете изабрати један од доступних профила.
Када отворите дијалог, профил који тренутно уређујете је изабран.
Додатне информације су такође приказане за активне профиле, које приказују да ли је профил ручно активиран, активиран користећи активаторе или се тренутно уређује.

Да преименујете или обришете профил, активирајте тастере преименуј или обриши.

Активирајте тастер затвори да затворите дијалог.

#### Правлјенје профила {#ProfilesCreating}

Da napravite profil, aktivirajte dugme novi.

U dijalogu novog profila, možete upisati ime za novi profil.
Takođe možete izabrati kako se ovaj profil treba koristiti.
Ako želite da aktivirate ovaj profil ručno, izaberite ručna aktivacija, koja je podrazumevana.
U suprotnom, izaberite aktivator koji treba da aktivira ovaj profil.
Za lakše korišćenje, ako niste upisali ime profila, izborom aktivatora ime će biti automatski upisano.
Pogledajte deo [ispod](#ConfigProfileTriggers) za više informacija o aktivatorima.

Aktiviranje tastera u redu će zatvoriti dijalog i aktivirati profil kako biste mogli da ga uredite.

#### Ručna aktivacija {#ConfigProfileManual}

Možete ručno aktivirati profil izborom profila i aktiviranjem tastera ručne aktivacije.
Kada je aktiviran, drugi profili takođe mogu biti aktivirani koristeći aktivatore, ali bilo koje podešavanje u trenutno aktiviranom profilu će zameniti podešavanja ostalih profila.
Na primer, ako je profil aktiviran za trenutno aktivnu aplikaciju i u njemu je prijavljivanje linkova omogućeno a u ručno aktiviranom profilu je onemogućeno, linkovi neće biti prijavljeni.
Ali, ako ste promenili glas u profilu za trenutnu aplikaciju ali ga niste nikada menjali u ručno aktiviranom profilu, glas iz profila za aplikaciju će se koristiti.
Sva podešavanja koja promenite se čuvaju u ručno aktiviranom profilu.
Da deaktivirate ručno aktiviran profil, izaberite ga u listi profila i aktivirajte dugme ručne deaktivacije.

#### Aktivatori {#ConfigProfileTriggers}

Aktiviranje dugmeta aktivatori vam dozvoljava da promenite profile koji se automatski aktiviraju korišćenjem različitih aktivatora.

Lista aktivatora prikazuje dostupne aktivatore, a oni su:

* Trenutna aplikacija: Aktivira se kada pređete na određenu aplikaciju.
* Izgovori sve: Aktivira se kada čitate koristeći komandu izgovori sve.

Da promenite profil koji automatski treba da se aktivira korišćenjem aktivatora, izaberite aktivator a zatim izaberite željeni profil iz liste.
Možete izabrati"(Standardna podešavanja)" ako ne želite da se profil koristi.

Aktivirajte dugme zatvori da se vratite u dijalog profila podešavanja.

#### Uređivanje profila {#ConfigProfileEditing}

Ako ste ručno aktivirali profil, sva podešavanja koja promenite se čuvaju u taj profil.
U suprotnom, sva podešavanja koja promenite se čuvaju u poslednjem aktiviranom profilu aktiviran korišćenjem aktivatora.
Na primer, ako ste podesili profil za aplikaciju Notepad i ako pređete na nju, sva promenjena podešavanja se čuvaju u taj profil.
Međutim, ako nijedan profil nije aktiviran, sva podešavanja koja promenite se čuvaju u standardnim podešavanjima.

Da uredite profil koji se koristi za režim izgovori sve, morate [ručno aktivirati](#ConfigProfileManual) taj profil.

#### Privremeno onemogući aktivatore {#ConfigProfileDisablingTriggers}

Nekada, može biti korisno onemogućiti sve aktivatore.
Na primer, možda želite da uredite vaša standardna podešavanja bez aktivacije ostalih profila.
Ovo možete da uradite tako štoćete označiti izborno polje privremeno onemogući sve aktivatore u dijalogu profila podešavanja.

Da biste uključili ili isključili aktivatore bilo gde da se nalazite, molimo podesite prilagođenu komandu korišćenjem [dijaloga ulazne komande](#InputGestures).

#### Aktiviranje profila korišćenjem ulaznih komandi {#ConfigProfileGestures}

Za svaki profil koji dodate, možete podesiti jednu ili više prečica kako biste ga aktivirali.
Po podrazumevanim podešavanjima, profili podešavanja nemaju podešene prečice.
Možete dodati prečice za aktivaciju profila korišćenjem [dijaloga ulazne komande](#InputGestures).
Svaki profil ima svoju stavku u kategoriji profili podešavanja.
Kada promenite ime profila, sve prečice koje ste prethodno dodali će ostati dostupne.
Uklanjanje profila će automatski obrisati prečice za taj profil.

### Lokacija datoteka podešavanja {#LocationOfConfigurationFiles}

Prenosne kopije čuvaju sva podešavanja, sve prilagođene dodatke za aplikacije i drajvere u folderu userConfig, koji se nalazi u NVDA folderu.

Instalirane verzije čuvaju sva podešavanja, prilagođene drajvere i dodatke za aplikacije u folderu vašeg Windows korisničkog profila.
Ovo znači da svaki korisnik sistema može imati svoja podešavanja.
Da otvorite vaša podešavanja bilo gde da se nalazite možete da koristite [dijalog za ulazne komande](#InputGestures) da biste dodali prilagođenu komandu.
Takođe, ako ste instalirali NVDA, u start meniju možete ući u programe-> NVDA -> istraži folder sa korisničkim podešavanjima.

Podešavanja za pokretanje programa NVDA na Windows ekranu za prijavljivanje i drugim bezbednosnim ekranima se nalaze u folderu systemConfig u folderu gde je NVDA instaliran.
Obično, ova podešavanja ne treba menjati.
Da promenite NVDA podešavanja na bezbednim ekranima, podesite NVDA onako kako želite dok ste prijavljeni u Windows, sačuvajte podešavanja, a zatim aktivirajte dugme "Koristi trenutno sačuvana podešavanja na bezbednim ekranima" u kategoriji opšta u dijalogu [NVDA podešavanja](#NVDASettings).

## Dodaci i prodavnica dodataka {#AddonsManager}

Dodaci su softverski paketi koji nude nove ili izmenjene NVDA funkcije.
Razvija ih NVDA zajednica, i spoljne organizacije kao što su prodavci komercijalnih alata.
Dodaci mogu da urade bilo koju od sledećih stvari:

* Dodavanje ili poboljšanje podrške za određenu aplikaciju.
* Pružanje podrške za dodatne brajeve redove ili govorne sintetizatore.
* Dodavanje ili promenu NVDA karakteristika.

Prodavnica NVDA dodataka vam dozvoljava da istražujete ili upravljate dodacima.
Svi dodaci koji su dostupni u NVDA prodavnici dodataka mogu se preuzeti besplatno.
Ali, neki od njih mogu zahtevati od korisnika da plate za licencu ili dodatni softver pre nego što mogu da se koriste.
Primer ovakve vrste dodatka su komercijalni govorni sintetizatori.
Ako instalirate dodatak sa komponentama koje se plaćaju i promenite vaše mišljenje o tome da li želite da ga koristite, dodatak se lako može ukloniti.

Prodavnici dodataka se pristupa iz podmenija alati u NVDA meniju.
Da pristupite prodavnici bilo gde da se nalazite, podesite prilagođenu prečicu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

### Istraživanje dodataka {#AddonStoreBrowsing}

Kada se otvori, prodavnica dodataka prikazuje listu dodataka.
Ako prethodno niste instalirai nijedan dodatak, prodavnica dodataka će se otvoriti sa listom dodataka koji su dostupni za instalaciju.
Ako imate instalirane dodatke, lista će prikazati trenutno instalirane dodatke.

Kada se izabere dodatak, kretanjem do  njega strelicama gore i dole, prikazaće se detalji tog dodatka.
Dodaci imaju određene radnje kojima možete da pristupite iz [menija radnji](#AddonStoreActions), kao što su instaliraj, pomoć, onemogući  i ukloni.
Dostupne radnje će se promeniti u zavisnosti od toga da li je dodatak instaliran ili ne, i  da li je omogućen ili onemogućen.

#### Prikazi lista dodataka {#AddonStoreFilterStatus}

Postoje različiti prikazi za instalirane dodatke, dodatke koji se mogu ažurirati, dostupne i nekompatibilne dodatke.
Da biste promenili prikaz dodataka, promenite aktivnu karticu liste dodataka prečicom `ctrl+tab`.
Možete se takođe kretati tasterom `tab` do liste prikaza, i kretati se kroz njih `strelicomLevo` i `strelicomDesno`.

#### Izdvajanje omogućenih ili onemogućenih dodataka {#AddonStoreFilterEnabled}

Obično, instaliran dodatak je "omogućen", što znači da je pokrenut i dostupan u programu NVDA.
Ali, neki instalirani dodaci mogu biti "onemogućeni".
Ovo znači da se neće koristiti, i njihove funkcije neće biti dostupne u toku ove NVDA sesije.
Možda ste onemogućili dodatak zato što je bio u sukobu sa nekim drugim dodatkom, ili sa određenom aplikacijom.
NVDA će možda takođe onemogućiti određene dodatke, ako su postali nekompatibilni u toku NVDA ažuriranja; ali dobićete upozorenje ako do ovoga dođe.
Dodaci se takođe mogu onemogućiti ako vam neće trebati u dužem periodu, ali ne želite da ih uklonite zato što očekujete da će vam trebati u budućnosti.

Liste instaliranih i nekompatibilnih dodataka se mogu izdvojiti na osnovu toga da li su omogućeni ili onemogućeni.
Podrazumevano će se prikazati i omogućeni i onemogućeni dodaci.

#### Uključi nekompatibilne dodatke {#AddonStoreFilterIncompatible}

Dostupni dodaci i dodaci koji se mogu ažurirati mogu se izdvojiti tako da uključuju [nekompatibilne dodatke](#incompatibleAddonsManager) koji su dostupni za instalaciju.

#### Izdvajanje dodataka po kanalima {#AddonStoreFilterChannel}

Dodaci se mogu nudidi na do četiri kanala:

* Stabilni: Programer je objavio ovaj dodatak kao testiran sa obljavljenom NVDA verzijom.
* Beta: Ovom dodatku je možda neophodno dodatno testiranje, ali objavljen je i čeka na povratne informacije korisnika.
Predlaže se korisnicima koji žele rani pristup.
* Dev: Ovaj kanal se predlaže za korišćenje programerima dodataka kako bi testirali API promene koje još uvek nisu objavljene.
NVDA alfa testeri će možda morati da koriste "Dev" verzije dodataka.
* Eksterni: Dodaci instalirani iz spoljnih izvora, van prodavnice dodataka.

Da pogledate dodatke određenog kanala, promenite izdvajanje "kanal".

#### Pretraga dodataka {#AddonStoreFilterSearch}

Da pretražite dodatke, koristite tekstualno polje pretrage.
Možete doći do njega pritiskanjem prečice `šift+tab` iz liste dodataka.
Upišite ključnu reč ili nekoliko reči vrste dodatka koju tražite, a zatim  tasterom `tab` dođite do liste dodataka.
Dodaci će biti prikazani ako tekst pretrage bude pronađen u ID-u dodatka, prikazanom imenu, izdavaču, autoru ili opisu.

### Radnje dodatka {#AddonStoreActions}

Dodaci imaju određene radnje, kao što su instaliraj, pomoć, onemogući i ukloni.
Za dodatak u  listi dodataka, ovim radnjama se može pristupiti kroz meni koji  se otvara pritiskanjem `aplikacionog` tastera, tastera `enter`, desnim klikom ili duplim klikom na dodatak.
Ovom meniju se takođe može pristupiti pritiskanjem dugmeta radnje u detaljima izabranog dodatka.

#### Instaliranje dodataka {#AddonStoreInstalling}

Ako je dodatak dostupan u NVDA prodavnici, to ne znači da ga je proverio ili odobrio NV Access ili bilo ko drugi.
Veoma je važno da instalirate dodatke samo iz izvora kojima verujete.
Dodaci imaju neograničenu funkcionalnost u okviru programa NVDA. 
Ovo može uključiti pristup vašim ličnim podacima pa čak i celom sistemu.

Možete instalirati i ažurirati već instalirane dodatke [istraživanjem dostupnih dodataka](#AddonStoreBrowsing).
Izaberite dodatak sa kartice "dostupni dodaci" ili "dodaci koji se mogu ažurirati".
Zatim koristite radnju ažuriraj, instaliraj, ili zameni da biste započeli instalaciju.

Možete takođe instalirati više dodataka odjednom.
Ovo se može uraditi tako što ćete izabrati više dodataka na kartici dostupnih dodataka, a zatim aktivirati kontekstni meni na izboru i izabrati opciju "Instaliraj izabrane dodatke".

Da biste instalirali dodatak koji ste preuzeli van prodavnice, pritisnite dugme "Instaliraj iz eksternog izvora".
Ovo će vam dozvoliti da potražite paket sa dodatkom (`.nvda-addon` datoteku) negde na vašem računaru ili na mreži.
Nakon što otvorite paket sa dodatkom, proces instalacije će započeti.

Ako je NVDA instaliran i pokrenut na vašem sistemu, možete takođe otvoriti datoteku sa dodatkom direktno iz istraživača datoteka ili sistema da biste započeli proces instalacije.

Kada se dodatak instalira iz eksternih izvora, NVDA će zahtevati da potvrdite instalaciju.
Nakon što se dodatak instalira, NVDA mora ponovo da se pokrene kako bi dodatak bio pokrenut, ali možete da odložite ponovno pokretanje programa NVDA ako imate druge dodatke koje želite da instalirate ili ažurirate.

#### Uklanjanje dodataka {#AddonStoreRemoving}

Da biste uklonili dodatak, izaberite dodatak iz liste i koristite radnju ukloni.
NVDA će zahtevati da potvrdite uklanjanje.
Kao i u toku instalacije, NVDA mora ponovo biti pokrenut kako bi dodatak u potpunosti bio uklonjen.
Dok to ne uradite, u listi će se za taj dodatak prikazivati status "čeka na uklanjanje".
Kao i za instalaciju, možete ukloniti više dodataka odjednom.

#### Omogući ili onemogući dodatak {#AddonStoreDisablingEnabling}

Da biste onemogućili dodatak, koristite radnju "onemogući".
Da omogućite dodatak koji je prethodno bio onemogućen, koristite radnju "omogući".
Možete da onemogućite dodatak ako status dodatka prikazuje da je  "omogućen", ili omogućite ako je "onemogućen".
Nakon svakog korišćenja radnje omogući/onemogući, status dodatka će se promeniti kako bi označio šta će se desiti kada se NVDA ponovo pokrene.
Ako je dodatak prethodno bio "onemogućen", status će prikazati "omogućen nakon ponovnog pokretanja".
Ako je dodatak prethodno bio "omogućen", status će prikazati "onemogućen nakon ponovnog pokretanja".
Kao i nakon što instalirate ili uklonite dodatke, morate ponovo da pokrenete NVDA kako bi se promene primenile.
Možete takođe omogućiti ili onemogućiti više dodataka odjednom tako što ćete izabrati više dodataka na kartici sa dostupnim dodacima, zatim aktivirati kontekstni meni na izboru i izabrati odgovarajuću radnju.

#### Recenzije za dodatke i čitanje recenzija {#AddonStoreReviews}

Možda ćete želeti da pročitate recenzije drugih korisnika za dodatak, na primer pre nego što ga instalirate, ili dok učite kako da ga koristite.
Takođe, može biti od pomoći drugim korisnicima ako pružite povratne informacije o dodacima koje ste probali.
Da biste pročitali recenzije za dodatak, izaberite ga, i koristite radnju "Recenzije zajednice".
Ovo je link ka Web stranici GitHub diskusije, gde možete da čitate i pišete recenzije za dodatak.
Molimo imajte na umu da ovo ne menja direktnu komunikaciju sa programerima dodataka.
Umesto toga, svrha ove funkcije je da podelite povratne informacije koje će pomoći da drugi korisnici odluče da li je određeni dodatak koristan za njih.

### Nekompatibilni dodaci {#incompatibleAddonsManager}

Neki stariji dodaci možda neće biti kompatibilni sa NVDA verzijom koju koristite.
Ako koristite stariju NVDA verziju, neki noviji dodaci takođe možda neće biti kopmatibilni.
Pokušaj da se instalira nekompatibilan dodatak prikazaće grešku koja će objasniti zašto se dodatak smatra nekompatibilnim.

Za starije dodatke, možete da promenite kompatibilnost na sopstvenu odgovornost.
Nekompatibilni dodaci možda neće raditi uz vašu NVDA verziju, a mogu izazvati nestabilno i neočekivano ponašanje uključujući rušenja.
Možete zameniti kompatibilnost kada omogućite ili instalirate dodatak.
Ako nekompatibilan dodatak izaziva probleme, možete da ga onemogućite ili uklonite.

Ako imate probleme pri pokretanju programa NVDA, a nedavno ste ažurirali ili instalirali neki dodatak, posebno ako je to nekompatibilan dodatak, možda ćete želeti privremeno da probate da pokrenete NVDA sa svim dodacima onemogućenim.
Da biste ponovo pokrenuli NVDA sa svim dodacima onemogućenim, izaberite odgovarajuću opciju pri izlazu iz programa NVDA.
Alternativno, koristite [opciju komandne linije](#CommandLineOptions) `--disable-addons`.

Možete istražiti dostupne nekompatibilne dodatke korišćenjem [kartica dostupnih dodataka i dodataka koji se mogu ažurirati](#AddonStoreFilterStatus).
Možete istražiti instalirane nekompatibilne dodatke korišćenjem [kartice nekompatibilni dodaci](#AddonStoreFilterStatus).

## Dodatni alati {#ExtraTools}
### Pregled dnevnika {#LogViewer}

Pregled dnevnika, koji se nalazi u alatima u NVDA meniju, vam dozvoljava da pročitate svo evidentiranje u dnevniku od momenta kada je pokrenuta najnovija sesija programa NVDA.

Osim čitanja sadržaja, možete takođe sačuvati kopiju datoteke dnevnika, ili da osvežite pregled kako bi učitao novu evidenciju koja je generisana nakon što je pregled dnevnika otvoren.
Ove radnje su dostupne iz menija dnevnika u pregledu dnevnika.

Datoteka koja se prikazuje kada otvorite pregled dnevnika je sačuvana na vašem računaru na lokaciji `%temp%\nvda.log`.
Nova datoteka dnevnika se pravi kad god se NVDA pokrene.
Kada se ovo desi, dnevnik prethodne NVDA sesije se premešta u `%temp%\nvda-old.log`.

Možete takođe kopirati deo trenutne datoteke dnevnika u privremenu memoriju bez otvaranja pregleda dnevnika.
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Otvori pregled dnevnika |`NVDA+f1` |Otvara pregled dnevnika i prikazuje informacije za programere o trenutnom navigacionom objektu.|
|Kopiraj deo dnevnika u privremenu memoriju |`NVDA+kontrol+šift+f1` |Kada se ova komanda jednom pritisne, postavlja početno mesto za sadržaj dnevnika koji treba sačuvati. Kada se pritisne drugi put, kopira sadržaj dnevnika od početne tačke u privremenu memoriju.|

<!-- KC:endInclude -->

### Preglednik govora {#SpeechViewer}

Za programere bez oštećenja vida ili osobe koje pokazuju program NVDA ovakvim osobama, plutajući prozor je dostupan koji vam dozvoljava da vidite sav tekst koji NVDA izgovara.

Da omogućite preglednik govora, označite stavku"Preglednik govora" u alatima u NVDA meniju.
Kada stavka nije označena biće onemogućena.

Prozor preglednika govora takođe sadrži izborno polje"Prikaži preglednik govora pri pokretanju".
Ako je označeno, preglednik govora će se pokrenuti kada se NVDA pokrene.
Ovaj prozor će pokušati da se otvori na istoj lokaciji kao i kada je zatvoren poslednji put.

Dok je preglednik govora omogućen, stalno se ažurira da prikaže tekst koji je izgovoren.
Ali, ako pomerate vaš miš  iznad ili se fokusirate na preglednik govora, NVDA će privremeno zaustaviti ažuriranje teksta, kako biste lakše mogli da kopirate postojeći sadržaj.

Da uključite i isključite preglednik govora bilo gde, dodajte prilagođenu komandu koristeći [dijalog za ulazne komande](#InputGestures).

### Preglednik brajevog reda {#BrailleViewer}

Za programere bez oštećenja vida ili osobe koje pokazuju program NVDA ljudima bez oštećenja vida, dostupan je plutajući prozor koji vam dozvoljava da pregledate brajev izlaz, kao i tekst za svaki brajev znak.
Preglednik brajevog reda se može koristiti zajedno sa brajevim redom, imaće jednak broj ćelija kao i fizički uređaj.
Dok je preglednik brajevog reda omogućen, stalno se ažurira kako bi prikazao brajev izlaz koji bi se prikazao na fizičkom uređaju.

Da biste omogućili preglednik brajevog reda, označite opciju "Preglednik brajevog reda" iz menija alati NVDA menija.
Onemogućite ovu stavku kako bi preglednik bio onemogućen.

Brajevi redovi obično imaju tastere za pomeranje brajevog reda nazad ili napred, kako biste omogućili pomeranje sa preglednikom koristite [dijalog ulazne komande](#InputGestures) da biste podesili prečice na tastaturi sa nazivom "Pomera brajev red nazad" i "Pomera brajev red napred".

Preglednik brajevog reda sadrži opciju "Prikaži preglednik brajevog reda pri pokretanju".
Ako je označena, preglednik brajevog reda će se otvoriti kada se NVDA pokrene.
Prozor preglednika brajevog reda će uvek pokušati da se otvori na istoj lokaciji i sa istim dimenzijama kao kada je poslednji put bio zatvoren.

Prozor brajevog preglednika sadrži izborno polje "prevlačenje za prebacivanje na brajevu ćeliju", po podrazumevanim podešavanjima nije označeno.
Ako je označeno, pomeranje miša po brajevim ćelijama će aktivirati komandu "prebaci na brajevu ćeliju " za tu ćeliju.
Ovo se često koristi za pomeranje kursora ili aktiviranje radnje vezane za kontrolu.
Ovo može biti korisno kako bi se testiralo da NVDA ispravno mapira brajeve ćelije.
Kako bi se sprečilo slučajno prebacivanje na ćelije, komanda ima malo kašnjenje.
Miš se mora prevlačiti dok ne promeni boju u zelenu.
Ćelija će početi kao svetlo žuta, prebaciti se u narandžastu, a zatim postati zelena.

Kako biste isključili ili uključili preglednik brajevog reda bilo gde, molimo podesite prilagođenu komandu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

### Python konzola {#PythonConsole}

NVDA python konzola, koja se nalazi u alatima u NVDA meniju, je alat za programere koji je koristan za otklanjanje grešaka, opšti pristup programu NVDA ili pristup elementima pristupačnosti neke aplikacije.
Za više informacija, pročitajte uputstvo za programere dostupno u[delu za programere NVDA Web stranice](https://community.nvda-project.org/wiki/Development).

### Prodavnica dodataka {#toc314}

Ovo će otvoriti [prodavnicu NVDA dodataka](#AddonsManager).
Za više informacija, pročitajte obimnu sekciju: [Dodaci i prodavnica dodataka](#AddonsManager).

### Napravi prenosnu kopiju {#CreatePortableCopy}

Ova opcija otvara dijalog koji će vam dozvoliti da napravite prenosnu kopiju programa NVDA iz instalirane verzije.
U suprotnom slučaju, kada koristite prenosnu kopiju programa NVDA, u meniju sa alatima ime opcije će biti "Instaliraj NVDA na ovaj računar" umesto "Napravi prenosnu kopiju").

Oba dijaloga će vas pitati da izaberete folder u kome će se napraviti prenosna kopija ili instalirati program NVDA.

U ovom dijalogu možete da omogućite ili onemogućite sledeće opcije:

* Kopiraj trenutna korisnička podešavanja (ovo uključuje datoteke u %appdata%\roaming\NVDA ili u podešavanjima vaše prenosne kopije i uključuje dodatke i druge module)
* Pokretanje nakon kreiranja prenosne kopije ili instalacije (automatski pokreće NVDA nakon završenog kreiranja prenosne kopije ili instalacije)

### Pokreni COM Registration Fixing alatku... {#RunCOMRegistrationFixingTool}

Instalacija ili uklanjanje programa može, u određenim slučajevima, da izazove deregistraciju COM DLL datoteka.
Budući da COM interfejsi kao što su IAccessible zavise od ispravne COM DLL registracije, do problema može doći ako nedostaje ispravna registracija.

Ovo može da se desi na primer ako se instalira ili ukloni Adobe Reader, Math Player i drugi programi.

Registracije koje nedostaju mogu izazvati probleme u pretraživačima, desktop aplikacijama, programskoj traci ili drugim interfejsima.

Tačnije, sledeći problemi se mogu rešiti pokretanjem ove alatke:

* NVDA prijavljuje "nepoznato" kada se krećete u pretraživačima kao što su Firefox, Thunderbird i slično.
* NVDA se ne prebacuje između režima pretraživanja i fokusiranja
* NVDA je veoma spor kada se krećete u pretraživačima korišćenjem režima pretraživanja
* I mogući drugi problemi.

### Ponovo učitaj dodatke {#ReloadPlugins}

Ova stavka, kada se aktivira, ponovo učitava module za aplikacije i globalne dodatke bez ponovnog pokretanja programa NVDA, što može biti korisno za programere.
Moduli za aplikacije upravljaju interakcijom programa NVDA sa određenim aplikacijama.
Globalni dodaci upravljaju interakciju programa NVDA sa svim aplikacijama.

Sledeće NVDA komande takođe mogu biti korisne:
<!-- KC:beginInclude -->

| Ime |Komanda |Opis|
|---|---|---|
|Ponovo učitaj dodatke |`NVDA+kontrol+f3` |Učitava NVDA globalne dodatke i module za aplikacije.|
|Prijavi učitani modul aplikacije i izvršnu datoteku |`NVDA+kontrol+f1` |Prijavi ime modula aplikacije, ako postoji i ime izvršne datoteke aplikacije koja je fokusirana.|

<!-- KC:endInclude -->

## Podržani sintetizatori govora {#SupportedSpeechSynths}

Ovaj deo sadrži informacije o govornim sintetizatorima koje NVDA podržava.
Za opširniju listu besplatnih i komercionalnih sintetizatora koje možete preuzeti i kupiti za korišćenje sa programom NVDA, pročitajte stranicu[https://www.nvda-project.org/wiki/ExtraVoices](https://www.nvda-project.org/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

[eSpeak NG](https://github.com/espeak-ng/espeak-ng) je ugrađen u NVDA i ne zahteva posebne komponente ili drajvere.
Na Windowsu 8.1 NVDA koristi eSpeak NG po podrazumevanim podešavanjima ([Windows OneCore](#OneCore) se koristi na Windowsu 10 i novijim po podrazumevanim podešavanjima).
Budući da je ovaj sintetizator ugrađen u NVDA, ovo je odličan izbor kada se NVDA pokreće sa USB memorije na drugim sistemima.

Svaki glas koji dolazi sa sintezom Espeak NG govori drugi jezik.
Espeak NG podržava preko 43 različitih jezika.

Takođe postoji puno različitih varijanti koje menjaju zvuk glasa.

### Microsoft Speech API version 4 (SAPI 4) {#SAPI4}

SAPI 4 je stariji govorni standard za Microsoft sintetizatore.
NVDA još uvek podržava ovo za korisnike koji imaju SAPI4 sintetizatore instalirane.
Ali, Microsoft više ne podržava ovo i potrebne komponente nisu dostupne sa njihovog sajta.

Kada koristite ovaj sintetizator uz NVDA, dostupni glasovi(kojima pristupate iz [kategorije govor](#SpeechSettings) dijaloga [NVDA podešavanja](#NVDASettings)ili [krugom menjanja podešavanja sintetizatora](#SynthSettingsRing)) će sadržati sve glasove svih SAPI4 sintetizatora na vašem sistemu.

### Microsoft Speech API version 5 (SAPI 5) {#SAPI5}

SAPI 5 je Microsoftov standard za govorne sintetizatore.
Puno sintetizatora koji podržavaju ovaj standard se mogu kupiti ili besplatno preuzeti od različitih kompanija, ali vaš sistem će verovatno doći sa barem jednim SAPI5 glasom.
Kada koristite ovaj sintetizator uz NVDA, dostupni glasovi(kojima pristupate iz [kategorije govor](#SpeechSettings) u dijalogu [NVDA podešavanja](#NVDASettings)ili [krugom menjanja podešavanja sintetizatora](#SynthSettingsRing)) će sadržati sve glasove svih SAPI5 sintetizatora na vašem sistemu.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Microsoft Speech Platform Pruža glasove za razne jezike koji se obično koriste za razvoj serverskih govornih aplikacija.
Ovi glasovi se takođe mogu koristiti sa programom NVDA.

Da biste koristili ove glasove, morate da instalirate dve komponente:

* [Microsoft Speech Platform - Runtime (verzija 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime jezici (verzija 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Ova stranica sadrži različite datoteke za prepoznavanje glasa i pretvaranje teksta u govor.
 Izaberite datoteke koje sadrže TTS skraćenicu nakon određenog jezika.
 Na primer, datoteka MSSpeech_TTS_en-US_ZiraPro.msi je glas za Američki Engleski.

### Windows OneCore glasovi {#OneCore}

Windows 10 i noviji uključuju nove glasove poznati i kao "OneCore" ili "Mobilni" glasovi.
Glasovi su ponuđeni za puno jezika, i oni su brži od Microsoft glasova dostupni korišćenjem opcije Microsoft Speech API verzija 5.
Na Windowsu 10 i novijim, NVDA koristi Windows OneCore glasove po podrazumevanim podešavanjima ([eSpeak NG](#eSpeakNG) se koristi na drugim verzijama).

Da biste dodali nove Windows OneCore glasove, posetite "podešavanja govora", u Windows podešavanjima sistema. 
Koristite opciju "Dodaj glasove" i pretražite željene jezike.
Puno jezika uključuje više varijanti.
"Velika britanija" i "Australija" su dve varijante Engleskog.
"Francuska", "Kanada" i "Švajcarska" su dostupne varijante Francuskog.
Pretražite konkretan jezik (kao što su Engleski ili Francuski), a zatim pronađite varijantu u listi.
Izaberite željene jezike i koristite dugme "dodaj" da ih dodate.
Nakon što ih dodate, ponovo pokrenite NVDA.

Molimo pogledajte [Podržani jezici i glasovi](https://support.microsoft.com/sr-latn-rs/windows/appendix-a-podr%C5%BEani-jezici-i-glasovi-4486e345-7730-53da-fcfe-55cc64300f01)

## Podržani brajevi redovi {#SupportedBrailleDisplays}

Ovaj deo sadrži informacije o brajevim redovima koje NVDA podržava.

### Redovi koji podržavaju automatsko prepoznavanje u pozadini {#AutomaticDetection}

NVDA ima sposobnost da automatski prepozna puno brajevih redova, putem USB ili bluetooth veze.
Ovo se podešava izborom opcije automatski kao željeni brajev red iz NVDA [dijaloga brajeva podešavanja](#BrailleSettings).
Ova opcija je podrazumevano podešavanje.

Sledeći redovi podržavaju ovu funkciju automatskog prepoznavanja.

* Handy Tech redovi
* Baum/Humanware/APH/Orbit brajevi redovi
* HumanWare Brailliant BI/B serije
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6 serije
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille serije
* Eurobraille Esys/Esytime/Iris redovi
* Nattiq nBraille redovi
* Seika beležnica: MiniSeika (16, 24 ćelije), V6, i V6Pro (40 ćelija)
* Tivomatic Caiku Albatross 46/80 redovi
* Bilo koji red koji podržava standardni HID brajev protokol

### Brajevi redovi Freedom Scientific Focus/PAC Mate {#FreedomScientificFocus}

Svi Focus i PAC Mate redovi firme[Freedom Scientific](https://www.freedomscientific.com/) su podržani kada se povezuju putem USB ili Bluetooth veze.
Morate instalirati drajvere za freedom scientific brajeve redove.
Ako ih još uvek nemate, možete ih preuzeti sa [Focus Blue stranice drajvera za brajev red](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Iako se na ovoj stranici govori o focus blue brajevim redovima, drajveri podržavaju sve focus i Pac mate brajeve redove.

Po podrazumevanim podešavanjima, NVDA može automatski prepoznati i uspostaviti vezu sa ovim brajevim redovima ili preko USB ili preko bluetooth-a.
Međutim, Kada se brajev red povezuje na računar, možete odrediti povezivanje preko "USB-a" ili "Bluetooth-a" da biste ograničili tip veze koji će se koristiti.
Ovo može biti korisno ako želite koristiti brajev red povezan bluetooth vezom, ali ga još uvek želite puniti preko USB priključka vašeg računara.
Automatsko prepoznavanje brajevih redova programa NVDA će prepoznati ove redove putem USB ili Bluetooth veze.

Sledeća lista prikazuje sve dostupne dodeljene prečice za NVDA.
Molimo pogledajte dokumentaciju za više informacija o opisu tastera i o tome gde se nalaze.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Prebaci brajev red na prethodni red |PrviTasterZaPomeranje1 (Prva ćelija na brajevom redu)|
|Prebaci brajev red napred |toprouting20/40/80 (zadnja ćelija na brajevom redu)|
|Prebaci brajev red nazad |leviAdvanceBar|
|Prebaci brajev red napred |desniAdvanceBar|
|Prebacuj se između usmeravanja brajevog pregleda |leviGDFTaster+desniGDFTaster|
|Uključi ili isključi akciju levog wiz točka |leviWizPritisakWheel|
|Prebaci se nazad koristeći levi točak |LeviWizWheelGore|
|Prebaci se napred koristeći levi točak |leviWizWheelDole|
|Uključi ili isključi desni wizwheel taster |desniWizPritisakWheel|
|Premesti se nazad koristeći desni točak |DesniWizWheelGore|
|Premesti se napred koristeći desni točak |desniWizWheelDole|
|Prebaci se na brajevu ćeliju |routing|
|šift+tab |BrajevRazmak+tačka1+tačka2|
|tab |BrajevRazmak+tačka4+tačka5|
|strelicaGore |BrajevRazmak+tačka1|
|strelicaDole |BrajevRazmak+tačka4|
|Kontrol+strelicaLevo |BrajevRazmak+tačka3|
|Kontrol+strelicaDesno |BrajevRazmak+tačka5|
|strelicaLevo |BrajevRazmak+tačka3|
|strelicaDesno |BrajevRazmak+tačka6|
|home |BrajevRazmak+tačka1+tačka3|
|end |BrajevRazmak+tačka4+tačka6|
|kontrol+home |BrajevRazmak+tačka1+tačka2+tačka3|
|kontrol+end |BrajevRazmak+tačka4+tačka5+tačka6|
|alt |BrajevRazmak+tačka1+tačka3+tačka4|
|alt+tab |BrajevRazmak+tačka2+tačka3+tačka4+tačka5|
|alt+šift+tab taster |BrajevRazmak+tačka1+tačka2+tačka5+tačka6|
|windows+tab taster |BrajevRazmak+tačka2+tačka3+tačka4|
|escape |BrajevRazmak+tačka1+tačka5|
|windows taster |BrajevRazmak+tačka2+tačka4+tačka5+tačka6|
|razmak |BrajevRazmak|
|Uključuje i isključuje taster kontrol |BrajevRazmak+Tačka3+tačka8|
|Uključuje i isključuje taster alt |BrajevRazmak+tačka6+tačka8|
|Uključuje i isključuje taster Windows |BrajevRazmak+tačka4+tačka8|
|Uključuje i isključuje taster NVDA |BrajevRazmak+tačka5+tačka8|
|Uključuje i isključuje taster šift |BrajevRazmak+tačka7+tačka8|
|Uključuje i isključuje tastere kontrol i šift |BrajevRazmak+tačka3+tačka7+tačka8|
|Uključuje i isključuje tastere alt i šift |BrajevRazmak+tačka6+tačka7+tačka8|
|Uključuje i isključuje tastere Windows i šift |BrajevRazmak+tačka4+tačka7+tačka8|
|Uključuje i isključuje tastere NVDA i šift |BrajevRazmak+tačka5+tačka7+tačka8|
|Uključuje i isključuje tastere kontrol i alt |BrajevRazmak+tačka3+tačka6+tačka8|
|Uključuje i isključuje tastere kontrol, alt i šift |BrajevRazmak+tačka3+tačka6+tačka7+tačka8|
|windows+d (umanji sve aplikacije) |BrajevRazmak+tačka1+tačka2+tačka3+tačka4+tačka5+tačka6|
|pročitaj trenutni red |BrajevRazmak+tačka1+tačka4|
|NVDA meni |BrajevRazmak+tačka1+tačka3+tačka4+tačka5|

Za novije modele fokus brajevih redova koji na sebi imaju rocker bar tastere (focus 40, focus 80 i focus blue):

| Ime |Komanda|
|---|---|
|Premesti brajev red na prethodni red |leviRockerBarGore, desniRockerBarGore|
|premesti brajev red na sledeći red |leviRockerBarDole, desniRockerBarDole|

Samo za Focus 80:

| Ime |Komanda|
|---|---|
|Pomeri brajev red nazad na prethodni red |leviBumperBarGore, desniBumperBarGore|
|Prebaci brajev red za red u napred |leviBumperBarDole, desniBumperBarDole|

<!-- KC:endInclude -->

### Optelec ALVA 6 serije/pretvarač protokola {#OptelecALVA}

ALVA BC640 i BC680 brajevi redovi firme [Optelec](https://www.optelec.com/) podržani su kada se povezuju putem USB ili bluetooth veze.
Alternativno, možete povezati stariji Optelec brajev red, kao što je Braille Voyager, korišćenjem pretvarača protokola kojeg izdaje Optelec.
Ne morate imati specijalne drajvere da biste koristili ove brajeve redove.
Samo povežite brajev red i podesite NVDA za njegovo korišćenje.

Napomena: NVDA možda neće moći da koristi ALVA BC6 preko Bluetooth veze kada je uparen korišćenjem ALVA Bluetooth alatke.
Kada uparite ovaj uređaj korišćenjem ove alatke i NVDA ga ne prepoznaje, preporučujemo vam da uparite vaš ALVA red na standardan način korišćenjem Windows Bluetooth podešavanja.

Napomena: Iako neki od ovih redova imaju brajevu tastaturu, po podrazumevanim podešavanjima oni sami kontrolišu prevod teksta.
Ovo znači da se NVDA podešavanja ne koriste po podrazumevanim podešavanjima (na primer podešavanje ulazne tabele nema efekta).
Za ALVA redove sa novijim softverom, moguće je onemogućiti HID simulaciju tastature korišćenjem ulazne komande.

Slede komande za ovaj red sa programom NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda da biste pogledali opis i raspored tastera na brajevom redu.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red za red unazad |t1, etouch1|
|Premesti brajev red na prethodni red |t2|
|premesti na trenutni fokus |t3|
|Premesti brajev red na sledeći red |t4|
|Pomeri brajev red napred za red |t5, etouch 3|
|Prijavi formatiranje teksta ispod brajeve ćelije |secondary routing|
|Prebaci na brajevu ćeliju |routing|
|Uključuje i isključuje HID simulaciju tastature |t1+spEnter|
|premesti se na najgornji red u pregledu |t1+t2|
|premesti se na poslednji red u pregledu |t4+t5|
|prebaci brajev vezan za |t1+t3|
|pročitaj naslov |etouch2|
|pročitaj traku statusa |etouch4|
|šift+tab |sp1|
|alt |sp2, alt|
|escape |sp3|
|tab |sp4|
|strelicaGore |spUp|
|strelicaDole |spDown|
|strelicaLevo |spLeft|
|strelicaDesno |spRight|
|enter |spEnter, enter, enter|
|izgovori datum i vreme |sp2+sp3|
|NVDA meni |sp1+sp3|
|windows+d (umanji sve aplikacije) |sp1+sp4|
|windows+b taster (fokusiranje sistemske trake) |sp3+sp4|
|windows taster |sp1+sp2, windows|
|alt+tab |sp2+sp4|
|ctrl+home |t3+spUp|
|control+end |t3+spDown|
|home |t3+spLeft|
|end |t3+spRight|
|Kontrol |Kontrol|

<!-- KC:endInclude -->

### Handy Tech brajevi redovi {#HandyTech}

NVDA podržava većinu brajevih redova firme [Handy Tech](https://www.handytech.de/) kada su povezani putem USB, bluetooth veze ili putem serijskog porta.
Za starije brajeve redove, koji se povezuju USB vezom, morate instalirati Usb drajvere na vaš sistem.

Sledeći redovi nisu podržani, ali se mogu koristiti putem[Handy Techovih univerzalnih drajvera](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) i NVDA dodatka:

* Braillino
* Bookworm
* Modularni redovi sa verzijom softvera 1.13 ili nižom. Molimo imajte na umu da se softver ovih redova može ažurirati.

Slede komande za Handy Tech redove sa programom NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda da biste znali gde se određeni tasteri nalaze.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red za red unazad |levo, gore, B3|
|Pomeri brajev red za red napred |desno, dole, B6|
|Premesti brajev red na prethodni red |b4|
|Premesti brajev red na sledeći red |b5|
|Prebaci se na brajevu ćeliju |routing|
|šift+tab |esc, levi trostruki akcijski taster gore+dole|
|alt |b2+b4+b5|
|escape |b4+b6|
|tab |enter, desni trostruki akcijski taster gore+dole|
|enter |esc+enter, Levi+desni trostruki akcijski taster gore+dole, AkcijaDžojstika|
|strelicaGore |Džojstik gore|
|strelicaDole |Džojstik dole|
|StrelicaLevo |Džojstik levo|
|StrelicaDesno |Džojstik desno|
|NVDA meni |b2+b4+b5+b6|
|Menjanje vezivanja brajevog reda |b2|
|Menjanje predstavljanja sadržaja fokusa |b7|
|Uključivanje i isključivanje brajevog unosa |Razmak+b1+b3+b4 (Razmak +veliko B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

Brajev red, kojeg prodaje Italijanska firma [MDV](https://www.mdvbologna.it/) je podržan.
Ne morate imati instalirane dodatne drajvere da biste koristili ovaj brajev red.
Samo povežite brajev red i podesite NVDA za njegovo korišćenje.

Ovaj red ne podržava funkciju automatskog prepoznavanja programa NVDA.

Slede dodeljene tasterske prečice za ovaj brajev red za korišćenje sa NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda kako biste ustanovili gde se ovi tasteri nalaze, zajedno sa pripadajućim opisom.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red za red unazad |LF|
|Pomeri brajev red za red napred |RG|
|Pomeri brajev red na prethodni red |UP|
|Pomeri brajev red na sledeći red |DN|
|Pomeri se na brajevu ćeliju |route|
|Šift+tab |SLF|
|tab |SRG|
|alt+tab |SDN|
|alt+šift+tab |SUP|

<!-- KC:endInclude -->

### Baum/Humanware/APH/Orbit Brajevi Redovi {#Baum}

Nekoliko [Baumovih](https://www.baum.de/cms/en/), [HumanWare-ovih](https://www.humanware.com/), [APH-ovih](https://www.aph.org/) i [Orbitovih](https://www.orbitresearch.com/) brajevih redova su podržani kada su povezani putem usb, bluetooth ili serijske veze.
Sledeći brajevi redovi su podržani:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Neki brajevi redovi, koje je proizveo baum mogu takođe raditi, iako to nije isprobano.

Ako povezujete brajeve redove koji ne koriste hid preko usb veze, morate instalirati usb drajvere proizvođača.
VarioUltra i Pronto! brajevi redovi koriste HID.
Refreshabraille i Orbit Reader 20 mogu koristiti HID ako su podešeni na određeni način.

 USB serijski način u Orbit Reader 20 brajevom redu, trenutno je podržan samo na Windows 10 operativnom sistemu i novijim.
Umesto toga, koristite USB HID.

Slede prečice za ovaj brajev red za korišćenje uz pomoć NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda kako biste saznali listu i raspored tastera na brajevom redu.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red unazad |`d2`|
|Pomeri brajev red napred |`d5`|
|Pomeri brajev red na prethodni red |`d1`|
|Pomeri brajev red na sledeći red |`d3`|
|Pomeri se na brajevu ćeliju |`routing`|
|`šift+tab` |`Razmak+tačka1+tačka3`|
|`tab` |`Razmak+tačka4+tačka6`|
|`alt` |`Razmak+tačka1+tačka3+tačka4` (`razmak+M`)|
|`escape` |`Razmak+tačka1+tačka5` (`razmak+e`)|
|`windows` |`Razmak+tačka3+tačka4`|
|`alt+tab` |`Razmak+tačka2+tačka3+tačka4+tačka5` (`razmak+t`)|
|NVDA meni |`razmak+tačka1+tačka3+tačka4+tačka5` (`razmak+n`)|
|`windows+d` (umanji sve aplikacije) |`Razmak+tačka1+tačka4+tačka5` (`razmak+d`)|
|Izgovori sve |`Razmak+tačka1+tačka2+tačka3+tačka4+tačka5+tačka6`|

Za brajeve redove koji imaju džojstik:

| Ime |Komanda|
|---|---|
|strelicaGore |gore|
|strelicaDole |dole|
|strelicaLevo |levo|
|strelicaDesno |desno|
|enter |odabir|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

Hedo ProfiLine USB brajev red firme [hedo Reha-Technik](https://www.hedo.de/) je podržan.
Prvo morate instalirati USB drajvere koje je napravio proizvođač.

Ovaj red još ne podržava funkciju automatskog prepoznavanja programa NVDA.

Slede prečice za brajev red za korišćenje uz pomoć NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda za više informacija o rasporedu i opisu tastera na brajevom redu.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red unazad |K1|
|Pomeri brajev red napred |K3|
|Pomeri brajev red na prethodni red |B2|
|Pomeri brajev red na sledeći red |B5|
|Premesti se na brajevu ćeliju |routing|
|Prebacuj brajev vezan za |K2|
|Izgovori sve |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

Hedo MobilLine USB firme [hedo Reha-Technik](https://www.hedo.de/) je podržan.
Prvo morate instalirati USB drajvere koje je napravio proizvođač.

Ovaj red još ne podržava funkciju automatskog prepoznavanja programa NVDA.

Slede tasterske prečice za korišćenje uz pomoć NVDA.
Molimo pogledajte uputstvo za upotrebu brajevog reda kako biste saznali raspored i opis brajevih tastera na brajevom redu.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red unazad |K1|
|Pomeri brajev red napred |K3|
|Pomeri brajev red na prethodni red |B2|
|Pomeri brajev red na sledeći red |B5|
|Pomeri se na brajevu ćeliju |routing|
|Prebacuj se između brajev vezan na |K2|
|Izgovori sve |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B serije / BrailleNote Touch {#HumanWareBrailliant}

Brailliant BI i B serije brajevih redova firme [HumanWare](https://www.humanware.com/), uključujući BI 14, BI 32, BI 20X, BI 40, BI 40X i B 80, su podržani putem USB ili bluetooth veze.
Ako brajev red povezujete putem USB veze, i protokolom postavljenim na Human Ware prvo morate instalirati USB drajvere koje je napravio proizvođač.
USB drajveri nisu potrebni ako je protokol postavljen na OpenBraille.

Sledeći dodatni uređaji su takođe podržani (i nije neophodno da instalirate posebne drajvere):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Slede komande za Brailliant BI/B i BrailleNote touch redove sa programom NVDA.
Molimo pogledajte uputstvo za upotrebu ovih brajevih redova kako biste saznali opise tastera i njihov raspored.

#### Komande za sve modele {#toc334}

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red unazad |Levo|
|Pomeri brajev red napred |desno|
|Premesti brajev red na prethodni red |gore|
|Premesti brajev red na sledeći red |dole|
|Premesti se na brajevu ćeliju |routing|
|Prebacuj brajev vezan za |gore+dole|
|strelicaGore |razmak+tačka1|
|strelicaDole |razmak+tačka4|
|strelicaLevo |razmak+tačka3|
|strelicaDesno |razmak+tačka6|
|Šift+tab |razmak+tačka1+tačka3|
|tab |razmak+tačka4+tačka6|
|alt |razmak+tačka1+tačka3+tačka4 (razmak+m)|
|escape |razmak+tačka1+tačka5 (razmak+e)|
|enter |tačka8|
|windows taster |razmak+tačka3+tačka4|
|alt+tab |razmak+tačka2+tačka3+tačka4+tačka5 (razmak+t)|
|NVDA meni |Razmak+tačka1+tačka3+tačka4+tačka5 (razmak+n)|
|windows+d (Minimizuj sve aplikacije) |razmak+tačka1+tačka4+tačka5 (razmak+d)|
|Izgovori sve |razmak+tačka1+tačka2+tačka3+tačka4+tačka5+tačka6|

<!-- KC:endInclude -->

#### Komande za Brailliant BI 32, BI 40 i B 80 {#toc335}

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|NVDA meni |c1+c3+c4+c5 (komanda n)|
|windows+d (minimizuj sve aplikacije) |c1+c4+c5 (komanda d)|
|Izgovori sve |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Komande za Brailliant BI 14 {#toc336}

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Strelica gore |Džojstik gore|
|Strelica dole |džojstik dole|
|Strelica levo |Džojstik levo|
|Strelica desno |Džojstik desno|
|enter |Akcija džojstika|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE / smart beetle /Sync BrailleSerije {#Hims}

NVDA podržava Braille Sense, Braille EDGE, SMART BEETLE i Sync Braille brajeve redove firme [Hims](https://www.hims-inc.com/) kada su povezani preko USB ili Bluetooth veze. 
Ako brajev red povezujete putem USB, morate instalirati [USB Hims drajvere](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip).

Slede dodeljene prečice za ove brajeve redove za NVDA.
Molimo pogledajte uputstva za upotrebu brajevih redova kako biste saznali raspored i opis tastera na brajevom redu.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Premesti se na brajevu ćeliju |routing|
|Pomeri brajev red nazad |leftSideScrollUp, rightSideScrollUp, leftSideScroll|
|Pomeri brajev red napred |leftSideScrollDown, rightSideScrollDown, rightSideScroll|
|Pomeri brajev red na prethodni red |leftSideScrollUp+rightSideScrollUp|
|Pomeri brajev red na sledeći red |leftSideScrollDown+rightSideScrollDown|
|Premesti se na sledeći red u pregledu |rightSideUpArrow|
|Premesti se na sledeći red u pregledu |rightSideDownArrow|
|Premesti se na prethodni znak u pregledu |rightSideLeftArrow|
|Premesti se na sledeći znak u pregledu |rightSideRightArrow|
|Premesti se na trenutni fokus |leftSideScrollUp+leftSideScrollDown, rightSideScrollUp+rightSideScrollDown, leftSideScroll+rightSideScroll|
|Kontrol taster |smartbeetle:f1, brailleedge:f3|
|windows taster |f7, smartbeetle:f2|
|alt taster |Tačka1+Tačka3+Tačka4+razmak, f2, smartbeetle:f3, brailleedge:f4|
|Šift taster |f5|
|insert taster |Tačka2+Tačka4+Razmak, f6|
|Aplikacijski Taster |Tačka1+Tačka2+Tačka3+Tačka4+razmak, f8|
|Taster velika slova |Tačka1+tačka3+tačka6+razmak|
|tab taster |tačka4+tačka5+razmak, f3, brailleedge:f2|
|šift+alt+tab taster |f2+f3+f1|
|alt+tab taster |f2+f3|
|Šift+tab |Tačka1+tačka2+razmak|
|end taster |Tačka4+tačka6+razmak|
|kontrol+end taster |tačka4+tačka5+tačka6+razmak|
|home taster |tačka1+tačka3+razmak, smartbeetle:f4|
|kontrol+home |Tačka1+tačka2+tačka3+razmak|
|alt+f4 taster |tačka1+tačka3+tačka5+tačka6+razmak|
|StrelicaLevo taster |tačka3+razmak, leftSideLeftArrow|
|kontrol+šift+StrelicaLevo taster |tačka2+tačka8+razmak+f1|
|kontrol+strelicaLevo |Tačka2+razmak|
|šift+alt+StrelicaLevo taster |tačka2+tačka7+f1|
|`alt+strelicaLevo` |`tačka2+tačka7+razmak`|
|StrelicaDesno taster |tačka6+razmak, leftSideRightArrow|
|Kontrol+šift+StrelicaDesno taster |tačka5+tačka8+razmak+f1|
|kontrol+strelicaDesno |Tačka5+razmak|
|šift+alt+StrelicaDesno taster |tačka5+tačka7+f1|
|`alt+strelicaDesno` |`tačka5+tačka7+razmak`|
|pageUp |Tačka1+tačka2+tačka6+razmak|
|kontrol+pageUp |Tačka1+tačka2+tačka6+tačka8+razmak|
|StrelicaGore taster |tačka1+razmak, leftSideUpArrow|
|kontrol+šift+StrelicaGore taster |tačka2+tačka3+tačka8+razmak+f1|
|kontrol+strelicaGore |Tačka2+tačka3+razmak|
|šift+alt+StrelicaGore taster |tačka2+tačka3+tačka7+f1|
|`alt+strelicaGore` |`tačka2+tačka3+tačka7+razmak`|
|šift+StrelicaGore taster |leftSideScrollDown+razmak|
|pageDown |Tačka3+tačka4+tačka5+razmak|
|kontrol+pageDown taster |tačka3+tačka4+tačka5+tačka8+razmak|
|StrelicaDole taster |tačka4+razmak, leftSideDownArrow|
|kontrol+šift+StrelicaDole taster |tačka5+tačka6+tačka8+razmak+f1|
|kontrol+strelicaDole |Tačka5+tačka6+razmak|
|šift+alt+StrelicaDole taster |tačka5+tačka6+tačka7+f1|
|`alt+strelicaDole` |`tačka5+tačka6+tačka7+razmak`|
|šift+strelicaDole taster |razmak+rightSideScrollDown|
|escape taster |tačka1+tačka5+razmak, f4, brailleedge:f1|
|Taster za brisanje |tačka1+tačka3+tačka5+razmak, tačka1+tačka4+tačka5+razmak|
|f1 |Tačka1+tačka2+tačka5+razmak|
|f3 taster |Tačka1+tačka4+tačka8+razmak|
|f4 taster |tačka7+f3|
|windows+b taster |tačka1+tačka2+f1|
|windows+d taster |tačka1+tačka4+tačka5+f1|
|kontrol+insert taster |smartbeetle:f1+rightSideScroll|
|alt+insert taster |smartbeetle:f3+rightSideScroll|

<!-- KC:endInclude -->

### Seika brajevi redovi {#Seika}

Sledeći Seika brajevi redovi kompanije Nippon Telesoft su podržani u dve različite grupe sa različitim funkcijama:

* [Seika verzija 3, 4, i 5 (40 ćelija), Seika80 (80 ćelija)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 ćelije), V6, i V6Pro (40 ćelija)](#SeikaNotetaker)

Možete pronaći više informacija o ovim redovima na njihovoj [stranici za demonstraciju i preuzimanje drajvera](https://en.seika-braille.com/down/index.html).

#### Seika verzija 3, 4 i 5 (40 ćelija), Seika80 (80 ćelija) {#SeikaBrailleDisplays}

* Ovi redovi još ne podržavaju funkciju automatskog prepoznavanja programa NVDA.
* Izaberite "Seika brajevi redovi" za ručno podešavanje
* Drajveri za uređaj se moraju instalirati pre korišćenja Seika v3/4/5/80.
Drajveri su [ponuđeni od strane proizvođača](https://en.seika-braille.com/down/index.html).

Slede Seika pridružene komande za tastere na brajevom redu.
Molimo pogledajte uputstva za upotrebu vašeg brajevog reda da biste saznali raspored tastera i njihov opis.
<!-- KC:beginInclude -->

| Ime |komanda|
|---|---|
|pomeri brajev red nazad |levo|
|Pomeri brajev red napred |desno|
|Premesti brajev red na prethodni red |b3|
|Premesti brajev red na sledeći red |b4|
|Prebacuj se između brajev vezan za |b5|
|Izgovori sve |b6|
|tab |b1|
|Šift+tab |b2|
|alt+tab |b1+b2|
|NVDA meni |levo+desno|
|Prebaci se na brajevu ćeliju |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 ćelije), V6, i V6Pro (40 ćelija) {#SeikaNotetaker}

* NVDA podržava funkciju automatskog prepoznavanja u pozadini putem USB i Bluetooth-a.
* Izaberite "Seika beležnica" ili "automatski" za podešavanje.
* Dodatni drajveri nisu potrebni kada se koristi Seika brajeva beležnica.

Slede komande za Seika brajevu beležnicu.
Molimo pogledajte dokumentaciju brajevog reda za uputstvo gde se ovi tasteri nalaze.
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red nazad |Levo|
|Pomeri brajev red napred |desno|
|Izgovori sve |razmak+backspace|
|NVDA meni |Levo+desno|
|Pomeri brajev red na prethodni red |LJ gore|
|Pomeri brajev red na sledeći red |LJ dole|
|Menjanje vezivanja brajevog reda |LJ centar|
|tab |LJ desno|
|šift+tab |LJ levo|
|Strelica gore |RJ gore|
|Strelica dole |RJ dole|
|Strelica levo |RJ levo|
|Strelica desno |RJ desno|
|Prebaci na brajevu ćeliju |prebacivanje|
|Šift+strelica gore |Razmak+RJ gore, Backspace+RJ gore|
|šift+strelica dole |Razmak+RJ dole, Backspace+RJ dole|
|šift+strelica levo |Razmak+RJ levo, Backspace+RJ levo|
|šift+strelica desno |razmak+RJ desno, Backspace+RJ desno|
|enter |RJ centar, Tačka8|
|escape |Razmak+RJ centar|
|windows |Backspace+RJ centar|
|Razmak |Space, Backspace|
|backspace |Tačka7|
|pageup |Razmak+LJ desno|
|pageDown taster |razmak+LJ levo|
|home |space+LJ gore|
|end |razmak+LJ dole|
|kontrol+home |backspace+LJ gore|
|kontrol+end |backspace+LJ dole|

### Papenmeier BRAILLEX Noviji Modeli {#Papenmeier}

Sledeći brajevi redovi su podržani: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB i bluetooth)
* BRAILLEX Live 20, BRAILLEX Live i BRAILLEX Live Plus (USB i bluetooth)

Ovi redovi ne podržavaju funkciju automatskog prepoznavanja programa NVDA.
Postoji opcija u USB drajveru koja može da izazove problem pri učitavanju brajevog reda.
Molimo pokušajte sledeće:

1. Molimo uverite se da ste instalirali [najnoviji drajver](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Otvorite Windows upravljač uređajima.
1. U listi pronađite stavku "USB kontroleri" ili "USB uređaji".
1. Izaberite "Papenmeier Braillex USB Device".
1. Otvorite svojstva i prebacite se na karticu "Napredno".
Ponekad se kartica "Napredno" ne pojavljuje.
Ako je ovo slučaj, isključite brajev red iz računara, izađite iz programa NVDA, sačekajte trenutak i ponovo povežite brajev red.
Ponovite ovo 4 do 5 puta ako je neophodno.
Ako se kartica "Napredno" još uvek ne prikazuje, molimo restartujte računar.
1. Onemogućite "Učitaj VCP" opciju.

Većina uređaja ima taster Easy Access Bar (EAB) koji omogućava brzo i intuitivno rukovanje.
EAB može biti premeštan u četiri smera gde u glavnom svaki smer ima dva preklopnika.
C i live serije su jedine verzije koji su izuzeci od ovog pravila.

C-serija i drugi brajevi redovi imaju dva reda routing tastera gde se gornji red koristi za izveštavanje o oblikovanju teksta.
Kada držite pritisnutim jedan od gornjih routing tastera i pritiskate EAB na uređajima c-serije emulira stanje drugog preklopnika.
Brajevi redovi Live serije imaju samo jedan red routing tastera i EAB ima samo jedan korak po smeru.
Drugi se korak može izvesti tako da pritisnete jedan od routing tastera i EAB u određenom smeru.
Kad pritisnete i držite gornje, donje, desne i leve tastere (ili EAB) uzrokuje ponavljanje dodeljene akcije.

Većinom, sledeći su tasteri dostupni na ovim brajevim redovima:

| Ime |taster|
|---|---|
|l1 |Levi prednji taster|
|l2 |Levi zadnji taster|
|r1 |Desni prednji taster|
|r2 |Desni zadnji taster|
|up |1 korak prema gore|
|up2 |2 koraka gore|
|left |1 korak levo|
|left2 |2 koraka levo|
|right |1 korak desno|
|right2 |2 koraka prema desno|
|dn |1 korak prema dole|
|dn2 |2 koraka prema dole|

Ovo su Papenmeier prečice dodeljene za korišćenje sa NVDA:
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|prebaci brajev red u levo |left|
|prebaci brajev red u desno |right|
|Prebaci brajev red u prethodni red |up|
|Premesti brajev red na sledeći red |dn|
|Prebaci se na brajevu ćeliju |routing|
|Pročitaj trenutni znak u režimu pregleda |l1|
|Aktiviraj trenutni objekat navigacije |l2|
|prebacuj između brajev vezan za |r2|
|Prijavi naslov |l1+up|
|Pročitaj statusnu traku |l2+down|
|Premesti se na sadržan objekat |up2|
|Premesti se na prvi sadržani objekat |dn2|
|Prebaci se na prethodni objekat |left2|
|Prebaci se na sledeći objekat |right2|
|Prijavi formatiranje teksta ispod brajeve ćelije |gornji red routing tastera|

<!-- KC:endInclude -->

Trio model ima četiri dodatna tastera koji se nalaze na prednjoj strani brajeve tastature.
Oni su po redu, (poređani od leva prema desno):

* leva palčana tipka (lt)
* razmak
* razmak
* Desna palčana tipka (rt)

Trenutno se ne koristi desna palčana tipka.
Oba dve unutrašnje tipke su približene razmaku.

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|escape |razmak sa tačkom 7|
|strelicaGore |razmak sa tačkom 2|
|strelicaLevo |razmak sa tačkom 1|
|strelicaDesno |razmak sa tačkom 4|
|strelicaDole |razmak sa tačkom 5|
|kontrol |lt+tačka2|
|alt |lt+tačka3|
|kontrol+escape |razmak sa tačkama 1 2 3 4 5 6|
|tab |razmak sa tačkama 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BRAILLEX stariji modeli {#PapenmeierOld}

Sledeći su brajevi redovi podržani: 

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Imajte na umu da se ovi brajevi redovi mogu povezati samo preko serijskog priključka.
Zbog toga, ovi redovi ne podržavaju funkciju automatskog prepoznavanja programa NVDA.
Morate izabrati port na koji je ovaj red povezan nakon izbora ovog drajvera u dijalogu [izaberi brajev red](#SelectBrailleDisplay).

Neki od ovih uređaja imaju Easy Access Bar (EAB) taster koji omogućuje intuitivno i brzo rukovanje.
EAB se može pomerati u četiri smera gde uglavnom svaki smer ima dva preklopnika.
Kad pritiskate i držite gornji, donji, desni i levi taster (ili EAB) Prouzrokuje ponavljanje dodeljene akcije.
Stariji uređaji nemaju EAB; tasteri sa prednje strane se koriste umesto EAB.

Uobičajeno mogu se naći sledeći tasteri na brajevim redovima:

| Ime |Taster|
|---|---|
|l1 |Levi prednji taster|
|l2 |Levi zadnji taster|
|r1 |desni prednji taster|
|r2 |desni zadnji taster|
|up |1 korak prema gore|
|up2 |2 koraka gore|
|left |1 korak levo|
|left2 |2 koraka levo|
|right |1 Korak desno|
|right2 |2 Koraka desno|
|dn |1 korak prema dole|
|dn2 |2 koraka prema dole|

Slede Papenmeierove dodeljene prečice za korišćenje sa NVDA:

<!-- KC:beginInclude -->
Uređaji koji imaju EAB:

| Ime |Komanda|
|---|---|
|Pomeri brajev red nazad |left|
|Pomeri brajev red napred |right|
|Pomeri brajev red na prethodni red |up|
|Pomeri brajev red na sledeći red |dn|
|Premesti se na brajevu ćeliju |routing|
|Izgovori trenutni znak u režimu pregleda |l1|
|aktiviraj trenutni objekat navigacije |l2|
|izgovori naslov |l1up|
|Izgovori statusnu traku |l2down|
|Premesti se na sadržan objekat |up2|
|Premesti se na prvi sadržani objekat |dn2|
|Premesti se na sledeći objekat |right2|
|Prebaci se na prethodni objekat |left2|
|Prijavi formatiranje teksta ispod brajeve ćelije |Gornji routing strip|

BRAILLEX Tiny:

| Ime |Komanda|
|---|---|
|izgovori trenutni znak u režimu pregleda |l1|
|Aktiviraj trenutni objekat navigacije |l2|
|Prebaci brajev red nazad |left|
|Prebaci brajev red napred |right|
|Prebaci brajev red na prethodni red |up|
|Prebaci brajev red na sledeći red |dn|
|Prebacuj vezivanje brajevog reda na |r2|
|Prebaci se na sadržan objekat |r1+up|
|Prebaci se na prvi sadržani objekat |r1+dn|
|Prebaci se na prvi objekat |r1+left|
|Prebaci se na sledeći objekat |r1+right|
|Prijavi formatiranje teksta ispod brajeve ćelije |Gornji routing strip|
|Izgovori naslov |l1+gore|
|izgovori statusnu traku |l2+dole|

BRAILLEX 2D Screen:

| Ime |Komanda|
|---|---|
|izgovori trenutni znak u režimu pregleda |l1|
|Aktiviraj trenutni objekat navigacije |l2|
|Prebacuj brajev vezan na |r2|
|Prijavi formatiranje teksta ispod brajeve ćelije |Gornji routing strip|
|Premesti brajev red na prethodni red |up|
|Pomeri brajev red nazad |left|
|Prebaci brajev red napred |right|
|Prebaci brajev red na sledeći red |dn|
|Prebaci se na sledeći objekat |left2|
|Prebaci se na sadržan objekat |up2|
|Prebaci se na prvi sadržani objekat |dn2|
|Prebaci se na prethodni objekat |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA podržava BrailleNote elektronske beležnice firme [Humanware](https://www.humanware.com) Kada se ponašaju kao brajevi redovi za čitače ekrana.
Sledeći modeli su podržani:

* BrailleNote Classic (samo serijska veza)
* BrailleNote PK (serijska i bluetooth veza)
* BrailleNote MPower (Serijska i Bluetooth veza)
* BrailleNote Apex (USB i bluetooth veza)

Za BrailleNote Touch, molimo pogledajte sekciju [Brailliant BI serije / BrailleNote Touch](#HumanWareBrailliant).

Osim za BrailleNote PK, i brajeva (BT) i QWERTY (QT) tastature su podržane.
Za BrailleNote QT, emulacija PC tastature nije podržana.
Možete takođe upisivati brajeve tačke korišćenjem QT tastature.
Molimo pogledajte deo brajev terminal BrailleNote korisničkog uputstva za više detalja.

Ako vaš uređaj podržava više od jedne vrste veze, kada spajate vaš BrailleNote za korišćenje sa NVDA, morate postaviti priključak brajevog terminala u podešavanjima brajevog terminala.
Za više informacija, molimo pogledajte korisničko uputstvo za BrailleNote elektronsku beležnicu.
Možda ćete morati da podesite port u [dijalogu izaberi brajev red](#SelectBrailleDisplay).
Ako povezujete uređaj putem USB ili bluetooth veze, možete postaviti priključak na "Automatski", "USB" ili "Bluetooth", u zavisnosti od dostupnih opcija.
Ako za povezivanje koristite serijski priključak (ili pretvarač sa serijskog priključka na USB) ili se ne pojavljuje nijedna od prethodnih opcija, morate tačno odabrati komunikacijski priključak koji će se koristiti pri komunikaciji sa uređajem.

Pre povezivanja vašeg BrailleNote Apex uz pomoć njegovog Usb klijenta, morate instalirati drajvere koje je napravila firma Human Ware.

Na BrailleNote Apex BT, možete koristiti scroll wheel koji se nalazi između tačke 1 i 4 za različite NVDA komande.
Točak se sastoji od četiri tačke za svaki pravac, dugme u sredini za klik, i točak koji se okreće u pravcu kazaljke sata ili u suprotnom pravcu.

Slede BrailleNote prečice za korišćenje sa NVDA čitačem ekrana.
Molimo pogledajte vaše BrailleNote uputstvo za upotrebu da biste znali gde se nalaze ovi tasteri.

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Prebaci brajev red nazad |nazad|
|Prebaci brajev red napred |napred|
|Premesti brajev red na prethodni red |prethodno|
|Premesti brajev red na sledeći red |sledeće|
|Prebaci se na brajevu ćeliju |routing|
|NVDA meni |razmak+tačka1+tačka3+tačka4+tačka5 (razmak+n)|
|Prebacuj brajev vezan za |Prethodni+Sledeći|
|Strelica Gore |razmak+tačka1|
|Strelica Dole |razmak+tačka4|
|Leva Strelica |razmak+tačka3|
|Strelica desno |razmak+tačka6|
|Page up |razmak+tačka1+tačka3|
|Page down |razmak+tačka4+tačka6|
|Home |razmak+tačka1+tačka2|
|End |razmak+tačka4+tačka5|
|Kontrol+home |razmak+tačka1+tačka2+tačka3|
|Control+end |razmak+tačka4+tačka5+tačka6|
|Razmak |brajev razmak|
|Enter |Razmak +tačka8|
|Backspace |Razmak +tačka7|
|Tab |razmak+tačka2+tačka3+tačka4+tačka5 (razmak+t)|
|Šift+tab |razmak+tačka1+tačka2+tačka5+tačka6|
|Windows taster |razmak+tačka2+tačka4+tačka5+tačka6 (razmak+w)|
|Alt |razmak+Tačka1+tačka3+tačka4 (razmak+m)|
|Uključi/isključi pomoć za unos |razmak+tačka2+tačka3+tačka6 (razmak+spušteno h)|

Slede komande dodeljene za BrailleNote QT kada nije u režimu brajevog unosa.

| Ime |Komanda|
|---|---|
|NVDA meni |read+n|
|StrelicaGore |StrelicaGore|
|StrelicaDole |StrelicaDole|
|StrelicaLevo |StrelicaLevo|
|StrelicaDesno |StrelicaDesno|
|Page up taster |function+StrelicaGore|
|Page down taster |function+StrelicaDole|
|Home taster |function+StrelicaLevo|
|End taster |function+StrelicaDesno|
|kontrol+home tasteri |read+t|
|kontrol+end tasteri |read+b|
|Enter taster |enter|
|Backspace taster |backspace|
|Tab taster |tab|
|šift+tab tasteri |šift+tab|
|Windows taster |read+w|
|Alt taster |read+m|
|Uključi i isključi pomoć za unos |read+1|

Slede komande dodeljene za scroll wheel:

| Ime |Komanda|
|---|---|
|Strelica gore |StrelicaGore|
|taster strelica dole |StrelicaDole|
|taster strelica levo |StrelicaLevo|
|Taster strelica desno |StrelicaDesno|
|Taster enter |dugme u sredini|
|Taster tab |Pomeranje točka u pravcu kazaljke sata|
|Tasteri šift+tab |Pomeranje točka u suprotnom pravcu|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA podržava EcoBraille brajeve redove koje proizvodi [ONCE](https://www.once.es/).
Sledeći modeli su podržani:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

U NVDA možete podesiti port na koji će brajev red biti povezan, u [dijalogu izaberi brajev red](#SelectBrailleDisplay).
Ovi redovi ne podržavaju funkciju automatskog prepoznavanja programa NVDA.

Slede Dodeljene prečice za EcoBraille brajeve redove.
Molimo pogledajte [EcoBraille korisničko uputstvo](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) Za opis i raspored tastera na vašem brajevom redu.

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red nazad za red |T2|
|Pomeri brajev red napred za jedan red |T4|
|Pomeri brajev red na prethodnu liniju teksta |T1|
|Pomeri brajev red na sledeću liniju teksta |T5|
|Pomeri se na brajevu ćeliju |Routing|
|Aktiviraj trenutni objekat navigacije |T3|
|Prebaci se na sledeći režim pregleda |F1|
|Pomeri se na prethodni objekat |F2|
|Pomeri se na prethodni režim pregleda |F3|
|Pomeri se na prethodni objekat |F4|
|Čitaj trenutni objekat |F5|
|Prebaci se na sledeći objekat |F6|
|Premesti se na objekat koji ima fokus |F7|
|Premesti se na prvi sadržan objekat |F8|
|Premesti fokus sistema i kursor na trenutnu poziciju |F9|
|Prijavi poziciju preglednog kursora |F0|
|Uključi /isključi brajev vezan na |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

 SuperBraille uređaj, uglavnom dostupan u Tajvanu, se može povezati putem USB ili serijskog porta.
Budući da SuperBraille nema fizičke tastere za unos teksta ili pomeranje, sav unos mora se vršiti putem tastature računara.
Zbog ovoga, i zbog zadržavanja kompatibilnosti sa drugim čitačima ekrana u Tajvanu, dve komande za pomeranje brajevog reda su dodate:
<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Pomeri brajev red nazad |NumeričkiMinus|
|Pomeri brajev red napred |NumeričkiPlus|

<!-- KC:endInclude -->

### Eurobraille redovi {#Eurobraille}

b.book, b.note, Esys, Esytime i Iris brajevi redovi kompanije Eurobraille su podržani od strane NVDA.  
Ovi uređaji imaju brajevu tastaturu sa 10 tastera. 
Molimo pogledajte dokumentaciju brajevog reda za opis ovih tastera.
Od dva tastera koji izgledaju slično razmaku, levi taster je backspace i desni je razmak.

Ovi uređaji se povezuju putem USB veze i imaju jednu samostalnu USB tastaturu. 
Moguće je omogućiti ili onemogućiti ovu tastaturu menjanjem opcije "HID simulacija tastature" korišćenjem ulazne komande.
Funkcije brajeve tastature koje su opisane ispod važe kada je "HID simulacija tastature" onemogućena.

#### Funkcije brajeve tastature {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Ime |Komanda|
|---|---|
|Obriši poslednju upisanu brajevu ćeliju ili znak |`taster za brisanje nazad`|
|Prevedi bilo koji brajev unos i pritisni taster enter |`taster za brisanje nazad+razmak`|
|Uključi ili isključi `NVDA` taster |`tačka3+tačka5+razmak`|
|`insert` taster |`tačka1+tačka3+tačka5+razmak`, `tačka3+tačka4+tačka5+razmak`|
|`delete` taster |`tačka3+tačka6+razmak`|
|`home` taster |`tačka1+tačka2+tačka3+razmak`|
|`end` taster |`tačka4+tačka5+tačka6+razmak`|
|`StrelicaLevo` |`tačka2+razmak`|
|`strelicaDesno` |`tačka5+razmak`|
|`strelicaGore` |`tačka1+razmak`|
|`strelicaDole` |`tačka6+razmak`|
|`pageUp` taster |`tačka1+tačka3+razmak`|
|`pageDown` taster |`tačka4+tačka6+razmak`|
|`NumeričkiTaster1` |`tačka1+tačka6+taster za brisanje nazad`|
|`NumeričkiTaster2` |`tačka1+tačka2+tačka6+taster za brisanje nazad`|
|`NumeričkiTaster3` |`tačka1+tačka4+tačka6+taster za brisanje nazad`|
|`numeričkiTaster4` |`tačka1+tačka4+tačka5+tačka6+taster za brisanje nazad`|
|`numeričkiTaster5` |`tačka1+tačka5+tačka6+taster za brisanje nazad`|
|`numeričkiTaster6` |`tačka1+tačka2+tačka4+tačka6+taster za brisanje nazad`|
|`numeričkiTaster7` |`tačka1+tačka2+tačka4+tačka5+tačka6+taster za brisanje nazad`|
|`numeričkiTaster8` |`tačka1+tačka2+tačka5+tačka6+taster za brisanje nazad`|
|`numeričkiTaster9` |`tačka2+tačka4+tačka6+taster za brisanje nazad`|
|`NumeričkiInsert` taster |`tačka3+tačka4+tačka5+tačka6+taster za brisanje nazad`|
|`NumeričkiDecimalniZarez` |`tačka2+taster za brisanje nazad`|
|`NumeričkiTasterPodeljeno` |`tačka3+tačka4+taster za brisanje nazad`|
|`NumeričkiTasterPuta` |`tačka3+tačka5+taster za brisanje nazad`|
|`NumeričkiTasterMinus` |`tačka3+tačka6+taster za brisanje nazad`|
|`NumeričkiTasterplus` |`tačka2+tačka3+tačka5+taster za brisanje nazad`|
|`NumeričkiTasterEnter` |`tačka3+tačka4+tačka5+taster za brisanje nazad`|
|`escape` taster |`tačka1+tačka2+tačka4+tačka5+razmak`, `l2`|
|`tab` taster |`tačka2+tačka5+tačka6+razmak`, `l3`|
|`šift+tab` tasteri |`tačka2+tačka3+tačka5+razmak`|
|`printScreen` taster |`tačka1+tačka3+tačka4+tačka6+razmak`|
|`Pauza` taster |`tačka1+tačka4+razmak`|
|`aplikacioni` taster |`tačka5+tačka6+taster za brisanje nazad`|
|`f1` taster |`tačka1+taster za brisanje nazad`|
|`f2` taster |`tačka1+tačka2+taster za brisanje nazad`|
|`f3` taster |`tačka1+tačka4+taster za brisanje nazad`|
|`f4` taster |`tačka1+tačka4+tačka5+taster za brisanje nazad`|
|`f5` taster |`tačka1+tačka5+taster za brisanje nazad`|
|`f6` taster |`tačka1+tačka2+tačka4+taster za brisanje nazad`|
|`f7` taster |`tačka1+tačka2+tačka4+tačka5+taster za brisanje nazad`|
|`f8` taster |`tačka1+tačka2+tačka5+taster za brisanje nazad`|
|`f9` taster |`tačka2+tačka4+taster za brisanje nazad`|
|`f10` taster |`tačka2+tačka4+tačka5+taster za brisanje nazad`|
|`f11` taster |`tačka1+tačka3+taster za brisanje nazad`|
|`f12` taster |`tačka1+tačka2+tačka3+taster za brisanje nazad`|
|`windows` taster |`tačka1+tačka2+tačka4+tačka5+tačka6+razmak`|
|Uključi ili isključi taster `windows` |`tačka1+tačka2+tačka3+tačka4+taster za brisanje nazad`, `tačka2+tačka4+tačka5+tačka6+razmak`|
|`capsLock` taster |`tačka7+taster za brisanje nazad`, `tačka8+taster za brisanje nazad`|
|`numLock` taster |`tačka3+taster za brisanje nazad`, `tačka6+taster za brisanje nazad`|
|`Šhift` taster |`tačka7+razmak`|
|Uključi ili isključi taster `šift` |`tačka1+tačka7+razmak`, `tačka4+tačka7+razmak`|
|`kontrol` taster |`tačka7+tačka8+razmak`|
|Uključi ili isključi taster `kontrol` |`tačka1+tačka7+tačka8+razmak`, `tačka4+tačka7+tačka8+razmak`|
|`alt` taster |`tačka8+razmak`|
|Uključi ili isključi taster `alt` |`tačka1+tačka8+razmak`, `tačka4+tačka8+razmak`|
|Uključi ili isključi HID simulaciju tastature |`Prekidač1Levo+Džojstik1Dole`, `Prekidač1Desno+džojstik1Dole`|

<!-- KC:endInclude -->

#### b.book komande tastature {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Ime |taster|
|---|---|
|Pomeri brajev red nazad |`nazad`|
|Pomeri brajev red napred |`napred`|
|Prebaci se na trenutni fokus |`nazad+napred`|
|Prebaci se na brajevu ćeliju |`prebacivanje`|
|`strelicaLevo` |`džojstik2Levo`|
|`strelicaDesno` |`džojstik2Desno`|
|`strelicaGore` |`džojstik2Gore`|
|`strelicaDole` |`džojstik2Dole`|
|`enter` taster |`džojstik2Centar`|
|`escape` taster |`c1`|
|`tab` taster |`c2`|
|Uključi ili isključi taster `šift` |`c3`|
|Uključi ili isključi taster `kontrol` |`c4`|
|Uključi ili isključi taster `alt` |`c5`|
|Uključi ili isključi taster `NVDA` |`c6`|
|`kontrol+Home` |`c1+c2+c3`|
|`kontrol+End` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### b.note komande tastature {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Ime |taster|
|---|---|
|Pomeri brajev red nazad |`levaGrupaStrelicaLevo`|
|Pomeri brajev red napred |`LevaGrupaStrelicaDesno`|
|Prebaci se na brajevu ćeliju |`prebacivanje`|
|Prijavi formatiranje teksta ispod brajeve ćelije |`Dvostruko prebacivanje`|
|Prebaci se na sledeći red u pregledu |`levaGrupaStrelicaDole`|
|Prebaci se na prethodni režim pregleda |`levaGrupaStrelicaLevo+levaGrupaStrelicaGore`|
|Prebaci se na sledeći režim pregleda |`levaGrupaStrelicaDesno+levaGrupaStrelicaDole`|
|`strelicaLevo` |`desnaGrupaStrelicaDesno`|
|`strelicaDesno` |`desnaGrupaStrelicaDesno`|
|`strelicaGore` |`desnaGrupaStrelicaGore`|
|`strelicaDole` |`desnaGrupaStrelicaDole`|
|`kontrol+home` |`desnaGrupaStrelicaLevo+desnaGrupaStrelicaGore`|
|`kontrol+end` |`desnaGrupaStrelicaLevo+desnaGrupaStrelicaGore`|

<!-- KC:endInclude -->

#### Esys komande tastature {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Ime |taster|
|---|---|
|Pomeri brajev red nazad |`prekidač1Levo`|
|Pomeri brajev red napred |`prekidač1Desno`|
|Prebaci se na trenutni fokus |`Prekidač1Centar`|
|Prebaci se na brajevu ćeliju |`prebacivanje`|
|prijavi formatiranje teksta ispod brajeve ćelije |`dvostrukoPrebacivanje`|
|Prebaci se na prethodni red u  rpegledu |`džojstik1Gore`|
|Prebaci se na sledeći red u pregledu |`džojstik1Dole`|
|Prebaci se na prethodni znak u pregledu |`džojstik1Levo`|
|Prebaci se na sledeći znak u pregledu |`džojstik1Desno`|
|`strelicaLevo` |`džojstik2Levo`|
|`strelicaDesno` |`džojstik2Desno`|
|`strelicaGore` |`džojstik2Gore`|
|`strelicaDole` |`džojstik2Dole`|
|`enter` taster |`džojstik2Centar`|

<!-- KC:endInclude -->

#### Esytime komande tastature {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Ime |taster|
|---|---|
|Pomeri brajev red nazad |`l1`|
|Pomeri brajev red napred |`l8`|
|Prebaci se na trenutni fokus |`l1+l8`|
|Prebaci se na brajevu ćeliju |`prebacivanje`|
|Prijavi formatiranje teksta ispod brajeve ćelije |`dvostrukoPrebacivanje`|
|Prebaci se na prethodni red u pregledu |`džojstik1Gore`|
|Prebaci se na sledeći red u pregledu |`džojstik1Dole`|
|Prebaci se na prethodni znak u pregledu |`džojstik1Levo`|
|Prebaci se na sledeći znak u pregledu |`džojstik1Desno`|
|`strelicaLevo` |`džojstik2Levo`|
|`strelicaDesno` |`džojstik2Desno`|
|`strelicaGore` |`džojstik2Gore`|
|`strelicaDole` |`džojstik2Dole`|
|`enter` taster |`džojstik2Centar`|
|`escape` taster |`l2`|
|`tab` taster |`l3`|
|Uključi ili isključi taster `šift` |`l4`|
|Uključi ili isključi taster `kontrol` |`l5`|
|Uključi ili isključi taster `alt` |`l6`|
|Uključi ili isključi taster `NVDA` |`l7`|
|`kontrol+home` |`l1+l2+l3`, `l2+l3+l4`|
|`kontrol+end` |`l6+l7+l8`, `l5+l6+l7`|
|Uključi ili isključi HID simulaciju tastature |`l1+džojstik1Dole`, `l8+džojstik1Dole`|

<!-- KC:endInclude -->

### Nattiq nBraille redovi {#NattiqTechnologies}

NVDA podržava redove kompanije [Nattiq Technologies](https://www.nattiq.com/) kada se povežu putem USB-a.
Windows 10 i noviji prepoznaju redove kada se povežu, možda ćete morati da instalirate drajvere ako koristite starije verzije Windowsa (starije od Win10).
Možete ih preuzeti sa sajta proizvođača.

Slede komande za Nattiq Technologies redove uz NVDA.
Molimo pogledajte dokumentaciju brajevog reda da biste pročitali opise tastera kao i gde se oni nalaze.
<!-- KC:beginInclude -->

| Ime |Taster|
|---|---|
|Pomeri brajev red nazad |Gore|
|Pomeri brajev red napred |Dole|
|Pomeri brajev red na prethodni red |Levo|
|Pomeri brajev red na sledeći red |Desno|
|Prebaci se na brajevu ćeliju |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.com/) je program koji se može koristiti za podršku puno više brajevih redova.
Da biste ga mogli koristiti, morate instalirati [BRLTTY za Windows](https://www.brltty.com/download.html).
Morate preuzeti i instalirati trenutnu verziju paketa, na primer koji će biti imenovan, brltty-win-4.2-2.exe.
Kada podešavate brajev red i priključak za korišćenje, budite sigurni da strogo pratite uputstva, pogotovo ako koristite Usb brajev red i ako već imate instalirane drajvere proizvođača.

Za brajeve redove koji imaju brajevu tastaturu, BRLTTY trenutno koristi unos brajevih znakova iz samog sebe.
Zbog toga, podešavanje za ulaznu brajevu tabelu u dijalogu Brajeva podešavanja, je nebitno.

BRLTTY ne učestvuje u funkciji automatskog prepoznavanja programa NVDA.

Ovo su BRLTTY prečice za NVDA.
Molimo pogledajte [BRLTTY tabele tasterskih prečica](https://brltty.app/doc/KeyBindings/) za više informacija o tome kako su dodeljene prečice za kontrole na brajevim redovima.
<!-- KC:beginInclude -->

| Ime |BRLTTY komanda|
|---|---|
|Prebaci brajev red nazad |`fwinlt` (idi jedan prozor u levo)|
|Prebaci brajev red napred |`fwinrt` (Prebaci se jedan prozor u desno)|
|Prebaci brajev red na prethodni red |`lnup` (Idi jedan red gore)|
|Prebaci brajev red na sledeći red |`lndn` (Idi dole za jedan red)|
|Pomeri se na brajevu ćeliju |`route` (Pomeri kursor na znak)|
|Uključi ili isključi pomoć za unos |`learn` (enter/izlaz iz režima za učenje komandi)|
|Otvori NVDA meni |`prefmenu` (enter/izlaz iz menija za podešavanja)|
|Vrati podešavanja |`prefload` (vrati podešavanja sa diska)|
|Sačuvaj podešavanja |`prefsave` (sačuvaj podešavanja na disk)|
|Prijavi vreme |`time` (prikaži trenutni datum i vreme)|
|Izgovori red u kojem se nalazi pregledni kursor |`say_line` (izgovori trenutni red)|
|Izgovori sve preglednim kursorom |`say_below` (izgovori od trenutnog reda do dna ekrana)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Caiku Albatross uređaji, koje je proizvela kompanija Tivomatic i koji su dostupni u Finskoj, mogu se povezati putem USB ili serijske veze.
Ne morate da instalirate određene drajvere da biste koristili ove redove.
Jednostavno povežite red i podesite NVDA da ga koristi.

Napomena: Baud rate 19200 se posebno preporučuje.
Ako je neophodno, promenite vrednost podešavanja Baud rate na 19200 iz menija brajevog uređaja.
Iako drajver podržava 9600 baud rate, nema način da kontroliše koji baud rate red koristi.
Zato što je 19200 podrazumevani baud rate za red, drajver će ovo prvo pokušati.
Ako baud rate nisu iste, drajver će se možda ponašati neočekivano.

Slede dodeljene tasterske prečice za ovaj brajev red uz NVDA.
Molimo pogledajte dokumentaciju brajevog reda za opis gde se ovi tasteri nalaze.
<!-- KC:beginInclude -->

| Ime |Prečica|
|---|---|
|Prebaci se na prvi red pregleda |`home1`, `home2`|
|Prebaci se na poslednji red pregleda |`end1`, `end2`|
|Prebaci navigacioni objekat na trenutni fokus |`eKursor1`, `eKursor2`|
|Prebaci se na trenutni fokus |`kursor1`, `kursor2`|
|Pomera miš na trenutni navigacioni objekat |`home1+home2`|
|Postavlja navigacioni objekat na trenutni objekat ispod pokazivača miša i izgovara ga |`end1+end2`|
|Pomera fokus na trenutni navigacioni objekat |`eKursor1+eKursor2`|
|Menja vezivanje brajevog reda |`kursor1+kursor2`|
|Pomera brajev red na prethodni red |`gore1`, `gore2`, `gore3`|
|Pomera brajev red na sledeći red |`dole1`, `dole2`, `dole3`|
|Pomera brajev red nazad |`levo`, `lTočakLevo`, `DTočakLevo`|
|Pomera brajev red napred |`desno`, `lTočakDesno`, `DTočakDesno`|
|Prebaci na brajevu ćeliju |`Prebacivanje`|
|Prijavi formatiranje teksta ispod brajeve ćelije |`Sekundarno prebacivanje`|
|Prebacuje načine predstavljanja sadržaja na brajevom redu |`atribut1+atribut3`|
|Kruži kroz režime govora |`atribut2+atribut4`|
|Prelazi na prethodni režim pregleda (npr. objekat, dokument ili ekran) |`f1`|
|Prelazi na sledeći režim pregleda (npr. objekat, dokument ili ekran) |`f2`|
|Pomera navigacioni objekat na objekat koji ga sadrži |`f3`|
|Pomera navigacioni objekat na prvi objekat unutar njega |`f4`|
|Pomera navigacioni objekat na prethodni objekat |`f5`|
|Pomera navigacioni objekat na sledeći objekat |`f6`|
|Prijavljuje trenutni navigacioni objekat |`f7`|
|Daje informacije o lokaciji teksta ili objekta na poziciji sistemskog kursora |`f8`|
|Prikazuje brajeva podešavanja |`f1+home1`, `f9+home2`|
|Čita statusnu traku i prebacuje navigacioni objekat na nju |`f1+end1`, `f9+end2`|
|Kruži kroz oblike brajevog kursora |`f1+eKursor1`, `f9+eKursor2`|
|Uključuje ili isključuje brajev kursor |`f1+kursor1`, `f9+kursor2`|
|Kruži kroz režime prikazivanja brajevih poruka |`f1+f2`, `f9+f10`|
|Menja stanje prikazivanja izbora na brajevom redu |`f1+f5`, `f9+f14`|
|Kruži kroz stanja opcije "Brajevo pomeranje sistemskog kursora kada se prebacuje pregledni kursor" |`f1+f3`, `f9+f11`|
|Izvršava podrazumevanu radnju na trenutnom navigacionom objektu |`f7+f8`|
|Prijavljuje datum/vreme |`f9`|
|obaveštava o statusu baterije i preostalom vremenu ako punjač nije uključen |`f10`|
|Prijavljuje naslov |`f11`|
|Prijavljuje statusnu traku |`f12`|
|Prijavljuje trenutni red ispod kursora za aplikacije |`f13`|
|Izgovori sve |`f14`|
|Prijavljuje trenutni znak preglednog kursora |`f15`|
|Prijavljuje red trenutnog navigacionog objekta gde se nalazi pregledni kursor |`f16`|
|Izgovara reč trenutnog navigacionog objekta gde se nalazi pregledni kursor |`f15+f16`|
|Pomera pregledni kursor na prethodni red trenutnog navigacionog objekta i izgovara ga |`lTočakGore`, `dTočakGore`|
|Pomera pregledni kursor na naredni red trenutnog navigacionog objekta i izgovara ga |`lTočakDole`, `dTočakDole`|
|`Windows+d` prečica (prebaci se na radnu površinu) |`atribut1`|
|`Windows+e` prečica (ovaj računar) |`atribut2`|
|`Windows+b` prečica (fokusiranje na sistemsku traku) |`atribut3`|
|`Windows+i` prečica (Windows podešavanja) |`atribut4`|

<!-- KC:endInclude -->

### Standardni HID brajevi redovi {#HIDBraille}

Ovo je eksperimentalan brajev drajver za novi HID brajev standard, na koji su se 2018 složile različite kompanije kao što su Microsoft, Google, Apple i različiti proizvođači asistivnih tehnologija uključujući i NV Access. 
Cilj je da svi budući brajevi redovi od bilo kog proizvođača, zajedno koriste ovaj protokol što će ukloniti potrebu za posebne drajvere svakog proizvođača.

Automatsko prepoznavanje brajevih redova od strane programa NVDA će takođe raditi za sve redove koji koriste ovaj protokol.

Slede trenutne tasterske prečice za ove redove.
<!-- KC:beginInclude -->

| Ime |komanda|
|---|---|
|Pomeri brajev red nazad |pan levo ili rocker gore|
|Pomeri brajev red napred |pan desno ili rocker dole|
|Prebaci na brajevu ćeliju |routing set 1||
|Promeni vezivanje brajevog reda |Gore+Dole|
|Strelica gore |Džojstik gore, strelica gore ili razmak+tačka1|
|Strelica dole |Džojstik dole, strelica dole ili razmak+tačka4|
|Strelica levo |Razmak+tačka3, džojstik levo ili strelica levo|
|Strelica desno |Razmak+tačka6, džojstik desno ili strelica desno|
|Šift plus tab |razmak+tačka1+tačka3|
|tab |Razmak+tačka4+tačka6|
|alt |Razmak+tačka1+tačka3+tačka4 (razmak+m)|
|escape |Razmak+tačka1+tačka5 (razmak+e)|
|enter |tačka8, centar džojstika ili centralna strelica|
|windows |Razmak+tačka3+tačka4|
|alt+tab |Razmak+tačka2+tačka3+tačka4+tačka5 (razmak+t)|
|NVDA meni |Razmak+tačka1+tačka3+tačka4+tačka5 (razmak+n)|
|windows+d (umanji sve aplikacije) |Razmak+tačka1+tačka4+tačka5 (razmak+d)|
|Izgovori sve |Razmak+tačka1+tačka2+tačka3+tačka4+tačka5+tačka6|

<!-- KC:endInclude -->

## Napredne teme {#AdvancedTopics}
### Bezbedan način rada {#SecureMode}

Administratori sistema će možda želeti da podese NVDA tako da mu se ograniči neovlašćen pristup sistemu.
NVDA dozvoljava instalaciju prilagođenih dodataka, koji mogu da izvrše i pokrenu kod, što uključuje kada NVDA ima administratorske privilegije.
NVDA takođe dozvoljava korisnicima da pokrenu kod kroz NVDA Python konzolu.
NVDA bezbedan režim sprečava da korisnici menjaju njihova NVDA podešavanja, i na druge načine ograničava pristup sistemu.

NVDA se pokreće u bezbednom načinu rada na [bezbednim ekranima](#SecureScreens), osim ako se ne omogući `serviceDebug` [sistemski parametar](#SystemWideParameters).
Da naterate NVDA da se uvek pokrene u bezbednom režimu, podesite `forceSecureMode` [sistemski parameta](#SystemWideParameters).
NVDA se takođe može pokrenuti u bezbednom režimu uz `-s` [opciju komandne linije](#CommandLineOptions).

Bezbedan način rada će onemogućiti:

* Čuvanje konfiguracije i drugih podešavanja na disku
* Čuvanje mape komandi na disku
* Opcije [profila podešavanja](#ConfigurationProfiles) kao što su pravljenje, brisanje, preimenovanje profila i slično.
* Učitavanje prilagođenih foldera podešavanja korišćenjem [`-c` opcije komandne linije](#CommandLineOptions)
* Ažuriranje programa NVDA i pravljenje prenosnih kopija
* [Prodavnicu dodataka](#AddonsManager)
* [NVDA Python konzolu](#PythonConsole)
* [Preglednik dnevnika](#LogViewer) i evidentiranje u dnevniku
* [Pregled brajevog reda](#BrailleViewer) i [Pregled govora](#SpeechViewer)
* Otvaranje eksternih dokumenata iz NVDA menija, kao što su korisničko uputstvo ili datoteku saradnika.

Instalirane kopije programa NVDA čuvaju podešavanja uključujući dodatke u `%APPDATA%\nvda`.
Da biste sprečili NVDA korisnike da direktno izmene podešavanja ili dodatke, korisnički pristup ovom folderu se takođe mora ograničiti.

Bezbedan režim nema efekta u prenosnim NVDA kopijama.
Ovo ograničenje takođe važi za privremenu kopiju programa NVDA koja se pokreće pri pokretanju instalacije.
U bezbednim okruženjima, korisnik koji može da pokrene prenosivu izvršnu datoteku predstavlja isti bezbednosni rizik bez obzira na bezbedni režim.
Očekuje se od administratora sistema da ograniče pokretanje neautorizovanog softvera na sistemu, što uključuje prenosne NVDA kopije.

NVDA korisnici često zavise od podešavanja njihovog NVDA profila kako bi zadovoljio njihove potrebe.
Ovo može uključiti instalaciju i podešavanje prilagođenih dodataka, koje treba pregledati nezavisno od programa NVDA.
Bezbedni režim će onemogućiti promene podešavanja, tako da prvo treba osigurati da je NVDA podešen pre nego što prisilite bezbedan režim.

### Bezbedni ekrani {#SecureScreens}

NVDA se pokreće u [bezbednom načinu rada](#SecureMode) kada je pokrenut na bezbednim ekranima osim ako je omogućen `serviceDebug` [sistemski parametar](#SystemWideParameters).

Kada je pokrenut sa bezbednog ekrana, NVDA koristi sistemski profil za podešavanja.
NVDA korisnička podešavanja se mogu kopirati [za korišćenje na bezbednim ekranima](#GeneralSettingsCopySettings).

Bezbedni ekrani uključuju:

* Windows ekran za prijavljivanje
* Dijalog kontrole korisničkog naloga, koji je aktivan kada se izvršava neka radnja kao administrator
  * Ovo uključuje instalaciju programa

### Opcije komandne linije {#CommandLineOptions}

NVDA može prihvatiti jednu ili više opcija kada se pokreće koje menjaju njegovo ponašanje.
Možete proslediti onoliko opcija koliko vam je potrebno.
Ove opcije mogu biti prosleđene kada pokrećete preko prečice(u svojstvima prečice), iz dijaloga pokreni(start meni-> pokreni ili Windows+r) ili iz Windows komandne linije.
Opcije trebaju biti odvojene od imena glavne datoteke programa NVDA i od drugih opcija razmacima.	
na primer, korisna opcija je `--disable-addons`, koja govori programu NVDA da onemogući sve pokrenute dodatke.
Ovo vam dozvoljava da proverite da li je neki od dodataka izazvao problem i da rešite ozbiljne probleme izazvane od strane dodataka.

Kao primer, možete izaći iz prethodno pokrenute kopije programa NVDA upisivanjem sledećeg u dijalog za pokretanje:

    nvda -q

Neke opcije komandne linije imaju kratku i dugu verziju, dok neke imaju samo dugu verziju.
Za one koje imaju kratku verziju, možete ih kombinovati ovako:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Ovo će pokrenuti NVDA bez zvukova i poruke o pokretanju, i sa određenom konfiguracijom|
|`nvda -mc CONFIGPATH --disable-addons` |Isto kao iznad, ali sa onemogućenim dodacima|

Neke opcije prihvataju dodatne parametre; na primer koliko detaljna evidencija u dnevniku treba da bude ili adresa za korisnička podešavanja.
Ovi parametri se postavljaju nakon opcije odvojeni razmakom, kada se koristi kratka verzija ili znakom jednako(`=`) kada se koristi duga verzija; na primer.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Govori programu NVDA da se pokrene sa evidencijom u dnevniku podešenom na otklanjanje grešaka|
|`nvda --log-file=c:\nvda.log` |Govori programiu NVDA da piše svoje dnevnike u `c:\nvda.log`|
|`nvda --log-level=20 -f c:\nvda.log` |Govori programu NVDA da se pokrene sa evidencijom u dnevniku podešenom na informacije i da piše datoteke sa dnevnikom na lokaciji c:\NVDA.log|

Slede opcije komandne linije za NVDA:

| Kratka |Duga |Opis|
|---|---|---|
|`-h` |`--help` |Prikaži pomoć komandne linije i izađi|
|`-q` |`--quit` |Izađi iz već pokrenute kopije programa NVDA|
|`-k` |`--check-running` |Prijavi da li je NVDA pokrenut korišćenjem koda izlaza; 0 ako je pokrenut, 1 ako nije pokrenut|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |Datoteka u kojoj poruke dnevnika trebaju biti pisane. Evidentiranje dnevnika je uvek onemogućeno u bezbednom režimu|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |Najniži nivo evidencije poruka(otklanjanje grešaka 10, ulaz/izlaz 12, upozorenje o otklanjanju grešaka 15, info 20, onemogućeno 100). Evidentiranje dnevnika je uvek onemogućeno ako je bezbedni režim omogućen|
|`-c CONFIGPATH` |`--config-path=CONFIGPATH` |Adresa na kojoj podešavanja za NVDA trebaju biti sačuvana. Podrazumevana vrednost je prisiljena ako je bezbedni režim omogućen|
|Nema |`--lang=Jezik` |Promena podešenog NVDA jezika. Kada je podešen na "Windows" koristi se trenutni korisnički podrazumevani, "en" za Engleski, i slično.|
|`-m` |`--minimal` |Nema zvukova, nema interfejsa, nema poruka pokretanja i tako dalje|
|`-s` |`--secure` |Pokreće NVDA u [bezbednom načinu rada](#SecureMode)|
|Nema |`--disable-addons` |Dodaci neće imati efekta|
|Nema |`--debug-logging` |Omogući evidenciju otklanjanja grešaka za ovo pokretanje. Ovo podešavanje će promeniti ostale nivoe evidencije( ``--loglevel``, `-l`) uključujući kada je evidentiranje onemogućeno.|
|Nema |`--no-logging` |Onemogući evidentiranje dok se NVDA koristi. Ovo podešavanje se može zameniti ako nivo evidentiranja ( ``--loglevel``, `-l`) bude određen iz komandne linije ili se dnevnici za otklanjanje grešaka uključe.|
|Nema |`--no-sr-flag` |Ne menjaj globalnu oznaku čitača ekrana na sistemu|
|Nema |`--install` |Instalira NVDA(i pokreće novo instaliranu kopiju)|
|Nema |`--install-silent` |Tiha instalacija programa NVDA(ne pokreće novo instaliranu kopiju)|
|Nema |`--enable-start-on-logon=True` |`False` |U toku instalacije, omogući podešavanje [pokreni NVDA na Windows ekranu za prijavljivanje](#StartAtWindowsLogon)|
|Nema |`--copy-portable-config` |Kada instalirate, kopira podešavanja iz označene adrese (`--config-path, -c`) u trenutni korisnički nalog|
|Nema |`--create-portable` |Pravi prenosnu kopiju programa NVDA (pokreće se automatski nakon pravljenja). Zahteva opciju `--portable-path` koja određuje adresu kopije|
|Nema |`--create-portable-silent` |Pravi prenosnu kopiju programa NVDA (bez pokretanja nakon završetka). Zahteva opciju `--portable-path` koja određuje adresu kopije|
|Nema |`--portable-path=AdresaKopije` |Adresa na kojoj će prenosna kopija biti napravljena|

### Sistemski parametri {#SystemWideParameters}

NVDA dozvoljava promenu određenih vrednosti u sistemskoj registry bazi koje menjaju ponašanje programa NVDA.
Ove vrednosti se čuvaju u registry bazi u jednom od sledećih ključeva:

* 32-bitni system: "`HKEY_LOCAL_MACHINE\SOFTWARE\nvda`"
* 64-bitni system: "`HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`"

Sledeće vrednosti se mogu podesiti u ovom registry ključu:

| Ime |Vrsta |Moguće vrednosti |Opis|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (Podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućeno, Čuva NVDA podešavanja u lokalnim podacima aplikacija umesto roming podataka|
|`serviceDebug` |DWORD |0 (podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućen, biće onemogućen [bezbedan način rada](#SecureMode) na [bezbednim ekranima](#SecureScreens). Zbog nekoliko ogromnih bezbednosnih rizika, korišćenje ove opcije se ne preporučuje|
|`forceSecureMode` |DWORD |0 (podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućeno, nateraće NVDA da koristi [bezbedan režim](#SecureMode) pri pokretanju.|

## Dodatne informacije {#FurtherInformation}

Ako vam trebaju dodatne informacije ili pomoć za program NVDA, molimo posetite [NVDA Websajt](NVDA_URL).
Ovde, možete pronaći dodatnu dokumentaciju, kao i tehničku podršku i mesta zajednice.
Ovaj sajt takođe pruža informacije o razvoju programa NVDA.
