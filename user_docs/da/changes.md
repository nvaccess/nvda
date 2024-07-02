# Nyheder i NVDA


## 2024.2

Der er en ny funktion kaldet lydopdeling.
Funktionen gør det muligt at have NVDA-lyde i én kanal (f.eks. venstre), mens lyde fra alle andre programmer udsendes i den anden kanal (f.eks. højre).

Der er nye kommandoer til ændring af ringen af talesynteseindstillinge, hvilket giver brugerne mulighed for at springe til den første eller sidste indstilling, og for at øge eller mindske den aktuelle indstilling med større trin.
Der er også nye hurtignavigationskommandoer, der gør det muligt for brugere at tilknytte tastetryk til hurtigt at hoppe mellem: afsnit, lodret justeret afsnit, tekst med samme typografi, tekst med en anderledes typografi, menuemne, skifteknap, behandlingslinje, figur og matematisk formel.

Der er mange nye punktskriftsfunktioner og fejlrettelser.
En ny punktskrifttilstand kaldet "vis taleoutput" er blevet tilføjet.
Når den er aktiv, viser punktdisplayet, hvad NVDA siger.
Der er også tilføjet understøttelse for punktdisplays BrailleEdgeS2, BrailleEdgeS3.
LibLouis blev opdateret, og tilføjede nye detaljerede (med store bogstaver angivet) hviderussiske og ukrainske punktskriftstabeller, en punkttabel for Lao, og en spansk tabel til læsning af græske tekster.

eSpeak blev opdateret med tilføjelsen af det nye sprog Tigrinya.

Der er mange mindre fejlrettelser for programmer, såsom Thunderbird, Adobe Reader, webbrowsere, Nudi og Geekbench.

### Nye Funktioner

