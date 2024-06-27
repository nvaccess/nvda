# NVDA NVDA_VERSION Gebruikershandleiding

[TOC]

<!-- KC:title: NVDA NVDA_VERSION overzicht commando's -->



## Inleiding {#Introduction}

Welkom bij NVDA!

NonVisual Desktop Access (NVDA) is een gratis en open source schermlezer voor het Microsoft Windows besturingssysteem.
Door het geven van feedback in synthetische spraak en braille stelt NVDA slechtzienden en blinden in staat om toegang te krijgen tot computers met het Windows besturingssysteem zonder bijkomende kosten.
NVDA wordt ontwikkeld door [NV Access](https://www.nvaccess.org/), met bijdragen van de gebruikers.

### Algemene kenmerken {#GeneralFeatures}

NVDA stelt blinden en slechtzienden in staat om te werken met het Windows besturingssysteem en veel toepassingen van derden.

Een korte videodemonstratie, ["Wat is NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) is te volgen op  het YouTube-kanaal van NV Access.

Belangrijke functies en mogelijkheden:

* Ondersteuning voor populaire toepassingen zoals webbrowsers, emailprogramma’s, chatprogramma’s en kantoorapplicaties
* Ingebouwde spraakmodule met ondersteuning voor meer dan 80 talen
* Vermeldding van tekstopmaakeigenschappen , voor zover beschikbaar, zoals naam lettertype, grootte, stijl- en spelfouten
* Tekst onder de muis wordt automatisch voorgelezen en er kan een akoestisch signaal worden ingesteld dat de muispositie aangeeft
* Ondersteuning voor veel brailleleesregels waaronder er veel zijn die automatisch herkend worden, alsmede brailleinvoer op brailleleesregels met een brailletoetsenbord
* Kan via usb-stick (flash drive) of ander draagbare media worden gedraaid zonder dat installatie nodig is
* Eenvoudige installatie dankzij gesproken ondersteuning
* In 54 talen beschikbaar
* Ondersteuning van moderne Windows besturingssystemen met inbegrip van 32- en 64-bit versies
* kan gebruikt worden tijdens Windows-aanmelding en voor [andere beveiligde schermen](#securescreens).
* Besturingselementen en tekst worden gemeld bij gebruik van aanraakgebaren
* Ondersteuning van gangbare toegankelijkheidsinterfaces zoals Microsoft Active Accessibility, Java Access Bridge, Iaccessible 2 en UI Automation
* Ondersteuning voor Windows commandoprompts en consoletoepassingen
* Mogelijkheid de systeemfocus uit te lichten

### Systeemvereisten {#SystemRequirements}

* Besturingssystemen: alle 32-bit en 64-bit edities van Windows 8.1, Windows 10, Windows 11, en alle Server besturingsSystemen vanaf  Windows Server 2012 R2.
  * zowel AMD64- als ARM64-varianten van Windows worden ondersteund.
* tenminste 150 mb aan opslagruimte.

### Internationalisering {#Internationalization}

Het is belangrijk dat mensen overal ter wereld, ongeacht de taal die zij spreken, gelijke toegang krijgen tot technologie.
Behalve de Engelse versie van NVDA is het programma beschikbaar in nog 54 andere talen, waaronder Afrikaans, Albanees, Amherisch, Arabisch, Aragonees, bulgaars, Birmees, Catalaans, Chinees (Vereenvoudigd en Traditioneel), Croatisch, Deens, Duits (Duitsland en Zwitserland), Fins, Frans, Galisisch, Georgisch, Grieks, Hebreeuws, Hindi, Hongaars, Iers, IJslands, Italiaans, Japans, Kannada, Koreaans, Kyrgyzisch, Litouws, Macedonisch, Mongools, Nederlands, Nepalees, Noors, Oekraïens, Pharsi, Pools, Portugees (Brazilië en Portugal), Punjabi, Roemeens, Russisch, Servisch, Sloveens, Slowaaks, Spaans (Spanje en Columbië), Tamil, Thai, Tsjechisch, Turks, Viëtnamees en Zweeds.

### Ondersteuning voor spraaksynthese {#SpeechSynthesizerSupport}

Je kunt een van de momenteel beschikbare talen kiezen om meldingen van NVDA, de interface of de inhoud van documenten te laten voorlezen, maarhet is ook mogelijk content te laten voorlezen in een willekeurige andere taal als op de pc een spraakmodule is geïnstalleerd die die taal spreekt.

De gratis, open source spraakmodule [eSpeak NG](https://github.com/espeak-ng/espeak-ng), die over een groot aantal talen beschikt, is standaard in de NVDA screen reader opgenomen.

Onder [Ondersteunde spraaksynthesizers](#SupportedSpeechSynths) vindt u informatie over andere door NVDA ondersteunde spraaksynthesizers.

### Brailleondersteuning {#BrailleSupport}

Gebruikers van Brailleleesregels kunnen met NVDA informatie in braille uitlezen.
NVDA gebruikt [LibLouis](https://liblouis.io/), een open-source programma,  voor het omzetten van tekst in braille.
Braille-invoer, zowel onverkort als verkort braille, door middel van een brailletoetsenbord wordt ook ondersteund.
Bovendien herkent NVDA standaard veel brailleleesregels automatisch.
Voor de ondersteunde leesregels, zie [Ondersteunde brailleleesregels](#SupportedBrailleDisplays)

NVDA ondersteunt Braillecodes in veel talen met inbegrip van braillecodes voor verkort en onverkort Braille alsmede computerbraille.

### Licentie en Copyright {#LicenseAndCopyright}

NVDA is auteursrechtelijk beschermd NVDA_COPYRIGHT_YEARS NVDA contributors.

NVDA is beschikbaar op basis van de GNU General Public License (Versie 2) waarop 2 specifieke uitzonderingen zijn.
Deze uitzonderingen staan omschreven in het document inhoudende de licentietekst in de paragrafen "Non-GPL Components in Plugins en Drivers" alsmede "Microsoft Distributable Code".
NVDA omvat en maakt ook gebruik van componenten die beschikbaar zijn op basis van verschillende gratis en open source licenties.
De software mag met anderen worden gedeeld of naar believen worden aangepast onder voorwaarde dat de licentie tezamen met de 	software wordt verspreid en de volledige broncode ter beschikking wordt gesteld aan iedereen die dat wil.
Dit is van toepassing voor zowel originele als aangepaste kopieën van de software alsmede voor software die gebruik maakt van code uit de NVDA-software.

Voor verdere bijzonderheden kunt u  de volledige licentie [raadplegen.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Voor details betreffende uitzonderingen kunt u het licentiedocument raadplegen in het NVDA-menu onder "help".

## Snel aan de Slag met NVDA {#NVDAQuickStartGuide}

Deze snelstartgids heeft drie hoofdrubrieken: downloaden, instellen voor gebruik en NVDA draaien.
Daarna volgt informatie over het wijzigen van Voorkeuren, gebruiken van Add-ons, participeren in de (NVDA-)gemeenschap en over het verkrijgen van hulp.
De informatie in deze snelstartgids is de beknopte weergave van wat elders in de gebruikershandleiding van NVDA uitgebreid aan bod komt.
Raadpleeg de volledige gebruikershandleiding voor meer gedetailleerde informatie over de afzonderlijke onderwerpen.

### NVDA Downloaden {#GettingAndSettingUpNVDA}

Iedereen kan NVDA gratis gebruiken.
Geen zorgen over de aanschaf van een licentie of duur abonnement.
Gemiddeld krijgt NVDA vier keer per jaar een update.
De recentste versie van NVDA is altijd beschikbaar op de "Download"-pagina van de [NV Access website](NVDA_URL).

NVDA is geschikt voor alle recente versies van Microsoft Windows.
Raadpleeg [Systeemvereisten](#SystemRequirements) voor alle bijzonderheden.

#### NVDA Download-procedure {#StepsForDownloadingNVDA}

Er wordt hier van uitgegaan dat u enigszins bekend bentmet het navigeren op een webpagina.

* Open uw webbrowser (Druk op de `Windows-toets`, typ het woord "internet" zonder aanhalingstekens en druk op `enter`)
* Laad de download-pagina van NV Access (Druk `alt+d` in, typ het volgende adres en druk vervolgens op `enter`): 
https://www.nvaccess.org/download: 
* Activeer de "download-knop"
* Na het downloaden krijgt u al dan niet een prompt van de browser om verder te gaan waarna u de  download start
* Afhankelijk van de gebruikte browser, zal het bestand automatisch worden uitgevoerd nadat het downloaden is voltooid
* Als het bestand handmatig geactiveerd moet worden druk dan `alt+n` in om naar het notificatiepaneel te gaan, dan `alt+r` indrukken om het bestand uit te voeren (of de aanwijzingen voor uw browser)

### NVDA instellen voor gebruik {#SettingUpNVDA}

Door het bestand dat u zojuist heeft gedownload uit te voeren wordt er een tijdelijke kopie van NVDA gestart.
Vervolgens wordt u gevraagd of u NVDA wilt installeren, een draagbare kopie wilt aanmaken of de tijdelijke kopie wilt blijven gebruiken.

Als het uitvoerbestand eenmaal is gedownload,  is verbinding met het Internet om NVDA te draaien of te installeren niet langer nodig.
Met een beschikbare internetverbinding kan NVDA regelmatig op updates controleren.

#### Gebruiksmogelijkheden van het gedownloade uitvoerbestand {#StepsForRunningTheDownloadLauncher}

Het setup-bestand  heeft als naam "nvda_2022.1.exe" of iets dergelijks.
Het jaar en de versie verschilt al naar gelang van de betreffende update.

1. Het gedownloade bestanduitvoeren 
Er klinkt een muziekje terwijl er een tijdelijke  kopie van NVDA wordt geladen.
Als deze eenmaal geladen is, biedt NVDA spraakondersteuning gedurende het verdere verloop van het proces.
1. Tegelijk met het  NVDA dialoogvenster van de Launcher verschijnt de licentieovereenkomst.
Druk op `PijlOmlaag` om, desgewenst, de licentieovereenkomst te lezen.
1. Druk op `tab` om naar het "Ik ga akkoord" selectievakje te gaan. Druk nu op de `spatiebalk` om dit vakje aan te kruisen.
1. Druk `tab` om de verschillende opties te verkennen, druk dan `enter` bij de gewenste optie.

De opties zijn: 

* "Installeer NVDA op deze computer": Dit is de meest gekozen optie met veel gebruiksgemak. 
* "Maak draagbare kopie aan": Hiermee kunt u NVDA in elke willekeurige map opslaan voor gebruik zonder het programma te installeren.
Dit is handig op computers waar u niet over admin-rechten beschikt, of op een  geheugen-stick die u meeneemt.
Als u hiervoor kiest, voert NVDA u stapsgewijs door het proces voor het aanmaken van een draagbare kopie.
Het belangrijkste dat NVDA moet weten is in welke map de draagbare kopie moet worden ondergebracht. 
* Doorgaan": Dit zorgt ervoor dat de tijdelijke kopie van NVDA actief blijft.
Dit is nuttig  als u features in een nieuwe versie wilt testen voordat u overgaat tot installatie.
Als u hiervoor kiest, zal het launcher-venster worden gesloten en blijft de tijdelijke kopie van NVDA actief totdat u deze afsluit of u de PC uitzet.
Merk op dat eventuele wijzigingen in de instellingen niet worden opgeslagen.  
* "Annuleren": Hiermee wordt NVDA afgesloten zonder verdere actie.

Als u van plan bent NVDA altijd op deze computer, te gebruiken, zult u er zeer waarschijnlijk voor kiezen om NVDA te installeren.
Een geïnstalleerde versie biedt extra functionaliteit, zoals het automatisch starten van het programma na aanmelding bij Windows en de mogelijkheid het Windows Aanmeldvenster en [Beveiligingsschermen](#SecureScreens) uit te lezen.
Met een draagbare en / of tijdelijke kopie is dit alles niet mogelijk.
Voor alle bijzonderheden  betreffende de beperkingen die samenhangen met het gebruik van een draagbare of tijdelijke kopie van  NVDA, raadpleegt uBeperkingen van Draagbare en Tijdelijke Kopieën #PortableAndTemporaryCopyRestrictions].

Door te Installeren wordt u ook de mogelijkheid geboden sneltoetsen voor Start Menu en  het bureaublad aan te maken, en tevens kunt u NVDA inschakelen met `control+alt+n`.

#### Procedure voor het installeren  van NVDA vanaf de launcher {#StepsForInstallingNVDAFromTheLauncher}

Hierbij komen de meest gebruikelijk setup opties aan de orde.
Raadpleeg voor meer details betreffende  de beschikbare opties [Installatie-opties](#InstallingNVDA).

1. Zorg dat het selectievakje van het dialoogvenster van de launcher, waarmee u aangeeft akkoord te gaan met de licentieovereenkomst, is aangevinkt.
1. `Tab` naar, en activeer de knop "Installeer NVDA op deze computer".
1. Vervolgens komen er opties om NVDA te gebruiken voor aanmelding bij Windows en om een snelkoppeling voor het bureaublad aan te maken.
Deze opties staan standaard aan.
Als u wilt, kunt u met `tab` en de `spatiebalk` deze opties, aanpassen of de standaardinstellingen  laten staan.
1. Druk op `enter` om verder te gaan.
1. Er verschijnt nueen UAC(User Account Control)"-dialoogvenster  met de vraag Wilt u toestaan dat deze app wijzigingen aan uw PC? aanbrengt".
1. Druk op `alt+`j` om de UAC-prompt te accepteren.
1. Het verloop van de installatie wordt via een voortgangsbalk weergegeven.
Tijdens dit proces laat NVDA een in hoogte toenemend piepsignaal horen.
Dit proces verloopt vaak snel  en mogelijk zonder dat u het opmerkt.
1. Er verschijnt een  dialoogvenster  met de mededeling dat de installatie van NVDA geslaagd is.
U wordt aangeraden op OK te drukken om de geïnstalleerde kopie" te starten.
Druk op `enter` om de geïnstalleerde kopie te starten.
1. U komt nu in het scherm "Welkom bij NVDA" en u krijgt een welkomsboodschap te horen.
De focus staat op het vervolgkeuzemenu  "Toetsenbordindeling".
Standaard gebruikt de "Desktop-toetsenbordindeling" het numerieke deel van het toetsenbord voor bepaalde functies.
Desgewenst kunt u met 'PijlOmlaag' kiezen voor "Laptop-toetsenbordindeling" om functies van het numerieke toetsenbord toe te wijzen aan andere toetsen.
1. Druk op `tab` om naar "Gebruik `capsLock` als een NVDA-programmatoets" te gaan.
`Insert` staat standaard ingesteld als de NVDA-programmatoets.
Druk op de `spatiebalk` om `capsLock` als een extra programmatoets te selecteren.
Merk op dat de toetsenbordindeling en de NVDA-programmatoets afzonderlijk worden ingesteld.
De NVDA-toets  en de toetsenbordindeling kunnen later via het menuonderdeel toetsenbordinstellingen worden gewijzigd.
1. Gebruik `tab` en `spatiebalk` om de verdere opties op dit scherm aan te passen.
Hiermee stelt u in of NVDA automatisch moet opstarten.
1. NVDA is nu actief en door op `enter` te drukken zal het dialoogvenster worden gesloten.

### Werken met  NVDA {#RunningNVDA}

De volledige  gebruikershandleiding van NVDA bevat een gerubriceerd Overzicht met NVDA-commando's.
De tabellen met commando's zijn ook te vinden in het "Overzicht Commando's".
De module "Basis training voor NVDA" gaat dieper in op afzonderlijke commando's met daarbij behorende gestructureerde activiteiten.
"Basistraining voor NVDA" is verkrijgbaar  in de [NV Access Shop](http://www.nvaccess.org/shop).

Hieronder enkele vaak gebruikte basiscommando's.
Alle commando's zijn individueel instelbaar dus  dit zijn de standaard toetscombinaties voor de vermelde functies.

#### De NVDA-programmatoets {#NVDAModifierKey}

De standaard NVDA-programmatoets is of wel de `numrieke Nul`, met `numLock` UIT), of de `insert-toets`, nabij de toetsen `delete`, `home` en `end`.
Als NVDA-programmatoets kunt u ook de  `capsLock-toets` gebruiken.

#### Invoerhulp {#InputHelp}

Om  plaats en rol van toetsen te leren kennen, drukt u op `NVDA+1` waarmee u Invoerhulp inschakelt.
Zo lang u in de Invoerhulp-modus bent, zult u van elke invoerhandeling (het indrukken van een toets dan wel  een veeg- of tikgebaar) te horen krijgen om welke handeling het gaat, voor zover die is toegekend, en waartoe deze dient.
Het eigenlijke commando wordt niet uitgevoerd wanneer u in de Invoerhulpmodus bent.

#### NVDA Starten en stoppen {#StartingAndStoppingNVDA}

| Naam |Desktop-toets |Laptop-toets |Omschrijvingn|
|---|---|---|---|
|NVDA starten |`control+alt+n` |`control+alt+n` |Start of herstart NVDA|
|NVDA afsluiten |`NVDA+q`, dan `enter` |`NVDA+q`, dan `enter` |Beëindigt NVDA|
|Pauzeert of hervatt spraakuitvoer |`shift` |`shift` |Hiermee wordt de spraak onderbroken, bij nogmaals indrukken gaat spraakuitvoer weer verder|
|Spraak stoppen |`control` |`control` |Stopt de spraak onmiddellijk|

#### tekst lezen {#ReadingText}

| Naam |Desktop-toets |Laptop-toets |Omschrijving|
|---|---|---|---|
|Alles lezen |`NVDA+pijlOmlaag` |`NVDA+a` |Starts Lezen begint vanaf de huidige positie en dat stopt als er niets meer te lezen is.|
|Huidige regel lezen |`NVDA+pijlOmhoog` |`NVDA+l` |Regel wordt voorgelezen. Druk 2maal om regel te laten spellen. Druk 3maal om regel te laten spellen met gebruik van spellingalfabet (Alpha, Bravo, Charlie, etc)|
|Geselecteerde tekst lezen |`NVDA+shift+pijlOmhoog` |`NVDA+shift+s` |Wat er aan geselecteerde tekst is, wordt voorgelezen Bij tweemaal drukken wordt de selectie gespeld. Door driemaal te drukken wordt er gebruik gemaakt van een spellingsalfabet bij het spellen|
|Tekst van het klembord lezen |`NVDA+c` |`NVDA+c` |Tekst die op het klembord staat wordt gelezen Bij tweemaal drukken wordt de selectie gespeld. Door driemaal te drukken wordt er gebruik gemaakt van een spellingsalfabet bij het spellen|

#### locatie en andere informatie melden {#ReportingLocation}

| Naam |Desktop-toets |Laptop-toets |Omschrijving|
|---|---|---|---|
|Venstertitel |`NVDA+t` |`NVDA+t` |Meldt de titel (naam) van het venster dat momenteel actief is. Pressing twice will spell the information. Pressing three times will copy it to the clipboard|
|Focus melden |`NVDA+tab` |`NVDA+tab` |Meldt het besturingselement dat focus.  heet, Bij tweemaal drukken wordt het element dat de focus heeft gespeld. Door driemaal te drukken wordt er gebruik gemaakt van een spellingsalfabet bij het spellen|
|Venster uitlezen |`NVDA+b` |`NVDA+b` |Hiermee wordt het hele, huidige venster uitgelezen (Handig voor dialoogvensters)|
|Statusbalk lezen |`NVDA+end` |`NVDA+shift+end` |Melden van  de Statusbalk als NVDA er 1 vindt. Druk 2maal om de informatie te laten spellen. Bij driemaal drukken wordt deze naar het klembord gekopieerd|
|Tijd melden |`NVDA+f12` |`NVDA+f12` |Eenmaal drukken meldt de huidige tijd, tweemaal drukken meldt datum. De tijd en datum worden gemeld overeenkomstig de indelingsopmaak zoals gespecifieerd in de Windows-instellingen voor de klok in het systeemvak.|
|Textopmaak melden |`NVDA+f` |`NVDA+f` |Tekstopmaak wordt gemeld. Bij tweemaal drukken verschijnt de informatie in een venster|
|Koppelingsbestemming melden |`NVDA+k` |`NVDA+k` |Bij 1 keer drukken hoort u naar welke url de koppeling bij huidige positie van de muisaanwijzer of focus verwijst. Tweemaal drukken laat deze zien in een venster voor meer duidelijkheid|

#### Instellen welke informatie NVDA voorleest {#ToggleWhichInformationNVDAReads}

| Naam |Desktop-toets |Laptop-toets |Omschrijving|
|---|---|---|---|
|Getypte lettertekens uitspreken |`NVDA+2` |`NVDA+2` |Deze instelling zorgt ervoor dat NVDA elk(e) letter, cijfer of symbool die / dat u typt uitspreekt.|
|Getypte woorden uitspreken |`NVDA+3` |`NVDA+3` |Deze instelling zorgt ervoor dat NVDA elke woord dat u typt uitspreekt.|
|Commandotoetsen uitspreken |`NVDA+4` |`NVDA+4` |Deze instelling zorgt ervoor dat NVDA de toetsen die niet dienen om letters, cijfers of symbolen te typen, uitspreekt. Hieronder vallen ook toetscombinaties zoals control plus een andere letter.|
|Muis volgen AAN |`NVDA+m` |`NVDA+m` |Deze instelling zorgt ervoor dat NVDA de tekst onder de muisaanwijzer, voorleest terwijl de muis over het scherm wordt verplaatst. Zo kunt u naar iets zoeken op het scherm door de muis met de hand te verplaatsen in plaats van te proberen iets te vinden door middel van objectnavigatie.|

#### The synth settings ring {#TheSynthSettingsRing}

| Naam |Desktop-toets |Laptop-toets |Omschrijving|
|---|---|---|---|
|Ga naar  volgende synth setting |`NVDA+control+pijlRechts` |`NVDA+shift+control+pijlRechts` |Gaat verder naar de eerstvolgend beschikbare spraakinstelling na de momenteel ingestelde, en begint weer bij de eerste instelling nadat de laatste is gepasseerd|
|Ga naar vorige synth setting |`NVDA+control+pijlLinks` |`NVDA+shift+control+pijlLinks` |Gaat naar de eerstvolgend beschikbare spraakinstelling die aan de huidige vooraf gaat en springt verder naar de laatste instelling  na het passeren van de eerste|
|Huidige synth setting stapsgewijs oplopend wijzigen |`NVDA+control+pijlOmhoog` |`NVDA+shift+control+pijlOmhoog` |Verhoogt of wijzigt de actuele instelling voor spraak. De spreeksnelheid wordt bijvoorbeeld verhoogd, volgende stem wordt gekozen, volume  gaat omhoog|
|De huidige synthesizer-instelling in grotere stappen oplopend bijstellen |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Verhoogt de waarde van de momenteel geldende spraakinstelling met een groter bereik. Als je bijv wilt veranderen van stem, spring je steeds 20 stemmen vooruit; voor aanpassingen met een schuifbalk (snelheid, toonhoogte, etc) wordt de waarde met tot 20% verhoogd.|
|Huidige synth setting stapsgewijs aflopend wijzigen |`NVDA+control+pijlOmlaag` |`NVDA+shift+control+pijlOmlaag` |Verlaagt of wijzigt de actuele instelling voor spraak. De spreeksnelheid wordt bijvoorbeeld verlaagd, vorige stem wordt gekozen, volume  gaat omlaag|
|De huidige synthesizer-instelling in grotere stappen aflopend bijstellen |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Verlaagt de waarde van de momenteel geldende spraakinstelling met een groter bereik. Als je bijv wilt veranderen van stem, spring je steeds 20 stemmen terug; voor aanpassingen met een schuifbalk (snelheid, toonhoogte, etc) wordt de waarde met tot 20% verlaagd.|

Het is ook mogelijk de eerste of laatste waarde van de huidige synthesizer-instelling in te stellen  door een aangepaste invoerhandeling toe te kennen [via het dialoogvenster](#InputGestures), in de categorie Spraak.
Dit houdt bijv in dat een instelling voor de spraaksnelheid op 0 of 100 wordt gezet.
Gaat het om het wijzigen van de spraakstem, dan wordt zo de eerste of de laatste stem ingesteld.

#### Navigeren op het Web {#WebNavigation}

De volledige lijst met de Letternavigatietoetsen  staat in de rubriek  [Bladermodus](#BrowseMode) van de gebruikershandleiding.

| Commandotoets |Omschrijving|
|---|---|
|Heading (Kop) |`h` |Ga naar de volgende kop|
|Heading level 1, 2, of 3 |`1`, `2`, `3` |Ga naar  de kop van het aangegeven niveau|
|Formulierveld |`f` |Ga naar het volgende formulierveld (edit box, button, etc)|
|Link |`k` |Ga naar de volgende link|
|Landmark (oriëntatiepunt) |`d` |Ga naar het volgende oriëntatiepunt|
|Lijst |`l` |Ga naar de volgende lijst|
|Tabel |`t` |Ga naar de volgende tabel|
|Achteruit gaan |`shift+letter` |Druk op `shift` en een van de letters hierboven om naar het vorige element van het bijbehorende type te gaan|
|Elementenlijst |`NVDA+f7` |Opsomming van verscheidene elementtypes zoals links en headings|

### Voorkeuren {#Preferences}

De meeste NVDA-functies kunnen via de NVDA-instellingen worden geactiveerd of aangepast.
Instellingen, en andere opties, zijn via het NVDA-menu te bereiken.
Om het NVDA-menu, te openen drukt u op `NVDA+n`.
Om het dialoogvenster met de algemene instellingen van NVDA rechtstreeks te openen drukt u op `NVDA+control+g`.
Veel schermen  met instellingen kunnen met toetscombinaties rechtstreeks geopend worden, bijvoorbeeld `NVDA+control+s` voor een synthesizer, of  `NVDA+control+v` voor andere stemmen met bijbehorende opties.

### Add-ons {#Addons}
Add-ons zijn programmaatjes  die nieuwe of gewijzigde functionaliteit voor NVDA bieden.
Add-ons worden door de NVDA-gemeenschap ontwikkeld , of door externe bedrijven die niet aan NV Access gelieerd zijn.
Wat voor alle software geldt, geldt ook hier; je vertrouwen kunnen stellen in de ontwikkelaar van een add-on voordat je die gaat gebruiken is belangrijk.
Raadpleeg [Add-ons installeren](#AddonStoreInstalling) om na te gaan hoe je de kwaliteit van  add-ons kunt verifiëren voordat je ze installeert.

Bij eerste opening van de Add-on Store zal NVDA een waarschuwing tonen over add-ons.
Add-ons worden door NV Access niet doorgelicht en hebben mogelijk mbt de functionaliteit en toegang tot informatie geen restricties.
Druk op de `spatiebalk` als je de waarschuwing hebt gelezen en je deze een volgende keer niet meer wilt zien.
Druk op `tab` om naar de "OK-knop" te gaan dan `enter` om de waarschuwing te accepteren en verder naar de Add-on Store te gaan.
+In de rubriek   "[Add-ons en de Add-on Store](#AddonsManager)" van de gebruikershandleiding vind je informatie over alle aspecten van de Add-on Store.

Je bereikt de Add-on Store via het menu Extra.
Druk op `NVDA+n` om het NVDA-menu te openen, dan op `e` voor extra, dan op `a` voor Add-on Store.
Wanneer de Add-on Store open gaat, worden beschikbare add-ons" getoond als er geen add-ons geïnstalleerd zijn.
Als er al  add-ons geïnstalleerd zijn, gaat de Add-on Store open op het  tabblad "Geïnstalleerde add-ons".

#### Beschikbare add-ons {#AvailableAddons}
Bij eerste opening van het venster kan het enkele seconden duren voordat de add-ons geladen zijn.
NVDA zal de naam van de eerste add-on voorlezen zodra het laden van de  lijst met add-ons voltooid is.
Beschikbare add-ons worden alfabetisch gerankschikt in de lijstweergave die uit meer kolommen bestaat.
Zo ga je door de lijst om meer te weten te komen over een specifieke add-on:


1. Gebruik de pijltjestoetsen of druk de eerste letter in van de naam van een add-on om de lijst te doorlopen.
1. Druk eenmaal op `tab` om naar de beschrijving van de op dat moment geselecteerde add-on te gaan.
1. Gebruik de [Leestoetsen](#ReadingText) of de pijltjestoetsen om de volledige beschrijving te lezen.
1. Druk op `tab` om bij de knop "Acties" te komen, waarmee je o.a. de add-on kunt installeren.
1. Druk op `tab` voor meer Details", zoals naam van de uitgever, versie en homepage.
1. Om terug te gaan naar de  lijst met beschikbare add-ons, druk je op  `alt+a`, dan wel op  `shift+tab`.

#### Naar add-onszoeken  {#SearchingForAddons}
Naast bladeren door alle beschikbare add-ons, is het ook mogelijk getoonde add-ons te sorteren.
Om te zoeken druk je op `alt+s` om naar het "zoekveld" te springen en typ daarin dan de tekst waarmee je wilt zoeken.
Je zoekopdracht zal proberen overeenkomsten te vinden in het veld   add-on ID, schermnaam, uitgever, auteur en beschrijving.
Tijdens het typen van de zoektermen past de lijst zich steeds aan.
Eenmaal gereed, druk je op `tab` om naar de gesorteerde lijst met add-ons te gaan waar je de zoekresultaten kunt bekijken.

#### Add-ons installeren {#InstallingAddons}

Zo installeer je een add-on:

1. Terwijl de focus op een add-on staat die je wilt installeren druk je op enter`.
1. Het menu  acties opent zich en er verschijnt een lijst met mogelijke acties; de eerste actie is "Installeren".
1. Om de add-on te installeren druk je op `i`, of op `pijlOmlaag` tot bij `Installeren` en druk je op `enter`.
1. De focus gaat terug naar de add-on in de lijst en NVDA zal de details over de add-on voorlezen.
1. Betreffende de  "Status" meldt NVDA dat deze verandert van "Beschikbaar " in "Downloading".
1. Als het downloaden van de add-on voltooid is, verandert deze in "Gedownload. In afwachting van installatie".
1. Herhaal het voorafgaande bij elke add-on die je verder tegelijkertijd  wilt installeren.
1. Als je klaar bent, druk je op `tab` totdat de focus op de knop "Sluiten" staat, waarna je op  `enter` drukt.
1. Het installeren van de gedownloade add-ons begint zodra de Add-on Store is afgesloten.
Er kunnen mogelijk dialoogvensters tijdens het installatieproces verschijnen waarop je dan wel moet reageren.
1. Als de add-ons eenmaal geïnstalleerd zijn,verschijnt er een dialoogvenster waarin wordt gemeld dat er wijzigingen zijn aangebracht, en dat NVDA opnieuw gestart moet worden om de installatie van de add-on(s) volledig af te ronden.
1. Druk op `enter` om NVDA te herstarten.

#### Geïnstalleerde add-ons beheren {#ManagingInstalledAddons}
Druk op `control+tab` om tussen de tabbladen van de Add-on Store te wisselen.
De tabbladen omvatten "Geïnstalleerde add-ons", "Bij te werken add-ons", "Beschikbare add-ons" en "Geïnstalleerde incompatibele add-ons".
De verschillende tabbladen zijn hetzelfde ingedeeld als lijst met add-ons, een paneel voor meer details over de geselecteerde add-on, en een knop waarmee acties uitgevoerd kunnen worden mbt de geselecteerde add-on.
Het actiemenu voor geïnstalleerde add-ons omvat "Uitschakelen" en "Verwijderen" ipv "Installeren".
Het uitschakelen van een add-on zorgt ervoor dat NVDA deze niet meer laadt maar de installatie ervan wordt niet ongedaan gemaakt.
Om een uitgeschakelde add-on, opnieuw in te schakelen kun je Inschakelen" activeren in het actiemenu.
Na het in- of uitschakelen dan wel verwijderen van add-ons, word je gevraagd NVDA te herstarten  bij het afsluiten van de Add-on Store.
Deze wijzigingen worden pas van kracht zodra NVDA herstart is.
Merk op dat in dit vemster van de Add-on Store `escape` hetzelfde werkt als de knop `Sluiten`.

#### Add-ons bijwerken {#UpdatingAddons}
Als er een update beschikbaar is voor een add-on die je geïnstalleerd hebt, tref je die aan in het tabblad met "Bij te werken add-ons".
Druk op  `control+tab` om naar dit tabblad te gaan vanuit elke willekeurige plaats in de Add-on Store.
De status van de add-on is voor zien van het predikaat "Update beschikbaar".
De lijst  toont de momenteel geïnstalleerde versie en de beschikbare versie.
Druk `enter` in op de add-on om de actie lijst te openen; kies "Bijwerken".

### Community {#Community}

NVDA kent een levendige gebruikersgemeenschap.
Zo is er een  [veel gebruikte, belangrijke engelstalige emaillijst](https://nvda.groups.io/g/nvda) en een pagina vol [gebruikersgroepen in de taal van de respectieve geografische locaties](https://github.com/nvaccess/nvda-community/wiki/Connect).
NV Access, makers van NVDA, zijn actief op [Twitter](https://twitter.com/nvaccess) en [Facebook](https://www.facebook.com/NVAccess).
NV Access post ook regelmatig via het  [In-Process blog](https://www.nvaccess.org/category/in-process/).

Er bestaat ook een door [NVDA Gecertificeerd Expert programma](https://certification.nvaccess.org/).
Dit is een online examen dat u kunt afleggen om te laten zien hoe vaardig u bent met NVDA.
[NVDA Certified Experts](https://certification.nvaccess.org/) kunnen hun contactgegevens en relevante zakelijke informatie hier presenteren.

### Hulp verkrijgen {#GettingHelp}

Om naar Help te gaan van  NVDA, drukt u op `NVDA+n` om het  menu,  te openen, vervolgens op `h` voor hulp.
Via dit submenu hebt u toegang tot de Gebruikershandleiding, een commandooverzicht, de geschiedenis van vernieuwingen / verbeteringen en meer.
Deze drie opties worden geopend in de standaard web-browser.
Er  is ook nog meer uitgebreid Trainingsmateriaal beschikbaar  in de [NV Access Shop](https://www.nvaccess.org/shop).

We raden aan te beginnen  met de module  "Basistraining voor NVDA".
Deze module behandelt uiteenlopende onderwerpen van hoe begin ik tot surfen op het web en objectnavigatie gebruiken.
De module  is beschikbaar als:

* [Electronische tekst](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), waaronder begrepen Word DOCX, Web page HTML, eBook ePub and Kindle KFX.
* [Ingesproken MP3 audio](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [UEB Brailleboek](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) inclusief wereldwijde bezorging.

Andere  modules, en, tegen gereduceerde prijs,  de [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/), zijn in de [NV Access Shop](https://www.nvaccess.org/shop/) verkrijgbaar.

NV Access biedt ook betaalde  [telefonische ondersteuning aan](https://www.nvaccess.org/product/nvda-telephone-support/), hetzij in blokken, of als onderdeel van de [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Telefonische ondersteuning is met inbegrip van lokale nummers in Australië en de Verenigde Staten.

Via de [email-gebruikersgroepen](https://github.com/nvaccess/nvda/wiki/Connect) wordt heel veel onderlinge hulp en ondersteuning geboden, wat zeker ook geldt voor het werk van de gecertificeerde NVDA-experts https://certification.nvaccess.org/].

Via [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md) kunnen bugs gemeld worden of features worden aangevraagd.
In de richtlijnen mbt bijdragen https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md] staat nuttige  informatie over het actief bijdragen aan het NVDA-gebeuren.

## Meer Setup-opties {#MoreSetupOptions}
### InstallatieOpties {#InstallingNVDA}

als u NVDA rechtstreeks vanuit de gedownloade NVDA-launcher installeert , drukt u  de knop Installeer NVDA in.
Als u dit dialoogvenster al gesloten hebt of als u de installatie wilt uitvoeren vanuit een draagbare kopie, kies dan  voor NVDA Installeren   via het menu;  in het NVDA-menu onder Extra.

In het dialoogvenster dat verschijnt, wordt bevestigd dat  u NVDA wilt gaan installeren en er wordt in gemeld of het bij deze installatie gaat om het bijwerken van een eerdere installatie.
 Met het indrukken van de knop Doorgaan wordt de installatie van NVDA gestart.
 In dit dialoogvenster staan nog enkele opties  die hieronder worden verklaard.
 Zodra de  installatie voltooid is, verschijnt er een melding dat die  succesvol was.
 Door nu op OK te drukken zal de zojuist geïnstalleerde kopie van NVDA worden gestart.

#### Waarschuwing voor Incompatibele add-ons {#InstallWithIncompatibleAddons}

Als u reeds add-ons geïnstalleerd hebt, dan kunt u een waarschuwing krijgen dat incompatibele add-ons worden uitgeschakeld.
Voordat u op de knop Doorgaan  kunt drukken dient u het selectievakje aan te vinken om aan te geven dat u begrijpt dat deze add-ons zullen worden uitgeschakeld.
Er is ook een knop waarmee u kunt nagaan welke add-ons zullen worden uitgeschakeld.
Raadpleeg het dialoogvenster [incompatibele add-ons van](#incompatibleAddonsManager) voor meer hulp bij deze knop.
Na installatie, kunt u incompatibele add-ons op eigen risico opnieuw inschakelen vanuit de [Add-on Store](#AddonsManager).

#### Gebruik NVDA bij het aanmelden {#StartAtWindowsLogon}

Met deze optie bepaalt u of NVDA automatisch moet worden opgestart wanneer u zich in het Aanmeldscherm bevindt nog voordat u een wachtwoord hebt ingevoerd. 
Dit geldt ook voor Gebruikersaccountbeheer en [voor andere beveiligde schermen](#SecureScreens)
In geval van een nieuwe (of her-)installatie is deze optie standaard ingeschakeld.

#### Snelkoppeling voor het bureaublad aanmaken (ctrl+alt+n) {#CreateDesktopShortcut}

Met deze optie kunt u bepalen of er een snelkoppeling voor het bureaublad moet worden aangemaakt waarmee u NVDA kunt starten.
Als u ervoor kiest de snelkoppeling aan te maken, dient deze tevens als sneltoetscombinatie , "Ctrl+Alt+n", waarmee u NVDA ook altijd kunt starten

#### De Draagbare Configuratie naar Account van Huidige Gebruiker kopiëren {#CopyPortableConfigurationToCurrentUserAccount}

Met deze optie kunt u bepalen of de gebruikte instellingen van de NVDA kopie die momenteel actief is, moeten worden gekopieerd naar de configuratie van momenteel aangemelde gebruiker van de geïnstalleerde versie van NVDA.
Als u kiest voor kopiëren van de configuratie geldt dit niet voor eventuele andere gebruikers van het systeem en ook niet voor de systeemconfiguratie ten behoeve van aanmelding bij Windows  en bij [andere beveiligde schermen](#SecureScreens). 
Deze optie is alleen beschikbaar wanneer de installatie wordt uitgevoerd vanuit een draagbare kopie en niet wanneer u de installatie direct vanuit het downloadbestand uitvoert.

### Een draagbare Kopie aanmaken {#CreatingAPortableCopy}

Als u een draagbare kopie direct vanuit het downloadbestand aanmaakt, drukt u op de knop Draagbare Kopie Aanmaken. 
Als u het dialoogvenster reeds gesloten hebt of als u werkt met een geïnstalleerde versie van NVDA, kiest u Draagbare Kopie Aanmaken wat u vindt onder Extra in het NVDA menu.

In het dialoogvenster dat wordt geopend kunt u aangeven waar de draagbare versie moet worden aangemaakt.
Dit kan een map op de harde schijf zijn of op een USB stick dan wel op een ander type draagbare media. 
U vindt hier ook een optie waarmee de gebruikte NVDA instellingen van de momenteel aangemelde gebruiker kunnen worden gekopieerd naar de configuratie van de zojuist aangemaakte draagbare versie. 
Deze optie is alleen beschikbaar wanneer de draagbare kopie wordt aangemaakt vanuit een op uw computer geïnstalleerde kopie van NVDA en niet wanneer u de kopie direct vanuit het downloadbestand uitvoert.
Door op de knop Doorgaan te drukken wordt de draagbare kopie aangemaakt.
Zodra het aanmaken is voltooid, hoort u de melding dat dit gelukt is. 
Druk nu op OK om het dialoogvenster te sluiten.

### Beperkingen van de draagbare en tijdelijke kopie van NVDA {#PortableAndTemporaryCopyRestrictions}

Als u NVDA wilt meenemen op een USB stick of op andere beschrijfbare media, dan moet u kiezen voor het aanmaken van een draagbare kopie.
Met de geïnstalleerde kopie kan ook altijd een draagbare kopie worden aangemaakt.
Met de draagbare kopie zelf kunt u op elk gewenst moment NVDA op een PC installeren.
Als u NVDA echter naar media met het kenmerk alleen-lezen, zoals een CD, wilt kopiëren, moet u het downloadbestand daarvoor gebruiken.
Op dit moment kan de draagbare versie niet rechtstreeks van media met het kenmerk alleen-lezen worden uitgevoerd.

Het [NVDA installatiebestand](#StepForRunningTheDownloadLauncher) kan als tijdelijke kopie van NVDA worden gebruikt.
Met een tijdelijke kopie is opslaan van de instellingen van NVDA niet mogelijk.
Dit geldt eveneens voor het uitschakelen van het gebruik van de [Add-on Store](#AddonsManager).

 Draagbare en  tijdelijke kopieën van NVDA kennen de volgende beperkingen:

 * Automatisch opstarten tijdens en/of na aanmelding is niet mogelijk.

* Werken met toepassingen die met beheerdersrechten worden uitgevoerd is niet mogelijk, tenzij NVDA ook met deze rechten wordt uitgevoerd natuurlijk, (niet aan te bevelen),
* UAC-schermen (User Account Control) kunnen niet worden voorgelezen bij het starten van toepassingen die met beheerdersrechten worden uitgevoerd,
* Geen ondersteuning voor invoer via het aanraakscherm,
* Mogelijkheden zoals bladermodus en het uitspreken van getypte karakters bij apps uit de Windows Store zijn niet beschikbaar.
* Audio ducking (volume van het ene audiosignaal verlagen t.o.v. het andere) wordt niet ondersteund.

## Aan de slag met NVDA {#GettingStartedWithNVDA}
### NVDA starten {#LaunchingNVDA}

Als u NVDA hebt geïnstalleerd met het installatieprogramma, kunt u NVDA eenvoudig starten met de toetscombinatie Ctrl+Alt+n, of NVDA selecteren onder Programma’s in het Startmenu gevolgd door Enter.
U kunt het programma ook starten door in het dialoogvenster Uitvoeren de letters NVDA te typen en vervolgens Enter in te drukken.
Als NVDA al actief is, zal de toepassing opnieuw gestart worden.
U kunt ook [commandoregelopties opgeven](#CommandLineOption) waarmee u NVDA herstart (-r), beëindigt (-q), add -ons uitschakelt (--disable-addons), etc.

In geval van een geïnstalleerde versie slaat NVDA de configuratie standaard op in de map roaming application data van de huidige gebruiker (bijv. "`C:\Users\<user>\AppData\Roaming`").
Het is mogelijk dit te wijzigen en wel zodanig dat in plaats daarvan NVDA de configuratie ophaalt uitthe map met de lokale applicatiedata.
Raadpleeg voor meer details de paragraaf over [systeem-brede parameters](#SystemWideParameters).

Om de draagbare versie van NVDA te starten gaat u naar de map waarin u de uitgepakte bestanden hebt opgeslagen. Daar selecteert u NVDA.exe. Druk op de Entertoets of dubbelklik op het bestand.
Als NVDA reeds actief was, stopt de toepassng automatisch voordat de draagbare versie wordt gestart.

Bij het opstarten van het programma hoort u eerst een reeks in hoogte oplopende tonen die aangeven dat NVDA wordt geladen. 
Afhankelijk van de snelheid van uw PC, of, als wordt geladen van een usb-stick of andere wat trage media, kan het laden even duren.
Als het laden extra lang duurt, hoort u "NVDA wordt geladen. Even geduld....". 

Als u niets hoort, of u krijgt een foutmelding van Windows dan wel een in hoogte aflopende tonenreeks hoort, is er iets fout gegaan met het programma. U doet er dan goed aan dit te melden aan de ontwikkelaars van NVDA.
Op de NVDA website kunt u lezen hoe u dit kunt doen.

#### Welkomsscherm {#WelcomeDialog}

Wanneer NVDA de eerste keer start, komt u in het welkomstscherm van het programma dat u informatie geeft over de NVDA-toets en het NVDA-menu.
Verderop in deze handleiding kunt u hier meer over lezen.
Op het welkomsscherm treft u een vervolgkeuzemenu en 3 selectievakjes aan.
Via het vervolgkeuzemenu kunt u een toetsenbordindeling selecteren.
Als u het eerste selectievakje inschakelt, wordt de CapsLock-toets ook als NVDA-programmatoets gebruikt.
Als u het tweede selectievakje inschakelt, zal NVDA automatisch opstarten zodra u bij Windows bent aangemeld. Deze mogelijkheid is alleen beschikbaar voor de geïnstalleerde versie van NVDA. 
Het inschakelen van het derde selectievakje zorgt ervoor dat dit welkomsscherm verschijnt, telkens wanneer NVDA wordt gestart.

#### Dialoogvenster Gebruiksgegevensstatistiek {#UsageStatsDialog}

Met ingang van NVDA 2018.3, wordt de gebruiker gevraagd of hij / zij toestaat dat gegevens over het gebruik naar NV Access worden gestuurd met het doel NVDA verder te verbeteren.
Wanneer NVDA de eerste keer start, verschijnt er een dialoogvenster  met de vraag of u ermee akkoord gaat dat er gegevens naar NV Access worden gestuurd tijdens uw gebruik van NVDA.
U leest meer over de door NV Access verzamelde data in het onderdeel Algemene  Instellingen , [ NV Access toestaan NVDA-gebruiksstatistieken te verzamelen](#GeneralSettingsGatherUsageStats).
Merk op dat  door op "ja" of "nee"  te drukken  uw keuze wordt opgeslagen en dat  dit dialoogvenster dan niet meer zal verschijnen, tenzij u NVDA opnieuw installeert.
U kunt het verzamelen van data echter handmatig in- of uitschakelen via de Instellingen van NVDA in de categorie Algemeen. Om de instelling handmatig te wijzigen zet of verwijdert u een vinkje in het selectievakje  met bijschrift Sta het NVDA project toe NVDA gebruiksstatistieken te verzamelen #GeneralSettingsGatherUsageStats].

### Over NVDA toetsenbordcommando’s {#AboutNVDAKeyboardCommands}
#### De NVDA programmatoets {#TheNVDAModifierKey}

Voor de meeste commando's binnen NVDA drukt u op een bepaalde toets, de NVDA programmatoets (of kortweg NVDA-toets) in combinatie met een of meer andere toetsen.
Als uitzondering hierop noemen we de commando's die gebruikt worden om tekst te laten voorlezen. Hiervoor gebruikt u alleen de toetsen van het numerieke toetsenbord zonder de NVDA programmatoets (dit geldt voor de desktoptoetsenbordindeling). Er zijn echter nog enkele andere uitzonderingen. 

U kunt NVDA zo configureren dat de numerieke Insert-toets, de uitgebreide Insert-toets en / of de CapsLock-toets als NVDA programmatoets worden/wordt gebruikt.
Standaard zijn zowel de numerieke Insert als de uitgebreide Insert-toets als NVDA programmatoets ingesteld.

Om een toets die u als NVDA programmatoets hebt ingesteld zijn oorspronkelijke functie te laten uitvoeren, u wilt CapsLock bij voorbeeld inschakelen om hoofdletters te typen, moet u deze toets tweemaal snel achter elkaar indrukken.

#### Toetsenbordindeling {#KeyboardLayouts}

Momenteel beschikt NVDA over twee profielen met toetscommando's die toetsenbordindelingen worden genoemd: de desktoptoetsenbordindeling en de laptoptoetsenbordindeling. 
De standaardinstelling van NVDA is de Desktoptoetsenbordindeling, maar u kunt dit wijzigen in Laptoptoetsenbordindeling bij de categorie Toetsenbord in het dialoogvenster [Instellingen van NVDA](#NVDASettings) dat u vindt in het NVDA-menu onder Opties.

Bij de Desktoptoetsenbordindeling wordt zeer veel gebruik gemaakt van het numerieke toetsenbord waarbij num lock uit moet staan.
Hoewel de meeste laptops geen apart numeriek toetsenbord hebben, kan dit soms wel worden gesimuleerd door de FN-toets ingedrukt te houden en letters en cijfers in te toetsen op het rechterdeel van het toetsenbord (7, 8, 9, u, i, o, j, k, l, etc.).
Als dit niet mogelijk is op uw laptop of als u NumLock niet kunt uitschakelen, kunt u beter kiezen voor de laptop toetsenbordindeling. 

### NVDA Aanraakgebaren {#NVDATouchGestures}

Als u met NVDA werkt op een met een aanraakscherm uitgerust apparaat dan kunt u NVDA ook rechtstreeks met aanraakcommando's bedienen.
Terwijl NVDA actief is, gaat alle door aanraking gegenereerde invoer rechtstreeks naar NVDA tenzij de ondersteuning voor aanraakinteractie is uitgeschakeld.
Daarom zullen taken die normaal zonder NVDA kunnen worden uitgevoerd niet uitvoerbaar zijn.
<!-- KC:beginInclude -->
Om ondersteuning voor aanraakinteractie aan- of uit te zetten drukt u op NVDA+control+alt+t.
<!-- KC:endInclude -->
U kunt  [ondersteuning voor aanraakinteractie](#TouchSupportEnable) ook aan- of uitzetten viahet menu Instellingen van NVDA in de categorie Aanraakinteractie.

#### Het Beeldscherm Verkennen {#ExploringTheScreen}

De meest elementaire taak die met behulp van het aanraakscherm kan worden uitgevoerd is het spraakondersteunde uitlezen van het scherm, dus wat is er aanwezig aan besturingselementen, tekst en dergelijke.
U doet dit door één vinger op een willekeurige plaats op het scherm te zetten.
Als u uw vinger op het scherm houdt en hem over het scherm beweegt, zullen knoppen en tekst die u tegenkomt worden gemeld.

#### Aanraakgebaren {#ExploringTheScreen}

Bij de beschrijving van NVDA-commando's verderop in deze handleiding kunnen ook aanraakgebaren voorkomen die het bijbehorende commando via aanraking activeert.
Hier volgen wat aanwijzingen voor het maken van de aanraakgebaren.

##### Tikken {#tikken}

Met de top / toppen van één of meer vingers snel op het scherm tikken.

Eenmaal tikken met één vinger heet gewoon een tik.
Met 2 vingers tegelijkertijd tikken heet een tik met twee vingers (two-finger tap) enzovoort.

Een snelle opeenvolging van tikken wordt door NVDA geïnterpreteerd als een multi-tikgebaar.
Twee tikken snel achter elkaar heet een dubbele tik (double-tap),
drie tikken snel achter elkaar is een driedubbele tik (triple-tap), enzovoorts.
Bij deze multi-tikgebaren wordt ook herkend met hoeveel vingers de tikbeweging wordt gemaakt zodat er driedubbele tikken met twee vingers kunnen zijn, maar ook een tik met vier vingers.

##### Veegbewegingen {#Flicks}

Met de vinger of vingers snel over het scherm bewegen / vegen.

Er zijn vier mogelijke, richtingafhankelijke veegbewegingen: veeg links, veeg rechts, veeg omhoog en veeg omlaag. 

Net als bij tikken kunnen veegbewegingen met meer dan één vinger worden gemaakt.
Daarom komen gebaren zoals een veegbeweging links met twee vingers en een veegbeweging omhoog met vier vingers, etc. allemaal voor.

#### Aanraakmodi {#TouchModes}

Aangezien er veel meer NVDA-commando’s zijn dan mogelijke aanraakgebaren, kan in NVDA gewisseld worden tussen verschillende aanraakmodi die ervoor zorgen dat commando’s in groepen worden onderverdeeld.
De twee modi zijn de tekstmodus en de objectmodus.
Bij een aantal NVDA-commando’s die u in deze handleiding tegenkomt, wordt, na het aanraakgebaar, tussen haakjes de toepasselijke modus vermeld.
Zo betekent “veeg omhoog (tekst modus)” dat de NVDA-opdracht wordt uitgevoerd door een veegbeweging omhoog, echter moet de tekstmodus dan wel actief zijn.
Als er bij een bepaald commando geen modus wordt aangegeven wordt dit altijd uitgevoerd ongeacht in welke modus men zich bevindt.

<!-- KC:beginInclude -->
Wisselen tussen aanraakmodi doet u door eenmaal tikken met drie vingers.
<!-- KC:endInclude -->

#### Schermtoetsenbord {#TouchKeyboard}

Bij gebruik van een aanraakscherm dient het schermtoetsenbord voor het invoeren van tekst en commando's.
Wanneer een tekstinvoerveld de focus heeft, kunt u het schermtoetsenbord activeren door te dubbeltikken op het ikoontje van het schermtoetsenbord onderaan het scherm.
Bij tablets zoals de Surface Pro van Microsoft , is het schermtoetsenbord altijd beschikbaar zodra het toetsenbord uit het dock is gehaald.
Om het schermtoetsenbord te laten verdwijnen dubbeltikt u op het schermtoetsenbordikoon of gaat u uit het tekstinvoerveld.

De letters en tekens op het schermtoetsenbord vindt u door met een vinger naar het toetsenbord te gaan, gewoonlijk te vinden onderaan het scherm, waar u vervolgens met uw vinger de toets zoekt van uw keuze. Hiervoor moet het toetsenbord wel actief zijn.
Zodra u de toets die u wilt gebruiken hebt gevonden, dubbeltikt u op de toets of u haalt uw vinger van de toets al naar gelang de gekozen opties in de categorie [Aanraakinteractie-instellingen](#TouchInteraction) van de Instellingen van NVDA.

### Invoerhulpmodus {#InputHelpMode}

Er worden veel NVDA-commando’s genoemd in deze handleiding, maar om op een gemakkelijke manier de verschillende commando’s te leren kennen kunt u het beste Invoerhulp inschakelen. 

Om invoerhulp in te schakelen, drukt u op de NVDA-toets+1. 
Om deze functie uit te schakelen drukt u opnieuw op NVDA+1. 
Wanneer de invoerhulpfunctie is ingeschakeld, kunt u elke willekeurige toets indrukken of een aanraakgebaar maken om te horen wat de functie ervan is (voor zover deze in NVDA is toegewezen). 
Zolang u in de hulpmodus bent worden de commando’s niet echt uitgevoerd.

### Het NVDA-menu {#TheNVDAMenu}

Via het NVDA-menu kunt u de instellingen van het programma aanpassen, hulpinformatie opvragen, uw configuratie opslaan of teruggaan naar een eerder opgeslagen configuratie, uitspraakwoordenboeken aanpassen, extra opties instellen, NVDA afsluiten.

Om het NVDA-menu vanuit een willekeurige plaats in Windows op te kunnen roepen kunt u, mits NVDA actief is, op een van de volgende manieren te werk gaan: 

* druk de NVDA-toets +n in op het toetsenbord,  
* dubbeltik met twee vingers op het aanraakscherm, 
* Ga het systeemvak in door op `Windows+b` te drukken, `pijl omlaag naar  het NVDA-icoon, en druk op  ``enter`.
* Of ga het systeemvak in door op  `Windows+b` te drukken , `omlaag te pijlen` naar het NVDA-icoon, en het contextmenu te openen door op de `toepassingstoets` te drukken. Deze toets zit naast de rechter  control-toets op de meeste toetsenborden.
Op een toetsenbord zonder ``toepassingstoets`, drukt u in plaats daarvan op `shift+f10`.
* Klik met rechter muisknop op het NVDA-icoon dat zich in het Windows-systeemvak bevindt.

Als het menu open gaat kunt u de pijltjestoetsen gebruiken om doorheen het menu te navigeren, en met de `enter-toets` activeert een item.

### De NVDA-basiscommando’s {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Aanraken |Beschrijving|
|---|---|---|---|---|
|Start of herstart NVDA |Control+alt+n |Control+alt+n |geen |Hiermee Start of herstart u NVDA vanaf  het bureaublad, als  deze Windows sneltoets  wordt geactiveerd tijdens het installatieproces van NVDA. Het gaat hier om  een Windows-specifieke ssneltoetscombinatie en daarom  is het niet mogelijk  deze te wijzigen in het dialoogvenster Invoerhandelingen.|
|Spraak stoppen |Control |Control |1tik met 2 vingers |Spreken wordt gestopt|
|Spraak pauzeren |Shift |Shift |geen |Spraakuitvoer wordt gepauzeerd. Druk Shift opnieuw in om verder te lezen vanaf de pauzepositie(als de gebruikte synthesizer dit ondersteunt)|
|NVDA Menu |NVDA+n |NVDA+n |dubbeltik met 2 vingers |Opent het menu voor opties, extra, hulp, etc.|
|Invoerhulpmodus aan-/uitzetten |NVDA+1 |NVDA+1 |geen |Als de invoerhulpmodus is ingeschakeld hoort u bij elke toets die wordt ingedrukt de naam van de toets en de (eventuele) bijbehorende functie van de toets(en)|
|NVDA afsluiten |NVDA+q |NVDA+q |geen |Sluit NVDA af|
|Volgende toetsaanslag niet uitvoeren |NVDA+f2 |NVDA+f2 |geen |De volgende toetsaanslag zal niet als NVDA-commando worden verwerkt maar als commando binnen de gebruikte toepassing worden uitgevoerd.|
|Zet slaapmodus aan/uit voor huidige applicatie |NVDA+shift+s |NVDA+shift+z |geen |Slaapmodus schakelt alle NVDA commando's en uitvoer in spraak en braille uit. Dit is vooral handig bij applicaties die in hun eigen spraakuitvoer of schermlezer voorzien. Druk deze toets nogmaals in om slaapmodus weer uit te schakelen - merk op dat NVDA opnieuw gestart moet worden om de slaapmodus beschikbaar te houden.|

<!-- KC:endInclude -->

### Systeeminformatie melden {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Naam |Ttoets |Omschrijving|
|---|---|---|
|Datum/tijd melden |NVDA+f12 |Eenmaal indrukken laat huidige tijd horen, tweemaal snel indrukken meldt de datum|
|Batterijstatus melden |NVDA+shift+b |Meldt de batterijstatus, of de computer is aangesloten op netstroom en het batterijpercentage.|
|Tekst op het klembord melden |NVDA+c |Meldt de tekst op het klembord als die er  staat.|

<!-- KC:endInclude -->

### Spraakmodi {#SpeechModes}

Met de spraakmodus kan worden bepaald of en in hoeverre de inhoud van het schermzoals meldingen, de respons op commando's, en overige uitvoer wordt uitgesproken bij gebruik van NVDA.
De standaardmodus is "spreken", wat betekent dat er spraak gebruikt wordt in omstandigheden waar dat te verwachten is bij gebruik van een schermlezer.
Onder bepaalde omstandigheden echter of bij gebruik van specifieke programma's, kan een van de andere spraakmodi mogelijk goed van pas komen.

De vier beschikbare spraakmodi zijn:

* Spreken (standaard): NVDA zal in 't algemeen    met spraak reageren op veranderingen op het scherm, meldingen / mededelingen, en handelingen zoals het verplaatsen van de focus, of het ingeven van commando's.
* Op-aanvraag(On-demand): NVDA zal alleen dan spreken wanneer commando's met een  meldfunctie, (bijv. meld vensternaam); maar er is geen spraakuitvoer in reactie op handelingen zoals het verplaatsen van de focus of de cursor.
* Uit: NVDA spreekt helemaal niets uit, maar, in tegenstelling tot de slaapstand, zullen commando's stilzwijgend worden uitgevoerd.
* Piepjes: NVDA zal normale spraak vervangen door kortepieptonen.

The Piepjeskunnen van pas komen als er in een terminal-venster lappen tekst voorbij scrollen, maar wat er gezegd wordt, doet er niet toe; het blijven scrollen, daar gaat 't om. Of anderszins kan het zijn dat het feit dat er uitvoer is, meer relevant is dan de uitvoer zelf.

De On-demand-modus kan van pas komen wanneer  je niet constant feedback nodig hebt mbt hetgeen zich op het scherm afspeelt of op de computer, maar als je van tijd tot tijd bepaalde dingetjes na moet gaan met behulp van controlecommando's, etc.
Voorbeelden zijn o.a. bij het maken van geluidsopnames, wanneer schermvergroting wordt gebruikt, tijdens een vergaderintg of een telefoongesprek, of als alternatief voor piepjes.

Met een invoerhandeling doorloop je de beschikbare spraakmodi:
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Spraakmodi doorlopen |`NVDA+s` |Van de een naar de andere spraakmodus gaan.|

<!-- KC:endInclude -->

Als wisselen tussen spraakmodi slechts beperkt nodig is, kijk dan bij[Modi die beschikbaar zijn in de Cycle speech mode command](#SpeechModesDisabling) om te zien hoe je ongewenste modi uitschakelt.

## Navigeren met NVDA {#NavigatingWithNVDA}

Met NVDA kunt u op verschillende manieren door en in het systeem navigeren, zowel via normale interactie als via review.

### Objecten {#Objects}

Elk programma en het besturingssysteem zelf bestaat uit veel objecten.
Een object is een afzonderlijk element zoals een stuk tekst, knop, selectievakje, schuifregelaar, lijst of bewerkbaar tekstvak.

### Navigeren met de systeemfocus {#SystemFocus}

De systeemfocus, of kortweg de focus, is het [object](#Objects) waar de toetsen die op het toetsenbord worden aangeslagen betrekking op hebben ( de interactie).
Als u bijvoorbeeld in een tekstvak typt, heeft dit tekstvak de focus.

De meest gebruikelijke manier om met NVDA in Windows te navigeren is eenvoudigweg het verplaatsen van de systeemfocus met standaard Windows-toetsenbordcommando's, zoals het indrukken van tab en shift+tab om verder naar volgende en terug naar vorige besturingselementen te gaan, het indrukken van  alt om de menubalk te activeren en vervolgens met de pijltjes door menu's te navigeren, en met alt+tab van de ene naar de andere geactiveerde applicatie te gaan.
Terwijl je dit doet, zal NVDA informatie geven over het object dat focus heeft, zoals de naam, type, waarde, status, beschrijving, sneltoets en plaatsaanduiding.
Wanneer  [Visuele Uitlichting](#VisionFocusHighlight) geactiveerd is, wordt de plaats waar de huidige systeemfocus zich bevindt ook zichtbaar weergegeven.

Enkele toetscommando’s die van pas komen bij het verplaatsen van de systeemfocus:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Beschrijving|
|---|---|---|---|
|Huidige focus melden |NVDA+tab |NVDA+tab |laat horen welk object of besturingselement momenteel de focus heeft. Bij tweemaal indrukken wordt informatie gespeld|
|Titel/naam melden |NVDA+t |NVDA+t |Laat horen hoe het momenteel actieve venster heet. Bij tweemaal indrukken wordt de informatie gespeld. Bij driemaal indrukken wordt deze naar het klembord gekopieerd.|
|Actieve venster voorlezen |NVDA+b |NVDA+b |Leest de inhoud (knoppen, vervolgkeuzenenu’s,selectievakjes, etc.) voor. Handig voor dialoogvensters|
|Statusbalk voorlezen |NVDA+End |NVDA+Shift+End |Leest de statusbalk als NVDA deze kan vinden. Bij tweemaal indrukken wordt de informatie gespeld. Driemaal drukken zorgt ervoor dat deze naar het klembord wordt gekopieerd.|
|Sneltoets melden |`shift+numpad2` |`NVDA+control+shift+.` |Meldt de sneltoets voor het object dat momenteel de focus heeft|

<!-- KC:endInclude -->

### Navigeren met de systeemcursor {#SystemCaret}

Wanneer  er een [object](#Objects)  [focusheeft is](#SystemFocus) waarmee  tekst gelezen kan worden of bewerkt kan worden, kunt u de systeemcursor gebruiken om door de tekst te navigeren. De systeemcursor wordt ook wel de tekstcursor genoemd.

Als een object met de systeemcursor is gefocusseerd, kunt u de pijltoetsen, pageUp, pageDown, home, end, etc gebruiken om door de tekst te navigeren.
U kunt de tekst ook wijzigen als het object het wijzigen van tekst ondersteunt.
NVDA meldt of u navigeert per teken, woord of regel. Ook wordt het selecteren en het ongedaan maken van de selectie gemeld.

U kunt de volgende NVDA-toetscommando's gebruiken om met de textcursor te navigeren:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Beschrijving|
|---|---|---|---|
|Alles voorlezen |NVDA+pijl omlaag |NVDA+a |Voorlezen starten vanaf de huidige positie van de tekstcursor die tijdens het lezen wordt verplaatst.|
|Deze regel lezen |NVDA+pijl omhoog |NVDA+l |Hiermee wordt de regel waarin de tekstcursor zich momenteel bevindt voorgelezen. Bij tweemaal drukken wordt regel gespeld. bij driemaal drukken wordt regel gespeld met gebruikmaking van spellingsalfabet.|
|Geselecteerde tekst lezen |NVDA+Shift+pijl omhoog |NVDA+Shift+s |Hiermee wordt geselecteerde tekst voorgelezen.|
|Tekstopmaak melden |NVDA+f |NVDA+f |Meldt  de opmaakkenmerken van de tekst op  de huidige cursorpositie. Bij tweemaal  drukken wordt de informatie weergegeven in bladermodus.|
|Einddoel van koppeling melden |`NVDA+k` |`NVDA+k` |Bij eenmaal drukken hoor je de URL van de link bij de huidige positie van de caret of van de focus. Bij tweemaal drukken wordt deze in een venster getoond om nauwkeurigere inspectie mogelijk te maken.|
|Cursorlocatie melden| NVDA+numeriekDelete |NVDA+delete |Meldt informatie over de locatie van de tekst of het object ten opzichte van de positie van de systeemcursor. Hieronder kan bij voorbeeld vallen waar procentsgewijs in  het document de cursor zich bevindt, de afstand vanaf  de rand van de pagina of de exacte schermpositie. Ttweemaal drukken geeft mogelijk meer details.|
|Volgende zin |alt+Pijl omlaag |alt+Pijl omlaag |Verplaatst cursor naar volgende zin en meldt deze (alleen ondersteund in Microsoft Word en Outlook).|
|Vorige zin |alt+Pijl omhoog |Alt+Pijl omhoog |Verplaatst cursor naar vorige zin en meldt deze (alleen ondersteund in Microsoft Word en Outlook ).|

Binnen een tabel kunt u ook de volgende toetscommando’s gebruiken:

| Naam |Toets |Beschrijving|
|---|---|---|
|Ga naar vorige kolom |control+alt+pijl links |Verplaatst systeemcursor naar vorige kolom(van dezelfde rij)|
|Ga naar volgende kolom |control+alt+pijl rechts |Verplaatst systeemcursor naar volgende kolom(van dezelfde rij)|
|Ga een rij naar boven |control+alt+pijl omhoog |Verplaatst de systeemcursor een rij omhoog(van dezelfde kolom)|
|Ga een rij omlaag |control+alt+pijl omlaag |Verplaatst de systeemcursor een rij omlaag(van dezelfde kolom)|
|Ga naar eerste kolom |control+alt+home |Verplaatst systeemcursor naar de eerste kolom (van dezelfde rij )|
|Ga naar laatste kolom |control+alt+end |Verplaatst de systeemcursor naar de laatste kolom (van dezelfde rij)|
|Ga naar eerste rij |control+alt+pageUp |Verplaatst de systeemcursor naar de eerste rij (van dezelfde kolom)|
|Ga naar laatste rij |control+alt+pageDown |Verplaatst de systeemcursor naar de laatste rij (van dezelfde kolom)|
|Alles lezen in kolom |`NVDA+control+alt+pijlOmlaag` |Kolom wordt vertikaal vanaf de huidige cel neerwaarts tot de laatste cel in de kolom gelezen.|
|Alles in rij lezen |`NVDA+control+alt+pijlRechts` |De rij wordt horizontaal vanaf de huidige cel naar rechts tot de laatste cel in de rij gelezen.|
|Hele kolom  lezen |`NVDA+control+alt+pijlOmhoog` |De huidige kolom wordt in zijn geheel van boven naar beneden gelezen zonder dat de systeemcursor wordt verplaatst.|
|Hele rij  lezen |`NVDA+control+alt+pijlLinks` |Huidige rij wordt horizontaal van links naar rechts gelezen zonder dat de systeemcursor wordt verplaatst.|

<!-- KC:endInclude -->

### Objectnavigatie {#ObjectNavigation}

U zult meestal met applicaties werken door middel van de commando's voor het verplaatsen van de [focus](#SystemFocus) en de [systeemcursor](#SystemCaret).
Soms kan het echter handig zijn om de huidige applicatie of het besturingssysteem te verkennen zonder de [focus](#SystemFocus) of de [systeemcursor](#SystemCaret) te verplaatsen.
Ook wilt u soms werken met [objecten](#Objects) die niet te bedienen zijn met de TAB-toets van het toetsenbord.
In deze gevallen kan objectnavigatie handig zijn.

Objectnavigatie stelt u in staat om te navigeren naar afzonderlijke objecten en informatie over deze objecten op te vragen.
NVDA meldt informatie over een object waar u met objectnavigatie naar toe gaat op een soortgelijke manier als informatie over de systeemfocus.
Om alle tekst zoals deze op het scherm verschijnt te lezen kunt u, in plaats van object navigatie, [Screen review (schermoverzicht)](#FlatReview) gebruiken.

De objecten van het besturingssysteem en van de programma's zijn hiërarchisch gegroepeerd (Vergelijk de boomstructuur van Windows Verkenner met mappen en submappen die op hun beurt weer submappen kunnen bevatten).
Dit betekent dat u naar een bepaald object navigeert om na te gaan welke objecten er eventueel in zijn opgenomen.
Een lijst bevat bijvoorbeeld lijst items, u dient dus de lijst binnen te gaan om de onderliggende items in de lijst te lezen.
Zodra u zich op een lijst item bevind, kunt u terug en vooruit navigeren om van item naar item te gaan in de lijst.
Als u zich op een lijstitem bevind, kunt u terug naar het bovenliggend object om weer op het lijstobject terecht te komen.
Nu kunt u verder gaan naar een ander object (op hetzelfde niveau).
Iets dergelijks geldt voor bv. een werkbalk. U gaat de werkbalk in, (navigeert naar het eerste subniveau (first child) om toegang te krijgen tot de bijbehorende besturingselementen.

Als u toch liever vooruit en terug gaat  naar elk afzonderlijk object in het systeem, kunt u via commando's navigeren naar vorig/volgend  object door gebruik te maken van een plattere weergavehirargie.
Als u bijvoorbeeld naar het volgende  object in deze afgeplatte weergave navigeert en als dan het huidige  object andere objecten bevat zal NVDA automatisch naar het eerste object daarbinnen gaan.
In het geval dat het huidige object geen objecten bevat, zal NVDA naar het volgende object gaan van het huidige hirarchische niveau.
Als er een dergelijk volgend object niet is, zal NVDA het volgende  object in de hierarchie op basis van ingesloten objecten proberen te vinden tot er geen in aanmerking komende objecten meer zijn.
Dezelfde regels gelden als binnen de hierarchie in omgekeerde richting (achterwaarts) wordt genavigeerd.

Het object dat op een gegeven moment bekeken wordt in objectnavigatie wordt het navigator object genoemd.
Wanneer u naar een object navigeert, kuntu de inhoud ervan bekijken met de [commando's voorhet Nalezen van Tekst](#ReviewingText) terwijl u zich in de [objectoverzichtmodus](#ObjectReview) bevindt.
Wanneer  [Visuele Uitlichting](#VisionFocusHighlight) geactiveerd is, wordt de plaats waar het huidige navigator Object zich bevindt ook zichtbaar weergegeven.
Standaard wordt in NVDA de object navigator tegelijk met de systeemfocus verplaatst, maar deze koppeling kan aan- en uitgezet worden.

Merk op dat u Braille objectnavigatie kunt laten volgen met behulp van [Braille Koppelen](#BrailleTether).

Voor objectnavigatie zijn de volgende toetscombinaties beschikbaar:

<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Aanraken |Beschrijving|
|---|---|---|---|---|
|Informatie over huidig object |NVDA+numeriek5 |NVDA+shift+o |geen |Geeft informatie over huidig navigator object. Bij tweemaal drukken wordt informatie gespeld, driemaal drukken kopieert naam en waarde ervan naar het klembord.|
|Naar hoger niveau navigeren |NVDA+numeriek8 |NVDA+shift+Pijl Omhoog |Veeg omhoog (objectmodus) |Hiermee gaat u naar een hoger niveau (de map) waartoe het huidige navigator object behoort|
|Naar vorig object gaan |NVDA+numeriek4 |NVDA+shift+Pijl links |geen |Hiermee navigeert u naar het object dat direct voorafgaat aan het huidige navigator object||
|Naar vorig object gaan in platte weergave |NVDA+numeriek9 |NVDA+shift+[ |veegbeweging naar links (objectmodus) |hiermee gaat u naar het vorige object  in een platte  weergave van  the objectnavigatie-hierarchie|
|Naar het volgende object gaan |NVDA+numeriek6 |NVDA+shift+Pijl rechts |geen |Hiermee navigeert u naar het object dat volgt op het huidige navigator object|
|Naar het volgende object gaan in platte weergave |NVDA+numeriek3 |NVDA+shift+] |veegbeweging naar rechts (objectmodus) |hiermee gaat u naar het volgende object  in een platte  weergave van  the objectnavigatie-hierarchie|
|Naar het eerstvolgende ingesloten object (een lager niveau) gaan |NVDA+numeriek2 |NVDA+shift+Pijl omlaag |Veeg omlaag (objectmodus) |Hiermee navigeert u vanuit het huidige navigator object (hoofdmap) naar het niveau eronder waar u bij de bijbehorende objecten komt|
|Naar object met de focus gaan |NVDA+numeriek minteken |NVDA+backspace |geen |Hiermee navigeert u naar het object waar de systeemfocus zich momenteel bevindt, en verplaatst u de leescursor (review cursor) naar de positie van de tekstcursor als deze zichtbaar is|
|Huidige navigator object activeren |NVDA+numeriek entertoets |NVDA+enter |dubbel tikken |Hiermee wordt het huidige navigator object geactiveerd(hetzelfde effect als klikken met de muis of het indrukken van de spatiebalk bij gefocusseerd object)|
|Verplaats de systeem focus of cursor naar de huidige review positie |NVDA+shift+numeriek minteken |NVDA+shift+backspace |geen |Een maal drukken verplaatst de focus naar het huidige navigator object, twee maal drukken verplaatst de systeem cursor naar de review cursor|
|Positie van de leescursor melden |NVDA+shift+numeriek Delete |NVDA+shift+delete |geen |Geeft informatie overde plaats van de tekst of het object bij de leescursor. Er kan, bij voorbeeld, in een percentage aangegeven worden waar in het document de cursor staat, wat de afstand is ten opzichte van de rand van de pagina of de exacte schermpositie. Door tweemaal te drukken krijgt u meer details.|
|Leescursor (review cursor) naar statusbalk verplaatsen |geen |geen |geen |Melden van  Statusbalk als NVDA deze vindt. Het navigatorobject wordt eveneens hierheen verplaatst.|

<!-- KC:endInclude | -->

Let op: voor een goede werking van de numerieke toetsen moet NumLock uitgeschakeld worden.

### Nalezen van tekst {#ReviewingText}

Met NVDA kunt u de inhoud van het [scherm (schermoverzicht)](#ScreenReview), het huidige [document (documentoverzicht)](#DocumentReview) of het huidige [object](#ObjectReview) , per karakter, per woord of regel nalezen.
Dit is vooral handig in Windows-opdrachtvensters of andere plaatsen waar de [tekstcursor](#SystemCaret) niet of slechts beperkt beschikbaar is.
U kunt dit bijvoorbeeld gebruiken voor het lezen van een lang, informatief bericht in een dialoogvenster

Bij het verplaatsen van de leescursor (review cursor) volgt de tekstcursor niet maar deze blijft op de huidige invoegpositie staan, zodat u tekst kun bekijken zonder de systeemcursor te verplaatsen.
Standaard wordt de leescursor echter gelijktijdig verplaatst wanneer de tekstcursor verplaatst wordt. 
Deze koppeling kan in- en uitgeschakeld worden.

Merk op dat u Braille de leescursor  kunt laten volgen met behulp van [Braille Koppelen](#BrailleTether).

Voor het nalezen van tekst kunt u de volgende toetscombinaties gebruiken:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Aanraken |Beschrijving|
|---|---|---|---|---|
|in de leesmodus naar de eerste regel gaan |shift+numeriek7 |NVDA+control+Home |geen |De leescursor wordt naar de eerste regel van de tekst verplaatst|
|In de leesmodus naar de vorige regel gaan |numeriek7 |NVDA+Pijl omhoog |Veeg omhoog (tekstmodus) |De leescursor wordt naar de vorige regel van de tekst verplaatst|
|Huidige regel van leescursor weergeven |numeriek8 |NVDA+shift+punt-teken |geen |Zegt in welke regel van de tekst de leescursor zich bevindt. Bij tweemaal drukken wordt de regel gespeld. Bij drie maal drukken wordt de regel gespeld met symboolomschrijvingen.|
|In de leesmodus naar de volgende regel gaan |numeriek9 |NVDA+Pijl omlaag, |Veeg omlaag (tekstmodus) |De leescursor wordt naar de volgende tekstregel verplaatst|
|In de leesmodus naar de laatste regel gaan |shift+numeriek9 |NVDA+control+End, |geen |De leescursor wordt naar de laatste tekstregel verplaatst|
|In de leesmodus naar het vorige woord gaan |numeriek4 |NVDA+control+pijl links |Veeg links met 2 vingers (tekstmodus) |De leescursor wordt naar het vorige woord in de tekst verplaatst|
|Het woord waar de leescursor zich bevindt weergeven |numeriek5 |NVDA+control+punt-teken |geen |Vertelt op welk woord in de tekst de leescursor nu staat. Bij tweemaal drukken wordt het woord gespeld. Bij drie maal drukken wordt het woord gespeld met symboolomschrijvingen.|
|In de leesmodus naar het volgende woord gaan |numeriek6 |NVDA+control+pijl rechts |Veeg rechts met 2 vingers (tekstmodus) |De leescursor wordt naar het volgende woord in de tekst verplaatst|
|In de leesmodus naar begin van een regel gaan |shift+numeriek1 |NVDA+home |geen |De leescursor wordt naar het begin van de huidige regel verplaatst|
|Ga in de leesmodus naar vorig karakter |numeriek1 |NVDA+pijl links |Veeg links (tekstmodus) |De leescursor wordt naar het vorige karakter in de huidige tekstregel verplaatst|
|Huidige karakter onder de leescursor weergeven |numeriek2 |NVDA+punt |geen |Noemt het huidige karakter in de tekstregel waar de leescursor zich bevindt. Tweemaal drukken geeft een omschrijving of voorbeeld van het karakter. Drie maal drukken geeft de numerieke waarde in decimalen en hexadecimalen.|
|In de leesmodus naar het volgende karakter gaan |numeriek3 |NVDA+pijl rechts |Veeg rechts (tekstmodus) |De leescursor wordt naar het volgende karakter verplaatst in de huidige tekstregel||
|In de leesmodus naar het einde van de regel gaan |shift+numeriek3 |NVDA+End |geen |De leescursor wordt naar het einde van de huidige tekstregel verplaatst|
|In de leesmodus naar vorige pagina gaan |`NVDA+pageUp` |`NVDA+shift+pageUp` |geen |Verplaatst leescursor naar vorige pagina met tekst als de toepassing dit ondersteunt|
|In de leesmodus naar volgende pagina gaan |`NVDA+pageDown` |`NVDA+shift+pageDown` |geen |Verplaatst leescursor naar volgende pagina met tekst als de toepassing dit ondersteunt|
|Alles voorlezen in leesmodus |numeriek Plus |NVDA+shift+a |Veeg omlaag met 3 vingers (tekstmodus) |Leest vanaf de huidige positie van de leescursor waarbij de leescursor zich mee beweegt.|
|Selecteer, kopieer dan vanaf leescursor |NVDA+f9 |NVDA+f9 |geen |Start het selectie- en daaropvolgend kopieerproces vanaf de huidige positie van de leescursor. De feitelijke actie wordt pas uitgevoerd zodra aan NVDA wordt doorgegeven waar het tekstgebied eindigt.|
|Selecteer, kopieer dan tot leescursor |NVDA+f10 |NVDA+f10 |geen |Bij de eerste maal drukken wordt tekst geselecteerd vanaf het eerder ingestelde beginpunt tot einde inclusief de huidige positie van de leescursor. Als de systeemcursor bij de tekst kan komen, zal die naar de geselecteerde tekst worden verplaatst. Nadat de toetscombinatie de 2de keer wordt ingedrukt wordt de tekst naar het klembord gekopieerd.|

|Verplaats naar ingesteld beginpunt voor kopie in leesmodus | NVDA+shift+f9 | NVDA+shift+f9 | geen | Verplaatst  leescursor naar het eerder ingestelde beginpunt voor kopie |

|Tekstopmaak melden |NVDA+shift+f |NVDA+shift+f |geen |NVDA laat horen hoe de tekst waarin de leescursor zich bevindt, is opgemaakt. Bij tweemaal drukken krijgt u de informatie in bladermodus.|
|Actuele symboolvervanging melden| geen |geen |geen |Het symbool waarbij de leescursor zich bevindt wordt uitgesproken. Bij tweemaal drukken wordt het symbool en de voor het benoemen hiervan gebruikte tekst weergegeven in bladermodus.|

<!-- KC:endInclude -->

Let op: voor een goede werking van de numerieke toetsen moet NumLock worden uitgeschakeld.

Om de basiscommando’s voor het navigeren met de leescursor beter te kunnen onthouden zou u zich een tabel kunnen voorstellen met drie kolommen en drie rijen. Van boven naar beneden: regel, woord en karakter, en van links naar rechts; vorig, huidig en volgend. 
Dit ziet er dan als volgt uit:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Vorige regel |Huidige regel |Volgende regel|
|Vorig woord |Huidig woord |Volgend woord|
|Vorig karakter |Huidige karakter |Volgende karakter|

### Leesoverzichtmodi (Review Modes) {#ReviewModes}

Met behulp van de [leesoverzichtcommando's](#ReviewingText) van NVDA kan, afhankelijk van de geselecteerde leesoverzichtmodus, de inhoud van het huidige navigatorobject, het huidige document, of scherm worden nagelezen.

U kunt de volgende commando’s gebruiken om van leesoverzichtmodus te wisselen:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Aanraakgebaar |Beschrijving|
|---|---|---|---|---|
|Naar volgende leesoverzichtmodus schakelen |NVDA+numeriek7 |NVDA+pageUp |met 2 vingers omhoog vegen |hiermee wordt naar de volgende, beschikbare modus geschakeld.|
|Naar vorige leesoverzichtmodus schakelen |NVDA+numeriek1 |NVDA+pageDown |met 2 vingers omlaag vegen |hiermee wordt naar de vorige, beschikbare modus geschakeld.|

<!-- KC:endInclude -->

#### Objectoverzicht (Object Review) {#ObjectReview}

In de objectoverzichtmodus kan alleen de inhoud van het huidige [navigatorobject](#ObjectNavigation) worden bekeken.
Voor objecten zoals bewerkbare invoervelden of andere eenvoudige bewerkingen gaat het daarbij in het algemeen om tekst.
Bij andere objecten kan het gaan om de naam en of de waarde van het object.

#### Documentoverzicht (Document Review) {#DocumentReview}

Wanneer het [navigatorobject](#ObjectNavigation) zich binnen een bladermodusdocument bevindt (een webpagina bij voorbeeld) of een ander complex documentdat veel objecten bevat (bij voorbeeldeen Lotus Symphony document), kan naar de documentoverzichtmodus worden overgeschakeld.
In de documentoverzichtmodus kan de tekst van het gehele document worden bekeken.

Wanneer wordt overgeschakeld van de objectoverzicht- naar de documentoverzichtmodus, komt de leescursor in het document op de plaats van het navigatorobject te staan.
Wanneer het document met de daarvoor bestemde leesoverzichtcommando's wordt verkend, wordt de plaats van het navigatorobject automatisch geactualiseerd zodat deze overeenkomt met de plaats van het object waar de leescursor bij staat. 

Merk op dat NVDA automatisch vanuit objectoverzicht overschakelt naar documentoverzicht wanneer bladermodusdocumenten worden verkend.

#### Schermoverzicht (Screen Review) {#ScreenReview}

In de schermoverzichtmodus kunt u tekst in de actieve toepassing verkennen die op het scherm te zien is.
Dit komt overeen met schermoverzichtopties of de muiscursorfuncties zoals die in veel andere schermleesprogramma's worden geboden.

Wanneer naar de schermoverzichtmodus wordt overgeschakeld, gaat de leescursor naar de plaats op het scherm waar het huidige [navigatorobject](#ObjectNavigation) zich bevindt.
Wanneer het scherm met de daarvoor bestemde leesoverzichtcommando's wordt verkend, wordt de plaats van het navigatorobject automatisch geactualiseerd en komt dan bij het object op het scherm waar de leescursor zich bevindt.

Merk op dat NVDA bij sommige recente toepassingen tekst die op het scherm verschijnt slechts gedeeltelijk of soms helemaal niet leest. Dit heeft te maken met nieuwe schermtechnologie die op dit moment nog niet ondersteund kan worden.

### Navigeren met de muis {#NavigatingWithTheMouse}

Door de muis over het scherm te verplaatsen wordt tekst die zich direct onder de muisaanwijzer bevindt standaard door NVDA voorgelezen.
Voor zover ondersteund, wordt een hele alinea tekst voorgelezen, maar bij bepaalde besturingselementen leest NVDA de tekst per regel voor.

U kunt NVDA zo instellen dat het programma ook meldt welk type besturingselement of object zich onder de muisaanwijzer bevindt, zoals een lijst, een knop, etc.
Dit kan voor mensen die helemaal blind zijn erg handig zijn, omdat soms alleen tekst niet voldoende is.

Om een idee te krijgen waar de muis zich op het scherm bevindt kunnen pieptonen worden gebruikt die de muispositie hoorbaar maken.
Hoe verder de muis naar de bovenkant van het scherm wordt bewogen, hoe hoger de pieptoon wordt.
Hoe verder de muis naar links wordt bewogen, hoe meer het geluid uit de linker luidspreker lijkt te komen, terwijl het geluid steeds meer van rechts komt als de muis naar rechts wordt bewogen. Hierbij wordt ervan uitgegaan dat de gebruiker over stereoluidsprekers of een stereohoofdtelefoon beschikt.

Deze extra muisopties staan standaard “uit”.
Als u deze functionaliteit wilt gebruiken, kunt u deze inschakelen in de categorie [muisinstellingen](#MouseSettings) van het dialoogvenster [Instellingen van NVDA](#NVDASettings), dat bereikbaar is via Opties in het NVDA-menu. 

Hoewel u voor het navigeren met de muis een fysieke muis of een muispad moet gebruiken, zijn er een aantal toetscombinaties in NVDA waarmee muisbewegingen en muiskliks kunnen worden gesimuleerd:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Aanraakgebaar |Beschrijving|
|---|---|---|---|---|
|Klikken met linker muisknop |numeriek Gedeeld Door |NVDA+[ |geen |Dit is hetzelfde als éénmaal klikken met linker muisknop. Deze toets tweemaal snel drukken is gelijk aan dubbelklikken met de muis.|
|Linker muisknop vergrendelen |shift+numeriek Gedeeld Door |NVDA+control+[ |geen |Hiermee houdt u de linker muisknop ingedrukt. Door nogmaals te drukken wordt de knop weer los gelaten. Om te kunnen slepen met de muis drukt u deze toetscombinatie zodat de linker muisknop ingedrukt blijft. Vervolgens kunt u de muis fysiek verplaatsen of met een van de andere daarvoor bestemde commando’s.|
|Klikken met rechter muisknop |numeriek Vermenigvuldig |NVDA+] |tik en hou vinger op scherm |Dit is gelijk aan eenmaal klikken met rechter muisknop, meestal gebruikt voor openen van contextmenu bij muispositie.|
|Rechter muisknop vergrendelen |shift+numeriek Vermenigvuldig |NVDA+control+] |geen |Hiermee wordt rechter muisknop ingedrukt gehouden. Door nogmaals te drukken wordt de vergrendeling opgeheven. Om te kunnen slepen met de muis drukt u deze toetscombinatie zodat de rechter muisknop ingedrukt blijft. Vervolgens kunt u de muis fysiek verplaatsen of met een van de andere daarvoor bestemde commando’s.|
|Muis naar huidige navigator object verplaatsen |NVDA+numeriek Gedeeld Door |NVDA+shift+m |geen |Muis wordt verplaatst naar huidig object en de leescursor|
|naar het object onder de muisaanwijzer gaan |NVDA+numeriek Vermenigvuldig |NVDA+shift+n |geen |Verplaats het navigator object naar het object van de muispositie|

<!-- KC:endInclude -->

## Bladermodus {#BrowseMode}

In NVDA worden complexe alleen-lezen documenten zoals een webpagina weergegeven in bladermodus.
Het gaat om documenten van de volgende toepassingen:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML-meldingen in Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* ondersteunde boeken in Amazon Kindle voor PC

Bladermodus is ook optioneel beschikbaar voor Microsoft Word-documenten.

In bladermodus wordt de inhoud van het document weergegeven als platte tekst waar u met de pijltoetsen doorheen kunt lopen alsof het een tekstdocument is.
Alle NVDA commando's voor de [systeemcursor](#SystemCaret) werken in bladermodus. Denk hierbij aan opmaakinformatie, alles lezen, tabelnavigatie etc.
Wanneer  [Visuele Uitlichting](#VisionFocusHighlight) geactiveerd is, wordt de plaats waar de huidige virtuele bladermodus-aanwijzer zich bevindt ook zichtbaar weergegeven.
Informatie over de tekst, of het bijvoorbeeld een link of kop betreft, wordt gemeld als u door de tekst navigeert.

Soms is directe interactie nodig met onderdelen van een document in bladermodus.
Dit geldt bijvoorbeeld voor het typen van tekst in tekstvakken of het gebruik van de pijltoetsen om een item in een lijst te selecteren.
Dit doet u door naar focusmodus te wisselen, hierdoor worden vrijwel alle toetsen doorgegeven aan het onderliggende besturingselement.
Standaard zal NVDA naar focusmodus wisselen als door middel van de tab-toets een besturingselement de focus krijgt, of als er geklikt wordt op een besturingselement dat focusmodus vereist.
Bij het klikken op, of focussen van een besturingselement dat geen focusmodus vereist zal NVDA automatisch terugschakelen naar de bladermodus.
U kunt ook op spatie of enter drukken om focusmodus in te schakelen zodra u zich op een besturingselement bevind dat focusmodus vereist.
Het drukken van escape brengt u terug naar de bladermodus.
Het is ook mogelijk om handmatig de focusmodus in te schakelen, deze zal dan actief blijven tot u deze weer handmatig uitschakelt.

<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Van modus wisselen |NVDA+spatiebalk |Wisselen tussen blader en focusmodus|
|Focusmodus verlaten |escape |Naar de bladermodus teruggaan vanuit de automatisch ingeschakelde focusmodus|
|Document vernieuwen |NVDA+f5 |Het document wordt opnieuw geladen (nuttig als er iets lijkt te ontbreken op de pagina. Niet beschikbaar in Microsoft Word en Outlook.)|
|Zoeken |NVDA+control+f |Er wordt een venster geopend waarin u tekst kunt typen die in het huidige document moet worden opgezocht. Zie voor meer informatie, [zoeken naar tekst](#SearchingForText).|
|Volgende zoeken |NVDA+f3 |Hiermee kunt u nagaan of tekst van een zoekopdracht verderop in het document nog vaker voorkomt.|
|Vorige zoeken |NVDA+shift+f3 |Hiermee kunt u nagaan of de gezochte tekst eerder in het document voorkomt|

<!-- KC:endInclude -->

### Lettertoetsnavigatie {#SingleLetterNavigation}

Om in de bladermodus snel te kunnen navigeren, kunt u een lettertoets gebruiken om naar bepaalde velden te springen in een document.
Merk op dat niet alle commando’s worden ondersteund in elk type document.

<!-- KC:beginInclude -->
Om naar het eerstvolgende element te springen gebruikt u uitsluitend één van de hierna vermelde toetsen, terwijl u in combinatie met de shifttoets naar een vorig element springt:

* h: heading (kop)
* l: lijst
* i: lijstonderdeel
* t: tabel
* k: link
* n: niet-gelinkte tekst
* f: formulierveld
* u: unvisited (niet-bezochte) link
* v: visited (bezochte) link
* e: edit field (tekstvak)
* b: button (knop)
* x: checkbox (selectievakje)
* c: combo box (vervolgkeuzelijst)
* r: radio button (keuzerondje)
* q: block quote (citaatblok)
* s: separator (scheiding)
* m: frame (kader)
* g: graphic (afbeelding)
* d: ARIA oriëntatiepunt in een Internetomgeving
* o: embedded object (ingebed object), (audio- en videospeler, toepassing, dialoogvenster, etc.)
* 1 tot en met 6: respectievelijk, kop op niveau 1, 2, 3, 4, 5 en 6.
* a: annotatie (invoeroptie voor notities, opmerkingen e.d.).
* `p`: paragraph (tekstalinea) 
* w: spelfout

Gebruik de volgende toetscombinaties om naar het begin resp. het einde van containerobjecten (lijsten tabellen e.d.) te springen:

| Naam |Toetscombinatie |Beschrijving|
|---|---|---|
|naar begin van containerobject springen |Shift+komma |Verplaatst de systeemcursor naar begin van het containerobject (lijst, tabel etc.)|
|achter het containerobject springen |komma |Verplaatst de systeemcursor achter het containerobject (lijst, tabel etc.) waar de cursor zich bevindt.|

<!-- KC:endInclude -->

Enkele Webapplicaties zoals Gmail, Twitter en Facebook gebruiken  lettertoetsen als sneltoetsen.
Als u hiermee wilt werken terwijl u ook uw cursortoetsen wilt kunnen gebruiken voor het lezen in bladermodus, kunt u de lettertoetsnavigatie in NVDA tijdelijk uitschakelen.
<!-- KC:beginInclude -->
Om de lettertoetsnavigatie voor het huidige document in of uit te schakelen drukt u op NVDA+shift+spatiebalk.
<!-- KC:endInclude -->

#### Opdracht voor het navigeren in tekst-alinea's {#TextNavigationCommand}

Met `p` of `shift+p` spring je naar de volgende of vorige tekst-alinea.
Tekst-alinea's zijn per definitie tekstgedeeltes die bestaan uit een aantal volzinnen.
Dit kan het gemakkelijker maken het begin van leesbare inhoud  op allerlei wbpagina's te vinden, zoals:

* Nieuws-websites
* Forums
* Blog posts

Deze commando's kunnen ook goed van pas komen als je ongewenste pagina-vulling wilt mijden, denk hierbij aan:

* Ads
* Menus
* Headers

Merk evenwel op dat, hoe zeer NVDA ook z'n best doet tekst-alinea's te identificeren, , het  gebruikte algoritme niet perfect is en dat NVDA zo nu end dan  ook fouten kam maken.
Bedenk ook dat dit commando niet hetzelfde is  als de commando's voor alinea-navigatie (paragraph navigation) `control+downArrow/upArrow`.
Tekst-alineanavigatie brengt je uitsluitend van de ene naar de andere tekstalinea, terwijl alinea-navigatiecommandos' de cursor naar de vorige/volgende alinea verplaatsen ongeacht of die al dan niet uit tekst bestaat.

#### Andere navigatiecommando's {#OtherNavigationCommands}

Naast de hierboven vermelde toetscombinaties voor snelle navigatie heeft NVDA commando's waaraan geen standaarrdtoetsen zijn toegewezen.
Om deze commando's, te gebruiken dient u hieraan eerst invoerhandelingen toe te kennen met behulp van het [dialoogvenster Invoerhandelingen](#InputGestures).
Hier is een lijst met  beschikbare commando's:

* Artikel
* Figuur
* Groepering
* Tab
* Menu-onderdeel
-- Omschakelknop
* Voortgangsbalk
* Math-formule (wisk.)
* Verticaaluitgelijnde alinea
* Same style tekst
* Different style tekst

Bedenk dat er twee commando's (nodig) zijn voor elk elementtype; om verder te gaan in het document en om terug te gaan in het document. Daarom moet u aan het ene alsmede aan het andere een commando toekennen zodat u snel in beide richtingen kunt navigeren.
Als u bijvoorbeeld de `y` / `shift+y` toetsen wilt gebruiken om snel door tabs te navigeren, zou u als volgt te werk gaan:

1. Open het dialoogvenster invoerhandelingen  vanuit bladermodus.
1. Zoek  het item "naar volgende tab gaan" in de  sectie Bladermodus.
1. Wijs de toets `y` toe voor de gevonden handeling.
1. Zoek  het item "naar vorige tab gaan".
1. Wijs `shift+y` toe voor de gevonden handeling.

### De lijst met elementen {#ElementsList}

Via de lijst met elementen krijgt u toegang tot de verschillende, bij de toepassing behorende, elementtypes in het document.
Als u zich bij voorbeeld in een webbrowser bevindt, kan de lijst met elementen koppen, koppelingen (links), formuliervelden, knoppen of oriëntatiepunten bevatten. 
Met behulp van keuzerondjes kunt u wisselen tussen de verschillende elementtypes.
In het dialoogvenster treft u ook een invoerveld aan waarmee u de lijst kunt filteren zodat u gerichter naar iets kunt zoeken op de pagina.
Als u uw keuze eenmaal gemaakt hebt, kunt u met de aanwezige knoppen in het dialoogvenster naar dat onderdeel springen of het activeren.
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Lijst met elementen |NVDA+f7 |Hiermee roept u de lijst met de verschillende elementtypes op die zich in het huidige document bevinden.|

<!-- KC:endInclude -->

### Naar tekst zoeken {#SearchingForText}

Door middel van dit dialoogvenster  kunt u naar termen zoeken in het huidige document.
In het vak  "Typ de tekst waarnaar u wilt zoeken', kunt u de desbetreffende tekst invoeren.
Door het selectievakje voor hoofdlettergevoeligheid in te schakelen zorgt u ervoor dat er onderscheid wordt gemaakt tussen hoofdletters en kleine letters bij het zoeken.
Als dit selectievakje is ingeschakeld, zult u bijv. wel "NV Access" vinden maar vindt u "nv access" niet.
Gebruik de volgende toetsen  voor zoekopdrachten:
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|tekst zoeken |NVDA+control+f |Zoekvenster wordt geopend|
|Volgende zoeken |NVDA+f3 |Hiermee gaat u naar de volgende vindplaats van de huidige zoekterm.|
|Vorige zoeken |NVDA+shift+f3 |Hiermee gaat u naar de vorige vindplaats van de huidige zoekterm.|

<!-- KC:endInclude -->

### Ingebedde objecten {#ImbeddedObjects}

De inhoud van pagina’s kan verrijkt zijn met programmatuur zoals Oracle Java en HTML5, maar ook met applicaties en dialoogvensters.
Wanneer u iets dergelijks tegenkomt in bladermodus zal NVDA dit respectievelijk melden als “Ingebed (Embedded) Object”, “applicatie”, of “dialoogvenster.
Met de letternavigatietoetsen o en Shift + o kunt u hier snel naar toe navigeren.
Door op Enter te drukken wordt interactie met zulke objecten mogelijk.
Als het object toegankelijk is, kunt u het met de TAB-toets verkennen en bewerkingen uitvoeren zoals u dat ook in andere toepassingen gewend bent.
Er is een toetscombinatie beschikbaar om weer terug te gaan naar de oorspronkelijke pagina waarop zich het object bevindt. 
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Terug naar inhoud van document |NVDA+control+spatiebalk |Verplaatst de focus van het huidige ingevoegde object naar “het document waarin het zich bevindt|

<!-- KC:endInclude -->

### NVDA-intrinsieke  SelectieModus {#NativeSelectionMode}

Bij het selecteren van tekst met  de `shift+pijltoetsen` in Bladermodus is de selectie standaard alleen van toepassing op de weergave van het document  in de bladermodus van NVDA, en niet op de  applicatie zelf.
Dit houdt in dat  de selectie niet zichtbaar is  op het scherm, en het kopiërenvan de tekst met `control+c` slechts NVDA's platte tekstweergave van de inhoud kopieert. Dat wil dus zeggen  dat geen tabelopmaak of dat iets een link is, zal worden gekopieerd.
NVDA heeft evenwel een Intrinsieke  Selectiemodus die voor bepaalde documenten in Bladermodus (tot dusver alleen  Mozilla Firefox) kan worden ingeschakeld  die er voor zorgt dat de intrinsieke selectie van het document   de bladermodusselectie van NVDA volgt.

<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Intrinsieke Selectiemodus in-  en uitschakelen |`NVDA+shift+f10` |Zet de intrinsieke selectiemodus aan en uit|

<!-- KC:endInclude -->

Wanneer de Intrinsieke Selectiemodus ingeschakeld wordt, zal bij het kopiëren van de selectie met  `control+c` hierbij ook de eigen kopieerfunctionaliteit van de applicatie worden ingezet, wat betekent dat ook verrijkte inhoud naar het klembord wordt gekopieerd, in plaats van louter platte tekst.
Met andere woorden, als je de inhoud in een programma zoals  Microsoft Word of Excel plakt, blijft opmaak van bijv. tabellen, of een link behouden.
Merk echter op dat in de intrinsieke selectiemodus sommige toegankelijke labels of andere informatie die NVDA genereert in de Bladermodus niet wordt meegenomen.
En hoewel de toepassing zo goed mogelijk probeert de intrinsieke selectie te laten overeenkomen met de bladermodusselectie van NVDA, kunnen onvolkomenheden soms voorkomen.
Echter, in scenario's waarbij  je een hele tabel of alinea  verrijkte content wilt kopiëren, kan deze optie heel handig blijken te zijn.

## Inhoud van wiskundige aard lezen {#ReadingMath}

Met NVDA kun je inhoud van wiskundige aard op het web en in andere toepassingen lezen en er in navigeren, waarbij zowel spraak als braille gebruikt kunnen worden.
Om NVDA in staat te stellen, wiskundige inhoud te lezen en er interactief mee om te gaan moet je evenwel eerst   een Math component voor NvDA installeren.
Er zijn verscheidene NVDA add-ons te krijgen in de NVDA Add-on Store die ondersteuning bieden voor math (wiskunde), waaronder de NVDA add-on [MathCAT](https://nsoiffer.github.io/MathCAT/) and [Access8Math](https://github.com/tsengwoody/Access8Math).
Ga naar de  [Add-on Store en lees onder](#AddonsManager)hoe je door de beschikbare add-ons bladert en deze installeert in NVDA.
In NVDA kan ook de oudere [MathPlayer](https://info.wiris.com/mathplayer-info) gebruikt worden; (software van Wiris) als deze op je systeem staat, hoewel deze software niet langer onderhouden wordt.

### Ondersteunde wiskundige inhoud {#SupportedMathContent}

Vooropgesteld dat er een geschikte math component is geïnstalleerd, biedt NVDA ondersteuning  voor de  volgende types wiskundige inhoud:

* MathML in Mozilla Firefox, Microsoft Internet Explorer en Google Chrome.
* Microsoft Word 365 Modern Math Equations via UI automation:
NVDA kan wiskundige vergelijkingen in Microsoft Word 365/2016 build 14326 en hoger lezen  en er interactief mee omgaan.
Merk evenwel op dat eerder gemaakte MathType-vergelijkingen eerst omgezet moeten worden naar Office Math.
Dit kunt u doendoor elk van de vergelijkingen te selecteren om vervolgens in het contextmenu van de opties voor vergelijkingen te kiezen  en dan 'Omzetten naar Office Math'.
Vergewis u ervan dat u over de nieuwste versie van MathType beschikt voordat u dit doet.
Microsoft Word biedt nu ook de mogelijkheid van lineaire symbool-gebaseerde navigatie door de  vergelijkingen zelf, en ondersteunt wiskundige invoer waarbij gebruik wordt gemaakt van syntaxis van uiteenlopende aard, waaronder LateX.
Verdere details, vindt u onder [Linear format equations using UnicodeMath and LaTeX in Word](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint, en oudere versies van Microsoft Word:
In zowel Microsoft Powerpoint als in  Microsoft Word kunt u met NVDA MathType-vergelijkingen lezen en er in navigeren.
MathType moet worden geïnstalleerd anders werkt dit niet.
De proefversie ishiervoor voldoende.
Je kunt deze  downloaden van the [MathType presentatiepagina](https://www.wiris.com/en/mathtype/).
* Adobe Reader.
NB. Dit is nog geen officiële standaard. Er is dan ook geen software publiek verkrijgbaar waarmee deze inhoud geproduceerd kan worden.
* Kindle Reader voor PC.
In boeken met toegankelijke wiskundige inhoud die u gebruikt via Kindle voor PC stelt NVDA u in staat de wiskundige inhoud te lezen en er in te navigeren.

Bij het lezen van een document zal NVDA alle ondersteunde wiskundige inhoud voorlezen wanneer deze voorkomt.
Als u een brailleleesregel gebruikt, wordt deze ook in braille weergegeven.

### Interactieve Navigatie {#InteractiveNavigation}

Als u voornamelijk met spraak werkt, zult u de probleemstelling waarschijnlijk meestal liever eerst in kleinere stukjes horen dan in zijn geheel.

Als u in de bladermodus bent, kunt u dit doen door de cursor naar de wiskundige inhoud te verplaatsen en dan op enter te drukken.

Als u zich niet in de bladermodus bevindt:

1. verplaatst u de leescursor naar de wiskundige inhoud.
Standaard volgt de leescursor de systeemcursor, dus kunt u deze gewoonlijk gebruiken om bij de gewenste inhoud te geraken.
1. Hierna activeert u het volgende commando:

<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Interactie met wiskundige inhoud |NVDA+alt+m |interactie met wiskundige inhoud starten.|

<!-- KC:endInclude -->

Nu schakelt NVDA naar de Math-modus, waarin  je commando’s zoals de pijltjestoetsen kunt gebruiken om de stelling te verkennen.
U kunt bij voorbeeld horizontaal door de stelling gaan met de linker en rechter pijltoets en inzoemen op een onderdeel van de stelling zoals een breuk met behulp van pijl omlaag.

Als u naar het document wilt teruggaan drukt u op Escape.

Raadpleeg voor meer informatie over beschikbare commando's en voorkeuren voor het lezen en navigeren in wiskundige inhoud, de documentatie van de specifieke math component die je hebt geïnstalleerd.

* [MathCAT documentatie](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math documentatie](https://github.com/tsengwoody/Access8Math)
* [MathPlayer documentatie](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Wiskundige inhoud kan soms worden weergegeven als een knop of een ander type besturingselement waarmee bij activering ervan , een dialoogvenster  of meer informatie kan worden getoond welke betrekking heeft op de formule.
Om  de knop of het besturingselement metdaarin  de formule te activeren, gebruikt u de toetscombinatie ctrl+enter.

### MathPlayer installeren {#InstallingMathPlayer}

Hoewel het in 't algemeen aan te bevelen is om een van de nieuwere NVDA add-ons te gebruiken om met wiskundige inhoud te werken  in NVDA, kan MathPlayer onder bepaalde omstandigheden een meer geschikte keus zijn.
MathPlayer kan bijv. ondersteuning voor een specifieke taal of Braill- code bieden waarvoor geen ondersteuning is in de nieuwere add-ons.
MathPlayer is gratis verkrijgbaar op de website van Wiris.
[Download MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Na installatie van  MathPlayer, moet NVDA opnieuw gestart worden.
Merk op dat in de informatie over  MathPlayer kan staan dat deze alleen bestemd is voor oudere browsers zoals Internet Explorer 8.
Hiermee wordt uitsluitend gedoeld op het gebruik van MathPlayer om wiskundige inhoud visueel weer te geven, en kan worden genegeerd door gebruikers  die met NVDA inhoud van wiskundige aard willen lezen of erin willen navigeren.

## Braille {#Braille}

Als u over een brailleleesregel beschikt, kan NVDA informatie in braille weergeven.
Als uw brailleleesregel een toetsenbord heeft van het type Perkins kunt u ook zowel verkort als onverkort braille invoeren.
Braille kan ook op het scherm worden weergegeven met behulp van de [Braille Viewer](#BrailleViewer) in plaats van, of tegelijk met een fysieke  brailleleesregel.

Raadpleegde paragraaf [Ondersteunde Brailleleesregels](#SupportedBrailleDisplays) voor informatie over de ondersteunde brailleleesregels.
In deze paragraaf vindt u ook informatie over die brailleleesregels die door NVDA automatisch als zodanig herkend worden.
U kunt braille configureren via de [categorie Braille](#BrailleSettings) in het dialoogvenster [Instellingen van NVDA](#NVDASettings).

### Braille-afkortingen voor besturingselementen, status-indicatoren en oriëntatiepunten {#BrailleAbbreviations}

Om zoveel mogelijk informatie op een brailleleesregel te krijgen zijn de volgende afkortingen samengesteld die verwijzen naar het type en de status van een besturingselement alsmede oriëntatiepunten.

| Afkorting |Type besturingselement|
|---|---|
|afb |afbeelding|
|app |applicatie / toepassing|
|art |artikel|
|bct |blokcitaat|
|bst |boomstructuur|
|bsitem |boomstructuuritem|
|bskn |boomstructuurknop|
|nv N |Items in de boomstructuur zijn hirarchisch ingedeeld, bijv. Niveau 1, 2, 3, enz|
|bijst |bijschrift (caption)|
|dlg |dialoogvenster|
|doc |document|
|fig |figuur|
|enoot |eindnoot|
|vnoot |voetnoot|
|grp |groepering|
|hlp |helpballon|
|ingebed |ingebed object|
|iv |invoerveld|
|wwiv |wachtwoord invoerveld|
|kn |knop|
|uschfknp |uitschuifknop|
|drkzkn |draaikeuzeknop|
|splkn |splitsknop|
|schkn |schakelknop|
|kN |kop op niveau (N), bijv. k1, k2.|
|kr |keuzerondje|
|lnk |link|
|blnk |bezochte link|
|lst |lijst|
|vkl |vervolgkeuzelijst|
|mnu |menu|
|mnubalk |menubalk|
|mnuitem |menuitem|
|mnukn |menuknop|
|ortp |oriëntatiepunt|
|pnl |paneel|
|bzgind |bezig-indicator|
|schfbalk |schuifbalk|
|sect |sectie|
|slv |selectievakje|
|stbalk |statusbalk|
|tabbld |tabblad|
|tbl |tabel|
|tltip |tooltip|
|kN |tabelkolomnnummer (N), bijv. k1, k2.|
|rN |tabelrijnummer (N), bijv. r1, r2.|
|term |terminal|
|vns |venster|
|vgsbalk |voortgangsbalk|
|wkbalk |werkbalk|
|⠤⠤⠤⠤⠤ |scheiding|
|mrkd |gemarkeerde inhoud|

Verder worden de volgende status-indicatoren gebruikt:

| Afkorting |status|
|---|---|
|... |wordt weergegeven wanneer object autoaanvulling ondersteunt|
|⢎⣿⡱ |wordt weergegeven wanneer een object (bijv. een schakelknop) ingedrukt is|
|⢎⣀⡱ |wordt weergegeven wanneer een object (bijv. een schakelknop) niet is ingedrukt|
|⣏⣿⣹ |wordt weergegeven wanneer een object (bijv. een selectievakje) aangevinkt is|
|⣏⣸⣹ |wordt weergegeven wanneer een object (bijv. een selectievakje) gedeeltelijk aangevinkt is|
|⣏⣀⣹ |wordt weergegeven wanneer een object (bijv. een selectievakje) niet aangevinkt is|
|- |wordt weergegeven wanneer een object zoals een boomstructuur kan worden samengevouwen|
|+ |wordt weergegeven wanneer een object zoals een boomstructuur kan worden uitgevouwen|
|*** |wordt weergegeven in geval van een beveiligd besturingselement of beveiligd document|
|klb |wordt weergegeven wanneer een objectklikbaar is|
|opm |wordt weergegeven wanneer er sprake is van opmerking bij een werkbladcel of een stukje tekst in een document|
|frml |wordt weergegeven in geval van een formule voor werkbladcel|
|ongeldig |wordt weergegeven in geval van ongeldige invoer|
|lbeschr |wordt weergegeven in geval van een object (meestal een grafiek) met lange beschrijving|
|mrg |wordt weergegeven wanneer meer regels kunnen worden ingevoerd in een tekstvak bijv. velden voor opmerkingen op websites|
|veist |wordt weergegeven in geval van een verplicht formulierveld|
|al |wordt weergegeven wanneer een object (bijv. een tekstinvoerveld ) het kenmerk "alleen lezen" heeft|
|sel |wordt weergegeven wanneer object geselecteerd is||
|nsel |wordt weergegeven wanneer object niet geselecteerd is|
|sort opl |wordt weergegeven wanneer object oplopend wordt gesorteerd|
|sort afl |wordt weergegeven wanneer object aflopend wordt gesorteerd|
|submnu |wordt weergegeven wanneer een object kan worden uitgeschoven, meestal in de vorm van een sub-menu|

Tot slot kunnen de volgende afkortingen gebruikt worden met betrekking tot oriëntatiepunten:

| Afkorting |Oriëntatiepunt|
|---|---|
|bnnr |banner|
|iinf |content info (inhoudsinfo)|
|aanv |aanvullend|
|form |formulier|
|hoofd |main (hoofdgebied)|
|navi |navigatie|
|zoek |zoeken ||
|gbd |gebied|

### Brailleinvoer {#BrailleInput}

NVDA ondersteunt de invoer van zowel onverkort als verkort braille via een brailletoetsenbord.
U kunt een omzettabel selecteren waarmee u braille in tekst kunt laten omzetten met behulp van de [Invoertabelopties](#BrailleSettingsInputTable) in de categorie Braille van het dialoogvenster [Instellingen van NVDA](#NVDASettings).

Bij gebruik van onverkort braille wordt tekst ingevoegd zodra deze wordt ingevoerd.
Bij gebruik van verkort braille wordt tekst ingevoegd wanneer u op de spatiebalk of de Enter-toets drukt aan het eind van een woord.
Merk op dat bij de omzetting alleen het woord dat u typt kan worden weergegeven en dat al bestaande tekst niet kan worden getoond.
Als u bijv. een braillecode gebruikt die getallen vooraf laat gaan door een nummerteken en u backspace indrukt om naar het einde van een getal te gaan, moet u het nummerteken opnieuw typen om weer getallen toe te voegen.

<!-- KC:beginInclude -->
Door punt 7 in te toetsen, verwijdert u de laatst ingevoerde braillecel of het laatste brailleteken.
Punt 8 zet alle braille-invoer om en activeert de Enter-toets.
Door punt 7 + punt 8 in te drukken wordt alle braille-invoer omgezet, maar zonder de spatiebalk of Enter-toets te activeren.
<!-- KC:endInclude -->

#### Sneltoetscombinaties instellen {#BrailleKeyboardShortcuts}

NVDA ondersteunt het instellen  van sneltoetsen en het emuleren van toetsenbordaanslagen met de brailleleesregel.
Dat emuleren kan op twee manieren: brailleinvoer rechtsreeks toewijzen aan een toetsaanslag en door gebruik te maken van virtuele functiewisseltoetsen.

Algemeen gebruikte toetsen, zoals de pijltjestoetsen of de Alt-toets  om bij menu's te komen, kunnen rechtstreeks toegekend worden aan een (willekeurige) brailleinvoer.
De driver voor iedere brailleleesregel is standaard voorzien van een aantal van deze toewijzingen.
U kunt deze toewijzingen aanpassen of er nieuwe geëmuleerde toetsen aan toevoegen vanuit het [dialoogvenster Invoerhandelingen](#InputGestures).

Hoewel deze aanpak goed bruikbaar isvoor algemeen gebruikte of unieke toetsen zoals Tab), wilt u misschien geen unieke set toetsen toewijzen aan elke sneltoets.
Om het emuleren van het indrukken van een toets mogelijk te maken waarbij  een functiewisseltoets ingedrukt gehouden moet worden, beschikt u in NVDA over commando's om te schakelen met control, alt, shift, windows, en de NVDA-toetsen, alsmede over commando's voor enkele  combinaties van die toetsen.
Om deze schakeltoetsen te gebruiken drukt u eerst op het commando (of de commandocombinatie) voor de functiewisseltoetsen die ingedrukt moeten worden. 
Voer dan het karakter (teken) in dat deel uitmaakt van de sneltoets  die u wilt instellen.
Als u bijvoorbeeld control+f wilt bewerkstelligen, gebruikt u  control " als funtiewisseltoetsd en dan typt u een f,
en om control+alt+t, in te stellen gebruikt u of, de control-toets" en  de alt-toets" als de commandotoetsen, in willekeurige volgorde, of de control- en alt-toetsen" om vervolgens een t te typen.

Als u per ongeluk functiewisseltoetsen omschakelt waarmee het funtiewisselcommando opnieuw wordt geactiveerd verliest u de toegewezen funtie.

Als u werkt met verkort braille, met gebruikmaking van de functiewisseltoetsen zal uw invoer zodanig worden omgezet dat het lijkt alsof punten 7+8 werden ingedrukt.
Daarenboven kan de geëmuleerde toetsaanslag geen braille weergeven die werd ingevoerd voordat de schakeltoets was ingedrukt.
Dit houdt in dat, u om alt+2 te typen met een braillecode met een cijferteken erin u eerst moet schakelen met Alt om daarna een cijferteken in te geven.

## Zicht {#Vision}

Hoewel NVDA op de eerste plaats bedoeld is voor blinden of slechtzienden die primair gebruik maken van spraak en/of braille om met een computer te werken, beschikt deze toepassing ook over ingebouwde faciliteiten waarmee de schermweergave kan worden aangepast.
In NVDA wordt zo'n visueel hulpmiddel een element met optische meerwaarde (vision enhancement provider) genoemd.

NVDA beschikt over verschillende elementen met optische meerwaarde die hieronder worden beschreven.
Er kunnen meer elementen met optische meerwaarde aan[NVDA worden toegevoegd via add-ons](#AddonsManager).

NVDA's instellingen voor Zicht kunnen aangepast worden in de  categorie [Zicht](#VisionSettings) in het dialoogvenster [Instellingen NVDA](#NVDASettings).

### Visuele Uitlichting {#VisionFocusHighlight}

Visuele Uitlichting maakt het gemakkelijker de [systeemfocus](#SystemFocus), het [navigatorobject](#ObjectNavigation) en [Bladermodus](#BrowseMode) posities (optisch) te identificeren.
Deze posities worden gemarkeerd met een gekleurde rechthoek er om.

* Egaal blauw markeert de plaats waar navigatorobject en systeemfocus samenkomen, (bijv. omdat het navigatorobject de systeemfocus #ReviewCursorFollowFocus] volgt).
* Gestreept blauw markeert alleen het systeemfocus-object.
* Egaal rose markeert alleen het navigatorobject.
* Egaal geel markeert de virtuele aanwijzer die in bladermodus (waar een fysieke aanwijzer, zoals in een webbrowser, ontbreekt), wordt gebruikt.

Wanneer Visuele Uitlichting ingeschakeld is in de categorie[zicht](#VisionSettings) in het dialoogvenster [NVDA-instellingen](#NVDASettings) , kunt u daar aanpassen of u al dan niet de focus, het navigatorobject of de bladermodusaanwijzer #VisionSettingsFocusHighlight] markeert.

### Scherm Dimmen (Schermgordijn) {#VisionScreenCurtain}

Als blinde of slechtziende gebruiker is het vaak niet mogelijk of noodzakelijk te zien wat er op het scherm wordt weergegeven.
Bovendien kan het heel lastig zijn met zekerheid vast te stellen dat er niet iemand over je schouder meekijkt.
In zo'n geval kent NVDA de optie 'Scherm Dimmen' die ingeschakeld kan worden om een donker scherm te krijgen.

U kunt Scherm Dimmen inschakelen in de categorie [zicht](#VisionSettings) in het dialoogvenster   [Instellingen van NVDA](#NVDASettings).

<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Wijzigt de staat van het schermgordijn |`NVDA+control+escape` |Inschakelen om het scherm te verduisteren of uitschakelen om te laten zien wat er op het scherm wordt weergegeven. Na eenmaal drukken is het schermgordijn actief totdat je NVDA opnieuw start. Na tweemaal drukken screen wordt het schermgordijn geactiveerd totdat je het uitzet.|

<!-- KC:endInclude -->

Wanneer Scherm Dimmen is ingeschakeld, zijn taken die rechtstreeks te maken hebben met wat er op het scherm verschijnt, zoals het uitvoeren van [een OCR-conversie](#Win10OCR) of het maken van een schermafbeelding, niet uitvoerbaar.

Vanwege een wijziging in de Windows vergrotins-API, moetst Scherm Dimmen worden bijgewerkt om ondersteuning te kunnen bieden voor de nieuwste versies van Windows.
Gebruik NVDA 2021.2 om Scherm Dimmen te activeren met Windows 10 21H2 (10.0.19044) of later.
Om zeker te zijn van een veilige werkomgeving bij gebruik van een nieuwe Windowsversie dient u (visueel) na te gaan dan wel laten nagaan of u een volledig donker scherm hebt.

Merk op dat wanneer het Windows-vergrootglas actief is, en er gebruik wordt gemaakt van kleurinversie. het niet mogelijk is om het schermgordijn in te schakelen.

## Inhoudherkenning {#ContentRecognition}

Wanneer auteurs onvoldoende informatie verschaffen waarmee een gebruiker van een schermleesprogramma kan bepalen om welke inhoud het gaat, kunnen verscheidene hulpprogramma's worden gebruikt om de inhoud te herkennen uit een afbeelding.
NVDA ondersteunt de OCR Optical Character Recognition, meestal 'tekstherkenning' genoemd in het nederlands, ) functionaliteit die in Windows 10 en later is ingebouwd om tekst uit afbeeldingen te herkennen.
In andere inhoudherkenningsprogramma's kan worden voorzien met behulp van NVDA add-ons.

Bij gebruik van een inhoudherkenningscommando herkent NVDA inhoud uit het huidige [navigatorobject](#ObjectNavigation).
Standaard volgt het navigatorobject de systeemfocus of de bladermoduscursor, zodat u meestal eenvoudigweg de focus of de bladermoduscursor naar wens kunt verplaatsen.
Als u bijv. de bladermoduscursor naar een grafiek verplaatst, zal de herkenning standaard inhoud herkennen uit de grafiek.
Wellicht wilt u echter direct met objectnavigatie werken om bij voorbeeld de inhoud van een compleet toepassingsvenster te herkennen.

Zodra de herkenning is uitgevoerd, wordt het resultaat gepresenteerd in een bladermodusachtig document zodat u de informatie met behulp van cursortoetsen, etc. kunt lezen.
Door op Enter of Spatie te drukken zal, zo mogelijk, de tekst bij de cursor op de gebruikelijke manier (klikken) worden geactiveerd.
Door op Escape te drukken wordt het herkenningsresultaat geannuleerd.

### Windows OCR {#Win10Ocr}

De OCR-functionaliteit van Windows 10 en later biedt ondersteuning voor veel talen.
NVDA kan hiervan gebruik maken om tekst uit afbeeldingen en ontoegankelijke toepassingen te herkennen.

In de categorie [Windows OCR](#Win10OcrSettings) van het dialoogvenster [Instellingen van NVDA](#NVDASettings) kunt u de tekstherkenningstaal opgeven.
U kunt extra talen toevoegen door in het menu Start, (of met linker Windows-toets +i) Instellingen te kiezen, Tijd en Taal -> Regio & Taal te selecteren en dan Een taal toevoegen te kiezen.

Als u inhoud die aan voortdurende verandering onderhevig is, wilt blijven volgen, bijvoorbeeld bij het bekijken van een video met ondertiteling,kunt u ervoor kiezen de herkende inhoud automatisch te laten verversen.
Dit kunt u ook doen via het dialoogvenster van de categorie [Windows OCR](#Win10OcrSettings) van de [NVDA-instellingen](#NVDASettings) dialog.

Het kan voorkomen dat Windows OCR gedeeltelijk of in het geheel niet compatibel is met [zicht-gerelateerde toepassingen van NVDA](#Vision) of andere externe visuele hulpmiddelen. U zult deze hulpprogramma's dan ook uit moeten schakelen voordat u verder gaat met herkennen.

<!-- KC:beginInclude -->
Om de tekst in het huidige navigatorobject te herkennen met behulp van Windows OCR drukt u op NVDA+r.
<!-- KC:endInclude -->

## Applicatie-specifieke kenmerken {#ApplicationSpecificFeatures}

NVDA beschikt over een aantal applicatie-specifieke kenmerken om het gebruik van deze applicaties te vergemakkelijken, of om toegang te geven tot functionaliteit die anders niet bruikbaar zou zijn voor screenreader gebruikers.

### Microsoft Word {#MicrosoftWord}
#### Automatisch Lezen van Kolom- en Rijhoofden {#WordAutomaticColumnAndRowHeaderReading}

Bij het navigeren in Microsoft Word-tabellen kan NVDA de toepasselijke kolom- en rijhoofden automatisch melden.
Hiertoe moet u er  voor zorgen dat de optie “Kolom-/Rijkoppen Melden” in de categorie Documentopmaak,welke u vindt in het dialoogvenster [Instellingen van NVDA](#NVDASettings), ingeschakeld is. 

Als je gebruik maakt van [UIA voor toegang tot Word-documenten](#MSWordUIA), wat standaard is in recente versies van Word en Windows, zullen de cellen van de eerste rij automatisch beschouwd worden als kolomhoofden; evenzo, zullen de cellen van de eerste kolom automatisch als rijhoofden beschouwd worden.

Als je daarentegen geen gebruik maakt van [UIA voor toegang tot Word-documenten](#MSWordUIA), moet je voor elke willekeurige tabel in NVDA aangeven welkeh rij of kolom als hoofd dient te worden aangemerkt.
Nadat u naar de eerste cel in de kolom of rij bent gegaan waar de kolom- of rijhoofdenn zich bevinden, kunt u de volgende commando’s gebruiken:
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Kolomhoofden instellen |NVDA+shift+c |Door eenmaal indrukken weet NVDA dat dit de eerste cel is in de rij waar de kolomkoppen in staan die automatisch moeten worden gemeld bij het gaan van kolom naar kolom in de rijen eronder. Door tweemaal drukken wordt de instelling opgeheven.|
|Rijhoofden instellen |NVDA+shift+r |Door eenmaal indrukken weet NVDA dat dit de eerste cel is in de kolom waar de rijkoppen in staan die automatisch moeten worden gemeld bij het gaan van rij naar rij na deze kolom. Door tweemaal drukken wordt de instelling opgeheven.|

<!-- KC:endInclude -->
Deze instellingen worden als bladwijzers die compatibel zijn met andere schermlezers zoals JAWS, in het document opgeslagen. 
Dit houdt in dat andere gebruikers die het document op een later moment openen direct gebruik kunnen maken van de reeds ingestelde kolom- en rijhoofden.

#### Bladermodus in Microsoft Word {#BrowseModeInMicrosoftWord}

Evenals bij het navigeren op het web, kunt u Bladermodus in Microsoft Word gebruiken waardoor werken met snelnavigatie en de Lijst met Elementen mogelijk wordt.
<!-- KC:beginInclude -->
Om Bladermodus in Microsoft Word, aan en uit te zetten drukt u op NVDA+spatiebalk.
<!-- KC:endInclude -->
Meer informatie over Bladermodus en Snelnavigatie vindt u in de paragraaf [Bladermodus](#BrowseMode).

##### De Lijst met Elementen {#WordElementsList}

<!-- KC:beginInclude -->
Terwijl u in Bladermodus bent in Microsoft Word, kunt u toegang tot de Lijst met Elementen krijgen door opNVDA+f7 te drukken.
<!-- KC:endInclude -->
De Elementenlijst kan koppen, hyperlinks en annotaties melden met inbegrip van opmerkingen en trackwijzigingen alsmede fouten met dien verstande dat dit momenteel alleen spelfouten betreft.

#### Opmerkingen Melden {#WordReportingComments}

<!-- KC:beginInclude -->
Om eventuele opmerkingen op de positie waar de cursor op dat moment staat te laten melden drukt u op NVDA+alt+c.
<!-- KC:endInclude -->
Alle opmerkingen bij het document alsmede andere trackveranderingen kunnen ook worden opgenomen in de NVDA Elementenlijst wanneer u Annotaties als het type selecteert.

### Microsoft Excel {#MicrosoftExcel}
#### Automatisch Lezen van Kolom- en Rijkoppen {#ExcelAutomaticColumnAndRowHeaderReading}

Bij het navigeren in Microsoft Excel-werkbladen kan NVDA de toepasselijke kolom- en rijkoppen automatisch melden.
Hiertoe moet u er in de eerste plaats voor zorgen dat de optie “Kolom-/Rijkoppen Melden” in de categorie Documentopmaak,welke u vindt in het dialoogvenster [Instellingen van NVDA](#NVDASettings), ingeschakeld is. 
Ten tweede moet NVDA voor elk werkblad weten in welke kolom of rij de kolom-/rijkoppen staan.
Nadat u naar de eerste cel in de kolom of rij bent gegaan waar de kolom- of rijkoppen zich bevinden, kunt u een van de volgende commando’s gebruiken:
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Kolomkoppen instellen |NVDA+shift+c |Door eenmaal indrukken weet NVDA dat dit de eerste cel is in de rij waar de kolomkoppen in staan die automatisch moeten worden gemeld bij het gaan van kolom naar kolom in de rijen eronder. Door tweemaal drukken wordt de instelling opgeheven.|
|Rijkoppen instellen |NVDA+shift+r |Door eenmaal indrukken weet NVDA dat dit de eerste cel is in de kolom waar de rijkoppen in staan die automatisch moeten worden gemeld bij het gaan van rij naar rij na deze kolom. Door tweemaal drukken wordt de instelling opgeheven.|

<!-- KC:endInclude -->
Deze instellingen worden als gedefiniëede naambereiken, die compatibel zijn met andere schermleesprogramma's zoals JAWS, opgeslagen in de werkmap.
Dit houdt in dat andere gebruikers die de werkmap op een later moment openen direct gebruik kunnen maken van de reeds ingestelde kolom- en rijkoppen.

#### De Elementenlijst {#ExcelElementsList}

Evenals voor op het Web heeft NVDA een Elementenlijst voor Microsoft Excel, waarmee u verschillende types informatie in een lijst kunt weergeven en toegankelijk maakt.
<!-- KC:beginInclude -->
Om toegank te krijgen tot de Elementenlijst in Excel, drukt u op NVDA+f7.
<!-- KC:endInclude -->
De volgende types informatie zijn in de Elementenlijst beschikbaar

* Grafieken: Voor het weergeven van alle grafieken op het actieve werkblad.
Door een grafiek te selecteren en op enter of de knop Ga naar te drukken krijgt de grafiek de focus voor navigatie en lezen met de pijltjestoetsen.
* Opmerkingen: Voor het weergeven van cellen op het actieve werkblad dat opmerkingen bevat.
Het cel-adres samen met de opmerkingen erin worden voor elke cel weergegeven.
Door op Enter of de knop Ga Naar te drukken wanneer u op een weergegeven opmerking staat, gaat u direct naar die cel.
* Formules: Voor het weergeven van alle cellen op het werkblad waar een formule in staat.
Het cel-adres samen met bijbehorende formule worden voor elke cel getoond.
Door enter of de Ga Naar-knop in te drukken op een formule in de lijst gaat u rechtstreeks naar  die cel.
* Bladen: Voor het weergeven van alle bladen in de werkmap.
Door f2 te drukken wanneer u zich op een weergegeven blad bevindt, kunt u de naam van het desbetreffende blad wijzigen.
Een druk op de Enter- of de Ga Naar-knop terwijl u zich op een weergegeven blad bevindt, brengt u naar dat blad.
* Formuliervelden: Voor het weergeven van alle formuliervelden op het actieve werkblad.
De Elementenlijst laat voor elk formulierveld, de alternatieve tekst van het veld zien samen met de adressen van de erbijbehorende cellen.
Door een formulierveld te selecteren en op Enter of de Ga naar knop te drukken, gaat u in de Bladermodus naar het desbetreffende veld.

#### Notities Melden {#ExcelReportingComments}

<!-- KC:beginInclude -->
Eventuele notities voor de cel die momenteel de focus heeft, kunt u laten horen door NVDA+alt+c in te drukken.
In Microsoft 2016, 365 en later is de klassieke benaming 'opmerkingen' in Microsoft Excel vervangen door 'notities'.
<!-- KC:endInclude -->
Alle notities voor het werkblad kunnen ook worden weergegeven in de NVDA Elementenlijst  door op NVDA+f7 te drukken.

NVDA kan ook een speciaal dialoogvenster weergeven  voor het toevoegen of bewerken van een bepaalde notitie.
NVDA neemt de plaats in van het oorspronkelijke van MS Excel afkomstige invoerveldd voor notities vanwege toegankelijkheidsbeperkingen, maar de toetscombinatie om het dialoogvenster op te roepen  wordt aan MS Excel ontleend en werkt daarom ook zonder dat NVDA draait.
<!-- KC:beginInclude -->
Om een notitie toe te voegen of te bewerken in een cel die de focus heeft, drukt u op shift+f2.
<!-- KC:endInclude -->

Deze toetscombinatie komt niet voor  en kan niet worden aangepast in de dialoog invoerhandelingen van NVDA. 

Merk op dat u het invoergebied voor notities in MS Excel ook kunt openen vanuit het contextmenu van elke willekeurige cel van het werkblad.
Hiermee opent u evenwel het ontoegankelijke invoerveld voor notities en niet het NVDA-specifieke dialoogvenster.

In Microsoft Office 2016, 365 en later, is een dialoogvenster voor notities nieuwe stijl toegevoegd.
Dit dialoogvenster  is toegankelijk en biedt meer functionaliteit zoals reageren op notities etc.
Het kan ook geopend worden vanuit  het contextmenu van een specifieke cel.
De opmerkingen die aan cellen worden toegevoegd via het dialoogvenster  voor opmerkingen nieuwe stijl staan los van "notities".

#### Beveiligde Cellen Lezen {#ExcelReadingProtectedCells}

Als een werkmap beveiligd is, kan het zijn dat bepaalde cellen die niet mogen worden bewerkt, de focus niet kunnen krijgen.
<!-- KC:beginInclude -->
Om naar beveiligde cellen te gaan, schakelt u over naar Bladermodus door op NVDA+spatiebalk te drukken, en vervolgens gebruikt u standaard Excel navigatieopties zoals de pijltjestoetsen om door de cellen te gaan op het huidige werkblad.
<!-- KC:endInclude -->

#### Formuliervelden {#ExcelFormFields}

Excel werkbladen kunnen formuliervelden bevatten.
Door middel van de Elementenlijst of, de toetsen f en shift+f in letternavigatie kunt u toegang tot het formulierveld krijgen.
Wanneer u in bladermodus naar een formulierveld gaat kunt u op Enter of de spatiebalk drukken om of het veld te activeren of naar focusmodus te wisselen zodat, afhankelijk van het besturingselement, handelingen kunnen worden uitgevoerd.
Voor verdere informatie over Bladermodus en letternavigatie, raadpleegt u de paragraaf [[Bladermodus](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerpoint}

<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Voorlezen aantekeningen van spreker in-/uitschakelen |control+shift+s |Tijdens een lopende presentatie kunt u met dit commando, of de aantekeningen van spreker bij een dia, of de tekst(inhoud) van de dia laten voorlezen. Dit heeft geen invloed op dat wat op het scherm getoond wordt.|

<!-- KC:endInclude -->

### Foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Naam |Toets |Omschrijving|
|---|---|---|
|Resterende tijd melden |control+shift+r |Meldt de resterende tijd van het huidige nummer, indien van toepassing.|
|Verstreken tijd melden |control+shift+e |Meldt, voor zover van toepassing, hoeveel tijd er is verstreken van het nummer dat op dat moment wordt afgespeeld.|
|Speelduur van nummer melden |control+shift+t |Meldt, voor zover van toepassing, de speelduur van het nummer dat op dat moment wordt afgespeeld.|

<!-- KC:endInclude -->

Merk op dat bovengenoemde sneltoetscombinaties alleen werken met de standaard opmaakreeks voor de Foobar-statusregel.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Naam |Toets |Omschrijving|
|---|---|---|
|Recent bericht melden |NVDA+control+1-4 |Meldt een recent bericht, afhankelijk van de gebruikte sneltoets. NVDA+control+2 meldt bijvoorbeeld het op één na nieuwste bericht.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA biedt uitgebreide ondersteuning voor Poedit 3.4 of nieuwer.

<!-- KC:beginInclude -->

| Naam |Toets |Omschrijving|
|---|---|---|
|Aantekeningen voor vertalers melden |control+shift+a |Meldt eventuele aantekeningen voor vertalers. Bij tweemaal drukken worden deze in bladermodus getoond. |Commentaar|
|Opmerkingen melden |control+shift+c |Meldt eventuele opmerkingen in het commentaarvenster. Bij tweemaal drukken worden deze in bladermodus getoond.|
|Oude brontekst melden |`control+shift+o` |Meldt de oude brontekst,als die er is.  Bij tweemaal drukken wordt deze in bladermodus getoond.|
|Vertaalwaarschuwing melden |`control+shift+w` |Meldt eventuele vertaalwaarschuwing. Bij tweemaal drukken wordt deze in bladermodus getoond.|

<!-- KC:endInclude -->

### Kindle voor de PC {#Kindle}

NVDA ondersteunt het lezen van en het navigeren in boeken met Amazon Kindle voor de PC.
Deze functionaliteit is alleen beschikbaar voor Kindle-boeken met het kenmerk "Schermlezers: worden ondersteund" (Screen Reader: supported). U kunt dit nagaan op de pagina met gegevens over het boek in kwestie.

U gebruikt de bladermodus om boeken te lezen.
Deze wordt vanzelf geactiveerd wanneer u een boek opent of de focus ergens in een boekgebied plaatst.
De pagina wordt, wanneer dit aan de orde is, automatisch omgeslagen door de cursor te verplaatsen of met behulp van het commando "Alles uitspreken".
<!-- KC:beginInclude -->
U kunt ook handmatig naar de volgende pagina gaan met de Pagina Omlaag-toets,en met de toets Pagina Omhoog kunt u naar de vorige bladzijde.
<!-- KC:endInclude -->

Navigeren met een enkele lettertoets wordt ondersteund voor koppelingen en afbeeldingen maar alleen binnen de huidige pagina.
Bij het navigeren tussen koppelingen (links) worden ook voetnoten meegenomen.

NVDA biedt ondersteuning (nog in een pril stadium) bij het lezen van en het interactief navigeren door wiskundige inhoud voor boeken met toegankelijke wiskunde.
Raadpleeg hierover het onderdeel [Inhoud van Wiskundige Aard Lezen](#ReadingMath) voor meer informatie.

#### Tekstselectie {#KindleTextSelection}

Met Kindle kunt u verschillende handelingen met betrekking tot geselecteerde tekst, uitvoeren, waaronder het verkrijgen van een definitie uit een woordenboek, het toevoegen van aantekeningen en tekstmarkeringen, het kopiëren van tekst naar het klembord en het doorzoeken van een webpagina. 
Daartoe dient u eerst tekst op de gebruikelijke manier te selecteren in de bladermodus, bijv. met shift en de cursortoetsen.
<!-- KC:beginInclude -->
Nadat u tekst hebt geselecteerd drukt u op de Windows contextmenutoets of op shift+f10 om te zien wat u kunt doen met de selectie.
<!-- KC:endInclude -->
Als u dit doet zonder dat er tekst is geselecteerd, worden de opties getoond voor het woord bij de cursor.

#### Aantekeningen van gebruiker {#KindleUserNotes}

U kunt een aantekening maken bij een woord of een tekstpassage. 
Hiertoe selecteert u eerst de tekst waar het omgaat en roept u het contextmenu voor de selectie op zoals hierboven beschreven.
Vervolgens kiest u "Aantekening toevoegen".

Als u in de bladermodus leest, verwijst NVDA naar deze aantekeningen als Opmerkingen.

Om een aantekening te bekijken, bewerken of verwijderen:

1. verplaatst u de cursor naar de tekst waar de aantekening zich bevindt,
1. roept u het Windows contextmenu op met de opties voor de selectie,
1. kiest u "Aantekening bewerken".

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Wanneer u in de tabelweergave van toegevoegde boeken bent:

| Naam |Toets |Beschrijving|
|---|---|---|
|Enter |enter |Opent het geselecteerde boek.|
|Contextmenu |Toepassingen |Opent het contextmenu voor het geselecteerde boek.|

<!-- KC:endInclude -->

1. Windowsconsool ++[WinConsole]
NVDA biedt ondersteuning voor het Windows-commandoconsool, ( ook wel de Windows-opdrachtmodule genoemd) dat gebruikt wordt door de Opdrachtprompt, de PowerShell, en het Subsysteem van Windows voor Linux.
Het consoolvenster heeft een vaste grootte, in het algemeen veel kleiner dan de buffer met de uitvoer.
Bij het toevoegen van nieuwe tekst schuift de inhoud omhoog en  eerdere tekst verdwijnt uit beeld.
In Windows-versies ouder dan Windows 11 22H2 is tekst die niet getoond wordt in het venster niet toegankelijk met de leescommando's van NVDA.
Daarom moet u het consoolvenster verschuiven om eerder ingevoerde tekst te lezen.
In latere versies van het consool en in Windows Terminal kan de gehele tekstbuffer vrijelijk worden bekeken zonder dat u het venster hoeft te scrollen.
<!-- KC:beginInclude -->
De volgende in het Windows-consool ingebouwde sneltoetscombinaties kunnen bij het [nalezen van tekst](#ReviewingText) met NVDA van pas komen in oudere versies van het Windows-consool:

| Naam |Toets |Beschrijving|
|---|---|---|
|Omhoog schuiven |control+pijltjeOmhoog| Schuift het consoolvenster omhoog om eerder ingevoerde tekst te kunnen lezen.|
|Omlaag schuiven |control+pijltjeOmlaag |Schuift consoolvenster omlaag om later ingevoerde tekst te lezen.|
|Schuiven naar begin |control+home |Schuift consoolvenster nar het begin van de buffer.|
|Schuiven naar einde |control+end |Schuift consoolvenster naar het eind van de buffer.|

<!-- KC:endInclude -->

## NVDA configureren {#ConfiguringNVDA}

De meeste instellingen van NVDA kunnen via dialoogvensters worden aangepast. Om dit te doen gaat u in het NVDA-menu naar “Opties” en kiest u het gewenste sub-menu in het NVDA-menu.
Veel van deze instellingen zijn te vinden in het uit meerdere pagina's bestaande [dialoogvenster Instellingen van NVDA](#NVDASettings).
In alle dialoogvensters geldt dat u met de OK-knop de aangebrachte wijzigingen accepteert.
Door op de knop “Annuleren” of de Escape-toets te drukken worden wijzigingen niet doorgevoerd.
Voor bepaalde dialoogvensters kunt u op de knop Toepassen drukken waarmee de instellingen onmiddellijk worden doorgevoerd zonder dat het dialoogvenster wordt gesloten.
De meeste NVDA dialoogvensters ondersteunen contekstuele hulp.
<!-- KC:beginInclude -->
Ben je in een  dialoogvenster en druk je vervolgens op `f1` dan zal de gebruikershandleiding worden getoond bij de alinea die betrekking heeft op de instelling met focus of op het huidige dialoogvenster.
<!-- KC:endInclude -->
Er zijn instellingen die ook gewijzigd kunnen  worden met sneltoetsen. Deze worden, voor zover van toepassing, hieronder vermeld.

### Instellingen van NVDA {#NVDASettings}

<!-- KC:settingsSection: || Naam | Desktoptoets | Laptoptoets | Beschrijving | -->
NVDA biedt veel configuratie-parameters die met behulp van het dialoogvenster Instellingen zijn aan te passen.
Om het vinden van het type instellingen dat u mogelijk wilt wijzigen te vergemakkelijken treft u in het dialoogvenster  een lijst met configuratie-categorïeenn aan waaruit u een keuze kunt maken.
Wanneer  u een categorie selecteert , ziet u in het dialoogvenster alle daarmee verbandhoudende instellingen.
Om van categorie naar categorie te gaan , gebruikt u `tab` of `shift+tab` om in de lijst met  de categorieën te komen, en vervolgens gebruikt u de pijltjestoetsen om naar boven of naar beneden door de lijst te lopen.
Vanaf een willekeurige plaats in het dialoogvenster kunt u ook een categorie vooruit of terug gaan door respectievelijk  `ctrl+tab`, of  ``shift+ctrl+tab` in te drukken.

Na het wijzigen van een of meer instellingen kunt u de wijzigingen van toepassing laten worden door op de knop "Toepassen" te drukken. Het dialoogvenster zal in dit geval geopend blijven zodat u meer wijzigingen kunt aanbrengen of naar een andere categorie kunt gaan.
Als u uw instellingen wilt opslaan en het dialoogvenster Instellingen van NVDA wilt sluiten gebruikt u de knop 'OK'.

Enkele categorieën instellingen hebben een geheel eigen sneltoets. 
Als deze wordt ingedrukt, wordt het dialoogvenster Instellingen van NVDA rechtstreeks bij die specifieke categorie geopend.
Niet alle categorieën zijn standaard toegankelijk door middel van toetsenbordcommando's.
Als u vaak moet zijn in categorieën die niet over een eigen sneltoets beschikken, kunt u het dialoogvenster [Invoerhandelingen](#InputGestures) gebruiken om een eigen invoerhandeling, zoals een toetsenbordcommando of een aanraakge baar, toe te voegen voor die categorie.

De categorieën instellingen die te vinden zijn in het dialoogvenster Instellingen van NVDA worden hieronder weergegeven.

#### Algemene instellingen {#GeneralSettings}

<!-- KC:setting -->

##### Algemene instellingen openen {#Algemeneinstellingenopenen}

Toets: `NVDA+control+g`

Via de categorie Algemeen van het dialoogvenster Instellingen van NVDA stelt u in hoe NVDA in z'n algemeenheid moet omgaan met zaken zoals de interface-taal en of er al dan niet op updates gecontroleerd moet worden.
In deze categorie zijn de vogende keuzemogelijkheden beschikbaar:

##### Taal {#GeneralSettingsLanguage}

Dit is een vervolgkeuzelijst waarmee u de taal van de gebruikersinterface en de meldingen van NVDA kunt kiezen. 
Er is een groot aantal talen waaruit gekozen kan worden, maar de standaardinstelling is “User default, Windows”.
Hiermee wordt bewerkstelligt dat NVDA de taal gebruikt die standaard op uw PC is ingesteld.

Merk op dat NVDA opnieuw moet worden gestart als u de taal verandert.
Wanneer u gevraagd wordt uw keus te bevestigen, kunt u kiezen uit "Nu opnieuw starten" of "Later herstarten", al naar gelang of u de nieuwe taal respectievelijk meteen of pas later, wilt gebruiken. Als 'Later herstarten wordt gekozen, moet de configuratie ( of handmatig of via de (geactiveerde) functionaliteit 'Opslaan bij afsluiten') worden opgeslagen.

##### Configuratie opslaan bij afsluiten {#GeneralSettingsSaveConfig}

Als u een vinkje plaatst in het selectievakje zal de huidige configuratie automatisch worden opgeslagen bij afsluiting van NVDA.

##### Toon afsluitopties bij het afsluiten van NVDA {#GeneralSettingsShowExitOptions}

Als u het selectievakje aanvinkt, verschijnt er bij het beëindigen van NVDA een dialoogvenster met afsluitopties. 
U hebt de keuze uit Afsluiten, Herstarten, Herstarten zonder add-ons of Installeren van eventueel beschikbare updates.
Wanneer het selectievakje niet aangevinkt is, sluit NVDA meteen af.

##### Geluid bij starten of afsluiten NVDA {#GeneralSettingsPlaySounds}

Als u een vinkje plaatst in dit selectievakje zal NVDA bij het opstarten of afsluiten geluid afspelen.

##### Niveau van loggen {#GeneralSettingsLogLevel}

Dit is een vervolgkeuzelijst waarmee u het niveau van loggen kiest, met andere worden wat moet NVDA allemaal loggen terwijl het draait.
In het algemeen kunt u de standaardinstelling ongewijzigd laten.
Als u evenwel informatie wilt doorgeven over mogelijke bugs van het programma kan het nuttig zijn het niveau van loggen te wijzigen, of u schakelt loggen uit als u dat wilt.

De beschikbare logniveaus zijn:

* Uitgeschakeld: Behalve een korte melding bij opstarten zal NVDA niets loggen.
* Info: NVDA logt basale informatie zoals opstartmeldingen en informatie die nuttig is voor ontwikkelaars.
* Debug-waarschuwing: Waarschuwingen die niet voortkomen uit ernstige fouten worden gelogd.
* Invoer/Uitvoer: Toetsenbordinvoer en invoer van brailleleesregels, alsmede spraak- en braille-uitvoer worden gelogd. 
Als u zich zorgen maakt over uw privacy, kies dan niet voor dit logniveau.
* Debug: Naast info, waarschuwingen, en gegevens uit invoer/uitvoer worden ook debug-berichten  gelogd. 
Evenals voor   invoer/uitvoer geldt hier ook dat u niet voor dit logniveau moet kiezen, als u zich zorgen maakt over uw privacy.

##### NVDA automatisch starten nadat ik me bij windows heb aangemeld {#GeneralSettingsStartAfterLogOn}

Als u het selectievakje aanvinkt, zal NVDA automatisch worden gestart zodra u zich bij Windows aanmeldt.
Deze optie is alleen beschikbaar als NVDA op uw PC is geïnstalleerd, dus niet voor de draagbare versie.

##### NVDA gebruiken bij Windows aanmelding(administratieve rechten vereist) {#GeneralSettingsStartOnLogOnScreen}

Als u zich bij Windows aanmeldt met een gebruikersnaam en een wachtwoord, dan zal NVDA samen met Windows bij aanmelding worden gestart. Hiervoor moet u het selectievakje inschakelen.
Deze optie is alleen beschikbaar als NVDA op uw PC is geïnstalleerd, dus niet voor de draagbare versie.

##### Huidige instellingen van NVDA gebruiken bij windows-aanmelding (administrative rechten vereist) {#GeneralSettingsCopySettings}

Met deze knop kopieert u uw huidige opgeslagen configuratie naar de systeemconfiguratiemap van NVDA, zodat de instellingen worden gebruikt bij het aanmeldscherm, gebruikersaccountbeheerscherm (UAC) en andere [beveiligde Windows-schermen](#SecureScreens).
Om ervoor te zorgen dat alle instellingen worden overgezet, moet u erop letten dat u eerst uw configuratie hebt opgeslagen met control+NVDA+c, of Configuratie Opslaan in het NVDA-menu.
Deze optie is alleen beschikbaar als NVDA op uw PC is geïnstalleerd, dus niet voor de draagbare versie.

##### Automatisch controleren op NVDA updates {#GeneralSettingsCheckForUpdates}

Als dit selectievakje is aangevinkt zal NVDA automatisch controleren of er bijgewerkte versies beschikbaar zijn en dit laten weten als dit het geval is.
Handmatig controleren of er een update beschikbaar is, kan ook. Ga dan naar: “Op update controleren” onder Help in het NVDA Menu.
Wanneer er handmatig of automatisch op updates, wordt gecontroleerd, is het noodzakelijk dat NVDA informatie naar de update-server stuurt zodat u de correcte update voor uw systeem krijgt.
De volgende informatie wordt altijd verstuurd:

* Huidige NVDA-versie
* Versie besturingssysteem
* Of het besturingssysteem 64- of 32-bit is

##### NV Access toestaan NVDA-gebruiksstatistieken te verzamelen {#GeneralSettingsGatherUsageStats}

Als dit wordt toegestaan zal NV Access de informatie van update checks gebruiken om het aantal NVDA-gebruikers vast te stellen met inbegrip van specifieke demografische gegevens zoals besturingssysteem en land van oorsprong.
Merk op dat uw IP-adres nooit wordt bewaard, al wordt het wel gebruikt tijdens de update-check om uw land te bepalen.
Naast de vereiste informatie voor het controleren op updates, wordt de volgende extra informatie momenteel ook verstuurd:

* interface-taal van NVDA 
* Of het gaat om een draagbare of geïnstalleerde kopie van NVDA 
* Naam van de spraaksynthesizer die op dat moment in gebruik is(met inbegrip van de naam van de add-on waar de driver vandaan komt)
* Naam van de Brailleleesregel die op dat moment in gebruik is ((met inbegrip van de naam van de add-on waar de driver vandaan komt)
-de huidige Brailleuitvoertabel (als Braille wordt gebruikt)

Deze informatie is van grote waarde voor NV Access om te kunnen bepalen waar de aandacht bij voorrang naar moet uitgaan bij de ontwikkeling van NVDA in de toekomst.

##### Beschikbare Updates bij opstarten melden {#GeneralSettingsNotifyPendingUpdates}

Als deze optie is ingeschakeld zal NVDA u laten weten wanneer er een update beschikbaar is bij het starten van het programma, waarbij u de mogelijkheid wordt geboden deze te installeren.
Een beschikbare update kan ook handmatig worden geïnstalleerd vanuit het dialoogvenster 'NVDA Afsluiten'(mits deze optie ingeschakeld is) of vanuit het NVDA-menu, door op updates te controleren via het Help-menu.

#### Spraakinstellingen {#SpeechSettings}

<!-- KC:setting -->

##### Spraakinstellingen openen {#Spraakinstellingenopenen}

Toets:`NVDA+control+v` 

In de categorie Spraak van het dialoogvenster Instellingen kunt u van spraaksynthesizer veranderen maar ook stemkarakteristieken van de gekozen synthesizer aanpassen.
Een snellere, alternatieve manier om steminstellingen te wijzigen vindt u onder [Synth Settings Ring](#SynthSettingsRing).

In de categorie Spraak vindt u de volgende opties:

##### Van synthesizer veranderen {#SpeechSettingsChange}

De eerste optie in de categorie Spraak is de knop Wijzigen`. Met deze knop activeert u de dialoog [Synthesizer Selecteren](#SelectSynthesizer) , waarmee u de actieve spraaksynthesizer en het uitvoerapparaat selecteert. 
Deze dialoog opent zich over het dialoogvenster Instellingen van NVDA heen.
Door de instellingen in de dialoog Synthesizer Selecteren op te slaan of te verrwerpen keert u terug naar het dialoogvenster Instellingen van NVDA.

##### Stem {#SpeechSettingsVoice}

Deze optie is een vervolgkeuzelijst waarin alle stemmen staan waarover de momenteel gebruikte synthesizer beschikt.
Met de pijltoetsen kunt u alle keuzemogelijkheden beluisteren.
Met pijl links en pijl omhoog gaat u naar het begin van de lijst en met pijl rechts en pijl omlaag naar het einde.

##### Variant {#SpeechSettingsVariant}

Als u gebruik maakt van de eSpeak NG synthesizer, die standaard is opgenomen in NVDA, kunt u via een vervolgkeuzelijst een stemvariant kiezen.
Met de stemvarianten kunt u stemeigenschappen enigszins aanpassen.
Er zijn varianten die als een mannen- of vrouwenstem klinken of zelfs als een kikker.
Bij gebruik van een synthesizer van derden, kunt u deze waarde wellicht ook aanpassen als de gekozen stem hiervoor ondersteuning biedt.

##### Snelheid {#SpeechSettingsRate}

Hiermee kunt u de spraaksnelheid instellen.
tDe schuifregelaar gaat van 0 tot 100 (0 is de laagste en 100 de hoogste snelheid).

##### Snelheid opvoeren {#SpeechSettingsRateBoost}

Met het activeren van deze optie verhoogt u de spreeksnelheid flink, op voorwaarde dat de gebruikte synthesizer hiervoor ondersteuning biedt.

##### Toonhoogte {#SpeechSettingsPitch}

Hiermee stelt u de hoogte van de gebruikte stem in.
De schuifregelaar gaat van 0 tot 100 ( bij 0 klinkt de stem het laagst en op 100 het hoogst).

##### Volume {#SpeechSettingsVolume}

Met de schuifregelaar kunt u het volume van de stem instellen waarbij 0 het laagste en 100 het hoogste volume is. 

##### Intonatie {#SpeechSettingsInflection}

Met de schuifregelaar kunt u instellen welk intonatieniveau de stem moet gebruiken, dus hoe sterk de stem in toonhoogte moet variëren. De enige synthesizer die op het moment deze mogelijkheid biedt is eSpeak NG.

##### Automatisch van taal wisselen {#SpeechSettingsLanguageSwitching}

Met dit selectievakje bepaalt u of NVDA automatisch naar een andere spraaksynthesizertaal moet overschakelen als het te lezen document is voorzien van taalcodes, zoals NL voor Nederlands.
Deze optie is standaard ingeschakeld.

##### Automatisch van dialect wisselen {#SpeechSettingsDialectSwitching}

Indien automatisch van taal wisselen is ingeschakeld, kan deze optie gebruikt worden om aan te geven dat ernaar een andere taalvariant moet worden overgeschakeld in plaats van enkel taalwisselingen. 
Als een tekst bijvoorbeeld als Brits Engels is gemarkeerd zal de synthesizer een Britse variant van het Engels gebruiken als deze optie is ingeschakeld.
Deze optie staat standaard uit.

<!-- KC:setting -->

##### Interpunctie-/symboolniveau {#SpeechSettingsSymbolLevel}

Toets: NVDA+p

Deze optie bepaalt welke leestekens en symbolen als woorden worden uitgesproken.
Als deze optie bijvoorbeeld op alles staat, zullen alle symbolen als woorden worden uitgesproken.
Deze optie geldt voor alle synthesizers, niet enkel de actieve synthesizer.

##### Vertrouw taal van stem bij het verwerken van karakters en symbolen {#SpeechSettingsTrust}

Met deze optie, die standaard staat ingeschakeld, kunt u NVDA laten weten of de gebruikte stemtaal betrouwbaar moet worden geacht voor de verwerking van symbolen en tekens. 
Als u vaststelt dat NVDA interpunctie in de verkeerde taal leest, een taal die niet overeenkomt met die van de gebruikte synthesizer of stem, dan wilt u deze optie wellicht uitschakelen waarmee u NVDA dwingt de algemene taalinstelling te gebruiken.

##### Unicode Consortium data (met inbegrip van emoji) opnemen bij het verwerken van karakters en symbolen {#SpeechSettingsCLDR}

Wanneer dit selectievakje aangevinkt is, zal NVDA extra uitspraakwoordenboeken raadplegen bij het uitspreken van (letter)tekens en symbolen.
In deze woordenboeken staan beschrijvingen van symbolenin het bijzonder emoji) die afkomstig zijn van [het Unicode Consortium](https://www.unicode.org/consortium/) als onderdeel van hun [Common Locale Data Repository](http://cldr.unicode.org/).unicode.org/].
Als u wilt dat NVDA de op basis van deze data gebaseerde beschrijving van emoji-tekens leest, moet u deze optie inschakelen.
Als u evenwel een spraaksynthesizer gebruikt die zelf zorgt voor het uitspreken van emoji-beschrijvingen, wilt u deze mogelijk uitschakelen.

Merk op dat handmatig toegevoegde of bewerkte beschrijvingen van (letter)tekens als onderdeel van uw gebruikersinstellingen bewaard worden.
Dit betekent dat, als u de beschrijving van een specifiek emoji verandert, uw aangepaste beschrijving voor die emoji altijd zal worden gelezen ongeacht of deze optie is ingeschakeld.
U kunt symboolbeshrijvingen toevoegen, bewerken of verwijderen in [het dialoogvenster Uitspraak interpunctie/symbolen van NVDA](#SymbolPronunciation).

Om Unicode Consortium data van elke willekeurige plaats al dan niet op te nemen kunt uzelf een invoerhandeling aanmaken met behulp van het dialoogvenster Invoerhandelingen #InputGestures].

##### Percentage toonhoogteverandering bij hoofdletters {#SpeechSettingsCapPitchChange}

Dit tekstvak stelt u in staat om de mate waarin de toonhoogte van de stem verandert zodra een hoofdletter wordt gelezen in te stellen.
Deze waarde is een percentage, een negatieve waarde verlaagt de toonhoogte en een positieve waarde verhoogt de toonhoogte.
Om de toonhoogte niet te veranderen voert u 0 in.
Gebruikelijk is dat  NVDA elke hoofdletter op een iets hogere toon uitspreekt, maar er kunnen synthesizers zijn die hiervoor geen goede ondersteuning bieden.
Indien hoofdletters zonder verhoging van toon worden uitgesproken, kunt u overwegen om in plaats hiervan [ "hoofdletter"zeggen voor een hoofdletter](#SpeechSettingsSayCapBefore) en/of [ pieptoon bij hoofdletters](#SpeechSettingsBeepForCaps) te gebruiken.

##### Het woord "Hoofdletter" uitspreken bij lezen van hoofdletters {#SpeechSettingsSayCapBefore}

Als dit selectievakje is aangevinkt zal NVDA, waar nodig, het woord “hoofdletter” zeggen bij het lezen en typen.

##### Pieptoon bij hoofdletters {#SpeechSettingsBeepForCaps}

Als dit selectievakje is aangevinkt zal NVDA een korte pieptoon laten horen telkens wanneer er sprake is van een hoofdletter.

##### Spellingfunctionaliteit gebruiken (wanneer ondersteund) {#SpeechSettingsUseSpelling}

Er zijn woorden die slechts uit één letterteken bestaan. Een voorbeeld hiervan is "a" in het Engels of "u" in het Nederlands. 
Als "a" in het Engels als woord wordt gebruikt (het equivalent van het Nederlandse "een") is de uitspraak anders dan wanneer we de naam van dit letterteken uitspreken zoals bij het spellen.
Door het selectievakje aan te vinken kan de synthesizer het verschil in uitspraak weergeven.
De meeste synthesizers ondersteunen deze functionaliteit.

In het algemeen is het aan te bevelen dit selectievakje aan te vinken. 
Er zijn evenwel synthesizers die van de Microsoft API gebruik maken die met de uitspraak van individuele lettertekens niet goed omgaan. 
Als u problemen hiermee ondervindt, kunt u het selectievakje beter niet aanvinken.

##### Vertraagde beschrijving van (letter)tekens bij cursorverplaatsing {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Ingeschakeld, Uitgeschakeld|
|---|---|
| Standaard |Uitgeschakeld|
|---|---|

Wanneer deze optie is aangevinkt zal NVDA het (letter)teken nader beschrijven wanneer  u de cursor letter voor letter verplaatst.

Wanneer u bijvoorbeeld een regel letter voor letter naleest, krijgt u bij de letter "b" met een vertraging van 1 seconde "Bravo" te horen.
Dit kan handig zijn als het lastig is het verschil in uitspraak te horen tussen 2 letters of voor slecht horende gebruikers.

De vertraagde nadere beschrijving van lettertekens komt niet ten uitvoer als er in de tussentijd andere tekst wordt voorgelezen of als u op de `control` toets drukt.

##### Modi beschikbaar in de Opdrachtreeks spraakmodus command {#SpeechModesDisabling}

Deze lijst met items die aangekruist kunnen worden om te bepalen [welke spraakmodi](#SpeechModes) worden meegenomen als je door de lijst gaat met `NVDA+s`.
Modi die niet zijn aangekruist worden niet meegenomen.
Standaard worden alle modi meegenomen.

Als je bijv. "piepjes" en "uit" modus niet hoeft te gebruiken,kun je het vinkje daarvan  beter  weghalen, en die van "sprekenk" en "on-demand" laten staan.
Merk op dat ten minste twee modi aangevinkt moeten zijn.

#### Synthesizer Selecteren (NVDA+control+s) {#SelectSynthesizer}

<!-- KC:setting -->

##### Dialoogvenster synthesizer selecteren openen {#synthesizerselecterenOpenen}

Toets: `NVDA+control+s`

Via het dialoogvenster Synthesizer dat u kunt openen door de knop Wijzigen te activeren in de categorie spraak van de dialoog Instellingen van NVDA kunt u selecteren welke Synthesizer NVDA moet gebruiken voor spraakuitvoer.
Als u de synthesizer van uw keuze hebt geselecteerd, kunt u op Ok drukken en NVDA zal de geselecteerde Synthesizer laden.
Als er een fout optreedt bij het laden van de synthesizer, zal NVDA dit melden en de vorige synthesizer blijven gebruiken.

##### Synthesizer {#SelectSynthesizerSynthesizer}

Hiermee kunt u de synthesizer kiezen die u NVDA wilt laten gebruiken voor de spraakuitvoer.

Voor een lijst met de Synthesizers die NVDA ondersteunt gaat u naar het onderdeel [Ondersteunde Sppraaksynthesizers](#SupportedSpeechSynths).

Er is één specifieke optie die altijd in deze lijst voorkomt en wel “geen spraak” waarmee alle spraakuitvoer wordt uitgeschakeld.
Dit kan nuttig zijn voor iemand die NVDA uitsluitend met braille wil gebruiken of voor goedziende ontwikkelaars die uitsluitend de speech viewer willen gebruiken.

#### Synth settings ring {#SynthSettingsRing}

Om spraakinstellingen snel aan te passen zonder dat u naar de categorie Spraak gaat van het dialoogvenster Instellingen van NVDA, kunt u te allen tijde beschikken over een aantal toetscombinaties terwijl u met NVDA werkt:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Beschrijving|
|---|---|---|---|
|Naar volgende synthesizerinstelling gaan |NVDA+control+pijl rechts |NVDA+shift+control+pijl rechts |Hiermee wordt steeds een volgende spraakinstelling gekozen. Na de laatst beschikbare instelling begint u weer vooraan enz.|
|Naar vorige spraakinstelling gaan |NVDA+control+pijl Links |NVDA+shift+control+pijl Links |Hiermee wordt de spraakinstelling gekozen die onmiddellijk voorafgaat aan de huidige. Eenmaal bij de eerste instelling bovenaan de lijst aangekomen begint u weer onderaan enzovoorts.|
|Oplopend bijstellen van huidige synthesizerinstelling |NVDA+control+Pijl Omhoog |NVDA+shift+control+Pijl Omhoog |Stelt de momenteel gebruikte spraakinstelling naar bovenbij. Verhoogt bij voorbeeld snelheid en volume, selecteert volgende stem.|
|De huidige synthesizer-instelling in grotere stappen oplopend bijstellen |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Verhoogt de waarde van de momenteel geldende spraakinstelling met een groter bereik. Als je je bijv wilt veranderen van stem, spring je steeds 20 stemmen vooruit; voor aanpassingen met een schuifbalk (snelheid, toonhoogte, etc) wordt de waarde met tot 20% verhoogd.|
|De huidige synthesizerinstelling aflopend bijstellen |NVDA+control+Pijl Omlaag |NVDA+shift+control+Pijl Omlaag |Stelt momenteel gebruikte spraakinstelling naar beneden bij. Verlaagt bij voorbeeld snelheid en volume, selecteert vorige stem|
|De huidige synthesizer-instelling in grotere stappen aflopend bijstellen |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Verlaagt de waarde van de momenteel geldende spraakinstelling met een groter bereik. Als je bijv wilt veranderen van stem, spring je steeds 20 stemmen terug; voor aanpassingen met een schuifbalk (snelheid, toonhoogte, etc) wordt de waarde met tot 20% verlaagd.|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

De categorie Braille in het dialoogvenster Instellingen van NVDA bevat opties waarmee u verschillende aspecten met betrekking tot de invoer en uitvoer van braille kunt aanpassen.
In deze categorie treft u de volgende opties aan:

##### Van leesregel veranderen {#BrailleSettingsChange}

Met de knop Wijzigen. in de categorie Braille van de dialoog Instellingen van NVDA activeert u de dialoog [Brailleleesregel Selecteren](#SelectBrailleDisplay) , waarmee u de actieve brailleleesregel selecteert. 
Deze dialoog opent zich over het dialoogvenster Instellingen van NVDA heen.
Door de instellingen in de dialoog Brailleleesregel Selecteren op te slaan of te verrwerpen keert u terug naar het dialoogvenster Instellingen van NVDA.

##### Uitvoertabel {#BrailleSettingsOutputTable}

Vervolgens komt u in deze categorie de vervolgkeuzelijst met braille-uitvoertabellen tegen.
In de lijst vindt u brailletabellen voor verschillende talen, braillestandaarden en graden.
De gekozen tabel zorgt ervoor dat tekst wordt omgezet in braille voor weergave op de brailleleesregel.
U kunt de pijltjestoetsen gebruiken om door de lijst met brailletabellen te navigeren.

##### Invoertabel {#BrailleSettingsInputTable}

Aanvullend op de vorige optie, is de volgende instelling die je tegenkomt de optie de vervolgkeuzelijst  met brailleinvoer-tabellen. 
Met de gekozen tabel kun je braille ingevoerd met een toetsenbord van het type Perkins omzetten intekst. 
U kunt de pijltjestoetsen gebruiken om door de lijst met brailletabellen te navigeren.

Merk op dat deze instelling alleen zinvol is als uw leesregel over een toetsenbord van het Perkins-type beschikt en het stuurprogramma van uw brailleleesregel hiervoor ondersteuning biedt. 
Als invoer niet wordt ondersteund door een leesregel die is uitgerust met een brailletoetsenbord, wordt dit vermeld in de rubriek [ondersteunde Brailleleesregels](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Braillemodus {#BrailleMode}

Toets: `NVDA+alt+t`

Met deze optie kun je een keuze maken uit de beschikbare braillemodi.

Momenteel worden er twee braillemodi ondersteund, "cursors volgen" en "spraakuitvoer tonen".

Wanneer  er voor cursors volgen is gekozen, zal de brailleleesregel  of wel de systeemfocus/caret of de navigator-object/review cursor volgen, afhankelijk van de ingestelde braille-koppeling.

Wanneer er gekozen wordt voor spraakuitvoer tonen, zal de brailleleesregel  weergeven wat NVDA zegt of gezegd zou hebben als  "talk" geactiveerd zou zijn.

##### Woord onder cursor uitbreiden naar computerbraille {#BrailleSettingsExpandToComputerBraille}

Door het selectievakje aan te vinken wordt het woord onder de cursor weergegeven in niet-verkort computerbraille.

##### Cursor weergeven {#BrailleSettingsShowCursor}

Met deze optie kunt u de braillecursor in- en uitschakelen.
Deze mogelijkheid is beschikbaar voor de invoegcursor en de leescursor, maar niet voor de selectie-indicator.

##### Knipperende cursor {#BrailleSettingsBlinkCursor}

Met deze optie kunt u een braillecursor laten knipperen.
Als knipperen wordt uitgezet, blijft de braillecursor steeds in de "omhoog" stand staan.
Deze optie heeft geen invloedt op de selectie-indicator. Hierop is altijd punt 7 en punt 8 van toepassing en de indicator knippert niet.

##### Knippersnelheid cursor {#BrailleSettingsBlinkRate}

In het invoerveld kunt u een getal invoeren dat de knippersnelheid van de cursor bepaalt in milliseconden.

##### Cursorvorm voor Focus {#BrailleSettingsCursorShapeForFocus}

Met deze optie kunt u de vorm (puntenpatroon) van de braillecursor kiezen wanneerbraille de focus moet volgen.
Deze optie heeft geen invloedt op de selectie-indicator. Hierop is altijd punt 7 en punt 8 van toepassing en de indicator knippert niet.

##### Leescursorvorm (Review) {#BrailleSettingsCursorShapeForReview}

Met deze optie kunt u de vorm (puntenpatroon) van de braillecursor kiezen wanneerbraille de leescursor (review) moet volgen.
Deze optie heeft geen invloedt op de selectie-indicator. Hierop is altijd punt 7 en punt 8 van toepassing en de indicator knippert niet.

##### Meldingen tonen {#BrailleSettingsShowMessages}

Dit is een keuzelijst waarmee u kunt kiezen of NVDA braillemeldingen wel of niet moet tonen  en wanneer eventuele meldingen automatisch moeten verdwijnen.

Om "Toon meldingen" van elke willekeurige plek in of uit te schakelen kunt u desgewenst een eigen invoerhandeling aanmaken met behulp van  het dialoogvenster [Invoerhandelingen](#InputGestures).

##### Time-out voor meldingen (sec.) {#BrailleSettingsMessageTimeout}

In het invoerveld kunt u een getal invoeren waarmee u bepaalt hoe lang NVDA-meldingen op de brailleleesregel worden weergegeven.
De melding van NVDA  verdwijnt onmiddellijk wanneer er een routing-toets op de brailleleesregel  wordt ingedrukt, maar verschijnt bij het indrukken van een corresponderende toets waarmee de melding wordt opgeroepen.
Deze optie is alleen beschikbaar als Meldingen tonen" ingesteld is op 'timeout" gebruiken.

<!-- KC:setting -->

##### Braille koppelen {#BrailleTether}

Toets: NVDA+control+t

Hiermee kunt u bepalen of de leesregel de systeemfocus / systeemcursor, het navigatorobject / de reviewcursor of beide moet volgen
Wanneer u "automatisch" selecteert, zal NVDA de systeemfocus en systeemcursor standaard volgen.
In dit geval zal NVDA, bij wisseling van positie met betrekking tot navigatorobject of de reviewcursor door toedoen van de gebruiker, tijdelijk overgaan naar de review-modus, tot de focus of de systeemcursor verandert.
Als u wilt dat alleen focus en caret gevolgd worden moet u een braillekoppeling  met de focus instellen.
In dit geval zal braille de NVDA navigator tijdens objectnavigatie of de leescursor bij het lezen niet volgen
Als u wilt dat braille in plaats daarvan objectnavigatie en tekst-review volgt, moet u een braillekoppeling met  review instellen.
In dit geval  zal Braille  de systeemfocus en systeemaanwijzer niet volgen.

##### Invoercursor verplaatsen bij routering van leescursor {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Nooit), Nooit, Alleen bij automatisch tethering, Altijd|
|---|---|
| Standaard |Nooit|
|---|---|

Deze instelling bepaalt of de invoercursor ook verplaatst moet worden  bij het indrukken van de routing-knop.
Deze optie staat standaard ingesteld op Nooit, wat inhoudt dat met routing de invoercursor nooit wordt verplaatst bij routing van de leescursor.

Als deze optie op  Altijd staat ingesteld, en [braille-koppeling](#BrailleTether) op "automatisch" of op review" staat, zal het indrukken van een cursor routing-toets de invoercursor of de focus eveneens verplaatsen indien ondersteund.
Wanneer de geldende overzichtsmodus [Schermoverzicht is](#ScreenReview), is er geen fysieke aanwijzer.
In dit geval probeert NVDA de focus op het object onder de tekst te plaatsen war je naar routeert.
Hetzelfde geldt voor [objectoverzicht](#ObjectReview).

U kunt deze optie ook zo instellen dat de aanwijzer alleen wordt verplaatst indien automatisch gekoppeld (tethered) is ingesteld.
In dat geval zal bij het indrukken van een cursor routing-toets alleen de systeemcursor of de focus worden verplaatst als NVDA automatisch aan de leescursor is gekoppeld (tethered), terwijl er van verplaatsing geen sprake is bij een handmatige koppeling met de leescursor.

Deze optie wordt alleen getoond indien "[braille koppelen](#BrailleTether)" op 'Automatisch" of "op review" is ingesteld.

Om de wijze waarop het verplaatsen van de systeemcursor moet verlopen aan te passen bij routering van de leescursor van af een willekeurige plaats, kunt u een aangepaste invoerhandeling toekennen met behulp van het dialoogvenster [Invoerhandelingen](#InputGestures).

##### Lezen per alinea {#BrailleSettingsReadByParagraph}

Als deze optie is ingeschakeld, zal braille per alinea in plaats van per regel worden weergegeven.
Ook de vorige/volgende regel commando's zullen van alinea naar alinea springen.
Dit betekent dat u de brailleleesregel niet hoeft te scrollen aan het eind van een regel als er nog meer tekst op de leesregel past.
Dit maakt het mogelijk om grote hoeveelheden tekst vloeiender te lezen.
Deze optie is standaard uitgeschakeld.

##### Waar mogelijk woorden niet afbreken {#BrailleSettingsWordWrap}

Wanneer deze optie is ingeschakeld, zal een woord dat te lang is om nog op de brailleregel te passen niet worden afgebroken.
In plaats daarvan blijft er wat lege ruimte aan het einde van de brailleleesregel.
Door te scrollen kunt u het gehele woord lezen.
Dit wordt wel “word wrap” of woordterugloop genoemd.
Merk op dat een woord dat van zichzelf zodanig lang is dat het niet op de regel past, toch afgebroken moet worden.

Wanneer deze optie is uitgeschakeld, wordt zoveel mogelijk tekst op de regel geplaatst terwijl wat overblijft wordt afgekapt. 
Door te scrollen kunt u dan de rest van het woord lezen.

Vloeiend lezen wordt gemakkelijker door deze optie in te schakelen, maar u zult als gevolg hiervan meer moeten scrollen.

##### Te tonen focuscontext {#BrailleSettingsFocusContextPresentation}

Met deze optie kunt u kiezen welke contextinformatie NVDA op de brailleleesregel moet tonen wanneer een object de focus krijgt.
Contextinformatie heeft betrekking op de hierarchie van objecten die de focus hebben.
Wanneer bij voorbeeld een lijst-item de focus krijgt, is dit lijst-item onderdeel van een lijst.
Deze lijst zou als bovenliggend object een dialoogvenster kunnen hebben, etc.
Raadpleeg het onderdeel [objectnavigatie](#ObjectNavigation) voor meer informatie over de hierarchie die van toepassing is op objecten in NVDA.

Bij selectie van de instelling leesregel vullen voor contextveranderingen zal NVDA proberen zoveel mogelijk contextinformatie op de brailleleesregel te tonen als moglijk is, maar alleen voor die onderdelen van de context die veranderd zijn.
Voor het bovengenoemde voorbeeld betekent dit dat NVDA een lijstitem zal tonen op de brailleleesregel wanneer een lijst de focus krijgt.
Verder zal NVDA proberen, als er voldoende ruimte over is op de leesregel, weer te geven dat het lijstitem deel uitmaakt van een lijst.
Als u vervolgens met de pijltoetsen door de lijst gaat, wordt er vanuit gegaan dat u er zich van bewust bent dat u zich nog steeds in een lijst bevindt.
Hieruit volgt dat voor de resterende lijstitems die u selecteert, NVDA alleen het lijstitem op de leesregel zal tonen dat de focus heeft.
Om de context opnieuw te lezen(dat wil zeggen als u zich in een lijst bevindt en de lijst deel uitmaakt van een dialoogvenster), moet u uw leesregel terugscrollen.

Bij selectie van de instelling leesregel altijd vullen zal NVDA proberen zoveel mogelijk contextinformatie op de brailleleesregel te tonen, ongeacht of u dezelfde contextinformatie al eerder zag.
Dit heeft als voordeel dat NVDA zoveel informatie als mogelijk is op de leesregel zal proberen weer te geven. 
Daar staat als nadeel tegenover dat de plaats op de brailleleesregel waar de focus begint telkens kan veranderen.
Hierdoor kan het bij voorbeeld lastig worden om door een lange lijst met items te lopen omdat u voortdurend uw vinger moet verplaatsen om het begin van het item te vinden.
In NVDA 2017.2 en eerder was dit de standaardinstelling.

Als u bij de optie te tonen contextinformatie kiest voor Alleen bij terugscrollen, toont NVDA standaard nooit contextinformatie op uw brailleleesregel.
Met betrekking tot bovengenoemd voorbeeld houdt dit in dat NVDA weergeeft dat u een lijstitem hebt geselecteerd.
Als u de context echter wilt lezen (dat wil zeggen wanneer u zich in een lijst bevindt en de lijst is onderdeel van een dialoog), moet u uw leesregel terugscrollen.

Om Te tonen contextinformatie aan of uit te zetten vanaf elke willekeurige plaats kunt u een aangepaste invoerhandeling toekennen met behulp van het [dialoogvenster Invoerhandelingen](#InputGestures).

##### Spraak onderbreken tijdens het scrollen {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Ingeschakeld), Ingeschakeld, Uitgeschakeld|
|---|---|
| Standaard |Ingeschakeld|
|---|---|

Met deze instelling bepaalt u of de spraak moet worden onderbroken bij vooruit-/achteruitscrollen van de brailleleesregel.
De opdracht 'Vorige/Volgende'regel leidt altijd tot onderbreking van de spraakuitvoer.

Het gesproken woord kan ertoe leiden dat de aandacht wordt afgeleid tijdens het braille-lezen.
Dat is de reden dat de optie, spraak onderbreken tijdens het scrollen van braille, standaard staat ingeschakeld.

Door deze optie uit te schakelen kunt u wat u in braille leest gelijktijdig hardop laten voorlezen.

##### Selectie tonen {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Ingeschakeld), Ingeschakeld, Uitgeschakeld|
|---|---|
| Standaard |Ingeschakeld|
|---|---|

Deze instelling bepaalt of de selectieaanwijzer (punt 7 en punt 8) op  de brailleleesregel wordt getoond.
De optie staat standaard aan, dus wordt de selectieaanwijzer  getoond.
De Selectieaanwijzer kan tijdens het lezen storend zijn.
De optie uitzetten kan het leesgemak bevorderen.

Om "Toon selectie' van elke willekeurige plek in of uit te schakelen kunt u desgewenst een eigen invoerhandeling aanmaken met behulp van  het dialoogvenster [Invoerhandelingen](#InputGestures).

#### Brailleleesregel Selecteren (NVDA+control+a) {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Dialoogvenster brailleleesregel selecteren openen {#OpenSelectBrailleDisplay}

Toets: `NVDA+control+a`

Via het dialoogvenster Brailleleesregel Selecteren dat u kunt openen door de knop Wijzigen te activeren in de categorie Braille van de dialoog Instellingen van NVDA kunt u selecteren welke leesregel NVDA moet gebruiken voor brailleuitvoer.
Als u de leesregel van uw keuze hebt geselecteerd, kunt u op Ok drukken en NVDA zal de geselecteerde leesregel laden.
Als er een fout optreedt bij het laden van de leesregel-driver zal NVDA dit melden en de eventuele vorige leesregel blijven gebruiken.

##### Brailleleesregel {#SelectBrailleDisplayDisplay}

Afhankelijk van de beschikbare leesregelstuurprogramma's op uw systeem biedt deze vervolgkeuzelijst u een aantal opties.
Met de pijltjestoetsen gaat u door de verschillende opties.

Met de optie automatisch zoekt NVDA op de achtergrond naar veel ondersteunde leesregels.
Wanneer deze optie ingeschakeld is, en u een ondersteunde leesregel aansluit via USB of bluetooth, brengt NVDA automatisch een verbinding met deze leesregel tot stand.

'Geen braille' wil zeggen dat u geen gebruik maakt van braille.

Raadpleeg de rubriek [Ondersteunde Brailleleesregels](#SupportedBrailleDisplays) voor meer informatie over ondersteunde leesregels en welke hiervan automatische herkenning op de achtergrond ondersteunen.

##### Automatisch te detecteren leesregels {#SelectBrailleDisplayAutoDetect}

Wanneer  een brailleleesregel op "Automatisch", ingesteld staat, kunt u via de selectievakjes in deze besturingslijst de display drivers activeren en deactiveren voor zover deze al dan niet betrokken moeten worden in het automatische detectieproces.
Hiermee kunt u brailleleesregeldriversuitsluiten die u niet regelmatig gebruikt.
Als u bijvoorbeeld alleen maar een leesregel hebt die met een driver van Baum werkt, kunt u de Baum-driver ingeschakeld laten terwijl de andere drivers kunnen worden uitgeschakeld.

Standaard staan alle drivers die automatische detectie ondersteunen ingeschakeld.
Elke driver die bijvoorbeeld in een toekomstige versie  van NVDA of via een add-on, wordt toegevoegd staat ook standaard ingeschakeld.

Raadpleeg de documentatie mbt uw brailleleesregel onder [Ondersteunde Brailleleesregels](#SupportedBrailleDisplays) of het desbetreffende stuurprogramma automatische detectie van leesregels ondersteunt.

##### Poort {#SelectBrailleDisplayPort}

Indien beschikbaar kunt u met deze optie kiezen welke poort of welk type verbinding er gebruikt wordt om te communiceren met de leesregel die u hebt geselecteerd.
Het betreft een vervolgkeuzelijst met mogelijke keuzes voor uw brailleleesregel.

Standaard voert NVDA een automatische poortdetectie uit, hetgeen inhoudt dat de verbinding met het brailletoestel automatisch tot stand wordt gebracht door te zoeken naar beschikbare USB- en bluetooth-apparaten op uw systeem.
Voor sommige brailleleesregels, kunt u echter expliciet kiezen welke poort gebruikt moet worden.
Algemene opties verlopen "Automatisch" (wat inhoudt dat NVDA standaard een automatische poortselectieprocedure uitvoert) voor "USB-", "Bluetooth-" en legacy seriële communicatiepoorten als uw brailleleesregel dit type communicatie ondersteunt.

Deze optie is niet beschikbaar als uw brailleleesregel uitsluitend automatische poortdetectie ondersteunt.

U kunt de documentatie voor uw brailleleesregel raadplegen in de rubriek [Ondersteunde Brailleleesregels](#SupportedBrailleDisplays) voor meer details over de ondersteunde types communicatie en beschikbare poorten.

Wilt u er opletten dat bij het tegelijkertijd aansluiten van meerdere brailleleesregels op uw systeem die hetzelfde stuurprogramma (driver) gebruiken (bijvoorbeeld als er twee Seika leesregels worden gekoppeld),
het momenteel niet mogelijk is om NVDA te laten weten welke leesregel gebruikt moet worden.
Het verdient dan ook aanbeveling slechts één leesregel van een bepaald type / fabrikant op u systeem aan te sluiten.

#### Audio {#AudioSettings}

<!-- KC:setting -->

##### Audio-instellingen openen {#OpenAudioSettings}

Toets: `NVDA+control+u`

Via het Instellingenvenster van NVDA zijn  in de rubriek Audio opties beschikbaar waarmee u allerlei aspecten van audiouitvoer kunt aanpassen.

##### Uitvoerapparaat {#SelectSynthesizerOutputDevice}

Hiermee kunt u het audioapparaat kiezen dat NVDA moet aansturen voor de spraakuitvoer.

<!-- KC:setting -->

##### Audio-onderdrukkingsmodus {#SelectSynthesizerDuckingMode}

Toets: NVDA+shift+d

Met deze optie kun je  bepalen of NVDA het volume van andere applicaties moet verlagen zodra en zolang NVDA aan het spreken is of gedurende de hele tijd dat NVDA actief is.

* Geen onderdrukking: NVDA zal het volume van andere audiobronnen niet verlagen.
* Onderdrukken bij spraak- en geluidsuitvoer: NVDA zal alleen het volume van andere audiobronnen verlagen wanneer NVDA aan het spreken is of geluiden afspeelt. Mogelijk dat dit niet bij alle synthesizers werkt.
* Altijd onderdrukken: NVDA zal het volume van andere audiobronnen steeds op een lager niveau houden zolang NVDA actief is.

Deze optie is alleen beschikbaar als u de geïnstalleerde versie van NVDA gebruikt.
audio-onderdrukking kan niet worden ondersteund bij gebruik van de draagbare en de tijdelijke versie van NVDA. 

##### Volume van NVDA-geluiden volgt stemvolume {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Uitgeschakeld, Ingeschakeld|
|---|---|
| Standaard |Uitgeschakeld|
|---|---|

Wanneer deze optie ingeschakeld is, zal het volume van   geluiden en piepjes die NVDA voortbrengt de volumeinstelling  van de stem die gebruikt wordt volgen.
Als u het volume van de stem verlaagt, zal het volume van geluiden mee naar beneden gaan.
Evenzo zal,  als u het volume van de stem verhoogt, het volume van geluiden mee omhoog gaan.
Deze optie is niet beschikbaar als u NVDA gestart hebt  terwijll [WASAPI voor audiouitvoer](#WASAPI) in Geavanceerde Instellingen UIT stond.

##### Volume van NVDA-geluiden {#SoundVolume}

Met deze schuifbalk kunt u het volume van geluiden en pieptonen van NVDA instellen.
Deze instelling werkt alleen wanneer "Volume van NVDA-geluiden volgt stemvolume" uitgeschakeld is.
Deze optie is niet beschikbaar als u NVDA gestart hebt  terwijll [WASAPI voor audiouitvoer](#WASAPI) in Geavanceerde Instellingen UIT stond.

##### Sound split (stereogeluid splitsen) {#SelectSoundSplitMode}

tereosplitsing (sound split) stelt gebruikers in staat te werken met stereo geluidsapparatuur zoals koptelefoons en speakers.
Met stereosplitsing kun je de spraak van NVDA via het ene kanaal horen (bijv llinks) en het geluid van alle overige toepassingen wordt dan afgespeeld via het andere kanaal (rechts).
Stereosplitsing staat standaard UIT.
Er is een commando waarmee je de modi voor stereosplitsing kunt doorlopen :
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Modus stereosplitsing doorlopen |`NVDA+alt+s` |Hiermee ga je van de ene naar de andere modus voor stereosplitsing.|

<!-- KC:endInclude -->

Standaard doorloop je met dit commando de volgende modi:

* stereosplitsing uitgeschakeld : NVDA past geen stereo-splitsing toe.
* NVDA via het linker en toepassingen via het rechter: spraak van NVDA komt via linker kanaal, terwijl andere toepassingen te horen zijn via het rechter kanaal.
* NVDA via het linker en toepassingen via beide kanalen: spraak van NVDA komt via linker kanaal, terwijl andere toepassingen te horen zijn zowel via het linker als rechter kanaal.

Er zijn meer geavanceerde modi voor stereosplitsing beschikbaar in het vervolgkeuzemenu instellingen van NVDA.

een van deze modi, "NVDA in beide kanalen en toepassingen in beide kanalen" zorgt ervoor dat alhet geluid naar beide kanalen wordt geleid.
Deze modus kan afwijken van de modus "stereo-splitsing uitgeschakeld" in het geval dat andere audio-bewerking interfereert met kanaalvolumes.

Merk op dat stereosplitsing (sound split) niet als mixer te gebruiken is.
Als een bepaalde toepassing bijv een stereo track afspeelt terwijl stereosplitsing is ingesteld op  "NVDA via het linker  en toepassingen via het rechter kanaal", zul je alleen het rechter kanaal van de sound track horen terwijl het linker kanaal van de sound track onderdrukt wordt.

Deze optie is niet beschikbaar  als bij het opstarten van NVDA  [WASAPI voor audiouitvoer in Geavanceerde Instellingen uitgeschakeld was](#WASAPI).

Merk op dat bij een crash van NVDA het geluidsvolume van de toepassingen niet hersteld kan worden en die toepassingen blijven mogelijk geluid via een enkel kanaall afspelen na een crash van NVDA.
Om dit te verhelpen is het het beste om NVDA opnieuw te starten en de modus "NVDA in beide kanalen en toepassingen in beide kanalen" te selecteren.

##### Stereosplitsingsmodi aanpassen {#CustomizeSoundSplitModes}

In deze lijst kun je aanvinken welke stereosplitsingsmodi opgenomen moeten zijn bij het doorlopen ervan met `NVDA+alt+s`.
Modi die niet zijn aangevinkt worden genegeerd.
Standaard zijn slechts drie modi opgenomen.

* Stereosplitsing uitgeschakeld.
* NVDA via het linker en toepassingen via rechter kanaal.
* NVDA via het linker kanaal en alle andere toepassingen via beide kanalen.

Merk op dat tenminste 1 modus moet worden geselecteerd.
Deze optie is niet beschikbaar  als bij het opstarten van NVDA  [WASAPI voor audiouitvoer in Geavanceerde Instellingen uitgeschakeld was](#WASAPI).

##### Duur van staat van paraatheid van audio-apparaat na audiouitvoer {#AudioAwakeTime}

Dit invoervak specifieert hoe lan NVDA het audioapparaat wakker  houdt, nadat de spraak stopt.
Hiermee kan NVDA voorkomen dat er haperingen en onvolkomenheden in de spraak optreden, zoals het wegvallen van delen van woorden.
Dit kan gebeuren wanneer audioapparate(n (met name Bluetooth en draadloze apparaten) in de standby modus gaan.
Dit kan ook handig zijn in andere gebruiksomstandigheden, bijv als NVDA binnen een virtuele machine wordt gedraaid, zoals (Citrix Virtual Desktop), of op bepaalde laptops.

Bij lagere waardes is de kans dat audio wordt afgekapt groter bij het te vlug overgaan van het apparaat in de standby modus waardoor het begin van het volgende spraakfragment wegvalt.
Als een te hoge waarde wordt ingesteld kan dit tot gevolg hebben dat de batterij van het afspeelapparaat sneller leeg raakt omdat het langer actief blijft zonder dat er geluid wordt afgespeeld.

Je kunt de tijd instellen op nul Als je van deze mogelijkheid geen gebruik wilt maken.

#### Zicht {#VisionSettings}

In de categorie Zicht in het dialoogvenster Instellingen van NVDA kunt u de [elementen voor visuele ondersteuning](#Vision) in- en uitschakelen, alsmede configureren.

Merk op dat de beschikbare opties in deze categorie via [NVDA add-ons](#AddonsManager) uitgebreid kunnen worden.
Standaard treft u in deze categorie instellingen  de volgende opties aan:

##### Visuele Uitlichting {#VisionSettingsFocusHighlight}

Via de selectievakjes van de groepering Visuele Uitlichting kunt u  de [Visuele Uitlichting](#VisionFocusHighlight) in NVDA beheren.

* Uitlichting activeren: Hiermee schakelt u Visuele Uitlichting in of uit.
* systeemfocus uitlichten: Hiermee kunt u bepalen of de [systeemfocus](#SystemFocus) al dan niet wordt uitgelicht.
* Navigatorobject uitlichten: Hiermee kunt u bepalen of het [navigatorobject](#ObjectNavigation) al dan niet wordt uitgelicht.
* Bladermoduscursor uitlichten: Hiermee kunt u bepalen of de [virtuele bbladermoduscursor](#BrowseMode) al dan niet wordt uitgelicht.

Merk op dat het aan- en uitvinken van het selectievakje "Uitlichten activeren" daarmee samenhangend ook de status van de andere selectievakjes wijzigt.
Daarom zullen, als 'Uitlichten activeren'UIT staat, en u dit selectievakje aanvinkt, de andere selectievakjes in de boom automatisch ook worden aangevinkt.
Als u alleen focus uitlichten wilt inschakelen en de selectievakjes voor navigatorobject en  bladermodus zonder vinkje moeten blijven, is het selectievakje "Uitlichten activeren" gedeeltelijk aangevinkt.

##### Scherm dimmen (Schermgordijn) {#VisionSettingsScreenCurtain}

U kunt [Scherm dimmen](#VisionScreenCurtain) inschakelen door een vinkje te zetten in het selectievakje "Maak scherm donker dit gebeurt meteen)".
Er verschijnt een waarschuwing dat na het inschakelen het scherm op zwart gaat.
Voordat u dit met 'ja' bevestigt, vergewist u er zich van dat spraak / braille ingeschakeld is / zijn, zodat u met uw computer kunt werken zonder het scherm te hoeven gebruiken.
Selecteer "Nee" als u wilt dat Scherm dimmen niet langer ingeschakeld is.
Als u zeker van uw zaak bent, kiest u de knop 'Ja' om het scherm te dimmen.
Als u niet langer wilt dat deze waarschuwing telkens opnieuw verschijnt, kunt u dit aanpassen in het  dialoogvenster dat deze waarschuwing toont.
U kunt te allen tijde het tonen van deze waarschuwing weer inschakelen door het selectievakje "Altijd waarschuwing tonen wanneer Scherm dimmen wordt geladen" dat u naast het vakje "Maak scherm donker" vindt.

Standaard worden bij in- of uitschakelen van Scherm dimmen geluidssignalen afgespeeld.
Als u niet wilt dat dit gebeurt, kunt u het vinkje in hetselectievakje 'Geluid afspelen bij in- / uitschakelen Scherm dimmen' weghalen.

##### Instellingen visuele ondersteuning van derden {#VisionSettingsThirdPartyVisualAids}

Elementen met optische meerwaarde kunnen via [NVDA add-ons](#AddonsManager) worden toegevoegd.
Wanneer  deze elementen aanpasbare instellingen hebben, zijn ze te vinden in de hier genoemde categorie instellingen onderverdeeld in afzonderlijke groeperingen.
Voor de ondersteunde instellingen per element kunt u de documentatie voor dat element raadplegen.

#### Toetsenbord (NVDA+control+k) {#KeyboardSettings}

<!-- KC:setting -->

##### Toetsenbordinstellingen openen {#OpenKeyboardSettings}

Toets: `NVDA+control+k`

Via de categorie Toetsenbord in het dialoogvenster Instellingen van NVDA kunt u instellen hoe NVDA moet reageren wanneer u met uw toetsenbord werkt.
In deze categorie treft u de volgende keuzemogelijkheden aan:

##### Toetsenbordindeling {#KeyboardSettingsLayout}

Dit is een vervolgkeuzelijst waarin u het type toetsenbordindeling kiest dat u wilt gebruiken. Momenteel zijn er in NVDA twee types beschikbaar: desktop en laptop. 

##### NVDA-programmatoetsen selecteren {#KeyboardSettingsModifiers}

Met de selectievakjes in deze lijst bepaalt u welke toetsen als [NVDA-programmatoetsen kunnen worden gebruikt](#TheNVDAModifierKey). U hebt de keuze uit de volgende toetsen :

* De Caps Lock-toets
* De insert-toets op het numerieke toetsenblok
* De uitgebreide insert-toets die meestal boven de pijltjestoetsen zit vlakbij home en end)

Als er geen toets als NVDA-toets wordt gekozen, zijn mogelijk veelcommando's niet beschikbaar. Daarom moet je minstens een van aangeboden opties aankruisen.  

<!-- KC:setting -->

##### Getypte karakters uitspreken {#KeyboardSettingsSpeakTypedCharacters}

Toets: NVDA+2

Door het selectievakje in te schakelen worden alle karakters die u op het toetsenbord typt uitgesproken.

<!-- KC:setting -->

##### Getypte woorden uitspreken {#KeyboardSettingsSpeakTypedWords}

Toets: NVDA+3

Door dit selectievakje in te schakelen wordt elk woord dat u getypt hebt uitgesproken.

##### Spraak onderbreken bij typen van karakters {#KeyboardSettingsSpeechInteruptForCharacters}

Als dit selectievakje is aangevinkt, wordt de spraak onderbroken telkens wanneer er een letterteken wordt getypt. Deze instelling staat standaard "aan".

##### Spraak onderbreken bij drukken van Enter-toets {#KeyboardSettingsSpeechInteruptForEnter}

Als dit selectievakje is aangevinkt, wordt de spraak onderbroken telkens wanneer de Enter-toets wordt ingedrukt. Deze instelling staat standaard "aan".

##### Doorlezen (skimmen) bij Alles Voorlezen toestaan {#KeyboardSettingsSkimReading}

Als dit selectievakje is aangevinkt,zullen navigatieopdrachten zoals snel navigeren in bladermodus of verplaatsen per regelof alinea er niet toe leiden dat Alles Voorlezen wordt gestopt, veeleer is het zo dat Alles Voorlezen naar de nieuwe positie springt waar het lezen wordt voortgezet.

##### Piep als kleine letters worden getypt terwijl CapsLock is ingeschakeld {#KeyboardSettingsBeepLowercase}

Als deze optie is geactiveerd, zal er een waarschuwingssignaal klinken bij het typen van letters in combinatie met de shift toets als Caps Lock is ingeschakeld.
Meestal is het niet de bedoeling om letters in combinatie met de shift toets te typen als Caps Lock is ingeschakeld. U heeft CapsLock dan wellicht ingeschakeld zonder dat u zich dat hebt gerealiseerd.
Daarom is het wel heel handig als u hiervoor wordt gewaarschuwd. 

<!-- KC:setting -->

##### Commandotoetsen uitspreken {#KeyboardSettingsSpeakCommandKeys}

Toets: NVDA+4

Door het selectievakje in te schakelen worden alle niet-karaktertoetsen (bij voorbeeld de pijltjestoetsen, de DEL-toets, etc.) uitgesproken. Dit geldt ook voor, bij voorbeeld, de Ctrl-toets in combinatie met een letter.

##### Geluid voor spelfouten afspelen tijdens typen {#KeyboardSettingsAlertForSpellingErrors}

Wanneer deze optie is ingeschakeld, zal er een kort zoemsignaal klinken als u een spelfout maakt in een woorrd dat u typt.
Deze optie is alleen beschikbaar indien "Spelfouten melden" is ingeschakeld in het dialoogvenster [Documentopmaakinstellingen](#DocumentFormattingSettings) dat u vindt in de dialoog Instellingen NVDA.

##### Toetsen van andere toepassingen verwerken {#KeyboardSettingsHandleKeys}

Met deze optie kan de gebruiker bepalen of invoer die afkomstig is van toepassingen zoals virtuele (scherm)toetsenborden of spraakherkenningssoftware door NVDA moet worden verwerkt.
Deze optie is standaard ingeschakeld, maar bepaalde gebruikers,zoals mensen die werken met het UniKey typeprogramma voor Viëtnamees, zullen er wellicht de voorkeur aan geven deze optie uit te zetten omdat er anders fouten bij de invoer ontstaan. 

#### Muis (NVDA+control+m) {#MouseSettings}

<!-- KC:setting -->

##### Muisinstellingen openen {#OpenMouseSettings}

Toets: `NVDA+control+m`

Via de categorie Muis in het dialoogvenster Instellingen van NVDA kunt u de muis volgen, het afspelen van pieptonen voor muiscoórdinaten en andere opties voor het gebruik van een muis instellen.
De categorie Muisinstellingen in het dialoogvenster Instellingen NVDA heeft de volgende opties:

##### Veranderingen van muisaanwijzervorm melden {#MouseSettingsShape}

Als dit selectievakje is ingeschakeld, zal NVDA elke verandering die optreedt in de vorm van de muisaanwijzer melden.
In Windows verandert de vorm van de muisaanwijzer om aan te geven waar de computer mee bezig is, zoals met het laden van iets of om te laten weten dat u tekst kunt invoeren.

<!-- KC:setting -->

##### Muis volgen {#MouseSettingsTracking}

Toets : NVDA+m |

Door het selectievakje in te schakelen wordt de tekst gelezen die zich onder de muisaanwijzer bevindt bij verplaatsing van de muis over het scherm. U kunt dus naar iets zoeken door de muis zelf te verplaatsen in plaats van zoeken met objectnavigatie.

##### Resolutie van teksteenheid {#MouseSettingsTextUnit}

Als u ervoor gekozen hebt om de tekst onder de muis te laten uitspreken, kunt u hier instellen hoeveel tekst moet worden uitgesproken.
U hebt de keuze uit karakter, woord, regel en alinea.

Om op een willekeurige plek te wisselen van resolutieniveau   moet u een aangepaste invoerhandeling toekennen via het dialoogvenster Invoerhandelingen#InputGestures].

##### Object  melden als de muis daar binnen  komt {#MouseSettingsRole}

Als dit selectievakje is ingeschakeld, zal NVDA informatie geven over objecten waarbinnen de muis zich bevindt.
Hieronder vallen de rol (type) van het object alsmede states (aangekruist/ingedrukt), celcoördinaten in tabellen, etc.
Merk op dat  het melden van bepaalde objectdetails kan afhangen van andere instellingen, bijv. zoals die in de categorie [objectweergave](#ObjectPresentationSettings) of in [Documentopmaak](#DocumentFormattingSettings).

##### Geluidscoördinaten gebruiken bij verplaatsen muis {#MouseSettingsAudio}

Als dit selectievakje is ingeschakeld laat NVDA pieptonen horen bij het verplaatsen van de muis. Met behulp van deze signalen kan de gebruiker bepalen waar de muis zich op het scherm bevindt.
Hoe verder de muis naar de bovenrand van het scherm wordt verplaatst, hoe hoger de pieptonen worden.
Bij gebruik van stereoluidsprekers of een koptelefoon zal het geluidssignaal steeds verder van links of rechts komen al naar gelang de muis naar links of rechts op het scherm wordt verplaatst. 

##### Schermhelderheid bepaalt Volume audio-coördinatie {#MouseSettingsBrightness}

Als dit selectievakje “geluidscoördinatie gebruiken bij verplaatsen muis” is ingeschakeld, dan zal het inschakelen van dit selectievakje ervoor zorgen dat het volume van de pieptonen wordt bepaald door de schermhelderheid onder de muis.
Deze functies staan standaard uit.

##### Muisinvoer van andere toepassingen negeren {#MouseSettingsHandleMouseControl}

Deze optie biedt de gebruiker de mogelijkheid muisacties (met inbegrip van muisbewegingen het klikken met muisknoppen die worden gegenereerd door andere toepassingen zoals TeamViewer en andere software waarmee pc's op afstand bestuurd worden) te negeren.
Deze optie staat standaard uit.
Als u deze optie inschakelt en als u de optie 'Muis volgen inschakelen" hebt aangevinkt zal NVDA niet melden wat er zich onder de muis bevindt als deze wordt verplaatst door een andere toepassing.

#### Aanraakinteractie {#TouchInteraction}

Met   de instellingen van deze categorie, die u  alleen aantreft op computers welke beschikken over mogelijkheden voor bediening d.m.v. aanraking, kunt u configureren hoe NVDA omgaat met aanraakschermen.
In deze categorie zijn de volgende keuzemogelijkheden beschikbaar:

##### Ondersteuning voor Aanraakinteractie inschakelen {#TouchSupportEnable}

Door dit selectievakje aan te vinken activeert u de ondersteuning voor aanraakinteractie van NVDA.
Eenmaal geactiveerd kunt u uw vingers gebruiken om over het scherm  te navigeren  en er handelingen uit te voeren met betrekking tot de daar voorkomende items, mits een apparaat met aanraakscherm wordt gebruikt.
Als deze functionaliteit uitgeschakeld is, wordt de ondersteuning voor aanraakschermen gestopt alsof NVDA niet actief is.
Met NVDA+control+alt+t kunt u deze instelling ook in- of uitschakelen.

##### Direct typen met aanraken {#TouchTypingMode}

Het al dan niet aanvinken van dit selectievakje bepaalt hoe u tekst invoert als u typt met het schermtoetsenbord.
Als het selectievakje is aangevinkt dan wordt de door u gewenste letter ingevoerd zodra u uw vinger van die letter afhaalt d.w.z. (een klein stukje optilt).
Als u geen vinkje zet, moet u dubbeltikken op de letter van uw keuze om deze in te voeren.

#### Leescursor (review cursor) {#ReviewCursorSettings}

Via de categorie Leescursor in het dialoogvenster Instellingen van NVDA kunt u configureren hoe de leescursor in NVDA reageert.
In deze categorie treft u de volgende keuzemogelijkheden aan:

<!-- KC:setting -->

##### Ssysteemfocus volgen {#ReviewCursorFollowFocus}

Toets : NVDA+7

Wanneer deze optie is ingeschakeld,wordt de leescursor (review cursor) altijd in hetzelfde object geplaatst als de systeemfocus telkens wanneer de focus zich wijzigt.

<!-- KC:setting -->

##### Systeemcursor volgen {#ReviewCursorFollowCaret}

Toets: NVDA+6

Als dit selectievakje is aangevinkt, volgt de leescursor (review cursor) automatisch de systeemcursor wanneer deze wordt verplaatst

##### Muiscursor volgen {#ReviewCursorFollowMouse}

Als dit selectievakje aangevinkt is, zal de leescursor (review cursor) de muis volgen wanneer deze wordt verplaatst.

##### Eenvoudige leesoverzichtmodus {#ReviewCursorSimple}

Als dit selectievakje aangevinkt is, zorgt NVDA ervoor dat objecten die voor de gebruiker niet van belang zijn, zoals verborgen objecten of die welke slechts een lay-out technisch doel dienen, worden uitgefilterd.

Om de eenvoudige leesoverzichtmodus vanaf een willekeurige plaats aan- of uit te zetten kunt u via het dialoogvenster [Invoerhandelingen](#InputGestures) een aangepaste handeling hiervoor aanmaken.

#### Objectweergave (NVDA+control+o) {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Objectweergaveinstellingen openen {#OpenObjectPresentationSettings}

Toets: `NVDA+control+o`

Via de categorie Objectweergave in het dialoogvenster Instellingen van NVDA kunt u instellen hoeveel informatie NVDA weergeeft met betrekking tot besturingselementen zoals een beschrijving, positie-informatie etc.
Deze opties zijn niet per definitie van toepassing op bladermodus.
Deze opties zijn eerst en vooral gericht op focusmelding en objectnavigatie van NVDA, maar niet op het lezen van tekstinhoud zoals in bladermodus.

##### Tooltips melden {#ObjectPresentationReportToolTips}

Als dit selectievakje aangevinkt is, zal NVDA eventuele flitsberichten (tooltips) laten horen wanneer deze op het scherm verschijnen.
Bij veel Windows schermen en besturingselementen verschijnt een kort berichtje, – dat “tooltip” genoemd wordt, – wanneer deze zich onder de muisaanwijzer bevinden of soms wanneer deze de focus krijgen.

##### Notificaties melden {#ObjectPresentationReportBalloons}

Als dit selectievakje aangevinkt is, zal NVDA eventuele hulpballonnen en toast meldingen weergeven wanneer deze op het scherm verschijnen.

* Hulpballonnen lijken op tooltips maar ze bevatten meer informatie dan tooltips. Ze hebben te maken met dingen die aan of met uw computer gebeuren zoals het verwijderen van een netwerk kabel of wellicht wordt u er attent op gemaakt dat er een beveiligingsprobleem is.
* Met Windows 10 zijn er zogenaamde 'toast' meldingen gekomen die in het  actiecentrum in het systeemvak te vinden zijn. Deze meldingen zijn van uiteenlopende aard  (bijv. dat er een update gedownload is, dat er een nieuw e-mailbericht  is binnengekomen, etc.).

##### Objectsneltoetsen melden {#ObjectPresentationShortcutKeys}

Als dit selectievakje is aangevinkt, zal NVDA bij de aankondiging van een bepaald object of element ook de bijbehorende sneltoetscombinatie vermelden.
Zo zal bij voorbeeld bij het onderdeel Bestand op de menubalk ook gemeld worden dat hiervoor de sneltoetscombinatie Alt + b. beschikbaar is.

##### Informatie over objectpositie melden {#ObjectPresentationPositionInfo}

Als dit selectievakje aangevinkt is, wordt de objectpositie gemeld,bijvoorbeeld 1 van 4, zodra het object focus krijgt, of zich in de objectnavigatie bevind.

==== Objectpositie raden indien deze niet beschikbaar is [ObjectPresentationGuessPositionInfo]
Als informatie van objectpositie weergeven is ingeschakeld, kan deze optie ervoor zorgen dat de positie van sommige objecten bij benadering wordt bepaald. Dit kan nodig zijn als de positie-informatie niet op een andere manier verkregen kan worden.

Als deze optie is ingeschakeld, zal positie-informatie voor meer objecten (zoals menu's en werkbalken) beschikbaar zijn, maar deze informatie is mogelijk niet geheel nauwkeurig.

##### Objectbeschrijvingen melden {#ObjectPresentationReportDescriptions}

Vink dit selectievakje niet aan als u, behalve de naam van het object, geen extra informatie hoeft te horen ( zoals zoeksuggesties, het melden van volledig dialoogvenster rechts na openen  van de dialoog). 

<!-- KC:setting -->

##### Weergave voortgangsbalk {#ObjectPresentationProgressBarOutput}

Toets : NVDA+u

Via de vervolgkeuzelijst kunt u kiezen hoe u wilt worden geïnformeerd over de voortgang van de voortgangsbalk.

U kunt kiezen uit

* uit: veranderingen in voortgangsbalken worden niet gemeld.
* uitspreken: u hoort het percentage dat aangeeft hoe ver het proces is gevorderd. Elke verandering wordt gemeld.
* Pieptonen: Bij elke verandering in de voortgangsbalk zal NVDA een pieptoon laten horen. Hoe hoger de toon, hoe verder de balk gevuld raakt.
* Uitspreken en pieptonen: U hoort zowel pieptonen als gesproken info over de voortgang van het proces.

##### Achtergrondvoortgangsbalken melden {#ObjectPresentationReportBackgroundProgressBars}

Als dit selectievakje is ingeschakeld blijft NVDA veranderingen in een voortgangsbalk weergeven, ook als deze niet langer op de voorgrond aanwezig is.
Als u een venster met een voortgangsbalk minimaliseert of naar een ander venster overschakelt, zal NVDA de veranderingen in de voortgangsbalk toch bijhouden terwijl u met iets anders bezig bent. 

<!-- KC:setting -->

##### Dynamische inhoudsveranderingen melden {#ObjectPresentationReportDynamicContent}

Toets: NVDA+5

Schakelt het automatisch melden van nieuwe inhoud aan of uit voor bepaalde besturingselementen zoals terminalvensters of chatgeschiedenis.

##### Geluid afspelen wanneer auto-aanvullen suggesties oplevert {#ObjectPresentationSuggestionSounds}

Schakelt de melding dat auto-aanvullen suggesties oplevert in of uit. Wanneer deze optie is ingeschakeld, zal NVDA een geluid afspelen om dit aan te geven. 
Auto-aanvullen levert mogelijk lijsten met suggesties op die gebaseerd zijn op de tekst die ingevoerd wordt in bepaalde velden en documenten.
Wanneer u bijvoorbeeld in het zoekvak van het startmenu van Windows Vista of latere Windows versies tekst invoert, zal er een lijst met suggesties worden getoond die gebaseerd is op wat u intypte. 
Voor bepaalde invoervelden zoals zoekvakken in verrschillende Windows 10 apps, kunt u NVDA laten melden dat er een lijst met suggesties is open gegaan tijdens het typen. 
De lijst met suggesties sluit zich wanneer u uit het invoerveld gaat. Voor sommige invoervelden kan NVDA hiervan melding maken.

#### Invoersamenstelling {#InputCompositionSettings}

Via de categorie instellingen Invoersamenstelling kunt u regelen hoe NVDA de karakters van  Aziatische talen weergeeft, wanneer u deze invoert. Dit geldt voor invoermethodes zoals IME en Text Service.
N.B. Aangezien er grote verschillen bestaan tussen de invoermethodes wat betreft mogelijkheden en de wijze van informatieoverdracht, zal het wellicht nodig zijn de instellingen aan te passen aan de gebruikte invoermethode. Hierdoor wordt typen aangenamer en gemakkelijker.

##### Automatisch alle beschikbare kandidaten melden {#InputCompositionReportAllCandidates}

Met deze keuzemogelijkheid, die standaard geactiveerd is, bepaalt u of de zichtbare kandidaten al dan niet automatisch moeten worden gemeld wanneer er een kandidatenlijst verschijnt of wanneer de pagina verandert.
Bij pictografische invoer, zoals voor Chinees Nieuw Tsjang-Dzji en Boshiami is het handig als deze keuze aangevinkt is, omdat u automatisch alle symbolen hoort met het bijbehorende nummer zodat u er direct één kunt kiezen.
Bij fonetische invoermethodes zoals Chinees Nieuw Fonetisch is het evenwel verstandiger deze optie uit te zetten omdat alle tekens hetzelfde klinken en u met de pijltoetsen door de lijst moet bladeren om uit de beschrijving van de afzonderlijke karakters de benodigde informatie te verkrijgen voor de te kiezen kandidaat.

##### Geselecteerde Kandidaat Melden {#InputCompositionAnnounceSelectedCandidate}

Met deze keuzemogelijkheid, die standaard geactiveerd is, bepaalt u of NVDA de geselecteerde kandidaat al dan niet automatisch moet melden wanneer er een kandidatenlijst verschijnt of wanneer de selectie wordt gewijzigd. 
Deze functie is nodig voor invoermethodes waarbij de selectie kan worden gewijzigd met de pijltoetsen  (zoals het Chinees Nieuw Fonetisch), maar voor andere invoermethodes is het wellicht efficiënter deze optie uit te zetten.
Merk op dat zelfs wanneer deze optie uit staat, de leescursor toch bij de geselecteerde kandidaat wordt geplaatst zodat u met gebruik van object navigatie / review deze of andere kandidaten handmatig kunt uitlezen.

##### Altijd korte beschrijving geven van kandidaat-karakters {#InputCompositionCandidateIncludesShortCharacterDescription}

Met deze keuzemogelijkheid, die standaard geactiveerd is, bepaalt u of NVDA   al dan niet een korte beschrijving moet geven van elk beoogd karakter wanneer dit wordt geselecteerd of automatisch wordt uitgelezen zodra er een kandidatenlijst verschijnt.
Merk op dat voor talen zoals het Chinees het melden van extra karakter beschrijvingen voor de geselecteerde kandidaat niet door deze optie wordt beïnvloed.
Deze optie kan nuttig zijn voor Koreaanse en Japanse invoermethodes.

##### Wijzigingen in de leesreeks melden {#InputCompositionReadingStringChanges}

Sommige invoermethodes zoals Chinees Nieuw Fonetisch en Nieuw TSjangDzjie hebben een leesreeks (soms ook wel precompositie reeks genoemd).
Met deze optie kunt u bepalen of NVDA de karakters die in de leesreeks worden ingevoerd al dan niet moet melden.
Deze optie is standaard aangevinkt.
Merk op dat sommige oudere invoermethodes zoals Chinees TsjangDzji de leesreeks mogelijk niet gebruiken om karakters voorafgaand aan de eigenlijke samenstelling in op te nemen, maar in plaats daarvan rechtstreeks gebruik maken van de samenstellingsreeks. In de optie hierna leest u hoe het rapporteren van de samenstellingsreeks kan worden ingesteld.

##### Wijzigingen in de samenstellingsreeks melden {#InputCompositionCompositionStringChanges}

Nadat de lees- of pré-compositiegegevens tot een geldig pictografisch symbool zijn gecombineerd slaan de meeste invoermethodes dit symbool, samen met andere gecombineerde symbolen, tijdelijk op in een samenstellingsreeks om tenslotte in het document te worden ingevoegd.   
Met deze optie kunt u bepalen of NVDA nieuwe symbolen die in de samenstellingsreeks verschijnen al dan niet moet melden.
Deze optie is standaard aangevinkt.

#### Bladermodus (NVDA+control+b) {#BrowseModeSettings}

<!-- KC:setting -->

##### Bladermodusinstellingen openen {#OpenBrowseModeSettings}

Toets: `NVDA+control+b`

Via de categorie Bladermodus in het dialoogvenster Instellingen van NVDA kunt u instellen hoe NVDA moet reageren bij het lezen van en het navigeren in complexe documenten zoals webpagina's.
In deze categorie zijn de volgende keuzemogelijkheden beschikbaar:

##### Maximale aantal karakters per regel {#BrowseModeSettingsMaxLength}

In het invoerveld kunt u het aantal karakters per regel instellen dat een document in bladermodus mag bevatten.

##### Aantal regels per pagina {#BrowseModeSettingsPageLines}

 Je kunt hier het maximumaantal regels invoeren dat opschuift als je Page Up (pagina omhoog) of Page Down (pagina omlaag) indrukt terwijl u zich in een document in bladermodus bevindt.

<!-- KC:setting -->

##### Schermlay-out gebruiken {#BrowseModeSettingsScreenLayout}

Toets: NVDA+v

Hiermee kunt u bepalen hoe de klikbare inhoud (links, knoppen en velden)van een document in bladermodus moet worden weergegeven. Wilt u dat de klikbare items op een aparte regel komen te staan of moet alles blijven staan zoals het wordt getoond. 
Merk op dat deze optie niet geldt voor  Microsoft Office apps zoals Outlook en Word die altijd gebruik maken  van scherm-layout.  
Wanneer  scherm-layout is ingeschakeld staan de elementen op de pagina zoals deze visueel worden weergegeven. 
Een regel waarop meerdere  links te zien zijn wordt in gesproken vorm en in braille gepresenteerd als inhoud van een en dezelfde regel. 
Als de optie uitgeschakeld is, dan komen elementen op de pagima elk op een eigen regel te staan. 
Dat kan het begrijpen ervan vergemakkelijken bij het navigeren per regel op de pagina, en kan voor sommige gebruikers de interactie met deze items gemakkelijker maken.

##### Bladermodus inschakelen bij laden van pagina {#BrowseModeSettingsEnableOnPageLoad}

Met dit selectievakje kunt u bepalen of bladermodus automatisch wordt ingeschakeld bij het laden van een pagina.
Als het selectievakje niet wordt aangevinkt,  kan bladermodus altijd nog handmatig worden geactiveerd op pagina's of in documenten die bladermodus ondersteunen.
Raadpleeg de paragraaf [Bladermodus#BrowseMode] voor een lijst van applicaties die door bladermodus ondersteund worden.
Merk op dat deze optie niet van toepassing is in situaties waar bladermodus altijd optioneel is, zoals in Microsoft Word.
Deze optie staat standaard ingeschakeld.

##### Automatisch lezen zodra pagina geladen is {#BrowseModeSettingsAutoSayAll}

Deze optie bepaalt of een pagina die geladen is in bladermodus automatisch wordt gelezen.
Deze optie is standaard ingeschakeld.

##### Lay-outtabellen opnemen {#BrowseModeSettingsIncludeLayoutTables}

Met deze optie kunt u bepalen hoe NVDA moet omgaan met tabellen die uitsluitend dienen ter ondersteuning van de layout.
Wanneer Layout-tabellen opnemen is ingeschakeld, zal NVDA zulke tabellen als normale tabellen beschouwen. Hoe ze gemeld worden is afhankelijk van de [opmaakinstellingen](#DocumentFormattingSettings) en met sneltoetscommando's kan men er naar toe navigeren.
Wanneer deze optie niet ingeschakeld is, worden de tabellen niet opgenomen en men kan er niet naar toe navigeren.
De inhoud wordt echter wel als normale tekst weergegeven.
Deze optie staat standaard uit.

Om het opnemen van layout tabellenin- en uit te kunnen schakelen vanuit elke willekeurige plaats maakt u met behulp van het [dialoogvenster Invoerhandelingen](#InputGestures) een daartoe aangepaste handeling aan.

##### Het melden van velden zoals links en koppen instellen {#BrowseModeLinksAndHeadings}

Zie de opties in de [categorie Documentopmaak](#DocumentFormattingSettings) van de dialoog [Instellingen van NVDA](#NVDASettings) om de velden in te stellen die worden uitgesproken bij het navigeren, zoals links, koppen en tabellen.

##### Automatische focusmodus bij focuswijzigingen {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Hiermee wordt de focusmodus automatisch geactiveerd bij focusveranderingen.
Als het selectievakje is ingeschakeld, zal de focusmodus automatisch worden geactiveerd wanneer u in een webpagina bij voorbeeld in een formulierveld terecht komt door op TAB te drukken.

##### Automatische focusmodus bij cursorbeweging {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Als dit selectievakje is ingeschakeld, zal NVDA de focusmodus vanzelf aanpassen bij gebruik van de pijltjestoetsen.
Als u bij voorbeeld met de pijltjestoetsen door een webpagina bladert en u in een invoerveld belandt, komt u automatisch in de focusmodus. 
Als u het invoerveld uitgaat, keert u weer terug in de bladermodus (ook wel surfmodus genoemd).

##### Geluidsmarkering voor focus- en bladermodus {#BrowseModeSettingsPassThroughAudioIndication}

Als dit selectievakje is ingeschakeld, hoort u een bepaald geluid als gewisseld wordt tussen de focus- en bladermodus in een document. Dit komt dan in de plaats van een uitgesproken wijziging van de focus.

##### Niet-commandogebonden handelingen onderscheppen voordat ze het document bereiken {#BrowseModeSettingsTrapNonCommandGestures}

Met deze optie, die standaard is ingeschakeld, kunt u bepalen of invoerhandelingen zoals toetsaanslagen die geen NVDA-commando opleveren en die niet worden beschouwd als commandotoets in het algemeen, moeten worden onderschept voordat ze het document dat op dat moment de focus heeft, bereiken.
Ervan uitgaande dat de optie is ingeschakeld zal de letter "j", bij voorbeeld, wanneer u deze indrukt, onderschept worden voordat ze het document bereikt, ook al is het geen navigatiesneltoets en waarschijnlijk ook geen commandotoets binnen de toepassing zelf. 
In een dergelijk geval geeft NVDA Windows opdracht een standaard-geluid af te spelen telkens wanneer er een onderschepte toets wordt ingedrukt. 

<!-- KC:setting -->

##### Systeemfocus automatisch op focus-gevoelige elementen plaatsen {#BrowseModeSettingsAutoFocusFocusableElements}

Toets: NVDA+8

Met deze optie die standaard uit staat, kunt u zorgen dat de systeemfocus automatisch naar elementen gaat  die de systeemfocus kunnen krijgen (links, formuliervelden, etc.) bij het navigeren door content met de bladermoduscursor.
Als u deze optie uit laat staan krijgen focus-gevoelige elementen niet automatisch de focus wanneer ze geselecteerd worden met de bladermoduscursor.
Dit kan er voor zorgen dat browsen sneller gaat en de reactiegevoeligheid verbetert in de bladermodus.
De focus zal evenwel alsnog naar een bepaald element worden verplaatst zodra er sprake is van inter-activiteit bijv.  het indrukken van een knop, het aanvinken van een selectievakje.
Het inschakelen van deze optie kan ondersteuing voor sommige websites verbeteren ten koste van de prestatie en de stabiliteit.

#### Documentopmaak (NVDA+control+d) {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Documentopmaakinstellingen openen {#OpenDocumentFormattingSettings}

Toets: `NVDA+control+d`

U kunt de meeste opties in deze categorie gebruiken om te bepalen welke informatie over de opmaak van een document u wilt horen als u de cursor in het document verplaatst.
Als u bij voorbeeld Lettertype vermelden inschakelt, wordt de naam hiervan gemeld telkens wanneer u bij een ander lettertype terecht komt.

De documentopmaakinstellingen zijn onderverdeeld in groepen. 
U kunt de vermelding laten horen van:

* Lettertype
  * Naam
  * Lettergrootte
  * Lettertype-eigenschappen
  * Superscripts en subscripts
  * Nadruk
  * Highlighted tekstmarkering (dmv uitlichting)
  * Stijl
  * Kleuren
* Documentinformatie
  Opmerkingen
  * bladwijzers
  * Aangebrachte wijzigingen in de tekst
  * Spelfouten
* Pagina's en Afstand
  * Paginanummers
  * Regelnummers
  * Regel inspringen melden [(Uit, Spraak, Tonen, Zowel Spraak als Tonen)](#DocumentFormattingSettingsLineIndentation)
  * Blanco regels negeren bij het melden van regelinspringing
  * Inspringen alinea (bij voorbeeld verkeerd om , eerste regel)
  * Regelafstand ( enkel, dubbel, etc.)
  * Uitlijning
* Tabelinformatie
  * Tabellen
  * Rij-/kolmkoppen (UITf, Rijen, kolommen, Rijen en kolommen)
  * Celcoördinaten
  * Celranden (Uit, Stijlen, Zowel kleuren als stijlen
* Elementen
  * Links
  * Koppen
  * Grafisch  
  * Lijsten
  * Blokcitaten
  * groeperingen 
  * Oriëntatiepunten
  * Artikels
  * Frames
  * Figuren en bijschriften
  * Wat klikbaar is

Als u vermelding van bovenstaande kenmerken altijd en overal wilt kunnen in- of uischakelen, kunt u daarvoor aangepaste invoerhandelingen aanmaken met behulp van [Invoerhandelingen koppelen onder Opties](#InputGestures).

##### Opmaakwijzigingen achter de cursor melden {#DocumentFormattingDetectFormatAfterCursor}

Als dit selectievakje aangevinkt is, zal NVDA proberen alle wijzigingen in de opmaak van een regel te melden bij het lezen van de regel ook als dit de prestatie vertraagt.

Standaard wordt de opmaak bij de systeemcursor / review cursor gedetecteerd, maar in bepaalde gevallen wordt ook de opmaak in de rest van de regel gedetecteerd voor zover dit geen nadelige invloed heeft op de prestatie.

Vink dit selectievakje aan bij het corrigeren van documenten in toepassingen zoals WordPad waar opmaak van belang is.

==== Regelinspringing melden ==== [DocumentFormattingSettingsLineIndentation]
Met deze optie kunt u bepalen hoe de inspringing van een regel wordt gemeld.
Het vervolgkeuzemenu voor het melden van regelinspringing heeft 4 keuzemogelijkheden.

* uit: NVDA maakt niet apart melding van inspringing.
* Spraak: Als u spraak kiest, hoort u NVDA iets zeggen als "twaalf spatie"of "vier tab" wanneer de afstand van de inspringing verandert."
* Pieptonen: Als u pieptonen kiest, wordt met behulp van tonen aangegeven in welke mate er verandering optreedt in de ingesprongen afstand.
De toonhoogte stijgtvoor elke spatie, en voor een tab, gaat de toon evenveel omhoog als voor 4 spaties.
* Zowel spraak als pieptonen: Deze optie is een combinatie van de twee hiervoor genoemde mogelijkheden.

Als u het selectievakje "Blanco regels negeren bij melden van regelinspringing" inschakelt worden veranderingen in de inspringing mbt blanco regels niet gemeld.
Dit kan handig zijn bij het lezen van een document waar blanco regels worden gebruikt om ingesprongen tekstblokken, zoals die voorkomen bij het programmeren van broncode, van elkaar te scheiden.

#### Documentnavigatie {#DocumentNavigation}

In deze categorie kunt u diverse aspecten  van  documentnavigatie aanpassen.

##### Alineastijl {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Verwerkt door applicatie), Verwerkt door applicatie, Enkelvoudig regeleinde, Meervoudige regeleinde|
|---|---|
| Standaard |Verwerkt door applicatie|
|---|---|

Met deze vervolgkeuzelijst kunt u de alineastijl selecteren die gebruikt moet worden bij alineanavigatie met `control+pijlOmhoog` en `control+pijlOmlaag`.
De beschikbare alineastijlen zijn:

* Verwerkt door toepassing: NVDA zal de toepassing de vorige en volgende alinea laten bepalen , en NVDA zal bij het navigeren de alinea lezen.
Deze stijl werkt het best wanneer de toepassing is uitgerust met ingebouwde alineanavigatie, en als deze standaard is ingesteld.
* Nieuwe regel (enkelvoudig> single line break): NVDA zal vorige of volgende alinea proberen te bepalen op basis van 'single line break' welke dient als markering van de alinea.
Deze stijl werkt het best wanneer u documenten leest in een toepassing  zonder ingebouwde ondersteuning voor alineanavigatie, en als de alinea's in het document worden aangegeven door de `enter-toets` eenmaal in te drukken.
* Meervoudige nieuwe regel(multi line break): NVDA zal vorige of volgende alinea proberen te bepalen op basis van tenminste 1 blanco regel (tweemaal drukken op de `enter-toets`)  welke dient om een alinea aan te geven.
Deze stijl werkt het best wanneer gewerkt wordt met documenten waarin blokalinea's worden gebruikt.
Merk op dat deze alineastijl niet in Microsoft Word of Microsoft Outlook, gebruikt kan worden tenzij u werkt met UIA zodat u toegang hebt tot de besturingselementen van Microsoft Word.

U kunt door de beschikbare alineastijlen bladeren  vanuit elke willekeurige plek door in het dialoogvenster [Invoerhandelingen](#InputGestures) hiervoor een toets toe te kennen.

#### Windows OCR {#Win10OcrSettings}

Aan de hand van de instellingen in deze categorie kunt u[Windows OCR](#Win10Ocr) configureren.
In deze categorie zijn de volgende keuzemogelijkheden beschikbaar:

##### Herkenningstaal {#Win10OcrSettingsRecognitionLanguage}

In het vervolgkeuzemenu kunt u de taal kiezen die voor de tekstherkenning gebruikt moet worden.
Om de lijst met beschikbare talen vanuit een willekeurige plaats te kunnen doorzoeken, kunt u via [het dialoogvenster Invoerhandelingen](#InputGestures) voor uzelf een aangepaste handeling toewijzen.

##### Periodiek herkende inhoud verversen {#Win10OcrSettingsAutoRefresh}

Wanneer dit selectievakje is geactiveerd zal NVDA de herkende inhoud automatisch verversen als een herkenningsresultaatt focus heeft.
Dit kan heel handig zijn als u steeds veranderende inhoud wilt blijven volgen, bijvoorbeeld als u een video met ondertiteling  aan het bekijken bent.
Elke anderhalve seconde wordt de tekst ververst.
Deze optie staat standaard uit.

#### Geavanceerde Instellingen {#AdvancedSettings}

Waarschuwing! De instellingen in deze categorie zijn bedoeld voor gevorderde gebruikers en als deze instellingen verkeerd worden geconfigureerd kan dit ertoe leiden dat NVDA niet correct werkt.
Breng alleen wijzigingen in deze instellingen aan als u zeker weet wat u doet of als u daartoe uitdrukkelijk opdracht hebt gekregen van een ontwikkelaar van NVDA.

##### Wijzigingen aanbrengen  in Geavanceerde Instellingen {#AdvancedSettingsMakingChanges}

Om wijzigingen in de geavanceerde instellingen te kunnen aanbrengen is het noodzakelijk dat, alvorens u hiermee begint, u door het aanvinken van het selectievakje te kennen  geeft de risico's te begrijpen die het wijzigen van deze instellingen inhoudt.

##### Teruggaan naar de standaardinstellingen {#AdvancedSettingsRestoringDefaults}

De knop herstelt de standaardwaarden voor de instellingen zelfs als het selectievakje (ter bevestiging) niet is aangevinkt.
Na wijziging van de instellingen wilt u wellicht terug naar de standaardwaarden.
Dat kan ook het geval zijn als u er niet zeker van bent of de instellingen wel gewijzigd zijn.

##### Schakel het laden van aangepaste, te testen code in, afkomstig uit ontwikkelaarskladblokmap {#AdvancedSettingsEnableScratchpad}

Bij het ontwikkelen van add-ons voor NVDA, is het nuttig dat u deze kunt testen terwijl u volop bezig bent met de ontwikkeling ervan.
Als deze optie is ingeschakeld kan NVDA aangepaste appModules, globalPlugins, brailleleesregel drivers, synthesizer drivers en ondersteuning voor verbeterd zicht, afkomstig uit  een speciale directory met codeontwikkelmappen in uwNVDA gebruikersconfiguratiemap laden.
Evenals hun tegenhangers in de vorm van add-ons worden deze modules geladen zodra NVDA  start, of, in geval van de appModules en globale Plugins, bij het herladen van plugins #ReloadPlugins].
Deze optie staat standaard uit, zodat voorkomen wordt dat er ongeteste code actief is in NVDA zonder medeweten van de gebruiker.
Als u aangepaste code aan anderen ter beschikking wilt stellen, dient dat te gebeuren in de vorm van een NVDA add-on.

##### Ontwikkelaarskladblokmap openen {#AdvancedSettingsOpenScratchpadDir}

Met deze knop opent u de directory waar u aangepaste code kunt bewaren terwijl u deze ontwikkelt.
Deze knop is eerst dan ingeschakeld als NVDA zo is ingesteld dat het laden van aangepaste code uit ontwikkelaarskladblokmap geactiveerd is.

##### Registratie betreffende gebeurtenissen en wijzigingen  in UI Automation {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Automatisch, Selectief, Globaal|
|---|---|
| Standaard |Automatisch|
|---|---|

Met deze optie kunt u bepalen hoe NVDA gebeurtenissen (events) die door de UI Automation accessibility API van Microsoft worden gegenereerd, moeten worden geregistreerd.
Het vervolgkeuzemenu registratie mbt UI Automation-gebeurtenissen en kenmerkbepalende  wijzigingen heeft drie opties:

* Automatisch: "selectief" in Windows 11 Sun Valley 2 (versie 22H2) en later, anders "globaal".
* Selectief: NVDA beperkt registratie van gebeurtenissen tot de systeemfocus voor de meeste events.
Als u te kampen hebt met prestatieproblemen bij één of meer toepassingen, raden we u aan deze functionaliteit uit te proberen om te zien of de prestaties verbeteren.
Het is echter wel mogelijk dat in oudere versies van Windows, NVDA moeite kan hebben met het volgen van de focus voor sommige besturingselementenzoals taakbeheer en emoji-paneel).
* Globaal: NVDA voert registratietaken uit voor veel UIA events die innen NVDA zelf behandeld en beëindigd worden.
Ofschoon het volgen van de focus in toenemende mate betrouwbaarder is geworden, is de prestatie nog duidelijk onder de maat in toepassingen zoals Microsoft Visual Studio.

##### UI automation gebruiken voor toegang tot besturingselementen van Microsoft Word-documenten {#MSWordUIA}

Hiermee stelt u in of NVDA al dan niet de UI (= User Interface) Automation accessibility API moet gebruiken voor  toegang tot Microsoft Word-documenten, in plaats van het oudere Microsoft Word object-model.
Dit is van toepassing op documenten in Microsoft word zelf, alsmede op berichten in Microsoft Outlook.
Deze instelling kent de volgende keuzemogelijkheden:

* Standaard (waar toepasselijk)
* Alleen voor zover nodig: daar waar  het Microsoft Word object-model in het geheel niet beschikbaar is
* Waar toepasselijk: Microsoft Word versie 16.0.15000 of hoger, of waar het Microsoft Word object-model niet beschikbaar is
* Altijd: steeds waar over  UI automation beschikt kan worden  in Microsoft word (ongeacht de mate waarin).

##### UI automation gebruiken voor toegang tot Microsoft  Excel spreadsheet-besturingselementen indien beschikbaar {#UseUiaForExcel}

Wanneer deze optie is ingeschakeld zal NVDA proberen de Microsoft UI Automation accessibility API te gebruiken om informatie op te halen uit Microsoft Excel Spreadsheet-besturingselementen.
Deze toepassing is in een experimentele fase, en sommige mogelijkheden van  Microsoft Excel zijn wellicht niet beschikbaar  in deze modus.
Zo is bijv. de Elementenlijst van NVDA voor het opsommen van formules en opmerkingen niet beschikbaar. Dit geldt ook voor de Bladermodus snelnavigatieoptie om naar formuliervelden te springen op een spreadsheet (rekenblad).
Voor zover het gaat om navigeren in / werken met spreadsheets op een meer elementair niveau kan deze  optie echter  een enorme prestatieverbetering opleveren.
Vooralsnog raden we de meeste gebruikers NIET aan dit standaard aan te zetten, al juichen we het toe dat gebruikers van Microsoft Excel  build 16.0.13522.10000  of hoger de optie activeren om uit te proberen en ons  feedback te geven over hun ervaringen.
De implementatie van Microsoft Excel's UI automation is aan voortdurende verandering onderhevig, en  versies van Microsoft Office die ouder zijn dan 16.0.13522.10000 geven mogelijk niet genoeg informatie prijs, wat deze optie vokomen onbruikbaar maakt.

##### enhanced event processing gebruiken {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Ingeschakeld), Uitgeschakeld, Ingeschakeld|
|---|---|
| Standaard |Ingeschakeld|
|---|---|

Wanneer deze optie is ingeschakeld, zou NVDA nog steeds moeten blijven reageren ook als er flinke aantallen UI Automation acties zijn, bijv. grote hoeveelheden tekst in een terminal.
Na wijziging in deze optie moet NVDA opnieuw gestart worden om de wijziging van kracht te laten worden.

##### Ondersteuning Windows Consool {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Automatisch, UIA wanneer beschikbaar, Legacy|
|---|---|
| Standaard |Automatisch|
|---|---|

Met deze instelling wordt bepaald hoe NVDA moet omgaan met de Windows-consool die door de Opdrachtprompt, PowerShell, en het Windows Subsysteem voor Linux gebruikt wordt.
Dit heeft geen invloed op de moderne Windows Terminal.
In de Windows 10-versie 1709, heeft Microsoft ondersteuning voor UI Automation API toegevoegd aan de consool https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/], bringing vastly improved performance and stability for screen readers that support it.
In situaties waar UI Automation niet beschikbaar is of als bekend is dat gebruik ervan ondermaats is, kan NVDA terugvallen op de 'legacyconsole support' optie.
Het keuzemenu waarmee ondersteuning voor de Windows-consool wordt bepaald heeft drie opties:

* Automatisch: maakt gebruik van  UI (User Interface) Automation in de versie van  de  Windows-consool die meekomt met Windows 11 versie 22H2 en later.
Deze optie wordt aanbevolen en is de standaardinstelling.
* UIA wanneer beschikbaar: maakt gebruik van UI Automation in consolen als deze beschikbaar zijn, zelfs voor versies met incomplete of gebrekkige implementatie.
Hoewel   deze beperkte functionaliteit nuttig kan zijn en alles doet wat voor u nodig is, is gebruik van deze optie volledig voor eigen risico en kan hiervoor geen ondersteuing worden geboden.
* Legacy: UI Automation in de Windows-consool staat helemaal uit.
Er wordt te allen tijde teruggevallen op legacy zelfs wanneer UI Automation tot een betere gebruikservaring zou leiden.
Daarom is de keuze voor deze optie niet aan te bevelen tenzij u weet wat u doet.

##### UI automation gebruiken bij Edge en andere op Chromium gebaseerde browsers waar beschikbaar {#ChromiumUIA}

Biedt de mogelijkheid aan te geven wanneer UIA (User Interface Automation)  gebruikt wordt, voor zover deze beschikbaar is, in op Chromium gebaseerde browsers zoals Microsoft Edge.
UIA Ondersteuning voor op Chromium gebaseerde browsers bevindt zich nog in een vroeg stadium van ontwikkeling en biedt wellicht nog niet hetzelfde toegankelijkheidsniveau als IA2.
Het keuzemenu heeft de volgende opties:

* Standaard (Alleen indien nodig: De huidige NVDA-standaardinstelling is Alleen indien nodig". Deze standaardinstelling kan met het voortschrijden van de technologie in de toekomst aangepast worden.
* Alleen indien nodig: Als NVDA niet in staat is in te breken inhet browserproces om IA2 te gebruiken en UIA beschikbaar is, dan zal NVDA terugvallen op UIA.
* Ja: Als de browser over UIA kan beschikken zal NVDA UIA gebruiken.
* Nee: UIA, niet gebruiken, zelfs niet als NVDA de toegang tot het browserproces wordt ontzegd. Dit kan nuttig zijn voor ontwikkelaars die bugs in / met IA2 proberen op te lossen en er zeker van willen zijn dat NVDA niet op UIA terugvalt.

##### annotaties {#Annotations}

Deze groep opties dient ter uitbreiding van de mogelijkheden voor experimentele   ondersteuning  van ARIA  annotaties  (ARIA = Accessible Rich Internet Applications).
Sommige van deze opties zijn mogelijk incompleet.

<!-- KC:beginInclude -->
Om een samenvatting van gelijk welke annotatie-details bij de systeemcursor te melden drukt u NVDA+d in.
<!-- KC:endInclude -->

De opties zijn:

* "Melding bevat details over samengestelde annotaties": maakt melding van verdere details mogelijk als deze beschikbaar zijn voor de tekst of het besturingselement.
-  "Altijd aria-beschrijving melden":
  Wanneer  de bron van aria-beschrijving `accDescription` is, wordt de beschrijving gemeld.
  Dit is nuttig voor annotaties op het web.
  Merk op:
  * Er bestaan veel bronnen voor `accDescription`; het komt nogal 's voor dat betekenisomschrijvingen van elkaar verschillen en onbetrouwbaar zijn.
    Door de tijd heen is AT er niet in geslaagd onderscheid te maken tussen de verschillende bronnen van `accDescription`;  vanwege de van elkaar verschillende betekenisomschrijvingen kwam er in de meeste gevallen geen spraakweergave tot stand.
  * Deze optie staat qua ontwikkeling nog in de kinderschoenen en hangt nauw samen met browser-mogelijkheden die nog niet ruim beschikbaar zijn.
  * Werkt naar verwachting met Chromium 92.0.4479.0+

##### Dynamische zones met wisselende inhoud melden {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Ingeschakeld), Uitgeschakeld, Ingeschakeld|
|---|---|
| Standaard |Ingeschakeld|
|---|---|

Met deze optie kunt u ervoor kiezen om NVDA bepaalde dynamische web-content in braille te laten melden.
Als deze optie uitgeschakeld wordt, reageert NVDA zoals  dat het geval was in versiess 2023.1 en eerder, toen alleen wijzigingen van de inhoud in gesproken vorm werden gemeld.

##### Wachtwoorden uitspreken in alle terminal-toepassingen {#AdvancedSettingsWinConsoleSpeakPasswords}

Met deze instelling kunt u bepalen of tekens in spraak worden weergegeven [via getypte tekens uitspreken](#KeyboardSettingsSpeakTypedCharacters) of [met getypte woorden uitspreken](#KeyboardSettingsSpeakTypedWords) in situaties waar het scherm niet wordt ververst, zoals bij het invoeren van wachwoorden in sommige terminal-programma's, zoals  het Windows Console wanneer ondersteuning voor UI automation ingeschakeld is alsmede Mintty.
Om veiligheidsredenen dient u deze instelling uitgeschakeld te laten.
Het kan echter voorkomen dat u hem toch wilt inschakelen, als e.e.a. niet goed werkt of er sprake is van instabiliteit m.b.t. het melden van getypte tekens  en/of woordden in consoles, of bij het werken in een vertrouwde omgeving en u de voorkeur geeft om wachtwoorden te laten uitspreken.

##### Gebruik de verbeterde  ondersteuning voor getypte karakters in het Windows-consool wanneer beschikbaar {#AdvancedSettingsKeyboardSupportInLegacy}

Met deze optie stelt u een alternatieve methode in voor het detecteren van getypte karakters in legacy opdrachtmodules van Windows.
Terwijl de prestatie hiermee verbetert en voorkomen wordt dat consool-uitvoer wordt uitgespeld, kan deze methode incompatibel zijn  met enkele terminal-programma's.
Dit alternatief is beschikbaar en staat standaard aan in Windows 10 versie 1607 en   in later uitgekomen versies van Windows 10 wanneer UI Automation niet beschikbaar is of uitgezet is.
Waarschuwing: Als deze optie is ingeschakeld, worden getypte karakters die niet op het scherm te zien zijn zoals wachtwoorden, niet onderdrukt.
In een omgeving die u niet vertrouwt kunt u [Getypte karakters uitspreken](#KeyboardSettingsSpeakTypedCharacters) en [Getypte woorden uitspreken](#KeyboardSettingsSpeakTypedWords) tijdelijk uitzetten wanneer u wachtwoorden invoert.

##### Diff algoritme {#DiffAlgo}

Deze instelling bepaalt hoe NVDA moet omgaan met de nieuwe in spraak om te zetten tekst in terminals.
Het diff algorithm keuzemenu heeft drie opties:

* Automatisch: Deze optie zorgt er voor dat NVDA in de meeste gevallen de voorkeur geeft aan Diff Match Patch maar op  Difflib terugvalt bij problematische toepassingen  zoals oudere versies van het Windows Console en Mintty.
* Diff Match Patch: Deze optie zorgt ervoor dat  NVDA wijzigingen aan de terminal-tekst per  teken berekent zelfs in situaties waar dat niet wordt aanbevolen.
Dit kan de prestatie verbeteren wanneer er grote tekstvolumes  naar het console worden weggeschreven en maakt een nauwkeurigere melding van wijzigingen midden in regels mogelijk.
In sommige toepassingen kan het (voor)lezen van nieuwe tekst echter onzorgvuldig of inconsistent verlopen.
* Difflib: Deze optie zorgt ervoor dat  NVDA wijzigingen aan terminaltekst per regel berekent, zelfs in situaties waar dit niet aanbevelenswaardig is.
Hiermee zal NVDA zich hetzelfde gedragen als  in versie 2020.4 en in daaraan voorafgaande versies.
Deze instelling kan meer stabiliteit bieden bij het lezen van nieuw in te voeren tekst in sommige toepassingen.
Wanneer er echter in terminal-toepassingen  een tekenmidden in een regel wordt ingevoerd of verwijderd wordt de tekst achter de cursor voorgelezen.

##### Nieuwe tekst in Windows Terminal via (voor)lezen {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Diffing), Diffing, UIA notificaties|
|---|---|
| Standaard |Diffing|
|---|---|

Met deze optie kiest u hoe NVDA bepaalt wat er aan nieuwe tekst is (en dus wat gelezen moet worden als "dynamische inhoudwijzigingen melden" ingeschakeld is) in Windows Terminal en de WPF Windows Terminal control die gebruikt wordt in Visual Studio 2022.
Dit is niet van invloed op de Windows-console (`conhost.exe`).
Het vervolgkeuzemenu Nieuwe tekst (voor)lezen in Windows Terminal heeft drie keuzemogelijkheden:

* Standaard: Deze mogelijkheid is momenteel hetzelfde als "diffing", maar zal naar verwachting anders worden als ondersteuning voor UIA-notificaties verder ontwikkeld wordt.
* Diffing: Deze mogelijkheid maakt gebruik van het geselecteerde diff algoritme om veranderingen te berekenen telkens wanneer de terminal nieuwe tekst aanbiedt.
Dit is identiek aan wat NVDA nu doet in versie 2022.4 en daarvoor.
* UIA-notificaties: Deze mogelijkheid draagt de verantwoordelijkheid om te bepalen wat er aan tekst moet worden (voor)gelezen over aan Windows Terminal zelf, wat inhoudt dat NVDA niet langer hoeft te bepalen wat er nieuw is in de tekst die op dat moment op het scherm staat.
Dit moet een sterke verbetering in de prestatie en van de stabiliteit opleveren van Windows Terminal, maar deze funtie is nog niet uitontwikkeld.
Met name getypte karakters die niet op het scherm worden weergegeven zoals wachtwoorden worden uitgesproken wanneer deze optie wordt geselecteerd.
Verder kan het zijn dat uitvoerclusters die uit meer dan 1,000 karakters bestaan niet accuraat worden weergegeven.

##### Probeer spraak te annuleren bij verlopen gebeurtenissen met focus {#CancelExpiredFocusSpeech}

Met deze optie kunt u ervoor zorgen dat geprobeerd wordt spraak bij verlopen gebeurtenissen met focus uitte zetten.
Met name als u snel met Chrome door berichten in Gmail gaat, doet de gesproken informatie die NVDA geeft er mogelijk niet meer toe.
Met de introductie van NVDA 2021.1 staat deze fucntionaliteit standaard ingeschakeld.

##### Reactievertraging invoercursor(in MS) {#AdvancedSettingsCaretMoveTimeout}

Met deze optie kunt u het aantal miliseconden instellen dat NVDA wacht voordat de invoercursor beschikbaar is voor het invoeren / bewerken van tekst.
Als u ervaart dat NVDA de invoercursor niet juist lijkt te volgen, hij loopt bijv. altijd 1 teken achter of herhaalt steeds regels dan kunt u eens proberen deze waarde te verhogen.

##### Transparantie van kleuren melden {#ReportTransparentColors}

Met deze optie kan men laten melden wanneer kleuren transparant zijn, wat handig is voor addon/appModuleontwikklaars die informatie verzamelen met het doel de gebruikerservaring met een applicatie van derden te verbeteren.
Enkele GDI-applicaties highlight (lichten) tekst (uit) door middel van achtergrondkleur en NVDA probeert (via display model) deze kleur te melden.
In sommige situaties, is de tekstachtergrond mogelijk volkomen transparant, waarbij de tekst een laagje vormt op een ander GUI element.
Bij verscheidene GUI API's, die al heel lang populair zijn, kan de  tekst weergegeven zijn door middel van een transparante achtergrond, maar visueel is de achtergrondkleur in orde.

##### WASAPI vor audio uitvoer gebruiken {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
| Opties |Standaard (Ingeschakeld), Uitgeschakeld, Ingeschakeld|
|---|---|
| Standaard |Ingeschakeld|
|---|---|

Met deze optie kan audiouitvoer  via Windows Audio Session API (WASAPI) ingeschakeld worden.
WASAPI is een moderner audio-framework dat potentieel betere response-eigenschappen, prestaties en stabiliteit van de NVDA audiouitvoer biedt, zowel van spraak als klank.
Na aanpassing van de optie moet u NVDA opnieuw opstarten om de aanpassing van kracht te laten worden.
Met het uitschakelen van WASAPI worden de volgende opties uitgezet:

* [Volume van NVDA-geluiden volgt stemvolume](#SoundVolumeFollowsVoice)
* [Volume van NVDA-geluiden](#SoundVolume)

##### categorieën Debug logging {#AdvancedSettingsDebugLoggingCategories}

Het selectievakje in deze lijst biedt u de mogelijkheid specifieke categorieën debug-meldingen in NVDA's log te activeren.
Het loggen van deze meldingen kan de prestatie nadelig beïnvloeden en kan grote logbestanden tot gevolg hebben.
Activeer er pas één als u daar uitdrukkelijk om gevraagd wordt door een ontwikkelaar van NVDA, bijv. bij  pogingen te achterhalen wat de oorzaak is dat de driver van een brailleleesregel niet goed werkt.

##### Een geluid afspelen voor gelogde fouten {#PlayErrorSound}

Met deze optie kunt u instellen of NVDA will een foutmeldingsgeluid afspeelt wanneer er een fout wordt gelogd.
Door te kiezen voor 'Alleen in testversies (standaard) zorgt u ervoor dat NVDA alleen foutmeldingsgeluiden afspeelt als de op dat moment gebruikte versie van NVDA een testversie is (alpha, beta of 'run from source').
Door voor 'Ja" te kiezen krijgt u foutmeldingsgeluiden te horen ongeacht welke versie van NVDA u op dat moment gebruikt.

##### Reguliere expressie voor tekstalinea sneltoetsnavigatie-commando's {#TextParagraphRegexEdit}

Dit invoerveld stelt de gebruiker in staat reguliere expressies aan te passen om daarmee tekstalinea's te vinden in bladermodus.
Het [navigatiecommando voor tekstalinea's](#TextNavigationCommand) zoekt naar tekstalinea's die overeenkomen met de criteria van de reguliere expressie.

### Diverse instellingen {#MiscSettings}

Naast het dialoogvenster Instellingen van [NVDA](#NVDASettings) kent het sub-menu Opties van het NVDA-menu nog verscheidene andere onderdelen die hierna worden voorgesteld.

#### Uitspraakwoordenboeken {#SpeechDictionaries}

Via het menu-item Uitspraakwoordenboeken dat te vinden is onder Opties kunt u aangeven hoe NVDA bepaalde woorden of woordgroepen moet uitspreken.
Op dit moment zijn er 3 soorten woordenboeken beschikbaar,
te weten, 

* Standaard woordenboek: de regels hierin hebben betrekking op alles wat in NVDA wordt uitgesproken.
* Stem-afhankelijk woordenboek: de regels hierin hebben betrekking op de in gebruik zijnde synthesizer stem.
* Tijdelijk woordenboek: de regels hierin hebben betrekking op alles wat er door NVDA wordt uitgesproken, maar dan alleen voor de huidige sessie. De gemaakte regels gaan verloren wanneer NVDA opnieuw wordt gestart.

Als u deze woordenboeken altijd en overal wilt kunnen openen, kunt u daarvoor aangepaste invoerhandelingen aanmaken met behulp van [Invoerhandelingen koppelen](#InputGestures) onder Opties.

In de dialoogvensters van de verschillende woordenboeken vindt u een lijst met regels die gebruikt worden om de uitspraak te sturen.
Tevens zijn er de knoppen Toevoegen, Bewerken, Verwijderen en Alles verwijderen.

Om een regel aan een woordenboek toe te voegen gebruikt u de knop Toevoegen. U vult de velden van het dialoogvenster in dat verschijnt en klikt op OK.
Nu zult u de nieuwe regel zien in het regeloverzicht.
Zodra u klaar bent met toevoegen of bewerken, klikt u op OK om het dialoogvenster te sluiten. Dit zorgt ervoor dat de wijzigingen worden opgeslagen.

Met de regels voor de NVDA uitspraakwoordenboeken kunt u een bepaalde karakterreeks vervangen door een andere.
Stel dat u NVDA , telkens als het woord “luid” voorkomt, het woord “hard” wilt laten zeggen.
U klikt dan op de knop Toevoegen en vult dan in het invoerveld patroon, “luid” in, en in het veld Vervangen vult u “hard” in.
Mogelijk wilt u in het commentaarveld nog een beschrijving geven van de regel, bij voorbeeld: luid wijzigen in hard. 

Met de uitspraakwoordenboeken van NVDA is veel meer mogelijk dan alleen het simpel vervangen van een woord door een ander woord.
In het dialoogvenster Toevoegen van een regel kan ook worden aangegeven of de regel hoofdlettergevoelig is. Als het selectievakje is aangevinkt, zal NVDA onderscheid maken tussen hoofdletters en kleine letters.
De standaardinstelling is dat geen verschil wordt gemaakt tussen hoofdletters en kleine letters.

Tenslotte kunt u met behulp van een aantal keuzerondjes bepalen wanneer en in hoeverre NVDA uw patroon als overeenkomst moet beschouwen; altijd ongeacht de plaats ervan binnen een woord, alleen als er sprake is van een heel woord of dat het patroon als “regular expression “ moet worden behandeld.
Als voor een patroon de voorwaarde voor overeenkomst wordt ingesteld als “heel woord”, zal vervanging ervan alleen gebeuren als het patroon GEEN deel uitmaakt van een langer woord. 
Aan deze voorwaarde wordt voldaan  indien de tekens direct voor en direct na het woord iets anders zijn dan een letter, een cijfer of een liggend streepje (underscore) of dat er helemaal geen tekens staan.
Als we uitgaan van het eerder gebruikte voorbeeld waarin “luid” werd vervangen door “hard”, dan zou er bij vervanging van een “heel woord” geen sprake van overeenkomst zijn voor harde en gehard.

Een regulieire expressie (regular expression) is een reeks waarin speciale tekens worden gebruikt om aan te geven hoe en in welke mate de reeks moet worden toegepast (op specifieke tekens, alleen getallen of alleen letters, bij voorbeeld.
In deze handleiding wordt niet verder ingegaan op reguliere expressies. 
Voor een inleidende  tutorial kunt u terecht bij  [Python's Regular Expression Guide](https://docs.python.org/3.11/howto/regex.html).

#### Uitspraak van interpunctie/symbolen {#SymbolPronunciation}

In dit dialoogvenster kan men de wijze waarop interpunctie en symbolen worden gemeld aanpassen, alsmede het interpunctieniveau waarop deze worden uitgesproken.

De taal waarop de bewerking van de uitspraak van symbolen betrekking heeft, wordt in de titelbalk van het dialoogvenster getoond.
Merk op dat voor de verwerking van symbolen en karakters in dit dialoogvenster wordt uitgegaan van de taal die als “vertrouwd” is ingesteld in de categorie [Spraak](#SpeechSettings) in het dialoogvenster [Instellingen van NVDA](#NVDASettings); dat wil zzeggen dat, wanneer deze optie is ingeschakeld, de stemtaal wordt gebruikt in plaats van de algemene taalinstelling van NVDA.

Selecteer eerst een symbool uit de symbolenlijst als u een symbool wilt aanpassen.
U kunt de symbolen filteren door het symbool of een deel van de vervanging van het symbool in te voeren  in het vak bewerken op Filter.

* In het veld "Vervangen door" kunt u de aangepaste tekst invoeren die uitgesproken moet worden in plaats van dit symbool.
* In het keuzevak Niveau kunt u het laagste niveau opgeven waarop dit symbool moet worden uitgesproken (geen, enkele, meeste of allemaal).
U kunt het niveau ook instellen op karakter; in dit geval wordt het  symbool niet gemeld, ongeacht  ingestelde symboolniveau, waarbij  de volgende twee uitzonderingen gelden:
  * Bij het  navigeren  op  karakterniveau.
  * Wanneer NVDA  tekst spelt waarin dat  symbool voorkomt.
* Het veld "Het eigenlijke symbool naar synthesizer sturen" specificeert wanneer het symbool zelf (in tegenstelling tot de vervanging ervan naar de synthesizer moet worden gestuurd.
Dit is nuttig alss het symbool de synthesizer even laat stoppen of als het de buiging van de stem verandert.
Een komma, bij voorbeeld, zorgt ervoor dat er een kort pauzemoment is in de spraakuitvoer
Er zijn drie opties:
  * nooit: Nooit het eigenlijke symbool naar de synthesizer sturen.
  * altijd: Altijd het eigenlijke symbool naar de synthesizer sturen.
  * Alleen onder symboolniveau: Het eigenlijke symbool alleen sturen als het ingesteldespraaksymboolniveau lager is dan het voor dit symbool opgegeven niveau. 
  U kunt deze optie bij voorbeeld gebruiken om ervoor te zorgen dat een symbool wordt uitgesproken met de vervangende vorm voor de hogere niveaus zonder dat er pauzes optreden terwijl op de lagere niveaus steeds een pauze wordt aangegeven.

U kunt nieuwe symbolen toevoegen door op de knop toevoegen te drukken
In het dialoogvenster dat verschijnt voert u het symbool in en vervolgens drukt u op de OK-knop. 
Pas daarna de velden aan voor het nieuwe symbool zoals u dat voor andere symbolen zou doen.

U kunt een eerder ingevoerd symbool verwijderen door op de knop Verwijderen te drukken.

Als u klaar bent, drukt u op Ok om de wijzigingen op te slaan of op Annuleren om deze niet door te voeren.

In geval van complexe symbolen kan het nodig zijn in het veld 'Vervangen door' bepaalde samengestelde verwijzingen van de gematchte tekst op te nemen. Voor een patroon dat overeenkomt met een complete datum, bij voorbeeld, zou \1, \2, en \3 in het veld moeten komen te staan,  om er voor te zorgen dat een juiste vervanging door de corresponderende delen van de datum plaats vindt.
In het veld 'Vervangen door' moeten normale (enkelvoudige) backslashes derhalve worden verdubbeld,u moet bijv.  "a\\b" typen om "a\b" als vervanging te krijgen.

#### Invoerhandelingen {#InputGestures}

In dit dialoogvenster kunt u toetsen voor invoerhandelingen op het toetsenbord, knoppen op de brailleleesregel, etc. instellen voor het uitvoeren van NVDA commando's.

Alleen commando's die toepasbaar zijn vlak voordat u het dialoogvenster opent, worden getoond.
Als u bij voorbeeld commando's wilt instellen die te maken hebben met bladermodus, dan moet u het dialoogvenster Invoerhandelingen openen,wanneer u zich in de bladermodus bevindt.

De boomstructuur in dit dialoogvenster toont alle beschikbare NVDA commando's die per categorie gegroepeerd zijn.
U kunt ze filteren door een of meer woorden van de commandonaam in willekeurige volgorde in te voeren in het bewerkingsvak “Filteren op”.
Onder elk commando treft u de ermee verbonden handeling aan.

Om een invoerhandeling aan een commando toe te voegen selecteert u het commando en drukt u op de knop Toevoegen.
Voer vervolgens de gewenste invoerhandeling uit; bij voorbeeld door het indrukken van een toets op het toetsenbord of een knop op een brailleleesregel.
Vaak kan de reikwijdte van een invoerhandeling verschillen.
Als u bij voorbeeld een toets op het toetsenbord indrukt,wilt u mogelijk dat dit specifiek voor de huidige toetsenbordindeling geldt (d.w.z. desktop of laptop) of mogelijk wilt u dat dit voor beide geldt.
Desgewenst kunt u via een menu de relevante optie instellen.

Om de aan een commando verbonden invoerhandeling ongedaan te maken, selecteert u de invoerhandeling en drukt u op de knop Ongedaan maken.

De categorie Geëmuleerde systeemtoetsenbordtoetsen bevat NVDA commando's welke toetsen op het systeemtoetsenbord emuleren.
Deze geëmuleerde systeemtoetsenbordtoetsen kunnen gebruikt worden om een systeemtoetsenbord rechtstreeks vanaf uw brailleleesregel te bedienen.
Om  een geëmuleerde invoerhandeling toe te voegen selecteert  u de categorie Geëmuleerde systeemtoetsenbortoetsen  en drukt  u op the knop Toevoegen.
Druk vervolgens op de toets van het toetsenbord die u wilt emuleren.
Hierna is de toets beschikbaar via de categorie Geëmuleerde systeemtoetsenbortoetsen  en kunt u er een invoerhandeling aan toekennen zoals hierboven beschreven.

Merk op:

* Aan geëmuleerde toetsen moeten handelingen zijn toegewezen om ze van kracht telaten blijven wanneer het dialoogvenster wordt opgeslagen / gesloten.
* Een invoerhandeling met  zogenaamde 'modifier'-toetsen kan mogelijk niet ingesteld (mapped) worden als geëmuleerde invoerhandeling zonder 'modifier' toetsen.
Het instellen van de geëmuleerde invoer `a` bij voorbeeld en het configureren van een ivoerhandeling `ctrl+m`, kan tot gevolg hebben dat de toepassing `ctrl+a` krijgt.

Als u klaar bent met het aanbrengen van de wijzigingen drukt u op de knop OK om de wijzigingen op te slaan of op de knop Annuleren als u geen wijzigingen wilt doorvoeren.

### De configuratie opslaan en opnieuw laden {#SavingAndReloading}

Als er wijzigingen worden aangebracht in de instellingen van NVDA worden deze automatisch opgeslagen bij het afsluiten van het programma.
Dit is de standaardinstelling, maar u kunt dit veranderen onder Algemeen in het menu Opties.
U kunt gewijzigde instellingen te allen tijde handmatig opslaan. Hiervoor gaat u in het NVDA-menu naar Configuratie opslaan.

Als het nodig is om terug te gaan naar een eerder opgeslagen configuratie, bij voorbeeld omdat u een vergissing hebt gemaakt bij het veranderen van de instellingen, kiest u in het NVDA-menu Terug naar opgeslagen configuratie.
U kunt de configuratie van NVDA ook terugzetten naar de oorspronkelijke instellingen door in het NVDA-menu “Zet NVDA terug naar fabrieksinstellingen" te kiezen.

De volgende toetscombinaties kunnen ook handig zijn:
<!-- KC:beginInclude -->

| Naam |Desktoptoets |Laptoptoets |Beschrijving|
|---|---|---|---|
|Configuratie opslaan |NVDA+control+c |NVDA+control+c |Hiermee worden de huidige instellingen opgeslagen zodat deze niet verloren gaan als NVDA wordt afgesloten.|
|Configuratie terugzetten |NVDA+control+r |NVDA+control+r |Door eenmaal drukken worden de instellingen hersteld zoals deze waren toen u de configuratie de laatste keer hebt opgeslagen. Bij driemaal drukken worden de fabrieksinstellingen hersteld.|

<!-- KC:endInclude -->

### Configuratieprofielen {#ConfigurationProfiles}

Het kan voorkomen dat u bepaalde instellingen wilt die gelden voor bepaalde situaties.
Zo kan het zijn dat u wilt dat "inspringen melden" aan staat als u een tekst aan het bewerken bent, of dat het melden van opmaakeigenschappen zoals lettertype, grootte, etc. is ingeschakeld als u tekst naleest ter correctie.
Dit kunt u in NVDA doen met behulp van configuratieprofielen.

Een configuratieprofiel bevat uitsluitend de instellingen die gewijzigd worden bij het bewerken van het profiel.
De meeste instellingen kunnen in een configuratieprofiel worden aangepast behalve waar het gaat om instellingen die gelden voor NVDA in zijn geheel. Deze vindt u in de categorie Algemeen van het dialoogvenster [Instellingen van NVDA](#NVDASettings).

U kunt Configuratieprofielen handmatig activeren, hetzij via een dialoog dan wel door persoonlijke, toegevoegde invoerhandelingen.
Ze kunnen ook automatisch geactiveerd "worden met behulp van een zogenaamde "trigger". Het overschakelen naar een applicatie, bij voorbeeld, kan de "trigger" zijn die een bepaald configuratieprofiel activeert.

#### Basisbeheer {#ProfilesBasicManagement}

U kunt configuratieprofielen beheren door in het NVDA-menu Configuratieprofielen te selecteren.
U kunt hiervoor ook de volgende toetscombinatie gebruiken:
<!-- KC:beginInclude -->

* NVDA+control+p: Het dialoogvenster Configuratieprofielen weergeven.

<!-- KC:endInclude -->

Het eerste element in dit dialoogvenster is de profiellijst waaruit u een van de beschikbare profielen kunt selecteren.
Bij het openen van het dialoogvenster wordt het profiel dat u aan het bewerken bent, geselecteerd.
Verder wordt van de actieve profielen aangegeven of ze handmatig, of automatisch (via trigger), worden aangezet en / of dat ze in bewerking zijn.

U kunt een profiel hernoemen of verwijderen door respectievelijk op de knop "Hernoemen" of "Verwijderen" te drukken.

U sluit het dialoogvenster met de knop "Sluiten".

#### Een Profiel aanmaken {#ProfilesCreating}

U kunt een profiel aanmaken door op de knop "Nieuw" te drukken.

In het dialoogvenster Nieuw Profiel, kunt u een naam voor het profiel opgeven.
Hier selecteert u ook hoe dit profiel gebruikt moet worden.
Als u het profiel uitsluitend handmatig wilt gebruiken, selecteert u "handmatigactiveren", wat de standaardinstelling is.
In het andere geval selecteert u een trigger die dit profiel automatisch moet activeren.
Als u geen naam voor het profiel hebt ingevoerd, zal gemakshalve bij het selecteren van een trigger de ermee verbonden naam worden overgenomen.
[Verderop](#ConfigProfileTriggers) leest u meer informatie over triggers.

Door op OK te drukken wordt het profiel aangemaakt en het dialoogvenster gesloten. Vervolgens kunt u het profiel bewerken.

#### Handmatig activeren {#ConfigProfileManual}

U kunt een profiel handmatig activeren door een profiel te selecteren en dan op de knop Handmatig Activeren te drukken
Naast een handmatig geactiveerd profiel blijft het mogelijk met behulp van triggers andere profielen aan te zetten, maar de instellingen van een handmatig geactiveerd profiel krijgen prioriteit ten koste van de automatische instellingen. 
Als er bij voorbeeld voor de huidige toepassing een profiel automatisch (via een trigger)is geactiveerd en als in dat profiel het melden van links is ingeschakeld terwijl in het handmatig geactiveerde profiel dit niet is gebeurd, dan worden links niet gemeld. 
Als u echter de stem in het via een trigger geactiveerde profiel hebt veranderd, maar als u die niet gewijzigd hebt in het handmatig geactiveerde profiel, dan zal de stem uit het automatisch (via trigger) geactiveerde profiel worden gebruikt. 
Instellingen die u wijzigt worden opgeslagen in het handmatig geactiveerde profiel.
U kunt een dergelijk profiel déactiveren door het te selecteren en op de knop "Handmatig déactiveren" te drukken.

#### Triggers {#ConfigProfileTriggers}

Door in het dialoogvenster Configuratieprofielen op de knop Triggers te drukken, kunt u instellen welke profielen met behulp van de verschillende triggers automatisch geactiveerd moeten worden.

In de lijst staan de volgende beschikbare Triggers: 

* Huidige toepassing: wordt ingeschakeld wanneer u de toepassing start.
* Alles voorlezen : wordt geactiveerd bij gebruik van het commando Alles voorlezen.

Om het profiel te wijzigen dat automatisch moet worden geactiveerd voor een bepaalde triggerselecteert u eerst de trigger en vervolgens het gewenste profiel in de lijst met profielen. 
Als u niet wilt dat er een profiel wordt gebruikt, selecteert u "(normale configuratie)".

Druk op de knop Sluiten om naar het dialoogvenster Configuratieprofielen terug te gaan.

#### Een Profiel bewerken {#ConfigProfileEditing}

Als u handmatig een profiel hebt geactiveerd, worden alle door u gewijzigde instellingen in dat profiel opgeslagen.
Als dat niet het geval is,zullen wijzigingen die u in de instellingen aanbrengt worden opgeslagen in het meest recente door een trigger geactiveerde profiel.
Als u bij voorbeeld een profiel gekoppeld hebt aan de toepassing Kladblok, dan zullen, zodra u naar Kladblok overschakelt, gewijzigde instellingen naar dat profiel worden opgeslagen.
Als er geen handmatig geactiveerd profiel is, en er ook geen sprake is van een automatisch geactiveerd profiel dan worden gewijzigde instellingen opgeslagen in de normale configuratie. 

Om het profiel dat gekoppeld is aan alles voorlezen te bewerken, moet u dat profiel [handmatig activeren](#ConfigProfileManual). 

#### Triggers tijdelijk uitschakelen {#ConfigProfileDisablingTriggers}

Het kan van pas komen dat alle triggers tijdelijk kunnen worden uitgeschakeld. 
U wilt bij voorbeeld een handmatig geactiveerd profiel of de normale configuratie bewerken zonder last te hebben van door triggers geactiveerde profielen 
Dit kunt u doen door een vinkje te zetten in het selectievakje bij "Alle triggers tijdelijk uitschakelen" in het dialoogvenster Configuratieprofielen.

Om vanaf een willekeurige plaats Triggers in of uit te schakelen wijst u een aangepaste invoerhandeling toe met behulp van het dialoogvenster [Invoerhandelingen](#InputGestures).

#### Een profiel activeren met behulp van invoerhandelingen {#ConfigProfileGestures}

Aan elk profiel dat u toevoegt, kunt u een of meer invoerhandelingen toekennen om het te  activeren.
Standaard zijn aan configuratieprofielen geen invoerhandelingen toegekend.
U kunt  handelingen toevoegen om een profiel te activeren  met behulp van het dialoogvenster Invoerhandelingen #InputGestures].
Elk profiel heeft een eigen aanduiding in de categorie configuratieprofielen.
Wanneer  u een  profiel hernoemt, blijven alle handelingen die u eerder bewerkte beschikbaar.
Met het verwijderen van een profiel worden de daaraan verbonden handelingen ook verwijderd.

### De Locatie van Configuratiebestanden {#LocationOfConfigurationFiles}

Als u een draagbare versie van NVDA hebt, worden alle instellingen en add-ons opgeslagen in een sub-map genaamd user config. Deze map bevindt zich in de NVDA hoofdmap.

Als u NVDA op een laptop of pc hebt geïnstalleerd, worden alle instellingen en add-ons opgeslagen in een aparte map die te vinden is in de map van de aangemelde gebruiker onder de Windows gebruikersprofielen.
Dit betekent dat elke gebruiker met de door hem- of haarzelf ingestelde configuratie van NVDA kan werken.
Om de hoofdmap met instellingen van een willekeurige plaats te openen gebruikt u het dialoogvenster Invoerhandelingen #InputGestures] om zo een aangepaste invoerhandeling toe te voegen.
Ook kunt u in geval van een geïnstalleerde versie van NVDA via menu start naar programma's -> NVDA -> de map gebruikersconfiguratie verkennen.

De NVDA-instellingen voor aanmeldingsscherm en UAC-schermen zijn opgeslagen in de systemConfig-map die zich in de hoofdmap van de NVDA-installatie bevindt.
In het algemeen moet u niets veranderen aan deze configuratie.
Om de instellingen van NVDA voor het aanmeldscherm of de UAC-schermen (gebruikersaccountbeheer) aan te passen, brengt u de gewenste wijzigingen aan terwijl u bij Windows bent aangemeld. Vervolgens slaat u de configuratie op waarna u in de categorie Algemeen van het dialoogvenster [Instellingen van NVDA](#NVDASettings) op de knop "Huidige Instellingen van NVDA gebruiken bij Windows-aanmelding", drukt.

## Add-ons en de Add-on Store {#AddonsManager}

Add-ons zijn software-pakketten die nieuwe of aanvullende functionaliteit bieden voor NVDA.
Ze worden ontwikkeld door mensen uit de NVDA-gemeenschap en  externe organisaties zoals commerciële partijen.
Add-ons bieden een breed scala aan mogelijkheden:

* Voegenondersteuning aan bepaalde toepassingen toe of vergroten die.
* Bieden ondersteuning voor extra Brailleleesregels of spraak-synthesizers.
* Voegen opties aan NVDA toe of wijzigen deze.

In de Add-on-store van NVDA kunt u naar add-ons zoeken en deze beheren.
Alle in de Add-on-store beschikbare add-ons kunnen gratis worden gedownload.
Er zijn er echter enkele waarvoor een betaalde licentie of aanvullende software nodig is voordat ze gebruikt kunnen worden.
Commerciële spraaksynthesizers zijn hiervan een voorbeeld.
Als u een add-on installeert   waaraan een prijskaartje hangt en u van verder gebruik afziet kunt u de add-on gemakkelijk verwijderen.

U komt bij de Add-on-store via Extra, een submenu van het  NVDA-menu.
Om de Add-on-store vanuit een willekeurige plaats te bereiken kunt u een eigen invoerhandeling aan maken via het dialoogvenster [Input Gestures](#InputGestures).

### Zoeken in add-ons {#AddonStoreBrowsing}

Wanneer de Add-on-store eenmaal geopend is, ziet u de lijst met add-ons.
Als u eerder geen add-on hebt geïnstalleerd  komt u in de Add-on Store terecht bij een lijst met  add-ons die voor installatie beschikbaar zijn.
Als u al eerder add-ons hebt geïnstalleerd, wordt de lijst met de momenteel geïnstalleerde add-ons getoond.

Als u een add-on, selecteert door er naar toe te gaan met de pijltjestoetsen omhoog en omlaag, ziet u de details voor de add-on.
Op Add-ons kunnen bepaalde handelingen worden toegepast die u [via een actiemenu uitvoert](#AddonStoreActions), zoals installeren, help, uitschakelen, en verwijderen.
Welke acties beschikbaar zijn is afhankelijk van het wel of niet geïnstalleerd zijn  van de add-on in kwestie , en in- of uitgeschakeld zijn.

#### Gesorteerde Add-on-lijsten {#AddonStoreFilterStatus}

De lijst met Add-ons kan op verschillende manieren worden gesorteerd, te weten, geïnstalleerde, bij te werken, beschikbare en incompatibele add-ons.
Om de voorliggende weergave van de Add-onlijst te wijzigen moet u het actieve tabblad aanpassen met  `ctrl+tab`.
U kunt ook naar de weergaveoverzichtslijst tabben en er doorheen lopen met de `linkerPijl` en `rechterPijl`.

#### Sorteren op in- of uitgeschakelde add-ons {#AddonStoreFilterEnabled}

Normaal gesproken, is een  geïnstalleerde add-on ingeschakeld wat inhoudt dat deze binnen NVDA actief en beschikbaar is.
Het is echter wel mogelijk dat enkele geïnstalleerde add-ons op 'uitgeschakeld'staan.
Dit houdt in dat ze niet in gebruik zijn en dat de functie ervan niet beschikbaar is tijdens de NVDA-sessie van het moment.
Het kan zijn dat u een add-on hebt uitgeschakeld omdat de werking ervan werd verstoord door een andere add-on, of door een of andere toepassing.
NVDA kan bepaalde add-ons, ook uitschakelen als blijkt dat ze incompatibel zijn tijdens een NVDA-upgrade; hiervoor wordt u echter wel gewaarschuwd als dit het geval is.
Add-ons kunnen ook worden uitgeschakeld als u ze eenvoudigweg gedurende langere tijd niet nodig hebt, maar u ze niet wilt deïnstalleren omdat u verwacht er in de toekomst weer gebruik van te gaan maken.

De lijsten met  geïnstalleerde en incompatibele add-ons kunnen op basis van de status íngeschakeld' of 'uitgeschakeld' worden gesorteerd.
Standaard worden zowel ingeschakelde als uitgeschakelde add-ons getoond.

#### Incompatibele add-ons insluiten {#AddonStoreFilterIncompatible}

Beschikbare en bij te werken add-ons kunnen worden gesorteerd met insluiting van[[incompatibele add-ons](#incompatibleAddonsManager) die voor installatie beschikbaar zijn.

#### Add-ons sorteren op basis van kanaal {#AddonStoreFilterChannel}

Add-ons kunnen via maximaal vier kanalen worden uitgezet:

* Stabiel: de ontwikkelaar heeft deze add-on uitgebracht  als geteste add-on in combinatie met een uitgebrachte versie van NVDA.
* Beta: deze add-on moet nog verder uitgeprobeerd worden, maar wordt uitgebracht om feedback van gebruikers te krijgen.
Gericht op  'early adopters'.
* Dev: dit kanaal richt zich op en is bedoeld voor ontwikkelaars van add-ons om nog niet uitgebrachte API-aanpassingen uit te testen.
Alpha testers van NVDA moeten mogelijk een  "Dev" versie van hun add-ons gebruiken.
* Extern: Add-ons van externe bronnen die van buiten de Add-on Store worden geïnstalleerd.

Om add-ons te sorteren uitsluitend op basis van een specifiek kanaal kunt u het selectiefilter aanpassen.

#### Zoeken naar add-ons {#AddonStoreFilterSearch}

Om add-ons, te zoeken gebruikt u het invoervak 'zoeken'.
U komt bij het zoekvak door op `shift+tab` te drukken vanuit de lijst met add-ons.
Typ een paar sleutelwoorden voor het soort add-on waar u naar op zoek bent waarna u naar de lijst met add-ons `tabt`.
Er verschijnt een lijst met gevonden add-ons als de opgegeven zoektermen overeenkomen met de add-on ID, de weergegeven naam, uitgever of de beschrijving.

### Add-on-acties {#AddonStoreActions}

Add-ons kennen bijbehorende acties, zoals installeren, help, uitschakelen, en verwijderen.
Hetmenu voor acties  mbt een add-on in de lijst met add-ons kan worden bereikt  door op de `Toepassingstoets te drukken, ``enter`  in te drukken, rechts te klikken of dubbel te klikken op de add-on.
Dit menu is ook te bereiken   in het geselecteerde  deelvenster details van een add-on.

#### Add-ons installeren {#AddonStoreInstalling}

Louter en alleen omdat een add-on beschikbaar is in de Add-on Store, mag hier niet uit worden opgemaakt deze goedgekeurd of gecontroleerd is door  NV Access of door wie dan ook.
Het is erg belangrijk dat u alleen add-ons installeert  die afkomstig zijn van bronnen die u vertrouwt.
Binnen NVDA gelden er geen beperkingen mbt de functionaliteit van  add-ons.
Dit zou ook kunnen gelden voor toegang tot uw persoonlijke gegevens of zelfs het gehele systeem.

U kunt add-ons installeren  en updaten [door te [zoeken in beschikbare add-ons](#AddonStoreBrowsing).
Selecteer een add-on uit de beschikbare add-ons" of uit de bij te werken  add-ons" tab.
Kies daarna de actie  bijwerken, installeren, of vervangen om het installatieproces te starten.

Je kunt ook meerdere add-ons tegelijk installeren.
Dit doe je door meerdere add-ons te selecteren op het tabblad beschikbare add-ons , vervolgens  het contextmenu te activeren bij de selectie en dan kies je "geselecteerde add-ons installeren" action.

Om een add-on te installeren  die niet uit de Add-on-store afkomstig is, drukt u op de knop "Installeren  vanuit  de externe bron".
Hiermee kunt u een add-on-pakket (`.nvda-addon` install ) opzoeken ergens op uw computer of op een netwerk.
Met het openen van het add-on-pakket begint het installatieproces.

Als  NVDA op uw systeem is geïnstalleerd en actief is, kunt u een add-on-bestand ook rechtstreeks vanuit de browser of het bestandssysteem openen om met het installatieproces te beginnen.

Wanneer een  add-on wordt geïnstalleerd uit een externe bron zal NVDA u vragen de  installatie te bevestigen.
Als de add-on eenmaal is geïnstalleerd, moet NVDA opnieuw gestart worden om de add-on in werking te stellen, al kunt u de herstart van NVDA wel even opschorten als u nog andere add-ons wilt installeren of bijwerken.

#### Add-ons verwijderen {#AddonStoreRemoving}

Om een add-on, te verwijderen selecteert u  de add-on in de lijst en voert u de actie Verwijderen uit.
NVDA zal u vragen de verwijderactie te bevestigen.
Evenals bij het installeren moet NVDA opnieuw gestart worden om de verwijdering van de add-on te voltooien.
Totdat de herstart is uitgevoerd,  wordt die add-on in de lijst aangemerkt als  "In afwachting van verwijdering".
Zoals  bij installeren, kun je ook meerdere  add-ons tegelijk verwijderen.

#### Add-ons in- en uitschakelen {#AddonStoreDisablingEnabling}

Om een add-on uit te schakelen voert u de actie "uitschakelen" uit.
Om een eerder uitgeschakelde  add-on, in te schakelen voert u de actie "inschakelen" uit.
U kunt een add-on uitschakelen als de status van de add-on  aangeeft dat deze 'ingeschakeld" is, of als de status 'inschakelen' is in het geval dat de add-on "uitgeschakeld" is.
Bij de actie in- of uitschakelen geldt steeds  dat de wijziging in de status van de add-on pas in werking treedt na herstart van NVDA.
Als de add-on eerder was "uitgeschakeld", geeft de statusindicatie "ingeschakeld' aan na een herstart".
Als de add-on eerder was "ingeschakeld", geeft de statusindicatie "uitgeschakeld' aan na een herstart".
Evenals bij het installeren  of verwijderen van add-ons, moet NVDA opnieuw gestart worden om de wijzigingen van kracht te laten worden.
Je kunt ook meerdere  add-ons tegelijk in- of uitschakelen  door deze te selecteren op het tabblad  beschikbare add-ons, vervolgens activeer je het contextmenu bij de selectie en kies je de desbetreffende actie.

#### Add-ons beoordelen en reviews lezen {#AddonStoreReviews}

Wellicht wil je reviews van andere gebruikers lezen die ervaring hebben met een add-on, voordat je die installeert bijvoorbeeld, of als je bezig bent die te leren gebruiken.
Ook kan het nuttig voor andere gebruikers zijn als je feedback geeft over add-ons die je hebt uitgeprobeerd.
Om reviews over een add-on, te lezen selecteer je een add-on uit de tab  van Beschikbare of Bij te werken add-ons en gebruik je de "Community reviews" action.
Dit is een link naar een GitHub Discussiewebpagina, waar je reviews kunt lezen en schrijven over de add-on.
Bedenk wel dat dit niet hetzelfde is als rechtstreeks contact hebben met  ontwikkelaars van add-ons.
Het doel vanreviews is eerder het delen van feedback om gebruikers te helpen te bepalen of een add-on voor hen wel of niet geschikt is.

### Incompatibele Add-ons {#incompatibleAddonsManager}

Sommige oudere add-ons zijn mogelijk niet langer compatibel met de versie van NVDA die u hebt.
Als u een oudere versie van NVDA gebruikt, zijn sommige nieuwere add-ons wellicht ook niet meer compatibel.
Als u probeert een incompatibele add-on te installeren krijgt u een foutmelding waarin wordt uitgelegd waarom de add-on als incompatibel beschouwd moet worden.

Met betrekking tot  oudere add-ons, kunt u, op eigen risico, ertoe overgaan de incompatibiliteit als niet terzake af te doen.
Incompatibele add-ons werken mogelijk niet  samen met uw versie van NVDA, en kunnen onstabiele en onverwachte gedragingen gaan vertonen, of zelfs crashen.
U kunt  de compatibiliteitskwestie  negeren wanneer u een add-on inschakelt of installeert.
Als de incompatibele add-on later, problemen veroorzaakt kunt u deze uitschakelen of verwijderen.

Als u problemen ondervindt bij het gebruik van NVDA, en u recent  een add-on, hebt bijgewerkt of geïnstalleerd, vooral als het een incompatibele add-on betreft, kunt u wellicht proberen NVDA tijdelijk te draaien terwijl u alle add-ons hebt uitgeschakeld.
Om NVDA op te starten zonder ingeschakelde add-ons kiest u de hiervoor bestemde optie bij het afsluiten van NVDA.
Een andere mogelijk heid is om de [commandoregel](#CommandLineOptions) `--disable-addons` te gebruiken.

U kunt door beschikbare incompatibele add-ons bladeren met behulp van de tabbladen [beschikbare en bij te werken add-ons](#AddonStoreFilterStatus).
U kunt door geïnstalleerde incompatibile add-ons bladeren met behulp van  de [tab incompatibele add-ons](#AddonStoreFilterStatus).

## Het menu Extra {#ExtraTools}
### Logboek weergeven {#LogViewer}

Door Logboek weergeven te kiezen in het NVDA-menu onder Extra kunt u alles bekijken wat er in het logboek is vastgelegd sinds de laatste sessie die in NVDA werd gestart.

Je kunt niet alleen de inhoud van het logbestand lezen, maar er ook een kopie van opslaan of de inhoud van het scherm vernieuwen zodat ook de gegevens worden getoond die werden vastgelegd na openen van het logbestand.
Dit kun je doen via het Log-menu  in het logweergave-venster.

Het bestand dat wordt getoond wanneer je het logweergave-venster opent, wordt op je computer bewaard en wel op volgende bestandslocatie `%temp%\nvda.log`.
Telkens wanneer je je computer start, wordt er een nieuw logbestand aangemaakt.
Wanneer  dit gebeurt, wordt het in de vorige sessie van NVDA aangemaakte logbestand verplaatst naar `%temp%\nvda-old.log`.

Je kunt ook een gedeelte van het huidige logbestand naar het klembord kopiëren zonder het logweergavevenster te openen.
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Logweergavevenster openen |`NVDA+f1` |Opent logweergavevenster en toont ontwikkelaarsinformatie mbt het huidige navigatorobject.|
|Een gedeelte van het log naar het klembord kopiëren |`NVDA+control+shift+f1` |Bij eenmaal drukken van deze toetscombinatie wordt het beginpunt  van het te kopiëren loggedeelte gemarkeerd. Door nogmaals deze toetscombinatie te drukken, wordt de loginhoud vanaf het gemarkeerde beginpunt tot waar de 2de keer wordt gedrukt, naar het klembord gekopieerd|

<!-- KC:endInclude -->

### Spraakweergavevenster (schermweergave gesproken tekst) {#SpeechViewer}

Voor goedziende softwareontwikkelaars of mensen die NVDA demonstreren voor een goedziend publiek is er een zwevend kader waarin alles op het scherm wordt getoond wat NVDA bezig is voor te lezen.

Om het spraakweergavevenster in te schakelen zet u een vinkje voor spraakweergavevenster onder Extra in het NVDA-menu.
Haal dit vinkje weg om de speech viewer uit te schakelen.

In het spraakweergavevenster treft u een selectievakje aan met de tekst "spraakweergave tonen bij opstarten". 
Als het vakje is aangevinkt, opent het spraakweergavevenster zich zodra NVDA wordt gestart.
Het spraakweergavevenster zal in principe elke keer dat het wordt geopend dezelfde plaats en grootte hebben als toen het de laatste keer gesloten werd.

Als het spraakweergavevenster ingeschakeld is, wordt de getoonde tekst voortdurend vernieuwd om het voorlezen bij te houden.
Maar hou je de muis boven of verplaats je de focus naar het viewer venster, dan wordt het verversen van de tekst tijdelijk gestopt om zo  gemakkelijk de getoonde tekst te kunnen selecteren en kopiëren.

Als u het Spraakweergavevenster altijd en overal wilt kunnen in- of uischakelen, kunt u daarvoor aangepaste invoerhandelingen aanmaken met behulp van [Invoerhandelingen koppelen onder Opties](#InputGestures).

### Braille Viewer (Brailleweergavevenster) {#BrailleViewer}

Voor goedziende softwareontwikkelaars of voor mensen die NVDA demonstreren aan een goedziend publiek is er een zwevend kader waarin alle brailleuitvoer  met het tekstequivalent voor elk brailleteken op het scherm wordt weergegeven.
De braille viewer (brailleweergavevenster) kan tegelijk met een fysieke leesregel worden gebruikt, het aantal cellen  komt overeen met het aantal op het fysieke apparaat.
Als de braille viewer ingeschakeld is, wordt de inhoud van het venster voortdurend ververst met wat er weergegeven wordt op de fysieke leesregel.

Om het brailleweergavevenster in te schakelen zet u een vinkje voor brailleweergavevenster onder Extra in het NVDA-menu.
Haal het vinkje weg om het uit te schakelen.

Fysieke brailleleesregels zijn uiteraard der zaak voorzien van knoppen om vooruit of terug te scrollen; om scrollen met de braille viewer mogelijk te maken kunt u in het [dialoogvenster Invoerhandelingen](#InputGestures) een sneltoets toewijzen waarmee u de brailleweergave 'terug- en vooruit scrollt'

In het braille weergavevenster treft u een selectievakje aan met het bijschrift 'braille viewer tonen bij start".
Als dit vakje is aangevinkt, opent de braille viewer wanneer  NVDA wordt gestart.
Het brailleweergavevenster zal in principe elke keer dat het wordt geopend dezelfde plaats en grootte hebben als toen het de laatste keer gesloten werd.

Het brailleweergavevenster  heeft een selectievakje met als label cel-routing via muisbeweging". Als standaardinstelling geldt dat dit vakje niet is aangevinkt.
Als het vakje is aangevinkt, zal het bewegen van de muis boven een braillecel ertoe leiden dat het commando "routeer naar braillecel" voor die cel wordt geactiveerd.
Hier wordt vaak mee gewerkt om de muisaanwijzer te verplaatsen of om een besturingselement te activeren.
Dit kan nuttig zijn om te testen of NVDA in staat is map a correct van braillecel terug te halen.
Om te voorkomen dat onbedoeld naar cellen wordt gerouteerd wordt het commando met een vertraging uitgevoerd.
Er moet met de muis bewogen worden tot dat deze groen kleurt.
De cell begint lichgeel gekleurd, gaat over in oranje en wordt dan plotseling groen.

Als u het Brailleweergavevenster altijd en overal wilt kunnen in- of uischakelen, kunt u daarvoor een aangepaste invoerhandeling aanmaken met behulp van [het dialoogvenster Invoerhandelingen](#InputGestures).

### Python-console {#PythonConsole}

Het NVDA Python-console, dat u aantreft in het NVDA-menu onder Extra, is een ontwikkelinstrument dat goed van pas komt bij het oplossen van bugs, algemene inspectie van het inwendige van NVDA  of het inspecteren van  de toegankelijkheidsopbouw van een toepassing.
Voor meer informatie gaat u naar de [NVDA Developer Guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Add-on-store {#AddonStoreMenuItem}

Hiermee opent u de Add-on-store #AddonsManager].
Hierover vindt u meer informatie in de uitgebreide rubriek: [Add-ons en de Add-on Store](#AddonsManager).

### Draagbare versie aanmaken {#CreatePortableCopy}

Hiermee opent u een dialoogvenster dat u in staat stelt een draagbare kopie van NVDA aan te maken vanuit de geïnstalleerde versie.
Zowel in het ene als in het andere geval geldt dat, wanneer u een draagbare versie van NVDA draait, er onder Extra in het NVDA-menu  het desbetreffende item vermeld staat als "NVDA op deze PC installeren" (in plaats van "Draagbare versie aanmaken').

Het dialoogvenster dat u in staat stelt een draagbare versie van NVDA aan te maken of NVDA op deze PC te installeren, laat u een pad naar een map kiezen waarin NVDA de draagbare versie moet aanmaken of waarin NVDA moet worden geïnstalleerd.

In dit dialoogvenster  kunt u het volgende in- of uitschakelen:

* Kopieer  configuratie van huidige gebruiker (dat is inclusief de bestanden in %appdata%\roaming\NVDA of in de gebruikersconfiguratie van uw draagbare kopie alsmede add-ons en andere modules)
* Nieuwe draagbare kopie van NVDA na het aanmaken starten  of NVDA na installatie starten (Hiermee start NVDA automatisch op nadat de draagbare versie is aangemaakt of nadat die  is geïnstalleerd)

### Hulpprogramma voor herstel van COM-registrfoutenn {#RunCOMRegistrationFixingTool}

Het installeren en deïnstalleren van programma's op een computer kan, er in bepaalde gevallen toe leiden dat COM DLL-bestanden niet langer in het register staan.
Omdat COM Interfaces zoals IAccessible afhankelijk zijn van een correcte COM DLL registratie, kunnen zich problemen voordoen in het geval dat er bij de registratie iets fout is gegaan.

Dit kan bijv gebeuren na het installeren en deïnstalleren  van Adobe Reader, Math Player en andere programma's.

Het ontbreken van een registeropname kan leiden tot problemen in browsers, desktop apps, de taakbalk en andere interfaces.

Met name kunnen navolgende problemen worden opgelost door dit hulpprogrammaatje uit te voeren:

* NVDA meldt "onbekend" bij het navigeren in browsers zoals Firefox, Thunderbird etc.
* NVDA schakelt niet tussen focusmodus en bladermodus
* NVDA is heel traag wanneer  u navigeert in browsers bij gebruik van de bladermodus
* En mogelijk andere problemen.

### Plugins herladen {#ReloadPlugins}

Zodra deze optie wordt geactiveerd, zullen alle app modules en globale plugins opnieuw worden geladen zonder dat NVDA wordt herstart. Dit is handig voor ontwikkelaars.
App-modules regelen hoe NVDA omgaat met  bepaalde applicaties.
Globale plugins regelen hoe  NVDA omgaat  met alel applicaties.

De volgende NVDA toetsenbordcommando's kunnen van pas komen:
<!-- KC:beginInclude -->

| Naam |Toets |Beschrijving|
|---|---|---|
|Pluginsherladen |`NVDA+control+f3` |Herlaadt NVDA's globale plugins en app-modules.|
|Geladen ep module en executabel |`NVDA+control+f1` |Meldt de naam van de app-module, indien aanwezig, en de naam van het executabel dat verbonden is met de  applicatie die de toetsenbord-focus heeft.|

<!-- KC:endInclude -->

## Ondersteunde spraaksynthesizers {#SupportedSpeechSynths}

In deze rubriek vindt u informatie over spraaksynthesizers die door NVDA worden ondersteund.
Een uitgebreidere lijst met gratis en betaalde spraaksynthesizers, die met NVDA compatibel zijn, vindt u onder [extra stemmen op](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

De [eSpeak NG](https://github.com/espeak-ng/espeak-ng) synthesizer is in NVDA ingebouwd en hiervoor hoeven geen drivers of andere componenten te worden geïnstalleerd.
In Windows 8.1 start NVDA  standaard op met de eSpeak NG spraaksynthesizer. In Windows 10 en later wordt standaard ([Windows OneCore gebruikt. 
Bij gebruik van de draagbare versie van NVDA is de ingebouwde eSpeak NG synthesizer de ideale optie.

Voor elk van de stemmen die in eSpeak NG is opgenomen, is een andere taal beschikbaar.
Er worden meer dan 43 talen door eSpeak NG ondersteund.

De klank van de stemmen kan worden aangepast.

### Microsoft Spraak API versie 4 (SAPI 4) {#SAPI4}

Sapi 4 is een oudere Microsoft standaard voor softwarematige spraaksynthesizers.
Voor gebruikers die reeds SAPI 4 synthesizers op hun systeem geïnstalleerd hebben, blijft NVDA deze ondersteunen.
Microsoft ondersteunt deze standaard echter niet meer en de benodigde componenten worden door Microsoft niet langer beschikbaar gesteld.

Als hiervan gebruik wordt gemaakt in NVDA dan treft u alle geïnstalleerde spraakgenerators met de beschikbare stemmen aan in de [categorie Spraak](#SpeechSettings) van het dialoogvenster [Instellingen van NVDA](#NVDASettings) of in [Synth Settins Ring](#SynthSettingsRing).

### Microsoft Spraak API versie 5 (SAPI 5) {#SAPI5}

Sapi 5 is een Microsoft standaard voor softwarematige spraaksynthesizers.
Op het internet zijn veel spraaksynthesizers te koop of gratis te downloaden die compatibel zijn met deze standaard. Waarschijnlijk is er op uw computer al minstens 1 SAPI 5 stem geïnstalleerd.
Als hiervan gebruik wordt gemaakt in NVDA dan treft u alle geïnstalleerde spraakgenerators met de beschikbare stemmen aan in de [categorie Spraak](#SpeechSettings) van het dialoogvenster [Instellingen van NVDA](#NVDASettings) of in [Synth Settins Ring](#SynthSettingsRing).

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Het Microsoft Speech Platform biedt stemmen voor veel talen die normaalgesproken gebruikt worden bij de ontwikkeling van server-gebaseerde spraaktoepassingen.
Deze stemmen kunnen ook met NVDA gebruikt worden.

Om van deze stemmen gebruik te maken dient u 2 componenten te installeren:

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  -- Deze Webpagina bevat veel bestanden voor spraakin- en uitvoer.
 -Kies het tekst-naar-sprraakbestand voor de gewenste taal / stem.
 -Voorbeeld: Het bestand MSSpeech_TTS_en-US_ZiraPro.msi is een amerikaans-engelse stem.
  -

### Windows OneCore-stemmen {#OneCore}

In Windows 10 en later zijn nieuwe stemmen beschikbaar die bekend staan als "OneCore" of "mobiele" stemmen.
Deze stemmen zijn er voor vele talen en ze reageren sneller dan de Microsoft-stemmen die beschikbaar zijn bij gebruik van Microsoft Speech API versie 5.
In Windows 10 gebruikt NVDA standaard de Windows OneCore stemmen ([eSpeak NG](#eSpeakNG) wordt in andere versies gebruikt).

Om nieuwe Windows OneCore-stemmen toe te voegen gaat u naar Spraakinstellingen in de systeeminstellingen van Windows.
Kies de optie "Stemmen toevoegen" en zoek naar de gewenste taal.
Van veel talen zijn meer varianten beschikbaar.
"Verenigd Koninkrijk" en "Australië" zijn 2 voorbeelden van de varianten van het Engels.
"Frankrijk", "Canada" en "Zwitserland" zijn beschikbaar als varianten  van het Frans.
Zoek eerst de algemene benaming van de gewenste taal (zoals Engels of Frans), om vervolgens de variant van uw keus in de lijst op te zoeken.
Selecteer  een taal of talen naar keuze en gebruik de knop "Toevoegen" om deze toe tevoegen.
Eenmaal toegvoegd moet u NVDA opnieuw starten.

Voor ondersteunde talen en stemmen raadpleeg je [ https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01] for a list of available voices.

## Ondersteunde Brailleleesregels {#SupportedBrailleDisplays}

In deze rubriek treft u informatie aan over de brailleleesregels die door NVDA worden ondersteund.

### Leesregels die automatische herkenning op de achtergrond ondersteunen {#AutomaticDetection}

Zowel via USB als bluetooth kan NVDA veel brailleleesregels op de achtergrond automatisch detecteren. 
U kunt dit zo instellen door in de dialoog [Braille-instellingen van NVDA](#BrailleSettings) de optie Automatisch te selecteren als de brailleleesregel van uw voorkeur.
Deze optie staat standaard ingeschakeld.

De volgende leesregels ondersteunen automatische herkenning:

* Handy Tech leesregels
* Baum/Humanware/APH/Orbit braille leesregels
* HumanWare Brailliant BI/B serie
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6 serie
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series
* Eurobraille Esys/Esytime/Iris leesregels
* Nattiq Brailleleesregels-
* Seika Notetaker: MiniSeika (16, 24 cellen), V6, en V6Pro (40 cellen)
* Tivomatic Caiku Albatross 46/80 leesregels
* Elke leesregel met ondersteuning voor het Standaard HID Brailleprotocol

### Freedom Scientific Focus/PAC Mate Series {#FreedomScientificFocus}

Alle Focus en PAC Mate leesregels van [Freedom Scientific](https://www.freedomscientific.com/) worden ondersteund.
De drivers voor de brailleleesregels van Freedom Scientific moeten op uw computer worden geïnstalleerd.
Zonodig kunt u de drivers downloaden van de pagina voor [Focus Blue Braille Display Driver](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Hoewel op deze pagina alleen de Focus 40 Blueleesregel wordt genoemd, ondersteunen deze drivers alleFocus en Packmate leesregels van Freedom Scientific.

De standaardinstelling is dat NVDA automatisch deze leesregels detecteert en via USB of bluetooth een verbinding tot stand brengt.
U kunt evenwel bij het configureren van de leesregel expliciet kiezen voor een "USB-" of "Bluetooth-poort" waarmee het te gebruiken verbindingstype wordt beperkt.
Dit kan handig zijn als u de Focus leesregel met NVDA wilt verbinden via bluetooth en hem tegelijkertijd wilt opladen via de usb-aansluiting op uw computer.
De automatische  brailleleesregeldetectie van NVDA herkent de leesregel ook op basis van USB of Bluetooth.

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregel raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets (van leesregel)|
|---|---|
|Brailleregel terugscrollen |topRouting1 (eerste braillecel)|
|Brailleregel vooruitscrollen |topRouting20/40/80 (laatste braillecel)|
|Brailleregel terugscrollen |leftAdvanceBar (linker advance-balk)|
|Brailleregel vooruitscrollen |rightAdvanceBar (rechter advance-balk)|
|Braille koppelen wisselen |linker GDF-knop+rechter GDF-knop|
|Functie linker WizWheel wisselen |Linker WizWheel indrukken|
|Achteruit scrollen met gebruik van linker WizWheel |Linker WizWheel omhoog|
|Vooruit scrollen met gebruik linker WizWheel |Linker WizWheel omlaag|
|Functie rechter WizWheel wisselen |Rechter WizWheel indrukken|
|Achteruitscrollen met gebruik van rechter WizWheel |Rechter WizWheel omhoog|
|Vooruit sscrollen met gebruik van rechter WizWheel |RechterWizWheel omlaag|
|Naar braillecel gaan |Routing|
|Shift+tab |Braille-spatiebalk+punt1+punt2|
|Tab |Braille-spatiebalk+punt4+punt5|
|Pijl omhoog |spatiebalk+punt1|
|Pijl omlaag |Braille-spatiebalk+punt4|
|Ctrl+Pijl links |Braille-spatiebalk+punt2|
|Ctrl+Pijl rechts |Braille-spatiebalk+punt5|
|Pijl links |Braille-spatiebalk+punt3|
|Pijl rechts |Braille-spatiebalk+punt6|
|Home |Braille-spatiebalk+punt1+punt3|
|End |Braille-spatiebalk+punt4+punt6|
|Ctrl+Home |Braille-spatiebalk+punt1+punt2+punt3|
|Ctrl+End |Braille-spatiebalk+punt4+punt5+punt6|
|Alt |Braille-spatiebalk+punt1+punt3+punt4|
|Alt+tab |Braille-spatiebalk+punt2+punt3+punt4+punt5|
|alt+shift+tab-toets |brailleSpatieBalk+punt1+punt2+punt5+punt6|
|windows+tab-toets |brailleSpatieBalk+punt2+punt3+punt4|
|Escape |Braille-spatiebalk+punt1+punt5|
|windows-toets |Braille-spatiebalk+punt2+punt4+punt5+punt6|
|Spatiebalk |braillespatiebalk|
|Functieschakeltoets control |braillespatiebalk+punt3+punt8|
|Functieschakeltoets alt |brailleSpatieBalk+punt6+punt8|
|Functieschakeltoets windows |brailleSpatieBalk+punt4+punt8|
|Functieschakeltoets NVDA |brailleSpatieBalk+punt5+punt8|
|Functieschakeltoets shifty |brailleSpatieBalk+punt7+punt8|
|Functieschakeltoetsen control en shift |brailleSpatieBalk+punt3+punt7+punt8|
|Functieschakeltoetsen alt en shift |brailleSpatieBalk+punt6+punt7+punt8|
|Functieschakeltoetsen windows en shifts |brailleSpatieBalk+punt4+punt7+punt8|
|Functieschakeltoetsen NVDA en shift |brailleSpatieBalk+punt5+punt7+punt8|
|Functieschakeltoetsen control en alt |brailleSpatieBalk+punt3+punt6+punt8|
|Functieschakeltoetsen control, alt, en shift |brailleSpatieBalk+punt3+punt6+punt7+punt8|
|Windows+d (alle toepassingen minimaliseren) |spatiebalk+punt1+punt2+punt3+punt4+punt5+punt6|
|Huidige regel weergeven |spatiebalk+punt1+punt4|
|NVDA-menu |spatiebalk+punt1+punt3+punt4+punt5|

Voor de nieuwere Focusmodellen die uitgerust zijn met "rocker bar" toetsen (Focus 40, Focus 80 en Focus Blue):

| Naam |Toetscombinatie|
|---|---|
|Brailleregel naar vorige regel verplaatsen |linkerRockerBarOmhoog, rechterRockerBarOmhoog|
|Brailleregel naar volgende regel verplaatsen |linkerRockerBarOmlaag, rechterRockerBarOmlaag|

Alleen voor de Focus 80:

| Naam |Toetscombinatie|
|---|---|
|Brailleregel terugscrollen |linkerBumperBarOmhoog, rechterBumperBarOmhoog|
|Brailleregel verder scrollen |linkerBumperBarOmlaag, rechterBumperBarOmlaag|

<!-- KC:endInclude -->

### Optelec ALVA 6 serie/protocol converter {#OptelecALVA}

Zowel de ALVA BC640 als de BC680 leesregel van [Optelec](https://www.optelec.com/) worden ondersteund.
U kunt een oudere Optelec-leesregel, zoals een Braille Voyager, desgewenst koppelen door gebruik te maken van een 'protocol converter' (protocolomvormer) van Optelec.
U hoeft geen specifieke drivers te installeren om deze leesregels te gebruiken.
Sluit de leesregel aan en pas de configuratie van NVDA aan voor het gebruik van deze leesregels.

Merk op dat NVDA mogelijk niet samenwerkt met een ALVA BC6-leesregel via een Bluetooth-verbinding als de koppeling tot stand is gebracht met behulp van het Bluetooth-hulpprogrammaatje van ALVA.
Als u dit hulpprogrammaatje gebruikt hebt om de koppeling tot stand te brengen en NVDA uw leesregel niet detecteert, raden we u aan uw ALVA-leesregel op de reguliere manier te koppelen door middel van de Bluetooth-instellingen van Windows. 

Merk op dat, hoewel sommige leesregels wel een brailletoetsenbord hebben, ze zelf standaard voor de omzetting van braille naar tekstzorgen.
Dit houdt in dat het brailleinvoersysteem van NVDA in de standaardsituatie niet gebruikt wordt, m.a.w. dat het instellen van een brailleïnvoertabel geen effect) heeft.
Bij ALVA-leesregels die voorzien zijn van recente firmware, kan de HID-toetsenbordsimulatie door middel van een invoerhandeling uitgeschakeld worden.

Bij gebruik van deze leesregels met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregels raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel achteruit scrollen |t1, etouch1|
|Brailleregel naar voorafgaande regel brengen |t2|
|Naar huidige focus verplaatsen |t3|
|Brailleregel naar volgende regel brengen |t4|
|Brailleregel vooruit scrollen |t5, etouch3|
|Naar braillecel gaan| Routing|
|tekstopmaakg onder braillecel melden |secondaire routing|
|HID-toetsenbordsimulatie in- of uitschakelen |t1+spEnter|
|Naar bovenste regel verplaatsen in leesmodus |t1+t2|
|Naar onderste regel verplaatsen in leesmodus |t4+t5|
|Braille koppelen wisselen |t1+t3|
|Titel weergeven |etouch2|
|Statusbalk weergeven |etouch4|
|Shift+Tabtoets |Sp1|
|Alt-toets |Sp2, alt|
|Escape-toets |Sp3|
|Tab-toets |Sp4|
|Pijltoets omhoog |SpUp|
|Pijltoets omlaag |SpDown|
|Pijltoets naar links |SpLinks|
|Pijltoets naar rechts |SpRechts|
|Enter-toets |spEnter, enter|
|Datum/tijd weergeven |sp2+sp3|
|NVDA-Menü |Sp1+Sp3|
|Windows-Toets+D (alle toepassingenn minimaliseren) |Sp1+Sp4|
|windows toets+b(focus op systeemvak) |sp3+sp4|
|Windows-Toets |Sp1+Sp2, Windows|
|Alt+Tabtoets |Sp2+Sp4|
|control+home-toets |t3+spOmhoog|
|control+end-toets |t3+spOmlaag|
|home-toets |t3+spLinks|
|end-toets |t3+spRechts|
|control-toets |control|

<!-- KC:endInclude -->

### Handy Tech Leesregels {#HandyTech}

NVDA ondersteunt de meeste via usb-gekoppelde of blutooth-verbonden dan wel op de sereële poort aangesloten leesregels van [Handy Tech](https://www.handytech.de/).de/].
Voor sommige oudere USB-leesregels moeten de USB-drivers van Handy Tech op uw computer worden geïnstalleerd. -Bovendien moet u de universele driver van Handy Tech installeren. Deze vindt u op ftp://ftp.handytech.de/public/Software/BrailleDriver/bsd1206a.exe

De volgende leesregels worden niet zonder meer ondersteund, maar ze kunnen wel gebruikt worden met behulp van het [universele stuurprogramma van [Handy Tech dat te vinden is op](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) en een NVDA add-on:

* Braillino
* Bookworm
* Modulaire leesregels met firmware-versie 1.13 of lager. Please note that the firmware of this displays can be updated.

Bij gebruik van de Handy Tech leesregels met NVDA zijn de volgende toetscombinaties van toepassing:
(U kunt in de documentatie bij deze leesregels nalezen waar deze toetsen zich precies bevinden.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel achteruit scrollen |Links, omhoog, b3|
|Brailleregel vooruit scrollen |Rechts, omlaag, b6|
|Een regel naar boven |B4|
|Een regel naar beneden |B5|
|Naar braillecel springen |Routing|
|Shift+Tabtoets |esc, links triple actietoets omhoog+omlaag|
|Alt-Toets |B2+B4+B5|
|Escape-Toets |B4+B6|
|Tabtoets |Enter, rechter triple actietoets omhoog+omlaag|
|Enter-toets |esc+enter, linker+rechter triple actietoets omhoog+omlaag, joystickAction|
|Pijltoets omhoog |joystickUp|
|Pijltoets omlaag |joystickDown|
|Pijltoets links |joystickLeft|
|Pijltoets rechts |joystickRight|
|NVDA-Menü |B2+B4+B5+B6|
|braille koppelen wisselen |b2|
|braillecursor in- of uitschakelen |b1|
|focuscontextweergave in- of uitschakelen |b7|
|brailleinvoer in- of uitschakelen |spatie+b1+b3+b4 (spatie+hoofdletter B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

De Lilli brailleleesregel die verkrijgbaar is op [MDV](https://www.mdvbologna.it/) wordt ondersteund.
U hoeft geen specifieke drivers te installeren om deze leesregel te gebruiken.
Sluit de leesregel aan en pas de configuratie van NVDA aan voor het gebruik van deze leesregel.

Deze leesregel heeft geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregel raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel achteruit scrollen |LF|
|Brailleregel vooruit scrollen |RG|
|Brailleregel naar vorige regel bewegen |UP|
|Brailleregel naar volgende regel bewegen |DN|
|Cursor naar Braillecel verplaatsen |route|
|Shift+Tabtoets |SLF|
|Tabtoets |SRG|
|Alt+Tabtoets |SDN|
|Alt+Shift+Tabtoets |SUP|

<!-- KC:endInclude -->

### Brailleleesregels van Baum/HumanWare/APH/Orbit {#Baum}

Verscheidene brailleleesregels van [Baum](https://www.visiobraille.de/index.php?article_id=1&clang=2), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) and [Orbit](https://www.orbitresearch.com/) worden ondersteund, voor zover deze via usb of Bluetooth dan wel serieel verbonden worden.
Hiertoe behoren:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Enkele andere Baum-leesregels zouden wellicht ook kunnen werken, maar dit is nog niet getest.

Als u leesregels die geen gebruik maken van HID via USB aansluit , moett u eerst de USB drivers installeren die door de fabrikant beschikbaar worden gesteld.
De VarioUltra en Pronto! gebruiken HID.
De Refreshabraille en Orbit Reader 20 kunnen van HID gebruik maken als ze op de juiste manier worden geconfigureerd.

De USB seriële modus van de Orbit Reader 20 wordt momenteel alleen in Windows 10 en later ondersteund.
Doorgaans moet in plaats daarvan de USB HID-modus worden gebruikt.

Bij gebruik van deze leesregels met NVDA zijn de volgende toetscombinaties van toepassing.
Waar de toetsen zich bevinden, leest u in de documentatie bij de leesregels.
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |`d2`|
|Brailleregel vooruit scrollen |`d5`|
|Brailleregel naar vorige regel verplaatsen |`d1`|
|Brailleregel naar volgende regel verplaatsen |`d3`|
|Cursor naar braillecel verplaatsen |`routing`|
|shift+tab-toetsen |`spatie+punt1+punt3`|
|tab-toets |`spatie+punt4+punt6`|
|alt-toets |`spatie+punt1+punt3+punt4` (`spatie+m`)|
|`escape-toets` |`spatie+punt1+punt5` (`spatie+e`)|
|windows-toets |`spatie+puntt3+punt4`|
|`alt+tab-toetsen` |`spatie+punt2+punt3+punt4+punt5` (`spatie+t`)|
|`NVDA-menu` |`spatie+punt1+punt3+punt4+punt5` (`spatie+n`)|
|`windows+d-toetsen` (minimaliseer alle applicaties) |`spatie+punt1+punt4+punt5` (`spatie+d`)|
|Alles lezen |`spatie+punt1+punt2+punt3+punt4+punt5+punt6`|

Voor leesregels die een Joystick hebben, geldt:

| Naam |Toets|
|---|---|
|Toets "pijl omhoog" |omhoog|
|Toets "Pijl omlaag" |omlaag|
|Toets "Pijl links" |links|
|Toets "Pijl rechts" |rechts|
|Enter-toets |selecteren|

<!-- KC:endInclude -->

### Hedo Profiline usb {#HedoProfiline}

De Profiline usb leesregels van [hedo Reha-Technik](https://www.hedo.de/) worden ondersteund.
U moet eerst de usb-driver van de fabrikant installeren.

Deze leesregel heeft geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregel raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |K1|
|Brailleregel vooruit scrollen |K3|
|Brailleregel naar vorige regel verplaatsen |B3|
|Brailleregel naar volgende regel verplaatsen |B5|
|Cursor naar braillecel verplaatsen |routing|
|Koppeling van leesregel omschakelen |K2|
|alles lezen |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

De MobilLine usb leesregels van [hedo Reha-Technik](https://www.hedo.de/) worden ondersteund.
U moet eerst de usb-driver van de fabrikant installeren.

Deze leesregel heeft nog geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregel raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |K1|
|Brailleregel vooruit scrollen |K3|
|Brailleregel naar vorige regel verplaatsen |B3|
|Brailleregel naar volgende regel verplaatsen |B5|
|Cursor naar braillecel verplaatsen |routing|
|Koppeling van leesregel omschakelen |K2|
|alles lezen |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Serie / BrailleNote Touch {#HumanWareBrailliant}

De brailleleesregels uit de serie BI en B van [HumanWare](https://www.humanware.com/), waaronder de BI 14, BI 32, BI 20X, BI 40, BI 40X en B 80, worden ondersteund, voor zover ze via USB of bluetooth verbonden zijn.
Als u de leesregels via usb, waarbij het protocol op HumanWare is ingesteld, wilt aansluiten, moet u eerst de usb-drivers van de fabrikant installeren.
USB drivers zijn niet nodig als u van het OpenBraille protocol gebruik maakt.

Aanvullend worden ook de volgende  toestellen  ondersteund en hiervoor hoeven geen speciale drivers te worden geïnstalleerd.

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Bij gebruik van de Brailliant BI/B en de BrailleNote touch met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregels raadplegen.)

#### Toegewezen toetsen die gelden voor Alle modellen {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |Links|
|Brailleregel vooruit scrollen |Rechts|
|Brailleregel naar vorige regel verplaatsen |Omhoog|
|Brailleregel naar volgende regel verplaatsen |Omlaag|
|Cursor naar braillecel verplaatsen |routing|
|Leesregel koppelen aan/uit |omhoog+omlaag|
|Toets Pijl omhoog |Spatiebalk+Punt1|
|Toets Pijl omlaag |Spatiebalk+Punt4|
|Toets Pijl links |Spatiebalk+Punt3|
|Toets Pijl rechts |Spatiebalk+Punt6|
|Shift+Tab-toets |Spatiebalk+Punt1+Punt3|
|Tab-Toets |Spatiebalk+Punt4+Punt6|
|Alt-Toets |Spatiebalk+Punt1+Punt3+Punt4 (spatiebalk+m)|
|Escape-toets |Spatiebalk+Punt1+Punt5 (spatiebalk+e)|
|Enter-toets |Punt8|
|Windows-toets |Spatiebalk+Punt3+Punt4|
|Alt+Tabtoets |Spatiebalk+Punt2+Punt3+Punt4+Punt5 (spatiebalk+t)|
|NVDA Menu |spatie+punt1+punt3+punt4+punt5 (spatie+n)|
|windows+d toets (alle toepassingen minimaliseren) |spatie+punt1+punt4+punt5 (spatie+d)|
|alles lezen |spatie+punt1+punt2+punt3+punt4+punt5+punt6|

<!-- KC:endInclude -->

#### Toegewezen toetsen voor de Brailliant BI 32, BI 40 en B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Naam |toets|
|---|---|
|NVDA Menu |c1+c3+c4+c5 (commando n)|
|windows+d toets (alle toepassingen minimaliseren) |c1+c4+c5 (commanod d)|

|Alles lezen | c1+c2+c3+c4+c5+c6 |
<!-- KC:endInclude -->

#### Toegewezen toetsen voor de Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Pijl Omhoog |joystick naar boven|
|Pijl Omlaag |joystick naar beneden|
|Pijl Links |joystick naar links|
|Pijl Rechts |joystick naar rechts|
|Enter-toets |joystick actie|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Serie {#Hims}

NVDA ondersteunt de leesregelmodellen Braille Sense, Braille EDGE, Smart Beetle en Sync Braille van [Hims](https://www.hims-inc.com/) die via USB of bluetooth kunnen worden aangesloten.
Als u voor de USB-aansluiting kiest, moet u wel eerst de [USB-drivers van HIMS, die je vindt op](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) op je systeem installeren. 

Bij gebruik van deze leesregels met NVDA zijn de volgende toetscombinaties van toepassing:
(Voor meer details kunt u de documentatie bij deze leesregels raadplegen.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Cursor naar braillecel brengen |routing|
|Brailleregel terugscrollen |LinkerzijdeOmhoogScrollen, Rechterzijde OmhoogScrollen, LinkerScroll|
|Brailleregel vooruit scrollen |LinkerzijdeOmlaagScrollen, RechterzijdeOmlaagScrollen, RechterScroll|
|Naar vorige regel verplaatsen |LinkerzijdeOmhoogScrollen+RechterzijdeOmhoogScrollen|
|Naar volgende regel verplaatsen |LinkerzijdeOmlaagScrollen+RechterzijdeOmlaagScrollen|
|Naar vorige regel verplaatsen in reviewmodus |RechterPijlOmhoog|
|Naar volgene regel verplaatsen in reviewmodus |RechterPijlOmlaag|
|Naar vorig teken verplaatsen in reviewmodus |RechterPijlLinks|
|Naar volgend teken verplaatsen in reviewmodus |RechterPijlRechts|
|Naar huidige focus verplaatsen |LinkerzijdeOmhoogScrollen+LinkerzijdeOmlaagScrollen, RechterzijdeOmhoogScrollen+RechterzijdeOmlaagScrollen, LinkerScroll+RechterScroll|
|control-toets |smartbeetle: F1, brailleedge:F3|
|windows-toets |F7, smartbeetle:f2|
|alt-toets |punt1+punt3+punt4+spatie, F2, smartbeetle:F3, brailleedge:f4|
|shift-toets |f5|
|insert-toets |punt2+punt4+spatie, F6|

|Contextmenutoets | punt1+punt2+punt3+punt4+spatie, F8 |

|Caps Locktoets |punt1+punt3+punt6+spatie|
|tab-toets |punt4+punt5+spatie, F3, brailleedge:F2|
|shift+alt+tab-toetscombinatie |f2+f3+f1|
|alt+tab-toetscombinatie |f2+f3|
|shift+tab-toetscombinatie |punt1+punt2+spatie|
|end-toets |punt4+punt6+spatie|
|control+end-toetscombinatie |punt4+punt5+punt6+spatie|
|home-toets |punt1+punt3+spatie, smartbeetle:f4|
|control+home-toetscombinatie |punt1+punt2+punt3+spatie|
|alt+f4-toetscombinatie |punt1+punt3+punt5+punt6+spatie|
|linker Pijltoets |punt3+spatie, Linker PijlLinks|
|control+shift+PijlLinks-toetscombinatie |punt2+punt8+spatie+f1|
|control+PijlLinks-toetscombinatie |punt2+spatie|
|shift+alt+PijlLinks-toetscombinatie |punt2+punt7+f1|
|`alt+PijlLinks-toetscombinatie` |`punt2+punt7+spatie`|
|PijlRechts-toets |punt6+spatie, Linker PijlRechts|
|control+shift+PijlRechts-toetscombinatie |punt5+punt8+spatie+f1|
|control+PijlRechts-toetscombinatie |punt5+spatie|
|shift+alt+PijlRechts-toetscombinatie |punt5+punt7+f1|
|`alt+PijlRechts-toetscombinatie` |`punft5+punt7+spatie`|
|pageUp-toets |punt1+punt2+punt6+spatie|
|control+pageUp-toetscombinatie |punt1+punt2+punt6+punt8+spatie|
|PijlOmhoog-toets |punt1+spatie, linker pijl omhoog|
|control+shift+PijlOmhoog-toetscombinatie |punt2+punt3+punt8+spatie+F1|
|control+PijlOmhoog-toets |punt2+punt3+spatie|
|shift+alt+PijlOmhoog-toetscombinatie |punt2+punt3+punt7+F1|
|`alt+PijlOmhoog-toetscombinatie` |`punt2+punt3+punt7+spatie`|
|shift+PijlOmhoog-toetscombinatie |Linker ScrollOmlaag+spatie|
|pageDown-toets |punt3+punt4+punt5+spatie|
|control+pageDown-toetscombinatie |punt3+punt4+punt5+punt8+spatie|
|PijlOmlaag-toets |punt4+spatie, Linker PijlOmlaag|
|control+shift+PijlOmlaag-toetscombinatie |punt5+punt6+punt8+spatie+F1|
|control+PijlOmlaag-toetscombinatie |punt5+punt6+spatie|
|shift+alt+PijlOmlaag-toetscombinatie |punt5+punt6+punt7+F1|
|`alt+PijlOmlaag-toetscombinatie` |`punt5+punt6+punt7+spatie`|
|shift+PijlOmlaag-toetscombinatie |spatie+Rechter ScrollOmlaag|
|escape-toets |punt1+punt5+spatie, f4, brailleedge:f1|
|del-toets |punt1+punt3+punt5+spatie, punt1+punt4+punt5+spatie|
|f1-toets |punt1+punt2+punt5+spatie|
|f3-toets |punt1+punt4+punt8+spatie|
|f4toets |punt7+f3|
|windows+b-toetscombinatie |punt1+punt2+f1|
|windows+d-toetscombinatie |punt1+punt4+punt5+f1|
|control+inserttoetscominatie |smartbeetle: f1+Rechter Scroll|
|alt+insert-toetscombinatie |smartbeetle: f3+Rechter Scroll|

<!-- KC:endInclude -->

### Seika Brailleleesregels {#Seika}

De volgende Seika Brailleleesregels van Nippon Telesoft onderverdeeld in twee groepen met verschillende functionaliteit worden ondersteund:

* [Seika Versie 3, 4, en 5 (40 cellen), Seika80 (80 cellen)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 cellen), V6, en V6Pro (40 cellen)](#SeikaNotetaker)

U vindt meer informatie over de leesregels op de [Demo en Driver Download pagina van de makers](https://en.seika-braille.com/down/index.html).

++++ Seika Versie 3, 4, en 5 (40 cellen), Seika80 (80 cellen) +++[SeikaBrailleDisplays]

* Deze leesregels hebben nog geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.
* Selecteer "Seika Braille Displays" om handmatig te configureren
* Voordat u de Seika v3/4/5/80 kunt gebruiken , moeten er apparaatstuurprogramma's worden geïnstalleerd. 
De stuurprogramma's zijn bij de fabrikant verkrijgbaar https://en.seika-braille.com/down/index.html].

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing:
(Informatie over de plaats van de toetsen vindt u in de documentatie bij deze leesregel.)
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |links|
|Brailleregel vooruit scrollen |rechts|
|Brailleregel naar vorige regel verplaatsen |B3|
|Brailleregel naar volgende regel verplaatsen |Br|
| Koppeling van leesregel omschakelen |b5|
|---|---|
|alles lezen |B6|
|tab |B1|
|shift+tab |B2|
|alt+tab |b1+b2|
|NVDA-menu |links+rechts|
|Cursor naar braillecel verplaatsen |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 cellen), V6, en V6Pro (40 cellen) {#SeikaNotetaker}

* Deze leesregels hebben  ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA via bluetooth en usb.
* Selecteer "Seika Notetaker" of "auto" om te configureren.
* U hoeft geen extra stuurprogramma's te installeren bij gebruik van een Seika Notetaker brailleleesregel.

Hierna volgen toetstoewijzingen voor de Seika Notetaker.
Informatie over de plaats van de toetsen vindt u in de documentatie bij deze leesregel.
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |Links|
|Leesregel vooruitscrollen |rechts|
|Alles  lezen |spatie+Backspace|
|NVDA-menu |Links+Rechts|
|Leesregel verplaatsen naar vorige regel |LJ up|
|Leesregel verplaatsen naar volgende regel |LJ down|
|Braille koppelen omschakelen |LJ center|
|tab |LJ rechts|
|shift+tab |LJ links|
|Pijl-omhoogtoets |RJ up|
|Pijl-omlaagtoets |RJ down|
|linkerPijltoets |RJ links|
|rechterPijltoets |RJ rechts|
|Naar braillecel routeren |routing|
|shift+Pijl-omhoogtoets |Spatie+RJ up, Backspace+RJ up|
|shift+Pijl-omlaagtoets |Spatie+RJ down, Backspace+RJ down|
|shift+linkerPijltoets |Spatie+RJ links, Backspace+RJ links|
|shift+rechterPijltoets |Spatie+RJ rechts, Backspace+RJ rechts|
|entertoets |RJ center, punt8|
|escape-toets |Spatie+RJ center|
|windows-toets |Backspace+RJ center|
|spatie-toets |Spatie, Backspace|
|backspace-toets |punt7|
|pageup-toets |spatie+LJ rechts|
|pagedown-toets |spatie+LJ links|
|home-toets |spatie+LJ up|
|end-toets |spatie+LJ down|
|control+home-toets |backspace+LJ up|
|control+end-toets |backspace+LJ down|

### Papenmeier Braillex Nieuwere Modellen {#PapenmeierNew}

De volgende brailleleesregels worden ondersteund:

* BRAILLEX EL 40c, EL 80c, EL 20c, EL60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2D80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB en Bluetooth)
* BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus (USB and bluetooth)

Deze leesregel heeft geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.
Er kan zich een probleem voordoen met een optie van de USB-driver van de leesregel bij het laden van de leesregel.
Probeer dan het volgende:

1. Vergewis je ervan dat je de [nieuwste driver hebt geïnstalleerd via](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Open Apparaatbeheer in Windows
1. Ga in de lijst naar beneden tot  je "USB Controllers" of "USB apparaten" tegenkomt.
1. Selecteer "Papenmeier Braillex USB Apparaat".
1. Open Eigenschappen en kies het tabblad "Geavanceerd".
Het gebeurt wel eens  dat het tabblad "Geavanceerd" niet tevoorschijn komt.
Als dat zich voordoet, koppel dan de braille leesregel los van de computer,sluit NVDA af, wacht even en verbind de leesregel opnieuw.
Zo nodig herhaal je dit 4 tot 5 keer.
Als het tabblad  "Geavanceerd" nog steeds niet wordt weergegeven, herstart dan de computer.
1. Schakel de optie "Laad VCP" uit.

De meeste leesregels hebben een gebruiksvriendelijke navigatiebalk (EAB = Easy Access Bar, waarmee intuïtief en snel gewerkt kan worden.
De navigatiebalk kan in vier richtingen bewogen worden waarbij er als regel twee schakelpunten per richting zijn.
De c-Serie en de Live-serie vormen hierop een uitzondering.

De modellen uit de c-serie en enkele andere leesregels hebben twee rijen routing toetsen waarvan de bovenste rij door NVDA gebruikt wordt om informatie over opmaak te krijgen.
Door bij de modellen uit de c-serie één van de routing toetsen ingedrukt te houden en daarbij op de EAB (navigatiebalk) te drukken, wordt de staat van het tweede schakelpunt gesimuleerd.
De leesregels uit de live-serie hebben maar één rij routing-toetsen en de EAB heeft 1 schakelpunt per richting.
Het tweede schakelpunt kan worden gesimuleerd door een van de routing-toetsen in te drukken en de EAP in de daarmee overeenkomende richting te drukken. 
Door de linker-, rechter-, omhoog- en omlaagtoets (of de EAB) in te drukken en vast te houden wordt de bijbehorende actie herhaald.

In het algemeen beschikken deze leesregels over de volgende toetsen:

| Naam |Toets|
|---|---|
|l1 |Linkertoets voor|
|l2 |Linkertoets achter|
|r1 |Rechtertoets voor|
|r2 |Rechtertoets achter|
|omhoog |Navigatiebalk eenmaal naar boven|
|omhoog2 |Navigatiebalk tweemaal naar boven|
|links |Navigatiebalk eenmaal naar links|
|links2 |Navigatiebalk tweemaal naar links|
|rechts |Navigatiebalk eenmaal naar rechts|
|rechts2 |Navigatiebalk tweemaal naar rechts|
|omlaag |Navigatiebalk eenmaal naar beneden|
|omlaag2 |Navigatiebalk tweemaal naar beneden|

De volgende toetscommando's zijn voor Papenmeier-Brailleleesregels beschikbaar:
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |links|
|Brailleregel vooruitscrollen |rechts|
|Brailleregel naar vorige regel verplaatsen |omhoog|
|Brailleregel naar volgende regel verplaatsen |omlaag|
|Cursor naar Braillecel verplaatsen |Routing|
|Teken onder cursor voorlezen |l1|
|Huidige navigatorobject activeren |l2|
|Wissel Braille gekoppeld aann |r2|
|Titel van actieve venster weergeven |l1+omhoog|
|Statusbalk actieve venster weergeven |l2+omlaag|
|Navigatorobject naar hoger niveau verplaatsen |omhoog2|
|Navigatorobject één niveau naar beneden verplaatsen |omlaag2|
|Navigatorobject naar vorige Object verplaatsen |links2|
|Navigatorobject naar volgend object verplaatsen |rechts2|
|Tekstopmaak weergeven onder braillecel |bovenste rij routingtoetsen|

<!-- KC:endInclude -->

De Braillex Trio heeft vierr extra toetsen die zich aan de voorkant van het brailletoetsenbord bevinden.
Van links naar rechts zijn dit:

* linker duimtoets (lt)
* spatie
* spatie
* rechter duimtoets (rt)

Momenteel is de rechterduimtoets buiten gebruik.
De twee binnenste toetsen zijn als spatietoets gedefinieerd.

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|escape-toets |spatie + punt 7|
|pijl omhoog-toets |spatie + punt 2|
|linker pijltoets |spatie + punt 1|
|rechter pijltoets |spatie + punt 4|
|pijl omlaag-toets |spatie + puunt 5|
|Ctrl-toets |lt+punt2|
|alt-toets |lt+punt3|
|ctrl+escape-toets |spatie + punt 1 2 3 4 5 6|
|tab-toets |spatie + punt 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BRAILLEX Oudere Modellen {#PapenmeierOld}

De volgende brailleleesregels worden ondersteund:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Merk op dat deze leesregels alleen via een seriële poort kunnen worden aangesloten.
Dientengevolge hebben deze leesregels geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.
U moet de poort waarop de leesregel is aangesloten selecteren nadat u deze driver hebt gekozen in het dialoogvenster [Brailleleesregel Selecteren](#SelectBrailleDisplay). 

Sommige leesregels hebben een gebruiksvriendelijke navigatiebalk (EAB = Easy Access Bar, waarmee intuïtief en snel gewerkt kan worden.
De navigatiebalk kan in vier richtingen bewogen worden waarbij er als regel twee schakelpunten per richting zijn.
door indrukken en vasthouden van de toetsen up, down, rechts en links (of EAB)wordt bewerkstelligd dat de ermee samenhangende handeling wordt herhaald. 
Oudere toestellen hebben geen EAB; In plaats daarvan worden toetsen aan de voorkant gebruikt.

Doorgaans beschikken de leesregels over de volgende toetsen :

| Naam |Toets|
|---|---|
|l1 |Linkertoets voor|
|l2 |Linkertoets achter|
|r1 |Rechtertoets voor|
|r2 |Rechtertoets achter|
|up |1 Stap omhoog|
|up2 |2 Stappen omhoog|
|left |1 Stap naar links|
|left2 |2 Stappen naar links|
|right |1 Stap naar rechts|
|right2 |2 Stappen naar rechts|
|dn |1 Stap omlaag|
|dn2 |2 Stappen omlaag|

In NVDA zijn de volgende toetscommando's voor Papenmeier-Brailleleesregels beschikbaar:

<!-- KC:beginInclude -->
Toestellen met EAB:

| Naam |Toets|
|---|---|
|Brailleregel terugscrollen |links|
|Brailleregel vooruitscrollen |rechts|
|Brailleregel naar vorige regel verplaatsen |omhoog|
|Brailleregel naar volgende regel verplaatsen |omlaag|
|Cursor naar Braillecel verplaatsen |Routing|
|Teken onder cursor voorlezen |l1|
|Huidige navigatorobject activeren |l2|
|Titel van actieve venster weergeven |l1+omhoog|
|Statusbalk actieve venster weergeven |l2+omlaag|
|Navigatorobject naar hoger niveau verplaatsen |omhoog2|
|Navigatorobject één niveau naar beneden verplaatsen |omlaag2|
|Navigatorobject naar volgende Object verplaatsen |rechts2|
|Navigatorobject naar voorafgaand object verplaatsen |links2|
|Tekstopmaak onder braillecel weergeven |bovenste rij routingtoetsen|

BRAILLEX Tiny:

| Naam |Toets|
|---|---|
|Teken onder cursor voorlezen |l1|
|Huidige navigatorobject activeren |l2|
|Brailleregel achteruitscrollen |links|
|Brailleregel vooruitscrollen |rechts|
|Brailleregel naar vorige regel verplaatsen |omhoog|
|Brailleregel naar volgende regel verplaatsen |omlaag|
|Braille koppelen wisselen |r2|
|Navigatorobject naar containing  niveau verplaatsen |r1+up|
|Navigatorobject één niveau naar beneden verplaatsen |r1+dn|
|Navigatorobject naar voorafgaand Object verplaatsen |r1+left|
|Navigatorobject naar volgende Object verplaatsen |r1+right|
|Tekstopmaak onder braillecel weergeven |Bovenste routingstrip|
|Titelweergeven |l1+omhoog|
|Statusbalk weergeven |l2+omlaag|

BRAILLEX 2D Scherm:

| Naam |Toets|
|---|---|
|Teken onder cursor voorlezen |l1|
|Huidige navigatorobject activeren |l2|
|Braille koppelen wisselen |r2|
|Tekstopmaak onder braillecel weergeven |Bovenste routingstrip|
|Naar vorige regel gaan |up/omhoog|
|Leesregel terugscrollen |left/links|
|Leesregel vooruitscrollen| right/rechts|
|Naar volgende regel gaan |dn/omlaag|
|Naar volgend object gaan |left2/links2|
|Één niveau omhoog gaan |up2/omhoog2|
|ÉÉn niveau omlaag gaan |dn2/omlaag2|
|Naar voorafgaand object gaan |right2/rechts2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA ondersteunt de BrailleNote notitieapparaten van [Humanware](https://www.humanware.com) wanneer deze gebruikt worden als leesregel voor een schermlezer.
De volgende modellen worden ondersteund:

* BrailleNote Classic (uitsluitend seriële verbinding)
* BrailleNote PK (Seriële en bluetooth verbinding)
* BrailleNote MPower (Seriële en bluetooth verbinding)
* BrailleNote Apex (USB en Bluetooth verbinding)

Voor de BrailleNote Touch kunt u de paragraaf [Brailliant BI Series / BrailleNote Touch](#HumanWareBrailliant) raadplegen.

Met uitzondering van de BrailleNote PK, is er ondersteuning voor zowel het braille (BT) als het QWERTY (QT) toetsenbord.
Voor de BrailleNote QT, is er geen onderrsteuning voor PC toetsenbord-emulatie.
U kunt ook braillepunten invoeren door het QT-toetsenbord te gebruiken.
Raadpleeg het onderdeel braille terminal in de handleiding van de BrailleNote voor nadere bijzonderheden.

Als uw toestel meer dan één verbindingstype ondersteunt, moet u bij het koppelen van uw BrailleNote met NVDA de poort van het braille-uitvoerapparaat instellen onder braille-terminal opties.
Raadpleeg de BrailleNote-handleiding voor meer informatie.
In NVDA kan hett ook noodzakelijk zijn de poort in te stellen in het dialoogvenster [Brailleleesregel Selecteren](#SelectBrailleDisplay).
Als u een USB- of bluetooth-verbinding tot stand brengt, kunt u de poort instellen op "Automatisch", "USB" of "Bluetooth", afhankelijk van de beschikbare keuzemogelijkheden.
Als u gebruik maakt van een legacy seriële poort (of van een USB-naar-serieel adapter), of als geen van de voornoemde opties beschikbaar is, moet u uit de lijst met hardware-poorten de te gebruiken communicatiepoort selecteren.

Voor u de BrailleNote Apex met behulp van de USB gebruikersinterface verbindt, moet u de stuurprogramma's installeren die door HumanWare beschikbaar worden gesteld.

Op de BrailleNote Apex BT, kunt u voor het uitvoeren van verschillende NVDA-commando's het scroll-wieltje gebruiken dat tussen punt 1 en punt 4 zit.
Het wieltje heeft vier punten met richtingindicatie, een centrale klik-knop, en een wieltje dat met de wijzers van de klok mee kan draaien of tegen de wijzers van de klok in.

Hieronder volgen de BrailleNote-toetscommando's voor NVDA.
Raadpleeg de documentatie bij de BrailleNote voor informatie over de positie van de toetsen.

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |terug|
|Leesregel vooruitscrollen |vooruit|
|Leesregel naar vorige regel verplaatsen |vorige|
|Leesregel naar volgende regel verplaatsen |volgende|
|Naar braillecel springen |routing|
|NVDA menu |spatie+punt1+punt3+punt4+punt5 (spatie+n)|
|Braille koppelen wisselen |vorige+volgende|
|Pijl omhoog |spatie+Punt1|
|Pijl omlaag |spatie+Punt4|
|Pijl links |spatie+Punt3|
|Pijl rechts |spatie+Punt6|
|Pagina omhoog |spatie+Punt1+punt3|
|Pagina omlaag |spatie+Punt4+punt6|
|Home |spatie+Punt1+punt2|
|End |spatie+Punt4+punt5|
|Control+home |spatie+punt1+punt2+punt3|
|Control+end |spatie+punt4+punt5+punt6|
|Spatiebalk |spatie|
|Enter |spatie+punt8|
|Backspace |spatie+punt7|
|Tab |spatie+punt2+punt3+punt4+punt5 (spatie+t)|
|Shift+tab |spatie+punt1+punt2+punt5+punt6|
|Windows-toets |spatie+punt2+punt4+punt5+punt6 (spatie+w)|
|Alt |spatie+punt1+punt3+punt4 (spatie+m)|
|Invoerhulp in-/uitschakelen |spatie+punt2+punt3+punt6 (spatie+kleine h)|

Voor de BrailleNote QT zijn de volgende commando's van toepassing als deze niet in de braille-invoermodus staat.

| Naam |Toets|
|---|---|
|NVDA-menu |Lezen+n|
|pijltoets Omhoog |Pijlomhoog|
|pijltoets Omlaag |Pijlomlaag|
|Pijltoets Links |Pijllinks|
|Pijltoets Rechts |Pijlrechts|
|Page uptoets |functiePijlomhoog|
|Page down-toets |functie+Pijlomlaag|
|Home-toets |functie+Pijllinks|
|End-toets |functie+Pijlrechts|
|Control+home-toetsen |lezen+t|
|Control+end-toetsen |lezen+b|
|Enter-toets |enter|
|Backspace-toets |backspace|
|Tab-toets |tab|
|Shift+tab-toetsen |shift+tab|
|Windows-toets |lezen+w|
|Alt-toets |lezen+m|
|Invoerhulp Aan/Uit |lezen+1|

Met het scrollwieltje kunnen de volgende commando's worden uitgevoerd:

| Naam |Toets|
|---|---|
|pijltoets Omhoog |Pijlomhoog|
|pijltoets Omlaag |Pijlomlaag|
|pijltoets Links |Pijllinks|
|pijltoets Rechts |Pijlrechts|
|Enter-toets |centrale knop|
|Tab-toets |scroll-wieltje met de klok mee|
|Shift+tab-toetsen |scroll-wieltje tegen de klok in|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA biedt ondersteuning voor EcoBraille-leesregels van [ONCE](https://www.once.es/).
De volgende modellen worden ondersteund:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

In NVDA kunt u in het dialoogvenster [Brailleleesregel Selecteren](#SelectBrailleDisplay) de seriële poort instellen waarmee de leesregel wordt verbonden
Deze leesregels hebben geen ondersteuning voor de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.

Bij gebruik van deze leesregel met NVDA zijn de volgende toetscombinaties van toepassing: 
(Raadpleeg de [EcoBraille documentatie](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) waar beschreven wordt waar de toetsen zich bevinden.)

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|brailleleesregel terugscrollen |T2|
|brailleleesregel vooruitscrollen |T4|
|brailleleesregel naar vorige regel verplaatsen |T1|
|brailleleesregel naar volgende regel verplaatsen |T5|
|Naar braillecel gaan |Routing|
|Huidige navigatorobject activeren |T3|
|Naar volgende leesmodus overschakelen |F1|
|Naar containerobject gaan |F2|
|Naar vorige leesmodus overschakelen |F3|
|Naar vorig object gaan |F4|
|Huidig object melden |F5|
|Naar volgend object gaan |F6|
|Naar object gaan dat de focus heeft |F7|
|Naar eerste “contained” object gaan |F8|
|Systeemfocus of invoegcursor naar huidige leespositie verplaatsen |F9|
|Leescursorpositie melden |F0|
|Wisselknop “braille tethered to” |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

De SuperBraille leesregel die voornamelijk verkrijgbaar is in Taiwan, kan ofwel serieel of via usb worden aangesloten. 
Aangezien de SuperBraille niet over fysieke invoertoetsen of scroltoetsen beschikt, moet alle invoer gebeuren door middel van een standaard computertoetsenbord.
Om deze reden en om compatibiliteit met andere schermlezers in Taiwan te bewerkstelligen, kan men over 2 toetsen beschikken waarmee scrollen van de leesregel mogelijk wordt gemaakt:
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |numerieke Min-toets|
|Leesregel vooruitscrollen |numerieke Plus-toets|

<!-- KC:endInclude -->

### Eurobraille leesregels {#Eurobraille}

De b.book, b.note, Esys, Esytime en Iris leesregels  van Eurobraille worden door NVDA ondersteund.
Deze apaaraten hebben een brailletoetsenbord met 10 toetsen.
Raadpleeg de bij deze leesregel behorende documentatie voor de beschrijving van deze toetsen.
Van de twee toetsen die als een spatiebalk geplaatst zijn, werkt de linker toets als backspace en met de rechter toets maak je een spatie.

Deze leesregels, die via usb worden aangesloten, hebben 1 los, op zichzelfstaand, usb-toetsenbord.
Het is mogelijk dit toetsenbord te activeren of te deactiveren door "HID Toetsenbord simulatie" aan of uit tezetten met behulp van een invoerhandeling.
In de onderstaande beschrijving van het brailletoetsenbord wordt er van uitgegaan dat dit gedeactiveerd is.

#### Brailletoetsenbordfuncties {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Wis laatst ingevoerde braillecel of teken |`backspace`|
|Alle brailleinvoer omzetten en enter-toets indrukken |`backspace+spatie`|
|Schakelen met `NVDA-toets` |`punt3+punt5+spatie`|
|`insert-toets` |`punt1+punt3+punt5+spatie`, `punt3+punt4+punt5+spatie`|
|`delete-toets` |`punt3+punt6+spatie`|
|`home-toets` |`punt1+punt2+punt3+spatie`|
|`end-toets` |`punt4+punt5+punt6+spatie`|
|`linker Pijltoets` |`punt2+spatie`|
|`rechterPijltoets` |`punt5+spatie`|
|`Pijlomhoogtoets` |`punt1+spatie`|
|`Pijlomlaag-toets`y |`punt6+spatie`|
|`pageUp-toets` |`punt1+punt3+spatie`|
|`pageDown-toets` |`punt4+punt6+spatie`|
|`numpad1-toets` |`punt1+punt6+backspace`|
|`numpad2-toets` |`punt1+punt2+punt6+backspace`|
|`numpad3-toets` |`punt1+punt4+punt6+backspace`|
|`numpad4-toets` |`punt1+punt4+punt5+punt6+backspace`|
|`numpad5-toets` |`punt1+punt5+punt6+backspace`|
|`numpad6-toets` |`punt1+punt2+punt4+punt6+backspace`|
|`numpad7-toets` |`punt1+punt2+punt4+punt5+punt6+backspace`|
|`numpad8-toets` |`punt1+punt2+punt5+punt6+backspace`|
|`numpad9-toets` |`punt2+punt4+punt6+backspace`|
|`numpadInsert-toets` |`punt3+punt4+punt5+punt6+backspace`|
|`numpadDecimaal-toets` |`punt2+backspace`|
|`numpadDelen-toets` |`punt3+punt4+backspace`|
|`numpadVermenigvuldigen-toets` |`punt3+punt5+backspace`|
|`numpadAftrekken-toets` |`punt3+punt6+backspace`|
|`numpadPlus-toets` |`punt2+punt3+punt5+backspace`|
|`numpadEnter-toets` |`punt3+punt4+punt5+backspace`|
|`escape-toets` |`punt1+punt2+punt4+punt5+spatie`, `l2`|
|`tab-toets` |`punt2+punt5+punt6+spatie`, `l3`|
|`shift+tab-toetscombinatie` |`punt2+punt3+punt5+spatie`|
|`printScreen-toets` |`punt1+punt3+punt4+punt6+spatie`|
|`pause-toets` |`punt1+punt4+spatie`|
|`Toepassingen-toets` |`punt5+punt6+backspace`|
|`f1-toets` |`punt1+backspace`|
|`f2-toets` |`punt1+punt2+backspace`|
|`f3-toets` |`punt1+punt4+backspace`|
|`f4-toets` |`punt1+punt4+punt5+backspace`|
|`f5-toets` |`punt1+punt5+backspace`|
|`f6-toets` |`punt1+punt2+punt4+backspace`|
|`f7-toets` |`punt1+punt2+punt4+punt5+backspace`|
|`f8-toets` |`punt1+punt2+punt5+backspace`|
|`f9-toets` |`punt2+punt4+backspace`|
|`f10-toets` |`punt2+punt4+punt5+backspace`|
|`f11-toets` |`punt1+punt3+backspace`|
|`f12-toets` |`punt1+punt2+punt3+backspace`|
|`windows-toets` |`punt1+punt2+punt4+punt5+punt6+spatie`|
|Schakelen met `windows-toets` |`punt1+punt2+punt3+punt4+backspace`, `punt2+punt4+punt5+punt6+spatie`|
|`capsLock-toets` |`punt7+backspace`, `punt8+backspace`|
|`numLock-toets` |`punt3+backspace`, `punt6+backspace`|
|`shift-toets` |`punt7+spatie`|
|Schakelen met `shift-toets` |`punt1+punt7+spatie`, `punt4+punt7+spatie`|
|`control-toets` |`punt7+punt8+spatie`|
|Schakelen met  `control-toets` |`punt1+punt7+punt8+spatie`, `punt4+punt7+punt8+spatie`|
|`alt-toets` |`punt8+spatie`|
|Schakelen met Alt-toets`` |`punt1+punt8+spatie`, `punt4+punt8+spatie`|
|HID Toetsenbord simulatie aan/uit |`schakelaar1Links+joystick1Omlaag`, `schakelaar1Rechts+joystick1Omlaag`|

<!-- KC:endInclude -->

#### b.book-toetsenbordcommando's {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |"achterwaarts"|
|Leesregel vooruitscrollen |voorwaarts""|
|Naar huidige focus gaan |`achterwaarts+voorwaarts`|
|Routeer naar braillecel |`routing`|
|`linkerPijl-toets` |``joystick2Links`|
|`rechterPijl-toets` |`joystick2Rechts`|
|`Pijlomhoog-toets` |`joystick2Omhoog`|
|`Pijlomlaag-toets` |`joystick2Omlaag`|
|`enter-toets` |`joystick2Centrum`|
|`escape-toets` |`c1`|
|`tab-toets` |`c2`|
|Schakelen met  `shift-toets` |`c3`|
|Schakelen met  `control-toets` |`c4`|
|Schakelen met `alt-toets` |`c5`|
|Schakelen met  `NVDA-toets` |`c6`|
|`control+Home-toetscombinatie` |`c1+c2+c3`|
|`control+End-toetscombinatie` |`c4+c5+c6`|

+<!-- KC:endInclude -->

#### b.note-toetsenbordcommando's {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|

|Brailleleesregel terugscrollen | `linkerToetsenblokLLinks` |

|Leesregel vooruitscrollen |`linkerToetsenblokRechts`|
|Routeer naar braillecel |`routing`|
|Tekstopmaak onder braillecel melden |`dubbelRouting`|
|Naar volgende regel gaan in review |`linkerToetsenblokomlaag`|
|Omschakelen naar vorige leesmodus |`linkerToetsenLinks+linkerToetsenblokOmhoog`|
|Omschakelen naar volgende leesmodus |`linkerToetsenblokRechts+linkerToetsenblokomlaag`|
|`llinkerPijl-toets` |`rechterToetsenblokLinks`|
|`rechterPijl-toets` |`rechterToetsenblokRechts`|
|`Pijlomhoog-toets` |`rechterToetsenOmhoog`|
|`Pijlomlaag-toets` |`rechterToetsenblokomlaag`|
|`control+home-toetscombinatie` |`rechterToetsenLinks+rechterToetsenblokOmhoog`|
|`control+end-toetscombinatie` |`rechterToetsenblokLinks+rechterToetsenblokOmhoog`|

<!-- KC:endInclude -->

#### Esys-toetsenbordcommando's {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |`sschakelaar1Links`|
|Leesregel vooruitscrollen |`chakelaar1Rechts`|
|Naar huidige focus gaan |`schakelaar1Centraal`|
|Routeer naar braillecel |`routing`|
|Tekstopmaak onder braillecel melden |`dubbelRouting`|
|Naar vorige regel gaan in review |`joystick1Omhoog`|
|Naar volgende regel gaan  in review |`joystick1Omlaag`|
|Naar vorig (letter)teken gaan in review |`joystick1Links`|
|Naar volgend (letter)teken gaan in review |`joystick1Rechts`|
|`linkerPijl-toets` |`joystick2Links`|
|`rechterPijl-toets` |`joystick2Rechts`|
|`Pijlomhoog-toets` |`joystick2Omhoog`|
|`Pijlomlaag-toets` |`joystick2Omlaag`|
|`enter-toets` |`joystick2Centraal`|

<!-- KC:endInclude -->

#### Esytime-toetsenbordcommando's {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |`l1`|
|Leesregel vooruitscrollen |`l8`|
|Naar huidige focus gaan |`l1+l8`|
|Routeren naar braillecel |`routing`|
|Tekstopmaak onder braillecel melden |`dubbelRouting`|
|Naar vorige regel gaan in review |`joystick1Omhoog`|
|Naar volgende regel gaan in review |`joystick1Omlaag`|
|Naar vorig (letter)teken gaan in review |`joystick1Links`|
|Naar volgend (letter)teken gaan in review |`joystick1Rechts`|
|`linkerPijl-toets` |`joystick2Links`|
|`rechterPijltoets` |`joystick2Rechts`|
|`Pijlomhoog-toets` |`joystick2Omhoog`|
|`Pijlomlaag-toets` |`joystick2Omlaag`|
|`enter-toets` |`joystick2Centraal`|
|`escape-toets` |`l2`|
|`tab-toets` |`l3`|
|Schakelen met  `shift-toets` |`l4`|
|Schakelen met `control-toets` |`l5`|
|Schakelen met `alt-toets` |`l6`|
|Schakelen met `NVDA-toets` |`l7`|
|`control+home-toetscombinatie` |`l1+l2+l3`, `l2+l3+l4`|
|`control+end-toetscombinatie` |`l6+l7+l8`, `l5+l6+l7`|
|HID Toetsenbord simulatie aan/uit |`l1+joystick1Omlaag`, `l8+joystick1Omlaag`|

<!-- KC:endInclude -->

### Nattiq nBraille Displays {#NattiqTechnologies}

NVDA ondersteunt de leesregels van [Nattiq Technologies](https://www.nattiq.com/) wanneer ze via USB worden aangesloten.
Windows 10 en later detecteert  the brailleleesregels zodra ze zijn verbonden.  Voor oudere versies van Windows (lager dan  Win10) moet u wellicht USB-drivers installeren.
U vindt ze op de website van de fabrikant.

Hieronder volgen de geldende toetscommando's van de leesregels van Nattiq Technologies bij gebruik met NVDA.
Raadpleeg de documentatie bij de leesregels waarin beschreven wordt waar deze toetsen zich bevinden.
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Leesregel terugscrollen |Omhoog|
|Leesregel vooruitscrollen |Omlaag|
|Verplaats leesregel naar vorige regel |links|
|Verplaats leesregel naar volgende regel |rechts|
|Routeer naar braille-cel |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) is een opzichzelfstaand programma dat kan dienen ter ondersteuning van veel meer brailleleesregels.
Om hiervan gebruik te kunnen maken moet u [BRLTTY voor Windows](https://www.brltty.app/download.html) installeren.
U moet de nieuwste versie van het programma (bij voorbeeld, met als naam brltty-win-4.2-2.exe) downloaden en installeren.
Wanneer u de leesregel configureert en de te gebruiken poort instelt, moet u ervoor zorgen de instructies nauwkeurig op te volgen, vooral bij gebruik van een USB-leesregel waarvoor de drivers van de fabrikant reeds zijn geïnstalleerd.

Het Brltty-programma zorgt zelf voor de verwerking van brailleïnvoer van leesregels die over een brailletoetsenbord beschikken.
Het is dan ook niet relevant dat een invoertabel in NVDA wordt ingesteld.

BRLTTY blijft buiten de op de achtergrond uitgevoerde automatische leesregelherkenning van NVDA.

De volgende BRLTTY-commando's worden in NVDA ondersteund.
Voor informatie over toetsenbordtabellen kunt u de [BRLTTY lijsten met toetstoewijzingen](https://brltty.app/doc/KeyBindings/) raadplegen.
<!-- KC:beginInclude -->

| Naam |BRLTTY-commando|
|---|---|
|Brailleregel terugscrollen |`fwinlt` (een scherm naar links bewegen)|
|Brailleregel vooruit scrollen |`fwinrt` (een scherm naar rechts bewegen)|
|Brailleregel naar vorige regel verplaatsen |`lnup` (een regel omhoog gaan)|
|Brailleregel naar volgende regel verplaatsen |`lndn` (een regel omlaag gaan)|
|Cursor naar Braillecel verplaatsen |`route` (Cursor naar karakter bewegen)|
|Invoerhulp in- of uitschakelen |`leren` (ingaan/verlaten commando leermodus)|
|Open het NVDA-menu |`prefmenu` (ingaan/verlaten menu voorkeuren)|
|Configuratie terugzetten |`prefload` (teruggaan naar voorkeuren van bron)|
|Configuratie opslaan |`prefsave` (voorkeuren op schijf opslaan)|
|Tijd melden |`tijd` (huidige datum en tijd weergeven)|
|Noem de regel waar de leescursor zich nu bevindt |`say_line` (huidige regel noemen)|
|Alles voorlezen met gebruikmaking van leescursor |`say_below` (vanaf huidige regel lezen tot aanonderkant scherm)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

De Caiku Albatross-toestellen, die door Tivomatic zijn vervaardigd en in Finland verkrijgbaar zijn, kunnen via USB dan wel serieel worden verbonden.
Om deze leesregels te gebruiken hoeven er geen specifieke stuurprogramma's te worden geïnstalleerd.
Plug de leesregel gewoon in, en configureer NVDA om hem te gebruiken.

Merk op: Baud rate 19200 wordt sterk aanbevolen.
Stel zo nodig de Baud rate-waarde in op 19200 via het leesregelmenu.
Hoewel de driver een baud rate, van 9600 ondersteunt, heeft deze geen controle over de baud rate die de leesregel gebruikt.
Omdat de standaard baud rate, van de leesregel 19200 is, zal de driver allereerst deze proberen.
Als baud rates (snelheden)  niet hetzelfde zijn, kan de driver onverwacht gedrag vertonen.

Hierna volgen de toetstoewijzingen voor deze leesregels met NVDA.
U kunt in de documentatie bij deze leesregels nalezen waar deze toetsen zich precies bevinden..
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Ga naar bovenste regel in leesmodus |`home1`, `home2`|
|Ga naar onderste regel in leesmodus |`end1`, `end2`|
|Verplaatst navigatorobject naar de huidige focus |`eCursor1`, `eCursor2`|
|Ga naar huidige focus |`cursor1`, `cursor2`|
|Verplaatst de muisaanwijzer naar het huidige navigatorobject |`home1+home2`|
|Plaatst navigatorobject bij  het huidige object onder de muisaanwijzer and speaks it |`end1+end2`|
|Verplaatst focus naar huidige navigatorobject |`eCursor1+eCursor2`|
|Wissel braille tethered naar |`cursor1+cursor2`|
|Verplaats brailleleesregel naar vorige regel |`up1`, `up2`, `up3`|
|Verplaats brailleleesregel naar volgende regel |`down1`, `down2`, `down3`|
|Scroll brailleleesregel terug |`left`, `lWheelLeft`, `rWheelLeft`|
|Scroll brailleleesregel vooruit |`right`, `lWheelRight`, `rWheelRight`|
|Routeer naar braillecel |`routing`|
|Meld tekstopmaak onder braillecel |`secondary routing`|
|Schakel tussen manieren waarop contextinformatie wordt aangeboden in braille |`attribute1+attribute3`|
|Schakelt tussen  opties voor spraakmodi |`attribute2+attribute4`|
|Schakelt om naar de vorige review-modus (bijv. object, document of scherm) |`f1`|
|Schakelt om naar de volgende review-modus (bijv. object, document of scherm) |`f2`|
|Verplaatst navigatorobject naar het object waarin het is opgenomen |`f3`|
|Verplaatst het navigatorobject naar het eerste object daarbinnen |`f4`|
|Verplaatst het navigatorobject naar het vorige object |`f5`|
|Verplaatst het navigatorobject naar het volgende object |`f6`|
|Geeft het huidige navigatorobject aan |`f7`|
|Geeft informatie over de locatie van de tekst of het object bij de leescursor |`f8`|
|Toont braille-instellingen |`f1+home1`, `f9+home2`|
|Leest statusbalk en verplaatst navigatorobject er in |`f1+end1`, `f9+end2`|
|De vormen van de braillecursor verkennen/aanpassen |`f1+eCursor1`, `f9+eCursor2`|
|Van braillecursor wisselen |`f1+cursor1`, `f9+cursor2`|
|Doorloop de braille toon meldingen modus |`f1+f2`, `f9+f10`|
|Doorloop de braille toon selectiestatus |`f1+f5`, `f9+f14`|

|Doorloop de stadia "braille systeemcursor verplaatsen bij routering leescursor"  | `f1+f3`, `f9+f11` |

|Voert de standaardactie uit mbt het huidige navigatorobject |`f7+f8`|
|Geeft datum/tijdweer |`f9`|
|Geeft batterij-status en resterende tijd aan  als netvoeding niet is aangesloten |`f10`|
|Geeft titel weer |`f11`|
|Geeft statusbalk aan |`f12`|
|Geeft de huidige regel  onder de applicatie-cursor aan |`f13`|
|Alles weergeven |`f14`|
|Geeft huidige karakter onder leescursor |`f15`|
|Geeft de regel van het huidige navigatorobject waar de leescursor zich bevindt |`f16`|
|Leest het woord voor bij het huidige navigatorobject waar de leescursor zich bevindt |`f15+f16`|
|Verplaatst de leescursor naar de vorige regel  van het huidige navigatorobject en leest die voor |`lWheelUp`, `rWheelUp`|
|Verplaatst de leescursor naar de volgende regel  van het huidige navigatorobject en leest die voor |`lWheelDown`, `rWheelDown`|
|`Windows+d` toetscombinatie  (alle toepassingen minimaliseren) |`attribute1`|
|`Windows+e` toetscombinatie (deze computer) |`attribute2`|
|`Windows+b` toetscombinatie (focus systeemvak) |`attribute3`|
|`Windows+i` toetscombinatie (Windows-instellingen) |`attribute4`|

<!-- KC:endInclude -->

### Standaard HID Brailleleesregels {#HIDBraille}

Het betreft hier een experimentele driver voor de nieuwe Standaard HID-Braillespecificatie die in 2018 overeengekomen is tussen  Microsoft, Google, Apple en verscheidene andere bedrijven op het gebied van ondersteunende technologie waaronder NV Access.
Gehoopt wordt dat alle toekomstige brailleleesregelmodellen van alle fabrikanten van dit standaardprotocol gebruik gaan maken waardoor het niet langer nodig is dat elke fabrikant een eigen merkspecifieke leesregelstuurprogramma ontwikkelt.

De automatische brailleleesregeldetectie van NVDA herkent ook elke leesregel die dit protocol ondersteunt.

Hieronder volgen de momenteel geldende toetsen met hun funftie voor deze leesregels.
<!-- KC:beginInclude -->

| Naam |Toets|
|---|---|
|Brailleleesregel terugscrollen |naar  links pannen of rocker omhoog|
|Brailleleesregel vooruitscrollen |naar rechts pannen of rocker omlaag|
|Naar braillecel routeren |routing-set 1||
|Braille volgen aan/uit |Omhoog+Omlaag|
|pijlOmhoog |joystick van je af, dpad omhoog of spatie+punt1|
|pijlOmlaag |joystick naar je toe, dpad omlaag of spatie+punt4|
|pijlLinks |spatie+punt3, joystick llinks  of dpad links|
|pijlRechts |spatie+punt6, joystick recht of dpad rechts|
|shift+tab-toets |spatie+punt1+punt3|
|tab-toets |spatie+punt4+punt6|
|alt-toetsy |spatie+punt1+punt3+punt4 (spatie+m)|
|escapetoets |spatie+punt1+punt5 (spatie+e)|
|enter-toets |punt8, joystick centraal of dpad centraal|
|windows-toets |spatie+punt3+punt4|
|alt+tab-toets |spatie+punt2+punt3+punt4+punt5 (spatie+t)|
|NVDA-menu |spatie+punt1+punt3+punt4+punt5 (spatie+n)|
|windows+d-toets (alle toepassingen minimaliseren) |spatie+punt1+punt4+punt5 (spatie+d)|
|Alles voorlezen |spatie+punt1+punt2+punt3+punt4+punt5+punt6|

<!-- KC:endInclude -->

## Geavanceerde Onderwerpen {#AdvancedTopics}
### Veilige Modus {#SecureMode}

Mogelijk willen systeembeheerders NVDA zodanig configureren dat  ongeoorloofde toegang tot het systeem verhinderd wordt. 
Met NVDA kunnen aangepaste add-ons worden  geïnstalleerd, waarmee willekeurige code, kan worden uitgevoerd ook wanneer NVDA wordt gedraaid met beheerdersrechten.
Met NVDA kunnen gebruikers eveneens willekeurige code uitvoeren door middel van de NVDA Python Console.
Met de veilige modus van NVDA wordt voorkomen dat gebruikers hun NVDA-configuratie wijzigen, en tevens wordt ongeoorloofde toegang tot het systeem beperkt.

NVDA draait in veilige modus wanneer u de opdracht uitvoert met betrekking tot  [beveiligde schermen](#SecureScreens), tenzij de `serviceDebug` [systeem-brede parameter](#SystemWideParameters) gebruikt is.
Om NVDA te dwingen altijd in veilige modus op te starten stelt u de `forceSecureMode` in [als systeembrede parameter](#SystemWideParameters).
NVDA kan ook worden  opgestart in veilige modus met  de `-s` [commandoregel-optie](#CommandLineOptions).

In veilige modus is het niet mogelijk om:

* De configuratie en andere instellingen op schijf op te slaan
* De map Invoerhandelingen op schijf op te slaan
* aanpassingen t.a.v. het [Configuratieprofiel](#ConfigurationProfiles) aan te brengen zoals het aanmaken, verwijderen, hernoemen van profielen etc.
* Aangepaste configuratiemappen laden met behulp van [de commandoregel-optie `-c`](#CommandLineOptions)
* NVDA bij te werken en draagbare versies aan te maken
* De [Add-on Store](#AddonsManager) te bereiken
* te werken met de[NVDA Python console](#PythonConsole)
* te werken met de [Log Viewer](#LogViewer) en om te loggen
* Toegang te krijgen tot het [Brailleweergavevenster](#BrailleViewer) en [Spraakweergavevenster](#SpeechViewer)
* externe documenten zoals de gebruikershandleiding of de lijst met medewerkers, vanuit het NVDA-menu te openen.

Geïnstalleerde kopieën van  NVDA slaan hun configuratieprofielen inclusief add-ons op in `%APPDATA%\nvda`.
Om  te voorkomen dat NVDA-gebruikers rechtstreeks wijzigingen aanbrengen in de configuratie of eventuele add-ons moet toegang van de gebruiker tot deze map ook worden beperkt.

Veilige modus  werkt niet voor draagbare kopieën van  NVDA.
Deze beperking geldt eveneens voor een tijdelijke kopie van NVDA die wordt gebruikt bij het uitvoeren van het installatiebestand.
In een veilige omgeving, loopt een gebruiker die een draagbaar uitvoerbestand uitvoert hetzelfde veiligheidsrisico ongeacht de veilige modus.
Het is te verwachten dat systeembeheerderss het uitvoeren van niet-geautoriseerde software op hun systemen beperkt toelaten en dat geldt evenzeer voor portable kopieën van NVDA.

NVDA-gebruikers zullen meestal uitgaan van een  NVDA-configuratieprofiel dat het beste aansluit bij hun behoeften.
Hieronder kan het installeren en configureren van aangepaste add-ons begrepen zijndie los van NVDA op hun geschiktheid beoordeeld moeten worden.
Veilige modus neutraliseert wijzigingen in de configuratie van NVDA, vergewis u er dan ook van dat NVDA naar behoren is geconfigureerd voordat  u  in veilige modus gaat.

### Beveiligde Schermen {#SecureScreens}

NVDA draait in [veilige modus](#SecureMode) wanneer het programma wordt uitgevoerd met betrekking tot beveiligde schermen tenzij de `serviceDebug` [systeem-brede parameter](#SystemWideParameters) gebruikt is.

Wanneer NVDA gedraaid wordt vanaf een beveiligd scherm, maakt het programma gebruik van een systeemprofiel met daarbij behorende voorkeursinstellingen.
De gebruikersvoorkeuren in NVDA kunnen gekopieerd worden [voor gebruik in beveiligde schermen](#GeneralSettingsCopySettings).

Onder beveiligde schermen vallen:

* Het Windows-aanmeldscherm
* Het dialoogvenster  User Access Control (UAC) dat actief is wanneer u een handeling als beheerder uitvoert
  * Het installeren van programma's is hierbij inbegrepen

### Commandoregelopties {#CommandLineOptions}

Aan het commando'NVDA starten' kunnenextra opties worden toegevoegd die van invloed zijn op het opstartgedrag. 
U kunt zoveel opties opgeven als u nodig hebt. 
Deze opties kunnen worden opgegeven in het dialoogvenster Eigenschappen van de snelkoppeling waarmee NVDA wordt gestart, het venster Uitvoeren (Windows-toets + r) of via de Windows-opdrachtprompt.
De opties moeten met spaties van de naam van het NVDA-uitvoerbestand en van elkaar worden gescheiden.
Een nuttige optie is bij voorbeeld, `--add-ons uitschakelen`, waarmee alle actieve Add-Ons in NVDA worden onderbroken.
Hierdoor kan worden vastgesteld of een probleem door een Add-On wordt veroorzaakt en kan de normale werking van NVDA, als deze ernstig werd verstoord door problemen met Add-Ons, worden hersteld.

U kunt bij voorbeeld het volgende opgeven in het dialoogvenster Uitvoeren om de op dat moment actieve kopie van NVDA af te sluiten:

    nvda -q

Er zijn commandoregel-opties die een lange en een korte notatie hebben, terwijl andere alleen een lange notatie hebben.
De opties met een korte notatie kunnen als volgt worden gecombineerd: 

| . {.hideHeaderRow} |.|
|---|---|
|nvda -mc CONFIGPATH |Hiermee  start NVDA terwijl opstartgeluid en melding uit staat, en met de opgegeven configuratie|
|nvda -mc CONFIGPATH --disable-addons |hetzelfde als hierboven, maar met uitgeschakelde add-ons|

Aan sommige commandoregelopties kunnen extra parameters worden toegevoegd, zoals het niveau van loggen of het pad naar het configuratie bestand van de gebruiker. 
Die parameters moeten achter de optie worden geplaatst en moeten daarvan gescheiden worden door een spatie wanneer het de korte notatie betreft terwijl bij de lange notatie het = teken wordt gebruikt. Voorbeelden zijn:

| . {.hideHeaderRow} |.|
|---|---|
|nvda -l 10 |Geeft NVDA opdracht te starten met log-niveau ingesteld op debug|
|nvda --log-file=c:\nvda.log |Geeft NVDA opdracht te loggen naar c:\nvda.log|
|nvda --log-level=20 -f c:\nvda.log |Geeft NVDA opdracht te starten met het log-niveau ingesteld op info en te loggen naar c:\nvda.log|

Hieronder volgen de commandoregelopties voor NVDA:

| Kort |Lang |Omschrijving|
|---|---|---|
|`-h` |`--help` |commandoregel-hulp tonen en afsluiten|
|`-q` |``--quit |De reeds actieve kopie van NVDA afsluiten.|
|`-k` |`--check-running` |Melden via afsluitcode of NVDA actief is,; 0 voor actief, 1 voor niet actief.|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |Het bestand waar log-berichten naartoe moeten worden geschreven. Logging wordt altijd uitgeschakeld als veilige modus wordt ingeschakeld.|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |Het laagste niveau gelogd bericht (debug 10, invoer/uitvoer 12, debug-melding 15, info 20, uitgeschakeld 100) Logging wordt altijd uitgeschakeld als veilige modus wordt ingeschakeld.|
|`-c CONFIGPATH` |`--config-path=CONFIGPATH` |Het pad waar alle instellingen voor NVDA worden opgeslagen. De standaardwaardewordt geforceerd ingesteld  als veilige modus wordt ingeschakeld.|
|Geen |`--lang=LANGUAGE` |de ingestelde  NVDA-taal overschrijven. Instellen naar "Windows-standaardtaal voor huidige gebruiker, "en" voor het Engels, etc.|
|`-m` |`--minimal` |Geen geluiden, geen interface, geen opstartbericht etc.|
|`-s` |`--secure` |Start NVDA in [Veilige Modus](#SecureMode)|
|Geen |`--disable-addons` |Add-ons buiten werking gesteld.|
|geen |`--debug-logging` |Loggen op Debug niveau alleen voor deze sessie inschakelen. Met deze instelling wordt elk ander niveau van loggen buiten werking gesteld ( --loglevel, -l) gegeven argument, optie niet loggen inbegrepen.|
|Geen |`--no-logging` |loggen volledig uitschakelen terwijl NVDA in gebruik is. Deze instelling kan onderdrukt worden als een logniveau ( --loglevel, -l) wordt gespecifieerd vanuit commandoregel of als debug-loggen wordt ingeschakeld.|
|Geen |`--no-sr-flag` |Verander de systeem-brede vlag voor de schermlezer niet.|
|Geen |`--install` |Installeert NVDA (de zojuist geïnstalleerde kopie wordt gestart)|
|Geen |`--install-silent` |Silently stille installatie van NVDA (de zojuist geïnstalleerde kopie wordt niet gestart)|
|Geen |`--enable-start-on-logon=True|False` |Bij het installeren NVDA [ gebruiken  voor aanmelding bij Windows](#StartAtWindowsLogon)|
|Geen |`--copy-portable-config` |Bij het installeren de portable configuratie vanaf het aangeboden pad (--config-path, -c) naar huidige gebruikersaccount kopiëren|
|Geen |`--Create-portable` |Draagbare kopie van NVDA wordt aangemaakt (waarbij de aangemaakte kopie vervolgens opstart). Het pad voor de draagbare kopie dient te worden opgegeven.|
|Geen |`--Create-portable-silent` |Draagbare kopie van NVDA wordt aangemaakt (waarbij aangemaakte kopie vervolgens niet opstart). Het pad voor de draagbare kopie dient te worden opgegeven.|
|Geen |`--portable-path=PORTABLEPATH` |Het pad waar een draagbare kopie wordt aangemaakt.|

### Systeem-brede Parameters {#SystemWideParameters}

U kunt voor NVDA enkele waarden in het systeemregister instellen die systeem-breed het gedrag van NVDA beïnvloeden.
Deze waarden worden in het register onder een van de volgende sleutels opgeslagen:

* 32-bit systeem: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* 64-bit systeem: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

De volgende waarden kunnen onder deze registersleutel worden ingesteld:

| Naam |Type |Mogelijke waarden |Beschrijving|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (standaard) om uit te schakelen, 1 om in te schakelen |Indien ingeschakeld, wordt de NVDA gebruikersconfiguratie in de lokale application data opgeslagen in plaats van de roaming application data|
|`serviceDebug` |DWORD |0 (standaard) om uit te schakelen, 1 om in te schakelen |Indien ingeschakeld, wordt [Veilige Modus](#SecureMode) mbt [beveilige schermen](#SecureScreens) buiten werking gesteld. Aangezien dit een aantal belangrijke veiligheidsrisico's met zich meebrent,wordt gebruik van deze optie ten zeerste afgeraden|
|`Veiligemodus forceren` |DWORD |0 (standaard) om uit te schakelen, 1 om in te schakelen |Indien ingeschakeld, wordt [Veilige Modus](#SecureMode) geforceerd ingeschakeld als NVDA wordt gedraaid.|

## Verdere informatie {#FurtherInformation}

Voor nadere informatie over NVDA of voor hulp kunt u terecht op de website NVDA_URL].
Hier kunt u aanvullende documentatie vinden, technische ondersteuning krijgen, maar ook ervaringen en kennis uitwisselen met andere gebruikers en ontwikkelaars.
U vindt er ook informatie over de nieuwste ontwikkelingen en verbeteringen van het programma.

