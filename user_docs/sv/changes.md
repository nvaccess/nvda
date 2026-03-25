# Vad är nytt i NVDA

## 2026.2

### Viktiga noteringar

### Nya funktioner

* Efter installation eller uppdatering av NVDA visas nu en dialogruta med alternativ för att starta om Windows, starta den installerade kopian eller avsluta installationsprogrammet. (#19268, #19718, @kefaslungu)
* NVDA innehåller nu en inbyggd förstoring som låter dig zooma in och förstora delar av skärmen. (#19228, @Boumtchack)
  * Förstoringen stöder olika zoomnivåer, färgfilter (normal, gråskala, inverterad) och olika fokusföljningslägen.
  * Färgfilter kan hjälpa användare med synnedsättningar eller ljuskänslighet genom att invertera eller desaturera skärmfärger.
  * Ett spotlight-läge är tillgängligt för presentationer eller fokuserade läsuppgifter.
  * Alla förstoringseinställningar kan konfigureras i en ny "Förstoring"-panel i NVDA:s inställningar.
  * Förstoringen kan inte användas samtidigt med Skärmridå av säkerhetsskäl.
* Ett nytt kommando, tilldelat `NVDA+x`, har introducerats för att upprepa den senaste informationen som NVDA talade; tryck två gånger för att visa det i ett bläddringsbart meddelande. (#625, @CyrilleB79)
* Lagt till ett otilldelat kommando för att växla tangentbordslayout. (#19211, @CyrilleB79)
* Lagt till ett otilldelat snabbnavigationskommando för att hoppa till nästa/föregående skjutreglage i bläddringsläge. (#17005, @hdzrvcc0X74)
* Lagt till stöd för anpassade talordlistor. (#19558, #17468, @LeonarddeR)
  * Ordlistor kan tillhandahållas i mappen `speechDicts` i ett tilläggspaket.
  * Ordlistemetadata kan läggas till i en valfri `speechDictionaries`-sektion i tilläggsmanifestet.
  * Se [avsnittet om anpassade talordlistor i utvecklarguiden](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSpeechDictionaries) för mer information.
* Nya typer har lagts till för talordlisteposter, såsom del av ord och början av ord.
Se avsnittet om talordlistor i användarguiden för mer information. (#19506, @LeonarddeR)
* Vid återställning av konfigurationen till fabriksinställningar från NVDA-menyn visas nu efteråt en dialogruta med en ångra-knapp för att återställa den tidigare konfigurationen.
Tangentbordsgenvägen med tre tryckningar (`NVDA+ctrl+r`) påverkas inte, eftersom den är avsedd för återställningsscenarier. (#19575, @bramd)
* Lagt till ett otilldelat kommando för att rapportera aktuell status för Skärmridån. (#19759)
* DotPad punktskriftsdisplayer stöder nu flerknappskombinationsgester. (#19565, @bramd)
  * Du kan nu trycka på flera knappar samtidigt för att skapa anpassade gester (t.ex. `f1+panLeft`).
* En ny röstinställning "Naturlig paus efter skiljetecken" har lagts till för OneCore-röster, vilket låter användare slå på eller av pausering vid skiljetecken. (#11876, @gexgd0419)

### Ändringar

* Uppdaterad Liblouis punktskriftsöversättare till [3.37.0](https://github.com/liblouis/liblouis/releases/tag/v3.37.0). (#19758, @codeofdusk)
  * Lagt till nya italienska och estniska 6-punktstabeller.
* Det är nu möjligt att öppna loggvisaren med `NVDA+f1`, även när loggnivån är inställd på "inaktiverad". (#19318, @CyrilleB79)
* Förbättrad sökalgoritm för filtrering av tillägg i Tilläggsbutiken. (#19309)
* NVDA kan nu konfigureras för att inte spela felljud, även i testversioner. (#13021, @CyrilleB79)
* NVDA stöder nu Orbit Reader 40 i dess proprietära HID-läge. (#19756, @trypsynth)
* NVDA startar nu i fokusläge som standard när WhatsApp 2.2584.3.0 eller senare används. (#19655, @josephsl)

### Felrättningar

* I Firefox bläddringsläge annonseras nu det tillgängliga namnet på formulärkontroller (som kryssrutor och radioknappar) korrekt när kontrollen har en `aria-label` och ett associerat `<label>`-element som endast innehåller `aria-hidden`-innehåll. (#19409, @bramd)
* Objektet "Växlar om skärmlayouten bevaras vid rendering av dokumentinnehållet" i kategorin "Bläddringsläge" i dialogrutan Inmatningsgester fungerar nu korrekt. (#18378)
* I Microsoft Word med UIA aktiverat annonseras nu sidändringar korrekt när man navigerar tabellrader som sträcker sig över flera sidor. (#19386, @akj)
* Åtgärdat överdriven resursanvändning och flimrande markeringar när Visuell markering används. (#17434, @hwf1324)
* Kommandot `NVDA+k` rapporterar nu korrekt destinationen för länkar som innehåller formaterad text, såsom fet eller kursiv. (#19428, @Cary-rowen)
* Versalindikatorer annonseras nu korrekt vid markering av enskilda tecken. (#19505, @cary-rowen)
* Konfigurationsprofilutlösare aktiveras nu när Tilläggsbutiken är öppen. (#19583, @bramd)

## 2026.1

Den här versionen innehåller inbyggt stöd för läsning av matematiskt innehåll med MathCAT.

Det har gjorts flera förbättringar av tal.
Stavfel kan nu rapporteras med ett ljud istället för tal vid läsning.
Du kan nu konfigurera NVDA att automatiskt säga allt efter framgångsrik igenkänning av innehåll, till exempel med Windows OCR.
NVDA rapporterar inte längre att språket som läses inte stöds när synthesizern stöder språket men inte den specifika dialekten.
NVDA stöder nu 64-bitars SAPI 5-röster.

Punktskriftsstödet har också förbättrats.
Det fortsätter nu att fungera vid växling till en säker skärm, som inloggningsskärmen eller Användarkontokontroll-dialogen.
NVDA-meddelanden från den lokala datorn visas nu i punktskrift vid styrning av en dator via fjärråtkomst.
Stavfel och antalet objekt i en lista i bläddringsläge kan nu visas i punktskrift.
Andra punktskriftsfelrättningar, inklusive i Microsoft Outlook och LibreOffice Writer, har också lagts till.

I bläddringsläge i webbläsare behandlar NVDA inte längre kontroller med 0 bredd eller höjd som osynliga.
Detta kan göra det möjligt att komma åt tidigare otillgängligt "endast skärmläsare"-innehåll på vissa webbplatser.
Felformaterade länkar förhindrar inte längre NVDA från att läsa innehåll i Google Chrome och andra Chromium-baserade webbläsare.
Bläddringslägets markering visas nu på innehållsigenkänningsresultat, till exempel vid användning av Windows OCR.
I Microsoft Word har otilldelade snabbnavigationskommandon för att hoppa till referenser lagts till.
De visas nu också i elementlistan.

Det är nu möjligt att visa virusgenomsökningsresultat för ett tillägg från Tilläggsbutiken.
För tillägg som innehåller en, kan du också visa ett tilläggs ändringslogg.
Tillförlitligheten för bakgrundstilläggsuppdateringar har förbättrats.

En ny kategori "Integritet och säkerhet" har lagts till i NVDA:s inställningsdialog.
Inställningarna "Loggnivå" och "Tillåt NV Access att samla NVDA-användningsstatistik" har flyttats hit från kategorin "Allmänt".
Inställningarna för Skärmridå har också flyttats hit från kategorin "Syn".
Dessutom är Skärmridåns inställningar nu oberoende av konfigurationsprofiler.

NVDA-gränssnittet är nu översatt till kambodjanska.
Liblouis, Unicode CLDR och eSpeak NG har uppdaterats.
Lagt till tabeller för engelsk grad 3, japanska (Rokuten Kanji) och makedonsk oförkortad punktskrift.
Förbättrat de biblisk-hebreiska, unified english braille, grekisk internationell, ungerska, norska, portugisiska 8-punkts och slovakiska punktskriftstabellerna.
Emoji-lokaliseringar för luxemburgiska har lagts till.

Det har också gjorts många andra felrättningar och förbättringar.

### Viktiga noteringar

* Den här versionen bryter kompatibiliteten med befintliga tillägg.
* Windows 8.1 stöds inte längre.
Windows 10 är den lägsta Windows-version som stöds.
Vi rekommenderar att uppdatera till Windows 11, eller när det inte är möjligt, till den senaste Windows 10-versionen (22H2).
* 32-bitars Windows stöds inte längre.
Windows 10 på ARM stöds inte heller längre.
* Wiris MathPlayer stöds inte längre.

## 2014.3

*[Tidigare versioner skulle översättas här]*