# Nyheder i NVDA

## 2024.3

Tilføjelsescenteret vil nu give dig besked, hvis der er tilgængelige opdateringer til tilføjelser ved opstart af NVDA.

Der er nu muligheder for at anvende Unicode-normalisering til tale- og punktskriftoutput.
Dette kan være nyttigt, når man læser tegn, som en bestemt talesyntese eller punktskriftstabel ikke genkender, og som har et kompatibelt alternativ, som de fede og kursiverede tegn, der ofte bruges på sociale medier.
Det muliggør også læsning af ligninger i Microsoft Words ligningseditor.

Help Tech Activator Pro punktdisplays understøttes nu.

Udefinerede kommandoer er blevet tilføjet til at rulle musehjulet vertikalt og horisontalt.

Der er flere fejlrettelser, især for Windows 11 Emoji-panelet og udklipshistorik.
For web-browsere er der rettelser til rapportering af fejlmeddelelser, figurer, billedtekster, navne for tabeller og check boxe/radioknapper, der udgør menupunkter.

LibLouis er blevet opdateret og tilføjet nye punkttabeller for kyrillisk serbisk, jiddisch, flere gamle sprog, tyrkisk og det internationale fonetiske alfabet.
eSpeak er blevet opdateret og tilføjet understøttelse af Karakalpak-sproget.
Unicode CLDR er også blevet opdateret.

### Nye funktioner

