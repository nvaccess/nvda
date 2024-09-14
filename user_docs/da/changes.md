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

For nyheder relateret til udvikling se venligst det engelske "What's New"-dokument.

## Tidligere versioner

For nyheder i ældre versioner se venligst det engelske "What's New"-dokument.

