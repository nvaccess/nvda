# Wat is Nieuw in NVDA

## 2024.4

Deze release bevat een aantal verbeteringen in Microsoft Office, braille en documentopmaak.

In Word of Excel is het nu mogelijk om twee keer de invoerhandeling voor commentaar in te drukken om het commentaar of de notitie te lezen in een bladermodusvenster.
Je kunt nu de opdracht voor leescursorselectie gebruiken om tekst te selecteren in PowerPoint.
NVDA geeft ook niet langer onzintekens weer in braille bij het weergeven van rij- of kolomkopteksten in tabellen in Word bij gebruik van het objectmodel.

NVDA kan nu geconfigureerd worden om lettertype-eigenschappen in spraak en braille afzonderlijk te melden.

Er is een nieuwe instelling toegevoegd om de time-out te configureren voor het uitvoeren van een meervoudige invoerhandeling, zoals de opdracht tijd/datum melden.

Je kunt nu instellen hoe NVDA tekstopmaak in braille weergeeft, en instellen dat NVDA het begin van alinea's in braille weergeeft.
NVDA kan nu het teken bij de cursor uitspreken wanneer je een braillecursorroutering uitvoert.
De betrouwbaarheid van de cursorroutering is verbeterd en er is ondersteuning toegevoegd voor routingtoetsen in PowerPoint.
Alle regels met cellen worden nu gebruikt bij gebruik van een meerregelige brailleleesregel via HID braille.
NVDA is niet langer instabiel na het herstarten van NVDA tijdens een automatische Braille Bluetooth scan.

De minimaal vereiste versie van Poedit die werkt met NVDA is nu versie 3.5.

eSpeak NG is bijgewerkt met ondersteuning voor de talen Faeröers en Xextan.

LibLouis is bijgewerkt en heeft nieuwe brailletabellen toegevoegd voor Thais en Grieks internationaal braille met eencellige accenten.

Er zijn ook een aantal fixes, onder andere voor muistracking in Firefox en de spraakmodus op aanvraag.

### Nieuwe functies

* Nieuwe braillefuncties:
  * Het is nu mogelijk om de manier waarop NVDA bepaalde tekstopmaakattributen weergeeft in braille te wijzigen.
    De beschikbare opties zijn:
    * Liblouis (standaard): Gebruikt opmaakmarkeringen gedefinieerd in de geselecteerde brailletabel.
    * Tags: Gebruikt begin- en eindtags om aan te geven waar bepaalde lettertypeattributen beginnen en eindigen. (#16864)
  * Wanneer de optie “Lezen per alinea” is ingeschakeld, kan NVDA nu worden geconfigureerd om het begin van alinea's in braille aan te geven. (#16895, @nvdaes)
  * Bij het uitvoeren van een braillecursorroutering kan NVDA nu automatisch het teken bij de cursor uitspreken. (#8072, @LeonarddeR)
    * Deze optie is standaard uitgeschakeld.
      Je kunt “Teken uitspreken wanneer cursor in tekst wordt verplaatst” inschakelen in de braille-instellingen van NVDA.
* De opdracht Opmerking in Microsoft Word en de opdracht Aantekeningen in Microsoft Excel kunnen nu twee keer worden ingedrukt om de opmerking of notitie weer te geven in een bladermodusbericht. (#16800, #16878, @Cary-Rowen)
* NVDA kan nu worden geconfigureerd om lettertype-eigenschappen in spraak en braille afzonderlijk te melden. (#16755)
* De time-out voor het uitvoeren van een meervoudige toetsaanslag is nu instelbaar; dit kan vooral handig zijn voor mensen met handvaardigheidsproblemen. (#11929, @CyrilleB79)

### Veranderingen

* De `-c`/`--config-path` en `--disable-addons` commandoregelopties worden nu gerespecteerd bij het starten van een update vanuit NVDA. (#16937)
* Updates van onderdelen:
  * LibLouis Braille vertaler bijgewerkt naar [3.31.0](https://github.com/liblouis/liblouis/releases/tag/v3.31.0). (#17080, @LeonarddeR, @codeofdusk)
    * Vertaling van getallen in Spaanse braille hersteld.
    * Nieuwe brailletabellen:
      * Thais graad 1
      * Grieks internationaal braille (eencellige letters met accenten)
    * Hernoemde tabellen:
      * “Thais 6 punt” werd hernoemd naar ‘Thais graad 0’ vanwege consistentie.
      * De bestaande tabel “Grieks internationaal braille” werd hernoemd naar “Grieks internationaal braille (2-cellige accentletters)” om het onderscheid tussen de twee Griekse systemen te verduidelijken.
  * eSpeak NG is bijgewerkt naar 1.52-dev commit `961454ff`. (#16775)
    * Nieuwe talen Faeröers en Xextan toegevoegd.
* Bij gebruik van een meerregelige brailleleesregel via het standaard HID brailleleesregelstuurprogramma worden alle cellijnen gebruikt. (#16993, @alexmoon)
* De stabiliteit van NVDA's Poedit ondersteuning is verbeterd met als neveneffect dat de minimaal vereiste versie van Poedit nu versie 3.5 is. (#16889, @LeonarddeR)

### Opgeloste problemen

* Braille oplossingen:
  * Het is nu mogelijk om routingtoetsen van brailleleesregels te gebruiken om de tekstcursor in Microsoft PowerPoint te verplaatsen. (#9101)
  * Bij het openen van Microsoft Word zonder UI Automation voert NVDA niet langer ongeldige tekens uit in tabelkoppen die zijn gedefinieerd met de opdrachten voor rij- en kolomkoppen instellen. (#7212)
  * Het Seika Notetaker-stuurprogramma genereert nu correct braille-invoer voor spatie, backspace en punten met spatie/backspace-bewegingen. (#16642, @school510587)
  * Cursorroutering is nu veel betrouwbaarder wanneer een regel een of meer Unicode-variatieselectors of gedecomponeerde tekens bevat. (#10960, @mltony, @LeonarddeR)
  * NVDA geeft niet langer een foutmelding wanneer de brailleleesregel naar voren wordt geschoven in sommige lege bewerkingselementen. (#12885)
  * NVDA is niet langer instabiel na het herstarten van NVDA tijdens een automatische Braille Bluetooth scan. (#16933)
* Het is nu mogelijk om de opdrachten voor leescursorselectie te gebruiken om tekst te selecteren in Microsoft PowerPoint. (#17004)
* In spraakmodus op aanvraag spreekt NVDA niet meer wanneer een bericht wordt geopend in Outlook, wanneer een nieuwe pagina wordt geladen in een browser of wanneer een nieuwe dia wordt weergegeven in een PowerPoint-diavoorstelling. (#16825, @CyrilleB79)
* In Mozilla Firefox geeft het bewegen van de muis over tekst voor of na een koppeling nu betrouwbaar de tekst weer. (#15990, @jcsteh)
* NVDA slaagt er niet langer af en toe niet in om berichten in de bladermodus te openen (zoals twee keer op `NVDA+f` drukken). (#16806, @LeonarddeR)
* Het bijwerken van NVDA terwijl add-on-updates in behandeling zijn, resulteert niet langer in het verwijderen van de add-on. (#16837)
* Het is nu mogelijk om te werken met vervolgkeuzelijsten voor gegevensvalidatie in Microsoft Excel 365. (#15138)
* NVDA is niet meer zo traag bij het omhoog en omlaag pijlen door grote bestanden in VS Code. (#17039)
* NVDA reageert niet langer niet als je een pijltjestoets lang ingedrukt houdt in de bladermodus, met name in Microsoft Word en Microsoft Outlook. (#16812)
* NVDA leest niet langer de laatste regel wanneer de cursor op de een-na-laatste regel staat van een multiline edit control in Java-toepassingen. (#17027)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Component updates:
  * Updated py2exe to 0.13.0.2 (#16907, @dpy013)
  * Updated setuptools to 72.0 (#16907, @dpy013)
  * Updated Ruff to 0.5.6. (#16868, @LeonarddeR)
  * Updated nh3 to 0.2.18 (#17020, @dpy013)
* Added a `.editorconfig` file to NVDA's repository in order for several IDEs to pick up basic NVDA code style rules by default. (#16795, @LeonarddeR)
* Added support for custom speech symbol dictionaries. (#16739, #16823, @LeonarddeR)
  * Dictionaries can be provided in locale specific folders in an add-on package, e.g. `locale\en`.
  * Dictionary metadata can be added to an optional `symbolDictionaries` section in the add-on manifest.
  * Please consult the [Custom speech symbol dictionaries section in the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSymbolDictionaries) for more details.
* It is now possible to redirect objects retrieved from on-screen coordinates, by using the `NVDAObject.objectFromPointRedirect` method. (#16788, @Emil-18)
* Running SCons with the parameter `--all-cores` will automatically pick the maximum number of available CPU cores. (#16943, #16868, @LeonarddeR)
* Developer info now includes information on app architecture (such as AMD64) for the navigator object. (#16488, @josephsl)

#### Deprecations

* The `bool` configuration key `[documentFormatting][reportFontAttributes]` is deprecated for removal in 2025.1, instead use `[fontAttributeReporting]`. (#16748)
  * The new key has an `int` value matching an `OutputMode` `enum` with options for speech, braille, speech and braille and off.
  * API consumers can use the `bool` value as previously, or check the `OutputMode` if handling speech or braille specifically.
  * These keys are currently synchronized until 2025.1.
* `NVDAObjects.UIA.InaccurateTextChangeEventEmittingEditableText` is deprecated with no replacement. (#16817, @LeonarddeR)

## 2024.3.1

Dit is een patchrelease om een bug te verhelpen in de automatische add-on-updatemelding.

### Opgeloste problemen

* Bij het automatisch controleren op add-on-updates loopt NVDA niet langer vast bij slechte verbindingen. (#17036)

## 2024.3

De Add-on Store zal je nu op de hoogte stellen als er add-on updates beschikbaar zijn bij het opstarten van NVDA.

Er zijn nu opties om Unicode-normalisatie toe te passen op spraak- en braille-uitvoer.
Dit kan handig zijn bij het lezen van tekens die onbekend zijn voor een bepaalde spraaksynthesizer of brailletabel, en die een compatibel alternatief hebben, zoals de vetgedrukte en cursieve tekens die vaak worden gebruikt op sociale media.
Het maakt ook het lezen van vergelijkingen in de Microsoft Word-vergelijkingseditor mogelijk.

Help Tech Activator Pro-brailleleesregels worden nu ondersteund.

Niet toegewezen opdrachten zijn toegevoegd om het muiswiel verticaal en horizontaal te scrollen.

Er zijn verschillende bugfixes, met name voor het Windows 11 Emoji-paneel en de klembordgeschiedenis.
Voor webbrowsers zijn er oplossingen voor het melden van fouten, afbeeldingen, bijschriften, tabellabels en menu-items van selectievakjes/radioknoppen.

LibLouis is bijgewerkt en voegt nieuwe brailletabellen toe voor Cyrillisch Servisch, Jiddisch, verschillende oude talen, Turks en het Internationaal Fonetisch Alfabet.
eSpeak is bijgewerkt met ondersteuning voor de Karakalpaks taal.
Unicode CLDR is ook bijgewerkt.

### Nieuwe functies

* Nieuwe toetsopdrachten:
  * Niet toegewezen opdrachten toegevoegd voor verticale en horizontale scroll van het muiswiel, om de navigatie op webpagina's en apps met dynamische inhoud, zoals Dism++, te verbeteren. (#16462, @Cary-Rowen)
* Ondersteuning toegevoegd voor Unicode-normalisatie in spraak- en braille-uitvoer. (#11570, #16466 @LeonarddeR).
  * Dit kan handig zijn bij het lezen van tekens die onbekend zijn voor een bepaalde spraaksynthesizer of brailletabel en die een compatibel alternatief hebben, zoals de vetgedrukte en cursieve tekens die vaak op sociale media worden gebruikt.
  * Het maakt ook het lezen van vergelijkingen in de Microsoft Word-vergelijkingseditor mogelijk. (#4631)
  * Je kunt deze functionaliteit inschakelen voor zowel spraak als braille in hun respectieve categorieën in het NVDA-instellingenmenu.
* Standaard ontvang je na het opstarten van NVDA een melding als er add-on updates beschikbaar zijn. (#15035)
  * Dit kan worden uitgeschakeld in de categorie "Add-on Store" in de instellingen.
  * NVDA controleert dagelijks op add-on updates.
  * Alleen updates binnen hetzelfde kanaal worden gecontroleerd (bijv. geïnstalleerde bèta-add-ons melden alleen updates in het bèta-kanaal).
* Ondersteuning toegevoegd voor Help Tech Activator Pro-leesregels. (#16668)

### Veranderingen

* Componentupdates:
  * eSpeak NG is bijgewerkt naar 1.52-dev commit `54ee11a79`. (#16495)
    * Nieuwe taal toegevoegd: Karakalpaks.
  * Unicode CLDR bijgewerkt naar versie 45.0. (#16507, @OzancanKaratas)
  * Fast_diff_match_patch (gebruikt om wijzigingen in terminals en andere dynamische inhoud te detecteren) bijgewerkt naar versie 2.1.0. (#16508, @codeofdusk)
  * LibLouis-braillevertaler bijgewerkt naar [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0). (#16652, @codeofdusk)
    * Nieuwe brailletabellen:
      * Cyrillisch Servisch.
      * Jiddisch.
      * Verschillende oude talen: Bijbels Hebreeuws, Akkadisch, Syrisch, Ugaritisch en getranslitereerde spijkerschriftteksten.
      * Turks graad 2. (#16735)
      * Internationaal Fonetisch Alfabet. (#16773)
  * NSIS bijgewerkt naar 3.10 (#16674, @dpy013)
  * Markdown bijgewerkt naar 3.6 (#16725, @dpy013)
  * NH3 bijgewerkt naar 0.2.17 (#16725, @dpy013)
* De standaard braille-invoertabel is nu gelijk aan de standaard uitvoertabel, namelijk Unified English Braille Code graad 1. (#9863, @JulienCochuyt, @LeonarddeR)
* NVDA zal nu afbeeldingen rapporteren zonder toegankelijke kinderen, maar met een label of beschrijving. (#14514)
* Bij het lezen per regel in de bladermodus wordt "bijschrift" niet langer bij elke regel van een lange afbeelding of tabelbijschrift gemeld. (#14874)
* In de Python-console gaat het laatste niet-uitgevoerde commando niet meer verloren bij het navigeren in de invoergeschiedenis. (#16653, @CyrilleB79)
* Een unieke anonieme ID wordt nu verzonden als onderdeel van de optionele NVDA-gebruikersstatistieken. (#16266)
* Standaard wordt een nieuwe map gemaakt bij het maken van een draagbare kopie.
Een waarschuwingsbericht informeert je als je probeert naar een niet-lege map te schrijven. (#16686)

### Opgeloste problemen

* Windows 11-oplossingen:
  * NVDA lijkt niet langer vast te lopen bij het sluiten van de geschiedenis van het klembord en het emoji-paneel. (#16346, #16347, @josephsl)
  * NVDA zal opnieuw zichtbare kandidaten aankondigen bij het openen van de IME-interface. (#14023, @josephsl)
  * NVDA kondigt niet langer tweemaal "klembordgeschiedenis" aan bij het navigeren door de emoji-paneelmenu-items. (#16532, @josephsl)
  * NVDA onderbreekt spraak en braille niet meer bij het bekijken van kaomojis en symbolen in het emoji-paneel. (#16533, @josephsl)
* Oplossingen voor webbrowsers:
  * Foutmeldingen die worden verwezen met `aria-errormessage` worden nu gerapporteerd in Google Chrome en Mozilla Firefox. (#8318)
  * Indien aanwezig, gebruikt NVDA nu `aria-labelledby` om toegankelijke namen voor tabellen te geven in Mozilla Firefox. (#5183)
  * NVDA kondigt correct radio- en selectievakjesmenu-items aan wanneer je voor het eerst submenu's betreedt in Google Chrome en Mozilla Firefox. (#14550)
  * NVDA's zoekfunctionaliteit in de bladermodus is nu nauwkeuriger wanneer de pagina emoji's bevat. (#16317, @LeonarddeR)
  * In Mozilla Firefox rapporteert NVDA nu correct het huidige teken, woord en regel wanneer de cursor zich op het invoegpunt aan het einde van een regel bevindt. (#3156, @jcsteh)
  * Zorgt er niet langer voor dat Google Chrome crasht bij het sluiten van een document of afsluiten van Chrome. (#16893)
* NVDA kondigt correct de autosuggesties aan in Eclipse en andere Eclipse-gebaseerde omgevingen op Windows 11. (#16416, @thgcode)
* Verbeterde betrouwbaarheid van automatische tekstuitvoer, met name in terminaltoepassingen. (#15850, #16027, @Danstiv)
* Het is opnieuw mogelijk om de configuratie betrouwbaar terug te zetten naar de fabrieksinstellingen. (#16755, @Emil-18)
* NVDA kondigt correct wijzigingen in de selectie aan bij het bewerken van de tekst in een cel in Microsoft Excel. (#15843)
* In toepassingen die gebruikmaken van Java Access Bridge leest NVDA nu correct de laatste lege regel van een tekst in plaats van de vorige regel te herhalen. (#9376, @dmitrii-drobotov)
* In LibreOffice Writer (versie 24.8 en nieuwer), wanneer tekstopmaak wordt omgeschakeld (vet, cursief, onderstrepen, subscript/superscript, uitlijning) met de bijbehorende sneltoets, kondigt NVDA het nieuwe opmaakattribuut aan (bijv. "Vet aan", "Vet uit"). (#4248, @michaelweghorn)
* Bij het navigeren met de pijltjestoetsen in tekstvakken in toepassingen die UI Automation gebruiken, meldt NVDA niet langer soms het verkeerde teken, woord, enz. (#16711, @jcsteh)
* Bij het plakken in de rekenmachine van Windows 10/11 rapporteert NVDA nu correct het volledige geplakte nummer. (#16573, @TristanBurchett)
* Spraak is niet langer stil na het loskoppelen en opnieuw verbinden met een Remote Desktop-sessie. (#16722, @jcsteh)
* Ondersteuning toegevoegd voor tekstrecensieopdrachten voor de naam van een object in Visual Studio Code. (#16248, @Cary-Rowen)
* Het afspelen van NVDA-geluiden mislukt niet langer op een mono-audioapparaat. (#16770, @jcsteh)
* NVDA meldt adressen bij het doorlopen van de velden Aan/CC/BCC in outlook.com / Moderne Outlook. (#16856)
* NVDA behandelt add-oninstallatiefouten nu op een elegantere manier.

### Veranderingen voor ontwikkelaars (niet vertaald)

* NVDA now uses Ruff instead of flake8 for linting. (#14817)
* Fixed NVDA's build system to work properly when using Visual Studio 2022 version 17.10 and above. (#16480, @LeonarddeR)
* A fixed width font is now used in Log Viewer and in the NVDA Python Console so that the cursor remains in the same column during vertical navigation.
It is especially useful to read the error location markers in tracebacks. (#16321, @CyrilleB79)
* Support for custom braille tables has been added. (#3304, #16208, @JulienCochuyt, @LeonarddeR)
  * Tables can be provided in the `brailleTables` folder in an add-on package.
  * Table metadata can be added to an optional `brailleTables` section in the add-on manifest or to a `.ini` file with the same format found in the brailleTables subdirectory of the scratchpad directory.
  * Please consult the [braille translation tables section in the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#BrailleTables) for more details.
* When a `gainFocus` event is queued with an object that has a valid `focusRedirect` property, the object pointed to by the `focusRedirect` property is now held by `eventHandler.lastQueuedFocusObject`, rather than the originally queued object. (#15843)
* NVDA will log its executable architecture (x86) at startup. (#16432, @josephsl)
* `wx.CallAfter`, which is wrapped in `monkeyPatches/wxMonkeyPatches.py`, now includes proper `functools.wraps` indication. (#16520, @XLTechie)
* There is a new module for scheduling tasks `utils.schedule`, using the pip module `schedule`. (#16636)
  * You can use `scheduleThread.scheduleDailyJobAtStartUp` to automatically schedule a job that happens after NVDA starts, and every 24 hours after that.
  Jobs are scheduled with a delay to avoid conflicts.
  * `scheduleThread.scheduleDailyJob` and `scheduleJob` can be used to schedule jobs at custom times, where a `JobClashError` will be raised on a known job scheduling clash.
* It is now possible to create app modules for apps hosting Edge WebView2 (msedgewebview2.exe) controls. (#16705, @josephsl)

## 2024.2

Er is een nieuwe functie genaamd "sound split".
Hiermee kunnen NVDA-geluiden naar één kanaal worden gestuurd (bijv. links), terwijl geluiden van alle andere applicaties naar het andere kanaal worden gestuurd (bijv. rechts).

Er zijn nieuwe commando's voor het aanpassen van de synth-instellingenring, waarmee gebruikers naar de eerste of laatste instelling kunnen springen, en de huidige instelling in grotere stappen kunnen verhogen of verlagen.
Er zijn ook nieuwe snelnavigatiecommando's, waarmee gebruikers gebaren kunnen toewijzen om snel te springen tussen: alinea, verticaal uitgelijnde alinea, tekst met dezelfde stijl, tekst met een andere stijl, menu-item, schakelknop, voortgangsbalk, afbeelding en wiskundige formule.

Er zijn veel nieuwe braille-functies en opgeloste problemen.
Een nieuwe braillemodus genaamd "weergave spraakuitvoer" is toegevoegd.
Wanneer actief, toont het braille-display precies wat NVDA zegt.
Er is ook ondersteuning toegevoegd voor de BrailleEdgeS2 en BrailleEdgeS3 displays.
LibLouis is bijgewerkt, met nieuwe gedetailleerde (met hoofdletters aangeduid) Wit-Russische en Oekraïense brailletabellen, een Laotiaanse tabel en een Spaanse tabel voor het lezen van Griekse teksten.

eSpeak is bijgewerkt, met ondersteuning voor de nieuwe taal Tigrinya.

Er zijn veel kleine bugfixes voor applicaties zoals Thunderbird, Adobe Reader, webbrowsers, Nudi en Geekbench.

### Nieuwe functies

* Nieuwe toetsencombinaties:
  * Nieuw snelnavigatiecommando `p` om te springen naar de volgende/vorige tekstalinea in browse-modus. (#15998, @mltony)
  * Nieuwe niet-toegewezen snelnavigatiecommando's, die kunnen worden gebruikt om te springen naar de volgende/vorige:
    * afbeelding (#10826)
    * verticaal uitgelijnde alinea (#15999, @mltony)
    * menu-item (#16001, @mltony)
    * schakelknop (#16001, @mltony)
    * voortgangsbalk (#16001, @mltony)
    * wiskundige formule (#16001, @mltony)
    * tekst met dezelfde stijl (#16000, @mltony)
    * tekst met een andere stijl (#16000, @mltony)
  * Toegevoegde commando's om te springen naar eerste, laatste, vooruit en achteruit in de synth-instellingenring. (#13768, #16095, @rmcpantoja)
    * Het instellen van de eerste/laatste instelling in de synth-instellingenring heeft geen toegewezen gebaar. (#13768)
    * Verlaag en verhoog de huidige instelling van de synth-instellingenring in grotere stappen (#13768):
      * Desktop: `NVDA+control+pageUp` en `NVDA+control+pageDown`.
      * Laptop: `NVDA+control+shift+pageUp` en `NVDA+control+shift+pageDown`.
  * Toegevoegd een nieuwe niet-toegewezen invoergebaar om de rapportage van afbeeldingen en bijschriften in/uit te schakelen. (#10826, #14349)
* Braille:
  * Ondersteuning toegevoegd voor de BrailleEdgeS2 en BrailleEdgeS3 displays. (#16033, #16279, @EdKweon)
  * Een nieuwe braillemodus genaamd "weergave spraakuitvoer" is toegevoegd. (#15898, @Emil-18)
    * Wanneer actief, toont het braille-display precies wat NVDA zegt.
    * Het kan worden in-/uitgeschakeld door `NVDA+alt+t` te drukken, of via het braille-instellingenvenster.
* Sound split: (#12985, @mltony)
  * Hiermee kunnen NVDA-geluiden naar één kanaal worden gestuurd (bijv. links), terwijl geluiden van alle andere applicaties naar het andere kanaal worden gestuurd (bijv. rechts).
  * In-/uitschakelen met `NVDA+alt+s`.
* Het rapporteren van rij- en kolomkoppen wordt nu ondersteund in contenteditable HTML-elementen. (#14113)
* Toegevoegd een optie om het rapporteren van afbeeldingen en bijschriften in Documentopmaakinstellingen uit te schakelen. (#10826, #14349)
* In Windows 11 zal NVDA meldingen aankondigen van stemtypen en voorgestelde acties, inclusief het bovenste voorstel wanneer gegevens zoals telefoonnummers naar het klembord worden gekopieerd (Windows 11 2022 Update en later). (#16009, @josephsl)
* NVDA houdt het audiokanaal actief nadat de spraak stopt, om te voorkomen dat het begin van de volgende spraak wordt afgekapt met sommige audiokanalen, zoals Bluetooth-koptelefoons. (#14386, @jcsteh, @mltony)
* HP Secure Browser wordt nu ondersteund. (#16377)

### Veranderingen

* Add-on Store:
  * De minimale en laatst geteste NVDA-versie voor een add-on worden nu weergegeven in het gebied "overige details". (#15776, @Nael-Sayegh)
  * De communitybeoordelingsactie zal beschikbaar zijn in alle tabbladen van de store. (#16179, @nvdaes)
* Componentupdates:
  * LibLouis braille-vertaler bijgewerkt naar [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Nieuwe gedetailleerde (met hoofdletters aangeduid) Wit-Russische en Oekraïense brailletabellen.
    * Nieuwe Spaanse tabel voor het lezen van Griekse teksten.
    * Nieuwe tabel voor Laotiaans graad 1. (#16470)
  * eSpeak NG bijgewerkt naar 1.52-dev commit `cb62d93fd7`. (#15913)
    * Nieuwe taal toegevoegd: Tigrinya.
* Meerdere gebaren voor BrailleSense-apparaten gewijzigd om conflicten met tekens van de Franse brailletabel te voorkomen. (#15306)
  * `alt+leftArrow` is nu toegewezen aan `dot2+dot7+space`
  * `alt+rightArrow` is nu toegewezen aan `dot5+dot7+space`
  * `alt+upArrow` is nu toegewezen aan `dot2+dot3+dot7+space`
  * `alt+downArrow` is nu toegewezen aan `dot5+dot6+dot7+space`
* Punten die vaak worden gebruikt in inhoudsopgaven worden niet langer gerapporteerd bij lage interpunctieniveaus. (#15845, @CyrilleB79)

### Opgeloste problemen

* Windows 11-oplossingen:
  * NVDA kondigt opnieuw suggesties voor hardwaretoetsenbordinvoer aan. (#16283, @josephsl)
  * In versie 24H2 (2024 Update en Windows Server 2025), kunnen muis- en aanraakinteractie worden gebruikt in snelle instellingen. (#16348, @josephsl)
* Add-on Store:
  * Bij het indrukken van `ctrl+tab`, verplaatst de focus correct naar de nieuwe huidige tabtitel. (#14986, @ABuffEr)
  * Als cachebestanden niet correct zijn, zal NVDA niet opnieuw opstarten. (#16362, @nvdaes)
* Oplossingen voor Chromium-gebaseerde browsers wanneer gebruikt met UIA:
  * Bugs verholpen die ervoor zorgden dat NVDA vastliep. (#16393, #16394)
  * Backspace-toets werkt nu correct in Gmail-inlogvelden. (#16395)
* Backspace werkt nu correct bij gebruik van Nudi 6.1 met NVDA's instelling "Handle keys from other applications" ingeschakeld. (#15822, @jcsteh)
* Een bug opgelost waarbij audiocoördinaten werden afgespeeld terwijl de applicatie in slaapstand stond wanneer "Speel audiocoördinaten af wanneer de muis beweegt" is ingeschakeld. (#8059, @hwf1324)
* In Adobe Reader negeert NVDA niet langer alternatieve tekst ingesteld op formules in PDF's. (#12715)
* Een bug verholpen die ervoor zorgde dat NVDA de ribbon en opties binnen Geekbench niet kon lezen. (#16251, @mzanm)
* Een zeldzaam geval opgelost waarbij het opslaan van de configuratie mogelijk niet alle profielen opsloeg. (#16343, @CyrilleB79)
* In Firefox en Chromium-gebaseerde browsers zal NVDA correct de focusmodus activeren wanneer op enter wordt gedrukt wanneer de cursor binnen een presentatie-lijst (ul / ol) in bewerkbare inhoud staat. (#16325)
* Kolomstatuswijzigingen worden nu correct gerapporteerd bij het selecteren van kolommen om weer te geven in de Thunderbird-berichtenlijst. (#16323)
* De commandoregeloptie `-h`/`--help` werkt weer correct. (#16522, @XLTechie)
* NVDA's ondersteuning voor de Poedit-vertaalsoftware versie 3.4 of hoger werkt correct bij het vertalen van talen met 1 of meer dan 2 meervoudsvormen (bijv. Chinees, Pools). (#16318)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Added a how-to document, explaining the process of building NVDA forks on AppVeyor. (#16293, @XLTechie)

## 2024.1

Een nieuwe "on-demand" spraakmodus is toegevoegd.
Wanneer spraak op aanvraag is, spreekt NVDA niet automatisch (bijvoorbeeld bij het verplaatsen van de cursor), maar spreekt het nog steeds wanneer er opdrachten worden aangeroepen waarvan het doel expliciet is om iets te melden (bijvoorbeeld venstertitel rapporteren).
In de categorie Spraak van de NVDA-instellingen is het nu mogelijk om ongewenste spraakmodi uit te sluiten van de Cyclus spraakmodi-opdracht (`NVDA+s`).

Een nieuwe Native Selectie-modus (geschakeld door `NVDA+shift+f10`) is nu beschikbaar in NVDA's browse-modus voor Mozilla Firefox.
Wanneer ingeschakeld, wordt het selecteren van tekst in de browse-modus ook gekoppeld aan Firefox' eigen native selectie.
Tekst kopiëren met `control+c` gaat rechtstreeks naar Firefox, waardoor de rijke inhoud wordt gekopieerd in plaats van NVDA's platte tekstweergave.

De Add-on Store ondersteunt nu bulkacties (bijv. installeren, inschakelen van add-ons) door meerdere add-ons te selecteren
Er is een nieuwe actie toegevoegd om een recensiepagina voor de geselecteerde add-on te openen.

De opties voor het audio-uitvoerapparaat en ducking-modus zijn verwijderd uit het dialoogvenster "Selecteer synthesizer".
Deze opties zijn te vinden in het audio-instellingenpaneel dat kan worden geopend met `NVDA+control+u`.

eSpeak-NG, LibLouis braillevertaler en Unicode CLDR zijn bijgewerkt.
Nieuwe Thaise, Filippijnse en Roemeense brailletabellen zijn beschikbaar.

Er zijn veel bugfixes, vooral voor de Add-on Store, braille, Libre Office, Microsoft Office en audio.

### Belangrijke opmerkingen

* Deze release verbreekt de compatibiliteit met bestaande add-ons.
* Windows 7 en Windows 8 worden niet langer ondersteund.
Windows 8.1 is de minimaal ondersteunde Windows-versie.

### Nieuwe functies

* Add-on Store:
  * De Add-on Store ondersteunt nu bulkacties (bijv. installeren, inschakelen van add-ons) door meerdere add-ons te selecteren. (#15350, #15623, @CyrilleB79)
  * Een nieuwe actie is toegevoegd om een speciale webpagina te openen voor feedback over de geselecteerde add-on. (#15576, @nvdaes)
* Ondersteuning toegevoegd voor Bluetooth Low Energy HID Braille-displays. (#15470)
* Een nieuwe Native Selectie-modus (geschakeld door `NVDA+shift+f10`) is nu beschikbaar in NVDA's browse-modus voor Mozilla Firefox.
Wanneer ingeschakeld, wordt het selecteren van tekst in de browse-modus ook gekoppeld aan Firefox' eigen native selectie.
Tekst kopiëren met `control+c` gaat rechtstreeks naar Firefox, waardoor de rijke inhoud wordt gekopieerd in plaats van NVDA's platte tekstweergave.
Let er echter op dat aangezien Firefox de daadwerkelijke kopie beheert, NVDA geen "kopiëren naar klembord"-melding zal rapporteren in deze modus. (#15830)
* Bij het kopiëren van tekst in Microsoft Word met NVDA's browse-modus ingeschakeld, wordt nu ook opmaak meegenomen.
Een neveneffect hiervan is dat NVDA geen "kopiëren naar klembord"-melding meer zal rapporteren bij het indrukken van `control+c` in Microsoft Word/Outlook-browse-modus, omdat de applicatie nu het kopiëren beheert, niet NVDA. (#16129)
* Een nieuwe "on-demand" spraakmodus is toegevoegd.
Wanneer spraak op aanvraag is, spreekt NVDA niet automatisch (bijv. bij het verplaatsen van de cursor), maar spreekt het nog steeds wanneer er opdrachten worden aangeroepen waarvan het doel expliciet is om iets te melden (bijv. venstertitel rapporteren). (#481, @CyrilleB79)
* In de categorie Spraak van de NVDA-instellingen is het nu mogelijk om ongewenste spraakmodi uit te sluiten van de Cyclus spraakmodi-opdracht (`NVDA+s`). (#15806, @lukaszgo1)
  * Als je momenteel de NoBeepsSpeechMode add-on gebruikt, overweeg deze te verwijderen en de "piepjes" en "op aanvraag" modi uit te schakelen in de instellingen.

### Veranderingen

* NVDA ondersteunt niet langer Windows 7 en Windows 8.
Windows 8.1 is de minimaal ondersteunde Windows-versie. (#15544)
* Componentupdates:
  * LibLouis braillevertaler bijgewerkt naar [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Nieuwe Thaise, Roemeense en Filippijnse brailletabellen toegevoegd.
  * eSpeak NG bijgewerkt naar 1.52-dev commit `530bf0abf`. (#15036)
  * CLDR emoji en symbool annotaties bijgewerkt naar versie 44.0. (#15712, @OzancanKaratas)
  * Java Access Bridge bijgewerkt naar 17.0.9+8Zulu (17.46.19). (#15744)
* Toetscombinaties:
  * De volgende opdrachten ondersteunen nu twee en drie keer drukken om de gemelde informatie te spellen en met karakterbeschrijvingen te spellen: selectie rapporteren, klembordtekst rapporteren en gefocust object rapporteren. (#15449, @CyrilleB79)
  * De opdracht om het schermgordijn in of uit te schakelen heeft nu een standaardgebaar: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * Bij vier keer drukken toont de opdracht selectie rapporteren nu de selectie in een doorbladerbaar bericht. (#15858, @Emil-18)
* Microsoft Office:
  * Bij het opvragen van opmaakinformatie over Excel-cellen worden randen en achtergrond alleen gerapporteerd als er dergelijke opmaak is. (#15560, @CyrilleB79)
  * NVDA rapporteert opnieuw geen ongenummerde groepen meer zoals in recente versies van Microsoft Office 365-menu's. (#15638)
* De opties voor het audio-uitvoerapparaat en ducking-modus zijn verwijderd uit het dialoogvenster "Selecteer synthesizer".
Deze opties zijn te vinden in het audio-instellingenpaneel dat kan worden geopend met `NVDA+control+u`. (#15512, @codeofdusk)
* De optie "Rol rapporteren wanneer muis object binnenkomt" in de muisinstellingen van NVDA is hernoemd naar "Object rapporteren wanneer muis het binnenkomt".
Deze optie meldt nu aanvullende relevante informatie over een object wanneer de muis het binnenkomt, zoals statussen (aangevinkt/ingedrukt) of celcoördinaten in een tabel. (#15420, @LeonarddeR)
* Nieuwe items zijn toegevoegd aan het Help-menu voor de NV Access "Get Help"-pagina en winkel. (#14631)
* NVDA's ondersteuning voor [Poedit](https://poedit.net) is herzien voor Poedit versie 3 en hoger.
Gebruikers van Poedit 1 worden aangemoedigd om bij te werken naar Poedit 3 als ze willen vertrouwen op verbeterde toegankelijkheid in Poedit, zoals sneltoetsen om vertalersnotities en opmerkingen te lezen. (#15313, #7303, @LeonarddeR)
* Braille viewer en spraakviewer zijn nu uitgeschakeld in beveiligde modus. (#15680)
* Tijdens objectnavigatie worden uitgeschakelde (niet-beschikbare) objecten niet meer genegeerd. (#15477, @CyrilleB79)
* Inhoudsopgave toegevoegd aan het document met toetscombinaties. (#16106)

### Opgeloste problemen

* Add-on Store:
  * Wanneer de status van een add-on verandert terwijl deze is gefocust, bijv. een wijziging van "downloaden" naar "gedownload", wordt het bijgewerkte item nu correct aangekondigd. (#15859, @LeonarddeR)
  * Wanneer add-ons worden geïnstalleerd, worden installatieprompten niet langer overlapt door het herstartdialoogvenster. (#15613, @lukaszgo1)
  * Wanneer een incompatibele add-on opnieuw wordt geïnstalleerd, wordt deze niet langer gedwongen uitgeschakeld. (#15584, @lukaszgo1)
  * Uitgeschakelde en incompatibele add-ons kunnen nu worden bijgewerkt. (#15568, #15029)
  * NVDA herstelt zich nu en toont een fout in het geval dat een add-on niet correct kan worden gedownload. (#15796)
  * NVDA start niet langer af en toe niet opnieuw op na het openen en sluiten van de Add-on Store. (#16019, @lukaszgo1)
* Audio:
  * NVDA bevriest niet langer kort wanneer meerdere geluiden snel achter elkaar worden afgespeeld. (#15311, #15757, @jcsteh)
  * Als het audio-uitvoerapparaat is ingesteld op iets anders dan het standaardapparaat en dat apparaat weer beschikbaar wordt nadat het niet beschikbaar was, schakelt NVDA nu terug naar het geconfigureerde apparaat in plaats van het standaardapparaat te blijven gebruiken. (#15759, @jcsteh)
  * NVDA hervat nu audio als de configuratie van het uitvoerapparaat verandert of wanneer een andere toepassing het exclusieve gebruik van het apparaat vrijgeeft. (#15758, #15775, @jcsteh)
* Braille:
  * Meerdere regels braille-displays zorgen niet langer voor een crash in de BRLTTY-driver en worden behandeld als één doorlopend display. (#15386)
  * Meer objecten die nuttige tekst bevatten, worden nu gedetecteerd en de tekstinhoud wordt weergegeven in braille. (#15605)
  * Gecontracteerde braille-invoer werkt weer correct. (#15773, @aaclause)
  * Braille wordt nu bijgewerkt wanneer het navigator-object tussen tabelcellen wordt verplaatst in meer situaties. (#15755, @Emil-18)
  * Het resultaat van het rapporteren van de huidige focus, het huidige navigator-object en de huidige selectie wordt nu weergegeven in braille. (#15844, @Emil-18)
  * De Albatross-brailledriver behandelt een Esp32-microcontroller niet langer als een Albatross-display. (#15671)
* LibreOffice:
  * Woorden die worden verwijderd met de toetsenbordcombinatie `control+backspace` worden nu correct aangekondigd wanneer het verwijderde woord wordt gevolgd door witruimte (zoals spaties en tabbladen). (#15436, @michaelweghorn)
  * Aankondiging van de statusbalk met de toetsenbordcombinatie `NVDA+end` werkt nu ook voor dialoogvensters in LibreOffice versie 24.2 en nieuwer. (#15591, @michaelweghorn)
  * Alle verwachte tekstattributen worden nu ondersteund in LibreOffice-versies 24.2 en hoger.
  Dit zorgt ervoor dat spelfouten worden aangekondigd wanneer een regel wordt aangekondigd in Writer. (#15648, @michaelweghorn)
  * Aankondiging van kopniveau's werkt nu ook in LibreOffice-versies 24.2 en nieuwer. (#15881, @michaelweghorn)
* Microsoft Office:
  * In Excel, met UIA uitgeschakeld, wordt braille bijgewerkt en wordt de inhoud van de actieve cel uitgesproken wanneer `control+y`, `control+z` of `alt+backspace` wordt ingedrukt. (#15547)
  * In Word, met UIA uitgeschakeld, wordt braille bijgewerkt wanneer `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace` of `control+backspace` wordt ingedrukt.
  Het wordt ook bijgewerkt met UIA ingeschakeld, wanneer tekst wordt getypt en braille is gekoppeld aan de review en de review de cursor volgt. (#3276)
  * In Word wordt de landingscel nu correct gerapporteerd bij het gebruik van de native Word-commando's voor tabelnavigatie `alt+home`, `alt+end`, `alt+pageUp` en `alt+pageDown`. (#15805, @CyrilleB79)
* Rapportage van sneltoetsen van objecten is verbeterd. (#10807, #15816, @CyrilleB79)
* De SAPI4-synthesizer ondersteunt nu correct volume-, snelheids- en toonhoogteveranderingen die in de spraak zijn ingebed. (#15271, @LeonarddeR)
* De meerregelige status wordt nu correct gerapporteerd in toepassingen die Java Access Bridge gebruiken. (#14609)
* NVDA zal nu de dialooginhoud aankondigen voor meer Windows 10- en 11-dialoogvensters. (#15729, @josephsl)
* NVDA zal niet langer falen bij het lezen van een pas geladen pagina in Microsoft Edge wanneer UI Automation wordt gebruikt. (#15736)
* Bij gebruik van "alles voorlezen" of opdrachten die tekst spellen, zullen pauzes tussen zinnen of tekens niet langer geleidelijk afnemen. (#15739, @jcsteh)
* NVDA bevriest niet langer soms bij het uitspreken van een grote hoeveelheid tekst. (#15752, @jcsteh)
* Bij toegang tot Microsoft Edge via UI Automation kan NVDA meer bedieningselementen activeren in de browse-modus. (#14612)
* NVDA zal niet meer falen om te starten wanneer het configuratiebestand beschadigd is, maar het zal de configuratie herstellen naar de standaardinstellingen zoals het in het verleden deed. (#15690, @CyrilleB79)
* Ondersteuning voor "System List view" (`SysListView32`) besturingselementen in Windows Forms-toepassingen is hersteld. (#15283, @LeonarddeR)
* Het is niet langer mogelijk om de geschiedenis van NVDA's Python-console te overschrijven. (#15792, @CyrilleB79)
* NVDA blijft responsief wanneer het wordt overspoeld met veel UI Automation-evenementen, bijvoorbeeld wanneer grote hoeveelheden tekst naar een terminal worden afgedrukt of bij het luisteren naar spraakberichten in WhatsApp Messenger. (#14888, #15169)
  * Dit nieuwe gedrag kan worden uitgeschakeld via de nieuwe instelling "Gebruik verbeterde gebeurtenisverwerking" in de geavanceerde instellingen van NVDA.
* NVDA kan opnieuw de focus volgen in toepassingen die binnen Windows Defender Application Guard (WDAG) draaien. (#15164)
* De spraaktekst wordt niet langer bijgewerkt wanneer de muis beweegt in de Spraakviewer. (#15952, @hwf1324)
* NVDA schakelt weer terug naar de browse-modus bij het sluiten van keuzelijsten met `escape` of `alt+omhoog` in Firefox of Chrome. (#15653)
* Bij het omhoog en omlaag bewegen in keuzelijsten in iTunes wordt niet langer ongepast teruggeschakeld naar de browse-modus. (#15653)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Note: this is an Add-on API compatibility breaking release.
Add-ons will need to be re-tested and have their manifest updated.
* Building NVDA now requires Visual Studio 2022.
Please refer to the [NVDA docs](https://github.com/nvaccess/nvda/blob/release-2024.1/projectDocs/dev/createDevEnvironment.md) for the specific list of Visual Studio components. (#14313)
* Added the following extension points:
  * `treeInterceptorHandler.post_browseModeStateChange`. (#14969, @nvdaes)
  * `speech.speechCanceled`. (#15700, @LeonarddeR)
  * `_onErrorSoundRequested` (should be retrieved calling `logHandler.getOnErrorSoundRequested()`) (#15691, @CyrilleB79)
* It is now possible to use plural forms in an add-on's translations. (#15661, @beqabeqa473)
* Included python3.dll in the binary distribution for use by add-ons with external libraries utilizing the [stable ABI](https://docs.python.org/3.11/c-api/stable.html). (#15674, @mzanm)
* The `BrailleDisplayDriver` base class now has `numRows` and `numCols` properties to provide information about multi line braille displays.
Setting `numCells` is still supported for single line braille displays and `numCells` will return the total number of cells for multi line braille displays. (#15386)
* Updated BrlAPI for BRLTTY to version 0.8.5, and its corresponding python module to a Python 3.11 compatible build. (#15652, @LeonarddeR)
* Added the `speech.speakSsml` function, which allows you to write NVDA speech sequences using [SSML](https://www.w3.org/TR/speech-synthesis11/). (#15699, @LeonarddeR)
  * The following tags are currently supported and translated to appropriate NVDA speech commands:
    * `Prosody` (`pitch`, `rate` and `volume`). Only multiplication (e.g. `200%` are supported.
    * `say-as` with the `interpret` attribute set to `characters`
    * `voice` with the `xml:lang` set to an XML language
    * `break` with the `time` attribute set to a value in milliseconds, e.g. `200ms`
    * `mark` with the `name` attribute set to a mark name, e.g. `mark1`, requires providing a callback
  * Example: `speech.speakSsml('&lt;speak&gt;&lt;prosody pitch="200%"&gt;hello&lt;/prosody&gt;&lt;break time="500ms" /&gt;&lt;prosody rate="50%"&gt;John&lt;/prosody&gt;&lt;/speak&gt;')`
  * The SSML parsing capabilities are backed by the `SsmlParser` class in the `speechXml` module.
* Changes to the NVDA Controller Client library:
  * The file names of the library no longer contain a suffix denoting the architecture, i.e. `nvdaControllerClient32/64.dll` are now called `nvdaControllerClient.dll`. (#15718, #15717, @LeonarddeR)
  * Added an example to demonstrate using nvdaControllerClient.dll from Rust. (#15771, @LeonarddeR)
  * Added the following functions to the controller client: (#15734, #11028, #5638, @LeonarddeR)
    * `nvdaController_getProcessId`: To get the process id (PID) of the current instance of NVDA the controller client is using.
    * `nvdaController_speakSsml`: To instruct NVDA to speak according to the given SSML. This function also supports:
      * Providing the symbol level.
      * Providing the priority of speech to be spoken.
      * Speaking both synchronously (blocking) and asynchronously (instant return).
    * `nvdaController_setOnSsmlMarkReachedCallback`: To register a callback of type `onSsmlMarkReachedFuncType` that is called in synchronous mode for every `&lt;mark /&gt;` tag encountered in the SSML sequence provided to `nvdaController_speakSsml`.
  * Note: the new functions in the controller client only support NVDA 2024.1 and above.
* Updated `include` dependencies:
  * detours to `4b8c659f549b0ab21cf649377c7a84eb708f5e68`. (#15695)
  * ia2 to `3d8c7f0b833453f761ded6b12d8be431507bfe0b`. (#15695)
  * sonic to `8694c596378c24e340c09ff2cd47c065494233f1`. (#15695)
  * w3c-aria-practices to `9a5e55ccbeb0f1bf92b6127c9865da8426d1c864`. (#15695)
  * wil to `5e9be7b2d2fe3834a7107f430f7d4c0631f69833`. (#15695)
* Device info yielded by `hwPortUtils.listUsbDevices` now contain the bus reported description of the USB device (key `busReportedDeviceDescription`). (#15764, @LeonarddeR)
* For USB serial devices, `bdDetect.getConnectedUsbDevicesForDriver` and `bdDetect.getDriversForConnectedUsbDevices` now yield device matches containing a `deviceInfo` dictionary enriched with data about the USB device, such as `busReportedDeviceDescription`. (#15764, @LeonarddeR)
* When the configuration file `nvda.ini` is corrupted, a backup copy is saved before it is reinitialized. (#15779, @CyrilleB79)
* When defining a script with the script decorator, the `speakOnDemand` boolean argument can be specified to control if a script should speak while in "on-demand" speech mode. (#481, @CyrilleB79)
  * Scripts that provide information (e.g. say window title, report time/date) should speak in the "on-demand" mode.
  * Scripts that perform an action (e.g. move the cursor, change a parameter) should not speak in the "on-demand" mode.
* Fixed bug where deleting git-tracked files during `scons -c` resulted in missing UIA COM interfaces on rebuild. (#7070, #10833, @hwf1324)
* Fix a bug where some code changes were not detected when building `dist`, that prevented a new build from being triggered.
Now `dist` always rebuilds. (#13372, @hwf1324)
* A `gui.nvdaControls.MessageDialog` with default type of standard, no longer throws a None conversion exception because no sound is assigned. (#16223, @XLTechie)

#### API Breaking Changes

These are breaking API changes.
Please open a GitHub issue if your Add-on has an issue with updating to the new API.

* NVDA is now built with Python 3.11. (#12064)
* Updated pip dependencies:
  * configobj to 5.1.0dev commit `e2ba4457c4651fa54f8d59d8dcdd3da950e956b8`. (#15544)
  * Comtypes to 1.2.0. (#15513, @codeofdusk)
  * Flake8 to 4.0.1. (#15636, @lukaszgo1)
  * py2exe to 0.13.0.1dev commit `4e7b2b2c60face592e67cb1bc935172a20fa371d`. (#15544)
  * robotframework to 6.1.1. (#15544)
  * SCons to 4.5.2. (#15529, @LeonarddeR)
  * sphinx to 7.2.6. (#15544)
  * wxPython to 4.2.2a commit `0205c7c1b9022a5de3e3543f9304cfe53a32b488`. (#12551, #16257)
* Removed pip dependencies:
  * typing_extensions, these should be supported natively in Python 3.11 (#15544)
  * nose, instead unittest-xml-reporting is used to generate XML reports. (#15544)
* `IAccessibleHandler.SecureDesktopNVDAObject` has been removed.
Instead, when NVDA is running on the user profile, track the existence of the secure desktop with the extension point: `winAPI.secureDesktop.post_secureDesktopStateChange`. (#14488)
* `braille.BrailleHandler.handlePendingCaretUpdate` has been removed with no public replacement. (#15163, @LeonarddeR)
* `bdDetect.addUsbDevices and bdDetect.addBluetoothDevices` have been removed.
Braille display drivers should implement the `registerAutomaticDetection` class method instead.
That method receives a `DriverRegistrar` object on which the `addUsbDevices` and `addBluetoothDevices` methods can be used. (#15200, @LeonarddeR)
* The default implementation of the check method on `BrailleDisplayDriver` now requires both the `threadSafe` and `supportsAutomaticDetection` attributes to be set to `True`. (#15200, @LeonarddeR)
* Passing lambda functions to `hwIo.ioThread.IoThread.queueAsApc` is no longer possible, as functions should be weakly referenceable. (#14627, @LeonarddeR)
* `IoThread.autoDeleteApcReference` has been removed. (#14924, @LeonarddeR)
* To support capital pitch changes, synthesizers must now explicitly declare their support for the `PitchCommand` in the `supportedCommands` attribute on the driver. (#15433, @LeonarddeR)
* `speechDictHandler.speechDictVars` has been removed. Use `NVDAState.WritePaths.speechDictsDir` instead of `speechDictHandler.speechDictVars.speechDictsPath`. (#15614, @lukaszgo1)
* `languageHandler.makeNpgettext` and `languageHandler.makePgettext` have been removed.
`npgettext` and `pgettext` are supported natively now. (#15546)
* The app module for [Poedit](https://poedit.net) has been changed significantly. The `fetchObject` function has been removed. (#15313, #7303, @LeonarddeR)
* The following redundant types and constants have been removed from `hwPortUtils`: (#15764, @LeonarddeR)
  * `PCWSTR`
  * `HWND` (replaced by `ctypes.wintypes.HWND`)
  * `ULONG_PTR`
  * `ULONGLONG`
  * `NULL`
  * `GUID` (replaced by `comtypes.GUID`)
* `gui.addonGui.AddonsDialog` has been removed. (#15834)
* `touchHandler.TouchInputGesture.multiFingerActionLabel` has been removed with no replacement. (#15864, @CyrilleB79)
* `NVDAObjects.IAccessible.winword.WordDocument.script_reportCurrentHeaders` has been removed with no replacement. (#15904, @CyrilleB79)
* The following app modules are removed.
Code which imports from one of them, should instead import from the replacement module. (#15618, @lukaszgo1)

| Removed module name |Replacement module|
|---|---|
|`azardi-2.0` |`azardi20`|
|`azuredatastudio` |`code`|
|`azuredatastudio-insiders` |`code`|
|`calculatorapp` |`calculator`|
|`code - insiders` |`code`|
|`commsapps` |`hxmail`|
|`dbeaver` |`eclipse`|
|`digitaleditionspreview` |`digitaleditions`|
|`esybraille` |`esysuite`|
|`hxoutlook` |`hxmail`|
|`miranda64` |`miranda32`|
|`mpc-hc` |`mplayerc`|
|`mpc-hc64` |`mplayerc`|
|`notepad++` |`notepadPlusPlus`|
|`searchapp` |`searchui`|
|`searchhost` |`searchui`|
|`springtoolsuite4` |`eclipse`|
|`sts` |`eclipse`|
|`teamtalk3` |`teamtalk4classic`|
|`textinputhost` |`windowsinternal_composableshell_experiences_textinput_inputapp`|
|`totalcmd64` |`totalcmd`|
|`win32calc` |`calc`|
|`winmail` |`msimn`|
|`zend-eclipse-php` |`eclipse`|
|`zendstudio` |`eclipse`|

#### Deprecations

* Using `watchdog.getFormattedStacksForAllThreads` is deprecated - please use `logHandler.getFormattedStacksForAllThreads` instead. (#15616, @lukaszgo1)
* `easeOfAccess.canConfigTerminateOnDesktopSwitch` has been deprecated, as it became obsolete since Windows 7 is no longer supported. (#15644, @LeonarddeR)
* `winVersion.isFullScreenMagnificationAvailable` has been deprecated - use `visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart` instead. (#15664, @josephsl)
* The following Windows release constants has been deprecated from winVersion module (#15647, @josephsl):
  * `winVersion.WIN7`
  * `winVersion.WIN7_SP1`
  * `winVersion.WIN8`
* The `bdDetect.KEY_*` constants have been deprecated.
Use `bdDetect.DeviceType.*` instead. (#15772, @LeonarddeR).
* The `bdDetect.DETECT_USB` and `bdDetect.DETECT_BLUETOOTH` constants have been deprecated with no public replacement. (#15772, @LeonarddeR).
* Using `gui.ExecAndPump` is deprecated - please use `systemUtils.ExecAndPump` instead. (#15852, @lukaszgo1)

## 2023.3.4

Dit is een patchrelease om een beveiligingsprobleem en een installatieprobleem op te lossen.
Gelieve beveiligingsproblemen verantwoord openbaar te maken volgens het [beveiligingsbeleid](https://github.com/nvaccess/nvda/blob/master/security.md) van NVDA.

### Beveiligingsfixes

* Voorkomt het laden van aangepaste configuraties terwijl de beveiligingsmodus is ingeschakeld.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Foutoplossingen

* Opgelost probleem waarbij het NVDA-proces niet correct kon afsluiten. (#16123)
* Opgelost probleem waarbij als het vorige NVDA-proces niet correct kon afsluiten, een NVDA-installatie in een onherstelbare toestand kon belanden. (#16122)

## 2023.3.3

Dit is een patchrelease om een beveiligingsprobleem op te lossen.
Gelieve beveiligingsproblemen verantwoord openbaar te maken volgens het [beveiligingsbeleid](https://github.com/nvaccess/nvda/blob/master/security.md) van NVDA.

### Beveiligingsfixes

* Voorkomt mogelijke reflectie XSS-aanvallen van op maat gemaakte inhoud die kan leiden tot willekeurige code-uitvoering.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Dit is een patchrelease om een beveiligingsprobleem op te lossen.
De beveiligingspatch in 2023.3.1 was niet correct opgelost.
Gelieve beveiligingsproblemen verantwoord openbaar te maken volgens het [beveiligingsbeleid](https://github.com/nvaccess/nvda/blob/master/security.md) van NVDA.

### Beveiligingsfixes

* De beveiligingspatch in 2023.3.1 was niet correct opgelost.
Voorkomt mogelijke systeemtoegang en willekeurige code-uitvoering met systeemrechten voor niet-geauthenticeerde gebruikers.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Dit is een patchrelease om een beveiligingsprobleem op te lossen.
Gelieve beveiligingsproblemen verantwoord openbaar te maken volgens het [beveiligingsbeleid](https://github.com/nvaccess/nvda/blob/master/security.md) van NVDA.

### Beveiligingsfixes

* Voorkomt mogelijke systeemtoegang en willekeurige code-uitvoering met systeemrechten voor niet-geauthenticeerde gebruikers.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Deze release bevat verbeteringen aan de prestaties, responsiviteit en stabiliteit van audio-uitvoer.
Opties zijn toegevoegd om het volume van NVDA-geluiden en -piepjes te regelen, of om ze het volume van de spraak die je gebruikt te laten volgen.

NVDA kan nu periodiek OCR-resultaten vernieuwen, waarbij nieuwe tekst wordt uitgesproken zodra deze verschijnt.
Dit kan worden ingesteld in de Windows OCR-categorie van NVDA's instellingen.

Er zijn verschillende braille-fouten opgelost, wat de detectie van apparaten en de beweging van de cursor verbetert.
Het is nu mogelijk om ongewenste stuurprogramma's uit te sluiten van automatische detectie om de autodetectieprestaties te verbeteren.
Er zijn ook nieuwe BRLTTY-commando's toegevoegd.

Ook zijn er bugfixes voor de Add-on Store, Microsoft Office, contextmenu's in Microsoft Edge en de Windows Calculator.

### Nieuwe functies

* Verbeterd geluidsbeheer:
  * Een nieuw Audio-instellingenpaneel:
    * Dit kan worden geopend met `NVDA+control+u`. (#15497)
    * Een optie in Audio-instellingen om het volume van NVDA-geluiden en -piepjes het volume van de spraak die je gebruikt te laten volgen. (#1409)
    * Een optie in Audio-instellingen om het volume van NVDA-geluiden afzonderlijk in te stellen. (#1409, #15038)
    * De instellingen om het audio-uitvoerapparaat te wijzigen en audio-demping in te schakelen zijn verplaatst naar het nieuwe Audio-instellingenpaneel vanuit de Select Synthesizer-dialoog.
    Deze opties zullen worden verwijderd uit de "select synthesizer" dialoog in 2024.1. (#15486, #8711)
  * NVDA zal nu audio via de Windows Audio Session API (WASAPI) uitvoeren, wat de responsiviteit, prestaties en stabiliteit van NVDA-spraak en -geluiden kan verbeteren. (#14697, #11169, #11615, #5096, #10185, #11061)
  * Opmerking: WASAPI is niet compatibel met sommige add-ons.
  Compatibele updates zijn beschikbaar voor deze add-ons, werk ze bij voordat je NVDA bijwerkt.
  Niet-compatibele versies van deze add-ons worden uitgeschakeld bij het bijwerken van NVDA:
    * Tony's Enhancements versie 1.15 of ouder. (#15402)
    * NVDA global commands extension 12.0.8 of ouder. (#15443)
* NVDA kan nu voortdurend de resultaten bijwerken bij het uitvoeren van optische tekenherkenning (OCR), waarbij nieuwe tekst wordt uitgesproken zodra deze verschijnt. (#2797)
  * Om deze functionaliteit in te schakelen, zet je de optie "Periodiek herkende inhoud vernieuwen" aan in de Windows OCR-categorie van NVDA's instellingen.
  * Zodra deze is ingeschakeld, kun je het uitspreken van nieuwe tekst inschakelen door de rapportage van dynamische inhoudsveranderingen in te schakelen (druk op `NVDA+5`).
* Bij gebruik van automatische detectie van braille-displays is het nu mogelijk om stuurprogramma's uit te sluiten van detectie via de braille-displayselectiedialoog. (#15196)
* Een nieuwe optie in Documentopmaakinstellingen, "Negeer lege regels voor lijninspringingsrapportage". (#13394)
* Een niet-toegewezen gebaar toegevoegd om te navigeren door tabbladen in browse-modus. (#15046)

### Veranderingen

* Braille:
  * Wanneer de tekst in een terminal verandert zonder de cursor bij te werken, wordt de tekst op een braille-display nu correct bijgewerkt wanneer deze zich op een gewijzigde regel bevindt.
  Dit omvat situaties waarbij braille is vastgelegd op review. (#15115)
  * Meer BRLTTY-toetsenbindingen zijn nu gekoppeld aan NVDA-commando's (#6483):
    * `learn`: NVDA-inputhulp inschakelen
    * `prefmenu`: het NVDA-menu openen
    * `prefload`/`prefsave`: NVDA-configuratie laden/opslagen
    * `time`: Tijd weergeven
    * `say_line`: Spreek de huidige regel uit waar de reviewcursor zich bevindt
    * `say_below`: Alles zeggen met behulp van de reviewcursor
  * De BRLTTY-stuurprogramma is alleen beschikbaar wanneer een BRLTTY-instantie met BrlAPI ingeschakeld draait. (#15335)
  * De geavanceerde instelling om ondersteuning voor HID-braille in te schakelen is verwijderd ten gunste van een nieuwe optie.
  Je kunt nu specifieke stuurprogramma's voor braille-display autodetectie uitschakelen in de braille-displayselectiedialoog. (#15196)
* Add-on Store: Geïnstalleerde add-ons worden nu vermeld in het tabblad Beschikbare add-ons, als ze beschikbaar zijn in de winkel. (#15374)
* Sommige sneltoetsen zijn bijgewerkt in het NVDA-menu. (#15364)

### Opgeloste problemen

* Microsoft Office:
  * Crash in Microsoft Word opgelost wanneer de documentopmaakopties "koppen rapporteren" en "opmerkingen en notities rapporteren" niet waren ingeschakeld. (#15019)
  * In Word en Excel wordt de tekstuitlijning nu correct gerapporteerd in meer situaties. (#15206, #15220)
  * Oplossingen voor de aankondiging van sommige cellenopmaak-sneltoetsen in Excel. (#15527)
* Microsoft Edge:
  * NVDA springt niet langer terug naar de laatste browse-moduspositie bij het openen van het contextmenu in Microsoft Edge. (#15309)
  * NVDA kan weer contextmenu's van downloads in Microsoft Edge lezen. (#14916)
* Braille:
  * De braillecursor en selectie-indicatoren worden nu altijd correct bijgewerkt na het tonen of verbergen van de respectieve indicatoren met een gebaar. (#15115)
  * Oplossing voor probleem waarbij Albatross-braille-displays proberen te initialiseren hoewel een ander braille-apparaat is verbonden. (#15226)
* Add-on Store:
  * Oplossing voor probleem waarbij het uitschakelen van "inclusief incompatibele add-ons" resulteerde in het nog steeds vermelden van incompatibele add-ons in de winkel. (#15411)
  * Add-ons die om compatibiliteitsredenen zijn geblokkeerd, moeten nu correct worden gefilterd bij het omschakelen van de filter voor ingeschakelde/uitgeschakelde status. (#15416)
  * Oplossing voor probleem waarbij overschreven ingeschakelde incompatibele add-ons niet konden worden bijgewerkt of vervangen met behulp van het externe installatietool. (#15417)
  * Oplossing voor probleem waarbij NVDA niet sprak totdat deze opnieuw werd opgestart na de installatie van een add-on. (#14525)
  * Oplossing voor probleem waarbij add-ons niet konden worden geïnstalleerd als een eerdere download was mislukt of geannuleerd. (#15469)
  * Oplossing voor problemen met het omgaan met incompatibele add-ons bij het upgraden van NVDA. (#15414, #15412, #15437)
* NVDA kondigt weer de rekenresultaten aan in de 32-bits Windows Calculator op Server-, LTSC- en LTSB-versies van Windows. (#15230)
* NVDA negeert geen focuswijzigingen meer wanneer een genest venster (klein kindvenster) focus krijgt. (#15432)
* Oplossing voor een mogelijke oorzaak van vastlopen tijdens de opstart van NVDA. (#15517)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* `braille.handler.handleUpdate` and `braille.handler.handleReviewMove` have been changed in order not to update instantly.
Before this change, when either of these methods was called very often, this would drain many resources.
These methods now queue an update at the end of every core cycle instead.
They should also be thread safe, making it possible to call them from background threads. (#15163)
* Added official support to register custom braille display drivers in the automatic braille display detection process.
Consult the `braille.BrailleDisplayDriver` class documentation for more details.
Most notably, the `supportsAutomaticDetection` attribute must be set to `True` and the `registerAutomaticDetection` `classmethod` must be implemented.  (#15196)

#### Deprecations

* `braille.BrailleHandler.handlePendingCaretUpdate` is now deprecated with no public replacement.
It will be removed in 2024.1. (#15163)
* Importing the constants `xlCenter`, `xlJustify`, `xlLeft`, `xlRight`, `xlDistributed`, `xlBottom`, `xlTop` from `NVDAObjects.window.excel` is deprecated.
Use `XlHAlign` or `XlVAlign` enumerations instead. (#15205)
* The mapping `NVDAObjects.window.excel.alignmentLabels` is deprecated.
Use the `displayString` methods of `XlHAlign` or `XlVAlign` enumerations instead. (#15205)
* `bdDetect.addUsbDevices` and `bdDetect.addBluetoothDevices` have been deprecated.
Braille display drivers should implement the `registerAutomaticDetection` classmethod instead.
That method receives a `DriverRegistrar` object on which the `addUsbDevices` and `addBluetoothDevices` methods can be used. (#15200)
* The default implementation of the check method on `BrailleDisplayDriver` uses `bdDetect.driverHasPossibleDevices` for devices that are marked as thread safe.
Starting from NVDA 2024.1, in order for the base method to use `bdDetect.driverHasPossibleDevices`, the `supportsAutomaticDetection` attribute must be set to `True` as well. (#15200)

## 2023.2

Deze release introduceert de Add-on Store ter vervanging van de Add-ons Manager.
In de Add-on Store kun je community-add-ons doorbladeren, zoeken, installeren en bijwerken.
Je kunt nu handmatig incompatibiliteitsproblemen met verouderde add-ons overschrijven op eigen risico.

Er zijn nieuwe braillefuncties, commando's en weergavesteun toegevoegd.
Er zijn ook nieuwe invoergebaren voor OCR en vlakke objectnavigatie.
Het navigeren en rapporteren van opmaak in Microsoft Office is verbeterd.

Er zijn veel bugfixes, met name voor braille, Microsoft Office, webbrowsers en Windows 11.

eSpeak-NG, LibLouis braillevertaler en Unicode CLDR zijn bijgewerkt.

### Nieuwe functies

* De Add-on Store is toegevoegd aan NVDA. (#13985)
  * Doorblader, zoek, installeer en werk community-add-ons bij.
  * Handmatig incompatibiliteitsproblemen met verouderde add-ons overschrijven.
  * De Add-ons Manager is verwijderd en vervangen door de Add-on Store.
  * Voor meer informatie kun je de bijgewerkte gebruikershandleiding lezen.
* Nieuwe invoergebaren:
  * Een niet-toegewezen gebaar om door de beschikbare talen voor Windows OCR te schakelen. (#13036)
  * Een niet-toegewezen gebaar om door de braille-berichtweergavemodi te schakelen. (#14864)
  * Een niet-toegewezen gebaar om het tonen van de selectie-indicator voor braille in of uit te schakelen. (#14948)
  * Toegevoegde standaardtoetscombinaties om naar het volgende of vorige object te verplaatsen in een vlakke weergave van de objecthiërarchie. (#15053)
    * Desktop: `NVDA+numpad9` en `NVDA+numpad3` om respectievelijk naar de vorige en volgende objecten te verplaatsen.
    * Laptop: `shift+NVDA+[` en `shift+NVDA+]` om respectievelijk naar de vorige en volgende objecten te verplaatsen.
* Nieuwe braillefuncties:
  * Ondersteuning toegevoegd voor de Help Tech Activator braille-display. (#14917)
  * Een nieuwe optie om de selectie-indicator (punten 7 en 8) in of uit te schakelen. (#14948)
  * Een nieuwe optie om optioneel de systeemcursor of focus te verplaatsen bij het wijzigen van de positie van de reviewcursor met braille-routingtoetsen. (#14885, #3166)
  * Wanneer `numpad2` drie keer wordt ingedrukt om de numerieke waarde van het teken op de positie van de reviewcursor te rapporteren, wordt de informatie nu ook in braille weergegeven. (#14826)
  * Ondersteuning toegevoegd voor het `aria-brailleroledescription` ARIA 1.3 attribuut, waardoor webauteurs het type van een element op het braille-display kunnen overschrijven. (#14748)
  * Baum braille-stuurprogramma: toegevoegd verschillende braille-akkoordgebaren voor het uitvoeren van veelvoorkomende toetsenbordcommando's zoals `windows+d` en `alt+tab`.
  Raadpleeg de NVDA-gebruikershandleiding voor een volledige lijst. (#14714)
* Uitspraak van Unicode-symbolen toegevoegd:
  * braille-symbolen zoals `⠐⠣⠃⠗⠇⠐⠜`. (#13778)
  * Mac Option-toets symbool `⌥`. (#14682)
* Gebaren toegevoegd voor Tivomatic Caiku Albatross braille-displays. (#14844, #15002)
  * het tonen van de braille-instellingen dialoog
  * toegang tot de statusbalk
  * het schakelen van de vorm van de braillecursor
  * het schakelen van de braille-berichtweergavemodus
  * het in- of uitschakelen van de braillecursor
  * het schakelen van de status van de "braille-show-selectie-indicator"
  * het schakelen van de "braille-verplaats-systeemcursor-when-routing-review-cursor" modus. (#15122)
* Microsoft Office-functies:
  * Wanneer de gemarkeerde tekst de Documentopmaakoptie "highlight" heeft ingeschakeld, worden de markeerkleuren nu gerapporteerd in Microsoft Word. (#7396, #12101, #5866)
  * Wanneer kleuren zijn ingeschakeld in Documentopmaak, worden achtergrondkleuren nu gerapporteerd in Microsoft Word. (#5866)
  * Bij het gebruiken van Excel-sneltoetsen om opmaak zoals vet, cursief, onderstrepen en doorhalen van een cel in Excel te schakelen, wordt het resultaat nu gerapporteerd. (#14923)
* Experimenteel verbeterd geluidsbeheer:
  * NVDA kan nu audio via de Windows Audio Session API (WASAPI) uitvoeren, wat de responsiviteit, prestaties en stabiliteit van NVDA-spraak en -geluiden kan verbeteren. (#14697)
  * Het gebruik van WASAPI kan worden ingeschakeld in Geavanceerde instellingen.
  Daarnaast kunnen, als WASAPI is ingeschakeld, de volgende Geavanceerde instellingen ook worden geconfigureerd.
    * Een optie om het volume van NVDA-geluiden en -piepjes het volume van de spraak die je gebruikt te laten volgen. (#1409)
    * Een optie om het volume van NVDA-geluiden afzonderlijk in te stellen. (#1409, #15038)
  * Er is een bekend probleem met sporadisch vastlopen bij het inschakelen van WASAPI. (#15150)
* In Mozilla Firefox en Google Chrome rapporteert NVDA nu wanneer een controle een dialoog, rooster, lijst of boom opent als de auteur dit heeft gespecificeerd met `aria-haspopup`. (#8235)
* Het is nu mogelijk om systeemvariabelen (zoals `%temp%` of `%homepath%`) te gebruiken in het pad terwijl je draagbare kopieën van NVDA maakt. (#14680)
* In Windows 10 Mei 2019 Update en later kan NVDA virtuele desktopnamen aankondigen bij het openen, wijzigen en sluiten ervan. (#5641)
* Een systeemwijd parameter is toegevoegd om gebruikers en systeembeheerders toe te staan NVDA te dwingen om in de beveiligde modus te starten. (#10018)

### Veranderingen

* Componentupdates:
  * eSpeak NG is bijgewerkt naar 1.52-dev commit `ed9a7bcf`. (#15036)
  * LibLouis braillevertaler is bijgewerkt naar [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR is bijgewerkt naar versie 43.0. (#14918)
* LibreOffice wijzigingen:
  * Bij het rapporteren van de locatie van de reviewcursor wordt de huidige cursor/caret locatie nu gerapporteerd ten opzichte van de huidige pagina in LibreOffice Writer 7.6 en nieuwer, vergelijkbaar met wat wordt gedaan voor Microsoft Word. (#11696)
  * Aankondiging van de statusbalk (bijv. getriggerd door `NVDA+eind`) werkt voor LibreOffice. (#11698)
  * Bij het verplaatsen naar een andere cel in LibreOffice Calc, kondigt NVDA de coördinaten van de eerder gefocuste cel niet langer onjuist aan wanneer de celcoördinaat-aankondiging is uitgeschakeld in de NVDA-instellingen. (#15098)
* Braille wijzigingen:
  * Bij het gebruik van een braille-display via de Standaard HID braille-stuurprogramma, kan de dpad worden gebruikt om de pijltjestoetsen en enter na te bootsen.
  Ook `space+dot1` en `space+dot4` worden nu respectievelijk toegewezen aan de omhoog en omlaag pijlen. (#14713)
  * Updates van dynamische webinhoud (ARIA live-regio's) worden nu weergegeven in braille.
  Dit kan worden uitgeschakeld in het paneel Geavanceerde Instellingen. (#7756)
* Dash- en em-dash-symbolen worden altijd naar de synthesizer gestuurd. (#13830)
* Afstand gerapporteerd in Microsoft Word houdt nu rekening met de eenheid gedefinieerd in de geavanceerde opties van Word, zelfs bij het gebruik van UIA om Word-documenten te openen. (#14542)
* NVDA reageert sneller bij het verplaatsen van de cursor in bewerkingsbesturingselementen. (#14708)
* Script voor het rapporteren van de bestemming van een link rapporteert nu vanaf de caret / focus positie in plaats van het navigatorobject. (#14659)
* Het maken van draagbare kopieën vereist niet langer dat een schijfletter wordt ingevoerd als onderdeel van het absolute pad. (#14680)
* Als Windows is geconfigureerd om seconden in de systeemklok te tonen, houdt het gebruik van `NVDA+f12` om de tijd te rapporteren nu rekening met die instelling. (#14742)
* NVDA zal nu ongeëtiketteerde groeperingen rapporteren die nuttige positie-informatie hebben, zoals in recente versies van Microsoft Office 365-menu's. (#14878)

### Opgeloste problemen

* Braille:
  * Verschillende stabiliteitsfixes voor invoer/uitvoer voor braille-displays, wat resulteert in minder frequente fouten en vastlopers van NVDA. (#14627)
  * NVDA schakelt niet langer onnodig meerdere keren naar geen braille tijdens automatische detectie, wat resulteert in een schoner logboek en minder overhead. (#14524)
  * NVDA schakelt nu weer terug naar USB als een HID Bluetooth-apparaat (zoals de HumanWare Brailliant of APH Mantis) automatisch wordt gedetecteerd en een USB-verbinding beschikbaar komt.
  Dit werkte eerder alleen voor Bluetooth-Seriële poorten. (#14524)
  * Wanneer er geen braille-display is aangesloten en de braille-viewer wordt gesloten door `alt+f4` in te drukken of op de sluitknop te klikken, wordt de weergavegrootte van de braille-subsystemen weer gereset naar geen cellen. (#15214)
* Webbrowsers:
  * NVDA veroorzaakt niet langer af en toe een crash of stopzetting van Mozilla Firefox. (#14647)
  * In Mozilla Firefox en Google Chrome worden getypte tekens niet langer gerapporteerd in sommige tekstvakken, zelfs wanneer het spreken van getypte tekens is uitgeschakeld. (#8442)
  * Je kunt nu browse-modus gebruiken in Chromium Embedded Controls waar dit eerder niet mogelijk was. (#13493, #8553)
  * In Mozilla Firefox rapporteert NVDA nu betrouwbaar de tekst wanneer de muis over tekst na een link beweegt. (#9235)
  * De bestemming van grafische links wordt nu nauwkeuriger gerapporteerd in meer gevallen in Chrome en Edge. (#14783)
  * Bij het proberen om de URL voor een link zonder href-attribuut te rapporteren, is NVDA niet langer stil.
  In plaats daarvan rapporteert NVDA dat de link geen bestemming heeft. (#14723)
  * In Browse-modus negeert NVDA niet langer onterecht de focus die verschuift naar een bovenliggend of kind-besturingselement, bijvoorbeeld bij het verplaatsen van een besturingselement naar een bovenliggend lijstitem of roostercel. (#14611)
    * Merk echter op dat deze fix alleen van toepassing is wanneer de optie "Automatisch focus instellen op focusbare elementen" in de Browse-modusinstellingen is uitgeschakeld (wat de standaardinstelling is).
* Fixes voor Windows 11:
  * NVDA kan weer de statusbalkinhoud van Kladblok aankondigen. (#14573)
  * Wisselen tussen tabbladen kondigt de nieuwe tabbladnaam en -positie aan voor Kladblok en Verkenner. (#14587, #14388)
  * NVDA kondigt weer kandidaat-items aan bij het invoeren van tekst in talen zoals Chinees en Japans. (#14509)
  * Het is weer mogelijk om de items Contributors en License in het NVDA Help-menu te openen. (#14725)
* Microsoft Office-fixes:
  * Bij het snel verplaatsen door cellen in Excel, is NVDA nu minder waarschijnlijk om de verkeerde cel of selectie te rapporteren. (#14983, #12200, #12108)
  * Wanneer je op een Excel-cel landt vanuit een andere werkblad, worden braille en focus-highlightter niet langer onterecht bijgewerkt naar het object dat eerder de focus had. (#15136)
  * NVDA faalt niet langer om het focussen van wachtwoordvelden in Microsoft Excel en Outlook aan te kondigen. (#14839)
* Voor symbolen die geen symboolomschrijving in de huidige taal hebben, wordt het standaard Engelse symboolniveau gebruikt. (#14558, #14417)
* Het is nu mogelijk om het backslash-teken in het vervangingsveld van een woordenboekitem te gebruiken, wanneer het type niet is ingesteld op reguliere expressie. (#14556)
* In Windows 10 en 11 Rekenkundige, doet een draagbare kopie van NVDA niet langer niets of speelt geen fouttonen af bij het invoeren van expressies in de standaard rekenmachine in de compacte overlaymodus. (#14679)
* NVDA herstelt zich weer uit veel meer situaties zoals toepassingen die stoppen met reageren, wat eerder leidde tot volledige bevriezing. (#14759)
* Bij het forceren van UIA-ondersteuning met bepaalde terminals en consoles, is een bug opgelost die een vastloper veroorzaakte en het logbestand volspamde. (#14689)
* NVDA weigert niet langer om de configuratie op te slaan na een configuratiereset. (#13187)
* Bij het uitvoeren van een tijdelijke versie vanuit de launcher, zal NVDA gebruikers niet langer misleiden door te denken dat ze de configuratie kunnen opslaan. (#14914)
* NVDA reageert nu algemeen iets sneller op commando's en focuswijzigingen. (#14928)
* Het weergeven van de OCR-instellingen zal niet langer mislukken op sommige systemen. (#15017)
* Bug opgelost met betrekking tot het opslaan en laden van de NVDA-configuratie, inclusief het wisselen van synthesizers. (#14760)
* Bug opgelost die ervoor zorgde dat de "flick up" touchgebaren voor tekstreview pagina's verplaatste in plaats van naar de vorige regel te verplaatsen. (#15127)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Suggested conventions have been added to the add-on manifest specification.
These are optional for NVDA compatibility, but are encouraged or required for submitting to the Add-on Store. (#14754)
  * Use `lowerCamelCase` for the name field.
  * Use `&lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;` format for the version field (required for add-on datastore).
  * Use `https://` as the schema for the url field (required for add-on datastore).
* Added a new extension point type called `Chain`, which can be used to iterate over iterables returned by registered handlers. (#14531)
* Added the `bdDetect.scanForDevices` extension point.
Handlers can be registered that yield `BrailleDisplayDriver/DeviceMatch` pairs that don't fit in existing categories, like USB or Bluetooth. (#14531)
* Added extension point: `synthDriverHandler.synthChanged`. (#14618)
* The NVDA Synth Settings Ring now caches available setting values the first time they're needed, rather than when loading the synthesizer. (#14704)
* You can now call the export method on a gesture map to export it to a dictionary.
This dictionary can be imported in another gesture by passing it either to the constructor of `GlobalGestureMap` or to the update method on an existing map. (#14582)
* `hwIo.base.IoBase` and its derivatives now have a new constructor parameter to take a `hwIo.ioThread.IoThread`.
If not provided, the default thread is used. (#14627)
* `hwIo.ioThread.IoThread` now has a `setWaitableTimer` method to set a waitable timer using a python function.
Similarly, the new `getCompletionRoutine` method allows you to convert a python method into a completion routine safely. (#14627)
* `offsets.OffsetsTextInfo._get_boundingRects` should now always return `List[locationHelper.rectLTWH]` as expected for a subclass of `textInfos.TextInfo`. (#12424)
* `highlight-color` is now a format field attribute. (#14610)
* NVDA should more accurately determine if a logged message is coming from NVDA core. (#14812)
* NVDA will no longer log inaccurate warnings or errors about deprecated appModules. (#14806)
* All NVDA extension points are now briefly described in a new, dedicated chapter in the Developer Guide. (#14648)
* `scons checkpot` will no longer check the `userConfig` subfolder anymore. (#14820)
* Translatable strings can now be defined with a singular and a plural form using `ngettext` and `npgettext`. (#12445)

#### Deprecations

* Passing lambda functions to `hwIo.ioThread.IoThread.queueAsApc` is deprecated.
Instead, functions should be weakly referenceable. (#14627)
* Importing `LPOVERLAPPED_COMPLETION_ROUTINE` from `hwIo.base` is deprecated.
Instead import from `hwIo.ioThread`. (#14627)
* `IoThread.autoDeleteApcReference` is deprecated.
It was introduced in NVDA 2023.1 and was never meant to be part of the public API.
Until removal, it behaves as a no-op, i.e. a context manager yielding nothing. (#14924)
* `gui.MainFrame.onAddonsManagerCommand` is deprecated, use `gui.MainFrame.onAddonStoreCommand` instead. (#13985)
* `speechDictHandler.speechDictVars.speechDictsPath` is deprecated, use `NVDAState.WritePaths.speechDictsDir` instead. (#15021)
* Importing `voiceDictsPath` and `voiceDictsBackupPath` from `speechDictHandler.dictFormatUpgrade` is deprecated.
Instead use `WritePaths.voiceDictsDir` and `WritePaths.voiceDictsBackupDir` from `NVDAState`. (#15048)
* `config.CONFIG_IN_LOCAL_APPDATA_SUBKEY` is deprecated.
Instead use `config.RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY`. (#15049)

## 2023.1

Een nieuwe optie is toegevoegd, "Paragraafstijl" in "Documentnavigatie".
Deze kan worden gebruikt met teksteditors die geen paragraafnavigatie van zichzelf ondersteunen, zoals Notepad en Notepad++.

Er is een nieuw globaal commando toegevoegd om de bestemming van een link te rapporteren, toegewezen aan `NVDA+k`.

De ondersteuning voor geannoteerde webinhoud (zoals opmerkingen en voetnoten) is verbeterd.
Druk op `NVDA+d` om door samenvattingen te bladeren wanneer annotaties worden gerapporteerd (bijv. "heeft opmerking, heeft voetnoot").

Tivomatic Caiku Albatross 46/80 braille-displays worden nu ondersteund.

De ondersteuning voor ARM64- en AMD64-versies van Windows is verbeterd.

Er zijn veel bugfixes, vooral voor Windows 11.

eSpeak, LibLouis, Sonic rate boost en Unicode CLDR zijn bijgewerkt.
Er zijn nieuwe Georgische, Swahili (Kenya) en Chichewa (Malawi) braille-tabellen.

Opmerking:

* Deze release breekt de compatibiliteit met bestaande add-ons.

### Nieuwe functies

* Microsoft Excel via UI Automation: Automatische rapportage van kolom- en rijheaders in tabellen. (#14228)
  * Opmerking: Dit verwijst naar tabellen opgemaakt via de knop "Tabel" op het Invoegpaneel van het lint.
  "Eerste kolom" en "Headerrij" in "Tabelstijlopties" komen overeen met respectievelijk kolom- en rijheaders.
  * Dit verwijst niet naar schermlezer-specifieke headers via benoemde bereiken, wat momenteel niet wordt ondersteund via UI Automation.
* Een niet-toegewezen script is toegevoegd om vertraagde tekenbeschrijvingen te schakelen. (#14267)
* Een experimentele optie is toegevoegd om de UIA-meldingsondersteuning in Windows Terminal te benutten om nieuwe of gewijzigde tekst in de terminal te rapporteren, wat de stabiliteit en reactievermogen verbetert. (#13781)
  * Raadpleeg de gebruikershandleiding voor beperkingen van deze experimentele optie.
* Op Windows 11 ARM64 is browse-modus nu beschikbaar in AMD64-apps zoals Firefox, Google Chrome en 1Password. (#14397)
* Een nieuwe optie is toegevoegd, "Paragraafstijl" in "Documentnavigatie".
Deze voegt ondersteuning toe voor enkele regelafbreking (normaal) en meerregelige afbreking (blok) paragraafnavigatie.
Deze kan worden gebruikt met teksteditors die geen paragraafnavigatie van zichzelf ondersteunen, zoals Notepad en Notepad++. (#13797)
* De aanwezigheid van meerdere annotaties wordt nu gerapporteerd.
`NVDA+d` bladert nu door het rapporteren van de samenvatting van elk annotatiedoel voor oorsprongen met meerdere annotatiedoelen.
Bijvoorbeeld, wanneer tekst een opmerking en een voetnoot heeft die eraan zijn gekoppeld. (#14507, #14480)
* Ondersteuning toegevoegd voor Tivomatic Caiku Albatross 46/80 braille-displays. (#13045)
* Nieuw globaal commando: Rapporteren linkbestemming (`NVDA+k`).
Een enkele keer drukken spreekt/brailleert de bestemming van de link die zich in het navigatorobject bevindt.
Twee keer drukken toont deze in een venster voor gedetailleerder onderzoek. (#14583)
* Nieuw niet-toegewezen globaal commando (Tools-categorie): Rapporteren linkbestemming in een venster.
Vergelijkbaar met twee keer drukken op `NVDA+k`, maar kan nuttiger zijn voor braillegebruikers. (#14583)

### Veranderingen

* LibLouis braillevertaler bijgewerkt naar [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Grote updates voor Hongaars, UEB en Chinese bopomofo braille.
  * Ondersteuning voor de Deense braillestandaard 2022.
  * Nieuwe braille-tabellen voor Georgische literaire braille, Swahili (Kenya) en Chichewa (Malawi).
* Sonic rate boost-bibliotheek bijgewerkt naar commit `1d70513`. (#14180)
* CLDR is bijgewerkt naar versie 42.0. (#14273)
* eSpeak NG is bijgewerkt naar 1.52-dev commit `f520fecb`. (#14281, #14675)
  * Probleem opgelost bij rapporteren van grote getallen. (#14241)
* Java-toepassingen met besturingselementen die de selecteerbare status gebruiken, kondigen nu aan wanneer een item niet is geselecteerd in plaats van wanneer het item is geselecteerd. (#14336)

### Opgeloste problemen

* Windows 11-fixes:
  * NVDA kondigt nu zoekmarkeringen aan bij het openen van het Startmenu. (#13841)
  * Op ARM worden x64-apps niet langer geïdentificeerd als ARM64-toepassingen. (#14403)
  * Menu-items voor klembordgeschiedenis zoals "item vastzetten" zijn toegankelijk. (#14508)
  * In Windows 11 22H2 en nieuwer is het weer mogelijk om met de muis en aanraking te interageren met gebieden zoals het systeemvak-overloopvenster en het dialoogvenster "Openen met". (#14538, #14539)
* Suggesties worden gerapporteerd bij het typen van een @vermelding in Microsoft Excel-opmerkingen. (#13764)
* In de locatiebalk van Google Chrome worden suggestiebedieningen (overschakelen naar tabblad, suggestie verwijderen, enz.) nu gerapporteerd wanneer ze zijn geselecteerd. (#13522)
* Bij het opvragen van opmaakinformatie worden kleuren nu expliciet gerapporteerd in Wordpad of logviewer, in plaats van alleen "Standaardkleur". (#13959)
* In Firefox werkt het activeren van de knop "Opties tonen" op GitHub-issuepagina's nu betrouwbaar. (#14269)
* De datumkiezerbedieningen in het Outlook 2016 / 365 Geavanceerd zoekdialoogvenster rapporteren nu hun label en waarde. (#12726)
* ARIA-schakelbedieningen worden nu daadwerkelijk als schakelaars gerapporteerd in Firefox, Chrome en Edge, in plaats van als selectievakjes. (#11310)
* NVDA kondigt automatisch de sorteertoestand aan op een HTML-tabelkolomkop wanneer deze wordt gewijzigd door op een interne knop te drukken. (#10890)
* De naam van een landmark of regio wordt altijd automatisch uitgesproken bij het springen van buitenaf naar binnen met behulp van snelle navigatie of focus in browse-modus. (#13307)
* Wanneer pieptonen of aankondigingen voor 'cap' voor hoofdletters zijn ingeschakeld met vertraagde tekenbeschrijvingen, piept of kondigt NVDA niet langer 'cap' twee keer aan. (#14239)
* Besturingselementen in tabellen in Java-toepassingen worden nu nauwkeuriger aangekondigd door NVDA. (#14347)
* Sommige instellingen zijn niet langer onverwacht verschillend bij gebruik met meerdere profielen. (#14170)
  * De volgende instellingen zijn aangepakt:
    * Lijninspringing in Documentopmaakinstellingen.
    * Celranden in documentopmaakinstellingen
    * Berichten in braille-instellingen
    * Koppel Braille in braille-instellingen
  * In enkele zeldzame gevallen kunnen deze instellingen in profielen onverwacht worden gewijzigd bij het installeren van deze versie van NVDA.
  * Controleer deze opties in je profielen na het upgraden naar deze versie van NVDA.
* Emoji's worden nu in meer talen gerapporteerd. (#14433)
* De aanwezigheid van een annotatie ontbreekt niet langer in braille voor sommige elementen. (#13815)
* Een probleem opgelost waarbij configuratiewijzigingen niet correct werden opgeslagen bij het wisselen tussen een "Standaard" optie en de waarde van de "Standaard" optie. (#14133)
* Bij het configureren van NVDA is er altijd minstens één toets gedefinieerd als een NVDA-toets. (#14527)
* Bij toegang tot het NVDA-menu via het meldingsgebied zal NVDA geen wachtende update meer voorstellen wanneer er geen update beschikbaar is. (#14523)
* Rest-, verstreken en totale tijd wordt nu correct gerapporteerd voor audiobestanden die langer dan een dag zijn in foobar2000. (#14127)
* In webbrowsers zoals Chrome en Firefox worden waarschuwingen zoals bestandsdownloads in braille weergegeven naast gesproken aankondigingen. (#14562)
* Een bug opgelost bij het navigeren naar de eerste en laatste kolom in een tabel in Firefox. (#14554)
* Wanneer NVDA wordt gestart met de parameter `--lang=Windows`, is het weer mogelijk om het Algemene instellingen-dialoogvenster van NVDA te openen. (#14407)
* NVDA stopt niet langer met lezen in Kindle voor PC na het omslaan van de pagina. (#14390)

### Veranderingen voor ontwikkelaars (niet vertaald)

Note: this is an Add-on API compatibility breaking release.
Add-ons will need to be re-tested and have their manifest updated.
Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* System tests should now pass when run locally on non-English systems. (#13362)
* In Windows 11 on ARM, x64 apps are no longer identified as ARM64 applications. (#14403)
* It is no longer necessary to use `SearchField` and `SuggestionListItem` `UIA` `NVDAObjects` in new UI Automation scenarios, where automatic reporting of search suggestions, and where typing has been exposed via UI Automation with the `controllerFor` pattern.
This functionality is now available generically via `behaviours.EditableText` and the base `NVDAObject` respectively. (#14222)
* The UIA debug logging category when enabled now produces significantly more logging for UIA event handlers and utilities. (#14256)
* NVDAHelper build standards updated. (#13072)
  * Now uses the C++20 standard, was C++17.
  * Now uses the `/permissive-` compiler flag which disables permissive behaviors, and sets the `/Zc` compiler options for strict conformance.
* Some plugin objects (e.g. drivers and add-ons) now have a more informative description in the NVDA python console. (#14463)
* NVDA can now be fully compiled with Visual Studio 2022, no longer requiring the Visual Studio 2019 build tools. (#14326)
* More detailed logging for NVDA freezes to aid debugging. (#14309)
* The singleton `braille._BgThread` class has been replaced with `hwIo.ioThread.IoThread`. (#14130)
  * A single instance `hwIo.bgThread` (in NVDA core) of this class provides background i/o for thread safe braille display drivers.
  * This new class is not a singleton by design, add-on authors are encouraged to use their own instance when doing hardware i/o.
* The processor architecture for the computer can be queried from `winVersion.WinVersion.processorArchitecture attribute.` (#14439)
* New extension points have been added. (#14503)
  * `inputCore.decide_executeGesture`
  * `tones.decide_beep`
  * `nvwave.decide_playWaveFile`
  * `braille.pre_writeCells`
  * `braille.filter_displaySize`
  * `braille.decide_enabled`
  * `braille.displayChanged`
  * `braille.displaySizeChanged`
* It is possible to set useConfig to False on supported settings for a synthesizer driver. (#14601)

#### API Breaking Changes

These are breaking API changes.
Please open a GitHub issue if your Add-on has an issue with updating to the new API.

* The configuration specification has been altered, keys have been removed or modified:
  * In `[documentFormatting]` section (#14233):
    * `reportLineIndentation` stores an int value (0 to 3) instead of a boolean
    * `reportLineIndentationWithTones` has been removed.
    * `reportBorderStyle` and `reportBorderColor` have been removed and are replaced by `reportCellBorders`.
  * In `[braille]` section (#14233):
    * `noMessageTimeout` has been removed, replaced by a value for `showMessages`.
    * `messageTimeout` cannot take the value 0 anymore, replaced by a value for `showMessages`.
    * `autoTether` has been removed; `tetherTo` can now take the value "auto" instead.
  * In `[keyboard]` section  (#14528):
    * `useCapsLockAsNVDAModifierKey`, `useNumpadInsertAsNVDAModifierKey`, `useExtendedInsertAsNVDAModifierKey` have been removed.
    They are replaced by `NVDAModifierKeys`.
* The `NVDAHelper.RemoteLoader64` class has been removed with no replacement. (#14449)
* The following functions in `winAPI.sessionTracking` are removed with no replacement. (#14416, #14490)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`
* It is no longer possible to enable/disable the braille handler by setting `braille.handler.enabled`.
To disable the braille handler programatically, register a handler to `braille.handler.decide_enabled`. (#14503)
* It is no longer possible to update the display size of the handler by setting `braille.handler.displaySize`.
To update the displaySize programatically, register a handler to `braille.handler.filter_displaySize`.
Refer to `brailleViewer` for an example on how to do this. (#14503)
* There have been changes to the usage of `addonHandler.Addon.loadModule`. (#14481)
  * `loadModule` now expects dot as a separator, rather than backslash.
  For example "lib.example" instead of "lib\example".
  * `loadModule` now raises an exception when a module can't be loaded or has errors, instead of silently returning `None` without giving information about the cause.
* The following symbols have been removed from `appModules.foobar2000` with no direct replacement. (#14570)
  * `statusBarTimes`
  * `parseIntervalToTimestamp`
  * `getOutputFormat`
  * `getParsingFormat`
* The following are no longer singletons - their get method has been removed.
Usage of `Example.get()` is now `Example()`. (#14248)
  * `UIAHandler.customAnnotations.CustomAnnotationTypesCommon`
  * `UIAHandler.customProps.CustomPropertiesCommon`
  * `NVDAObjects.UIA.excel.ExcelCustomProperties`
  * `NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes`

#### Deprecations

* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA` is deprecated and usage is discouraged. (#14047)
* `config.addConfigDirsToPythonPackagePath` has been moved.
Use `addonHandler.packaging.addDirsToPythonPackagePath` instead. (#14350)
* `braille.BrailleHandler.TETHER_*` are deprecated.
Use `configFlags.TetherTo.*.value` instead. (#14233)
* `utils.security.postSessionLockStateChanged` is deprecated.
Use `utils.security.post_sessionLockStateChanged` instead. (#14486)
* `NVDAObject.hasDetails`, `NVDAObject.detailsSummary`, `NVDAObject.detailsRole` has been deprecated.
Use `NVDAObject.annotations` instead. (#14507)
* `keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS` is deprecated with no direct replacement.
Consider using the class `config.configFlags.NVDAKey` instead. (#14528)
* `gui.MainFrame.evaluateUpdatePendingUpdateMenuItemCommand` has been deprecated.
Use `gui.MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand` instead. (#14523)

## 2022.4

Deze release bevat verschillende nieuwe toetscommando's, waaronder Alles lezen commando's voor tabellen.
Er is een sectie "Snelstartgids" toegevoegd aan de gebruikershandleiding.
Er zijn ook verschillende bugfixes.

eSpeak is bijgewerkt en LibLouis is bijgewerkt.
Er zijn nieuwe Chinese, Zweedse, Luganda en Kinyarwanda brailletabellen.

### Nieuwe functies

* Een sectie "Snelstartgids" toegevoegd aan de gebruikershandleiding. (#13934)
* Een nieuwe opdracht toegevoegd om de sneltoets van de huidige focus te controleren. (#13960)
  * Desktop: `shift+numpad2`.
  * Laptop: `NVDA+ctrl+shift+.`.
* Nieuwe commando's toegevoegd om de leescursor per pagina te verplaatsen, waar ondersteund door de applicatie. (#14021)
  * Ga naar de vorige pagina:
    * Desktop: `NVDA+pageUp`.
    * Laptop: `NVDA+shift+pageUp`.
  * Ga naar de volgende pagina:
    * Desktop: `NVDA+pageDown`.
    * Laptop: `NVDA+shift+pageDown`.
* De volgende tabelopdrachten toegevoegd. (#14070)
  * Alles lezen in kolom: `NVDA+control+alt+pijl omlaag`
  * Alles lezen in rij: `NVDA+control+alt+rightArrow`
  * Lees hele kolom: `NVDA+control+alt+pijl omhoog`
  * Lees hele rij: `NVDA+control+alt+linkerpijl`
* Microsoft Excel via UI-automatisering: NVDA Meldt nu  het verlaten van een tabel binnen een spreadsheet. (#14165)
* Het melden van tabelkoppen kan nu afzonderlijk worden geconfigureerd voor rijen en kolommen. (#14075)

### Veranderingen

* eSpeak NG is bijgewerkt naar 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Rapportage van Latijnse karakters bij gebruik van Mandarijn opgelost. (#12952, #13572, #14197)
* LibLouis braillevertaler Bijgewerkt naar [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Brailletabellen toegevoegd:
    * Chinese gewone braille (vereenvoudigde Chinese karakters)
    * Kinyarwanda literaire braille
    * Luganda literaire braille
    * Zweeds niet-samengetrokken braille
    * Zweeds gedeeltelijk samengetrokken braille
    * Zweeds contract braille
    * Chinees (China, Mandarijn) huidig braillesysteem (geen tonen) (#14138)
* NVDA neemt nu de architectuur van het besturingssysteem mee bij het bijhouden van gebruikersstatistieken. (#14019)

### Opgeloste problemen

* Bij het updaten van NVDA met behulp van de Windows Package Manager CLI (ook wel winget genoemd), wordt een uitgebrachte versie van NVDA niet langer altijd als nieuwer behandeld dan de geïnstalleerde alfaversie. (#12469)
* NVDA kondigt nu correct Groepsboxen aan in Java-toepassingen. (#13962)
* De cursor volgt de gesproken tekst correct tijdens "alles lezen in toepassingen zoals Bookworm, WordPad of de NVDA-logviewer. (#13420, #9179)
* In programma's die UI-automatisering gebruiken, worden gedeeltelijk aangevinkte selectievakjes correct gerapporteerd. (#13975)
* Verbeterde prestaties en stabiliteit in Microsoft Visual Studio, Windows Terminal en andere op UI Automation gebaseerde applicaties. (#11077, #11209)
  * Deze fixes zijn van toepassing op Windows 11 Sun Valley 2 (versie 22H2) en hoger.
  * Selectieve registratie voor UI Automation-gebeurtenissen en eigenschapswijzigingen nu standaard ingeschakeld.
* Tekstrapportage, braille-uitvoer en wachtwoordonderdrukking werken nu zoals verwacht in het ingebouwde Windows Terminal-besturingselement in Visual Studio 2022. (#14194)
* NVDA is nu DPI-bewust bij gebruik van meerdere monitoren.
Er zijn verschillende oplossingen voor het gebruik van een DPI-instelling hoger dan 100% of meerdere monitoren.
Er kunnen nog steeds problemen optreden met versies van Windows ouder dan Windows 10 1809.
Om deze fixes te laten werken, moeten applicaties waarmee NVDA communiceert ook DPI-bewust zijn.
Let op: er zijn nog steeds bekende problemen met Chrome en Edge. (#13254)
  * Visuele markeringskaders moeten nu in de meeste toepassingen correct worden geplaatst. (#13370, #3875, #12070)
  * Interactie met het aanraakscherm zou nu nauwkeurig moeten zijn voor de meeste toepassingen. (#7083)
  * Muis volgen zou nu voor de meeste applicaties moeten werken. (#6722)
* Veranderingen in de oriëntatiestatus (liggend/portret) worden nu correct genegeerd als er geen verandering is (bijv. monitorveranderingen). (#14035)
* NVDA kondigt het slepen van items op het scherm aan op plaatsen zoals het herschikken van Windows 10 Start-menutegels en virtuele desktops in Windows 11. (#12271, #14081)
* In geavanceerde instellingen wordt de optie "Speel een geluid af voor gelogde fouten" nu correct hersteld naar de standaardwaarde wanneer op de knop "Standaardinstellingen herstellen" wordt gedrukt. (#14149)
* NVDA kan nu tekst selecteren met behulp van de sneltoets `NVDA+f10` in Java-toepassingen. (#14163)
* NVDA blijft niet langer vastzitten in een menu bij het omhoog en omlaag bewegen van conversaties in Microsoft Teams. (#14355)

### Veranderingen voor ontwikkelaars (niet vertaald)

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* The [NVDA API Announcement mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) was created. (#13999)
* NVDA no longer processes `textChange` events for most UI Automation applications due to their extreme negative performance impact. (#11002, #14067)

#### Deprecations

* `core.post_windowMessageReceipt` is deprecated, use `winAPI.messageWindow.pre_handleWindowMessage` instead.
* `winKernel.SYSTEM_POWER_STATUS` is deprecated and usage is discouraged, this has been moved to `winAPI._powerTracking.SystemPowerStatus`.
* `winUser.SM_*` constants are deprecated, use `winAPI.winUser.constants.SystemMetrics` instead.

## 2022.3.3

Dit is een kleine release om problemen met 2022.3.2, 2022.3.1 en 2022.3 op te lossen.
Deze release behandelt ook een beveiligingsprobleem.

### Beveiligingsoplossingen

* Voorkomt mogelijke systeemtoegang (bijv. NVDA Python-console) voor niet-geverifieerde gebruikers.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Opgeloste problemen

* Opgelost: wanneer NVDA vastloopt tijdens het vergrendelen, geeft NVDA toegang tot het bureaublad van de gebruiker terwijl het zich op het Windows-vergrendelscherm bevindt. (#14416)
* Opgelost: wanneer NVDA vastloopt tijdens het vergrendelen, functioneert NVDA niet correct, alsof het apparaat nog steeds vergrendeld is. (#14416)
* Opgeloste toegankelijkheidsproblemen met het Windows "wachtwoord vergeten"-proces en de Windows update/installatie-ervaring. (#14368)
* Opgelost probleem bij het proberen te installeren van NVDA in sommige Windows-omgevingen, zoals Windows Server. (#14379)

### Veranderingen voor ontwikkelaars (niet vertaald)

#### Deprecations

* `utils.security.isObjectAboveLockScreen(obj)` is deprecated, instead use `obj.isBelowLockScreen`. (#14416)
* The following functions in `winAPI.sessionTracking` are deprecated for removal in 2023.1. (#14416)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`

## 2022.3.2

Dit is een kleine release om regressies in 2022.3.1 op te lossen en een beveiligingsprobleem aan te pakken.

### Beveiligingsoplossingen

* Voorkomt mogelijke systeemtoegang voor niet-geverifieerde gebruikers.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Opgeloste problemen

* Oplossing voor een regressie in 2022.3.1 waarbij bepaalde functionaliteiten waren uitgeschakeld op beveiligde schermen. (#14286)
* Oplossing voor een regressie in 2022.3.1 waarbij bepaalde functionaliteiten waren uitgeschakeld na het inloggen, als NVDA was gestart op het vergrendelscherm. (#14301)

## 2022.3.1

Dit is een kleine release om meerdere beveiligingsproblemen op te lossen.
Beveiligingsproblemen kunnen vertrouwelijk worden gemeld via <info@nvaccess.org>.

### Beveiligingsoplossingen

* Opgelost: exploit waarmee het mogelijk was om van gebruikers- naar systeemrechten te escaleren.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Opgelost: beveiligingsprobleem waarbij toegang tot de Python-console mogelijk was op het vergrendelscherm via een race condition bij het opstarten van NVDA.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Opgelost: probleem waarbij de tekst in de spraakviewer werd gecachet bij het vergrendelen van Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Opgeloste problemen

* Voorkom dat een niet-geverifieerde gebruiker instellingen voor de spraak- en brailleviewer kan aanpassen op het vergrendelscherm. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Een aanzienlijk deel van deze release is bijgedragen door de NVDA-ontwikkelingsgemeenschap.
Dit omvat uitgestelde karakterbeschrijvingen en verbeterde ondersteuning voor Windows Console.

Deze release bevat ook verschillende foutoplossingen.
Met name zullen recente versies van Adobe Acrobat/Reader niet meer crashen bij het lezen van een PDF-document.

eSpeak is bijgewerkt en introduceert 3 nieuwe talen: Wit-Russisch, Luxemburgs en Totontepec Mixe.

### Nieuwe functies

* In de Windows Console Host gebruikt door Opdrachtprompt, PowerShell en het Windows-subsysteem voor Linux op Windows 11 versie 22H2 (Sun Valley 2) en later:
  * Sterk verbeterde prestaties en stabiliteit. (#10964)
  * Bij het indrukken van `control+f` om tekst te zoeken, wordt de positie van de reviewcursor bijgewerkt om de gevonden term te volgen. (#11172)
  * Het rapporteren van getypte tekst die niet op het scherm verschijnt (zoals wachtwoorden) is standaard uitgeschakeld.
Het kan worden ingeschakeld in het geavanceerde instellingenpaneel van NVDA. (#11554)
  * Tekst die van het scherm is gescrold, kan worden doorgelezen zonder het consolevenster te scrollen. (#12669)
  * Meer gedetailleerde informatie over tekstopmaak is beschikbaar. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Een nieuwe spraakoptie is toegevoegd om na een vertraging karakterbeschrijvingen te lezen. (#13509)
* Een nieuwe brailleoptie is toegevoegd om te bepalen of het scrollen van het scherm naar voren/achteren de spraak moet onderbreken. (#2124)

### Veranderingen

* eSpeak NG is bijgewerkt naar 1.52-dev commit `9de65fcb`. (#13295)
  * Toegevoegde talen:
    * Wit-Russisch
    * Luxemburgs
    * Totontepec Mixe
* Bij gebruik van UI Automation om toegang te krijgen tot Microsoft Excel-spreadsheetbesturingselementen, kan NVDA nu melden wanneer een cel is samengevoegd. (#12843)
* In plaats van "heeft details" wordt, waar mogelijk, het doel van de details vermeld, bijvoorbeeld "heeft opmerking". (#13649)
* De installatiegrootte van NVDA wordt nu weergegeven in het gedeelte Programma's en Onderdelen van Windows. (#13909)

### Opgeloste problemen

* Adobe Acrobat / Reader 64-bits crasht niet meer bij het lezen van een PDF-document. (#12920)
  * Opmerking: de meest recente versie van Adobe Acrobat / Reader is ook vereist om de crash te voorkomen.
* Lettergroottemetingen zijn nu vertaalbaar in NVDA. (#13573)
* Negeer Java Access Bridge-evenementen waarbij geen vensterhandle kan worden gevonden voor Java-toepassingen.
Dit zal de prestaties verbeteren voor sommige Java-toepassingen, waaronder IntelliJ IDEA. (#13039)
* Aankondiging van geselecteerde cellen voor LibreOffice Calc is efficiënter en resulteert niet langer in een Calc-bevriezing wanneer veel cellen zijn geselecteerd. (#13232)
* Bij uitvoering onder een andere gebruiker is Microsoft Edge niet langer ontoegankelijk. (#13032)
* Wanneer snelheidsboost is uitgeschakeld, daalt de snelheid van eSpeak niet meer tussen 99% en 100%. (#13876)
* Fout opgelost die het mogelijk maakte om twee invoergebaarvensters te openen. (#13854)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Updated Comtypes to version 1.1.11. (#12953)
* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * This can be overridden by changing the "Windows Console support" setting in NVDA's advanced settings panel.
  * To find your Windows Console's NVDA API level, set "Windows Console support" to "UIA when available", then check the NVDA+F1 log opened from a running Windows Console instance.
* The Chromium virtual buffer is now loaded even when the document object has the MSAA `STATE_SYSTEM_BUSY` exposed via IA2. (#13306)
* A config spec type `featureFlag` has been created for use with experimental features in NVDA. See `devDocs/featureFlag.md` for more information. (#13859)

#### Deprecations

There are no deprecations proposed in 2022.3.

## 2022.2.4

Dit is een patch-release om een beveiligingsprobleem op te lossen.

### Opgeloste problemen

* Exploit opgelost waarbij het mogelijk was om de NVDA Python-console te openen via de logviewer op het vergrendelscherm.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Dit is een patch-release om een onbedoelde API-breuk te herstellen die was geïntroduceerd in 2022.2.1.

### Opgeloste problemen

* Fout opgelost waarbij NVDA niet "Veilig bureaublad" aankondigde bij het openen van een veilig bureaublad.
Dit zorgde ervoor dat NVDA Remote geen veilige bureaubladen herkende. (#14094)

## 2022.2.2

Dit is een patch-release om een fout op te lossen die in 2022.2.1 is geïntroduceerd met invoergebaren.

### Opgeloste problemen

* Fout opgelost waarbij invoergebaren niet altijd werkten. (#14065)

## 2022.2.1

Dit is een kleine release om een beveiligingsprobleem op te lossen.
Meld beveiligingsproblemen op verantwoorde wijze aan <info@nvaccess.org>.

### Beveiligingsoplossingen

* Exploit opgelost waarbij het mogelijk was om een Python-console uit te voeren vanaf het vergrendelscherm. (GHSA-rmq3-vvhq-gp32)
* Exploit opgelost waarbij het mogelijk was om via objectnavigatie het vergrendelscherm te omzeilen. (GHSA-rmq3-vvhq-gp32)

### Veranderingen voor ontwikkelaars (niet vertaald)

#### Deprecations

These deprecations are currently not scheduled for removal.
The deprecated aliases will remain until further notice.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModules.lockapp.LockAppObject` should be replaced with `NVDAObjects.lockscreen.LockScreenObject`. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS` should be replaced with `utils.security.getSafeScripts()`. (GHSA-rmq3-vvhq-gp32)

## 2022.2

Deze release bevat veel bugfixes.
Opvallend zijn de aanzienlijke verbeteringen voor Java-gebaseerde applicaties, brailleleesregels en Windows-functies.

Nieuwe tabelnavigatieopdrachten zijn geïntroduceerd.
Unicode CLDR is bijgewerkt.
LibLouis is bijgewerkt, wat een nieuwe Duitse brailletabel bevat.

### Nieuwe functies

* Ondersteuning voor interactie met Microsoft Loop-componenten in Microsoft Office-producten. (#13617)
* Nieuwe tabelnavigatieopdrachten toegevoegd. (#957)
 * `control+alt+home/end` om naar de eerste/laatste kolom te springen.
 * `control+alt+pageUp/pageDown` om naar de eerste/laatste rij te springen.
* Een niet toegewezen opdracht om te wisselen tussen taal- en dialectwisselmodi is toegevoegd. (#10253)

### Veranderingen

* NSIS is bijgewerkt naar versie 3.08. (#9134)
* CLDR is bijgewerkt naar versie 41.0. (#13582)
* Bijgewerkte LibLouis braillevertaler naar [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nieuwe brailletabel: Duitse graad 2 (gedetailleerd)
* Nieuwe rol toegevoegd voor "bezigheidsindicator"-besturingselementen. (#10644)
* NVDA kondigt nu aan wanneer een NVDA-actie niet kan worden uitgevoerd. (#13500)
  * Dit omvat wanneer:
    * De NVDA Windows Store-versie wordt gebruikt.
    * In een beveiligde context.
    * Wachten op een antwoord op een modaal dialoogvenster.

### Opgeloste problemen

* Oplossingen voor Java-gebaseerde applicaties:
  * NVDA kondigt nu de alleen-lezen-status aan. (#13692)
  * NVDA kondigt nu de uitgeschakelde/ingeschakelde status correct aan. (#10993)
  * NVDA kondigt nu functietoets-snelkoppelingen aan. (#13643)
  * NVDA kan nu een pieptoon laten horen of spreken bij voortgangsbalken. (#13594)
  * NVDA verwijdert niet langer ten onrechte tekst uit widgets wanneer deze aan de gebruiker worden gepresenteerd. (#13102)
  * NVDA kondigt nu de status van schakelaars aan. (#9728)
  * NVDA herkent nu het venster in een Java-applicatie met meerdere vensters. (#9184)
  * NVDA kondigt nu positie-informatie aan voor tabbladen. (#13744)
* Braille-oplossingen:
  * Oplossing voor braille-uitvoer bij het navigeren door bepaalde tekst in Mozilla rich edit-controls, zoals bij het opstellen van een bericht in Thunderbird. (#12542)
  * Wanneer braille automatisch verankerd is en de muis wordt verplaatst met ingeschakelde muistracking,
   worden tekstreviewopdrachten nu weergegeven op de brailleleesregel met de gesproken inhoud. (#11519)
  * Het is nu mogelijk om door de inhoud te bladeren op de brailleleesregel na het gebruik van tekstrecensieopdrachten. (#8682)
* De NVDA-installatie kan nu worden uitgevoerd vanuit mappen met speciale tekens. (#13270)
* In Firefox meldt NVDA niet langer geen items op webpagina's wanneer aria-rowindex, aria-colindex, aria-rowcount of aria-colcount attributen ongeldig zijn. (#13405)
* De cursor schakelt niet langer van rij of kolom wanneer wordt genavigeerd door samengevoegde cellen met tabelnavigatie. (#7278)
* Bij het lezen van niet-interactieve PDF's in Adobe Reader worden het type en de status van formuliervelden (zoals selectievakjes en keuzerondjes) nu gemeld. (#13285)
* "Configuratie terugzetten naar fabrieksinstellingen" is nu toegankelijk in het NVDA-menu tijdens de beveiligde modus. (#13547)
* Eventuele vergrendelde muisknoppen worden ontgrendeld wanneer NVDA afsluit; voorheen bleef de muisknop vergrendeld. (#13410)
* Visual Studio meldt nu regelnummers. (#13604)
  * Let op dat voor het rapporteren van regelnummers het weergeven van regelnummers moet zijn ingeschakeld in zowel Visual Studio als NVDA.
* Visual Studio meldt nu correct de inspringing van regels. (#13574)
* NVDA kondigt opnieuw de details van zoekresultaten in het Startmenu aan in recente releases van Windows 10 en 11. (#13544)
* In Windows 10 en 11 Calculator versie 10.1908 en later,
kondigt NVDA resultaten aan wanneer er meer opdrachten worden gegeven, zoals opdrachten in de wetenschappelijke modus. (#13383)
* In Windows 11 is het opnieuw mogelijk om te navigeren en te communiceren met gebruikersinterface-elementen,
zoals de taakbalk en Taakweergave met behulp van muis- en aanraakinteracties. (#13506)
* NVDA kondigt de inhoud van de statusbalk aan in Windows 11 Kladblok. (#13688)
* Het navigatieobject wordt nu onmiddellijk gemarkeerd bij het activeren van de functie. (#13641)
* Oplossing voor het lezen van items in lijstweergaven met één kolom. (#13659, #13735)
* Oplossing voor automatische taalwisselproblemen bij eSpeak voor Engels en Frans, waarbij werd teruggevallen op Brits Engels en Frans (Frankrijk). (#13727)
* Oplossing voor automatische taalwisselproblemen bij OneCore wanneer geprobeerd werd over te schakelen naar een eerder geïnstalleerde taal. (#13732)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Compiling NVDA dependencies with Visual Studio 2022 (17.0) is now supported.
For development and release builds, Visual Studio 2019 is still used. (#13033)
* When retrieving the count of selected children via accSelection,
the case where a negative child ID or an IDispatch is returned by `IAccessible::get_accSelection` is now handled properly. (#13277)
* New convenience functions `registerExecutableWithAppModule` and `unregisterExecutable` were added to the `appModuleHandler` module.
They can be used to use a single App Module with multiple executables. (#13366)

#### Deprecations

These are proposed API breaking changes.
The deprecated part of the API will continue to be available until the specified release.
If no release is specified, the plan for removal has not been determined.
Note, the roadmap for removals is 'best effort' and may be subject to change.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModuleHandler.NVDAProcessID` is deprecated, use `globalVars.appPid` instead. (#13646)
* `gui.quit` is deprecated, use `wx.CallAfter(mainFrame.onExitCommand, None)` instead. (#13498)
  -
* Some alias appModules are marked as deprecated.
Code which imports from one of them, should instead import from the replacement module.  (#13366)

| Removed module name |Replacement module|
|---|---|
|azuredatastudio |code|
|azuredatastudio-insiders |code|
|calculatorapp |calculator|
|code - insiders |code|
|commsapps |hxmail|
|dbeaver |eclipse|
|digitaleditionspreview |digitaleditions|
|esybraille |esysuite|
|hxoutlook |hxmail|
|miranda64 |miranda32|
|mpc-hc |mplayerc|
|mpc-hc64 |mplayerc|
|notepad++ |notepadPlusPlus|
|searchapp |searchui|
|searchhost |searchui|
|springtoolsuite4 |eclipse|
|sts |eclipse|
|teamtalk3 |teamtalk4classic|
|textinputhost |windowsinternal_composableshell_experiences_textinput_inputapp|
|totalcmd64 |totalcmd|
|win32calc |calc|
|winmail |msimn|
|zend-eclipse-php |eclipse|
|zendstudio |eclipse|

## 2022.1

Deze release bevat grote verbeteringen in de ondersteuning van UIA in MS Office.
Voor Microsoft Office 16.0.15000 en hoger op Windows 11 gebruikt NVDA standaard UI Automation om toegang te krijgen tot Microsoft Word-documenten.
Dit zorgt voor een aanzienlijke prestatieverbetering ten opzichte van het oude Object Model-toegang.

Er zijn verbeteringen aangebracht in brailleleesregel-stuurprogramma's, waaronder Seika Notetaker, Papenmeier en HID Braille.
Ook zijn er verschillende oplossingen voor Windows 11, voor apps zoals Rekenmachine, Console, Terminal, Mail en Emoji Paneel.

eSpeak-NG en LibLouis zijn bijgewerkt, met nieuwe Japanse, Duitse en Catalaanse tabellen.

Opmerking:

 * Deze release maakt bestaande add-ons incompatibel.

### Nieuwe functies

* Ondersteuning voor het rapporteren van notities in MS Excel met UI Automation ingeschakeld op Windows 11. (#12861)
* In recente versies van Microsoft Word via UI Automation op Windows 11 worden de aanwezigheid van bladwijzers, conceptopmerkingen en opgeloste opmerkingen nu gemeld in zowel spraak als braille. (#12861)
* De nieuwe opdrachtregelparameter `--lang` maakt het mogelijk om de geconfigureerde NVDA-taal te overschrijven. (#10044)
* NVDA waarschuwt nu voor opdrachtregelparameters die onbekend zijn en niet door add-ons worden gebruikt. (#12795)
* In Microsoft Word via UI Automation maakt NVDA nu gebruik van MathPlayer om wiskundige vergelijkingen te lezen en te navigeren. (#12946)
  * Hiervoor moet Microsoft Word 365/2016 build 14326 of later worden uitgevoerd.
  * MathType-vergelijkingen moeten handmatig worden geconverteerd naar Office Math door elk te selecteren, het contextmenu te openen, de optie Vergelijking te kiezen en vervolgens naar Office Math om te zetten.
* Rapportage van "heeft details" en de bijbehorende opdracht om de detailsrelatie samen te vatten, is bijgewerkt om te werken in focusmodus. (#13106)
* Seika Notetaker kan nu automatisch worden gedetecteerd wanneer verbonden via USB en Bluetooth. (#13191, #13142)
  * Dit betreft de volgende apparaten: MiniSeika (16, 24 cellen), V6, en V6Pro (40 cellen).
  * Het handmatig selecteren van de Bluetooth COM-poort wordt nu ook ondersteund.
* Een opdracht toegevoegd om de brailleviewer in- of uit te schakelen; er is geen standaardgebaar toegewezen. (#13258)
* Opdrachten toegevoegd voor het gelijktijdig inschakelen van meerdere modi met een brailleleesregel. (#13152)
* Het Spraakwoordenboekvenster heeft nu een knop "Alles verwijderen" om een heel woordenboek te wissen. (#11802)
* Ondersteuning toegevoegd voor de Windows 11 Rekenmachine. (#13212)
* In Microsoft Word met UI Automation ingeschakeld op Windows 11 kunnen nu regelnummers en sectienummers worden gemeld. (#13283, #13515)
* Voor Microsoft Office 16.0.15000 en hoger op Windows 11 gebruikt NVDA standaard UI Automation om toegang te krijgen tot Microsoft Word-documenten, wat een aanzienlijke prestatieverbetering biedt ten opzichte van de oude Object Model-toegang. (#13437)
 * Dit geldt voor documenten in Microsoft Word zelf, en ook voor de berichtlezer en -componist in Microsoft Outlook.

### Veranderingen

* Espeak-ng is bijgewerkt naar 1.51-dev commit `7e5457f91e10`. (#12950)
* Bijgewerkte LibLouis braillevertaler naar [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Nieuwe brailletabel toegevoegd: Japanse (Kantenji) literaire braille.
  * Nieuwe Duitse 6-punt computerbrailletabel toegevoegd.
  * Catalaanse graad 1 brailletabel toegevoegd. (#13408)
* NVDA meldt selectie en samengevoegde cellen in LibreOffice Calc 7.3 en hoger. (#9310, #6897)
* Unicode Common Locale Data Repository (CLDR) bijgewerkt naar 40.0. (#12999)
* `NVDA+Numpad Delete` meldt standaard de locatie van de cursor of het gefocuste object. (#13060)
* `NVDA+Shift+Numpad Delete` meldt de locatie van de recensie-cursor. (#13060)
* Standaardkoppelingen toegevoegd voor het in-/uitschakelen van functietoetsen op Freedom Scientific displays. (#13152)
* "Basislijn" wordt niet langer gemeld via de opdracht "Tekstopmaak rapporteren" (`NVDA+f`). (#11815)
* De opdracht "Lange beschrijving activeren" heeft geen standaardgebaar meer toegewezen. (#13380)
* De opdracht "Samenvatting van details rapporteren" heeft nu een standaardgebaar (`NVDA+d`). (#13380)
* NVDA moet opnieuw worden gestart na het installeren van MathPlayer. (#13486)

### Opgeloste problemen

* Het Klembordbeheer-paneel steelt niet langer onterecht de focus bij het openen van sommige Office-programma's. (#12736)
* Op een systeem waarbij de gebruiker ervoor heeft gekozen om de primaire muisknop van links naar rechts te wisselen, brengt NVDA niet langer per ongeluk een contextmenu naar voren in plaats van een item te activeren, in applicaties zoals webbrowsers. (#12642)
* Wanneer de recensie-cursor voorbij het einde van tekstvelden beweegt, zoals in Microsoft Word met UI Automation, wordt "onderkant" correct gemeld in meer situaties. (#12808)
* NVDA kan de naam en versie van de applicatie melden voor binaries in system32 bij gebruik van een 64-bits versie van Windows. (#12943)
* Consistentie van uitvoer bij het lezen van terminalprogramma's verbeterd. (#12974)
  * In sommige situaties, wanneer tekens worden ingevoegd of verwijderd in het midden van een regel, kunnen de tekens na de cursor opnieuw worden voorgelezen.
* MS Word met UIA: navigeren door koppen in browse-modus blijft niet langer vastzitten op de laatste kop van een document en deze kop wordt ook niet tweemaal weergegeven in de NVDA-elementenlijst. (#9540)
* In Windows 8 en later kan de statusbalk van Verkenner nu worden opgevraagd met het standaardgebaar NVDA+end (desktop) / NVDA+shift+end (laptop). (#12845)
* Binnenkomende berichten in de chat van Skype for Business worden opnieuw gemeld. (#9295)
* NVDA kan opnieuw audio dempen wanneer de SAPI5-synthesizer wordt gebruikt op Windows 11. (#12913)
* In de Rekenmachine van Windows 10 kondigt NVDA de labels voor geschiedenis- en geheugenlijstitems aan. (#11858)
* Gebaren zoals scrollen en routeren werken weer met HID-braille-apparaten. (#13228)
* Windows 11 Mail: na het wisselen van focus tussen apps, terwijl je een lang e-mailbericht leest, blijft NVDA niet langer hangen op een regel van de e-mail. (#13050)
* HID-braille: gechordde gebaren (bijv. `spatie+punt4`) kunnen met succes worden uitgevoerd vanaf de brailleleesregel. (#13326)
* Een probleem opgelost waarbij meerdere instellingenvensters tegelijkertijd konden worden geopend. (#12818)
* Een probleem opgelost waarbij sommige Focus Blue-brailleleesregels zouden stoppen met werken na het ontwaken van de computer uit slaapstand. (#9830)
* "Basislijn" wordt niet langer onterecht gemeld wanneer de optie "superscript en subscript rapporteren" actief is. (#11078)
* In Windows 11 voorkomt NVDA dat navigatie in het emoji-paneel wordt geblokkeerd bij het selecteren van emoji's. (#13104)
* Een bug opgelost waardoor dubbele rapportage ontstond bij gebruik van Windows Console en Terminal. (#13261)
* Meerdere gevallen opgelost waarin lijstitems niet konden worden gerapporteerd in 64-bits applicaties, zoals REAPER. (#8175)
* In de downloadmanager van Microsoft Edge schakelt NVDA nu automatisch over naar focusmodus zodra het lijstitem met de meest recente download de focus krijgt. (#13221)
* NVDA veroorzaakt niet langer crashes van 64-bits versies van Notepad++ 8.3 en hoger. (#13311)
* Adobe Reader crasht niet langer bij het opstarten wanneer de beveiligde modus van Adobe Reader is ingeschakeld. (#11568)
* Een bug opgelost waarbij het selecteren van de Papenmeier-brailleleesregelstuurprogramma NVDA liet crashen. (#13348)
* In Microsoft Word met UIA: paginanummers en andere opmaak worden niet langer ongepast gemeld bij het verplaatsen van een lege tabelcel naar een cel met inhoud, of van het einde van een document naar bestaande inhoud. (#13458, #13459)
* NVDA meldt de paginatitel en start niet langer automatisch met voorlezen bij het laden van een pagina in Google Chrome 100. (#13571)
* NVDA crasht niet langer bij het terugzetten van de NVDA-configuratie naar de fabrieksinstellingen terwijl de optie om toetscombinaties voor te lezen is ingeschakeld. (#13634)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Note: this is a Add-on API compatibility breaking release. Add-ons will need to be re-tested and have their manifest updated.
* Although NVDA still requires Visual Studio 2019, Builds should no longer fail if a newer version of Visual Studio (E.g. 2022) is installed along side 2019. (#13033, #13387)
* Updated SCons to version 4.3.0. (#13033)
* Updated py2exe to version 0.11.1.0. (#13510)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` has been removed. Use `apiLevel` instead. (#12955, #12660)
* `TVItemStruct` has been removed from `sysTreeView32`. (#12935)
* `MessageItem` has been removed from the Outlook appModule. (#12935)
* `audioDucking.AUDIODUCKINGMODE_*` constants are now a `DisplayStringIntEnum`. (#12926)
  * usages should be replaced with `AudioDuckingMode.*`
  * usages of `audioDucking.audioDuckingModes` should be replaced with `AudioDuckingMode.*.displayString`
* `audioDucking.ANRUS_ducking_*` constants usages should be replaced with `ANRUSDucking.*`. (#12926)
* `synthDrivers.sapi5` changes (#12927):
  * `SPAS_*` usages should be replaced with `SPAudioState.*`
  * `constants.SVSF*` usages should be replaced with `SpeechVoiceSpeakFlags.*`
    * Note: `SVSFlagsAsync` should be replaced with `SpeechVoiceSpeakFlags.Async` not `SpeechVoiceSpeakFlags.lagsAsync`
  * `constants.SVE*` usages should be replaced with `SpeechVoiceEvents.*`
* The `soffice` appModule has the following classes and functions removed `JAB_OOTableCell`, `JAB_OOTable`, `gridCoordStringToNumbers`. (#12849)
* `core.CallCancelled` is now `exceptions.CallCancelled`. (#12940)
* All constants starting with RPC from `core` and `logHandler` are moved into `RPCConstants.RPC` enum. (#12940)
* It is recommended that `mouseHandler.doPrimaryClick` and `mouseHandler.doSecondaryClick` functions should be used to click the mouse to perform a logical action such as activating (primary) or secondary (show context menu),
rather than using `executeMouseEvent` and specifying the left or right mouse button specifically.
This ensures code will honor the Windows user setting for swapping the primary mouse button. (#12642)
* `config.getSystemConfigPath` has been removed - there is no replacement. (#12943)
* `shlobj.SHGetFolderPath` has been removed - please use `shlobj.SHGetKnownFolderPath` instead. (#12943)
* `shlobj` constants have been removed. A new enum has been created, `shlobj.FolderId` for usage with `SHGetKnownFolderPath`. (#12943)
* `diffHandler.get_dmp_algo` and `diffHandler.get_difflib_algo` have been replaced with `diffHandler.prefer_dmp` and `diffHandler.prefer_difflib` respectively. (#12974)
* `languageHandler.curLang` has been removed - to get the current NVDA language use `languageHandler.getLanguage()`. (#13082)
* A `getStatusBarText` method can be implemented on an appModule to customize the way NVDA fetches the text from the status bar. (#12845)
* `globalVars.appArgsExtra` has been removed. (#13087)
  * If your add-on need to process additional command line arguments see the documentation of `addonHandler.isCLIParamKnown` and the developer guide for details.
* The UIA handler module and other UIA support modules are now part of a UIAHandler package. (#10916)
  * `UIAUtils` is now `UIAHandler.utils`
  * `UIABrowseMode` is now `UIAHandler.browseMode`
  * `_UIAConstants` is now `UIAHandler.constants`
  * `_UIACustomProps` is now `UIAHandler.customProps`
  * `_UIACustomAnnotations` is now `UIAHandler.customAnnotations`
* The `IAccessibleHandler` `IA2_RELATION_*` constants have been replaced with the `IAccessibleHandler.RelationType` enum. (#13096)
  * Removed `IA2_RELATION_FLOWS_FROM`
  * Removed `IA2_RELATION_FLOWS_TO`
  * Removed `IA2_RELATION_CONTAINING_DOCUMENT`
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` and `LOCALE_SLANGDISPLAYNAME` are removed from `languageHandler` - use members of `languageHandler.LOCALE` instead. (#12753)
* Switched from Minhook to Microsoft Detours as a hooking library for NVDA. Hooking with this library is mainly used to aid the display model. (#12964)
* `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` is removed. (#13211)
* SCons now warns to build with a number of jobs that is equal to the number of logical processors in the system.
This can dramatically decrease build times on multi core systems. (#13226, #13371)
* `characterProcessing.SYMLVL_*` constants are removed - please use `characterProcessing.SymbolLevel.*` instead. (#13248)
* Functions `loadState` and `saveState` are removed from addonHandler - please use `addonHandler.state.load` and `addonHandler.state.save` instead. (#13245)
* Moved the UWP/OneCore interaction layer of NVDAHelper [from C++/CX to C++/Winrt](https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx). (#10662)
* It is now mandatory to subclass `DictionaryDialog` to use it. (#13268)
* `config.RUN_REGKEY`, `config.NVDA_REGKEY` are deprecated, please use `config.RegistryKey.RUN`, `config.RegistryKey.NVDA` instead. These will be removed in 2023. (#13242)
* `easeOfAccess.ROOT_KEY`, `easeOfAccess.APP_KEY_PATH` are deprecated, please use`easeOfAccess.RegistryKey.ROOT`, `easeOfAccess.RegistryKey.APP` instead. These will be removed in 2023. (#13242)
* `easeOfAccess.APP_KEY_NAME` has been deprecated, to be removed in 2023. (#13242)
* `DictionaryDialog` and `DictionaryEntryDialog` are moved from `gui.settingsDialogs` to `gui.speechDict`. (#13294)
* IAccessible2 relations are now shown in developer info for IAccessible2 objects. (#13315)
* `languageHandler.windowsPrimaryLCIDsToLocaleNames` has been removed, instead use `languageHandler.windowsLCIDToLocaleName` or `winKernel.LCIDToLocaleName`. (#13342)
* `UIAAutomationId` property for UIA objects should be preferred over `cachedAutomationId`. (#13125, #11447)
  * `cachedAutomationId` can be used if obtained directly from the element.
* `NVDAObjects.window.scintilla.CharacterRangeStruct` has moved to `NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct`. (#13364)
* Boolean `gui.isInMessageBox` is removed, please use the function `gui.message.isModalMessageBoxActive` instead. (#12984, #13376)
* `controlTypes` has been split up into various submodules. (#12510, #13588)
  * `ROLE_*` and `STATE_*` have been replaced with `Role.*` and `State.*`.
  * Although still available, the following should be considered deprecated:
    * `ROLE_*` and `STATE_*`, use `Role.*` and `State.*` instead.
    * `roleLabels`, `stateLabels` and `negativeStateLabels`, usages like `roleLabels[ROLE_*]` should be replaced with their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
    * `processPositiveStates` and `processNegativeStates` should use `processAndLabelStates` instead.
* Excel cell state constants (`NVSTATE_*`) are now values in the `NvCellState` enum, mirrored in the `NvCellState` enum in `NVDAObjects/window/excel.py` and mapped to `controlTypes.State` via _nvCellStatesToStates. (#13465)
* `EXCEL_CELLINFO` struct member `state` is now `nvCellStates`.
* `mathPres.ensureInit` has been removed, MathPlayer is now initialized when NVDA starts. (#13486)

## 2021.3.5

Dit is een kleine release om een beveiligingsprobleem op te lossen.
Geef beveiligingsproblemen alstublieft op een verantwoorde manier door aan <info@nvaccess.org>.

### Beveiligingsoplossingen

* Beveiligingsadvies `GHSA-xc5m-v23f-pgr7` aangepakt.
  * De symbolen-uitspraakdialoog is nu uitgeschakeld in beveiligde modus.

## 2021.3.4

Dit is een kleine release om verschillende beveiligingsproblemen op te lossen.
Geef beveiligingsproblemen alstublieft op een verantwoorde manier door aan <info@nvaccess.org>.

### Beveiligingsoplossingen

* Beveiligingsadvies `GHSA-354r-wr4v-cx28` aangepakt. (#13488)
  * Mogelijkheid om NVDA te starten met ingeschakelde foutopsporingslogboeken is verwijderd wanneer NVDA in beveiligde modus draait.
  * Mogelijkheid om NVDA te updaten is verwijderd wanneer NVDA in beveiligde modus draait.
* Beveiligingsadvies `GHSA-wg65-7r23-h6p9` aangepakt. (#13489)
  * Mogelijkheid om de invoergebaren-dialoog te openen in beveiligde modus is verwijderd.
  * Mogelijkheid om de standaard-, tijdelijke- en spraakwoordenboeken-dialoog te openen in beveiligde modus is verwijderd.
* Beveiligingsadvies `GHSA-mvc8-5rv9-w3hx` aangepakt. (#13487)
  * Het wx GUI-inspectietool is nu uitgeschakeld in beveiligde modus.

## 2021.3.3

Deze release is identiek aan 2021.3.2.
In NVDA 2021.3.2 was er een fout waardoor het zichzelf verkeerd identificeerde als 2021.3.1.
Deze release identificeert zichzelf correct als 2021.3.3.

## 2021.3.2

Dit is een kleine release om verschillende beveiligingsproblemen op te lossen.
Geef beveiligingsproblemen alstublieft op een verantwoorde manier door aan <info@nvaccess.org>.

### Opgeloste problemen

* Beveiligingsoplossing: Voorkomen dat objectnavigatie buiten het vergrendelscherm plaatsvindt op Windows 10 en Windows 11. (#13328)
* Beveiligingsoplossing: Het beheerdersdialoogvenster voor invoegtoepassingen is nu uitgeschakeld op beveiligde schermen. (#13059)
* Beveiligingsoplossing: De NVDA-contexthulp is niet langer beschikbaar op beveiligde schermen. (#13353)

## 2021.3.1

Dit is een kleine release om verschillende problemen in 2021.3 op te lossen.

### Veranderingen

* Het nieuwe HID-brailleprotocol heeft niet langer de voorkeur wanneer een andere braille-displaystuurprogramma kan worden gebruikt. (#13153)
* Het nieuwe HID-brailleprotocol kan worden uitgeschakeld via een instelling in het geavanceerde instellingenpaneel. (#13180)

### Opgeloste problemen

* Landmark wordt weer afgekort in braille. (#13158)
* Opgelost: instabiele automatische detectie van braille-displays voor Humanware Brailliant en APH Mantis Q40 braille-displays bij gebruik van Bluetooth. (#13153)

## 2021.3

Deze release introduceert ondersteuning voor de nieuwe HID Braille-specificatie.
Deze specificatie is bedoeld om de ondersteuning voor brailleleesregels te standaardiseren zonder dat er afzonderlijke stuurprogramma's nodig zijn.
Er zijn updates voor eSpeak-NG en LibLouis, inclusief nieuwe Russische en Tshivenda-tabellen.
Geluiden bij fouten kunnen worden ingeschakeld in stabiele versies van NVDA via een nieuwe optie in geavanceerde instellingen.
Alles lezen in Word schuift nu door de weergave om de huidige positie zichtbaar te houden.
Er zijn veel verbeteringen bij het gebruik van Office met UIA.
Een UIA-oplossing is dat Outlook nu meer soorten lay-outtabellen in berichten negeert.

Belangrijke opmerkingen:

Door een update van ons beveiligingscertificaat krijgt een klein aantal gebruikers een foutmelding wanneer NVDA 2021.2 op updates controleert.
NVDA vraagt ​​Windows nu om beveiligingscertificaten bij te werken, waardoor deze fout in de toekomst wordt voorkomen.
Getroffen gebruikers moeten deze update handmatig downloaden.

### Nieuwe functies

* Voegt een invoergebaar toe voor het schakelen tussen instellingen voor het rapporteren van de stijl van celranden. (#10408)
* Ondersteuning voor de nieuwe HID Braille-specificatie die tot doel heeft de ondersteuning voor brailleleesregels te standaardiseren. (#12523)
  * Apparaten die deze specificatie ondersteunen, worden automatisch gedetecteerd door NVDA.
  * Voor technische details over de implementatie van deze specificatie door NVDA, zie https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Ondersteuning toegevoegd voor het VisioBraille Vario 4 brailleapparaat. (#12607)
* Foutmeldingen kunnen worden ingeschakeld (geavanceerde instellingen) bij gebruik van elke versie van NVDA. (#12672)
* In Windows 10 en later zal NVDA het aantal suggesties aankondigen bij het invoeren van zoektermen in apps zoals Instellingen en Microsoft Store. (#7330, #12758, #12790)
* Tabelnavigatie wordt nu ondersteund in rasterbesturingselementen die zijn gemaakt met behulp van de Out-GridView-cmdlet in PowerShell. (#12928)

### Veranderingen

* Espeak-ng is bijgewerkt naar 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* NVDA zal standaard eSpeak gebruiken als er geen geïnstalleerde OneCore-stemmen de NVDA-voorkeurstaal ondersteunen. (#10451)
* Als OneCore-stemmen consequent niet spreken, wordt eSpeak als synthesizer gebruikt. (#11544)
* Bij het lezen van de statusbalk met `NVDA+end`, wordt de leescursor niet langer naar zijn locatie verplaatst.
Als u deze functionaliteit nodig hebt, wijst u een invoerhandeling toe aan het juiste script in de categorie Objectnavigatie in het dialoogvenster Invoerhandelingen. (#8600)
* Bij het openen van een instellingendialoogvenster dat al geopend is, stelt NVDA de focus in op het bestaande dialoogvenster in plaats van een foutmelding te geven. (#5383)
* Liblouis braillevertaler bijgewerkt naar [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Nieuwe brailletabellen: Russisch graad 1, Tshivenda graad 1, Tshivenda graad 2
* Instead of "marked content" or "mrkd", "highlight" or "hlght" will be announced for speech and braille respectively. (#12892)
* NVDA zal niet langer proberen af ​​te sluiten wanneer dialoogvensters wachten op een vereiste actie (bijv. Bevestigen/Annuleren). (#12984)

### Opgeloste problemen

* Het volgen van toetsenbordmodificaties (zoals Control of Insert) is robuuster wanneer watchdog herstelt. (#12609)
* Het is weer mogelijk om op bepaalde systemen te controleren op NVDA-updates; bijv. schone Windows-installaties. (#12729)
* NVDA meldt correct lege tabelcellen in Microsoft Word bij gebruik van UI automation. (#11043)
* In ARIA-gegevensrastercellen op internet wordt de Escape-toets nu doorgegeven aan het raster en wordt de focusmodus niet langer onvoorwaardelijk uitgeschakeld. (#12413)
* Bij het lezen van een kopcel van een tabel in Chrome, lost het twee keer noemen van de kolomnaam op. (#10840)
* NVDA rapporteert niet langer een numerieke waarde voor UIA-schuifregelaars waarvoor een tekstuele weergave van hun waarde is gedefinieerd. (UIA ValuePattern heeft nu de voorkeur boven RangeValuePattern). (#12724)
* NVDA behandelt de waarde van UIA-schuifregelaars niet langer als altijd op percentages gebaseerd.
* Het rapporteren van de locatie van een cel in Microsoft Excel bij toegang via UI automation werkt weer correct op Windows 11. (#12782)
* NVDA stelt niet langer ongeldige Python-landinstellingen in. (#12753)
* Als een uitgeschakelde add-on wordt verwijderd en vervolgens opnieuw wordt geïnstalleerd, wordt deze opnieuw ingeschakeld. (#12792)
* Bugs opgelost rond het updaten en verwijderen van add-ons waar de add-onmap is hernoemd of waarin bestanden zijn geopend. (#12792, #12629)
* Bij gebruik van UI automation om toegang te krijgen tot Microsoft Excel-spreadsheetbesturingselementen, kondigt NVDA niet langer redundant aan wanneer een enkele cel wordt geselecteerd. (#12530)
* Meer dialoogtekst wordt automatisch gelezen in LibreOffice Writer, zoals in bevestigingsdialogen. (#11687)
* Lezen/navigeren met bladermodus in Microsoft Word via UI automation zorgt er nu voor dat het document altijd wordt gescrolld, zodat de huidige bladermoduspositie zichtbaar is en dat de cursorpositie in focusmodus de bladermoduspositie correct weerspiegelt. (#9611)
* Bij het uitvoeren van Alles lezen in Microsoft Word via UI automation, wordt nu automatisch door het document gescrolld en wordt de positie van de cursor correct bijgewerkt. (#9611)
* Bij het lezen van e-mails in Outlook terwijl NVDA toegang krijgt tot het bericht met UI Automation, worden bepaalde tabellen nu gemarkeerd als lay-outtabellen, wat betekent dat ze niet langer standaard worden gerapporteerd. (#11430)
* Een zeldzame fout bij het wisselen van audioapparaten is verholpen. (#12620)
* Invoer met literaire brailletabellen zou zich betrouwbaarder moeten gedragen in bewerkingsvelden. (#12667)
* Bij het navigeren door de Windows-systeemvakkalender geeft NVDA nu de dag van de week volledig weer. (#12757)
* Bij gebruik van een Chinese invoermethode zoals Taiwan - Microsoft Quick in Microsoft Word, het vooruit en achteruit scrollen van de brailleleesregel blijft niet langer foutief terugspringen naar de oorspronkelijke positie van de cursor. (#12855)
* Bij het lezen van Microsoft Word-documenten via UIA is navigeren per zin (alt+pijl omlaag / alt+pijl omhoog) weer mogelijk. (#9254)
* Bij het openen van MS Word met UIA wordt nu het inspringen van alinea's gerapporteerd. (#12899)
* Bij het openen van MS Word met UIA worden de opdracht voor het volgen van wijzigingen en enkele andere gelokaliseerde opdrachten nu gerapporteerd in Word. (#12904)
* Dubbele braille en spraak opgelost wanneer 'beschrijving' overeenkomt met 'inhoud' of 'naam'. (#12888)
* In MS Word met UIA ingeschakeld, is het afspelen van spelfoutgeluiden terwijl u typt nauwkeuriger. (#12161)
* In Windows 11 zal NVDA niet langer "venster" aankondigen wanneer u op Alt+Tab drukt om tussen programma's te schakelen. (#12648)
* Het nieuwe deelvenster Moderne opmerkingen aan de zijkant wordt nu ondersteund in MS Word wanneer het document niet via UIA wordt geopend. Druk op alt+f12 om tussen het deelvenster en het document te wisselen. (#12982)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Building NVDA now requires Visual Studio 2019 16.10.4 or later.
To match the production build environment, update Visual Studio to keep in sync with the [current version AppVeyor is using](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019). (#12728)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` has been deprecated for removal in 2022.1. (#12660)
  * Instead use `apiLevel` (see the comments at `_UIAConstants.WinConsoleAPILevel` for details).
* Transparency of text background color sourced from GDI applications (via the display model), is now exposed for add-ons or appModules. (#12658)
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` and `LOCALE_SLANGDISPLAYNAME` are moved to the `LOCALE` enum in languageHandler.
They are still available at the module level but are deprecated and to be removed in NVDA 2022.1. (#12753)
* The usage of functions `addonHandler.loadState` and `addonHandler.saveState` should be replaced with their equivalents `addonHandler.state.save` and `addonHandler.state.load` before 2022.1. (#12792)
* Braille output can now be checked in system tests. (#12917)

## 2021.2

Deze release introduceert voorlopige ondersteuning voor Windows 11.
Hoewel Windows 11 nog moet worden uitgebracht, is deze release getest op preview-versies van Windows 11.
Dit omvat een belangrijke oplossing voor Schermgordijn (zie belangrijke opmerkingen).
De Probleemoplosser voor COM-registratie kan nu meer problemen oplossen terwijl NVDA wordt uitgevoerd.
Er zijn updates voor de synthesizer eSpeak en braillevertaler LibLouis.
Er zijn ook verschillende bugfixes en verbeteringen, met name voor brailleondersteuning en Windows-terminals, rekenmachine, emoji-paneel en klembordgeschiedenis.

### Belangrijke opmerkingen

Vanwege een wijziging in de Windows Magnification API moest Schermgordijn worden bijgewerkt om de nieuwste versies van Windows te ondersteunen.
Gebruik NVDA 2021.2 om Schermgordijn te activeren met Windows 10 21H2 (10.0.19044) of hoger.
Dit omvat Windows 10 Insiders en Windows 11.
Als u een nieuwe versie van Windows gebruikt, moet u om veiligheidsredenen om een bevestiging vragen van iemand die kan zien dat het schermgordijn het scherm volledig zwart maakt.

### Nieuwe functies

* Experimentele ondersteuning voor ARIA-annotaties:
  * voegt een commando toe om een ​​samenvatting van details van een object met aria-details te lezen. (#12364)
  * voegt een optie toe in geavanceerde instellingen om te melden of een object details heeft in bladermodus. (#12439)
* In Windows 10 versie 1909 en later (inclusief Windows 11) zal NVDA het aantal suggesties aankondigen bij het uitvoeren van zoekopdrachten in Verkenner. (#10341, #12628)
* In Microsoft Word kondigt NVDA nu het resultaat aan van sneltoetsen voor inspringen en verkeerd-om inspringen wanneer ze worden uitgevoerd. (#6269)

### Veranderingen

* Espeak-ng is bijgewerkt naar 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Als artikel is ingeschakeld in de gebruikersinstellingen voor documentopmaak, kondigt NVDA "artikel" aan na de inhoud. (#11103)
* Liblouis braillevertaler bijgewerkt naar [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Nieuwe brailletabellen: Bulgaars graad 1, Birmees graad 1, Birmees graad 2, Kazachs graad 1, Khmer graad 1, Noord-Koerdische graad 0, Sepedi graad 1, Sepedi graad 2, Sesotho graad 1, Sesotho graad 2, Setswana graad 1, Setswana graad 2, Tatar graad 1, Vietnamees graad 0, Vietnamees graad 2, Zuid-Vietnamees graad 1, Xhosa graad 1, Xhosa graad 2, Yakut graad 1, Zulu graad 1, Zulu graad 2
* Windows 10 OCR is hernoemd naar Windows OCR. (#12690)

### Opgeloste problemen

* In Windows 10 Rekenmachine toont NVDA rekenmachine-uitdrukkingen op een brailleleesregel. (#12268)
* In terminalprogramma's in Windows 10 versie 1607 en later worden bij het invoegen of verwijderen van tekens in het midden van een regel de tekens rechts van de cursor niet meer voorgelezen. (#3200)
  * Diff Match Patch nu standaard ingeschakeld. (#12485)
* De braille-invoer werkt correct met de volgende gecontracteerde tabellen: Arabisch graad 2, Spaans graad 2, Urdu graad 2, Chinees (China, Mandarijn) graad 2. (#12541)
* Het COM-registratiehulpprogramma lost nu meer problemen op, vooral op 64-bits Windows. (#12560)
* Verbeteringen aan het gebruik van de knoppen voor de Seika Notetaker braille leesregel van Nippon Telesoft. (#12598)
* Verbeteringen in het melden van het Windows Emoji-paneel en de klembordgeschiedenis. (#11485)
* De karakterbeschrijvingen van het Bengaalse alfabet bijgewerkt. (#12502)
* NVDA sluit veilig af wanneer een nieuw proces wordt gestart. (#12605)
* Het opnieuw selecteren van het Handy Tech brailleleesregelstuurprogramma in het dialoogvenster Brailleleesregel selecteren veroorzaakt geen fouten meer. (#12618)
* Windows versie 10.0.22000 of later wordt herkend als Windows 11, niet als Windows 10. (#12626)
* Ondersteuning voor schermgordijn is hersteld en getest voor Windows-versies tot 10.0.22000. (#12684)
* Als er geen resultaten worden weergegeven bij het filteren van invoerhandelingen, blijft het dialoogvenster voor het configureren van invoerhandelingen werken zoals verwacht. (#12673)
* Een bug opgelost waarbij het eerste menu-item van een submenu in sommige contexten niet werd aangekondigd. (#12624)

### Veranderingen voor ontwikkelaars (niet vertaald)

* `characterProcessing.SYMLVL_*` constants should be replaced using their equivalent `SymbolLevel.*` before 2022.1. (#11856, #12636)
* `controlTypes` has been split up into various submodules, symbols marked for deprecation must be replaced before 2022.1. (#12510)
  * `ROLE_*` and `STATE_*` constants should be replaced to their equivalent `Role.*` and `State.*`.
  * `roleLabels`, `stateLabels` and `negativeStateLabels` have been deprecated, usages such as `roleLabels[ROLE_*]` should be replaced to their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
  * `processPositiveStates` and `processNegativeStates` have been deprecated for removal.
* On Windows 10 Version 1511 and later (including Insider Preview builds), the current Windows feature update release name is obtained from Windows Registry. (#12509)
* Deprecated: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` will be removed in 2022.1, there is no direct replacement. (#12544)

## 2021.1

Deze release bevat optionele experimentele ondersteuning voor UIA in Excel- en Chromium-browsers.
Er zijn verbeteringen voor verschillende talen en voor het openen van koppelingen in braille.
Er zijn updates voor Unicode CLDR, wiskundige symbolen en LibLouis.
En verder Veel bugfixes en verbeteringen, o.a.  in Office, Visual Studio en verschillende talen.

Opmerking:

 * Add-ons moeten worden bijgewerkt om met deze release van NVDA gebruikt te kunnen worden.
 * Deze release heeft ook geen ondersteuning meer voor Adobe Flash.

### Nieuwe functies

* Vroege ondersteuning voor UIA met op Chromium gebaseerde browsers (zoals Edge). (#12025)
* Optionele experimentele ondersteuning voor Microsoft Excel via UI Automation. Alleen aanbevolen voor Microsoft Excel build 16.0.13522.10000 of hoger. (#12210)
* Gemakkelijkere navigatie door uitvoer in de NVDA Python Console. (#9784)
  * alt + pijl omhoog / omlaag springt naar het vorige / volgende uitvoer resultaat (met shift erbij kun je selecteren).
  * control + l wist de uitvoer.
* NVDA meldt nu de categorieën die zijn toegewezen aan een afspraak in Microsoft Outlook, indien van toepassing. (#11598)
* Ondersteuning voor de Seika Notetaker brailleleesregel van Nippon Telesoft. (#11514)

### Veranderingen

* In bladermodus kunnen besturingselementen nu worden geactiveerd met de braillecursorrouterings knoppen bij de beschrijvende afkorting (o.a. "Lnk" voor een link). Dit is vooral handig voor het activeren van bijv. Selectievakjes zonder labels. (#7447)
* NVDA voorkomt nu dat de gebruiker Windows 10 OCR kan uitvoeren als schermgordijn is ingeschakeld. (#11911)
* Unicode Common Locale Data Repository (CLDR) bijgewerkt naar 39.0. (#11943, #12314)
* Meer wiskundige symbolen toegevoegd aan het symbolenwoordenboek. (#11467)
* De gebruikershandleiding, het Wat is er nieuw bestand en de lijst met sneltoetsen hebben nu een vernieuwd uiterlijk. (#12027)
* "Niet-ondersteund" wordt nu gemeld bij een poging om de schermindeling te wijzigen in toepassingen die dit niet ondersteunen, zoals Microsoft Word. (#7297)
* De optie 'Poging om spraak te annuleren voor verlopen focusgebeurtenissen' in het paneel met geavanceerde instellingen is nu standaard ingeschakeld. (#10885)
  * Dit gedrag kan worden uitgeschakeld door deze optie in te stellen op "Nee".
  * In webapplicaties (bijv. Gmail) wordt niet langer verouderde informatie meer uitgesproken wanneer de focus snel wordt verplaatst.
* Liblouis braillevertaler bijgewerkt naar [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Nieuwe brailletabellen: Wit-Russische literaire braille, Wit-Russische computerbraille, Urdu graad 1, Urdu graad 2.
* Ondersteuning voor Adobe Flash-inhoud is verwijderd uit NVDA omdat het gebruik van Flash actief wordt ontmoedigd door Adobe. (#11131)
* NVDA zal afsluiten, zelfs als de vensters nog open zijn, het afsluitproces sluit nu alle NVDA-vensters en dialoogvensters. (#1740)
* Het Spraakweergavevenster kan nu worden afgesloten met `alt+F4` en heeft een standaard sluitknop voor eenvoudigere interactie met gebruikers van aanwijsapparaten. (#12330)
* Het Brailleweergavevenster heeft nu een standaard sluitknop voor eenvoudigere interactie met gebruikers van aanwijsapparaten. (#12328)
* In het dialoogvenster Elementenlijst is de sneltoets voor de knop "Activeren" in sommige landen verwijderd om een konflikt met een label van een keuzerondje van het elementtype te voorkomen. Indien beschikbaar, is de knop nog steeds de standaardinstelling van het dialoogvenster en kan als zodanig nog steeds worden opgeroepen door simpelweg op enter te drukken vanuit de elementenlijst zelf. (#6167)

### Opgeloste problemen

* De lijst met berichten in Outlook 2010 is weer leesbaar. (#12241)
* In terminalprogramma's op Windows 10 versie 1607 en later worden bij het invoegen of verwijderen van tekens in het midden van een regel de tekens rechts van de cursor niet meer voorgelezen. (#3200)
  * Deze experimentele oplossing moet handmatig worden ingeschakeld in het paneel met geavanceerde instellingen van NVDA door het diff-algoritme te wijzigen in Diff Match Patch.
* In MS Outlook zullen onnodige afstandsmeldingen bij het shift + tabben van de berichttekst naar het onderwerpveld niet meer moeten voorkomen. (#10254)
* In de Python-console wordt nu het invoegen van een tab voor inspringen aan het begin van een niet-lege invoerregel en het uitvoeren van tabaanvulling in het midden van een invoerregel ondersteund. (#11532)
* Opmaakinformatie en andere doorzoekbare berichten bevatten niet langer onverwachte lege regels wanneer de schermindeling is uitgeschakeld. (#12004)
* Het is nu mogelijk om opmerkingen in MS Word te lezen met UIA ingeschakeld. (#9285)
* De prestaties bij interactie met Visual Studio zijn verbeterd. (#12171)
* Grafische bugs zoals ontbrekende elementen bij gebruik van NVDA met een rechts-naar-links lay-out opgelost. (#8859)
* Baseer de GUI-lay-outrichting op de NVDA-taal, niet de landinstelling van het systeem. (#638)
  * bekend probleem voor talen die van rechts naar links worden geschreven: de rechterrand van groeperingsclips met labels / bedieningselementen. (#12181)
* De Python-locale is zo ingesteld dat deze consistent overeenkomt met de taal die is geselecteerd in de Instellingen, en zal voorkomen bij gebruik van de standaardtaal. (#12214)
* TextInfo.getTextInChunks loopt niet langer vast wanneer gebruikt op Rich Edit-besturingselementen zoals de NVDA-logviewer. (#11613)
* Het is weer mogelijk om NVDA te gebruiken in talen met onderstrepingstekens in de locale naam zoals de_CH op Windows 10 1803 en 1809. (#12250)
* In WordPad werkt de configuratie van superscript / subscript-meldingen zoals verwacht. (#12262)
* NVDA verzuimt niet langer om de nieuw gefocuste inhoud op een webpagina aan te kondigen als de oude focus verdwijnt en wordt vervangen door de nieuwe focus op dezelfde positie. (#12147)
* Doorhalen, superscript en subscript-opmaak voor hele Excel-cellen worden nu gerapporteerd als de overeenkomstige optie is ingeschakeld. (#12264)
* Probleem opgelost met het kopiëren van config tijdens installatie vanaf een draagbare kopie als de standaard bestemmingsconfiguratiemap leeg is. (# 12071, #12205)
* Opgelost: onjuiste aankondiging van sommige letters met accenten of diakritische tekens wanneer de optie 'Het woord "Hoofdletter" uitspreken voor hoofdletters' is aangevinkt. (#11948)
* Probleem met toonhoogteverandering opgelost in SAPI4-spraaksynthesizer. (#12311)
* Het NVDA-installatieprogramma respecteert nu ook de `--minimal` opdrachtregelparameter en speelt het opstartgeluid niet af, volgens hetzelfde gedocumenteerde gedrag als een geïnstalleerd of draagbaar exemplaar van NVDA. (#12289)
* In MS Word of Outlook kan de snelnavigatietoets voor tabellen nu naar de lay-outtabel springen als de optie "Lay-outtabellen opnemen" is ingeschakeld in de instellingen van de bladermodus. (#11899)
* NVDA zal niet langer "↑↑↑" aankondigen voor emoji's in bepaalde talen. (#11963)
* Espeak ondersteunt nu weer Kantonees en Mandarijn. (#10418)
* In de nieuwe op Chromium gebaseerde Microsoft Edge worden tekstvelden, zoals de adresbalk, nu aangekondigd als ze leeg zijn. (#12474)
* Probleem met Seika Braille-stuurprogramma opgelost. (#10787)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Note: this is an Add-on API compatibility breaking release. Add-ons will need to be re-tested and have their manifest updated.
* NVDA's build system now fetches all Python dependencies with pip and stores them in a Python virtual environment. This is all done transparently.
  * To build NVDA, SCons should continue to be used in the usual way. E.g. executing scons.bat in the root of the repository. Running `py -m SCons` is no longer supported, and `scons.py` has also been removed.
  * To run NVDA from source, rather than executing `source/nvda.pyw` directly, the developer should now use `runnvda.bat` in the root of the repository. If you do try to execute `source/nvda.pyw`, a message box will alert you this is no longer supported.
  * To perform unit tests, execute `rununittests.bat [&lt;extra unittest discover options&gt;]`
  * To perform system tests: execute `runsystemtests.bat [&lt;extra robot options&gt;]`
  * To perform linting, execute `runlint.bat &lt;base branch&gt;`
  * Please refer to readme.md for more details.
* The following Python dependencies have also been upgraded:
  * comtypes updated to 1.1.8.
  * pySerial updated to 3.5.
  * wxPython updated to 4.1.1.
  * Py2exe updated to 0.10.1.0.
* `LiveText._getTextLines` has been removed. (#11639)
  * Instead, override `_getText` which returns a string of all text in the object.
* `LiveText` objects can now calculate diffs by character. (#11639)
  * To alter the diff behaviour for some object, override the `diffAlgo` property (see the docstring for details).
* When defining a script with the script decorator, the 'allowInSleepMode' boolean argument can be specified to control if a script is available in sleep mode or not. (#11979)
* The following functions are removed from the config module. (#11935)
  * canStartOnSecureScreens - use config.isInstalledCopy instead.
  * hasUiAccess and execElevated - use them from the systemUtils module.
  * getConfigDirs - use globalVars.appArgs.configPath instead.
* Module level REASON_* constants are removed from controlTypes - please use controlTypes.OutputReason instead. (#11969)
* REASON_QUICKNAV has been removed from browseMode - use controlTypes.OutputReason.QUICKNAV instead. (#11969)
* `NVDAObject` (and derivatives) property `isCurrent` now strictly returns Enum class `controlTypes.IsCurrent`. (#11782)
  * `isCurrent` is no longer Optional, and thus will not return None.
    * When an object is not current `controlTypes.IsCurrent.NO` is returned.
* The `controlTypes.isCurrentLabels` mapping has been removed. (#11782)
  * Instead use the `displayString` property on a `controlTypes.IsCurrent` enum value.
    * For example: `controlTypes.IsCurrent.YES.displayString`.
* `winKernel.GetTimeFormat` has been removed - use `winKernel.GetTimeFormatEx` instead. (#12139)
* `winKernel.GetDateFormat` has been removed - use `winKernel.GetDateFormatEx` instead. (#12139)
* `gui.DriverSettingsMixin` has been removed - use `gui.AutoSettingsMixin`. (#12144)
* `speech.getSpeechForSpelling` has been removed - use `speech.getSpellingSpeech`. (#12145)
* Commands cannot be directly imported from speech as `import speech; speech.ExampleCommand()` or `import speech.manager; speech.manager.ExampleCommand()` - use `from speech.commands import ExampleCommand` instead. (#12126)
* `speakTextInfo` will no longer send speech through `speakWithoutPauses` if reason is `SAYALL`, as `SayAllHandler` does this manually now. (#12150)
* The `synthDriverHandler` module is no longer star imported into `globalCommands` and `gui.settingsDialogs` - use `from synthDriverHandler import synthFunctionExample` instead. (#12172)
* `ROLE_EQUATION` has been removed from controlTypes - use `ROLE_MATH` instead. (#12164)
* `autoSettingsUtils.driverSetting` classes are removed from `driverHandler` - please use them from `autoSettingsUtils.driverSetting`. (#12168)
* `autoSettingsUtils.utils` classes are removed from `driverHandler` - please use them from `autoSettingsUtils.utils`. (#12168)
* Support of `TextInfo`s that do not inherit from `contentRecog.BaseContentRecogTextInfo` is removed. (#12157)
* `speech.speakWithoutPauses` has been removed - please use `speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses` instead. (#12195, #12251)
* `speech.re_last_pause` has been removed - please use `speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause` instead. (#12195, #12251)
* `WelcomeDialog`, `LauncherDialog` and `AskAllowUsageStatsDialog` are moved to the `gui.startupDialogs`. (#12105)
* `getDocFilePath` has been moved from `gui` to the `documentationUtils` module. (#12105)
* The gui.accPropServer module as well as the AccPropertyOverride and ListCtrlAccPropServer classes from the gui.nvdaControls module have been removed in favor of WX native support for overriding accessibility properties. When enhancing accessibility of WX controls, implement wx.Accessible instead. (#12215)
* Files in `source/comInterfaces/` are now more easily consumable by developer tools such as IDEs. (#12201)
* Convenience methods and types have been added to the winVersion module for getting and comparing Windows versions. (#11909)
  * isWin10 function found in winVersion module has been removed.
  * class winVersion.WinVersion is a comparable and order-able type encapsulating Windows version information.
  * Function winVersion.getWinVer has been added to get a winVersion.WinVersion representing the currently running OS.
  * Convenience constants have been added for known Windows releases, see winVersion.WIN* constants.
* IAccessibleHandler no longer star imports everything from IAccessible and IA2 COM interfaces - please use them directly. (#12232)
* TextInfo objects now have start and end properties which can be compared mathematically with operators such as &lt; &lt;= == != &gt;= &gt;. (#11613)
  * E.g. ti1.start &lt;= ti2.end
  * This usage is now prefered instead of ti1.compareEndPoints(ti2,"startToEnd") &lt;= 0
* TextInfo start and end properties can also be set to each other. (#11613)
  * E.g. ti1.start = ti2.end
  * This usage is prefered instead of ti1.SetEndPoint(ti2,"startToEnd")
* `wx.CENTRE_ON_SCREEN` and `wx.CENTER_ON_SCREEN` are removed, use `self.CentreOnScreen()` instead. (#12309)
* `easeOfAccess.isSupported` has been removed, NVDA only supports versions of Windows where this evaluates to `True`. (#12222)
* `sayAllHandler` has been moved to `speech.sayAll`. (#12251)
  * `speech.sayAll.SayAllHandler` exposes the functions `stop`, `isRunning`, `readObjects`, `readText`, `lastSayAllMode`.
  * `SayAllHandler.stop` also resets the `SayAllHandler` `SpeechWithoutPauses` instance.
  * `CURSOR_REVIEW` and `CURSOR_CARET` has been replaced with `CURSOR.REVIEW` and `CURSOR.CARET`.
* `speech.SpeechWithoutPauses` has been moved to `speech.speechWithoutPauses.SpeechWithoutPauses`. (#12251)
* `speech.curWordChars` has been renamed `speech._curWordChars`. (#12395)
* the following have been removed from `speech` and can be accessed through `speech.getState()`. These are readonly values now. (#12395)
  * speechMode
  * speechMode_beeps_ms
  * beenCanceled
  * isPaused
* to update `speech.speechMode` use `speech.setSpeechMode`. (#12395)
* the following have been moved to `speech.SpeechMode`. (#12395)
  * `speech.speechMode_off` becomes `speech.SpeechMode.off`
  * `speech.speechMode_beeps` becomes `speech.SpeechMode.beeps`
  * `speech.speechMode_talk` becomes `speech.SpeechMode.talk`
* `IAccessibleHandler.IAccessibleObjectIdentifierType` is now `IAccessibleHandler.types.IAccessibleObjectIdentifierType`. (#12367)
* The following in `NVDAObjects.UIA.WinConsoleUIA` have been changed (#12094)
  * `NVDAObjects.UIA.winConsoleUIA.is21H1Plus` renamed `NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable`.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo` renamed to start class name with upper case.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1` renamed `NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive`
    * The implementation works around both end points being inclusive (in text ranges) before [microsoft/terminal PR 4018](https://github.com/microsoft/terminal/pull/4018)
    * Workarounds for `expand`, `collapse`, `compareEndPoints`, `setEndPoint`, etc

## 2020.4

Deze release bevat nieuwe Chinese invoermethoden, een update van Liblouis en de elementenlijst (NVDA + f7) werkt nu in focusmodus.
Contextgevoelige hulp is nu beschikbaar wanneer u op F1 drukt in NVDA-dialoogvensters.
Verbeteringen aan de regels voor de uitspraak van symbolen, het spraakwoordenboek, braillemeldingen en Doorbladeren bij Alles lezen.
Bugfixes en verbeteringen aan Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
Op internet zijn er verbeteringen in Google Documenten en meer ondersteuning voor ARIA.
Plus vele andere belangrijke bugfixes en verbeteringen.

### Nieuwe Functies

* Als u in de dialoogvensters van NVDA op F1 drukt, wordt nu het helpbestand geopend op de meest relevante sectie. (#7757)
* Ondersteuning voor suggesties voor automatisch aanvullen (IntelliSense) in Microsoft SQL Server Management Studio plus Visual Studio 2017 en hoger. (#7504)
* Uitspraak van symbolen: ondersteuning voor groepering in een complexe symbooldefinitie en ondersteuning van groepsreferenties in een vervangende regel, waardoor ze eenvoudiger en krachtiger worden. (#11107)
* Gebruikers worden nu op de hoogte gesteld wanneer ze proberen om spraakwoordenboekvermeldingen te maken met ongeldige vervangingen voor reguliere expressies. (#11407)
  * Specifiek worden groeperingsfouten nu gedetecteerd.
* Ondersteuning toegevoegd voor de nieuwe Chinese traditionele snelle en Pinyin-invoermethoden in Windows 10. (#11562)
* Tabkopteksten worden nu beschouwd als formuliervelden met de f-toets voor snelle navigatie. (#10432)
* Een commando toegevoegd om het melden van gemarkeerde tekst in of uit te schakelen; Er is geen standaard sneltoets toegewezen. (#11807)
* De opdrachtregelparameter --copy-portable-config toegevoegd waarmee u de opgegeven configuratie automatisch naar het gebruikersaccount kunt kopiëren wanneer u NVDA stil installeert. (#9676)
* Braille-routing wordt nu ondersteund met het Brailleweergavevenster voor muisgebruikers, beweeg de muis om naar een braillecel te springen. (#11804)
* NVDA zal nu automatisch de Humanware Brailliant BI 40X- en 20X-apparaten detecteren via zowel USB als Bluetooth. (#11819)

### Veranderingen

* Liblouis braillevertaler bijgewerkt naar versie 3.16.1:
 * Lost meerdere crashes op
 * Voegt Bashkir graad 1 brailletabel toe
 * Voegt Koptische 8-punts computer brailletabel toe
 * Voegt Russische literaire braille en Russische literaire braille (gedetailleerd) tabellen toe
 * Voegt Afrikaans graad 2 brailletabel toe
 * Verwijdert de Russische graad 1 brailletabel
* Bij 'alles lezen' in de bladermodus, stoppen de volgende en vorige zoeken opdrachten het lezen niet meer als de optie Doorbladeren bij alles lezen toestaan is ingeschakeld; het lezen wordt in plaats daar van hervat na het volgende of vorige zoekresultaat. (#11563)
* Voor HIMS-brailleleesregels is F3 opnieuw toegewezen aan spatie + punten 148. (#11710)
* Verbeteringen aan de UX van de opties "braille time-out" voor meldingen en "Toon meldingen voor onbepaalde tijd". (#11602)
* In webbrowsers en andere toepassingen die de bladermodus ondersteunen, kan het dialoogvenster Elementenlijst (NVDA + F7) nu worden opgeroepen in de focusmodus. (#10453)
* Updates voor live ARIA-regio's worden nu onderdrukt wanneer het melden van wijzigingen van dynamische inhoud is uitgeschakeld. (#9077)
* NVDA meldt nu "Gekopieerd naar klembord" vóór de gekopieerde tekst. (#6757)
* Presentatie van grafische weergavetabel in schijfbeheer is verbeterd. (#10048)
* Labels voor bedieningselementen zijn nu uitgeschakeld (grijs weergegeven) wanneer het bedieningselement is uitgeschakeld. (#11809)
* CLDR-emoji-annotatie bijgewerkt naar versie 38. (#11817)
* De ingebouwde "Focus markering" -functie is omgedoopt tot "Visuele markering". (#11700)

### Opgeloste Problemen

* NVDA werkt weer correct met invoervelden bij gebruik van de applicatie Fast Log Entry. (#8996)
* Meld verstreken tijd in Foobar2000 als er geen totale tijd beschikbaar is (bijvoorbeeld bij het afspelen van een livestream). (#11337)
* NVDA respecteert nu het aria-roledescription-attribuut voor elementen in bewerkbare inhoud op webpagina's. (#11607)
* 'lijst' wordt niet langer aangekondigd op elke regel van een lijst in Google Documenten of andere bewerkbare inhoud in Google Chrome. (#7562)
* Wanneer u per teken of woord van het ene lijstitem naar het andere gaat in bewerkbare inhoud op internet, wordt het binnengaan van het nieuwe lijstitem nu aangekondigd. (#11569)
* NVDA leest nu de juiste regel wanneer de cursor aan het einde van een link aan het einde van een lijstitem in Google Documenten of andere bewerkbare inhoud op internet wordt geplaatst. (#11606)
* In Windows 7, het openen en sluiten van het startmenu vanaf het bureaublad plaatst de focus nu correct. (#10567)
* Wanneer "Probeer spraak te annuleren voor verlopen focuswijzigingen" is ingeschakeld, wordt de titel van het tabblad nu opnieuw aangekondigd bij het wisselen van tabbladen in Firefox. (#11397)
* NVDA verzuimt niet langer om een ​​lijstitem te melden na het typen van een teken in een lijst bij het gebruik van de SAPI5 Ivona-stemmen. (#11651)
* Het is weer mogelijk om de bladermodus te gebruiken bij het lezen van e-mails in Windows 10 Mail 16005.13110 en hoger. (#11439)
* Bij gebruik van de SAPI5 Ivona-stemmen van harposoftware.com, kan NvDA nu de configuratie opslaan, van synthesizer wisselen en blijft NVDA niet langer stil na het herstarten. (#11650)
* Het is nu mogelijk om nummer 6 in computerbraille in te voeren vanaf een brailletoetsenbord op HIMS-leesregels. (#11710)
* Grote prestatieverbeteringen in Azure Data Studio. (#11533, #11715)
* Met "Poging om spraak te annuleren voor verlopen focusgebeurtenissen" ingeschakeld, wordt de titel van het NVDA-zoeken dialoogvenster opnieuw aangekondigd. (#11632)
* NVDA zou niet langer moeten bevriezen bij het ontwaken van de computer als de focus terecht komt in een Microsoft Edge-document. (#11576)
* Het is niet langer nodig om op tab te drukken of de focus te verplaatsen na het sluiten van een contextmenu in MS Edge om de bladermodus weer te laten werken. (#11202)
* NVDA verzuimt niet langer om items in lijstweergaven te lezen binnen een 64-bits applicatie zoals Tortoise SVN. (#8175)
* ARIA-treegrids worden nu weergegeven als normale tabellen in bladermodus in zowel Firefox als Chrome. (#9715)
* Een omgekeerde zoekopdracht kan nu worden gestart met 'vorige zoeken' via NVDA + shift + F3 (#11770)
* Een NVDA-script wordt niet langer als herhaald beschouwd als een niet-gerelateerde toetsaanslag plaatsvindt tussen de twee uitvoeringen van het script. (#11388)
* Sterke tags en nadruk tags in Internet Explorer kunnen weer niet gemeld worden door Nadruk melden uit te schakelen in de NVDA-instellingen voor documentopmaak. (#11808)
* Een bevriezing van enkele seconden die door een klein aantal gebruikers wordt ervaren bij het verplaatsen tussen cellen met de pijltjes in Excel zou niet langer moeten voorkomen. (#11818)
* In Microsoft Teams-builds met versienummers zoals 1.3.00.28xxx, faalt NVDA niet langer bij het lezen van berichten in chats of Teams-kanalen vanwege een verkeerd gefocust menu. (#11821)
* Tekst die zowel als een spelling- en grammaticafout is gemarkeerd in Google Chrome, wordt door NVDA ook aangekondigd als zowel een spellings- als grammaticafout. (#11787)
* Bij gebruik van Outlook (Franse versie) werkt de sneltoets voor 'Allen beantwoorden' (control + shift + R) weer. (#11196)
* In Visual Studio worden IntelliSense-tooltips die aanvullende details geven over het momenteel geselecteerde IntelliSense-item nu slechts één keer gerapporteerd. (#11611)
* In Windows 10 Rekenmachine kondigt NVDA de voortgang van berekeningen niet aan als uitspreken van getypte tekens is uitgeschakeld. (#9428)
* NVDA crasht niet langer bij gebruik van Engels US grade 2 en met Woord onder cursor uitbreiden naar computerbraille  ingeschakeld, bij het weergeven van bepaalde inhoud, zoals een URL in braille. (#11754)
* Het is weer mogelijk om opmaakinformatie te rapporteren voor de gefocuste Excel-cel met NVDA + F. (#11914)
* QWERTY-invoer op Papenmeier-brailleleesregels die dit ondersteunen, werkt weer en veroorzaakt niet langer dat NVDA willekeurig vastloopt. (#11944)
* In Chromium based browsers, several cases were solved where table navigation didn't work and NVDA didn't report the number of rows/columns of the table. (#12359)

### Veranderingen voor ontwikkelaars (niet vertaald)

* System tests can now send keys using spy.emulateKeyPress, which takes a key identifier that conforms to NVDA's own key names, and by default also blocks until the action is executed. (#11581)
* NVDA no longer requires the current directory to be the NVDA application directory in order to function. (#6491)
* The aria live politeness setting for live regions can now be found on NVDA Objects using the liveRegionPoliteness property. (#11596)
* It is now possible to define separate gestures for Outlook and Word document. (#11196)

## 2020.3

Deze release bevat verschillende grote verbeteringen op het gebied van stabiliteit en prestaties, met name in Microsoft Office-toepassingen. Er zijn nieuwe instellingen om touchscreenondersteuning en grafische rapportage in of uit te schakelen.
Het bestaan ​​van gemarkeerde inhoud kan in browsers worden gemeld en er zijn nieuwe Duitse brailletabellen.

### Nieuwe Functies

* U kunt nu het melden van afbeeldingen in- en uitschakelen via de instellingen voor documentopmaak van NVDA. Merk op dat als u deze optie uitschakelt, nog steeds de alternatieve teksten van afbeeldingen worden gelezen. (#4837)
* U kunt nu de touchscreen-ondersteuning van NVDA in- en uitschakelen. Er is een optie toegevoegd aan de instellingen voor aanraakinteractie van de NVDA-instellingen. De standaardsneltoets is NVDA+control+alt+t. (#9682)
* Nieuwe Duitse brailletabellen toegevoegd. (#11268)
* NVDA detecteert nu UIA-tekstvelden die alleen lezen zijn. (#10494)
* Het bestaan ​​van gemarkeerde (gehighlighte) inhoud wordt in alle webbrowsers zowel in spraak als in braille gemeld. (#11436)
 * Dit kan worden in- en uitgeschakeld met de nieuwe optie voor gemarkeerde tekst in de NVDA-instellingen voor documentopmaak.
* Nieuwe geëmuleerde systeemtoetsen kunnen worden toegevoegd vanuit het NVDA-dialoogvenster Invoerhandelingen. (#6060)
  * Om dit te doen, drukt u op de knop Toevoegen nadat u de categorie Geëmuleerde systeemtoetsen heeft geselecteerd.
* Handy Tech Active Braille met joystick wordt nu ondersteund. (#11655)
* De instelling "Automatische focusmodus bij cursorbeweging" is nu compatibel met het uitschakelen van "Systeemfocus automatisch verplaatsen naar focusbare elementen". (#11663)

### Veranderingen

* Het script om opmaakinformatie op te vragen (NVDA + f) is dusdanig gewijzigd dat het nu de opmaak onder de systeemcursor meldt in plaats van bij de leescursor. Voor de opmaak bij de positie van de leescursor gebruikt u NVDA+shift+f. (#9505)
* NVDA stelt de systeemfocus niet langer standaard automatisch in op focusbare elementen in de bladermodus, waardoor de prestaties en stabiliteit worden verbeterd. (#11190)
* CLDR bijgewerkt van versie 36.1 naar versie 37. (#11303)
* ESpeak-NG bijgewerkt naar 1.51-dev, commit 1fb68ffffea4
* U kunt nu tabelnavigatie gebruiken in lijsten met lijstitems met selectievakjes wanneer de betreffende lijst meerdere kolommen heeft. (#8857)
* Wanneer in het venster Add-ons beheren wordt gevraagd om het verwijderen van een add-on te bevestigen, is "Nee" nu de standaardinstelling. (#10015)
* In de elementenlijst binnen Microsoft Excel worden formules nu in hun vertaalde vorm weergegeven. (#9144)
* NVDA gebruikt nu de juiste terminologie voor notities in MS Excel. (#11311)
* Bij gebruik van het script "Verplaats leescursor naar focus" in bladermodus, wordt de leescursor nu geplaatst op de positie van de virtuele cursor. (#9622)
* Informatie die wordt gemeld in bladermodus, zoals de opmaakinformatie met NVDA+F, wordt nu weergegeven in een iets groter venster gecentreerd op het scherm. (#9910)

### Opgeloste Problemen

* NVDA spreekt nu altijd bij het navigeren per woord en bij het navigeren langs een enkel symbool dat gevolgd wordt door witruimte, ongeacht de breedsprakigheidsinstellingen. (#5133)
* In applicaties die QT 5.11 of nieuwer gebruiken, worden objectbeschrijvingen opnieuw gemeld. (#8604)
* Bij het verwijderen van een woord met control+delete, blijft NVDA niet langer stil. (#3298, #11029)
  * Nu wordt het woord rechts van het verwijderde woord gemeld.
* In de algemene instellingen van NVDA wordt de talenlijst nu correct gesorteerd. (#10348)
* In het dialoogvenster Invoerhandelingen zijn de prestaties tijdens het filteren aanzienlijk verbeterd. (#10307)
* U kunt nu Unicode-tekens buiten U+FFFF verzenden vanaf een brailleleesregel. (#10796)
* NVDA meldt de inhoud van het Openen met dialoogvenster nu correct in de Mei 2020 update van Windows 10. (#11335)
* Een nieuwe experimentele optie in de Geavanceerde instellingen (Selectieve registratie voor UI Automation gebeurtenissen en elementwijzigingen inschakelen) kan belangrijke prestatieverbeteringen bieden in Microsoft Visual Studio en andere op UIAutomation gebaseerde applicaties, indien ingeschakeld. (#11077, #11209)
* Voor lijstitems met selectievakje wordt de geselecteerde status niet langer nutteloos aangekondigd, en indien van toepassing wordt de niet-geselecteerde status in plaats daarvan aangekondigd. (#8554)
* Bij gebruik van de Mei 2020 update van Windows 10 toont NVDA nu "Microsoft-geluidstoewijzing" bij het bekijken van uitvoerapparaten vanuit het dialoogvenster voor synthesizerselectie. (#11349)
* In Internet Explorer worden nummers nu correct aangekondigd voor geordende lijsten als de lijst niet begint met 1. (#8438)
* In Google Chrome meldt NVDA nu voor alle aanvinkbare besturingselementen (niet alleen selectievakjes) dat ze niet aangevinkt zijn wanneer dit niet het geval is. (#11377)
* Het is weer mogelijk om in verschillende besturingselementen te navigeren wanneer de taal van NVDA is ingesteld op Aragonees. (#11384)
* NVDA zou niet langer soms moeten vastlopen in Microsoft Word bij het snel omhoog en omlaag pijlen of het typen van tekens terwijl Braille is ingeschakeld. (#11431, #11425, #11414)
* NVDA voegt aan het einde van het klembord niet langer een niet-bestaande spatie toe bij het kopiëren van het huidige navigatorobject. (#11438)
* NVDA activeert het automatisch lezen configuratieprofiel niet langer als er niets te lezen is. (#10899, #9947)
* Het is niet langer onmogelijk voor NVDA om de lijst met onderdelen te lezen in internet Information Services (IIS) Manager. (#11468)
* NVDA houdt het audioapparaat nu open en verbetert de prestaties met sommige geluidskaarten. (#5172, #10721)
* NVDA zal niet langer vastlopen of afsluiten bij het ingedrukt houden van control+shift+Pijl omlaag in Microsoft Word. (#9463)
* De uitgevouwen / samengevouwen status van mappen in de navigatiestructuur op drive.google.com wordt nu altijd gerapporteerd door NVDA. (#11520)
* NVDA detecteert automatisch de NLS eReader Humanware brailleleesregel via Bluetooth wanneer de Bluethooth-naam "NLS eReader Humanware" is. (#11561)
* Grote prestatieverbeteringen in Visual Studio Code. (#11533)

### Veranderingen voor ontwikkelaars (niet vertaald)

* The GUI Helper's BoxSizerHelper.addDialogDismissButtons supports a new "separated" keyword argument, for adding a standard horizontal separator to dialogs (other than messages and single input dialogs). (#6468)
* Additional properties were added to app modules, including path for the executable (appPath), is a Windows Store app (isWindowsStoreApp), and machine architecture for the app (appArchitecture). (#7894)
* It is now possible to create app modules for apps hosted inside wwahost.exe on Windows 8 and later. (#4569)
* A fragment of the log can now be delimited and then copied to clipboard using NVDA+control+shift+F1. (#9280)
* NVDA-specific objects that are found by Python's cyclic garbage collector are now logged when being deleted by the collector to aide in removing reference cycles from NVDA. (#11499)
 * The majority of NVDA's classes are tracked including NVDAObjects, appModules, GlobalPlugins, SynthDrivers, and TreeInterceptors.
 * A class that needs to be tracked should inherit from garbageHandler.TrackedObject.
* Significant debug logging for MSAA events can be now enabled in NVDA's Advanced settings. (#11521)
* MSAA winEvents for the currently focused object are no longer filtered out along with other events if the event count for a given thread is exceeded. (#11520)

## 2020.2

Hoogtepunten van deze release zijn onder meer ondersteuning voor een nieuwe brailleleesregel van Nattiq, betere ondersteuning voor de ESET antivirus GUI en Windows Terminal, prestatieverbeteringen in 1Password en met de Windows OneCore synthesizer. Plus vele andere belangrijke oplossingen en verbeteringen.

### Nieuwe Functies

* Ondersteuning voor nieuwe brailleleesregels:
  * Nattiq nBraille (#10778)
* Script toegevoegd om de configuratiemap van NVDA te openen (geen standaard toegewezen invoerhandeling). (#2214)
* Betere ondersteuning voor ESET antivirus GUI. (#10894)
* Ondersteuning toegevoegd voor Windows Terminal. (#10305)
* Een commando toegevoegd om het actieve configuratieprofiel te melden (standaard geen invoerhandeling). (#9325)
* Een commando toegevoegd om het melden van subscripts en superscripts in- en uit te schakelen (standaard geen invoerhandeling). (#10985)
* Webapplicaties (bijv. Gmail) spreken geen verouderde informatie meer uit wanneer de focus snel wordt verplaatst. (#10885)
  * Deze experimentele oplossing moet handmatig worden ingeschakeld via de optie 'Probeer spraak te annuleren voor verlopen focuswijzigingen' in het paneel met geavanceerde instellingen.
* Er zijn veel meer symbolen toegevoegd aan het standaard interpunctiewoordenboek. (#11105)

### Veranderingen

* Liblouis braillevertaler bijgewerkt van 3.12 naar [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Het melden van superscripts en subscripts wordt nu apart beheerd van het melden van lettertypeattributen. (#10919)
* Vanwege wijzigingen die zijn aangebracht in VS Code, schakelt NVDA de bladermodus in Code niet langer standaard uit. (#10888)
* NVDA rapporteert niet langer de berichten "boven" en "onder" wanneer de leescursor rechtstreeks naar de eerste of laatste regel van het huidige navigatorobject wordt verplaatst met de scripts voor respectievelijk verplaats naar vorige/volgende regel. (#9551)
* NVDA meldt niet langer de berichten "links" en "rechts" bij het direct verplaatsen van de leescursor naar het eerste of laatste teken van de regel voor het huidige navigatorobject met de scripts voor respectievelijk verplaats naar begin/einde regel. (#9551)

### Opgeloste Problemen

* NVDA start nu correct wanneer het logbestand niet kan worden aangemaakt. (#6330)
* In recente releases van Microsoft Word 365 kondigt NVDA niet langer aan dat het vorige woord is verwijderd wanneer Control+Backspace wordt ingedrukt tijdens het bewerken van een document. (#10851)
* In Winamp kondigt NVDA opnieuw de status aan bij het in- en uitschakelen van shuffle en herhalen. (#10945)
* NVDA is niet langer extreem traag bij het navigeren binnen de lijst met items in 1Password. (#10508)
* De Windows OneCore-spraaksynthesizer is niet langer traag tussen uitspraken. (#10721)
* NVDA loopt niet langer vast wanneer u het contextmenu voor 1Password opent vanuit de systeemwerkbalk. (#11017)
* In Office 2013 en ouder:
  * Linten worden aangekondigd wanneer de focus er voor het eerst naartoe wordt verplaatst. (#4207)
  * Contextmenu-items worden weer correct gemeld. (#9252)
  * Lintsecties worden consequent aangekondigd bij het navigeren met Control+pijltjes. (#7067)
* In de bladermodus in Mozilla Firefox en Google Chrome verschijnt tekst niet langer ten onrechte op een aparte regel wanneer de webinhoud CSS display: inline-flex gebruikt. (#11075)
* In bladermodus met Systeemfocus automatisch verplaatsen naar focusbare elementen uitgeschakeld, is het nu mogelijk om elementen te activeren die de focus niet kunnen hebben.
* In bladermodus met Systeemfocus automatisch verplaatsen naar focusbare elementen uitgeschakeld, is het nu mogelijk om elementen te activeren waar naartoe is genavigeerd door op de Tab-toets te drukken. (#8528)
* In bladermodus met Systeemfocus automatisch verplaatsen naar focusbare elementen uitgeschakeld, veroorzaakt het activeren van bepaalde elementen niet langer een muisklik op een verkeerde locatie. (#9886)
* NVDA logt niet langer een foutmelding bij het gebruik van DevExpress-tekstvelden. (#10918)
* De flitsberichten van de pictogrammen in het systeemvak worden niet langer gerapporteerd bij toetsenbordnavigatie als hun tekst gelijk is aan de naam van de pictogrammen, om dubbele aankondiging te voorkomen. (#6656)
* In bladermodus met Systeemfocus automatisch verplaatsen naar focusbare elementen uitgeschakeld, krijgt bij schakelen naar focusmodus met NVDA + spatie nu het element onder de cursor de focus. (#11206)
* Op bepaalde systemen is het weer mogelijk om te controleren op NVDA-updates; bijv. schone Windows-installaties. (#11253)
* De focus wordt niet langer verplaatst in Java-applicaties wanneer de selectie wordt gewijzigd in een boomstructuur, tabel of lijst die niet de focus heeft. (#5989)

### Veranderingen voor ontwikkelaars (niet vertaald)

* execElevated and hasUiAccess have moved from config module to systemUtils module. Usage via config module is deprecated. (#10493)
* Updated configobj to 5.1.0dev commit f9a265c4. (#10939)
* Automated testing of NVDA with Chrome and a HTML sample is now possible. (#10553)
* IAccessibleHandler has been converted into a package, OrderedWinEventLimiter has been extracted to a module and unit tests added (#10934)
* Updated BrlApi to version 0.8 (BRLTTY 6.1). (#11065)
* Status bar retrieval may now be customized by an AppModule. (#2125, #4640)
* NVDA no longer listens for IAccessible EVENT_OBJECT_REORDER. (#11076)
* A broken ScriptableObject (such as a GlobalPlugin missing a call to its base class' init method) no longer breaks NVDA's script handling. (#5446)

## 2020.1

Hoogtepunten van deze release zijn onder meer ondersteuning voor verschillende nieuwe brailleleesregels van HumanWare en APH, plus vele andere belangrijke bugfixes zoals de mogelijkheid om wiskunde opnieuw te lezen in Microsoft Word met MathPlayer / MathType.

### Nieuwe Functies

* Het momenteel geselecteerde item in keuzelijsten wordt opnieuw gepresenteerd in bladermodus in Chrome, vergelijkbaar met NVDA 2019.1. (#10713)
* U kunt nu met de rechtermuisknop klikken door iddel van 	touchscreens door met één vinger te tikken en vast te houden. (#3886)
* Ondersteuning voor nieuwe brailleleesregels: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2 en NLS eReader. (#10830)

### Veranderingen

* NVDA probeert te voorkomen dat het systeem vergrendelt of in slaap valt tijdens automatisch lezen. (#10643)
* Ondersteuning voor out-of-process iframes in Mozilla Firefox. (#10707)
* Liblouis braillevertaler bijgewerkt naar versie 3.12. (#10161)

### Opgeloste Problemen

* Probleem opgelost waardoor NVDA het Unicode-minteken (U+2212) niet uitsprak. (#10633)
* Bij het installeren van een add-on vanuit het dialoogvenster Add-ons beheren worden namen van bestanden en mappen in het bladervenster niet langer tweemaal gemeld. (#10620, #2395)
* In Firefox, wanneer Mastodon wordt geladen met de geavanceerde webinterface ingeschakeld, worden alle tijdlijnen nu correct weergegeven in bladermodus. (#10776)
* In bladermodus meldt NVDA nu "uitgeschakeld" voor niet-ingeschakelde selectievakjes waar dit voorheen niet het geval was. (#10781)
* ARIA switch besturingselementen melden niet langer verwarrende informatie zoals "niet ingedrukt ingeschakeld" or "pressed checked". (#9187)
* SAPI4 stemmen zouden niet langer moeten kunnen weigeren om bepaalde tekst uit te spreken. (#10792)
* NVDA kan weer wiskundige vergelijkingen in Microsoft Word lezen en ermee werken. (#10803)
* NVDA is weer in staat om te melden dat tekst wordt gedeselecteerd in bladermodus als op een pijltoets wordt gedrukt terwijl er tekst is geselecteerd. (#10731).
* NVDA wordt niet meer afgesloten als er een fout optreedt bij het initialiseren van eSpeak. (#10607)
* Fouten veroorzaakt door unicode in vertalingen voor snelkoppelingen stoppen het installatieprogramma niet langer, wat berijkt wordt door terug te vallen op de Engelse tekst. (#5166, #6326)
* Het uit en weg van lijsten navigeren met de pijltjestoetsen wanneer doorbladeren tijdens automatisch lezen is ingeschakeld, kondigt niet langer continu het verlaten van de lijst of tabel aan. (#10706)
* Muis volgen voor sommige MSHTML-elementen in Internet Explorer functioneert weer naar behoren. (#10736)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Developer documentation is now build using sphinx. (#9840)
* Several speech functions have been split into two. (#10593)
  The speakX version remains, but now depends on a getXSpeech function which returns a speech sequence.
  * speakObjectProperties now relies on getObjectPropertiesSpeech
  * speakObject now relies on getObjectSpeech
  * speakTextInfo now relies on getTextInfoSpeech
  * speakWithoutPauses has been converted into a class, and refactored, but should not break compatibility.
  * getSpeechForSpelling is deprecated (though still available) use getSpellingSpeech instead.
  Private changes that should not affect addon developers:
  * _speakPlaceholderIfEmpty is now _getPlaceholderSpeechIfTextEmpty
  * _speakTextInfo_addMath is now _extendSpeechSequence_addMathForTextInfo
* Speech 'reason' has been converted to an Enum, see controlTypes.OutputReason class. (#10703)
  * Module level 'REASON_*' constants are deprecated.
* Compiling NVDA dependencies now requires Visual Studio 2019 (16.2 or newer). (#10169)
* Updated SCons to version 3.1.1. (#10169)
* Again allow behaviors._FakeTableCell to have no location defined (#10864)

## 2019.3

NVDA 2019.3 is een zeer belangrijke release die veel veranderingen onder de motorkap bevat, waaronder de upgrade van Python 2 naar Python 3 en een belangrijke herschrijving van het spraaksubsysteem van NVDA.
Hoewel deze wijzigingen de compatibiliteit met oudere NVDA-add-ons verbreken, is de upgrade naar Python 3 noodzakelijk voor de veiligheid. De veranderingen in het spraaksysteem zorgen daarnaast voor belangrijke innovatiemogelijkheden in de nabije toekomst.
 Andere hoogtepunten in deze release zijn 64-bits ondersteuning voor Java, schermgordijn en focusmarkeringsffunctionaliteit, ondersteuning voor meer brailleleesregels en een nieuw spraakweergavevenster, en vele andere probleemojplossingen.

### Nieuwe Functies

* De nauwkeurigheid van het commando muis naar navigatorobject verplaatsen is verbeterd in tekstvelden in Java-toepassingen. (#10157)
* Ondersteuning voor de volgende Handy Tech brailleleesregels toegevoegd (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Alle door de gebruiker gedefinieerde invoerhandelingen kunnen nu worden verwijderd via een nieuwe knop "Fabrieksinstellingen herstellen" in het dialoogvenster Invoerhandelingen. (#10293)
* Het melden van het lettertype in Microsoft Word omvat nu ook of tekst is gemarkeerd als verborgen. (#8713)
* Een commando toegevoegd om de leescursor te verplaatsen naar de positie die eerder was ingesteld als startmarkering voor selectie of kopiëren: NVDA+shift+F9. (#1969)
* In Internet Explorer, Microsoft Edge en recente versies van Firefox en Chrome worden oriëntatiepunten (landmarks) nu gemeld in focusmodus en bij objectnavigatie. (#10101)
* In Internet Explorer, Google Chrome en Mozilla Firefox kunt u nu navigeren per artikel met gebruik van snelnavigatiescripts. Deze scripts zijn standaard niet toegewezen en kunnen worden toegewezen in het dialoogvenster Invoerhandelingen wanneer het dialoogvenster wordt geopend vanuit een bladermodusdocument. (#9227)
 * Figures are also reported. They are considered objects and therefore navigable with the o quick navigation key.
* In Internet Explorer, Google Chrome en Mozilla Firefox worden artikel-elementen nu gemeld bij objectnavigatie en optioneel in de bladermodus indien ingeschakeld in de instellingen voor documentopmaak. (#10424)
* Schermgordijn, dat, indien ingeschakeld, het hele scherm zwart maakt op Windows 8 en hoger. (#7857)
 * Added a script to enable screen curtain (until next restart with one press, or always while NVDA is running with two presses), no default gesture is assigned.
 * Can be enabled and configured via the 'vision' category in NVDA's settings dialog.
* Added screen highlight functionality to NVDA. (#971, #9064)
 * Highlighting of the focus, navigator object, and browse mode caret position can be enabled and configured via the 'vision' category in NVDA's settings dialog.
 * Note: This feature is incompatible with the focus highlight add-on, however, the add-on can still be used while the built-in highlighter is disabled.
* Added Braille Viewer tool, allows viewing braille output via an on-screen window. (#7788)

### Veranderingen

* De gebruikershandleiding beschrijft nu hoe NVDA te gebruiken in de Windows Console. (#9957)
* Het uitvoeren van nvda.exe zal nu een ​​reeds actief exemplaar van NVDA afsluiten alvorens NVDA te starten. De opdrachtregelparameter -r | --replace wordt nog steeds geaccepteerd, maar genegeerd. (#8320)
* In Windows 8 en nieuwer meldt NVDA nu productnaam- en versiegegevens voor gehoste apps zoals apps die zijn gedownload vanuit de Microsoft Store. Deze informatie wordt door de app verstrekt. (#4259, #10108)
* Bij het met het toetsenbord in- en uitschakelen van wijzigingen bijhouden in Microsoft Word zal NVDA de status van de instelling melden. (#942)
* Het NVDA-versienummer wordt nu vastgelegd als het eerste bericht in het logboek. Dit gebeurt zelfs als logboekregistratie is uitgeschakeld in de instellingen. (#9803)
* In het instellingendialoogvenster kunt u het geconfigureerde logniveau niet meer wijzigen als dit is overschreven vanaf de opdrachtregel. (#10209)
* In Microsoft Word meldt NVDA nu de weergavestatus van niet-afdrukbare tekens bij het indrukken van de sneltoets Ctrl+Shift+8. (#10241)
* Updated Liblouis braille translator to commit 58d67e63. (#10094)
* Wanneer het melden van CLDR-tekens (inclusief emoji) is ingeschakeld worden ze nu uitgesproken op alle symboolniveaus. (#8826)
* Pythonpakketten van derden die zijn opgenomen in NVDA, zoals comtypes, registreren nu hun waarschuwingen en fouten in het NVDA-logboek. (#10393)
* Updated Unicode Common Locale Data Repository emoji annotations to version 36.0. (#10426)
* When focussing a grouping in browse mode, the description is now also read. (#10095)
* The Java Access Bridge is now included with NVDA to enable access to Java applications, including for 64 bit Java VMs. (#7724)
* If the Java Access Bridge is not enabled for the user, NVDA automatically enables it at NVDA startup. (#7952)
* Updated eSpeak-NG to 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Opgeloste Problemen

* Emoji en andere 32-bits unicode-tekens nemen nu minder ruimte in op een brailleleesregel wanneer ze worden weergegeven als hexadecimale waarden. (#6695)
* In Windows 10 zal NVDA flitsberichten van universele apps aankondigen als NVDA is geconfigureerd om flitsberichten te rapporteren in de instellingen voor objectweergave. (#8118)
* In Windows 10 versie 1607 en nieuwer wordt getypte tekst nu gemeld in Mintty. (#1348)
* In Windows 10 versie 1607 en hoger wordt de uitvoer in de Windows-console die dicht bij de cursor verschijnt niet meer gespeld. (#513)
* Besturingselementen in het Compressor dialoogvenster in Audacity worden nu gemeld tijdens het navigeren in het venster. (#10103)
* NVDA behandelt spaties niet langer als woorden bij het gebruik van de leescursor in op Scintilla gebaseerde tessktverwerkers zoals Notepad++. (#8295)
* NVDA zal voorkomen dat het systeem in de slaapstand gaat wanneer er door tekst wordt gescrolld met een brailleleesregel. (#9175)
* In Windows 10 zullen veranderingen correct weergegeven worden in braille bij het bewerken van celinhoud in Microsoft Excel en in andere UIA-tekstbesturingselementen waar dit eerder niet het geval was. (#9749)
* NVDA meldt opnieuw suggesties in de adresbalk van Microsoft Edge. (#7554)
* NVDA blijft niet langer stil bij het focussen van een HTML-tabbesturingselement in Internet Explorer. (#8898)
* In Microsoft Edge op basis van EdgeHTML speelt NVDA geen geluid voor zoeksuggesties meer af wanneer het venster wordt gemaximaliseerd. (#9110, #10002)
* ARIA 1.1 vervolgkeuezelijsten worden nu ondersteund in Mozilla Firefox en Google Chrome. (#9616)
* NVDA meldt niet langer de inhoud van visueel verborgen kolommen voor lijstitems in SysListView32-besturingselementen. (#8268)
* Het dialoogvenster Instellingen laat niet langer "informatie" zien als het huidige logniveau wanneer gebruikt op een beveiligd bureaublad. (#10209)
* In het Start-menu van de Windows 10 Verjaardagsupdate en niewuer zal NVDA details van zoekresultaten melden. (#10232)
* Als in de bladermodus het document wordt gewijzigd als de cursor wordt verplaatst of snelnavigatie wordt gebruikt, spreekt NVDA in sommige gevallen niet langer onjuiste inhoud uit. (#8831, #10343)
* Sommige namen van opsommingstekens in Microsoft Word zijn gecorrigeerd. (#10399)
* In de Windows 10 mei 2019 Update en nieuwer zal NVDA opnieuw de eerst geselecteerde emoji of het eerste klemborditem melden wanneer respectievelijk het emoji-paneel en de klembordgeschiedenis worden geopend. (#9204)
* In Poedit is het opnieuw mogelijk om sommige vertalingen te bekijken voor talen van rechts naar links. (#9931)
* In de Instellingen-app in de Windows 10 april 2018 Update en nieuwer meldt NVDA niet langer voortgangsbalkinformatie voor volumemeters op de pagina Systeem / Geluid. (#10284)
* Ongeldige reguliere expressies in spraakwoordenboeken zorgen er niet langer voor dat de spraak in NVDA stopt met werken. (#10334)
* Bij het lezen van items met opsommingstekens in Microsoft Word met UIA ingeschakeld, wordt het opsommingsteken van het volgende lijstitem niet langer ten onrechte gemeld. (#9613)
* Some rare braille translation issues and errors with liblouis have been resolved. (#9982)
* Java applications started before NVDA are now accessible without the need to restart the Java app. (#10296)
* In Mozilla Firefox, when the focused element becomes marked as current (aria-current), this change is no longer spoken multiple times. (#8960)
* NVDA will now treat certain composit unicode characters such as e-acute as one single character when moving through text. (#10550)
* Spring Tool Suite Version 4 is now supported. (#10001)
* Don't double speak name when aria-labelledby relation target is an inner element. (#10552)
* On Windows 10 version 1607 and later, typed characters from Braille keyboards are spoken in more situations. (#10569)
* When changing the audio output device, tones played by NVDA will now play through the newly selected device. (#2167)
* In Mozilla Firefox, moving focus in browse mode is faster. This makes moving the cursor in browse mode more responsive in many cases. (#10584)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Updated Python to 3.7. (#7105)
* Updated pySerial to version 3.4. (#8815)
* Updated wxPython to 4.0.3 to support Python 3.5 and later. (#9630)
* Updated six to version 1.12.0. (#9630)
* Updated py2exe to version 0.9.3.2 (in development, commit b372a8e from albertosottile/py2exe#13). (#9856)
* Updated UIAutomationCore.dll comtypes module to version 10.0.18362. (#9829)
* The tab-completion in the Python console only suggests attributes starting with an underscore if the underscore is first typed. (#9918)
* Flake8 linting tool has been integrated with SCons reflecting code requirements for Pull Requests. (#5918)
* As NVDA no longer depends on pyWin32, modules such as win32api and win32con are no longer available to add-ons. (#9639)
 * win32api calls can be replaced with direct calls to win32 dll functions via ctypes.
 * win32con constants should be defined in your files.
* The "async" argument in nvwave.playWaveFile has been renamed to "asynchronous". (#8607)
* speakText and speakCharacter methods on synthDriver objects are no longer supported.
 * This functionality is handled by SynthDriver.speak.
* SynthSetting classes in synthDriverHandler have been removed. Now use driverHandler.DriverSetting classes instead.
* SynthDriver classes should no longer expose index via the lastIndex property.
 * Instead, they should notify the synthDriverHandler.synthIndexReached action with the index, once all previous audio has finished playing before that index.
* SynthDriver classes must now notify the synthDriverHandler.synthDoneSpeaking action, once all audio from a SynthDriver.speak call has completed playing.
* SynthDriver classes must support the speech.PitchCommand in their speak method, as changes in pitch for speak spelling now depends on this functionality.
* The speech function getSpeechTextForProperties has been renamed to getPropertiesSpeech. (#10098)
* The braille function getBrailleTextForProperties has been renamed to getPropertiesBraille. (#10469)
* Several speech functions have been changed to return speech sequences. (#10098)
 * getControlFieldSpeech
 * getFormatFieldSpeech
 * getSpeechTextForProperties now called getPropertiesSpeech
 * getIndentationSpeech
 * getTableInfoSpeech
* Added a textUtils module to simplify string differences between Python 3 strings and Windows unicode strings. (#9545)
 * See the module documentation and textInfos.offsets module for example implementations.
* Deprecated functionality now removed. (#9548)
 * AppModules removed:
  * Windows XP sound recorder.
  * Klango Player, which is abandoned software.
 * configobj.validate wrapper removed.
  * New code should use from configobj import validate instead of import validate
 * textInfos.Point and textInfos.Rect replaced by locationHelper.Point and locationHelper.RectLTRB respectively.
 * braille.BrailleHandler._get_tether and braille.BrailleHandler.set_tether have been removed.
 * config.getConfigDirs has been removed.
 * config.ConfigManager.getConfigValidationParameter has been replaced by getConfigValidation
 * inputCore.InputGesture.logIdentifier property has been removed.
   * Use _get_identifiers in inputCore.InputGesture instead.
 * synthDriverHandler.SynthDriver.speakText/speakCharacter have been removed.
 * Removed several synthDriverHandler.SynthSetting classes.
   * Previously kept for backwards compatibility (#8214), now considered obsolete.
   * Drivers that used the SynthSetting classes should be updated to use the DriverSetting classes.
 * Some legacy code has been removed, particularly:
  * Support for the Outlook pre 2003 message list.
  * An overlay class for the classic start menu, only found in Windows Vista and earlier.
  * Dropped support for Skype 7, as it is definitely not working any more.
* Added a framework to create vision enhancement providers; modules that can change screen contents, optionally based on input from NVDA about object locations. (#9064)
 * Add-ons can bundle their own providers in a visionEnhancementProviders folder.
 * See the vision and visionEnhancementProviders modules for the implementation of the framework and examples, respectively.
 * Vision enhancement providers are enabled and configured via the 'vision' category in NVDA's settings dialog.
* Abstract class properties are now supported on objects that inherit from baseObject.AutoPropertyObject (e.g. NVDAObjects and TextInfos). (#10102)
* Introduced displayModel.UNIT_DISPLAYCHUNK as a textInfos unit constant specific to DisplayModelTextInfo. (#10165)
 * This new constant allows walking over the text in a DisplayModelTextInfo in a way that more closely resembles how the text chunks are saved in the underlying model.
* displayModel.getCaretRect now returns an instance of locationHelper.RectLTRB. (#10233)
* The UNIT_CONTROLFIELD and UNIT_FORMATFIELD constants have been moved from virtualBuffers.VirtualBufferTextInfo to the textInfos package. (#10396)
* For every entry in the NVDA log, information about the originating thread is now included. (#10259)
* UIA TextInfo objects can now be moved/expanded by the page, story and formatField text units. (#10396)
* External modules (appModules and globalPlugins) are now less likely to be able to break the creation of NVDAObjects.
 * Exceptions caused by the "chooseNVDAObjectOverlayClasses" and "event_NVDAObject_init" methods are now properly caught and logged.
* The aria.htmlNodeNameToAriaLandmarkRoles dictionary has been renamed to aria.htmlNodeNameToAriaRoles. It now also contains roles that aren't landmarks.
* scriptHandler.isCurrentScript has been removed due to lack of use. There is no replacement. (#8677)Deze zijn niet vertaald. We verwijzen naar [de Engelstalige versie van dit document](../en/changes.html).

## 2019.2.1

In deze versie van NVDA zijn er diverse crashes opgelost die zich voordeden in 2019.2, waaronder:

* Verschillende crashes opgelost in Gmail die merkbaar waren in zowel Firefox als Chrome bij interactie met bepaalde pop-upmenu's zoals bij het maken van filters of het wijzigen van bepaalde Gmail-instellingen. (#10175, #9402, #8924)
* In Windows 7 veroorzaakt NVDA niet langer een crash van de Windows Verkenner wanneer de muis wordt gebruikt in het startmenu. (#9435)
* Windows Verkenner in Windows 7 crasht niet langer bij het gebruik van metadata-invoervelden. (#5337)
* NVDA crasht niet langer bij interactie met afbeeldingen met een base64 URI in Mozilla Firefox of Google Chrome. (#10227)

## 2019.2

Hoogtepunten in deze versie zijn automatische detectie van Freedom Scientific brailleleesregels, een expirimentele functie in de geavanceerde instellingencategorie waardoor de bladermodus de focus niet langer automatisch verplaatst (wat mogelijk prestatieverbeteringen oplevert), toevoeging van de optie snelheidsboost voor de Windows OneCore synthesizer voor het gebruiken van zeer snelle spraak, en vele andere oplossingen voor problemen.

### Nieuwe Functies

* NVDA's ondersteuning voor Miranda NG werkt met nieuwere versies van de client. (#9053)
* U kunt nu standaard de bladermodus uitschakelen door het uitschakelen van de optie "Bladermodus inschakelen bij laden van pagina" in de NVDA-instellingen voor de bladermodus. (#8716)
 * Merk op dat wanneer deze optie is uitgeschakeld, u nog steeds de bladermodus handmatig kunt inschakelen door op NVDA+spatie te drukken.
* U kunt nu symbolen filteren in het dialoogvenster voor uitspraak van interpunctie en symbolen, vergelijkbaar met hoe filteren werkt in de elementenlijst en het dialoogvenster invoerhandelingen. (#5761)
* Er is een commando toegevoegd om de Resolutie van de teksteenheid voor de muis aan te passen (hoeveel tekst er wordt uitgesproken wanneer de muis zich verplaatst), er is geen standaardinvoerhandeling aan toegewezen. (#9056)
* De windows OneCore synthesizer heeft nu een optie snelheidsboost, die aanzienlijk snellere spraak mogelijk maakt. (#7498)
* De optie snelheidsboodst kan nu ingesteld worden in de ring met synthesizerinstellingen voor ondersteunde spraaksynthesizers. (Momenteel eSpeak-NG en Windows OneCore). (#8934)
* Configuratieprofielen kunnen nu handmatig worden geactiveerd met invoerhandelingen. (#4209)
 * De invoerhandeling moet worden ingesteld in het dialoogvenster "Invoerhandelingen".
* In Eclipse, ondersteuning toegevoegd voor automatische aanvullingen in de code editor. (#5667)
 * Bovendien kan Javadoc-informatie worden gelezen vanuit de editor wanneer deze aanwezig is door NVDA + d te gebruiken.
* Er is een experimentele optie toegevoegd aan het paneel met Geavanceerde instellingen waarmee u kunt voorkomen dat de systeemfocus de bladermoduscursor volgt (Systeemfocus automatisch verplaatsen naar focusbare elementen). (#2039) Hoewel dit misschien niet geschikt is om voor alle websites uit te schakelen , kan dit mogelijk de volgende problemen oplossen:
 * Rubberen band effect: NVDA maakt de laatste toetsaanslag binnen de bladermodus sporadisch ongedaan door naar de vorige locatie te springen.
 * Invoervelden die de systeemfocus stelen wanneer u op sommige websites door deze invoervelden loopt.
 * De toetsaanslagen in de bladermodus reageren traag.
* Voor ondersteunde brailleleesregels kunnen de instellingen van de driver nu gewijzigd worden vanuit de categorie braillein NVDA's instellingenvenster. (#7452)
* Automatische detectie van Freedom Scientific brailleleesregels wordt nu ondersteund. (#7727)
* Er is een commando toegevoegd om de vervanging weer te geven van het symbool onder de leescursor. (#9286)
* Er is een experimentele optie toegevoegd aan het paneel met Geavanceerde instellingen die u in staat stel om een nieuwe, in ontwikkeling zijnde herschreven implementatie te proberen van NVDA's Windows Console ondersteuning die gebruik maakt van de Microsoft UI Automation API. (#9614)
* In the Python Console ondersteunt het invoerveld nu het plakken van meerdere regels vanaf het klembord. (#9776)

### Veranderingen

* Synthesizervolume wordt nu verhoogd en verlaagd met 5 in plaats van 10 bij gebruik van de instellingenring. (#6754)
* De tekst in add-onbeheer verduidelijkt wanneer NVDA wordt gestart met de --disable-addons parameter. (#9473)
* Unicode Common Locale Data Repository (uitspraak van emoji) bnbijgewerkt naar versie 35.0. (#9445)
* The hotkey for the filter field in the elements list in browse mode has changed to alt+y. (#8728)
* Wanneer een automatisch gedetecteerde brailleleesregel via Bluetooth verbonden is, zal NVDA blijven zoeken naar USB-leesregels die door dezelfde driver worden aangestuurd en overschakelen naar een USB-verbinding als deze beschikbaar komt. (#8853)
* ESpeak-NG is bijgewerkt naar commit 67324cc.
* Liblouis braillevertaler bijgewerkt naar versie 3.10.0. (#9439, #9678)
* NVDA meldt het woord 'geselecteerd' nu na de zojuist door de gebruiker geselecteerde tekst. (#9028, #9909)
* In Microsoft Visual Studio Code is de bladermodus nu standaard uitgeschakeld. (#9828)

### Opgeloste Problemen

* NVDA crasht niet langer als de map van een add-on leeg is. (#7686)
* Links-naar-rechts en rechts-naar-links-markeringen worden niet langer weergegeven in Braille of spraak bij het openen van het eigenschappenvenster. (#8361)
* Bij het springen naar formuliervelden met snelnavigatie in de bladermodus wordt nu het volledige formulierveld gemeld in plaats van alleen de eerste regel. (#9388)
* NVDA valt niet langer stil na het afsluiten van de Windows 10 Mail-app. (#9341)
* NVDA weigert niet langer te starten wanneer de regionale instellingen van de gebruiker is ingesteld op een taal die niet bekend is bij NVDA, zoals Engels (Nederland). (#8726)
* Als de bladermodus is ingeschakeld in Microsoft Excel en u overschakelt naar een browser in de focusmodus of vice versa, wordt de status van de bladermodus nu juist gemeld. (#8846)
* NVDA meldt nu correct de regel onder de muiscursor in Notepad++ en andere op Scintilla gebaseerde tekstverwerker. (#5450)
* In Google Docs (en andere webgebaseerde tekstverwerkers) wordt er in braille niet langer onterecht "lst einde" getoond voor de cursor in het midden van een lijstitem. (#9477)
* In de Windows 10 mei 2019 Update spreekt NVDA niet langer veel volumemeldingen uit als het volume wordt gewijzigd met hardwareknoppen wanneer de Windows Verkenner de focus heeft. (#9466)
* Het laden van het dialoogvenster voor uitspraak van interpunctie en symbolen is nu veel sneller bij het gebruik van symboolwoordenboeken met meer dan 1000 items. (#8790)
* In Scintilla-besturingselementen zoals Notepad++ is NVDA nu in staat om de juiste regel te melden wanneer automatische terugloop is ingeschakeld. (#9424)
* In Microsoft Excel wordt de locatie van de cel nu gemeld nadat deze is gewijzigd als gevolg van de toetscombinatie shift+enter of shift+numpadEnter. (#9499)
* In Visual Studio 2017 en nieuwer wordt in de Objects Explorer het geselecteerde item in de objects tree of members tree nu correct gemeld. (#9311)
* Add-ons met namen die alleen verschillen in hoofdletters worden niet langer als afzonderlijke add-ons behandeld. (#9334)
* Voor Windows OneCore stemmen wordt de in NVDA ingestelde snelheid niet langer beinvloed door de ingestelde snelheid in de Windows 10 Spraakinstellingen. (#7498)
* Het logboek kan nu worden geopend met NVDA+F1 wanneer er geen ontwikkelaarsinfo is voor het huidige navigatorobject. (#8613)
* Het is opnieuw mogelijk om NVDA's tabelnavigatiecommando's te gebruiken in Google Docs, in Firefox en Chrome. (#9494)
* De bumpertoetsen op Freedom Scientific brailleleesregels werken nu correct. (#8849)
* Bij het lezen van het eerste teken van een document in Notepad++ 7.7 X64 zal NVDA niet langer tot wel tien seconden bevriezen. (#9609)
* HTCom kan nu gebruikt worden met een Handy Tech brailleleesregel in combinatie met NVDA. (#9691)
* In Mozilla Firefox worden updates in een live region niet langer gemeld wanneer de live region zich in een achtergrondtablad bevindt. (#1318)
* Het zoekvenster van de NVDA bladermodus functioneert nu ook wanneer het Over dialoogvenster momenteel in de achtergrond is geopend. (#8566)

### Veranderingen voor ontwikkelaars (niet vertaald)

* You can now set the "disableBrowseModeByDefault" property on app modules to leave browse mode off by default. (#8846)
* The extended window style of a window is now exposed using the `extendedWindowStyle` property on Window objects and their derivatives. (#9136)
* Updated comtypes package to 1.1.7. (#9440, #8522)
* When using the report module info command, the order of information has changed to present the module first. (#7338)
* Added an example to demonstrate using nvdaControllerClient.dll from C#. (#9600)
* Added a new isWin10 function to the winVersion module which returns whether or not this copy of NVDA is running on (at least) the supplied release version of Windows 10 (such as 1903). (#9761)
* The NVDA Python console now  contains more useful modules in its namespace (such as appModules, globalPlugins, config and textInfos). (#9789)
* The result of the last executed command in the NVDA Python console is now accessible from the _ (line) variable. (#9782)
 * Note that this shadows the gettext translation function also called "_". To access the translation function: del _

## 2019.1.1

In deze versie van NVDA zijn de volgende problemen opgelost:

* NVDA veroorzaakt niet langer een crash van Excel 2007 en weigert niet langer om te melden wanneer een cel een formule heeft. (#9431)
* Google Chrome crasht niet langer bij interactie met bepaalde keuzelijsten. (#9364)
* Er is een probleem opgelost waardoor de gebruikersconfiguratie mogelijk niet naar het systeemconfiguratieprofiel kon worden gekopieerd. (#9448)
* In Microsoft Excel gebruikt NVDA opnieuw de vertaalde melding bij het melden van de locatie van samengevoegde cellen. (#9471)

## 2019.1

Hoogtepunten in deze versie zijn prestatieverbeteringen bij het gebruik van zowel Microsoft Word als Excel, stabiliteits- en beveiligingsverbeteringen zoals ondersteuning voor add-ons met informatie over versiecompatibiliteit en vele andere probleemoplossingen.

Houd er rekening mee dat aangepaste appModules, globalPlugins en brailleleesregel- en synthesizer drivers vanaf deze versie van NVDA niet langer automatisch worden geladen vanuit de NVDA-gebruikersconfiguratiemap.
Deze dienen in plaats daarvan geïnstalleerd te worden als onderdeel van een NVDA add-on. Voor het ontwikkelen van code voor een add-on kan gebruik gemaakt worden van het ontwikkelaarskladblok (developer scratchpad) in de NVDA-gebruikersconfiguratiemap. Hiervoor dient de optie voor het ontwikkelaarskladblok ingeschakeld te zijn in de nieuwe categorie met geavanceerde instellingen van NVDA.
Deze wijzigingen zijn nodig om compatibiliteit van aangepaste code beter te waarborgen, zodat er geen problemen in NVDA ontstaan wanneer deze code incompatibel wordt met nieuwere versies.
Raadpleeg de lijst met wijzigingen verderop voor meer informatie hierover.

### Nieuwe Functies

* Nieuwe brailletabellen: Afrikaans, Arabisch 8 punt computerbraille, Arabisch graad 2, Spaans graad 2. (#4435, #9186)
* Een optie toegevoegd aan de muisinstellingen van NVDA om ervoor te zorgen dat NVDA situaties verwerkt waarin de muis wordt bestuurd door een andere applicatie. (#8452)
 * Hierdoor kan NVDA de muis volgen wanneer een systeem op afstand wordt bediend met behulp van TeamViewer of andere afstandsbedieningssoftware.
* De `--enable-start-on-logon` commandoregelparameter is toegevoegd zodat stille installaties van NVDA dusdanig geconfigureerd kunnen worden dat NVDA wel of niet start tijdens Windows aanmelding. Specificeer true om te starten op het aanmeldscherm of false om dit niet te doen. Wanneer --enable-start-on-logon niet gespecificeerd is, zal NVDA standaard starten tijdens Windows aanmelding, tenzij dit tijdens een eerdere installatie uitgeschakeld was. (#8574)
* Het is mogelijk om de logfuncties van NVDA uit te schakelen door het niveau van loggen in te stellen op "uitgeschakeld" in de categorie met Algemene instellingen. (#8516)
* De aanwezigheid van formules in -spreadsheets in LibreOffice en Apache OpenOffice wordt nu gemeld. (#860)
* In Mozilla Firefox en Google Chrome meldt de bladermodus nu het geselecteerde item in keuzelijsten en boomstructuren.
 * Dit werkt in Firefox 66 en later.
 * Dit werkt niet voor bepaalde keuzelijsten (HTML select elementen) in Chrome.
* Vroege ondersteuning voor apps zoals Mozilla Firefox op computers met ARM64-processors (bijvoorbeeld Qualcomm Snapdragon). (#9216)
* Er is een nieuwe geavanceerd categorie toegevoegd aan het dialoogvenster Instellingen van NVDA, inclusief een optie om NVDA's nieuwe ondersteuning voor Microsoft Word uit te proberen via de Microsoft UI Automation API. (#9200)
* Ondersteuning toegevoegd voor de grafische weergave in Windows Schijfbeheer. (#1486)
* Ondersteuning toegevoegd voor Handy Tech Connect Braille en Basic Braille 84. (#9249)

### Veranderingen

* Liblouis braillevertaler bijgewerkt naar versie 3.8.0. (#9013)
* Add-on-auteurs kunnen nu een minimaal vereiste NVDA-versie afdwingen voor hun add-ons. NVDA zal weigeren een add-on te installeren of te laden waarvan de minimaal vereiste NVDA-versie hoger is dan de huidige NVDA-versie. (#6275)
* Add-on-auteurs kunnen nu de versie van NVDA specificeren waarmee de add-on als laatste is getest. Als een add-on alleen getest is met een versie van NVDA ouder dan de huidige versie, weigert NVDA de add-on te installeren of te laden. (#6275)
* Deze versie van NVDA staat het installeren en laden van add-ons toe die nog geen gegevens over de Minimale en Laatst Getestte NVDA-versie bevatten. Het upgraden naar toekomstige versies van NVDA (bijv. 2019.2) zou er echter automatisch voor kunnen gaan zorgen dat deze oudere add-ons worden uitgeschakeld.
* De opdracht om de muis naar het huidige navigatorobject te verplaatsen, is nu beschikbaar in Microsoft Word evenals voor UIA-besturingselementen, waaronder Microsoft Edge. (#7916, #8371)
* Het melden van tekst onder de muis is verbeterd binnen Microsoft Edge en andere UIA-applicaties. (#8370)
* Wanneer NVDA wordt gestart met de opdrachtregelparameter `--portable-path`, wordt het opgegeven pad automatisch ingevuld wanneer wordt geprobeerd een draagbare kopie van NVDA te maken met behulp van het NVDA-menu. (#8623)
* Het pad naar de Noorse brailletabel is bijgewerkt voor gebruik van de standaard uit het jaar 2015. (#9170)
* Bij navigeren op basis van een alinea (control + pijl omhoog of omlaag) of bij tabelnavigatie(control + alt + pijltjestoetsen), wordt de aanwezigheid ​​van spelfouten niet langer gemeld, zelfs als NVDA is geconfigureerd om deze automatisch te melden. Dit komt doordat alinea's en tabelcellen vrij omvangrijk kunnen zijn en het detecteren van spelfouten in sommige toepassingen erg veel tijd kan kosten. (#9217)
* NVDA laadt niet langer automatisch aangepaste appModules, globalPlugins en brailleleesregel- en synthesizer drivers uit de NVDA-gebruikersconfiguratiemap. Deze code moet in plaats daarvan worden gedistribueerd als een add-on met de juiste versiegegevens, zodat incompatibele code niet wordt uitgevoerd door huidige versies van NVDA. (#9238)
 * Ontwikkelaars die code dienen te testen terwijl deze wordt ontwikkeld, kunnen NVDA's ontwikkelaarskladblokmap inschakelen via de categorie geavanceerd in de NVDA-instellingen. Na het inschakelen kan code geplaatst worden in de map 'scratchpad' in de NVDA-gebruikersconfiguratiemap.

### Opgeloste Problemen

* Bij gebruik van de OneCore spraaksynthesizer met de Windows 10 april 2018 update en nieuwer, worden er niet langer grote stukken stilte toegevoegd in de spraak. (#8985)
* Bij het navigeren per karakter in invoervelden voor platte tekst (zoals Kladblok) of bladermodus, worden 32-bits emoji-tekens die bestaan uit twee UTF-16 code points (zoals 🤦) nu correct gelezen. (#8782)
* Het dialoogvenster om het herstarten van NVDA te bevestigen na het wijzigen van de interfacetaal is verbeterd. De tekst en de knoplabels zijn nu beknopter en minder verwarrend. (#6416)
* Als een spraaksynthesizer van een derde partij niet kan worden geladen, zal NVDA bij gebruik van Windows 10 terugvallen op de Windows OneCore spraaksynthesizer in plaats van espeak. (#9025)
* Het item "Welkomstvenster" in het NVDA-menu is niet langer zichtbaar . (#8520)
* Bij gebruik van tab of snelnavigatie in bladermodus worden legenda's op tabbladen nu consequenter gemeld. (#709)
* NVDA zal nu selectiewijzigingen aankondigen voor bepaalde tijdkiezers, zoals in de app Alarmen en klok in Windows 10. (#5231)
* In het Actiecentrum van Windows 10 zal NVDA statusmeldingen aankondigen bij het veranderen van snelle acties zoals helderheid en Concentratiehulp. (#8954)
* In het Actiecentrum in de Windows 10 oktober 2018 Update en ouder, zal NVDA de snelle actie voor helderheid herkennen als een knop in plaats van een schakelknop. (#8845)
* NVDA is opnieuw in staat om de cursor te volgen en verwijderde karakters te melden in de Microsoft Excel invoervelden voor ga naar en zoeken. (#9042)
* Een zeldzame crash in de bladermodus in Firefox is opgelost. (#9152)
* NVDA heeft niet langer moeite met het melden van de focus voor sommige besturingselementen in het lint van Microsoft Office 2016 wanneer dit is samengevouwen.
* NVDA heeft niet langer moeite met het melden van de voorgestelde contactpersoon bij het invoeren van adressen in nieuwe berichten in Outlook 2016. (#8502)
* De laatste cursorroutingstoetsen op 80-cellige leesregels van Eurobraille verplaatsen de cursor niet langer naar een positie aan of net na het begin van de brailleleesregel. (#9160)
* Tabelnavigatie is opnieuw beschikbaar in de conversatieweergave van Mozilla Thunderbird. (#8396)
* In Mozilla Firefox en Google Chrome werkt het overschakelen naar de focusmodus nu correct voor bepaalde keuzelijsten en boomstructuren (waarbij de keuzelijst/boomstructuur niet zelf de focus kan krijgen, maar de items daarin wel). (#3573, #9157)
* Bladermodus is standaard correct ingeschakeld bij het lezen van berichten in Outlook 2016/365 als de experimentele UI Automation-ondersteuning van NVDA wordt gebruikt voor Word-documenten. (#9188)
* NVDA zal nu minder snel dusdanig bevriezen dat uitloggen uit uw huidige Windows-sessie de enige manier is om te ontsnappen. (#6291)
* Wanneer in de Windows 10 oktober 2018 update en nieuwer de geschiedenis van het klembord in de cloud wordt geopend als het klembord leeg is, meldt NVDA de klembordstatus. (#9103)
* Wanneer er in de Windows 10 oktober 2018 update en nieuwer wordt gezocht naar emoji in het emoji-paneel, meldt NVDA het bovenste zoekresultaat. (#9105)
* NVDA bevriest niet langer in het hoofdvenster van Oracle VirtualBox 5.2 en nieuwer. (#9202)
* De responsiviteit in Microsoft Word bij het navigeren per regel, alinea of ​​tabelcel kan in sommige documenten aanzienlijk zijn verbeterd. Een herinnering dat u Microsoft Word voor de beste prestaties dient in te stellen op de conceptweergave met alt + v, p na het openen van een document. (#9217)
* In Mozilla Firefox en Google Chrome worden lege berichten (ARIA alerts) niet langer gemeld. (#5657)
* Aanzienlijke prestatieverbeteringen bij het navigeren door cellen in Microsoft Excel, met name wanneer de spreadsheet opmerkingen en/of keuzelijsten voor validatie bevat. (#7348)
* Het is niet langer nodig om het direct bewerken in cellen uit te schakelen in de opties van Microsoft Excel om met NVDA toegang te krijgen tot het invoerveld voor celbewerking in Excel 2016/365. (#8146).
* Een bevriezingsprobleem opgelost in Firefox dat soms zichtbaar werd wanneer snelnavigatie gebruikt werd om te navigeren tussen oriëntatiepunten terwijl de Enhanced Aria add-on gebruikt werd. (#8980)

### Veranderingen voor ontwikkelaars (niet vertaald)

* NVDA can now  be built with all editions of Microsoft Visual Studio 2017 (not just the Community edition). (#8939)
* You can now include log output from liblouis into the NVDA log by setting the louis boolean flag in the debugLogging section of the NVDA configuration. (#4554)
* Add-on authors are now able to provide NVDA version compatibility information in add-on manifests. (#6275, #9055)
 * minimumNVDAVersion: The minimum required version of NVDA for an add-on to work properly.
 * lastTestedNVDAVersion: The last version of NVDA an add-on has been tested with.
* OffsetsTextInfo objects can now implement the _getBoundingRectFromOffset method to allow retrieval of bounding rectangles per characters instead of points. (#8572)
* Added a boundingRect property to TextInfo objects to retrieve the bounding rectangle of a range of text. (#8371)
* Properties and methods within classes can now be marked as abstract in NVDA. These classes will raise an error if instantiated. (#8294, #8652, #8658)
* NVDA can log the time since input when text is spoken, which helps in measuring perceived responsiveness. This can be enabled by setting the timeSinceInput setting to True in the debugLog section of the NVDA configuration. (#9167)

## 2018.4.1

Deze versie lost een crash op bij het opstarten wanneer de taal van de NVDA gebruikersinterface is ingesteld op Aragonees. (#9089)

## 2018.4

Hoogtepunten in deze versie zijn prestatieverbeteringen in recente Mozilla Firefox versies, het uitspreken van emoji door alle synthesizers, het melden van beantwoord/doorgestuurd voor berichten in Outlook, het melden van de afstand tussen de cursor en de rand van een Microsoft Word pagina, en vele probleemoplossingen.

### Nieuwe Functies

* Nieuwe brailletabellen: Chinees (China, Mandarijn) graden 1 en 2. (#5553)
* De status beantwoord / doorgestuurd wordt nu gemeld voor e-mails in de Microsoft Outlook berichtenlijst. (#6911)
* NVDA is nu in staat om beschrijvingen te lezen van emoji en andere tekens die deel uitmaken van de Unicode Common Locale Data Repository. (#6523)
* In Microsoft Word kan de afstand tussen de cursor en de linker- en bovenrand van de pagina gemeld worden bij het indrukken van NVDA+numpadDelete. (#1939)
* In Google Sheets met brailleondersteuning ingeschakeld, meldt NVDA niet langer 'geselecteerd' voor iedere cel bij het verplaatsen van de focus tussen cellen. (#8879)
* Ondersteuning toegevoegd voor Foxit Reader en Foxit Phantom PDF. (#8944)
* Ondersteuning toegevoegd voor de DBeaver database tool. (#8905)

### Veranderingen

* "Helpbalonnen melden" in de instellingen voor objectweergave is hernoemd naar "Notificaties melden" om aan te geven dat deze optie ook het melden van toast-notificaties in Windows 8 en nieuwer omvat. (#5789)
* In de NVDA toetsenbordinstellingen worden de selectievakjes voor het in- of uitschakelen van de NVDA_toetsen nu weergegeven in een lijst in plaats van als aparte selectievakjes.
* NVDA zal niet langer overbodige informatie presenteren bij het lezen van de klok in de systeembalk bij sommige versies van Windows. (#4364)
* Liblouis braillevertaler bijgewerkt naar versie 3.7.0. (#8697)
* ESpeak-ng is bijgewerkt naar commit 919f3240cbb.

### Opgeloste Problemen

* In Outlook 2016/365 worden de categorie en vlagstatus nu gemeld voor berichten. (#8603)
* Wanneer de taal van NVDA is ingesteld op Kirgyzisch, Mongools of Macedonisch wordt er niet langer een waarschuwing weergegeven dat de taal niet ondersteund wordt door het besturingssysteem. (#8064)
* Het verplaatsen van de muis naar het navigatorobject zal de muis nu veel accurater verplaatsen naar de bladermoduspositie in Mozilla Firefox, Google Chrome en Acrobat Reader DC. (#6460)
* De interactie met vervolgkeuzelijsten op het web in Firefox, Chrome en Internet Explorer is verbeterd. (#8664)
* Bij gebruik met de Japanse versie van Windows XP of Vista geeft NVDA nu zoals verwacht de systeemvereisten weer. (#8771)
* Prestatieverbeteringen bij het navigeren binnen lange pagina's met een grote hoeveelheid dynamische wijzigingen in Mozilla Firefox. (#8678)
* Er zijn niet langer lettertypeattributen zichtbaar in braille wanneer deze zijn uitgeschakeld in de instellingen voor documentopmaak. (#7615)
* NVDA no longer fails to track focus in File Explorer and other applications using UI Automation when another app is busy (such as batch processing audio). (#7345)
* In ARIA menu's op het web wordt de escape-toets nu doorgestuurd naar het menu, waardoor de focusmodus niet langer onvoorwaardelijk wordt uigeschakeld. (#3215)
* Bij het lezen van berichten in de nieuwe webinterface van GMail wordt bij het gebruiken van snelnavigatie niet langer de volledige inhoud gemeld na het element waar naartoe genavigeerd is. (#8887)
* Na het updaten van NVDA zullen browsers zoals Firefox en google Chrome niet langer crashen, en zal bladermodus updates blijven weergeven in momenteel geladen documenten. (#7641)
* NVDA meldt niet langer meerdere malen klikbaar op een rij bij het navigeren door klikbare inhoud. (#7430)
* Invoerhandelingen uitgevoerd op baum Vario 40 brailleleesregels worden opnieuw correct afgehandeld. (#8894)
* In Google Slides met Mozilla Firefox zal NVDA niet langer geselecteerde tekst melden bij ieder element dat de focus krijgt. (#8964)

### Veranderingen voor ontwikkelaars (niet vertaald)

* gui.nvdaControls now contains two classes to create accessible lists with check boxes. (#7325)
 * CustomCheckListBox is an accessible subclass of wx.CheckListBox.
 * AutoWidthColumnCheckListCtrl adds accessible check boxes to an AutoWidthColumnListCtrl, which itself is based on wx.ListCtrl.
* If you need to make a wx widget accessible which isn't already, it is possible to do so by using an instance of gui.accPropServer.IAccPropServer_impl. (#7491)
 * See the implementation of gui.nvdaControls.ListCtrlAccPropServer for more info.
* Updated configobj to 5.1.0dev commit 5b5de48a. (#4470)
* The config.post_configProfileSwitch action now takes the optional prevConf keyword argument, allowing handlers to take action based on differences between configuration before and after the profile switch. (#8758)

## 2018.3.2

Deze versie lost een probleem op dat een crash in Google Chrome veroorzaakte bij het navigeren tussen tweets op [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Deze versie lost een kritiek probleem op in NVDA dat ervoor zorgde dat 32-bit versies van Mozilla Firefox konden crashen. (#8759)

## 2018.3

Hoogtepunten in deze versie zijn het automatisch detecteren van verschillende brailleleesregels, ondersteuning voor nieuwe Windows 10 functies waaronder het Windows 10 Emoji invoerpaneel, en veel aanvullende probleemoplossingen.

### Nieuwe Functies

* NVDA meldt nu grammaticafouten wanneer zij correct worden aangeboden op webpagina's in Mozilla Firefox en Google Chrome. (#8280)
* Inhoud in webpagina's die is aangemerkt als ingevoegd of verwijderd, wordt nu als zodanig gemeld in Google Chrome. (#8558)
* Ondersteuning toegevoegd voor BrailleNote QT en Apex BT's scrollwiel wanneer BrailleNote wordt gebruikt als een brailleleesregel met NVDA. (#5992, #5993)
* Scripts toegevoegd voor het melden van verstreken en totale tijd voor het huidige nummer in Foobar2000. (#6596)
* Het symbool voor de Mac command-toets (⌘) wordt nu gemeld door iedere synthesizer bij het lezen van tekst. (#8366)
* Aangepaste rollen (roles) via het aria-roledescription attribuut worden nu ondersteund in alle web browsers. (#8448)
* Nieuwe brailletabbellen: Tsjechisch 8 punt, Centraal-Koerdisch, Esperanto, Hongaars, Zweeds 8 punt computerbraille. (#8226, #8437)
* Ondersteuning toegevoegd voor het automatisch herkennen van brailleleesregels op de achtergrond. (#1271)
 * ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille en HumanWare BrailleNote en Brailliant BI/B leesregels worden op dit moment ondersteund.
 * U kunt deze functie activeren door het selecteren van de optie automatisch in de lijst met leesregels in het dialoogvenster "selecteer brailleleesregel".
 * Bekijk de documentatie voor meer details.
* Ondersteuning toegevoegd voor moderne invoermethoden die geïntroduceerd zijn in recente versies van Windows 10. Deze omvatten het emoji-paneel (Fall Creators Update), dicteren (Fall Creators Update), hardwaretoetsenbord invoersuggesties (April 2018 Update), en het cloud klembord (October 2018 Update). (#7273)
* Inhoud die gemarkeerd is als blokcitaat met gebruik van ARIA (role blockquote) wordt nu ondersteund in Mozilla Firefox 63. (#8577)

### Veranderingen

* De lijst met beschikbare talen in de algemene instellingen van NVDA wordt nu gesorteerd op taal in plaats van op basis van ISO 639 codes. (#7284)
* Standaardtoewijzingen toegevoegd voor alt shift tab en windows tab voor alle ondersteunde Freedom Scientific brailleleesregels. (#7387)
* Voor ALVA BC680 en protocol converter leesregels is het nu mogelijk om verschillende functies toe te wijzen aan de linker en rechter smart pad-, duim- en etouch toetsen. (#8230)
* Voor ALVA BC6 leesregels zal de toetsencombinatie sp2+sp3 de huidige datum en tijd melden, terwijl sp1+sp2 nu de Windows-toets emuleert. (#8230)
* De gebruiker wordt bij het starten van NVDA nu eenmalig gevraagd of hij/zij ermee akkoord gaat dat NVDA gebruiksstatistieken verstuurd naar NV Access bij het automatisch controleren op updates. (#8217)
* Wanneer er gecontroleerd wordt op updates en de gebruiker ermee akkoord is gegaan dat er gebruiksstatistieken worden verstuurd naar NV Access, zal NVDA nu de naam van de huidige synthesizer driver en brailleleesregel versturen om te helpen bij een betere prioritering van toekomstig werk aan deze drivers. (#8217)
* Liblouis braillevertaler bijgewerkt naar versie 3.5.0. (#8365)
* Het pad naar de juiste Russische 8 punt brailletabel is bijgewerkt. (#8446)
* ESpeak-ng is bijgewerkt naar 1.49.3dev commit 910f4c2 (#8561)

### Opgeloste Problemen

* Toegankelijke labels voor elementen in Google Chrome worden nu directer gemeld in bladermodus wanneer het label zelf geen deel uitmaakt van de inhoud. (#4773)
* Notificaties worden nu ondersteund in Zoom. Dit omvat notificaties voor dempen/dempen opheffen en inkomende berichten.(#7754)
* Het wisselen van te tonen focuscontext in braille zorgt er in de bladermodus niet langer voor dat de braille-uitvoer de cursor niet volgt. (#7741)
* ALVA BC680 brailleleesregels hebben niet langer sporadisch moeite met initialiseren. (#8106)
* In de standaardsituatie zullen ALVA BC6 leesregels niet langer geëmuleerde systeemtoetsen uitvoeren bij het indrukken van toetsencombinaties die sp2+sp3 omvatten en gekoppeld zijn aan interne functionaliteit van de leesregel. (#8230)
* Het indrukken van sp2 op een ALVA BC6 leesregel om de alt-toets te emuleren werkt nu daadwerkelijk zoals vermeld. (#8360)
* NVDA meldt niet langer overbodig wijzigingen van de toetsenbordindeling. (#7383, #8419)
* Het volgen van de muis is nu stukken accurater in Kladblok en andere invoervelden voor platte tekst wanneer er sprake is van een document met meer dan 65535 karakters. (#8397)
* NVDA zal meer dialoogvensters herkennen in Windows 10 en andere moderne applicaties. (#8405)
* In de Windows 10 October 2018 Update en Windows Server 2019 en nieuwer zal NVDA niet langer moeite hebben met het volgen van de systeemfocus wanneer een applicatie vastloopt of het systeem overspoelt met gebeurtenissen. (#7345, #8535)
* Gebruikers worden nu geïnformeerd bij een poging tot het lezen of kopiëren van een lege statusbalk. (#7789)
* Een probleem opgelost waarbij de niet ingeschakelde staat van elementen niet door de spraak uitgesproken werd wanneer het element eerder gedeeltelijk ingeschakeld was. (#6946)
* In de lijst met talen in de algemene instellingen van NVDA wordt de naam van de Birmese taal nu correct weergegeven onder Windows 7. (#8544)
* In Microsoft Edge zal NVDA nu notificaties melden zoals over de beschikbaarheid van de leesweergave en de voortghang van het laden van pagina's. (#8423)
* Bij het navigeren naar een lijst op het web meldt NVDA nu het label van de lijst wanneer de web-auteur een label heeft ingesteld. (#7652)
* Bij het handmatig toewijzen van functies aan invoerhandelingen voor een bepaalde leesregel worden deze nu altijd weergegeven als toegewezen aan die leesregel. In het verleden werden ze altijd weergegeven alsof ze waren toegewezen aan de actieve leesregel. (#8108)
* De 64-bit-versie van Media Player Classic wordt nu ondersteund. (#6066)
* Diverse verbeteringen in de braille-ondersteuning in Microsoft Word met UI Automation ingeschakeld:
 * Zoals ook bij andere invoervelden met meerdere regels het geval is, wordt bij documenten het eerste karakter van het document nu aan het begin van de leesregel weergegeven wanneer de cursor zich aan het begin van het document bevindt. (#8406)
 * De in eerdere versies overdreven focusweergave is gereduceerd voor zowel spraak als braille wanneer een Word-document de focus krijgt. (#8407)
 * Cursor routing in braille werkt nu correct bij gebruik in een lijst in een Word-document. (#7971)
 * Nieuw ingevoegde opsommingstekens/nummering in een Word-document worden correct gemeld voor zowel braille als spraak. (#7970)
* In Windows 10 1803 en nieuwer is het nu mogelijk om add-ons te installeren wanneer de optie "Gebruik Unicode UTF-8 voor wereldwijde taalondersteuning" is ingeschakeld. (#8599)
* NVDA maakt het gebruik van iTunes 12.9 en nieuwer niet langer compleet onmogelijk. (#8744)

### Veranderingen voor ontwikkelaars (niet vertaald)

* Added scriptHandler.script, which can function as a decorator for scripts on scriptable objects. (#6266)
* A system test framework has been introduced for NVDA. (#708)
* Some changes have been made to the hwPortUtils module: (#1271)
 * listUsbDevices now yields dictionaries with device information including hardwareID and devicePath.
 * Dictionaries yielded by listComPorts now also contain a usbID entry for COM ports with USB VID/PID information in their hardware ID.
* Updated wxPython to 4.0.3. (#7077)
* As NVDA now only supports Windows 7 SP1 and later, the key "minWindowsVersion" used to check if UIA should be enabled for a particular release of Windows has been removed. (#8422)
* You can now register to be notified about configuration saves/reset actions via new config.pre_configSave, config.post_configSave, config.pre_configReset, and config.post_configReset actions. (#7598)
 * config.pre_configSave is used to be notified when NVDA's configuration is about to be saved, and config.post_configSave is called after configuration has been saved.
 * config.pre_configReset and config.post_configReset includes a factory defaults flag to specify if settings are reloaded from disk (false) or reset to defaults (true).
* config.configProfileSwitch has been renamed to config.post_configProfileSwitch to reflect the fact that this action is called after profile switch takes place. (#7598)
* UI Automation interfaces updated to Windows 10 October 2018 Update and Server 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)

## 2018.2.1

Deze versie bevat bijgewerkte vertalingen omdat op het laatste moment een functie die problemen opleverde werd verwijderd.

## 2018.2

Hoogtepunten in deze versie zijn ondersteuning voor tabellen in Kindle voor PC, ondersteuning voor HumanWare BrailleNote Touch en BI14 brailleleesregels, verbeteringen aan zowel Onecore als Sapi5 spraaksynthesizers, verbeteringen in Microsoft Outlook en veel meer.

### Nieuwe Functies

* samengevoegde cellen in rijen en kolommen van tabellen worden nu gemeld in spraak en braille. (#2642)
* NVDA tabelnavigatiecommando's worden nu ondersteund in Google Docs (met Braillemodus ingeschakeld). (#7946)
* In Kindle voor PC is er de mogelijkheid om tabellen te lezen en er tussen te navigeren. (#7977)
* Ondersteuning voor de BrailleNote touch en Brailliant BI 14 brailleleesregels via zowel USB als bluetooth. (#6524)
* In de Windows 10 Fall Creators Update en nieuwer kan NVDA nu notificaties melden van apps zoals Rekenmachine en Windows Store. (#8045)
* Nieuwe brailletabellen: Litouws 8 punts, Oekraïns, Mongools graad 2. (#7839)
* Een script toegevoegd om opmaak te melden van de tekst onder een specifieke braillecel. (#7106)
* Bij het updaten van NVDA is er nu de mogelijkheid om de installatie van de update uit te stellen tot een later gekozen moment. (#4263)
* Nieuwe talen: Mongools, Zwitsers Duits.
* Het is nu mogelijk om control, shift, alt, windows en NVDA in- en uit te schakelen vanaf uw brailletoetsenbord en deze modifiers te combineren met brailleinvoer (bijv. het indrukken van control+s). (#7306)
 * U kunt deze nieuwe virtuele modifierschakelaars toewijzen met de commando's die te vinden zijn onder Geëmuleerde systeemtoetsen in het dialoogvenster invoerhandelingen.
* Herstelde ondersteuning voor de leesregels Handy Tech Braillino en Modular (met oude firmware). (#8016)
* Datum en tijd voor ondersteunde Handy Tech leesregels (zoals Active Braille en Active Star) worden nu automatisch gesynchroniseerd door NVDA als ze meer dan vijf seconden uit elkaar lopen. (#8016)
* Er kan nu een invoerhandeling toegewezen worden om triggers voor configuratieprofielen tijdelijk uit te schakelen. (#4935)

### Veranderingen

* De statuskolom in het venster voor add-ons beheren is zodanig gewijzigd dat deze nu aangeeft of de add-on in- of uitgeschakeld is in plaats van werkend of onderbroken. (#7929)
* Liblouis braillevertaler bijgewerkt naar 3.5.0. (#7839)
* De Litouwse brailletabel is hernoemd naar Litouws 6 punts om verwarring te vermijden met de nieuwe 8 punts tabel. (#7839)
* De tabellen Frans (Canada) graad 1 en graad 2 zijn verwijderd. In plaats daarvan zullen resp. de Frans (unified) 6 punts computerbraille en Graad 2 tabellen worden gebruikt. (#7839)
* De secundaire cursorroutingtoetsen op Alva BC6, EuroBraille en Papenmeier brailleleesregels melden nu informatie over de opmaak voor de tekst onder de braillecel behorend bij die toets. (#7106)
* Brailletabellen voor kortschrift schakelen nu terug naar onverkort braille in niet-bewerkbare gevallen (d.w.z. bij besturingselementen zonder cursor of in bladermodus). (#7306)
* NVDA is nu minder breedsprakig voor afspraken of tijdsloten in de Outlok agenda die een hele dag betreffen. (#7949)
* Alle voorkeuren van NVDA bevinden zich nu gegroepeerd in één instellingenvenster onder NVDA-menu -> Opties -> Instellingen, in plaats van verspreid in een veelvoud aan dialoogvensters. (#7302)
* De standaard spraaksynthesizer bij het gebruik van Windows 10 is nu oneCore stemmen in plaats van eSpeak. (#8176)

### Opgeloste Problemen

* NVDA heeft niet langer problemen bij het lezen van elementen die de focus hebben in het Microsoft Account inlogscherm in instellingen na het invullen van een e-mailadres. (#7997)
* NVDA heeft niet langer moeite met het lezen van de paginana het teruggaan naar een vorige pagina in Microsoft Edge. (#7997)
* Op het windows 10 inlogscherm spreekt NVDA niet langer het laatst ingevoerde karakter uit van de pincode bij het ontgrendelen van het scherm. (#7908)
* IN Chrome en Firefox worden Labels van selectievakjes en keuzerondjes niet langer twee keer gemeldbij het navigeren met tab of snelnavigatie in de bladermodus. (#7960)
* aria-current waarden met de waarde false worden nu daadwerkelijk behandeld als false in plaats van true. (#7892).
* Het laden van de driver voor Windows Onecore stemmen gaat niet langer verkeerd wanneer de geconfigureerde stem verwijderd is. (#7999)
* Het wijzigen van stemmen voor de Windows Onecore stemmen driver is nu een stuk sneller. (#7999)
* De incorrecte uitvoer voor verschillende brailletabellen, waaronder hoofdletters in 8 punts Deens kortschrift braille, is gecorrigeerd. (#7526, #7693)
* NVDA is nu in staat om meerdere soorten opsommingstekens te melden in Microsoft Word. (#6778)
* Het script voor het melden van opmaak zal de positie van de leescursor niet langer verplaatsen. Daarom zal het meerdere keren indrukken van een toegewezen invoerhandeling niet langer verschillende resultaten geven. (#7869)
* Het is niet langer mogelijk om kortschrift braille in te voeren in situaties waarin dit niet ondersteund wordt (d.w.z. er worden niet langer complete woorden naar het systeem gestuurd buiten tekstinhoud en in de bladermodus). (#7306)
* Problemen in de stabiliteit van de verbinding met Handy Tech Easy Braille en Braille Wave leesregels zijn opgelost. (#8016)
* Onder Windows 8 en nieuwer zal NVDA niet langer "onbekend"melden wanneer het Windows+X snelmenu wordt geopend en items in dit menu worden geselecteerd. (#8137)
* Modelspecifieke toewijzingen aan toetsen voor Hims leesregels functioneren nu daadwerkelijk zoals vermeld in de gebruikershandleiding. (#8096)
* NVDA zal nu proberen om problemen met COM-registraties op het systeem op te lossen die onder andere Firefox en Internet Explorer ontoegankelijk kunnen maken en resulteren in het veelvoudig melden van "onbekend". (#2807)
* Er is een oplossing gerealiseerd voor een probleem in Windows Taakbeheer waardoor NVDA gebruikers niet in staat stelde om de inhoud van specifieke procesdetails te bekijken. (#8147)
* Nieuwere Microsoft SAPI5 stemmen hebben niet langer last van vertraging aan het einde van spraakuitvoer, waardoor het navigeren met deze stemmen veel efficiënter verloopt. (#8174)
* NVDA meldt niet langer links-naar-rechts- en rechts-naar-links-markeringen in braille of bij het navigeren per karakter in spraak wanneer de klok wordt bekeken in recente versies van Windows. (#5729)
* Detectie van de scrolltoetsen op Hims Smart Beetle leesregels is opnieuw niet meer onbetrouwbaar. (#6086)
* In sommige besturingselementen voor tekstinvoer, voornamelijk in Delphi-applicaties, is de informatie over bewerken en navigeren een stuk betrouwbaarder dan voorheen. (#636, #8102)
* In Windows 10 RS5, NVDA no longer reports extra redundant information when switching tasks with alt+tab. (#8258)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* The developer info for UIA objects now contains a list of the UIA patterns available. (#5712)
* App modules can now force certain windows to always use UIA by implementing the isGoodUIAWindow method. (#7961)
* The hidden boolean flag "outputPass1Only" in the braille section of the configuration has again been removed. Liblouis no longer supports pass 1 only output. (#7839)

## 2018.1.1

Dit is een speciale versie van NVDA die een probleem oplost in de driver voor de Onecore Windows spraaksynthesizer die zorgde voor het afspelen van de spraak op een te hoge toonhoogte bij gebruik vanaf de Windows 10 April Update (1803). (#8082)

## 2018.1

Hoogtepunten in deze versie zijn ondersteuning voor grafieken in Microsoft Word en PowerPoint, toegevoegde ondersteuning voor brailleleesregels waaronder Eurobraille en de Optelec protocol converter, verbeterde ondersteuning voor Hims en Optelec brailleleesregels, prestatieverbeteringen voor Mozilla Firefox 58 en nieuwer, en nog veel meer.

### Nieuwe Functies

* Het is nu mogelijk om te werken met grafieken in Microsoft Word en Microsoft PowerPoint op een vergelijkbare manier als in Microsoft Excel. (#7046)
 * In Microsoft Word: navigeer in bladermodus naar een ingebedde grafiek en druk op enter om interactie met deze grafiek te starten.
 * In Microsoft PowerPoint tijdens het bewerken van een dia: tab naar een grafiekobject en druk op enter of spatie voor interactie met de grafiek.
 * OM de interactie met een grafiek af te breken, druk op escape.
* Nieuwe taal: Kirgizisch.
* Ondersteuning toegevoegd voor VitalSource Bookshelf. (#7155)
* Ondersteuning toegevoegd voor de Optelec protocol converter, een apparaat dat iemand in staat stelt om een Braille Voyager of Satellite leesregel aan te sturen via het ALVA BC6 communicatieprotocol. (#6731)
* Het is nu mogelijk om braille-invoer te gebruiken met een ALVA 640 Comfort brailleleesregel. (#7733)
 * De braille-invoerfunctionaliteit van NVDA kan gebruikt worden met deze en andere BC6 leesregelsmet firmware 3.0.0 en nieuwer.
* Vroege ondersteuning toegevoegd voor Google Sheets met de braille-modus ingeschakeld. (#7935)
* Ondersteuning voor Eurobraille Esys, Esytime en Iris brailleleesregels. (#7488)

### Veranderingen

* De drivers voor HIMS Braille Sense/Braille EDGE/Smart Beetle en Hims Sync Braille leesregels zijn vervangen door één driver. De nieuwe driver wordt automatisch geactiveerd voor voormalige syncBraille driver gebruikers. (#7459)
 * Sommige toetsen, met name de scrolltoetsen, zijn opnieuw toegewezen om beter aan te sluiten bij hoe deze toetsen gebruikt worden binnen producten van Hims. Raadpleeg de gebruikershandleiding voor meer details.
* Bij het typen op een schermtoetsenbord via aanraakinteractie is het nu standaard zo dat u dubbel moet tikken op een toets om deze te activeren, op de zelfde manier waarop u een ander element zou activeren. (#7309)
 * Om de bestaande modus ("direct typen met aanraken") te gebruiken waarbij het simpelweg optillen van uw vinger genoeg is om de toets te activeren, moet u deze optie inschakelen in het nieuwe instellingenvenster aanraakinteractie in het optiesmenu.
* Het is niet langer nodig om braille expliciet te koppelen aan de focus of de leescursor, aangezien dit vanaf nu standaard automatisch gebeurd. (#2385)
 * Houd er rekening mee dat het koppelen aan de leescursor alleen gebeurt bij het gebruik van een commando voor het bedienen van de leescursor of objectnavigatie. Scrollen activeert dit nieuwe gedrag dus niet.

### Opgeloste Problemen

* Het tonen van meldingen in de bladermodus, zoals het bekijken van opmaakinformatie door middel van het twee keer snel indrukken van NVDA+f, gaat niet langer verkeerd wanneer NVDA geïnstalleerd is in een map waarvan de naam niet-ASCII-tekens bevat. (#7474)
* De focus wordt opnieuw correct hersteld bij het terugkeren naar Spotify vanuit een andere applicatie. (#7689)
* In de Windows 10 Fall Creaters Update gaat het bijwerken van NVDA niet langer verkeerd wanneer Beheerde maptoegang is ingeschakeld vanuit het Windows Defender beveiligingscentrum. (#7696)
* Het detecteren van de scrolltoetsen van Hims Smart Beetle leesregels is niet langer onbetrouwbaar. (#6086)
* Een lichte prestatieverbetering bij het weergeven van grote hoeveelheden inhoud in Mozilla Firefox 58 en nieuwer. (#7719)
* In Microsoft Outlook veroorzaakt het lezen van tabellen niet langer fouten. (#6827)
* Invoerhandelingen van brailleleesregels die modifier-toetsen emuleren, kunnen nu ook gecombineerd worden met andere geëmuleerde systeemtoetsen wanneer één van de invoerhandelingen specifiek is voor een bepaald model leesregel. (#7783)
* Bladermodus in Mozilla Firefox werkt nu naar behoren in pop-ups die getoond worden door extensies als LastPass en bitwarden. (#7809)
* NVDA loopt niet langer vast bij iedere focuswijziging wanneer Firefox of Chrome niet meer reageert, bijvoorbeeld vanwege een bevriezingsprobleem of vastloper. (#7818)
* In Twitter-clients zoals Chicken Nugget zal NVDA de laatste 20 karakters niet langer negeren bij het lezen van tweets met 280 karakters. (#7828)
* NVDA gebruikt nu de juiste taal voor het melden van symbolen bij het selecteren van tekst. (#7687)
* In recente versies van Office 365 is het opnieuw mogelijk om door Excel-grafieken te navigeren met de pijltjestoetsen. (#7046)
* In spraak- en braille-uitvoer worden de diverse statusindicatoren nu altijd in de zelfde volgorde getoond, ongeacht of ze positief of negatief zijn. (#7076)
* In apps zoals Windows 10 Mail heeft NVDA bij het gebruik van backspace niet langer problemen met het melden van verwijderde karakters. (#7456)
* Alle toetsen op de Hims Braille Sense Polaris leesregels werken nu zoals verwacht. (#7865)
* NVDA heeft niet langer problemen met starten onder bepaalde versies van Windows 7 vanwege een foutmelding over een interne api-ms dll. Opstartproblemen konden zich voordoen wanneer een bepaalde versie van de Visual Studio 2017 redistributables geÏnstalleerd was door een andere applicatie. (#7975)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Added a hidden boolean flag to the braille section in the configuration: "outputPass1Only". (#7301, #7693, #7702)
 * This flag defaults to true. If false, liblouis multi pass rules will be used for braille output.
* A new dictionary (braille.RENAMED_DRIVERS) has been added to allow for smooth transition for users using drivers that have been superseded by others. (#7459)
* Updated comtypes package to 1.1.3. (#7831)
* Implemented a generic system in braille.BrailleDisplayDriver to deal with displays which send confirmation/acknowledgement packets. See the handyTech braille display driver as an example. (#7590, #7721)
* A new "isAppX" variable in the config module can be used to detect if NVDA is running as a Windows Desktop Bridge Store app. (#7851)
* For document implementations such as NVDAObjects or browseMode that have a textInfo, there is now a new documentBase.documentWithTableNavigation class that can be inherited from to gain standard table navigation scripts. Please refer to this class to see which helper methods must be provided by your implementation for table navigation to work. (#7849)
* The scons batch file now better handles when  Python 3 is also installed, making use of the launcher to specifically launch python 2.7 32 bit. (#7541)
* hwIo.Hid now takes an additional parameter exclusive, which defaults to True. If set to False, other applications are allowed to communicate with a device while it is connected to NVDA. (#7859)

## 2017.4

Hoogtepunten in deze versie zijn sterk verbeterde ondersteuning voor het web zoals standaard bladermodus voor dialoogvensters binnen websites, beter melden van labels van gegroepeerde velden in bladermodus, ondersteuning voor nieuwe Windows 10 technologieën zoals Windows Defender Application Guard en Windows 10 met ARM64, en automatisch melden van schermstand en batterijstatus.
Let op: deze versie van NVDA ondersteunt Windows XP en Windows Vista niet meer. De minimumvereiste voor NVDA is nu windows 7 met Service Pack 1.

### Nieuwe Functies

* In bladermodus is het nu mogelijk om voorbij/naar het begin van een oriëntatiepunt te springen met behulp van de commando's ga voorbij/naar het begin van een containerelement (komma/shift+komma). (#5482)
* In Firefox, Chrome en Internet Explorer omvat snelnavigatie naar invoer- en formuliervelden nu ook invoervelden met opmaakondersteuning (D.w.z. contentEditable). (#5534)
* In web browsers kan de elementenlijst nu formuliervelden en knoppen weergeven. (#588)
* Initiële ondersteuning voor Windows 10 op ARM64. (#7508)
* Vroege ondersteuning voor het lezen van en interactief navigeren door wiskundige inhoud voor Kindle boeken, mits deze inhoud toegankelijk is. (#7536)
* Ondersteuning toegevoegd voor Azardi e-book reader. (#5848)
* Bij het updaten van add-ons wordt nu versie-informatie gemeld. (#5324)
* Ondersteuning toegevoegd voor nieuwe commandoregelopties om een draagbare versie van NVDA aan te maken. (#6329)
* Ondersteuning voor Microsoft Edge toegevoegd wanneer dit draait binnen Windows Defender Application Guard (#7600)
* Wanneer NVDA gebruikt wordt op een laptop of tablet wordt het vanaf nu gemeld als er een adapter wordt aangesloten/losgekoppeld en als de schermstand wijzigt. (#4574, #4612)
* Nieuwe taal: Macedonisch.
* Nieuwe brailletabellen: Croatisch graad 1, Viëtnamees graad 1. (#7518, #7565)
* Ondersteuning toegevoegd voor de Handy Tech Actilino brailleleesregel. (#7590)
* Braille-invoer wordt nu ondersteund voor leesregels van Handy Tech. (#7590)

### Veranderingen

* Het miminimaal door NVDA ondersteunde besturingssysteem is nu Windows 7 met Service Pack 1, of Windows Server 2008 R2 met Service Pack 1. (#7546)
* Webdialoogvensters in Firefox en Chrome web browsers gebruiken nu automatisch bladermodus, tenzij binnen een webapplicatie. (#4493)
* In bladermodus meldt het gebruik van tab of snelnavigatiecommando's niet langer het verlaten van containers zoals lijsten en tabellen, waardoor navigatie efficiënter wordt. (#2591)
* In bladermodus voor Firefox en Chrome wordt nu de naam van formulierveldgroeperingen gemeld wanneer daarin genavigeerd wordt met snelnavigatie of tab. (#3321)
* In bladermodusomvat het snelnavigatiecommando voor ingebedde objecten (o en shift+o) nu zowel elementen van het type audio en video als met de aria roles application en dialog. (#7239)
* Espeak-ng is bijgewerkt (naar commit 01919cd48a566cdf34347784b2e74554b376e900), wat enkele problemen oplost met het produceren van release builds. (#7385)
* Bij het derde keer activeren van het 'lees statusbalk' commando wordt de inhoud van de statusbalk naar het klembord gekopieerd. (#1785)
* Bij het toewijzen van invoerhandelingen voor een Baum leesregel is het nu mogelijk om specifieke toewijzingen te doen voor het model van de brailleleesregel die momenteel in gebruik is (bijv. VarioUltra of Pronto). (#7517)
* De sneltoets van het filterveld in de elementenlijst in bladermodus is gewijzigd van alt+f in alt+e. (#7569)
* Er is een niet toegewezen invoerhandeling toegevoegd voor bladermodus om het melden van lay-outtabellen snel in of uit te schakelen. U kunt deze optie vinden in de categorie bladermodus van het dialoogvenster Invoerhandelingen. (#7634)
* Liblouis braillevertaler bijgewerkt naar 3.3.0. (#7565)
* De sneltoets van het keuzerondje reguliere expressie in het dialoogvenster voor uitspraakwoordenboeken is gewijzigd van alt+r in alt+e. (#6782)
* De bestanden voor Stem-afhankelijke woordenboeken hebben vanaf nu een versienummer en zijn verplaatst naar de map 'speechDicts/voiceDicts.v1'. (#7592)
* Aanpassingen in versie-afhankelijke bestanden (gebruikersconfiguratie, stem-afhankelijke woordenboeken) worden niet langer opgeslagen wanneer NVDA gestart is vanuit het installatiebestand. (#7688)
* De Braillino, Bookworm en Modular (met oude firmware) brailleleesregels van Handy Tech worden niet langer standaard ondersteund. Installeer de Handy Tech Universele Driver en NVDA add-on om deze leesregels te gebruiken. (#7590)

### Opgeloste Problemen

* Links worden nu als zodanig weergegeven in braille in applicaties zoals Microsoft Word. (#6780)
* NVDA wordt niet langer merkbaar langzamer wanneer er veel tabbladen geopend zijn in Firefox of Chrome web browsers. (#3138)
* De cursorroutingtoetsen van de MDV Lilli brailleleesregel worden niet langer één cel te ver naar rechts geactiveerd. (#7469)
* In Internet Explorer en andere MSHTML-documenten wordt het HTML5 required attribuut nu ondersteund om de vereiste status van een formulierveld aan te geven. (#7321)
* Brailleleesregels worden nu bijgewerkt bij het typen van Arabische karakters in een WordPad-document dat links uitgelijnd is. (#511).
* Toegankelijke labels voor elementen in Mozilla Firefox worden nu gemeld in bladermodus wanneer het label geen deel uitmaakt van de inhoud. (#4773)
* In de windows 10 Creators Update heeft NVDA na een herstart niet langer problemen met het benaderen van Firefox. (#7269)
* Bij het starten van NVDA terwijl Mozilla Firefox de focus heeft, zou bladermodus nu opnieuw beschikbaar moeten zijn. Wanneer bladermodus nog niet werkt, is dit te verhelpen door met alt+tab uit en terug in het venster te navigeren. (#5758)
* Het is nu mogelijk om wiskundige inhoud te bekijken in Google Chrome op een systeem waarop Mozilla Firefox niet geïnstalleerd is. (#7308)
* In vergelijking met eerdere installaties van NVDA zouden het besturingssysteem en andere applicaties stabieler moeten zijn wanneer u NVDA direct start na de installatie, dus voor u het systeem herstart hebt. (#7563)
* Bij het gebruik van een commando voor tekstherkenning (bijv. NVDA+r) geeft NVDA nu een foutmelding in plaats van geen melding wanneer het navigatorobject verdwenen is. (#7567)
* De functionaliteit om terug te scrollen is hersteld voor Freedom Scientific brailleleesregels die een linker bumperbalk bevatten. (#7713)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* "scons tests" now checks that translatable strings have translator comments. You can also run this alone with "scons checkPot". (#7492)
* There is now a new extensionPoints module which provides a generic framework to enable code extensibility at specific points in the code. This allows interested parties to register to be notified when some action occurs (extensionPoints.Action), to modify a specific kind of data (extensionPoints.Filter) or to participate in deciding whether something will be done (extensionPoints.Decider). (#3393)
* You can now register to be notified about configuration profile switches via the config.configProfileSwitched Action. (#3393)
* Braille display gestures that emulate system keyboard key modifiers (such as control and alt) can now be combined with other emulated system keyboard keys without explicit definition. (#6213)
 * For example, if you have a key on your display bound to the alt key and another display key to downArrow, combining these keys will result in the emulation of alt+downArrow.
* The braille.BrailleDisplayGesture class now has an extra model property. If provided, pressing a key will generate an additional, model specific gesture identifier. This allows a user to bind gestures limited to a specific braille display model.
 * See the baum driver as an example for this new functionality.
* NVDA is now compiled with Visual Studio 2017 and the Windows 10 SDK. (#7568)

## 2017.3

Hoogtepunten in deze versie zijn invoer van braille kortschrift, ondersteuning voor nieuwe Windows OneCore stemmen beschikbaar in Windows 10, ingebouwde ondersteuning voor Windows 10 OCR, en veel significante verbeteringen voor Braille en het web.

### Nieuwe Functies

* Een Braille-instelling is toegevoegd: "Meldingen voor onbepaalde tijd tonen". (#6669)
* In Microsoft Outlook berichtenlijsten meldt NVDA nu of een bericht een vlag heeft. (#6374)
* In Microsoft PowerPoint wordt nu het exacte soort vorm gemeld bij het bewerken van een slide (zoals driehoek, cirkel, video of pijl), in plaats van enkel "vorm". (#7111)
* Wiskundige inhoud (aangeboden als MathML) wordt nu ondersteund in Google Chrome. (#7184)
* NVDA kan nu spreken met de nieuwe Windows OneCore stemmen (ook bekend als Microsoft Mobile stemmen) inbegrepen in Windows 10. U vindt ze door Windows OneCore stemmen te selecteren in NVDA's Synthesizer dialoogvenster. (#6159)
* De bestanden van de gebruikersconfiguratie van NVDA kunnen nu worden opgeslagen in de local application data map. Dit wordt bepaald via een instelling in het register. Zie "Systeem-brede parameters" in de Gebruikershandleiding voor meer details. (#6812)
* In web browsers meldt NVDA nu placeholder-waarden voor velden (specificiek, aria-placeholder wordt nu ondersteund). (#7004)
* In Bladermodus voor Microsoft Word is het nu mogelijk naar spelfouten te navigeren via snelnavigatie (w en shift+w). (#6942)
* Ondersteuning toegevoegd voor besturingselementen voor datumselectie in dialoogvensters voor afspraken in Microsoft Outlook. (#7217)
* De momenteel geselecteerde suggestie wordt nu gemeld in Windows 10 Mail aan-/cc-velden en het Windows 10 Instellingen zoekveld. (#6241)
* Er wordt een geluid afgespeeld om aan te geven dat suggesties verschenen zijn in bepaalde zoekvelden in Windows 10 (Bijvoorbeeld het startscherm, instellingen zoeken, Windows 10 mail aan-/cc-velden). (#6241)
* NVDA meldt nu automatisch notificaties in Skype voor Business Desktop, zoals wanneer iemand met u een conversatie start. (#7281)
* NVDA meldt nu automatisch binnenkomende chatberichten in een Skype voor Business conversatie. (#7286)
* NVDA meldt nu automatisch notificaties in Microsoft Edge, zoals wanneer een download start. (#7281)
* U kunt nu ook braille typen in kortschrift op een brailleleesregel met een brailletoetsenbord. Dit omvat ook Nederlands literair braille. Zie de sectie Braille-invoer van de Gebruikershandleiding voor details. (#2439)
* U kunt nu Unicode braillekarakters invoeren via het brailletoetsenbord van een brailleleesregel door Unicode braille te selecteren als de invoertabel in Braille-instellingen. (#6449)
* Ondersteuning toegevoegd voor de SuperBraille brailleleesregel die wordt gebruikt in Taiwan. (#7352)
* Nieuwe brailletabellen: Deens 8 punts computer braille, Litouws, Persisch 8 punts computer braille, Persisch graad 1, Sloveens 8 punts computer braille. (#6188, #6550, #6773, #7367)
* Verbeterde Engels (V.S.) 8 punt computerbrailletabel, inclusief ondersteuning voor opsommingstekens, het euroteken en letters met accenten. (#6836)
* NVDA kan nu de OCR functionaliteit gebruiken die is ingebouwd in Windows 10 om de tekst in afbeeldingen of ontoegankelijke applicaties te herkennen. (#7361)
 * De taal kan worden ingesteld in het nieuwe dialoogvenster Windows 10 OCR in in de NVDA Opties.
 * Om de inhoud te herkennen van het huidige navigatorobject, druk NVDA+r.
 * Zie de sectie Inhoudherkenning van de Gebruikershandleiding voor verdere details.
* U kunt nu kiezen welke contextinformatie wordt getoond op een brailleleesregel als een object focus krijgt via de nieuwe instelling "Te tonen Focuscontext" in het dialoogvenster Braille-instellingen. (#217)
 * Bijvoorbeeld, de opties "Leesregel vullen voor contextveranderingen" en "Alleen bij terugscrollen" kunnen het werken met lijsten en menu's efficiënter maken, omdat de items niet continu van plaats veranderen op de leesregel.
 * Zie de sectie over de instelling "Te tonen Focuscontext" in de Gebruikershandleiding voor verdere details en voorbeelden.
* In Firefox en Chrome ondersteunt NVDA nu complexe dynamische grids zoals spreadsheets waar slechts een gedeelte van de inhoud geladen of weergegeven wordt (specifiek,, de attributen aria-rowcount, aria-colcount, aria-rowindex en aria-colindex die zijn ingevoerd in ARIA 1.1). (#7410)

### Veranderingen

* Er is een niet toegewezen invoerhandeling toegevoegd om NVDA op verzoek te herstarten. U kunt deze optie vinden in de categorie Diversen van het dialoogvenster Invoerhandelingen. (#6396)
* De toetsenbordindeling kan nu worden ingesteld in het welkomscherm van NVDA. (#6863)
* Veel meer soorten besturingselementen en bijbehorende status-indicatoren zijn afgekort voor braille. Ook oriëntatiepunten zijn afgekort. Zie "Braille-afkortingen voor besturingselementen, status-indicatoren en oriëntatiepunten" onder Braille in de Gebruikershandleiding voor een volledige lijst. (#7188, #3975)
* Updated eSpeak NG to 1.49.1. (#7280)
* In het dialoogvenster Braille-instellingen zijn de lijsten van uitvoer- en invoertabellen nu alfabetisch gerangschikt. (#6113)
* Liblouis braille translator bijgewerkt naar 3.2.0. (#6935)
* De standaard brailletabel is nu Uniforme Engelse Braillecode graad 1. (#6952)
* Standaard toont NVDA op een brailleleesregel nu enkel de delen van de inhoudsinformatie die gewijzigd zijn als een object focus krijgt. (#217)
 * Voorheen toonde het altijd zoveel mogelijk contextinformatie, ongeacht of u dezelfde contextinformatie eerder al zag.
 * U kunt terugkeren naar het oude gedrag door de nieuwe instelling "Te tonen Focuscontext" te wijzigen in "Leesregel altijd vullen" in het dialoogvenster Braille-instellingen.
* Bij gebruik van Braille kan de cursor geconfigureerd worden om een andere vorm aan te nemen, afhankelijk van of braille gekoppeld is aan de focus of de leescursor. (#7112)
* Het NVDA logo is bijgewerkt. Het bijgewerkte NVDA logo is een gestileerde mix van de letters NVDA in wit op een paarse achtergrond. Dit garandeeert dat het zichtbaar is tegen elke gekleurde achtergrond, en gebruikt het paars van het NV Access logo. (#7446)

### Opgeloste Problemen

* Bij bewerkbare elementen van het type div wordt in Chrome bladermodus het label niet langer gemeldt als zijnde de waarde. (#7153)
* Het indrukken van end terwijl u zich in bladermodus binnen een leeg Microsoft Word document bevindt, levert niet langer een foutmelding (runtime error) op. (#7009)
* Bladermodus wordt nu correct ondersteund in Microsoft Edge waar een document specifiek voorzien is van de ARIA role document. (#6998)
* In bladermodus kunt u nu selecteren of deselecteren tot het einde van de regel met shift+end, zelfs als de cursor op het laatste karacter van de regel staat. (#7157)
* Als een dialoogvenster een voortgangsbalk bevat, wordt de tekst van het dialoogvenster nu bijgewerkt in braille als de voortgangsbalk wijzigt. Dit betekent bijvoorbeeld dat u nu de resterende tijd kunt lezen in het dialoogvenster dat getoond wordt bij het downloaden van NVDA updates. (#6862)
* NVDA meldt vanaf nu selectiewijzigingen voor bepaalde Windows 10 vervolgkeuzelijsten, zoals Automatisch afspelen in Instellingen. (#6337).
* Er wordt niet langer overtollige informatie gemeld bij het invoeren van afspraken in Microsoft Outlook. (#7216)
* Pieptonen voor bepaalde NVDA dialoogvensters met voortgangsbalken (zoals voor het controleren op updates) worden nu alleen afgespeeld wanneer weergave van voortgangsbalken dusdanig is ingesteld dat pieptonen worden afgespeeld. (#6759)
* In Microsoft Excel 2003 en 2007 worden cellen weer gemeld bij het rondpijlen door een werkblad. (#7243)
* In de Windows 10 Creators Update en nieuwere versies wordt bladermodus opnieuw automatisch ingeschakeld bij het lezen van e-mails in Windows 10 Mail. (#7289)
* Op de meeste brailleleesregels met een brailletoetsenbord verwijdert punt 7 nu het laatst ingevoerde braillekarakter, waar punt 8 zorgt voor een druk op de enter-toets. (#6054)
* Bij het verplaatsen van de cursor in bewerkbare tekst (zoals met de cursortoetsen of backspace) is de gesproken feedback van NVDA in veel gevallen een stuk nauwkeuriger, met name in Chrome en terminal applicaties. (#6424)
* De inhoud van het dialoogvenster om handtekeningen te bewerken in Microsoft Outlook 2016 kan nu worden gelezen. (#7253)
* In Java Swing applicaties is NVDA er niet langer de oorzaak van dat de applicatie crasht bij het navigeren door tabellen. (#6992)
* In de Windows 10 Creators Update zal NVDA Pop-upmeldingen niet langer meerdere keren achter elkaar melden. (#7128)
* In het startmenu in Windows 10 zal NVDA de zoektekst niet langer melden na het indrukken van de Enter-toets om het startmenu te sluiten na een zoekopdracht. (#7370)
* Het uitvoeren van snelnavigatie naar koppen is nu beduidend sneller in Microsoft Edge. (#7343)
* In Microsoft Edge zal het navigeren in bladermodus niet langer grote stukken van bepaalde webpagina's (zoals het Wordpress 2015 thema) overslaan. (#7143)
* In Microsoft Edge worden oriëntatiepunten nu correct vertaald in andere talen dan Engels. (#7328)
* IN braille wordt de selectie nu correct gevolgd wanneer de geselecteerde tekst de leesregelbreedte overschrijdt. Wanneer u bijvoorbeeld meerdere regels selecteert met shift+pijlOmlaag, zal in braille de laatst geselecteerde regel getoond worden. (#5770)
* In Firefox zal NVDA niet langer onnodig meerdere keren "sectie" uitspreken bij het openen van details voor een tweet op twitter.com. (#5741)
* Tabelnavigatiecommando's zijn niet langer beschikbaar voor opmaaktabellen in BladerModus tenzij het melden van lay-outtabellen is ingeschakeld. (#7382)
* In Firefox en Chrome springen tabelnavigatiecommando's in bladermodus nu over verborgen tabelcellen heen. (#6652, #5655)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Timestamps in the log now include milliseconds. (#7163)
* NVDA must now be built with Visual Studio Community 2015. Visual Studio Express is no longer supported. (#7110)
 * The Windows 10 Tools and SDK are now also required, which can be enabled when installing Visual Studio.
 * See the Installed Dependencies section of the readme for additional details.
* Support for content recognizers such as OCR and image description tools can be easily implemented using the new contentRecog package. (#7361)
* The Python json package is now included in NVDA binary builds. (#3050)

## 2017.2

Hoogtepunten in deze versie zijn volledige ondersteuning voor audio-onderdrukking in de Windows 10 Creators Update; oplossingen voor verschillende selectieproblemen in bladermodus, inclusief problemen met Alles Selecteren; significante verbeteringen in de ondersteuning van Microsoft Edge; en verbeteringen op het web zoals aangeven van elementen gemarkeerd als huidig (via aria-current).

### Nieuwe Functies

* Informatie over celranden kan nu worden gemeld in Microsoft Excel via NVDA+f. (#3044)
* Ondersteuning toegevoegd voor aria-current attributen. (#6358)
* Automatische taalverandering wordt nu ondersteund in Microsoft Edge. (#6852)
* Ondersteuning toegevoegd voor Windows Rekenmachine op Windows 10 Enterprise LTSB (Long-Term Servicing Branch) en Server. (#6914)
* Als u het commando read current line driemaal snel uitvoert, wordt de regel gespeld met karakterbeschrijvingen. (#6893)
* Nieuwe taal: Burmees.
* Unicode symbolen zoals pijl omhoog, pijl omlaag en breuksymbolen worden nu juist uitgesproken. (#3805)

### Veranderingen

* Bij het navigeren in de simpele leesoverzichtmodus in applicaties die gebruik maken van UI Automation worden bepaalde irrelevante objecten nu genegeerd om de navigatie eenvoudiger te maken. (#6948, #6950)

### Opgeloste Problemen

* Menu-items op webpagina's kunnen nu geactiveerd worden binnen de bladermodus. (#6735)
* Het drukken van escape in het dialoogvenster configuratieprofielen "Verwijderen bevestigen" zorgt ervoor dat het venster gesloten wordt. (#6851)
* Het mogelijke vastlopen van Mozilla Firefox en andere Gecko-applicaties waar de multi-process-functie is ingeschakeld, is opgelost. (#6885)
* De accuratesse van het melden van de achtergrondkleur in de schermoverzichtmodus is verbeterd bij tekst die getekend is met een transparante achtergrond. (#6467)
* Verbeterde ondersteuning binnen Internet Explorer 11 voor elementbeschrijvingen die beschikbaar zijn op webpagina's (specifiek, ondersteuning voor aria-describedby in iframes en wanneer meerdere ID's zijn opgegeven). (#5784)
* In de Windows 10 Creators Update werkt NVDA's audio-onderdrukking opnieuw zoals in eerdere Windows-versies (d.w.z. Onderdrukken bij spraak- en geluidsuitvoer, Altijd onderdrukken, en geen onderdrukking zijn allemaal beschikbaar). (#6933)
* Bij bepaalde (UIA) controls waarvoor geen toetsenbordsneltoets is gedefineerd, weigert NVDA nniet langer deze te melden of ernaar te navigeren. (#6779)
* In sneltoets-informatie voor bepaalde (UIA) controls worden niet langer twee lege spaties toegevoegd. (#6790)
* Het weigeren van bepaalde toetscombinaties op HIMS leesregels (o.a. spatie+punt4) is opgelost. (#3157)
* Een probleem opgelost bij het openen van een seriële poort op systemen die gebruik maken van bepaalde niet-Engelse talen waarbij het verbinden met brailleleesregels in sommige gevallen mislukte. (#6845)
* De kans dat het configuratiebestand beschadigt bij het afsluiten van Windows is verminderd. Configuratiebestanden worden nu naar een tijdelijk bestand geschreven voordat het eigenlijke configuratiebestand vervangen wordt. (#3165)
* Bij het twee keer uitvoeren van het lees huidige regel commando om de huidige regel te laten spellen, wordt nu de juiste taal gebruikt voor het spellen van karakters. (#6726)
* Het navigeren per regel in Microsoft Edge is nu tot wel drie keer zo snel in de Windows 10 Creators Update. (#6994)
* NVDA meldt niet langer "Web Runtime groepering" wanneer een Microsoft Edge document in de Windows 10 Creators Update de focus krijgt. (#6948)
* Alle bestaande versies van SecureCRT worden nu ondersteund. (#6302)
* Adobe Acrobat Reader loopt niet langer vast in bepaalde PDF-documenten (specifiek, de documenten die lege ActualText attributen bevatten). (#7021, #7034)
* In bladermodus in Microsoft Edge worden interactieve tabellen (ARIA grids) niet langer overgeslagen bij het navigeren naar tabellen met t en shift+t. (#6977)
* In bladermodus zal het indrukken van shift+home na een voorwaardse selectie de selectie zoals verwacht weer ongedaan maken tot het begin van de regel. (#5746)
* In bladermodus gaat het selecteren van alle tekst (control+a) niet langer fout wanneer de cursor zich niet aan het begin van de tekst bevindt (#6909)
* Enkele andere zeldzame selectieproblemen in bladermodus opgelost. (#7131)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Commandline arguments are now processed with Python's argparse module, rather than optparse. This allows certain options such as -r and -q to be handled exclusively. (#6865)
* core.callLater now queues the callback to NVDA's main queue after the given delay, rather than waking the core and executing it directly. This stops possible freezes due to the  core accidentally going to sleep after processing a callback, in the midle of  a modal call such as the desplaying of a message box. (#6797)
* The InputGesture.identifiers property has been changed so that it is no longer normalized. (#6945)
 * Subclasses no longer need to normalize identifiers before returning them from this property.
 * If you want normalized identifiers, there is now an InputGesture.normalizedIdentifiers property which normalizes the identifiers returned by the identifiers property .
* The InputGesture.logIdentifier property is now deprecated. Callers should use InputGesture.identifiers[0] instead. (#6945)
* Removed some deprecated code:
 * `speech.REASON_*` constants: `controlTypes.REASON_*` should be used instead. (#6846)
 * `i18nName` for synth settings: `displayName` and `displayNameWithAccelerator` should be used instead. (#6846, #5185)
 * `config.validateConfig`. (#6846, #667)
 * `config.save`: `config.conf.save` should be used instead. (#6846, #667)
* The list of completions in the autocomplete context menu of the Python Console no longer shows  any object path leading up to the final symbol being completed. (#7023)
* There is now a unit testing framework for NVDA. (#7026)
 * Unit tests and infrastructure are located in the tests/unit directory. See the docstring in the tests\unit\init.py file for details.
 * You can run tests using "scons tests". See the "Running Tests" section of readme.md for details.
 * If you are submitting a pull request for NVDA, you should first run the tests and ensure they pass.

## 2017.1

Hoogtepunten in deze versie zijn melden van secties en tekstkolommen in Microsoft Word; Ondersteuning voor lezen, navigeren en annoteren van boeken in Kindle voor PC; en verbeterde ondersteuning voor Microsoft Edge.

### Nieuwe Functies

* In Microsoft Word kan het soort sectie-einde en het nummer van de sectie nu gemeld worden. Dit schakelt u in met de optie "paginanummers melden" in het dialoogvenster documentopmaak. (#5946)
* In Microsoft Word kunnen de tekstkolommen nu gemeld worden. Dit schakelt u in met de optie "paginanummers melden" in het dialoogvenster documentopmaak. (#5946)
* Automatische taalherkenning wordt nu ondersteund in Wordpad. (#6555)
* Het NVDA-commando om te zoeken (NVDA+control+f) wordt nu ondersteund in bladermodus voor Microsoft Edge. (#6580)
* Snelnavigatie voor knoppen in bladermodus (b en shift+b) worden nu ondersteund in Microsoft Edge. (#6577)
* Bij het kopiëren van een werkblad in Microsoft Excel worden kolom- en rijkoppen onthouden. (#6628)
* Ondersteuning voor lezen en navigeren van boeken in Kindle voor PC versie 1.19, inclusief toegang tot links, voetnoten, afbeeldingen, highlights en gebruikersnotities. Voor meer informatie verwijzen we naar de sectie Kindle voor PC in NVDA handleiding. (#6247, #6638)
* Bladermodus tabel navigatie wordt nu ondersteund in Microsoft Edge. (#6594)
* In Microsoft Excel meldt het commando om de locatie van de leescursor te melden (desktop: NVDA+numpadDelete, laptop: NVDA+delete) nu de naam van het werkblad en de cellocatie. (#6613)
* Een optie toegevoegd aan het Afsluiten dialoogvenster om te herstarten met het loggen van debug-informatie. (#6689)

### Veranderingen

* Het minimum voor de knippersnelheid van de braillecursor is nu 200 ms. Wanneer dit eerder lager was ingesteld, zal dit worden verhoogd naar 200 ms. (#6470)
* Er is een selectievakje toegevoegd aan het dialoogvenster braille-instellingen voor het in/uitschakelen van het knipperen van de braillecursor. Eerder werd een waarde van nul gebruikt om dit te bereiken. (#6470)
* ESpeak NG bijgewerkt (commit e095f008, 10 januari 2017). (#6717)
* Vanwege wijzigingen in de Windows 10 Creators Update is de "Altijd onderdrukken" modus niet meer beschikbaar in de audio-onderdrukkingsinstellingen van NVDA. Deze optie is nog wel beschikbaar bij oudere versies van windows 10. (#6684)
* Vanwege wijzigingen in de Windows 10 Creators Update is het in de "Onderdrukken bij spraak- en geluidsuitvoer" modus niet meer mogelijk om te waarborgen dat de audio volledig onderdrukt is voordat het spreken van de spraak begint. Ook wordt audio na het spreken niet lang genoeg onderdrukt om ervoor te zorgen dat er geen stuitereffect ontstaat in het volume. Deze veranderingen hebben geen effect op oudere versies van windows 10. (#6684)

### Opgeloste problemen

* Een bevriezingsprobleem opgelost in Microsoft Word bij het navigeren per alinea door een groot document in bladermodus. (#6368)
* Tabellen in Microsoft Word die gekopieerd werden uit Microsoft Excel worden niet langer behandeld als lay-outtabellen en worden daardoor niet langer genegeerd. (#5927)
* Wanneer er geprobeerd wordt te typen in de beveiligde weergave van Microsoft Excel maakt NVDA nu een geluid in plaats van het uitspreken van karakters die niet getypt werden. (#6570)
* Het drukken van escape in Microsoft Excel schakelt niet langer onterecht naar bladermodus, tenzij de gebruiker eerder expliciet naar bladermodus is geschakeld met NVDA+spatiebalk en dan focusmodus heeft geactiveerd door enter te drukken op een formulierveld. (#6569)
* NVDA loopt niet langer vast in Microsoft Excel spreadsheets waarin een gehele rij of kolom is samengevoegd. (#6216)
* Het melden van afgesneden/Overschrijdende tekst in cellen in Microsoft Excel zou nu accurater moeten zijn (#6472)
* NVDA meldt nu wanneer een selectievakje alleen-lezen is. (#6563)
* Het NVDA installatieprogramma laat niet langer een waarschuwing zien dat het logo-geluid niet afgespeeld kan worden omdat er geen audioapparaat beschikbaar is. (#6289)
* Besturingselementen in het lint van Microsoft Excel die niet beschikbaar zijn worden nu als zodanig gemeld. (#6430)
* NVDA zal niet langer "venster" aankondigen bij het minimaliseren van vensters. (#6671)
* Getypte karakters worden nu uitgesproken in Universal Windows Platform (UWP) apps (inclusief Microsoft Edge) in de Windows 10 Creators Update. (#6017)
* De muis wordt nu gevolgd over alle schermen op computers met meerdere monitoren. (#6598)
* NVDA wordt niet langer onbruikbaar na het afsluiten van Windows Media Player als de focus op een schuifbalk staat. (#5467)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Profiles and configuration files are now automatically upgraded to meet the requirements of schema modifications. If there is an error during upgrade, a notification is shown, the configuration is reset and the old configuration file is available in the NVDA log at 'Info' level. (#6470)Deze zijn niet vertaald. We verwijzen naar [de Engelstalige versie van dit document](../en/changes.html).

## 2016.4

Hoogtepunten in deze versie zijn verbeterde ondersteuning voor Microsoft Edge; bladermodus in de Windows 10 Mail app; en significante verbeteringen aan de dialoogvensters van NVDA.

### Nieuwe Functies

* NVDA kan nu regelinspringing aangeven met tonen. Dit kunt u instellen met de keuzelijst "Regelinspringing melden" in het dialoogvenster Documentopmaak. (#5906)
* Ondersteuning voor de Orbit Reader 20 brailleleesregel. (#6007)
* Een optie om het spraakweergavevenster te openen bij het opstarten is toegevoegd. Dit kunt u inschakelen via een selectievakje in het spraakweergavevenster. (#5050)
* Bij het opnieuw openen van het spraakweergavevenster, worden de locatie en afmetingen nu teruggezet. (#5050)
* Kruisverwijzingen in Microsoft Word worden nu behandeld als hyperlinks. Ze worden gemeld als links en kunnen geactiveerd worden. (#6102)
* Ondersteuning voor de Baum SuperVario2, Baum Vario 340 en HumanWare Brailliant2 brailleleesregels. (#6116)
* Initiële ondersteuning voor de Verjaardagsupdate van Microsoft Edge. (#6271)
* Bladermodus wordt nu gebruikt bij het lezen van emails in de Windows 10 mail app. (#6271)
* New language: Lithuanian.

### Veranderingen

* Liblouis braillevertaler bijgewerkt naar 3.0.0. Dit geeft significante verbeteringen in de uniforme Engelse braillecode. (#6109, #4194, #6220, #6140)
* In het venster Add-ons Beheren hebben de knoppen Add-on uitschakelen en Add-on inschakelen nu toetsenbordsneltoetsen (resp. alt+u en alt+i). (#6388)
* Verschillende opvullings- en uitlijningsproblemen in dialoogvensters van NVDA zijn opgelost. (#6317, #5548, #6342, #6343, #6349)
* Het dialoogvenster documentopmaak is aangepast zodat de inhoud scrollt. (#6348)
* De layout van het dialoogvenster Uitspraak van symbolen is aangepast zodat de volledige breedte van het dialoogvenster wordt gebruikt voor de symbolenlijst. (#6101)
* In bladermodus in webbrowsers kunt u nu de letttertoetsnavigatiecommando's e en shift+e en f en shift+f gebruiken om naar alleen-lezen invoervelden te gaan. (#4164)
* In de instelllingen voor Documentopmaak is "Wijziging van opmaak achter de cursor weergeven" hernoemd naar "Opmaakwijzigingen achter de cursor melden", omdat dit een invloed heeft op zowel braille als spraak. (#6336)
* Uiterlijk gewijzigd van het NVDA "Welkom dialoogvenster". (#6350)
* In dialoogvensters van NVDA zijn de knoppen "Ok" en "Annuleren" nu rechts uitgelijnd. (#6333)
* Er worden nu draaiknoppen gebruikt voor numerieke invoervelden zoals de instelling "Percentage toonhoogteverandering bij hoofdletters" in het dialoogvenster Stem-instellingen. U kunt de gewenste waarde invoeren of de pijltoetsen omhoog en omlaag gebruiken om de waarde aan te passen. (#6099)
* De manier waarop IFrames worden gemeld, is consistenter gemaakt in alle browsers. IFrames worden nu gemeld als "frame" in Firefox. (#6047)

### Opgeloste problemen

* Een zeldzame fout opgelost bij het afsluiten van NVDA terwijl het spraakweergavevenster open is. (#5050)
* Afbeeldingen maps verschijnen nu zoals verwacht in bladermodus in Mozilla Firefox. (#6051)
* Voorheen gebeurde er niets als u op de Entertoets drukte in het dialoogvenster Woordenboek. Nu worden alle wijzigingen opgeslagen die u hebt aangebracht en wordt het dialoogvenster afgesloten. (#6206)
* Berichten worden nu getoond in braille als u invoermodi wijzigt voor een invoermethode (native invoer/alfanumeriek, halve/volledige xmodus, etc.). (#5892, #5893)
* Als u een add-on uitschakelt en onmiddellijk weer inschakelt of omgekeerd, keert de status van de add-on nu correct terug naar de oorspronkelijke. (#6299)
* In Microsoft Word kunnen velden met paginanummers nu gelezen worden in kopteksten. (#6004)
* In het dialoogvenster symbooluitspraak kan de muis nu worden gebruikt om de focus te verplaatsen tussen de symbolenlijst en de invoervelden. (#6312)
* In bladermodus in Microsoft Word is een probleem opgelost dat de elementenlijst niet liet verschijnen als een document een ongeldige hyperlink bevatte. (#5886)
* Als u het spraakweergavevenster sluit via de taakbalk of de alt+F4 sneltoets, zal het selectievakje in het NVDA-menu nu correct aangeven of het venster al dan niet zichtbaar is. (#6340)
* Het commando Plugins herladen, veroorzaakt niet langer problemen voor getriggerde configuratieprofielen, nieuwe documenten in web browsers en schermoverzichtmodus. (#2892, #5380)
* In de talenlijst van het dialoogvenster Algemene Instellingen, worden talen als Aragonese nu correct getoond in Windows 10. (#6259)
* Geëmuleerde systeemtoetsen (b.v. een knop op een brailleleesregel die een druk op de tabtoets emuleert) worden nu getoond in de gekozen NVDA-taal in invoerhulp en het dialoogvenster Invoerhandelingen koppelen. Voorheen werden ze altijd in het Engels getoond. (#6212)
* Wijzigen van de NVDA-taal (in het dialoogvenster Algemene Instellingen) heeft nu pas effect als NVDA is herstart. (#4561)
* Het is niet langer mogelijk om het Patroonveld leeg te laten voor een nieuwe regel in het spraakwoordenboek. (#6412)
* Een zeldzaam probleem opgelost bij het zoeken naar seriële poorten in sommige systemen wat sommige drivers voor brailleleesregels onbruikbaar maakte. (#6462)
* Genummerde opsommingstekens in tabelcellen worden nu gelezen in Microsoft Word als u per cel navigeert. (#6446)
* It is now possible to assign gestures to commands for the Handy Tech braille display driver in the NVDA Input Gestures dialog. (#6461)
* In Microsoft Excel, pressing enter or numpadEnter when navigating a spreadsheet now correctly reports navigation to the next row. (#6500)
* iTunes no longer intermittently freezes forever when using browse mode for the iTunes Store, Apple Music, etc. (#6502)
* Fixed crashes in 64 bit Mozilla and Chrome-based applications. (#6497)
* In Firefox with multi-process enabled, browse mode and editable text fields now function correctly. (#6380)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* It is now possible to provide app modules for executables containing a dot (.) in their names. Dots are replaced with underscores (_). (#5323)
* The new gui.guiHelper module includes utilities to simplify the creation of wxPython GUIs, including automatic management of spacing. This facilitates better visual appearance and consistency, as well as easing creation of new GUIs for blind developers. (#6287)

## 2016.3

Hoogtepunten in deze versie zijn de mogelijkheid om individuele add-ons uit te schakelen; ondersteuning voor formuliervelden in Microsoft Excel; significante verbeteringen bij het melden van kleuren; correcties en verbeteringen voor verschillende brailleleesregels; en gecorrigeerde en verbeterde ondersteuning voor Microsoft Word.

### Nieuwe Functies

* U kunt nu bladermodus gebruiken om PDF-documenten te lezen in Microsoft Edge, in de windows 10 verjaardagsupdate. (#5740)
* Doorhalen en dubbel doorhalen worden nu gemeld indien van toepassing in Microsoft Word. (#5800)
* In Microsoft Word wordt nu de titel van een tabel gemeld als die beschikbaar is. Als er een beschrijving is, kunt u die bereiken met het commando open lange beschrijving (NVDA+d) in bladermodus. (#5943)
* In Microsoft Word meldt NVDA nu positie-informatie bij wisselen tussen paragrafen (alt+shift+pijlOmlaag en alt+shift+pijlOmhoog). (#5945)
* Als Regelafstand melden is ingeschakeld in NVDA-instellingen voor Documentopmaak, wordt in Microsoft Word regelafstand nu gemeld als u die wijzigt met de voorziene sneltoetsen van Microsoft word, en als u naar tekst gaat met een andere regelafstand. (#2961)
* In Internet Explorer worden HTML5 structuurelementen nu herkend. (#5591)
* Het melden van opmerkingen (zoals in Microsoft Word) kan nu worden uitgeschakeld via het selectievakje Opmerkingen melden in het dialoogvenster met instellingen voor Documentopmaak . (#5108)
* In het venster add-ons beheren kunt u nu individuele add-ons uitschakelen. (#3090)
* Bijkomende toetskoppelingen zijn toegevoegd voor ALVA BC640/680 brailleleesregels. (#5206)
* Er is nu een commando om de brailleleesregel te verplaatsen naar de huidige focus. Momenteel is enkel bij de ALVA BC640/680 serie een toets aan dit commando gekoppeld. Voor andere leeesregels kunt u het zelf koppelen in het dialoogvenster Invoerhandelingen koppelen. (#5250)
* In Microsoft Excel kunt u nu werken met formuliervelden. Ga naar formuliervelden via de elementenlijst of met lettertoetsnavigatie in bladermodus. (#4953)
* In het dialoogvenster invoehrandelingen koppelen kunt U nu een invoerhandeling toewijzen om vereenvoudigde leesmodus in en uit te schakelen. (#6173)

### Veranderingen

* NVDA meldt nu kleuren met een begrijpelijke basisreeks van 9 kleurtinten en 3 schakeringen, met variaties van helderheid en bleekheid. Dit komt in de plaats van de subjectieve en moeilijk te begrijpen kleurnamen. (#6029)
* Het bestaande gedrag van NVDA+F9 en later NVDA+F10 is gewijzigd. Als f10 een eerste keer wordt gedrukt, wordt tekst geselecteerd. Als F10 tweemaal (snel na elkaar) wordt gedrukt, wordt de tekst gekopieerd naar het klembord. (#4636)
* ESpeakNG bijgewerkt naar versie Master 11b1a7b (22 juni 2016). (#6037)

### Opgeloste Problemen

* In bladermodus in Microsoft Word blijft de opmaak nu behouden bij het kopiëren naar het klembord. (#5956)
* In Microsoft Word reageert NVDA nu correct bij gebruik van de tabelnavigatiecommando's van Word zelf (alt+home, alt+end, alt+pageUp en alt+pageDown) en tabelselectiecommando's (navigatiecommando's met shift). (#5961)
* In dialoogvensters van Microsoft Word is de objectnavigatie van NVDA sterk verbeterd. (#6036)
* In sommige toepassingen zoals Visual Studio 2015 worden sneltoetsen (b.v. control+c om te kopiëren) nu gemeld zoals verwacht. (#6021)
* Een zeldzaam probleem opgelost bij het scannen naar seriële poorten dat op sommige systemen sommige drivers voor brailleleesregels onbruikbaar maakte. (#6015)
* Kleuren melden in Microsoft Word is nu meer accuraat omdat er nu rekening wordt gehouden met wijzigingen in Microsoft Office Thema's. (#5997)
* Bladermodus voor Microsoft Edge en ondersteuning voor Start Menu zoeksuggesties is opnieuw beschikbaar in versies van Windows 10 van na april 2016. (#5955)
* In Microsoft Word werkt het automatisch lezen van tabelkoppen beter in het geval van samengevoegde cellen. (#5926)
* In de Windows 10 Mail app weigert NVDA niet langer de inhoud van berichten te lezen. (#5635)
* Als Commandotoetsen uitspreken is ingeschakeld, worden lock-toetsen zoals caps lock niet langer tweemaal aangekondigd. (#5490)
* Dialoogvensters van Windows Gebruikersaccountbeheer worden opnieuw correct gelezen in de Windows 10 verjaardagsupdate. (#5942)
* In de Web Conference Plugin (zoals gebruikt in de website out-of-sight.net) zal NVDA niet langer piepen en wijzigingen van de voortgangsbalk uitspreken die te maken hebben met invoer via de microfoon. (#5888)
* Als u de commando's Volgende/Vorige zoeken uitvoert in Bladermodus zal er nu een correcte hoofdlettergevoelige zoekopdracht gebeuren als de oorspronkelijke zoekopdracht hoofdlettergevoelig was. (#5522)
* Bij het bewerken van woordenboekregels krijgt u nu feedback als een reguliere expressie fout is. NVDA loopt niet langer vast als een woordenboekbestand een verkeerde reguliere expressie bevat. (#4834)
* Als NVDA niet kan communiceren met een brailleleesregel (b.v. omdat hij werd ontkoppeld), zal dit automatisch het gebruik van de leesregel uitschakelen. (#1555)
* Lichtverbeterde perstaties van filters in de Bladermodus Elementenlijst in sommige gevallen. (#6126)
* In Microsoft Excel meldt NVDA de achtergrondpatronen. De gebruikte namen komen nu overeen met die van Excel. (#6092)
* Verbeterde ondersteuning voor het Windows 10 inlogscherm, inclusief aankondigingen van waarschuwingen en het activeren van het wachtwoordveld via aanraken. (#6010)
* NVDA detecteert nu correct de secundaire routingknoppen van de ALVA BC640/680 brailleleesregels. (#5206)
* NVDA kan opnieuw Windows Pop-upmeldingen weergeven in recente versies van Windows 10. (#6096)
* Het kon gebeuren dat NVDA geen toetsaanslagen meer herkende op Baum compatibele en HumanWare Brailliant B brailleleesregels. Dit is niet langer het geval. (#6035)
* Als het melden van regelnummers is ingeschakeld in NVDA's voorkeuren voor Documentopmaak, dan worden regelnummers nu getoond op een brailleleesregel. (#5941)
* Als spraakmodus uit is, verschijnen gemelde objecten (zoals het drukken van NVDA+tab om de focus te melden) nu in het spraakweergavevenster zoals verwacht. (#6049)
* In the Outlook 2016 message list,  associated draft information is no longer reported. (#6219)
* In Google Chrome and Chrome-based browsers in a language other than English, browse mode no longer fails to work in many documents. (#6249)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Logging information directly from a property no longer results in the property  being called recursively over and over again. (#6122)

## 2016.2.1

Deze versie verhelpt het vastlopen van Microsoft Word:

* NVDA veroorzaakt niet langer het vastlopen van Microsoft Word onmiddellijk nadat het wordt gestart in Windows XP. (#6033)
* Melden van grammaticafouten is verwijderd omdat het Microsoft Word liet vastlopen. (#5954, #5877)

## 2016.2

Hoogtepunten in deze versie zijn de mogelijkheid om spelfouten aan te geven tijdens het typen; ondersteuning voor melden van grammaticafouten in Microsoft Word; en verbeteringen en correcties aan de Microsoft Office ondersteuning.

### Nieuwe Functies

* In bladermodus in Internet Explorer en andere MSHTML-elementen, bij gebruik van lettertoetsnavigatie a en shift+a (om naar aantekeningen te springen), gaat u nu ook naar ingevoegde en verwijderde tekst. (#5691)
* In Microsoft Excel meldt NVDA nu het niveau van een groep van cellen, en ook of het is samen- of uitgevouwen. (#5690)
* Het commando Tekstopmaak melden (NVDA+f) tweemaal drukken, toont de informatie in bladermodus zodat u het kan nakijken. (#4908)
* In Microsoft Excel 2010 en hoger worden celschaduw en opvullingen met kleurovergang nu gemeld. Automatisch melden wordt gecontroleerd door de optie Kleuren melden in NVDA-instellingen voor Documentopmaak. (#3683)
* Nieuwe brailletabel: Koine Grieks. (#5393)
* In het dialoogvenster logboek weergeven kunt u de log nu opslaan met de sneltoets control+s. (#4532)
* Als het melden van spelfouten is ingeschakeld en ondersteund in het element dat de focus heeft, zal NVDA een geluid afspelen om u op een spelfout te wijzen tijdens het typen. Dit kunt u uitschakelen met de nieuwe optie "Geluid bij spelfouten tijdens typen" in het dialoogvenster Toetsenbordinstellingen van NVDA. (#2024)
* Grammaticafouten worden nu gemeld in Microsoft Word. Dit kunt u uitschakelen met de nieuwe optie "Grammaticafouten melden" in dialoogvenster met voorkeuren voor Documentopmaak. (#5877)

### Veranderingen

* In bladermodus en invulbare tekstvelden behandelt NVDA de nummerieke enter op de zelfde manier als de gewone entertoets. (#5385)
* NVDA is overgeschakeld naar de eSpeak NG spraaksynthesizer. (#5651)
* In Microsoft Excel negeert NVDA niet langer een kolomkop voor een cel als er een lege rij is tussen de cel en de kop. (#5396)
* In Microsoft Excel worden coördinaten nu aangekondigd voorafgaand aan de koppen om verwarring te voorkomen tussen koppen en inhoud. (#5396)

### Opgeloste Problemen

* Als u in bladermodus lettertoetsnavigatie probeert te gebruiken om naar een element te gaan dat niet is ondersteund voor het document, meldt NVDA dat dit niet ondersteund is in plaats van te melden dat er in die richting geen element is. (#5691)
* Bij het weergeven van de lijst met werkbladen in de Elementenlijst in Microsoft Excel, worden nu ook werkbladen opgenomen die enkel grafieken bevatten. (#5698)
* NVDA meldt niet langer overbodige informatie bij het schakelen tussen vensters in een Java-toepassing met meerdere venster zoals IntelliJ of Android Studio. (#5732)
* In Scintilla-gebaseerde editors zoals Notepad++ wordt braille nu correct bijgewerkt als u de cursor beweegt via een brailleleesregel. (#5678)
* NVDA loopt niet langer soms vast bij het inschakelen van braille-uitvoer. (#4457)
* In Microsoft Word wordt alinea-inspringing nu altijd gemeld in de meeteenheid die de gebruiker kiest (b.v. centimeters of inches). (#5804)
* Bij gebruik van een brailleleesregel worden veel NVDA-berichten die voorheen enkel werden uitgesproken nu ook in braille getoond. (#5557)
* In toegankelijke Java-toepassingen wordt nu het niveau van items in een boomstructuur gemeld. (#5766)
* Vastlopers opgelost in Adobe Flash in Mozilla Firefox in sommige gevallen. (#5367)
* In Google Chrome en Chrome-gebaseerde browsers kunnen documenten binnen dialoogvensters of toepassingen nu gelezen worden in bladermodus. (#5818)
* In Google Chrome en Chrome-gebaseerde browsers kunt u NVDA nu verplichten om naar bladermodus over te schakelen in web-dialoogvensters of toepassingen. (#5818)
* Het verplaatsen van de focus naar bepaalde elementen in Internet Explorer en andere MSHTML-elementen (specifiek waar aria-activedescendant is gebruikt) schakelt niet langer onterecht naar bladermodus. Dit gebeurde bijvoorbeeld als u naar suggesties ging in adresvelden bij het schrijven van een bericht in Gmail. (#5676)
* In Microsoft Word loopt NVDA niet langer vast in grote tabellen als melden van tabelrij/kolomkoppen is ingeschakeld. (#5878)
* In Microsoft word meldt NVDA niet langer onterecht tekst als een kop als die een overzichtsniveau heeft maar geen ingebouwde kopstijl. (#5186)
* In bladermodus in Microsoft Word werken de commando's Achter/Naar begin van containerobject springen (komma en shift+komma) nu voor tabellen. (#5883)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* NVDA's C++ components are now built with Microsoft Visual Studio 2015. (#5592)
* You can now present a text or HTML message to the user in browse mode using ui.browseableMessage. (#4908)
* In the User Guide, when a &lt;!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) -->

## 2016.1

Hoogtepunten in deze versie zijn de mogelijkheid om het volume van andere geluiden te verlagen; verbeteringen aan braille-uitvoer en ondersteuning voor brailleleesregels; verschillende belangrijke correcties aan Microsoft Office ondersteuning; en correcties aan bladermodus in iTunes.

### Nieuwe Functies

* Nieuwe brailletabellen: Pools 8 punts computerbraille, Mongools. (#5537, #5574)
* U kunt de braillecursor uitschakelen en zijn vorm veranderen via de nieuwe opties Cursor weergeven en Cursorvorm in het dialoogvenster Braille-instelllingen. (#5198)
* NVDA kan nu via Bluetooth verbinden met een HIMS Smart Beetle brailleleesregel. (#5607)
* NVDA kan het volume verlagen van andere geluiden als het is geïnstalleerd op Windows 8 en hoger. U kunt deze audio-onderdrukkingsmodus instellen in de Synthesizer-instellingen of door NVDA+shift+d te drukken. (#3830, #5575)
* Ondersteuning voor de APH Refreshabraille in HID mode en de Baum VarioUltra en Pronto! via een USB-verbinding. (#5609)
* Ondersteuning voor HumanWare Brailliant BI/B braille leesregels met het protocol ingesteld als OpenBraille. (#5612)

### Veranderingen

* Melden van nadruk is nu standaard uitgeschakeld. (#4920)
* In het dialoogvenster Elementenlijst in Microsoft Excel is de sneltoets voor Formules gewijzigd naar alt+r zodat hij verschilt van de sneltoets voor het Filterveld. (#5527)
* LibLouis braillevertaler bijgewerkt naar 2.6.5. (#5574)
* Het woord "tekst" wordt niet langer gemeld als de focus of de leescursor naar tekstobjecten beweegt. (#5452)

### Opgeloste problemen

* In iTunes 12 update bladermodus nu correct als een nieuwe pagina laadt in de iTunes Store. (#5191)
* In Internet Explorer en andere MSHTML-elementen gedraagt naar specifieke kopniveau's gaan met lettertoetsnavigatie zich nu zoals verwacht als het kopniveau is overschreven voor toegankelijkheidsredenen (specifiek als aria-level het niveau overschrijft van een h-tag). (#5434)
* In Spotify landt de focus minder vaak op "unbekende" objecten. (#5439)
* Focus wordt nu correct teruggezet bij het terugkeren naar Spotify vanuit een andere toepassing. (#5439)
* Bij het schakelen tussen bladermodus en focusmodus wordt de modus zowel in braille als via spraak gemeld. (#5239)
* De Startknop op de Taakbalk wordt niet langer gemeld als een lijst en/of als geselecteerd in sommige versies van Windows. (#5178)
* Berichten als "ingevoegd" worden niet langer gemeld bij het opstellen van berichten in Microsoft Outlook. (#5486)
* Bij gebruik van een brailleleesregel en tekst is geselecteerd op de huidige regel (b.v. bij het zoeken in een tekstverwerker naar tekst die op dezelfde regel voorkomt), zal de brailleleesregel scrollen al sdat nodig is. (#5410)
* NVDA sluit niet langer stil af bij het sluiten van een Windows opdrachtprompt met alt+f4 in Windows 10. (#5343)
* Als u het soort element wijzigt in de Elementenlijst in bladermodus, wordt het filterveld nu leeggemaakt. (#5511)
* Als u de muis beweegt in tekstvelden in Mozilla-toepassingen, leest dit opnieuw de betreffende regel, woord, etc. zoals verwacht in plaats van de hele inhoud. (#5535)
* Bij het bewegen van de muis in tekstvelden in Mozilla-toepassingen stopt het lezen niet langer bij elementen als links binnen het woord of de regel worden gelezen. (#2160, #5535)
* In Internet Explorer kan de shoprite.com website nu worden gelezen in bladermodus. Vroeger werd hij gemeld als leeg. (Specifiek worden misvormde lang-attributen nu keurig opgevangen.) (#5569)
* In Microsoft Word worden bijgehouden wijzigingen zoals "ingevoegd" niet langer gemeld als bijgehouden wijzigingen niet worden weergegeven. (#5566)
* Als een aankruisknop focus krijgt, meldt NVDA nu wanneer hij verandert van ingedrukt naar niet ingedrukt. (#5441)
* Melden van veranderingen van muisvormen werkt opnieuw zoals verwacht. (#5595)
* Als regelinspringing wordt uitgesproken, worden non-breaking spaces nu behandeld als normale spaties. Voorheen kon dit aankondigingen veroorzaken als "spatie spatie spatie" in plaats van "3 spaties". (#5610)
* Bij het sluiten van een moderne Microsoft invoermethode kandidatenlijst wordt de focus correct teruggezet naar ofwel de invoersamenstelling of het onderliggende document. (#4145)
* In Microsoft Office 2013 en later, als het lint is ingesteld om enkel tabs te tonen, worden items in het lint opnieuw gemeld zoals verwacht als een tab wordt geactiveerd. (#5504)
* Oplossingen en verbeteringen voor aanraakscherm gebarendetectie en -koppeling. (#5652)
* Aanraakscherm hovers worden niet langer gemeld in invoerhulp. (#5652)
* NVDA weigert niet langer opmerkingen op te lijsten in de Elementenlijst voor Microsoft Excel als de opmerking op samengevoegde cellen is geplaatst. (#5704)
* In een zeer uitzonderlijk geval weigert NVDA niet langer inhoud te lezen van een werkblad in Microsoft Excel met melden van rij- en kolomkoppen ingeschakeld. (#5705)
* In Google Chrome werkt navigatie binnen een Invoersamenstelling nu zoals verwacht bij het invoeren van Oost-Aziatische karakters. (#4080)
* Bij het zoeken van Apple Music in iTunes wordt bladermodus voor de zoekresultaten nu bijgewerkt zoals verwacht. (#5659)
* Als u in Microsoft Excel shift+f11 drukt om een nieuw werkblad te maken, wordt nu uw nieuwe positie gemeld in plaats van helemaal niets. (#5689)
* Problemen opgelost met de uitvoer op de brailleleesregel bij het ingeven van Koreaanse karakters. (#5640)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* The new audioDucking.AudioDucker class allows code which outputs audio to indicate when background audio should be ducked. (#3830)
* nvwave.WavePlayer's constructor now has a wantDucking keyword argument which specifies whether background audio should be ducked while audio is playing. (#3830)
 * When this is enabled (which is the default), it is essential that WavePlayer.idle be called when appropriate.
* Enhanced I/O for braille displays: (#5609)
 * Thread-safe braille display drivers can declare themselves as such using the BrailleDisplayDriver.isThreadSafe attribute. A driver must be thread-safe to benefit from the following features.
 * Data is written to thread-safe braille display drivers in the background, thus improving performance.
 * hwIo.Serial extends pyserial to call a callable when data is received instead of drivers having to poll.
 * hwIo.Hid provides support for braille displays communicating via USB HID.
 * hwPortUtils and hwIo can optionally provide detailed debug logging, including devices found and all data sent and received.
* There are several new properties accessible from touch screen gestures: (#5652)
 * MultitouchTracker objects now contain a childTrackers property which contains the MultiTouchTrackers the tracker was composed of. For example, 2 finger double tap has child trackers for two 2-finger taps. The 2-finger taps themselves have child trackers for two taps.
 * MultiTouchTracker objects now also contain a rawSingleTouchTracker property if the tracker was the result of one single finger doing a tap, flick or hover. The SingleTouchTracker allows access to the underlying ID assigned to the finger by the operating system and whether or not the finger is still in contact at the current time.
 * TouchInputGestures now have x and y properties, removing the need to access the tracker for trivial cases.
 * TouchInputGesturs now contain a preheldTracker property, which is a MultitouchTracker object representing the other fingers held while this action was being performed.
* Two new touch screen gestures can be emitted: (#5652)
 * Plural tap and holds (e.g. double tap and hold)
 * A generalized identifier with finger count removed for holds (e.g. hold+hover for 1finger_hold+hover).

## 2015.4

Hoogtepunten in deze versie zijn prestatieverbeteringen in Windows 10; opname in het Toegankelijkheidscentrum in Windows 8 en hoger; verbeteringen voor Microsoft Excel, zoals een lijst van werkbladen en het hernoemen ervan, en toegang tot vergrendelde cellen in beveiligde werkbladen; en ondersteuning voor het bewerken van rich text in Mozilla Firefox, Google Chrome en Mozilla Thunderbird.

### Nieuwe Functies

* NVDA verschijnt nu in het Toegankelijkheidscentrum in Windows 8 en hoger. (#308)
* Bij het bewegen tussen cellen in Excel, worden veranderingen in de opmaak nu automatisch gemeld als die opties zijn ingeschakeld in het dialoogvenster documentopmaak instellingen van NVDA. (#4878)
* Aan het dialoogvenster documentopmaak instellingen is de optie Nadruk Melden toegevoegd. Ze is standaard ingeschakeld en laat NVDA automatisch melden dat tekst benadrukt is in documenten. Momenteel is dit enkel ondersteund voor em en strong tags in Bladermodus voor Internet Explorer en andere MSHTML-elementen. (#4920)
* De aanwezigheid van ingevoegde en verwijderde tekst wordt nu gemeld in Bladermodus voor Internet Explorer en andere MSHTML-elementen als de optie Aangebrachte wijzigingen in de tekst melden, is ingeschakeld. (#4920)
* Bij het bekijken van gemaakte wijzigingen in de Elementenlijst van NVDA voor Microsoft Word, wordt meer informatie getoond zoals welke opmaakeigenschappen gewijzigd zijn. (#4920)
* In Microsoft Excel zie je een lijst van werkbladen met de mogelijkheid ze te hernoemen via de Elementenlijst (NVDA+f7). (#4630, #4414)
* Je kan nu configureren om symbolen al dan niet naar spraaksynthesizers te sturen (bijvoorbeeld om een pauze in te lassen of de intonatie te wijzigen) in het dialoogvenster Symbooluitspraak. (#5234)
* In Microsoft Excel meldt NVDA nu de invoerberichten die de auteur van het werkblad heeft toegevoegd aan cellen. (#5051)
* Ondersteuning voor de Baum Pronto! V4 en VarioUltra brailleleesregels via Bluetooth-aansluiting. (#3717)
* Ondersteuning voor het bewerken van rich text in Mozilla applicaties zoals Google Docs met braille-ondersteuning ingeschakeld in Mozilla Firefox en HTML-opstelling in Mozilla Thunderbird. (#1668)
* Ondersteuning voor het bewerken van rich text in Google Chrome en Chrome-gebaseerde browsers zoals Google Docs met braille-ondersteuning ingeschakeld. (#2634)
 * Dit vereist Chrome versie 47 of hoger.
* In bladermodus in Microsoft Excel kan je nu navigeren naar vergrendelde cellen in beveiligde werkbladen. (#4952)

### Veranderingen

* De optie Aangebrachte wijzigingen in de tekst melden, is nu standaard ingeschakeld in het dialoogvenster Documentopmaak instellingen. (#4920)
* Tijdens het navigeren per karakter in Microsoft Word met de ingeschakelde optie Aangebrachte wijzigingen in de tekst melden, wordt nu minder informatie gemeld bij wijzigingen, waardoor navigatie efficiënter verloopt. Om de extra informatie te zien, gebruikt u de Elementenlijst. (#4920)
* Liblouis braillevertaler bijgewerkt naar 2.6.4. (#5341)
* Heel wat symbolen (waaronder eenvoudige wiskundige symbolen) zijn verplaatst naar het niveau sommige zodat ze standaard worden uitgesproken. (#3799)
* Als de synthesizer het ondersteunt, zou de spraak nu moeten pauzeren voor haakjes en het gedachtenstreepje (–). (#3799)
* Bij het selecteren van tekst, wordt de tekst gemeld voor de aanduiding "geselecteerd" in plaats van erna. (#1707)

### Opgeloste problemen

* Grote performantieverbeteringen bij het navigeren door de berichtenlijst van Outlook 2010/2013. (#5268)
* In een grafiek in Microsoft Excel werkt het navigeren met bepaalde toetsen (zoasl wisselen van werkblad met control+pageUp en control+pageDown) nu correct. (#5336)
* Het visuele uitzicht is gecorrigeerd van de knoppen in het waarschuwingsvenster dat verschijnt als u NVDA probeert te downgraden. (#5325)
* In Windows 8 en hoger start NVDA nu een stuk vroeger als het is geconfigureerd om te starten na het aanmelden bij Windows. (#308)
 * Als u dit heeft ingeschakeld in een vorige versie van NVDA, dan moet u het uitschakelen en het opnieuw inschakelen om deze verandering van kracht te laten worden. Volg deze procedure:
  1. Open het dialoogvenster met Algemene instellingen.
  1. Schakel dit selectievakje uit: NVDA &automatisch starten nadat ik me bij windows heb aangemeld.
  1. Druk op de OK knop.
  1. Open opnieuw het dialoogvenster met Algemene instellingen.
  1. Schakel het selectievakje in: NVDA &automatisch starten nadat ik me bij windows heb aangemeld".
  1. Druk op de OK knop.
* Performantieverbeteringen voor UI Automation inclusief File Explorer en Task Viewer. (#5293)
* NVDA schakelt nu correct naar focusmodus bij het tabben naar alleen-lezen ARIA grid controls in Bladermodus voor Mozilla Firefox en andere Gecko-gebaseerde controls. (#5118)
* NVDA meldt nu correct "geen vorig" in plaats van "geen volgend" als er geen objecten meer zijn bij het vegen naar links op een aanraakscherm.
* Problemen opgelost bij het typen van meerdere woorden in het filterveld in het dialoogvenster Invoerhandelingen koppelen. (#5426)
* NVDA loopt niet langer vast in sommige gevallen bij het opnieuw verbinden via USB met een HumanWare Brailliant BI/B series leesregel. (#5406)
* In talen met samengevoegde karakters werken omschrijvingen van karakters nu zoals verwacht voor Engelse karakters in hoofdletters. (#5375)
* NVDA zou niet langer af en toe mogen vastlopen bij het openen van het Startmenu in Windows 10. (#5417)
* In Skype voor Desktop worden meldingen die verschijnen voor een eerdere melding verdween nu gemeld. (#4841)
* Meldingen worden nu correct gemeld in Skype voor Desktop 7.12 en hoger. (#5405)
* NVDA meldt de focus nu correct bij het sluiten van een contextmenu in sommige toepassingen zoals Jart. (#5302)
* In Windows 7 en hoger wordt Kleur opnieuw gemeld in bepaalde toepassingen zoals Wordpad. (#5352)
* Bij het bewerken in Microsoft PowerPoint meldt een druk op de enter-toets nu automatisch de ingegeven tekst zoals een opsommingsteken of getal. (#5360)

## 2015.3

Hoogtepunten in deze versie zijn initiële ondersteuning voor Windows 10; de mogelijkheid om lettertoetsnavigatie uit te schakelen in bladermodus (nuttig voor sommige web apps); verbeteringen in Internet Explorer; en correcties voor rommelige tekst tijdens het typen in bepaalde toepassingen als braille is ingeschakeld.

### Nieuwe Functies

* De aanwezigheid van spelfouten wordt aangekondigd in bewerkbare velden voor Internet Explorer en andere MSHTML-elementen. (#4174)
* Veel meer unicode wiskunde-symbolen worden nu uitgesproken als ze in tekst voorkomen. (#3805)
* Zoeksuggesties in het Windows 10 startscherm worden automatisch gemeld (#5049)
* Ondersteuning voor de EcoBraille 20, EcoBraille 40, EcoBraille 80 en EcoBraille Plus brailleleesregels. (#4078)
* In bladermodus kunt u nu lettertoetsnavigatie in- en uitschakelen door NVDA+shift+spatiebalk te drukken. Uitgeschakeld betekent dat ingetoetste letters doorgegeven worden aan de applicatie, wat handig is voor sommige webtoepassingen zoals Gmail, Twitter en Facebook. (#3203)
* Nieuwe brailletabellen: Fins 6 punts, Iers graad 1, Iers graad 2, Koreaans graad 1 (2006), Koreaans graad 2 (2006). (#5137, #5074, #5097)
* Het QWERTY toetsenbord van de Papenmeier BRAILLEX Live Plus brailleleesregel wordt nu ondersteund. (#5181)
* Experimentele ondersteuning voor de Microsoft Edge webbrowser en browsing engine in Windows 10. (#5212)
* Nieuwe taal: Kannada.

### Veranderingen

* Liblouis braillevertaler bijgewekrt naar 2.6.3. (#5137)
* Als u een oudere versie van NVDA probeert te installeren dan degene die momenteel is geïnstalleerd, zal u nu gewaarschuwd worden dat dit niet aanbevolen is en dat NVDA helemaal verwijderd moet worden voordat u doorgaat. (#5037)

### Opgeloste problemen

* In bladermodus voor Internet Explorer en andere MSHTML-elementen gaat de snelnavigatie per formulierveld niet langer foutief naar lijstonderdelen die louter visueel zijn. (#4204)
* Voor ARIA tab panels In Firefox probeert NVDA niet langer een beschrijving te maken met alle tekst die ze bevatten. (#4638)
* In Internet Explorer en andere MSHTML-elementen, wordt bij het tabben in secties, artikels of dialoogvensters niet langer alle inhoud van de container als naam gemeld. (#5021, #5025)
* Bij gebruik van Baum/HumanWare/APH brailleleesregels met een braille toetsenbord stopt de braille-invoer niet langer te werken na het drukken op een andere soort toets op de leesregel. (#3541)
* In Windows 10 wordt niet langer irrelevante informatie gemeld bij het drukken van alt+tab of alt+shift+tab om tussen toepassingen te schakelen. (#5116)
* Getypte tekst is niet langer rommelig bij gebruik van bepaalde toepassingen zoals Microsoft Outlook met een brailleleesregel. (#2953)
* In bladermodus in Internet Explorer en andere MSHTML-elementen, wordt nu de juiste inhoud gemeld als een element verschijnt of wijzigt en krijgt onmiddellijk de focus. (#5040)
* In bladermodus in Microsoft Word, update lettertoetsnavigatie nu de brailleleesregel en de leescursor zoals men verwacht. (#4968)
* In braille worden niet langer overbodige spaties getoond tussen of na indicatoren voor controls en opmaak. (#5043)
* Als een toepassing traag reageert en u schakelt weg van die toepassing, is NVDA in de meeste gevallen nu veel meer responsive in andere toepassingen. (#3831)
* Windows 10 Pop-upmeldingen worden nu gemeld zoals men verwacht. (#5136)
* In bepaalde (UI Automation) keuzelijsten wordt nu de waarde gemeld als ze verandert. Vroeger waren er gevallen waar dit niet werkte.
* In bladermodus in web browsers werkt tabben nu zoals men verwacht na het tabben naar een frame document. (#5227)
* Het Windows 10 lock screen kan nu weggestuurd worden bij gebruik van een aanraakscherm. (#5220)
* In Windows 7 en hoger is tekst niet langer rommelig bij het typen in bepaalde toepassingen zoals Wordpad en Skype met een brailleleesregel. (#4291)
* Op het Windows 10 lock screen is het niet langer mogelijk het klembord te lezen, draaiende toepassingen te bereiken met de leescursor, de NVDA-configuratie te wijzigen, etc. (#5269)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* You can now inject raw input from a system keyboard that is not handled natively by Windows (e.g. a QWERTY keyboard on a braille display) using the new keyboardHandler.injectRawKeyboardInput function. (#4576)
* eventHandler.requestEvents has been added to request particular events that are blocked by default; e.g. show events from a specific control or certain events even when in the background. (#3831)
* Rather than a single i18nName attribute, synthDriverHandler.SynthSetting now has separate displayNameWithAccelerator and displayName attributes to avoid reporting of the accelerator in the synth settings ring in some languages.
 * For backwards compatibility, in the constructor, displayName is optional and will be derived from displayNameWithAccelerator if not provided. However, if you intend to have an accelerator for a setting, both should be provided.
 * The i18nName attribute is deprecated and may be removed in a future release.

## 2015.2

Hoogtepunten in deze versie zijn de mogelijkheid om grafieken te lezen in Microsoft Excel en ondersteuning voor lezen van, interageren met, en navigeren in wiskundige inhoud.

### Nieuwe Functies

* Per zin vooruit en achteruit bewegen is nu mogelijk in Microsoft Word met respectievelijk alt+pijlOmlaag en alt+pijlOmhoog. (#3288)
* Nieuwe brailletabellen voor verschillende Indische talen. (#4778)
* In Microsoft Excel meldt NVDA nu als de inhoud van een cel is overschreden of afgesneden. (#3040)
* In Microsoft Excel kunt u nu de Elementenlijst (NVDA+f7) gebruiken voor een lijst van grafieken, opmerkingen en formules. (#1987)
* Ondersteuning voor het lezen van grafieken in Microsoft Excel. Selecteer de grafiek via de Elementenlijst (NVDA+f7) en gebruik dan de pijltoetsen om tussen de gegevenspunten te bewegen. (#1987)
* Als u MathPlayer 4 van Design Science gebruikt, kan NVDA nu wiskundige inhoud lezen en ermee interageren in internetbrowsers en in Microsoft Word en PowerPoint. Voor meer details verwijzen we naar het hoofdstuk "Inhoud van wiskundige aard lezen" van de gebruikershandleiding. (#4673)
* Via het dialoogvenster Invoerhandelingen koppelen, is het nu mogelijk om invoerhandelingen (toetsenbordsneltoetsen, aanraakgebaren, enz.) te koppelen aan alle dialoogvensters met instellingen van NVDA en opties voor documentopmaak. (#4898)

### Veranderingen

* In het dialoogvenster Documentopmaak zijn de sneltoetsen gewijzigd voor het melden van lijsten, links, regelnummers en lettertypes. (#4650)
* In het dialoogvenster Muisinstellingen zijn sneltoetsen toegevoegd voor "Geluidscoördinatie gebruiken bij verplaatsen van muis" en "Schermhelderheid bepaalt Volume audio-coördinatie". (#4916)
* Melden van kleurnamen is aanzienlijk verbeterd. (#4984)
* Liblouis braillevertaler bijgewerkt naar 2.6.2. (#4777)

### Opgeloste Problemen

* In bepaalde Indische talen worden omschrijvingen van karakters nu correct behandeld voor samengevoegde karakters. (#4582)
* Als de optie "Vertrouw taal van stem bij het verwerken van karakters en symbolen" ingeschakeld is, zal het dialoogvenster Uitspraak van interpunctie en symbolen nu correct de stemtaal gebruiken. Ook wordt de taal waarvoor de uitspraak gewijzigd wordt getoond als titel van het dialoogvenster. (#4930)
* In Internet Explorer en andere MSHTML-elementen worden getypte karakters niet langer foutief aangekondigd in bewerkbare keuzelijsten zoals het zoekveld op de Google homepage. (#4976)
* Als u in Microsoft Officetoepassingen kleuren selecteert, worden de kleurnamen nu gemeld. (#3045)
* Deense brailleweergave hersteld. (#4986)
* U kunt opnieuw PageUp/pageDown gebruiken om dia's te wisselen in een PowerPoint presentatie. (#4850)
* In Skype voor Desktop 7.2 en hoger worden typing meldingen nu gemeld en er zijn problemen opgelost onmiddellijk nadat de focus uit een conversatie beweegt. (#4972)
* Problemen opgelost bij het typen van bepaalde leestekens/symbolen zoals haken in het filterveld in het dialoogvenster Invoerhandelingen koppelen. (#5060)
* Als u in Internet Explorer en andere MSHTML-elementen g of shift+g drukt om te navigeren naar afbeeldingen komt u nu ook bij elementen die gemarkeerd zijn als afbeelding via ARIA role img. (#5062)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* brailleInput.handler.sendChars(mychar) will no longer filter out a character if it is equal to the previous character by ensuring that the key sent is correctly released. (#4139)
* Scripts for changing touch modes will now honor new labeles added to touchHandler.touchModeLabels. (#4699)
* Add-ons can provide their own math presentation implementations. See the mathPres package for details. (#4509)
* Speech commands have been implemented to insert a break between words and to change the pitch, volume and rate. See BreakCommand, PitchCommand, VolumeCommand and RateCommand in the speech module. (#4674)
 * There is also speech.PhonemeCommand to insert specific pronunciation, but the current implementations only support a very limited number of phonemes.

## 2015.1

Hoogtepunten in deze versie zijn bladermodus voor Microsoft Word en Outlook documenten; drastisch verbeterde ondersteuning voor de Desktop client van Skype; en aanzienlijke verbeteringen aan Microsoft Internet Explorer.

### Nieuwe Functies

* U kunt nu nieuwe symbolen toevoegen in het dialoogvenster Uitspraak van interpunctie en symbolen. (#4354)
* In het dialoogvenster INvoerhandelingen koppelen kunt u nu het veld "Filter op" gebruiken om enkel invoerhandelingen weer te geven die bepaalde woorden bevatten. (#4458)
* NVDA meldt nu automatisch nieuwe tekst in mintty. (#4588)
* In het zoekvenster van de bladermodus bevindt zich nu een optie voor het uitvoeren van een hoofdlettegevoelige zoekopdracht. (#4584)
* Lettertoetsnavigatie (h om per kop te navigeren, etc.) en de lijst met elementen (NVDA+f7) zijn nu beschikbaar in Microsoft Word documenten door het inschakelen van bladermodus met NVDA+spatie. (#2975)
* De mogelijkheid tot het lezen van HTML-berichten in Microsoft Outlook 2007 en nieuwer heeft belangrijke verbeteringen ondergaan. Bladermodus wordt automatisch geactiveerd voor deze berichten. Wanneer bladermodus in bepaalde zeldzame situaties niet geactiveerd wordt, kunt u activatie forceren met NVDA+spatie. (#2975)
* Tabel kolomkoppen in Microsoft word worden automatisch gemeld bij tabellen waarbij expliciet een rij met koppen is ingesteld door de auteur via de Microsoft word tabeleigenschappen. (#4510)
 * Dit werkt echter niet automatisch voor tabellen waarbij rijen samengevoegd zijn. In deze situaties kunt u de kolomkoppen handmatig instellen in NVDA met NVDA+shift+c.
* In Skype voor Desktop worden notificaties nu gemeld. (#4741)
* In Skype voor Desktop kunt u nu een overzicht van de meest recente berichten krijgen door gebruik te maken van NVDA+control+1 tot en met NVDA+control+0; bijv. NVDA+control+1 voor het meest recente bericht en NVDA+control+0 voor het tiende meest recente bericht. (#3210)
* In een conversatie in Skype voor Desktop zal NVDA nu melden wanneer een contactpersoon aan het typen is. (#3506)
* NVDA kan nu stil geïnstalleerd worden via de commandoregel zonder de geïnstalleerde versie automatisch te starten na de installatie. Om dit te doen gebruikt u de optie --install-silent. (#4206)
* Ondersteuning voor de Papenmeier BRAILLEX Live 20, BRAILLEX Live en BRAILLEX Live Plus brailleleesregels. (#4614)

### Veranderingen

* In het NVDA instellingenvenster Documentopmaak heeft de optie voor het melden van spellingsfouten nu een sneltoets (alt+f). (#793)
* NVDA zal nu de taal van de synthesizer/stem gebruiken voor het uitspreken van karakters en symbolen (inclusief interpunctie en symboolnamen), ongeacht automatisch van taal wisselen is ingeschakeld. Om deze optie uit te schaklen zodat NVDA de interfacetaal weer gebruikt schakelt u de nieuwe optie Vertrouw taal van stem bij het verwerken van karakters en symbolen uit in de steminstellingen. (#4210)
* Ondersteuning voor de Newfon-synthesizer is verwijderd. Newfon is nu beschikbaar als een add-on. (#3184)
* Skype voor Desktop 7 of nieuwer is nu vereist voor gebruik met NVDA; eerdere versies worden niet ondersteund. (#4218)
* Het downloaden van NVDA updates is nu veiliger. (Concreet wordt de update-informatie nu opgevraagd via https en wordt de hash van het bestand gecontroleerd nadat het bestand gedownload is.) (#4716)
* eSpeak heeft een upgrade gekregen naar versie 1.48.04 (#4325)

### Opgeloste Problemen

* In Microsoft Excel worden samengevoegde cellen met rij- en kolomkoppen nu correct afgehandeld. Als bijvoorbeeld A1 en B1 zijn samengevoegd, worden bij B2 zowel A1 en B1 gemeld als kolomkop in plaats van helemaal niets. (#4617)
* Bij het bewerken van de inhoud van een tekstvak in Microsoft PowerPoint 2003 zal NVDA nu de inhoud van iedere regel correct melden. (#4619)
* Alle dialoogvensters van NVDA worden nu op het midden van het scherm weergegeven om visuele presentatie en bruikbaarheid te verbeteren. (#3148)
* Wanneer er in Skype voor desktop bij het toevoegen van een contactpersoon een introducerend bericht wordt ingetypt, werkt het invoeren van en navigeren door de tekst nu correct. (#3661)
* Wanneer de focus verplaatst naar een nieuw item in boomstructuren in de Eclipse IDEen het eerder geselecteerde item een selectivakje is, wordt het niet langer onterecht gemeld. (#4586)
* In het venster voor spellingscontrole van Microsoft Word zal de volgende fout automatisch gemeld moeten worden wanneer de laatste fout veranderd of genegeerd is met gebruik van de daarvoor bedoelde sneltoetsen. (#1938)
* Tekst kan weer correct worden gelezen in plaatsen zoals het terminalvenster van Tera Term Pro en documenten in Balabolka. (#4229)
* Focus now correctly returns to the document being edited When finishing input composition of text in Korean and other east Asian languages while editing within a frame in Internet Explorer and other MSHTML documents. (#4045)
* Wanneer u in het dialoogvenster Invoerhandelingen koppelen tijdens het selecteren van een toetsenbordindeling voor een toetsenbordsneltoets op escape drukt, zal het menu gesloten worden in plaats van het hele venster. (#3617)
* Bij het verwijderen van een add-on wordt de map van de add-on nu correct verwijderd na het herstarten van NVDA. Voorheen moest NVDA twee keer herstart worden. (#3461)
* Er zijn belangrijke problemen opgelost bij het gebruik van Skype voor Desktop 7. (#4218)
* Bij het versturen van een bericht in Skype voor Desktop wordt het niet langer twee keer gelezen. (#3616)
* In Skype voor Desktop zou NVDA niet langer af en toe onterecht een grote berichtenstroom moeten voorlezen (mogelijk zelfs een hele conversatie). (#4644)
* er is een probleem opgelost waarbij het NVDA-commando voor het melden van de datum/tijd de regionale instellingen van de gebruiker in sommige gevallen niet respecteerde. (#2987)
* In de bladermodus wordt onzinnige tekst (die soms zelfs meerdere regels omvat) niet langer gepresenteerd voor bepaalde afbeeldingen zoals te vinden op Google Groups. Dit gebeurde specifiek met base64 gecodeerde afbeeldingen.) (#4793)
* NVDA zou niet langer na enkele seconden moeten bevriezen wanneer de focus verplaatst wordt uit een app uit de Windows Store. (#4572)
* The aria-atomic attribute on live regions in Mozilla Firefox is now honored even when the atomic element itself changes. Previously, it only affected descendant elements. (#4794)
* Browse mode will reflect updates, and live regions will be announced, for   browse mode documents within ARIA applications embedded in a document in Internet Explorer or other MSHTML controls. (#4798)
* When text is changed or added in live regions in Internet Explorer and other MSHTML controls where the author has specified that text is relevant, only the changed or added text is announced, rather than all of the text in the containing element. (#4800)
* Content indicated by the aria-labelledby attribute on elements in Internet Explorer and other MSHTML controls correctly replaces the original content  where it is appropriate to do so. (#4575)
* Bij de spellingscontrole in Microsoft Outlook 2013 wordt het verkeerd gespelde woord nu gemeld. (#4848)
* In Internet Explorer and other MSHTML controls, content inside elements hidden with visibility:hidden is no longer inappropriately presented in browse mode. (#4839, #3776)
* In Internet Explorer and other MSHTML controls, the title attribute on form controls no longer inappropriately takes preference over other label associations. (#4491)
* In Internet Explorer and other MSHTML controls, NVDA no longer ignores focusing  of elements  due to the aria-activedescendant attribute. (#4667)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Updated wxPython to 3.0.2.0. (#3763)
* Updated Python to 2.7.9. (#4715)
* NVDA no longer crashes when restarting after removing or updating an add-on which imports speechDictHandler in its installTasks module. (#4496)

## 2014.4

### Nieuwe Functies

* Nieuwe talen: Colombiaans Spaans, Punjabi.
* Het is nu mogelijk om NVDA te herstarten of NVDA te herstarten met add-ons uitgeschakeld vanuit het afsluitvenster van NVDA. (#4057)
 * NVDA kan ook worden gestart met add-ons uitgeschakeld via de --disable-addons commandoregeloptie.
* In uitspraakwoordenboeken is het nu mogelijk om in te stellen dat een patroon alleen gebruikt wordt wanneer het een heel woord betreft, d.w.z. het vervangen vindt niet plaats wanneer het woord een deel van een langer woord is. (#1704)

### Veranderingen

* Wanneer u met objectnavigatie naar een object genavigeerd bent en dit object zich wel en het vorige object zich niet in een bladermodusdocument bevindt, zal de leesoverzichtsmodus automatisch ingesteld worden op document. Dit gebeurde voorheen alleen wanneer het navigatorobject veranderde door een focusverandering. (#4369)
* De lijsten voor brailleleesregels en synthesizers in de respectievelijke instellingsvensters zijn nu alfabetisch gesorteerd, behalve geen braille/geen spraak die zich nu onderaan de lijst bevinden. (#2724)
* Liblouis braillevertaler bijgewerkt naar 2.6.0. (#4434, #3835)
* Het navigeren naar tekstvelden in bladermodus door het indrukken van e en shift+e omvat nu bewerkbare keuzelijsten. Dit omvat ook het zoekvak in de nieuwste versie van Google Zoeken. (#4436)
* Het klikken op het NVDA-pictogram in het systeemvak met de linker muisknop opent nu het NVDA-menu. (#4459)

### Opgeloste Problemen

* When moving focus back to a browse mode document (e.g. alt+tabbing to an already opened web page), the review cursor is properly positioned at the virtual caret, rather than the focused control (e.g. a nearby link). (#4369)
* In Powerpoint-presentaties volgt de leescursor nu de virtuele cursor op een correcte manier. (#4370)
* In Mozilla Firefox and other Gecko-based browsers, new content within a live region will be announced even if the new content has a usable ARIA live type different to the parent live region; e.g. when content marked as assertive is added to a live region marked as polite. (#4169)
* In Internet Explorer and other MSHTML controls, some cases where a document is contained within another document no longer prevent the user from accessing some of the content (specifically, framesets inside framesets). (#4418)
* NVDA loopt in sommige gevallen niet langer vast bij het gebruik van een Handy Tech brailleleesregel. (#3709)
* Het in een aantal gevallen weergeven van een foutmelding in Windows Vista, bijv. bij het starten van NVDA via de bureaubladsnelkoppeling of via de sneltoets, is opgelost.(#4235)
* Er zijn ernstige problemen met tekstinvoer opgelost in dialoogvensters in recente versies van Eclipse. (#3872)
* In Outlook 2010 werkt het verplaatsen van de cursor in het locatieveld van afspraken en vergaderverzoeken nu naar behoren. (#4126)
* Inside a live region, content which is marked as not being live (e.g. aria-live="off") is now correctly ignored. (#4405)
* Bij het melden van de tekst van een statusbalk met een naam wordt de naam nu correct gescheiden van het eerste woord van de statusbalktekst. (#4430)
* Bij het invoeren van wachtwoorden met het uitspreken van woorden ingeschakeld worden er niet langer nodeloos meerdere sterretjes uitgesproken bij het beginnen aan een nieuw woord. (#4402)
* In de berichtenlijst van Microsoft Outlook worden items niet langer nodeloos benoemd als data-items. (#4439)
* Bij het selecteren van tekst in het codevenster van de Eclipse IDE wordt de hele selectie niet langer iedere keer uitgesproken bij een selectieverandering. (#2314)
* Verschillende versies van Eclipse worden nu als zodanig herkend en behandeld. (#4360, #4454)
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls (including many Windows 8 applications) is now much more accurate  on high DPI displays or when document zoom is changed. (#3494)
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls will now announce the label of more buttons. (#4173)
* Bij het gebruik van een Papenmeier BRAILLEX brailleleesregel met BrxCom werken de toetsen op de leesregel nu als verwacht. (#4614)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* For executables which host many different apps (e.g. javaw.exe), code can now be provided to load specific app modules for each app instead of loading the same app module for all hosted apps. (#4360)
 * See the code documentation for appModuleHandler.AppModule for details.
 * Support for javaw.exe is implemented.

## 2014.3

### Nieuwe Functies

* De geluiden die worden gespeeld bij het starten en afsluiten van NVDA kunnen uitgeschakeld worden via een nieuwe optie in het dialoogvenster met Algemene instellingen. (#834)
* Hulp voor add-ons is bereikbaar vanuit de Add-ons Manager voor add-ons die dit ondersteunen. (#2694)
* Ondersteuning voor de Agenda in Microsoft Outlook 2007 en hoger (#2943) inclusief:
 * Aankondiging van de huidige tijd tijdens het bewegen met de pijltjestoetsen.
 * Aanduiding of de geselecteerde tijd overlapt pet een afspraak.
 * aankondiging van de geselecteerde afspraak als men op tab drukt.
 * Smart filtering van de datum zodat de datum enkel wordt aangekondigd als de nieuw geselecteerde tijd of afspraak op een andere dag is dan de vorige.
* Ondersteuning uitgebreid voor de Inbox en andere berichtenlijsten in Outlook 2010 en hoger (#3834) inclusief:
 * De mogelijkheid om kolomkoppen te onderdrukken (van, onderwerp enz.) door de optie Rij- en kolomkoppen melden uit te schakelen in Documentopmaak instellingen.
 * De mogelijkheid om tabelnavigatiecommando's te gebruiken (control + alt + pijltjestoetsen) om door individuele kolommen te bewegen.
* Microsoft word: als een inline afbeelding geen alternatieve tekst heeft, zal NVDA in plaats daarvan de titel van de afbeelding melden als de auteur deze heeft opgegeven. (#4193)
* Microsoft Word: melden van Alinea inspringing met het commando opmaak melden (NVDA+f) en automatisch als de nieuwe instelling Melden van alinea inspringing is ingeschakeld bij Documentopmaak instellingen. (#4165).
* Automatisch melden van ingevoegde tekst zoals een nieuw opsommingsteken, getal of tabsprong bij het drukken op enter in bewerkbare documenten en tekstvelden. (#4185)
* Microsoft word: NVDA+alt+c meldt de tekst van een opmerking als de cursor binnen een opmerking staat. (#3528)
* Verbeterde ondersteuning voor het automatisch lezen van kolom- en rijkoppen in Microsoft Excel (#3568) inclusief:
 * Ondersteuning voor Excel defined name ranges om kopcellen te identificeren (compatibel met de Jaws screenreader)
 * De commando's kolomkoppen instellen (NVDA+shift+c) en rijkoppen instellen (NVDA+shift+r) bewaren de instelllingen nu in het werkblad zodat ze beschikbaar zijn de volgende keer dat het blad wordt geopend, en zo zullen ze ook beschikbaar zijn voor andere schermlezers die het defined name range schema ondersteunen.
 * Deze commando's kunnen nu ook meerdere keren per blad worden gebruikt om verschillende koppen in te stellen voor verschillende gebieden.
* Ondersteuning voor het automatisch lezen van kolom- en rijkoppen in Microsoft Word (#3110) inclusief:
 * Ondersteuning van MS Word bookmarks om kopcellen te identificeren (compatibel met de Jaws screenreader)
 -  De commando's kolomkoppen instellen (NVDA+shift+c) en rijkoppen instellen (NVDA+shift+r) laten u in de eerste kopcel van een tabel toe om NVDA te laten weten dat deze koppen automatisch gemeld moeten worden. De instellingen worden in het document bewaard zodat ze beschikbaar zijn de volgende keer dat het document wordt geopend, en ze zullen beschikbaar zijn voor andere schermlezers die het bookmark schema ondersteunen.
* Microsoft Word: meld de afstand van de linkerrand van de pagina als men op de tabtoets drukt. (#1353)
* Microsoft Word: geeft feedback in spraak en braille voor de meest beschikbare opmaaksneltoetsen (vet, cursief, onderlijnen, uitlijning en kopniveau's). (#1353)
* Microsoft Excel: als de geselecteerde cel opmerkingen bevat, kunnen deze nu gemeld worden via NVDA+alt+c (#2920)
* Microsoft Excel voorziet een NVDA-specifiek dialoogvenster om de opmerkingen te bewerken bij de momenteel geselecteerde cel als u het Excel-commando shift+f2 drukt om in de modus te komen voor het bewerken van opmerkingen. (#2920)
* Microsoft Excel: feedback in spraak en braille voor veel meer sneltoetsen die de selectie verplaatsen (#4211) inclusief:
 * Verticale paginaverplaatsing (pageUp en pageDown)
 * Horizontale paginaverplaatsing (alt+pageUp en alt+pageDown)
 * Selectie uitbreiden (bovengenoemde toetsen samen met Shift).
 * Selecteren van het huidige gebied (control+shift+8)
* Microsoft Excel: meld verticale en horizontale uitlijning voor cellen met het commando opmaak melden (NVDA+f) en automatisch als de optie voor het melden van uitlijning is ingeschakeld in de Documentopmaak instellingen. (#4212)
* Microsoft Excel: de stijl van een cel kan nu worden gemeld met het commando opmaak melden (NVDA+f). Ze kan ook automatisch worden gemeld als in Documentopmaak instellingen de optie Stijl melden is ingeschakeld. (#4213)
* Microsoft Powerpoint: bij het verplaatsen van vormen binnen een dia met de pijltoetsen wordt nu de huidige locatie van de vorm gemeld (#4214) inclusief:
 * De afstand tussen de vorm en elke diarand wordt gemeld.
 * Als de vorm overlapt met een andere vorm of erdoor wordt overlapt, dan wordt de overlapte afstand en de andere vorm gemeld.
 * Om deze informatie op te vragen zonder een vorm te verplaatsen, drukt u het commando locatie melden (NVDA+delete)
 * Bij het selecteren van een vorm, if it is covered by een andere vorm, zal NVDA melden dat it is obscured.
* Het commando Locatie melden (NVDA+delete) is in sommige situaties meer inhoudsafhankelijk. (#4219):
 * In standaard invoervelden en bladermodus wordt de cursorpositie gemeld als een percentage through de content, samen met zijn schermcoördinaten.
 * Bij vormen in Powerpoint Presentaties wordt positie van de vorm gemeld relatief ten opzichte van de dia en andere vormen.
 * Dit commando tweemaal drukken, resulooteert in het oudere gedrag dat de locatie-informatie meldt voor de hele control.
* Nieuwe taal: Catalaans.

### Veranderingen

* Liblouis braillevertaler bijgewerkt naar 2.5.4. (#4103)

### Opgeloste Problemen

* In Google Chrome en Chrome-gebaseerde browsers worden bepaalde stukken tekst (bvb. als ze beklemtoond zijn) niet langer herhaald bij het melden van de tekst van een waarschuwing of dialoogvenster. (#4066)
* Als u in bladermodus in Mozilla applicaties enter drukte op een knop etc. werd die niet altijd geactiveerd (of de verkeerde control werd geactiveerd). Dit was enkel in sommige gevallen zoals de knoppen bovenaan Facebook. Dit probleem is verholpen. (#4106)
* Nutteloze informatie wordt niet langer aangekondigd bij het tabben door iTunes. (#4128)
* In bepaalde lijsten in iTunes zoals de Muzieklijst, werkt het bewegen naar het volgende item nu correct via gebruik van objectnavigatie. (#4129)
* HTML-elementen die via WAI ARIA markup worden veranderd in koppen zijn nu opgenomen in de Bladermodus Elementenlijst en snelnavigatie voor Internet Explorer documenten. (#4140)
* Als u, in bladermodus documenten, binnen pagina links volgt in recente versies van Internet Explorer verplaatst de focus nu correct naar doelpositie en dit wordt ook gemeld. (#4134)
* Microsoft Outlook 2010 en hoger: overall access to secure dialogs zoals de Nieuwe profielen en mail setup dialogs is verbeeterd. (#4090, #4091, #4095)
* Microsoft Outlook: Useless verbosity has been decreased in command toolbars when navigating through certain dialogs. (#4096, #3407)
* Microsoft Word: tabben naar een lege cel in een tabel kondigt niet langer foutief aan dat de tabel wordt verlaten. (#4151)
* Microsoft Word: het eerste teken na het einde van een tabel (inclusief een nieuwe lege regel) wordt niet langer foutief als onderdeel van de tabel beschouwd. (#4152)
* In de spellingcontrole van Microsoft Word 2010 wordt het eigenlijke foutief gespelde woord gemeld in plaats van onterecht enkel het eerste vette woord te melden. (#3431)
* In bladermodus in Internet Explorer en andere MSHTML-elementen, tabbing of gebruik van lettertoetsnavigatie om naar formuliervelden te gaan, meldt opnieuw het label in veel gevallen waar dat vroeger niet gebeurde (specifiek waar HTML label elements zijn gebruikt). (#4170)
* Microsoft Word: Reporting de aanwezigheid en placement of comments is more accurate. (#3528)
* Navigatie in bepaalde dialoogvensters in MS Office producten zoals Word, Excel en Outlook is verbeterd door niet langer bepaalde control container toolbars te melden die niet nuttig zijn voor de gebruiker. (#4198)
* Task panes zoals clipboard manager of File recovery lijken niet langer per ongeluk focus te krijgen bij het openen van een toepassing als Microsoft Word of Excel, waardoor de gebruiker soms heen en weer moest schakelen naar de toepassing om het document of werkblad te gebruiken. (#4199)
* NVDA weigert niet langer te werken op recente Windows besturingssystemen als de taal van Windows is ingesteld als Servisch (Latin). (#4203)
* Pressing numlock in invoerhulp nu correctly toggles numlock, rather than causing het toetsenbord en het besturingssysteem to become out of sync in regards to de status van deze toets. (#4226)
* In Google Chrome wordt de titel van het document opnieuw gemeld bij het wisselen van tabblad. In NVDA 2014.2 gebeurde dit in sommige gevallen niet. (#4222)
* In Google Chrome en Chrome-gebaseerde browsers wordt het webadres van het document niet langer gemeld bij het lezen van het document. (#4223)
* When running say all als de No speech synthesizer is geselecteerd (nuttig voor automated testing), say all will nu complete in plaats van te stoppen na de eerste regels. (#4225)
* Microsoft Outlook's Signature dialog: het Signature editing veld is nu toegankelijk, wat full cursor tracking en format detection mogelijk maakt. (#3833)
* Microsoft Word: bij het lezen van de laatste regel van een tabelcel, wordt niet langer de hele tabelcel gelezen. (#3421)
* Microsoft Word: bij het lezen van de eerste of de laatste regel van een inhoudsopgave, wordt niet langer de hele inhoudsopgave gelezen. (#3421)
* Bij het uitspreken van woorden en in sommige andere gevallen, worden woorden niet langer onterecht onderbroken bij markeringen zoals klinkertekens en virama in Indische talen. (#4254)
* Invoervelden voor getallen worden nu correct behandeld in GoldWave. (#670)
* Microsoft Word: als u per alinea navigeert met control+pijlOmlaag / control+pijlOmhoog is het niet langer nodig de toetscombinatie tweemaal te drukken als u door een lijst gaat. (#3290)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* NVDA now has unified support for add-on documentation. See the Add-on Documentation section of the Developer Guide for details. (#2694)
* When providing gesture bindings on a ScriptableObject via __gestures, it is now possible to provide the None keyword as the script. This unbinds the gesture in any base classes. (#4240)
* It is now possible to change the shortcut key used to start NVDA for locales where the normal shortcut causes problems. (#2209)
 * This is done via gettext.
 * Note that the text for the Create desktop shortcut option in the Install NVDA dialog, as well as the shortcut key in the User Guide, must also be updated.

## 2014.2

### Nieuwe Functies

* Aankondiging van tekstselectie is nu mogelijk in sommige custom invoervelden waar display information wordt gebruikt. (#770)
* In toegankelijke Javatoepassingen wordt informatie over de positie nu aangekondigd voor keuzerondjes en andere controls die groepsinformatie weergeven. (#3754)
* In toegankelijke Javatoepassingen worden sneltoetsen nu aangekondigd voor controls die hiervan voorzien zijn. (#3881)
* In bladermodus worden nu labels bij oriëntatiepunten gemeld. Ze zijn ook opgenomen in het dialoogvenster van de Elementenlijst. (#1195)
* In bladermodus worden gelabelde gebieden nu behandeld als oriëntatiepunten. (#3741)
* In Internet Explorer documenten en toepassingen worden Live Regions (onderdeel van de W3c ARIA standaard) nu ondersteund. Deze laten auteurs van webpagina's toe om bepaalde gebieden te markeren als veranderlijk. Als de inhoud van zo een gebied verandert, zal die automatisch worden voorgelezen. (#1846)

### Veranderingen

* Bij het afsluiten van een dialoogvenster of toepassing in een bladermodus document, wordt de naam en het type van het bladermodus document niet langer aangekondigd. (#4069)

### Opgeloste problemen

* Het standaard Windows Systeemmenu wordt niet langer onverwacht geblokkeerd in Javatoepassingen (#3882)
* Bij het kopiëren van tekst van Schermoverzichtmodus, worden lijnsprongen niet langer genegeerd. (#3900)
* Nutteloze objecten met witruimte worden niet langer gemeld in sommige toepassingen als de focus verandert of bij gebruik van objectnavigatie met eenvoudige leesoverzichtmodus ingeschakeld. (#3839)
* Berichtvakken en andere dialoogvensters van NVDA veroorzaken opnieuw dat eerdere spraak wordt geannuleerd vooraleer het dialoogvenster aan te kondigen.
* In bladermodus worden de labels van controls zoals links en knoppen nu correct weergegeven als de auteur het label heeft overschreven om de toegankelijkheid te verbeteren (meer bepaald door aria-label of aria-labelledby te gebruiken). (#1354)
* In Bladermodus in Internet Explorer wordt tekst in een element met aria-presentation niet langer genegeerd. (#4031)
* Het is nu opnieuw mogelijk Viëtnamese tekst te typen met de Unikey software. Schakel hiervoor het selectievakje Behandel toetsen van andere toepassingen uit, dat is toegevoegd aan het dialoogvenster Toetsenbordinstellingen. (#4043)
* In bladermodus worden menu items van keuzerondjes en selectievakjes gemeld als controls in plaats van gewone klikbare tekst. (#4092)
* NVDA schakelt niet langer foutief van focusmodus naar bladermodus als een menu item van een keuzerondje of selectievakje focus krijgt. (#4092)
* Als in Microsoft PowerPoint "getypte woorden uitspreken is ingeschakeld, worden karakters die worden verwijderd met backspace niet langer aangekondigd als deel van het getypte woord. (#3231)
* In de dialoogvensters met opties van Microsoft Office 2010 worden de labels van vervolgkeuzelijsten correct gemeld. (#4056)
* Als u in bladermodus in Mozillatoepassingen de snelnavigatiecommando's gebruikt om naar volgende/vorige knop of formulierveld te springen, worden nu ook aankruisknoppen meegenomen. (#4098)
* De inhoud van alerts in Mozillatoepassingen wordt niet langer tweemaal gemeld. (#3481)
* In bladermodus worden containers en oriëntatiepunten niet langer herhaald als u erbinnen navigeert terwijl de pagina-inhoud wijzigt (b.v. bij het navigeren op de websites van Facebook en Twitter). (#2199)
* NVDA herstelt zich vaker als u wegschakelt van toepassingen die niet meer reageren. (#3825)
* The caret (insertion point) opnieuw correctly updates when doing een sayAll command while in tekstvelden drawn directly to het scherm. (#4125)

## 2014.1

### Nieuwe Functies

* Ondersteuning voor Microsoft PowerPoint 2013. Merk op dat beveiligde weergave niet wordt ondersteund. (#3578)
* In Microsoft word en Excel kan NVDA nu het geselecteerde symbool lezen bij het kiezen van symbolen uit het dialoogvenster Symbolen Invoegen. (#3538)
* U kunt nu kiezen of inhoud in documenten als klikbaar moet worden aangegeven via een nieuwe optie in het dialoogvenster Documentopmaak. Deze optie is standaard ingeschakeld overeenkomstig het vroegere gedrag. (#3556)
* Ondersteuning voor brailleleesregels die via Bluetooth zijn verbonden met een computer die met de Widcomm Bluetooth Software werkt. (#2418)
* Bij het bewerken van tekst in PowerPoint worden hyperlinks nu gemeld. (#3416)
* In ARIA-toepassingen of dialoogvensters op internet kunt u nu NVDA naar bladermodus laten schakelen met NVDA+spatiebalk. Dit laat documentachtige navigatie toe in de toepassing of het dialoogvenster. (#2023)
* In Outlook Express, Windows Mail en Windows Live Mail meldt NVDA het nu als een bericht een bijlage heeft of gemarkeerd is. (#1594)
* Bij het navigeren door tabellen in toegankelijke Java toepassingen worden rij- en kolomcoördinaten nu gemeld, inclusief kolom- en rijkoppen als die er zijn. (#3756)

### Veranderingen

* Voor Papenmeier brailleleesregels is het commando move to flat review/focus verwijderd. Gebruikers kunnen de gewenste toetsen toekennen via het dialoogvenster Invoerhandelingen koppelen. (#3652)
* NVDA vereist nu Microsoft VC runtime versie 11, wat inhoudt dat het niet langer kan werken op besturingssystemen ouder dan Windows XP Service Pack 2 of Windows Server 2003 Service Pack 1.
* Als het interpunctieniveau is ingesteld op Sommige, zullen nu de asterisk (*) en het plusteken (+) worden uitgesproken. (#3614)
* ESpeak bijgewerkt naar versie 1.48.04 die veel taalverbeteringen bevat en die een aantal vastlopers oplost. (#3842, #3739, #3860)

### Opgeloste problemen

* Bij het navigeren tussen of het selecteren van cellen in Microsoft Excel zou NVDA niet langer foutief de oude cel mogen aankondigen in plaats van de nieuwe cel als Microsoft Excel traag is bij het verplaatsen van de selectie. (#3558)
* NVDA werkt nu correct als u via het contextmenu een keuzelijst opent binnen een cel in Microsoft Excel. (#3586)
* In winkelpagina's van iTunes 11 wordt nieuwe pagina-inhoud nu juist getoond in bladermodus als u een link volgt in de winkel of bij het initieel openen van de winkel. (#3625)
* Knoppen om een preview van nummers te krijgen in de iTunes 11 winkel tonen nu hun label in bladermodus. (#3638)
* In bladermodus in Google Chrome worden de labels van selectievakjes en keuzerondjes nu correct weergegeven. (#1562)
* In Instantbird meldt NVDA niet langer nutteloze informatie elke keer u naar een contact gaat in de Contactenlijst. (#2667)
* In bladermodus in Adobe Reader wordt de juiste tekst nu weergegeven voor knoppen, etc. waar het label werd overschreven via een tooltip of op andere manieren. (#3640)
* In bladermodus in Adobe Reader zullen overbodige afbeeldingen die de tekst "mc-ref" bevatten niet langer worden weergegeven. (#3645)
* NVDA meldt niet langer alle cellen in Microsoft Excel als onderlijnd bij hun opmaakinformatie. (#3669)
* Toont niet langer betekenisloze karakters in bladermodus documenten zoals die in de Unicode-reeks voor privé-gebruik. In sommige gevallen verhinderden deze dat zinvoller labels werden getoond. (#2963)
* Invoersamenstelling voor het invoeren van Oost-Aziatische karakters weigert niet langer in PuTTY. (#3432)
* Navigeren door een document na afgebroken automatisch lezen leidt er niet langer toe dat NVDA soms foutief aankondigde dat u een veld verliet (zoals een tabel) lager in het document dat het automatisch lezen eigenlijk nooit had uitgesproken. (#3688)
* Bij gebruik van bladermodus snelnavigatiecommando's tijdens automatisch lezen met doorbladeren ingeschakeld, kondigt NVDA accurater het nieuwe veld aan; b.v. zegt nu dat een kop een kop is, in plaats van enkel zijn tekst. (#3689)
* De snelnavigatiecommando's om te springen naar het einde of begin van een container werken nu met doorbladeren tijdens automatisch lezen; d.w.z. dat ze niet langer het huidige automatisch lezen zullen afbreken. (#3675)
* Benamingen van invoerhandelingen die voorkomen in het dialoogvenster Invoerhandelingen koppelen zijn nu duidelijker en vertaald. (#3624)
* NVDA veroorzaakt niet langer het vastlopen van bepaalde programma's bij het bewegen van de muis over hun rich edit (TRichEdit) controls. Het gaat o.a. om de programma's Jarte 5.1 en BRfácil. (#3693, #3603, #3581)
* In Internet Explorer en andere MSHTML-elementen worden containers zoals tabellen die zijn gemarkeerd met de ARIA presentation role niet langer gemeld aan de gebruiker. (#3713)
* in Microsoft Word herhaalt NVDA op de brailleleesregel niet langer meermaals de informatie over rijen en kolommen voor een tabelcel. (#3702)
* In talen zoals Frans en Duits die een spatie gebruiken om duizendtallen te scheiden, worden de cijfers van aparte groepjes niet langer uitgesproken als een enkel getal. Dit was vooral problematisch voor tabelcellen die getallen bevatten. (#3698)
* Braille weigert niet langer soms te vernieuwen als de systeemcursor beweegt in Microsoft Word 2013. (#3784)
* Als u gepositioneerd bent op het eerste karakter van een kop in Microsoft Word, verdwijnt de tekst die de kop en zijn niveau aankondigt niet langer van de brailleleesregel. (#3701)
* Als een programma wordt afgesloten waarvoor een configuratieprofiel actief is, weigert NVDA niet langer soms het profiel uit te schakelen. (#3732)
* Bij Aziatische invoer in een control binnen NVDA zelf (b.v. het bladermodus dialoogvenster om te zoeken), wordt niet langer foutief "NVDA" gemeld in plaats van de kandidaat. (#3726)
* De tabbladen in het opties-dialoogvenster van Outlook 2013 worden nu gemeld. (#3826)
* Verbeterde ondersteuning voor ARIA live regions in Firefox en andere Mozilla Geckotoepassingen:
 * Ondersteuning voor aria-atomic updates en filtering van aria-busy updates (#2640)
 * Alternatieve tekst (zoals alt-attribuut of aria-label) wordt gebruikt als er geen andere nuttige tekst is. (#3329)
 * Live region updates worden niet langer onderdrukt als ze gebeuren terwijl de focus beweegt. (#3777)
* Bepaalde presentatie-elementen worden niet langer foutief getoond in Firefox en andere Mozilla Geckotoepassingen in bladermodus (meer bepaald als het element is gemarkeerd met aria-presentation maar ook focus kan krijgen). (#3781)
* Een performantieverbetering bij het navigeren door een document in Microsoft Word als melden van spelfouten is ingeschakeld. (#3785)
* Verschillende verbeteringen aan de ondersteuning voor toegankelijke Java toepassingen:
 * De control die initieel focus had in een frame of dialoogvenster weigert niet langer gemeld te worden als het frame of dialoogvenster op de voorgrond komt. (#3753)
 * Overbodige positie-informatie wordt niet langer aangekondigd voor keuzerondjes (b.v. 1 van 1). (#3754)
 * Beter melden van JComboBox controls (html niet langer gemeld, beter melden van de statussen uitgevouwen en samengevouwen). (#3755)
 * Bij het melden van de tekst van dialoogvensters ontbrak soms tekst. Die is nu inbegrepen. (#3757)
 * Veranderingen aan de naam, waarde of beschrijving van de control die focus heeft worden nu accurater gemeld. (#3770)
* Een vastloper opgelost in NVDA in Windows 8 als de focus gaat naar bepaalde RichEdit controls die grote hoeveelheden tekst bevatten (b.v. NVDA's log viewer, windbg). (#3867)
* Op systemen met een hoge DPI display setting (wat standaard het geval is bij veel moderne schermen), stuurt NVDA de muis niet langer naar de verkeerde plaats in sommige toepassingen. (#3758, #3703)
* Een probleem opgelost dat zich soms voordeed bij het surfen waarbij NVDA niet langer correct werkte totdat het werd herstart, zelfs als het niet was vastgelopen. (#3804)
* Een Papenmeier brailleleesregel kan nu gebruikt worden zelfs als er nooit een Papenmeier leesregel aangesloten was via USB. (#3712)
* NVDA loopt niet langer vast als een ouder model Papenmeier BRAILLEX brailleleesregel wordt geselecteerd zonder dat er een leesregel is aangesloten.

### Veranderingen voor Ontwikkelaars (niet vertaald)

* AppModules now contain productName and productVersion properties. This info is also now included in Developer Info (NVDA+f1). (#1625)
* In the Python Console, you can now press the tab key to complete the current identifier. (#433)
 * If there are multiple possibilities, you can press tab a second time to choose from a list.

## 2013.3

### Nieuwe Functies

* Formuliervelden worden nu gemeld in Microsoft word documenten. (#2295)
* NVDA kan nu aangebrachte wijzigingen in de tekst aankondigen in Microsoft Word als Wijzigingen Bijhouden is ingeschakeld. Merk op dat u hiervoor in NVDA ook het selectievakje "Aangebrachte wijzigingen in de tekst melden" moet inschakelen in het dialoogvenster documentinstellingen (standaard is het uitgeschakeld). (#1670)
* In Microsoft Excel 2003 tot 2010 worden keuzelijsten nu aangekondigd bij het openen en navigeren. (#3382)
* een nieuwe optie 'Doorbladeren tijdens automatisch lezen toestaan' in het dialoogvenster Toetsenbordinstellingen laat toe door een document te navigeren met de navigatietoetsen van bladermodus en de commando's om naar paragrafen of regels te gaan, terwijl u automatisch blijft lezen. Deze optie is standaard uitgeschakeld. (#2766)
* Er is nu een dialoogvenster Invoerhandelingen koppelen, dat u eenvoudiger toelaat om snelkoppelingen (zoals toetsen op het toetsenbord) toe te kennen aan NVDA-commando's. (#1532)
* U kan nu verschillende instellingen hebben voor verschillende situaties door configuratieprofielen te gebruiken. Profielen kunnen manueel of automatisch geactiveerd worden (v.b. voor een bepaalde toepassing). (#87, #667, #1913)
* In Microsoft Excel worden cellen die links zijn nu als links aangekondigd. (#3042)
* In Microsoft Excel wordt het nu gemeld als een cel opmerkingen bevat. (#2921)

### Opgeloste problemen

* Zend Studio werkt nu hetzelfde als Eclipse. (#3420)
* Als de status verandert van bepaalde selectievakjes in het dialoogvenster Berichtregels van Microsoft Outlook 2010 wordt dat nu automatisch gemeld. (#3063)
* NVDA meldt nu de status "vastgemaakt" voor vastgemaakte items zoals tabs in Mozilla Firefox. (#3372)
* Het is nu mogelijk scripts te koppelen aan toetsenbordsneltoetsen in combinatie met de Alt- en/of de Windowstoetsen. Als dit voorheen gebeurde, werd bij het oproepen van het script ofwel het Startmenu ofwel de menubalk geactiveerd. (#3472)
* Het selecteren van tekst in bladermodusdocumenten (v.b. met control+shift+end) veroorzaakt geen verandering meer van de toetsenbordindeling op systemen waarop meerdere toetsenbordindelingen zijn geïnstalleerd. (#3472)
* Internet Explorer zou niet langer mogen vastlopen of onbruikbaar worden bij het afsluiten van NVDA. (#3397)
* Fysieke beweging en andere activiteiten op sommige nieuwere computers worden niet langer behandeld als ongeldige toetsaanslagen. Voorheen konden deze ertoe leiden dat de spraak stopte en soms activeerden ze NVDA-commando's. (#3468)
* NVDA gedraagt zich nu zoals verwacht in Poedit 1.5.7. Gebruikers van oudere versies zullen moeten updaten. (#3485)
* NVDA kan nu beveiligde documenten lezen in Microsoft Word 2010 en zal Word niet langer doen vastlopen. (#1686)
* Een onbekende commandline swiwtch bij het starten van het installatiebestand voor NVDA veroorzaakt niet langer een eindeloze loop van dialoogvensters met foutboodschappen. (#3463)
* NVDA weigert niet langer de alt-tekst te melden van afbeeldingen en objecten in Microsoft Word als de alt-tekst aanhalingstekens bevat of andere karakters die niet standaard zijn. (#3579)
* Het juiste aantal items wordt nu gemeld in bepaalde horizontale lijsten in Bladermodus. Voorheen werd soms het dubbele gemeld van het werkelijke aantal. (#2151)
* Als u control+a drukt in een Microsoft Excel werkblad wordt nu de bijgewerkte selectie gemeld. (#3043)
* NVDA kan nu XHTML-documenten correct lezen in Microsoft Internet Explorer en andere MSHTML-elementen. (#3542)
* Bij het afsluiten van het dialoogvenster Toetsenbordinstellingen krijgt de gebruiker nu een foutmelding als hij geen toets heeft gekozen als NVDA-toets. Voor een correcte werking van NVDA moet er minstens één toets gekozen worden. (#2871)
* In Microsoft Excel kondigt NVDA samengevoegde cellen nu anders aan dan meerdere geselecteerde cellen. (#3567)
* De bladermoduscursor wordt niet langer foutief gepositioneerd bij het verlaten van een dialoogvenster of toepassing binnen het document. (#3145)
* Een probleem opgelost waarbij op sommige systemen de driver voor de HumanWare Brailliant BI/B serie brailleleesregel niet als optie verscheen in het Braille-instellingen dialoogvenster, zelfs als de leesregel was verbonden via USB.
* NVDA no longer fails  to switch to screen review when the navigator object has no actual screen location. In this case the review cursor is now placed at the top of the screen. (#3454)
* Fixed an issue which caused the Freedom Scientific braille display driver to fail when the port was set to USB in some circumstances. (#3509, #3662)
* Fixed an issue where keys on Freedom Scientific braille displays weren't detected in some circumstances. (#3401, #3662)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* You can specify the category to be displayed to the user for scripts using the scriptCategory attribute on ScriptableObject classes and the category attribute on script methods. See the documentation for baseObject.ScriptableObject for more details. (#1532)
* config.save is deprecated and may be removed in a future release. Use config.conf.save instead. (#667)
* config.validateConfig is deprecated and may be removed in a future release. Add-ons which need this should provide their own implementation. (#667, #3632)

## 2013.2

### Nieuwe Functies

* Ondersteuning voor het Chromium Embedded Framework, een webbrowser control die gebruikt wordt in meerdere toepassingen. (#3108)
* Nieuwe eSpeak stemvariant: Iven3.
* In Skype worden nieuwe chatberichten automatisch gemeld als de conversatie focus krijgt. (#2298)
* Ondersteuning voor Tween, inbegrepen het melden van tabnamen en minder breedsprakigheid bij het lezen van tweets.
* U kan nu het tonen van NVDA-berichten uitschakelen op een brailleleesregel door de Time-out voor berichten op 0 te zetten in het dialoogvenster Braille Instellingen. (#2482)
* Bij het beheren van Add-ons is er nu een knop "Download Add-ons" om de NVDA Add-ons-website te openen waar u beschikbare add-ons kan bekijken en downloaden. (#3209)
* In het NVDA Welkom dialoogvenster dat altijd verschijnt bij de eerste keer dat u NVDA gebruikt, kunt u nu aangeven of NVDA automatisch moet starten nadat u inlogt bij Windows. (#2234)
* Slaapmodus is automatisch ingeschakeld als u Dolphin Cicero gebruikt. (#2055)
* De Windows x64 versie van Miranda IM/Miranda NG wordt nu ondersteund. (#3296)
* Zoeksuggesties in het Windows 8.1 Startscherm worden automatisch gemeld. (#3322)
* Ondersteuning voor het navigeren in en bewerken van rekenbladen in Microsoft Excel 2013. (#3360)
* De Freedom Scientific Focus 14 Blue en Focus 80 Blue brailleleesregels, evenals de Focus 40 Blue in bepaalde configuraties die eerder waren ondersteund, zijn nu ondersteund als ze aangesloten zijn via Bluetooth. (#3307)
* Autocomplete suggesties worden nu gemeld in Outlook 2010. (#2816)
* Nieuwe brailletabellen: Engels (U.K.) computerbraille, Koreaans graad 2, Russisch braille voor computercode.
* Nieuwe taal: Farsi. (#1427)

### Veranderingen

* Als u in de objectmodus op een aanraakscherm met één vinger naar links of rechts veegt, beweegt u nu naar het vorige of volgende object, niet enkel deze in de huidige container. Veegt u met twee vingers naar links of rechts dan voert u de originele actie uit of beweegt u naar het vorige of volgende object binnen de huidige container.
* het selectievakje "Lay-outtabellen melden" in het dialoogvenster "bladermodus instellingen" is hernoemd naar "Lay-outtabellen opnemen" om aan te geven dat snelnavigatie ze ook niet zal localiseren als het selectievakje is uitgeschakeld. (#3140)
* Platte overzichtsmodus is vervangen door object-, document en schermoverzichtmodi. (#2996)
 * Objectoverzichtmodus bekijkt tekst enkel in het navigatorobject, documentoverzicht bekijkt alle tekst in een bladermodusdocument (indien beschikbaar) en schermoverzicht bekijkt tekst op het scherm voor de huidige applicatie.
 * De commando's die vroeger overgingen naar/van platte overzichtsmodus schakelen nu tussen deze nieuwe overzichtsmodi.
 * Het navigatorobject volgt automatisch de leescursor zodat het het laagste object blijft op de positie van de leescursor als u in document- of schermoverzichtmodus bent.
 * Na het schakelen naar schermoverzichtmodus, zal NVDA in deze modus blijven totdat u expliciet terugschakelt naar document- of objectoverzichtmodus.
 * Als u in document- of objectoverzichtmodus bent, kan NVDA automatisch schakelen tussen deze twee modi afhankelijk of u al dan niet in een bladermodusdocument navigeert.
* Liblouis braillevertaler bijgewerkt naar 2.5.3. (#3371)

### Opgeloste Problemen

* Het activeren van een object kondigt nu de actie voor de activatie aan, in plaats van de actie na de activatie (b.v. uitvouwen bij het uitvouwen in plaats van invouwen). (#2982)
* Meer accuraat lezen en volgen van de cursor in verschillende invoervelden voor recente versies van Skype, zoals chat- en zoekvelden. (#1601, #3036)
* In de lijst met recente conversaties in Skype, wordt nu het aantal nieuwe gebeurtenissen gelezen voor elke conversatie, indien van toepassing. (#1446)
* Verbeteringen aan cursor tracking en leesvolgorde voor rechts-naar-links tekst die naar het scherm wordt geschreven; b.v. bewerken van Arabische tekst in Microsoft Excel. (#1601)
* Snelnavigatie naar knoppen en formuliervelden zal nu links aangeven die gemarkeerd zijn als knoppen voor toegankelijkheidsredenen in Internet Explorer. (#2750)
* In bladermodus wordt de inhoud binnen boomstructuren niet langer weergegeven omdat een platte weergave niet bruikbaar is. U kan Enter drukken op een boomstructuur om ermee te interageren in focusmodus. (#3023)
* Het drukken van alt+pijlOmlaag of alt+PijlOmhoog, om een vervolgkeuzelijst uit te klappen in focusmodus, schakelt niet langer foutief over naar bladermodus. (#2340)
* In Internet Explorer 10 activeren tabelcellen niet langer focusmodus, tenzij de auteur van de webpagina ze expliciet focuseerbaar heeft gemaakt (#3248)
* NVDA weigert niet langer te starten als de systeemtijd eerder is dan de laaste controle op updates. (#3260)
* Als een voortgangsbalk wordt getoond op een brailleleesregel, wordt de brailleleesregel bijgewerkt als de voortgangsbalk verandert. (#3258)
* In bladermodus in Mozillatoepassingen, worden tabelbijschriften niet langer tweemaal weergegeven. Bovendien wordt de samenvatting weergegeven als er ook een bijschrift is. (#3196)
* Als u de invoertaal verandert in Windows 8, spreekt NVDA nu de juiste taal in plaats van de vorige.
* NVDA kondigt nu IME conversie mode veranderingen aan in Windows 8.
* NVDA kondigt niet langer rommel aan op het bureaublad als de Google Japanese of Atok IME invoermethodes gebruikt worden. (#3234)
* In Windows 7 en hoger, kondigt NVDA niet langer foutief spraakherkenning of aanraakinvoer aan als een toetsenbordtaalverandering.
* NVDA kondigt niet langer een specifiek speciaal karakter (0x7f) aan als u control+backspace drukt in sommige editors als "getypte karakters uitspreken" is ingeschakeld. (#3315)
* espeak verandert niet langer foutief van toonhoogte, volume, etc. als NVDA tekst leest die bepaalde XML controlekarakters bevat. (#3334) (regressie van #437)
* In Javatoepassingen worden veranderingen aan het label of waarde van de control die de focus heeft nu automatisch aangekondigd, en weergegeven bij herhaaldelijk bevragen van de control. (#3119)
* In Scintilla controls worden regels nu correct gemeld als automatische terugloop is ingeschakeld. (#885)
* In Mozillatoepassingen wordt de naam van alleen-lezen lijstitems nu correct gemeld; b.v. bij het navigeren door tweets in focusmodus op twitter.com. (#3327)
* De inhoud van bevestigingsdialoogvensters in Microsoft Office 2013 wordt nu automatisch gelezen als ze verschijnen.
* Performantieverbeteringen bij het navigeren in bepaalde tabellen in Microsoft Word (#3326)
* NVDA's tabelnavigatiecommando's (control+alt+pijltjes) werken beter in bepaalde Microsoft Word tabellen waar een cel meerdere rijen overspant.
* Als de Add-ons Manager geopend is en u activeert hem nogmaals (ofwel vanuit het menu Extra of door een add-on-bestand te openen) weigert hij niet langer dienst. Het is nu mogelijk de Add-ons Manager te sluiten. (#3351)
* NVDA loopt niet langer vast in bepaalde dialoogvensters als Japanse of Chinese Office 2010 IME in gebruik is. (#3064)
* Meerdere spaties worden niet langer samengetrokken tot één spatie op brailleleesregels. (#1366)
* Zend Eclipse PHP Developer Tools werkt nu hetzelfde als Eclipse. (#3353)
* In Internet Explorer is het opnieuw niet nodig tab te drukken om te interageren met een ingebed object (zoals Flash content) nadat u er enter op heeft gedrukt. (#3364)
* Bij het bewerken van tekst in Microsoft PowerPoint wordt de laatste regel niet langer gemeld als de vorige regel, als de laatste regel leeg is. (#3403)
* In Microsoft PowerPoint worden objecten niet langer soms tweemaal uitgesproken als u ze selecteert of ervoor kiest om ze te bewerken. (#3394)
* NVDA veroorzaakt niet langer het vastlopen van Adobe Reader bij bepaalde slecht opgemaakte PDF-documenten die rijen bevatten die geen deel uitmaken van een tabel. (#3399)
* NVDA detecteert nu correct welke de volgende dia is die focus heeft na het verwijderen van een dia in de miniaturen-weergave van Microsoft PowerPoint. (#3415)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* windowUtils.findDescendantWindow has been added to search for a descendant window (HWND) matching the specified visibility, control ID and/or class name.
* The remote Python console no longer times out after 10 seconds while waiting for input. (#3126)
* Inclusion of the bisect module in binary builds is deprecated and may be removed in a future release. (#3368)
 * Add-ons which depend on bisect (including the urllib2 module) should be updated to include this module.

## 2013.1.1

Deze versie lost het probleem op waarbij NVDA vastliep als Iers als taal werd ingesteld. De vertalingen zijn bijgewerkt en enkele andere problemen zijn opgelost.

### Opgeloste Problemen

* De juiste karakters worden geproduceerd bij het typen in NVDA's eigen gebruikersinterface als u een Koreaanse of Japanse invoermethode als standaardmethode gebruikt. (#2909)
* In Internet Explorer en andere MSHTML-elementen worden velden met een ongeldige invoer nu correct behandeld. (#3256)
* NVDA loopt niet langer vast bij het starten als Iers is ingesteld als taal.

## 2013.1

Hoogtepunten in deze versie zijn een meer intuïtieve en consistente laptop toetsenbordindeling; basisondersteuning voor Microsoft PowerPoint; ondersteuning voor lange beschrijvingen in webbrowsers; en ondersteuning voor invoer van computerbraille voor brailleleesregels met een brailletoetsenbord.

### Belangrijk

#### Nieuwe Laptop Toetsenbordindeling

De laptop toetsenbordindeling is helemaal herzien om ze intuîtiever en consistenter te maken.
De nieuwe indeling gebruikt de pijltjestoetsen in combinatie met de NVDA-toets en andere modifiers voor leescommando's.

Let op de volgende veranderingen aan veelgebruikte commando's:

| Naam |Toets|
|---|---|
|Alles voorlezen |NVDA+a|
|Deze regel lezen |NVDA+l|
|Geselecteerde tekst lezen |NVDA+shift+s|
|Statusbalk voorlezen |NVDA+shift+end|

Bovendien zijn, samen met andere veranderingen, alle commando's veranderd voor objectnavigatie, tekstreview, muisklik en synth-instellingenring.
Bekijk het [Overzicht van Commando's](keyCommands.html) voor de nieuwe toetsen.

### Nieuwe Functies

* Basisondersteuning voor bewerken en lezen van Microsoft PowerPoint presentaties. (#501)
* Basisondersteuning voor lezen en schrijven van berichten in Lotus Notes 8.5. (#543)
* Ondersteuning voor automatische taalverandering bij het lezen van documenten in Microsoft Word. (#2047)
* In bladermodus voor MSHTML (b.v. Internet Explorer) en Gecko (b.v. Firefox) wordt de aanwezigheid van lange beschrijvingen nu aangekondigd. Het is ook mogelijk de lange beschrijving te openen in een nieuw venster door op NVDA+d te drukken. (#809)
* Meldingen in Internet Explorer 9 en hoger worden nu uitgesproken (zoals geblokkeerde inhoud of bestandsdownloads). (#2343)
* Automatisch melden van rij- en kolomkoppen van een tabel wordt nu ondersteund voor bladermodusdocumenten in Internet Explorer en andere MSHTML-elementen. (#778)
* Nieuwe talen: Aragonees, Iers
* Nieuwe brailletabellen: Deens graad 2, Koreaans graad 1. (#2737)
* Ondersteuning voor brailleleesregels verbonden via bluetooth op een computer met de Toshiba Bluetooth Stack voor Windows. (#2419)
* Ondersteuning voor poortselectie bij gebruik van Freedom Scientific leesregels (Automatisch, USB of Bluetooth).
* Ondersteuning voor de BrailleNote familie van notitietoestellen van HumanWare, gebruikt als een brailleleesregel voor een screenreader. (#2012)
* Ondersteuning voor oudere modellen van Papenmeier BRAILLEX brailleleesregels. (#2679)
* Ondersteuning voor invoer van computerbraille voor brailleleesregels met een brailletoetsenbord. (#808)
* Nieuwe toetsenbordinstellingen die de keuze geven of NVDA de spraak moet onderbreken voor getypte karakters en/of de Entertoets. (#698)
* Ondersteuning voor verschillende browsers gebaseerd op Google Chrome: Rockmelt, BlackHawk, Comodo Dragon en SRWare Iron. (#2236, #2813, #2814, #2815)

### Veranderingen

* Liblouis braillevertaler bijgewerkt naar 2.5.2. (#2737)
* De laptop toetsenbordindeling is helemaal herzien om ze intuïtiever en consistenter te maken. (#804)
* ESpeak speech synthesizer bijgewerkt naar 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Opgeloste Problemen

* De snelnavigatietoetsen om te springen naar de volgende of vorige scheiding in bladermodus werken nu in Internet Explorer en andere MSHTML-elementen. (#2781)
* Als NVDA terugvalt naar eSpeak of als er geen spraak is omdat de gekozen spraaksynthesizer dienst weigert bij het starten van NVDA, dan wordt niet meer automatisch de fallback synthesizer teruggezet. Dit betekent dat nu, de originele synthesizer opnieuw geprobeerd wordt volgende keer dat NVDA start. (#2589)
* Als NVDA terugvalt op geen braille omdat de gekozen brailleleesregel dienst weigerde bij het starten van NVDA, dan wordt de brailleleesregel niet meer automatisch terug ingesteld op geen braille. Dit betekent dat nu, de originele leesregel opnieuw wordt geprobeerd bij de volgende keer dat NVDA start. (#2264)
* In bladermodus in Mozillatoepassingen worden updates aan tabellen nu correct weergegeven. Bijvoorbeeld, in bijgewerkte cellen worden rij- en kolomcoördinaten gemeld en tabelnavigatie werkt zoals het moet. (#2784)
* In bladermodus in web browsers werden bepaalde klikbare niet-gelabelde afbeeldingen vroeger niet weergegeven. Nu werkt dit correct. (#2838)
* Eerdere en latere versies van SecureCRT worden nu ondersteund. (#2800)
* Voor invoermethodes zoals Easy Dots IME onder XP worde de leesreeks nu correct gemeld.
* De kandidatenlijst in de Chinese Simplified Microsoft Pinyin invoermethode onder Windows 7 wordt nu correct gelezen bij het veranderen van pagina met pijl links en rechts, en bij de eerste keer dat het met Home wordt geopend.
* Als gepersonaliseerde uitspraakinformatie voor symbolen wordt opgeslagen, wordt het geavanceerde "preserve" veld niet langer verwijderd. (#2852)
* Als u "automatisch controleren op updates" uitschakelt, moet NVDA niet langer herstarten om de wijziging door te voeren.
* NVDA weigert niet langer te starten als een add-on niet kan worden verwijderd omdat zijn map momenteel in gebruik is door een andere applicatie. (#2860)
* Tablabels in het dialoogvenster met DropBox-instellingen kunnen nu gezien worden met platte overzichtzsmodus.
* Als de invoertaal wordt veranderd naar iets anders dan de standaard, detecteert NVDA nu correct de toetsen voor commando's en invoerhelpmodus.
* Voor talen zoals Duits waar het + (plus)teken een enkele toets op het toetsenbord is, is het nu mogelijk er commando's aan te binden door het woord "plus" te gebruiken. (#2898)
* In Internet Explorer en andere MSHTML-elementen worden citaten nu gemeld indien van toepassing. (#2888)
* De HumanWare Brailliant BI/B series brailleleesregel driver kan nu worden geselecteerd als de leesregel verbonden is via Bluetooth maar nooit verbonden was via USB.
* Het filteren van elementen in de Elementenlijst van de bladermodus met hoofdlettertekstfilter geeft nu niet-hoofdlettergevoelige resultaten net zoals kleine letters in plaats van helemaal niets. (#2951)
* In Mozilla browsers kan bladermodus opnieuw worden gebruikt als Flash content focus krijgt. (#2546)
* Bij gebruik van een kortschrift brailletabel en als "Naar computerbraille uitbreiden voor het woord onder de cursor" is ingeschakeld, wordt de braillecursor nu correct gepositioneerd na een woord waarin een karakter is voorgesteld door meerdere braillecellen (b.v. hoofdletterteken, letterteken, cijferteken, etc.). (#2947)
* Tekstselectie wordt nu correct getoond op een brailleleesregel in toepassingen zoals Microsoft Word 2003 en Internet Explorer invoercontrols.
* Het is opnieuw mogelijk tekst achterwaarts te selecteren in Microsoft Word terwijl Braille is ingeschakeld.
* Bij het lezen en verwijderen van karakters In Scintilla invoercontrols, kondigt NVDA correct multibyte karakters aan. (#2855)
* NVDA weigert niet langer te installeren als het pad naar het gebruikersprofiel bepaalde multibyte karakters bevat. (#2729)
* Het melden van groepen voor Lijstbeeldcontrols (SysListview32) in 64-bit toepassingen veroorzaakt niet langer een fout.
* In bladermodus in Mozillatoepassingen wordt tekstcontent niet langer foutief behandeld als bewerkbaar in sommige zeldzame gevallen. (#2959)
* Als u in IBM Lotus Symphony en OpenOffice de systeemcursor beweegt, beweegt nu de leescursor indien van toepassing.
* Adobe Flash content is nu toegankelijk in Internet Explorer in Windows 8. (#2454)
* Bluetooth ondersteuning gecorrigeerd voor Papenmeier Braillex Trio. (#2995)
* Onmogelijkheid opgelost om bepaalde Microsoft Speech API versie 5 stemmen te gebruiken zoals Koba Speech 2 stemmen. (#2629)
* In toepassingen die de Java Access Bridge gebruiken, worden brailleleesregels nu correct bijgewerkt als de systeemcursor beweegt in bewerkbare tekstvelden. (#3107)
* Ondersteunt het formulier oriëntatiepunt in bladermodusdocumenten die oriëntatiepunten ondersteunen. (#2997)
* De eSpeak synthesizer driver behandelt het lezen per karakter nu correcter (b.v. aankondigen van de naam of de waarde van een vreemde letter in plaats van enkel zijn geluid of generieke naam). (#3106)
* NVDA weigert niet langer gebruikersinstellingen te kopiëren voor gebruik op inlog- en andere beveiligde schermen als het pad naar het gebruikersprofiel non-ASCII karakters bevat. (#3092)
* NVDA loopt niet langer vast bij gebruik van Aziatische karakterinvoer in sommige .NET-toepassingen. (#3005)
* het is nu mogelijk bladermodus te gebruiken voor pagina's in Internet Explorer 10 als u in standaardmodus bent; b.v. [www.gmail.com](http://www.gmail.com) login-pagina. (#3151)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Braille display drivers can now support manual port selection. (#426)
 * This is most useful for braille displays which support connection via a legacy serial port.
 * This is done using the getPossiblePorts class method on the BrailleDisplayDriver class.
* Braille input from braille keyboards is now supported. (#808)
 * Braille input is encompassed by the brailleInput.BrailleInputGesture class or a subclass thereof.
 * Subclasses of braille.BrailleDisplayGesture (as implemented in braille display drivers) can also inherit from brailleInput.BrailleInputGesture. This allows display commands and braille input to be handled by the same gesture class.
* You can now use comHelper.getActiveObject to get an active COM object from a normal process when NVDA is running with the UIAccess privilege. (#2483)

## 2012.3

Hoogtepunten in deze versie zijn ondersteuning voor Aziatische karakterinvoer; experimentele ondersteuning voor aanraakschermen op Windows 8; melden van paginanummers en verbeterde ondersteuning voor tabellen in Adobe Reader; tabelnavigatiecommando's in tabelrijen en Windows lijstbeeldcontrols die focus krijgen; ondersteuning voor verschillende brailleleesregels; en het melden van rij- en kolomkoppen in Microsoft Excel.

### Nieuwe Functies

* NVDA ondersteunt nu Aziatische karakterinvoer bij gebruik van IME en text service invoermethodes in alle toepassingen, Inbegrepen:
 * Melden van en navigatie in kandidatenlijsten;
 * Melden van en navigatie in samenstellingsreeksen; en
 * Melden van leesreeksen.
* De aanwezigheid van onderlijning en doorstrepen wordt nu gemeld in Adobe Reader documenten. (#2410)
* Als de Windowsfunctie Plaktoetsen is ingeschakeld, zal de NVDA modifier toets zich nu gedragen als andere modifier toetsen. Dit laat u toe de NVDA modifier toets te gebruiken zonder dat u deze ingedrukt moet houden terwijl u andere toetsen indrukt. (#230)
* Automatisch melden van kolom- en rijkoppen wordt nu ondersteund in Microsoft Excel. Druk NVDA+shift+c om de rij in te stellen die kolomkoppen bevat en NVDA+shift+r om de kolom in te stellen die rijkoppen bevat. Druk een van beide commando's tweemeel snel na elkaar om de instelling ongedaan te maken. (#1519)
* Ondersteuning voor HIMS Braille Sense, Braille EDGE en SyncBraille brailleleesregels. (#1266, #1267)
* Als Windows 8 Pop-upmeldingen verschijnen, zal NVDA deze melden als "helpballonnen weergeven" is ingeschakeld. (#2143)
* Experimentele ondersteuning voor aanraakschermen in Windows 8, inclusief:
 * Lezen van tekst direct onder uw vinger terwijl u hem beweegt
 * Veel gebaren voor objectnavigatie, text review, en andere NVDA commando's.
* Ondersteuning voor VIP Mud. (#1728)
* Als in Adobe Reader een tabel een samenvatting heeft, wordt die nu weergegeven. (#2465)
* In Adobe Reader kunnen rij- en kolomkoppen van een tabel nu worden gemeld. (#2193, #2527, #2528)
* Nieuwe talen: Amharisch, Koreaans, Nepalees, Sloveens.
* NVDA kan nu autocomplete suggesties lezen bij het ingeven van emailadressen in Microsoft Outlook 2007. (#689)
* Nieuwe eSpeak stemvarianten: Gene, Gene2. (#2512)
* In Adobe Reader kunnen nu paginanummers worden weeergegeven. (#2534)
 * In Reader XI worden paginalabels gemeld waar aanwezig. Deze kunnen wijzen op veranderingen van paginanummering in verschillende secties, etc. In eerdere versies is dit niet mogelijk en worden enkel sequentiële paginanummers gemeld.
* Het is nu mogelijk om NVDA's configuratie terug te zetten naar fabrieksinstellingen ofwel door NVDA+control+r drie keer snel in te drukken of door te kiezen voor "zet de configuratie terug naar fabrieksinstellingen" in het NVDA menu. (#2086)
* Ondersteuning voor de Seika Versie 3, 4 en 5 en Seika80 brailleleesregels van Nippon Telesoft. (#2452)
* De eerste en laatste top routing knoppen op Freedom Scientific PAC Mate en Focus Brailleleesregels kunnenn nu gebruikt worden om achterwaarts en voorwaarts te scrollen. (#2556)
* Veel meer features zijn ondersteund op Freedom Scientific Focus Brailleleesregels zoals advance bars, rocker bars en bepaalde puntcombinaties voor veelgebruikte acties. (#2516)
* In toepassingen die IAccessible2 gebruiken "zoals Mozillatoepassingen) kunnen rij- en kolomkoppen van een tabel nu worden gemeld buiten bladermodus. (#926)
* Vroegtijdige ondersteuning voor de document control in Microsoft Word 2013. (#2543)
* Tekstuitlijning kan nu worden gemeld in toepassingen die IAccessible2 gebruiken zoals Mozillatoepassingen. (#2612)
* Als een tabelrij of standaard Windows lijstbeeld control met meerdere kolommen focus krijgt, kunt u nu de tabelnavigatiecommando's gebruiken om toegang te krijgen tot individuele cellen. (#828)
* Nieuwe brailletabellen: Ests graad 0, Portugees 8 punt computerbraille, Italiaans 6 punt computerbraille. (#2319, #2662)
* Als NVDA op het systeem is geïnstalleerd, kunt u een NVDA add-on package direct openen om te installeren (b.v. vanuit Windows Explorer of na het downloaden in een web browser). (#2306)
* Ondersteuning voor nieuwere modellen van Papenmeier BRAILLEX brailleleesregels. (#1265)
* Positie informatie (b.v. 1 van 4) wordt nu gemeld voor Windows Explorer lijstitems op Windows 7 en hoger. Dit omvat ook alle UIAutomation controls die de itemIndex en itemCount custom eigenschappen ondersteunen. (#2643)

### Veranderingen

* In het NVDA leescursor dialoogvenster is de Follow toetsenbord focus optie hernoemd naar Follow systeem focus voor consistentie met terminologie die elders in NVDA voorkomt.
* Als braille aan de leescursor gekoppeld is en de cursor is op een object dat geen tekstobject is (b.v. een bewerkbaar tekstveld), activeren cursor routing toetsen nu het object. (#2386)
* De optie "instellingen opslaan bij afsluiten" is nu standaard ingeschakeld voor nieuwe configuraties.
* Bij het updaten van een geïnstalleerde versie van NVDA wordt de bureaublad-sneltoets niet langer teruggezet naar control+alt+n als de gebruiker hem manueel had veranderd in iets anders. (#2572)
* De add-ons lijst in de Add-ons Manager toont nu de package naam voorafgaand aan zijn status. (#2548)
* Als u dezelfde of een andere versie van een momenteel geïnstalleerde add-on installeert, zal NVDA vragen of u de add-on wilt bijwerken in plaats van enkel een fout te tonen en de installatie af te breken. (#2501)
* Objectnavigatiecommando's (behalve het meld huidig object commando) melden nu met minder breedsprakigheid. U kan de extra informatie nog steeds krijgen door het meld huidig object commando te gebruiken. (#2560)
* Liblouis braillevertaler bijgewerkt naar 2.5.1. (#2319, #2480, #2662, #2672)
* Het NVDA Key Commands Quick Reference document is hernoemd naar Commands Quick Reference omdat het nu zowel aanraakgebaren bevat als toetsenbordcommando's.
* De Elementenlijst in bladermodus onthoudt nu het laatst getoonde elementtype (b.v. links, koppen of oriëntatiepunten) elke keer het dialoogvenster wordt getoond tijdens dezelfde sessie van NVDA. (#365)
* De meeste Metro apps in Windows 8 (b.v. Mail, Calendar) activeren niet langer de bladermodus voor de volledige app.
* Handy Tech BrailleDriver COM-Server bijgewerkt naar 1.4.2.0.

### Opgeloste Problemen

* In Windows Vista en later behandelt NVDA de Windowstoets niet langer foutief als ingedrukt bij het unlocken van Windows nadat het is gelocked door Windows+l te drukken. (#1856)
* In Adobe Reader worden rijkoppen nu correct herkend als tabelcellen; i.e. coördinaten worden gemeld en ze kunnen benaderd worden met tabelnavigatiecommando's. (#2444)
* In Adobe Reader worden tabelcellen die meer dan één kolom en/of rij overspannen nu correct behandeld. (#2437, #2438, #2450)
* Het NVDA distributiepakket controleert nu zijn integriteit voordat het wordt uitgevoerd. (#2475)
* Tijdelijke downloadbestanden worden nu verwijderd als het downloaden van een NVDA update mislukt is. (#2477)
* NVDA loopt niet langer vast als het draait als een administrator tijdens het kopiëren van de gebruikersconfiguratie naar de systeemconfiguratie (voor gebruik op Windows logon en andere beveiligde schermen). (#2485)
* Tegels op het Windows 8 Startscherm worden nu beter getoond in spraak en braille. De naam wordt niet langer herhaald, Niet Geselecteerd wordt niet langer gemeld op alle tegels, en live status informatie wordt getoond als de beschrijving van de tegel (b.v. huidige temperatuur voor de Weather tegel).
* Paswoorden worden niet langer aangekondigd bij het lezen van paswoordvelden in Microsoft Outlook en andere standaard invoercontrols die gemarkeerd zijn als beveiligd. (#2021)
* In Adobe Reader worden veranderingen aan formuliervelden nu correct weergegeven in bladermodus. (#2529)
* Verbeterde ondersteuning voor de Microsoft Word spellingscontrole, inclusief meer accuraat lezen van de huidige spellingsfout, en de mogelijkheid om de spellingscontrole te ondersteunen als u een geïnstalleerde kopie van NVDA gebruikt in Windows Vista of hoger.
* Add-ons die bestanden bevatten met niet-Engelse karakters kunnen nu in de meeste gevallen correct worden geïnstalleerd. (#2505)
* In Adobe Reader gaat de taal van de tekst niet langer verloren als ze wordt bijgewerkt of als ernaar gescrolld wordt. (#2544)
* Bij het installeren van een add-on, toont het bevestigingsdialoogvenster nu correct de vertaalde naam van de add-on indien beschikbaar. (#2422)
* In toepassingen die UI Automation gebruiken (zoals .net en Silverlight-toepassingen), is de berekening van numerieke waarden voor controls zoals sliders gecorrigeerd. (#2417)
* De configuratie voor het melden van voortgangsbalken is nu erkend voor de onbepaalde voortgangsbalken, getoond door NVDA bij het installeren, maken van een draagbare kopie, etc. (#2574)
* NVDA-commando's kunnen niet langer uitgevoerd worden vanop een brailleleesregel als een secure Windows scherm (zoals het Lock scherm) actief is. (#2449)
* In bladermodus wordt braille nu bijgewerkt als de tekst die getoond wordt verandert. (#2074)
* Als op een secure Windows scherm zoals het Lock scherm, berichten van toepassingen speaking of displaying braille direct via NVDA worden nu genegeerd.
* In bladermodus is het niet langer mogelijk buiten de onderkant van het document te gaan met pijl rechts als u op het laatste karakter bent, of bij het springen naar het einde van een container als die container het laatste item is in het document. (#2463)
* Onbelangrijke inhoud wordt niet langer foutief inbegrepen bij het melden van de tekst van dialoogvensters in webtoepassingen (specifiek in ARIA dialoogvensters zonder aria-describedby attribuut). (#2390)
* NVDA meldt of localiseert niet langer foutief bepaalde invoervelden in MSHTML documenten (b.v. Internet Explorer), specifiek waar de auteur van de webpagina een expliciete ARIA role heeft gebruikt. (#2435)
* De backspace-toets wordt nu correct behandeld bij het uitspreken van getypte woorden in Windows command consoles. (#2586)
* Celcoördinaten in Microsoft Excel worden nu opnieuw in Braille getoond.
* In Microsoft Word laat NVDA u niet langer in de steek in een alinea met lijstopmaak als u probeert te navigeren over een opsommingsteken of getal met pijl links of control + pijl links. (#2402)
* In bladermodus in Mozillatoepassingen worden de items in bepaalde lijstboxes (meer bepaald, ARIA list boxes) niet langer foutief weergegeven.
* In bladermodus in Mozillatoepassingen worden bepaalde controls, die werden weergegeven met een fout label of met enkel witruimte, nu weergegeven met het correcte label.
* In bladermodus in Mozillatoepassingen, is sommige overbodige witruimte weggelaten.
* In bladermodus in web browsers worden bepaalde afbeeldingen, die expliciet zijn gemarkeerd als decoratief (meer bepaald, met een alt="" attribuut), nu correct genegeerd.
* In webbrowsers verbergt NVDA nu inhoud die is gemarkeerd als verborgen voor schermlezers (specifiek bij gebruik van het aria-hidden attribuut). (#2117)
* Negatieve bedragen (b.v. -$123) worden nu correct uitgesproken als negatief, onafhankleijk van symboolniveau. (#2625)
* Tijdens het automatisch lezen zal NVDA niet langer foutief terugkeren naar de standaardtaal waar een regel geen zin beëindigt. (#2630)
* Lettertype informatie wordt nu correct gedetecteerd in Adobe Reader 10.1 en later. (#2175)
* Als in Adobe Reader alternatieve tekst beschikbaar is, zal enkel die tekst worden weergegeven. Vroeger bevatte die soms ook onbelangrijke tekst. (#2174)
* Waar een document een applicatie bevat, wordt de inhoud van de applicatie niet langer inbegrepen in bladermodus. Dit voorkomt onverwacht bewegen binnen de applicatie bij het navigeren. U kan interageren met de applicatie op dezelfde manier als voor embedded objecten. (#990)
* In Mozillatoepassingen wordt de waarde van spin knoppen nu correct gemeld als ze verandert. (#2653)
* Verbeterde ondersteuning voor Adobe Digital Editions zodat het werkt in versie 2.0. (#2688)
* Als u NVDA+PijlOmhoog drukt op een vervolgkeuzelijst in Internet Explorer en andere MSHTML documenten worden niet langer foutief alle items gelezen. Enkel het actieve item zal worden gelezen. (#2337)
* Spraakwoordenboeken slaan nu juist op als u een #-teken gebruikt in het patroon voor vervanging. (#961)
* Bladermodus voor MSHTML documenten (b.v. Internet Explorer) nu correct displays visible content contained binnen verborgen content (specifiek, elementen met een style of visibility:visible binnen een element met style visibility:hidden). (#2097)
* Links in Windows XP's Security Center melden niet langer random junk na hun namen. (#1331)
* UI Automation text controls (b.v. het zoekveld in het Windows 7 Startmenu) worden nu correct aangekondigd als u de muis erover beweegt in plaats van stil te blijven.
* Veranderingen van toetsenbordindeling worden niet langer gemeld tijdens automatisch lezen, wat vooral problematisch was voor meertalige documenten die Arabische tekst bevatten. (#1676)
* De hele inhoud van sommige UI Automation bewerkbare tekstcontrols (b.v. het zoekvak in het Windows 7/8 Startmenu) wordt niet langer aangekondigd elke keer dat het verandert.
* Bij het schakelen tussen groepen op het Windows 8 startscherm, kondigen ongelabelde groepen niet langer hun eerste tegel aan als de naam van de groep. (#2658)
* Bij het openen van het Windows 8 startscherm wordt de focus correct op de eerste tegel geplaatst, in plaats van te springen naar de root van het startscherm wat het navigateren verwarrend kan maken. (#2720)
* NVDA weigert niet langer te starten als het pad naar het gebruikersprofiel bepaalde multibyte karakters bevat. (#2729)
* In bladermodus in Google Chrome wordt de tekst van tabs nu correct weergegeven.
* In bladermodus worden menuknoppen nu correct weergegeven.
* In OpenOffice.org/LibreOffice Calc, werkt het lezen van rekenbladcellen nu correct. (#2765)
* NVDA kan opnieuw functioneren in de Yahoo! Mail berichtenlijst in Internet Explorer. (#2780)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Previous log file is now copied to nvda-old.log on NVDA initialization. Therefore, if NVDA crashes or is restarted, logging information from that session is still accessible for inspection. (#916)
* Fetching the role property in chooseNVDAObjectOverlayClasses no longer causes the role to be incorrect and thus not reported on focus for certain objects such as Windows command consoles and Scintilla controls. (#2569)
* The NVDA Preferences, Tools and Help menus are now accessible as attributes on gui.mainFrame.sysTrayIcon named preferencesMenu, toolsMenu and helpMenu, respectively. This allows plugins to more easily add items to these menus.
* The navigatorObject_doDefaultAction script in globalCommands has been renamed to review_activate.
* Gettext message contexts are now supported. This allows multiple translations to be defined for a single English message depending on the context. (#1524)
 * This is done using the pgettext(context, message) function.
 * This is supported for both NVDA itself and add-ons.
 * xgettext and msgfmt from GNU gettext must be used to create any PO and MO files. The Python tools do not support message contexts.
 * For xgettext, pass the --keyword=pgettext:1c,2 command line argument to enable inclusion of message contexts.
 * See http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts for more information.
* It is now possible to access built-in NVDA modules where they have been overridden by third party modules. See the nvdaBuiltin module for details.
* Add-on translation support can now be used within the add-on installTasks module. (#2715)

## 2012.2.1

Deze versie pakt verschillende potentiële beveiligingszaken aan (door een upgrade naar Python 2.7.3).

## 2012.2

Hoogtepunten in deze versie zijn een ingebouwd installatieprogramma en het aanmaken van een draagbare kopie, automatische updates, eenvoudig beheer van nieuwe NVDA add-ons, aankondiging van afbeeldingen in Microsoft Word, ondersteuning voor Windows 8 Metro style apps, en verschillende belangrijke opgeloste problemen.

### Nieuwe Functies

* NVDA kan nu automatisch controleren op updates, ze downloaden en installeren. (#73)
* Het uitbreiden van NVDA's functionaliteit is vereenvoudigd door de toevoeging van een Add-ons Manager (die u vindt in Extra in het NVDA menu). Deze laat u toe nieuwe NVDA add-on packages (.nvda-addon bestanden) die plugins en drivers bevatten te installeren en verwijderen. Merk op dat de Add-on manager geen oudere custom plugins en drivers toont die manueel zijn gekopieerd naar uw configuratiemap. (#213)
* Veel meer algemene NVDA-functies werken nu in Windows 8 Metro style apps als u een geïnstalleerde versie van NVDA gebruikt, inclusief het uitsprkeen van getypte karakters, en bladermodus voor webdocumenten (inclusief ondersteuning voor de metro versie van Internet Explorer 10). Draagbare kopieën of NVDA hebben geen toegang tot metro style apps. (#1801)
* In bladermodus documenten (Internet Explorer, Firefox, etc.) kunt u nu springen naar het begin en voorbij het einde van bepaalde containing elementen (zoals lijsten en tabellen) met respectievelijk shift+, en ,. (#123)
* Nieuwe taal: Grieks.
* Afbeeldingen en alt-tekst worden nu gemeld in Microsoft Word Documenten. (#2282, #1541)

### Veranderingen

* Het aankondigen van celcoördinaten in Microsoft Excel gebeurt nu nà de inhoud in plaats van ervoor, en dit gebeurt nu enkel als de meld tabellen en meld tabelcelcoördinaten instellingen zijn ingeschakeld in het Documentopmaak instellingen dialoogvenster. (#320)
* NVDA is nu gedistribueerd in één pakket. In plaats van aparte draagbare en installeerbare versies, is er nu slechts één bestand dat een tijdelijke kopie van NVDA zal starten en die u toelaat het programma te installeren of een draagbare kopie aan te maken. (#1715)
* NVDA wordt nu altijd geïnstalleerd in Program Files op alle systemen. Als u een vorige installatie bijwerkt zal het ook automatisch worden verplaatst als het niet vroeger daar was geïnstalleerd.

### Opgeloste Problemen

* Met auto taalverandering ingeschakeld, wordt inhoud zoals alt-tekst voor afbeeldignen en labels voor andere bepaalde controls in Mozilla Gecko (b.v. Firefox) nu gemeld in de aangegeven taal.
* SayAll in BibleSeeker (en andere TRxRichEdit controls) stopt niet langer in het midden van een passage.
* Lijsten in de Windows 8 Explorer bestandseigenschappen (permitions tab) en in Windows 8 Windows Update worden nu correct gelezen.
* Mogelijke vastlopers opgelost in MS Word die konden voorkomen als het meer dan 2 seconden duurde om tekst van een document te verkrijgen (extreem lange regels of inhoudsopgaves). (#2191)
* Detectie van word breaks werkt nu correct waar witruimte wordt gevolgd door bepaalde leestekens. (#1656)
* In bladermodus in Adobe Reader is het nu mogelijk om te navigeren naar koppen zonder een niveau gebruik makend van snelnavigatie en de Elementenlijst. (#2181)
* In Winamp wordt braille nu correct bijgewerkt als u beweegt naar een ander item in de Playlist Editor. (#1912)
* De boom in de elementenlijst (beschikbaar voor bladermodus documenten) heeft nu de juiste afmetingen om de tekst te tonen van elk element. (#2276)
* In toepassingen die de Java Access Bridge gebruiken, worden bewerkbare tekstvelden nu correct in braille getoond. (#2284)
* In toepassingen die de java Access Bridge gebruiken, melden bewerkbare tekstvelden niet langer vreemde karakters in bepaalde omstandigheden. (#1892)
* In toepassingen die de Java Access Bridge gebruiken, wordt, als men aan het einde van een bewerkbaar tekstveld is, de huidige regel nu correct gemeld. (#1892)
* In bladermodus in toepassingen die Mozilla Gecko 14 en later gebruiken (b.v. Firefox 14), werkt snelnavigatie nu voor citaten en embedded objecten. (#2287)
* In Internet Explorer 9 leest NVDA niet langer ongewilde inhoud als de focus beweegt binnen bepaalde oriëntatiepunten of focuseerbare elementen (specifiek, een div element dat focuseerbaar is of een ARIA landmark role heeft).
* Het NVDA-icoon voor de NVDA Desktop en Startmenu snelkoppelingen wordt nu correct getoond in 64 bit versies van Windows. (#354)

### Veranderingen voor Ontwikkelaars (niet vertaald)

* Due to the replacement of the previous NSIS installer for NVDA with a built-in installer in Python, it is no longer necessary for translaters to maintain a langstrings.txt file for the installer. All localization strings are now managed by gettext po files.

## 2012.1

Hoogtepunten in deze versie zijn functies voor vlotter lezen van braille; aanduiding van documentopmaak in braille; toegang tot veel meer opmaakinformatie en verbeterde performantie in Microsoft Word; en ondersteuning voor de iTunes Store.

### New Features

* NVDA can announce the number of leading tabs and spaces of the current line in the order that they are entered. This can be enabled by selecting report line indentation in the document formatting dialogue. (#373)
* NVDA can now detect key presses generated from alternative keyboard input emulation such as on-screen keyboards and speech recognition software.
* NVDA can now detect colors in Windows command consoles.
* Bold, italic and underline are now indicated in braille using signs appropriate to the configured translation table. (#538)
* Much more information is now reported in Microsoft Word documents, including:
 * Inline information such as footnote and endnote numbers, heading levels, the existence of comments, table nesting levels, links, and text color;
 * Reporting when entering document sections such as the comments story, footnotes and endnotes stories, and header and footer stories.
* Braille now indicates selected text using dots 7 and 8. (#889)
* Braille now reports information about controls within documents such as links, buttons and headings. (#202)
* Support for the hedo ProfiLine and MobilLine USB braille displays. (#1863, #1897)
* NVDA now avoids splitting words in braille when possible by default. This can be disabled in the Braille Settings dialog. (#1890, #1946)
* It is now possible to have braille displayed by paragraphs instead of lines, which may allow for more fluent reading of large amounts of text. This is configurable using the Read by paragraphs option in the Braille Settings dialog. (#1891)
* In browse mode, you can activate the object under the cursor using a braille display. This is done by pressing the cursor routing key where the cursor is located (which means pressing it twice if the cursor is not already there). (#1893)
* Basic support for web areas in iTunes such as the Store. Other applications using WebKit 1 may also be supported. (#734)
* In books in Adobe Digital Editions 1.8.1 and later, pages are now turned automatically when using say all. (#1978)
* New braille translation tables: Portuguese grade 2, Icelandic 8 dot computer braille, Tamil grade 1, Spanish 8 dot computer braille, Farsi grade 1. (#2014)
* You can now configure whether frames in documents are reported from the Document Formatting preferences dialog. (#1900)
* Sleep mode is automatically enabled when using OpenBook. (#1209)
* In Poedit, translators can now read translator added and automatically extracted comments. Messages that are untranslated or fuzzy are marked with a star and a beep is heard when you navigate onto them. (#1811)
* Support for the HumanWare Brailliant BI and B series displays. (#1990)
* New languages: Norwegian Bokmål, Traditional Chinese (Hong Kong).

### Changes

* Commands to describe the current character or to spell the current word or line now will spell in the appropriate language according to the text, if auto language switching is turned on and the appropriate language information is available.
* Updated eSpeak speech synthesizer to 1.46.02.
* NVDA will now truncate extremely long (30 characters or greater) names guessed from graphic and link URLs as they are most likely garbage that gets in the way of reading. (#1989)
* Some information displayed in braille has been abbreviated. (#1955, #2043)
* When the caret or review cursor moves, braille is now scrolled in the same way as when it is manually scrolled. This makes it more appropriate when braille is configured to read by paragraphs and/or avoid splitting words. (#1996)
* Updated to new Spanish grade 1 braille translation table.
* Updated liblouis braille translator to 2.4.1.

### Bug Fixes

* In Windows 8, focus is no longer incorrectly moved away from the Windows Explorer search field, which was not allowing NVDA to interact with it.
* Major performance improvements when reading and navigating Microsoft Word documents while automatic reporting of formatting is enabled, thus now making it quite comfortable to proof read formatting etc. Performance may be also improved over all for some users.
* Browse mode is now used for full screen Adobe Flash content.
* Fixed poor audio quality in some cases when using Microsoft Speech API version 5 voices with the audio output device set to something other than the default (Microsoft Sound Mapper). (#749)
* Again allow NVDA to be used with the "no speech" synthesizer, relying purely on braille or the speech viewer. (#1963)
* Object navigation commands no longer report "No children" and "No parents", but instead report messages consistent with the documentation.
* When NVDA is configured to use a language other than English, the name of the tab key is now reported in the correct language.
* In Mozilla Gecko (e.g. Firefox), NVDA no longer intermittently switches to browse mode while navigating menus in documents. (#2025)
* In Calculator, the backspace key now reports the updated result instead of reporting nothing. (#2030)
* In browse mode, the move mouse to current navigator object command now routes to the center of the object at the review cursor instead of the top left, making it more accurate it some cases. (#2029)
* In browse mode with automatic focus mode for focus changes enabled, focusing on a toolbar will now switch to focus mode. (#1339)
* The report title command works correctly again in Adobe Reader.
* With automatic focus mode for focus changes enabled, focus mode is now correctly used for focused table cells; e.g. in ARIA grids. (#1763)
* In iTunes, position information in certain lists is now reported correctly.
* In Adobe Reader, some links are no longer treated as containing read-only editable text fields.
* The labels of some editable text fields are no longer incorrectly included when reporting the text of a dialog. (#1960)
* The description of groupings is once again reported if reporting of object descriptions is enabled.
* The human readable sizes are now included in the text of the Windows Explorer drive properties dialog.
* Double reporting of property page text has been suppressed in some cases. (#218)
* Improved tracking of the caret in editable text fields which rely on text written to the screen. In particular, this improves editing in the Microsoft Excel cell editor and the Eudora message editor. (#1658)
* In Firefox 11, the move to containing virtual buffer command (NVDA+control+space) now works as it should to escape embedded objects such as Flash content.
* NVDA now restarts itself correctly (e.g. after changing the configured language) when it is located in a directory which contains non-ASCII characters. (#2079)
* Braille correctly respects the settings for reporting of object shortcut keys, position information and descriptions.
* In Mozilla applications, switching between browse and focus modes is no longer slow with braille enabled. (#2095)
* Routing the cursor to the space at the end of the line/paragraph using braille cursor routing keys in some editable text fields now works correctly instead of routing to the start of the text. (#2096)
* NVDA again works correctly with the Audiologic Tts3 synthesizer. (#2109)
* Microsoft Word documents are correctly treated as multi-line. This causes braille to behave more appropriately when a document is focused.
* In Microsoft Internet Explorer, errors no longer occur when focusing on certain rare controls. (#2121)
* Changing the pronunciation of punctuation/symbols by the user will now take effect straight away, rather than requiring NVDA to be restarted or auto language switching to be disabled.
* When using eSpeak, speech no longer goes silent in some cases in the Save As dialog of the NVDA Log Viewer. (#2145)

### Changes for Developers

* There is now a remote Python console for situations where remote debugging is useful. See the Developer Guide for details.
* The base path of NVDA's code is now stripped from tracebacks in the log to improve readability. (#1880)
* TextInfo objects now have an activate() method to activate the position represented by the TextInfo.
 * This is used by braille to activate the position using cursor routing keys on a braille display. However, there may be other callers in future.
* TreeInterceptors and NVDAObjects which only expose one page of text at a time can support automatic page turns during say all by using the textInfos.DocumentWithPageTurns mix-in. (#1978)
* Several control and output constants have been renamed or moved. (#228)
 * speech.REASON_* constants have been moved to controlTypes.
 * In controlTypes, speechRoleLabels and speechStateLabels have been renamed to just roleLabels and stateLabels, respectively.
* Braille output is now logged at level input/output. First, the untranslated text of all regions is logged, followed by the braille cells of the window being displayed. (#2102)
* subclasses of the sapi5 synthDriver can now override _getVoiceTokens and extend init to support custom voice tokens such as with sapi.spObjectTokenCategory to get tokens from a custom registry location.

## 2011.3

Highlights of this release include automatic speech language switching when reading documents with appropriate language information; support for 64 bit Java Runtime Environments; reporting of text formatting in browse mode in Mozilla applications; better handling of application crashes and freezes; and initial fixes for Windows 8.

### New Features

* NVDA can now change the eSpeak synthesizer language on the fly when reading certain web/pdf documents with appropriate language information. Automatic language/dialect switching can be toggled on and off from the Voice Settings dialog. (#845)
* Java Access Bridge 2.0.2 is now supported, which includes support for 64 bit Java Runtime Environments.
* In Mozilla Gecko (e.g. Firefox) Heading levels are now announced  when using object navigation.
* Text formatting can now be reported when using browse mode in Mozilla Gecko (e.g. Firefox and Thunderbird). (#394)
* Text with underline and/or strikethrough can now be detected and reported in standard IAccessible2 text controls such as in Mozilla applications.
* In browse mode in Adobe Reader, table row and column counts are now reported.
* Added support for the Microsoft Speech Platform synthesizer. (#1735)
* Page and line numbers are now reported for the caret in IBM Lotus Symphony. (#1632)
* The percentage of how much the pitch changes when speaking a capital letter is now configurable from the voice settings dialog. However, this does replace the older raise pitch for capitals checkbox (therefore to turn off this feature set the percentage to 0). (#255)
* Text and background color is now included in the reporting of formatting for cells in Microsoft Excel. (#1655)
* In applications using the Java Access Bridge, the activate current navigator object command now works on controls where appropriate. (#1744)
* New language: Tamil.
* Basic support for Design Science MathPlayer.

### Changes

* NVDA will now restart itself if it crashes.
* Some information displayed in braille has been abbreviated. (#1288)
* the Read active window script (NVDA+b) has been improved to filter out unuseful controls   and also is now much more easy to silence. (#1499)
* Automatic say all when a browse mode document loads is now optional via a setting in the Browse Mode settings dialog. (#414)
* When trying to read the status bar (Desktop NVDA+end), If a real status bar object cannot be located, NVDA will instead resort to using the bottom line of text written to the display for the active application. (#649)
* When reading with say all in browse mode documents, NVDA will now pause at the end of headings and other block-level elements, rather than speaking the text together with the next lot of text as one long sentence.
* In browse mode, pressing enter or space on a tab now activates it instead of switching to focus mode. (#1760)
* Updated eSpeak speech synthesizer to 1.45.47.

### Bug Fixes

* NVDA  no longer shows bullets or numbering for lists in Internet Explorer and other MSHTML controls when the author has indicated that these should not be shown (i.e. the list style is "none"). (#1671)
* Restarting NVDA when it has frozen (e.g. by pressing control+alt+n) no longer exits the previous copy without starting a new one.
* Pressing backspace or arrow keys in a Windows command console no longer causes strange results in some cases. (#1612)
* The selected item in WPF combo boxes (and possibly some other combo boxes exposed using UI Automation) which do not allow text editing is now reported correctly.
* In browse mode in Adobe Reader, it is now always possible to move to the next row from the header row and vice versa using the move to next row and move to previous row commands. Also, the header row is no longer reported as row 0. (#1731)
* In browse mode in Adobe Reader, it is now possible to move to (and therefore past) empty cells in a table.
* Pointless position information (e.g. 0 of 0 level 0) is no longer reported in braille.
* When braille is tethered to review, it is now able to show  content in flat review. (#1711)
* A text control's text is no longer presented twice on a braille display in some cases, e.g. scrolling back from the start of Wordpad documents.
* In browse mode in Internet Explorer, pressing enter on a file upload button now correctly presents the dialog to choose a file to upload instead of switching to focus mode. (#1720)
* Dynamic content changes such as in Dos consoles are no longer announced if  sleep mode for that application is currently on. (#1662)
* In browse mode, the behaviour of alt+upArrow and alt+downArrow to collapse and expand combo boxes has been improved. (#1630)
* NVDA now recovers from many more situations such as applications that stop responding which previously caused it to freeze completely. (#1408)
* For Mozilla Gecko (Firefox etc) browse mode documents NVDA will no longer fail to render text in a very specific situation where an element is styled as display:table. (#1373)
* NVDA will no longer announce label controls when focus moves inside of them. Stops double announcements of labels for some form fields in Firefox (Gecko) and Internet Explorer (MSHTML). (#1650)
* NVDA no longer fails to read a cell in Microsoft Excel after pasting in to it with control+v. (#1781)
* In Adobe Reader, extraneous information about the document is no longer announced when moving to a control on a different page in focus mode. (#1659)
* In browse mode in Mozilla Gecko applications (e.g. Firefox), toggle buttons are now detected and reported correctly. (#1757)
* NVDA can now   correctly read the Windows Explorer Address Bar in Windows 8 developer preview.
* NVDA will no longer crash apps such as winver and wordpad in Windows 8 developer preview due to bad glyph translations.
* In browse mode in applications using Mozilla Gecko 10 and later (e.g. Firefox 10), the cursor is more often positioned correctly when loading a page with a target anchor. (#360)
* In browse mode in Mozilla Gecko applications (e.g. Firefox), labels for image maps are now rendered.
* With mouse tracking enabled, moving the mouse over certain editable text fields (such as in Synaptics Pointing Device Settings and SpeechLab SpeakText) no longer causes the application to crash. (#672)
* NVDA now functions correctly in several about dialogs in applications distributed with Windows XP, including the About dialog in Notepad and the About Windows dialog. (#1853, #1855)
* Fixed reviewing by word in Windows Edit controls. (#1877)
* Moving out of an editable text field with leftArrow, upArrow or pageUp while in focus mode now correctly switches to browse mode when automatic focus mode for caret movement is enabled. (#1733)

### Changes for Developers

* NVDA can now instruct speech synthesizers to switch languages for particular sections of speech.
 * To support this, drivers must handle speech.LangChangeCommand in sequences past to SynthDriver.speak().
 * SynthDriver objects should also provide the language argument to VoiceInfo objects (or override the language attribute to retrieve the current language). Otherwise, NVDA's user interface language will be used.

## 2011.2

Highlights of this release include major improvements concerning punctuation and symbols, including configurable levels, custom labelling and character descriptions; no pauses at the end of lines during say all; improved support for ARIA in Internet Explorer; better support for XFA/LiveCycle PDF documents in Adobe Reader; access to text written to the screen in more applications; and access to formatting and color information for text written to the screen.

### New Features

* It is now possible to hear the description for any given character by pressing the review current character script twice in quick succession.  For English characters this is the standard English phonetic alphabet. For pictographic languages such as traditional Chinese, one or more example phrases using the given symbol are provided. Also pressing review current word or review current line three times will spell the word/line using the first of these descriptions. (#55)
* More text can be seen in flat review for applications such as Mozilla Thunderbird that write their text directly to the display as glyphs.
* It is now possible to choose from several levels of punctuation and symbol announcement. (#332)
* When punctuation or other symbols are repeated more than four times, the number of repetitions is now announced instead of speaking the repeated symbols. (#43)
* New braille translation tables: Norwegian 8 dot computer braille, Ethiopic grade 1, Slovene grade 1, Serbian grade 1. (#1456)
* Speech no longer unnaturally pauses at the end of each line when using the say all command. (#149)
* NVDA will now announce whether something is sorted (according to the aria-sort property) in web browsers. (#1500)
* Unicode Braille Patterns are now displayed correctly on braille displays. (#1505)
* In Internet Explorer and other MSHTML controls when focus moves inside a group of controls (surrounded by a fieldset), NVDA will now announce the name of the group (the legend). (#535)
* In Internet Explorer and other MSHTML controls, the aria-labelledBy and aria-describedBy properties are now honoured.
* in Internet Explorer and other MSHTML controls, support for ARIA list, gridcell, slider and progressbar controls has been improved.
* Users can now change the pronunciation of punctuation and other symbols, as well as the symbol level at which they are spoken. (#271, #1516)
* In Microsoft Excel, the name of the active sheet is now reported when switching sheets with control+pageUp or control+pageDown. (#760)
* When navigating a table in Microsoft Word with the tab key NVDA will now announce the current cell as you move. (#159)
* You can now configure whether table cell coordinates are reported from the Document Formatting preferences dialog. (#719)
* NVDA can now detect formatting and color for text written to the screen.
* In the Outlook Express/Windows Mail/Windows Live Mail message list, NVDA will now announce the fact that a message is unread and also if it's expanded or collapsed in the case of conversation threads. (#868)
* eSpeak now has a rate boost setting which triples the speaking rate.
* Support for the  calendar control found in the Date and Time Information dialog accessed from the  Windows 7 clock. (#1637)
* Additional key bindings have been added for the MDV Lilli braille display. (#241)
* New languages: Bulgarian, Albanian.

### Changes

* To move the caret to the review cursor, now press the move focus to navigator object script (desktop NVDA+shift+numpadMinus, laptop NVDA+shift+backspace) twice in quick succession. This frees up more keys on the keyboard. (#837)
* To hear the  decimal and hexadecimal representation of the character under the review cursor, now press review current character three times rather than twice, as twice now speaks the character description.
* Updated eSpeak speech synthesiser to 1.45.03. (#1465)
* Layout tables are no longer announced in Mozilla Gecko applications while moving the focus when in focus mode or outside of a document.
* In Internet Explorer and other MSHTML controls, browse mode now works for documents inside ARIA applications. (#1452)
* Updated liblouis braille translator to 2.3.0.
* When in browse mode  and jumping to a control with quicknav or focus, the description of the control is now announced if it has one.
* Progress bars are now announced in brows mode.
* Nodes marked with an ARIA role of presentation in Internet Explorer and other MSHTML controls are now filtered out of simple review and the focus ancestry.
* NVDA's user interface and documentation now refer to virtual buffers as browse mode, as the term "virtual buffer" is rather meaningless to most users. (#1509)
* When the user wishes to copy their user settings to the system profile for use on the logon screen, etc., and their settings contain custom plugins, they are now warned that this could be a security risk. (#1426)
* The NVDA service no longer starts and stops NVDA on user input desktops.
* On Windows XP and Windows Vista, NVDA no longer makes use of UI Automation even if it is available via the platform update. Although using UI Automation can improve the accessibility of some modern applications, on XP and Vista there were too many freezes, crashes and over all performance loss while using it. (#1437)
* In applications using Mozilla Gecko 2 and later (such as Firefox 4 and later), a document can now be read in browse mode before it is fully finished loading.
* NVDA now announces the state of a container when focus moves to a control inside it (e.g. if focus moves inside a document that is still loading it will report it as busy).
* NVDA's user interface and documentation no longer use the terms "first child" and "parent" with respect to object navigation, as these terms are confusing for many users.
* Collapsed is no longer reported for some menu items which have sub-menus.
* The reportCurrentFormatting script (NVDA+f) now reports the formatting at the position of the review cursor rather than the system caret / focus. As  by default the review cursor follows the caret, most people should not notice a difference. However this now enables the user to find out the formatting when moving the review cursor, such as in flat review.

### Bug Fixes

* Collapsing combo boxes in browse mode documents when focus mode has been forced with NVDA+space no longer auto-switches back to browse mode. (#1386)
* In Gecko (e.g. Firefox) and MSHTML (e.g. Internet Explorer) documents, NVDA now correctly renders certain text on the same line which was previously rendered on separate lines. (#1378)
* When Braille is tethered to review and the navigator object is moved to a browse mode document, either manually or due to a focus change, braille will appropriately show the browse mode content. (#1406, #1407)
* When speaking of punctuation is disabled, certain punctuation is no longer incorrectly spoken when using some synthesisers. (#332)
* Problems no longer occur when loading configuration for synthesisers which do not support the voice setting such as Audiologic Tts3. (#1347)
* The Skype Extras menu is now read correctly. (#648)
* Checking the Brightness controls volume checkbox in the Mouse Settings dialog should no longer cause a major lag for beeps when moving the mouse around the screen on Windows Vista/Windows 7 with Aero enabled. (#1183)
* When NVDA is configured to use the laptop keyboard layout, NVDA+delete now works as documented to report the dimensions of the current navigator object. (#1498)
* NVDA now Appropriately honours the aria-selected attribute in Internet Explorer documents.
* When NVDA automatically switches to focus mode in browse mode documents, it now announces information about the context of the focus. For example, if a list box item receives focus, the list box will be announced first. (#1491)
* In Internet Explorer and other MSHTML controls, ARIA listbox controls are now treeted as lists, rather than list items.
* When a read-only editable text control receives focus, NVDA now reports that it is read-only. (#1436)
* In browse mode, NVDA now behaves correctly with respect to read-only editable text fields.
* In browse mode documents, NVDA no longer incorrectly switches out of focus mode when aria-activedescendant is set; e.g. when the completion list appeared in some auto complete controls.
* In Adobe Reader, the name of controls is now reported when moving focus or using quick navigation in browse mode.
* In XFA PDF documents in Adobe Reader, buttons, links and graphics are now rendered correctly.
* In XFA PDF documents in Adobe Reader, all elements are now rendered on separate lines. This change was made because large sections (sometimes even the entire document) were being rendered without breaks due to the general lack of structure in these documents.
* Fixed problems when moving focus to or away from editable text fields in XFA PDF documents in Adobe Reader.
* In XFA PDF documents in Adobe Reader, changes to the value of a focused combo box will now be reported.
* Owner-drawn Combo boxes such as the ones to choose colors in Outlook Express are now accessible with NVDA. (#1340)
* In languages which use a space as a digit group/thousands separator such as French and German, numbers from separate chunks of text are no longer pronounced as a single number. This was particularly problematic for table cells containing numbers. (#555)
* nodes with an ARIA role of description in Internet Explorer and other MSHTML controls now are classed as static text, not edit fields.
* Fixed various issues when pressing tab while focus is on a document in browse mode (e.g. tab inappropriately moving to the address bar in Internet Explorer). (#720, #1367)
* When entering lists while reading text, NVDA now says, for example, "list with 5 items" instead of "listwith 5 items". (#1515)
* In input help mode, gestures are logged even if their scripts bypass input help such as the scroll braille display forward and back commands.
* In input help mode, when a modifier is held down on the keyboard, NVDA no longer reports the modifier as if it is modifying itself; e.g. NVDA+NVDA.
* In Adobe Reader documents, pressing c or shift+c to navigate to a combo box now works.
* The selected state of selectable table rows is now reported the same way it is for list and tree view items.
* Controls in Firefox and other Gecko applications can now be activated while in browse mode even if their content has been floated off-screen. (#801)
* You can no longer show an NVDA settings dialog while a message dialog is being shown, as the settings dialog was frozen in this case. (#1451)
* In Microsoft Excel, there is no longer a lag when holding down or rapidly pressing keys to move between or select cells.
* Fixed intermittent crashes of the NVDA service which meant that NVDA stopped running on secure Windows screens.
* Fixed problems that sometimes occurred with braille displays when a change caused text that was being displayed to disappear. (#1377)
* The downloads window in Internet Explorer 9 can now be navigated and read with NVDA. (#1280)
* It is no longer possible to accidentally start multiple copies of NVDA at the same time. (#507)
* On slow systems, NVDA no longer inappropriately causes its main window to be shown all the time while running. (#726)
* NVDA no longer crashes on Windows xP when starting a WPF application. (#1437)
* Say all and say all with review are now able to work in UI automation text controls that support all required functionality. For example, you can now use say all with review on XPS Viewer documents.
* NVDA no longer inappropriately classes some list items in the Outlook Express / Windows Live Mail message rules Apply Now dialog as being checkboxes. (#576)
* Combo boxes are no longer reported as having a sub-menu.
* NVDA is  now able to read the recipiants in the To, CC and BCC fields in Microsoft Outlook. (#421)
* Fixed the issue in NVDA's Voice Settings dialog where the value of sliders was sometimes not reported when changed. (#1411)
* NVDA no longer fails to announce the new cell when moving in an Excel spreadsheet after cutting and pasting. (#1567)
* NVDA no longer becomes worse at guessing color names the more colors it announces.
* In Internet Explorer and other MSHTML controls, fixed the inability to read parts of rare pages which contain iframes marked with an ARIA role of presentation. (#1569)
* In Internet Explorer and other MSHTML controls, fixed a rare problem where the focus kept bouncing infinitely between the document and a multi-line editable text field in focus mode. (#1566)
* In Microsoft Word 2010 NVDA will now automatically read confirmation dialogs. (#1538)
* In multi-line editable text fields in Internet Explorer and other MSHTML controls, selection on lines after the first is now reported correctly. (#1590)
* Improved moving by word in many cases, including browse mode and Windows Edit controls. (#1580)
* The NVDA installer no longer shows garbled text for Hong Kong versions of Windows Vista and Windows 7. (#1596)
* NVDA no longer fails to load the Microsoft Speech API version 5 synthesizer if the configuration contains settings for that synthesizer but is missing the voice setting. (#1599)
* In editable text fields in Internet Explorer and other MSHTML controls, NVDA no longer lags or freezes when braille is enabled.
* In firefox brows mode, NVDA no longer refuses to include content that is inside a focusable node with an ARIA role of presentation.
* In Microsoft Word with braille enabled, lines on pages after the first page are now reported correctly. (#1603)
* In Microsoft Word 2003, lines of right-to-left text can once again be read with braille enabled. (#627)
* In Microsoft Word, say all now works correctly when the document does not end with a sentence ending.
* When opening a plain text message in Windows Live Mail 2011, NVDA will correctly focus on the message document allowing it to be read.
* NVDA no longer temporarily freezes or refuses to speak when in the Move to / Copy to dialogs in Windows Live Mail. (#574)
* In Outlook 2010, NVDA will now correctly track the focus in the message list. (#1285)
* Some USB connection issues have been resolved with the MDV Lilli braille display. (#241)
* In Internet explorer and other MSHTML controls, spaces are no longer ignored in browse mode in certain cases (e.g. after a link).
* In Internet Explorer and other MSHTML controls, some extraneous line breaks have been eliminated in browse mode. specifically, HTML elements with a display style of None no longer force a line break. (#1685)
* If NVDA is unable to start, failure to play the Windows critical stop sound no longer clobbers the critical error message in the log file.

### Changes for Developers

* Developer documentation can now be generated using SCons. See readme.txt at the root of the source distribution for details, including associated dependencies.
* Locales can now provide descriptions for characters. See the Character Descriptions section of the Developer Guide for details. (#55)
* Locales can now provide information about the pronunciation of specific punctuation and other symbols. See the Symbol Pronunciation section of the Developer Guide for details. (#332)
* You can now build NVDAHelper with several debugging options using the nvdaHelperDebugFlags SCons variable. See readme.txt at the root of the source distribution for details. (#1390)
* Synth drivers are now passed a sequence of text and speech commands to speak, instead of just text and an index.
 * This allows for embedded indexes, parameter changes, etc.
 * Drivers should implement SynthDriver.speak() instead of SynthDriver.speakText() and SynthDriver.speakCharacter().
 * The old methods will be used if SynthDriver.speak() is not implemented, but they are deprecated and will be removed in a future release.
* gui.execute() has been removed. wx.CallAfter() should be used instead.
* gui.scriptUI has been removed.
 * For message dialogs, use wx.CallAfter(gui.messageBox, ...).
 * For all other dialogs, real wx dialogs should be used instead.
 * A new gui.runScriptModalDialog() function simplifies using modal dialogs from scripts.
* Synth drivers can now support boolean settings. See SynthDriverHandler.BooleanSynthSetting.
* SCons now accepts a certTimestampServer variable specifying the URL of a timestamping server to use to timestamp authenticode signatures. (#1644)

## 2011.1.1

This release fixes several security and other important issues found in NVDA 2011.1.

### Bug Fixes

* The Donate item in the NVDA menu is now disabled when running on the logon, lock, UAC and other secure Windows screens, as this is a security risk. (#1419)
* It is now impossible to copy or paste within NVDA's user interface while on secure desktops (lock screen, UAC screen and windows logon) as this is a security risk. (#1421)
* In Firefox 4, the move to containing virtual buffer command (NVDA+control+space) now works as it should to escape embedded objects such as Flash content. (#1429)
* When speaking of command keys is enabled, shifted characters are no longer incorrectly spoken as command keys. (#1422)
* When speaking of command keys is enabled, pressing space with modifiers other than shift (such as control and alt) is now reported as a command key. (#1424)
* Logging is now completely disabled when running on the logon, lock, UAC and other secure Windows screens, as this is a security risk. (#1435)
* In input help mode, Gestures are now logged even if they are not bound to a script (in accordance with the user guide). (#1425)

## 2011.1

Highlights of this release include automatic reporting of new text output in mIRC, PuTTY, Tera Term and SecureCRT; support for global plugins; announcement of bullets and numbering in Microsoft Word; additional key bindings for braille displays, including keys to move to the next and previous line; support for several Baum, HumanWare and APH braille displays; and reporting of colors for some controls, including IBM Lotus Symphony text controls.

### New Features

* Colors can now be reported for some controls. Automatic announcement can be configured in the Document Formatting preferences dialog. It can also be reported on demand using the report text formatting command (NVDA+f).
 * Initially, this is supported in standard IAccessible2 editable text controls (such as in Mozilla applications), RichEdit controls (such as in Wordpad) and IBM Lotus Symphony text controls.
* In virtual buffers, you can now select by page (using shift+pageDown and shift+pageUp) and paragraph (using shift+control+downArrow and shift+control+upArrow). (#639)
* NVDA now automatically reports new text output in mIRC, PuTTY, Tera Term and SecureCRT. (#936)
* Users can now add new key bindings or override existing ones for any script in NVDA by providing a single user input gesture map. (#194)
* Support for global plugins. Global plugins can add new functionality to NVDA which works across all applications. (#281)
* A small beep is now heard when typing characters with the shift key while capslock is on. This can be turned off by unchecking the related new option in the Keyboard settings dialog. (#663)
* hard page breaks are now announced when moving by line in Microsoft Word. (#758)
* Bullets and numbering are now spoken in Microsoft Word when moving by line. (#208)
* A command to toggle Sleep mode for the current application (NVDA+shift+s) is now available. Sleep mode (previously known as self voicing mode) disables all screen reading functionality in NVDA for a particular application. Very useful for applications that provide their own speech and or screen reading features. Press this command again to disable Sleep mode.
* Some additional braille display key bindings have been added. See the Supported Braille Displays section of the User Guide for details. (#209)
* For the convenience of third party developers, app modules as well as global plugins can now be reloaded without restarting NVDA. Use tools -&gt; Reload plugins in the NVDA menu or NVDA+control+f3. (#544)
* NVDA now remembers the position you were at when returning to a previously visited web page. This applies until either the browser or NVDA is exited. (#132)
* Handy Tech braille displays can now be used without installing the Handy Tech universal driver. (#854)
* Support for several Baum, HumanWare and APH braille displays. (#937)
* The status bar in Media Player Classic Home Cinema is now recognised.
* The Freedom Scientific Focus 40 Blue braille display can now be used when connected via bluetooth. (#1345)

### Changes

* Position information is no longer reported by default in some cases where it was usually incorrect; e.g. most menus, the Running Applications bar, the Notification Area, etc. However, this can be turned on again by an added option in the Object Presentation settings dialog.
* Keyboard help has been renamed to input help to reflect that it handles input from sources other than the keyboard.
* Input Help no longer reports a script's code location via speech and braille as it is cryptic and irrelevant to the user. However, it is now logged for developers and advanced users.
* When NVDA detects that it has frozen, it continues to intercept NVDA modifier keys, even though it passes all other keys through to the system. This prevents the user from unintentionally toggling caps lock, etc. if they press an NVDA modifier key without realising NVDA has frozen. (#939)
* If keys are held down after using the pass next key through command, all keys (including key repeats) are now passed through until the last key is released.
* If an NVDA modifier key is pressed twice in quick succession to pass it through and the second press is held down, all key repeats will now be passed through as well.
* The volume up, down and mute keys are now reported in input help. This could be helpful if the user is uncertain as to what these keys are.
* The hotkey for the Review Cursor item in the NVDA Preferences menu has been changed from r to c to eliminate the conflict with the Braille Settings item.

### Bug Fixes

* When adding a new speech dictionary entry, the title of the dialog is now "Add dictionary entry" instead of "Edit dictionary entry". (#924)
* In speech dictionary dialogs, the content of the Regular expression and Case sensitive columns of the Dictionary entries list is now presented in the configured NVDA language instead of always in English.
* In AIM, position information is now announced in tree views.
* On sliders in the Voice Settings dialog, up arrow/page up/home now increase the setting and down arrow/page down/end decrease it. Previously, the opposite occurred, which is not logical and is inconsistent with the synth settings ring. (#221)
* In virtual buffers with screen layout disabled, some extraneous blank lines no longer appear.
* If an NVDA modifier key is pressed twice quickly but there is an intervening key press, the NVDA modifier key is no longer passed through on the second press.
* Punctuation keys are now spoken in input help even when speaking of punctuation is disabled. (#977)
* In the Keyboard Settings dialog, the keyboard layout names are now presented in the configured NVDA language instead of always in English. (#558)
* Fixed an issue where some items were rendered as empty in Adobe Reader documents; e.g. the links in the table of contents of the Apple iPhone IOS 4.1 User Guide.
* The "Use currently saved settings on the logon and other secure screens" button in NVDA's General Settings dialog now works if used immediately after NVDA is newly installed but before a secure screen has appeared. Previously, NVDA reported that copying was successful, but it actually had no effect. (#1194)
* It is no longer possible to have two NVDA settings dialogs open simultaneously. This fixes issues where one open dialog depends on another open dialog; e.g. changing the synthesiser while the Voice Settings dialog is open. (#603)
* On systems with UAC enabled, the "Use currently saved settings on the logon and other secure screens" button in NVDA's General Settings dialog no longer fails after the UAC prompt if the user's account name contains a space. (#918)
* In Internet Explorer and other MSHTML controls, NVDA now uses the URL as a last resort to determine the name of a link, rather than presenting empty links. (#633)
* NVDA no longer ignores the focus  in AOL Instant Messenger 7 menus. (#655)
* Announce the correct label for errors in the Microsoft Word Spell Check dialog (e.g. Not in dictionary, Grammar error, punctuation). Previously  they were all announced as grammar error. (#883)
* Typing in Microsoft Word while using a braille display should no longer cause garbled text to be typed, and a rare freeze when pressing a braille routing key in Word documents has been fixed. (#1212) However a limitation is that Arabic text can no longer be read in Word 2003 and below, while using a braille display. (#627)
* When pressing the delete key in an edit field, the text/cursor on a braille display should now always be updated appropriately to reflect the change. (#947)
* Changes on dynamic pages in Gecko2 documents (E.g. Firefox 4) while multiple tabs are open are now properly reflected by NVDA. Previously only changes in the first tab were reflected. (Mozilla bug 610985)
* NVDA can now properly announce the suggestions for grammar and punctuation errors in Microsoft Word spell check dialog. (#704)
* In Internet Explorer and other MSHTML controls, NVDA no longer presents destination anchors as empty links in its virtual buffer. Instead, these anchors are hidden as they should be. (#1326)
* Object navigation around and within standard groupbox windows is no longer broken and asymmetrical.
* In Firefox and other Gecko-based controls, NVDA will no longer get stuck in a subframe if it finishes loading before the outer document.
* NVDA  now appropriately announces the next character when deleting a character with numpadDelete. (#286)
* On the Windows XP logon screen, the user name is once again reported when the selected user is changed.
* Fixed problems when reading text in Windows command consoles with reporting of line numbers enabled.
* The Elements List dialog for virtual buffers is now usable by sighted users. All controls are visible on screen. (#1321)
* The list of entries in the Speech Dictionary dialog is now more readable by sighted users. The list is now large enough to show all of its columns on screen. (#90)
* On ALVA BC640/BC680 braille displays, NVDA no longer disregards display keys that are still held down after another key is released.
* Adobe Reader X no longer crashes after leaving the untagged document options before the processing dialog appears. (#1218)
* NVDA now switches to the appropriate braille display driver when you revert to saved configuration. (#1346)
* The Visual Studio 2008 Project Wizard is read correctly again. (#974)
* NVDA no longer completely fails to work in applications which contain non-ASCII characters in their executable name. (#1352)
* When reading by line in AkelPad with word wrap enabled, NVDA no longer reads the first character of the following line at the end of the current line.
* In the Visual Studio 2005/2008 code editor, NVDA no longer reads the entire text after every typed character. (#975)
* Fixed the issue where some braille displays weren't cleared properly when NVDA was exited or the display was changed.
* The initial focus is no longer sometimes spoken twice when NVDA starts. (#1359)

### Changes for Developers

* SCons is now used to prepare the source tree and create binary builds, portable archives, installers, etc. See readme.txt at the root of the source distribution for details.
* The key names used by NVDA (including key maps) have been made more friendly/logical; e.g. upArrow instead of extendedUp and numpadPageUp instead of prior. See the vkCodes module for a list.
* All input from the user is now represented by an inputCore.InputGesture instance. (#601)
 * Each source of input subclasses the base InputGesture class.
 * Key presses on the system keyboard are encompassed by the keyboardHandler.KeyboardInputGesture class.
 * Presses of buttons, wheels and other controls on a braille display are encompassed by subclasses of the braille.BrailleDisplayGesture class. These subclasses are provided by each braille display driver.
* Input gestures are bound to ScriptableObjects using the ScriptableObject.bindGesture() method on an instance or an __gestures dict on the class which maps gesture identifiers to script names. See baseObject.ScriptableObject for details.
* App modules no longer have key map files. All input gesture bindings must be done in the app module itself.
* All scripts now take an InputGesture instance instead of a key press.
 * KeyboardInputGestures can be sent on to the OS using the send() method of the gesture.
* To send an arbitrary key press, you must now create a KeyboardInputGesture using KeyboardInputGesture.fromName() and then use its send() method.
* Locales may now provide an input gesture map file to add new bindings or override existing bindings for scripts anywhere in NVDA. (#810)
 * Locale gesture maps should be placed in locale\LANG\gestures.ini, where LANG is the language code.
 * See inputCore.GlobalGestureMap for details of the file format.
* The new LiveText and Terminal NVDAObject behaviors facilitate automatic reporting of new text. See those classes in NVDAObjects.behaviors for details. (#936)
 * The NVDAObjects.window.DisplayModelLiveText overlay class can be used for objects which must retrieve text written to the display.
 * See the mirc and putty app modules for usage examples.
* There is no longer an _default app module. App modules should instead subclass appModuleHandler.AppModule (the base AppModule class).
* Support for global plugins which can globally bind scripts, handle NVDAObject events and choose NVDAObject overlay classes. (#281) See globalPluginHandler.GlobalPlugin for details.
* On SynthDriver objects, the available* attributes for string settings (e.g. availableVoices and availableVariants)  are now OrderedDicts keyed by ID instead of lists.
* synthDriverHandler.VoiceInfo now takes an optional language argument which specifies the language of the voice.
* SynthDriver objects now provide a language attribute which specifies the language of the current voice.
 * The base implementation uses the language specified on the VoiceInfo objects in availableVoices. This is suitable for most synthesisers which support one language per voice.
* Braille display drivers have been enhanced to allow buttons, wheels and other controls to be bound to NVDA scripts:
 * Drivers can provide a global input gesture map to add bindings for scripts anywhere in NVDA.
 * They can also provide their own scripts to perform display specific functions.
 * See braille.BrailleDisplayDriver for details and existing braille display drivers for examples.
* The 'selfVoicing' property on AppModule classes has now been renamed to 'sleepMode'.
* The app module events event_appLoseFocus and event_appGainFocus have now been renamed to event_appModule_loseFocus and event_appModule_gainFocus, respectivly, in order to make the naming convention consistent with app modules and tree interceptors.
* All braille display drivers should now use braille.BrailleDisplayDriver instead of braille.BrailleDisplayDriverWithCursor.
 * The cursor is now managed outside of the driver.
 * Existing drivers need only change their class statement accordingly and rename their _display method to display.

## 2010.2

Notable features of this release include greatly simplified object navigation; virtual buffers for Adobe Flash content; access to many previously inaccessible controls by retrieving text written to the screen; flat review of screen text; support for IBM Lotus Symphony documents; reporting of table row and column headers in Mozilla Firefox; and significantly improved user documentation.

### New Features

* Navigating through objects with the review cursor has been greatly simplified. The review cursor now excludes objects which aren't useful to the user; i.e. objects only used for layout purposes and unavailable objects.
* In applications using the Java Access Bridge (including OpenOffice.org), formatting can now be reported in text controls. (#358, #463)
* When moving the mouse over cells in Microsoft Excel, NVDA will appropriately announce them.
* In applications using the Java Access Bridge, the text of a dialog is now reported when the dialog appears. (#554)
* A virtualBuffer can now be used to navigate adobe Flash content. Object navigation and interacting with the controls directly (by turning on focus mode) is still supported. (#453)
* Editable text controls in the Eclipse IDE, including the code editor, are now accessible. You must be using Eclipse 3.6 or later. (#256, #641)
* NVDA can now retrieve most text written to the screen. (#40, #643)
 * This allows for reading of controls which do not expose information in more direct/reliable ways.
 * Controls made accessible by this feature include: some menu items which display icons (e.g. the Open With menu on files in Windows XP) (#151), editable text fields in Windows Live applications (#200), the errors list in Outlook Express (#582), the editable text control in TextPad (#605), lists in Eudora, many controls in Australian E-tax and the formula bar in Microsoft Excel.
* Support for the code editor in Microsoft Visual Studio 2005 and 2008. At least Visual Studio Standard is required; this does not work in the Express editions. (#457)
* Support for IBM Lotus Symphony documents.
* Early experimental support for Google Chrome. Please note that Chrome's screen reader support is far from complete and additional work may also be required in NVDA. You will need a recent development build of Chrome to try this.
* The state of toggle keys (caps lock, num lock and scroll lock) is now displayed in braille when they are pressed. (#620)
* Help balloons are now displayed in braille when they appear. (#652)
* Added a driver for the MDV Lilli braille display. (#241)
* When selecting an entire row or column in Microsoft Excel with the shortcut keys shift+space and control+space, the new selection is now reported. (#759)
* Table row and column headers can now be reported. This is configurable from the Document Formatting preferences dialog.
 * Currently, this is supported in documents in Mozilla applications such as Firefox (version 3.6.11 and later) and Thunderbird (version 3.1.5 and later). (#361)
* Introduced commands for flat review: (#58)
 * NVDA+numpad7  switches to flat review, placing the review cursor at the position of the current object, allowing you  to review the screen (or a document if within one) with the text review commands.
 * NVDA+numpad1 moves the review cursor into the object represented by the text at  the position of the review cursor, allowing you to navigate by object from that point.
* Current NVDA user settings can be  copied to be used on secure Windows screens such as the logon and UAC screens by pressing a button in the General Settings dialog. (#730)
* Support for Mozilla Firefox 4.
* Support for Microsoft Internet Explorer 9.

### Changes

* The sayAll by Navigator object (NVDA+numpadAdd), navigator object next in flow (NVDA+shift+numpad6) and navigator object previous in flow (NVDA+shift+numpad4) commands have been removed for the time being, due to bugginess and to free up the keys for other possible features.
* In the NVDA Synthesizer dialog, only the display name of the synthesizer is now listed. Previously, it was prefixed by the driver's name, which is only relevant internally.
* When in embedded applications or virtual buffers inside another virtualBuffer (e.g. Flash), you can now  press nvda+control+space to move out of the embedded application or virtual buffer to the containing document. Previously nvda+space  was used for this. Now nvda+space is specifically only for toggling brows/focus modes on virtualBuffers.
* If the speech viewer (enabled under the tools menu) is given the focus (e.g. it was clicked in) new text will not appear in the control until focus is moved away. This allows for selecting the text with greater ease (e.g. for copying).
* The Log Viewer and Python Console are maximised when activated.
* When focusing on a worksheet in Microsoft Excel and there is more than one cell selected, the selection range is announced, rather than just the active cell. (#763)
* Saving configuration and changing of particular sensitive options is now disabled when running on the logon, UAC and other secure Windows screens.
* Updated eSpeak speech synthesiser to 1.44.03.
* If NVDA is already running, activating the NVDA shortcut on the desktop (which includes pressing control+alt+n) will restart NVDA.
* Removed the report text under the mouse checkbox from the Mouse settings dialog and replaced it with an Enable mouse tracking checkbox, which better matches the toggle mouse tracking script (NVDA+m).
* Updates to the laptop keyboard layout so that it includes all commands available in the desktop layout and works correctly on non-English keyboards. (#798, #800)
* Significant improvements and updates to the user documentation, including documentation of the laptop keyboard commands and synchronisation of the Keyboard Commands Quick Reference with the User Guide. (#455)
* Updated liblouis braille translator to 2.1.1. Notably, this fixes some issues related to Chinese braille as well as characters which are undefined in the translation table. (#484, #499)

### Bug Fixes

* In µTorrent, the focused item in the torrents list no longer reports repeatedly or steals focus when a menu is open.
* In µTorrent, the names of the files in the Torrent Contents list are now reported.
* In Mozilla applications, focus is now correctly detected when it lands on an empty table or tree.
* In Mozilla applications, "not checked" is now correctly reported for checkable controls such as checkable table cells. (#571)
* In Mozilla applications, the text of correctly implemented ARIA dialogs is no longer ignored and will now be reported when the dialog appears. (#630)
* in Internet Explorer and other MSHTML controls, the ARIA level attribute is now  honoured correctly.
* In Internet Explorer and other MSHTML controls, the ARIA role is now chosen over other type information to give a much more correct and predictable ARIA experience.
* Stopped a rare crash in Internet Explorer when navigating through frames or iFrames.
* In Microsoft Word documents, right-to-left lines (such as Arabic text) can be read again. (#627)
* Greatly reduced lag when large amounts of text are displayed in a Windows command console on 64-bit systems. (#622)
* If Skype is already started when NVDA starts, it is no longer necessary to restart Skype to enable accessibility. This may also be true for other applications which check the system screen reader flag.
* In Microsoft Office applications, NVDA no longer crashes when speak foreground (NVDA+b) is pressed or when navigating some objects on toolbars. (#616)
* Fixed incorrect speaking of numbers containing a 0 after a separator; e.g. 1,023. (#593)
* Adobe Acrobat Pro and Reader 9 no longer crash when closing a file or performing certain other tasks. (#613)
* The selection is now announced when control+a is pressed to select all text in some editable text controls such as in Microsoft Word. (#761)
* In Scintilla controls (e.g. Notepad++), text is no longer incorrectly selected when NVDA moves the caret such as during say all. (#746)
* It is again possible to review the contents of cells in Microsoft Excel with the review cursor.
* NVDA can again read by line in certain problematic textArea fields in Internet Explorer 8. (#467)
* Windows Live Messenger 2009 no longer exits immediately after it is started while NVDA is running. (#677)
* In web browsers, It is no longer necessary to press tab to interact with an embedded object (such as Flash content) after pressing enter on the embedded object or returning from another application. (#775)
* In Scintilla controls (e.g. Notepad++), the beginning of long lines is no longer truncated when it scrolls off the screen. Also, these long lines will be correctly displayed in braille when they are selected.
* In Loudtalks, it is now possible to access the contact list.
* The URL of the document and "MSAAHTML Registered Handler" are no longer sometimes spuriously reported in Internet Explorer and other MSHTML controls. (#811)
* In tree views in the Eclipse IDE, the previously focused item is no longer incorrectly announced when focus moves to a new item.
* NVDA now functions correctly on a system where the current working directory has been removed from the DLL search path (by setting the CWDIllegalInDllSearch registry entry to 0xFFFFFFFF). Note that this is not relevant to most users. (#907)
* When the table navigation commands are used outside of a table in Microsoft Word, "edge of table" is no longer spoken after "not in table". (#921)
* When the table navigation commands cannot move due to being at the edge of a table in Microsoft Word, "edge of table" is now spoken in the configured NVDA language rather than always in English. (#921)
* In Outlook Express, Windows Mail and Windows Live Mail, the state of the checkboxes in message rules lists is now reported. (#576)
* The description of message rules can now be read in Windows Live Mail 2010.

## 2010.1

This release focuses primarily on bug fixes and improvements to the user experience, including some significant stability fixes.

### New Features

* NVDA no longer fails to start on a system with no audio output devices. Obviously, a braille display or the Silence synthesiser in conjunction with the Speech Viewer will need to be used for output in this case. (#425)
* A report landmarks checkbox has been added to the Document Formatting settings dialog which allows you to configure whether NVDA should announce landmarks in web documents. For compatibility with the previous release, the option is on by default.
* If speak command keys is enabled, NVDA will now announce the names of multimedia keys (e.g. play, stop, home page, etc.) on many keyboards when they are pressed. (#472)
* NVDA now announces the word being deleted when pressing control+backspace in controls that support it. (#491)
* Arrow keys can now be used in the Web formator window to navigate and read the text. (#452)
* The entry list in the Microsoft Office Outlook address book is now supported.
* NVDA better supports embedded editable (design mode) documents in Internet Explorer. (#402)
* a new script (nvda+shift+numpadMinus) allows you to move the system focus to the current navigator object.
* New scripts to lock and unlock the left and right mouse buttons. Useful for performing drag and drop operations. shift+numpadDivide to lock/unlock the left, shift+numpadMultiply to lock/unlock the right.
* New braille translation tables: German 8 dot computer braille, German grade 2, Finnish 8 dot computer braille, Chinese (Hong Kong, Cantonese), Chinese (Taiwan, Manderin). (#344, #369, #415, #450)
* It is now possible to disable the creation of the desktop shortcut (and thus the shortcut key) when installing NVDA. (#518)
* NVDA can now use IAccessible2 when present in 64 bit applications. (#479)
* Improved support for live regions in Mozilla applications. (#246)
* The NVDA Controller Client API is now provided to allow applications to control NVDA; e.g. to speak text, silence speech, display a message in Braille, etc.
* Information and error messages are now read in the logon screen in Windows Vista and Windows 7. (#506)
* In Adobe Reader, PDF interactive forms developed with Adobe LiveCycle are now supported. (#475)
* In Miranda IM, NVDA now automatically reads incoming messages in chat windows if reporting of dynamic content changes is enabled. Also, commands have been added to report the three most recent messages (NVDA+control+number). (#546)
* Input text fields are now supported in Adobe Flash content. (#461)

### Changes

* The extremely verbose keyboard help message in the Windows 7 Start menu is no longer reported.
* The Display synth has now been replaced with a new Speech Viewer. To activate it, choose Speech Viewer from the Tools menu. The speech viewer can be used independently of what ever speech synthesizer you are using. (#44)
* Messages on the braille display will automatically be dismissed if the user presses a key that results in a change such as the focus moving. Previously the message would always stay around for its configured time.
* Setting whether braille should be tethered to the focus or the review cursor (NVDA+control+t) can now be also set from the braille settings dialog, and is also now saved in the user's configuration.
* Updated eSpeak speech synthesiser to 1.43.
* Updated liblouis braille translator to 1.8.0.
* In virtual buffers, the reporting of elements when moving by character or word has been greatly improved. Previously, a lot of irrelevant information was reported and the reporting was very different to that when moving by line. (#490)
* The Control key now simply stops speech like other keys, rather than pausing speech. To pause/resume speech, use the shift key.
* Table row and column counts are no longer announced when reporting focus changes, as this announcement is rather verbose and usually not useful.

### Bug Fixes

* NVDA no longer fails to start if UI Automation support appears to be available but fails to initialise for some reason. (#483)
* The entire contents of a table row is no longer sometimes reported when moving focus inside a cell  in Mozilla applications. (#482)
* NVDA no longer lags for a long time when expanding tree view items that contain a very large amount of sub-items.
* When listing SAPI 5 voices, NVDA now tries to detect buggy voices and excludes them from the Voice Settings dialog and synthesiser settings ring. Previously, when there was just one problematic voice, NVDA's SAPI 5 driver would sometimes fail to start.
* Virtual buffers now honour the report object shortcut keys setting found in the Object Presentation dialog. (#486)
* In virtual buffers, row/column coordinates are no longer incorrectly read for row and column headers when reporting of tables is disabled.
* In virtual buffers, row/column coordinates are now correctly read when you leave a table and then re-enter the same table cell without visiting another cell first; e.g. pressing upArrow then downArrow on the first cell of a table. (#378)
* Blank lines in Microsoft Word documents and  Microsoft HTML edit controls are now shown appropriately on braille displays. Previously NVDA was displaying the current sentence on the display, not the current line for these situations. (#420)
* Multiple security fixes when running NVDA at Windows logon and on other secure desktops. (#515)
* The cursor position (caret) is now correctly updated when performing a Say All that goes off the bottom of the screen, in standard Windows edit fields and Microsoft Word documents. (#418)
* In virtual buffers, text is no longer incorrectly included for images inside links and clickables that are marked as being irrelevant to screen readers. (#423)
* Fixes to the laptop keyboard layout. (#517)
* When Braille is tethered to review when you focus on a Dos console window, the review cursor can now properly navigate the text in the console.
* While working with TeamTalk3 or TeamTalk4 Classic, the VU meter progress bar in the main window is no longer announced as it updates. Also, special characters can be read properly in the incoming chat window.
* Items are no longer spoken twice in the Windows 7 Start Menu. (#474)
* Activating same-page links in Firefox 3.6 appropriately moves the cursor in the virtualBuffer to the correct place on the page.
* Fixed the issue where some text was not rendered in Adobe Reader in certain PDF documents.
* NVDA no longer incorrectly speaks certain numbers separated by a dash; e.g. 500-1000. (#547)
* In Windows XP, NVDA no longer causes Internet Explorer to freeze when toggling checkboxes in Windows Update. (#477)
* When using the in-built eSpeak synthesiser, simultaneous speech and beeps no longer intermittently cause freezes on some systems. This was most noticeable, for example, when copying large amounts of data in Windows Explorer.
* NVDA no longer announces that a Firefox document has become busy (e.g. due to an update or refresh) when that document is in the background. This also caused the status bar of the foreground application to be spuriously announced.
* When switching Windows keyboard layouts (with control+shift or alt+shift), the full name of the layout is reported in both speech and braille. Previously it was only reported in speech, and alternative layouts (e.g. Dvorak) were not reported at all.
* If reporting of tables is disabled, table information is no longer announced when the focus changes.
* Certain standard tree view controls in 64 bit applications (e.g. the Contents tree view in Microsoft HTML Help) are now accessible. (#473)
* Fixed some problems with logging of messages containing non-ASCII characters. This could cause spurious errors in some cases on non-English systems. (#581)
* The information in the About NVDA dialog now appears in the user's configured language instead of always appearing in English. (#586)
* Problems are no longer encountered when using the synthesiser settings ring after the voice is changed to one which has less settings than the previous voice.
* In Skype 4.2, contact names are no longer spoken twice in the contact list.
* Fixed some potentially major memory leaks in the GUI and in virtual buffers. (#590, #591)
* Work around a nasty bug in some SAPI 4 synthesisers which was causing frequent errors and crashes in NVDA. (#597)

## 2009.1

Major highlights of this release include support for 64 bit editions of Windows; greatly improved support for Microsoft Internet Explorer and Adobe Reader documents; support for Windows 7; reading of the Windows logon, control+alt+delete and User Account Control (UAC) screens; and the ability to interact with Adobe Flash and Sun Java content on web pages. There have also been several significant stability fixes and improvements to the general user experience.

### New Features

* Official support for 64 bit editions of Windows! (#309)
* Added a synthesizer driver for the Newfon synthesizer. Note that this requires a special version of Newfon. (#206)
* In virtual buffers, focus mode and browse mode can now be reported using sounds instead of speech. This is enabled by default. It can be configured from the Virtual buffers dialog. (#244)
* NVDA no longer cancels speech when volume control keys are pressed on the keyboard, allowing the user to change the volume and listen to actual results immediately. (#287)
* Completely rewritten support for Microsoft Internet Explorer and Adobe Reader documents. This support has been unified with the core support used for Mozilla Gecko, so features such as fast page rendering, extensive quick navigation, links list, text selection, auto focus mode and braille support are now available with these documents.
* Improved support for the date selection control found in the Windows Vista Date / Time properties dialog.
* improved support for the Modern XP/Vista start menu (specifically the all programs, and places menus). Appropriate level information is now announced.
* The amount of text that is announced when moving the mouse is now configurable from the Mouse settings dialog. A choice of paragraph, line, word or character can be made.
* announce spelling errors under the cursor in Microsoft Word.
* support for the Microsoft Word 2007 spell checker. Partial support may be available for prior Microsoft Word versions.
* Better support for Windows Live Mail. Plain text messages can now be read and both the plain text and HTML message composers are useable.
* In Windows Vista, if the user moves to the secure desktop (either because a UAC control dialog appeared, or because control+alt+delete was pressed), NVDA will announce the fact that the user is now on the secure desktop.
* NVDA can announce text under the mouse within dos console windows.
* Support for UI Automation via the UI Automation client API available in Windows 7, as well as fixes to improve the experience of NVDA in Windows 7.
* NVDA can be configured to start automatically after you log on to Windows. The option is in the General Settings dialog.
* NVDA can read secure Windows screens such as the Windows logon, control+alt+delete and User Account Control (UAC) screens in Windows XP and above. Reading of the Windows logon screen can be configured from the General Settings dialog. (#97)
* Added a driver for the Optelec ALVA BC6 series braille displays.
* When browsing web documents, you can now press n and shift+n to skip forward and backward past blocks of links, respectively.
* When browsing web documents, ARIA landmarks are now reported, and you can move forward and backward through them using d and shift+d, respectively. (#192)
* The Links List dialog available when browsing web documents has now become an Elements List dialog which can list links, headings and landmarks. Headings and landmarks are presented hierarchically. (#363)
* The new Elements List dialog contains a "Filter by" field which allows you to filter the list to contain only those items including the text that was typed. (#173)
* Portable versions of NVDA now look in the 'userConfig' directory inside the NVDA directory, for the user's configuration. Like for the installer version, this keeps the user's configuration separate from NVDA itself.
* Custom app modules, braille display drivers and synth drivers can now be stored in the user's configuration  directory. (#337)
* Virtual buffers are now rendered in the background, allowing the user to interact with the system to some extent during the rendering process. The user will be notified that the document is being rendered if it takes longer than a second.
* If NVDA detects that it has frozen for some reason, it will automatically pass all keystrokes through so that the user has a better chance of recovering the system.
* Support for ARIA drag and drop in Mozilla Gecko. (#239)
* The document title and current line or selection is now spoken when you move focus inside a virtual buffer. This makes the behaviour when moving focus into virtual buffers consistent with that for normal document objects. (#210)
* In virtual buffers, you can now interact with embedded objects (such as Adobe Flash and Sun Java content) by pressing enter on the object. If it is accessible, you can then tab around it like any other application. To return focus to the document, press NVDA+space. (#431)
* In virtual buffers, o and shift+o move to the next and previous embedded object, respectively.
* NVDA can now fully access applications running as administrator in Windows Vista and later. You must install an official release of NVDA for this to work. This does not work for portable versions and snapshots. (#397)

### Changes

* NVDA no longer announces "NVDA started" when it starts.
* The startup and exit sounds are now played using NVDA's configured audio output device instead of the Windows default audio output device. (#164)
* Progress bar reporting has been improved. Most notably you can now configure NVDA to announce via both speech and beeps at the same time.
* Some generic roles, such as pane, application and frame, are no longer reported on focus unless the control is unnamed.
* The review copy command (NVDA+f10) copies the text from the start marker up to and including the current review position, rather than excluding the current position. This allows the last character of a line to be copied, which was not previously possible. (#430)
* the navigatorObject_where script (ctrl+NVDA+numpad5) has been removed. This key combination did not work on some keyboards, nore was the script found to be that useful.
* the navigatorObject_currentDimentions script has been remapped to NVDA+numpadDelete. The old key combination did not work on some keyboards. This script also now reports the width and height of the object instead of the right/bottom coordinates.
* Improved performance (especially on netbooks) when many beeps occur in quick succession; e.g. fast mouse movement with audio coordinates enabled. (#396)
* The NVDA error sound is no longer played in release candidates and final releases. Note that errors are still logged.

### Bug Fixes

* When NVDA is run from an 8.3 dos path, but it is installed in the related long path (e.g. progra~1 verses program files) NVDA will correctly  identify that it is an installed copy and properly load the user's settings.
* speaking the title of the current foreground window with nvda+t now works correctly when in menus.
* braille no longer shows useless information in its focus context such as unlabeled panes.
* stop announcing some useless information when the focus changes such as root panes, layered panes and scroll panes in Java or Lotus applications.
* Make the  keyword search field in Windows Help (CHM) viewer much more usable. Due to buggyness in that control, the current keyword could not be read as it would be continually changing.
* report correct page numbers in Microsoft Word if the page numbering has been specifically offset in the document.
* Better support for edit fields found in Microsoft Word dialogs (e.g. the Font dialog). It is now possible  to navigate these controls with the arrow keys.
* better support for Dos consoles. specifically: NVDA can now read the content of particular consoles it always used to think were blank. Pressing control+break no longer terminates NVDA.
* On Windows Vista and above, the NVDA installer now starts NVDA with normal user privileges when requested to run NVDA on the finish screen.
* Backspace is now handled correctly when speaking typed words. (#306)
* Don't incorrectly report "Start menu" for certain context menus in Windows Explorer/the Windows shell. (#257)
* NVDA now correctly handles ARIA labels in Mozilla Gecko when there is no other useful content. (#156)
* NVDA no longer incorrectly enables focus mode automatically for editable text fields which update their value when the focus changes; e.g. http://tigerdirect.com/. (#220)
* NVDA will now attempt to recover from some situations which would previously cause it to freeze completely. It may take up to 10 seconds for NVDA to detect and recover from such a freeze.
* When the NVDA language is set to "User default", use the user's Windows  display language setting instead of the Windows locale setting. (#353)
* NVDA now recognises the existence of controls in AIM 7.
* The pass key through command no longer gets stuck if a key is held down. Previously, NVDA stopped accepting commands if this occurred and had to be restarted. (#413)
* The taskbar is no longer ignored when it receives focus, which often occurs when exiting an application. Previously, NVDA behaved as if the focus had not changed at all.
* When reading text fields in applications which use the Java Access Bridge (including OpenOffice.org), NVDA now functions correctly when reporting of line numbers is enabled.
* The review copy command (NVDA+f10) gracefully handles the case where it is used on a position before the start marker. Previously, this could cause problems such as crashes in Notepad++.
* A certain control character (0x1) no longer causes strange eSpeak behaviour (such as changes in volume and pitch) when it is encountered in text. (#437)
* The report text selection command (NVDA+shift+upArrow) now gracefully reports that there is no selection in objects which do not support text selection.
* Fixed the issue where pressing the enter key on certain Miranda-IM buttons or links was causing NVDA to freeze. (#440)
* The current line or selection is now properly respected when spelling or copying the current navigator object.
* Worked around a Windows bug which was causing garbage to be spoken after the name of link controls in Windows Explorer and Internet Explorer dialogs. (#451)
* Fixed a problem with the report date and time command (NVDA+f12). Previously, date reporting was truncated on some systems. (#471)
* Fixed the issue where the system screen reader flag was sometimes inappropriately cleared after interacting with secure Windows screens. This could cause problems in applications which check the screen reader flag, including Skype, Adobe Reader and Jart. (#462)
* In an Internet Explorer 6 combo box, the active item is now reported when it is changed. (#342)

## 0.6p3

### New Features

* As Microsoft Excel's formula bar is inaccessible to NVDA, provide an NVDA specific dialog box for editing when the user presses f2 on a cell.
* Support for formatting in IAccessible2 text controls, including Mozilla applications.
* Spelling errors can now be reported where possible. This is configurable from the Document Formatting preferences dialog.
* NVDA can be configured to beep for either all or only visible progress bars. Alternatively, it can be configured to speak progress bar values every 10%.
* Links can now be identified in richedit controls.
* The mouse can now be moved to the character under the review cursor in most editable text controls. Previously, the mouse could only be moved to the center of the control.
* In virtual buffers, the review cursor now reviews the text of the buffer, rather than just the internal text of the navigator object (which is often not useful to the user). This means that you can navigate the virtual buffer hierarchically using object navigation and the review cursor will move to that point in the buffer.
* Handle some additional states on Java controls.
* If the title command (NVDA+t) is pressed twice, it spells the title. If pressed thrice, it is copied to the clipboard.
* Keyboard help now reads the names of modifier keys when pressed alone.
* Key names announced by keyboard help are now translatable.
* Added support for the recognized text field in SiRecognizer. (#198)
* Support for braille displays!
* Added a command (NVDA+c) to report the text on the Windows clipboard. (#193)
* In virtualBuffers, if NVDA automatically switches to focus mode, you can use the escape key to switch back to browse mode. NVDA+space can still also be used.
* In virtual buffers, when the focus changes or the caret is moved, NVDA can automatically switch to focus mode or browse mode as appropriate for the control under the caret. This is configured from the Virtual Buffers dialog. (#157)
* Rewritten SAPI4 synthesizer driver which replaces the sapi4serotek and sapi4activeVoice drivers and should fix the problems encountered with these drivers.
* The NVDA application now includes a manifest, which means that it no longer runs in compatibility mode in Windows Vista.
* The configuration file and speech dictionaries are now saved in the user's application data directory if NVDA was installed using the installer. This is necessary for Windows Vista and also allows multiple users to have individual NVDA configurations.
* Added support for position information for IAccessible2 controls.
* Added the ability to copy text to the clipboard using the review cursor. NVDA+f9 sets the start marker to the current position of the review cursor. NVDA+f10 retrieves the text between the start marker and the current position of the review cursor and copies it to the clipboard. (#240)
* Added support for some edit controls in pinacle tv software.
* When announcing selected text for long selections (512 characters or more), NVDA now speaks the number of selected characters, rather than speaking the entire selection. (#249)

### Changes

* If the audio output device is set to use the Windows default device (Microsoft Sound Mapper), NVDA will now switch to the new default device for eSpeak and tones when the default device changes. For example, NVDA will switch to a USB audio device if it automatically becomes the default device when it is connected.
* Improve performance of eSpeak with some Windows Vista audio drivers.
* reporting of links, headings, tables, lists and block quotes can now be configured from the Document Formatting settings dialog. Previously to configure these settings for virtual buffers, the virtual buffer settings dialog would have been used. Now all documents share this configuration.
* Rate is now the default setting in the speech synthesizer settings ring.
* Improve the loading and unloading of appModules.
* The title command (NVDA+t) now only reports the title instead of the entire object. If the foreground object has no name, the application's process name is used.
* Instead of virtual buffer pass through on and off, NVDA now reports focus mode (pass through on) and browse mode (pass through off).
* Voices are now stored in the configuration file by ID instead of by index. This makes voice settings more reliable across systems and configuration changes. The voice setting will not be preserved in old configurations and an error may be logged the first time a synthesizer is used. (#19)
* The level of a tree view item is now announced first if it has changed from the previously focused item for all tree views. Previously, this was only occurring for native Windows (SysTreeView32) tree views.

### Bug Fixes

* The last chunk of audio is no longer cut off when using NVDA with eSpeak on a remote desktop server.
* Fix problems with saving speech dictionaries for certain voices.
* Eliminate the lag when moving by units other than character (word, line, etc.) towards the bottom of large plain text documents in Mozilla Gecko virtual buffers. (#155)
* If speak typed words is enabled, announce the word when enter is pressed.
* Fix some character set issues in richedit documents.
* The NVDA log viewer now uses richedit instead of just edit to display the log. This improves reading by word with NVDA.
* Fix some issues related to embedded objects in richedit controls.
* NVDA now reads page numbers in Microsoft Word. (#120)
* Fix the issue where tabbing to a checked checkbox in a Mozilla Gecko virtual buffer and pressing space would not announce that the checkbox was being unchecked.
* Correctly report partially checked checkboxes in Mozilla applications.
* If the text selection expands or shrinks in both directions, read the selection as one chunk instead of two.
* When reading with the mouse, text in Mozilla Gecko edit fields should now be read.
* Say all should no longer cause certain SAPI5 synthesizers to crash.
* Fixed an issue which meant that text selection changes were not being read in Windows standard edit controls before the first focus change after NVDA was started.
* Fix mouse tracking in Java objects. (#185)
* NVDA no longer reports Java tree view items with no children as being collapsed.
* Announce the object with focus when a Java window comes to the foreground. Previously, only the top-level Java object was announced.
* The eSpeak synthesizer driver no longer stops speaking completely after a single error.
* Fix the issue whereby updated voice parameters (rate, pitch, etc.) were not saved when the voice was changed from the synthesizer settings ring.
* Improved the speaking of typed characters and words.
* Some new text that was previously not spoken in text console applications (such as some text adventure games) is now spoken.
* NVDA now ignores focus changes in background windows. Previously, a background focus change could be treated as if the real focus changed.
* Improved the detection of the focus when leaving context menus. Previously, NVDA often didn't react at all when leaving a context menu.
* NVDA now announces when the context menu is activated in the Start menu.
* The classic Start menu is now announced as Start menu instead of Application menu.
* Improved the reading of alerts such as those encountered in Mozilla Firefox. The text should no longer be read multiple times and other extraneous information will no longer be read. (#248)
* The text of focusable, read-only edit fields will no longer be included when retrieving the text of dialogs. This fixes, for example, the automatic reading of the entire license agreement in installers.
* NVDA no longer announces the unselection of text when leaving some edit controls (example: Internet Explorer address bar, Thunderbird 3 email address fields).
* When opening plain text emails in Outlook Express and Windows Mail, focus is correctly placed in the message ready for the user to read it. Previously the user had to press tab or click on the message in order to use cursor keys to read it.
* Fixed several major issues with the "Speak command keys" functionality.
* NVDA can now read text past 65535 characters in standard edit controls (e.g. a large file in Notepad).
* Improved line reading in MSHTML edit fields (Outlook Express editable messages and Internet Explorer text input fields).
* NVDA no longer sometimes freezes completely when editing text in OpenOffice. (#148, #180)

## 0.6p2

* Improved the default ESpeak voice in NVDA
* Added a laptop keyboard layout. Keyboard layouts can be configured from NVDA's  Keyboard settings dialog. (#60)
* Support for grouping items in SysListView32 controls, mainly found in Windows Vista. (#27)
* Report the checked state of treeview items in SysTreeview32 controls.
* Added shortcut keys for many of NVDA's configuration dialogs
* Support for IAccessible2 enabled applications such as Mozilla Firefox when running NVDA from portable media, with out having to register any special Dll files
* Fix a crash with the virtualBuffers Links List in Gecko applications. (#48)
* NVDA should no longer crash Mozilla Gecko applications such as Firefox and Thunderbird if NVDA is running with higher privilages than the Mozilla Gecko application. E.g. NVDA is  running as Administrator.
* Speech dictionaries (previously User dictionaries) now can be either case sensitive or insensitive, and the patterns can optionally be regular expressions. (#39)
* Whether or not NVDA uses a 'screen layout' mode for virtual buffer documents can now be configured from a settings dialog
* No longer report anchor tags with no href in Gecko documents as links. (#47)
* The NVDA find command now remembers what you last searched for, across all applications. (#53)
* Fix issues where the checked state would not be announced for some checkboxes and radio buttons in virtualBuffers
* VirtualBuffer pass-through mode is now specific to each document, rather than NVDA globally. (#33)
* Fixed some sluggishness with focus changes and incorrect speech interuption which sometimes occured when using NVDA on a system that had been on standby or was rather slow
* Improve support for combo boxes in Mozilla Firefox. Specifically when arrowing around them text isn't repeated, and when jumping out of them, ancestor controls are not announced unnecessarily. Also virtualBuffer commands now work when focused on one  when you are in a virtualBuffer.
* Improve accuracy of finding the statusbar in many applications. (#8)
* Added the NVDA interactive Python console tool, to enable developers to look at and manipulate NVDA's internals as it is running
* sayAll, reportSelection and reportCurrentLine scripts now work properly when in virtualBuffer pass-through mode. (#52)
* The increase rate and decrease rate scripts have been removed. Users should use the synth settings ring scripts (control+nvda+arrows) or the Voice settings dialog
* Improve the range and scale of the progress bar beeps
* Added more quick keys to the new virtualBuffers:  l for list, i for list item, e for edit field, b for button, x for checkbox, r for radio button, g for graphic, q for blockquote, c for combo box, 1 through 6 for respective heading levels, s for separator, m for frame. (#67, #102, #108)
* Canceling the loading of a new document in Mozilla Firefox now allows the user to keep using the old document's virtualBuffer if the old document hadn't yet really been destroyed. (#63)
* Navigating by words in virtualBuffers is now more accurate as  words do not accidentally contain text from more than one field. (#70)
* Improved accuracy of focus tracking and focus updating when navigating in Mozilla Gecko virtualBuffers.
* Added a findPrevious script (shift+NVDA+f3) for use in new virtualBuffers
* Improved sluggishness in Mozilla Gecko dialogs (in Firefox and Thunderbird). (#66)
* Add the ability to view the current log file for NVDA. it can be found in the NVDA menu -&gt; Tools
* Scripts such as say time and date now take the current language in to account; punctuation and ordering of words now reflects the language
* The language combo box in NVDA's General settings dialog now shows full language names for ease of use
* When reviewing text in the current navigator object, the text is always up to date if it changes dynamically. E.g. reviewing the text of a list item in Task Manager. (#15)
* When moving with the mouse, the current paragraph of text under the mouse is now announced, rather than either all the text in that particular object or just the current word. Also audio coordinates, and announcement of object roles is optional, they are turned off by default
* Support for reading text with the mouse in Microsoft Word
* Fixed bug where leaving the menu bar in applications such as Wordpad would cause text selection to not be announced anymore
* In Winamp, the title of the track is no longer announced again and again when switching tracks, or pausing/resuming/stopping playback.
* In Winamp,  Added ability to announce state of the shuffle and repeat controls as they are switched. Works in the main window and in the playlist editor
* Improve the ability to activate particular fields in Mozilla Gecko virtualBuffers. May include clickable graphics, links containing paragraphs, and other weird structures
* Fixed an initial lag when opening NVDA dialogs on some systems. (#65)
* Add specific support for the Total Commander application
* Fix bug in the sapi4serotek driver where the pitch could get locked at a particular value, i.e. stays high after reading a capital letter. (#89)
* Announce clickable text and other fields as clickable in Mozilla Gecko VirtualBuffers. e.g.  a field which has an onclick HTML attribute. (#91)
* When moving around Mozilla Gecko virtualBuffers, scroll the current field in to view -- useful so sighted peers have an idea of where the user is up to in the document. (#57)
* Add basic support for ARIA live region show events in IAccessible2 enabled applications. Useful in the Chatzilla IRC application, new messages will now be read automatically
* Some slight improvements to help use ARIA enabled web applications,  e.g. Google Docs
* Stop adding extra blank lines to text when copying it from a virtualBuffer
* Stop the space key from activating a link in the Links List. Now it can be used like other letters in order to  start typing the name of a particular link you wish to go to
* The moveMouseToNavigator script (NVDA+numpadSlash) now moves the mouse to the centre of the navigator object, rather than the top left
* Added scripts to click the left and right mouse buttons (numpadSlash and numpadStar respectively)
* Improve access to the Windows System Tray. Focus hopefully should no longer seem to keep jumping back to one particular item. Reminder: to get to the System Tray use the Windows command WindowsKey+b. (#10)
* Improve performance and stop announcing extra text when holding down a cursor key in an edit field and it hits the end
* Stop the ability for NVDA to make the user wait while particular messages are spoken. Fixes some crashes/freezes with particular speech synthesizers. (#117)
* Added support for the Audiologic Tts3 speech synthesizer, contribution by Gianluca Casalino. (#105)
* Possibly improve performance when navigating around documents in Microsoft Word
* Improved accuracy when reading text of alerts in Mozilla Gecko applications
* Stop possible crashes when trying to save configuration on non-English versions of Windows. (#114)
* Add an NVDA welcome dialog. This dialog is designed to provide essential information for new users and allows CapsLock to be configured as an NVDA modifier key. This dialog will be displayed when NVDA is started by default until it is disabled.
* Fix basic support for Adobe Reader so it is possible to read documents  in  versions 8 and 9
* Fix some errors that may have occured when holding down keys before NVDA is properly initialized
* If the user has configured NVDA to save configuration on exit, make sure the configuration is properly saved when shutting down or logging out of  Windows.
* Added an NVDA logo sound to the beginning of the installer, contributed by Victer Tsaran
* NVDA, both running in the installer and otherwise, should properly clean up its system tray icon when it exits
* Labels for standard controls in NVDA's dialogs (such as Ok and cancel buttons) should now show in the language NVDA is set to, rather than just staying in English.
* NVDA's icon should now be  used for  the NVDA shortcuts in the start menu and on the Desktop, rather than a default application icon.
* Read cells in MS Excel when moving with tab and shift+tab. (#146)
* Fix some double speaking in particular lists in Skype.
* Improved caret tracking in IAccessible2 and Java applications; e.g. in Open Office and Lotus Symphony, NVDA properly waits for the caret to move in documents rather than accidentally reading the wrong word or line at the end of some paragraphs. (#119)
* Support for AkelEdit controls found in Akelpad 4.0
* NVDA no longer locks up in Lotus Synphony when moving from the document to the menu bar.
* NVDA no longer freezes in the Windows XP Add/Remove programs applet when launching an uninstaller. (#30)
* NVDA no longer freezes when opening Spybot Search and Destroy

## 0.6p1

### Access to web content with new in-process virtualBuffers (so far for Mozilla Gecko applications including Firefox3 and Thunderbird3)

* Load times have been improved almost by a factor of thirty (you no longer have to wait at all for most web pages to load in to the buffer)
* Added a links list (NVDA+f7)
* Improved the find dialog (control+nvda+f) so that it performs a case-insencitive search, plus fixed a few focus issues with that dialog box.
* It is now possible to select and copy text in the new virtualBuffers
* By default the new virtualBuffers represent the document in a screen layout (links and controls are not on separate lines unless they really are visually). You can toggle this feature with NVDA+v.
* It is possible to move by paragraph with control+upArrow and control+downArrow.
* Improved support for dynamic content
* Improved over all accuracy of reading lines and fields when arrowing up and down.

### Internationalization

* It is now possible to type accented characters that rely on a "dead character", while NVDA is running.
* NVDA now announces when the keyboard layout is changed (when pressing alt+shift).
* The announce date and time feature now takes the system's current regional and language options in to account.
* added czech translation (by Tomas Valusek with help from Jaromir Vit)
* added vietnamese translation by Dang Hoai Phuc
* Added Africaans (af_ZA) translation, by Willem van der Walt.
* Added russian translation by Dmitry Kaslin
* Added polish translation by DOROTA CZAJKA and friends.
* Added Japanese translation by Katsutoshi Tsuji.
* added Thai translation by Amorn Kiattikhunrat
* added croatian translation by Mario Percinic and Hrvoje Katic
* Added galician translation by Juan C. buno
* added ukrainian translation by Aleksey Sadovoy

### Speech

* NVDA now comes packaged with eSpeak 1.33 which contains many improvements, among those are improved languages, named variants, ability to speak faster.
* The voice settings dialog now allows you to change the variant of a synthesizer if it supports one. Variant is usually a slight variation on the current voice. (eSpeak supports variants).
* Added the ability to change the inflection of a voice in the voice settings dialog if the current synthesizer supports this. (eSpeak supports inflection).
* Added the ability to turn off speaking of object position information(e.g. 1 of 4). This option can be found in the Object presentation settings dialog.
* NVDA can now beep when speaking a capital letter. This can be turned on and off with a check box in the voice settings dialog. Also added a raise pitch for capitals check box to configure whether NVDA should actually do its normal pitch raise for capitals. So now you can have either raise pitch, say cap, or beep, for capitals.
* Added the ability to pause speech in NVDA (like found in Voice Over for the Mac). When NVDA is speaking something, you can press the control or shift keys to silence speech just like normal, but if you then tap the shift key again (as long as you havn't pressed any other keys) speech will continue from exactly where it left off.
* Added a virtual synthDriver which outputs text to a window instead of speaking via a speech synthesiser. This should be more pleasant for sighted developers who are not used to speech synthesis but want to know what is spoken by NVDA. There are probably still some bugs, so feedback is most definitely welcome.
* NVDA no longer by default speaks punctuation, you can enable speaking of punctuation with NVDA+p.
* eSpeak by default now speaks quite a bit slower, which should make it easier for people who are using eSpeak for the first time, when installing or starting to use NVDA.
* Added user dictionaries to NVDA. These allow you to make NVDA speak certain text differently. There are three dictionaries: default, voice, and temporary. Entries you add to the default dictionary will happen all the time in NVDA. Voice dictionaries are specific to the current synthesizer and voice you currently have set. And temporary dictionary is  for those times you quickly want to set a rule while you are doing a particular task, but you don't want it to be perminant (it will disappear if you close NVDA). For now the rules are regular expressions, not just normal text.
* Synthesizers can now use any audio output device on your system, by setting the output device combo box in the Synthesizer dialog before selecting the synthesizer you want.

### Performance

* NVDA no longer takes up a huge amount of system memory , when editing messages in mshtml edit controls
* Improved performance when reviewing text inside many controls that do not actually have a real cursor. e.g. MSN Messenger history window, treeview items, listview items etc.
* Improved performance in rich edit documents.
* NVDA should no longer slowly creep up in system memory size for no reason
* Fixed bugs when  trying to focus on a dos console window more than three or so times. NVDA did have a tendency to completely crash.

### Key commands

* NVDA+shift+numpad6 and NVDA+shift+numpad4 allow you to navigate to the next or previous object in flow respectively. This means that you can navigate in an application by only using these two keys with out having to worry about going up by parent, or down to first child as you move around the object hyerarchy. For instance in a web browser such as firefox, you could navigate the document by object, by just using these two keys. If next in flow or previous in flow takes you up and out of an object, or down in to an object, ordered beeps indicate the direction.
* You can now configure voice settings with out opening the voice settings dialog, by using the Synth Settings Ring. The synth settings ring is a group of voice settings you can toggle through by pressing control+NVDA+right and control+NVDA+left. To change a setting use control+NVDA+up and control+NVDA+down.
* Added a command to report the current selection in edit fields (NVDA+shift+upArrow).
* Quite a few NVDA commands that speak text (such as report current line etc) now can spell the text if pressed twice quickly.
* the capslock, numpad insert and extended insert can all be used as the NVDA modifier key. Also if one of these keys is used, pressing the key twice with out pressing any other keys will send the key through to the operating system, just like you'd pressed the key with out NVDA running. To make one of these keys be the NVDA modifier key, check its checkbox in the Keyboard settings dialog (used to be called the keyboard echo dialog).

### Application support

* Improved support for Firefox3 and Thunderbird3 documents. Load times have been improved by almost a factor of thirty, a screen layout is used by default (press nvda+v to toggle between this and no screen layout), a links list (nvda+f7 has been added), the find dialog (control+nvda+f) is now case-insensitive, much better support for dynamic content, selecting and copying text is now possible.
* In the MSN Messenger and Windows Live Messenger history windows, it is now possible to select and copy text.
* Improved support for the audacity application
* Added support for a few edit/text controls in Skype
* Improved support for Miranda instant messenger application
* Fixed some focus issues when opening html and plain text messages in Outlook Express.
* Outlook express newsgroup message fields are now labeled correctly
* NVDA can now read the addresses in the Outlook Express message fields (to/from/cc etc)
* NVDA should be now more accurate at announcing the next message in out look express when deleting a message from the message list.

### APIs and toolkits

* Improved object navigation for MSAA objects. If a window has a system menu, title bar, or scroll bars, you can now navigate to them.
* Added support for the IAccessible2 accessibility API. A part from the ability to announce more control types, this also allows NVDA to access the cursor in applications such as Firefox 3 and Thunderbird 3, allowing you to navigate, select or edit text.
* Added support for Scintilla edit controls (such controls can be found in Notepad++ or Tortoise SVN).
* Added support for Java applications (via the Java Access Bridge). This can provide basic support for Open Office (if Java is enabled), and any other stand-alone Java application. Note that java applets with in a web browser may not work yet.

### Mouse

* Improved support for reading what is under the mouse pointer as it moves. It is now much faster, and it also now has the ability in some controls such as standard edit fields, Java and IAccessible2 controls, to read the current word, not just the current object. This may be of some used to vision impared people who just want to read a specific bit of text with the mouse.
* Added a new config option, found in the mouse settings dialog. Play audio when mouse moves, when checked, plays a 40 ms beep each time the mouse moves, with its pitch (between 220 and 1760 hz) representing the y axis, and left/right volume, representing the x axis. This enables a blind person to get a rough idea of where the mouse is on the screen as its being moved. This feature also depends on reportObjectUnderMouse also being turned on. So this means that if you quickly need to disable both beeps and announcing of objects, then just press NVDA+m. The beeps are also louder or softer depending on how bright the screen is at that point.

### Object presentation and interaction

* Improved support for most common treeview controls. NVDA now tells you how many items are in the branch when you expand it. It also announces the level when moving in and out of branches. And, it announces the current item number and number of items, according to the current branch, not the entire treeview.
* Improved what is announced when focus changes as you move around applications or the operating system. Now instead of just hearing the control you land on, you hear information about any controls this control is positioned inside of. For instance if you tab and land on a button inside a groupbox, the groupbox will also get announced.
* NVDA now tries to speak the message inside many dialog boxes as they appear. This is accurate most of the time, though there are still many dialogs that arn't as good as they could be.
* Added a report object descriptions checkbox to the object presentation settings dialog. Power users may wish to sometimes uncheck this to stop NVDA announcing a lot of extra descriptions on particular controls,  such as in Java applications.
* NVDA automatically announces selected text in edit controls when focus moves to them. If there isn't any selected text, then it just announces the current line like usual.
* NVDA is a lot more careful now when it plays beeps to indicate progress bar changes in applications. It no longer goes crazy in Eclipse applications such as Lotus Notes/Symphony, and Accessibility Probe.

### User Interface

* Removed the NVDA interface window, and replaced it with a simple NVDA popup menu.
* NVDA's user interface settings dialog is now called General Settings. It also contains an extra setting: a combo box to set the log level, for what messages should go to NVDA's log file. Note that NVDA's log file is now called nvda.log not debug.log.
* Removed the report object group names checkBox from the object presentation settings dialog, reporting of group names now is handled differently.

## 0.5

* NVDA now has a built-in synthesizer called eSpeak, developed by Jonathan Duddington.It is very responsive and lite-weight, and has support for many different languages. Sapi synthesizers can still be used, but eSpeak will be used by default.
 * eSpeak does not depend on any special software to be installed, so it can be used with NVDA on any computer, on a USB thumb drive, or anywhere.
 * For more info on eSpeak, or to find other versions, go to http://espeak.sourceforge.net/.
* Fix bug where the wrong character was being announced when pressing delete in Internet Explorer / Outlook Express editable panes.
* Added support for more edit fields in Skype.
* VirtualBuffers only get loaded when focus is on the window that needs to be loaded. This fixes some problems when the preview pane is turned on in Outlook Express.
* Added commandline arguments to NVDA:
 * -m, --minimal: do not play startup/exit sounds and do not show the interface on startup if set to do so.
 * -q, --quit: quit any other already running instance of NVDA and then exit
 * -s, --stderr-file fileName: specify where NVDA should place uncaught errors and exceptions
 * -d, --debug-file fileName: specify where NVDA should place debug messages
 * -c, --config-file: specify an alternative configuration file
 * -h, -help: show a help message listing commandline arguments
* Fixed bug where punctuation symbols would not be translated to the appropriate language, when using a language other than english, and when speak typed characters was turned on.
* Added Slovak language files thanks to Peter Vagner
* Added a Virtual Buffer settings dialog and a Document Formatting settings dialog, from Peter Vagner.
* Added French translation thanks to Michel Such
* Added a script to toggle beeping of progress bars on and off (insert+u). Contributed by Peter Vagner.
* Made more messages in NVDA be translatable for other languages. This includes script descriptions when in keyboard help.
* Added a find dialog to the virtualBuffers (internet Explorer and Firefox). Pressing control+f when on a page brings up a dialog in which you can type some text to find. Pressing enter will then search for this text and place the virtualBuffer cursor on this line. Pressing f3 will also search for the next occurance of the text.
* When speak typed characters is turned on, more characters should be now spoken. Technically, now ascii characters from 32 to 255 can now be spoken.
* Renamed some control types for better readability. Editable text is now edit, outline is now tree view and push button is now button.
* When arrowing around list items in a list, or tree view items in a tree view, the control type (list item, tree view item) is no longer spoken, to speed up navigation.
* Has Popup (to indicate that a menu has a submenu) is now spoken as submenu.
* Where some language use control and alt (or altGR) to enter a special character, NVDA now will speak these characters when speak typed characters is on.
* Fixed some problems with reviewing static text controls.
* Added Translation for Traditional Chinese, thanks to Coscell Kao.
* Re-structured an important part of the NVDA code, which should now fix many issues with NVDA's user interface (including settings dialogs).
* Added Sapi4 support to NVDA. Currently there are two sapi4 drivers, one based on code contributed by Serotek Corporation, and one using the ActiveVoice.ActiveVoice com Interface. Both these drivers have issues, see which one works best for you.
* Now when trying to run a new copy of NVDA while an older copy is still running will cause the new copy to just exit. This fixes a major problem where running multiple copies of NVDA makes your system very unusable.
* Renamed the title of the NVDA user interface from NVDA Interface to NVDA.
* Fixed a bug in Outlook Express where pressing backspace at the start of an editable message would cause an error.
* Added patch from Rui Batista that adds a script to report the current battery status on laptops (insert+shift+b).
* Added a synth driver called Silence. This is a synth driver that does not speak anything, allowing NVDA to stay completely silent at all times. Eventually this could be used along with Braille support, when we have it.
* Added capitalPitchChange setting for synthesizers thanks to J.J. Meddaugh
* Added patch from J.J. Meddaugh that makes the toggle report objects under mouse script more like the other toggle scripts (saying on/off rather than changing the whole statement).
* Added spanish translation (es) contributed by Juan C. buo.
* Added Hungarian language file from Tamas Gczy.
* Added Portuguese language file from Rui Batista.
* Changing the voice in the voice settings dialog now sets the rate, pitch and volume sliders to the new values according to the synthesizer, rather than forcing the synthesizer to be set to the old values. This fixes issues where a synth like eloquence or viavoice seems to speek at a much faster rate than all other synths.
* Fixed a bug where either speech would stop, or NVDA would entirely crash, when in a Dos console window.
* If support for a particular language exists, NVDA now automatically can show its interface and speak its messages in the language Windows is set to. A particular language can still be chosen manualy from the user interface settings dialog as well.
* Added script 'toggleReportDynamicContentChanges' (insert+5). This toggles whether new text, or other dynamic changes should be automatically announced. So far this only works in Dos Console Windows.
* Added script 'toggleCaretMovesReviewCursor' (insert+6). This toggles whether the review cursor should be automatically repositioned when the system caret moves. This is useful in Dos console windows when trying to read information as the screen is updating.
* Added script 'toggleFocusMovesNavigatorObject' (insert+7). This toggles whether the navigator object is repositioned on the object with focus as it changes.
* Added some documentation translated in to various languages. So far there is French, Spannish and Finish.
* Removed some developer documentation from the binary distribution of NVDA, it is only now in the source version.
* Fixed a possible bug in Windows Live Messanger and MSN Messenger where arrowing up and down the contact list would cause errors.
* New messages are now automatically spoken when in a conversation using Windows Live Messenger. (only works for English versions so far)
* The history window in a Windows Live Messenger conversation can now be read by using the arrow keys. (Only works for English versions so far)
* Added script 'passNextKeyThrough' (insert+f2). Press this key, and then the next key pressed will be passed straight through to Windows. This is useful if you have to press a certain key in an application but NVDA uses that key for something else.
* NVDA no longer freezes up for more than a minute when opening very large documents in MS Word.
* Fixed a bug where moving out of a table in MS Word, and then moving back in, caused the current row/column numbers not to be spoken if moving back in to exactly the same cell.
* When starting NVDA with a synthesizer that doesn't exist, or is not working, the sapi5 synth will try and be loaded in stead, or if sapi5 isn't working, then speech will be set to silence.
* Increasing and decreasing rate scripts can no longer take the rate above 100 or below 0.
* If there is an error with a language when choosing it in the User Interface Settings dialog, a message box will alert the user to the fact.
* NVDA now asks if it should save configuration and restart if the user has just changed the language in the User Interface Settings Dialog. NVDA must be restarted for the language change to fully take effect.
* If a synthesizer can not be loaded, when choosing it from the synthesizer dialog, a message box alerts the user to the fact.
* When loading a synthesizer for the first time, NVDA lets the synthesizer choose the most suitable voice, rate and pitch parameters, rather than forcing it to defaults it thinks are ok. This fixes a problem where Eloquence and Viavoice sapi4 synths start speaking way too fast for the first time.
