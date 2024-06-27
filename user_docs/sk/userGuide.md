# NVDA NVDA_VERSION Používateľská príručka

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Zoznam príkazov -->



## Úvod {#Introduction}

Vitajte v NVDA!

NonVisual Desktop Access (NVDA) je voľne šíriteľný open-source čítač obrazovky pre operačný systém Windows.
Pomocou hlasového a hmatového výstupu umožňuje nevidiacim a zrakovo postihnutým používateľom pristupovať k PC so systémom Windows za rovnakú cenu ako vidiacim osobám.
Vývoj NVDA zastrešuje organizácia [NV Access](https://www.nvaccess.org/), za pomoci príspevkov od členov komunity.

### Všeobecné vlastnosti {#GeneralFeatures}

NVDA umožňuje nevidiacim a zrakovo postihnutým prístup a interakciu s operačným systémom Windows a množstvom ďalších voliteľných aplikácií.

Na YouTube kanály NV Access je k dispozícii krátke demonštračné video s názvom ["Čo je NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo).

Najvýznamnejšie prednosti programu:

* Podpora pre populárne aplikácie vrátane internetových prehliadačov, emailových klientov, programov slúžiacich na okamžitú komunikáciu a kancelárskych balíkov
* Vstavaný hlasový výstup, ktorý podporuje viac než 80 jazykov
* Oznamovanie informácií o formátovaní ako napríklad názov a veľkosť písma, štýl textu a pravopisné chyby
* Automatické oznamovanie textu pod kurzorom myši a voliteľné akustické oznamovanie pozície kurzora myši
* Podpora množstva brailových zobrazovačov vrátane písania na riadkoch, ktoré majú brailovú klávesnicu a automatickej detekcie riadka, ktorý je pripojený
* Možnosť spustenia programu z USB kľúča, alebo iného prenosného zariadenia, bez nutnosti inštalácie
* Ozvučený inštalátor
* Preložený do 54 jazykov
* Podpora pre moderné operačné systémy Windows, 32 aj 64 bitové verzie
* Možnosť spúšťania na prihlasovacej obrazovke a [iných zabezpečených obrazovkách](#SecureScreens)
* Oznamovanie prvkov a textu pri práci s dotykovou obrazovkou
* Kompatibilita s rôznymi rozhraniami slúžiacimi na sprístupnenie aplikácií: Microsoft Active Accessibility, Java Access Bridge, IAccessible2 a UI Automation
* Podpora pre prostredie príkazového riadku Windows a konzolové aplikácie
* Podpora pre zvýraznenie zameraných objektov na obrazovke

### Systémové požiadavky {#SystemRequirements}

* NVDA spustíte v 32 aj 64 bitových verziách systémov Windows 8.1, 10, Windows 11 a tiež v serverových edíciách Windows od verzie 2012 R2.
  * Podporované sú AMD64 a ARM64 varianty operačného systému Windows.
* Mali by ste mať aspoň 150 MB voľného miesta úložného priestoru

### Medzinárodná podpora {#Internationalization}

Je dôležité, aby ľudia na celom svete hovoriaci akýmkoľvek jazykom, mali kdekoľvek prístup k špeciálnym technológiám.
NVDA bol dodnes okrem angličtiny lokalizovaný do týchto 54 jazykov: Afrikánčina, Albánčina, Arabčina, Aragónčina, Amharčina, Barmčina,  Bulharčina, Čeština, Dánčina, Fínčina, Francúzština, Galícijčina, Gréčtina, Gruzínčina, Hebrejčina,  Hindčina, Holandčina, Chorvátčina, Islandčina, Írčina, Japončina, Kannada, Katalánčina, Kyrgyz, Kórejčina, Litovčina, Macedónčina, Maďarčina, Mongolčina, Nemčina (Nemecko a Švajčiarsko), Nepálčina, Nórčina, Perzština, Poľština, Brazílska a Portugalská Portugalčina , Punjabi, Rumunčina, Ruština, Slovenčina, Slovinčina, Srbčina, Kolombijská a Španielska Španielčina, Švédčina, Taliančina, Tamilčina, Thajčina, Tradičná a zjednodušená čínština, Turečtina, Ukrajinčina, Vietnamčina .

### Podpora hlasového výstupu {#SpeechSynthesizerSupport}

Bez ohľadu na poskytovanie hlásení, a rozhraní v niekoľkých jazykoch, NVDA ponúka možnosť čítania textov v akomkoľvek jazyku, pokiaľ je dostupný hlasový výstup pre daný jazyk.

NVDA je distribuovaný s viacjazyčným voľne šíriteľným/Open-Source hlasovým výstupom [eSpeak NG](https://github.com/espeak-ng/espeak-ng).

Informácie o ďalších hlasových výstupoch, ktoré NVDA podporuje môžete nájsť v časti [Podporované hlasové výstupy](#SupportedSpeechSynths).

### Podpora brailových zobrazovačov {#BrailleSupport}

Pre používateľov, ktorí vlastnia brailový zobrazovač - ľudovo nazývaný tiež brailový riadok, NVDA umožňuje výstup v braillovom písme.
NVDA využíva na preklad do a z brailovho písma otvorené  tabuľky [LibLouis](https://liblouis.io/).
NVDA tiež podporuje zápis textu v Brailovom plnopise alebo skratkopise cez brailový riadok.
Navyše, NVDA dokáže automaticky rozpoznať mnohé pripojené brailové riadky.
Prosím pozrite si časť [Podporované brailové zobrazovače](#SupportedBrailleDisplays) pre informácie o podporovaných zariadeniach.

NVDA podporuje rôzne kódové tabuľky umožňujúce tak čítať brailový výstup vo viacerých jazykoch. V mnohých prípadoch existujú tabuľky pre plnopis aj skratkopis prípadne počítačový kód.

### Licencia a autorské práva {#LicenseAndCopyright}

NVDA je chránený autorskými právami Copyright NVDA_COPYRIGHT_YEARS Tím NVDA.

Distribúcia NVDA je možná pod licenciou GNU General Public License 2 s dvoma vínimkami.
Výnimky sú uvedené v častiach licencie "komponenty a ovládače, ktoré nepodliehajú licencii GPL" (Non-GPL Components in Plugins and Drivers) a "Kód poskytovaný spoločnosťou Microsoft" (Microsoft Distributable Code).
NVDA tiež používa kód, ktorý je dostupný pod licenciami s otvoreným kódom.
Tento produkt môžete voľne šíriť a meniť rôznym spôsobom, podmienkou však je pripojiť k nemu túto licenciu a sprístupniť zdrojový kód každému, kto si to vyžiada.
Týka sa to oboch pôvodných, aj upravených kópií daného software.

Pre viac informácií si môžete pozrieť [kompletnú licenciu (anglicky)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
Pre podrobné informácie o výnimkáchh, pozrite dokument v menu NVDA > Pomocník > Licencia (anglicky).

## Ako začať s programom NVDA {#NVDAQuickStartGuide}

Táto kapitola  pozostáva z troch základných častí: prevzatie programu, úvodné nastavenie a prvé spustenie NVDA.
Potom nasledujú informácie o prispôsobení nastavení, používaní doplnkov, dobrovoľnej účasti v komunite používateľov a získavaní pomoci.
Táto kapitola je zostavená z textov ostatných častí používateľskej príručky.
Podrobnejšie informácie získate prečítaním celej príručky.

### Získanie a inštalácia programu NVDA {#GettingAndSettingUpNVDA}

Používanie NVDA je úplne zdarma pre každého.
Nie je potrebné si strážiť licenčné kľúče alebo platiť za drahé predplatné.
Program NVDA je aktualizovaný priemerne štyri krát za rok.
Posledná verzia programu NVDA je vždy dostupná v časti "Download" [na stránke NV Access](NVDA_URL).

NVDA funguje so všetkými aktuálnymi verziami systému Microsoft Windows.
Ak vás zaujímajú podrobnosti, Skontrolujte si [Systémové požiadavky](#SystemRequirements).

#### Prevzatie programu NVDA {#StepsForDownloadingNVDA}

Tento zoznam krokov predpokladá, že máte základné znalosti navigácie  na webových stránkach.

* Otvorte si internetový prehliadač (Stlačte kláves `Windows`, do vyhľadávania napíšte slovo "internet" bez úvodzoviek a stlačte `enter`)
* Prejdite do časti download na stránke NV Access (Stlačte klávesy `alt+d`, do panela s adresou napíšte nasledujúcu adresu a stlačte `enter`): 
https://www.nvaccess.org/download 
* Nájdite a aktivujte tlačidlo Download
* Internetový prehliadač sa môže dožadovať akcie, ktorá sa vykoná po prevzatí a spustí preberanie súboru.
* V závislosti od prehliadača sa súbor môže automaticky spustiť hneď po prevzatí.
* Ak je súbor potrebné spustiť ručne, stláčaním `F6` prejdite do oblasti s oznámeniami a stiahnutý súbor spustite stlačením `alt+s` (prípadne iným spôsobom podľa použitého prehliadača).

### Inštalácia programu NVDA {#SettingUpNVDA}

Po spustení súboru sa spustí dočasná kópia NVDA.
V dialógu si môžete vybrať, či chcete NVDA nainštalovať, vytvoriť prenosnú verziu alebo chcete pokračovať v používaní dočasnej kópie.

Na inštaláciu a spustenie NVDA viac po stiahnutí nepotrebuje prístup na internet.
Ak je pripojenie na internet k dispozícii, NVDA dokáže pravidelne kontrolovať dostupnosť aktualizácií.

#### Spustenie stiahnutého súboru NVDA {#StepsForRunningTheDownloadLauncher}

Názov inštalačného súboru je "nvda_2022.1.exe" alebo podobný.
Rok a číslo verzie sa zmení s každou aktualizáciou podľa aktuálneho vydania.

1. Spustite stiahnutý súbor.
Počas samotného spúšťania dočasnej kópie programu NVDA sa prehrá krátka znelka.
Po úspešnom spustení už NVDA ozvučí celý proces inštalácie.
1. Zobrazí sa okno inštalácie programu NVDA s licenčnými podmienkami.
Ak si to želáte, licenciu si môžete čítať stláčaním klávesu `Šípka dolu`.
1. Stlačením klávesu `Tab` prejdite na začiarkavacie políčko "Súhlasím" a začiarknite ho stlačením `Medzerníka`.
1. Stláčajte `Tab` na prechádzanie po tlačidlách a požadovanú voľbu aktivujte stlačením `Enter`. 

K dispozícii sú nasledujúce možnosti:

* "Nainštalovať NVDA do počítača": Toto je najdôležitejšia možnosť pre všetkých používateľov, ktorí chcú NVDA plnohodnotne používať.
* "Vytvoriť prenosnú verziu": Týmto môžete rozbaliť NVDA do ľubovoľného priečinka bez inštalácie.
Je to užitočné na počítačoch bez oprávnení správcu alebo ak chcete NVDA mať na USB kľúči, ktorý si môžete nosiť so sebou.
Ak si zvolíte túto možnosť, NVDA vás prevedie krokmi vytvorenia prenosnej verzie.
Najdôležitejší parameter je priečinok, do ktorého sa rozbalí prenosná verzia.
* "Ponechať spustenú dočasnú kópiu": Dočasná kópia zostane spustená.
Môže to byť užitočné napríklad na odskúšanie vlastností v novej verzii pred jej nainštalovaním.
Dočasná kópia ostane spustená, až kým ju neukončíte klávesovou skratkou, položkou v ponuke NVDA alebo kým vypnete alebo reštartujete počítač.
Pozor: Zmeny v nastaveniach nebudú uložené.
* "Zrušiť": Ukončí NVDA a nevykoná sa žiadna akcia.

Ak chcete NVDA používať na tomto počítači, pravdepodobne ho budete chcieť nainštalovať.
Pristupovať k prihlasovacej obrazovke, obrazovkám systému UAC, [ iným zabezpečeným obrazovkám](#SecureScreens) a aplikáciám spusteným ako administrátor je možné len po nainštalovaní NVDA.
Tieto vlastnosti nefungujú v prenosnej verzii a dočasnej kópii NVDA.
Všetky podrobnosti o obmedzeniach si pozrite  v časti [Obmedzenia pre prenosnú verziu a dočasnú kópiu](#PortableAndTemporaryCopyRestrictions).

Počas inštalácie NVDA je možné vytvoriť odkazy v ponuke štart a na pracovnej ploche s klávesovou skratkou `ctrl+alt+n`.

#### Inštalácia z dočasnej kópie NVDA {#StepsForInstallingNVDAFromTheLauncher}

Tento zoznam krokov opisuje najčastejšie možnosti inštalácie.
Pre viac informácií o dostupných možnostiach si prosím prečítajte časť [Inštalácia NVDA](#InstallingNVDA).

1. Uistite sa, že začiarkavacie políčko Súhlasím s licenčnou dohodou je začiarknuté.
1. Stláčaním klávesu `Tab` nájdite a aktivujte tlačidlo "Nainštalovať NVDA do počítača".
1. Nasledujú možnosti súvisiace s používaním NVDA pri prihlasovaní do systému Windows a vytvorením odkazu na pracovnej ploche.
Tieto sú predvolene začiarknuté.
Ak si to želáte, na zmenu týchto možností použite klávesy `tab` a `medzerník` alebo ich môžete nechať na predvolených hodnotách.
1. Pokračujte stlačením `enter`.
1. Zobrazí sa dialógové okno kontroly používateľských účtov Windows s otázkou, či chcete tejto aplikácii povoliť vykonať zmeny v systéme.
1. Stlačte `alt+a` aby ste akceptovali výzvu.
1. Počas inštalácie sa zobrazí  indikátor priebehu.
Počas tohto procesu NVDA prehráva postupne sa zvyšujúci tón.
Môže to prebehnúť veľmi rýchlo a nemusíte si to vôbec všimnúť.
1. Na konci sa zobrazí dialógové okno potvrdzujúce úspešnosť inštalácie.
Správa napovedá "Stlačte OK, aby ste spustili nainštalovanú verziu.".
Stlačte `enter` a spustí sa nainštalovaná verzia NVDA.
1. NVDA prečíta uvítaciu správu a zobrazí sa dialógové okno "Vitajte v NVDA".
Zameraný je zoznamový rámik "Rozloženie klávesnice:".
Rozloženie "Desktop" v predvolenej konfigurácii používa klávesy na numerickom bloku.
Stlačením klávesu `šípka dolu` môžete vybrať rozloženie "laptop" a namiesto numerického bloku sa použijú iné klávesy.
1. Stlačte kláves `tab` a prejdite na "Používať `Capslock` ako kláves NVDA".
Kláves `Insert` je predvoleným klávesom NVDA.
Stlačte `medzerník` ak chcete používať `capslock` ako alternatívny kláves NVDA.
Všimnite si, že rozloženie klávesov je nastavené nezávisle na modifikačných klávesoch NVDA.
Aj kláves NVDA aj rozloženie klávesov môžete neskôr zmeniť v nastaveniach klávesnice.
1. Použite klávesy `tab` a `medzerník` na úpravu ostatných nastavení na tejto obrazovke.
Určujú, či sa NVDA bude spúšťať automaticky.
1. Stlačte kláves `enter` na zatvorenie dialógového okna a NVDA ostane spustené.

### Po spustení NVDA {#RunningNVDA}

Táto používateľská príručka NVDA obsahuje všetky príkazy NVDA rozdelené do rôznych sekcií.
Tabuľky s týmito príkazmi sú dostupné aj v dokumente "Zoznam Príkazov".
Modul "Basic Training for NVDA" (anglicky) obsahuje rozbor príkazov do hĺbky aj s príkladmi použitia.
Modul "Basic Training for NVDA" je možné kúpiť cez internet v obchode [NV Access Shop](https://www.nvaccess.org/shop).

Tu sú niektoré často používané príkazy.
Všetky príkazy sú konfigurovateľné a toto sú predvolené skratky priradené k týmto funkciám.

#### Modifikačný kláves NVDA {#NVDAModifierKey}

Predvolený modifikačný kláves NVDA je buď `numerická nula` (s vypnutým klávesom `numlock`) alebo kláves `insert`, neďaleko klávesov `delete`, `home` a `end`.
Ako kláves NVDA môžete nastaviť aj kláves `capsLock`.

#### Nápoveda vstupu {#InputHelp}

Aby ste si mohli precvičovať umiestnenie klávesov na klávesnici, zapnite nápovedu vstupu stlačením `NVDA+1`.
Kým je nápoveda vstupu zapnutá, vykonanie akejkoľvek vstupnej akcie (napríklad stlačenie klávesu alebo urobenie gesta na dotykovej obrazovke) oznámi funkciu a jej popis, ak existuje.
Priradené príkazy sa pri zapnutej nápovede vstupu nebudú spúšťať.

#### Spustenie a ukončenie NVDA {#StartingAndStoppingNVDA}

| Názov |Klávesová skratka pre desktop |klávesová skratka pre Laptop |Popis|
|---|---|---|---|
|Spustiť alebo reštartovať NVDA |`ctrl+alt+n` |`ctrl+alt+n` |Spustí alebo reštartuje NVDA.|
|Ukončiť NVDA |`NVDA+q` potom `enter` |`NVDA+q` potom `enter` |Ukončí NVDA|
|Pozastaviť reč |`Shift` |`shift` |Okamžite pozastaví reč. Po nasledujúcom stlačení bude reč pokračovať na prerušenom mieste|
|Zastaviť reč |`ctrl` |`ctrl` |Okamžite zastaví reč|

#### Čítanie textu {#ReadingText}

| Názov |Klávesová skratka pre Desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|Plynulé čítanie |`NVDA+šípka dolu` |`NVDA+A` |Prečíta text od pozície systémového kurzora do konca textu, pričom sa systémový kurzor posúva|
|Aktuálny riadok |`NVDA+šípka hore` |`NVDA+l` |Prečíta   aktuálny riadok zameraný systémovým kurzorom. Stlačené dvakrát rýchlo za sebou vyhláskuje riadok a stlačené trikrát za sebou vyhláskuje riadok foneticky.|
|Aktuálny výber |`NVDA+Shift+šípka hore` |`NVDA+shift+s` |Oznámi práve vybratý text. Stlačené dvakrát vyhláskuje text, stlačené trikrát, vyhláskuje text foneticky|
|Oznámiť text v schránke Windows |`NVDA+c` |`NVDA+c` |Ak je v schránke Windows text, NVDA ho oznámi. Stlačené dvakrát vyhláskuje text, stlačené trikrát, vyhláskuje text foneticky|

#### Oznamovanie umiestnenia a ostatné informácie {#ReportingLocation}

| Názov |Klávesová skratka pre Desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|názov okna |`NVDA+t` |`NVDA+t` |Oznámi titulok aktuálneho aplikačného okna alebo okna v popredí. Stlačené 2 krát rýchlo za sebou vyhláskuje názov okna a stlačené 3 krát rýchlo za sebou skopíruje názov aktuálneho okna do schránky.|
|Fokus |`NVDA+tab` |`NVDA+tab` |Oznámi meno objektu, ktorý má systémový fokus. Stlačené dvakrát informáciu vyhláskuje, stlačené trikrát informáciu vyhláskuje foneticky.|
|obsah okna v popredí |`NVDA+b` |`NVDA+b` |Oznámi všetky prvky aktuálneho okna v popredí (užitočné pre dialógy)|
|Stavový riadok |`NVDA+end` |`NVDA+shift+end` |Oznámi obsah stavového riadku ak ho NVDA dokáže nájsť. Stlačené dvakrát stavový riadok vyhláskuje. Stlačené trikrát skopíruje obsah stavového riadka do schránky|
|Čas a dátum |`NVDA+f12` |`NVDA+f12` |Oznámi čas; stlačené 2 krát rýchlo za sebou oznámi dátum. Dátum a čas je oznamovan podľa formátu nastaveného v systéme Windows.|
|Oznámiť formátovanie textu |`NVDA+f` |`NVDA+f` |Oznámi formátovanie pod textovým kurzorom. Stlačené dvakrát za sebou zobrazí informáciu v režime prehliadania|
|Oznámiť URL adresu odkazu |`NVDA+k` |`NVDA+k` |Oznámi URL adresu odkazu, na ktorom je fokus alebo systémový kurzor.  Stlačené dvakrát za sebou zobrazí URL adresu v samostatnom okne, aby bolo možné ju podrobnejšie prezerať|

#### Prepínanie čítania informácií {#ToggleWhichInformationNVDAReads}

| Názov |Klávesová skratka pre Desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|Čítať napísané znaky |`NVDA+2` |`NVDA+2` |Ak je zapnuté, NVDA bude oznamovať všetky napísané znaky.|
|Čítať po slovách |`NVDA+3` |`NVDA+3` |Ak je zapnuté, NVDA bude čítať pri písaní text po slovách.|
|Čítať príkazové skratky |`NVDA+4` |`NVDA+4` |Ak je zapnuté, NVDA bude čítať klávesové skratky použité ako príkazy, teda nie samotné znaky. Do tejto funkcie spadajú kombinácie znakov a klávesov napr. s klávesom ctrl.|
|Povoliť sledovanie kurzora myši |`NVDA+m` |`NVDA+m` |Ak je možnosť povolená, NVDA bude oznamovať text cez ktorý prechádza kurzor myši. Takto môžete nájsť položky na obrazovke pomocou  myši a nemusíte použiť objektovú navigáciu.|

#### Kruh nastavení hlasového výstupu {#TheSynthSettingsRing}

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|ďalšie nastavenie hlasového výstupu |`NVDA+ctrl+pravá šípka` |`NVDA+ctrl+shift+pravá šípka` |Prejde na nasledujúce dostupné nastavenie hlasového výstupu. Z posledného nastavenia NVDA automaticky prejde na prvé.|
|Predchádzajúce nastavenie hlasového výstupu |`NVDA+ctrl+ľavá šípka` |`NVDA+ctrl+shift+ľavá šípka` |Prejde na predchádzajúce dostupné nastavenie hlasového výstupu. Z prvého NVDA automaticky prejde na posledné nastavenie.|
|Zvýšiť hodnotu nastavenia hlasového výstupu |`NVDA+ctrl+šípka hore` |`NVDA+ctrl+shift+šípka hore` |Zvýši hodnotu aktuálne zameraného nastavenia hlasového výstupu. Napríklad zrýchli tempo, vyberie nasledujúci hlas, zosilní hlasitosť|
| Zvýšiť hodnotu nastavenia hlasu po väčších krokoch | `NVDA+ctrl+pageUp` | `NVDA+shift+ctrl+pageUp` | Zvyšuje hodnotu nastavenia hlasového výstupu po väčších krokoch. Posuvníky sú posúvané po 20 percentách, výška hlasu napríklad po dvadsiatich krokoch|
|Znížiť hodnotu nastavenia hlasu |`NVDA+ctrl+šípka dolu` |`NVDA+ctrl+shift+šípka dolu` |Zníži hodnotu aktuálne zameraného nastavenia hlasového výstupu. Napríklad spomalí tempo, vyberie predchádzajúci hlas, stíši hlasitosť.|
| Znížiť  hodnotu nastavenia hlasu po väčších krokoch | `NVDA+ctrl+pageWown` | `NVDA+shift+ctrl+pageDown` | znižuje  hodnotu nastavenia hlasového výstupu po väčších krokoch. Posuvníky sú posúvané po 20 percentách, výška hlasu napríklad po dvadsiatich krokoch|

Môžete tiež nastaviť klávesové skratky, ktoré budú nastavovať prvú a poslednú hodnotu aktuálneho nastavenia v kruhu nastavení. Nastavenie vykonáte v dialógu [Klávesové skratky](#InputGestures), v kategórii reč.
Ak napríklad budete na nastavení rýchlosti, budete môcť okamžite nastaviť hodnoty 0 alebo 100.
Na nastavení hlas budete môcť vybrať prvý alebo posledný hlas.

#### Navigácia na webových stránkach {#WebNavigation}

Kompletný zoznam jednoznakových navigačných príkazov na webe nájdete v časti [Režim prehliadania](#BrowseMode).

| Príkaz |Skratka |Popis|
|---|---|---|
|Nadpis |`h` |prejde na nasledujúci nadpis|
|Nadpis úrovne 1, 2, alebo 3 |`1`, `2`, `3` |Prejde na nasledujúci nadpis príslušnej úrovne|
|Prvok formulára |`f` |Prejde na nasledujúci prvok formulára (editačné pole, tlačidlo a pod)|
|Odkaz |`k` |Prejde na nasledujúci odkaz|
|Oblasť stránky |`d` |Prejde do nasledujúcej oblasti stránky|
|Zoznam |`l` |Prejde do nasledujúceho zoznamu|
|Tabuľka |`t` |Prejde do nasledujúcej tabuľky|
|Pohyb v opačnom smere |`shift+písmeno` |Stlačte `shift` spolu s niektorým z predchádzajúcich písmen a prejdete na predchádzajúci prvok takého typu.|
|Zoznam prvkov |`NVDA+f7` |Zobrazí zoznamy rôznych prvkov napr. odkazov alebo nadpisov|

### Nastavenia {#Preferences}

Väčšinu vlastností NVDA je možné konfigurovať v dialogu nastavenia.
Nastavenia a ostatné možnosti nájdete v ponuke NVDA
Túto ponuku otvoríte stlačením `nvda+n`.
Dialóg nastavenia priamo v časti všeobecné môžete otvoriť stlačením `NVDA+ctrl+g`.
Viaceré obrazovky s nastaveniami majú priradené klávesové skratky ako napríklad `NVDA+ctrl+s` hlasový výstup alebo `NVDA+ctrl+v` nastavenia hlasu.

### Doplnky {#Addons}
Doplnky umožňujú doplniť do NVDA nové funkcie, alebo pozmeniť existujúce funkcie NVDA.
Vyvýja ich komunita okolo NVDA, ale aj externé prípadne aj komerčné organizácie. NV Access nezodpovedá za obsah a funkčnosť doplnkov.
Pred inštaláciou doplnku si overte dôverihodnosť jeho dodávateľa a vývojára.
O možnostiach overenia píšeme podrobnejšie v časti o [Katalógu s doplnkami ](#AddonStoreInstalling).

Pri prvom spustení katalógu s doplnkami sa objaví varovanie.
Doplnky nie sú preverované NV Access a môžu mať neobmedzený prístup k funkciám a vašim údajom.
Stlačte `medzeru` ak ste sa oboznámili s varovaním a nechcete ho viac zobrazovať.
Stlačte `tab` aby ste prešli na tlačidlo "OK" a stlačte kláves `enter` na zatvorenie varovania a prechod do katalógu s doplnkami.
Všetky detaily o "[doplnkoch a katalógu](#AddonsManager)" sú popísané v samostatných kapitolách.

Katalóg s doplnkami je dostupný z menu nástroje.
Otvorte Ponuku NVDA skratkou `NVDA+n`, písmenom `n` otvorte položku nástroje a následne písmenom `a` otvorte dialóg katalógu s doplnkami.
Ak spustíte katalóg s doplnkami a ešte nemáte nainštalované žiadne doplnky, otvorí sa záložka "dostupné doplnky".
Ak už máte nainštalované doplnky, otvorí sa katalóg na záložke "nainštalované doplnky".

#### Dostupné doplnky {#AvailableAddons}
Pri prvom otvorení tohto okna môže načítanie doplnkov chvíľu trvať.
NVDA po načítaní prečíta názov prvého dostupného doplnku.
Doplnky sú zoradené v abecednom poradí v tabuľke.
Ak chcete vyhľadať konkrétny doplnok, postupujte nasledovne:

1. Na pohyb po položkách použite šípky hore a dole, prípadne prvé písmená názvu doplnku.
1. Popis vybratého doplnku si môžete prečítať po stlačení klávesu `tab`.
1. Na čítanie textu použite [príkazy na čítanie textu](#ReadingText) alebo šípky.
1. Klávesom `tab` prejdite na tlačidlo "Akcie". Po aktivovaní tohto tlačidla sa dostanete k inštalácii doplnku a ostatným možnostiam.
1. Opätovným stlačením klávesu `tab` sa dostanete na pole "ďalšie podrobnosti", kde sú uvedené informácie ako autor, webová stránka a podobne.
1. Na návrat k zoznamu doplnkov použite `alt+d`, alebo opakovane stláčajte `shift+tab` kým sa opäť nedostanete k zoznamu.

#### Vyhľadávanie doplnkov {#SearchingForAddons}
Okrem prezerania celého zoznamu doplnkov, je možné vyfiltrovať doplnky podľa kritérií.
Na prechod do poľa hľadania stlačte `alt+h` a napíšte, čo hľadáte.
Vyhľadávanie prehľadáva Identifikátor, názov, autora, vydavateľa a popis.
Zoznam sa automaticky aktualizuje pri písaní reťazca hľadania.
Po zadaní hľadaného reťazca, prejdite klávesom `tab` do zoznamu s výsledkami.

#### Inštalácia doplnkov {#InstallingAddons}

Doplnok nainštalujete nasledovne:

1. Po zameraní doplnku, ktorý chcete nainštalovať, stlačte kláves `enter`.
1. Otvorí sa zoznam dostupných akcií, prvá je "Inštalovať doplnok".
1. Ak chcete doplnok nainštalovať, stlačte písmeno `i` alebo `šípkou dole` nájdite možnosť "nainštalovať" a potvrďte klávesom `enter`.
1. Fokus sa opäť vráti k zoznamu doplnkov a NVDA prečíta práve vybratý doplnok.
1. Všimnite si, že stav doplnku sa zmení z "dostupný" na "prebieha sťahovanie".
1. Po stiahnutí doplnku sa stav zmení na "stiahnuté, bude povolený po reštarte".
1. V tomto bode môžete nainštalovať rovnakým postupom aj ďalšie doplnky.
1. Po stiahnutí všetkých požadovaných doplnkov, klávesom `tab` prejdite na tlačidlo "zavrieť" a stlačte `enter`.
1. Po zatvorení katalógu budú nainštalované zvolené doplnky.
Niektoré doplnky môžu počas inštalácie zobraziť dialógy,  v ktorých bude potrebné reagovať.
1. Po nainštalovaní doplnkov sa objaví výzva na reštartovanie NVDA.
1. Klávesom `enter` potvrďťe reštart.

#### Spravovanie nainštalovaných doplnkov {#ManagingInstalledAddons}
Na pohyb po záložkách katalógu s doplnkami použite skratku `ctrl+tab`.
Dostupné sú záložky: "nainštalované doplnky", "dostupné aktualizácie doplnkov", "dostupné doplnky" a "nainštalované nekompatibilné doplnky".
Záložky majú rovnaký vzhľad. Obsahujú zoznam doplnkov, detaily k vybratému doplnku a tlačidlo pre spravovanie doplnkov.
Pri nainštalovaných doplnkoch sú dostupné možnosti "zakázať" a "odinštalovať", namiesto "nainštalovať".
Zakázanie doplnku spôsobí, že NVDA doplnok nenačíta, ale doplnok nebude odstránený.
Ak chcete povoliť zakázaný doplnok, zvoľte z menu akcií možnosť "povoliť".
Po zakázaní, povolení alebo odinštalovaní doplnku budete po zatvorení katalógu s doplnkami vyzvaní na reštartovanie NVDA.
Zmeny sa prejavia až po reštarte.
Na zatvorenie katalógu s doplnkami je možné použiť kláves `escape`.

#### Aktualizovanie doplnkov {#UpdatingAddons}
Ak sú dostupné aktualizácie doplnkov, zobrazia sa na záložke "dostupné aktualizácie doplnkov".
Na túto záložku sa môžete dostať rýchlo klávesovou skratkou `ctrl+tab`.
Stav pri doplnku bude "dostupné aktualizácie".
V zozname sa zobrazí aktuálna a tiež dostupná verzia.
Na zvolenom doplnku stlačte `enter` čím otvoríte zoznam dostupných možností. Následne zvoľte "aktualizovať".

### Komunita {#Community}

Okolo programu NVDA existuje rozsiahla komunita používateľov.
Hlavným komunikačným kanálom je [emailová konferencia v anglickom jazyku](https://nvda.groups.io/g/nvda) a  stránka s odkazmi na [skupiny lokalizované do rôznych jazykov](https://github.com/nvaccess/nvda/wiki/Connect).
Tvorcovia NVDA, NV Access sú aktívni aj na [Twitteri](https://twitter.com/nvaccess) a [Facebooku](https://www.facebook.com/NVAccess). V oboch prípadoch v Angličtine.
NV Access tiež píšu pravidelný blog (anglicky) nazvaný [In-Process blog](https://www.nvaccess.org/category/in-process/).

Existuje tiež program [NVDA Certified Expert](https://certification.nvaccess.org/) (anglicky).
Je to online test, ktorý môžete podstúpiť, aby ste demonštrovali vaše znalosti s používaním programu NVDA.
[Certifikovaní experti NVDA](https://certification.nvaccess.org/) môžu zverejniť svoje kontaktné údaje a podrobnosti o nimi ponúkaných službách.

### Ako získať pomoc {#GettingHelp}

Pomocníka si môžete otvoriť tak, že stlačíte `NVDA+n` na otvorenie ponuky NVDA, potom `p` pre pomocník.
V tejto podponuke nájdete Používateľskú príručku, zoznam príkazov, históriu nových vlastností NVDA a ďalšie.
Dokumenty sa otvoria v predvolenom prehliadači webových stránok.
[V obchode NV Access](https://www.nvaccess.org/shop) je tiež k dispozícii veľmi podrobný materiál v anglickom jazyku.

Odporúčame začať s modulom "Basic Training for NVDA module".
Tento pokrýva koncepty pre začiatočníkov až po navigáciu na webe a používanie objektovej navigácie.
Je dostupný:

* [Ako elektronický text](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), čo obsahuje dokumenty vo formáte Word DOCX, Web stránky HTML, elektronickú knihu ePub a Kindle KFX.
* [Zvuk vo formáte MP3, čítaný ľudskou rečou](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Tlačenú knihu v Braillovom písme UEB](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) s doručením po celom svete.

Ďalšie moduli a [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/) so zľavou, sú tiež dostupné v obchode [NV Access Shop](https://www.nvaccess.org/shop/).

NV Access tiež predáva [telefonickú podporu](https://www.nvaccess.org/product/nvda-telephone-support/) v anglickom jazyku, buď individuálne, alebo ako súčasť [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Pre telefonickú podporu sú zriadené lokálne telefónne čísla v Austrálii a v spojených štátoch.

[Používateľské emailové konferencie](https://github.com/nvaccess/nvda/wiki/Connect) a [certifikovaní experti NVDA](https://certification.nvaccess.org/) sú dobrým zdrojom používateľskej pomoci.

Chyby a nové funkcie môžete hlásiť anglicky cez [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
Pokiaľ chcete akýmkoľvek spôsobom prispieť k vývoju NVDA, odporúčame vám pozrieť si [Inštrukcie](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md), kde nájdete dôležité informácie o komunite.

## Ďalšie možnosti inštalácie {#MoreSetupOptions}
### Možnosti inštalácie {#InstallingNVDA}

Ak inštalujete NVDA zo stiahnutého súboru z internetu, stlačte tlačidlo Nainštalovať do počítača.
Ak ste úvodnú obrazovku zatvorili alebo chcete NVDA inštalovať z prenosnej verzie, aktivujte položku Nainštalovať NVDA z podmenu nástroje v ponuke NVDA.

Po spustení inštalácie sa vás program opýta, či skutočne chcete NVDA inštalovať a takisto vás upozorní v prípade, že sa rozhodnete aktualizovať už nainštalovanú verziu NVDA.
Inštaláciu spustíte aktivovaním tlačidla Pokračovať.
Počas inštalácie máte niekoľko možností, ktoré sú opísané v nasledujúcej podkapitole.
Po úspešnom nainštalovaní sa zobrazí okno so správou, ktoré môžete zatvoriť stlačením tlačidla OK.
Po zatvorení okna sa NVDA reštartuje.

#### Upozornenie na nekompatibilné doplnky {#InstallWithIncompatibleAddons}

Ak používate nejaké doplnky, NVDA vás môže upozorniť, že vaše doplnky nie sú kompatibilné s verziou NVDA, ktorú sa pokúšate nainštalovať.
Pred tým, než budete pokračovať, musíte odsúhlasiť zakázanie doplnkov.
Po aktivovaní tlačidla zobraziť nekompatibilné doplnky si môžete pozrieť, ktoré doplnky budú zakázané.
Podrobnosti si môžete prečítať v časti [Nekompatibilné doplnky](#incompatibleAddonsManager).
Po inštalácii môžete na vlastné riziko povoliť nekompatibilné doplnky z [Katalógu doplnkov](#AddonsManager).

#### Spúšťať NVDA na prihlasovacej obrazovke {#StartAtWindowsLogon}

Umožňuje nastaviť, či sa má NVDA automaticky spustiť pri zobrazení prihlasovacej obrazovky, teda ešte pred tým, ako zadáte svoje heslo.
toto zahŕňa aj obrazovky UAC (zabezpečenie systému) a [iné zabezpečené obrazovky](#SecureScreens).
Táto možnosť je predvolene začiarknutá.

#### Vytvoriť odkaz na pracovnej ploche so skratkou ctrl+alt+n {#CreateDesktopShortcut}

Môžete sa rozhodnúť, či chcete, aby sa pri inštalácii NVDA vytvoril odkaz na pracovnej ploche.
Ak sa rozhodnete vytvoriť odkaz, inštalátor automaticky tomuto odkazu priradí skratku `ctrl+alt+n`. Touto skratkou budete môcť NVDA kedykoľvek spustiť.

#### Skopírovať nastavenia s prenosnej verzie do profilu aktuálne prihláseného používateľa {#CopyPortableConfigurationToCurrentUserAccount}

Ak začiarknete túto voľbu, pri inštalácii sa skopírujú aktuálne nastavenia NVDA do profilu aktuálne prihláseného používateľa.
Nastavenia nebudú skopírované do iných používateľských účtov v systéme a nebudú sa používať ani na  prihlasovacej obrazovke a [iných zabezpečených obrazovkách](#SecureScreens).
Táto voľba je dostupná len ak inštalujete NVDA z prenosnej verzie. Voľba sa nezobrazí, ak inštalujete NVDA priamo zo súboru z webovej stránky NVDA.

### Vytvorenie prenosnej verzie {#CreatingAPortableCopy}

Ak vytvárate prenosnú verziu priamo so súboru so stránky NVDA, aktivujte tlačidlo Vytvoriť prenosnú verziu.
Ak ste zatvorili úvodnú obrazovku, alebo máte spustenú inštalačnú verziu NVDA, v ponuke NVDA v podmenu nástroje aktivujte položku Vytvoriť prenosnú verziu.

V nasledujúcom dialógu môžete vybrať priečinok, v ktorom sa uloží prenosná verzia NVDA.
Môže to byť priečinok na vašom pevnom disku, USB kľúči, pamäťovej karte alebo inom prenosnom médiu.
K dispozícii je tiež voľba, ktorá umožňuje zahrnúť do prenosnej verzie nastavenia práve prihláseného používateľa.
Táto možnosť je dostupná len ak vytvárate prenosnú verziu z nainštalovanej verzie NVDA a nezobrazí sa, ak vytvárate prenosnú verziu priamo zo stiahnutého súboru zo stránky NVDA.
Vytvorenie prenosnej verzie potvrdíte stlačením tlačidla Pokračovať.
Po úspešnom skopírovaní súborov sa zobrazí správa, ktorá vás informuje o úspešnosti operácie.
Dialóg zatvorte aktivovaním tlačidla OK.

### Obmedzenia pre prenosnú verziu a dočasnú kópiu {#PortableAndTemporaryCopyRestrictions}

Ak chcete NVDA používať z USB kľúča alebo z iného zapisovateľného média (pamäťová karta a podobne), v úvodnom dialógu vyberte možnosť vytvoriť prenosnú verziu.
Z nainštalovanej verzie si kedykoľvek môžete vytvoriť prenosnú verziu.
Prenosnú verziu môžete kedykoľvek neskôr nainštalovať do počítača, takže budete môcť využívať výhody nainštalovanej verzie.
Ak chcete NVDA nahrať na CD alebo iný druh média len na čítanie, skopírujte priamo súbor stiahnutý zo stránky NVDA.
Spúšťanie skutočnej prenosnej verzie z média len na čítanie nie je zatiaľ podporované.

[Inštalátor NVDA](#StepsForRunningTheDownloadLauncher) je možné použiť tiež ako dočasnú kópiu NVDA.
Dočasná kópia NVDA nedokáže ukladať nastavenia.
Rovnako nie je možné [spravovať doplnky](#AddonsManager).

Prenosná a dočasná kópia NVDA má tieto obmedzenia:

* Nemožnosť automatického spustenia po štarte systému.
* Nemožnosť pracovať s aplikáciami, ktoré bežia správami administrátora, ak spustená verzia NVDA tiež nemá práva administrátora (čo sa však neodporúča).
* Nemožnosť čítať obrazovku na prepnutie užívateľského účtu (UAC) pri pokuse spustiť aplikáciu s právami administrátora.
* Nefunguje používanie dotykovej obrazovky.
* Nie je možné využívať režim prehliadania a čítanie napísaných znakov vo Windows Store.
* Nie je možné využívať automatické stíšenie.

## Používanie NVDA {#GettingStartedWithNVDA}
### Spustenie NVDA {#LaunchingNVDA}

Ak už máte nainštalovaný NVDA podľa pokynov inštalátora, spustiť NVDA je veľmi jednoduché. Stačí stlačiť klávesovú skratku Ctrl+Alt+N, alebo vybrať položku NVDA zo skupiny NVDA z menu štart/programy.
Tiež môžete NVDA spustiť napísaním "NVDA" do okna Spustiť v ponuke štart.
Ak  NVDA v tomto čase beží, automaticky sa reštartuje.
Pomocou [parametrov príkazového riadka](#CommandLineOptions) môžete Ukončiť NVDA (-q), zakázať doplnky (--disable-addons) a podobne.

Nainštalovaná verzia NVDA si ukladá súbory s konfiguráciou do priečinka Roaming určeného pre konkrétneho používateľa (teda "`C:\Users\<user>\AppData\Roaming`").
Môžete NVDA nastaviť tak, aby si Načítalo konfiguráciu z lokálneho adresára.
Podrobnosti nájdete v časti [Systémové parametre](#SystemWideParameters) for more details.

Na spustenie prenosnej verzie vstúpte do priečinka, kam ste si NVDA rozbalili a stlačte enter, alebo kliknite na súbor NVDA.exe.
Ak NVDA v tomto čase beží, automaticky sa reštartuje.

Hneď ako sa NVDA spustí, prvé čo budete počuť je rad stúpajúcich tónov, ktoré vám hovoria, že sa NVDA práve spúšťa.
V závislosti od toho, aký rýchly je váš počítač, alebo médium z ktorého NVDA spúšťate, môže spustenie chvíľu trvať.
Ak spúšťanie trvá príliš dlho, NVDA oznámi, "Spúšťanie programu NVDA, prosím čakajte".

Ak sa neobjaví nič z uvedeného, alebo sa objaví chyba ohlásená zvukom Windows, prípadne rad klesajúcich tónov, znamená to, že NVDA má problém pri spúšťaní a túto chybu by ste mali ohlásiť tvorcom programu.
Informácie o tom, ako chybu ohlásiť nájdete na stránkach NVDA.

#### Dialóg Vitajte v NVDA {#WelcomeDialog}

Keď sa NVDA spustí prvý krát, objaví sa uvítacie okno informujúce o použití tzv. klávesu NVDA a základné informácie o ponuke NVDA.
Viac podrobností si môžete prečítať v nasledujúcich odsekoch.
Ďalej toto okno obsahuje jeden zoznamový rámik a tri začiarkavacie políčka.
V zozname môžete určiť rozloženie klávesnice, ktoré chcete používať.
Prvé začiarkávacie políčko umožní zvoliť, či chcete používať capslock ako modifikačný kláves NVDA.
Druhé začiarkávacie pole rozhoduje o tom, či sa má NVDA spúšťať po prihlásení do systému Windows a je prístupné len v nainštalovanej verzii NVDA.
Tretie začiarkavacie políčko umožňuje nastaviť, či sa uvítacie okno má zobraziť po každom štarte NVDA.

#### Získavanie údajov od používateľov NVDA {#UsageStatsDialog}

Od verzie NVDA 2018.3 sa pýtame používateľov, či nám chcú posielať dáta, ktoré môžeme využiť na zlepšenie funkcií NVDA.
Pri prvom spustení NVDA sa zobrazí otázka, či chcete povoliť zasielanie anonymných údajov do NV Access.
Podrobnosti sú vysvetlené v kapitole [Povoliť zasielanie štatistických údajov do NV Access](#GeneralSettingsGatherUsageStats).
Upozorňujeme, že odpoveď áno alebo nie automaticky zatvorí tento dialóg a táto otázka sa nezobrazí až dokým nepreinštalujete NVDA.
Kedykoľvek môžete zasielanie štatistík zapnúť alebo vypnúť. Hľadajte začiarkávacie pole označené [Povoliť zasielanie údajov](#GeneralSettingsGatherUsageStats) v časti všeobecné nastavenia.

### Klávesové skratky {#AboutNVDAKeyboardCommands}
#### Klávesový modifikátor NVDA {#TheNVDAModifierKey}

Väčšina klávesových príkazov NVDA je kombináciou zvláštneho klávesu nazývaného kláves NVDA s inými klávesmi.
Výnimkou sú príkazy na navigáciu  v desktop rozložení pomocou prezeracieho kurzora, keďže tu sa používajú číslice na vypnutom  numerickom bloku bez klávesu NVDA. Existujú však aj ďalšie výnimky.

Ako kláves NVDA je možné nastaviť klávesy insert, numerický insert a capslock pričom všetky je možné použiť súčasne.
Predvolené nastavenia majú ako kláves NVDA nastavený insert aj numerický insert.

Ak si želáte vykonať pôvodnú funkcionalitu klávesu, ktorý Ste nastavili ako kláves NVDA (napr. prepnúť stav veľkých písmen pomocou klávesu capslock) stlačte kláves NVDA 2 krát rýchlo za sebou.

#### Rozloženia klávesnice {#KeyboardLayouts}

NVDA má dve sady  klávesových príkazov, teda tzv. rozloženia: rozloženie pre stolné počítače a pre prenosné (laptop) počítače.
Predvolene je NVDA nastavený na rozloženie desktop. Je možné to zmeniť v [Nastaveniach](#NVDASettings) v ponuke NVDA v kategórii klávesnica.

Rozloženie pre stolné počítače sa spolieha na klávesy z numerického bloku, keď je tlačidlo numlock vypnuté.
Aj keď väčšina prenosných počítačov nemá fyzický numerický blok, na mnohých notebookoch je možné emulovať klávesy numerického bloku pridržaním klávesu fn a stláčaním písmen a číslic v pravej časti klávesnice (7, 8, 9, u, i, o, j, k, l, atď).
Ak toto Váš notebook nepodporuje, alebo nie je možné vypnúť tlačidlo numlock, môžete použiť rozloženie nazvané laptop.

### Dotykové gestá NVDA {#NVDATouchGestures}

Ak používate NVDA na zariadení vybavenom dotykovou obrazovkou, môžete NVDA ovládať tiež priamo cez dotykové gestá.
Počas behu NVDA bude každý vstup z dotykovej obrazovky presmerovaný do programu NVDA. Túto funkciu je možné vypnúť.
Z tohto dôvodu nie je v takejto situácii možné štandardným spôsobom vykonávať pomocou dotykovej obrazovky akcie, ktoré je možné vykonávať bez spusteného programu NVDA.
<!-- KC:beginInclude -->
Podporu pre dotykové gestá zapnete a vypnete skratkou NVDA+ctrl+alt+t.
<!-- KC:endInclude -->
Nastavenie môžete tiež meniť v nastaveniach NVDA, kategória Dotyková obrazovka, položka [povoliť dotykové gestá](#TouchSupportEnable).

#### Skúmanie obrazovky {#ExploringTheScreen}

Základná akcia, ktorú môžete spustiť dotykom na obrazovku je oznámenie objektu zobrazeného v akomkoľvek bode obrazovky.
Položením jedného prsta kdekoľvek na obrazovku spustíte túto akciu.
Môžete tiež nechať prst pritlačený k obrazovke a postupným posúvaním po ploche obrazovky si nechať vyčítať prvky, cez ktoré Váš prst prechádza spolu s ich textom 

#### Dotykové gestá {#TouchGestures}

V ďalšom texte tejto príručky sa vyskytnú zoznamy príkazov NVDA, ktoré okrem štandardných klávesových skratiek budú obsahovať tzv. dotykové gestá, vykonávané pomocou dotykovej obrazovky.
Nasledujú jednoduché inštrukcie, ktoré majú za cieľ vysvetliť ako vykonávať dotykové gestá pomocou dotykovej obrazovky tak, aby Ste na základe ich použitia dokázali vyvolať príkazy NVDA k týmto gestám priradené.

##### Klepnutia {#Taps}

Rýchlo poklepte po obrazovke jedným alebo viacerými prstami.

Poklepanie raz jedným prstom je jednoducho nazývané klepnutie.
Poklepanie dvoma prstami súčasne je klepnutie dvoma prstami.

Ak vykonáte rovnaký spôsob klepnutia viac ako jeden krát rýchlo za sebou, NVDA takúto akciu rozpozná ako tzv. viacnásobné klepnutie.
Klepnutie dva krát rýchlo za sebou sa prejaví ako tzv. dvojité klepnutie.
Klepnutie tri krát rýchlo za sebou znamená trojité klepnutie a tak ďalej.
Samozrejme tieto viac násobné klepnutia je možné vykonávať viacerými prstami, výsledkom čoho sú gestá ako dvojité klepnutie troma prstami, štvorité klepnutie a podobne.

##### Švihanie {#Flicks}

Rýchlym pohybom posuňte prst po obrazovke.

Sú štyri možnosti švihnutia na základe smeru pohybu: švihnutie vľavo, vpravo, hore alebo dolu.

Rovnako ako pri vykonávaní klepnutí je možné švihať viacerými prstami.
Znamená to, že sú k dispozícii rôzne gestá ako napríklad švihnutie hore dvoma prstami, švihnutie vľavo štyrmi prstami a podobne.

#### Režim dotyku {#TouchModes}

K dispozícii je nepochybne väčšie množstvo príkazov NVDA než dostupných gest, ktoré je možné vykonať pomocou dotykovej obrazovky. Znamená to, že NVDA používa niekoľko tzv. režimov dotyku, medzi ktorými je možné prepínať a podľa aktívneho režimu dotyku sú aj dostupné konkrétne podmnožiny príkazov NVDA.
Zatiaľ sú k dispozícii textový režim a objektový režim.
Niektoré príkazy ďalej v tomto dokumente môžu mať preto za názvom gesta uvedený v zátvorke jeden z týchto režimov.
Napríklad švihnutie hore (textový režim) znamená, že príkaz sa vykoná po švihnutí smerom na hor ale len ak je aktívny textový režim dotyku.
Ak príkaz za názvom gesta nemá uvedený názov režimu dotyku, bude tento príkaz fungovať vo všetkých dostupných režimoch.

<!-- KC:beginInclude -->
Prepínať režimy dotyku je možné klepnutím troma prstami.
<!-- KC:endInclude -->

#### Dotyková klávesnica {#TouchKeyboard}

Dotyková klávesnica sa používa na zadávanie textu a príkazov cez dotykovú obrazovku.
ak ste v editačnom poli, dotykovú klávesnicu si zobrazíte dvojitým poklepaním na ikonu klávesnice.
Pri používaní tabletov, ako napríklad Microsoft Surface Pro, sa klávesnica zobrazí vždy, keď je odpojená fyzická klávesnica.
Dotykovú klávesnicu skryjete opätovným dvojitým poklepaním na ikonu klávesnice, alebo opustením editačného poľa.

ak už máte zobrazenú dotykovú klávesnicu, klávesy nájdete pohybom prsta (zvyčajne sa nachádzajú na spodku obrazovky). Medzi klávesmi sa presúvajte pohybom jedného prsta.
Keď nájdete požadovaný kláves, uvoľnite prst, alebo na mieste dvakrát poklepte. (Toto závisí od nastavenia v kategórii  [Dotyková obrazovka](#TouchInteraction) v nastaveniach NVDA).

### Režim nápovedy vstupu {#InputHelpMode}

Táto príručka obsahuje mnoho príkazov NVDA, no veľmi jednoduchý spôsob, ako ich preskúmať je použitie režimu nápovedy vstupu.

Nápovedu vstupu spustíte stlačením kombinácie NVDA+1.
Pre zrušenie nápovedy opäť stlačte NVDA+1.
Počas spustenej tejto nápovedy môžete ľubovoľne stláčať klávesové skratky a vykonávať gestá na dotykovej obrazovke a NVDA vám povie viac o ich funkcii ak je k práve vykonanému príkazu nejaká funkcia vôbec priradená.
Príkazy nebudú aktívne vykonávané, budete počuť len patričné informácie k popisu funkcie.

### Ponuka NVDA {#TheNVDAMenu}

Ponuka NVDA umožňuje meniť nastavenia, čítať pomocníka, načítať a uložiť konfiguráciu, editovať rečové slovníky, pristupovať k ďalším nástrojom a ukončiť NVDA.

Pre vstup do ponuky NVDA odkiaľkoľvek zo systému Windows počas behu NVDA môžete použiť niektorý z nasledujúcich postupov:

* Stlačte na klávesnici skratku `nvda+n`.
* Dvakrát poklepte dvoma prstami na obrazovku.
* Ponuku môžete vyvolať aj zo systémového panelu. Stlačte `windows+b`. `Šípkami` Vyhľadajte tlačidlo  NVDA a aktivujte ho klávesom `Enter`.	
* Môžete postupovať aj tak, že skratkou `windows+b` prejdete na systémový panel, `šípkami hore a dole` vyhľadáte tlačidlo NVDA a aktivujete kontextovú ponuku klávesom `aplikácie`. Tento sa zvyčajne nachádza vedľa klávesu pravý kontrol.
Ak sa na klávesnici tlačidlo `aplikácie` nenachádza, môžete ju vyvolať skratkou `shift+f10`.
* Ponuku NVDA  je možné vyvolať aj kliknutím pravým tlačidlom myši na ikone NVDA na systémovom panely.

Po zobrazení ponuky programu môžete použiť šípky na pohyb po položkách, klávesom `enter` aktivujete aktuálnu položku.

### Všeobecné príkazy NVDA {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |klávesová skratka pre Laptop |Dotykové gesto |Popis|
|---|---|---|---|---|
|Spustiť alebo reštartovať NVDA |ctrl+alt+n |ctrl+alt+n |nie je |Spustí alebo reštartuje NVDA. Túto skratku je potrebné povoliť počas inštalácie NVDA. Ide o skratku definovanú v systéme Windows a preto nie je možné ju meniť v dialógu klávesové skratky.|
|Zastaviť reč |ctrl |ctrl |Klepnutie dvoma prstami |Okamžite zastaví reč|
|Pozastaviť reč |Shift |shift |Nie je |Okamžite pozastaví reč. Po nasledujúcom stlačení bude reč pokračovať na prerušenom mieste ak to práve používaný hlasový výstup podporuje|
|Ponuka NVDA |NVDA+n |NVDA+n |Dvojnásobné klepnutie dvoma prstami |Zobrazí ponuku NVDA, odkiaľ je možné pristupovať k nastaveniam, nástrojom a pomocníkovi|
|Nápoveda vstupu |NVDA+1 |NVDA+1 |Nie je |Zapína a vypína nápovedu vstupu. Každý vstup ako napríklad stlačenie klávesu spôsobí, že NVDA ohlási názov a popis skriptu, ktorý je s danou kombináciou asociovaný. Pre vypnutie stlačte znova NVDA+1.|
|Ukončiť NVDA |NVDA+q |NVDA+q |Nie je |Opýta sa či naozaj chcete ukončiť NVDA. V dialógu všeobecné nastavenia je voľba, ktorou sa otázka pred ukončením dá vypnúť.|
|Prepustiť nasledujúci kláves |NVDA+f2 |NVDA+f2 |Nie je |Prinúti NVDA nasledujúci stlačený kláves prepustiť aktívnej aplikácii aj keď sa jedná o príkaz programu NVDA.|
|Prepnúť režim spánku |NVDA+shift+s |NVDA+shift+z |Nie je |Režim spánku deaktivuje všetky klávesové skratky a hlasový a brailový výstup. Toto je užitočné pre aplikácie, ktoré sami poskytujú niektorý z takýchto druhov výstupu. Režim spánku sa automaticky vypne po reštarte NVDA.|

<!-- KC:endInclude -->

### Oznamovanie systémových informácii {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Čas a dátum |NVDA+f12 |Oznámi čas; stlačené 2 krát rýchlo po sebe oznámi dátum.|
|Stav napájania z batérie |NVDA+shift+b |Oznámi informácie o stave napájania. Buď oznámi stav nabitia batérie v percentách, alebo oznámi nabíjanie zo siete.|
|Oznámiť text v schránke Windows |NVDA+c |Ak je v schránke Windows text, NVDA ho oznámi.|

<!-- KC:endInclude -->

### Režimi reči {#SpeechModes}

Režimi reči určujú, ako NVDA oznamuje zmeny na obrazovke, notifikácie, príkazy a podobne.
Predvolene je nastavený režim "reč". NVDA tak oznamuje všetky užitočné informácie tak, ako očakávame od čítača obrazovky.
V niektorých situáciách a pri niektorých aplikáciách však môžete chcieť zmeniť správanie NVDA.

Dostupné sú tieto režimi:

* Reč (predvolené): NVDA bude oznamovať zmeny na obrazovke, čítať notifikácie, hlásiť zmeny fokusu a hlásiť informácie požadované skratkami.
* Na vyžiadanie: NVDA bude hovoriť len ak si vyžiadate informáciu príkazom alebo klávesovou skratkou, napríklad si necháte prečítať názov okna alebo aktuálne zameranie. Nebude však oznamovať zmeny fokusu či pohyb kurzora.
* Bez reči: NVDA nebude oznamovať vôbec nič, bude však vykonávať funkcie napozadí. (Poznámka prekladateľa: Toto je užitočné pre používateľov brailových riadkov, ktorý môžu takto používať NVDA čisto len s využitím brailového riadka).
* Pípanie: NVDA namiesto reči bude len pípať.

Pípanie môže byť užitočné, keď sledujete priebeh v okne terminálu. Nie je pre vás dôležitý obsah, ale potrebujete vedieť, že sa stále generuje výstup ako taký.

Režim na vyžiadanie je užitočný, ak nepotrebujete neustály výstup, ale zároveň chcete, aby NVDA oznamoval niektoré udalosti.
Toto je užitočné napríklad pri práci v zvukových editoroch, počas konferenčného hovoru, alebo tiež pri sledovaní výstupu v konzolových aplikáciách.

Na prepínanie režimov je možné využiť skratku:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |popis|
|---|---|---|
|Prepnúť režim reči |`NVDA+s` |Prepína medzi dostupnými režimami reči|

<!-- KC:endInclude -->

Ak nepotrebujete všetky dostupné režimi reči, pozrite si [Ako zakázať a povoliť určité režimi](#SpeechModesDisabling).

## Pohyb v NVDA {#NavigatingWithNVDA}

NVDA umožňuje používateľovi rôzne spôsoby navigácie vrátane klasickej interakcie a prezerania.

### Objekty {#Objects}

Každá aplikácia, dokonca aj samotný operačný systém, obsahuje množstvo objektov.
Objekt v tomto prípade je jediná položka: kúsok textu, tlačidlo, začiarkávacie políčko, posuvník alebo aj editačné pole.

### Pohyb pomocou zamerania systémového fokusu {#SystemFocus}

Systémový fokus, často nazývaný skrátene len fokus, je [objekt](#Objects), ktorý reaguje na klávesy stlačené na klávesnici.
Napríklad v čase, keď píšete text do editačného poľa, má fokus toto editačné pole.

Najbežnejší spôsob pohybu v systéme Windows s NVDA je používanie obvyklých klávesových skratiek pre pohyb po ovládacích prvkoch: tab a shift+tab, vyvolanie panela ponúk pomocou klávesu alt, pohyby v ponukách prostredníctvom kurzorových šípok, či prepínanie sa medzi spustenými aplikáciami alt+tab.
Toto spôsobuje zmeny systémového fokusu, objektu, ktorý práve reaguje na príkazy z klávesnice. NVDA reaguje na zmeny fokusu, čo spôsobuje, že  budete počuť informáciu o názve objektu, type, hodnote, popise, jeho klávesovú skratku, či informáciu o pozícii vzhľadom na susediace objekty.
Ak je zapnuté [zvýraznenie na obrazovke](#VisionFocusHighlight), systémový fokus je zvýraznený aj na obrazovke.

Pri zameraní fokusu možno použiť niekoľko užitočných skratiek:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre Desktop |Klávesová skratka pre Laptop |Popis|
|---|---|---|---|
|Fokus |NVDA+tab |NVDA+tab |Oznámi alebo vyhláskuje meno objektu, ktorý má systémový fokus|
|názov okna |NVDA+t |NVDA+t |Oznámi titulok aktuálneho aplikačného okna alebo okna v popredí. Stlačené 2 krát rýchlo za sebou vyhláskuje názov okna a stlačené 3 krát rýchlo za sebou skopíruje názov aktuálneho okna do schránky.|
|obsah okna v popredí |NVDA+b |NVDA+b |Oznámi všetky prvky aktuálneho okna v popredí (užitočné pre dialógy)|
|Stavový riadok |NVDA+end |NVDA+shift+end |Oznámi obsah stavového riadku ak ho NVDA dokáže nájsť. Stlačené dvakrát stavový riadok vyhláskuje. Stlačené trikrát skopíruje obsah stavového riadka do schránky|
|Oznámiť klávesovú skratku |`shift+numerická 2` |`NVDA+ctrl+shift+.` |Oznámi klávesovú (podčiarknutú) skratku zameraného objektu|

<!-- KC:endInclude -->

### Pohyb pomocou textového kurzora {#SystemCaret}

Ak má [fokus](#SystemFocus) [objekt](#Objects), ktorý podporuje navigáciu alebo úpravu textu, je možné pohybovať sa v texte pomocou systémového kurzora.

Ak je fokus v poli, ktoré má textový kurzor, môžete text čítať bežnými navigačnými klávesmi ako napríklad šípky, page up, page down, home a end.
Ak pole podporuje editáciu, môžete text aj meniť.
NVDA bude oznamovať pohyb po znakoch, slovách, riadkoch, a tiež bude indikovať vybratý a nevybratý text.

NVDA obsahuje nasledujúce klávesové skratky súvisiace so systémovým kurzorom:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre Desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|Plynulé čítanie |NVDA+šípka dolu |NVDA+A |Prečíta text od pozície systémového kurzora do konca textu pri čom sa systémový kurzor posúva|
|Aktuálny riadok |NVDA+šípka hore |NVDA+l |Prečíta   aktuálny riadok zameraný systémovým kurzorom. Stlačené dvakrát rýchlo za sebou vyhláskuje riadok a stlačené trikrát za sebou vyhláskuje riadok foneticky.|
|Aktuálny výber |NVDA+Shift+šípka hore |NVDA+shift+s |Oznámi práve vybratý text|
|Oznámiť formátovanie textu |NVDA+f |NVDA+f |Oznámi formátovanie pod textovým kurzorom. Stlačené dvakrát za sebou zobrazí informáciu v režime prehliadania|
|Oznámiť cieľ odkazu |`NVDA+k` |`NVDA+k` |Prečíta cieľ, zvyčajne url adresu odkazu pod kurzorom. Stlačené dvakrát zobrazí cieľ v samostatnom okne, kde je možné s údajom podrobnejšie pracovať|
|Oznámiť súradnice kurzora |NVDA+numerický Delete |NVDA+delete |Oznámi informáciu o súradniciach textu, alebo objektu pod textovým kurzorom. Toto môže zahŕňať oznámenie percent prečítaného dokumentu, alebo vzdialenosť objektu od okrajov alebo presné súradnice na obrazovke. Stlačené dvakrát poskytne podrobnejšie informácie.|
|Nasledujúca veta |alt+šípka dole |alt+šípka dole |presunie systémový kurzor na nasledujúcu vetu a prečíta ju (platí len pre Microsoft Word a Outlook)|
|Predchádzajúca veta |alt+šípka hore |alt+šípka hore |Presunie systémový kurzor na predchádzajúcu vetu a prečíta ju (platí len pre Microsoft Word a Outlook)|

Pri navigácii v tabuľkách sú tiež dostupné tieto klávesové príkazy:

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Predchádzajúci stĺpec |ctrl+alt+ľavá šípka |Prejde do predchádzajúcej bunky v aktuálnom riadku|
|Nasledujúci stĺpec |ctrl+alt+pravá šípka |Prejde do nasledujúcej bunky v aktuálnom riadku|
|Predchádzajúci riadok |ctrl+alt+šípka hore |Prejde do aktuálnej bunky v predchádzajúcom riadku|
|Ďalší riadok |ctrl+alt+šípka dolu |Prejde do aktuálnej bunky v nasledujúcom riadku|
|Prejdi na prvý stĺpec |ctrl+alt+home |Presunie systémový kurzor na prvý stĺpec (v tom istom riadku)|
|Prejdi na posledný stĺpec |ctrl+alt+end |Presunie systémový kurzor na posledný stĺpec (v tom istom riadku)|
|Prejdi na prvý riadok |ctrl+alt+pageUp |Presunie systémový kurzor na prvý riadok (v tom istom stĺpci)|
|Prejdi na posledný riadok |ctrl+alt+pageDown |Presunie systémový kurzor na posledný riadok (v tom istom stĺpci)|
|Plynulé čítanie stĺpca |`NVDA+ctrl+alt+šípka dolu` |Zvislo číta obsah stĺpca od aktuálnej bunky smerom dolu až po poslednú bunku v stĺpci.|
|Plynulé čítanie riadku |`NVDA+ctrl+alt+pravá šípka` |Vodorovne číta obsah riadku od aktuálnej bunky vpravo až po poslednú bunku v riadku.|
|prečítať celý stĺpec |`NVDA+ctrl+alt+šípka hore` |Zvislo číta celý stĺpec od hora po spodok bez posúvania systémového kurzora.|
|Prečítať celý riadok |`NVDA+ctrl+alt+ľavá šípka` |Vodorovne číta celý riadok z ľava vpravo bez posúvania systémového kurzora.|

<!-- KC:endInclude -->

### Objektová navigácia {#ObjectNavigation}

Najčastejšie budete pravdepodobne pracovať s aplikáciami pomocou príkazov, ktoré menia [fokus](#SystemFocus) alebo s takými, ktoré majú[ textový kurzor](#SystemCaret).
Niekedy môžete potrebovať prezrieť si aktuálnu aplikáciu alebo položky operačného systému bez toho, že by sa zmenil systémový fokus alebo pozícia systémového kurzora.
Taktiež sú situácie, keď potrebujete pracovať s [objektmi](#Objects), ktoré nepodporujú navigáciu z klávesnice.
V takýchto prípadoch môžete použiť objektovú navigáciu.

Objektová navigácia vám umožní presúvať sa a získavať informácie o jednotlivých [objektoch](#Objects).
Pri zameraní objektu objektovou navigáciou, NVDA oznámi tento objekt podobne ako oznamuje systémový fokus.
Ak si chcete len prečítať všetok text zobrazený na obrazovke, môžete tiež použiť [prezeranie obrazovky](#ScreenReview).

Aby nebolo nutné prechádzať vždy dopredu a dozadu cez každý objekt systému, objekty sú organizované hierarchicky.
Toto znamená, že aby ste mohli skúmať objekty, ktoré obsahujú ďalšie objekty, musíte sa do niektorých z nich vnoriť.
Napríklad ak zameriate zoznam, nie je možné prelistovať všetky jeho položky, ale je potrebné sa pohybovať vo vnútri zoznamu, prejsť na prvý podradený objekt.
Ak zameriate položku zoznamu, prechádzaním na predchádzajúci alebo nasledujúci objekt prejdete na ostatné položky toho istého zoznamu.
Prechodom na nadradený objekt položky zoznamu sa vrátite naspäť na zoznam.
Ak chcete preskúmať ďalšie objekty za zoznamom, môžete sa presunúť na nasledujúci objekt.
Veľmi podobne aj panel nástrojov obsahuje viaceré prvky. Aby ste mohli tieto prvky preskúmať, musíte sa po zameraní panela nástrojov doň vnoriť.

Ak si chcete pozerať všetky objekty v systéme samostatne, môžete na prechod na nasledujúci a predchádzajúci objekt použiť príkazy plošného prezerania.
Ak napríklad v plošnom prezeraní prejdete na nasledujúci objekt a aktuálny objekt obsahuje vnorené objekty, NVDA sa automaticky zanorí na prvý vnorený objekt.
Ak aktuálny objekt neobsahuje vnorené objekty, NVDA prejde na nasledujúci objekt v aktuálnej hierarchii.
Ak na tejto úrovni nie sú ďalšie objekty, NVDA skúsi nájsť objekt o úroveň vyššie, až dokým už nie je možné nájsť objekty o úroveň vyššie.
Rovnako funguje pohyb aj v opačnom smere.

Objekt, ktorý si práve týmto spôsobom prezeráte je nazývaný navigačný objekt.
Po zameraní objektu je možné [prezerať text objektu](#ReviewingText) ak sa nachádzate v [prezeraní objektov](#ObjectReview).
Ak je zapnuté [zvýraznenie na obrazovke](#VisionFocusHighlight), navigačný objekt  je zvýraznený aj na obrazovke.
Ak presuniete fokus na iný objekt, predvolene sa  zmení  aj objekt ktorý prezeráte, avšak toto je možné vypnúť a zapnúť podľa potreby.

Sledovanie objektov na brailovom riadku je možné nastaviť s použitím funkcie [zviazania brailového kurzora](#BrailleTether).

Pre pohyb po objektoch použite nasledujúce príkazy:

<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre laptop |Dotykové gesto |Popis|
|---|---|---|---|---|
|Aktuálny objekt |NVDA+numerická 5 |NVDA+shift+o |Nie je |Oznámenie aktuálneho objektu - pri stlačení 2 krát je informácia vyhláskovaná a tri krát rýchlo za sebou je obsah skopírovaný do schránky.|
|Nadradený objekt |NVDA+numerická8 |NVDA+shift+šípka hore |Švihnutie hore |Prejde na objekt, ktorý obsahuje aktuálny navigačný objekt|
|Predchádzajúci objekt |NVDA+numerická4 |NVDA+shift+ľavá šípka |nie je |Prejde na predchádzajúci objekt od navigačného objektu|
|Predchádzajúci objekt v plošnom prezeraní |NVDA+numerická9 |NVDA+shift+[ |Švihnutie vľavo (objektový režim) |Prejde na predchádzajúci dostupný objekt v plošnom prezeraní|
|nasledujúci objekt |NVDA+numerická6 |NVDA+shift+pravá šípka |nie je |Prejde na nasledujúci objekt od navigačného objektu|
|Nasledujúci objekt v plošnom prezeraní |NVDA+numerická3 |NVDA+shift+] |švihnutie vpravo (objektový režim) |Prejde na nasledujúci dostupný objekt v plošnom prezeraní|
|Prvý podradený objekt |NVDA+numerická2 |NVDA+shift+šípka dolu |Švihnutie dolu |Pohyb na prvý objekt, ktorý je vo vnútri navigačného objektu|
|navigačný objekt na fokus |NVDA+numerické Mínus |NVDA+backspace |Nie je |Premiestni navigačný objekt na prvok, ktorý má systémový fokus. Ak je zobrazený systémový kurzor, pokúsi sa nastaviť na jeho pozíciu aj prezerací kurzor|
|Aktivovať navigačný objekt |NVDA+numerický Enter |NVDA+enter |Dvojité klepnutie |Aktivuje prvok práve zameraný objektovou navigáciou - rovnaké ako stlačenie klávesu enter alebo dvojité kliknutie po zameraní kurzorom myši.|
|Fokus alebo systémový kurzor na pozíciu prezeracieho kurzora |NVDA+shift+numerické mínus |NVDA+shift+backspace |Nie je |Po prvom stlačení nastaví fokus na navigačný objekt, po druhom stlačení sa pokúsi umiestniť systémový kurzor na pozíciu prezeracieho kurzora|
|Súradnice kurzora v režime prezerania |NVDA+shift+numerický Delete |NVDA+delete |Nie je |Oznamuje polohu prezeracieho kurzora. Informácia môže pozostávať z polohy v dokumente uvedenej v percentách, vzdialenosti od začiatku stránky alebo presnej polohy na obrazovke. Podrobnejšie informácie NVDA prečíta po dvojitom stlačení.|
|Premiestniť prezerací kurzor  na stavový riadok |nie je |nie je |nie je |Oznámi stavový riadok, ak ho NVDA dokáže nájsť. Tiež premiestni prezerací kurzor na stavový riadok.|

<!-- KC:endInclude -->

Všimnite si: Numerický blok musí byť vypnutý, aby všetky skratky fungovali korektne.

### Prezeranie textu {#ReviewingText}

NVDA umožňuje čítať obsah [obrazovky](#ScreenReview), obsah aktuálneho [dokumentu](#DocumentReview) alebo [objektu](#ObjectReview) po slovách, riadkoch alebo aj po znakoch.
Toto je užitočné v príkazovom riadku Windows, alebo na iných miestach, kde nie je dostupný [systémový kurzor](#SystemCaret).
Týmto spôsobom si napríklad môžete po častiach prečítať dlhšiu informatívnu správu v dialógových oknách.

Počas posúvania prezeracím kurzorom sa systémový kurzor nepohybuje, čo znamená, že môžete čítať text bez toho, že by Ste stratili aktuálne upravovanú pozíciu.
Pri pohybe systémovým kurzorom sa prezerací kurzor automaticky prispôsobuje pozícii systémového kurzora.
Túto vlastnosť je možné prepínať.

Text zobrazovaný na brailovom riadku môžete prispôsobiť nastavením [zviazania brailového kurzoru](#BrailleTether).

Na navigáciu v texte je možné použiť nasledovné príkazy:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre Laptop |Dotykové gesto |Popis|
|---|---|---|---|---|
|Prezerací kurzor do prvého riadku |shift+numerická 7 |NVDA+ctrl+home |Nie je |Presunie prezerací kurzor do prvého riadku textu|
|Prezerací kurzor do predchádzajúceho riadku |numerická 7 |NVDA+šípka hore |Švihnutie hore (textový režim) |Presunie prezerací kurzor do predchádzajúceho riadku textu|
|Aktuálny riadok prezeracieho kurzora |numerická 8 |NVDA+shift+bodka |Nie je |Oznámi riadok, na ktorý ukazuje prezerací kurzor. Dvojnásobné stlačenie vyhláskuje riadok. Stlačené tri krát rýchlo za sebou foneticky vyhláskuje riadok.|
|Prezerací kurzor do nasledujúceho riadku |numerická 9 |NVDA+šípka dolu |Švihnutie dolu (textový režim) |Presunie prezerací kurzor do nasledujúceho riadku textu|
|Prezerací kurzor do posledného riadku |shift+numerická 9 |NVDA+ctrl+end |Nie je |Presunie prezerací kurzor do posledného riadku textu|
|Prezerací kurzor na predchádzajúce slovo |numerická 4 |NVDA+ctrl+ľavá šípka |Švihnutie vľavo dvoma prstami (textový režim) |Presunie prezerací kurzor na predchádzajúce slovo textu|
|Aktuálne slovo prezeracieho kurzora |numerická 5 |NVDA+ctrl+bodka |Nie je |Oznámi slovo, na ktoré práve ukazuje prezerací kurzor. Dvojnásobné stlačenie vyhláskuje slovo. Stlačené tri krát rýchlo za sebou foneticky vyhláskuje aktuálne slovo.|
|Prezerací kurzor na nasledujúce slovo |numerická 6 |NVDA+ctrl+pravá šípka |Švihnutie vpravo dvoma prstami (textový režim) |Presunie prezerací kurzor na nasledujúce slovo textu|
|Prezerací kurzor na začiatok riadku |shift+numerická 1 |NVDA+home |Nie je |Presunie prezerací kurzor na začiatok aktuálneho riadku textu|
|Prezerací kurzor na predchádzajúci znak |numerická 1 |NVDA+ľavá šípka |Švihnutie vľavo (textový režim) |Presunie prezerací kurzor na predchádzajúci znak v aktuálnom riadku textu|
|Aktuálny znak prezeracieho kurzora |numerická 2 |NVDA+bodka |Nie je |Oznámi aktuálny znak prezeracieho kurzora. Dvojnásobné stlačenie vyhláskuje alebo oznámi príklad použitia znaku. Stlačené tri krát rýchlo po sebe oznámi ten istý znak v numerickom a hexadecimálnom formáte.|
|Prezerací kurzor na nasledujúci znak |numerická 3 |NVDA+pravá šípka |Švihnutie vpravo (textový režim) |Presunie prezerací kurzor na nasledujúci znak v aktuálnom riadku textu|
|Prezerací kurzor na koniec riadku |shift+numerická 3 |NVDA+end |Nie je |Presunie prezerací kurzor na koniec aktuálneho riadku textu|
|Prezerací kurzor na predchádzajúcu stranu |`NVDA+pageUp` |`NVDA+shift+pageUp` |nie je |Presunie prezerací kurzor na predchádzajúcu stranu textu ak je podporované aplikáciou|
|Prezerací kurzor na nasledujúcu stranu |`NVDA+pageDown` |`NVDA+shift+pageDown` |nie je |Presunie prezerací kurzor na nasledujúcu stranu textu ak je podporované aplikáciou|
|Plynulé čítanie prezeracím kurzorom |numerické Plus |NVDA+shift+a |Švihnutie dolu troma prstami (textový režim) |Číta od aktuálnej pozície prezeracieho kurzora a posúva sa smerom dolu.|
|Začiatok bloku kopírovania prezeracím kurzorom |NVDA+f9 |NVDA+f9 |Nie je |Označí aktuálnu pozíciu ako začiatok výberu a bloku na kopírovanie do schránky. Kopírovanie sa neuskutoční kým neurčíte koniec bloku kopírovania.|
|Koniec bloku kopírovania prezeracím kurzorom |NVDA+f10 |NVDA+f10 |Nie je |Po prvom stlačení označí text  od označeného miesta po aktuálnu pozíciu prezeracieho kurzora. Ak systémový kurzor dokáže nájsť text, označí ho. Po dvojitom stlačení skopíruje text od značky po aktuálnu pozíciu  do schránky Windows.|
|Presunúť prezerací  kurzor na začiatok bloku na kopírovanie alebo označenie |NVDA+shift+f9 |NVDA+shift+f9 |nie je |Presunie prezerací kurzor na miesto, ktoré ste označili ako začiatok bloku na kopírovanie alebo označenie|
|formátovanie textu |NVDA+shift+f |NVDA+shift+f |Nie je |Oznámi formátovanie textu na pozícii prezeracieho kurzora. Po dvojitom stlačení zobrazí informáciu v režime prehliadania.|
|Prečítať výslovnosť symbolu |Nie je |Nie je |Nie je |Prečíta symbol pod prezeracím kurzorom. Dvojité stlačenie zobrazí dialóg, v ktorom je možné prečítať si textový popis symbolu v režime prehliadania.|

<!-- KC:endInclude -->

Všimnite si: Pri týchto operáciách musí byť numerický blok vypnutý, aby skratky fungovali správne.

Aby ste si mohli lepšie zapamätať priradenie klávesových skratiek všimnite si, že základné príkazy navigácie textom v rozložení pre desktop sú usporiadané do pomyselnej tabuľky tri krát tri, kde riadok, slovo, znak smerujú z hora dolu a predchádzajúci, aktuálny, nasledujúci zľava doprava. 
Toto rozloženie je ilustrované v nasledujúcej tabuľke:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|predchádzajúci riadok |aktuálny riadok |nasledujúci riadok|
|predchádzajúce slovo |aktuálne slovo |nasledujúce slovo|
|predchádzajúci znak |aktuálny znak |nasledujúci znak|

### Režimy prezerania {#ReviewModes}

Režimy prezerania vám umožňujú [čítať obsah](#ReviewingText) aktuálneho objektu, aktuálneho dokumentu alebo obrazovky, v závislosti od toho, aký režim prezerania si vyberiete.

Na prepínanie medzi režimami prezerania použite nasledujúce klávesové skratky:
<!-- KC:beginInclude -->

| názov |klávesová skratka pre Desktop |klávesová skratka pre Laptop |dotykové gesto |popis|
|---|---|---|---|---|
|Nasledujúci režim prezerania |NVDA+numerická 7 |NVDA+pageUp |švihnutie dvomi prstami nahor |Prepne na nasledujúci  režim prezerania|
|predchádzajúci režim prezerania |NVDA+numerická 1 |NVDA+pageDown |švihnutie dvomi prstami nadol |prepne na predchádzajúci režim prezerania|

<!-- KC:endInclude -->

#### Prezeranie objektu {#ObjectReview}

Pri prezeraní objektu si môžete prezerať len navigačný objekt zameraný [objektovou navigáciou](#ObjectNavigation).
Pre editačné polia a iné vstupné prvky budete najčastejšie vidieť text konkrétneho prvku.
Pre iné objekty môžete vidieť ich popis, hodnotu alebo oboje.

#### Prezeranie dokumentu {#DocumentReview}

Ak je [navigačný  objekt](#ObjectNavigation) v režime prehliadania (napríklad na internetovej stránke), alebo v inom komplexnom dokumente (napríklad dokumenty programu Lotus Symphony), môžete sa prepnúť do režimu prezerania dokumentu.
V tomto režime sa zobrazí text celého dokumentu.

Ak sa z prezerania objektu prepnete do prezerania dokumentu, prezerací kurzor sa presunie na miesto, kde je navigačný objekt.
Ak sa pohybujete kurzorom po dokumente, navigačný objekt sa automaticky presúva na objekty pod kurzorom.

Všimnite si, že NVDA sa automaticky prepne do prezerania dokumentu vždy, keď budete v režime prehliadania.

#### Prezeranie obrazovky {#ScreenReview}

Režim prezerania obrazovky umožňuje prezerať text v okne práve otvorenej aplikácie tak, ako je viditeľný na obrazovke.
Toto funguje podobne, ako emulácia myši alebo virtualizácia okna v ostatných čítačoch obrazovky pre Windows.

Ak sa prepnete do prezerania obrazovky, prezerací kurzor sa presunie na pozíciu [navigačného objektu](#ObjectNavigation).
Pri pohybe prezeracím kurzorom sa navigačný objekt presunie na objekt nájdený pod kurzorom.

Všimnite si, že NVDA nedokáže rozpoznať text v niektorých nových aplikáciách, čo je spôsobené technikami vykresľovania, ktoré zatiaľ nie sú podporované.

### Pohyb myšou {#NavigatingWithTheMouse}

Počas posúvania myšou, v predvolenom nastavení NVDA oznamuje text, ktorým prechádza kurzor myši.
Na niektorých miestach dokáže NVDA oznámiť celý odsek, inde len aktuálny riadok.

NVDA je možné nastaviť tak, že okrem textu bude oznamovať aj typ [prvku](#Objects), cez ktorý prechádza kurzor myši ako napr. tlačidlo alebo zoznam.
Toto môže byť užitočné pre úplne nevidiacich používateľov.

NVDA používateľovi ponúka aj možnosť akustickej signalizácie polohy myši na základe vzdialenosti od okrajov obrazovky.
Čím vyššie sa myš na obrazovke nachádza, tým vyššie je pípanie.
Pre pravú a ľavú stranu sa pípanie presúva z jedného kanála do druhého, predpokladá sa, že používateľ má k dispozícii stereo reproduktory,.

Tieto funkcie v NVDA nie sú štandardne zapnuté.
Aktivovať je ich možné v kategórii  [nastavenia myši](#MouseSettings) v [Nastaveniach](#NVDASettings) z ponuky možnosti.

Aj napriek tomu, že sa na tento druh navigácie bežne používa myš alebo trackpad, NVDA má zabudovaných niekoľko klávesových skratiek, ktoré simulujú niektoré funkcie ukazovacieho zariadenia:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre laptop |Dotykové gesto |Popis|
|---|---|---|---|---|
|Ľavý klik |numerické lomeno |NVDA+ú |nie je |Vykoná klik ľavým tlačidlom myši. Dvojklik je možné nasimulovať stlačením tejto skratky dva krát rýchlo za sebou.|
|Zamknúť ľavé tlačidlo myši |shift+numerické  lomeno |NVDA+ctrl+ú |nie je |Stlačí a uzamkne ľavé tlačidlo myši. Stlačte znovu na uvoľnenie. Operáciu drag & drop môžete začať uzamknutím tlačidla použitím tohto príkazu a následne posunúť myš fyzicky alebo pomocou iných klávesových príkazov.|
|Pravý klik |numerická hviezdička |NVDA+ä |klepnúť a podržať |Vykoná klik pravým tlačidlom myši.|
|Zamknúť pravé tlačidlo myši |shift+numerická  hviezdička |NVDA+ctrl+ä |nie je |Stlačí a uzamkne pravé tlačidlo myši. Stlačte znovu na uvoľnenie. Operáciu drag & drop môžete začať uzamknutím tlačidla použitím tohto príkazu a následne posunúť myš fyzicky alebo pomocou iných klávesových príkazov.|
|Myš na navigačný objekt |NVDA+numerické  lomeno |NVDA+shift+m |nie je |Premiestni kurzor myši na miesto aktuálneho prvku zameraného objektovou navigáciou na mieste, kde ukazuje prezerací kurzor|
|Objektová navigácia na myš |NVDA+numerická hviezdička |NVDA+shift+n |nie je |Nastaví objektovú navigáciu na prvok, na ktorého umiestnenie ukazuje kurzor myši|

<!-- KC:endInclude -->

## Režim prehliadania {#BrowseMode}

Súhrnnejšie dokumenty, ako napríklad web stránky, nám NVDA dokáže zobraziť v TZV. režime prehliadania.
Toto zahŕňa dokumenty v programoch:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML správy v programe Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Podporované knihy v aplikácii Amazon Kindle pre  PC

Režim prehliadania môžete aktivovať aj v dokumentoch programu Microsoft Word.

V režime prehliadania je obsah dokumentu usporiadaný plošne, takže na navigáciu je možné použiť bežné navigačné príkazy ako v prípade textových dokumentov.
V tomto režime fungujú štandardné klávesové skratky na [čítanie textu systémovým kurzorom](#SystemCaret) ako napríklad plynulé čítanie, informácie o formátovaní a navigačné príkazy po tabuľkách.
Ak je zapnuté [zvýraznenie na obrazovke](#VisionFocusHighlight), pozícia kurzora v režime prehliadania je zvýraznená aj na obrazovke.
Informácia o type prvku napr. či sa jedná o odkaz, nadpis a podobne je automaticky oznamovaná pri pohybe.

Niektoré situácie si vyžadujú interakciu priamo s prvkami v dokumente.
Napríklad, keď potrebujete písať do editačného poľa alebo pomocou kurzorových klávesov vybrať položku v zozname.
Vtedy je vhodné prepnúť do režimu fokusu a klávesové príkazy sú prepúšťané priamo prvku, ktorý má fokus.
Ak čítate dokument v režime prehliadania a presuniete sa na prvok, ktorý si vyžaduje interakciu, predvolene sa NVDA automaticky prepne do režimu fokusu.
Naopak ak sa napr. stláčaním klávesu tab presuniete na prvok, ktorý si nevyžaduje priamu interakciu, NVDA sa prepne automaticky späť do režimu prehliadania.
Na prepínanie z režimu prehliadania do režimu fokusu je tiež možné pri čítaní prvku, ktorý si to vyžaduje použiť stlačenie klávesov medzerník alebo enter.
Stlačením klávesu Esc sa vrátite do režimu prehliadania.
Nakoniec je možné režim fokusu vynútiť, v takom prípade ostane aktívny, až kým sa znovu nevrátite do režimu prehliadania.

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Prepnúť režimy fokusu / prehliadania |NVDA+medzera |Prepína medzi režimom fokusu a režimom prehliadania|
|Ukončiť režim fokusu |escape |Prepína do režimu prehliadania, ak bol režim fokusu aktivovaný automaticky|
|Obnoviť dokument v režime prehliadania |NVDA+f5 |Obnoví obsah aktuálneho dokumentu (užitočné ak časť obsahu nebola správne načítaná. Nie je dostupné v programoch Microsoft Word a Outlook.)|
|Hľadať |NVDA+ctrl+f |Zobrazí dialóg, ktorý umožní vyhľadávanie textu v aktuálnom dokumente. Podrobnosti sú popísané v časti [Hľadanie textu](#SearchingForText).|
|Hľadať ďalej |NVDA+f3 |Vyhľadá nasledujúci výskyt textu v aktívnom dokumente, ktorý Ste už hľadali|
|Hľadať späť |NVDA+shift+f3 |Vyhľadá predchádzajúci výskyt textu v aktívnom dokumente, ktorý Ste už hľadali|

<!-- KC:endInclude -->

### Príkazy rýchlej navigácie {#SingleLetterNavigation}

V režime prehliadania NVDA podporuje jednoznakové príkazy pre rýchlejší pohyb po prvkoch v dokumente.
Niektoré príkazy však nemusia byť dostupné vo všetkých typoch dokumentov.

<!-- KC:beginInclude -->
Za pomoci nasledujúcich klávesov sa môžete posúvať na nasledujúci prvok v dokumente, v opačnom smere sa môžete pohybovať kombinovaním príkazov s klávesom shift.

* h: nadpis
* l: zoznam
* i: položka zoznamu
* t: tabuľka
* k: odkaz
* n: text, ktorý nie je odkazom
* f: prvok formulára
* u: nenavštívený odkaz
* v: navštívený odkaz
* e: editačné pole
* b: tlačidlo
* x: začiarkavacie políčko
* c: zoznamový rámik
* r: prepínač
* q: citácia
* s: oddeľovač
* m: rámik
* g: grafika
* d: oblasť stránky
* o: vnorený objekt (audio a video prehrávač, aplikácia, dialóg...)
* 1-6: nadpis príslušnej úrovne
* a: anotácie (komentár, zmena alebo úprava)
* `p`: textový odsek
* w:  chyba

Rýchly prechod na začiatok alebo koniec skupín prvkov, ako napríklad zoznamov a tabuliek:

| Názov |Klávesová skratka |popis|
|---|---|---|
|Prejdi na začiatok skupiny prvkov |shift+čiarka |Presunie fokus na začiatok skupiny prvkov (zoznam, tabuľka a podobne) podľa aktuálneho prvku|
|prejdi za skupinu prvkov |čiarka |Presunie fokus za skupinu prvkov (zoznam, tabuľka a podobne) podľa aktuálneho prvku|

<!-- KC:endInclude -->

Niektoré aplikácie, ako Gmail, Twitter a Facebook používajú písmená ako klávesové skratky.
ak ich chcete používať a súčasne chcete čítať text pomocou kurzora, môžete dočasne vypnúť rýchlu navigáciu v režime prehliadania.
<!-- KC:beginInclude -->
Na zapnutie a vypnutie rýchlej navigácie v režime prehliadania, použite skratku NVDA+shift+medzera.
<!-- KC:endInclude -->

#### Navigácia po textových odsekoch {#TextNavigationCommand}

Na nasledujúci textový odsek môžete prejsť skratkou `p` a na predchádzajúci odsek skratkou `shift+p`.
Textové odseky sú definované ako kúsok textu, ktorý zvyčajne tvoria celé vety.
Toto môže byť užitočné pri vyhľadávaní väčších textových celkov na webových stránkach, ako napríklad:

* novinové články
* Fóra
* Blogy

Tieto príkazy vám môžu pomôcť rýchlo preskakovať rušivé prvky, ako napríklad:

* Reklamy
* Menu
* Hlavičky

Upozorňujeme, že hoci sa NVDA snaží čo najlepšie identifikovať textové odseky, niekedy nie je identifikácia dostatočne presná a môže byť chybová.
Navyše, príkaz je odlišný od navigácie po odsekoch skratkami `ctrl+šípky hore a dole`.
Príkazy na pohyb po odsekoch prechádzajú po odsekoch aj v prípade, že odseky neobsahujú text.

#### Ďalšie príkazy navigácie {#OtherNavigationCommands}

Okrem príkazov spomenutých vyššie, existujú aj ďalšie príkazy, ku ktorým ale predvolene nie sú priradené klávesové skratky.
Aby ste mohli používať tieto príkazy, musíte im priradiť klávesové skratky v [Dialógu klávesové skratky](#InputGestures).
Dostupné sú nasledujúce príkazy:

* Článok
* Ilustrácia
* Skupina
* Záložka
* Položka menu
* Prepínacie tlačidlo
* Indikátor priebehu
* Matematický obsah
* Vertikálne zarovnaný odsek
* Text s rovnakým formátovaním
* Text s odlišným formátovaním

Uvedomte si, že pre každý príkaz potrebujete dve skratky, jednu na pohyb v dokumente dopredu a jednu na pohyb v dokumente späť. Obe je potrebné nastaviť, aby ste mohli v dokumente prechádzať v oboch smeroch.
Ak napríklad chcete použiť `y` / `shift+y` na prechod medzi záložkami, budete postupovať nasledovne

1. Otvoríte si nejaký dokument v režime prehliadania a následne otvoríte dialóg s nastavením klávesových skratiek.
1. V časti režim prehliadania nájdete položku "prejde na nasledujúcu záložku".
1. Priradíte skratku `y`.
1. Nájdete položku "prejde na predchádzajúcu záložku".
1. Priradíte skratku `shift+y`.

### Zoznam prvkov {#ElementsList}

Dialóg zoznam prvkov zobrazuje zoznam rôznych  typov prvkov v závislosti od toho, v akej aplikácii tento dialóg otvoríte.
napríklad v internetových prehliadačoch zobrazuje  zoznam odkazov, nadpisov, formulárových prvkov, tlačidiel alebo zoznam oblastí dokumentu.
Pomocou výberového políčka je možné sa prepínať medzi jednotlivými typmi obsahu.
Dialóg obsahuje editačné pole, v ktorom môžete filtrovať obsah práve zobrazeného zoznamu.
Tlačidlami prejsť na alebo aktivovať vykonávame akcie pre prvky vybraté v zozname.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Zoznam prvkov v režime prehliadania |NVDA+f7 |Zobrazí dialóg so zoznamom   prvkov aktuálneho dokumentu|

<!-- KC:endInclude -->

### Hľadanie textu {#SearchingForText}

Tento dialóg vám umožní vyhľadávať reťazce v aktuálnom dokumente.
Text na vyhľadanie zadajte do editačného poľa "Napíšte text, ktorý chcete vyhľadať".
Ak chcete, aby sa pri hľadaní zohľadňovali aj malé a veľké písmená, začiarknite políčko "Rozlišovať malé a veľké písmená".
Ak začiarknete toto políčko a vyhľadáte reťazec "NV Access", NVDA vyhľadá len vtento reťazec a vynechá napríklad výskyt "nv access".
Na vyhľadávanie môžete použiť nasledujúce klávesové skratky:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Vyhľadať text |NVDA+ctrl+f |Otvorí dialóg s moľžnosťami hľadania|
|Vyhľadať nasledujúci výskyt |NVDA+f3 |Vyhľadá nasledujúci výskyt hľadaného reťazca od aktuálnej pozície kurzora|
|Vyhľadať predchádzajúce |NVDA+shift+f3 |Vyhľadá predchádzajúci výskyt reťazca od aktuálnej pozície kurzora|

<!-- KC:endInclude -->

### Vnorené objekty {#ImbeddedObjects}

Moderné webové stránky môžu byť obohatené o prvky Oracle Java a HTML5, ale aj o dialógy či aplikácie.
Ak sa tieto nachádzajú v dokumente, NVDA oznámi "vnorený objekt", "aplikácia", alebo "dialóg".
medzi týmito prvkami sa môžete pohybovať skratkami rýchlej  navigácie O a shift+O.
Stlačením klávesu enter môžete premiestniť fokus do takéhoto vnoreného objektu.
Ak je objekt prístupný, môžete sa v objekte pohybovať stláčaním klávesov tab alebo shift+tab.
Je možné použiť klávesovú skratku na prechod späť do dokumentu v ktorom je objekt vnorený.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Prejsť do nadradeného dokumentu |NVDA+ctrl+medzera |Premiestni fokus z aktuálneho vnoreného objektu do nadradeného dokumentu ktorý tento objekt obsahuje|

<!-- KC:endInclude -->

### Formátovaný výber {#NativeSelectionMode}

Keď označujete text pomocou `shift+šípky` v režime prehliadania, označuje sa len textová reprezentácia v rámci režimu prehliadania NVDA.
To znamená, že výber nie je vidieť na obrazovke. Navyše, ak skopírujete text pomocou `ctrl+c` do schránky, skopíruje sa len čistý text, v ktorom nie sú správne zobrazené odkazy a tabuľky.
Je však možné v NVDA zapnúť formátovaný výber pre určité dokumenty v režime prehliadania (aktuálne len v prehliadači Mozilla Firefox), čo spôsobí, že sa namiesto výberu v režime prehliadania použije výber priamo v prehliadači.

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Zapnúť alebo vypnúť režim formátovaného výberu |`NVDA+shift+f10` |Zapína a vypína režim formátovaného výberu|

<!-- KC:endInclude -->

Ak je formátovaný výber zapnutý, po stlačení `ctrl+c` použije natívne kopírovanie v rámci aplikácie, čo skopíruje do schránky aj informácie o formátovaní.
Ak takto skopírovaný obsah prilepíte napríklad do MS Wordu, alebo do tabuľky Excelu, bude správne zachované formátovanie tabuliek a odkazov.
Upozorňujeme však, že v tomto režime nie sú zachované niektoré popisky prístupnosti a informácie, ktoré NVDA zvyčajne zobrazuje v režime prehliadania.
Môže sa tiež stať, že výber v rámci aplikácie nebude úplne presný s výberom NVDA.
Ak však chcete skopírovať celý odsek alebo celú tabuľku, táto funkcia môže byť užitočná.

## Čítanie matematického obsahu {#ReadingMath}

NVDA umožňuje čítať matematický obsah a pohybovať sa v ňom, pričom poskytuje spätnú väzbu pomocou hlasového výstupu a tiež na brailovom riadku. Takýto obsah je možné sprístupniť vo webových prehliadačoch aj iných aplikáciách.
Aby bolo možné sprostredkovať matematický obsah, je potrebné nainštalovať ďalšie matematické komponenty.
V katalógu s doplnkami je dostupných viacero doplnkov, ktoré poskytujú podporu pre zobrazovanie a interpretáciu matematického obsahu, napríklad [MathCAT](https://nsoiffer.github.io/MathCAT/) a [Access8Math](https://github.com/tsengwoody/Access8Math). 
Podrobnosti o tom, ako nájsť a inštalovať doplnky sú uvedené v časti o [katalógu s doplnkami](#AddonsManager).
NVDA tiež dokáže využívať [MathPlayer](https://info.wiris.com/mathplayer-info) od spoločnosti Wiris, ak je prítomný v systéme. Mathplayer sa však už nevyvíja.

### Podporovaný obsah {#SupportedMathContent}

Ak sú nainštalované príslušné komponenty, NVDA podporuje tieto typy obsahu:

* MathML v prehliadačoch Mozilla Firefox, Microsoft Internet Explorer a google Chrome.
* Moderné matematické rovnice v Microsoft Word 365 cez rozhranie UI automation:
NVDA dokáže čítať a pracovať s matematickými rovnicami v Microsoft Word 365/2016 od zostavy 14326.
Upozorňujeme, že všetky doteraz zapísané rovnice je potrebné ručne konvertovať na office math.
Vyberte požadované rovnice, v kontextovej ponuke zvoľte možnosti rovníc a aktivujte položku konvertovať na office math.
Je potrebné používať aktuálnu verziu MathType. 
Microsoft Word podporuje lineárnu navigáciu v rovniciach linea a podporuje rôzne možnosti zápisu vrátane LateX.
Podrobnosti nájdete v dokumente [Lineárne formátovanie rovníc s použitím UnicodeMath a LaTeX vo Worde (anglicky)](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint a staršie verzie Microsoft Word:
NVDA dokáže čítať a sprostredkovať navigáciu v matematickom obsahu pre tieto aplikácie.
Je potrebné  nainštalovať MathType.
Postačuje skúšobná verzia.
Môžete ju stiahnuť zo stránok [MathType](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Tu  zatiaľ nie je dostupný oficiálny štandard, preto neexistuje software, ktorý by vedel takéto dokumenty vyrobiť.
* Čítačka Kindle pre PC:
NVDA dokáže sprostredkovať matematický obsah, pokiaľ je použitý správny zápis.

NVDA automaticky prečíta matematický  obsah počas čítania dokumentu.
Ak používate brailový riadok, matematický obsah sa zobrazí aj na brailovom riadku.

### Interakcia s matematickým obsahom {#InteractiveNavigation}

Ak na prácu s počítačom používate len hlasový výstup, pravdepodobne si budete chcieť matematický obsah čítať po častiach.

V režime prehliadania to môžete docieliť tak, že sa presuniete na matematický príklad a stlačíte enter.

Ak nie ste v režime prehliadania:

1. Presuňte prezerací kurzor na matematický príklad.
Predvolene prehliadací kurzor sleduje systémový kurzor, takže môžete na pohyb použiť systémový kurzor.
1. potom aktivujte tento príkaz:

<!-- KC:beginInclude -->

| Názov |klávesová skratka |Popis|
|---|---|---|
|Interakcia s matematickým obsahom |NVDA+alt+m |Umožní prácu s matematickým obsahom|

<!-- KC:endInclude -->

od tohto momentu sa aktivuje matematický režim, v ktorom je možné napríklad použiť šípky na prezeranie obsahu.
Napríklad ľavou a pravou šípkou sa pohybujete po matematickom výraze a šípkou dole rozbalíte konkrétnu časť výrazu, napríklad zlomok.

Ak príklad dočítate a chcete sa vrátiť, stlačte Escape.

Podrobnejšie informácie o dostupných príkazoch nájdete v dokumentácii k príslušnému matematickému komponentu.

* [Dokumentácia MathCAT (anglicky)](https://nsoiffer.github.io/MathCAT/users.html)
* [Dokumentácia Access8Math (anglicky)](https://github.com/tsengwoody/Access8Math)
* [Dokumentácia MathPlayer (anglicky)](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Môžete sa stretnúť s tým, že je matematický obsah zobrazený ako tlačidlo alebo iný prvok a až  po jeho stlačení sa zobrazia podrobnosti.
V tomto prípade na aktiváciu prvku použite skratku ctrl+enter.

### Inštalácia komponentu MathPlayer {#InstallingMathPlayer}

Hoci odporúčame používať niektorý z novších doplnkov pre NVDA, v niektorých špecifických prípadoch môže byť Mathplayer lepšou voľbou.
Je možné, že Mathplayer podporuje konkrétnu brailovú tabuľku, ktorá nie je dostupná v novších doplnkoch.
Mathplayer je možné stiahnuť zdarma z webových stránok Wiris.
[Stiahnuť MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Po inštalácii je potrebné reštartovať NVDA.
Pravdepodobne sa dočítate, že Mathplayer je dostupný len pre staršie prehliadače, ako Internet Explorer 8.
Toto v skutočnosti ovplyvňuje len vizuálne zobrazenie matematického obsahu. Pri práci s obsahom cez NVDA je možné použiť aj novšie prehliadače.

## Braille {#Braille}

Ak máte brailový riadok, NVDA môže informácie zobrazovať priamo na brailovom riadku.
Ak váš riadok podporuje písanie cez klávesnicu, môžete ho použiť na písanie textu v plnopise alebo skratkopise.
brailový výstup je možné zobraziť aj na obrazovke počítača použitím [Zobrazovača Braillu](#BrailleViewer). Zobrazovač braillu funguje v prípade, že používate brailový riadok, ale tiež bez brailového riadka.

Informácie o podporovaných riadkoch nájdete v časti [Podporované brailové zobrazovače](#SupportedBrailleDisplays).
Na tomto mieste tiež nájdete informácie o tom, ktoré riadky dokáže NVDA rozpoznať automaticky.
Všetky nastavenia týkajúce sa brailových riadkov a tabuliek nájdete v kategórii  [Braillovo písmo](#BrailleSettings) v [nastaveniach](#NVDASettings).

### Skratky pre prvky, oblasti stránky a typy stavov v brailovom zobrazení {#BrailleAbbreviations}

Aby sa na brailový riadok dostalo čo najviac informácií, pre prvky, oblasti stránky a stavy sa používajú tieto skratky.

| skratka |typ prvku|
|---|---|
|ap |aplikácia|
|čln |článok|
|cit |citácia|
|tlo |tlačidlo|
|tloko |Tlačidlo s kontextovou ponukou|
|vybtlo |výberové tlačidlo|
|krhtlo |kruhové tlačidlo|
|prtlo |prepínacie tlačidlo|
|pop |popis|
|ram |zoznamový rámik|
|zcp |začiarkávacie políčko|
|dok |dokument|
|dlg |dialóg|
|edt |editačné pole|
|hesedt |Heslové editačné pole|
|vnor |vnorený objekt|
|kpoz |koncová poznámka|
|obr |obrázok|
|cpoz |poznámka pod čiarou|
|gra |grafika|
|skp |zoskupenie|
|hN |nadpis úrovne, pričom N udáva úroveň, napríklad h1, h2|
|bbl |bublinková nápoveda|
|obl |oblasť stránky|
|odk |odkaz|
|nodk |navštívený odkaz|
|zoz |zoznam|
|mnu |menu|
|ppnk |panel ponúk|
|pontlo |tlačidlo ponuky|
|polmnu |položka menu|
|pnl |panel|
|priebeh |indikátor priebehu|
|znprzdn |Indikátor priebehu, Zaneprázdnené|
|prep |prepínač|
|pos |posúvač|
|sekc |sekcia|
|stav |stavový riadok|
|zozal |zoznam záložiek|
|tbl |tabuľka|
|sN |stĺpec v tabuľke, kde N je číslo stĺpca, napríklad s1, s2.|
|rN |riadok v tabuľke, kde N je číslo riadka, napríklad r1, r2.|
|term |terminál|
|panas |panel nástrojov|
|konap |kontextová nápoveda|
|sz |stromové zobrazenie|
|tlosz |tlačidlo stromového zobrazenia|
|polsz |položka stromového zobrazenia|
|úro N |položka v stromovom zobrazení, N udáva hierarchickú úroveň|
|okno |okno|
|⠤⠤⠤⠤⠤ |oddeľovač|
|ozn |označený obsah|

Skratkami sú tiež označené tieto stavy:

| skratka |stav prvku|
|---|---|
|... |zobrazuje sa, ak prvok podporuje automatické dopĺňanie|
|⢎⣿⡱ |Zobrazí sa, ak je objekt (napríklad prepínacie tlačidlo) stlačený|
|⢎⣀⡱ |Zobrazí sa, ak objekt (napríklad prepínacie tlačidlo) nie je stlačený|
|⣏⣿⣹ |Zobrazí sa, ak je objekt (napríklad začiarkávacie políčko)  začiarknutý|
|⣏⣸⣹ |zobrazí sa, ak je objekt (napríklad začiarkávacie políčko) čiastočne začiarknutý|
|⣏⣀⣹ |zobrazí sa,ak objekt (napríklad začiarkávacie políčko) nie je začiarknutý|
|- |Zobrazuje sa, ak sa dá objekt (napríklad vetva v stromovom zobrazení) zbaliť|
|+ |zobrazuje sa, ak sa dá objekt (napríklad vetva v stromovom zobrazení) rozbaliť|
|*** |Označuje chránený dokument alebo prvok|
|klik |zobrazuje sa, ak je objekt klikateľný|
|kmnt |Označuje komentár v dokumente alebo bunke tabuľky|
|vzor |Označuje vzorec v bunke tabuľky|
|nespr |Označuje nesprávne zadanú informáciu|
|popis |Označuje, že objekt (zvyčajne obrázok) obsahuje dlhý popis|
|vredt |Označuje viacriadkové editačné pole, najčastejšie vo webových dokumentoch|
|pov |Označuje povinné pole vo formulári|
|ln |Zobrazuje sa, ak je objekt (napríklad editačné pole) len na čítanie|
|vybr |zobrazuje sa, ak je objekt vybratý|
|nvybr |zobrazí sa,ak objekt nie je vybratý|
|vzost |Zobrazí sa, ak je objekt zobrazený vzostupne|
|zost |zobrazí sa,ak je objekt zobrazený zostupne|
|pmnu |zobrazuje sa, ak objekt obsahuje podmenu|

Pre oblasti stránky sa používajú tieto skratky:

| skratka |Oblasť stránky|
|---|---|
|bnnr |banner|
|obsah |Info o obsahu|
|dopln |doplnková|
|form |formulár|
|hlav |hlavná|
|navi |navigácia|
|hľad |vyhľadávanie|
|obl |oblasť|

### brailový zápis {#BrailleInput}

NVDA podporuje písanie textu cez klávesnicu brailového riadka v plnopise i skratkopise.
Prekladovú tabuľku, ktorá sa použije na preklad textu, môžete určiť v [Nastaveniach](#NVDASettings) v kategórii Braillovo písmo nastavením [Vstupnej tabuľky](#BrailleSettingsInputTable).

Keď píšete v plnopise, text sa vkladá okamžite.
Ak píšete v skratkopise, text sa preloží a vloží po stlačení medzeri alebo klávesu enter na konci slova.
Majte na pamäti, že pri preklade sa berie ohľad len na to, čo píšete a nie na to, čo ste už napísali a kde sa práve nachádza kurzor.
Ak napríklad používate tabuľku, ktorá vyžaduje začíanie čísel číslicovým znakom a klávesom backspace sa presuniete na koniec čísla, musíte znovu stlačiť číslicový znak, aby ste mohli pokračovať v písaní čísel.

<!-- KC:beginInclude -->
Bod 7 odstráni posledne zadaný znak alebo kombináciu bodov.
Bod 8 preloží zadaný text a stlačí kláves Enter.
Body 7+8: preloží zadaný text, ale nevloží medzeru ani nový riadok.
<!-- KC:endInclude -->

#### Zadávanie klávesových skratiek {#BrailleKeyboardShortcuts}

NVDA umožňuje zadávať klávesové skratky a emulovať rôzne kombinácie kláves priamo z brailového riadka.
Takáto emulácia je možná dvoma spôsobmi: Priradením konkrétnej skratky konkrétnemu tlačidlu, alebo použitím virtuálnych preraďovačov.

Najčastejšie klávesy, ako napríklad šípky, alebo kláves alt na vyvolanie panela ponúk, je možné priradiť priamo konkrétnym tlačidlám alebo kombináciám brailových bodov.
Mnohé ovládače brailových riadkov už majú predvolené takéto skratky.
Tieto skratky môžete meniť a pridávať [V dialógu klávesové skratky](#InputGestures).

Táto metóda veľmi dobre funguje napríklad pre klávesy Tab a podobne. Často ale nechcete definovať úplne všetky existujúce klávesové skratky.
Aby bolo možné emulovať klávesy, kde je potrebné súčasne stlačiť viacero kláves súčasne, NVDA umožňuje definovať skratky pre CTRL, alt, shift, windows, NVDA a prípadne priradiť kombinácie týchto kláves.
Ak chcete použiť takéto preraďovače, najprv stlačte príslušné tlačidlo (alebo kombináciu tlačidiel), ktoré sú priradené ku klávesom.
Potom stlačte písmeno, ktoré je súčasťou klávesovej skratky.
Napríklad: Ak chcete použiť skratku ctrl+f, použite tlačidlo, ktoré odošle do systému Ctrl a následne stlačte f, 
Ak chcete zadať ctrl+alt+t, použite buď samostatné tlačidlá pre stlačenie kláves ctrl a alt, v ľubovoľnom poradí, alebo jedno tlačidlo, ktoré automaticky stláča obe klávesy súčasne. Následne napíšte t.

Ak nechtiac odošlete do systému kláves a chcete odoslanie zrušiť, stlačte tlačidlo alebo kombináciu znovu.

Ak používate skratkopis, modifikačné klávesy sú prekladané ako použitie bodov 7+8.
Navyše, tieto skratky nezahŕňajú znaky zapísané pred použitím príkazu. 
Takže ak chcete stlačiť alt+2, pričom na zapísanie čísla 2 je potrebné použiť číslicový znak, najprv stlačte tlačidlo, ktorým do systému odošlete kláves alt, potom zapíšte číslicový znak a následne body 1 a 2.

## Zrak {#Vision}

NVDA je primárne určené pre zrakovo postihnutých používateľov, ktorí na prácu s počítačom využívajú hlasový výstup alebo brailový riadok. Dokáže však upravovať aj zobrazenie na obrazovke.
Takéto úpravy v NVDA označujeme ako vizuálne rozšírenie.

NVDA ponúka viacero vizuálnych rozšírení, ktoré sú popísané nižšie.
Ďalšie si môžete nainštalovať vo forme [doplnku](#AddonsManager).

Nastavenia vizuálnych rozšírení nájdete v [kategórii zrak](#VisionSettings) v dialógu [Nastavenia](#NVDASettings).

### Zvýraznenie na obrazovke {#VisionFocusHighlight}

Zvýraznenie na obrazovke vám uľahčí identifikovanie [systémového fokusu](#SystemFocus), [navigačného objektu](#ObjectNavigation) a pozíciu kurzora v [Režime prehliadania](#BrowseMode).
Objekty sú vyznačené farebným obdĺžnikom.

* Neprerušovaný modrý obdĺžnik charakterizuje súčasne navigačný objekt a systémový fokus (typicky v prípadoch, keď [navigačný objekt sleduje systémový fokus](#ReviewCursorFollowFocus)).
* Prerušovaný modrý obdĺžnik upozorňuje len na systémový fokus.
* Neprerušovaný ružový obdĺžnik upozorňuje na navigačný objekt.
* Neprerušovaný žltý obdĺžnik zvýrazňuje virtuálny kurzor, ktorý sa používa v režime prehliadania (Kde nie je fyzický kurzor, napríklad vo webových prehliadačoch).

Ak aktivujete zvýraznenie na obrazovke v [kategórii zrak](#VisionSettings) v dialógu [nastavenia](#NVDASettings), môžete nastaviť, či chcete [zvýrazňovať fokus, navigačný objekt alebo kurzor v režime prehliadania](#VisionSettingsFocusHighlight).

### Tienenie obrazovky {#VisionScreenCurtain}

Ak ste zrakovo postihnutí alebo úplne nevidiaci, často nechcete alebo jednoducho nemôžete pozerať na obrazovku.
Navyše sa nemôžete uistiť, že niekto nenazerá na obrazovku vášho počítača.
V týchto situáciách môžete použiť funkciu tienenia obrazovky. Toto spôsobí, že celá obrazovka bude úplne čierna.

Tienenie obrazovky môžete aktivovať v [kategórii zrak](#VisionSettings) v [Dialógu Nastavenia](#NVDASettings).

<!-- KC:beginInclude -->

| názov |klávesová skratka |popis|
|---|---|---|
|Zapína a vypína tienenie obrazovky |`NVDA+ctrl+escape` |Zapína a vypína tienenie obrazovky. Stlačené raz zapne tienenie do najbližšieho reštartu. Stlačené dvakrát zapne tienenie obrazovky natrvalo.|

<!-- KC:endInclude -->

Kým je tienenie obrazovky aktívne, nie je možné robiť činnosti priamo závislé na obsahu obrazovky ako [rozpoznávanie textu použitím OCR](#Win10Ocr) alebo zachytenie snímky obrazovky.

Keďže v najnovších verziách systému Windows došlo k úpravám v API na zväčšovanie, bolo potrebné v NVDA aktualizovať spôsob, akým sa zabezpečuje tienenie obrazovky.
Použite NVDA od verzie 2021.2 v kombinácii s Windows od verzie 10 21H2 (10.0.19044).
Z bezpečnostných dôvodov odporúčame, aby ste sa pri prvom použití tienenia obrazovky uistili vlastným zrakom, alebo prostredníctvom vidiacej osoby, či je obrazovka skutočne čierna.

Upozorňujeme, že ak je zapnuté zväčšenie obrazovky  a inverzia farieb, nie je možné aktivovať tienenie obrazovky.

## Optické rozpoznávanie textu Windows {#ContentRecognition}

Ak nie sú k dispozícii užitočné textové informácie, je možné použiť nástroje na optické  rozpoznávanie textu z obrázka.
NVDA dokáže rozpoznávať text z obrázka pomocou optického rozpoznávania (OCR) vstavaného v operačnom systéme Windows od verzie 10.
Ďalšie spôsoby rozpoznávania textu môžu byť integrované pomocou doplnkov.

Ak vyvoláte rozpoznanie textu, NVDA bude analyzovať aktuálny [navigačný objekt](#ObjectNavigation).
Predvolene navigačný objekt sleduje systémový kurzor alebo kurzor v režime prehliadania, takže vo väčšine prípadov stačí presunúť kurzor na požadované miesto.
Ak napríklad presuniete kurzor na obrázok, bude rozpoznaný text z obrázka.
Ak chcete cez OCR rozpoznať celé okno aplikácie, budete musieť použiť objektovú navigáciu.

Keď je rozpoznávanie dokončené, text sa zobrazí v režime prehliadania a môžete ho čítať šípkami.
objekt pod kurzorom môžete aktivovať (zvyčajne kliknúť naň) medzerou alebo klávesom enter.
Klávesom ESC zatvoríte okno s rozpoznaným textom.

### Rozpoznávanie textu Windows {#Win10Ocr}

priamo v systéme windows od verzie 10 je k dispozícii optické rozpoznávanie textu pre mnohé jazyky, vrátane Slovenčiny.
NVDA môže pomocou OCR rozpoznať text v obrázku alebo v neprístupnom okne aplikácie.

jazyk rozpoznávania nastavíte v kategórii  [Rozpoznávanie textu Windows](#Win10OcrSettings) v [Nastaveniach](#NVDASettings).
Doplnkové jazyky pre rozpoznávanie (Napríklad Češtinu) nainštalujete z menu štart > nastavenia > čas a jazyk > miestne a jazykové nastavenia > Pridanie jazyka.

Ak chcete pravidelne sledovať zmeny v aktuálnom okne, napríklad ak sledujete video s titulkami, môžete zapnúť možnosť pravidelne obnovovať rozpoznaný text.
Toto je možné zapnúť v časti [Rozpoznávanie textu Windows](#Win10OcrSettings) v [Nastaveniach NVDA](#NVDASettings).

OCR systému Windows od verzie 10 môže byť čiastočne alebo úplne nefunkčné  v kombinácii s [vizuálnymi rozšíreniami NVDA](#Vision) alebo inými externými vizuálnymi pomôckami. Pred spustením optického rozpoznávania by ste mali obmedziť použitie takýchto pomôcok.

<!-- KC:beginInclude -->
rozpoznanie textu v aktuálnom navigačnom objekte vyvoláte skratkou NVDA+R.
<!-- KC:endInclude -->

## Vylepšenia pre aplikácie {#ApplicationSpecificFeatures}

NVDA pre niektoré aplikácie implementuje svoje vlastné príkazy, čím buď umožňuje ľahšie vykonávať niektoré úlohy, alebo sprístupňuje časti aplikácií, ktoré nie sú inak prístupné používateľom odkázaným na čítač obrazovky.

### Microsoft Word {#MicrosoftWord}
#### Automatické  čítanie hlavičiek stĺpcov a riadkov {#WordAutomaticColumnAndRowHeaderReading}

NVDA vám môže automaticky oznamovať  hlavičky riadkov a stĺpcov pri čítaní tabuliek v programe MS Word.
Je potrebné mať začiarknuté "Oznamovať hlavičky riadkov / stĺpcov tabuľky" v kategórii  čítanie textu v [Nastaveniach](#NVDASettings).

Ak na prístup k dokumentom MS Word používate [UIA](#MSWordUIA), (predvolene je toto zapnuté), budú bunky prvého riadka použité ako hlavičky stĺpcov. Rovnako, bunky prvého stĺpca budú použité ako hlavičky riadka.

Ak [UIA](#MSWordUIA) nepoužívate, je potrebné určiť hlavičky ručne.
Keď sa nastavíte na prvý riadok alebo stĺpec a chcete ho nastaviť ako hlavičku, použite tieto príkazy:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |popis|
|---|---|---|
|Nastaviť hlavičky stĺpcov |NVDA+shift+c |Ak stlačíte raz, NVDA bude vybratý stĺpec a nasledujúce stĺpce považovať za hlavičku tabuľky a bude ich oznamovať pri pohybe v nasledujúcich riadkoch. Nastavenie zrušíte dvojitým stlačením.|
|Nastaviť hlavičky riadkov |NVDA+shift+r |Ak stlačíte raz, NVDA bude vybratý stĺpec  a stĺpce   pod ním považovať za hlavičku tabuľky a bude ich oznamovať pri pohybe v stĺpcoch medzi riadkami. Nastavenie zrušíte dvojitým stlačením.|

<!-- KC:endInclude -->
Tieto nastavenia sa natrvalo uložia do dokumentu tak, aby im porozumeli aj iné čítače obrazovky (napríklad JAWS).
Ak  neskôr dokument otvorí používateľ, ktorý používa iný čítač obrazovky, bude mať už správne nastavené hlavičky v tabuľkách.

#### Režim prehliadania v programe Microsoft Word {#BrowseModeInMicrosoftWord}

Podobne ako na internete, aj v programe MS Word môžete aktivovať režim prehliadania. V režime prehliadania potom funguje rýchla navigácia a zoznam prvkov.
<!-- KC:beginInclude -->
Režim prehliadania v programe Microsoft Word zapnete a vypnete skratkou NVDA+medzera.
<!-- KC:endInclude -->
Viac informácií nájdete v kapitole  [Režim prehliadania](#BrowseMode).

##### Zoznam prvkov {#WordElementsList}

<!-- KC:beginInclude -->
Ak máte aktívny režim prehliadania v programe Microsoft Word, zoznam prvkov vyvoláte skratkou NVDA+F7.
<!-- KC:endInclude -->
V zozname prvkov môžete prezerať nadpisy, odkazy, komentáre a revízie dokumentu a tiež  chyby (v súčasnosti len pravopisné).

#### Čítanie komentárov {#WordReportingComments}

<!-- KC:beginInclude -->
Ak si chcete prečítať komentár, na ktorom je systémový fokus, stlačte NVDA+alt+c.
<!-- KC:endInclude -->
Všetky komentáre spolu s revíziami si môžete prezerať aj v zozname prvkov, ak vyberiete ako prvok komentáre a zmeny.

### Microsoft Excel {#MicrosoftExcel}
#### Automatické  čítanie hlavičiek stĺpcov a riadkov {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA vám môže automaticky oznamovať  hlavičky riadkov a stĺpcov pri čítaní  tabuliek v programe MS Excel.
Najprv Musíte mať začiarknuté "Oznamovať hlavičky riadkov / stĺpcov tabuľky" v [Nastaveniach](#NVDASettings) v kategórii čítanie textu.
Následne musíte určiť, ktorý riadok alebo stĺpec má NVDA považovať za hlavičku.
Keď sa nastavíte na prvý riadok alebo stĺpec a chcete ho nastaviť ako hlavičku, použite tieto príkazy:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Nastaviť hlavičky stĺpcov |NVDA+shift+c |Ak stlačíte raz, NVDA bude vybratý stĺpec a nasledujúce stĺpce považovať za hlavičku tabuľky a bude ich oznamovať pri pohybe v nasledujúcich riadkoch. Nastavenie zrušíte dvojitým stlačením.|
|Nastaviť hlavičky riadkov |NVDA+shift+r |Ak stlačíte raz, NVDA bude vybratý stĺpec a stĺpce pod ním považovať za hlavičku tabuľky a bude ich oznamovať pri pohybe v stĺpcoch medzi riadkami. Nastavenie zrušíte dvojitým stlačením.|

<!-- KC:endInclude -->
Tieto nastavenia sa natrvalo uložia do dokumentu tak, aby im porozumeli aj iné čítače obrazovky (napríklad JAWS).
Ak  neskôr dokument otvorí používateľ, ktorý používa iný čítač obrazovky, bude mať už správne nastavené hlavičky v tabuľkách.

#### Zoznam prvkov {#ExcelElementsList}

Podobne ako na internete, aj v programe MS Excel môžete používať zoznam prvkov a takto sa dostať k viacerým informáciám.
<!-- KC:beginInclude -->
Zoznam prvkov v programe MS Excel vyvoláte skratkou NVDA+F7.
<!-- KC:endInclude -->
V zozname prvkov si môžete zobraziť tieto časti dokumentu:

* Grafy: Zobrazuje všetky grafy v aktívnom hárku.
Keď vyberiete graf, stlačíte na ňom enter, alebo aktivujete tlačidlo "prejsť na", fokus sa presunie na požadovaný graf. V grafe sa potom pohybujte šípkami.
* Komentáre: Zobrazí všetky bunky v aktívnom hárku, ktoré obsahujú komentár.
NVDA pre každú bunku prečíta jej súradnice a text komentára.
Ak stlačíte enter, alebo aktivujete tlačidlo prejsť na, fokus sa presunie na vybratú bunku.
* Vzorce: Zobrazí všetky bunky v aktívnom hárku, ktoré obsahujú vzorec.
NVDA pre každú bunku prečíta jej súradnice a vzorec.
Ak stlačíte enter, alebo aktivujete tlačidlo prejsť na, fokus sa presunie na vybratú bunku.
* Hárky: Zobrazí zoznam hárkov v dokumente.
Klávesom F2 môžete premenovať vybratý hárok.
Klávesom enter, alebo  aktivovaním tlačidla "prejsť na" sa presuniete na požadovaný hárok.
* Formuláre: Zobrazí všetky formuláre vo vybratom hárku.
pre každý prvok formulára sa zobrazuje alternatívny text a tiež súradnice bunky, v ktorej sa formulárové pole nachádza.
Do požadovaného poľa sa presuniete klávesom enter, alebo aktivovaním tlačidla "prejsť na".

#### Čítanie poznámok {#ExcelReportingComments}

<!-- KC:beginInclude -->
Ak si chcete prečítať poznámky  pre aktuálnu bunku, stlačte NVDA+alt+c.
V aplikáciách Microsoft Office 2016, 365 a novších boli komentáre nahradené poznámkami.
<!-- KC:endInclude -->
Všetky poznámky   v aktuálnom hárku si môžete prezerať aj v zozname prvkov po stlačení nvda+F7.

NVDA dokáže zobraziť vlastný dialóg na pridanie alebo úpravu poznámky.
Štandardné okno na prácu s poznámkami  v MS Excely nie je prístupné. Preto NVDA používa vlastný dialóg, ale používa klávesovú skratku, ktorú poskytuje MS Excel. Preto skratka funguje aj vtedy, ak NVDA nie je spustené.
<!-- KC:beginInclude -->
Na pridanie poznámky, alebo úpravu existujúcej  poznámky pre aktuálnu bunku, stlačte shift+f2.
<!-- KC:endInclude -->

Túto skratku nie je možné zmeniť.

Upozorňujeme, že okno na prácu s poznámkami  je možné vyvolať aj z kontextovej ponuky pre bunku v MS Excely.
Toto však otvorí predvolený neprístupný dialóg, ktorý sa štandardne používa v MS Excely.

V Microsoft Office 2016, 365 a novších, bol pridaný aj nový spôsob komentovania.
Tento spôsob je prístupnejší a umožňuje napríklad odpovedať na komentáre.
Možnosť nájdete v kontextovej ponuke bunky.
Takto pridané komentáre ale nie sú zviazané s poznámkami.

#### Čítanie chránených buniek {#ExcelReadingProtectedCells}

Ak je dokument programu MS Excel chránený, môžete mať problém prečítať niektoré bunky, ktoré sú chránené proti úpravám.
<!-- KC:beginInclude -->
Ak si chcete prezerať aj chránené bunky, najprv aktivujte režim prehliadania skratkou NVDA+medzera. Následne použite na prezeranie tabuľky štandardné príkazy (napríklad šípky).
<!-- KC:endInclude -->

#### Formuláre {#ExcelFormFields}

V zošite programu MS Excel sa môžu nachádzať formuláre.
dostanete sa k nim cez zoznam prvkov, alebo skratkami rýchlej navigácie f a shift+f.
Aj v tomto prípade aktivujete režim fokusu medzerou alebo klávesom enter. V tomto režime môžete napríklad vyplniť editačné pole.
pre viac informácii o práci v režime prehliadania a o skratkách rýchlej navigácie pozrite časť [Režim prehliadania](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |popis|
|---|---|---|
|Zobraziť alebo skryť poznámky |ctrl+shift+s |keď máte spustenú prezentáciu, tento príkaz prepína medzi poznámkami pre aktuálnu snímku a obsahom aktuálnej snímky. Skratka má vplyv len na to, čo NVDA číta a nie na samotné zobrazenie snímky na obrazovke.|

<!-- KC:endInclude -->

### Foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Oznámiť zostávajúci čas |ctrl+shift+r |V prípade, že je práve prehrávaná skladba, oznámi zostávajúci čas.|
|Oznámiť uplinulý čas |ctrl+shift+e |Oznámi koľko zo skladby bolo prehraté, ak je spustené prehrávanie.|
|Oznámiť dĺžku skladby |ctrl+shift+t |Oznámi dĺžku prehrávanie skladby, ak je spustené prehrávanie.|

<!-- KC:endInclude -->

Všimnite si: tieto skratky fungujú len ak máte vo Foobare nastavené predvolené zobrazenie stavového riadka.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Oznámiť poslednú správu |NVDA+ctrl+1-4 |Oznámi jednu z posledných správ. napr. NVDA+ctrl+2 oznámi predposlednú správu.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA ponúka nasledujúce funkcie pre program Poedit od verzie 3.4.

<!-- KC:beginInclude -->

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Oznámiť poznámku pre prekladateľov |`ctrl+shift+a` |Oznámi poznámku pre prekladateľov. Stlačené dvakrát zobrazí poznámku v režime prehliadania|
|Oznámiť komentár |`ctrl+shift+c` |Oznámi komentár. Stlačené dvakrát zobrazí komentár v režime prehliadania|
|Oznámiť pôvodný zdrojový text |`ctrl+shift+o` |Oznámi pôvodný zdrojový text. Stlačené dvakrát za sebou zobrazí text v režime prehliadania|
|Oznámiť varovanie |`ctrl+shift+w` |Oznámi dostupné varovania. Stlačené dvakrát za sebou zobrazí varovanie v režime prehliadania|

<!-- KC:endInclude -->

### Kindle pre PC {#Kindle}

NVDA podporuje čítanie a prácu s knihami v aplikácii amazon Kindle pre PC.
Funkcia je však dostupná len pre knihy, ktoré majú atribút "Screen Reader: Supported". Toto si môžete overiť v detailoch konkrétnej knihy.

Knihy sú zobrazované v režime prehliadania.
Režim prehliadania sa automaticky aktivuje po otvorení knihy, alebo po zobrazení textu knihy.
Nová strana sa načíta vždy, keď sa pri čítaní dostanete na koniec aktuálnej strany, aj v prípade ak knihu čítate šípkami alebo plynulým čítaním.
<!-- KC:beginInclude -->
ručne môžete prejsť na nasledujúcu stranu klávesom page up. Na predchádzajúcu stranu sa vrátite klávesom page down.
<!-- KC:endInclude -->

na prechod medzi odkazmi a obrázkami môžete použiť skratky rýchlej navigácie. Tieto však fungujú len v rámci aktuálnej strany.
Skratka na prechod medzi odkazmi prechádza aj medzi poznámkami pod čiarou.

NVDA poskytuje základnú podporu pre čítanie matematiky a navigáciu v matematickom obsahu.
Podrobnosti nájdete v časti [Čítanie matematického obsahu](#ReadingMath).

#### Výber textu {#KindleTextSelection}

Kindle umožňuje vykonávať rôzne operácie s práve vybratým textom. Môžete si vyhľadať definíciu v slovníku, pridať poznámku alebo zvýraznenie, skopírovať text do schránky alebo ho vyhľadať na internete.
najprv vyberte text pomocou shiftu v kombinácii so šípkami.
<!-- KC:beginInclude -->
Keď vyberiete text, zobrazte si možnosti stlačením klávesy aplikácie alebo skratky Shift+F10.
<!-- KC:endInclude -->
Ak nevyberiete žiadny text, zobrazia sa možnosti pre slovo pod kurzorom.

#### Používateľské poznámky {#KindleUserNotes}

K slovu alebo k pasáži v texte môžete pridať poznámku.
Aby ste mohli pridať poznámku, označte text a otvorte kontextové menu spôsobom opísaným vyššie.
V menu vyberte položku pridať poznámku.

Pri čítaní NVDA oznamuje tieto poznámky ako komentáre.

Poznámku upravíte alebo zmažete nasledujúcim spôsobom:

1. Presuňte kurzor na miesto, kde sa nachádza poznámka.
1. Otvorte kontextové menu.
1. Vyberte položku upraviť poznámku.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
V tabuľke s knihami:

| Názov |Klávesová skratka |Popis|
|---|---|---|
|otvoriť |enter |otvorí vybratú knihu.|
|kontextová ponuka |kláves aplikácie (kontextové menu) |Otvorí kontextové menu pre vybratú knihu.|

<!-- KC:endInclude -->

### Konzola Windows {#WinConsole}

NVDA poskytuje podporu pre konzolu, ktorá sa používa v príkazovom riadku, PowerShell, a Windows Subsystéme pre Linux.
Okno konzoly má pevne stanovenú veľkosť a zvyčajne sa doň nevmestí celý výstup.
Keď sa v okne objaví nový text, staršie záznamy nie sú viditeľné.
Vo verziách Windows pred verziou 11 22H2, Takto skrytý text nie je možné čítať prezeracím kurzorom NVDA.
Preto je potrebné posúvať okno konzoly, aby ste si mohli prečítať staršie výstupi.
V nových verziách systému Windows je možné prezerať buffer Windows konzoly a terminálu bez nutnosti skrolovať výstup.
<!-- KC:beginInclude -->
Nasledujúce vstavané klávesové skratky  môžu byť užitočné pri [čítaní textu](#ReviewingText) v starších typoch Windows konzoly:

| Názov |Klávesová skratka |Popis|
|---|---|---|
|Posunúť hore |CTRL+šípka hore |Posunie okno konzoly vyššie, takže je možné čítať staršie záznamy.|
|Posunúť dole |CTRL+šípka dole |posunie okno konzoly nižšie, takže je možné čítať novšie záznamy.|
|Posunúť na začiatok |CTRL+Home |Posunie okno konzoly na začiatok celého výstupu.|
|Posunúť na koniec |CTRL+end |Posunie okno konzoly na koniec celého výstupu.|

<!-- KC:endInclude -->

## Konfigurácia NVDA {#ConfiguringNVDA}

Väčšinu nastavení NVDA je možné nájsť  v dialógových oknách z podmenu Možnosti v ponuke NVDA.
Mnohé nastavenia sú v multystránkovom dialógu [Nastavení](#NVDASettings).
Vo všetkých dialógoch nastavení môžete akceptovať vykonané zmeny stlačením tlačidla OK.
Ak chcete zahodiť vykonané zmeny, môžete stlačiť tlačidlo Zrušiť, alebo kláves esc.
V niektorých dialógoch môžete nastavenia okamžite uložiť bez nutnosti zatvárať dialóg aktivovaním tlačidla použiť.
Vo väčšine dialógov je dostupná kontextová pomoc.
<!-- KC:beginInclude -->
Po stlačení `f1` sa otvorí používateľská príručka na príslušnom mieste.
<!-- KC:endInclude -->
Na prepínanie niektorých volieb existujú tiež globálne klávesové skratky, ktoré sú zobrazované pri popise jednotlivých nastavení v texte nižšie.

### Nastavenia {#NVDASettings}

<!-- KC:settingsSection: || názov | klávesová skratka pre desktop | klávesová skratka pre laptop | popis | -->
Mnoho nastavení NVDA nájdete v dialógu nastavenia.
Aby bolo možné rýchlo vyhľadať požadované nastavenie, nastavenia sú usporiadané do kategórií.
Po vybratí príslušnej kategórie sa zobrazia len nastavenia vo zvolenej kategórii.
V zozname kategórií na pohyb použite šípku hore a šípku dole. Na prechod ku konkrétnym nastaveniam potom použite `tab` a `shift+tab`.
V dialógu nastavení je možné kedykoľvek prepínať kategórie skratkami `ctrl+tab` dopredu a `ctrl+shift+tab` v opačnom smere.

Nastavenia môžete uložiť aktivovaním tlačidla použiť. V tomto prípade ostane dialóg otvorený a vy môžete meniť ďalšie nastavenia a to aj v iných kategóriách.
Ak chcete uložiť nastavenia a súčasne zatvoriť dialóg nastavení, aktivujte tlačidlo OK.

Niektoré kategórie nastavení majú aj vlastnú klávesovú skratku.
Po stlačení tejto skratky sa automaticky otvorí dialóg nastavení a kurzor bude presunutý na požadovanú kategóriu.
Predvolene nemajú klávesovú skratku všetky kategórie.
Ak chcete vytvoriť skratku pre kategórie, ktoré často používate, použite dialóg [Klávesové skratky](#InputGestures), kde môžete nastaviť novú klávesovú skratku alebo dotykové gesto.

Kategórie nastavení sú popísané na nasledujúcich riadkoch.

#### Všeobecné {#GeneralSettings}

<!-- KC:setting -->

##### Otvoriť všeobecné nastavenia {#OpenGeneralSettings}

Klávesová skratka: `NVDA+ctrl+g`

Tu môžete nastaviť základné správanie NVDA, vrátane jazyka rozhrania NVDA a tiež kontroly aktualizácii.
Kategória Obsahuje tieto nastavenia:

##### Jazyk {#GeneralSettingsLanguage}

Je to zoznam, kde je možné vybrať jazyk, ktorý NVDA bude používať a v ňom zobrazovať všetky hlásenia.
Nachádza sa tu mnoho jazykov a poslednou položkou zoznamu je Jazyk systému.
Táto posledná voľba hovorí NVDA, aby používal jazyk, v ktorom sú zobrazované dialógy Windows.

Aby sa prejavili zmeny, je potrebné reštartovať NVDA.
Môžete si vybrať, či chcete reštartovať teraz, alebo neskôr. V oboch prípadoch je potrebné, aby bolo povolené ukladanie nastavení pri ukončení NVDA (buď ručne, alebo automaticky).

##### Uložiť nastavenia pri ukončení {#GeneralSettingsSaveConfig}

Začiarkavacie políčko, ktoré ak začiarknete, bude NVDA pri ukončení automaticky ukladať svoje nastavenia.

##### Pri ukončení NVDA zobraziť dialóg s možnosťami {#GeneralSettingsShowExitOptions}

Toto začiarkávacie pole určuje, či sa pri ukončení NVDA zobrazí dialóg, v ktorom môžete vybrať akciu.
Ak je začiarknuté, pri ukončení NVDA sa zobrazí dialóg, v ktorom môžete vybrať, či chcete NVDA ukončiť, reštartovať,  reštartovať a zakázať doplnky, alebo reštartovať a nainštalovať čakajúce aktualizácie.
Ak toto pole nie je začiarknuté, NVDA sa ukončí okamžite.

##### prehrať zvuk pri spustení a ukončení NVDA {#GeneralSettingsPlaySounds}

Začiarkávacie pole. Ak začiarknete, NVDA pri spustení  a pred ukončením prehrá zvuk.

##### Úroveň záznamu {#GeneralSettingsLogLevel}

Zoznamový rámik, ktorý umožňuje používateľovi zvoliť, aké množstvo dát má NVDA  zaznamenať počas svojho vlastného behu.
Všeobecne sa používateľ týmto nastavením nemusí zaoberať.
Ak chcete tvorcom programu poskytnúť informácie o chybových hláseniach, je dobré nastaviť túto voľbu na vyššiu úroveň. Takisto môžete zaznamenávanie úplne vypnúť.

Dostupné sú tieto možnosti:

* Zakázaný: NVDA zaznamená len krátku správu pri štarte.
* Info: NVDA zaznamená správu pri štarte a základné informácie pre vývojárov.
* Upozornenie: Zaznamená len menej závažné chyby.
* Vstup a výstup: Zaznamená vstup z klávesnice a brailového riadka a tiež to, čo NVDA zobrazuje a hovorí.
Ak sa obávate o vaše súkromie, nepoužívajte túto úroveň záznamu.
* Debug: Zaznamenáva závažné aj menej závažné chyby a tiež vstup a výstup.
Opäť, ak sa obávate o vaše súkromie, nepoužívajte túto úroveň záznamu.

##### Spustiť NVDA po prihlásení {#GeneralSettingsStartAfterLogOn}

Ak je táto voľba začiarknutá, NVDA sa spustí hneď po prihlásení do systému.
Táto voľba je dostupná len po nainštalovaní NVDA a nemôže byť použitá pri spustenej prenosnej verzii.

##### Spúšťať NVDA pri zobrazení prihlasovacej obrazovky (vyžaduje administrátorské práva) {#GeneralSettingsStartOnLogOnScreen}

Ak sa do Windows prihlasujete zadaním vášho prihlasovacieho mena a hesla, zaškrtnutím tejto voľby zaistíte, aby sa NVDA spustil už pri zobrazení práve spomínanej obrazovky.
Táto voľba je dostupná len po nainštalovaní NVDA a nemôže byť použitá pri spustenej prenosnej verzii.

##### použiť aktuálne nastavenia NVDA na prihlasovacej a zabezpečených obrazovkách (vyžaduje administrátorské práva) {#GeneralSettingsCopySettings}

Po stlačení tohto tlačidla NVDA skopíruje aktuálne nastavenia do systémového priečinka, aby mohli byť tieto nastavenia použité v prípade, ak je NVDA spustený na prihlasovacej obrazovke alebo [iných zabezpečených obrazovkách](#SecureScreens).
Ak sa chcete uistiť, že budú správne prekopírované všetky nastavenia, môžete uložiť nastavenia stlačením Ctrl+NVDA+c, alebo použitím voľby z ponuky NVDA.
Táto voľba je dostupná len po nainštalovaní NVDA a nemôže byť použitá pri spustenej prenosnej verzii.

##### Kontrolovať dostupnosť novej verzie NVDA {#GeneralSettingsCheckForUpdates}

Ak je začiarknuté, NVDA bude automaticky kontrolovať dostupnosť novej verzie a ak novú verziu nájde, upozorní vás na to.
Aktualizácie môžete skontrolovať ručne aktivovaním položky skontrolovať aktualizácie v menu pomocník v ponuke NVDA.
Ak požiadate o stiahnutie aktualizácie, NVDA z vášho počítača odosiela na náš server niektoré údaje.
Aby bolo možné poskytnúť aktualizáciu, zisťujeme:

* Aktuálnu verziu NVDA, ktorú používate
* Aktuálnu verziu vášho operačného systému
* Či používate 32 alebo 64 bitovú verziu

##### Povoliť zasielanie štatistických údajov do NV Access {#GeneralSettingsGatherUsageStats}

Ak začiarknete túto možnosť, NV Access využije tieto informácie na zisťovanie, koľko ľudí používa NVDA, z akých krajín pochádzajú. Informácie sú zasielané vždy pri kontrole dostupnosti novej verzie.
Na zisťovanie krajiny, v ktorej sa nachádzate, využívame IP adresu. Vašu IP adresu si však ďalej neukladáme.
Okrem nevyhnutných údajov na získanie aktualizácie tiež po začiarknutí tohto políčka budeme odosielať tieto informácie:

* Aktuálny jazyk NVDA
* Či používate portable alebo nainštalovanú verziu NVDA
* Aký hlasový výstup používate (vrátane názvu doplnku z ktorého je nainštalovaný ovládač)
* Aký brailový riadok používate (vrátane názvu doplnku z ktorého je nainštalovaný ovládač)
* Akú brailovú tabuľku používate (ak využívate brailový výstup)

Tieto údaje nám umožnia určiť ďalšie priority pri vývoji NVDA.

##### Upozorniť na čakajúcu aktualizáciu po štarte {#GeneralSettingsNotifyPendingUpdates}

Ak je začiarknuté, NVDA po štarte upozorní, že máte stiahnuté aktualizácie a ponúkne možnosť inštalácie.
Aktualizáciu môžete ručne nainštalovať z dialógu Ukončiť NVDA (ak ho máte aktívny), z menu NVDA alebo z pomocníka v menu NVDA.

#### Reč {#SpeechSettings}

<!-- KC:setting -->

##### Otvoriť nastavenia reči {#OpenSpeechSettings}

Klávesová skratka: `NVDA+ctrl+v`

táto kategória obsahuje nastavenia na  zmenu hlasového výstupu a úpravu reči konkrétneho hlasového výstupu.
Pre rýchlejšiu alternatívu, ktorá umožňuje meniť parametre hlasu odkiaľkoľvek zo systému si prosím pozrite časť [Kruh nastavení hlasového výstupu](#SynthSettingsRing).

Táto kategória obsahuje tieto nastavenia:

##### Zmeniť hlasový výstup {#SpeechSettingsChange}

V tejto kategórii je ako prvé tlačidlo Zmeniť... Po aktivovaní tohto tlačidla sa otvorí nové okno [Hlasový výstup](#SelectSynthesizer), v ktorom môžete vybrať hlasový výstup a výstupné zariadenie.
Toto okno sa otvorí nad oknom s nastaveniami.
Potvrdenie alebo zatvorenie tohto dialógu vás preto vráti späť do okna s nastaveniami.

##### Hlas {#SpeechSettingsVoice}

Ide o zoznam obsahujúci všetky dostupné hlasy aktuálneho hlasového výstupu.
Za pomoci šípok môžete tento zoznam prehliadať a vypočuť si všetky hlasy.
Hornou a ľavou šípkou sa presuniete na predchádzajúci hlas, dolnou a pravou šípkou sa môžete presunúť na nasledujúci hlas.

##### Variant {#SpeechSettingsVariant}

Ak používate hlasový výstup eSpeak NG, toto je zoznamový rámik, ktorý nastavuje variant hlasu.
Varianty hlasu výstupu eSpeak NG môžeme chápať takmer ako ďalšie hlasy, pretože dodávajú hlasu úplne iné vlastnosti.
Niektoré varianty budú znieť ako mužský, iné ako ženský hlas a niektoré dokonca úplne inak.
Táto možnosť je tiež dostupná aj pre niektoré hlasové výstupy tretích strán a v takom prípade budete môcť upraviť variant hlasu aj pri nich.

##### Tempo {#SpeechSettingsRate}

Je to posuvník od nula po sto, ktorým nastavíte rýchlosť reči.
Nula znamená najpomalšie tempo reči a sto najrýchlejšie.

##### Zdvojnásobiť tempo {#SpeechSettingsRateBoost}

Začiarknutím tejto možnosti docielite značné zrýchlenie reči. Túto funkciu podporujú len niektoré hlasové výstupi.

##### Výška {#SpeechSettingsPitch}

Posuvník, ktorým nastavíte výšku od nula po sto.
Nula je najnižší tón a sto najvyšší tón reči.

##### Hlasitosť {#SpeechSettingsVolume}

Posuvník, ktorým v rozmedzí od nula po sto nastavíte hlasitosť hlasu od najtichšieho po najhlasnejší.

##### Intonácia {#SpeechSettingsInflection}

Posuvník, ktorého hodnota hovorí hlasovému výstupu do akej miery má byť intonácia uplatnená smerom na hor i smerom na dol. V súčasnosti intonáciu podporuje len hlasový výstup eSpeak NG.

##### Automaticky prepínať jazyk {#SpeechSettingsLanguageSwitching}

Ak je začiarknuté, NVDA bude automaticky počas čítania meniť jazyk. Jazyk určí podľa jazykových značiek v texte.
Predvolene je toto začiarknuté.

##### Automaticky prepínať dialekt {#SpeechSettingsDialectSwitching}

Ak je začiarknuté automaticky prepínať jazyk, toto umožňuje zmeny aj dialektu jazyka hlasového výstupu.
Napríklad ak budete anglickým hlasom čítať  v jazyku Angličtina - spojené štáty a NVDA narazí na značku pre zmenu dialektu  na  Angličtina - Veľká Británia, hlasový výstup sa prepne na správny dialekt.
Predvolene toto nie je začiarknuté.

<!-- KC:setting -->

##### Úroveň interpunkcie {#SpeechSettingsSymbolLevel}

Klávesová skratka: NVDA+p

Môžete nastaviť, či má NVDA slovne  oznamovať interpunkčné znamienka a symboly.
Ak je toto napríklad nastavené na všetko, všetky symboly budú vyslovované ako slová.
Nastavenie interpunkcie ovplyvňuje prejav NVDA pre všetky hlasové výstupy.

##### pri spracovaní textu sa riadiť jazykom hlasového výstupu {#SpeechSettingsTrust}

táto možnosť je predvolene začiarknutá a hovorí NVDA, že pri spracovaní textu sa má riadiť jazykom konkrétneho hlasu.
Ak vám NVDA pri použití konkrétneho hlasu alebo hlasového výstupu nesprávne číta interpunkciu, odčiarknite túto možnosť, aby boli uprednostnené globálne nastavenia NVDA.

##### Na spracovanie špeciálnych znakov a emoji použiť databázu Unicode Konzorcia {#SpeechSettingsCLDR}

Ak začiarknete túto možnosť, NVDA bude na spracovanie symbolov využívať dodatočné slovníky.
Tieto slovníky obsahujú popisy pre interpunkciu a emotikony od [Unicode Konzorcia](https://www.unicode.org/consortium/), ktoré sú súčasťou [Spoločnej jazykovej databázy](https://cldr.unicode.org/).
Ak chcete, aby NVDA pri spracovaní špeciálnych symbolov používalo tento slovník, začiarknite túto možnosť.
Ak používate hlasový výstup, ktorý už podporuje popisovanie emotikonov, mali by ste tieto dodatočné slovníky vypnúť.

Nezabudnite, že ak upravíte výslovnosť špeciálnych symbolov, úpravy sa uložia do vašich nastavení NVDA.
Ak upravíte popis pre konkrétny emotikon, tento popis bude použitý aj v prípade, ak je zapnutá podpora pre slovníky Unicode konzorcia.
Výslovnosť špeciálnych symbolov môžete upravovať v dialógu [Výslovnosť interpunkčných a špeciálnych symbolov](#SymbolPronunciation).

Ak chcete kdekoľvek zapínať a vypínať použitie dát z Unicode konzorcia, nastavte si klávesovú skratku v dialógu [Klávesové skratky](#InputGestures).

##### Zmeniť výšku hlasu pri čítaní veľkých písmen v percentách {#SpeechSettingsCapPitchChange}

Do tohto editačného poľa je možné napísať hodnotu v percentách, ako sa zmení výška hlasu pri čítaní veľkých písmen.
Záporné čísla znižujú a kladné čísla zvyšujú výšku hlasu.
Ak si neželáte pri vyslovovaní veľkých písmen meniť výšku hlasu vložte do tohto poľa číslo 0.
NVDA môže zvyšovať výšku hlasu pri veľkých písmenách, ale nie všetky hlasové výstupy túto funkcionalitu  podporujú.
Ak oznamovanie veľkých písmen zvýšeným hlasom nefunguje správne, zvážte použitie funkcii [Vysloviť "veľké" pred prečítaním veľkého písmena](#SpeechSettingsSayCapBefore) alebo tiež  [ Pípať pred hláskovaním veľkých písmen](#SpeechSettingsBeepForCaps).

##### Vysloviť "veľké" pred prečítaním veľkého písmena {#SpeechSettingsSayCapBefore}

Začiarkávacie políčko, ktoré nastaví NVDA tak, aby čítal slovo "veľké" vždy pred veľkým písmenom pri čítaní po znakoch.

##### Pípať pred hláskovaním veľkých písmen {#SpeechSettingsBeepForCaps}

Ak je toto začiarkavacie políčko začiarknuté, NVDA krátko zapípa vždy, keď sa pri hláskovaní objaví veľké písmeno.

##### Hláskovanie riadi hlasový výstup (ak je podporované) {#SpeechSettingsUseSpelling}

Existujú slová pozostávajúce len z jediného znaku. Výslovnosť tohto znaku sa líši od kontextu, napr. pri vyslovovaní jediného znaku sa obyčajne znak hláskuje a pri čítaní slova sa len prečíta.
V slovenčine je príkladom takéhoto znaku písmeno k, ktoré znie ako "k" ak je použité ako predložka, ale "ká" ak je hláskované samostatne.
Táto možnosť umožňuje na základe použitého hlasového výstupu rozlišovať medzi týmito dvoma možnosťami, ak to hlasový výstup podporuje.
Väčšina hlasových výstupov to podporuje.

Odporúča sa nechať túto možnosť zapnutú.
Žiaľ niektoré hlasové výstupy Microsoft Speech API toto nastavenie nepodporujú a môžu sa správať zvláštne, ak je to začiarknuté.
Ak pozorujete problémy s vyslovovaním jednotlivých znakov, skúste túto voľbu odčiarknuť.

##### Foneticky hláskovať pri čítaní po znakoch {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Vypnuté, zapnuté|
|predvolene |vypnuté|

Ak je táto možnosť zapnutá, bude NVDA vyslovovať aj fonetické popisky pre znaky, ktoré prečítate pod kurzorom.

Ak napríklad prejdete šípkou doprava na písmeno B, NVDA po sekunde povie Božena.
Toto môže byť užitočné, ak nedokážete správne rozpoznať znaky, alebo ak horšie počujete.

Fonetické hláskovanie je prerušené v prípade, že NVDA vyslovuje iný text, alebo stlačíte kláves `ctrl`.

##### Dostupné režimi reči {#SpeechModesDisabling}

V tomto zozname je možné začiarknuť [režimi](#SpeechModes), ktoré majú byť dostupné pri prepínaní pomocou skratky `NVDA+S`.
Odčiarknuté režimi nebudú dostupné.
Predvolene sú začiarknuté a zapnuté všetky režimi.

Ak napríklad nepoužívate režim "pípanie" a "bez reči", môžete ich odčiarknuť a nechať začiarknuté možnosti "reč" a "na vyžiadanie".
Upozorňujeme, že je potrebné mať aktívne minimálne dva režimi.

#### Nastavenie hlasového výstupu {#SelectSynthesizer}

<!-- KC:setting -->

##### Otvoriť nastavenia hlasového výstupu {#OpenSelectSynthesizer}

Klávesová skratka: `NVDA+ctrl+s`

Toto okno sa otvorí, ak v kategórii reč aktivujete tlačidlo zmeniť. Tu môžete následne nastaviť hlasový výstup a zvukovú kartu, ktorú chcete používať.
Ak ste vybrali požadovaný hlasový výstup, stlačte tlačidlo OK a NVDA začne tento výstup automaticky používať.
Ak pri načítaní hlasového výstupu dôjde k chybe, NVDA na to upozorní a vráti sa k používaniu aktuálneho hlasového výstuupu.

##### Hlasový výstup {#SelectSynthesizerSynthesizer}

Tu môžete nastaviť hlasový výstup, ktorý chcete používať.

Zoznam podporovaných hlasových výstupov získate v časti [Podporované hlasové výstupy](#SupportedSpeechSynths).

V tomto zozname vždy nájdete aj jednu špeciálnu položku bez reči, čo umožní prevádzku NVDA úplne bez hlasového výstupu.
Toto môže byť užitočné pre niekoho, kto chce používať NVDA len s brailovým výstupom alebo to môže byť užitočné vidiacim vývojárom, ktorí plánujú používať zobrazovač reči.

#### Kruh nastavení hlasového výstupu {#SynthSettingsRing}

Ak chcete zmeniť niektoré vlastnosti reči bez nutnosti otvárať dialóg nastavenia hlasu, môžete použiť niektoré z klávesových skratiek dostupných kdekoľvek počas behu NVDA.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|ďalšie nastavenie hlasového výstupu |NVDA+ctrl+pravá šípka |NVDA+ctrl+shift+pravá šípka |Prejde na nasledujúce dostupné nastavenie hlasového výstupu. Z posledného nastavenia NVDA automaticky prejde na prvé.|
|Predchádzajúce nastavenie hlasového výstupu |NVDA+ctrl+ľavá šípka |NVDA+ctrl+shift+ľavá šípka |Prejde na predchádzajúce dostupné nastavenie hlasového výstupu. Z prvého NVDA automaticky prejde na posledné nastavenie.|
|Zvýšiť hodnotu nastavenia hlasového výstupu |NVDA+ctrl+šípka hore |NVDA+ctrl+shift+šípka hore |Zvýši hodnotu aktuálne zameraného nastavenia hlasového výstupu. Napríklad zrýchli tempo, vyberie nasledujúci hlas, zosilní hlasitosť|
| Zvýšiť hodnotu nastavenia hlasového výstupu po väčších krokoch | `NVDA+ctrl+pageUp` | `NVDA+shift+ctrl+pageUp` | Zvyšuje hodnotu nastavenia, na ktorom sa nachádzate. Napríklad pri nastavení hlasu prejde o dvadsať hlasov dopredu, pri nastavení posuvníkov prejde o dvadsať percent vyššie. |
|Znížiť hodnotu nastavenia hlasu |NVDA+ctrl+šípka dolu |NVDA+ctrl+shift+šípka dolu |Zníži hodnotu aktuálne zameraného nastavenia hlasového výstupu. Napríklad spomalí tempo, vyberie predchádzajúci hlas, stíši hlasitosť.|
| znížiť  hodnotu nastavenia hlasového výstupu po väčších krokoch | `NVDA+ctrl+pageDown` | `NVDA+shift+ctrl+pageDown` | Znižuje  hodnotu nastavenia, na ktorom sa nachádzate. Napríklad pri nastavení hlasu prejde o dvadsať hlasov späť, pri nastavení posuvníkov prejde o dvadsať percent nižšie. |

<!-- KC:endInclude -->

#### Brailovo písmo {#BrailleSettings}

Táto kategória obsahuje nastavenia ohľadom brailových riadkov, brailového vstupu a výstupu.
Nájdete tu nasledujúce možnosti:

##### Nastavenia brailového riadka {#BrailleSettingsChange}

Po aktivovaní tlačidla zmeniť... sa otvorí dialóg s [možnosťou výberu brailového riadka](#SelectBrailleDisplay), kde môžete nastaviť požadované zariadenie.
Toto okno sa otvorí nad oknom s nastaveniami.
Ak toto okno potvrdíte alebo zatvoríte, vrátite sa späť do okna s nastaveniami.

##### Výstupná prekladová tabuľka {#BrailleSettingsOutputTable}

Ďalšou voľbou v tejto kategórii je výstupná prekladová tabuľka.
Tu nájdete tabuľky pre rôzne jazyky a kodifikácie braillovho písma.
Vybratá tabuľka sa použije na správne zobrazenie textu na brailovom zobrazovači.
Medzi tabuľkami sa môžete pohybovať šípkami.

##### Vstupná prekladová tabuľka {#BrailleSettingsInputTable}

Podobne ako v prvom prípade, aj tu môžete vybrať prekladovú tabuľku.
Táto však bude použitá na správne interpretovanie znakov, ktoré zadávate na brailovom zobrazovači.
Konkrétnu tabuľku vyberte šípkami.

Zdôrazňujeme, že táto možnosť je užitočná len ak váš riadok má brailovú klávesnicu a ak je táto funkcia podporovaná ovládačom príslušného riadku.
Ak má brailový riadok klávesnicu, ale zadávanie textu nie je podporované, upozorňujeme na to v časti [Podporované brailové zobrazovače](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Režim brailu {#BrailleMode}

Klávesová skratka: `NVDA+alt+t`

Umožňuje prepínať medzi dostupnými režimami brailu.

V súčasnosti sú dostupné dva režimi, "Sleduje kurzor" a "sleduje reč".

Ak zvolíte možnosť "sleduje kurzor", potom bude brailový riadok sledovať zameranie alebo textový kurzor, alebo navigačný objekt a prezerací kurzor, v závislosti od toho, s čím je brailový riadok zviazaný.

Ak zvolíte možnosť "Sleduje reč", potom NVDA zobrazuje to, čo hovorí hlasový výstup, resp. čo by hovoril hlasový výstup,ak by bol režim reči nastavený na reč.

##### Slovo, kde sa nachádza kurzor zobraziť počítačovým braillom {#BrailleSettingsExpandToComputerBraille}

Toto začiarkavacie políčko umožní zobrazovať aktuálne slovo v počítačovom braillovom písme, čo v mnohých jazykoch zodpovedá plnopisu. Je to užitočné, ak nechceme aplikovať pravidlá skratkopisu tabuľky vybratej v poli Prekladová tabuľka.

##### Zobraziť kurzor {#BrailleSettingsShowCursor}

Tu môžete určiť, či chcete alebo nechcete zobrazovať brailový kurzor.
toto sa týka systémového kurzora a tiež prezeracieho kurzora. Toto nastavenie neovplyvňuje zobrazenie vybratého textu.

##### Blikajúci kurzor {#BrailleSettingsBlinkCursor}

Umožňuje aktivovať blikajúci kurzor na brailovom riadku.
Ak nezačiarknete túto možnosť, kurzor bude stále zobrazený.
Táto možnosť neovplyvňuje zobrazenie vybratého textu. Označenie sa zobrazuje ako body 7+8 bez blikania.

##### Rýchlosť blikania kurzora (ms) {#BrailleSettingsBlinkRate}

Ide o číselnú hodnotu, ktorá určuje frekvenciu blikania kurzora brailového zobrazovača v milisekundách.

##### Tvar kurzora fokusu {#BrailleSettingsCursorShapeForFocus}

toto nastavenie určuje tvar kurzora (teda kombináciu bodov), ktoré sa zobrazujú, ak je brailový kurzor zviazaný so systémovým kurzorom.
Neovplyvňuje však zobrazenie vybratého textu.

##### Tvar prezeracieho  kurzora {#BrailleSettingsCursorShapeForReview}

toto nastavenie určuje tvar kurzora (teda kombináciu bodov), ktoré sa zobrazujú, ak je brailový kurzor zviazaný s prezeracím kurzorom.
Neovplyvňuje však zobrazenie vybratého textu.

##### Zobrazovať správy {#BrailleSettingsShowMessages}

V tomto zozname môžete určiť, či sa hlásenia na brailovom riadku budú zobrazovať stále, alebo zmiznú po zadanom čase.

Ak chcete toto nastavenie meniť odkiaľkoľvek, je potrebné nastaviť skratku v [dialógu klávesové skratky](#InputGestures).

##### Zobrazovať správy (sek) {#BrailleSettingsMessageTimeout}

Táto numerická hodnota určuje ako dlho majú na riadku byť zobrazované správy NVDA.
Správy NVDA sú automaticky odstránené pri použití smerových tlačidiel na riadku. Opätovne sa zobrazia po stlačení príslušnej klávesovej skratky.
Táto možnosť je dostupná len v prípade, že ste v predošlom zoznamovom rámiku vybrali možnosť "po určenú dobu".

<!-- KC:setting -->

##### brailový kurzor zviazaný s {#BrailleTether}

Klávesová skratka: NVDA+ctrl+t

Táto voľba umožňuje nastaviť, či bude brailový kurzor sledovať systémový a textový kurzor, alebo či bude brailový kurzor sledovať navigačný objekt a prezerací kurzor, alebo oboje.
Ak nastavíte možnosť "automaticky", NVDA bude sledovať textový a systémový kurzor.
Ak sa v tomto prípade presuniete na iný objekt, alebo pohnete prezeracím kurzorom, NVDA zviaže brailový kurzor s prezeracím kurzorom až do momentu, keď sa zmení fokus.
Ak chcete sledovať len textový kurzor a zamerané objekty, nastavte možnosť na fokus.
V tomto prípade NVDA nebude sledovať navigačný objekt a prezerací kurzor.
Ak chcete na brailovom riadku sledovať objektovú navigáciu a prezerací kurzor, nastavte možnosť Na prezerací kurzor.
V tomto prípade nebude brailový riadok sledovať systémový a textový kurzor.

##### Smerové tlačidlá posúvajú systémový aj prezerací kurzor {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Predvolené |Nikdy|
|Možnosti |Predvolené (nikdy), nikdy, Len ak je zviazaný automaticky, vždy|

Toto nastavenie určuje, či sa systémový kurzor posúva pri použití smerových tlačidiel na brailovom riadku.
Predvolene je toto nastavenie nastavené na nikdy, takže pri stláčaní smerových tlačidiel sa systémový kurzor neposúva.

Ak je táto možnosť nastavená na vždy, a súčasne je [Brailový kurzor zviazaný s](#BrailleTether) nastavený na automaticky, alebo na prezerací kurzor, stlačenie smerových tlačidiel presunie aj systémový kurzor, alebo zameranie, ak je to možné.
Ak je aktuálny režim prezerania [prezeranie obrazovky](#ScreenReview), fyzicky systémový kurzor neexistuje.
V tomto prípade sa NVDA pokúsi premiestniť fokus na objekt, na ktorého texte ste použili smerové tlačidlá.
To isté platí aj pre režim [prezerania objektov](#ObjectReview).

Môžete tiež túto možnosť nastaviť tak, aby sa kurzor posúval len v prípade, že k zviazaniu došlo automaticky.
V tomto prípade budú smerové tlačidlá posúvať systémový kurzor len vtedy, ak došlo automaticky k zviazaniu systémového a prezeracieho kurzora.

Táto možnosť je dostupná len vtedy, ak je možnosť "[Brailový kurzor zviazaný](#BrailleTether)" nastavená na "Automaticky" alebo "na prezerací kurzor".

Ak chcete toto nastavenie meniť kedykoľvek, priraďte klávesové skratku v [dialógu klávesové skratky](#InputGestures).

##### Čítať po odsekoch {#BrailleSettingsReadByParagraph}

Ak je to začiarknuté, text v brailly bude zobrazený po odsekoch namiesto predvoleného zobrazenia po riadkoch.
Tiež príkazy na prechod na nasledujúci alebo predchádzajúci riadok v brailly budú posúvať po odsekoch.
Znamená to, že nie je nutné posúvať riadok na konci každého riadku, aj ak sa tam vojde väčšie množstvo textu.
Toto umožní plynulé čítanie väčšieho množstva textu.
Predvolene je to odčiarknuté.

##### zabrániť deleniu slov keď je to možné {#BrailleSettingsWordWrap}

Ak je začiarknuté, slovo, ktoré je dlhé a nezmestí sa na riadok, nebude rozdelené.
Namiesto toho ostane na konci riadka voľné miesto.
Celé slovo bude presunuté na nasledujúci riadok.
toto sa zvykne označovať ako "zalamovanie textu".
Ak je však slovo také dlhé, že sa samo o sebe nezmestí na riadok, bude aj v takomto prípade rozdelené.

Ak túto možnosť odčiarknete, zobrazí sa na konci riadka kúsok slova, ktorý sa ešte na riadok vojde.
Zvyšok slova bude až na ďalšom riadku.

Začiarknutím tejto možnosti docielite plynulejšie čítanie, na druhej strane budete musieť riadok posúvať častejšie.

##### prezentácia kontextu {#BrailleSettingsFocusContextPresentation}

toto nastavenie určuje, aké kontextové informácie sa zobrazia na riadku pri objekte, ktorý má fokus.
Kontextové informácie môžu informovať o hierarchii objektov.
Ak napríklad presuniete fokus na položku v zozname, táto položka je súčasťou zoznamu.
Tento zoznam sa nachádza v nejakom dialógu a tak ďalej.
Hierarchia objektov je podrobne vysvetlená v časti [Objektová navigácia](#ObjectNavigation).

Ak nastavíte možnosť "len zmeny", NVDA bude zobrazovať informácie o kontexte aktuálneho objektu, ale len ak dôjde ku zmene kontextu.
Ak v našom príklade prejdete na položku v zozname, na riadku sa zobrazí informácia o tom, že ide o položku.
Ak na riadku ostane ešte voľné miesto, NVDA zobrazí aj informáciu o tom, že položka je súčasťou zoznamu.
Ak sa začnete v zozname pohybovať šípkami, NVDA predpokladá, že viete, že sa nachádzate v zozname.
Preto túto informáciu viac nezobrazí a na riadku nájdete len meno aktuálnej položky.
ak si chcete prečítať kontextovú informáciu znovu, musíte zobrazenie na riadku posunúť späť.

ak nastavíte možnosť "vždy zobraziť", NVDA bude zobrazovať všetky kontextové informácie aj v prípade, že už boli zobrazené.
Výhodou je, že na riadku takto uvidíte vždy čo najviac kontextových informácií.
Nevýhodou však môže byť, že na riadku bude vždy rozdiel  v tom, kde sa  začína fokus.
pri tomto nastavení je ťažké napríklad rýchlo prechádzať dlhý zoznam položiek, lebo musíte vždy prstom hľadať kde sa nová položka začína.
Toto bolo predvolené nastavenie do verzie NVDA 2017.2.

Poslednou možnosťou je nastavenie "len pri návrate späť". V tomto prípade sa nebudú zobrazovať žiadne kontextové informácie.
V našom príklade sa teda dozviete len to, že ste napoložke v zozname.
ak si chcete prečítať celú kontextovú informáciu (že ste v zozname a tento je súčasťou dialógu), musíte posunúť zobrazenie na riadku späť.

Ak chcete toto nastavenie meniť kedykoľvek z klávesnice, môžete si k nemu priradiť klávesovú skratku v dialógu [Klávesové skratky](#InputGestures).

##### Prerušiť reč počas posúvania {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Predvolene |zapnuté|
|Možnosti |Predvolené (zapnuté), zapnuté, vypnuté|

Toto nastavenie určuje, či má byť reč prerušená, ak posuniete brailový riadok vpred alebo späť.
Príkazy, ktoré prechádzajú na predchádzajúci alebo nasledujúci riadok, vždy prerušia tok reči.

Súčasné čítanie textu a počúvanie iného textu môže byť rušivé.
Z tohto dôvodu je predvolene zapnuté prerušenie reči v prípade posúvania riadka.

Ak túto možnosť vypnete, je možné počúvať hlas a čítať text zároveň.

##### Ukázať výber {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Predvolené |Povolené|
|Možnosti |Predvolené (povolené), povolené, zakázané|

Určuje, či bude výber vyznačený na brailovom riadku bodmi 7 a 8.
Predvolene je toto zapnuté a výber sa ukazuje.
Ukazovanie výberu ale môže byť rušivé pri čítaní.
Vypnutie tejto možnosti môže zlepšiť a zrýchliť čitateľnosť textu.

Ak chcete nastavenie meniť odkiaľkoľvek, vytvorte klávesovú skratku v [dialógu klávesové skratky](#InputGestures).

#### Nastavenie brailového riadka {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Otvoriť nastavenia brailového riadka {#OpenSelectBrailleDisplay}

Klávesová skratka: `NVDA+ctrl+a`

Tento dialóg môžete otvoriť v nastaveniach NVDA v kategórii Braille stlačením tlačidla zmeniť... Tu následne môžete nastaviť brailový riadok, ktorý chcete používať.
Ak si vyberiete požadovaný riadok, zatvorte dialóg tlačidlom OK a NVDa automaticky začne tento riadok používať.
Ak pri načítaní riadka nastane chyba, NVDA vás na to upozorní a vráti sa k predchádzajúcemu nastaveniu.

##### brailový riadok {#SelectBrailleDisplayDisplay}

V zozname budú vždy zobrazené možnosti podľa toho, aké ovládače brailových zariadení máte nainštalované v systéme.
Medzi jednotlivými voľbami je možné sa pohybovať použitím kurzorových klávesov.

Ak vyberiete možnosť "automaticky", NVDA bude sledovať pripájanie riadkov na pozadí.
To znamená, že ak cez USB alebo Bluetooth pripojíte brailový riadok, NVDA ho automaticky začne používať.

Žiadny zobrazovač Znamená, že nepoužívate výstup v braillovom písme.

Prosím, prečítajte si tiež [Podporované brailové zobrazovače](#SupportedBrailleDisplays) pre získanie viac informácií o podporovaných zariadeniach a o tom, ktoré dokáže NVDA rozpoznať automaticky.

##### Brailové riadky na automatickú detekciu {#SelectBrailleDisplayAutoDetect}

Ak ste v predošlom nastavení zvolili automatickú detekciu brailového riadka, bude dostupný aj tento zoznam. Pomocou začiarkávacích polí môžete určiť brailové riadky, ktoré bude NVDA kontrolovať pri automatickej detekcii.
Toto vám umožní vylúčiť riadky, ktoré často nepoužívate.
Ak napríklad používate riadok od spoločnosti Baum, môžete ponechať aktívnu detekciu len pre riadky Baum a ostatné zakázať.

Predvolene sú všetky ovládače, ktoré umožňujú automatickú detekciu riadka, povolené.
Ďalšie ovládače pridané pri aktualizácii NVDA alebo pomocou doplnkov budú tiež automaticky detegované.

V časti [Podporované brailové riadky](#SupportedBrailleDisplays) vždy uvádzame, či konkrétny riadok podporuje automatickú detekciu.

##### Port {#SelectBrailleDisplayPort}

Táto možnosť, ak je dostupná, určuje, aký port sa použije pri komunikácii s vybratým brailovým zobrazovačom.
V zozname si môžete vybrať jednu z možností pre váš brailový zobrazovač.

NVDA predvolene automaticky určí, cez aký port bude komunikovať s vybratým zariadením. Znamená to, že skontroluje všetky pripojené Bluetooth a USB zariadenia.
Pre niektoré brailové riadky však môžete samy určiť port.
Najčastejšie možnosti sú "automaticky" (kedy NVDA samo určuje typ pripojenia), "USB", "Bluetooth" a označenia sériových portov, ak brailový riadok podporuje komunikáciu cez sériový port.

Táto možnosť nie je dostupná, ak zvolený riadok podporuje len automatický výber komunikačného portu.

Pre podrobnejšie informácie si pozrite časť [Podporované brailové zobrazovače](#SupportedBrailleDisplays).

Upozorňujeme, že ak súčasne pripojíte dva riadky od rovnakého výrobcu, ktoré používajú rovnaký ovládač (napríklad dva riadky od výrobcu Seika),
NVDA nedokáže rozpoznať, ktorý riadok chcete používať.
Preto odporúčame vždy pripájať len jeden brailový riadok výrobcu.

#### Zvuk {#AudioSettings}

<!-- KC:setting -->

##### Otvoriť nastavenia zvuku {#OpenAudioSettings}

Klávesová skratka: `NVDA+ctrl+u`

Táto kategória obsahuje nastavenia, ktorými môžete ovplyvniť zvuky a výstupné zvukové zariadenie pre NVDA.

##### Výstupné zariadenie {#SelectSynthesizerOutputDevice}

Toto nastavenie umožňuje vybrať zvukovú kartu, cez ktorú bude rozprávať hlasový výstup.

<!-- KC:setting -->

##### Režim automatického stíšenia zvuku {#SelectSynthesizerDuckingMode}

Klávesová skratka: `NVDA+Shift+D`

Môžete určiť, či má NVDA stišovať zvuk ostatných aplikácií, keď rozpráva, alebo konštantne stíšiť zvuk z aplikácií, keď NVDA spustíte.

* Nestíšiť: NVDA nebude stišovať zvuk z ostatných aplikácií.
* Stíšiť, keď NVDA hovorí a prehráva zvuky: NVDA bude stišovať zvuk z ostatných programov len vtedy, keď bude čítať alebo oznamovať udalosti zvukom. Toto ale nemusí fungovať pre všetky syntézy reči.
* Vždy stíšiť: NVDA stíši všetky zvuky ostatných programov po štarte   až do ukončenia NVDA.

Táto možnosť je dostupná, len ak je NVDA nainštalované.
Nemôžete ju využiť, ak NVDA beží v portable režime alebo z dočasnej kópie.

##### Hlasitosť zvukov je rovnaká ako hlasitosť reči {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|predvolené |vypnuté|
|Možnosti |vypnuté, zapnuté|

Ak je táto možnosť zapnutá, hlasitosť zvukov sa prispôsobí hlasitosti reči.
Ak znížite hlasitosť reči, zníži sa hlasitosť zvukov.
Rovnako ak zvýšite hlasitosť reči, zvýši sa hlasitosť zvukov.
Táto možnosť nie je dostupná, ak ste v pokročilých nastaveniach zakázali použitie [WASAPI](#WASAPI).

##### Hlasitosť zvukov NVDA {#SoundVolume}

Tento posuvník umožňuje nastaviť hlasitosť pípania a ostatných zvukov NVDA.
Toto nastavenie má vplyv na správanie NVDA len v prípade, že je vypnuté "hlasitosť zvukov je rovnaká ako hlasitosť reči".
Táto možnosť nie je dostupná, ak ste v pokročilých nastaveniach zakázali použitie [WASAPI](#WASAPI).

##### Oddelenie zvuku {#SelectSoundSplitMode}

Oddelenie zvuku využíva samostatne ľavý a pravý kanál slúchadiel a reproduktorov.
Môžete nastaviť, že zvuk NVDA budete počuť v jednom kanály (napríklad vľavo) a zvuky aplikácií v druhom kanály (napríklad vpravo).
Predvolene je táto funkcia vypnutá.
Režimi oddelenia zvukov je možné prepínať skratkou.
<!-- KC:beginInclude -->

| Názov | Klávesová skratka | popis |
|---|---|---|
| Prepnúť režim oddelenia zvuku | `NVDA+alt+s` | Prepína medzi dostupnými režimami oddelenia zvuku. |

<!-- KC:endInclude -->

Predvolene skratka prepína medzi týmito režimami:

* Vypnuté: NVDA nijako neovplyvňuje spracovanie zvuku.
* NVDA v ľavo a zvuky v pravo: NVDA bude rozprávať v ľavom kanály a zvuky ostatných aplikácií budú v pravom kanály.
* NVDA v ľavo  a zvuky v strede: NVDA bude rozprávať v ľavom kanály a všetky ostatné zvuky budete počuť v oboch kanáloch.

Ďalšie možnosti sa dajú nastaviť priamo v nastaveniach NVDA.
Je tiež možné zvoliť možnosť "NVDA a zvuky v oboch kanáloch".
Táto možnosť môže priniesť iné výsledky v porovnaní s úplne vypnutým oddelením zvukov, ak iné spracovanie zvuku ovplyvňuje hlasitosť kanálov.

Upozorňujeme, že pri rozdelení zvukov od hlasového výstupu nedochádza k zmiešaniu kanálov.
Ak teda aplikácia prehráva stereo zvuk a súčasne ste nastavili, že NVDA bude v ľavo a zvuky v pravo, budete počuť len pravý kanál zo zvuku aplikácie.

Funkcia nie jedostupná, ak ste NVDA spustili a bolo vypnuté [použitie WASAPI](#WASAPI) v pokročilých nastaveniach.

Upozorňujeme, že ak dôjde k pádu NVDA, aplikácie môžu aj naďalej prehrávať zvuk len v jednom kanály.
Pre správne fungovanie a nápravu situácie je potrebné reštartovať NVDA a tiež nastaviť možnosť NVDA a zvuky v oboch kanáloch.

##### Úprava dostupných režimov rozdelenia zvuku {#CustomizeSoundSplitModes}

V tomto zozname môžete začiarknuť režimi rozdelenia zvuku, ktoré majú byť dostupné pri prepínaní skratkou `NVDA+alt+s`.
Režimi, ktoré odčiarknete, nebudú dostupné.
Predvolene sú povolené len tri režimi:

* Oddelenie zvukov vypnuté.
* NVDA v ľavo a zvuky v pravo.
* NVDA v ľavo a zvuky v oboch kanáloch.

Upozorňujeme, že je potrebné začiarknuť minimálne jeden režim.
Funkcia nie jedostupná, ak ste NVDA spustili a bolo vypnuté [použitie WASAPI](#WASAPI) v pokročilých nastaveniach.

##### Nechať zvukové zariadenie prebudené po skončení reči {#AudioAwakeTime}

Toto pole určuje, ako dlho nechá NVDA zariadenie prebudené po skončení reči.
Toto zabraňuje odsekávaniu začiatkov alebo koncov slov a fráz.
Toto odsekávanie je spôsobené, ak zvukové zariadenie (najčastejšie Bluetooth alebo bezdrôtové súpravy) prejdú do režimu spánku.
Táto funkcia je tiež užitočná, ak NVDA beží vo rirtuálnom systéme (napríklad Citrix Virtual Desktop), a na niektorých notebookoch.

Nízke hodnoty môžu spôsobovať odsekávanie začiatkov a koncov slov, keďže zariadenie priskoro prechádza do režimu spánku.
Vysoké hodnoty zas môžu spôsobovať rýchle vybíjanie zariadenia, keďže je dlho aktívne aj v prípade, že sa neprehráva zvuk.

Ak chcete funkciu vypnúť, nastavte hodnotu 0.

#### Zrak {#VisionSettings}

V kategórii Zrak môžete zapínať, vypínať a upravovať jednotlivé [vizuálne rozšírenia](#Vision).

Upozorňujeme, že dostupné možnosti môžete rozšíriť pomocou [doplnkov](#AddonsManager).
Predvolene sú dostupné tieto možnosti:

##### Zvýraznenie na obrazovke {#VisionSettingsFocusHighlight}

Začiarkávacie polia v tejto skupine nastavujú správanie [zvýraznenia na obrazovke](#VisionFocusHighlight).

* Povoliť zvýraznenie: Zapína a vypína zvýraznenie fokusu.
* Zvýrazniť systémový fokus: Určuje, či bude na obrazovke zvýraznený [systémový fokus](#SystemFocus).
* Zvýrazniť navigačný objekt: určuje, či bude na obrazovke zvýraznený [navigačný objekt](#ObjectNavigation).
* Zvýrazniť kurzor v režime prehliadania: Určuje, či sa na obrazovke zvýrazní pozícia [kurzora v režime prehliadania](#BrowseMode).

Upozorňujeme, že začiarknutie a odčiarknutie políčka "Povoliť zvýraznenie fokusu" má vplyv aj na nasledujúce tri začiarkávacie polia.
Preto ak začiarknete políčko "Povoliť zvýraznenie fokusu", začiarknú sa aj tri možnosti spomenuté vyššie.
Ak chcete sledovať pomocou zvýraznenia len fokus a zvyšné polia odčiarknete, potom bude pole "povoliť zvýraznenie fokusu" čiastočne začiarknuté.

##### Tienenie obrazovky {#VisionSettingsScreenCurtain}

Tu môžete zapnúť [tienenie obrazovky](#VisionScreenCurtain) začiarknutím políčka "Aktivovať tienenie obrazovky (okamžitý efekt)".
Pred zatienením obrazovky sa zobrazí varovanie.
Pred tým, než budete pokračovať, aktivujte reč alebo braill, aby ste mohli aj naďalej ovládať počítač.
Tlačidlom Nie sa vrátite späť bez aktivovania tienenia.
Tlačidlom áno povolíte tienenie obrazovky.
Ak si neželáte zobrazovať toto varovanie, môžete začiarknuť príslušné políčko vo varovnom dialógu.
Zobrazovanie varovania môžete kedykoľvek obnoviť, ak začiarknete políčko "Varovať pred spustením tienenia obrazovky".

Predvolene NVDA oznamuje zapnutie a vypnutie tienenia obrazovky zvukom.
Ak to chcete zmeniť, odčiarknite možnosť "prehrať zvuk pri prepínaní funkcie tienenie obrazovky".

##### Nastavenia pre vizuálne rozšírenia tretích strán {#VisionSettingsThirdPartyVisualAids}

Ďalšie vizuálne rozšírenia môžete nainštalovať do NVDA pomocou [doplnkov](#AddonsManager).
Ak tieto rozšírenia majú konfigurovateľné nastavenia, zobrazia sa v príslušných skupinách v tejto kategórii.
Podrobnosti nájdete v príslušnom návode k danému doplnku.

#### Klávesnica {#KeyboardSettings}

<!-- KC:setting -->

##### Otvoriť nastavenia klávesnice {#OpenKeyboardSettings}

Klávesová skratka: `NVDA+ctrl+k`

V tejto kategórii môžete nastaviť, ako sa NVDA správa pri písaní a používaní klávesových skratiek.
Obsahuje nasledujúce voľby:

##### Rozloženie klávesnice {#KeyboardSettingsLayout}

Tento zoznamový rámik nám umožňuje vybrať, aký typ klávesnice chceme používať. Či pôjde o verziu pre desktop/stolné PC, alebo laptop/pre prenosné počítače/notebooky.

##### Vybrať kláves NVDA {#KeyboardSettingsModifiers}

Začiarkávacie políčka v tomto zozname určujú, ktoré klávesy sa budú používať ako [kláves NVDA](#TheNVDAModifierKey). Dostupné sú tieto možnosti:

* kláves Capslock
* Numerický insert
* Insert (zvyčajne sa nachádza pod šípkami, vedľa klávesov home a end)

Ak nevyberiete žiadny kláves ako kláves NVDA, je ťažké vykonávať väčšinu príkazov NVDA, preto je potrebné vybrať aspoň jeden.

<!-- KC:setting -->

##### Čítať napísané znaky {#KeyboardSettingsSpeakTypedCharacters}

Klávesová skratka: NVDA+2

Ak je zapnuté, NVDA bude oznamovať všetky napísané znaky.

<!-- KC:setting -->

##### Čítať po slovách {#KeyboardSettingsSpeakTypedWords}

Klávesová skratka: NVDA+3

Ak je zapnuté, NVDA bude čítať pri písaní text po slovách.

##### prerušiť reč pri písaní {#KeyboardSettingsSpeechInteruptForCharacters}

Ak je zapnuté, NVDA prestane hovoriť hneď, ako začnete písať. Predvolene je táto možnosť začiarknutá.

##### Prerušiť reč klávesom Enter {#KeyboardSettingsSpeechInteruptForEnter}

Ak je začiarknuté, NVDA prestane hovoriť hneď, ako stlačíte kláves enter. Táto voľba je predvolene zapnutá.

##### Povoliť rýchlu navigáciu počas plynulého čítania {#KeyboardSettingsSkimReading}

Ak je začiarknuté, niektoré príkazy neprerušia plynulé čítanie, ale len presunú kurzor a plynulé čítanie bude pokračovať od daného miesta. Takýmito príkazmi sú napríklad rýchla navigácia v režime prehliadania a pohyb po riadkoch a odsekoch.

##### Pípať pri písaní malých písmen ak je zapnutý capslock {#KeyboardSettingsBeepLowercase}

Ak je to zapnuté, pri písaní so zapnutým capslockom budete počuť upozornenie v podobe krátkeho pípnutia, ak je pridržaný aj kláves shift.
Všeobecne sa písanie s preraďovačom pri zapnutom capslocku nepoužíva a vo väčšine prípadov to znamená, že Ste si neuvedomili, že je kláves capslock zapnutý.
Je teda vhodné byť na túto skutočnosť upozornený.

<!-- KC:setting -->

##### Čítať príkazové skratky {#KeyboardSettingsSpeakCommandKeys}

Klávesová skratka: NVDA+4

Ak je zapnuté, NVDA bude čítať klávesové skratky použité ako príkazy, teda nie samotné znaky. Do tejto funkcie spadajú kombinácie znakov a klávesov napr. s klávesom ctrl.

##### oznamovať počas písania zvukom pravopisné chyby {#KeyboardSettingsAlertForSpellingErrors}

ak začiarknete túto možnosť, NVDA vás zvukom upozorní, ak pri písaní urobíte pravopisnú chybu.
táto možnosť je dostupná len vtedy, ak si začiarknete oznamovanie pravopisných chýb v nastaveniach, v kategórii [čítanie textu](#DocumentFormattingSettings)

##### Spracovať vstup z externých programov {#KeyboardSettingsHandleKeys}

Táto možnosť určuje, či bude NVDA spracúvať vstupy z aplikácií, akými sú klávesnica na obrazovke, alebo program prevodu reči na text.
predvolene je možnosť začiarknutá. Niektorí používatelia ju môžu chcieť vypnúť, aby nedochádzalo k nesprávnemu zápisu znakov vo vietnamčine, napríklad cez program UniKey.

#### Myš {#MouseSettings}

<!-- KC:setting -->

##### Otvoriť nastavenia myšy {#OpenMouseSettings}

Klávesová skratka: `NVDA+ctrl+m`

Tu môžete nastaviť sledovanie kurzora myši, oznamovanie polohy myši a ďalšie užitočné funkcie.
Kategória  obsahuje nasledujúce prvky:

##### Oznamovať zmeny tvaru kurzora myši {#MouseSettingsShape}

Začiarkávacie políčko ktoré ak začiarknete, NVDA bude oznamovať zmenu tvaru kurzora myši vždy, keď sa tvar kurzora zmení.
Zmena tvaru kurzora myši vo Windows signalizuje napríklad také informácie, ako je načítavanie, či editovateľnosť nejakého poľa.

<!-- KC:setting -->

##### Povoliť sledovanie kurzora myši {#MouseSettingsTracking}

Klávesová skratka: NVDA+m

Ak je možnosť povolená, NVDA bude oznamovať text cez ktorý prechádza kurzor myši. Takto môžete nájsť položky na obrazovke za pomoci myši a nemusíte použiť objektovú navigáciu.

##### Jednotka oznamovania pri zameraní textu {#MouseSettingsTextUnit}

Ak je začiarknutá voľba Oznamovať text pod kurzorom myši, toto nastavenie určuje aké množstvo textu bude oznamované.
Je možno vyberať z: znak, slovo, riadok alebo odsek.

Ak potrebujete často meniť jednotku pri zameraní textu, môžete tejto funkcii priradiť klávesovú skratku v dialógu [Klávesové skratky](#InputGestures).

##### Oznamovať prvok   zameraný kurzorom myši {#MouseSettingsRole}

Ak je toto začiarkavacie políčko začiarknuté, NVDA bude oznamovať typ prvku  pri prechode myšou.
Toto zahŕňa rolu (typ) objektu a tiež jeho stav (začiarknuté / stlačené), súradnice v tabuľke a podobne.
Vyslovovanie informácií sa riadi podľa nastavení [prezentácie objektov](#ObjectPresentationSettings) alebo [nastavení čítania textu](#DocumentFormattingSettings).

##### Signalizovať polohu myši počas posúvania {#MouseSettingsAudio}

Po začiarknutí tohto políčka bude NVDA prechod po objektoch indikovať zvukom. Používateľ tak bude vedieť, kde sa myš práve nachádza.
Čím bližšie ste k hornému okraju obrazovky, tým vyšší je tón a naopak, tón klesá, ak sa posúvate myšou k dolnej časti obrazovky.
Ak myš posuniete doľava na obrazovke, pípanie sa bude ozývať z ľavého reproduktora, ak sa budete myšou posúvať smerom doprava na obrazovke, aj zvuk pípania pôjde čoraz viac z pravého reproduktora. Aby ste mohli sledovať tento rozdiel, budete potrebovať dva správne rozmiestnené reproduktory alebo slúchadlá.

##### Úroveň jasu ovplyvňuje hlasitosť signalizácie {#MouseSettingsBrightness}

Začiarknutie tohto políčka znamená, že hlasitosť signalizácie je riadená tým aká je úroveň jasu na mieste obrazovky kadiaľ prechádza kurzor myši. Toto funguje len ak začiarknete možnosť "signalizovať polohu myši počas posúvania".
Táto  voľba je predvolene vypnutá.

##### Ignorovať pokyny pre myš z externých aplikácií {#MouseSettingsHandleMouseControl}

Umožňuje ignorovať pokyny pre myš (pohyb myšou a klikanie) cez iné aplikácie, napríklad z programu TeamViewer.
Predvolene je táto možnosť vypnutá.
Ak začiarknete túto možnosť, máte povolené oznamovanie textu pod kurzorom myši a iná aplikácia bude napríklad hýbať myšou, NVDA ani v takomto prípade nebude oznamovať text pod kurzorom.

#### Dotyková obrazovka {#TouchInteraction}

Táto kategória je dostupná len ak vaše zariadenie disponuje dotykovou obrazovkou. Môžete tu nastaviť, ako sa NVDA bude správať pri používaní dotykovej obrazovky.
Nájdete tu nasledujúce možnosti.

##### Povoliť dotykové gestá {#TouchSupportEnable}

Tu môžete zapnúť a vypnúť podporu pre dotykové gestá.
Ak zapnete podporu pre dotykové gestá, môžete na ovládanie systému použiť dotykovú obrazovku a špeciálne gestá NVDA na prácu s prvkami.
Ak túto možnosť vypnete, dotyková obrazovka sa bude správať tak, akoby NVDA nebolo spustené.
Nastavenie je možné meniť aj skratkou nvda+ctrl+alt+t.

##### Písať okamžite po dotyku {#TouchTypingMode}

Určuje, akú metódu použijete pri písaní na dotykovej klávesnici.
Ak toto políčko začiarknete, na klávesnici stačí nájsť požadovaný znak a uvolľniť prst. Znak sa okamžite zapíše.
Ak políčko odčiarknete, po nájdení znaku je potrebné dvakrát poklepať na klávesnicu a až potom sa znak napíše.

#### Prezerací kurzor {#ReviewCursorSettings}

Tu môžete nastaviť, ako sa bude správať prezerací kurzor.
Táto kategória obsahuje nasledujúce možnosti:

<!-- KC:setting -->

##### Sledovať systémový fokus {#ReviewCursorFollowFocus}

Klávesová skratka: NVDA+7

Ak je táto voľba zapnutá, prezerací kurzor bude vždy pri zmene ukazovať na objekt, ktorý má systémový fokus.

<!-- KC:setting -->

##### Sledovať systémový kurzor {#ReviewCursorFollowCaret}

Klávesová skratka: NVDA+6

Ak je táto voľba zapnutá, prezerací kurzor sa vždy pri zmene posunie na miesto, na ktoré ukazuje systémový kurzor.

##### Sledovať kurzor myši {#ReviewCursorFollowMouse}

Ak je táto voľba zapnutá, prezerací kurzor bude pri posúvaní sledovať kurzor myši.

##### Jednoduchý režim objektovej navigácie {#ReviewCursorSimple}

Ak je táto voľba zapnutá, NVDA bude filtrovať stromovú hierarchiu objektovej navigácie a vynechá objekty, ktoré nie sú pre vás dôležité. Sú to objekty, ktoré nie sú viditeľné alebo objekty, ktoré dopĺňajú vzhľad.

jednoduchý režim môžete zapínať a vypínať aj klávesovou skratkou. Stačí, ak ju definujete v dialógu [Klávesové skratky](#InputGestures).

#### Prezentácia objektov {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Otvorí nastavenia prezentácie objektov {#OpenObjectPresentationSettings}

Klávesová skratka: `NVDA+ctrl+o`

Tu môžete nastaviť, aké informácie bude NVDA čítať o prvkoch, napríklad pozíciu, počet a podobne.
Tieto nastavenia neovplyvňujú režim prehliadania.
Tieto nastavenia ovplyvňujú oznamovanie pri pohybe kurzorom a objektovej navigácii, nie pri čítaní textu napríklad v režime prehliadania.

##### Oznamovať kontextovú nápovedu {#ObjectPresentationReportToolTips}

Začiarkávacie políčko, ktoré ak je začiarknuté, NVDA bude oznamovať kontextovú nápovedu.
Mnoho programov zobrazuje krátke texty, ak sa na ne postavíme kurzorom myši, alebo ak na ne presunieme fokus.

##### Automaticky oznamovať notifikácie {#ObjectPresentationReportNotifications}

Keď je začiarknuté, NVDA bude automaticky oznamovať upozornenia a bublinkovú nápovedu.

* Bublinková nápoveda je podobná ako kontextová nápoveda, ale zvyčajne zaberá na obrazovke viac miesta a viaže sa ku systémovým informáciám, ako napríklad odpojenie sieťového kábla, či ohlásenie výstrah k bezpečnosti systému.
* Oznámenia na pruhu (známe tiež ako toast notifikácie) boli predstavené v systéme Windows 10 a objavujú sa v centre akcií. Informujú napríklad o stiahnutí aktualizácie alebo príchode e-mailu.

##### Oznamovať skratkové klávesy objektov {#ObjectPresentationShortcutKeys}

Ak je toto začiarkavacie políčko začiarknuté, NVDA bude oznamovať klávesové skratky, ktoré sú viazané ku rôznym príkazom a objektom.
Napríklad: menu súbor má skratku Alt +S, takže súčasťou popisu objektu pri ohlásení bude aj jeho klávesová skratka.

##### Oznamovať pozíciu objektu {#ObjectPresentationPositionInfo}

Táto voľba umožňuje prispôsobenie čítania informácií o pozícii objektu v prípade získania fokusu alebo zamerania objektovou navigáciou. Je to napr. informácia o položke zoznamu (1 z 10) a pod.

##### Odhadnúť pozíciu objektu ak nie je dostupná {#ObjectPresentationGuessPositionInfo}

Ak je zapnuté oznamovanie pozícii objektu, táto voľba umožňuje NVDA odhadnúť pozíciu aktuálne zameraného objektu ak informácia o pozícii nie je štandardne dostupná.

Ak je toto začiarknuté, NVDA bude oznamovať informácie o pozícii pre viacej prvkov, napr. položky v ponukách a panely nástrojov, aj keď tieto informácie nemusia vždy byť dostatočne presné.

##### Oznamovať popisky objektov {#ObjectPresentationReportDescriptions}

Odčiarknite toto políčko, ak si myslíte, že vás popisy objektov obťažujú. NVDA v takomto prípade nebude čítať napríklad návrhy výsledkov hľadania, alebo neprečíta obsah dialógu po jeho otvorení.

<!-- KC:setting -->

##### Oznamovanie aktualizácie indikátora priebehu {#ObjectPresentationProgressBarOutput}

Klávesová skratka: NVDA+u

Táto voľba nastavuje ako bude NVDA oznamovať zmenu počas aktualizácie indikátora priebehu.

Momentálne sú dostupné tieto možnosti:

* Vypnuté: aktualizácia indikátora priebehu nebude oznamovaná.
* Čítať: Toto zaistí čítanie hodnoty indikátora priebehu v percentách. Vždy ak sa hodnota zmení, NVDA na túto skutočnosť upozorní.
* Pípať: Toto nastavenie zaistí, že pri každej aktualizácii indikátora priebehu NVDA zapípa. Čím je tón pípania vyšší, tým je akcia sprevádzajúca indikátorom priebehu bližšie ku koncu.
* Čítať a pípať: Táto voľba je kombináciou dvoch predchádzajúcich. NVDA zároveň pípa aj oznamuje aktualizáciu indikátora priebehu hlasom.

##### Oznamovať aktualizáciu indikátorov priebehu na pozadí {#ObjectPresentationReportBackgroundProgressBars}

Ak je táto voľba začiarknutá, NVDA bude sledovať aj priebeh takých indikátorov, ktoré nie sú zobrazené v okne v popredí.
Znamená to, že ak minimalizujete okno, v ktorom je zobrazený indikátor priebehu, môžete robiť niečo úplne iné, zatiaľ čo NVDA naďalej oznamuje aktualizáciu tohto priebehu.

<!-- KC:setting -->

##### Oznamovať dynamicky menený obsah {#ObjectPresentationReportDynamicContent}

Klávesová skratka: NVDA+5

Prepína automatické oznamovanie obsahu v niektorých objektoch ako sú napríklad terminály alebo prichádzajúci text v chatovacích programoch.

##### Upozorňovať zvukom na automatické návrhy {#ObjectPresentationSuggestionSounds}

Zapína a vypína oznamovanie v situáciách, keď sa zobrazia automatické návrhy. Ak je toto zapnuté, pri zobrazení automatických návrhov sa ozve zvuk.
Automatické návrhy sú položky, ktoré sa zobrazia na základe toho, čo napíšete do editačného poľa.
Ak napríklad napíšete text do poľa hľadať v ponuke štart v systéme Windows Vista a novších, systém zobrazí návrhy toho, čo dokáže vyhľadať.
NVDA môže rozpoznať takýto zoznam návrhov v editačných poliach na vyhľadávanie v rôznych aplikáciách v systéme Windows 10 a upozorniť naň.
Zoznam s automatickými návrhmi sa zatvorí, keď opustíte editačné pole a NVDA vás na to tiež v mnohých prípadoch dokáže upozorniť.

#### Nastavenia vstupu {#InputCompositionSettings}

Môžete tu nastaviť odozvu pri písaní ázijských znakov, ak je použitá textová služba alebo IME.
Je dôležité si uvedomiť, že v závislosti od konkrétnych textových služieb sú dostupné rôzne vlastnosti pri vkladaní znakov s rôznymi spôsobmi sprístupnenia poskytovaných informácií. Preto je veľmi pravdepodobné, že bude potrebné tieto zmeny prispôsobiť tak, aby Ste s použitím konkrétnej textovej služby dosahovali čo najlepšie skúsenosti pri písaní.

##### Automaticky oznamovať všetky návrhy {#InputCompositionReportAllCandidates}

Táto možnosť je predvolene začiarknutá. Určuje, či budú oznamované všetky návrhy, ak sa zobrazí alebo zmení zoznam návrhov.
Toto je užitočné pri písaní v piktografických písmach, ako napríklad chinese New ChangJie, alebo Boshiami. Budete počuť návrhy a zvolenú možnosť vyberiete zadaním konkrétneho čísla.
Pri používaní fonetického písma, ako napríklad Chinese New Phonetic, je lepšie túto možnosť odčiarknuť. Všetky znaky totiž znejú rovnako a musíte si zoznam prehliadať šípkami, aby ste získali podrobnejšiu informáciu o vybratom znaku.

##### Oznamovať vybratý návrh {#InputCompositionAnnounceSelectedCandidate}

Táto predvolene začiarknutá voľba umožňuje nastaviť automatické oznamovanie ak sa na obrazovke objaví zoznam návrhov alebo ak dôjde ku zmene v tomto zozname.
Pre textové služby, kde je možné v zozname návrhov vybrať položku pomocou kurzorových klávesov napr. chinese new phonetic je povolenie tohto nastavenia nevyhnutné, ale s inými službami bude písanie efektívnejšie ak bude toto nastavenie vypnuté.
Ak bude aj toto nastavenie vypnuté, prezerací kurzor bude vždy automaticky ukazovať na vybratý návrh, čo umožní rýchle čítanie pomocou objektovej navigácie a prezeracieho kurzora.

##### Oznamovať popis pre znaky v zozname návrhov {#InputCompositionCandidateIncludesShortCharacterDescription}

Táto predvolene začiarknutá možnosť umožňuje nastaviť, či má NVDA pre každý znak v zozname návrhov prečítať krátky popis či už pri výbere návrhu alebo aj pri jeho automatickom prečítaní hneď ako sa objaví zoznam návrhov.
Pre niektoré miestne nastavenia napr. čínštinu táto voľba nemá vplyv na oznamovanie rozšírených popisov pre znaky v zozname návrhu.
Táto možnosť je užitočná pre textové služby, ktoré sa používajú pri zapisovaní japončiny a kórejčiny.

##### Oznamovať zmeny predbežného návrhu {#InputCompositionReadingStringChanges}

Pri niektorých službách sa používa tzv. predbežný návrh Sú to napríklad Chinese New Phonetic a New ChangJie.
Môžete nastaviť, či má NVDA oznamovať nové znaky, ktoré sa objavia v tomto návrhu.
Táto možnosť je predvolene začiarknutá.
Niektoré staršie textové služby napr. Chinese ChangJie môžu namiesto predbežného návrhu meniť priamo skladaný reťazec, v takom prípade si pozrite nasledujúce nastavenie.

##### Oznamovať zmeny v práve skladanom reťazci {#InputCompositionCompositionStringChanges}

Potom, čo z údajov v predbežnom návrhu vznikne správny piktografický symbol, ešte pred vložením do samotného dokumentu textové služby vložia tento symbol k ostatným symbolom do tzv. skladaného reťazca.
Toto nastavuje, či NVDA bude oznamovať nové znaky, ktoré sa objavia v skladanom reťazci.
Táto možnosť je predvolene začiarknutá.

#### Režim prehliadania {#BrowseModeSettings}

<!-- KC:setting -->

##### Otvorí nastavenia režimu prehliadania {#OpenBrowseModeSettings}

Klávesová skratka: `NVDA+ctrl+b`

V tejto kategórii nastavení môžeme nastaviť správanie NVDA pri čítaní webových stránok a iných komplexných dokumentov.
Tu nájdeme nasledujúce možnosti:

##### Maximálny počet znakov na riadku {#BrowseModeSettingsMaxLength}

V tomto editačnom poli nastavíte počet znakov na jeden riadok v režime prehliadania.

##### Maximálny počet riadkov na jednej stránke {#BrowseModeSettingsPageLines}

Toto nastavenie určuje o koľko riadkov sa má NVDA posunúť pri pohybe po stlačení page up a page down v režime prehliadania.

<!-- KC:setting -->

##### Zachovať vzhľad ako na obrazovke {#BrowseModeSettingsScreenLayout}

Klávesová skratka: NVDA+v

Určuje, či budú klikateľné prvky zobrazené na samostatných riadkoch, alebo budú zobrazené v texte tak, ako sú usporiadané vizuálne.
Upozorňujeme, že táto možnosť neovplyvňuje prezentáciu prvkov v Aplikáciách MS Office, ako napríklad Word a Outlook. Tu je automaticky vždy uprednostnené zachovanie vzhľadu ako na obrazovke.
Ak je možnosť zapnutá, ostanú prvky zobrazené tak, ako sú rozmiestnené na obrazovke.
Viacero odkazov na jednom riadku bude prečítaných a zobrazených na brailovom riadku spoločne na jednom riadku.
Ak je možnosť vypnutá, budú odkazy rozdelené každý na samostatnom riadku.
Toto mnohým používateľom zjednodušuje navigáciu a interakciu.

##### Po načítaní stránky  automaticky aktivovať režim prehliadania {#BrowseModeSettingsEnableOnPageLoad}

Určuje, či sa má po načítaní dokumentu automaticky aktivovať režim prehliadania.
Ak je táto možnosť vypnutá, stále môžete v podporovaných dokumentoch a prvkoch aktivovať režim prehliadania ručne.
Podporované aplikácie sú popísané v časti [Režim prehliadania](#BrowseMode).
Toto nastavenie neovplyvňuje aplikácie, v ktorých je režim prehliadania voliteľný, napríklad Microsoft Word.
Predvolene je toto nastavenie začiarknuté.

##### Automaticky spustiť plynulé čítanie po načítaní stránky {#BrowseModeSettingsAutoSayAll}

Toto začiarkavacie políčko prepína automatické plynulé čítanie po načítaní stránky v režime prehliadania.
Predvolene je začiarknuté.

##### Oznamovať tabuľky formujúce vzhľad {#BrowseModeSettingsIncludeLayoutTables}

Táto voľba rozhoduje o tom, ako NVDA spracuje tabuľky určené výhradne na formovanie vzhľadu dokumentu.
Ak voľbu začiarknete, NVDA tieto tabuľky spracuje štandardne podľa [nastavení čítania textu](#DocumentFormattingSettings) a budete ich môcť nájsť pomocou rýchlej navigácie.
Ak voľbu odčiarknete, NVDA ich nebude hlásiť ako tabuľky a nebudú sa dať nájsť pomocou rýchlej navigácie.
obsah týchto tabuliek však bude NVDA zobrazovať ako čistý text.
Táto možnosť je v predvolenom nastavení vypnutá.

Ak chcete toto nastavenie meniť odkiaľkoľvek, môžete si nastaviť samostatnú skratku v dialógu [Klávesové skratky](#InputGestures).

##### Ohlásenie podrobných nastavení prvkov {#BrowseModeLinksAndHeadings}

Môžete rozhodnúť, či bude NVDA oznamovať odkazy, nadpisy, tabuľky a podobne. Nastavenie vykonáte v dialógu [nastavenia](#NVDASettings) v kategórii [Nastavenia čítania textu](#DocumentFormattingSettings).

##### Automaticky aktivovať režim fokusu pri zmene fokusu {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Táto možnosť umožňuje automatické zapínanie režimu fokusu v prípade, že sa zmení systémový fokus.
Napríklad ak pri prehliadaní web stránky použijete kláves tab a fokus získa editačné pole, automaticky sa zapne režim fokusu.

##### Automaticky aktivovať režim fokusu pri pohybe kurzorom {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Po zapnutí tejto voľby NVDA dokáže automaticky zapínať a vypínať režim fokusu pri čítaní v režime prehliadania.
Napríklad ak sa po riadkoch posúvate po stránke a zameriate týmto spôsobom editačné pole, automaticky sa aktivuje režim fokusu.
Ak budete v navigácii pokračovať, režim  fokusu sa automaticky vypne.

##### Režim prehliadania a režim fokusu oznamovať zvukom {#BrowseModeSettingsPassThroughAudioIndication}

Ak je táto voľba začiarknutá, NVDA bude namiesto oznamovania prepínania režimu prehliadania a režimu fokusu prehrávať zvuky špeciálne priradené k týmto akciám.

##### Ignorovať skratky mimo rýchlej navigácie {#BrowseModeSettingsTrapNonCommandGestures}

Táto možnosť je predvolene začiarknutá a spôsobuje, že skratky, ktoré sa nepoužívajú v rýchlej navigácii, nebudú posielané do aktívnej aplikácie.
Ak napríklad stlačíte v dokumente písmeno j, toto sa pri začiarknutom poli nenapíše do aktívneho dokumentu, ani nebude poslané do aplikácie  ako klávesová skratka.
V tomto prípade NVDA prikáže systému, aby prehral predvolený zvuk vždy, ak je stlačená skratka, ktorá nie je skratkou NVDA ani skratkou rýchlej navigácie.

<!-- KC:setting -->

##### Automaticky presúvať fokus na zamerané prvky {#BrowseModeSettingsAutoFocusFocusableElements}

Klávesová skratka: NVDA+8

Táto možnosť je predvolene vypnutá. Určuje, či sa má systémový fokus presúvať na prvky, ktoré je možné zamerať a prejdete na ne kurzorom v režime prehliadania (napríklad odkazy, prvky formulárov a podobne).
Ak vypnete túto možnosť, prvky nebudú automaticky zamerané.
Toto môže zrýchlyť prehliadanie dokumentov v režime prehliadania.
Fokus sa automaticky presunie na prvok až vtedy, keď s ním budete pracovať (aktivovanie tlačidla, začiarknutie políčka a pod).
Zapnutie tejto možnosti môže zlepšiť prácu na niektorých vebových stránkach.

#### Čítanie textu {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Otvorí nastavenia čítania textu {#OpenDocumentFormattingSettings}

Klávesová skratka: `NVDA+ctrl+d`

Väčšina možností v tejto kategóriislúži na nastavenie typu formátovania, ktorý bude automaticky oznamovaný pri pohybe kurzora v dokumentoch.
Napríklad ak začiarknete oznamovanie písma, NVDA oznámi keď systémový kurzor bude ukazovať na iný typ písma.

Dialóg je rozdelený do skupín.
Takto môžete nastaviť:

* písmo
  * Názov písma
  * Veľkosť písma
  * Vlastnosti písma
  * indexy
  * Zvýraznenie
  * vyznačený text
  * štýl
  * Farby
* Informácie o dokumente
  * Komentáre
  * Záložky
  * Zmeny
  * Pravopisné chyby
* Riadkovanie a strany
  * Číslovanie strán
  * Číslovanie riadkov
  * Odsadenie riadka [(vypnuté, reč, pípanie alebo reč a pípanie)](#DocumentFormattingSettingsLineIndentation)
  * Ignorovanie prázdnych riadkov pri oznamovaní odsadenia
  * Odsadenie odseku (vysunutý text, odsadenie prvého riadka)
  * Riadkovanie (jednoduché, dvojité, ...)
  * zarovnanie
* Informácie o tabuľke
  * Tabuľky
  * Hlavičky riadkov stĺpcov tabuľky (Vypnuté, Riadky, Stĺpce, Riadky aj stĺpce)
  * súradnice buniek tabuľky
  * orámovanie (vypnuté, štýly, oboje farby a štýly)
* Prvky
  * nadpisy
  * odkazy
  * grafiku
  * zoznamy
  * citácie
  * Zoskupenia
  * oblasti
  * články
  * rámce
  * Ilustrácie a ich popisy
  * pri kliknutí

Ak chcete tieto nastavenia meniť bez nutnosti otvárať dialóg s nastaveniami, môžete si nastaviť  klávesové príkazy   v dialógu [Klávesové skratky](#InputGestures).

##### Oznamovať zmeny formátovania pri pohybe kurzorom {#DocumentFormattingDetectFormatAfterCursor}

Ak je zapnuté, NVDA sa pokúsi nájsť zmeny formátovania v celom riadku a počas čítania ich všetky oznámi. Toto  môže do určitej miery spomaliť odozvu.

Predvolene NVDA deteguje formátovacie možnosti na mieste systémového / prezeracieho kurzora a voliteľne môže detegovať formátovacie možnosti v celom aktuálnom riadku ak to nespôsobí príliš veľké spomalenie.

Túto voľbu odporúčame použiť, keď kontrolujete dokumenty v aplikáciách ako Wordpad a formátovanie je pre vás dôležité.

##### odsadenie riadka {#DocumentFormattingSettingsLineIndentation}

určuje, ako budú oznamované medzeri na začiatku riadka.
Môžete si vybrať zo štyroch možností:

* Vypnuté: Medzeri na začiatku riadka nebudú hlásené
* Reč: ak sa zmení odsadenie riadka, budete počuť napríklad "12 medzera" alebo "4 tab"
* Pípať: Zmeny odsadenia sú oznamované pípaním.
Tón sa zvyšuje pri každej medzere, pri každom tabulátore sa zvyšuje štvornásobne.
* Oznamovať a pípať: Oznamuje odsadenie riadka hlasom aj pípaním podľa pravidiel uvedených vyššie.

Ak začiarknete možnosť "Ignorovať prázdne riadky pre oznamovanie odsadenia", NVDA nebude oznamovať odsadenie na prázdnych riadkoch.
Toto je užitočné pri čítaní dokumentov, v ktorých sa prázdne riadky používajú na oddelenie odsadených častí textu, napríklad pri tvorbe zdrojového kódu.

#### Navigácia v dokumente {#DocumentNavigation}

Táto kategória nastavení umožňuje upraviť rôzne možnosti navigácie v dokumentoch.

##### Za odsek považovať {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Predvolené |Podľa aplikácie|
|Možnosti |Predvolené (podľa aplikácie), Podľa aplikácie, jeden zlom riadka, viacero zlomov riadka|

Toto nastavenie určuje, čo bude považované za odseky, pri pohybe pomocou skratiek `ctrl+šípka hore` a `ctrl+šípka dole`.
Dostupné sú tieto možnosti:

* Podľa aplikácie: NVDA požiada aplikáciu o prechod na predchádzajúci alebo nasledujúci odsek a prejde naň podľa nastavení aplikácie.
Toto najlepšie funguje v prípadoch, ak samotná aplikácia podporuje navigáciu medzi odsekmi. Toto nastavenie sa používa ako predvolené.
* Jeden zlom riadka: Nvda bude za oddeľovač odsekov považovať jeden zlom riadka.
Toto najlepšie funguje v aplikáciách, ktoré predvolene neumožňujú navigáciu po odsekoch a odseky sú oddeľované jedným stlačením klávesu `enter`.
* Viacero zlomov riadka: NVDA bude za oddeľovač odsekov považovať jeden prázdny riadok, teda dvojité stlačenie klávesu `enter`.
Toto nastavenie najlepšie funguje v prípadoch, ak sa používajú blokové odseky.
Upozorňujeme, že toto nastavenie nefunguje v aplikáciách Microsoft Word alebo Microsoft Outlook, ak nepoužívate rozhranie UIA na prácu s prvkami MS Word.

Toto nastavenie je možné kdekoľvek meniť aj pomocou klávesových skratiek. Tieto je potrebné definovať v dialógu [Klávesové skratky](#InputGestures).

#### Rozpoznávanie textu windows {#Win10OcrSettings}

Môžete tu  nastaviť parametre pre rozpoznávanie textu pomocou rozhrania [Windows OCR](#Win10Ocr).
Kategória obsahuje nasledujúce možnosti:

##### jazyk rozpoznávania {#Win10OcrSettingsRecognitionLanguage}

V tomto zozname môžete vybrať jazyk, ktorý sa bude používať na rozpoznávanie textu.
Ak chcete prepínať medzi dostupnými jazykmi odkiaľkoľvek, vytvorte si skratku v [Dialógu klávesové skratky](#InputGestures).

##### Pravidelne obnovovať rozpoznaný text {#Win10OcrSettingsAutoRefresh}

Ak je táto možnosť zapnutá, NVDA bude pravidelne sledovať zmeny v rozpoznanom texte, ak je fokus v okne rozpoznávania.
Toto je užitočné, ak chcete často sledovať zmeny, napríklad pri sledovaní filmu s titulkami.
K obnoveniu dochádza raz za jeden a pol sekundy.
Predvolene je táto možnosť vypnutá.

#### Pokročilé {#AdvancedSettings}

Pozor! Tieto nastavenia sú určené pre pokročilých používateľov. Nesprávnou konfiguráciou môžete spôsobiť, že NVDA nebude pracovať správne.
Upravujte tieto nastavenia v prípade, že viete, čo máte robiť alebo ste dostali inštrukcie od vývojára NVDA.

##### Povolenie zmien v pokročilích nastaveniach {#AdvancedSettingsMakingChanges}

Pred úpravou pokročilých nastavení musíte začiarknuť začiarkávacie políčko, čím potvrdíte, že rozumiete ryzikám.

##### Obnovenie predvolených nastavení {#AdvancedSettingsRestoringDefaults}

Toto tlačidlo obnoví predvolené hodnoty pre pokročilé možnosti a to aj v prípade, ak je vyššie spomenuté začiarkávacie políčko odčiarknuté.
Po zmene nastavení sa časom môžete chcieť vrátiť k pôvodným hodnotám.
Môžete chcieť obnoviť pôvodné nastavenie, ak si nie ste istí, čo všetko ste zmenili.

##### Načítať vlastné moduly z priečinka Scratchpad {#AdvancedSettingsEnableScratchpad}

Keď vyvíjate doplnky pre NVDA, je lepšie testovať ich okamžite počas písania kódu.
Ak začiarknete túto možnosť, NVDA bude načítavať aplikačné moduly, globálne pluginy, ovládače pre syntézy reči a brailové riadky a rozšírenia pre rozpoznávanie textu a obrázkov, z priečinka scratchpad vo vašom priečinku s nastaveniami NVDA.
Rovnako ako doplnky, aj tieto moduly sa automaticky načítajú po spustení  NVDA, alebo, ak ide o globálne pluginy a aplikačné moduly, ak ručne [Vyvoláte položku znovu načítať pluginy](#ReloadPlugins).
Predvolene je táto možnosť vypnutá, aby sme zaistili, že sa nespúšťa neoverený kód bez výslovného súhlasu používateľa.
Ak chcete to, čo ste naprogramovali distribuovať, je potrebné vytvoriť doplnok pre NVDA vo formáte nvda-addon.

##### Otvoriť priečinok Scratchpad {#AdvancedSettingsOpenScratchpadDir}

Po aktivovaní tohto tlačidla sa otvorí priečinok, do ktorého môžete ukladať vlastné experimentálne kódy počas práce na doplnkoch, moduloch a pod.
Toto tlačidlo sa zobrazí, len ak povolíte načítavanie vlastných modulov z priečinka Scratchpad.

##### Sledovanie zmien a udalostí UI Automation {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Automaticky, Vybraté, Globálne|
|Predvolené |Automaticky|

Určuje, ako NVDA spracúva udalosti prijaté z rozhrania Microsoft UI Automation.
zoznamový rámik Sledovanie zmien a udalostí UI Automation má tri možnosti:

* Automaticky: "vybraté" vo Windows 11 Sun Valley 2 (verzia 22H2) a novších, "globalne" v ostatných prípadoch.
* Vybraté: NVDA obmedzí sledovanie na systémový fokus pre väčšinu udalostí.
Ak badáte spomalenie pri práci v aplikáciách, skúste zapnúť túto možnosť.
Avšak v starších verziách systému Windows môže mať NVDA problémy sledovať zamerané prvky napríklad na panely úloh alebo v panely emotikonov.
* Globálne: NVDA sleduje všetky udalosti a zmeny vlastností a sám určuje, ktoré spracovať a ktoré zahodiť.
Vďaka tomuto môže byť sledovanie zameranej položky omnoho spoľahlivejšie v mnohých prípadoch, ale výkon môže byť výrazne ukrátený najmä v aplikácii Visual Studio.

##### Na sprístupnenie prvkov v dokumentoch Microsoft Word preferovať UI Automation {#MSWordUIA}

Určuje, či sa má na sprístupnenie prvkov v dokumentoch MS Word použiť rozhranie UI Automation, alebo starší objektový model.
Toto sa týka dokumentov MS Word a tiež správ v programe MS Outlook.
Je možné nastaviť tieto možnosti:

* predvolené  (Ak to má zmysel
* Len keď  je to nevyhnutné: Použije sa len v prípadoch, ak nie je dostupný objektový model
* Ak to má zmysel: Od verzie Microsoft Word  16.0.15000, alebo ak objektový model nie je dostupný
* Vždy: Použije sa vždy, keď je dostupná podpora pre UI Automation, pričom táto podpora nemusí byť kompletná.

##### Na sprístupnenie prvkov v zošitoch Microsoft Excel používať UI Automation {#UseUiaForExcel}

Keď je táto voľba aktívna, NVDA sa pokúsi na získavanie informácií o ovládacích prvkoch v programe Microsoft Excel používať rozhranie prístupnosti Microsoft UI Automation.
Toto je experimentálna funkcia a niektoré vlastnosti programu Microsoft Excel nemusia byť v tomto režime dostupné.
Takímito sú hlavne zoznam prvkov NVDA, kde je možné si zobraziť zoznamy vzorcov a komentárov a podpora pre rýchlu navigáciu v režime prehliadania na pohyb po prvkoch formulára v zošite.
Pre základnú navigáciu v zošite a jednoduché úpravy, tento režim poskytne výrazné zrýchlenie odozvy.
Zatiaľ neodporúčame toto nastavenie aktivovať pre väčšinu bežných používateľov, ale budeme radi, ak si tento režim vyskúšate s programom Microsoft Excel od verzie  16.0.13522.10000 a poskytnete nám spätnú väzbu.
Implementácia rozhrania UI automation v programe Microsoft Excel sa stále zlepšuje a staršie verzie než Microsoft Office 16.0.13522.10000 nemusia poskytovať dostatok informácií, aby ste z tohto nastavenia mohli mať skutočný úžitok.

##### Použiť pokročilé spracovanie udalostí {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Predvolené (zapnuté), vypnuté, zapnuté|
|Predvolené|  Zapnuté |

Ak je toto zapnuté, NVDA má rýchlu odozvu aj v prípade, že dostáva množstvo udalostí cez rozhranie UIA, napríklad v oknách konzolových aplikácií a terminálov.
Aby sa prejavili zmeny, je potrebné NVDA po zmene tohto nastavenia reštartovať.

##### Podpora pre konzolu Windows {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Automaticky, UIA ak je dostupné, staršie|
|Predvolené |Automaticky|

Určuje, ako NVDA spolupracuje s Windows konzolami v príkazovom riadku, PowerShell a Windows Subsystémom pre Linux.
Nastavenie tejto možnosti nemá vplyv na moderný Windows terminál.
V systéme Windows 10 vo verzii 1709, Microsoft [pridal podporu pre UI Automation API do konzoly (text v angličtine)](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), čím priniesol vylepšenú odozvu a stabilitu pre čítače obrazovky, ktoré túto možnosť podporujú.
Ak UI Automation nie je dostupné, alebo je známe, že prináša horšie výsledky, NVDA sa vráti k pôvodnému, staršiemu spôsobu spracovania výstupu z konzoly.
Dostupné sú tri možnosti:

* Automaticky: Používa UI Automation od verzie Windows 11  22H2.
Táto možnosť je odporúčaná a predvolene nastavená.
* UIA ak je dostupné: Používa UI Automation v konzolách vždy, keď je to možné, aj vo verziách s nepresnou a chybovou implementáciou.
Hoci táto možnosť môže byť užitočná (a postačujúca pre vaše potreby), používate ju na vlastné ryziko a pre tieto prípady neponúkame podporu.
* Staršie: UI Automation vo Windows konzolách bude úplne vypnuté.
Táto možnosť sa zapína automaticky vždy, ak by použitie UI Automation prinášalo zhoršenú odozvu.
Preto odporúčame zvoliť túto možnosť len v prípadoch, ak viete, čo robíte.

##### Použiť UI Automation v Microsoft Edge a ostatných prehliadačoch založených na Chromium {#ChromiumUIA}

Umožňuje nastaviť za akých okolností sa použije rozhranie UIA, ak je dostupné v prehliadačoch založených na jadre Chromium ako je Microsoft Edge.
Podpora pre sprístupnenie prehliadačov založených na jadre Chromium cez rozhranie prístupnosti UIA je v skorom štádiu vývoja a nemusí poskytovať dostatočnú úroveň prístupnosti ako prístupnosť cez rozhranie IA2.
V zoznamovom rámiku sa nachádzajú tieto možnosti:

* Predvolené (len keď je to nevyhnutné): Predvolená hodnota NVDA, momentálne len keď je to nevyhnutné. V budúcnosti sa  môže zmeniť, keď sa technológia vyvinie do dokonalosti.
* Len keď je to nevyhnutné: Ak sa NVDA nedokáže zaviesť do procesu prehliadača s cieľom použiť rozhranie IA2 a k dispozícii je rozhranie UIA, NVDA použie UIA ako náhradu.
* Áno: Vždy ak je v prehliadači k dispozícii rozhranie UIA, NVDA ho použije.
* Nie: UIA sa nepoužije vôbec, ani ak sa NVDA nedokáže zaviesť do procesu prehliadača. Môže byť užitočné pre vývojárov, pri ladení implementácie IA2.

##### Revízie {#Annotations}

Táto skupina experimentálnych funkcií určuje, ako bude NVDA oznamovať revízie označované pomocou aria atribútov.
Niektoré funkcie nemusia byť dokončené.

<!-- KC:beginInclude -->
Aby ste zobrazili informácie o komentároch a poznámkach pod systémovým kurzorom, stlačte nvda+d.
<!-- KC:endInclude -->

Dostupné sú tieto možnosti:

* Oznamovať detaily pre štruktúrované poznámky a komentáre: Ak je začiarknuté, oznamuje, ak text alebo prvok obsahuje anotácie.
* Vždy oznamovať prítomnosť atribútu aria-description:
  Ak je zdroj `accDescription` určený ako aria-description, nvda tento popis oznámi.
  Toto je užitočné pri oznamovaní zmien na webe.
  Upozornenie:
  * Existuje viacero zdrojov pre `accDescription` Mnohé majú viaceré alebo nepresné významy.
    V minulosti asistenčné technológie neoznamovali  zdroje `accDescription`, nakoľko nebolo možné rozlíšiť, o aký druh zdroja ide.
  * Táto funkcia je v ranom štádiu vývoja a jej dostupnosť závisí od použitého prehliadača, pričom mohé ju zatiaľ nepodporujú.
  * Očakávame funkčnosť v Chromium 92.0.4479.0+

##### Oznamovať dynamicky menený obsah označený pomocou Live Region {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |predvolené (zapnuté), Vypnuté, zapnuté|
|Predvolené |Zapnuté|

Toto nastavenie určuje, či bude NVDA oznamovať niektoré typy dynamicky meneného obsahu na brailovom riadku.
Vypnutím tejto možnosti dosiahnete stav, ktorý platil do verzie NVDA 2023.1, kedy boli zmeny oznamované len cez hlasový výstup.

##### Hovoriť heslá v rozšírených termináloch {#AdvancedSettingsWinConsoleSpeakPasswords}

Toto nastavenie určuje, či NVDA [číta napísané znaky](#KeyboardSettingsSpeakTypedCharacters) alebo [číta po slovách](#KeyboardSettingsSpeakTypedWords) v prípadoch, ak sa obrazovka neaktualizuje (napríklad pri písaní hesiel) v niektorých termináloch, ako napríklad Windows konzola s aktívnou podporou UI automation, alebo v programe Mintty.
Z bezpečnostného hľadiska odporúčame toto nastavenie ponechať vypnuté.
Môžete ho zapnúť, ak zaznamenáte zhoršenú odozvu alebo stabilitu vo Windows konzolách pri aktívnom čítaní po znakoch a po slovách, alebo ak pracujete v bezpečnom prostredí.

##### Použiť rozšírenú  podporu oznamovania napísaných znakov v starších Windows konzolách {#AdvancedSettingsKeyboardSupportInLegacy}

Toto začiarkávacie pole aktivuje alternatívnu metódu oznamovania napísaných znakov v starších windows konzolách.
Toto môže zlepšiť odozvu a odstrániť hláskovanie výstupu z konzoly, súčasne však toto nastavenie nie je vhodné pre všetky terminály.
Táto možnosť je dostupná a predvolene aktivovaná v systémoch od verzie Windows 10 1607 ak je vypnuté alebo nedostupné UI Automation.
Pozor: Keď aktivujete túto funkciu, NVDA bude čítať napísané znaky a slová aj pri písaní hesiel.
Ak tomu chcete zabrániť, vypnite dočasne [čítanie po znakoch](#KeyboardSettingsSpeakTypedCharacters) a [slovách](#KeyboardSettingsSpeakTypedWords) pri písaní hesiel.

##### Algoritmus počítania rozdielov {#DiffAlgo}

Toto nastavenie ovplyvňuje, ako NVDA zisťuje nový text na prečítanie v okne príkazového riadku.
V zoznamovom rámiku sú 3 možnosti:

* Automaticky: NVDA v tomto prípade preferuje metódu Diff Match Patch, ale v niektorých prípadoch, napríklad starších Windows konzolách a v Mindty uprednostní Difflib.
* Diff Match Patch: Táto možnosť spôsobí, že NVDA zisťuje text na prečítanie v okne príkazového riadku po znakoch.
Môže to zlepšiť odozvu pri veľkom množstve textu na výstupe a spresniť oznamovanie zmien v strede riadkov.
V niektorých prípadoch však môže byť čítanie textu trhané a nekonzistentné.
* Difflib: Pri tomto nastavení NVDA počíta text na prečítanie po riadkoch a to aj v situáciách, kedy toto nemusí byť žiaduce.
Takto sa správalo NVDA do verzie 2020.4.
Tento spôsob môže zlepšiť čítanie textu v niektorých prípadoch.
Ak však v terminály použijete túto metódu a súčasne odstránite text uprostred riadka, automaticky bude dočítaný text do konca riadka.

##### Oznamovať nový text vo Windows termináloch cez {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Predvolené (Diffing), Diffing, Upozornenia rozhrania UIA|
|Predvolené |Diffing|

Toto nastavenie určuje, ako NVDA identifikuje nový text vo Windows konzole a WPF Windows Termináloch používaných vo Visual Studio 2022. Nový text je potom automaticky oznamovaný, ak je zapnuté oznamovanie dynamicky meneného obsahu.
Toto nemá vplyv na Windows konzolu(`conhost.exe`).
Dostupné sú tieto možnosti:

* Predvolené: Aktuálne sa používa "diffing", keď sa zlepší podpora pre UIA, môže byť nahradené upozorneniami z UIA rozhrania.
* Diffing: Používa zvolený algoritmus na určovanie rozdielov na výpočet vždy, keď terminál zobrazí nový text.
Toto je správanie identické do verzie NVDA 2022.4.
* Upozornenia rozhrania UIA: V tomto prípade rozhoduje priamo Windows konzola, čo je považované za nový text a NVDA len preberá obsah.
Toto zlepšuje odozvu a stabilitu Windows terminálov, ale funkcionalita v súčasnosti nie je dokončená.
Aktuálne sú pri tejto metóde oznamované napísané znaky vrátane hesiel.
Navyše, výstup dlhší ako 1000 znakov nemusí byť oznamovaný správne.

##### Prerušiť reč po vypršaní zameranej udalosti {#CancelExpiredFocusSpeech}

Ak je táto možnosť zapnutá, NVDA prestane čítať udalosti, ktoré už nie sú aktuálne.
Toto môže vyriešiť problém, keď pri prezeraní správ v aplikácii Gmail v prehliadači Chrome NVDA čítalo neaktuálne informácie.
Táto funkcia je predvolene zapnutá od verzie NVDA 2021.1.

##### Počkať pred pohybom systémového kurzora (v milisekundách) {#AdvancedSettingsCaretMoveTimeout}

Tu môžete nastaviť časový úsek, ktorý NVDA počká pred pohybom systémového kurzora (bodu vloženia).
Ak zistíte, že NVDA nesprávne sleduje kurzor, napríklad je o znak pozadu alebo opakuje riadky, môže vám pomôcť zvýšiť tento časový úsek.

##### Oznamovať hodnoty priehľadných farieb {#ReportTransparentColors}

Umožňuje zapnúť oznamovanie priehľadných farieb. Toto je užitočné pre vývojárov doplnkov, ktorí sprístupňujú aplikácie tretích strán.
Niektoré GDI aplikácie označujú text farbou na pozadí, čo sa nvda pokúša identifikovať pomocou display modelu.
V niektorých situáciách môže byť pozadie priehľadné a text sa môže nachádzať v inom prvku. 
Tiež je možné stretnúť sa s tým, že text je zobrazený s priehľadnou farbou, ale vizuálne je farba presná.

##### Na výstup pre reč a zvuky používať rozhranie WASAPI {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Možnosti |Predvolené (zapnuté), Vypnuté, zapnuté|
|Predvolené |Zapnuté|

Táto možnosť umožňuje na posielanie zvukového výstupu z NVDA využiť rozhranie Windows Audio Session API (WASAPI).
Ide o moderné rozhranie, ktoré zlepšuje stabilitu reči a zvukov NVDA.
Zmeny v tomto nastavení sa prejavia až po reštarte NVDA.
Ak odčiarknete možnosť používať WASAPI, nebudú viac dostupné tieto možnosti:

* [Hlasitosť zvukov je rovnaká ako hlasitosť reči](#SoundVolumeFollowsVoice)
* [Hlasitosť zvukov NVDA](#SoundVolume)

##### Úroveň záznamu {#AdvancedSettingsDebugLoggingCategories}

Začiarkávacie políčka v tejto časti umožňujú povoliť dodatočné zaznamenávanie do logu NVDA.
Zapisovanie  týchto správ môže spomaliť NVDA a zvýšiť veľkosť súborov.
Zaznamenávanie týchto správ povoľte, len ak dostanete inštrukcie od vývojárov, napríklad pri diagnostike nefunkčného ovládača brailového riadka.

##### Oznamovať zvukom zaznamenané chyby {#PlayErrorSound}

Ak je zapnuté, NVDA bude zvukom oznamovať situácie, keď do logu zapíše chybu.
Ak zvolíte Len v testovacích verziách NVDA (predvolené), NVDA bude zvuk prehrávať, len ak je spustená alpha, beta, alebo verzia zo zdroja.
Ak vyberiete možnosť áno, bude zvuky NVDA prehrávať nezávisle od spustenej verzie.

##### Regulárny výraz pre navigáciu po textových odsekoch {#TextParagraphRegexEdit}

Tu môžete definovať regulárny výraz, ktorý sa používa na detekciu textových odsekov v režime prehliadania.
Tento regulárny výraz je násedne použitý pri [Navigácii po textových odsekoch](#TextNavigationCommand).

### Ďalšie nastavenia {#MiscSettings}

Okrem rozsiahleho [dialógu nastavení](#NVDASettings), je v ponuke NVDA v časti možnosti viacero položiek, ktorým sa budeme venovať v nasledujúcich riadkoch.

#### Rečové slovníky {#SpeechDictionaries}

Ponuka Rečové slovníky (vnorená v ponuke Možnosti) obsahuje dialógy, v ktorých môžete nastaviť ako bude NVDA vyslovovať konkrétne slová alebo frázy.
Existujú 3 typy rečových slovníkov.
Sú to:

* Predvolený: Pravidlá v tomto slovníku ovplyvnia každý rečový prejav NVDA.
* Slovník pre aktuálny hlas: Slovník, ktorého pravidlá ovplyvnia reč aktuálneho hlasu práve použitého hlasového výstupu.
* Dočasný: Pravidlá v tomto slovníku ovplyvnia každý rečový prejav NVDA ale len počas aktuálneho spustenia NVDA. Po reštarte NVDA sa obsah tohto slovníka stratí.

Ak chcete otvárať  dialógy slovníkov z hociktorého miesta, musíte im priradiť skratky v dialógu [Klávesové skratky](#InputGestures).

Všetky dialógy rečových slovníkov obsahujú zoznam pravidiel spracovania reči.
Nájdete tu tiež tlačidlá Pridať, Upraviť, Odstrániť a odstrániť všetky.

Stlačením tlačidla Pridať a vyplnením dialógu, ktorý sa otvorí pridáte položku do zoznamu pravidiel.
Práve pridané pravidlo sa zobrazí v zozname.
Aby ste si boli istí, že práve pridané pravidlo sa skutočne uloží a vstúpi do platnosti, musíte potom, ako skončíte s úpravami pravidiel, ukončiť dialóg slovníka stlačením tlačidla OK.

Pravidlá pre rečové slovníky NVDA umožňujú zmeniť sled znakov na úplne niečo iné.
Napríklad si predstavte, že chcete aby NVDA povedal slovo "žaba" vždy keď  sa v texte vyskytne slovo "vták".
Najjednoduchšie to docielite, ak v dialógu Upraviť položku slovníka vložíte do poľa Vzor slovo vták a do poľa Nahradiť s slovo žaba.
Aby ste sa v zozname pravidiel nestratili, je vhodné zadať nejaký text vystihujúci aktuálne pravidlo do políčka Komentár. Napríklad: toto mení vyslovovanie slova vták na slovo žaba.

Rečové slovníky NVDA toho dokážu ešte viac než len zamieňať slová.
Dialóg Upraviť položku slovníka obsahuje začiarkavacie políčko Rozlišovať malé a veľké písmená, čím môžete NVDA prinútiť rozlišovať či text je písaný veľkými písmenami alebo nie.
Predvolene NVDA ignoruje veľkosť písmen.

Nasleduje prepínač, ktorým určíte, či sa má výraz použiť ak sa nachádza kdekoľvek, ak je to celé slovo, alebo ide o "regulárny výraz".
Ak nastavíte možnosť Iba celé slová, výraz sa použije len vtedy, ak nie je súčasťou väčšieho slova.
Toto platí, keď pred a za výrazom nenasleduje žiadny alfanumerický znak, alebo podčiarkovník, alebo za a pred výrazom nie sú žiadne znaky a symboly.
Vráťme sa ešte k predchádzajúcemu príkladu, v ktorom sme nahradili výraz "vták" výrazom "žaba". Ak nastavíte prepínač na Iba celé slová, výraz sa nezmení, ak bude v texte výraz "vtáky" alebo "bielyvták".

Regulárny výraz je špeciálny druh vzoru, ktorý umožňuje filtrovať len znaky, len číslice alebo ľubovoľný počet ľubovoľných znakov v rôznych kombináciách.
Regulárne výrazy nie sú popísané v tejto používateľskej príručke.
Odporúčame preštudovať [Použitie regulárnych  výrazov v prostredí Python](https://docs.python.org/3.11/howto/regex.html).

#### Výslovnosť interpunkčných a špeciálnych symbolov {#SymbolPronunciation}

V tomto dialógu môžete nastavovať výslovnosť interpunkčných a ostatných špeciálnych symbolov ako aj úroveň interpunkcie, pri ktorom budú tieto vyslovované.

V názve okna sa zobrazuje jazyk, ktorého symboly upravujete.
Tento dialóg rešpektuje nastavenie "pri spracovaní textu sa riadiť hlasovým výstupom", ktoré je v kategórii  [Nastavenia hlasu](#SpeechSettings) v dialógu [Nastavenia](#NVDASettings). Ak je toto políčko začiarknuté, upravujete nastavenie pre jazyk hlasu a nie jazyk NVDA.

Ak si želáte upraviť symbol, musíte ho najprv vybrať v zozname symbolov.
Zoznam symbolov môžete filtrovať, ak zadáte symbol alebo jeho nahradenie do políčka filtrovať.

* Do poľa nahradiť s môžete vpísať text, ktorý sa má vysloviť vždy, keď bude NVDA čítať tento symbol.
* Zmenou výberu v zozname úrovní môžete určiť najnižšiu úroveň, na ktorej bude symbol oznamovaný (žiadne, niektoré, väčšina, všetko).
Úroveň tiež môžete nastaviť na možnosť znak. V takom prípade bude symbol oznamovaný len v týchto prípadoch:
  * Pri čítaní po znakoch.
  * Pri hláskovaní.
* V zozname "ponechať pôvodný symbol na spracovanie hlasovému výstupu" určíte, kedy má NVDA ponechať pôvodný symbol na spracovanie pre hlasový výstup. Toto sa netýka textu, ktorý ste zvolili v editačnom poli Nahradiť s.
Toto je užitočné vtedy, ak hlasový výstup dokáže pri symbole urobiť prestávku alebo zmeniť intonáciu.
Mnohé syntézy reči napríklad dokážu urobiť pauzu, ak narazia v texte na čiarku.
Máte tri možnosti:
  * nikdy: Symbol sa neodošle na spracovanie hlasovému výstupu.
  * Vždy: NVDa bude vždy symbol posielať na spracovanie hlasovému výstupu.
  * Od zadanej úrovne: Symbol sa odošle na spracovanie len vtedy, ak je aktuálna úroveň interpunkcie nižšia, ako je nastavená úroveň pre tento symbol.
  Takto môžete rozhodnúť, že symbol nahradíte nejakým textom pri úrovni interpunkcie všetko, ale pri úrovni nič, bude symbol odoslaný na spracovanie hlasovému výstupu. Ten ho nahradí pauzou, takže nestratíte prehľad.

Nový symbol môžete pridať tak, že stlačíte tlačidlo pridať.
v dialógu, ktorý sa otvorí, vložte nový symbol a stlačte tlačidlo OK.
Následne nastavte parametre tak, ako pri ostatných symboloch.

Symboly, ktoré ste pridali, môžete odstrániť aktivovaním tlačidla odstrániť.

Ak ste skončili s úpravami, môžete stlačiť tlačidlo OK a uložiť zmeny, alebo tlačidlom Zrušiť zmeny zahodiť.

Ak chcete použiť komplexné symboly, v poli nahradiť je potrebné zadať skupinu znakov, ktoré majú reprezentovať interpretovaný text. Napríklad, ak chceme hľadať celý dátum, budeme očakávať výstup v tvare \1, \2 a \3.
V poli nahradiť potom použijeme odkazy na pamäť, napríklad "\\1".

#### Klávesové skratky {#InputGestures}

V tomto dialógu môžete nastaviť klávesové skratky (klávesy na klávesnici, tlačidlá na brailovom riadku a podobne) pre príkazy NVDA.

V okne sa zobrazujú len skratky, ktoré sú funkčné tesne pred otvorením dialógu.
Ak napríklad chcete nastaviť skratky pre príkazy v režime prehliadania, pred otvorením dialógu musíte byť v režime prehliadania.

V strome sú všetky príkazy NVDA usporiadané podľa kategórií.
Zoznam dostupných funkcii môžete prehľadávať tak, že do poľa filtrovať napíšete slovo alebo viacero slov z názvu funkcie, pričom na poradí slov nezáleží.
Pod každým príkazom nájdete aktívne klávesové skratky.

Ak chcete vytvoriť novú skratku, vyberte požadovaný príkaz a stlačte tlačidlo pridať.
Potom stlačte požadovanú skratku na klávesnici alebo na brailovom riadku.
Jedna skratka môže byť často interpretovaná viacerými spôsobmi.
Ak ste napríklad stlačili klávesy na klávesnici, môžete chcieť, aby skratka fungovala len v jednom rozložení (desktop alebo laptop), alebo aby platila pre všetky rozloženia.
preto sa po zadaní skratky zobrazí menu, v ktorom môžete vybrať požadovanú možnosť.

Ak chcete skratku odstrániť, vyberte ju v strome a stlačte tlačidlo odstrániť.

Vo vetve Emulované klávesy nájdete funkcie, ktoré emulujú klávesové skratky.
Takto môžete odosielať príkazy do systému priamo z brailového riadka.
Ak chcete pridať príkaz, vyberte vetvu Emulované klávesy a aktivujte tlačidlo pridať.
Potom stlačte kláves, ktorý chcete emulovať.
Kláves sa následne objaví vo vetve Emulované klávesy a budete ho môcť priradiť k tlačidlu na brailovom riadku, ako sme popísali vyššie.

Upozornenia:

* Ak pridáte kláves, ale nepriradíte zodpovedajúce tlačidlo na brailovom riadku, kláves sa po opustení dialógu neuloží.
* Skratky s preraďovačmi nemusia fungovať bez preraďovača.
Ak napríklad na písmeno `A`  namapujete skratku `ctrl+m`, vo výsledku môžu aplikácie dostávať príkaz `ctrl+a`.

Keď skončíte, stlačte tlačidlo OK, ktorým nastavenia uložíte, alebo tlačidlo Zrušiť, ktorým dialóg zatvoríte bez uloženia zmien.

### Uloženie a opätovné načítanie konfigurácie {#SavingAndReloading}

NVDA automaticky ukladá vaše nastavenia.
Automatické ukladanie nastavení pri ukončení je možné nastaviť v dialógu Všeobecné nastavenia v podmenu Možnosti.
Nastavenia môžete ručne uložiť potvrdením položky Uložiť nastavenia z ponuky NVDA.

Ak ste pri nastaveniach programu urobili chybu a potrebujete sa vrátiť k uloženým nastaveniam, zvoľte možnosť opätovného načítania nastavení  z ponuky NVDA.
Môžete sa tiež kedykoľvek  vrátiť k predvoleným nastaveniam. Z ponuky NVDA aktivujte položku Obnoviť predvolené nastavenia.

Užitočné môžu byť tiež nasledujúce klávesové skratky:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka pre desktop |Klávesová skratka pre laptop |Popis|
|---|---|---|---|
|Uložiť nastavenia |NVDA+ctrl+c |NVDA+ctrl+c |Uloží aktuálne nastavenia NVDA tak, aby sa pri ukončení nestratili|
|Návrat k uloženým nastaveniam |NVDA+ctrl+r |NVDA+ctrl+r |Obnoví nastavenia z času, čo Ste naposledy konfiguráciu uložili. Stlačené trikrát obnoví predvolené nastavenia.|

<!-- KC:endInclude -->

### Konfiguračné profily {#ConfigurationProfiles}

Niekedy môžete potrebovať rôzne nastavenia pre rôzne situácie.
Môžete napríklad chcieť počuť odsadenie textu pri úpravách, alebo informácie o formátovaní pri korektúre.
NVDA vám umožňuje urobiť takéto nastavenia pomocou konfiguračných profilov.

Konfiguračný profil obsahuje len tie nastavenia, ktoré zmeníte, keď je profil aktívny.
Zmeniť môžete všetky nastavenia okrem tých, ktoré sú v kategórii všeobecné v dialógu [Nastavenia](#NVDASettings), lebo tie sa týkajú NVDA ako celku.

Konfiguračné profily môžete aktivovať ručne z dialógu alebo pomocou klávesovej skratky.
Môžu ich však aktivovať aj rôzne udalosti, ako napríklad prepnutie sa do určitej aplikácie.

#### Základné nastavenie {#ProfilesBasicManagement}

Do nastavení profilov sa dostanete z menu NVDA, aktivovaním položky Konfiguračné profily.
Na otvorenie dialógu môžete tiež použiť klávesovú skratku:
<!-- KC:beginInclude -->

* NVDA+ctrl+p: otvorí dialóg s nastaveniami konfiguračných profilov.

<!-- KC:endInclude -->

Prvým prvkom v tomto dialógu je zoznam dostupných profilov.
Predvolene je vybratý ten profil, ktorý práve upravujete.
Pre aktívny profil sa tiež zobrazujú informácie  o tom, či je aktivovaný ručne, či je aktívna udalosť, ktorá ho spúšťa a či je práve upravovaný.

Ak chcete profil premenovať, alebo odstrániť, aktivujte príslušné tlačidlá.

Tlačidlom zavrieť zatvoríte dialóg.

#### Vytvorenie profilu {#ProfilesCreating}

Aby ste vytvorili nový profil, aktivujte tlačidlo nový.

V dialógu, ktorý sa zobrazí, môžete zadať názov vášho profilu.
Tu tiež môžete vybrať, ako chcete profil používať.
Ak chcete profil spúšťať ručne, vyberte predvolenú možnosť ručná aktivácia.
Ak nie, vyberte udalosť, ktorá spustí tento profil.
Ak ste nedali profilu názov a vyberiete udalosť, automaticky sa názov priradí podľa danej udalosti.
Pre podrobnosti Čítajte [Ďalej](#ConfigProfileTriggers).

tlačidlom OK vytvoríte nový profil a zatvoríte dialóg s profilmi, a hneď môžete nový profil upraviť.

#### Ručná aktivácia {#ConfigProfileManual}

Profil môžete aktivovať jeho vybratím v dialógu konfiguračné profily a aktivovaním tlačidla ručne  aktivovať.
pri aktívnom profile sa môžu aktivovať iné profily, ak nastane udalosť, ktorá ich aktivuje, vždy však budú zohľadnené nastavenia aktívneho profilu.
Ak napríklad máte vytvorený profil pre nejakú aplikáciu, v ktorom ste zapli oznamovanie odkazov, ale aktivujete profil, v ktorom je oznamovanie odkazov vypnuté, NVDA nebude odkazy oznamovať.
Ak však zmeníte nastavenia hlasu v profile pre aplikáciu, ale nezmeníte ich v ručne aktivovanom profile, použijú sa nastavenia hlasu z profilu pre aplikáciu.
Všetky nastavenia, ktoré zmeníte sa ukladajú do ručne aktivovaného profilu.
Ak chcete deaktivovať aktívny profil, v dialógu konfiguračné profily vyberte daný profil a stlačte tlačidlo ručne deaktivovať.

#### Udalosti {#ConfigProfileTriggers}

Ak v dialógu konfiguračné profily aktivujete tlačidlo udalosti, môžete nastaviť, kedy sa majú profily automaticky spúšťať.

Zoznam udalostí zobrazuje dostupné možnosti:

* aktuálna aplikácia: Profil sa automaticky aktivuje po prepnutí do okna aplikácie.
* Plynulé čítanie: profil bude použitý pri plynulom čítaní.

Ak chcete vybrať profil pre danú udalosť, zvoľte požadovanú udalosť a potom zo zoznamu vyberte požadovaný profil.
Môžete tiež vybrať možnosť "(normálna konfigurácia)", ak nechcete použiť pre udalosť žiadny profil.

Tlačidlom zatvoriť sa vrátite do dialógu konfiguračné profily.

#### Upravenie Profilu {#ConfigProfileEditing}

Ak ste ručne aktivovali nejaký profil, všetky nastavenia, ktoré zmeníte, sa uložia do tohto profilu.
V opačnom prípade sa nastavenia uložia do profilu, ktorý bol aktivovaný poslednou udalosťou.
Ak ste si napríklad zviazali profil s poznámkovým blokom a budete v okne poznámkového bloku, všetky zmeny sa uložia do profilu pre poznámkový blok.
Ak nemáte aktívny žiadny profil, ani nie je žiadny profil aktivovaný udalosťou, nastavenia sa zapíšu do normálnej konfigurácie.

Ak chcete upraviť profil pre plynulé čítanie, musíte ho [ručne aktivovať](#ConfigProfileManual).

#### Dočasné vypnutie udalostí {#ConfigProfileDisablingTriggers}

Niekedy môže byť užitočné vypnúť všetky udalosti naraz.
Môžete napríklad chcieť upraviť aktívny profil alebo normálne nastavenia bez toho, aby sa vám nechtiac spustil profil vyvolaný nejakou udalosťou.
toto docielite začiarknutím možnosti dočasne zakázať všetky udalosti v dialógu konfiguračné profily.

Ak chcete dočasne zakázať udalosti klávesovou skratkou, môžete ju nastaviť v dialógu [Klávesové skratky](#InputGestures).

#### Aktivovanie profilu klávesovou skratkou {#ConfigProfileGestures}

Pre každý vytvorený profil môžete vytvoriť jednu alebo viacero klávesových skratiek.
Predvolene NVDA nevytvára žiadne klávesové skratky pre profily.
Klávesové skratky k profilu priradíte v dialógu [Klávesové skratky](#InputGestures).
Každý profil má samostatnú vetvu v strome Konfiguračné profily.
Klávesové skratky sa zachovajú aj vtedy, ak profil premenujete.
Ak odstránite profil, automaticky sa odstráni aj klávesová skratka.

### Umiestnenie súborov s nastaveniami {#LocationOfConfigurationFiles}

Prenosné verzie NVDA si ukladajú všetky nastavenia, vlastné aplikačné moduly, ovládače hlasových a brailových výstupov v podpriečinku userConfig v priečinku NVDA.

Nainštalované verzie NVDA si ukladajú všetky nastavenia, vlastné aplikačné moduly, ovládače hlasových a brailových výstupov v špecifickom priečinku NVDA v používateľskom profile Windows.
Znamená to, že každý používateľ Windows môže mať svoje nastavenia NVDA.
Môžete si nastaviť skratku na otvorenie adresára s nastaveniami v dialógu [Klávesové skratky](#InputGestures).
Vstúpiť do svojho priečinka s nastaveniami nainštalovanej verzie NVDA môžete tiež cez odkaz Otvoriť adresár s používateľskými nastaveniami v ponuke štart, v priečinku Programy > NVDA.

Nastavenia, ktoré sa použijú v prípadoch, keď NVDA beží na prihlasovacej alebo inej zabezpečenej obrazovke, sú uložené v priečinku systemConfig, ktorý je podpriečinkom inštalačného adresára NVDA.
Normálne nie je potrebné do tohto priečinka zasahovať.
Ak chcete zmeniť konfiguráciu NVDA pre prihlasovaciu obrazovku, nakonfigurujte NVDA podľa vašich predstáv kým ste prihlásení do Windows. Následne uložte nastavenia a potom pomocou tlačidla v kategórii  Všeobecné v dialógu [Nastavenia](#NVDASettings) skopírujte vaše nastavenia na prihlasovaciu obrazovku.

## Doplnky a katalóg s doplnkami {#AddonsManager}

Doplnky umožňujú doplniť do NVDA nové funkcie, alebo pozmeniť existujúce funkcie NVDA.
Vyvýja ich komunita okolo NVDA, ale aj externé prípadne aj komerčné organizácie.
Doplnky môžu robiť nasledovné:

* Pridať alebo zlepšiť podporu pre rôzne aplikácie.
* Poskytovať podporu pre nové brailové riadky a hlasové výstupi.
* Pridávať alebo meniť funkcionalitu NVDA.

Katalóg s doplnkami umožňuje prehľadávať a spravovať doplnky.
Všetky doplnky sú poskytované zdarma.
Niektoré však môžu vyžadovať zakúpenie licencie alebo kúpu dodatočného software, aby ste ich mohli používať.
Najčastejšie sa s tým môžete stretnúť pri doplnkoch k syntézam reči.
Ak nainštalujete doplnok, ktorý vyžaduje platbu a rozmyslíte si to, doplnok môžete jednoducho odinštalovať.

Katalóg s doplnkami môžete nájsť v menu NVDA > Nástroje.
Ak chcete mať ku katalógu prístup odkiaľkoľvek, môžete si vytvoriť skratku v [dialógu klávesové skratky](#InputGestures).

### Prechádzanie doplnkov {#AddonStoreBrowsing}

Po otvorení katalógu sa zobrazí zoznam doplnkov.
Ak ešte nemáte nainštalované žiadne doplnky, v zozname sa zobrazia dostupné doplnky.
Ak už nejaké doplnky máte nainštalované, zobrazia sa aktuálne nainštalované doplnky.

Ak šípkami hore a dole zvolíte nejaký doplnok, zobrazia sa informácie o ňom.
S každým doplnkom môžete vykonať niekoľko akcií, ktoré sú dostupné v [menu akcie](#AddonStoreActions), ako napríklad inštalovať, pomocník, zakázať a odstrániť.
Dostupné akcie sa môžu meniť v závislosti od toho, či je doplnok už nainštalovaný alebo povolený.

#### Možnosti zobrazenia doplnkov {#AddonStoreFilterStatus}

Môžete si zobraziť zoznam nainštalovaných doplnkov, doplnkov, pre ktoré sú dostupné aktualizácie, zoznam dostupných alebo nekompatibilných doplnkov.
Medzi týmito zobrazeniami sa prepínajte ako medzi záložkami, skratkou  `ctrl+tab`.
Môžete tiež klávesom `tab` prejsť na zoznam záložiek a následne medzi nimi prechádzať `ľavou šípkou` a `pravou šípkou`.

#### Filtrovanie povolených a zakázaných doplnkov {#AddonStoreFilterEnabled}

Predvolene je nainštalovaný doplnok aj povolený, čo znamená, že je spustený a dostupný v NVDA.
Niektoré nainštalované doplnky však môžu byť zakázané.
To znamená, že nie sú spustené a ich funkcionalita aktuálne nie je dostupná.
Doplnok môžete zakázať napríklad vtedy, ak je v konflikte s iným doplnkom, alebo aplikáciou.
NVDA tiež môže zakázať doplnky, ktoré sa ukážu ako nekompatibilné s aktuálnou verziou nvda. Vždy však na to upozorní.
Doplnky môžete tiež zakázať, ak ich dlhší čas nepoužívate, zároveň si ich ale chcete ponechať dostupné na neskôr.

Zoznam nainštalovaných alebo nekompatibilných doplnkov je možné filtrovať podľa toho, či sú zakázané alebo povolené.
Predvolene sa zobrazujú aj zakázané aj povolené doplnky.

#### Ukázať nekompatibilné doplnky {#AddonStoreFilterIncompatible}

Doplnky, ktoré ešte nie sú nainštalované, alebo doplnky, pre ktoré je dostupná aktualizácia, je možné zobraziť aj v prípade, že [nie sú kompatibilné](#incompatibleAddonsManager) s aktuálnou verziou NVDA.

#### Filtrovanie doplnkov podľa zdroja {#AddonStoreFilterChannel}

Doplnky sú distribuované zo štyroch zdrojov:

* Stabilné: Vývojár doplnku uvoľnil doplnok ako funkčný a otestovaný doplnok, pričom ho otestoval s najnovšou stabilnou verziou NVDA.
* Beta: Doplnok vyžaduje ešte testovanie a očakáva sa práve odozva od používateľov.
Tieto doplnky sú vhodné pre tých, ktorí radi testujú nové funkcie.
* Vo vývoji: Tento zdroj je určený pre vývojárov doplnkov, ktorí testujú nové rozhrania.
Tento zdroj tiež využívajú používatelia NVDA vo verzii Alpha.
* Externé: Ide o doplnky, ktoré sú nainštalované z externého zdroja, mimo katalógu s doplnkami NVDA.

Ak chcete zobraziť doplnky len z konkrétneho zdroja, nastavte ho v zozname zdroj.

#### Vyhľadávanie doplnkov {#AddonStoreFilterSearch}

Na vyhľadávanie doplnkov použite editačné pole vyhľadávanie.
Môžete ho rýchlo nájsť, ak v zozname s doplnkami stlačíte `shift+tab`.
Zadajte kľúčové slová, alebo názov doplnku. Potom klávesom `tab` prejdite do zoznamu s doplnkami.
Doplnky sa zobrazia v zozname, ak sa podarilo nájsť reťazec v názve doplnku, v názve vydavateľa, V identifikátore alebo v popise doplnku.

### Akcie {#AddonStoreActions}

Ku každému doplnku sú asociované akcie, ako napríklad inštalovať, pomocník, zakázať a odstrániť.
Zoznam akcií je možné vyvolať priamo na konkrétnom doplnku po stlačení `klávesu s kontextovým menu`, klávesom `enter`, dvojitým kliknutím ľavého tlačidla myši, alebo kliknutím pravým tlačidlom myši.
Tiež môžete aktivovať tlačidlo akcie v podrobnostiach doplnku.

#### Inštalovanie doplnkov {#AddonStoreInstalling}

To, že je doplnok dostupný v katalógu neznamená, že ho NV Access alebo ktokoľvek iný preveril a odporúča používať.
Je veľmi dôležité, aby ste inštalovali doplnky z overených zdrojov.
Funkcie doplnkov nie sú nijako obmedzené.
Doplnky môžu mať prístup k vašim osobným údajom aj celému systému.

Doplnky môžete inštalovať a aktualizovať [prechádzaním dostupných doplnkov](#AddonStoreBrowsing).
Vyberte doplnok na záložke dostupné doplnky, alebo dostupné aktualizácie doplnkov.
Následne z menu akcie zvoľte možnosť aktualizovať alebo nainštalovať.

Je tiež možné nainštalovať viacero doplnkov súčasne.
Najprv označte požadované doplnky na záložke dostupných doplnkov, následne z kontextovej ponuky aktivujte možnosť "nainštalovať vybraté doplnky".

Ak máte doplnok mimo katalógu a chcete ho nainštalovať, aktivujte tlačidlo "Inštalovať z externého zdroja".
Toto zobrazí štandardný dialóg systému Windows, pomocou ktorého môžete vyhľadať na vašom disku alebo na sieti doplnok (súbor s príponou `.nvda-addon`).
Po otvorení súboru sa spustí inštalácia doplnku.

Ak je NVDA nainštalované a spustené, môžete inštaláciu doplnku spustiť aj tak, že priamo v správcovi súborov otvoríte súbor s doplnkom.

Ak inštalujete doplnok z externého zdroja, NVDA sa opýta, či skutočne chcete pokračovať.
Aby doplnok začal po inštalácii fungovať, je potrebné reštartovať NVDA. Reštartovať môžete aj neskôr, ak máte v pláne inštalovať alebo aktualizovať aj ďalšie doplnky.

#### Odstránenie doplnkov {#AddonStoreRemoving}

Ak chcete odstrániť doplnok, zvoľte ho v zozname doplnkov a z menu akcie aktivujte položku odstrániť.
NVDA sa opýta, či skutočne chcete doplnok odstrániť.
Rovnako ako pri inštalácii, aj odstránenie doplnku sa vykoná až po reštarte NVDA.
Kým tak urobíte, zobrazí sa pri doplnku v časti stav informácia, že bude odstránený po reštarte.
Rovnako ako pri inštalácii, aj pri odstraňovaní doplnkov je možné vybrať a odstrániť viacero doplnkov súčasne.

#### Zakázanie a povolenie doplnkov {#AddonStoreDisablingEnabling}

Ak chcete zakázať doplnok, z menu akcie aktivujte položku "zakázať".
Ak chcete povoliť doplnok, ktorý ste zakázali, z menu akcie aktivujte položku "povoliť".
Doplnok môžete zakázať, ak je v časti stav napísané, že je povolený. Opačne, ak je v časti stav napísané, že je zakázaný, môžete ho povoliť.
V časti stav sa zobrazuje, čo sa s doplnkom stane pri najbližšom reštarte NVDA.
Ak bol doplnok zakázaný a aktivujete položku povoliť, stav sa zmení na "bude povolený po reštarte".
Ak bol doplnok povolený a aktivujete položku zakázať, v časti stav sa zobrazí "bude zakázaný po reštarte".
Aj v tomto prípade sa všetky zmeny prejavia až po reštarte NVDA.
Je tiež možné naraz zakázať a povoliť viacero doplnkov. V zozname doplnkov vyberte požadované doplnky a následne v kontextovej ponuke aktivujte príslušnú možnosť.

#### Hodnotenie doplnkov a čítanie komentárov komunity {#AddonStoreReviews}

Pred inštaláciou a používaním  doplnku si môžete pozrieť, ako doplnok hodnotia ostatní používatelia.
Rovnako môžete aj vy poskytnúť spätnú väzbu k doplnkom, ktoré používate alebo ste ich vyskúšali.
Ak si chcete pozrieť hodnotenia a recenzie, vyberte požadovaný doplnok na záložke dostupné doplnky alebo dostupné aktualizácie doplnkov a v kontextovej ponuke aktivujte položku "komentáre komunity".
Otvorí sa diskusia na GitHube, kde je možné čítať a písať komentáre (anglicky).
Upozorňujeme, že toto nenahrádza priamu komunikáciu s vývojárom doplnkov.
Odporúčame využívať tento spôsob na získanie informácie, či je doplnok pre vás užitočný.

### Nekompatibilné doplnky {#incompatibleAddonsManager}

Staršie doplnky už nemusia byť kompatibilné s verziou NVDA, ktorú používate.
Opačne, ak používate staršiu verziu NVDA, novšie doplnky tiež nemusia byť kompatibilné.
Pri pokuse nainštalovať nekompatibilný doplnok sa objaví varovanie, ktoré upozorní na nekompatibilitu.

Staršie doplnky môžete povoliť na vlastné riziko.
Nekompatibilné doplnky nemusia pracovať správne a môžu spôsobiť nestabilitu, nečakané správanie a pády NVDA.
Varovanie o kompatibilite môžete ignorovať priamo počas inštalácie alebo povolenia doplnku.
Ak zistíte, že doplnok spôsobuje problémy, môžete ho neskôr zakázať alebo odstrániť.

Ak ste zaznamenali problémy práve po inštalácii alebo aktualizácii doplnku, hlavne ak išlo o nekompatibilný doplnok, môžete NVDA spustiť v režime bez doplnkov.
Ak chcete NVDA reštartovať a zakázať doplnky, zvoľte príslušnú možnosť v dialógu Ukončiť NVDA.
Prípadne, použite na [príkazovom riadku](#CommandLineOptions) parameter `--disable-addons`.

Dostupné nekompatibilné doplnky je možné zobraziť na záložkách [Dostupné doplnky a dostupné aktualizácie doplnkov](#AddonStoreFilterStatus).
Nekompatibilné doplnky je možné zobraziť na záložke [Nainštalované nekompatibilné doplnky](#AddonStoreFilterStatus).

## Ďalšie nástroje {#ExtraTools}
### Zobraziť log {#LogViewer}

Zobrazovač logu, ktorý je možné spustiť z podmenu nástroje, dokáže zobraziť všetok zápis do súboru log, ktorý sa zaznamenal od posledného štartu NVDA.

Okrem čítania záznamu je možné záznam uložiť, alebo obnoviť zobrazenie a načítať tak záznam, ktorý sa zapísal, kým bol zobrazovač spustený.
Tieto funkcie sú dostupné v menu log.

Súbor so záznamom sa ukladá do súboru `%temp%\nvda.log`.
Nový záznam sa vytvorí vždy po štarte NVDA.
Predošlý záznam je presunutý do súboru `%temp%\nvda-old.log`.

Je tiež možné do schránky skopírovať len časť záznamu, ktorú považujete za dôležitú. Napríklad ak zaznamenávate konkrétny problém a chcete sledovať záznam v konkrétnom čase.
<!-- KC:beginInclude -->

| názov |klávesová skratka |popis|
|---|---|---|
|Zobraziť záznam |`NVDA+f1` |Otvorí záznam a zapíše doň informácie o práve zameranom objekte.|
|Skopírovať fragment záznamu do schránky |`NVDA+ctrl+shift+f1` |Po prvom stlačení sa určí miesto v zázname, od ktorého sa bude sledovať zápis. Po druhom stlačení bude od tohto miesta po súčasnosť záznam skopírovaný do schránky.|

<!-- KC:endInclude -->

### Zobrazovač reči {#SpeechViewer}

Pre vidiacich vývojárov software alebo pre ľudí, ktorí predstavujú NVDA vidiacim záujemcom, existuje plávajúce okno, ktoré zobrazuje všetok text, čo NVDA posiela hlasovému výstupu.

Zobrazovač reči je možné aktivovať začiarknutím rovnomennej položky v podmenu nástroje.
Deaktivovať ho môžete odčiarknutím tej istej položky.

v okne zobrazovača reči nájdete aj začiarkávacie pole "spustiť pri štarte Zobrazovač reči".
ak ho začiarknete, zobrazovač reči sa spustí vždy po spustení NVDA.
Okno sa bude otvárať vždy na tom mieste a s tými hodnotami, s akými ste ho naposledy zatvorili.

Zatiaľ, čo je zobrazovač reči aktívny, Jeho obsah sa neustále aktualizuje s práve čítaným textom.
Pozastaviť zobrazovanie aktuálneho textu (napr. užitočné pre kopírovanie) je možné kliknutím, prepnutím fokusu alebo prejdením myšou v okne zobrazovač reči.

Ak potrebujete Zobrazovač reči spúšťať z hociktorého miesta, môžete mu priradiť  skratku v dialógu [Klávesové skratky](#InputGestures).

### Zobrazovač braillu {#BrailleViewer}

Ak ste vidiaci vývojár software, alebo chcete predvádzať funkcionalitu NVDA vidiacej verejnosti, máte k dispozícii plávajúce okno, v ktorom sa zobrazí brailový výstup a tiež textová reprezentácia každého brailového znaku.
Zobrazovač Braillu môžete používať súčasne s fyzickým brailovým riadkom. Zobrazenie sa prispôsobí fyzickému počtu buniek na riadku.
Keď je aktívny zobrazovač braillu, v plávajúcom okne sa stále zobrazuje to, čo by inak bolo premietnuté na brailový riadok.

Zobrazovač Braillu zapnete začiarknutím položky Zobrazovač braillu v menu nástroje v ponuke NVDA.
Odčiarknutím tej istej položky zobrazenie vypnete.

Fyzické brailové riadky používajú na posúvanie obsahu tlačidlá. Ak chcete podobnú funkciu dosiahnuť so zobrazovačom braillu, v dialógu [Klávesové skratky](#InputGestures) nastavte skratky na posunutie riadka dopredu a dozadu.

V okne s brailovým zobrazením je aj začiarkávacie pole "spustiť zobrazovač braillu pri štarte".
Po začiarknutí sa bude zobrazovač braillu spúšťať pri každom spustení NVDA.
NVDA sa pokúsi okno zobrazovača otvoriť na rovnakom mieste a v rovnakom pomere v akom bolo naposledy.

V okne brailového zobrazovača je možné začiarknuť možnosť "Pridržanie myši simuluje presunutie na znak". Predvolene je táto možnosť vypnutá.
Ak je táto možnosť zapnutá, potom pridržanie kurzora myši nad brailovým znakom spustí funkciu presunúť na znak.
Toto sa často používa na presunutie systémového kurzora, prípadne aktivovanie prvku.
Funkcionalitu využijete, keď chcete vyskúšať, či správne funguje presúvanie kurzora na znak pomocou fyzických tlačidiel brailového riadka a súčasne riadok nemáte pripojený.
Aby sa zabránilo ustavičnému spúšťaniu prechodu na znak, pridržanie myšy funguje ako semafor:
Funkcia sa spustí až vtedy, keď sa farba znaku zmení na zelenú.
Po pridržaní kurzora myši je farba žltá, následne sa zmení na oranžovú a napokon na zelenú.

Ak chcete zobrazovač brailu aktivovať kedykoľvek klávesovou skratkou, môžete ju nastaviť [V dialógu klávesové skratky](#InputGestures).

### Python konzola {#PythonConsole}

Python konzola programu NVDA, dostupná z podmenu nástroje, je nástroj pre vývojárov, ktorý umožňuje kontrolovať správnosť behu NVDA, zisťovať stav vnútorných premenných NVDA a tiež skúmať hierarchiu prístupnosti aplikácií.
Viac informácií je dostupných v príručke pre vývojárov, ktorú nájdete na stránke NVDA v časti [vývoj (anglicky)](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Katalóg s doplnkami {#AddonStoreMenuItem}

Toto otvorí dialóg [Katalóg s doplnkami](#AddonsManager).
Podrobnosti sú popísané v kapitole [Doplnky a katalóg s doplnkami](#AddonsManager).

### Vytvoriť prenosnú verziu {#CreatePortableCopy}

Umožní z aktuálne spustenej kópie NVDA vytvoriť prenosnú verziu.
Ak je už spustená prenosná verzia, položka funguje opačne a umožní z prenosnej verzie nainštalovať NVDA do systému.

V prvom kroku je potrebné vybrať priečinok, do ktorého sa uloží prenosná verzia, alebo do ktorého sa NVDA nainštaluje.

V tomto dialógu tiež môžete zapnúť a vypnúť tieto možnosti:

* Skopírovať aktuálne používateľské nastavenia (toto zahŕňa súbory z priečinka %appdata%\roaming\nvda alebo súbory z priečinka s nastaveniami prenosnej verzie, vrátane doplnkov a modulov)
* Po dokončení spustiť (po vytvorení prenosnej verzie rovno spustí prenosnú verziu alebo po nainštalovaní automaticky  spustíNVDA zo systému)

### Spustiť opravný nástroj COM... {#RunCOMRegistrationFixingTool}

Počas inštalácie alebo odinštalácie programov sa niekedy stáva, že dôjde k odregistrovaniu knižníc COM DLL.
Rozhrania COM ako napríklad  IAccessible sú závislé na správnej registrácii knižníc a ak nie sú knižnice registrované, môžu nastávať problémi.

Toto zvyčajne nastáva po nainštalovaní a odinštalovaní programov ako Adobe Reader, Math Player a podobne.

Chýbajúce registrácie môžu spôsobovať problémi pri práci s webovými prehliadačmi, desktopovými aplikáciami, panelmi úloh a podobne.

Nástroj použite, ak nastanú tieto situácie:

* NVDA v prehliadačoch Firefox a Thunderbird pri navigácii hlási "neznáme"
* NVDA nedokáže prepínať medzi režimom fokusu a režimom prehliadania
* NVDA zaostáva pri navigácii po webových stránkach
* Iné problémi.

### Načítať pluginy {#ReloadPlugins}

Po aktivovaní tejto položky NVDA znovu načíta pluginy a aplikačné moduly bez nutnosti reštartu. Môže byť užitočné pre vývojárov.
Aplikačné moduly prispôsobujú správanie NVDA v konkrétnych aplikáciách.
Globálne pluginy ovplyvňujú správanie NVDA naprieč aplikáciami.

Do pozornosti dávame tieto klávesové skratky:
<!-- KC:beginInclude -->

| Názov |klávesová skratka |popis|
|---|---|---|
|Znovu Načítať pluginy |`NVDA+ctrl+f3` |Znovu načíta aplikačné moduly a pluginy.|
|Oznámiť aktívny aplikačný modul a názov spustenej aplikácie |`NVDA+ctrl+f1` |Oznámi názov aktívneho aplikačného modulu, ak je aktívny, a tiež názov spustej aplikácie, ktorá má fokus.|

<!-- KC:endInclude -->

## Podporované hlasové výstupy {#SupportedSpeechSynths}

Táto časť obsahuje informácie o hlasových výstupoch, ktoré môžete používať s NVDA.
Zoznam niektorých konkrétnych hlasových výstupov, ktoré je možné používať s NVDA nájdete v časti [Hlasové výstupy (anglicky)](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

Hlasový výstup [eSpeak NG](https://github.com/espeak-ng/espeak-ng) je priamo zabudovaný do NVDA a nie je závislý na iných špeciálnych ovládačoch alebo iných komponentoch, ktoré by bolo potrebné doinštalovať.
V systéme Windows 8.1 NVDA používa  eSpeak NG ako predvolený hlasový výstup. ([Hlasy Windows OneCore](#OneCore) sa používajú predvolene v systéme Windows od verzie 10).
Tento hlas by mal pracovať na každom systéme, kde beží NVDA, čo znamená, že NVDA môžete spúšťať na ľubovoľnom počítači dokonca aj z USB kľúča alebo iného prenosného média.

Každý hlas hlasového výstupu eSpeak NG hovorí iným jazykom.
eSpeak NG pozostáva z viacej než 43 hlasov pre rôzne jazyky.

Existuje tiež množstvo variantov, ktorými je možné zmeniť vlastnosti zvuku aktuálneho hlasu.

### Microsoft Speech API verzia 4 (SAPI 4) {#SAPI4}

SAPI 4 je starší štandard vyvinutý v spoločnosti Microsoft, ktorý slúži na obsluhu softwarových hlasových výstupov v systéme Windows.
NVDA stále podporuje tento hlasový výstup.
Spoločnosť Microsoft však už ukončila podporu pre SAPI4 a potrebné komponenty viac neponúka na svojej webovej stránke.

Po použití ovládača hlasových výstupov SAPI 4 bude zoznam hlasov (prístupný z [Kategórií   reč](#SpeechSettings) [NVDA Settings](#NVDASettings) v [Nastaveniach NVDA](#NVDASettings) alebo v [kruhu nastavení hlasového výstupu](#SynthSettingsRing)) obsahovať všetky SAPI 4 hlasy nainštalované v systéme.

### Microsoft Speech API verzia 5 (SAPI 5) {#SAPI5}

SAPI 5 je štandard vyvinutý v spoločnosti Microsoft, ktorý slúži na obsluhu softwarových hlasových výstupov v systéme Windows.
Množstvo hlasových výstupov kompatibilných s týmto štandardom je možné kúpiť alebo stiahnuť zadarmo od rôznych dodávateľov alebo z rôznych webových stránok, ale v systéme už pravdepodobne máte aspoň jeden SAPI 5 kompatibilný hlas nainštalovaný.
Po použití ovládača hlasových výstupov SAPI 5 bude zoznam hlasov (prístupný z [Kategórií   reč](#SpeechSettings) [NVDA Settings](#NVDASettings) v [Nastaveniach NVDA](#NVDASettings) alebo v [kruhu nastavení hlasového výstupu](#SynthSettingsRing)) obsahovať všetky SAPI 4 hlasy nainštalované v systéme.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Platforma Microsoft Speech poskytuje TTS služby pre rôzne jazyky. Štandardne sa tieto hlasy používajú pri vývoji serverových TTS aplikácií.
Tieto hlasy je možné použiť aj s NVDA.

Aby Ste mohli používať tieto hlasy, je potrebné nainštalovať dva komponenty:

* [Microsoft Speech Platform - Runtime (Verzia 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime jazyky (Verzia 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Tu nájdete súbory pre prevod textu na reč a tiež pre rozpoznávanie reči.
 Vyberte súbor, ktorý obsahuje dáta pre vami požadovaný jazyk / hlas.
 Napríklad súbor MSSpeech_TTS_en-US_ZiraPro.msi obsahuje dáta pre americký hlas.

### Hlasy OneCore {#OneCore}

Operačný systém windows od verzie 10 obsahuje hlasy označené ako "one core" alebo "mobile".
hlasy sú dostupné pre mnoho jazykov (vrátane Slovenčiny a Češtiny) a často majú lepšiu odozvu ako hlasy v rozhraní Sapi5.
NVDA používa Hlasy Onecore predvolene v systémoch Windows od verzie 10. ([eSpeak NG](#eSpeakNG) sa používa v starších systémoch).

Ak chcete nainštalovať nový hlas, otvorte nastavenia systému (windows+i), tu hľadajte kategóriu čas a jazyk a následne sekciu reč. Môžete samozrejme prejsť priamo do tejto sekcie cez vyhľadávanie.
Aktivujte tlačidlo Pridať hlasy.
Pre mnohé jazyky je dostupných viacero hlasov. (Poznámka prekladateľa: V Slovenčine je dostupný hlas Filip, v Češtine hlas Jakub).
Môžete si nainštalovať Austrálsku alebo britskú angličtinu.
Pre Francúzštinu sú dostupné verzie Francúzsko, Kanada a Švajčiarsko.
Vyhľadajte príslušné jazyky a potom ich varianty.
Vyberte jazyky klávesom enter a potvrďte inštaláciu tlačidlom Pridať.
Aby sa prejavili zmeny, reštartujte NVDA.

Pozrite si prosím [Podporované jazyky a hlasy (anglicky)](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) pre zoznam dostupných hlasov.

## Podporované brailové zobrazovače {#SupportedBrailleDisplays}

Táto sekcia obsahuje informácie o brailových zobrazovačoch, ktoré môžete používať s NVDA.

### Riadky, ktoré NVDA dokáže automaticky rozpoznať {#AutomaticDetection}

NVDA dokáže rozpoznať a automaticky používať mnoho brailových riadkov, ktoré pripojíte cez USB alebo Bluetooth.
Stačí, ak ako brailový riadok zvolíte možnosť "automaticky". Nastavenie vykonáte v dialógu [Braillovo písmo](#BrailleSettings).
NVDA predvolene automaticky vyhľadáva a pripája brailové riadky na pozadí.

Funkcia aktuálne funguje s týmito riadkami:

* Handy Tech
* Baum/Humanware/APH/Orbit
* HumanWare Brailliant BI/B
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille
* Eurobraille Esys/Esytime/Iris
* Brailové riadky Nattiq nBraille
* Zápisníky Seika: MiniSeika (16, 24 buniek), V6, a V6Pro (40 buniek)
* Riadky Tivomatic Caiku Albatross 46/80
* Všetky brailové riadky podporujúce štandard HID

### Riadky Focus/PAC Mate od spoločnosti Freedom Scientific {#FreedomScientificFocus}

Podporované sú všetky brailové riadky Focus a PAC Mate od spoločnosti [Freedom Scientific](https://www.freedomscientific.com/), ktoré sú k počítaču pripojené cez USB alebo bluetooth.
Pre správnu funkčnosť musíte mať v systéme nainštalované ovládače brailových riadkov Freedom scientific.
Ak ich ešte nemáte, je možné ich získať zo stránky [Focus Blue](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Aj keď na stránke sa píše len o riadku Focus Blue, ovládač spolupracuje so všetkými zobrazovačmi Freedom scientific.

NVDA sa dokáže predvolene k týmto zobrazovačom pripojiť cez USB alebo Bluetooth rozhranie.
Môžete však samy určiť typ pripojenia a obmedziť ho len na pripojenie cez "USB" alebo "bluetooth".
Toto je užitočné, ak chcete nabiť riadok cez USb, ale chcete ho používať cez Bluetooth.
NVDA dokáže automaticky rozpoznať tieto riadky, ak sú pripojené cez USB alebo Bluetooth.

Nasleduje zoznam klávesových príkazov pre tento typ riadku.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |topRouting1 (prvý znak na riadku)|
|Posunúť riadok vpred |topRouting20/40/80 (posledný znak na riadku)|
|Posunúť riadok späť |leftAdvanceBar|
|Posunúť riadok vpred |rightAdvanceBar|
|Prepnúť nastavenie brailový kurzor zviazaný s |ľavé GDF tlačidlo+pravé GDF tlačidlo|
|Prepnúť akciu ľavého kolieska |Stlačenie ľavého kolieska|
|posunúť späť pomocou ľavého kolieska |ľavé koliesko hore|
|Posunúť vpred použitím ľavého kolieska |ľavé koliesko dolu|
|Prepnúť akciu pravého kolieska |Stlačenie pravého kolieska|
|posunúť späť pomocou pravého kolieska |pravé koliesko hore|
|Posunúť vpred použitím pravého kolieska |pravé koliesko dolu|
|Prejsť na znak v brailly |smerové tlačidlá|
|shift+tab |brailová medzera+body 1,2|
|tab |brailová medzera +body 4,5|
|šípka hore |brailová medzera +bod 1|
|šípka dole |brailová medzera +bod 4|
|ctrl+šípka vľavo |brailová medzera +bod 2|
|ctrl+šípka vpravo |brailová medzera +bod 5|
|šípka vľavo |brailová medzera +bod 3|
|šípka vpravo |brailová medzera+bod6|
|home |brailová medzera +body 1,3|
|end |brailová medzera+body 4,6|
|ctrl+home |brailová medzera+body 1,2,3|
|ctrl+end |brailová medzera+body 4,5,6|
|alt |brailová medzera+body 1,3,4|
|alt+tab |brailová medzera+body 2,3,4,5|
|alt+shift+tab |brailová medzera + body 1256|
|windows+tab |brailová medzera +body 234|
|escape |brailová medzera+body 1,5|
|kláves windows |brailová medzera+body2,4,5,6|
|medzera |brailová medzera|
|Kláves ctrl |brailová medzera +dbody3+body8|
|Kláves alt |brailová medzera+bod6+bod8|
|Kláves Windows |brailová medzera+bod4+bod8|
|Kláves NVDA |brailová medzera+bod5+bod8|
|Kláves Shift |brailová medzera+bod7+bod8|
|Klávesy ctrl+shift |brailová medzera+bod3+bod7+bod8|
|Klávesy alt+shift |brailová medzera+bod6+bod7+bod8|
|klávesy windows+shift |brailová medzera+bod4+bod7+bod8|
|Klávesy nvda+shift |brailová medzera+bod5+bod7+bod8|
|Klávesy ctrl+alt |brailová medzera+bod3+bod6+bod8|
|Klávesy ctrl+alt+shift |brailová medzera+bod3+bod6+bod7+bod8|
|windows+d (minimalizovať všetky aplikácie) |brailová medzera +body 1,2,3,4,5,6|
|prečítaj aktuálny riadok |brailová medzera+body 1,4|
|Ponuka NVDA |brailová medzera+body 1,3,4,5|

Nové modely brailových riadkov (focus 40, focus 80 a focus blue), ktoré majú tzv. rocker bars:

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |leftRockerBarUp, rightRockerBarUp|
|Posunúť riadok vpred |leftRockerBarDown, rightRockerBarDown|

Len pre riadok Focus 80:

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |leftBumperBarUp, rightBumperBarUp|
|Posunúť riadok vpred |leftBumperBarDown, rightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA 6 series/protocol converter {#OptelecALVA}

Podporované sú oba zobrazovače od [Optelec](https://www.optelec.com/) pripojené cez USB a bluetooth, aj ALVA BC640 aj BC680.
ak máte starší riadok, napríklad Braille Voyager, môžete ho pripojiť pomocou rozhrania protocol converter od Optelec.
Na ich používanie nie je potrebné inštalovať žiadne ovládače.
Stačí zapojiť riadok a nastaviť NVDA na jeho používanie.

Upozorňujeme, že v niektorých prípadoch NVDA nedokáže správne identifikovať riadok ALVA BC6. Toto sa stáva vtedy, ak ste na spárovanie zariadenia cez Bluetooth použili ALVA Bluetooth utility.
problém vyriešite tak, že riadok spárujete cez štandardné rozhranie bluetooth v systéme Windows.

Upozorňujeme, že Tieto riadky umožňujú písanie pomocou vstavanej brailovej klávesnice, avšak používajú vlastné nastavenie vstupnej prekladovej tabuľky.
Nastavenie vstupnej prekladovej tabuľky v NVDA preto nemá na vstup z brailovej klávesnice tohto typu riadku v predvolenom nastavení žiadny vplyv.
Ak používate riadok s najnovším firmwérom, je možné vypnúť simuláciu HID klávesnice. Klávesovú skratku na vypnutie a zapnutie HID klávesnice nastavíte v dialógu klávesové skratky.

Nasleduje zoznam klávesových príkazov pre tento typ riadku.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |t1, etouch1|
|predchádzajúci riadok |t2|
|Presunúť na fokus |t3|
|nasledujúci riadok |t4|
|posunúť riadok vpred |t5, etouch3|
|Prejsť na znak v brailly |smerové tlačidlá|
|Oznámiť formátovanie pod aktuálnym  brailovým znakom |sekundárne smerové tlačidlá|
|Prepnúť simuláciu HID klávesnice |t1+spEnter|
|presunúť na prvý riadok v režime prezerania |t1+t2|
|Presunúť na posledný riadok v režime prezerania |t4+t5|
|prepnúť funkciu brailový kurzor zviazaný s |t1+t3|
|oznámiť názov okna |etouch2|
|oznámiť stavový riadok |etouch4|
|emulácia shift+tab |sp1|
|emulácia alt |sp2, alt|
|emulácia escape |sp3|
|emulácia tab |sp4|
|šípka hore |spUp|
|šípka dolu |spDown|
|šípka vľavo |spLeft|
|šípka vpravo |spRight|
|enter |spEnter, Enter|
|oznámiť dátum a čas |sp2+sp3|
|ponuka NVDA |sp1+sp3|
|klávesová skratka windows+d (minimalizovať všetky aplikácie) |sp1+sp4|
|windows+b (prechod na systémovú lištu) |sp3+sp4|
|kláves windows |sp1+sp2, Windows|
|klávesová skratka alt+tab |sp2+sp4|
|ctrl+home |t3+spUp|
|ctrl+end |t3+spDown|
|home |t3+spLeft|
|end |t3+spRight|
|ctrl |ctrl|

<!-- KC:endInclude -->

### Zobrazovače od spoločnosti Handy Tech {#HandyTech}

NVDA podporuje väčšinu  zobrazovačov od spoločnosti [Handy Tech](https://www.handytech.de/), ak sú pripojené k počítaču cez USB, sériový port alebob  bluetooth.
Pre niektoré staršie USB riadky je potrebné do systému nainštalovať USB ovládače Handy Tech.

Nasledujúce brailové riadky nie sú podporované priamo, môžete ich však používať po inštalácií [Univerzálneho ovládača Handy](Techhttps://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) a doplnku pre NVDA.

* Braillino
* Bookworm
* Modulárne riadky s firmwérom vo verzii 1.13 alebo nižšej. tieto riadky však môžete aktualizovať.

Nasleduje zoznam klávesových príkazov pre riadky Handy Tech.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |ľavá šípka, šípka hore, B3|
|posunúť riadok vpred |pravá šípka, šípka dolu, B6|
|predchádzajúci riadok |b4|
|nasledujúci riadok |b5|
|Prejsť na znak v brailly |smerové tlačidlá|
|shift+tab |esc, trojité stlačenie kláves left+up+down|
|emulácia alt |b2+b4+b5|
|emulácia klávesu escape |b4+b6|
|tab |enter, trojité stlačenie kláves right+up+down|
|enter |esc+enter, trojité stlačenie kláves up+down+left+right alebo joysticku|
|šípka hore |Joistick hore|
|šípka dolu |joistick dole|
|šípka vľavo |jostick vľavo|
|šípka vpravo |joistick vpravo|
|Ponuka NVDA |b2+b4+b5+b6|
|Prepnúť brailový kurzor zviazaný s |b2|
|Prepnúť brailový kurzor |b1|
|Prepnúť prezentáciu kontextu |b7|
|Prepnúť brailový vstup |medzera+b1+b3+b4 (medzera a veľké písmeno B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

Riadok Lilli od [MDV](https://www.mdvbologna.it/) je plne podporovaný.
Na jeho používanie nie je potrebné inštalovať žiadne ovládače.
Stačí zapojiť riadok a nastaviť NVDA na jeho používanie.

NVDA sa v súčasnosti nedokáže automaticky pripájať k týmto riadkom.

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |LF|
|posunúť riadok vpred |RG|
|predchádzajúci riadok |UP|
|nasledujúci riadok |DN|
|Prejsť na znak v brailly |smerové tlačidlá|
|shift+tab |SLF|
|tab |SRG|
|alt+tab |SDN|
|alt+shift+tab |SUP|

<!-- KC:endInclude -->

### Zobrazovače Baum/Humanware/APHp/Orbit {#Baum}

Podporované sú niektoré riadky od [Baum](https://www.visiobraille.de/index.php?article_id=1&clang=2), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) a [Orbit](https://www.orbitresearch.com/) pripojené cez USB, bluetooth alebo sériový port.
Toto zahŕňa:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Niektoré ďalšie riadky od Baum by mohli tiež fungovať, no zatiaľ toto nebolo dostatočne odskúšané.

Ak pripájate niektorý z  riadkov cez USB a riadok nepodporuje režim HID, musíte najskôr nainštalovať ovládače dodávané od výrobcu.
Riadky VarioUltra a Pronto! používajú pripojenie cez HID.
Riadky Refreshabraille a Orbit Reader môžete nastaviť tak, aby používali technológiu HID.

USB sériový režim je podporovaný  pri riadkoch Orbit Reader 20 len v systéme Windows od verzie 10.
Odporúčame vám ale používať režim HID.

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |`d2`|
|Posunúť riadok vpred |`d5`|
|Predchádzajúci riadok |`d1`|
|Nasledujúci riadok |`d3`|
|Prejsť na znak v brailly |`smerové tlačidlá`|
|`shift+tab` |`medzera + bod1+bod3`|
|`tab` |`medzera + bod4+bod6`|
|`alt` |`medzera +bod1+bod3+bod4` (`medzera+m)`|
|`escape` |`medzera+bod1+bod5` (`medzera+e)`|
|`windows` |`medzera+bod3+bod4`|
|`alt+tab` |`medzera+bod2+bod3+bod4+bod5` (`medzera+t)`|
|NVDA Menu |`medzera+bod1+bod3+bod4+bod5` (`medzera+n)`|
|`windows+d` (minimalizovať všetky aplikácie) |`medzera+bod1+bod4+bod5` (`medzera+d)`|
|Plynulé čítanie |`medzera+bod1+bod2+bod3+bod4+bod5+bod6`|

Pre zobrazovače, ktoré majú džojstik:

| Názov |Klávesová skratka|
|---|---|
|šípka hore |up|
|šípka dolu |down|
|ľavá šípka |left|
|pravá šípka |right|
|kláves enter |select|

<!-- KC:endInclude -->

### Hedo ProfiLine USB {#HedoProfiLine}

Hedo ProfiLine USB od [hedo Reha-Technik](https://www.hedo.de/) sú plne podporované.
Pred použitím je potrebné nainštalovať USB ovládače od výrobcu.

NVDA sa v súčasnosti nedokáže automaticky pripájať k týmto riadkom.

Nasleduje zoznam klávesových príkazov pre tento typ riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |K1|
|posunúť riadok vpred |K3|
|Predchádzajúci riadok |B2|
|nasledujúci riadok |B5|
|Prejsť na znak v brailly |smerové tlačidlá|
|Prepnúť nastavenie brailový kurzor zviazaný s |K2|
|Plynulé čítanie |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

HedoMobilLine USB od [hedo Reha-Technik](https://www.hedo.de/) sú plne podporované.
Pred použitím je potrebné nainštalovať USB ovládače od výrobcu.

NVDA sa v súčasnosti nedokáže automaticky pripájať k týmto riadkom.

Nasleduje zoznam klávesových príkazov pre tento typ riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |K1|
|posunúť riadok vpred |K3|
|Predchádzajúci riadok |B2|
|nasledujúci riadok |B5|
|Prejsť na znak v brailly |smerové tlačidlá|
|Prepnúť nastavenie brailový kurzor zviazaný s |K2|
|Plynulé čítanie |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B / BrailleNote Touch {#HumanWareBrailliant}

Riadky Brailliant BI and B od [HumanWare](https://www.humanware.com/), zahŕňajúc BI 14, BI 32, BI 20X, BI 40 BI 40X a B 80, sú podporované pripojené cez USB alebo bluetooth.
Ak máte riadok pripojený cez USB a protokol nastavený na HumanWare, je potrebné nainštalovať ovládač dodaný od výrobcu.
Ovládače nebudete potrebovať, ak nastavíte protokol na OpenBraille.

Takisto môžete používať bez nutnosťi inštalovať ovládače aj nasledujúce zariadenia:

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.

#### Klávesové skratky spoločné pre všetky modely {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|posunúť riadok späť |left|
|posunúť riadok vpred |right|
|predchádzajúci riadok |up|
|nasledujúci riadok |down|
|Prejsť na znak v brailly |smerové tlačidlá|
|Prepnúť nastavenie brailový kurzor zviazaný s |up+down|
|šípka hore |medzera+bod1|
|šípka dolu |medzera+bod4|
|ľavá šípka |medzera+bod3|
|pravá šípka |medzera+bod6|
|shift+tab |medzera+bod1+bod3|
|tab |medzera+bod4+bod6|
|alt |medzera+bod1+bod3+bod4 (medzera+m)|
|escape |medzera+bod1+bod5 (medzera+e)|
|enter |bod8|
|kláves windows |medzera+bod3+bod4|
|alt+tab |medzera+bod2+bod3+bod4+bod5 (medzera+t)|
|Ponuka NVDA |medzera+body 1+3+4+5 (medzera + n)|
|windows+d (minimalizovať všetky aplikácie) |medzera + body 1+4+5 (medzera + d)|
|Plynulé čítanie |medzera + body 123456|

<!-- KC:endInclude -->

#### Klávesové skratky pre riadky Brailliant BI 32, BI 40 a B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| názov |klávesová skratka|
|---|---|
|Ponuka NVDA |c1+c3+c4+c5 (príkaz n)|
|windows+d (minimalizovať všetky aplikácie) |c1+c4+c5 (príkaz d)|
|Plynulé čítanie |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Klávesové skratky pre Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|šípka hore key |joystick up|
|šípka dole |joystick down|
|šípka doľava |joystick left|
|šípka doprava |joystick right|
|enter |joystick action|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille {#Hims}

NVDA podporuje riadky Braille Sense, Smart Beetle, Sync Braille a Braille EDGE od spoločnosti [Hims](https://www.hims-inc.com/). Je potrebné ich pripájať cez USB alebo bluetooth rozhranie.
Ak pripájate riadok cez USB, je potrebné nainštalovať [USB ovládače Zo stránok HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip).

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením  na zistenie rozmiestnenia klávesov.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Presunúť na znak v brailly |routing|
|Posunúť riadok späť |leftSideScrollUp, rightSideScrollUp, leftSideScroll|
|Posunúť riadok vpred |leftSideScrollDown, rightSideScrollDown, rightSideScroll|
|Predchádzajúci riadok |leftSideScrollUp+rightSideScrollUp|
|Nasledujúci riadok |leftSideScrollDown+rightSideScrollDown|
|Prezerací kurzor na predchádzajúci riadok |rightSideUpArrow|
|Prezerací kurzor na nasledujúci riadok |rightSideDownArrow|
|Prezerací kurzor na predchádzajúci znak |rightSideLeftArrow|
|Prezerací kurzor na nasledujúci znak |rightSideRightArrow|
|Presunúť na fokus |leftSideScrollUp+leftSideScrollDown, rightSideScrollUp+rightSideScrollDown, leftSideScroll+rightSideScroll|
|ctrl |smartbeetle:f1, brailleedge:f3|
|windows |f7, smartbeetle:f2|
|alt |body 134+medzera, f2, smartbeetle:f3, brailleedge:f4|
|shift |f5|
|insert |body 24+medzera, f6|
|Kontextové menu |body 1+2+3+4+medzera, f8|
|CapsLock |body 136+medzera|
|tab |body 45+medzera, f3, brailleedge:f2|
|shift+alt+tab |f2+f3+f1|
|alt+tab |f2+f3|
|shift+tab |bod1+bod2+medzera|
|end |bod4+bod6+medzera|
|ctrl+end |bod4+bod5+bod6+medzera|
|home |bod1+bod3+medzera, smartbeetle:f4|
|ctrl+home |bod1+bod2+bod3+medzera|
|alt+f4 |body 1356+medzera|
|šípka vľavo |bod 3+medzera, leftSideLeftArrow|
|ctrl+shift+šípka vľavo |body2+8+medzera+f1|
|ctrl+ľavá šípka |bod2+medzera|
|shift+alt+ľavá šípka |bod2+bod7+F1|
|`alt+ľavá šípka` |`bod2+bod7+medzera` |
|šípka vpravo |bod 6+medzera, leftSideRightArrow|
|ctrl+shift+šípka vpravo |body 58+medzera+f1|
|ctrl+pravá šípka |bod5+medzera|
|shift+alt+pravá šípka |bod5+bod7+F1|
|`alt+pravá šípka` |`bod5+bod7+medzera`|
|page up |bod1+bod2+bod6+medzera|
|ctrl+page up |bod1+bod2+bod6+bod8+medzera|
|šípka hore |bod1+medzera, šípka hore na ľavej strane|
|ctrl+shift+šípka hore |bod2+bod3+bod8+medzera+advance1|
|ctrl+šípka hore |body 23+medzera|
|shift+alt+šípka hore |bod2+bod3+bod7+F1|
|`alt+šípka hore` |`bod2+bod3+bod7+medzera`|
|shift+šípka hore |left side scroll down  +medzera|
|pageDown |bod3+bod4+bod5+medzera|
|ctrl+pagedown |bod3+bod4+bod5+bod8+medzera|
|šípka dole |bot 4+medzera, leftSideDownArrow|
|ctrl+shift+šípka dole |body 5+6+8+medzera+f1|
|ctrl+šípka dolu |bod5+bod6+medzera|
|shift+alt+šípka dolu |bod5+bod6+bod7+F11|
|`alt+šípka dolu` |`bod5+bod6+bod7+medzera`|
|shift+šípka dolu |right side scroll down  +medzera|
|escape |body 1+5+medzera, f4, brailleedge:f1|
|delete key |body 135+medzera, body 145+medzera|
|f1 |bod1+bod2+bod5+medzera|
|f3 |bod1+bod4+bod8 + medzera|
|f4 |bod7+f3|
|windows+b |body 12+f1|
|windows+d |body 145+f1|
|ctrl+insert |smartbeetle:f1+rightSideScroll|
|alt+insert |smartbeetle:f3+rightSideScroll|

<!-- KC:endInclude -->

### brailové riadky od spoločnosti Seika {#Seika}

Podporované sú viaceré brailové riadky od spoločnosti Seika, pričom sú rozdelené do dvoch skupín. Tieto sa líšia svojou funkcionalitou:

* [Seika Verzia 3, 4, a 5 (40 bunkové), Seika80 (80 bunkové)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 bunkové), V6, a V6Pro (40 cells)](#SeikaNotetaker)

Viac informácií o riadkoch je možné nájsť v angličtine  [Na stránkach Seika](https://en.seika-braille.com/down/index.html).

#### Seika Verzia 3, 4, a 5 (40 bunkové), Seika80 (80 bunkové) {#SeikaBrailleDisplays}

* Tieto riadky v súčasnosti nepodporujú automatickú detekciu riadka na pozadí.
* V nastaveniach braillovho písma zvoľte zariadenie "zobrazovače Seika"
* Pre správnu funkčnosť je potrebné nainštalovať ovládače pre riadky Seika v3/4/5/80.
Ovládače [Poskytuje dodávateľ (anglicky)](https://en.seika-braille.com/down/index.html).

Nasledujú klávesové skratky pre tieto riadky.
Popis a umiestnenie jednotlivých tlačidiel nájdete v dokumentácii k príslušnému riadku.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Predchádzajúci riadok |b3|
|Nasledujúci riadok |b4|
|Prepnúť nastavenie brailový kurzor zviazaný s |b5|
|Plynulé čítanie |b6|
|tab |b1|
|shift+tab |b2|
|alt+tab |b1+b2|
|Ponuka NVDA |left+right|
|prejsť na znak v braily |smerové tlačidlá|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 bunkové), V6, a V6Pro (40 bunkové) {#SeikaNotetaker}

* NVDA dokáže automaticky napozadí detegovať tieto riadky, ak sú pripojené cez USB a Bluetooth.
* V nastaveniach braillovho písma zvoľte ako zariadenie "zápisník Seika", prípadne možnosť "automaticky".
* Nie je potrebné inštalovať špeciálne ovládače.

Nasledujú klávesové skratky pre tieto zápisníky.
Umiestnenie a rozloženie tlačidiel nájdete v príručke k vášmu zariadeniu.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Plynulé čítanie |medzera+Backspace|
|NVDA Menu |Left+Right|
|Presunúť na predchádzajúci riadok |LJ up|
|Presunúť na nasledujúci riadok |LJ down|
|Prepnúť nastavenie brailový kurzor zviazaný s |LJ center|
|tab |LJ right|
|shift+tab |LJ left|
|šípka hore |RJ up|
|šípka dole |RJ down|
|šípka vľavo |RJ left|
|šípka vpravo |RJ right|
|prejsť na znak v braily |routing|
|shift+šípka hore |medzera+RJ up, Backspace+RJ up|
|shift+šípka dole |medzera+RJ down, Backspace+RJ down|
|shift+šípka vľavo |medzera+RJ left, Backspace+RJ left|
|shift+šípka vpravo |medzera+RJ right, Backspace+RJ right|
|enter |RJ center, bod8|
|escape |medzera+RJ center|
|windows |Backspace+RJ center|
|medzera |medzera, Backspace|
|backspace |bod7|
|pageup |medzera+LJ right|
|pagedown |medzera+LJ left|
|home |medzera+LJ up|
|end |medzera+LJ down|
|ctrl+home |backspace+LJ up|
|ctrl+end |backspace+LJ down|

### Nové modely riadkov Papenmeier BRAILLEX {#Papenmeier}

Podporované sú tieto brailové riadky:

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB a bluetooth)
* BRAILLEX Live 20, BRAILLEX Live a BRAILLEX Live Plus (USB a bluetooth)

NVDA sa v súčasnosti nedokáže automaticky pripájať k týmto riadkom.
Jedna funkcionalita v USB ovládačoch riadka spôsobuje, že riadok v NVDA nemusí byť dostupný.
Skúste problém riešiť nasledovne:

1. Uistite sa, že máte nainštalovaný [Najnovší ovládač](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Otvorte správcu zariadení Windows.
1. Nájdite vetvu USB zariadenia.
1. Vyberte "Papenmeier Braillex USB Device".
1. Otvorte vlastnosti a prejdite na záložku pokročilé.
Niekedy sa stáva, že záložka pokročilé nie je dostupná.
Ak je to váš prípad, zatvorte správcu zariadení, ukončite nvda, odpojte zariadenie, chvíľu počkajte a pripojte riadok znovu.
Opakujte aj 4 až 5 krát, ak sa stále záložka neobjaví.
Ak stále nie je možné zobraziť záložku pokročilé, reštartujte počítač.
1. Vypnite možnosť "Load VCP" (načítať vcp).

Väčšina zariadení má tzv. panel rýchleho prístupu, ktorý umožňuje rýchle a intuitívne ovládanie.
Tento panel môžete posúvať do štyroch strán, pričom na každej strane sú dva prepínače.
Výnimkou sú riadky zo série c a Live.

Tieto a aj niektoré ďalšie riadky majú dva rady smerových tlačidiel, pričom prvý rad sa používa na získanie informácii o formátovaní.
Stlačením niektorého zo smerových tlačidiel v prvom rade v kombinácii s pohybom panela rýchleho prístupu emulujete prepnutie prepínača.
Riadky zo série Live majú len jeden rad smerových tlačidiel a panel rýchleho prístupu môžete posunúť v každom smere len o jeden krok.
Druhý krok dosiahnete tak, že stlačíte príslušné smerové tlačidlo a panel rýchleho prístupu v požadovanom smere.
Stlačením a podržaním tlačidiel up, down, right a left, prípadne pohybom na panely rýchleho prístupu zopakujete priradenú akciu.

Vo všeobecnosti sú dostupné tieto tlačidlá:

| Názov |Kláves|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov:
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Predchádzajúci riadok |up|
|Nasledujúci riadok |dn|
|Prejsť na znak v brailly |smerové tlačidlá|
|Aktuálny znak prezeracieho kurzora |l1|
|Aktivovať prvok zameraný objektovou navigáciou |l2|
|Prepnúť nastavenie brailový kurzor zviazaný s |r2|
|Názov okna |l1+up|
|Stavový riadok |l2+down|
|Nadradený objekt |up2|
|Prvý podradený objekt |dn2|
|Predchádzajúci objekt |left2|
|Nasledujúci objekt |right2|
|Oznámiť formátovanie textu pod brailovým znakom |prvý rad smerových tlačidiel|

<!-- KC:endInclude -->

Model trio má štyri dodatočné tlačidlá umiestnené pred brailovou klávesnicou.
Tlačidlá sú usporiadané zľava doprava takto:

* ľavé tlačidlo (lt)
* medzera
* medzera
* pravé tlačidlo (rt)

Pravé tlačidlo sa v súčasnosti nepoužíva.
Obe stredné tlačidlá sa používajú ako medzera.

<!-- KC:beginInclude -->

| Názov |klávesová skratka|
|---|---|
|escape |Medzera s bodom 7|
|šípka hore |medzera s bodom 2|
|šípka vľavo |medzera s bodom 1|
|šípka vpravo |medzera s bodom 4|
|šípka dolu |medzera s bodom 5|
|CTRL |lt+bod2|
|alt |lt+bod3|
|CTRL+escape |medzera s bodmi 1 2 3 4 5 6|
|tab |medzera s bodmi 3 7|

<!-- KC:endInclude -->

### Staršie modely Papenmeier Braille BRAILLEX {#PapenmeierOld}

Podporované sú tieto brailové riadky:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen+-

tieto zariadenia môžu byť pripojené len cez sériový port.
Z tohto dôvodu sa NVDA nedokáže automaticky pripájať k týmto riadkom.
Môžete teda vybrať konkrétny port, na ktorom je zariadenie pripojené, ak ste zvolili príslušný ovládač v dialógu [nastavenie brailového riadka](#SelectBrailleDisplay) dialog.

Väčšina zariadení má tzv. panel rýchleho prístupu, ktorý umožňuje rýchle a intuitívne ovládanie.
Tento panel môžete posúvať do štyroch strán, pričom na každej strane sú dva prepínače.
Stlačením a podržaním ľavého, pravého, horného alebo dolného tlačidla spôsobíte zopakovanie príslušnej akcie.
Niektoré staršie zariadenia nemajú tento panel, preto sa používajú predné tlačidlá.

Vo všeobecnosti sú dostupné tieto tlačidlá:

| Názov |kláves|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Nasleduje zoznam klávesových príkazov pre tieto typy riadkov:

<!-- KC:beginInclude -->
Zariadenia s panelom rýchleho prístupu:

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Predchádzajúci riadok |up|
|Nasledujúci riadok |dn|
|Prejsť na znak v brailly |smerové tlačidlá|
|Aktuálny znak prezeracieho kurzora |l1|
|Aktivovať prvok zameraný objektovou navigáciou |l2|
|Názov okna |l1+up|
|Stavový riadok |l2+down|
|Nadradený objekt |up2|
|Prvý podradený objekt |dn2|
|Nasledujúci objekt |right2|
|Predchádzajúci objekt |left2|
|Oznámiť formátovanie textu pod brailovým znakom |prvý rad smerových tlačidiel|

BRAILLEX Tiny:

| Názov |Klávesová skratka|
|---|---|
|Aktuálny znak prezeracieho kurzora |l1|
|Aktivovať prvok zameraný objektovou navigáciou |l2|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Predchádzajúci riadok |up|
|Nasledujúci riadok |dn|
|Prepnúť nastavenie brailový kurzor zviazaný s |r2|
|Nadradený objekt |r1+up|
|Prvý podradený objekt |r1+dn|
|Predchádzajúci objekt |r1+left|
|Nasledujúci objekt |r1+right|
|Oznámiť formátovanie pod brailovým znakom |horný rad smerových tlačidiel|
|Názov okna |l1+up|
|Stavový riadok |l2+down|

BRAILLEX 2D Screen:

| Názov |Klávesová skratka|
|---|---|
|Aktuálny znak prezeracieho kurzora |l1|
|Aktivovať prvok zameraný objektovou navigáciou |l2|
|Prepnúť nastavenie brailový kurzor zviazaný s |r2|
|Oznámiť formátovanie textu pod aktuálnym brailovým znakom |horný rád smerových tlačidiel|
|Predchádzajúci riadok |up|
|Posunúť riadok späť |left|
|Posunúť riadok vpred |right|
|Nasledujúci riadok |dn|
|Nasledujúci objekt |left2|
|Nadradený objekt |up2|
|prvý podradený objekt |dn2|
|Predchádzajúci objekt |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA podporuje zápisníky BrailleNote od [Humanware](https://www.humanware.com), ak sú nastavené do režimu pre príjem príkazov z čítača obrazovky.
Podporované sú tieto typy:

* BrailleNote Classic (len cez sériový port)
* BrailleNote PK (Sériový port a Bluetooth)
* BrailleNote MPower (Sériový port a Bluetooth)
* BrailleNote Apex (USB a Bluetooth)

Pre informácie o podpore zariadenia BrailleNote Touch, Pozrite časť [Brailliant BI  / BrailleNote Touch](#HumanWareBrailliant).

Podporované je písanie cez brailovú klávesnicu (BT) aj cez qwerty klávesnicu (QT). Výnimku tvorí zariadenie BrailleNote PK.
Riadok BrailleNote QT nepodporuje emuláciu počítačovej klávesnice.
brailové body môžete zadávať aj pomocou QT klávesnice.
Pozrite si časť Braille terminal v používateľskej príručke k Braille note.

Ak zariadenie podporuje viacero druhov pripojenia, je potrebné nastaviť druh pripojenia "braille terminal port" v nastaveniach "braille terminal".
Podrobnosti nájdete v návode k Braillenote.
Môžete tiež chcieť nastaviť port v [Dialóg nastavenie brailového riadka](#SelectBrailleDisplay) dialog.
Ak sa pripájate cez USb alebo Bluetooth, môžete si vybrať automatickú detekciu portu, "Bluetooth" alebo "USB", v závislosti od vybraného zariadenia.
Ak sa pripájate cez niektorý zo sériových portov, alebo cez USB / sériový prevodník, alebo ak nie sú dostupné iné možnosti, musíte si vybrať niektorý z hardwarových komunikačných portov.

Pred pripojením BrailleNote Apex cez USB je potrebné nainštalovať ovládače dodávané spoločnosťou HumanWare.

Na riadku BrailleNote Apex BT môžete používať skrolovacie koliesko na ovládanie príkazov NVDA.
Koliesko pozostáva zo štyroch smerových tlačidiel, jedného potvrdzovacieho tlačidla v strede a kolieska, ktoré možno otočiť v smere alebo protismere hodinových ručičiek.

Nasleduje zoznam klávesových príkazov pre tento typ riadku.
Prosím, prečítajte si dokumentáciu dodanú spolu so zariadením na zistenie rozmiestnenia klávesov.

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |back|
|Posunúť riadok vpred |advance|
|Predchádzajúci riadok |previous|
|Nasledujúci riadok |next|
|Prejsť na znak v brailly |smerové tlačidlá|
|NVDA menu |medzera +body 1345 (medzera+n)|
|Prepnúť nastavenie brailový kurzor zviazaný s |previous+next|
|Šípka hore |medzera+bod1|
|Šípka dole |medzera+bod4|
|Šípka vľavo |space+bod3|
|Šípka vpravo |space+bod6|
|Strana hore |medzera+body 1,3|
|Strana dole |medzera+body 4,6|
|Home |medzera+body 1,2|
|End |medzera+body 4,5|
|ctrl+home |medzera+body 1,2,3|
|ctrl+end |medzera+body 4,5,6|
|Medzera |medzera|
|Enter |medzera+bod8|
|Backspace |medzera+bod7|
|Tab |medzera+body 2345 (medzera+t)|
|Shift+tab |medzera+body 1,2,5,6|
|Windows |medzera+body 2,4,5,6 (medzera+w)|
|Alt |medzera+body 1,3,4 (medzera+m)|
|Nápoveda vstupu |medzera+body 2,3, 6 (medzera+znížené h)|

Nasledujú skratky špecifické pre model BrailleNote QT, ak nie je v brailovom režime.

| Názov |klávesová skratka|
|---|---|
|NVDA menu |read+n|
|šípka hore |šípka hore|
|šípka dole |šípka dole|
|šípka vľavo |šípka vľavo|
|šípka vpravo |šípka vpravo|
|Page up |function+šípka hore|
|Page down |function+šípka dole|
|Home |function+šípka vľavo|
|End |function+šípka vpravo|
|ctrl+home |read+t|
|ctrl+end |read+b|
|Enter |enter|
|Backspace |backspace|
|Tab |tab|
|Shift+tab |shift+tab|
|kláves Windows |read+w|
|Alt |read+m|
|Nápoveda vstupu |read+1|

Nasledujúce príkazy je možné vykonať pomocou skrolovacieho kolieska:

| Názov |klávesová skratka|
|---|---|
|šípka hore |tlačidlo hore|
|šípka dole |tlačidlo dole|
|šípka vľavo |tlačidlo vľavo|
|šípka vpravo |tlačidlo vpravo|
|Enter |stredné potvrdzovacie tlačidlo|
|Tab |pootočiť kolieskom v smere hodinových ručičiek|
|Shift+tab |pootočiť kolieskom v protismere hodinových ručičiek|

<!-- KC:endInclude -->

### Zobrazovače EcoBraille {#EcoBraille}

NVDA podporuje zobrazovače EcoBraille od spoločnosti [ONCE](https://www.once.es/).
Podporované sú tieto riadky:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

Sériový port, do ktorého je riadok pripojený, môžete vybrať v dialógu [nastavenie brailového riadka](#SelectBrailleDisplay) dialog.
NVDA sa v súčasnosti nedokáže automaticky pripájať k týmto riadkom.

Nasleduje zoznam klávesových príkazov.
Pre popis a umiestnenie tlačidiel si prosím pozrite [Návod k zobrazovačom EcoBraille (anglicky)](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) for descriptions of where these keys can be found.

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |T2|
|Posunúť riadok vpred |T4|
|Predchádzajúci riadok |T1|
|Nasledujúci riadok |T5|
|prejsť na znak v brailly |smerové tlačidlá|
|Aktivovať navigačný objekt |T3|
|Nasledujúci režim prezerania |F1|
|Nadradený objekt |F2|
|Predchádzajúci režim prezerania |F3|
|predchádzajúci objekt |F4|
|Aktuálny objekt |F5|
|nasledujúci objekt |F6|
|navigačný objekt na fokus |F7|
|Prvý podradený objekt |F8|
|Fokus alebo systémový kurzor na pozíciu prezeracieho kurzora |F9|
|Súradnice kurzora v režime prezerania |F0|
|Prepnúť nastavenie brailový kurzor zviazaný s |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

brailový riadok SuperBraille, populárny hlavne v Tajvane, je možné pripojiť cez USB alebo sériový port.
Tento riadok nemá žiadne tlačidlá a preto sa na prácu s ním používa klávesnica počítača.
Aby bolo možné zaisťiť prácu s riadkom a tiež kompatibilitu s inými čítačmi obrazovky v Tajvane, sú k dispozícii tieto klávesové skratky.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť zobrazenie späť |mínus na numerickej klávesnici|
|Posunúť zobrazenie vpred |plus na numerickej klávesnici|

<!-- KC:endInclude -->

### Zobrazovače Eurobraille {#Eurobraille}

Podporované sú riadky b.book, b.note, Esys, Esytime a Iris od spoločnosti Eurobraille.
Tieto zariadenia majú brailovú klávesnicu s desiatimi tlačidlami.
Popis tlačidiel nájdete v používateľskej príručke príslušného riadka.
Ľavá časť tlačidla, ktoré vyzerá ako medzera, funguje ako kláves backspace, pravá ako medzera.

Tieto zariadenia sa pripájajú cez USB a aktívna je aj ich vstavaná klávesnica.
Túto klávesnicu je možné vypnúť alebo zapnúť pomocou klávesovej skratky.
Nižšie popísané skratky fungujú, ak je táto možnosť vypnutá.

#### Funkcie brailovej klávesnice {#EurobrailleBraille}

<!-- KC:beginInclude -->

| názov |Klávesová skratka|
|---|---|
|Vymazať naposledy zadaný znak |`backspace`|
|Preložiť aktuálny brailový vstup a odoslať kláves Enter |`backspace+medzera`|
|Prepnúť kláves `NVDA` |`bod3+bod5+medzera`|
|`insert` |`bod1+bod3+bod5+medzera`, `bod3+bod4+bod5+medzera`|
|`delete` |`bod3+bod6+medzera`|
|`home` |`bod1+bod2+bod3+medzera`|
|`end` |`bod4+bod5+bod6+medzera`|
|`šípka vľavo` |`bod2+medzera`|
|`šípka vpravo` |`bod5+medzera`|
|`šípka hore` |`bod1+medzera`|
|`šípka dole` key |`bod6+medzera`|
|`page up` |`bod1+bod3+medzera`|
|`pageDown` |`bod4+bod6+medzera`|
|`numerická 1` |`bod1+bod6+backspace`|
|`numerická 2` |`bod1+bod2+bod6+backspace`|
|`numerická 3` |`bod1+bod4+bod6+backspace`|
|`numerická 4` |`bod1+bod4+bod5+bod6+backspace`|
|`numerická 5` |`bod1+bod5+bod6+backspace`|
|`numerická 6` |`bod1+bod2+bod4+bod6+backspace`|
|`numerická 7` |`bod1+bod2+bod4+bod5+bod6+backspace`|
|`numerická 8` |`bod1+bod2+bod5+bod6+backspace`|
|`numerická 9` |`bod2+bod4+bod6+backspace`|
|`numerický Insert` |`bod3+bod4+bod5+bod6+backspace`|
|`numerická čiarka` |`bod2+backspace`|
|`numerické lomeno` |`bod3+bod4+backspace`|
|`numerický krát` |`bod3+bod5+backspace`|
|`numerické mínus` |`bod3+bod6+backspace`|
|`numerické plus` |`bod2+bod3+bod5+backspace`|
|`numerický enter` |`bod3+bod4+bod5+backspace`|
|`escape` |`bod1+bod2+bod4+bod5+medzera`, `l2`|
|`tab` |`bod2+bod5+bod6+medzera`, `l3`|
|`shift+tab` |`bod2+bod3+bod5+medzera`|
|`printScreen` |`bod1+bod3+bod4+bod6+medzera`|
|`pause` |`bod1+bod4+medzera`|
|`aplikácie` |`bod5+bod6+backspace`|
|`f1` |`bod1+backspace`|
|`f2` |`bod1+bod2+backspace`|
|`f3` |`bod1+bod4+backspace`|
|`f4` |`bod1+bod4+bod5+backspace`|
|`f5` |`bod1+bod5+backspace`|
|`f6` |`bod1+bod2+bod4+backspace`|
|`f7` |`bod1+bod2+bod4+bod5+backspace`|
|`f8` |`bod1+bod2+bod5+backspace`|
|`f9` |`bod2+bod4+backspace`|
|`f10` |`bod2+bod4+bod5+backspace`|
|`f11` |`bod1+bod3+backspace`|
|`f12` |`bod1+bod2+bod3+backspace`|
|`windows` |`bod1+bod2+bod4+bod5+bod6+medzera`|
|Prepnúť kláves `windows` |`bod1+bod2+bod3+bod4+backspace`, `bod2+bod4+bod5+bod6+medzera`|
|`capsLock` |`bod7+backspace`, `bod8+backspace`|
|`numLock` |`bod3+backspace`, `bod6+backspace`|
|`shift` |`bod7+medzera`|
|Prepnúť kláves `shift` |`bod1+bod7+medzera`, `bod4+bod7+medzera`|
|`ctrl` |`bod7+bod8+medzera`|
|Prepnúť kláves `ctrl` |`bod1+bod7+bod8+medzera`, `bod4+bod7+bod8+medzera`|
|`alt` |`bod8+medzera`|
|Prepnúť kláves `alt` |`bod1+bod8+medzera`, `bod4+bod8+medzera`|
|Prepnúť simuláciu HID klávesnice |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### Klávesové skratky pre riadok b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |`backward`|
|Posunúť riadok vpred |`forward`|
|Presunúť na fokus |`backward+forward`|
|Prejsť na znak v brailly |`smerové tlačidlá`|
|`šípka vľavo` |`joystick2Left`|
|`šípka vpravo` |`joystick2Right`|
|`šípka hore` |`joystick2Up`|
|`šípka dole` |`joystick2Down`|
|`enter` |`joystick2Center`|
|`escape` |`c1`|
|`tab` |`c2`|
|Prepnúť kláves `shift` |`c3`|
|Prepnúť kláves `ctrl` |`c4`|
|Prepnúť kláves `alt` |`c5`|
|Prepnúť kláves `NVDA` |`c6`|
|`ctrl+Home` |`c1+c2+c3`|
|`ctrl+End` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### Klávesové skratky pre riadky b.note {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |`leftKeypadLeft`|
|Posunúť riadok vpred |`leftKeypadRight`|
|Prejsť na znak v braily |`smerové tlačidlá`|
|Oznámiť formátovanie pod brailovou bunkou |`doubleRouting`|
|Presunúť prezerací kurzor na nasledujúci riadok |`leftKeypadDown`|
|Prepnúť na predchádzajúci režim prezerania |`leftKeypadLeft+leftKeypadUp`|
|Prepnúť na nasledujúci režim prezerania |`leftKeypadRight+leftKeypadDown`|
|`šípka vľavo` |`rightKeypadLeft`|
|`šípka vpravo` |`rightKeypadRight`|
|`šípka hore` |`rightKeypadUp`|
|`šípka dole` |`rightKeypadDown`|
|`ctrl+home` |`rightKeypadLeft+rightKeypadUp`|
|`ctrl+end` |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Klávesové skratky pre riadky Esys {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |`switch1Left`|
|POsunúť riadok vpred |`switch1Right`|
|Presunúť na fokus |`switch1Center`|
|Prejsť na znak v braily |`smerové tlačidlá`|
|Oznámiť formátovanie pod brailovou bunkou |`doubleRouting`|
|Presunúť prezerací kurzor na predchádzajúci riadok |`joystick1Up`|
|Presunúť prezerací kurzor na nasledujúci riadok |`joystick1Down`|
|Presunúť prezerací kurzor na predchádzajúci znak |`joystick1Left`|
|Presunúť prezerací kurzor na nasledujúci riadok |`joystick1Right`|
|`šípka vľavo` |`joystick2Left`|
|`šípka vpravo` |`joystick2Right`|
|`šípka hore` |`joystick2Up`|
|`šípka dole` |`joystick2Down`|
|`enter` |`joystick2Center`|

<!-- KC:endInclude -->

#### Klávesové skratky pre riadky Esytime {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Posunúť riadok späť |`l1`|
|Posunúť riadok vpred |`l8`|
|Presunúť na fokus |`l1+l8`|
|Prejsť na znak v braily |`smerové tlačidlá`|
|Oznámiť formátovanie pod bunkov v braily |`doubleRouting`|
|Prezerací kurzor na predchádzajúci riadok |`joystick1Up`|
|Prezerací kurzor na nasledujúci riadok |`joystick1Down`|
|Prezerací kurzor na predchádzajúci znak |`joystick1Left`|
|Prezerací kurzor na Nasledujúci znak |`joystick1Right`|
|`šípka vľavo` |`joystick2Left`|
|`šípka vpravo` |`joystick2Right`|
|`šípka hore` |`joystick2Up`|
|`šípka dole` |`joystick2Down`|
|`enter` |`joystick2Center`|
|`escape` |`l2`|
|`tab` |`l3`|
|Prepnúť kláves `shift` |`l4`|
|Prepnúť kláves `ctrl` |`l5`|
|Prepnúť kláves `alt` |`l6`|
|Prepnúť kláves `NVDA` |`l7`|
|`ctrl+home` |`l1+l2+l3`, `l2+l3+l4`|
|`ctrl+end` |`l6+l7+l8`, `l5+l6+l7`|
|Prepnúť simuláciu HID klávesnice |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Riadky Nattiq nBraille {#NattiqTechnologies}

NVDA podporuje brailové riadky od spoločnosti [Nattiq Technologies](https://www.nattiq.com/) pripojené cez USB.
V systéme Windows od verzie 10 sú riadky rozpoznané automaticky. Pre staršie verzie operačného systému Windows je potrebné ručne nainštalovať ovládače.
Tie sú dostupné zo stránok výrobcu.

Nasledujú príkazy, ktoré môžete používať na tomto riadku v kombinácii s NVDA.
Umiestnenie jednotlivých tlačidiel je popísané v dokumentácii k zariadeniu.
<!-- KC:beginInclude -->

| Názov |klávesová skratka|
|---|---|
|Posunúť riadok späť |up|
|Posunúť riadok vpred |down|
|Predchádzajúci riadok |left|
|Nasledujúci riadok |right|
|Prejsť na znak |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) je osobitný program, prostredníctvom ktorého je možné použiť množstvo ďalších brailových zobrazovačov.
Na používanie ovládača brailových riadkov BRLTTY je potrebné nainštalovať [BRLTTY pre Windows](https://www.brltty.app/download.html).
Mali by ste si stiahnuť najnovšiu inštalačnú verziu, ktorá bude pomenovaná napríklad brltty-win-4.2-2.exe.
Počas konfigurácie riadku a portu dávajte veľký pozor na presné dodržiavanie inštrukcií, hlavne ak pripájate riadok cez USB a už máte nainštalované ovládače od výrobcu.

Riadky, ktoré podporujú písanie pomocou vstavanej klávesnice sa riadia nastavením BRLTTY.
Nastavenie vstupnej prekladovej tabuľky v NVDA preto nemá na vstup z brailovej klávesnice tohto typu riadku žiadny vplyv.

Ovládač brltty nie je zahrnutý do automatického rozpoznávania brailových riadkov.

Nasledujú brltty klávesové skratky pre NVDA.
Prosím prečítajte si [dokumentáciu skratiek  brltty](https://brltty.app/doc/KeyBindings/) pre viac informácií o tom, ako sú príkazy brltty mapované na tlačidlá skutočných zobrazovačov.
<!-- KC:beginInclude -->

| Názov |príkaz brltty|
|---|---|
|posunúť riadok späť |`fwinlt` (go left one window)|
|posunúť riadok vpred |`fwinrt` (go right one window)|
|predchádzajúci riadok |`lnup` (go up one line)|
|nasledujúci riadok |`lndn` (go down one line)|
|Prejsť na znak v brailly |`route` (bring cursor to character)|
|Zapnúť alebo vypnúť nápovedu vstupu |`learn` (enter/leave command learn mode)|
|Otvoriť ponuku NVDA |`prefmenu` (enter/leave preferences menu)|
|Obnoviť nastavenia |`prefload` (restore preferences from disk)|
|Uložiť nastavenia |`prefsave` (save preferences to disk)|
|Oznámiť čas |`time` (show current date and time)|
|Zobraziť riadok pod kurzorom |`say_line` (speak current line)|
|Spustiť plynulé čítanie |`say_below` (speak from current line through bottom of screen)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Zariadenia Caiku Albatross, ktoré vyrábala spoločnosť Tivomatic a boli dostupné hlavne vo Fínsku, môžete pripojiť cez sériový port alebo usb.
Pre správne fungovanie tohto zariadenia nie je potrebné inštalovať ovládače.
Jednoducho pripojte riadok a zvoľte ho v nastaveniach NVDA.

Pozor: Odporúčame nastaviť prenosovú rýchlosť (Baud rate) na hodnotu 19200.
Zmenu prenosovej rýchlosti vykonajte v interných nastaveniach riadka.
Samotný ovládač podporuje aj rýchlosť 9600, avšak nedokáže zistiť, akú rýchlosť používa samotný riadok.
Nakoľko rýchlosť 19200 je predvolená, používa sa ako prvá možnosť.
Ak je prenosová rýchlosť odlišná, môže dochádzať k chybám.

Nasledujú klávesové skratky dostupné pre tento riadok.
Popis umiestnenia tlačidiel je možné nájsť v dokumentácii k riadku.
<!-- KC:beginInclude -->

| Názov |Klávesová skratka|
|---|---|
|Presunúť prezerací kurzor na začiatok |`home1`, `home2`|
|Presunúť prezerací kurzor na koniec |`end1`, `end2`|
|Presunúť navigačný objekt na fokus |`eCursor1`, `eCursor2`|
|Presunúť kurzor na fokus |`cursor1`, `cursor2`|
|Presunúť myš na navigačný objekt |`home1+home2`|
|Nastaviť navigačný objekt na objekt pod kurzorom myši a oznámiť ho |`end1+end2`|
|Presunúť fokus na navigačný objekt |`eCursor1+eCursor2`|
|Prepínať nastavenie brailový riadok zviazaný s |`cursor1+cursor2`|
|Predchádzajúci riadok |`up1`, `up2`, `up3`|
|Nasledujúci riadok |`down1`, `down2`, `down3`|
|Posunúť riadok späť |`left`, `lWheelLeft`, `rWheelLeft`|
|Posunúť riadok vpred |`right`, `lWheelRight`, `rWheelRight`|
|Prejsť na znak v brailly |`routing`|
|Oznámiť informácie o formátovaní pod aktuálnou braillovou bunkou |`secondary routing`|
|Nastaviť prezentovanie kontextu |`attribute1+attribute3`|
|Prepína režim reči |`attribute2+attribute4`|
|Prejsť na predchádzajúci režim prezerania (objekt, dokument, obrazovka) |`f1`|
|Prejsť na nasledujúci režim prezerania (objekt, dokument, obrazovka) |`f2`|
|Presunúť navigačný objekt na prvý nadradený objekt |`f3`|
|Presunúť navigačný objekt na prvý podradený objekt |`f4`|
|Presunúť navigačný objekt na predchádzajúci objekt |`f5`|
|Presunúť navigačný objekt na nasledujúci objekt |`f6`|
|Oznámiť aktuálny navigačný objekt |`f7`|
|Oznámiť súradnice objektu pod prezeracím kurzorom |`f8`|
|Zobraziť nastavenia brailovho písma |`f1+home1`, `f9+home2`|
|Prečíta stavový riadok a presunie naň navigačný objekt |`f1+end1`, `f9+end2`|
|Prepína tvar kurzora |`f1+eCursor1`, `f9+eCursor2`|
|Prepína brailový kurzor |`f1+cursor1`, `f9+cursor2`|
|Prepína režimi zobrazovania správ na brailovom riadku |`f1+f2`, `f9+f10`|
|Prepína režimi ukazovania výberu |`f1+f5`, `f9+f14`|
|Prepína režimi pre nastavenie "smerové tlačidlá posúvajú prezerací aj systémový kurzor" |`f1+f3`, `f9+f11`|
|Vykonať predvolenú akciu na navigačnom objekte |`f7+f8`|
|Oznámiť čas a dátum |`f9`|
|Oznámiť stav batérie, zostávajúci čas a stav nabíjania |`f10`|
|Oznámiť názov okna |`f11`|
|Oznámiť stavový riadok |`f12`|
|Oznámiť aktuálny riadok pod kurzorom |`f13`|
|Plynulé čítanie |`f14`|
|Oznámiť aktuálny znak pod prezeracím kurzorom |`f15`|
|Oznámiť riadok, na ktorom sa nachádza kurzor v navigačnom objekte |`f16`|
|Oznámiť slovo, na ktorom sa nachádza prezerací kurzor v navigačnom objekte |`f15+f16`|
|Presunúť kurzor na predchádzajúci riadok v navigačnom objekte a oznámiť ho |`lWheelUp`, `rWheelUp`|
|Presunúť kurzor na nasledujúci riadok v navigačnom objekte a oznámiť ho |`lWheelDown`, `rWheelDown`|
|`Windows+d` (minimalizovať všetky aplikácie) |`attribute1`|
|`Windows+e` (tento počítač) |`attribute2`|
|`Windows+b` (prejsť na systémový panel) |`attribute3`|
|`Windows+i` (Nastavenia Windows) |`attribute4`|

<!-- KC:endInclude -->

### Riadky podporujúce HID štandard {#HIDBraille}

Toto je experimentálny ovládač pre riadky podporujúce nový HID štandard, na ktorom sa v roku 2018 dohodli Microsoft, Google, Apple a viaceré spoločnosti dodávajúce asistívne technológie vrátane NV Access. 
Cieľom je, aby všetky budúce brailové riadky podporovali tento štandard čím sa odstráni nutnosť mať pre každý riadok samostatný ovládač.

NVDA dokáže automaticky rozpoznať, že váš riadok podporuje tento spôsob komunikácie.

Nasledujú klávesové skratky pre tieto riadky:
<!-- KC:beginInclude -->

| názov |klávesová skratka|
|---|---|
|Posunúť riadok späť |pan left alebo rocker up|
|Posunúť riadok vpred |pan right alebo rocker down|
|Prejsť na znak v brailly |routing set 1|
|Prepnúť nastavenie brailový kurzor zviazaný s |šípka hore + šípka dole|
|Šípka hore |joystick hore, dpad hore alebo medzera+bod1|
|Šípka dole |joystick dole, dpad dole alebo  medzera+bod4|
|Šípka vľavo |medzera+bod3 alebo joystick vľavo alebo dpad vľavo|
|Šípka vpravo |medzera+bod6 alebo joystick vpravo alebo dpad vpravo|
|shift+tab |medzera+bod1+bod3|
|tab |medzera+bod4+bod6|
|alt |medzera+bod1+bod3+bod4 (medzera+m)|
|escape |medzera+bod1+bod5 (medzera+e)|
|enter |bod8 alebo  stred joysticku  alebo stred dpad|
|windows |medzera+bod3+bod4|
|alt+tab |medzera+bod2+bod3+bod4+bod5 (medzera+t)|
|NVDA Menu |medzera+bod1+bod3+bod4+bod5 (medzera+n)|
|windows+d (minimalizovať všetky aplikácie) |medzera+bod1+bod4+bod5 (medzera+d)|
|Plynulé čítanie |medzera+bod1+bod2+bod3+bod4+bod5+bod6|

<!-- KC:endInclude -->

## Pre pokročilých {#AdvancedTopics}
### Bezpečný režim {#SecureMode}

Systémoví administrátori môžu chcieť nastaviť NVDA tak, aby nemal oprávnenia pristupovať k celému systému.
NVDA umožňuje inštaláciu doplnkov, ktoré môžu spúšťať vlastný kód, a to aj v situáciách, keď má NVDA práva adminitrátora.
Navyše, je možné spúšťať vlastný kód cez Python konzolu.
Bezpečný režim zabraňuje používateľovi v úprave konfigurácie NVDA a ďalšími spôsobmi zabraňuje v neoprávnenom prístup k systému.

NVDA sa automaticky spúšťa v bezpečnom režime na [zabezpečených obrazovkách](#SecureScreens). Ak chcete aj na týchto obrazovkách mať plný prístup, použite [systémový parameter](#SystemWideParameters) `serviceDebug`.
Ak chcete vynútiť bezpečný režim, použite [systémový parameter](#SystemWideParameters). `forceSecureMode`.
NVDA je tiež možné spustiť v bezpečnom režime z [príkazového riadka](#CommandLineOptions) parametrom `-s`.

Bezpečný režim vypína:

* Ukladanie konfigurácie a nastavení na disk
* Ukladanie zmenených klávesových skratiek na disk
* [Možnosť pracovať s konfiguračnými profilmi](#ConfigurationProfiles), teda nie je možné ich vytvárať, premenovať, mazať a podobne
* Načítať  vlastnú konfiguráciu  s použitím [ príkazu `-c`](#CommandLineOptions)
* aktualizovať NVDA a vytvárať prenosnú verziu
* [katalóg s doplnkami](#AddonsManager)
* [Python konzolu](#PythonConsole)
* [Zobrazovač logu](#LogViewer) a vytváranie záznamu
* [Zobrazovač brailu](#BrailleViewer) a [Zobrazovač reči](#SpeechViewer)
* Otváranie externých dokumentov z ponuky NVDA, akými sú používateľská príručka a Tím NVDA.

Nainštalovaná verzia NVDA ukladá nastavenia a doplnky v adresári `%APPDATA%\nvda`.
Odporúčame zabrániť prístupu k tomuto priečinku aj na používateľskej úrovni, aby nebolo možné ani priamo meniť nastavenia a vkladať doplnky.

Bezpečný režim nie je efektívny pri prenosnej verzii NVDA.
To isté platí, ak je spustená dočasná kópia NVDA pri inštalácii.
Používateľ, ktorý má umožnené spúšťať externé aplikácie, predstavuje bezpečnostné riziko.
Je potrebné, aby systémový administrátor zabránil spúšťaniu neautorizovaného software, vrátane prenosných verzii NVDA.

Používatelia NVDA často potrebujú upravovať nastavenia tak, aby vyhovovali ich požiadavkám.
Toto zahŕňa inštaláciu doplnkov, ktoré je potrebné individuálne vložiť do NVDA.
Bezpečný režim neumožňuje meniť nastavenia NVDA, preto sa uistite, že je NVDA nastavené podľa požiadaviek používateľa skôr, než tento režim nastavíte natrvalo.

### Zabezpečené obrazovky {#SecureScreens}

NVDA sa spúšťa v [bezpečnom režime](#SecureMode) ak je spustené na zabezpečených obrazovkách. Ak chcete mať plný prístup, použite [systémový parameter](#SystemWideParameters) `serviceDebug`.

Na zabezpečenej obrazovke NVDA používa nastavenia uložené v systémovom profile.
Nastavenia je možné skopírovať [pre použitie na zabezpečených obrazovkách](#GeneralSettingsCopySettings).

Zabezpečené obrazovky zahŕňajú:

* Prihlasovaciu obrazovku Windows
* Obrazovku UAC, ktorá sa otvorí pri pokuse vykonať akciu ako administrátor
  * Toto zahŕňa inštaláciu programov

### Parametre príkazového riadka {#CommandLineOptions}

NVDA dokáže pri spustení spracovať parametre, ktoré ovplyvnia jeho činnosť.
Môžete použiť viacero parametrov súčasne.
parametre sa dajú použiť priamo v odkaze (cez vlastnosti odkazu), v dialógu spustiť (menu štart > spustiť alebo skratka Windows+r) alebo priamo cez príkazový riadok Windows.
parametre oddeľujte od seba a od názvu spustiteľného súboru NVDA medzerou.
Užitočný parameter je `--disable-addons`, ktorý zakáže všetky doplnky.
toto vám môže pomôcť zistiť, či problémy s NVDA spôsobuje doplnok a prípadne zabrániť vážnym problémom, ktoré doplnok spôsobuje.

NVDA môžete napríklad ukončiť tak, že do okna spustiť napíšete:

    NVDA -q

Niektoré parametre majú dlhý a skrátený zápis, iné majú len dlhý zápis.
Tie, ktoré podporujú skrátený zápis môžete kombinovať takto:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc C:\esta-k-nastaveniam` |Spustí NVDA bez zvukov a úvodnej správy a načíta konfiguráciu zo zadaného adresára.|
|`nvda -mc CONFIGPATH --disable-addons` |To isté ako predošlý príklad a takisto zakáže doplnky|

K niektorým parametrom príkazového riadka musíte pridať aj argumenty. Tak určíte, ako podrobne má NVDA zaznamenávať informácie do logu, alebo môžete určiť priečinok s používateľskými dátami NVDA.
Ak použijete krátky zápis parametra, argumenty oddeľte medzerou, ak použijete dlhý zápis, použite znak rovná sa (`=`). napríklad:

| . {.hideHeaderRow} |.|
|---|---|
|`NVDA -l 10` |Povie NVDA, že úroveň záznamu je debug|
|`NVDA --log-file=c:\NVDA.log` |Povie NVDA, aby log zapisoval do súboru `c:\NVDA.log`|
|`NVDA --log-level=20 -f c:\NVDA.log` |Povie NVDA, že úroveň záznamu je info a log sa má zapísať do `c:\NVDA.log`|

NVDA v súčasnosti podporuje tieto parametre:

| krátky zápis |dlhý zápis |popis|
|---|---|---|
|`-h` |`--help` |zobrazí pomoc pre parametre príkazového riadka a skončí|
|`-q` |`--quit` |Ukončí práve spustenú kópiu NVDA|
|`-k` |`--check-running` |Oznámi, či NVDA beží alebo nie. 0 =beží, 1 =nie|
|`-f c:\esta\k\suboru` |`--log-file=c:\esta\k\suboru` |Cesta k súboru, kde sa má zapisovať log. Zapisovanie logu je vždy vypnuté v bezpečnom režime.|
|`-l loglevel` |`--log-level=loglevel` |Určuje úroveň záznamu (debug 10, Vstup a výstup 12, debug 15, info 20, vypnuté 100), predvolene je úroveň nastavená na upozornenia.  Zapisovanie logu je vždy vypnuté v bezpečnom režime.|
|`-c C:\esta\k\profilu` |`--config-path=C:\esta\k\profilu` |určuje cestu, kam sa ukladajú nastavenia NVDA. Zapisovanie logu je vždy vypnuté v bezpečnom režime.|
|Nie je |`--lang=jazyk` |Uprednostniť iné nastavenie jazyka NVDA. Použite parameter Windows, ak chcete nastaviť jazyk NVDA rovnako, ako je nastavený jazyk systému. en pre angličtinu, sk pre slovenčinu, cs pre češtinu a pod.|
|`-m` |`--minimal` |spustí NVDA bez zvukov, bez používateľského rozhrania, bez úvodného dialógu a podobne|
|`-s` |`--secure` |Spustí NVDA v [bezpečnom režime](#SecureMode)|
|nie je |`--disable-addons` |Všetky doplnky budú vypnuté|
|Nie je |`--debug-logging` |nastaví úroveň záznamu pre najbližšie spustenie NVDA na najvyššiu úroveň (debug). Toto nastavenie má prednosť pred ostatnými argumentmi ( `--loglevel`, `-l` aj ak bolo zaznamenávanie vypnuté).|
|Nie je |`--no-logging` |Vypne zaznamenávanie do logu. Toto nastavenie môže byť zmenené ak nastavíte úroveň záznamu cez príkazový riadok (`--loglevel -l`) alebo ak zapnete zaznamenávanie najvyššej úrovne cez príkaz `--debug-logging`|
|nie je |`--no-sr-flag` |Nezmení predvolené označenie čítača obrazovky v systéme|
|Nie je |`--install` |Nainštaluje NVDA a spustí nainštalovanú kópiu|
|nie je |`--install-silent` |Nainštaluje NVDA s predvolenými parametrami bez používateľského rozhrania, ale nespustí nainštalovanú kópiu|
|Nie je |`--enable-start-on-logon=True` |False |Počas inštalácie povolí [Spustenie na prihlasovacej obrazovke](#StartAtWindowsLogon)|
|nie je |`--copy-portable-config` |Počas inštalácie skopíruje nastavenia z prenosnej verzie NVDA podľa zadanej cesty (`--config-path`, `-c`) do používateľského profilu|
|Nie je |`--create-portable` |Vytvorí prenosnú verziu NVDA a spustí ju. Je potrebné určiť cestu cez argument `--portable-path`|
|Nie je |`--create-portable-silent` |Vytvorí prenosnú verziu NVDA, ale nespustí ju. Je potrebné určiť cestu cez argument `--portable-path`|
|Nie je |`--portable-path=cesta` |určuje, kam sa uloží prenosná verzia NVDA|

### Systémové parametre {#SystemWideParameters}

Niektoré Nastavenia NVDA je možné zmeniť v editore registrov.
Hodnoty sú uložené v nasledujúcich kľúčoch:

* 32-bitový systém: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* 64-bitový systém: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

V súčasnosti je možné upraviť tieto hodnoty:

| Názov |Typ |dostupné hodnoty |Popis|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (predvolená hodnota) =vypnuté, 1 =zapnuté |Ak je zapnuté, ukladá konfiguráciu  do lokálneho používateľského adresára a nie do priečinka roaming.|
|`serviceDebug` |DWORD |0 (predvolené) =vypnuté, 1 =zapnuté |Ak je povolené, vypne [bezpečný  režim](#SecureMode) na [prihlasovacích a zabezpečených obrazovkách](#SecureScreens). Toto nastavenie však predstavuje vysoké bezpečnostné ryziko, preto vás od jeho použitia v neodôvodnených prípadoch odrádzame.|
|`forceSecureMode` |DWORD |0 (predvolené) =vypnuté, 1 =zapnuté |Ak je zapnuté, vynúti [bezpečný režim](#SecureMode) automaticky pri každom spustení NVDA.|

## Ako získať viac informácií {#FurtherInformation}

Ak hľadáte ďalšie informácie o NVDA, o jeho vývoji, alebo hľadáte pomoc, navštívte [stránku projektu (anglicky)](NVDA_URL).
Na tejto stránke môžete tiež nájsť e-mailové konferencie a odkazy na ďalšie komunitné projekty a stránky o NVDA.
Môžete tu tiež nájsť informácie o vývoji, zdrojové kódy a iné súvisiace materiály.
