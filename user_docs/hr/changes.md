# ﻿Što je novo u NVDA

## 2024.4

Ovo izdanje sadrži brojna poboljšanja u Microsoft Officeu, Brailleovom pismu i oblikovanju dokumenata.

U Wordu ili Excelu sada je moguće dvaput pritisnuti gestu komentara da biste pročitali komentar ili bilješku u dijaloškom okviru koji se može pregledavati.
Sada možete koristiti naredbu za pregled odabira pokazivača za odabir teksta u programu PowerPoint.
NVDA također više ne šalje znakove smeća na Brailleovom pismu kada prikazuje tekst zaglavlja retka ili stupca u tablicama u Wordu kada koristite objektni model.

NVDA se sada može konfigurirati za zasebno izvještavanje o atributima fonta u govoru i Brailleovom pismu.

Dodana je nova postavka za konfiguriranje vremenskog ograničenja za izvođenje geste višestrukog pritiska, kao što je naredba za vrijeme/datum izvješća.

Sada možete konfigurirati način na koji NVDA prikazuje oblikovanje teksta na Brailleovom pismu i podesiti NVDA da prikazuje početak odlomaka na Brailleovom pismu.
NVDA sada može izgovoriti znak na kursoru prilikom izvođenja radnje usmjeravanja kursora na Brailleovom pismu.
Poboljšana je pouzdanost usmjeravanja kursora i dodana je podrška za tipke za usmjeravanje u programu PowerPoint.
Svi redovi ćelija sada će se koristiti kada koristite višelinijski brajični redak putem HID brajice.
NVDA više nije nestabilan nakon ponovnog pokretanja NVDA tijekom automatskog Bluetooth skeniranja Brailleovog pisma.

Minimalna potrebna verzija Poedita koja radi s NVDA sada je verzija 3.5.

eSpeak NG je ažuriran, dodajući podršku za farski i xextanski jezik.

LibLouis je ažuriran, dodajući nove tablice na Brailleovom pismu za tajlandsku i grčku međunarodnu Brailleovu pismo s jednoćelijskim naglašenim slovima.

Također je bilo nekoliko popravaka, uključujući praćenje miša u Firefoxu i govorni način rada na zahtjev.

### Nove značajke

* Nove značajke Brailleovog pisma:
  * Sada je moguće promijeniti način na koji NVDA prikazuje određene atribute oblikovanja teksta na Brailleovom pismu.
    Dostupne opcije su:
    * Liblouis (zadano): Koristi oznake oblikovanja definirane u odabranoj tablici brajice.
    * Oznake: koristi početne i završne oznake za označavanje gdje određeni atributi fonta počinju i završavaju. (#16864)
  * Kada je opcija "Čitaj po odlomku" omogućena, NVDA se sada može konfigurirati tako da označava početak odlomaka na Brailleovom pismu. (#16895, @nvdaes)
  * Prilikom izvođenja radnje usmjeravanja kursora na Brailleovom pismu, NVDA sada može automatski izgovoriti znak na pokazivaču. (#8072, @LeonarddeR)
    * Ova je opcija onemogućena prema zadanim postavkama.
      Možete omogućiti "Izgovori znakove prilikom usmjeravanja kursora u tekstu" u NVDA postavkama brajice.
* Naredba za komentare u programu Microsoft Word i naredba za bilješke u programu Microsoft Excel sada se mogu pritisnuti dvaput da bi se prikazao komentar ili bilješka u poruci koja se može pregledavati. (#16800, #16878, @Cary-Rowen)
* NVDA se sada može konfigurirati za zasebno izvještavanje o atributima fonta u govoru i Brailleovom pismu. (#16755)
* Vremensko ograničenje za izvođenje višestrukog pritiska tipke sada se može konfigurirati; Ovo može biti posebno korisno za osobe s oštećenjem spretnosti. (#11929, @CyrilleB79)

### Promjenama

* Opcije naredbenog retka '-c'/'--config-path' i '--disable-addons' sada se poštuju prilikom pokretanja ažuriranja iz NVDA-a. (#16937)
* Ažuriranja komponenti:
  * Ažuriran LibLouis Brailleov prevoditelj na [3.31.0](https://github.com/liblouis/liblouis/releases/tag/v3.31.0). (#17080, @LeonarddeR, @codeofdusk)
    * Popravljen prijevod brojeva na španjolskom Brailleovom pismu.
    * Nove tablice na Brailleovom pismu:
      * Tajlandski razred 1
      * Grčka međunarodna brajica (jednoznačini naglasni sustav)
    * Preimenovane tablice:
      * "Tajlandski 6 točaka" preimenovan je u "Tajlandski stupanj 0" zbog dosljednosti.
      * Postojeća tablica "Grčka međunarodna brajica" preimenovana je u "Grčka međunarodna brajica (slova s naglaskom u 2 ćelije)" kako bi se razjasnila razlika između dva grčka sustava.
  * eSpeak NG je ažuriran na 1.52-dev commit '961454ff'. (#16775)
    * Dodani su novi jezici farski i xextan.
* Kada koristite višeredni brajični zaslon putem standardnog HID upravljačkog programa za brajicu, koristit će se svi redovi ćelija. (#16993, @alexmoon)
* Stabilnost NVDA-ine podrške za Poedit je poboljšana s nuspojavom da je minimalna potrebna verzija Poedita sada verzija 3.5. (#16889, @LeonarddeR)

### Ispravci grešaka

* Popravci Brailleovog pisma:
  * Sada je moguće koristiti tipke za usmjeravanje brajice za pomicanje tekstnog pokazivača u programu Microsoft PowerPoint. (#9101)
  * Kada pristupate Microsoft Wordu bez automatizacije korisničkog sučelja, NVDA više ne ispisuje znakove smeća u zaglavljima tablice definiranim naredbama za postavljanje zaglavlja retka i stupca. (#7212)
  * Upravljački program Seika Notetaker sada ispravno generira Brailleov unos za razmak, backspace i točke s gestama razmaka/backspacea. (#16642, @school510587)
  * Usmjeravanje kursora sada je mnogo pouzdanije kada redak sadrži jedan ili više Unicode birača varijacija ili dekomponiranih znakova. (#10960, @mltony, @LeonarddeR)
  * NVDA više ne izbacuje pogrešku prilikom pomicanja brajičnog pisma prema naprijed u nekim praznim kontrolama za uređivanje. (#12885)
  * NVDA više nije nestabilan nakon ponovnog pokretanja NVDA tijekom automatskog Bluetooth skeniranja Brailleovog pisma. (#16933)
* Sada je moguće koristiti naredbe za odabir kursora za pregled za odabir teksta u programu Microsoft PowerPoint. (#17004)
* U načinu govora na zahtjev, NVDA više ne govori kada se poruka otvori u Outlooku, kada se nova stranica učita u pregledniku ili kada se prikazuje novi slajd u PowerPoint slideshowu. (#16825, @CyrilleB79)
* U pregledniku Mozilla Firefox, pomicanje miša preko teksta prije ili poslije veze sada pouzdano izvještava o tekstu. (#15990, @jcsteh)
* NVDA više ne uspijeva povremeno otvarati poruke koje se mogu pregledavati (kao što je dvaput pritisak na NVDA+f'). (#16806, @LeonarddeR)
* Ažuriranje NVDA-a dok su ažuriranja dodataka na čekanju više ne rezultira uklanjanjem dodatka. (#16837)
* Sada je moguća interakcija s padajućim popisima za provjeru valjanosti podataka u programu Microsoft Excel 365. (#15138)
* NVDA više nije tako spor kada se strelicama kreće gore-dolje kroz velike datoteke u VS Codeu. (#17039)
* NVDA više ne reagira nakon duljeg držanja tipke sa strelicom dok je u načinu pregledavanja, posebno u Microsoft Wordu i Microsoft Outlooku. (#16812)
* NVDA više ne čita zadnji redak kada je pokazivač na pretposljednjem retku kontrole za uređivanje s više redaka u Java aplikacijama. (#17027)

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Ažuriranja komponenti:
  * Ažuriran py2exe na 0.13.0.2 (#16907, @dpy013)
  * Ažurirani alati za postavljanje na 72.0 (#16907, @dpy013)
  * Ažuriran Ruff na 0.5.6. (#16868, @LeonarddeR)
  * Ažurirano NH3 na 0.2.18 (#17020, @dpy013)
* Dodana je datoteka '.editorconfig' u NVDA repozitorij kako bi nekoliko IDE datoteka prema zadanim postavkama pokupilo osnovna pravila stila NVDA koda. (#16795, @LeonarddeR)
* Dodana je podrška za prilagođene rječnike govornih simbola. (#16739, #16823, @LeonarddeR)
  * Rječnici se mogu pronaći u mapama specifičnim za lokalizaciju u dodatnom paketu, npr. 'locale\en'.
  * Metapodaci rječnika mogu se dodati u neobavezni odjeljak 'simbolDictionaries' u manifestu dodatka.
  * Dodatne pojedinosti potražite u odjeljku [Rječnici prilagođenih simbola govora u vodiču za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSymbolDictionaries).
* Sada je moguće preusmjeriti objekte dohvaćene s koordinata na zaslonu pomoću metode 'NVDAObject.objectFromPointRedirect'. (#16788, @Emil-18)
* Pokretanje SCona s parametrom '--all-cores' automatski će odabrati maksimalan broj dostupnih CPU jezgri. (#16943, #16868, @LeonarddeR)
* Informacije za razvojne inženjere sada uključuju informacije o arhitekturi aplikacije (kao što je AMD64) za objekt navigatora. (#16488, @josephsl)

#### Zastarjelosti

* Konfiguracijski ključ 'bool' '[documentFormatting][reportFontAttributes]' zastario je za uklanjanje u 2025.1, umjesto toga koristite '[fontAttributeReporting]'. (#16748)
  * Novi ključ ima vrijednost 'int' koja odgovara 'OutputMode' 'enum' s opcijama za govor, Brailleovo pismo, govor i Brailleovo pismo i isključeno.
  * Korisnici API-ja mogu koristiti vrijednost 'bool' kao i prije ili provjeriti 'OutputMode' ako posebno rukuju govorom ili Brailleovim pismom.
  * Ti su ključevi trenutno sinkronizirani do 2025.1.
* 'NVDAObjects.UIA.Inaccurate TextChangeEventEmittingEditableText' je zastario bez zamjene. (#16817, @LeonarddeR)

## 2024.3.1

Ovo je izdanje zakrpe za ispravljanje greške s automatskom obavijesti o ažuriranju dodatka.

### Ispravci grešaka

* Prilikom automatske provjere ažuriranja dodataka, NVDA se više ne zamrzava na lošim vezama. (#17036)

## 2024.3

Add-on store će vas obavijestiti o dostupnosti ažuriranja dodataka prilikom pokretanja NVDA.

Dodane su opcije za primjenu unicode normalizacije na govor i brajicu.
To može biti korisno pri čitanju znakova koji su nepoznati određenoj govornoj jedinici ili ne postoje u određenoj brajičnoj tablici. Takvi znakovi mogu imati kompatibilnu alternativu, poput podebljanih ili kosih slova koja se uobičajeno koriste na društvenim mrežama.
Ta opcija također omogućuje čitanje jednadžbi u Microsoft Word uređivaču jednadžbi.

Help Tech Activator Pro brajični redci su sada podržani.

Dodane su nedodijeljene geste za pomicanje kotačića miša vertikalno ili horizontalno.

Ispravljeno je nekoliko pogrešaka, prije svega u Windows 11 emoji panelu i povijesti međuspremnika.
Dodane su ispravke u web preglednicima za čitanje poruka o pogreškama, figure, crteže, oznake tablica te potvrdne okvire i izborne gumbe.

Liblouis je nadograđen sa dodanom podrškom za srpsku ćirilicu, Jidiš, nekoliko drevnih jezika, turski i međunarodnu fonetsku abecedu.
eSpeak je nadograđen sa dodanom podrškom za karakalpački.
Unicode CLDR je također nadograđen.

### nove značajke

* Novi tipkovnički prečaci:
  * Dodani su prečaci za vertikalno i horizontalno pomicanje kotačića miša, kako bi se unaprijedilo kretanje u nekim aplikacijama i na nekim web stranicama čiji se sadržaj osvježava, kao što je to na primjer Dism++. (#16462, @Cary-Rowen)
* Dodana podrška za Unicode normalizaciju za govor i brajicu. (#11570, #16466 @LeonarddeR).
  * To može biti korisno kada je određeni znak nepoznat za govornu jedinicu ili ne postoji u brajičnoj tablici, ali ima kompatibilnu alternativu kao što su to na primjer podebljani ili kosi znakovi koji se uobičajeno koriste na društvenim mrežama.
  * To također omogućuje čitanje jednadžbi u Microsoft Word uređivaču jednadžbi. (#4631)
  * Ovu značajku možete uključiti za govor i brajicu u dijaloškom okviru postavki u pripadajućim kategorijama.
* Od sada ćete biti podrazumijevano obavješteni o novim ažuriranjima dodataka prilikom pokretanja NVDA. (#15035)
  * To se može isključiti u "Add-on Store" kategoriji u postavkama.
  * NVDA provjerava svakodnevno za ažuriranje NVDA dodataka.
  * Provjeravat će se ažuriranja samo za jedan kanal (na primjer instalirani beta dodaci će biti provjeravani iz beta kanala).
* Dodana podrška za Help Tech Activator Pro brajične redke. (#16668)

### Izmjene

* nadogradnje komponenata:
  * eSpeak NG je nadograđen na inačicu 1.52-dev commit `54ee11a79`. (#16495)
    * Dodan novi jezik: karakalpački.
  * Nadograđen Unicode CLDR na inačicu 45.0. (#16507, @OzancanKaratas)
  * Nadograđen fast_diff_match_patch (koristi se za otkrivanje izmjena u naredbenom redku i drugom dinamičkom sadržaju) na inačicu 2.1.0. (#16508, @codeofdusk)
  * Nadograđen LibLouis brajični prevoditelj na inačicu [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0). (#16652, @codeofdusk)
    * nove brajične tablice:
      * Srpski ćirilica.
      * Jidiš.
      * Nekoliko drevnih jezika: biblijski hebrejski, akadski, sirijski, ugaricki te transliterirani klinopis.
      * Turski kratkopis. (#16735)
      * Međunarodna fonetska abeceda. (#16773)
  * Nadograđen NSIS na inačicu 3.10 (#16674, @dpy013)
  * Nadograđen markdown na inačicu 3.6 (#16725, @dpy013)
  * Nadograđen nh3 na inačicu 0.2.17 (#16725, @dpy013)
* Sigurnosna ulazna brajična tablica je jednaka izlaznoj sigurnosnoj brajičnoj tablici, koja je "Unificirani Engleski brajični kod puno pismo". (#9863, @JulienCochuyt, @LeonarddeR)
* NVDA će sada čitati figure bez pristupačnih podređenih objekata, ali sa oznakom i opisom. (#14514)
* Prilikom čitanja po redku  u modusu čitanja, "potpis" se više ne čita pri svakom redku potpisa ili tablice. (#14874)
* U Python konzoli, zadnja neizvršena komanda više neće biti izgubljena prilikom kretanja po povijesti ulaza. (#16653, @CyrilleB79)
* Unikatan anonimni identifikator sada se šalje kao dio neobaveznih statistika korištenja NVDA. (#16266)
* Pri stvaranju prijenosne kopije, podrazumijevano će se automatski stvarati nova mapa.
Od sada će se prikazivati upozorenje ako pokušate pisati unutar mape koja nije prazna. (#16686)

### Ispravke grešaka

* Windows 11 ispravke:
  * NVDA se više neće zaglavljivati prilikom zatvaranja povijesti međuspremnika i emoji panela. (#16346, #16347, @josephsl)
  * NVDA će ponovno izgovarati vidljive kandidate prilikom otvaranja Ime sučelja. (#14023, @josephsl)
  * NVDA više neće dvaput izgovoriti "povijest međuspremnika" pri kretanju stavkama izbornika emoji panela. (#16532, @josephsl)
  * NVDA više neće prekidati govor i brajicu pri pregledu kaomojia i znakova u emoji panelu. (#16533, @josephsl)
* Ispravke u preglednicima:
  * Poruke o pogrešci zabilježene kao `aria-errormessage` sada se izgovaraju u Google Chromeu i Mozilla Firefoxu. (#8318)
  * Ako postoji, NVDA će sada koristiti `aria-labelledby` atribut za  dohvaćanje pristupačnih naziva tablica u Mozilla Firefoxu. (#5183)
  * NVDA će ispravno izgovarati stavke izbornika u obliku izbornih gumbi i potvrdnih okvira prilikom prvog otvaranja podizbornika u Google Chromeu i Mozilla Firefoxu. (#14550)
  * Značajka pretrage u modusu čitanja NVDA čitača zaslona sada je točnija kada stranica sadrži emoji znakove. (#16317, @LeonarddeR)
  * U Mozilla Firefoxu, NVDA sada ispravno čita trenutni znak, trenutnu riječ i trenutni redak kada se kursor nalazi na točki umetanja na kraju redka. (#3156, @jcsteh)
  * NVDA više ne prouzrokuje rušenje poslije zatvaranja dokumenta ili zatvaranja Google Chromea. (#16893)
* NVDA će sada ispravno čitati prijedloge automatskog popunjavanja u Eclipse i drugim okruženjima baziranima na Eclipseu u Windowsima 11. (#16416, @thgcode)
* Unapređena pouzdanost automatskog čitanja teksta, osobito u aplikacijama naredbenog redka. (#15850, #16027, @Danstiv)
* Sada je ponovno moguće pouzdano vratiti konfiguraciju na prethodne vrijednosti. (#16755, @Emil-18)
* NVDA će ispravno izgovarati promjene u označavanju pri uređivanju teksta ćelije u Microsoft Excelu. (#15843)
* U aplikacijama koje koriste Jawa access bridge, NVDA će sada ispravno pročitati zadnji prazan redak teksta umjesto ponavljanja prethodnog redka teksta. (#9376, @dmitrii-drobotov)
* U LibreOffice Writeru (inačica 24.8 i novijim), prilikom uključivanja ili isključivanja oblikovanja teksta (podebljanja, ukošenja, podcrtavanja, indeksa/eksponenta, poravnanja) kada se koriste odgovarajući tipkovnički prečaci, NVDA će izgovoriti novo obilježje oblikovanja (na primjer, "podebljano uključeno", "podebljano isključeno"). (#4248, @michaelweghorn)
* pri kretanju po poljima za uređivanje u aplikacijama koje koriste UI automation, NVDA više ne izgovara krivi znak, krivu riječ, Itd. (#16711, @jcsteh)
* Pri ljepljenju u  Windows 10/11 kalkulator, NVDA sada ispravno čita cijeli broj koji je zalijepljen. (#16573, @TristanBurchett)
* Govor se više ne gubi prilikom ponovnog povezivanja u sesiju udaljene radne površine. (#16722, @jcsteh)
* Dodana je podrška za prečace za pregledavanje teksta za ime objekta u Visual Studio Codeu. (#16248, @Cary-Rowen)
* Zvukovi NVDA sada se reproduciraju i na Mono audiouređajima. (#16770, @jcsteh)
* NVDA će od sada čitati adrese prilikom kretanja po poljima do/kopija/skrivena kopija u prgramu outlook.com i suvremenom Outlooku. (#16856)
* NVDA sada bolje rukuje pogreškama pri instalaciji dodataka. (#16704)

### Promjene za programere

* NVDA sada koristi Ruff umjesto flake8 za linting. (#14817)
* Popravljen je NVDA-in sustav izrade kako bi ispravno radio kada koristite Visual Studio 2022 verzije 17.10 i novije. (#16480, @LeonarddeR)
* Font fiksne širine sada se koristi u pregledniku dnevnika i u NVDA Python konzoli tako da kursor ostaje u istom stupcu tijekom okomite navigacije.
Posebno je korisno pročitati oznake lokacije pogrešaka u tragovima. (#16321, @CyrilleB79)
* Dodana je podrška za prilagođene tablice brajice. (#3304, #16208, @JulienCochuyt, @LeonarddeR)
  * Tablice se mogu pronaći u mapi 'brailleTables' u dodatnom paketu.
  * Metapodaci tablice mogu se dodati u neobavezni odjeljak 'brailleTables' u manifestu dodatka ili u datoteku '.ini' u istom formatu koji se nalazi u poddirektoriju brailleTables direktorija bloka za ogrebotine.
  * Više pojedinosti potražite u odjeljku [Tablice za prijevod Brailleovog pisma u vodiču za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#BrailleTables).
* Kada je događaj 'gainFocus' stavljen u red čekanja s objektom koji ima valjano svojstvo 'focusRedirect', objekt na koji upućuje svojstvo 'focusRedirect' sada drži 'eventHandler.lastQueuedFocusObject', a ne izvorni objekt u redu čekanja. (#15843)
* NVDA će zabilježiti svoju izvršnu arhitekturu (x86) pri pokretanju. (#16432, @josephsl)
* 'wx. CallAfter', koji je umotan u 'monkeyPatches/wxMonkeyPatches.py', sada uključuje odgovarajuću indikaciju 'functools.wraps'. (#16520, @XLTechie)
* Postoji novi modul za raspoređivanje zadataka 'utils.schedule', koristeći pip modul 'schedule'. (#16636)
  * Možete koristiti 'scheduleThread.scheduleDailyJobAtStartUp' za automatsko zakazivanje posla koji se događa nakon pokretanja NVDA i svaka 24 sata nakon toga.
  Poslovi se zakazuju sa zakašnjenjem kako bi se izbjegli sukobi.
  * 'scheduleThread.scheduleDailyJob' i 'scheduleJob' mogu se koristiti za zakazivanje poslova u prilagođeno vrijeme, gdje će se 'JobClashError' pokrenuti na poznatom sukobu zakazivanja zadataka.
* Sada je moguće stvoriti module aplikacije za aplikacije koje hostiraju kontrole Edge WebView2 (msedgewebview2.exe). (#16705, @josephsl)

## 2024.2

Dodana nova značajka način podjeljenog zvuka.
Ta značajka omogućuje postavljanje zvuka NVDA u jedan kanal (npr. lijevi), dok su zvukovi drugih programa usmjereni u  drugi kanal (na primjer desni).

Dodani su novi prečaci za promjenu postavki prstena govorne jedinice, koje omogućuju premještanje od prve do zadnje postavke, te njihovo mijenjanje u većim koracima.
Dodani su novi prečaci brze navigacije, koji omogućuju korisnicima kretanje po: odlomcima, okomito poravnatim odlomcima, tekstu istog stila, tekstu različitog stila, stavkama izbornika, preklopnim gumbima, trakama napredovanja, figurama, te matematičkim formulama.

Dodano je puno novih značajki vezanih uz brajicu, te je ispravljeno puno pogrešaka.
Dodan je novi modus brajice "prikaz govora".
Kada je aktivan, na brajičnom se redku prikazuje točno ono što NVDA izgovara.
Također je dodana podrška za brajične redke BrailleEdgeS2, BrailleEdgeS3.
LibLouis je nadograđen sa dodanim novim brajičnim tablicama sa označavanjem velikih slova za bjeloruski i ukrajinski jezik, brajičnom tablicom za Laoski jezik te brajičnom tablicom za španjolski jezik, predviđena za čitanje starogrčkog teksta.

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
  * Omogućuje postavljanje NVDA u jednom kanalu (na primjer lijevom) dok su zvukovi drugih programa usmjereni u drugi kanal (na primjer desni).
  * Regulira se uz pomoć prečaca `NVDA+alt+s`.
* Izgovaranje zaglavlja redaka i stupaca u ContentEditable html elementima. (#14113)
* Dodana opcija za isključivanje čitanja figura i potpisa u postavkama oblikovanja dokumenata. (#10826, #14349)
* U Windowsima 11, NVDA će izgovarati upozorenja glasovnog upisivanja i preporučene radnje uključujući glavnu preporučenu radnju prilikom kopiranja podataka poput telefonskih brojeva u međuspremnik (Windows 11 nadogradnja 2022 i novije inačice). (#16009, @josephsl)
* NVDA će držati audiouređaj budnim poslije zaustavljanja govora, kako bi se izbjeglo rezanje sljedeće izgovorene fraze na nekim audiouređajima poput Bluetooth slušalica. (#14386, @jcsteh, @mltony)
* HP Secure Browser je sada podržan. (#16377)

### Izmjene

* Trgovina dodataka:
  * Minimalna verzija i posljednja testirana verzija dodatka sada se prikazuju u području "više detalja". (#15776, @Nael-Sayegh)
  * Radnja "recenzije zajednice" biti će dostupna u pojedinostima u svim karticama svojstava u Add-on storeu. (#16179, @nvdaes)
* Nadogradnje komponenti:
  * Nadograđen LibLouis brajični prevoditelj na inačicu [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Nove brajične tablice za bjeloruski i ukrajinski jezik sa podrškom prikazivanja znakova za velika slova.
    * Nova španjolska brajična tablica sa podrškom za čitanje grčkog teksta.
    * Nova brajična tablica za laoski jezik, puno pismo. (#16470)
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
* Trgovina dodataka:
  * Kada se pritisne `ctrl+tab`, fokus se ispravno prebacuje na novi aktualni naslov kartice svojstva. (#14986, @ABuffEr)
  * Ako datoteke predmemorije nisu ispravne, NVDA se više neće ponovno pokretati. (#16362, @nvdaes)
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
* preklopnik u naredbenom redku `-h`/`--help` ponovno ispravno radi. (#16522, @XLTechie)
* NVDA podrška za Poedit softver za prevođenje inačica 3.4 ili novije verzije ispravno radi prilikom prevođenja na jezike sa jednim ili više od dva oblika množine (npr: u kineskom, poljskom). (#16318)

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Instanciranje objekata 'winVersion.WinVersion' s nepoznatim verzijama sustava Windows iznad 10.0.22000, kao što je 10.0.25398, vraća "Windows 11 nepoznat" umjesto "Windows 10 nepoznato" za naziv izdanja. (#15992, @josephsl)
* Olakšajte proces izrade AppVeyor-a za NVDA forkove dodavanjem konfigurabilnih varijabli u appveyor.yml za onemogućavanje ili izmjenu NV Access specifičnih dijelova skripti za izradu. (#16216, @XLTechie)
* Dodan je dokument s uputama, koji objašnjava proces izrade NVDA forkova na AppVeyoru. (#16293, @XLTechie)

## 2024.1

Dodan je novi modus govora čitanja informacija na zahtjev.
Kada je modus govora postavljen da izgovara informacije na zahtjev, NVDA ne čita informacije automatski na primjer prilikom pomicanja kursora, ali još uvijek izgovara informacije i koje se dobivaju uz pomoć prečaca, čiji je cilj izgovaranja određenih informacija na primjer, izgovaranje naslovne trake.
U kategoriji "govor" NVDA postavki, sada je moguće izostavljanje neželjenih modusa govora iz odabira modusa govora (`NVDA+s`).

Novi način kopiranja sa sačuvanim oblikovanjem, koji se poziva uz pomoć prečaca `NVDA+shift+f10` dostupan je na web stranicama u Mozilla Firefoxu.
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

* Trgovina dodataka:
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

* Trgovina dodataka:
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

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Napomena: ovo je izdanje koje krši kompatibilnost dodatnog API-ja.
Dodatke će trebati ponovno testirati i ažurirati njihov manifest.
* Za izradu NVDA sada je potreban Visual Studio 2022.
Pogledajte [NVDA docs](https://github.com/nvaccess/nvda/blob/release-2024.1/projectDocs/dev/createDevEnvironment.md) za specifičan popis komponenti Visual Studija. (#14313)
* Dodane su sljedeće točke proširenja:
  * 'treeInterceptorHandler.post_browseModeStateChange'. (#14969, @nvdaes)
  * 'speech.speechCanceled'. (#15700, @LeonarddeR)
  * '_onErrorSoundRequested' (treba dohvatiti pozivom 'logHandler.getOnErrorSoundRequested()') (#15691, @CyrilleB79)
* Sada je moguće koristiti oblike množine u prijevodima dodatka. (#15661, @beqabeqa473)
* Uključeno python3.dll u binarnu distribuciju za korištenje od strane dodataka s vanjskim bibliotekama koje koriste [stable ABI](https://docs.python.org/3.11/c-api/stable.html). (#15674, @mzanm)
* Osnovna klasa "BrailleDisplayDriver" sada ima svojstva "numRows" i "numCols" za pružanje informacija o višelinijskim prikazima brajice.
Postavljanje "numCells" i dalje je podržano za jednoredničke brajice, a "numCells" će vratiti ukupan broj ćelija za brajice s više redaka. (#15386)
* Ažuriran BrlAPI za BRLTTY na verziju 0.8.5 i njegov odgovarajući python modul na verziju kompatibilnu s Pythonom 3.11. (#15652, @LeonarddeR)
* Dodana je funkcija 'speech.speakSsml' koja vam omogućuje pisanje NVDA govornih sekvenci pomoću [SSML](https://www.w3.org/TR/speech-synthesis11/). (#15699, @LeonarddeR)
  * Sljedeće oznake trenutno su podržane i prevedene u odgovarajuće NVDA govorne naredbe:
    * 'Prozodija' ('visina', 'stopa' i 'glasnoća'). Podržano je samo množenje (npr. '200%').
    * 'reci kao' s atributom 'interpret' postavljenim na 'znakovi'
    * 'voice' s 'xml:lang' postavljenim na XML jezik
    * 'break' s atributom 'vrijeme' postavljenim na vrijednost u milisekundama, npr. '200ms'
    * 'mark' s atributom 'name' postavljenim na naziv marke, npr. 'mark1', zahtijeva povratni poziv
  * Example: `speech.speakSsml('&lt;speak&gt;&lt;prosody pitch="200%"&gt;hello&lt;/prosody&gt;&lt;break time="500ms" /&gt;&lt;prosody rate="50%"&gt;John&lt;/prosody&gt;&lt;/speak&gt;')`
  * Mogućnosti raščlanjivanja SSML-a podržane su klasom 'SsmlParser' u modulu 'speechXml'.
* Promjene u biblioteci klijenta NVDA kontrolera:
  * Nazivi datoteka biblioteke više ne sadrže sufiks koji označava arhitekturu, npr. 'nvdaControllerClient32/64.dll' sada se nazivaju 'nvdaControllerClient.dll'. (#15718, #15717, @LeonarddeR)
  * Dodan je primjer za demonstraciju korištenja nvdaControllerClient.dll iz Rusta. (#15771, @LeonarddeR)
  * Dodane su sljedeće funkcije klijentu kontrolera: (#15734, #11028, #5638, @LeonarddeR)
    * 'nvdaController_getProcessId': Za dobivanje ID-a procesa (PID) trenutne instance NVDA koju klijent kontrolera koristi.
    * 'nvdaController_speakSsml': Uputiti NVDA da govori u skladu s navedenim SSML-om. Ova funkcija također podržava:
      * Pružanje razine simbola.
      * Osiguravanje prioriteta govora koji se izgovara.
      * Govor sinkrono (blokiranje) i asinkrono (trenutni povratak).
    * `nvdaController_setOnSsmlMarkReachedCallback`: To register a callback of type `onSsmlMarkReachedFuncType` that is called in synchronous mode for every `&lt;mark /&gt;` tag encountered in the SSML sequence provided to `nvdaController_speakSsml`.
  * Napomena: nove funkcije u klijentu kontrolera podržavaju samo NVDA 2024.1 i novije verzije.
* Ažurirane ovisnosti o uključivanju:
  * Skretanje na '4b8c659f549b0ab21cf649377c7a84eb708f5e68'. (#15695)
  * IA2 do '3d8c7f0b833453f761ded6b12d8be431507bfe0b'. (#15695)
  * Sonic na '8694c596378c24e340c09ff2cd47c065494233f1'. (#15695)
  * w3c-aria-prakse na '9a5e55ccbeb0f1bf92b6127c9865da8426d1c864'. (#15695)
  * na '5e9be7b2d2fe3834a7107f430f7d4c0631f69833'. (#15695)
* Informacije o uređaju koje daje 'hwPortUtils.listUsbDevices' sada sadrže opis USB uređaja koji je prijavljena sabirnica (ključ 'busReportedDeviceDescription'). (#15764, @LeonarddeR)
* Za USB serijske uređaje, 'bdDetect.getConnectedUsbDevicesForDriver' i 'bdDetect.getDriversForConnectedUsbDevices' sada daju podudaranja uređaja koja sadrže 'deviceInfo' rječnik obogaćen podacima o USB uređaju, kao što je 'busReportedDeviceDescription'. (#15764, @LeonarddeR)
* Kada je konfiguracijska datoteka 'nvda.ini' oštećena, sigurnosna kopija se sprema prije ponovne inicijalizacije. (#15779, @CyrilleB79)
* Prilikom definiranja skripte pomoću dekoratora skripte, može se navesti logički argument 'speakOnDemand' kako bi se kontroliralo treba li skripta govoriti dok je u govornom načinu rada "na zahtjev". (#481, @CyrilleB79)
  * Skripte koje pružaju informacije (npr. naslov prozora, vrijeme/datum izvješća) trebale bi govoriti u načinu rada "na zahtjev".
  * Skripte koje izvode radnju (npr. pomicanje pokazivača, promjena parametra) ne bi trebale govoriti u načinu rada "na zahtjev".
* Ispravljena greška zbog koje je brisanje datoteka praćenih git-om tijekom 'scons -c' rezultiralo nedostatkom UIA COM sučelja pri ponovnoj izgradnji. (#7070, #10833, @hwf1324)
* Ispravite grešku zbog koje neke promjene koda nisu otkrivene prilikom izrade 'dist', što je spriječilo pokretanje nove verzije.
Sada se 'dist' uvijek obnavlja. (#13372, @hwf1324)
* 'gui.nvdaControls.MessageDialog' sa zadanom vrstom standarda više ne izbacuje iznimku pretvorbe None jer nije dodijeljen zvuk. (#16223, @XLTechie)

#### Promjene koje prekidaju API

To su pokvarene promjene API-ja.
Otvorite problem s GitHubom ako vaš dodatak ima problema s ažuriranjem na novi API.

* NVDA je sada izgrađen s Pythonom 3.11. (#12064)
* Ažurirane ovisnosti pipa:
  * configobj to 5.1.0dev commit 'e2ba4457c4651fa54f8d59d8dcdd3da950e956b8'. (#15544)
  * Komtipovi na 1.2.0. (#15513, @codeofdusk)
  * Pahuljice8 do 4.0.1. (#15636, @lukaszgo1)
  * py2exe na 0.13.0.1dev commit '4e7b2b2c60face592e67cb1bc935172a20fa371d'. (#15544)
  * RobotFramework do 6.1.1. (#15544)
  * SCons do 4.5.2. (#15529, @LeonarddeR)
  * Sfinga do 7.2.6. (#15544)
  * wxPython u 4.2.2a commit '0205c7c1b9022a5de3e3543f9304cfe53a32b488'. (#12551, #16257)
* Uklonjene ovisnosti pipa:
  * typing_extensions, oni bi trebali biti izvorno podržani u Pythonu 3.11 (#15544)
  * nose, umjesto toga unittest-xml-reporting koristi se za generiranje XML izvješća. (#15544)
* 'IAccessibleHandler.SecureDesktopNVDAObject' je uklonjen.
Umjesto toga, kada je NVDA pokrenut na korisničkom profilu, pratite postojanje sigurne radne površine pomoću točke proširenja: 'winAPI.secureDesktop.post_secureDesktopStateChange'. (#14488)
* 'Brailleovo pismo. BrailleHandler.handlePendingCaretUpdate' uklonjen je bez javne zamjene. (#15163, @LeonarddeR)
* "bdDetect.addUsbDevices i bdDetect.addBluetoothDevices" su uklonjeni.
Upravljački programi Brailleovog zaslona trebali bi umjesto toga implementirati metodu klase 'registerAutomaticDetection'.
Ta metoda prima objekt 'DriverRegistrar' na kojem se mogu koristiti metode 'addUsbDevices' i 'addBluetoothDevices'. (#15200, @LeonarddeR)
* Zadana implementacija metode provjere na 'BrailleDisplayDriver' sada zahtijeva da atributi 'threadSafe' i 'supportsAutomaticDetection' budu postavljeni na 'True'. (#15200, @LeonarddeR)
* Prosljeđivanje lambda funkcija u 'hwIo.ioThread.IoThread.queueAsApc' više nije moguće jer bi funkcije trebale biti slabo referencirane. (#14627, @LeonarddeR)
* 'IoThread.autoDeleteApcReference' je uklonjen. (#14924, @LeonarddeR)
* Kako bi podržali velike promjene visine, sintisajzeri sada moraju eksplicitno deklarirati svoju podršku za 'PitchCommand' u atributu 'supportedCommands' na upravljačkom programu. (#15433, @LeonarddeR)
* 'speechDictHandler.speechDictVars' je uklonjen. Upotrijebite 'NVDAState.WritePaths.speechDictsDir' umjesto 'speechDictHandler.speechDictVars.speechDictsPath'. (#15614, @lukaszgo1)
* 'languageHandler.makeNpgettext' i 'languageHandler.makePgettext' su uklonjeni.
'npgettext' i 'pgettext' sada su izvorno podržani. (#15546)
* Modul aplikacije za [Poedit](https://poedit.net) značajno je promijenjen. Funkcija 'fetchObject' je uklonjena. (#15313, #7303, @LeonarddeR)
* Sljedeći suvišni tipovi i konstante uklonjeni su iz 'hwPortUtils': (#15764, @LeonarddeR)
  * 'PCWSTR'
  * 'HWND' (zamijenjeno s 'ctypes.wintypes.HWND')
  * 'ULONG_PTR'
  * 'ULONGLONG'
  * 'NULA'
  * "GUID" (zamijenjeno s "comtypes. GUID')
* 'gui.addonGui.AddonsDialog' je uklonjen. (#15834)
* 'touchHandler.TouchInputGesture.multiFingerActionLabel' uklonjen je bez zamjene. (#15864, @CyrilleB79)
* 'NVDAObjects.IAccessible.winword.WordDocument.script_reportCurrentHeaders' je uklonjen bez zamjene. (#15904, @CyrilleB79)
* Uklanjaju se sljedeći moduli aplikacije.
Kod koji se uvozi iz jednog od njih, umjesto toga treba uvesti iz zamjenskog modula. (#15618, @lukaszgo1)

| Uklonjen naziv modula |Zamjenski modul|
|---|---|
|'azardi-2.0' |'azardi20'|
|'azuredatastudio' |'kod'|
|'azuredatastudio-insiders' |'kod'|
|'calculatorapp' |'kalkulator'|
|'kod - upućeni' |'kod'|
|'commsapps' |'hxmail'|
|'dbeaver' |'pomrčina'|
|'digitaleditionspreview' |'digitaleditions'|
|'esybraille' |'esysuite'|
|'hxoutlook' |'hxmail'|
|'miranda64' |'miranda32'|
|'mpc-hc' |'mplayerc'|
|'mpc-hc64' |'mplayerc'|
|'notepad++' |'notepadPlusPlus'|
|'searchapp' |'searchui'|
|'searchhost' |'searchui'|
|'springtoolsuite4' |'pomrčina'|
|'sts' |'pomrčina'|
|'teamtalk3' |'teamtalk4classic'|
|'textinputhost' |'windowsinternal_composableshell_experiences_textinput_inputapp'|
|'totalcmd64' |'totalcmd'|
|'win32calc' |'calc'|
|'winmail' |'msimn'|
|'zend-eclipse-php' |'pomrčina'|
|'ZendStudio' |'Pomrčina'|

#### Zastarjelosti

* Korištenje 'watchdog.getFormattedStacksForAllThreads' je zastarjelo - umjesto toga koristite 'logHandler.getFormattedStacksForAllThreads'. (#15616, @lukaszgo1)
* 'easeOfAccess.canConfigTerminateOnDesktopSwitch' je zastario jer je zastario jer Windows 7 više nije podržan. (#15644, @LeonarddeR)
* 'winVersion.isFullScreenMagnificationAvailable' je zastario - umjesto toga koristite 'visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart'. (#15664, @josephsl)
* Sljedeće konstante izdanja sustava Windows zastarjele su iz modula winVersion (#15647, @josephsl):
  * 'winVersion.WIN7'
  * 'winVersion.WIN7_SP1'
  * 'winVersion.WIN8'
* Konstante 'bdDetect.KEY_*' su zastarjele.
Umjesto toga upotrijebite 'bdDetect.DeviceType.*'. (#15772, @LeonarddeR).
* Konstante 'bdDetect.DETECT_USB' i 'bdDetect.DETECT_BLUETOOTH' su zastarjele bez javne zamjene. (#15772, @LeonarddeR).
* Korištenje 'gui. ExecAndPump' je zastario - umjesto toga koristite 'systemUtils.ExecAndPump'. (#15852, @lukaszgo1)

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
  * NVDA će sada emitirati zvuk putem Windows Audio Session API-ja (WASAPI), što može poboljšati odziv, performanse i stabilnost NVDA govora i zvukova. (#14697, #11169, #11615, #5096, #10185, #11061)
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
* Microsoft Edge:
  * NVDA se više neće vraćati na prethodnu poziciju u modusu čitanja pri otvaranju kontekstnog izbornika u Microsoft Edgeu. (#15309)
  * NVDA opet može čitati kontekstni izbornik preuzimanja u Microsoft Edgeu. (#14916)
* Brajica:
  * Brajični kursor i pokazivač označenosti bit će ispravno osvježeni poslije uključenja ili isključenja gestom. (#15115)
  * Ispravljena pogreška prilikom koje su se Albatros brajični redci pokušali inicijalizirati čak iako je drugi brajični redak bio spojen. (#15226)
* Trgovina dodataka:
  * Ispravljena greška poslije odznačavanja "uključi nekompatibilne dodatke" koja je prouzrokovala vidljivost nekompatibilnih dodataka. (#15411)
  * Dodaci blokirani zbog nekompatibilnosti bi se sada trebali pravilno osvježavati prilikom sortiranja po statusu uključenosti ili isključenosti. (#15416)
  * Ispravljena pogreška nadpisivanja ili nadogradnje dodataka koristeći ručnu instalaciju. (#15417)
  * Ispravljena pogreška prilikom koje NVDA neće govoriti poslije ponovnog pokretanja i završetka NVDA instalacije. (#14525)
  * Ispravljena pogreška  pri instalaciji dodataka ako je prethodna instalacija ili preuzimanje prekinuto. (#15469)
  * Ispravljene pogreške s rukovanjem nekompatibilnim dodacima pri nadogradnji NVDA. (#15414, #15412, #15437)
* NVDA opet izgovara rezultate računskih operacija u 32-bitnom kalkulatoru za Windows u operacijskim sustavima Server, LTSC i LTSB. (#15230)
* NVDA više ne ignorira izmjene fokusa kada višeslojni prozor (prozor koji se nalazi iznad drugog prozora) postane fokusiran. (#15432)
* Ispravljeno moguće rušenje prilikom pokretanja NVDA. (#15517)

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* 'braille.handler.handleUpdate' i 'braille.handler.handleReviewMove' promijenjeni su kako se ne bi odmah ažurirali.
Prije ove promjene, kada se bilo koja od ovih metoda pozivala vrlo često, to bi iscrpilo mnoge resurse.
Ove metode sada umjesto toga stavljaju ažuriranje u red čekanja na kraju svakog jezgrenog ciklusa.
Također bi trebali biti sigurni za niti, što omogućuje njihovo pozivanje iz pozadinskih niti. (#15163)
* Dodana je službena podrška za registraciju prilagođenih upravljačkih programa za Brailleovo pismo u procesu automatskog otkrivanja brajevog pisma.
Pogledajte Brailleovo pismo. BrailleDisplayDokumentacija o klasi vozača za više detalja.
Najznačajnije, atribut 'supportsAutomaticDetection' mora biti postavljen na 'True' i 'registerAutomaticDetection' 'classmethod' mora biti implementiran.  (#15196)

#### Zastarjelosti

* 'Brailleovo pismo. BrailleHandler.handlePendingCaretUpdate' sada je zastario bez javne zamjene.
Bit će uklonjen 2024.1. (#15163)
* Uvoz konstanti 'xlCenter', 'xlJustify', 'xlLeft', 'xlRight', 'xlDistributed', 'xlBottom', 'xlTop' iz 'NVDAObjects.window.excel' je zastario.
Umjesto toga upotrijebite nabrajanje 'XlHAlign' ili 'XlVAlign'. (#15205)
* Mapiranje "NVDAObjects.window.excel.alignmentLabels" je zastarjelo.
Umjesto toga koristite metode 'displayString' nabrajanja 'XlHAlign' ili 'XlVAlign'. (#15205)
* 'bdDetect.addUsbDevices' i 'bdDetect.addBluetoothDevices' su zastarjeli.
Upravljački programi Brailleovog zaslona trebali bi umjesto toga implementirati metodu klase 'registerAutomaticDetection'.
Ta metoda prima objekt 'DriverRegistrar' na kojem se mogu koristiti metode 'addUsbDevices' i 'addBluetoothDevices'. (#15200)
* Zadana implementacija metode provjere na 'BrailleDisplayDriver' koristi 'bdDetect.driverHasPossibleDevices' za uređaje koji su označeni kao sigurni za niti.
Počevši od NVDA 2024.1, kako bi osnovna metoda koristila 'bdDetect.driverHasPossibleDevices', atribut 'supportsAutomaticDetection' također mora biti postavljen na 'True'. (#15200)

## 2023.2

Ova verzija dodaje add-on store koja Zamjenjuje upravljanje dodacima.
U  Add-on storeu možete pregledavati, pretraživati, instalirati i ažurirati dodatke zajednice.
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
* Novi prečaci:
  * Nova ulazna gesta bez dodijeljenog prečaca za kruženje kroz dostupne jezike za Windows OCR. (#13036)
  * nova ulazna gesta bez dodijeljenog prečaca za kruženje kroz moduse prikazivanja poruka na brajičnom redku. (#14864)
  * Ulazna gesta bez dodijeljenog prečaca za uključivanje ili isključivanje indikacije označavanja. (#14948)
  * Dodani podrazumjevani prečaci na tipkovnice za kretanje na sljedeći ili prethodni objekt u raskropljenom prikazu hierarhije objekata. (#15053)
    * stolno računalo: `NVDA+numerički9` i `NVDA+numerički3` za kretanje na slijedeći ili prethodni objekt.
    * prijenosno računalo: `šift+NVDA+[` i `šift+NVDA+]` za kretanje na prethodni i slijedeći objekt.
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
* Eksperimentalno poboljšano upravljanje zvukom:
  * NVDA sada može reproducirati zvukove putem standarda Windows Audio Session API (WASAPI), što može poboljšati brzinu, performanse i stabilnost NVDA govora i zvukova.
  * Korištenje WASAPI se može omogućiti u naprednim postavkama.
  Također, ako je WASAPI omogućen, sljedeće napredne postavke se mogu regulirati.
    * Opcija koja prouzrokuje praćenje glasnoće NVDA govornog izlaza i zvučnih signala. (#1409)
    * Opcija za odvojeno postavljanje glasnoće NVDA zvukova. (#1409, #15038)
  * Postoji poznat problem sa povremenim rušenjem kada je WASAPI omogućen. (#15150)
* U preglednicima Mozilla Firefox i Google Chrome, NVDA sada čita ako kontrola otvara dijaloški okvir, mrežu, popis ili stablasti prikaz ako je autor ovo označio uz pomoć `aria-haspopup` atributa . (#14709)
* Sada je moguće koristiti varijable  sustava (poput  `%temp%` ili  `%homepath%`) pri određivanju putanje pri stvaranju NVDA prijenosne kopije. (#14680)
* u ažuriranju Windowsa 10 za svibanj 2019 i novijim, NVDA može izgovarati imena virtualnih radnih površina kada se otvaraju, mijenjaju ili zatvaraju. (#5641)
* Dodan je sveopći parametar sustava koji će dozvoliti korisnicima i administratorima sustava prisilno pokretanje NVDA u sigurnom modusu. (#10018)

### Izmjene

* Ažurirane komponente:
  * eSpeak NG je ažuriran na inačicu 1.52-dev commit `ed9a7bcf`. (#15036)
  * Ažuriran LibLouis brajični prevoditelj na inačicu [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR je ažuriran na inačicu 43.0. (#14918)
* Izmjene u LibreOffice paketu:
  * Kada se čita pozicija preglednog kursora, trenutna pozicija kursora se sada čita u odnosu na trenutnu stranicu u programu LibreOffice Writer za LibreOffice inačicu 7.6 i novije, slično čitanju u programu Microsoft Word. (#11696)
  * Izgovor trake stanja (na primjer kada se pritisne `NVDA+end`) radi u paketu LibreOffice. (#11698)
  * Kada se prebacite na neku drugu ćeliju u programu LibreOffice Calc, NVDA više neće neispravno izgovarati koordinate prethodno fokusirane ćelije kada se izgovor koordinata ćelija onemogući u NVDA postavkama. (#15098)
* Promjene za brajične redke:
  * Kada se koristi brajični redak uz pomoć upravljačkog programa za Hid brajični standard, dpad se sada može koristiti za emuliranje strelica tipkovnice i entera.
  Takođe,  `razmaknica+točka1` i `razmaknica+točka4` sada se koriste kao strelice dole i gore. (#14713)
  * Ažuriranja dinamičkog sadržaja na Web stranicama (ARIA žive regije) se sada prikazuju na brajičnom redku.
  Ovo se može onemogućiti na panelu naprednih postavki. (#7756)
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
  Umjesto toga NVDA će prijaviti da poveznica  nema odredište. (#14723)
  * U modusu pretraživanja, NVDA neće neispravno ignorirati pomeranje fokusa na glavnu kontrolu ili kontrolu unutar nje na primer pomicanje sa kontrole na njenu unutrašnju stavku popisa ili ćeliju mreže. (#14611)
    * Napomena međutim da se ova ispravka primenjuje samo kada je opcija "Automatsko postavljanje fokusa na stavke koje se mogu fokusirati" u postavkama modusa pretraživanja isključena (što je podrazumevano postaka).
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

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Predložene konvencije dodane su specifikaciji manifesta dodataka.
Oni su opcionalni za NVDA kompatibilnost, ali se potiču ili zahtijevaju za slanje u Trgovinu dodataka. (#14754)
  * Upotrijebite 'lowerCamelCase' za polje naziva.
  * Use `&lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;` format for the version field (required for add-on datastore).
  * Upotrijebite 'https://' kao shemu za polje url-a (obavezno za spremište podataka dodataka).
* Dodana je nova vrsta točke proširenja pod nazivom 'Chain', koja se može koristiti za ponavljanje iterables koje vraćaju registrirani rukovatelji. (#14531)
* Dodana je točka proširenja 'bdDetect.scanForDevices'.
Mogu se registrirati rukovatelji koji daju parove "BrailleDisplayDriver/DeviceMatch" koji se ne uklapaju u postojeće kategorije, kao što su USB ili Bluetooth. (#14531)
* Dodana točka proširenja: 'synthDriverHandler.synthChanged'. (#14618)
* NVDA Synth Settings Ring sada predmemorira dostupne vrijednosti postavki kada su prvi put potrebne, a ne prilikom učitavanja sintisajzera. (#14704)
* Sada možete pozvati metodu izvoza na mapi gesta da biste je izvezli u rječnik.
Ovaj se rječnik može uvesti u drugu gestu tako da ga proslijedite konstruktoru 'GlobalGestureMap' ili metodi ažuriranja na postojećoj karti. (#14582)
* 'hwIo.base.IoBase' i njegovi derivati sada imaju novi parametar konstruktora za uzimanje 'hwIo.ioThread.IoThread'.
Ako nije navedeno, koristi se zadani niz. (#14627)
* 'hwIo.ioThread.IoThread' sada ima metodu 'setWaitableTimer' za postavljanje mjerača vremena za čekanje pomoću python funkcije.
Slično tome, nova metoda 'getCompletionRoutine' omogućuje vam sigurno pretvaranje python metode u rutinu dovršavanja. (#14627)
* 'Kompenzacije. OffsetsTextInfo._get_boundingRects' bi sada uvijek trebao vratiti 'List[locationHelper.rectLTWH]' kao što se i očekivalo za podklasu 'textInfos.TextInfo'. (#12424)
* 'highlight-color' sada je atribut polja formata. (#14610)
* NVDA bi trebao točnije utvrditi dolazi li zabilježena poruka iz NVDA jezgre. (#14812)
* NVDA više neće bilježiti netočna upozorenja ili pogreške o zastarjelim appModules. (#14806)
* Sve NVDA proširene točke sada su ukratko opisane u novom, posvećenom poglavlju u Vodiču za razvojne programere. (#14648)
* 'scons checkpot' više neće provjeravati podmapu 'userConfig'. (#14820)
* Prevodivi nizovi sada se mogu definirati u obliku jednine i množine koristeći 'ngettext' i 'npgettext'. (#12445)

#### Zastarjelosti

* Prosljeđivanje lambda funkcija u 'hwIo.ioThread.IoThread.queueAsApc' je zastarjelo.
Umjesto toga, funkcije bi trebale biti slabo referentne. (#14627)
* Uvoz 'LPOVERLAPPED_COMPLETION_ROUTINE' iz 'hwIo.base' je zastario.
Umjesto toga uvezite s 'hwIo.ioThread'. (#14627)
* 'IoThread.autoDeleteApcReference' je zastario.
Predstavljen je u NVDA 2023.1 i nikada nije trebao biti dio javnog API-ja.
Do uklanjanja se ponaša kao no-op, tj. (#14924)
* 'Gui. MainFrame.onAddonsManagerCommand' je zastario, koristite 'gui. MainFrame.onAddonStoreCommand'. (#13985)
* 'speechDictHandler.speechDictVars.speechDictsPath' je zastario, umjesto toga koristite 'NVDAState.WritePaths.speechDictsDir'. (#15021)
* Uvoz 'voiceDictsPath' i 'voiceDictsBackupPath' iz 'speechDictHandler.dictFormatUpgrade' je zastario.
Umjesto toga koristite 'WritePaths.voiceDictsDir' i 'WritePaths.voiceDictsBackupDir' iz 'NVDAState'. (#15048)
* 'config.CONFIG_IN_LOCAL_APPDATA_SUBKEY' je zastarjelo.
Umjesto toga koristite 'config. RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY'. (#15049)

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

* U ovoj inačici narušena je kompatibilnost s postojećim dodacima.

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

### Promjene za programere

Napomena: ovo je izdanje koje krši kompatibilnost dodatnog API-ja.
Dodatke će trebati ponovno testirati i ažurirati njihov manifest.
Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Testovi sustava sada bi trebali proći kada se pokreću lokalno na sustavima koji nisu engleski. (#13362)
* U sustavu Windows 11 na ARM-u, x64 aplikacije više nisu identificirane kao ARM64 aplikacije. (#14403)
* Više nije potrebno koristiti 'SearchField' i 'SuggestionListItem' 'UIA' 'NVDAObjects' u novim scenarijima automatizacije korisničkog sučelja, gdje je automatsko izvješćivanje o prijedlozima pretraživanja i gdje je tipkanje izloženo putem automatizacije korisničkog sučelja s obrascem 'controllerFor'.
Ova je funkcija sada dostupna općenito putem 'ponašanja. EditableText' i osnovni 'NVDAObject'. (#14222)
* Kategorija zapisivanja pogrešaka UIA kada je omogućena sada proizvodi znatno više zapisivanja za rukovatelje događajima UIA i uslužne programe. (#14256)
* Ažurirani su standardi izrade NVDAHelpera. (#13072)
  * Sada koristi standard C++20, bio je C++17.
  * Sada koristi zastavicu kompajlera '/permissive-' koja onemogućuje permisivno ponašanje i postavlja opcije kompajlera '/Zc' za strogu usklađenost.
* Neki objekti dodataka (npr. upravljački programi i dodaci) sada imaju informativniji opis u NVDA python konzoli. (#14463)
* NVDA se sada može u potpunosti kompajlirati sa Visual Studio 2022 i više ne zahtijeva alate za izradu Visual Studio 2019. (#14326)
* Detaljnije bilježenje NVDA zamrzava se kako bi se olakšalo otklanjanje pogrešaka. (#14309)
* Klasa singleton 'braille._BgThread' zamijenjena je klasom 'hwIo.ioThread.IoThread'. (#14130)
  * Jedna instanca 'hwIo.bgThread' (u NVDA jezgri) ove klase pruža pozadinske ulaze/izlaze za upravljačke programe za Brailleovo pismo.
  * Ova nova klasa nije jedinstvena po dizajnu, autori dodataka potiču se da koriste vlastitu instancu kada rade hardverske i/o.
* Arhitektura procesora za računalo može se upitati iz atributa "winVersion.WinVersion.processorArchitecture". (#14439)
* Dodane su nove točke proširenja. (#14503)
  * 'inputCore.decide_executeGesture'
  * 'tones.decide_beep'
  * 'nvwave.decide_playWaveFile'
  * 'braille.pre_writeCells'
  * 'braille.filter_displaySize'
  * 'braille.decide_enabled'
  * 'braille.displayChanged'
  * 'braille.displaySizeChanged'
* Moguće je postaviti useConfig na False na podržanim postavkama za upravljački program sintisajzera. (#14601)

#### Promjene koje prekidaju API

To su pokvarene promjene API-ja.
Otvorite problem s GitHubom ako vaš dodatak ima problema s ažuriranjem na novi API.

* Specifikacija konfiguracije je promijenjena, ključevi su uklonjeni ili izmijenjeni:
  * U odjeljku '[documentFormatting]' (#14233):
    * 'reportLineIndentation' pohranjuje int vrijednost (0 do 3) umjesto logičke vrijednosti
    * 'reportLineIndentationWithTones' je uklonjen.
    * 'reportBorderStyle' i 'reportBorderColor' uklonjeni su i zamijenjeni su s 'reportCellBorders'.
  * U odjeljku '[Brailleovo pismo]' (#14233):
    * 'noMessageTimeout' je uklonjen, zamijenjen vrijednošću za 'showMessages'.
    * 'messageTimeout' više ne može primati vrijednost 0, zamijenjena vrijednošću za 'showMessages'.
    * 'autoTether' je uklonjen; 'tetherTo' sada umjesto toga može uzeti vrijednost "auto".
  * U odjeljku '[tipkovnica]' (#14528):
    * 'useCapsLockAsNVDAModifierKey', 'useNumpadInsertAsNVDAModifierKey', 'useExtendedInsertAsNVDAModifierKey' su uklonjeni.
    Zamjenjuju se s 'NVDAModifierKeys'.
* Klasa 'NVDAHelper.RemoteLoader64' uklonjena je bez zamjene. (#14449)
* Sljedeće funkcije u 'winAPI.sessionTracking' uklanjaju se bez zamjene. (#14416, #14490)
  * 'isWindowsLocked'
  * 'handleSessionChange'
  * 'odjaviti'
  * 'Registar'
  * 'isLockStateSuccessfullyTracked'
* Više nije moguće omogućiti/onemogućiti rukovatelj brajicom postavljanjem 'braille.handler.enabled'.
Da biste programski onemogućili rukovatelj brajicom, registrirajte rukovatelj na 'braille.handler.decide_enabled'. (#14503)
* Više nije moguće ažurirati veličinu zaslona rukovatelja postavljanjem 'braille.handler.displaySize'.
Da biste programski ažurirali displaySize, registrirajte rukovatelj na 'braille.handler.filter_displaySize'.
Pogledajte 'brailleViewer' za primjer kako to učiniti. (#14503)
* Došlo je do promjena u korištenju 'addonHandler.Addon.loadModule'. (#14481)
  * 'loadModule' sada očekuje točku kao razdjelnik, a ne obrnutu kosu crtu.
  Na primjer "lib.example" umjesto "lib\example".
  * 'loadModule' sada postavlja iznimku kada se modul ne može učitati ili ima pogreške, umjesto da tiho vraća 'None' bez davanja informacija o uzroku.
* Sljedeći simboli uklonjeni su iz 'appModules.foobar2000' bez izravne zamjene. (#14570)
  * 'statusBarTimes'
  * 'parseIntervalToTimestamp'
  * 'getOutputFormat'
  * 'getParsingFormat'
* Sljedeći više nisu singletoni - njihova metoda dobivanja je uklonjena.
Upotreba 'Example.get()' sada je 'Example()'. (#14248)
  * 'UIAHandler.customAnnotations.CustomAnnotationTypesCommon'
  * 'UIAHandler.customProps.CustomPropertiesCommon'
  * 'NVDAObjects.UIA.excel.ExcelCustomProperties'
  * 'NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes'

#### Zastarjelosti

* 'NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA' je zastario i ne preporučuje se korištenje. (#14047)
* 'config.addConfigDirsToPythonPackagePath' je premješten.
Umjesto toga upotrijebite 'addonHandler.packaging.addDirsToPythonPackagePath'. (#14350)
* 'Brailleovo pismo. BrailleHandler.TETHER_*' su zastarjeli.
Umjesto toga upotrijebite 'configFlags.TetherTo.*.value'. (#14233)
* 'utils.security.postSessionLockStateChanged' je zastario.
Umjesto toga upotrijebite 'utils.security.post_sessionLockStateChanged'. (#14486)
* 'NVDAObject.hasDetails', 'NVDAObject.detailsSummary', 'NVDAObject.detailsRole' je zastario.
Umjesto toga koristite 'NVDAObject.annotations'. (#14507)
* 'keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS' je zastario bez izravne zamjene.
Razmislite o korištenju klase 'config.configFlags.NVDAKey' umjesto toga. (#14528)
* 'Gui. MainFrame.evaluateUpdatePendingUpdateMenuItemCommand' je zastario.
Koristite 'gui. MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand'. (#14523)

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

### Promjene za programere

Molimo pogledajte [vodič za razvojne programere](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) za informacije o postupku zastarjelosti i uklanjanja NVDA API-ja.

* Kreirana je [Mailing lista NVDA API-ja](https://groups.google.com/a/nvaccess.org/g/nvda-api/about). (#13999)
* NVDA više ne obrađuje 'textChange' događaje za većinu aplikacija za automatizaciju korisničkog sučelja zbog njihovog ekstremnog negativnog utjecaja na performanse. (#11002, #14067)

#### Zastarjelosti

* 'core.post_windowMessageReceipt' je zastarjelo, umjesto toga koristite 'winAPI.messageWindow.pre_handleWindowMessage'.
* 'winKernel.SYSTEM_POWER_STATUS' je zastarjelo i upotreba se ne preporučuje, ovo je premješteno u 'winAPI._powerTracking.SystemPowerStatus'.
* Konstante 'winUser.SM_*' su zastarjele, umjesto toga upotrijebite 'winAPI.winUser.constants.SystemMetrics'.

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

### Promjene za programere

#### Zastarjelosti

* 'utils.security.isObjectAboveLockScreen(obj)' je zastario, umjesto toga koristite 'obj.isBelowLockScreen'. (#14416)
* Sljedeće funkcije u 'winAPI.sessionTracking' zastarjele su za uklanjanje u 2023.1. (#14416)
  * 'isWindowsLocked'
  * 'handleSessionChange'
  * 'odjaviti'
  * 'Registar'
  * 'isLockStateSuccessfullyTracked'

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

### Promjene za programere

* Ažurirani Comtypes na verziju 1.1.11. (#12953)
* U verzijama Windows konzole ('conhost.exe') s NVDA API-jem razine 2 ('FORMATTED') ili većom, kao što su one uključene u Windows 11 verziju 22H2 (Sun Valley 2), automatizacija korisničkog sučelja sada se koristi prema zadanim postavkama. (#10964)
  * To se može poništiti promjenom postavke "Podrška za Windows konzolu" na NVDA ploči naprednih postavki.
  * Da biste pronašli razinu NVDA API-ja na Windows konzoli, postavite "Podrška za Windows konzolu" na "UIA kada je dostupna", a zatim provjerite NVDA+F1 dnevnik otvoren iz pokrenute instance Windows konzole.
* Chromium virtualni međuspremnik sada se učitava čak i kada objekt dokumenta ima MSAA 'STATE_SYSTEM_BUSY' izložen putem IA2. (#13306)
* Kreiran je tip konfiguracijske specifikacije 'featureFlag' za korištenje s eksperimentalnim značajkama u NVDA. Pogledajte 'devDocs/featureFlag.md' za više informacija. (#13859)

#### Zastarjelosti

U 2022.3 nisu predložene zastarjelosti.

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

### Promjene za programere

#### Zastarjelosti

Uklanjanje ovih zastarjelih trenutačno nije zakazano.
Zastarjeli aliasi ostat će do daljnjeg.
Testirajte novi API i pošaljite povratne informacije.
Za autore dodataka, otvorite problem s GitHubom ako te promjene spriječe API da zadovolji vaše potrebe.

* 'appModules.lockapp.LockAppObject' treba zamijeniti s 'NVDAObjects.lockscreen.LockScreenObject'. (GHSA-rmq3-vvhq-gp32)
* 'appModules.lockapp.AppModule.SAFE_SCRIPTS' treba zamijeniti s 'utils.security.getSafeScripts()'. (GHSA-rmq3-vvhq-gp32)

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

### Promjene za programere

* Sada je podržano kompajliranje NVDA ovisnosti sa Visual Studio 2022 (17.0).
Za razvojne i izdane međuverzije i dalje se koristi Visual Studio 2019. (#13033)
* Prilikom dohvaćanja broja odabrane djece putem accSelectiona,
slučaj u kojem je negativan ID djeteta ili IDispatch vraćen putem 'IAccessible::get_accSelection' sada se ispravno obrađuje. (#13277)
* Nove praktične funkcije 'registerExecutableWithAppModule' i 'unregisterExecutable' dodane su modulu 'appModuleHandler'.
Mogu se koristiti za korištenje jednog modula aplikacije s više izvršnih datoteka. (#13366)

#### Zastarjelosti

Ovo su predložene promjene API-ja.
Zastarjeli dio API-ja i dalje će biti dostupan do navedenog izdanja.
Ako nije navedeno puštanje, plan uklanjanja nije određen.
Imajte na umu da je plan za uklanjanje "najbolji napor" i može biti podložan promjenama.
Testirajte novi API i pošaljite povratne informacije.
Za autore dodataka, otvorite problem s GitHubom ako te promjene spriječe API da zadovolji vaše potrebe.

* 'appModuleHandler.NVDAProcessID' je zastario, umjesto toga koristite 'globalVars.appPid'. (#13646)
* 'gui.quit' je zastario, koristite 'wx. CallAfter(mainFrame.onExitCommand, None)' umjesto toga. (#13498)
  -
* Neki aliasi appModules označeni su kao zastarjeli.
Kod koji se uvozi iz jednog od njih, umjesto toga treba uvesti iz zamjenskog modula.  (#13366)

| Uklonjen naziv modula |Zamjenski modul|
|---|---|
|AzuredataStudio |kod|
|azuredatastudio-insiders |kod|
|kalkulatorapp |kalkulator|
|kod - insajderi |kod|
|commsapps |hxmail|
|dbeaver |pomrčina|
|digitaleditionspreview |digitaleditions|
|esybraille |esysuite|
|hxoutlook |hxmail|
|miranda64 |miranda32|
|mpc-hc |mplayerc|
|MPC-HC64 |mplayerc|
|notepad++ |notepadPlusPlus|
|searchapp |searchui|
|searchhost |searchui|
|springtoolsuite4 |pomrčina|
|STS |pomrčina|
|Teamtalk3 |teamtalk4classic|
|TextInputHost |windowsinternal_composableshell_experiences_textinput_inputapp|
|ukupnocmd64 |ukupnocmd|
|win32calc |calc|
|winmail |msimn|
|zend-eclipse-php |eclipse|
|zendstudio |eclipse|

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
* Prijavljivanje kada objekat  "ima detalje " kao i odgovarajuća komanda za prijavljivanje odnosa detalja sada se mogu koristiti u režimu fokusiranja. (#13106)
* Seika brajična bilježnica se sada može automatski prepoznati putem USB i Bluetooth veze. (#13191, #13142)
  * Ovo utiče na slijedeće uređaje: MiniSeika (16, 24 znakova), V6, i V6Pro (40 znakova)
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
* `NVDA+numerička tipka za brisanje ` podrazumjevano prijavljuje lokaciju kursora ili fokusiranog objekta. (#13060)
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

### Promjene za programere

* Napomena: ovo je izdanje koje krši kompatibilnost dodatnog API-ja. Dodatke će trebati ponovno testirati i ažurirati njihov manifest.
* Iako NVDA i dalje zahtijeva Visual Studio 2019, međuverzije više ne bi trebale propasti ako je uz 2019. instalirana novija verzija Visual Studija (npr. 2022). (#13033, #13387)
* Ažurirani SConi na verziju 4.3.0. (#13033)
* Ažuriran py2exe na verziju 0.11.1.0. (#13510)
* "NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable" je uklonjeno. Umjesto toga upotrijebite 'apiLevel'. (#12955, #12660)
* 'TVItemStruct' je uklonjen iz 'sysTreeView32'. (#12935)
* 'MessageItem' je uklonjen iz Outlook appModule. (#12935)
* Konstante 'audioDucking.AUDIODUCKINGMODE_*' sada su 'DisplayStringIntEnum'. (#12926)
  * upotrebe treba zamijeniti s 'AudioDuckingMode.*'
  * korištenje 'audioDucking.audioDuckingModes' treba zamijeniti s 'AudioDuckingMode.*.displayString'
* Korištenje konstanti 'audioDucking.ANRUS_ducking_*' treba zamijeniti s 'ANRUSDucking.*'. (#12926)
* Promjene 'synthDrivers.sapi5' (#12927):
  * Upotreba 'SPAS_*' trebala bi biti zamijenjena s 'SPAudioState.*'
  * 'konstante. SVSF*' treba zamijeniti s 'SpeechVoiceSpeakFlags.*'
    * Napomena: "SVSFlagsAsync" treba zamijeniti s "SpeechVoiceSpeakFlags.Async", a ne "SpeechVoiceSpeakFlags.lagsAsync"
  * 'konstante. Korištenje SVE*' treba zamijeniti s 'SpeechVoiceEvents.*'
* AppModule 'soffice' ima uklonjene sljedeće klase i funkcije 'JAB_OOTableCell', 'JAB_OOTable', 'gridCoordStringToNumbers'. (#12849)
* 'Jezgra. CallCancelled' je sada 'iznimke. Poziv otkazan'. (#12940)
* Sve konstante koje počinju s RPC iz 'core' i 'logHandler' premještaju se u 'RPCConstants.RPC' enum. (#12940)
* Preporučuje se da se funkcije 'mouseHandler.doPrimaryClick' i 'mouseHandler.doSecondaryClick' koriste za klikanje mišem za izvođenje logičke radnje kao što je aktiviranje (primarno) ili sekundarno (prikaz kontekstnog izbornika),
umjesto korištenja 'executeMouseEvent' i specificiranja lijeve ili desne tipke miša.
To osigurava da će kod poštovati korisničku postavku sustava Windows za zamjenu primarne tipke miša. (#12642)
* 'config.getSystemConfigPath' je uklonjen - nema zamjene. (#12943)
* 'Shlobj. SHGetFolderPath' je uklonjen - molimo koristite 'shlobj. SHGetKnownFolderPath' umjesto toga. (#12943)
* Konstante 'shlobj' su uklonjene. Stvoren je novi enum, 'shlobj. FolderId' za korištenje s 'SHGetKnownFolderPath'. (#12943)
* "diffHandler.get_dmp_algo" i "diffHandler.get_difflib_algo" zamjenjuju se slovima "diffHandler.prefer_dmp" i "diffHandler.prefer_difflib". (#12974)
* 'languageHandler.curLang' je uklonjen - za dobivanje trenutnog NVDA jezika koristite 'languageHandler.getLanguage()'. (#13082)
* Metoda 'getStatusBarText' može se implementirati na appModule kako bi se prilagodio način na koji NVDA dohvaća tekst sa statusne trake. (#12845)
* 'globalVars.appArgsExtra' je uklonjen. (#13087)
  * Ako vaš dodatak mora obraditi dodatne argumente naredbenog retka, pojedinosti potražite u dokumentaciji 'addonHandler.isCLIParamKnown' i vodiču za razvojne programere.
* UIA modul za rukovanje i drugi moduli za podršku UIA sada su dio UIAHandler paketa. (#10916)
  * 'UIAUtils' je sada 'UIAHandler.utils'
  * 'UIABrowseMode' sada je 'UIAHandler.browseMode'
  * '_UIAConstants' je sada 'UIAHandler.constants'
  * '_UIACustomProps' je sada 'UIAHandler.customProps'
  * '_UIACustomAnnotations' je sada 'UIAHandler.customAnnotations'
* Konstante 'IAccessibleHandler' 'IA2_RELATION_*' zamijenjene su enumom 'IAccessibleHandler.RelationType'. (#13096)
  * Uklonjeno 'IA2_RELATION_FLOWS_FROM'
  * Uklonjeno 'IA2_RELATION_FLOWS_TO'
  * Uklonjeno 'IA2_RELATION_CONTAINING_DOCUMENT'
* 'LOCALE_SLANGUAGE', 'LOCALE_SLIST' i 'LOCALE_SLANGDISPLAYNAME' uklonjeni su iz 'languageHandler' - umjesto toga koristite članove 'languageHandler.LOCALE'. (#12753)
* Prebačen s Minhooka na Microsoft Detours kao biblioteku za spajanje za NVDA. Spajanje s ovom bibliotekom uglavnom se koristi za pomoć modelu zaslona. (#12964)
* 'winVersion.WIN10_RELEASE_NAME_TO_BUILDS' se uklanja. (#13211)
* SCons sada upozorava na izgradnju s brojem poslova koji je jednak broju logičkih procesora u sustavu.
To može dramatično smanjiti vrijeme izrade na višejezgrenim sustavima. (#13226, #13371)
* Konstante 'characterProcessing.SYMLVL_*' su uklonjene - umjesto toga koristite 'characterProcessing.SymbolLevel.*'. (#13248)
* Funkcije 'loadState' i 'saveState' uklonjene su iz addonHandlera - umjesto toga koristite 'addonHandler.state.load' i 'addonHandler.state.save'. (#13245)
* Premješten je UWP/OneCore sloj interakcije NVDAHelpera [iz C++/CX u C++/Winrt](https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx). (#10662)
* Sada je obavezno podrazred 'DictionaryDialog' da biste ga koristili. (#13268)
* 'config. RUN_REGKEY', 'config. NVDA_REGKEY' su zastarjeli, upotrijebite 'config. RegistryKey.RUN', 'config. RegistryKey.NVDA'. Oni će biti uklonjeni 2023. godine. (#13242)
* 'easeOfAccess.ROOT_KEY', 'easeOfAccess.APP_KEY_PATH' su zastarjeli, umjesto toga koristite 'easeOfAccess.RegistryKey.ROOT', 'easeOfAccess.RegistryKey.APP'. Oni će biti uklonjeni 2023. godine. (#13242)
* 'easeOfAccess.APP_KEY_NAME' je zastario i bit će uklonjen 2023. (#13242)
* 'DictionaryDialog' i 'DictionaryEntryDialog' premješteni su iz 'gui.settingsDialogs' u 'gui.speechDict'. (#13294)
* Odnosi IAccessible2 sada se prikazuju u informacijama za razvojne inženjere za objekte IAccessible2. (#13315)
* 'languageHandler.windowsPrimaryLCIDsToLocaleNames' je uklonjen, umjesto toga koristite 'languageHandler.windowsLCIDToLocaleName' ili 'winKernel.LCIDToLocaleName'. (#13342)
* Svojstvo 'UIAAutomationId' za UIA objekte treba imati prednost u odnosu na 'cachedAutomationId'. (#13125, #11447)
  * 'cachedAutomationId' može se koristiti ako se dobije izravno iz elementa.
* 'NVDAObjects.window.scintilla.CharacterRangeStruct' premješteno je u 'NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct'. (#13364)
* Booleov 'gui.isInMessageBox' je uklonjen, umjesto toga koristite funkciju 'gui.message.isModalMessageBoxActive'. (#12984, #13376)
* 'controlTypes' je podijeljen u različite podmodule. (#12510, #13588)
  * "ROLE_*" i "STATE_*" zamjenjuju se s "Uloga.*" i "Država.*".
  * Iako je još uvijek dostupan, sljedeće bi se trebalo smatrati zastarjelim:
    * 'ROLE_*' i 'STATE_*', umjesto toga koristite 'Role.*' i 'State.*'.
    * 'roleLabels', 'stateLabels' i 'negativeStateLabels', upotrebe kao što su 'roleLabels[ROLE_*]' treba zamijeniti njihovim ekvivalentom 'Role.*.displayString' ili 'State.*.negativeDisplayString'.
    * 'processPositiveStates' i 'processNegativeStates' trebali bi umjesto toga koristiti 'processAndLabelStates'.
* Konstante stanja ćelije programa Excel ("NVSTATE_*") sada su vrijednosti u enumu 'NvCellState', zrcaljene u enumu 'NvCellState' u 'NVDAObjects/window/excel.py' i mapirane u 'controlTypes.State' putem _nvCellStatesToStates. (#13465)
* 'EXCEL_CELLINFO' struct member 'state' sada je 'nvCellStates'.
* 'mathPres.ensureInit' je uklonjen, MathPlayer je sada inicijaliziran kada se NVDA pokrene. (#13486)

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
  * wx GUI inspection alat je sada onemogućena u sigurnom načinu rada.

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

### Promjene za programere

* Za izgradnju NVDA sada je potreban Visual Studio 2019 16.10.4 ili noviji.
Da biste odgovarali proizvodnom okruženju za međuverziju, ažurirajte Visual Studio da bi bio sinkroniziran s [trenutnom verzijom koju koristi AppVeyor](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019). (#12728)
* 'NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable' zastario je za uklanjanje u 2022.1. (#12660)
  * Umjesto toga upotrijebite 'apiLevel' (za detalje pogledajte komentare na '_UIAConstants.WinConsoleAPILevel').
* Prozirnost boje pozadine teksta koja potječe iz GDI aplikacija (putem modela prikaza), sada je izložena za dodatke ili appModules. (#12658)
* 'LOCALE_SLANGUAGE', 'LOCALE_SLIST' i 'LOCALE_SLANGDISPLAYNAME' premještaju se u 'LOCALE' enum u languageHandleru.
I dalje su dostupni na razini modula, ali su zastarjeli i treba ih ukloniti u NVDA 2022.1. (#12753)
* Korištenje funkcija 'addonHandler.loadState' i 'addonHandler.saveState' trebalo bi zamijeniti njihovim ekvivalentima 'addonHandler.state.save' i 'addonHandler.state.load' prije 2022.1. (#12792)
* Izlaz Brailleovog pisma sada se može provjeriti u testovima sustava. (#12917)

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

### Promjene za programere

* Konstante "characterProcessing.SYMLVL_*" trebalo bi zamijeniti njihovim ekvivalentom "SymbolLevel.*" prije 2022.1. (#11856, #12636)
* 'controlTypes' je podijeljen u različite podmodule, simboli označeni za zastarjelo moraju se zamijeniti prije 2022.1. (#12510)
  * Konstante "ROLE_*" i "STATE_*" trebalo bi zamijeniti ekvivalentnim "Uloga.*" i "Država.*".
  * 'roleLabels', 'stateLabels' i 'negativeStateLabels' su zastarjeli, upotrebe kao što su 'roleLabels[ROLE_*]' trebale bi se zamijeniti njihovim ekvivalentom 'Role.*.displayString' ili 'State.*.negativeDisplayString'.
  * 'processPositiveStates' i 'processNegativeStates' su zastarjeli za uklanjanje.
* U sustavu Windows 10 verzije 1511 i novijim verzijama (uključujući međuverzije programa Insider Preview) naziv trenutnog izdanja ažuriranja značajki sustava Windows dobiva se iz registra sustava Windows. (#12509)
* Zastarjelo: 'winVersion.WIN10_RELEASE_NAME_TO_BUILDS' bit će uklonjen 2022.1, nema izravne zamjene. (#12544)

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
* Podrška za Seika brajičnu bilježnicu tvrtke Nippon Telesoft. (#11514)

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

### Promjene za programere

* Napomena: ovo je izdanje koje krši kompatibilnost dodatnog API-ja. Dodatke će trebati ponovno testirati i ažurirati njihov manifest.
* NVDA-in sustav izrade sada dohvaća sve Python ovisnosti s pip-om i pohranjuje ih u Python virtualno okruženje. Sve se to radi transparentno.
  * Za izgradnju NVDA-a, SConi bi se trebali nastaviti koristiti na uobičajeni način. Npr. izvršavanje scons.bat u korijenu repozitorija. Pokretanje 'py -m SCons' više nije podržano, a 'scons.py' je također uklonjeno.
  * Za pokretanje NVDA iz izvora, umjesto izravnog izvršavanja 'source/nvda.pyw', programer bi sada trebao koristiti 'runnvda.bat' u korijenu repozitorija. Ako pokušate izvršiti 'source/nvda.pyw', okvir s porukom će vas upozoriti da više nije podržan.
  * To perform unit tests, execute `rununittests.bat [&lt;extra unittest discover options&gt;]`
  * To perform system tests: execute `runsystemtests.bat [&lt;extra robot options&gt;]`
  * To perform linting, execute `runlint.bat &lt;base branch&gt;`
  * Za više detalja pogledajte readme.md.
* Sljedeće Python ovisnosti također su nadograđene:
  * Komtipovi ažurirani na 1.1.8.
  * pySerial ažuriran na 3.5.
  * wxPython ažuriran na 4.1.1.
  * Py2exe ažuriran na 0.10.1.0.
* 'LiveText._getTextLines' je uklonjeno. (#11639)
  * Umjesto toga, nadjačajte '_getText' koji vraća niz svih tekstova u objektu.
* Objekti 'LiveText' sada mogu izračunati razlike po znaku. (#11639)
  * Da biste promijenili ponašanje diff za neki objekt, nadjačajte svojstvo 'diffAlgo' (pogledajte docstring za detalje).
* Kada definirate skriptu pomoću dekoratora skripte, može se navesti logički argument 'allowInSleepMode' kako bi se kontroliralo je li skripta dostupna u stanju mirovanja ili ne. (#11979)
* Sljedeće funkcije su uklonjene iz konfiguracijskog modula. (#11935)
  * canStartOnSecureScreens - umjesto toga koristite config.isInstalledCopy.
  * hasUiAccess i execElevated - koristite ih iz modula systemUtils.
  * getConfigDirs - umjesto toga koristite globalVars.appArgs.configPath.
* Konstante REASON_* razine modula uklanjaju se iz controlTypes – umjesto toga koristite controlTypes.OutputReason. (#11969)
* REASON_QUICKNAV je uklonjen iz browseMode – umjesto toga upotrijebite controlTypes.OutputReason.QUICKNAV. (#11969)
* 'NVDAObject' (i izvedenice) svojstvo 'isCurrent' sada strogo vraća klasu Enum 'controlTypes.IsCurrent'. (#11782)
  * 'isCurrent' više nije Optional i stoga neće vratiti None.
    * Kada objekt nije aktualan, vraća se 'controlTypes.IsCurrent.NO'.
* Mapiranje 'controlTypes.isCurrentLabels' je uklonjeno. (#11782)
  * Umjesto toga, upotrijebite svojstvo 'displayString' na vrijednosti enuma 'controlTypes.IsCurrent'.
    * Na primjer: 'controlTypes.IsCurrent.YES.displayString'.
* 'winKernel.GetTimeFormat' je uklonjen - umjesto toga koristite 'winKernel.GetTimeFormatEx'. (#12139)
* 'winKernel.GetDateFormat' je uklonjen - umjesto toga koristite 'winKernel.GetDateFormatEx'. (#12139)
* 'Gui. DriverSettingsMixin' je uklonjen - koristite 'gui. AutoSettingsMixin'. (#12144)
* 'speech.getSpeechForSpelling' je uklonjen - koristite 'speech.getSpellingSpeech'. (#12145)
* Naredbe se ne mogu izravno uvesti iz govora kao 'uvoz govora; govor. ExampleCommand()' ili 'uvoz speech.manager; speech.manager.ExampleCommand()' - umjesto toga upotrijebite 'from speech.commands import ExampleCommand'. (#12126)
* 'speakTextInfo' više neće slati govor putem 'speakWithoutPauses' ako je razlog 'SAYALL', jer 'SayAllHandler' to sada radi ručno. (#12150)
* Modul 'synthDriverHandler' više nije uvezen zvjezdicom u 'globalCommands' i 'gui.settingsDialogs' - umjesto toga koristite 'from synthDriverHandler import synthFunctionExample'. (#12172)
* 'ROLE_EQUATION' je uklonjen iz controlTypes - umjesto toga koristite 'ROLE_MATH'. (#12164)
* Klase 'autoSettingsUtils.driverSetting' uklonjene su iz 'driverHandler' - koristite ih iz 'autoSettingsUtils.driverSetting'. (#12168)
* Klase 'autoSettingsUtils.utils' uklonjene su iz 'driverHandler' - koristite ih iz 'autoSettingsUtils.utils'. (#12168)
* Podrška za 'TextInfo's koji ne nasljeđuju od 'contentRecog.BaseContentRecogTextInfo' je uklonjena. (#12157)
* 'speech.speakWithoutPauses' je uklonjen - umjesto toga koristite 'speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses'. (#12195, #12251)
* 'speech.re_last_pause' je uklonjeno - umjesto toga koristite 'speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause'. (#12195, #12251)
* 'WelcomeDialog', 'LauncherDialog' i 'AskAllowUsageStatsDialog' premješteni su u 'gui.startupDialogs'. (#12105)
* 'getDocFilePath' je premješten iz 'gui' u modul 'documentationUtils'. (#12105)
* Modul gui.accPropServer kao i klase AccPropertyOverride i ListCtrlAccPropServer iz modula gui.nvdaControls uklonjeni su u korist WX izvorne podrške za nadjačavanje svojstava pristupačnosti. Kada poboljšavate pristupačnost WX kontrola, implementirajte wx. Umjesto toga pristupačan. (#12215)
* Datoteke u 'source/comInterfaces/' sada se lakše koriste alatima za razvojne programere kao što su IDE. (#12201)
* Praktične metode i vrste dodane su u winVersion modul za dohvaćanje i usporedbu verzija sustava Windows. (#11909)
  * isWin10 funkcija pronađena u winVersion modulu je uklonjena.
  * class winVersion.WinVersion je usporediv tip koji se može naručiti koji obuhvaća informacije o verziji sustava Windows.
  * Dodana je funkcija winVersion.getWinVer kako bi se dobila winVersion.WinVersion koja predstavlja trenutno pokrenuti OS.
  * Za poznata izdanja sustava Windows dodane su konstante praktičnosti, pogledajte konstante winVersion.WIN*.
* IAccessibleHandler više ne uvozi sve iz IAccessible i IA2 COM sučelja - koristite ih izravno. (#12232)
* TextInfo objects now have start and end properties which can be compared mathematically with operators such as &lt; &lt;= == != &gt;= &gt;. (#11613)
  * E.g. ti1.start &lt;= ti2.end
  * This usage is now prefered instead of ti1.compareEndPoints(ti2,"startToEnd") &lt;= 0
* Početna i završna svojstva TextInfo također se mogu međusobno postaviti. (#11613)
  * Npr. ti1.start = ti2.kraj
  * Ova upotreba je poželjnija umjesto ti1. SetEndPoint(ti2;"startToEnd")
* 'wx. CENTRE_ON_SCREEN' i 'wx. CENTER_ON_SCREEN' su uklonjeni, koristite 'self. CentreOnScreen()'. (#12309)
* 'easeOfAccess.isSupported' je uklonjen, NVDA podržava samo verzije Windowsa za koje se to procjenjuje kao 'True'. (#12222)
* 'sayAllHandler' je premješten u 'speech.sayAll'. (#12251)
  * 'speech.sayAll.SayAllHandler' izlaže funkcije 'stop', 'isRunning', 'readObjects', 'readText', 'lastSayAllMode'.
  * 'SayAllHandler.stop' također resetira instancu 'SayAllHandler' 'SpeechWithoutPauses'.
  * "CURSOR_REVIEW" i "CURSOR_CARET" zamjenjuju se slovima "CURSOR. RECENZIJA' i 'KURSOR. KARET'.
* 'govor. SpeechWithoutPauses' je premješten u 'speech.speechWithout Pauses.SpeechWithoutPauses'. (#12251)
* 'speech.curWordChars' je preimenovan u 'speech._curWordChars'. (#12395)
* sljedeće je uklonjeno iz 'speech' i može im se pristupiti putem 'speech.getState()'. To su sada vrijednosti samo za čitanje. (#12395)
  * speechMode
  * speechMode_beeps_ms
  * bio je otkazan
  * isPauzirano
* Da biste ažurirali 'speech.speechMode', upotrijebite 'speech.setSpeechMode'. (#12395)
* Sljedeće je premješteno u 'Govor. SpeechMode'. (#12395)
  * 'speech.speechMode_off' postaje 'govor. SpeechMode.off'
  * 'speech.speechMode_beeps' postaje 'govor. SpeechMode.bieps'
  * 'speech.speechMode_talk' postaje 'govor. SpeechMode.talk'
* 'IAccessibleHandler.IAccessibleObjectIdentifierType' sada je 'IAccessibleHandler.types.IAccessibleObjectIdentifierType'. (#12367)
* Sljedeće u 'NVDAObjects.UIA.WinConsoleUIA' je promijenjeno (#12094)
  * 'NVDAObjects.UIA.winConsoleUIA.is21H1Plus' preimenovan 'NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable'.
  * 'NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo' preimenovan je u početni naziv klase velikim slovima.
  * 'NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1' preimenovan 'NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive'
    * Implementacija radi oko obje krajnje točke koje su inkluzivne (u rasponima teksta) prije [microsoft/terminal PR 4018](https://github.com/microsoft/terminal/pull/4018)
    * Zaobilazna rješenja za 'expand', 'collapse', 'compareEndPoints', 'setEndPoint' itd

## 2020.4

Ova inačica uključuje novu metodu unosa za kineski, nadogradnja Liblouisa te popis elemenata (NVDA+f7) u modusu fokusa.
Kontekstualna pomoć od sada je dostupna prilikom pritiska F1 u NVDA dijaloškim okvirima.
Unapređenje pravila čitanja simbola, govornih rječnika, brajičnih poruka i letimičnog čitanja.
Ispravke grešaka i unapređenja za Mail u windowsima 10, outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
Na web stranicama, unapređenja u Google docs, i veća podrška za ARIA.
Te puno drugih važnih ispravaka grešaka  i unapređenja.

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
* U preglednicima temeljenim na Chromiumu riješeno je nekoliko slučajeva u kojima navigacija tablicom nije radila, a NVDA nije izvještavao o broju redaka/stupaca tablice. (#12359)

### Promjene za programere

* Testovi sustava sada mogu slati ključeve pomoću spy.emulateKeyPress, koji uzima identifikator ključa koji je u skladu s NVDA vlastitim imenima ključeva, a prema zadanim postavkama također blokira dok se akcija ne izvrši. (#11581)
* NVDA više ne zahtijeva da trenutni direktorij bude direktorij NVDA aplikacije kako bi mogao funkcionirati. (#6491)
* Postavka uljudnosti arije uživo za žive regije sada se može pronaći na NVDA objektima koristeći svojstvo liveRegionPoliteness. (#11596)
* Sada je moguće definirati zasebne geste za Outlook i Word dokument. (#11196)

## 2020.3

Ovo izdanje uključuje nekoliko velikih poboljšanja stabilnosti i performansi, posebno u aplikacijama sustava Microsoft Office. Postoje nove postavke za prebacivanje podrške za zaslon osjetljiv na dodir i izvješćivanje o grafici.
Postojanje označenog (istaknutog) sadržaja može se prijaviti u preglednicima, a postoje i nove njemačke tablice na Brailleovom pismu.

### Nove značajke

* Sada možete prebaciti izvještavanje o grafici iz NVDA postavki oblikovanja dokumenta. Imajte na umu da će onemogućavanje ove opcije i dalje čitati alternativne tekstove grafike. (#4837)
* Sada možete prebaciti podršku za NVDA zaslon osjetljiv na dodir. Dodana je opcija na zaslon Interakcija dodirom u postavkama NVDA-a. Zadana gesta je NVDA+control+alt+t. (#9682)
* Dodane su nove njemačke tablice na Brailleovom pismu. (#11268)
* NVDA sada detektira UIA kontrole teksta samo za čitanje. (#10494)
* Postojanje označenog (istaknutog) sadržaja prijavljuje se i u govoru i na Brailleovom pismu u svim web-preglednicima. (#11436)
 * To se može uključiti i isključiti novom opcijom NVDA formatiranja dokumenta za isticanje.
* Nove emulirane tipke sistemske tipkovnice mogu se dodati iz NVDA dijaloškog okvira Ulazne geste. (#6060)
  * Da biste to učinili, pritisnite gumb za dodavanje nakon što ste odabrali kategoriju Oponašane tipke sistemske tipkovnice.
* Sada je podržan Handy Tech Active Braille s joystickom. (#11655)
* Postavka "Automatski način fokusiranja za kretanje kurseta" sada je kompatibilna s onemogućavanjem opcije "Automatski postavi fokus na elemente koji se mogu fokusirati". (#11663)

### Promjenama

* Skripta za oblikovanje izvješća (NVDA+f) sada je promijenjena tako da izvještava o oblikovanju u sistemskom kursoru, a ne na položaju kursora za pregled. Za prijavu formatiranja na poziciji kursora za pregled sada koristite NVDA+shift+f. (#9505)
* NVDA više ne postavlja automatski fokus sustava na elemente koji se mogu fokusirati prema zadanim postavkama u načinu pregledavanja, poboljšavajući performanse i stabilnost. (#11190)
* CLDR ažuriran s verzije 36.1 na verziju 37. (#11303)
* Ažuriran eSpeak-NG na 1.51-dev, commit 1fb68ffffea4
* Sada možete koristiti navigaciju tablicom u okvirima popisa sa stavkama popisa koje se mogu označiti kada određeni popis ima više stupaca. (#8857)
* U upravitelju dodataka, kada se od vas zatraži da potvrdite uklanjanje dodatka, "Ne" je sada zadano. (#10015)
* U programu Microsoft Excel dijaloški okvir Popis elemenata sada prikazuje formule u njihovom lokaliziranom obliku. (#9144)
* NVDA sada izvještava o ispravnoj terminologiji za bilješke u MS Excelu. (#11311)
* Kada koristite naredbu "premjesti kursor pregleda u fokus" u načinu pregledavanja, kursor pregleda sada je postavljen na položaj virtualnog kursora. (#9622)
* Informacije prijavljene u načinu pregledavanja, kao što su informacije o formatiranju pomoću NVDA+F, sada se prikazuju u malo većem prozoru centriranom na zaslonu. (#9910)

### Ispravci grešaka

* NVDA sada uvijek govori kada se krećete po riječi i slijećete na bilo koji pojedinačni simbol iza kojeg slijedi razmak, bez obzira na postavke opširnosti. (#5133)
* U aplikacijama koje koriste QT 5.11 ili noviji, opisi objekata ponovno se prijavljuju. (#8604)
* Prilikom brisanja riječi pomoću control+delete, NVDA više ne ostaje tih. (#3298, #11029)
  * Sada je najavljena riječ desno od izbrisane riječi.
* Na ploči općih postavki popis jezika sada je ispravno sortiran. (#10348)
* U dijaloškom okviru Ulazne geste značajno su poboljšane performanse tijekom filtriranja. (#10307)
* Sada možete slati Unicode znakove izvan U+FFFF sa Brailleovog pisma. (#10796)
* NVDA će objaviti sadržaj dijaloškog okvira Otvori s u ažuriranju sustava Windows 10 za svibanj 2020. (#11335)
* Nova eksperimentalna mogućnost u Naprednim postavkama (Omogući selektivnu registraciju za događaje automatizacije korisničkog sučelja i promjene svojstava) može pružiti značajna poboljšanja performansi u Microsoft Visual Studiju i drugim aplikacijama temeljenim na UIAutomation ako je omogućeno. (#11077, #11209)
* Za stavke popisa koje se mogu provjeriti, odabrano stanje više se ne najavljuje suvišno, a ako je primjenjivo, umjesto toga najavljuje se neodabrano stanje. (#8554)
* Na ažuriranju sustava Windows 10 za svibanj 2020., NVDA sada prikazuje Microsoft Sound Mapper prilikom pregledavanja izlaznih uređaja iz dijaloškog okvira sintisajzera. (#11349)
* U pregledniku Internet Explorer brojevi se sada ispravno najavljuju za poredane popise ako popis ne počinje s 1. (#8438)
* U pregledniku Google chrome, NVDA će sada izvijestiti da nisu označene sve kontrole koje se mogu označiti (ne samo potvrdne okvire) koje trenutno nisu označene. (#11377)
* Ponovno je moguće kretati se u različitim kontrolama kada je NVDA jezik postavljen na aragonski. (#11384)
* NVDA se više ne bi trebao ponekad zamrznuti u Microsoft Wordu prilikom brzog strelice gore-dolje ili upisivanja znakova s omogućenom Brailleovom pismom. (#11431, #11425, #11414)
* NVDA više ne dodaje nepostojeći završni prostor prilikom kopiranja trenutnog objekta navigatora u međuspremnik. (#11438)
* NVDA više ne aktivira profil Reci sve ako nema što čitati. (#10899, #9947)
* NVDA više ne može čitati popis značajki u upravitelju internetskih informacijskih usluga (IIS). (#11468)
* NVDA sada drži audio uređaj otvorenim poboljšavajući performanse na nekim zvučnim karticama (#5172, #10721)
* NVDA se više neće zamrznuti ili izaći kada držite pritisnutu tipku control+shift+strelica prema dolje u Microsoft Wordu. (#9463)
* Prošireno/sažeto stanje direktorija u navigacijskom prikazu stabla na drive.google.com sada uvijek izvještava NVDA. (#11520)
* NVDA će automatski detektirati NLS eReader Humanware Braille zaslon putem Bluetootha jer je njegovo Bluetooth ime sada "NLS eReader Humanware". (#11561)
* Velika poboljšanja performansi u Visual Studio Codeu. (#11533)

### Promjene za programere

* GUI Helper's BoxSizerHelper.addDialogDismissButtons podržava novi argument "odvojene" ključne riječi, za dodavanje standardnog horizontalnog razdjelnika dijalozima (osim poruka i dijaloškog okvira s jednim unosom). (#6468)
* Modulima aplikacije dodana su dodatna svojstva, uključujući put za izvršnu datoteku (appPath), aplikaciju iz Windows trgovine (isWindowsStoreApp) i arhitekturu računala za aplikaciju (appArchitecture). (#7894)
* Sada je moguće izraditi module aplikacija za aplikacije koje se nalaze unutar wwahost.exe u sustavu Windows 8 i novijima. (#4569)
* Fragment dnevnika sada se može razdvojiti i zatim kopirati u međuspremnik koristeći NVDA+control+shift+F1. (#9280)
* Objekti specifični za NVDA koje pronađe Pythonov ciklički sakupljač smeća sada se bilježe kada ih sakupljač briše kako bi pomogao u uklanjanju referentnih ciklusa iz NVDA. (#11499)
 * Većina NVDA klasa se prati, uključujući NVDAObjects, appModules, GlobalPlugins, SynthDrivers i TreeInterceptors.
 * Klasa koju je potrebno pratiti trebala bi naslijediti od garbageHandler.TrackedObject.
* Značajno bilježenje otklanjanja pogrešaka za MSAA događaje sada se može omogućiti u NVDA Naprednim postavkama. (#11521)
* MSAA winEvents za trenutno fokusirani objekt više se ne filtriraju zajedno s drugim događajima ako se prekorači broj događaja za određenu nit. (#11520)

## 2020.2

Istaknute značajke ovog izdanja uključuju podršku za novi zaslon na brajici tvrtke Nattiq, bolju podršku za ESET-ov antivirusni grafički prikaz i Windows terminal, poboljšanja performansi u aplikaciji 1Password i za Windows OneCore sintesajzer. Plus mnogi drugi važni ispravci grešaka i poboljšanja.

### Nove značajke

* Podrška za nove Brailleove zaslone:
  * Nattiq nBraille (#10778)
* Dodana skripta za otvaranje NVDA konfiguracijskog direktorija (bez zadane geste). (#2214)
* Bolja podrška za ESET-ov antivirusni GUI. (#10894)
* Dodana podrška za Windows terminal. (#10305)
* Dodana je naredba za prijavu aktivnog konfiguracijskog profila (bez zadane geste). (#9325)
* Dodana je naredba za prebacivanje izvješćivanja o indeksima i eksponentima (nema zadane geste). (#10985)
* Web aplikacije (npr. Gmail) više ne govore zastarjele informacije pri brzom premještanju fokusa. (#10885)
  * Ovaj eksperimentalni popravak mora se ručno omogućiti putem opcije "Pokušaj otkazivanja govora za istekle fokusne događaje" na ploči naprednih postavki.
* Mnogo je više simbola dodano u zadani rječnik simbola. (#11105)

### Promjenama

* Ažuriran prevoditelj brajice liblouis s 3.12 na [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Izvješćivanje o eksponentima i indeksima sada se kontrolira odvojeno od izvješćivanja o atributima fonta. (#10919)
* Zbog promjena napravljenih u VS Codeu, NVDA više ne onemogućuje način pregledavanja u Codeu prema zadanim postavkama. (#10888)
* NVDA više ne izvještava o porukama "gore" i "dolje" kada pomaknete kursor za pregled izravno na prvi ili zadnji redak trenutnog objekta navigatora sa skriptama kursora za pomicanje na vrh i pomicanje na dno. (#9551)
* NVDA više ne izvještava o "lijevim" i "desnom" porukama kada izravno pomaknete kursor na prvi ili zadnji znak retka za trenutni objekt navigatora s premještanjem na početak retka i premještanjem na kraj reda. (#9551)

### Ispravci grešaka

* NVDA se sada ispravno pokreće kada se datoteka dnevnika ne može stvoriti. (#6330)
* U nedavnim izdanjima programa Microsoft Word 365, NVDA više neće najavljivati "brisanje riječi" kada se pritisne Control+Backspace tijekom uređivanja dokumenta. (#10851)
* U Winampu, NVDA će još jednom objaviti status prebacivanja nasumičnog i ponavljanja. (#10945)
* NVDA više nije ekstremno spor kada se kreće unutar popisa stavki u 1Passwordu. (#10508)
* Windows OneCore sintetizator govora više ne zaostaje između izgovora. (#10721)
* NVDA se više ne zamrzava kada otvorite kontekstni izbornik za 1Password u području obavijesti sustava. (#11017)
* U sustavu Office 2013 i starijim verzijama:
  * Vrpce se najavljuju kada se fokus prvi put pomakne na njih. (#4207)
  * Stavke kontekstnog izbornika ponovno se ispravno prijavljuju. (#9252)
  * Odjeljci vrpce dosljedno se najavljuju prilikom navigacije pomoću tipke Control + strelice. (#7067)
* U načinu pregledavanja u Mozilla Firefoxu i Google Chromeu, tekst se više ne prikazuje pogrešno u zasebnom retku kada web sadržaj koristi CSS prikaz: inline-flex. (#11075)
* U načinu pregledavanja s onemogućenim opcijama Automatski postavi fokus sustava na elemente koji se mogu fokusirati, sada je moguće aktivirati elemente koji se ne mogu fokusirati.
* U načinu pregledavanja s onemogućenim opcijama Automatski postavi fokus sustava na elemente koji se mogu fokusirati, sada je moguće aktivirati elemente do kojih se dolazi pritiskom na tipku Tab. (#8528)
* U načinu pregledavanja s onemogućenom opcijom Automatski postavi fokus sustava na elemente koji se mogu izoštriti, aktiviranje određenih elemenata više ne klikne na pogrešnoj lokaciji. (#9886)
* NVDA zvukovi pogrešaka više se ne čuju prilikom pristupa DevExpress tekstualnim kontrolama. (#10918)
* Opisi alata ikona u programskoj traci više se ne prijavljuju pri navigaciji tipkovnicom ako je njihov tekst jednak nazivu ikona, kako bi se izbjeglo dvostruko najavljivanje. (#6656)
* U načinu pregledavanja s onemogućenom opcijom "Automatski postavi fokus sustava na elemente koji se mogu fokusirati", prebacivanje u način fokusiranja s NVDA+razmak sada fokusira element ispod kursora. (#11206)
* Ponovno je moguće provjeriti NVDA ažuriranja na određenim sustavima; npr. čiste instalacije sustava Windows. (#11253)
* Fokus se ne pomiče u Java aplikaciji kada se odabir promijeni u nefokusiranom stablu, tablici ili popisu. (#5989)

### Promjene za programere

* execElevated i hasUiAccess premješteni su iz konfiguracijskog modula u modul systemUtils. Upotreba putem konfiguracijskog modula je zastarjela. (#10493)
* Ažuriran configobj na 5.1.0dev commit f9a265c4. (#10939)
* Sada je moguće automatizirano testiranje NVDA s Chromeom i HTML uzorkom. (#10553)
* IAccessibleHandler je pretvoren u paket, OrderedWinEventLimiter je izdvojen u modul i dodani su jedinični testovi (#10934)
* Ažuriran BrlApi na verziju 0.8 (BRLTTY 6.1). (#11065)
* Dohvaćanje statusne trake sada može prilagoditi AppModule. (#2125, #4640)
* NVDA više ne osluškuje IAccessible EVENT_OBJECT_REORDER. (#11076)
* Pokvareni ScriptableObject (kao što je GlobalPlugin koji propušta poziv na init metodu svoje osnovne klase) više ne prekida NVDA-ino rukovanje skriptom. (#5446)

## 2020.1

Istaknute značajke ovog izdanja uključuju podršku za nekoliko novih Brailleovih zaslona iz HumanWarea i APH-a, plus mnoge druge važne ispravke grešaka kao što je mogućnost ponovnog čitanja matematike u programu Microsoft Word pomoću MathPlayera / MathTypea.

### Nove značajke

* Trenutno odabrana stavka u okvirima s popisima ponovno se prikazuje u načinu pregledavanja u Chromeu, slično kao u NVDA 2019.1. (#10713)
* Sada možete kliknuti desnom tipkom miša na dodirnim uređajima dodirom i držanjem jednim prstom. (#3886)
* Podrška za nove Brailleove zaslone: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2 i NLS eReader. (#10830)

### Promjenama

* NVDA će spriječiti zaključavanje sustava ili odlazak u stanje mirovanja kada je u redu. (#10643)
* Podrška za iframeove izvan procesa u Mozilla Firefoxu. (#10707)
* Ažuriran prevoditelj brajice liblouis na verziju 3.12. (#10161)

### Ispravci grešaka

* Ispravljen NVDA koji nije najavljivao Unicode minus simbol (U+2212). (#10633)
* Prilikom instaliranja dodatka iz upravitelja dodataka, nazivi datoteka i mapa u prozoru za pregledavanje više se ne prijavljuju dvaput. (#10620, #2395)
* U Firefoxu, prilikom učitavanja Mastodona s omogućenim naprednim web sučeljem, sve vremenske trake sada se ispravno prikazuju u načinu pregledavanja. (#10776)
* U načinu pregledavanja, NVDA sada izvještava o "nije označeno" za neoznačene potvrdne okvire tamo gdje se prije ponekad nije javljalo. (#10781)
* ARIA kontrole prekidača više ne prijavljuju zbunjujuće informacije kao što su "nije pritisnuto označeno" ili "pritisnuto označeno". (#9187)
* SAPI4 glasovi više ne bi trebali odbijati izgovarati određeni tekst. (#10792)
* NVDA ponovno može čitati i komunicirati s matematičkim jednadžbama u programu Microsoft Word. (#10803)
* NVDA će ponovno objaviti da je tekst neodabran u načinu pregledavanja ako pritisnete tipku sa strelicom dok je tekst odabran. (#10731).
* NVDA više ne izlazi ako postoji pogreška pri inicijalizaciji eSpeaka. (#10607)
* Pogreške uzrokovane Unicodeom u prijevodima za prečace više ne zaustavljaju instalacijski program, što se ublažava vraćanjem na engleski tekst. (#5166, #6326)
* Strelica prema van i dalje od popisa i tablica u sayAll s omogućenim preletnim čitanjem više ne najavljuje kontinuirano izlazak iz popisa ili tablice. (#10706)
* Ispravite praćenje miša za neke MSHTML elemente u pregledniku Internet Explorer. (#10736)

### Promjene za programere

* Dokumentacija za razvojne programere sada se izrađuje pomoću sfinge. (#9840)
* Nekoliko govornih funkcija podijeljeno je na dva dijela. (#10593)
  Verzija speakX ostaje, ali sada ovisi o funkciji getXSpeech koja vraća govorni slijed.
  * speakObjectProperties sada se oslanja na getObjectPropertiesSpeech
  * speakObject sada se oslanja na getObjectSpeech
  * speakTextInfo sada se oslanja na getTextInfoSpeech
  * speakWithoutPauses je pretvoren u klasu i refaktoriran, ali ne bi trebao narušiti kompatibilnost.
  * getSpeechForSpelling je zastario (iako je još uvijek dostupan) umjesto toga koristite getSpellingSpeech.
  Privatne promjene koje ne bi trebale utjecati na programere dodataka:
  * _speakPlaceholderIfEmpty je sada _getPlaceholderSpeechIfTextEmpty
  * _speakTextInfo_addMath je sada _extendSpeechSequence_addMathForTextInfo
* Govorni 'razlog' pretvoren je u Enum, pogledajte klasu controlTypes.OutputReason (#10703)
  * Konstante 'REASON_*' na razini modula su zastarjele.
* Za kompajliranje NVDA ovisnosti sada je potreban Visual Studio 2019 (16.2 ili noviji). (#10169)
* Ažurirani SConi na verziju 3.1.1. (#10169)
* Ponovno dopustite behaviors._FakeTableCell da nema definiranu lokaciju (#10864)

## 2019.3

NVDA 2019.3 je vrlo značajno izdanje koje sadrži mnoge promjene ispod haube, uključujući nadogradnju Pythona 2 na Python 3 i veliko ponovno pisanje NVDA-inog govornog podsustava.
Iako ove promjene narušavaju kompatibilnost sa starijim NVDA dodacima, nadogradnja na Python 3 neophodna je zbog sigurnosti, a promjene govora omogućuju neke uzbudljive inovacije u bliskoj budućnosti.
 Ostale značajke u ovom izdanju uključuju 64-bitnu podršku za Java VM-ove, funkciju Screen Curtain i Focus Isticanje, podršku za više Brailleovih zaslona i novi preglednik Brailleovog pisma te mnoge druge ispravke grešaka.

### Nove značajke

* Točnost naredbe za pomicanje miša na objekt navigatora poboljšana je u tekstualnim poljima u Java aplikacijama. (#10157)
* Dodana podrška za sljedeće Handy Tech Brailleove zaslone (#8955):
 * Osnovna Brailleova pisma Plus 40
 * Osnovna Brailleova pisma Plus 32
 * Povezivanje Brailleovog pisma
* Sve korisnički definirane geste sada se mogu ukloniti putem novog gumba "Vrati na tvorničke postavke" u dijaloškom okviru Ulazne geste. (#10293)
* Izvješćivanje o fontovima u programu Microsoft Word sada uključuje ako je tekst označen kao skriven. (#8713)
* Dodana je naredba za pomicanje kursora za pregled na položaj koji je prethodno postavljen kao oznaka početka za odabir ili kopiranje: NVDA+shift+F9. (#1969)
* U Internet Exploreru, Microsoft Edgeu i najnovijim verzijama Firefoxa i Chromea orijentiri se sada prijavljuju u načinu fokusiranja i navigaciji objektima. (#10101)
* U Internet Exploreru, Google Chromeu i Mozilla Firefoxu sada se možete kretati po članku i grupiranju pomoću skripti za brzu navigaciju. Te skripte prema zadanim postavkama nisu vezane i mogu se dodijeliti u dijaloškom okviru Geste unosa kada se dijaloški okvir otvori iz dokumenta načina pregledavanja. (#9485, #9227)
 * Izvještavaju se i brojke. Smatraju se objektima i stoga se mogu kretati pomoću tipke za brzu navigaciju.
* U Internet Exploreru, Google Chromeu i Mozilla Firefoxu elementi članaka sada se prijavljuju pomoću navigacije objektima, a po želji i u načinu pregledavanja ako su uključeni u postavkama oblikovanja dokumenta. (#10424)
* Dodana zavjesa zaslona, koja, kada je omogućena, čini cijeli zaslon crnim u sustavu Windows 8 i novijima. (#7857)
 * Dodana je skripta za omogućavanje zavjese zaslona (do sljedećeg ponovnog pokretanja jednim pritiskom, ili uvijek dok NVDA radi s dva pritiska), nije dodijeljena zadana gesta.
 * Može se aktivirati i konfigurirati putem kategorije 'vid' u dijaloškom okviru postavki NVDA.
* NVDA je dodana funkcija isticanja zaslona. (#971, #9064)
 * Isticanje fokusa, objekta navigatora i položaja kursora u načinu pregledavanja može se omogućiti i konfigurirati putem kategorije 'vid' u NVDA dijaloškom okviru postavki.
 * Napomena: Ova značajka nije kompatibilna s dodatkom za isticanje fokusa, međutim, dodatak se i dalje može koristiti dok je ugrađeni highlighter onemogućen.
* Dodan alat za preglednik Brailleovog pisma, omogućuje pregled Brailleovog ispisa putem prozora na zaslonu. (#7788)

### Promjenama

* Korisnički priručnik sada opisuje kako koristiti NVDA u Windows konzoli. (#9957)
* Pokretanje nvda.exe sada prema zadanim postavkama zamjenjuje već pokrenutu kopiju NVDA. Parametar naredbenog retka -r|--replace i dalje je prihvaćen, ali zanemaren. (#8320)
* U sustavu Windows 8 i novijim verzijama, NVDA će sada izvještavati o nazivu proizvoda i informacijama o verzijama hostiranih aplikacija, kao što su aplikacije preuzete iz trgovine Microsoft Store, koristeći informacije koje pruža aplikacija. (#4259, #10108)
* Prilikom uključivanja i isključivanja promjena zapisa pomoću tipkovnice u programu Microsoft Word, NVDA će objaviti stanje postavke. (#942)
* Broj verzije NVDA sada je zabilježen kao prva poruka u dnevniku. To se događa čak i ako je zapisivanje onemogućeno iz GUI-ja. (#9803)
* Dijaloški okvir postavki više ne dopušta promjenu konfigurirane razine zapisnika ako je nadjačana iz naredbenog retka. (#10209)
* U programu Microsoft Word, NVDA sada objavljuje stanje prikaza znakova koji se ne mogu ispisati pritiskom na prečac Ctrl+Shift+8 . (#10241)
* Ažuriran Liblouis prevoditelj brajice da izvrši 58d67e63. (#10094)
* Kada je omogućeno izvještavanje CLDR znakova (uključujući emotikone), oni se najavljuju na svim razinama interpunkcije. (#8826)
* Python paketi trećih strana uključeni u NVDA, kao što su tipovi, sada bilježe svoja upozorenja i pogreške u NVDA dnevnik. (#10393)
* Ažurirane napomene emojija Unicode Common Locale Data Repository na verziju 36.0. (#10426)
* Kada fokusirate grupiranje u načinu pregledavanja, sada se čita i opis. (#10095)
* Java Access Bridge sada je uključen u NVDA kako bi omogućio pristup Java aplikacijama, uključujući 64-bitne Java VM-ove. (#7724)
* Ako Java Access Bridge nije omogućen za korisnika, NVDA ga automatski aktivira pri pokretanju NVDA-e. (#7952)
* Ažuriran eSpeak-NG na 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Ispravci grešaka

* Emoji i drugi 32-bitni Unicode znakovi sada zauzimaju manje prostora na Brailleovom pismu kada su prikazani kao heksadecimalne vrijednosti. (#6695)
* U sustavu Windows 10, NVDA će objaviti opise alata iz univerzalnih aplikacija ako je NVDA konfiguriran za izvještavanje o opisima alata u dijaloškom okviru prezentacije objekta. (#8118)
* Na Windows 10 Anniversary Update i novijim verzijama, upisani tekst sada se prijavljuje u Minttyju. (#1348)
* Na Windows 10 Anniversary Update i novijim verzijama izlaz na Windows konzoli koji se pojavljuje blizu kursora više nije napisan. (#513)
* Kontrole u dijaloškom okviru kompresora Audacitys sada se najavljuju prilikom navigacije dijaloškim okvirom. (#10103)
* NVDA više ne tretira razmake kao riječi u pregledu objekata u uređivačima temeljenim na Scintilli kao što je Notepad++. (#8295)
* NVDA će spriječiti sustav da uđe u stanje mirovanja prilikom pomicanja teksta s gestama na Brailleovom pismu. (#9175)
* U sustavu Windows 10 brajica će sada slijediti prilikom uređivanja sadržaja ćelije u programu Microsoft Excel i u drugim kontrolama teksta UIA gdje je zaostajala. (#9749)
* NVDA će još jednom prijaviti prijedloge u adresnoj traci Microsoft Edgea. (#7554)
* NVDA više ne šuti prilikom fokusiranja zaglavlja kontrole HTML kartice u Internet Exploreru. (#8898)
* U pregledniku Microsoft Edge koji se temelji na EdgeHTML-u, NVDA više neće reproducirati zvuk prijedloga za pretraživanje kada prozor postane maksimiziran. (#9110, #10002)
* ARIA 1.1 kombinirani okviri sada su podržani u Mozilla Firefoxu i Google Chromeu. (#9616)
* NVDA više neće izvještavati o sadržaju vizualno skrivenih stupaca za stavke popisa u kontrolama SysListView32. (#8268)
* Dijaloški okvir postavki više ne prikazuje "info" kao trenutnu razinu zapisnika u sigurnom načinu rada. (#10209)
* U izborniku Start za Windows 10 Anniversary Update i novije, NVDA će objaviti detalje rezultata pretraživanja. (#10340)
* U načinu pregledavanja, ako pomicanje kursora ili korištenje brze navigacije uzrokuje promjenu dokumenta, NVDA više ne govori netočan sadržaj u nekim slučajevima. (#8831, #10343)
* Ispravljeni su neki nazivi grafičkih oznaka u programu Microsoft Word. (#10399)
* U ažuriranju sustava Windows 10 za svibanj 2019. i novijima, NVDA će još jednom objaviti prvi odabrani emoji ili stavku međuspremnika kada se otvori ploča emojija i povijest međuspremnika. (#9204)
* U Poeditu je ponovno moguće vidjeti neke prijevode za jezike zdesna nalijevo. (#9931)
* U aplikaciji Postavke u ažuriranju sustava Windows 10 za travanj 2018. i novijima, NVDA više neće objavljivati informacije o traci napretka za mjerače glasnoće koji se nalaze na stranici Sustav/zvuk. (#10412)
* Nevažeći regularni izrazi u govornim rječnicima više ne prekidaju u potpunosti govor u NVDA. (#10334)
* Prilikom čitanja stavki s grafičkim oznakama u programu Microsoft Word s omogućenim UIA-om, grafička oznaka sa sljedeće stavke popisa više se ne najavljuje neprimjereno. (#9613)
* Riješeni su neki rijetki problemi s prijevodom Brailleovog pisma i pogreške s liblouisom. (#9982)
* Java aplikacije pokrenute prije NVDA sada su dostupne bez potrebe za ponovnim pokretanjem Java aplikacije. (#10296)
* U pregledniku Mozilla Firefox, kada fokusirani element postane označen kao trenutni (aria-current), ta se promjena više puta ne izgovara. (#8960)
* NVDA će sada tretirati određene sastavljene Unicode znakove kao što je e-acute kao jedan znak prilikom kretanja kroz tekst. (#10550)
* Sada je podržan Spring Tool Suite verzije 4. (#10001)
* Nemojte dvostruko izgovarati ime kada je arija-označena relacijskim ciljem unutarnji element. (#10552)
* U sustavu Windows 10 verzije 1607 i novijim verzijama upisani znakovi s Brailleovih tipkovnica izgovaraju se u više situacija. (#10569)
* Prilikom promjene audio izlaznog uređaja, tonovi koje reproducira NVDA sada će se reproducirati putem novoodabranog uređaja. (#2167)
* U pregledniku Mozilla Firefox, pomicanje fokusa u načinu pregledavanja je brže. To u mnogim slučajevima čini pomicanje kursora u načinu pregledavanja responzivnijim. (#10584)

### Promjene za programere

* Ažuriran Python na 3.7. (#7105)
* Ažuriran pySerial na verziju 3.4. (#8815)
* Ažuriran wxPython na 4.0.3 kako bi podržao Python 3.5 i novije verzije. (#9630)
* Ažurirano šest na verziju 1.12.0. (#9630)
* Ažuriran py2exe na verziju 0.9.3.2 (u razvoju, commit b372a8e iz albertosottile/py2exe#13). (#9856)
* Ažuriran UIAutomationCore.dll modul comtipova na verziju 10.0.18362. (#9829)
* Dovršavanje tabulatora u Python konzoli samo predlaže atribute koji počinju s podvlakom ako je podvlaka prvo upisana. (#9918)
* Alat za linting Flake8 integriran je sa SConima koji odražavaju zahtjeve koda za zahtjeve za povlačenje. (#5918)
* Budući da NVDA više ne ovisi o pyWin32, moduli kao što su win32api i win32con više nisu dostupni za dodatke. (#9639)
 * Win32API pozivi mogu se zamijeniti izravnim pozivima na Win32 DLL funkcije putem ctypesa.
 * Win32con konstante trebaju biti definirane u vašim datotekama.
* Argument "async" u nvwave.playWaveFile preimenovan je u "asinkroni". (#8607)
* metode speakText i speakCharacter na objektima synthDriver više nisu podržane.
 * Ovom funkcionalnošću upravlja SynthDriver.speak.
* SynthSetting klase u synthDriverHandleru su uklonjene. Sada umjesto toga koristite klase driverHandler.DriverSetting.
* Klase SynthDriver više ne bi trebale izlagati indeks putem svojstva lastIndex.
 * Umjesto toga, trebali bi obavijestiti radnju synthDriverHandler.synthIndexReached s indeksom, nakon što se sav prethodni zvuk završi s reprodukcijom prije tog indeksa.
* Klase SynthDriver sada moraju obavijestiti radnju synthDriverHandler.synthDoneSpeaking nakon što se sav zvuk iz poziva SynthDriver.speak završi reprodukcija.
* Klase SynthDrivera moraju podržavati govor. PitchCommand u svojoj metodi govora, jer promjene u visini tona za pravopis govora sada ovise o ovoj funkcionalnosti.
* Govorna funkcija getSpeechTextForProperties preimenovana je u getPropertiesSpeech. (#10098)
* Brajicova funkcija getBrailleTextForProperties preimenovana je u getPropertiesBraille. (#10469)
* Nekoliko govornih funkcija promijenjeno je kako bi se vratili govorni slijedovi. (#10098)
 * getControlFieldSpeech
 * getFormatFieldSpeech
 * getSpeechTextForProperties sada se naziva getPropertiesSpeech
 * getIndentationSpeech
 * getTableInfoSpeech
* Dodan je modul textUtils za pojednostavljenje razlika u nizovima između nizova Python 3 i Windows unicode nizova. (#9545)
 * Pogledajte dokumentaciju modula i modul textInfos.offsets za primjere implementacija.
* Zastarjela funkcionalnost sada je uklonjena. (#9548)
 * Uklonjeni AppModules:
  * Snimač zvuka u sustavu Windows XP.
  * Klango Player, koji je napušteni softver.
 * configobj.validate omot uklonjen.
  * Novi kod trebao bi koristiti iz configobj import validate umjesto import validate
 * textInfos.Point i textInfos.Rect zamijenjeni su s locationHelper.Point i locationHelper.RectLTRB.
 * Brailleovo pismo. BrailleHandler._get_tether i Brailleovo pismo. BrailleHandler.set_tether su uklonjeni.
 * config.getConfigDirs je uklonjen.
 * konfiguracija. ConfigManager.getConfigValidationParameter zamijenjen je s getConfigValidation
 * inputCore.InputGesture.logIdentifier svojstvo je uklonjeno.
   * Umjesto toga koristite _get_identifiers u inputCore.InputGesture.
 * synthDriverHandler.SynthDriver.speakText/speakCharacter su uklonjeni.
 * Uklonjeno je nekoliko klasa synthDriverHandler.SynthSetting.
   * Prethodno čuvano za kompatibilnost s prethodnim verzijama (#8214), sada se smatra zastarjelim.
   * Upravljačke programe koji su koristili klase SynthSetting treba ažurirati kako bi koristili klase DriverSetting.
 * Neki naslijeđeni kod su uklonjeni, posebno:
  * Podrška za popis poruka programa Outlook prije 2003.
  * Klasa preklapanja za klasični izbornik Start, koja se nalazi samo u sustavu Windows Vista i starijim verzijama.
  * Odbačena je podrška za Skype 7, jer definitivno više ne radi.
* Dodan je okvir za stvaranje pružatelja usluga poboljšanja vida; moduli koji mogu mijenjati sadržaj zaslona, opcionalno na temelju NVDA podataka o lokacijama objekata. (#9064)
 * Dodaci mogu objediniti vlastite davatelje usluga u mapu visionEnhancementProviders.
 * Pogledajte module vision i visionEnhancementProviders za implementaciju okvira i primjere.
 * Pružatelji usluga poboljšanja vida omogućeni su i konfigurirani putem kategorije 'vid' u NVDA dijaloškom okviru postavki.
* Svojstva apstraktne klase sada su podržana na objektima koji nasljeđuju iz baseObject.AutoPropertyObject (npr. NVDAObjects i TextInfos). (#10102)
* Uveden displayModel.UNIT_DISPLAYCHUNK kao konstanta jedinice textInfos specifična za DisplayModelTextInfo. (#10165)
 * Ova nova konstanta omogućuje prelazak preko teksta u DisplayModelTextInfo na način koji više nalikuje načinu na koji se dijelovi teksta spremaju u temeljni model.
* displayModel.getCaretRect sada vraća instancu locationHelper.RectLTRB. (#10233)
* Konstante UNIT_CONTROLFIELD i UNIT_FORMATFIELD premještene su iz virtualBuffers.VirtualBufferTextInfo u paket textInfos. (#10396)
* Za svaki unos u NVDA dnevnik sada su uključeni podaci o izvornoj niti. (#10259)
* UIA TextInfo objekti sada se mogu premještati/proširivati pomoću tekstualnih jedinica stranice, priče i formatField. (#10396)
* Manje je vjerojatno da će vanjski moduli (appModules i globalPlugins) sada moći prekinuti stvaranje NVDAObjects.
 * Iznimke uzrokovane metodama "chooseNVDAObjectOverlayClasses" i "event_NVDAObject_init" sada su ispravno uhvaćene i zabilježene.
* Rječnik aria.htmlNodeNameToAriaLandmarkRoles preimenovan je u aria.htmlNodeNameToAriaRoles. Sada sadrži i uloge koje nisu orijentir.
* scriptHandler.isCurrentScript je uklonjen zbog nekorištenja. Nema zamjene. (#8677)

## 2019.2.1

Ovo je manje izdanje za ispravljanje nekoliko rušenja prisutnih u 2019.2. Popravci uključuju:

* Riješeno je nekoliko rušenja na Gmailu koja su se pojavila u Firefoxu i Chromeu prilikom interakcije s određenim skočnim izbornicima, kao što je stvaranje filtara ili promjena određenih postavki Gmaila. (#10175, #9402, #8924)
* U sustavu Windows 7 NVDA više ne uzrokuje rušenje Windows Explorera kada se miš koristi u izborniku Start. (#9435)
* Windows Explorer u sustavu Windows 7 više se ne ruši prilikom pristupa poljima za uređivanje metapodataka. (#5337)
* NVDA se više ne zamrzava prilikom interakcije sa slikama s base64 URI-jem u Mozilla Firefoxu ili Google Chromeu. (#10227)

## 2019.2

Istaknuti dijelovi ovog izdanja uključuju automatsko otkrivanje brajevih redaka Freedom Scientific, eksperimentalnu postavku na ploči Napredno za zaustavljanje automatskog pomicanja fokusa u načinu pregledavanja (što može pružiti poboljšanja performansi), opciju povećanja brzine za Windows OneCore sintisajzer za postizanje vrlo brzih brzina i mnoge druge ispravke grešaka.

### Nove značajke

* NVDA Miranda NG podrška radi s novijim verzijama klijenta. (#9053)
* Sada možete onemogućiti način pregledavanja prema zadanim postavkama tako da onemogućite novu opciju "Omogući način pregledavanja pri učitavanju stranice" u postavkama NVDA načina pregledavanja. (#8716)
 * Imajte na umu da kada je ova opcija onemogućena, i dalje možete ručno uključiti način pregledavanja pritiskom na NVDA+razmak.
* Sada možete filtrirati simbole u dijaloškom okviru za interpunkciju/izgovor simbola, slično kao što filtriranje funkcionira u dijaloškom okviru popisa elemenata i gesta unosa. (#5761)
* Dodana je naredba za promjenu razlučivosti jedinice teksta miša (koliko će se teksta izgovoriti kada se miš pomiče), nije joj dodijeljena zadana gesta. (#9056)
* Windows OneCore sintisajzer sada ima opciju povećanja brzine, što omogućuje znatno brži govor. (#7498)
* Opcija Rate Boost sada se može konfigurirati iz Synth Settings Ring za podržane sintisajzere govora. (Trenutno eSpeak-NG i Windows OneCore). (#8934)
* Konfiguracijski profili sada se mogu ručno aktivirati gestama. (#4209)
 * Gesta mora biti konfigurirana u dijaloškom okviru "Ulazne geste".
* U Eclipseu je dodana podrška za automatsko dovršavanje u uređivaču koda. (#5667)
 * Osim toga, Javadoc informacije mogu se čitati iz uređivača kada su prisutne pomoću NVDA+d.
* Dodana je eksperimentalna opcija na ploču Napredne postavke koja vam omogućuje da zaustavite fokus sustava da slijedi kursor načina pregledavanja (Automatski postavite fokus sustava na elemente koji se mogu fokusirati). (#2039) Iako ovo možda nije prikladno za isključivanje za sve web stranice, ovo može riješiti:
 * Efekt gumene trake: NVDA sporadično poništava zadnji pritisak na tipku u načinu pregledavanja skokom na prethodnu lokaciju.
 * Okviri za uređivanje kradu fokus sustava kada se strelice provlače kroz njih na nekim web stranicama.
 * Pritisci tipki u načinu pregledavanja sporo reagiraju.
* Za upravljačke programe Brailleovog pisma koji ga podržavaju, postavke upravljačkog programa sada se mogu promijeniti iz kategorije postavki brajice u NVDA dijaloškom okviru postavki. (#7452)
* Freedom Scientific Brailleovi zasloni sada su podržani automatskim otkrivanjem brajice. (#7727)
* Dodana je naredba za prikaz zamjene za simbol ispod kursora za pregled. (#9286)
* Dodana je eksperimentalna opcija na ploču Napredne postavke koja vam omogućuje da isprobate novo prepisivanje NVDA-ine podrške za Windows konzolu pomoću Microsoftovog API-ja za automatizaciju korisničkog sučelja. (#9614)
* U Python konzoli, polje za unos sada podržava lijepljenje više redaka iz međuspremnika. (#9776)

### Promjenama

* Glasnoća sintisajzera sada je povećana i smanjena za 5 umjesto 10 kada koristite prsten postavki. (#6754)
* Pojašnjen je tekst u upravitelju dodataka kada se NVDA pokrene sa zastavicom --disable-addons. (#9473)
* Ažurirane napomene emojija Unicode Common Locale Data Repository na verziju 35.0. (#9445)
* Prečac za polje filtra na popisu elemenata u načinu pregledavanja promijenjen je u alt+y. (#8728)
* Kada je automatski detektirani Brailleov zaslon spojen putem Bluetootha, NVDA će nastaviti tražiti USB zaslone koje podržava isti upravljački program i prebaciti se na USB vezu ako postane dostupna. (#8853)
* Ažuriran eSpeak-NG da commit 67324cc.
* Ažuriran prevoditelj brajice liblouis na verziju 3.10.0. (#9439, #9678)
* NVDA će sada prijaviti riječ 'odabrano' nakon što prijavi tekst koji je korisnik upravo odabrao. (#9028, #9909)
* U programu Microsoft Visual Studio Code, NVDA je prema zadanim postavkama u fokusnom načinu rada. (#9828)

### Ispravci grešaka

* NVDA se više ne ruši kada je direktorij dodataka prazan. (#7686)
* Oznake LTR i RTL više se ne prijavljuju na Brailleovom pismu ili govoru po znaku prilikom pristupa prozoru svojstava. (#8361)
* Kada prelazite na polja obrasca s brzom navigacijom u načinu pregledavanja, sada se najavljuje cijelo polje obrasca, a ne samo prvi redak. (#9388)
* NVDA više neće utihnuti nakon izlaska iz aplikacije Windows 10 Mail. (#9341)
* NVDA se više ne pokreće kada su korisničke regionalne postavke postavljene na regionalnu shemu nepoznatu NVDA-u, kao što je engleski (Nizozemska). (#8726)
* Kada je način pregledavanja omogućen u programu Microsoft Excel i prebacite se na preglednik u načinu rada fokusa ili obrnuto, stanje načina pregledavanja sada se prijavljuje na odgovarajući način. (#8846)
* NVDA sada ispravno izvještava o liniji na kursoru miša u Notepad++ i drugim uređivačima koji se temelje na Scintilli. (#5450)
* U Google dokumentima (i drugim uređivačima na webu) Brailleovo pismo više ponekad ne prikazuje pogrešno "lst end" ispred pokazivača u sredini stavke popisa. (#9477)
* U ažuriranju sustava Windows 10 za svibanj 2019., NVDA više ne izgovara mnogo obavijesti o glasnoći ako mijenjate glasnoću hardverskim gumbima kada je File Explorer u fokusu. (#9466)
* Učitavanje dijaloškog okvira za interpunkciju/izgovor simbola sada je mnogo brže kada se koriste rječnici simbola koji sadrže više od 1000 unosa. (#8790)
* U Scintilla kontrolama kao što je Notepad++, NVDA može pročitati ispravan redak kada je omogućeno prelamanje riječi. (#9424)
* U programu Microsoft Excel lokacija ćelije se objavljuje nakon što se promijeni zbog gesta shift+enter ili shift+numpadEnter. (#9499)
* U programu Visual Studio 2017 i novijim verzijama, u prozoru Istraživač objekata, odabrana stavka u stablu objekata ili stablu članova s kategorijama sada se ispravno prijavljuje. (#9311)
* Dodaci s nazivima koji se razlikuju samo u velikim slovima više se ne tretiraju kao zasebni dodaci. (#9334)
* Za Windows OneCore glasove na brzinu postavljenu u NVDA više ne utječe brzina postavljena u postavkama govora sustava Windows 10. (#7498)
* Dnevnik se sada može otvoriti pomoću NVDA+F1 kada nema podataka za razvojne programere za trenutni objekt navigatora. (#8613)
* Ponovno je moguće koristiti NVDA naredbe za navigaciju tablicom u Google dokumentima, Firefoxu i Chromeu. (#9494)
* Tipke na braniku sada ispravno rade na Brailleovim pismima Freedom Scientific. (#8849)
* Prilikom čitanja prvog znaka dokumenta u Notepad++ 7.7 X64, NVDA se više ne zamrzava do deset sekundi. (#9609)
* HTCom se sada može koristiti s Handy Tech Brailleovim pismom u kombinaciji s NVDA. (#9691)
* U pregledniku Mozilla Firefox, ažuriranja aktivne regije više se ne prijavljuju ako je aktivna regija na kartici pozadine. (#1318)
* NVDA-ov dijaloški okvir Pronađi način pregledavanja više ne funkcionira ako je NVDA-in dijaloški okvir O nama trenutno otvoren u pozadini. (#8566)

### Promjene za programere

* Sada možete postaviti svojstvo "disableBrowseModeByDefault" na modulima aplikacije tako da način pregledavanja ostane isključen prema zadanim postavkama. (#8846)
* Prošireni stil prozora prozora sada je izložen pomoću svojstva 'extendedWindowStyle' na objektima prozora i njihovim izvedenicama. (#9136)
* Ažuriran paket komtipova na 1.1.7. (#9440, #8522)
* Kada koristite naredbu info modula izvješća, redoslijed informacija promijenio se kako bi se modul prvi prikazao. (#7338)
* Dodan je primjer za demonstraciju korištenja nvdaControllerClient.dll iz C#. (#9600)
* Dodana je nova funkcija isWin10 u winVersion modul koja vraća radi li ova kopija NVDA ili ne na (barem) isporučenoj verziji izdanja Windowsa 10 (kao što je 1903). (#9761)
* NVDA Python konzola sada sadrži više korisnih modula u svom imenskom prostoru (kao što su appModules, globalPlugins, config i textInfos). (#9789)
* Rezultat posljednje izvršene naredbe u NVDA Python konzoli sada je dostupan iz varijable _ (linija). (#9782)
 * Imajte na umu da ovo zasjenjuje funkciju prevođenja gettexta koja se također naziva "_". Za pristup funkciji prevođenja: del _

## 2019.1.1

Ovo izdanje točke ispravlja sljedeće greške:

* NVDA više ne uzrokuje rušenje programa Excel 2007 ili odbija izvješćivanje ako ćelija ima formulu. (#9431)
* Google Chrome više se ne ruši prilikom interakcije s određenim okvirima s popisima. (#9364)
* Riješen je problem koji je sprječavao kopiranje korisničke konfiguracije u konfiguracijski profil sustava. (#9448)
* U Microsoft Excelu, NVDA ponovno koristi lokaliziranu poruku kada izvještava o lokaciji spojenih ćelija. (#9471)

## 2019.1

Istaknute značajke ovog izdanja uključuju poboljšanja performansi pri pristupu Microsoft Wordu i Excelu, poboljšanja stabilnosti i sigurnosti kao što su podrška za dodatke s informacijama o kompatibilnosti verzija i mnoge druge ispravke programskih pogrešaka.

Imajte na umu da se od ovog izdanja NVDA-a, prilagođeni appModules, globalPlugins, upravljački programi za Brailleovo pismo i upravljački programi za sintisajzere više neće automatski učitavati iz vašeg NVDA korisničkog konfiguracijskog direktorija.
Umjesto toga, oni bi trebali biti instalirani kao dio NVDA dodatka. Za one koji razvijaju kod za dodatak, kod za testiranje može se smjestiti u novi direktorij za graditelje u direktoriju za konfiguraciju korisnika NVDA, ako je opcija Razvojni blok uključena u novoj NVDA ploči s naprednim postavkama.
Ove promjene su potrebne kako bi se osigurala bolja kompatibilnost prilagođenog koda, tako da se NVDA ne pokvari kada ovaj kod postane nekompatibilan s novijim izdanjima.
Molimo pogledajte popis promjena niže za više detalja o tome i kako su dodaci sada bolje verzionirani.

### Nove značajke

* Nove tablice na Brailleovom pismu: afrikaans, arapski računalni braille s 8 točaka, arapski razred 2, španjolski razred 2. (#4435, #9186)
* Dodana je opcija u NVDA postavkama miša kako bi NVDA upravljao situacijama u kojima mišem upravlja druga aplikacija. (#8452)
 * To će omogućiti NVDA da prati miš kada se sustavom upravlja daljinski pomoću TeamViewera ili drugog softvera za daljinsko upravljanje.
* Dodan je parametar naredbenog retka '--enable-start-on-logon' kako bi se omogućilo konfiguriranje da li tihe instalacije NVDA postavljaju NVDA da se pokreće pri prijavi u Windows ili ne. Navedite true za početak pri prijavi ili false da se ne pokreće pri prijavi. Ako argument --enable-start-on-logon uopće nije naveden, NVDA će se prema zadanim postavkama pokrenuti prilikom prijave, osim ako je već bio konfiguriran da to ne radi prethodna instalacija. (#8574)
* Moguće je isključiti NVDA značajke zapisivanja dnevnika postavljanjem razine zapisivanja na "onemogućeno" na ploči Opće postavke. (#8516)
* Sada se izvještava o prisutnosti formula u proračunskim tablicama LibreOffice i Apache OpenOffice. (#860)
* U Mozilla Firefoxu i Google Chromeu, način pregledavanja sada izvještava o odabranoj stavci u okvirima popisa i stablima.
 * Ovo radi u Firefoxu 66 i novijim verzijama.
 * To ne funkcionira za određene okvire popisa (kontrole za odabir HTML-a) u Chromeu.
* Rana podrška za aplikacije kao što je Mozilla Firefox na računalima s ARM64 (npr. Qualcomm Snapdragon) procesorima. (#9216)
* Nova kategorija Napredne postavke dodana je u NVDA dijaloški okvir Postavke, uključujući opciju isprobavanja NVDA-ine nove podrške za Microsoft Word putem Microsoftovog API-ja za automatizaciju korisničkog sučelja. (#9200)
* Dodana je podrška za grafički prikaz u Windows Disk Managementu. (#1486)
* Dodana je podrška za Handy Tech Connect Brailleovo pismo i Basic Braille 84. (#9249)

### Promjenama

* Ažuriran prevoditelj brajice liblouis na verziju 3.8.0. (#9013)
* Autori dodataka sada mogu nametnuti minimalnu potrebnu NVDA verziju za svoje dodatke. NVDA će odbiti instalirati ili učitati dodatak čija je minimalna potrebna NVDA verzija viša od trenutne NVDA verzije. (#6275)
* Autori dodataka sada mogu odrediti posljednju verziju NVDA na kojoj je dodatak testiran. Ako je dodatak testiran samo na verziji NVDA koja je niža od trenutne, NVDA će odbiti instalirati ili učitati dodatak. (#6275)
* Ova verzija NVDA omogućit će instaliranje i učitavanje dodataka koji još ne sadrže informacije o minimalnoj i posljednjoj testiranoj verziji NVDA-a, ali nadogradnja na buduće verzije NVDA (npr. 2019.2) može automatski uzrokovati onemogućavanje ovih starijih dodataka.
* Naredba za pomicanje miša na objekt navigatora sada je dostupna u programu Microsoft Word, kao i za UIA kontrole, posebno Microsoft Edge. (#7916, #8371)
* Izvješćivanje o tekstu ispod miša poboljšano je u pregledniku Microsoft Edge i drugim aplikacijama UIA. (#8370)
* Kada se NVDA pokrene s parametrom naredbenog retka '--portable-path', ponuđena putanja se automatski popunjava prilikom pokušaja stvaranja prijenosne kopije NVDA pomoću NVDA izbornika. (#8623)
* Ažuriran je put do tablice norveškog Brailleovog pisma kako bi odražavao standard iz 2015. godine. (#9170)
* Prilikom navigacije po odlomku (control+strelice gore ili dolje) ili navigaciji po ćeliji tablice (control+alt+strelice), postojanje pravopisnih pogrešaka više se neće objavljivati, čak i ako je NVDA konfiguriran da ih automatski najavljuje. To je zato što odlomci i ćelije tablice mogu biti prilično veliki, a otkrivanje pravopisnih pogrešaka u nekim aplikacijama može biti vrlo skupo. (#9217)
* NVDA više ne učitava automatski prilagođene appModules, globalPlugins i upravljačke programe za brajicu i sintisajzer iz NVDA direktorija za konfiguraciju korisnika. Ovaj kod bi umjesto toga trebao biti zapakiran kao dodatak s točnim informacijama o verziji, osiguravajući da se nekompatibilni kod ne pokreće s trenutnim verzijama NVDA. (#9238)
 * Za programere koji trebaju testirati kod dok se razvija, omogućite NVDA direktorij za brisanje u kategoriji Napredno NVDA postavki i stavite svoj kod u direktorij 'scratchpad' koji se nalazi u direktoriju za konfiguraciju korisnika NVDA kada je ova opcija omogućena.

### Ispravci grešaka

* Kada koristite OneCore sintisajzer govora na ažuriranju sustava Windows 10 za travanj 2018. i novijim verzijama, veliki dijelovi tišine više se ne umeću između govornih izgovora. (#8985)
* Kada se pomičete po znaku u kontrolama običnog teksta (kao što je Notepad) ili načinu pregledavanja, 32-bitni znakovi emojija koji se sastoje od dvije UTF-16 kodne točke (kao što je 🤦 ) sada će se ispravno čitati. (#8782)
* Poboljšan dijaloški okvir za potvrdu ponovnog pokretanja nakon promjene jezika NVDA sučelja. Oznake teksta i gumba sada su sažetije i manje zbunjujuće. (#6416)
* Ako se sintisajzer govora treće strane ne uspije učitati, NVDA će se vratiti na Windows OneCore sintisajzer govora u sustavu Windows 10, umjesto da govori. (#9025)
* Uklonjen je unos "Dijalog dobrodošlice" u NVDA izborniku dok ste bili na sigurnim zaslonima. (#8520)
* Kada koristite karticu ili koristite brzu navigaciju u načinu pregledavanja, legende na pločama kartica sada se dosljednije izvješćuju. (#709)
* NVDA će sada najaviti promjene odabira za određene birače vremena, kao što su aplikacije Alarmi i sat u sustavu Windows 10. (#5231)
* U akcijskom centru sustava Windows 10, NVDA će najavljivati poruke o statusu prilikom prebacivanja brzih radnji kao što su svjetlina i pomoć pri fokusiranju. (#8954)
* U akcijskom centru u Windows 10 ažuriranju za listopad 2018. i ranijim verzijama, NVDA će prepoznati kontrolu brze akcije svjetline kao gumb umjesto preklopnog gumba. (#8845)
* NVDA će ponovno pratiti kursor i objaviti izbrisane znakove u Microsoft Excelu, otići i pronaći polja za uređivanje. (#9042)
* Ispravljen je rijedak pad načina pregledavanja u Firefoxu. (#9152)
* NVDA više ne prijavljuje fokus za neke kontrole na vrpci sustava Microsoft Office 2016 kada je sažet.
* NVDA više ne prijavljuje predloženi kontakt prilikom unosa adresa u nove poruke u programu Outlook 2016. (#8502)
* Posljednjih nekoliko tipki za usmjeravanje kursora na zaslonima eurobrailleovog pisma od 80 ćelija više ne usmjeravaju pokazivač na položaj na ili neposredno nakon početka brajice. (#9160)
* Popravljena navigacija tablicom u prikazu s navojem u Mozilla Thunderbirdu. (#8396)
* U Mozilla Firefoxu i Google Chromeu, prebacivanje u način fokusiranja sada ispravno funkcionira za određene okvire s popisom i stabla (gdje okvir s popisom/stablo nije sam po sebi fokusiran, ali njegove stavke jesu). (#3573, #9157)
* Način pregledavanja sada je ispravno uključen prema zadanim postavkama kada čitate poruke u programu Outlook 2016/365 ako koristite NVDA eksperimentalnu podršku za automatizaciju korisničkog sučelja za Word dokumente. (#9188)
* Manje je vjerojatno da će se NVDA zamrznuti na takav način da je jedini način za bijeg odjava iz trenutne Windows sesije. (#6291)
* U ažuriranju sustava Windows 10 za listopad 2018. i novijima, prilikom otvaranja povijesti međuspremnika u oblaku s praznim međuspremnikom, NVDA će objaviti status međuspremnika. (#9103)
* U ažuriranju sustava Windows 10 za listopad 2018. i novijim verzijama, prilikom traženja emojija na ploči s emojijima, NVDA će objaviti najbolji rezultat pretraživanja. (#9105)
* NVDA se više ne zamrzava u glavnom prozoru Oracle VirtualBoxa 5.2 i novijih verzija. (#9202)
* Responzivnost u programu Microsoft Word prilikom navigacije po liniji, odlomku ili ćeliji tablice može se značajno poboljšati u nekim dokumentima. Podsjetnik da za najbolje performanse postavite Microsoft Word na prikaz skice s alt+w,e nakon otvaranja dokumenta. (#9217)
* U Mozilla Firefoxu i Google Chromeu prazna upozorenja više se ne prijavljuju. (#5657)
* Značajna poboljšanja performansi prilikom navigacije ćelijama u programu Microsoft Excel, osobito kada proračunska tablica sadrži padajuće popise za komentare i/ili provjeru valjanosti. (#7348)
* Više ne bi trebalo biti potrebno isključiti uređivanje unutar ćelije u opcijama programa Microsoft Excel za pristup kontroli za uređivanje ćelija pomoću NVDA u programu Excel 2016/365. (#8146).
* Popravljeno je zamrzavanje u Firefoxu koje se ponekad viđa prilikom brze navigacije po orijentirima, ako se koristi dodatak Enhanced Aria. (#8980)

### Promjene za programere

* NVDA se sada može izraditi sa svim izdanjima Microsoft Visual Studio 2017 (ne samo sa Community izdanjem). (#8939)
* Sada možete uključiti izlaz dnevnika iz liblouisa u NVDA dnevnik postavljanjem louis boolean zastavice u odjeljku debugLogging NVDA konfiguracije. (#4554)
* Autori dodataka sada mogu pružiti informacije o kompatibilnosti NVDA verzija u manifestima dodataka. (#6275, #9055)
 * minimumNVDAVersion: Minimalna potrebna verzija NVDA za ispravan rad dodatka.
 * lastTestedNVDAVersion: Posljednja verzija NVDA s kojom je testiran dodatak.
* Objekti OffsetsTextInfo sada mogu implementirati metodu _getBoundingRectFromOffset kako bi omogućili dohvaćanje graničnih pravokutnika po znakovima umjesto točaka. (#8572)
* Dodano je svojstvo boundingRect objektima TextInfo za dohvaćanje rubnog pravokutnika raspona teksta. (#8371)
* Svojstva i metode unutar klasa sada se mogu označiti kao apstraktne u NVDA. Ove će klase pokrenuti pogrešku ako se instanciraju. (#8294, #8652, #8658)
* NVDA može zabilježiti vrijeme od unosa kada se izgovara tekst, što pomaže u mjerenju percipirane responzivnosti. To se može omogućiti postavljanjem postavke timeSinceInput na True u odjeljku debugLog NVDA konfiguracije. (#9167)

## 2018.4.1

Ovo izdanje ispravlja pad pri pokretanju ako je jezik korisničkog sučelja NVDA postavljen na aragonski. (#9089)

## 2018.4

Istaknuti dijelovi ovog izdanja uključuju poboljšanja performansi u nedavnim verzijama Mozilla Firefoxa, najavu emojija sa svim sintisajzerima, izvještavanje o statusu odgovora/proslijeđenja u programu Outlook, izvještavanje o udaljenosti pokazivača do ruba stranice Microsoft Worda i mnoge ispravke grešaka.

### Nove značajke

* Nove tablice na Brailleovom pismu: kineski (Kina, mandarinski) razred 1 i stupanj 2. (#5553)
* Status Odgovoreno / Proslijeđeno sada se izvještava o stavkama pošte na popisu poruka programa Microsoft Outlook. (#6911)
* NVDA sada može čitati opise emojija, kao i druge znakove koji su dio Unicode Common Locale Data Repository. (#6523)
* U Microsoft Wordu, udaljenost pokazivača od gornjeg i lijevog ruba stranice može se prijaviti pritiskom na NVDA+numpadDelete. (#1939)
* U Google tablicama s omogućenim načinom brajice, NVDA više ne objavljuje "odabrano" na svakoj ćeliji prilikom premještanja fokusa između ćelija. (#8879)
* Dodana podrška za Foxit Reader i Foxit Phantom PDF. (#8944)
* Dodana je podrška za alat baze podataka DBeaver. (#8905)

### Promjenama

* "Izvješćivanje balona pomoći" u dijaloškom okviru Prezentacije objekata preimenovano je u "Obavijesti o prijavi" kako bi se uključilo izvješćivanje o obavijestima o zdravicama u sustavu Windows 8 i novijim verzijama. (#5789)
* U postavkama NVDA tipkovnice, potvrdni okviri za omogućavanje ili onemogućavanje NVDA modifikatorskih tipki sada se prikazuju na popisu, a ne kao zasebni potvrdni okviri.
* NVDA više neće prikazivati suvišne informacije prilikom čitanja satne programske trake na nekim verzijama sustava Windows. (#4364)
* Ažuriran je prevoditelj brajice liblouis na verziju 3.7.0. (#8697)
* Ažuriran eSpeak-NG da izvrši 919f3240cbb.

### Ispravci grešaka

* U programu Outlook 2016/365 za poruke se prijavljuju kategorija i status zastavice. (#8603)
* Kada je NVDA postavljen na jezike kao što su kirgiski, mongolski ili makedonski, više ne prikazuje dijaloški okvir pri pokretanju s upozorenjem da operacijski sustav ne podržava taj jezik. (#8064)
* Pomicanjem miša na objekt navigatora sada će se mnogo točnije pomaknuti miš na položaj načina pregledavanja u Mozilla Firefoxu, Google Chromeu i Acrobat Readeru DC. (#6460)
* Interakcija s kombiniranim okvirima na webu u Firefoxu, Chromeu i Internet Exploreru je poboljšana. (#8664)
* Ako se izvodi na japanskoj verziji sustava Windows XP ili Vista, NVDA sada prikazuje poruku o zahtjevima za verziju OS-a prema očekivanjima. (#8771)
* Poboljšanja performansi pri navigaciji velikim stranicama s puno dinamičkih promjena u Mozilla Firefoxu. (#8678)
* Brailleovo pismo više ne prikazuje atribute fonta ako su onemogućeni u postavkama formatiranja dokumenta. (#7615)
* NVDA više ne uspijeva pratiti fokus u File Exploreru i drugim aplikacijama koje koriste automatizaciju korisničkog sučelja kada je druga aplikacija zauzeta (kao što je skupna obrada zvuka). (#7345)
* U ARIA izbornicima na webu, tipka Escape sada će se prosljeđivati u izbornik i više neće bezuvjetno isključivati način fokusiranja. (#3215)
* U novom Gmail web sučelju, kada koristite brzu navigaciju unutar poruka dok ih čitate, cijeli se korpus poruke više ne prijavljuje nakon elementa na koji ste upravo navigirali. (#8887)
* Nakon ažuriranja NVDA-a, preglednici kao što su Firefox i Google Chrome više se ne bi trebali rušiti, a način pregledavanja trebao bi nastaviti ispravno odražavati ažuriranja svih trenutno učitanih dokumenata. (#7641)
* NVDA više ne izvještava o mogućnosti klikanja više puta zaredom prilikom navigacije sadržajem koji se može kliknuti u načinu pregledavanja. (#7430)
* Geste izvedene na baum Vario 40 brajičnom pismu više se neće izvršavati. (#8894)
* U Google prezentacijama s Mozilla Firefoxom, NVDA više ne izvještava o odabranom tekstu na svakoj kontroli s fokusom. (#8964)

### Promjene za programere

* gui.nvdaControls sada sadrži dvije klase za stvaranje pristupačnih popisa s potvrdnim okvirima. (#7325)
 * CustomCheckListBox je pristupačna podklasa wx. CheckListBox.
 * AutoWidthColumnCheckListCtrl dodaje pristupačne potvrdne okvire u AutoWidthColumnListCtrl, koji se i sam temelji na wx-u. ListCtrl.
* Ako trebate učiniti wx widget pristupačnim, a to već nije, to je moguće učiniti korištenjem instance gui.accPropServer.IAccPropServer_impl. (#7491)
 * Dodatne informacije potražite u implementaciji gui.nvdaControls.ListCtrlAccPropServer.
* Ažuriran configobj na 5.1.0dev commit 5b5de48a. (#4470)
* Akcija config.post_configProfileSwitch sada preuzima neobavezni argument ključne riječi prevConf, omogućujući rukovateljima da poduzmu akciju na temelju razlika između konfiguracije prije i nakon promjene profila. (#8758)

## 2018.3.2

Ovo je manje izdanje za zaobilaženje rušenja u pregledniku Google Chrome prilikom navigacije tweetovima na [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Ovo je manje izdanje za ispravljanje kritične greške u NVDA koja je uzrokovala pad 32-bitnih verzija Mozilla Firefoxa. (#8759)

## 2018.3

Istaknute značajke ovog izdanja uključuju automatsko otkrivanje mnogih Brailleovih zaslona, podršku za nove značajke sustava Windows 10, uključujući Windows 10 Emoji ploču za unos i mnoge druge ispravke grešaka.

### Nove značajke

* NVDA će prijaviti gramatičke pogreške kada ih web stranice u Mozilla Firefoxu i Google Chromeu na odgovarajući način otkriju. (#8280)
* Sadržaj koji je označen kao umetnut ili izbrisan na web-stranicama sada se prijavljuje u pregledniku Google Chrome. (#8558)
* Dodana je podrška za BrailleNote QT i Apex BT-ov kotačić za pomicanje kada se BrailleNote koristi kao Brailleov zaslon s NVDA. (#5992, #5993)
* Dodane su skripte za izvještavanje o proteklom i ukupnom vremenu trenutne pjesme u Foobar2000. (#6596)
* Simbol Mac naredbene tipke (⌘) sada se najavljuje prilikom čitanja teksta bilo kojim sintisajzerom. (#8366)
* Prilagođene uloge putem atributa aria-roledescription sada su podržane u svim web preglednicima. (#8448)
* Nove tablice na Brailleovom pismu: češki s 8 točaka, središnji kurdski, esperanto, mađarski, švedski s 8 točaka računalno brailleovo pismo. (#8226, #8437)
* Dodana je podrška za automatsko otkrivanje Brailleovih prikaza u pozadini. (#1271)
 * Trenutno su podržani ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille i HumanWare BrailleNote i Brailliant BI/B zasloni.
 * Ovu značajku možete omogućiti odabirom opcije automatski s popisa prikaza brajice u NVDA dijaloškom okviru za odabir brajice.
 * Dodatne pojedinosti potražite u dokumentaciji.
* Dodana je podrška za razne moderne značajke unosa uvedene u nedavnim izdanjima sustava Windows 10. To uključuje ploču emojija (Fall Creators Update), diktiranje (Fall Creators Update), prijedloge za unos hardverske tipkovnice (ažuriranje za travanj 2018.) i lijepljenje međuspremnika u oblaku (ažuriranje za listopad 2018.). (#7273)
* Sadržaj označen kao blok citat pomoću ARIA (role blockquote) sada je podržan u Mozilla Firefoxu 63. (#8577)

### Promjenama

* Popis dostupnih jezika u NVDA Općim postavkama sada je sortiran na temelju naziva jezika umjesto ISO 639 kodova. (#7284)
* Dodane su zadane geste za Alt+Shift+Tab i Windows+Tab sa svim podržanim Freedom Scientific brajicama. (#7387)
* Za ALVA BC680 i zaslone pretvarača protokola sada je moguće dodijeliti različite funkcije lijevoj i desnoj pametnoj tipki, palcu i tipkama etouch. (#8230)
* Za ALVA BC6 zaslone, kombinacija tipki sp2+sp3 sada će objaviti trenutni datum i vrijeme, dok sp1+sp2 oponaša Windows tipku. (#8230)
* Korisnik se jednom pita kada NVDA pokrene je li zadovoljan slanjem statistike korištenja NV Accessu prilikom provjere NVDA ažuriranja. (#8217)
* Prilikom provjere ažuriranja, ako je korisnik pristao dopustiti slanje statistike korištenja NV Accessu, NVDA će sada poslati naziv trenutnog sintisajzerskog drajvera i Brailleovog pisma koji se koristi, kako bi pomogao u boljem određivanju prioriteta za budući rad na tim upravljačkim programima. (#8217)
* Ažuriran prevoditelj brajice liblouis na verziju 3.6.0. (#8365)
* Ažuriran put do ispravne ruske tablice Brailleovog pisma s osam točaka. (#8446)
* Ažuriran eSpeak-ng na 1.49.3dev commit 910f4c2. (#8561)

### Ispravci grešaka

* Pristupačne oznake za kontrole u pregledniku Google Chrome sada se lakše prijavljuju u načinu pregledavanja kada se oznaka ne prikazuje kao sam sadržaj. (#4773)
* Obavijesti su sada podržane u Zoomu. Na primjer, to uključuje status isključivanja/uključivanja zvuka i dolazne poruke. (#7754)
* Prebacivanje kontekstne prezentacije brajice u modu pretraživanja više ne uzrokuje prestanak ispisa brajice prateći pokazivač načina pretraživanja. (#7741)
* ALVA BC680 Brajičevi zasloni više se povremeno ne inicijaliziraju. (#8106)
* Prema zadanim postavkama, ALVA BC6 zasloni više neće izvršavati emulirane tipke sistemske tipkovnice kada pritisnete kombinacije tipki koje uključuju sp2+sp3 za pokretanje interne funkcionalnosti. (#8230)
* Pritiskom na sp2 na ALVA BC6 zaslonu za emulaciju alt tipke sada radi kako je reklamirano. (#8360)
* NVDA više ne najavljuje suvišne promjene rasporeda tipkovnice. (#7383, #8419)
* Praćenje miša sada je mnogo preciznije u Notepadu i drugim kontrolama za uređivanje običnog teksta kada je u dokumentu s više od 65535 znakova. (#8397)
* NVDA će prepoznati više dijaloga u sustavu Windows 10 i drugim modernim aplikacijama. (#8405)
* Na Windows 10 ažuriranju za listopad 2018. i Server 2019 i novijim verzijama, NVDA više ne uspijeva pratiti fokus sustava kada se aplikacija zamrzne ili preplavi sustav događajima. (#7345, #8535)
* Korisnici su sada obaviješteni prilikom pokušaja čitanja ili kopiranja prazne statusne trake. (#7789)
* Riješen je problem zbog kojeg se stanje "nije provjereno" na kontrolama ne prijavljuje u govoru ako je kontrola prethodno napola provjerena. (#6946)
* Na popisu jezika u NVDA Općim postavkama, naziv jezika za burmanski jezik ispravno je prikazan u sustavu Windows 7. (#8544)
* U Microsoft Edgeu, NVDA će objaviti obavijesti kao što su dostupnost prikaza za čitanje i napredak učitavanja stranice. (#8423)
* Prilikom navigacije na popis na webu, NVDA će sada prijaviti svoju oznaku ako ju je autor web stranice naveo. (#7652)
* Prilikom ručnog dodjeljivanja funkcija gestama za određeni brajični zaslon, te se geste sada uvijek prikazuju kao dodijeljene tom zaslonu. Prije su se prikazivali kao da su dodijeljeni trenutno aktivnom zaslonu. (#8108)
* Sada je podržana 64-bitna verzija programa Media Player Classic. (#6066)
* Nekoliko poboljšanja podrške za Brailleovo pismo u programu Microsoft Word s omogućenom automatizacijom korisničkog sučelja:
 * Slično drugim tekstnim poljima s više redaka, kada se postavi na početak dokumenta na Brailleovom pismu, zaslon se sada pomiče tako da je prvi znak dokumenta na početku prikaza. (#8406)
 * Smanjena je pretjerano opširna prezentacija fokusa u govoru i na Brailleovom pismu prilikom fokusiranja dokumenta programa Word. (#8407)
 * Usmjeravanje pokazivača na Brailleovom pismu sada ispravno funkcionira kada je na popisu u dokumentu programa Word. (#7971)
 * Novoumetnute grafičke oznake/brojevi u Word dokumentu ispravno se prijavljuju i u govoru i na Brailleovom pismu. (#7970)
* U sustavu Windows 10 1803 i novijim verzijama sada je moguće instalirati dodatke ako je omogućena značajka "Koristi Unicode UTF-8 za svjetsku jezičnu podršku". (#8599)
* NVDA više neće učiniti iTunes 12.9 i novije verzije potpuno neupotrebljivima za interakciju. (#8744)

### Promjene za programere

* Dodan scriptHandler.script, koji može funkcionirati kao dekorator za skripte na objektima koji se mogu skriptirati. (#6266)
* Uveden je okvir za testiranje sustava za NVDA. (#708)
* Napravljene su neke promjene u modulu hwPortUtils: (#1271)
 * listUsbDevices sada daje rječnike s informacijama o uređaju, uključujući hardwareID i devicePath.
 * Rječnici koje daje listComPorts sada također sadrže unos usbID-a za COM priključke s USB VID/PID informacijama u njihovom hardverskom ID-u.
* Ažuriran wxPython na 4.0.3. (#7077)
* Budući da NVDA sada podržava samo Windows 7 SP1 i novije verzije, uklonjen je ključ "minWindowsVersion" koji se koristi za provjeru treba li UIA biti omogućen za određeno izdanje Windowsa. (#8422)
* Sada se možete registrirati da biste bili obaviješteni o radnjama spremanja/resetiranja konfiguracije putem novih radnji config.pre_configSave, config.post_configSave, config.pre_configReset i config.post_configReset. (#7598)
 * config.pre_configSave se koristi za obavještavanje kada se NVDA konfiguracija sprema za spremanje, a config.post_configSave se poziva nakon spremanja konfiguracije.
 * config.pre_configReset i config.post_configReset uključuje zastavicu tvornički zadane postavke koja određuje hoće li se postavke ponovno učitati s diska (false) ili vratiti na zadane postavke (true).
* config.configProfileSwitch preimenovan je u config.post_configProfileSwitch kako bi odražavao činjenicu da se ta radnja poziva nakon promjene profila. (#7598)
* Sučelja za automatizaciju korisničkog sučelja ažurirana su na Windows 10 ažuriranje za listopad 2018. i Server 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)

## 2018.2.1

Ovo izdanje uključuje ažuriranja prijevoda zbog uklanjanja značajke koja je uzrokovala probleme u zadnji čas.

## 2018.2

Istaknuti dijelovi ovog izdanja uključuju podršku za tablice u Kindleu za PC, podršku za HumanWare BrailleNote Touch i BI14 Brailleove zaslone, poboljšanja Onecore i Sapi5 sintisajzera govora, poboljšanja u programu Microsoft Outlook i još mnogo toga.

### Nove značajke

* Raspon redaka i stupaca za ćelije tablice sada se izvještava u govoru i Brailleovom pismu. (#2642)
* Naredbe za navigaciju NVDA tablicom sada su podržane u Google dokumentima (s omogućenim Brailleovim modom). (#7946)
* Dodana je mogućnost čitanja i navigacije tablicama u Kindleu za PC. (#7977)
* Podrška za HumanWare BrailleNote touch i Brailliant BI 14 brajice putem USB-a i Bluetootha. (#6524)
* U Windows 10 Fall Creators Update i novijim verzijama, NVDA može najavljivati obavijesti iz aplikacija kao što su Kalkulator i Windows Store. (#7984)
* Nove tablice za prijevod Brailleovog pisma: litavski 8 točaka, ukrajinski, mongolski razred 2. (#7839)
* Dodana je skripta za izvješćivanje o informacijama o oblikovanju teksta ispod određene ćelije brajice. (#7106)
* Prilikom ažuriranja NVDA-a sada je moguće odgoditi instalaciju ažuriranja za kasniji trenutak. (#4263)
* Novi jezici: mongolski, švicarski njemački.
* Sada možete prebacivati control, shift, alt, windows i NVDA s brajice i kombinirati te modifikatore s brajičnim unosom (npr. pritisnite control+s). (#7306)
 * Ove nove prekidače modifikatora možete dodijeliti pomoću naredbi koje se nalaze u odjeljku Emulirane tipke sistemske tipkovnice u dijaloškom okviru Geste unosa.
* Vraćena podrška za Handy Tech Braillino i Modular (sa starim firmware) zaslonima. (#8016)
* Datum i vrijeme za podržane Handy Tech uređaje (kao što su Active Braille i Active Star) sada će se automatski sinkronizirati od strane NVDA kada nisu sinkronizirani dulje od pet sekundi. (#8016)
* Može se dodijeliti gesta unosa kako bi se privremeno onemogućili svi okidači konfiguracijskog profila. (#4935)

### Promjenama

* Stupac statusa u upravitelju dodataka promijenjen je kako bi se naznačilo je li dodatak omogućen ili onemogućen, a ne pokrenut ili obustavljen. (#7929)
* Ažuriran prevoditelj brajice liblouis na 3.5.0. (#7839)
* Litavska tablica na Brailleovom pismu preimenovana je u litavsku tablicu sa 6 točaka kako bi se izbjegla zabuna s novom tablicom s 8 točaka. (#7839)
* Francuske (Kanada) tablice 1. i 2. razreda su uklonjene. Umjesto toga, koristit će se francuska (ujedinjena) računalna brajica sa 6 točaka i tablice 2. stupnja. (#7839)
* Sekundarni gumbi za usmjeravanje na Alva BC6, EuroBrailleovom i Papenmeierovom Brailleovom pismu sada izvještavaju o informacijama o oblikovanju teksta ispod brajice tog gumba. (#7106)
* Skraćene tablice za unos Brailleovog pisma automatski će se vratiti u neskraćeni način rada u slučajevima koji se ne mogu uređivati (tj. kontrole u kojima nema pokazivača ili u načinu pregledavanja). (#7306)
* NVDA je sada manje opširan kada termin ili termin u Outlook kalendaru pokriva cijeli dan. (#7949)
* Sve NVDA postavke sada se mogu pronaći u jednom dijaloškom okviru postavki pod NVDA izbornikom -> Postavke -> Postavke, umjesto da su razbacane po mnogim dijaloškim okvirima. (#577)
* Zadani sintisajzer govora kada se izvodi u sustavu Windows 10 sada je oneCore govor, a ne eSpeak. (#8176)

### Ispravci grešaka

* NVDA više ne uspijeva čitati fokusirane kontrole na zaslonu za prijavu na Microsoftov račun u Postavkama nakon unosa adrese e-pošte. (#7997)
* NVDA više ne uspijeva pročitati stranicu kada se vratite na prethodnu stranicu u Microsoft Edgeu. (#7997)
* NVDA više neće pogrešno najavljivati konačni znak PIN-a za prijavu na Windows 10 dok se uređaj otključava. (#7908)
* Oznake potvrdnih okvira i izbornih gumba u Chromeu i Firefoxu više se ne prijavljuju dvaput prilikom kartice ili upotrebe brze navigacije u načinu pregledavanja. (#7960)
* aria-current s vrijednošću false bit će objavljen kao "false" umjesto "true". (#7892).
* Windows OneCore Voices više se ne učitava ako je konfigurirani glas deinstaliran. (#7553)
* Promjena glasova u Windows OneCore Voices sada je puno brža. (#7999)
* Popravljen je neispravan izlaz Brailleovog pisma za nekoliko tablica na Brailleovom pismu, uključujući velike znakove u danskom Brailleovom pismu sa skraćenim 8 točaka. (#7526, #7693)
* NVDA sada može prijaviti više vrsta grafičkih oznaka u programu Microsoft Word. (#6778)
* Pritiskom na skriptu za oblikovanje izvješća više se ne pomiče reviewPosition pogrešno i stoga višekratni pritisak više ne daje različite rezultate. (#7869)
* Unos Brailleovog pisma više ne dopušta korištenje ugovorene brajice u slučajevima kada nije podržan (tj. cijele riječi više se neće slati u sustav izvan tekstualnog sadržaja i u načinu pregledavanja). (#7306)
* Riješeni su problemi sa stabilnošću veze za zaslone Handy Tech Easy Braille i Braille Wave. (#8016)
* U sustavu Windows 8 i novijim verzijama, NVDA više neće objavljivati "nepoznato" prilikom otvaranja izbornika brzih veza )Windows+X) i odabira stavki iz ovog izbornika. (#8137)
* Geste specifične za model na gumbima na Hims zaslonima sada rade kako je oglašeno u korisničkom priručniku. (#8096)
* NVDA će sada pokušati ispraviti probleme s registracijom COM-a sustava uzrokujući da programi kao što su Firefox i Internet Explorer postanu nedostupni i prijave "Nepoznato" od strane NVDA-e. (#2807)
* Zaobišao je grešku u Upravitelju zadataka zbog koje NVDA ne dopušta korisnicima pristup sadržaju određenih detalja o procesima. (#8147)
* Noviji glasovi Microsoft SAPI5 više ne zaostaju na kraju govora, što čini navigaciju s tim glasovima mnogo učinkovitijom. (#8174)
* NVDA više ne izvještava (LTR i RTL oznake) na Brailleovom pismu ili govoru po znaku prilikom pristupa satu u novijim verzijama sustava Windows. (#5729)
* Otkrivanje tipki za pomicanje na zaslonima Hims Smart Beetle ponovno nije nepouzdano. (#6086)
* U nekim tekstualnim kontrolama, posebno u Delphi aplikacijama, informacije o uređivanju i navigaciji sada su mnogo pouzdanije. (#636, #8102)
* U sustavu Windows 10 RS5 NVDA više ne izvještava o dodatnim suvišnim informacijama prilikom prebacivanja zadataka pomoću alt+tab. (#8258)

### Promjene za razvojne programere

* Informacije za razvojne inženjere za UIA objekte sada sadrže popis dostupnih UIA uzoraka. (#5712)
* Moduli aplikacije sada mogu prisiliti određene prozore da uvijek koriste UIA implementacijom metode isGoodUIAWindow. (#7961)
* Skrivena logička oznaka "outputPass1Only" u odjeljku Brailleovog pisma konfiguracije ponovno je uklonjena. Liblouis više ne podržava izlaz samo za prolaz 1. (#7839)

## 2018.1.1

Ovo je posebno izdanje NVDA koje rješava grešku u upravljačkom programu Onecore Windows Speech sintisajzera, zbog čega je govorio s većom visinom i brzinom u sustavu Windows 10 Redstone 4 (1803). (#8082)

## 2018.1

Istaknuti dijelovi ovog izdanja uključuju podršku za grafikone u Microsoft Wordu i PowerPointu, podršku za nove Brailleove zaslone uključujući Eurobraille i pretvarač protokola Optelec, poboljšanu podršku za Brailleove zaslone Hims i Optelec, poboljšanja performansi za Mozilla Firefox 58 i novije verzije i još mnogo toga.

### Nove značajke

* Sada je moguća interakcija s grafikonima u programima Microsoft Word i Microsoft PowerPoint, slično postojećoj podršci za grafikone u programu Microsoft Excel. (#7046)
 * U programu Microsoft Word: Kada ste u načinu pregledavanja, pokazivač na ugrađeni grafikon i pritisnite enter za interakciju s njim.
 * U programu Microsoft PowerPoint prilikom uređivanja slajda: tabulatorom do objekta grafikona i pritisnite enter ili razmaknicu za interakciju s grafikonom.
 * Da biste zaustavili interakciju s grafikonom, pritisnite escape.
* Novi jezik: kirgiski.
* Dodana podrška za VitalSource Bookshelf. (#7155)
* Dodana je podrška za pretvarač protokola Optelec, uređaj koji omogućuje korištenje Brailleovog Voyagera i satelitskih zaslona pomoću komunikacijskog protokola ALVA BC6. (#6731)
* Sada je moguće koristiti Brailleov ulaz s ALVA 640 Comfort brajičnim pismom. (#7733)
 * NVDA funkcija brajičnog unosa može se koristiti s ovim, kao i s drugim BC6 zaslonima s firmverom 3.0.0 i novijim.
* Rana podrška za Google tablice s omogućenim načinom rada Brailleovog pisma. (#7935)
* Podrška za Eurobraille Esys, Esytime i Iris Brailleove zaslone. (#7488)

### Promjenama

* Upravljački programi HIMS Braille Sense/Braille EDGE/Smart Beetle i Hims Sync Brailleovog zaslona zamijenjeni su jednim upravljačkim programom. Novi upravljački program automatski će se aktivirati za bivše korisnike upravljačkog programa za sinkronizaciju Brailleovog pisma. (#7459)
 * Neke tipke, posebno tipke za pomicanje, preraspoređene su kako bi slijedile konvencije koje koriste Himsovi proizvodi. Za više detalja pogledajte korisnički priručnik.
* Kada tipkate zaslonskom tipkovnicom putem interakcije dodirom, prema zadanim postavkama sada morate dvaput dodirnuti svaku tipku na isti način na koji biste aktivirali bilo koju drugu kontrolu. (#7309)
 * Da biste koristili postojeći način "tipkanja dodirom" u kojem je jednostavno podizanje prsta s tipke dovoljno da biste ga aktivirali, omogućite ovu opciju u novom dijaloškom okviru postavki interakcije dodirom koji se nalazi u izborniku Postavke.
* Više nije potrebno izričito vezati Brailleovo pismo za fokusiranje ili pregled jer će se to automatski dogoditi prema zadanim postavkama. (#2385)
 * Imajte na umu da će se automatsko povezivanje za pregled dogoditi samo kada koristite pokazivač pregleda ili naredbu za navigaciju objektom. Pomicanje neće aktivirati ovo novo ponašanje.

### Ispravci grešaka

* Poruke koje se mogu pregledavati, kao što je prikaz trenutnog formatiranja kada se dvaput brzo pritisne NVDA+f, više ne uspijevaju kada je NVDA instaliran na putu s ne-ASCII znakovima. (#7474)
* Fokus se sada ponovno ispravno vraća kada se vratite na Spotify iz druge aplikacije. (#7689)
* U Windows 10 Fall Creaters Update, NVDA se više ne ažurira kada je omogućen kontrolirani pristup mapi iz Windows Defender Security Centera. (#7696)
* Otkrivanje tipki za pomicanje na zaslonima Hims Smart Beetle više nije nepouzdano. (#6086)
* Blago poboljšanje performansi pri renderiranju velikih količina sadržaja u Mozilla Firefoxu 58 i novijim verzijama. (#7719)
* U programu Microsoft Outlook čitanje e-pošte koja sadrži tablice više ne uzrokuje pogreške. (#6827)
* Geste na Brailleovom pismu koje oponašaju modifikatore tipki tipkovnice sustava sada se mogu kombinirati i s drugim emuliranim tipkama tipkovnice sustava ako je jedna ili više uključenih gesti specifično za model. (#7783)
* U pregledniku Mozilla Firefox, način pregledavanja sada ispravno funkcionira u skočnim prozorima koje stvaraju proširenja kao što su LastPass i bitwarden. (#7809)
* NVDA se više ne zamrzava pri svakoj promjeni fokusa ako Firefox ili Chrome prestanu reagirati, primjerice zbog zamrzavanja ili rušenja. (#7818)
* U twitter klijentima kao što je Chicken Nugget, NVDA više neće ignorirati posljednjih 20 znakova od 280 znakova tweetova kada ih čita. (#7828)
* NVDA sada koristi ispravan jezik prilikom najavljivanja simbola kada je odabran tekst. (#7687)
* U novijim verzijama sustava Office 365 ponovno je moguće kretati se Excel grafikonima pomoću tipki sa strelicama. (#7046)
* U govoru i Brailleovom pismu, kontrolna stanja sada će se uvijek izvještavati istim redoslijedom, bez obzira jesu li pozitivna ili negativna. (#7076)
* U aplikacijama kao što je Windows 10 Mail, NVDA više neće propuštati najavljivati izbrisane znakove kada pritisnete backspace. (#7456)
* Sve tipke na zaslonima Hims Braille Sense Polaris sada rade prema očekivanjima. (#7865)
* NVDA se više ne pokreće u sustavu Windows 7 koji se žali na interni api-ms dll, kada je određena verzija programa Visual Studio 2017 za redistribuciju instalirana u drugoj aplikaciji. (#7975)

### Promjene za razvojne programere

* Dodana je skrivena logička zastavica u odjeljak brajice u konfiguraciji: "outputPass1Only". (#7301, #7693, #7702)
 * Ova zastavica je zadana na true. Ako je netočno, liblouis multi pass pravila koristit će se za Brailleov izlaz.
* Novi rječnik (Brailleovo pismo. RENAMED_DRIVERS) je dodan kako bi se omogućio nesmetan prijelaz za korisnike koji koriste upravljačke programe koje su zamijenili drugi. (#7459)
* Ažuriran paket komtipova na 1.1.3. (#7831)
* Implementiran je generički sustav na Brailleovom pismu. BrailleDisplayDriver za rad sa zaslonima koji šalju pakete potvrde/potvrde. Pogledajte handyTech upravljački program za brajicu kao primjer. (#7590, #7721)
* Nova varijabla "isAppX" u konfiguracijskom modulu može se koristiti za otkrivanje radi li NVDA kao Windows Desktop Bridge Store aplikacija. (#7851)
* Za implementacije dokumenata kao što su NVDAObjects ili browseMode koje imaju textInfo, sada postoji nova klasa documentBase.documentWithTableNavigation koja se može naslijediti da bi se dobile standardne skripte za navigaciju tablicama. Molimo pogledajte ovaj razred da biste vidjeli koje pomoćne metode mora osigurati vaša implementacija da bi navigacija tablicom funkcionirala. (#7849)
* Skupna datoteka scons sada se bolje nosi kada je instaliran i Python 3, koristeći pokretač za posebno pokretanje pythona 2.7 32 bita. (#7541)
* hwIo.Hid sada uzima dodatni parametar exclusive, koji je zadani True. Ako je postavljeno na False, drugim aplikacijama dopušteno je komunicirati s uređajem dok je povezan s NVDA. (#7859)

## 2017.4

Istaknuti dijelovi ovog izdanja uključuju mnoge popravke i poboljšanja web-podrške, uključujući način pregledavanja za web-dijaloške okvire prema zadanim postavkama, bolje izvješćivanje o oznakama grupa polja u načinu pregledavanja, podršku za nove tehnologije sustava Windows 10 kao što su Windows Defender Application Guard i Windows 10 na ARM64 te automatsko izvješćivanje o orijentaciji zaslona i statusu baterije.
Imajte na umu da ova verzija NVDA više ne podržava Windows XP ili Windows Vista. Minimalni preduvjet za NVDA sada je Windows 7 sa servisnim paketom Service Pack 1.

### Nove značajke

* U načinu pregledavanja, sada je moguće preskočiti pored/na početak orijentira pomoću naredbi "preskoči na kraj/početak kontejnera" (zarez/shift+zarez). (#5482)
* U Firefoxu, Chromeu i Internet Exploreru brza navigacija za uređivanje polja i polja obrazaca sada uključuje sadržaj obogaćenog teksta koji se može uređivati (tj. (#5534)
* U web-preglednicima popis elemenata sada može navesti polja i gumbe obrasca. (#588)
* Početna podrška za Windows 10 na ARM64. (#7508)
* Rana podrška za čitanje i interaktivnu navigaciju matematičkim sadržajem za Kindle knjige s pristupačnom matematikom. (#7536)
* Dodana podrška za Azardi čitač e-knjiga. (#5848)
* Informacije o verziji dodataka sada se prijavljuju prilikom ažuriranja. (#5324)
* Dodani su novi parametri naredbenog retka za stvaranje prijenosne kopije NVDA. (#6329)
* Podrška za Microsoft Edge koji se izvodi unutar Windows Defender Application Guarda u Windows 10 Fall Creators Update. (#7600)
* Ako radi na prijenosnom računalu ili tabletu, NVDA će sada izvijestiti kada je punjač spojen/isključen i kada se promijeni orijentacija zaslona. (#4574, #4612)
* Novi jezik: makedonski.
* Nove tablice prijevoda na Brailleovom pismu: hrvatski razred 1, vijetnamski razred 1. razred. (#7518, #7565)
* Dodana je podrška za Actilino Brailleov zaslon tvrtke Handy Tech. (#7590)
* Unos brajice za zaslone za Brailleovo pismo Handy Tech sada je podržan. (#7590)

### Promjenama

* Minimalni podržani operativni sustav za NVDA sada je Windows 7 Service Pack 1 ili Windows Server 2008 R2 Service Pack 1. (#7546)
* Web dijaloški okviri u Firefox i Chrome web preglednicima sada automatski koriste način pregledavanja, osim ako se ne nalaze u web aplikaciji. (#4493)
* U načinu pregledavanja, tabulatori i pomicanje pomoću naredbi za brzu navigaciju više ne najavljuju iskakanje iz spremnika kao što su popisi i tablice, što navigaciju čini učinkovitijom. (#2591)
* U načinu pregledavanja za Firefox i Chrome, nazivi grupa polja obrasca sada se najavljuju kada se krećete u njih brzom navigacijom ili prilikom kartice. (#3321)
* U načinu pregledavanja, naredba za brzu navigaciju za ugrađene objekte (o i shift+o) sada uključuje audio i video elemente, kao i elemente s aplikacijom aria uloga i dijaloškim okvirom. (#7239)
* Espeak-ng je ažuriran na 1.49.2, rješavajući neke probleme s proizvodnjom verzija izdanja. (#7385, #7583)
* Pri trećoj aktivaciji naredbe 'čitaj statusnu traku', njezin se sadržaj kopira u međuspremnik. (#1785)
* Kada dodjeljujete geste tipkama na Baumovom zaslonu, možete ih ograničiti na model zaslona za brajicu koji se koristi (npr. VarioUltra ili Pronto). (#7517)
* Prečac za polje filtra na popisu elemenata u načinu pregledavanja promijenio se iz alt+f u alt+e. (#7569)
* Dodana je nevezana naredba za način pregledavanja kako bi se uključilo uključivanje tablica izgleda u hodu. Ovu naredbu možete pronaći u kategoriji Način pregledavanja u dijaloškom okviru Ulazne geste. (#7634)
* Nadograđen liblouis prevoditelj brajice na 3.3.0. (#7565)
* Prečac za izborni gumb regularnog izraza u dijaloškom okviru rječnika promijenio se iz alt+r u alt+e. (#6782)
* Datoteke glasovnog rječnika sada su verzionirane i premještene su u direktorij 'speechDicts/voiceDicts.v1'. (#7592)
* Izmjene verzija datoteka (korisnička konfiguracija, glasovni rječnici) više se ne spremaju kada se NVDA pokrene iz pokretača. (#7688)
* Braillino, Bookworm i Modular (sa starim firmware) Braillino, Bookworm i modularni (sa starim firmware) zasloni za brajicu tvrtke Handy Tech više nisu podržani iz kutije. Instalirajte Handy Tech Universal Driver i NVDA dodatak za korištenje ovih zaslona. (#7590)

### Ispravci grešaka

* Veze su sada označene na Brailleovom pismu u aplikacijama kao što je Microsoft Word. (#6780)
* NVDA više ne postaje osjetno sporiji kada je otvoreno mnogo kartica u Firefox ili Chrome web preglednicima. (#3138)
* Usmjeravanje kursora za MDV Lilli Brailleov zaslon više se ne pomiče pogrešno za jednu Brajicovu ćeliju ispred mjesta na kojem bi trebala biti. (#7469)
* U pregledniku Internet Explorer i drugim MSHTML dokumentima sada je podržan obavezni atribut HTML5 koji označava obavezno stanje polja obrasca. (#7321)
* Brajičevi se zasloni sada ažuriraju prilikom upisivanja arapskih znakova u dokument programa WordPad poravnat ulijevo. (#511)
* Pristupačne oznake za kontrole u Mozilla Firefoxu sada se lakše prijavljuju u načinu pregledavanja kada se oznaka ne pojavljuje kao sam sadržaj. (#4773)
* Na Windows 10 Creaters Updateu, NVDA može ponovno pristupiti Firefoxu nakon ponovnog pokretanja NVDA-a. (#7269)
* Prilikom ponovnog pokretanja NVDA s Mozilla Firefoxom u fokusu, način pregledavanja će ponovno biti dostupan, iako ćete možda morati isključiti alt+tab i ponovno natrag. (#5758)
* Sada je moguće pristupiti matematičkom sadržaju u pregledniku Google Chrome na sustavu bez instaliranog Mozilla Firefoxa. (#7308)
* Operativni sustav i druge aplikacije trebale bi biti stabilnije neposredno nakon instalacije NVDA prije ponovnog pokretanja, u usporedbi s instalacijama prethodnih NVDA verzija. (#7563)
* Kada koristite naredbu za prepoznavanje sadržaja (npr. NVDA+r), NVDA sada izvještava o pogrešci umjesto ništa ako je objekt navigatora nestao. (#7567)
* Ispravljena je funkcija pomicanja unatrag za Brailleove zaslone Freedom Scientific koji sadrže lijevu šipku branika. (#7713)

### Promjene za programere

* "Scons testovi" sada provjerava imaju li prevodivi nizovi komentare prevoditelja. Ovo možete pokrenuti i sami s "scons checkPot". (#7492)
* Sada postoji novi modul extensionPoints koji pruža generički okvir za omogućavanje proširivosti koda na određenim točkama u kodu. To omogućuje zainteresiranim stranama da se registriraju kako bi bile obaviještene kada se dogodi neka radnja (extensionPoints.Action), da izmijene određenu vrstu podataka (extensionPoints.Filter) ili da sudjeluju u odlučivanju hoće li se nešto poduzeti (extensionPoints.Decider). (#3393)
* Sada se možete registrirati da biste bili obaviješteni o promjenama konfiguracijskog profila putem radnje config.configProfileSwitched. (#3393)
* Geste na Brailleovom pismu koje oponašaju modifikatore tipki tipkovnice sustava (kao što su Control i Alt) sada se mogu kombinirati s drugim emuliranim tipkama tipkovnice sustava bez eksplicitne definicije. (#6213)
 * Na primjer, ako imate tipku na zaslonu vezanu za tipku alt i drugu tipku za prikaz sa strelicom prema dolje, kombiniranje tih tipki rezultirat će emulacijom alt+downArrow.
* Brailleovo pismo. Klasa BrailleDisplayGesture sada ima dodatno svojstvo modela. Ako je navedeno, pritiskom na tipku generirat će se dodatni identifikator geste specifičan za model. To korisniku omogućuje povezivanje gesta ograničenih na određeni model Brailleovog pisma.
 * Pogledajte baum upravljački program kao primjer za ovu novu funkcionalnost.
* NVDA je sada kompajliran sa Visual Studio 2017 i Windows 10 SDK. (#7568)

## 2017.3

Istaknuti dijelovi ovog izdanja uključuju unos ugovorene Brailleove pisme, podršku za nove Windows OneCore glasove dostupne u sustavu Windows 10, ugrađenu podršku za Windows 10 OCR i mnoga značajna poboljšanja u vezi s Brailleovim pismom i webom.

### Nove značajke

* Dodana je postavka Brailleovog pisma za "prikazivanje poruka na neodređeno vrijeme". (#6669)
* Na popisima poruka u programu Microsoft Outlook, NVDA sada izvještava je li poruka označena zastavicom. (#6374)
* U programu Microsoft PowerPoint sada se prilikom uređivanja slajda (kao što su trokut, krug, videozapis ili strelica) izvješćuje o točnoj vrsti oblika, a ne samo o "obliku". (#7111)
* Matematički sadržaj (dostupan kao MathML) sada je podržan u pregledniku Google Chrome. (#7184)
* NVDA sada može govoriti koristeći nove Windows OneCore glasove (poznate i kao Microsoft Mobile glasovi) uključene u Windows 10. Njima možete pristupiti odabirom Windows OneCore glasova u NVDA dijaloškom okviru sintisajzera. (#6159)
* NVDA korisničke konfiguracijske datoteke sada se mogu pohraniti u korisnikovu mapu s podacima lokalne aplikacije. To je omogućeno putem postavke u registru. Za više detalja pogledajte "Parametri za cijeli sustav" u Korisničkom priručniku. (#6812)
* U web preglednicima, NVDA sada izvještava o vrijednostima rezerviranih mjesta za polja (točnije, sada je podržano aria-placeholder). (#7004)
* U načinu pregledavanja za Microsoft Word sada je moguće navigirati do pravopisnih pogrešaka pomoću brze navigacije (w i shift+w). (#6942)
* Dodana je podrška za kontrolu Odabir datuma koja se nalazi u dijaloškim okvirima Obveze programa Microsoft Outlook. (#7217)
* Trenutačno odabrani prijedlog sada se prijavljuje u poljima Windows 10 Pošta na/cc i polje za pretraživanje postavki sustava Windows 10. (#6241)
* Sada se reproducira zvuk koji označava pojavu prijedloga u određenim poljima za pretraživanje u sustavu Windows 10 (npr. početni zaslon, pretraživanje postavki, polja pošte na / cc u sustavu Windows 10). (#6241)
* NVDA sada automatski izvještava o obavijestima u Skype za tvrtke za stolna računala, primjerice kada netko započne razgovor s vama. (#7281)
* NVDA sada automatski izvještava o dolaznim chat porukama dok ste u Skype za Business razgovoru. (#7286)
* NVDA sada automatski izvještava o obavijestima u Microsoft Edgeu, primjerice kada preuzimanje započne. (#7281)
* Sada možete upisivati i skraćenu i neskraćenu brajicu na Brailleovom pismu s brajičnom tipkovnicom. Pojedinosti potražite u odjeljku Unos brajice u Korisničkom priručniku. (#2439)
* Sada možete unijeti Unicode brajeve znakove s brajične tipkovnice na Brajičevom pismu tako da odaberete Unicode brajicu kao ulaznu tablicu u postavkama brajice. (#6449)
* Dodana je podrška za SuperBrailleov zaslon na brajici koji se koristi na Tajvanu. (#7352)
* Nove tablice za prevođenje Brailleovog pisma: danski računalni braille s 8 točaka, litavski, perzijski računalni braille s 8 točaka, perzijski razred 1, slovenski računalni braille s 8 točaka. (#6188, #6550, #6773, #7367)
* Poboljšana engleska (SAD) računalna brajeva tablica s 8 točaka, uključujući podršku za grafičke oznake, znak eura i slova s naglaskom. (#6836)
* NVDA sada može koristiti OCR funkcionalnost uključenu u Windows 10 za prepoznavanje teksta slika ili nedostupnih aplikacija. (#7361)
 * Jezik se može postaviti u novom Windows 10 OCR dijaloškom okviru u NVDA postavkama.
 * Za prepoznavanje sadržaja trenutnog objekta navigatora pritisnite NVDA+r.
 * Dodatne pojedinosti potražite u odjeljku Prepoznavanje sadržaja u Korisničkom priručniku.
* Sada možete odabrati koje će se kontekstne informacije prikazivati na Brailleovom pismu kada se objekt fokusira pomoću nove postavke "Fokus kontekstne prezentacije" u dijaloškom okviru Postavke brajice. (#217)
 * Na primjer, opcije "Ispuni prikaz za promjene konteksta" i "Samo pri pomicanju unatrag" mogu učiniti rad s popisima i izbornicima učinkovitijim, budući da stavke neće stalno mijenjati svoj položaj na zaslonu.
 * Pogledajte odjeljak o postavki "Prezentacija konteksta fokusa" u Korisničkom priručniku za dodatne pojedinosti i primjere.
* U Firefoxu i Chromeu, NVDA sada podržava složene dinamičke rešetke kao što su proračunske tablice u kojima se samo dio sadržaja može učitati ili prikazati (točnije, atributi aria-rowcount, aria-colcount, aria-rowindex i aria-colindex uvedeni u ARIA 1.1). (#7410)

### Promjenama

* Dodana je nevezana naredba za ponovno pokretanje NVDA na zahtjev. Možete ga pronaći u kategoriji Razno dijaloškog okvira Ulazne geste. (#6396)
* Raspored tipkovnice sada se može podesiti iz NVDA dijaloškog okvira dobrodošlice. (#6863)
* Mnogo više vrsta kontrole i stanja skraćeno je za Brailleovo pismo. Znamenitosti su također skraćene. Za potpuni popis pogledajte "Vrsta kontrole, država i kratice orijentira" pod Brailleovim pismom u Korisničkom priručniku. (#7188, #3975)
* Ažuriran eSpeak NG na 1.49.1. (#7280)
* Popisi izlazne i ulazne tablice u dijaloškom okviru Postavke brajice sada su poredani abecednim redom. (#6113)
* Ažuriran liblouis prevoditelj brajice na 3.2.0. (#6935)
* Zadana tablica brajice sada je Unified English Braille Code 1. stupnja. (#6952)
* Prema zadanim postavkama, NVDA sada prikazuje samo dijelove kontekstnih informacija koji su se promijenili na Brailleovom pismu kada se objekt fokusira. (#217)
 * Prije je uvijek prikazivao što više informacija o kontekstu, bez obzira na to jeste li već vidjeli iste informacije o kontekstu.
 * Možete se vratiti na staro ponašanje promjenom nove postavke "Kontekstna prezentacija fokusa" u dijaloškom okviru postavki Brailleovog pisma u "Uvijek ispuniti prikaz".
* Kada koristite Brailleovo pismo, pokazivač se može konfigurirati tako da bude različitog oblika kada je vezan za fokusiranje ili pregled. (#7122)
* NVDA logotip je ažuriran. Ažurirani NVDA logotip stilizirana je mješavina slova NVDA u bijeloj boji, na jednobojnoj ljubičastoj pozadini. To osigurava da će biti vidljiv na pozadini bilo koje boje i koristi ljubičastu boju s logotipa NV Access. (#7446)

### Ispravci grešaka

* Oznaka elemenata div koji se mogu uređivati u Chromeu više se ne prijavljuje kao vrijednost dok su u načinu pregledavanja. (#7153)
* Pritiskom na end dok ste u načinu pregledavanja za prazan Microsoft Word dokument više ne uzrokuje pogrešku tijekom izvođenja. (#7009)
* Način pregledavanja sada je ispravno podržan u pregledniku Microsoft Edge gdje je dokumentu dodijeljena određena ARIA uloga dokumenta. (#6998)
* U načinu pregledavanja sada možete odabrati ili poništiti odabir do kraja retka pomoću shift+end čak i kada je kursor na posljednjem znaku retka. (#7157)
* Ako dijaloški okvir sadrži traku napretka, tekst dijaloškog okvira sada se ažurira na Brailleovom pismu kada se promijeni traka napretka. To znači, na primjer, da se preostalo vrijeme sada može očitati u NVDA dijaloškom okviru "Preuzimanje ažuriranja". (#6862)
* NVDA će sada objaviti promjene odabira za određene kombinirane okvire sustava Windows 10 kao što je automatska reprodukcija u postavkama. (#6337).
* Besmislene informacije više se ne objavljuju prilikom ulaska u dijaloške okvire za stvaranje sastanka / sastanka u programu Microsoft Outlook. (#7216)
* Zvučni signali za neodređene dijaloške okvire trake napretka, kao što je alat za provjeru ažuriranja, samo kada je izlaz trake napretka konfiguriran tako da uključuje zvučne signale. (#6759)
* U programima Microsoft Excel 2003 i 2007 ćelije se ponovno prijavljuju prilikom strelica oko radnog lista. (#7243)
* U Windows 10 Creators Update i novijim verzijama, način pregledavanja ponovno je automatski omogućen prilikom čitanja e-pošte u Windows 10 Mailu. (#7289)
* Na većini brajevih zaslona s brajičnom tipkovnicom, točka 7 sada briše posljednju unesenu brajičnu ćeliju ili znak, a točka 8 pritišće tipku Enter. (#6054)
* U tekstu koji se može uređivati, prilikom pomicanja kursora (npr. tipkama kursora ili backspaceom), NVDA govorne povratne informacije sada su točnije u mnogim slučajevima, posebno u Chrome i terminalnim aplikacijama. (#6424)
* Sada se može čitati sadržaj uređivača potpisa u programu Microsoft Outlook 2016. (#7253)
* U Java Swing aplikacijama, NVDA više ponekad ne uzrokuje rušenje aplikacije prilikom navigacije tablicama. (#6992)
* U Windows 10 Creators Updateu, NVDA više neće najavljivati obavijesti o tostu više puta. (#7128)
* U izborniku Start u sustavu Windows 10 pritiskom na Enter za zatvaranje izbornika Start nakon pretraživanja više ne uzrokuje da NVDA najavljuje tekst pretraživanja. (#7370)
* Brza navigacija do naslova u pregledniku Microsoft Edge sada je znatno brža. (#7343)
* U pregledniku Microsoft Edge navigacija u načinu pregledavanja više ne preskače velike dijelove određenih web-stranica kao što je tema Wordpress 2015. (#7143)
* U pregledniku Microsoft Edge orijentiri su ispravno lokalizirani na jezike koji nisu engleski. (#7328)
* Brailleovo pismo sada ispravno prati odabir prilikom odabira teksta izvan širine zaslona. Ako, primjerice, odaberete više redaka pomoću shift+strelica prema dolje, brajica sada prikazuje zadnji redak koji ste odabrali. (#5770)
* U Firefoxu, NVDA više ne izvještava lažno o "odjeljku" nekoliko puta kada otvara detalje za tweet na twitter.com. (#5741)
* Naredbe za navigaciju tablicom više nisu dostupne za tablice izgleda u načinu pregledavanja osim ako nije omogućeno izvješćivanje o tablicama izgleda. (#7382)
* U Firefoxu i Chromeu naredbe za navigaciju tablicom Način pregledavanja sada preskaču skrivene ćelije tablice. (#6652, #5655)

### Promjene za programere

* Vremenske oznake u dnevniku sada uključuju milisekunde. (#7163)
* NVDA se sada mora izgraditi pomoću Visual Studio Community 2015. Visual Studio Express više nije podržan. (#7110)
 * Sada su potrebni i Windows 10 alati i SDK, koji se mogu omogućiti prilikom instalacije Visual Studija.
 * Dodatne pojedinosti potražite u odjeljku Instalirane ovisnosti u readme-u.
* Podrška za prepoznavače sadržaja kao što su OCR i alati za opis slika može se jednostavno implementirati pomoću novog paketa contentRecog. (#7361)
* Python json paket sada je uključen u NVDA binarne verzije. (#3050)

## 2017.2

Istaknute značajke ovog izdanja uključuju punu podršku za prigušivanje zvuka u ažuriranju Windows 10 Creators Update; popravci za nekoliko problema s odabirom u načinu pregledavanja, uključujući probleme s odabirom svega; značajna poboljšanja u podršci za Microsoft Edge; i poboljšanja na webu, kao što je označavanje elemenata označenih kao tekući (pomoću ARIA-current).

### Nove značajke

* Informacije o obrubu ćelije sada se mogu prijaviti u programu Microsoft Excel pomoću NVDA+f. (#3044)
* U web preglednicima, NVDA sada pokazuje kada je element označen kao trenutni (točnije, koristeći atribut aria-current). (#6358)
* Automatska promjena jezika sada je podržana u pregledniku Microsoft Edge. (#6852)
* Dodana je podrška za Windows Calculator na Windows 10 Enterprise LTSB (Long-Term Servicing Branch) i Serveru. (#6914)
* Izvođenjem naredbe za čitanje trenutnog retka tri puta brzo se piše redak s opisima znakova. (#6893)
* Novi jezik: burmanski.
* Unicode strelice gore i dolje i simboli razlomaka sada se izgovaraju na odgovarajući način. (#3805)

### Promjenama

* Prilikom navigacije jednostavnim pregledom u aplikacijama koje koriste automatizaciju korisničkog sučelja, više stranih objekata sada se zanemaruje, što olakšava navigaciju. (#6948, #6950)

### Ispravci grešaka

* Stavke izbornika web stranice sada se mogu aktivirati dok ste u načinu pregledavanja. (#6735)
* Pritiskom na escape dok je konfiguracijski profil "Potvrdi brisanje" dijaloški okvir sada se zatvara dijaloški okvir. (#6851)
* Ispravljena su neka rušenja u Mozilla Firefoxu i drugim Gecko aplikacijama gdje je omogućena značajka više procesa. (#6885)
* Izvještavanje o boji pozadine u pregledu zaslona sada je točnije kada je tekst nacrtan s prozirnom pozadinom. (#6467)
* Poboljšana podrška za opise kontrola na web-stranicama u pregledniku Internet Explorer 11 (konkretno, podrška za aria-describedby unutar iframeova i kada je navedeno više ID-ova). (#5784)
* U ažuriranju Windows 10 Creators Update, NVDA-ino prigušivanje zvuka ponovno radi kao u prethodnim izdanjima sustava Windows; tj. Patka s govorom i zvukovima, uvijek patka i bez saganja su dostupni. (#6933)
* NVDA više neće propuštati navigaciju ili prijavljivanje određenih (UIA) kontrola u kojima tipkovnički prečac nije definiran. (#6779)
* Dva prazna mjesta više se ne dodaju u informacije o tipkovnim prečacima za određene (UIA) kontrole. (#6790)
* Određene kombinacije tipki na HIMS zaslonima (npr. razmak+točka4) više ne otkazuju povremeno. (#3157)
* Riješen je problem prilikom otvaranja serijskog porta na sustavima koji koriste određene jezike osim engleskog, što je u nekim slučajevima uzrokovalo neuspjeh povezivanja s Brailleovim zaslonima. (#6845)
* Smanjena je mogućnost oštećenja konfiguracijske datoteke prilikom isključivanja sustava Windows. Konfiguracijske datoteke sada se zapisuju u privremenu datoteku prije zamjene stvarne konfiguracijske datoteke. (#3165)
* Kada dvaput brzo izvršite naredbu za čitanje trenutnog retka kako biste napisali redak, sada se koristi odgovarajući jezik za napisane znakove. (#6726)
* Navigacija po liniji u Microsoft Edgeu sada je do tri puta brža u ažuriranju Windows 10 Creators Update. (#6994)
* NVDA više ne najavljuje "Web Runtime grupiranje" kada fokusira Microsoft Edge dokumente u Windows 10 Creators Update. (#6948)
* Sada su podržane sve postojeće verzije SecureCRT-a. (#6302)
* Adobe Acrobat Reader više se ne ruši u određenim PDF dokumentima (točnije onima koji sadrže prazne atribute stvarnog teksta). (#7021, #7034)
* U načinu pregledavanja u pregledniku Microsoft Edge interaktivne tablice (ARIA rešetke) više se ne preskaču prilikom navigacije do tablica s t i shift+t. (#6977)
* U načinu pregledavanja, pritiskom na shift+home nakon odabira naprijed sada se poništava odabir na početku retka kao što se očekivalo. (#5746)
* U načinu pregledavanja odabir svega (control+a) više ne uspijeva odabrati sav tekst ako se kursor ne nalazi na početku teksta. (#6909)
* Riješeni su neki drugi rijetki problemi s odabirom u načinu pregledavanja. (#7131)

### Promjene za programere

* Argumenti naredbenog retka sada se obrađuju pomoću Pythonovog modula argparse, a ne optparse. To omogućuje isključivo rukovanje određenim opcijama kao što su -r i -q. (#6865)
* core.callLater sada stavlja povratni poziv u NVDA glavni red čekanja nakon zadanog kašnjenja, umjesto da probudi jezgru i izvrši je izravno. Ovo zaustavlja moguća zamrzavanja zbog slučajnog odlaska jezgre u stanje mirovanja nakon obrade povratnog poziva, u sredini modalnog poziva, kao što je uklanjanje okvira s porukama. (#6797)
* Svojstvo InputGesture.identifiers promijenjeno je tako da se više ne normalizira. (#6945)
 * Podklase više ne moraju normalizirati identifikatore prije nego što ih vrate iz ovog svojstva.
 * Ako želite normalizirane identifikatore, sada postoji svojstvo InputGesture.normalizedIdentifiers koje normalizira identifikatore koje vraća svojstvo identifiers .
* Svojstvo InputGesture.logIdentifier sada je zastarjelo. Pozivatelji bi umjesto toga trebali koristiti InputGesture.identifiers[0]. (#6945)
* Uklonjen je neki zastarjeli kod:
 * 'govor. REASON_*' konstante: umjesto toga treba koristiti 'controlTypes.REASON_*'. (#6846)
 * 'i18nName' za postavke sintisajzera: umjesto toga treba koristiti 'displayName' i 'displayNameWithAccelerator'. (#6846, #5185)
 * 'config.validateConfig'. (#6846, #667)
 * 'config.save': umjesto toga treba koristiti 'config.conf.save'. (#6846, #667)
* Popis dovršetka u kontekstnom izborniku automatskog dovršavanja Python konzole više ne prikazuje nijedan put objekta koji vodi do dovršetka konačnog simbola. (#7023)
* Sada postoji okvir za testiranje jedinica za NVDA. (#7026)
 * Jedinični testovi i infrastruktura nalaze se u imeniku testova/jedinica. Pojedinosti potražite u docstringu u datoteci tests\unit\init.py.
 * Testove možete pokrenuti pomoću "scons testova". Pojedinosti potražite u odjeljku "Izvođenje testova" u readme.md.
 * Ako šaljete zahtjev za povlačenje za NVDA, prvo biste trebali pokrenuti testove i provjeriti jesu li prošli.

## 2017.1

Istaknute značajke ovog izdanja uključuju izvještavanje o odjeljcima i tekstualnim stupcima u programu Microsoft Word; Podrška za čitanje, navigaciju i komentiranje knjiga u Kindleu za PC; i poboljšana podrška za Microsoft Edge.

### Nove značajke

* U programu Microsoft Word sada se mogu prijaviti vrste prijeloma sekcija i brojevi sekcija. To je omogućeno opcijom "Brojevi stranica izvješća" u dijaloškom okviru Oblikovanje dokumenta. (#5946)
* U programu Microsoft Word sada se mogu izvještavati o tekstnim stupcima. To je omogućeno opcijom "Brojevi stranica izvješća" u dijaloškom okviru za oblikovanje dokumenta. (#5946)
* Automatska promjena jezika sada je podržana u programu WordPad. (#6555)
* NVDA naredba za pronalaženje (NVDA+control+f) sada je podržana u načinu pregledavanja u pregledniku Microsoft Edge. (#6580)
* Brza navigacija gumbima u načinu pregledavanja (b i shift+b) sada je podržana u pregledniku Microsoft Edge. (#6577)
* Prilikom kopiranja lista u programu Microsoft Excel pamte se zaglavlja stupaca i redaka. (#6628)
* Podrška za čitanje i navigaciju knjigama u Kindleu za PC verzije 1.19, uključujući pristup vezama, fusnotama, grafikama, istaknutom tekstu i korisničkim bilješkama. Za više informacija pogledajte odjeljak Kindle za PC u NVDA korisničkom priručniku. (#6247, #6638)
* Navigacija tablicom načina pregledavanja sada je podržana u pregledniku Microsoft Edge. (#6594)
* U programu Microsoft Excel naredba za pregled pokazivača izvješća (radna površina: NVDA+numpadDelete, prijenosno računalo: NVDA+delete) sada izvještava o nazivu radnog lista i lokaciji ćelije. (#6613)
* Dodana je opcija u izlazni dijaloški okvir za ponovno pokretanje s zapisivanjem na razini otklanjanja pogrešaka. (#6689)

### Promjenama

* Minimalna brzina treptanja kursora na Brailleovom pismu sada je 200 ms. Ako je ovo prethodno postavljeno niže, povećat će se na 200 ms. (#6470)
* U dijaloški okvir postavki brajice dodan je potvrdni okvir koji omogućuje omogućavanje/onemogućavanje treptanja pokazivača brajice. Ranije se za to koristila vrijednost nula. (#6470)
* Ažurirano eSpeak NG (commit e095f008, 10. siječnja 2017.). (#6717)
* Zbog promjena U ažuriranju za kreatore sustava Windows 10, način "Uvijek se spušta" više nije dostupan u NVDA postavkama prigušivanja zvuka. Još uvijek je dostupan na starijim izdanjima sustava Windows 10. (#6684)
* Zbog promjena u ažuriranju Windows 10 Creators Update, način rada "Duck when outoutput speech and sounds" više ne može osigurati da se zvuk potpuno sagnuo prije nego što počne govoriti, niti će zadržati zvuk dovoljno dugo nakon govora da zaustavi rappid poskakivanje u glasnoći. Te promjene ne utječu na starija izdanja sustava Windows 10. (#6684)

### Ispravci grešaka

* Popravljeno zamrzavanje u programu Microsoft Word pri kretanju po odlomku kroz veliki dokument dok je u načinu pregledavanja. (#6368)
* Tablice u programu Microsoft Word koje su kopirane iz programa Microsoft Excel više se ne prikazuju kao tablice izgleda i stoga se više ne zanemaruju. (#5927)
* Kada pokušavate tipkati u Microsoft Excelu dok ste u zaštićenom prikazu, NVDA sada proizvodi zvuk umjesto da izgovara znakove koji zapravo nisu upisani. (#6570)
* Pritiskom na escape u Microsoft Excelu više se ne prebacuje pogrešno u način pregledavanja, osim ako je korisnik prethodno prešao u način pregledavanja eksplicitno s NVDA+razmak i zatim ušao u način fokusiranja pritiskom na enter u polju obrasca. (#6569)
* NVDA se više ne zamrzava u Microsoft Excel proračunskim tablicama gdje se spaja cijeli redak ili stupac. (#6216)
* Izvješćivanje o izrezanom/preplavljenom tekstu u ćelijama programa Microsoft Excel sada bi trebalo biti točnije. (#6472)
* NVDA sada izvještava kada je potvrdni okvir samo za čitanje. (#6563)
* NVDA pokretač više neće prikazivati dijaloški okvir upozorenja kada ne može reproducirati zvuk logotipa jer nema dostupnog audio uređaja. (#6289)
* Kontrole na vrpci programa Microsoft Excel koje nisu dostupne sada se prijavljuju kao takve. (#6430)
* NVDA više neće najavljivati "okno" prilikom minimiziranja prozora. (#6671)
* Upisani znakovi sada se izgovaraju u aplikacijama Universal Windows Platform (UWP) (uključujući Microsoft Edge) u ažuriranju Windows 10 Creators Update. (#6017)
* Praćenje miša sada radi na svim zaslonima na računalima s više monitora. (#6598)
* NVDA više ne postaje neupotrebljiv nakon izlaska iz Windows Media Playera dok je usredotočen na kontrolu klizača. (#5467)

### Promjene za programere

* Profili i konfiguracijske datoteke sada se automatski nadograđuju kako bi zadovoljili zahtjeve izmjena sheme. Ako dođe do pogreške tijekom nadogradnje, prikazuje se obavijest, konfiguracija se resetira i stara konfiguracijska datoteka dostupna je u NVDA dnevniku na razini 'Info'. (#6470)

## 2016.4

Istaknute značajke ovog izdanja uključuju poboljšanu podršku za Microsoft Edge; način pregledavanja u aplikaciji Windows 10 Mail; i značajna poboljšanja NVDA dijaloga.

### Nove značajke

* NVDA sada može označavati uvlačenje linije pomoću tonova. To se može konfigurirati pomoću kombiniranog okvira "Izvješćivanje o uvlačenju linije" u NVDA dijaloškom okviru postavki formatiranja dokumenta. (#5906)
* Podrška za Orbit Reader 20 Braille Display. (#6007)
* Dodana je opcija za otvaranje prozora preglednika govora pri pokretanju. To se može omogućiti putem potvrdnog okvira u prozoru preglednika govora. (#5050)
* Prilikom ponovnog otvaranja prozora preglednika govora, mjesto i dimenzije sada će se vratiti. (#5050)
* Polja unakrsnih referenci u programu Microsoft Word sada se tretiraju kao hiperveze. Prijavljuju se kao poveznice i mogu se aktivirati. (#6102)
* Podrška za Baum SuperVario2, Baum Vario 340 i HumanWare Brailliant2 brajice. (#6116)
* Početna podrška za ažuriranje Microsoft Edgea za godišnjicu. (#6271)
* Način pregledavanja sada se koristi prilikom čitanja e-pošte u aplikaciji za poštu sustava Windows 10. (#6271)
* Novi jezik: litavski.

### Promjenama

* Ažuriran prevoditelj brajice liblouis na 3.0.0. To uključuje značajna poboljšanja objedinjenog engleskog Brailleovog pisma. (#6109, #4194, #6220, #6140)
* U Upravitelju dodataka, gumbi Onemogući dodatak i Omogući dodatak sada imaju tipkovne prečace (alt+d i alt+e). (#6388)
* Razni problemi s podmetanjem i poravnanjem u NVDA dijaloškim okvirima su riješeni. (#6317, #5548, #6342, #6343, #6349)
* Dijaloški okvir za oblikovanje dokumenta prilagođen je tako da se sadržaj pomiče. (#6348)
* Prilagođen je izgled dijaloškog okvira Izgovor simbola tako da se puna širina dijaloškog okvira koristi za popis simbola. (#6101)
* U načinu pregledavanja u web-preglednicima, jednoslovne navigacijske naredbe polja za uređivanje (e i shift+e) i polja obrasca (f i shift+f) sada se mogu koristiti za premještanje u polja za uređivanje samo za čitanje. (#4164)
* U NVDA postavkama oblikovanja dokumenta, "Najavi promjene formatiranja nakon kursora" preimenovano je u "Prijavi promjene formatiranja nakon kursora", jer utječe na Brailleovo pismo kao i na govor. (#6336)
* Podešen je izgled NVDA "Dijaloga dobrodošlice". (#6350)
* NVDA dijaloški okviri sada imaju gumbe "ok" i "cancel" poravnate desno od dijaloškog okvira. (#6333)
* Kontrole vrtnje sada se koriste za numerička polja za unos kao što je postavka "Postotak promjene visine tona velikim slovom" u dijaloškom okviru Postavke glasa. Možete unijeti željenu vrijednost ili koristiti tipke sa strelicama gore i dolje za podešavanje vrijednosti. (#6099)
* Način na koji se IFrames (dokumenti ugrađeni u dokumente) izvještavaju postao je dosljedniji u svim web preglednicima. IFrame se sada prijavljuju kao "okvir" u Firefoxu. (#6047)

### Ispravci grešaka

* Ispravljena je rijetka pogreška prilikom izlaska iz NVDA dok je preglednik govora otvoren. (#5050)
* Slikovne karte sada se prikazuju prema očekivanjima u načinu pregledavanja u pregledniku Mozilla Firefox. (#6051)
* Dok ste u dijaloškom okviru rječnika, pritiskom na tipku enter sada se spremaju sve promjene koje ste napravili i zatvara se dijaloški okvir. Prije toga, pritiskom na Enter nije bilo ništa. (#6206)
* Poruke se sada prikazuju na Brailleovom pismu prilikom promjene načina unosa za način unosa (izvorni unos/alfanumerički, puni oblik/poluoblikovan itd.). (#5892, #5893)
* Kada onemogućite, a zatim odmah ponovno omogućite dodatak ili obrnuto, status dodatka sada se ispravno vraća na ono što je bio prije. (#6299)
* Kada koristite Microsoft Word, polja s brojevima stranica u zaglavljima sada se mogu čitati. (#6004)
* Miš se sada može koristiti za pomicanje fokusa između popisa simbola i polja za uređivanje u dijaloškom okviru za izgovor simbola. (#6312)
* U načinu pregledavanja u programu Microsoft Word, riješen je problem koji sprječava pojavljivanje popisa elemenata kada dokument sadrži nevažeću hipervezu. (#5886)
* Nakon zatvaranja putem programske trake ili prečaca alt+F4, potvrdni okvir preglednika govora u NVDA izborniku sada će odražavati stvarnu vidljivost prozora. (#6340)
* Naredba za ponovno učitavanje dodataka više ne uzrokuje probleme za pokrenute konfiguracijske profile, nove dokumente u web preglednicima i pregled zaslona. (#2892, #5380)
* Na popisu jezika u NVDA dijaloškom okviru Opće postavke, jezici poput aragonskog sada se ispravno prikazuju u sustavu Windows 10. (#6259)
* Emulirane tipke sistemske tipkovnice (npr. gumb na Brailleovom pismu koji emulira pritiskanje tipke tabulatora) sada su prikazani na konfiguriranom NVDA jeziku u pomoći za unos i dijaloškom okviru Geste unosa. Prije su uvijek bili predstavljeni na engleskom jeziku. (#6212)
* Promjena NVDA jezika (iz dijaloškog okvira Opće postavke) sada nema učinka dok se NVDA ponovno ne pokrene. (#4561)
* Više nije moguće ostaviti polje Uzorak prazno za novi unos u govorni rječnik. (#6412)
* Riješen je rijedak problem prilikom skeniranja serijskih priključaka na nekim sustavima zbog kojeg su neki upravljački programi za Brailleovo pismo bili neupotrebljivi. (#6462)
* U programu Microsoft Word numerirane grafičke oznake u ćelijama tablice sada se čitaju prilikom premještanja po ćeliji. (#6446)
* Sada je moguće dodijeliti geste naredbama za upravljački program za Brailleovo pismo Handy Tech u dijaloškom okviru NVDA Input Gestures. (#6461)
* U programu Microsoft Excel pritiskom na Enter ili numpad prilikom navigacije proračunskom tablicom sada ispravno izvještava o navigaciji do sljedećeg retka. (#6500)
* iTunes se više ne zamrzava povremeno zauvijek kada koristite način pregledavanja za iTunes Store, Apple Music itd. (#6502)
* Ispravljena rušenja u 64-bitnim aplikacijama temeljenim na Mozilli i Chromeu. (#6497)
* U Firefoxu s omogućenim više procesa, način pregledavanja i tekstualna polja koja se mogu uređivati sada ispravno funkcioniraju. (#6380)

### Promjene za programere

* Sada je moguće osigurati module aplikacije za izvršne datoteke koje sadrže točku (.) u nazivu. Točke se zamjenjuju podvlakama (_). (#5323)
* Novi modul gui.guiHelper uključuje uslužne programe za pojednostavljenje izrade wxPython GUI-ja, uključujući automatsko upravljanje razmacima. To olakšava bolji vizualni izgled i dosljednost, kao i olakšavanje stvaranja novih GUI-ja za slijepe programere. (#6287)

## 2016.3

Istaknute značajke ovog izdanja uključuju mogućnost onemogućavanja pojedinačnih dodataka; podrška za polja obrazaca u programu Microsoft Excel; značajna poboljšanja u izvješćivanju o bojama; popravci i poboljšanja vezani uz nekoliko Brailleovih zaslona; te popravci i poboljšanja podrške za Microsoft Word.

### Nove značajke

* Način pregledavanja sada se može koristiti za čitanje PDF dokumenata u pregledniku Microsoft Edge u ažuriranju Windows 10 Anniversary Update. (#5740)
* Precrtani i dvostruki precrtani sada se prijavljuju ako je prikladno u programu Microsoft Word. (#5800)
* U programu Microsoft Word naslov tablice sada se prijavljuje ako je naveden. Ako postoji opis, može mu se pristupiti pomoću naredbe otvorenog dugog opisa (NVDA+d) u načinu pregledavanja. (#5943)
* U Microsoft Wordu, NVDA sada izvještava o položaju prilikom premještanja paragrafa (alt+shift+strelica prema dolje i alt+shift+strelica gore). (#5945)
* U Microsoft Wordu, razmak između redaka sada se prijavljuje putem NVDA naredbe za oblikovanje izvješća, kada ga mijenjate pomoću različitih tipki prečaca Microsoft Word i kada prelazite na tekst s različitim proredima ako je Izvješćivanje o razmaku između redaka uključeno u NVDA postavkama oblikovanja dokumenta. (#2961)
* U pregledniku Internet Explorer sada se prepoznaju strukturni elementi HTML5. (#5591)
* Izvještavanje o komentarima (kao što je u Microsoft Wordu) sada se može onemogućiti putem potvrdnog okvira Prijavi komentare u NVDA dijaloškom okviru postavki formatiranja dokumenta. (#5108)
* Sada je moguće onemogućiti pojedinačne dodatke u Upravitelju dodataka. (#3090)
* Dodane su dodatne dodjele tipki za zaslone za brajicu serije ALVA BC640/680. (#5206)
* Sada postoji naredba za premještanje brajičnog zaslona na trenutni fokus. Trenutno samo ALVA serija BC640/680 ima tipku dodijeljenu ovoj naredbi, ali se po želji može ručno dodijeliti za druge zaslone u dijaloškom okviru Input Gestures. (#5250)
* U programu Microsoft Excel sada možete komunicirati s poljima obrazaca. Na polja obrasca prelazite pomoću popisa elemenata ili navigacije jednim slovom u načinu pregledavanja. (#4953)
* Sada možete dodijeliti gestu unosa za prebacivanje jednostavnog načina pregleda pomoću dijaloškog okvira Geste unosa. (#6173)

### Promjenama

* NVDA sada izvještava o bojama koristeći osnovni dobro shvaćeni skup od 9 nijansi boja i 3 nijanse, s varijacijama svjetline i blijedosti. Ovo je umjesto korištenja subjektivnijih i manje razumljivih naziva boja. (#6029)
* Postojeće ponašanje NVDA+F9, a zatim NVDA+F10 je izmijenjeno tako da odabire tekst pri prvom pritisku na F10. Kada se F10 pritisne dvaput (u brzom slijedu), tekst se kopira u međuspremnik. (#4636)
* Ažuriran eSpeak NG na verziju Master 11b1a7b (22. lipnja 2016.). (#6037)

### Ispravci grešaka

* U načinu pregledavanja u programu Microsoft Word, kopiranje u međuspremnik sada čuva oblikovanje. (#5956)
* U Microsoft Wordu, NVDA sada izvještava na odgovarajući način kada koristi Wordove vlastite naredbe za navigaciju tablicom (alt+home, alt+end, alt+pageUp i alt+pageDown) i naredbe za odabir tablice (shift dodan navigacijskim naredbama). (#5961)
* U dijaloškim okvirima Microsoft Worda, NVDA navigacija objektima je znatno poboljšana. (#6036)
* U nekim aplikacijama, kao što je Visual Studio 2015, tipke prečaca (npr. kontrola+c za kopiranje) sada se prijavljuju prema očekivanjima. (#6021)
* Riješen je rijedak problem prilikom skeniranja serijskih priključaka na nekim sustavima zbog kojeg su neki upravljački programi za Brailleovo pismo bili neupotrebljivi. (#6015)
* Boje izvješćivanja u programu Microsoft Word sada su točnije jer se sada uzimaju u obzir promjene u temama sustava Microsoft Office. (#5997)
* Način pregledavanja za Microsoft Edge i podrška za prijedloge pretraživanja izbornika Start ponovno su dostupni u međuverzijama sustava Windows 10 nakon travnja 2016. (#5955)
* U programu Microsoft Word automatsko čitanje zaglavlja tablice bolje funkcionira kada se radi o spojenim ćelijama. (#5926)
* U aplikaciji Windows 10 Mail NVDA više ne uspijeva čitati sadržaj poruka. (#5635)
* Kada je tipka za izgovaranje naredbi uključena, tipke za zaključavanje kao što je Caps Lock više se ne najavljuju dvaput. (#5490)
* Dijaloški okviri za kontrolu korisničkog računa sustava Windows ponovno se ispravno čitaju u ažuriranju Windows 10 Anniversary (#5942)
* U dodatku za web konferencije (kao što je korišten na out-of-sight.net) NVDA više ne oglašava zvučne signale i ne izgovara ažuriranja trake napretka koja se odnose na ulaz mikrofona. (#5888)
* Izvođenje naredbe Pronađi sljedeće ili Pronađi prethodno u načinu pregledavanja sada će ispravno izvršiti pretraživanje s razlikom od velikih i malih slova ako je izvorni Pronalaženje razlikovalo velika i mala slova. (#5522)
* Prilikom uređivanja unosa u rječniku, sada se daju povratne informacije za nevažeće regularne izraze. NVDA se više ne ruši ako datoteka rječnika sadrži nevažeći regularni izraz. (#4834)
* Ako NVDA ne može komunicirati s Brailleovim pismom (npr. jer je isključen), automatski će onemogućiti korištenje zaslona. (#1555)
* Malo su poboljšane performanse filtriranja na popisu elemenata načina pregledavanja u nekim slučajevima. (#6126)
* U programu Microsoft Excel, nazivi pozadinskih uzoraka koje je prijavio NVDA sada odgovaraju onima koje koristi Excel. (#6092)
* Poboljšana podrška za zaslon za prijavu u sustav Windows 10, uključujući najavu upozorenja i aktiviranje polja za lozinku dodirom. (#6010)
* NVDA sada ispravno prepoznaje sekundarne tipke za usmjeravanje na zaslonima za brajicu serije ALVA BC640/680. (#5206)
* NVDA ponovno može prijaviti Windows Toast obavijesti u nedavnim verzijama sustava Windows 10. (#6096)
* NVDA više ne prestaje povremeno prepoznavati pritiske tipki na Baum kompatibilnim i HumanWare Brailliant B Braille zaslonima. (#6035)
* Ako je prijavljivanje brojeva redaka omogućeno u NVDA postavkama formatiranja dokumenta, brojevi redaka sada se prikazuju na Brailleovom pismu. (#5941)
* Kada je govorni mod isključen, objekti za prijavljivanje (kao što je pritiskanje NVDA+tab za prijavu fokusa) sada se pojavljuju u Pregledniku govora prema očekivanjima. (#6049)
* Na popisu poruka programa Outlook 2016 više se ne prijavljuju povezane skice. (#6219)
* U pregledniku Google Chrome i preglednicima temeljenim na Chromeu na jeziku koji nije engleski, način pregledavanja više ne funkcionira u mnogim dokumentima. (#6249)

### Promjene za programere

* Zapisivanje podataka izravno iz svojstva više ne rezultira rekurzivnim pozivanjem svojstva iznova i iznova. (#6122)

## 2016.2.1

Ovo izdanje popravlja rušenja u programu Microsoft Word:

* NVDA više ne uzrokuje rušenje Microsoft Worda odmah nakon pokretanja u sustavu Windows XP. (#6033)
* Uklonjeno je izvješćivanje o gramatičkim pogreškama jer to uzrokuje rušenje u programu Microsoft Word. (#5954, #5877)

## 2016.2

Istaknute značajke ovog izdanja uključuju mogućnost označavanja pravopisnih pogrešaka tijekom tipkanja; podrška za prijavljivanje gramatičkih pogrešaka u programu Microsoft Word; te poboljšanja i popravci podrške za Microsoft Office.

### Nove značajke

* U načinu pregledavanja u pregledniku Internet Explorer i drugim MSHTML kontrolama, korištenje navigacije prvim slovom za pomicanje napomenom (a i shift+a) sada se premješta na umetnuti i izbrisani tekst. (#5691)
* U Microsoft Excelu, NVDA sada izvještava o razini grupe ćelija, kao i o tome je li sažeta ili proširena. (#5690)
* Dvaput pritiskom na naredbu Oblikovanje teksta izvješća (NVDA+f) prikazuju se informacije u načinu pregledavanja kako bi ih se moglo pregledati. (#4908)
* U programu Microsoft Excel 2010 i novijim verzijama sada se izvješćuje o sjenčanju ćelija i ispuni gradijenta. Automatskim izvještavanjem upravlja opcija Boje izvješća u NVDA postavkama oblikovanja dokumenta. (#3683)
* Nova tablica za prijevod Brailleovog pisma: Koine grčki. (#5393)
* U pregledniku dnevnika sada možete spremiti zapisnik pomoću tipke prečaca control+s. (#4532)
* Ako je prijavljivanje pravopisnih pogrešaka omogućeno i podržano u fokusiranoj kontroli, NVDA će reproducirati zvuk koji će vas upozoriti na pravopisnu pogrešku napravljenu tijekom tipkanja. To se može onemogućiti pomoću nove opcije "Reproduciraj zvuk za pravopisne pogreške tijekom tipkanja" u NVDA dijaloškom okviru Postavke tipkovnice. (#2024)
* Gramatičke pogreške sada se prijavljuju u programu Microsoft Word. To se može onemogućiti pomoću nove opcije "Prijavi gramatičke pogreške" u NVDA dijaloškom okviru postavki oblikovanja dokumenta. (#5877)

### Promjenama

* U načinu pregledavanja i tekstualnim poljima koja se mogu uređivati, NVDA sada tretira numpad Enter isto kao i glavnu tipku za unos. (#5385)
* NVDA je prešao na eSpeak NG sintetizator govora. (#5651)
* U programu Microsoft Excel NVDA više ne zanemaruje zaglavlje stupca za ćeliju kada postoji prazan redak između ćelije i zaglavlja. (#5396)
* U programu Microsoft Excel koordinate se sada najavljuju prije zaglavlja kako bi se uklonila dvosmislenost između zaglavlja i sadržaja. (#5396)

### Ispravci grešaka

* U načinu pregledavanja, kada pokušavate koristiti navigaciju jednim slovom za prelazak na element koji nije podržan za dokument, NVDA izvještava da to nije podržano umjesto da izvještava da nema elementa u tom smjeru. (#5691)
* Prilikom navođenja listova na popisu elemenata u programu Microsoft Excel sada su uključeni listovi koji sadrže samo grafikone. (#5698)
* NVDA više ne izvještava o suvišnim informacijama prilikom prebacivanja prozora u Java aplikaciji s više prozora kao što su IntelliJ ili Android Studio. (#5732)
* U uređivačima temeljenim na Scintilli, kao što je Notepad++, Brailleovo pismo se sada ispravno ažurira prilikom pomicanja kursora pomoću zaslona brajice. (#5678)
* NVDA se više ponekad ne ruši prilikom omogućavanja Brailleovog izlaza. (#4457)
* U programu Microsoft Word uvlačenje odlomka sada se uvijek prijavljuje u mjernoj jedinici koju je odabrao korisnik (npr. centimetri ili inči). (#5804)
* Kada koristite Brailleov zaslon, mnoge NVDA poruke koje su se prije samo izgovarale sada se također brailliraju. (#5557)
* U pristupačnim Java aplikacijama sada se izvještava o razini stavki prikaza stabla. (#5766)
* Ispravljena rušenja u Adobe Flashu u Mozilla Firefoxu u nekim slučajevima. (#5367)
* U preglednikima Google Chrome i Chrome, dokumenti unutar dijaloških okvira ili aplikacija sada se mogu čitati u načinu pregledavanja. (#5818)
* U Google Chromeu i preglednicima koji se temelje na Chromeu, sada možete prisiliti NVDA da se prebaci u način pregledavanja u web dijaloškim okvirima ili aplikacijama. (#5818)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama premještanje fokusa na određene kontrole (konkretno, gdje se koristi aria-activedescendant) više se ne prebacuje pogrešno u način pregledavanja. To se dogodilo, na primjer, prilikom prelaska na prijedloge u adresnim poljima prilikom sastavljanja poruke na Gmailu. (#5676)
* U Microsoft Wordu, NVDA se više ne zamrzava u velikim tablicama kada je omogućeno izvještavanje o zaglavljima redaka/stupaca tablice. (#5878)
* U Microsoft Wordu, NVDA više ne izvještava pogrešno o tekstu s razinom obrisa (ali ne i ugrađenim stilom naslova) kao naslovom. (#5186)
* U načinu pregledavanja u programu Microsoft Word, naredbe Premjesti preko kraja/na početak spremnika (zarez i shift+zarez) sada rade za tablice. (#5883)

### Promjene za programere

* NVDA C++ komponente sada su izgrađene s Microsoft Visual Studio 2015. (#5592)
* Sada možete predstaviti tekstualnu ili HTML poruku korisniku u načinu pregledavanja pomoću ui.browseableMessage. (#4908)
* In the User Guide, when a &lt;!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) --&gt;

## 2016.1

Istaknuti dijelovi ovog izdanja uključuju mogućnost opcionalnog smanjenja glasnoće drugih zvukova; poboljšanja Brailleovog izlaza i podrške za Brailleovo pismo; nekoliko značajnih popravaka podrške za Microsoft Office; i popravke načina pregledavanja u iTunesu.

### Nove značajke

* Nove tablice za prijevod Brailleovog pisma: poljska računalna brajica s 8 točaka, mongolska. (#5537, #5574)
* Možete isključiti pokazivač brajice i promijeniti njegov oblik pomoću novih opcija Prikaži pokazivač i Oblik kursora u dijaloškom okviru Postavke brajice. (#5198)
* NVDA se sada može povezati s HIMS Smart Beetle Brailleovim pismom putem Bluetootha. (#5607)
* NVDA može po želji smanjiti glasnoću drugih zvukova kada je instaliran na Windows 8 i novijim verzijama. To se može konfigurirati pomoću opcije Način prigušivanja zvuka u dijaloškom okviru NVDA sintisajzera ili pritiskom na NVDA+shift+d. (#3830, #5575)
* Podrška za APH Refreshabraille u HID načinu rada i Baum VarioUltra i Pronto! kada je spojen putem USB-a. (#5609)
* Podrška za HumanWare Brailliant BI/B Brailleovo pismo prikazuje se kada je protokol postavljen na OpenBraille. (#5612)

### Promjenama

* Izvješćivanje o naglasku sada je onemogućeno prema zadanim postavkama. (#4920)
* U dijaloškom okviru Popis elemenata u programu Microsoft Excel prečac za formule promijenjen je u alt+are tako da se razlikuje od prečaca za polje Filtar. (#5527)
* Ažuriran prevoditelj brajevog pisma liblouis na 2.6.5. (#5574)
* Riječ "tekst" više se ne prijavljuje prilikom premještanja fokusa ili pregleda kursora na tekstualne objekte. (#5452)

### Ispravci grešaka

* U aplikaciji iTunes 12 način pretraživanja sada se ispravno ažurira kada se nova stranica učita u trgovini iTunes Store. (#5191)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama prelazak na određene razine naslova s navigacijom jednim slovom sada se ponaša kao što se očekuje kada je razina naslova nadjačana u svrhu pristupačnosti (točnije, kada razina arije nadjačava razinu oznake h). (#5434)
* U Spotifyju fokus više ne pada često na "nepoznate" objekte. (#5439)
* Fokus se sada ispravno vraća prilikom povratka na Spotify iz druge aplikacije. (#5439)
* Prilikom prebacivanja između načina pregledavanja i načina fokusiranja, način rada se izvještava na Brailleovom pismu i govoru. (#5239)
* Pokreni stražnjicu na programskoj traci više se ne prijavljuje kao popis i/ili kao odabrano u nekim verzijama sustava Windows. (#5178)
* Poruke kao što je "umetnuto" više se ne prijavljuju prilikom sastavljanja poruka u programu Microsoft Outlook. (#5486)
* Kada se upotrebljava prikaz brajice i odabire se tekst u trenutnom retku (npr. kada u uređivaču teksta pretražujete tekst koji se nalazi u istom retku), prikaz brajice pomiče se prema potrebi. (#5410)
* NVDA više ne izlazi tiho prilikom zatvaranja Windows naredbene konzole s alt+f4 u sustavu Windows 10. (#5343)
* Na popisu elemenata u načinu pregledavanja, kada promijenite vrstu elementa, polje Filtriraj po sada je obrisano. (#5511)
* U tekstu koji se može uređivati u Mozillinim aplikacijama, ponovnim pomicanjem miša čita se odgovarajući redak, riječ itd. kako se očekuje umjesto cijelog sadržaja. (#5535)
* Prilikom pomicanja miša u tekstu koji se može uređivati u Mozillinim aplikacijama, čitanje se više ne zaustavlja na elementima kao što su poveznice unutar riječi ili retka koji se čita. (#2160, #5535)
* U pregledniku Internet Explorer web-mjesto shoprite.com sada se može čitati u načinu pregledavanja umjesto da se prijavljuje kao prazno. (Konkretno, neispravni atributi langa sada se obrađuju graciozno.) (#5569)
* U programu Microsoft Word evidentirane promjene kao što je "umetnute" više se ne prijavljuju kada se ne prikaže oznaka praćenja promjena. (#5566)
* Kada je preklopna tipka fokusirana, NVDA sada izvještava kada je promijenjena iz pritisnute u nepritisnutu. (#5441)
* Izvješćivanje o promjenama oblika miša ponovno funkcionira prema očekivanjima. (#5595)
* Kada izgovarate uvlačenje redaka, razmaci bez loma sada se tretiraju kao normalni razmaci. Ranije je to moglo uzrokovati najave kao što je "svemirski prostor" umjesto "3 prostora". (#5610)
* Prilikom zatvaranja popisa kandidata za modernu Microsoftovu metodu unosa, fokus se ispravno vraća na sastav unosa ili temeljni dokument. (#4145)
* U sustavu Microsoft Office 2013 i novijim verzijama, kada je vrpca postavljena na prikaz samo kartica, stavke na vrpci ponovno se prijavljuju prema očekivanjima kada se kartica aktivira. (#5504)
* Popravci i poboljšanja prepoznavanja i povezivanja gesta na dodirnom zaslonu. (#5652)
* Lebdenja dodirnog zaslona više se ne prijavljuju u pomoći za unos. (#5652)
* NVDA više ne uspijeva navesti komentare na popisu elemenata za Microsoft Excel ako je komentar na spojenoj ćeliji. (#5704)
* U vrlo rijetkim slučajevima, NVDA više ne uspijeva čitati sadržaj lista u Microsoft Excelu s omogućenim izvještavanjem o zaglavljima redaka i stupaca. (#5705)
* U pregledniku Google Chrome navigacija unutar ulazne kompozicije prilikom unosa istočnoazijskih znakova sada funkcionira prema očekivanjima. (#4080)
* Prilikom pretraživanja Apple Musica u iTunesu, način pregledavanja dokumenta s rezultatima pretraživanja sada se ažurira prema očekivanjima. (#5659)
* U programu Microsoft Excel pritiskom na shift+f11 za stvaranje novog lista sada se izvještava o novoj poziciji umjesto da se ništa ne prijavljuje. (#5689)
* Riješeni su problemi s izlazom na Brailleovom pismu prilikom unosa korejskih znakova. (#5640)

### Promjene za programere

* Nova klasa audioDucking.AudioDucker omogućuje kod koji izlazi zvuk kako bi naznačio kada pozadinski zvuk treba sakriti. (#3830)
* nvwave. Konstruktor WavePlayera sada ima argument ključne riječi wantDucking koji određuje treba li se pozadinski zvuk sakriti tijekom reprodukcije zvuka. (#3830)
 * Kada je to omogućeno (što je zadano), bitno je da se WavePlayer.idle pozove kada je to prikladno.
* Poboljšani I/O za Brailleove zaslone: (#5609)
 * Upravljački programi Brailleovog zaslona koji su sigurni za nit mogu se proglasiti takvim pomoću atributa BrailleDisplayDriver.isThreadSafe. Upravljački program mora biti siguran za nit kako bi imao koristi od sljedećih značajki.
 * Podaci se zapisuju na upravljačke programe Brailleovog pisma koji su sigurni za nit u pozadini, čime se poboljšavaju performanse.
 * hwIo.Serial proširuje pyserial da pozove poziv kada se primi podatak umjesto da vozači moraju anketirati.
 * hwIo.Hid pruža podršku za Brailleove zaslone koji komuniciraju putem USB HID-a.
 * hwPortUtils i hwIo po želji mogu pružiti detaljno bilježenje otklanjanja pogrešaka, uključujući pronađene uređaje i sve poslane i primljene podatke.
* Postoji nekoliko novih svojstava dostupnih putem gesta na zaslonu osjetljivom na dodir: (#5652)
 * MultitouchTracker objekti sada sadrže svojstvo childTrackers koje sadrži MultiTouchTrackers od kojeg se sastojao. Na primjer, dvostruki dodir s 2 prsta ima praćenje djece za dva dodira s 2 prsta. Sami dodiri s 2 prsta imaju praćenje djece za dva dodira.
 * Objekti MultiTouchTracker sada sadrže i svojstvo rawSingleTouchTracker ako je tragač rezultat dodira, pomicanja prsta ili lebdenja jednim prstom. SingleTouchTracker omogućuje pristup temeljnom ID-u koji je dodijelio prstu operativni sustav i je li prst još uvijek u kontaktu u trenutnom trenutku.
 * TouchInputGestures sada imaju svojstva x i y, uklanjajući potrebu za pristupom trackeru za trivijalne slučajeve.
 * TouchInputGesturs sada sadrže svojstvo preheldTracker, što je MultitouchTracker objekt koji predstavlja ostale prste koje se drže tijekom izvođenja ove akcije.
* Mogu se emitirati dvije nove geste na zaslonu osjetljivom na dodir: (#5652)
 * Dodir i zadržavanje u množini (npr. dvostruki dodir i držanje)
 * Generalizirani identifikator s uklonjenim brojem prstiju za zadržavanja (npr. držanje+lebdenje za 1finger_hold+lebdeći).

## 2015.4

Istaknute značajke ovog izdanja uključuju poboljšanja performansi u sustavu Windows 10; uključivanje u centar za olakšani pristup u sustavu Windows 8 i novijim verzijama; poboljšanja za Microsoft Excel, uključujući popis i preimenovanje listova te pristup zaključanim ćelijama u zaštićenim listovima; i podrška za uređivanje obogaćenog teksta u Mozilla Firefoxu, Google Chromeu i Mozilla Thunderbirdu.

### Nove značajke

* NVDA se sada pojavljuje u Centru za olakšani pristup u sustavu Windows 8 i novijim verzijama. (#308)
* Prilikom kretanja po ćelijama u Excelu, promjene formatiranja sada se automatski prijavljuju ako su odgovarajuće opcije uključene u NVDA dijaloškom okviru Postavke oblikovanja dokumenta. (#4878)
* Opcija Naglasak izvješća dodana je u NVDA dijaloški okvir Postavke oblikovanja dokumenta. Uključeno prema zadanim postavkama, ova opcija omogućuje NVDA da automatski prijavi postojanje naglašenog teksta u dokumentima. Zasad je to podržano samo za em i jake oznake u načinu pregledavanja za Internet Explorer i druge MSHTML kontrole. (#4920)
* Postojanje umetnutog i obrisanog teksta sada se prijavljuje u načinu pregledavanja za Internet Explorer i druge MSHTML kontrole ako je NVDA opcija Revizije uređivača izvješća omogućena. (#4920)
* Kada pregledavate promjene zapisa na NVDA popisu elemenata za Microsoft Word, sada se prikazuje više informacija kao što su svojstva oblikovanja koja su promijenjena. (#4920)
* Microsoft Excel: popis i preimenovanje listova sada je moguće iz NVDA popisa elemenata (NVDA+f7). (#4630, #4414)
* Sada je moguće konfigurirati šalju li se stvarni simboli sintetizatorima govora (npr. da izazovu pauzu ili promjenu fleksije) u dijaloškom okviru Izgovor simbola. (#5234)
* U Microsoft Excelu, NVDA sada izvještava o svim ulaznim porukama koje je autor lista postavio na ćelije. (#5051)
* Podrška za Baum Pronto! Prikazi brajice V4 i VarioUltra kada su povezani putem Bluetootha. (#3717)
* Podrška za uređivanje obogaćenog teksta u Mozilla aplikacijama kao što su Google dokumenti s omogućenom podrškom za brajicu u Mozilla Firefoxu i HTML kompozicijom u Mozilla Thunderbirdu. (#1668)
* Podrška za uređivanje obogaćenog teksta u Google Chromeu i preglednicima koji se temelje na Chromeu kao što su Google dokumenti s omogućenom podrškom za Brailleovo pismo. (#2634)
 * Za to je potrebna verzija Chromea 47 ili novija.
* U načinu pregledavanja u programu Microsoft Excel možete se kretati do zaključanih ćelija u zaštićenim listovima. (#4952)

### Promjenama

* Opcija Revizije uređivača izvješća u NVDA dijaloškom okviru Postavke oblikovanja dokumenta sada je uključena prema zadanim postavkama. (#4920)
* Kada se pomičete po znakovima u Microsoft Wordu s uključenom NVDA opcijom Revizije uređivača izvješća, sada se prijavljuje manje informacija o promjenama zapisa, što navigaciju čini učinkovitijom. Da biste vidjeli dodatne informacije, upotrijebite popis elemenata. (#4920)
* Ažuriran prevoditelj brajice liblouis na 2.6.4. (#5341)
* Nekoliko simbola (uključujući osnovne matematičke simbole) premješteno je na razinu tako da se prema zadanim postavkama izgovaraju. (#3799)
* Ako sintisajzer to podržava, govor bi sada trebao pauzirati za zagrade i crticu (–). (#3799)
* Prilikom odabira teksta, tekst se prijavljuje prije naznake odabira, a ne poslije. (#1707)

### Ispravci grešaka

* Velika poboljšanja performansi prilikom navigacije popisom poruka programa Outlook 2010/2013. (#5268)
* U grafikonu u programu Microsoft Excel navigacija određenim tipkama (kao što je promjena listova pomoću control+pageUp i control+pageDown) sada ispravno funkcionira. (#5336)
* Popravljen je vizualni izgled gumba u dijaloškom okviru upozorenja koji se prikazuje kada pokušate smanjiti NVDA. (#5325)
* U sustavu Windows 8 i novijim verzijama, NVDA se sada pokreće puno ranije kada je konfiguriran za pokretanje nakon prijave u Windows. (#308)
 * Ako ste to omogućili pomoću prethodne verzije NVDA-a, morat ćete je onemogućiti i ponovno omogućiti kako bi promjena stupila na snagu. Slijedite ovaj postupak:
  1. Otvorite dijaloški okvir Opće postavke.
  1. Poništite potvrdni okvir Automatski pokreni NVDA nakon što se prijavim na Windows.
  1. Pritisnite gumb OK.
  1. Ponovno otvorite dijaloški okvir Opće postavke.
  1. Označite potvrdni okvir Automatski pokreni NVDA nakon što se prijavim na Windows.
  1. Pritisnite gumb OK.
* Poboljšanja performansi za automatizaciju korisničkog sučelja, uključujući File Explorer i Preglednik zadataka. (#5293)
* NVDA se sada ispravno prebacuje u način fokusiranja kada prelazite na ARIA kontrole mreže samo za čitanje u načinu pregledavanja za Mozilla Firefox i druge kontrole temeljene na Gecku. (#5118)
* NVDA sada ispravno izvještava "nema prethodnog" umjesto "nema sljedećeg" kada više nema objekata prilikom pomicanja ulijevo na zaslonu osjetljivom na dodir.
* Riješeni su problemi prilikom upisivanja više riječi u polje filtra u dijaloškom okviru Geste unosa. (#5426)
* NVDA se više ne zamrzava u nekim slučajevima prilikom ponovnog povezivanja sa zaslonom serije HumanWare Brailliant BI/B putem USB-a. (#5406)
* U jezicima s konjunkcijskim znakovima opisi znakova sada funkcioniraju kao što se očekuje za velike engleske znakove. (#5375)
* NVDA se više ne bi trebao povremeno zamrzavati prilikom otvaranja izbornika Start u sustavu Windows 10. (#5417)
* U Skypeu za stolna računala sada se prijavljuju obavijesti koje se prikazuju prije nestanka prethodne obavijesti. (#4841)
* Obavijesti se sada ispravno prijavljuju u Skypeu za stolna računala 7.12 i novijim verzijama. (#5405)
* NVDA sada ispravno izvještava o fokusu prilikom odbacivanja kontekstnog izbornika u nekim aplikacijama kao što je Jart. (#5302)
* U sustavu Windows 7 i novijim verzijama, boja se ponovno prijavljuje u određenim aplikacijama kao što je Wordpad. (#5352)
* Prilikom uređivanja u programu Microsoft PowerPoint, pritiskom na Enter sada se automatski unosi tekst kao što je grafička oznaka ili broj. (#5360)

## 2015.3

Istaknute značajke ovog izdanja uključuju početnu podršku za Windows 10; mogućnost onemogućavanja navigacije jednim slovom u načinu pregledavanja (korisno za neke web aplikacije); poboljšanja u pregledniku Internet Explorer; i popravci iskrivljenog teksta prilikom tipkanja u određenim aplikacijama s omogućenom brajicom.

### Nove značajke

* Postojanje pravopisnih pogrešaka najavljuje se u poljima koja se mogu uređivati za Internet Explorer i druge MSHTML kontrole. (#4174)
* Sada se izgovara mnogo više Unicode matematičkih simbola kada se pojave u tekstu. (#3805)
* Prijedlozi za pretraživanje na početnom zaslonu sustava Windows 10 automatski se prijavljuju. (#5049)
* Podrška za zaslone za brajice EcoBraille 20, EcoBraille 40, EcoBraille 80 i EcoBraille Plus. (#4078)
* U načinu pregledavanja sada možete uključiti i isključiti navigaciju jednim slovom pritiskom na NVDA+shift+razmak. Kada su isključeni, jednoslovni ključevi prosljeđuju se aplikaciji, što je korisno za neke web aplikacije kao što su Gmail, Twitter i Facebook. (#3203)
* Nove tablice za prijevod Brailleovog pisma: finski 6 točaka, irski razred 1, irski razred 2, korejski razred 1 (2006), korejski razred 2 (2006). (#5137, #5074, #5097)
* Sada je podržana QWERTY tipkovnica na Brajičnom pismu Papenmeier BRAILLEX Live Plus. (#5181)
* Eksperimentalna podrška za web-preglednik Microsoft Edge i mehanizam za pregledavanje u sustavu Windows 10. (#5212)
* Novi jezik: Kannada.

### Promjenama

* Ažuriran prevoditelj brajevog pisma na 2.6.3. (#5137)
* Kada pokušavate instalirati stariju verziju NVDA od trenutno instalirane, sada ćete biti upozoreni da se to ne preporučuje i da NVDA treba potpuno deinstalirati prije nego što nastavite. (#5037)

### Ispravci grešaka

* U načinu pregledavanja za Internet Explorer i druge MSHTML kontrole brza navigacija po polju obrasca više ne uključuje pogrešno stavke prezentacijskog popisa. (#4204)
* U Firefoxu, NVDA više ne prijavljuje neprimjereno sadržaj ARIA kartice kada se fokus pomakne unutar nje. (#4638)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama tabulatorom u odjeljke, članke ili dijaloške okvire više se ne prijavljuje neprimjereno sav sadržaj u spremniku. (#5021, #5025)
* Kada koristite Baum/HumanWare/APH brajeve zaslone s brajičnom tipkovnicom, unos brajice više ne prestaje funkcionirati nakon pritiska na drugu vrstu tipke na zaslonu. (#3541)
* U sustavu Windows 10 suvišne informacije više se ne prijavljuju kada pritisnete alt+tab ili alt+shift+tab za prebacivanje između aplikacija. (#5116)
* Upisani tekst više se ne iskrivljuje kada koristite određene aplikacije kao što je Microsoft Outlook sa zaslonom brajice. (#2953)
* U načinu pregledavanja u pregledniku Internet Explorer i drugim MSHTML kontrolama sada se prijavljuje ispravan sadržaj kada se element pojavi ili promijeni i odmah se fokusira. (#5040)
* U načinu pregledavanja u programu Microsoft Word, navigacija jednim slovom sada ažurira Brailleov prikaz i kursor za pregled prema očekivanjima. (#4968)
* Na Brailleovom pismu suvišni razmaci više se ne prikazuju između ili poslije indikatora za kontrole i oblikovanje. (#5043)
* Kada aplikacija sporo reagira i vi se prebacite s te aplikacije, NVDA sada u većini slučajeva puno bolje reagira u drugim aplikacijama. (#3831)
* Windows 10 Toast obavijesti sada se prijavljuju prema očekivanjima. (#5136)
* Vrijednost se sada izvještava kako se mijenja u određenim kombiniranim okvirima (automatizacija korisničkog sučelja) u kojima to prije nije funkcioniralo.
* U načinu pregledavanja u web-preglednicima, tabulatori se sada ponašaju prema očekivanjima nakon ulaganja tabulatora u dokument okvira. (#5227)
* Zaključani zaslon sustava Windows 10 sada se može odbaciti pomoću zaslona osjetljivog na dodir. (#5220)
* U sustavu Windows 7 i novijim verzijama tekst se više ne iskrivljuje prilikom upisivanja u određenim aplikacijama kao što su Wordpad i Skype sa zaslonom za brajicu. (#4291)
* Na zaključanom zaslonu sustava Windows 10 više nije moguće čitati međuspremnik, pristupati pokrenutim aplikacijama pomoću kursora za pregled, mijenjati NVDA konfiguraciju itd. (#5269)

### Promjene za programere

* Sada možete ubaciti neobrađeni unos sa sistemske tipkovnice kojom Windows ne upravlja izvorno (npr. QWERTY tipkovnica na Brailleovom pismu) pomoću nove funkcije keyboardHandler.injectRawKeyboardInput. (#4576)
* eventHandler.requestEvents dodan je za zahtjev za određene događaje koji su blokirani prema zadanim postavkama; npr. prikazati događaje iz određene kontrole ili određene događaje čak i kada su u pozadini. (#3831)
* Umjesto jednog atributa i18nName, synthDriverHandler.SynthSetting sada ima odvojene atribute displayNameWithAccelerator i displayName kako bi se izbjeglo izvještavanje o akceleratoru u prstenu postavki sintisajzera na nekim jezicima.
 * Za kompatibilnost s prethodnim verzijama, u konstruktoru, displayName nije obavezan i bit će izveden iz displayNameWithAccelerator ako nije naveden. Međutim, ako namjeravate imati akcelerator za postavku, treba osigurati oboje.
 * Atribut i18nName je zastario i može se ukloniti u budućem izdanju.

## 2015.2

Istaknute značajke ovog izdanja uključuju mogućnost čitanja grafikona u programu Microsoft Excel i podršku za čitanje i interaktivnu navigaciju matematičkim sadržajem.

### Nove značajke

* Pomicanje naprijed i natrag po rečenicama u Microsoft Wordu i Outlooku sada je moguće uz alt+downArrow i alt+upArrow. (#3288)
* Nove tablice za prijevod Brailleovog pisma za nekoliko indijskih jezika. (#4778)
* U Microsoft Excelu NVDA sada izvještava kada ćelija ima prepun ili izrezan sadržaj. (#3040)
* U programu Microsoft Excel sada možete koristiti popis elemenata (NVDA+f7) kako biste omogućili popis grafikona, komentara i formula. (#1987)
* Podrška za čitanje grafikona u programu Microsoft Excel. Da biste to koristili, odaberite grafikon pomoću popisa elemenata (NVDA+f7), a zatim koristite tipke sa strelicama za pomicanje između podatkovnih točaka. (#1987)
* Koristeći MathPlayer 4 iz Design Sciencea, NVDA sada može čitati i interaktivno navigirati matematičkim sadržajem u web preglednicima te u Microsoft Wordu i PowerPointu. Za detalje pogledajte odjeljak "Čitanje matematičkog sadržaja" u Korisničkom priručniku. (#4673)
* Sada je moguće dodijeliti geste unosa (tipkovničke naredbe, dodirne geste, itd.) za sve dijaloške okvire NVDA postavki i opcije oblikovanja dokumenta pomoću dijaloškog okvira Ulazne geste. (#4898)

### Promjenama

* U NVDA dijaloškom okviru Oblikovanje dokumenta, promijenjeni su tipkovni prečaci za popise izvješća, veze na izvješća, brojeve redaka izvješća i naziv fonta izvješća. (#4650)
* U NVDA dijaloškom okviru Postavke miša, dodani su tipkovnički prečaci za reprodukciju audio koordinata kada se miš pomiče, a svjetlina kontrolira glasnoću audio koordinata. (#4916)
* Značajno poboljšano izvještavanje o nazivima boja. (#4984)
* Ažuriran prevoditelj brajice liblouis na 2.6.2. (#4777)

### Ispravci grešaka

* Opisi znakova sada se ispravno obrađuju za konjunkcijske znakove u određenim indijskim jezicima. (#4582)
* Ako je omogućena opcija "Vjeruj jeziku glasa prilikom obrade znakova i simbola", dijaloški okvir Interpunkcija/izgovor simbola sada ispravno koristi jezik glasa. Također, jezik za koji se izgovor uređuje prikazan je u naslovu dijaloškog okvira. (#4930)
* U Internet Exploreru i drugim MSHTML kontrolama upisani znakovi više se ne objavljuju neprimjereno u kombiniranim okvirima koji se mogu uređivati, kao što je polje za Google pretraživanje na Googleovoj početnoj stranici. (#4976)
* Prilikom odabira boja u aplikacijama sustava Microsoft Office sada se prijavljuju nazivi boja. (#3045)
* Danski Brailleov izlaz sada ponovno funkcionira. (#4986)
* PageUp/pageDown ponovno se može koristiti za promjenu slajdova unutar dijaprojekcije programa PowerPoint. (#4850)
* U Skypeu za stolna računala 7.2 i novijim verzijama sada se prijavljuju obavijesti o tipkanju i riješeni su problemi odmah nakon premještanja fokusa iz razgovora. (#4972)
* Riješeni su problemi prilikom upisivanja određenih interpunkcijskih znakova/simbola kao što su zagrade u polje filtra u dijaloškom okviru Geste unosa. (#5060)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama pritiskom na g ili shift+g za navigaciju do grafike sada se nalaze elementi označeni kao slike u svrhu pristupačnosti (npr. ARIA uloga img). (#5062)

### Promjene za programere

* brailleInput.handler.sendChars(mychar) više neće filtrirati znak ako je jednak prethodnom znaku tako što će osigurati da je poslani ključ ispravno otpušten. (#4139)
* Skripte za promjenu načina dodira sada će poštovati nove oznake dodane u touchHandler.touchModeLabels. (#4699)
* Dodaci mogu pružiti vlastite implementacije matematičke prezentacije. Za detalje pogledajte mathPres paket. (#4509)
* Implementirane su govorne naredbe za umetanje pauze između riječi i promjenu visine, glasnoće i brzine. Pogledajte BreakCommand, PitchCommand, VolumeCommand i RateCommand u govornom modulu. (#4674)
 * Tu je i govor. PhonemeNaredba za umetanje određenog izgovora, ali trenutne implementacije podržavaju samo vrlo ograničen broj fonema.

## 2015.1

Istaknute značajke ovog izdanja uključuju način pregledavanja dokumenata u programima Microsoft Word i Outlook; velika poboljšanja podrške za Skype za stolna računala; i značajne popravke za Microsoft Internet Explorer.

### Nove značajke

* Sada možete dodati nove simbole u dijaloškom okviru Izgovor simbola. (#4354)
* U dijaloškom okviru Ulazne geste možete koristiti novo polje "Filtriraj prema" za prikaz samo gesta koje sadrže određene riječi. (#4458)
* NVDA sada automatski izvještava o novom tekstu u mintty. (#4588)
* U dijaloškom okviru Pronađi način pregledavanja sada postoji mogućnost pretraživanja osjetljivog na velika i mala slova. (#4584)
* Brza navigacija (pritiskom na h za pomicanje po naslovu itd.) i Popis elemenata (NVDA+f7) sada su dostupni u Microsoft Word dokumentima uključivanjem načina pregledavanja s NVDA+razmak. (#2975)
* Čitanje HTML poruka u programu Microsoft Outlook 2007 i novijim verzijama znatno je poboljšano jer je način pregledavanja automatski omogućen za te poruke. Ako način pregledavanja nije omogućen u nekim rijetkim situacijama, možete ga prisilno uključiti pomoću NVDA+razmaka. (#2975)
* Zaglavlja stupaca tablice u Microsoft Wordu automatski se prijavljuju za tablice u kojima je autor izričito odredio redak zaglavlja putem svojstava tablice Microsoft Worda. (#4510)
 * Međutim, za tablice u kojima su spojeni reci to neće funkcionirati automatski. U tom slučaju i dalje možete ručno postaviti zaglavlja stupaca u NVDA uređaju s NVDA+shift+c.
* U Skypeu za stolna računala sada se prijavljuju obavijesti. (#4741)
* U Skypeu za stolna računala sada možete prijaviti i pregledati nedavne poruke koristeći NVDA+control+1 do NVDA+control+0; npr. NVDA+control+1 za najnoviju poruku i NVDA+control+0 za desetu najnoviju. (#3210)
* U razgovoru u Skypeu za stolna računala, NVDA sada izvještava kada kontakt tipka. (#3506)
* NVDA se sada može tiho instalirati putem naredbenog retka bez pokretanja instalirane kopije nakon instalacije. Da biste to učinili, upotrijebite opciju --install-silent. (#4206)
* Podrška za brajice Papenmeier BRAILLEX Live 20, BRAILLEX Live i BRAILLEX Live Plus. (#4614)

### Promjenama

* U NVDA dijaloškom okviru postavki oblikovanja dokumenta, opcija za prijavu pravopisnih pogrešaka sada ima tipku prečaca (alt+r). (#793)
* NVDA će sada koristiti jezik sintisajzera/glasa za obradu znakova i simbola (uključujući nazive interpunkcijskih znakova/simbola), bez obzira na to je li uključena automatska promjena jezika. Da biste isključili ovu značajku kako bi NVDA ponovno koristio jezik sučelja, poništite novu opciju u postavkama Glasa pod nazivom Vjeruj jeziku Glasa prilikom obrade znakova i simbola. (#4210)
* Podrška za Newfon sintisajzer je uklonjena. Newfon je sada dostupan kao NVDA dodatak. (#3184)
* Skype za stolna računala 7 ili noviji sada je potreban za korištenje s NVDA; Starije verzije nisu podržane. (#4218)
* Preuzimanje NVDA ažuriranja sada je sigurnije. (Točnije, podaci o ažuriranju dohvaćaju se putem https-a, a hash datoteke provjerava se nakon preuzimanja.) (#4716)
* eSpeak je nadograđen na verziju 1.48.04 (#4325)

### Ispravci grešaka

* U programu Microsoft Excel spojene ćelije zaglavlja retka i stupca sada se ispravno obrađuju. Na primjer, ako su A1 i B1 spojeni, tada će B2 sada imati A1 i B1 prijavljene kao zaglavlje stupca, a ne ništa. (#4617)
* Prilikom uređivanja sadržaja tekstualnog okvira u programu Microsoft PowerPoint 2003, NVDA će ispravno izvijestiti o sadržaju svakog retka. Prije toga, u svakom odlomku, retci bi sve više bili pomaknuti za jedan znak. (#4619)
* Svi NVDA dijalozi sada su usredotočeni na zaslon, poboljšavajući vizualnu prezentaciju i upotrebljivost. (#3148)
* U Skypeu za stolna računala, prilikom unosa uvodne poruke za dodavanje kontakta, unos i pomicanje teksta sada ispravno funkcionira. (#3661)
* Kada se fokus premjesti na novu stavku u prikazima stabla u Eclipse IDE-u, ako je prethodno fokusirana stavka potvrdni okvir, više se ne objavljuje pogrešno. (#4586)
* U dijaloškom okviru za provjeru pravopisa programa Microsoft Word, sljedeća će se pogreška automatski prijaviti kada je posljednja promijenjena ili zanemarena pomoću odgovarajućih tipki prečaca. (#1938)
* Tekst se opet može ispravno pročitati na mjestima kao što su prozor terminala Tera Term Pro i dokumenti u Balabolki. (#4229)
* Fokus se sada ispravno vraća na dokument koji se uređuje Kada dovršavate sastavljanje teksta na korejskom i drugim istočnoazijskim jezicima tijekom uređivanja unutar okvira u pregledniku Internet Explorer i drugim MSHTML dokumentima. (#4045)
* U dijaloškom okviru Ulazne geste, prilikom odabira rasporeda tipkovnice za dodanu tipkovnicu, pritiskom na escape sada se zatvara izbornik prema očekivanjima umjesto zatvaranja dijaloškog okvira. (#3617)
* Prilikom uklanjanja dodatka, direktorij dodataka sada se ispravno briše nakon ponovnog pokretanja NVDA-e. Prije ste morali ponovno pokrenuti dva puta. (#3461)
* Riješeni su glavni problemi pri korištenju Skypea za stolna računala 7. (#4218)
* Kada pošaljete poruku u Skypeu za stolna računala, ona se više ne čita dvaput. (#3616)
* U Skypeu za stolna računala, NVDA više ne bi trebao povremeno lažno čitati veliku poplavu poruka (možda čak i cijeli razgovor). (#4644)
* riješen je problem zbog kojeg NVDA-ina naredba za prijavu datuma/vremena nije poštovala regionalne postavke koje je odredio korisnik u nekim slučajevima. (#2987)
* U načinu pregledavanja besmisleni tekst (ponekad se proteže nekoliko redaka) više se ne prikazuje za određene grafike kao što su one koje se nalaze u Google grupama. (Konkretno, to se dogodilo sa slikama kodiranim base64.) (#4793)
* NVDA se više ne bi trebao zamrzavati nakon nekoliko sekundi kada se fokus odmakne od aplikacije iz Windows trgovine jer se obustavlja. (#4572)
* Atribut aria-atom na živim područjima u Mozilla Firefoxu sada se poštuje čak i kada se sam atomski element promijeni. Prije je to utjecalo samo na elemente potomaka. (#4794)
* Način pregledavanja odražavat će ažuriranja i najavit će se živa područja za dokumente načina pregledavanja unutar ARIA aplikacija ugrađenih u dokument u pregledniku Internet Explorer ili drugim MSHTML kontrolama. (#4798)
* Kada se tekst promijeni ili doda u aktivnim područjima u pregledniku Internet Explorer i drugim MSHTML kontrolama gdje je autor naveo da je tekst relevantan, najavljuje se samo promijenjeni ili dodani tekst, a ne sav tekst u elementu koji sadrži. (#4800)
* Sadržaj označen atributom aria-labelledby na elementima u pregledniku Internet Explorer i drugim MSHTML kontrolama ispravno zamjenjuje izvorni sadržaj tamo gdje je to prikladno. (#4575)
* Prilikom provjere pravopisa u programu Microsoft Outlook 2013 sada se objavljuje pogrešno napisana riječ. (#4848)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama sadržaj unutar elemenata skrivenih pomoću visibility:hidden više nije neprikladno prikazan u načinu pregledavanja. (#4839, #3776)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama atribut title na kontrolama obrasca više ne ima neprikladnu prednost u odnosu na druge asocijacije oznaka. (#4491)
* U Internet Exploreru i drugim MSHTML kontrolama, NVDA više ne zanemaruje fokusiranje elemenata zbog atributa aria-activedescendant. (#4667)

### Promjene za programere

* Ažuriran wxPython na 3.0.2.0. (#3763)
* Ažuriran Python na 2.7.9. (#4715)
* NVDA se više ne ruši prilikom ponovnog pokretanja nakon uklanjanja ili ažuriranja dodatka koji uvozi speechDictHandler u svoj modul installTasks. (#4496)

## 2014.4

### Nove značajke

* Novi jezici: kolumbijski španjolski, pandžapski.
* Sada je moguće ponovno pokrenuti NVDA ili ponovno pokrenuti NVDA s deaktiviranim dodacima iz izlaznog dijaloškog okvira NVDA-e. (#4057)
 * NVDA se također može pokrenuti s onemogućenim dodacima pomoću opcije naredbenog retka --disable-addons.
* U govornim rječnicima sada je moguće odrediti da se uzorak treba podudarati samo ako se radi o cijeloj riječi; tj. ne pojavljuje se kao dio veće riječi. (#1704)

### Promjenama

* Ako se objekt na koji ste se premjestili pomoću navigacije objektom nalazi unutar dokumenta načina pregledavanja, ali objekt na kojem ste prethodno bili nije, način pregleda automatski se postavlja na dokument. Prije se to događalo samo ako je objekt navigatora pomaknut zbog promjene fokusa. (#4369)
* Popisi Brailleovog pisma i sintisajzera u odgovarajućim dijaloškim okvirima postavki sada su abecednim redom poredani osim Bez brajice/Bez govora, koji su sada na dnu. (#2724)
* Ažuriran prevoditelj brajevog pisma liblouis na 2.6.0. (#4434, #3835)
* U načinu pregledavanja, pritiskom na e i shift+e za navigaciju do polja za uređivanje sada se nalaze kombinirani okviri koji se mogu uređivati. To uključuje okvir za pretraživanje u najnovijoj verziji Google pretraživanja. (#4436)
* Klikom na ikonu NVDA u području obavijesti lijevom tipkom miša sada se otvara NVDA izbornik umjesto da ne radite ništa. (#4459)

### Ispravci grešaka

* Prilikom premještanja fokusa natrag na dokument načina pregledavanja (npr. alt+tabulator na već otvorenu web-stranicu), pokazivač pregleda ispravno je postavljen na virtualni kursor, a ne na fokusiranu kontrolu (npr. obližnja veza). (#4369)
* U dijaprojekcijama programa PowerPoint pokazivač pregleda ispravno slijedi virtualni kursor. (#4370)
* U Mozilla Firefoxu i drugim preglednicima koji se temelje na Gecku, novi sadržaj unutar žive regije bit će najavljen čak i ako novi sadržaj ima upotrebljivu ARIA live vrstu različitu od nadređene žive regije; npr. kada se sadržaj označen kao asertivan doda u živu regiju označenu kao pristojna. (#4169)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama neki slučajevi u kojima je dokument sadržan u drugom dokumentu više ne sprječavaju korisnika da pristupi nekom sadržaju (točnije, skupovima okvira unutar skupova okvira). (#4418)
* NVDA se u nekim slučajevima više ne ruši prilikom pokušaja korištenja zaslona za brajicu Handy Tech. (#3709)
* U sustavu Windows Vista, lažni dijaloški okvir "Ulazna točka nije pronađena" više se ne prikazuje u nekoliko slučajeva, kao što je pokretanje NVDA iz prečaca na radnoj površini ili putem tipke prečaca. (#4235)
* Ozbiljni problemi s kontrolama teksta koje se mogu uređivati u dijalozima u novijim verzijama Eclipsea su riješeni. (#3872)
* U programu Outlook 2010 premještanje kursora sada funkcionira prema očekivanjima u polju mjesta obveza i zahtjeva za sastanak. (#4126)
* Unutar živog područja, sadržaj koji je označen kao neaktivan (npr. aria-live="off") sada se ispravno zanemaruje. (#4405)
* Prilikom prijavljivanja teksta statusne trake koja ima naziv, naziv je sada ispravno odvojen od prve riječi teksta statusne trake. (#4430)
* U poljima za unos lozinke s omogućenim govorom o upisanim riječima, više zvjezdica više se ne prijavljuje besmisleno kada započinju nove riječi. (#4402)
* Na popisu poruka programa Microsoft Outlook stavke se više ne objavljuju besmisleno kao podatkovne stavke. (#4439)
* Prilikom odabira teksta u kontroli za uređivanje koda u Eclipse IDE-u, cijeli odabir više se ne najavljuje svaki put kada se odabir promijeni. (#2314)
* Različite verzije Eclipsea, kao što su Spring Tool Suite i verzija uključena u paket Android Developer Tools, sada su prepoznate kao Eclipse i s njima se postupa na odgovarajući način. (#4360, #4454)
* Praćenje miša i istraživanje dodirom u pregledniku Internet Explorer i drugim MSHTML kontrolama (uključujući mnoge aplikacije sustava Windows 8) sada su mnogo precizniji na zaslonima s visokim razlučivošću ili kada se promijeni zumiranje dokumenta. (#3494)
* Praćenje miša i istraživanje dodira u pregledniku Internet Explorer i drugim MSHTML kontrolama sada će najaviti oznaku više gumba. (#4173)
* Kada koristite Papenmeier BRAILLEX brajičin zaslon s BrxComom, tipke na zaslonu sada rade prema očekivanjima. (#4614)

### Promjene za programere

* Za izvršne datoteke koje hostiraju mnogo različitih aplikacija (npr. javaw.exe), sada se može pružiti kod za učitavanje određenih modula aplikacije za svaku aplikaciju umjesto učitavanja istog modula aplikacije za sve hostirane aplikacije. (#4360)
 * Pojedinosti potražite u dokumentaciji koda za appModuleHandler.AppModule.
 * Implementirana je podrška za javaw.exe.

## 2014.3

### Nove značajke

* Zvukovi koji se reproduciraju prilikom pokretanja i izlaska NVDA mogu se onemogućiti putem nove opcije u dijaloškom okviru Opće postavke. (#834)
* Pomoći za dodatke može se pristupiti iz Upravitelja dodataka za dodatke koji to podržavaju. (#2694)
* Podrška za kalendar u programu Microsoft Outlook 2007 i novijim verzijama (#2943), uključujući:
 * Najava trenutnog vremena pri kretanju pomoću tipki sa strelicama.
 * Naznaka je li odabrano vrijeme unutar bilo kojeg termina.
 * Najava odabrane obveze pritiskom na karticu.
 * Pametno filtriranje datuma tako da se datum najavljuje samo ako je novo odabrano vrijeme ili sastanak na drugi dan od prethodnog.
* Poboljšana podrška za ulaznu poštu i druge popise poruka u programu Microsoft Outlook 2010 i novijim verzijama (#3834), uključujući:
 * Mogućnost utišavanja zaglavlja stupaca (od, predmet itd.) isključivanjem mogućnosti zaglavlja redaka i stupaca tablice izvješća u postavkama oblikovanja dokumenta.
 * Mogućnost korištenja naredbi za navigaciju tablicom (kontrola + alt + strelice) za kretanje kroz pojedinačne stupce.
* Microsoft word: Ako umetnuta slika nema postavljen alternativni tekst, NVDA će umjesto toga prijaviti naslov slike ako ga je autor naveo. (#4193)
* Microsoft Word: NVDA sada može prijaviti uvlačenje odlomaka pomoću naredbe za oblikovanje izvješća (NVDA+f). Također se može automatski prijaviti kada je nova mogućnost uvlačenja odlomka izvješća omogućena u postavkama oblikovanja dokumenta. (#4165)
* Prijavite automatski umetnuti tekst, kao što je nova grafička oznaka, broj ili uvlaka tabulatora pritiskom na Enter u dokumentima i tekstnim poljima koja se mogu uređivati. (#4185)
* Microsoft word: Pritiskom na NVDA+alt+c prijavit će se tekst komentara ako je pokazivač unutar njega. (#3528)
* Poboljšana podrška za automatsko čitanje zaglavlja stupaca i redaka u programu Microsoft Excel (#3568), uključujući:
 * Podrška za Excel definirane raspone naziva za identifikaciju ćelija zaglavlja (kompatibilno s čitačem zaslona Jaws).
 * Naredbe postavi zaglavlje stupca (NVDA+shift+c) i postavi zaglavlje retka (NVDA+shift+r) sada pohranjuju postavke na radnom listu tako da budu dostupne prilikom sljedećeg otvaranja lista, a bit će dostupne i drugim čitačima zaslona koji podržavaju definiranu shemu raspona naziva.
 * Ove se naredbe sada mogu koristiti i više puta po listu za postavljanje različitih zaglavlja za različite regije.
* Podrška za automatsko čitanje zaglavlja stupaca i redaka u programu Microsoft Word (#3110), uključujući:
 * Podrška za Microsoft Word oznake za prepoznavanje ćelija zaglavlja (kompatibilno s čitačem zaslona Jaws).
 - naredbe za postavljanje zaglavlja stupca (NVDA+shift+c) i postavljanje zaglavlja retka (NVDA+shift+r) dok se nalazi u prvoj ćeliji zaglavlja u tablici omogućuju vam da obavijestite NVDA da se ta zaglavlja trebaju automatski prijaviti.  Postavke se pohranjuju u dokument tako da su dostupne prilikom sljedećeg otvaranja dokumenta, a bit će dostupne i drugim čitačima zaslona koji podržavaju shemu knjižnih oznaka.
* Microsoft Word: Prijavite udaljenost od lijevog ruba stranice kada se pritisne tipka Tab. (#1353)
* Microsoft Word: pružite povratne informacije u govoru i brajici za većinu dostupnih tipki prečaca za oblikovanje (podebljano, kurziv, podcrtano, poravnanje, razina strukture, eksponent, indeks i veličina fonta). (#1353)
* Microsoft Excel: Ako odabrana ćelija sadrži komentare, oni se sada mogu prijaviti pritiskom na NVDA+alt+c. (#2920)
* Microsoft Excel: Omogućite dijaloški okvir specifičan za NVDA za uređivanje komentara na trenutno odabranoj ćeliji kada pritisnete Excelovu naredbu shift+f2 za ulazak u način uređivanja komentara. (#2920)
* Microsoft Excel: povratne informacije o govoru i Brailleovom pismu za mnoge druge prečace kretanja odabira (#4211), uključujući:
 * Okomito pomicanje stranice (pageUp i pageDown);
 * Vodoravno pomicanje stranice (alt+pageUp i alt+pageDown);
 * Proširite odabir (gornje tipke s dodanim Shiftom); i
 * Odabir trenutačne regije (control+shift+8).
* Microsoft Excel: Okomito i vodoravno poravnanje ćelija sada se može prijaviti pomoću naredbe za oblikovanje izvješća (NVDA+f). Također se može automatski prijaviti ako je omogućena mogućnost poravnanja izvješća u postavkama oblikovanja dokumenta. (#4212)
* Microsoft Excel: Stil ćelije sada se može prijaviti pomoću naredbe za oblikovanje izvješća (NVDA+f). Također se može automatski prijaviti ako je omogućena mogućnost Stil izvješća u postavkama oblikovanja dokumenta. (#4213)
* Microsoft PowerPoint: prilikom premještanja oblika po slajdu pomoću tipki sa strelicama sada se prijavljuje trenutna lokacija oblika (#4214), uključujući:
 * Prikazuje se udaljenost između oblika i svakog od rubova klizača.
 * Ako oblik prekriva ili je prekriven drugim oblikom, tada se izvještava o preklapajućoj udaljenosti i preklapajućem obliku.
 * Da biste prijavili ove informacije u bilo kojem trenutku bez pomicanja oblika, pritisnite naredbu Prijavi lokaciju (NVDA+brisanje).
 * Prilikom odabira oblika, ako je prekriven drugim oblikom, NVDA će prijaviti da je zaklonjen.
* Naredba za lokaciju izvješća (NVDA+delete) u nekim je situacijama više specifična za kontekst. (#4219)
 * U standardnim poljima za uređivanje i načinu pregledavanja izvještava se o položaju pokazivača kao postotak kroz sadržaj i njegove koordinate zaslona.
 * Na oblicima u prezentacijama programa PowerPoint izvješćuje se o položaju oblika u odnosu na slajd i druge oblike.
 * Dvaput pritiskom na ovu naredbu proizvest će se prethodno ponašanje izvješćivanja o informacijama o lokaciji za cijelu kontrolu.
* Novi jezik: katalonski.

### Promjenama

* Ažuriran prevoditelj brajevog pisma na 2.5.4. (#4103)

### Ispravci grešaka

* U Google Chromeu i preglednicima koji se temelje na Chromeu određeni dijelovi teksta (kao što su oni s naglaskom) više se ne ponavljaju prilikom prijavljivanja teksta upozorenja ili dijaloškog okvira. (#4066)
* U načinu pregledavanja u Mozillinim aplikacijama, pritiskom na enter na gumbu itd. više se ne uspijeva aktivirati (ili aktivira pogrešna kontrola) u određenim slučajevima kao što su gumbi na vrhu Facebooka. (#4106)
* Beskorisne informacije više se ne objavljuju prilikom kartica u iTunesu. (#4128)
* Na određenim popisima u iTunesu, kao što je popis Glazba, prelazak na sljedeću stavku pomoću navigacije objektima sada ispravno funkcionira. (#4129)
* HTML elementi koji se smatraju naslovima zbog oznake WAI ARIA sada su uključeni u popis elemenata načina pregledavanja i brzu navigaciju za dokumente preglednika Internet Explorer. (#4140)
* Praćenje veza na istoj stranici u novijim verzijama preglednika Internet Explorer sada se ispravno premješta na odredišni položaj i izvještava o njemu u dokumentima načina pregledavanja. (#4134)
* Microsoft Outlook 2010 i novije verzije: Poboljšan je ukupni pristup sigurnim dijaloškim okvirima kao što su Novi profili i dijaloški okviri za postavljanje pošte. (#4090, #4091, #4095)
* Microsoft Outlook: Beskorisna opširnost smanjena je u naredbenim alatnim trakama prilikom navigacije kroz određene dijaloške okvire. (#4096, #3407)
* Microsoft Word: Prelazak tabulatora u praznu ćeliju u tablici više ne označava pogrešno izlazak iz tablice. (#4151)
* Microsoft Word: prvi znak iza kraja tablice (uključujući novi prazan redak) više se ne smatra pogrešno unutar tablice. (#4152)
* Dijaloški okvir za provjeru pravopisa programa Microsoft Word 2010: Prijavljuje se stvarna pogrešno napisana riječ, a ne neprimjereno prijavljuje samo prvu podebljanu riječ. (#3431)
* U načinu pregledavanja u pregledniku Internet Explorer i drugim MSHTML kontrolama, tabulatorima ili navigacijom jednim slovom za ponovno premještanje na polja obrasca izvještava o natpisu u mnogim slučajevima kada se to nije dogodilo (konkretno, kada se koriste elementi HTML oznake). (#4170)
* Microsoft Word: Izvješćivanje o postojanju i postavljanju komentara je točnije. (#3528)
* Navigacija određenim dijaloškim okvirima u MS Office proizvodima kao što su Word, Excel i Outlook poboljšana je tako što više ne prijavljuje određene alatne trake kontrolnih spremnika koje nisu korisne korisniku. (#4198)
* Čini se da okna zadataka kao što su upravitelj međuspremnika ili Oporavak datoteke više slučajno ne dobivaju fokus prilikom otvaranja aplikacije kao što je Microsoft Word ili Excel, što je ponekad uzrokovalo da se korisnik mora prebaciti s aplikacije i natrag na nju kako bi koristio dokument ili proračunsku tablicu.  (#4199)
* NVDA se više ne pokreće na novijim Windows operativnim sustavima ako je korisnikov Windows jezik postavljen na srpski (latinica). (#4203)
* Pritiskom na numlock dok ste u načinu pomoći za unos sada ispravno prebacujete numlock, umjesto da tipkovnica i operativni sustav postanu nesinkronizirani u odnosu na stanje ove tipke. (#4226)
* U pregledniku Google Chrome naslov dokumenta ponovno se prijavljuje prilikom prebacivanja kartica. U NVDA 2014.2 to se nije dogodilo u nekim slučajevima. (#4222)
* U Google Chromeu i preglednicima koji se temelje na Chromeu URL dokumenta više se ne prijavljuje prilikom prijavljivanja dokumenta. (#4223)
* Kada se pokrene reci sve s odabranim sintisajzerom govora bez govora (korisno za automatizirano testiranje), recite da će se sve sada dovršiti umjesto da se zaustavi nakon prvih nekoliko redaka. (#4225)
* Dijaloški okvir Potpis programa Microsoft Outlook: Polje za uređivanje potpisa sada je dostupno, što omogućuje potpuno praćenje kursora i otkrivanje oblika. (#3833)
* Microsoft Word: Prilikom čitanja posljednjeg retka ćelije tablice više se ne čita cijela ćelija tablice. (#3421)
* Microsoft Word: Prilikom čitanja prvog ili posljednjeg retka tablice sadržaja više se ne čita cijela tablica sadržaja. (#3421)
* Kada izgovarate tipkane riječi i u nekim drugim slučajevima, riječi se više ne lome pogrešno na oznakama kao što su samoglasnički znakovi i virama u indijskim jezicima. (#4254)
* Numerička tekstualna polja koja se mogu uređivati u GoldWaveu sada se ispravno obrađuju. (#670)
* Microsoft Word: kada se krećete po odlomku s control+downArrow / control+upArrow, više ih nije potrebno dvaput pritisnuti ako se krećete kroz popise s grafičkim oznakama ili numerirane. (#3290)

### Promjene za programere

* NVDA sada ima jedinstvenu podršku za dodatnu dokumentaciju. Pojedinosti potražite u odjeljku Dokumentacija o dodatku u Vodiču za razvojne inženjere. (#2694)
* Prilikom pružanja povezivanja gesta na ScriptableObject putem __gestures, sada je moguće navesti ključnu riječ None kao skriptu. Time se gesta odvezuje u svim osnovnim klasama. (#4240)
* Sada je moguće promijeniti tipku prečaca koja se koristi za pokretanje NVDA za lokalizacije gdje normalni prečac uzrokuje probleme. (#2209)
 * To se radi putem gettexta.
 * Imajte na umu da se tekst za opciju Stvori prečac na radnoj površini u dijaloškom okviru Instaliraj NVDA, kao i tipka prečaca u Korisničkom priručniku, također moraju ažurirati.

## 2014.2

### Nove značajke

* Najava odabira teksta sada je moguća u nekim prilagođenim poljima za uređivanje u kojima se koriste informacije za prikaz. (#770)
* U pristupačnim Java aplikacijama sada se najavljuju informacije o položaju za izborne tipke i druge kontrole koje otkrivaju informacije o grupi. (#3754)
* U pristupačnim Java aplikacijama sada se najavljuju tipkovnički prečaci za kontrole koje ih imaju. (#3881)
* U načinu pregledavanja sada se prijavljuju oznake na orijentirima. Također su uključeni u dijaloški okvir Popis elemenata. (#1195)
* U načinu pregledavanja označene regije sada se tretiraju kao orijentiri. (#3741)
* U dokumentima i aplikacijama preglednika Internet Explorer sada su podržane žive regije (dio standarda W3c ARIA), što omogućuje autorima weba da označe određeni sadržaj koji će se automatski izgovarati kako se mijenja. (#1846)

### Promjenama

* Prilikom izlaska iz dijaloškog okvira ili aplikacije unutar dokumenta načina pregledavanja, naziv i vrsta dokumenta načina pregledavanja više se ne objavljuju. (#4069)

### Ispravci grešaka

* Standardni izbornik sustava Windows više nije slučajno utišan u Java aplikacijama. (#3882)
* Prilikom kopiranja teksta s pregleda zaslona, prijelomi redaka više se ne zanemaruju. (#3900)
* Besmisleni objekti razmaka više se ne prijavljuju u nekim aplikacijama kada se fokus promijeni ili kada se koristi navigacija objektima s omogućenim jednostavnim pregledom. (#3839)
* Okviri s porukama i drugi dijaloški okviri koje proizvodi NVDA ponovno uzrokuju otkazivanje prethodnog govora prije najave dijaloškog okvira.
* U načinu pregledavanja, oznake kontrola kao što su veze i gumbi sada se ispravno prikazuju tamo gdje je autor nadjačao oznaku u svrhu pristupačnosti (točnije, pomoću aria-label ili aria-labelledby). (#1354)
* U načinu pregledavanja u pregledniku Internet Explorer tekst sadržan u elementu označenom kao prezentacijski (ARIA role="presentation") više se ne zanemaruje neprimjereno. (#4031)
* Sada je ponovno moguće upisivati vijetnamski tekst pomoću softvera Unikey. Da biste to učinili, poništite potvrdni okvir Ručka tipki iz drugih aplikacija u NVDA dijaloškom okviru Postavke tipkovnice. (#4043)
* U načinu pregledavanja, stavke izbornika za radio i potvrdu prijavljuju se kao kontrole, a ne samo kao tekst na koji se može kliknuti. (#4092)
* NVDA se više ne prebacuje pogrešno iz fokusa u način pregledavanja kada je fokusirana stavka izbornika za provjeru radija ili provjere. (#4092)
* U programu Microsoft PowerPoint s omogućenim govorom o upisanim riječima, znakovi izbrisani s backspaceom više se ne najavljuju kao dio upisane riječi. (#3231)
* U dijaloškim okvirima Mogućnosti sustava Microsoft Office 2010 oznake kombiniranih okvira ispravno se prijavljuju. (#4056)
* U načinu pregledavanja u Mozillinim aplikacijama, korištenje naredbi za brzu navigaciju za prelazak na sljedeći ili prethodni gumb ili polje obrasca sada uključuje preklopne gumbe prema očekivanjima. (#4098)
* Sadržaj upozorenja u Mozillinim aplikacijama više se ne prijavljuje dva puta. (#3481)
* U načinu pregledavanja, spremnici i oriti više se ne ponavljaju neprimjereno dok se krećete unutar njih u isto vrijeme kada se mijenja sadržaj stranice (npr. navigacija web stranicama Facebook i Twitter). (#2199)
* NVDA se oporavlja u više slučajeva kada se prebacuje s aplikacija koje prestaju reagirati. (#3825)
* Kursor (točka umetanja) ponovno se ispravno ažurira prilikom izvođenja naredbe sayAll dok je u tekstu koji se može uređivati nacrtanom izravno na zaslon. (#4125)

## 2014.1

### Nove značajke

* Podrška za Microsoft PowerPoint 2013. Imajte na umu da zaštićeni prikaz nije podržan. (#3578)
* U Microsoft Wordu i Excelu, NVDA sada može pročitati odabrani simbol prilikom odabira simbola pomoću dijaloškog okvira Umetni simbole. (#3538)
* Sada je moguće odabrati hoće li se sadržaj u dokumentima identificirati kao klikljiv putem nove opcije u dijaloškom okviru postavki oblikovanja dokumenta. Ova je opcija uključena prema zadanim postavkama u skladu s prethodnim ponašanjem. (#3556)
* Podrška za Brailleove zaslone povezane putem Bluetootha na računalu sa softverom Widcomm Bluetooth. (#2418)
* Prilikom uređivanja teksta u programu PowerPoint sada se izvješćuju o hipervezama. (#3416)
* Kada se nalazite u ARIA aplikacijama ili dijaloškim okvirima na webu, sada je moguće prisiliti NVDA da se prebaci u način pregledavanja s NVDA+razmak koji omogućuje navigaciju aplikacijom ili dijaloškim okvirom u stilu dokumenta. (#2023)
* U Outlook Expressu / Windows Mailu / Windows Live Mailu, NVDA sada izvještava ima li poruka privitak ili je označena zastavicom. (#1594)
* Prilikom navigacije tablicama u pristupačnim Java aplikacijama, sada se izvještavaju koordinate redaka i stupaca, uključujući zaglavlja stupaca i redaka ako postoje. (#3756)

### Promjenama

* Za Papenmeierove brajice uklonjena je naredba za pomicanje na plošni pregled/fokus. Korisnici mogu dodijeliti vlastite tipke pomoću dijaloškog okvira Ulazne geste. (#3652)
* NVDA se sada oslanja na Microsoft VC runtime verziju 11, što znači da se više ne može pokrenuti na operativnim sustavima starijim od Windows XP Service Pack 2 ili Windows Server 2003 Service Pack 1.
* Razina interpunkcije Neki će sada izgovarati znakove zvjezdice (*) i plus (+). (#3614)
* Nadograđen eSpeak na verziju 1.48.04 koja uključuje mnoge jezične popravke i ispravlja nekoliko rušenja. (#3842, #3739, #3860)

### Ispravci grešaka

* Prilikom premještanja ili odabira ćelija u Microsoft Excelu, NVDA više ne bi trebao neprimjereno najavljivati staru ćeliju umjesto nove ćelije kada Microsoft Excel sporo pomiče odabir. (#3558)
* NVDA ispravno upravlja otvaranjem padajućeg popisa za ćeliju u Microsoft Excelu putem kontekstnog izbornika. (#3586)
* Novi sadržaj stranice na stranicama iTunes 11 trgovine sada se ispravno prikazuje u načinu pretraživanja kada slijedite vezu u trgovini ili kada otvorite trgovinu. (#3625)
* Gumbi za pregled pjesama u iTunes 11 trgovini sada prikazuju svoju oznaku u načinu pregledavanja. (#3638)
* U načinu pregledavanja u pregledniku Google Chrome oznake potvrdnih okvira i izbornih gumba sada se ispravno prikazuju. (#1562)
* U Instantbirdu, NVDA više ne prijavljuje beskorisne informacije svaki put kada prijeđete na kontakt na popisu kontakata. (#2667)
* U načinu pregledavanja u programu Adobe Reader, ispravan tekst sada se prikazuje za gumbe itd. gdje je oznaka nadjačana pomoću opisa alata ili na drugi način. (#3640)
* U načinu pregledavanja u programu Adobe Reader, suvišne grafike koje sadrže tekst "mc-ref" više se neće prikazivati. (#3645)
* NVDA više ne izvještava o svim ćelijama u Microsoft Excelu kao što je podcrtano u njihovim informacijama o formatiranju. (#3669)
* Više ne prikazuju besmislene znakove u dokumentima načina pregledavanja kao što su oni koji se nalaze u rasponu privatne upotrebe Unicode. U nekim slučajevima to je sprječavalo prikazivanje korisnijih oznaka. (#2963)
* Ulazna kompozicija za unos istočnoazijskih znakova više ne uspijeva u PuTTY-u. (#3432)
* Navigacija u dokumentu nakon otkazanog izgovaranja više ne rezultira time da NVDA ponekad pogrešno objavi da ste ostavili polje (kao što je tablica) niže u dokumentu koje se zapravo nikada nije izgovorilo. (#3688)
* Kada koristite naredbe za brzu navigaciju u načinu pregledavanja, a recimo sve s omogućenim preletnim čitanjem, NVDA točnije najavljuje novo polje; npr. sada piše da je naslov naslov, a ne samo njegov tekst. (#3689)
* Naredbe za brzu navigaciju spremnika od skoka do kraja ili početka spremnika sada poštuju obrađeno očitanje tijekom postavke recimo sve; tj. više neće otkazivati trenutnu opciju "reci sve". (#3675)
* Nazivi pokreta dodirom navedeni u NVDA dijaloškom okviru Ulazne geste sada su prijateljski i lokalizirani. (#3624)
* NVDA više ne uzrokuje rušenje određenih programa prilikom pomicanja miša preko njihovih kontrola za obogaćeno uređivanje (TRichEdit). Programi uključuju Jarte 5.1 i BRfácil. (#3693, #3603, #3581)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama spremnici kao što su tablice koje je ARIA označila kao prezentaciju više se ne prijavljuju korisniku. (#3713)
* u programu Microsoft Word NVDA više ne ponavlja informacije o recima i stupcima tablice za ćeliju na zaslonu brajice više puta. (#3702)
* U jezicima koji koriste razmak kao grupu znamenki/razdjelnik tisuća, kao što su francuski i njemački, brojevi iz zasebnih dijelova teksta više se ne izgovaraju kao jedan broj. To je bilo posebno problematično za ćelije tablice koje sadrže brojeve. (#3698)
* Brailleovo pismo više se ponekad ne ažurira kada se kursor sustava premjesti u programu Microsoft Word 2013. (#3784)
* Kada se postavi na prvi znak naslova u programu Microsoft Word, tekst koji komunicira da je naslov (uključujući razinu) više ne nestaje s brajičnog zaslona. (#3701)
* Kada se pokrene konfiguracijski profil za aplikaciju i ta aplikacija izađe, NVDA više ponekad ne uspijeva deaktivirati profil. (#3732)
* Prilikom unosa azijskog unosa u kontrolu unutar samog NVDA (npr. dijaloški okvir za pronalaženje načina pregledavanja), "NVDA" se više ne prijavljuje pogrešno umjesto kandidata. (#3726)
* Kartice u dijaloškom okviru mogućnosti programa Outlook 2013 sada se prijavljuju. (#3826)
* Poboljšana podrška za ARIA live regije u Firefoxu i drugim Mozilla Gecko aplikacijama:
 * Podrška za aria-atomic ažuriranja i filtriranje aria-busy ažuriranja. (#2640)
 * Alternativni tekst (kao što je alt atribut ili aria-label) uključen je ako nema drugog korisnog teksta. (#3329)
 * Ažuriranja područja uživo više se ne utišavaju ako se dogode u isto vrijeme kada se fokus pomiče. (#3777)
* Određeni elementi prezentacije u Firefoxu i drugim Mozilla Gecko aplikacijama više nisu neprikladno prikazani u načinu pregledavanja (točnije, kada je element označen aria-prezentacijom, ali je također fokusiran). (#3781)
* Poboljšanje performansi prilikom navigacije dokumentom u programu Microsoft Word s omogućenim pravopisnim pogreškama. (#3785)
* Nekoliko popravaka podrške za pristupačne Java aplikacije:
 * Inicijalno fokusirana kontrola u okviru ili dijaloškom okviru više se ne prijavljuje kada okvir ili dijaloški okvir dođu u prvi plan. (#3753)
 * Nekorisne informacije o položaju više se ne objavljuju za radio tipke (npr. 1 od 1). (#3754)
 * Bolje izvještavanje o JComboBox kontrolama (html se više ne izvještava, bolje izvještavanje o proširenim i srušenim stanjima). (#3755)
 * Prilikom prijavljivanja teksta dijaloških okvira sada je uključen neki tekst koji je prije nedostajao. (#3757)
 * Promjene naziva, vrijednosti ili opisa fokusirane kontrole sada se izvješćuju točnije. (#3770)
* Ispravljanje rušenja NVDA u sustavu Windows 8 kada se fokusirate na određene RichEdit kontrole koje sadrže velike količine teksta (npr. NVDA-ov preglednik dnevnika, windbg). (#3867)
* Na sustavima s visokom postavkom DPI zaslona (koja se prema zadanim postavkama javlja na mnogim modernim zaslonima), NVDA više ne usmjerava miš na pogrešno mjesto u nekim aplikacijama. (#3758, #3703)
* Riješen je povremeni problem prilikom pregledavanja weba gdje bi NVDA prestao ispravno raditi do ponovnog pokretanja, iako se nije rušio ili zamrzavao. (#3804)
* Papenmeierov brajični zaslon sada se može koristiti čak i ako Papenmeierov zaslon nikada nije bio spojen putem USB-a. (#3712)
* NVDA se više ne zamrzava kada se odabere Papenmeier BRAILLEX Brailleov zaslon starijih modela bez priključenog zaslona.

### Promjene za programere

* AppModules sada sadrže svojstva productName i productVersion. Te su informacije sada uključene i u Informacije za razvojne programere (NVDA+f1). (#1625)
* U Python konzoli sada možete pritisnuti tipku tab da biste dovršili trenutni identifikator. (#433)
 * Ako postoji više mogućnosti, možete pritisnuti tabulatora drugi put da biste odabrali s popisa.

## 2013.3

### Nove značajke

* Polja obrasca sada se prijavljuju u Microsoft Word dokumentima. (#2295)
* NVDA sada može objaviti informacije o izmjenama u Microsoft Wordu kada je omogućena opcija Praćenje promjena. Imajte na umu da revizije uređivača izvješća u NVDA dijaloškom okviru postavki dokumenta (isključeno prema zadanim postavkama) moraju biti omogućene i da bi bile najavljene. (#1670)
* Padajući popisi u programu Microsoft Excel 2003 do 2010 sada se najavljuju prilikom otvaranja i navigacije. (#3382)
* nova opcija 'Dopusti preletno čitanje u Say All' u dijaloškom okviru postavki tipkovnice omogućuje navigaciju kroz dokument s brzom navigacijom u načinu pregledavanja i naredbama za pomicanje redaka / odlomka, dok ostajete u Reci sve. Ova je opcija prema zadanim postavkama isključena. (#2766)
* Sada postoji dijaloški okvir Ulazne geste koji omogućuje jednostavniju prilagodbu ulaznih gesta (kao što su tipke na tipkovnici) za NVDA naredbe. (#1532)
* Sada možete imati različite postavke za različite situacije pomoću konfiguracijskih profila. Profili se mogu aktivirati ručno ili automatski (npr. za određenu primjenu). (#87, #667, #1913)
* U programu Microsoft Excel ćelije koje su veze sada se najavljuju kao veze. (#3042)
* U programu Microsoft Excel, postojanje komentara na ćeliji sada se prijavljuje korisniku. (#2921)

### Ispravci grešaka

* Zend Studio sada funkcionira isto kao i Eclipse. (#3420)
* Promijenjeno stanje određenih potvrdnih okvira u dijaloškom okviru pravila poruka programa Microsoft Outlook 2010 sada se automatski prijavljuje. (#3063)
* NVDA će sada izvještavati o stanju prikvačenosti za prikvačene kontrole kao što su kartice u pregledniku Mozilla Firefox. (#3372)
* Sada je moguće povezati skripte s tipkama na tipkovnici koje sadrže Alt i/ili Windows tipke kao modifikatore. Prije toga, ako je to učinjeno, izvođenje skripte uzrokovalo bi aktiviranje izbornika Start ili trake izbornika. (#3472)
* Odabir teksta u dokumentima načina pregledavanja (npr. pomoću control+shift+end) više ne uzrokuje uključivanje rasporeda tipkovnice na sustavima s instaliranim više rasporeda tipkovnice. (#3472)
* Internet Explorer se više ne bi trebao rušiti ili postati neupotrebljiv prilikom zatvaranja NVDA-a. (#3397)
* Fizičko kretanje i drugi događaji na nekim novijim računalima više se ne tretiraju kao neprikladni pritisci tipki. Prije je to utišavalo govor i ponekad aktiviralo NVDA naredbe. (#3468)
* NVDA se sada ponaša kao što se očekuje u Poeditu 1.5.7. Korisnici koji koriste starije verzije morat će ažurirati. (#3485)
* NVDA sada može čitati zaštićene dokumente u programu Microsoft Word 2010 i više ne uzrokuje rušenje programa Microsoft Word. (#1686)
* Ako se prilikom pokretanja NVDA distribucijskog paketa navede nepoznati prekidač naredbenog retka, on više ne uzrokuje beskrajnu petlju dijaloških okvira s pogreškama. (#3463)
* NVDA više ne izvještava o zamjenskom tekstu grafika i objekata u Microsoft Wordu ako zamjenski tekst sadrži navodnike ili druge nestandardne znakove. (#3579)
* Broj stavki za određene vodoravne popise u načinu pregledavanja sada je točan. Prije je to mogao biti dvostruko veći od stvarnog iznosa. (#2151)
* Kada pritisnete control+a na radnom listu programa Microsoft Excel, sada će se prijaviti ažurirani odabir. (#3043)
* NVDA sada može ispravno čitati XHTML dokumente u Microsoft Internet Exploreru i drugim MSHTML kontrolama. (#3542)
* Dijaloški okvir postavki tipkovnice: ako nijedna tipka nije odabrana za korištenje kao NVDA tipka, korisniku se prikazuje pogreška prilikom odbacivanja dijaloškog okvira. Za pravilno korištenje NVDA uređaja mora se odabrati barem jedan ključ. (#2871)
* U Microsoft Excelu, NVDA sada najavljuje spojene ćelije drugačije od više odabranih ćelija. (#3567)
* Pokazivač načina pregledavanja više nije pogrešno postavljen prilikom napuštanja dijaloškog okvira ili aplikacije unutar dokumenta. (#3145)
* Riješen je problem zbog kojeg upravljački program za Brailliant BI/B seriju nije bio prikazan kao opcija u dijaloškom okviru Postavke Brailleovog pisma na nekim sustavima, iako je takav zaslon bio povezan putem USB-a.
* NVDA se više ne uspijeva prebaciti na pregled zaslona kada objekt navigatora nema stvarnu lokaciju zaslona. U tom je slučaju pokazivač pregleda sada postavljen na vrh zaslona. (#3454)
* Riješen je problem koji je u nekim okolnostima uzrokovao neuspjeh upravljačkog programa Brailleovog pisma Freedom Scientific kada je priključak postavljen na USB. (#3509, #3662)
* Riješen je problem zbog kojeg tipke na Brailleovom pismu Freedom Scientific nisu otkrivene u nekim okolnostima. (#3401, #3662)

### Promjene za programere

* Možete odrediti kategoriju koja će se prikazati korisniku za skripte pomoću atributa scriptCategory na klasama ScriptableObject i atributa category na metodama skripte. Dodatne pojedinosti potražite u dokumentaciji za baseObject.ScriptableObject. (#1532)
* config.save je zastario i može se ukloniti u budućem izdanju. Umjesto toga koristite config.conf.save. (#667)
* config.validateConfig je zastario i može se ukloniti u budućem izdanju. Dodaci kojima je to potrebno trebali bi osigurati vlastitu implementaciju. (#667, #3632)

## 2013.2

### Nove značajke

* Podrška za Chromium Embedded Framework, koji je kontrola web preglednika koja se koristi u nekoliko aplikacija. (#3108)
* Nova eSpeak glasovna varijanta: Iven3.
* U Skypeu se nove poruke čavrljanja automatski prijavljuju dok je razgovor usredotočen. (#2298)
* Podrška za Tween, uključujući izvještavanje o nazivima kartica i manje opširnosti prilikom čitanja tweetova.
* Sada možete onemogućiti prikaz NVDA poruka na Brailleovom pismu tako da postavite vremensko ograničenje poruke na 0 u dijaloškom okviru Postavke brajice. (#2482)
* U Upravitelju dodataka sada se nalazi gumb Dohvati dodatke za otvaranje web stranice NVDA dodataka na kojoj možete pregledavati i preuzimati dostupne dodatke. (#3209)
* U dijaloškom okviru dobrodošlice NVDA koji se uvijek pojavljuje prilikom prvog pokretanja NVDA-e, sada možete odrediti hoće li se NVDA automatski pokrenuti nakon što se prijavite u Windows. (#2234)
* Način mirovanja automatski je omogućen kada koristite Dolphin Cicero. (#2055)
* Sada je podržana Windows x64 verzija Miranda IM/Miranda NG. (#3296)
* Prijedlozi za pretraživanje na početnom zaslonu sustava Windows 8.1 automatski se prijavljuju. (#3322)
* Podrška za navigaciju i uređivanje proračunskih tablica u programu Microsoft Excel 2013. (#3360)
* Brajevi zasloni Freedom Scientific Focus 14 Blue i Focus 80 Blue, kao i Focus 40 Blue u određenim konfiguracijama koje prije nisu bile podržane, sada su podržani kada su povezani putem Bluetootha. (#3307)
* Prijedlozi automatskog dovršetka sada se prijavljuju u programu Outlook 2010. (#2816)
* Nove tablice za prijevod Brailleovog pisma: engleska (UK) računalna brajica, korejski razred 2, ruski Brailleovo pismo za računalni kod.
* Novi jezik: farsi. (#1427)

### Promjenama

* Na dodirnom zaslonu, izvođenje pomicanja jednim prstom ulijevo ili udesno u načinu rada objekta sada se pomiče prethodni ili sljedeći kroz sve objekte, a ne samo one u trenutnom spremniku. Upotrijebite pomicanje prsta ulijevo ili udesno s 2 prsta za izvođenje izvorne radnje premještanja na prethodni ili sljedeći objekt u trenutnom spremniku.
* potvrdni okvir tablice izgleda izvješća koji se nalazi u dijaloškom okviru postavki načina pregledavanja sada je preimenovan u Uključi tablice izgleda kako bi se odrazilo da ih brza navigacija također neće locirati ako potvrdni okvir nije označen. (#3140)
* Plošni pregled zamijenjen je načinima pregleda objekata, dokumenata i zaslona. (#2996)
 * Pregled objekata pregledava tekst samo unutar objekta navigatora, pregled dokumenta pregledava sav tekst u dokumentu načina pregledavanja (ako postoji) i pregled zaslona pregledava tekst na zaslonu za trenutnu aplikaciju.
 * Naredbe koje su se prethodno premještale na/iz ravnog pregleda sada se prebacuju između ovih novih načina pregleda.
 * Objekt navigatora automatski slijedi kursor pregleda tako da ostaje najdublji objekt na položaju kursora pregleda kada je u načinu pregleda dokumenta ili zaslona.
 * Nakon prelaska u način pregleda zaslona, NVDA će ostati u ovom načinu rada sve dok se izričito ne vratite u način pregleda dokumenta ili objekta.
 * Kada je u načinu pregleda dokumenta ili objekta, NVDA se može automatski prebacivati između ova dva načina rada ovisno o tome krećete li se po dokumentu ili ne.
* Ažuriran prevoditelj brajice liblouis na 2.5.3. (#3371)

### Ispravci grešaka

* Aktiviranje objekta sada najavljuje radnju prije aktivacije, a ne radnju nakon aktivacije (npr. proširi prilikom proširenja, a ne sažim). (#2982)
* Preciznije čitanje i praćenje kursora u raznim poljima za unos za novije verzije Skypea, kao što su polja za chat i pretraživanje. (#1601, #3036)
* Na popisu nedavnih razgovora putem Skypea sada se čita broj novih događaja za svaki razgovor, ako je relevantno. (#1446)
* Poboljšanja praćenja kursora i redoslijeda čitanja teksta koji se piše zdesna nalijevo na zaslon; npr. uređivanje arapskog teksta u programu Microsoft Excel. (#1601)
* Brza navigacija do gumba i polja obrazaca sada će pronaći veze označene kao gumbi za potrebe pristupačnosti u pregledniku Internet Explorer. (#2750)
* U načinu pregledavanja sadržaj unutar prikaza stabla više se ne prikazuje jer spljošteni prikaz nije koristan. Možete pritisnuti enter u prikazu stabla za interakciju s njim u načinu fokusiranja. (#3023)
* Pritiskom na alt+strelica prema dolje ili alt+strelica prema gore da biste proširili kombinirani okvir dok ste u načinu fokusiranja više se neispravno ne prebacuje u način pregledavanja. (#2340)
* U pregledniku Internet Explorer 10 ćelije tablice više ne aktiviraju način fokusiranja, osim ako ih je autor weba izričito izoštrio. (#3248)
* NVDA se više ne pokreće ako je vrijeme sustava ranije od posljednje provjere ažuriranja. (#3260)
* Ako je na brajičnom zaslonu prikazana traka napretka, brajičin prikaz ažurira se kada se promijeni traka napretka. (#3258)
* U načinu pregledavanja u Mozillinim aplikacijama, opisi tablica više se ne prikazuju dvaput. Osim toga, sažetak se prikazuje kada postoji i naslov. (#3196)
* Prilikom promjene jezika unosa u sustavu Windows 8, NVDA sada govori ispravan jezik, a ne prethodni.
* NVDA sada najavljuje promjene načina pretvorbe IME-a u sustavu Windows 8.
* NVDA više ne objavljuje smeće na radnoj površini kada se koriste Google japanski ili Atok IME načini unosa. (#3234)
* U sustavu Windows 7 i novijim verzijama, NVDA više ne najavljuje neprimjereno prepoznavanje govora ili unos dodirom kao promjenu jezika tipkovnice.
* NVDA više ne najavljuje određeni poseban znak (0x7f) kada pritisnete control+backspace u nekim uređivačima kada je omogućeno izgovaranje upisanih znakova. (#3315)
* eSpeak više ne mijenja neprimjereno visinu tona, glasnoću itd. kada NVDA čita tekst koji sadrži određene kontrolne znakove ili XML. (#3334) (regresija #437)
* U Java aplikacijama promjene oznake ili vrijednosti fokusirane kontrole sada se automatski najavljuju i odražavaju se prilikom naknadnog postavljanja upita kontroli. (#3119)
* U kontrolama Scintilla redovi se sada ispravno prijavljuju kada je omogućeno prelamanje riječi. (#885)
* U Mozillinim aplikacijama, nazivi stavki popisa samo za čitanje sada se ispravno prijavljuju; Npr. prilikom navigacije tweetovima u načinu rada fokusa na twitter.com. (#3327)
* Dijaloški okviri za potvrdu u sustavu Microsoft Office 2013 sada se automatski čitaju kada se pojave.
* Poboljšanja performansi prilikom navigacije određenim tablicama u programu Microsoft Word. (#3326)
* NVDA naredbe za navigaciju tablicom (control+alt+strelice) bolje funkcioniraju u određenim Microsoft Word tablicama gdje se ćelija proteže kroz više redaka.
* Ako je Upravitelj dodataka već otvoren, njegovo ponovno aktiviranje (bilo iz izbornika Alati ili otvaranjem datoteke dodataka) više ne uspijeva ili onemogućuje zatvaranje Upravitelja dodataka. (#3351)
* NVDA se više ne zamrzava u određenim dijaloškim okvirima kada se koristi japanski ili kineski Office 2010 IME. (#3064)
* Više razmaka više se ne komprimira u samo jedan prostor na Brajevom pismu. (#1366)
* Zend Eclipse PHP Developer Tools sada funkcionira isto kao i Eclipse. (#3353)
* U Internet Exploreru, Opet nije potrebno pritisnuti tabulator za interakciju s ugrađenim objektom (kao što je Flash sadržaj) nakon što pritisnete enter na njemu. (#3364)
* Prilikom uređivanja teksta u programu Microsoft PowerPoint, zadnji redak više se ne prijavljuje kao redak iznad, ako je posljednji redak prazan. (#3403)
* U programu Microsoft PowerPoint objekti se više ne izgovaraju dvaput kada ih odaberete ili uredite. (#3394)
* NVDA više ne uzrokuje pad ili zamrzavanje Adobe Readera za određene loše oblikovane PDF dokumente koji sadrže retke izvan tablica. (#3399)
* NVDA sada ispravno detektira sljedeći slajd s fokusom prilikom brisanja slajda u prikazu sličica programa Microsoft PowerPoint. (#3415)

### Promjene za programere

* windowUtils.findDescendantWindow dodan je za traženje prozora potomka (HWND) koji odgovara navedenoj vidljivosti, ID-u kontrole i/ili nazivu klase.
* Udaljena Python konzola više ne istječe nakon 10 sekundi dok čeka unos. (#3126)
* Uključivanje bisect modula u binarne verzije je zastarjelo i može se ukloniti u budućem izdanju. (#3368)
 * Dodatke koji ovise o bisectu (uključujući urllib2 modul) treba ažurirati kako bi uključili ovaj modul.

## 2013.1.1

Ovo izdanje rješava problem zbog kojeg se NVDA srušio prilikom pokretanja ako je konfiguriran za korištenje irskog jezika, kao i ažuriranja prijevoda i neke druge ispravke grešaka.

### Ispravci grešaka

* Ispravni znakovi se proizvode prilikom tipkanja u NVDA vlastitom korisničkom sučelju dok koristite korejsku ili japansku metodu unosa dok je to zadana metoda. (#2909)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama polja koja su označena kao da sadrže nevažeći unos sada se ispravno obrađuju. (#3256)
* NVDA se više ne ruši kada se pokrene ako je konfiguriran za korištenje irskog jezika.

## 2013.1

Istaknute značajke ovog izdanja uključuju intuitivniji i dosljedniji raspored tipkovnice prijenosnog računala; osnovna podrška za Microsoft PowerPoint; podrška za duge opise u web preglednicima; i podrška za unos računalne brajice za brajice koji imaju brajičnu tipkovnicu.

### Važno

#### Novi raspored tipkovnice prijenosnog računala

Raspored tipkovnice prijenosnog računala potpuno je redizajniran kako bi bio intuitivniji i dosljedniji.
Novi izgled koristi tipke sa strelicama u kombinaciji s NVDA tipkom i drugim modifikatorima za naredbe za pregled.

Obratite pažnju na sljedeće promjene u često korištenim naredbama:

| Ime |Ključ|
|---|---|
|Reci sve |NVDA+a|
|Pročitajte trenutni redak |NVDA+l|
|Čitanje trenutnog odabira teksta |NVDA+shift+s|
|Traka stanja izvješća |NVDA+shift+kraj|

Osim toga, između ostalih promjena, promijenjene su sve naredbe prstena za navigaciju objektima, pregled teksta, klik mišem i sintisajzerske postavke.
Za nove tipke pogledajte dokument [Commands Quick Reference](keyCommands.html).

### Nove značajke

* Osnovna podrška za uređivanje i čitanje Microsoft PowerPoint prezentacija. (#501)
* Osnovna podrška za čitanje i pisanje poruka u programu Lotus Notes 8.5. (#543)
* Podrška za automatsko prebacivanje jezika prilikom čitanja dokumenata u programu Microsoft Word. (#2047)
* U načinu pregledavanja za MSHTML (npr. Internet Explorer) i Gecko (npr. Firefox), sada je najavljeno postojanje dugih opisa. Također je moguće otvoriti dugi opis u novom prozoru pritiskom na NVDA+d. (#809)
* Obavijesti u pregledniku Internet Explorer 9 i novijim verzijama sada se izgovaraju (kao što su blokiranje sadržaja ili preuzimanja datoteka). (#2343)
* Automatsko izvješćivanje o zaglavljima redaka i stupaca tablice sada je podržano za dokumente načina pregledavanja u pregledniku Internet Explorer i drugim MSHTML kontrolama. (#778)
* Novi jezik: aragonski, irski
* Nove tablice za prijevod Brailleovog pisma: danski razred 2, korejski razred 1. (#2737)
* Podrška za Brailleove zaslone povezane putem bluetootha na računalu s kojim je pokrenut Bluetooth Stack za Windows tvrtke Toshiba. (#2419)
* Podrška za odabir priključaka pri korištenju zaslona Freedom Scientific (automatski, USB ili Bluetooth).
* Podrška za BrailleNote obitelj bilježnika iz programa HumanWare kada djeluje kao Brailleov terminal za čitač zaslona. (#2012)
* Podrška za starije modele Papenmeier BRAILLEX brajevih zaslona. (#2679)
* Podrška za unos računalne brajice za brajice koji imaju brajičnu tipkovnicu. (#808)
* Nove postavke tipkovnice koje omogućuju odabir hoće li NVDA prekinuti govor za upisane znakove i/ili tipku Enter. (#698)
* Podrška za nekoliko preglednika temeljenih na Google Chromeu: Rockmelt, BlackHawk, Comodo Dragon i SRWare Iron. (#2236, #2813, #2814, #2815)

### Promjenama

* Ažuriran prevoditelj brajevog pisma liblouis na 2.5.2. (#2737)
* Raspored tipkovnice prijenosnog računala potpuno je redizajniran kako bi bio intuitivniji i dosljedniji. (#804)
* Ažuriran eSpeak sintisajzer govora na 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Ispravci grešaka

* Tipke za brzu navigaciju za prelazak na sljedeći ili prethodni razdjelnik u načinu pregledavanja sada funkcioniraju u pregledniku Internet Explorer i drugim MSHTML kontrolama. (#2781)
* Ako se NVDA vrati na eSpeak ili nema govora zbog neuspjeha konfiguriranog sintisajzera govora kada se NVDA pokrene, konfigurirani izbor više se ne postavlja automatski na rezervni sintisajzer. To znači da će se sada originalni sintisajzer ponovno isprobati sljedeći put kada NVDA pokrene. (#2589)
* Ako NVDA padne na brak brajice zbog neuspjeha konfiguriranog prikaza brajice kada se NVDA pokrene, konfigurirani zaslon više nije automatski postavljen na bez brajice. To znači da će se sada originalni zaslon ponovno pokušati sljedeći put kada NVDA pokrene. (#2264)
* U načinu pregledavanja u Mozillinim aplikacijama, ažuriranja tablica sada se ispravno prikazuju. Na primjer, u ažuriranim ćelijama izvještavaju se koordinate redaka i stupaca, a navigacija tablicom funkcionira kako treba. (#2784)
* U načinu pregledavanja u web-preglednicima, određene neoznačene grafike koje se mogu kliknuti, a koje prethodno nisu bile prikazane, sada se ispravno prikazuju. (#2838)
* Sada su podržane starije i novije verzije SecureCRT-a. (#2800)
* Za metode unosa kao što je Easy Dots IME pod XP-om, niz za čitanje sada se ispravno prijavljuje.
* Popis kandidata u kineskoj pojednostavljenoj metodi unosa Microsoft Pinyin u sustavu Windows 7 sada se ispravno čita prilikom mijenjanja stranica strelicom lijevo i desno te prilikom prvog otvaranja pomoću početne stranice.
* Kada se spremaju podaci o izgovoru prilagođenih simbola, napredno polje "sačuvaj" više se ne uklanja. (#2852)
* Kada onemogućite automatsku provjeru ažuriranja, NVDA se više ne mora ponovno pokretati kako bi promjena u potpunosti stupila na snagu.
* NVDA se više ne pokreće ako se dodatak ne može ukloniti jer njegov direktorij trenutno koristi druga aplikacija. (#2860)
* Oznake kartica u dijaloškom okviru postavki DropBoxa sada se mogu vidjeti s ravnim pregledom.
* Ako se jezik unosa promijeni u nešto drugo osim zadanog, NVDA sada ispravno detektira tipke za naredbe i način pomoći za unos.
* Za jezike kao što je njemački gdje je znak + (plus) jedna tipka na tipkovnici, sada je moguće povezati naredbe s njim pomoću riječi "plus". (#2898)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama blokirani navodnici sada se prijavljuju gdje je to prikladno. (#2888)
* Upravljački program za brajicu serije HumanWare Brailliant BI/B sada se može odabrati kada je zaslon povezan putem Bluetootha, ali nikada nije bio povezan putem USB-a.
* Filtriranje elemenata na popisu elemenata načina pregledavanja s velikim slovima tekstom filtra sada vraća rezultate bez razlikovanja velikih i malih slova, kao i malih slova, a ne ništa. (#2951)
* U Mozillinim preglednicima, način pregledavanja može se ponovno koristiti kada je Flash sadržaj fokusiran. (#2546)
* Kada koristite skraćenu tablicu brajice i proširite na računalnu brajicu za riječ na pokazivaču, pokazivač brajice sada je ispravno postavljen kada se nalazi iza riječi u kojoj je znak predstavljen s više ćelija brajice (npr. velikim znakom, slovnim znakom, brojčanim znakom itd.). (#2947)
* Odabir teksta sada se ispravno prikazuje na brajicinom jeziku u aplikacijama kao što su Microsoft Word 2003 i kontrole za uređivanje preglednika Internet Explorer.
* Ponovno je moguće odabrati tekst u smjeru unatrag u programu Microsoft Word dok je Brailleovo pismo omogućeno.
* Prilikom pregleda, razmaka ili brisanja znakova U kontrolama za uređivanje Scintilla, NVDA ispravno najavljuje višebajtne znakove. (#2855)
* NVDA se više neće uspjeti instalirati ako put korisničkog profila sadrži određene višebajtne znakove. (#2729)
* Izvješćivanje o grupama za kontrole prikaza popisa (SysListview32) u 64-bitnim aplikacijama više ne uzrokuje pogrešku.
* U načinu pregledavanja u Mozillinim aplikacijama, tekstualni sadržaj se u nekim rijetkim slučajevima više ne tretira pogrešno kao da se može uređivati. (#2959)
* U IBM Lotus Symphony i OpenOffice, pomicanje kursora sada pomiče kursor pregleda ako je prikladno.
* Adobe Flash sadržaj sada je dostupan u pregledniku Internet Explorer u sustavu Windows 8. (#2454)
* Fiksna Bluetooth podrška za Papenmeier Braillex Trio. (#2995)
* Ispravljena je nemogućnost korištenja određenih glasova Microsoft Speech API-ja verzije 5 kao što su glasovi Koba Speech 2. (#2629)
* U aplikacijama koje koriste Java Access Bridge, brajičevi se zasloni sada ispravno ažuriraju kada se kursor pomiče u tekstnim poljima koja se mogu uređivati. (#3107)
* Podržavajte orijentir obrasca u dokumentima načina pregledavanja koji podržavaju orijentir. (#2997)
* Upravljački program eSpeak sintesajzera sada prikladnije obrađuje čitanje po znakovima (npr. najavljuje naziv ili vrijednost stranog slova, a ne samo njegov zvuk ili generički naziv). (#3106)
* NVDA više ne uspijeva kopirati korisničke postavke za korištenje na zaslonima za prijavu i drugim sigurnim zaslonima kada put korisničkog profila sadrži znakove koji nisu ASCII. (#3092)
* NVDA se više ne zamrzava kada se koristi unos azijskih znakova u nekim .NET aplikacijama. (#3005)
* sada je moguće koristiti način pregledavanja za stranice u pregledniku Internet Explorer 10 kada je u standardnom načinu rada; npr. [www.gmail.com](http://www.gmail.com) stranica za prijavu. (#3151)

### Promjene za programere

* Upravljački programi Brailleovog zaslona sada mogu podržavati ručni odabir porta. (#426)
 * Ovo je najkorisnije za Brailleove zaslone koji podržavaju povezivanje putem naslijeđenog serijskog priključka.
 * To se radi pomoću metode klase getPossiblePorts na klasi BrailleDisplayDriver.
* Sada je podržan unos brajice s tipkovnica za brajicu. (#808)
 * Brailleov unos obuhvaćen je klasom brailleInput.BrailleInputGesture ili njezinom podklasom.
 * Podklase Brailleovog pisma. BrailleDisplayGesture (kao što je implementirano u upravljačkim programima za Brailleov zaslon) također može naslijediti od brailleInput.BrailleInputGesture. To omogućuje da naredbe za prikaz i unos brajice upravlja istom klasom gesta.
* Sada možete koristiti comHelper.getActiveObject za dobivanje aktivnog COM objekta iz normalnog procesa kada je NVDA pokrenut s privilegijom UIAccess. (#2483)

## 2012.3

Istaknuti dijelovi ovog izdanja uključuju podršku za unos azijskih znakova; eksperimentalna podrška za zaslone osjetljive na dodir u sustavu Windows 8; izvještavanje o brojevima stranica i poboljšana podrška za tablice u Adobe Readeru; naredbe za navigaciju tablicom u fokusiranim retcima tablice i kontrolama prikaza popisa u sustavu Windows; podrška za još nekoliko Brailleovih zaslona; i izvješćivanje o zaglavljima redaka i stupaca u programu Microsoft Excel.

### Nove značajke

* NVDA sada može podržavati unos azijskih znakova pomoću IME-a i metoda unosa tekstualnih usluga u svim aplikacijama, uključujući:
 * Izvješćivanje i navigacija popisima predloženih kandidata;
 * Izvješćivanje i navigacija nizovima sastava; i
 * Izvještavanje o čitanju nizova.
* Prisutnost podcrtavanja i precrtavanja sada je prijavljena u dokumentima Adobe Readera. (#2410)
* Kada je omogućena funkcija Windows Sticky Keys, NVDA modifikacijska tipka sada će se ponašati kao i druge modifikacijske tipke. To vam omogućuje korištenje NVDA modifikatorske tipke bez potrebe da je držite pritisnutom dok pritišćete druge tipke. (#230)
* Automatsko izvješćivanje o zaglavljima stupaca i redaka sada je podržano u programu Microsoft Excel. Pritisnite NVDA+shift+c za postavljanje retka koji sadrži zaglavlja stupaca i NVDA+shift+r za postavljanje stupca koji sadrži zaglavlja redaka. Pritisnite bilo koju naredbu dva puta uzastopno da biste izbrisali postavku. (#1519)
* Podrška za HIMS Braille Sense, Braille EDGE i SyncBraille Braille zaslone. (#1266, #1267)
* Kada se pojave obavijesti o zdravlju sustava Windows 8, NVDA će ih prijaviti ako je omogućeno izvještavanje o balončićima pomoći. (#2143)
* Eksperimentalna podrška za zaslone osjetljive na dodir u sustavu Windows 8, uključujući:
 * Čitanje teksta izravno ispod prsta dok ga pomičete
 * Mnoge geste za navigaciju objektima, pregled teksta i druge NVDA naredbe.
* Podrška za VIP Mud. (#1728)
* U programu Adobe Reader, ako tablica ima sažetak, on se sada prikazuje. (#2465)
* U programu Adobe Reader sada se mogu prijaviti zaglavlja redaka i stupaca tablice. (#2193, #2527, #2528)
* Novi jezici: amharski, korejski, nepalski, slovenski.
* NVDA sada može čitati prijedloge za automatsko dovršavanje prilikom unosa e-mail adresa u Microsoft Outlook 2007. (#689)
* Nove eSpeak glasovne varijante: Gene, Gene2. (#2512)
* U programu Adobe Reader sada se mogu prijaviti brojevi stranica. (#2534)
 * U Readeru XI, oznake stranica se prijavljuju tamo gdje postoje, odražavajući promjene u numeriranju stranica u različitim odjeljcima itd. U ranijim verzijama to nije bilo moguće i prijavljuju se samo uzastopni brojevi stranica.
* Sada je moguće vratiti NVDA konfiguraciju na tvorničke postavke ili brzim pritiskom na NVDA+control+r tri puta ili odabirom Vrati na tvorničke postavke iz NVDA izbornika. (#2086)
* Podrška za Seika verzije 3, 4 i 5 i Seika80 brajice iz Nippon Telesofta. (#2452)
* Prvi i posljednji gornji gumbi za usmjeravanje na Freedom Scientific PAC Mate i Focus Brailleovom pismu sada se mogu koristiti za pomicanje unatrag i natrag. (#2556)
* Na zaslonima brajice Freedom Scientific Focus podržane su mnoge druge značajke, kao što su napredne trake, preklopne trake i određene kombinacije točaka za uobičajene radnje. (#2516)
* U aplikacijama koje koriste IAccessible2, kao što su Mozilline aplikacije, zaglavlja redaka i stupaca tablice sada se mogu prijaviti izvan načina pregledavanja. (#926)
* Preliminarna podrška za kontrolu dokumenata u programu Microsoft Word 2013. (#2543)
* Poravnanje teksta sada se može prijaviti u aplikacijama koje koriste IAccessible2 kao što su Mozilla aplikacije. (#2612)
* Kada je redak tablice ili standardna kontrola prikaza popisa sustava Windows s više stupaca usredotočena, sada možete koristiti naredbe za navigaciju tablicom za pristup pojedinačnim ćelijama. (#828)
* Nove tablice za prijevod Brailleovog pisma: estonski razred 0, portugalski računalni braille s 8 točaka, talijanski računalni braille sa 6 točaka. (#2319, #2662)
* Ako je NVDA instaliran na sustavu, izravno otvaranje NVDA dodatnog paketa (npr. iz Windows Explorera ili nakon preuzimanja u web pregledniku) instalirat će ga u NVDA. (#2306)
* Podrška za novije modele Papenmeier BRAILLEX brajevih zaslona. (#1265)
* Informacije o položaju (npr. 1 od 4) sada se prijavljuju za stavke popisa Windows Explorera u sustavu Windows 7 i novijim verzijama. To također uključuje sve kontrole UIAutomation koje podržavaju prilagođena svojstva itemIndex i itemCount. (#2643)

### Promjenama

* U dijaloškom okviru Postavke NVDA pregleda kursor, opcija Prati fokus tipkovnice preimenovana je u Prati fokus sustava radi dosljednosti s terminologijom koja se koristi drugdje u NVDA.
* Kada je brajica vezana za pregled, a pokazivač je na objektu koji nije tekstni objekt (npr. tekstno polje koje se može uređivati), tipke za usmjeravanje pokazivača sada će aktivirati objekt. (#2386)
* Opcija Spremi postavke pri izlasku sada je uključena prema zadanim postavkama za nove konfiguracije.
* Prilikom ažuriranja prethodno instalirane kopije NVDA-a, tipka prečaca na radnoj površini više se ne vraća na control+alt+n ako ju je korisnik ručno promijenio u nešto drugo. (#2572)
* Popis dodataka u Upravitelju dodataka sada prikazuje naziv paketa prije njegovog statusa. (#2548)
* Ako instalirate istu ili drugu verziju trenutno instaliranog dodatka, NVDA će vas pitati želite li ažurirati dodatak, umjesto da samo prikaže pogrešku i prekine instalaciju. (#2501)
* Naredbe za navigaciju objektima (osim naredbe za prijavu trenutnog objekta) sada izvješćuju s manje opširnosti. Dodatne informacije i dalje možete dobiti pomoću naredbe za prijavu trenutnog objekta. (#2560)
* Ažuriran prevoditelj brajevog pisma liblouis na 2.5.1. (#2319, #2480, #2662, #2672)
* Dokument Brza referenca NVDA naredbi za tipke preimenovan je u Brza referenca naredbi jer sada uključuje naredbe na dodir i tipkovnice.
* Popis elemenata u načinu pregledavanja sada će zapamtiti posljednju prikazanu vrstu elementa (npr. poveznice, naslove ili orijentire) svaki put kada se dijaloški okvir prikaže unutar iste NVDA sesije. (#365)
* Većina Metro aplikacija u sustavu Windows 8 (npr. Pošta, Kalendar) više ne aktivira način pregledavanja za cijelu aplikaciju.
* Ažuriran Handy Tech BrailleDriver COM-Server na 1.4.2.0.

### Ispravci grešaka

* U sustavu Windows Vista i novijim verzijama, NVDA više ne tretira pogrešno tipku Windows kao pritisnutu prilikom otključavanja sustava Windows nakon što je zaključa pritiskom na Windows+l. (#1856)
* U programu Adobe Reader zaglavlja redaka sada se ispravno prepoznaju kao ćelije tablice; tj. koordinate se prijavljuju i može im se pristupiti pomoću naredbi za navigaciju u tablici. (#2444)
* U programu Adobe Reader, ćelije tablice koje obuhvaćaju više od jednog stupca i/ili retka sada se obrađuju ispravno. (#2437, #2438, #2450)
* NVDA distribucijski paket sada provjerava svoj integritet prije izvođenja. (#2475)
* Privremene datoteke za preuzimanje sada se uklanjaju ako preuzimanje NVDA ažuriranja ne uspije. (#2477)
* NVDA se više neće zamrzavati kada je pokrenut kao administrator dok kopira korisničku konfiguraciju u konfiguraciju sustava (za korištenje na Windows logiranju i drugim sigurnim zaslonima). (#2485)
* Pločice na početnom zaslonu sustava Windows 8 sada su bolje prikazane u govoru i Brailleovom pismu. Naziv se više ne ponavlja, neodabrano se više ne prijavljuje na svim pločicama, a informacije o statusu uživo prikazuju se kao opis pločice (npr. trenutna temperatura za pločicu Vrijeme).
* Lozinke se više ne najavljuju prilikom čitanja polja lozinki u programu Microsoft Outlook i drugim standardnim kontrolama za uređivanje koje su označene kao zaštićene. (#2021)
* U programu Adobe Reader promjene polja obrasca sada se ispravno odražavaju u načinu pregledavanja. (#2529)
* Poboljšanja podrške za Microsoft Word provjeru pravopisa, uključujući točnije čitanje trenutne pravopisne pogreške i mogućnost podrške za provjeru pravopisa prilikom pokretanja instalirane kopije NVDA uređaja u sustavu Windows Vista ili novijim.
* Dodaci koji sadrže datoteke koje sadrže znakove koji nisu na engleskom jeziku sada se mogu ispravno instalirati u većini slučajeva. (#2505)
* U programu Adobe Reader jezik teksta više se ne gubi kada se ažurira ili pomiče u. (#2544)
* Prilikom instaliranja dodatka, dijaloški okvir za potvrdu sada ispravno prikazuje lokalizirani naziv dodatka ako je dostupan. (#2422)
* U aplikacijama koje koriste automatizaciju korisničkog sučelja (kao što su .net i Silverlight aplikacije) ispravljen je izračun numeričkih vrijednosti za kontrole kao što su klizači. (#2417)
* Konfiguracija za izvještavanje o trakama napretka sada se poštuje za neodređene trake napretka koje NVDA prikazuje prilikom instalacije, stvaranja prijenosne kopije itd. (#2574)
* NVDA naredbe više se ne mogu izvršavati s Brailleovog pisma dok je aktivan siguran zaslon sustava Windows (kao što je zaključani zaslon). (#2449)
* U načinu pregledavanja, Brailleovo pismo se sada ažurira ako se tekst koji se prikazuje promijeni. (#2074)
* Kada su na sigurnom Windows zaslonu kao što je zaključani zaslon, poruke iz aplikacija koje govore ili prikazuju Brailleovo pismo izravno putem NVDA sada se zanemaruju.
* U načinu pregledavanja više nije moguće pasti s dna dokumenta tipkom sa strelicom udesno kada ste na završnom znaku ili skokom na kraj spremnika kada je taj spremnik posljednja stavka u dokumentu. (#2463)
* Vanjski sadržaj više nije pogrešno uključen prilikom prijavljivanja teksta dijaloških okvira u web aplikacijama (točnije, ARIA dijalozi bez atributa aria-describedby). (#2390)
* NVDA više ne izvještava ili locira određena polja za uređivanje u MSHTML dokumentima (npr. Internet Explorer), posebno tamo gdje je autor web stranice koristio eksplicitnu ARIA ulogu. (#2435)
* Tipka backspace sada se ispravno obrađuje prilikom izgovaranja upisanih riječi u naredbenim konzolama sustava Windows. (#2586)
* Koordinate ćelija u programu Microsoft Excel sada se ponovno prikazuju na Brailleovom pismu.
* U programu Microsoft Word NVDA vas više ne ostavlja zaglavljenim na odlomku s oblikovanjem popisa kada pokušavate prijeći preko grafičke oznake ili broja sa strelicom ulijevo ili kontrolom + strelicom ulijevo. (#2402)
* U načinu pregledavanja u Mozillinim aplikacijama, stavke u određenim okvirima popisa (točnije, ARIA okviri popisa) više se ne prikazuju pogrešno.
* U načinu pregledavanja u Mozillinim aplikacijama, određene kontrole koje su prikazane s netočnom oznakom ili samo razmakom sada se prikazuju s ispravnom oznakom.
* U načinu pregledavanja u Mozillinim aplikacijama, uklonjen je neki suvišni razmak.
* U načinu pregledavanja u web preglednicima, određene grafike koje su eksplicitno označene kao prezentacijske (točnije, s atributom alt="") sada se ispravno zanemaruju.
* U web preglednicima, NVDA sada skriva sadržaj koji je označen kao skriven od čitača zaslona (točnije, koristeći atribut aria-hidhid). (#2117)
* Negativni iznosi valute (npr. -123 USD) sada se ispravno izgovaraju kao negativni, bez obzira na razinu simbola. (#2625)
* Tijekom reci sve, NVDA se više neće pogrešno vraćati na zadani jezik gdje redak ne završava rečenicu. (#2630)
* Informacije o fontu sada su ispravno otkrivene u programu Adobe Reader 10.1 i novijim verzijama. (#2175)
* U programu Adobe Reader, ako je dostupan zamjenski tekst, prikazat će se samo taj tekst. Prije je ponekad bio uključen strani tekst. (#2174)
* Ako dokument sadrži aplikaciju, sadržaj aplikacije više nije uključen u način pregledavanja. To sprječava neočekivano kretanje unutar aplikacije tijekom navigacije. S aplikacijom možete komunicirati na isti način kao i s ugrađenim objektima. (#990)
* U Mozillinim aplikacijama, vrijednost gumba za okretanje sada se ispravno izvještava kada se promijeni. (#2653)
* Ažurirana podrška za Adobe Digital Editions tako da radi u verziji 2.0. (#2688)
* Pritiskom na NVDA+strelica prema gore dok ste na kombiniranom okviru u Internet Exploreru i drugim MSHTML dokumentima više nećete pogrešno čitati sve stavke. Umjesto toga, pročitat će se samo aktivna stavka. (#2337)
* Govorni rječnici sada će se ispravno spremati kada se koristi znak broja (#) unutar uzorka ili zamjenskih polja. (#961)
* Način pregledavanja za MSHTML dokumente (npr. Internet Explorer) sada ispravno prikazuje vidljivi sadržaj sadržan u skrivenom sadržaju (točnije, elemente sa stilom vidljivost:vidljivo unutar elementa sa stilom vidljivost:skriveno). (#2097)
* Veze u centru za sigurnost sustava Windows XP više ne prijavljuju nasumično neželjeno izdanje iza imena. (#1331)
* Kontrole teksta za automatizaciju korisničkog sučelja (npr.  polje za pretraživanje u izborniku Start sustava Windows 7) sada su ispravno najavljeni kada pomaknete miš preko njih, umjesto da šutite.
* Promjene rasporeda tipkovnice više se ne prijavljuju tijekom recimo sve, što je bilo posebno problematično za višejezične dokumente koji uključuju arapski tekst. (#1676)
* Cijeli sadržaj nekih tekstualnih kontrola koje se mogu uređivati automatizacijom korisničkog sučelja (npr. okvir za pretraživanje u izborniku Start sustava Windows 7/8) više se ne objavljuje svaki put kada se promijeni.
* Prilikom kretanja između grupa na početnom zaslonu sustava Windows 8 neoznačene grupe više ne objavljuju svoju prvu pločicu kao naziv grupe. (#2658)
* Prilikom otvaranja početnog zaslona sustava Windows 8, fokus je ispravno postavljen na prvu pločicu, umjesto da skočite na korijen početnog zaslona što može zbuniti navigaciju. (#2720)
* NVDA se više neće uspjeti pokrenuti kada put korisnikovog profila sadrži određene višebajtne znakove. (#2729)
* U načinu pregledavanja u pregledniku Google Chrome tekst kartica sada se ispravno prikazuje.
* U načinu pregledavanja, gumbi izbornika sada se ispravno prijavljuju.
* U OpenOffice.org/LibreOffice Calcu čitanje ćelija proračunske tablice sada radi ispravno. (#2765)
* NVDA ponovno može funkcionirati na popisu poruka Yahoo! Maila kada se koristi iz Internet Explorera. (#2780)

### Promjene za programere

* Prethodna datoteka dnevnika sada se kopira u nvda-old.log prilikom NVDA inicijalizacije. Stoga, ako se NVDA sruši ili ponovno pokrene, zapisivanje podataka iz te sesije i dalje je dostupno za pregled. (#916)
* Dohvaćanje svojstva role u chooseNVDAObjectOverlayClasses više ne uzrokuje da uloga bude netočna i stoga se ne prijavljuje u fokusu za određene objekte kao što su Windows naredbene konzole i Scintilla kontrole. (#2569)
* NVDA izbornici Preferences, Tools i Help sada su dostupni kao atributi na gui.mainFrame.sysTrayIcon pod nazivom preferencesMenu, toolsMenu i helpMenu, respektivno. To omogućuje dodacima da lakše dodaju stavke u ove izbornike.
* Skripta navigatorObject_doDefaultAction u globalCommands preimenovana je u review_activate.
* Sada su podržani konteksti za dobivanje tekstualne poruke. To omogućuje definiranje više prijevoda za jednu englesku poruku ovisno o kontekstu. (#1524)
 * To se radi pomoću funkcije pgettext(context, message).
 * Ovo je podržano i za sam NVDA i za dodatke.
 * xgettext i msgfmt iz GNU gettext-a moraju se koristiti za stvaranje bilo koje PO i MO datoteke. Python alati ne podržavaju kontekste poruka.
 * Za xgettext proslijedite argument naredbenog retka --keyword=pgettext:1c,2 da biste omogućili uključivanje konteksta poruka.
 * Pogledajte http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts za više informacija.
* Sada je moguće pristupiti ugrađenim NVDA modulima gdje su ih nadjačali moduli trećih strana. Za detalje pogledajte modul nvdaBuiltin.
* Podrška za prijevod dodataka sada se može koristiti unutar modula installTasks dodatka. (#2715)

## 2012.2.1

Ovo izdanje rješava nekoliko potencijalnih sigurnosnih problema (nadogradnjom Pythona na 2.7.3).

## 2012.2

Istaknuti dijelovi ovog izdanja uključuju ugrađeni instalacijski program i značajku stvaranja prijenosnih podataka, automatska ažuriranja, jednostavno upravljanje novim NVDA dodacima, najavu grafike u Microsoft Wordu, podršku za aplikacije u stilu Windows 8 Metro i nekoliko važnih ispravaka grešaka.

### Nove značajke

* NVDA sada može automatski provjeravati, preuzimati i instalirati ažuriranja. (#73)
* Proširenje NVDA funkcionalnosti olakšano je dodavanjem Upravitelja dodataka (koji se nalazi pod Alati u NVDA izborniku) koji vam omogućuje instaliranje i deinstaliranje novih NVDA paketa dodataka (.nvda-addon datoteke) koji sadrže dodatke i upravljačke programe. Imajte na umu da upravitelj dodataka ne prikazuje starije prilagođene dodatke i upravljačke programe ručno kopirane u vaš konfiguracijski direktorij. (#213)
* Mnoge druge uobičajene NVDA značajke sada rade u aplikacijama u stilu Windows 8 Metro kada se koristi instalirano izdanje NVDA-a, uključujući govor o upisanim znakovima i način pregledavanja web dokumenata (uključuje podršku za Metro verziju Internet Explorera 10). Prijenosne kopije NVDA ne mogu pristupiti aplikacijama u stilu metroa. (#1801)
* U načinu pregledavanja dokumenata (Internet Explorer, Firefox, itd.) sada možete skočiti na početak i kraj određenih elemenata koji sadrže (kao što su popisi i tablice) pomoću shift+, odnosno , respektivno. (#123)
* Novi jezik: grčki.
* Grafika i zamjenski tekst sada se prijavljuju u dokumentima programa Microsoft Word. (#2282, #1541)

### Promjenama

* Najava koordinata ćelija u programu Microsoft Excel sada je nakon sadržaja, a ne prije, a sada je uključena samo ako su postavke tablica izvješća i koordinata ćelija tablice izvješća omogućene u dijaloškom okviru Postavke oblikovanja dokumenta. (#320)
* NVDA se sada distribuira u jednom paketu. Umjesto odvojenih prijenosnih i instalacijskih verzija, sada postoji samo jedna datoteka koja će, kada se pokrene, pokrenuti privremenu kopiju NVDA i omogućiti vam da instalirate ili generirate prijenosnu distribuciju. (#1715)
* NVDA je sada uvijek instaliran u programskim datotekama na svim sustavima. Ažuriranje prethodne instalacije također će je automatski premjestiti ako prethodno nije bila tamo instalirana.

### Ispravci grešaka

* S omogućenom automatskom promjenom jezika, sadržaj kao što je zamjenski tekst za grafiku i oznake za druge određene kontrole u Mozilla Gecku (npr. Firefox) sada se prijavljuje na ispravnom jeziku ako je označen na odgovarajući način.
* SayAll u BibleSeekeru (i drugim TRxRichEdit kontrolama) više se ne zaustavlja usred odlomka.
* Popisi koji se nalaze u svojstvima datoteke programa Windows 8 Explorer (kartica dopuštenja) i na servisu Windows Update sustava Windows Update sada se ispravno čitaju.
* Ispravljena moguća zamrzavanja u MS Wordu koja bi nastala kada bi trebalo više od 2 sekunde za dohvaćanje teksta iz dokumenta (iznimno dugi redovi ili sadržaji). (#2191)
* Otkrivanje prijeloma riječi sada ispravno funkcionira tamo gdje nakon razmaka slijede određeni interpunkcijski znakovi. (#1656)
* U načinu pregledavanja u programu Adobe Reader sada je moguće navigirati do naslova bez razine pomoću brze navigacije i popisa elemenata. (#2181)
* U Winampu se brajica sada ispravno ažurira kada prijeđete na drugu stavku u uređivaču reprodukcijske liste. (#1912)
* Stablo na popisu elemenata (dostupno za dokumente u načinu pregledavanja) sada je odgovarajuće veličine za prikaz teksta svakog elementa. (#2276)
* U aplikacijama koje koriste Java Access Bridge, tekstna polja koja se mogu uređivati sada su ispravno prikazana na Brailleovom pismu. (#2284)
* U aplikacijama koje koriste java Access Bridge, tekstualna polja koja se mogu uređivati više ne prijavljuju čudne znakove u određenim okolnostima. (#1892)
* U aplikacijama koje koriste Java Access Bridge, kada je na kraju tekstnog polja koje se može uređivati, trenutni redak sada se ispravno prijavljuje. (#1892)
* U načinu pregledavanja u aplikacijama koje koriste Mozilla Gecko 14 i novije (npr. Firefox 14), brza navigacija sada radi za blokovske navodnike i ugrađene objekte. (#2287)
* U Internet Exploreru 9, NVDA više ne čita neželjeni sadržaj kada se fokus pomakne unutar određenih orijentira ili elemenata koji se mogu fokusirati (točnije, div element koji se može fokusirati ili ima ulogu ARIA orijentira).
* NVDA ikona za NVDA prečace za radnu površinu i izbornik Start sada se ispravno prikazuje u 64-bitnim izdanjima sustava Windows. (#354)

### Promjene za programere

* Zbog zamjene prethodnog NSIS instalacijskog programa za NVDA ugrađenim instalacijskim programom u Pythonu, prevoditelji više ne moraju održavati langstrings.txt datoteku za instalacijski program. Svim nizovima lokalizacije sada upravljaju gettext po datoteke.

## 2012.1

Istaknute značajke ovog izdanja uključuju značajke za tečnije čitanje Brailleovog pisma; naznaka oblikovanja dokumenta na Brailleovom pismu; pristup mnogo više informacija o oblikovanju i poboljšane performanse u programu Microsoft Word; i podrška za iTunes Store.

### Nove značajke

* NVDA može objaviti broj početnih kartica i razmaka trenutnog retka redoslijedom kojim su uneseni. To se može omogućiti odabirom uvlačenja retka izvješća u dijaloškom okviru za oblikovanje dokumenta. (#373)
* NVDA sada može detektirati pritiske tipki generirane alternativnom emulacijom unosa tipkovnice kao što su zaslonske tipkovnice i softver za prepoznavanje govora.
* NVDA sada može detektirati boje u Windows naredbenim konzolama.
* Podebljano, kurziv i podcrtano sada su označeni na Brailleovom pismu pomoću znakova koji odgovaraju konfiguriranoj tablici prijevoda. (#538)
* Mnogo više informacija sada se izvještava u dokumentima programa Microsoft Word, uključujući:
 * Umetnute informacije kao što su brojevi fusnota i krajnjih bilješki, razine naslova, postojanje komentara, razine ugniježđenja tablice, veze i boja teksta;
 * Izvješćivanje prilikom unosa odjeljaka dokumenta, kao što su članci komentara, bilješke i bilješke te članci zaglavlja i podnožja.
* Brajica sada označava odabrani tekst pomoću točaka 7 i 8. (#889)
* Brailleovo pismo sada izvještava o kontrolama unutar dokumenata kao što su veze, gumbi i naslovi. (#202)
* Podrška za hedo ProfiLine i MobilLine USB brajevo pismo. (#1863, #1897)
* NVDA sada izbjegava dijeljenje riječi na Brailleovom pismu kada je to moguće prema zadanim postavkama. To se može onemogućiti u dijaloškom okviru Postavke Brailleovog pisma. (#1890, #1946)
* Sada je moguće prikazati Brailleovo pismo u odlomcima umjesto u redovima, što može omogućiti tečnije čitanje velikih količina teksta. To se može konfigurirati pomoću mogućnosti Čitanje po odlomcima u dijaloškom okviru Postavke brajice. (#1891)
* U načinu pregledavanja možete aktivirati objekt ispod pokazivača pomoću brajičnog zaslona. To se postiže pritiskom na tipku za usmjeravanje kursora na mjestu gdje se kursor nalazi (što znači da ga dvaput pritisnete ako kursor već nije tamo). (#1893)
* Osnovna podrška za web-područja u programu iTunes kao što je trgovina. Druge aplikacije koje koriste WebKit 1 također mogu biti podržane. (#734)
* U knjigama u Adobe Digital Editions 1.8.1 i novijim verzijama, stranice se sada automatski okreću kada se koristi Reci sve. (#1978)
* Nove tablice za prijevod Brailleovog pisma: portugalski razred 2, islandski računalni braille s 8 točaka, tamilski stupanj 1, španjolski računalni braille s 8 točaka, farsi razred 1. (#2014)
* Sada možete konfigurirati hoće li se okviri u dokumentima izvještavati iz dijaloškog okvira preferenci oblikovanja dokumenta. (#1900)
* Stanje mirovanja automatski se omogućuje kada koristite OpenBook. (#1209)
* U Poeditu prevoditelji sada mogu čitati dodane i automatski izdvojene komentare prevoditelja. Poruke koje nisu prevedene ili nejasne označene su zvjezdicom i čuje se zvučni signal kada prijeđete na njih. (#1811)
* Podrška za zaslone serije HumanWare Brailliant BI i B. (#1990)
* Novi jezici: norveški bokmål, tradicionalni kineski (Hong Kong).

### Promjenama

* Naredbe za opisivanje trenutnog znaka ili za sricanje trenutne riječi ili retka sada će se pisati na odgovarajućem jeziku u skladu s tekstom, ako je uključeno automatsko prebacivanje jezika i dostupne su odgovarajuće informacije o jeziku.
* Ažuriran eSpeak sintetizator govora na 1.46.02.
* NVDA će sada skratiti iznimno dugačka (30 znakova ili više) imena pogodena iz grafičkih URL-ova i URL-ova poveznica jer su to najvjerojatnije smeće koje smeta čitanju. (#1989)
* Neke informacije prikazane na Brailleovom pismu skraćene su. (#1955, #2043)
* Kada se kursor za kursor ili kursor za pregled pomiče, Brailleovo pismo se sada pomiče na isti način kao i kada se ručno pomiče. Zbog toga je prikladnija kada je Brailleovo pismo konfigurirano za čitanje po odlomcima i/ili izbjegavanje razdvajanja riječi. (#1996)
* Ažurirano na novu tablicu za prijevod španjolskog Brailleovog pisma 1. razreda.
* Ažuriran prevoditelj brajice liblouis na 2.4.1.

### Ispravci grešaka

* U sustavu Windows 8 fokus se više ne pomiče pogrešno od polja za pretraživanje Windows Explorera, što nije dopuštalo NVDA-u interakciju s njim.
* Velika poboljšanja performansi pri čitanju i navigaciji Microsoft Word dokumentima dok je omogućeno automatsko izvješćivanje o oblikovanju, što sada čini prilično ugodnim za provjeru čitanja, formatiranje itd. Performanse također mogu biti poboljšane za neke korisnike.
* Način pregledavanja sada se koristi za Adobe Flash sadržaj preko cijelog zaslona.
* Ispravljena je loša kvaliteta zvuka u nekim slučajevima kada se koriste glasovi Microsoft Speech API-ja verzije 5 s izlaznim audio uređajem postavljenim na nešto drugo osim zadanog (Microsoft Sound Mapper). (#749)
* Opet dopustite korištenje NVDA sa sintisajzerom "bez govora", oslanjajući se isključivo na Brailleovo pismo ili preglednik govora. (#1963)
* Naredbe za navigaciju objektima više ne prijavljuju "Nema djece" i "Nema roditelja", već umjesto toga izvještavaju o porukama u skladu s dokumentacijom.
* Kada je NVDA konfiguriran za korištenje jezika koji nije engleski, naziv tipke tabulatora sada se prijavljuje na ispravnom jeziku.
* U Mozilla Gecko (npr. Firefox), NVDA se više ne prebacuje povremeno u način pregledavanja tijekom navigacije izbornicima u dokumentima. (#2025)
* U Kalkulatoru tipka za povratni prostor sada izvještava o ažuriranom rezultatu umjesto da ne prijavljuje ništa. (#2030)
* U načinu pregledavanja, naredba za pomicanje miša na trenutni objekt navigatora sada usmjerava do središta objekta na kursoru za pregled umjesto u gornjem lijevom kutu, što je čini preciznijom u nekim slučajevima. (#2029)
* U načinu pregledavanja s omogućenim automatskim načinom fokusiranja za promjene fokusa, fokusiranje na alatnoj traci sada će se prebaciti u način fokusiranja. (#1339)
* Naredba naslova izvješća ponovno ispravno funkcionira u programu Adobe Reader.
* S omogućenim automatskim načinom fokusiranja za promjene fokusa, način fokusiranja sada se ispravno koristi za fokusirane ćelije tablice; npr. u mrežama ARIA-e. (#1763)
* U programu iTunes informacije o položaju na određenim popisima sada se ispravno prijavljuju.
* U programu Adobe Reader neke se veze više ne tretiraju kao da sadrže tekstualna polja koja se mogu uređivati samo za čitanje.
* Oznake nekih tekstnih polja koja se mogu uređivati više nisu pogrešno uključene prilikom izvješćivanja o tekstu dijaloškog okvira. (#1960)
* Opis grupiranja ponovno se prijavljuje ako je omogućeno izvješćivanje o opisima objekata.
* Veličine čitljive ljudima sada su uključene u tekst dijaloškog okvira svojstava pogona programa Windows Explorer.
* Dvostruko izvješćivanje o tekstu stranice entiteta u nekim je slučajevima potisnuto. (#218)
* Poboljšano praćenje kursora u tekstnim poljima koja se mogu uređivati i koja se oslanjaju na tekst napisan na zaslonu. To posebno poboljšava uređivanje u uređivaču ćelija Microsoft Excel i uređivaču poruka Eudora. (#1658)
* U Firefoxu 11, prelazak na naredbu za sadržavanje virtualnog međuspremnika (NVDA+kontrola+razmak) sada radi kako bi trebao pobjeći od ugrađenih objekata kao što je Flash sadržaj.
* NVDA se sada ispravno ponovno pokreće (npr. nakon promjene konfiguriranog jezika) kada se nalazi u direktoriju koji sadrži znakove koji nisu ASCII. (#2079)
* Brailleovo pismo ispravno poštuje postavke za izvješćivanje o tipkama prečaca objekata, informacijama o položaju i opisima.
* U Mozillinim aplikacijama prebacivanje između načina pregledavanja i fokusiranja više nije sporo s omogućenom Brailleovom žicom. (#2095)
* Usmjeravanje kursora na razmak na kraju retka/odlomka pomoću tipki za usmjeravanje kursora na Brailleovom pismu u nekim tekstnim poljima koja se mogu uređivati sada ispravno funkcionira umjesto usmjeravanja na početak teksta. (#2096)
* NVDA ponovno radi ispravno s Audiologic Tts3 sintisajzerom. (#2109)
* Microsoft Word dokumenti ispravno se tretiraju kao višeredni. To uzrokuje da se Brailleovo pismo ponaša prikladnije kada je dokument fokusiran.
* U pregledniku Microsoft Internet Explorer pogreške se više ne pojavljuju kada se usredotočite na određene rijetke kontrole. (#2121)
* Promjena izgovora interpunkcijskih znakova od strane korisnika sada će odmah stupiti na snagu, umjesto da se zahtijeva ponovno pokretanje NVDA-a ili onemogućavanje automatske promjene jezika.
* Kada koristite eSpeak, govor više ne utišava u nekim slučajevima u dijaloškom okviru Spremi kao NVDA preglednika dnevnika. (#2145)

### Promjene za programere

* Sada postoji udaljena Python konzola za situacije u kojima je daljinsko otklanjanje pogrešaka korisno. Pojedinosti potražite u Vodiču za razvojne programere.
* Osnovni put NVDA-inog koda sada je uklonjen iz tragova u dnevniku kako bi se poboljšala čitljivost. (#1880)
* Objekti TextInfo sada imaju metodu activate() za aktiviranje položaja koji predstavlja TextInfo.
 * To koristi Brailleovo pismo za aktiviranje položaja pomoću tipki za usmjeravanje kursora na Brailleovom pismu. Međutim, u budućnosti bi moglo biti i drugih pozivatelja.
* TreeInterceptors i NVDAObjects koji istovremeno izlažu samo jednu stranicu teksta mogu podržavati automatsko okretanje stranica tijekom recimo svega pomoću miješanja textInfos.DocumentWithPageTurns. (#1978)
* Nekoliko kontrolnih i izlaznih konstanti preimenovano je ili premješteno. (#228)
 * govor. REASON_* konstante premještene su u controlTypes.
 * U controlTypes, speechRoleLabels i speechStateLabels preimenovani su samo u roleLabels i stateLabels.
* Izlaz Brailleovog pisma sada se bilježi na razini ulaza/izlaza. Prvo se bilježi neprevedeni tekst svih regija, a zatim se prikazuju ćelije brajice prozora. (#2102)
* podklase sapi5 synthDriver sada mogu nadjačati _getVoiceTokens i proširiti init kako bi podržali prilagođene glasovne tokene kao što je sapi.spObjectTokenCategory za dobivanje tokena s prilagođene lokacije registra.

## 2011.3

Istaknuti dijelovi ovog izdanja uključuju automatsko prebacivanje jezika govora prilikom čitanja dokumenata s odgovarajućim jezičnim informacijama; podrška za 64-bitna Java Runtime okruženja; izvještavanje o oblikovanju teksta u načinu pregledavanja u Mozillinim aplikacijama; bolje rukovanje padovima i zamrzavanjem aplikacija; i početni popravci za Windows 8.

### Nove značajke

* NVDA sada može mijenjati jezik eSpeak sintisajzera u hodu prilikom čitanja određenih web/pdf dokumenata s odgovarajućim jezičnim informacijama. Automatsko prebacivanje jezika/dijalekta može se uključiti i isključiti iz dijaloškog okvira Glasovne postavke. (#845)
* Sada je podržan Java Access Bridge 2.0.2, koji uključuje podršku za 64-bitna Java Runtime okruženja.
* U Mozilla Gecku (npr. Firefoxu) razine naslova sada se najavljuju kada se koristi navigacija objektima.
* Formatiranje teksta sada se može prijaviti kada koristite način pregledavanja u Mozilla Gecko (npr. Firefox i Thunderbird). (#394)
* Tekst s podcrtavanjem i/ili precrtavanjem sada se može otkriti i prijaviti u standardnim kontrolama teksta IAccessible2, kao što su Mozilla aplikacije.
* U načinu pregledavanja u programu Adobe Reader sada se izvješćuje o broju redaka i stupaca tablice.
* Dodana je podrška za sintetizator Microsoft Speech Platform. (#1735)
* Brojevi stranica i redaka sada su prijavljeni za kursor u IBM Lotus Symphony. (#1632)
* Postotak promjene visine tona prilikom izgovaranja velikog slova sada se može konfigurirati iz dijaloškog okvira postavki glasa. Međutim, ovo zamjenjuje stariji potvrdni okvir za povećanje visine za velika slova (stoga za isključivanje ove značajke postavite postotak na 0). (#255)
* Boja teksta i pozadine sada su uključeni u izvješćivanje o oblikovanju ćelija u programu Microsoft Excel. (#1655)
* U aplikacijama koje koriste Java Access Bridge, naredba aktiviraj trenutni objekt navigatora sada radi na kontrolama gdje je to prikladno. (#1744)
* Novi jezik: tamilski.
* Osnovna podrška za Design Science MathPlayer.

### Promjenama

* NVDA će se sada ponovno pokrenuti ako se sruši.
* Neke informacije prikazane na Brailleovom pismu skraćene su. (#1288)
* skripta za čitanje aktivnog prozora (NVDA+b) je poboljšana kako bi se filtrirale nekorisne kontrole, a sada je i mnogo lakše utišati. (#1499)
* Automatsko izgovaranje svih prilikom učitavanja dokumenta u načinu pregledavanja sada je opcionalno putem postavke u dijaloškom okviru postavki načina pregledavanja. (#414)
* Prilikom pokušaja čitanja statusne trake (Desktop NVDA+end), ako se stvarni objekt statusne trake ne može locirati, NVDA će umjesto toga pribjeći korištenju donjeg retka teksta zapisanog na zaslonu aktivne aplikacije. (#649)
* Kada čitate s recimo sve u dokumentima u načinu pregledavanja, NVDA će sada pauzirati na kraju naslova i drugih elemenata na razini bloka, umjesto da izgovara tekst zajedno sa sljedećom serijom teksta kao jednu dugu rečenicu.
* U načinu pregledavanja, pritiskom na enter ili razmak na kartici sada se aktivira umjesto prebacivanja u način fokusiranja. (#1760)
* Ažuriran eSpeak sintetizator govora na 1.45.47.

### Ispravci grešaka

* NVDA više ne prikazuje grafičke oznake ili numeriranje popisa u Internet Exploreru i drugim MSHTML kontrolama kada je autor naznačio da se one ne smiju prikazivati (npr. stil popisa je "none"). (#1671)
* Ponovno pokretanje NVDA kada se zamrzne (npr. pritiskom na control+alt+n) više ne izlazi iz prethodne kopije bez pokretanja nove.
* Pritiskanje backspacea ili tipki sa strelicama u naredbenoj konzoli sustava Windows u nekim slučajevima više ne uzrokuje čudne rezultate. (#1612)
* Odabrana stavka u WPF kombiniranim okvirima (i možda nekim drugim kombiniranim okvirima izloženim pomoću automatizacije korisničkog sučelja) koja ne dopušta uređivanje teksta sada se ispravno prijavljuje.
* U načinu pregledavanja u Adobe Readeru sada je uvijek moguće prijeći na sljedeći redak iz retka zaglavlja i obrnuto pomoću naredbi za premještanje na sljedeći redak i prelazak na prethodni redak. Također, redak zaglavlja više se ne prijavljuje kao redak 0. (#1731)
* U načinu pregledavanja u programu Adobe Reader sada je moguće premjestiti se u prazne ćelije u tablici (a time i prijeći).
* Besmislene informacije o položaju (npr. 0 od 0, razina 0) više se ne prikazuju na Brailleovom pismu.
* Kada je Brailleovo pismo vezano za pregled, sada može prikazati sadržaj u plošnom pregledu. (#1711)
* Tekst kontrole teksta više se ne prikazuje dvaput na Brailleovom pismu u nekim slučajevima, npr. pomicanje unatrag od početka dokumenata programa Wordpad.
* U načinu pregledavanja u pregledniku Internet Explorer pritiskom na enter na gumbu za prijenos datoteke sada se ispravno prikazuje dijaloški okvir za odabir datoteke za prijenos umjesto prebacivanja u način fokusiranja. (#1720)
* Promjene dinamičkog sadržaja, kao što su Dos konzole, više se ne najavljuju ako je trenutno uključen način mirovanja za tu aplikaciju. (#1662)
* U načinu pregledavanja poboljšano je ponašanje alt+strelica prema gore i alt+strelica prema dolje za sažimanje i proširenje kombiniranih okvira. (#1630)
* NVDA se sada oporavlja od mnogo više situacija kao što su aplikacije koje prestaju reagirati što je prethodno uzrokovalo potpuno zamrzavanje. (#1408)
* Za Mozilla Gecko (Firefox itd.) dokumente u načinu pregledavanja, NVDA više neće uspjeti prikazati tekst u vrlo specifičnoj situaciji kada je element stiliziran kao display:table. (#1373)
* NVDA više neće najavljivati kontrole naljepnica kada se fokus pomakne unutar njih. Zaustavlja dvostruke najave oznaka za neka polja obrazaca u Firefoxu (Gecko) i Internet Exploreru (MSHTML). (#1650)
* NVDA više ne uspijeva čitati ćeliju u Microsoft Excelu nakon što je zalijepi u nju pomoću control+v. (#1781)
* U programu Adobe Reader suvišne informacije o dokumentu više se ne objavljuju prilikom prelaska na kontrolu na drugoj stranici u načinu rada fokusa. (#1659)
* U načinu pregledavanja u aplikacijama Mozilla Gecko (npr. Firefox), preklopni gumbi sada se otkrivaju i ispravno prijavljuju. (#1757)
* NVDA sada može ispravno čitati adresnu traku Windows Explorera u Windows 8 Developer Previewu.
* NVDA više neće rušiti aplikacije kao što su winver i wordpad u Windows 8 Developer Preview zbog loših prijevoda glifa.
* U načinu pregledavanja u aplikacijama koje koriste Mozilla Gecko 10 i novije (npr. Firefox 10), kursor se češće ispravno postavlja prilikom učitavanja stranice s ciljnim sidrom. (#360)
* U načinu pregledavanja u aplikacijama Mozilla Gecko (npr. Firefox), oznake za slikovne karte sada se prikazuju.
* Kada je omogućeno praćenje miša, pomicanje miša preko određenih tekstnih polja koja se mogu uređivati (kao što su postavke uređaja za pokazivanje Synaptics i SpeechLab SpeakText) više ne uzrokuje rušenje aplikacije. (#672)
* NVDA sada ispravno funkcionira u nekoliko dijaloških okvira u aplikacijama koje se distribuiraju sa sustavom Windows XP, uključujući dijaloški okvir O nama u Notepadu i dijaloški okvir O sustavu Windows. (#1853, #1855)
* Riješeno pregledavanje riječi u kontrolama uređivanja sustava Windows. (#1877)
* Izlazak iz tekstualnog polja koje se može uređivati pomoću lijeve strelice, strelice prema gore ili pageUp u načinu rada fokusa sada se ispravno prebacuje u način pregledavanja kada je omogućen automatski način fokusiranja za pomicanje kursora. (#1733)

### Promjene za programere

* NVDA sada može uputiti sintisajzere govora da promijene jezike za određene dijelove govora.
 * Da bi to podržali, vozači moraju upravljati govorom. LangChangeCommand u sekvencama koje su prošle do SynthDriver.speak().
 * Objekti SynthDriver također bi trebali pružiti argument jezika objektima VoiceInfo (ili nadjačati atribut jezika za dohvaćanje trenutnog jezika). U suprotnom će se koristiti jezik korisničkog sučelja NVDA.

## 2011.2

Istaknute značajke ovog izdanja uključuju velika poboljšanja u vezi s interpunkcijom i simbolima, uključujući podesive razine, prilagođene oznake i opise znakova; nema pauza na kraju redaka tijekom reci sve; poboljšana podrška za ARIA u Internet Exploreru; bolja podrška za XFA/LiveCycle PDF dokumente u Adobe Readeru; pristup tekstu napisanom na zaslonu u više aplikacija; i pristup formatiranju i informacijama o boji za tekst upisan na zaslon.

### Nove značajke

* Sada je moguće čuti opis za bilo koji lik pritiskom na skriptu pregleda trenutnog lika dva puta u brzom slijedu.  Za engleske znakove ovo je standardna engleska fonetska abeceda. Za piktografske jezike kao što je tradicionalni kineski naveden je jedan ili više primjera fraza koje koriste zadani simbol. Također pritiskom na pregled trenutne riječi ili pregled trenutnog retka tri puta napisat će riječ/redak koristeći prvi od ovih opisa. (#55)
* Više teksta može se vidjeti u ravnom pregledu za aplikacije kao što je Mozilla Thunderbird koje svoj tekst pišu izravno na zaslon kao glifi.
* Sada je moguće birati između nekoliko razina interpunkcije i najave simbola. (#332)
* Kada se interpunkcijski znakovi ili drugi simboli ponavljaju više od četiri puta, sada se najavljuje broj ponavljanja umjesto izgovaranja ponavljajućih simbola. (#43)
* Nove tablice za prevođenje Brailleovog pisma: Norveški računalni Braille s 8 točaka, etiopski razred 1, slovenski razred 1, srpski razred 1. (#1456)
* Govor više ne pauzira neprirodno na kraju svakog retka kada koristite naredbu say all. (#149)
* NVDA će sada objaviti je li nešto sortirano (prema svojstvu aria-sort) u web preglednicima. (#1500)
* Unicode Brailleovi uzorci sada se ispravno prikazuju na Brailleovim pismima. (#1505)
* U Internet Exploreru i drugim MSHTML kontrolama kada se fokus pomakne unutar grupe kontrola (okruženih skupom polja), NVDA će sada objaviti naziv grupe (legendu). (#535)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama sada se poštuju svojstva aria-labelledBy i aria-describedBy.
* u Internet Exploreru i drugim MSHTML kontrolama poboljšana je podrška za ARIA popis, gridcell, klizač i kontrole trake napretka.
* Korisnici sada mogu promijeniti izgovor interpunkcijskih znakova i drugih simbola, kao i razinu simbola na kojoj se izgovaraju. (#271, #1516)
* U programu Microsoft Excel naziv aktivnog lista sada se prijavljuje prilikom prebacivanja listova pomoću control+pageUp ili control+pageDown. (#760)
* Kada se krećete po tablici u Microsoft Wordu pomoću tipke tabulatora, NVDA će sada najaviti trenutnu ćeliju dok se krećete. (#159)
* Sada možete konfigurirati hoće li se koordinate ćelija tablice izvještavati u dijaloškom okviru Preference oblikovanja dokumenta. (#719)
* NVDA sada može detektirati formatiranje i boju teksta upisanog na zaslon.
* Na popisu poruka Outlook Express/Windows Mail/Windows Live Mail, NVDA će sada objaviti činjenicu da je poruka nepročitana i je li proširena ili sažeta u slučaju niza razgovora. (#868)
* eSpeak sada ima postavku povećanja brzine koja utrostručuje brzinu govora.
* Podrška za kontrolu kalendara koja se nalazi u dijaloškom okviru Informacije o datumu i vremenu kojem se pristupa sa sata sustava Windows 7. (#1637)
* Dodana su dodatna povezivanja tipki za MDV Lilli Brailleov redak. (#241)
* Novi jezici: bugarski, albanski.

### Promjenama

* Da biste premjestili kursor za pregled, sada pritisnite fokus za premještanje fokusa na skriptu objekta navigatora (desktop NVDA+shift+numpadMinus, laptop NVDA+shift+backspace) dva puta u brzom slijedu. Time se oslobađa više tipki na tipkovnici. (#837)
* Da biste čuli decimalni i heksadecimalni prikaz znaka ispod kursora za pregled, sada pritisnite pregled trenutnog znaka tri puta, a ne dvaput, jer dva puta sada izgovara opis znaka.
* Ažuriran eSpeak sintetizator govora na 1.45.03. (#1465)
* Tablice izgleda više se ne najavljuju u aplikacijama Mozilla Gecko dok pomičete fokus u načinu fokusiranja ili izvan dokumenta.
* U pregledniku Internet Explorer i drugim MSHTML kontrolama, način pregledavanja sada radi za dokumente unutar ARIA aplikacija. (#1452)
* Ažuriran prevoditelj brajevog pisma na 2.3.0.
* Kada ste u načinu pregledavanja i prijeđete na kontrolu s brzom navigacijom ili fokusom, sada se najavljuje opis kontrole ako je ima.
* Trake napretka sada se najavljuju u načinu rada obrva.
* Čvorovi označeni ARIA ulogom prezentacije u pregledniku Internet Explorer i drugim MSHTML kontrolama sada se filtriraju iz jednostavnog pregleda i podrijetla fokusa.
* NVDA-ino korisničko sučelje i dokumentacija sada se odnose na virtualne međuspremnike kao način pregledavanja, jer je izraz "virtualni međuspremnik" prilično besmislen za većinu korisnika. (#1509)
* Kada korisnik želi kopirati svoje korisničke postavke u profil sustava za korištenje na zaslonu za prijavu itd., a njegove postavke sadrže prilagođene dodatke, sada je upozoren da bi to mogao predstavljati sigurnosni rizik. (#1426)
* NVDA usluga više ne pokreće i ne zaustavlja NVDA na radnim površinama s korisničkim unosom.
* U sustavima Windows XP i Windows Vista, NVDA više ne koristi automatizaciju korisničkog sučelja čak i ako je dostupna putem ažuriranja platforme. Iako korištenje automatizacije korisničkog sučelja može poboljšati pristupačnost nekih modernih aplikacija, na XP-u i Visti bilo je previše zamrzavanja, padova i gubitka performansi tijekom korištenja. (#1437)
* U aplikacijama koje koriste Mozilla Gecko 2 i novije (kao što su Firefox 4 i noviji), dokument se sada može čitati u načinu pregledavanja prije nego što se u potpunosti završi s učitavanjem.
* NVDA sada objavljuje stanje spremnika kada se fokus pomakne na kontrolu unutar njega (npr. ako se fokus pomakne unutar dokumenta koji se još uvijek učitava, prijavit će ga kao zauzet).
* NVDA-ino korisničko sučelje i dokumentacija više ne koriste izraze "prvi potomak" i "roditelj" u odnosu na navigaciju objektima, jer su ti pojmovi zbunjujući za mnoge korisnike.
* Sažeto se više ne prijavljuje za neke stavke izbornika koje imaju podizbornike.
* Skripta reportCurrentFormatting (NVDA+f) sada izvještava o oblikovanju na položaju kursora pregleda, a ne na kursoru / fokusu sustava. Budući da prema zadanim postavkama kursor pregleda slijedi kursor, većina ljudi ne bi trebala primijetiti razliku. Međutim, to sada omogućuje korisniku da sazna oblikovanje prilikom pomicanja kursora pregleda, kao što je u ravnom pregledu.

### Ispravci grešaka

* Slaganje kombiniranih okvira u dokumentima u načinu pregledavanja kada je način fokusiranja forsiran s NVDA+razmakom više se ne prebacuje automatski natrag u način pregledavanja. (#1386)
* U Gecko (npr. Firefox) i MSHTML (npr. Internet Explorer) dokumentima, NVDA sada ispravno renderira određeni tekst u istom retku koji je prethodno bio prikazan u zasebnim redovima. (#1378)
* Kada je Brailleovo pismo vezano za pregled, a objekt navigatora premješten u dokument načina pregledavanja, bilo ručno ili zbog promjene fokusa, Brailleovo pismo će na odgovarajući način prikazati sadržaj načina pregledavanja. (#1406, #1407)
* Kada je interpunkcija onemogućena, određena interpunkcija više nije pogrešno izgovorena kada se koriste neki sintetizatori. (#332)
* Problemi se više ne javljaju prilikom učitavanja konfiguracije za sintetizatore koji ne podržavaju glasovnu postavku, kao što je Audiologic Tts3. (#1347)
* Izbornik Skype Extras sada se ispravno čita. (#648)
* Potvrdivanje okvira Glasnoća kontrola svjetline u dijaloškom okviru Postavke miša više ne bi trebalo uzrokovati veliko kašnjenje zvučnih signala prilikom pomicanja miša po zaslonu u sustavu Windows Vista/Windows 7 s omogućenom značajkom Aero. (#1183)
* Kada je NVDA konfiguriran za korištenje rasporeda tipkovnice prijenosnog računala, NVDA+delete sada radi kao što je dokumentirano za izvještavanje o dimenzijama trenutnog objekta navigatora. (#1498)
* NVDA sada prikladno poštuje atribut koji je odabrao aria u dokumentima Internet Explorera.
* Kada se NVDA automatski prebaci u način fokusiranja u dokumentima u načinu pregledavanja, sada objavljuje informacije o kontekstu fokusa. Na primjer, ako stavka okvira s popisom dobije fokus, okvir s popisom bit će najavljen prvi. (#1491)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama ARIA kontrole okvira s popisom sada se postavljaju kao popisi, a ne kao stavke popisa.
* Kada kontrola teksta koja se može uređivati samo za čitanje dobije fokus, NVDA sada izvještava da je samo za čitanje. (#1436)
* U načinu pregledavanja, NVDA se sada ispravno ponaša u odnosu na tekstualna polja koja se mogu uređivati samo za čitanje.
* U dokumentima u načinu pregledavanja, NVDA se više ne prebacuje pogrešno iz fokusa kada je podešena aria-activedescendant; npr. kada se popis dovršetka pojavio u nekim kontrolama automatskog dovršavanja.
* U programu Adobe Reader, nazivi kontrola sada se prijavljuju prilikom pomicanja fokusa ili korištenja brze navigacije u načinu pregledavanja.
* U XFA PDF dokumentima u programu Adobe Reader, gumbi, veze i grafike sada se ispravno prikazuju.
* U XFA PDF dokumentima u Adobe Readeru svi se elementi sada prikazuju u zasebnim linijama. Ova promjena je napravljena jer su se veliki dijelovi (ponekad čak i cijeli dokument) prikazivali bez prekida zbog općeg nedostatka strukture u tim dokumentima.
* Riješeni su problemi pri premještanju fokusa na ili s tekstualnih polja koja se mogu uređivati u XFA PDF dokumentima u programu Adobe Reader.
* U XFA PDF dokumentima u programu Adobe Reader sada će se izvještavati o promjenama vrijednosti fokusiranog kombiniranog okvira.
* Kombinirani okviri koje su nacrtali vlasnici, kao što su oni za odabir boja u programu Outlook Express, sada su dostupni uz NVDA. (#1340)
* U jezicima koji koriste razmak kao grupu znamenki/razdjelnik tisuća, kao što su francuski i njemački, brojevi iz zasebnih dijelova teksta više se ne izgovaraju kao jedan broj. To je bilo posebno problematično za ćelije tablice koje sadrže brojeve. (#555)
* čvorovi s ARIA ulogom opisa u pregledniku Internet Explorer i drugim MSHTML kontrolama sada se klasificiraju kao statični tekst, a ne polja za uređivanje.
* Riješeni su razni problemi prilikom pritiskanja tabulatora dok je fokus na dokumentu u načinu pregledavanja (npr. kartica se neprimjereno premješta u adresnu traku u pregledniku Internet Explorer). (#720, #1367)
* Prilikom unosa popisa tijekom čitanja teksta, NVDA sada kaže, na primjer, "popis s 5 stavki" umjesto "popis s 5 stavki". (#1515)
* U načinu pomoći za unos, geste se bilježe čak i ako njihove skripte zaobilaze pomoć za unos kao što su naredbe za pomicanje brajice naprijed i natrag.
* U načinu pomoći za unos, kada se modifikator drži pritisnutim na tipkovnici, NVDA više ne izvještava o modifikatoru kao da se mijenja; npr. NVDA+NVDA.
* U dokumentima programa Adobe Reader sada funkcionira pritisak na c ili shift+c za navigaciju do kombiniranog okvira.
* Odabrano stanje redaka tablice koje se mogu odabrati sada se prijavljuje na isti način kao i za stavke prikaza popisa i stabla.
* Kontrole u Firefoxu i drugim Gecko aplikacijama sada se mogu aktivirati dok su u načinu pregledavanja, čak i ako je njihov sadržaj prebačen izvan zaslona. (#801)
* Više ne možete prikazivati dijaloški okvir NVDA postavki dok se prikazuje dijaloški okvir s porukom, jer je dijaloški okvir postavki u ovom slučaju zamrznut. (#1451)
* U programu Microsoft Excel više nema kašnjenja prilikom držanja ili brzog pritiskanja tipki za kretanje između ćelija ili odabir ćelija.
* Ispravljeni su povremeni padovi NVDA servisa što je značilo da je NVDA prestao raditi na sigurnim Windows zaslonima.
* Riješeni su problemi koji su se ponekad pojavljivali na zaslonima brajice kada je promjena uzrokovala nestanak teksta koji se prikazuje. (#1377)
* Prozor za preuzimanje u Internet Exploreru 9 sada se može kretati i čitati pomoću NVDA. (#1280)
* Više nije moguće slučajno pokrenuti više kopija NVDA uređaja u isto vrijeme. (#507)
* Na sporim sustavima, NVDA više ne uzrokuje neprimjereno prikazivanje glavnog prozora cijelo vrijeme dok radi. (#726)
* NVDA se više ne ruši u sustavu Windows xP prilikom pokretanja WPF aplikacije. (#1437)
* Reci sve i reci sve s pregledom sada mogu raditi u tekstualnim kontrolama za automatizaciju korisničkog sučelja koje podržavaju sve potrebne funkcionalnosti. Na primjer, sada možete koristiti Recimo sve s pregledom na dokumentima XPS Viewer.
* NVDA više ne klasificira neke stavke popisa u Outlook Express / Windows Live Mail pravilima za poruke Primijeni sada kao potvrdne okvire. (#576)
* Kombinirani okviri više se ne prijavljuju kao da imaju podizbornik.
* NVDA sada može čitati prijemnike u poljima Za, CC i BCC u Microsoft Outlooku. (#421)
* Riješen je problem u NVDA dijaloškom okviru Glasovne postavke gdje se vrijednost klizača ponekad nije prijavljivala kada se mijenja. (#1411)
* NVDA više ne propušta najavljivati novu ćeliju prilikom premještanja u Excel proračunskoj tablici nakon izrezivanja i lijepljenja. (#1567)
* NVDA više ne postaje lošiji u pogađanju imena boja što više boja najavljuje.
* U Internet Exploreru i drugim MSHTML kontrolama ispravljena je nemogućnost čitanja dijelova rijetkih stranica koje sadrže iframe označene ARIA ulogom prezentacije. (#1569)
* U Internet Exploreru i drugim MSHTML kontrolama riješen je rijedak problem zbog kojeg se fokus nastavio beskonačno pomicati između dokumenta i tekstnog polja koje se može uređivati u više redaka u načinu fokusa. (#1566)
* U programu Microsoft Word 2010 NVDA će sada automatski čitati dijaloške okvire za potvrdu. (#1538)
* U tekstnim poljima koja se mogu uređivati u više redaka u pregledniku Internet Explorer i drugim MSHTML kontrolama, odabir u recima nakon prvog sada se ispravno prijavljuje. (#1590)
* Poboljšano pomicanje po riječi u mnogim slučajevima, uključujući način pregledavanja i kontrole uređivanja sustava Windows. (#1580)
* NVDA instalacijski program više ne prikazuje iskrivljeni tekst za hongkonške verzije sustava Windows Vista i Windows 7. (#1596)
* NVDA više ne uspijeva učitati sintisajzer Microsoft Speech API-ja verzije 5 ako konfiguracija sadrži postavke za taj sintisajzer, ali nedostaje glasovna postavka. (#1599)
* U tekstnim poljima koja se mogu uređivati u Internet Exploreru i drugim MSHTML kontrolama, NVDA više ne zaostaje ili se zamrzava kada je omogućena brajica.
* U Firefox modu pregleda, NVDA više ne odbija uključiti sadržaj koji se nalazi unutar čvora koji se može fokusirati s ARIA ulogom prezentacije.
* U programu Microsoft Word s omogućenom brajicom, redovi na stranicama nakon prve stranice sada se ispravno prijavljuju. (#1603)
* U programu Microsoft Word 2003 redovi teksta koji se pišu zdesna nalijevo mogu se ponovno čitati s omogućenom Brailleovom pismom. (#627)
* U programu Microsoft Word, recimo da sve sada radi ispravno kada dokument ne završava završetkom rečenice.
* Prilikom otvaranja obične tekstualne poruke u programu Windows Live Mail 2011, NVDA će se ispravno usredotočiti na dokument poruke koji omogućuje čitanje.
* NVDA se više privremeno ne zamrzava ili odbija govoriti u dijaloškom okviru Premjesti u / Kopiraj u u Windows Live Mailu. (#574)
* U programu Outlook 2010 NVDA će sada ispravno pratiti fokus na popisu poruka. (#1285)
* Neki problemi s USB vezom riješeni su s MDV Lilli brajičnim zaslonom. (#241)
* U pregledniku Internet Explorer i drugim MSHTML kontrolama razmaci se više ne zanemaruju u načinu pregledavanja u određenim slučajevima (npr. nakon veze).
* U pregledniku Internet Explorer i drugim MSHTML kontrolama uklonjeni su neki suvišni prijelomi redaka u načinu pregledavanja. konkretno, HTML elementi sa stilom prikaza None više ne forsiraju prijelom retka. (#1685)
* Ako se NVDA ne može pokrenuti, neuspjeh reprodukcije Windows kritičnog zvuka zaustavljanja više ne ometa kritičnu poruku o pogrešci u datoteci dnevnika.

### Promjene za programere

* Dokumentacija za razvojne inženjere sada se može generirati pomoću SCons-a. Pojedinosti potražite u readme.txt u korijenu izvorne distribucije, uključujući povezane ovisnosti.
* Regionalne sheme sada mogu pružati opise znakova. Pojedinosti potražite u odjeljku Opisi znakova u Vodiču za razvojne programere. (#55)
* Regionalne sheme sada mogu pružati informacije o izgovoru određenih interpunkcijskih znakova i drugih simbola. Pojedinosti potražite u odjeljku Izgovor simbola u Vodiču za razvojne programere. (#332)
* Sada možete izgraditi NVDAHelper s nekoliko opcija za otklanjanje pogrešaka pomoću varijable nvdaHelperDebugFlags SCons. Pojedinosti potražite u readme.txt u korijenu izvorne distribucije. (#1390)
* Sintisajzerskim upravljačkim programima sada se prosljeđuje niz tekstualnih i govornih naredbi za govor, umjesto samo teksta i indeksa.
 * To omogućuje ugrađene indekse, promjene parametara itd.
 * Upravljački programi trebaju implementirati SynthDriver.speak() umjesto SynthDriver.speakText() i SynthDriver.speakCharacter().
 * Stare metode će se koristiti ako SynthDriver.speak() nije implementiran, ali su zastarjele i bit će uklonjene u budućem izdanju.
* gui.execute() je uklonjen. wx. Umjesto toga treba koristiti CallAfter().
* gui.scriptUI je uklonjen.
 * Za dijaloške okvire poruka koristite wx. CallAfter(gui.messageBox, ...).
 * Za sve ostale dijaloške okvire umjesto toga treba koristiti prave wx dijaloške okvire.
 * Nova funkcija gui.runScriptModalDialog() pojednostavljuje korištenje modalnih dijaloških okvira iz skripti.
* Sintisajzerski upravljački programi sada mogu podržavati booleove postavke. Pogledajte SynthDriverHandler.BooleanSynthSetting.
* SCons sada prihvaća varijablu certTimestampServer koja specificira URL poslužitelja za vremenske oznake koji će se koristiti za označavanje autentičnih potpisa vremenskim žigovima. (#1644)

## 2011.1.1

Ovo izdanje rješava nekoliko sigurnosnih i drugih važnih problema pronađenih u NVDA 2011.1.

### Ispravci grešaka

* Stavka Doniraj u NVDA izborniku sada je onemogućena kada se pokreće na zaslonu za prijavu, zaključavanje, UAC i drugim sigurnim Windows zaslonima jer predstavlja sigurnosni rizik. (#1419)
* Sada je nemoguće kopirati ili zalijepiti unutar NVDA korisničkog sučelja dok ste na sigurnim radnim površinama (zaključani zaslon, UAC zaslon i prijava u sustav Windows) jer to predstavlja sigurnosni rizik. (#1421)
* U Firefoxu 4, prelazak na naredbu za sadržavanje virtualnog međuspremnika (NVDA+kontrola+razmak) sada radi kako bi trebao bježati od ugrađenih objekata kao što je Flash sadržaj. (#1429)
* Kada je omogućeno upravljanje naredbenim tipkama, pomaknuti znakovi više se ne izgovaraju pogrešno kao naredbene tipke. (#1422)
* Kada govorimo o naredbenim tipkama je omogućeno, pritiskanje razmaka s modifikatorima koji nisu shift (kao što su control i alt) sada se prijavljuje kao naredbena tipka. (#1424)
* Zapisivanje je sada potpuno onemogućeno kada se izvodi na zaslonima za prijavu, zaključavanje, UAC i drugim sigurnim Windows zaslonima, jer je to sigurnosni rizik. (#1435)
* U načinu pomoći za unos, geste se sada bilježe čak i ako nisu vezane za skriptu (u skladu s korisničkim priručnikom). (#1425)

## 2011.1

Istaknuti dijelovi ovog izdanja uključuju automatsko izvještavanje o novom tekstualnom ispisu u mIRC-u, PuTTY-u, Tera Termu i SecureCRT-u; podrška za globalne dodatke; najava grafičkih oznaka i numeriranja u programu Microsoft Word; dodatna povezivanja tipki za brajice, uključujući tipke za prelazak na sljedeći i prethodni redak; podrška za nekoliko Baum, HumanWare i APH Brailleovih zaslona; i izvještavanje o bojama za neke kontrole, uključujući IBM Lotus Symphony tekstualne kontrole.

### Nove značajke

* Boje se sada mogu prijaviti za neke kontrole. Automatska najava može se konfigurirati u dijaloškom okviru preferenci formatiranja dokumenta. Također se može prijaviti na zahtjev pomoću naredbe za oblikovanje teksta izvješća (NVDA+f).
 * U početku, ovo je podržano u standardnim IAccessible2 uređivačkim kontrolama teksta (kao što su Mozilla aplikacije), RichEdit kontrolama (kao što je u Wordpadu) i IBM Lotus Symphony tekstualnim kontrolama.
* U virtualnim međuspremnikima sada možete birati po stranici (koristeći shift+pageDown i shift+pageUp) i paragrafu (koristeći shift+control+downArrow i shift+control+downArrow). (#639)
* NVDA sada automatski izvještava o novom tekstualnom izlazu u mIRC-u, PuTTY-u, Tera Termu i SecureCRT-u. (#936)
* Korisnici sada mogu dodati nove veze tipki ili nadjačati postojeće za bilo koju skriptu u NVDA pružajući jednu kartu geste unosa korisnika. (#194)
* Podrška za globalne dodatke. Globalni dodaci mogu dodati nove funkcionalnosti NVDA koja radi u svim aplikacijama. (#281)
* Sada se čuje mali zvučni signal prilikom tipkanja znakova tipkom shift dok je capslock uključen. To se može isključiti tako da poništite odabir povezane nove opcije u dijaloškom okviru Postavke tipkovnice. (#663)
* tvrdi prijelomi stranica sada se najavljuju prilikom premještanja po retku u programu Microsoft Word. (#758)
* Grafičke oznake i numeriranje sada se izgovaraju u programu Microsoft Word prilikom kretanja po liniji. (#208)
* Sada je dostupna naredba za prebacivanje stanja mirovanja za trenutnu aplikaciju (NVDA+shift+s). Stanje mirovanja (ranije poznato kao način samoizražavanja) onemogućuje sve funkcije čitanja zaslona u NVDA za određenu aplikaciju. Vrlo korisno za aplikacije koje pružaju vlastite značajke čitanja govora i/ili zaslona. Ponovno pritisnite ovu naredbu da biste onemogućili stanje mirovanja.
* Dodane su neke dodatne veze s tipkama na Brailleovom pismu. Pojedinosti potražite u odjeljku Podržani brajični zasloni u Korisničkom priručniku. (#209)
* Radi praktičnosti programera trećih strana, moduli aplikacije kao i globalni dodaci sada se mogu ponovno učitati bez ponovnog pokretanja NVDA-e. Koristite alati -> Ponovno učitajte dodatke u NVDA izborniku ili NVDA+kontrola+f3. (#544)
* NVDA sada pamti poziciju na kojoj ste se nalazili kada ste se vratili na prethodno posjećenu web stranicu. To vrijedi sve dok se ne zatvori preglednik ili NVDA. (#132)
* Zasloni za brajicu Handy Tech sada se mogu koristiti bez instaliranja univerzalnog upravljačkog programa Handy Tech. (#854)
* Podrška za nekoliko Baum, HumanWare i APH Brailleovih zaslona. (#937)
* Traka stanja u programu Media Player Classic Home Cinema sada je prepoznata.
* Brajevi zaslon Freedom Scientific Focus 40 Blue sada se može koristiti kada je povezan putem bluetootha. (#1345)

### Promjenama

* Informacije o poziciji više se ne prijavljuju prema zadanim postavkama u nekim slučajevima kada su obično bile netočne; npr. većina izbornika, traka pokrenutih aplikacija, područje obavijesti itd. Međutim, to se može ponovno uključiti dodanom opcijom u dijaloškom okviru postavki Prikaz objekta.
* Pomoć za tipkovnicu preimenovana je u pomoć za unos kako bi odražavala da obrađuje unos iz izvora koji nisu tipkovnica.
* Pomoć za unos više ne izvještava o lokaciji koda skripte putem govora i Brailleovog pisma jer je zagonetna i nebitna za korisnika. Međutim, sada je zabilježen za programere i napredne korisnike.
* Kada NVDA otkrije da se zamrznuo, nastavlja presretati NVDA modifikatorske ključeve, iako sve ostale ključeve prosljeđuje sustavu. To sprječava korisnika da nenamjerno uključi caps lock itd. ako pritisne tipku za modifikaciju NVDA, a da ne shvati da se NVDA zamrznula. (#939)
* Ako se tipke drže pritisnute nakon korištenja naredbe pass next key through, sve tipke (uključujući ponavljanja tipki) sada se prosljeđuju dok se ne otpusti posljednja tipka.
* Ako se pritisne NVDA tipka modifikatora dva puta u brzom slijedu kako bi se proslijedila, a drugi pritisak je pritisnut, sada će se proslijediti i sva ponavljanja tipki.
* Tipke za pojačavanje, smanjivanje glasnoće i isključivanje zvuka sada se prijavljuju u pomoći za unos. To bi moglo biti korisno ako korisnik nije siguran što su ti ključevi.
* Prečac za stavku Pregled kursora u izborniku NVDA postavki promijenjen je iz r u c kako bi se uklonio sukob sa stavkom Postavke brajice.

### Ispravci grešaka

* Kada dodajete novi unos govornog rječnika, naslov dijaloškog okvira sada je "Dodaj unos u rječnik" umjesto "Uredi unos rječnika". (#924)
* U dijaloškim okvirima govornog rječnika, sadržaj stupaca Regularni izraz i Velika i mala slova na popisu unosa rječnika sada se prikazuje na konfiguriranom NVDA jeziku umjesto uvijek na engleskom.
* U AIM-u se informacije o položaju sada objavljuju u prikazima stabla.
* Na klizačima u dijaloškom okviru Glasovne postavke, strelica gore/stranica gore/početna sada povećavaju postavku, a strelica prema dolje/stranica prema dolje/kraj smanjuju. Ranije se dogodilo suprotno, što nije logično i nije u skladu s prstenom za postavke sintisajzera. (#221)
* U virtualnim međuspremnicima s onemogućenim rasporedom zaslona neke se suvišne prazne linije više ne pojavljuju.
* Ako se tipka za modifikaciju NVDA pritisne dvaput brzo, ali dođe do pritiska tipke, tipka za modifikaciju NVDA više se ne prosljeđuje pri drugom pritisku.
* Interpunkcijske tipke sada se izgovaraju u pomoći za unos čak i kada je govor o interpunkciji onemogućen. (#977)
* U dijaloškom okviru Postavke tipkovnice, nazivi rasporeda tipkovnice sada su prikazani na konfiguriranom NVDA jeziku umjesto uvijek na engleskom. (#558)
* Riješen je problem zbog kojeg su neke stavke prikazane kao prazne u dokumentima programa Adobe Reader; npr. poveznice u sadržaju Korisničkog priručnika za Apple iPhone IOS 4.1.
* Gumb "Koristi trenutno spremljene postavke na zaslonu za prijavu i drugim sigurnim zaslonima" u NVDA dijaloškom okviru Opće postavke sada radi ako se koristi odmah nakon nove instalacije NVDA-a, ali prije nego što se pojavi siguran zaslon. Prethodno je NVDA izvijestila da je kopiranje bilo uspješno, ali zapravo nije imalo učinka. (#1194)
* Više nije moguće istovremeno otvoriti dva dijaloška okvira NVDA postavki. Ovo rješava probleme u kojima jedan otvoreni dijaloški okvir ovisi o drugom otvorenom dijaloškom okviru; npr. promjena sintisajzera dok je otvoren dijaloški okvir Glasovne postavke. (#603)
* Na sustavima s omogućenim UAC-om, gumb "Koristi trenutno spremljene postavke na zaslonu za prijavu i drugim sigurnim zaslonima" u NVDA dijaloškom okviru Opće postavke više ne uspijeva nakon upita UAC-a ako naziv korisničkog računa sadrži razmak. (#918)
* U Internet Exploreru i drugim MSHTML kontrolama, NVDA sada koristi URL kao posljednje sredstvo za određivanje naziva veze, umjesto da prikazuje prazne veze. (#633)
* NVDA više ne zanemaruje fokus u AOL Instant Messenger 7 izbornicima. (#655)
* Najavite ispravnu oznaku za pogreške u dijaloškom okviru za provjeru pravopisa u programu Microsoft Word (npr. Nije u rječniku, gramatička pogreška, interpunkcija). Prethodno su svi bili najavljeni kao gramatička pogreška. (#883)
* Tipkanje u programu Microsoft Word tijekom korištenja brajičnog zaslona više ne bi trebalo uzrokovati upisivanje iskrivljenog teksta, a rijetko zamrzavanje prilikom pritiskanja tipke za usmjeravanje brajice u dokumentima programa Word riješeno je. (#1212) No ograničenje je da se arapski tekst više ne može čitati u programu Word 2003 i starijim verzijama dok se koristi zaslon za brajicu. (#627)
* Kada pritisnete tipku za brisanje u polju za uređivanje, tekst/pokazivač na Brajevom pismu sada bi se uvijek trebao ažurirati na odgovarajući način kako bi odražavao promjenu. (#947)
* Promjene na dinamičkim stranicama u Gecko2 dokumentima (npr. Firefox 4) dok je otvoreno više kartica sada se ispravno odražavaju u NVDA. Prije su se odražavale samo promjene na prvoj kartici. (Mozilla bug 610985)
* NVDA sada može ispravno najaviti prijedloge za gramatičke i interpunkcijske pogreške u dijaloškom okviru za provjeru pravopisa u programu Microsoft Word. (#704)
* U Internet Exploreru i drugim MSHTML kontrolama, NVDA više ne prikazuje odredišna sidra kao prazne veze u svom virtualnom međuspremniku. Umjesto toga, ta su sidra skrivena kako bi trebala biti. (#1326)
* Navigacija objektima oko i unutar standardnih prozora grupnih okvira više nije pokvarena i asimetrična.
* U Firefoxu i drugim kontrolama temeljenim na Gecku, NVDA više neće zapeti u podokviru ako završi s učitavanjem prije vanjskog dokumenta.
* NVDA sada prikladno najavljuje sljedeći znak prilikom brisanja znaka pomoću numpadDelete. (#286)
* Na zaslonu za prijavu u sustav Windows XP korisničko ime ponovno se prijavljuje kada se odabrani korisnik promijeni.
* Riješeni su problemi pri čitanju teksta u naredbenim konzolama sustava Windows s omogućenim izvješćivanjem o brojevima redaka.
* Dijaloški okvir Popis elemenata za virtualne međuspremnike sada mogu koristiti korisnici koji vide. Sve kontrole vidljive su na zaslonu. (#1321)
* Popis unosa u dijaloškom okviru Rječnik govora sada je čitljiviji korisnicima koji vide. Popis je sada dovoljno velik da prikaže sve stupce na zaslonu. (#90)
* Na ALVA BC640/BC680 brajici, NVDA više ne zanemaruje tipke zaslona koje se i dalje drže pritisnute nakon otpuštanja druge tipke.
* Adobe Reader X više se ne ruši nakon napuštanja nestrukturiranih opcija dokumenta prije nego što se pojavi dijaloški okvir za obradu. (#1218)
* NVDA se sada prebacuje na odgovarajući upravljački program brajičnog zaslona kada se vratite na spremljenu konfiguraciju. (#1346)
* Čarobnjak za projekt Visual Studio 2008 ponovno se ispravno čita. (#974)
* NVDA više ne radi u potpunosti u aplikacijama koje sadrže ne-ASCII znakove u svom izvršnom nazivu. (#1352)
* Kada čitate po retku u AkelPadu s omogućenim prelamanjem riječi, NVDA više ne čita prvi znak sljedećeg retka na kraju trenutnog retka.
* U uređivaču koda Visual Studio 2005/2008, NVDA više ne čita cijeli tekst nakon svakog upisanog znaka. (#975)
* Riješen je problem zbog kojeg neki Brailleovi zasloni nisu bili ispravno obrisani kada je NVDA izašao ili je zaslon promijenjen.
* Početni fokus se više ne izgovara dva puta kada se NVDA pokrene. (#1359)

### Promjene za programere

* SCons se sada koristi za pripremu izvornog stabla i stvaranje binarnih verzija, prijenosnih arhiva, instalacijskih programa itd. Za detalje pogledajte readme.txt u korijenu izvorne distribucije.
* Nazivi ključeva koje koristi NVDA (uključujući karte tipki) postali su prijateljskiji/logičniji; npr. upArrow umjesto extendedUp i numpadPageUp umjesto prior. Pogledajte modul vkCodes za popis.
* Sav unos korisnika sada je predstavljen instancom inputCore.InputGesture. (#601)
 * Svaki izvor ulaznih podklasa osnovna je klasa InputGesture.
 * Pritiski na tipke na tipkovnici sustava obuhvaćeni su klasom keyboardHandler.KeyboardInputGesture.
 * Pritiske gumba, kotačića i drugih kontrola na Brailleovom pismu obuhvaćeni su podrazredima brajice. Klasa BrailleDisplayGesture. Ove podklase pruža svaki upravljački program za Brailleovo pismo.
* Ulazne geste vezane su za ScriptableObjects pomoću metode ScriptableObject.bindGesture() na instanci ili __gestures dikta na klasi koja mapira identifikatore gesta na nazive skripti. Pojedinosti potražite u članku baseObject.ScriptableObject.
* Moduli aplikacije više nemaju datoteke s kartama ključeva. Sva povezivanja gestom unosa moraju se izvršiti u samom modulu aplikacije.
* Sve skripte sada uzimaju instancu InputGesture umjesto pritiska tipke.
 * KeyboardInputGestures može se poslati u operacijski sustav pomoću metode send() geste.
* Da biste poslali proizvoljni pritisak tipke, sada morate stvoriti KeyboardInputGesture pomoću KeyboardInputGesture.fromName(), a zatim koristiti njegovu metodu send().
* Regionalne sheme sada mogu sadržavati datoteku karte geste unosa za dodavanje novih veza ili nadjačavanje postojećih veza za skripte bilo gdje u NVDA. (#810)
 * Mape gesti regionalnih shema trebaju biti smještene u locale\LANG\gestures.ini, gdje je LANG kod jezika.
 * Pogledajte inputCore.GlobalGestureMap za pojedinosti o formatu datoteke.
* Novi LiveText i Terminal NVDAObject ponašanja olakšavaju automatsko izvještavanje o novom tekstu. Pogledajte te klase u NVDAObjects.behaviors za detalje. (#936)
 * Klasa preklapanja NVDAObjects.window.DisplayModelLiveText može se koristiti za objekte koji moraju dohvatiti tekst zapisan na zaslonu.
 * Pogledajte module aplikacija mirc i putty za primjere upotrebe.
* Više ne postoji _default modul aplikacije. Moduli aplikacije trebali bi umjesto toga podklasirati appModuleHandler.AppModule (osnovna klasa AppModule).
* Podrška za globalne dodatke koji mogu globalno vezati skripte, obrađivati NVDAObject događaje i odabrati NVDAObject klase preklapanja. (#281) Pojedinosti potražite u globalPluginHandler.GlobalPlugin.
* Na objektima SynthDriver, atributi available* za postavke niza (npr. availableVoices i availableVariants) sada su OrderedDicts s tipkom ID-a umjesto popisa.
* synthDriverHandler.VoiceInfo sada uzima neobavezni argument jezika koji određuje jezik glasa.
* SynthDriver objekti sada pružaju atribut jezika koji određuje jezik trenutnog glasa.
 * Osnovna implementacija koristi jezik naveden na VoiceInfo objektima u availableVoices. Ovo je prikladno za većinu sintisajzera koji podržavaju jedan jezik po glasu.
* Upravljački programi Brailleovog pisma poboljšani su kako bi omogućili povezivanje gumba, kotačića i drugih kontrola s NVDA skriptama:
 * Upravljački programi mogu pružiti globalnu kartu gesta unosa za dodavanje veza za skripte bilo gdje u NVDA.
 * Oni također mogu pružiti vlastite skripte za izvođenje određenih funkcija prikaza.
 * Vidi Brailleovo pismo. BrailleDisplayDriver za detalje i postojeće upravljačke programe za Brailleovo pismo na primjere.
* Svojstvo 'selfVoicing' na klasama AppModule sada je preimenovano u 'sleepMode'.
* Događaji modula aplikacije event_appLoseFocus i event_appGainFocus sada su preimenovani u event_appModule_loseFocus i event_appModule_gainFocus, s poštovanjem, kako bi konvencija imenovanja bila u skladu s modulima aplikacije i presretačima stabala.
* Svi upravljački programi za Brailleovo pismo sada bi trebali koristiti Brailleovo pismo. BrailleDisplayDriver umjesto Brailleovog pisma. BrailleDisplayDriverWithCursor.
 * Pokazivačem se sada upravlja izvan upravljačkog programa.
 * Postojeći upravljački programi trebaju samo promijeniti svoju izjavu o klasi u skladu s tim i preimenovati svoju _display metodu za prikaz.

## 2010.2

Značajne značajke ovog izdanja uključuju znatno pojednostavljenu navigaciju objektima; virtualni međuspremniki za Adobe Flash sadržaj; pristup mnogim prethodno nedostupnim kontrolama dohvaćanjem teksta napisanog na zaslonu; ravan pregled teksta zaslona; podrška za IBM Lotus Symphony dokumente; izvještavanje o zaglavljima redaka i stupaca tablice u Mozilla Firefoxu; i značajno poboljšana korisnička dokumentacija.

### Nove značajke

* Navigacija kroz objekte pomoću kursora za pregled uvelike je pojednostavljena. Pokazivač pregleda sada isključuje objekte koji nisu korisni korisniku; tj. predmeti koji se koriste samo u svrhu rasporeda i nedostupni objekti.
* U aplikacijama koje koriste Java Access Bridge (uključujući OpenOffice.org), oblikovanje se sada može prijaviti u tekstualnim kontrolama. (#358, #463)
* Kada pomičete miš preko ćelija u Microsoft Excelu, NVDA će ih prikladno najaviti.
* U aplikacijama koje koriste Java Access Bridge, tekst dijaloškog okvira sada se prijavljuje kada se pojavi dijaloški okvir. (#554)
* VirtualBuffer se sada može koristiti za navigaciju Adobe Flash sadržajem. Navigacija objektima i izravna interakcija s kontrolama (uključivanjem načina fokusiranja) i dalje su podržani. (#453)
* Kontrole teksta koje se mogu uređivati u Eclipse IDE-u, uključujući uređivač koda, sada su dostupne. Morate koristiti Eclipse 3.6 ili noviji. (#256, #641)
* NVDA sada može dohvatiti većinu teksta napisanog na zaslonu. (#40, #643)
 * To omogućuje čitanje kontrola koje ne izlažu informacije na izravniji/pouzdaniji način.
 * Kontrole koje ova značajka čini dostupnima uključuju: neke stavke izbornika koje prikazuju ikone (npr. izbornik Otvori s na datotekama u sustavu Windows XP) (#151), tekstna polja koja se mogu uređivati u aplikacijama Windows Live (#200), popis pogrešaka u programu Outlook Express (#582), kontrolu teksta koja se može uređivati u TextPadu (#605), popise u Eudori, mnoge kontrole u australskom e-porezu i traku formule u programu Microsoft Excel.
* Podrška za uređivač koda u Microsoft Visual Studio 2005 i 2008. Potreban je barem Visual Studio Standard; ovo ne funkcionira u Express izdanjima. (#457)
* Podrška za IBM Lotus Symphony dokumente.
* Rana eksperimentalna podrška za Google Chrome. Imajte na umu da je podrška za Chromeov čitač zaslona daleko od potpune i da će možda biti potreban dodatni rad u NVDA. Trebat će vam nedavna razvojna verzija Chromea da biste to isprobali.
* Stanje preklopnih tipki (Caps Lock, Num Lock i Scroll Lock) sada se prikazuje na Brailleovom pismu kada se pritisnu. (#620)
* Balončići pomoći sada se prikazuju na Brailleovom pismu kada se pojave. (#652)
* Dodan je upravljački program za MDV Lilli Brailleov zaslon. (#241)
* Prilikom odabira cijelog retka ili stupca u programu Microsoft Excel pomoću tipki prečaca shift+razmak i control+razmak, sada se izvještava o novom odabiru. (#759)
* Sada se mogu izvješćivati o zaglavljima redaka i stupaca tablice. To se može konfigurirati u dijaloškom okviru preferenci oblikovanja dokumenta.
 * Trenutno je to podržano u dokumentima u Mozillinim aplikacijama kao što su Firefox (verzija 3.6.11 i novija) i Thunderbird (verzija 3.1.5 i novija). (#361)
* Uvedene naredbe za plošni pregled: (#58)
 * NVDA+numerička tipkovnica7 prebacuje se na plošni pregled, postavljajući kursor za pregled na položaj trenutnog objekta, omogućujući vam pregled zaslona (ili dokumenta ako je unutar njega) pomoću naredbi za pregled teksta.
 * NVDA+numerička tipkovnica1 pomiče kursor za pregled u objekt predstavljen tekstom na poziciji kursora za pregled, omogućujući vam navigaciju po objektu od te točke.
* Trenutne NVDA korisničke postavke mogu se kopirati za korištenje na sigurnim Windows zaslonima kao što su zasloni za prijavu i UAC zaslon pritiskom na gumb u dijaloškom okviru Opće postavke. (#730)
* Podrška za Mozilla Firefox 4.
* Podrška za Microsoft Internet Explorer 9.

### Promjenama

* Naredbe sayAll by Navigator objekt (NVDA+numpadAdd), navigator objekt sljedeći u toku (NVDA+shift+numpad6) i navigator objekt prethodni u toku (NVDA+shift+numpad4) za sada su uklonjene, zbog grešaka i kako bi se oslobodile tipke za druge moguće značajke.
* U dijaloškom okviru NVDA sintisajzera sada je naveden samo zaslonski naziv sintisajzera. Prije toga mu je prethodilo ime vozača, koje je relevantno samo interno.
* Kada ste u ugrađenim aplikacijama ili virtualnim međuspremnikima unutar drugog virtualBuffera (npr. Flash), sada možete pritisnuti nvda+control+razmak da biste izašli iz ugrađene aplikacije ili virtualnog međuspremnika u dokument koji sadrži. Ranije se za to koristio nvda+space. Sada je nvda+space posebno samo za prebacivanje obrva/fokusa na virtualBuffers.
* Ako se pregledniku govora (omogućenom u izborniku alata) dodijeli fokus (npr. kliknulo se), novi tekst neće se pojaviti u kontroli dok se fokus ne pomakne. To omogućuje lakši odabir teksta (npr. za kopiranje).
* Preglednik dnevnika i Python konzola maksimizirani su kada se aktiviraju.
* Kada se usredotočite na radni list u programu Microsoft Excel i odabrano je više od jedne ćelije, najavljuje se raspon odabira, a ne samo aktivna ćelija. (#763)
* Spremanje konfiguracije i promjena određenih osjetljivih opcija sada je onemogućeno prilikom pokretanja na zaslonima za prijavu, UAC i drugim sigurnim Windows zaslonima.
* Ažuriran eSpeak sintetizator govora na 1.44.03.
* Ako je NVDA već pokrenut, aktiviranje NVDA prečaca na radnoj površini (što uključuje pritiskanje control+alt+n) ponovno će pokrenuti NVDA.
* Uklonjen je tekst izvješća ispod potvrdnog okvira miša iz dijaloškog okvira Postavke miša i zamijenjen potvrdnim okvirom Omogući praćenje miša, što bolje odgovara skripti za prebacivanje praćenja miša (NVDA+m).
* Ažurira raspored tipkovnice prijenosnog računala tako da uključuje sve naredbe dostupne u rasporedu radne površine i ispravno radi na tipkovnicama koje nisu engleske. (#798, #800)
* Značajna poboljšanja i ažuriranja korisničke dokumentacije, uključujući dokumentaciju naredbi tipkovnice prijenosnog računala i sinkronizaciju brzih referenci naredbi tipkovnice s korisničkim priručnikom. (#455)
* Ažuriran prevoditelj brajice liblouis na 2.1.1. Naime, ovo rješava neke probleme povezane s kineskom Brailleovom pismom, kao i znakove koji nisu definirani u tablici prijevoda. (#484, #499)

### Ispravci grešaka

* U μTorrentu, fokusirana stavka na popisu torrenta više ne prijavljuje više puta ili krade fokus kada je izbornik otvoren.
* U μTorrentu se sada prijavljuju nazivi datoteka na popisu sadržaja torrenta.
* U Mozillinim aplikacijama fokus se sada ispravno detektira kada padne na prazan stol ili stablo.
* U Mozillinim aplikacijama, "nije označeno" sada se ispravno prijavljuje za provjerljive kontrole, kao što su ćelije tablice koje se mogu provjeriti. (#571)
* U Mozillinim aplikacijama, tekst ispravno implementiranih ARIA dijaloških okvira više se ne zanemaruje i sada će biti prijavljen kada se pojavi dijaloški okvir. (#630)
* u pregledniku Internet Explorer i drugim MSHTML kontrolama atribut razine ARIA sada se ispravno poštuje.
* U pregledniku Internet Explorer i drugim MSHTML kontrolama sada se odabire uloga ARIA umjesto drugih vrsta informacija da bi se omogućilo mnogo ispravnije i predvidljivije ARIA iskustvo.
* Zaustavio je rijedak pad u pregledniku Internet Explorer prilikom navigacije kroz okvire ili iFrameove.
* U dokumentima programa Microsoft Word redovi koji se pišu zdesna nalijevo (kao što je arapski tekst) mogu se ponovno pročitati. (#627)
* Znatno smanjeno kašnjenje kada se velike količine teksta prikazuju u naredbenoj konzoli sustava Windows na 64-bitnim sustavima. (#622)
* Ako je Skype već pokrenut kada se NVDA pokrene, više nije potrebno ponovno pokretati Skype da biste omogućili pristupačnost. To može vrijediti i za druge aplikacije koje provjeravaju zastavicu čitača zaslona sustava.
* U Microsoft Office aplikacijama NVDA se više ne ruši kada se pritisne govor u prednjem planu (NVDA+b) ili kada se krećete nekim objektima na alatnim trakama. (#616)
* Ispravljen netočan govor brojeva koji sadrže 0 nakon razdjelnika; npr. 1,023. (#593)
* Adobe Acrobat Pro i Reader 9 više se ne ruše prilikom zatvaranja datoteke ili izvođenja određenih drugih zadataka. (#613)
* Odabir se sada najavljuje kada se pritisne control+a da bi se odabrao sav tekst u nekim kontrolama teksta koje se mogu uređivati, kao što je Microsoft Word. (#761)
* U Scintilla kontrolama (npr. Notepad++), tekst više nije pogrešno odabran kada NVDA pomiče kursor, kao što je tijekom reci sve. (#746)
* Ponovno je moguće pregledati sadržaj ćelija u programu Microsoft Excel pomoću pokazivača pregleda.
* NVDA ponovno može čitati po retku u određenim problematičnim poljima textArea u Internet Exploreru 8. (#467)
* Windows Live Messenger 2009 više se ne zatvara odmah nakon pokretanja dok je NVDA pokrenut. (#677)
* U web preglednicima, Više nije potrebno pritisnuti tab za interakciju s ugrađenim objektom (kao što je Flash sadržaj) nakon pritiska na enter na ugrađenom objektu ili povratka iz druge aplikacije. (#775)
* U kontrolama Scintilla (npr. Notepad++), početak dugih redaka više se ne skraćuje kada se pomiče sa zaslona. Također, ove duge crte bit će ispravno prikazane na Brailleovom pismu kada su odabrane.
* U Loudtalksu je sada moguće pristupiti popisu kontakata.
* URL dokumenta i "MSAAHTML registrirani rukovatelj" više se ponekad ne prijavljuju lažno u pregledniku Internet Explorer i drugim MSHTML kontrolama. (#811)
* U prikazima stabla u Eclipse IDE-u, prethodno fokusirana stavka više nije pogrešno najavljena kada se fokus pomakne na novu stavku.
* NVDA sada ispravno funkcionira na sustavu u kojem je trenutni radni direktorij uklonjen iz DLL puta pretraživanja (postavljanjem unosa registra CWDIllegalInDllSearch na 0xFFFFFFFF). Imajte na umu da to nije relevantno za većinu korisnika. (#907)
* Kada se naredbe za navigaciju tablicom koriste izvan tablice u programu Microsoft Word, "rub tablice" više se ne izgovara nakon "nije u tablici". (#921)
* Kada se naredbe za navigaciju tablicom ne mogu pomicati jer se nalaze na rubu tablice u programu Microsoft Word, "rub tablice" sada se izgovara na konfiguriranom NVDA jeziku, a ne uvijek na engleskom. (#921)
* U programima Outlook Express, Windows Mail i Windows Live Mail sada se izvješćuje o stanju potvrdnih okvira na popisima pravila za poruke. (#576)
* Opis pravila za poruke sada se može pročitati u programu Windows Live Mail 2010.

## 2010.1

Ovo izdanje prvenstveno se fokusira na ispravke grešaka i poboljšanja korisničkog iskustva, uključujući neke značajne popravke stabilnosti.

### Nove značajke

* NVDA se više ne uspijeva pokrenuti na sustavu bez audio izlaznih uređaja. Očito je da će se u ovom slučaju za izlaz morati koristiti Brailleov zaslon ili sintetizator tišine u kombinaciji s preglednikom govora. (#425)
* U dijaloški okvir postavki formatiranja dokumenta dodan je potvrdni okvir za obilježja izvješća koji vam omogućuje da konfigurirate treba li NVDA najavljivati orijentir u web dokumentima. Radi kompatibilnosti s prethodnim izdanjem, opcija je uključena prema zadanim postavkama.
* Ako je omogućeno izgovaranje naredbenih tipki, NVDA će sada objaviti nazive multimedijskih tipki (npr. reprodukcija, zaustavljanje, početna stranica, itd.) na mnogim tipkovnicama kada ih pritisnete. (#472)
* NVDA sada najavljuje da će se riječ izbrisati pritiskom na control+backspace u kontrolama koje je podržavaju. (#491)
* Tipke sa strelicama sada se mogu koristiti u prozoru Web formator za navigaciju i čitanje teksta. (#452)
* Popis unosa u adresaru programa Microsoft Office Outlook sada je podržan.
* NVDA bolje podržava ugrađene dokumente koji se mogu uređivati (način dizajna) u Internet Exploreru. (#402)
* nova skripta (nvda+shift+numpadMinus) omogućuje vam premještanje fokusa sustava na trenutni objekt navigatora.
* Nove skripte za zaključavanje i otključavanje lijeve i desne tipke miša. Korisno za izvođenje operacija povlačenja i ispuštanja. shift+numpadPodijeli za zaključavanje/otključavanje lijeve strane, shift+numpadMultiply za zaključavanje/otključavanje desne.
* Nove tablice za prijevod Brailleovog pisma: njemački računalni braille s 8 točaka, njemački razred 2, finski računalni braille s 8 točaka, kineski (Hong Kong, kantonski), kineski (Tajvan, Manderin). (#344, #369, #415, #450)
* Sada je moguće onemogućiti stvaranje prečaca na radnoj površini (a time i tipke prečaca) prilikom instaliranja NVDA-e. (#518)
* NVDA sada može koristiti IAccessible2 kada je prisutan u 64-bitnim aplikacijama. (#479)
* Poboljšana podrška za žive regije u Mozillinim aplikacijama. (#246)
* Sada je dostupan API klijenta NVDA kontrolera koji aplikacijama omogućuje upravljanje NVDA-om; npr. za izgovaranje teksta, utišavanje govora, prikazivanje poruke na Brailleovom pismu itd.
* Informacije i poruke o pogreškama sada se čitaju na zaslonu za prijavu u sustavima Windows Vista i Windows 7. (#506)
* U programu Adobe Reader sada su podržani PDF interaktivni obrasci razvijeni pomoću programa Adobe LiveCycle. (#475)
* U Miranda IM-u, NVDA sada automatski čita dolazne poruke u chat prozorima ako je omogućeno izvještavanje o dinamičkim promjenama sadržaja. Također, dodane su naredbe za prijavljivanje tri najnovije poruke (NVDA+kontrola+broj). (#546)
* Ulazna tekstualna polja sada su podržana u Adobe Flash sadržaju. (#461)

### Promjenama

* Iznimno opširna poruka pomoći tipkovnice u izborniku Start sustava Windows 7 više se ne prijavljuje.
* Sintisajzer zaslona sada je zamijenjen novim preglednikom govora. Da biste ga aktivirali, odaberite Preglednik govora na izborniku Alati. Preglednik govora može se koristiti neovisno o tome koji sintisajzer govora koristite. (#44)
* Poruke na Brailleovom pismu automatski će se odbaciti ako korisnik pritisne tipku koja rezultira promjenom kao što je pomicanje fokusa. Prije bi poruka uvijek ostala na razini konfiguriranog vremena.
* Podešavanje treba li Brailleova pisma biti vezana za fokus ili kursor za pregled (NVDA+kontrola+t) sada se također može postaviti iz dijaloškog okvira postavki brajice, a sada se sprema i u korisnikovu konfiguraciju.
* Ažuriran eSpeak sintetizator govora na 1.43.
* Ažuriran prevoditelj brajice liblouis na 1.8.0.
* U virtualnim međuspremnikima znatno je poboljšano izvještavanje o elementima prilikom kretanja po znaku ili riječi. Ranije je prijavljeno mnogo nebitnih informacija, a izvještavanje je bilo vrlo različito od onog pri kretanju po liniji. (#490)
* Tipka Control sada jednostavno zaustavlja govor kao i druge tipke, umjesto da pauzira govor. Za pauziranje/nastavak govora koristite tipku Shift.
* Broj redaka i stupaca tablice više se ne objavljuje prilikom izvješćivanja o promjenama fokusa jer je ta objava prilično opširna i obično nije korisna.

### Ispravci grešaka

* NVDA se više ne uspijeva pokrenuti ako se čini da je podrška za automatizaciju korisničkog sučelja dostupna, ali se iz nekog razloga ne može inicijalizirati. (#483)
* Cijeli sadržaj retka tablice više se ponekad ne prijavljuje prilikom premještanja fokusa unutar ćelije u Mozillinim aplikacijama. (#482)
* NVDA više ne zaostaje dugo vremena kada proširuje stavke prikaza stabla koje sadrže vrlo veliku količinu podstavki.
* Prilikom navođenja SAPI 5 glasova, NVDA sada pokušava otkriti glasove s greškama i isključuje ih iz dijaloškog okvira Glasovne postavke i zvona postavki sintisajzera. Prije, kada je postojao samo jedan problematičan glas, NVDA-ov SAPI 5 upravljački program ponekad se ne bi uspio pokrenuti.
* Virtualni međuspremnici sada poštuju postavku tipki prečaca objekta izvješća koja se nalazi u dijaloškom okviru Prezentacija objekta. (#486)
* U virtualnim međuspremnikima koordinate redaka/stupaca više se ne čitaju pogrešno za zaglavlja redaka i stupaca kada je izvješćivanje o tablicama onemogućeno.
* U virtualnim međuspremnikima koordinate redaka/stupaca sada se ispravno čitaju kada napustite tablicu i zatim ponovno unesete istu ćeliju tablice bez prethodnog posjeta drugoj ćeliji; npr. pritiskom na goreStrelica, a zatim doljeStrelica na prvoj ćeliji tablice. (#378)
* Prazni redovi u Microsoft Word dokumentima i Microsoft HTML kontrole za uređivanje sada se na odgovarajući način prikazuju na brajici. Ranije je NVDA prikazivao trenutnu rečenicu na zaslonu, a ne trenutnu liniju za ove situacije. (#420)
* Višestruki sigurnosni popravci prilikom pokretanja NVDA pri prijavi u Windows i na drugim sigurnim radnim površinama. (#515)
* Položaj pokazivača (kursor) sada se ispravno ažurira prilikom izvođenja Reci sve koji se nalazi s dna zaslona, u standardnim poljima za uređivanje sustava Windows i dokumentima programa Microsoft Word. (#418)
* U virtualnim međuspremnikima tekst više nije pogrešno uključen za slike unutar veza i klikova koji su označeni kao nevažni za čitače zaslona. (#423)
* Popravci rasporeda tipkovnice prijenosnog računala. (#517)
* Kada je Brailleovo pismo vezano za pregled kada se usredotočite na prozor Dos konzole, kursor za pregled sada može ispravno navigirati tekstom u konzoli.
* Tijekom rada s TeamTalk3 ili TeamTalk4 Classic, traka napretka VU mjerača u glavnom prozoru više se ne najavljuje dok se ažurira. Također, posebni znakovi mogu se ispravno pročitati u prozoru za dolazni chat.
* Stavke se više ne izgovaraju dvaput u izborniku Start sustava Windows 7. (#474)
* Aktiviranje poveznica na istu stranicu u Firefoxu 3.6 na odgovarajući način pomiče kursor u virtualBufferu na ispravno mjesto na stranici.
* Riješen je problem zbog kojeg neki tekst nije prikazan u programu Adobe Reader u određenim PDF dokumentima.
* NVDA više ne izgovara pogrešno određene brojeve odvojene crticom; npr. 500-1000. (#547)
* U sustavu Windows XP NVDA više ne uzrokuje zamrzavanje Internet Explorera prilikom uključivanja potvrdnih okvira na servisu Windows Update. (#477)
* Kada koristite ugrađeni eSpeak sintisajzer, simultani govor i zvučni signali više ne uzrokuju povremeno zamrzavanje na nekim sustavima. To je bilo najuočljivije, na primjer, prilikom kopiranja velikih količina podataka u Windows Exploreru.
* NVDA više ne objavljuje da je Firefox dokument zauzet (npr. zbog ažuriranja ili osvježavanja) kada je taj dokument u pozadini. To je također uzrokovalo lažno objavljivanje statusne trake prijave u prvom planu.
* Prilikom prebacivanja rasporeda tipkovnice sustava Windows (s control+shift ili alt+shift), puni naziv rasporeda bilježi se i u govoru i na Brailleovom pismu. Ranije se o tome izvještavalo samo u govoru, a o alternativnim izgledima (npr. Dvorak) uopće se nije izvještavalo.
* Ako je izvješćivanje o tablicama onemogućeno, informacije o tablici više se ne objavljuju kada se fokus promijeni.
* Sada su dostupne određene standardne kontrole prikaza stabla u 64-bitnim aplikacijama (npr. prikaz stabla sadržaja u Microsoftovoj HTML pomoći). (#473)
* Riješeni su neki problemi s zapisivanjem poruka koje sadrže znakove koji nisu ASCII. To bi moglo uzrokovati lažne pogreške u nekim slučajevima na sustavima koji nisu engleski. (#581)
* Informacije u dijaloškom okviru O NVDA-u sada se prikazuju na korisnikovo konfiguriranom jeziku umjesto da se uvijek prikazuju na engleskom. (#586)
* Problemi se više ne susreću pri korištenju zvona postavki sintisajzera nakon što se glas promijeni u onaj koji ima manje postavki od prethodnog glasa.
* U Skypeu 4.2 imena kontakata više se ne izgovaraju dvaput na popisu kontakata.
* Ispravljena su neka potencijalno velika curenja memorije u grafičkom sučelju i u virtualnim međuspremnikima. (#590, #591)
* Zaobiđite gadnu grešku u nekim SAPI 4 sintisajzerima koja je uzrokovala česte pogreške i rušenja u NVDA. (#597)

## 2009.1

Glavni naglasci ovog izdanja uključuju podršku za 64-bitna izdanja sustava Windows; znatno poboljšana podrška za dokumente Microsoft Internet Explorer i Adobe Reader; podrška za Windows 7; čitanje zaslona za prijavu u sustav Windows, control+alt+delete i kontrolu korisničkog računa (UAC); i mogućnost interakcije s Adobe Flash i Sun Java sadržajem na web stranicama. Također je bilo nekoliko značajnih popravaka stabilnosti i poboljšanja općeg korisničkog iskustva.

### Nove značajke

* Službena podrška za 64-bitna izdanja sustava Windows! (#309)
* Dodan je upravljački program sintisajzera za sintisajzer Newfon. Imajte na umu da je za to potrebna posebna verzija Newfona. (#206)
* U virtualnim međuspremnikima, način fokusiranja i način pregledavanja sada se mogu prijaviti pomoću zvukova umjesto govora. To je omogućeno prema zadanim postavkama. Može se konfigurirati iz dijaloškog okvira Virtualni međuspremniki. (#244)
* NVDA više ne poništava govor kada se pritisnu tipke za kontrolu glasnoće na tipkovnici, omogućujući korisniku da odmah promijeni glasnoću i presluša stvarne rezultate. (#287)
* Potpuno prepisana podrška za dokumente Microsoft Internet Explorer i Adobe Reader. Ova je podrška objedinjena s osnovnom podrškom koja se koristi za Mozilla Gecko, tako da su značajke kao što su brzo prikazivanje stranica, opsežna brza navigacija, popis veza, odabir teksta, način automatskog fokusa i podrška za Brailleovo pismo sada dostupne s ovim dokumentima.
* Poboljšana podrška za kontrolu odabira datuma koja se nalazi u dijaloškom okviru svojstava datuma / vremena sustava Windows Vista.
* poboljšana podrška za početni izbornik Modern XP/Vista (posebno izbornike svih programa i mjesta). Sada su objavljene informacije o odgovarajućoj razini.
* Količina teksta koja se najavljuje prilikom pomicanja miša sada se može konfigurirati u dijaloškom okviru Postavke miša. Može se napraviti izbor odlomka, retka, riječi ili znaka.
* najavljuju pravopisne pogreške ispod pokazivača u programu Microsoft Word.
* podrška za provjeru pravopisa programa Microsoft Word 2007. Djelomična podrška može biti dostupna za prethodne verzije programa Microsoft Word.
* Bolja podrška za Windows Live Mail. Sada se mogu čitati obične tekstualne poruke i mogu se koristiti i obični tekst i HTML poruke.
* U sustavu Windows Vista, ako se korisnik pomakne na sigurnu radnu površinu (bilo zato što se pojavio dijaloški okvir UAC kontrole, ili zato što je pritisnut control+alt+delete), NVDA će objaviti činjenicu da je korisnik sada na sigurnoj radnoj površini.
* NVDA može najavljivati tekst ispod miša unutar prozora dos konzole.
* Podrška za automatizaciju korisničkog sučelja putem klijentskog API-ja za automatizaciju korisničkog sučelja dostupnog u sustavu Windows 7, kao i popravci za poboljšanje iskustva NVDA u sustavu Windows 7.
* NVDA se može konfigurirati da se automatski pokreće nakon što se prijavite u Windows. Opcija se nalazi u dijaloškom okviru Opće postavke.
* NVDA može čitati sigurne Windows zaslone kao što su Windows logon, control+alt+delete i zasloni User Account Control (UAC) u Windows XP i novijim verzijama. Čitanje zaslona za prijavu u sustav Windows može se konfigurirati iz dijaloškog okvira Opće postavke. (#97)
* Dodan je upravljački program za Brajeve retke Optelec ALVA BC6 serije.
* Kada pregledavate web dokumente, sada možete pritisnuti n i shift+n za preskakanje unaprijed i natrag pored blokova veza.
* Prilikom pregledavanja web dokumenata sada se prijavljuju ARIA orijentiri i možete se kretati naprijed i natrag kroz njih koristeći d i shift + d. (#192)
* Dijaloški okvir Popis veza dostupan prilikom pregledavanja web-dokumenata sada je postao dijaloški okvir Popis elemenata u kojem se mogu navesti veze, naslovi i orijentiri. Naslovi i orijentiri prikazani su hijerarhijski. (#363)
* Novi dijaloški okvir Popis elemenata sadrži polje "Filtriraj prema" koje vam omogućuje filtriranje popisa tako da sadrži samo one stavke, uključujući tekst koji je upisan. (#173)
* Prijenosne verzije NVDA sada traže korisnikovu konfiguraciju u direktoriju 'userConfig' unutar NVDA direktorija. Kao i za instalacijsku verziju, ovo drži korisnikovu konfiguraciju odvojenom od samog NVDA-a.
* Prilagođeni moduli aplikacija, upravljački programi za Brailleovo pismo i upravljački programi za sintisajzer sada se mogu pohraniti u korisnikov konfiguracijski direktorij. (#337)
* Virtualni međuspremniki sada se prikazuju u pozadini, omogućujući korisniku interakciju sa sustavom u određenoj mjeri tijekom procesa renderiranja. Korisnik će biti obaviješten da se dokument prikazuje ako traje dulje od sekunde.
* Ako NVDA otkrije da se iz nekog razloga zamrznuo, automatski će proslijediti sve pritiske tipki kako bi korisnik imao veće šanse za oporavak sustava.
* Podrška za ARIA povlačenje i ispuštanje u Mozilla Gecku. (#239)
* Naslov dokumenta i trenutačni redak ili odabir sada se izgovaraju kada premjestite fokus unutar virtualnog međuspremnika. To čini ponašanje pri premještanju fokusa u virtualne međuspremnike u skladu s onim za normalne objekte dokumenta. (#210)
* U virtualnim međuspremnikima sada možete komunicirati s ugrađenim objektima (kao što su Adobe Flash i Sun Java sadržaj) pritiskom na enter na objektu. Ako je dostupan, možete ga zaobići kao i bilo koju drugu aplikaciju. Za vraćanje fokusa na dokument pritisnite NVDA+razmaknica. (#431)
* U virtualnim međuspremnicima, o i Shift+o prelaze na sljedeći i prethodni ugrađeni objekt.
* NVDA sada može u potpunosti pristupiti aplikacijama koje se pokreću kao administrator u sustavu Windows Vista i novijim verzijama. Da bi ovo funkcioniralo, morate instalirati službeno izdanje NVDA-a. To ne funkcionira za prijenosne verzije i snimke. (#397)

### Promjenama

* NVDA više ne objavljuje "NVDA je započela" kada započne.
* Zvukovi pokretanja i izlaska sada se reproduciraju pomoću NVDA konfiguriranog audio izlaznog uređaja umjesto zadanog Windows audio izlaznog uređaja. (#164)
* Izvještavanje o traci napretka je poboljšano. Najznačajnije je to što sada možete konfigurirati NVDA tako da istovremeno najavljuje i govorom i zvučnim signalom.
* Neke generičke uloge, kao što su okno, aplikacija i okvir, više se ne prijavljuju u fokusu, osim ako kontrola nije neimenovana.
* Naredba kopiranja pregleda (NVDA+f10) kopira tekst od početnog markera do i uključujući trenutni položaj pregleda, a ne isključuje trenutni položaj. To omogućuje kopiranje posljednjeg znaka retka, što prije nije bilo moguće. (#430)
* navigatorObject_where skripta (ctrl+NVDA+numpad5) je uklonjena. Ova kombinacija tipki nije radila na nekim tipkovnicama, nore je otkriveno da je skripta toliko korisna.
* skripta navigatorObject_currentDimentions preimenovana je u NVDA+numpadDelete. Stara kombinacija tipki nije radila na nekim tipkovnicama. Ova skripta sada također izvješćuje o širini i visini objekta umjesto koordinata desno/dno.
* Poboljšane performanse (posebno na netbookovima) kada se javljaju mnogi zvučni signali u brzom nizu; npr. brzi pokreti miša s omogućenim audio koordinatama. (#396)
* Zvuk pogreške NVDA više se ne reproducira u kandidatima za izdavanje i konačnim izdanjima. Imajte na umu da su pogreške i dalje zabilježene.

### Ispravci grešaka

* Kada se NVDA pokreće s 8,3 dos puta, ali je instaliran na povezanom dugom putu (npr. programski ~1 verzija programskih datoteka), NVDA će ispravno  identificirati da se radi o instaliranoj kopiji i pravilno učitati korisničke postavke.
* izgovaranje naslova trenutnog prozora u prednjem planu s nvda +t sada radi ispravno kada je u izbornicima.
* brajica više ne prikazuje beskorisne informacije u kontekstu fokusa kao što su neoznačena okna.
* prestanite objavljivati neke beskorisne informacije kada se fokus promijeni, kao što su korijenska okna, slojevita okna i okna za pomicanje u Java ili Lotus aplikacijama.
* Učinite polje za pretraživanje ključnih riječi u pregledniku pomoći za Windows (CHM) mnogo korisnijim. Zbog buggynessa u toj kontroli, trenutna ključna riječ nije se mogla pročitati jer bi se kontinuirano mijenjala.
* prijaviti ispravne brojeve stranica u programu Microsoft Word ako je numeriranje stranica posebno pomaknuto u dokumentu.
* Bolja podrška za polja za uređivanje koja se nalaze u dijaloškim okvirima programa Microsoft Word (npr. dijaloški okvir Font). Sada je moguće kretati se ovim kontrolama pomoću tipki sa strelicama.
* bolja podrška za dos konzole. konkretno: NVDA sada može čitati sadržaj pojedinih konzola za koje je uvijek mislio da su prazne. Pritiskom na Control+Break više se ne prekida NVDA.
* U sustavu Windows Vista i novijem, NVDA instalater sada pokreće NVDA s uobičajenim korisničkim ovlastima kada se zatraži pokretanje NVDA na završnom zaslonu.
* Backspace se sada ispravno obrađuje prilikom izgovaranja upisanih riječi. (#306)
* Nemojte netočno prijaviti "izbornik Start" za određene kontekstne izbornike u programu Windows Explorer/ljusci sustava Windows. (#257)
* NVDA sada ispravno rukuje ARIA oznakama u Mozilla Gecko kada nema drugog korisnog sadržaja. (#156)
* NVDA više ne omogućuje automatski način fokusiranja za tekstualna polja koja se mogu uređivati i koja ažuriraju svoju vrijednost kada se fokus promijeni; npr. http://tigerdirect.com/. (#220)
* NVDA će se sada pokušati oporaviti od nekih situacija koje bi prethodno uzrokovale potpuno zamrzavanje. Može biti potrebno do 10 sekundi da NVDA otkrije i oporavi se od takvog smrzavanja.
* Kad je jezik NVDA podešen na "User default", koristite korisnikovu postavku jezika za Windows umjesto postavke za Windows locale. (#353)
* NVDA sada priznaje postojanje kontrola u CILJU 7.
* Naredba za prolaz više se ne zaglavi ako se tipka drži pritisnutom. Ranije je NVDA prestala prihvaćati naredbe ako se to dogodilo i morala se ponovno pokrenuti. (#413)
* Traka zadataka više se ne zanemaruje kada primi fokus, što se često događa pri izlasku iz aplikacije. Ranije se NVDA ponašala kao da se fokus uopće nije promijenio.
* Prilikom čitanja tekstualnih polja u aplikacijama koje koriste Java Access Bridge (uključujući OpenOffice.org), NVDA sada ispravno funkcionira kada je omogućeno izvješćivanje o brojevima redaka.
* Naredba kopiranja pregleda (NVDA+f10) graciozno obrađuje slučaj u kojem se koristi na položaju prije početnog markera. Ranije je to moglo uzrokovati probleme kao što su padovi u Notepadu++.
* Određeni kontrolni znak (0x1) više ne uzrokuje čudno ponašanje eSpeaka (kao što su promjene u glasnoći i visini tona) kada se pojavi u tekstu. (#437)
* Naredba za odabir teksta izvješća (NVDA+Shift+ strelica prema gore) sada graciozno izvješćuje da nema odabira u objektima koji ne podržavaju odabir teksta.
* Riješen je problem zbog kojeg je pritisak tipke Enter na određenim tipkama ili poveznicama Miranda-IM uzrokovao zamrzavanje NVDA-e. (#440)
* Trenutačni redak ili odabir sada se pravilno poštuje prilikom pravopisa ili kopiranja trenutnog objekta navigatora.
* Radila je oko greške u sustavu Windows koja je uzrokovala izgovaranje smeća nakon naziva kontrola veze u dijalozima programa Windows Explorer i Internet Explorer. (#451)
* Riješen je problem s naredbom datuma i vremena izvješća (NVDA+f12). Prethodno je izvješćivanje o datumima skraćeno na nekim sustavima. (#471)
* Riješen je problem u kojem je zastavica čitača zaslona sustava ponekad neprimjereno uklonjena nakon interakcije sa sigurnim zaslonima sustava Windows. To može uzrokovati probleme u aplikacijama koje provjeravaju zastavicu čitača zaslona, uključujući Skype, Adobe Reader i Jart. (#462)
* U kombiniranom okviru programa Internet Explorer 6 aktivna se stavka sada prijavljuje kada se promijeni. (#342)

## 0,6p3

### Nove značajke

* Budući da traka formule programa Microsoft Excel nije dostupna NVDA-u, navedite dijaloški okvir specifičan za NVDA za uređivanje kada korisnik pritisne f2 na ćeliju.
* Podrška za oblikovanje u IAccessible2 kontrolama teksta, uključujući Mozilla aplikacije.
* Pravopisne pogreške sada se mogu prijaviti gdje god je to moguće. To se može konfigurirati iz dijaloškog okvira postavki oblikovanja dokumenta.
* NVDA se može konfigurirati za zvučni signal za sve ili samo vidljive trake napretka. Alternativno, može se konfigurirati za izgovaranje vrijednosti trake napretka svakih 10%.
* Poveznice se sada mogu identificirati u richedit kontrolama.
* Miš se sada može premjestiti na znak ispod pokazivača za pregled u većini tekstualnih kontrola koje se mogu uređivati. Prethodno se miš mogao premjestiti samo u središte kontrole.
* U virtualnim međuspremnicima, pokazivač pregleda sada pregledava tekst međuspremnika, a ne samo interni tekst objekta navigatora (što često nije korisno za korisnika). To znači da se hijerarhijski možete kretati virtualnim međuspremnikom pomoću navigacije objekta i pokazivač pregleda će se pomaknuti na tu točku u međuspremniku.
* Upravljajte nekim dodatnim stanjima na Java kontrolama.
* Ako se naredba title (NVDA+t) pritisne dvaput, izgovara se title. Ako se pritisne tri puta, kopira se u međuspremnik.
* Pomoć na tipkovnici sada čita nazive tipki modifikatora kada se pritisne sama.
* Imena tipki koja je najavila pomoć tipkovnice sada se mogu prevesti.
* Dodana podrška za prepoznato tekstualno polje u SiRecognizeru. (#198)
* Podrška za brajeve zaslone!
* Dodana je naredba (NVDA+c) za prijavu teksta u međuspremnik sustava Windows. (#193)
* U virtualBuffersu, ako se NVDA automatski prebaci na način izoštravanja, možete upotrijebiti tipku za izlazak kako biste se vratili na način pregledavanja. NVDA+prostor se također može koristiti.
* U virtualnim međuspremnicima, kada se fokus promijeni ili se karter pomakne, NVDA se može automatski prebaciti u način izoštravanja ili način pretraživanja prema potrebi za kontrolu pod karterom. Ovo je konfigurirano iz dijaloškog okvira Virtual Buffers. (#157)
* Ponovno napisan upravljački program sapi4 sintetizatora koji zamjenjuje upravljačke programe sapi4serotek i sapi4activeVoice i trebao bi riješiti probleme s tim upravljačkim programima.
* Aplikacija NVDA sada uključuje manifest, što znači da se više ne pokreće u načinu kompatibilnosti u sustavu Windows Vista.
* Konfiguracijska datoteka i rječnici govora sada se spremaju u korisnikov direktorij podataka aplikacije ako je NVDA instaliran pomoću instalacijskog programa. To je potrebno za Windows Vista i također omogućuje više korisnika da imaju pojedinačne NVDA konfiguracije.
* Dodana podrška za informacije o položaju za IAccessible2 kontrole.
* Dodana je mogućnost kopiranja teksta u međuspremnik pomoću kursora za pregled. NVDA+f9 postavlja početni marker na trenutni položaj kursora za pregled. NVDA+f10 dohvaća tekst između početnog markera i trenutnog položaja kursora za pregled i kopira ga u međuspremnik. (#240)
* Dodana je podrška za neke kontrole uređivanja u Pinacle TV softveru.
* Kada najavljuje odabrani tekst za dugi odabir (512 znakova ili više), NVDA sada govori broj odabranih znakova, umjesto da govori cijeli odabir. (#249)

### Promjenama

* Ako je izlazni audio uređaj podešen za upotrebu zadanog uređaja sa sustavom Windows (Microsoft Sound Mapper), NVDA će se sada prebaciti na novi zadani uređaj za eSpeak i tonove kada se zadani uređaj promijeni. Na primjer, NVDA će se prebaciti na USB audio uređaj ako automatski postane zadani uređaj kada je spojen.
* Poboljšajte performanse eSpeaka s nekim Windows Vista audio upravljačkim programima.
* izvješćivanje o vezama, naslovima, tablicama, popisima i skupnim navodnicima sada se može konfigurirati iz dijaloškog okvira postavki oblikovanja dokumenta. Prethodno bi se za konfiguriranje ovih postavki za virtualne međuspremnike koristio dijaloški okvir za postavke virtualnog međuspremnika. Sada svi dokumenti dijele ovu konfiguraciju.
* Stopa je sada zadana postavka u prstenu postavki sintetizatora govora.
* Poboljšajte utovar i istovar appModula.
* Naredba title (NVDA+t) sada prijavljuje samo naslov umjesto cijelog objekta. Ako objekt u prednjem planu nema naziv, koristi se naziv procesa aplikacije.
* Umjesto uključivanja i isključivanja virtualnog međuspremnika, NVDA sada izvješćuje o načinu izoštravanja (uključivanje) i načinu pregledavanja (isključivanje).
* Glasovi se sada pohranjuju u konfiguracijsku datoteku prema ID-u umjesto prema indeksu. To čini glasovne postavke pouzdanijima u svim sustavima i promjenama konfiguracije. Glasovna postavka neće se sačuvati u starim konfiguracijama i može se zabilježiti pogreška pri prvoj uporabi sintisajzera. (#19)
* Razina stavke prikaza stabla sada se objavljuje prva ako se promijenila u odnosu na prethodno fokusiranu stavku za sve prikaze stabla. Prije se to događalo samo za izvorne prikaze stabla sustava Windows (SysTreeView32).

### Ispravci grešaka

* Posljednji dio zvuka više nije odsječen kada koristite NVDA s eSpeak na udaljenom računalnom poslužitelju.
* Riješite probleme s spremanjem govornih rječnika za određene glasove.
* Uklonite kašnjenje prilikom pomicanja jedinica koje nisu znakovi (riječ, redak itd.) prema dnu velikih dokumenata s običnim tekstom u virtualnim međuspremnicima Mozilla Gecko. (#155)
* Ako je omogućeno izgovaranje upisanih riječi, objavite riječ kada pritisnete Enter.
* Riješite neke probleme s skupom znakova u richedit dokumentima.
* NVDA preglednik zapisnika sada koristi richedit umjesto samo uređivanja za prikaz zapisnika. To poboljšava čitanje po riječi s NVDA-om.
* Riješite neke probleme povezane s ugrađenim objektima u richedit kontrolama.
* NVDA sada čita brojeve stranica u Microsoft Wordu. (#120)
* Riješite problem kada označavanje potvrdnog okvira u virtualnom međuspremniku Mozilla Gecko i pritiskanje razmaka ne bi objavilo da je potvrdni okvir poništen.
* Ispravno prijavite djelomično označene potvrdne okvire u Mozilla aplikacijama.
* Ako se odabir teksta proširi ili smanji u oba smjera, pročitajte odabir kao jedan komad umjesto dva.
* Kada čitate mišem, tekst u poljima za uređivanje Mozilla Gecko sada bi trebao biti pročitan.
* Recimo da svi više ne bi trebali uzrokovati pad određenih SAPI5 sintisajzera.
* Riješen je problem što je značilo da se promjene odabira teksta nisu čitale u Windows standardnim kontrolama uređivanja prije prve promjene fokusa nakon pokretanja NVDA.
* Popravite praćenje miša u Java objektima. (#185)
* NVDA više ne prijavljuje stavke prikaza Java stabla bez djece kao sažete.
* Najavite objekt s fokusom kada se u prvom planu pojavi Java prozor. Prethodno je najavljen samo Java objekt najviše razine.
* Upravljački program sintesajzera eSpeak više ne prestaje govoriti u potpunosti nakon jedne pogreške.
* Riješite problem zbog kojeg ažurirani parametri glasa (brzina, visina tona itd.) nisu spremljeni kada je glas promijenjen iz prstena za postavke sintetizatora.
* Poboljšano govorenje upisanih znakova i riječi.
* Sada se govori neki novi tekst koji ranije nije bio izgovoren u aplikacijama tekstualne konzole (kao što su neke tekstualne avanturističke igre).
* NVDA sada zanemaruje promjene fokusa u pozadinskim prozorima. Prethodno se promjena fokusa pozadine mogla tretirati kao da se pravi fokus promijenio.
* Poboljšano otkrivanje fokusa prilikom napuštanja kontekstnih izbornika. Ranije, NVDA često uopće nije reagirala kada je napuštala kontekstni izbornik.
* NVDA sada objavljuje kada je kontekstni izbornik aktiviran u izborniku Start.
* Klasični izbornik Start sada je najavljen kao izbornik Start umjesto izbornika Application.
* Poboljšano čitanje upozorenja poput onih koja se pojavljuju u Mozilla Firefoxu. Tekst se više ne smije čitati više puta i neće se više čitati druge strane informacije. (#248)
* Tekst polja za uređivanje koja se mogu fokusirati i samo za čitanje više neće biti uključen prilikom dohvaćanja teksta dijaloga. Time se, primjerice, popravlja automatsko čitanje cjelokupnog licencnog ugovora u instalaterima.
* NVDA više ne najavljuje poništavanje odabira teksta prilikom napuštanja nekih kontrola za uređivanje (primjer: adresna traka Internet Explorera, polja adrese e-pošte Thunderbirda 3).
* Prilikom otvaranja običnih tekstualnih poruka e-pošte u programima Outlook Express i Windows Mail, fokus je ispravno postavljen u poruku koja je spremna da je korisnik pročita. Prije toga korisnik je morao pritisnuti tabulator ili kliknuti na poruku kako bi je pročitao pomoću kursorskih tipki.
* Riješeno je nekoliko većih problema s funkcijom "Speak command keys".
* NVDA sada može čitati tekst iznad 65535 znakova u standardnim kontrolama uređivanja (npr. velika datoteka u Notepadu).
* Poboljšano čitanje redaka u poljima za uređivanje MSHTML-a (poruke koje se mogu uređivati u programu Outlook Express i polja za unos teksta u Internet Explorer).
* NVDA se ponekad više ne zamrzava u potpunosti prilikom uređivanja teksta u OpenOfficeu. (#148, #180)

## 0,6p2

* Poboljšan zadani ESpeak glas u NVDA-u
* Dodan je raspored tipkovnice prijenosnog računala. Rasporedi tipkovnice mogu se konfigurirati iz NVDA dijaloškog okvira za postavke tipkovnice. (#60)
* Podrška za grupiranje stavki u kontrolama SysListView32, koje se uglavnom nalaze u sustavu Windows Vista. (#27)
* Prijavite provjereno stanje stavki prikaza stabla u kontrolama SysTreeview32.
* Dodane su tipke prečaca za mnoge konfiguracijske dijaloge NVDA-a
* Podrška za IAccessible2 omogućene aplikacije kao što je Mozilla Firefox prilikom pokretanja NVDA s prijenosnih medija, bez potrebe za registracijom bilo kakvih posebnih Dll datoteka
* Popravite pad s popisom poveznica VirtualBuffers u Gecko aplikacijama. (#48)
* NVDA više ne bi trebao rušiti aplikacije Mozilla Gecko kao što su Firefox i Thunderbird ako NVDA radi s većim privilegijama od aplikacije Mozilla Gecko. Npr. NVDA radi kao administrator.
* Govorni rječnici (prethodno Korisnički rječnici) sada mogu biti osjetljivi na velika i mala slova ili neosjetljivi, a uzorci mogu opcionalno biti regularni izrazi. (#39)
* Bez obzira na to koristi li NVDA način "izgleda zaslona" za dokumente virtualnog međuspremnika, sada se može konfigurirati iz dijaloškog okvira s postavkama
* Više ne prijavljuje sidrene oznake bez href u Gecko dokumentima kao poveznice. (#47)
* Naredba NVDA find sada pamti ono što ste zadnji tražili, u svim aplikacijama. (#53)
* Riješite probleme u kojima označeno stanje ne bi bilo najavljeno za neke potvrdne okvire i radio gumbe u virtualBuffersu
* Način prijenosa VirtualBuffer sada je specifičan za svaki dokument, a ne za NVDA na globalnoj razini. (#33)
* Popravio je neku tromost s promjenama fokusa i netočnim prekidima govora koji su se ponekad javljali pri korištenju NVDA-a na sustavu koji je bio u stanju pripravnosti ili je bio prilično spor
* Poboljšajte podršku za kombinirane okvire u Mozilla Firefoxu. Konkretno, kada se strelice oko njih ne ponavljaju, a kada iskaču iz njih, kontrole predaka se ne najavljuju nepotrebno. Također, naredbe VirtualBuffer sada rade kada ste usredotočeni na jednu  kada ste u VirtualBufferu.
* Poboljšati točnost pronalaženja statusne trake u mnogim aplikacijama. (#8)
* Dodan je interaktivni alat konzole NVDA Python kako bi se programerima omogućilo da gledaju i manipuliraju internim podacima NVDA dok je pokrenut
* sayAll, reportSelection i reportCurrentLine skripte sada rade ispravno kada su u virtualnomBuffer prolazu. (#52)
* Skripte za povećanje i smanjenje brzine su uklonjene. Korisnici bi trebali koristiti skripte prstena sintetskih postavki (kontrola+nvda+strelice) ili dijaloški okvir Glasovne postavke
* Poboljšajte raspon i skalu zvučnih signala trake napretka
* Dodano je više brzih tipki novim virtualnim baferima:  l za popis, i za stavku popisa, e za polje za uređivanje, b za gumb, x za potvrdni okvir, r za radio gumb, g za grafiku, q za blockquote, c za kombinirani okvir, 1 do 6 za odgovarajuće razine naslova, s za separator, m za okvir. (#67, #102, #108)
* Otkazivanje učitavanja novog dokumenta u Mozilla Firefox sada omogućuje korisniku da nastavi koristiti virtualni bafer starog dokumenta ako stari dokument još nije stvarno uništen. (#63)
* Navigacija po riječima u virtualBuffersu sada je točnija jer  riječi ne sadrže slučajno tekst iz više od jednog polja. (#70)
* Poboljšana točnost praćenja fokusa i ažuriranja fokusa prilikom navigacije u Mozilla Gecko virtualBuffers.
* Dodana je skripta findPrevious (Shift+NVDA+f3) za uporabu u novim virtualnim baferima
* Poboljšana tromost u dijalozima Mozilla Gecko (u Firefoxu i Thunderbirdu). (#66)
* Dodajte mogućnost pregleda trenutne datoteke dnevnika za NVDA. možete ga pronaći u NVDA izborniku -> Alati
* Skripte kao što su vrijeme i datum sada uzimaju u obzir trenutni jezik; interpunkcija i redoslijed riječi sada odražavaju jezik
* Kombinirani okvir za jezik u dijaloškom okviru Opće postavke NVDA-a sada prikazuje pune nazive jezika radi lakšeg korištenja
* Prilikom pregleda teksta u trenutnom objektu navigatora, tekst je uvijek ažuran ako se dinamički mijenja. Npr. pregled teksta stavke popisa u Upravitelju zadacima. (#15)
* Kada se krećete mišem, sada se najavljuje trenutni odlomak teksta ispod miša, a ne bilo sav tekst u tom određenom objektu ili samo trenutna riječ. Također, audio koordinate i najava uloga objekta nisu obavezni, oni su prema zadanim postavkama isključeni
* Podrška za čitanje teksta pomoću miša u programu Microsoft Word
* Ispravljena pogreška gdje bi napuštanje trake izbornika u aplikacijama kao što je Wordpad uzrokovalo da se odabir teksta više ne objavljuje
* U Winampu se naslov pjesme više ne objavljuje iznova i iznova prilikom prebacivanja pjesama ili pauziranja/nastavljanja/zaustavljanja reprodukcije.
* U Winampu  je dodana mogućnost najave stanja miješanja i ponavljanja kontrola prilikom prebacivanja. Radi u glavnom prozoru i u uređivaču popisa za reprodukciju
* Poboljšajte mogućnost aktiviranja određenih polja u Mozilla Gecko virtualBuffers. Može uključivati grafike na koje se može kliknuti, poveznice koje sadrže odlomke i druge čudne strukture
* Fiksno početno kašnjenje prilikom otvaranja NVDA dijaloga na nekim sustavima. (#65)
* Dodajte posebnu podršku za aplikaciju Total Commander
* Popravite grešku u upravljačkom programu sapi4serotek gdje bi se visina tona mogla zaključati na određenoj vrijednosti, tj. ostati visoka nakon čitanja velikog slova. (#89)
* Najavite tekst koji se može kliknuti i druga polja kao ona koja se mogu kliknuti u Mozilla Gecko VirtualBuffersu. npr. polje koje ima HTML atribut onclick. (#91)
* Kada se krećete Mozilla Gecko virtualBuffers, pomičite se trenutnim poljem za prikaz -- korisno kako bi viđeni vršnjaci imali predodžbu o tome gdje se korisnik nalazi u dokumentu. (#57)
* Dodajte osnovnu podršku za ARIA live region show događaje u IAccessible2 omogućenim aplikacijama. Korisno u aplikaciji Chatzilla IRC, nove će se poruke sada automatski čitati
* Neka neznatna poboljšanja za pomoć u korištenju web-aplikacija s omogućenom aplikacijom ARIA,  npr. Google Dokumenti
* Prestani dodavati dodatne prazne retke u tekst prilikom kopiranja iz virtualnog bafera
* Zaustavite da razmaknica aktivira poveznicu na Popisu poveznica. Sada se može koristiti kao i druga slova kako biste  počeli upisivati naziv određene poveznice na koju želite otići
* Skripta moveMouseToNavigator (NVDA+ numpadSlash) sada pomiče miš u središte objekta navigatora, a ne gore lijevo
* Dodane su skripte za klik lijeve i desne tipke miša (numpadSlash i numpadStar)
* Poboljšajte pristup pretincu sustava Windows. Nadamo se da se fokus više neće vraćati na jednu određenu stavku. Podsjetnik: za pristup traci sustava koristite Windows naredbu WindowsKey +b. (#10)
* Poboljšajte performanse i prestanite najavljivati dodatni tekst kada držite tipku pokazivača u polju za uređivanje i ona dođe do kraja
* Zaustavite mogućnost da NVDA natjera korisnika da čeka dok se izgovaraju određene poruke. Popravlja neke padove/zamrzavanja s određenim sintesajzerima govora. (#117)
* Dodana podrška za sintisajzer govora Audiologic TTS3, doprinos Gianluce Casalina. (#105)
* Moguće poboljšanje performansi prilikom navigacije po dokumentima u programu Microsoft Word
* Poboljšana točnost prilikom čitanja teksta upozorenja u aplikacijama Mozilla Gecko
* Zaustavite moguće padove prilikom pokušaja spremanja konfiguracije na verzijama sustava Windows koje nisu na engleskom jeziku. (#114)
* Dodajte NVDA dijaloški okvir dobrodošlice. Ovaj dijalog osmišljen je kako bi pružio bitne informacije novim korisnicima i omogućuje konfiguriranje CapsLocka kao NVDA modifikacijskog ključa. Ovaj će se dijaloški okvir prikazati kada se NVDA pokrene prema zadanim postavkama dok se ne onemogući.
* Popravite osnovnu podršku za Adobe Reader tako da je moguće čitati dokumente  u  verzijama 8 i 9
* Ispravite neke pogreške koje su se mogle pojaviti prilikom držanja tipki prije nego što se NVDA pravilno inicijalizira
* Ako je korisnik konfigurirao NVDA za spremanje konfiguracije pri izlasku, provjerite je li konfiguracija pravilno spremljena prilikom isključivanja ili odjave iz  sustava Windows.
* Početku instalatera dodan je zvuk logotipa NVDA, koji je pridonio Victer Tsaran
* NVDA, koji radi u instalacijskom programu i na drugi način, trebao bi pravilno očistiti ikonu svoje ladice sustava kada izađe
* Oznake za standardne kontrole u dijalozima NVDA-a (kao što su gumbi U redu i Otkaži) sada bi se trebale prikazivati na jeziku na kojem je postavljen NVDA, a ne samo na engleskom jeziku.
* Ikona NVDA sada bi  se trebala koristiti za prečace NVDA u izborniku Start i na radnoj površini, a ne zadana ikona aplikacije.
* Čitanje ćelija u MS Excelu prilikom premještanja pomoću kartice i Shift+kartica. (#146)
* Popravite neke dvostruke govore u određenim popisima u Skypeu.
* Poboljšano praćenje kareta u IAccessible2 i Java aplikacijama; npr. u Open Office i Lotus Symphony, NVDA ispravno čeka da se karet pomakne u dokumentima, umjesto da slučajno pročita pogrešnu riječ ili redak na kraju nekih odlomaka. (#119)
* Podrška za AkelEdit kontrole pronađene u Akelpad 4.0
* NVDA se više ne zaključava u Lotus Synphony prilikom prelaska s dokumenta na traku izbornika.
* NVDA se više ne zamrzava u programu za dodavanje/uklanjanje programa u sustavu Windows XP prilikom pokretanja programa za deinstalaciju. (#30)
* NVDA se više ne zamrzava kada se otvori Spybot Search and Destroy

## 0,6p1

### Pristup web-sadržaju s novim virtualnim baferima (za sada za aplikacije Mozilla Gecko, uključujući Firefox3 i Thunderbird3)

* Vrijeme učitavanja poboljšano je gotovo za faktor trideset (više uopće ne morate čekati da se većina web stranica učita u međuspremnik)
* Dodan je popis poveznica (NVDA+f7)
* Poboljšan je dijaloški okvir za pronalaženje (kontrola+nvda+f) kako bi se provelo pretraživanje neosjetljivo na velika i mala slova, a riješeno je i nekoliko problema s fokusom u tom dijaloškom okviru.
* Sada je moguće odabrati i kopirati tekst u novim virtualnim baferima
* Prema zadanim postavkama novi virtualni baferi predstavljaju dokument u izgledu zaslona (poveznice i kontrole nisu u odvojenim linijama, osim ako stvarno nisu vizualno). Ovu značajku možeš promijeniti pomoću opcije NVDA+v.
* Moguće je pomicati se po odlomku s kontrolom+ strelicom prema gore i kontrolom+ strelicom prema dolje.
* Poboljšana podrška za dinamički sadržaj
* Poboljšano u odnosu na svu točnost linija i polja čitanja prilikom strelica gore i dolje.

### Internacionalizacija

* Sada je moguće upisivati naglašene znakove koji se oslanjaju na "mrtav znak", dok je NVDA pokrenut.
* NVDA sada objavljuje kada se raspored tipkovnice promijeni (kada pritisnete Alt+Shift).
* Značajka najave datuma i vremena sada uzima u obzir trenutačne regionalne i jezične opcije sustava.
* dodan češki prijevod (autor Tomas Valusek uz pomoć Jaromira Vita)
* dodao vijetnamski prijevod Dang Hoai Phuc
* Dodan prijevod Afrikanaca (af_ZA), Willema van der Walta.
* Dodaje ruski prijevod Dmitryja Kaslina
* Dodan poljski prijevod DOROTE CZAJKE i prijatelja.
* Dodan je japanski prijevod Katsutoshija Tsujija.
* dodao je tajlandski prijevod Amorn Kiattikhunrat
* dodan hrvatski prijevod Marija Percinića i Hrvoja Katića
* Dodan galicijski prijevod Juana C. bunoa
* dodao ukrajinski prijevod Aleksey Sadovoy

### Govor

* NVDA sada dolazi u paketu s eSpeak 1.33 koji sadrži mnoga poboljšanja, među kojima su poboljšani jezici, imenovane varijante, sposobnost bržeg govora.
* Dijaloški okvir za glasovne postavke sada vam omogućuje promjenu varijante sintisajzera ako ga podržava. Varijanta je obično mala varijacija na trenutni glas. (eSpeak podržava varijante).
* Dodana je mogućnost promjene infleksije glasa u dijaloškom okviru postavki glasa ako trenutni sintetizator to podržava. (eSpeak podržava infleksiju).
* Dodana je mogućnost isključivanja govora o informacijama o položaju objekta (npr. 1 od 4). Ova se opcija može pronaći u dijaloškom okviru Postavke prezentacije objekta.
* NVDA se sada može oglasiti zvučnim signalom kada govori velikim slovom. To se može uključiti i isključiti potvrdnim okvirom u dijaloškom okviru za glasovne postavke. Također je dodan potvrdni okvir za povećanje visine tona za glavne gradove kako bi se konfiguriralo treba li NVDA zapravo izvršiti uobičajeno povećanje visine tona za glavne gradove. Dakle, sada možete imati ili podizanje tona, recimo kapu, ili zvučni signal, za velika slova.
* Dodana je mogućnost pauziranja govora u NVDA-u (kao što je pronađeno u Voice Over za Mac). Kad NVDA nešto govori, možete pritisnuti tipke Control ili Shift kako biste utišali govor kao i obično, ali ako zatim ponovno dodirnete tipku Shift (sve dok ne pritisnete nijednu drugu tipku), govor će se nastaviti točno tamo gdje je stao.
* Dodan je virtualni synthDriver koji šalje tekst u prozor umjesto da govori putem sintetizatora govora. To bi trebalo biti ugodnije vidnim programerima koji nisu navikli na sintezu govora, ali žele znati što govori NVDA. Vjerojatno još uvijek ima nekih pogrešaka, pa su povratne informacije svakako dobrodošle.
* NVDA više prema zadanim postavkama ne govori interpunkciju, možete omogućiti govorenje interpunkcije s NVDA+str.
* eSpeak prema zadanim postavkama sada govori prilično sporije, što bi trebalo olakšati ljudima koji prvi put koriste eSpeak, prilikom instaliranja ili početka korištenja NVDA.
* Dodani korisnički rječnici u NVDA. Omogućavaju izgovor teksta na drugačiji način. Postoje tri tipa rječnika: podrazumjevani, glasovnii privremeni. Upisi koji budu dodani u glavni rječnik, izvršavat će se svaki put. Glasovni rječnici se odnose na postavljeni glas i govornu jedinicu. A privremeni rječnici služe za testiranje nekog pravila (nestat će kada se ponovno pokrene NVDA). Za sada, pravila se sastoje od regularnih izraza, ne samo pravilnog teksta.
* Sintetizatori sada mogu koristiti bilo koji izlazni audio uređaj na vašem sustavu, postavljanjem kombiniranog okvira izlaznog uređaja u dijaloškom okviru Sintetizatora prije odabira željenog sintetizatora.

### performanse

* NVDA više ne zauzima veliku količinu sistemske memorije prilikom uređivanja poruka u mshtml kontrolama za uređivanje
* Poboljšane performanse prilikom pregleda teksta unutar mnogih kontrola koje zapravo nemaju pravi kursor. npr. Prozor povijesti MSN Messengera, stavke prikaza stabla, stavke prikaza popisa itd.
* Poboljšane performanse u bogatim dokumentima za uređivanje.
* NVDA se više ne bi trebao polako uvlačiti u veličinu memorije sustava bez razloga
* Otklonjene su pogreške kada se pokušavate usredotočiti na prozor konzole DOS-a više od tri puta. NVDA je imala tendenciju da se potpuno sruši.

### &Naredbe tipki

* NVDA+SHIFT+NUMPAD6 i NVDA+SHIFT+NUMPAD4 omogućuju vam da se krećete do sljedećeg ili prethodnog objekta u protoku. To znači da u aplikaciji možete kretati samo pomoću ova dva ključeva, bez da se brinete o tome da se roditelja podigne ili dolje do prvog djeteta dok se krećete oko objekta Hyerarhije. Na primjer, u web -pregledniku kao što je Firefox, možete se kretati dokumentom prema objektu, samo pomoću ove dvije tipke. Ako vas sljedeći u protoku ili prethodnom protoku odvede gore i izvan objekta ili dolje u objekt, uređeni zvučni signali ukazuju na smjer.
* Sada možete konfigurirati glasovne postavke bez otvaranja dijaloškog okvira za glasovne postavke, pomoću prstena za postavke sint. Prsten za postavke sinkronizacije skupina je glasovnih postavki koje možete mijenjati pritiskom na Control+NVDA+right i Control+NVDA+left. Za promjenu postavke koristite Control+NVDA+gore i Control+NVDA+dolje.
* Dodana je naredba za izvješćivanje o trenutačnom odabiru u poljima za uređivanje (NVDA+Shift+ strelica prema gore).
* Dosta NVDA naredbi koje govore tekst (kao što je tekući redak izvješća itd.) sada mogu pisati tekst ako se pritisnu dvaput brzo.
* Capslock, NumPad Insert i prošireni umetak mogu se koristiti kao tipka NVDA modifikatora. Također ako se koristi jedan od ovih tipki, pritiskom na tipku dvaput pritiskom na pritisak na bilo koje druge tipke poslat će tipku u operativni sustav, baš kao što ste pritisnuli tipku s pokretanjem NVDA. Da biste jedan od ovih tipki bili tipka NVDA modifikator, provjerite njegov potvrdni okvir u dijaloškom okviru postavki tipkovnice (nekada se naziva dijaloški okvir tipkovnice Echo).

### Aplikacijska podrška

* Poboljšana podrška dokumentima Firefox3 i Thunderbird3. Vremena učitavanja poboljšana su gotovo trideset, izgled zaslona koristi se prema zadanim postavkama (pritisnite nvda+v za prebacivanje između ovog i bez izgleda zaslona), dodan je popis veza (NVDA+F7), dijalog za pronalaženje ( Control+NVDA+F) sada je neosjetljiva na slučaj, sada je moguća puno bolja podrška za dinamički sadržaj, odabir i kopiranje teksta sada je moguće.
* U prozorima povijesti programa MSN Messenger i Windows Live Messenger sada je moguće odabrati i kopirati tekst.
* Poboljšana podrška za aplikaciju Audacity
* Dodana je podrška za nekoliko kontrola uređivanja/teksta u Skypeu
* Poboljšana podrška za aplikaciju Miranda instant messenger
* Riješeni su neki problemi s fokusom prilikom otvaranja html i običnih tekstualnih poruka u programu Outlook Express.
* Polja s porukama grupe novosti programa Outlook Express sada su ispravno označena
* NVDA sada može čitati adrese u poljima poruka programa Outlook Express (za/od/cc itd.)
* NVDA bi sada trebao biti točniji pri objavljivanju sljedeće poruke u out look expressu prilikom brisanja poruke s popisa poruka.

### API-ji i alati

* Poboljšana navigacija objektima za MSAA objekte. Ako prozor ima izbornik sustava, naslovnu traku ili klizne trake, sada ih možete otvoriti.
* Dodana je podrška za IAccessible2 accessibility API. Kao dio mogućnosti najave više vrsta kontrola, to također omogućuje NVDA-u pristup pokazivaču u aplikacijama kao što su Firefox 3 i Thunderbird 3, omogućujući vam navigaciju, odabir ili uređivanje teksta.
* Dodana podrška za Scintilla kontrole uređivanja (takve kontrole možete pronaći u Notepad++ ili Tortoise SVN).
* Dodana podrška za Java aplikacije (putem Java Access Bridge). To može pružiti osnovnu podršku za Open Office (ako je Java omogućena) i bilo koju drugu samostalnu Java aplikaciju. Imajte na umu da java apleti u web-pregledniku možda još ne rade.

### Miš

* Poboljšana podrška za čitanje onoga što se nalazi pod pokazivačem miša dok se kreće. Sada je mnogo brži, a sada ima i mogućnost u nekim kontrolama kao što su standardna polja uređivanja, Java i IACCEssible2 kontrola, čitati trenutnu riječ, a ne samo trenutni objekt. Ovo bi moglo biti od nekih vizija ometalo ljude koji samo žele pročitati određeni dio teksta s mišem.
* Dodana je nova opcija konfiguracije, pronađena u dijaloškom okviru Postavke miša. Reproducirajte zvuk kada se miš, kad se provjeri, svira 40 ms zvučni signal svaki put kada se miš pomiče, sa svojim tonom (između 220 i 1760 Hz) koji predstavlja osi Y, a lijevo/desno volumen, što predstavlja X osi. To omogućava slijepoj osobi da dobije grubu ideju gdje je miš na ekranu dok se pomiče. Ova značajka također ovisi o tome da je i reportObjectUnderMouse također uključen. To znači da ako brzo trebate onemogućiti i zvučne signale i najavljivanje objekata, samo pritisnite NVDA+M. Zžnosnici su također glasniji ili mekši, ovisno o tome koliko je zaslon u tom trenutku svijetli.

### Prezentacija i interakcija objekta

* Poboljšana podrška za najčešće kontrole prikaza stabla. NVDA vam sada govori koliko je stavki u podružnici kada je proširite. Također objavljuje razinu prilikom ulaska i izlaska iz grana. I, najavljuje trenutni broj stavke i broj stavki, prema trenutnoj grani, a ne cijelom prikazu stabla.
* Poboljšano je ono što se najavljuje kada se fokus promijeni dok se krećete po aplikacijama ili operativnom sustavu. Sada umjesto da samo čujete kontrolu na koju se spuštate, čujete informacije o svim kontrolama u kojima je ova kontrola smještena. Na primjer, ako odaberete karticu i sletite na gumb unutar grupnog okvira, grupni okvir će također biti objavljen.
* NVDA sada pokušava izgovoriti poruku unutar mnogih dijaloških okvira kako se pojavljuju. To je uglavnom točno, iako još uvijek postoji mnogo dijaloga koji nisu tako dobri kao što bi mogli biti.
* Dodan je potvrdni okvir za opise objekta izvješća u dijaloški okvir postavki prezentacije objekta. Napredni korisnici možda će ponekad htjeti poništiti ovu opciju kako bi spriječili NVDA da objavi mnogo dodatnih opisa na određenim kontrolama,  kao što je to slučaj u Java aplikacijama.
* NVDA automatski najavljuje odabrani tekst u kontrolama uređivanja kada se fokus pomakne na njih. Ako nema odabranog teksta, tada samo najavljuje trenutni redak kao i obično.
* NVDA je sada mnogo pažljivija kada reproducira zvučne signale kako bi ukazala na promjene trake napretka u aplikacijama. Više ne ludi u aplikacijama Eclipse kao što su Lotus Notes/Symphony i Accessibility Probe.

### Korisničko sučelje

* Uklonio je prozor NVDA sučelja i zamijenio ga jednostavnim skočnim izbornikom NVDA.
* Dijaloški okvir postavki korisničkog sučelja NVDA-a sada se naziva Opće postavke. Također sadrži dodatnu postavku: kombinirani okvir za postavljanje razine zapisnika, za poruke koje bi trebale ići u datoteku zapisnika NVDA. Imajte na umu da se NVDA datoteka zapisnika sada naziva nvda.log, a ne debug.log.
* Uklonjeno je polje za potvrdu naziva grupe objekta izvješća iz dijaloškog okvira postavki prezentacije objekta, izvješćivanje o nazivima grupa sada se obrađuje drugačije.

## 0,5

* NVDA sada ima ugrađeni sintisajzer nazvan eSpeak, koji je razvio Jonathan Duddington. Vrlo je odzivan i lagan te ima podršku za mnoge različite jezike. Sapi sintetizatori i dalje se mogu koristiti, ali eSpeak će se koristiti prema zadanim postavkama.
 * eSpeak ne ovisi o bilo kojem posebnom softveru koji se instalira, tako da se može koristiti s NVDA-om na bilo kojem računalu, na USB memoriji ili bilo gdje.
 * Za više informacija o eSpeaku ili za pronalaženje drugih verzija posjetite http://espeak.sourceforge.net/.
* Ispravite pogrešku kod najave pogrešnog znaka kada pritisnete Delete u oknima koja se mogu uređivati u pregledniku Internet Explorer / Outlook Express.
* Dodana je podrška za više polja za uređivanje u Skypeu.
* VirtualBuffers se učitavaju samo kada je fokus na prozoru koji treba učitati. To rješava neke probleme kada je okno za pregled uključeno u programu Outlook Express.
* Dodani argumenti naredbenog retka u NVDA:
 * -m, --minimal: nemojte reproducirati zvukove pokretanja/izlaska i nemojte prikazivati sučelje pri pokretanju ako je tako podešeno.
 * -q, --quit: zatvorite bilo koju drugu već pokrenutu instancu NVDA-a, a zatim izađite
 * -s, --stderr-datotekaName: navedite gdje bi NVDA trebao postaviti neulovljene pogreške i iznimke
 * -d, --debug-datotekaName: navedite gdje bi NVDA trebao postaviti poruke za ispravljanje pogrešaka
 * -c, --config-datoteka: navedite alternativnu konfiguracijsku datoteku
 * -h, -help: prikaži argumente naredbenog retka za unos poruke pomoći
* Fiksna pogreška gdje se simboli interpunkcije ne bi preveli na odgovarajući jezik, kada se koristi jezik koji nije engleski i kada je uključen govor upisanih znakova.
* Datoteke na slovačkom jeziku dodao je Peter Vagner
* Dodan je dijaloški okvir za postavke virtualnog međuspremnika i dijaloški okvir za postavke oblikovanja dokumenta, od Petera Vagnera.
* Dodan francuski prijevod zahvaljujući Michelu Takvom
* Dodana je skripta za uključivanje i isključivanje zvučnog signala traka napretka (INSERT+u). Doprinosi Peter Vagner.
* Omogućio je da se više poruka u NVDA može prevesti na druge jezike. To uključuje opise skripti kada ste u pomoći tipkovnicom.
* VirtualBuffersu (Internet Explorer i Firefox) dodan je dijaloški okvir za pronalaženje. Pritiskom na Control+f na stranici otvara se dijaloški okvir u koji možete upisati tekst koji želite pronaći. Pritiskom tipke Enter tražit će se ovaj tekst i postaviti kursor VirtualBuffer na ovaj redak. Pritiskom na f3 također će se tražiti sljedeća pojava teksta.
* Kad je uključeno izgovaranje unesenih znakova, sada bi se trebalo izgovoriti više znakova. Tehnički, sada se mogu govoriti ascii znakovi od 32 do 255.
* Preimenovane su neke vrste kontrola radi bolje čitljivosti. Tekst koji se može uređivati sada se uređuje, kontura je sada prikaz stabla, a tipka je sada gumb.
* Prilikom strelice oko stavki popisa u popisu ili stavki prikaza stabla u prikazu stabla, vrsta kontrole (stavka popisa, stavka prikaza stabla) više se ne izgovara kako bi se ubrzala navigacija.
* Ima skočni prozor (koji označava da izbornik ima podizbornik) koji se sada izgovara kao podizbornik.
* Ako neki jezik koristi kontrolu i alt (ili altGR) za unos posebnog znaka, NVDA će sada govoriti ove znakove kada je uključen govor upisanih znakova.
* Riješeni su neki problemi s pregledom statičkih kontrola teksta.
* Zahvaljujući Coscell Kao dodan je prijevod za tradicionalni kineski.
* Restrukturiran je važan dio NVDA koda, koji bi sada trebao riješiti mnoge probleme s korisničkim sučeljem NVDA-a (uključujući dijaloge s postavkama).
* Dodana je podrška za Sapi4 u NVDA. Trenutačno postoje dva upravljačka programa sapi4, jedan na temelju koda koji je pridonijela tvrtka Serotek Corporation, a drugi koristi sučelje ActiveVoice.ActiveVoice com. Oba vozača imaju problema. Pogledaj koji ti najviše odgovara.
* Sada kada pokušavate pokrenuti novu kopiju NVDA dok je starija kopija još uvijek pokrenuta, nova kopija će se samo zatvoriti. To rješava veliki problem kada pokretanje više kopija NVDA-a čini vaš sustav vrlo neupotrebljivim.
* Preimenovan je naziv NVDA korisničkog sučelja iz NVDA sučelja u NVDA.
* Ispravljena je pogreška u programu Outlook Express gdje bi pritisak na backspace na početku poruke koja se može uređivati uzrokovao pogrešku.
* Dodana zakrpa od Rui Batiste koja dodaje skriptu za prijavu trenutnog stanja baterije na prijenosnim računalima (INSERT+Shift+b).
* Dodan je upravljački program za sintisajzer pod nazivom Silence. Ovo je sintisajzer koji ne govori ništa, omogućujući NVDA da ostane potpuno tih u svakom trenutku. Na kraju bi se to moglo koristiti zajedno s podrškom za Braillevo pismo, kada ga budemo imali.
* Postavka CapitalPitchChange za sintisajzere dodana je zahvaljujući J.J. Meddaughu
* Dodana zakrpa od J.J. Meddaugha koja čini objekte za prebacivanje izvješća pod skriptom miša više kao i druge skripte za prebacivanje (reći uključivanje/isključivanje umjesto mijenjanja cijele izjave).
* Dodano španjolsko prevođenje (i) koje je priložio Juan C. buo.
* Dodana datoteka na mađarskom jeziku od Tamasa Gczyja.
* Dodana datoteka na portugalskom jeziku iz Rui Batiste.
* Promjena glasa u dijaloškom okviru postavki glasa sada postavlja klizače brzine, visine i glasnoće na nove vrijednosti prema sintisajzeru, a ne prisiljavanje sintisajzera da se postavi na stare vrijednosti. To rješava probleme u kojima se čini da sintisajzer poput rječitosti ili putem glasa govori mnogo brže od svih ostalih sintisajzera.
* Ispravljena je pogreška u kojoj bi se govor zaustavio ili bi se NVDA u potpunosti srušio u prozoru konzole Dos.
* Ako postoji podrška za određeni jezik, NVDA sada može automatski prikazati svoje sučelje i izgovoriti svoje poruke na jeziku na kojem je postavljen Windows. Određeni jezik i dalje se može ručno odabrati i iz dijaloškog okvira postavki korisničkog sučelja.
* Dodana je skripta 'toggleReportDynamicContentChanges' (umetnite+5). To uključuje automatsku objavu novog teksta ili drugih dinamičkih promjena. Zasad to funkcionira samo u sustavu Dos Console Windows.
* Dodana je skripta 'toggleCaretMovesReviewCursor' (umetnite+6). Ovim se prebacuje treba li se pokazivač pregleda automatski premjestiti kada se pomiče pokazivač sustava. To je korisno u prozorima Dos konzole kada pokušavate čitati informacije dok se zaslon ažurira.
* Dodana je skripta 'toggleFocusMovesNavigatorObject' (umetnuti+7). Ovo mijenja je li objekt navigatora premješten na objekt s fokusom dok se mijenja.
* Dodana je neka dokumentacija prevedena na različite jezike. Do sada postoje francuski, španjolski i finski.
* Uklonio je neku razvojnu dokumentaciju iz binarne distribucije NVDA, sada je tek u izvornoj verziji.
* Ispravljena je moguća pogreška u programima Windows Live Messanger i MSN Messenger gdje bi strelica gore i dolje po popisu kontakata uzrokovala pogreške.
* Nove se poruke sada automatski izgovaraju kada se u razgovoru koristi Windows Live Messenger. (zasad vrijedi samo za verzije na engleskom jeziku)
* Prozor povijesti u razgovoru sa sustavom Windows Live Messenger sada se može pročitati pomoću tipki sa strelicama. (Zasad radi samo za verzije na engleskom jeziku)
* Dodana skripta 'passNextKeyThrough' (umetnuti+f2). Pritisnite ovu tipku, a zatim će se sljedeća pritisnuta tipka proslijediti izravno u sustav Windows. To je korisno ako morate pritisnuti određenu tipku u aplikaciji, ali NVDA koristi tu tipku za nešto drugo.
* NVDA se više ne zamrzava dulje od minute pri otvaranju vrlo velikih dokumenata u MS Wordu.
* Ispravljena je pogreška pri izlasku iz tablice u MS Wordu, a zatim ponovnom ulasku, što je uzrokovalo da se trenutni brojevi redaka/stupaca ne izgovaraju ako se vratite u potpuno istu ćeliju.
* Kada pokrenete NVDA sa sintesajzerom koji ne postoji ili ne radi, sapi5 sintisajzer će se pokušati učitati umjesto sapi5, ili ako sapi5 ne radi, onda će govor biti utišan.
* Skripte za povećanje i smanjenje stope više ne mogu imati stopu iznad 100 ili ispod 0.
* Ako dođe do pogreške s jezikom prilikom odabira u dijaloškom okviru Postavke korisničkog sučelja, okvir za poruku upozorit će korisnika na to.
* NVDA sada pita treba li spremiti konfiguraciju i ponovno pokrenuti ako je korisnik upravo promijenio jezik u dijaloškom okviru za postavke korisničkog sučelja. NVDA se mora ponovno pokrenuti kako bi promjena jezika u potpunosti stupila na snagu.
* Ako se sintisajzer ne može učitati, prilikom odabira iz dijaloškog okvira sintisajzera, okvir s porukom upozorava korisnika na to.
* Prilikom prvog učitavanja sintisajzera, NVDA omogućuje sintisajzeru da odabere najprikladnije parametre glasa, brzine i visine tona, umjesto da ga prisiljava na zadane vrijednosti za koje smatra da su u redu. To rješava problem u kojem sintisajzeri Eloquence i Viavoice sapi4 po prvi put počinju govoriti prebrzo.