* Nye tastaturkommandoer:
  * Ny hurtignavigationskommando `p` til at hoppe til næste/forrige tekstafsnit i gennemsynstilstand. (#15998, @mltony)
  * Nye ikke-tildelte hurtignavigationskommandoer, som kan bruges til at hoppe til næste/forrige:
    * figur (#10826)
    * lodret justeret afsnit (#15999, @mltony)
    * menupunkt (#16001, @mltony)
    * skifteknap (#16001, @mltony)
    * behandlingslinje (#16001, @mltony)
    * matematisk formel (#16001, @mltony)
    * tekst med samme typografi (#16000, @mltony)
    * tekst med en anden typografi (#16000, @mltony)
  * Tilføjede kommandoer til at springe til første, sidste, frem og tilbage gennem indstillingsværdier i ringen for talesynteseindstillinger. (#13768, #16095, @rmcpantoja)
    * Skift til første og sidste værdi for den aktuelle indstilling i ringen af talesynteseindstillinger. Denne har ingen tildelt kommando. (#13768)
    * Formindske og forøge den aktuelle indstilling i ringen af talesynteseindstillinger med i større trin (#13768):
      * Desktop: `NVDA+Ctrl+sideOp` eller `NVDA+Ctrl+sideNed`.
      * Laptop: `NVDA+Ctrl+shift+sideOp` eller `NVDA+Ctrl+Shift+sideNed`.
  * Tilføjet en ny ikke-tildelt kommando til at skifte rapportering af figurer og billedtekster. (#10826, #14349)
* Punktskrift:
  * Tilføjet support for BrailleEdgeS2, BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * En ny punktskrifttilstand kaldet "vis taleoutput" er blevet tilføjet. (#15898, @Emil-18)
    * Når aktiv, viser dit punktdisplay, hvad NVDA siger.
    * Kan aktiveres ved at trykke `NVDA+alt+t`, eller fra punktskriftsindstillingsdialogen.
* Lydopdeling: (#12985, @mltony)
  * Gør det muligt at dele NVDA-lyde i én kanal (f.eks. venstre) mens lyde fra alle andre programmer udsendes i den anden kanal (f.eks. højre).
  * Aktiveres med `NVDA+alt+s`.
* Rapportering af række- og kolonneoverskrifter understøttes nu i redigerbare HTML-elementer med indhold. (#14113)
* Tilføjet muligheden for at deaktivere rapportering af figurer og billedtekster i indstillinger for dokumentformatering. (#10826, #14349)
* I Windows 11 vil NVDA annoncere meddelelser fra stemmeindtastning og foreslåede handlinger, herunder det øverste forslag, når data som telefonnumre kopieres til udklipsholderen (Windows 11 2022-opdatering og senere). (#16009, @josephsl)
* NVDA kan holde lydenheden i gang efter at tale er stoppet, for at forhindre at starten af næste tale bliver afbrudt med nogle lydenheder som Bluetooth-hovedtelefoner. (#14386, @jcsteh, @mltony)
* HP Secure Browser er nu understøttet. (#16377)

### Ændringer

* Tilføjelsescenter:
  * Den mindste og den sidst testet NVDA-version for en tilføjelse vises nu i området "andre detaljer". (#15776, @Nael-Sayegh)
  * Handlingen for fællesskabets anmeldelser vil være tilgængelig, og anmeldelseswebstedet vil blive vist i detaljepanelet, i alle faner i centeret. (#16179, @nvdaes)
* Komponentopdateringer:
  * Opdateret LibLouis punktskriftsoversætter til [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Tilføjet nye detaljerede (med store bogstaver angivet) hviderussiske og ukrainske punktskriftstabeller.
    * Ny spansk tabel til læsning af græske tekster.
    * Ny tabel for Lao Niveau 1. (#16470)
  * eSpeak NG er blevet opdateret til 1.52-dev commit `cb62d93fd7`. (#15913)
    * Tilføjet nyt sprog Tigrinya.
* Ændret flere kommandoer for BrailleSense-enheder for at undgå konflikter med tegn fra den franske punktskriftstabel. (#15306)
  * `alt+venstre pil` er nu tildelt `punkt2+punkt7+mellemrum`.
  * `alt+højre pil` er nu tildelt `punkt5+punkt7+mellemrum`
  * `alt+pil op` er nu tildelt `punkt2+punkt3+punkt7+mellemrum`
  * `alt+pil ned` er nu tildelt `punkt5+punkt6+punkt7+mellemrum`
* Prikker, der almindeligvis bruges i indholdsfortegnelser, rapporteres ikke længere på lave tegnsætningsniveauer. (#15845, @CyrilleB79)

### Fejlrettelser

* Windows 11-rettelser:
  * NVDA vil igen oplyse forslag til hardwaretastaturindtastning. (#16283, @josephsl)
  * I version 24H2 (2024-opdatering og Windows Server 2025) kan mus og berøringsinteraktion bruges i hurtige indstillinger. (#16348, @josephsl)
* Tilføjelsescenter:
  * Når der trykkes på `ctrl+tab`, flyttes fokus korrekt til den nye aktuelle faneoverskrift. (#14986, @ABuffEr)
  * Hvis filer i NVDAs cache ikke er korrekte, vil NVDA ikke længere konstant genstarte. (#16362, @nvdaes)
* Rettelser for Chromium-baserede browsere, når de bruges med UIA:
  * Rettet fejl, der forårsagede, at NVDA sad fast. (#16393, #16394)
  * Backspace-tasten virker nu korrekt i Gmail log-ind felter. (#16395)
* Backspace virker nu korrekt, når Nudi 6.1 bruges med NVDA's indstilling "Håndtér tastetryk fra andre programmer" aktiveret. (#15822, @jcsteh)
* Rettet en fejl, hvor lydkoordinater ville blive afspillet, mens applikationen er i dvaletilstand, når "Afspil lydkoordinater, når musen bevæger sig" er aktiveret. (#8059, @hwf1324)
* I Adobe Reader ignorerer NVDA ikke længere alternativ tekst , der benyttes i formularer i PDF'er. (#12715)
* Rettet en fejl, der forårsagede, at NVDA ikke kunne læse båndet og indstillingerne i Geekbench. (#16251, @mzanm)
* Rettede et sjældent tilfælde, hvor gemning af konfigurationen kunne fejle, når NVDA gemmer alle profiler. (#16343, @CyrilleB79)
* I Firefox og Chromium-baserede browsere vil NVDA korrekt gå ind i fokus-tilstand, når der trykkes enter, når man er placeret i en punktopstilling (med tal og punkttegn) i redigerbart indhold. (#16325)
* Kolonnetilstandsændring rapporteres automatisk, når kolonner vælges til visning i Thunderbirds meddelelsesliste. (#16323)
* Kommandolinjeparametre `-h`/`--help` virker nu igen. (#16522, @XLTechie)
* NVDAs understøttelse for PoEdit version 3.4 eller nyere fungerer nu igen korrekt, hvis du oversætter til et sprog med én eller flere flertalsformer (F.eks. Kinesisk eller Polsk). (#16318)

### Ændringer for udviklere

For nyheder relateret til udvikling se venligst det engelske "What's New"-dokument.

## Tidligere versioner

For nyheder i ældre versioner se venligst det engelske "What's New"-dokument.

