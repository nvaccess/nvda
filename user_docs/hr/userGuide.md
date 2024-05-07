# NVDA NVDA_VERSION – Priručnik za korisnike

[TOC]

<!-- KC:title: NVDA NVDA_VERSION – Pregled tipkovničkih prečaca -->



## Uvod {#Introduction}

Dobrodošli u NVDA!

NonVisual Desktop Access (NVDA) je besplatan čitač ekrana otvorenog koda za operacijski sustav Microsoft Windows.
Pružajući povratne informacije pomoću sintetičkog govora i brajice, NVDA omogućuje slijepim osobama i osobama s oštećenjem vida pristup računalima s operacijskim sustavom Windows za cijenu koja nije veća od one koju plaćaju korisnici koji vide.
NVDA razvija organizacija [NV Access](https://www.nvaccess.org/), uz doprinose zajednice.

### Glavne značajke {#GeneralFeatures}

NVDA omogućuje slijepim i slabovidnim osobama pristup i interakciju s operacijskom sustavu Windows te mnogim aplikacijama trećih strana.

Kratka video demonstracija, ["što je NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) dostupna je na NV Access youtube kanalu.

Glavne značajke uključuju:

* podrška za poznate programe uključujući web preglednike, klijente elektroničke pošte, programe za čavrljanje putem interneta i uredske pakete
* ugrađena govorna jedinica koja podržava preko 80 jezika
* izvještavanje o oblikovanju teksta, gdje je to podržano, kao što su ime fonta, informacije o bojama, stil i pravopisne pogreške
* automatska najava teksta ispod pokazivača miša i opcionalna zvučna indikacija o položaju miša
* podrška za mnoge brajične retke, uključujući podršku za automatsko otkrivanje brajičnih redaka kao i podršku brajičnog unosa na brajičnim redcima pomoću brajične tipkovnice
* mogućnost pokretanja s USB memorijskih stickova ili drugih prijenosnih medija bez instaliranja samog čitača ekrana
* govorni instalacijski program koji je jednostavan za korištenje
* preveden na 54 jezika
* podrška za moderne operacijske sustave Windows u 32 i 64 bitnim verzijama
* Mogućnost pokretanja prilikom prijavljivanja te na [sigurnim zaslonima](#SecureScreens).
* najavljivanje kontrola i teksta pri korištenju dodirnih gesti
* podrška za uobičajena sučelja za pristupačnost, kao što su Microsoft Active Accessibility, Java Access Bridge, IAccessible2 i UI Automation
* podrška za Windowsov naredbeni redak i druge aplikacije koje rade u naredbenom retku
* mogućnost isticanja fokusa sustava

### Preduvjeti za pokretanje NVDA čitača {#SystemRequirements}

* Operacijski sustavi: sva 32-bitna i 64-bitna izdanja sustava Windows 8.1, Windows 10, Windows 11 i svih serverskih operacijskih sustava, počevši od Windows Server 2008 R2.
  * Obje inačice,  AMD64 kao i ARM64 operacijskog sustava Windows su podržane.
* Najmanje 150 MB prostora na tvrdom disku.

### Internacionalizacija {#Internationalization}

Vrlo je važno da ljudi bilo gdje u svijetu i bez obzira na jezik kojim govore, imaju jednak pristup tehnologiji.
Osim engleskog, NVDA je preveden na 54 jezika, uključujući: hrvatski, afrikanerski, albanski, amharski, arapski, aragonski, brazilski portugalski, bugarski, katalonski, kolumbijski španjolski, češki, danski, nizozemski, perzijski, finski, francuski, galicijski, grčki, gruzijski, njemački, švicarski njemački, hebrejski, hindi, mađarski, islandski, irski, talijanski, japanski, kirgizki, korejski, litavski, makedonski, mongolski, burmanski, nepalski, norveški, poljski, portugalski, pendžabski, rumunjski, ruski, srpski, slovački, slovenski, španjolski, švedski, tamilski, tajski, tradicionalni i pojednostavljeni kineski, turski, ukrajinski i vijetnamski.

### Podrška za govornu jedinicu {#SpeechSynthesizerSupport}

Osim podrške za mnoge jezike, NVDA može omogućiti korisniku čitanje sadržaja na bilo kojem jeziku, sve dok korisnik ima govornu jedinicu za taj određeni jezik.

NVDA dolazi s besplatnom, višejezičnom govornom jedinicom otvorenog koda [eSpeak NG](https://github.com/espeak-ng/espeak-ng).

Informacije o drugim govornim jedinicama koje NVDA podržava mogu se pronaći u poglavlju [Podržane govorne jedinice](#SupportedSpeechSynths).

### Podrška za brajične retke {#BrailleSupport}

Za korisnike koji posjeduju brajični redak, NVDA može prikazati informacije brajicom.
NVDA koristi brajični prevoditelj otvorenog koda [LibLouis](https://liblouis.io/) za pretvaranje teksta u brajične znakove.
Podržan je i unos brajice putem brajične tipkovnice, koristeći kratkopis, puno pismo te osmotočkastu brajicu.
Čak štoviše, NVDA će standardno automatski pronaći brajične retke.
Za informacije o podržanim brajičnim redcima pogledajte poglavlje [Podržani brajični redci](#SupportedBrailleDisplays).

NVDA podržava brajične kodove za mnoge jezike, uključujući kratkopis, puno pismo i kompjutorsku brajicu.

### Licenca i autorska prava {#LicenseAndCopyright}

NVDA autorska prava NVDA_COPYRIGHT_YEARS NVDA doprinositelji.

NVDA je dostupan pod uvjetima  GNU opće javne licence (verzija 2) uz dvije važne iznimke.
Iznimke su istaknute u dokumentu licence u poglavljima "Non-GPL Components in Plugins and Drivers" i "Microsoft Distributable Code". Bilješka: dokument je dostupan samo na engleskom.
NVDA takđer uključuje i koristi komponente koje su dostupne pod drugim besplatnim i licencama otvorenog koda.
Dozvoljeno je dijeljenje i promjena ovog softvera na koji god način želite, sve dok je popraćen licencom i dok omogućite pristup izvornom kodu bilo kome tko ga želi.
Ovo se odnosi na originalni i promijenjeni softver, kao i na rad koji je iz toga proizašao.

Za pojedinosti [pogledajte cijelu licencu.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Za detalje o iznimkama, molimo pročitajte dokument licence kojeg možete naći u NVDA izborniku u podizborniku "pomoć".

## NVDA vodič za brzo pokretanje {#NVDAQuickStartGuide}

Ovaj vodič za brzo pokreanje sadrži tri glavna poglavlja: preuzimanje, početno postavljanje, te pokretanje NVDA.
Poslje tih poglavlja slijede informacije o prilagođavanju postavki, sudjelovanje u zajednici te kako dobiti pomoć.
Informacije u ovom vodiču skupljene su iz drugih djelova priručnika za NVDA.
ZA više detaljnijih informacija, molimo pogledajte priručnik za korisnike i svaku njegovu rubriku.

### Preuzimanje NVDA {#GettingAndSettingUpNVDA}

NVDA je putpuno besplatan za svakog tko ga želi koristiti.
Ne postoji niti licenčni ključ o kojem trebate brinuti, niti skupa pretplata koju trebate plaćati.
NVDA se u prosjeku ažurira tri puta godišnje.
Posljednja NVDA inačica je dostupna na "stranici Download" glavne web stranice  [NV Access website](NVDA_URL), organizacije koja razvija NVDA.

NVDA radi u svim posljednjim verzijama operacijskog sustava Windows.
Za više detalja, molimo pogledajte [Preduvjete za pokretanje](#SystemRequirements).

#### Koraci za preuzimanje NVDA {#StepsForDownloadingNVDA}

Ovi koraci podrazumjevaju da ste upoznati sa načinom kretanja po web stranici.

* Otvorite vaš internetski preglednik (pritisnite `Windows` tipku, napišite riječ "internet" bez navodnika, te pritisnite `enter`)
* Otvorite NV Access stranicu za preuzimanje (pritisnite `alt+d`, napišite the sljedeću adresu i pritisnite `enter`): 
https://www.nvaccess.org/download 
* Aktivirajte gumb "download"
* Preglednik može, ali i ne mora prikazati dijaloški okvir u kojem ćete biti pitani za akciju koja će se izvršiti nakon preuzimanja, te će će preuzimanje započeti
* Ovisno o internetskom pregledniku, datoteka se može automatski pokrenuti poslije preuzimanja
* Ako datoteka mora biti ručno pokrenuta, pritisnite `alt+n` kako biste se premjestili na područje obavijesti, a potom `alt+r` kako biste pokrenuli datoteku (ili slične korake koji se primjenjuju u vašem web pregledniku)

### Postavljanje NVDA {#SettingUpNVDA}

Pokrenete li datoteku koju ste upravo preuzeli, pokrenut će se privremena kopija NVDA čitača.
Tada će vas NVDA pitati želite li instalirati NVDA, izraditi prijenosnu kopiju ili nastaviti koristiti privremenu kopiju.

Jednom kada se pokrene NVDA program za pokretanje, internetski pristup nije više potreban.
Ako je internetska veza dostupna, biti ćete u mogućnosti nadograđivati NVDA.

#### Koraci za pokretanje preuzetog programa za pokretanje {#StepsForRunningTheDownloadLauncher}

Datoteka nosi ime "nvda_2022.1.exe" ili slično.
Godina i verzija se mijenjaju, kako bi ste znali da se izmjene odnose baš na tu verziju.

1. Pokrenite preuzetu datoteku.
Prilikom pokretanja instalacijskog programa, začut ćete glazbenu datoteku.
Jednom kada se pokrene, NVDA će govoriti tijekom cijelog procesa.
1. Pojavit će se proces NVDA programa za pokretanje sa tekstom licencnog ugovora.
Pritišćite `strelicu dolje` kako biste pročitali licencni ugovor ako želite.
1. Pritišćite `tab` kako biste se pomaknuli na potvrdni okvir "Prihvaćam", a potom pritisnite `razmaknicu` kako biste ga odabrali.
1. Pritišćite `tab` kako biste se premještali između opcija, a potom pritisnite `enter` na željenoj opciji.

Opcije su slijedeće: 

* "Instaliraj NVDA na ovom računalu": Ovo je opcija koju većina korisnika želi zbog jednostavnog korištenja NVDA. 
* "Stvori prijenosnu kopiju": Ovo omogućuje postavljenje NVAD u bilo koju mapu bez instalacije.
Ovo je korisno na računalima bez administratorskih prava, te na Usb stickovima u svrhu nošenja sa sobom.
Kada ej ova opcija označena, NVDA će vas voditi kroz korake za stvaranje prijenosne kopije.
Glavna informacija koja je potrebna NVDA je mapa u kojoj će biti smještena njegova prijenosna kopija. 
* "Nastavi pokretanje": Ovo ostavlja pokrenutu privremenu kopiju.
Ovo je korisno prilikom testiranja novih značajki nove verzije prije instalacije.
Kada je ova opcija odabrana, prozor programa za pokretanje se zatvara a privremena kopija NVDA nastavlja s radom sve dok ne bude ugašena ili računalo ne bude isključeno.
Imajte na umu da se postavke neće sačuvati u ovoj kopiji. 
* "Odustani": Ovo zatvara NVDA bez izvođenja bilo koje radnje.

Ako planirate koristiti NVDA na ovom računalu, htjeti ćete ga instalirati.
Kada instalirate NVDA, dobit ćete značajke poput automatskog pokretanja poslije prijave, mogućnost čitanja zaslona za prijavu i druge [sigurne zaslone](#SecureScreens).
Ovo nije moguće u prijenosnim i privremenim kopijama.
Za više informacija o ograničenjima prijenosnih i privremenih kopija NVDA, molimo pogledajte poglavlje [Ograničenja prijenosne i privremene kopije](#PortableAndTemporaryCopyRestrictions).

Instalacija također omogućuje automatsko pokretanje NVDA, te također omogućuje pokretanje koristeći prečac `control+alt+f5`.

#### Koraci za instalaciju NVDA iz programa za pokretanje {#StepsForInstallingNVDAFromTheLauncher}

Ovi će vas koraci voditi kroz najuobičajenijih opcija za postavljanje.
Za više informacija o dostupnim opcijama, molimo pogledajte [Opcije instalacije](#InstallingNVDA).

1. Uvjerite se da je potvrdni okvir za prihvaćanje licence odabran.
1. `Pritišćite tab` te aktivirajte gumb "Instaliraj NVDA na ovo računalo".
1. Slijede opcije za stvaranje prečaca na radnoj površini, te za automatsko pokretanje NVDA.
One su podrazumjevano odabrane.
Ako želite, pritišćite `tab` i `razmaknicu` za promjenu bilo koje od tih opcija, ili ih ostavite na podrazumjevanim vrijednostima.
1. Pritisnite `enter` za nastavak.
1. Dijaloški okvir kontrole korisničkog računa (UAC)" pojavit će se s pitanjem "Želite li dozvoliti ovoj aplikaciji vršenje izmjena na na ovom računalu?".
1. Pritisnite `alt+d` kako biste prihvatili upit dialoškog okvira UAC.
1. Traka napredka se popunjava tijekom NVDA instalacije.
U toku tog procesa, NVDA reproducira zvučni signal povišene frekvencije.
Ovaj proces je često brz i i neprimjetno brz.
1. Pojavljuje se dijaloški okvir koji obavještava korisnika o uspješnoj instalaciji.
U poruci se savjetuje korisnika da "pritisne Ok kako bi pokrenuo instaliranu kopiju".
Pritisnite `enter` kako biste pokrenuli instaliranu kopiju.
1. Pojavljuje se dijaloški okvir "Dobrodošli u NVDA" te NVDA čita poruku dobrodošlice.
Fokus se nalazi u polju raspored tipkovnice.
Podrazumjevano, "raspored za stolna računala" koristi numeričku tipkovnicu za većinu funkcija.
Ako želite, pritisnite `strelicu dolje` kako biste odabrali "raspored za prijenosna računala" kako biste funkcijama na numeričkom dijelu dodjelili druge tipke.
1. Pritisnite `tab` kako biste se premjestili na opciju "Koristi `capsLock` kao NVDA modifikacijsku tipku".
`Insert` ke postavljen kao zadana modifikacijska tipka.
Pritisnite `razmaknicu` kako biste odabrali `capsLock` kao alternativnu modifikacijsku tipku.
Imajte na umu da se raspored tipkovnice postavlja odvojeno od NVDA modifikacijske tipke.
NVDA tipka i raspored tipkovnice mogu se kasnije promijeniti u postavkama tipkovnice.
1. Koristite `tab` i `razmaknicu` kako biste prilagodili ostale opcije na tom zaslonu.
One određuju način automatskog pokretanja.
1. Pritisnite `enter` kako biste zatvorili dijaloški okvir sa pokrenutim programom NVDA.

### Pokretanje NVDA {#RunningNVDA}

Potpun vodič za korisnike sadrži sve prečace programa NVDA, podijejljene po raznim kategorijama za lakše čitanje.
Tablice sa prečacima su također dostupne u "brzom prikazu NVDA prečaca".
Modul "Osnovna obuka za korištenje NVDA" detaljno opisuje kroz svaki prečac sa aktivnostima korak po korak.
"Osnovna obuka za korištenje NVDA" dostupna je u [NV Access trgovini](http://www.nvaccess.org/shop).

Ovdje se nalaze često korišteni prečaci.
Svi su prečaci podesivi, što zčači da su ovo podrazumjevani prečaci.

#### NVDA modifikacijska tipka {#NVDAModifierKey}

NVDA modifikacijska tipka je jedna od sljedećih tipki: Tipka `uumerička nula`, (sa isključenim `numLockom`), ili `insert` tipka, blizu tipke `delete`, `home` i `end` tipki.
`capsLock` tipka može biti postavljena kao NVDA modifikacijska tipka.

#### Pomoć tipkovnice {#InputHelp}

Kako biste naučili raspored svake tipke, pritisnite `NVDA+1` kako biste uključili pomoć tipkovnice.
Sve dok se nalazite u načinu pomoći tipkovnice, izvođenje bilo koje ulazne geste, poput pritiska tipke ili izvođenja dodirne geste) će izgovoriti koju radnju izvršava (ako je pridjeljena).
Prečaci se neće izvršavati sve dok se nalazite u ovom načinu. 

#### Pokretanje i zaustavljanje NVDA {#StartingAndStoppingNVDA}

| Naziv |Prečac za stolna računala |Prečac za prijenosna računala |opis|
|---|---|---|---|
|Pokreni NVDA |`control+alt+f5` |`control+alt+f5` |Pokreće ili ponovno pokreće NVDA|
|Zaustavljanej programa NVDA |`NVDA+q`, potom `enter` |`NVDA+q`, potom `enter` |izlazi iz programa NVDA|
|Pauzira ili ponovno pokreće govor |`shift` |`shift` |Brzo pauzira govor. Ponovnim pritiskom govor nastavlja tamo gdje je stao|
|Zaustavlja govor |`control` |`control` |Brzo zaustavlja govor|

#### Čitanje teksta {#ReadingText}

| Naziv |Prečac za stolna računala |Prečac za prijenosna računala |opis|
|---|---|---|---|
|Čitaj sve |`NVDA+strelica dolje` |`NVDA+a` |Čita sve istovremeno pomičući kursor|
|Čitaj trenutni redak |`NVDA+strelica gore` |`NVDA+l` |Čita redak. Kada se pritisne dvaput, redak se slovka. Kada se pritisne tri puta slovka redak fonetski (alan, biokovo, cavtat, itd)|
|Čitaj označeno |`NVDA+shift+strelica gore` |`NVDA+shift+s` |Čita bilo koji označeni tekst. Kada se pritisne dvaput, informacija se slovka. Kada se pritisne tri put, informacija se slovka uz pomoć opisa znakova|
|Čitaj tekst u međuspremniku |`NVDA+c` |`NVDA+c` |Čita bilo koji tekst u međuspremniku. Kada se pritisne dvaput, informacija se slovka. Kada se pritisne tri put, informacija se slovka uz pomoć opisa znakova|

#### Čitanje lokacije i drugih informacija {#ReportingLocation}

| Naziv |Prečac za stolna računala |Prečac za prijenosna računala |opis|
|---|---|---|---|
|Naslovna traka |`NVDA+t` |`NVDA+t` |Čita naslovnu traku trenutno aktivnog prozora. Pressing Kada se pritisne dvaput, informacija će biti slovkana. Kada se pritisne tri put, informacija će biti kopirana u međuspremnik|
|Izgovori fokus |`NVDA+tab` |`NVDA+tab` |Izgovara trenutnu kontrolu u fokusu.  Kada se pritisne dvaput, slovka informaciju Kada se pritisne tri put, informacija se slovka fonetski.|
|Pročitaj prozor |`NVDA+b` |`NVDA+b` |Čita cijeli trenutni prozor (korisno za dijaloške okvire)|
|Pročitaj traku stanja |`NVDA+end` |`NVDA+shift+end` |Čita traku stanja ako ju NVDA pronađe. Kada se pritisne dva puta, informacija će biti slovkana. Kada se pritisne tri put, informacija će biti kop8irana u međuspremnik|
|Pročitaj vrijeme |`NVDA+f12` |`NVDA+f12` |Ako se pritisne jedamput čita se trenutno vrijeme, ako se pritisne dva puta čita se datum. Vrijeme i datum se čitaju u  skladu sa oblikovanjem datuma i vremena postavljenom za sat u području obavijesti.|
|Pročitaj informacije o oblikovanju teksta |`NVDA+f` |`NVDA+f` |Čita informacije o oblikovanju teksta. Kada se pritisne dva put, informacija se prikazuje u prozoru|
|Čitaj odredište poveznice |`NVDA+k` |`NVDA+k` |Kada se pritisne jednom, izgovara adresu odredišne poveznice na trenutnoj poziciji kursora sustava. Kada se pritisne dvaput, prikazuje poveznicu u prozoru za pažljiviji pregled|

#### Regulacija informacija koje čita NVDA {#ToggleWhichInformationNVDAReads}

| Naziv |Prečac za stolna računala |Prečac za prijenosna računala |opis|
|---|---|---|---|
|Čitaj upisane znakove |`NVDA+2` |`NVDA+2` |kadae je ova opcija uključena, NVDA če izgovarati sve upisane znakove na tipkovnici.|
|Izgovaraj upsane riječi |`NVDA+3` |`NVDA+3` |Kada je ova opcija uključena, NVDA će izgovarati sve riječi napisane na tipkovnici.|
|Čitaj naredbene tipke |`NVDA+4` |`NVDA+4` |Kada je ova opcija uključena, NVDA će izgovarati sve naredbene tipke na tipkovnici. Ovo uključuje kombinacije tipaka kao što su to control plus neko slovo.|
|Uključi praćenje miša |`NVDA+m` |`NVDA+m` |Kada je ova opcija uključena, NVDA će izgovarati tekst pod pokazivačem miša, u isto vrijeme kada ga pomićete. Ovo vam omogućuje nalaženje opcija na zaslonu fizički pomičući miša umjesto traženja opcija objektnom navigacijom.|

#### Prsten govorne jedinice {#TheSynthSettingsRing}

| Naziv |Prečac za stolna računala |Prečac za prijenosna računala |opis|
|---|---|---|---|
|Premjesti se na sljedeću postavku govorne jedinice |`NVDA+control+Strelica desno` |`NVDA+shift+control+strelica desno` |Premješta na sljedeću postavku govorne jedinice poslije aktivne postavke, ponovno se vraćajući na prvu postavku poslije posljednje|
|Premjesti se na prethodnu postavku govorne jedinice |`NVDA+control+strelica lijevo` |`NVDA+shift+control+strelica lijevo` |Premješta na sljedeću postavku govorne jedinice prije aktivne postavke, ponovno se vraćajući na prvu postavku poslije posljednje|
|Povećaj vrijednost postavke govorne jedinice |`NVDA+control+strelica gore` |`NVDA+shift+control+strelica gore` |Povećava vrijednost trenutne postavke govorne jedinice na kojoj se nalazite. Npr: Povećava brzinu, bira sljedeći glas, povećava glasnoću|
|Povećaj  postavku govorne jedinice u većim koracima |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Povećava vrijednost trenutne postavke govora na kojoj se nalazite u većim koracima. Na primjer kada se nalazite na postavci glasa, premještavat ćete se svakih dvadeset glasova; kada se nalazite na postavci sa klizačem (brzina, visina, itd.) postavka će se promijeniti za 20%|

|Smanji postavku govorne jedinice |`NVDA+control+strelica dolje` |`NVDA+shift+control+strelica dolje` |smanjuje vrijednost trenutne postavke govorne jedinice na kojoj se nalazite. Npr: smanjuje brzinu, bira prethodni glas, smanjuje glasnoću|
|Smanji postavku govorne  jedinice u većim koracima |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Smanjuje vrijednost trenutne postavke govorne jedinice na kojoj se nalazite u većim koracima. Na primjer kada se nalazite na postavci glas, prebacivat ćete se u nazad za dvadeset glasova; kada se nalazite na postavci klizača, prebacivat ćete se između opcija za 20%.|

Također je moguće postaviti prvu ili zadnju postavku govorne jedinice. Za to morate dodijeliti prilagođeni prečac [u postavkama ulaznih gesti](#InputGestures), u kategoriji govor.
Ovo znači da kada se nalazite na postavci brzine brzina će se postaviti na nula ili sto posto.
Kada se nalazite na postavci glasa, biti će postavljen prvi ili zadnji glas.

#### Kretanje po Web stranicama {#WebNavigation}

Puni se popis brzih tipki nalazi u poglavlju [Modus pregleda](#BrowseMode) korisničkog priručnika.

| Komanda |Prečac |Opis|
|---|---|---|
|Naslov |`h` |Premještava na sljedeći naslov|
|Naslov razine 1, 2, ili 3 |`1`, `2`, `3` |Premješta na naslov određene razine|
|Polje obrasca |`f` |Premješta na sljedeće polje obrasca (polje za uređivanje, gumb, itd)|
|veza |`k` |Premješta na sljedeću poveznicu|
|orjentir |`d` |premještava na sljedeći orjentir|
|popis |`l` |premješta na sljedeći popis|
|Tablica |`t` |Premješta na sljedeću tablicu|
|Premješta u nazad |`shift+slovo` |Pritisnite `shift` i bilo koje od slóva kako biste se premjestili na prethodni element tog tipa|
|Popis elemenata |`NVDA+f7` |Popisuje razne tipove elemenata, poput poveznica i naslova|

### Postavke {#Preferences}

Većina NVDA funkcija može biti omogućena ili izmjenjena uz pomoć NVDA postavki.
Postavke i druge opcije dostupne su u NVDA izborniku.
Kako biste otvorili NVDA izbornik, pritisnite `NVDA+n`.
Kako biste izravno otvorili NVDA opće postavke, pritisnite `NVDA+control+g`.
Većina NVDA ekrana postavki ima pripadajuće prečace za izravno otvaranje, kao što je to `NVDA+control+s` za postavke govorne jedinice, ili `NVDA+control+v` za ostale glasovne postavke.

### Zajednica {#Community}

NVDA ima živu zajednicu korisnika. 
Postoji glavna [Mailing lista na engleskom jeziku](https://nvda.groups.io/g/nvda) te stranica koja sadrži puno [grupa na lokalnim jezicima](https://github.com/nvaccess/nvda-community/wiki/Connect).
NV Access, tvorci NVDA, aktivni su na [Twitteru](https://twitter.com/nvaccess) i [Facebooku](https://www.facebook.com/NVAccess).
Članovi organizacije NV Access također vode [Blog s novostima](https://www.nvaccess.org/category/in-process/).

Također postoji program [Certifikacije NVDA eksperata](https://certification.nvaccess.org/).
To je On-line ispit koji možete položiti kako biste polazali svoje znanje i vještine u korištenju NVDA.
[NVDA certificirani eksperti](https://certification.nvaccess.org/) mogu objaviti svoje kontakt podatke i detalje o svom poslovanju.

### Dobivanje pomoći {#GettingHelp}

Kako biste dobili pomoć za NVDA, pritisnite `NVDA+n` kako biste otvorili NVDA izbornik, a potom `p` za pomoć.
Iz ovog podizbornika možete dobiti pristup korisničkom vodiču, brzom ispisu tipkovničkih prečaca, povjesti svih promjena i novih značajki, te još puno toga.
Ove tri opcije otvaraju se u podrazumjevanom web pregledniku.
Postoji također puno opširnihi materijal za obuku dostupan u [NV Access trgovini](https://www.nvaccess.org/shop).

Preporučujemo vam započeti sa "Osnovnom obukom za korištenje NVDA".
Ovaj modul pokriva teme od početka korištenja pa sve do surfanja internetom i korištenja objektne navigacije.
Ovaj je modul dostupan u obliku:

* [elektronskog teksta](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), koji uključuje word DOCX, web stranicu HTML, e-knjigu ePub i Kindle KFX formate.
* [Audio koji čita čovjek](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Kopija napisana Unificiranim engleskim brajevim pismom u tvrdom uvezu](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) s isporukom u cijelom svijetu.

Ostali moduli, i  NVDA komplet za produktivnost po sniženoj cijeni https://www.nvaccess.org/product/nvda-productivity-bundle/], su dostupni u [NV Access trgovini](https://www.nvaccess.org/shop/).

NV Access također prodaje [Telefonsku podršku](https://www.nvaccess.org/product/nvda-telephone-support/), u blokovima, ili kao dio [NVDA kompleta za produktivnost](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Telefonska podrška uključuje telefonske brojeve u Australiji i Sad-u.

[Korisničke mailing liste](https://github.com/nvaccess/nvda-community/wiki/Connect) su odličan izvor dobivanja pomoći, kao i [certificirani NVDA eksperti](https://certification.nvaccess.org/).

Možete poslati izvještaj o pogrešci ili sugestiju nove značajke koristeći [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
[Smjernice za doprinos](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) sadrže vrijedne informacije za doprinositelje zajednici.

## Više opcija za postavljanje {#MoreSetupOptions}
### Opcije instalacije {#InstallingNVDA}

Ako instalirate NVDA izravno pokrečući preuzeti instalacijski paket, pritisnite gumb Instaliraj NVDA.
Ako ste već zatvorili ovaj dijaloški okvir ili želite instalirati iz prijenosne kopije, odaberite stavku izbornika Instaliraj NVDA koju možete pronaći u podizborniku Alati u NVDA izborniku.

Prikazani dijaloški okvir instalacije će potvrditi, želite li instalirati NVDA i obavijestit će vas, nadograđuje li se postojeća instalacija.
Kad pritisnete gumb Nastavi, započet će NVDA instalacija.
U ovom dijaloškom okviru postoji i nekoliko opcija koje su objašnjene niže dolje.
Nakon završetka instalacije, pojavit će se poruka da je instalacija uspjela.
Kad pritisnete U redu, pokrenut ćete novoinstaliranu kopiju NVDA čitača.

#### Upozorenje o nekompatibilnim dodacima {#InstallWithIncompatibleAddons}

Ako već imate instalirane dodatke, može se pojaviti upozorenje koje označava potrebu za deinstaliranjem nekompatibilnih dodataka.
Prije nego što ćete moći pritisnuti gumb Nastavi, morat ćete označiti potvrdni okvir kojim potvrđujete suglasnost o tome, da se deaktiviraju svi nekompatibilni dodaci.
Također postoji gumb, koji omogućuje pregled nekompatibilnih dodataka.
Pogledajte poglavlje [Upravljanje nekompatibilnim dodacima](#incompatibleAddonsManager) za daljnje informacije o ovom gumbu.
Nakon instalacije, možete ponovo omogućiti nekompatibilne dodatke na vlastitu odgovornost iz [add-on storea](#AddonsManager).

#### Koristi NVDA prilikom prijave {#StartAtWindowsLogon}

Ova opcija omogućuje automatsko pokretanje NVDA čitača na Windows ekranu za prijavu, prije upisivanja lozinke.
Ovo također uključuje kontrolu korisničkog računa i [ostale sigurne zaslone](#SecureScreens).
Ova je opcija standardno aktivirana za nove instalacije.

#### Izradi prečac na radnoj površini (kontrol+alt+F5) {#CreateDesktopShortcut}

Ova opcija omogućuje izradu prečaca na radnoj površini za pokretanje NVDA čitača. 
Ako je izrađen, prečacu na radnoj površini bit će dodijeljen tipkovnički prečac kontrol+alt+F5, pomoću kojeg je moguće pokrenuti NVDA čitača u bilo kojem trenutku.

#### Kopiraj prijenosnu konfiguraciju na ovaj korisnički račun {#CopyPortableConfigurationToCurrentUserAccount}

Ova opcija omogućuje kopiranje trenutačne konfiguracije iz prijenosne kopije na trenutačno prijavljeni korisnički račun za trenutačno instaliranu kopiju NVDA čitača. 
Ova opcija neće kopirati konfiguraciju za bilo kojeg drugog korisnika ovog sustava niti u konfiguraciju sustava za korištenje prilikom prijave u sustav Windows i [ostale zaslone za prijavu](#SecureScreens).
Ova je opcija dostupna samo kad se NVDA instalira iz prijenosne kopije, ali ne i u trenutku kad se NVDA instalira iz instalacijske datoteke koja je preuzeta s interneta.

### Izrada prijenosne kopije {#CreatingAPortableCopy}

Ako izrađujete prijenosnu kopiju iz preuzetog instalacijskog paketa za NVDA, jednostavno pritisnite gumb Stvori prijenosnu kopiju.
Ako ste već zatvorili dijaloški okvir ili ako ste pokrenuli instaliranu kopiju NVDA čitača, odaberite stavku Stvori prijenosnu kopiju, u NVDA izborniku.

Dijaloški okvir koji se prikazuje omogućuje biranje mjesta, gdje će se izraditi prijenosna kopija.
To može biti mapa na vašem tvrdom disku ili lokacija na vašem USB sticku ili na drugom prijenosnom uređaju.
Također, postoji opcija koja omogućuje kopiranje konfiguracije trenutačno prijavljenog korisnika za korištenje u prijenosnoj kopiji.
Ova je opcija dostupna samo kad se prijenosna kopija izrađuje iz instalirane kopije, ali ne i kad se izrađuje iz instalacijske datoteke preuzete s interneta.
Kad pritisnete Nastavi, započet ćete proces izrade prijenosne kopije.
Kad proces izrade završi, prikazat će se poruka da je izrada prijenosne kopije uspjela.
Pritisnite U redu da biste zatvorili ovaj dijaloški okvir.

### Ograničenje privremene i prijenosne kopije {#PortableAndTemporaryCopyRestrictions}

Ako želite nVDA nositi sa sobom na USB sticku ili drugom zapisivom mediju, tada trebate odabrati stvaranje prijenosne kopije.
Instalirana kopija može stvoriti prijenosnu kopiju u bilo kojem trenutku. 
Prijenosna kopija također posjeduje mogućnost instalacije na bilo koje računalo u neko dogledno vrijeme.
Međutim, ako želite kopirati NVDA na medij koji je samo za čitanje kao što je to CD, trebate samo kopirati preuzeti paket.
Izravno pokretanje prijenosne verzije sa nosača koji je samo za čitanje nije podržano u ovom trenutku.

[NVDA instalacija](#StepsForRunningTheDownloadLauncher) se može koristiti kao privremena kopija programa NVDA.
Privremene kopije sprečavaju čuvanje NVDA podešavanja.
Ovo uključuje nemogućnost korišćenja [prodavnice dodataka](#AddonsManager).

Prenosne i privremene kopije programa NVDA imaju sledeća ograničenja:

* Nemogućnost automatskog pokretanja u toku ili nakon prijave.
* Nemogućnost interakcije aplikacija sa administrativnim privilegijama, osim ako NVDA nije pokrenut s istima (nije preporučeno).
* Nemogućnost čitanja zaslona kontrole korisničkih računa (UAC) prilikom pokušaja pokretanja aplikacije s administratorskim pravima.
* Nemogućnost korištenja dodirnika.
* Nemogućnost podrške značajki poput modusa pregleda, čitanje upisanih znakova u Windows Store aplikacijama.
* Utišavanje zvuka nije podržano.

## Korištenje NVDA {#GettingStartedWithNVDA}
### Pokretanje NVDA čitača {#LaunchingNVDA}

Ako ste instalirali NVDA pomoću instalacijskog programa, tada se NVDA jednostavno pokreće pritiskom kontrol+alt+f5 ili odabirom NVDA iz NVDA izbornika u podizborniku Programi u izborniku Start.
NVDA se može pokrenuti i u dijaloškom okviru Pokreni. Upišite NVDA i pritisnite tipku enter.
Ako je NVDA već pokrenut, pokrenut će se ponovo.
Možete koristiti i neke [opcije naredbenog retka](#CommandLineOptions) za izlazak iz NVDA čitača (-q), za deaktiviranje dodataka (--disable-addons) itd.

Podrazumjevano, NVDA sprema svoju konfiguraciju u roaming application data mapi trenutnog korisnika (npr: "`C:\Users\<user>\AppData\Roaming`").
To je moguće promijeniti, tako da NVDA učitava svoje postavke iz lokalne mape aplikacijskih podataka.
Za više detalja, pročitajte poglavlje o [cjelosustavnim parametrima](#SystemWideParameters).

Da biste pokrenuli prijenosnu kopiju, uđite u mapu u kojoj ste raspakirali NVDA i pritisnite enter ili dva puta kliknite na datoteku nvda.exe.
Ako je NVDA bio ponovo pokrenut, isključit će se prije pokretanja prijenosne kopije.

Tijekom pokretanja NVDA čitača, prvo ćete čuti seriju uzlaznih tonova (koji vam govore da se NVDA učitava).
Ovisno o brzini vašeg računala ili o tome, pokrećete li NVDA s USB sticka ili s drugog sporog medija, pokretanje može potrajati.
Ako učitavanje traje jako dugo, NVDA bi trebao izgovoriti "NVDA se učitava. Pričekaj …"

Ako ne čujete ništa od navedenog ili ako čujete Windows zvuk za grešku ili silaznu seriju tonova, to znači da postoji greška u NVDA čitaču i možda ćete trebati prijaviti grešku timu razvijatelja.
Za više informacija kako to učiniti, pogledajte NVDA web stranicu

#### Dijaloški okvir dobrodošlice {#WelcomeDialog}

Kad prvi put pokrenete NVDA, otvorit će se dijaloški okvir dobrodošlice koji daje osnovne informacije o NVDA modifikacijskoj tipci i NVDA izborniku.
(Pogledajte daljnja poglavlja o ovim temama.)
Dijaloški okvir sadrži jedan odabirni okvir i tri potvrdna okvira.
Odabirni okvir omogućuje biranje rasporeda tipkovnice.
Prvi potvrdni okvir određuje, hoće li se koristiti capslock (tipka za velika slova) kao modifikacijska tipka.
Drugi potvrdni okvir određuje, hoće li se NVDA pokretati prilikom prijave u Windows sustav. Dostupan je samo za instalirane kopije NVDA čitača.
Treći potvrdni okvir određuje, hoće li se ovaj dijaloški okvir prikazivati tijekom svakog pokretanja NVDA čitača.

#### Dijaloški okvir o prikupljanju podataka {#UsageStatsDialog}

Počevši s verzijom NVDA 2018.3, korisnika se pita želi li pristati davati statističke podatke NV Accessu koji pomažu razvijati NVDA. 
Prilikom prvog pokretanja NVDA, otvorit će se dijaloški okvir u kojem ćete biti pitani, želite li slati korisničke podatke NV Accessu kakda koristite NVDA.
O tome koji se podaci prikupljaju, možete pročitati u poglavlju o općenitim postavkama, [Dozvoli NV accessu prikupljanje statističkih podataka](#GeneralSettingsGatherUsageStats).
Upozorenje: pritiskom gumba "Da" ili "Ne" ova će se postavka spremiti, a dijaloški okvir se više nikada neće pojavljivati osim u slučaju kad ponovo instalirate NVDA.
Međutim, možete uključiti ili isključiti proces prikupljanja podataka ručno u ploči općih postavki. Kako biste tu postavku promijenili ručno, možete označiti ili odznačiti potvrdni okvir [Dozvoli NVDA projektu prikupljanje statistike o korištenju](#GeneralSettingsGatherUsageStats).

### O NVDA tipkovničkim prečacima {#AboutNVDAKeyboardCommands}
#### NVDA modifikacijska tipka {#TheNVDAModifierKey}

Većina tipkovničkih prečaca koji su specifični za NVDA, koriste se pritiskanjem određene tipke koja se zove NVDA modifikacijska tipka, u kombinaciji s jednom ili više drugih tipki.
S tim u vezi postoje iznimke, kao što su prečaci za pregled teksta u rasporedu tipkovnice za stolna računala koje koriste numerički dio tipkovnice, kao i neke druge.

NVDA se može konfigurirati tako da se kao NVDA modifikacijska tipka koriste tipke numerički Insert, Prošireni Insert i-ili capslock.
Tipke numerički insert i prošireni insert su standardno postavljene kao NVDA modifikacijske tipke.

Ako želite da se NVDA modifikacijske tipke ponašaju na način kao da NVDA nije pokrenut (npr. želite uključiti velika slova kad ste velika slova postavili kao modifikacijsku tipku), pritisnite tipku dva puta brzo.

#### Rasporedi tipkovnice {#KeyboardLayouts}

NVDA trenutačno dolazi s dva skupa tipkovničkih prečaca (poznatih kao rasporedi tipkovnice): raspored tipkovnice za stolna računala i raspored tipkovnice za prijenosna računala.
NVDA standardno dolazi s rasporedom tipkovnice za stolna računala, međutim možete se prebaciti na raspored za prijenosna računala u kategoriji "Tipkovnica" u dijaloškom okviru [NVDA Postavke](#NVDASettings), u podizborniku Postavke, u NVDA izborniku.

Raspored tipkovnice za stolna računala maksimalno iskorištava numeričku tipkovnicu (s isključenim numeričkim blokom).
Iako neka prijenosna računala nemaju numeričku tipkovnicu, neka prijenosna računala mogu emulirati numeričku tipkovnicu pritiskom tipke FN i pritiščući slova i brojke koji se nalaze s desne strane na tipkovnici (7, 8, 9, u, i, o, j, k, l, itd.).
Ako vaše prijenosno računalo to ne može izvršiti ili ako ne postoji mogućnost za isključivanje numeričkog bloka, možda se umjesto toga morate prebaciti na raspored tipkovnice za prijenosna računala.

### NVDA dodirne geste {#NVDATouchGestures}

Ako pokrećete NVDA na uređaju koji ima ekran osjetljiv na dodir, možete upravljati NVDA čitačem izravno pomoću dodirnih naredbi, osim ako podrška ekrana osjetljivih na dodir nije isključena.
Kad je NVDA pokrenut, svaki unos dodirom bit će proslijeđen izravno NVDA čitaču. 
Stoga, radnje koje se mogu uraditi normalno bez NVDA čitača, neće raditi.
<!-- KC:beginInclude -->
Kako biste uključili ili isključili podršku ekrana osjetljivih na dodir, pritisnite NVDA+control+alt+t.
<!-- KC:endInclude -->
[Podršku ekrana osjetljivih na dodir](#TouchSupportEnable) možete uključiti ili isključiti u kategoriji interakciaj s ekranima osjetljivim na dodir u NVDA postavkama.

#### Istraživanje ekrana {#ExploringTheScreen}

Najosnovnija stvar koju možete učiniti s ekranom osjetljivim na dodir je izvještavanje o kontroli ili tekstu na bilo kojem dijelu ekrana.
Da biste to učinili, postavite prst na bilo koje mjesto na ekranu.
Također možete držati prst na ekranu i pomicati ga okolo, da biste pročitali ostale kontrole i tekst po kojem se pomičete vašim prstom.

#### Dodirne geste {#TouchGestures}

Kad se NVDA naredbe opisuju u ovom priručniku, one će možda navoditi dodirnu gestu koja služi za aktivaciju naredbe pomoću ekrana osjetljivog na dodir.
Slijedi nekoliko uputa kako izvesti određene dodirne geste.

##### Dodiri {#toc45}

Brzo dodirnite ekran s jednim ili više prstiju.

Dodir jednim prstom je poznato kao dodir.
Dodir s dva prsta je poznato kao dvoprstni dodir itd.

Ako se isti dodir ponovi jednom ili više puta brzo, NVDA će to shvatiti kao višedodirnu gestu.
Dvostruki dodir rezultira dvostrukim dodirom nekog elementa na ekranu.
Trostruki dodir rezultira trostrukim dodirom itd.
Naravno, ove višedodirne geste prepoznaju koliko se prstiju koristi. Stoga je moguće imati geste kao što su na primjer trostruki dodir s dva prsta, dodir sa četiri prsta itd. 

##### Klizanje {#toc46}

Brzo klizanje prstom po ekranu.

Postoje 4 moguće klizajuće geste ovisno o smjeru: klizanje u lijevo, klizanje u desno, klizanje prema gore i klizanje prema dolje.

Kao i kod dodira, moguće je koristiti više od jednog prsta za izvođenje geste.
Stoga su moguće geste, kao što su klizanje s 2 prsta gore i klizanje s 4 prsta u lijevo.

#### Modusi dodira {#TouchModes}

Budući da postoji puno više NVDA prečaca nego dodirnih gesti, NVDA ima nekoliko modusa dodira između kojih se možete prebacivati i koji omogućuju određene podskupove prečaca.
Modusi dodira su tekstualni modus i objektni modus. 
Neke od navedenih naredbi u ovom dokumentu sadrže podatak o modusu dodira u zagradama poslije dodirne geste.
Na primjer, klizni gore (tekstualni modus), znači da će prečac biti izvršen ako kliznete gore, ali samo kad ste u tekstualnom modusu.
Ako prečac nema podatak o modusu, taj će prečac raditi u bilo kojem modusu.

<!-- KC:beginInclude -->
Za prebacivanje između modusa dodira, izvedite dodir s tri prsta.
<!-- KC:endInclude -->

#### Dodirna tipkovnica {#TouchKeyboard}

Dodirna tipkovnica se koristi za unos teksta i naredbi na ekranu osjetljivom na dodir.
Kad ste fokusirani na polju za uređivanje, možete prikazati dodirnu tipkovnicu tako da dva puta dodirnete ikonu dodirne tipkovnice na kraju ekrana.
Na tabletima, poput Microsoft Surface Pro, dodirna tipkovnica je uvijek dostupna, kad je hardverska tipkovnica otkvačena.
Kako biste sakrili dodirnu tipkovnicu, dva puta dodirnite ikonu za dodirnu tipkovnicu ili izađite iz polja za uređivanje teksta.

Kad je dodirna tipkovnica aktivna, kako biste locirali tipke na dodirnoj tipkovnici, premjestite prst tamo gdje se nalazi dodirna tipkovnica (skoro uvijek na kraju ekrana), a nakon toga kružite po tipkovnici s jednim prstom.
Kad pronađete tipku koju želite pritisnuti, pritisnite je dvaput ili dignite prst, ovisno o opciji, koju ste odabrali u kategoriji [Interakcija dodirom](#TouchInteraction) u NVDA postavkama.

### Pomoć pri unosu {#InputHelpMode}

Mnogi NVDA tipkovnički prečaci su navedeni u ovom priručniku niže dolje, ali najlakši način istraživanja svih različitih prečaca je uključivanje pomoći pri unosu.

Da biste uključili pomoć pri unosu, pritisnite NVDA+1.
Da biste je isključili, ponovo pritisnite NVDA+1.
Dok se nalazite u modusu pomoći pri unosu, izvođenjem bilo koje ulazne geste (kao što je pritiskanje tipke ili izvođenje dodirne geste) će se izvijestiti o radnji i opisati što radi (ako išta radi).
Same naredbe se neće izvršavati dok se nalazite u modusu pomoći pri unosu.

### NVDA izbornik {#TheNVDAMenu}

NVDA izbornik omogućuje mijenjanje NVDA postavki, pristup pomoći, spremanje ili vraćanje vaše konfiguracije, izmjenu govornih rječnika, pristup dodatnim alatima i izlaz iz programa NVDA.

Da biste ušli u NVDA izbornik bilo gdje u Windowsu dok je NVDA pokrenut, možete izvršiti bilo koju od sljedećih radnji:

* pritisnuti `NVDA+n` na tipkovnici.
* Dvostruki dodir sa dva prsta na ekranu osjetljivom na dodir.
* pristupanjem području obavijesti tako da pritisnete prečac `Windows+b`, i tako da se krećete `strelicom Dolje` do NVDA ikone, a zatim pritiskanje tastera `enter`.
* Alternativno, pristupite području obavijesti prečacem `Windows+b`, krećite se `strelicomDolje` do NVDA ikone, i otvorite kontekstni meni pritiskanjem `aplikacijske` tipke koji se nalazi pored desne control tipke na većem broju tipkovnica.
Na tipkovnici bez `aplikacijske` tipke, umjesto toga pritisnite `šift+f10`.
* Desni klik na NVDA ikoni na Windows području obavijesti

Kada se izbornik otvori, možete koristiti strelice da se krećete po izborniku, i tipku `enter` za aktivaciju stavke.

### Osnovni NVDA tipkovnički prečaci {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Dodir |Opis|
|---|---|---|---|---|
|Pokreće ili ponovno pokreće NVDA |Control+alt+f5 |Control+alt+f5 |nema |Pokreće ili ponovno pokreće NVDA s radne površine, ako je ovaj Windowsov prečac omogućen tijekom NVDA instalacijskog procesa. Ovo je Windowsov prečac stoga se ne može mijenjati u dijaloškom okviru ulaznih gesti.|
|Zaustavi govor |kontrol |kontrol |dodir s dva prsta |Trenutno zaustavlja govor|
|Pauziraj govor |šift |šift |nema |Trenutno pauzira govor. Kad tipku ponovo pritisnete, NVDA će nastaviti govoriti gdje je stao (ako trenutačna govorna jedinica podržava pauziranje)|
|NVDA Izbornik |NVDA+n |NVDA+n |dvostruki dodir s dva prsta |Prikazuje NVDA izbornik koji omogućuje pristup postavkama, alatima, pomoći itd.|
|Mijenjanje modusa unosa |NVDA+1 |NVDA+1 |nema |Pritiskom bilo koje tipke, izvijestit će se o tome što ta tipka radi s opisom bilo kojeg NVDA prečaca koji joj je pridružen|
|Izlaz iz NVDA |NVDA+q |NVDA+q |nema |Izlazi iz NVDA|
|Proslijedi sljedeću tipku |NVDA+f2 |NVDA+f2 |nema |Naređuje NVDA čitaču da proslijedi sljedeći pritisak tipke ravno aktivnoj aplikaciji, čak iako je ta kombinacija tretirana kao NVDA prečac|
|Uključi ili isključi modus mirovanja |NVDA+šift+s |NVDA+šift+z |nema |Modus mirovanja deaktivira sve NVDA prečace i govorni ili brajični izlaz za trenutačnu aplikaciju. Vrlo korisno kad aplikacije pružaju vlastiti govor ili funkcije čitanja ekrana. Pritisnite prečac još jednom da biste isključili modus mirovanja.|

<!-- KC:endInclude -->

### Izvještavanje o informacijama sustava {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Izgovori datum i vrijeme |NVDA+f12 |Kad se pritisne jednom izgovara trenutačno vrijeme, kad se pritisne dvaput izgovara datum|
|Izgovor stanja baterije |NVDA+šift+b |Izvještava o trenutačnom stanju baterije, kao i o tome je li priključen punjač i stanje baterije u postotcima.|
|Pročitaj tekst iz međuspremnika |NVDA+c |Čita tekst iz međuspremnika ako postoji.|

<!-- KC:endInclude -->

### Modusi govora {#SpeechModes}

Načini govora reguliraju kako će se sadržaj ekrana, obavjesti  i reakcije na prečacei druge izlazne informacije izgovarati prilikom korištenja NVDA.
Podrazumjevani modus je "govor", prilikom se kojega informacije izgovaraju onako kaiko je to očekivano prilikom korištenja čitača ekrana.
Međutim, u nekim okolnostima, ili prilikom pokretanja određenih programa, uvidjet ćete da su niki od drugih modusa korisni.

Četiri su dostupna modusa:

* Govor (podrazumijevani): NVDA će govoriti uobičajeno pri reakciji na izmjene na ekranu, obavijesti, i radnje poput pomicanja fokusa, ili izdavanje naredbi.
* Na zahtjev: NVDA će govoriti samo onda kada koristite naredbe koje služe za čitanje određene informacije (npr: čitanje informacija o prozoru); ali neće govoriti kao odgovor na radnje pomicanja fokusa.
* Isključeno: NVDA neće čitati ništa, međutim, za razliku od načina mirovanja, NVDA će tiho reagirati na prečace.
* Zvučni signali: NVDA će zamijeniti uobičajeni govor zvučnim signalima.

Način zvučnih signala je koristan kada se pojavljuje velika količina teksta  u prozoru naredbenog redka, ali vas nije briga što taj tekst znači, ali vam je samo važno da se tekst pomiće ili u ostalim slučajevima kada vam se važno da samo postoji neki izlaz.

Način govora na zahtjev može biti koristan kada ne trebate stalnu povratnu informaciju o tome što se događa na zaslonu ili na računalu, ali trebate provjeriti neke stvari koristeći prečace za pregled, itd.
Jedan od primjera uključuje snimanje zvuka, prilikom korištenja lupe, prilikom poziva ili susreta, ili kao alternativa načinu govora zvučni signali.

Prečac omogućuje prebacivanje između raznih modusa govora:
<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Prebacuj se između modusa govora |`NVDA+s` |Cycles between speech modes.|

<!-- KC:endInclude -->

Ako se trebate prebacivati samo između određenog skupa modusa govora, pogledajte [Dostupni načini u prečacu prebacivanja između načina govora](#SpeechModesDisabling) kao način isključivanja neželjenih načina govora.

## Kretanje pomoću NVDA čitača {#NavigatingWithNVDA}

NVDA omogućuje istraživanje i kretanje u sustavu na nekoliko načina, uključujući normalnu interakciju i pregled.

### Objekti {#Objects}

Svaka aplikacija, kao i sam operacijski sustav, sastoji se od više objekata.
Pod objektom se podrazumijeva jedna stavka kao što je komad teksta, gumb, potvrdni okvir, klizač, popis ili polje za uređivanje teksta.

### Kretanje pomoću fokusa sustava {#SystemFocus}

Fokus sustava (ili jednostavno fokus) je [objekt](#Objects) koji prima upisane znakove s tipkovnice.
Na primjer, ako upisujete tekst u polje za uređivanje teksta, polje za uređivanje teksta je u fokusu.

Najuobičajeni način kretanja po Windowsu pomoću NVDA čitača je jednostavno premještanje fokusa sustava koristeći osnovne Windowsove tipkovničke prečace. Tipke tabulator i šift+tabulator služe za premještanje prema naprijed i natrag između kontrola. Tipka alt služi za premještanje na traku izbornika. Tipke strelica gore, dolje, lijevo i desno služe za kretanje po izbornicima. Tipke alt+tabulator služe za premještanje između pokrenutih programa.
Tijekom premještanja NVDA javlja informacije o fokusiranom objektu, kao što su ime objekta, vrsta, vrijednost, stanje, opis, tipkovnički prečac i informacije o položaju.
Kad je [Vizualno praćenje](#VisionFocusHighlight) uključeno, prikazuje se i pozicija fokusa na ekranu.

Postoji nekoliko tipkovničkih prečaca koji su korisni za kretanje po objektima:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Opis|
|---|---|---|---|
|Izvijesti o trenutačnom fokusu |NVDA+tabulator |NVDA+tabulator |Izvještava o objektu koji je trenutačno u fokusu. Kad pritisnete dvaput, slovkat će izgovoreno|
|Izvijesti o naslovu |NVDA+t |NVDA+t |Izvještava o naslovu trenutačnog prozora. Kad pritisnete dvaput, NVDA će slovkati izgovoreno. Kad pritisnete triput naslov se kopira u međuspremnik.|
|Pročitaj trenutačni prozor |NVDA+b |NVDA+b |Čita sve kontrole u trenutačno aktivnom prozoru (korisno za dijaloške okvire)|
|Izvijesti o traci stanja |NVDA+end |NVDA+šift+end |Izvještava o traci stanja, ako je NVDA pronađe. Kad se pritisne dvaput, informacije na traci stanja se slovkaju, a kad se pritisne triput, kopiraju se u međuspremnik.|
|pročitaj tipkovnički prečac |`shift+numerički2` |`NVDA+control+shift+.` |Izgovara tipkovnički prečac aktivnog NVDA objekta|

<!-- KC:endInclude -->

### Kretanje pomoću kursora sustava {#SystemCaret}

Kad je [objekt](#Objects) koji omogućuje kretanje i-ili uređivanje teksta [u fokusu](#SystemFocus), možete se kretati po tekstu koristeći kursor sustava, također poznat kao kursor uređivanja.

Kad je objekt koji ima kursor sustava u fokusu, možete koristiti strelice, pejdž ap, pejdž daun, houm, end, itd, da biste se kretali po tekstu.
Možete promjeniti tekst, ako kontrola podržava uređivanje.
NVDA će vas obavještavati o kretanju po znakovima, riječima i redcima te o označavanju i odznačavanju teksta.

NVDA omogućuje korištenje sljedećih prečaca u svezi s kursorom sustava:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Opis|
|---|---|---|---|
|Izgovori sve |NVDA+strelicaDolje |NVDA+a |Čita od trenutačne pozicije kursora sustava, pomičući ga dok se kreće|
|Čitaj trenutačni redak |NVDA+strelicaGore |NVDA+l |Čita trenutačni redak gdje je kursor sustava pozicioniran. Kad se pritisne dvaput, NVDA slovka taj redak. Kad se pritisne tri puta, NVDA slovka redak fonetski.|
|Čitaj trenutačno označeni tekst |NVDA+šift+strelicaGore |NVDA+šift+s |Čita bilo koji trenutačno označen tekst|
|Izvijesti o oblikovanju teksta |NVDA+f |NVDA+f |Izgovara svojstva oblikovanja teksta na mjestu gdje se kursor sustava nalazi. Kada se pritisne dva put pokazuje informaciju u modusu čitanja|
|Čitaj odredište poveznice |`NVDA+k` |`NVDA+k` |Kada se pritisne jedamput, izgovara poveznicu pod kursorom ili u fokusu. Kada se pritisne dvaput, pokazuje poveznicu u prozoru za pažljiviji pregled|
|Izvjesti o poziciji kursora sustava |NVDA+numeričkiDelete |NVDA+delete |Čita informacije o lokaciji teksta ili objekta na poziciji kursora sustava. Na primjer, ovo može uuključivati postotak diljem dokumenta, udaljenost od ruba stranice ili točnu lokaciju na zaslonu. Kada se pritisne dvaput postoji mogućnost dobivanja više detalja.|
|Sljedeća rečenica |alt+Strelicadolje |alt+StrelicaDolje |Premješta kursor na sljedeću rečenicu, a potom je izgovara. (Podržano u Microsoft Wordu i Outlooku)|
|Prethodna rečenica |alt+StrelicaGore |alt+StrelicaGore |Premješta kursor na prethodnu rečenicu, a potom je izgovara. (Podržano u Microsoft Wordu i Outlooku)|

Unutar tablice su dostupni i sljedeći prečaci:

| Naziv |Tipka |Opis|
|---|---|---|
|Premjesti se na prethodni stupac |kontrol+alt+strelicaLijevo |Premješta kursor sustava na prethodni stupac (pritom ostajući u istom retku)|
|Premjesti se na sljedeći stupac |kontrol+alt+strelicaDesno |Premješta kursor sustava na sljedeći stupac (pritom ostajući u istom retku)|
|Premjesti se na prethodni redak |kontrol+alt+strelicaGore |Premješta kursor sustava na prethodni redak (pritom ostajući u istom stupcu)|
|Premjesti se na sljedeći stupac |kontrol+alt+strelicaDolje |Premješta kursor sustava na sljedeći redak (pritom ostajući u istom stupcu)|
|Premjesti se na prvi stupac |ctrl+alt+home |Pomiće kursor sustava na prvi stupac (ostajući u istom redku)|
|Premjesti se na zadnji stupac |ctrl+alt+end |pomiće kursor na zadnji stupac (ostajući u istom redku)|
|Premjesti se na prvi redak |ctrl+alt+pageUp |Pomiće kursor sustava u prvi redak (ostajući u istom stupcu)|
|Premjesti se na zadnji redak |ctrl+alt+pageDown |pomiće kursor sustava na zadnji redak (ostajući u istom stupcu)|
|Čitaj sve u stupcu |`NVDA+control+alt+strelica dolje` |Čita stupac vertikalno od trenutne ćelije prema dolje do zadnje ćelije u stupcu.|
|Čitaj sve u redku |`NVDA+control+alt+strelica desno` |Čita redak horizontalno od trenutne ćelije prema desno do zadnje ćelije u redku.|
|Čitaj cijeli stupac |`NVDA+control+alt+strelica gore` |Čita trenutni redak vertikalno od gore prema dolje bez pomicanja kursora sustava.|
|Čitaj cijeli redak |`NVDA+control+alt+strelica lijevo` |Čita trenutni redak horizontalno s lijeva na desno bez pomicanja kursora sustava.|

<!-- KC:endInclude -->

### Kretanje po objektima {#ObjectNavigation}

Većinu vremena radit ćete s aplikacijama koristeći prečace koji pomiču [fokus](#SystemFocus) i [kursor](#SystemCaret).
Međutim, možda ćete željeti istražiti trenutačnu aplikaciju ili operacijski sustav bez pomicanja fokusa ili kursora.
Također, možda želite raditi s [objektima](#Objects) kojima se ne može pristupiti putem tipkovnice na uobičajeni način.
U tim slučajevima, možete koristiti kretanje po objektima.

Kretanje po objektima omogućuje pomicanje između objekata i pristup informacijama pojedinih [objekata](#Objects).
Kad se pomaknete na objekt, NVDA će o njemu izvještavati slično kao što izvještava o fokusu sustava.
Da biste vidjeli tekst kako on doista izgleda na ekranu, možete umjesto kretanja po objektima koristiti [Pregled ekrana](#ScreenReview).

Umjesto pojedinačnog pomicanja po svakom objektu naprijed-natrag, oni su organizirani hijerarhijski.
To znači da neki objekti sadrže druge objekte i da u njih morate ući, kako biste pristupili objektima koje oni sadrže.
Na primjer, popis sadrži stavke popisa. Morate ući u popis, kako biste pristupili njegovom sadržaju.
Ako ste se premjestili na stavku popisa, premještanjem naprijed-natrag, prebacujete se na ostale stavke istog popisa.
Premještanjem na objekt popisa koji sadrži stavku, vratit će vas na popis.
Tada se možete premjestiti izvan popisa, ako želite pristupiti drugim objektima.
Slično tome, alatna traka sadrži kontrole, dakle, morate ući u alatnu traku, da biste pristupili kontrolama na alatnoj traci.

Ako ipak želite da se krećete između svakog pojedinačnog objekta na sistemu, možete koristiti komande da se pomerite na prethodni ili sledeći objekat u  ravnom prikazu.
Na primer, ako se krećete do sledećeg objekta u ovom ravnom prikazu a trenutni objekat u sebi sadrži druge objekte, NVDA će se automatski prebaciti na prvij unutrašnji objekat.
U suprotnom, ako trenutni objekat ne sadrži objekte, NVDA će se prebaciti na sledeći objekat u trenutnom nivou hierarhije.
Ako nema takvog sledećeg objekta, NVDA će pokušati da pronađe sledeći objekat u hierarhiji u zavisnosti od unutrašnjih objekata dok više nema objekata na koje se možete prebaciti.
Ista pravila se primenjuju i kada se krećete nazad u hierarhiji.

Objekt koji se trenutačno pregledava se zove navigacijski objekt.
Kad se pomaknete na određeni objekt, možete pregledati njegov sadržaj pomoću prečaca za [Pregledavanje teksta](#ReviewingText), dok ste u modusu [Pregled objekta](#ObjectReview).
Kad je [Vizualno praćenje](#VisionFocusHighlight) aktivirano, pozicija navigacijskog objekta se prikazuje na ekranu.
Navigacijski objekt se standardno pokreće zajedno s fokusom sustava, ali se to ponašanje može uključiti ili isključiti.

Upozorenje: brajica koja prati objekt navigatora može se podesiti preko [povezanosti brajice](#BrailleTether).

Da biste se kretali po objektima, koristite sljedeće prečace:

<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Dodir |Opis|
|---|---|---|---|---|
|Izvijesti o trenutačnom objektu |NVDA+num5 |NVDA+šift+o |nema |Izvještava o trenutačnom navigacijskom objektu. Kad se dvaput pritisne, slovka objekt. Kad se triput pritisne, kopira ime i vrijednost tog objekta u međuspremnik.|
|Premjesti se na sadržavajući objekt |NVDA+num8 |NVDA+šift+strelicaGore |klizni gore (objektni modus) |Premješta se na objekt koji sadrži trenutačni navigacijski objekt|
|Premesti se na prethodni objekat |NVDA+numeričko4 |NVDA+šift+strelica levo |nema |pomera se na objekat pre trenutnog navigacionog objekta|
|Premesti se na prethodni objekat u ravnom prikazu |NVDA+numeričko9 |NVDA+šift+[ |prevlačenje levo (režim objekata) |Premešta se na prethodni objekat u ravnom prikazu hierarhije navigacije objekata|
|Premesti se na sledeći objekat |NVDA+numeričko6 |NVDA+šift+strelica desno |nema |premešta se na objekat posle trenutnog navigacionog objekta|
|Premesti se na sledeći objekat u ravnom prikazu |NVDA+numeričko3 |NVDA+šift+] |prevlačenje desno (režim objekata) |Premešta se na sledeći objekat u ravnom prikazu hierarhije navigacije objekata|
| Premjesti se na sljedeći sadržavajući objekt |NVDA+num2 |NVDA+šift+strelicaDolje |klizni dolje (objektni modus) |Premješta se na prvi objekt sadržan u navigacijskom objektu|
|---|---|---|---|---|
|Premjesti se na objekt fokusa |NVDA+numMinus |NVDA+backspace |nema |Premješta se na objekt koji je trenutačno u fokusu sustava te premješta kursor pregleda na poziciju kursora sustava, ako se prikazuje|
|Aktiviraj trenutačni navigacijski objekt |NVDA+numEnter |NVDA+enter |dvostruki dodir |Aktivira trenutačni navigacijski objekt (slično pritiskanjem miša ili razmaknice kad postoji fokus sustava)|
|Premjesti fokus sustava ili kursor na trenutačnu poziciju |NVDA+šift+numMinus |NVDA+šift+backspace |nema |Kad se pritisne jedanput, premješta fokus sustava na trenutačni navigacijski objekt. Kad se pritisne dvaput, premješta kursor sustava na trenutačnu poziciju preglednog kursora|
|Čitaj poziciju preglednog kursora |NVDA+shift+numpadDelete |NVDA+shift+delete |nema |Čita informaciju o tekstu ili objektu pod preglednim kursorom. Na primjer, to može uključivati postotak u dokumentu, rubove stranica ili točnu poziciju na zaslonu. Ako se pritisne dvaput, možete dobiti više detalja.|
|Premjesti kursor na traku stanja |nema |nema |nema |izgovara traku stanja ako ju NVDA pronađe. Objekt navigatora će se također premjestiti na tu lokaciju.|

<!-- KC:endInclude -->

Napomena: za tipke na numeričkoj tipkovnici je potrebno isključiti numerički blok, kako bi ispravno radile.

### Pregledavanje teksta {#ReviewingText}

NVDA omogućuje čitanje sadržaja [ekrana](#ScreenReview) trenutačnog [dokumenta](#DocumentReview) ili trenutačnog [objekta](#ObjectReview) riječ po riječ, slovo po slovo ili redak po redak.
To je veoma korisno u slučajevima (ukljućujući Windows naredbene retke) gdje ne postoji [kursor sustava](#SystemCaret).
Na primjer, može se koristiti za pregled teksta neke dugačke informacije u dijaloškom okviru.

Kad pomičete pregledni kursor, kursor sustava se ne pomiče, dakle možete pregledati tekst bez gubljenja pozicije uređivanja.
Međutim, kad pomičete kursor sustava, pregledni kursor se također pomiče.
Ovo se može uključiti ili isključiti.

Upozorenje: brajica koja prati kursor pregleda može se konfigurirati putem [povezivanja brajice](#BrailleTether).

Sljedeći prečaci su dostupni za pregledavanje teksta:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Dodir |Opis|
|---|---|---|---|---|
|Premjesti se na početak retka u pregledu |šift+num7 |NVDA+kontrol+houm |nema |Pomiče pregledni kursor na najviši redak teksta|
|Premjesti se na prethodni redak u pregledu |num7 |NVDA+strelicaGore |klizni gore (tekstualni modus) |Pomiče pregledni kursor na prethodni redak teksta|
|Izvijesti o trenutačnom retku u pregledu |num8 |NVDA+šift+. |nema |Čita trenutačni redak teksta gdje je pozicioniran pregledni kursor. Kad se pritisne dvaput, NVDA slovka trenutačni redak. Kad se pritisne triput, cijeli se redak slovka fonetski.|
|Premjesti se na idući redak u pregledu |num9 |NVDA+strelicaDolje |klizni dolje (tekstualni modus) |Pomiče pregledni kursor na idući redak teksta|
|Premjesti redak na kraj preglednog kursora |šift+num9 |NVDA+kontrol+end |nema |Pomiče pregledni kursor na krajnji redak teksta|
|Premjesti se na prethodnu riječ u pregledu |num4 |NVDA+kontrol+strelicaLijevo |klizni lijevo s dva prsta (tekstualni modus) |Pomiće pregledni kursor na prethodnu riječ u tekstu|
|Izgovori trenutačnu riječ pod preglednim kursorom |num5 |NVDA+kontrol+. |nema |Čita trenutačnu riječ u tekstu gdje je pozicioniran pregledni kursor. Kad se pritisne dvaput, slovka cijelu riječ. a Kad se pritisne tri put, slovka riječ fonetski.|
|Premjesti se na iduću riječ u pregledu |num6 |NVDA+kontrol+strelicaDesno |klizanje s dva prsta (tekstualni modus) |Premjesti pregledni kursor na iduću riječ u tekstu|
|Premjesti se na početak retka u pregledu |šift+num1 |NVDA+houm |nema |Pomiče pregledni kursor na početak trenutačnog retka u tekstu|
|Premjesti se na prethodni znak u pregledu |num1 |NVDA+strelicaLijevo |klizni lijevo (tekstualni modus) |Pomiče kursor pregleda na prethodni znak na trenutačnom retku u tekstu|
|Izvijesti o trenutačnom znaku pod preglednim kursorom |num2 |NVDA+. |nema |Izvještava o trenutačnom znaku u retku teksta gdje je pozicioniran pregledni kursor. Kad se pritisne dvaput, izvještava o opisu ili primjer tog znaka. Kad se pritisne triput, izgovara brojčanu vrijednost znaka u decimalnom i heksadecimalnom obliku.|
|Premjesti se na sljedeći znak u pregledu |num3 |NVDA+strelicaDesno |klizni desno (tekstualni modus) |Premjesti kursor pregleda na idući znak na trenutačnom retku teksta|
|Premjesti se na kraj retka u pregledu |šift+num3 |NVDA+end |nema |Pomiče pregledni kursor na kraj u trenutačnom retku teksta|
|Čitaj prethodnu stranicu u pregledu |`NVDA+pageUp` |`NVDA+shift+pageUp` |nema |Premješta na prethodnu stranicu teksta, ako podržava program|
|Premjesti na sljedeću stranicu pregleda |`NVDA+pageDown` |`NVDA+shift+pageDown` |nema |Premješta pregledni kursor na sljedeću stranicu teksta, ako to podržava program|
|Izgovori sve pomoću pregleda |numPlus |NVDA+šift+a |klizni s tri prsta prema dolje (tekstualni modus) |Čita od trenutačne pozicije preglednog kursora, pomičući se s pomićanjem kursora|
|Odaberi i potom kopiraj od preglednog kursora |insert+f9 |insert+f9 |nema |Započinje proces biranja, a zatim kopiranja od trenutačne pozicije preglednog kursora. Sama radnja se ne izvodi sve dok ne kažete NVDA-u gdje se nalazi kraj teksta|
|Odaberi i potom kopiraj do preglednog kursora |NVDA+f10 |NVDA+f10 |nema |Prilikom prvog pritiska, tekst je označen od pozicije od prije poznate kao početni marker sve do i uključujući poziciju preglednog kursora. Ako kursor sustava može dohvatiti tekst, isti će biti premješten na označeni tekst. Poslje pritiska prečaca drugi put, tekst će biti kopiran u windowsow međuspremnik|
|Premjesti se na označeni početak kopiranja na pregled |NVDA+šift+f9 |NVDA+šift+f9 |nema |Pomiče pregledni kursor na poziciju koja je određena kao početak markera za kopiranje|
|Izvijesti o oblikovanju teksta |NVDA+šift+f |NVDA+šift+f |nema |Izvještava o oblikovanje teksta gdje se pregledni kursor nalazi. Kad se pritisne dvaput, informacija se prikazuje u modusu čitanja.|
|Izvijesti o trenutačnoj zamjeni simbola |nema |nema |nema |Izgovara simbol na kojem se nalazi pregledni kursor. Kad se pritisne dvaput, pokazuje simbol i tekst koji ga opisuje u modusu čitanja.|

<!-- KC:endInclude -->

Bilješka: tipke na numeričkoj tipkovnici zahtijevaju da je numerički blok isključen, kako bi ispravno radile.

Dobar način pamćenja prečaca za pregled teksta kad se koristi raspored tipkovnice za stolna računala je, da ih zamislite kao matricu od tri sa tri. Redoslijed odozgo prema dolje je: redak, riječ i znak. Redoslijed s lijeva na desno je: prethodni, trenutačni, sljedeći.
Raspored je opisan kako slijedi:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|prethodni redak |trenutačni redak |sljedeći redak|
|prethodna riječ |trenutačna riječ |sljedeća riječ|
|prethodni znak |trenutačni znak |sljedeći znak|

### Modusi pregleda {#ReviewModes}

NVDA [prečaci za pregledavanje teksta](#ReviewingText) mogu služiti za pregled sadržaja u trenutačnom navigacijskom objektu, trenutačnom dokumentu ili ekranu, ovisno o odabranom modusu pregleda.

Sljedeći prečaci se koriste za prebacivanje između modusa pregleda:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Dodir |Opis|
|---|---|---|---|---|
|Prebaci na sljedeći modus pregleda |NVDA+num7 |NVDA+pejdž ap |klizanje s dva prsta prema gore |prebacuje na sljedeći dostupni modus pregleda|
|Prebaci na prethodni modus pregleda |NVDA+num1 |NVDA+pejdž daun |klizanje s dva prsta prema dolje |prebacuje na prethodni dostupni modus pregleda|

<!-- KC:endInclude -->

#### Pregled objekta {#ObjectReview}

Kad se nalazite u modusu pregleda objekta, možete pregledati samo sadržaj trenutačnog [navigacijskog objekta](#ObjectNavigation).
Za objekte kao što su polja za uređivanje teksta ili ostale osnovne kontrole za uređivanje teksta, to će uglavnom biti sadržaj teksta.
Za ostale objekte to može biti ime i-ili vrijednost.

#### Pregled dokumenta {#DocumentReview}

Kad se [navigacijski objekt](#ObjectNavigation) nalazi u dokumentu koji koristi modus čitanja (npr. web stranici) ili drugom kompleksnom dokumentu (npr. dokumentu programa Lotus symphony), moguće je prebaciti se u modus pregleda dokumenta.
Modus pregleda dokumenta omogućuje pregled teksta cijelog dokumenta.

Kad se prebacujete iz modusa pregleda dokumenta u modus pregleda objekta, pregledni kursor se nalazi u dokumentu na poziciji navigacijskog objekta.
Kad se krećete po dokumentu s prečacima za pregled dokumenta, navigacijski objekt se automatski aktualizira s objektom koji se nađe na trenutačnoj poziciji preglednog kursora.

Imajte na umu da će se NVDA automatski prebaciti na pregled objekta s pregleda dokumenta kad se krećete po dokumentima u modusu čitanja.

#### Pregled ekrana {#ScreenReview}

Modus pregleda ekrana omogućuje prikaz dokumenta kako se on zaista prikazuje na ekranu.
To je slično pregledu ekrana ili funkcionalnosti kursora miša u mnogim drugim čitačima ekrana za Windows sustav.

Kad se prebacujete na modus pregleda ekrana, pregledni kursor se premješta na ekransku poziciju trenutačnog [navigacijskog objekta](#ObjectNavigation).
Kad se pomičete po ekranu s prečacima za pregled ekrana, navigacijski objekt se automatski aktualizira s objektom koji se nađe na ekranskoj poziciji preglednog kursora.

Imajte na umu da u većini novijih aplikacija, NVDA neće moći vidjeti većinu ili cijeli tekst prikazan na ekranu zbog upotrebe novijih tehnologija za iscrtavanja ekrana, koje trenutačno nije moguće podržati.

### Kretanje pomoću miša {#NavigatingWithTheMouse}

Kad pomičete miša, NVDA čita tekst koji se nalazi izravno ispod pokazivača miša, kad se pokazivač miša kreće preko njega.
NVDA će pročitati popratni odlomak teksta, gdje je to podržano, ali neke kontrole čitaju samo cijeli redak.

NVDA se može konfigurirati tako da obavještava o vrsti [objekta](#Objects) ispod miša tijekom kretanja po tekstu (npr. popis, gumb, itd.).
To može pomoći potpuno slijepim korisnicima, jer ponekad tekst nije dovoljan.

NVDA pruža korisnicima mogućnost obavještavanja o položaju miša sviranjem zvučnih signala za trenutačne koordinate miša u odnosu na dimenzije ekrana.
Što je pozicija miša na ekranu viša, to je viši i zvučni signal.
Ako se miš na ekranu nalazi više lijevo ili desno, zvuk će se čuti više lijevo ili desno (ako uzmemo u obzir da korisnik ima stereo zvučnike ili slušalice).

Ove značajke nisu standardno uključene u postavkama NVDA.
Ako želite koristiti te značajke, možete ih konfigurirati u [postavkama Miša](#MouseSettings), kategorija [NVDA Postavke](#NVDASettings) u NVDA izborniku Postavke.

Iako bi se za kretanje pomoću miša trebao koristiti miš ili trackpad, NVDA ima neke prečace povezane uz miš:
<!-- KC:beginInclude -->

| Naziv |Prečac za stolna računala |Prečac za prenosna računala |Dodir |Opis|
|---|---|---|---|---|
|Lijeva tipka miša |Podijeljeno na numeričkoj tipkovnici |NVDA+[ |Nema |Pritišće lijevu tipku miša jedamput. Uobičajeni dvustruki pritisak postiže se pritiskom ove tipke dva puta brzo.|
|Zaključavanje lijeve tipke miša |shift+Podijeljeno na numeričkoj tipkovnici |NVDA+control+[ |Nema |Zaključava lijevu tipku miša. Pritisnite opet za otpuštanje. Za premještanje miša, pritisnite ovu tipku kako biste zaključali miš i pomićite miš fizički ili ili koristite prečace za usmjeravanje miša|
|Desna tipka miša |množenje na numeričkoj tipkovnici |NVDA+] |Dodirnite i držite |Jednokratan pritisak desne tipke miša U većini slučajeva koristi se za otvaranje kontekstnog izbornika na poziciji miša.|
|Zaključavanje desne tipke miša |shift+numeričko množenje |NVDA+control+] |Nema |Zaključava desnu tipku miša. Pritisnite opet za otpuštanje. Kako biste premjestili miš, pritisnite ovu tipku i pomićite miš fizički ili koristite jedan od prečaca za premještavanje miša|
|Premjesti miš na sljedeći objekt navigatora |NVDA+numeričko dijeljenje |NVDA+shift+m |nema |Premještava miš na sljedeći objekt navigatora i preglednog kursora|
|Premjesti tipkovnicu na objekt pod mišem |NVDA+numeričko množenje |NVDA+shift+n |nema |postavlja objekt navigatora na poziciju miša|

<!-- KC:endInclude -->

## Modus čitanja {#BrowseMode}

Kompleksni dokumenti koji su samo za čitanje kao na primjer web stranice, se u NVDA čitaču pregledavaju pomoću modusa čitanja.
Ovo uključuje dokumente sljedećih aplikacija:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML poruke u Microsoft Outlooku
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Podržane knjige u Amazon Kindle za osobna računala

Modus čitanja je opcionalno dostupan i za Microsoft Word dokumente.

U modusu čitanja, html dokument je dostupan u virtualnom pregledu koji omogućuje kretanje pomoću kursorskih tipaka kao da se radi o običnom tekstualnim dokumentu.
Svi NVDA prečaci [kursora sustava](#SystemCaret) rade u ovom modusu; npr. Izgovori sve, Izvijesti o promjenama oblikovanja, prečaci za kretanje po tablicama itd.
Kad je [Vizualno praćenje](#VisionFocusHighlight) uključeno, na ekranu se pokazuje pozicija objekta.
Informacije o tome je li tekst poveznica, naslov itd. se izgovaraju tijekom kretanja po tekstu.

Ponekad ćete se trebati služiti kontrolama u tom dokumentu.
Na primjer, to ćete trebati činiti u poljima za uređivanje teksta i popisima tako da možete upisivati znakove i koristiti kursorske tipke da biste mogli raditi s tom kontrolom.
To činite tako da se prebacujete u modus fokusa, gdje su sve tipke proslijeđene kontroli.
Kad ste u modusu čitanja, NVDA će se standardno automatski prebaciti na modus fokusa, ako s tabom dođete ili kliknete na određenu kontrolu koja to zahtjeva.
U obratnom slučaju, pritiskom taba ili entera na kontrolu koja ne zahtjeva modus fokusa NVDA će se prebaciti natrag na modus čitanja.
Također, možete pritisnuti enter ili razmaknicu da biste se prebacili na modus fokusa za kontrole koje ga zahtjevaju.
Kad pritisnete escape, vratit ćete se u modus čitanja.
Dodatno, ručno možete uključiti modus fokusa, nakon čega će ostati aktivan sve dok ne odaberete da ćete ga isključiti.

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Mijenjaj između modusa čitanja i modusa fokusa |NVDA+razmaknica |Prebacuje između modusa fokusa i modusa čitanja|
|Izađi iz modusa fokusa |escape |Prebacuje natrag na modus čitanja, ako je prije toga modus fokusa prebačen na automatski|
|Osvježi dokument u modusu čitanja |NVDA+f5 |Osvježava trenutačni sadržaj dokumenta (korisno kad izgleda da neki dio sadržaja nedostaje iz dokumenta Nije dostupno u Microsoft Wordu i Outlooku.)|
|Traži |NVDA+kontrol+f |Otvara dijaloški okvir pretrage, u kojem možete upisati tekst koji tražite u dokumentu. Pogledajte [Traženje teksta](#SearchingForText) za daljnje informacije.|
|Traži sljedeće |NVDA+f3 |Traži sljedeće pojavljivanje teksta u dokumentu kojeg ste prethodno tražili|
|Traži prethodno |NVDA+šift+f3 |Traži prethodno pojavljivanje teksta u dokumentu kojeg ste prethodno tražili|

<!-- KC:endInclude -->

### Brzo kretanje pomoću početnih slova {#SingleLetterNavigation}

Kad se nalazite u modusu čitanja, za brže kretanje, NVDA također pruža jednoslovne prečace za premještanje na razna polja u dokumentu.
Imajte na umu da neki prečaci nisu dostupne u svim vrstama dokumenata.

<!-- KC:beginInclude -->
Sljedeće tipke služe za premještanje na idući dostupni element, dodavanjem šifta se premještate na prethodni element:

* h: naslov
* l: popis
* i: stavka popisa
* t: tablica
* k: poveznica
* n: tekst nakon poveznice
* f: polje obrasca
* u: neposjećena poveznica
* v: posjećena poveznica
* e: polje za uređivanje
* b: gumb
* x: potvrdni okvir
* c: odabirni okvir
* r: izborni gumb
* q: citat
* s: rastavljač
* m: okvir
* g: slika
* d: orjentir
* o: ugrađeni objekt (audio i video player, aplikacija, dijaloški okvir, itd.)
* 1 do 6: naslovi od 1 do 6
* a: zabilješka (komentar, revizija urednika, itd.)
* `p`: odlomak teksta
* w: pravopisna pogreška

Da biste se premjestili na početak ili kraj sadržaja elementa kao što su popisi ili tablice:

| Naziv |Tipka |Opis|
|---|---|---|
|Premjesti se na početak sadržaja |šift+zarez |Premješta se na početak sadržaja (popisa, tablice, itd.) gdje se nalazi kursor|
|Premjesti se na kraj sadržaja |zarez |Premješta se na kraj sadržaja (popisa, tablice, itd.) gdje se nalazi kursor|

<!-- KC:endInclude -->

Neke web aplikacije poput Gmaila, Twittera i Facebooka koriste jednoslovne tipkovničke prečace.
Ako ih želite koristiti istovremeno s kursorskim tipkama kako biste mogli nesmetano čitati sadržaj web stranice, NVDA prečace za brzo kretanje po dokumentu možete privremeno deaktivirati.
<!-- KC:beginInclude -->
Da biste isključili ili uključili brzo kretanje za trenutačni dokument, pritisnite tipke NVDA+šift+razmaknica.
<!-- KC:endInclude -->

#### Prečac za kretanje po odlomcima {#TextNavigationCommand}

Možete se kretati između sljedećeg i prethodnog odlomka tako da pritisnete `p` ili `shift+p`.
Odlomci teksta su definirani kao grupa teksta koja je napisana punim rečenicama.
Ovo može biti korisno za pronalaženje čitljivog sadržaja na raznim web stranicama poput:

* novinskih portala
* Foruma
* objava na blogovima

Ovaj set prečaca može biti od koristi pri preskakanju stvari koje mogu odvući pažnju korisnika poput:

* reklama
* izbornika
* zaglavlja

Imajte na umu, da iako NVDA pokušava najbolje otkriti odlomke teksta, algoritam nije savršen i s vremena na vrijeme mogu se pojaviti greške.
Dodatno se ovaj prečac razlikuje od prečaca za kretanje po odlomcima `control+strelicaDolje/gore`.
Prečac za kretanje po odlomcima teksta premješta između odlomaka teksta, dok prečaci za kretanje po odlomcima premještaju kursor na prethodni-sljedeći odlomak, neovisno od toga sadrže li tekst ili ne.

#### Drugi prečaci za kretanje {#OtherNavigationCommands}

Osim prečaca za kretanje koji su popisani više, NVDA NVDA posjeduje prečace koji nisu definirani.
Kako biste ih koristili, morate ih definirati koristeći [dijaloški okvir ulaznih gesti](#InputGestures).
Ovdje su popisani dostupni prečaci

* Članak
* figura
* Grupiranje
* Kartica svojstava
* stavka izbornika
* Preklopni gumb
* Traka napredka
* Matematička formula
* Okomito poravnat odlomak
* Tekst istog stila
* Tekst različitog stila

Imajte na umu da postoje dva tipa prečaca za kretanje po elementima za kretanje u naprijed i u nazad po dokumentu te morate pridjeliti oba prečaca kako biste se mogli kretati u oba smjera.
Na primjer, ako biste htjeli koristiti `y` / `šift+y` tipke za brzo kretanje po karticama svojstva, učinit ćete slijedeće

1. Otvorit ćete dijaloški okvir ulaznih gesti iz modusa čitanja.
1. Pronači ćete "premješta se na sljedeću karticu svojstva" u odjeljku modus čitanja.
1. Pridjelit ćete slovo `y` za pronađeni prečac.
1. Pronaći ćete "premjesti se na prethodnu karticu svojstva".
1. Pridjelit ćete `šift+y` za pronađeni prečac.

### Popis elemenata {#ElementsList}

Popis elemenata prikazuje razne vrste elemenata, što ovisi od aplikacije do aplikacije.
Na primjer, u web preglednicima, popis elemenata može izraditi popis poveznica, naslova, gumba, polja obrazaca ili orijentira.
Izborni gumbi omogućuju prebacivanje između raznih vrsta elemenata.
U dijaloškom okviru također postoji polje za uređivanje koje omogućuje filtriranje popisa, kao pomoć pri traženju konkretne stavke na stranici.
Kad ste odabrali stavku, možete koristiti ponuđene gumbe u dijaloškom okviru za premještanje na element ili za njegovo aktiviranje.
<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Popis elemenata u modusu čitanja |NVDA+f7 |Popisuje razne vrste elemenata u trenutačnom dokumentu|

<!-- KC:endInclude -->

### Traženje teksta {#SearchingForText}

Ovaj dijaloški okvir omogućuje traženje teksta u trenutačnom dokumentu.
U polju za uređivanje "Utipkaj tekst kojeg želiš pronaći" možete upisati tekst koji tražite.
Potvrdni okvir "Razlikovanje velikih i malih slova" služi za razlikovanje velikih i malih slova prilikom traženja.
Na primjer, kad je potvrdni okvir "Razlikovanje velikih i malih slova" označen, moći ćete pronaći "NV Access", ali ne i "nv access".
Za traženje teksta koristite sljedeće prečace:
<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Traži tekst |NVDA+kontrol+f |Otvara dijaloški okvir pretrage|
|Traži sljedeće |NVDA+f3 |Traži sljedeće pojavljivanje trenutačno traženog teksta|
|Traži prethodno |NVDA+šift+f3 |Traži prethodno pojavljivanje trenutačno traženog teksta|

<!-- KC:endInclude -->

### Ugrađeni objekti {#ImbeddedObjects}

Web stranice mogu uključivati obogaćeni sadržaj koristeći tehnologije kao što su Oracle Java i HTML5, kao i aplikacije i dijaloške okvire.
NVDA će izgovoriti "ugrađeni objekt", "aplikacija" ili "dijaloški okvir" Gdje su takvi objekti otkriveni.
Možete se brzo kretati po njima koristeći o i šift+o prečace za brzo kretanje po ugrađenim objektima.
Kako biste ušli u interakciju s tim objektima, pritisnite tipku enter kad se nalazite na njima.
Ako je pristupačan, možete u njemu pritiskati tabulator i koristiti ga kao u svim drugim aplikacijama.
Postoji prečac za vraćanje na izvornu stranicu koja sadrži taj ugrađeni objekt:
<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Premjesti se na dokument sadržaja u modusu čitanja |NVDA+kontrol+razmaknica |Premješta kursor iz trenutačnog ugrađenog objekta u dokument koji ga sadrži|

<!-- KC:endInclude -->

### Način kopiranja sa sačuvanim oblikovanjem {#NativeSelectionMode}

Poodrazumjevano, prilikom označavanja teksta uz pomoć `shift+strelica` u modusu čitanja, tekst se označava samo unutar virtualnog prikaza NVDA, ali ne i unutar same aplikacije.
To znači da označeni tekst nije vidljiv na zaslonu, a kopiranje teksta uz pomoć prečaca `control+c` će kopirati samo prikaz čistog teksta sadržaja. i.e. formatting of tables, or whether something is a link will not be copied.
Međutim, NVDA pruža način kopiranja sa sačuvanim formatiranjem koji se može uključiti u određenim dokumentima u modusu čitanja (za sada samo u Mozilla firefoxu) što prouzrokuje da označeni tekst prati odabir teksta na zaslonu.

<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Uključi način kopiranja sa sačuvanim oblikovanjem |`NVDA+shift+f10` |Uključuje i isključuje način kopiranja sa sačuvanim formatiranjem|

<!-- KC:endInclude -->

Kada se način kopiranja sa čuvanjem formatiranja uključi, kopiranje označenog teksta uz pomoć prečaca `control+c` koiristit će funkcionalnost kopiranja aplikacije, što znači a će oblikovanje biti kopirano u međuspremnik, umjesto čistog teksta.
Ovo znači da ljepljenje tog teksta u program poput Microsoft Worda ili Excela, oblikovanje poput tablica i poveznica bit će kopirano.
Imajte međutim na umu da u načinu kopiranja sa sačuvanim oblikovanjem, neke oznake pristupačnosti i informacije koje generira NVDA u modusu čitanja neće biti uključene.
Također, iako će NVDA učiniti sve da preslika oblikovanje u modus čitanja, može biti u nekim slučajevima netočno.
Međutim, za scenarije kada želite kopirati cijelu tablicu ili odlomak sa oblikovanjem, ova se funkcija pokazala korisnom.

## Čitanje matematičkog sadržaja {#ReadingMath}

Uz pomoć NVDA se možete kretati po matematičkom sadržaju na web stranicama i u drugim aplikacijama, koristeći govor i brajicu. 
Međutim, kako bi NVDA mogao čitati matematički sadržaj, najprije trebate instalirati matematički komponentu za NVDA.
Postoji nekoliko NVDA dodataka u add-on storeu koji omogućuju pristup matematičkom sadržaju, uključujući [MathCAT NVDA add-on](https://nsoiffer.github.io/MathCAT/) i [Access8Math](https://github.com/tsengwoody/Access8Math). 
Molimo pogledajte poglavlje [Add-on Store](#AddonsManager) kako biste saznali kako pregledavati i instaliravati dostupne dodatke unutar NVDA.
NVDA također može koristiti stariji [MathPlayer](https://info.wiris.com/mathplayer-info) softver tvrtke Wiris ako se pronađe u vašem sustavu, iako ovaj softver se više ne razvija.

### Podržani matematički sadržaj {#SupportedMathContent}

Sa odgovarajućom komponentom instaliranom u NVDA, NVDA podržava sljedeće tipove matematičkog sadržaja:

* MathML u Mozilla Firefoxu, Google Chromeu i Microsoft Internet Exploreru.
* Microsoft Word 365 suvremene matematičke jednadžbe uz pomoć UI automation:
NVDA može čitati i ulaziti u interakciju sa matematičkim jednadžbama u Microsoft Word 365/2016 međuverziji 14326 i novijim.
Note however that any previously created MathType equations must be first converted to Office Math.
Ovo može biti učinjeno tako da se označi svaka te odabere "Opcije jednadžbe", potom "Konvertiraj u Office matematiku" u kontekstnom izborniku.
Prije nego što to učinite, uvjerite se da posjedujete posljednju verziju MathPlayera.
Microsoft Word pruža linearno kretanje bazirano na znakovima po jednadžbama te podržava unos matematike korištenjem nekoliko sintaksi, uključujući LateX.
Za više detalja, molimo pogledajte [Jednadžbe u linearnom formatu koristeći UnicodeMath i LaTeX u Wordu](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint, i starije inačice Microsoft Worda: 
NVDA može čitati i kretati se po MathType jednadžbama u Microsoft Wordu i Powerpointu.
MathType mora biti instaliran kako bi ovo radilo.
Probna verzija je dovoljna.
Može se preuzeti sa [Stranice prezentacije MathType](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Imajte na umu, da ovo još uvijek nije službeni standard, stoga ne postoji dostupan softver s kojim se može izrađivati takav tip sadržaja.
* Kindle Reader za osobna računala:
NVDA može čitati matematiku u Kindle readeru za osobna računala u knjigama u kojima se nalazi pristupačna matematika.

Dok čita dokument, NVDA će izgovoriti bilo koji podržani matematički sadržaj gdje se pojavi.
Ako koristite brajični redak, sadržaj će se prikazati i na brajičnom retku.

### Interaktivno kretanje {#InteractiveNavigation}

Ako primarno radite uz pomoć govora, u većini slučajeva ćete htjeti ispitati manje segmente izraza, umjesto slušanja cijelog izraza odjedanput.

Ako ste u modusu čitanja, to možete učiniti pomicanjem kursora i pritiskom tipke enter.

Ako niste u modusu čitanja:

1. Pomaknite pregledni kursor na matematički sadržaj.
Pregledni kursor standardno prati kursor sustava, tako da je obično moguće koristiti kursor sustava za premještanje na željeni sadržaj.
1. Potom, pritisnite sljedeći prečac:

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Uđi u interakciju s matematičkim sadržajem |NVDA+alt+m |Započinje interakciju s matematičkim sadržajem.|

<!-- KC:endInclude -->

U tom trenutku, NVDA će aktivirati način matematike, u kojem možete koristiti prečace poput strelica kako biste istražili izraz.
Na primjer, možete se pomicati po izrazu uz pomoć lijeve i desne strelice ili dublje zaroniti u izraz kao što je razlomak, koristeći strelicu dolje.

Kad se želite vratiti u dokument, pritisnite tipku escape.

Za više informacija o postavkama i načinima kretanja po matematičkom sadržaju, Molimo pogledajte dokumentaciju vaše određene komponente za čitanje matematike koju ste instalirali.

* [Dokumentacija za MathCat](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math dokumentacija](https://github.com/tsengwoody/Access8Math)
* [MathPlayer dokumentacija](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Ponekada se matematički sadržaj može prikazivati kao gumb ili drugi tip elementa koji kada je aktiviran može prikazati dijaloški okvir sa više informacija o formuli.
Kako biste aktivirali gumb ili element koji sadrži formulu, Pritisnite ctrl+enter.

### Instaliranje MathPlayera {#InstallingMathPlayer}

Iako je uobičajeno preporučeno korištenje jednog od novijih NVDA dodataka za podršku matematike u NVDA, u nekim ograničenim scenarijima MathPlayer može još uvijek biti prihvatljiva opcija.
Na primjer MathPlayer može podržavati određeni jezik ili standard brajice koji nisu podržani u novijim dodacima.
MathPlayer je besplatno dostupan na web stranici Wiris.
[Preuzmite MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Poslije instalacije MathPlayera, trebat ćete ponovno pokrenuti NVDA. 
Imajte na umu da u informacijama može biti naznačeno da je MathPlayer samo za starije preglednike poput Internet Explorera 8.
Ovo se odnosi na vizualni prikaz matematike, i oni koji koriste MathPlayer za čitanje matematike sa NVDA, slobodno mogu ovo ignorirati.

## Brajica {#Braille}

Ako posjedujete brajični redak, NVDA može prikazivati informacije koristeći brajicu.
Ako vaš brajični redak posjeduje perkins tipkovnicu, možete pisati kratkopisom ili punim pismom.
Brajica također može biti prikazana koristeći [preglednik brajice](#BrailleViewer) umjesto na brajičnom retku, ili se može prikazivati na brajičnom retku i uz pomoć preglednika brajice.

Za više informacija o podržanim brajičnim redcima, pogledajte poglavlje [Podržani brajični redci](#SupportedBrailleDisplays).
To poglavlje sadrži dodatne informacije o tome, koji brajični redci podržavaju automatsko otkrivanje brajičnih redaka.
Možete konfigurirati brajicu koristeći [kategoriju Brajica](#BrailleSettings) u dijaloškom okviru [NVDA Postavke](#NVDASettings).

### Kratice za orijentire, stanja i vrste kontrola {#BrailleAbbreviations}

Kako bi stalo što više informacija na brajični redak, definirane su sljedeće kratice za vrste i stanja kontrola te za orijentire.

| Kratica |Vrsta kontrole|
|---|---|
|ap |aplikacija|
|čl |članak|
|ct |citat|
|gb |gumb|
|gbpp |gumb padajućeg popisa|
|ogb |okretni gumb|
|odgb |odvojeni gumb|
|pgb |preklopni gumb|
|opis |opis|
|oo |odabirni okvir|
|po |potvrdni okvir|
|do |dijaloški okvir|
|dok |dokument|
|tp |tekstualno polje|
|pl |polje lozinke|
|uo |ugrađeni objekt|
|zb |završna bilješka|
|sl |slika|
|fn |fusnota|
|gra |grafika|
|gr |grupa|
|nx |naslov razine x, npr. n1, n2|
|bp |balončić pomoći|
|or |orijentir|
|pvz |poveznica|
|ppvz |posjećena poveznica|
|pp |popis|
|iz |izbornik|
|tiz |traka izbornika|
|gbiz |gumb izbornika|
|stiz |stavka izbornika|
|plč |ploča|
|tn |traka napretka|
|iz |indikator zauzetosti|
|igb |izborni gumb|
|kt |klizna traka|
|odj |odjeljak|
|tst |traka stanja|
|kk |kontrola kartica|
|tbl |tablica|
|sx |broj stupca tablice, npr. s1, s2|
|rx |broj redka u tablici, npr. r1, r2|
|trm |terminal|
|at |alatna traka|
|as |alatni savjetnik|
|sp |stablasti prikaz|
|gbsp |gumb za stablasti prikaz|
|ssp |stavka stablastog prikaza|
|raz x |stavka stabla na razini x u hierarhiji|
|pr |prozor|
|⠤⠤⠤⠤⠤ |rastavljač|
|⠕⠃⠣⠮ |obilježen sadržaj|

Definirane kratice za indikatore stanja:

| Kratica |Stanje kontrole|
|---|---|
|... |prikazuje se kad objekt podržava automatsko dovršavanje|
|⢎⣿⡱ |prikazuje se kad je objekt pritisnut (npr. preklopni gumb)|
|⢎⣀⡱ |prikazuje se kad objekt nije pritisnu (npr. preklopni gumb)t|
|⣏⣿⣹ |prikazuje se kad je potvrdni okvir označen|
|⣏⣸⣹ |prikazuje se kad je potvrdni okvir polovično označen|
|⣏⣀⣹ |prikazuje se kad potvrdni okvir nije označen|
|- |prikazuje se kad je objekt sklopiv (npr. stavka u prikazu stabla)|
|+ |prikazuje se kad je objekt rasklopiv (npr. stavka u prikazu stabla)|
|*** |prikazuje se kad se otkrije zaštićena kontrola ili dokument|
|klk |prikazuje se kad je objekt moguće kliknuti|
|kom |prikazuje se kad postoji komentar za ćeliju tablice ili dio teksta u dokumentu|
|frml |prikazuje se kad postoji formula u ćeliji tablice|
|neispravno |prikazuje se kad se upiše neispravna informacija|
|dgopis |prikazuje se kad objekt sadrži dugi opis (često se radi o slici)|
|vr |prikazuje se kad polje za uređivanje sadrži više redaka (kao što je polje za komentar na web stranicama)|
|obv |prikazuje se kad se otkrije obvezno polje|
|szč |prikazuje se kad je objekt samo za čitanje (npr. tekstualno polje za uređivanje)|
|oz |prikazuje se kad je objekt označen|
|neoz |prikazuje se kad objekt nije označen|
|svruzl |prikazuje se kad je popis svrstan uzlazno|
|svrsil |prikazuje se kad je popis svrstan silazno|
|podiz |prikazuje se kad objekt ima skočni prozorčić (često se radi o podizborniku)|

Definirane kratice za orijentire:

| Kratica |Orijentir|
|---|---|
|nslv |naslov|
|ios |informacije o sadržaju|
|ns |neovisni sadržaj|
|obrz |obrazac|
|glv |glavni sadržaj|
|nav |navigacija|
|pret |pretraživanje|
|pdrč |područje|

### Brajični unos {#BrailleInput}

NVDA podržava pisanje punim pismom i kratkopisom putem brajične tipkovnice.
Brajičnu tablicu koja služi za prijevod brajice u tekst možete podesiti u postavci [Ulazna tablica](#BrailleSettingsInputTable), u kategoriji Brajica, u dijaloškom okviru [NVDA Postavke](#NVDASettings).

Kad se koristi puno pismo, tekst se umeće tijekom upisa.
Kad se koristi kratkopis, tekst se umeće nakon pritiskanja razmaknice ili tipke enter na kraju riječi.
Imajte na umu, da prijevod djeluje na brajičnu riječ koju upisujete i ne uključuje postojeći tekst.
Na primjer, ako koristite brajični kod koji sadrži pravilo, da brojevi započinju znakom za broj (ljestve) i pritisnete backspace za prebacivanje na kraj broja, morat ćete ponovo upisati znak za broj, da biste mogli upisati dodatne brojeve.

<!-- KC:beginInclude -->
Pritiskom točkice 7 briše se zadnja brajična ćelija ili znak.
Točkica 8 prevodi svaki brajični unos i pritišće tipku enter.
Pritiskom kombinacije točkice 7 + točkice 8 prevodi svaki brajični unos, ali bez dodavanja razmaka ili pritiskanja tipke enter.
<!-- KC:endInclude -->

#### Izvođenje tipkovničkih prečaca {#BrailleKeyboardShortcuts}

NVDA podržava izvođenje tipkovničkih prečaca i emulaciju pritiska tipaka uz pomoć brajičnog redka.
Ova emulacija dolazi u dva oblika: pridjeljivanje određene tipkovničke kombinacije brajičnom unosu i te korištenje virtualnih modifikacijskih tipki.

Često korištene tipke, poput strelica ili tipke alt za pristup izbornicima mogu se direktno mapirati na brajični unos.
Upravljački program svakog brajičnog redka već dolazi programiran sa takvim definicijama.
Možete promijeniti te definicije ili dodati nove emulirane tipke koristeći [dijaloški okvir ulaznih gesti](#InputGestures).

Iako je takva metoda korisna za uobičajene ili često korištene tipkovničke prečace (poput tipke Tab), ne biste željeli dodjeljivati definiciju za svaki prečac.
Kako bi se emulirali pritisci tipaka koji se zadržavaju, NVDA pruža prečace za uključivanje ili isključivanje control, alt, shift, windows, i NVDA tipaka, kao i prečace za druge kombinacije takvih tipki.
Kako biste koristili te tipke, prvo pritisnite prečac (ili sekvencu prečaca) za modifikator koji želite pritisnuti. 
Poslije toga pritisnite drugi dio prečaca kojeg želite izvesti.
Na primjer, kako biste pritisnuli CTRL+f, koristite prečac "prebacivanje tipke CTRL" a potom pritisnite f,
a kako biste izveli prečac ctrl+alt+t, koristite prečace "uključi tipku Ctrl" i "uključi alt tipku", u bilo kojem poredku, ili prečac "uključi CTRL i alt tipke", poslije kojeg trebate napisati "t".

Ako slučajno uključite modifikacijsku tipku, pokretanje prečaca za ukljućivanje će poništiti modifikator.

Kada pišete kratkopisom, korištenje uključenja modifikatora će prouzročiti da vaš brajični ulaz bude preveden kao da ste pritisnuli točkice 7 i 8.
Još ćemo dodati, da emulirani pritisak tipke ne može i neće utjecati na napisani brajični tekst prije uključenja modifikatora.
To znači da ako biste htjeli pritisnuti alt+2 sa brajičnom tablicom koja koristi brojčani znak, najprije morate uključiti alt, a potom a nakon toga upisati brojčani znak.

## Vid {#Vision}

Iako je NVDA namijenjen slijepim i slabovidnim korisnicima koji koriste govor ili brajicu kako bi koristili računalo, NVDA pruža i ugrađene mogućnosti za mijenjanje sadržaja ekrana.
Unutar NVDA čitača, takva vizualna pomoć se zove poboljšanje vidljivosti.

NVDA nudi nekoliko ugrađenih poboljšanja vidljivosti koji su opisani niže dolje.
Dodatna poboljšanja vidljivosti se mogu ponuditi kao [NVDA dodaci](#AddonsManager).

NVDA postavke vida se mogu promijeniti u kategoriji [Vid](#VisionSettings), u dijaloškom okviru [NVDA Postavke](#NVDASettings).

### Vizualno praćenje {#VisionFocusHighlight}

Vizualno praćenje pomaže prepoznati [fokus sustava](#SystemFocus), [navigacijski objekt](#ObjectNavigation) i [modus čitanja](#BrowseMode).
Pozicije se ističu obojanim pravokutnikom.

* Plava ističe kombiniranu poziciju navigacijskog objekta i fokusa sustava (npr. jer [navigacijski objekt prati fokus sustava](#ReviewCursorFollowFocus)).
* Iscrtkana plava ističe samo objekt fokusa sustava.
* Ružičasta ističe samo navigacijski objekt.
* Žuta ističe virtualni kursor koji se koristi u modusu čitanja (gdje ne postoji fizički kursor, npr. u internetskim preglednicima).

Kad je vizualno praćenje uključeno u kategoriji [Vid](#VisionSettings), u dijaloškom okviru [NVDA Postavke](#NVDASettings), možete [promjeniti isticanje fokusa, navigacijskog objekta ili kursora u modusu čitanja](#VisionSettingsFocusHighlight)

### Ekranska zavjesa {#VisionScreenCurtain}

Kao slijep ili slabovidan korisnik, često nije moguće ili potrebno vidjeti sadržaj ekrana.
Pored toga je ponekad teško znati, gleda li netko preko vašeg ramena.
Zbog takvih situacija, NVDA sadrži funkciju "Ekranska zavjesa" koja se može uključiti kako bi se zatamnio ekran.

Ekransku zavjesu možete uključiti u kategoriji [Vid](#VisionSettings), u [NVDA Postavkama](#NVDASettings).

<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Uključuje i isključuje zaslonsku zavjesu |`NVDA+control+escape` |Uključite ako želite učiniti zaslon crnim ili isključite ako želite vidjeti sadržaj zaslona. Kada se pritisne jedamput, zaslonska zavjesa je uključena sve dok je NVDA uključen. Kada se pritisne dva put, zaslonska zavjesa je uključena uvijek|

<!-- KC:endInclude -->

Kada je zaslonska zavjesa uključena, neki zadaci koji su bazirani na sadržaju ekrana kao što je to izvođenje [prepoznavanja teksta](#Win10Ocr) ili slikanja zaslona ne mogu biti izvedeni.

Zbog izmjena u Api-ju lupe sustava windows, značajka zaslonska zavjesa  je obnovljena kako bi radila sa novijim verzijama operacijskog sustava Windows.
Koristite NVDA 2021.2 kako biste aktivirali zaslonsku zavjesu u operacijskom sustavu Windows 10 21H2 (10.0.19044) i novijim.
Iz sigurnosnih razloga, kada koristite noviju inačicu sustava Windows, trebali biste pitati čovjeka koji normalno vidi radi li ova funkcija.

Imajte na umu kada je Windowsowa lupa uključena sa uključenom opcijom inverzije boja, zaslonska se zavjesa ne može uključiti.

## Prepoznavanje sadržaja {#ContentRecognition}

Kad autori ne daju dovoljno informacija korisniku čitača ekrana, kako bi mogao prepoznati informaciju, mogu se koristiti razni alati, kako bi se tekst mogao prepoznati sa slike.
NVDA podržava funkciju za optičko prepoznavanje znakova (OCR), koja je ugrađena u Windowse 10 i novije inačice kako bi se tekst mogao prepoznati sa slika.
Dodatni prepoznavači sadržaja se mogu ponuditi putem NVDA dodataka.

Pri korištenju naredbe za prepoznavanje sadržaja, NVDA prepoznaje sadržaj s trenutačnog [navigacijskog objekta](#ObjectNavigation).
Navigacijski objekt standardno prati fokus sustava i pokazivač u modusu čitanja, tako da kursor možete premještati po želji.
Na primjer, ako premjestite kursora modusa čitanja na sliku, prepoznavanje će standardno prepoznati sadržaj slike.
Međutim, možda biste kretanje po objektima željeli koristiti izravno, kako biste prepoznali sadržaj cijelog prozora aplikacije.

Kad prepoznavanje završi, rezultat će se predstaviti slično modusu čitanja, omogućujući čitanje objekta kursorskim tipkama, itd.
Pritiskom tipke enter ili razmaknice aktivirat će (kliknuti) tekst pri kursoru, ako je moguće.
Pritiskom tipke escape se rezultat prepoznavanja odbacuje.

### Windows OCR {#Win10Ocr}

Windows 10 i novije inačice uključuju OCR za mnoge jezike.
NVDA može to koristiti kako bi se prepoznavao tekst sa slike ili nedostupne aplikacije.

Jezik prepoznavanja možete postaviti u [kategoriji Windows OCR](#Win10OcrSettings) [u dijaloškom okviru postavki](#NVDASettings).
Dodatni jezici se mogu instalirati putem izbornika Start>Postavke>Vrijeme i Jezik>Regija i jezik, a zatim Dodaj jezik.

Kada želite čitati sadržaj koji se stalno mijenja, poput videa sa titlovima koji se stalno mijenjaju, možete uključiti automatsko osvježavanja prepoznatog sadržaja.
Ovo se također može učiniti u [Windows OCR kategoriji](#Win10OcrSettings) u dijaloškom okviru [NVDA postavki](#NVDASettings).

Funkcija Windows OCR može biti djelomično ili u cijelosti nekompatibilna sa [NVDA poboljšanjima vida](#Vision) ili drugim vanjskim vizualnim pomagalima. Prije početka prepoznavanja, ta ćete pomagala trebati isključiti.

<!-- KC:beginInclude -->
Za prepoznavanje teksta u navigacijskom objektu koristeći windows ocr, pritisnite NVDA+r.
<!-- KC:endInclude -->

## Značajke specifične za neke aplikacije {#ApplicationSpecificFeatures}

NVDA pruža svoje dodatne značajke  za neke aplikacije kako bi učinio neke zadatke jednostavnijima i kako bi omogučio pristup nekim funkcijama koje nisu inače dostupne korisnicima čitača ekrana.

### Microsoft Word {#MicrosoftWord}
#### Automatsko čitanje zaglavlja redaka i stupaca {#WordAutomaticColumnAndRowHeaderReading}

NVDA može automatski čitati odgovarajuća zaglavlja redaka i stupaca  u tablicama u Microsoft Wordu.
Ovo zahtjeva uključenu opciju Izvještavaj o zaglavljima redaka/stupaca u postavkama oblikovanja dokumenta NVDA koje se nalaze u  [NVDA postavkama](#NVDASettings).

Ako koristite [UIA za pristup dokumentima Microsoft worda](#MSWordUIA), što je podrazumjevana opcija u posljednjim verzijama Microsoft Worda i Windowsa, Ćelije prvog redka će automatsko postati zaglavlja redaka; Slično tome, prvi redak stupca će biti prepoznat kao zaglavlje redka.

U suprotnom, ako ne koristite [UIA za pristup Word dokumentima](#MSWordUIA), morat ćete dati do znanja NVDA, koji redci sadrže zaglavlja u svakoj tablici.
Poslije pomicanja na ćeliju u stupcu ili retku koja sadrži zaglavlja, koristite sljedeće naredbe:
<!-- KC:beginInclude -->

| Ime |Tipka |opis|
|---|---|---|
|postavi zaglavlja stupaca |insert+šift+c |pritišćući ovu kombinaciju nvda zna da je ovo prvo zaglavlje  u redku koje sadržava zaglavlje stupaca, koji trebaju biti automatski izgovoreni kad se krećete po stupcima ispod tog stupca. kad se pritisne dvaput briše postavku.|
|postavi zaglavlja redaka |insert+šift+r |kad se pritisne nvda zna da je to prvo zaglavlje ćelije u stupcu koje sadrži zaglavlje redaka, koji će biti automatski izgovoren šećući se po stupcima između tih stupaca. Kad se pritisne dvaput, izbrisat će se postavka.|

<!-- KC:endInclude -->
Ove će postavke biti spremljene kao knjižne oznake, kompatibilne s drugim čitačima ekrana poput Jawsa. 
To znači ako drugi korisnik otvori isti dokument kasnije, imat će postavljena zaglavlja redaka i stupaca.

#### Modus čitanja u Microsoft wordu {#BrowseModeInMicrosoftWord}

Slično kao i na web stranicama, modus čitanja se može koristiti u Microsoft Wordu, kako bi se omogućilo korištenje funkcija poput brzog kretanja i popisa elemenata.
<!-- KC:beginInclude -->
Kako biste uključili ili isključili modus čitanja (u Microsoft Wordu), pritisnite tipke insert+razmaknica.
<!-- KC:endInclude -->
Za više informacija o modusu čitanja i brzom kretanju, pročitajte [odjeljak o modusu čitanja](#BrowseMode).

##### Popis elemenata {#WordElementsList}

<!-- KC:beginInclude -->
Kad se nalazite u modusu čitanja u Microsoft Wordu, popisu elemenata možete pristupiti pritiskom tipki NVDA+f7.
<!-- KC:endInclude -->
Popis elemenata može popisati naslove, poveznice, primjedbe (koje uključuju komentare i praćenje promjena) i pogreške (trenutačno ograničeno na pravopisne pogreške).

#### Izvještavanje o komentarima {#WordReportingComments}

<!-- KC:beginInclude -->
Za izvještavanje o komentarima na poziciji kursora, pritisnite NVDA+alt+c.
<!-- KC:endInclude -->
Svi komentari za dokument se mogu popisati i u NVDA popisu elemenata.

### Microsoft Excel {#MicrosoftExcel}
#### Automatsko čitanje zaglavlja redaka i stupaca {#ExcelAutomaticColumnAndRowHeaderReading}

Nvda je u stanju čitati odgovarajuća zaglavlja redaka i stupaca pri kretanju po radnim listovima excela.
Ovo najprije zahtijeva uključenu opciju izvijesti o zaglavljima redaka/stupaca u postavkama oblikovanja dokumenta, koje možete pronaći u [NVDA postavkama](#NVDASettings).
Nvda treba znati gdje se nalaze zaglavlja.
poslije premještanja na odgovarajuću ćeliju ili redak koji sadrži zaglavlja, koristite sljedeće prečace:
<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Postavi zaglavlja stupaca |NVDA+šift+c |Kad se pritisne jednom, NVDA zna da je to prva ćelija zaglavlja u retku koja sadrži zaglavlje stupaca, koja treba automatski najaviti kad se premještate po stupcima ispod ovog retka. Kad se pritisne dvaput, postavka se briše.|
|Postavi zaglavlja redaka |NVDA+šift+r |Kad se pritisne jednom, NVDA zna da je to prva ćelija zaglavlja u stupcu koja sadrži zaglavlja redaka, koja treba automatski najaviti kad se premještate po redcima nakon ovog stupca. Kad se pritisne dvaput, postavka se briše.|

<!-- KC:endInclude -->
Ove će se postavke spremiti u radnu knjigu kao definirani imenovani raspon, kompatibilan s drugim čitačima ekrana poput JAWS.
To znači, da će korisnici drugih čitača ekrana, koji kasnije otvore tu radnu knjigu, imati automatski postavljena zaglavlja stupaca i redaka. 

#### Popis elemenata {#ExcelElementsList}

Slično kao i na web stranicama, Nvda ima popis elemenata za microsoft excel, koja omogućuje pristup raznim vrstama informacija.
<!-- KC:beginInclude -->
kako biste pristupili popisu elemenata u excelu, pritisnite NVDA+f7.
<!-- KC:endInclude -->
Razne vrste informacija u popisu elemenata u excelu su:

* Grafikoni: Ovo popisuje sve grafikone u aktivnom radnom listu. 
Označivanjem grafikona i pritiskom tipke enter ili gumba "Prijeđi na", fokusira grafikon za kretanje i čitanje pomoću strelica.
* Komentari: Ovo popisuje sve ćelije u aktivnom radnom listu koje sadrže komentare. 
Adresa ćelije s pripadajućim komentarima se prikazuje za svaku ćeliju. 
Pritiskom tipke enter ili gumba "Prijeđi na", kad se nalazite na popisanom komentaru, premješta se izravno na tu ćeliju.
* Formule: Ovo popisuje sve ćelije u aktivnom radnom listu koje sadrže formulu. 
Adresa ćelije skupa s formulom je prikazuje za svaku ćeliju.
Pritiskom tipke enter ili gumba "Prijeđi na" premjestit će se izravno na tu ćeliju. 
* Radni listovi: Ovo popisuje sve radne listove u radnoj knjizi. 
Pritiskom tipke f2 na odabranom radnom listu omogućuje preimenovanje radnog lista. 
Pritiskom tipke enter ili gumba "Prijeđi na", kad se nalazite na radnom listu, premješta se na taj radni list.
* Obrazci: Ovo popisuje sve obrasce u aktivnom radnom listu.
Za svaki obrazac, u popisu elemenata prikazuje se alternativni tekst polja, zajedno s adresama ćelija koje pokriva.
Biranjem polja obrasca i pritiskom tipke enter ili gumba "Prijeđi na", premješta se na to polje u modusu čitanja.

#### Izvještavanje o bilješkama {#ExcelReportingComments}

<!-- KC:beginInclude -->
Za izvještavanje o bilješkama na poziciji kursora, pritisnite NVDA+alt+c.
In Microsoft Officeu 2016, 365 i novijim inačicama, klasični su komentari u Microsoft Excelu su preimenovani u "bilješke".
<!-- KC:endInclude -->
Sve bilješke za radni list se mogu popisati i u NVDA popisu elemenata poslije pritiska prečaca insert+f7.

NVDA također može prikazati poseban dijaloški okvir za dodavanje ili uređivanje bilješke.
NVDA nadpisuje nativnu kontrolu za upis bilješki u MS excelu zbog problema s pristupačnošću, ali se prećac za pristupanje istoj ne razlikuje stoga radi bez potrebe za uključenim NVDA.
<!-- KC:beginInclude -->
Kako biste dodali ili uredili bilješku u fokusiranoj ćeliji, pritisnite shift+f2.
<!-- KC:endInclude -->

Ovaj se prečac ne prikazuje, stoga se ne može mijenjati u dijaloškom okviru ulaznih gesti.

Upozorenje: također postoji mogućnost otvaranja dijaloškog okvira upisivanja bilješki iz kontekstnog izbornika.
Međutim, to će otvoriti MS excelovu nedostupnu regiju za uređivanje bilješki umjesto specifičnog dijaloškog okvira za uređivanje komentara koji kiristi NVDA.

In Microsoft Officeu 2016, 365 i novijim inačicama, dodan je novi dijaloški okvir za dodavanje komentara.
Ovaj dijaloški okvir je pristupačan te pruža nove značajke poput odgovaranja na komentare i tako dalje
Isti se također može otvoriti iz kontekstnog izbornika određene ćelije.
Komentari koji su dodani iz ovog dijaloškog okvira nisu povezani s "bilješkama".

#### Čitanje zaštićenih ćelija {#ExcelReadingProtectedCells}

Ako je radna knjiga zaštićena, neće možda biti moguće premještati fokus na određene ćelije koje su zaključane za uređivanje.
<!-- KC:beginInclude -->
Kako biste dozvolili premještanje po zaključanim ćelijama, prebacite se na modus čitanja pritiskom tipki NVDA+razmaknica, a potom koristite standardne excelove prečace za kretanje po dokumentu poput strelica, kako biste se premještali po trenutačnom radnom listu.
<!-- KC:endInclude -->

#### Polja obrazaca {#ExcelFormFields}

Excelovi radni listovi mogu sadržavati obrasce.
Možete im pristupiti koristeći popis elemenata ili prečace za brzo kretanje po obrascima f i šift+f.
Jednom kad se premjestite na obrazac u modusu čitanja, možete pritisnuti enter ili razmaknicu kako biste aktivirali ili se prebacili na modus fokusa, kako biste mogli manipulirati s time, ovisno o kontroli.
Za više informacija o modusu čitanja i brzom kretanju, pogledajte poglavlje [Modus čitanja](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Uključi čitanje govornikovih bilješki |kontrol+šift+s |Kad se nalazite u trenutačnom prikazu slajda, ova naredba prebacuje između govornikovih bilješki za slajd i sadržaja slajda. Ovo utječe samo na ono što NVDA čita, ne i na ono što se prikazuje na ekranu.|

<!-- KC:endInclude -->

### Foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Izvijesti o preostalom vremenu |kontrol+šift+r |Izvještava o preostalom vremenu trenutačno svirane pjesme, ako postoji|
|Izvijesti o proteklom vremenu |kontrol+šift+e |Izvještava o proteklom vremenu trenutačno svirane pjesme, ako postoji|
|Izvijesti o trajanju zvučne datoteke |kontrol+šift+t |Izvještava o dužini trenutačno svirane pjesme, ako postoji|

<!-- KC:endInclude -->

Napomena: ovi prečaci rade samo s Foobarovim standardnim stringovima za oblikovanje trake stanja.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Naziv |Tipka |Opis|
|---|---|---|
|Izvijesti o nedavnoj poruci |NVDA+kontrol+1-4 |Izvještava o jednoj od nedavnih poruka, ovisno o pritisnutom broju; npr. NVDA+kontrol+2 čita drugu najnedavniju poruku.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA sadrži unapređenu podršku za Poedit 3.4 ili novije inačice.

<!-- KC:beginInclude -->

| Naziv |prečac |Opis|
|---|---|---|
|Čita bilješke za prevoditelje |`control+šift+a` |Čita bilo koju bilješku za prevoditelje. Kada se pritisne dvaput, pokazuje bilješke u modusu čitanja|
|Čitaj komentar |`control+šift+c` |Čitaj bilo koji komentar u prozoru komentara. Kada se pritisne dvaput, pokazuje komentare u modusu čitanja|
|Čita stari izvorni tekst |`control+šift+o` |Čita stari izvorni tekst, ako postoji. Kada se pritisne dvaput, pokazuje tekst u modusu čitanja|
|Čita upozorenje prijevoda |`control+šift+w` |Čita upozorenje prijevoda, ako postoji. Kada se pritisne dvaput, pokazuje upozorenje u modusu čitanja|

<!-- KC:endInclude -->

### Kindle za osobna računala {#Kindle}

NVDA podržava čitanje i kretanje po knjigama u Amazonovom Kindlu za osobna računala.
Ova je funkcionalnost dostupna samo u Kindle knjigama označenima sa "Screen Reader: Supported", što možete provjeriti na stranici s detaljima o knjizi.

Modus pregleda se upotrebljava za čitanje knjiga.
Automatski je aktiviran kad otvorite knjigu ili kad premjestite fokus na područje knjige.
Stranice će se okretati automatski po potrebi kad pomičete kursor ili prilikom korištenja prečaca "čitaj sve".
<!-- KC:beginInclude -->
možete se ručno prebacivati na sljedeću stranicu uz pomoć tipke pejdž daun i prebacivati na prethodnu stranicu uz pomoć tipke pejdž ap.
<!-- KC:endInclude -->

Brzo kretanje je podržano za poveznice i grafike, ali samo za trenutačnu stranicu.
Kretanje po poveznicama također uključuje fusnote.

NVDA podržava matematiku u Kindleu za PC s knjigama koje imaju pristupačnu matematiku.
Za više informacija, pogledajte poglavlje [čitanje matematičkog sadržaja](#ReadingMath).

#### Odabrani tekst {#KindleTextSelection}

Kindle omogućuje izvođenje različitih funkcija na odabranom tekstu, uključujući izvlačenje objašnjenja iz rječnika, dodavanje bilježaka i oznaka, kopiranje teksta u međuspremnik i pretraživanje interneta.
Kako biste ovo učinili, najprije odaberite tekst na uobičajeni način u modusu čitanja; npr. koristeći šift i kursorske tipke.
<!-- KC:beginInclude -->
Kad ste odabrali tekst, pritisnite aplikacijsku tipku ili šift+f10 kako biste prikazali dostupne opcije za rad s označenim tekstom.
<!-- KC:endInclude -->
Ako to uradite bez odabranog teksta, pokazat će se opcije za riječ pri kursoru.

#### Korisničke bilješke {#KindleUserNotes}

Možete dodavati bilješku koja se odnosi na riječ ili pasus teksta.
Kako biste ovo učinili, najprije odaberite relevantan tekst i pristupite opcijama označenoga teksta kao što je gore opisano.
Potom, odaberite opciju "Dodaj bilješku".

Prilikom čitanja u modusu čitanja, NVDA se odnosi prema bilješkama kao prema komentarima.

Za prikaz, uređivanje ili brisanje bilješke:

1. Premjestite se na tekst koji sadrži bilješku.
1. Pristupite opcijama označenog teksta kao što je gore opisano.
1. Odaberite opciju "Uredi bilješku". Napomena: budući da hrvatski prevoditelj NVDA čitača ekrana ne zna, je li je amazon lokaliziran na hrvatski, preveo je nazive opcija u postupcima za rad s tekstom.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Kad se nalazite u tabličnom pregledu dodanih knjiga:

| Naziv |Tipka |Opis|
|---|---|---|
|Enter |enter |Otvara odabranu knjigu.|
|Kontekstni izbornik |aplikacijska tipka |Otvara kontekstni izbornik za odabranu knjigu.|

<!-- KC:endInclude -->

### Windows naredbeni redak {#WinConsole}

NVDA pruža podršku za Windowsov naredbeni redak, kojeg koristi aplikacija naredbenog retka, PowerShell i Windows podsustav za Linux.
Prozor naredbenog retka je fiksne veličine, tipično mnogo manje od spremnika koji sadrži informaciju.
Tijekom zapisivanja novog teksta, sadržaj kliže prema gore i raniji tekst se više ne vidi. 
U inačicama sustava Windows koje sežu sve do Windows 11 22H2, ali ne uključivo s tom inačicom, tekst u naredbenom redku koji nije vidljiv nije pristupačan sa prečacima preglednog kursora NVDA.
Stoga je potrebno spuštati se po prozoru naredbenog retka, kako bi se pročitao raniji tekst.
U novim inačicama konzole te Windows terminala, sada je moguće pregledati cjelovit spremnik teksta slobodno bez potrebe za podizanjem ili spuštanjem prozora.
<!-- KC:beginInclude -->
Sljedeći ugrađeni tipkovnički prečaci naredbenog retka mogu biti korisni za [Pregledavanje teksta](#ReviewingText) pomoću NVDA čitača zaslona u starijim inačicama Windowsove konzole:

| Naziv |Tipka |Opis|
|---|---|---|
|Kliži gore |kontrol+strelicaGore |Kliže po prozoru naredbenog retka gore, tako da se raniji tekst može čitati.|
|Kliži dolje |kontrol+StrelicaDolje |Kliže po prozoru naredbenog retka dolje, tako da se kasniji tekst može čitati.|
|Kliži na početak |kontrol+houm |Kliže po prozoru naredbenog retka na početak spremnika.|
|Kliži na kraj |kontrol+end |Kliže po prozoru naredbenog retka na kraj spremnika.|

<!-- KC:endInclude -->

## Podešavanje NVDA čitača {#ConfiguringNVDA}

Većina konfiguracije se može obaviti u dijaloškim okvirima podizbornika Postavke, u NVDA izborniku.
Mnoge od tih postavki je moguće pronaći u višestraničnom dijaloškom okviru [NVDA Postavke](#NVDASettings).
Za prihvaćanje učinjenih promjena, pritisnite gumb U redu. To vrijedi za sve dijaloške okvire.
Za odustajanje od promjena, pritisnite gumb Odustani ili tipku escape.
U nekim dijaloškim okvirima je moguće pritisnuti gumb Primijeni, kako bi postavke odmah stupile na snagu.
Neke postavke se mogu promijeniti pomoću tipkovničkih prečaca, koji su navedeni u sljedećim poglavljima.
Većina NVDA dijaloških okvira podržava kontekstualnu pomoć.
<!-- KC:beginInclude -->
Kada se nalazite u dijaloškom okviru, pritisak prečaca `f1` otvara Vodić za korisnike u odlomku koji je vezan za tu određenu postavku ili trenutni dijaloški okvir.
<!-- KC:endInclude -->

### NVDA Postavke {#NVDASettings}

<!-- KC:settingsSection: || Naziv | Tipka za stolna računala | Tipka za prijenosna računala | Opis | -->
NVDA nudi puno postavki koje se mogu promijeniti iz ovog dijaloškog okvira.
Kako biste lakše pronašli tip postavki koji želite promjeniti, dijaloški okvir prikazuje listu sa kategorijama postavki iz koje možete izabrati neku od njih .
Kada izaberete kategoriju, sve postavke vezane za tu kategoriju će se prikazati u dijaloškom okviru.
Da biste se kretali između kategorija, koristite `tab` ili `šift+tab` kako biste došli do popisa kategorija, a zatim koristite strelice gore i dolje kako biste se kretali po popisu.
Bilo gdje iz dijaloškog okvira, možete takođe prijeći na sljedeću kategoriju prečacem `ctrl+tab`, ili na prethodnu prečicom `šift+ctrl+tab`.

Nakon što promenite jednu ili više postavki, postavke se mogu  primijeniti aktiviranjem gumba primjeni, u tom slučaju će dijaloški okvir ostati otvoren, što će vam dozvoliti mijenjanje drugih postavki ili prelazak na drugu kategoriju.
Ako želite spremiti postavke i zatvoriti dijaloški okvir NVDA Postavke, pritisnite gumb U redu.

Neke kategorije postavki imaju vlastiti tipkovnički prečac.
Ako se pritisne, taj prečac će otvoriti NVDA dijaloški okvir postavki izravno u  toj kategoriji.
Pomoću tipkovničkih prečaca nije moguće pristupiti svim kategorijama.
Ako često pristupate kategorijama postavki koje nemaju dodjeljen prečac, možda ćete željeti iskoristiti [dijaloški okvir ulaznih gesti](#InputGestures) kako biste doali prilagođen prečac kao što je to tipkovnički prečac ili gesta na ekranu osjetljivom na dodir za tu kategoriju.

Kategorije postavki u dijaloškom okviru NVDA Postavke se opisuju niže dolje.

#### Opće {#GeneralSettings}

<!-- KC:setting -->

##### Otvara opće postavke {#toc110}

Prečac: `NVDA+kontrol+g`

Kategorija "Opće", u dijaloškom okviru NVDA Postavke, postavlja opće opcije poput jezika ili provjeravanja nadogradnji.
Ova kategorija sadrži sljedeće opcije:

##### Jezik {#GeneralSettingsLanguage}

Ovo je odabirni okvir koji omogućuje biranje jezika na kojem će se prikazati NVDA sučelje i sve poruke.
Postoji puno jezika, međutim standardna opcija je "Korisnički standard, Windows".
Kad je ova opcija aktivna, NVDA koristi standarni jezik sustava.

Imajte na umu, da NVDA morate ponovo pokrenuti kad promijenite jezik.
Kad se pojavi dijaloški okvir za potvrdu, odaberite "Ponovo pokreni sada" ili "Ponovo pokreni kasnije", ako želite koristiti novi jezik sada ili kasnije. Ako odaberete gumb "Ponovo pokreni kasnije", konfiguraciju morate spremiti (ručno ili pomoću opcije "Spremi konfiguraciju pri izlasku").

##### Spremi konfiguraciju pri izlasku {#GeneralSettingsSaveConfig}

Ova opcija je potvrdni okvir. Kad se označi, sprema konfiguraciju pri izlazu.

##### Prikaži opcije izlaza pri izlasku iz NVDA programa {#GeneralSettingsShowExitOptions}

Ova opcija je potvrdni okvir, koji omogućuje prikazivanja ili ne prikazivanja dijaloškog okvira pri izlasku iz NVDA programa, u kojem vas se pita koju radnju želite izvesti.
Kad je potvrdni okvir označen, pri pokušaju izlaska iz NVDA programa, prikazat će se dijaloški okvir u kojem će vas se pitati, želite li isključiti NVDA, ponovo ga pokrenuti, ponovo ga pokrenuti s deaktiviranim dodacima ili instalirati nadogradnje na čekanju, ako ih ima.
Kad potvrdni okvir nije označen, NVDA će se odmah isključiti.

##### Sviraj zvukove pri pokretanju ili izlasku iz NVDA programa {#GeneralSettingsPlaySounds}

Ova opcija je potvrdni okvir. Kad je označen, svirat će se zvukovi pri pokretanju čitača ili pri izlasku iz čitača.

##### Razina zapisivanja {#GeneralSettingsLogLevel}

Ovo je odabirni okvir u kojem se može odabrati količina zapisivanja tijekom rada NVDA čitača.
Zapravo, korisnici ovo ne bi trebali dirati, jer se baš i na zapisuje puno toga.
Međutim, ako želite pružiti više informacija u izvještaju o grešci ili pak potpuno aktivirati ili deaktivirati zapisivanje, onda je ova opcija korisna.

Dostupne razine zapisivanja su:

* Deaktivirano: Osim kratke poruke o pokretanju, NVDA neće zapisivati ništa za svo vrijeme dok radi.
* Informacije: NVDA će zapisivati osnovne informacije, poput poruke o pokretanju te informacije koje su korisne za razvojne programere.
* Debug upozorenja: Upozorenja, koja ne prouzrokuju ozbiljne pogreške će se zapisivati.
* Ulaz/izlaz: Upisani znakovi s tipkovnice ili s brajičnog retka, kao i sve što je poslano govornoj jedinici će se zapisivati.
Ako se bojite za svoju privatnost, ne postavljajte ovu razinu zapisnika.
* Debug: Uz informacije, upozorenja te poruke o ulazima/izlazima, zapisivat će se dodatne poruke koje služe za ispravljanje grešaka.
Kao u slučaju ulaz/izlaz, ako se bojite za svoju privatnost, ne postavljajte ovu razinu zapisnika.

##### Automatski pokreni NVDA nakon što se prijavim u Windows sustav {#GeneralSettingsStartAfterLogOn}

Ako je ova opcija aktivirana, NVDA će se automatski pokrenuti nakon što se prijavite u Windows.
Ova je opcija dostupna samo u instaliranim kopijama NVDA čitača.

##### Koristi NVDA u Windows ekranu prijave (zahtijeva administratorska prava) {#GeneralSettingsStartOnLogOnScreen}

Aktiviranjem ove opcije, NVDA će se automatski pokrenuti na ekranu za prijavu tijekom pokretanja Windows sustava, ako se prijavljujete u Windows upisujući svoje korisničko ime i lozinku.
Ova je opcija dostupna samo u instaliranim kopijama NVDA čitača.

##### Koristi trenutačno spremljene postavke za ekran prijave te ostale sigurne ekrane (zahtijeva administratorska prava) {#GeneralSettingsCopySettings}

Kada pritisnete ovaj gumb, vaša trenutna NVDA  konfiguracija bit će kopirana u mapu NVDA konfiguracije sustava što znači da će ju NVDA koristiti na zaslonu za prijavu te ako se pokreće kontrola korisničkog računa (UAC) te na drugim [sigurnim zaslonima](#SecureScreens).
Da biste se uvjerili da su sve vaše postavke kopirane, prvo spremite vašu konfiguraciju pomoću prečaca kontrol+NVDA+c ili pomoću opcije spremi konfiguraciju u NVDA izborniku.
Ova je opcija dostupna samo u instaliranim kopijama NVDA čitača.

##### Automatski provjeri nadogradnje za NVDA {#GeneralSettingsCheckForUpdates}

Ako je ova opcija uključena, NVDA će automatski provjeriti nadogradnje i obavjestiti vas kad je nadogradnja dostupna.
Nadogradnje možete i ručno provjeriti. Odaberite Provjeri nadogradnje u podizborniku Pomoć u NVDA izborniku.
Pri ručnom ili automatskom provjeravanju nadogradnje, nužno je da NVDA pošalje neke informacije na server za nadogradnje, kako bi vam se isporučila ispravna nadogradnja za vaš operacijski sustav.
Sljedeće informacije se uvijek šalju: 

* Aktualna NVDA verzija
* Verzija operacijskog sustava
* Radi li se o 64 ili 32 bitnom operacijskom sustavu

##### Dozvoli Organizaciji NV Access prikupljanje statističkih podataka  okorištenju NVDA {#GeneralSettingsGatherUsageStats}

Ako je ova opcija aktivirana, NV Access će koristiti informacije dobivene od servera za nadogradnje kako bi pratila broj korisnika uključujući opće demografske statistike kao što su to operacijski sustav i zemlja porijekla.
Imajte na umu da iako vaša IP adresa će biti korištena za izračunavanje vaše države porijekla, ista nije zadržavana na serveru.
Osim obaveznih informacija koje se šalju pri provjeri nadogradnje, trenutačno se šalju i sljedeće informacije:

* Jezik NVDA sučelja
* Vrsta kopije NVDA čitača, instalirana ili prijenosna
* Ime trenutačno korištene govorne jedinice (uključujući ime dodatka od kojeg potiče driver)
* Ime trenutačno korištenog brajičnog retka (uključujući ime dodatka od kojeg potiče driver)
* trenutačno korištena brajična tablica (ako se koristi brajični redak)

Ove informacije puno pomažu programu NV Access postaviti prioritete za budući razvoj NVDA.

##### Tijekom pokretanja obavijesti o nadogradnjama na čekanju {#GeneralSettingsNotifyPendingUpdates}

Ako je ova opcija aktivirana, NVDA će vas tijekom pokretanja informirati o nadogradnji na čekanju, te će ponuditi mogućnost da se instalira.
Nadogradnje na čekanju je moguće i ručno instalirati u dijaloškom okviru Izađi iz programa NVDA (ako je aktivirano) u NVDA izborniku ili ako ponovo provjeravate nadogradnju putem izbornika Pomoć.

#### Postavke govora {#SpeechSettings}

<!-- KC:setting -->

##### Otvara postavke govora {#toc123}

Prečac: `NVDA+kontrol+v`

Kategorija Govor u dijaloškom okviru Postavke, omogućuje mijenjanje govorne jedinice, kao i njenih karakteristika glasa.
Za brže mjenjanje postavki govora s bilo kojeg mjesta pogledajte poglavlje [Kružne postavke govorne jedinice](#SynthSettingsRing).

Kategorija Postavke govora sadrži sljedeće opcije:

##### Promijeni govornu jedinicu {#SpeechSettingsChange}

Prva opcija u kategoriji Postavke govora je gumb "Promijeni …". Ova tipka aktivira dijaloški okvir [Odaberi govornu jedinicu](#SelectSynthesizer), koji omogućuje odabir govorne jedinice i izlaznog uređaja.
Ovaj se dijaloški okvir otvara ispred dijaloškog okvira NVDA postavke.
Spremanjem ili nepreuzimanjem postavki, vraća vas u dijaloški okvir NVDA Postavke.

##### Glas {#SpeechSettingsVoice}

Opcija Glas je odabirni okvir, u kojem su popisani svi glasovi govorne jedinice koje ste instalirali.
Za preslušavanje glasova koristite strelice.
Strelica Lijevo i Gore omogućuju kretanje u popisu prema gore. Strelice Desno i Dolje omogućuju kretanje u popisu prema dolje.

##### Varijanta {#SpeechSettingsVariant}

Ako koristite Espeak NG govornu jedinicu koja dolazi s NVDA čitačem, ovo je odabirni okvir koji omogućuje odabrati varijantu glasa koju će govorna jedinica koristiti za govor.
Espeak NG varijante su bolji glasovi, jer pružaju malo drugačije atribute od Espeak NG glasova.
Neke će varijante zvučati kao muški glasovi, neke kao ženski, neke čak i kao žaba.
Ako koristite govornu jedinicu treće strane i ako vaš odabrani glas govorne jedinice to podržava, možda ćete moći promjeniti ovu opciju.

##### Brzina {#SpeechSettingsRate}

Ova opcija omogućuje promjenu brzine glasa.
Ovaj klizač ima vrijednosti od 0 do 100 (0 je najsporije, 100 je najbrže).

##### Pojačanje brzine {#SpeechSettingsRateBoost}

Ako uključite ovu opciju, brzina će se značajno povećati ako to podržava trenutna govorna jedinica.

##### Visina {#SpeechSettingsPitch}

Ova opcija omogućuje promjenu visine trenutačnog glasa.
Ovaj klizač ima vrijednosti od 0 do 100 (0 je najniže, 100 je najviše).

##### Glasnoća {#SpeechSettingsVolume}

Ovaj klizač ima vrijednosti od 0 do 100 (0 je najtiše, 100 je najglasnije).

##### Intonacija {#SpeechSettingsInflection}

S ovim klizačem je moguće odabrati intonaciju govorne jedinice (dizanje i spuštanje visine pri čitanju) koju će koristiti za govor.

##### Automatsko mijenjanje jezika {#SpeechSettingsLanguageSwitching}

Ovaj potvrdni okvir omogućuje aktiviranje i deaktiviranje automatskog mijenjanja jezika govorne jedinice, ako čitani tekst sadrži podatak o jeziku.
Ova je opcija standardno aktivirana.

##### Automatsko mijenjanje dijalekta {#SpeechSettingsDialectSwitching}

Ovaj potvrdni okvir omogućuje mijenjanje dijalekta, umjesto mijenjanja jezika.
Na primjer, ako čitate tekst glasom namijenjenim za američki engleski, ali je u dokumentu postavljen britanski dijalekt, onda će govorna jedinica prebacivati između naglasaka, ako je ova opcija aktivirana.
Ova je opcija standardno deaktivirana.

<!-- KC:setting -->

##### Razina interpunkcije i simbola: {#SpeechSettingsSymbolLevel}

Prečac: NVDA+p

Ova opcija omogućuje određivanje količine interpunkcijskih znakova i drugih simbola koji se trebaju izgovoriti kao riječi.
Na primjer, kad je ova opcija postavljena na sve, svi će se simboli izgovoriti kao riječi.
Ova se opcija primjenjuje na sve govorne jedinice, ne samo na trenutačno aktivnu.

##### Vjeruj jeziku glasa za čitanje opisa znakova i simbola {#SpeechSettingsTrust}

Standardno je uključena. Ova opcija govori programu NVDA da se jeziku trenutačno odabranog glasa može vjerovati, kad se procesiraju simboli i znakovi.
Ako shvatite da NVDA čita interpunkciju koristeći krivi jezik za određenu govornu jedinicu ili glas, možda biste ovu opciju željeli isključiti kako biste prisilili NVDA da umjesto toga koristi glavnu jezičnu postavku.

##### Koristi Unicode bazu podataka za čitanje opisa znakova i simbola (uključujući emoji znakove) {#SpeechSettingsCLDR}

Kad se ovaj potvrdni okvir označi, NVDA će uključiti dodatne znakove i simbole tijekom čitanja.
Ovi rječnici sadrže opise simbola (uglavnom Emojia) koje je dostavio [Unicode Consortium](https://www.unicode.org/consortium/) kao dio njihovog [repozitorija općih jezičnih podataka](http://cldr.unicode.org/).
Ako želite da NVDA izgovara opise emoji znakova uz pomoć ovih podataka, uključite ovu opciju.
Međutim, ako vaša govorna jedinica već sama po sebi izgovara opise emoji znakova, možete isključiti ovu opciju.

Imajte na umu, da se ručno dodani ili uređeni opisi znakova spremaju u vašu korisničku mapu.
Dakle, ako promijenite opis određenog emojia, izgovorit će se vaš opis, neovisno o tome je li ova opcija uključena.
Možete dodati, ukloniti ili urediti opise simbola u dijaloškom okviru [Izgovaranje interpunkcije i simbola](#SymbolPronunciation).

Kako biste odasvud mogli uključiti ili isključiti korištenje Unicode podataka, dodijelite prilagođeni prečac ili gestu u dijaloškom okviru [Ulazne geste](#InputGestures).

##### Postotak promjene visine glasa za velika slova {#SpeechSettingsCapPitchChange}

Ovo polje za uređivanje omogućuje promjenu vrijednosti visine koju će govorna jedinica koristiti pri izgovoru velikih slova.
Ova je vrijednost oblikovana kao postotak, u kojem negativna vrijednost snizuje visinu dok ju pozitivna vrijednost bez predznaka minus povisuje.
Kad ne želite promjenu visine koristite 0 kao vrijednost.
Uobičajeno, NVDA malo povisuje visinu glasa za svako veliko slovo, ali neke govorne jedinice to možda ne podržavaju na dobar način.
U slučaju da promjena visine glasa nije podržana, umjesto toga možete koristiti opcije [Izgovori "veliko" prije velikih slova](#SpeechSettingsSayCapBefore) ili [Zvučni signal za velika slova](#SpeechSettingsBeepForCaps).

##### Izgovori "veliko" prije velikih slova {#SpeechSettingsSayCapBefore}

Kad je ovaj potvrdni okvir označen, omogućuje da NVDA izgovara riječ "veliko", prije svakog velikog slova na primjer kad se tekst slovka.

##### Zvučni signal za velika slova {#SpeechSettingsBeepForCaps}

Ako je ovaj potvrdni okvir označen, NVDA će se javiti zvučnim signalom, svaki put kad naiđe na veliko slovo.

##### Koristi funkcionalnost slovkanja, ako je podržano {#SpeechSettingsUseSpelling}

Neke se riječi sastoje od samo jednog znaka, ali je izgovor različit ovisno o tome je li se znak izgovara kao jedan znak (kao kad se slovka) ili kao riječ.
Na primjer, u engleskom jeziku, "a" predstavlja i slovo i riječ, ali se izgovara drugačije ovisno o slučaju.
Ova opcija omogućuje govornoj jedinici razlikovati ta dva slučaja, ako govorna jedinica to podržava.
Većina govornih jedinica to podržava.

Ova opcija bi općenito trebala biti aktivirana.
Međutim, u nekim Microsoft Speech API govornim jedinicama ova se opcija ne primijenjuje pravilno i one se ponašaju čudno kad je ova opcija aktivirana.
Ako imate problem s izgovorom pojedinačnih znakova, pokušajte s deaktiviranom opcijom.

##### Opis znakova koji kasni prilikom pomicanja kursora {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |omogućeno, onemogućeno|
|podrazumjevano |onemogućeno|

Kada je ova postavka odabrana, NVDA će izgovoriti opis znaka prilikom pomicanja znak po znak.

na primjer, prilikom čitanja redka znak po znak, kada se izgovori slovo "b" će izgovoriti "Biokovo" poslije zadrške od jedne sekunde.
Ovo može biti korisno ako je teško razaznati razliku između izgovorenih znakova ili isto može biti korisno korisnicima s oštećenjima sluha.

Opis znakova koji kasni biti će obustavljen ako je drugi tekst izgovoren u tom vremenskom intervalu, ili ako pritisnete tipku `ctrl`.

##### Dostupni modusi prilikom prebacivanja modusa govora {#SpeechModesDisabling}

Ovaj popis sa potvrdnim okvirima omogućuje odabir [modusa govora](#SpeechModes) između kojih se možete prebacivati koristeći prečac `NVDA+s`.
Modusi koji nisu označeni su izuzeti.
Podrazumjevano, svi su modusi uključeni.

Na primjer ako ne trebate koristiti  "zvučne signale" i "isključeno" maknite potvrdne okvire s tih dviju opcija, i ostavite opcije "govor" i "na zahtjev" uključene.
Imajte na umu da je potrebno odabrati najmanje dva modusa.

#### Odaberi govornu jedinicu {#SelectSynthesizer}

<!-- KC:setting -->

##### Otvara postavke govorne jedinice {#toc144}

Prečac: `NVDA+kontrol+s`

Dijaloški okvir Govorna jedinica, koji se otvara na pritiskom gumba "Promijeni …" u kategoriji za govor u dijaloškom okviru NVDA Postavke, omogućuje promjenu govorne jedinice koju će NVDA koristiti.
Kad odaberete govornu jedinicu, pritisnite gumb U redu i NVDA će učitati odabranu govornu jedinicu.
Ako postoji greška pri učitavanju govorne jedinice, NVDA će prikazati poruku, a govorna jedinica se neće promijeniti.

##### Govorna jedinica {#SelectSynthesizerSynthesizer}

Ovaj odabirni okvir omogućuje izbor govorne jedinice koju će NVDA koristiti za generiranje govora.

Za prikaz popisa govornih jedinica koje NVDA podržava, pogledajte poglavlje [Podržane govorne jedinice](#SupportedSpeechSynths).

Jedna specijalna stavka koja će se pojaviti u ovom popisu je "Bez govora", koja omogućuje korištenje NVDA čitača apsolutno bez govora.
To može biti korisno za nekoga tko koristi NVDA s brajičnim retkom ili za razvojne programere koji žele koristiti preglednik govora.

#### Kružne postavke govorne jedinice {#SynthSettingsRing}

Ako želite promijeniti postavke odasvud bez ulaženja u kategoriju govor u NVDA postavkama, postoji nekoliko NVDA tipkovničkih prečaca koji to omogućuju:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Opis|
|---|---|---|---|
|Premjesti se na sljedeću postavku govorne jedinice |NVDA+kontrol+desnaStrelica |NVDA+šift+kontrol+desnaStrelica |Premješta se na sljedeću postavku govora poslije trenutačne, prebacujući se natrag na prvu postavku poslije posljednje|
|Premjesti se na prethodnu postavku govorne jedinice |NVDA+kontrol+strelicaLijevo |NVDA+šift+kontrol+strelicaLijevo |Premješta se na sljedeću dostupnu postavku govora prije trenutačne, prebacujući se na posljednju postavku prije prve|
|Povećaj vrijednost postavke govorne jedinice |NVDA+kontrol+strelicaGore |NVDA+šift+kontrol+strelicaGore |Povećava vrijednost postavke govora na kojoj se nalazite. Npr. povećava brzinu, izabire sljedeći glas, povećava glasnoću|
|Povećaj postavku govorne jedinice u većim koracima |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Povećava vrijednost trenutne postavke govorne jedinice na kojoj se nalazite u većim koracima. Na primjer, kada se nalazite na postavci glasa, prebacivat će se po dvadeset glasova; kada se nalazite na postavkama klizača (brzina, visina, itd) vrijednost će se povečavati do 20 posto|
|Smanji vrijednost postavke govorne jedinice |NVDA+kontrol+strelicaDolje |NVDA+šift+kontrol+strelicaDolje |Smanjuje vrijednost trenutačne postavke glasa na kojoj se nalazite. Npr. smanjuje brzinu, odabire prethodni glas, smanjuje glasnoću|
|Smanji vrijednost trenutne postavke u većim koracima |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |smanjuje vrijednost trenutne postavke govorne jedinice na kojoj se nalazite u većim koracima. Na primjer, kada se nalazite na postavci glasa, vraćat ćete se u nazad za dvadeset glasova; Kada se nalazite na postavci klizača, vraćat ćete se u nazad za dvadeset posto|

<!-- KC:endInclude -->

#### Brajica {#BrailleSettings}

Kategorija Brajica, u dijaloškom okviru NVDA Postavke, omogućuje promjenu nekih parametara brajičnog ulaza i izlaza.
Ova kategorija sadrži sljedeće opcije:

##### Promijeni brajični redak {#BrailleSettingsChange}

Gumb "Promijeni …" u kategoriji Brajica, u dijaloškom okviru NVDA Postavke, aktivira dijaloški okvir [Odaberi brajični redak](#SelectBrailleDisplay) u kojem je moguće odabrati brajični redak koji će se koristiti.
Ovaj se dijaloški okvir otvara ispred dijaloškog okvira NVDA Postavke.
Spremanjem ili nepreuzimanjem postavki, vraćate se u dijaloški okvir NVDA Postavke.

##### Izlazna tablica {#BrailleSettingsOutputTable}

Sljedeća opcija na koju ćete ovdje naići je odabirni okvir izlazne brajične tablice.
U ovom odabirnom okviru ćete naći različite brajične tablice za različite jezike, brajične standarde i-ili puno pismo i kratkopis.
Odabrana brajična tablica će korištena za prikaz teksta koji se prikazuje na brajičnom retku.
Između brajičnih tablica se možete pomicati pomoću tipki strelica.

##### Ulazna tablica {#BrailleSettingsInputTable}

Uz prethodnu opciju, pronači ćete odabirni okvir ulaznu brajičnu tablicu.
Ova će se brajična tablica koristiti pri unosu znakova s brajične tipkovnice vašeg brajičnog retka.
Između brajičnih tablica se možete pomicati pomoću tipki strelica.

Imajte na umu da je ova opcija korisna samo u slučaju kad vaš brajični redak ima brajičnu tipkovnicu i ako upravljački program brajičnog retka podržava unos tu funkciju.
Ako unos s brajičnog retka koji ima brajičnu tipkovnicu nije podržan, to će biti navedeno u poglavlju [Podržani brajični redci](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Modus brajice {#BrailleMode}

Prečac: `NVDA+alt+t`

Ova vam opcija omogućuje izbor dostupnih modusa brajice.

Trenutno su dostupna dva modusa brajice: "prećenje kursora" i "prikaz govora".

Kada je označeno praćenje kursora, brajični redak će pratiti kursor sustava ili navigator objekta ovisno o tome na koji od njih je brajica povezana.

Kada je prikaz govora odabran, Brajični redak će pokazati što NVDA govori, ili što će izgovoriti ako je modus govora postavljen na"govor"

##### Proširi na kompjutorsku brajicu za riječ na položaju kursora {#BrailleSettingsExpandToComputerBraille}

Ova opcija omogućuje prikaz riječi pod kursorom koristeći kompjutorsku brajicu.

##### Prikaži kursor {#BrailleSettingsShowCursor}

Ova opcija omogućuje aktiviranje i deaktiviranje brajičnog kursora.
Ovo se primjenjuje na kursor sustava i na pregledni kursor, ali ne i na indikatora odabira.

##### Titranje kursora {#BrailleSettingsBlinkCursor}

Ova opcija omogućuje titranje brajičnog kursora.
Ako je titranje isključeno, brajični redak će konstantno biti u tzv. "gornjoj" poziciji.
Ova opcija ne utječe na indikatora odabira, to su uvijek točkice 7 i 8 bez titranja.

##### Brzina titranja kursora (ms) {#BrailleSettingsBlinkRate}

Ova opcija je brojčano polje koja omogućuje promjenu brzine titranja kursora u milisekundama.

##### Oblik kursora za fokus {#BrailleSettingsCursorShapeForFocus}

Ova opcija omogućuje biranje oblika (kombinacije točkica) brajičnog kursora kad je brajični redak povezan na fokus.
Ova opcija ne utječe na indikatora odabira, to su uvijek točkice 7 i 8 bez titranja.

##### Oblik kursora za pregled {#BrailleSettingsCursorShapeForReview}

Ova opcija omogućuje biranje oblika (kombinacije točkica) brajičnog kursora, kad je brajični redak povezan na pregled.
Ova opcija ne utječe na indikator odabira, to su uvijek točkice 7 i 8 bez titranja.

##### Prikazuj poruke {#BrailleSettingsShowMessages}

Ovo je odabirni okvir koji vam omogućuje odabir toga kako će se prikazivati poruke na brajičnom retku te kada te poruke trebaju nestati.

Da biste uključili ili isključili prikazivanje poruka s bilo kojeg mjesta, molimo stvorite prilagođen prečac uz pomoć [dijaloškog okvira ulaznih gesti](#InputGestures).

##### Trajanje poruke (u sekundama) {#BrailleSettingsMessageTimeout}

Ova opcija je numeričko polje, kojim se određuje trajanje prikazivanja NVDA poruka na brajičnom retku.
Poruka odmah nestaje prilikom pritiska routing tipke na brajičnom retku, ali se ponovno pojavljuje prilikom pritiska tipke koja ju okida.
Ova se poruka prikazuje samo ako je  opcija "prikazuj poruke" podešena da "koristi stanku".

<!-- KC:setting -->

##### Poveži brajični redak {#BrailleTether}

Prečac: NVDA+kontrol+t

Ova opcija kontrolira hoće li brajični redak pratiti fokus sustava / kursor, objekt navigatora / pregledni kursor, ili oboje.
Kad je opcija "automatski" označena, NVDA će standardno pratiti fokus sustava i kursor.
U tom slučaju, kad se pozicija navigacijskog objekta i-ili preglednog kursora promijeni korisničkom interakcijom, NVDA će se privremeno povezati na pregled, sve dok se ne promijeni fokus ili pregled.
Ako želite praćenje samo fokusa i kursora, morate konfigurirati brajicu povezanu na fokus.
U tom slučaju, NVDA neće pratiti pregledni kursor tijekom objektne navigacije ili pregledni kursor tokom pregleda sadržaja.
Ako želite da NVDA prati pregled objekta i kursor pregleda umjesto toga, Morate postaviti brajicu povezanu na pregled.
U tom slučaju, brajica neće pratiti kursor sustava i fokus.

##### Pomeranje sistemskog kursora kada se prebacuje pregledni kursor {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |podrazumjevano (nikad), nikad, samo kad je povezano na automatski, uvijek|
|Podrazumjevano |nikad|

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

##### Čitaj po odlomku {#BrailleSettingsReadByParagraph}

Ako je ova opcija aktivirana, tekst na brajičnom retku bit će prikazan odlomak po odlomak umjesto redak po redak.
Također, naredbe za sljedeći i prethodni redak će također pomicati po odlomcima.
To znači da ne morate svaki put klizati po brajičnom retku na kraju svakog retka, čak i kad bi više teksta stalo na brajični redak.
Ova opcija može omogućiti tečnije čitanje veće količine teksta.
Ova je opcija standardno deaktivirana.

##### Izbjegni rastavljanje riječi kad je to moguće {#BrailleSettingsWordWrap}

Ako je ova opcija aktivirana, riječ koja je predugačka da bi stala na brajični redak, se neće rastavljati.
Umjesto toga, do kraja brajičnog retka će ostati prazno mjesto na kojem se znakovi neće prikazivati.
Kad kližete po brajičnom retku, moći ćete pročitati cijelu riječ.
Ova opcija se ponekad zove prelamanje riječi.
Imajte na umu da ako cijela riječ sama po sebi ne može stati na brajični redak, riječ se mora rastaviti.

Ako je ova opcija deaktivirana, bit će prikazan onaj dio riječi koji stane na brajični redak, ali će ostatak biti odrezan.
Kad kližete po brajičnom retku, moći ćete pročitati ostatak riječi.

Aktiviranjem ove opcije ćete tekst moći tečnije čitati, ali ćete morati i više klizati po brajičnom retku.

##### Predstavljanje konteksta fokusa {#BrailleSettingsFocusContextPresentation}

Ova opcija omogućuje podešavanje koju kontekstnu informaciju će NVDA prikazati na brajičnom retku kad je objekt fokusiran.
Kontekstna informacija se nadovezuje na hijerarhiju objekta koji je fokusiran.
Na primjer, kad se fokusirate na stavku popisa, ova stavka popisa je dio popisa.
Ovaj popis može biti sadržaj dijaloškog okvira, itd.
Pročitajte poglavlje [Kretanje po objektima](#ObjectNavigation) za više informacija o hijerarhiji koja se primijenjuje na objekte u NVDA čitaču.

Kad je postavljen da popunjava brajični redak s promjenama konteksta, NVDA će pokušati prikazati što više relevantnih informacija, ali samo za dijelove konteksta koji se promijenio.
Koristeći gornji primjer, to znači, kad se promijeni fokus na popis, NVDA će prikazati popis na brajičnom retku.
Čak štoviše, ako je preostalo dovoljno mjesta na retku, NVDA će pokušati prikazati da je stavka popisa dio popisa.
Ako se tada pomičete po popisu pomoću strelica, podrazumijeva se, da ste svjesni činjenice da se nalazite u popisu.
Stoga, za preostale stavke popisa na koje ste se fokusirali, NVDA će prikazati samo fokusiranu stavku popisa na retku.
Da biste ponovo pročitali kontekst, (npr. da se nalazite u popisu i da je taj popis dio dijaloškog okvira), morat ćete klizati po brajičnom retku natrag.

Kad je ova opcija postavljena da se redak uvijek popunjuje, NVDA će prikazati što više kontekstnih informacija, neovisno od toga, jeste li vidjeli te informacije prije.
Prednost ove opcije je ta, da će NVDA će prikazivati onoliko informacija koliko stane na redak.
Međutim, loša je strana, da uvijek postoji razlika u poziciji početka fokusa na retku.
To može otežati brzo pregledavanje dugog popisa stavki, na primjer, jer ćete morati stalno pomicati prst kako biste pronašli početak stavke.
To je bila standardna opcija u NVDA 2017.2 i starijim verzijama.

Ako se postavi opcija za prikaz konteksta fokusa, tako da se kontekst prikazuje samo prilikom klizanja natrag, NVDA nikad neće standardno prikazati kontekstnu informaciju.
Dakle, u gornjem primjeru, NVDA će prikazati da ste fokusirali stavku popisa.
Međutim, da biste pročitali kontekst, (npr. da se nalazite u popisu i da je taj popis dio dijaloškog okvira), morat ćete klizati po brajičnom retku natrag.

Kako biste mijenjali prikaz konteksta fokusa s bilo kojeg mjesta, dodijelite prilagođeni prečac pomoću dijaloškog okvira [Ulazne geste](#InputGestures).

##### Prekini govor prilikom pomicanja teksta na brajičnom redku {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |podrazumjevano (omogućeno), omogućeno, onemogućeno|
|Podrazumjevano |omogućeno|

Ova opcija regulira treba li govor biti prekinut prilikom prilikom pomicanja brajičnog redka za redak u naprijed ili u nazad.
Prečaci za pomicanje na prethodni redak ili sljedeći redak uvijek prekidaju govor.

Prilikom čitanja brajice, dolazni govor može odvlaćiti pažnju korisnika.
Iz tog razloga opcija je uključena podrazumjevano, tako da će govor biti svaki puta prekinut kada se pomakne brajični redak za jedan redak.

Kada se onemogući ova opcija moći ćete istovremeno čuti govor i čitati brajicu.

##### Pokaži označeno {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |podrazumjevano (omogućeno), omogućeno, onemogućeno|
|podrazumjevano |omogućeno|

Ova postavka određuje da li će se pokazivač označenog (točkice 7 i 8) prikazivati na brajičnom redku.
Opcija je podrazumijevano omogućena, pa će se pokazivač izbora prikazivati.
Pokazivač označenog može ometati u toku čitanja.
Isključivanje ove opcije može poboljšati iskustvo pri čitanju.

Da biste uključili ili isključili prikazivanje označenog bilo gde da se nalazite, molimo podesite prilagođenu prečicu korišćenjem [dijaloga ulaznih komandi](#InputGestures).

#### Odaberi brajični redak {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Otvara dijaloški okvir odabira brajičnog redka {#toc168}

Prečac: `NVDA+kontrol+a`

Dijaloški okvir Odaberi brajični redak, koji se može otvoriti koristeći gumb "Promijeni …" u kategoriji Brajica u dijaloškom okviru NVDA Postavke, omogućuje odabir brajičnog retka koji će se koristiti.
Kad odaberete vaš omiljeni brajični redak, možete pritisnuti gumb U redu i NVDA će učitati vaš brajični redak.
Ako postoji greška pri učitavanju brajičnog retka, NVDA će vas obavijestiti porukom, te će nastaviti koristiti prethodni brajični redak, ako postoji.

##### Brajični redak {#SelectBrailleDisplayDisplay}

Ovaj odabirni okvir sadrži brajične retke instalirane u vašem sustavu.
Krećite se između opcija pomoću strelica.

Opcija "automatski", omogućuje NVDA čitaču tražiti mnoge podržane brajične retke u pozadini.
Kad je ova opcija uključena i kad spojite vaš brajični redak putem USB ili Bluetooth veze, NVDA će automatski uspostaviti vezu s tim brajičnim redkom.

Opcija "Bez brajice" znači da ne koristite brajični redak.

Za više informacija o podržanim brajičnim redcima, te o tome koji od njih podržavaju automatsko otkrivanje brajičnih redaka u pozadini, pogledajte poglavlje [Podržani brajični redci](#SupportedBrailleDisplays).

##### Brajični redci koji će se automatski otkrivati {#SelectBrailleDisplayAutoDetect}

Kada je brajični redak postavljen na "automatski", potvrdni okviri na ovom popisu omogućuju vam uključivanje i iskljuučivanje upravljačkih programa koji će biti uključeni u procesu automatskog otkrivanja.
Ovo vam omogućuje isključivanje brajičnih redaka koje ne koristite uvijek.
Na primjer, ako posjedujete samo brajični redak koji koristi Baumov upravljački program za svoje funkcioniranje, ostavit ćete baum upravlojački program uključen a ostale ćete isključiti.

Podrazumjevano, svi podržani brajični redci su uključeni.
Svaki dodani upravljački programm, na primjer u budućoj verziji NVDA ili u NVDA dodatku biti će podrazumjevano omogućen.

Trebat ćete provjeriti dokumentaciju vašeg brajičnog redka u poglavlju [podržani brajični redci](#SupportedBrailleDisplays) kako biste provjerili podržava li vaš brajični redak automatsko otkrivanje.

##### Priključak {#SelectBrailleDisplayPort}

Ova opcija, ako je dostupna, omogućuje izbor komunikacijskog priključka na kojem je spojen brajični redak kojeg ste izabrali.
To je odabirni okvir, koji sadrži mogućnosti za vaš brajični redak.

NVDA standardno koristi automatsko otkrivanje priključka, što znači, da će veza s brajičnim retkom biti uspostavljena automatski skeniranjem svih dostupnih USB i bluetooth uređaja na vašem računalu.
Međutim, za neke brajične retke, možete odrediti koji se priključak treba koristiti.
Uobičajene opcije su "automatski" (čime NVDA automatski traži uređaje), "USB", "Bluetooth" i zastarjele serijske komunikacijske priključke, ako vaš brajični redak još uvijek podržava tu vrstu povezivanja.

Ova opcija neće biti dostupna ako vaš brajični redak koristi automatsko otkrivanje brajičnih redaka.

Pročitajte dokumentaciju za vaš brajični redak u poglavlju [Podržani brajični redci](#SupportedBrailleDisplays) za više informacija o podržanim načinima spajanja i dostupnim priključcima.

Imajte na umu da ako spojite više brajičnih redaka na jedno računalo u isto vrijeme a ti redci koriste isti upravljački program npr. spajanje dva seika brajična redka,
Trenutno je nemoguće odrediti koji brajični redak NVDA bi trebao koristiti.
Stoga preporuča se spajanje samo jednog brajičnog redka određenog tipa ili proizvođača na vaše računalo u isto vrijeme.

#### Zvuk {#AudioSettings}

<!-- KC:setting -->

##### Otvara postavke zvuka {#toc173}

Prečac: `NVDA+kontrol+u`

Kategorija zvuk u NVDA postavkama omogućuje vam mijenjanje nekih opcija vezanih uz zvuk.

##### Izlazni uređaj {#SelectSynthesizerOutputDevice}

Ovaj odabirni okvir omogućuje odabir zvučnog uređaja kojeg će govorna jedinica koristiti za govor.

<!-- KC:setting -->

##### Modus stišavanja zvuka {#SelectSynthesizerDuckingMode}

Tipkovnički prečac: NVDA+šift+d

Ova opcija omogućuje odabir hoće li NVDA stišati glasnoću drugih aplikacija dok NVDA govori ili će to raditi cijelo vrijeme dok je NVDA pokrenut.

* Bez stišavanja: NVDA nikad neće smanjiti glasnoću drugih zvukova. 
* Stišaj tijekom govora ili sviranja zvukova: NVDA će stišavati zvuk samo kad on govori, a u pozadini se javljaju zvukovi. Ovo možda ne radi u svim govornim jedinicama. 
* Uvijek stišaj: NVDA cijelo vrijeme stišava zvukove drugih aplikacija kad je NVDA pokrenut.

Ova je opcija dostupna, samo ako je NVDA instaliran.
Na prijenosnim i privremenim kopijama NVDA čitača, podrška za stišavanje zvuka nije moguća.

##### Glasnoća zvukova NVDA prati glasnoću govorne jedinice  (zahtijeva WASAPI) {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |onemogućeno, omogućeno|
|Podrazumjevano |onemogućeno|

Kada se ova opcija omogući, jačina govorne jedinice i NVDA zvukova će pratiti podešavanje jačine glasa kojeg koristite.
Ako utišate jačinu glasa kojeg koristite, jačina NVDA zvukova će se takođe utišati.
Slično tome, ako pojačate glas, jačina zvukova će se pojačati.
Ova postavka nije dostupna ako ste pokrenuli  NVDA sa isključenim [WASAPI za audio izlaz](#WASAPI) U naprednim postavkama.

##### Glasnoća NVDA zvukova {#SoundVolume}

Ovaj klizač vam dozvoljava regulaciju glasnoće govorne jedinice i  zvukova.
Ova postavka se primjenjuje samo kada je opcija "Koristi WASAPI za audio izlaz" omogućena i opcija "Jačina NVDA zvukova prati jačinu glasa" onemogućena.
Ova postavka nije dostupna ako ste pokrenuli  NVDA sa isključenim [WASAPI za audio izlaz](#WASAPI) U naprednim postavkama.

##### Vrijeme držanja audiouređaja budnim poslije zadnje izgovorene stavke {#AudioAwakeTime}

U ovom se polju za uređivanje određuje koliko će dugo audiouređaj ostati budan poslije završetka govora.
Ovo omogućuje NVDA izbjegavanje većinu problema sa govorom poput izrezanih riječi.
Ovo se može događati zbog toga što audiouređaji, a posebno oni povezani putem Bluetootha ulaze u način mirovanja.
Ovo može biti od pomoći i u drugim slučajevima poput pokretanja NVDA u u virtualnom okruženju (npr. Citrix Virtual Desktop), ili na nekim prijenosnim računalima.

Manje vrijednosti mogu prouzrokovati češće rezanje zvuka, jer audiouređaj može ulaziti u način mirovanja prečesto, što prouzrokuje češće rezanje početka govora.
Postavljanje ove opcije na višu vrijednost može prouzročiti brže pražnjenje baterije audiouređaja, zbog toga što audiouređaj ostaje duže aktivan kada nema zvuka.

Kako biste onemogućili ovu značajku, postavite vrijeme na nulu.

##### Način podijeljenog zvuka {#SelectSoundSplitMode}

Ova funkcija omogućuje korisnicima korištenje stereouređaja poput zvučnika ili slušalica.
Ova funkcija omogućuje da zvuk govora NVDA bude na primjer u lijevom kanalu, a drugi zvukove na primjer u desnom.
Podrazumjevano način podjeljenog zvuka je onemogućen, što znači da će svi programi, uključujući i NVDA reproducirati zvukove u oba audiokanala.
Tipkovničkim prečacem možete se prebacivati između različitih načina podjele zvuka:
<!-- KC:beginInclude -->

| naziv |prečac |opis|
|---|---|---|
|prebacuj se između načina podjele zvuka |`NVDA+alt+s` |Cycles between sound split modes.|

<!-- KC:endInclude -->

Podrazumijevano, ovaj će prečac prebacivati između slijedećih modusa:

* Onemogućena podjela zvuka: Programi i NVDA reproduciraju svoje zvukove u oba kanala.
* NVDA u lijevom kanalu, a programi u desnom: NVDA će govoriti u lijevom kanalu, dok će drugi programi reproducirati svoje zvukove u desnom.
* NVDA u desnom kanalu, a programi u lijevom: NVDA će govoriti u desnom kanalu, dok će zvukovi drugih programa biti reproducirani u lijevom.

Dostupno je više naprednih načina podjele u oabirnom okviru.
Ako želite postaviti glasnoću za druge programe koji nisu NVDA, koristite [za to predviđene prečace](#OtherAppVolume).
Imajte na umu da ova opcija ne radi kao mikser.
Na primjer, ako program reproducira  glazbu u stereo formatu kada je način podjele zvuka postavljen na "NVDA u lijevom kanalu a programi u desnom", tada ćete čuti desni kanal pjesme, dok će lijevi kanal biti utišan.

Ova opcija nije dostupna ako ste pokrenuli NVDA sa [isključenim Wasapi za izlaz zvuka](#WASAPI) in Advanced Settings.

Imajte na umu da ako se NVDA sruši, glasnoća zvuka programa neće se vratiti na zadane vrijednosti, i ti programi će i dalje reproducirati zvuk samo u jednom kanalu.
Kako biste to spriječili, molimo ponovno pokrenite NVDA.

##### Prilagođavanje načina podjele zvuka {#CustomizeSoundSplitModes}

Ovaj popis sa odabirnim okvirima omogućuje vam prilagođavanje koji će načini podjele zvuka biti dostupni pri prebacivanju uz pomoć prečaca `NVDA+alt+s`.
Načini koji nisu odabrani nedostupni na tom popisu.
Podrazumjevano su dostupna tri modusa.

* Modus podjele zvuka isključen: NVDA i drugi programi reproduraju zvuk u oba kanala.
* NVDA u lijevom kanalu i ostali programi u desnom.
* NVDA u desnom kanalu i sve ostali programi u lijevom.

Imajte na umu da je potrebno odabrati barem jedan modus.
Ova opcija nije dostupna ako je NVDA pokrenut [sa isključenim Wasapi za audioizlaz](#WASAPI) u naprednim postavkama.

##### Glasnoća drugih programa {#OtherAppVolume}

Ovaj vam klizač omogućuje promjenu glasnoće drugih programam koji nisu NVDA.
Ova će promjena glasnoće biti primijenjena čak i kada se taj program tek pokrene.
Ova postavka glasnoće može se mijenjati i uz pomoć sljedećih tipkovničkih prečaca sa bilo kojeg mjesta:

<!-- KC:beginInclude -->

| naziv |prečac |opis|
|---|---|---|
|povećaj glasnoću drugih programa |`NVDA+alt+pageUp` |Povećava glasnoću svih programa osim NVDA.|
|Smanji glasnoću programa |`NVDA+alt+pageDown` |smanjuje glasnoću svih programa osim NVDA.|

<!-- KC:endInclude -->

Ova opcija nije dostupna ako ste pokrenuli NVDA sa [isključenim Wasapi za audioizlaz](#WASAPI) u naprednim postavkama.

##### Utišaj druge programe {#MuteApplications}

Ovaj vam potvrdni okvir omogućuje utišavanje svih drugih programa koji nisu NVDA.
Ova će se postavka utišavanja primijeniti čak i kada se neki drugi program tek pokrene.
Sljedeći tipkovnički prečac se može također koristiti s bilo kojeg mjesta:

<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Uključi ili isključi utišavanje drugih programa |`NVDA+alt+delete` |Utišava ili odtišava sve druge programe osim NVDA.|

<!-- KC:endInclude -->

Ova opcija nije dostupna ako ste pokrenuli NVDA sa [isključenim Wasapi za audioizlaz](#WASAPI) u naprednim postavkama.

#### Vid {#VisionSettings}

Kategorija "Vid" u dijaloškom okviru NVDA Postavke omogućuje aktiviranje, deaktiviranje i konfiguriranje [vizualnih pomagala](#Vision).

Imajte na umu da se opcije u ovoj kategoriji mogu proširiti pomoću [NVDA dodataka](#AddonsManager).
Ova kategorija standardno sadrži sljedeće opcije:

##### Vizualno praćenje {#VisionSettingsFocusHighlight}

Potvrdni okviri u grupi kontrola za vizualno praćenje reguliraju ponašanje ugrađene mogućnosti [Vizualno praćenje](#VisionFocusHighlight).

* Aktiviraj isticanje: uključuje i isključuje vizualno praćenje.
* Istakni fokus sustava: uključuje i isključuje isticanje [fokusa sustava](#SystemFocus).
* Istakni navigacijski objekt: uključuje i isključuje isticanje [navigacijskog objekta](#ObjectNavigation).
* Istakni kursor modusa čitanja: uključuje i isključuje isticanje [virtualnog kursora modusa čitanja](#BrowseMode).

Imajte na umu da ćete označavanjem ili odznačavanjem potvrdnog okvira "Aktiviraj isticanje" usporedno promijeniti stanje triju ostalih potvrdnih okvira.
Dakle, ako je "Aktiviraj isticanje" isključeno, a vi označite ovaj potvrdni okvir, ostala tri potvrdna okvira će se automatski također označiti.
Ako želite samo istaknuti fokus i ostaviti potvrdne okvire navigacijskog objekta i modusa čitanja neoznačene, stanje potvrdnog okvira "Aktiviraj isticanje" će se označiti polovično.

##### Ekranska zavjesa {#VisionSettingsScreenCurtain}

[Ekransku zavjesu](#VisionScreenCurtain) možete aktivirati tako da označite potvrdni okvir "Zatamni ekran (trenutna radnja)".
Prikazat će se upozorenje, da će se vaš ekran zatamniti.
Prije nego što nastavite (odabirom gumba "Da"), uvjerite se da su govor ili brajični redak uključeni te da ćete moći kontrolirati vaše računalo bez ekrana.
Odaberite "Ne", ako više ne želite koristiti ekransku zavjesu.
Ako ste sigurni, pritisnite gumb Da, kako biste uključili ekransku zavjesu.
Ako ne želite vidjeti ovu poruku svaki put, možete to promijeniti u dijaloškom okviru koji prikazuje ovu poruku.
Upozorenje možete uvijek vratiti. Označite odabirni okvir "Uvijek prikaži upozorenje tijekom učitavanja ekranske zavjese" koji se nalazi pored potvrdnog okvira "Zatamni ekran".

Kada se zaslonska zavjesa uključuje, reproducirat će se zvuk.
Kada želite promjeniti status te opcije, možete maknuti kvačicu sa potvrdnog okvira "reproduciraj zvuk prilikom uključivanja zaslonske zavjese".

##### Postavke za vizualna pomagala treće strane {#VisionSettingsThirdPartyVisualAids}

Dodatne pružatelja vizualnih poboljšanja je moguće pružiti putem [NVDA dodataka](#AddonsManager).
Kad ti pružatelji sadrže prilagodljive postavke, one će se prikazati u ovoj kategoriji postavki u odvojenim grupama.
Podržane postavke za pružatelje potražite u njihovoj dokumentaciji.

#### Tipkovnica {#KeyboardSettings}

<!-- KC:setting -->

##### Otvara postavke tipkovnice {#toc188}

prečac: `NVDA+kontrol+k`

Kategorija Tipkovnica u dijaloškom okviru NVDA Postavke sadrži opcije, s kojima se podešava ponašanje NVDA čitača tijekom upotrebe tipkovnice.
Ova kategorija postavki sadrži sljedeće opcije:

##### Raspored tipkovnice {#KeyboardSettingsLayout}

Ova opcija omogućuje odabir rasporeda tipkovnice kojeg će NVDA koristiti. Trenutačno NVDA sadrži raspored tipkovnice za stolna i za prijenosna računala.

##### Odaberi NVDA modifikacijske tipke {#KeyboardSettingsModifiers}

Ovi potvrdni okviri u ovom popisu određuju tipke koje će se koristiti kao [NVDA modifikacijska tipka](#TheNVDAModifierKey). Dostupne su sljedeće tipke:

* Tipka za velika slova (caps lock)
* Numerička tipka insert
* Proširena tipka insert (obično se nalazi iznad strelica, blizu tipki houm i end)

Ako niti jedna tipka nije podešena kao modifikacijska tipka, može biti nemoguće pristupiti većini NVDA prečacima, stoga, trebate označiti jedan od odabirnih okvira.

<!-- KC:setting -->

##### Izgovori utipkane znakove {#KeyboardSettingsSpeakTypedCharacters}

Prečac: NVDA+2

Kad je aktivirano, NVDA će izgovoriti sve znakove koje tipkate na tipkovnici.

<!-- KC:setting -->

##### Izgovori utipkane riječi {#KeyboardSettingsSpeakTypedWords}

Prečac: NVDA+3

Kad je aktivirano, NVDA će izgovoriti sve riječi koje tipkate na tipkovnici.

##### Prekid govora za utipkane znakove {#KeyboardSettingsSpeechInteruptForCharacters}

Ako je uključena, ova će opcija prekinuti govor svaki put kad se upiše neki znak. Ovo je standardno uključeno.

##### Prekid govora za tipku enter {#KeyboardSettingsSpeechInteruptForEnter}

Ako je uključena, ova će opcija prekinuti govor svaki put kad se pritisne tipka enter. Ovo je standardno uključeno.

##### Dopusti brzo čitanje u "Izgovori sve" {#KeyboardSettingsSkimReading}

Ako je ova opcija uključena, određeni prečaci za kretanje (kao što je brzo kretanje u modusu čitanja ili premještanje po redcima ili odlomcima) ne zaustavljaju naredbu "Izgovori sve", već se naredba "Izgovori sve" prebacuje na novu poziciju i nastavlja se sa čitanjem.

##### Zvučni signal za tipkanje malih slova, kad je caps lock uključen {#KeyboardSettingsBeepLowercase}

Kad je ova opcija aktivirana, čut će se zvučni signal upozorenja kad se utipka znak koristeći pri tome tipku šift, dok je caps lock uključen.
Pisanje malih slova s pritisnutom tipkom šift je općenito nenamjerna greška u neznanju da je caps lock uključen.
Stoga može biti korisno o tome biti obaviješten zvučnim signalom.

<!-- KC:setting -->

##### Izgovori naredbene tipke {#KeyboardSettingsSpeakCommandKeys}

Prečac: NVDA+4

Kad je ova opcija aktivirana, NVDA će izgovarati sve tipke koje nisu znakovi, a koje pritišćete na tipkovnici. To uključuje kombinacije tipki poput kontrol+neko drugo slovo.

##### Sviraj zvuk za pravopisne greške tijekom tipkanja {#KeyboardSettingsAlertForSpellingErrors}

Kad je ova opcija aktivirana, čuje se kratki zvuk kad utipkana riječ sadrži pravopisnu grešku.
Ova je opcija dostupna samo ako je izvještavanje o pravopisnim pogrreškama aktivirano u [Postavkama oblikovanja dokumenta](#DocumentFormattingSettings), u dijaloškom okviru NVDA Postavke.

##### Rukovanje tipkama iz drugih aplikacija {#KeyboardSettingsHandleKeys}

Ova opcija omogućuje korisniku kontrolu nad time, hoće li ili neće NVDA obraditi kombinacije tipaka koje su namijenjene nekoj drugoj aplikaciji, poput ekranskih tipkovnica i softvera za prepoznavanje govora. 
Ova je opcija standardno aktivirana, ali neki korisnici bi to htjeli isključiti, npr. korisnici koji upisuju vijetnamski pomoću UniKey programa za tipkanje, jer će to prouzrokovati pogrešan unos znakova.

#### Miš {#MouseSettings}

<!-- KC:setting -->

##### Otvara postavke miša {#toc201}

Prečac: `NVDA+kontrol+m`

Kategorija Miš u dijaloškom okviru NVDA Postavke, omogućuje praćenje miša, reproduciranje zvučnih koordinata te postavljanje drugih opcija.
Ova kategorija sadrži sljedeće opcije:

##### Izvijesti o promjenama oblika miša {#MouseSettingsShape}

Kad se ovaj potvrdni okvir odabere, NVDA izgovara promjene oblika pokazivača miša.
Pokazivač miša u Windowsu mijenja oblik, kako bi prenio određene informacije, npr: kad je nešto moguće urediti ili kad se nešto pokreće itd.

<!-- KC:setting -->

##### Aktiviraj praćenje miša {#MouseSettingsTracking}

Prečac: NVDA+m

Kad je ova opcija aktivirana, NVDA će izvijestiti o tekstu koji se trenutačno nalazi ispod pokazivača miša, dok pomičete miša po ekranu. Ovo omogućuje pronalaženje elemenata na ekranu pomoću miša, umjesto pomoću kretanja po objektima.

##### Razlučivost tekstualne jedinice {#MouseSettingsTextUnit}

Ako je NVDA postavljen da izgovara tekst ispod miša dok pomičete miša po ekranu, ova opcija omogućuje podešavanje količine teksta koja će se izgovarati.
Možete birati između znaka, retka, riječi i odlomka.

Za mijenjanje razlučivost tekstualne jedinice s bilo kojeg mjesta, dodijelite prilagođeni prečac u dijaloškom okviru [Ulazne geste](#InputGestures).

##### Čitaj objekt pod mišem {#MouseSettingsRole}

Kada je ovaj potvrdni okvir odabran, NVDA će čitati informacije o objektima kada se miš kreće unutar njih.
Ovo uključuje vrstu (tip) objekta kao  i stanja (odabrano/pritisnuto), koordinate ćelija u tablicama, itd.
Imajte na umu da neke postavke određenih detalja o objektu mogu ovisiti od drugih postavki, poput [prezentacije objekata](#ObjectPresentationSettings) ili [oblikovanja dokumenta](#DocumentFormattingSettings).

##### Sviraj zvučne koordinate kad se miš miče {#MouseSettingsAudio}

Kad se ovaj potvrdni okvir odabere, NVDA reproducira zvučni signal kako se miš pomiče, tako da korisnik može shvatiti gdje se miš nalazi u odnosu na poziciju na ekranu.
Što je pozicija miša na ekranu viša, visina zvučnih signala je veća.
Ako se miš na ekranu nalazi više lijevo ili desno, zvuk će biti reproduciran više lijevo ili desno (ako uzmemo u obzir da korisnik ima stereo zvučnike ili slušalice).

##### Svjetlost kontrolira glasnoću zvučnih koordinata {#MouseSettingsBrightness}

Ako je potvrdni okvir "Sviraj zvučne koordinate kad se miš miče" označen, glasnoća zvučnih signala za koordinate će ovisiti o svjetloći ekrana pod mišem.
Ovaj potvrdni okvir standardno nije označen.

##### Ignoriraj unos miša iz drugih aplikacija {#MouseSettingsHandleMouseControl}

Ova opcija omogućuje korisniku ignoriranje događaja miša (uključujući kretnje mišem i gumbe) koji su generirale druge aplikacije poput Teamviewera i drugih softvera za udaljenu kontrolu računala.
Ova je opcija standardno deaktivirana.
Ako označite ovu opciju i pri tom imate aktiviranu opciju "Aktiviraj praćenje miša", NVDA neće izgovarati što je pod pokazivačem miša, ako druga aplikacija pomiće miša.

#### Interakcija dodirom {#TouchInteraction}

Ova kategorija postavki, koja je dostupna samo na računalima s dodirnicima, omogućuje podešavanje načina interakcije NVDA čitača s ekranima osjetljivim na dodir.
Ova kategorija sadrži sljedeće opcije:

##### Uključi podršku ekrana osjetljivih na dodir {#TouchSupportEnable}

Ovaj potvrdni okvir uključuje podršku ekrana osjetljivih na dodir.
Ako je uključen, možete koristiti vaše prste za interakciju sa ekranom i elementima na njemu koristeći uređaj koji podržava zaslon osjetljiv na dodir.
Ako je isključen, podrška zaslona osjetljivih na dodir bit će isključena kao da NVDA nije niti pokrenut.
Ova postavka može biti regulirana koristeći NVDA+control+alt+t. 

##### Modus tipkanja dodirom {#TouchTypingMode}

Ovaj odabirni okvir omogućuje odrediti modus tipkanja kad se koristi dodirna tipkovnica.
Ako je ovaj potvrdni okvir označen, kad nađete tipku na dodirnoj tipkovnici, dignite prst i tipka će se pritisnuti.
Ako nije označen, morate dva puta dodirnuti tipku na dodirnoj tipkovnici, da bi se tipka pritisnula.

#### Pregledni kursor {#ReviewCursorSettings}

Kategorija Pregledni kursor u dijaloškom okviru NVDA Postavke se koristi za podešavanje ponašanja preglednog kursora NVDA čitača.
Ova kategorija sadrži sljedeće opcije:

<!-- KC:setting -->

##### Prati fokus sustava {#ReviewCursorFollowFocus}

Prečac: NVDA+7

Kad je ova opcija aktivirana, pregledni kursor će biti smješten na mjesto trenutačnog fokusa sustava pri svakoj promjeni fokusa.

<!-- KC:setting -->

##### Prati kursor sustava {#ReviewCursorFollowCaret}

Prečac: NVDA+6

Kad je ova opcija aktivirana, pregledni kursor će automatski biti premješten na poziciju kursora sustava pri svakom pomicanju.

##### Prati kursor miša {#ReviewCursorFollowMouse}

Kad je ova opcija aktivirana, pregledni kursor će pratiti pomicanje miša.

##### Jednostavni modus pregleda {#ReviewCursorSimple}

Kad je ova opcija aktivirana, NVDA će filtrirati hijerarhiju objekata po kojima se možete kretati kako bi se izbacili suvišni objekti koji nisu zanimljivi korisniku; Npr. nevidljivi objekti i objekti koji imaju estetsku svrhu.

Da biste uključili ili isključili jednostavni modus pregleda s bilo kojeg mjesta, dodijelite prilagođeni prečac u dijaloškom okviru [Ulazne geste](#InputGestures).

#### Prezentacija objekata {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Otvara dijaloški okvir prezentacija objekata {#toc218}

Prečac: `NVDA+kontrol+o`

Kategorija Prezentacija objekta u dijaloškom okviru NVDA Postavke se koristi za podešavanje količine informacija kontrola koje će NVDA prikazivati. Te informacije su na primjer opis, informacija o položaju i tako dalje.
Ove se opcije ne primjenjuju na modus čitanja.
Ove se opcije uobičajeno primjenjuju na izgovor fokusa i NVDA objektnu navigaciju, ali ne i na čitanje tekstualnog sadržaja, kao što je to modus čitanja.

##### Izvijesti o alatnim savjetima {#ObjectPresentationReportToolTips}

Kad je ovaj potvrdni okvir označen, NVDA izvještava o alatnim savjetima kad se pojave.
Puno prozora i poruka preko sebe prikazuju malu poruku (ili alatni savjetnik) kad pomaknete pokazivač miša na njih ili ponekad kad pomićete fokus po njima.

##### Čitaj obavijesti {#ObjectPresentationReportNotifications}

Kada je ovaj potvrdni okvir odabran, NVDA će čitati balončiće pomoći i obavijesti akcijskog centra kad se pojave.

* Balončići pomoći su poput alatnih savjetnika, ali su uobičajeno veći, i povezani su sa događajima sustava poput isključenja mrežng kabla, ili obavještenju o sigurnosnim prijetnjama u Windowsima.
* Obavijesti centra obavijesti su uvedene u Windowsima 10 i prikazuju se u akcijskom centru u traci obavijesti, informirajući o sljedećim događajima (npr. preuzeta nadogradnja, prispjeće e-maila u vašoj ulaznoj pošti, itd.).

##### Izvijesti o tipkovnim prečacima za objekte {#ObjectPresentationShortcutKeys}

Kad je ovaj potvrdni okvir označen, NVDA izvještava i o prečacu koji je pridružen određenom objektu ili kontroli kad se o jednom od njih izvještava.
Na primjer, u traci izbornika, stavka Datoteka može imati prečac alt+f.

##### Izvijesti o položaju objekta {#ObjectPresentationPositionInfo}

Ova opcija omogućuje izvještavanje o poziciji objekta (npr. 1 od 4) kad se premještate na objekt pomoću fokusa ili pomoću kretanja po objektima.

##### Pogodi položaj objekta kad je nedostupan {#ObjectPresentationGuessPositionInfo}

Ako je izvještavanje o poziciji objekta uključeno, ova opcija omogućuje NVDA čitaču pogađanje pozicije objekta za određenu kontrolu kad je ista nedostupna.

Kad je ova opcija uključena, NVDA će čitati informacije za više kontrola kao što su izbornici i alatne trake. Međutim, te informacije mogu biti pomalo netočne.

##### Izvijesti o opisu objekta {#ObjectPresentationReportDescriptions}

Odznačite potvrdni okvir, ako ne želite da se pored izvještavanja o objektu, izvještava i o opisu.

<!-- KC:setting -->

##### Rezultat trake napredovanja {#ObjectPresentationProgressBarOutput}

Prečac: NVDA+u

Ova opcija omogućuje podešavanje načina na koji će vas NVDA izvještavati o trakama napretka.

Ovaj odabirni okvir sadrži sljedeće opcije:

* Isključeno: Trake napretka neće biti izgovarane kako se budu mijenjale.
* Govor: ovom se opcijom izgovara traka napretka kao postoci. Svaki put kad se traka napretka promjeni, NVDA će izgovoriti novu vrijednost.
* Zvučni signali: ovom se opcijom svira zvučni signal svaki put kad se traka napretka promjeni. Što je zvučni signal viši, to je traka napretka bliža kraju.
* Zvučni signali i govor: ovom se opcijom istovremeno koriste zvučni signali i govora kad se aktualizira traka napretka.

##### Izvijesti o trakama napredovanja u pozadini {#ObjectPresentationReportBackgroundProgressBars}

Kad je ova opcija odabrana, NVDA će izvještavati o traci napretka kad ona nije u fokusu.
Ako smanjite prozor u kojem se nalazi traka napretka ili se prebacite na jedan drugi prozor, NVDA će pratiti tu traku, a vama će istovremeno omogućiti baviti se drugim stvarima dok NVDA prati traku napretka.

<!-- KC:setting -->

##### Izvijesti o dinamičkim promjenama sadržaja {#ObjectPresentationReportDynamicContent}

Prečac: NVDA+5

Uključuje i isključuje najavu sadržaja u određenim objektima poput terminala i povijesti u programima za čavrljanje.

##### Sviraj zvuk kad se pojave automatski prijedlozi {#ObjectPresentationSuggestionSounds}

Uključuje i isključuje najavu prisutnosti automatskih prijedloga, te ako je uključeno, NVDA će odsvirati zvuk koji će to potvrditi.
Automatski prijedlozi su unosi bazirani na upisanom tekstu u nekim poljima za uređivanje i dokumentima.
Na primjer, kad upišete tekst u polje za uređivanje u izborniku Start u Windows Vista i novijim sustavima, Windows prikazuje popis prijedloga baziranih na tome što ste upisali.
Za neka polja, kao što su to polja za pretragu raznim Windows 10 aplikacijama, NVDA vas može obavijestiti da se pojavio popis prijedloga kad upišete tekst.
Popis automatskih prijedloga će se zatvoriti jednom kad se pomakenete izvan polja za uređivanje, i za neka polja, NVDA vas može o tome obavijestiti kad se to dogodi.

#### Unos sastavljenih znakova {#InputCompositionSettings}

Ova kategorija postavki omogućuje kontrolu izgovora unosa azijskih znakova, koristeći IME ili načine unosa s tekstualnim uslugama.
Imajte na umu da, zbog činjenice da se metode unosa teksta razlikuju po dostupnim značajkama i po tome kako dostavljaju informacije, u većini slučajeva bit će potrebno posebno konfigurirati postavke za svaku metodu unosa da biste dobili najbolje iskustvo pisanja.

##### Automatski izvijesti o svim dostupnim kandidatima {#InputCompositionReportAllCandidates}

Ova opcija, koja je standardno aktivirana, omogućuje hoće li se ili neće automatski izvještavati svi vidljivi kandidati kad se pojavljuje lista kandidata ili je stranica liste promjenjena.
Korisno je imati uključenu ovu opciju za piktografske metode unosa kao što su Kineski Novi ChangJie ili Boshiami, jer možete čuti sve dostupne simbole i tako ih izravno unositi.
Međutim, za fonetske metode unosa, kao što je Kineski Novi fonetski, korisno je isključiti ovu opciju jer će svi simboli zvučati isto i trebat ćete koristiti kursorske tipke da biste se kretali između stavaka popisa pojedinačno da biste dobili više informacija iz opisa znakova za svaki kandidat.

##### Najavi odabranog kandidata {#InputCompositionAnnounceSelectedCandidate}

Ova opcija, koja je standardno aktivirana, omogućuje odabir između toga hoće li ili neće NVDA čitati označeni kandidat kad se krećete po listi ili kad je označavanje promjenjeno.
Za metode unosa kod kojih se označavanje znakova vrši strelicama (kao što je kineski novi fonetski) to je nužno, ali za neke opcije bilo bi najbolje ovu opciju isključiti.
Imajte na umu da, čak iako je ova opcija isključena, pregledni će kursor biti smješten na označenom kandidatu dozvoljavajući korištenje kretanja po objektima, kako biste ručno pročitali ovaj ili neki drugi kandidat.

##### Uvijek uključi kratak opis znakova kad se najavljuju kandidati {#InputCompositionCandidateIncludesShortCharacterDescription}

Ova opcija, koja je standardno uključena, omogućuje podešavanje između toga hoće li ili neće NVDA izgovarati opise znakova za označeni kandidat ili kad je označen ili kad je automatski pročitan s popisa kandidata.
Imajte na umu da se za jezike, kao što je kineski, ovom opcijom ne mijenja najava dodatnih opisa znakova, jer ova opcija ne dotiče odabrane kandidate.
Ova opcija može biti korisna za Korejske i Japanske metode unosa.

##### Izvijesti o promjenama na nizu znakova koji se čita {#InputCompositionReadingStringChanges}

Neke metode unosa, kao što su Kineski novi fonetski ili novi ChangJie, imaju niz znakova (Ponekad naziva i prekompozicijski niz znakova) koji se čita.
Možete odabrati hoće li ili neće NVDA izvještavati o znakovima koji su upisivani u taj niz.
Ova je opcija standardno aktivirana.
Napomena: neke starije metode unosa, kao što su kineski ChangJie, neće koristiti prekompozicijski niz znakova kako bi čuvao prekompozicijske znakove, ali umjesto toga koriste izravno kompozicijski niz. Pogledajte sljedeću opciju za podešavanje čitanja kompozicijskog niza.

##### Izvijesti o promjenama na nizu sastavljenih znakova {#InputCompositionCompositionStringChanges}

Nakon čitanja ili u slučaju kad su kompozicijski podaci spremljeni kao valjan piktografski simbol, većina metoda unosa stavlja taj znak u kompozicijski niz za privremeno spremanje zajedno s drugim sastavljenim simbolima prije nego što se konačno umetnu u dokument.
Ova opcija omogućuje odabir između toga hoće li ili neće NVDA izgovarati nove simbole kako se isti budu pojavljivali u kompozicijskom nizu.
Ova je opcija standardno aktivirana.

#### Modus čitanja {#BrowseModeSettings}

<!-- KC:setting -->

##### Otvara postavke modusa čitanja {#toc236}

Prečac: `NVDA+kontrol+b`

Kategorija Modus čitanja u NVDA postavkama se koristi za podešavanje toga, kako će se NVDA ponašati pri čitanju kompleksnih dokumenata, kao što su na primjer web stranice.
Ova kategorija sadrži sljedeće opcije:

##### Maksimalni broj znakova u jednom retku {#BrowseModeSettingsMaxLength}

Ovo polje služi za postavljanje dužine retka u modusu čitanja (koristeći znakove kao mjernu jedinicu).

##### Broj redaka po stranici {#BrowseModeSettingsPageLines}

Ovo polje postavlja količinu redaka po kojima se možete kretati kad u modusu čitanja pritišćete pejdž ap i pejdž daun.

<!-- KC:setting -->

##### Koristi raspored ekrana {#BrowseModeSettingsScreenLayout}

Prečac: NVDA+v

Ova vam opcija omogućuje da odredite treba li u načinu pregleda smjestiti sadržaj koji se može kliknuti (poveznice, gumbe i polja) u svoje zasebne redke, ili trebaju ostati zajedno s tekstom kao što je to vizualno prikazano. 
Imajte na umu da se ova opcija ne primjenjuje na Microsoft Office aplikacije poput Outlooka ili Worda koji uvijek koriste izgled zaslona.
Kada je izgled zaslona uključen, elementi na stranici će ostati prikazani kako se vizualno prikazuju. 
Na primjer, vizualni redak sa više poveznica biti će prikazan u govoru i brajici kao više poveznica u više redaka. 
Ako je onemogućen, Elementi će biti smješteni u svojim zasebnim redcima, što će biti jednostavnije prilikom kretanja po stranici redak po redak. 
To će učiniti stavke jednostavnima za interakciju za neke korisnike.

##### Aktiviraj modus čitanja nakon učitavanja stranice {#BrowseModeSettingsEnableOnPageLoad}

Ovaj potvrdni okvir regulira hoće li se modus čitanja uključiti prilikom učitavanja stranice.
Kad je ova opcija uključena, modus čitanja može biti uključen ručno na stranicama ili u dokumentima gdje je modus čitanja podržan.
Pogledajte [poglavlje Modus čitanja](#BrowseMode) kako biste pogledali popis podržanih aplikacija u modusu čitanja.
Imajte na umu da se ovo ne primjenjuje u situacijama gdje je modus čitanja uvijek neobavezan, na primjer u Microsoft Wordu.
Ova je opcija standardno aktivirana.

##### Automatski "Izgovori sve" nakon učitavanja stranice {#BrowseModeSettingsAutoSayAll}

Ova opcija uključuje ili isključuje automatsko čitanje web stranice kad se ista učita u modusu čitanja.
Ova je opcija standardno aktivirana.

##### Uključi tablice rasporeda {#BrowseModeSettingsIncludeLayoutTables}

Ova opcija utječe na to kako će NVDA baratati tablicama koje imaju svrhu prikazivanja nekog rasporeda.
Kad je ova opcija uključena, NVDA će tretirati ove tablice kao normalne tablice, čitajući ih onako kako je podešeno u [postavkama oblikovanja dokumenta](#DocumentFormattingSettings) i locirajući iste pomoću tipki za brzo kretanje.
Kad je ova opcija isključena, o takvim tablicama NVDA neće izvještavati i neće ih biti moguće pronaći uz pomoć brzog kretanja.
Međutim, tada se sadržaj tablice prikazuje kao običan tekst.
Ova je opcija standardno aktivirana.

Kako biste mogli globalno uključiti tablice rasporeda koristeći prečace, dodijelite prilagođeni prečac koristeći dijaloški okvir [Ulazne geste](#InputGestures).

##### Podešavanje izvještavanje o poljaima kao što su poveznice i naslovi {#BrowseModeLinksAndHeadings}

Pogledajte opcije u kategoriji [Oblikovanje dokumenta](#DocumentFormattingSettings) u [NVDA Postavkama](#NVDASettings) kako biste podesili izgovor polja pri kretanju poput poveznica, naslova i tablica.

##### Automatski modus fokusa pri promjeni fokusa {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Ova opcija omogućuje da modus fokusa bude pozvan kad se fokus promjeni.
Na primjer, kad se nalazite na web stranici, ako pritisnete tabulator i naiđete na obrazac, ako je ova opcija odabrana, modus fokusa će se automatski pokrenuti.

##### Automatski modus fokusa pri pomicanju kursora sustava {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Ova opcija, kad je odabrana, omogućuje  NVDA ulaz i izlaz iz modusa fokusa kad se koriste kursorske tipke.
Na primjer, kad se krećete po web stranici sa strelicom prema dolje i naiđete na polje za uređivanje, NVDA će automatski prebaciti na modus fokusa.
Ako izađete iz polja za uređivanje uz pomoć strelice, NVDA će vas vratiti u modus čitanja.

##### Audio oznaka za moduse fokusa i čitanja {#BrowseModeSettingsPassThroughAudioIndication}

Ako je ova opcija aktivirana, NVDA će svirati specijalne zvukove kad se prebacuje između modusa čitanja i modusa fokusa, umjesto da izgovori promjenu.

##### Onemogući nenaredbenim gestama pristup dokumentu {#BrowseModeSettingsTrapNonCommandGestures}

Standardno aktivirana, ova opcija omogućuje donijeti odluku o tome, hoće li geste (kao što su pritisci tipaka) koje ne rezultiraju u NVDA naredbi i koje se općenito ne smatraju NVDA naredbama, biti spriječene pristupiti trenutačno fokusiranom dokumentu. 
Na primjer, kad je ova opcija aktivirana, ako se pritisne slovo j, ono se neće proslijediti dokumentu, iako nije prečac za brzo kretanje ili prečac u samoj aplikaciji.
U tom slučaju će NVDA narediti operativnom sustavu da svira standardni zvuk, kadgod se pritisne tipka koja se ne proslijeđuje.

<!-- KC:setting -->

##### Automatski postavi fokus na elemente koji se mogu fokusirati {#BrowseModeSettingsAutoFocusFocusableElements}

Prečac: NVDA+8

Onemogućena podrazumjevano, ova opcija omogućuje vam hoće li elementi koji  mogu preuzeti fokus sustava činiti isto. To mogu biti Veze, polja obrazaca, itd. when navigating content with the browse mode caret.
Ako ostavite ovu opciju isključenom elementi koji se mogu fokusirati automatski neće biti fokusirani kada se odaberu korsorom modusa čitanja.
Ovo može prouzročiti bržu reakciju i rad u modusu čitanja.
Fokus će se aktivirati samo onda kada dođete u interakciju s elementom  (na primjer pritiščući gumb, odabirući potvrdni okvir).
Ako omogućite ovu opciju, možda će se poboljšati podrška za neke web stranice u zamjenu za perfornse i stabilnost.

#### Oblikovanje dokumenta {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Otvara postavke oblikovanja dokumenta {#toc250}

Prečac: `NVDA+kontrol+d`

Većina ovih opcija služi za podešavanje opcija koje služe za podešavanje izgovora svojstva oblikovanja pri kretanju.
Na primjer, ako odaberete potvrdni okvir izvijesti o imenu fonta, svaki put, kad se budete pomicali po tekstu uz pomoć kursorskih tipaka i nailazili na drugačiji font, ime fonta biti će izgovoreno.

Dijaloški okvir za oblikovanje teksta je organiziran u grupe.
Možete podesiti izvještavanje o sljedećim elementima:

* font
  * ime fonta
  * veličina fonta
  * Indeksi i eksponenti
  * karakteristika fonta
  * Istaknut (označen) tekst
  * isticanje
  * stil
  * boje
* informacije o dokumentu
  * komentari
  * Knjižne oznake
  * revizije urednika
  * pravopisne pogreške
* stranice i numeriranje
  * brojevi stranica
  * brojevi redaka
  * izvještavanje o uvlačenju retka [(Isključeno, Govor, Zvučni signali, Oboje Govor i zvučni signali)](#DocumentFormattingSettingsLineIndentation)
  * uvlačenje odlomka (npr. viseća uvlaka, samo prvi redak)
  * Ignoriranje praznih redaka pri čitanju uvlačenja
  * prored (jednostruki, dvostruki itd.)
  * poravnanje retka
* informacije o tablici
  * tablice
  * Zaglavlja redaka ili stupaca (isključeno, redci, stupci, redci i stupci)
  * koordinate ćelija
  * rubovi ćelija (Isključeno, Stilovi, Boje i stilovi)
* elementi
  * naslovi
  * poveznice
  * grafički elementi
  * popisi
  * citati
  * grupe
  * orijentiri
  * članci
  * okviri
    * figure i potpisi
  * klikajući elementi

Da biste ove postavke mogli uključiti ili isključiti s bilo kojeg mjesta, dodijelite prilagođene tipkovničke prečace, koristeći [dijaloški okvir ulazne geste](#InputGestures).

##### Izvijesti o promjenama oblikovanja nakon kursora {#DocumentFormattingDetectFormatAfterCursor}

Ako je ova opcija uključena, ova će opcija uzrokovati da NVDA pokuša prepoznati sve postavke oblikovanja u retku i potom ih izgovara, čak iako uključite ovu opciju to može uzrokovati usporavanje NVDA.

NVDA će standardno prepoznati oblikovanje na poziciji kursora sustava odnosno preglednog kursora i u nekim slučajevima može otkriti formatiranje na ostatku retka, samo ako to ne izazva pad performansi.

Uključite ovu opciju kad radite na korekciji teksta u aplikacijama kao što je Word pad, gdje je oblikovanje važno.

##### Izvještavanje o uvlačenju redaka {#DocumentFormattingSettingsLineIndentation}

Ova opcija omogućuje podešavanje načina izvještavanja o uvlačenju retka.
Odabirni okvir "Izvijesti o uvlaćenju redaka", ima četiri opcije.

* Isključeno: NVDA neće obraćati pažnju na poravnanje retka.
* Govor: Ako je ova opcija označena, kad se broj uvlaka promijeni, nvda će izgovoriti na primjer "dvanaest razmaka" ili "četiri tabulatora."
* Zvučni signali: ako su zvučni signali označeni, kad se vrijednost uvlake promijeni, zvučni signali obavještavaju o promjeni uvlake.
Zvuk se povećava u visini za svaki razmak, a za tabulator, povećavat će se ekvivalentno četirima razmacima.
* Govor i zvučni signali: Ova opcija čita uvlake koristeći obje metode.

Ako označite potvrdni okvir "ignoriraj prazne redke pri čitanju uvlačenja" tada se promjene uvlačenja neće čitati za prazne redke.
Ovo može biti korisno pri čitanju izvornog koda nekog programa gdje se prazni redci koriste za odvajanje blokova uvučenog teksta.

#### Kretanje po dokumentu {#DocumentNavigation}

Ova vam kategorija omogućuje podešavanje raznih opcija vezanih uz kretanje po dokumentu.

##### Stil odlomka {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumjevano (neka rukuje aplikacija), neka rukuje aplikacija, jednostruki pritisak entera, dvostruki pritisak entera|
|podrazumjevano |neka rukuje aplikacija|

Ovaj odabirni okvir omogućuje odabir stila odlomka koji bi se trebao koristiti prilikom kretanja po odlomcima uz pomoć tipkovničkih prečaca `control+Strelica gore` i `control+strelica dolje`.
Slijedeći stilovi odlomaka su dostupni:

* Neka rukuje aplikacija: NVDA će omogućiti aplikaciji određivanje sljedećeg ili prethodnog odlomka, i NVDA će pročitati slijedeći odlomak pri kretanju.
Ovaj stil radi najbolje kada aplikacija podržava nativno kretanje po odlomcima, i postavljen je podrazumijevano.
* Jednostruki pritisak entera: NVDA će pokušati odrediti prethodni ili slijedeći odlomak koristeći jednostruki prijelom redka kao indikator odlomka.
Ovaj stil radi najbolje u aplikacijama koje ne podržavaju kretanje po odlomcima nativno, a odlomci su označeni jednim pritiskom tipke `enter`.
* dva pritiska entera: NVDA će pokušati odrediti prethodni ili slijedeći odlomak koristeći najmanje jedan prazan redak (dva pritiska tipke `enter`) kao oznake odlomka.
Ovaj stil radi najbolje u dokumentima koji koriste blokovne odlomke.
Imajte na umuu da se ovaj stil odlomka ne može koristiti u Microsoft Wordu ili Microsoft Outlooku, osim ako koristite UIA za pristup Microsoft Word kontrolama.

Možete se prebacivati između dostupnih stilova odlomaka tako da pridijelite tipkovnički prečac u [dijaloškom okviru ulazne geste](#InputGestures).

#### Windows OCR postavke {#Win10OcrSettings}

Postavke u ovoj kategoriji omogućuju podešavanje [Windows OCR](#Win10Ocr).
Ova kategorija sadrži sljedeće opcije:

##### Jezik prepoznavanja {#Win10OcrSettingsRecognitionLanguage}

Ovaj odabirni okvir omogućuje izbor jezika koji će se koristiti za prepoznavanje sadržaja.
Kako biste kružili kroz dostupne jezike s bilo kojeg mjesta, molimo podesite prilagođenu prečicu u [dijaloškom okviru ulaznih gesti](#InputGestures).

##### S vremena na vrijeme osvježavaj prepoznati sadržaj {#Win10OcrSettingsAutoRefresh}

Kada je ovaj potvrdni okvir uključen, NVDA će automatski osvježavati tekst kada je prepoznati rezultat u fokusu.
Ovo može biti vrlo korisno kada želite čitati sadržaj koji se često mijenja kao što je to na primjer video sa titlovima.
Sadržaj se osvježava svakih pol sekunde.
Ova je opcija podrazumjevano isključena.

#### Napredne postavke {#AdvancedSettings}

Upozorenje! Ove postavke mogu prouzročiti nepravilno funkcioniranje NVDA, ako su konfigurirane nepravilno.
Radite ove izmjene ako znate što radite, ili vas je na to uputio NVDA razvojni programer.

##### Mijenjanje naprednih postavki {#AdvancedSettingsMakingChanges}

U slučaju da želite promijeniti napredne postavke, kontrole se moraju aktivirati potvrdnim okvirom, kojim potvrđujete, da razumijete da postoji rizik kad se postavke mijenjaju 

##### Vraćanje na standardne postavke {#AdvancedSettingsRestoringDefaults}

Gumb vraća standardne postavke, čak kad potvrdni okvir nije označen.
Poslije testiranja izmjena, možda se želite vratiti na standardne vrijednosti.
To isto može biti slučaj ako niste sigurni, jeste li promijenili postavke.

##### Aktiviraj učitavanje koda iz mape bilježnica razvojnog programera {#AdvancedSettingsEnableScratchpad}

Prilikom razvijanja NVDA dodataka, korisno je testirati kod prilikom pisanja istog.
Kada je ova opcija omogućena, dozvoljava programu NVDA učitavanje prilagođenih modula za aplikacije, globalnih dodataka, upravljačkih programa za brajične redke, upravljačke programe govornih jedinica i usluga pomoći za vid iz specijalne mape Scratchpad u vašem folderu za NVDA konfiguraciju.
Kao i njihovi ekvivalenti u dodacima, ovi moduli se učitavaju kada se NVDA pokrene, ili u slučaju modula za aplikacije i globalnih dodataka, kada se  [ponovo učitaju dodaci](#ReloadPlugins).
Ova je opcija standardno isključena, kako bi korisnik bio siguran da se nekompatibilan kod neće izvršavati u NVDA čitaču ekrana.
Ako želite distribuirati prilagođeni kod drugima, spakirajte ga kao NVDA dodatak.

##### Otvori mapu bilježnica razvojnog programera {#AdvancedSettingsOpenScratchpadDir}

Ovaj gumb otvara mapu gdje je smješten prilagođeni kod kojeg trenutačno razvijate.
Ovaj gumb postoji samo kad je uključena opcija "omogući bilježnicu razvojnog programera NVDA".

##### Registracija za događaje automatizacije korisničkog sučelja i promjene svojstava {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |automatski, selektivno, globalno|
|podrazumjevano |automatski|

Ova opcija mijenja način na koji NVDA registrira događaje UI automation sučelja za pristupačnost.
Odabirni okvir Registracija za događaje automatizacije korisničkog sučelja i promjene svojstava sadrži tri opcije:

* Automatska: "selektivna" u Windowsima 11 Sun Valley 2 (verzija 22H2) i novijim, u suprotnom "globalna".
* Selektivna: NVDA će ograničiti registraciju događaja na fokus sustava za većinu događaja.
Ako vam smetaju problemi sa performansama u jednoj ili više aplikacija, preporučujemo vam da isprobate ovu funkciju i vidite postoji li poboljšanje u performansama.
Međutim, u starijim inačicama sustava Windows, NVDA može imati probleme sa sljeđenjem fokusa u nekim kontrolama poput upravitelja zadataka i panela za emoji).
* Globalna: NVDA registrira puno UIA događaja koji su procesirani i uništavani u NVDA čitaču.
Iako je sljeđenje fokusa pouzdanije u više situacija, performanse su značajno degradirane, naročito u  Microsoft Visual Studiu.

##### Koristi UI automation za pristup Microsoft Word dokumentima {#MSWordUIA}

Regulira treba li  NVDA koristiti UI Automation API za pristupačnost za pristup Microsoft Word dokumentima, umjesto starog Microsoft Word modela objekata.
Ovo se primjenjuje na dokumente u Microsoft Wordu, te poruke u Microsoft Outlooku.
Ova postavka sadrži sljedeće vrijednosti:

* Podrazumjevano (gdje je to potrebno)
* Samo kada je to potrebno: Tamo gdje Microsoft Wordov model objekata nije dostupan sasvim
* Gdje je to potrebno: Microsoft Word inačica 16.0.15000 ili novija, ili ako Microsoft Word model objekata nije dostupan
* Svugdje: Gdjegod da je UI automation dostupan u Microsoft wordu (bez obzira na kompletnost).

##### Koristi UI automation za pristup Excel proračunskim tablicama kada je to moguće {#UseUiaForExcel}

Kada je ova opcija omogućena, NVDA će probati koristiti Microsoft UI Automation API za pristupačnost kako bi izvlačio informacije iz kontrola proračunskih tablica Microsoft Excela.
To je eksperimentalna funkcija, i neke značajke Microsoft Excela mogu biti nedostupne koristeći taj modus.
Na primjer, NVDA popis elemenata za popisivanje formula i komentara, i i brzo kretanje u modusu čitanje za preskakanje na polja obrazaca u proračunskoj tablici.
Međutim, prilikom osnovnog kretanja po proračunskoj tablici ili uređivanja , ova opcija može donijeti značajno unapređenje u performansama.
Još uvijek ne preporučujemo da većina korisnika uključuje ovo kao podrazumjevani način rada, ali pozivamo korisnike Microsoft Excela  koji koriste verziju 16.0.13522.10000 ili noviju da testiraju ovu funkciju i poišalju povratnu informaciju.
Implementacija UIA u Microsoft excelu se mijenja od verzije do verzije, te  verzije Microsoft office paketa starije od 16.0.13522.10000 mogu pružati nedovoljno informacija na način da ova opcija bude od koristi.

##### Koristi unapređeno procesuiranje događaja {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |podrazumjevano (omogućeno), onemogućeno, omogućeno|
|Podrazumjevano |Omogućeno|

Kada je ova opcija uključena, NVDA će ostati brz i responsivan kada dobije previše događaja UI Automation, Na primjer velika količina teksta u naredbenom redku.
Poslije promjene ove opcije, trebate ponovno pokrenuti NVDA kako bi promjene stupile na snagu.

##### Podrška Windows naredbenog redka {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Automatski, UIA kada je dostupno, zastarjelo|
|Podrazumjevano |automatski|

Ova opcija utječe na to kako NVDA radi u korištenom Windows naredbenom redku kojeg koristi stari naredbeni redak, PowerShell, i podsustav linux za sustav Windows.
Ovo ne utjeće na suvremeni Windows terminal.
U Windowsima 10 inačici 1709, Microsoft [je dodao podršku za svoj UI automation API u naredbeni redak](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), koji donosi unapređenje u stabilnosti i performansama za čitače zaslona koji ga podržavaju.
U situacijama u kojima UI automation nije dostupan ili je poznato da će prouzrokovati nedovoljno korisničko iskustvo, dostupna je zastarjela NVDA podrška kao povratna opcija.
Odabirni okvir podrška za Windows naredbene redke ima tri opcije:

* Automatski: koristi UI automation u inačicama Windowsovog naredbenog redka koji dolazi sa Windowsima 11 inačicom 22H2 i novijima.
Ova je opcija preporučena i podrazumjevano uključena.
* UIA kada je dostupno: Koristi UI automation u naredbenim redcima kada je to moguće, čak za nekompletne ili neispravne implementacije.
Iako ova funkcionalnost može biti korisna, (i čak dostatna za vaše korištenje), korištenje ove opcije prepušteno je vašem riziku te podrška za nju neće bit pružena.
* Zastarjela: UI Automation u Windows naredbenom redku bit će potpuno isključen.
Zastarjela povratna opcija biti će uvijek korištena čak u situacijama gdje bi UI automation pružio superiornije korisničko iskustvo.
Stoga, odabir ove opcije nije preporučljiv osim ako znate što radite.

##### Koristi UIA u Microsoft Edgeu i drugim preglednicima baziranim na Chromium platformi kad je to moguće {#ChromiumUIA}

Omogućuje određivanje kada će se UIA koristiti kada je dostupna u preglednicima baziranim na Chromium platformi kao što je to Microsoft Edge.
UIA podrška za preglednike bazirana na Chromium platformi je u ranom stadiju razvoja i može  manje biti funkcionalna od stare  IA2 implementacije.
Odabirni okvir sadrži sljedeće opcije:

* Podrazumijevano (samo kada je to potrebno): podrazumjevana opcija koju koristi NVDA, trenutno se koristi "samo kada je to potrebno". Ova se podrazumjevana opcija može promijeniti u budućnosti kada tehnologija bude zrela za široku uporabu.
* Samo kada je to potrebno: kada NVDA ne može ući u proces preglednika kako bi koristio IA2 UIA će biti dostupna, te će se tada NVAD prebaciti na UIA.
* Da: Ako će UIA biti dostupna u pregledniku, će ju koristiti.
* ne: ne koristi UIA, čak ako NVDA nije u stanju ući u proces. Ovo može biti zanimljivo za razvojne programere koji otklanjaju pogreške sa IA2, i žele osigurati da se NVDA ne vraća na korištenje UIA.

##### Zabilješke {#Annotations}

Ova grupa opcija se koristi za omogućavanje značajki koje dodaju eksperimentalnu podršku za ARIA zabilješke.
Neke od ovih značajki mogu biti nedovršene.

<!-- KC:beginInclude -->
Kako biste "pročitali detalje bilo koje zabilješke pod kursorom", pritisnite NVDA+d.
<!-- KC:endInclude -->

Postoje sljedeće opcije: 

* "Izgovaraj 'postoje detalji' za strukturne zabilješke": uključuje izvještavanje o postojanju dodatnih detalja u tekstu ili kontroli.
* "Uvijek izgovaraj aria-description":
  Kada je izvor `accDescription` aria-description, opis će se izgovarati.
  ovo je korisno za zabilješke na mreži.
  Upozorenje:
  * Postoji više izvora za `accDescription` neki od njih imaju nepouzdanu ili miješanu semantiku.
    U povijesti asistivne tehnologije nisu mogle  razlikovati izvore `accDescription` uobičajeno nije se izgovaralo zbog mješane semantike.
  * Ova je opcija u jako ranom razvoju. Ova opcija ovisi o značajkama preglednika koje nisu široko dostupne.
  * Očekuje se da će ova opcija raditi sa Chromium verzija 92.0.4479.0 i novijim

##### Prijavi žive regione {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumjevano (omogućeno), onemogućeno, omogućeno|
|Podrazumjevano |omogućeno|

Ova opcija bira da li će NVDA prijaviti promene u određenom dinamičkom Web sadržaju na brajevom redu.
Onemogućavanje ove opcije je jednako ponašanju programa NVDA u verziji 2023.1 i starijim, koja je ove promjene prijavljivala samo govorom.

##### Izgovori lozinke u svim unapređenim naredbenim redcima {#AdvancedSettingsWinConsoleSpeakPasswords}

Ova opcija regulira mogućnost izgovora znakova kada su uključene opcije  [izgovor upisanih znakova](#KeyboardSettingsSpeakTypedCharacters) ili [izgovor upisanih riječi](#KeyboardSettingsSpeakTypedWords) kada se zaslon ne obnavlja (kao što je to slučaj kod upisa lozinke) u nekim programima naredbenog redka, poput Windows naredbenog redka sa uključenom podrškom za UI automation i Mintty.
Iz sigurnosnih razloga, ova opcija treba biti isključena.
Međutim, možete ju isključiti ako uočavate nestabilnosti ili nestabilnost sa čitanjem upisanih znakova u naredbenim redcima, ili radite u povjerljivom okruženju i preferirate čitanje lozinki.

##### Koristi podršku naprednog upisivanja znakova u starijim naredbenim redcima sustava Windows kada je to moguće {#AdvancedSettingsKeyboardSupportInLegacy}

Ova opcija pruža alternativnu metodu otkrivanja upisanih znakova u starijim naredbenim redcima sustava Windows.
Iako ova opcija  donosi unapređenja performansi i ispravlja problem slovkanja neželjenih stavki, ista može biti nekompatibilna s nekim programima naredbenog retka.
Ova je opcija dostupna i standardno je uključena u Windows 10 verzijama 1607, i novijim kad je UIA nedostupno ili deaktivirano.
Upozorenje: s uključenom ovom opcijom, izgovoreni znakovi koji se ne pokazuju na ekranu, poput lozinki, biti će izgovoreni.
U nepovjerljivim okruženjima, možda biste trebali privremeno isključiti opcije [izgovor upisanih znakova](#KeyboardSettingsSpeakTypedCharacters) i [Izgovor upisanih riječi](#KeyboardSettingsSpeakTypedWords) pri upisivanju lozinki.

##### Metoda praćenja izmjena sadržaja u konzolama {#DiffAlgo}

Ovom se opcijom određuje kako NVDA označuje novi tekst koji treba biti ozgovoren u programima koji koriste naredbeni redak.
Odabirni okvir  metoda praćenja izmjena sadržaja u konzolama sadrži tri opcije:

* Automatski: Ova opcija prouzrokuje da NVDA koristi Diff match patch u većini slučajeva, ali da se vraća na difflib u problematičnim situacijama, kao što je to starija inačica Windows naredbenog redka i Mintty.
* Diff Match Patch: Ova opcija prouzrokuje da NVDA računa izmjene u tekstu naredbenog redka znak po znak, čak u situacijama kada to nije preporučljivo.
To može unaprediti performanse kada se zapisuju velike količine teksta u terminal te omogućuje točnije izgovaranje novog teksta.
Međutim, u nekim aplikacijama, čitanje novog teksta može biti isprekidano ili nedosljedno.
* Difflib: Ova opcija prouzrokuje da NVDA izračunava izmjene u naredbenom redku redak po redak, čak u situacijama kada se to ne preporućuje.
To je istovjetno ponašanju NVDA u inačicama 2020.4 i starijim.
Ova postavka može stabilizirati čitanje dolaznog teksta u nekim programima.
Međutim, u naredbenim redcima, prilikom dodavanja ili brisanja znakova u sredini redka, tekst poslije kursora bit će pročitan.

##### Izgovori novi tekst u Windows terminalu uz pomoć {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |Podrazumjevano (difovanje), difovanje, UIA obavjesti|
|Podrazumjevano |difovanje|

Ova opcija regulira način na koji NVDA otkriva "novi" tekst, i stoga što treba izgovoriti kada je opcija  "izgovori promjene dinamičkog sadržaja" uključena u Windows Terminalu i WPF Windows Terminalu kontroli koja se koristi u  Visual studio 2022.
Ovo ne utjeće na naredbeni redak sustava windows (`conhost.exe`).
Odabirni okvir izgovori novi tekst u naredbenom redku sadrži tri opcije:

* Podrazumjevano: Ova je opcija trenutno istobinta opciji "difovanje", ali se to planira promijeniti kada će UIA podrška biti dorađenija.
* Difovanje: Ova opcija koristi označeni algoritam difovanja za računanje novih izmjena kada terminal prikazuje novi tekst.
Ovo je istovjetno ponašanju NVDA u inačicama 2022.4 i ranijim.
* UIA obavijesti: Ova opcija prebacuje odgovornost određivanja novog teksta na Windows terminal, što znači da NVDA više ne mora motriti novi tekst.
Ovo unapređuje performanse i stabilnost Windows terminala, ali ova funkcija nije još usavršena.
Točnije, znakovi koji se ne vide na zaslonu poput lozinki, se čitaju kada je ova opcija uključena.
Dodatno, izlaz teksta koji prekoračuje 1000 znakova može biti neispravno pročitan.

##### Pokušaj zaustavljanja govora za događaje fokusa koji su istekli {#CancelExpiredFocusSpeech}

Ova opcija uključuje ponašanje koje omogućuje zaustavljanje govora za događaje fokusa koji su istekli.
Uobičajeno kretanje kroz poruke u Gmailu sa Chromeom može prouzročiti da NVDA izgovara netočne informacije.
Ova je funkcija podrazumjevano uključena od  NVDA verzije 2021.1.

##### Brzina micanja kursora sustava (u milisekundama) {#AdvancedSettingsCaretMoveTimeout}

Ova opcija omogućuje povećanje ograničenja čekanja, u kojem NVDA čeka da se pojavi pokazivač u polju za uređivanje.
Ako mislite da NVDA uvijek kasni jedan znak iza ili ponavlja retke, tada biste trebali povećati ovu vrijednost.

##### Izgovaraj transparentnost boja {#ReportTransparentColors}

Ova opcija omogućuje izgovor transparentnosti boja, korisno za programere koji razvijaju module aplikacija ili dodatke te koji skupljaju informacije u svrhu unapređivanja korisničkog iskustva sa aplikacijom treće strane.
Neke GDI aplikacije će isticati tekst pozadinskom bojom, NVDA (uz pomoć modela prikaza) će pokušati izgovoriti tu boju.
U nekim situacijama, pozadina teksta može biti potpuno transparentna, sa tekstom prekrivenim na nekom drugom elementu prozora.
Sa nekim povijesno popularnim GUI api-jima, tekst može biti prikazan sa transparentnom pozadinom, ali je vizualno pozadinska boja točna.

##### Koristi WASAPI za audio izlaz {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Opcije |podrazumjevano (omogućeno), onemogućeno, omogućeno|
|Podrazumjevano |omogućeno|

Ova opcija će omogućiti reprodukciju zvukova korištenjem standarda Windows Audio Session API (WASAPI).
WASAPI je moderniji standard zvuka koji može poboljšati brzinu, performanse i stabilnost NVDA zvukova, što uključuje govor i NVDA zvukove.
Nakon što promjenite ovu opciju, morat ćete ponovo pokrenuti NVDA kako bi se promjene primjenile.
Kada onemogućite WASAPI biti će onemogućene slijedeće opcije:

* [Glasnoća NVDA zvukova prati glasnoću drugih zvukova](#SoundVolumeFollowsVoice)
* [Glasnoća NVDA zvukova](#SoundVolume)

##### Kategorije zapisivanja {#AdvancedSettingsDebugLoggingCategories}

Potvrdni okviri u ovoj kategoriji omogućuju dodavanje kategorija debugiranja u zapisnik.
Zapisivanje ovih poruka može prouzročiti pad performansi i velike datoteke zapisnika.
Uključite iste samo ako vas je na to naveo Programer NVDA razvojnog tima, u slučaju da, na primjer, ne radi brajični redak.

##### Reproduciraj zvuk za zapisane greške {#PlayErrorSound}

Ova opcija omogućuje određivanje hoće li NVDA reproducirati zvuk u slučaju zapisane pogreške.
Ako izaberete samo u testnim verzijama (podrazumijevano) prouzročit će da će se zvukovi reproducirati samo ako se radi o testnoj verziji (alpha, beta ili ako se pokreće iz izvornog koda).
Ako odaberete da zvukovi će se reproducirati neovisno od verzije NVDA.

##### Regularni izraz za kretanje po odlomcima {#TextParagraphRegexEdit}

Ovo polje omogućuje prilagođavanje regularnog izraza za otkrivanje odlomka modusu čitanja.
Traženje odlomaka koristeći [Prečac za kretanje po odlomcima](#TextNavigationCommand) ovisi od ovog polja.

### Razne postavke {#MiscSettings}

Osim [Postavki NVDA](#NVDASettings) dijaloškog okvira, podizbornik postavke, sadrži sljedeće stavke koje su opisane ispod.

#### Govorni rječnici {#SpeechDictionaries}

Izbornik govorni rječnici (kojeg možete pronaći u izborniku postavke) sadrži dijaloške okvire koji omogućuju upravljanje načinom na koji NVDA izgovara određene riječi ili fraze.
trenutačno postoje tri vrste govornih rječnika.
To su:

* Glavni riječnik: Pravila u ovom rječniku važe za sav govor u NVDA.
* Glasovni: Pravila u ovom rječniku primjenjuju se na govornu jedinicu i na glas koji se trenutačno koristi.
* Privremeni: pravila u ovom rječniku Primjenjuju se na sav govor u NVDA, ali samo za trenutačnu sesiju. Ova su pravila privremena i bit će izgubljena kad NVDA bude ponovo pokrenut.

Morate definirati prilagođene ulazne geste koristeći [dijaloški okvir ulazne geste](#InputGestures) ako želite otvarati jedan od ovih dijaloških okvira za riječnike od bilo gdje.

Svi dijaloški okviri za rječnike sadrže listu pravila koja se koriste za procesiranje govora.
Dijaloški okvir također sadrži gumbe dodaj, uredi, ukloni i ukloni sve.

Da biste dodali novo pravilo u rječnik, pritisnite gumb dodaj i popunite polja u dijaloškom okviru koji se prikaže i pritisnite u redu.
Tada ćete vidjeti vaše novo pravilo u popisu pravila.
međutim, da biste se uvjerili da je vaše pravilo spremljeno, ne zaboravite zatvoriti dijaloški okvir pritiskom na gumb u redu nakon dodavanja ili uređivanja pravila.

Pravila u NVDA rječnicima omogućuju promjenu jednog niza znakova u drugi.
Najjednostavniji bi primjer bio da umjesto riječi ptica NVDA svaki put, umjesto riječi ptica, izgovori žaba.
Kad uđete u dijaloški okvir dodavanje pravila, najlakši način za ovu izmjenu je upisati riječ ptica u polje za uzorak i riječ žaba u polje za zamjensku riječ.
Također biste možda htjeli napisati opis pravila u polje za komentar (nešto poput: Mjenja riječ ptica u žaba).

Međutim, NVDA govorni rječnici su daleko močniji od zamjene riječi.
Dijaloški okvir za dodavanje pravila sadrži potvrdni okvir, kojim se određuje razlikovanje između malih i velikih slova (što znači da NVDA mora paziti, jesu li se u određenom pravilu koriste velika slova ili ne.
NVDA standardno zanemaruje razlikovanje velikih i malih slova).

I na kraju, serija izbornih gumba omogućuje da uzrokujete da NVDA zna da vaš uzorak se poklapa svugdje, da se tretira kao cijela riječ ili kao "regularni izraz".
Postavljanje uzorka da se poklapa kao cijela riječ znači da će se zamjena izvršiti samo uzorak ne dolazi kao dio veće riječi.
Ovaj je uvjet zadovoljen ako znakovi neposredno prije i poslije riječi su sve osim slova, broja, ili donje crte, te ako uopće ne postoje znakovi.
Već, kad koristimo primjer zamjene riječi "ptica" s riječi "žaba", ako ste izabrali da NVDA tu riječ tretira kao zamjenu za cijelu riječ, neće se poklapati s "ptice" ili "bluebird".

Regularni je izraz uzorak koji sadrži specijalne znakove koji omogućuju preklapanja više znakova od jednom ili podudaranje samo brojeva ili samo slova, kao nekoliko primjera.
Regularni izrazi nisu pokriveni u ovom korisničkom priručniku.
Za uvodni tutorial, molimo pogledajte [Pythonov vodič po regularnim izrazima](https://docs.python.org/3.11/howto/regex.html).

#### Izgovor simbola interpunkcije {#SymbolPronunciation}

Ovaj dijaloški okvir omogućuje promjenu načina na koji su interpunkcija i drugi simboli izgovoreni, kao i razinu simbola na koji je izgovoren znak.

Jezik za koji se uređuje izgovor simbola će se prikazati u naslovnoj traci dijaloškog okvira.
Imajte na umu da ovaj dijaloški okvir poštuje opciju "Vjeruj jeziku glasa za čitanje opisa znakova i simbola" koja se nalazi u [kategoriji govor](#SpeechSettings) u [dijaloškom okviru postavki](#NVDASettings); to jest, to koristi jezik trenutačno označenog glasa, a ne glabalni jezik NVDA kad je ova opcije uključena.

Da biste promijenili simbol, označite ga u listi simbola.
Možete filtrirati simbol, upisujući cijelu zamjenu ili dio zamjene simbola u polje za uređivanje filtriraj po.

* Polje zamjena omogućuje izmjenu teksta koji će biti izgovoren na mjestu tog simbola.
* Koristeći polje razina, možete prilagoditi najnižu razinu simbola na kojoj taj simbol treba biti izgovoren (ništa, neki, većina ili sve).
Također možete postaviti razinu na znak; u tom slučaju simbol neće biti izgovoren, neovisno o razini koja se koristi, uz slijedeće dve iznimke:
 * prilikom kretanja po znakovima.
 * Kada NVDA slovka tekst koji sadrži taj simbol.
* Polje "Pošalji trenutačni simbol govornoj jedinici", kad će sam simbol (u sprezi s njegovom zamjenom) biti poslan govornoj jedinici.
To je korisno kad govorna jedinica reagira na simbol pauzom ili povisivanjem modulacije glasa.
Na primjer, zarez prouzrokuje pauzu kod govorne jedinice.
Postoje tri mogućnosti:
  * Nikad: Nikad ne šalji trenutačni simbol govornoj jedinici.
  * Uvijek: Uvijek pošalji simbol govornoj jedinici.
  * samo ispod razine simbola: Pošalji trenutačni simbol samo ako je podešena razina simbola niža od one postavljene za simbol.
  Na primjer, mogli biste ovo koristiti da bi se simbol izgovarao na višim razinama bez pauza, a da istovremeno bude pauziran na nižim razinama.

Možete dodati nove simbole pritišćući gumb dodaj.
U dijaloškom okviru koji će se pojaviti, upišite simbol i pritisnite u redu.
Promijenite sva polja za novi simbol kao što bi ste učinili za druge simbole.

Možete ukloniti simbol kojeg ste prije dodali kad pritisnete gumb ukloni.

Kad završite, pritisnite gumb u redu da biste spremili vaše promjene ili gumb odustani da bi ste ih poništili.

U slučaju kompleksnih simbola, polje zamjene bi trebalo sadržavati neke grupne reference teksta koji se poklapa. Na primjer, za uzorak koji se poklapa sa cijelim datumom, \1, \2, i \3 trebalo bi se pokazati u polju, te bi trebalo biti zamjeno sa određenim dijelovima datuma.
Obične obrnute kose crte trebale bi biti duplicirane, npr. "a\\b" treba biti upisano kako biste dobili "a\b" zamjenu.

#### Ulazne geste {#InputGestures}

U ovom dijaloškom okviru Možete prilagođavati ulazne geste: (Tipke na tipkovnici, tipke na brajičnom retku itd.) kao NVDA prečace.

Naredbe koje se mogu promjeniti su one za čiju je promjenu otvorena aplikacija koja ih koristi.
Na primjer, ako želite prilagoditi prečace koji su vezani uz modus čitanja, trebate otvoriti dijaloški okvir za promjenu ulaznih gesti kad ste u modusu čitanja.

Stablo u ovom dijaloškom okviru popisuje sve primjenjive NVDA prečace grupirane po kategoriji.
Možete ih filtrirati upisujući jednu ili više riječi imena prečaca u "filtriraj" polje za uređivanje.
Sve geste pridružene prečacu su popisane uz prečac.

Da biste dodali ulaznu gestu prečacu, označite prečac i pritisnite gumb Dodaj.
Nakon toga izvedite ulaznu gestu koju želite pridružiti; npr. pritisnite tipku na tipkovnici ili tipku na brajičnom retku.
Geste često mogu biti protumačene na više načina.
Na primjer, kad pritisnete tipku na tipkovnici, možda je želite koristiti za trenutačni raspored tipkovnice (npr. za stolna ili prijenosna računala) ili možda želite da se ta gesta primjenjuje za sve tipkovničke rasporede.
U tom slučaju, pojavit će se izbornik u kojem ćete moći označiti željenu opciju.

Da biste uklonili gestu iz prečaca, označite gestu i pritisnite gumb Ukloni.

Kategorija Emulirani prečaci sustava sadrži prečace koji emuliraju prečace na tipkovnici sustava.
Ovi prečaci se mogu koristiti za kontrolu tipkovnice s vašeg brajičnig retka.
Kako biste dodali emulirani prečac, odaberite kategoriju emulirani prečaci i pritisnite gumb dodaj.
Potom pritisnite gumb na tipkovnici kojeg želite emulirati.
Poslije toga, tipka će biti dostupna u popisu emuliranih prečaca te će te moći dodjeliti prečac na način kako je to opisano iznad.

Upozorenje:

* Emulirani prečaci moraju imati pridjeljene geste kako bi se zadržali prilikom spremanja /zatvaranja dijaloškog okvira.
* Geste sa modifikatorima možda neće moći biti pridjeljene emuliranoj gesti bez modifikatora
Na primjer, postavljanjem emuliranog unosa 'a' i podešavanje ulazne geste 'ctrl+m', prouzrokovat će 
da će program primiti 'ctrl+a'.

Kad ste gotovi s promjenama, pritisnite gumb U redu da biste ih sačuvali ili gumb Odustani da biste ih poništili.

### Spremanje i vraćanje konfiguracije {#SavingAndReloading}

NVDA će standardno automatski spremati vaše postavke pri izlazu.
Međutim, imajte na umu da se ova opcija može promijeniti pod stavkom opće postavke u izborniku postavke.
Da biste spremili postavke ručno u bilo koje vrijeme, odaberite stavku spremi konfiguraciju u NVDA izborniku.

Ako ikad napravite pogrešku u vašim postavkama i trebate se vratiti natrag na pospremljene postavke, odaberite "vrati na spremljenu konfiguraciju" opciju koja se nalazi u NVDA izborniku.
Možete također vratiti postavke na njihove standardne vrijednosti kad odaberete opciju vrati konfiguraciju na standardnu, koja se također nalazi u NVDA izborniku.

Sljedeći prečaci su također korisni:
<!-- KC:beginInclude -->

| Naziv |Tipka za stolna računala |Tipka za prijenosna računala |Opis|
|---|---|---|---|
|Spremi konfiguraciju |NVDA+kontrol+c |NVDA+kontrol+c |Sprema vašu trenutačnu konfiguraciju kako se ne bi izgubila, kad izađete iz NVDA čitača|
|Vrati konfiguraciju |NVDA+kontrol+r |NVDA+kontrol+r |Kad se pritisne jednom, vraća na zadnje spremljene postavke. Kad se pritisne triput, vratit će je na standardnu.|

<!-- KC:endInclude -->

### Konfiguracijski profili {#ConfigurationProfiles}

Ponekad biste željeli imati različite postavke za različite situacije.
Na primjer, možda biste željeli imati uključeno izvještavanje o poravnanju kad uređujete tekst ili želite imati uključeno izvještavanje o svojstvima fonta kad radite korekturu nekog teksta.
NVDA to omogućuje uz pomoć konfiguracijskih profila.

Konfiguracijski profil sadrži samo one postavke koje su mjenjane kad je profil uređivan.
Većina postavki mogu se promijeniti u konfiguracijskim profilima osim onih postavki, koje se nalaze u kategoriji općenito u [dijaloškom okviru postavki](#NVDASettings), jer se te postavke primjenjuju na NVDA u cijelosti.

Konfiguracijski profili mogu biti aktivirani putem dijaloškog okvira ili uz pomoć prilagođenih dodanih gesti.
Oni se mogu aktivirati i automatski zbog okidača kao što je prebacivanje na određenu aplikaciju.

#### Osnovno upravljanje {#ProfilesBasicManagement}

Konfiguracijskim profilima možete upravljati kad dođete na opciju "Konfiguracijski profili" u NVDA izborniku.
Također to možete učiniti koristeći prečac:
<!-- KC:beginInclude -->

* NVDA+kontrol+p: Prikazuje dijaloški okvir konfiguracijski profili.

<!-- KC:endInclude -->

Prva kontrola u ovom dijaloškom okviru je popis profila iz kojeg možete odabrati jedan od dostupnih profila.
Kad otvorite dijaloški okvir, označen je prvi konfiguracijski profil kojeg uređujete.
Također su prikazane dodatne informacije za aktivne profile, pokazujući jesu li ili nisu ručno aktivirani, okinuti i/ili trenutačno uređivani.

Da biste preimenovali ili izbrisali profil, pritisnite gumb preimenuj ili gumb izbriši.

Pritisnite gumb zatvori da biste zatvorili dijaloški okvir.

#### Stvaranje profila {#ProfilesCreating}

Da biste stvorili profil, pritisnite gumb novi.

U dijaloškom okviru novi profil možete upisati ime za profil.
Također možete označiti kako će se taj profil koristiti.
Ako taj profil želite koristiti ručno, označite ručnu aktivaciju koja je standardna.
U suprotnom, odaberite okidač koji će automatski odabrati ovaj profil.
Zbog manje brige, ako niste upisali ime profila, kad označite okidač, ime će najtočnije biti upisano.
za više informacija o okidačima pogledajte [ispod](#ConfigProfileTriggers).

Kad pritisnete gumb u redu, dijaloški okvir konfiguracijski profili će se zatvoriti tako da možete urediti konfiguracijski profil.

#### Ručna aktivacija {#ConfigProfileManual}

Ručnu aktivaciju profila možete napraviti tako da označite profil u listi i pritisnete gumb ručna aktivacija.
Jednom kad je profil aktiviran, drugi profili još uvijek mogu biti aktivirani zbog okidača, ali postavke u ručno odabranom profilu će ih prepisati.
Na primjer, ako je profil okinut za trenutačnu aplikaciju i izvještavanje o poveznicama je aktivirano u tom profilu, ali deaktivirano u ručno aktiviranom profilu, poveznice se neće izgovarati.
Međutim, ako ste promjenili glas u okinutom profilu, ali ga nikad niste mjenjali u ručno aktiviranom profilu, bit će korišten glas iz okinutog profila.
Bilo koju postavku koju promjenite bit će spremljena u ručno aktivirani profil.
Da biste deaktivirali ručno aktivirani profil, označite ga u dijaloškom okviru konfiguracijski profili i pritisnite gumb ručno deaktiviraj.

#### Okidači {#ConfigProfileTriggers}

Pritisnete li gumb okidači u dijaloškom okviru konfiguracijski profili, to omogućuje izmjenu konfiguracijskih profila koji se automatski aktiviraju uz pomoć različitih okidača.

Popis okidača prikazuje sljedeće dostupne okidače:

* Trenutačna aplikacija: Okida se kad se prebacujete na trenutačnu aplikaciju.
* Izgovori sve: Okinut se kad se koristi naredba Izgovori sve.

Da biste izmjenili profil koji će koristiti okidanje, označite okidač, a nakon toga označite željeni profil s popisa profila.
Možete označiti "(standardna konfiguracija)" ako ne želite da se koristi profil.

Pritisnite gumb Zatvori da biste se vratili u dijaloški okvir Konfiguracijski profili.

#### Uređivanje profila {#ConfigProfileEditing}

Ako ste ručno aktivirali profil, sve postavke koje izmijenite bit će pospremljene u taj profil.
U suprotnom, sve postavke koje promijenite bit će pospremljene u najčešće okidani profil.
Na primjer, ako ste pridružili profil aplikaciji Notepad za pisanje i prebacujete se na Notepad za pisanje, sve promjenjene postavke bit će spremljene u taj profil.
Na kraju, ako ne postoji niit jedan ručno aktivirani ili okinuti profil, svaku postavku koju promijenite bit će pospremljena u vašu uobičajenu konfiguraciju.

Da biste uredili profil kojemu je pridružena naredba "Izgovori sve", morate [ručno aktivirati](#ConfigProfileManual) taj profil.

#### Privremeno deaktiviranje okidača {#ConfigProfileDisablingTriggers}

Ponekad je korisno deaktivirati sve okidače.
Na primjer, možda biste htjeli urediti ručno aktivirani profil ili urediti vašu uobičajenu konfiguraciju bez ometanja okinutog profila.
To možete učiniti na sljedeći način: označite potvrdni okvir Privremeno deaktiviraj sve okidače u dijaloškom okviru Konfiguracijski profili.

Za aktiviranje okidača profila s bilo kojeg mjesta, dodijelite prilagođenu gestu koristeći dijaloški okvir [Ulazne geste](#InputGestures).

#### Aktiviranje profila uz pomoć ulaznih gesti {#ConfigProfileGestures}

Možete dodati tipkovnički prečac za svaki profil koji stvorite kako boste ga mogli aktivirati.
Konfiguracijski profili standardno nemaju pridjeljenje ulazne geste.
Možete dodati prečace koristeći [Dijaloški okvir ulazne geste](#InputGestures).
Svaki profil ima svoj zapis u kategoriji ulaznih gesti.
Kad preimenujete profil, bilo koji prečac kojeg ste prethodno dodali oš će uvijek biti dostupan.
Kad izbrišete profil, također će biti izbrisane i geste, koje su s njim povezane.

### Lokacija konfiguracijskih datoteka {#LocationOfConfigurationFiles}

Prijenosne kopije NVDA čitača spremaju sve postavke, prilagođene module za aplikacije i prilagođene upravljačke programe za govorne jedinice u mapu userConfig koja se nalazi u mapi gdje je smješten NVDA.

Instalirane kopije NVDA čitača spremaju sve postavke, prilagođene module aplikacija i prilagođene upravljačke programe za govorne jedinice u posebnu mapu NVDA koja se nalazi u vašem Windows korisničkom profilu.
To znači da svaki korisnik sustava može imati vlastite NVDA postavke.
Kako biste otvorili mapu postavki s bilo kojeg mjesta, Možete koristiti [Dijaloški okvir ulazne geste](#InputGestures) kako biste za tu radnju pridjelili prilagođeni prečac.
Na instaliranim inačicama NVDA, možete u izborniku start ući u podizbornik programi -> NVDA -> istraži NVDA konfiguracijsku mapu.

Tijekom pokretanja na ekranima za prijavu ili kontrolama korisničkog računa, NVDA postavke se spremaju u direktorij systemConfig u instalacijskom direktoriju NVDA čitača.
Obično se ta konfiguracija ne treba dirati.
Da biste promijenili NVDA konfiguraciju na ekranima za prijavu ili kontrolama korisničkog računa, konfigurirajte NVDA po želji dok ste prijavljeni u Windowsu, spremite konfiguraciju, a zatim pritisnite gumb "Koristi trenutačno spremljene postavke na ekranima za prijavu te ostalim sigurnim ekranima" u kategoriji Opće, u dijaloškom okviru [NVDA Postavke](#NVDASettings).

## Dodaci i Add-on store {#AddonsManager}

Dodaci su softverski paketi koji nude nove ili izmijenjene NVDA funkcije.
Razvija ih NVDA zajednica, i organizacije treće strane kao što su prodavci komercijalnih alata.
Dodaci mogu raditi bilo koju od slijedećih stvari:

* Dodavanje ili poboljšanje podrške za određenu aplikaciju.
* Pružanje podrške za dodatne brajične redke ili govorne jedinice.
* Dodavanje ili promjenu NVDA postavki.

Add-on store vam dozvoljava pregled ili upravljanje dodacima.
Svi dodaci koji su dostupni u add-on storeu mogu se preuzeti besplatno.
Ali, neki od njih mogu zahtijevati od korisnika plaćanje za licencu ili dodatni softver prije nego korištenja.
Primjer ovakve vrste dodatka su komercijalne govorne jedinice.
Ako instalirate dodatak sa komponentama koje se plaćaju i predomislite se o njegovom korištenju, dodatak se lako može ukloniti.

Add-on storeu se pristupa iz podizbornika alati u NVDA izborniku.
Kako biste pristupili Add-on storeu sa bilo kojeg mjesta, podesite prilagođenu prečicu u dijaloškom okviru [ulazne geste](#InputGestures).

### Pregled dodataka {#AddonStoreBrowsing}

Kada se otvori, add-on store prikazuje popis dodataka.
Ako prethodno niste instalirali nijedan dodatak, add-on store će se otvoriti sa popisom dodataka koji su dostupni za instalaciju.
Ako imate instalirane dodatke, na popisu će se prikazati trenutno instalirani dodaci.

Kada se izabere dodatak, kretanjem do  njega strelicama gore i dolje, prikazaće se detalji tog dodatka.
Dodaci imaju određene radnje kojima možete da pristupite iz [izbornika radnji](#AddonStoreActions), kao što su instaliraj, pomoć, onemogući  i ukloni.
Dostupne radnje će se promijeniti ovisno o tome da li je dodatak instaliran ili ne, i  da li je omogućen ili onemogućen.

#### Prikazi popisa dodataka {#AddonStoreFilterStatus}

Postoje različiti prikazi za instalirane dodatke, dodatke koji se mogu ažurirati, dostupne i nekompatibilne dodatke.
Da biste promenili prikaz dodataka, promenite aktivnu karticu liste dodataka prečicom `ctrl+tab`.
Možete se takođe kretati tipkom `tab` do popisa prikaza, i kretati se kroz njih `strelicomLevo` i `strelicomDesno`.

#### Filtriranje omogućenih ili onemogućenih dodataka {#AddonStoreFilterEnabled}

Obično, instaliran dodatak je "omogućen", što znači da je pokrenut i dostupan u programu NVDA.
Ali, neki instalirani dodaci mogu biti "onemogućeni".
Ovo znači da se neće koristiti, i njihove funkcije neće biti dostupne u toku ove NVDA sesije.
Možda ste onemogućili dodatak zato što je bio u sukobu sa nekim drugim dodatkom, ili sa određenom aplikacijom.
NVDA će možda također onemogućiti određene dodatke, ako su postali nekompatibilni u toku NVDA ažuriranja; ali dobićete upozorenje ako do ovoga dođe.
Dodaci se također mogu onemogućiti ako vam neće trebati u dužem periodu, ali ne želite ih ukloniti zato što očekujete da će vam trebati u budućnosti.

Popisi instaliranih i nekompatibilnih dodataka se mogu izdvojiti na osnovi toga da li su omogućeni ili onemogućeni.
Podrazumijevano će se prikazati i omogućeni i onemogućeni dodaci.

#### Uključi nekompatibilne dodatke {#AddonStoreFilterIncompatible}

Dostupni dodaci i dodaci koji se mogu ažurirati mogu se izdvojiti tako da uključuju [nekompatibilne dodatke](#incompatibleAddonsManager) koji su dostupni za instalaciju.

#### Izdvajanje dodataka po kanalima {#AddonStoreFilterChannel}

Dodaci se mogu nuditi u četiri kanala:

* Stabilni: Programer je objavio ovaj dodatak kao testiran sa objavljenom NVDA verzijom.
* Beta: Ovom dodatku je možda neophodno dodatno testiranje, ali objavljen je i čeka na povratne informacije korisnika.
Predlaže se korisnicima koji žele rani pristup.
* Dev: Ovaj kanal se predlaže za korišćenje programerima dodataka kako bi testirali API promene koje još uvek nisu objavljene.
NVDA alfa testeri će možda morati da koriste "Dev" verzije dodataka.
* Eksterni: Dodaci instalirani iz vanjskih izvora, izvan add-on storea.

Da biste vidjeli dodatke određenog kanala, promijenite filter "kanal".

#### Pretraga dodataka {#AddonStoreFilterSearch}

Da pretražite dodatke, koristite tekstualno polje pretrage.
Možete doći do njega pritiskanjem prečice `šift+tab` iz liste dodataka.
Upišite ključnu riječ ili nekoliko riječi vrste dodatka koju tražite, a zatim  tasterom `tab` dođite do liste dodataka.
Dodaci će biti prikazani ako tekst pretrage bude pronađen u ID-u dodatka, prikazanom imenu, izdavaču, autoru ili opisu.

### Radnje dodatka {#AddonStoreActions}

Dodaci imaju određene radnje, kao što su instaliraj, pomoć, onemogući i ukloni.
Za dodatak u  listi dodataka, ovim radnjama se može pristupiti kroz izbornik koji  se otvara pritiskom `aplikacijske` tipke, `enterom`, desnim klikom ili duplim klikom na dodatak.
Ovom izborniku se takođe može pristupiti pritiskanjem gumba radnje u detaljima izabranog dodatka.

#### Instaliranje dodataka {#AddonStoreInstalling}

Ako je dodatak dostupan u NVDA add-on storeu, to ne znači da ga je proverio ili odobrio NV Access ili bilo ko drugi.
Veoma je važno da instalirate dodatke samo iz izvora kojima verujete.
Dodaci imaju neograničenu funkcionalnost u okviru programa NVDA. 
Ovo može uključiti pristup vašim ličnim podacima pa čak i celom sistemu.

Možete instalirati i ažurirati već instalirane dodatke [istraživanjem dostupnih dodataka](#AddonStoreBrowsing).
Izaberite dodatak sa kartice "dostupni dodaci" ili "dodaci koji se mogu ažurirati".
Zatim koristite radnju ažuriraj, instaliraj, ili zamijeni da biste započeli instalaciju.

Možete instalirati više dodataka odjednom.
Ovo možete učiniti tako da odaberete dodatke na kartici dostupni dodaci, potom pritisnite kontekstni izbornik na označenim dodacima i pritisnite "instaliraj označene dodatke".

Da biste instalirali dodatak koji ste preuzeli izvan add-on storea, pritisnite dugme "Instaliraj iz eksternog izvora".
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
Kao i kod instalacije, možete ukloniti više dodataka od jednom.

#### Omogući ili onemogući dodatak {#AddonStoreDisablingEnabling}

Da biste onemogućili dodatak, koristite radnju "onemogući".
Da omogućite dodatak koji je prethodno bio onemogućen, koristite radnju "omogući".
Možete da onemogućite dodatak ako status dodatka prikazuje da je  "omogućen", ili omogućite ako je "onemogućen".
Nakon svakog korištenja radnje omogući/onemogući, status dodatka će se promeniti kako bi označio šta će se desiti kada se NVDA ponovo pokrene.
Ako je dodatak prethodno bio "onemogućen", status će prikazati "omogućen nakon ponovnog pokretanja".
Ako je dodatak prethodno bio "omogućen", status će prikazati "onemogućen nakon ponovnog pokretanja".
Kao i nakon što instalirate ili uklonite dodatke, morate ponovo da pokrenete NVDA kako bi se promene primijenile.
Također možete uključiti i isključiti više dodataka odjednom tako da označite više dodataka na kartici dostupnih dodataka, a potom aktivirajte kontekstni izbornik na označenim dodacima i odaberite potrebnu radnju.

#### Recenziranje dodataka i čitanje recenzija {#AddonStoreReviews}

Možda biste htjeli pročitati recenzije drugih korisnika koji su isprobali dodatak, na primjer prije njegove instalacije ili tokom učenja kako ga koristiti.
Također, od pomoći je kada ostavite povratnu informaciju drugim korisnicima koji bi htjeli isprobati dodatak tried.
Kako biste pročitali recenzije o dodatku, odaberite ga, i kliknite na radnju "recenzije zajednice".
Ovo preusmjerava na web stranicu GitHub diskusije o tom dodatku.
Imajte na umu da ovo nije zamjena za direktnu komunikaciju sa autormia dodataka.
Umjesto toga, ova funkcija služi kako bi se korisnici mogli odlučiti da li im dodatak odgovara.

### Nekompatibilni dodaci {#incompatibleAddonsManager}

Neki stariji dodaci možda neće biti kompatibilni sa NVDA verzijom koju koristite.
Ako koristite stariju NVDA verziju, neki noviji dodaci takođe možda neće biti kompatibilni.
Pokušaj da se instalira nekompatibilan dodatak prikazaće grešku koja će objasniti zašto se dodatak smatra nekompatibilnim.

Za starije dodatke, možete promijeniti kompatibilnost na vlastiu odgovornost.
Nekompatibilni dodaci možda neće raditi uz vašu NVDA verziju, a mogu izazvati nestabilno i neočekivano ponašanje uključujući rušenja.
Možete zamijeniti kompatibilnost kada omogućite ili instalirate dodatak.
Ako nekompatibilan dodatak izaziva probleme, možete onemogućiti ili ukloniti.

Ako imate probleme pri pokretanju programa NVDA, a nedavno ste ažurirali ili instalirali neki dodatak, posebno ako je to nekompatibilan dodatak, možda ćete želeti privremeno da probate da pokrenete NVDA sa svim dodacima onemogućenim.
Da biste ponovo pokrenuli NVDA sa svim dodacima onemogućenim, izaberite odgovarajuću opciju pri izlazu iz programa NVDA.
Alternativno, koristite [opciju komandne linije](#CommandLineOptions) `--disable-addons`.

Možete istražiti dostupne nekompatibilne dodatke korištenjem [kartica dostupnih dodataka i dodataka koji se mogu ažurirati](#AddonStoreFilterStatus).
Možete istražiti instalirane nekompatibilne dodatke korišćenjem [kartice nekompatibilni dodaci](#AddonStoreFilterStatus).

## Dodatni alati {#ExtraTools}
### Preglednik log zapisa {#LogViewer}

Preglednik zapisnika koji se nalazi u Alatima u NVDA izborniku, omogućuje vam prikaz izlaza zapisnika koji je bio generiran tokom posljednje sesije kada je NVDA bio pokrenut.

Osim čitanja sadržaja, možete spremiti kopiju zapisnika, ili osvježiti preglednik kako bi se prikazao novi tekst zapisa od zadnjeg pokretanja preglednika.
Ove su radnje dostupne u izborniku preglednika zapisnika.

Datoteka koja se prikazuje u zapisniku nalazi se  u vašem računalu na lokaciji `%temp%\nvda.log`.
Zapisnik se stvara svaki puta kada je NVDA pokrenut.
Kada se to dogodi, stara datoteka zapisnika se premještava u `%temp%\nvda-old.log`.

Možete kopirati fragment datoteke zapisnika bez otvaranja zapisnika.
<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Otvori pregled zapisnika |`NVDA+f1` |Otvara zapisnik i pokazuje informaciju za razvojne programere o trenutnom objektu navigatora.|
|Kopiraj dio zapisnika u međuspremnik |`NVDA+control+shift+f1` |Kada se ovaj prečac pritisne jedamput, postavlja se početna pozicija za sadržaj zapisnika koji treba biti uhvaćen. Kada se pritisne drugi put, Kopirat će se zapisnik od startne pozicije do zadnjeg zapisa.|

<!-- KC:endInclude -->

### Preglednik govora {#SpeechViewer}

Za programere koji normalno vide ili za ljude koji prezentiraju NVDA publici normalnog vida, dostupan je plutajući prozor koji omogućuje prikaz cijelog teksta kojeg NVDA trenutačno izgovara.

Da biste omogućili preglednik govora, označite stavku "Preglednik govora" koja se nalazi u izborniku Alati u NVDA izborniku.
Maknite kvačicu sa stavke izbornika pomoću tipke enter da biste je onemogučili.

Prozor preglednika govora sadrži odabirni okvir "Prikaži preglednik govora pri pokretanju".
Ako je ova opcija označena, preglednik govora će se otvoriti kad se NVDA pokrene.
Preglednik govora se uvijek pokušava otvoriti s istim dimenzijama i pozicijom kao pri zadnjoj upotrebi.

Dok je preglednik govora aktiviran, on se stalno osvježava kako bi prikazao tekst koji se trenutačno izgovara.
Međutim, ako prelazite mišem ili kursorom unutar preglednika, NVDA će privremeno zaustaviti osvježavanje teksta, tako da možete označiti ili kopirati postojeći sadržaj.

Da biste uključili ili isključili preglednika govora s bilo kojeg mjesta, dodijelite prilagođenu gestu, koristeći [dijaloški okvir Ulazne geste](#InputGestures).

### Preglednik brajice {#BrailleViewer}

Za ljude koji vide i razvijaju aplikacije, ili pokazuju NVDA publici koja vidi, dostupan je plutajući prozor koji vam omogućuje pregled brajice i ekvivalentnog teksta jednom brajičnom znaku.
Preglednik brajice se može koristiti istovremeno kao fizički brajični redak, broj ćelija će se poklapati sa brojem ćelija na fizičkom uređaju.
Kada je preglednik brajice uključen, isti će se konstantno osvježavati kako bi se prikazale informacije kao na brajičnom retku.

Da biste uključili preglednik brajice, odaberite stavku izbornika "preglednik brajice" u podizborniku alati u NVDA izborniku.
Odznačite stavku izbornika za njegovo isključivanje.

Uobičajeno brajični redci posjeduju tipke za pomicanje u naprijed ili u nazad. Da biste omogućili pomicanje u brajičnom pregledniku najprije [pridjelite tipkovničke prečace](#InputGestures) koji će služiti za pomicanje brajičnog retka u nazad ili u naprijed.

Prozor preglednika brajice sadrži potvrdni okvir označen "pokaži brajični preglednik prilikom pokretanja".
Ako je ovo odabrano, prozob brajičnog preglednika će se otvoriti poslije pokretanja NVDA.
Preglednik brajice će se uvijek pokušati otvoriti sa istim dimenzijama i pozicijom sa kojom je bio zatvoren.

Brajični preglednik sadrži potvrdni okvir "navigacija po ćelijama pomoću prelaženja mišem", koje podrazumjevano nije označeno.
Ako je odabrano, prelaskom mišem po brajičnoj ćeliji će okinuti prečac "premjesti se na brajičnu ćeliju" za tu ćeliju.
Ovo se često koristi za premještanje kursora ili ozvršavanje akcije za neku kontrolu.
Ovo može biti korisno kako bi se testirala ispravna navigacija po brajičnim ćelijama.
Kako bi se spriječilo namjerno premještavanje na ćeliju, prečac ima zakašnjelu reakciju.
Miš se mora kretati sve dok ne pozeleni.
Na početku će miš biti žut, potom će preći u narančasto, a onda će iznenadno pozelenjeti.

Kako biste mogli otvarati brajični preglednik s bilo kojeg mjesta, molimo dodjelite ulaznu gestu koristeći [Dijaloški okvir ulaznih gesti](#InputGestures).

### Python Konzola {#PythonConsole}

NVDA Python konzola koju možemo pronaći u alatima u NVDA izborniku je alat za razvoj koji služi za otkrivanje grešaka, opći nadzor NVDA unutarnjih komponenata ili nadzor hijerarhije aplikacije.
Za više informacija, Molimo pogledajte [NVDA priručnik za programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Add-on store {#toc314}

Ovo će otvoriti [Add-on store](#AddonsManager).
Za više informacija, pročitajte opširno poglavlje: [Dodaci i Add-on store](#AddonsManager).

### Stvori prijenosnu kopiju {#CreatePortableCopy}

Ovo otvara dijaloški okvir koji služi za stvaranje prijenosne verzije iz instalacijske.
Na ovaj način, kada pokrećemo prijenosnu inačicu NVDA, u podizborniku Alati stavka izbornika će se zvati "Instaliraj NVDA na ovaj PC" umjesto "Stvori prijenosnu kopiju).

Dijaloški okvir za stvaranje prijenosne verzije  NVDA odnosno instalacije NVDA na ovaj Pc će vas pitati gdje želite stvoriti prijenosnu kopiju odnosno instalirati NVDA.

U ovom dijaloškom okviru možete uključiti ili isključiti slijedeće:

* Kopiraj trenutnu korisničku konfiguraciju (ovo uključuje datoteke u %appdata%\roaming\NVDA ili u korisničkoj konfiguraciji prijenosne verzije te uključuje tekođer dodatke i druge komponente)
* Pokreni novu prijenosnu kopiju poslije stvaranja odnosno pokreni instalacijsku verziju poslije instalacije (Pokreće NVDA poslije stvaranja prijenosne kopije ili poslije instalacijske)

### Pokreni alat za popravak Com registracija... {#RunCOMRegistrationFixingTool}

U nekim slučajevima, instalacija i deinstalacija nekih programa može odjaviti registraciju com dll datoteke.
Budući da Com sučelja poput IAccessible ovise o ispravnoj Com registraciji, mogu se pojaviti problemi ako nedostaje ispravna registracija.

Ovo se može dogoditi u slučaju uklanjanja Adobe Readera, Math Playera ili drugih programa.

Registracije koje nedostaju mogu prouzročiti probleme u internetskim preglednicima, aplikacijama za stolna računala, traci zadataka i drugim sučeljima.

Točnije govoreći, slijedeći problemi mogu biti rješeni koristeći ovaj alat:

* NVDA izgovara "nepoznato" prilikom kretanja u internetskim preglednicima poput Firefoxa, Thunderbirda itd.
* NVDA odbija prebacivanje između modusa pregleda i čitanja
* NVDA je jako spor prilikom kretanja u preglednicima prilikom korištenja načina čitanja
* te moguće druge probleme.

### Ponovo učitaj dodatke {#ReloadPlugins}

Jednom kad se ova stavka aktivira, NVDA dodaci će se ponovo učitati bez potrebe za ponovnim pokretanjem NVDA, što može biti korisno za razvojne programere.
Moduli aplikacija upravljaju time kako NVDA ulazi u interakciju sa određenim aplikacijama.
Globalni dodaci upravljaju kako NVDA upravlja sa svim aplikacijama.

Sljedeći NVDA prečaci mogu također biti korisni:
<!-- KC:beginInclude -->

| Naziv |Prečac |Opis|
|---|---|---|
|Ponovno pokreni dodatke |`NVDA+control+f3` |Ponovno pokreće globalne dodatke i module aplikacija.|
|Izgovori učitani modul aplikacija i izvršnu datoteku |`NVDA+control+f1` |Izgovara naziv modula aplikacije, i naziv izvršne datoteke aplikacije u fokusu.|

<!-- KC:endInclude -->

## Podržane govorne jedinice {#SupportedSpeechSynths}

Ovo poglavlje sadrži informacije o govornim jedinicama koje NVDA podržava.
Za detaljniji i iscrpniji popis besplatnih i komercijalnih govornih jedinica koje možete kupiti i koristiti s NVDA čitačem ekrana, pogledajte [stranicu s dodatnim glasovima](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

[eSpeak NG](https://github.com/espeak-ng/espeak-ng) je govorna jedinica ugrađena u NVDA čitaču, koja ne zahtijeva dodatne komponente niti instaliranje specijalnih upravljačkih programa.
U Windowsima 8.1, NVDA standardno koristi eSpeak NG ([Windows OneCore](#OneCore) se standardno koristi u Windowsima 10 i novijim).
Budući da je Espeak NG ugrađen u NVDA, to je dobar izbor kad se NVDA pokreće s USB sticka na drugim sustavima.

Svaki glas, koji dolazi s eSpeak NG-om, govori različitim jezikom.
Postoji preko 43 različita jezika koje eSpeak NG podržava.

Postoje još i mnoge varijante koje je moguće odabrati, kako bi se prilagodio zvuk glasa.

### Microsoft Speech API version 4 (SAPI 4) {#SAPI4}

SAPI 4 je stariji Microsoftov standard za softverske govorne jedinice.
NVDA još uvijek ovo podržava, za one korisnike koji imaju instalirane ovakve govorne jedinice..
Međutim, microsoft ga ne podržava i Microsoft ne dostavlja više te komponente.

Kad ćete koristiti ove glasove s NVDA, dostupni glasovi (kojima se može pristupiti iz [kategorije govor](#SpeechSettings) u [NVDA postavkama](#NVDASettings)  ili putem [kružne postavke govorne jedinice](#SynthSettingsRing)) će popisivati glasove svih sapi4 govornih jedinica dostupnih u sustavu.

### Microsoft Speech API version 5 (SAPI 5) {#SAPI5}

SAPI 5 je Microsoftov standard za govorne jedinice.
Puno se govornih jedinica, koje su u skladu s ovim standardom, mogu kupiti ili preuzeti od različitih kompanija i s različitih web stranica, premda će, na vašem sustavu, biti barem jedan instalirani sapi 5 glas.
Kad ćete koristiti ove glasove s NVDA, dostupni glasovi (kojima se može pristupiti iz [kategorije govor](#SpeechSettings) u [NVDA postavkama](#NVDASettings)  ili putem [kružne postavke govorne jedinice](#SynthSettingsRing)) će popisivati glasove svih sapi5 govornih jedinica dostupnih u sustavu.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Microsoft Speech Platform pruža glasove za mnoge jezike koji se uobičajeno koriste za razvoj poslužiteljski baziranih govornih aplikacija.
Ovi se glasovi mogu također koristiti uz pomoć NVDA.

Za korištenje ovih glasova, potrebno je instalirati dvije komponente:

* [Microsoft Speech Platform - Runtime (verzija 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime jezici (verzija 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Ova stranica uključuje datoteke za "tekst u govor" i za prepoznavanje govora.
 Odaberite datoteke koje sadrže glasovne podatke za željene glasove/jezike.
 Na primjer, datoteka MSSpeech_TTS_en-US_ZiraPro.msi je glas za američki engleski.

### Windows OneCore glasovi {#OneCore}

U sustavu Windows 10 ili novijim inačicama su uključeni novi glasovi poznati pod nazivom "OneCore" ili "mobile" glasovi.
Glasovi su dostupni za mnoge jezike i brži su od Microsoft glasova koji koriste Microsoft Speech API verzije 5. Bilješka prevoditelja: od Windows 10 verzije 1709, dostupan je hrvatski glas Matej.
U sustavu Windows 10 i novijim inačicama, NVDA standardno koristi Windows OneCore glasove ([[eSpeak NG](#eSpeakNG) se koristi u drugim izdanjima).

Kako biste dodali nove Windows OneCore glasove, uđite u odjeljak  "postavke govora", koji se nalazi unutar Windowsovih postavki. 
Aktivirajte opciju "Dodaj glasove" i potražite željeni jezik.
Puno jezika na ovom popisu je viševarijantno, što znači da dolaze u više varijanata izgovora.
"Engleski ujedinjeno kraljevstvo" i "australski engleski" su dvije varijante engleskog jezika.
Francuski "francuska", "Kanada" i "Švicarska" su dostupne varijante francuskog jezika.
Pronađite širi jezik poput engleskog ili francuskog, a onda pronađite jezik na popisu.
Odaberite bilo koji željeni jezik i koristite gumb "Dodaj" kako biste ga dodali.
Kada ste dodali jezik, ponovno pokrenite NVDA.

Za popis dostupnih glasova molimo pogledajte [podržani jezici i glasovi](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01).

## Podržani brajični redci {#SupportedBrailleDisplays}

Ovo poglavlje sadrži informacije o brajičnim redcima koje podržava NVDA.

### Brajični redci koji podržavaju automatsko otkrivanje brajičnih redaka u pozadini {#AutomaticDetection}

NVDA ima mogućnost automatskog prepoznavanja brajičnih redaka u pozadini, preko USB ili Bluetooth veze.
Ovo se postiže označavanjem opcije "Automatski", kao preferirani brajični redak u NVDA [dijaloškom okviru za brajične postavke](#BrailleSettings).
Ova je opcija standardno označena.

Sljedeći brajični redci podržavaju ovu funkcionalnost automatskog prepoznavanja.

* Handy Tech brajični redci
* Baum/Humanware/APH/Orbit brajični redci
* HumanWare Brailliant BI/B serije
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6 serije
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille serije
* Eurobraille Esys/Esytime/Iris brajični redci
* Nattiq nBraille brajični retci
* Seika brajična bilježnica: MiniSeika (16, 24 znakova), V6, i V6Pro (40 znakova)
* Tivomatic Caiku Albatross 46/80 displays
* Svaki brajični redak koji podržava standardni HID brajični protokol

### Brajični redci Freedom Scientific Focus/PAC Mate {#FreedomScientificFocus}

Podržani su svi Focus i PAC Mate brajični redci firme [Freedom Scientific](https://www.freedomscientific.com/), kad se spajaju putem USB ili Bluetooth veze.
Trebat ćete instalirati upravljačke programe za freedom scientific brajične retke.
Ako ih još uvijek nemate, možete ih preuzeti sa [Stranice upravljačkih programa Focus Blue](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Premda se na ovoj stranici govori o Focus Blue brajičnim redcima, upravljački programi podržavaju sve Focus i PAC Mate brajične retke.

NVDA standardno može automatski prepoznati i uspostaviti vezu s ovim brajičnim redcima putem USB-a ili bluetooth-a.
Međutim, kad se brajični redak spaja na računalo, možete odabrati "USB" ili "Bluetooth", kako biste ograničili vrstu veze koja će se koristiti.
Ovo može biti korisno, ako želite koristiti brajični redak spojen bluetooth vezom, ali ga još uvijek želite puniti putem USB priključka vašeg računala.
NVDA automatsko otkrivanje brajičnih redaka će također prepoznati brajični redak na USB-u ili Bluetooth-u.

Slijede prečaci za ovaj brajični redak s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |topRouting1 (prva ćelija na brajičnom retku)|
|Kliži po brajičnom retku naprijed |topRouting20/40/80 (zadnja ćelija na brajičnom retku)|
|Kliži po brajičnom retku natrag |lijeviAdvanceBar|
|Kliži po brajičnom retku naprijed |desniAdvanceBar|
|Mijenjaj povezanost brajičnog retka |lijeviGDFGumb+desniGDFGumb|
|Uključi ili isključi radnju lijevog kotačića |lijeviKotačićPritisni|
|Premjesti se natrag koristeći lijevi kotačić |lijeviKotačićGore|
|Premjesti se naprijed koristeći lijevi kotačić |lijeviKotačićDolje|
|Uključi ili isključi radnju desnog kotačića |desniKotačićPritisni|
|Premjesti se natrag koristeći desni kotačić |desniKotačićGore|
|Premjesti se naprijed koristeći desni kotačić |desniKotačićDolje|
|Premjesti se na brajičnu ćeliju |routing|
|Tipka šift+tabulator |brajičnaRazmaknica+točkica1+točkica2|
|Tipka tabulator |brajičnaRazmaknica+točkica4+točkica5|
|Tipka strelica gore |brajičnaRazmaknica+točkica1|
|Tipka strelica dolje |brajičnaRazmaknica+točkica4|
|Tipka kontrol+strelica lijevo |brajičnaRazmaknica+točkica2|
|Tipka kontrol+strelica desno |brajičnaRazmaknica+točkica5|
|Tipka strelica lijevo |brajičnaRazmaknica+točkica3|
|Tipka strelica desno |brajičnaRazmaknica+točkica6|
|Tipka houm |brajičnaRazmaknica+točkica1+točkica3|
|Tipka end |brajičnaRazmaknica+točkica4+točkica6|
|Tipka kontrol+houm |brajičnaRazmaknica+točkica1+točkica2+točkica3|
|Tipka kontrol+end |brajičnaRazmaknica+točkica4+točkica5+točkica6|
|Tipka alt |brajičnaRazmaknica+točkica1+točkica3+točkica4|
|Tipka alt+tabulator |brajičnaRazmaknica+točkica2+točkica3+točkica4+točkica5|
|Tipka alt+šift+tabulator |brajičnaRazmaknica+točkica1+točkica2+dočkica5+točkica6|
|Tipka windows+tabulator |brajičnaRazmaknica+točkica2+točkica3+točkica4|
|Tipka escape |brajičnaRazmaknica+točkica1+točkica5|
|Tipka windows |brajičnaRazmaknica+točkica2+točkica4+točkica5+točkica6|
|Tipka razmaknica |brajičnaRazmaknica|
|uključi i isključi tipku ctrl |razmaknica+točkica3+točkica8|
|uključi alt tipku |razmaknica+točkica6+točkica8|
|uključi windows tipku |razmaknica+točkica4+točkica8|
|uključi NVDA tipku |razmaknica+točkica5+točkica8|
|Uključi shift tipku |razmaknica+točkica7+točkica8|
|Uključi control i shift tipke |razmaknica+točkica3+točkica7+točkica8|
|Uključi alt i shift tipke |razmaknica+točkica6+točkica7+točkica8|
|Uključi windows and shift tipke |razmaknica+točkica4+točkica7+točkica8|
|Uključi NVDA i shift tipke |razmaknica+točkica5+točkica7+točkica8|
|Uključi control i alt tipke |razmaknica+točkica3+točkica6+točkica8|
|Uključi control, alt, i shift tipke |razmaknica+točkica3+točkica6+točkica7+točkica8|
|Tipka windows+d (smanji prozore svih aplikacija) |brajičnaRazmaknica+točkica1+točkica2+točkica3+točkica4+točkica5+točkica6|
|Izvijesti o trenutačnom retku |brajičnaRazmaknica+točkica1+točkica4|
|NVDA izbornik |brajičnaRazmaknica+točkica1+točkica3+točkica4+točkica5|

Za novije modele fokus brajičnih redaka koji na sebi imaju rocker bar tipke (Focus 40, Focus 80 i Focus blue):

| Naziv |Tipka|
|---|---|
|Premjesti brajični redak na prethodni redak |lijeviRockerBarGore, desniRockerBarGore|
|premjesti brajični redak na sljedeći redak |lijeviRockerBarDolje, desniRockerBarDolje|

Samo za Focus 80:

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |lijeviBumperBarGore, desniBumperBarGore|
|Kliži po brajičnom retku naprijed |lijeviBumperBarDolje, desniBumperBarDolje|

<!-- KC:endInclude -->

### Optelec Alva 6 serije/pretvornik protokola {#OptelecALVA}

ALVA BC640 i BC680 brajični redci firme [Optelec](https://www.optelec.com/) podržani su kad se spajaju putem USB ili bluetooth veze.
U drugom slučaju, možete spojiti stariji Optelec brajični redak , kao što je braille voyager, koristeći pretvornik protokola kojeg dostavlja Optelec.
Ne trebate imati specijalne upravljačke programe da biste koristili ove brajične retke.
Samo spojite brajični redak i podesite NVDA za njegovo korištenje.

Upozorenje: NVDA možda neće moći koristiti ALVA BC6 brajični redak, kad je isti spojen koristeći ALVA Bluetooth dodatak.
Ako ste uparivali vaš brajični redak koristeći taj dodatak, a NVDA ga nije prepoznao, preporučujemo uparivanje brajičnog redka koristeći standardne bluetooth postavke operacijskog sustava.

Upozorenje: iako neki od ovih brajičnih redaka imaju brajevu tipkovnicu, oni standardno barataju prijevodom brajice u tekst interno, tj. hardverski.
To znači, da se NVDA sustav brajičnog unosa ne koristi standardno (odnosno, postavka ulazne brajične tablice nema nikakvog utjecaja).
Za ALV'Ine redke na kojima je instaliran posljednji firmware, sada je moguće onemogučiti tu simulaciju tipkovnice, koristeći tipkovnički prečac.

Slijede prečaci za ovaj brajični redak s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |t1, etouch1|
|Premjesti brajični redak na prethodni redak |t2|
|Premjesti se na trenutačni fokus |t3|
|Premjesti brajični redak na sljedeći redak |t4|
|Kliži po brajičnom retku naprijed |t5, etouch 3|
|Premjesti se na brajičnu ćeliju |routing|
|Izvijesti o oblikovanju teksta pod brajičnom ćelijom |secondary routing|
|Uključi ili isključi simulaciju tipkovnice |t1+spEnter|
|Premjesti se na najgornji redak u pregledu |t1+t2|
|Premjesti se na posljednji redak u pregledu |t4+t5|
|Mijenjaj povezanost brajičnog retka |t1+t3|
|Izvijesti o naslovu |etouch2|
|Izvijesti o traci stanja |etouch4|
|Tipka šift+tabulator |sp1|
|Tipka alt |sp2, alt|
|Tipka escape |sp3|
|Tipka tabulator |sp4|
|Tipka strelica gore |spGore|
|Tipka strelica dolje |spDolje|
|Tipka strelica lijevo |spLijevo|
|Tipka strelica desno |spDesno|
|Tipka enter |spEnter, enter|
|Izvijesti o datumu/vremenu |sp2+sp3|
|NVDA izbornik |sp1+sp3|
|Tipka windows+d (smanji prozore svih aplikacija) |sp1+sp4|
|Tipka windows+b (fokusiranje područja obavijesti) |sp3+sp4|
|Tipka windows |sp1+sp2, windows|
|Tipka alt+tabulator |sp2+sp4|
|Tipka kontrol+houm |t3+spGore|
|Tipka kontrol+end |t3+spDolje|
|Tipka houm |t3+spLijevo|
|Tipka end |t3+spDesno|
|Tipka kontrol |kontrol|

<!-- KC:endInclude -->

### Handy Tech brajični redci {#HandyTech}

NVDA podržava većinu brajičnih redaka tvrtke [Handy Tech](https://www.handytech.de/) kad su spojeni putem USB ili Bluetooth veze.
Za starije brajične retke, koji se povezuju USB vezom, trebat ćete instalirati Usb upravljačke programe na vaš sustav.

Ovi brajični redci nisu podržani izravno iz NVDA, no mogu se koristiti pomoću [Handy Techovog univerzalnog upravljačkog programa](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) and NVDA add-on:

* Braillino
* Bookworm
* Modular brajični redci s pogonskim softverom verzije 1.13 ili niže. Imajte na umu, da se pogonski softver na ovim brajičnim redcima može nadograditi.

Slijede prečaci za Handy Tech brajične retke s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natragd |lijevo, gore, b3|
|Kliži po brajičnom retku naprijed |desno, dolje, b6|
|Premjesti brajični redak na prethodni redak |b4|
|Premjesti brajični redak na sljedeći redak |b5|
|Premjesti se na brajičnu ćeliju |routing|
|Tipka šift+tabulator |esc, lijeva tipka trostruke radnje gore+dolje|
|Tipka alt |b2+b4+b5|
|Tipka escape |b4+b6|
|Tipka tabulator |enter, desna tipka trostruke radnje gore+dolje|
|Tipka enter |esc+enter, lijeva+desna tipka trostruke radnje gore+dolje, joystickAction|
|Tipka strelica gore |joystickGore|
|Tipka strelica dolje |joystickDolje|
|Tipka strelica lijevo |joystickLijevo|
|Tipka strelica desno |joystickDesno|
|NVDA izbornik |b2+b4+b5+b6|
|Mijenjaj povezanost brajičnog retka |b2|
|Uključi ili isključi brajični kursor |b1|
|Mijenjaj prikaz konteksta fokusa |b7|
|Uključi ili isključi brajični unos |razmaknica+b1+b3+b4 (razmaknica+veliko slovo B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

Brajični redak, kojeg prodaje talijanska tvrtka [MDV](https://www.mdvbologna.it/) je podržan.
Ne trebate imati instalirane dodatne upravljačke programe da biste koristili ovaj brajični redak.
Samo spojite brajični redak i podesite NVDA za njegovo korištenje.

Ovaj brajični redak ne podržava funkcionalnost automatskog otkrivanja brajičnih redaka.

Slijede prečaci za ovaj brajični redak s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |LF|
|Kliži po brajičnom retku naprijed |RG|
|Premjesti brajični redak na prethodni redak |UP|
|Premjesti brajični redak na prethodni redak |DN|
|Premjesti se na brajičnu ćeliju |route|
|Tipka šift+tabulator |SLF|
|Tipka tabulator |SRG|
|Tipka alt+tabulator |SDN|
|Tipka alt+šift+tabulator |SUP|

<!-- KC:endInclude -->

### Baum/Humanware/APH/Orbit brajični redci {#Baum}

Nekoliko [Baumovih](https://www.baum.de/cms/en/), [HumanWare-ovih](https://www.humanware.com/), [APH-ovih](https://www.aph.org/) i [Orbitovih](https://www.orbitresearch.com/) brajičnih redaka su podržani kad su spojeni putem usb, bluetooth ili serijske veze.
Sljedeći brajični redci su podržani:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Neki brajični redci, koje je proizveo baum mogu također raditi, premda to nije isprobano.

Ako spajate brajične redke koji ne koriste hid preko usb veze, morate instalirati usb upravljačke programe proizvođača.
VarioUltra i Pronto! brajični redci koriste HID.
Refreshabraille i Orbit Reader 20 mogu koristiti HID ako su konfigurirani na određeni način.

 USB serijski način u Orbit Reader 20 brajičnom redku, trenutačno je podržan samo u Windows 10 i novijim inačicama operacijskog sustava.
Umjesto toga, trebali biste koristiti USB HID.

Slijede prečaci za ove brajične retke s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Ime |Tipka|
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

Za brajične retke koji imaju joystick:

| Naziv |Tipka|
|---|---|
|Tipka strelica gore |gore|
|Tipka strelica dolje |dolje|
|Tipka strelica lijevo |lijevo|
|Tipka strelica desno |desno|
|Tipka enter |odabir|

<!-- KC:endInclude -->

### Hedo ProfiLine USB {#HedoProfiLine}

Hedo ProfiLine USB brajični redak tvrtke [hedo Reha-Technik](https://www.hedo.de/) je podržan.
Prvo morate instalirati USB upravljačke programe koje je napravio proizvođač.

Ovaj brajični redak još uvijek ne podržava funkcionalnost automatskog otkrivanja brajičnih redaka.

Slijede prečaci za ovaj brajični redak s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Ime |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |K1|
|Kliži po brajičnom retku naprijed |K3|
|Premjesti brajični redak na prethodni redak |B2|
|Premjesti brajični redak na sljedeći redak |B5|
|Premjesti se na brajičnu ćeliju |routing|
|Mijenjaj povezanost brajičnog retka |K2|
|Izgovori sve |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

Hedo MobilLine USB tvrtke [hedo Reha-Technik](https://www.hedo.de/) je podržan.
Prvo morate instalirati USB upravljačke programe koje je napravio proizvođač.

Ovaj brajični redak još uvijek ne podržava funkcionalnost automatskog otkrivanja brajičnih redaka.

Slijede prečaci za ovaj brajični redak s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |K1|
|Kliži po brajičnom retku naprijed |K3|
|Premjesti brajični redak na prethodni redak |B2|
|Premjesti brajični redak na sljedeći redak |B5|
|Premjesti se na brajičnu ćeliju |routing|
|Mijenjaj povezanost brajičnog retka |K2|
|Izgovori sve |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Serije / BrailleNote Touch {#HumanWareBrailliant}

Brailliant BI i B serije brajični redci tvrtke [HumanWare](https://www.humanware.com/), uključujući BI 14, BI 32, BI 20X, BI 40, BI 40X B 80 i B 80 su podržani kad su spojeni putem USB ili bluetooth veze.
Ako brajični redak spajate putem USB veze, i protokolom postavljenim na Human Ware prvo morate instalirati USB upravljačke programe koje je napravio proizvođač.
USB upravljački programi nisu potrebni ako  je protokol postavljen na OpenBraille.

Podržani su također slijedeći dodatni uređaji, i za njih nisu potrebni dodatni upravljački programi za korištenje:

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Slijede prečaci za Brailliant BI/B i BrailleNote brajične retke s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.

#### Dodijeljeni prečaci za sve modele {#toc334}

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na prethodni redak |gore|
|Premjesti brajični redak na sljedeći redak |dolje|
|Premjesti se na brajičnu ćeliju |routing|
|Mijenjaj povezanost brajičnog retka |gore+dolje|
|Tipka strelica gore |razmaknica+točkica1|
|Tipka strelica dolje |razmaknica+točkica4|
|Tipka strelica lijevo |razmaknica+točkica3|
|Tipka strelica desno |razmaknica+točkica6|
|Tipka šift+tabulator |razmaknica+točkica1+točkica3|
|Tipka tabulator |razmaknica+točkica4+točkica6|
|Tipka alt |razmaknica+točkica1+točkica3+točkica4 (razmaknica+m)|
|Tipka escape |razmaknica+točkica1+točkica5 (razmaknica+e)|
|Tipka enter |točkica8|
|Tipka windows |razmaknica+točkica3+točkica4|
|Tipka alt+tabulator |razmaknica+točkica2+točkica3+točkica4+točkica5 (razmaknica+t)|
|NVDA Izbornik |razmaknica+točkica1+točkica3+točkica4+točkica5 (razmaknica+n)|
|Tipka windows+d (smanjuje prozore svih aplikacija) |razmaknica+točkice1+točkica4+točkica5 (razmaknica+d)|
|Izgovori sve |razmaknica+točkica1+točkica2+točkica3+točkica4+točkica5+točkica6|

<!-- KC:endInclude -->

#### Dodijeljeni prečaci za Brailliant BI 32, BI 40 and B 80 {#toc335}

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|NVDA Izbornik |c1+c3+c4+c5 (command n)|
|Tipka windows+d (smanjuje prozore svih aplikacija) |c1+c4+c5 (command d)|
|Izgovori sve |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Dodijeljeni prečaci za Brailliant BI 14 {#toc336}

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Tipka strelica gore |joystick gore|
|Tipka strelica dolje |joystick dolje|
|Tipka strelica lijevo |joystick lijevo|
|Tipka strelica desno |joystick desno|
|Tipka enter |joystick akcija|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille serije {#Hims}

NVDA podržava Braille Sense, Braille EDGE, Smart Beetle i Sync Braille brajične retke tvrtke [Hims](https://www.hims-inc.com/) kad su spojeni preko USB ili bluetooth veze. 
Ako spajate brajični redak preko Usb priključka, trebat ćete instalirati [USB upravljake programe od Himsa](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) u vaš sustav.

Slijede prečaci za ove brajične retke s NVDA čitačem.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Premjesti se na brajičnu ćeliju |routing|
|Kliži po brajičnom retku natrag |lijevaStranaKlizačGore, desnaStranaKlizačGore, lijevaStranaKlizač|
|Kliži po brajičnom retku naprijed |lijevaStranaKlizačDolje, desnaStranaKlizačDolje, desnaStranaKlizač|
|Premjesti brajični redak na prethodni redak |lijevaStranaKlizačGore+desnaStranaKlizačGore|
|Premjesti brajični redak na sljedeći redak |lijevaStranaKlizačDolje+desnaStranaKlizačDolje|
|Premjesti se na prethodni redak u pregledu |desnaStranaStrelicaGore|
|Premjesti se na sljedeći redak u pregledu |desnaStranaStrelicaDolje|
|Premjesti se na prethodni znak u pregledu |desnaStranaStrelicaLijevo|
|Premjesti se na sljedeći znak u pregledu |desnaStranaStrelicaDesno|
|Premjesti se na trenutačni fokus |lijevaStranaKlizačGore+lijevaStranaKlizačDolje, desnaStranaKlizačGore+desnaStranaKlizačDolje, lijevaStranaKlizač+desnaStranaKlizač|
|Tipka kontrol |smartbeetle:f1, brailleedge:f3|
|Tipka windows |f7, smartbeetle:f2|
|Tipka alt |točkica1+točkica3+točkica4+razmaknica, f2, smartbeetle:f3, brailleedge:f4|
|Tipka šift |f5|
|Tipka insert |točkica2+točkica4+razmaknica, f6|
|Aplikacijska tipka |točkica1+točkica2+točkica3+točkica4+razmaknica, f8|
|Tipka capsLock |točkica1+točkica3+točkica6+razmaknica|
|Tipka tabulator |točkica4+točkica5+razmaknica, f3, brailleedge:f2|
|Tipka šift+alt+tabulator |f2+f3+f1|
|Tipka alt+tabulator |f2+f3|
|Tipka šift+tabulator |točkica1+točkica2+razmaknica|
|Tipka end |točkica4+točkica6+razmaknica|
|Tipka kontrol+end |točkica4+točkica5+točkica6+razmaknica|
|Tipka houm |točkica1+točkica3+razmaknica, smartbeetle:f4|
|Tipka kontrol+houm |točkica1+točkica2+točkica3+razmaknica|
|Tipka alt+f4 |točkica1+točkica3+točkica5+točkica6+razmaknica|
|Tipka strelica lijevo |točkica3+razmaknica, lijevaStranaStrelicaLijevo|
|Tipka kontrol+šift+strelica lijevo |točkica2+točkica8+razmaknica+f1|
|Tipka kontrol+strelica lijevo |točkica2+razmaknica|
|Tipka šift+alt+strelica lijevo |točkica2+točkica7+f1|
|`Tipka alt+strelica lijevo` |`točkica2+točkica7+razmak`|
|Tipka strelica lijevo |točkica6+razmaknica, lijevaStranaStrelicaDesno|
|Tipka kontrol+šift+strelica lijevo |točkica5+točkica8+razmaknica+f1|
|Tipka kontrol+strelica desno |točkica5+razmaknica|
|Tipka šift+alt+strelica desno |točkica5+točkica7+f1|
|`Tipka alt+strelica desno` |točkica5+točkica7+razmak|
|Tipka pejdž ap |točkica1+točkica2+točkica6+razmaknica|
|Tipka kontrol+pejdž ap key |točkica1+točkica2+točkica6+točkica8+razmaknica|
|Tipka strelica gore |točkica1+razmaknica, lijevaStranaStrelicaGore|
|Tipka kontrol+šift+strelica gore |točkica2+točkica3+točkica8+razmaknica+f1|
|Tipka kontrol+strelica gore |točkica2+točkica3+razmaknica|
|Tipka šift+alt+strelica gore |točkica2+točkica3+točkica7+f1|
|`Tipka alt+strelica gore` |`točkica2+točkica3+točkica7+razmak`|
|Tipka šift+strelica gore |lijevaStranaKlizačDolje+razmaknica|
|Tipka pejdž daun |točkica3+točkica4+točkica5+razmaknica|
|Tipka kontrol+pejdž daun |točkica3+točkica4+točkica5+točkica8+razmaknica|
|Tipka strelica dolje |točkica4+razmaknica, lijevaStranaStrelicaDolje|
|Tipka kontrol+šift+strelica dolje |točkica5+točkica6+točkica8+razmaknica+f1|
|Tipka kontrol+strelica dolje |točkica5+točkica6+razmaknica|
|Tipka šift+alt+strelica dolje |točkica5+točkica6+točkica7+f1|
|++Tipka alt+strelica dolje++ |točkica5+točkica6+točkica7+razmak|
|Tipka šift+strelica dolje |razmaknica+desnaStranaKlizačDolje|
|Tipka escape |točkica1+točkica5+razmaknica, f4, brailleedge:f1|
|Tipka dilit |točkica1+točkica3+točkica5+razmaknica, točkica1+točkica4+točkica5+razmaknica|
|Tipka f1 |točkica1+točkica2+točkica5+razmaknica|
|Tipka f3 |točkica1+točkica4+točkica8+razmaknica|
|Tipka f4 |točkica7+f3|
|Tipka windows+b |točkica1+točkica2+f1|
|Tipka windows+d |točkica1+točkica4+točkica5+f1|
|Tipka kontrol+insert |smartbeetle:f1+desnaStranaKlizač|
|Tipka alt+insert |smartbeetle:f3+desnaStranaKlizač|

<!-- KC:endInclude -->

### Seika brajični redci {#Seika}

Slijedeći Seika brajični redci tvrtke Nippon Telesoft su podržani u dvije grupe sa različitim funkcijama:

* [Seika verzija 3, 4, i 5 (40 znakova), Seika80 (80 znakova)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 znakova), V6, i V6Pro (40 znakova)](#SeikaNotetaker)

Možete pronaći više informacija o ovim brajičnim redcima [na njihovoj stranici demonstracije i preuzimanja upravljačkih programa](https://en.seika-braille.com/down/index.html).

#### Seika verzija 3, 4, i 5 (40 znakova), Seika80 (80 znakova) {#SeikaBrailleDisplays}

* Ovi brajični redci još ne podržavaju funkcionalnost automatskog otkrivanja brajičnih redaka u pozadini.
* Odaberite "Seika brajični redci" za ručnu konfiguraciju.
* Prije korištenja Seika v3/4/5/80 brajičnog redka, morate instalirati upravljačke programe za uređaj.
Upravljačke programe [pruža proizvođač](https://en.seika-braille.com/down/index.html).

Slijede tipkovnički prečaci za Seika brajični redak.
Smještaj ovih tipki potražite u dokumentaciji brajičnog retka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na prethodni redak |b3|
|Premjesti brajični redak na sljedeći redak |b4|
|Mijenjaj povezanost brajičnog retka |b5|
|Izgovori sve |b6|
|Tipka tabulator |b1|
|Tipka šift+tabulator |b2|
|Tipka alt+tabulator |b1+b2|
|NVDA Izbornik |lijevo+desno|
|Premjesti se na brajičnu ćeliju |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 znakova), V6, i V6Pro (40 znakova) {#SeikaNotetaker}

* NVDA automatsko otkrivanje brajičnih redaka je podržano koristeći USB i Bluetooth.
* Odaberite "Seika brajična elektronička bilježnica" ili "automatski" kako biste konfigurirali.
* Nisu potrebni dodatni upravljački programi kako bi se koristila Seika brajična elektronička bilježnica.

Slijede prečaci za Seika brajičnu elektroničku bilježnicu.
Za opis i razmještaj tih tipki na brajičnom redku, molimo pogledajte dokumentaciju brajičnog redka.
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Prebaci brajični redak u nazad |left|
|Prebaci brajični redak u naprijed |right|
|Čitaj sve |Razmaknica+Backspace|
|NVDA izbornik |Left+Right|
|Premjesti brajični redak na prethodni redak |LJ up|
|Premjesti brajični redak na slijedeći redak |LJ down|
|Prebaci povezivanje brajičnog redka na |LJ center|
|tab |LJ right|
|shift+tab |LJ left|
|Strelica gore |RJ up|
|Strelica dolje |RJ down|
|strelica lijevo |RJ left|
|Strelica desno |RJ right|
|Prebaci se na brajičnu ćeliju |routing|
|shift+strelica gore |razmaknica+RJ up, Backspace+RJ up|
|shift+strelica dolje |razmaknica+RJ down, Backspace+RJ down|
|shift+strelica lijevo |razmaknica+RJ left, Backspace+RJ left|
|shift+strelica desno |razmaknica+RJ right, Backspace+RJ right|
|enter |RJ center, točkica8|
|escape |razmaknica+RJ center|
|windows tipka |Backspace+RJ center|
|razmaknica |razmaknica, Backspace|
|backspace |točkica7|
|pageup |razmaknica+LJ right|
|pagedown |razmaknica+LJ left|
|home |razmaknica+LJ up|
|end |razmaknica+LJ down|
|control+home |backspace+LJ up|
|control+end |backspace+LJ down|

### Papenmeier BRAILLEX noviji modeli {#Papenmeier}

Sljedeći brajični redci su podržani: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB i bluetooth)
* BRAILLEX Live 20, BRAILLEX Live i BRAILLEX Live Plus (USB i bluetooth)

Ovaj brajični redak još uvijek ne podržava funkcionalnost automatskog otkrivanja brajičnih redaka.
Postoji opcija u upravljačkom programu redka koja može prouzročiti problem prilikom učitavanja redka.
Molimo pokušajte slijedeće:

1. Uvjerite se da imate instalirane [posljednje upravljačke programe](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Otvorite upravitelj uređaja sustava Windows.
1. Pronađite "USB kontrolere" ili "USB uređaje".
1. Odaberite "Papenmeier Braillex USB Device".
1. Otvorite svojstva i prebacite se na karticu "napredno".
Ponekad se kartica "Napredno" ne pojavljuje.
Ako je to slučaj, odspojite brajični redak od računala, isključite NVDA, pričekajte trenutak i ponovno spojite brajični redak.
Ako je potrebno, ponovite to 4 ili 5 puta.
Ako se kartica "napredno" još uvijek ne pojavljuje, molimo ponovno pokrenite računalo.
1. Onemogućite opciju "učitaj VCP".

Većina uređaja ima tipku Easy Access Bar (EAB) koja omogućuje brzo i intuitivno rukovanje.
EAB može biti premještan u četiri smjera gdje u glavnom svaki smjer ima dva preklopnika.
C i live serije su jedina iznimka od ovog pravila.

C-serija i drugi brajični redci imaju dva reda routing tipki gdje se gornji red koristi za izvještavanje o oblikovanju teksta.
Kad držite pritisnutu jednu od gornjih routing tipki i pritiščući EAB na uređajima c-serije emulira stanje drugog preklopnika.
Brajični redci Live serije imaju samo jedan red routing tipki i EAB ima samo jedan korak po smjeru.
Drugi se korak može izvesti tako da pritisnete jednu od routing tipki i EAB u odgovarajućem smjeru.
Kad pritisnete i držite gornje, doljnje, desne i lijeve tipke (ili EAB) uzrokuje ponavljanje dodjeljene akcije.

Sljedeće tipke su općenito dostupne na ovim brajičnim redcima:

| Naziv |Tipka|
|---|---|
|l1 |Lijeva prednja tipka|
|l2 |Lijeva stražnja tipka|
|r1 |Desna prednja tipka|
|r2 |Desna stražnja tipka|
|up |Jedan korak gore|
|up2 |Dva koraka gore|
|left |Jedan korak lijevo|
|left2 |Dva koraka lijevo|
|right |Jedan korak desno|
|right2 |Dva koraka desno|
|dn |Jedan korak dolje|
|dn2 |Dva koraka dolje|

Slijede Papenmeier prečaci za NVDA čitača:
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na prethodni redak |gore|
|Premjesti brajični redak na sljedeći redak |dolje|
|Premjesti se na brajičnu ćeliju |routing|
|Izvijesti o trenutačni znak u pregledu |l1|
|Aktiviraj trenutačni navigacijski objekt |l2|
|Mijenjaj povezanost brajičnog retka |r2|
|Izvijesti o naslovu |l1+gore|
|Izvijesti o traci stanja |l2+dolje|
|Premjesti se na sadržavajući objekt |gore2|
|Premjesti se na prvi sadržavajući objekt |dolje2|
|Premjesti se na prethodni objekt |lijevo2|
|Premjesti se na sljedeći objekt |desno2|
|Izvijesti o oblikovanju teksta pod brajičnom ćelijom |Gornji red routing tipki|

<!-- KC:endInclude -->

Trio model ima četiri dodatne tipke koje se nalaze na prednjoj strani brajične tipkovnice.
To su sljedeće tipke (redoslijed s lijeva na desno):

* lijeva palčana tipka (lt)
* razmaknica
* razmaknica
* desna palčana tipka (rt)

Trenutačno se ne koristi desna palčana tipka.
Obje srednje tipke su mapirane na razmaknicu.

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Tipka escape |razmaknica s točkicom 7|
|Tipka strelica gore |razmaknica s točkicom 2|
|Tipka strelica lijevo |razmaknica s točkicom 1|
|Tipka strelica desno |razmaknica s točkicom 4|
|Tipka strelica dolje |razmaknica s točkicom 5|
|Tipka kontrol |lijeva palčana tipka+točkica2|
|Tipka alt |lijeva palčana tipka+točkica3|
|Tipka kontrol+escape |razmaknica s točkicama 1 2 3 4 5 6|
|Tipka tabulator |razmaknica s točkicama 3 7|

<!-- KC:endInclude  -->

### Papenmeier Braille BRAILLEX stariji modeli {#PapenmeierOld}

Sljedeći su brajični redci podržani: 

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Imajte na umu da se ovi brajični redci mogu spojiti samo preko serijskog priključka.
Zbog ovoga, ovi brajični redci ne podržavaju automatsko otkrivanje brajičnih redaka.
Poslije izbora brajičnog retka, morat ćete odabrati priključak u [dijaloškom okviru odabir brajičnog retka](#SelectBrailleDisplay).

Neki od ovih uređaja imaju Easy Access Bar (EAB) tipku koja omogućuje intuitivno i brzo rukovanje.
EAB se može pomicati u četiri smjera gdje uglavnom svaki smjer ima dva preklopnika.
Kad pritišćete i držite gornju, doljnju, desnu i lijevu tipku (ili EAB) Prouzrokuje ponavljanje dodjeljene akcije.
Stariji uređaji nemaju EAB; tipke s prednje strane se koriste umjesto EAB.

Na brajičnim redcima su općenito dostupne sljedeće tipke:

| Naziv |Tipka|
|---|---|
|l1 |Lijeva prednja tipka|
|l2 |Lijeva stražnja tipka|
|r1 |Desna prednja tipka|
|r2 |Desna stražnja tipka|
|up |Jedan korak gore|
|up2 |Dva koraka gore|
|left |Jedan korak lijevo|
|left2 |Dva koraka lijevo|
|right |Jedan korak desno|
|right2 |Dva koraka desno|
|dn |Jedan korak dolje|
|dn2 |Dva koraka dolje|

Slijede Papenmeierovi dodjeljeni prečaci za korištenje s NVDA:

<!-- KC:beginInclude -->
Uređaji koji imaju EAB:

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na prethodni redak |gore|
|Premjesti brajični redak na prethodni redak |dolje|
|Premjesti se na brajičnu ćeliju |routing|
|Izgovori trenutačni znak u pregledu |l1|
|Aktiviraj trenutačni navigacijski objekt |l2|
|Izvijesti o naslovu |l1gore|
|Izvijesti o traci stanja |l2dolje|
|Premjesti se na sadržavajući objekt |gore2|
|Premjesti se na prvi sadržavajući objekt |dolje2|
|Premjesti se na sljedeći objekt |desno2|
|Premjesti se na prethodni objekt |lijevo2|
|Izvijesti o oblikovanju teksta pod brajičnom ćelijom |gornji red routing tipki|

BRAILLEX Tiny:

| Naziv |Tipka|
|---|---|
|Izgovori trenutačni znak u pregledu |l1|
|Aktiviraj trenutačni navigacijski objekt |l2|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na prethodni redak |gore|
|Premjesti brajični redak na sljedeći redak |dolje|
|Mijenjaj povezanost brajičnog retka |r2|
|Premjesti se na sadržavajući objekt |r1+gore|
|Premjesti se na prvi sadržavajući objekt |r1+dolje|
|Premjesti se na prethodni objekt |r1+lijevo|
|Premjesti se na sljedeći objekt |r1+desno|
|Izvijesti o oblikovanju teksta pod brajičnom ćelijom |gornji red routing tipki|
|Izvijesti o naslovu |l1+gore|
|Izvijesti o traci stanja |l2+dolje|

BRAILLEX 2D Screen:

| Naziv |Tipka|
|---|---|
|Izgovori trenutačni znak u pregledu |l1|
|Aktiviraj trenutačni navigacijski objekt |l2|
|Mijenjaj povezanost brajičnog retka |r2|
|Izvijesti o oblikovanju teksta ispod brajične ćelije |gornji red routing tipki|
|Premjesti brajični redak na prethodni redak |gore|
|Kliži po brajičnom retku natrag |lijevo|
|Kliži po brajičnom retku naprijed |desno|
|Premjesti brajični redak na sljedeći redak |dolje|
|Premjesti se na sljedeći objekt |lijevo2|
|Premjesti se na sadržavajući objekt |gore2|
|Premjesti se na prvi sadržavajući objekt |dolje2|
|Premjesti se na prethodni objekt |desno2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA podržava BrailleNote elektroničke bilježnice tvrtke [Humanware](https://www.humanware.com) Kad se ponašaju kao brajični redci za čitače ekrana.
Sljedeći modeli su podržani:

* BrailleNote Classic (samo serijska veza)
* BrailleNote PK (serijska i bluetooth veza)
* BrailleNote MPower (Serijska i Bluetooth veza)
* BrailleNote Apex (USB i bluetooth veza)

Za BrailleNote Touch, pogledajte poglavlje [Brailliant BI serije / BrailleNote Touch](HumanWareBrailliant).

Izuzimajući BrailleNote PK, braille (BT) i QWERTY (QT) tipkovnice su podržane.
Za BrailleNote QT, emulacija tipkovnice osobnog računala nije podržana.
Moguće je također upisivanje brajice koristeći qwerty tipkovnicu.
Pogledajte poglavlje brajični terminal Braillenote korisničkih uputa za više informacija.

Ako vaš uređaj podržava više od jedne vrste veze, kad spajate vaš BrailleNote za korištenje s NVDA, morate postaviti priključak brajičnog terminala u postavkama brajičnog terminala.
Za više informacija, pogledajte korisničke upute za BrailleNote elektroničku bilježnicu.
U NVDA ćete možda trebati odabrati priključak u [dijaloškom okviru odabir brajičnog retka](#SelectBrailleDisplay).
Ako povezujete uređaj putem USB ili bluetooth veze, možete postaviti priključak na "Automatski", "USB" ili "Bluetooth", ovisno o dostupnim opcijama.
Ako za spajanje koristite serijski priključak (ili pretvarač sa serijskog priključka na USB) ili se ne pojavljuje niti jedna od prethodnih opcija, morate točno odabrati komunikacijski priključak koji će se koristiti pri komunikaciji s uređajem.

Prije spajanja vašeg BrailleNote Apex uz pomoć njegovog Usb klijenta, morate instalirati upravljačke programe koje je napravila tvrtka Human Ware.

Na BrailleNote Apex BT, možete koristiti kotačić koji se nalazi između točkica 1 i 4 za različite NVDA prečace.
Kotačić se sastoji od četiri usmjerene točke, centralnog gumba za klikanje i kotačića koji se može vrtiti u smjeru ili obrnuto od smjera kazaljke na satu.

Slijede BrailleNote prečaci za NVDA.
Smještaj ovih tipki potražite u BrailleNote dokumentaciji.

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |natrag|
|Kliži po brajičnom retku naprijed |naprijed|
|Premjesti brajični redak na prethodni redak |prethodno|
|Premjesti brajični redak na sljedeći redak |sljedeće|
|Premjesti se na brajičnu ćeliju |routing|
|NVDA izbornik |razmaknica+točkica1+točkica3+točkica4+točkica5 (razmaknica+n)|
|Mijenjaj povezanost brajičnog retka |prethodno+sljedeće|
|Tipka strelica gore |razmaknica+točkica1|
|Tipka strelica golje |razmaknica+točkica4|
|Tipka strelica lijevo |razmaknica+točkica3|
|Tipka strelica desno |razmaknica+točkica6|
|Tipka pejdž ap |razmaknica+točkica1+točkica3|
|Tipka pejdž daun |razmaknica+točkica4+točkica6|
|Tipka houm |razmaknica+točkica1+točkica2|
|Tipka end |razmaknica+točkica4+točkica5|
|Tipke kontrol+houm |razmaknica+točkica1+točkica2+točkica3|
|Tipke kontrol+end |razmaknica+točkica4+točkica5+točkica6|
|Razmaknica |razmaknica|
|Tipka enter |razmaknica+točkica8|
|Tipka backspace |razmaknica+točkica7|
|Tipka tabulator |razmaknica+točkica2+točkica3+točkica4+točkica5 (razmaknica+t)|
|Tipke šift+tabulator |razmaknica+točkica1+točkica2+točkica5+točkica6|
|Tipka windows |razmaknica+točkica2+točkica4+točkica5+točkica6 (razmaknica+w)|
|Tipka alt |razmaknica+točkica1+točkica3+točkica4 (razmaknica+m)|
|Uključi i isključi pomoć pri unosu |razmaknica+točkica2+točkica3+točkica6 (razmaknica+malo slovo h)|

Slijede prečaci za BrailleNote QT kad nije u modusu brajičnog unosa.

| Naziv |Tipka|
|---|---|
|NVDA izbornik |read+n|
|Tipka strelica gore |strelica gore|
|Tipka strelica dolje |strelica dolje|
|Tipka strelica lijevo |strelica lijevo||
|Tipka strelica desno |strelica desno|
|Tipka pejdž ap |funkcija+strelica gore|
|Tipka pejdž daun |funkcija+strelica dolje|
|Tipka houm |funkcija+strelica lijevo|
|Tipka end |funkcija+strelica desno|
|Tipke kontrol+houm |read+t|
|Tipke kontrol+end |read+b|
|Tipka enter |enter|
|Tipka backspace |backspace|
|Tipka tabulator |tabulator|
|Tipke šift+tabulator |šift+tabulator|
|Tipka windows |read+w|
|Tipka alt |read+m|
|Uključi i isključi pomoć pri unosu |read+1|

Slijede prečaci dodijeljeni kotačiću za klizanje:

| Naziv |Tipka|
|---|---|
|Tipka strelica gore |strelica gore|
|Tipka strelica dolje |strelica dolje|
|Tipka strelica lijevo |strelica lijevo|
|Tipka strelica desno |strelica desno|
|Tipka enter |srednji gumb|
|Tipka tabulator |okreći kotačić u smjeru kazaljke na satu|
|Tipke šift+tabulator |okreći kotačić u obrnutom smjeru od kazaljke na satu|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA podržava EcoBraille brajične retke koje proizvodi [ONCE](https://www.once.es/).
Sljedeći modeli su podržani:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

U NVDA čitaču možete odabrati priključak na koji je spojen brajični redak u dijaloškom okviru [Odaberi brajični redak](#SelectBrailleDisplay).
NVDA ne podržava funkcionalnost automatskog otkrivanja brajičnih redaka za ovaj brajični redak.

Slijede prečaci za EcoBraille brajične retke.
Smještaj ovih tipki potražite u [EcoBraille dokumentaciji](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/).

<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |T2|
|Kliži po brajičnom retku naprijed |T4|
|Premjesti brajični redak na prethodni redak |T1|
|Premjesti brajični redak na sljedeći redak |T5|
|Premjesti se na brajičnu ćeliju |Routing|
|Aktiviraj trenutačni navigacijski objekt |T3|
|Prebaci na sljedeći modus pregleda |F1|
|Premjesti se na sadržavajući objekt |F2|
|Prebaci na prethodni modus pregleda |F3|
|Premjesti se na prethodni objekt |F4|
|Izvijesti o trenutačnom objektu |F5|
|Premjesti se na sljedeći objekt |F6|
|Premjesti se na objekt fokusa |F7|
|Premjesti se na prvi sadržavajući objekt |F8|
|Premjesti fokus sustava ili kursor na trenutačnu poziciju pregleda |F9|
|Izvijesti o poziciji preglednog kursora |F0|
|Mijenjaj povezanost brajičnog retka |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

Uređaj SuperBraille, pretežno dostupan na Tajvanu, može se spajati putem serijskog ili USB priključka.
Budući da SuperBraille nema nikakvih fizičkih tipki za pisanje ili gumbova za klizanje, svi znakovi se moraju unositi pomoću standardne tipkovnice računala.
Zbog toga, te kako bi se zadržala kompatibilnost s drugim čitačima ekrana na Tajvanu, dodana su dva tipkovnička prečaca za klizanje po brajičnom retku:
<!-- KC:beginInclude -->

| Naziv |Tipka|
|---|---|
|Kliži po brajičnom retku natrag |numMinus|
|Kliži po brajičnom retku naprijed |numPlus|

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

| Naziv |Prečac|
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

[BRLTTY](https://www.brltty.app/) je program koji se može koristiti za podršku puno više brajičnih redaka.
Da biste ga mogli koristiti, morate instalirati [BRLTTY za Windows](https://www.brltty.app/download.html).
Trebali biste preuzeti i instalirati aktualnu verziju instalacijskog paketa, koji se na primjer zove, brltty-win-4.2-2.exe.
Kad podešavate brajični redak i priključak za korištenje, budite sigurni da strogo pratite upute, pogotovo ako koristite USB brajični redak i ako već imate instalirane upravljačke programe proizvođača.

Za brajične retke koji imaju brajičnu tipkovnicu, BRLTTY trenutačno samostalno rukuje brajičnim unosom.
Stoga, postavka za ulaznu brajičnu tablicu nije bitna.

BRLTTY ne sudjeluje u automatskom otkrivanju brajičnih redaka.

Slijede BRLTTY prečaci za NVDA.
Pogledajte [BRLTTY tablice tipkovničkih prečaca](https://brltty.app/doc/KeyBindings/) za više informacija o tome kako su BRLTTY prečaci dodijeljeni kontrolama na brajičnim redcima.
<!-- KC:beginInclude -->

| Naziv |BRLTTY naredba|
|---|---|
|Kliži po brajičnom retku natrag |fwinlt (idi jedan prozor u lijevo)|
|Kliži po brajičnom retku naprijed |fwinrt (idi jedan prozor u desno)|
|Premjesti brajični redak na prethodni redak |lnup (idi jedan redak gore)|
|Premjesti brajični redak na sljedeći redak |lndn (idi jedan redak dolje)|
|Premjesti se na brajičnu ćeliju |route (dovedi kursor na znak)|
|Uključi pomoć tipkovnice |learn (uključuje način učenja tipkovnice)|
|Otvori NVDA izbornik |prefmenu (otvara izlazi iz izbornika postavki)|
|Vrati konfiguraciju |prefload (vraća postavke s diska)|
|Spremi konfiguraciju |prefsave (sprema postavke na disk)|
|Čitaj vrijeme |time (pokazuje trenutni datum i vrijeme)|
|Čitaj redaj gdje se nalazi pregledni kursor |say_line (izgovara trenutni redak)|
|Čitaj sve koristeći pregledni kursor |say_below (izgovara od trenutnog redka do kraja)|

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
|Prebacuje između modusa govora |`atribut2+atribut4`|
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

### Standardni HID brajični retci {#HIDBraille}

Ovo je eksperimentalni upravljački program za novu standardnu HID specifikaciju, oko koje su se dogovorili Microsoft, Google, Apple i neke druge tvrtke koje proizvode asistivnu tehnologiju u 2018. godini uključujući i NV Access. 
Nadamo se da će bilo koji model brajičnog redka kojeg će proizvesti bilo koji proizvođač  koristiti ovaj standardni protokol, što će ukloniti potrebu pisanja upravljačkih programa koji su specifični za bilo kojeg proizvođača.

NVDA funkcija automatskog prepoznavanja brajičnih redaka će prepoznavati bilo koji brajični redak koji podržava ovaj protokol.

Slijede dodjeljeni prečaci za te brajične retke.
<!-- KC:beginInclude -->

| Naziv |prečac|
|---|---|
|premještanje brajičnog retka u natrag |pan left ili rocker up|
|Premještanje brajičnog redka u naprijed |pan right ili rocker down|
|premjesti se na brajičnu ćeliju |routing set 1||
|prebacuje prikazivanje fokusa |up+down|
|Strelica gore |joystick up, dpad up ili razmaknica+točkica1|
|strelica dolje |joystick down, dpad down ili razmaknica+točkica4|
|strelica lijevo |razmaknica+točkica3, joystick left  ili dpad left|
|strelica desno |razmaknica+točkica6, joystick right ili dpad right|
|shift+tab tipka |razmak+točkica1+točkica3|
|Tab |razmak+točkica4+točkica6|
|Alt |razmak+točkica1+točkica3+točkica4 (razmak+m)|
|escape |razmak+točkica1+točkica5 (razmak+e)|
|enter |točkica8, joystick center ili dpad center|
|windows tipka |razmak+točkica3+točkica4|
|alt+tab |razmak+točkica2+točkica3+točkica4+točkica5 (razmak+t)|
|NVDA izbornk |razmak+točkica1+točkica3+točkica4+točkica5 (razmak+n)|
|windows+d tipka (minimizira sve programe) |razmak+točkica1+točkica4+točkica5 (razmak+d)|
|Čitaj sve |razmak+točkica1+točkica2+točkica3+točkica4+točkica5+točkica6|

<!-- KC:endInclude -->

## Teme za napredne korisnike {#AdvancedTopics}
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
* Učitavanje prilagođenih mapa konfiguracije korištenjem [opcije `-c` u naredbenom redku](#CommandLineOptions)
* Ažuriranje programa NVDA i pravljenje prenosnih kopija
* [Prodavnicu dodataka](#AddonsManager)
* [NVDA Python konzolu](#PythonConsole)
* [Preglednik dnevnika](#LogViewer) i evidentiranje u dnevniku
* [Pregled brajice](#BrailleViewer) i [Pregled govora](#SpeechViewer)
* Otvaranje eksternih dokumenata iz NVDA menija, kao što su korisničko uputstvo ili datoteku saradnika.

Instalirane kopije programa NVDA čuvaju podešavanja uključujući dodatke u `%APPDATA%\nvda`.
Da biste sprečili NVDA korisnike da direktno izmene podešavanja ili dodatke, korisnički pristup ovom folderu se takođe mora ograničiti.

Siguran način je neefektivan za prijenosne kopije NVDA.
Ovo ograničenje se primjenjuje i na privremenu kopiju koju porećete kada instalirate NVDA.
U sigurnim okruženjima, korisnik koji može pokrenuti prijenosnu izvršnu datoteku je isti rizik za sigurnost neovisno o sigurnom načinu.
Očekuje se da administratori sustava ograničavaju pokretanje neautoriziranog softvera u svojim sustavima, uključujući prijenosne kopije NVDA.

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

### Opcije naredbenog retka {#CommandLineOptions}

Tijekom pokretanja, NVDA može prihvatiti jednu ili više opcija, čime se mijenja ponašanje čitača.
Možete proslijediti onoliko opcija koliko trebate.
Ove se opcije mogu proslijediti kad se NVDA pokreće putem prečaca na radnoj površini (u postavkama prečaca), iz dijaloškog okvira "Pokreni" (izbornik Start>Pokreni ili prečac Windows+r) ili iz Windowsovog naredbenog retka.
Opcije moraju biti odvojene od imena NVDA izvršne datoteke i od drugih opcija razmacima.
Na primjer, korisna opcija je --disable-addons, koja govori NVDA čitaču da se pokrene bez dodataka.
Ovo vam pomaže otkriti je li problem nastao zbog dodatka i omogućuje oporavljanje od ozbiljnih problema koje dodaci mogu prouzročiti.

Na primjer, iz trenutačno pokrenute kopije NVDA čitača možete izaći upisom sljedeće opcije u dijaloški okvir "Pokreni":

    nvda -q

Neke opcije naredbenog retka imaju dugu i kratku verziju, dok neke od njih imaju samo dugu verziju.
Za opcije koje imaju kratku verziju, možete ih kombinirati na sljedeće načine:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Ovo će pokrenuti NVDA sa zvukom za pokretanje i isključenim porukama, i sa određenom konfiguracijom|
|nvda -mc CONFIGPATH --disable-addons |Ista opcija kao i prethodna, ali s deaktiviranim dodacima|

Neke opcije naredbenog retka prihvaćaju dodatne parametre; npr. koliko će zapisivanje u zapisnik biti detaljno ili staza do korisničke konfiguracijske mape.
Ovi parametri trebaju biti smješteni poslije opcije, odvojene razmakom ako se koristi kratka verzija ili znakom jednakosti (=) kad se koristi duga verzija; npr:
+|| . {.hideHeaderRow} | . |

|nvda -l 10 |proslijeđuje NVDA informaciju da se mora pokrenuti s razinom loga postavljenom kao debug|
|nvda --log-file=c:\nvda.log |određuje put do NVDA datoteke zapisnika na sljedeću vrijednost c:\nvda.log|
|nvda --log-level=20 -f c:\nvda.log |proslijeđuje naredbu da se NVDA pokreće s razinom loga info i da zapisuje svoj log u c:\nvda.log|

Slijede opcije naredbenog retka za NVDA:

| Kratka |Duga |Opis|
|---|---|---|
|-h |--help |Prikazuje pomoć u naredbenom retku i izlazi|
|-q |--quit |Zaustavlja trenutačno pokrenutu kopiju NVDA čitača|
|-k |--check-running |Izvještava o pokrenutosti NVDA putem izlaznog koda; 0 ako je pokrenut, 1 ako nije pokrenut|
|-f LOGFILENAME |--log-file=LOGFILENAME |datoteka u kojoj poruke zapisnika trebaju biti zapisane. Zapisivanje dnevnika je uvijek isključeno kada je sigurni način uključen.|
|-l LOGLEVEL |--log-level=LOGLEVEL |Najniža razina zapisivanih poruak u zapisniku (debug 10, ulaz/izlaz 12, debug upozorenje 15, info 20, onemogućeno 100). Zapisivanje dnevnika je uvijek isključeno kada je sigurni način uključen.|
|-c CONFIGPATH |--config-path=CONFIGPATH |određuje mapu u kojoj su pospremljene sve postavke Podrazumjevana vrijednost je prisilno ako je uključen sigurni način.|
|Nema |--lang=LANGUAGE |Nadpisuje konfigurirani NVDA jezik. Postavljen na "korisnički zadan" za trenutnog korisnika podrazumjevano, "en" za engleski, itd.|
|-m |--minimal |bez zvuka, bez sučelja, bez poruke dobrodošlice itd|
|-s |--secure |sigurni modus: onemogućuje Python konzolu značajke profila poput stvaranja, brisanja, preimenovanja profila itd., provjeru nadogradnji, neke potvrdne okvire u dijaloškom okviru dobrodošlice i u kategoriji općenitih postavki (npr. koristi NVDA prilikom prijave, spremi konfiguraciju poslje izlaza itd.), kao i zapisnik dnevnika i funkcije zapisa  (koristi se često na sigurnim ekranima). Imajte na umu da se postavke neće odavde spremati u mapu konfiguracije sustava te isto tako neće se spremati definirani prečaci.|
|nema |--disable-addons |dodaci neće imati utjecaja|
|nema |--debug-logging |Omogućuje dijagnostiku samo pri trenutačno pokrenutoj kopiji. Ova postavka natpisuje bilo koju drugu razinu vođenja zapisnika ( --loglevel, -l) specificirani argument uključujući i opciju bez logiranja.|
|nema |--no-logging |Potpuno isključuje vođenje zapisnika. OVa postavka može biti nadpisana ako razina loga ( --loglevel, -l) je specificiran iz naredbenog retka, ili je uključeno vođenje zapisnika.|
|nema |--no-sr-flag |Ne mijenjaj glavnu zastavicu čitača ekrana u sustavu|
|nema |--install |Instalira NVDA, pritom pokrečući novoinstaliranu kopiju|
|nema |--install-silent |Tiho instalira NVDA (ne pokreće novu instaliranu kopiju)|
|nema |--enable-start-on-logon=True|False |Tijekom instaliranja, aktivirajte [opciju pokretanja NVDA čitača na ekranu za prijavu](#StartAtWindowsLogon)|
|Nema |~~copy-portable-config |Prilikom instalacije, kopira se prijenosna kopija sa zadane lokacije (~~config-path, -c) u trenutnu korisničku mapu|
|nema |--create-portable |Stvara prijenosnu kopiju NVDA čitača (pri tome ponovo pokrečući novostvorenu kopiju). Zahtijeva određenu funkciju --portable-path|
|nema |--create-portable-silent |Stvara prijenosnu kopiju NVDA čitača (ne pokreće novostvorenu kopiju). zahtjeva određen parametar --portable-path|
|nema |--portable-path=PORTABLEPATH |Putanja za stvorenu prijenosnu kopiju|

### Cijelosustavski parametri {#SystemWideParameters}

NVDA omogućuje izmjenu nekih postavki u registru sustava, čime se mijenja ponašanje NVDA čitača u tom sustavu.
Te su vrijednosti spremljene u registru pod sljedećim ključevima:

* 32-bitni sustav: "HKEY_LOCAL_MACHINE\SOFTWARE\nvda"
* 64-bitni sustav: "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda"

Sljedeće vrijednosti se mogu postaviti pod ovim ključem:

| Naziv |Vrijednost |Moguće vrijednosti |Opis|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (Podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućeno, Čuva NVDA podešavanja u lokalnim podacima aplikacija umesto roming podataka|
|`serviceDebug` |DWORD |0 (podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućen, biće onemogućen [bezbedan način rada](#SecureMode) na [bezbednim ekranima](#SecureScreens). Zbog nekoliko ogromnih bezbednosnih rizika, korišćenje ove opcije se ne preporučuje|
|`forceSecureMode` |DWORD |0 (podrazumevano) da onemogućite, 1 da omogućite |Ako je omogućeno, nateraće NVDA da koristi [bezbedan režim](#SecureMode) pri pokretanju.|

## Dodatne Informacije {#FurtherInformation}

Ako trebate više informacija ili pomoć sa čitačem ekrana NVDA, molimo posjetite [NVDA web stranicu](NVDA_URL).
Tamo je moguće naći dodatnu dokumentaciju, tehničku podršku i resurse zajednice.
Ova web stranica sadržava informacije koje se tiču razvoja NVDA čitača.