* Nye tastaturkommandoer:
  * Tilføjede udefinerede kommandoer til vertikal og horisontal rulling af musehjulet for at forbedre navigationen på websider og apps med dynamisk indhold, såsom Dism++. (#16462, @Cary-Rowen)
* Tilføjet understøttelse af Unicode-normalisering til tale- og punktskriftoutput. (#11570, #16466 @LeonarddeR).
  * Dette kan være nyttigt, når man læser tegn, som en bestemt talesyntese eller punktskriftstabel ikke genkender, og som har et kompatibelt alternativ, som de fede og kursiverede tegn, der ofte bruges på sociale medier.
  * Det muliggør også læsning af ligninger i Microsoft Words ligningseditor. (#4631)
  * Du kan aktivere denne funktionalitet for både tale og punktskrift i deres respektive indstillingskategorier i NVDA's indstillingsdialog.
* Som standard vil du efter NVDA-opstart blive underrettet, hvis der er tilgængelige opdateringer til tilføjelser. (#15035)
  * Dette kan deaktiveres i kategorien "Tilføjelsescenter" i indstillingerne.
  * NVDA tjekker dagligt for opdateringer til tilføjelser.
  * Kun opdateringer inden for samme kanal vil blive tjekket (f.eks. installerede beta-tilføjelser vil kun give besked om opdateringer i beta-kanalen).
* Tilføjet understøttelse af Help Tech Activator Pro displays. (#16668)

### Ændringer

* Komponentopdateringer:
  * eSpeak NG er blevet opdateret til 1.52-dev commit `54ee11a79`. (#16495)
    * Tilføjet nyt sprog Karakalpak.
  * Opdateret Unicode CLDR til version 45.0. (#16507, @OzancanKaratas)
  * Opdateret fast_diff_match_patch (brugt til at registrere ændringer i terminaler og andet dynamisk indhold) til version 2.1.0. (#16508, @codeofdusk)
  * Opdateret LibLouis punktskriftoversætter til [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0). (#16652, @codeofdusk)
    * Nye punkttabeller:
      * Kyrillisk serbisk.
      * Jiddisch.
      * Flere gamle sprog: Bibelsk hebraisk, akkadisk, syrisk, ugaritisk og translittereret kileskrift.
      * Tyrkisk grad 2. (#16735)
      * Internationalt fonetisk alfabet. (#16773)
  * Opdateret NSIS til 3.10 (#16674, @dpy013)
  * Opdateret markdown til 3.6 (#16725, @dpy013)
  * Opdateret nh3 til 0.2.17 (#16725, @dpy013)
* Den alternative punktskrift input-tabel er nu den samme som den alternative output-tabel, som er Unified English Braille Code grad 1. (#9863, @JulienCochuyt, @LeonarddeR)
* NVDA vil nu rapportere figurer uden tilgængelige underelementer, men med et navn eller en beskrivelse. (#14514)
* Når der læses linjevis i gennemsynstilstand, rapporteres "Billedtekst" ikke længere på hver linje af en lang figur- eller tabelbilledtekst. (#14874)
* I Python-konsollen vil den sidste ikke-udførte kommando ikke længere gå tabt, når man bevæger sig i inputhistorikken. (#16653, @CyrilleB79)
* Et unikt anonymt ID sendes nu som en del af den valgfrie NVDA-brugsstatistik. (#16266)
* Som standard vil en ny mappe blive oprettet, når der laves en flytbar kopi.
En advarselsbesked vil informere dig, hvis du forsøger at skrive til en mappe, der ikke er tom. (#16686)

### Fejlrettelser

* Windows 11 rettelser:
  * NVDA vil ikke længere se ud til at sidde fast, når udklipshistorikken og emoji-panelet lukkes. (#16346, #16347, @josephsl)
  * NVDA vil igen annoncere synlige kandidater, når IME-interface åbnes. (#14023, @josephsl)
  * NVDA vil ikke længere annoncere "udklipshistorik" to gange, når der navigeres gennem emoji-panelmenuen. (#16532, @josephsl)
  * NVDA vil ikke længere afbryde tale og punktskrift, når der gennemgås kaomoji'er og symboler i emoji-panelet. (#16533, @josephsl)
* Web-browserrettelser:
  * Fejlmeddelelser refereret med `aria-errormessage` rapporteres nu i Google Chrome og Mozilla Firefox. (#8318)
  * Hvis til stede, vil NVDA nu bruge `aria-labelledby` til at give tilgængelige navne til tabeller i Mozilla Firefox. (#5183)
  * NVDA annoncerer korrekt radio- og check box menuemner, når man første gang går ind i undermenuer i Google Chrome og Mozilla Firefox. (#14550)
  * NVDAs søgefunktionalitet i gennemsynstilstand er nu mere præcis, når siden indeholder emojis. (#16317, @LeonarddeR)
  * I Mozilla Firefox rapporterer NVDA nu korrekt det aktuelle tegn, ord og linje, når markøren er ved indsætningspunktet ved slutningen af en linje. (#3156, @jcsteh)
  * Google Chrome går ikke længere ned, hvis der lukkes et vindue eller browseren afsluttes. (#16893)
* NVDA vil korrekt annoncere autoudfyldningsforslag i Eclipse og andre Eclipse-baserede miljøer på Windows 11. (#16416, @thgcode)
* Forbedret pålidelighed af automatisk tekstoplæsning, især i terminalapplikationer. (#15850, #16027, @Danstiv)
* Nulstilling til fabriksindstillingerne vil nu konsekvent virke. (#16755, @Emil-18)
* NVDA vil korrekt annoncere ændringer i markeringen, når der redigeres en celles tekst i Microsoft Excel. (#15843)
* I applikationer, der bruger Java Access Bridge, vil NVDA nu korrekt læse den sidste tomme linje af en tekst i stedet for at gentage den foregående linje. (#9376, @dmitrii-drobotov)
* I LibreOffice Writer (version 24.8 og nyere), når du skifter tekstformatering (fed, kursiv, understreget, nedsænket/hævet skrift, justering) ved hjælp af den tilsvarende tastaturgenvej, annoncerer NVDA den nye formateringsattribut (f.eks. "Fed til", "Fed fra"). (#4248, @michaelweghorn)
* Når du navigerer med piletasterne i tekstbokse i applikationer, der bruger UI Automation, rapporterer NVDA ikke længere nogle gange det forkerte tegn, ord osv. (#16711, @jcsteh)
* Når du indsætter i Windows 10/11's lommeregner, rapporterer NVDA nu korrekt det fulde indsatte tal. (#16573, @TristanBurchett)
* Tale er ikke længere stille, efter at have frakoblet og genforbundet til en fjernskrivebordssession. (#16722, @jcsteh)
* Understøttelse tilføjet for tekstlæsningskommandoer til et objekts navn i Visual Studio Code. (#16248, @Cary-Rowen)
* Afspilning af NVDA-lyde fejler ikke længere på en mono lydenhed. (#16770, @jcsteh)
* NVDA vil rapportere adresser, når der bevæges gennem Til/CC/BCC-felter i outlook.com / Modern Outlook. (#16856)
* NVDA håndterer nu fejl ved installation af tilføjelser mere elegant. (#16704)

### Ændringer for udviklere

* NVDA bruger nu Ruff i stedet for flake8 til linting. (#14817)
* Rettet NVDA's build-system, så det fungerer korrekt med Visual Studio 2022 version 17.10 og nyere. (#16480, @LeonarddeR)
* En fast bredde-skrifttype bruges nu i logviseren og i NVDA's Python-konsol, så markøren forbliver i samme kolonne under lodret navigation. Dette er især nyttigt for at læse fejlplaceringsmarkører i tracebacks. (#16321, @CyrilleB79)
* Understøttelse af brugerdefinerede punktoversættelsestabeller er tilføjet. (#3304, #16208, @JulienCochuyt, @LeonarddeR)
  * Tabeller kan leveres i mappen `brailleTables` i en tilføjelsespakke.
  * Metadata om tabeller kan tilføjes i en valgfri `brailleTables`-sektion i tilføjelsesmanifestet eller til en `.ini`-fil med samme format, som findes i brailleTables-undermappen i scratchpad-mappen.
  * Se venligst afsnittet om [punktoversættelsestabeller i udviklerguiden](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#BrailleTables) for flere detaljer.
* Når en `gainFocus`-hændelse køes med et objekt, der har en gyldig `focusRedirect`-egenskab, holdes objektet, som peges på af `focusRedirect`-egenskaben, nu af `eventHandler.lastQueuedFocusObject` i stedet for det oprindeligt køede objekt. (#15843)
* NVDA vil logge sin eksekverbare arkitektur (x86) ved opstart. (#16432, @josephsl)
* `wx.CallAfter`, som er pakket ind i `monkeyPatches/wxMonkeyPatches.py`, inkluderer nu korrekt `functools.wraps`-angivelse. (#16520, @XLTechie)
* Der er et nyt modul til planlægning af opgaver `utils.schedule`, som bruger pip-modulet `schedule`. (#16636)
  * Du kan bruge `scheduleThread.scheduleDailyJobAtStartUp` til automatisk at planlægge en opgave, der udføres, når NVDA starter, og hver 24. time derefter. Opgaver planlægges med en forsinkelse for at undgå konflikter.
  * `scheduleThread.scheduleDailyJob` og `scheduleJob` kan bruges til at planlægge opgaver på brugerdefinerede tidspunkter, hvor en `JobClashError` vil blive udløst ved en kendt konflikt i opgaveplanlægningen.
* Det er nu muligt at oprette app-moduler til apps, der er vært for Edge WebView2 (msedgewebview2.exe)-kontroller. (#16705, @josephsl)

## 2024.2

Der er en ny funktion kaldet lydopdeling. Funktionen gør det muligt at have NVDA-lyde i én kanal (f.eks. venstre), mens lyde fra alle andre programmer udsendes i den anden kanal (f.eks. højre).

Der er nye kommandoer til ændring af ringen af talesynteseindstillinger, hvilket giver brugerne mulighed for at springe til den første eller sidste indstilling, og for at øge eller mindske den aktuelle indstilling med større trin. Der er også nye hurtignavigationskommandoer, der gør det muligt for brugere at tilknytte tastetryk til hurtigt at hoppe mellem: afsnit, lodret justeret afsnit, tekst med samme typografi, tekst med en anderledes typografi, menuemne, skifteknap, behandlingslinje, figur og matematisk formel.

Der er mange nye punktskriftsfunktioner og fejlrettelser. En ny punktskrifttilstand kaldet "vis taleoutput" er blevet tilføjet. Når den er aktiv, viser punktdisplayet, hvad NVDA siger. Der er også tilføjet understøttelse for punktdisplays BrailleEdgeS2, BrailleEdgeS3. LibLouis blev opdateret, og tilføjede nye detaljerede (med store bogstaver angivet) hviderussiske og ukrainske punktskriftstabeller, en punkttabel for Lao, og en spansk tabel til læsning af græske tekster.

eSpeak blev opdateret med tilføjelsen af det nye sprog Tigrinya.

Der er mange mindre fejlrettelser for programmer, såsom Thunderbird, Adobe Reader, webbrowsere, Nudi og Geekbench.

### Nye funktioner

* Nye tastaturkommandoer:
  * Ny hurtignavigationskommando `p` til at hoppe til næste/forrige tekstafsnit i gennemsynstilstand. 
  * Nye ikke-tildelte hurtignavigationskommandoer, som kan bruges til at hoppe til næste/forrige:
    * figur
    * lodret justeret afsnit
    * menupunkt
    * skifteknap
    * behandlingslinje
    * matematisk formel
    * tekst med samme typografi
    * tekst med en anden typografi
  * Tilføjede kommandoer til at springe til første, sidste, frem og tilbage gennem indstillingsværdier i ringen for talesynteseindstillinger.
    * Skift til første og sidste værdi for den aktuelle indstilling i ringen af talesynteseindstillinger. Denne har ingen tildelt kommando.
    * Formindske og forøge den aktuelle indstilling i ringen af talesynteseindstillinger med større trin:
      * Desktop: `NVDA+Ctrl+sideOp` eller `NVDA+Ctrl+sideNed`
      * Laptop: `NVDA+Ctrl+Shift+sideOp` eller `NVDA+Ctrl+Shift+sideNed`
  * Tilføjet en ny ikke-tildelt kommando til at skifte rapportering af figurer og billedtekster.
  
* Punktskrift:
  * Tilføjet support for BrailleEdgeS2, BrailleEdgeS3.
  * En ny punktskrifttilstand kaldet "vis taleoutput" er blevet tilføjet.
    * Når aktiv, viser dit punktdisplay, hvad NVDA siger.
    * Kan aktiveres ved at trykke `NVDA+alt+t`, eller fra punktskriftsindstillingsdialogen.
    
* Lydopdeling:
  * Gør det muligt at dele NVDA-lyde i én kanal (f.eks. venstre) mens lyde fra alle andre programmer udsendes i den anden kanal (f.eks. højre).
  * Aktiveres med `NVDA+alt+s`.
  
* Rapportering af række- og kolonneoverskrifter understøttes nu i redigerbare HTML-elementer med indhold.
* Tilføjet muligheden for at deaktivere rapportering af figurer og billedtekster i indstillinger for dokumentformatering.
* I Windows 11 vil NVDA annoncere meddelelser fra stemmeindtastning og foreslåede handlinger, herunder det øverste forslag, når data som telefonnumre kopieres til udklipsholderen (Windows 11 2022-opdatering og senere).
* NVDA kan holde lydenheden i gang efter at tale er stoppet, for at forhindre at starten af næste tale bliver afbrudt med nogle lydenheder som Bluetooth-hovedtelefoner.
* HP Secure Browser er nu understøttet.

### Ændringer

* Tilføjelsescenter:
  * Den mindste og den sidst testede NVDA-version for en tilføjelse vises nu i området "andre detaljer".
  * Handlingen for fællesskabets anmeldelser vil være tilgængelig i alle faner i centeret.
  
* Komponentopdateringer:
  * Opdateret LibLouis punktskriftsoversætter til 3.29.0.
    * Tilføjet nye detaljerede (med store bogstaver angivet) hviderussiske og ukrainske punktskriftstabeller.
    * Ny spansk tabel til læsning af græske tekster.
    * Ny tabel for Lao Niveau 1.
  * eSpeak NG er blevet opdateret til 1.52-dev commit `cb62d93fd7`.
    * Tilføjet nyt sprog Tigrinya.
    
* Ændret flere kommandoer for BrailleSense-enheder for at undgå konflikter med tegn fra den franske punktskriftstabel.
  * `alt+venstre pil` er nu tildelt `punkt2+punkt7+mellemrum`.
  * `alt+højre pil` er nu tildelt `punkt5+punkt7+mellemrum`.
  * `alt+pil op` er nu tildelt `punkt2+punkt3+punkt7+mellemrum`.
  * `alt+pil ned` er nu tildelt `punkt5+punkt6+punkt7+mellemrum`.
  
* Prikker, der almindeligvis bruges i indholdsfortegnelser, rapporteres ikke længere på lave tegnsætningsniveauer.

### Fejlrettelser

* Windows 11-rettelser:
  * NVDA vil igen oplyse forslag til hardwaretastaturindtastning.
  * I version 24H2 (2024-opdatering og Windows Server 2025) kan mus og berøringsinteraktion bruges i hurtige indstillinger.
  
* Tilføjelsescenter:
  * Når der trykkes på `ctrl+tab`, flyttes fokus korrekt til den nye aktuelle faneoverskrift.
  * Hvis filer i NVDAs cache ikke er korrekte, vil NVDA ikke længere konstant genstarte.
  
* Rettelser for Chromium-baserede browsere, når de bruges med UIA:
  * Rettet fejl, der forårsagede, at NVDA sad fast.
  * Backspace-tasten virker nu korrekt i Gmail-log-ind-felter.
  
* Backspace virker nu korrekt, når Nudi 6.1 bruges med NVDA's indstilling "Håndtér tastetryk fra andre programmer" aktiveret.
* Rettet en fejl, hvor lydkoordinater ville blive afspillet, mens applikationen er i dvaletilstand, når "Afspil lydkoordinater, når musen bevæger sig" er aktiveret.
* I Adobe Reader ignorerer NVDA ikke længere alternativ tekst, der benyttes i formularer i PDF'er.
* Rettet en fejl, der forårsagede, at NVDA ikke kunne læse båndet og indstillingerne i Geekbench.
* Rettet et sjældent tilfælde, hvor gemning af konfigurationen kunne fejle, når NVDA gemmer alle profiler.
* I Firefox og Chromium-baserede browsere vil NVDA korrekt gå ind i fokus-tilstand, når der trykkes enter, når man er placeret i en punktopstilling (med tal og punkttegn) i redigerbart indhold.
* Kolonnetilstandsændring rapporteres automatisk, når kolonner vælges til visning i Thunderbirds meddelelsesliste.
* Kommandolinjeparametre `-h`/`--help` virker nu igen.
* NVDAs understøttelse for PoEdit version 3.4 eller nyere fungerer nu igen korrekt, hvis du oversætter til et sprog med én eller flere flertalsformer (f.eks. kinesisk eller polsk).

### Ændringer for udviklere

* Instansiering af `winVersion.WinVersion`-objekter med ukendte Windows-versioner over 10.0.22000, såsom 10.0.25398, returnerer nu "Windows 11 unknown" i stedet for "Windows 10 unknown" som versionsnavn.
* Gør AppVeyor-byggeprocessen nemmere for NVDA-forks ved at tilføje konfigurerbare variabler i `appveyor.yml` til at deaktivere eller ændre NV Access-specifikke dele af build-scripts.
* Tilføjet et "how-to"-dokument, der forklarer processen med at bygge NVDA-forks på AppVeyor.



## 2017.4

Højdepunkter i denne version inkluderer mange fejlrettelser og forbedringer til websupport, herunder gennemsynstilstand for webdialoger som standard, bedre rapportering af feltgruppelabels i gennemsynstilstand, understøttelse af nye Windows 10-teknologier som Windows Defender Application Guard og Windows 10 på ARM64, samt automatisk rapportering af skærmretning og batteristatus.
Bemærk venligst, at denne version af NVDA ikke længere understøtter Windows XP eller Windows Vista. Den minimale krav til NVDA er nu Windows 7 med Service Pack 1.

### Nye funktioner

* I gennemsynstilstand er det nu muligt at springe til slutningen/til starten af landemærker ved hjælp af kommandoerne spring til slutningen/begyndelsen af beholder (komma/skift+komma). (#5482)
* I Firefox, Chrome og Internet Explorer inkluderer hurtig navigation til redigeringsfelter og formularfelter nu redigerbart righoldigt tekstindhold (dvs. contentEditable). (#5534)
* I webbrowsere kan elementlisten nu vise formularfelter og knapper. (#588)
* Indledende understøttelse af Windows 10 på ARM64. (#7508)
* Tidlig understøttelse af læsning og interaktiv navigation af matematisk indhold for Kindle-bøger med tilgængelig matematik. (#7536)
* Tilføjet understøttelse af Azardi e-bogslæser. (#5848)
* Versionsinformation for tilføjelser rapporteres nu ved opdatering. (#5324)
* Tilføjet nye kommandolinjeparametre for at oprette en bærbar kopi af NVDA. (#6329)
* Understøttelse af Microsoft Edge, der kører inden for Windows Defender Application Guard i Windows 10 Fall Creators Update. (#7600)
* Hvis NVDA kører på en bærbar eller tablet, vil den nu rapportere, når en oplader er tilsluttet/frakoblet, og når skærmretningen ændres. (#4574, #4612)
* Nyt sprog: Makedonsk.
* Nye punktskrift oversættelsestabeller: Kroatisk grad 1, Vietnamesisk grad 1. (#7518, #7565)
* Understøttelse af Actilino punktdisplay fra Handy Tech er tilføjet. (#7590)
* Punktskriftinput for Handy Tech punktdisplays understøttes nu. (#7590)

### Ændringer

* Den minimale understøttede operativsystem for NVDA er nu Windows 7 Service Pack 1, eller Windows Server 2008 R2 Service Pack 1. (#7546)
* Webdialoger i Firefox og Chrome-webbrowsere bruger nu automatisk gennemsynstilstand, medmindre de er inden for en webapplikation. (#4493)
* I gennemsynstilstand meddeler tabulering og bevægelse med hurtige navigationskommandoer ikke længere, at der hoppes ud af beholdere som lister og tabeller, hvilket gør navigation mere effektiv. (#2591)
* I gennemsynstilstand for Firefox og Chrome meddeles navnet på formularfeltgrupper nu, når man bevæger sig ind i dem med hurtig navigation eller ved tabulering. (#3321)
* I gennemsynstilstand inkluderer hurtig navigationskommandoen for indlejrede objekter (o og skift+o) nu også lyd- og videoelementer samt elementer med aria rollerne applikation og dialog. (#7239)
* Espeak-ng er blevet opdateret til 1.49.2, hvilket løser nogle problemer med at producere frigivelsesbygger. (#7385, #7583)
* Ved tredje aktivering af kommandoen 'læs statuslinje', kopieres dens indhold til udklipsholderen. (#1785)
* Når man tildeler kommandoer til taster på en Baum-enhed, kan man begrænse dem til modellen af det anvendte punktdisplay (f.eks. VarioUltra eller Pronto). (#7517)
* Genvejstasten for filterfeltet i elementlisten i gennemsynstilstand er ændret fra alt+f til alt+e. (#7569)
* En ikke-tilknyttet kommando er blevet tilføjet til gennemsynstilstand for at skifte inklusionen af layouttabeller til og fra dynamisk. Du kan finde denne kommando i kategorien Gennemsynstilstand i dialogboksen Indtastningskommandoer. (#7634)
* Liblouis-punktskriftoversætteren er opgraderet til 3.3.0. (#7565)
* Genvejstasten for regulært udtryk-radio-knappen i ordbogsdialogboksen er ændret fra alt+r til alt+e. (#6782)
* Stemmediktatfiler er nu versionsstyrede og er blevet flyttet til mappen 'speechDicts/voiceDicts.v1'. (#7592)
* Versionsstyrede filer (brugeropsætning, stemmeordbøger) ændringer gemmes ikke længere, når NVDA køres fra en launcher. (#7688)
* Braillino, Bookworm og Modular (med gammel firmware) punktdisplays fra Handy Tech understøttes ikke længere ud af boksen. Installer Handy Tech Universal Driver og NVDA-tilføjelse for at bruge disse displays. (#7590)

### Fejlrettelser

* Links angives nu i punktskrift i applikationer som Microsoft Word. (#6780)
* NVDA bliver ikke længere mærkbart langsommere, når mange faner er åbne i enten Firefox eller Chrome-webbrowsere. (#3138)
* Cursorrouting for MDV Lilli punktdisplay flytter ikke længere forkert én punktcelle fremad. (#7469)
* I Internet Explorer og andre MSHTML-dokumenter understøttes HTML5-krævet-attributten nu for at angive den krævede tilstand for et formularfelt. (#7321)
* Punktdisplays opdateres nu, når man indtaster arabiske tegn i et venstrejusteret WordPad-dokument. (#511)
* Tilgængelige labels for kontroller i Mozilla Firefox rapporteres nu mere konsekvent i gennemsynstilstand, når labelen ikke fremstår som indhold i sig selv. (#4773)
* På Windows 10 Creators Update kan NVDA igen tilgå Firefox efter en genstart af NVDA. (#7269)
* Ved genstart af NVDA med Mozilla Firefox i fokus vil gennemsynstilstand igen være tilgængelig, selvom du muligvis skal skifte væk med alt+tab og tilbage igen. (#5758)
* Det er nu muligt at tilgå matematikindhold i Google Chrome på et system uden Mozilla Firefox installeret. (#7308)
* Operativsystemet og andre applikationer bør være mere stabile lige efter installationen af NVDA, før genstart, sammenlignet med installationer af tidligere NVDA-versioner. (#7563)
* Når man bruger en indholdsgenkendelseskommando (f.eks. NVDA+r), rapporterer NVDA nu en fejlmeddelelse i stedet for ingenting, hvis navigatorobjektet er forsvundet. (#7567)
* Baglæns rulning er blevet rettet for Freedom Scientific punktdisplays, der har en venstre bumperstang. (#7713)

### Ændringer for udviklere

* "scons tests" kontrollerer nu, at oversættelige strenge har oversætterkommentarer. Du kan også køre dette alene med "scons checkPot". (#7492)
* Der er nu et nyt extensionPoints-modul, der giver en generisk ramme for at muliggøre kodeudvidelse på specifikke punkter i koden. Dette gør det muligt for interesserede parter at registrere for at blive underrettet, når en handling sker (extensionPoints.Action), for at ændre en bestemt slags data (extensionPoints.Filter) eller for at deltage i beslutningen om, hvorvidt noget vil blive gjort (extensionPoints.Decider). (#3393)
* Du kan nu registrere for at blive underrettet om konfigurationsprofilskift via config.configProfileSwitched Action. (#3393)
* Punktskriftkommandoer, der emulerer systemtastatur-modifikatortaster (såsom control og alt), kan nu kombineres med andre emulerede systemtastaturtaster uden eksplicit definition. (#6213)
 * For eksempel, hvis du har en tast på dit display bundet til alt-tasten og en anden display-tast til ned-pilen, vil kombination af disse taster resultere i emulering af alt+ned-pilen.
* Klassen braille.BrailleDisplayGesture har nu en ekstra model-egenskab. Hvis den angives, genererer et tryk på en tast en ekstra, modelspecifik kommando-identifikator. Dette gør det muligt for en bruger at tildele kommandoer begrænset til en specifik punktdisplaymodel.
 * Se baum-driveren som et eksempel på denne nye funktionalitet.
* NVDA kompileres nu med Visual Studio 2017 og Windows 10 SDK. (#7568)

## 2017.3

Højdepunkterne i denne version inkluderer input af forkortet punktskrift, understøttelse af de nye Windows OneCore-stemmer tilgængelige på Windows 10, indbygget understøttelse af Windows 10 OCR, og mange væsentlige forbedringer vedrørende punktskrift og internettet.

### Nye funktioner

* En punktskriftsindstilling er blevet tilføjet til at "vise meddelelser på ubestemt tid". (#6669)
* I Microsoft Outlook-meddelelseslister rapporterer NVDA nu, om en meddelelse er markeret. (#6374)
* I Microsoft PowerPoint rapporteres den præcise type af en form, når man redigerer en slide (såsom trekant, cirkel, video eller pil), frem for blot "form". (#7111)
* Matematiske indhold (givet som MathML) understøttes nu i Google Chrome. (#7184)
* NVDA kan nu tale ved brug af de nye Windows OneCore-stemmer (også kendt som Microsoft Mobile-stemmer), som er inkluderet i Windows 10. Du får adgang til disse ved at vælge Windows OneCore-stemmer i NVDA's Synthesizer-dialog. (#6159)
* NVDA-brugerkonfigurationsfiler kan nu gemmes i brugerens lokale programdata-mappe. Dette aktiveres via en indstilling i registreringsdatabasen. Se "Systemomspændende Parametre" i Brugervejledningen for flere detaljer. (#6812)
* I web-browsere rapporterer NVDA nu pladsholderværdier for felter (specifikt understøttes aria-placeholder). (#7004)
* I Gennemsynstilstand for Microsoft Word er det nu muligt at navigere til stavefejl ved brug af hurtig navigation (w og shift+w). (#6942)
* Tilføjet understøttelse for datovælgerkontrollen, der findes i Microsoft Outlook Aftaledialoger. (#7217)
* Den aktuelt valgte forslag rapporteres nu i Windows 10 Mail til/cc-felterne og i søgefeltet i Windows 10-indstillingerne. (#6241)
* En lyd afspilles nu for at indikere, når forslag vises i visse søgefelter i Windows 10 (f.eks. startskærm, søgning i indstillinger, Windows 10 mail til/cc-felter). (#6241)
* NVDA rapporterer nu automatisk meddelelser i Skype for Business Desktop, såsom når nogen starter en samtale med dig. (#7281)
* NVDA rapporterer nu automatisk indkommende chatbeskeder under en Skype for Business-samtale. (#7286)
* NVDA rapporterer nu automatisk meddelelser i Microsoft Edge, såsom når en download starter. (#7281)
* Du kan nu skrive i både forkortet og uforkortet punktskrift på et punktdisplay med et punkt-tastatur. Se afsnittet om Punktskriftsinput i Brugervejledningen for flere detaljer. (#2439)
* Du kan nu indtaste Unicode punktskrift-tegn fra punkt-tastaturet på et punktdisplay ved at vælge Unicode punktskrift som inputtabel i Punktskriftindstillinger. (#6449)
* Tilføjet understøttelse for SuperBraille-punktdisplayet, der anvendes i Taiwan. (#7352)
* Nye punktskrifttabeller: Dansk 8-punkt computer punktskrift, Litauisk, Persisk 8-punkt computer punktskrift, Persisk grad 1, Slovensk 8-punkt computer punktskrift. (#6188, #6550, #6773, #7367)
* Forbedret Engelsk (U.S.) 8-punkt computer punktskrift-tabel, herunder understøttelse for punkttegn, euro-tegn og accentuerede bogstaver. (#6836)
* NVDA kan nu bruge OCR-funktionaliteten, der er inkluderet i Windows 10, til at genkende teksten i billeder eller utilgængelige applikationer. (#7361)
 * Sproget kan indstilles fra den nye Windows 10 OCR-dialog i NVDA-præferencer.
 * For at genkende indholdet af det aktuelle navigatorobjekt, tryk NVDA+r.
 * Se afsnittet om Indholdsgenkendelse i Brugervejledningen for flere detaljer.
* Du kan nu vælge, hvilken kontekstinformation der vises på et punktdisplay, når et objekt får fokus ved hjælp af den nye indstilling "Fokus kontekstpræsentation" i Punktskriftindstillinger-dialogen. (#217)
 * For eksempel kan indstillingerne "Fyld display for kontekstændringer" og "Kun når man ruller tilbage" gøre arbejdet med lister og menuer mere effektivt, da elementerne ikke kontinuerligt ændrer position på displayet.
 * Se afsnittet om indstillingen "Fokus kontekstpræsentation" i Brugervejledningen for flere detaljer og eksempler.
* I Firefox og Chrome understøtter NVDA nu komplekse dynamiske gittere, såsom regneark, hvor kun en del af indholdet kan være indlæst eller vist (specifikt understøttes aria-rowcount, aria-colcount, aria-rowindex og aria-colindex attributterne, som blev introduceret i ARIA 1.1). (#7410)

### Ændringer

* En udefineret kommando er blevet tilføjet for at genstarte NVDA efter behov. Du kan finde den i kategorien Diverse i Kommandoindstillinger-dialogen. (#6396)
* Tastaturlayoutet kan nu indstilles fra NVDA's Velkomst-dialog. (#6863)
* Mange flere kontroltyper og tilstande er blevet forkortet for punktskrift. Landemærker er også blevet forkortet. Se "Kontroltype-, Tilstands- og Landemærkeforkortelser" under Punktskrift i Brugervejledningen for en komplet liste. (#7188, #3975)
* Opdateret eSpeak NG til 1.49.1. (#7280)
* Output- og inputtabellerne i Punktskriftindstillinger-dialogen sorteres nu alfabetisk. (#6113)
* Opdateret liblouis punktskriftoversætter til 3.2.0. (#6935)
* Standardpunktskriftstabel er nu Unified English Braille Code grad 1. (#6952)
* Som standard viser NVDA nu kun de dele af kontekstinformationen, der har ændret sig på et punktdisplay, når et objekt får fokus. (#217)
 * Tidligere viste den altid så meget kontekstinformation som muligt, uanset om du har set den samme kontekstinformation før.
 * Du kan vende tilbage til den gamle opførsel ved at ændre den nye indstilling "Fokus kontekstpræsentation" i Punktskriftindstillinger-dialogen til "Altid fyld display".
* Når du bruger punktskrift, kan markøren konfigureres til at have en anden form, når den er forbundet til fokus eller gennemsyn. (#7122)
* NVDA-logoet er blevet opdateret. Det opdaterede NVDA-logo er en stiliseret blanding af bogstaverne NVDA i hvidt, på en solid lilla baggrund. Dette sikrer, at det er synligt på enhver farvebaggrund, og bruger den lilla farve fra NV Access-logoet. (#7446)

### Fejlrettelser

* Redigerbare div-elementer i Chrome har ikke længere deres etikette rapporteret som deres værdi i gennemsynstilstand. (#7153)
* At trykke på slutningen i gennemsynstilstand for et tomt Microsoft Word-dokument forårsager ikke længere en runtime-fejl. (#7009)
* Gennemsynstilstand understøttes nu korrekt i Microsoft Edge, hvor et dokument har fået tildelt en specifik ARIA-rolle som dokument. (#6998)
* I gennemsynstilstand kan du nu vælge eller fravælge til slutningen af linjen ved hjælp af shift+end, selv når markøren er på det sidste tegn i linjen. (#7157)
* Hvis en dialog indeholder en statuslinje, opdateres dialogteksten nu i punktskrift, når statuslinjen ændres. Dette betyder for eksempel, at den resterende tid nu kan læses i NVDA's "Hentning af opdatering" dialog. (#6862)
* NVDA vil nu annoncere ændringer i valg for visse Windows 10-rullelister, såsom AutoPlay i Indstillinger. (#6337).
* Meningsløs information annonceres ikke længere, når man går ind i Møde-/Aftaleskabelsesdialoger i Microsoft Outlook. (#7216)
* Bip for uspecifikke statuslinjedialoger såsom opdateringstjekker afspilles kun, når statuslinjeoutput er konfigureret til at inkludere bip. (#6759)
* I Microsoft Excel 2003 og 2007 rapporteres celler igen, når man bruger piletasterne til at navigere rundt i et regneark. (#7243)
* I Windows 10 Creators Update og senere aktiveres gennemsynstilstand igen automatisk, når du læser e-mails i Windows 10 Mail. (#7289)
* På de fleste punktdisplays med et punkt-tastatur sletter punkt 7 nu den sidst indtastede punktskriftcelle eller tegn, og punkt 8 trykker på enter-tasten. (#6054)
* I redigerbar tekst, når markøren flyttes (f.eks. med piletasterne eller backspace), er NVDA's talte feedback nu mere præcis i mange tilfælde, især i Chrome og terminalapplikationer. (#6424)
* Indholdet af signaturredigeringsværktøjet i Microsoft Outlook 2016 kan nu læses. (#7253)
* I Java Swing-applikationer forårsager NVDA ikke længere, at applikationen undertiden går ned, når man navigerer i tabeller. (#6992)
* I Windows 10 Creators Update annoncerer NVDA ikke længere toastmeddelelser flere gange. (#7128)
* I startmenuen i Windows 10 forårsager tryk på enter for at lukke startmenuen efter en søgning ikke længere, at NVDA annoncerer søgetekst. (#7370)
* At udføre hurtig navigation til overskrifter i Microsoft Edge er nu betydeligt hurtigere. (#7343)
* I Microsoft Edge springer navigation i gennemsynstilstand ikke længere store dele af visse websider som f.eks. Wordpress 2015-temaet over. (#7143)
* I Microsoft Edge er landemærker korrekt lokaliseret på andre sprog end engelsk. (#7328)
* Punktskrift følger nu korrekt valget, når man vælger tekst ud over displayets bredde. For eksempel, hvis du vælger flere linjer med shift+pil ned, viser punktskrift nu den sidste linje, du har valgt. (#5770)
* I Firefox rapporterer NVDA ikke længere fejlagtigt "sektion" flere gange, når man åbner detaljer for en tweet på twitter.com. (#5741)
* Tabellens navigationskommandoer er ikke længere tilgængelige for layouttabeller i Gennemsynstilstand, medmindre rapportering af layouttabeller er aktiveret. (#7382)
* I Firefox og Chrome springer Gennemsynstilstandens tabellenavigationskommandoer nu over skjulte tabelceller. (#6652, #5655)

### Ændringer for udviklere

* Tidsstempler i loggen inkluderer nu millisekunder. (#7163)
* NVDA skal nu bygges med Visual Studio Community 2015. Visual Studio Express understøttes ikke længere. (#7110)
 * Windows 10-værktøjer og SDK er nu også påkrævet, hvilket kan aktiveres, når Visual Studio installeres.
 * Se afsnittet om installerede afhængigheder i readme for flere detaljer.
* Understøttelse af indholdsgenkendere såsom OCR og værktøjer til billedbeskrivelse kan nemt implementeres ved brug af den nye contentRecog-pakke. (#7361)
* Python json-pakken er nu inkluderet i NVDA's binære builds. (#3050)

## 2017.2

Højdepunkterne i denne version inkluderer fuld understøttelse af lydstyrkenedsættelse i Windows 10 Creators Update, rettelser af flere problemer med valg i gennemsynstilstand, herunder problemer med at vælge alt, betydelige forbedringer i understøttelsen af Microsoft Edge og forbedringer på internettet, såsom indikering af elementer markeret som aktuelle (ved brug af aria-current).

### Nye funktioner

* Cellegrænseoplysninger kan nu rapporteres i Microsoft Excel ved brug af NVDA+f. (#3044)
* I web-browsere angiver NVDA nu, når et element er markeret som aktuelt (specifikt ved brug af aria-current attributten). (#6358)
* Automatisk sprogskift understøttes nu i Microsoft Edge. (#6852)
* Tilføjet understøttelse for Windows Calculator på Windows 10 Enterprise LTSB (Long-Term Servicing Branch) og Server. (#6914)
* At udføre kommandoen "læs aktuel linje" tre gange hurtigt vil stave linjen med bogstavbeskrivelser. (#6893)
* Nyt sprog: Burmesisk.
* Unicode pil op og pil ned samt brøksymboler tales nu korrekt. (#3805)

### Ændringer

* Når man navigerer med simpel gennemsyn i applikationer, der bruger UI Automation, ignoreres flere overflødige objekter nu, hvilket gør navigationen nemmere. (#6948, #6950)

### Fejlrettelser

* Menuemner på websider kan nu aktiveres i gennemsynstilstand. (#6735)
* Tryk på escape, mens dialogboksen "Bekræft sletning" for konfigurationsprofilen er aktiv, lukker nu dialogboksen. (#6851)
* Rettet nogle nedbrud i Mozilla Firefox og andre Gecko-applikationer, hvor multiproces-funktionen er aktiveret. (#6885)
* Rapporteringen af baggrundsfarve i skærmgennemsyn er nu mere præcis, når tekst blev tegnet med en gennemsigtig baggrund. (#6467)
* Forbedret understøttelse af kontrolbeskrivelser leveret på websider i Internet Explorer 11 (specifikt understøttelse af aria-describedby inden for iframes og når flere IDs er angivet). (#5784)
* I Windows 10 Creators Update fungerer NVDA's lydstyrkenedsættelse igen som i tidligere Windows-udgivelser; dvs. Nedsæt ved tale og lyde, altid nedsæt og ingen nedsættelse er alle tilgængelige. (#6933)
* NVDA vil ikke længere undlade at navigere til eller rapportere visse (UIA) kontroller, hvor en tastaturgenvej ikke er defineret. (#6779)
* To tomme mellemrum tilføjes ikke længere i oplysninger om tastaturgenveje for visse (UIA) kontroller. (#6790)
* Visse kombinationer af taster på HIMS-displays (f.eks. space+dot4) fejler ikke længere intermitterende. (#3157)
* Rettet et problem ved åbning af en seriel port på systemer, der bruger visse andre sprog end engelsk, som forårsagede, at tilslutning til punktskriftsdisplays mislykkedes i nogle tilfælde. (#6845)
* Reduceret risiko for, at konfigurationsfilen bliver beskadiget, når Windows lukkes ned. Konfigurationsfiler skrives nu til en midlertidig fil, før den faktiske konfigurationsfil erstattes. (#3165)
* Når kommandoen "læs aktuel linje" udføres to gange hurtigt for at stave linjen, bruges det korrekte sprog nu til de stavede tegn. (#6726)
* Navigation efter linje i Microsoft Edge er nu op til tre gange hurtigere i Windows 10 Creators Update. (#6994)
* NVDA annoncerer ikke længere "Web Runtime gruppering", når Microsoft Edge-dokumenter fokuseres i Windows 10 Creators Update. (#6948)
* Alle eksisterende versioner af SecureCRT understøttes nu. (#6302)
* Adobe Acrobat Reader går ikke længere ned i visse PDF-dokumenter (specifikt dem, der indeholder tomme ActualText-attributter). (#7021, #7034)
* I gennemsynstilstand i Microsoft Edge springes interaktive tabeller (ARIA-gittere) ikke længere over, når man navigerer til tabeller med t og shift+t. (#6977)
* I gennemsynstilstand fungerer shift+home korrekt efter fremadrettet valg ved at fravælge til begyndelsen af linjen som forventet. (#5746)
* I gennemsynstilstand fejler "vælg alt" (control+a) ikke længere i at vælge al tekst, hvis markøren ikke er i starten af teksten. (#6909)
* Rettet nogle andre sjældne valgproblemer i gennemsynstilstand. (#7131)

### Ændringer for udviklere

* Kommandolinjeargumenter behandles nu med Pythons argparse-modul i stedet for optparse. Dette tillader visse muligheder som -r og -q at blive håndteret eksklusivt. (#6865)
* core.callLater køer nu callbacken til NVDA's hovedkø efter den givne forsinkelse, i stedet for at vække kernen og udføre den direkte. Dette stopper mulige frysninger på grund af, at kernen ved et uheld går i dvale efter behandling af en callback, midt i et modalt opkald, såsom visning af en meddelelsesboks. (#6797)
* InputGesture.identifiers-ejendommen er ændret, så den ikke længere normaliseres. (#6945)
 * Underklasser behøver ikke længere normalisere identifiers, før de returneres fra denne ejendom.
 * Hvis du ønsker normaliserede identifiers, er der nu en InputGesture.normalizedIdentifiers-ejendom, der normaliserer identifiers returneret af identifiers-ejendommen.
* InputGesture.logIdentifier-ejendommen er nu forældet. Kaldere bør bruge InputGesture.identifiers[0] i stedet. (#6945)
* Fjernet noget forældet kode:
 * `speech.REASON_*`-konstanter: `controlTypes.REASON_*` bør bruges i stedet. (#6846)
 * `i18nName` for syntheindstillinger: `displayName` og `displayNameWithAccelerator` bør bruges i stedet. (#6846, #5185)
 * `config.validateConfig`. (#6846, #667)
 * `config.save`: `config.conf.save` bør bruges i stedet. (#6846, #667)
* Listen over fuldførelser i autocomplete-kontekstmenuen i Python-konsollen viser ikke længere nogen objektsti, der fører frem til det sidste symbol, der fuldføres. (#7023)
* Der er nu et enhedstestningsrammeværk for NVDA. (#7026)
 * Enhedstests og infrastruktur er placeret i tests/unit-mappen. Se docstringen i tests\unit\init.py-filen for detaljer.
 * Du kan køre tests ved hjælp af "scons tests". Se afsnittet "Køre Tests" i readme.md for detaljer.
 * Hvis du indsender en pull-anmodning for NVDA, bør du først køre testsene og sikre dig, at de består.

## 2017.1

Højdepunkterne i denne version inkluderer rapportering af sektioner og tekstkolonner i Microsoft Word; understøttelse af læsning, navigation og annotation af bøger i Kindle til PC; og forbedret understøttelse af Microsoft Edge.

### Nye funktioner

* I Microsoft Word kan sektionstyper og sektionsnumre nu rapporteres. Dette aktiveres med indstillingen "Rapporter sidetal" i Dokumentformateringsdialogen. (#5946)
* I Microsoft Word kan tekstkolonner nu rapporteres. Dette aktiveres med indstillingen "Rapporter sidetal" i dokumentformateringsdialogen. (#5946)
* Automatisk sprogskift understøttes nu i WordPad. (#6555)
* NVDA's søgekommando (NVDA+control+f) understøttes nu i gennemsynstilstand i Microsoft Edge. (#6580)
* Hurtig navigation til knapper i gennemsynstilstand (b og shift+b) understøttes nu i Microsoft Edge. (#6577)
* Når man kopierer et ark i Microsoft Excel, huskes kolonne- og rækkeoverskrifterne. (#6628)
* Understøttelse af læsning og navigation i bøger i Kindle til PC version 1.19, herunder adgang til links, fodnoter, grafik, fremhævet tekst og brugerkommentarer. Se venligst afsnittet om Kindle til PC i NVDA Brugervejledningen for yderligere oplysninger. (#6247, #6638)
* Gennemsynstilstands tabelnavigation understøttes nu i Microsoft Edge. (#6594)
* I Microsoft Excel rapporterer kommandoen "rapportér gennemgangsmarkørens placering" (desktop: NVDA+numpadDelete, laptop: NVDA+delete) nu navnet på regnearket og celleplaceringen. (#6613)
* En mulighed er tilføjet til afslutningsdialogen for at genstarte med fejlniveau-logning. (#6689)

### Ændringer

* Den mindste blinkhastighed for punktskriftmarkøren er nu 200 ms. Hvis dette tidligere var indstillet lavere, vil det blive øget til 200 ms. (#6470)
* En check box er blevet tilføjet til punktskriftsindstillingsdialogen for at muliggøre aktivering/deaktivering af punktskriftmarkørens blinkning. Tidligere blev en værdi på nul brugt til at opnå dette. (#6470)
* Opdateret eSpeak NG (commit e095f008, 10. januar 2017). (#6717)
* På grund af ændringer i Windows 10 Creators Update er "Altid nedsæt"-tilstanden ikke længere tilgængelig i NVDA's Lydstyrkenedsættelsesindstillinger. Den er stadig tilgængelig på ældre Windows 10-udgivelser. (#6684)
* På grund af ændringer i Windows 10 Creators Update kan tilstanden "Nedsæt ved tale og lyde" ikke længere sikre, at lyden er nedsat fuldt ud, før den begynder at tale, og vil heller ikke holde lyden nedsat længe nok efter tale for at stoppe hurtig volumenændring. Disse ændringer påvirker ikke ældre Windows 10-udgivelser. (#6684)

### Fejlrettelser

* Rettet frysefejl i Microsoft Word, når der navigeres med afsnit gennem et stort dokument i gennemsynstilstand. (#6368)
* Tabeller i Microsoft Word, der er kopieret fra Microsoft Excel, behandles ikke længere som layouttabeller og ignoreres derfor ikke længere. (#5927)
* Når man forsøger at skrive i Microsoft Excel, mens man er i beskyttet visning, afspiller NVDA nu en lyd i stedet for at tale tegn, der ikke blev skrevet. (#6570)
* Tryk på escape i Microsoft Excel skifter ikke længere forkert til gennemsynstilstand, medmindre brugeren tidligere har skiftet til gennemsynstilstand eksplicit med NVDA+space og derefter gået ind i fokustilstand ved at trykke på enter på et formularfelt. (#6569) 
* NVDA fryser ikke længere i Microsoft Excel-regneark, hvor en hel række eller kolonne er flettet. (#6216)
* Rapportering af afskåret/overløbet tekst i Microsoft Excel-celler bør nu være mere præcis. (#6472)
* NVDA rapporterer nu, når en check box er skrivebeskyttet. (#6563)
* NVDA-launcheren viser ikke længere en advarselsdialog, når den ikke kan afspille logolyden på grund af manglende lydudstyr. (#6289)
* Kontroller i Microsoft Excel-båndet, der ikke er tilgængelige, rapporteres nu som sådan. (#6430)
* NVDA annoncerer ikke længere "rude", når vinduer minimeres. (#6671)
* Tastede tegn tales nu i Universal Windows Platform (UWP) apps (inklusive Microsoft Edge) i Windows 10 Creators Update. (#6017)
* Museovervågning fungerer nu på tværs af alle skærme på computere med flere skærme. (#6598)
* NVDA bliver ikke længere ubrugelig efter at have lukket Windows Media Player, mens der er fokus på en skydekontrol. (#5467)

### Ændringer for udviklere

* Profiler og konfigurationsfiler opgraderes nu automatisk for at opfylde kravene i skemamodifikationer. Hvis der opstår en fejl under opgraderingen, vises en meddelelse, konfigurationen nulstilles, og den gamle konfigurationsfil er tilgængelig i NVDA-loggen på 'Info'-niveau. (#6470)

## 2016.4

Højdepunkterne i denne udgivelse inkluderer forbedret understøttelse af Microsoft Edge; gennemsynstilstand i Windows 10 Mail-appen; og væsentlige forbedringer af NVDA's dialogbokse.

### Nye funktioner

* NVDA kan nu angive linjeindrykning ved hjælp af toner. Dette kan konfigureres ved hjælp af komboboksen "Linjeindrykningsrapportering" i NVDA's dialogboks for dokumentformatering. (#5906)
* Understøttelse af Orbit Reader 20 punktdisplay. (#6007)
* En mulighed for at åbne vinduet til talevisning ved opstart er tilføjet. Dette kan aktiveres via en check box i vinduet for talevisning. (#5050)
* Når talevisningsvinduet genåbnes, vil dets placering og dimensioner nu blive gendannet. (#5050)
* Krydsreferencer i Microsoft Word behandles nu som hyperlinks. De rapporteres som links og kan aktiveres. (#6102)
* Understøttelse af Baum SuperVario2, Baum Vario 340 og HumanWare Brailliant2 punktdisplays. (#6116)
* Indledende understøttelse af jubilæumsopdateringen af Microsoft Edge. (#6271)
* Gennemsynstilstand bruges nu, når der læses e-mails i Windows 10 Mail-appen. (#6271)
* Nyt sprog: Litauisk.

### Ændringer

* Opdateret liblouis punktoversætter til version 3.0.0. Dette inkluderer væsentlige forbedringer af Unified English Braille. (#6109, #4194, #6220, #6140)
* I tilføjelsesstyringen har knapperne Deaktiver tilføjelse og Aktiver tilføjelse nu tastaturgenveje (alt+d og alt+e). (#6388)
* Forskellige problemer med polstring og justering i NVDA's dialogbokse er løst. (#6317, #5548, #6342, #6343, #6349)
* Dokumentformateringsdialogen er justeret, så indholdet kan rulles. (#6348)
* Layoutet af dialogboksen for symboludtale er justeret, så hele dialogens bredde udnyttes til symbollisten. (#6101)
* I gennemsynstilstand i webbrowsere kan redigeringsfelter (e og shift+e) og formularfelter (f og shift+f) nu bruges til at navigere til skrivebeskyttede redigeringsfelter. (#4164)
* I NVDA's indstillinger for dokumentformatering er "Announce formatting changes after the cursor" omdøbt til "Rapporter formateringsændringer efter markøren", da det påvirker både punktskrift og tale. (#6336)
* Udseendet af NVDA's "Velkomstdialog" er justeret. (#6350)
* NVDA-dialogbokse har nu deres "ok"- og "annuller"-knapper justeret til højre i dialogen. (#6333)
* Spinkontroller bruges nu til numeriske indtastningsfelter, såsom indstillingen "Ændring af stor bogstav tonehøjde i procent" i stemmeindstillingerne. Du kan indtaste den ønskede værdi eller bruge pil op og ned for at justere værdien. (#6099)
* Måden, hvorpå IFrames (dokumenter indlejret i dokumenter) rapporteres, er gjort mere konsistent på tværs af webbrowsere. IFrames rapporteres nu som "ramme" i Firefox. (#6047)

### Fejlrettelser

* Rettet en sjælden fejl ved afslutning af NVDA, mens taleviseren er åben. (#5050)
* Billedkort gengives nu som forventet i gennemsynstilstand i Mozilla Firefox. (#6051)
* I ordbogsdialogen gemmer Enter-tasten nu de ændringer, du har foretaget, og lukker dialogen. Tidligere gjorde Enter-tasten ingenting. (#6206)
* Meddelelser vises nu i punktskrift, når inputtilstande ændres for en inputmetode (f.eks. native input/alfanumerisk, fuldt formet/halvt formet osv.). (#5892, #5893)
* Når en tilføjelse deaktiveres og derefter straks genaktiveres, genoprettes status for tilføjelsen nu korrekt til det, det var tidligere. (#6299)
* Når du bruger Microsoft Word, kan sidetalsfelter i sidehoveder nu læses. (#6004)
* Musen kan nu bruges til at flytte fokus mellem symbollisten og redigeringsfelterne i dialogboksen for symboludtale. (#6312)
* I gennemsynstilstand i Microsoft Word er et problem, der forhindrer, at elementlisten vises, når et dokument indeholder et ugyldigt hyperlink, rettet. (#5886)
* Når talevisningsvinduet lukkes via proceslinjen eller genvejstasten alt+F4, vil check boxen i NVDA-menuen nu afspejle vinduets faktiske synlighed. (#6340)
* Genindlæsning af plugins-kommandoen skaber ikke længere problemer for udløste konfigurationsprofiler, nye dokumenter i webbrowsere og skærmgennemgang. (#2892, #5380)
* I listen over sprog i NVDA's generelle indstillinger vises sprog som Aragonese nu korrekt på Windows 10. (#6259)
* Emulerede systemtastaturtaster (f.eks. en knap på et punktdisplay, der emulerer tab-tasten) præsenteres nu i det konfigurerede NVDA-sprog i inputhjælp og kommandoer for inputkommandoer. Tidligere blev de altid præsenteret på engelsk. (#6212)
* Ændring af NVDA's sprog (fra dialogboksen for generelle indstillinger) har nu ingen effekt, før NVDA genstartes. (#4561)
* Det er ikke længere muligt at efterlade mønsterfeltet tomt for en ny indtastning i taleordbogen. (#6412)
* Rettet et sjældent problem ved scanning efter serielle porte på nogle systemer, hvilket gjorde nogle punktdisplay-drivere ubrugelige. (#6462)
* I Microsoft Word læses nummererede punkter i tabelceller nu, når der navigeres efter celle. (#6446)
* Det er nu muligt at tildele kommandoer til kommandoer for Handy Tech punktdisplay-driveren i NVDA's dialogboks for inputkommandoer. (#6461)
* I Microsoft Excel rapporteres navigation til næste række nu korrekt, når du trykker på Enter eller numpadEnter under navigering i et regneark. (#6500)
* iTunes fryser ikke længere intermitterende for evigt, når gennemsynstilstand bruges til iTunes Store, Apple Music osv. (#6502)
* Rettet nedbrud i 64-bit Mozilla- og Chrome-baserede applikationer. (#6497)
* I Firefox med multi-process aktiveret fungerer gennemsynstilstand og redigerbare tekstfelter nu korrekt. (#6380)

### Ændringer for udviklere

* Det er nu muligt at levere app-moduler til eksekverbare filer, der indeholder et punktum (.). Punktummer erstattes med understregninger (_). (#5323)
* Det nye gui.guiHelper-modul indeholder værktøjer til at forenkle oprettelsen af wxPython-GUI'er, inklusive automatisk styring af afstande. Dette muliggør bedre visuelt udseende og konsistens samt gør det nemmere at oprette nye GUI'er for blinde udviklere. (#6287)

## 2016.3

Højdepunkterne i denne udgivelse inkluderer muligheden for at deaktivere individuelle tilføjelser; understøttelse af formularfelter i Microsoft Excel; væsentlige forbedringer i rapporteringen af farver; fejlrettelser og forbedringer relateret til flere punktdisplays; og rettelser og forbedringer af understøttelsen af Microsoft Word.

### Nye funktioner

* Gennemsynstilstand kan nu bruges til at læse PDF-dokumenter i Microsoft Edge i Windows 10 jubilæumsopdateringen. (#5740)
* Overstregning og dobbelt overstregning rapporteres nu, hvis det er relevant i Microsoft Word. (#5800)
* I Microsoft Word rapporteres titlen på en tabel nu, hvis en sådan er angivet. Hvis der er en beskrivelse, kan den tilgås ved hjælp af kommandoen for lang beskrivelse (NVDA+d) i gennemsynstilstand. (#5943)
* I Microsoft Word rapporterer NVDA nu positionsoplysninger, når afsnit flyttes (alt+shift+pilNed og alt+shift+pilOp). (#5945)
* I Microsoft Word rapporteres linjeafstand nu via NVDA's kommando til rapportering af formatering, når den ændres med forskellige Microsoft Word-genvejstaster, og når der navigeres til tekst med forskellig linjeafstand, hvis rapportering af linjeafstand er aktiveret i NVDA's dokumentformateringsindstillinger. (#2961)
* I Internet Explorer genkendes HTML5-strukturelementer nu. (#5591)
* Rapportering af kommentarer (såsom i Microsoft Word) kan nu deaktiveres via en check box til rapportering af kommentarer i NVDA's dialogboks for dokumentformatering. (#5108)
* Det er nu muligt at deaktivere individuelle tilføjelser i tilføjelsesstyringen. (#3090)
* Yderligere tasteopgaver er tilføjet til ALVA BC640/680-seriens punktdisplays. (#5206)
* Der er nu en kommando til at flytte punktdisplayet til det aktuelle fokus. I øjeblikket har kun ALVA BC640/680-serien en tildelt tast til denne kommando, men den kan tildeles manuelt for andre displays i dialogboksen for inputkommandoer, hvis det ønskes. (#5250)
* I Microsoft Excel kan du nu interagere med formularfelter. Du kan navigere til formularfelter ved hjælp af elementlisten eller bogstavnavigation i gennemsynstilstand. (#4953)
* Du kan nu tildele en inputkommando til at slå simpel gennemgangstilstand til/fra ved hjælp af dialogboksen for inputkommandoer. (#6173)

### Ændringer

* NVDA rapporterer nu farver ved hjælp af et grundlæggende, velkendt sæt af 9 farvenuancer og 3 nuancer med variationer i lysstyrke og bleghed. Dette er i stedet for at bruge mere subjektive og mindre forståede farvenavne. (#6029)
* Den eksisterende NVDA+F9 og derefter NVDA+F10-adfærd er blevet ændret til at vælge tekst ved første tryk på F10. Når F10 trykkes to gange (hurtigt efter hinanden), kopieres teksten til udklipsholderen. (#4636)
* Opdateret eSpeak NG til version Master 11b1a7b (22. juni 2016). (#6037)

### Fejlrettelser

* I gennemsynstilstand i Microsoft Word bevares formateringen nu ved kopiering til udklipsholderen. (#5956)
* I Microsoft Word rapporterer NVDA nu korrekt, når der bruges Words egne tabelnavigationskommandoer (alt+home, alt+end, alt+pageUp og alt+pageDown) og tabelmarkeringskommandoer (shift tilføjet til navigationskommandoerne). (#5961)
* I Microsoft Words dialogbokse er NVDA's objektnavigation blevet væsentligt forbedret. (#6036)
* I nogle applikationer som Visual Studio 2015 rapporteres genvejstaster (f.eks. control+c for kopiér) nu som forventet. (#6021)
* Rettet et sjældent problem ved scanning efter serielle porte på nogle systemer, hvilket gjorde nogle punktdisplay-drivere ubrugelige. (#6015)
* Rapportering af farver i Microsoft Word er nu mere nøjagtig, da ændringer i Microsoft Office-temaer nu tages i betragtning. (#5997)
* Gennemsynstilstand for Microsoft Edge og understøttelse af søgeforslag i Startmenuen er igen tilgængelig på Windows 10-versioner efter april 2016. (#5955)
* I Microsoft Word fungerer automatisk tabelhovedlæsning bedre, når der er tale om flettede celler. (#5926)
* I Windows 10 Mail-appen undlader NVDA ikke længere at læse indholdet af meddelelser. (#5635)
* Når kommandoen for tale af kommandoer er aktiveret, annonceres låsetaster som caps lock ikke længere to gange. (#5490)
* Dialoger for Windows-brugerkontokontrol læses igen korrekt i Windows 10 jubilæumsopdateringen. (#5942)
* I webkonference-pluginet (såsom brugt på out-of-sight.net) bipper NVDA ikke længere og taler statuslinjeopdateringer relateret til mikrofoninput. (#5888)
* Ved udførelse af en Find næste eller Find forrige-kommando i gennemsynstilstand udføres der nu korrekt en søgning, der skelner mellem store og små bogstaver, hvis den oprindelige søgning var følsom over for store og små bogstaver. (#5522)
* Når du redigerer ordbogsindgange, gives der nu feedback ved ugyldige regulære udtryk. NVDA går ikke længere ned, hvis en ordbogsfil indeholder et ugyldigt regulært udtryk. (#4834)
* Hvis NVDA ikke kan kommunikere med et punktdisplay (f.eks. fordi det er blevet afbrudt), deaktiverer det automatisk brugen af displayet. (#1555)
* Let forbedret ydeevne ved filtrering i elementlisten i gennemsynstilstand i nogle tilfælde. (#6126)
* I Microsoft Excel matcher NVDA nu baggrundsmønsternavne, som de bruges af Excel. (#6092)
* Forbedret understøttelse af Windows 10 logonskærm, inklusive annoncering af advarsler og aktivering af adgangskodefeltet med touch. (#6010)
* NVDA registrerer nu korrekt de sekundære routingknapper på ALVA BC640/680-seriens punktdisplays. (#5206)
* NVDA kan igen rapportere Windows Toast-meddelelser i nyere versioner af Windows 10. (#6096)
* NVDA stopper ikke længere med at genkende tastetryk lejlighedsvis på Baum-kompatible og HumanWare Brailliant B punktdisplays. (#6035)
* Hvis rapportering af linjenumre er aktiveret i NVDA's dokumentformateringsindstillinger, vises linjenumre nu på et punktdisplay. (#5941)
* Når tale er slået fra, vises rapportering af objekter (f.eks. ved at trykke på NVDA+tab for at rapportere fokus) nu i taleviseren som forventet. (#6049)
* I Outlook 2016-meddelelseslisten rapporteres der ikke længere tilknyttede kladdeoplysninger. (#6219)
* I Google Chrome og Chrome-baserede browsere på et andet sprog end engelsk fungerer gennemsynstilstand nu korrekt i mange dokumenter. (#6249)

### Ændringer for udviklere

* Logning af oplysninger direkte fra en egenskab resulterer ikke længere i, at egenskaben kaldes rekursivt igen og igen. (#6122)

## 2016.2.1

Denne udgivelse retter nedbrud i Microsoft Word:

* NVDA får ikke længere Microsoft Word til at gå ned umiddelbart efter opstart i Windows XP. (#6033)
* Fjernet rapportering af grammatikfejl, da dette forårsagede nedbrud i Microsoft Word. (#5954, #5877)

## 2016.2

Højdepunkterne i denne udgivelse inkluderer muligheden for at indikere stavefejl, mens du skriver; understøttelse af rapportering af grammatikfejl i Microsoft Word; og forbedringer og rettelser til understøttelse af Microsoft Office.

### Nye funktioner

* I gennemsynstilstand i Internet Explorer og andre MSHTML-kontroller bruges første bogstavsnavigation til at navigere ved annotation (a og shift+a) nu til indsatte og slettede tekster. (#5691)
* I Microsoft Excel rapporterer NVDA nu niveauet af en gruppe celler samt om den er sammenklappet eller udvidet. (#5690)
* Ved at trykke på kommandoen til at rapportere tekstformatering (NVDA+f) to gange præsenteres informationen i gennemsynstilstand, så den kan gennemgås. (#4908)
* I Microsoft Excel 2010 og nyere rapporteres cellefyld og gradientfyld nu. Automatisk rapportering styres af indstillingen Rapporter farver i NVDA's dokumentformateringsindstillinger. (#3683)
* Ny punktoversættelsestabel: Koine-græsk. (#5393)
* I logviseren kan du nu gemme loggen ved hjælp af genvejstasten control+s. (#4532)
* Hvis rapportering af stavefejl er aktiveret og understøttes i den fokuserede kontrol, afspiller NVDA en lyd for at advare om en stavefejl, mens du skriver. Dette kan deaktiveres ved hjælp af den nye mulighed "Afspil lyd for stavefejl under indtastning" i NVDA's dialogboks for tastaturindstillinger. (#2024)
* Grammatikfejl rapporteres nu i Microsoft Word. Dette kan deaktiveres ved hjælp af den nye mulighed "Rapporter grammatikfejl" i NVDA's dialogboks for dokumentformateringsindstillinger. (#5877)

### Ændringer

* I gennemsynstilstand og redigerbare tekstfelter behandler NVDA nu numpadEnter-tasten på samme måde som hoved-Enter-tasten. (#5385)
* NVDA er skiftet til eSpeak NG talesyntese. (#5651)
* I Microsoft Excel ignorerer NVDA ikke længere en kolonneoverskrift for en celle, når der er en tom række mellem cellen og overskriften. (#5396)
* I Microsoft Excel annonceres koordinater nu før overskrifter for at eliminere tvetydighed mellem overskrifter og indhold. (#5396)

### Fejlrettelser

* I gennemsynstilstand, når du forsøger at bruge navigation med enkelt bogstav til at flytte til et element, som ikke understøttes for dokumentet, rapporterer NVDA nu, at dette ikke understøttes, i stedet for at rapportere, at der ikke er noget element i den retning. (#5691)
* Når der vises ark i elementlisten i Microsoft Excel, er ark, der kun indeholder diagrammer, nu inkluderet. (#5698)
* NVDA rapporterer ikke længere overflødig information ved skift af vinduer i en Java-applikation med flere vinduer, såsom IntelliJ eller Android Studio. (#5732)
* I Scintilla-baserede redaktører som Notepad++ opdateres punktskrift nu korrekt, når markøren flyttes ved hjælp af et punktdisplay. (#5678)
* NVDA går ikke længere ned nogle gange, når punktudgang aktiveres. (#4457)
* I Microsoft Word rapporteres afsnitsindrykninger nu altid i den måleenhed, der er valgt af brugeren (f.eks. centimeter eller tommer). (#5804)
* Når du bruger et punktdisplay, vises mange NVDA-beskeder, der tidligere kun blev læst højt, nu også i punktskrift. (#5557)
* I tilgængelige Java-applikationer rapporteres niveauet for elementer i træstrukturer nu. (#5766)
* Rettet nedbrud i Adobe Flash i Mozilla Firefox i visse tilfælde. (#5367)
* I Google Chrome og Chrome-baserede browsere kan dokumenter i dialoger eller applikationer nu læses i gennemsynstilstand. (#5818)
* I Google Chrome og Chrome-baserede browsere kan du nu tvinge NVDA til at skifte til gennemsynstilstand i webdialoger eller applikationer. (#5818)
* I Internet Explorer og andre MSHTML-kontroller skifter fokus ikke længere forkert til gennemsynstilstand, når det flyttes til visse kontroller (specifikt når aria-activedescendant bruges). Dette skete f.eks. ved forslag i adressefelter, når der komponeres en besked i Gmail. (#5676)
* I Microsoft Word fryser NVDA ikke længere i store tabeller, når rapportering af tabelrække-/kolonneoverskrifter er aktiveret. (#5878)
* I Microsoft Word rapporterer NVDA ikke længere tekst med et dispositionsniveau (men ikke en indbygget overskriftsstil) forkert som en overskrift. (#5186)
* I gennemsynstilstand i Microsoft Word fungerer kommandoerne Flyt forbi slutning/til start af beholder (komma og shift+komma) nu for tabeller. (#5883)

### Ændringer for udviklere

* NVDA's C++-komponenter kompileres nu med Microsoft Visual Studio 2015. (#5592)
* Du kan nu præsentere en tekst- eller HTML-besked for brugeren i gennemsynstilstand ved hjælp af ui.browseableMessage. (#4908)
* I brugervejledningen kan en <!-- KC:setting-kommando bruges til en indstilling, der har en fælles tast for alle layout, hvor tasten nu kan placeres efter et fuldbredde-kolon (：) såvel som det almindelige kolon (:). (#5739)

## 2016.1

Højdepunkterne i denne udgivelse inkluderer muligheden for at sænke lydstyrken af andre lyde; forbedringer i punktskriftudgang og punktdisplay-understøttelse; flere væsentlige rettelser til understøttelsen af Microsoft Office; og rettelser til gennemsynstilstand i iTunes.

### Nye funktioner

* Nye punktoversættelsestabeller: Polsk 8-punkt computer braille, Mongolsk. (#5537, #5574)
* Du kan slå punktskriftsmarkøren fra og ændre dens form ved hjælp af de nye indstillinger Vis markør og Markørform i NVDA's punktindstillinger. (#5198)
* NVDA kan nu oprette forbindelse til et HIMS Smart Beetle punktdisplay via Bluetooth. (#5607)
* NVDA kan valgfrit sænke lydstyrken af andre lyde, når det er installeret på Windows 8 og nyere. Dette kan konfigureres ved hjælp af lydsænkningsindstillingen i NVDA's taleindstillinger eller ved at trykke på NVDA+shift+d. (#3830, #5575)
* Understøttelse af APH Refreshabraille i HID-tilstand samt Baum VarioUltra og Pronto! når de er forbundet via USB. (#5609)
* Understøttelse af HumanWare Brailliant BI/B punktdisplays, når protokollen er indstillet til OpenBraille. (#5612)

### Ændringer

* Rapportering af fremhævning er nu deaktiveret som standard. (#4920)
* I elementlisten i Microsoft Excel er genvejen til formler blevet ændret til alt+r, så den er forskellig fra genvejen til filterfeltet. (#5527)
* Opdateret liblouis punktoversætter til version 2.6.5. (#5574)
* Ordet "tekst" rapporteres ikke længere, når fokus eller gennemgangsmarkøren flyttes til tekstobjekter. (#5452)

### Fejlrettelser

* I iTunes 12 opdateres gennemsynstilstand nu korrekt, når en ny side indlæses i iTunes Store. (#5191)
* I Internet Explorer og andre MSHTML-kontroller fungerer navigation med enkelt bogstav til specifikke overskriftsniveauer nu som forventet, når overskriftsniveauet ændres for tilgængelighed (specifikt når aria-level ændrer niveauet for et h-tag). (#5434)
* I Spotify lander fokus ikke længere ofte på "ukendte" objekter. (#5439)
* Fokus gendannes nu korrekt, når du vender tilbage til Spotify fra en anden applikation. (#5439)
* Ved skift mellem gennemsynstilstand og fokustilstand rapporteres tilstanden nu i punktskrift såvel som i tale. (#5239)
* Startknappen på proceslinjen rapporteres ikke længere som en liste og/eller som markeret i nogle versioner af Windows. (#5178)
* Meddelelser som "indsat" rapporteres ikke længere, når du skriver beskeder i Microsoft Outlook. (#5486)
* Når du bruger et punktdisplay, og tekst er markeret på den aktuelle linje (f.eks. når du søger i en teksteditor efter tekst, der forekommer på samme linje), vil punktdisplayet blive rullet, hvis det er relevant. (#5410)
* NVDA afsluttes ikke længere lydløst, når et Windows-kommandokonsol lukkes med alt+f4 i Windows 10. (#5343)
* I elementlisten i gennemsynstilstand ryddes filtreringsfeltet nu, når du ændrer typen af element. (#5511)
* I redigerbar tekst i Mozilla-applikationer læses den relevante linje, ord osv. nu korrekt, når musen flyttes i stedet for hele indholdet. (#5535)
* Når musen flyttes i redigerbar tekst i Mozilla-applikationer, stopper læsningen ikke længere ved elementer som links inden for ordet eller linjen, der læses. (#2160, #5535)
* I Internet Explorer kan websitet shoprite.com nu læses i gennemsynstilstand i stedet for at blive rapporteret som tomt. (Specifikt håndteres misdannede lang-attributter nu korrekt.) (#5569)
* I Microsoft Word rapporteres sporbare ændringer som "indsat" ikke længere, når markeringen af ændringer ikke vises. (#5566)
* Når en skift-knap er i fokus, rapporterer NVDA nu, når den ændres fra trykket til ikke trykket. (#5441)
* Rapportering af museformændringer fungerer igen som forventet. (#5595)
* Når der tales linjeindrykninger, behandles ikke-brudte mellemrum nu som normale mellemrum. Tidligere kunne dette medføre annonceringer som "mellemrum mellemrum mellemrum" i stedet for "3 mellemrum". (#5610)
* Når en moderne Microsoft inputmetodeliste lukkes, gendannes fokus korrekt til enten inputkompositionen eller det underliggende dokument. (#4145)
* I Microsoft Office 2013 og nyere, når båndet er indstillet til kun at vise faner, rapporteres elementer i båndet igen som forventet, når en fane aktiveres. (#5504)
* Rettelser og forbedringer af registrering og binding af touchscreen-bevægelser. (#5652)
* Touchscreen-hovers rapporteres ikke længere i inputhjælp. (#5652)
* NVDA undlader ikke længere at liste kommentarer i elementlisten for Microsoft Excel, hvis en kommentar findes på en flettet celle. (#5704)
* I en meget sjælden sag undlader NVDA ikke længere at læse arkindhold i Microsoft Excel, når rapportering af række- og kolonneoverskrifter er aktiveret. (#5705)
* I Google Chrome fungerer navigation inden for en inputkomposition, når østasiatiske tegn indtastes, nu som forventet. (#4080)
* Når der søges i Apple Music i iTunes, opdateres gennemsynstilstanden for søgeresultatdokumentet nu som forventet. (#5659)
* I Microsoft Excel rapporteres din nye position, når du trykker shift+f11 for at oprette et nyt ark, i stedet for at der ikke rapporteres noget. (#5689)
* Rettet problemer med punktdisplay-output ved indtastning af koreanske tegn. (#5640)

### Ændringer for udviklere

* Den nye audioDucking.AudioDucker-klasse gør det muligt for kode, der afspiller lyd, at angive, når baggrundslyd skal sænkes. (#3830)
* nvwave.WavePlayer's constructor har nu et wantDucking-nøgleargument, der angiver, om baggrundslyd skal sænkes, mens lyd afspilles. (#3830)
  * Når dette er aktiveret (hvilket er standardindstillingen), er det vigtigt, at WavePlayer.idle kaldes, når det er relevant.
* Forbedret I/O for punktdisplays: (#5609)
  * Tråd-sikre punktdisplay-drivere kan erklære sig som sådan ved hjælp af attributten BrailleDisplayDriver.isThreadSafe. En driver skal være tråd-sikker for at drage fordel af følgende funktioner.
  * Data skrives til tråd-sikre punktdisplay-drivere i baggrunden, hvilket forbedrer ydeevnen.
  * hwIo.Serial udvider pyserial til at kalde en callable, når data modtages, i stedet for at drivere skal poll.
  * hwIo.Hid understøtter punktdisplays, der kommunikerer via USB HID.
  * hwPortUtils og hwIo kan valgfrit levere detaljeret fejllogning, herunder fundne enheder og al data, der sendes og modtages.
* Der er flere nye egenskaber tilgængelige fra touchscreen-bevægelser: (#5652)
  * MultiTouchTracker-objekter indeholder nu en childTrackers-egenskab, der indeholder MultiTouchTrackers, som trackeren er sammensat af. For eksempel har dobbelt tap med to fingre childTrackers for to 2-finger tap. 2-finger tapene har selv childTrackers for to tap.
  * MultiTouchTracker-objekter indeholder nu også en rawSingleTouchTracker-egenskab, hvis trackeren er resultatet af en enkelt finger, der udfører et tap, flick eller hover. SingleTouchTracker giver adgang til det underliggende ID, der er tildelt fingeren af operativsystemet, og om fingeren stadig er i kontakt på det nuværende tidspunkt.
  * TouchInputGestures har nu x- og y-egenskaber, hvilket fjerner behovet for at få adgang til trackeren i trivielle tilfælde.
  * TouchInputGestures indeholder nu en preheldTracker-egenskab, som er et MultiTouchTracker-objekt, der repræsenterer de andre fingre, der blev holdt, mens denne handling blev udført.
* To nye touchscreen-bevægelser kan nu udsendes: (#5652)
  * Plural tap and hold (f.eks. dobbelt tryk og hold)
  * En generaliseret identifikator med fjernet fingerantal for hold (f.eks. hold+hover for 1finger_hold+hover).

## 2015.4

Højdepunkter i denne udgivelse inkluderer ydelsesforbedringer i Windows 10; inkludering i center for nem adgang i Windows 8 og senere; forbedringer til Microsoft Excel, inklusive visning og omdøbning af ark samt adgang til låste celler i beskyttede ark; og understøttelse af redigering af rig tekst i Mozilla Firefox, Google Chrome og Mozilla Thunderbird.

### Nye Funktioner

* NVDA vises nu i center for nem adgang i Windows 8 og senere. (#308)
* Når man bevæger sig rundt i celler i Excel, rapporteres formateringsændringer nu automatisk, hvis de relevante indstillinger er slået til i NVDA's dokumentformateringsindstillinger. (#4878)
* En Rapportér Fremhævning indstilling er blevet tilføjet til NVDA's dokumentformateringsindstillinger. Som standard slået til gør denne indstilling det muligt for NVDA automatisk at rapportere tilstedeværelsen af fremhævet tekst i dokumenter. Indtil videre er dette kun understøttet for em og strong tags i Gennemsynstilstand for Internet Explorer og andre MSHTML kontroller. (#4920)
* Eksistensen af indsat og slettet tekst rapporteres nu i Gennemsynstilstand for Internet Explorer og andre MSHTML kontroller, hvis NVDA's Rapportér Redaktør Revisioner indstilling er aktiveret. (#4920)
* Når man ser sporændringer i NVDA's elementliste for Microsoft Word, vises flere oplysninger som f.eks. hvilke formateringsindstillinger der er ændret. (#4920)
* Microsoft Excel: visning og omdøbning af ark er nu muligt fra NVDA's elementliste (NVDA+f7). (#4630, #4414)
* Det er nu muligt at konfigurere, om faktiske symboler sendes til talesynteserne (f.eks. for at forårsage en pause eller ændring i tonefald) i Symboludtalelsesdialogen. (#5234)
* I Microsoft Excel rapporterer NVDA nu eventuelle indtastningsbeskeder, der er angivet af arkets forfatter på celler. (#5051)
* Understøttelse af Baum Pronto! V4 og VarioUltra punktdisplays, når de er tilsluttet via Bluetooth. (#3717)
* Understøttelse af redigering af rig tekst i Mozilla-applikationer såsom Google Docs med punktunderstøttelse aktiveret i Mozilla Firefox og HTML-komposition i Mozilla Thunderbird. (#1668)
* Understøttelse af redigering af rig tekst i Google Chrome og Chrome-baserede browsere såsom Google Docs med punktunderstøttelse aktiveret. (#2634)
 * Dette kræver Chrome version 47 eller senere.
* I Gennemsynstilstand i Microsoft Excel kan du navigere til låste celler i beskyttede ark. (#4952)

### Ændringer

* Rapportér Redaktør Revisioner indstillingen i NVDA's dokumentformateringsindstillinger er nu som standard slået til. (#4920)
* Når man bevæger sig med tegn i Microsoft Word med NVDA's Rapportér Redaktør Revisioner indstilling aktiveret, rapporteres der nu færre oplysninger for sporændringer, hvilket gør navigationen mere effektiv. For at se de ekstra oplysninger kan du bruge Elementlisten. (#4920)
* Opdateret liblouis punktoversætter til 2.6.4. (#5341)
* Flere symboler (inklusive grundlæggende matematiske symboler) er flyttet til niveau nogle, så de nu bliver talt som standard. (#3799)
* Hvis talesyntesen understøtter det, bør talen nu pause ved parenteser og tankestreg (–). (#3799)
* Når man markerer tekst, rapporteres teksten før angivelsen af markering i stedet for efter. (#1707)

### Fejlrettelser

* Store ydelsesforbedringer ved navigation i Outlook 2010/2013 meddelelsesliste. (#5268)
* I et diagram i Microsoft Excel fungerer navigation med bestemte taster (såsom at skifte ark med control+pageUp og control+pageDown) nu korrekt. (#5336)
* Rettet det visuelle udseende af knapperne i advarselsdialogen, der vises, når du forsøger at nedgradere NVDA. (#5325)
* I Windows 8 og senere starter NVDA nu meget tidligere, når det er konfigureret til at starte efter login på Windows. (#308)
 * Hvis du aktiverede dette med en tidligere version af NVDA, skal du deaktivere det og aktivere det igen for at ændringen træder i kraft. Følg denne procedure:
  1. Åbn Generelle indstillinger dialogen.
  1. Fjern markeringen i check boxen  Start NVDA automatisk efter login på Windows.
  1. Tryk på OK knappen.
  1. Åbn Generelle indstillinger dialogen igen.
  1. Marker check boxen Start NVDA automatisk efter login på Windows.
  1. Tryk på OK knappen.
* Ydelsesforbedringer for UI Automation, inklusive File Explorer og Opgavefremviser. (#5293)
* NVDA skifter nu korrekt til fokustilstand, når der tabbes til skrivebeskyttede ARIA gitterkontroller i Gennemsynstilstand for Mozilla Firefox og andre Gecko-baserede kontroller. (#5118)
* NVDA rapporterer nu korrekt "ingen tidligere" i stedet for "ingen næste", når der ikke er flere objekter ved flicking til venstre på en berøringsskærm.
* Rettede problemer, når man indtastede flere ord i filterfeltet i kommando-dialogen. (#5426)
* NVDA fryser ikke længere i nogle tilfælde, når der genoprettes forbindelse til en HumanWare Brailliant BI/B serie display via USB. (#5406)
* I sprog med sammenføjede tegn fungerer tegnbeskrivelser nu som forventet for store engelske bogstaver. (#5375)
* NVDA bør ikke længere lejlighedsvis fryse, når startmenuen åbnes i Windows 10. (#5417)
* I Skype for Desktop rapporteres meddelelser, der vises før en tidligere meddelelse forsvinder, nu korrekt. (#4841)
* Meddelelser rapporteres nu korrekt i Skype for Desktop 7.12 og senere. (#5405)
* NVDA rapporterer nu korrekt fokus, når en kontekstmenu lukkes i nogle applikationer som Jart. (#5302)
* I Windows 7 og senere rapporteres farve igen i visse applikationer som Wordpad. (#5352)
* Ved redigering i Microsoft PowerPoint rapporteres automatisk indsat tekst som f.eks. et punktum eller nummer nu, når der trykkes på Enter. (#5360)

## 2015.3

Højdepunkter i denne udgivelse inkluderer den første understøttelse af Windows 10; muligheden for at deaktivere navigation med enkeltbogstaver i gennemsynstilstand (nyttigt for nogle webapps); forbedringer i Internet Explorer; og fejlrettelser for forvrænget tekst ved indtastning i visse applikationer med punkt aktiveret.

### Nye Funktioner

* Eksistensen af stavefejl annonceres i redigerbare felter for Internet Explorer og andre MSHTML-kontroller. (#4174)
* Mange flere Unicode-matematiksymboler udtales nu, når de optræder i teksten. (#3805)
* Søgeforslag på startskærmen i Windows 10 rapporteres automatisk. (#5049)
* Understøttelse af EcoBraille 20, EcoBraille 40, EcoBraille 80 og EcoBraille Plus punktdisplays. (#4078)
* I gennemsynstilstand kan du nu slå navigation med enkeltbogstaver til og fra ved at trykke NVDA+shift+space. Når funktionen er slået fra, sendes enkeltbogstaver til applikationen, hvilket er nyttigt for nogle webapplikationer såsom Gmail, Twitter og Facebook. (#3203)
* Nye punktoversættelsestabeller: Finsk 6 punkt, Irsk grad 1, Irsk grad 2, Koreansk grad 1 (2006), Koreansk grad 2 (2006). (#5137, #5074, #5097)
* QWERTY-tastaturet på Papenmeier BRAILLEX Live Plus punktdisplayet understøttes nu. (#5181)
* Eksperimentel understøttelse af Microsoft Edge webbrowseren og browsingmotoren i Windows 10. (#5212)
* Nyt sprog: Kannada.

### Ændringer

* Opdateret liblouis punktoversætter til 2.6.3. (#5137)
* Når du forsøger at installere en tidligere version af NVDA end den aktuelt installerede, vil du nu blive advaret om, at dette ikke anbefales, og at NVDA skal afinstalleres fuldstændigt, før du fortsætter. (#5037)

### Fejlrettelser

* I gennemsynstilstand for Internet Explorer og andre MSHTML-kontroller inkluderer hurtignavigation efter formularfelter ikke længere fejlagtigt præsentationslisteelementer. (#4204)
* I Firefox rapporterer NVDA ikke længere uhensigtsmæssigt indholdet af et ARIA fanepanel, når fokus flyttes indenfor det. (#4638)
* I Internet Explorer og andre MSHTML-kontroller rapporteres alt indhold i sektioner, artikler eller dialogbokse ikke længere uhensigtsmæssigt, når der tabbes ind i dem. (#5021, #5025)
* Ved brug af Baum/HumanWare/APH punktdisplays med et punkt-tastatur ophører punktinput ikke længere med at fungere efter tryk på en anden tast på displayet. (#3541)
* I Windows 10 rapporteres der ikke længere overflødig information, når der trykkes på alt+tab eller alt+shift+tab for at skifte mellem applikationer. (#5116)
* Indtastet tekst forvrænges ikke længere ved brug af visse applikationer som Microsoft Outlook med et punktdisplay. (#2953)
* I gennemsynstilstand for Internet Explorer og andre MSHTML-kontroller rapporteres det korrekte indhold nu, når et element vises eller ændres og straks fokuseres. (#5040)
* I gennemsynstilstand for Microsoft Word opdateres punktdisplayet og gennemsemarkøren som forventet ved navigation med enkeltbogstaver. (#4968)
* I punkt vises der ikke længere unødvendige mellemrum mellem eller efter indikatorer for kontroller og formatering. (#5043)
* Når en applikation reagerer langsomt, og du skifter væk fra den applikation, er NVDA nu meget mere responsiv i andre applikationer i de fleste tilfælde. (#3831)
* Windows 10 Toast-meddelelser rapporteres nu som forventet. (#5136)
* Værdien rapporteres nu korrekt, når den ændres i visse (UI Automation) combo boxe, hvor dette tidligere ikke fungerede.
* I gennemsynstilstand for webbrowsere fungerer tabulatortasten nu som forventet efter at have tabbet til et rammedokument. (#5227)
* Låseskærmen i Windows 10 kan nu lukkes ved hjælp af en berøringsskærm. (#5220)
* I Windows 7 og senere forvrænges teksten ikke længere ved indtastning i visse applikationer som Wordpad og Skype med et punktdisplay. (#4291)
* På Windows 10 låseskærmen er det ikke længere muligt at læse udklipsholderen, få adgang til kørende applikationer med gennemsemarkøren, ændre NVDA-konfiguration mv. (#5269)

## 2015.2

Højdepunkter i denne udgivelse inkluderer evnen til at læse diagrammer i Microsoft Excel og understøttelse af læsning og interaktiv navigation af matematisk indhold.

### Nye Funktioner

* At bevæge sig frem og tilbage med sætning i Microsoft Word og Outlook er nu muligt med alt+nedpil og alt+oppil henholdsvis. (#3288)
* Nye punktoversættelsestabeller for flere indiske sprog. (#4778)
* I Microsoft Excel rapporterer NVDA nu, når en celle har overløbende eller beskåret indhold. (#3040)
* I Microsoft Excel kan du nu bruge Elementlisten (NVDA+f7) til at vise diagrammer, kommentarer og formler. (#1987)
* Understøttelse af læsning af diagrammer i Microsoft Excel. For at bruge dette skal du vælge diagrammet ved hjælp af Elementlisten (NVDA+f7) og derefter bruge piletasterne til at bevæge dig mellem datapunkterne. (#1987)
* Ved brug af MathPlayer 4 fra Design Science kan NVDA nu læse og interaktivt navigere matematisk indhold i webbrowsere og i Microsoft Word og PowerPoint. Se afsnittet "Læsning af matematisk indhold" i brugervejledningen for detaljer. (#4673)
* Det er nu muligt at tildele inputkommandoer (tastaturkommandoer, berøringskommandoer osv.) for alle NVDA præference-dialoger og dokumentformateringsindstillinger ved hjælp af kommando-dialogen. (#4898)

### Ændringer

* I NVDA's dokumentformateringsindstillinger er tastaturgenvejene for rapporter lister, rapporter links, rapporter linjenumre og rapporter skriftnavn blevet ændret. (#4650)
* I NVDA's musenindstillinger er tastaturgenveje blevet tilføjet for afspil lydkoordinater når musen bevæger sig og lysstyrke styrer lydkoordinaters lydstyrke. (#4916)
* Signifikant forbedret rapportering af farvenavne. (#4984)
* Opdateret liblouis punktoversætter til 2.6.2. (#4777)

### Fejlrettelser

* Tegnbeskrivelser håndteres nu korrekt for sammenføjede tegn i visse indiske sprog. (#4582)
* Hvis "Stol på stemmens sprog ved behandling af tegn og symboler" indstillingen er aktiveret, bruger dialogboksen for tegnsætning/symboludtale nu korrekt stemmens sprog. Desuden vises sproget, for hvilket udtalen redigeres, i dialogboksens titel. (#4930)
* I Internet Explorer og andre MSHTML-kontroller annonceres indtastede tegn ikke længere uhensigtsmæssigt i redigerbare combo boxe såsom Google søgefeltet på Google hjemmesiden. (#4976)
* Ved valg af farver i Microsoft Office-applikationer rapporteres farvenavne nu. (#3045)
* Dansk punktudgang fungerer nu igen. (#4986)
* PageUp/PageDown kan igen bruges til at skifte dias i en PowerPoint-diasshow. (#4850)
* I Skype for Desktop 7.2 og senere rapporteres skrivemeddelelser nu korrekt, og problemer umiddelbart efter, at fokus er flyttet ud af en samtale, er rettet. (#4972)
* Rettet problemer ved indtastning af visse tegnsætningstegn/symboler såsom parenteser i filterfeltet i kommando-dialogen. (#5060)
* I Internet Explorer og andre MSHTML-kontroller inkluderer navigation med g eller shift+g til grafik nu elementer markeret som billeder tilgængelighedsmæssigt (dvs. ARIA role img). (#5062)

### Ændringer for udviklere

* brailleInput.handler.sendChars(mychar) filtrerer ikke længere et tegn, hvis det er lig med det forrige tegn, ved at sikre, at den sendte tast frigives korrekt. (#4139)
* Scripts til ændring af berøringstilstande vil nu respektere nye etiketter tilføjet til touchHandler.touchModeLabels. (#4699)
* Tilføjelser kan levere deres egne matematikpræsentationer. Se mathPres-pakken for detaljer. (#4509)
* Tale-kommandoer er implementeret til at indsætte en pause mellem ord og ændre tonehøjde, lydstyrke og hastighed. Se BreakCommand, PitchCommand, VolumeCommand og RateCommand i tale-modulet. (#4674)
 * Der er også tale.PhonemeCommand til at indsætte specifik udtale, men de nuværende implementeringer understøtter kun et meget begrænset antal fonemer.

## 2015.1

Højdepunkter i denne udgivelse inkluderer gennemsynstilstand for dokumenter i Microsoft Word og Outlook; store forbedringer i understøttelsen af Skype for Desktop; og væsentlige fejlrettelser for Microsoft Internet Explorer.

### Nye Funktioner

* Du kan nu tilføje nye symboler i dialogen for symboludtale. (#4354)
* I dialogen for kommandoer kan du bruge det nye "Filtrer efter" felt til kun at vise kommandoer, der indeholder specifikke ord. (#4458)
* NVDA rapporterer nu automatisk ny tekst i mintty. (#4588)
* I dialogboksen Find i gennemsynstilstand er der nu en mulighed for at udføre en søgning, der skelner mellem store og små bogstaver. (#4584)
* Hurtignavigation (tryk på h for at bevæge dig efter overskrift, osv.) og Elementliste (NVDA+f7) er nu tilgængelige i Microsoft Word-dokumenter ved at slå gennemsynstilstand til med NVDA+space. (#2975)
* Læsning af HTML-beskeder i Microsoft Outlook 2007 og senere er blevet væsentligt forbedret, da gennemsynstilstand automatisk aktiveres for disse meddelelser. Hvis gennemsynstilstand ikke er aktiveret i nogle sjældne situationer, kan du tvinge det til at slå til med NVDA+space. (#2975)
* Tabelkolonneoverskrifter i Microsoft Word rapporteres automatisk for tabeller, hvor en overskriftsrække eksplicit er angivet af forfatteren via Microsoft Word's tabelindstillinger. (#4510)
 * Dog, for tabeller hvor rækker er blevet flettet, vil dette ikke fungere automatisk. I dette tilfælde kan du stadig manuelt angive kolonneoverskrifter i NVDA med NVDA+shift+c.
* I Skype for Desktop rapporteres notifikationer nu. (#4741)
* I Skype for Desktop kan du nu rapportere og gennemgå nylige beskeder ved hjælp af NVDA+control+1 gennem NVDA+control+0; f.eks. NVDA+control+1 for den seneste besked og NVDA+control+0 for den tiende seneste. (#3210)
* I en samtale i Skype for Desktop rapporterer NVDA nu, når en kontaktperson skriver. (#3506)
* NVDA kan nu installeres lydløst via kommandolinjen uden at starte den installerede kopi efter installationen. For at gøre dette skal du bruge --install-silent indstillingen. (#4206)
* Understøttelse af Papenmeier BRAILLEX Live 20, BRAILLEX Live og BRAILLEX Live Plus punktdisplays. (#4614)

### Ændringer

* I NVDA's dokumentformateringsindstillinger har indstillingen for rapportering af stavefejl nu en genvejstast (alt+r). (#793)
* NVDA vil nu bruge talesynteseens sprog til behandling af tegn og symboler (inklusive tegnsætnings-/symbolnavne), uanset om automatisk sprogomskiftning er slået til. For at deaktivere denne funktion, så NVDA igen bruger sit grænsefladesprog, skal du fjerne markeringen i den nye mulighed i stemmeindstillinger kaldet "Stol på stemmens sprog ved behandling af tegn og symboler". (#4210)
* Understøttelse af Newfon talesyntese er blevet fjernet. Newfon er nu tilgængelig som en NVDA-tilføjelse. (#3184)
* Skype for Desktop version 7 eller senere er nu påkrævet til brug med NVDA; tidligere versioner understøttes ikke. (#4218)
* Downloading af NVDA-opdateringer er nu mere sikker. (Specifikt hentes opdateringsoplysningerne via https, og filens hash verificeres efter download.) (#4716)
* eSpeak er blevet opgraderet til version 1.48.04 (#4325)

### Fejlrettelser

* I Microsoft Excel håndteres fletteceller i rækker og kolonneoverskrifter nu korrekt. For eksempel, hvis A1 og B1 er flettet, vil B2 nu få rapporteret både A1 og B1 som dens kolonneoverskrift i stedet for ingenting. (#4617)
* Ved redigering af indholdet af en tekstboks i Microsoft PowerPoint 2003 rapporterer NVDA nu korrekt indholdet af hver linje. Tidligere, i hvert afsnit, ville linjerne være forskudt med én karakter. (#4619)
* Alle NVDA's dialogbokse er nu centreret på skærmen, hvilket forbedrer det visuelle layout og brugervenligheden. (#3148)
* I Skype for Desktop, når du skriver en introduktionsbesked for at tilføje en kontakt, fungerer indtastning og navigation i teksten nu korrekt. (#3661)
* Når fokus flyttes til et nyt element i trævisninger i Eclipse IDE, hvis det tidligere fokuserede element er en afkrydsningsboks, annonceres dette ikke længere fejlagtigt. (#4586)
* I Microsoft Words stavekontroldialog rapporteres den næste fejl automatisk, når den sidste er ændret eller ignoreret ved brug af de respektive genvejstaster. (#1938)
* Tekst kan nu læses korrekt i steder som Tera Term Pro's terminalvindue og dokumenter i Balabolka. (#4229)
* Fokus vender nu korrekt tilbage til det redigerede dokument, når indtastningen af tekst i koreansk og andre østasiatiske sprog er afsluttet, mens der redigeres inden for en ramme i Internet Explorer og andre MSHTML-dokumenter. (#4045)
* I kommando-dialogen, når du vælger et tastaturlayout til en tastaturkommando, der tilføjes, lukker esc nu menuen som forventet i stedet for at lukke dialogen. (#3617)
* Når en tilføjelse fjernes, slettes tilføjelsesbiblioteket nu korrekt efter genstart af NVDA. Tidligere var du nødt til at genstarte to gange. (#3461)
* Store problemer er blevet rettet ved brug af Skype for Desktop version 7. (#4218)
* Når du sender en besked i Skype for Desktop, læses den ikke længere to gange. (#3616)
* I Skype for Desktop bør NVDA ikke længere lejlighedsvis læse en stor mængde beskeder (måske endda en hel samtale) fejlagtigt. (#4644)
* Rettet et problem, hvor NVDA's "Rapportér dato/tid"-kommando ikke respekterede de regionale indstillinger angivet af brugeren i nogle tilfælde. (#2987)
* I gennemsynstilstand præsenteres meningsløs tekst (nogle gange over flere linjer) ikke længere for visse grafik, såsom dem fundet på Google Groups. (Specifikt opstod dette med base64-kodede billeder.) (#4793)
* NVDA bør ikke længere fryse efter få sekunder, når fokus flyttes væk fra en Windows Store-app, da den suspenderes. (#4572)
* aria-atomic-attributten på liveområder i Mozilla Firefox respekteres nu, selv når det atomare element selv ændres. Tidligere påvirkede det kun underordnede elementer. (#4794)
* Gennemsynstilstand vil afspejle opdateringer, og liveområder vil blive annonceret for gennemsynstilstandsdokumenter inden for ARIA-applikationer indlejret i et dokument i Internet Explorer eller andre MSHTML-kontroller. (#4798)
* Når tekst ændres eller tilføjes i liveområder i Internet Explorer og andre MSHTML-kontroller, hvor forfatteren har specificeret, at teksten er relevant, annonceres kun den ændrede eller tilføjede tekst i stedet for al tekst i det indeholdende element. (#4800)
* Indhold angivet af aria-labelledby-attributten på elementer i Internet Explorer og andre MSHTML-kontroller erstatter korrekt det oprindelige indhold, hvor det er passende. (#4575)
* Ved stavekontrol i Microsoft Outlook 2013 annonceres det fejlagtige ord nu. (#4848)
* I Internet Explorer og andre MSHTML-kontroller præsenteres indhold i elementer skjult med visibility:hidden ikke længere fejlagtigt i gennemsynstilstand. (#4839, #3776)
* I Internet Explorer og andre MSHTML-kontroller har title-attributten på formularfelter ikke længere forrang over andre mærkningsassociationer på uhensigtsmæssige måder. (#4491)
* I Internet Explorer og andre MSHTML-kontroller ignorerer NVDA ikke længere fokus på elementer på grund af aria-activedescendant-attributten. (#4667)

### Ændringer for udviklere

* Opdateret wxPython til 3.0.2.0. (#3763)
* Opdateret Python til 2.7.9. (#4715)
* NVDA går ikke længere ned ved genstart efter fjernelse eller opdatering af en tilføjelse, der importerer speechDictHandler i dens installTasks modul. (#4496)

## 2014.4

### Nye Funktioner

* Nye sprog: Colombiansk spansk, Punjabi.
* Det er nu muligt at genstarte NVDA eller genstarte NVDA med tilføjelser deaktiveret fra NVDA's afslutningsdialog. (#4057)
 * NVDA kan også startes med tilføjelser deaktiveret ved brug af kommandolinjemuligheden --disable-addons.
* I taleordbøger er det nu muligt at specificere, at et mønster kun skal matche, hvis det er et helt ord; dvs. det ikke forekommer som en del af et større ord. (#1704)

### Ændringer

* Hvis et objekt, du har navigeret til med objektnavigation, er inde i et gennemsynstilstands-dokument, men det objekt, du tidligere var på, ikke var det, indstilles gennemsynstilstand automatisk til dokument. Tidligere skete dette kun, hvis navigationsobjektet blev flyttet på grund af ændringer i fokus. (#4369)
* Listerne over punktdisplays og talesynteser i de respektive indstillingsdialoger er nu alfabetisk sorterede bortset fra Ingen punkt/Ingen tale, som nu er i bunden. (#2724)
* Opdateret liblouis punktoversætter til 2.6.0. (#4434, #3835)
* I gennemsynstilstand inkluderer navigation til redigeringsfelter ved at trykke på e og shift+e nu også redigerbare kombobokse. Dette inkluderer søgefeltet i den nyeste version af Google-søgning. (#4436)
* At klikke på NVDA-ikonet i meddelelsesområdet med venstre museknap åbner nu NVDA-menuen i stedet for at gøre ingenting. (#4459)

### Fejlrettelser

* Når fokus flyttes tilbage til et gennemsynstilstands-dokument (f.eks. ved at alt+tabbe til en allerede åben webside), er gennemgangsmarkøren korrekt placeret ved den virtuelle markør, snarere end på den fokuserede kontrol (f.eks. et nærliggende link). (#4369)
* I PowerPoint-diasshows følger gennemgangsmarkøren nu korrekt den virtuelle markør. (#4370)
* I Mozilla Firefox og andre Gecko-baserede browsere vil nyt indhold i et live-område blive annonceret, selvom det nye indhold har en anvendelig ARIA live-type, der er forskellig fra det overordnede live-område; f.eks. når indhold markeret som assertivt tilføjes et live-område markeret som høfligt. (#4169)
* I Internet Explorer og andre MSHTML-kontroller forhindrer visse tilfælde, hvor et dokument er indeholdt i et andet dokument, ikke længere brugeren i at få adgang til noget af indholdet (specifikt framesets inde i framesets). (#4418)
* NVDA går ikke længere ned, når der forsøges at bruge et Handy Tech punktdisplay i visse tilfælde. (#3709)
* I Windows Vista vises der ikke længere en uønsket "Entry Point Not Found"-dialog i flere tilfælde, f.eks. når NVDA startes fra skrivebordsgenvejen eller via genvejstasten. (#4235)
* Alvorlige problemer med redigerbare tekstkontroller i dialogbokse i nyere versioner af Eclipse er blevet rettet. (#3872)
* I Outlook 2010 fungerer flytning af markøren nu som forventet i placeringsfeltet for aftaler og mødeindkaldelser. (#4126)
* Indhold markeret som ikke live (f.eks. aria-live="off") i et live-område ignoreres nu korrekt. (#4405)
* Ved rapportering af teksten fra en statuslinje, der har et navn, adskilles navnet nu korrekt fra det første ord i statuslinjeteksten. (#4430)
* I adgangskodefelter med tale af indtastede ord aktiveret, rapporteres flere stjerner ikke længere unødigt, når nye ord påbegyndes. (#4402)
* I Microsoft Outlook-meddelelseslisten annonceres elementer ikke længere unødigt som Dataelementer. (#4439)
* Ved markering af tekst i kode-redigeringskontrollen i Eclipse IDE annonceres hele markeringen ikke længere hver gang markeringen ændres. (#2314)
* Forskellige versioner af Eclipse, såsom Spring Tool Suite og versionen inkluderet i Android Developer Tools-bundtet, genkendes nu som Eclipse og håndteres korrekt. (#4360, #4454)
* Muse-tracking og berøringsudforskning i Internet Explorer og andre MSHTML-kontroller (inklusive mange Windows 8-applikationer) er nu meget mere præcise på skærme med høj DPI eller når dokumentzoom ændres. (#3494)
* Muse-tracking og berøringsudforskning i Internet Explorer og andre MSHTML-kontroller vil nu annoncere etiketten på flere knapper. (#4173)
* Når du bruger et Papenmeier BRAILLEX punktdisplay med BrxCom, fungerer tasterne på displayet nu som forventet. (#4614)

### Ændringer for Udviklere

* For eksekverbare filer, der indeholder mange forskellige apps (f.eks. javaw.exe), kan der nu leveres kode til at indlæse specifikke app-moduler for hver app i stedet for at indlæse det samme app-modul for alle apps. (#4360)
 * Se kodedokumentationen for appModuleHandler.AppModule for detaljer.
 * Support for javaw.exe er implementeret.

## 2014.3

### Nye Funktioner

* Lydene, der afspilles, når NVDA starter og afsluttes, kan nu deaktiveres via en ny indstilling i dialogboksen Generelle indstillinger. (#834)
* Hjælp til tilføjelser kan tilgås fra Tilføjelsesadministratoren for tilføjelser, der understøtter dette. (#2694)
* Support for kalenderen i Microsoft Outlook 2007 og nyere (#2943), inklusive:
 * Annoncering af den aktuelle tid, når man navigerer med piletasterne.
 * Indikering af, om den valgte tid er inden for en aftale.
 * Annoncering af den valgte aftale ved tryk på tab.
 * Smart filtrering af datoen, så den kun annonceres, hvis den nye valgte tid eller aftale er på en anden dag end den sidste.
* Forbedret support for indbakken og andre meddelelseslister i Microsoft Outlook 2010 og nyere (#3834), inklusive:
 * Muligheden for at deaktivere kolonneoverskrifter (fra, emne osv.) ved at slå Rapportér tabelrække- og kolonneoverskrifter fra i dokumentformateringsindstillingerne.
 * Muligheden for at bruge tabelnavigationskommandoer (control + alt + pile) til at navigere gennem de enkelte kolonner.
* Microsoft Word: Hvis et inline-billede ikke har nogen alternativ tekst, rapporterer NVDA nu i stedet titlen på billedet, hvis forfatteren har angivet en. (#4193)
* Microsoft Word: NVDA kan nu rapportere afsnitsindrykninger med kommandoen for rapportering af formatering (NVDA+f). Det kan også rapporteres automatisk, hvis den nye indstilling Rapportér afsnitsindrykninger er aktiveret i dokumentformateringsindstillingerne. (#4165)
* Rapportér automatisk indsat tekst som et nyt punkt, tal eller indrykning, når enter trykkes i redigerbare dokumenter og tekstfelter. (#4185)
* Microsoft Word: Tryk på NVDA+alt+c for at rapportere teksten i en kommentar, hvis markøren er inden for en. (#3528)
* Forbedret support for automatisk læsning af kolonne- og rækkeoverskrifter i Microsoft Excel (#3568), inklusive:
 * Support for Excel-definerede navneområder til at identificere overskriftsceller (kompatibel med Jaws skærmlæser).
 * Kommandoerne Sæt kolonneoverskrift (NVDA+shift+c) og Sæt rækkeoverskrift (NVDA+shift+r) gemmer nu indstillingerne i regnearket, så de er tilgængelige næste gang, regnearket åbnes, og vil være tilgængelige for andre skærmlæsere, der understøtter det definerede navneområdeskema.
 * Disse kommandoer kan nu også bruges flere gange pr. ark til at sætte forskellige overskrifter for forskellige områder.
* Support for automatisk læsning af kolonne- og rækkeoverskrifter i Microsoft Word (#3110), inklusive:
 * Support for Microsoft Word-bogmærker til at identificere overskriftsceller (kompatibel med Jaws skærmlæser).
 * Kommandoerne Sæt kolonneoverskrift (NVDA+shift+c) og Sæt rækkeoverskrift (NVDA+shift+r), mens du er på den første overskriftscelle i en tabel, gør det muligt at fortælle NVDA, at disse overskrifter skal rapporteres automatisk. Indstillingerne gemmes i dokumentet, så de er tilgængelige næste gang, dokumentet åbnes, og vil være tilgængelige for andre skærmlæsere, der understøtter bogmærkeskemaet.
* Microsoft Word: Rapportér afstanden fra venstre kant af siden, når tab-tasten trykkes. (#1353)
* Microsoft Word: Giv feedback i tale og punkt for de fleste tilgængelige genveje til formatering (fed, kursiv, understregning, justering, dispositionsniveau, hævet skrift, sænket skrift og skriftstørrelse). (#1353)
* Microsoft Excel: Hvis den valgte celle indeholder kommentarer, kan de nu rapporteres ved at trykke på NVDA+alt+c. (#2920)
* Microsoft Excel: Giv en NVDA-specifik dialog til at redigere kommentarerne i den aktuelt valgte celle, når Excel's shift+f2-kommando bruges til at gå ind i kommentartilstand. (#2920)
* Microsoft Excel: Tale- og punkt-feedback for mange flere genveje til valgflytning (#4211), inklusive:
 * Lodret sideskift (pageUp og pageDown);
 * Vandret sideskift (alt+pageUp og alt+pageDown);
 * Udvid valg (ovenstående taster med shift tilføjet); og
 * Valg af det aktuelle område (control+shift+8).
* Microsoft Excel: Den lodrette og vandrette justering for celler kan nu rapporteres med kommandoen for rapportering af formatering (NVDA+f). Det kan også rapporteres automatisk, hvis indstillingen Rapportér justering er aktiveret i dokumentformateringsindstillingerne. (#4212)
* Microsoft Excel: Cellens stil kan nu rapporteres med kommandoen for rapportering af formatering (NVDA+f). Det kan også rapporteres automatisk, hvis indstillingen Rapportér stil er aktiveret i dokumentformateringsindstillingerne. (#4213)
* Microsoft PowerPoint: Når du flytter figurer rundt på en slide med piletasterne, rapporteres figurens aktuelle placering (#4214), inklusive:
 * Afstanden mellem figuren og hver af slide-kanterne rapporteres.
 * Hvis figuren dækker eller dækkes af en anden figur, rapporteres den overlappede afstand og den overlappede figur.
 * For at rapportere denne information til enhver tid uden at flytte en figur, skal du trykke på kommandoen for rapportering af placering (NVDA+delete).
 * Når du vælger en figur, rapporterer NVDA, hvis den er dækket af en anden figur.
* Kommandoen for rapportering af placering (NVDA+delete) er mere kontekstspecifik i visse situationer. (#4219)
 * I standardredigeringsfelter og gennemsynstilstand rapporteres markørens position som en procentdel gennem indholdet og dens skærmkoordinater.
 * På figurer i PowerPoint-præsentationer rapporteres figurens position i forhold til sliden og andre figurer.
 * Hvis denne kommando trykkes to gange, vil den producere den tidligere adfærd med at rapportere placeringsinformation for hele kontrollen.
* Nyt sprog: Katalansk.

### Ændringer

* Opdateret liblouis punktoversætter til 2.5.4. (#4103)

### Fejlrettelser

* I Google Chrome og Chrome-baserede browsere gentages visse tekststykker (såsom dem med fremhævelse) ikke længere, når teksten i en advarsel eller dialog rapporteres. (#4066)
* I gennemsynstilstand i Mozilla-applikationer fejler tryk på enter på en knap osv. ikke længere med at aktivere den (eller aktiverer den forkerte kontrol) i visse tilfælde som knapperne øverst på Facebook. (#4106)
* Ubrugelig information annonceres ikke længere, når man tabber i iTunes. (#4128)
* I visse lister i iTunes, såsom Musiklisten, fungerer flytning til det næste element med objektnavigation nu korrekt. (#4129)
* HTML-elementer, der betragtes som overskrifter på grund af WAI ARIA-markering, er nu inkluderet i gennemsynstilstandens elementliste og hurtignavigation for Internet Explorer-dokumenter. (#4140)
* Følgende af samme-sidelinks i nyere versioner af Internet Explorer flytter nu korrekt til og rapporterer destinationspositionen i gennemsynstilstandsdokumenter. (#4134)
* Microsoft Outlook 2010 og nyere: Adgang til sikre dialogbokse som Ny profiler og Mailopsætning-dialogerne er generelt forbedret. (#4090, #4091, #4095)
* Microsoft Outlook: Ubrugelig snak er reduceret i kommandoværktøjslinjer, når der navigeres gennem visse dialoger. (#4096, #3407)
* Microsoft Word: Tab til en tom celle i en tabel annoncerer ikke længere fejlagtigt, at man forlader tabellen. (#4151)
* Microsoft Word: Det første tegn efter enden af en tabel (inklusive en ny tom linje) betragtes ikke længere fejlagtigt som værende inde i tabellen. (#4152)
* Microsoft Word 2010 stavekontroldialog: Det faktiske fejlstavede ord rapporteres nu korrekt i stedet for blot at rapportere det første fede ord. (#3431)
* I gennemsynstilstand i Internet Explorer og andre MSHTML-kontroller rapporteres etiketten for formfelter igen i mange tilfælde, hvor den ikke gjorde det før (specifikt, hvor HTML-label-elementer anvendes). (#4170)
* Microsoft Word: Rapportering af tilstedeværelsen og placeringen af kommentarer er mere præcis. (#3528)
* Navigation af visse dialoger i MS Office-produkter som Word, Excel og Outlook er forbedret ved ikke længere at rapportere bestemte kontrolværktøjslinjer, der ikke er nyttige for brugeren. (#4198)
* Opgavepaneler som udklipsholdermanager eller Filgendannelse ser ikke længere ud til fejlagtigt at få fokus, når en applikation som Microsoft Word eller Excel åbnes, hvilket nogle gange fik brugeren til at skulle skifte væk fra og tilbage til applikationen for at bruge dokumentet eller regnearket. (#4199)
* NVDA fejler ikke længere at køre på nyere Windows-operativsystemer, hvis brugerens Windows-sprog er indstillet til serbisk (latin). (#4203)
* Tryk på numlock i input-hjælpetilstand skifter nu korrekt numlock i stedet for at få tastaturet og operativsystemet til at komme ud af synkronisering i forhold til status for denne tast. (#4226)
* I Google Chrome rapporteres dokumentets titel igen, når man skifter faner. I NVDA 2014.2 skete dette ikke i nogle tilfælde. (#4222)
* I Google Chrome og Chrome-baserede browsere rapporteres dokumentets URL ikke længere, når dokumentet rapporteres. (#4223)
* Når der køres "say all" med ingen talesyntesizer valgt (nyttigt til automatiseret testning), fuldfører "say all" nu i stedet for at stoppe efter de første par linjer. (#4225)
* Microsoft Outlooks Signatur-dialog: Signatur-redigeringsfeltet er nu tilgængeligt og giver fuld markørsporing og formatregistrering. (#3833)
* Microsoft Word: Når du læser den sidste linje af en tabelcelle, læses hele tabelcellen ikke længere. (#3421)
* Microsoft Word: Når du læser den første eller sidste linje af en indholdsfortegnelse, læses hele indholdsfortegnelsen ikke længere. (#3421)
* Når talte ord aktiveres og i nogle andre tilfælde, opdeles ord ikke længere fejlagtigt ved tegn som vokaltegn og virama i indiske sprog. (#4254)
* Numeriske redigerbare tekstfelter i GoldWave håndteres nu korrekt. (#670)
* Microsoft Word: Når du navigerer med control+pil ned/pil op gennem afsnit, er det ikke længere nødvendigt at trykke to gange, når du navigerer gennem punkt- eller nummererede lister. (#3290)

### Ændringer for Udviklere

* NVDA har nu samlet support for dokumentation af tilføjelser. Se afsnittet om tilføjelsesdokumentation i udviklerguiden for detaljer. (#2694)
* Når du leverer kommando-bindings til et ScriptableObject via __kommandoer, er det nu muligt at levere None som script. Dette ophæver kommandoen i alle basis-klasser. (#4240)
* Det er nu muligt at ændre genvejstasten, der bruges til at starte NVDA i lokaliteter, hvor den normale genvej giver problemer. (#2209)
 * Dette gøres via gettext.
 * Bemærk, at teksten til indstillingen Opret skrivebordsgenvej i NVDA's installationsdialog samt genvejstasten i brugervejledningen også skal opdateres.

## 2014.2

### Nye Funktioner

* Annoncering af tekstvalg er nu muligt i nogle brugerdefinerede redigeringsfelter, hvor visningsinformation bruges. (#770)
* I tilgængelige Java-applikationer annonceres positionsinformation nu for radioknapper og andre kontroller, der viser gruppeinformation. (#3754)
* I tilgængelige Java-applikationer annonceres tastaturgenveje nu for kontroller, der har dem. (#3881)
* I gennemsynstilstand rapporteres etiketter på landemærker nu. De er også inkluderet i dialogboksen Elementliste. (#1195)
* I gennemsynstilstand behandles områder med etiketter nu som landemærker. (#3741)
* I Internet Explorer-dokumenter og -applikationer understøttes nu Live Regions (en del af W3c ARIA-standarden), hvilket gør det muligt for webudviklere at markere bestemt indhold til automatisk at blive talt, når det ændres. (#1846)

### Ændringer

* Når man forlader en dialog eller applikation inden for et gennemsynstilstands-dokument, annonceres dokumentets navn og type ikke længere. (#4069)

### Fejlrettelser

* Standard Windows-systemmenuen er ikke længere fejlagtigt tavs i Java-applikationer. (#3882)
* Når tekst kopieres fra skærmanmeldelse, ignoreres linjeskift ikke længere. (#3900)
* Unødvendige mellemrumselementer rapporteres ikke længere i nogle applikationer, når fokus ændres, eller når objektnavigation bruges med enkel anmeldelse aktiveret. (#3839)
* Meddelelsesbokse og andre dialogbokse oprettet af NVDA afbryder igen tidligere tale, før dialogen annonceres.
* I gennemsynstilstand rapporteres kontrolers etiketter, såsom links og knapper, korrekt, når etiketten er blevet ændret af forfatteren for tilgængelighed (specifikt ved brug af aria-label eller aria-labelledby). (#1354)
* I gennemsynstilstand i Internet Explorer ignoreres tekst indeholdt i et element markeret som præsentation (ARIA role="presentation") ikke længere fejlagtigt. (#4031)
* Det er nu igen muligt at skrive vietnamesisk tekst ved hjælp af Unikey-software. For at gøre dette skal du fjerne markeringen i den nye afkrydsningsboks "Håndter taster fra andre applikationer" i NVDA's Tastaturindstillinger. (#4043)
* I gennemsynstilstand rapporteres radioknapper og afkrydsningsmenuer nu som kontroller i stedet for blot som klikbare tekster. (#4092)
* NVDA skifter ikke længere fejlagtigt fra fokustilstand til gennemsynstilstand, når en radioknap eller afkrydsningsmenu fokuseres. (#4092)
* I Microsoft PowerPoint, når tale af indtastede ord er aktiveret, annonceres slettede tegn med backspace ikke længere som en del af det indtastede ord. (#3231)
* I Microsoft Office 2010-indstillingsdialoger rapporteres komboboksers etiketter korrekt. (#4056)
* I gennemsynstilstand i Mozilla-applikationer inkluderer hurtignavigationskommandoer til at flytte til næste eller forrige knap eller formularfelt nu også skifteknapper som forventet. (#4098)
* Indholdet af advarsler i Mozilla-applikationer rapporteres ikke længere to gange. (#3481)
* I gennemsynstilstand gentages containere og landemærker ikke længere uhensigtsmæssigt, mens der navigeres i dem, samtidig med at sideindhold ændres (f.eks. ved navigation på Facebook og Twitter). (#2199)
* NVDA genvinder funktionaliteten i flere tilfælde, når der skiftes væk fra applikationer, der stopper med at svare. (#3825)
* Markøren opdateres igen korrekt, når "say all"-kommandoen bruges i redigerbar tekst, der tegnes direkte på skærmen. (#4125)

## 2014.1

### Nye Funktioner

* Support for Microsoft PowerPoint 2013. Bemærk, at beskyttet visning ikke understøttes. (#3578)
* I Microsoft Word og Excel kan NVDA nu læse det valgte symbol, når symboler vælges ved hjælp af dialogboksen Indsæt symboler. (#3538)
* Det er nu muligt at vælge, om indhold i dokumenter skal identificeres som klikbart via en ny indstilling i dokumentformateringsindstillingerne. Denne indstilling er aktiveret som standard i overensstemmelse med den tidligere adfærd. (#3556)
* Support for punktdisplays forbundet via Bluetooth på en computer, der kører Widcomm Bluetooth-software. (#2418)
* Når der redigeres tekst i PowerPoint, rapporteres hyperlinks nu. (#3416)
* Når man er i ARIA-applikationer eller dialogbokse på nettet, er det nu muligt at tvinge NVDA til at skifte til gennemsynstilstand med NVDA+space, hvilket muliggør dokumentstil-navigation i applikationen eller dialogen. (#2023)
* I Outlook Express / Windows Mail / Windows Live Mail rapporterer NVDA nu, om en meddelelse har en vedhæftet fil eller er markeret. (#1594)
* Når man navigerer i tabeller i tilgængelige Java-applikationer, rapporteres række- og kolonnekoordinater nu, inklusive kolonne- og rækkeoverskrifter, hvis de eksisterer. (#3756)

### Ændringer

* For Papenmeier punktdisplays er kommandoen til at flytte til flad anmeldelse/fokus fjernet. Brugere kan tildele deres egne taster ved hjælp af dialogboksen Inputkommandoer. (#3652)
* NVDA er nu afhængig af Microsoft VC runtime version 11, hvilket betyder, at det ikke længere kan køre på operativsystemer ældre end Windows XP Service Pack 2 eller Windows Server 2003 Service Pack 1.
* Tegnsætningsniveauet "Nogle" vil nu tale stjerne (*) og plus (+)-tegn. (#3614)
* Opgraderet eSpeak til version 1.48.04, som inkluderer mange sprogforbedringer og løser flere nedbrud. (#3842, #3739, #3860)

### Fejlrettelser

* Når du bevæger dig rundt eller vælger celler i Microsoft Excel, bør NVDA ikke længere fejlagtigt annoncere den gamle celle i stedet for den nye, når Microsoft Excel er langsom til at flytte valget. (#3558)
* NVDA håndterer korrekt åbningen af en dropdown-liste for en celle i Microsoft Excel via genvejsmenuen. (#3586)
* Nyt sideindhold i iTunes 11-butikssider vises nu korrekt i gennemsynstilstand, når et link følges i butikken, eller når butikken åbnes. (#3625)
* Knapper til forhåndsvisning af sange i iTunes 11-butikken viser nu deres etiket i gennemsynstilstand. (#3638)
* I gennemsynstilstand i Google Chrome gengives etiketterne for check boxer og radioknapper korrekt. (#1562)
* I Instantbird rapporterer NVDA ikke længere ubrugelig information, hver gang du flytter til en kontakt i kontaktlisten. (#2667)
* I gennemsynstilstand i Adobe Reader gengives den korrekte tekst nu for knapper osv., hvor etiketten er blevet ændret ved hjælp af et værktøjstip eller andre midler. (#3640)
* I gennemsynstilstand i Adobe Reader gengives overflødige grafik, der indeholder teksten "mc-ref", ikke længere. (#3645)
* NVDA rapporterer ikke længere alle celler i Microsoft Excel som understregede i deres formateringsinformation. (#3669)
* Meningsløse tegn i browse-mode dokumenter, såsom dem, der findes i det private brugsområde i Unicode, vises ikke længere. I nogle tilfælde forhindrede disse mere nyttige etiketter i at blive vist. (#2963)
* Tastaturkomposition for indtastning af østasiatiske tegn fejler ikke længere i PuTTY. (#3432)
* Navigation i et dokument efter en afbrudt "say all" resulterer ikke længere i, at NVDA fejlagtigt annoncerer, at du har forladt et felt (såsom en tabel), lavere i dokumentet, som "say all" aldrig talte. (#3688)
* Når hurtignavigationskommandoer bruges i gennemsynstilstand, mens "say all" er aktiveret med skumlæsning, annoncerer NVDA mere præcist det nye felt; f.eks. siger den nu, at en overskrift er en overskrift i stedet for blot dens tekst. (#3689)
* Kommandoerne til at hoppe til begyndelsen eller slutningen af en container respekterer nu indstillingen for skumlæsning under "say all"; dvs. de vil ikke længere afbryde den aktuelle "say all". (#3675)
* Navnene på kommandoer, der er opført i NVDA's Inputkommando-dialog, er nu brugervenlige og lokaliserede. (#3624)
* NVDA får ikke længere visse programmer til at gå ned, når musen bevæges over deres rich edit (TRichEdit) kontroller. Programmer inkluderer Jarte 5.1 og BRfácil. (#3693, #3603, #3581)
* I Internet Explorer og andre MSHTML-kontroller rapporteres containere såsom tabeller, der er markeret som præsentation af ARIA, ikke længere til brugeren. (#3713)
* I Microsoft Word rapporterer NVDA ikke længere fejlagtigt tabelrække- og kolonneinformation for en celle på et punktdisplay flere gange. (#3702)
* I sprog, der bruger mellemrum som tusindtalsseparator, såsom fransk og tysk, udtales tal fra separate tekststykker ikke længere som et enkelt tal. Dette var især problematisk for tabelceller, der indeholder tal. (#3698)
* Punktopdateringer mislykkes ikke længere nogle gange, når systemmarkøren flyttes i Microsoft Word 2013. (#3784)
* Når der er placeret på det første tegn i en overskrift i Microsoft Word, forsvinder teksten, der kommunikerer, at det er en overskrift (inklusive niveauet), ikke længere fra et punktdisplay. (#3701)
* Når en konfigurationsprofil aktiveres for en applikation, og den applikation lukkes, fejler NVDA ikke længere nogle gange at deaktivere profilen. (#3732)
* Når der indtastes asiatisk tekst i en kontrol inden for NVDA selv (f.eks. dialogen Find i gennemsynstilstand), rapporteres "NVDA" ikke længere fejlagtigt i stedet for kandidaten. (#3726)
* Fanerne i dialogboksen Outlook 2013-indstillinger rapporteres nu. (#3826)
* Forbedret support for ARIA-liveområder i Firefox og andre Mozilla Gecko-applikationer:
 * Support for aria-atomic opdateringer og filtrering af aria-busy opdateringer. (#2640)
 * Alternativ tekst (såsom alt-attribut eller aria-label) er inkluderet, hvis der ikke er nogen anden nyttig tekst. (#3329)
 * Liveområder opdateres ikke længere stiltiende, hvis de opdateres samtidig med, at fokus flytter. (#3777)
* Visse præsentationselementer i Firefox og andre Mozilla Gecko-applikationer vises ikke længere fejlagtigt i gennemsynstilstand (specifikt, når elementet er markeret med aria-presentation, men det også er fokuserbart). (#3781)
* En præstationsforbedring, når man navigerer et dokument i Microsoft Word med stavefejl aktiveret. (#3785)
* Flere fejlrettelser i supporten for tilgængelige Java-applikationer:
 * Den oprindeligt fokuserede kontrol i en ramme eller dialog mislykkes ikke længere med at blive rapporteret, når rammen eller dialogen kommer i forgrunden. (#3753)
 * Ubrugelig positionsinformation annonceres ikke længere for radioknapper (f.eks. 1 af 1). (#3754)
 * Bedre rapportering af JComboBox-kontroller (HTML rapporteres ikke længere, og udvidet og skjult status rapporteres bedre). (#3755)
 * Når teksten i dialoger rapporteres, inkluderes noget tekst, der tidligere manglede, nu. (#3757)
 * Ændringer i navnet, værdien eller beskrivelsen af den fokuserede kontrol rapporteres mere præcist. (#3770)
* Rettet et nedbrud i NVDA set i Windows 8, når man fokuserer på visse RichEdit-kontroller, der indeholder store mængder tekst (f.eks. NVDA's logviewer, windbg). (#3867)
* På systemer med en høj DPI-skærmindstilling (hvilket er standard for mange moderne skærme), ruter NVDA ikke længere musen til den forkerte placering i nogle applikationer. (#3758, #3703)
* Løste et lejlighedsvist problem ved browsing på nettet, hvor NVDA stoppede med at fungere korrekt, indtil det blev genstartet, selvom det ikke gik ned eller frøs. (#3804)
* Et Papenmeier punktdisplay kan nu bruges, selvom et Papenmeier display aldrig har været forbundet via USB. (#3712)
* NVDA fryser ikke længere, når det Papenmeier BRAILLEX ældre model punktdisplay vælges uden et display tilsluttet.

### Ændringer for Udviklere

* AppModules indeholder nu productName- og productVersion-egenskaber. Denne info er også nu inkluderet i Udviklerinfo (NVDA+f1). (#1625)
* I Python-konsollen kan du nu trykke på tab-tasten for at fuldføre den aktuelle identifikator. (#433)
 * Hvis der er flere muligheder, kan du trykke på tab en gang til for at vælge fra en liste.

## 2013.3

### Nye funktioner

* Formularfelter rapporteres nu i Microsoft Word-dokumenter. (#2295)
* NVDA kan nu meddele revisionsoplysninger i Microsoft Word, når "Spor ændringer" er aktiveret. Bemærk, at "Rapportér redaktørrevisioner" i NVDA's dokumentindstillingsdialog (som er slået fra som standard) også skal aktiveres for at de kan blive meddelt. (#1670)
* Rullelister i Microsoft Excel 2003 til 2010 annonceres nu, når de åbnes og navigeres rundt i. (#3382)
* En ny mulighed 'Tillad Skim-læsning i sig alle' i tastaturindstillingsdialogen giver mulighed for at navigere gennem et dokument med kommandoer for hurtig navigation og linje-/afsnitsbevægelseskommandoer, mens man forbliver i sig alle. Denne mulighed er som standard deaktiveret. (#2766)
* Der er nu en inputkommando-dialog for enklere tilpasning af inputkommandoer (såsom taster på tastaturet) til NVDA-kommandoer. (#1532)
* Du kan nu have forskellige indstillinger til forskellige situationer ved hjælp af konfigurationsprofiler. Profiler kan aktiveres manuelt eller automatisk (f.eks. for en bestemt applikation). (#87, #667, #1913)
* I Microsoft Excel annonceres celler, der er links, nu som links. (#3042)
* I Microsoft Excel rapporteres tilstedeværelsen af kommentarer på en celle nu til brugeren. (#2921)

### Fejlrettelser

* Zend Studio fungerer nu på samme måde som Eclipse. (#3420)
* Den ændrede tilstand for visse check boxer i Microsoft Outlook 2010-meddelelsesregler-dialogen rapporteres nu automatisk. (#3063)
* NVDA vil nu rapportere den fastgjorte tilstand for fastgjorte kontroller såsom faner i Mozilla Firefox. (#3372)
* Det er nu muligt at binde scripts til tastaturkommandoer, der indeholder Alt- og/eller Windows-taster som modifikatorer. Tidligere, hvis dette blev gjort, ville udførelsen af scriptet medføre, at startmenuen eller menulinjen blev aktiveret. (#3472)
* Valg af tekst i dokumenter i gennemsynstilstand (f.eks. ved brug af control+shift+end) får ikke længere tastaturlayoutet til at skifte på systemer med flere installerede tastaturlayouts. (#3472)
* Internet Explorer bør ikke længere gå ned eller blive ubrugelig, når NVDA lukkes. (#3397)
* Fysiske bevægelser og andre hændelser på nogle nyere computere behandles ikke længere som upassende tastetryk. Tidligere kunne dette dæmpe talen og nogle gange udløse NVDA-kommandoer. (#3468)
* NVDA opfører sig nu som forventet i Poedit 1.5.7. Brugere, der anvender tidligere versioner, skal opdatere. (#3485)
* NVDA kan nu læse beskyttede dokumenter i Microsoft Word 2010, uden at Microsoft Word går ned. (#1686)
* Hvis der gives en ukendt kommandolinjeparameter ved opstart af NVDA-distributionspakken, forårsager det ikke længere en endeløs løkke af fejlmeddelelsesdialoger. (#3463)
* NVDA fejler ikke længere i at rapportere alt-tekster for grafik og objekter i Microsoft Word, hvis alt-teksten indeholder anførselstegn eller andre ikke-standardtegn. (#3579)
* Antallet af elementer for visse horisontale lister i gennemsynstilstand er nu korrekt. Tidligere kunne det være dobbelt så stort som det faktiske antal. (#2151)
* Når du trykker på control+a i et Microsoft Excel-regneark, rapporteres den opdaterede markering nu. (#3043)
* NVDA kan nu korrekt læse XHTML-dokumenter i Microsoft Internet Explorer og andre MSHTML-kontroller. (#3542)
* Tastaturindstillingsdialog: hvis ingen tast er valgt som NVDA-tast, præsenteres der en fejlmeddelelse, når dialogen lukkes. Der skal vælges mindst én tast for korrekt brug af NVDA. (#2871)
* I Microsoft Excel annoncerer NVDA nu sammenflettede celler forskelligt fra flere valgte celler. (#3567)
* Gennemsynsmarkøren er ikke længere placeret forkert, når man forlader en dialog eller applikation inde i dokumentet. (#3145)
* Et problem, hvor HumanWare Brailliant BI/B-seriens punktdisplay-driver ikke blev præsenteret som en mulighed i punktindstillinger-dialogen på nogle systemer, selvom et sådant display var tilsluttet via USB, er blevet løst.
* NVDA fejler ikke længere i at skifte til skærmgennemgang, når navigatorobjektet ikke har nogen egentlig skærmplacering. I dette tilfælde placeres gennemgangsmarkøren nu øverst på skærmen. (#3454)
* Et problem, der forårsagede, at Freedom Scientifics punktdisplay-driver fejlede, når porten var indstillet til USB i visse tilfælde, er blevet løst. (#3509, #3662)
* Et problem, hvor taster på Freedom Scientifics punktdisplays ikke blev registreret i visse tilfælde, er blevet løst. (#3401, #3662)

### Ændringer for udviklere

* Du kan specificere den kategori, der skal vises for brugeren for scripts ved hjælp af scriptCategory-attributten på ScriptableObject-klasser og category-attributten på script-metoder. Se dokumentationen for baseObject.ScriptableObject for flere detaljer. (#1532)
* config.save er forældet og kan blive fjernet i en fremtidig udgivelse. Brug config.conf.save i stedet. (#667)
* config.validateConfig er forældet og kan blive fjernet i en fremtidig udgivelse. Tilføjelser, der har brug for dette, bør levere deres egen implementering. (#667, #3632)

## 2013.2

### Nye funktioner

* Understøttelse af Chromium Embedded Framework, som er en webbrowserkontrol, der bruges i flere applikationer. (#3108)
* Ny eSpeak stemmevariant: Iven3.
* I Skype rapporteres nye chatbeskeder automatisk, mens samtalen er fokuseret. (#2298)
* Understøttelse af Tween, inklusive rapportering af fanenavne og mindre snakkesalighed ved læsning af tweets.
* Du kan nu deaktivere visning af NVDA-beskeder på et punktdisplay ved at sætte timeout for beskeder til 0 i punktindstillinger-dialogen. (#2482)
* I Tilføjelsesadministratoren er der nu en "Hent tilføjelser"-knap til at åbne NVDA's tilføjelseswebsted, hvor du kan gennemse og downloade tilgængelige tilføjelser. (#3209)
* I NVDA-velkomstdialogen, som altid vises første gang du starter NVDA, kan du nu specificere, om NVDA skal starte automatisk, når du logger på Windows. (#2234)
* Dvaletilstand aktiveres automatisk, når Dolphin Cicero bruges. (#2055)
* Windows x64-versionen af Miranda IM/Miranda NG understøttes nu. (#3296)
* Søgeforslag på Startskærmen i Windows 8.1 rapporteres automatisk. (#3322)
* Understøttelse af navigering og redigering af regneark i Microsoft Excel 2013. (#3360)
* Freedom Scientific Focus 14 Blue og Focus 80 Blue punktdisplays, samt Focus 40 Blue i visse konfigurationer, der tidligere ikke blev understøttet, understøttes nu, når de er tilsluttet via Bluetooth. (#3307)
* Automatisk fuldførelsesforslag rapporteres nu i Outlook 2010. (#2816)
* Nye punktoversættelsestabeller: Engelsk (U.K.) computerpunkt, Koreansk grad 2, Russisk punkt til computerkode.
* Nyt sprog: Farsi. (#1427)

### Ændringer

* På en touchskærm bevæger en enkelt fingerstrygning til venstre eller højre i objektmodus nu forrige eller næste gennem alle objekter, ikke kun dem i den nuværende container. Brug to-fingerstrygning til venstre eller højre for at udføre den oprindelige handling med at flytte til forrige eller næste objekt i den nuværende container.
* "Rapportér layouttabeller"-check boxen i gennemsynstilstandsindstillingsdialogen er nu blevet omdøbt til "Inkluder layouttabeller" for at afspejle, at hurtignavigation heller ikke vil finde dem, hvis check boxen er slået fra. (#3140)
* Flad gennemgang er blevet erstattet med objekt-, dokument- og skærmgennemgangstilstande. (#2996)
  * Objektgennemgang gennemgår kun tekst inden for navigatorobjektet, dokumentgennemgang gennemgår al tekst i et gennemsynstilstandsdokument (hvis nogen), og skærmgennemgang gennemgår tekst på skærmen for den aktuelle applikation.
  * Kommandoerne, der tidligere bevægede sig til/fra flad gennemgang, skifter nu mellem disse nye gennemgangstilstande.
  * Navigatorobjektet følger automatisk gennemgangsmarkøren, så det forbliver det dybeste objekt på positionen af gennemgangsmarkøren, når det er i dokument- eller skærmgennemgangstilstande.
  * Efter skift til skærmgennemgangstilstand forbliver NVDA i denne tilstand, indtil du eksplicit skifter tilbage til dokument- eller objektgennemgangstilstand.
  * Når du er i dokument- eller objektgennemgangstilstand, kan NVDA automatisk skifte mellem disse to tilstande afhængigt af, om du bevæger dig rundt i et gennemsynstilstandsdokument eller ej.
* Opdateret liblouis punktoversætter til 2.5.3. (#3371)

### Fejlrettelser

* Aktivering af et objekt annoncerer nu handlingen før aktiveringen, snarere end handlingen efter aktiveringen (f.eks. "udvid", når du udvider, i stedet for "skjul"). (#2982)
* Mere præcis læsning og markørsporing i forskellige inputfelter for nyere versioner af Skype, såsom chat- og søgefelter. (#1601, #3036)
* I Skypes liste over seneste samtaler læses antallet af nye hændelser nu for hver samtale, hvis relevant. (#1446)
* Forbedringer i markørsporing og læseorden for højre-til-venstre-tekst skrevet til skærmen, f.eks. redigering af arabisk tekst i Microsoft Excel. (#1601)
* Hurtignavigation til knapper og formularfelter vil nu finde links markeret som knapper for tilgængelighedsformål i Internet Explorer. (#2750)
* I gennemsynstilstand vises indholdet i trævisninger ikke længere, da en fladet repræsentation ikke er nyttig. Du kan trykke på enter på en trævisning for at interagere med den i fokusmodus. (#3023)
* Tryk på alt+nedpil eller alt+uppil for at udvide en komboboks i fokusmodus skifter ikke længere fejlagtigt til gennemsynstilstand. (#2340)
* I Internet Explorer 10 aktiverer tabelceller ikke længere fokusmodus, medmindre de er blevet eksplicit gjort fokusbare af webudvikleren. (#3248)
* NVDA starter ikke længere fejlagtigt, hvis systemtiden er tidligere end sidste opdateringskontrol. (#3260)
* Hvis en statuslinje vises på et punktdisplay, opdateres punktdisplayet, når statuslinjen ændrer sig. (#3258)
* I gennemsynstilstand i Mozilla-applikationer gengives tabeloverskrifter ikke længere to gange. Derudover gengives resuméet, når der også er en overskrift. (#3196)
* Ved skift af input-sprog i Windows 8 taler NVDA nu det korrekte sprog i stedet for det foregående.
* NVDA annoncerer nu IME-konverteringstilstandsændringer i Windows 8.
* NVDA annoncerer ikke længere skrald på skrivebordet, når Google Japanese eller Atok IME inputmetoder bruges. (#3234)
* I Windows 7 og nyere annoncerer NVDA ikke længere upassende talegenkendelse eller berøringsinput som en tastatursprogsændring.
* NVDA annoncerer ikke længere et bestemt specialtegn (0x7f), når du trykker på control+backspace i nogle redaktører, når "tale indtastede tegn" er aktiveret. (#3315)
* eSpeak ændrer ikke længere tonehøjde, volumen osv. upassende, når NVDA læser tekst, der indeholder visse kontroltegn eller XML. (#3334) (tilbageførsel af #437)
* I Java-applikationer meddeles ændringer af etiketten eller værdien af det fokuserede kontrol automatisk og afspejles ved efterfølgende forespørgsler til kontrol. (#3119)
* I Scintilla-kontroller rapporteres linjer nu korrekt, når ordbrydning er aktiveret. (#885)
* I Mozilla-applikationer rapporteres navnet på skrivebeskyttede listeelementer nu korrekt, f.eks. når der navigeres tweets i fokusmodus på twitter.com. (#3327)
* Bekræftelsesdialoger i Microsoft Office 2013 får nu automatisk læst deres indhold op, når de vises.
* Ydelsesforbedringer ved navigation i visse tabeller i Microsoft Word. (#3326)
* NVDA's tabelnavigationskommandoer (control+alt+pile) fungerer bedre i visse Microsoft Word-tabeller, hvor en celle strækker sig over flere rækker.
* Hvis tilføjelsesadministratoren allerede er åben, fejler det ikke længere eller gør det umuligt at lukke tilføjelsesadministratoren, hvis du aktiverer den igen (enten fra Værktøjsmenuen eller ved at åbne en tilføjelsesfil). (#3351)
* NVDA fryser ikke længere i visse dialoger, når japansk eller kinesisk Office 2010 IME er i brug. (#3064)
* Flere mellemrum komprimeres ikke længere til kun ét mellemrum på punktdisplays. (#1366)
* Zend Eclipse PHP Developer Tools fungerer nu på samme måde som Eclipse. (#3353)
* I Internet Explorer er det igen ikke nødvendigt at trykke på tab for at interagere med et indlejret objekt (f.eks. Flash-indhold), efter at du har trykket på enter på det. (#3364)
* Ved redigering af tekst i Microsoft PowerPoint rapporteres den sidste linje ikke længere som linjen ovenover, hvis den sidste linje er tom. (#3403)
* I Microsoft PowerPoint bliver objekter ikke længere talt to gange, når du vælger dem eller vælger at redigere dem. (#3394)
* NVDA får ikke længere Adobe Reader til at gå ned eller fryse for visse dårligt formaterede PDF-dokumenter, der indeholder rækker uden for tabeller. (#3399)
* NVDA registrerer nu korrekt næste dias med fokus, når et dias slettes i Microsoft PowerPoints miniaturer. (#3415)

### Ændringer for udviklere

* windowUtils.findDescendantWindow er blevet tilføjet til at søge efter et efterkommer-vindue (HWND), der matcher den specificerede synlighed, kontrol-ID og/eller klassens navn.
* Den fjerntliggende Python-konsol tidsudløber ikke længere efter 10 sekunder, mens den venter på input. (#3126)
* Inkluderingen af bisect-modulet i binære builds er forældet og kan blive fjernet i en fremtidig udgivelse. (#3368)
  * Tilføjelser, der er afhængige af bisect (inklusive urllib2-modulet), bør opdateres til at inkludere dette modul.

## 2013.1.1

Denne udgivelse retter problemet, hvor NVDA gik ned ved opstart, hvis det var konfigureret til at bruge det irske sprog, samt indeholder opdateringer til oversættelser og nogle andre fejlrettelser.

### Fejlrettelser

* Korrekte tegn produceres, når der indtastes i NVDA's eget brugergrænseflade ved brug af en koreansk eller japansk inputmetode, mens det er den standardmetode. (#2909)
* I Internet Explorer og andre MSHTML-kontroller behandles felter markeret som indeholdende en ugyldig indtastning nu korrekt. (#3256)
* NVDA går ikke længere ned ved opstart, hvis det er konfigureret til at bruge det irske sprog.

## 2013.1

Højdepunkter for denne udgivelse inkluderer et mere intuitivt og konsistent tastaturlayout til bærbare computere; grundlæggende understøttelse af Microsoft PowerPoint; understøttelse af lange beskrivelser i webbrowsere; og understøttelse af input af computerpunkt for punktdisplays, der har et punkt-tastatur.

### Vigtigt

#### Nyt tastaturlayout til bærbare computere

Tastaturlayoutet til bærbare computere er blevet fuldstændig redesignet for at gøre det mere intuitivt og konsistent.
Det nye layout bruger piletasterne i kombination med NVDA-tasten og andre modifikatorer til læsekommandoer.

Bemærk følgende ændringer til ofte anvendte kommandoer:

| Navn |Tast|
|---|---|
|Sig alt |NVDA+a|
|Læs aktuel linje |NVDA+l|
|Læs aktuel tekstmarkering |NVDA+shift+s|
|Rapportér statuslinje |NVDA+shift+end|

Derudover er alle objektnavigation-, tekstgennemgang-, museklik- og syntese-indstillingsringkommandoer blevet ændret.
Se venligst dokumentet [Kommandoernes hurtigreference](keyCommands.html) for de nye taster.

### Nye funktioner

* Grundlæggende understøttelse af redigering og læsning af Microsoft PowerPoint-præsentationer. (#501)
* Grundlæggende understøttelse af læsning og skrivning af beskeder i Lotus Notes 8.5. (#543)
* Understøttelse af automatisk sprogskift ved læsning af dokumenter i Microsoft Word. (#2047)
* I gennemsynstilstand for MSHTML (f.eks. Internet Explorer) og Gecko (f.eks. Firefox) meddeles tilstedeværelsen af lange beskrivelser nu. Det er også muligt at åbne den lange beskrivelse i et nyt vindue ved at trykke på NVDA+d. (#809)
* Meddelelser i Internet Explorer 9 og nyere annonceres nu (såsom indholdsblokering eller filoverførsler). (#2343)
* Automatisk rapportering af tabelrække- og kolonneoverskrifter understøttes nu i gennemsynstilstandsdokumenter i Internet Explorer og andre MSHTML-kontroller. (#778)
* Nye sprog: Aragonese, irsk
* Nye punktoversættelsestabeller: Dansk grad 2, koreansk grad 1. (#2737)
* Understøttelse af punktdisplays tilsluttet via Bluetooth på en computer, der kører Bluetooth Stack for Windows af Toshiba. (#2419)
* Understøttelse af portvalg ved brug af Freedom Scientific displays (Automatisk, USB eller Bluetooth).
* Understøttelse af BrailleNote-familien af notatapparater fra HumanWare, når de fungerer som punktterminaler for en skærmlæser. (#2012)
* Understøttelse af ældre modeller af Papenmeier BRAILLEX punktdisplays. (#2679)
* Understøttelse af input af computerpunkt for punktdisplays, der har et punkt-tastatur. (#808)
* Nye tastaturindstillinger, der giver mulighed for at vælge, om NVDA skal afbryde tale for indtastede tegn og/eller Enter-tasten. (#698)
* Understøttelse af flere browsere baseret på Google Chrome: Rockmelt, BlackHawk, Comodo Dragon og SRWare Iron. (#2236, #2813, #2814, #2815)

### Ændringer

* Opdateret liblouis punktoversætter til 2.5.2. (#2737)
* Tastaturlayoutet til bærbare computere er blevet fuldstændig redesignet for at gøre det mere intuitivt og konsistent. (#804)
* Opdateret eSpeak talesyntese til 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Fejlrettelser

* Hurtignavigationskommandoerne for at springe til næste eller forrige separator i gennemsynstilstand fungerer nu i Internet Explorer og andre MSHTML-kontroller. (#2781)
* Hvis NVDA falder tilbage til eSpeak eller ingen tale på grund af den konfigurerede talesyntese, der fejler ved NVDA-start, sættes den konfigurerede valgmulighed ikke længere automatisk til den tilbagefaldssyntese. Det betyder, at den oprindelige talesyntese forsøges igen næste gang NVDA starter. (#2589)
* Hvis NVDA falder tilbage til ingen punkt på grund af det konfigurerede punktdisplay, der fejler ved NVDA-start, sættes det konfigurerede display ikke længere automatisk til ingen punkt. Det betyder, at det oprindelige display forsøges igen næste gang NVDA starter. (#2264)
* I gennemsynstilstand i Mozilla-applikationer gengives opdateringer til tabeller nu korrekt. For eksempel rapporteres række- og kolonnekoordinater i opdaterede celler, og tabelnavigation fungerer som det skal. (#2784)
* I gennemsynstilstand i webbrowsere gengives visse klikbare, ulabelerede grafik, der tidligere ikke blev gengivet, nu korrekt. (#2838)
* Tidligere og nyere versioner af SecureCRT understøttes nu. (#2800)
* For inputmetoder som Easy Dots IME under XP rapporteres læsestrengen nu korrekt.
* Kandidatlisten i den kinesiske forenklede Microsoft Pinyin inputmetode under Windows 7 læses nu korrekt ved skift af sider med venstre og højre pil samt ved første åbning med hjemmetasten.
* Når tilpassede symboludtaleoplysninger gemmes, fjernes det avancerede "bevar"-felt ikke længere. (#2852)
* Når automatisk opdateringskontrol deaktiveres, skal NVDA ikke længere genstartes for at ændringen træder i kraft.
* NVDA fejler ikke længere ved opstart, hvis en tilføjelse ikke kan fjernes, fordi dens bibliotek i øjeblikket er i brug af en anden applikation. (#2860)
* Fanebladsetiketter i DropBox's præferencedialog kan nu ses med flad gennemgang.
* Hvis indtastningssproget ændres til noget andet end standarden, registrerer NVDA nu tasterne korrekt til kommandoer og input-hjælpetilstand.
* For sprog som tysk, hvor "+" (plustegnet) er en enkelt tast på tastaturet, er det nu muligt at binde kommandoer til det ved at bruge ordet "plus". (#2898)
* I Internet Explorer og andre MSHTML-kontroller rapporteres blokcitater nu, hvor det er passende. (#2888)
* HumanWare Brailliant BI/B-seriens punktdisplay-driver kan nu vælges, når displayet er tilsluttet via Bluetooth, men aldrig har været tilsluttet via USB.
* Filtrering af elementer i gennemsynstilstandselementlisten med filtertekst med store bogstaver returnerer nu storebogstavs-insensitive resultater ligesom små bogstaver, i stedet for slet ingenting. (#2951)
* I Mozilla-browsere kan gennemsynstilstand igen bruges, når Flash-indhold er fokuseret. (#2546)
* Når du bruger en punkttabel med forkortet punkt og udvider til computer braille for ordet ved markøren, placeres punktmarkøren nu korrekt, når den er placeret efter et ord, hvor et tegn er repræsenteret af flere punktceller (f.eks. store bogstaver, bogstavtegn, nummertegn osv.). (#2947)
* Tekstmarkering vises nu korrekt på et punktdisplay i applikationer som Microsoft Word 2003 og Internet Explorer-redigeringsfelter.
* Det er igen muligt at vælge tekst i en bagudgående retning i Microsoft Word, mens punkt er aktiveret.
* Ved gennemgang, backspace eller sletning af tegn i Scintilla-redigeringsfelter meddeler NVDA korrekt flertalsbyte-tegn. (#2855)
* NVDA fejler ikke længere i at installere, når brugerens profilsti indeholder visse flertalsbyte-tegn. (#2729)
* Rapportering af grupper for ListView-kontroller (SysListview32) i 64-bit-applikationer forårsager ikke længere en fejl.
* I gennemsynstilstand i Mozilla-applikationer behandles tekstindhold ikke længere fejlagtigt som redigerbart i nogle sjældne tilfælde. (#2959)
* I IBM Lotus Symphony og OpenOffice flytter markøren nu gennemgangsmarkøren, hvis det er relevant.
* Adobe Flash-indhold er nu tilgængeligt i Internet Explorer i Windows 8. (#2454)
* Løst Bluetooth-understøttelse for Papenmeier Braillex Trio. (#2995)
* Løst manglende evne til at bruge visse Microsoft Speech API version 5-stemmer såsom Koba Speech 2-stemmer. (#2629)
* I applikationer, der bruger Java Access Bridge, opdateres punktdisplays nu korrekt, når markøren flytter sig i redigerbare tekstfelter. (#3107)
* Understøttelse af form-landmærket i gennemsynstilstandsdokumenter, der understøtter landmærker. (#2997)
* eSpeak syntesedriver håndterer nu læsning af tegn mere passende (f.eks. meddeler et fremmed brevs navn eller værdi i stedet for kun dets lyd eller generelle navn). (#3106)
* NVDA fejler ikke længere i at kopiere brugerindstillinger til brug på logon- og andre sikre skærme, når brugerens profilsti indeholder ikke-ASCII-tegn. (#3092)
* NVDA fryser ikke længere, når asiatiske tegn input bruges i nogle .NET-applikationer. (#3005)
* Det er nu muligt at bruge gennemsynstilstand til sider i Internet Explorer 10, når de er i standardtilstand; f.eks. [www.gmail.com](http://www.gmail.com) login-side. (#3151)

### Ændringer for udviklere

* Punktdisplay-drivere kan nu understøtte manuel portvalg. (#426)
  * Dette er mest nyttigt for punktdisplays, der understøtter forbindelse via en legacy-serielport.
  * Dette gøres ved hjælp af getPossiblePorts-klassens metode på BrailleDisplayDriver-klassen.
* Punktinput fra punkt-tastaturer understøttes nu. (#808)
  * Punktinput er dækket af brailleInput.BrailleInputGesture-klassen eller en underklasse deraf.
  * Underklasser af braille.BrailleDisplayGesture (som implementeret i punktdisplay-drivere) kan også arve fra brailleInput.BrailleInputGesture. Dette tillader displaykommandoer og punktinput at blive behandlet af den samme gestureklasse.
* Du kan nu bruge comHelper.getActiveObject til at få et aktivt COM-objekt fra en normal proces, når NVDA kører med UIAccess-privilegiet. (#2483)

## 2012.3

Højdepunkter i denne udgivelse inkluderer understøttelse af asiatisk tegninput, eksperimentel understøttelse af berøringsskærme i Windows 8, rapportering af sidetal og forbedret understøttelse af tabeller i Adobe Reader, tabelnavigationskommandoer i fokuserede tabelrækker og Windows listevisningskontroller, understøttelse af flere punktdisplays samt rapportering af række- og kolonneoverskrifter i Microsoft Excel.

### Nye funktioner

* NVDA kan nu understøtte asiatisk tegninput ved hjælp af IME og teksttjenesteinputmetoder i alle applikationer, herunder:
 * Rapportering og navigation af kandidatlisten;
 * Rapportering og navigation af sammensætningsstrenge; og
 * Rapportering af læsestrenge.
* Tilstedeværelsen af understregning og gennemstregning rapporteres nu i Adobe Reader-dokumenter. (#2410)
* Når funktionen Klæbetaster i Windows er aktiveret, vil NVDA-modifikatortasten nu opføre sig som andre modifikatortaster. Dette gør det muligt at bruge NVDA-modifikatortasten uden at skulle holde den nede, mens du trykker på andre taster. (#230)
* Automatisk rapportering af kolonne- og rækkeoverskrifter understøttes nu i Microsoft Excel. Tryk på NVDA+shift+c for at indstille rækken, der indeholder kolonneoverskrifter, og NVDA+shift+r for at indstille kolonnen, der indeholder rækkeoverskrifter. Tryk hurtigt to gange på en af kommandoerne for at rydde indstillingen. (#1519)
* Understøttelse af HIMS Braille Sense, Braille EDGE og SyncBraille punktdisplays. (#1266, #1267)
* Når Toast-notifikationer i Windows 8 vises, vil NVDA rapportere dem, hvis rapportering af hjælpeballoner er aktiveret. (#2143)
* Eksperimentel understøttelse af berøringsskærme i Windows 8, herunder:
 * Læsning af tekst direkte under din finger, mens du bevæger den;
 * Mange kommandoer til objektnavigation, tekstgennemgang og andre NVDA-kommandoer.
* Understøttelse af VIP Mud. (#1728)
* I Adobe Reader præsenteres tabeloversigter, hvis de findes. (#2465)
* I Adobe Reader kan række- og kolonneoverskrifter nu rapporteres i tabeller. (#2193, #2527, #2528)
* Nye sprog: Amharisk, Koreansk, Nepalesisk, Slovensk.
* NVDA kan nu læse autofuldførelsesforslag, når du indtaster e-mailadresser i Microsoft Outlook 2007. (#689)
* Nye eSpeak-stemmevarianter: Gene, Gene2. (#2512)
* I Adobe Reader kan sidetal nu rapporteres. (#2534)
 * I Reader XI rapporteres sidemærkninger, hvis de er tilgængelige, hvilket afspejler ændringer i sidetalsnummerering i forskellige sektioner. I tidligere versioner er dette ikke muligt, og kun sekventielle sidetal rapporteres.
* Det er nu muligt at nulstille NVDAs konfiguration til fabriksindstillinger ved at trykke NVDA+control+r tre gange hurtigt eller vælge Nulstil til fabriksindstillinger fra NVDA-menuen. (#2086)
* Understøttelse af Seika version 3, 4 og 5 samt Seika80 punktdisplays fra Nippon Telesoft. (#2452)
* De første og sidste top-markørknapper på Freedom Scientific PAC Mate og Focus punktdisplays kan nu bruges til at rulle bagud og fremad. (#2556)
* Mange flere funktioner understøttes nu på Freedom Scientific Focus punktdisplays såsom avancerede bjælker, vippebjælker og visse prikkombinationer til almindelige handlinger. (#2516)
* I applikationer, der bruger IAccessible2 såsom Mozilla-applikationer, kan række- og kolonneoverskrifter nu rapporteres uden for gennemsynstilstand. (#926)
* Foreløbig understøttelse af dokumentkontrollen i Microsoft Word 2013. (#2543)
* Tekstjustering kan nu rapporteres i applikationer, der bruger IAccessible2 såsom Mozilla-applikationer. (#2612)
* Når en tabelrække eller en standard Windows listevisningskontrol med flere kolonner er fokuseret, kan du nu bruge tabelnavigationskommandoer til at få adgang til individuelle celler. (#828)
* Nye punkttabeloversættelser: Estisk grad 0, Portugisisk 8-punkts computer braille, Italiensk 6-punkts computer braille. (#2319, #2662)
* Hvis NVDA er installeret på systemet, vil direkte åbning af en NVDA-tilføjelsespakke (f.eks. fra Windows Stifinder eller efter download i en webbrowser) installere den i NVDA. (#2306)
* Understøttelse af nyere modeller af Papenmeier BRAILLEX punktdisplays. (#1265)
* Positionsoplysninger (f.eks. 1 af 4) rapporteres nu for listeelementer i Windows Stifinder på Windows 7 og nyere. Dette inkluderer også alle UIAutomation-kontroller, der understøtter itemIndex- og itemCount-egenskaberne. (#2643)

### Ændringer

* I dialogen for NVDA-gennemgangscursorindstillinger er indstillingen Følg tastaturfokus blevet omdøbt til Følg systemfokus for konsistens med terminologien, der bruges andre steder i NVDA.
* Når punkt er tøjret til læsemarkøren, og markøren er på et objekt, der ikke er et tekstobjekt (f.eks. et redigerbart tekstfelt), vil markørknapperne nu aktivere objektet. (#2386)
* Indstillingen Gem konfiguration ved afslutning er nu som standard aktiveret for nye konfigurationer.
* Når du opdaterer en tidligere installeret kopi af NVDA, tvinges genvejstasten til skrivebordet ikke længere tilbage til control+alt+n, hvis den manuelt blev ændret til noget andet af brugeren. (#2572)
* Tilføjelseslisten i håndtering af tilføjelser viser nu pakkenavnet før dens status. (#2548)
* Hvis du installerer den samme eller en anden version af en allerede installeret tilføjelse, vil NVDA spørge, om du vil opdatere tilføjelsen, i stedet for blot at vise en fejl og afbryde installationen. (#2501)
* Objektnavigationskommandoer (undtagen kommandoen til at rapportere det aktuelle objekt) rapporterer nu med mindre detaljer. Du kan stadig få den ekstra information ved at bruge kommandoen til at rapportere det aktuelle objekt. (#2560)
* Opdateret liblouis-punktskriftoversætter til version 2.5.1. (#2319, #2480, #2662, #2672)
* NVDA's genvejskommandodokument er blevet omdøbt til Kommandoer Hurtig Reference, da det nu inkluderer berøringskommandoer samt tastaturkommandoer.
* Elementlisten i gennemsynstilstand husker nu den sidste viste elementtype (f.eks. links, overskrifter eller landemærker) hver gang dialogen vises inden for samme NVDA-session. (#365)
* De fleste Metro-apps i Windows 8 (f.eks. Mail, Kalender) aktiverer ikke længere gennemsynstilstand for hele appen.
* Opdateret Handy Tech BrailleDriver COM-Server til version 1.4.2.0.

### Fejlrettelser

* I Windows Vista og senere behandler NVDA ikke længere fejlagtigt Windows-tasten som nede, når du låser op for Windows efter at have låst det ved at trykke på Windows+l. (#1856)
* I Adobe Reader genkendes rækkeoverskrifter nu korrekt som tabelceller; dvs. koordinater rapporteres, og de kan tilgås ved hjælp af tabelnavigationskommandoer. (#2444)
* I Adobe Reader håndteres tabelceller, der spænder over mere end én kolonne og/eller række, nu korrekt. (#2437, #2438, #2450)
* NVDA-distributionspakken kontrollerer nu sin integritet, før den udføres. (#2475)
* Midlertidige downloadfiler fjernes nu, hvis downloading af en NVDA-opdatering mislykkes. (#2477)
* NVDA fryser ikke længere, når det kører som administrator, mens brugerens konfiguration kopieres til systemkonfigurationen (til brug på Windows-logon og andre sikre skærme). (#2485)
* Felter på Windows 8-startskærmen præsenteres nu bedre i tale og punkt. Navnet gentages ikke længere, ikke valgt rapporteres ikke længere på alle felter, og live-statusoplysninger præsenteres som feltets beskrivelse (f.eks. den aktuelle temperatur for Vejr-feltet).
* Adgangskoder annonceres ikke længere, når du læser adgangskodefelter i Microsoft Outlook og andre standardredigeringsfelter, der er markeret som beskyttede. (#2021)
* I Adobe Reader afspejles ændringer i formularfelter nu korrekt i gennemsynstilstand. (#2529)
* Forbedringer i understøttelsen af Microsoft Words stavekontrol, herunder mere præcis læsning af den aktuelle stavefejl og muligheden for at understøtte stavekontrollen, når der køres en installeret kopi af NVDA på Windows Vista eller højere.
* Tilføjelser, der indeholder filer med ikke-engelske tegn, kan nu installeres korrekt i de fleste tilfælde. (#2505)
* I Adobe Reader går sproget for teksten ikke længere tabt, når det opdateres eller rulles til. (#2544)
* Ved installation af en tilføjelse viser bekræftelsesdialogen nu korrekt det lokaliserede navn på tilføjelsen, hvis det er tilgængeligt. (#2422)
* I applikationer, der bruger UI Automation (f.eks. .net og Silverlight-applikationer), er beregningen af numeriske værdier for kontroller såsom skyderkontroller blevet rettet. (#2417)
* Konfigurationen for rapportering af statusbjælker respekteres nu for ubestemte statusbjælker vist af NVDA ved installation, oprettelse af en bærbar kopi osv. (#2574)
* NVDA-kommandoer kan ikke længere udføres fra et punktdisplay, mens en sikker Windows-skærm (såsom låseskærmen) er aktiv. (#2449)
* I gennemsynstilstand opdateres punkt nu, hvis teksten, der vises, ændres. (#2074)
* Når du er på en sikker Windows-skærm som låseskærmen, ignoreres beskeder fra applikationer, der taler eller viser punkt direkte via NVDA.
* I gennemsynstilstand er det ikke længere muligt at falde af bunden af dokumentet med højre pil-tasten, når du er på det sidste tegn, eller ved at hoppe til slutningen af en container, når denne container er det sidste element i dokumentet. (#2463)
* Ekstra indhold medtages ikke længere fejlagtigt, når teksten i dialogbokse i webapplikationer rapporteres (specifikt ARIA-dialoger uden aria-describedby-attribut). (#2390)
* NVDA rapporterer eller lokaliserer ikke længere visse redigeringsfelter forkert i MSHTML-dokumenter (f.eks. Internet Explorer), specifikt hvor en eksplicit ARIA-rolle er blevet brugt af websideforfatteren. (#2435)
* Backspace-tasten håndteres nu korrekt, når ord, der er skrevet, tales i Windows kommandokonsoller. (#2586)
* Cellekoordinater i Microsoft Excel vises igen i punkt.
* I Microsoft Word sidder NVDA ikke længere fast på et afsnit med listeformatering, når man forsøger at navigere ud over en punkt eller nummerering med venstre pil eller control+venstre pil. (#2402)
* I gennemsynstilstand i Mozilla-applikationer gengives elementerne i visse listebokse (specifikt ARIA-listebokse) ikke længere forkert.
* I gennemsynstilstand i Mozilla-applikationer er visse kontroller, der blev gengivet med en forkert etiket eller kun mellemrum, nu gengivet med den korrekte etiket.
* I gennemsynstilstand i Mozilla-applikationer er noget overflødigt mellemrum fjernet.
* I gennemsynstilstand i webbrowsere ignoreres visse grafikfiler, der eksplicit er markeret som præsentationelle (specifikt med en alt=""-attribut), nu korrekt.
* I webbrowsere skjuler NVDA nu indhold, der er markeret som skjult for skærmlæsere (specifikt ved hjælp af aria-hidden-attributten). (#2117)
* Negative valutabeløb (f.eks. -$123) tales nu korrekt som negative, uanset symboletiveauet. (#2625)
* Under læs alt vil NVDA ikke længere fejlagtigt vende tilbage til standardsproget, hvor en linje ikke afslutter en sætning. (#2630)
* Skriftoplysninger registreres nu korrekt i Adobe Reader 10.1 og senere. (#2175)
* I Adobe Reader, hvis der leveres alternativ tekst, vil kun denne tekst blive gengivet. Tidligere blev overflødig tekst undertiden inkluderet. (#2174)
* Hvor et dokument indeholder en applikation, er applikationens indhold ikke længere inkluderet i gennemsynstilstand. Dette forhindrer uventet bevægelse ind i applikationen under navigation. Du kan interagere med applikationen på samme måde som med indlejrede objekter. (#990)
* I Mozilla-applikationer rapporteres værdien af drejeknapper nu korrekt, når den ændres. (#2653)
* Opdateret understøttelse af Adobe Digital Editions, så det fungerer i version 2.0. (#2688)
* Ved at trykke på NVDA+pil op, mens du er på en combo box i Internet Explorer og andre MSHTML-dokumenter, vil NVDA ikke længere fejlagtigt læse alle elementer. Kun det aktive element læses. (#2337)
* Taleordbøger gemmes nu korrekt, når der bruges et nummer (#) i mønster- eller erstatningsfelterne. (#961)
* Gennemsynstilstand for MSHTML-dokumenter (f.eks. Internet Explorer) viser nu korrekt synligt indhold indeholdt i skjult indhold (specifikt elementer med en style af visibility:visible inde i et element med style visibility:hidden). (#2097)
* Links i Windows XP's sikkerhedscenter rapporterer ikke længere tilfældige tegn efter deres navne. (#1331)
* UI Automation-tekstkontroller (f.eks. søgefeltet i Windows 7 Startmenuen) annonceres nu korrekt, når musen bevæges over dem, i stedet for at forblive tavse.
* Tastaturlayoutændringer rapporteres ikke længere under læs alt, hvilket var særligt problematisk for flersprogede dokumenter, herunder arabisk tekst. (#1676)
* Det samlede indhold af nogle UI Automation-redigerbare tekstkontroller (f.eks. søgefeltet i Windows 7/8 Startmenuen) annonceres ikke længere, hver gang det ændres.
* Når du bevæger dig mellem grupper på Windows 8-startskærmen, annoncerer ulabelerede grupper ikke længere deres første felt som navnet på gruppen. (#2658)
* Når du åbner Windows 8-startskærmen, placeres fokus korrekt på det første felt i stedet for at hoppe til rodmappen af startskærmen, hvilket kan forvirre navigation. (#2720)
* NVDA vil ikke længere undlade at starte, når brugerens profilsti indeholder visse multibyte-tegn. (#2729)
* I gennemsynstilstand i Google Chrome gengives fanebladsteksten nu korrekt.
* I gennemsynstilstand rapporteres menuknapper nu korrekt.
* I OpenOffice.org/LibreOffice Calc fungerer læsning af regnearksceller nu korrekt. (#2765)
* NVDA kan igen fungere i Yahoo! Mail-meddelelseslisten, når det bruges fra Internet Explorer. (#2780)

### Ændringer for udviklere

* Tidligere logfil kopieres nu til nvda-old.log ved NVDA-initialisering. Hvis NVDA derfor går ned eller genstartes, er logoplysninger fra den session stadig tilgængelige til inspektion. (#916)
* Hentning af rolleegenskaben i chooseNVDAObjectOverlayClasses forårsager ikke længere, at rollen er forkert og derfor ikke rapporteres ved fokus for visse objekter såsom Windows kommandokonsoller og Scintilla-kontroller. (#2569)
* NVDA-indstillinger, værktøjer og hjælpemenuer er nu tilgængelige som attributter på gui.mainFrame.sysTrayIcon, navngivet preferencesMenu, toolsMenu og helpMenu. Dette gør det lettere for plugins at tilføje elementer til disse menuer.
* navigatorObject_doDefaultAction-scriptet i globalCommands er blevet omdøbt til review_activate.
* Gettext-meddelelsessammenhænge understøttes nu. Dette gør det muligt at definere flere oversættelser for en enkelt engelsk besked afhængigt af konteksten. (#1524)
 * Dette gøres ved hjælp af pgettext(kontekst, besked)-funktionen.
 * Dette understøttes både for NVDA selv og tilføjelser.
 * xgettext og msgfmt fra GNU gettext skal bruges til at oprette eventuelle PO- og MO-filer. Python-værktøjerne understøtter ikke meddelelsessammenhænge.
 * For xgettext skal du angive --keyword=pgettext:1c,2-kommandoen for at aktivere meddelelsessammenhænge.
 * Se http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts for mere information.
* Det er nu muligt at få adgang til indbyggede NVDA-moduler, hvor de er blevet tilsidesat af tredjepartsmoduler. Se nvdaBuiltin-modulet for detaljer.
* Oversættelse af en tilføjelse kan nu bruges inden for add-on installTasks-modulet. (#2715)

## 2012.2.1

Denne udgivelse adresserer flere potentielle sikkerhedsproblemer (ved at opgradere Python til version 2.7.3).

## 2012.2

Højdepunkter i denne udgivelse inkluderer en indbygget installations- og bærbar oprettelsesfunktion, automatiske opdateringer, nem styring af nye NVDA-tilføjelser, annoncering af grafik i Microsoft Word, understøttelse af Windows 8 Metro-apps samt flere vigtige fejlrettelser.

### Nye funktioner

* NVDA kan nu automatisk kontrollere for, downloade og installere opdateringer. (#73)
* Udvidelse af NVDAs funktionalitet er blevet lettere med tilføjelsen af en Tilføjelsesadministrator (findes under Værktøjer i NVDA-menuen), der giver dig mulighed for at installere og afinstallere nye NVDA-tilføjelsespakker (.nvda-tilføjelser), der indeholder plugins og drivere. Bemærk, at tilføjelsesadministratoren ikke viser ældre brugerdefinerede plugins og drivere, der manuelt er kopieret til din konfigurationsmappe. (#213)
* Mange flere almindelige NVDA-funktioner fungerer nu i Windows 8 Metro-stil apps, når der bruges en installeret version af NVDA, herunder tale af indtastede tegn og gennemsynstilstand for webdokumenter (inkluderer understøttelse af metro-versionen af Internet Explorer 10). Bærbare kopier af NVDA kan ikke få adgang til Metro-stil apps. (#1801)
* I gennemsynstilstandsdokumenter (Internet Explorer, Firefox osv.) kan du nu springe til starten og forbi slutningen af visse indeholdende elementer (såsom lister og tabeller) med shift+, og , henholdsvis. (#123)
* Nyt sprog: Græsk.
* Grafik og alternativ tekst rapporteres nu i Microsoft Word-dokumenter. (#2282, #1541)

### Ændringer

* Annoncering af cellekoordinater i Microsoft Excel sker nu efter indholdet i stedet for før, og er nu kun inkluderet, hvis indstillingerne rapporter tabeller og rapporter tabelcellekoordinater er aktiveret i dialogen for dokumentformateringsindstillinger. (#320)
* NVDA distribueres nu i én pakke. I stedet for separate bærbare og installerede versioner er der nu kun én fil, der, når den køres, vil starte en midlertidig kopi af NVDA og vil give dig mulighed for at installere eller generere en bærbar distribution. (#1715)
* NVDA installeres nu altid i Programfiler på alle systemer. Opdatering af en tidligere installation vil også automatisk flytte den, hvis den ikke tidligere var installeret der.

### Fejlrettelser

* Med automatisk sprogskift aktiveret rapporteres indhold som alternativ tekst for grafik og etiketter for andre bestemte kontroller i Mozilla Gecko (f.eks. Firefox) nu på det korrekte sprog, hvis det er markeret korrekt.
* Læs alt i BibleSeeker (og andre TRxRichEdit-kontroller) stopper ikke længere midt i en passage.
* Lister i Windows 8 Stifinders filattributter (tilladelser-fanen) og i Windows 8 Windows Update læses nu korrekt.
* Rettede mulige frysninger i MS Word, som kunne opstå, når det tog mere end 2 sekunder at hente tekst fra et dokument (ekstremt lange linjer eller indholdsfortegnelser). (#2191)
* Registrering af ordbrud fungerer nu korrekt, hvor mellemrum efterfølges af visse tegnsætninger. (#1656)
* I gennemsynstilstand i Adobe Reader er det nu muligt at navigere til overskrifter uden niveau ved hjælp af hurtignavigation og elementlisten. (#2181)
* I Winamp opdateres punkt nu korrekt, når du bevæger dig til et andet element i afspilningseditoren. (#1912)
* Træet i elementlisten (tilgængelig for gennemsynstilstandsdokumenter) er nu korrekt størrelsesjusteret til at vise teksten for hvert element. (#2276)
* I applikationer, der bruger Java Access Bridge, præsenteres redigerbare tekstfelter nu korrekt i punkt. (#2284)
* I applikationer, der bruger Java Access Bridge, rapporteres der ikke længere mærkelige tegn i visse tilfælde i redigerbare tekstfelter. (#1892)
* I applikationer, der bruger Java Access Bridge, rapporteres den aktuelle linje korrekt, når du er i slutningen af et redigerbart tekstfelt. (#1892)
* I gennemsynstilstand i applikationer, der bruger Mozilla Gecko 14 og senere (f.eks. Firefox 14), fungerer hurtignavigation nu for blokcitater og indlejrede objekter. (#2287)
* I Internet Explorer 9 læser NVDA ikke længere uønsket indhold, når fokus flyttes ind i visse landemærker eller fokuserbare elementer (specifikt et div-element, der er fokuserbart eller har en ARIA-landemærkerolle).
* NVDA-ikonet for genveje på skrivebordet og i startmenuen vises nu korrekt på 64-bit versioner af Windows. (#354)

### Ændringer for udviklere

* På grund af udskiftningen af den tidligere NSIS-installationsprogram for NVDA med en indbygget installationsprogram i Python, er det ikke længere nødvendigt for oversættere at vedligeholde en langstrings.txt-fil til installationsprogrammet. Alle lokaliseringsstrenge håndteres nu af gettext po-filer.

## 2012.1

Højdepunkter i denne udgivelse inkluderer funktioner til mere flydende læsning af punkt; indikation af dokumentformatering i punkt; adgang til meget mere formateringsinformation og forbedret ydeevne i Microsoft Word; samt understøttelse af iTunes Store.

### Nye funktioner

* NVDA kan annoncere antallet af foranstillede tabulatorer og mellemrum på den aktuelle linje i den rækkefølge, de er indtastet. Dette kan aktiveres ved at vælge rapportér linjeindrykning i dialogboksen for dokumentformatering. (#373)
* NVDA kan nu registrere tastetryk, der genereres fra alternativ tastaturinputemulering såsom on-screen tastaturer og talegenkendelsessoftware.
* NVDA kan nu registrere farver i Windows kommandokonsoller.
* Fed, kursiv og understregning indikeres nu i punkt ved hjælp af tegn, der er passende til den konfigurerede punkttabel. (#538)
* Meget mere information rapporteres nu i Microsoft Word-dokumenter, herunder:
 * Inline-information såsom fodnote- og slutnote-numre, overskriftsniveauer, tilstedeværelse af kommentarer, tabelnestingsniveauer, links og tekstfarve;
 * Rapportering ved indgang i dokumentsektioner såsom kommentarafsnit, fodnoter og slutnoter samt header- og footerafsnit.
* Punkt indikerer nu markeret tekst ved hjælp af punkterne 7 og 8. (#889)
* Punkt rapporterer nu information om kontroller inden for dokumenter såsom links, knapper og overskrifter. (#202)
* Understøttelse af hedo ProfiLine og MobilLine USB punktdisplays. (#1863, #1897)
* NVDA undgår nu som standard at opdele ord i punkt, hvor det er muligt. Dette kan deaktiveres i dialogboksen for punktindstillinger. (#1890, #1946)
* Det er nu muligt at få vist punkt pr. afsnit i stedet for linjer, hvilket kan gøre det lettere at læse større tekstmængder mere flydende. Dette kan konfigureres ved at bruge indstillingen Læs pr. afsnit i dialogboksen for punktindstillinger. (#1891)
* I gennemsynstilstand kan du aktivere objektet under markøren ved hjælp af et punktdisplay. Dette gøres ved at trykke på markørknapperne, hvor cursoren er placeret (hvilket betyder, at du skal trykke på den to gange, hvis cursoren ikke allerede er der). (#1893)
* Grundlæggende understøttelse af webområder i iTunes såsom Store. Andre applikationer, der bruger WebKit 1, kan også understøttes. (#734)
* I bøger i Adobe Digital Editions 1.8.1 og senere vendes sider nu automatisk, når du bruger læs alt. (#1978)
* Nye punkttabeloversættelser: Portugisisk grad 2, Islandsk 8-punkts computer braille, Tamilsk grad 1, Spansk 8-punkts computer braille, Farsi grad 1. (#2014)
* Du kan nu konfigurere, om rammer i dokumenter skal rapporteres fra dialogboksen for dokumentformateringsindstillinger. (#1900)
* Dvaletilstand aktiveres automatisk, når du bruger OpenBook. (#1209)
* I Poedit kan oversættere nu læse oversættertilføjede og automatisk udtrukne kommentarer. Meddelelser, der er uoversatte eller usikre, markeres med en stjerne, og der høres et bip, når du navigerer til dem. (#1811)
* Understøttelse af HumanWare Brailliant BI og B-serie displays. (#1990)
* Nye sprog: Norsk Bokmål, Traditionel kinesisk (Hong Kong).

### Ændringer

* Kommandoer til at beskrive det aktuelle tegn eller stave det aktuelle ord eller linje vil nu stave på det relevante sprog afhængigt af teksten, hvis automatisk sprogskift er aktiveret, og de relevante sprogoplysninger er tilgængelige.
* Opdateret eSpeak talesyntese til version 1.46.02.
* NVDA afkorter nu ekstremt lange (30 tegn eller mere) navne gættet fra grafik- og link-URL'er, da de sandsynligvis er ubrugeligt indhold, der forhindrer læsning. (#1989)
* Nogle oplysninger vist i punkt er blevet forkortet. (#1955, #2043)
* Når cursoren eller gennemgangscursoren bevæger sig, rulles punkt nu på samme måde, som når det rulles manuelt. Dette gør det mere passende, når punkt er konfigureret til at læse pr. afsnit og/eller undgå opdeling af ord. (#1996)
* Opdateret til ny spansk grad 1 punkttabel.
* Opdateret liblouis-punktskriftoversætter til version 2.4.1.

### Fejlrettelser

* I Windows 8 flyttes fokus ikke længere fejlagtigt væk fra søgefeltet i Windows Stifinder, som tidligere forhindrede NVDA i at interagere med det.
* Store forbedringer i ydeevnen ved læsning og navigation i Microsoft Word-dokumenter, når automatisk rapportering af formatering er aktiveret, hvilket nu gør det ret behageligt at korrekturlæse formatering osv. Ydeevnen kan også være forbedret generelt for nogle brugere.
* Gennemsynstilstand bruges nu til fuldskærms Adobe Flash-indhold.
* Løst dårlig lydkvalitet i nogle tilfælde ved brug af Microsoft Speech API version 5-stemmer, når lydenheden ikke var indstillet til standard (Microsoft Sound Mapper). (#749)
* NVDA kan igen bruges med "ingen tale"-syntese, udelukkende ved hjælp af punkt eller talebrowseren. (#1963)
* Objektnavigationskommandoer rapporterer ikke længere "Ingen børn" og "Ingen forældre", men rapporterer i stedet meddelelser, der er i overensstemmelse med dokumentationen.
* Når NVDA er konfigureret til at bruge et andet sprog end engelsk, rapporteres navnet på tabulatortasten nu på det korrekte sprog.
* I Mozilla Gecko (f.eks. Firefox) skifter NVDA ikke længere periodisk til gennemsynstilstand under navigering i menuer i dokumenter. (#2025)
* I Lommeregner rapporterer backspace-tasten nu den opdaterede værdi i stedet for ingenting. (#2030)
* I gennemsynstilstand flyttes musen nu til det aktuelle navigatorobjekt til midten af objektet ved gennemgangscursoren i stedet for til øverste venstre hjørne, hvilket gør det mere præcist i nogle tilfælde. (#2029)
* I gennemsynstilstand med automatisk fokustilstand for fokusændringer aktiveret, vil fokusering på et værktøjslinjeelement nu skifte til fokustilstand. (#1339)
* Kommandoen til at rapportere titlen fungerer igen korrekt i Adobe Reader.
* Med automatisk fokustilstand for fokusændringer aktiveret, bruges fokustilstand nu korrekt for fokuserede tabelceller, f.eks. i ARIA-gitre. (#1763)
* I iTunes rapporteres positionsoplysninger i visse lister nu korrekt.
* I Adobe Reader behandles nogle links ikke længere som om de indeholder skrivebeskyttede redigerbare tekstfelter.
* Etiketterne på nogle redigerbare tekstfelter medtages ikke længere fejlagtigt ved rapportering af teksten i en dialogboks. (#1960)
* Beskrivelsen af grupper rapporteres igen, hvis rapportering af objektbeskrivelser er aktiveret.
* Den menneskelige læsbare størrelse inkluderes nu i teksten i dialogboksen for Windows Stifinders drevegenskaber.
* Dobbelt rapportering af egenskabssidetekst er blevet undertrykt i nogle tilfælde. (#218)
* Forbedret sporing af cursoren i redigerbare tekstfelter, der afhænger af tekst, der er skrevet til skærmen. Dette forbedrer især redigering i Microsoft Excel-celleredigeringsprogrammet og Eudora-meddelelseseditoren. (#1658)
* I Firefox 11 fungerer kommandoen flyt til indeholdende virtuel buffer (NVDA+control+space) nu som den burde for at forlade indlejrede objekter såsom Flash-indhold.
* NVDA genstarter nu sig selv korrekt (f.eks. efter ændring af det konfigurerede sprog), når det er placeret i en mappe, der indeholder ikke-ASCII-tegn. (#2079)
* Punkt respekterer nu korrekt indstillingerne for rapportering af objektgenvejstaster, positionsoplysninger og beskrivelser.
* I Mozilla-applikationer er skift mellem gennemsyns- og fokustilstand ikke længere langsomt, når punkt er aktiveret. (#2095)
* Flytning af markøren til pladsen i slutningen af linjen/afsnittet ved hjælp af markørknapperne i nogle redigerbare tekstfelter fungerer nu korrekt i stedet for at blive routet til starten af teksten. (#2096)
* NVDA fungerer igen korrekt med Audiologic Tts3-syntesen. (#2109)
* Microsoft Word-dokumenter behandles korrekt som flerrækkede. Dette får punkt til at opføre sig mere passende, når et dokument er fokuseret.
* I Microsoft Internet Explorer opstår der ikke længere fejl ved fokusering på visse sjældne kontroller. (#2121)
* Ændring af udtalen af tegnsætning/symboler af brugeren træder nu i kraft med det samme, i stedet for at kræve, at NVDA genstartes eller at automatisk sprogskift deaktiveres.
* Ved brug af eSpeak går tale ikke længere tavs i nogle tilfælde i dialogboksen Gem som i NVDA Log Viewer. (#2145)

### Ændringer for udviklere

* Der er nu en fjern Python-konsol til situationer, hvor fjernfejlfinding er nyttig. Se udviklerguiden for detaljer.
* Basisstien for NVDA's kode fjernes nu fra tracebacks i loggen for at forbedre læsbarheden. (#1880)
* TextInfo-objekter har nu en activate()-metode til at aktivere den position, der er repræsenteret af TextInfo.
 * Dette bruges af punktdisplays til at aktivere positionen ved hjælp af markørknapperne på et punktdisplay. Der kan dog være andre kaldere i fremtiden.
* TreeInterceptors og NVDAObjects, der kun eksponerer én side tekst ad gangen, kan understøtte automatiske sidevendinger under læs alt ved hjælp af textInfos.DocumentWithPageTurns-mix-in. (#1978)
* Flere kontrol- og outputkonstanter er blevet omdøbt eller flyttet. (#228)
 * speech.REASON_*-konstanter er flyttet til controlTypes.
 * I controlTypes er speechRoleLabels og speechStateLabels blevet omdøbt til blot roleLabels og stateLabels, henholdsvis.
* Punktoutput logges nu på niveauet input/output. Først logges den uoversatte tekst i alle regioner, efterfulgt af punkterne i vinduet, der vises. (#2102)
* Subklasser af sapi5-synthDriver kan nu tilsidesætte _getVoiceTokens og extend init for at understøtte brugerdefinerede stemmetokens såsom med sapi.spObjectTokenCategory for at hente tokens fra en brugerdefineret registreringsplacering.

## 2011.3

Højdepunkter i denne udgivelse inkluderer automatisk skift af talesprog ved læsning af dokumenter med passende sprogoplysninger; understøttelse af 64-bit Java Runtime Environment; rapportering af tekstformatering i gennemsynstilstand i Mozilla-applikationer; bedre håndtering af applikationsnedbrud og frysninger; samt indledende rettelser til Windows 8.

### Nye funktioner

* NVDA kan nu ændre eSpeak syntese-sproget automatisk, når der læses visse web-/pdf-dokumenter med passende sprogoplysninger. Automatisk skift af sprog/dialekt kan slås til og fra i dialogboksen Stemmeindstillinger. (#845)
* Java Access Bridge 2.0.2 understøttes nu, hvilket inkluderer understøttelse af 64-bit Java Runtime Environment.
* I Mozilla Gecko (f.eks. Firefox) annonceres overskriftsniveauer nu ved brug af objekt-navigation.
* Tekstformatering kan nu rapporteres ved brug af gennemsynstilstand i Mozilla Gecko (f.eks. Firefox og Thunderbird). (#394)
* Tekst med understregning og/eller gennemstregning kan nu opdages og rapporteres i standard IAccessible2 tekstkontroller såsom i Mozilla-applikationer.
* I gennemsynstilstand i Adobe Reader rapporteres nu række- og kolonneantal i tabeller.
* Understøttelse af Microsoft Speech Platform talesyntese er tilføjet. (#1735)
* Side- og linjenumre rapporteres nu for markøren i IBM Lotus Symphony. (#1632)
* Procenten for hvor meget tonehøjden ændres ved udtale af store bogstaver kan nu konfigureres i dialogen for stemmeindstillinger. Dette erstatter dog den ældre "hævet tonehøjde for store bogstaver"-indstilling (for at slå denne funktion fra, skal procenten sættes til 0). (#255)
* Tekst- og baggrundsfarve indgår nu i rapporteringen af formatering af celler i Microsoft Excel. (#1655)
* I applikationer, der bruger Java Access Bridge, virker "aktiver nuværende navigator-objekt"-kommandoen nu på kontroller, hvor det er relevant. (#1744)
* Nyttilføjet sprog: Tamil.
* Grundlæggende understøttelse af Design Science MathPlayer.

### Ændringer

* NVDA vil nu genstarte sig selv, hvis det går ned.
* Noget information vist på punktdisplay er blevet forkortet. (#1288)
* "Læs aktivt vindue"-kommandoen (NVDA+b) er blevet forbedret til at filtrere ubrugelige kontroller fra og er nu også lettere at afbryde. (#1499)
* Automatisk "sig alt", når et gennemsynstilstand-dokument indlæses, er nu valgfrit via en indstilling i gennemsynstilstandsindstillingerne. (#414)
* Når du forsøger at læse statuslinjen (Desktop NVDA+end), vil NVDA, hvis en ægte statuslinje ikke kan findes, i stedet bruge den nederste linje af tekst, der er skrevet på skærmen for den aktive applikation. (#649)
* Når du læser med "sig alt" i gennemsynstilstandsdokumenter, vil NVDA nu tage en pause ved slutningen af overskrifter og andre blokniveauelementer, i stedet for at læse teksten sammen med den næste tekst som én lang sætning.
* I gennemsynstilstand aktiverer tryk på enter eller mellemrum på en fane den nu, i stedet for at skifte til fokustilstand. (#1760)
* Opdateret eSpeak talesyntese til version 1.45.47.

### Fejlrettelser

* NVDA viser ikke længere punkttegn eller nummerering for lister i Internet Explorer og andre MSHTML-kontroller, når forfatteren har angivet, at disse ikke skal vises (f.eks. hvis listeformatet er "none"). (#1671)
* Genstart af NVDA, når det er frosset (f.eks. ved at trykke på control+alt+n), lukker ikke længere den tidligere kopi uden at starte en ny.
* Tryk på backspace eller piletaster i en Windows-kommandokonsol giver ikke længere mærkelige resultater i nogle tilfælde. (#1612)
* Det valgte element i WPF-combo boxe (og muligvis nogle andre combo boxe eksponeret ved brug af UI Automation), der ikke tillader tekstredigering, rapporteres nu korrekt.
* I gennemsynstilstand i Adobe Reader er det nu altid muligt at flytte til næste række fra header-rækken og omvendt ved brug af kommandoerne til at flytte til næste og forrige række. Header-rækken rapporteres heller ikke længere som række 0. (#1731)
* I gennemsynstilstand i Adobe Reader er det nu muligt at flytte til (og dermed forbi) tomme celler i en tabel.
* Ubrugelig positionsinformation (f.eks. 0 af 0 niveau 0) rapporteres ikke længere på punktdisplay.
* Når punktdisplay er bundet til gennemgang, er det nu i stand til at vise indhold i flad gennemgang. (#1711)
* En tekstkontrols tekst præsenteres ikke længere dobbelt på et punktdisplay i nogle tilfælde, f.eks. når der rulles tilbage fra starten af Wordpad-dokumenter.
* I gennemsynstilstand i Internet Explorer, fremkalder tryk på enter på en filupload-knap nu korrekt dialogboksen til at vælge en fil, der skal uploades, i stedet for at skifte til fokustilstand. (#1720)
* Dynamiske indholdsændringer, såsom i DOS-konsoller, annonceres ikke længere, hvis dvaletilstand for den applikation er aktiveret. (#1662)
* I gennemsynstilstand er adfærden for alt+opPil og alt+nedPil til at folde og udvide combo boxe forbedret. (#1630)
* NVDA genopretter sig nu fra mange flere situationer, såsom applikationer, der ikke reagerer, hvilket tidligere fik det til at fryse helt. (#1408)
* For Mozilla Gecko (Firefox osv.) gennemsynstilstandsdokumenter vil NVDA ikke længere fejle i at gengive tekst i en meget specifik situation, hvor et element er stylet som display:table. (#1373)
* NVDA vil ikke længere annoncere label-kontroller, når fokus flyttes inden i dem. Stopper dobbeltannoncering af labels for nogle formularfelter i Firefox (Gecko) og Internet Explorer (MSHTML). (#1650)
* NVDA fejler ikke længere i at læse en celle i Microsoft Excel efter indsættelse med control+v. (#1781)
* I Adobe Reader annonceres overflødig information om dokumentet ikke længere, når man flytter til en kontrol på en anden side i fokustilstand. (#1659)
* I gennemsynstilstand i Mozilla Gecko-applikationer (f.eks. Firefox) opdages og rapporteres skifteknapper nu korrekt. (#1757)
* NVDA kan nu korrekt læse Windows Stifinder-adresselinjen i Windows 8 developer preview.
* NVDA vil ikke længere få apps som winver og wordpad i Windows 8 developer preview til at gå ned på grund af forkerte glyph-oversættelser.
* I gennemsynstilstand i applikationer, der bruger Mozilla Gecko 10 og senere (f.eks. Firefox 10), er markøren oftere korrekt placeret, når en side indlæses med et målanger. (#360)
* I gennemsynstilstand i Mozilla Gecko-applikationer (f.eks. Firefox) gengives labels for imagemaps nu.
* Når musesporing er aktiveret, vil det ikke længere få applikationen til at gå ned at flytte musen over visse redigerbare tekstfelter (såsom i Synaptics Pointing Device Settings og SpeechLab SpeakText). (#672)
* NVDA fungerer nu korrekt i flere "om"-dialogbokse i applikationer, der distribueres med Windows XP, inklusive "Om"-dialogen i Notesblok og "Om Windows"-dialogen. (#1853, #1855)
* Fikset læsning efter ord i Windows Edit-kontroller. (#1877)
* Når man forlader et redigerbart tekstfelt med venstrePil, opPil eller pageUp, mens man er i fokustilstand, skifter NVDA nu korrekt til gennemsynstilstand, når automatisk fokustilstand for markørbevægelser er aktiveret. (#1733)

### Ændringer for udviklere

* NVDA kan nu instruere talesynteser til at skifte sprog for bestemte dele af tale.
 * For at understøtte dette skal drivere håndtere speech.LangChangeCommand i sekvenser sendt til SynthDriver.speak().
 * SynthDriver-objekter bør også levere sprogargumentet til VoiceInfo-objekter (eller tilsidesætte sprog-attributten for at hente det aktuelle sprog). Ellers vil NVDA's brugergrænsefladesprog blive brugt.

## 2011.2

Højdepunkter i denne version inkluderer store forbedringer med hensyn til tegnsætning og symboler, inklusive konfigurerbare niveauer, brugerdefineret mærkning og tegnbeskrivelser; ingen pauser ved slutningen af linjer under "sig alt"; forbedret støtte til ARIA i Internet Explorer; bedre støtte til XFA/LiveCycle PDF-dokumenter i Adobe Reader; adgang til tekst, der skrives til skærmen i flere applikationer; og adgang til formaterings- og farveoplysninger for tekst, der skrives til skærmen.

### Nye funktioner

* Det er nu muligt at høre beskrivelsen af et givet tegn ved at trykke på kommandoen for gennemgang af det aktuelle tegn to gange hurtigt efter hinanden. For engelske tegn er dette det standard engelske fonetiske alfabet. For piktografiske sprog såsom traditionel kinesisk gives der et eller flere eksempler med sætninger, der bruger det pågældende symbol. At trykke tre gange på kommandoen for gennemgang af det aktuelle ord eller linje vil stave ordet/linjen ved brug af den første af disse beskrivelser. (#55)
* Mere tekst kan ses i flad gennemgang for applikationer som Mozilla Thunderbird, der skriver deres tekst direkte til skærmen som glyphs.
* Det er nu muligt at vælge mellem flere niveauer af tegnsætning og symboludtalelse. (#332)
* Når tegnsætning eller andre symboler gentages mere end fire gange, bliver antallet af gentagelser nu annonceret i stedet for at gentage symbolerne. (#43)
* Nye punkttabeller: Norsk 8-punkt computer braille, Etiopisk grad 1, Slovensk grad 1, Serbisk grad 1. (#1456)
* Tale holder ikke længere unaturlige pauser ved slutningen af hver linje, når man bruger "sig alt"-kommandoen. (#149)
* NVDA vil nu annoncere, om noget er sorteret (ifølge aria-sort egenskaben) i webbrowsere. (#1500)
* Unicode Braille-mønstre vises nu korrekt på punktdisplays. (#1505)
* I Internet Explorer og andre MSHTML-kontroller, når fokus flytter sig inden for en gruppe af kontroller (omgivet af et fieldset), vil NVDA nu annoncere navnet på gruppen (legenden). (#535)
* I Internet Explorer og andre MSHTML-kontroller respekteres nu aria-labelledBy og aria-describedBy egenskaberne.
* I Internet Explorer og andre MSHTML-kontroller er støtte til ARIA-liste, gridcelle, slider og progressbar kontroller blevet forbedret.
* Brugere kan nu ændre udtalen af tegnsætning og andre symboler samt niveauet for, hvornår de bliver talt. (#271, #1516)
* I Microsoft Excel annonceres navnet på det aktive ark nu, når der skiftes ark med control+pageUp eller control+pageDown. (#760)
* Når man navigerer i en tabel i Microsoft Word med tabulatortasten, vil NVDA nu annoncere den aktuelle celle, når du flytter dig. (#159)
* Du kan nu konfigurere, om tabelcellekoordinater skal annonceres fra dialogboksen for dokumentformatering. (#719)
* NVDA kan nu opdage formatering og farver for tekst, der skrives til skærmen.
* I meddelelseslisten i Outlook Express/Windows Mail/Windows Live Mail annoncerer NVDA nu, om en meddelelse er ulæst, samt om den er udvidet eller kollapset i samtaletråde. (#868)
* eSpeak har nu en "rate boost"-indstilling, der tredobler taletempoet.
* Støtte til kalenderkontrollen, der findes i dialogboksen for Dato og tid fra Windows 7-uret. (#1637)
* Yderligere tastaturbindinger er blevet tilføjet til MDV Lilli punktdisplayet. (#241)
* Nye sprog: Bulgarsk, Albansk.

### Ændringer

* For at flytte markøren til gennemgangsmarkøren, tryk nu på kommandoen for at flytte fokus til navigatorobjektet (desktop NVDA+shift+numpadMinus, laptop NVDA+shift+backspace) to gange hurtigt efter hinanden. Dette frigør flere taster på tastaturet. (#837)
* For at høre den decimale og hexadecimale repræsentation af tegnet under gennemgangsmarkøren, tryk nu tre gange på kommandoen for gennemgang af det aktuelle tegn i stedet for to gange, da to gange nu taler tegnbeskrivelsen.
* Opdateret eSpeak talesyntese til version 1.45.03. (#1465)
* Layouttabeller annonceres ikke længere i Mozilla Gecko-applikationer, når man flytter fokus i fokus-tilstand eller uden for et dokument.
* I Internet Explorer og andre MSHTML-kontroller fungerer gennemsynstilstand nu for dokumenter inde i ARIA-applikationer. (#1452)
* Opdateret liblouis brailleoversætter til version 2.3.0.
* Når man er i gennemsynstilstand og hopper til en kontrol med quicknav eller fokus, bliver beskrivelsen af kontrollen nu annonceret, hvis den har en.
* Fremdriftslinjer annonceres nu i gennemsynstilstand.
* Noder markeret med en ARIA-rolle som præsentation i Internet Explorer og andre MSHTML-kontroller bliver nu filtreret fra i simpel gennemgang og fokus-stamtræet.
* NVDA's brugergrænseflade og dokumentation henviser nu til virtuelle buffere som gennemsynstilstand, da termen "virtuelle buffere" er ret meningsløs for de fleste brugere. (#1509)
* Når brugeren ønsker at kopiere sine brugerindstillinger til systemprofilen til brug ved loginskærmen mv., og deres indstillinger indeholder brugerdefinerede plugins, advares de nu om, at dette kan udgøre en sikkerhedsrisiko. (#1426)
* NVDA-tjenesten starter og stopper ikke længere NVDA på brugerinput-skriveborde.
* På Windows XP og Windows Vista benytter NVDA ikke længere UI Automation, selvom det er tilgængeligt via platformopdateringen. Selvom brugen af UI Automation kan forbedre tilgængeligheden af nogle moderne applikationer, var der for mange nedbrud, frysninger og overordnet ydelsestab ved brug af det på XP og Vista. (#1437)
* I applikationer, der bruger Mozilla Gecko 2 og senere (såsom Firefox 4 og senere), kan et dokument nu læses i gennemsynstilstand, før det er fuldstændigt indlæst.
* NVDA annoncerer nu tilstanden af en container, når fokus flyttes til en kontrol inde i den (f.eks. hvis fokus flyttes inde i et dokument, der stadig indlæses, vil det blive rapporteret som travlt).
* NVDA's brugergrænseflade og dokumentation bruger ikke længere termerne "første barn" og "forælder" med hensyn til objekt-navigation, da disse termer er forvirrende for mange brugere.
* "Kollapset" annonceres ikke længere for nogle menupunkter, der har undermenuer.
* Kommandoen "Rapporter aktuel formatering" (NVDA+f) rapporterer nu formateringen ved gennemgangsmarkøren i stedet for systemmarkøren/fokus. Da gennemgangsmarkøren som standard følger markøren, vil de fleste ikke bemærke nogen forskel. Dette giver dog nu brugeren mulighed for at finde ud af formateringen, når man flytter gennemgangsmarkøren, f.eks. i flad gennemgang.

### Fejlrettelser

* Kollapsende kombobokse i gennemsynstilstandsdokumenter, når fokus-tilstand er blevet tvunget med NVDA+mellemrum, skifter ikke længere automatisk tilbage til gennemsynstilstand. (#1386)
* I Gecko (f.eks. Firefox) og MSHTML (f.eks. Internet Explorer) dokumenter gengiver NVDA nu korrekt visse tekster på samme linje, der tidligere blev gengivet på separate linjer. (#1378)
* Når punktskrift er forbundet med gennemgang, og navigatorobjektet flyttes til et gennemsynstilstandsdokument, enten manuelt eller på grund af en fokusændring, vil punktskrift passende vise gennemsynstilstandsindholdet. (#1406, #1407)
* Når tale af tegnsætning er deaktiveret, bliver visse tegnsætninger ikke længere fejlagtigt talt, når man bruger nogle talesynteser. (#332)
* Der opstår ikke længere problemer ved indlæsning af konfiguration for talesynteser, der ikke understøtter stemmeindstillingen, såsom Audiologic Tts3. (#1347)
* Skype Ekstras-menuen bliver nu læst korrekt. (#648)
* Markering af check boxen for Lysstyrke kontrollerer lydstyrke i dialogboksen Musens indstillinger bør ikke længere forårsage store forsinkelser for beep-lyde, når musen flyttes rundt på skærmen på Windows Vista/Windows 7 med Aero aktiveret. (#1183)
* Når NVDA er konfigureret til at bruge laptop-tastaturlayout, fungerer NVDA+slet nu som dokumenteret til at rapportere dimensionerne af det aktuelle navigatorobjekt. (#1498)
* NVDA respekterer nu korrekt aria-selected attributten i Internet Explorer dokumenter.
* Når NVDA automatisk skifter til fokus-tilstand i gennemsynstilstandsdokumenter, annoncerer den nu oplysninger om konteksten for fokus. For eksempel, hvis et listeboks-element modtager fokus, vil listeboksen blive annonceret først. (#1491)
* I Internet Explorer og andre MSHTML-kontroller behandles ARIA listeboks-kontroller nu som lister i stedet for listeelementer.
* Når en skrivebeskyttet redigerbar tekstkontrol modtager fokus, rapporterer NVDA nu, at den er skrivebeskyttet. (#1436)
* I gennemsynstilstand opfører NVDA sig nu korrekt med hensyn til skrivebeskyttede redigerbare tekstfelter.
* I gennemsynstilstandsdokumenter skifter NVDA ikke længere fejlagtigt ud af fokus-tilstand, når aria-activedescendant er indstillet; f.eks. når fuldførelseslisten dukkede op i nogle autoudfyldningskontroller.
* I Adobe Reader rapporteres navnet på kontroller, når fokus flyttes eller når der bruges hurtig navigation i gennemsynstilstand.
* I XFA PDF-dokumenter i Adobe Reader gengives knapper, links og grafik nu korrekt.
* I XFA PDF-dokumenter i Adobe Reader er alle elementer nu gengivet på separate linjer. Denne ændring blev foretaget, fordi store sektioner (nogle gange hele dokumentet) blev gengivet uden mellemrum på grund af den generelle mangel på struktur i disse dokumenter.
* Rettede problemer, når der flyttes fokus til eller væk fra redigerbare tekstfelter i XFA PDF-dokumenter i Adobe Reader.
* I XFA PDF-dokumenter i Adobe Reader rapporteres ændringer i værdien af en fokuseret komboboks nu.
* Ejermalede kombobokse såsom dem, der bruges til at vælge farver i Outlook Express, er nu tilgængelige med NVDA. (#1340)
* I sprog, der bruger et mellemrum som en tusindskilletegn, såsom fransk og tysk, udtales tal fra separate tekststykker ikke længere som et enkelt tal. Dette var især problematisk for tabelceller, der indeholdt tal. (#555)
* Noder med en ARIA-rolle som beskrivelse i Internet Explorer og andre MSHTML-kontroller bliver nu klassificeret som statisk tekst og ikke som redigeringsfelter.
* Rettede forskellige problemer, når man trykkede på tabulatortasten, mens fokus var på et dokument i gennemsynstilstand (f.eks. flyttede tab-tasten fejlagtigt til adresselinjen i Internet Explorer). (#720, #1367)
* Når man går ind i lister, mens man læser tekst, siger NVDA nu f.eks. "liste med 5 elementer" i stedet for "listemed 5 elementer". (#1515)
* I input-hjælpetilstand logges kommandoer, selvom deres scripts omgår input-hjælpen, såsom kommandoerne for at rulle punktdisplayet frem og tilbage.
* I input-hjælpetilstand, når en tastaturmodifikator holdes nede, rapporterer NVDA ikke længere modifikatoren, som om den modificerer sig selv; f.eks. NVDA+NVDA.
* I Adobe Reader-dokumenter fungerer tryk på c eller shift+c for at navigere til en komboboks nu korrekt.
* Den valgte tilstand af valgbare tabelrækker rapporteres nu på samme måde som liste- og trævisningselementer.
* Kontroller i Firefox og andre Gecko-applikationer kan nu aktiveres i gennemsynstilstand, selvom deres indhold er blevet flyttet ud af skærmen. (#801)
* Det er ikke længere muligt at vise en NVDA-indstillingsdialog, mens en meddelelsesdialog vises, da indstillingsdialogen var frosset i dette tilfælde. (#1451)
* I Microsoft Excel er der ikke længere forsinkelser, når man holder nede eller hurtigt trykker på taster for at flytte mellem eller vælge celler.
* Rettede intermitterende nedbrud af NVDA-tjenesten, hvilket betød, at NVDA stoppede med at køre på sikre Windows-skærme.
* Rettede problemer, der undertiden opstod med punktdisplays, når en ændring fik teksten, der blev vist, til at forsvinde. (#1377)
* Downloadvinduet i Internet Explorer 9 kan nu navigeres og læses med NVDA. (#1280)
* Det er ikke længere muligt ved et uheld at starte flere kopier af NVDA på samme tid. (#507)
* På langsomme systemer forhindrer NVDA nu uhensigtsmæssigt, at hovedvinduet vises hele tiden, mens det kører. (#726)
* NVDA går ikke længere ned på Windows XP, når en WPF-applikation startes. (#1437)
* "Sig alt" og "sig alt med gennemgang" fungerer nu i UI Automation-tekstkontroller, der understøtter al nødvendig funktionalitet. For eksempel kan du nu bruge "sig alt med gennemgang" på XPS Viewer-dokumenter.
* NVDA klassificerer ikke længere visse listeelementer i Outlook Express/Windows Live Mail-meddelelsesregler Anvend nu-dialogen som værende check boxer. (#576)
* Kombobokse rapporteres ikke længere som havende en undermenu.
* NVDA er nu i stand til at læse modtagerne i felterne Til, CC og BCC i Microsoft Outlook. (#421)
* Rettede problemet i NVDA's taleindstillinger, hvor værdien af skydeknapperne undertiden ikke blev rapporteret, når den blev ændret. (#1411)
* NVDA annoncerer ikke længere den nye celle, når man bevæger sig i et Excel-regneark efter at have klippet og indsat. (#1567)
* NVDA bliver ikke længere dårligere til at gætte farvenavne, jo flere farver det annoncerer.
* I Internet Explorer og andre MSHTML-kontroller rettede vi problemet med at læse sjældne sider med iframes markeret med en ARIA-rolle som præsentation. (#1569)
* I Internet Explorer og andre MSHTML-kontroller rettede vi et sjældent problem, hvor fokus blev ved med at hoppe uendeligt mellem dokumentet og et flerlinjet redigeringsfelt i fokus-tilstand. (#1566)
* I Microsoft Word 2010 læser NVDA nu automatisk bekræftelsesdialoger. (#1538)
* I flerlinjede redigerbare tekstfelter i Internet Explorer og andre MSHTML-kontroller rapporteres markeringen på linjer efter den første korrekt. (#1590)
* Forbedrede bevægelsen efter ord i mange tilfælde, inklusive gennemsynstilstand og Windows redigeringskontroller. (#1580)
* NVDA-installationsprogrammet viser ikke længere fejlbehæftede tekster for Hongkong-versioner af Windows Vista og Windows 7. (#1596)
* NVDA fejler ikke længere ved indlæsning af Microsoft Speech API version 5 talesyntese, hvis konfigurationen indeholder indstillinger for den talesyntese, men mangler stemmeindstillingen. (#1599)
* I redigerbare tekstfelter i Internet Explorer og andre MSHTML-kontroller fryser eller hænger NVDA ikke længere, når punkt er aktiveret.
* I Firefox gennemsynstilstand nægter NVDA ikke længere at inkludere indhold, der er inden i en fokuserbar node med en ARIA-rolle som præsentation.
* I Microsoft Word med punkt aktiveret rapporteres linjer på sider efter den første side nu korrekt. (#1603)
* I Microsoft Word 2003 kan linjer med højre-til-venstre-tekst igen læses, når punkt er aktiveret. (#627)
* I Microsoft Word fungerer "sig alt" nu korrekt, når dokumentet ikke slutter med en sætning.
* Når man åbner en almindelig tekstmeddelelse i Windows Live Mail 2011, vil NVDA korrekt fokusere på meddelelsesdokumentet, så det kan læses.
* NVDA fryser ikke længere midlertidigt eller nægter at tale i dialogerne Flyt til/Kopier til i Windows Live Mail. (#574)
* I Outlook 2010 vil NVDA nu korrekt følge fokus i meddelelseslisten. (#1285)
* Nogle USB-forbindelsesproblemer er blevet løst med MDV Lilli punktdisplayet. (#241)
* I Internet Explorer og andre MSHTML-kontroller ignoreres mellemrum ikke længere i gennemsynstilstand i visse tilfælde (f.eks. efter et link).
* I Internet Explorer og andre MSHTML-kontroller er nogle overflødige linjeskift blevet elimineret i gennemsynstilstand. Specifikt tvinger HTML-elementer med en display-stil af None ikke længere et linjeskift. (#1685)
* Hvis NVDA ikke kan starte, vil undladelse af at afspille Windows-kritisk stop-lyd ikke længere forhindre den kritiske fejlmeddelelse i logfilen.

### Ændringer for udviklere

* Udviklerdokumentation kan nu genereres ved brug af SCons. Se readme.txt i roden af kildefordelingen for detaljer, herunder tilknyttede afhængigheder.
* Lokaliser kan nu levere beskrivelser for tegn. Se sektionen Tegnbeskrivelser i Udviklerguiden for detaljer. (#55)
* Lokaliser kan nu levere oplysninger om udtale af specifik tegnsætning og andre symboler. Se sektionen Symboludtale i Udviklerguiden for detaljer. (#332)
* Du kan nu bygge NVDAHelper med flere fejlretningsmuligheder ved at bruge nvdaHelperDebugFlags SCons-variablen. Se readme.txt i roden af kildefordelingen for detaljer. (#1390)
* Synth-drivere får nu overført en sekvens af tekst og tale-kommandoer til at tale, i stedet for kun tekst og en indeks.
 * Dette muliggør indlejrede indekser, parameterændringer mv.
 * Drivere bør implementere SynthDriver.speak() i stedet for SynthDriver.speakText() og SynthDriver.speakCharacter().
 * De gamle metoder vil blive brugt, hvis SynthDriver.speak() ikke er implementeret, men de er forældede og vil blive fjernet i en fremtidig version.
* gui.execute() er blevet fjernet. wx.CallAfter() bør bruges i stedet.
* gui.scriptUI er blevet fjernet.
 * For meddelelsesdialoger, brug wx.CallAfter(gui.messageBox, ...).
 * For alle andre dialoger bør rigtige wx-dialoger bruges i stedet.
 * En ny gui.runScriptModalDialog() funktion forenkler brugen af modale dialoger fra scripts.
* Synth-drivere kan nu understøtte boolske indstillinger. Se SynthDriverHandler.BooleanSynthSetting.
* SCons accepterer nu en certTimestampServer-variabel, der specificerer URL'en på en tidsstemplingsserver, som skal bruges til at tidsstemple autenticode-signaturer. (#1644)

## 2011.1.1

Denne udgivelse løser flere sikkerheds- og andre vigtige problemer, der er fundet i NVDA 2011.1.

### Fejlrettelser

* Punktet Doner i NVDA-menuen er nu deaktiveret, når man kører på logon-, låse-, UAC- og andre sikre Windows-skærme, da dette udgør en sikkerhedsrisiko. (#1419)
* Det er nu umuligt at kopiere eller indsætte inden for NVDA's brugergrænseflade, mens man er på sikre skriveborde (låseskærm, UAC-skærm og Windows-logon), da dette udgør en sikkerhedsrisiko. (#1421)
* I Firefox 4 fungerer kommandoen flyt til den indeholdende virtuelle buffer (NVDA+control+space) nu som den burde for at undslippe indlejrede objekter såsom Flash-indhold. (#1429)
* Når tale af kommando-taster er aktiveret, bliver skiftede tegn ikke længere fejlagtigt talt som kommando-taster. (#1422)
* Når tale af kommando-taster er aktiveret, bliver tryk på mellemrum med andre modifikatorer end skift (såsom control og alt) nu rapporteret som en kommando-tast. (#1424)
* Logføring er nu helt deaktiveret, når man kører på logon-, låse-, UAC- og andre sikre Windows-skærme, da dette udgør en sikkerhedsrisiko. (#1435)
* I input-hjælpetilstand logges kommandoer, selvom de ikke er bundet til et script (i overensstemmelse med brugerguiden). (#1425)

## 2011.1

Højdepunkter i denne version inkluderer automatisk rapportering af ny tekstudgang i mIRC, PuTTY, Tera Term og SecureCRT; støtte til globale plugins; annoncering af punkttegn og nummerering i Microsoft Word; yderligere tastaturbindinger til punktdisplays, inklusive taster til at flytte til næste og forrige linje; støtte til flere Baum, HumanWare og APH punktdisplays; og rapportering af farver for nogle kontroller, inklusive IBM Lotus Symphony tekstkontroller.

### Nye funktioner

* Farver kan nu rapporteres for nogle kontroller. Automatisk annoncering kan konfigureres i dialogboksen for dokumentformatering. Det kan også rapporteres efter behov ved hjælp af kommandoen "rapporter tekstformatering" (NVDA+f).
 * Indledningsvist understøttes dette i standard IAccessible2-redigerbare tekstkontroller (såsom i Mozilla-applikationer), RichEdit-kontroller (såsom i Wordpad) og IBM Lotus Symphony tekstkontroller.
* I virtuelle buffere kan du nu vælge pr. side (ved hjælp af shift+pageDown og shift+pageUp) og paragraf (ved hjælp af shift+control+downArrow og shift+control+upArrow). (#639)
* NVDA rapporterer nu automatisk ny tekstudgang i mIRC, PuTTY, Tera Term og SecureCRT. (#936)
* Brugere kan nu tilføje nye tastaturbindinger eller overskrive eksisterende for ethvert script i NVDA ved at tildele én kommando til det pågældende script. (#194)
* Støtte til globale plugins. Globale plugins kan tilføje ny funktionalitet til NVDA, der fungerer på tværs af alle applikationer. (#281)
* Et lille bip høres nu, når der skrives tegn med shift-tasten, mens capslock er aktiveret. Dette kan slås fra ved at fjerne markeringen af den relaterede nye indstilling i dialogboksen for tastaturindstillinger. (#663)
* Hårde sideskift annonceres nu, når man bevæger sig linje for linje i Microsoft Word. (#758)
* Punkttegn og nummerering tales nu i Microsoft Word, når man bevæger sig linje for linje. (#208)
* En kommando til at skifte dvaletilstand for den aktuelle applikation (NVDA+shift+s) er nu tilgængelig. Dvaletilstand (tidligere kendt som selvtalende tilstand) deaktiverer al skærmlæsningsfunktionalitet i NVDA for en bestemt applikation. Meget nyttigt for applikationer, der leverer deres egen tale- og/eller skærmlæsningsfunktionalitet. Tryk på denne kommando igen for at deaktivere dvaletilstand.
* Nogle yderligere punktdisplay-tastaturbindinger er blevet tilføjet. Se sektionen Støttede punktdisplays i brugerguiden for detaljer. (#209)
* Til bekvemmelighed for tredjepartsudviklere kan app-moduler samt globale plugins nu genindlæses uden at genstarte NVDA. Brug værktøjer -> Genindlæs plugins i NVDA-menuen eller NVDA+control+f3. (#544)
* NVDA husker nu den position, du var på, når du vender tilbage til en tidligere besøgt webside. Dette gælder, indtil enten browseren eller NVDA afsluttes. (#132)
* Handy Tech punktdisplays kan nu bruges uden at installere Handy Tech universal driver. (#854)
* Støtte til flere Baum, HumanWare og APH punktdisplays. (#937)
* Statuslinjen i Media Player Classic Home Cinema genkendes nu.
* Freedom Scientific Focus 40 Blue punktdisplayet kan nu bruges, når det er forbundet via bluetooth. (#1345)

### Ændringer

* Positionsinformation rapporteres ikke længere som standard i nogle tilfælde, hvor det normalt var ukorrekt; f.eks. de fleste menuer, køreprogramlinjen, meddelelsesområdet osv. Dette kan dog genaktiveres ved en tilføjet mulighed i dialogboksen for objektpræsentation.
* Tastaturhjælp er blevet omdøbt til input-hjælp for at afspejle, at det håndterer input fra andre kilder end tastaturet.
* Input-hjælp rapporterer ikke længere en scripts kodelokation via tale og punkt, da det er kryptisk og irrelevant for brugeren. Dog logges det nu for udviklere og avancerede brugere.
* Når NVDA opdager, at det er frosset, fortsætter det med at opsnappe NVDA-modifikatortaster, selvom det giver alle andre taster videre til systemet. Dette forhindrer brugeren i utilsigtet at skifte caps lock mv., hvis de trykker på en NVDA-modifikatortast uden at indse, at NVDA er frosset. (#939)
* Hvis taster holdes nede efter brug af kommandoen "giv næste tast videre", gives alle taster (inklusive tastagentagelser) nu videre, indtil den sidste tast er frigivet.
* Hvis en NVDA-modifikatortast trykkes to gange hurtigt efter hinanden for at give den videre, og det andet tryk holdes nede, vil alle tastagentagelser nu også blive givet videre.
* Volumen op, ned og lydløs-tasterne rapporteres nu i input-hjælp. Dette kan være nyttigt, hvis brugeren er usikker på, hvad disse taster er.
* Genvejstasten for "Gennemgangsmarkør" i NVDA's præferencemenu er blevet ændret fra r til c for at eliminere konflikten med punktindstillinger.

### Fejlrettelser

* Når der tilføjes en ny taleordbogspost, er titlen på dialogboksen nu "Tilføj ordbogspost" i stedet for "Rediger ordbogspost". (#924)
* I taleordbogens dialogbokse præsenteres indholdet af kolonnerne Regelmæssigt udtryk og Store/små bogstaver følsomme nu i det konfigurerede NVDA-sprog i stedet for altid på engelsk.
* I AIM annonceres positionsinformation nu i trævisninger.
* På skydeknapperne i dialogboksen Taleindstillinger øger op-pil/side op/home nu indstillingen, og ned-pil/side ned/end mindsker den. Tidligere skete det modsatte, hvilket ikke er logisk og ikke stemmer overens med talesyntese-indstillingsringen. (#221)
* I virtuelle buffere med skærmlayout deaktiveret vises nogle overflødige tomme linjer ikke længere.
* Hvis en NVDA-modifikatortast trykkes to gange hurtigt, men der er en mellemliggende tastetryk, gives NVDA-modifikatortasten ikke længere videre ved det andet tryk.
* Tegnsætningstaster tales nu i input-hjælp, selv når tale af tegnsætning er deaktiveret. (#977)
* I dialogboksen for tastaturindstillinger præsenteres tastaturlayoutnavnene nu i det konfigurerede NVDA-sprog i stedet for altid på engelsk. (#558)
* Rettede et problem, hvor nogle elementer blev gengivet som tomme i Adobe Reader-dokumenter; f.eks. linksene i indholdsfortegnelsen i Apple iPhone IOS 4.1 brugervejledningen.
* Knappen "Brug aktuelt gemte indstillinger på logon og andre sikre skærme" i NVDA's Generelle indstillinger fungerer nu, hvis den bruges umiddelbart efter, at NVDA er nyinstalleret, men før en sikker skærm har vist sig. Tidligere rapporterede NVDA, at kopiering var succesfuld, men det havde faktisk ingen effekt. (#1194)
* Det er ikke længere muligt at have to NVDA-indstillingsdialogbokse åbne samtidig. Dette løser problemer, hvor én åben dialog afhænger af en anden åben dialog; f.eks. ændring af talesyntese, mens dialogboksen for taleindstillinger er åben. (#603)
* På systemer med UAC aktiveret, fejler knappen "Brug aktuelt gemte indstillinger på logon og andre sikre skærme" i NVDA's Generelle indstillinger ikke længere efter UAC-prompten, hvis brugerens kontonavn indeholder et mellemrum. (#918)
* I Internet Explorer og andre MSHTML-kontroller bruger NVDA nu URL'en som sidste udvej til at bestemme navnet på et link i stedet for at præsentere tomme links. (#633)
* NVDA ignorerer ikke længere fokus i AOL Instant Messenger 7-menuer. (#655)
* Annoncerer nu den korrekte etiket for fejl i Microsoft Word stavekontrol-dialogboksen (f.eks. Ikke i ordbog, Grammatikfejl, tegnsætning). Tidligere blev de alle annonceret som grammatikfejl. (#883)
* Indtastning i Microsoft Word ved brug af punktdisplay bør ikke længere forårsage, at der indtastes forvansket tekst, og en sjælden frysefejl ved tryk på en punktmarkørtast i Word-dokumenter er blevet rettet. (#1212) En begrænsning er dog, at arabisk tekst ikke længere kan læses i Word 2003 og derunder, når der bruges et punktdisplay. (#627)
* Når der trykkes på slet-tasten i et redigeringsfelt, bør teksten/markøren på et punktdisplay nu altid blive opdateret passende for at afspejle ændringen. (#947)
* Ændringer på dynamiske sider i Gecko2-dokumenter (f.eks. Firefox 4), mens flere faner er åbne, afspejles nu korrekt af NVDA. Tidligere blev kun ændringer i den første fane afspejlet. (Mozilla fejl 610985)
* NVDA kan nu korrekt annoncere forslag til grammatik- og tegnsætningsfejl i Microsoft Words stavekontrol-dialogboks. (#704)
* I Internet Explorer og andre MSHTML-kontroller præsenterer NVDA ikke længere destinationsankre som tomme links i sin virtuelle buffer. I stedet skjules disse ankre, som de bør være. (#1326)
* Objekt-navigation omkring og inden for standard gruppedialogvinduer er ikke længere ødelagt og asymmetrisk.
* I Firefox og andre Gecko-baserede kontroller sidder NVDA ikke længere fast i en underframe, hvis den er færdig med at indlæse, før det ydre dokument er færdigt.
* NVDA annoncerer nu passende det næste tegn, når man sletter et tegn med numpadDelete. (#286)
* På Windows XP logonskærmen annonceres brugernavnet igen, når den valgte bruger ændres.
* Rettede problemer, når man læser tekst i Windows kommandokonsoller med rapportering af linjenumre aktiveret.
* Dialogboksen for elementlisten i virtuelle buffere er nu anvendelig af seende brugere. Alle kontroller er synlige på skærmen. (#1321)
* Listen over poster i taleordbogens dialogboks er nu mere læsbar for seende brugere. Listen er nu stor nok til at vise alle dens kolonner på skærmen. (#90)
* På ALVA BC640/BC680 punktdisplays ignorerer NVDA ikke længere display-taster, der stadig er holdt nede, efter en anden tast er frigivet.
* Adobe Reader X går ikke længere ned, efter man forlader de uopmærkede dokumentindstillinger, før behandlingsdialogen vises. (#1218)
* NVDA skifter nu til den passende punktdisplay-driver, når du vender tilbage til gemt konfiguration. (#1346)
* Visual Studio 2008 Project Wizard læses igen korrekt. (#974)
* NVDA holder ikke længere helt op med at fungere i applikationer, der indeholder ikke-ASCII-tegn i deres eksekverbare navn. (#1352)
* Når man læser linje for linje i AkelPad med linjeombrydning aktiveret, læser NVDA ikke længere det første tegn på den følgende linje ved slutningen af den aktuelle linje.
* I Visual Studio 2005/2008 kodeeditoren læser NVDA ikke længere hele teksten efter hver indtastede tast. (#975)
* Rettede problemet, hvor nogle punktdisplays ikke blev ryddet korrekt, når NVDA blev afsluttet, eller displayet blev ændret.
* Den indledende fokus tales ikke længere nogle gange to gange, når NVDA starter. (#1359)

### Ændringer for udviklere

* SCons bruges nu til at forberede kildekoden og skabe binære builds, bærbare arkiver, installationsprogrammer mv. Se readme.txt i roden af kildefordelingen for detaljer.
* Tasternavne brugt af NVDA (inklusive tastkort) er blevet gjort mere brugervenlige/logiske; f.eks. opPil i stedet for extendedUp og numpadPageUp i stedet for prior. Se vkCodes-modulet for en liste.
* Alt input fra brugeren repræsenteres nu af en inputCore.InputGesture-forekomst. (#601)
 * Hver input-kilde underklasser basen InputGesture-klassen.
 * Tastetryk på systemtastaturet er dækket af keyboardHandler.KeyboardInputGesture-klassen.
 * Tryk på knapper, hjul og andre kontroller på et punktdisplay er dækket af underklasserne af braille.BrailleDisplayGesture-klassen. Disse underklasser leveres af hver punktdisplay-driver.
* Input-kommandoer bindes til ScriptableObjects ved hjælp af ScriptableObject.bindGesture() metoden på en forekomst eller en __gestures dict på klassen, som kortlægger gesture-identifikatorer til script-navne. Se baseObject.ScriptableObject for detaljer.
* App-moduler har ikke længere tastkort-filer. Alle input-kommando-bindinger skal udføres i selve app-modulet.
* Alle scripts tager nu en InputGesture-forekomst i stedet for et tastetryk.
 * KeyboardInputGestures kan sendes videre til OS'et ved hjælp af send()-metoden på kommandoen.
* For at sende et vilkårligt tastetryk skal du nu oprette en KeyboardInputGesture ved hjælp af KeyboardInputGesture.fromName() og derefter bruge dens send()-metode.
* Lokaliser kan nu levere input gesture for at tilføje nye bindinger eller overskrive eksisterende bindinger for scripts hvor som helst i NVDA. (#810)
 * Locale-gesture-map bør placeres i locale\LANG\gestures.ini, hvor LANG er sprognavnet.
 * Se inputCore.GlobalGestureMap for detaljer om filformatet.
* De nye LiveText- og Terminal NVDAObject-adfærdsmønstre faciliterer automatisk rapportering af ny tekst. Se disse klasser i NVDAObjects.behaviors for detaljer. (#936)
 * NVDAObjects.window.DisplayModelLiveText overlay-klassen kan bruges til objekter, der skal hente tekst skrevet til skærmen.
 * Se mirc- og putty-app-modulerne for brugseksempler.
* Der findes ikke længere et _default-app-modul. App-moduler bør i stedet underklasser appModuleHandler.AppModule (basen AppModule-klassen).
* Støtte til globale plugins, der kan globalt binde scripts, håndtere NVDAObject-begivenheder og vælge NVDAObject-overlay-klasser. (#281) Se globalPluginHandler.GlobalPlugin for detaljer.
* På SynthDriver-objekter er attributterne available* for strengindstillinger (f.eks. availableVoices og availableVariants) nu OrderedDicts nøglede efter ID i stedet for lister.
* synthDriverHandler.VoiceInfo tager nu et valgfrit language-argument, der specificerer sproget for stemmen.
* SynthDriver-objekter har nu en language-attribut, der specificerer sproget for den aktuelle stemme.
 * Basisimplementeringen bruger sproget specificeret på VoiceInfo-objekterne i availableVoices. Dette er velegnet til de fleste talesynteser, der understøtter ét sprog pr. stemme.
* Punktdisplay-drivere er blevet forbedret for at tillade, at knapper, hjul og andre kontroller kan bindes til NVDA-scripts:
 * Drivere kan levere en global input gesture  for at tilføje bindinger for scripts hvor som helst i NVDA.
 * De kan også levere deres egne scripts til at udføre specifikke displayfunktioner.
 * Se braille.BrailleDisplayDriver for detaljer og eksisterende punktdisplay-drivere for eksempler.
* Ejendommen 'selfVoicing' på AppModule-klasser er nu blevet omdøbt til 'sleepMode'.
* App-modulbegivenhederne event_appLoseFocus og event_appGainFocus er nu blevet omdøbt til event_appModule_loseFocus og event_appModule_gainFocus, henholdsvis, for at gøre navngivningskonventionen konsistent med app-moduler og træinterceptorer.
* Alle punktdisplay-drivere bør nu bruge braille.BrailleDisplayDriver i stedet for braille.BrailleDisplayDriverWithCursor.
 * Markøren administreres nu uden for driveren.
 * Eksisterende drivere behøver kun at ændre deres klassesætning i overensstemmelse hermed og omdøbe deres _display-metode til display.

## 2010.2

Bemærkelsesværdige funktioner i denne udgivelse inkluderer kraftigt forenklet objektnavigation; virtuelle buffere til Adobe Flash-indhold; adgang til mange tidligere utilgængelige kontroller ved at hente tekst, der er skrevet til skærmen; flad gennemgang af skærmtekst; support for IBM Lotus Symphony-dokumenter; rapportering af tabelrække- og kolonneoverskrifter i Mozilla Firefox; og betydeligt forbedret brugerdokumentation.

### Nye Funktioner

* Navigation gennem objekter med gennemgangsmarkøren er blevet kraftigt forenklet. Gennemgangsmarkøren udelukker nu objekter, som ikke er nyttige for brugeren; dvs. objekter, der kun bruges til layoutformål, og utilgængelige objekter.
* I applikationer, der bruger Java Access Bridge (inklusive OpenOffice.org), kan formatering nu rapporteres i tekstkontroller. (#358, #463)
* Når musen flyttes over celler i Microsoft Excel, vil NVDA korrekt annoncere dem.
* I applikationer, der bruger Java Access Bridge, rapporteres teksten i en dialogboks nu, når dialogboksen vises. (#554)
* En virtuelBuffer kan nu bruges til at navigere i Adobe Flash-indhold. Objektnavigation og interaktion med kontrollerne direkte (ved at aktivere fokustilstand) understøttes stadig. (#453)
* Redigerbare tekstkontroller i Eclipse IDE, inklusive kodeditoren, er nu tilgængelige. Du skal bruge Eclipse 3.6 eller nyere. (#256, #641)
* NVDA kan nu hente det meste tekst, der skrives til skærmen. (#40, #643)
 * Dette gør det muligt at læse kontroller, der ikke udsender information på mere direkte/pålidelige måder.
 * Kontroller, der bliver tilgængelige via denne funktion inkluderer: nogle menupunkter, der viser ikoner (f.eks. menuen Åbn med på filer i Windows XP) (#151), redigerbare tekstfelter i Windows Live-applikationer (#200), fejloversigten i Outlook Express (#582), det redigerbare tekstfelt i TextPad (#605), lister i Eudora, mange kontroller i Australian E-tax og formellinjen i Microsoft Excel.
* Understøttelse af kodeditoren i Microsoft Visual Studio 2005 og 2008. Minimumsversionen skal være Visual Studio Standard; dette virker ikke i Express-udgaverne. (#457)
* Understøttelse af IBM Lotus Symphony-dokumenter.
* Tidlig eksperimentel understøttelse af Google Chrome. Bemærk venligst, at Chromes skærmlæserstøtte langt fra er fuldstændig, og at der kan være behov for yderligere arbejde i NVDA. Du skal bruge en nyere udviklingsudgave af Chrome for at afprøve dette.
* Tilstanden for taster med skiftfunktion (caps lock, num lock og scroll lock) vises nu på punkt, når de trykkes. (#620)
* Hjælpeballoner vises nu på punkt, når de dukker op. (#652)
* Tilføjet en driver til MDV Lilli punktdisplay. (#241)
* Når en hel række eller kolonne vælges i Microsoft Excel med genvejstasterne shift+space og control+space, rapporteres det nye valg nu. (#759)
* Tabelrække- og kolonneoverskrifter kan nu rapporteres. Dette kan konfigureres fra dialogboksen Dokumentformatering.
 * I øjeblikket understøttes dette i dokumenter i Mozilla-applikationer som Firefox (version 3.6.11 og senere) og Thunderbird (version 3.1.5 og senere). (#361)
* Kommandoer til flad gennemgang blev introduceret: (#58)
 * NVDA+numpad7 skifter til flad gennemgang og placerer gennemgangsmarkøren ved det nuværende objekts position, hvilket giver dig mulighed for at gennemgå skærmen (eller et dokument, hvis du er i et) med tekstgennemgangskommandoer.
 * NVDA+numpad1 flytter gennemgangsmarkøren ind i det objekt, der er repræsenteret af teksten ved gennemgangsmarkørens position, hvilket giver dig mulighed for at navigere efter objekt fra dette punkt.
* Aktuelle NVDA-brugerindstillinger kan kopieres til brug på sikre Windows-skærme som logon- og UAC-skærme ved at trykke på en knap i dialogboksen Generelle Indstillinger. (#730)
* Understøttelse af Mozilla Firefox 4.
* Understøttelse af Microsoft Internet Explorer 9.

### Ændringer

* Sig alt ved Navigator-objekt (NVDA+numpadAdd), næste navigator-objekt i flow (NVDA+shift+numpad6) og forrige navigator-objekt i flow (NVDA+shift+numpad4) er blevet fjernet midlertidigt på grund af fejl og for at frigøre taster til andre mulige funktioner.
* I NVDA talesyntesedialogen vises nu kun syntesens visningsnavn. Tidligere blev det forudgået af driverens navn, hvilket kun er relevant internt.
* Når du er i indlejrede applikationer eller virtuelle buffere inde i en anden virtuelBuffer (f.eks. Flash), kan du nu trykke på nvda+control+space for at bevæge dig ud af den indlejrede applikation eller virtuelle buffer til det overordnede dokument. Tidligere blev nvda+space brugt til dette. Nu bruges nvda+space specifikt kun til at skifte mellem gennemsyns-/fokustilstande i virtuelleBuffere.
* Hvis taleviseren (aktiveret i menuen Værktøjer) får fokus (f.eks. ved klik), vil ny tekst ikke vises i kontrolfeltet, før fokus er fjernet. Dette giver mulighed for lettere valg af tekst (f.eks. til kopiering).
* Logviseren og Python-konsollen maksimeres, når de aktiveres.
* Når der fokuseres på et regneark i Microsoft Excel, og der er mere end én celle valgt, annonceres valgintervallet i stedet for kun den aktive celle. (#763)
* Gemning af konfiguration og ændring af bestemte følsomme indstillinger er nu deaktiveret, når du kører på logon-, UAC- og andre sikre Windows-skærme.
* Opdateret eSpeak talesyntese til 1.44.03.
* Hvis NVDA allerede kører, vil aktivering af NVDA-genvejen på skrivebordet (som inkluderer at trykke på control+alt+n) genstarte NVDA.
* Fjernet check boxen Rapportér tekst under musen fra dialogboksen Mus-indstillinger og erstattet det med et check box for Aktiver musesporing, som bedre matcher scriptet til at skifte musesporing (NVDA+m).
* Opdateringer til tastaturlayoutet til bærbare computere, så det inkluderer alle kommandoer tilgængelige i skrivebordslayoutet og fungerer korrekt på ikke-engelske tastaturer. (#798, #800)
* Betydelige forbedringer og opdateringer til brugerdokumentationen, herunder dokumentation af tastaturkommandoer til bærbare computere og synkronisering af hurtigreference til tastaturkommandoer med brugervejledningen. (#455)
* Opdateret liblouis punktskriftsoversætter til 2.1.1. Dette retter især nogle problemer relateret til kinesisk punktskrift samt tegn, der er udefinerede i oversættelsestabellen. (#484, #499)

### Fejlrettelser

* I µTorrent rapporteres det fokuserede element i torrentlisten ikke længere gentagne gange eller stjæler fokus, når en menu er åben.
* I µTorrent rapporteres filnavnene i listen over torrentindhold nu.
* I Mozilla-applikationer registreres fokus nu korrekt, når det lander på en tom tabel eller et træ.
* I Mozilla-applikationer rapporteres "ikke markeret" nu korrekt for kontroller, der kan markeres, såsom markerbare tabelceller. (#571)
* I Mozilla-applikationer ignoreres teksten i korrekt implementerede ARIA-dialoger ikke længere og rapporteres nu, når dialogboksen vises. (#630)
* I Internet Explorer og andre MSHTML-kontroller overholdes ARIA-niveauattributten nu korrekt.
* I Internet Explorer og andre MSHTML-kontroller vælges ARIA-rollen nu over andre typeoplysninger for at give en meget mere korrekt og forudsigelig ARIA-oplevelse.
* En sjælden nedbrud i Internet Explorer ved navigation gennem rammer eller iFrames er stoppet.
* I Microsoft Word-dokumenter kan højre-til-venstre-linjer (som arabisk tekst) læses igen. (#627)
* Kraftigt reduceret forsinkelse, når store mængder tekst vises i en Windows-kommandokonsol på 64-bit-systemer. (#622)
* Hvis Skype allerede er startet, når NVDA starter, er det ikke længere nødvendigt at genstarte Skype for at aktivere tilgængelighed. Dette kan også være tilfældet for andre applikationer, der kontrollerer systemets skærmlæserflag.
* I Microsoft Office-applikationer nedbryder NVDA ikke længere, når tal den forgrund (NVDA+b) trykkes, eller når der navigeres gennem nogle objekter på værktøjslinjer. (#616)
* Rettet fejlagtig udtale af tal, der indeholder et 0 efter et separator; f.eks. 1.023. (#593)
* Adobe Acrobat Pro og Reader 9 går ikke længere ned, når en fil lukkes eller visse andre opgaver udføres. (#613)
* Valget annonceres nu, når control+a trykkes for at vælge al tekst i nogle redigerbare tekstkontroller som i Microsoft Word. (#761)
* I Scintilla-kontroller (f.eks. Notepad++) vælges tekst ikke længere fejlagtigt, når NVDA flytter markøren, som f.eks. under sig alt. (#746)
* Det er igen muligt at gennemgå indholdet af celler i Microsoft Excel med gennemgangsmarkøren.
* NVDA kan igen læse linjevis i visse problematiske tekstområder i Internet Explorer 8. (#467)
* Windows Live Messenger 2009 afsluttes ikke længere med det samme efter start, mens NVDA kører. (#677)
* I webbrowsere er det ikke længere nødvendigt at trykke på tabulator for at interagere med et indlejret objekt (som Flash-indhold) efter at have trykket på enter på det indlejrede objekt eller vendt tilbage fra en anden applikation. (#775)
* I Scintilla-kontroller (f.eks. Notepad++) afkortes begyndelsen af lange linjer ikke længere, når den ruller af skærmen. Disse lange linjer vises også korrekt på punkt, når de er markeret.
* I Loudtalks er det nu muligt at få adgang til kontaktlisten.
* Dokumentets URL og "MSAAHTML Registered Handler" rapporteres ikke længere sporadisk i Internet Explorer og andre MSHTML-kontroller. (#811)
* I trævisninger i Eclipse IDE annonceres det tidligere fokuserede element ikke længere fejlagtigt, når fokus flyttes til et nyt element.
* NVDA fungerer nu korrekt på et system, hvor den aktuelle arbejdsmappe er fjernet fra DLL-søgestien (ved at indstille registreringsnøglen CWDIllegalInDllSearch til 0xFFFFFFFF). Bemærk, at dette ikke er relevant for de fleste brugere. (#907)
* Når tabelnavigationskommandoer bruges uden for en tabel i Microsoft Word, siges "kant af tabel" ikke længere efter "ikke i tabel". (#921)
* Når tabelnavigationskommandoer ikke kan flyttes på grund af at være ved kanten af en tabel i Microsoft Word, siges "kant af tabel" nu på det konfigurerede NVDA-sprog i stedet for altid på engelsk. (#921)
* I Outlook Express, Windows Mail og Windows Live Mail rapporteres tilstanden af check boxerne i meddelelsesregelisten nu. (#576)
* Beskrivelsen af meddelelsesregler kan nu læses i Windows Live Mail 2010.

## 2010.1

Denne udgivelse fokuserer primært på fejlrettelser og forbedringer af brugeroplevelsen, herunder nogle betydelige stabilitetsforbedringer.

### Nye Funktioner

* NVDA starter ikke længere op på et system uden lydudgangsenheder. Naturligvis skal et punktdisplay eller Silence talesyntese sammen med taleviseren bruges til output i dette tilfælde. (#425)
* Et check box til rapportering af landemærker er blevet tilføjet til dialogboksen Dokumentformatering, hvilket giver dig mulighed for at konfigurere, om NVDA skal annoncere landemærker i webdokumenter. For kompatibilitet med den tidligere udgivelse er muligheden aktiveret som standard.
* Hvis "Sig kommandoer" er aktiveret, vil NVDA nu annoncere navne på multimedietaster (f.eks. play, stop, hjemmesiden osv.) på mange tastaturer, når de trykkes. (#472)
* NVDA annoncerer nu det ord, der slettes, når du trykker på control+backspace i kontroller, der understøtter det. (#491)
* Piletaster kan nu bruges i webformatorvinduet til at navigere og læse teksten. (#452)
* Postliste i Microsoft Office Outlook-adressebogen understøttes nu.
* NVDA understøtter bedre indlejrede redigerbare (design mode) dokumenter i Internet Explorer. (#402)
* Et nyt script (nvda+shift+numpadMinus) giver dig mulighed for at flytte systemets fokus til det nuværende navigator-objekt.
* Nye scripts til at låse og låse op for venstre og højre museknap. Nyttigt til at udføre træk og slip operationer. shift+numpadDivide for at låse/låse venstre, shift+numpadMultiply for at låse/låse højre.
* Nye punktskriftoversættelsestabeller: Tysk 8-punkts computer braille, tysk grad 2, finsk 8-punkts computer braille, kinesisk (Hong Kong, kantonesisk), kinesisk (Taiwan, mandarin). (#344, #369, #415, #450)
* Det er nu muligt at deaktivere oprettelsen af genvejen på skrivebordet (og dermed genvejstasten), når du installerer NVDA. (#518)
* NVDA kan nu bruge IAccessible2, når det er til stede i 64-bit applikationer. (#479)
* Forbedret support for liveområder i Mozilla-applikationer. (#246)
* NVDA Controller Client API leveres nu for at give applikationer mulighed for at kontrollere NVDA; f.eks. for at tale tekst, slå tale fra, vise en besked på punkt, osv.
* Informationer og fejlmeddelelser læses nu på logonskærmen i Windows Vista og Windows 7. (#506)
* I Adobe Reader understøttes PDF-interaktive formularer udviklet med Adobe LiveCycle nu. (#475)
* I Miranda IM læser NVDA nu automatisk indkommende beskeder i chatvinduer, hvis rapportering af dynamiske indholdsændringer er aktiveret. Der er også tilføjet kommandoer for at rapportere de tre seneste beskeder (NVDA+control+nummer). (#546)
* Input-tekstfelter understøttes nu i Adobe Flash-indhold. (#461)

### Ændringer

* Den meget omfattende tastaturhjælpsbesked i Windows 7 Start-menuen rapporteres ikke længere.
* Display syntesen er nu erstattet med en ny taleviser. For at aktivere den, vælg Taleviser fra Værktøjer-menuen. Taleviseren kan bruges uafhængigt af den talesyntese, du bruger. (#44)
* Meddelelser på punktdisplayet fjernes automatisk, hvis brugeren trykker på en tast, der resulterer i en ændring, såsom fokusflytning. Tidligere blev meddelelsen altid vist i sin konfigurerede tid.
* Indstilling om punkt skal være bundet til fokus eller gennemgangsmarkør (NVDA+control+t) kan nu også indstilles fra dialogboksen Punktskriftindstillinger og gemmes nu også i brugerens konfiguration.
* Opdateret eSpeak talesyntese til 1.43.
* Opdateret liblouis punktskriftoversætter til 1.8.0.
* I virtuelle buffere er rapportering af elementer ved flytning med tegn eller ord blevet betydeligt forbedret. Tidligere blev en masse irrelevant information rapporteret, og rapporteringen var meget anderledes end ved flytning med linje. (#490)
* Control-tasten stopper nu tale, som andre taster gør, i stedet for at sætte tale på pause. For at pause/genoptage tale skal du bruge shift-tasten.
* Tabelrække- og kolonneantal annonceres ikke længere ved rapportering af fokusændringer, da denne rapportering er ret omfattende og normalt ikke nyttig.

### Fejlrettelser

* NVDA fejler ikke længere ved opstart, hvis UI Automation-support ser ud til at være tilgængelig, men mislykkes i at initialisere af en eller anden grund. (#483)
* Hele indholdet af en tabelrække rapporteres ikke længere nogle gange, når fokus flyttes inde i en celle i Mozilla-applikationer. (#482)
* NVDA oplever ikke længere betydelig forsinkelse, når trævisningselementer, der indeholder et meget stort antal underordnede elementer, udvides.
* Når SAPI 5-stemmer listes, forsøger NVDA nu at opdage defekte stemmer og udelukker dem fra Stemmens Indstillinger-dialogboksen og synteseindstillingsringen. Tidligere, når der var blot én problematisk stemme, kunne NVDA's SAPI 5-driver nogle gange ikke starte.
* Virtuelle buffere respekterer nu indstillingen for genvejstaster til objektpræsentation fundet i dialogboksen Objektpræsentation. (#486)
* I virtuelle buffere læses række-/kolonnekoordinater ikke længere forkert for række- og kolonneoverskrifter, når rapportering af tabeller er deaktiveret.
* I virtuelle buffere læses række-/kolonnekoordinater nu korrekt, når du forlader en tabel og derefter genindtaster samme celle uden først at besøge en anden celle; f.eks. tryk på pil op og derefter pil ned på den første celle i en tabel. (#378)
* Tomme linjer i Microsoft Word-dokumenter og Microsoft HTML-redigeringskontroller vises nu korrekt på punktdisplays. Tidligere viste NVDA den aktuelle sætning på displayet, ikke den aktuelle linje i disse situationer. (#420)
* Flere sikkerhedsrettelser ved kørsel af NVDA på Windows logon og andre sikre skriveborde. (#515)
* Markørpositionen (caret) opdateres nu korrekt ved udførelse af Sig Alt, der går uden for skærmen, i standard Windows-redigeringsfelter og Microsoft Word-dokumenter. (#418)
* I virtuelle buffere inkluderes tekst ikke længere fejlagtigt for billeder inde i links og klikbare elementer, der er markeret som værende irrelevante for skærmlæsere. (#423)
* Rettelser til tastaturlayoutet til bærbare computere. (#517)
* Når punkt er bundet til gennemgangsmarkøren, og du fokuserer på et Dos-konsolvindue, kan gennemgangsmarkøren nu navigere korrekt i teksten i konsollen.
* Mens du arbejder med TeamTalk3 eller TeamTalk4 Classic, annonceres VU-meterets fremgangsbar i hovedvinduet ikke længere, mens den opdateres. Derudover kan specialtegn læses korrekt i det indgående chatvindue.
* Elementer i Windows 7 Startmenuen tales ikke længere to gange. (#474)
* Aktivering af samme-sidelinks i Firefox 3.6 flytter korrekt markøren i den virtuelleBuffer til det rigtige sted på siden.
* Rettet problemet, hvor noget tekst ikke blev gengivet i Adobe Reader i visse PDF-dokumenter.
* NVDA taler ikke længere forkert visse tal adskilt af en bindestreg; f.eks. 500-1000. (#547)
* I Windows XP forårsager NVDA ikke længere, at Internet Explorer fryser ved aktivering af check box i Windows Update. (#477)
* Når den indbyggede eSpeak talesyntese bruges, forårsager samtidig tale og bip ikke længere lejlighedsvise systemfrysninger på nogle systemer. Dette var mest mærkbart, f.eks. ved kopiering af store datamængder i Windows Stifinder.
* NVDA annoncerer ikke længere, at et Firefox-dokument er blevet travlt (f.eks. på grund af en opdatering eller opfriskning), når det dokument er i baggrunden. Dette fik også statuslinjen i forgrundsapplikationen til at blive fejlagtigt annonceret.
* Ved skift af Windows-tastaturlayouts (med control+shift eller alt+shift) rapporteres det fulde navn af layoutet både i tale og på punkt. Tidligere blev det kun rapporteret i tale, og alternative layouts (f.eks. Dvorak) blev slet ikke rapporteret.
* Hvis rapportering af tabeller er deaktiveret, annonceres tabelinformationer ikke længere, når fokus ændres.
* Visse standardtrævisningskontroller i 64-bit applikationer (f.eks. Indholdsoversigten i Microsoft HTML-hjælp) er nu tilgængelige. (#473)
* Rettet nogle problemer med logning af beskeder, der indeholdt ikke-ASCII-tegn. Dette kunne i nogle tilfælde forårsage fejlagtige fejl på ikke-engelske systemer. (#581)
* Informationerne i dialogboksen Om NVDA vises nu på brugerens konfigurerede sprog i stedet for altid på engelsk. (#586)
* Der opstår ikke længere problemer ved brug af synteseindstillingsringen efter at stemmen er ændret til én, der har færre indstillinger end den forrige stemme.
* I Skype 4.2 tales kontaktnavne ikke længere to gange i kontaktlisten.
* Rettet nogle potentielt store hukommelseslækager i GUI'en og i virtuelle buffere. (#590, #591)
* Omgået en irriterende fejl i nogle SAPI 4 talesynteser, som forårsagede hyppige fejl og nedbrud i NVDA. (#597)

## 2009.1

Væsentlige højdepunkter i denne udgivelse inkluderer understøttelse af 64-bit versioner af Windows; kraftigt forbedret understøttelse af Microsoft Internet Explorer og Adobe Reader-dokumenter; understøttelse af Windows 7; læsning af Windows logon-, control+alt+delete- og Brugeradgangskontrol (UAC)-skærme; og muligheden for at interagere med Adobe Flash- og Sun Java-indhold på websider. Der er også foretaget flere væsentlige stabilitetsforbedringer og forbedringer af den generelle brugeroplevelse.

### Nye Funktioner

* Officiel understøttelse af 64-bit versioner af Windows! (#309)
* Tilføjet en driver til Newfon talesyntese. Bemærk, at dette kræver en speciel version af Newfon. (#206)
* I virtuelle buffere kan fokus- og gennemsynstilstand nu rapporteres med lyde i stedet for tale. Dette er som standard aktiveret og kan konfigureres fra dialogboksen Virtuelle buffere. (#244)
* NVDA afbryder ikke længere tale, når lydstyrketaster trykkes på tastaturet, hvilket gør det muligt for brugeren at ændre lydstyrken og lytte til de faktiske resultater med det samme. (#287)
* Fuldstændigt omskrevet understøttelse af Microsoft Internet Explorer og Adobe Reader-dokumenter. Denne understøttelse er blevet forenet med den kerneunderstøttelse, der bruges til Mozilla Gecko, så funktioner som hurtig sideindlæsning, omfattende hurtignavigation, linksliste, tekstvalg, automatisk fokustilstand og punktskriftstøtte nu er tilgængelige med disse dokumenter.
* Forbedret understøttelse af datovalgskontrollen fundet i Windows Vista-dato-/tidsdialogboksen.
* Forbedret understøttelse af Modern XP/Vista startmenu (specifikt "alle programmer" og steder-menuer). Passende niveauinformationer annonceres nu.
* Mængden af tekst, der annonceres, når musen bevæges, kan nu konfigureres fra dialogboksen Mus-indstillinger. Der kan vælges afsnit, linje, ord eller tegn.
* Rapporter stavefejl under markøren i Microsoft Word.
* Understøttelse af stavekontrollen i Microsoft Word 2007. Delvis understøttelse kan være tilgængelig for tidligere versioner af Microsoft Word.
* Bedre understøttelse af Windows Live Mail. Tekstbeskeder kan nu læses, og både tekst- og HTML-beskedkomposering er anvendelige.
* I Windows Vista annoncerer NVDA, når brugeren skifter til det sikre skrivebord (enten fordi en UAC-kontrolboks er dukket op, eller fordi control+alt+delete er blevet trykket).
* NVDA kan annoncere tekst under musen i DOS-konsolvinduer.
* Understøttelse af UI Automation via UI Automation-klient API tilgængelig i Windows 7 samt rettelser for at forbedre NVDA-oplevelsen i Windows 7.
* NVDA kan konfigureres til at starte automatisk efter logon til Windows. Muligheden findes i dialogboksen Generelle Indstillinger.
* NVDA kan læse sikre Windows-skærme som Windows logon, control+alt+delete og Brugeradgangskontrol (UAC)-skærme i Windows XP og nyere. Læsning af Windows logonskærmen kan konfigureres fra dialogboksen Generelle Indstillinger. (#97)
* Tilføjet en driver til Optelec ALVA BC6-serien punktdisplays.
* Ved gennemsyn af webdokumenter kan du nu trykke på n og shift+n for at springe fremad og tilbage forbi blokke af links.
* Ved gennemsyn af webdokumenter rapporteres ARIA-landemærker nu, og du kan flytte fremad og tilbage gennem dem ved hjælp af tasterne d og shift+d. (#192)
* Links-listen tilgængelig ved gennemsyn af webdokumenter er nu blevet til en elementliste, der kan vise links, overskrifter og landemærker. Overskrifter og landemærker præsenteres hierarkisk. (#363)
* Den nye elementliste indeholder et "Filtrér efter"-felt, der giver dig mulighed for at filtrere listen til kun at indeholde de elementer, der inkluderer den indtastede tekst. (#173)
* Bærbare versioner af NVDA ser nu i mappen 'userConfig' inde i NVDA-mappen efter brugerens konfiguration. Ligesom installer-versionen holder dette brugerens konfiguration adskilt fra NVDA selv.
* Brugerdefinerede app-moduler, punktdisplaydrivere og syntesedrivere kan nu gemmes i brugerens konfigurationsmappe. (#337)
* Virtuelle buffere gengives nu i baggrunden, hvilket giver brugeren mulighed for at interagere med systemet i en vis grad under gengivelsesprocessen. Brugeren vil blive informeret om, at dokumentet bliver gengivet, hvis det tager længere end et sekund.
* Hvis NVDA opdager, at det er frosset af en eller anden grund, vil det automatisk lade alle tastetryk passere igennem, så brugeren har større chance for at genoprette systemet.
* Understøttelse af ARIA træk-og-slip i Mozilla Gecko. (#239)
* Dokumentets titel og den aktuelle linje eller markering annonceres nu, når fokus flyttes inden for en virtuel buffer. Dette gør adfærden ved flytning af fokus til virtuelle buffere konsistent med den for normale dokumentobjekter. (#210)
* I virtuelle buffere kan du nu interagere med indlejrede objekter (såsom Adobe Flash og Sun Java-indhold) ved at trykke på enter på objektet. Hvis det er tilgængeligt, kan du derefter navigere rundt med tab-tasten ligesom i enhver anden applikation. For at vende tilbage til dokumentet, tryk NVDA+space. (#431)
* I virtuelle buffere flytter o og shift+o til næste og forrige indlejrede objekt, henholdsvis.
* NVDA kan nu fuldt ud tilgå applikationer, der kører som administrator i Windows Vista og nyere. Du skal installere en officiel udgivelse af NVDA for at få dette til at virke. Dette virker ikke for bærbare versioner og snapshots. (#397)

### Ændringer

* NVDA annoncerer ikke længere "NVDA startet", når det starter.
* Start- og afslutningslyde afspilles nu via NVDA's konfigurerede lydudgangsenhed i stedet for Windows' standardlydudgangsenhed. (#164)
* Rapportering af fremgangsbjælker er blevet forbedret. Mest bemærkelsesværdigt kan du nu konfigurere NVDA til at annoncere både via tale og bip samtidig.
* Nogle generiske roller, såsom rude, applikation og ramme, rapporteres ikke længere ved fokus, medmindre kontrolfeltet er navnløst.
* Kommandoen gennemgangskopi (NVDA+f10) kopierer teksten fra startmarkøren og frem til og med den aktuelle gennemgangsposition, i stedet for at ekskludere den aktuelle position. Dette gør det muligt at kopiere det sidste tegn i en linje, hvilket ikke tidligere var muligt. (#430)
* navigatorObject_where-skriptet (ctrl+NVDA+numpad5) er blevet fjernet. Denne tastekombination fungerede ikke på nogle tastaturer, og scriptet blev ikke fundet særligt nyttigt.
* navigatorObject_currentDimentions-skriptet er blevet omplaceret til NVDA+numpadDelete. Den gamle tastekombination fungerede ikke på nogle tastaturer. Dette script rapporterer nu bredden og højden af objektet i stedet for de højre/bundkoordinater.
* Forbedret ydeevne (især på netbooks), når mange bip lyder hurtigt efter hinanden; f.eks. hurtig musebevægelse med aktiverede lydkoordinater. (#396)
* NVDA-fejlllyden afspilles ikke længere i releasekandidater og endelige udgivelser. Bemærk, at fejl stadig logges.

### Fejlrettelser

* Når NVDA køres fra en 8.3 DOS-sti, men det er installeret i den tilknyttede lange sti (f.eks. progra~1 kontra programfiler), identificerer NVDA korrekt, at det er en installeret kopi og indlæser korrekt brugerens indstillinger.
* At tale titlen på det aktuelle forgrundsvindue med nvda+t fungerer nu korrekt, når du er i menuer.
* Punkt viser ikke længere ubrugelig information i sin fokuskontekst, såsom ikke-navngivne ruder.
* Stop med at annoncere en del ubrugelig information, når fokus ændres, såsom rod-ruder, lagdelte ruder og rulningsruder i Java- eller Lotus-applikationer.
* Gør søgefeltet i Windows Hjælp (CHM) seer meget mere anvendeligt. På grund af fejl i denne kontrol kunne det aktuelle søgeord ikke læses, da det konstant ændrede sig.
* Rapportér de korrekte sidetal i Microsoft Word, hvis sidetallene specifikt er blevet justeret i dokumentet.
* Bedre understøttelse af redigeringsfelter i Microsoft Word-dialoger (f.eks. dialogboksen Skrifttype). Det er nu muligt at navigere disse kontroller med piletasterne.
* Bedre understøttelse af DOS-konsoller. Specifikt: NVDA kan nu læse indholdet af bestemte konsoller, som det tidligere troede var tomme. Ved at trykke på control+break afsluttes NVDA ikke længere.
* På Windows Vista og nyere starter NVDA-installationsprogrammet NVDA med normale brugerrettigheder, når der anmodes om at køre NVDA på slutskærmen.
* Backspace håndteres nu korrekt, når der tales indtastede ord. (#306)
* Rapporter ikke længere "Startmenu" for visse genvejsmenuer i Windows Stifinder/Windows shell. (#257)
* NVDA håndterer nu korrekt ARIA-etiketter i Mozilla Gecko, når der ikke er andet nyttigt indhold. (#156)
* NVDA aktiverer ikke længere automatisk fokustilstand for redigerbare tekstfelter, der opdaterer deres værdi, når fokus ændres; f.eks. http://tigerdirect.com/. (#220)
* NVDA vil nu forsøge at genoprette sig fra nogle situationer, der tidligere ville forårsage, at det fryser fuldstændigt. Det kan tage op til 10 sekunder for NVDA at opdage og genoprette sig fra et sådant frysepunkt.
* Når NVDA-sproget er indstillet til "Brugerstandard", bruges brugerens Windows-sprogsætning i stedet for Windows' landestandard. (#353)
* NVDA genkender nu eksistensen af kontroller i AIM 7.
* Kommandoen for at passere næste tast igennem bliver ikke længere hængende, hvis en tast holdes nede. Tidligere stoppede NVDA med at acceptere kommandoer, hvis dette skete, og skulle genstartes. (#413)
* Proceslinjen ignoreres ikke længere, når den modtager fokus, hvilket ofte sker, når en applikation afsluttes. Tidligere opførte NVDA sig, som om fokus slet ikke var ændret.
* Ved læsning af tekstfelter i applikationer, der bruger Java Access Bridge (inklusive OpenOffice.org), fungerer NVDA nu korrekt, når rapportering af linjenumre er aktiveret.
* Gennemgangskopi-kommandoen (NVDA+f10) håndterer nu korrekt den situation, hvor den bruges på en position før startmarkøren. Tidligere kunne dette forårsage problemer som nedbrud i Notepad++.
* En bestemt kontroltegn (0x1) forårsager ikke længere underlig opførsel i eSpeak (såsom ændringer i lydstyrke og tonehøjde), når det mødes i tekst. (#437)
* Kommandoen for rapportering af tekstmarkering (NVDA+shift+pil op) rapporterer nu korrekt, at der ikke er nogen markering i objekter, der ikke understøtter tekstmarkering.
* Rettet problemet, hvor det at trykke på enter på bestemte Miranda-IM knapper eller links fik NVDA til at fryse. (#440)
* Den aktuelle linje eller markering respekteres nu korrekt, når det aktuelle navigatorobjekt staves eller kopieres.
* Omgået en Windows-fejl, som forårsagede, at skrald blev talt efter navnet på linkkontroller i Windows Stifinder- og Internet Explorer-dialogbokse. (#451)
* Rettet et problem med kommandoen for at rapportere dato og tid (NVDA+f12). Tidligere blev datarapporteringen afskåret på nogle systemer. (#471)
* Rettet problemet, hvor systemets skærmlæserflag nogle gange blev fejlagtigt ryddet efter interaktion med sikre Windows-skærme. Dette kunne forårsage problemer i applikationer, der kontrollerer skærmlæserflaget, herunder Skype, Adobe Reader og Jart. (#462)
* I en Internet Explorer 6-combo box rapporteres det aktive element nu, når det ændres. (#342)

## 0.6p3

### Nye Funktioner

* Da Microsoft Excels formellinje er utilgængelig for NVDA, leveres en NVDA-specifik dialogboks til redigering, når brugeren trykker på f2 på en celle.
* Understøttelse af formatering i IAccessible2-tekstkontroller, herunder Mozilla-applikationer.
* Stavefejl kan nu rapporteres, hvor det er muligt. Dette kan konfigureres fra dialogboksen Dokumentformatering.
* NVDA kan konfigureres til at bippe ved enten alle eller kun synlige fremgangsbjælker. Alternativt kan det konfigureres til at tale fremgangsbjælkernes værdier for hver 10%.
* Links kan nu identificeres i richedit-kontroller.
* Musen kan nu flyttes til tegnet under gennemgangsmarkøren i de fleste redigerbare tekstkontroller. Tidligere kunne musen kun flyttes til midten af kontrollen.
* I virtuelle buffere gennemgår gennemgangsmarkøren nu teksten i bufferen, snarere end bare navigatorobjektets interne tekst (som ofte ikke er nyttig for brugeren). Dette betyder, at du kan navigere den virtuelle buffer hierarkisk ved hjælp af objektnavigation, og gennemgangsmarkøren flyttes til det punkt i bufferen.
* Håndter nogle yderligere tilstande på Java-kontroller.
* Hvis titlen kommandoen (NVDA+t) trykkes to gange, staver den titlen. Hvis den trykkes tre gange, kopieres titlen til udklipsholderen.
* Tastaturhjælpen læser nu navne på modifikatortaster, når de trykkes alene.
* Tastenavne, som annonceres af tastaturhjælp, kan nu oversættes.
* Tilføjet understøttelse for det genkendte tekstfelt i SiRecognizer. (#198)
* Understøttelse af punktdisplays!
* Tilføjet en kommando (NVDA+c) til at rapportere teksten på Windows-udklipsholderen. (#193)
* I virtuelle buffere, hvis NVDA automatisk skifter til fokustilstand, kan du bruge escape-tasten til at skifte tilbage til gennemsynstilstand. NVDA+space kan stadig også bruges.
* I virtuelle buffere, når fokus ændres eller markøren flyttes, kan NVDA automatisk skifte til fokustilstand eller gennemsynstilstand, alt efter hvad der er passende for kontrollen under markøren. Dette konfigureres fra dialogboksen Virtuelle Buffere. (#157)
* Omskrevet SAPI4-syntesedriver, der erstatter sapi4serotek- og sapi4activeVoice-driverne og bør rette de problemer, der blev oplevet med disse drivere.
* NVDA-applikationen inkluderer nu en manifestfil, hvilket betyder, at den ikke længere kører i kompatibilitetstilstand i Windows Vista.
* Konfigurationsfilen og taleordbøger gemmes nu i brugerens applikationsdatamappe, hvis NVDA blev installeret ved hjælp af installationsprogrammet. Dette er nødvendigt for Windows Vista og giver også mulighed for, at flere brugere kan have individuelle NVDA-konfigurationer.
* Tilføjet understøttelse af positionsinformationer for IAccessible2-kontroller.
* Tilføjet muligheden for at kopiere tekst til udklipsholderen ved hjælp af gennemgangsmarkøren. NVDA+f9 indstiller startmarkøren til den aktuelle position af gennemgangsmarkøren. NVDA+f10 henter teksten mellem startmarkøren og den aktuelle position af gennemgangsmarkøren og kopierer den til udklipsholderen. (#240)
* Tilføjet understøttelse af nogle redigeringskontroller i Pinnacle TV-software.
* Når udvalgt tekst rapporteres for lange valg (512 tegn eller mere), rapporterer NVDA nu antallet af valgte tegn i stedet for at læse hele valget. (#249)

### Ændringer

* Hvis lydoutputenheden er indstillet til at bruge Windows standardenhed (Microsoft Sound Mapper), skifter NVDA nu til den nye standardenhed for eSpeak og lydeffekter, når standardenheden ændres. For eksempel skifter NVDA til en USB-lydenhed, hvis den automatisk bliver standardenheden, når den tilsluttes.
* Forbedret ydeevne for eSpeak med nogle Windows Vista-lyddrivere.
* Rapportering af links, overskrifter, tabeller, lister og blokcitater kan nu konfigureres fra dialogboksen Dokumentformatering. Tidligere skulle disse indstillinger for virtuelle buffere konfigureres fra dialogboksen Virtuelle Buffere. Nu deler alle dokumenter denne konfiguration.
* Talehastighed er nu standardindstillingen i synteseindstillingsringen.
* Forbedret ind- og udlæsning af appmoduler.
* Kommandoen Titel (NVDA+t) rapporterer nu kun titlen i stedet for hele objektet. Hvis forgrundsobjektet ikke har noget navn, bruges applikationens procesnavn.
* I stedet for pass-through-tilstand for virtuel buffer til og fra, rapporterer NVDA nu fokustilstand (pass-through til) og gennemsynstilstand (pass-through fra).
* Stemmer gemmes nu i konfigurationsfilen efter ID i stedet for efter indeks. Dette gør stemmeindstillingerne mere pålidelige på tværs af systemer og konfigurationsændringer. Stemmeindstillingen bevares ikke i gamle konfigurationer, og der kan logges en fejl første gang, en syntese bruges. (#19)
* Niveauet for et trævisningselement rapporteres nu først, hvis det har ændret sig fra det tidligere fokuserede element i alle trævisninger. Tidligere skete dette kun for native Windows (SysTreeView32) trævisninger.

### Fejlrettelser

* Den sidste lyddel afbrydes ikke længere, når NVDA bruges med eSpeak på en fjernskrivebordsserver.
* Rettet problemer med lagring af taleordbøger for visse stemmer.
* Eliminér forsinkelsen, når der navigeres med enheder, der ikke er tegn (ord, linje osv.) mod bunden af store tekstdokumenter i Mozilla Gecko virtuelle buffere. (#155)
* Hvis "Sig indtastede ord" er aktiveret, annonceres ordet, når der trykkes på enter.
* Rettet nogle tegnsætningsproblemer i richedit-dokumenter.
* NVDA-logviseren bruger nu richedit i stedet for blot edit til at vise loggen. Dette forbedrer læsning med NVDA.
* Rettet nogle problemer relateret til indlejrede objekter i richedit-kontroller.
* NVDA læser nu sidetal i Microsoft Word. (#120)
* Rettet problemet, hvor faneblad til et markeret check box i en Mozilla Gecko virtuel buffer og tryk på mellemrumstasten ikke annoncerede, at check box blev fjernet markeringen fra.
* Rapporter korrekt delvist markerede check box i Mozilla-applikationer.
* Hvis tekstvalget udvides eller krympes i begge retninger, læses valget nu som ét stykke i stedet for to.
* Når der læses med musen, læses tekst i Mozilla Gecko-redigeringsfelter nu korrekt.
* Sig Alt bør ikke længere få visse SAPI5 talesynteser til at gå ned.
* Rettet et problem, hvor tekstvalgsændringer ikke blev læst i Windows standard redigeringsfelter før første fokusændring efter NVDA blev startet.
* Rettet muse-sporing i Java-objekter. (#185)
* NVDA rapporterer ikke længere Java trævisningselementer uden underordnede som værende sammenklappet.
* Annoncér objektet med fokus, når et Java-vindue kommer til forgrunden. Tidligere blev kun Java's øverste niveau-objekt annonceret.
* eSpeak-syntesedriveren stopper ikke længere helt med at tale efter en enkelt fejl.
* Rettet problemet, hvor opdaterede stemmeparametre (hastighed, tonehøjde osv.) ikke blev gemt, når stemmen blev ændret fra synteseindstillingsringen.
* Forbedret tale af indtastede tegn og ord.
* Ny tekst, der tidligere ikke blev talt i tekstkonsolapplikationer (såsom nogle tekst-eventyrspil), læses nu.
* NVDA ignorerer nu fokusændringer i baggrundsvinduer. Tidligere kunne en baggrunds-fokusændring behandles, som om det virkelige fokus havde ændret sig.
* Forbedret detektering af fokus, når kontekstmenuer forlades. Tidligere reagerede NVDA ofte slet ikke, når kontekstmenuen blev forladt.
* NVDA annoncerer nu, når kontekstmenuen aktiveres i Startmenuen.
* Den klassiske startmenu annonceres nu som startmenu i stedet for applikationsmenu.
* Forbedret læsning af advarsler som dem, der stødes på i Mozilla Firefox. Teksten læses ikke længere flere gange, og anden overflødig information læses ikke længere. (#248)
* Teksten i fokuserbare, skrivebeskyttede redigeringsfelter medtages ikke længere, når dialogbokse henter tekst. Dette løser f.eks. automatisk læsning af hele licensaftalen i installationsprogrammer.
* NVDA annoncerer ikke længere fjernelse af tekstmarkering, når nogle redigeringsfelter forlades (f.eks. Internet Explorer adressefeltet, Thunderbird 3 e-mail adressefelter).
* Når almindelige tekst-e-mails åbnes i Outlook Express og Windows Mail, placeres fokus korrekt i beskeden klar til, at brugeren kan læse den. Tidligere skulle brugeren trykke på tab-tasten eller klikke på beskeden for at bruge piletasterne til at læse den.
* Rettet flere større problemer med "Sig kommandoer" funktionalitet.
* NVDA kan nu læse tekst, der overstiger 65535 tegn i standardredigeringsfelter (f.eks. en stor fil i Notesblok).
* Forbedret linjelæsning i MSHTML redigeringsfelter (Outlook Express redigerbare beskeder og Internet Explorer tekstinputfelter).
* NVDA fryser ikke længere helt, når tekst redigeres i OpenOffice. (#148, #180)

## 0.6p2

* Forbedret standardstemmen til eSpeak i NVDA
* Tilføjet et tastaturlayout til bærbare computere. Tastaturlayouts kan konfigureres fra NVDA's Tastaturindstillinger dialog. (#60)
* Understøttelse af grupperede elementer i SysListView32-kontroller, primært fundet i Windows Vista. (#27)
* Rapporter check box-tilstand for trævisningselementer i SysTreeview32-kontroller.
* Tilføjet genvejstaster for mange af NVDA's konfigurationsdialogbokse.
* Understøttelse af IAccessible2 aktiverede applikationer som Mozilla Firefox, når NVDA kører fra bærbare medier, uden at skulle registrere specielle Dll-filer.
* Rettet et nedbrud med linkslisten i virtuelle buffere i Gecko-applikationer. (#48)
* NVDA bør ikke længere nedbryde Mozilla Gecko-applikationer som Firefox og Thunderbird, hvis NVDA kører med højere privilegier end Mozilla Gecko-applikationen. F.eks. hvis NVDA kører som administrator.
* Taleordbøger (tidligere Brugerdictionaries) kan nu enten være store/små-bogstavsfølsomme eller følsomme, og mønstrene kan valgfrit være regulære udtryk. (#39)
* Hvorvidt NVDA bruger en 'skærmlayout'-tilstand for virtuelle bufferdokumenter kan nu konfigureres fra en indstillingsdialog.
* Rapporter ikke længere anker-tags uden href i Gecko-dokumenter som links. (#47)
* NVDA's søgekommando husker nu, hvad du sidst søgte efter, på tværs af alle applikationer. (#53)
* Rettet problemer, hvor check box-tilstanden ikke ville blive annonceret for nogle check box og radioknapper i virtuelle buffere.
* Pass-through-tilstand for virtuelle buffere er nu specifik for hvert dokument i stedet for NVDA globalt. (#33)
* Rettet en langsommelighed med fokusændringer og forkert taleafbrydelse, der nogle gange opstod, når NVDA blev brugt på et system, der havde været i standby eller var ret langsomt.
* Forbedret understøttelse af kombinationsbokse i Mozilla Firefox. Specifikt gentages tekst ikke, når der navigeres med piletasterne, og når der springes ud af dem, annonceres ikke unødvendigt overordnede kontroller. Virtuelle buffer-kommandoer fungerer også, når de er fokuseret på en, når du er i en virtuel buffer.
* Forbedret præcision af statuslinjefinding i mange applikationer. (#8)
* Tilføjet NVDA interaktivt Python-konsolværktøj, der gør det muligt for udviklere at se på og manipulere NVDA's interne systemer, mens det kører.
* Kommandoerne Sig alt, rapporter valg og rapporter aktuel linje fungerer nu korrekt, når du er i pass-through-tilstand for virtuelle buffere. (#52)
* Øg og formindsk talekommandoerne er blevet fjernet. Brugere bør bruge synteseindstillingsringens kommandoer (control+nvda+piletaster) eller dialogboksen Stemmens indstillinger.
* Forbedret skala og rækkevidde for bip i fremgangsbjælker.
* Tilføjet flere hurtige taster til nye virtuelle buffere: l for liste, i for listeelement, e for redigeringsfelt, b for knap, x for check box, r for radioknap, g for grafik, q for blokcitat, c for kombinationsboks, 1 gennem 6 for respektive overskriftsniveauer, s for separator, m for ramme. (#67, #102, #108)
* Annullering af indlæsning af et nyt dokument i Mozilla Firefox giver nu brugeren mulighed for at fortsætte med at bruge den gamle dokuments virtuelle buffer, hvis det gamle dokument endnu ikke var blevet slettet. (#63)
* Navigation efter ord i virtuelle buffere er nu mere præcis, da ord ikke ved en fejl indeholder tekst fra mere end ét felt. (#70)
* Forbedret præcision af fokussporing og fokusopdatering ved navigation i Mozilla Gecko virtuelle buffere.
* Tilføjet findForrige-kommando (shift+NVDA+f3) til brug i nye virtuelle buffere.
* Forbedret langsomhed i Mozilla Gecko-dialoger (i Firefox og Thunderbird). (#66)
* Tilføjet muligheden for at se den aktuelle logfil for NVDA. Den findes i NVDA-menuen -> Værktøjer.
* Kommandoer som sig tid og dato tager nu det aktuelle sprog i betragtning; tegnsætning og ordstilling afspejler nu sproget.
* Sprogkombinationsboksen i NVDA's Generelle Indstillinger dialog viser nu fulde sprognavne for nem brug.
* Ved gennemgang af tekst i det aktuelle navigatorobjekt er teksten altid opdateret, hvis den ændres dynamisk. F.eks. gennemgang af teksten i et listeelement i Jobliste. (#15)
* Når der flyttes med musen, annonceres nu det aktuelle tekstafsnit under musen, i stedet for enten al teksten i det pågældende objekt eller blot det aktuelle ord. Også lydkoordinater og annoncering af objektroller er valgfri, og de er som standard deaktiveret.
* Understøttelse af læsning af tekst med musen i Microsoft Word.
* Rettet en fejl, hvor efterladelse af menulinjen i applikationer som Wordpad ville medføre, at tekstvalget ikke længere blev annonceret.
* I Winamp annonceres sporets titel ikke længere igen og igen, når du skifter spor eller pauser/genoptager/stopper afspilning.
* I Winamp tilføjet evnen til at annoncere status for shuffle- og repeat-kontroller, mens de skiftes. Fungerer i hovedvinduet og i afspilningslisteeditoren.
* Forbedret evnen til at aktivere bestemte felter i Mozilla Gecko virtuelle buffere. Dette kan inkludere klikbare grafik, links, der indeholder afsnit, og andre mærkelige strukturer.
* Rettet indledende forsinkelse ved åbning af NVDA-dialoger på nogle systemer. (#65)
* Tilføjet specifik understøttelse af Total Commander-applikationen.
* Rettet fejl i sapi4serotek-driveren, hvor tonehøjden kunne låses ved en bestemt værdi, f.eks. forbliver høj efter læsning af et stort bogstav. (#89)
* Annoncer klikbar tekst og andre felter som klikbare i Mozilla Gecko Virtuelle Buffere. F.eks. et felt, der har en onclick HTML-attribut. (#91)
* Når der navigeres rundt i Mozilla Gecko virtuelle buffere, rulles det aktuelle felt nu i syne – nyttigt, så seende kolleger har en idé om, hvor brugeren er kommet til i dokumentet. (#57)
* Tilføjet grundlæggende understøttelse af ARIA liveområder i IAccessible2-aktiverede applikationer. Nyttigt i Chatzilla IRC-applikationen, hvor nye beskeder nu vil blive læst automatisk.
* Nogle små forbedringer for at hjælpe med at bruge ARIA-aktiverede webapplikationer, f.eks. Google Docs.
* Stop med at tilføje ekstra tomme linjer til tekst, når den kopieres fra en virtuel buffer.
* Stop mellemrumstasten fra at aktivere et link i Links-listen. Nu kan det bruges ligesom andre bogstaver til at begynde at skrive navnet på et bestemt link, du vil gå til.
* Kommandoen moveMouseToNavigator (NVDA+numpadSlash) flytter nu musen til midten af navigatorobjektet i stedet for øverst til venstre.
* Tilføjet scripts til at klikke på venstre og højre museknap (numpadSlash og numpadStar henholdsvis).
* Forbedret adgang til Windows' Systembakke. Fokus bør forhåbentlig ikke længere synes at springe tilbage til et bestemt element. Husk: For at få adgang til Systembakken brug Windows-tasten WindowsKey+b. (#10)
* Forbedret ydeevne og stop annoncering af ekstra tekst, når en piletast holdes nede i et redigeringsfelt, og det når slutningen.
* Stop NVDA fra at få brugeren til at vente, mens bestemte beskeder læses. Retter nogle nedbrud/frysninger med bestemte talesynteser. (#117)
* Tilføjet understøttelse af Audiologic Tts3 talesyntese, bidraget af Gianluca Casalino. (#105)
* Forbedret ydeevne ved navigation af dokumenter i Microsoft Word.
* Forbedret præcision ved læsning af advarsler i Mozilla Gecko-applikationer.
* Stop med at forårsage nedbrud, når du prøver at gemme konfigurationen på ikke-engelske versioner af Windows. (#114)
* Tilføjet en NVDA velkomstdialog. Denne dialog er designet til at give væsentlige oplysninger til nye brugere og tillader, at CapsLock kan konfigureres som en NVDA-modifikatortast. Denne dialog vil blive vist, når NVDA starter som standard, indtil den deaktiveres.
* Rettet grundlæggende understøttelse af Adobe Reader, så det er muligt at læse dokumenter i versionerne 8 og 9.
* Rettet nogle fejl, der kan være opstået, når taster blev holdt nede, før NVDA var fuldt initialiseret.
* Hvis brugeren har konfigureret NVDA til at gemme konfigurationen ved afslutning, sørg for, at konfigurationen er korrekt gemt, når Windows lukkes ned eller logger ud.
* Tilføjet en NVDA logo-lyd i starten af installationsprogrammet, bidraget af Victer Tsaran.
* NVDA, både når det kører i installationsprogrammet og ellers, rydder korrekt sin systembakkeikon, når det afsluttes.
* Etiketternes standardkontroller i NVDA's dialogbokse (såsom Ok- og Annuller-knapper) vises nu på det sprog, NVDA er indstillet til, i stedet for bare at blive på engelsk.
* NVDA's ikon bruges nu til NVDA-genvejene i startmenuen og på skrivebordet i stedet for et standardprogramikon.
* Læs celler i MS Excel, når der navigeres med tab og shift+tab. (#146)
* Rettet nogle dobbeltudtalelser i bestemte lister i Skype.
* Forbedret markørsporing i IAccessible2- og Java-applikationer; f.eks. i OpenOffice og Lotus Symphony, venter NVDA korrekt på, at markøren flyttes i dokumenter i stedet for ved et uheld at læse det forkerte ord eller linje ved slutningen af nogle afsnit. (#119)
* Understøttelse af AkelEdit-kontroller fundet i Akelpad 4.0.
* NVDA fryser ikke længere i Lotus Symphony, når der flyttes fra dokumentet til menulinjen.
* NVDA fryser ikke længere i Windows XP-tilføj/fjern-program applet, når en afinstallationsprogram startes. (#30)
* NVDA fryser ikke længere, når Spybot Search and Destroy åbnes.

## 0.6p1

### Adgang til webindhold med nye in-process virtuelle buffere (indtil videre for Mozilla Gecko-applikationer, herunder Firefox3 og Thunderbird3)

* Indlæsningstider er blevet forbedret næsten tredive gange (du behøver slet ikke længere vente på, at de fleste websider indlæses i bufferen).
* Tilføjet en links-liste (NVDA+f7).
* Forbedret søgedialogen (control+nvda+f), så den udfører en ikke-følsom søgning, plus rettet et par fokusproblemer med den dialogboks.
* Det er nu muligt at vælge og kopiere tekst i de nye virtuelle buffere.
* Som standard repræsenterer de nye virtuelle buffere dokumentet i et skærmlayout (links og kontroller er ikke på separate linjer, medmindre de virkelig er visuelt). Du kan skifte denne funktion med NVDA+v.
* Det er muligt at navigere med afsnit ved hjælp af control+pil op og control+pil ned.
* Forbedret understøttelse af dynamisk indhold.
* Forbedret overordnet nøjagtighed ved læsning af linjer og felter, når der navigeres op og ned med piletasterne.

### Internationalisering

* Det er nu muligt at skrive accentuerede tegn, der er afhængige af et "dødt tegn", mens NVDA kører.
* NVDA annoncerer nu, når tastaturlayoutet ændres (når der trykkes på alt+shift).
* Funktionen annoncer dato og tid tager nu systemets aktuelle regionale og sproglige indstillinger i betragtning.
* Tilføjet tjekkisk oversættelse (af Tomas Valusek med hjælp fra Jaromir Vit).
* Tilføjet vietnamesisk oversættelse af Dang Hoai Phuc.
* Tilføjet afrikaans (af_ZA) oversættelse, af Willem van der Walt.
* Tilføjet russisk oversættelse af Dmitry Kaslin.
* Tilføjet polsk oversættelse af DOROTA CZAJKA og venner.
* Tilføjet japansk oversættelse af Katsutoshi Tsuji.
* Tilføjet thai oversættelse af Amorn Kiattikhunrat.
* Tilføjet kroatisk oversættelse af Mario Percinic og Hrvoje Katic.
* Tilføjet galicisk oversættelse af Juan C. Buno.
* Tilføjet ukrainsk oversættelse af Aleksey Sadovoy.

### Tale

* NVDA leveres nu med eSpeak 1.33, som indeholder mange forbedringer, herunder forbedrede sprog, navngivne varianter og evnen til at tale hurtigere.
* Stemmens indstillinger dialogboksen giver dig nu mulighed for at ændre varianten af en talesyntese, hvis den understøtter en. Variant er normalt en let variation af den nuværende stemme. (eSpeak understøtter varianter).
* Tilføjet muligheden for at ændre tonefaldet af en stemme i Stemmens indstillinger dialogboksen, hvis den aktuelle talesyntese understøtter dette. (eSpeak understøtter tonefald).
* Tilføjet muligheden for at slå tale af objektpositionsinformation fra (f.eks. 1 af 4). Denne indstilling findes i dialogboksen Objektpræsentation.
* NVDA kan nu bippe, når et stort bogstav siges. Dette kan slås til og fra med et check box i Stemmens indstillinger dialogboksen. Der er også tilføjet et check box til at konfigurere, om NVDA skal hæve tonehøjden for store bogstaver. Så nu kan du vælge mellem hævet tonehøjde, sige "stort", eller bippe ved store bogstaver.
* Tilføjet muligheden for at pause tale i NVDA (som fundet i Voice Over til Mac). Når NVDA taler noget, kan du trykke på control- eller shift-tasten for at stoppe tale, ligesom normalt, men hvis du derefter trykker på shift-tasten igen (så længe du ikke har trykket på nogen andre taster), vil tale fortsætte fra det præcise sted, hvor det stoppede.
* Tilføjet en virtuel syntesedriver, der outputter tekst til et vindue i stedet for at tale via en talesyntese. Dette bør være mere behageligt for seende udviklere, der ikke er vant til talesyntese, men vil vide, hvad der siges af NVDA. Der er sandsynligvis stadig nogle fejl, så feedback er bestemt velkommen.
* NVDA taler som standard ikke længere tegnsætning, du kan aktivere tale af tegnsætning med NVDA+p.
* eSpeak taler nu som standard meget langsommere, hvilket bør gøre det nemmere for folk, der bruger eSpeak for første gang, når de installerer eller begynder at bruge NVDA.
* Tilføjet brugerordbøger til NVDA. Disse giver dig mulighed for at få NVDA til at sige visse tekststykker anderledes. Der er tre ordbøger: standard, stemme og midlertidig. Indgange du tilføjer til standardordbogen vil gælde hele tiden i NVDA. Stemmeordbøger er specifikke for den aktuelle talesyntese og stemme, du har indstillet. Og midlertidig ordbog er til de tidspunkter, hvor du hurtigt vil oprette en regel, mens du udfører en bestemt opgave, men ikke ønsker, at den skal være permanent (den forsvinder, når du lukker NVDA). For nu er reglerne regulære udtryk, ikke bare normal tekst.
* Talesynteser kan nu bruge enhver lydudgangsenhed på dit system ved at indstille udgangsenheden i syntesedialogboksen, før du vælger den talesyntese, du vil bruge.

### Ydeevne

* NVDA bruger ikke længere en enorm mængde systemhukommelse, når beskeder redigeres i MSHTML-redigeringsfelter.
* Forbedret ydeevne ved gennemgang af tekst i mange kontroller, der ikke har en reel markør. F.eks. MSN Messenger historie-vinduet, trævisningselementer, listevisningselementer osv.
* Forbedret ydeevne i richedit-dokumenter.
* NVDA bør ikke længere langsomt bruge mere systemhukommelse uden nogen åbenbar grund.
* Rettet fejl ved forsøg på at fokusere på et DOS-konsolvindue mere end tre gange. NVDA havde en tendens til at gå fuldstændig ned.

### Tastaturkommandoer

* NVDA+shift+numpad6 og NVDA+shift+numpad4 giver dig mulighed for at navigere til det næste eller forrige objekt i flowet. Dette betyder, at du kan navigere i en applikation ved kun at bruge disse to taster uden at skulle bekymre dig om at gå op til overordnet objekt eller ned til første barn, mens du bevæger dig rundt i objektets hierarki. For eksempel i en webbrowser som Firefox kan du navigere dokumentet ved objekt ved blot at bruge disse to taster. Hvis næste i flow eller forrige i flow tager dig op og ud af et objekt eller ned i et objekt, høres ordnede bip, der indikerer retningen.
* Du kan nu konfigurere stemmeindstillinger uden at åbne stemmens indstillinger dialogboksen ved at bruge synteseindstillingsringen. Synteseindstillingsringen er en gruppe af stemmeindstillinger, du kan skifte mellem ved at trykke på control+NVDA+pil højre og control+NVDA+pil venstre. For at ændre en indstilling skal du bruge control+NVDA+pil op og control+NVDA+pil ned.
* Tilføjet en kommando til at rapportere den aktuelle markering i redigeringsfelter (NVDA+shift+pil op).
* En række NVDA-kommandoer, der læser tekst (såsom rapporter aktuel linje osv.), kan nu stave teksten, hvis de trykkes to gange hurtigt.
* CapsLock, numpad insert og extended insert kan alle bruges som NVDA-modifikatortasten. Også, hvis en af disse taster bruges, vil dobbelttryk på tasten uden at trykke på andre taster sende tasten igennem til operativsystemet, ligesom du ville gøre, hvis NVDA ikke kørte. For at gøre en af disse taster til NVDA-modifikatortasten skal du markere dens check box i dialogboksen Tastaturets indstillinger (tidligere kaldet tastaturets ekko dialogboksen).

### Applikationsunderstøttelse

* Forbedret understøttelse af Firefox3 og Thunderbird3 dokumenter. Indlæsningstider er forbedret næsten tredive gange, et skærmlayout bruges som standard (tryk på NVDA+v for at skifte mellem dette og uden skærmlayout), en links-liste (NVDA+f7) er blevet tilføjet, søgedialogen (control+NVDA+f) er nu ikke-følsom for store/små bogstaver, betydeligt forbedret understøttelse af dynamisk indhold, valg og kopiering af tekst er nu muligt.
* I MSN Messenger og Windows Live Messenger historie-vinduerne er det nu muligt at vælge og kopiere tekst.
* Forbedret understøttelse af Audacity-applikationen.
* Tilføjet understøttelse af nogle redigerings- og tekstkontroller i Skype.
* Forbedret understøttelse af Miranda Instant Messenger-applikationen.
* Rettet fokusproblemer, når HTML- og almindelige tekstbeskeder åbnes i Outlook Express.
* Outlook Express nyhedsgruppe-beskedfelter er nu korrekt mærket.
* NVDA kan nu læse adresserne i Outlook Express' beskedfelter (til/fra/cc osv.).
* NVDA bør nu være mere præcis ved annoncering af næste besked i Outlook Express, når der slettes en besked fra beskedlisten.

### API'er og værktøjssæt

* Forbedret objektnavigation for MSAA-objekter. Hvis et vindue har en systemmenu, titellinje eller rullepaneler, kan du nu navigere til dem.
* Tilføjet understøttelse af IAccessible2 tilgængeligheds-API'en. Ud over muligheden for at annoncere flere kontroltyper gør dette også NVDA i stand til at få adgang til markøren i applikationer som Firefox 3 og Thunderbird 3, hvilket giver dig mulighed for at navigere, vælge eller redigere tekst.
* Tilføjet understøttelse af Scintilla redigeringskontroller (sådanne kontroller findes i Notepad++ eller TortoiseSVN).
* Tilføjet understøttelse af Java-applikationer (via Java Access Bridge). Dette kan give grundlæggende understøttelse af OpenOffice (hvis Java er aktiveret) og andre selvstændige Java-applikationer. Bemærk, at Java-applikationer i en webbrowser muligvis ikke fungerer endnu.

### Mus

* Forbedret understøttelse af læsning af, hvad der er under musemarkøren, mens den flyttes. Det er nu meget hurtigere, og det har også nu evnen i nogle kontroller som standard redigeringsfelter, Java- og IAccessible2-kontroller, til at læse det aktuelle ord, ikke kun det aktuelle objekt. Dette kan være nyttigt for synshæmmede personer, der bare vil læse et specifikt tekststykke med musen.
* Tilføjet en ny konfigurationsmulighed, som findes i dialogboksen Mus-indstillinger. Afspil lyd, når musen bevæges; når aktiveret, afspilles et 40 ms bip hver gang musen bevæges, med tonehøjden (mellem 220 og 1760 hz), der repræsenterer y-aksen og venstre/højre lydstyrke, der repræsenterer x-aksen. Dette giver en blind person mulighed for at få en grov idé om, hvor musen er på skærmen, mens den bevæges. Denne funktion afhænger også af, at reportObjectUnderMouse er aktiveret. Det betyder, at hvis du hurtigt skal deaktivere både bip og annoncering af objekter, så tryk blot på NVDA+m. Bipene er også højere eller blødere afhængigt af, hvor lys skærmen er på det punkt.

### Objektpræsentation og interaktion

* Forbedret understøttelse af de mest almindelige trævisningskontroller. NVDA fortæller nu, hvor mange elementer der er i grenen, når du udvider den. Det annoncerer også niveauet, når du flytter ind og ud af grene. Og det annoncerer det aktuelle elementnummer og antal elementer, ifølge den aktuelle gren, ikke hele trævisningen.
* Forbedret, hvad der annonceres, når fokus ændres, mens du bevæger dig rundt i applikationer eller operativsystemet. Nu hører du, i stedet for bare kontrollen, du lander på, også information om eventuelle kontroller, denne kontrol er placeret inde i. For eksempel hvis du tab'er og lander på en knap inde i en gruppeboks, vil gruppeboksen også blive annonceret.
* NVDA forsøger nu at tale beskeden inde i mange dialogbokse, når de vises. Dette er præcist det meste af tiden, men der er stadig mange dialogbokse, der ikke er så gode, som de kunne være.
* Tilføjet en "Rapporter objektbeskrivelser" check box i dialogboksen Objektpræsentation. Erfarne brugere vil måske nogle gange fjerne markeringen af dette for at stoppe NVDA i at annoncere mange ekstra beskrivelser på bestemte kontroller, som i Java-applikationer.
* NVDA annoncerer automatisk markeret tekst i redigeringsfelter, når fokus flyttes til dem. Hvis der ikke er markeret tekst, annonceres den aktuelle linje som sædvanlig.
* NVDA er nu meget mere omhyggelig, når det afspiller bip for at indikere ændringer i fremgangsbjælker i applikationer. Det går ikke længere amok i Eclipse-applikationer som Lotus Notes/Symphony og Accessibility Probe.

### Brugergrænseflade

* Fjernet NVDA-grænsefladevinduet og erstattet det med en simpel NVDA-popupmenu.
* NVDA's brugergrænsefladeindstillinger dialogboksen kaldes nu Generelle Indstillinger. Den indeholder også en ekstra indstilling: en kombinationsboks til at indstille logningsniveauet for, hvilke meddelelser der skal sendes til NVDA's logfil. Bemærk, at NVDA's logfil nu hedder nvda.log i stedet for debug.log.
* Fjernet rapportering af objektgruppenavne fra objektpræsentationsindstillingerne. Rapportering af gruppenavne håndteres nu anderledes.

## 0.5

* NVDA har nu en indbygget talesyntese kaldet eSpeak, udviklet af Jonathan Duddington. Den er meget responsiv og letvægts, og har understøttelse af mange forskellige sprog. SAPI-talesynteser kan stadig bruges, men eSpeak vil være standardtalesyntesen.
 * eSpeak er ikke afhængig af nogen speciel softwareinstallation, så den kan bruges med NVDA på enhver computer, fra et USB-drev, eller hvor som helst.
 * For mere information om eSpeak, eller for at finde andre versioner, gå til [http://espeak.sourceforge.net/](http://espeak.sourceforge.net/).
* Rettet fejl, hvor det forkerte tegn blev annonceret, når der blev trykket på delete i Internet Explorer/Outlook Express redigerbare felter.
* Tilføjet understøttelse af flere redigeringsfelter i Skype.
* Virtuelle buffere indlæses kun, når fokus er på vinduet, der skal indlæses. Dette løser nogle problemer, når forhåndsvisningsruden er aktiveret i Outlook Express.
* Tilføjet kommandolinjeargumenter til NVDA:
 * -m, --minimal: spiller ikke opstarts-/afslutningslyde og viser ikke grænsefladen ved opstart, hvis denne indstilling er valgt.
 * -q, --quit: afslut enhver anden allerede kørende instans af NVDA og afslut derefter.
 * -s, --stderr-file filNavn: specificerer, hvor NVDA skal placere ukontrollerede fejl og undtagelser.
 * -d, --debug-file filNavn: specificerer, hvor NVDA skal placere fejlfindingbeskeder.
 * -c, --config-file: specificerer en alternativ konfigurationsfil.
 * -h, --help: viser en hjælpemeddelelse, der lister kommandolinjeargumenter.
* Rettet fejl, hvor tegnsætningstegn ikke blev oversat til det korrekte sprog, når der blev brugt et andet sprog end engelsk, og når "tal indtastede tegn" var aktiveret.
* Tilføjet slovakiske sprogfiler takket være Peter Vagner.
* Tilføjet en virtuel buffer-indstillinger dialog og en dokumentformateringsindstillinger dialog, fra Peter Vagner.
* Tilføjet fransk oversættelse takket være Michel Such.
* Tilføjet et script til at skifte bip for fremgangsbjælker til og fra (insert+u). Bidraget af Peter Vagner.
* Flere beskeder i NVDA kan nu oversættes til andre sprog. Dette inkluderer scriptbeskrivelser, når man er i tastaturhjælp.
* Tilføjet en søgedialog til virtuelle buffere (Internet Explorer og Firefox). Ved at trykke på control+f på en side åbnes en dialog, hvor du kan indtaste noget tekst til at finde. Ved at trykke på enter vil denne tekst blive søgt, og den virtuelle buffers markør vil placeres på denne linje. Ved at trykke på f3 vil du også søge efter den næste forekomst af teksten.
* Når "tal indtastede tegn" er aktiveret, bør flere tegn nu blive talt. Teknisk set kan tegn fra ASCII 32 til 255 nu tales.
* Omdøbt nogle kontroltyper for bedre læsbarhed. Redigerbar tekst er nu redigeringsfelt, outline er nu trævisning, og trykknap er nu knap.
* Når man navigerer rundt i listeelementer i en liste eller trævisningselementer i en trævisning, tales kontroltypen (listeelement, trævisningselement) ikke længere, for at gøre navigationen hurtigere.
* "Har popup" (for at indikere, at en menu har en undermenu) tales nu som "undermenu".
* Hvor nogle sprog bruger kontrol og alt (eller altGR) til at indtaste et specialtegn, vil NVDA nu tale disse tegn, når "tal indtastede tegn" er aktiveret.
* Rettet nogle problemer med gennemgang af statiske tekstkontroller.
* Tilføjet traditionel kinesisk oversættelse takket være Coscell Kao.
* Omstruktureret en vigtig del af NVDA's kode, som nu burde rette mange problemer med NVDA's brugergrænseflade (herunder indstillingsdialogbokse).
* Tilføjet SAPI4-understøttelse til NVDA. Der er i øjeblikket to SAPI4-drivere, en baseret på kode bidraget af Serotek Corporation og en, der bruger ActiveVoice.ActiveVoice COM-interface. Begge disse drivere har problemer, se hvilken der fungerer bedst for dig.
* Nu, når man prøver at køre en ny kopi af NVDA, mens en ældre kopi allerede kører, vil den nye kopi blot afslutte. Dette løser et stort problem, hvor kørsel af flere kopier af NVDA gør dit system meget ubrugeligt.
* Omdøbt titlen på NVDA's brugergrænseflade fra NVDA Interface til NVDA.
* Rettet en fejl i Outlook Express, hvor tryk på backspace i starten af en redigerbar besked forårsagede en fejl.
* Tilføjet patch fra Rui Batista, der tilføjer et script til at rapportere den aktuelle batteristatus på bærbare computere (insert+shift+b).
* Tilføjet en talesyntesedriver kaldet Silence. Dette er en talesyntesedriver, der ikke taler noget, hvilket tillader NVDA at forblive helt stille til enhver tid. Dette kan senere bruges sammen med punktskrifttilstand, når vi har det.
* Tilføjet "capitalPitchChange"-indstilling for talesynteser, takket være J.J. Meddaugh.
* Tilføjet patch fra J.J. Meddaugh, der gør "tænd/sluk rapporter objekter under musen"-scriptet mere som de andre tænd/sluk-scripts (der siger til/fra i stedet for at ændre hele udsagnet).
* Tilføjet spansk oversættelse (es) bidraget af Juan C. Buno.
* Tilføjet ungarsk sprogfil fra Tamas Gczy.
* Tilføjet portugisisk sprogfil fra Rui Batista.
* Når man ændrer stemmen i Stemmens indstillinger dialogboksen, indstilles hastigheds-, tonehøjde- og volumen-sliders til de nye værdier i henhold til talesyntesen, i stedet for at tvinge talesyntesen til at blive indstillet til de gamle værdier. Dette løser problemer, hvor en talesyntese som Eloquence eller Viavoice taler meget hurtigere end alle andre talesynteser.
* Rettet en fejl, hvor enten tale stoppede, eller NVDA gik helt ned, når det var i et DOS-konsolvindue.
* Hvis understøttelse for et bestemt sprog findes, kan NVDA nu automatisk vise sin brugergrænseflade og tale sine beskeder på det sprog, Windows er indstillet til. Et bestemt sprog kan stadig vælges manuelt fra dialogboksen for brugergrænsefladeindstillinger.
* Tilføjet scriptet 'toggleReportDynamicContentChanges' (insert+5). Dette skifter, om nye tekster eller andre dynamiske ændringer skal annonceres automatisk. Indtil videre fungerer dette kun i DOS-konsolvinduer.
* Tilføjet scriptet 'toggleCaretMovesReviewCursor' (insert+6). Dette skifter, om gennemgangsmarkøren automatisk skal genplaceres, når systemets markør flytter sig. Dette er nyttigt i DOS-konsolvinduer, når du forsøger at læse information, mens skærmen opdateres.
* Tilføjet scriptet 'toggleFocusMovesNavigatorObject' (insert+7). Dette skifter, om navigatorobjektet automatisk skal genplaceres på objektet med fokus, når dette ændres.
* Tilføjet dokumentation oversat til forskellige sprog. Indtil videre er der fransk, spansk og finsk.
* Fjernet noget udviklerdokumentation fra NVDA's binære distribution, det er nu kun i kildeversionen.
* Rettet mulig fejl i Windows Live Messenger og MSN Messenger, hvor navigation med pil op/ned i kontaktlisten forårsagede fejl.
* Nye beskeder læses nu automatisk, når der føres en samtale i Windows Live Messenger. (fungerer kun for engelske versioner indtil videre).
* Historievinduet i en Windows Live Messenger-samtale kan nu læses med piletasterne. (fungerer kun for engelske versioner indtil videre).
* Tilføjet scriptet 'passNextKeyThrough' (insert+f2). Tryk på denne tast, og næste tastetryk sendes direkte til Windows. Dette er nyttigt, hvis du skal trykke på en bestemt tast i en applikation, men NVDA bruger denne tast til noget andet.
* NVDA fryser ikke længere i mere end et minut ved åbning af meget store dokumenter i MS Word.
* Rettet fejl, hvor det at bevæge sig ud af en tabel i MS Word og derefter ind igen, forårsagede, at de aktuelle række-/kolonnenumre ikke blev talt, hvis du flyttede ind i præcis den samme celle.
* Når NVDA startes med en talesyntese, der ikke eksisterer eller ikke virker, vil SAPI5-talesyntesen forsøge at blive indlæst i stedet, eller hvis SAPI5 ikke virker, indstilles tale til Silence.
* Skripterne til at øge og formindske hastighed kan ikke længere tage hastigheden over 100 eller under 0.
* Hvis der er en fejl med et sprog, når det vælges i dialogboksen for brugergrænsefladeindstillinger, vises en fejlmeddelelse, der advarer brugeren om fejlen.
* NVDA beder nu om at gemme konfiguration og genstarte, hvis brugeren lige har ændret sproget i dialogboksen for brugergrænsefladeindstillinger. NVDA skal genstartes, for at sprogændringen træder i kraft.
* Hvis en talesyntese ikke kan indlæses, når den vælges fra talesyntesedialogboksen, vises en fejlmeddelelse, der advarer brugeren om fejlen.
* Når en talesyntese indlæses for første gang, tillader NVDA talesyntesen at vælge de mest egnede stemme-, hastigheds- og tonehøjdsparametre i stedet for at tvinge talesyntesen til at bruge forudindstillede værdier. Dette retter et problem, hvor Eloquence- og Viavoice SAPI4-talesynteser starter med at tale alt for hurtigt første gang.
