# Was ist neu in NVDA


## 2024.2

Es gibt eine neue Funktion namens Sound-Teilung.
Dies ermöglicht die Aufteilung von NVDA-Sounds auf einen Kanal (z. B. links), während Sounds von allen anderen Anwendungen auf den anderen Kanal (z. B. rechts) ausgegeben werden.

Es gibt neue Befehle zum Ändern des Sprachausgaben-Einstellungsrings, mit denen lassen sich die ersten oder letzten Einstellung sowie die aktuelle Einstellung in größeren Schritten verändern.
Außerdem gibt es neue Schnellnavigationsbefehle, mit denen lassen sich die Tastenbefehle verbinden, um schnell zwischen folgenden Optionen zu wechseln: Absätze, vertikal ausgerichtete Absätze, Texte im gleichen Stil, Texte unterschiedlichem Stil, Menü-Elemente, Umschalter, Fortschrittsbalken, Abbildungen und mathematische Formeln.

Es gibt viele neue Braille-Funktionen und Fehlerbehebungen.
Ein neuer Braille-Modus namens "Sprachausgabenverlauf anzeigen" wurde hinzugefügt.
Wenn dieser aktiviert ist, wird auf der Braillezeile genau das angezeigt, was NVDA spricht.
Unterstützung für die Braillezeilen BrailleEdgeS2 und BrailleEdgeS3 hinzugefügt.
LibLouis wurde aktualisiert, wobei neue detaillierte (mit Großbuchstaben versehene) belarussische und ukrainische Braille-Tabellen, eine laotische Tabelle und eine spanische Tabelle zum Lesen griechischer Texte hinzugefügt wurden.

Die Sprachausgabe eSpeak wurde aktualisiert und um die neue Sprache Tigrinisch erweitert.

Es gibt viele kleinere Fehlerbehebungen für Anwendungen wie Mozilla Thunderbird, Adobe Reader, Web-Browser, Nudi und Geekbench.

### Neue Features

* Neue Tastaturbefehle:
  * Neuer Schnellnavigationsbefehl `P` zum Springen zum nächsten/vorherigen Textabsatz im Lesemodus. (#15998, @mltony)
  * Neue, nicht zugewiesene Schnellnavigationsbefehle, mit denen man zum Nächsten/Vorherigen Element springen kann:
    * Abbildungen (#10826)
    * Vertikal ausgerichteter Absatz (#15999, @mltony)
    * Menü-Element (#16001, @mltony)
    * Umschalter (#16001, @mltony)
    * Fortschrittsbalken (#16001, @mltony)
    * Mathematische Formeln (#16001, @mltony)
    * Text mit gleichem Stil (#16000, @mltony)
    * Text in einem anderen Stil (#16000, @mltony)
  * Es wurden Befehle hinzugefügt, um zum ersten, zum letzten, vorwärts und rückwärts durch den Sprachausgaben-Einstellungsring zu springen. (#13768, #16095, @rmcpantoja)
    * Das Einstellen der ersten/letzten Einstellung im Sprachausgaben-Einstellungsring hat keinen zugewiesenen Tastenbefehl. (#13768)
    * Verändern der aktuellen Einstellung des Sprachausgaben-Einstellungsrings in größeren Schritten (#13768):
      * Desktop: `NVDA+Strg+Seite nach oben` und `NVDA+Strg+Seite nach unten`.
      * Laptop: `NVDA+Strg+Umschalt+Seite nach oben` und `NVDA+Strg+Umschalt+Seite nach unten`.
  * Es wurde ein neuer, nicht zugewiesener Tastenbefehl hinzugefügt, mit der die Anzeige von Abbildungen und Beschriftungen umgeschaltet werden kann. (#10826, #14349)
* Braille:
  * Unterstützungen für die Braillezeilen BrailleEdgeS2 und BrailleEdgeS3 hinzugefügt. (#16033, #16279, @EdKweon)
  * Ein neuer Braille-Modus mit der Bezeichnung "Sprachausgabenverlauf anzeigen" wurde hinzugefügt. (#15898, @Emil-18)
    * Wenn dieser aktiviert ist, wird auf der Braillezeile genau das angezeigt, was NVDA spricht.
    * Er kann mit der Tastenkombination `NVDA+Alt+T` oder über in den Einstellungen in der Kategorie "Braille" umgeschaltet werden.
* Sound-Teilung: (#12985, @mltony)
  * Ermöglicht die Aufteilung von NVDA-Sounds auf einen Kanal (z. B. links), während Sounds von allen anderen Anwendungen auf den anderen Kanal (z. B. rechts) ausgegeben werden.
  * Umgeschaltet mit `NVDA+Alt+S`.
* Die Meldung von Zeilen- und Spaltenüberschriften wird jetzt in inhaltsverarbeitbaren HTML-Elementen unterstützt. (#14113)
* In den Einstellungen für die Dokument-Formatierung wurde eine Option für die Ausgabe zum Deaktivieren von Abbildungen und Beschriftungen hinzugefügt. (#10826, #14349)
* In Windows 11 spricht NVDA Warnungen bei der Spracheingabe und schlägt Aktionen vor, einschließlich des obersten Vorschlags beim Kopieren von Daten wie Telefonnummern in die Zwischenablage (Windows 11 Version 2022 Update und neuer). (#16009, @josephsl)
* NVDA blendet das Audio-Gerät nach Beendigung der Wiedergabe über die Sprachausgabe nicht länger aus, um zu verhindern, dass der Beginn der nächsten Wiedergabe über die Sprachausgabe bei einigen Audio-Geräten wie Bluetooth-Kopfhörern abgeschnitten wird. (#14386, @jcsteh, @mltony)
* Der HP Secure-Browser wird nun unterstützt. (#16377)

### Änderungen

* Store für NVDA-Erweiterungen:
  * Die minimale und die zuletzt getestete NVDA-Version für eine NVDA-Erweiterung werden nun im Bereich "Weitere Details" angezeigt. (#15776, @Nael-Sayegh)
  * Die Aktion "Community-Rezensionen" wird auf allen Registerkarten im Store verfügbar sein. (#16179, @nvdaes)
* Komponenten-Updates:
  * Der Braille-Übersetzer LibLouis wurde auf [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0) aktualisiert. (#16259, @codeofdusk)
    * Neue detaillierte (mit Großbuchstaben gekennzeichnete) belarussische und ukrainische Braille-Tabellen.
    * Neue spanische Tabelle zum Lesen griechischer Texte.
    * Neue Tabelle:  laotische Kurzschrift. (#16470)
  * Die Sprachausgabe eSpeak NG wurde auf 1.52-dev commit `cb62d93fd7` aktualisiert. (#15913)
    * Neue Sprache Tigrinisch hinzugefügt.
* Mehrere Tastenbefehle für Braillezeilen BrailleSense wurden geändert, um Konflikte mit Zeichen der französischen Braille-Tabelle zu vermeiden. (#15306)
  * `Alt+Pfeiltaste nach links` wurde jetzt neu zugeordnet auf `Punkt2+Punkt7+Leertaste`
  * `Alt+Pfeiltaste nach rechts` wurde jetzt neu zugeordnet auf `Punkt5+Punkt7+Leertaste`
  * `Alt+Pfeiltaste nach oben` wurde jetzt neu zugeordnet auf `Punkt2+Punkt3+Punkt7+Leertaste`
  * `Alt+Pfeiltaste nach unten` wurde jetzt neu zugeordnet auf `Punkt5+Punkt6+Punkt7+Leertaste`
* Die in Inhaltsverzeichnissen üblicherweise verwendeten gepunkteten Linien werden bei niedrigen Interpunktionsstufen nicht mehr mitgeteilt. (#15845, @CyrilleB79)

### Fehlerbehebungen

* Windows 11:
  * NVDA teilt wieder Hardware-Tastatur-Eingabevorschläge mit. (#16283, @josephsl)
  * In Version 24H2 (2024 Update und Windows Server 2025) können Maus- und Touch-Interaktion in den Schnelleinstellungen verwendet werden. (#16348, @josephsl)
* Store für NVDA-Erweiterungen:
  * Wenn Sie die Tastenkombination `Strg+Tab` drücken, wird der Fokus korrekt auf den neuen Titel des aktuellen Tabs gesetzt. (#14986, @ABuffEr)
  * Wenn die Cache-Dateien nicht korrekt sind, lässt sich NVDA nicht mehr neu starten. (#16362, @nvdaes)
* Chromium-basierte Browser bei Verwendung mit UIA:
  * Fehler behoben, die zum Einfrieren von NVDA führten. (#16393, #16394)
  * Die Rücktaste funktioniert jetzt in Anmeldefeldern von Google Mail korrekt. (#16395)
* Die Rücktaste funktioniert jetzt korrekt, wenn Nudi 6.1 mit der NVDA-Einstellung "Tasten aus anderen Anwendungen behandeln" verwendet wird. (#15822, @jcsteh)
* Es wurde ein Fehler behoben, bei dem Audio-Koordinaten wiedergegeben wurden, während sich die Anwendung im Ruhezustand befand, wenn "Audio-Koordinaten bei Mausbewegungen wiedergeben" aktiviert war. (#8059, @hwf1324)
* In Adobe Reader ignoriert NVDA nicht mehr den alternativen Text von Formeln in PDFs. (#12715)
* Es wurde ein Fehler behoben, der dazu führte, dass NVDA das Menüband und die Optionen in Geekbench nicht lesen konnte. (#16251, @mzanm)
* Ein seltener Fall wurde behoben, in dem beim Speichern der Konfiguration nicht alle Profile gespeichert werden konnten. (#16343, @CyrilleB79)
* In Firefox und Chromium-basierten Browsern geht NVDA korrekt in den Fokusmodus über, sobald die Eingabetaste innerhalb einer Präsentationsliste (ul / ol) innerhalb eines bearbeitbaren Inhalts gedrückt wird. (#16325)
* Die Änderung des Status der Spalten wird nun korrekt mitgeteilt, wenn Spalten zur Anzeige in der Nachrichtenliste in Mozilla Thunderbird ausgewählt werden. (#16323)
* Der Kommandozeilen-Parameter `--help` bzw. `h` funktioniert wieder korrekt. (#16522, @XLTechie)
* Die Unterstützung in NVDA für die Poedit-Übersetzungssoftware ab Version 3.4 funktioniert korrekt, wenn Sprachen mit 1 oder mehr als 2 Pluralformen (z. B. Chinesisch, Polnisch) übersetzt werden. (#16318)

### Änderungen für Entwickler

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Es wurde ein Dokument hinzugefügt, welches den Prozess der Erstellung von NVDA-Forks auf AppVeyor erklärt. (#16293, @XLTechie)

## 2024.1

Ein neuer Sprachmodus namens "Nur bei Bedarf" wurde hinzugefügt.
Bei aktiviertem Modus spricht NVDA beispielsweise beim Bewegen der Schreibmarke nicht automatisch. NVDA spricht nur noch, wenn ein Befehl ausgelößtwird, dessen Ziel es ist, eine Information wie z. B. das Lesen des Fenstertitels vorzulesen.
In der Kategorie "Sprachausgabe" der NVDA-Einstellungen ist es jetzt möglich, unerwünschte Sprachmodi aus dem Befehl "Sprachmodi wechseln" (`NVDA+S`) auszuschließen.

Ein neuer nativer Auswahlmodus (einzuschalten  mittels `NVDA+Umschalt+F10`) ist jetzt im Lesemodus von NVDA für Mozilla Firefox verfügbar.
Wenn diese Funktion aktiviert ist, wird durch das Auswählen von Text im Lesemodus auch die native Auswahl von Firefox einbezogen.
Das Kopieren von Text mittels `Strg+C` wird direkt an Firefox weitergeleitet, wodurch der formatierte Inhalt und nicht die reine Textdarstellung von NVDA kopiert wird.

Der Store für NVDA-Erweiterungen unterstützt jetzt Massenaktionen, so z. B. das Installieren oder Aktivieren von Erweiterungen durch Auswahl mehrerer Einträge in der Liste.
Es gibt eine neue Aktion zum Öffnen einer Diskussionsseite für die ausgewählte Erweiterung.

Die Optionen zur Auswahl des Audio-Ausgabegeräts und die Lautstärkenreduktion anderer Anwendungen wurden aus dem Dialogfeld "Sprachausgabe auswählen" entfernt.
Diese befinden sich nun in den Audio-Einstellungen, die mit `NVDA+Strg+U` geöffnet werden können.

Die Sprachausgabe eSpeak-NG, der Braille-Übersetzer LibLouis und die Unicode-CLDR wurden aktualisiert.
Neue Brailletabellen sind verfügbar: Thai, Filipinisch und Rumänisch.

Es gibt viele Fehlerbehebungen, vor allem für den Store für NVDA-Erweiterungen, Braille, Libre Office, Microsoft Office und Audio.

### Wichtige Anmerkungen

* Diese Version ist nicht mit vorhandenen NVDA-Erweiterungen kompatibel.
* Windows 7 und Windows 8 werden nicht mehr unterstützt.
Windows 8.1 ist mindestens erforderlich.

### Neue Features

* Store für NVDA-Erweiterungen:
  * Der Store unterstützt jetzt Massenaktionen, so z. B. das Installieren oder Aktivieren von Erweiterungen durch Auswahl mehrerer Einträge in der Liste. (#15350, #15623, @CyrilleB79)
  * Es wurde eine neue Aktion hinzugefügt, mit deren Hilfe Rückmeldungen zur gewählten Erweiterung gegeben oder gelesen werden kann. (#15576, @nvdaes)
* Unterstützung für Bluetooth Low Energy HID-Braillezeilen hinzugefügt. (#15470)
* Ein neuer nativer Auswahlmodus (einzuschalten  via `NVDA+Umschalt+F10`) ist jetzt im Lesemodus von NVDA für Mozilla Firefox verfügbar.
Wenn diese Funktion aktiviert ist, wird durch das Auswählen von Text im Lesemodus auch die native Auswahl von Firefox manipuliert.
Das Kopieren von Text mit "Strg+C" wird direkt an Firefox weitergeleitet, wodurch der formatierte Inhalt und nicht die reine Textdarstellung von NVDA kopiert wird.
Beachten Sie jedoch, dass NVDA in diesem Modus keine Meldung "In die Zwischenablage kopiert" ausgibt, da Firefox die eigentliche Kopie ausführt. (#15830)
* Beim Kopieren von Text in Microsoft Word mit aktiviertem Lesemodus ist jetzt auch die Formatierung enthalten.
Ein Nebeneffekt davon ist, dass NVDA beim Drücken von "Strg+C" im Microsoft Word-/Outlook-Lesemodus nicht mehr die Meldung "In die Zwischenablage kopiert" ausgibt, da die Anwendung nun die Kopie durchführt, nicht NVDA. (#16129)
* Ein neuer Sprachmodus namens "Nur bei Bedarf" wurde hinzugefügt.
Bei aktiviertem Modus spricht NVDA beispielsweise beim Bewegen der Schreibmarke nicht automatisch. NVDA spricht nur noch, wenn ein Befehl ausgelößtwird, dessen Ziel es ist, eine Information wie z. B. das Lesen des Fenstertitels vorzulesen. (#481, @CyrilleB79)
* In der Kategorie "Sprachausgabe" der NVDA-Einstellungen ist es jetzt möglich, unerwünschte Sprachmodi aus dem Befehl "Sprachmodi wechseln" (`NVDA+S`) auszuschließen. (#15806, @lukaszgo1)
  * Wenn Sie derzeit die NVDA-Erweiterung NoBeepsSpeechMode verwenden, sollten Sie es deinstallieren und die Modi "Signaltöne" und "Nur bei Bedarf" in den Einstellungen deaktivieren.

### Änderungen

* NVDA unterstützt Windows 7 und Windows 8 nicht mehr.
Windows 8.1 ist mindestens erforderlich. (#15544)
* Komponenten-Updates:
  * LibLouis Braille-Übersetzer auf [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0) aktualisiert. (#15435, #15876, @codeofdusk)
    * Neue thailändische, rumänische und philippinische Braille-Tabellen hinzugefügt.
  * eSpeak NG wurde auf 1.52-dev commit `530bf0abf` aktualisiert. (#15036)
  * CLDR-Emoji- und Symbolanmerkungen wurden auf Version 44.0 aktualisiert. (#15712, @OzancanKaratas)
  * Java Access Bridge auf 17.0.9+8Zulu aktualisiert (17.46.19). (#15744)
* Tastenkombinationen:
  * Die folgenden Befehle unterstützen jetzt zwei- und dreimaliges Drücken, um die gemeldeten Informationen zu buchstabieren bzw. phonetisch zu buchstabieren: Auswahl vorlesen, Textinhalte der Zwischenablage vorlesen und fokussiertes Objekt vorlesen (#15449, @CyrilleB79)
  * Der Befehl zum Umschalten des Bildschirmvorhangs verfügt jetzt über eine Standardgeste: `NVDA+Strg+Escape`. (#10560, @CyrilleB79)
  * Bei viermaligem Drücken des Befehls "Auswahl vorlesen" wird der Text in einem Textfenster angezeigt. (#15858, @Emil-18)
* Microsoft Office:
  * Beim Anfordern von Formatierungsinformationen zu Excel-Zellen werden Rahmen und Hintergrund nur ausgegeben, wenn eine solche Formatierung vorhanden ist. (#15560, @CyrilleB79)
  * NVDA gibt keine unbeschrifteten Gruppierungen mehr aus, wie sie beispielsweise in neueren Versionen von Microsoft Office 365-Menüs vorkommen. (#15638)

Die Optionen zur Auswahl des Audioausgabegeräts und die Lautstärkenreduktion anderer Anwendungen wurden aus dem Dialogfeld "Sprachausgabe auswählen" entfernt.
Sie finden sie in den Audio-Einstellungen, die mit `NVDA+Strg+U` geöffnet werden können. (#15512, @codeofdusk)

* Die Option "Objekttyp unter dem Mauszeiger ansagen" in den Mauseinstellungen von NVDA wurde in "Objekt ansagen, wenn die Maus hineinbewegt wird" umbenannt.
Diese Option gibt nun zusätzlich relevante Informationen zu einem Objekt aus, wenn die Maus hineinbewegt wird. Dies sind Informationen wie z. B. Zustände (markiert/gedrückt) oder Zellkoordinaten in einer Tabelle. (#15420, @LeonarddeR)
* Das Hilfe-Menü hat folgende neuen Einträge zu NV Access-Seiten erhalten: "Support erhalten" und "Shop". (#14631)
* Die Unterstützung von [Poedit](https://poedit.net) wurde ab Version 3 und höher komplett überarbeitet.
Nutzer von Poedit 1 wird geraten auf die Version 3 zu aktualisieren, falls sie verbesserte Bedienbarkeit in Poedit möchten. So funktionieren die Tastenkombinationen zum Lesen von Anmerkungen für Übersetzer sowie Kommentaren wieder. (#15313, #7303, @LeonarddeR)
* Braille- und Sprachbetrachter sind im geschützten Modus nicht nutzbar. (#15680)
* Während der Objektnavigation werden deaktivierte (nicht verfügbare) Objekte nicht mehr ignoriert. (#15477, @CyrilleB79)
* Inhaltsverzeichnis zur Befehlsreferenz hinzugefügt. (#16106)

### Fehlerbehebungen

* Store für NVDA-Erweiterungen:
  * Wenn sich der Zustand einer Erweiterung ändert (z. B. von "wird heruntergeladen" in "Übertragung abgeschlossen", wird dies nun korrekt angezeigt. (#15859, @LeonarddeR)
  * Beim Installieren von Erweiterungen wird der Installationsfrtschritt nicht mehr vom Neustartdialog überlagert. (#15613, @lukaszgo1)
  * Wird eine inkompatible Erweiterung erneut installiert, wird diese nicht mehr zwangsläufig deaktiviert. (#15584, @lukaszgo1)
  * deaktivierte inkompatible Erweiterungen können jetzt aktualisiert werden. (#15568, #15029)
  * NVDA zeigt nun einen Fehler an, wenn eine Erweiterung nicht heruntergeladen werden konnte. (#15796)
  * NVDA wird ordnungsgemäß neu gestartet, wenn der Store für Erweiterungenm geöffnet und geschlossen wird. (#16019, @lukaszgo1)
* Audio:
  * NVDA friert nun nicht mehr ein, wenn mehrere Klänge in schneller Folge abgespielt werden. (#15311, #15757, @jcsteh)
  * Wenn ein vom Standard abweichendes Audiogerät eingestellt wird und das Gerät wird (wieder) verfügbar, wird NVDA auf das eingestellte Gerät wechseln. (#15759, @jcsteh)
  * NVDA now resumes audio if the configuration of the output device changes or another application releases exclusive control of the device. (#15758, #15775, @jcsteh)
* Braille:
  * Nehrzeilige Brailleanzeigegeräte bringen BRLTTY nicht mehr zum Absturz. (#15386)
  * Es werde Testinhalte von mehr Objekten in Braille angezeigt (#15605)
  * Die Brailleeingabe von Kurzschrift funktioniert wieder. (#15773, @aaclause)
  * Die Brailleanzeige wird nun zuveerlässiger aktualisiert, wenn der Navigator zwischen Tabellenzellen bewegt wird. (#15755, @Emil-18)
  * Befehle ie "fokussiertes Objekt anzeigtn", "aktuelles Navigatorobjekt anzeigen" oder "Markierten Text anzeigen" funktionieren jetzt auch für Braille. (#15844, @Emil-18)
  * Der Treiber für Albatross behandelt einen ESP32 Microcontroller nicht mehr als Albatross Braillezeile. (#15671)
* LibreOffice:
  * mit strg+Rücktaste gelöschte Wörter erden auch dann korrekt angezeigt, wenn hinter ihnen Leerzeichen oder Tabs stehen. (#15436, @michaelweghorn)
  * Das Anzeigen der Statuszeile mit nvda+(Umschalt+)Ende funktioniert jetzt auch in Dialogen in Libreoffice 2024.2 und neuer. (#15591, @michaelweghorn)
  * In Libreoffice 24.2 und neuer werden alle Textattribute erkannt
  Dies erlaubt die Anzeige von Rechtschreibfehlern in Libreoffice Writer. (#15648, @michaelweghorn)
  * Die Anzeige von Überschriftsebenen funktioniert nun auch in Libreoffice 24.2 und neuer. (#15881, @michaelweghorn)
* Microsoft Office:
  * Wenn Sie in Excel mit deaktiviertem UIA  `strg+y`, `strg+z` oder `alt+Rüpckte` drücken, wird die Brailleanzeige korrekt aktualisiert und der aktuelle Zelleninhalt gesprochen. (#15547)
  * Beim Drücken von `strg+v`, `STRG+x`, `STRG+y`, `STRG+z`, `alt+Rücktaste`, `backspace` oder `STRG+Rücktaste` wird in Microsoft Word mit deaktiviertem UIA die Brailleanzeige aktualisiert.
  Dies funktioniert auch mir aktiviertem UIA, sofern die Brailleanzeige an den NVDA-Cursor gekoppelt ist und der NVDA-Cursor dem Systemcursor folgt. (#3276)
  * In Word wird die Zielzelle korrekt angezeigt, wenn Sie die Word-Eigenen Befehle zur Tabellennavigation verwenden. Hierzu gehören `alt+Pos1`, `alt+ende`, `alt+Bild Auf` und `alt+Bild Ab`. (#15805, @CyrilleB79)
* Die Anzeige von Kurztasten für Objekte wurde verbessert. (#10807, #15816, @CyrilleB79)
* Sapi4-Sprachausgaben können nun beim Sprechen Lautstärke, Stimmhöhe oder Geschwindigkeit ändern. (#15271, @LeonarddeR)
* Mehrzeilige (Eingabe)felder werden in Java-Anwendungen korrekt erkannt. (#14609)
* Das Lesen von Dialoginhalten von Windows 10- und Windows 11-Dialogen funktioniert jetzt zuverlässiger. (#15729, @josephsl)
* Wenn in Microsoft Edge eine Webseite neu geladen wurde, wird sie wieder ordnungsgemäß gelesen. (#15736)
* Beim Buchstabieren sind die Pausen zwischen Sätzen Bzw. Zeichen jetzt wieder angemessen lang und verkürzen sich nicht im Laufe der Zeit. (#15739, @jcsteh)
* NVDA stürzt beim Lesen längerer Texte nicht mehr ab. (#15752, @jcsteh)
* In Microsoft Edge werden jetzt mehr Elemente auf der Webseite angezeigt. (#14612)
* Sollte(n) die Konfogiruationsdatei(en  beschädigt sein, startet NVDA zukünftig mit den Standardeinstellungen - wie früher. (#15690, @CyrilleB79)
* Listenansichten werden wieder ordnungsgemäß angezeigt. (#15283, @LeonarddeR)
* Niemand kann mehr den Eingabeverlauf in der Pyzhon-konsole überschreiben. (#15792, @CyrilleB79)
* NVDA sollte nun nicht mehr abstürzen, wenn viel Text über die Eingabeaufforderung (cmd) rollt oder wenn Sprachnachrichten in Whatsapp abgespielt werden.. (#14888, #15169)
  * Dieses Verhalten kann in den Erweiterten Einstellungen über die Option "Erweiterte Ereignisbehandlung verwenden" abgeschaltet werden.
* NVDA verfolgt den Fokus nun auch in Anwendungen, die unter Windows defender Application Guard ausgeführt werden.. (#15164)
* Der Sprachbetrachter wird nicht mehr aktualisiert, wenn die Maus in seinem Fenster bewegt wird. (#15952, @hwf1324)
* Beim Schließen von Kobinationsfeldern in Firefox oder Chrome mit alt+pfeil auf oder Esc kehrt NVDA in den Lesemodus zurück. (#15653)
* Beim Navigieren in Kombinationsfeldern mit den Pfeiltasten in Itunes schaltet nvda nicht mehr in den Lesemodus. (#15653)

### Änderungen für Entwiskler

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
  * Example: `speech.speakSsml('<speak><prosody pitch="200%">hello</prosody><break time="500ms" /><prosody rate="50%">John</prosody></speak>')`
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
    * `nvdaController_setOnSsmlMarkReachedCallback`: To register a callback of type `onSsmlMarkReachedFuncType` that is called in synchronous mode for every `<mark />` tag encountered in the SSML sequence provided to `nvdaController_speakSsml`.
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

This is a patch release to fix a security issue and installer issue.
Please responsibly disclose security issues following NVDA's [security policy](https://github.com/nvaccess/nvda/blob/master/security.md).

### Security Fixes

* Prevents loading custom configuration while secure mode is forced.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Bug Fixes

* Fixed bug which caused the NVDA process to fail to exit correctly. (#16123)
* Fixed bug where if the previous NVDA process failed to exit correctly, an NVDA installation could fail to an unrecoverable state. (#16122)

## 2023.3.3

This is a patch release to fix a security issue.
Please responsibly disclose security issues following NVDA's [security policy](https://github.com/nvaccess/nvda/blob/master/security.md).

### Security Fixes

* Prevents possible reflected XSS attack from crafted content to cause arbitrary code execution.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

This is a patch release to fix a security issue.
The security patch in 2023.3.1 was not resolved correctly.
Please responsibly disclose security issues following NVDA's [security policy](https://github.com/nvaccess/nvda/blob/master/security.md).

### Security Fixes

* The security patch in 2023.3.1 was not resolved correctly.
Prevents possible system access and arbitrary code execution with system privileges for unauthenticated users.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

This is a patch release to fix a security issue.
Please responsibly disclose security issues following NVDA's [security policy](https://github.com/nvaccess/nvda/blob/master/security.md).

### Security Fixes

* Prevents possible system access and arbitrary code execution with system privileges for unauthenticated users.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Diese Version enthält Verbesserungen bei der Leistung, Reaktionsfähigkeit und Stabilität der Audio-Ausgabe.
Es wurden Optionen für die Lautstärke der NVDA-Sounds und -Signaltöne zum Steuern oder Anpassen der Lautstärke der verwendeten Stimme hinzugefügt.

NVDA aktualisiert die Ergebnisse der Texterkennung jetzt regelmäßig und teilt neuen Text mit, sobald er erscheint.
Dies kann in der Kategorie "Windows-Texterkennung" in den NVDA-Einstellungen konfiguriert werden.

Mehrere Korrekturen wurden für Braille vorgenommen, die die Geräteerkennung und die Navigation der Schreibmarke verbessern.
Unerwünschte Treiber können jetzt von der automatischen Erkennung ausgeschlossen werden, um die Leistung der automatischen Erkennung zu verbessern.
Außerdem gibt es neue BRLTTY-Befehle.

Weitere Fehler wurden außerdem im Store für NVDA-Erweiterungen, in Microsoft Office, in den Kontextmenüs von Microsoft Edge und im Windows-Rechner behoben.

### Neue Features

* Verbessertes Sound-Management:
  * Ein neues Audio-Einstellungsfeld:
    * Dies kann mit `NVDA+Strg+U` geöffnet werden. (#15497)
    * Eine Option in den Audio-Einstellungen, mit der die Lautstärke der NVDA-Sounds und -Signaltöne der Lautstärke-Einstellung der verwendeten Stimme folgt. (#1409)
    * Eine Option in den Audio-Einstellungen, um die Lautstärke der NVDA-Sounds separat zu konfigurieren. (#1409, #15038)
    * Die Einstellungen zum Ändern des Audio-Ausgabegeräts und zum Umschalten zur Verringerung der Audio-Quellen wurden in das neue Audio-Einstellungsfeld im Dialogfeld "Sprachausgabe auswählen" verschoben.
    Diese Optionen werden im Dialogfeld "Sprachausgabe auswählen" in 2024.1 entfernt. (#15486, #8711)
  * NVDA verwendet nun Audio über die API der Windows-Audio-Session (WASAPI), was die Reaktionsfähigkeit, Leistung und Stabilität der Sprachausgaben und NVDA-Sounds verbessern kann. (#14697, #11169, #11615, #5096, #10185,e #11061)
  * Hinweis: WASAPI ist mit einigen NVDA-Erweiterungen nicht kompatibel.
  Für diese NVDA-Erweiterungen sind kompatible Updates verfügbar. Bitte aktualisieren Sie diese, bevor Sie NVDA aktualisieren.
  Inkompatible Versionen dieser NVDA-Erweiterungen werden beim NVDA-Update deaktiviert:
    * Tony's Enhancements Version 1.15 oder älter. (#15402)
    * NVDA Global Commands Extension 12.0.8 oder älter. (#15443)
* NVDA ist nun in der Lage, bei der Texterkennung (OCR) das Ergebnis kontinuierlich zu aktualisieren und neuen Text mitzuteilen, sobald er erscheint. (#2797)
  * Um diese Funktion zu aktivieren, aktivieren Sie in den NVDA-Einstellungen in der Kategorie "Windows-Texterkennung" die Option "Erkannte Inhalte regelmäßig aktualisieren".
  * Sobald diese Funktion aktiviert ist, können Sie neuen Text mit `NVDA+5` sich mitteilen lassen, indem Sie die Änderungen dynamischer Inhalte umschalten.
* Bei der automatischen Erkennung von Braillezeilen ist es nun möglich, Treiber von der Erkennung auszuschließen, und zwar im Dialogfeld zur Auswahl der Braillezeile. (#15196)
* Eine neue Option in den Einstellungen für die Dokument-Formatierung "Ignorieren von Leerzeilen bei Mitteilung von Zeileneinrückungen". (#13394)
* Es wurde ein nicht zugewiesener Tastenbefehlhinzugefügt, um im Lesemodus durch die Registerkarten-Gruppierungen zu navigieren. (#15046)

### Änderungen

* Braille:
  * Wenn sich der Text in einem Terminal ändert, ohne dass der Cursor aktualisiert wird, wird der Text auf einer Braillezeile jetzt korrekt aktualisiert, wenn er auf einer geänderten Zeile steht.
  Dies gilt auch für Situationen, in denen die Braille-Ausgabe dem NVDA-Cursor folgt. (#15115)
  * Weitere BRLTTY-Tastenbelegungen sind nun NVDA-Befehlen zugeordnet (#6483):
    * `learn`: Eingabehilfe von NVDA umschalten
    * `prefmenu`: Das NVDA-Menü öffnen
    * `prefload`/`prefsave`: NVDA-Konfiguration laden/speichern
    * `time`: Datum und Uhrzeit anzeigen
    * `say_line`: Teilt die aktuelle Zeile mit, in der sich der NVDA-Cursor befindet
    * `say_below`: Alles sich mit dem NVDA-cursor vorlesen lassen
  * Der BRLTTY-Treiber ist nur verfügbar, wenn eine BRLTTY-Instanz mit aktivierter BrlAPI läuft. (#15335)
  * Die erweiterte Einstellung zur Aktivierung der HID-Unterstützung für die Braille-Ausgabe wurde zugunsten einer neuen Option entfernt.
  Sie können nun bestimmte Treiber für die automatische Erkennung von Braillezeilen im Dialogfeld zur Auswahl für Braillezeilen deaktivieren. (#15196)
* Store für NVDA-Erweiterungen: Installierte Pakete werden nun in der Registerkarte Verfügbare Pakete aufgelistet, sofern sie im Store verfügbar sind. (#15374)
* Einige Tastenkombinationen wurden im NVDA-Menü aktualisiert. (#15364)

### Fehlerbehebungen

* Microsoft Office:
  * Absturz behoben in Microsoft Word, wenn die Option in den Dokument-Formatierungen "Überschriften mitteilen" und "Kommentare und Anmerkungen mitteilen" nicht aktiviert waren. (#15019)
  * In Microsoft Word und Microsoft Excel wird die Textausrichtung in weiteren Situationen korrekt mitgeteilt. (#15206, #15220)
  * Behebt die Anzeige bei einigen Kurztasten für die Zellenformatierung in Microsoft Excel. (#15527)
* Microsoft Edge:
  * NVDA springt beim Öffnen des Kontextmenüs in Microsoft Edge nicht mehr zur letzten Position im Lesemodus zurück. (#15309)
  * NVDA ist wieder in der Lage, Kontextmenüs von Downloads in Microsoft Edge auszulesen. (#14916)
* Braille:
  * Der Braille-Cursor und die Auswahl-Indikatoren werden nun immer korrekt aktualisiert, wenn die entsprechenden Indikatoren durch einen Tastenbefehl ein- oder ausgeblendet werden. (#15115)
  * Fehler behoben, bei dem Braillezeilen von Albatross versuchten, sich zu initialisieren, obwohl eine andere Braillezeile angeschlossen ist. (#15226)
* Store für NVDA-Erweiterungen:
  * Fehler behoben, bei dem das Deaktivieren der Option "Inkompatible Pakete einschließen" dazu führte, dass inkompatible NVDA-Erweiterungen weiterhin im Store aufgeführt wurden. (#15411)
  * NVDA-Erweiterungen, die aus Kompatibilitätsgründen blockiert sind, sollten nun korrekt gefiltert werden, wenn der Filter für den Status aktiviert/deaktiviert umgeschaltet wird. (#15416)
  * Fehler behoben, der verhindert, dass inkompatible NVDA-Erweiterungen, die installiert und aktiviert sind, mit dem externen Installations-Tool aktualisiert oder ersetzt werden. (#15417)
  * Fehler behoben, bei dem NVDA nach der Installation der NVDA-Erweiterung erst nach einem Neustart die Sprachausgabe  wieder funktionierte. (#14525)
  * Fehler behoben, bei dem NVDA-Erweiterungen nicht installiert werden konnten, wenn ein vorheriger Download fehlschlug oder abbrach. (#15469)
  * Probleme beim Umgang mit inkompatiblen NVDA-Erweiterungen beim NVDA-Update wurden behoben. (#15414, #15412, #15437)
* NVDA teilt erneut Berechnungsergebnisse im Windows-Rechner (32-Bit) auf Server-, LTSC- und LTSB-Versionen von Windows mit. (#15230)
* NVDA ignoriert beim Wechseln nicht mehr den Fokus, sobald ein verschachteltes Fenster (großes Unterfenster) fokussiert wurde. (#15432)
* Eine mögliche Absturzursache beim Starten von NVDA wurde behoben. (#15517)

### Änderungen für Entwickler

Bitte lesen Sie [das Entwicklerhandbuch](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) für Informationen über den Prozess bei API-Änderungen in NVDA.

* `braille.handler.handleUpdate` und `braille.handler.handleReviewMove` wurden geändert, um eine sofortige Erneuerung zu vermeiden.
Vor dieser Änderung wurden bei sehr häufigen Aufrufen einer dieser Methoden viele Ressourcen verbraucht.
Diese Methoden stellen nun eine Erneuerung am Ende jedes Kernzyklus in die Warteschlange.
Sie sollten auch Thread-sicher sein, so dass sie von Hintergrund-Threads aus aufgerufen werden können. (#15163)
* Offizielle Unterstützung für die Registrierung von benutzerdefinierten Braillezeilen-Treibern bei der automatischen Erkennung von Braillezeilen wurde hinzugefügt.
Lesen Sie die Dokumentation der Klasse `braille.BrailleDisplayDriver` für weitere Details.
Vor allem muss das Attribut `supportsAutomaticDetection` auf `True` gesetzt und die Klassenmethode `registerAutomaticDetection` implementiert sein. (#15196)

#### Veraltete Funktionen

* Die Funktion `braille.BrailleHandler.handlePendingCaretUpdate` ist jetzt veraltet, ohne Ersatz.
Sie wird in 2024.1 entfernt. (#15163)
* Das Importieren der Konstanten `xlCenter`, `xlJustify`, `xlLeft`, `xlRight`, `xlDistributed`, `xlBottom`, `xlTop` aus `NVDAObjects.window.excel` sind veraltet.
Verwenden Sie stattdessen die Enumerationen `XlHAlign` oder `XlVAlign`. (#15205)
* Das Mapping `NVDAObjects.window.excel.alignmentLabels` ist veraltet.
Verwenden Sie stattdessen die Methoden `displayString` der `XlHAlign`- oder die Enumerationen `XlVAlign`. (#15205)
* `bdDetect.addUsbDevices` und `bdDetect.addBluetoothDevices` sind veraltet
In Braillezeilen-Treiber sollte stattdessen die Methode `registerAutomaticDetection` implementiert werden.
Diese Methode erhält ein Objekt `DriverRegistrar`, auf das die Methoden `addUsbDevices` und `addBluetoothDevices` angewendet werden können. (#15200)
* Die Standard-Implementierung der Methode zur Überprüfung von `BrailleDisplayDriver` verwendet `bdDetect.driverHasPossibleDevices` für Geräte, die als Thread-sicher markiert sind.
Damit die Basis-Methode `bdDetect.driverHasPossibleDevices` verwendet werden kann, muss ab NVDA 2024.1 das Attribut `supportsAutomaticDetection` ebenfalls auf `True` gesetzt werden. (#15200)

## 2023.2

Mit dieser Version wird der Store für NVDA-Erweiterungen eingeführt, der den vorherigen Eintrag "Erweiterungen verwalten" ersetzt.
Im diesem Store können Sie nach NVDA-Erweiterungen aus der Community direkt suchen, installieren und aktualisieren.
Sie können jetzt Inkompatibilitätsprobleme mit veralteten NVDA-Erweiterungen auf eigene Gefahr manuell ausschalten.

Es gibt neue Braille-Funktionen, Befehle und Unterstützung für Braillezeilen.
Außerdem gibt es neue Tastenbefehle für die Texterkennung und die Navigation mit abgeflachten Objekten.
Die Navigation und Mitteilung von Formatierungen in Microsoft Office wurde verbessert.

Es gibt viele Fehlerbehebungen, insbesondere für Braille, Microsoft Office, Web-Browsern und Windows 11.

Die Sprachausgabe eSpeak-NG, der Braille-Übersetzer LibLouis, und das vom Unicode-Konsortium stammende Common Locale Data Repository (kurz CLDR) wurden aktualisiert.

### Neue Features

* Der Store für NVDA-Erweiterungen wurde in NVDA integriert. (#13985)
  * Durchsuchen, suchen, installieren und aktualisieren von NVDA-Erweiterungen aus der Community.
  * Inkompatibilitätsprobleme mit veralteten NVDA-Erweiterungen können manuell deaktiviert werden.
  * Der Eintrag "Erweiterungen verwalten" im Menü Werkzeuge wurde entfernt und durch den Store für NVDA-Erweiterungen ersetzt.
  * Für weitere Informationen lesen Sie bitte das aktualisierte NVDA-Benutzerhandbuch.
* Neue Tastenbefehle:
  * Ein nicht zugewiesener Tastenbefehl zum Wechseln der verfügbaren Sprachen für die Windows-Texterkennung. (#13036)
  * Ein nicht zugewiesener Tastenbefehl, um durch die Modi der Braillezeilen zu wechseln. (#14864)
  * Ein nicht zugewiesener Tastenbefehl, um die Anzeige des Auswahl-Indikators auf der Braillezeile umzuschalten. (#14948)
  * Es wurden Standard-Zuweisungen für die Tastenbefehle hinzugefügt, um in einer reduzierten Ansicht der Hierarchie zum nächsten oder vorherigen Objekt zu wechseln. (#15053)
    * Desktop: `NVDA+Nummernblock 9` und `NVDA+Nummernblock 3`, um zum vorherigen bzw. nächsten Objekt zu gelangen.
    * Laptop: `Umschalt+NVDA+Ü` und `Umschalt+NVDA+Plus`, um zum vorherigen bzw. nächsten Objekt zu gelangen.
* Neue Braille-Features:
  * Unterstützung für die Braillezeile des Help Tech Activator wurde hinzugefügt. (#14917)
  * Eine neue Option zum Umschalten der Anzeige des Auswahl-Indikators (Punkte 7 und 8). (#14948)
  * Eine neue Option zur optionalen Verschiebung des System-Cursors oder des Fokus beim Ändern der Position des NVDA-Cursors mit den Routing-Tasten auf der Braillezeile. (#14885, #3166)
  * Wenn man `Nummernblock 2` dreimal drückt, um den numerischen Wert des Zeichens an der Position des NVDA-Cursors anzuzeigen, wird die Information jetzt auch auf der Braillezeile angezeigt. (#14826)
  * Unterstützung für das ARIA 1.3-Attribut `aria-brailleroledescription` hinzugefügt, welches es Web-Autoren ermöglicht, den Typ eines auf der Braillezeile angezeigten Elements zu überschreiben. (#14748)
  * Braillezeilen-Treiber für Geräte von der ehemaligen Firma Baum Retec AG: Mehrere Braille-Tastenkombinationen zur Ausführung gängiger Tastaturbefehle wie `Windows+D` und `Alt+Tab` hinzugefügt.
  Eine vollständige Liste finden Sie im NVDA-Benutzerhandbuch. (#14714)
* Aussprache von Unicode-Symbolen hinzugefügt:
  * Braille-Symbole, wie z. B. `⠐⠣⠃⠗⠇⠐⠜`. (#14548)
  * Symbol der Mac-Optionstaste `⌥`. (#14682)
* Tastenbefehle für die Braillezeilen Albatross von Tivomatic Caiku hinzugefügt. (#14844, #15002)
  * Anzeigen des Dialogfelds für die Braille-Einstellungen
  * Zugriff auf die Statusleiste
  * Wechseln der Form des Braille-Cursors
  * Modus umschalten für die Anzeige von Meldungen in Braille-Schrift
  * Ein- / Ausschalten des Braille-Cursors
  * Umschalten des Zustands "Braille-Anzeige zur Auswahl".
  * Umschalten auf den Modus auf der Braillezeile verschiebt den System-Cursor beim folgen des NVDA-Cursors. (#15122)
* Microsoft Office-Features:
  * Wenn die Dokument-Formatierung für hervorgehobenen Text aktiviert ist, werden die Farben der Hervorhebungen jetzt in Microsoft Word mitgeteilt. (#7396, #12101, #5866)
  * Wenn Farben in der Dokument-Formatierung aktiviert sind, werden die Hintergrundfarben jetzt in Microsoft Word mitgeteilt. (#5866)
  * Wenn Sie Tastenkombinationen in Microsoft Excel verwenden, um Formatierungen wie Fett, Kursiv, Unterstrichen und Durchgestrichen für eine Zelle umzuschalten, wird das Ergebnis entsprechend mitgeteilt. (#14923)
* Verbessertes Sound-Management (experimentell):
  * NVDA kann jetzt Audio über die Windows-Audio-Session-API (WASAPI) ausgeben, was die Reaktionsfähigkeit, Leistung und Stabilität von NVDA-Sounds und Sprachausgaben verbessern kann. (#14697)
  * Die Verwendung von WASAPI kann in den erweiterten Einstellungen aktiviert werden.
  Wenn WASAPI aktiviert ist, können außerdem die folgenden erweiterten Einstellungen konfiguriert werden:
    * Eine Option, mit der die Lautstärke der NVDA-Sounds und Signaltöne an die Lautstärke-Einstellung der verwendeten Stimme angepasst werden kann. (#1409)
    * Eine Option zur separaten Konfiguration der Lautstärke von NVDA-Sounds. (#1409, #15038)
  * Es gibt ein bekanntes Problem mit zeitweiligen Abstürzen, falls WASAPI aktiviert ist. (#15150)
* In Mozilla Firefox und Google Chrome teilt NVDA nun mit, wenn ein Steuerelement einen Dialog, ein Gitter, eine Liste oder einen Baum öffnet, wenn der Autor dies mit `aria-haspopup` angegeben hat. (#14709)
* Es ist nun möglich, bei der Erstellung portabler NVDA-Versionen die Systemvariablen (wie `%temp%` oder `%homepath%`) in der Pfadangabe zu verwenden. (#14680)
* In Windows 10 Mai 2019 Update und neuer teilt NVDA die Namen virtueller Desktops beim Öffnen, Ändern und Schließen mit. (#5641)
* Es wurde ein systemweiter Parameter hinzugefügt, der es Benutzern und Systemadministratoren ermöglicht, den Start von NVDA im sicheren Modus zu erzwingen. (#10018)

### Änderungen

* Komponenten-Updates:
  * Die Sprachausgabe eSpeak NG wurde auf 1.52-dev commit `ed9a7bcf` aktualisiert. (#15036)
  * Der LibLouis-Braille-Übersetzer wurde auf [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0) akutalisiert. (#14970)
  * CLDR wurde auf Version 43.0 aktualisiert. (#14918)
* Änderungen für LibreOffice:
  * Bei der Meldung der Position des NVDA-Cursors wird in LibreOffice Writer 7.6 und neuer nun die aktuelle Cursor-Position des bzw. System-Cursors relativ zur aktuellen Seite gemeldet, ähnlich wie bei Microsoft Word. (#11696)
  * Die Mitteilung der Statusleiste (z. B. ausgelöst durch `NVDA+Ende`) funktioniert bei LibreOffice. (#11698)
  * Beim Wechsel zu einer anderen Zelle in LibreOffice Calc zeigt NVDA nicht mehr fälschlicherweise die Koordinaten der zuvor fokussierten Zelle an, wenn die Anzeige der Zellkoordinaten in den Einstellungen von NVDA deaktiviert ist. (#15098)
* Änderungen für Braille:
  * Bei Verwendung einer Braillezeile über den Standard-HID-Braillezeilen-Treiber kann das Daumen-Pad (D-Pad) zur Emulation der Pfeiltasten und der Eingabetaste verwendet werden.
  Auch `Leertaste+Punkt1` und `Leertaste+Punkt4` entsprechen jetzt den Pfeiltasten nach oben bzw. nach unten. (#14713)
  * Aktualisierungen dynamischer Web-Inhalte (ARIA-Live-Regionen) werden jetzt in auf der Braillezeile angezeigt.
  Diese Funktion kann im Bereich für die Erweiterte Einstellungen deaktiviert werden. (#7756)
* Bindestrich- und Strich-Symbole werden immer an die Sprachausgabe gesendet. (#13830)
* Bei Entfernungsangaben in Microsoft Word wird nun die in den erweiterten Optionen von Word definierte Einheit berücksichtigt, auch wenn UIA für den Zugriff auf Word-Dokumente verwendet wird. (#14542)
* Bei der Meldung der Position des NVDA-Cursors wird in LibreOffice Writer für LibreOffice-Versionen >= 7.6 nun die aktuelle Position des normalen Cursor und System-Cursors relativ zur aktuellen Seite mitgeteilt, ähnlich wie bei Microsoft Word. (#11696)
* NVDA reagiert nun etwas schneller auf Befehle und bei Fokus-Änderungen. (#14701)
* NVDA reagiert schneller beim Bewegen des Cursors in den Bearbeitungsfunktionen. (#14708)
* Das Skript für die Meldung der Link-Zieladresse geht nun von der Position des normalen Cursors und des System-Cursors aus und nicht mehr vom Navigator-Objekt. (#14659)
* Bei der Erstellung portabler NVDA-Versionen ist es nicht mehr erforderlich, dass ein Laufwerksbuchstabe als Teil des absoluten Pfads angegeben werden muss. (#14680)
* Bei der Sekunden-Anzeige der Uhrzeit in der Taskleiste von Windows, wird diese Einstellung durch die Verwendung von `NVDA+F12` zur Anzeige der Uhrzeit berücksichtigt. (#14742)
* NVDA teilt jetzt nicht beschriftete Gruppierungen mit, die nützliche Positionsinformationen enthalten, wie z. B. in Menüs aktueller Versionen von Microsoft Office 365. (#14878) 

### Fehlerbehebungen

* Braille:
  * Mehrere Korrekturen in der Stabilität bei der Eingabe bzw. Ausgabe für Braillezeilen, was zu weniger Fehlern und Abstürzen von NVDA führt. (#14627)
  * NVDA schaltet bei der automatischen Erkennung nicht mehr unnötigerweise mehrmals auf keine Braille-Schrift um, was zu einem saubereren Protokoll und weniger Overhead führt. (#14524)
  * NVDA schaltet nun wieder auf USB um, wenn ein HID-Bluetooth-Gerät (z. B. HumanWare Brailliant oder APH Mantis) automatisch erkannt wird und eine USB-Verbindung verfügbar ist.
  Dies funktionierte bisher nur bei seriellen Bluetooth-Schnittstellen. (#14524)
  * Ist keine Braillezeile angeschlossen und wird der Braille-Betrachter durch Drücken von `Alt+F4` oder durch Anklicken des Schalters "Schließen" geschlossen, wird die Anzeigegröße des Braille-Subsystems sowie auch die Braille-Module wieder zurückgesetzt. (#15214)
* Web-Browser:
  * NVDA führt nicht mehr gelegentlich dazu, dass Mozilla Firefox abstürzt oder nicht mehr antwortet. (#14647)
  * In Mozilla Firefox und Google Chrome werden Zeichen während der Eingabe in einigen Textfeldern nicht mehr angezeigt, auch wenn die Funktion "Zeichen während der Eingabe ansagen" deaktiviert ist. (#8442)
  * Sie können jetzt den Lesemodus in Chromium Embedded Controls verwenden, wo dies vorher nicht möglich war. (#13493, #8553)
  * In Mozilla Firefox wird der Text nach einem Link nun zuverlässig angezeigt, wenn man die Maus über den Text bewegt. (#9235)
  * Das Ziel von grafischen Links wird jetzt in Google Chrome und Microsoft Edge in mehr Fällen korrekt angezeigt.  (#14783)
  * Beim Versuch, die URL für einen Link ohne href-Attribut mitzuteilen, schweigt NVDA sich nicht mehr aus.
  Stattdessen teilt NVDA mit, dass der Link kein Ziel hat. (#14723)
  * Im Lesemodus ignoriert NVDA nicht mehr fälschlicherweise den Fokus, wenn er zu einem über- oder untergeordneten Steuerelement wechselt, z. B. wenn er von einem Steuerelement zu einem übergeordneten Listenelement oder einer Gitterzelle wechselt. (#14611)
    * Beachten Sie jedoch, dass diese Korrektur nur gilt, wenn die Option Fokus automatisch auf fokussierbare Elemente setzen" in den Einstellungen für den Lesemodus deaktiviert ist (was die Standard-Einstellung ist).
* Korrekturen für Windows 11:
  * NVDA zeigt wieder den Inhalt der Statusleiste im Editor (Notepad) an. (#14573)
  * Wenn Sie zwischen den Registerkarten wechseln, werden der neue Name und die neue Position der Registerkarte im Editor (Notepad) und Datei-Explorer angezeigt. (#14587, #14388)
  * NVDA teilt bei der Texteingabe in Sprachen wie Chinesisch und Japanisch wieder Kandidaten mit. (#14509)
  * Es ist nun wieder möglich, die Punkte Mitwirkende und Lizenz im NVDA-Hilfemenü aufzurufen. (#14725)
* Korrekturen für Microsoft Office:
  * Wenn Sie sich schnell durch Zellen in Excel bewegen, meldet NVDA jetzt seltener die falsche Zelle oder Auswahl. (#14983, #12200, #12108)
  * Wenn Sie von außerhalb eines Arbeitsblatts auf eine Zelle in Microsoft Excel zugreifen, werden der Highlighter für die Braille-Ausgabe und für den Fokus nicht mehr unnötigerweise auf das Objekt aktualisiert, das zuvor den Fokus hatte. (#15136)
  * NVDA teilt keine fokussierenden Passwortfelder in Microsoft Excel und Microsoft Outlook mehr mit. (#14839)
* Für Symbole, die keine Symbolbeschreibung im aktuellen Gebietsschema haben, wird standardmäßig die englische Symbolstufe entsprechend verwendet. (#14558, #14417)
* Es ist jetzt möglich, das Backslash-Zeichen im Ersetzungsfeld eines Wörterbucheintrags zu verwenden, wenn der Typ nicht auf regulären Ausdruck eingestellt ist. (#14556)
* Im Rechner von Windows 10 und 11 gibt eine portable NVDA-Version bei der Eingabe von Ausdrücken in den Standard-Taschenrechner im kompakten Überlagerungsmodus keine Fehlermeldungen mehr aus oder spielt Fehlertöne ab. (#14679)
* NVDA erholt sich wieder von vielen weiteren Situationen, wie z. B. von Anwendungen, die nicht mehr reagieren, was zuvor zu einem vollständigen Einfrieren führte. (#14759) 
* Beim Erzwingen der UIA-Unterstützung mit bestimmten Terminals und Konsolen wurde ein Fehler behoben, der zu einem Einfrieren und einem Spamming der Protokolldatei führte. (#14689)
* NVDA verweigert nicht mehr die Konfiguration nach einem Zurücksetzen der Konfiguration zu speichern. (#13187)
* Wenn eine temporäre Version über den Launcher gestartet wird, führt NVDA den Benutzer nicht mehr in die Irre, dass er die Konfiguration speichern kann. (#14914)
* NVDA reagiert jetzt generell etwas schneller auf Befehle und Fokus-Änderungen. (#14928)
* Die Anzeige der Einstellungen für die Texterkennung schlägt auf einigen Systemen nicht mehr fehl. (#15017)
* Behebung eines Fehlers im Zusammenhang mit dem Speichern und Laden der NVDA-Konfiguration, einschließlich des Umschaltens von Sprachausgaben. (#14760)
* Es wurde ein Fehler behoben, der dazu führte, dass die Touch-Geste "Nach oben streichen" bei der Textansicht zum Verschieben der Seiten führte, anstatt zur vorherigen Zeile. (#15127)

### Änderungen für Entwickler

Bitte lesen Sie [das Entwicklerhandbuch](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) für Informationen über den Prozess bei API-Änderungen in NVDA.

* Die Spezifikation des Manifests bei NVDA-Erweiterungen wurde um vorgeschlagene Konventionen ergänzt.
Diese sind für die Kompatibilität für NVDA optional, werden aber für die Einreichung im Store für NVDA-Erweiterungen empfohlen oder benötigt. (#14754)
  * Verwenden Sie `lowerCamelCase` für das Namensfeld.
  * Verwenden Sie das Format `<major>.<minor>.<patch>` für das Versionsfeld (erforderlich für Datenspeicher der NVDA-Erweiterung).
  * Verwenden Sie `https://` als Schema für das Adressfeld (erforderlich für Datenspeicher der NVDA-Erweiterung).
* Es wurde ein neuer Erweiterungspunkttyp namens `Chain` hinzugefügt, der verwendet werden kann, um über Iterables zu iterieren, die von registrierten Handlern zurückgegeben werden. (#14531)
* Der Erweiterungspunkt `bdDetect.scanForDevices` wurde hinzugefügt.
Es können Handler registriert werden, die Paare `BrailleDisplayDriver/DeviceMatch` liefern, die nicht in die bestehenden Kategorien passen, wie USB oder Bluetooth. (#14531)
* Erweiterungspunkt hinzugefügt: `synthDriverHandler.synthChanged`. (#14618)
* Der Einstellungsring für die Sprachausgabe von NVDA speichert jetzt die verfügbaren Einstellungswerte, wenn sie zum ersten Mal benötigt werden, und nicht mehr beim Laden der Sprachausgabe. (#14704)
* Sie können jetzt die Exportmethode für eine Zusammenstellung der Tastenbefehlen aufrufen, um sie in ein Wörterbuch zu exportieren.
Dieses Wörterbuch kann in einen anderen Tastenbefehl importiert werden, indem es entweder an den Konstruktor von `GlobalGestureMap` oder an die Update-Methode einer bestehenden Zusammenstellung übergeben wird. (#14582)
* `hwIo.base.IoBase` und seine Derivate haben nun einen neuen Konstruktorparameter, der einen `hwIo.ioThread.IoThread` aufnehmen kann.
Wenn nicht angegeben, wird der Standard-Thread verwendet. (#14627)
* `hwIo.ioThread.IoThread` hat nun eine Methode `setWaitableTimer`, um einen verzögerten Timer mittels einer Python-Funktion zu setzen.
Ebenso erlaubt die neue Methode `getCompletionRoutine` die sichere Umwandlung einer Python-Methode in eine Abschlussroutine. (#14627)
* `offsets.OffsetsTextInfo._get_boundingRects` sollte nun immer `List[locationHelper.rectLTWH]` zurückgeben, wie es für eine Unterklasse von `textInfos.TextInfo` erwartet wird. (#12424)
* `Highlight-Farbe` ist nun ein Formatfeld-Attribut. (#14610)
* NVDA sollte genauer feststellen können, ob eine protokollierte Meldung vom NVDA-Kern stammt. (#14812)
* NVDA protokolliert keine unpräzisen Warnungen oder Fehler über veraltete appModules mehr. (#14806)
* Alle NVDA-Erweiterungspunkte werden jetzt in einem neuen, eigenen Kapitel im Entwicklerhandbuch kurz beschrieben. (#14648)
* `scons checkpot` überprüft nun nicht mehr den Unterordner `userConfig`. (#14820)
* Zu übersetzende Strings können nun mit Hilfe von `ngettext` und `npgettext` mit einer Singular- und einer Pluralform definiert werden. (#12445)

#### Veraltete Funktionen

* Die Übergabe von Lambda-Funktionen an `hwIo.ioThread.IoThread.queueAsApc` ist veraltet.
Stattdessen sollten Funktionen schwach referenzierbar sein. (#14627)
* Der Import von `LPOVERLAPPED_COMPLETION_ROUTINE` aus `hwIo.base` ist veraltet.
Stattdessen besser aus `hwIo.ioThread` importieren. (#14627)
* `IoThread.autoDeleteApcReference` ist veraltet.
Dies wurde in NVDA 2023.1 eingeführt und war nie als Teil der öffentlichen API gedacht.
Solange er nicht entfernt wird, verhält er sich wie ein No-op, d. h., ein Kontext-Manager, ohne Auswirkung. (#14924)
* `gui.MainFrame.onAddonsManagerCommand` ist veraltet, verwenden Sie stattdessen `gui.MainFrame.onAddonStoreCommand`. (#13985)
* `speechDictHandler.speechDictVars.speechDictsPath` ist veraltet, verwenden Sie stattdessen `NVDAState.WritePaths.speechDictsDir`. (#15021)
* Importieren von `voiceDictsPath` und `voiceDictsBackupPath` aus `speechDictHandler.dictFormatUpgrade` ist veraltet.
Verwenden Sie stattdessen `WritePaths.voiceDictsDir` und `WritePaths.voiceDictsBackupDir` aus `NVDAState`. (#15048)
* `config.CONFIG_IN_LOCAL_APPDATA_SUBKEY` ist veraltet.
Verwenden Sie stattdessen `config.RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY`. (#15049)

## 2023.1

Eine neue Option wurde hinzugefügt, "Absatzstil" in "Dokument-Navigation".
Dies kann mit Text-Editoren verwendet werden, die die Absatznavigation nicht von Haus aus unterstützen, wie Notepad und Notepad++.

Es gibt einen neuen globalen Befehl, um das Ziel eines Links mitzuteilen, der über `NVDA+K` abgerufen werden kann.

Die Unterstützung für kommentierte Webinhalte (wie Kommentare und Fußnoten) wurde verbessert.
Drücken Sie `NVDA+D`, um durch die Zusammenfassungen zu navigieren, wenn Anmerkungen mitgeteilt werden (z. B. "enthält Kommentar, enthält Fußnote").

Die Braillezeilen Tivomatic Caiku Albatross 46 und 80 werden nun unterstützt.

Die Unterstützung für ARM64- und AMD64-Versionen von Windows wurde verbessert.

Es gibt viele Fehlerbehebungen, vor allem für Windows 11.

eSpeak, LibLouis, Sonic Rate Boost und Unicode CLDR wurden aktualisiert.
Es gibt neue Braille-Tabellen für Georgisch, Swahili (Kenia) und Chichewa (Malawi).

Hinweis:

* In dieser Version müssen die Kompatibilitätsanforderungen mit bestehenden NVDA-Erweiterungen überprüft werden.

### Neue Features

* Microsoft Excel über UIA: Automatische Mitteilung von Spalten- und Zeilenüberschriften in Tabellen. (#14228)
  * Hinweis: Dies bezieht sich auf Tabellen, die über die Schaltfläche "Tabelle" im Bereich "Einfügen" der Multifunktionsleiste formatiert werden.
  "Erste Spalte" und "Kopfzeile" in "Tabellen-Eigenschaftens-Optionen" entsprechen den Spalten- bzw. Zeilenköpfen.
  * Dies bezieht sich nicht auf Screenreader-spezifische Überschriften über benannte Bereiche, die derzeit von UIA nicht unterstützt werden.
* Ein nicht zugewiesenes Skript wurde hinzugefügt, um verzögerte Zeichen-Beschreibungen umzuschalten. (#14267)
* Es wurde eine experimentelle Option zur Nutzung der UIA-Benachrichtigungsunterstützung in Windows-Terminal hinzugefügt, um neuen oder geänderten Text im Terminal mitzuteilen, was zu einer verbesserten Stabilität und Reaktionsfähigkeit führt. (#13781)
  * Informationen zu den Einschränkungen dieser experimentellen Option finden Sie im Benutzerhandbuch.
* Unter Windows 11 ARM64 ist der Browse-Modus jetzt in AMD64-Anwendungen wie Mozilla Firefox, Google Chrome und 1Password verfügbar. (#14397)
* Eine neue Option wurde hinzugefügt, "Absatz-Eigenschaften" in "Dokument-Navigation".
Damit wird die Absatz-Navigation mit einfachem Zeilenumbruch (normal) und mehrzeiligem Umbruch (Block) unterstützt.
Dies kann mit Text-Editoren verwendet werden, die die Absatz-Navigation nicht nativ unterstützen, wie Editor und Notepad++. (#13797)
* Das Vorhandensein von mehreren Anmerkungen wird nun mitgeteilt.
Die Tastenkombination `NVDA+D` durchläuft nun die Zusammenfassung jedes Anmerkungsziels für Ursprünge mit mehreren Anmerkungszielen.
Zum Beispiel, wenn der Text mit einem Kommentar und einer Fußnote versehen ist. (#14507, #14480)
* Unterstützung für Braillezeilen Tivomatic Caiku Albatross 46/80 hinzugefügt. (#13045)
* Neuer globaler Befehl: Link-Ziel mitteilen (`NVDA+K`).
Einmaliges Drücken wird das Ziel des Links im Navigator-Objekt mitgeteilt.
Zweimaliges Drücken zeigt die Information in einem Fenster an, welches eine genauere Überprüfung ermöglicht. (#14583)
* Neuer, nicht zugeordneter globaler Befehl (Kategorie Werkzeuge): Link-Ziel in einem Fenster mitteilen.
Entspricht dem zweimaligen Drücken von `NVDA+K`, kann aber für Braille-Nutzer nützlicher sein. (#14583)

### Änderungen

* Der LibLouis-Braille-Übersetzer wurde auf [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0) aktualisiert. (#14436)
  * Wichtige Aktualisierungen der ungarischen, UEB- und chinesischen Bopomofo-Schrift.
  * Unterstützung der dänischen Braille-Schriftnorm 2022.
  * Neue Braille-Tabellen für die georgische Braille-Schrift, Suaheli (Kenia) und Chichewa (Malawi).
* Sonic-Rate-Boost-Bibliothek auf Commit `1d70513` aktualisiert. (#14180)
* CLDR wurde auf Version 42.0 aktualisiert. (#14273)
* eSpeak NG wurde auf 1.52-dev commit `f520fecb` aktualisiert. (#14281, #14675)
  * Die Ansage großer Zahlen wurde korrigiert. (#14241)
* Java-Anwendungen mit Steuerelementen, die den auswählbaren Zustand verwenden, teilen nun mit, wenn ein Element nicht ausgewählt ist, anstatt wenn das Element ausgewählt ist. (#14336)

### Fehlerbehebungen

* Für Windows 11:
  * NVDA zeigt beim Öffnen des Startmenüs die Highlights der Suche an. (#13841)
  * Auf ARM werden x64-Anwendungen nicht mehr als ARM64-Anwendungen erkannt. (#14403)
  * Auf Menüpunkte der Zwischenablage wie z. B. "Element anheften" kann zugegriffen werden. (#14508)
  * In Windows 11 Version 22H2 und neuer ist es wieder möglich, Maus- und Touch-Interaktion zu nutzen, um mit Bereichen wie dem Überlauf-Fenster der Taskleiste und dem Dialogfeld "Öffnen mit" zu interagieren. (#14538, #14539)
* Vorschläge werden beim Eingeben einer @Erwähnung in Microsoft Excel-Kommentaren gemeldet. (#13764)
* In der Standortleiste von Google Chrome werden die Steuerelemente für Vorschläge (zu einer Registerkarte wechseln, Vorschlag entfernen, etc.) nun mitgeteilt, wenn sie ausgewählt werden. (#13522)
* Bei der Abfrage von Formatierungsinformationen werden die Farben nun explizit in WordPad oder im Protokoll-Betrachter angezeigt und nicht mehr nur "Standardfarbe". (#13959)
* In Mozilla Firefox funktioniert die Aktivierung der Schaltfläche "Optionen anzeigen" auf GitHub-Ausgabeseiten nun zuverlässig. (#14269)
* Die Steuerelemente für die Datumsauswahl im Dialogfeld für die Erweiterte Suche von Outlook 2016 / 365 teilt nun deren Bezeichnung und Wert mit. (#12726)
* ARIA-Switch-Steuerelemente werden in Firefox, Chrome und Edge jetzt tatsächlich als Schalter und nicht mehr als Kontrollkästchen angezeigt. (#11310)
* NVDA teilt automatisch den Sortierstatus einer HTML-Tabellenspaltenüberschrift mit, wenn dieser durch Drücken einer inneren Schaltfläche geändert wird. (#10890)
* Der Name eines Wahrzeichens oder einer Region wird immer automatisch gesprochen, wenn man von außen nach innen springt, indem man die Schnellnavigation oder den Fokus im Lesemodus verwendet. (#13307)
* Wenn der Signalton oder die Ansage von "Groß" für Großbuchstaben mit verzögerten Zeichen-Beschreibungen aktiviert ist, wird nicht mehr zweimal angesagt in NVDA "Groß" oder gibt hierbei keinen Signalton mehr doppelt wieder. (#14239)
* Steuerelemente in Tabellen in Java-Anwendungen werden jetzt von NVDA präziser angezeigt. (#14347)
* Einige Einstellungen werden nicht mehr unerwartet unterschiedlich sein, wenn sie mit mehreren Profilen verwendet werden. (#14170)
  * Die folgenden Einstellungen wurden berücksichtigt:
    * Zeileneinrückungen in den Einstellungen für die Dokument-Formatierungen.
    * Zellrahmen in den Einstellungen für die Dokument-Formatierungen
    * Anzeigen von Benachrichtigungen in Braille-Einstellungen
    * Braille-Kopplung in den Braille-Einstellungen
  * In einigen seltenen Fällen können diese in Profilen verwendeten Einstellungen bei der Installation dieser NVDA-Version unerwartet geändert werden.
  * Bitte überprüfen Sie diese Optionen in Ihren Profilen, nachdem Sie NVDA auf diese Version aktualisiert haben.
* Emojis sollten nun in mehreren Sprachen mitgeteilt werden. (#14433)
* Das Vorhandensein einer Anmerkung fehlt auf der braillezeile bei einigen Elementen nicht mehr. (#13815)
* Ein Problem wurde behoben, bei dem Änderung in der Konfiguration nicht korrekt gespeichert wurden, wenn zwischen einer "Standard"-Option und dem Wert der "Standard"-Option gewechselt wurde. (#14133)
* Bei der Konfiguration von NVDA wird immer mindestens eine Taste als NVDA-Taste definiert. (#14527)
* Wenn Sie das NVDA-Menü über den Infobereich aufrufen, schlägt NVDA kein ausstehendes Update mehr vor, wenn kein Update verfügbar ist. (#14523)
* Die verbleibende, verstrichene und gesamte Zeit wird nun für Audiodateien, die mehr als einen Tag lang sind, in Foobar2000 korrekt angezeigt. (#14127)
* In Web-Browsern wie Google Chrome und Mozilla Firefox werden Warnmeldungen, z. B. zum Herunterladen von Dateien, nicht nur gesprochen, sondern auch in Braille-Schrift angezeigt. (#14562)
* Fehler beim Navigieren zur ersten und letzten Spalte in einer Tabelle in Firefox behoben. (#14554)
* Wenn NVDA mit dem Parameter `--lang=Windows` gestartet wird, ist es wieder möglich, den Dialog Allgemeine Einstellungen von NVDA zu öffnen. (#14407)
* Beim Umblättern einer Seite im Kindle für PC unterbricht NVDA das Vorlesen nicht mehr. (#14390)

### Änderungen für Entwickler

Hinweis: Dies ist eine Version, die die Kompatibilität der API für NVDA-Erweiterungen verändert.
Die NVDA-Erweiterungen müssen erneut getestet werden und die Manifest-Datei muss aktualisiert werden.
Bitte lesen Sie das [Entwicklerhandbuch](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) für Informationen über den Abkündigungs- und Entfernungsprozess für die API in NVDA.

* Die Systemtests sollten nun erfolgreich sein, wenn diese lokal auf nicht-englischsprachigen Systemen ausgeführt werden. (#13362)
* In Windows 11 auf ARM werden x64-Anwendungen nicht mehr als ARM64-Anwendungen erkannt. (#14403)
* Es ist nicht mehr notwendig, `SearchField` und `SuggestionListItem` `UIA` `NVDAObjects` in neuen UIA-Szenarien zu verwenden, in denen automatisch Suchvorschläge mitgeteilt werden und in denen die Eingabe über UIA mit dem Muster `ControllerFor` ausgesetzt wurde.
Diese Funktionalität ist nun generisch über `behaviours.EditableText` bzw. die Basis `NVDAObject` verfügbar. (#14222)
* Wenn die UIA-Debug-Protokollierungskategorie aktiviert ist, wird jetzt deutlich mehr Protokollierung für UIA-Ereignishandler und Dienstprogramme erzeugt. (#14256)
* Die NVDAHelper-Build-Standards wurden aktualisiert. (#13072)
  * Verwendet nun den C++20-Standard, vorher war es C++17.
  * Nun wird der Compiler-Flag `/permissive-` verwendet, das das permissive Verhalten deaktiviert und die Compiler-Optionen "/Zc" für strikte Konformität gesetzt.
* Einige Plugin-Objekte (z. B. Treiber und NVDA-Erweiterungen) haben nun eine informativere Beschreibung in der NVDA-Python-Konsole. (#14463)
* NVDA kann nun vollständig mit Visual Studio 2022 kompiliert werden und benötigt keine Visual Studio 2019 Build-Tools mehr.  (#14326)
* Detailliertere Protokollierung für Einfrierungen von NVDA zur Unterstützung der Fehlersuche. (#14309)
* Die Singleton-Klasse `braille._BgThread` wurde durch `hwIo.ioThread.IoThread` ersetzt. (#14130)
  * Eine einzelne Instanz `hwIo.bgThread` (im NVDA-Kern) dieser Klasse bietet Hintergrund-Informationen für Ein- und Ausgaben bei Thread-sichere Braillezeilen-Treiber.
  * Diese neue Klasse ist nicht als Singleton konzipiert, Entwickler von NVDA-Erweiterungen sind aufgefordert, ihre eigene Instanz zu verwenden, wenn sie Hardware-Eingabe bzw. -Ausgabe verwenden.
* Die Prozessor-Architektur des Computers kann über das Attribut `winVersion.WinVersion.processorArchitecture` abgefragt werden (#14439)
* Es wurden neue Skripte hinzugefügt. (#14503)
  * `inputCore.decide_executeGesture`
  * `tones.decide_beep`
  * `nvwave.decide_playWaveFile`
  * `braille.pre_writeCells`
  * `braille.filter_displaySize`
  * `braille.decide_enabled`
  * `braille.displayChanged`
  * `braille.displaySizeChanged`
* Es ist möglich, useConfig bei unterstützten Einstellungen für einen Synthesizer-Treiber auf False zu setzen. (#14601)

#### API-Änderungen

Dies sind die neuen API-Änderungen.
Bitte öffnen Sie ein Ticket auf GitHub, wenn eine NVDA-Erweiterung ein Problem mit der Aktualisierung auf die neue API hat.

* Die Konfigurationsspezifikation wurde geändert, Schlüssel wurden entfernt oder geändert:
  * Im Abschnitt `[documentFormatting]` (#14233):
    * `reportLineIndentation` speichert einen INT-Wert (0 bis 3) anstelle eines booleschen Wertes
    * `reportLineIndentationWithTones` wurde entfernt.
    * `reportBorderStyle` und `reportBorderColor` wurden entfernt und sind durch `reportCellBorders` ersetzt worden.
  * Im Abschnitt `[braille]` (#14233):
    * `noMessageTimeout` wurde entfernt und durch einen Wert für `showMessages` ersetzt.
    * `noMessageTimeout` wurde entfernt und durch einen Wert für `showMessages` ersetzt. a`messageTimeout` kann nicht mehr den Wert 0 annehmen und wurde durch einen Wert für `showMessages` ersetzt.
    * `autoTether` wurde entfernt; `tetherTo` kann nun stattdessen den Wert "auto" annehmen.
  * Im Abschnitt `[keyboard]` (#14528):
    * `useCapsLockAsNVDAModifierKey`, `useNumpadInsertAsNVDAModifierKey`, `useExtendedInsertAsNVDAModifierKey` wurden entfernt.
    Sie wurden durch `NVDAModifierKeys` ersetzt.
* Die Klasse `NVDAHelper.RemoteLoader64` wurde ersatzlos entfernt. (#14449)
* Die folgenden Funktionen in `winAPI.sessionTracking` werden ersatzlos entfernt. (#14416, #14490)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`
* Es ist nicht mehr möglich den Braille-Handler durch die Einstellung `braille.handler.enabled` einzuschalten.
Um den Braille-Handler programmatisch zu deaktivieren, registrieren Sie einen Handler für `braille.handler.decide_enabled`. (#14503)
* Es ist nicht mehr möglich, die Anzeigegröße des Handlers durch definieren von `braille.handler.displaySize` zu aktualisieren.
Um `displaySize` programmatisch zu aktualisieren, registrieren Sie einen Handler für `braille.handler.filter_displaySize`.
Siehe `brailleViewer` für ein Beispiel, wie das erledigt werden kann. (#14503)
* Es gab Änderungen bei der Verwendung von `addonHandler.Addon.loadModule`. (#14481)
  * `loadModule` erwartet nun einen Punkt als Trennzeichen, statt eines Backslashs.
  Zum Beispiel "lib.example" anstelle von "lib\example".
  * `loadModule` löst nun eine Exception aus, wenn ein Modul nicht geladen werden kann oder Fehler aufweist, anstatt `None` zurückzugeben, ohne Informationen über die Ursache zu geben.
* Die folgenden Symbole wurden aus der Datei `appModules.foobar2000` entfernt und nicht direkt ersetzt. (#14570)
  * `statusBarTimes`
  * `parseIntervalToTimestamp`
  * `getOutputFormat`
  * `getParsingFormat`
* Die Folgenden sind keine Singletons mehr - deren get-Methode wurde entfernt.
Die Verwendung von `Example.get()` ist jetzt `Example()`. (#14248)
  * `UIAHandler.customAnnotations.CustomAnnotationTypesCommon`
  * `UIAHandler.customProps.CustomPropertiesCommon`
  * `NVDAObjects.UIA.excel.ExcelCustomProperties`
  * `NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes`

#### Veraltete Funktionen

* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA` ist veraltet und es wird von der Verwendung abgeraten. (#14047)
* `config.addConfigDirsToPythonPackagePath` wurde verschoben.
Verwenden Sie stattdessen `addonHandler.packaging.addDirsToPythonPackagePath`. (#14350)
* `braille.BrailleHandler.TETHER_*` sind veraltet.
Verwenden Sie stattdessen `configFlags.TetherTo.*.value`. (#14233)
* `utils.security.postSessionLockStateChanged` ist veraltet.
Verwenden Sie stattdessen `utils.security.post_sessionLockStateChanged`. (#14486)
* `NVDAObject.hasDetails`, `NVDAObject.detailsSummary`, `NVDAObject.detailsRole` sind veraltet.
Verwenden Sie stattdessen `NVDAObject.annotations`. (#14507)
* `keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS` ist veraltet und wird nicht direkt ersetzt.
Verwenden Sie stattdessen die Klasse `config.configFlags.NVDAKey`. (#14528)
* `gui.MainFrame.evaluateUpdatePendingUpdateMenuItemCommand` ist veraltet.
Verwenden Sie stattdessen `gui.MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand`. (#14523)

## 2022.4

Diese Version enthält mehrere neue Tastenkombinationen, darunter die Tastenbefehle für das Vorlesen von Tabellen.
Das Benutzerhandbuch wurde um den Abschnitt "Schnellstartanleitung" erweitert.
Außerdem wurden mehrere Fehler behoben.

Die Sprachausgabe eSpeak und der Braille-Übersetzer LibLouis wurden aktualisiert.
Es gibt neue Braille-Tabellen für Chinesisch, Schwedisch, Luganda und Kinyarwanda.

### Neue Features

* Dem Benutzerhandbuch wurde ein Abschnitt "Schnellstartanleitung" hinzugefügt. (#13934)
* Es wurde ein neuer Tastenbefehl eingeführt, um das Tastaturkürzel des aktuellen Fokus zu überprüfen. (#13960)
  * Desktop: `Umschalt+Nummernblock 2`.
  * Laptop: `NVDA+Strg+Umschalt+Punkt`.
* Es wurden neue Tastenbefehle eingeführt, um den NVDA-Cursor seitenweise zu navigieren, sofern dies von der Anwendung unterstützt wird. (#14021)
  * Zur vorherigen Seite wechseln:
    * Desktop: `NVDA+Seite nach oben`.
    * Laptop: `NVDA+Umschalt+Seite nach oben`.
  * Zur nächsten  Seite wechseln:
    * Desktop: `NVDA+Seite nach unten`.
    * Laptop: `NVDA+Umschalt+Seite nach unten`.
* Die folgenden Tabellenbefehle wurden hinzugefügt. (#14070)
  * Aktuelle Spalte vorlesen: `NVDA+Strg+Alt+Pfeiltaste nach unten`
  * Aktuelle Zeile vorlesen: `NVDA+Strg+Alt+Pfeiltaste nach rechts`
  * Gesamte Spalte vorlesen `NVDA+Strg+Alt+Pfeiltaste nach oben`
  * Gesamte Zeile vorlesen: `NVDA+Strg+Alt+Pfeiltaste nach links`
* Microsoft Excel über UIA: NVDA teilt nun mit, sobald Sie eine Tabelle innerhalb einer Tabelle verlassen. (#14165)
* Das Mitteilen von Überschriften in Tabellen können nun für Zeilen und Spalten getrennt konfiguriert werden. (#14075)

### Änderungen

* Die Sprachausgabe eSpeak NG wurde aktualisiert auf 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Die Ansage von lateinischen Schriftzeichen bei der Verwendung von Mandarin wurde korrigiert. (#12952, #13572, #14197)
* Der Braille-Übersetzer LibLouis wurde aktualisiert auf [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Braille-Tabellen hinzugefügt:
    * Chinesische Braille-Schrift (vereinfachte chinesische Schriftzeichen)
    * Literatur-Braille (Kinyarwanda)
    * Literatur-Braille-Schrift (Luganda)
    * Schwedische basisschrift
    * Schwedische Vollschrift
    * Schwedische Kurzschrift
    * Chinesisch (China, Mandarin) Aktuelles Braille-System (ohne Laute) (#14138)
* NVDA erfasst nun die Architektur des Betriebssystems als Teil der Benutzer-Statistiken. (#14019)

### Fehlerbehebungen

* Bei der Aktualisierung von NVDA mit dem Windows Package Manager CLI (aka winget) wird eine freigegebene Version von NVDA nicht mehr immer als neuer als die installierte Alpha-Version behandelt. (#12469)
* NVDA zeigt nun Gruppenfelder in Java-Anwendungen korrekt an. (#13962)
* Der System-Cursor folgt dem vorgelesenen Text während "Alles Lesen" in Anwendungen wie Bookworm, WordPad oder dem NVDA-Protokollbetrachter. (#13420, #9179)
* In Programmen, die UIA verwenden, werden teilweise angehakte Kontrollkästchen korrekt mitgeteilt. (#13975)
* Verbesserte Leistung und Stabilität in Microsoft Visual Studio, Windows Terminal und anderen auf UIA-basierenden Anwendungen. (#11077, #11209)
  * Diese Anpassungen  gelten für Windows 11 Version 22H2 bzw. 2022 (Sun Valley 2).
  * Ausgewählte Registrierung für UIA-Ereignisse und Eigenschaftsänderungen nun standardmäßig aktiviert.
* Text vorlesen, Braille-Ausgabe und Passwort-Unterdrückung funktionieren jetzt wie erwartet im eingebetteten Windows-Terminal-Steuerelement in Visual Studio 2022. (#14194)
* NVDA kann nun mit mehreren Monitoren umgehen, die verschiedene Auflösungen verwenden.
Es gibt mehrere Lösungen für die Verwendung einer DPI-Einstellung von mehr als 100 % oder mehrerer Monitore.
Bei älteren Windows-Versionen als Windows 10 Version 1809 können weiterhin Probleme auftreten.
Damit diese Anpassungen  funktionieren, müssen die Anwendungen, mit denen NVDA interagiert, ebenfalls DPI-kompatibel sein.
Beachten Sie, dass es immer noch bekannte Probleme mit Google Chrome und Microsoft Edge gibt. (#13254)
  * Visuelle Hervorhebungsrahmen sollten nun in den meisten Anwendungen korrekt platziert werden. (#13370, #3875, #12070)
  * Die Touchscreen-Interaktionen sollte nun für die meisten Anwendungen präzise sein. (#7083)
  * Die Mausverfolgung sollte nun für die meisten Anwendungen funktionieren. (#6722)
* Änderungen der Ausrichtung (Querformat/Hochformat) werden nun korrekt ignoriert, wenn es keine Änderung gibt (z. B. beim Umschalten des Monitors). (#14035)
* NVDA teilt mit, dass das Ziehen von Elementen auf dem Bildschirm an Stellen wie der Neuanordnung von Kacheln im Startmenü von Windows 10 und virtuellen Desktops in Windows 11 möglich ist. (#12271, #14081)
* In den erweiterten Einstellungen wird die Option "Bei protokollierten Fehlern einen Signalton wiedergeben" nun korrekt auf den Standardwert zurückgesetzt, wenn die Schaltfläche "Standardwerte wiederherstellen" betätigt wird. (#14149)
* NVDA kann nun Text mit dem Tastaturkürzel `NVDA+F10` in Java-Anwendungen auswählen. (#14163)
* NVDA bleibt nicht mehr in einem Menü hängen, wenn Sie in Microsoft Teams mit den Pfeiltasten nach oben oder unten durch die Unterhaltungen gehen. (#14355)

### Änderungen für Entwickler

Bitte lesen Sie das [Entwicklerhandbuch](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) für Informationen über den NVDA-API-Abkündigungs- und Entfernungsprozess.

* Die [Mailingliste für NVDA-API-Ankündigungen](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) wurde ins Leben gerufen. (#13999)
* NVDA verarbeitet keine `TextChange`-Ereignisse mehr für die meisten UIA-Anwendungen, da diese extrem negative Auswirkungen auf die Leistung haben. (#11002, #14067)

#### Veraltete Funktionen

* `core.post_windowMessageReceipt` ist veraltet, verwenden Sie stattdessen `winAPI.messageWindow.pre_handleWindowMessage`.
* `winKernel.SYSTEM_POWER_STATUS` ist veraltet und es wird von der Verwendung abgeraten, dies wurde nach `winAPI._powerTracking.SystemPowerStatus` verschoben.
* `winUser.SM_*`-Konstanten sind veraltet, verwenden Sie stattdessen `winAPI.winUser.constants.SystemMetrics`.

## 2022.3.3

Dies ist eine kleinere Version, die Fehler in 2022.3.2, 2022.3.1 und 2022.3 behebt.
Damit wird auch ein Sicherheitsproblem gelöst.

### Sicherheitsproblembehebungen

* Verhindert den möglichen Systemzugang (z. B. durch die Python-Konsole in NVDA) für nicht authentifizierte Benutzer. ([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Fehlerbehebungen

* Wenn NVDA beim Sperren einfriert, erlaubt NVDA den Zugriff auf den Desktop des Benutzers, während der Windows-Sperrbildschirm angezeigt wird. (#14416)
* Fehler behoben, bei dem NVDA sich nicht korrekt verhält, wenn es beim Sperren einfriert, als ob das Gerät noch gesperrt wäre. (#14416)
* Zugänglichkeitsprobleme mit dem Windows-Prozess "PIN vergessen" und der Windows-Update-/Installationserfahrung wurden behoben. (#14368)
* Fehler bei der NVDA-Installation in einigen Windows-Umgebungen, z. B. Windows Server, behoben. (#14379)

### Änderungen für Entwickler

#### Veraltete Funktionen

* `utils.security.isObjectAboveLockScreen(obj)` ist veraltet, verwenden Sie stattdessen `obj.isBelowLockScreen`. (#14416)
* Die folgenden Funktionen in `winAPI.sessionTracking` sind veraltet und werden in 2023.1 entfernt. (#14416)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`

## 2022.3.2

Dies ist eine kleinere Version, die Probleme mit 2022.3.1 behebt und eine Sicherheitslücke schließt.

### Sicherheitsproblembehebungen

* Verhindert den möglichen Zugriff auf Systemebene für nicht authentifizierte Benutzer. ([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Fehlerbehebungen

* Behebt ein Problem aus 2022.3.1, bei der bestimmte Funktionen während der Anzeige von Sicherheitsmeldungen deaktiviert wurden. (#14286)
* Behebt ein Problem aus 2022.3.1, bei der bestimmte Funktionen nach der Anmeldung deaktiviert wurden, sobald NVDA auf dem Sperrbildschirm gestartet wurde. (#14301)

## 2022.3.1

Dies ist eine kleinere Version, die mehrere Sicherheitsprobleme behebt.
Bitte melden Sie Sicherheitsprobleme umgehend an <info@nvaccess.org>.

### Sicherheitsproblembehebungen

* Ein Exploit wurde behoben, durch den es möglich war, von Benutzer- zu Systemrechten zu gelangen. ([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Es wurde ein Sicherheitsproblem behoben, das den Zugriff auf die Python-Konsole auf dem Sperrbildschirm über eine Laufbedingung beim NVDA-Start ermöglichte. ([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Es wurde ein Problem behoben, bei dem der Text des Sprachausgaben-Betrachters beim Sperren von Windows zwischengespeichert wurde. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Fehlerbehebungen

* Verhindert, dass ein nicht authentifizierter Benutzer die Einstellungen für die Anzeige von Sprach- und Braille-Ausgaben auf dem Sperrbildschirm aktualisiert. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Ein großer Teil dieser Version wurde von der NVDA-Entwicklergemeinschaft beigesteuert. 
Dazu gehören verzögerte Zeichenbeschreibungen und eine verbesserte Unterstützung der Windows-Konsole.

Diese Version enthält auch mehrere Fehlerbehebungen.
Insbesondere stürzen aktuelle Versionen von Adobe Acrobat bzw. Adobe Reader beim Lesen von PDF-Dokumenten nicht mehr  ab.

ESpeak wurde aktualisiert, wodurch drei neue Sprachen hinzugekommen sind: Belarussisch, Luxemburgisch und Totontepec Mixe.

### Neue Features

* Im Windows-Konsolen-Host, der von der Eingabeaufforderung, PowerShell und dem Windows-Subsystem für Linux unter Windows 11 Version 22H2 (Sun Valley 2) und neuer verwendet wird:
  * Deutlich verbesserte Leistung und Stabilität. (#10964)
  * Wenn Sie `Strg+F` drücken, um nach Text zu suchen, wird die Position des NVDA-Cursors aktualisiert, um dem gefundenen Begriff zu folgen. (#11172)
  * Die Meldung von eingegebenem Text, der nicht auf dem Bildschirm erscheint (z. B. Kennwörter), ist standardmäßig deaktiviert. Dies kann in den erweiterten NVDA-Einstellungen wieder aktiviert werden. (#11554)
  * Text, der aus dem Bildschirm gescrollt wurde, kann ohne Scrollen des Konsolenfensters nachgelesen werden. (#12669)
  * Ausführlichere Informationen zur Textformatierung sind verfügbar. ([Microsoft Windows-Terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Eine neue Sprachoption wurde hinzugefügt, um Zeichenbeschreibungen nach einer Verzögerung zu lesen. (#13509)
* Eine neue Braille-Option wurde hinzugefügt, mit der festgelegt werden kann, ob beim Vorwärts- bzw. Rückwärtsscrollen der Anzeige die Sprachausgabe unterbrochen werden soll. (#2124)

### Änderungen

* eSpeak NG wurde auf 1.52-dev commit `9de65fcb` aktualisiert. (#13295)
  * Weitere Sprachen hinzugefügt:
    * Belarussisch
    * Luxembourgisch
    * Totontepec Mixe
 Bei Verwendung von UIA für den Zugriff auf Steuerelemente von Microsoft Excel-Tabellenkalkulationen teilt NVDA nun mit, sobald eine Zelle zusammengeführt wird. (#12843)
* Anstatt "hat Details" zu melden, wird, sofern möglich, der Zweck der Details angegeben, zum Beispiel "enthält Kommentar". (#13649)
* Die Installationsgröße von NVDA wird nun im Abschnitt Windows-Programme und -Funktionen angezeigt. (#13909)

### Fehlerbehebungen

* Der Adobe Acrobat bzw. Adobe Reader (64-Bit) stürzt beim Lesen eines PDF-Dokuments nicht mehr ab. (#12920)
  * Bitte beachten Sie, dass die aktuellste Version von Adobe Acrobat bzw. Adobe Reader ebenfalls erforderlich ist, um den Absturz zu vermeiden.
* Die Maßeinheiten von Schriftgrößen sind nun in NVDA übersetzbar. (#13573)
* NVDA ignoriert Java Access Bridge-Ereignisse, bei denen kein Fensterhandle für Java-Anwendungen gefunden werden kann.
Dies verbessert die Leistung für einige Java-Anwendungen, einschließlich IntelliJ IDEA. (#13039)
* Die Mitteilungen ausgewählter Zellen für LibreOffice Calc ist effizienter und führt nicht mehr zu einem Einfrieren von Calc, wenn viele Zellen ausgewählt sind. (#13232)
* Wenn Microsoft Edge unter einem anderen Benutzer ausgeführt wird, ist es (weiterhin) zugänglich. (#13032)
* Wenn die Erhöhung der Geschwindigkeit ausgeschaltet ist, sinkt die Geschwindigkeit von eSpeak nicht mehr zwischen 99 und 100 %. (#13876)
* Behebung eines Fehlers, der das Öffnen von doppelten Dialogfeldern der Tastenbefehle ermöglichte. (#13854)

### Änderungen für Entwickler

* Comtypes auf Version 1.1.11 aktualisiert. (#12953)
* In Builds der Windows-Konsole (`conhost.exe`) mit einem NVDA-API-Level von 2 (`FORMATTED`) oder höher, wie sie in Windows 11 Version 22H2 (Sun Valley 2) enthalten sind, wird nun standardmäßig UIA verwendet. (#10964)
  * Dies kann durch Ändern der Einstellung der Unterstützung für Windows-Konsolen in den erweiterten Einstellungen von NVDA außer Kraft gesetzt werden.
  * Um die NVDA-API-Level Ihrer Windows-Konsole zu ermitteln, setzen Sie "Windows-Konsolenunterstützung" auf "UIA, wenn verfügbar" und überprüfen Sie dann das Protokoll mit NVDA+F1, das von einer laufenden Windows-Konsoleninstanz geöffnet wurde.
* Die virtuelle Chromium-Ansicht wird nun auch dann geladen, wenn das Dokumentobjekt den MSAA `STATE_SYSTEM_BUSY` hat, der über IA2 ausgesetzt ist. (#13306)
* Für die Verwendung mit experimentellen Funktionen in NVDA wurde ein Konfigurationsspezifikationstyp `featureFlag` erstellt. Siehe `devDocs/featureFlag.md` für weitere Informationen. (#13859)

#### Veraltete Funktionen

Für 2022.3 wurden keine Änderungen an der API vorgenommen.

## 2022.2.4

Dies ist ein Patch-Release zur Behebung einer Sicherheitslücke.

### Fehlerbehebungen

* Es wurde ein Exploit behoben, bei dem es möglich war, die Python-Konsole von NVDA über die Protokollanzeige auf dem Sperrbildschirm zu öffnen.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Dies ist ein Patch-Release, um einen versehentlichen API-Fehler zu beheben, der sich in 2022.2.1 einschlich.

### Fehlerbehebungen

* Ein Fehler wurde behoben, bei dem NVDA beim Aufrufen eines geschützten Desktops nicht "Geschützter Desktop" ausgab.
Dies führte dazu, dass NVDA Remote keine geschützten Desktops mehr erkannte. (#14094)

## 2022.2.2

Dieser Patch behebt einen Fehler, der in Version 2022.2.1 beim Öffnen der Tastenbefehle auftrat.

### Fehlerbehebung

* Ein Fehler wurde behoben, bei dem Tastenbefehle nicht immer funktionierten. (#14065)

## 2022.2.1

Dies ist eine kleinere Version zur Behebung einer Sicherheitslücke.
Bitte melden Sie Sicherheitsprobleme umgehend an <info@nvaccess.org>.

### Sicherheitsproblembehebungen

* Es wurde ein Exploit behoben, durch den es möglich war, die Python-Konsole über den Sperrbildschirm zu starten. (GHSA-rmq3-vvhq-gp32)
* Es wurde ein Exploit behoben, bei dem es möglich war, den Sperrbildschirm durch die Objekt-Navigation zu umgehen. (GHSA-rmq3-vvhq-gp32)

### Änderungen für Entwickler

#### Veraltete Funktionen

Die veralteten Funktionen sind derzeit nicht zur Entfernung  vorgesehen.
Die veralteten Aliasnamen werden bis auf weiteres beibehalten.
Bitte testen Sie die neue API und teilen Sie uns Ihr Feedback mit.
Autoren von NVDA-Erweiterungen sollten bitte ein Ticket bei GitHub einreichen, wenn diese Änderungen dazu führen, dass die API nicht mehr Ihren Anforderungen entspricht.

* `appModules.lockapp.LockAppObject` sollte durch `NVDAObjects.lockscreen.LockScreenObject` ersetzt werden. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS` sollte durch `utils.security.getSafeScripts()` ersetzt werden. (GHSA-rmq3-vvhq-gp32)

## 2022.2

Diese Version enthält viele Fehlerbehebungen.
Vor allem für Java-basierte Anwendungen, Braillezeilen und Windows-Funktionen gibt es erhebliche Verbesserungen.

Neue Befehle für die Tabellennavigation wurden eingeführt.
Unicode CLDR wurde aktualisiert.
LibLouis wurde aktualisiert und enthält eine neue deutsche Braille-Tabelle.

### Neue Features

* Unterstützung für die Interaktion mit Microsoft Loop-Komponenten in Microsoft Office-Produkten. (#13617)
* Es wurden neue Befehle für die Tabellen-Navigation hinzugefügt. (#957)
 * `Strg+Alt+Pos1/Ende`, um zur ersten/letzten Spalte zu springen.
 * `Strg+Alt+Seite nach oben/unten`, um zur ersten/letzten Zeile zu springen.
* Ein nicht zugewiesenes Skript zum Durchlaufen der Sprach- und Dialektwechselmodi wurde hinzugefügt. (#10253)

### Änderungen

* NSIS wurde auf Version 3.08 aktualisiert. (#9134)
* CLDR wurde auf Version 41.0 aktualisiert. (#13582)
* LibLouis-Braille-Übersetzer wurde auf Version [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0) aktualisiert. (#13775)
  * Neue Braille-Tabelle: Deutsche Kurzschrift (ausführlich)
* Neue Rolle für Steuerelemente "Beschäftigt-Status" hinzugefügt. (#10644)
* NVDA teilt nun mit, sobald eine Aktion in NVDA nicht ausgeführt werden konnte. (#13500)
  * Dies gilt beim:
    * Verwenden der NVDA Windows-Store-Version.
    * Lesen in einem geschützten Kontext.
    * Warten auf eine Antwort eines modalen Dialogfeldes.

### Fehlerbehebungen

* Für Java-basierte Anwendungen:
  * NVDA teilt nun den schreibgeschützten Zustand mit. (#13692)
  * NVDA teilt nun den deaktivierten oder aktivierten Status korrekt mit. (#10993)
  * NVDA gibt nun Tastenkombinationen mit F-Tasten aus. (#13643)
  * NVDA teilt nun die Fortschrittsbalken entweder durch Signaltöne oder über die Sprachausgabe mit. (#13594)
  * NVDA entfernt nicht mehr fälschlicherweise Text aus Widgets, wenn diese dem Benutzer angezeigt werden. (#13102)
  * NVDA teilt nun den Zustand von Umschalt-Tasten mit. (#9728)
  * NVDA erkennt nun das Fenster in einer Java-Anwendung mit mehreren Fenstern. (#9184)
  * NVDA zeigt nun Informationen der Position für Registerkarten an. (#13744)
* Braille:
  * Braille-Ausgabe beim Navigieren in bestimmten Texten in Mozilla-RichEdit-Steuerelementen behoben, z. B. beim Verfassen einer Nachricht in Thunderbird. (#12542)
  * Wenn die Braillezeile automatisch verbunden wird und die Maus bei aktivierter Mausverfolgung bewegt wird,
  Befehle für die Textanzeige aktualisieren nun die Ausgabe auf der Braillezeile mit dem vorgelesenen Inhalt. (#11519)
  * Es ist nun möglich, die Braillezeile nach der Verwendung von Befehlen für die Textanzeige durch den Inhalt zu navigieren. (#8682)
* Das NVDA-Installationsprogramm kann fortan von Verzeichnissen mit Sonderzeichen aus gestartet werden. (#13270)
* In Firefox teilt NVDA keine Elemente auf Webseiten mehr mit, wenn die Attribute aria-rowindex, aria-colindex, aria-rowcount oder aria-colcount ungültig sind. (#13405)
* Der Cursor wechselt nicht mehr die Zeile oder Spalte, wenn Sie die Tabellennavigation verwenden, um durch zusammengeführte Zellen zu navigieren. (#7278)
* Beim Lesen nicht-interaktiver PDF-Dateien in Adobe Reader werden nun Typ und Zustand von Formularfeldern (z. B. Kontrollkästchen und Optionsfelder) mitgeteilt. (#13285)
* Die Funktion "Konfiguration auf Standard-Einstellungen zurücksetzen" ist nun im NVDA-Menü im geschützten Modus verfügbar. (#13547)
* Gesperrte Maus-Tasten werden beim Beenden von NVDA wieder entsperrt, vorher blieb die Maus-Taste gesperrt. (#13410)
* In Visual Studio werden nun Zeilennummern mitgeteilt. (#13604)
  * Beachten Sie, dass die Anzeige von Zeilennummern in Visual Studio und NVDA aktiviert sein muss, damit die Zeilennummernanzeige funktioniert.
* In Visual Studio werden die Zeileneinrückungen nun korrekt mitgeteilt. (#13574)
* NVDA teilt in den neuen Versionen von Windows 10 und 11 erneut Details zu den Suchergebnissen im Startmenü mit. (#13544)
* Im Rechner in Windows 10 und 11 Version 10.1908 und neuer,
teilt NVDA die Ergebnisse mit, wenn weitere Befehle gedrückt werden, z. B. Befehle aus dem wissenschaftlichen Modus. (#13383)
* In Windows 11 ist es wieder möglich, mit Elementen der Benutzeroberfläche zu navigieren und zu interagieren,
wie z. B. die Taskleiste und die Task-Ansicht mit Hilfe von Maus- und Touch-Interaktion. (#13506)
* NVDA zeigt nun den Inhalt der Statusleiste in Windows 11 Notepad an. (#13388)
* Die Hervorhebung von Navigationsobjekten wird nun sofort nach Aktivierung der Funktion angezeigt. (#13641)
* Das Auslesen einspaltiger Elemente in Listenansichten wurde behoben. (#13659, #13735)
* Automatische Sprachumschaltung von eSpeak für Englisch und Französisch wurde behoben, falls nicht möglich auf britisches Englisch und Französisch (Frankreich). (#13727)
* Automatische Sprachumschaltung in OneCore wurde behoben, wenn versucht wird, zu einer zuvor installierten Sprache zu wechseln. (#13732)

### Änderungen für Entwickler

* Die Kompilierung von NVDA-Abhängigkeiten mit Visual Studio 2022 (17.0) wird jetzt unterstützt.
Für Entwicklungs- und Release-Builds wird weiterhin Visual Studio 2019 verwendet. (#13033)
* Beim Abrufen der Anzahl der ausgewählten untergeordneten Elemente über accSelection
wird der Fall, dass eine negative ID des untergeorneten Elements oder ein IDispatch von `IAccessible::get_accSelection` zurückgegeben wird, wird nun korrekt behandelt. (#13277)
* Neue praktische Funktionen `registerExecutableWithAppModule` und `unregisterExecutable` wurden dem Modul `appModuleHandler` hinzugefügt.
Diese können verwendet werden, um ein einzelnes App-Modul mit mehreren ausführbaren Dateien zu verwenden. (#13366)

#### Veraltete Funktionen

Es handelt sich um vorgeschlagene API-Änderungen.
Der veraltete  Teil der API wird bis zur angegebenen Version weiterhin verfügbar sein.
Wenn keine Freigabe angegeben ist, wurde der Plan für die Entfernung noch nicht festgelegt.
Beachten Sie, dass die Roadmap für Umzüge nach bestem Wissen und Gewissen erstellt wurde und sich noch ändern kann.
Bitte testen Sie die neue API und geben Sie uns Rückmeldung.
Autoren von Erweiterungen sollten bitte ein Problem auf GitHub einreichen, falls diese Änderungen dazu führen, dass die API nicht mehr Ihren Anforderungen entspricht.

* `appModuleHandler.NVDAProcessID` ist veraltet, verwenden Sie stattdessen `globalVars.appPid`. (#13646)
* `gui.quit` ist veraltet, verwenden Sie stattdessen `wx.CallAfter(mainFrame.onExitCommand, None)`. (#13498)
  -
* Einige Alias-AppModule sind als veraltet gekennzeichnet.
Code, der von einem dieser Module importiert, sollte stattdessen von dem Ersatzmodul importiert werden. (#13366)

| Entfernter Modulname |Ersatzmodul|
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

Diese Version enthält wichtige Verbesserungen der UIA-Unterstützung für Microsoft Office.
Für Microsoft Office 16.0.15000 und neuer unter Windows 11 verwendet NVDA standardmäßig UIA für den Zugriff auf Dokumente in Microsoft Word.
Dies stellt eine erhebliche Leistungsverbesserung gegenüber dem älteren Objektmodell-Zugriff dar.

Verbesserungen bei Braillezeilen-Treibern, darunter Seika Notetaker, Papenmeier und HID-Braille.
Des Weiteren gibt es verschiedene Windows 11 Fehlerbehebungen für Apps wie Rechner, Konsole, Terminal, Mail und Emoji-Panel.

Die Sprachausgabe eSpeak-NG und der braille-Übersetzer LibLouis wurden aktualisiert und liblouis wurde um neue japanische, deutsche und katalanische Braillen-Tabellen ergänzt.

Hinweis:

 * Diese Version beeinträchtigt die Kompatibilität mit bestehenden Erweiterungen!

### Neue Features

* Unterstützung für die Mitteilung von Notizen in Microsoft Excel mit aktivierter UIA unter Windows 11. (#12861)
* In neueren Builds von Microsoft Word über UIA unter Windows 11 werden Lesezeichen, Entwurfskommentare und Kommentare nun sowohl mit der Sprachausgabe als auch in Braille mitgeteilt. (#12861)
* Der neue Kommandozeilen-Parameter `--lang` erlaubt das Überschreiben der konfigurierten NVDA-Sprache. (#10044)
* NVDA warnt nun vor unbekannten Kommandozeilen-Parametern, die von keiner Erweiterung verwendet werden. (#12795)
* In Microsoft Word, auf das über UIA zugegriffen wird, verwendet NVDA nun den mathPlayer, um mathematische Gleichungen in Office zu lesen und zu navigieren. (#12946)
  * Damit dies funktioniert, müssen Sie Microsoft Word 365 / 2016 Build 14326 oder neuer verwenden. 
  * MathType-Gleichungen müssen auch manuell in Office-Mathematik umgewandelt werden, indem Sie die Gleichungen markieren, das Kontextmenü öffnen und "Gleichungsoptionen", "In Office-Mathematik umwandeln" auswählen.
* Die Meldung "hat Details" und der zugehörige Befehl zum Zusammenfassen der Detailbeziehung wurden aktualisiert und funktionieren nun auch im Fokus-Modus. (#13106)
* Seika Notetaker kann nun automatisch erkannt werden, wenn es über USB und Bluetooth verbunden ist. (#13191, #13142)
  * Dies betrifft die folgenden Geräte: MiniSeika (mit 16 und 24 Modulen), V6 und V6Pro (mit 40 Modulen).
  * Die manuelle Auswahl des Bluetooth-COM-Ports wird nun ebenfalls unterstützt.
* Es wurde ein Befehl zum Umschalten des Braille-Betrachters hinzugefügt, allerdings gibt es keinen standardmäßig zugehörigen Tastenbefehl. (#13258)
* Befehle zum gleichzeitigen Umschalten mehrerer Modifikatoren mit einer Braillezeile hinzugefügt (#13152)
* Das Dialogfeld "Sprachwörterbuch" verfügt nun über eine Schaltfläche "Alles entfernen", mit der ein ganzes Wörterbuch geleert werden kann. (#11802)
* Unterstützung für den Rechner unter Windows 11 hinzugefügt. (#13212)
* In Microsoft Word bei aktivierter UIA unter Windows 11 können nun Zeilennummern und Abschnittsnummern mitgeteilt werden. (#13283, #13515)
* Für Microsoft Office 16.0.15000 und neuer unter Windows 11 verwendet NVDA standardmäßig UIA für den Zugriff in dokumenten in Microsoft Word, was eine erhebliche Leistungsverbesserung gegenüber dem älteren Objektmodell-Zugriff bedeutet. (#13437)
 * Dies gilt sowohl für Dokumente in Microsoft Word selbst als auch beim Lesen der Nachrichten und die Erstellung von Nachrichten in Microsoft Outlook. 

### Änderungen

* Espeak-ng wurde auf 1.51-dev commit `7e5457f91e10` aktualisiert. (#12950)
* Der Braille-Übersetzer LibLouis wurde auf Version [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0) aktualisiert. (#13141, #13438)
  * Neue Braille-Tabellen hinzugefügt: Japanisches Literatur-Braille (Kantenji).
  * Neue Deutsche Computerbraille-Tabelle für 6-Punkt-Darstellung hinzugefügt.
  * Katalanische Vollschrift hinzugefügt. (#13408)
* NVDA teilt nun Auswahl und zusammengeführte Zellen in LibreOffice Calc 7.3 und neuer mit. (#9310, #6897)
* Unicode Common Locale Data Repository (CLDR) wurde auf 40.0 aktualisiert. (#12999)
* `NVDA+Nummernblock Komma` teilt standardmäßig die Position des Cursor oder des fokussierten Objekts mit. (#13060)
* `NVDA+Umschalt+Nummernblock Komma` teilt die Position des NVDA-Cursors mit. (#13060)
* Standard-Tastenbefehle für das Umschalten von NVDA-Tasten für Braillezeilen von Freedom Scientific hinzugefügt (#13152)
* Das Wort "Grundlinie" wird nicht mehr über den Befehl zur Textformatierung mittels NVDA+F mitgeteilt. (#11815)
* Für die Aktivierung der langen Beschreibungen ist keine Standard-Tastenbefehl mehr zugewiesen. (#13380)
* Für die Zusammenfassung der Details wurde nun standardmäßig der Tastenbefehl NVDA+D zugewiesen. (#13380)
* NVDA muss nach der Installation des MathPlayers neu gestartet werden. (#13486)

### Fehlerbehebungen

* Im Verwaltungsbereich für die Zwischenablage sollte der Fokus nicht mehr verloren gehen, sobald einige Office-Programme geöffnet werden. (#12736)
* Auf einem System, auf dem der Benutzer die primäre Maustaste von der linken auf die rechte Maustaste umgestellt hat, ruft NVDA in Anwendungen wie Webbrowsern nicht mehr versehentlich ein Kontextmenü auf, anstatt ein Element zu aktivieren. (#12642)
* Wenn der NVDA-Cursor über das Ende von Textsteuerelementen hinaus bewegt wird, z. B. in Microsoft Word mit UIA, wird nun in mehreren Situationen "unten" korrekt mitgeteilt. (#12808)
* NVDA kann den Anwendungsnamen und die Version für Binärdateien mitteilen, die in system32 abgelegt sind, wenn sie unter der 64-Bit-Version von Windows laufen. (#12943)
* Verbesserte Konsistenz beim Lesen von Ausgaben in Terminal-Anwendungen. (#12974)
  * Beachten Sie, dass in manchen Situationen beim Einfügen oder Löschen von Zeichen in der Mitte einer Zeile die Zeichen nach dem System-Cursor wieder ausgelesen werden können.
* Microsoft Word mit UIA: Überschriften-Schnellnavigation im Blätternmodus bleibt nicht mehr an der letzten Überschrift eines Dokuments hängen, noch wird diese Überschrift in der NVDA-Elementliste doppelt angezeigt. (#9540)
* In Windows 8 und höher kann die Statusleiste des Datei-Explorers nun mit dem Standard-Tastenbefehl NVDA+Ende (Desktop) bzw. NVDA+Umschalt+Ende (Laptop) abgefragt  werden. (#12845)
* Eingehende Nachrichten im Chat von Skype for Business werden wieder mitgeteilt. (#9295)
* NVDA kann bei Verwendung des SAPI5-Synthesizers unter Windows 11 wieder Audio ausblenden. (#12913)
* Im Rechner von Windows 10 zeigt NVDA Beschriftungen für Verlaufs- und Speicherlistenelemente an. (#11858)
* Tastenbefehle und Gesten wie Scrollen und Weiterleiten funktionieren wieder mit HID-Braille-Geräten. (#13228)
* Windows 11 Mail: Nach dem Umschalten des Fokus zwischen Anwendungen beim Lesen einer langen E-Mail bleibt NVDA nicht mehr in einer Zeile der E-Mail hängen. (#13050)
* HID-Braille: Tastenkombinationen (z. B. `Leertaste+Punkt4`) können erfolgreich über die Braillezeile ausgeführt werden. (#13326)
* Ein Problem wurde behoben, bei dem mehrere Einstellungsdialoge gleichzeitig geöffnet werden konnten. (#12818)
* Es wurde ein Problem behoben, bei dem einige Braillezeilen wie Focus Blue nach dem Aufwachen des Computers aus dem Ruhezustand nicht mehr funktionierten. (#9830)
* Das Wort "Grundlinie" wird nicht mehr fälschlicherweise mitgeteilt, sobald die Option für die Mitteilung hoch- und tiefgestellter Zeichen aktiviert ist. (#11078)
* In Windows 11 verhindert NVDA nicht mehr die Navigation im Emoji-Panel, wenn Emojis ausgewählt werden. (#13104)
* Behebt einen Fehler, der bei der Verwendung von Windows-Konsole und Terminal zu Doppelmeldungen führt. (#13261)
* Mehrere Fälle wurden behoben, in denen Listenelemente in 64-Bit-Anwendungen, wie z. B. in Reaper, nicht mitgeteilt werden konnten. (#8175)
* Im Download-Manager in Microsoft Edge wechselt NVDA jetzt automatisch in den Fokus-Modus, sobald das Listenelement mit dem zuletzt getätigten Download den Fokus erhält. (#13221)
* NVDA verursacht bei 64-Bit-Versionen von Notepad++ 8.3 und neuer keinen Absturz mehr. (#13311)
* Der Adobe Reader stürzt nicht mehr beim Start ab, sobald der geschützte Modus von Adobe Reader aktiviert wird. (#11568)
* Ein Fehler wurde behoben, bei dem die Auswahl des Braillezeilen-Treibers von Papenmeier zu einem Absturz in NVDA führte. (#13348)
* In Microsoft Word mit UIA: Seitenzahlen und andere Formatierungen werden nicht mehr fälschlicherweise angezeigt, wenn man von einer leeren Tabellenzelle in eine Zelle mit Inhalt oder vom Ende des Dokuments in einen bestehenden Inhalt wechselt. (#13458, #13459)
* NVDA liest den Seitentitel vor und beginnt automatisch mit dem Lesen, wenn eine Seite in Google Chrome 100 geladen wurde. (#13571)
* NVDA stürzt nicht mehr ab, wenn die NVDA-Konfiguration auf die Standard-Einstellungen zurückgesetzt wird, während die Befehlstasten zum Vorlesen verwendet werden. (#13634)

### Änderungen für entwickler

* Hinweis: Dies ist eine Version, die die Kompatibilität der API für Erweiterungen beeinträchtigt. NVDA-Erweiterungen müssen erneut getestet werden und die Manifest-Datei muss aktualisiert werden.
* Obwohl NVDA immer noch Visual Studio 2019 benötigt, sollten Builds nicht mehr fehlschlagen, sobald eine neuere Version von Visual Studio (z. B. 2022) parallel zu 2019 installiert ist. (#13033, #13387)
* SCons wurde auf Version 4.3.0 aktualisiert. (#13033)
* Py2exe wurde auf Version 0.11.1.0 aktualisiert. (#13510)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` wurde entfernt. Verwenden Sie stattdessen `apiLevel`. (#12955, #12660)
* `TVItemStruct` wurde aus `sysTreeView32` entfernt. (#12935)
* `MessageItem` wurde aus dem App-Modul für Microsoft Outlook entfernt. (#12935)
* Die Konstanten `audioDucking.AUDIODUCKINGMODE_*` sind jetzt eine `DisplayStringIntEnum`. (#12926)
  * sollte durch `AudioDuckingMode.*` ersetzt werden.
  * Verwendungen von `audioDucking.audioDuckingModes` sollten durch `AudioDuckingMode.*.displayString` ersetzt werden
* Die Verwendung der Konstanten `audioDucking.ANRUS_ducking_*` sollte durch `ANRUSDucking.*` ersetzt werden. (#12926)
* Änderungen in `synthDrivers.sapi5` (#12927):
  * Die Verwendung von `SPAS_*` sollte durch `SPAudioState.*` ersetzt werden.
  * Die Verwendung von `constants.SVSF*` sollte durch `SpeechVoiceSpeakFlags.*` ersetzt werden.
    * Hinweis: `SVSFlagsAsync` sollte durch `SpeechVoiceSpeakFlags.Async` ersetzt werden, nicht durch `SpeechVoiceSpeakFlags.lagsAsync`.
  * Die Verwendung von `constants.SVE*` sollte durch `SpeechVoiceEvents.*` ersetzt werden.
* Aus dem App-Modul `soffice` wurden die folgenden Klassen und Funktionen entfernt `JAB_OOTableCell`, `JAB_OOTable`, `gridCoordStringToNumbers`. (#12849)
* core.CallCancelled`` ist jetzt `exceptions.CallCancelled`. (#12940)
* Alle Konstanten, die mit RPC beginnen, aus `core` und `logHandler` wurden in `RPCConstants.RPC` enum verschoben. (#12940)
* Es wird empfohlen, die Funktionen `mouseHandler.doPrimaryClick` und `mouseHandler.doSecondaryClick` zu verwenden, um die logische Maus-Aktion auszuführen, wie z. B. das Aktivieren (primär) oder sekundär (Kontextmenü anzeigen), anstatt `executeMouseEvent` zu verwenden und die linke oder rechte Maustaste festzulegen. Dies stellt sicher, daß der Code die Windows-Benutzereinstellung für das Vertauschen der primären Maustaste beachtet. (#12642)
* `config.getSystemConfigPath` wurde entfernt - es gibt keinen Ersatz. (#12943)
* `shlobj.SHGetFolderPath` wurde entfernt - bitte verwenden Sie stattdessen `shlobj.SHGetKnownFolderPath`. (#12943)
* Die `shlobj`-Konstanten wurden entfernt. Ein neues Enum wurde erstellt, `shlobj.FolderId` für die Verwendung mit `SHGetKnownFolderPath`. (#12943)
* `diffHandler.get_dmp_algo` und `diffHandler.get_difflib_algo` wurden ersetzt durch `diffHandler.prefer_dmp` bzw. `diffHandler.prefer_difflib`. (#12974)
* `languageHandler.curLang` wurde entfernt - um die aktuelle NVDA Sprache zu erhalten, verwenden Sie `languageHandler.getLanguage()`. (#13082)
* Die Methode `getStatusBarText` kann in ein appModule implementiert werden, um die Art und Weise, wie NVDA den Text aus der Statusleiste holt, anzupassen. (#12845)
* `globalVars.appArgsExtra` wurde entfernt. (#13087)
  * Wenn Ihre Erweiterung zusätzliche Kommandozeilen-Argumente verarbeiten muss, lesen Sie die Dokumentation von `addonHandler.isCLIParamKnown` und das Entwicklerhandbuch für Details.
* Das UIA-Handler-Modul und andere UIA-Unterstützungsmodule sind jetzt Teil eines UIAHandler-Pakets. (#10916)
  * `UIAUtils` ist jetzt `UIAHandler.utils`
  * `UIABrowseMode` ist jetzt `UIAHandler.browseMode`
  * `_UIAConstants` ist jetzt `UIAHandler.constants`
  * `_UIACustomProps` ist jetzt `UIAHandler.customProps`
  * `_UIACustomAnnotations` ist jetzt `UIAHandler.customAnnotations`
* Die `IAccessibleHandler`-Konstanten `IA2_RELATION_*` wurden durch Enum der `IAccessibleHandler.RelationType` ersetzt. (#13096)
  * `IA2_RELATION_FLOWS_FROM` entfernt.
  * `IA2_RELATION_FLOWS_TO` entfernt.
  * `IA2_RELATION_CONTAINING_DOCUMENT` entfernt.
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` und `LOCALE_SLANGDISPLAYNAME` wurden aus `languageHandler` entfernt. Verwenden Sie stattdessen Mitglieder von `languageHandler.LOCALE`. (#12753)
* Umstellung von Minhook auf Microsoft Detours als Hooking-Bibliothek für NVDA. Mit dieser Hooking-Bibliothek wird hauptsächlich zur Unterstützung des Anzeigemodells verwendet. (#12964)
* `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` wurde entfernt. (#13211)
* SCons warnt nun davor, basierend mit einer Anzahl von Aufträgen, die der Anzahl der logischen Prozessorkerne im System entspricht. Dies kann die Erstellungszeit bei mehreren Kernen drastisch verkürzen. (#13226, #13371)
* Die Konstanten `characterProcessing.SYMLVL_*` wurden entfernt. Bitte verwenden Sie stattdessen `characterProcessing.SymbolLevel.*`. (#13248)
* Die Funktionen `loadState` und `saveState` wurden aus addonHandler entfernt. Bitte verwenden Sie stattdessen `addonHandler.state.load` und `addonHandler.state.save`. (#13245)
* Die Interaktionsbefehle aus NVDAHelper für UWP/OneCore wurden [von C++/CX nach C++/Winrt](https://docs.microsoft.com/de-de/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx) verschoben. (#10662)
* Es ist nun obligatorisch, die Unterklasse `DictionaryDialog` zu benutzen. (#13268)
* `config.RUN_REGKEY`, `config.NVDA_REGKEY` sind veraltet. Bitte verwenden Sie stattdessen `config.RegistryKey.RUN`, `config.RegistryKey.NVDA`. Diese werden 2023 entfernt. (#13242)
* `easeOfAccess.ROOT_KEY`, `easeOfAccess.APP_KEY_PATH` sind veraltet. Bitte verwenden Sie stattdessen `easeOfAccess.RegistryKey.ROOT`, `easeOfAccess.RegistryKey.APP`. Diese werden 2023 entfernt. (#13242)
* `easeOfAccess.APP_KEY_NAME` ist veraltet und wird 2023 entfernt. (#13242)
* `DictionaryDialog` und `DictionaryEntryDialog` wurden von `gui.settingsDialogs` nach `gui.speechDict` verschoben. (#13294)
* IAccessible2-Beziehungen werden nun in der Entwickler-Info für IAccessible2-Objekte angezeigt. (#13315)
* `languageHandler.windowsPrimaryLCIDsToLocaleNames` wurde entfernt, verwenden Sie stattdessen `languageHandler.windowsLCIDToLocaleName` oder `winKernel.LCIDToLocaleName`. (#13342)
* Die Eigenschaft `UIAAutomationId` für UIA-Objekte sollte gegenüber `cachedAutomationId` bevorzugt werden. (#13125, #11447)
  * `cachedAutomationId` kann verwendet werden, wenn sie direkt vom Element bezogen wird.
* `NVDAObjects.window.scintilla.CharacterRangeStruct` wurde verschoben nach `NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct`. (#13364)
* `gui.isInMessageBox` (Boolean) wurde entfernt, bitte verwenden Sie stattdessen die Function `gui.message.isModalMessageBoxActive`. (#12984, #13376)
* `controlTypes` wurde in mehreren Submodulen aufgeteilt. (#12510, #13588)
  * `ROLE_*` und `STATE_*` wurden ersetzt durch `Role.*` und `State.*`.
  * Obwohl sie noch verfügbar sind, sollten die Folgenden als veraltet betrachtet werden:
    * `ROLE_*` und `STATE_*`, verwenden Sie stattdessen `Role.*` und `State.*`.
    * `roleLabels`, `stateLabels` und `negativeStateLabels`, verwenden Sie stattdessen `roleLabels[ROLE_*]` und deren Entsprechung `Role.*.displayString` oder `State.*.negativeDisplayString`.
    * `processPositiveStates` und `processNegativeStates`, verwenden Sie stattdessen `processAndLabelStates`.
* Die Konstanten für den Status einer Excel-Zelle (`NVSTATE_*`) sind nun Werte im `NvCellState`-Enum, gespiegelt im `NvCellState`-Enum in `NVDAObjects/window/excel.py` und abgebildet auf `controlTypes.State` über _nvCellStatesToStates. (#13465)
* Die Information für die Struktur `state` in `EXCEL_CELLINFO` befindet sich nun in `nvCellStates`.
* `mathPres.ensureInit` wurde entfernt, der MathPlayer wird nun beim Start von NVDA initialisiert. (#13486)

+= 2021.3.5 =
Dies ist eine kleinere Version zur Behebung einer Sicherheitslücke.
Bitte melden Sie Sicherheitsprobleme umgehend an <info@nvaccess.org>.

### Sicherheitsproblembehebungen

* Behoben wurde der Sicherheitshinweis `GHSA-xc5m-v23f-pgr7`.
  * Das Dialogfeld für die Ansage von Symbolen wurde im geschützten Modus deaktiviert.

## 2021.3.4

In dieser Version wurden mehrere Sicherheitsprobleme behoben.
Bitte melden Sie Sicherheitsprobleme umgehend an <info@nvaccess.org>! Vielen Dank.

### Sicherheitsproblembehebungen

* Behoben wurde der Sicherheitshinweis `GHSA-354r-wr4v-cx28`. (#13488)
  * Die Möglichkeit, NVDA mit aktivierter Debug-Protokollierung zu starten, sobald NVDA im geschützten Modus läuft, wurde entfernt.
  * Die Möglichkeit, NVDA zu aktualisieren, sobald NVDA im geschützten Modus läuft, wurde entfernt.
* Behoben wurde der Sicherheitshinweis `GHSA-wg65-7r23-h6p9`. (#13489)
  * Die Möglichkeit, das Dialogfeld für Tastenbefehle im geschützten Modus zu öffnen, wurde entfernt.
  * Die Möglichkeit, die Dialogfelder für die verschiedenen Wörterbücher im geschützten Modus zu öffnen, wurde entfernt.
* Behoben wurde der Sicherheitshinweis `GHSA-mvc8-5rv9-w3hx`. (#13487)
  * Die WX-GUI für das Inspektionswerkzeug wurde im geschützten Modus deaktiviert.

## 2021.3.3

Diese Version ist identisch mit 2021.3.2.
Es gab einen Fehler in NVDA 2021.3.2, der sich fälschlicherweise als 2021.3.1 identifizierte.
Diese Version gibt sich korrekt als 2021.3.3 zu erkennen.

## 2021.3.2

Mehrere kritische Sicherheitsprobleme wurden in dieser Version behoben.
Bitte melden Sie Sicherheitsprobleme umgehend an die E-Mail-Adresse <info@nvaccess.org>! Vielen Dank.

### Fehlerbehebungen

* Sicherheitsproblem behoben: Verhindert die Objektnavigation außerhalb des Sperrbildschirms in Windows 10 und Windows 11. (#13328)
* Sicherheitsproblem behoben: Das Dialogfeld für die Verwaltung der Erweiterungen ist nun im geschützten Bereich deaktiviert. (#13059)
* Sicherheitsproblem behoben: Die Kontexthilfe in NVDA ist im geschützten Bereich nicht mehr verfügbar. (#13353)

## 2021.3.1

Diese Version behebt mehrere Probleme in 2021.3.

### Änderungen

* Das neue HID-Protokoll für Braillezeilen wird nicht mehr bevorzugt, wenn ein anderer Braillezeilen-Treiber verwendet wird. (#13153)
* Das neue HID-Protokoll für Braillezeilen kann über eine Einstellung in den erweiterten Einstellungen deaktiviert werden. (#13180)

### Fehlerbehebungen

* Landmark wird wieder auf der Braillezeile abgekürzt. #13158
* Die automatische Erkennung der Braillezeilen für Humanware Brailliant und APH Mantis Q40 in Verwendung mit Bluetooth wurde behoben. (#13153)

## 2021.3

Diese Version bietet Unterstützung für die neue HID-Braille-Spezifikation.
Diese Spezifikation vereinfacht die Unterstützung für Braillezeilen zu standardisieren, ohne dass individuelle Treiber benötigt werden.
Neue Updates für eSpeak-NG und LibLouis, einschließlich neue Braille-Tabellen für Russisch und Tshivenda.
Fehlertöne können in stabilen Builds von NVDA über eine neue Option für erweiterte Einstellungen aktiviert werden.
Alles Lesen in Microsoft Word scrollt nun durch die Ansicht, um die aktuelle Position sichtbar zu halten.
Es gibt viele Verbesserungen bei der Verwendung von UIA in Office-Anwendungen.
Ein Problem mit UIA wurde behoben, dass Outlook jetzt mehr Arten von Layouttabellen in Nachrichten ignoriert.

Wichtige Anmerkungen:

Auf Grund einer Aktualisierung unseres Sicherheitszertifikats erhalten einige Benutzer einen Fehler, wenn NVDA 2021.2 nach Updates sucht.
NVDA fordert nun Windows auf, Sicherheitszertifikate zu aktualisieren, wodurch dieser Fehler in Zukunft verhindert wird.
Betroffene Benutzer müssen dieses Update manuell herunterladen.

### Neue Features

* Fügt einen Tastenbefehl zum Umschalten der Einstellungen zum Mitteilen des Stils von Zellenrahmen hinzu. (#10408)
* Unterstützung der neuen HID-Braille-Spezifikation, die darauf abzielt, die Unterstützung für Braille-Displays zu standardisieren. (#12523)
 * Geräte, die diese Spezifikation unterstützen, werden von NVDA automatisch erkannt.
 * Technische Details zur Implementierung dieser Spezifikation durch NVDA finden Sie unter https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
-
* Unterstützung für VisioBraille Vario 4 Braille hinzugefügt. (#12607)
* Fehlermeldungen können bei Verwendung einer beliebigen Version von NVDA aktiviert werden (erweiterte Einstellungen). (#12672)
* In Windows 10 und neuer gibt NVDA die Anzahl der Vorschläge bei der Eingabe von Suchbegriffen in Apps wie Einstellungen und Microsoft Store an. (#7330, #12758, #12790)
* Die Tabellen-Navigation wird nun in Rastersteuerelementen unterstützt, die mit dem Out-GridView-Cmdlet in PowerShell erstellt wurden. (#12928)

### Änderungen

* eSpeak NG wurde auf 1.51-dev Commit `74068b91bcd578bd7030a7a6cde2085114b79b44` aktualisiert. (#12665)
* NVDA verwendet standardmäßig eSpeak, wenn keine installierten OneCore-Stimmen die von NVDA bevorzugte Sprache unterstützen. (#10451)
* Wenn die OneCore-Stimmen nicht verwendet werden können, wird die Sprachausgabe auf eSpeak zurückgesetzt. (#11544)
* Beim Lesen der Statusleiste mit `NVDA+Ende` wird der NVDA-Cursor nicht mehr an die Position verschoben.
Wenn Sie jedoch diese Funktionalität benötigen, weisen Sie dem entsprechenden Skript in der Kategorie "Objekt-Navigation" im Dialogfeld für die Tastenbefehle einen entsprechenden Tastenbefehl zu. (#8600)
* Beim Öffnen eines bereits geöffneten Einstellungsdialogs legt NVDA den Fokus auf den vorhandenen Dialog, anstatt einen Fehler auszulösen. (#5383)
* Der Braille-Übersetzer LibLouis wurde aktualisiert auf [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Neue Braille-Tabellen: Russisch Vollschrift, Tshivenda Vollschrift, Tshivenda Kurzschrift
* Anstelle von "Markierter Inhalt" oder "mrkd" wird "hervorgehoben" in Braille oder mit der Sprachausgabe mitgeteilt. (#12892)
* NVDA versucht nicht länger unter manchen Umständen das geöffnete Dialogfeld selbst zu schließen, wenn Dialogfelder auf eine erforderliche Aktion warten (z. B. bei Bestätigen bzw. Abbrechen). (#12984)

### Fehlerbehebung

* Das Verfolgen von NVDA-Tasten (wie Strg oder Einfügen) ist robuster, wenn "Watchdog" wiederhergestellt wird. (#12609)
* Es ist wieder möglich, auf bestimmten Systemen nach NVDA-Updates zu suchen; z. B. nach einer Bereinigung oder kompletten Neuinstallationen von Windows. (#12729)
* NVDA teilt leere Tabellenzellen in Microsoft Word nun korrekt mit, wenn UIA verwendet wird. (#11043)
* In ARIA-Datenrasterzellen im Web wird die Escape-Taste jetzt an das Raster weitergegeben und deaktiviert den Fokusmodus nicht mehr bedingungslos. (#12413)
* Beim Lesen einer Kopfzeile einer Tabelle in Chrome wurde korrigiert, dass der Spaltenname zweimal angesagt wird. (#10840)
* NVDA meldet keinen numerischen Wert mehr für UIA-Schieberegler, für die eine Textdarstellung ihres Wertes definiert ist. (UIA ValuePattern wird jetzt RangeValuePattern vorgezogen). (#12724)
* NVDA behandelt den Wert von UIA-Schiebereglern nicht mehr immer prozentual.
* Das Mitteilen des Standorts einer Zelle in Microsoft Excel beim Zugriff über die UIA funktioniert unter Windows 11 wieder ordnungsgemäß. (#12782)
* NVDA legt keine ungültigen Python-Gebietsschemas mehr fest. (#12753)
* Wenn eine deaktivierte Erweiterung deinstalliert und dann erneut wieder installiert wird, wird diese nun automatisch aktiviert. (#12792)
* Fehler beim Aktualisieren und Entfernen von Erweiterungen behoben, bei denen der Ordner der Erweiterung umbenannt wurde oder Dateien geöffnet wurden. (#12792, #12629)
* Bei Verwendung der UIA für den Zugriff auf Steuerelemente in Microsoft Excel-Tabellenkalkulationen gibt NVDA nicht mehr redundant an, wenn eine einzelne Zelle ausgewählt wird. (#12530)
* Weitere Dialogtexte werden in LibreOffice Writer automatisch vorgelesen, beispielsweise in Bestätigungsdialogen. (#11687)
* Das Lesen bzw. Navigieren im Lesemodus in Microsoft Word über die UIA stellt nun sicher, dass das Dokument immer gescrollt wird, so dass die aktuelle Position im Lesemodus sichtbar ist und dass die Position des System-Cursors im Fokus-Modus die Position des Lesemodus korrekt widerspiegelt. (#9611)
* Beim Ausführen von Alles Lesen in Microsoft Word über die UIA wird das Dokument nun automatisch gescrollt und die Position der Einfügemarke wird korrekt aktualisiert. (#9611)
* Wenn E-Mails in Outlook gelesen werden und NVDA mit der UIA auf die Nachricht zugreift, werden bestimmte Tabellen jetzt als Layouttabellen markiert, was bedeutet, dass sie nicht mehr standardmäßig mitgeteilt werden. (#11430)
* Ein seltener Fehler beim Wechseln von Audio-Geräten wurde behoben. (#12620)
* Eingaben in Kurzschrift sollten sich in Eingabefeldern zuverlässiger verhalten. (#12667)
* Beim Navigieren im Windows-Taskleistenkalender teilt NVDA nun den Wochentag vollständig mit. (#12757)
* Bei Verwendung einer chinesischen Eingabemethode wie Taiwan - Microsoft Quick in Microsoft Word springt das Vor- und Zurücknavigieren der Braillezeile nicht mehr fälschlicherweise immer wieder an die ursprüngliche Position der Einfügemarke zurück. (#12855)
* Beim Zugriff auf Microsoft Word-Dokumente über UIA ist die satzweise Navigation (Alt+Pfeil nach oben/unten) wieder möglich. (#9254)
* Beim Zugriff auf MS Word mit UIA wird jetzt das Einrücken von Absätzen mitgeteilt. (#12899)
* Beim Zugriff auf MS Word mit UIA werden der Befehl zur Änderungsverfolgung und einige andere lokalisierte Befehle jetzt in Word mitgeteilt. (#12904)
* Doppelte Ausgaben in Braille und der Sprachausgabe behoben, wenn "description" mit "content" oder "name" übereinstimmt. (#12888)
* Bei der Eingabe in Microsoft Word mit aktiviertem UIA teilt NVDA die Rechtschreibfehler exakter mit. (#12161)
* In Windows 11 sagt NVDA nicht mehr "Fenster", wenn Sie Alt+Tab drücken, um zwischen den Anwendungen zu wechseln. (#12648)
* Der neue Bereich der Modernen Kommentare wird nun in Microsoft Word unterstützt, wenn nicht über UIA auf das Dokument zugegriffen wird. Drücken Sie Alt+F12, um zwischen dem Panel und dem Dokument zu wechseln. (#12982)

### Änderungen für Entwickler

* Das Erstellen von NVDA erfordert jetzt Visual Studio 2019 Version 16.10.4 oder neuer.
Aktualisieren Sie Visual Studio, damit es der Produktionsumgebung des Builds entspricht, damit es mit der [aktuellen Version von AppVeyor verwendet](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019) synchronisiert bleibt. (#12728)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable` wurde für die Entfernung in 2022.1 eingestellt. (#12660)
  * Verwenden Sie stattdessen `apiLevel` (siehe die Kommentare zu `_UIAConstants.WinConsoleAPILevel` für Details).
* Die Transparenz der Texthintergrundfarbe, die aus GDI-Anwendungen (über das Anzeigemodell) stammt, wird nun für Erweiterungen oder App-Modulen verfügbar gemacht. (#12658)
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST` und `LOCALE_SLANGDISPLAYNAME` werden in die `LOCALE`-Enumeration im languageHandler verschoben.
Sie sind weiterhin auf Modulebene verfügbar, aber veraltet und werden in NVDA 2022.1 entfernt. (#12753)
* Die Verwendung der Funktionen `addonHandler.loadState` und `addonHandler.saveState` sollte vor 2022.1 durch ihre Äquivalente `addonHandler.state.save` und `addonHandler.state.load` ersetzt werden. (#12792)
* Die Braille-Ausgabe kann nun in System-Tests überprüft werden. (#12917)

## 2021.2

Diese Version führt die vorläufige Unterstützung für Windows 11 ein.
Während Windows 11 noch veröffentlicht werden muss, wurde diese Version auf Vorab-Versionen von Windows 11 getestet.
Dies beinhaltet eine wichtige Korrektur für den Bildschirmvorhang (siehe Wichtige Hinweise).
Das Behebungs-Tool für die COM-Registrierung kann nun mehr Probleme beim Ausführen von NVDA beheben.
Außerdem gibt es Updates für die Sprachausgabe eSpeak und den Braille-Übersetzer LibLouis.
Ferner sind auch verschiedene Fehlerbehebungen und Verbesserungen, insbesondere für Braille-Unterstützung und Windows-Terminals, Rechner, Emoji-Panel und Zwischenablageverlauf mit dabei.

### Wichtige Hinweise

Auf Grund einer Änderung in der API für die Windows-Lupe musste die Funktion für den Bildschirmvorhang aktualisiert werden, um die neuesten Versionen von Windows zu unterstützen.
Verwenden Sie NVDA 2021.2, um den Bildschirmvorhang mit Windows 10 21H2 (10.0.19044) oder neuer zu aktivieren.
Dazu gehören Insider Builds für Windows 10 und Windows 11.
Wenn Sie eine neuere Windows-Version verwenden, erhalten Sie aus Sicherheitsgründen eine visuelle Bestätigung, dass der Bildschirmvorhang den Bildschirm vollständig verdunkelt.

### Neue Features

* Experimentelle Unterstützung für ARIA-Anmerkungen:
  * Fügt einen Befehl hinzu, um eine Zusammenfassung der Details eines Objekts mit "aria-details" zu lesen. (#12364)
  * Fügt eine Option in den Erweiterten Einstellungen hinzu, um zu benachrichtigen, sobald ein Objekt Details im Lesemodus enthält. (#12439)
* In Windows 10 Version 1909 und neuer (einschließlich Windows 11) gibt NVDA die Anzahl der Vorschläge an, wenn Suchvorgänge im Datei-Explorer durchgeführt werden. (#10341, #12628)
* In Microsoft Word teilt NVDA nun bei der Ausführung das Ergebnis von Einrückungen und hängenden Absätzen mit. (#6269)

### Änderungen

* eSpeak NG wurde auf 1.51-dev Commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb` aktualisiert. (#12449, #12202, #12280, #12568)
* Wenn Artikel in den Benutzereinstellungen für die Dokument-Formatierung aktiviert ist, teilt NVDA "Artikel" nach dem Inhalt mit. (#11103)
* Der Braille-Übersetzer LibLouis wurde auf [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0) aktualisiert. (#12526)
  * Neue Braille-Tabellen: Bulgarische Vollschrift, Burmesische Vollschrift, Burmesische Kurzschrift, Kasachische Vollschrift, Vollschrift für Khmer, Nordkurdische Basisschrift, Voll- und Kurzschrift für Sepedi, Voll- und Kurzschrift für Sesotho, Voll- und Kurzschrift für Setswana, Vollschrift für Tatar, Vietnamesische Basisschrift, Vietnamesische Kurzschrift, Südvietnamesische Vollschrift, Voll- und Kurzschrift für Xhosa, Vollschrift für Yakut, Voll und Kurzschrift fürZulu.
* Der Eintrag "Windows 10-Texterkennung" in den NVDA-Einstellungen wurde in "Windows-Texterkennung" umbenannt. (#12690)

### Fehlerbehebung

* In Windows 10 Rechner teilt NVDA Rechenausdrücke auf der Braillezeile mit. (#12268)
* In Terminal-Anwendungen unter Windows 10 ab Version 1607 werden beim Einfügen oder Löschen von Zeichen in der Mitte einer Zeile die Zeichen rechts neben der Einfügemarke nicht mehr vorgelesen. (#3200)
  * Diff Match Patch jetzt standardmäßig aktiviert. (#12485)
* Die Braille-Eingabe funktioniert einwandfrei mit den folgenden Kurzschrift-Tabellen: Arabisch, Spanisch, Urdu, Chinesisch (China, Mandarin). (#12541)
* Das Tool zur Behebung für die COM-Registrierung behebt jetzt mehr Probleme, insbesondere unter 64-Bit-Windows. (#12560)
* Verbesserungen bei der Tastenbedienung für das Braillegerät Seika Notetaker von Nippon Telesoft. (#12598)
* Verbesserungen bei der Ankündigung des Windows-Emoji-Bedienfelds und des Zwischenablageverlaufs. (#11485)
* Die Zeichen-Beschreibungen des bengalischen Alphabets wurden aktualisiert. (#12502)
* NVDA wird sicher beendet, wenn ein neuer Prozess gestartet wird. (#12605)
* Die erneute Auswahl des Braillezeilen-Treibers von HandyTech aus dem Dialogfeld der Braillezeilen auswählen führt nicht mehr zu Fehlern. (#12618)
* Windows Version 10.0.22000 oder höher wird als Windows 11 erkannt, nicht als Windows 10. (#12626)
* Die Unterstützung für den Bildschirmvorhang wurde behoben und für Windows-Versionen bis 10.0.22000 getestet. (#12684)
* Wenn beim Filtern von Tastenbefehle keine Ergebnisse angezeigt werden, funktioniert das Dialogfeld für diese Konfiguration für die Tastenbefehle weiterhin wie erwartet. (#12673)
* Es wurde ein Fehler behoben, bei dem der erste Menü-Eintrag eines Untermenüs in einigen Kontexten nicht vorgelesen wurde. (#12624)

### Änderungen für Entwickler

* `characterProcessing.SYMLVL_*`-Konstanten sollten vor 2022.1 durch deren Äquivalent `SymbolLevel.*` ersetzt werden. (#11856, #12636)
* `controlTypes` wurde in verschiedene Submodule aufgeteilt, als veraltet markierte Symbole müssen vor 2022.1 ersetzt werden. (#12510)
  * Die Konstanten `ROLE_*` und `STATE_*` sollten durch entsprechende `Role.*` und `State.*` ersetzt werden.
  * `roleLabels`, `stateLabels` und `negativeStateLabels` sind veraltet, Verwendungen wie `roleLabels[ROLE_*]` sollten entsprechenden durch `Role.*.displayString` ersetzt werden oder `State.*.negativeDisplayString`.
  * `processPositiveStates` und `processNegativeStates` sind zum Entfernen veraltet.
* Unter Windows 10 Version 1511 und neuer (einschließlich Insider-Builds) wird der aktuelle Versionsname des Windows-Feature-Updates aus der Windows-Registrierung abgerufen. (#12509)
* Veraltet: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` wird in 2022.1 entfernt, es gibt keinen direkten Ersatz. (#12544)

## 2021.1

Diese Version enthält optionale experimentelle Unterstützung für UIA in Microsoft Excel und Chromium-basierte Browser.
Viele Korrekturen für mehrere Sprachen und für den Zugriff auf Links in Braille-Schrift wurden durchgeführt.
Daneben gibt es auch Updates für Unicode CLDR und mathematische Symbole, die Sprachausgabe eSpeak-NG und den braille-Übersetzer LibLouis.
Sowie viele Fehlerbehebungen und Verbesserungen, einschließlich in Office, Visual Studio und mehreren Sprachen.

Hinweis:

 * Für diese Version muss die Kompatibilität aller Erweiterungen überprüft und ggf. angepasst werden.
 * In dieser Version wurde auch die Unterstützung für Adobe Flash endgültig eingestellt.

### Neue Features

* Frühe Unterstützung für UIA mit Chromium-basierte Browser (wie Microsoft Edge). (#12025)
* Optionale experimentelle Unterstützung für Microsoft Excel über UIA. Nur empfohlen für Microsoft Excel Build 16.0.13522.10000 oder neuer. (#12210)
* Vereinfachtere Navigation der Ausgabe in der NVDA-Python-Konsole. (#9784)
  * Mit Alt+Pfeiltasten nach oben/unten springt man zum vorherigen/nächsten Ausgabe-Ergebnis (zum Auswählen Umschalt-Taste zusätzlich drücken).
  * Mit Strg+L wird das Ausgabefenster geleert.
* NVDA sagt nun die Kategorien an, die einem Termin in Microsoft Outlook zugeordnet sind, sofern vorhanden. (#11598)
* Unterstützung für die Braillezeile Seika Notetaker von Nippon Telesoft. (#11514)

### Änderungen

* Im Lesemodus können Steuerelemente nun mit Braille-Cursor-Routing auf ihrem Deskriptor (z. B. "lnk" für einen Link) aktiviert werden. Dies ist besonders nützlich, um z. B. Kontrollkästchen ohne Beschriftung zu aktivieren. (#7447)
* NVDA verhindert jetzt, dass der Benutzer die Windows 10-Texterkennung ausführt, wenn der Bildschirmvorhang aktiviert ist. (#11911)
* Das Unicode Common Locale Data Repository (CLDR) wurde auf 39.0 aktualisiert. (#11943, #12314)
* Weitere mathematische Symbole zum Symbolwörterbuch hinzugefügt. (#11467)
* Das Benutzerhandbuch, Was ist neu und die Auflistung der Kurzübersicht der Befehle haben jetzt ein aktualisiertes Aussehen. (#12027)
* Die Meldung "Nicht unterstützt" wird jetzt gemeldet, wenn versucht wird, das Bildschirmlayout in Anwendungen umzuschalten, die dies nicht unterstützen, wie z. B. in Microsoft Word. (#7297)
* Die Option "Versuch, die Sprachausgabe bei abgelaufenen Fokus-Ereignissen abzubrechen" in der Kategorie "Erweiterte Einstellungen" nun standardmäßig aktiviert. (#10885)
  * Dieses Verhalten kann deaktiviert werden, indem diese Option auf "Nein" gesetzt wird.
  * In Web-Anwendungen, wie z. B. Gmail, werden nicht mehr veraltete Informationen mitgeteilt, wenn der Fokus schnell verschoben wird.
* Der Braille-Übersetzer LibLouis wurde auf [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0) aktualisiert. (#12137)
  * Neue Braille-Tabellen: Belarussisches Literaturbraille, Belarussisches Computer-Braille sowie Voll- und Kurzschrift in Urdu (Indien und Pakistan).
* Die Unterstützung für Adobe Flash wurde aus NVDA vollständig entfernt, da Adobe die Entwicklung eingestellt hat und damit der Support auch bereits Ende 2020 auslief. (#11131)
* NVDA beendet sich auch bei noch geöffneten Fenstern, der Beendigungsvorgang schließt nun alle NVDA-Fenster und -Dialoge. (#1740)
* Der Sprachausgaben-Betrachter kann nun mit `Alt+F4` geschlossen werden und hat einen Schließen-Schalter für eine einfachere Interaktion mit Benutzern von Zeigegeräten. (#12330)
* Der Braille-Betrachter verfügt nun standardmäßig über einen Schließen-Schalter, um die Interaktion mit Benutzern von Zeigegeräten zu erleichtern. (#12328)
* Im Dialog "Elementliste" wurde in einigen Sprachumgebungen die Beschleunigungstaste auf der Schaltfläche "Aktivieren" entfernt, um Konflikte mit der Beschriftung eines Optionsfeldes für den Elementtyp zu vermeiden. Sofern vorhanden, ist die Schaltfläche immer noch der Standard des Dialogs und kann als solcher weiterhin durch einfaches Drücken der Eingabetaste in der Elementliste selbst aufgerufen werden. (#6167)

### Fehlerbehebungen

* Die Liste der Nachrichten in Microsoft Outlook 2010 ist wieder auslesbar. (#12241)
* In Terminalprogrammen unter Windows 10 ab Version 1607 werden beim Einfügen oder Löschen von Zeichen in der Mitte einer Zeile die Zeichen rechts vom Cursor nicht mehr mit vorgelesen. (#3200)
  * Diese experimentelle Korrektur kann manuell in den erweiterten Einstellungen von NVDA aktiviert werden, indem der Diff-Algorithmus auf "Diff-Match-Patch zulassen" geändert wird.
* In Microsoft Outlook sollte die unangemessene Abstandsmeldung beim Verwenden von Umschalt+Tab vom Nachrichtentext zum Betreff-Feld nicht mehr vorkommen. (#10254)
* In der Python-Konsole wird nun das Einfügen eines Tabulators zur Einrückung am Anfang einer nicht leeren Eingabezeile und das Ausführen der Tabulator-Vervollständigung in der Mitte einer Eingabezeile unterstützt. (#11532)
* Formatierungsinformationen und andere blätterbare Meldungen zeigen keine unerwarteten Leerzeilen mehr an, wenn das Bildschirmlayout ausgeschaltet ist. (#12004)
* Es ist jetzt möglich, Kommentare in Microsoft Word mit aktivierter UIA zu auszulesen. (#9285)
* Die Leistung bei der Interaktion mit Visual Studio wurde verbessert. (#12171)
* Behebung von Grafikfehlern wie fehlende Elemente bei Verwendung von NVDA mit einem Layout von Rechts nach Links. (#8859)
* Die Richtung des GUI-Layouts wird nun basierend auf der NVDA-Sprache und nicht auf dem Systemgebietsschema berücksichtigt. (#638)
 * Ein bekanntes Problem für Sprachen, die von Rechts nach Links verlaufen: der rechte Rand von Gruppierungen klammert mit Beschriftungen/Steuerungen. (#12181)
* Die Landessprache für Python wird konsistent auf die in den Voreinstellungen gewählte Sprache eingestellt und tritt bei Verwendung der Standardsprache auf. (#12214)
* TextInfo.getTextInChunks friert nicht mehr ein, wenn es auf Rich-Edit-Steuerelementen wie dem NVDA Log Viewer aufgerufen wird. (#11613)
* Es ist wieder möglich, NVDA in Sprachen zu verwenden, die Unterstriche im Gebietsschemennamen enthalten, wie z. B. de_CH unter Windows 10 Version 1803 und 1809. (#12250)
* In WordPad funktioniert die Konfiguration der Hochstellung/Tiefstellung wie erwartet. (#12262)
* NVDA zeigt den neu fokussierten Inhalt auf einer Webseite nicht mehr an, wenn der alte Fokus verschwindet und durch den neuen Fokus an der gleichen Position ersetzt wird. (#12147)
* Durchgestrichene, hoch- und tiefgestellte Formatierungen für die komplette Zelle in Microsoft Excel werden nun gemeldet, wenn die entsprechende Option aktiviert ist. (#12264)
* Das Kopieren der Konfiguration während der Installation aus einer portablen Kopie wurde korrigiert, wenn das Standard-Zielverzeichnis für die Konfiguration leer ist. (#12071, #12205)
* Fehlerhafte Ansage einiger Buchstaben mit Akzenten oder diakritischen Zeichen behoben, wenn die Option 'Großbuchstaben vor Großbuchstaben sagen' aktiviert ist. (#11948)
* Fehler bei der Tonhöhenänderung in Sprachausgaben für SAPI4 behoben. (#12311)
* Das NVDA-Installationsprogramm beachtet nun auch den `--minimal` Kommandozeilen-Parameter und spielt keinen Start-Sound ab. Es folgt damit dem gleichen dokumentierten Verhalten wie eine installierte oder portable Kopie des NVDA-Programms. (#12289)
* In Microsoft Word oder Microsoft Outlook kann die Tabellenschnellnavigationstaste jetzt zur Layouttabelle springen, wenn die Option "Layout-Tabellen einbeziehen" in den Einstellungen des Lesemodus aktiviert ist. (#11899)
* NVDA sagt nicht mehr "↑↑↑" bei manchen Emojis in bestimmten Sprachen. (#11963)
* eSpeak unterstützt nun wieder Kantonesisch und Mandarin. (#10418)
* Im neuen Chromium-basierten Microsoft Edge werden Textfelder wie die Adressleiste nun angesagt, wenn sie leer sind. (#12474)
* Der Treiber für die Seika-Braillezeilen funktioniert nun wieder. (#10787)

### Änderungen für Entwickler

* Hinweis: Dies ist eine Version, die die Kompatibilität der API für Erweiterungen inkompatibel macht. Daher sollten Erweiterungen erneut getestet und deren Manifest-Dateien aktualisiert werden.
* Das Build-System von NVDA holt jetzt alle Python-Abhängigkeiten mit pip und speichert sie in einer virtuellen Python-Umgebung. Dies geschieht alles transparent.
  * Um NVDA zu kompilieren, sollte SCons weiterhin auf die übliche Weise verwendet werden, z. B. Ausführen von "scons.bat" im Stammverzeichnis des Repositorys. Die Ausführung von `py -m SCons` wird nicht mehr unterstützt. Die Datei `scons.py` wurde ebenfalls entfernt.
  * Um NVDA aus dem Quellcode zu starten, sollte der Entwickler nun `runnvda.bat` im Wurzelverzeichnis des Repositorys verwenden, anstatt `source/nvda.pyw` direkt auszuführen. Wenn Sie versuchen, `source/nvda.pyw` auszuführen, werden Sie in einem Meldungsfenster darauf hingewiesen, dass dies nicht mehr unterstützt wird.
  * Um Unit-Tests durchzuführen, führen Sie `rununittests.bat [<extra unittest discover options>]` aus.
  * Um Systemtests durchzuführen: führen Sie `runsystemtests.bat [<extra robot options>]` aus.
  * Um Linting auszuführen, führen Sie `runlint.bat <Basiszweig>` aus.
  * Weitere Details entnehmen Sie bitte der englischsprachigen Datei "readme.md".
* Die folgenden Python-Abhängigkeiten wurden ebenfalls aktualisiert:
  * comtypes wurde auf 1.1.8 aktualisiert.
  * pySerial wurde auf 3.5 aktualisiert.
  * wxPython wurde auf 4.1.1 aktualisiert.
  * Py2exe wurde auf 0.10.1.0 aktualisiert.
* Die Funktion `LiveText._getTextLines` wurde entfernt. (#11639)
  * Überschreiben Sie stattdessen `_getText`, welches eine Zeichenkette mit dem gesamten Text des Objekts zurückgibt.
* Die Objekte von `LiveText` können nun Diffs nach Zeichen berechnen. (#11639)
  * Um das Diff-Verhalten für ein bestimmtes Objekt zu ändern, überschreiben Sie die Eigenschaft `diffAlgo` (siehe den Docstring für Details).
* Bei der Definition eines Skripts mit dem Skript-Dekorator kann das boolesche Argument "allowInSleepMode" angegeben werden, um zu signalisieren, ob ein Skript im Schlafmodus verfügbar ist oder nicht. (#11979)
* Die folgenden Funktionen wurden aus dem Konfigurationsmodul entfernt. (#11935)
  * "canStartOnSecureScreens" - verwenden Sie stattdessen "config.isInstalledCopy".
  * "hasUiAccess" und "execElevated" - verwenden Sie diese aus dem systemUtils-Modul.
  * "getConfigDirs" - verwenden Sie stattdessen "globalVars.appArgs.configPath".
* Die Konstanten aus "REASON_*" auf Modulebene wurden aus "controlTypes" entfernt - bitte verwenden Sie stattdessen "controlTypes.OutputReason". (#11969)
* Die Konstante "REASON_QUICKNAV" wurde aus browseMode entfernt - verwenden Sie stattdessen "controlTypes.OutputReason.QUICKNAV". (#11969)
* Die Eigenschaft `isCurrent` von `NVDAObject` (und Derivaten) liefert nun strikt die Enum-Klasse `controlTypes.IsCurrent` zurück. (#11782)
  * `isCurrent` ist nicht länger mehr optional und gibt daher keinen Wert zurück.
  * Wenn ein Objekt nicht aktuell ist, wird `controlTypes.IsCurrent.NO` zurückgegeben.
* Das Mapping `controlTypes.isCurrentLabels` wurde entfernt. (#11782)
  * Verwenden Sie stattdessen die Eigenschaft `displayString` für einen Enum-Wert `controlTypes.IsCurrent`.
    * Zum Beispiel: `controlTypes.IsCurrent.YES.displayString`.
* `winKernel.GetTimeFormat` wurde entfernt - verwenden Sie stattdessen `winKernel.GetTimeFormatEx`. (#12139)
* `winKernel.GetDateFormat` wurde entfernt - verwenden Sie stattdessen `winKernel.GetDateFormatEx`. (#12139)
* `gui.DriverSettingsMixin` wurde entfernt - verwenden Sie `gui.AutoSettingsMixin`. (#12144)
* `speech.getSpeechForSpelling` wurde entfernt - verwenden Sie `speech.getSpellingSpeech`. (#12145)
* Befehle können nicht direkt aus "speech" als `import speech; speech.ExampleCommand()` oder `import speech.manager; speech.manager.ExampleCommand()` importiert werden - verwenden Sie stattdessen `from speech.commands import ExampleCommand`. (#12126)
* `speakTextInfo` schleift die Sprachausgabe nicht mehr durch `speakWithoutPauses`, wenn der Grund `SAYALL` ist, da `SayAllHandler` dies nun manuell macht. (#12150)
* Das Modul `SynthDriverHandler` wird nicht mehr in `globalCommands` und `gui.settingsDialogs` importiert - verwenden Sie stattdessen `from synthDriverHandler import synthFunctionExample`. (#12172)
* `ROLE_EQUATION` wurde aus "controlTypes" entfernt - verwenden Sie stattdessen `ROLE_MATH`. (#12164)
* Die Klassen `autoSettingsUtils.driverSetting` wurden aus dem `driverHandler` entfernt - bitte verwenden Sie diese aus `autoSettingsUtils.driverSetting`. (#12168)
* Die Klassen `autoSettingsUtils.utils` wurden aus `driverHandler` entfernt - bitte verwenden Sie diese aus `autoSettingsUtils.utils`. (#12168)
* Die Unterstützung von `TextInfo`, die nicht von `contentRecog.BaseContentRecogTextInfo` erben, wurde entfernt. (#12157)
* `speech.speakWithoutPauses` wurde entfernt - bitte verwenden Sie stattdessen `speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses`. (#12195, #12251)
* `speech.re_last_pause` wurde entfernt - bitte verwenden Sie stattdessen `speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause`. (#12195, #12251)
* `WelcomeDialog`, `LauncherDialog` und `AskAllowUsageStatsDialog` wurden nach `gui.startupDialogs` verschoben. (#12105)
* `getDocFilePath` wurde von `gui` in das Modul `documentationUtils` verschoben. (#12105)
* Das Modul "gui.accPropServer" sowie die Klassen "AccPropertyOverride" und "ListCtrlAccPropServer" aus dem Modul "gui.nvdaControls" wurden zugunsten der nativen WX-Unterstützung für das Überschreiben von eigenschaften der Barrierefreiheit entfernt. Wenn Sie die Barrierefreiheit von WX-Steuerelementen verbessern, implementieren Sie stattdessen "wx.Accessible". (#12215)
* Dateien in `source/comInterfaces/` sind nun leichter von Entwicklerwerkzeugen wie IDEs verwendbar. (#12201)
* Dem winVersion-Modul wurden komfortablere Methoden und -Typen hinzugefügt, um Windows-Versionen zu erhalten und besser zu vergleichen. (#11909)
  * Die Funktion "isWin10" wurde aus dem Modul "winVersion" entfernt.
  * Die Klasse "winVersion.WinVersion" ist ein vergleichbarer und bestellbarer Typ, der Windows-Versionsinformationen kapselt.
  * Die Funktion "winVersion.getWinVer" wurde hinzugefügt, um "winVersion.WinVersion" zu erhalten, die das aktuelle Betriebssystem zurückgibt.
  * Komfortablere Konstanten für bekannte Windows-Versionen hinzugefügt, siehe winVersion.WIN*-Konstanten.
* IAccessibleHandler importiert nicht mehr alles von IAccessible und IA2 COM Schnittstellen - bitte verwenden Sie diese direkt. (#12232)
* TextInfo-Objekte haben jetzt Start- und Endeigenschaften, die mit Operatoren wie < <= == != >= > mathematisch verglichen werden können. (#11613)
  * Z. B. ti1.start <= ti2.end
  * Diese Verwendung wird nun anstelle von ti1.compareEndPoints(ti2, "startToEnd") <= 0 bevorzugt
* TextInfo-Start- und -Ende-Eigenschaften können auch zueinander gesetzt werden. (#11613)
  * Z. B. ti1.start = ti2.end
  * Diese Verwendung wird anstelle von ti1.SetEndPoint(ti2, "startToEnd") bevorzugt
* `wx.CENTRE_ON_SCREEN` und `wx.CENTER_ON_SCREEN` wurden entfernt, verwenden Sie stattdessen `self.CentreOnScreen()`. (#12309)
* `easeOfAccess.isSupported` wurde entfernt, NVDA unterstützt nur noch Versionen von Windows, bei denen dies als `True` ausgewertet wird. (#12222)
* `sayAllHandler` wurde nach `speech.sayAll` verschoben. (#12251)
  * `speech.sayAll.SayAllHandler` stellt die Funktionen `stop`, `isRunning`, `readObjects`, `readText`, `lastSayAllMode` zur Verfügung.
  * `SayAllHandler.stop` setzt auch die `SayAllHandler`-Instanz `SpeechWithoutPauses` zurück.
  * `CURSOR_REVIEW` und `CURSOR_CARET` wurde durch `CURSOR.REVIEW` und `CURSOR.CARET` ersetzt.
* `speech.SpeechWithoutPauses` wurde nach `speech.speechWithoutPauses.SpeechWithoutPauses` verschoben. (#12251)
* `speech.curWordChars` wurde umbenannt in `speech._curWordChars`. (#12395)
* Die folgenden Werte wurden aus `speech` entfernt und können über `speech.getState()` abgerufen werden. Diese sind nun schreibgeschützte Werte. (#12395)
  * speechMode
  * speechMode_beeps_ms
  * beenCanceled
  * isPaused
* Um `speech.speechMode` zu aktualisieren, verwenden Sie `speech.setSpeechMode`. (#12395)
* Die folgenden Funktionen wurden nach `speech.SpeechMode` verschoben. (#12395)
  * Aus `speech.speechMode_off` wurde `speech.SpeechMode.off`.
  * Aus `speech.speechMode_beeps` wurde `speech.SpeechMode.beeps`.
  * Aus `speech.speechMode_talk` wurde `speech.SpeechMode.talk`.
* `IAccessibleHandler.IAccessibleObjectIdentifierType` ist jetzt `IAccessibleHandler.types.IAccessibleObjectIdentifierType`. (#12367)
* Folgendes in `NVDAObjects.UIA.WinConsoleUIA` wurde geändert (#12094)
  * `NVDAObjects.UIA.winConsoleUIA.is21H1Plus` wurde umbenannt in `NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable`.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo` umbenannt, um den Klassennamen mit Großbuchstaben zu beginnen.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1` umbenannt in `NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive`
    * Die Implementierung arbeitet einschließlich mit den beiden Endpunkten (in Textbereichen) vor [Microsoft/Terminal PR 4018](https://github.com/microsoft/terminal/pull/4018).
    * Workarounds für `expand`, `collapse`, `compareEndPoints`, `setEndPoint`, etc.

## 2020.4

Diese Version enthält neue chinesische Eingabemethoden, ein Update für den Braille-Übersetzer LibLouis und die Elementliste (NVDA+F7) funktioniert jetzt im Fokusmodus.
Die kontextbezogene Hilfe ist jetzt in NVDA-Dialogfeldern mit der Taste F1 erreichbar.
Verbesserungen der Regeln für die Aussprache von Symbolen, des Sprachwörterbuchs, der Braille-Nachricht und des Überfliegens.
Fehlerbehebungen und Verbesserungen für Mail, Outlook, Teams, Visual Studio, Azure Data Studio und Foobar2000.
Im Web gibt es Verbesserungen an Google Text & Tabellen und eine bessere Unterstützung für ARIA.
Diverse weitere Fehlerbehebungen und Verbesserungen.

### Neue Features

* Durch Drücken von F1 in NVDA-Dialogfeldern wird nun die Hilfedatei für den relevantesten Abschnitt geöffnet. (#7757)
* Unterstützung für Vorschläge zur automatischen Vervollständigung (IntelliSense) in Microsoft SQL Server Management Studio sowie Visual Studio 2017 und neuer. (#7504)
* Aussprache von Symbolen: Unterstützung für die Gruppierung in einer komplexen Symboldefinition und Unterstützung von Gruppenreferenzen in einer Ersetzungsregel, um sie einfacher und leistungsfähiger zu machen. (#11107)
* Anwender werden jetzt benachrichtigt, wenn sie versuchen, Sprachwörterbucheinträge mit ungültigen Ersetzungen für reguläre Ausdrücke zu erstellen. (#11407)
  * Speziell Gruppierungsfehler werden jetzt erkannt.
* Unterstützung für die neuen chinesischen traditionellen Schnell- und Pinyin-Eingabemethoden in Windows 10 hinzugefügt. (#11562)
* Registerkartenüberschriften werden jetzt als Formularfelder mit der Schnellnavigationstaste "f" betrachtet. (#10432)
* Es wurde ein Befehl zum Umschalten der Berichterstellung für markierten (hervorgehobenen) Text hinzugefügt. Es gibt keinen standardmäßig zugeordneten Tastenbefehl. (#11807)
* Der Befehlszeilenparameter "--copy-portable-config" wurde hinzugefügt, mit dem Sie die bereitgestellte Konfiguration automatisch in das Benutzerkonto kopieren können, wenn Sie NVDA unbeaufsichtigt installieren. (#9676)
* Das Braille-Routing wird jetzt mit dem Braille-Betrachter für Maus-Anwender unterstützt. Bewegen Sie den Mauszeiger, um zu einer Braille-Zelle zu springen. (#11804)
* NVDA erkennt die braillezeilen Humanware Brailliant BI 40X und 20X nun automatisch über USB und Bluetooth. (#11819)

### Änderungen

* Der Braille-Übersetzer LibLouis wurde auf Version 3.16.1 aktualisiert:
 * Mehrere Abstürze behoben.
 * Braille-Tabelle für Baschkirische Vollschrift hinzugefügt.
 * Koptische Tabelle für 8-Punkt-Computer-Braille hinzugefügt.
 * Braille-Tabelle für Kurzschrift (Afrikaans) hinzugefügt
 * Russische literarische Braille- und russische literarische Braille-Tabellen (detailliert) hinzugefügt.
 * Die russische Braille-Tabelle für Vollschrift wurde entfernt.
* Wenn Sie im Suchmodus mit "Alles Lesen" sich vorlesen lassen, werden die Befehle "Weiter suchen" und "Vorherige suchen" nicht mehr beendet, wenn die Option "Überfliegen des Lesens zulassen" aktiviert ist. Sagen wir, alle werden eher nach dem nächsten oder vorherigen gefundenen Begriff fortgesetzt. (#11563)
* Für HIMS-Braillezeilen wurde für F3 Leerzeichen+Punkte 148 neu zugeordnet. (#11710)
* Verbesserungen an der Benutzeroberfläche der Optionen "Zeitlimit für Braille-Meldungen" und "Nachrichten auf unbestimmte Zeit anzeigen". (#11602)
* In Web-Browsern und anderen Anwendungen, die den Suchmodus unterstützen, kann das Dialogfeld "Elementliste" (NVDA+F7) jetzt im Fokusmodus aufgerufen werden. (#10453)
* Aktualisierungen von ARIA-Live-Regionen werden jetzt unterdrückt, wenn die Berichterstellung für dynamische Inhaltsänderungen deaktiviert ist. (#9077)
* NVDA meldet jetzt "In die Zwischenablage kopiert" vor dem kopierten Text. (#6757)
* Die Darstellung der grafischen Ansichtstabelle in der Datenträgerverwaltung wurde verbessert. (#10048)
* Beschriftungen für Steuerelemente sind jetzt deaktiviert (ausgegraut), wenn das Steuerelement deaktiviert ist. (#11809)
* Die CLDR-Emoji-Annotation wurde auf Version 38 aktualisiert. (#11817)
* Die integrierte Funktion "Fokus-Highlight" wurde in "Visuell hervorheben" umbenannt. (#11700)

### Fehlerbehebungen

* NVDA arbeitet wieder korrekt mit Eingabefeldern, wenn die Anwendung Fast Log Entry verwendet wird. (#8996)
* Die abgelaufene Zeit wird in Foobar2000 angesagt, sofern keine Gesamtzeit zur Verfügung steht (z. B. beim Abspielen eines Livestreams). (#11337)
* NVDA berücksichtigt jetzt das Attribut "aria-roledescription" für Elemente in bearbeitbaren Inhalten auf Webseiten.
* "Liste" wird nicht mehr in jeder Zeile einer Liste in Google Text und Tabellen oder anderen bearbeitbaren Inhalten in Google Chrome mitgeteilt. (#7562)
* Wenn Sie in bearbeitbaren Inhalten im Web nach Zeichen oder Wörtern von einem Listenelement zu einem anderen mit den Pfeiltasten gehen, wird jetzt die Eingabe des neuen Listenelements mitgeteilt. (#11569)
* NVDA liest jetzt die richtige Zeile vor, wenn der System-Cursor am Ende eines Links am Ende eines Listenelements in Google Text und Tabellen oder anderen bearbeitbaren Inhalten im Web platziert wird. (#11606)
* Unter Windows 7 setzt das Öffnen und Schließen des Startmenüs vom Desktop aus den Fokus korrekt. (#10567)
* Wenn "Versuch, abgelaufene Fokus-Ereignisse abzubrechen" aktiviert ist, wird der Titel der Registerkarte jetzt beim Wechseln der Registerkarten in Firefox erneut angekündigt. (#11397)
* NVDA meldet kein Listenelement mehr zurück, nachdem ein Zeichen in eine Liste eingegeben wurde, wenn die Ivona-Stimmen (SAPI5) verwendet werden. (#11651)
* Es ist wieder möglich, den Suchmodus beim Lesen von E-Mails in Windows 10 Mail 16005.13110 und neuer zu verwenden. (#11439)
* Bei Verwendung der Ivona-Stimmen (SAPI5) von harposoftware.com kann NVDA jetzt die Konfiguration speichern, die Sprachausgabe wechseln und nach dem Neustart nicht mehr stumm bleiben. (#11650)
* Es ist jetzt möglich, Nummer 6 in Computer-Braille über eine Braille-Tastatur auf HIMS-Braillezeilen einzugeben. (#11710)
* Wesentliche Leistungsverbesserungen in Azure Data Studio. (#11533, #11715)
* Wenn "Versuch, die Sprachausgabe für abgelaufene Fokus-Ereignisse abzubrechen" aktiviert ist, wird der Titel des NVDA-Suchdialogs erneut mitgeteilt. (#11632)
* NVDA sollte beim Aufwecken des Computers nicht mehr einfrieren, wenn der Fokus in einem Microsoft Edge-Dokument landet. (#11576)
* Nach dem Schließen eines Kontextmenüs in Microsoft Edge muss nicht mehr die Tabulatortaste gedrückt oder der Fokus verschoben werden, damit der Suchmodus wieder funktioniert. (#11202)
* NVDA kann Elemente in Listenansichten in einer 64-Bit-Anwendung wie Tortoise SVN nicht mehr lesen. (#8175)
* ARIA-Treegrids werden jetzt sowohl in Firefox als auch in Chrome als normale Tabellen im Suchmodus angezeigt. (#9715)
* Eine umgekehrte Suche kann jetzt mit der Rückwärtssuche über NVDA+Umschalt+F3 erfolgen. (#11770)
* Ein NVDA-Skript wird nicht mehr als wiederholt behandelt, wenn zwischen den beiden Ausführungen des Skripts ein nicht zusammenhängender Tastendruck erfolgt. (#11388)
* Strong- und Emphasis-Tags im Internet Explorer können wieder unterdrückt werden, indem man die Report Emphasis in den NVDA-Einstellungen unter "Dokument-Formatierung" ausschaltet. (#11808)
* Ein Einfrieren von mehreren Sekunden, das bei einer kleinen Anzahl von Benutzern beim Navigieren mit den Pfeiltasten zwischen Zellen in Microsoft Excel auftritt, sollte nicht mehr auftreten. (#11818)
* In Microsoft Teams-Builds mit Versionsnummern wie 1.3.00.28xxx schlägt NVDA das Lesen von Nachrichten in Chats oder Team-Channels auf Grund eines falsch fokussierten Menüs nicht mehr fehl. (#11821)
* Text, der in Google Chrome gleichzeitig als Rechtschreib- und Grammatikfehler markiert ist, wird von NVDA entsprechend als Rechtschreib- und Grammatikfehler mitgeteilt. (#11787)
* Bei Verwendung von Microsoft Outlook (französisches Gebietsschema) funktioniert die Verknüpfung für "Allen antworten" (Strg+Umschalt+R) wieder. (#11196)
* In Visual Studio werden IntelliSense-Tooltipps, die zusätzliche Details zum aktuell ausgewählten IntelliSense-Element enthalten, nur noch einmal mitgeteilt. (#11611)
* In Windows 10-Rechner gibt NVDA den Fortschritt der Berechnungen nicht aus, wenn die Ansage der Zeichen während der Eingabe deaktiviert sind. (#9428)
* NVDA stürzt nicht mehr bei der Verwendung der amerikanische Kurzschrift ab und Sie mit aktiviertem Cursor auf Computer-Braille umschalten, wenn bestimmte Inhalte wie eine URL in Braille angezeigt werden. (#11754)
* In Microsoft Excel ist es wieder möglich, Formatierungsinformationen für die aktuelle Zelle mit NVDA+F abzufragen. (#11914)
* Die QWERTZ-Eingabe auf Papenmeier-Braillezeilen, die dies unterstützen, funktioniert wieder und bewirkt nicht mehr, dass NVDA zufällig einfriert. (#11944)
* In Chromium-basierten Browsern wurden mehrere Fälle behoben, in denen die Tabellen-Navigation nicht funktionierte und NVDA nicht die Anzahl der Zeilen und/oder Spalten der Tabelle meldete. (#12359)

### Änderungen für Entwickler

* Systemtests können jetzt Schlüssel mit "spy.emulateKeyPress" senden, das einen Schlüsselbezeichner verwendet, der mit den NVDA-eigenen Schlüsselnamen übereinstimmt und standardmäßig auch blockiert, bis die Aktion ausgeführt wird. (#11581)
* NVDA benötigt nicht mehr das aktuelle NVDA-Anwendungsverzeichnis, um zu funktionieren. (#6491)
* Die Einstellung "Aria Live Politeness" für Live-Regionen kann jetzt auf NVDA-Objekten mit der Eigenschaft "liveRegionPoliteness" gefunden werden. (#11596)
* Es ist nun möglich, separate Gesten für Outlook- und Word-Dokumente zu definieren. (#11196)

## 2020.3

Diese Version enthält mehrere große Verbesserungen der Stabilität und Leistung, insbesondere bei Microsoft Office-Anwendungen. Es gibt neue Einstellungen zum Umschalten zwischen Touchscreen-Unterstützung und Ansage von Grafiken.
Markierte (hervorgehobenene) Inhalte kann man in Browsern sich ansagen lassen. Außerdem gibt es neue deutsche Braille-Tabellen.

### Neue Features

* Sie können nun die Ansage der Einstellung von Grafiken aus den Dokument-Formatierungen von NVDA ausschalten. Beachten Sie, dass die Deaktivierung dieser Option weiterhin die alternativen Texte von Grafiken vorliest. (#4837)
* Sie können jetzt die Touchscreen-Unterstützung von NVDA umschalten. In den Einstellungen von NVDA wurde eine Option für Berührungsinteraktion auf Touchscreens hinzugefügt. Die Standard-Tastenkombination ist NVDA+Strg+Alt+T. (#9682)
* Neue deutsche Braille-Tabellen hinzugefügt. (#11268)
* NVDA erkennt jetzt schreibgeschützte Text-UIA-Steuerelemente. (#10494)
* Markierter (hervorgehobener) Text wird sowohl mit der Sprachausgabe als auch in Braille in allen Web-Browsern ausgegeben. (#11436)
 * Dies kann durch die Option in den Dokument-Formatierung von NVDA für die Hervorhebung ein- und ausgeschaltet werden.
* Tasten für die emulierte Systemtastatur können über das Dialogfeld für die Tastenbefehle von NVDA hinzugefügt werden. (#6060)
  * Klicken Sie dazu die Schaltfläche "Hinzufügen", nachdem Sie die Kategorie "Tasten der emulierten Systemtastatur" ausgewählt haben.
* Active Braille mit Joystick von HandyTech wird nun unterstützt. (#11655)
* Die Einstellung "Automatischer Fokusmodus für Bewegung des System-Cursors" ist nun kompatibel mit der Deaktivierung von "Automatisch den Fokus auf fokussierbare Elemente setzen". (#11663)

### Änderungen

* Das Skript für die Berichtsformatierung (NVDA+F) wurde jetzt so geändert, dass die Formatierung unter dem System-Cursor und nicht an der Cursor-Position des NVDA-Cursors ausgegeben wird. Um die Formatierung an der Cursor-Position zu erhalten, betätigen Sie NVDA+Umschalt+F. (#9505)
* NVDA setzt den System-Fokus im Lesemodus nicht mehr automatisch standardmäßig auf fokussierbare Elemente, wodurch Leistung und Stabilität verbessert werden. (#11190)
* CLDR von Version 36.1 auf Version 37 aktualisiert. (#11303)
* eSpeak-NG auf 1.51-dev aktualisiert, 1fb68ffffffea4
* Sie können jetzt die Tabellennavigation in Listenfeldern mit auswählbaren Listenelementen verwenden, wenn die jeweilige Liste mehrere Spalten enthält. (#8857)
* Wenn Sie eine Erweiterung in NVDA entfernen und Sie aufgefordert werden, dies zu bestätigen, ist der Schalter "Nein" jetzt standardmäßig ausgewählt. (#10015)
* In Microsoft Excel zeigt das Dialogfeld für die Elementliste jetzt Formeln in der entsprechenden Sprache der Anwendung an. (#9144)
* NVDA teilt nun die korrekte Terminologie für Anmerkungen in Microsoft Excel mit. (#11311)
* Wenn Sie den Befehl "NVDA-Cursor zum Fokus ziehen" im Lesemodus verwenden, wird der NVDA-Cursor jetzt auf die Position des virtuellen Cursors gesetzt. (#9622)
* Im Lesemodus angezeigte Informationen, wie z. B. die Informationen zur Textformatierung mit NVDA+F, werden nun in einem etwas größeren Fenster zentriert auf dem Bildschirm angezeigt. (#9910)

### Fehlerbehebungen

* NVDA spricht nun immer, wenn man nach Wörtern navigiert und auf einem einzelnen Symbol, gefolgt von einem Leerzeichen, landet, unabhängig von den Ausführlichkeitseinstellungen. (#5133)
* Bei Anwendungen, die QT 5.11 oder neuer verwenden, werden wieder Objekt-Beschreibungen mitgeteilt. (#8604)
* Wenn ein Wort mit Strg+Entf gelöscht wird, schweigt NVDA nicht mehr. (#3298, #11029)
  * Es wird nun das nächste Wort davon angesagt.
* In den allgemeinen Einstellungen ist die Sprachliste jetzt korrekt sortiert. (#10348)
* Im Dialogfeld für die Tastenbefehle wurde die Leistung beim Filtern erheblich verbessert. (#10307)
* Sie können nun Unicode-Zeichen, die über U+FFFF hinausgehen, von einer Braillezeile aus senden. (#10796)
* NVDA sagt das Dialogfeld "Öffnen mit" in Windows 10 Mai 2020 Update an. (#11335)
* Eine neue experimentelle Option in den erweiterten Einstellungen (Selektive Registrierung für UIA-Ereignisse und Eigenschaftsänderungen aktivieren) kann bei Aktivierung erhebliche Leistungsverbesserungen in Microsoft Visual Studio und anderen UIAutomation-basierten Anwendungen bieten. (#11077, #11209)
* Bei überprüfbaren Listeneinträgen wird der ausgewählte Zustand nicht mehr redundant angesagt und gegebenenfalls wird stattdessen der nicht ausgewählte Zustand mitgeteilt. (#8554)
* Mit dem Windows 10 Mai 2020 Update zeigt NVDA jetzt den Microsoft Sound Mapper an, wenn die Ausgabegeräte im Dialogfeld für die Sprachausgabe eingestellt wird. (#11349)
* In Internet Explorer werden Zahlen jetzt bei geordneten Listen korrekt angesagt, wenn die Liste nicht mit der Zahl 1 beginnt (#8438)
* In Google Chrom meldet NVDA jetzt für alle aktivierbaren Kontrollen (nicht nur für Kontrollkästchen), die derzeit nicht aktiviert sind, dass sie nicht aktiviert sind. (#11377)
* Es ist wieder möglich, in verschiedenen Bedienelementen zu navigieren, wenn  Aragonisch als Sprache in NVDA verwendet wird. (#11384)
* NVDA sollte teilweise nicht mehr verstummen in Microsoft Word, wenn man schnell die Tasten Pfeil nach oben und/oder Pfeil nach unten drückt oder Zeichen über die Braille-Eingabe eintippt. (#11431, #11425, #11414)
* NVDA hängt keine Leerzeichen beim Kopieren des aktuellen Navigator-Objekts in die Zwischenablage mehr am Ende an. (#11438)
* Wenn kein Text vorhanden ist, führt NVDA auch die "Alles Lesen"-Funktion nicht mehr aus. (#10899, #9947)
* NVDA liest nun die Features-Liste im Internet-Informations-Service (IIS) vor. (#11468)
* NVDA hält das Audiogerät nun offen und verbessert die Leistung einiger Soundkarten (#5172, #10721)
* NVDA friert nicht mehr ein oder wird nicht mehr beendet, wenn in Microsoft Word die Tastenkombination Strg+Umschalttaste+Pfeil nach unten gedrückt wird. (#9463)
* In der Navigationsbaumansicht auf drive.google.com wird der Zustand, ob ein Verzeichnis eingeklappt oder ausgeklappt ist, immer von NVDA angesagt. (#11520)
* NVDA erkennt nun die Braillezeile NLS eReader von Humanware über Bluetooth automatisch, da der Bluethooth-Name nun "NLS eReader Humanware" lautet. (#11561)
* Wesentliche Leistungsverbesserungen in Visual Studio Code. (#11533)

### Änderungen für Entwickler

* BoxSizerHelper.addDialogDismissButtons der GUI-Hilfe unterstützt ein neues "getrenntes" Schlüsselwort-Argument zum Hinzufügen eines horizontalen Standard-Trennzeichens zu Dialogen (mit Ausnahme von Meldungen und einzelnen Eingabefeldern). (#6468)
* Den Anwendungsmodulen wurden zusätzliche Eigenschaften hinzugefügt, darunter der Pfad für die ausführbare Datei (appPath), eine Windows-Store-Anwendung (isWindowsStoreApp) und die Anwendungs-Architektur (appArchitecture). (#7894)
* Es ist jetzt möglich, Anwendungsmodule für in wwahost.exe gehostete Anwendungen unter Windows 8 und neuer zu erstellen. (#4569)
* Ein Protokoll-Abschnitt kann nun markiert werden und dann mit NVDA+Strg+Umschalt+F1 in die Zwischenablage kopiert werden. (#9280)
* Spezifische Objekte in NVDA, die vom zyklischen Garbage-Collector von Python gefunden werden, werden jetzt beim Löschen durch den Collector protokolliert, um das Entfernen von Referenzzyklen aus NVDA zu unterstützen. (#11499)
 * Die Mehrzahl der NVDA-Klassen wird verfolgt, darunter NVDAObjects, appModules, GlobalPlugins, SynthDrivers und TreeInterceptors.
 * Eine Klasse, die verfolgt werden muss, sollte von "garbageHandler.TrackedObject" erben.
* Signifikante Debug-Protokollierung für MSAA-Ereignisse kann nun in den erweiterten Einstellungen von NVDA aktiviert werden. (#11521)
* MSAA-Ereignisse von Windows für das aktuell fokussierte Objekt werden nicht mehr zusammen mit anderen Ereignissen herausgefiltert, wenn die Ereignisanzahl für einen bestimmten Thread überschritten wird. (#11520)

## 2020.2

Zu den Highlights dieser Version gehören die Unterstützung für eine neue Braillezeile von Nattiq, verbessere Unterstützung für ESET Antivirus und Windows-Terminal, Leistungsverbesserungen in 1Password und mit Windows OneCore-Sprachausgaben und viele wietere wichtige Fehlerbehebungen und Verbesserungen.

### Neue Features

* Unterstützungen neuer braillezeilen::
  * Nattiq nBraille (#10778)
* Ein Skript zum Öffnen des NVDA-Benutzerverzeichnis wurde hinzugefügt (ist keinem Tastenbefehl zugeordnet). (#2214)
* Verbesserte Unterstützung für die Oberfläche von ESET Antivirus. (#10894)
* Unterstützung für das Windows-Terminal hinzugefügt. (#10305)
* Ein Befehl zum Ansagen des aktiven Konfigurationsprofils wurde hinzugefügt (ohne Standard-Tastenbefehl). (#9325)
* Ein Tastenbefehl wurde hinzugefügt, um die Ansage von hoch- und tiefgestellten Zeichen umzuschalten (ohne Standard-Tastenbefehl). (#10985)
* In Web-Anwendungen (z. B. Gmail) werden beim schnellen Navigieren mit dem Fokus nicht länger veraltete Informationen mehr angesagt. (#10885)
  * Diese experimentelle Funktion muss manuell über die Option "Sprachausgabe unterbrechen, wenn das Ereignis für den Fokus abgelaufen ist" im Erweiterten Einstellungsfenster aktiviert werden.
* Viele weitere Symbole wurden ergänzt. (#11105)

### Änderungen

* Der Braille-Übersetzer LibLouis wurde von Version 3.12.0 auf [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0) aktualisiert. (#10832, #11221)
* Die Ansage von hoch- und tiefgestellte Zeichen werden nun getrennt von den Meldungen der Schrift-Attribute gesteuert. (#10919)
* Auf Grund von Änderungen im VS-Code deaktiviert NVDA den Lesemodus im Code standardmäßig nicht mehr. (#10888)
* NVDA sagt nicht mehr "Nach oben" und "Nach unten" an, wenn der NVDA-Cursor direkt auf das erste oder letzte Zeichen der Zeile für das aktuelle Navigator-Objekt mit der Bewegung zum Anfang der Zeile bzw. zum Ende der Zeile bewegt wird. (#9551)
* NVDA sagt nicht mehr "Nach links" und "Nach rechts" an, wenn der NVDA-Cursor direkt auf das erste oder letzte Zeichen der Zeile für das aktuelle Navigator-Objekt mit der Bewegung zum Anfang der Zeile bzw. zum Ende der Zeile bewegt wird. (#9551)

### Fehlerbehebungen

* NVDA startet nun korrekt, wenn keine Protokolldatei angelegt werden konnte. (#6330)
* In neueren Versionen von Microsoft Word 365 meldet NVDA nicht mehr, dass "Rückwort löschen" beim Drücken von Strg+Rücktaste während der Bearbeitung eines Dokuments gelöscht wird. (#10851)
* In Winamp meldet NVDA wieder die Umschaltung von der Zufallswiedergabe und der Wiederholen. (#10945)
* Korrektur der Mausverfolgung für einige MSHTML-Elemente in Internet Explorer. (#10736)
* NVDA reagiert nicht mehr extrem langsam beim navigieren in den Listeneinträgen in 1Password. (#10508)
* Die Windows OneCore-Sprachausgabe verzögert nicht mehr bei den Ansagen. (#10721)
* NVDA hängt sich nicht mehr auf, sobald Sie das Kontextmenü für 1Passwort aus dem Infobereich heraus öffnen. (#11017)
* In Microsoft Office 2013 und älter:
  * Die Menübänder werden angesagt, sobald sie fokussiert werden. (#4207)
  * Kontextmenüeinträge werden wieder korrekt vorgelesen. (#9252)
  * Die Menübänder werden beim Navigieren mit Strg+Pfeiltasten durchgehend angesagt. (#7067)
* Im Lesemodus in Mozilla Firefox und Google Chrome wird Text nicht mehr fälschlicherweise in einer separaten Zeile angezeigt, wenn Web-Inhalte die CSS-Darstellung verwenden: Inline-Flex. (#11075)
* Im Lesemodus mit deaktiviertem automatischen Setzen des System-Fokus auf fokussierbare Elemente ist es nun möglich, Elemente zu aktivieren, die durch Drücken der Tabulatortaste erreicht werden. (#8528)
* Im Lesemodus mit deaktiviertem automatischen Setzen des System-Fokus auf fokussierbare Elemente werden bestimmte Elemente aktiviert und der Klick wird nicht mehr an einer falschen Stelle ausgeführt. (#9886)
* Es sind keine NVDA-Fehlertöne mehr zu hören, wenn auf Textsteuerelemente von DevExpress zugegriffen wird. (#10918)
* Die Tool-Tipps der Symbole im Infobereich werden bei der Tastatur-Navigation nicht mehr gemeldet, wenn ihr Text mit dem Namen der Icons übereinstimmt, um eine doppelte Ansage zu vermeiden. (#6656)
* Im Lesemodus mit deaktiviertem "Automatisch den System-Fokus auf fokussierbare Elemente setzen" fokussiert der Wechsel in den Fokusmodus mit NVDA+Leertaste nun das Element unter dem Cursor. (#11206)
* Auf bestimmten Systemen kann wieder nach NVDA-Updates gesucht werden, z. B. nach einer sauberen Windows-Installationen. (#11253)
* Der Fokus wird in einer Java-Anwendung nicht mehr verschoben, wenn die Auswahl in einem unfokussierten Bereich geändert wird. (#5989)

### Änderungen für Entwickler

* Die Funktionen "execElevated" und "hasUiAccess" sind vom Konfigurationsmodul in das "systemUtils"-Modul umgezogen. Die Verwendung über das Konfigurationsmodul ist veraltet. (#10493)
* Das Python-Modul "configObj" wurde auf Version 5.1.0dev Commit f9a265c4 aktualisiert. (#10939)
* Automatisiertes Testen von NVDA mit Google Chrome und einem HTML-Beispiel ist nun möglich. (#10553)
* Das Modul "IAccessibleHandler" wurde in ein Paket umgewandelt, "OrderedWinEventLimiter" wurde in ein Modul ausgelagert und Unit-Tests hinzugefügt. (#10934)
* BrlApi auf Version 0.8 (BRLTTY 6.1) aktualisiert. (#11065)
* Die Ansage der Statusleiste kann nun durch ein Anwendungsmodul angepasst werden. (#2125, #4640)
* NVDA reagiert nicht mehr auf "EVENT_OBJECT_REORDER" von "IAccessible". (#11076)
* Ein defektes ScriptableObject (z. B. ein GlobalPlugin, bei dem ein Aufruf der "init"-Methode dessen Basisklasse fehlt) unterbricht nicht mehr die Skriptbehandlung von NVDA. (#5446)

## 2020.1

Zu den Highlights dieser Version gehört die Unterstützung mehrerer neuer Braillezeilen von Humanware und APH sowie viele andere wichtige Fehlerbehebungen, wie z. B. die Möglichkeit, mit MathPlayer / MathType wieder Mathematik in Microsoft Word lesen zu können.

### Neue Features

* Das aktuell ausgewählte Element in Ausklapplisten wird im Lesemodus in Google Chrome wieder angezeigt, ähnlich wie in NVDA 2019.1. (#10713)
* Sie können nun einen rechthen Mausklick auf Geräten mit Touchscreens ausführen, indem Sie mit einem Finger tippen und halten. (#3886)
* Unterstützung für neue Braillezeilen: APH Chameleon 20, APH Mantis Q40, Humanware BrailleOne, BrailleNote Touch v2 und NLS eReader. (#10830)

### Änderungen

* NVDA verhindert nun, dass das System sich abschaltet oder in den Schlafmodus wechselt, während Alles Lesen aktiviert ist. (#10643)
* Unterstützung für Out-of-Process iFrames in Mozilla Firefox. (#10707)
* Der Braille-Übersetzer LibLouis wurde auf Version 3.12 aktualisiert. (#10161)

### Fehlerbehebungen

* Ein Problem wurde behoben, bei dem das Unicode-Minus-Symbol nicht angesagt wurde (U+2212). (#10633)
* Bei der Installation von Erweiterungen aus dem Dialog "Erweiterungen verwalten" werden die Datei- und Ordnernamen nicht mehr doppelt gemeldet. (#10620, #2395)
* In Mozilla Firefox werden nun beim Laden von Mastodon mit aktivierter erweiterter Web-Oberfläche im Lesemodus alle Zeitleisten korrekt gerendert. (#10776)
* Ein Problem wurde behoben, bei dem nicht ausgewählte Kontrollkästchen im Lesemodus manchmal nicht angesagt wurden. (#10781)
* Die ARIA-Umschaltelemente melden nicht mehr verwirrende Informationen wie "nicht gedrückt aktiviert" oder "gedrückt aktiviert". (#9187)
* Ein Problem wurde behoben, bei dem SAPI4-Stimmen bestimmte Texte nicht ansagten. (#10792)
* NVDA kann wieder mathematische Gleichungen in Microsoft Word lesen und mit ihnen interagieren. (#10803)
* NVDA sagt wieder an, dass der Text im Lesemodus nicht ausgewählt ist, wenn nach dem Auswählen des Textes eine Pfeiltaste gedrückt wird. (#10731).
* NVDA beendet sich nicht mehr selbst, wenn ein Fehler bei der Initialisierung von eSpeak auftritt. (#10607)
* Während des Installationsvorgangs bricht das Installationsprogramm nicht mehr ab, wenn ein Unicode-Zeichen in der Tastenkombination für die Desktopverknüpfung unerwarteter Weise auftritt. Es wird stattdessen die englische Originalbezeichnung verwendet. (#5166, #6326)
* Beim Navigieren mit den Pfeiltasten bzw. beim Verlassen von Listen und Tabellen wird während Alles Lesen nicht mehr ständig "listenende" oder tabellenende" angesagt. (#10706)
* Korrektur der Mausverfolgung für einige MSHTML-Elemente in Internet Explorer. (#10736)

### Änderungen für Entwickler

* Die Entwickler-Dokumentation wird zukünftig mit Sphinx erstellt. (#9840)
* Mehrere Sprachfunktionen wurden in zwei Teile aufgeteilt. (#10593)
  Die speakX-Version bleibt bestehen, hängt aber nun von einer getXSpeech-Funktion ab, die eine Sprachsequenz zurückgibt.
  * speakObjectProperties verlässt sich jetzt auf getObjectPropertiesSpeech.
  * speakObject verlässt sich jetzt auf getObjectSpeech.
  * speakTextInfo setzt jetzt auf getTextInfoSpeech.
  * speakWithoutPauses wurde zu einer Class konvertiert und refaktorisiert, sollte aber die Kompatibilität nicht beeinträchtigen.
  * Die Klasse "getSpeechForSpelling" ist veraltet (aber immer noch verfügbar), verwenden Sie stattdessen "getSpellingSpeech".
  Kernänderungen, die jedoch die Entwickler von Erweiterungen nicht betreffen sollten:
  * _speakPlaceholderIfEmpty wurde in _getPlaceholderSpeechIfTextEmpty umbenannt.
  * _speakTextInfo_addMath wurde in _extendSpeechSequence_addMathForTextInfo umbenannt.
* Die Klasse Speech 'reason' wurde in eine Enum umgewandelt (siehe Klasse controlTypes.OutputReason). (#10703)
  * Die Konstanten der Modulebene "REASON_*" sind nicht mehr verfügbar.
* Visual Studio 2019 (16.2 oder neuer) wird zum Kompilieren von NVDA-Abhängigkeiten benötigt. (#10169)
* SCons auf Version 3.1.1 aktualisiert. (#10169)
* Die Funktion behaviors._FakeTableCell kann wieder ohne definierte Position genutzt werden. (#10864)

## 2019.3

NVDA 2019.3 ist ein umfangreiches Release, das viele Änderungen unter der Haube mit sich bringt. Darunter das Upgrade von Python 2 auf Python 3 und ein komplett neu überarbeitetes Subsystem für die Sprachausgaben in NVDA.
Obwohl diese Änderungen die Kompatibilität mit älteren NVDA-Erweiterungen nicht mehr besteht, ist das Upgrade auf Python 3 aus Sicherheitsgründen notwendig. Weitere Änderungen an der Sprachausgabe folgen in naher Zukunft.
 Weitere Highlights in dieser Version sind die 64-Bit-Unterstützung für Java-VMs, die Funktionalität für den Bildschirmvorhang und die Fokus-Hervorhebung, die Unterstützung weiterer Braillezeilen und einem neuen Braille-Betrachter sowie diverse Fehlerbehebungen.

### Neue Features

* Die Genauigkeit des Befehls zum Ziehen der Maus zum Navigator-Objekt wurde in Textfeldern in Java-Anwendungen verbessert. (#10157)
* Unterstützung für die folgenden HandyTech-Braillezeilen hinzugefügt (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Alle Tastenbefehle können nun über einen neuen Schalter "Auf Standard-Einstellungen zurücksetzen" im Dialogfeld "Tastenbefehle" entfernt werden. (#10293)
* Die Ansage der Schriftarten in Microsoft Word berücksichtigt nun auch, wenn Text als Verborgen markiert ist. (#8713)
* Es wurde ein Befehl hinzugefügt, um den NVDA-Cursor an die zuvor als Startmarke für die Auswahl oder das Kopieren markierte Position zu bewegen: NVDA+Umschalt+F9. (#1969)
* In Internet Explorer, Microsoft Edge und neue Versionen von Mozilla Firefox und Google Chrome werden Sprungmarken nun auch im Fokusmodus und Objekt-Navigation angesagt. (#10101)
* In Internet Explorer, Google Chrome und Mozilla Firefox können Sie nun mit Hilfe der Schnellnavigationsbefehle zu Artikeln und Gruppierungen navigieren. Diese Befehle sind standardmäßig nicht zugewiesen und können im Dialogfeld "Tastenbefehle" zugewiesen werden, wenn das Dialogfeld aus einem Dokument im Lesemodus geöffnet wird. (#9485, #9227)
 * Es werden auch Illustrationen erkannt und angesagt. Sie gelten als Objekte und sind daher mit der Schnellnavigationstaste "o" navigierbar.
* In Internet Explorer, Google Chrome und Mozilla Firefox werden nun Artikel-Elemente in der Objektnavigation und optional im Lesemodus angezeigt, wenn sie in den Einstellungen für die Dokumentenformatierung aktiviert sind. (#10424)
* Die Funktion eines Bildschirmvorhangs wurde hinzugefügt, die bei Aktivierung den gesamten Bildschirminhalt unter Windows 8 und neuer ausblendet und das Bildschirm verdunkelt. (#7857)
 * Ein Skript zum Aktivieren des Bildschirmvorhangs wurde hinzugefügt, jedoch wurde kein Tastenbefehl zugewiesen. Bei einmal Drücken wird der Bildschirmvorhang bis zum nächsten Neustart aktiviert. Bei zweimal Drücken wird er immer ausgeführt, sofern NVDA verwendet wird.
 * Dies kann über die Kategorie "Visuelle Darstellungen" im Einstellungsdialog von NVDA aktiviert und konfiguriert werden.
* NVDA wurde um eine Funktion zur visuellen Hervorhebung des Fokus erweitert. (#971, #9064)
 * Die Hervorhebung von System Fokus, Navigator-Objekt und virtuellen Cursor im Lesemodus kann über die Kategorie "visuelle Darstellungen" im Einstellungsdialog von NVDA aktiviert und konfiguriert werden.
 * Hinweis: Diese Funktion ist nicht mit der Erweiterung "Fokus hervorheben" kompatibel, jedoch kann die Erweiterung weiterhin verwendet werden, während die eingebaute Hervorhebungsfunktion deaktiviert ist.
* Braille-Betrachter hinzugefügt, ermöglicht die Anzeige der Braille-Ausgabe über den Bildschirm. (#7788)

### Änderungen

* Im Benutzerhandbuch wird nun beschrieben, wie Sie NVDA in der Windows-Konsole verwenden können. (#9957)
* Wenn Sie die Datei "nvda.exe" ausführen, wird nun standardmäßig ein bereits laufender Prozess von NVDA ersetzt. Der Befehlszeilenparameter "-r" oder "---replace" wird weiterhin akzeptiert, jedoch ignoriert. (#8320)
* Unter Windows 8 und neuer wird NVDA nun Produktnamen und Versionsinformationen für gehostete Anwendungen, wie beispielsweise Anwendungen, die aus dem Microsoft Store heruntergeladen wurden, unter Verwendung der von der Anwendung bereitgestellten Informationen mitteilen. (#4259, #10108)
* Beim Ein- und Ausschalten der Änderungsverfolgung mit der Tastatur in Microsoft Word meldet NVDA den Status der Einstellung. (#942) 
* Die NVDA-Versionsnummer wird nun als erste Meldung im Protokoll angezeigt. Dies geschieht auch dann, wenn die Protokollierung über die Einstellungen deaktiviert wurde. (#9803)
* Der Einstellungsdialog lässt es nicht mehr zu, die konfigurierte Protokollstufe zu ändern, wenn sie von der Kommandozeile aus überschrieben wurde. (#10209)
* In Microsoft Word meldet NVDA nun den Anzeigestatus von nicht druckbaren Zeichen, wenn Sie die Umschalt-Taste Strg+Umschalt+8 drücken. (#10241)
* Der Braille-Übersetzer LibLouis wurde auf den Commit 58d67e63 aktualisiert. (#10094)
* Wenn die CLDR-Zeichen (einschließlich Emojis) aktiviert sind, werden sie auf allen Interpunktionsebenen angezeigt. (#8826)
* Python-Pakete von Drittanbietern, die in NVDA enthalten sind, wie beispielsweise comtypes, protokollieren nun ihre Warnungen und Fehler im NVDA-Protokoll. (#10393)
* Die Emoji-Anmerkungen der Unicode Common Locale Data Repository wurden auf Version 36.0 aktualisiert. (#10426)
* Beim Hervorheben einer Gruppe im Lesemodus wird nun auch die Beschreibung vorgelesen. (#10095)
* Die Java Access Bridge ist nun im NVDA enthalten, um den Zugriff auf Java-Anwendungen zu ermöglichen, auch für 64-Bit-Java-VMs. (#7724)
* Wenn die Java Access Bridge für den Benutzer nicht aktiviert ist, aktiviert NVDA sie automatisch beim Start von NVDA. (#7952)
* eSpeak-NG aktualisiert auf 1.51-dev, Commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Fehlerbehebungen

* Emoji und andere 32-Bit-Unicode-Zeichen benötigen nun weniger Platz auf einer Braillezeile, wenn sie als hexadezimale Werte angezeigt werden. (#6695)
* Unter Windows 10 meldet NVDA Sprechblasen aus universellen Anwendungen, wenn im Dialogfeld "Objektdarstellung" NVDA konfiguriert ist, um Benachrichtigungen mitzuteilen. (#8118)
* Bei Windows 10 Anniversary Update und neuer wird der eingegebene Text nun in Mintty angezeigt. (#1348)
* Bei Windows 10 Anniversary Update und neuer wird die Ausgabe in der Windows-Konsole, die in der Nähe des Einfügemarke erscheint, nicht mehr buchstabiert. (#513)
* Die Steuerelemente im Kompressor von Audacity werden nun beim Navigieren durch das Dialogfeld angesagt. (#10103)
* NVDA behandelt Leerzeichen nicht mehr als Wörter in der Objektprüfung in Scintilla-basierten Editoren wie Notepad++. (#8295)
* NVDA verhindert, dass das System in den Ruhezustand wechselt, wenn mit den Gesten auf der Braillezeile durch Text navigiert wird. (#9175)
* Unter Windows 10 folgt nun die Braille-Anzeige bei der Bearbeitung von Zellinhalten in Microsoft Excel und anderen UIA-Text-Steuerelementen. (#9749)
* NVDA meldet wieder Vorschläge in der Adressleiste von Microsoft Edge. (#7554)
* NVDA ist nicht mehr stumm, wenn eine HTML-Registerkartenüberschrift im Internet Explorer fokussiert wird. (#8898)
* Im EdgeHTML-basierten Microsoft Edge gibt NVDA keinen Sound für Suchvorschläge mehr aus, wenn das Fenster maximiert ist. (#9110, #10002)
* Kombinationsfelder mit ARIA 1.1 werden nun in Mozilla Firefox und Google Chrome unterstützt. (#9616)
* NVDA meldet nicht mehr den Inhalt von visuell ausgeblendeten Spalten für Listenelemente in SysListView32-Steuerelementen. (#8268)
* Das Dialogfeld für die Einstellungen zeigt im geschützten Modus nicht mehr "Information" als aktuelle Protokollierungsstufe an. (#10209)
* Im Startmenü für Windows 10 Anniversary Update und neuer gibt nun NVDA Details der Suchergebnisse bekannt. (#10340)
* Im Lesemodus, wenn sich das Dokument durch Bewegen des Cursors oder durch Schnellnavigation ändert, spricht NVDA in einigen Fällen nicht mehr den falschen Inhalt. (#8831, #10343)
* Die Aussprache einiger Aufzählungszeichen in Microsoft Word wurde korrigiert. (#10399)
* In Windows 10 Mai 2019 Update und neuer meldet NVDA wieder das erste ausgewählte Emoji oder das Element der Zwischenablage mitteilen, wenn das Dialogfeld für die Emojis oder der Verlauf der Zwischenablage geöffnet ist. (#9204)
* In Poedit ist es wieder möglich, einige Übersetzungen für Sprachen von rechts nach links anzuzeigen. (#9931)
* In den Einstellungen in Windows 10 April 2018 Update und neuer gibt nun NVDA keine Informationen zum Fortschrittsbalken mehr für die Lautstärke auf der Seite für System/Sound bekannt. (#10412)
* Ungültige reguläre Ausdrücke in Sprachwörterbüchern unterbrechen die Sprache in NVDA nicht mehr vollständig. (#10334)
* Beim Lesen von gegliederten Elementen in Microsoft Word mit aktivierter UIA wird der Punkt aus dem nächsten Listenelement nicht mehr unangemessen angekündigt. (#9613)
* Einige Probleme und Fehler bei der Übersetzung von Brailleschrift bei LibLouis wurden behoben. (#9982)
* Java-Anwendungen, die vor NVDA gestartet wurden, sind nun zugänglich, ohne dass die Java-App neu gestartet werden muss. (#10296)
* Wenn im Mozilla Firefox das hervorgehobene Element mit dem Attribut "aria-current" markiert wird, wird diese Änderung nicht mehr mehrfach angesagt. (#8960)
* NVDA behandelt nun bestimmte zusammengesetzte Unicode-Zeichen, wie z. B. das Zeichen é, als ein einziges Zeichen, wenn Sie sich durch Text bewegen. (#10550)
* Spring Tool Suite Version 4 wird nun unterstützt. (#10001)
* Namen werden nicht mehr doppelt angesagt, wenn das Attribut "aria-labelledby" sich in einem inneren Element befindet. (#10552)
* Unter Windows 10 Version 1607 und neuer werden in mehreren Situationen Zeichen während der Eingabe von Braille-Tastaturen zurückgemeldet. (#10569)
* Wenn Sie das Audio-Ausgabegerät wechseln, werden die von NVDA ausgegebenen Töne nun durch das aktuell ausgewählte Gerät wiedergegeben. (#2167)
* In Mozilla Firefox ist nun das Navigieren mit dem Cursor im Lesemodus deutlich schneller. (#10584)

### Änderungen für Entwickler

* Python auf 3.7 aktualisiert. (#7105)
* pySerial auf Version 3.4 aktualisiert. (#8815)
* wxPython wurde auf 4.0.3 aktualisiert, um Python 3.5 und neuer zu unterstützen. (#9630)
* Six auf Version 1.12.0 aktualisiert. (#9630)
* Py2Exe auf Version 0.9.3.2 aktualisiert (in Entwicklung, Commit b372a8e von albertosottile/py2exe#13). (#9856)
* Modul "comtypes" der Datei "UIAutomationCore.dll" auf Version 10.0.18362 aktualisiert. (#9829)
* Die Tab-Vervollständigung in der Python-Konsole schlägt nur dann Attribute vor, die mit einem Unterstrich beginnen, wenn der Unterstrich zuerst eingegeben wird. (#9918)
* Das Werkzeug Flake8 Linting wurde in SCons integriert, die die Code-Anforderungen für Pull-Requests widerspiegeln. (#5918)
* Da NVDA nicht mehr von pyWin32 abhängig ist, sind Module wie win32api und win32con für Erweiterungen nicht mehr verfügbar. (#9639)
 * "win32api"-Aufrufe können durch direkte Aufrufe von "win32.dll"-Funktionen über "ctypes" ersetzt werden.
 * "win32con"-Konstanten sollten in Ihren Dateien definiert werden.
* Das Argument "async" in nvwave.playWaveFile wurde in "asynchronous" umbenannt. (#8607)
* Methoden von speakText und speakCharacter in synthDriver-Objekten werden nicht mehr unterstützt.
 * Diese Funktionalität wird verwendet von SynthDriver.speak.
* SynthSetting-Klassen in synthDriverHandler wurde entfernt. Nun stattdessen die driverHandler.DriverSetting-Klassen verwenden.
* SynthDriver-Klassen sollten den Index nicht mehr über die lastIndex-Eigenschaft freigeben.
 * Stattdessen sollten sie die Aktion "synthDriverHandler.synthIndexReached" mit dem Index benachrichtigen, sobald alle vorherigen Audiodateien vor diesem Index abgespielt wurden.
* Die Klassen "SynthDriver" müssen nun die Aktion "synthDriverHandler.synthDoneSpeaking" melden, sobald alle Audiodaten eines "SynthDriver.speak"-Aufrufs abgespielt wurden.
* Die Klassen "SynthDriver" müssen die speech.PitchCommand in ihrer Sprachmethode unterstützen, da Änderungen in der Tonhöhe für die Rechtschreibung nun von dieser Funktionalität abhängen.
* Die Sprachausgaben-Funktion "getSpeechTextForProperties" wurde in "getPropertiesSpeech" umbenannt. (#10098)
* Die Braille-Funktion "getBrailleTextForProperties" wurde in "getPropertiesBraille" umbenannt. (#10469)
* Mehrere Sprachausgaben-Funktionen wurden geändert, um Sprachsequenzen zurückzugeben. (#10098)
 * getControlFieldSpeech
 * getFormatFieldSpeech
 * getSpeechTextForProperties nennt sich nun getPropertiesSpeech
 * getIndentationSpeech
 * getTableInfoSpeech
* Es wurde ein "textUtils"-Modul hinzugefügt, um die Zeichenkettenunterschiede zwischen Zeichenketten in Python 3 und Windows-Unicode zu vereinfachen. (#9545)
 * Schauen Sie dazu im Module "documentation" und "textInfos.offsets" für die Implementierung des Frameworks bzw. der Beispiele nach.
* Veraltete Funktionen wurden entfernt. (#9548)
 * Anwendungsmodule entfernt:
  * Die Unterstützung des Audiorekorders unter Windows XP.
  * Klango Player, der nicht mehr weiterentwickelt wird.
 * "configobj.validate"-Wrapper entfernt.
  * Im Code sollte nun "from configobj import validate" anstelle "import validate" verwendet werden.
 * "textInfos.Point" und "textInfos.Rect" wurden jeweils ersetzt durch "locationHelper.Point" und "locationHelper.RectLTRB".
 * "braille.BrailleHandler._get_tether" und "braille.BrailleHandler.set_tether" wurden entfernt.
 * "config.getConfigDirs" wurde entfernt.
 * "config.ConfigManager.getConfigValidationParameter" wurde ersetzt durch "getConfigValidation".
 * Die Eigenschaft "inputCore.InputGesture.logIdentifier" wurde entfernt.
   * Verwenden Sie stattdessen "_get_identifiers" in "inputCore.InputGesture".
 * Die Eigenschaften "speakText" und "speakCharacter" in "synthDriverHandler.SynthDriver" wurden entfernt.
 * Mehrere Klassen in "synthDriverHandler.SynthSetting" wurden entfernt.
   * Zuvor aus Gründen der Rückwärtskompatibilität (#8214) aufbewahrt, gilt nun als veraltet.
   * Treiber, die die Klassen "SynthSetting" verwendet haben, sollten aktualisiert werden, um die DriverSetting-Klassen zu verwenden.
 * Einige ältere Code-Abschnitte wurden entfernt, insbesondere:
  * Unterstützung für die Nachrichtenliste in Microsoft Outlook 2003.
  * Eine Overlay-Klasse für das klassische Startmenü, die nur in Windows Vista und älter zu finden waren.
  * Die Unterstützung für Skype 7 wurde eingestellt, da es definitiv nicht mehr funktioniert.
* Ein Framework zur Erstellung von Quellen für Verbesserungen visueller Darstellungen wurde hinzugefügt; Module, die Bildschirminhalte ändern können, optional basierend auf Eingaben von NVDA über Objektpositionen. (#9064)
 * Erweiterungen können eigene Quellen in einem "visionEnhancementProvider"-Ordner bündeln.
 * Schauen Sie dazu im Module "vision" und "visionEnhancementProviders" für die Implementierung des Frameworks bzw. der Beispiele nach.
 * Die Quelle für Verbesserungen visueller Darstellungen ist über die Kategorie "Visuelle Darstellungen" im NVDA-Einstellungsdialog aktivierbar.
* Abstrakte Klassen-Eigenschaften werden nun auch für Objekte unterstützt, die von "baseObject.AutoPropertyObject" erben (z. B. "NVDAObjects" und "TextInfos"). (#10102)
* Einführung von "displayModel.UNIT_DISPLAYCHUNK" als eine für "DisplayModelTextInfo" spezifische Einheitenkonstante für "TextInfos". (#10165)
 * Diese neue Konstante ermöglicht es, den Text in "DisplayModelTextInfo" in einer Weise zu behandeln, die der Speicherung der Textbausteine im zugrunde liegenden Modell ähnelt.
* "displayModel.getCaretRect" gibt nun eine Instanz von locationHelper.RectLTRB zurück. (#10233)
* Die Konstanten "UNIT_CONTROLFIELD" und "UNIT_FORMATFIELD" wurden von "virtualBuffers.VirtualBufferTextInfo" in das Paket "textInfos" verschoben. (#10396)
* Für jeden Eintrag im NVDA-Protokoll werden nun Informationen über den Ursprungs-Thread angezeigt. (#10259)
* TextInfo-Objekte der UIA können nun verschoben / erweitert werden von den Text-Einheiten "page", "story" und "formatField". (#10396)
* Externe Module (appModules und globalPlugins) sind nun weniger wahrscheinlich in der Lage, die Erstellung von NVDA-Objekten zu unterbrechen. 
 * Ausnahmen, die durch die Methoden "chooseNVDAObjectOverlayClasses" und "event_NVDAObject_init" verursacht werden, werden nun korrekt abgefangen und protokolliert.
* Das Wörterbuch "aria.htmlNodeNameToAriaLandmarkRoles" wurde umbenannt in "aria.htmlNodeNameToAriaRoles". Es enthält nun auch Regeln, die keine Sprungmarken sind.
* Die Funktion "scriptHandler.isCurrentScript" wurde auf Grund mangelnder Verwendung entfernt. Es gibt keinen Ersatz dafür. (#8677)

## 2019.2.1

Dies ist eine kleinere Version, um mehrere Abstürze in 2019.2 zu beheben, darunter:

* Mehrere Abstürze in Google Mail , die sowohl in Firefox als auch in Chrome bei der Interaktion mit bestimmten Popup-Menüs auftraten, z. B. beim Erstellen von Filtern oder beim Ändern bestimmter Google Mail-Einstellungen. (#10175, #9402, #8924)
* In Windows 7 führt NVDA nicht mehr zum Absturz von Windows Explorer, wenn die Maus im Startmenü verwendet wird. (#9435)
* Unter Windows 7 stürzt Windows Explorer beim Zugriff auf Metadaten-Eingabefelder nicht mehr ab. (#5337)
* NVDA friert bei der Interaktion mit Bildern mit einem base64-URI in Mozilla Firefox oder Google Chrome nicht mehr ein. (#10227)

## 2019.2

Zu den Highlights dieser Version gehören die automatische Erkennung von braillezeilen von Freedom Scientific, eine experimentelle Einstellung in DEN erweiterten Einstellungen, um die automatische Bewegung des systemfokus beim Verwenden des Lesemodus zu deaktivieren (was unter Umständen zu Leistungsverbesserungen führen kann), eine Option zur Erhöhung der Geschwindigkeit für die Windows OneCore-Sprachausgabe, um sehr schnelle Geschwindigkeiten zu erzielen und viele andere Fehlerbehebungen.

### Neue Features

* NVDA unterstützt nun auch neuere Client-Versionen des Miranda NG. (#9053)
* Sie können den Lesemodus nun standardmäßig deaktivieren, wenn eine Webseite geladen wird. Deaktivieren Sie dazu die neue Option "Lesemodus beim Laden von Webseiten verwenden" in den Lesemodus-Einstellungen im Einstellunfsfenster von NVDA. (#8716)
 * Beachten Sie, dass Sie den Lesemodus mit NVDA+Leertaste manuell aktivieren können, auch wenn diese Option deaktiviert ist.
* Sie können nun Symbole im Dialogfeld "Interpunktion und Symbol-Aussprache" filtern, ähnlich wie das Filtern in der Elementliste und im Dialogfeld "Tastenbefehle". (#5761)
* Es wurde ein Befehl hinzugefügt, um die Auflösung der Maustexteinheit zu ändern, d. h. wie viel Text vorgelesen wird, wenn sich die Maus bewegt. Ein Tastenbefehl wurde nicht zugewiesen. Dies können Sie über das Dialogfeld "Tastenbefehle" selbst vornehmen. (#9056)
* Die Windows OneCore-Sprachausgabe verfügt nun über eine Option, welche eine zusätzliche Erhöhung der Sprechgeschwindigkeit ermöglicht. (#7498)
* Die Option "Geschwindigkeit zusätzlich erhöhen" kann nun über den Einstellungsring der Sprachausgabe für unterstützte Sprachausgaben konfiguriert werden (derzeit eSpeak-NG und Windows OneCore). (#8934)
* Konfigurationsprofile können nun manuell mithilfe von Tastenkürzel aktiviert werden. (#4209)
 * Die Tastenkürzel müssen über das Dialogfeld "Tastenbefehle" konfiguriert werden.
* In eClipse wurde die Unterstützung für die Autovervollständigung im Code-Editor hinzugefügt. (#5667)
 * Zusätzlich können vorhandene JavaDoc-Informationen aus dem Editor über den Tastenbefehl NVDA+d gelesen werden.
* Dem Bereich Erweiterte Einstellungen wurde eine experimentelle Option hinzugefügt, mit der Sie den System-Fokus daran hindern können, dem virtuellen Cursor zu folgen (automatische Bewegung des System-Fokus auf hervorhebbare Elemente ausschalten). (#2039) Diese Option ist nicht für jede Seite von Nutzen, aber für viele Webseiten löst diese Option folgende Probleme:
 * Gummibandeffekt: Der virtuelle Cursor im Lesemodus springt sporadisch zu vorherigen Positionen.
 * Eingabefelder blockieren den System-Fokus, wenn sie auf einigen Webseiten mit Pfeiltaste nach unten navigieren.
 * Die Schnellnavigationstasten im Lesemodus reagieren langsam.
* Einstellungen für Braillezeilen-Treiber können nun direkt in der Benutzeroberfläche von NVDA in der Kategorie Braille-Einstellungen im Einstellungsdialog angepasst werden. Voraussetzung ist, dass der Treiber der Braillezeile dies unterstützt. (#7452)
* Braillezeilen von Freedom Scientific werden nun automatisch unterstützt. (#7727)
* Es wurde ein Befehl hinzugefügt, um den Ersatz für das Symbol unter dem Cursor anzuzeigen. (#9286)
* Dem Bereich Erweiterte Einstellungen wurde eine experimentelle Option hinzugefügt, mit der Sie ein neues, noch nicht abgeschlossenes Refactoring der Unterstützung der Windows-Konsolen von NVDA über die API der UIA von Microsoft ausprobieren können. (#9614)
* In der Python-Konsole unterstützt das Eingabefeld nun das Einfügen mehrerer Zeilen aus der Zwischenablage. (#9776)

### Änderungen

* Die Lautstärke der Sprachausgabe wird nun jeweils um 5 statt um 10 Einheiten erhöht oder verringert, wenn Sie den Einstellungsring verwenden. (#6754)
* Der Text im Dialogfeld "Erweiterungen verwalten..." wurde angepasst, wenn NVDA mit deaktivierten Erweiterungen neu gestartet wird. (#9473)
* Emoji Annotationen vom Unicode Common Locale Data Repository wurden auf Version 35.0 aktualisiert. (#9445)
* Die Tastenkombination für das Eingabefeld "Filtern nach" in der Elementliste im Lesemodus wurde auf Alt+y geändert. (#8728)
* Wenn eine automatisch erkannte Braillezeile über Bluetooth angeschlossen ist, sucht NVDA weiterhin nach Braillezeilen via USB, die vom gleichen Treiber unterstützt werden und wechselt zu einer USB-Verbindung, sobald diese verfügbar ist. (#8853)
* Die Sprachausgabe eSpeak-NG wurde auf Commit 67324cc aktualisiert.
* Der Braille-Übersetzer LibLouis wurde auf Version 3.10.0 aktualisiert. (#9439, #9678)
* NVDA teilt nun das Wort "ausgewählt" mit, nachdem es den Text gemeldet hat, den ein Benutzer gerade ausgewählt hat. (#9028, #9909)
* In Microsoft Visual Studio Code ist der Lesemodus nun standardmäßig deaktiviert. (#9828)

### Fehlerbehebungen

* NVDA stürzt nicht mehr ab, wenn ein Erweiterungsverzeichnis leer ist. (#7686)
* LTR- und RTL-Markierungen werden beim Navigieren zeichenweise oder im Braille im Windowsdialog "Eigenschaften" nicht mehr angezeigt oder angesagt. (#8361)
* Beim Navigieren zu Formularfeldern mit Schnellnavigationstasten im Lesemodus wird nun das gesamte Formularfeld und nicht nur die erste Zeile angesagt. (#9388)
* NVDA stürzt nicht mehr ab, wenn die Windows 10 Mail-App beendet wird. (#9341)
* NVDA startet nun auch wenn die regionalen Einstellungen des Benutzers auf ein für NVDA unbekanntes Gebietsschema wie Englisch (Niederlande) eingestellt sind. (#8726)
* Der Status des Lesemodus wird nun auch nach dem Wechsel des Fensters zwischen MS Excel und einem Fenster mit aktivem Fokusmodus angesagt. (#8846)
* NVDA meldet nun korrekt die Zeile am Mauszeiger in Notepad++ und anderen Scintilla-basierten Editoren. (#5450)
* In Google Docs und anderen webbasierten Editoren zeigt die Braillezeile nicht mehr manchmal fälschlicherweise "lst ende" vor dem Cursor in der Mitte eines Listenelements an. (#9477)
* Im Windows 10 Mai 2019 Update, wenn das Explorer oder Desktop-Fenster fokusiert ist, sagt NVDA nicht mehr viele Lautstärkebenachrichtigungen an, wenn Sie die Lautstärke mit Lautstärketasten ändern. (#9466)
* Das Dialogfeld "Interpunktion und Symbol-Aussprache" wird nun schneller geladen, auch wenn Sie Symbol-Wörterbücher mit mehr als 1000 Einträgen verwenden. (#8790)
* NVDA liest nun die richtige Zeile, wenn der Wortumbruch in Scintilla-Steuerelementen wie Notepad++ aktiviert ist. (#9424)
* In Microsoft Excel werden die Zellenkoordinaten nun auch beim Umschalt+Eingabetaste oder Umschalt+Numpad-Eingabe angesagt. (#9499)
* In Visual Studio 2017 und neuer, im Fenster Objektexplorer, wird das ausgewählte Element im Objektbaum oder Mitgliederbaum mit Kategorien nun korrekt angesagt. (#9311)
* Erweiterungen mit Namen, die sich nur in der Groß- und Kleinschreibung unterscheiden, werden nicht mehr separat behandelt. (#9334)
* Die in NVDA eingestellte Rate für Geschwindigkeit oder Stimmhöhe bei Windows OneCore-Stimmen wird nicht mehr von der in Windows 10 Sprach-Einstellungen eingestellten Rate beeinflusst. (#7498)
* Der Protokollbetrachter kann nun mit NVDA+F1 geöffnet werden, auch wenn es keine Entwicklerinformationen für das aktuelle Navigatorobjekt gibt. (#8613)
* Es ist wieder möglich, die Tabellen-Navigationsbefehle von NVDA in Google Docs unter Mozilla Firefox und Google Chrome zu verwenden. (#9494)
* Die Kipptasten funktionieren nun korrekt bei den Braillezeilen von Freedom Scientific. (#8849)
* Beim Lesen des ersten Zeichens eines Dokuments in Notepad++ 7.7 x64 friert NVDA nicht mehr ein. (#9609)
* In Mozilla Firefox werden Aktualisierungen einer aktiven Region nicht mehr gemeldet, wenn sich die aktive Region in einer Registerkarte im Hintergrund befindet. (#1318)
* Der NVDA-spezifische Suchmodus funktioniert nun wieder, auch wenn das Dialogfeld für die NVDA-Informationen im Hintergrund geöffnet ist. (#8566)
* HTCom kann nun mit einer Braillezeile von HandyTech in Kombination mit NVDA benutzt werden. (#9691)

### Änderungen für Entwickler

* Sie können nun die Eigenschaft "disableBrowseModeByDefault" in Anwendungsmodulen so einstellen, dass der Lesemodus standardmäßig ausgeschaltet ist. (#8846)
* Der erweiterte Fensterstil eines Fensters wird nun mit der Eigenschaft "extendedWindowStyle" auf Fenster-Objekte und deren Derivate angewendet. (#9136)
* Das Paket "comTypes" wurde auf 1.1.7 aktualisiert. (#9440, #8522)
* Das aktuell geladene Anwendungsmodul wird nun zuerst angesagt, wenn Sie den Befehl "report module info" verwenden. (#7338)
* Ein Beispiel zur Demonstration der Verwendung der Datei "nvdaControllerClient.dll" aus C# hinzugefügt. (#9600)
* Dem Modul "winVersion" wurde eine neue Funktion "isWin10" hinzugefügt, die zurückgibt, ob NVDA auf (mindestens) der mitgelieferten Release-Version von Windows 10 (wie 1903) läuft oder nicht. (#9761)
* Die Python-Konsole in NVDA enthält nun weitere nützliche Module im Namensraum (z. B. "appModules", "globalPlugins", "config" und "textInfos"). (#9789)
* Das Ergebnis des zuletzt ausgeführten Befehls in der Python-Konsole in NVDA ist nun über die Variable "_" zugänglich. (#9782)
 * Beachten Sie, dass dies die Übersetzungsfunktion "gettext", die auch "_" (Unterstrich) genannt wird, überschattet. Um die Übersetzungsfunktion aufzurufen: "del _ _".

## 2019.1.1

Diese Version behebt die folgenden Probleme:

* Es kommt in Microsoft Excel 2007 nicht mehr zu Abstürzen, wenn NVDA ansagen soll, ob eine Zelle eine Formel enthält. (#9431)
* Beim Umgang mit Listenfeldern in Google Chrome kommt es nicht mehr zu Abstürzen. (#9364)
* Ein Problem beim Kopieren der Benutzerkonfiguration ins Systemprofil wurde behoben. (#9448)
* Bei der Angabe der Zellkoordinaten für verbundene Zellen in Excel verwendet NVDA nun wieder die übersetzten Meldungen. (#9471)

## 2019.1

Zu den Highlights dieser Version gehören Leistungsverbesserungen beim Zugriff auf Microsoft Word und Excel, Stabilitäts- und Sicherheitsverbesserungen wie die Unterstützung von Erweiterungen mit Versionskompatibilitätsinformationen und viele andere Fehlerbehebungen.

Bitte beachten Sie, dass ab dieser NVDA-Version benutzerdefinierte Anwendungsmodule, GlobalPlugins, Treiber für Braillezeilen und Sprachausgaben nicht mehr automatisch aus Ihrem NVDA-Benutzerkonfigurationsverzeichnis geladen werden.
Vielmehr sollten diese als Teil einer NVDA-Erweiterung installiert werden. Für diejenigen, die Code für eine Erweiterung entwickeln, kann Code zum Testen in ein neues Developer Scratchpad-Verzeichnis im NVDA-Benutzerkonfigurationsverzeichnis verschoben werden. Dies funktioniert nur, wenn die Option Developer-Scratchpad in der neuen NVDA-Einstellungskathegorie "erweitert" aktiviert ist.
Diese Änderungen sind notwendig, um die Kompatibilität von benutzerdefiniertem Code besser zu gewährleisten, sodass NVDA stabil bleibt, wenn dieser Code mit neueren Versionen inkompatibel wird.
Bitte beachten Sie die unten folgende Liste der Änderungen für weitere Details dazu und wie Erweiterungen nun versioniert werden.

### Neue Features

* Neue Braille-Tabellen: Afrikaans, Arabisches 8-Punkt-Computerbraille, Arabische Kurzschrift, Spanische Kurzschrift. (#4435)
* Den Maus-Einstellungen von NVDA wurde eine Option hinzugefügt, womit NVDA nun auch die Maus erkennen kann, selbst wenn diese von einer anderen Anwendung gesteuert wird. (#8452)
 * Dies ermöglicht die Mausverfolgung in NVDA, wenn ein System durch Teamviewer oder ähnliche Software ferngesteuert wird.
* Der Befehlszeilenparameter "--enable-start-on-logon" wurde hinzugefügt, um stille Installationen von NVDA zu ermöglichen, bei welchen NVDA danach standardmäßig nicht auf dem Anmeldebildschirm ausgeführt wird. (#8574)
* Es ist nun möglich die Protokollierungsfunktionen von NVDA komplett auszuschalten, indem Sie im Bereich Allgemeine Einstellungen die Protokollierungsstufe auf "deaktiviert" setzen. (#8516)
* Formeln in LibreOffice und Apache OpenOffice Tabellenkalkulationen werden nun gemeldet. (#860)
* In Mozilla Firefox und Google Chrome meldet der Lesemodus nun das ausgewählte Element in Listenfeldern und Baumansichten.
 * Dies funktioniert ab Mozilla Firefox 66 und neuer.
 * Dies funktioniert noch nicht für bestimmte Listenfelder (HTML Select Controls) in Google Chrome.
* Basis-Unterstützung von Apps wie Mozilla Firefox auf Computern mit ARM64-Prozessoren (z. B. Qualcomm Snapdragon). (#9216)
* Eine neue Kategorie "Erweiterte Einstellungen" wurde dem NVDA-Einstellungsdialog hinzugefügt, welche u. a. eine Option enthält, um die neue Unterstützung für Microsoft Word durch NVDA über die API-Schnittstelle der UIA von Microsoft testen zu können. (#9200)
* Unterstützung für die grafische Ansicht in der Windows Datenträgerverwaltung wurde hinzugefügt. (#1486)
* Die Braillezeilen HandyTech Connect Braille und Basic Braille 84 werden nun unterstützt. (#9249)

### Änderungen

* Der Braille-Übersetzer LibLouis wurde auf Version 3.8.0 aktualisiert. (#9013)
* Entwickler können nun eine NVDA-Version angeben, die für eine Erweiterung mindestens erforderlich ist. NVDA wird eine Erweiterung nicht laden, wenn die angegebene Minimalversion neuer ist als die aktuell verwendete NVDA-Version. (#6275)
* Autoren von Erweiterungen können nun die letzte NVDA-Version angeben, mit der die Erweiterung getestet wurde. Wenn eine Erweiterung nur mit einer NVDA-Version getestet wurde, die niedriger ist als die aktuelle Version, wird NVDA die Installation oder das Laden der entsprechenden Erweiterungen ablehnen. (#6275)
* Diese NVDA-Version ermöglicht die Installation und das Laden von Erweiterungen, die noch keine Informationen zur minimalen und letzten getesteten NVDA-Version enthalten, aber ein Upgrade auf zukünftige NVDA-Versionen (z. B. 2019.2) kann automatisch dazu führen, dass diese älteren Erweiterungen deaktiviert werden.
* Der Befehl zum Bewegen der Maus zum Navigator-Objekt (NVDA-Cursor) funktioniert nun sowohl in Microsoft Word als auch für UIA-Steuerungen, insbesondere in Microsoft Edge. (#7916, #8371)
* Das Melden des Textes unter dem Maus-Cursor wurde in Microsoft Edge und anderen UIA-Anwendungen verbessert. (#8370)
* Wenn NVDA mit dem Befehlszeilenparameter "--portable-path" gestartet wird, wird der angegebene Pfad beim Erstellen einer portablen Version aus dem Menü automatisch ausgefüllt. (#8623)
* Der Pfad zur norwegischen Braille-Table wurde geändert, um dem Standard aus dem Jahr 2015 zu entsprechen. (#9170)
* Bei der Navigation nach Absatz (Strg+Pfeiltasten) oder nach Tabellenzelle (Strg+Alt+Pfeiltasten) werden Rechtschreibfehler nicht mehr gemeldet, auch wenn dies in den Einstellungen aktiviert ist. Absätze und Tabellenzellen können recht groß sein und große Textmengen enthalten. Die Berechnung von Rechtschreibfehlern in einigen Anwendungen kann sehr kostspielig sein und die Performance stark beeinträchtigen. (#9217)
* NVDA lädt nicht mehr automatisch benutzerdefinierte Anwendungsmodulle, globalPlugins sowie Braille- und Sprachausgabentreiber aus dem NVDA-Benutzer-Konfigurationsverzeichnis. Dieser Code sollte stattdessen als Erweiterung mit korrekten Versionsinformationen verpackt werden, um sicherzustellen, dass inkompatibler Code nicht mit aktuellen NVDA-Versionen ausgeführt wird. (#9238)
 * Für Entwickler, die Code während der Entwicklung testen müssen, aktivieren Sie das Developer Scratchpad-Verzeichnis von NVDA in der Kategorie Erweiterte Einstellungen in den NVDA-Einstellungen und legen Sie Ihren Code in das Verzeichnis 'scratchpad' im NVDA-Benutzerkonfigurationsverzeichnis ab, nachdem diese Option aktiviert wurde.

### Fehlerbehebungen

* Bei der Verwendung des OneCore-Sprachsynthesizers unter Windows 10 April 2018 Update und später werden keine langen Pausen mehr zwischen den Sprachäußerungen eingefügt. (#8985)
* Wenn Sie sich in Klartext-Steuerelementen bewegen (z. B. Notepad) oder im Lesemodus navigieren, werden 32-Bit-Emoji-Zeichen, die aus zwei UTF-16-Codepunkten bestehen (z. B. 🤦) nun korrekt gelesen. (#8782)
* Der Bestätigungsdialog für den Neustart nach dem Ändern der Oberflächensprache von NVDA wurde verbessert. Der Text und die Beschriftungen der Schaltflächen sind nun prägnanter und weniger verwirrend. (#6416)
* Wenn ein Sprachsynthesizer von Drittanbietern nicht geladen werden kann, greift NVDA unter Windows 10 auf den Windows OneCore-Sprachsynthesizer zurück, anstatt eSpeak. (#9025)
* Der Eintrag für den Willkommensdialog im NVDA-Menü wird in geschützten Bildschirmen nicht mehr angezeigt. (#8520)
* Beim Tabben oder bei der Schnellnavigation im Lesemodus werden Legenden der Registerkarten nun einheitlicher dargestellt. (#709)
* NVDA wird nun Auswahländerungen für bestimmte Zeitpicker bekannt geben, z. B. in der App Wecker- und Uhren unter Windows 10. (#5231)
* Im Aktionscenter von Windows 10 sagt NVDA Statusmeldungen an, wenn Sie zwischen schnellen Aktionen wie Helligkeit und Fokusunterstützung umschalten. (#8954)
* Im Aktionscenter in Windows 10 Oktober 2018 Update und früher erkennt NVDA das Steuerelement für die Helligkeit als Schaltfläche anstelle einer Umschalttaste. (#8845)
* NVDA verfolgt nun den Cursor wieder und meldet wieder gelöschte Zeichen in den Dialogfeldern "Suchen, "Gehe zu" und anderen Dialogfeldern in Microsoft Excel. (#9042)
* Ein seltener Absturz im Lesemodus in Firefox wurde behoben. (#9152)
* NVDA meldet nun wieder den Fokus für einige Steuerelemente im Menüband von Microsoft Office 2016, wenn das Menüband reduziert wird.
* NVDA meldet den vorgeschlagenen Kontakt wieder automatisch, wenn Adressen in neuen Nachrichten in Outlook 2016 eingegeben werden. (#8502)
* Die letzten paar Cursor-Routing-Tasten auf der 80er Eurobraille-Braillezeile verschieben den Cursor nicht mehr zum Anfang oder kurz nach dem Beginn der Zeile auf dem Brailledisplay. (#9160)
* Die Tabellennavigation in der Thread-Ansicht in Mozilla Thunderbird wurde verbessert. (#8396)
* In Mozilla Firefox und Google Chrome funktioniert das Umschalten in den Fokus-Modus jetzt korrekt für bestimmte Ausklapplisten / Kombinationsfelder und Baumansichten, welche selbst nicht fokussierbar sind aber ihre Elemente schon. (#3573, #9157)
* Der Lesemodus ist nun standardmäßig richtigerweise eingeschaltet, wenn Nachrichten in Outlook 2016 / 365 gelesen werden, sofern die experimentelle UIA in NVDA für Word-Dokumente aktiviert ist. (#9188)
* Ein Problem wurde behoben, bei welchem NVDA abstürzte und wo der einzige Ausweg darin bestandt, die komplette Windows-Sitzung ab- und wieder anzumelden. (#6291)
* In Windows 10 Oktober 2018 Update und später, beim Öffnen des Cloud-Clipboard-Verlaufs mit leerer Zwischenablage, wird NVDA den Status der Zwischenablage melden. (#9103)
* In Windows 10 Oktober 2018 Update und später, bei der Suche nach Emojis im Emoji-Panel, wird NVDA die besten Suchergebnisse melden. (#9105)
* NVDA friert im Hauptfenster von Oracle VirtualBox 5.2 und neuer nicht mehr ein. (#9202)
* Die Reaktionsfähigkeit in Microsoft Word bei der Navigation durch Zeilen, Absätze oder Tabellenzellen konnte deutlich verbessert werden. Zur Erinnerung: Um die beste Leistung zu erzielen, stellen Sie Microsoft Word nach dem Öffnen eines Dokuments mit Alt+W auf Entwurfsansicht ein. (#9217)
* In Mozilla Firefox und Google Chrome werden leere Warnungen nicht mehr gemeldet. (#5657)
* Deutliche Leistungsverbesserungen bei der Navigation durch Zellen in Microsoft Excel, insbesondere wenn die Kalkulationstabelle Kommentare und / oder Ausklapplisten zur Validierung enthält. (#7348)
* Die Bearbeitung in Zellen in MS Excel 2016/365 funktioniert nun wieder. Das "Editieren in Zelle" in den Optionen von Microsoft Excel kann wieder aktiviert werden, um in Excel 2016 / 365 auf die Steuerung der Zellenbearbeitung mit NVDA zuzugreifen. (#8146).
* Ein Absturz in Mozilla Firefox wurde behoben, der manchmal beim schnellen Navigieren nach Artikeln auftrat, wenn die Erweiterung erweitertes Aria verwendet wurde. (#8980)

### Änderungen für Entwickler

* NVDA kann nun mit allen Editionen von Microsoft Visual Studio 2017 (nicht nur mit der Community-Version) kompiliert werden. (#8939)
* Sie können nun Protokollausgaben von LibLouis in das NVDA-Protokoll aufnehmen, indem Sie das boolesche Flag "louis" im Abschnitt "debug" in den erweiterten Einstellungen von NVDA aktivieren. (#4554)
* Autoren von Erweiterungen können nun Informationen zur Kompatibilität mit NVDA-Versionen im Manifest der Erweiterungen bereitstellen. (#6275, #9055)
 * minimumNVDAVersion: Die minimale erforderliche NVDA-Version, damit eine Erweiterung ordnungsgemäß funktioniert.
 * lastTestedNVDAVersion: Die zuletzt getestete NVDA-Version, mit der die Erweiterung getestet wurde.
* Die Objekte "OffsetsTextInfo" können nun die Methode _getBoundingRectFromOffset implementieren, um das Abrufen von begrenzten Rechtecken pro Zeichen anstelle von Punkten zu ermöglichen. (#8572)
* Den TextInfo-Objekten wurde eine Eigenschaft boundingRect hinzugefügt, um das umschließende Rechteck eines Textbereichs abzurufen. (#8371)
* Eigenschaften und Methoden innerhalb von Klassen können nun in NVDA als abstrakt gekennzeichnet werden. Diese Klassen lösen einen Fehler aus, wenn sie instanziiert werden. (#8294, #8652, #8658)
* NVDA kann die Zeit seit der Eingabe protokollieren, wenn Text gesprochen wird, was bei der Messung der wahrgenommenen Reaktionsfähigkeit hilft. Dies kann durch Aktivieren der Einstellung "timeSinceInput" im Abschnitt "Debugprotokollierung" in den erweiterten Einstellungen von NVDA aktiviert werden. (#9167)

## 2018.4.1

Diese Version behebt einen Absturz beim Start, wenn die Sprache der Benutzeroberfläche von NVDA auf Aragonesisch eingestellt ist. (#9089)

## 2018.4

Zu den Highlights dieser Version gehören Leistungsverbesserungen in den neuesten Versionen von Mozilla Firefox, die Ankündigung von Emojis mit allen Sprachausgaben, die Meldung des Status Beantwortet/Weitergeleitet in Microsoft Outlook, die Meldung der Entfernung des Cursors zum Rand einer Seite im Microsoft Word-Dokument und viele Fehlerbehebungen.

### Neue Features

* Neue Braille-Tabellen: Chinesische Voll- und Kurzschrift (Mandarin). (#5553)
* In der Nachrichtenansicht in Microsoft Outlook meldet NVDA nun den Status "Beantwortet" und "Weitergeleitet" für jede Nachricht. (#6911)
* NVDA kann jetzt Beschreibungen für Emoji und andere Zeichen vorlesen, welche Teil der gemeinsamen Unicode-Gebietsschemata sind. (#6523)
* In Microsoft Word kann NVDA jetzt den Abstand des Cursors vom oberen und vom linken Rand der aktuellen Seite melden. Drücken Sie dafür NVDA+Entfernen. (#1939)
* NVDA sagt nicht mehr "Ausgewählt" bei jeder Zelle während der Navigation mit den Pfeiltasten zwischen Zellen in Google Sheets, wenn Braille-Modus aktiviert wurde. (#8879)
* Unterstützung für Foxit Reader und Foxit Phantom PDF hinzugefügt. (#8944)
* Unterstützung für das DBeaver-Datenbankwerkzeug. (#8905)

### Änderungen

* Der Menüeintrag "Hilfesprechblasen ausgeben" im Dialogfeld Objektpräsentationen wurde in "Benachrichtigungen mitteilen" umbenannt, um die Meldung von Benachrichtigungen in Windows 8 und neuer aufzunehmen. (#5789)
* In den Tastatur-Einstellungen von NVDA werden die Kontrollkästchen zum Aktivieren oder Deaktivieren der NVDA-Taste nun in einer Liste und nicht mehr als separate Kontrollkästchen angezeigt.
* NVDA zeigt unter einigen Windows-Versionen keine doppelten Informationen mehr an, wenn die Uhr in der Taskleiste vorgelesen wird. (#4364)
* Der Braille-Übersetzer LibLouis wurde auf Version 3.7.0 aktualisiert. (#8697)
* Die Sprachausgabe eSpeak-NG wurde auf Commit 919f3240cbb aktualisiert
* NVDA meldet nicht mehr mehrfach hintereinander "Anklickbar", wenn Sie im Lesemodus durch klickbare Inhalte navigieren. (#7430)
* Die Tastenbefehle, die auf Baum Vario 40 Braillezeilen ausgeführt werden, funktionieren nun korrekt. (#8894)
* NVDA meldet nicht mehr "Text ausgewählt" bei jedem fokussierten Objekt in Google-Präsentationen mit Mozilla Firefox. (#8964)

### Fehlerbehebungen

* In Microsoft Outlook 2016/365 werden der Kategorie- und Kennzeichenstatus für Nachrichten gemeldet. (#8603)
* Wenn NVDA auf Sprachen wie Kirgyz, Mongolisch oder Mazedonisch eingestellt ist, wird beim Start kein Dialogfeld mehr angezeigt, das davor warnt, dass die Sprache vom Betriebssystem nicht unterstützt wird. (#8064)
* Wenn Sie die Maus mit Hilfe der Tastatur auf das Navigatorobjekt bewegen, wird die Maus nun viel genauer auf die Position im Fokus- und Lesemodus in Mozilla Firefox, Google Chrome und Acrobat Reader DC bewegt. (#6460)
* Der Umgang mit Kombinationsfeldern im Web in Firefox, Chrome und Internet Explorer wurde verbessert. (#8664)
* Die Warnmeldung über die erforderliche Windows-Version wird nunauch auf Windows XP und Vista mit japanischer Anzeigesprache richtig angezeigt. (#8771)
* Verbesserung der Leistung in Mozilla Firefox auf komplexen Webseiten mit verschiedenen dynamischen Inhalten. (#8678)
* Format-Atribute (Überschrift, Link etc.) werden in Braille nicht mehr angezeigt, wenn die entsprechenden Einträge in den Einstellungen für Dokument-Formatierung deaktiviert wurden. (#7615)
* Im Windows-Explorer und anderen Anwendungen bei Verwendung von UIA wird der Fokus zuverlässig von NVDA verfolgt, wenn eine andere Anwendung lädt (z. B. während der Batch-Ausführung bei der Audio-bearbeitung). (#7345)
* In ARIA-Menüs im Web wird die Escape-Taste nun an das menü weitergereicht, sodass das Fokus-Modus nicht mehr unterbrochen wird. (#3215)
* Während der Navigation mit den Schnellnavigationstasten in Nachrichten im neuen Gmail, liest NVDA nun nicht mehr den ganzen Text der Nachricht vor, sobald man ein entsprechendes Element fokusiert. (#8887)
* Browser wie Mozilla Firefox und Google Chrome dürften nicht mehr abstürzen, nachdem NVDA aktualisiert wurde. Das Lesemodus müsste nun weiterhin Aktualisierungen in aktuell geladenen Dokumenten richtig reflektieren. (#7641)

### Änderungen für Entwickler

* Die Funktion "gui.nvdaControls" beinhaltet nun zwei Klassen zum Erstellen zugänglicher Listen mit Kontrollkästchen. (#7325)
 * "CustomCheckListBox" ist eine zugängliche Unterklasse von "wx.CheckListBox".
 * "AutoWidthColumnCheckListCtrl" fügt zugängliche Kontrollkästchen zu einem "AutoWidthColumnListCtrl" hinzu, welches wiederum auf "wx.ListCtrl" basiert.
* Wenn ein wx-Widget noch nicht zugänglich ist, können Sie dies über eine Instanz von "gui.accPropServer.IAccPropServer_impl" erledigen. (#7491)
 * Schauen Sie für weitere Informationen in den Implementierung von "gui.nvdaControls.ListCtrlAccPropServer" nach.
* Paket "configobj" auf 5.1.0dev Commit 5b5de48a aktualisiert. (#4470)
* Die config.post_configProfileSwitch Aktion akzeptiert nun auch das optionale prevConf Schlagwort-Argument. Dies erlaubt handlern vorzugreifen basierend auf Unterschiede zwischen Konfigurationen vor und nach dem Wechsel des Konfigurationsprofils. (#8758)

## 2018.3.2

In dieser Version wurde ein Fehler behoben, der einen Absturz in Google Chrome bei der Navigation durch Tweets auf [www.twitter.com](http://www.twitter.com) zur Folge hatte. (#8777)

## 2018.3.1

Dies ist ein kleineres Update, in dem ein kritischer Fehler in NVDA behoben wurde, der zum Absturz von 32-Bit-Versionen von Mozilla Firefox führte. (#8759)

## 2018.3

Zu den Highlights dieser Version gehören die automatische Erkennung vieler Braillezeilen, die Unterstützung neuer Windows 10-Funktionen, einschließlich des Windows 10 Emoji-Eingabebereichs und viele andere Fehlerbehebungen.

### Neue Features

* NVDA meldet Grammatikfehler, wenn sie von Webseiten in Mozilla Firefox und Google Chrome angemessen dargestellt werden. (#8280)
* Inhalte, die in Webseiten als eingefügt oder gelöscht gekennzeichnet sind, werden nun in Google Chrome angezeigt. (#8558)
* Unterstützung für BrailleNote QT und das Scrollrad von Apex BT wurde hinzugefügt, wenn BrailleNote als Braillezeile mit NVDA verwendet wird. (#5992, #5993)
* Es wurden Skripte für die Anzeige der abgelaufenen und der Gesamtzeit des aktuellen Tracks in Foobar2000 hinzugefügt. (#6596)
* Das Mac-Befehlstastensymbol (⌘) wird nun beim Lesen von Text mit einem beliebigen Synthesizer angezeigt. (#8366)
* Benutzerdefinierte Regeln über das Attribut "aria-roledescription" werden nun in allen Web-Browsern unterstützt. (#8448)
* Neue Braille-Tabellen: Tschechisches 8-Punkt-Computerbraille, Zentralkurdisch, Spanisch (Esperanto), Ungarisch, Schwedisches 8-Punkt-Computerbraille. (#8226, #8437)
* Unterstützung wurde hinzugefügt, um Braillezeilen im Hintergrund automatisch zu erkennen. (#1271)
 * Braillezeilen ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, HandyTech, Hims, SuperBraille und HumanWare BrailleNote und Brailliant BI/B werden derzeit unterstützt.
 * Sie können diese Funktion aktivieren, indem Sie die automatische Option aus der Liste der Braillezeilen im Braillezeilen-Auswahldialog von NVDA auswählen.
 * Weitere Informationen entnehmen Sie bitte der Dokumentation.
* Unterstützung für verschiedene moderne Eingabefunktionen, die in den letzten Versionen von Windows 10 eingeführt wurden, wurden hinzugefügt. Dazu gehören Emoji-Panel (Fall Creators Update), Diktat (Fall Creators Update), Hardware-Tastatur-Eingabevorschläge (April 2018 Update) und Einfügen aus der Cloud-Zwischenablage (Oktober 2018 Update). (#7273)
* Inhalte, die mit ARIA (role blockquote) als Blockzitat gekennzeichnet sind, werden nun in Mozilla Firefox 63 unterstützt. (#8577)

### Änderungen

* Die Liste der verfügbaren Sprachen im Dialogfeld "Allgemeine Einstellungen" werden nun nach Sprachnamen statt nach ISO-639 sortiert. (#7284)
* Die Tastenkombinationen Alt+Umschalt+Tab und Windows+Tab können mit allen Braillezeilen von Freedom Scientific emuliert werden. (#7387)
* Für ALVA BC680 und Protokollkonverter-Brailezeilen ist es nun möglich, der linken und rechten Smart Pad-, Daumen- und Etouch-Taste unterschiedliche Funktionen zuzuweisen. (#8230)
* Bei ALVA BC6 Braillezeilen werden nun mit der Tastenkombination sp2+sp3 das aktuelle Datum und die Uhrzeit angezeigt, während sp1+sp2 die Windows-Taste emuliert. (#8230)
* Der Benutzer wird einmalig beim Start von NVDA gefragt, ob bei der Überprüfung auf NVDA-Aktualisierungen Nutzungsstatistiken an NV Access gesendet werden sollen. (#8217)
* Der Braille-Übersetzer LibLouis wurde auf Version 3.6.0 aktualisiert. (#8365)
* Der Pfad zur korrekten russischen 8-Punkt-Braille-Tabelle wurde aktualisiert. (#8446)
* Die Sprachausgabe eSpeak-NG wurde auf 1.49.3dev Commit 910f4c2 aktualisiert. (#8561)
* Wenn der Benutzer zugestimmt hat, Nutzungsstatistiken an NV Access zu senden, sendet NVDA nun den Namen des aktuell verwendeten Sprachausgaben-Treibers und der Braillezeile, um eine bessere Priorisierung für zukünftige Arbeiten an diesen Treibern zu ermöglichen. (#8217)

### Fehlerbehebungen

* Zugängliche Beschriftungen für Steuerelemente in Google Chrome werden nun leichter im Lesenmodus angezeigt, wenn die Beschriftung selbst nicht als Inhalt angezeigt wird. (#4773)
* Benachrichtigungen werden jetzt in Zoom unterstützt. Dazu gehören zum Beispiel der Status Stummschaltung ein/aus und eingehende Nachrichten. (#7754)
* Das Umschalten der Braille-Kontextdarstellung im Lesemodus führt nicht mehr dazu, dass die Braille-Ausgabe nach dem Cursor im Lesemodus stehen bleibt. (#7741)
* ALVA BC680 Braillezeilen schlagen nicht mehr beim Initialisieren fehl. (#8106)
* Standardmäßig führen ALVA BC6 Braillezeilen keine emulierten Systemtastaturtasten mehr aus, wenn Tastenkombinationen mit Sp2+Sp3 gedrückt werden, um interne Funktionen auszulösen. (#8230)
* Das Drücken von Sp2 auf einer ALVA BC6 Braillezeile, um die Alt-Taste zu emulieren, funktioniert jetzt wie angekündigt. (#8360)
* NVDA kündigt keine redundanten Änderungen am Tastaturlayout mehr an. (#7383, #8419)
* Die Mausverfolgung ist jetzt viel genauer in Notepad und anderen Editoren, wenn es sich um ein Dokument mit mehr als 65.535 Zeichen handelt. (#8397)
* NVDA erkennt mehr Dialoge in Windows 10 und anderen modernen Anwendungen. (#8405)
* Unter Windows 10 Oktober 2018 Update und Server 2019 und neuer kann NVDA den System-Fokus nicht mehr verfolgen, wenn eine Anwendung das System einfriert oder mit Ereignissen überschwemmt. (#7345, #8535)
* Anwender werden nun informiert, wenn sie versuchen, eine leere Statusleiste zu lesen oder zu kopieren. (#7789)
* Es wurde ein Problem behoben, in dem der Zustand eines Kontrollfelds "nicht angehakt" nicht in der Sprachausgabe gemeldet wurden, wenn die Kontrollfelder zuvor halb angehakt wurde. (#6946)
* In der Liste der Sprachen in den Allgemeinen Einstellungen von NVDA wird der Sprachname für Burmesisch unter Windows 7 korrekt angezeigt. (#8544)
* In Microsoft Edge meldet NVDA Benachrichtigungen wie die Verfügbarkeit der Leseansicht und den Fortschritt des Seitenladens. (#8423)
* Beim Navigieren in eine Liste im Web meldet NVDA nun dessen Beschriftung, wenn der Web-Autor eines angegeben hat. (#7652)
* Bei der manuellen Zuordnung von Funktionen zu Gesten für eine bestimmte Braillezeile erscheinen diese Gesten nun immer als dieser Anzeige zugeordnet. Zuvor tauchten sie auf, als wären sie der gerade aktiven Anzeige zugeordnet. (#8108)
* Die 64-Bit-Version von Media Player Classic wird nun unterstützt. (#6066)
* Verschiedene Verbesserungen der Braille-Unterstützung in Microsoft Word mit aktivierter UIA:
 * Wenn sie an den Anfang des Dokuments springen, wird - ähnlich wie in anderen mehrzeiligen Eingabefeldern auch - die Anzeige auf der Braillezeile linksbündig ausgerichtet. (#8406)
 * Bei der Fokussierung eines Word-Dokuments wurde die Fokussierung für die Sprachausgabe und auf der braillezeile reduziert. (#8407)
 * Das Cursor-Routing auf der Braillezeile funktioniert nun auch in einer Liste in einem Word-Dokument korrekt. (#7971)
 * Neu eingefügte Aufzählungen / Zahlen in einem Word-Dokument werden von der Sprachausgabe und auf der Braillezeile korrekt dargestellt. (#7970)
* Ab Windows 10 1803 ist es nun möglich, Erweiterungen zu installieren, wenn die Funktion "Unicode UTF-8 für weltweite Sprachunterstützung verwenden" aktiviert ist. (#8599)
* iTunes 12.9 ist mit NVDA wieder bedienbar. (#8744)

### Änderungen für Entwickler

* scriptHandler.script hinzugefügt; kann als decorator für Scripts verwendet werden. (#6266)
* Für NVDA wurde ein Systemtest-Framework eingeführt. (#708)
* Im Modul "hwPortUtils" wurden einige Änderungen vorgenommen: (#1271)
 * Das Skript "listUsbDevices" liefert nun Wörterbücher mit Geräte-Informationen wie Hardware-ID und Geräte-Pfad.
 * Wörterbücher von "listComPorts" enthalten nun auch einen uSB-ID-Eintrag für COM-Ports mit USB-VID/PID-Informationen in dessen Hardware-ID.
* wxPython wurde aktualisiert auf 4.0.3. (#7077)
* Da NVDA jetzt nur noch Windows 7 SP1 und neuer unterstützt, wurde der Schlüssel "minWindowsVersion" entfernt, mit dem geprüft wird, ob UIA für eine bestimmte Windows-Version aktiviert werden sollte. (#8422)
* Sie können sich nun über die neuen Aktionen "config.pre_configSave", "config.post_configSave", "config.pre_configReset" und "config.post_configReset" informieren lassen. (#7598)
 * Das Skript "config.pre_configSave" wird verwendet, um benachrichtigt zu werden, wenn die Konfiguration von NVDA gespeichert werden soll und "config.post_configSave" wird nach dem Speichern der Konfiguration aufgerufen.
 * Die Skripte "config.pre_configReset" und "config.post_configReset" enthalten ein Flag (für die Standard-Einstellung), um festzulegen, ob die Einstellungen von der Festplatte zurückgeladen werden (false) oder auf die Standard-Einstellungen zurückgesetzt werden soll (true).
* Das Skript "config.configProfileSwitch" wurde in "config.post_configProfileSwitch" umbenannt, um der Tatsache Rechnung zu tragen, dass diese Aktion nach dem Profilwechsel aufgerufen wird. (#7598)a
* UIA-Schnittstellen wurden aktualisiert auf Windows 10, Oktober 2018 Update und Server 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)

## 2018.2.1

Diese Version enthält Übersetzungsaktualisierungen, da eine Funktion, die Probleme verursacht hat, in letzter Minute entfernt wurde.

## 2018.2

Zu den Highlights dieser Version gehören die Unterstützung von Tabellen in Kindle für PC, Unterstützung für BrailleNote Touch- und BI14 Braillezeilen von Humanware, Verbesserungen für Onecore- und Sapi5-Sprachausgaben, Verbesserungen in Microsoft Outlook und vieles mehr.

### Neue Features

* Zeilen- und Spaltenausdehnungen bei verbundenen Zellen werden nun per Sprache und Braille deutlich ausgegeben. (#2642)
* Die Tabellennavigationsbefehle funktionieren jetzt auch in Google Docs-Dokumenten mit aktiviertem Braille-Modus. (#7946)
* Unterstützung für Tabellen in Amazons Kindle für PC (#7977)
* Unterstützung für die Braillezeilenmodelle BrailleNote touch und Brailliant BI 14 via USB und Bluetooth. (#6524)
* In Windows 10 Fall Creators Update und neuer kann NVDA nun Benachrichtigungen von Apps wie etwa dem Rechner oder dem Windows-Store ausgeben. (#8045)
* Neue Braille-Übersetzungstabellen: litauisch 8-Punkt, rumänisch 8 Punkt, Ukrainisch, Mongolische Kurzschrift. (#7839)
* Es wurde ein Skript hinzugefügt, das die Ausgabe von Formatierungsinformationen des Textes unter einem bestimmten Braille-Modul erlaubt. (#7106)
* Bei der Aktualisierung von NVDA auf eine neue Version ist es nun möglich, die Instalation der Aktualisierung auf einen späteren Zeitpunkt zu verschieben. (#4263)
* Neue Sprachen: mongolisch, schweizer-deutsch.
* Sie können nun Tasten(Kombinationen) an Ihrer Braillezeile verwenden, um Umschalttasten wie alt, Strg oder Umschalt mit anderen Tasten zu kombinieren. (#7306)
 * Verwenden Sie hierzu die neu hinzugekommenen Einträge im Dialogfeld "Einstellungen" -> "Tastenbefehle" in der Kategorie "Emulierte Tasten".
* Unterstützung der Braillezeilen von HandyTech wie Braillino und Modular mit älterer Firmware wiederhergestellt. (#8016)
* Datum und Uhrzeit für unterstützte Braillezeilen von HandyTech (wie Active Braille und Active Star) werden nun automatisch von NVDA synchronisiert, wenn sie länger als fünf Sekunden nicht synchronisiert sind. (#8016)
* Es kann nun ein neuer Befehl im Dialogfeld "Tastenbefehle" zugewiesen werden, um temporär alle Profil-Trigger zu deaktivieren. (#4935)

### Änderungen

* Die Spalte Status im Dialogfeld Erweiterungen verwalten zeigt den Status als "aktiviert" oder "deaktiviert" an; nicht mehr als "wird ausgeführt" oder "stillgelegt". (#7929)
* Der Braille-Übersetzer Liblouis wurde auf Version 3.5.0 aktualisiert. (#7839)
* Die litauische Braille-Übersetzungstabelle wurde auf Litauisch 6-Punkt umbenannt, um Verwechslungen mit der neuen 8-Punkt-Tabelle zu vermeiden. (#7839)
* Die kanadisch-französischen Braille-Tabellen für Kurz- und Vollschrift wurden entfernt, stattdessen werden die vereinheitlichten 6-Punkt-Computerbraille und Kurzschrift-Tabellen verwendet. (#7839)
* Die sekundären Routing-Tasten auf Alva BC6-, EuroBraille- und Papenmeier-Braillezeilen zeigen nun Formatierungsinformationen für den Text unter dem Braille-Modul dieser Taste an. (#7106)
* Beim Eingeben von Kurzschrift fällt NVDA automatisch auf eine Basisschrift-Eingabetabelle zurück, wenn sich der Fokus z. B. im Lesemodus auf einem Steuerelement befindet, das keine Einfügemarke besitzt. (#7306)
* NVDA zeigt in Outlook weniger ausführliche Informationen an, wenn eine Besprechung oder ein Termin angezeigt wird, der/die einen ganzen Tag umfasst. (#7949)
* Alle Einstellungen von NVDA werden nun in einem einzigen Dialogfeld unter Optionen -> Einstellungen angezeigt. (#7302)
* Unter Windows 10 wurde die Standardsprachausgabe auf Windows-OneCore geändert. (#8176)

### Fehlerbehebungen

* Das Auslesen des Anmeldebildschirms für das Microsoft-Konto funktioniert nun ordnungsgemäß, nachdem Sie eine E-Mail-Adresse eingegeben haben. (#7997)
* Das Auslesen von Webseiten in Microsoft Edge funktioniert nun auch dann noch, wenn Sie eine Seite zurückgesprungen sind. (#7997)
* NVDA gibt nun nicht mehr die letzte Ziffer der Pin beim Entsperren des Rechners im Klartext aus. (#7908)
* Beim Navigieren durch Webseiten mit Tab oder mit den Schnellnavigationsbefehlen werden Beschriftungen für Auswahlschalter oder Kontrollkästchen nicht mehr doppelt ausgegeben. (#7960)
* Das Attribut "aria-current" wird auch dann korrekt ausgewertet, wenn es auf "false" gesetzt ist. (#7892).
* Das Laden des Treibers für die Windows OneCore-Sprachausgabe schlägt nicht mehr fehl, wenn die eingestellte Stimme deinstalliert wurde. (#7999)
* Das Ändern der Stimmen im Treiber von Windows OneCore ist jetzt viel schneller. (#7999)
* Behebung fehlerhafter Braille-Ausgabe für mehrere Braille-Tabellen, einschließlich Großbuchstaben in Dänischer 8-Punkt-Kurzschrift. (#7526, #7693)
* NVDA erkennt nun mehr Aufzählungsarten in Microsoft Word. (#6778)
* Bei der Ausgabe der Formatierungsinformationen wird der Cursor nicht mehr fälschlicherweise verschoben, d. h., wenn Sie sie mehrmals abrufen, führt dies nicht mehr zu verschiedenen Ergebnissen. (#7869)
* Braille-Eingabe in Kurzschrift ist nur noch dort möglich, wo sie auch tatsächlich unterstützt wird (z. B. in Eingabefeldern). (#7306)
* Braillezeilenspezifische Tastenkombinationen für handytech-Zeilen wurden korrigiert. (#8016)
* NVDA zeigt nicht mehr "Unbekannt" an, wenn Sie in Windows 8 oder neuer mit Windows-Taste+X das "Kleine Startmenü" aufrufen. (#8137)
* Modellspezifische Tastenkombinationen auf Hims-Braillezeilen funktionieren nun wie im handbuch dokumentiert. (#8096)
* Probleme mit fehlerhaft registrierten COM-Objekten für Firefox und internet Explorer wurden gelöst. (#2807)
* Probleme mit der Anzeige mancher Details im Taskmanager wurden gelöst. (#8147)
* Neuere SAPI5-Stimmen sollten jetzt schneller reagieren. (#8174)
* NVDA meldet nicht mehr (LTR- und RTL) Marken in Braille oder bei "zeichenweises Lesen", wenn in neueren Windows-Versionen auf die Uhr zugegriffen wird. (#5729)
* Die Erkennung von Scroll-Tasten auf den Hims Smart Beetle Braillezeilen ist jetzt zuverlässiger. (#6086)
* In einigen Textsteuerelementen, insbesondere in Delphi-Anwendungen, sind die Informationen zum Bearbeiten und Navigieren jetzt viel zuverlässiger. (#636, #8102)
* Unter Windows 10 (Redstone 5) meldet NVDA keine zusätzlichen redundanten Informationen mehr, wenn mit Alt + Tab zwischen ausgeführten Programmen gewechselt wird. (#8258)

### Änderungen für Entwickler

* Die Entwickler-Informationen für UIA-Objekte enthält nun eine Liste aller unterstützten Muster. (#5712)
* Sie können nun die Verwendung von UIA innerhalb Ihres Anwendungsmoduls erzwingen, indem Sie die Methode isGoodUIAWindow implementieren. (#7961)
* Die boolesche Einstellung "outputPass1Only" im Abschnitt Braille in der Konfiguration wurde wieder entfernt, da LibLouis diese Funktion nicht mehr unterstützt. (#7839)

## 2018.1.1

Dies ist eine spezielle NVDA-Version, die einen Fehler im Windows-OneCore-Sprachausgabentreiber behebt. Zuvor sprach NVDA unter Windows 10 Redstone 4 (1803) mit höherer Stimme und höherer Geschwindigkeit. (#8082)

## 2018.1

Zu den Highlights dieser Version gehören die Unterstützung für Diagramme in Microsoft Word und Microsoft PowerPoint, neu unterstützte Braillezeilen einschließlich Eurobraille und dem Optelec Protokollkonverter, verbesserte Unterstützung für Hims und Optelec Braillezeilen, Leistungsverbesserungen für Mozilla Firefox 58 und neuer und vieles mehr.

### Neue Features

* In Microsoft Word und Microsoft PowerPoint ist es nun möglich mit Diagrammen zu interagieren, ähnlich der Unterstützung für Diagramme in Microsoft Excel. (#7046)
 * In Microsoft Word: Wenn Sie sich im Lesemodus befinden, stellen Sie sich auf ein eingebettetes Diagramm und drücken Eingabe, um damit zu interagieren.
 * In Microsoft PowerPoint, während Sie eine Folie bearbeiten: Springen Sie mit der Tabulatortaste auf ein diagramm-Objekt und drücken Sie die Eingabe- oder Leertaste, um damit zu interagieren.
 * Das interagieren beenden Sie mit der Escape-Taste.
* neue Sprache: Kirgisisch.
* Unterstützung für VitalSource Bookshelf wurde hinzugefügt. (#7155)
* Unterstützung für den Optelec-Protokollkonverter wurde hinzugefügt. Dies ist ein Gerät, dass die Nutzung von Braille-Voyager- und Satellite-Braillezeielen ermöglicht. Dabei wird das ALVA BC6 Kommunikationsprotocol verwendet. (#6731)
* Die Breilleeingabe über eine ALVA-640-Comfort-Braillezeile wird nun unterstützt. (#7733)
* Die Braille-Eingabe kann auch mit den obigen oder mit anderen BC6-Braillezeilen mit Firmware 3.0.0 oder neuer genutzt werden.
* Erstmalige Unterstützung von Google Tabellen mit aktiviertem Braillemodus. (#7935)
* Die Braillezeilen Esys, Esytime und Iris von Eurobraille werden nun unterstützt. (#7488)

### Änderungen

* Die Treiber für die Zeilen HIMS Braille Sense / Braille EDGE / Smart Beetle und Hims Sync Braille wurden durch einen einzelnen Treiber ersetzt, der automatisch aktiviert wird, sofern Sie eine Syncbraille-zeile verwenden. (#7459)
 * Einige Tasten, insbesondere die Scroll-Tasten, wurden neu zugewiesen, um den von Hims-Produkten verwendeten Konventionen zu entsprechen. Für mehr Details siehe die Bedienungsanleitung.
* Beim Eingeben von Zeichen über die bildschirmtastatur müssen Sie nun jedes zeichen doppelt antippen, so wie Sie jedes andere Steuerelement betätigen. (#7309)
 * Um das vorherige Verhalten zurückzubekommen und Touch typing zu aktivieren, benutzen Sie die neu hinzugekommenen Optionen im Touch interaktion-Einstellungsdialog.
* Es ist nicht mehr nötig, die Braillezeile ausdrücklich an den Fokus oder den NVDA-Cursor zu koppeln. Standardmäßig wird die Braillezeile automatisch gekoppelt. (#2385)
 * Die automatische Kopplung der Braillezeile an den NVDA-Cursor funktioniert nur bei Befehlen, die ausdrücklich den NVDA-Cursor oder den Navigator betreffen (wie z. B. die Befehle zum Betrachten von Text). Scrollen auf der Braillezeile wird keine automatische Kopplung auslösen.

### Fehlerbehebungen

* Sollte der Pfad des Ordners, in dem NVDA installiert ist, nicht-ASCII-Zeichen enthalten, schlägt die Anzeige der Formatierungsinformationen im lesemodus nicht mehr fehl, wenn Sie NVDA+F zweimal drücken. (#7474)
* Der Fokus wird nun korrekt gesetzt, wenn Sie von einer anderen Anwendung zu Spotify zurückkehren. (#7689)
* Wenn unter Windows 10 Fall Creators Update der ordnerschutz im Windows Defender Security Center aktiviert ist, schlägt die Aktualisierung von NVDA nicht mehr fehl. (#7696)
* Die Scroll-Tasten von HIMS Smart Beetle funktionieren nun korrekt. (#6086)
* Eine leichte Leistungsverbesserung bei der Darstellung umfangreichere Inhalte in Mozilla Firefox 58 und neuer. (#7719)
* Beim Lesen von Mails in Microsoft Outlook, die Tabellen enthalten, kommt es nicht mehr zu fehlern. (#6827)
* Braillezeilen-Befehle, die ModifikationsTasten der Computertastatur emulieren, können auch dann kombiniert werden, wenn sie auf ein bestimmtes Braillezeilenmodell beschränkt sind. (#7783)
* Dialoge, die von Erweiterungen wie LastPass oder bitwarden in Firefox erzeugt werden, werden nun korrekt im Lesemodus angezeigt. (#7809)
* Sollten Firefox oder Chrome einfrieren oder abstürzen, ist nVDA jetzt nicht mehr unmittelbar betroffen. (#7818)
* In Twitter-Clients, wie Chicken Nugget, werden beim Lesen von Beiträgen mit 280 Zeichen die letzten 20 Zeichen nicht mehr ignoriert. (#7828)
* Beim Markieren von Text sagt NVDA die Sonderzeichen und Symbole jetzt in der richtigen Sprache an. (#7687)
* In aktuellen Versionen von Microsoft Office können Sie wieder mit den Pfeiltasten in Microsoft Excel-Diagrammen navigieren. (#7046)
* Der Status für aktivierbare Kontrollfelder wird nun in Sprache und braille immer in der richtigen Reihenfolge ausgegeben, sowohl im positiven als auch im negativen Fall. (#7076)
* In Windows-Apps wie Windows Mail sagt nVDA gelöschte zeichen beim Drücken der Rücktaste korrekt an. (#7456)
* Alle Tasten der Hims Braille Sense Polaris Braillezeilen funktionieren nun richtig. (#7865)
* NVDA gibt beim Starten auf Windows 7 keine Fehlermeldung mehr aus, wenn bestimmte Versionen der Visual Studio 2017 Redistributable durch andere Anwendungen installiert wurden. Die Fehlermeldung betraf interne API-LS dll-Dateien. (#7975)

### Änderungen für Entwickler

* Neue versteckte bool'sche Einstellung im Abschnitt Braille in der NVDA-Konfiguration: "outputPass1Only". (#7301, #7693, #7702)
 * Wird diese Einstellung auf False gesetzt, werden auch LibLouis-Regeln verarbeitet, die mehrere Durchläufe erfordern. Standardmäßig ist True voreingestellt.
* Ein neues Wörterbuch (Braille.RENAMED_DRIVERS) wurde hinzugefügt, um einen reibungslosen übergang beim Wechseln von alten Treibern für Benutzer zu ermöglichen. (#7459)
* Python: comtypes wurde auf Version 1.1.3 aktualisiert. (#7831)
* Um mit Braillezeilentreibern richtig umgehen zu können, die Bestätigungsmeldungen senden, wurde braille.brailledisplaydriver überarbeitet. Sehen Sie sich den Handytechtreiber für weitere Informationen an. (#7590, #7721)
* Um zu erkennen, ob NVDA aus dem Windows Store heraus ausgeführt wurde, wurde dem Modul config eine neue Variable ISAPPX hinzugefügt. (#7851)
* Für Dokumentklassen, die den Lesemodus unterstützen und ein Textinfo-Objekt enthalten, wurde eine neue Klasse "documentBase.documentWithTableNavigation" eingeführt, um Standard-Tabellennavigationsbefehle zur Verfügung zu stellen. Weitere Informationen über die Helper-Methoten, die bei der Implementierung berücksichtigt werden müssen, finden Sie in der Entwicklerdokumentation für die Klasse. (#7849)
* Die Scons-Batch-Datei kann nun besser funktionieren wenn auch Python 3 installiert ist. Die Batch-Datei nutzt den Launcher, um python 2.7 32 bit auszuführen. (#7541)
* Die Funktion "hwIo.Hid" erhält einen zusätzlichen exklusiven parameter, welcher standardmäßig auf True gesetzt ist. Wenn der Parameter auf False gesetzt wird, dann können andere Anwendunngen mit einem Gerät kommunizieren, während die Anwendungen von NVDA getriggert werden. (#7859)

## 2017.4

Schwerpunkt dieser Version sind zahlreiche Verbesserungen und Fehlerbehebungen im Lesemodus. Hierzu zählen die standardmäßige Verwendung des Lesemodus in Web-Dialogen, eine verbesserte Anzeige der Beschriftungen von Gruppierungen im Lesemodus, die Unterstützung neuer Windows 10-Technologien wie Windows Defender Application Guard und Windows 10 auf ARM64 sowie die automatische Ausgabe der Ausrichtung (Hoch- oder Querformat) des Bildschirms sowie des Akku-Status.
Bitte beachten Sie, dass diese NVDA-Version unter Windows XP und Windows Vista nicht mehr läuft. Sie benötigen mindestens Windows 7 mit Service pack 1.

### Neue Features

* Im Lesemodus können die Tasten Komma und Umschalt+Komma verwendet werden, um vor oder hinter Sprungmarken zu navigieren. (#5482)
* Im Lesemodus können Sie mit den Schnellnavigationstasten für Eingabefelder und Formularfelder nun auch zu Rich-Text-Eingabefeldern navigieren. (#5534)
* In Web-Browsern enthält die Elementliste nun auch Formularfelder und Schalter. (#588)
* Grundlegende Unterstützung für Windows 10 auf ARM64. (#7508)
* Grundlegende Unterstützung beim Lesen von und Navigieren in mathematischen Inhalten in Kindle-Büchern, welche barrierefreie Mathematik berücksichtigen. (#7536)
* Unterstützung für den Azardi eBook Reader. (#5848)
* Beim Aktualisieren von NVDA-Erweiterungen werden Versionsinformationen angegeben. (#5324)
* Neue Kommandozeilen-Parameter zum Erstellen einer portablen NVDA-Version wurden hinzugefügt. (#6329)
* Microsoft Edge wird unterstützt, wenn es innerhalb von Windows Defender Application Guard ausgeführt wird. Dies gillt ab dem Windows 10 Fall Creators Update. (#7600)
* Wenn NVDA auf einem Laptop oder einem Tablet ausgeführt wird, werden Sie benachrichtigt, wenn Sie ein Netzteil anschließen, abziehen oder wenn sich die Bildschirmausrichtung ändert. (#4574, #4612)
* neue Sprache: Mazedonisch.
* Neue Braille-Übersetzungstabellen: kroatische Vollschrift, vietnamesische Vollschrift. (#7518, #7565)
* Das Braillezeilenmodell Actilino von handyTech wird unterstützt. (#7590)
* die Brailleeingabe auf handytech-Braillezeilen wird unterstützt. (#7590)

### Änderungen

* NVDA benötigt mindestens Windows 7 Service Pack 1 oder Windows Server 2008 R2 Service Pack 1. (#7546)
* In Firefox und Google Chrome wird in Web-Dialogen der Lesemodus verwendet, es sei denn, die Webdialoge befinden sich in Webanwendungen. (#4493)
* Beim Navigieren im Lesemodus mittels Tab oder Schnellnavigationstasten wird das Verlassen von Containern wie Listen und Tabellen nicht mehr ausdrücklich angezeigt. (#2591)
* In Firefox und Google Chrome werden die Namen von Formulargruppen angezeigt, wenn Sie zu einem Formularfeld springen. (#3321)
* Die Schnellnavigationstasten für eingebettete Objekte (O und Umschalt+O) berücksichtigen Audio- und Video-Elemente ebenso wie Web-Anwendungen und Web-Dialoge. (#7239)
* eSpeak-NG wurde auf Version 1.49.2 aktualisiert, Dadurch werden einige Probleme bei der Produktion von neuen Versionen behoben. (#7385, #7583)
* Bei dreimal Drücken der Tastenkombination zum Lesen der statuszeile wird diese in die Zwischenablage kopiert. (#1785)
* Beim Zuweisen von NVDA-Befehlen an Tasten der Braillezeilen von Baum kann die Zuweisung auf ein bestimmtes Braillezeilenmodell beschränkt werden (z. B. Baum Vario Ultra, Baum Pronto). (#7517)
* Die Tastenkombination zum direkten Anspringen des Suchfeldes in der Elementliste wurde von Alt+F in Alt+E geändert. (#7569)
* Im Dialogfeld "Einstellungen" -> "Eingaben" gibt es in der Kategorie Lesemodus einen neuen (noch nicht zugewiesenen) Befehl. Mit diesem Befehl können Sie Layout-Tabellen ein- oder ausblenden. (#7634)
* Der Braille-Übersetzer LibLouis wurde auf Version 3.3.0 aktualisiert. (#7565)
* Die Tastenkombination zum Aktivieren von regulären Ausdrücken als Ersetzungskriterium im Wörterbuchdialog wurde von alt+r auf alt+e geändert. (#6782)
* Die Aussprache-Wörterbücher werden nun versioniert und wurden in den Ordner "speechDicts/voiceDicts.v1" verschoben. (#7592)
* Versionierte Dateien (Benutzerkonfiguration, Aussprache-Wörterbücher) werden nicht gespeichert, wenn NVDA von Launcher aus ausgeführt wird. (#7688)
* Die Braillezeilenmodelle Braillino, Buchwurm und Modular (mit der alten Firmware) werden nicht mehr ohne weiteres unterstützt. Um diese Braillezeilenmodelle zu verwenden, müssen Sie den Handytech-Universaltreiber und die NVDA-Erweiterung installieren. (#7590)

### Fehlerbehebungen

* In Anwendungen, wie Microsoft Word, werden Links nun in Braille angezeigt. (#6780)
* Wenn in Firefox oder Google Chrome viele Registerkarten geöffnet sind, reagiert NVDA nun schneller. (#3138)
* Die Cursor-Routing-Tasten von MDV Lilli-Braillezeilen platzieren den Cursor nicht mehr eine Position hinter die gedrückte Position. (#7469)
* Im Internet Explorer und anderen MSHTML-Dokumenten wird das Attribut Required korrekt unterstützt, sodass NVDA angiebt, dass ein Formularfeld zwingend ausgefüllt werden muss. (#7321)
* Die Anzeige in Braille wird beim Eingeben arabischer Zeichen aktualisiert. (#511).
* In Firefox wird die Beschriftung von Formularelementen auch dann angezeigt, wenn die Beschriftung nicht auf den Formularelementen selbst zu finden ist. (#4773)
* Unter Windows 10 Creators Update funktioniert die NVDA-Unterstützung von Firefox auch dann noch, wenn Sie NVDA neu starten. (#7269)
* Wenn Sie NVDA neu starten, während Firefox im Vordergrund ist, steht der Lesemodus wieder zur Verfügung, auch wenn Sie den Fokus mit alt+tab aus Firefox hinaus und wieder hineinbewegen müssen. (#5758)
* Unterstützung mathematischer Inhalte in Google Chrome auf Systemen, auf denen Firefox nicht installiert ist. (#7308)
* Das Betriebssystem und die Anwendungen sollten nun nach der Installation von NVDA stabiler laufen (verglichen mit vorherigen NVDA-Versionen). (#7563)
* Wenn das Navigator-Objekt beim Aufruf der Inhaltserkennung (z. B. mit NVDA+R) verschwunden sein sollte, zeigt NVDA eine Warnmeldung an. (#7567)
* Das Zurückscrollen bei Freedom Scientific-Braillezeilen mit einer linken Wipptaste funktioniert nun ordnungsgemäß. (#7713)

### Änderungen für Entwickler

* Beim Ausführen von "scons tests" wird geprüft, ob sämtliche übersetzbaren Zeichenketten Kommentare besitzen. Dieser Test kann auch separat ausgeführt werden. Benutzen Sie dafür den Befehl "scons checkPot". (#7492)
* Es gibt jetzt ein neues Modul extensionPoints, das ein generisches Framework zur Verfügung stellt, um die Erweiterbarkeit des Codes an bestimmten Stellen im Code zu ermöglichen. Dies ermöglicht es Interessenten, sich zu registrieren, um bei einem bestimmten Ereignis benachrichtigt zu werden (ExtensionPoints.Action), um eine bestimmte Art von Daten zu ändern (ExtensionPoints.Filter) oder um an der Entscheidung teilzunehmen, ob etwas getan wird (ExtensionPoints.Decider). (#3393)
* Sie können sich jetzt registrieren, um über Konfigurationsprofilwechsel benachrichtigt zu werden, indem Sie die Aktion config.configProfileSwitched aufrufen. (#3393)
* Braille-Gesten, die Umschaltttasten emulieren (z. B. Strg und Alt), können nun ohne explizite Definition mit anderen emulierten Systemtasten kombiniert werden. (#6213)
 * Wenn Sie z. B. eine Taste auf Ihrer Braillezeile an die Alt-Taste gebunden haben und eine andere BraillezeilenTaste an die Taste Pfeil ab, führt das Kombinieren dieser Tasten zur Emulation von alt+Pfeil ab.
* die Klasse BrailleDisplayGesture hat jetzt eine zusätzliche Eigenschaft Namens model. Wenn vorhanden, wird durch Drücken einer Taste ein zusätzlicher, modellspezifischer Gesten-Identifikator erzeugt. Damit kann der Benutzer Gesten binden, die auf ein bestimmtes Braillezeilenmodell beschränkt sind.
 * Sehen Sie sich den Treiber für Baum-Braillezeilen als Beispiel für diese neue Funktionalität an.
* NVDA wird nun mit Visual Studio 2017 und Windows 10 SDK compiliert. (#7568)

## 2017.3

Schwerpunkte dieser Version sind u. a. die eingabe von voll- und Kurzschrift über eine Braillezeile, die Unterstützung von Windows OneCore-Stimmen, die Unterstützung von OCR unter Windows 10 sowie viele Verbesserungen bei der Braille-ausgabe.

### Neue Features

* In den Braille-Einstellungen gibt es eine neue Option, die die dauerhafte Anzeige von Meldungen ermöglicht. (#6669)
* In der Nachrichtenliste von Microsoft Outlook werden markierte Nachrichten als solche angezeigt. (#6374)
* In Microsoft PowerPoint wird beim Bearbeiten einer Folie eine Form genau beschrieben, wenn Sie sie bearbeiten (Beispiele sind z. B. Dreieck, Kreis, Video oder Pfeil). Zuvor wurde eine Form lediglich als "Form" angezeigt. (#7111)
* MathML wird jetzt auch in Google Chrome unterstützt. (#7184)
* NVDA unterstützt jetzt auch die neuen Windows OneCore-Stimmen, die in Windows 10 enthalten sind. Sie können diese Stimmen verwenden, indem Sie Windows OneCore-Stimmen unter Einstellungen --> Sprachausgabe auswählen. (#6159)
* Die Konfigurationsdateien von NVDA können jetzt auch im lokalen Konfigurationsverzeichnis gespeichert werden. Die betreffende Einstellung wird in der Registrierungsdatenbank von Windows vorgenommen. Weitere Informationen dazu finden Sie im Abschnitt "Systemparameter" im Benutzerhandbuch. (#6812)
* In Internet-Browsern werden Platzhalterwerte für Eingabefelder angezeigt, solange sie noch leer sind. NVDA unterstützt jetzt auch das Aria-Attribut "aria-placeholder". (#7004)
* Im Lesemodus von Microsoft Word können Sie nun mit W und Umschalt+W zum nächsten und vorherigen Rechtschreibfehlern navigieren. (#6942)
* Datumsfelder in Dialogfeldern für Microsoft Outlook-Termine werden unterstützt. (#7217)
* In dem "An"- und "CC"-Feld in der Windows 10 Mail-App und im Suchfeld für die Windows-Einstellungen wird der aktuell hervorgehobene Vorschlag angezeigt. (#6241)
* Sobald die Vorschlagsliste für ein Suchfeld in Windows 10 erscheint, wird ein Klang abgespielt. (#6241)
* In Skype für Unternehmen werden Benachrichtigungen, wie ankommende Nachrichten automatisch angezeigt. (#7281)
* In Skype für Unternehmen werden ankommende Chatnachrichten automatisch vorgelesen, während man sich in einer Unterhaltung befindet. (#7286))
* In Microsoft Edge werden Benachrichtigungen (z. B. über abgeschlossene Downloads) automatisch angezeigt. (#7281)
* Sie können nun Kurz-, Voll- und Basisschrift über die Brailletastatur einer Braillezeile eingeben. Für weitere Informationen lesen Sie den Abschnitt über Braille-Eingabe in Benutzerhandbuch. (#2439)
* Mit Hilfe der Brailletabelle Unicode können Sie nun Unicode-Zeichen über die Brailletastatur einer Braillezeile eingeben. (#6449)
* Die in Taiwan gebräuchliche Braillezeile Superbraille wird nun unterstützt. (#7352)
* Neue Braille-Übersetzungstabellen: Dänisches 8-Punkt-Computerbraille, Litauisch, Persisches 8-Punkt-Computerbraille, Persische Vollschrift, Slowenisches 8-Punkt-Computerbraille. (#6188, #6550, #6773, #7367)
* Die Braille-Übersetzungstabelle für Englisches 8-Punkt-Computerbraille (USA) wurde verbessert; dies betrifft Aufzählungszeichen, das Eurosymbol und Akzentbuchstaben. (#6836)
* Sie können die in Windows 10 integrierte Texterkennung verwenden, um unzugängliche Bilder und Anwendungen zu erkennen. (#7361)
 * Die Erkennungssprache kann im neuen Dialogfeld "Windows 10-Texterkennung" eingestellt werden.
 * Um den Inhalt des Navigator-Objektes zu erkennen, drücken Sie NVDA+R.
 * Lesen Sie den Abschnitt über die Inhaltserkennung für weitere Informationen im Benutzerhandbuch.
* Sie können nun einstellen, wann der Kontext für ein fokussiertes Objekt in Braille angezeigt werden soll. Verwenden Sie dafür die Einstellung "Kontext anzeigen" in den Braille-Einstellungen. (#217)
 * Die Einstellungen "Nur bei Änderungen" und "Nur beim Scrollen" bewirken eine bessere Anzeige, weil sich die Position von neu angezeigten Listen- und Menüeinträgen auf der Braillezeile nicht verändert.
 * Lesen Sie den Abschnitt "Fokuskontext anzeigen" im Benutzerhandbuch für weitere Informationen.
* In Firefox und Google Chrome werden komplexe Tabellenblätter unterstützt, von denen nur ein Teil geladen und angezeigt wird (Dies betrifft Elemente mit den Attributen "aria-rowcount", "aria-colcount", "aria-rowindex" und "aria-colindex", die mit ARIA 1.1 eingeführt wurden). (#7410)

### Änderungen

* Mit Hilfe eines neuen, nicht zugewiesenen Befehls kann NVDA schnell neu gestartet werden. Dieser Befehl ist unter der Kategorie "Verschiedenes" zu finden. (#6396)
* Das Tastaturschema kann nun im Willkommensbildschirm von NVDA eingestellt werden. (#6863)
* Viele neue Steuerelementtypen und Statusinformationen werden in Braille abgekürzt. Dies betrifft u. a. Sprungmarken. Lesen Sie die Abschnitte über Abkürzungen für Steuerelementtypen und Statusinformationen im Benutzerhandbuch für eine komplette Liste. (#7188, #3975)
* Die Sprachausgabe eSpeak-NG wurde auf Version 1.49.1 aktualisiert. (#7280).
* Die Liste der Braille-Ein- und -Ausgabetabellen wird nun alphabetisch sortiert. (#6113)
* Der Braille-Übersetzer LibLouis wurde auf 3.2.0 aktualisiert. (#6935)
* Als Standard-Brailletabelle wird nun "Vereinheitlichte Englische Vollschrift" voreingestellt. (#6952)
* Standardmäßig zeigt NVDA nur noch dann den Kontext eines Objektes an, wenn ein neues Objekt den Fokus erhält. (#217)
 * Zuvor wurde der Kontext auch dann angezeigt, wenn er sich nicht geändert hat.
 * Sie können das alte Verhalten erzwingen, indem Sie in den Braille-Einstellungen von NVDA die Option "Kontext anzeigen" auf "immer" umstellen.
* In den Braille-Einstellungen können - je nach Kopplung der Braillezeile - unterschiedliche Cursofformen eingestellt werden. (#7122)
* Das Logo von NVDA wurde geändert. Es zeigt nun die Buchstaben NVDA in weißer Schrift auf rotem Hintergrund. (#7446)

### Fehlerbehebungen

* Bearbeitbare Div-Elemente in Chrome haben nicht mehr ihre Beschriftung als Wert. (#7153)
* Das Drücken von "Ende" im Lesemodus in einem lehren Microsoft Word Dokument führt nicht mehr zu einem Laufzeitfehler. (#7009)
* Der Lesemodus von Microsoft Edge wird auch dann vollständig unterstützt, wenn das angezeigte Dokument die ARIA-Klasse "document" besitzt. (#6998)
* Im Lesemodus können Sie selbst dann mit Umschalt+Ende den Rest der Zeile markieren, wenn sich der Cursor bereits auf dem letzten Zeichen befindet. (#7157)
* Wenn ein Dialogfenster eine Fortschrittsanzeige enthält, wird bei Änderungen an der Fortschrittsanzeige auch der Text des Dialogfensters in Braille aktualisiert. Das bedeutet, dass z. B. das Fortschreiten der Zeit zum Herunterladen beim Aktualisieren von NVDA Sie verfolgen können. (#6862)
* Einige Kombinationsfelder in Windows 10 wie z. B. die Einstellungen für automatische Wiedergabe werden jetzt unterstützt. (#6337).
* Beim Erstellen von Besprechungen und Terminen in Microsoft Outlook werden keine wertlosen Informationen mehr angezeigt. (#7216)
* Signaltöne für Fortschrittsbalken mit scheinbar unbegrenztem Wertebereich (wie der Fortschrittsbalken bei der Prüfung nach Aktualisierungen) werden nur noch wiedergegeben, wenn Sie in den Einstellungen für Objektdarstellungen die Signaltöne für Fortschrittsbalken aktiviert haben. (#6759)
* In Microsoft Excel 2003 und 2007 werden die Zellen wieder angezeigt, wenn Sie in einem Tabellenblatt navigieren. (#7243)
* Der lesemodus in Windows 10 Mail in Windows 10 Creators Update funktioniert nun wieder korrekt. (#7289)
* Auf den meisten Braillezeilen mit einer Brailletastatur bewirkt das Drücken von Punkt 7 ein Löschen des zuletzt eingegebenen zeichens und ein Drücken von Punkt 8 betätigt die Eingabetaste. (#6054)
* Das Bewegen des System-Cursors (mit den Pfeiltasten) wird nun exakter verfolgt. Dies betrifft vor allem Chrome und eingabeaufforderungen. (#6424)
* Das Eingabefeld für die Signatur in Microsoft Outlook 2016 wird nun korrekt erkannt. (#7253)
* In Java-Swing-Anwendungen stürzt NVDA beim Navigieren in Tabellen nicht mehr ab. (#6992)
* In Windows 10 Creators Update werden Benachrichtigungen nicht mehr mehrfach angezeigt. (#7128)
* Wenn das Startmenü von Windows 10 beim Drücken der Eingabetaste geschlossen wird, wird der Suchbegriff nicht mehr angezeigt. (#7370)
* Die Schnellnavigation für Überschriften in Microsoft Edge ist nun schneller. (#7343)
* Beim Verwenden der Schnellnavigation in Microsoft Edge werden in bestimmten Seiten wie Wordpress 2015 nicht mehr große Teile der Webseite übersprungen. (#7143)
* In Microsoft Edge werden Sprungmarken korrekt übersetzt. (#7328)
* Die Braillezeile verfolgt nun die markierung korrekt, wenn Sie mehr Text markieren, als auf die Braillezeile passt. Wenn Sie mit Umschalt+Pfeil Ab mehrere Zeilen markieren, zeigt die Braillezeile nur die letzte markierte Textzeile an. (#5770)
* Wenn Sie auf twitter.com die Details zu einem Beitrag öffnen, zeigt NVDA in Firefox nicht mehr mehrfach "Abschnitt" an. (#5741)
* Die Schnellnavigationstasten für Tabellen berücksichtigen Layout-Tabellen nur noch, wenn diese auch in den Einstellungen für den Lesemodus aktiviert wurden. (#7382)
* Im Lesemodus für Firefox und Google Chrome überspringen die Schnellnavigationsbefehle für Tabellen nun verborgene Zellen. (#6652, #5655)

### Änderungen für Entwickler

* Die Zeitstempel im Protokoll enthalten jetzt auch Millisekunden. (#7163)
* NVDA muss mit Visual Studio Community 2015 erzeugt werden. Visual Studio Express wird nicht mehr unterstützt. (#7110)
 * Das Windows 10 SDK inkl. Tools ist nun ebenfalls erforderlich. Es kann aktiviert werden, wenn Sie Visual Studio installieren.
 * Lesen Sie den Abschnitt über Abhängigkeiten in der Liesmich-Datei für weitere Informationen.
* Die Inhaltserkennung von Windows 10 kann nun mit Hilfe des Paketes contentRecog verwendet werden. Dazu gehört die Beschreibung von Bildern und die Texterkennung. (#7361)
* Das Paket Python Json wird nun standardmäßig mitgeliefert. (#3050)

## 2017.2

Schwerpunkte dieser Version sind u. a. eine volle Unterstützung von Audio-Ducking unter Windows 10 Creators Update; Fehlerbehebungen beim Markieren von Text im Lesemodus; Verbesserungen in der Unterstützung von Microsoft Edge; sowie Verbesserungen bei der Anzeige von Webdokumenten, die das Aria-Current-Attribut verwenden.

### Neue Features

* In Microsoft Excel können nun Informationen über Zellrahmen mittels NVDA+F abgefragt werden. (#3044)
* Unterstützung für ARIA-Current-Attribute hinzugefügt. (#6358)
* Microsoft Edge unterstützt jetzt auch den automatischen Sprachenwechsel. (#6852)
* Unterstützung für den Windows-Rechner in Windows 10 LTSB hinzugefügt. (#6914)
* Wird die Tastenkombination zum Lesen der aktuellen Zeile dreimal hintereinander gedrückt, so wird die Zeile phonetisch buchstabiert. (#6893)
* Neue Sprache: Birmanisch.
* In Unicode Auf- und Ab-Pfeile sowie Bruchzeichen werden nun korrekt ausgesprochen. (#3805)

### Änderungen

* Die Navigation mit dem NVDA-Cursor bei aktivierter Option ""Einfacher Darstellungsmodus" in UIA-Anwendungen wurde vereinfacht. (#6948, #6950)

### Behobene Fehler

* Menüeinträge auf Webseiten, die Kontrollkästchen oder Auswahlschalter enthalten, können jetzt im Lesemodus aktiviert werden. (#6735)
* Die Rückfrage zur Löschung eines Konfigurationsprofils kann nun mit Escape beantwortet, also abgebrochen werden. (#6851)
* Probleme mit Abstürzen in Firefox und anderen Gecko-Anwendungen behoben, die in mehreren Prozessen ausgeführt werden. (#6885)
* Die Erkennung von Hintergrundfarben wurde verbessert; dies betrifft Elemente, die auf einen transparenten hintergrund gezeichnet werden. (#6467)
* Anzeige von Beschreibungen für Steuerelemente auf Webseiten in Internet Explorer 11 verbessert, Dies betrifft die Unterstützung des "aria-describedby"-Attributs für eingebettete Rahmen und objekte, die mehrere Ids besitzen. (#5784)
* Im Windows 10 Creators Update sind alle Audioducking-Funktionen wieder verfügbar. (#6933)
* NVDA zeigt nun auch solche (UIA)-Steuerelemente korrekt an, deren Tastenkombination nicht (richtig) definiert wurde. (#6779)
* An die Tastenkombination von (UIA)-Steuerelementen werden nicht mehr fälschlicherweise zwei Leerzeichen angehängt. (#6790)
* Einige Tastenkombinationen auf HIMS-Braillezeilen (wie z. B. Leertaste+Punkt 4) funktionieren nun korrekt. (#3157)
* Auf einigen (nicht-englischen) Systemen funktioniert nun die Verbindung mit seriellen Braillezeilen korrekt. (#6845)
* Beim Herunterfahren von Windows werden Konfigurationsdateien zunächst temporär gespeichert, bevor sie ersetzt werden. Dies verringert die Wahrscheinlichkeit für Beschädigungen der Konfigurationsdateien. (#3165)
* Beim Buchstabieren der aktuellen Zeile wird nun die aktuell eingestellte Sprache verwendet. (#6726)
* In Windows 10 Creators Update funktioniert die zeilenweise Navigation in Microsoft Edge nun bis zu dreimal so schnell wie zuvor. (#6994)
* Beim Verwenden von Microsoft Edge in Windows 10 Creators Update wird nicht mehr "Web Runtime Grouping" angezeigt. (#6948)
* Alle existierenden Versionen von SecureCRT werden nun unterstützt. (#6302)
* Adobe Acrobat Reader stürtzt nicht mehr bei bestimmten PDF-Dokumenten ab (speziell jene, die ein lehres ActualText-Atribut haben). (#7021, #7034)
* Im Lesemodus von Microsoft Edge werden interaktive Tabellen (Aria-Gitternetzlinien) nicht mehr übersprungen, wenn Sie mit den Schnelltasten T und Umschalt+T navigieren. (#6977)
* Wenn Sie im Lesemodus Umschalt+Pos1 drücken, nachdem Sie einen Text vorwärts markiert haben, wird nun die Zeile wie erwartet rückwärts demarkiert. (#5746)
* Im Lesemodus funktioniert das Markieren des gesamten Dokuments mit Strg+A auch dann, wenn sich der System-Cursor nicht am Anfang des Dokuments befindet. (#6909)
* Einige weitere Fehler beim Markieren im Lesemodus wurden behoben.. (#7131)

### Änderungen für Entwickler

* Die Befehlszeile von NVDA wird nun mit Hilfe des Moduls "Argparser" abgearbeitet. Dadurch werden Optionen wie "-R" oder "-Q" exklusiv abgearbeitet. (#6865)
* Die Funktion "core.calllater" fügt jetzt die Rückruffunktion nach einer angegebenen Zeitspanne in eine Warteschlange ein, anstatt sie direkt auszuführen. Dadurch wird verhindert, dass NVDA beim Anzeigen modaler Dialoge (wie Meldungsfenster) hängen bleibt. (#6797)
* Die Eigenschaft "InputGesture.identifiers" wird nicht mehr normalisiert. (#6945)
 * Untergeordnete Klassen müssen Bezeichner nicht mehr normalisieren, bevor sie sie zurückgeben.
 * Wenn Sie normalisierte Eigenschaften wünschen, verwenden Sie stattdessen "InputGesture.normalizedIdentifiers".
* Die Eigenschaft "InputGesture.logIdentifier" ist veraltet. Verwenden Sie stattdessen "InputGesture.identifiers[0]". (#6945)
* Veralteter Code wurde entfernt:
 * "speech.REASON_*"-Konstanten: Verwenden sie stattdessen die Konstanten "controlTypes.REASON_*". (#6846)
 * "i18nName" für Sprachausgaben-Einstellungen: Verwenden Sie stattdessen "displayName" und "displayNameWithAccelerator". (#6846, #5185)
 * "config.validateConfig". (#6846, #667)
 * "config.save": Verwenden Sie stattdessen "config.conf.save". (#6846, #667)
* Die Liste mit Vorschlägen zur Autovervollständigung im Kontextmenü der Python-Konsole zeigt keine führenden Objektpfade mehr vor den Symbolnamen an. (#7023)
* Es gibt jetzt ein Unit Test Framework für NVDA. (#7026)
 * Unit-Tests und Infrastruktur befinden sich im Verzeichnis tests/unit. Sehen Sie sich den Docstring in der Datei tests\unit\init.py für weitere Informationen an.
 * Sie können Tests mit "scons tests" durchführen. Weitere Informationen finden Sie im Abschnitt "Ausführen von Tests" in der Datei readme.md.
 * Wenn Sie einen Pull-Request für NVDA einreichen, sollten Sie zunächst die Tests durchführen und sicherstellen, dass diese bestanden werden.

## 2017.1

Schwerpunkte dieser Version sind u. a. die Ansage von Abschnitten und Spalten in Microsoft Word; Unterstützung beim Navigieren in, Lesen von und Einfügen von Anmerkungen in Kindle-Büchern sowie verbesserte Unterstützung von Microsoft Edge.

### Neue Features

* Mit der neuen Option "Seitenzahlen ansagen" in den Einstellungen für Dokument-Formatierungen können Sie sich nun Abschnittswechsel und -Nummern ansagen lassen. (#5946)
* Diese Option aktiviert des Weiteren eine Ansage von Spalten in mehrspaltigen Texten in Microsoft Word. (#5946)
* Der automatische Sprachenwechsel wird nun auch in WordPad unterstützt. (#6555)
* Der NVDA-Suchbefehl NVDA+Strg+F wird nun auch in Microsoft Edge unterstützt. (#6580)
* Die Schnellnavigationstasten für Schalter werden im Lesemodus in Microsoft Edge unterstützt. (#6577)
* Beim Kopieren von Tabellenblättern in Microsoft Excel werden Reihen- und Spaltenüberschriften berücksichtigt. (#6628)
* Unterstützung für Kindle für PC. Weitere Informationen finden Sie im Abschnitt für Kindle für PC im Handbuch. (#6247, #6638)
* Die Tabellennavigation im Lesemodus von Microsoft Edge wird nun unterstützt. (#6594)
* In Microsoft Excel gibt der Befehl zur Ausgabe des aktuellen Standorts (NVDA+Entf und NVDA+NUM-Entf) nun den Namen des Tabellenblatts und die aktuell hervorgehobene Zelle aus. (#6613)
* Im Dialogfeld zum Beenden von NVDA gibt es eine neue Option zum Neustart von NVDA im Debug-Modus. (#6689)

### Änderungen

* Die minimale Cursor-Blinkfrequenz beträgt nun 200 Millisekunden. Falls in einem Konfigurationsprofil ein niedrigerer Wert hinterlegt wurde, wird dieser automatisch angehoben. (#6470)
* In den Braille-Einstellungen wurde eine neue Option zum Ein-/Ausschalten des CursorBlinkens hinzugefügt. Bisher war das Abschalten der Cursor-Blinkfrequenz durch die Angabe von 0 als Cursor-Blinkfrequenz möglich. (#6470)
* eSpeak-NG wurde aktualisiert (commit e095f008, vom 10. Januar 2017). (#6717)
* Auf Grund von Änderungen im Windows 10 Creators Update ist die Option "Lautstärke anderer Anwendungen immer reduzieren" nicht mehr verfügbar. In älteren Versionen von Windows 10 steht die Option weiterhin zur Verfügung. (#6684)
* Auf Grund von Änderungen in Windows 10 Creators Update kann die Einstellung der Lautstärkereduktion "nur beim Sprechen" weder sicherstellen, dass die lautstärke anderer Anwendungen rechtzeitig reduziert wird, noch bevor NVDA zu sprechen beginnt; noch wird die Lautstärke lange genug reduziert, bis NVDA ausgesprochen hat. Diese Änderungen wirken sich nicht auf älteren Windows 10-Versionen aus. (#6684)

### Fehlerbehebungen

* Fehler beim absatzweisen Navigieren im Lesemodus von Microsoft Word korrigiert. (#6368)
* Tabellen, die von Microsoft Excel in Microsoft Word eingefügt wurden, werden nicht mehr ignoriert. (#5927)
* Bei dem Versuch, in geschützte Microsoft Excel-Zellen zu schreiben wird nun ein Signalton abgespielt. Bisher wurden die eingegebenen zeichen gesprochen, obwohl diese nicht geschrieben wurden. (#6570)
* Das Drücken der Escape-Taste in Microsoft Excel schaltet nun nicht mehr unerwartet in den Lesemodus um. Dies geschieht nur noch, wenn der Lesemodus mittels NVDA+Leertaste eingeschaltet und anschließend die Fokusmodus mittels Eingabe aktiviert wurde. (#6569)
* NVDA stürzt nicht mehr in Microsoft Excel-Tabellenblättern ab, bei denen eine ganze Reihe/Spalte in eine Zelle zusammengeführt wurde. (#6216)
* Die Ansage von überlagertem Text in Microsoft Excel wurde verbessert. (#6472)
* NVDA zeigt nun schreibgeschützte Kontrollkästchen korrekt an. (#6563)
* NVDA zeigt nun keine Warnmeldungen mehr an, wenn der Logo-Klang nicht abgespielt werden konnte. (#6289)
* Nicht verfügbare Steuerelemente in Menübändern von Microsoft Excel werden als solche angezeigt. (#6430)
* NVDA zeigt nicht mehr "Feld" an, wenn Fenster minimiert werden. (#6671)
* Im Windows 10 Creators Update werden in universellen Windows-Platform-Apps (UWP) eingegebene Zeichen gesprochen. (#6017)
* Bei der Verwendung mehrerer Monitore funktioniert die Mausverfolgung nun über alle Monitore hinweg. (#6598)
* NVDA verhält sich korrekt, wenn Sie Windows Media Player beenden, während ein Schieberegler den Fokus besitzt. (#5467)

### Änderungen für Entwickler

* Konfigurationsprofile und -Dateien werden automatisch aktualisiert. Falls beim Aktualisieren ein Fehler auftritt, wird eine Fehlermeldung mit der Ebene "info" im Protokoll hinterlegt. (#6470)

## 2016.4

Zu den Schwerpunkten dieser Version gehören Verbesserungen in der Unterstützung von Microsoft Edge; der Lesemodus in der Mail-App in Windows 10 sowie Verbesserungen in Dialogfeldern von NVDA.

### Neue Features

* NVDA kann Zeileneinrückungen nun auch mit Hilfe von Signaltönen ausgeben. Um dies einzustellen, können Sie die neue Option "Zeileneinrückungen ausgeben durch..." in den Einstellungen für Dokument-Formatierung verwenden. (#5906)
* Unterstützung für die Braillezeile Orbit Reader 20. (#6007)
* Eine neue Option zum Anzeigen des Sprachbetrachters beim Start von NVDA wurde hinzugefügt. Dies kann mittels eines Kontrollkästchens im Sprachbetrachter eingeschaltet werden. (#5050)
* Die Position und Größe des Sprachbetrachters wird beim erneuten Öffnen wiederhergestellt. (#5050)
* Felder mit Querverweisen in Microsoft Word werden von NVDA als Links angezeigt und können wie solche aktiviert werden. (#6102)
* Die Unterstützung für folgende Braillezeilen wurden hinzugefügt: Baum SuperVario2, Baum Vario 340 und HumanWare Brailliant2. (#6116)
* Grundlegende Unterstützung für die jährliche Aktualisierung von Microsoft Edge. (#6271)
* Zum Lesen von Mails in der Mail-App in Windows 10 wird nun der Lesemodus verwendet. (#6271)
* Neue Sprache: Littauisch.

### Änderungen

* Libluis wurde auf Version 3.0.0 aktualisiert. Dies enthällt signifikante Verbesserungen der vereinheitlichten englischen Braille-schrift. (#6109, #4194, #6220, #6140)
* Die Schalter zum Aktivieren und Deaktivieren von Erweiterungen besitzen nun Tastenkombinationen. (#6388)
* Einige (kosmetische) Änderungen wurden vorgenommen. (#6317, #5548, #6342, #6343, #6349)
* Die Einstellungen für Dokument-Formatierung werden korrekt ausgegeben. (#6348)
* Das Dialogfeld für die Aussprache von Symbolen und Sonderzeichen besitzt jetzt die korrekte Breite. (#6101)
* Die Schnellnavigationstasten für Formularfelder und Eingabefelder berücksichtigen nun auch schreibgeschützte Felder. (#4164)
* Die Option "Formatierungen hinter dem Cursor ansagen" wurde umbenannt in "Formatänderungen hinter dem Cursor ausgeben", weil die Meldungen auch in Braille ausgegeben werden. (#6336)
* Das Erscheinungsbild des Willkommensdialogs wurde korrigiert. (#6350)
* In sämtlichen Dialogen werden die Schalter "OK" und "Abbrechen" nun rechtsbündig angezeigt. (#6333)
* Für numerische Eingaben werden nun Drehknöpfe verwendet. (#6099)
* Eingebettete Rahmen (Dokumente, die in Dokumente eingebettet sind) werden in Firefox nun als Rahmen ausgegeben. Dies wurde Browserübergreifend vereinheitlicht. (#6047)

### Fehlerbehebungen

* Ein Fehler wurde behoben, wenn beim Beenden von NVDA der Sprachbetrachter angezeigt wurde. (#5050)
* In Firefox werden Verweise von Grafiken wie erwartet berücksichtigt und angezeigt. (#6051)
* Das Drücken der Eingabetaste in Wörterbuchdialogen führt nun wie erwartet zum Speichern der Einträge. (#6206)
* Beim Wechsel der Eingabemethode werden Meldungen in Braille angezeigt. (#5892, #5893)
* Wenn Sie eine Erweiterung aus- und wieder einschalten, wird deren Status korrekt angezeigt. (#6299)
* In Microsoft Word werden Seitenzahlen korrekt ausgegeben, auch wenn sich diese in Überschriften befinden. (#6004)
* Im Dialogfeld "Interpunktion und Symbol-Aussprache" können Sie nun die Maus benutzen, um den Fokus auf die Liste der Symbole und auf die Eingabefelder zu setzen. (#6312)
* Die Elementliste von Microsoft Word funktioniert nun korrekt, wenn das Dokument einen ungültigen Link enthält. (#5886)
* Nach dem Schließen des Sprachbetrachters mit Alt+F4 spiegelt das Kontrollfeld für den Sprachbetrachter dessen Status korrekt wider. (#6340)
* Probleme beim erneuten Laden von Erweiterungen mit Hilfe der Tastenkombination NVDA+Strg+F3 wurden behoben. (#2892, #5380)
* In der Sprachenliste in den allgemeinen Einstellungen werden einige Sprachen (wie z. B. Aragonesisch) richtig angezeigt. (#6259)
* Im Dialogfeld "Einstellungen" -> "Eingaben" werden emulierte Tastendrücke und Tastenkombinationen in der in NVDA eingestellten Sprache angezeigt. (#6212)
* Das Umstellen der Sprache in NVDA wirkt sich nun erst nach dem Neustart von NVDA aus. (#4561)
* Im Dialogfeld zum Hinzufügen neuer Wörterbuch-Einträge darf das Feld für das Suchmuster nicht mehr leer bleiben. (#6412)
* Probleme bei der Suche nach seriellen Anschlüssen bei einigen Braillezeilen-Treibern wurden behoben. (#6462)
* In Microsoft Word werden numerierte Listen korrekt erkannt, wenn sie sich innerhalb von Tabellenzellen befinden. (#6446)
* Sie können das Dialogfeld "Einstellungen" -> "Eingaben" verwenden, um NVDA-Befehle an Tasten bzw. Tastenkombinationen der Braillezeilen von HandyTech zuzuweisen. (#6461)
* Wenn Sie in Microsoft Excel innerhalb einer Tabelle die Eingabetaste drücken, erkennt NVDA korrekt, dass sich der Fokus in die nächste Zeile bewegt hat. (#6500)
* iTunes friert nicht mehr ein, wenn Sie im iTunes Store, Apple Music, etc. den Lesemodus verwenden. (#6502)
* Probleme mit Abstürzen von 64-Bit-Versionen von Mozilla- und Chrome-basierten Anwendungen behoben. (#6497)
* In Firefox mit aktivierter Multi-Prozessunterstützung funktioniert der lesemodus korrekt. (#6380)

### Änderungen für Entwickler

* Sie können nun Anwendungsmodule für Programme erstellen, deren Namen einen Punkt enthalten. der Punkt muss im Namen des Anwendungsmoduls durch einen Unterstrich ersetzt werden. (#5323)
* Das Modul "gui.guihelper" enthält Funktionen, mit denen die Erstellung neuer WX-Oberflächen vereinfacht wird. Dies betrifft Größen und Abstände von wx-Elementen. (#6287)

## 2016.3

Schwerpunkte dieser Version sind u. a. eine Möglichkeit zum Deaktivieren einzelner Erweiterungen; die Unterstützung von Formularfeldern in Microsoft Excel, Verbesserungen bei der Ansage von Farben und Fehlerbehebungen bzgl. einiger Braillezeilen sowie Fehlerbehebungen und Verbesserungen an der Unterstützung für Microsoft Word.

### Neue Features

* Der Lesemodus kann nun verwendet werden, um in Microsoft Edge PDF-Dokumente zu lesen, sofern Sie das Windows 10 Anniversary Update installiert haben. (#5740)
* In Microsoft Word wird durchgestrichener und doppelt durchgestrichener Text erkannt. (#5800)
* In Microsoft Word wird der Titel einer Tabelle korrekt erkannt. Wenn außerdem eine Beschreibung vorhanden ist, kann diese im Lesemodus mit dem Befehl Ausführliche Beschreibung öffnen (NVDA+D) angezeigt werden. (#5943)
* In Microsoft Word wird die Position im Dokument korrekt ausgegeben, wenn Sie mittels Alt+Umschalt+Pfeil auf und Alt+Umschalt+Pfeil ab Absätze im Dokument verschieben. (#5945)
* In Microsoft Word werden jetzt Zeilenabstände erkannt. Die ansage von Zeilenabständen kann in den Einstellungen für Dokument-Formatierungen eingestellt werden. Außerdem werden die Zeilenabstände angesagt, wenn Sie den Zeilenabstand mit den Tastenkombinationen von Word ändern oder wenn Sie sich beim Navigieren im Dokument in einen Abschnitt mit einem anderen Zeilenabstand bewegen. (#2961)
* Im Internet Explorer werden strukturierende HTML5-Elemente erkannt. (#5591)
* Die Ansage von kommentaren (z. B. in Microsoft Word) kann nun in den Einstellungen für Dokument-Formatierungen eingestellt werden. (#5108)
* Sie können nun einzelne Erweiterungen im Dialogfeld "Erweiterungen verwalten" deaktivieren. (#3090)
* Zusätzliche Tastenkombinationen für die Braillezeilen ALVA BC640 und BC680 wurden hinzugefügt. (#5206)
* Es gibt einen neuen Befehl zum Bewegen der Braillezeile zum Fokus. Momentan wird dieser Befehl nur von Alva-Braillezeilen verwendet; es steht Ihnen jedoch frei, diesen Befehl auch an Ihrer Braillezeile auf eine Tastenkombination zu legen. Hierfür können Sie das Dialogfeld "Einstellungen" -> "Eingaben" verwenden. (#5250)
* In Microsoft Excel können Sie nun mit Formularfeldern interagieren. Verwenden Sie hierfür entweder die Elementliste oder die Schnellnavigationstasten. (#4953)
* Es gibt einen neuen Befehl zum Umschalten des einfachen Darstellungsmodus. Sie können das Dialogfeld "Einstellungen" -> "Eingaben" verwenden. (#6173)

### Änderungen

* NVDA gibt Farben nun leichter verständlich mit 9 Farbnamen und in verschiedenen Schattierungen wieder, anstatt subjektivere aber dafür schwere verständliche Bezeichnungen zu verwenden. (#6029)
* Das Verhalten von NVDA+F9 und NVDA+F10 wurde geändert. Wird NVDA+F10 einmal gedrückt, so wird der Text zwischen der zuvor gesetzten Startmarke und der aktuellen Position des NVDA-Cursors markiert. Wird die Tastenkombination zweimal gedrückt, so wird er in die Zwischenablage kopiert. (#4636)
* eSpeak NG auf die Testversion Master 11b1a7b (22. Juni 2016) aktualisiert. (#6037)

### Fehlerbehebungen

* Im Lesemodus in Microsoft Word wird beim Kopieren von Text in die Zwischenablage die Formatierung beibehalten. (#5956)
* In Microsoft Word werden Word-eigene Tabellennavigationsbefehle (Alt+Pos1, Alt+Ende, Alt+Seite auf und Alt+Seite ab) korrekt unterstützt. Dies gilt auch für die Markierungsbefehle für Tabellen (Alt+Umschalt+Pos1, Alt+Umschalt+Ende, Alt+Umschalt+Seite auf, Alt+Umschalt+Seite ab). (#5961)
* In Dialogen von Microsoft Word wurde die Objektnavigation von NVDA verbessert. (#6036)
* In Anwendungen wie Visual Studio 2015 werden Tastenkombinationen wie Strg+C korrekt angesagt. (#6021)
* Fehler bei der Suche nach seriellen Anschlüssen bei der Verwendung einiger Braillezeilentreiber behoben. (#6015)
* Die Ansage von Farben in Microsoft Word ist nun genauer, da Änderungen im Design von Microsoft Office berücksichtigt werden. (#5997)
* In Windows 10-Versionen die im Aprill 2016 oder später erschienen sind, wird Microsoft Edge unterstützt. Außerdem werden Suchvorschläge im Startmenü unterstützt. (#5955)
* In Microsoft Word funktioniert die Ansage von Tabellenüberschriften besser, wenn Sie sich in einer verbundenen Zelle befinden. (#5926)
* In Windows 10-Mail werden Nachrichten korrekt gelesen. (#5635)
* Wenn die Ansage von Funktionstasten aktiviert ist, werden Umschalttasten (Num lock, Dauergroßschreibung etc.) nicht mehr zweimal angesagt. (#5490)
* Die Dialogfelder der Benutzerkontensteuerung werden ab Windows 10 Anniversary update wieder korrekt ausgelesen. (#5942)
* Im Web-Conference-Plugin (z. B. auf [www.out-of-sight.net](http://www.out-of-sight.net)) spielt NVDA keine Signaltöne mehr ab, wenn sich die Aussteuerungsanzeige für das Mikrofon ändert. (#5888)
* Die Befehle Weitersuchen und Rückwärtssuchen berücksichtigen jetzt die Groß-/Kleinschreibung, wenn beim vorherigen Aufruf des Suchdialogs die Groß-/Kleinschreibung berücksichtigt wurde. (#5522)
* Beim Bearbeiten von Wörterbucheinträgen wird bei fehlerhaften regulären Ausdrücken eine Fehlermeldung angezeigt. Außerdem stürtzt NVDA nicht mehr ab, wenn ein Wörterbuch fehlerhafte Einträge enthält. (#4834)
* Falls NVDA nicht (mehr) in der Lage sein sollte, mit einer Braillezeile zu kommunizieren (etwa weil sie abgezogen wurde), wird die Verwendung von Braillezeilen generell unterlassen. (#1555)
* Leistungsverbesserungen im Dialogfeld "Filtern nach" im Lesemodus. (#6126)
* Die von NVDA zurückgegebenen namen für Filtergrundmuster in Microsoft Excel entsprechen jetzt denen, die tatsächlich in Excel verwendet wurden. (#6092)
* Verbesserungen im Anmeldebildschirm von Windows 10 (einschließlich Aktivierung des Kennwortfeldes mittels Berührung) und der Ansage von Meldungen. (#6010)
* NVDA unterstützt nun die zweiten Routing-Tasten an Alva BC640/680-Braillezeilen. (#5206)
* NVDA kann Windows 10-Benachrichtigungen nun wieder anzeigen. Dies betrifft vor allem aktuelle Versionen von Windows 10. (#6096)
* NVDA erkennt Tastendrücke an Baum-/Humanware-Braillezeilen zuverlässiger. (#6035)
* Wenn die Ausgabe von Zeilennummern im Dialogfeld für Dokument-Formatierungen aktiviert ist, werden die Zeilennummern auch in Braille angezeigt. (#5941)
* Wenn die Sprache abgeschaltet wurde, erscheinen Objektinformationen (z. B. beim Drücken von NVDA+Tab) trotzdem im Sprachbetrachter. (#6049)
* In der Nachrichtenansicht von Microsoft Outlook 2016 werden nun nicht länger bestimmte Informationen in der Entwurfsansicht mehr angesagt. (#6219)
* In Chrome und Chrome-basierten Browsern funktioniert der Lesemodus nun korrekt, wenn der Browser in einer anderen Sprache als Englisch verwendet wird. (#6249)

### Änderungen für Entwickler

* Informationen zur Protokollierung von bestimmten Eigenschaften werden nicht mehr rekursiv in einer Endlosschleife behandelt. (#6122)

## 2016.2.1

Diese Version behebt einige Fehler in Microsoft Word:

* Word stürzt nicht mehr ab, wenn es unter Windows XP gestartet wird. (#6033)
* Die Ansage von Grammatikfehlern wurde entfernt, weil sie zu Abstürzen führte. (#5954, #5877)

## 2016.2

Schwerpunkte sind u. a. die Ausgabe von Rechtschreibfehlern beim schreiben, die Ausgabe von Grammatikfehlern in Microsoft Word; sowie Verbesserungen und Fehlerbehebungen in der Unterstützung von Microsoft Office.

### Neue Features

* Wenn Sie im Internet Explorer und anderen MSHTML-Dokumenten mit den Schnellnavigationstasten A und Umschalt+A zur nächsten oder vorherigen Anmerkung springen, wird auch eingefügter oder gelöschter Text angesprungen. (#5691)
* In Microsoft Excel wird bei Zellengruppen sowohl die Verschachtelungsebene als auch der Status (erweitert/reduziert) angezeigt. (#5690)
* Beim zweimaligen Drücken der Tastenkombination für die Ansage der Textformatierungen werden nun die Informationen im Lesemodus angezeigt. (#4908)
* In Microsoft Excel 2010 und neuer werden nun Zellschattierungen und Rahmen angesagt. Die automatische Ansage hierzu wird von der Einstellung für die Dokument-Formatierungen in NVDA gesteuert. (#3683)
* Neue Braille-Übersetzungstabelle: Griechisch (Koine). (#5393)
* Im Protokollbetrachter kann das Protokoll mit der Tastenkombination Strg+S gespeichert werden. (#4532)
* Über eine Option in den Tastatur-Einstellungen kann nun festgelegt werden, ob ein Signalton bei Rechtschreibfehlern während der Eingabe wiedergegeben werden soll. Dies gillt, sofern die Ausgabe von Rechtschreibfehlern aktiviert ist und im aktuellen Feld unterstützt wird. (#2024)
* Die Ausgabe von Grammatikfehlern in Microsoft Word kann nun in den Einstellungen für Dokument-Formatierung von NVDA ein- oder ausgeschaltet werden. (#5877)

### Änderungen

* Im Lesemodus und in Eingabefeldern werden beide Eingabetasten nun gleich behandelt. (#5385)
* NVDA verwendet nun eSpeeak NG. (#5651)
* In Microsoft Excel wird die Spaltenüberschrift korrekt erkannt, wenn sich zwischen der aktuellen Zelle und der Spaltenüberschrift eine leere Zeile befindet. (#5396)
* In Microsoft Excel werden die Zellkoordinaten nun vor den Überschriften angesagt. (#5396)

### Fehlerbehebungen

* Wenn Sie die Schnellnavigationstasten verwenden, um zu einem Element eines Typs zu navigieren, der im aktuellen Dokument nicht unterstützt wird, wird dies von NVDA ausdrücklich angezeigt. (#5691)
* Wenn Sie die Liste der Tabellenblätter in Excel aufrufen, werden nun auch Tabellenblätter einbezogen, die nur Diagramme enthalten. (#5698)
* NVDA gibt nun nicht länger mehr belanglose Informationen beim Fensterwechseln in Java-Anwendungen mit mehrfachen Fenstern wie z. B. in IntelliJ oder Android Studio wieder. (#5732)
* In Scincilla-basierten Anwendungen wie Notepad++ wird die Brailleanzeige korrekt aktualisiert, wenn Sie den Cursor mit Hilfe der Braillezeile bewegen. (#5678)
* NVDA stürzt nun nicht mehr ab, wenn Sie die Brailleausgabe aktivieren. (#4457)
* In Microsoft Word wird die Absatzeinrückung immer in der vom Anwender gewählten maßeinheit ausgegeben (z. B. Zentimeter). (#5804)
* Wenn Sie eine Braillezeile verwenden, werden viele meldungen in Braille angezeigt, die zuvor nur gesprochen wurden. (#5557)
* In zugänglichen Java-Anwendungen wird die Ebene in Baumstrukturen korrekt angezeigt. (#5766)
* Probleme mit abstürzendem Adobe Flash und Firefox behoben. (#5367)
* In Google Chrome und Chrome-basierten Browsern können Dokumente, die sich innerhalb von Web-Anwendungen befinden, im Lesemodus gelesen werden. (#5818)
* In Google Chrome und Chrome-basierten Browsern können Sie NVDA in den Lesemodus zwingen, während Sie sich in Web-Anwendungen befinden. (#5818)
* Im Internet Explorer schaltet NVDA nicht mehr irrtümlich in den Lesemodus um, wenn der Fokus auf ein Element bewegt wird, dessen Eigenschaft Aria-ActivateDescendant verwendet wird. Dies betrifft beispielsweise die Vorschlagsliste im Adressfeld beim Erstellen einer Nachricht in Gmail. (#5676)
* In Microsoft Word-Dokumenten mit großen Tabellen wird NVDA nun nicht mehr abstürzen, wenn die Ausgabe von Reihen-/Spaltenüberschriften aktiviert ist. (#5878)
* In Microsoft Word wird NVDA Text nicht mehr länger als Überschrift anzeigen, wenn er zwar eine Gliederungsebene besitzt, nicht jedoch mit einer der integrierten Vorlagen für Überschriften formatiert wurde. (#5186)
* Im Lesemodus für Microsoft Word funktionieren die Befehle zum Navigieren in/aus Container-Objekten auch für Tabellen. (#5883)

### Änderungen für Entwickler

* Die C++-Komponenten von NVDA werden nun mit Microsoft Visual Studio 2015 erzeugt. (#5592)
* Sie können nun einen Text oder eine HTML-Meldung für den Anwender im Lesemodus darstellen, in dem Sie ui.browseableMessage verwenden. (#4908)
* Wenn im Benutzerhandbuch der Befehl <!-- KC:setting für eine Einstellung verwendet wird, die eine gemeinsame Tastenkombination für alle Tastaturschemen besitzt, wird nun eine Spalte in voller Breite verwendet. (#5739) -->

## 2016.1

Schwerpunkte dieser Version sind u. a. eine Option zum Reduzieren der Lautstärke anderer Anwendungen zugunsten von NVDA; Verbesserungen bei der Brailleausgabe und der Unterstützung von Braillezeilen; mehrere herausragende Neuerungen in der Unterstützung von Microsoft Office sowie Fehlerbehebungen im Lesemodus von iTunes.

### Neue Features

* Neue Braille-Übersetzungstabellen: Polnisches 8-Punkt-Computerbraille, Mongolisch. (#5537 #5574)
* Mit Hilfe zweier neuer Optionen im Braille-Einstellungsdialog kann nun die Form des Cursors auf der Braillezeile geändert oder die Anzeige des Cursors gänzlich abgeschaltet werden. (#5198)
* NVDA kann nun mittels Bluetooth mit HIMS Smart Beetle Braillezeilen kommunizieren. (#5607)
* Ab Windows 8 und neuer kann NVDA die Lautstärke anderer Audio-Quellen optional reduzieren. Dies kann im Dialogfeld für die Sprachausgabe mit der Option "Lautstärke anderer Audio-Quellen reduzieren" oder NVDA+Umschalt+D eingestellt werden. (#3830, #5575)
* Unterstützung für folgende Braillezeilen: APH Refreshabraille im HID-Modus, Baum VarioUltra und Pronto! wenn diese mittels USB angeschlossen werden. (#5609)
* Unterstützung für HumanWare Brailliant BI/B-Braillezeilen bei ausgewähltem OpenBraille-Protokoll. (#5612)

### Änderungen

* Die Ansage betonter Texte ist nun standardmäßig ausgeschaltet. (#4920)
* Die Tastenkombination für den Auswahlschalter "Formel" in der Elementliste von Microsoft Excel wurde in Alt+R geändert. Jetzt kollidiert sie nicht mehr mit Alt+F für das Suchfeld. (#5527)
* Der Braille-Übersetzer LibLouis wurde auf 2.6.5 aktualisiert. (#5574)
* Das Wort "Text" wird nun nicht länger ausgegeben, wenn der Fokus oder der NVDA-Cursor zu Text-Objekten bewegt wird. (#5452)

### Fehlerbehebungen

* In iTunes 12 wird der Lesemodus korrekt aktualisiert, wenn eine Seite im iTunes Store neu geladen wird. (#5191)
* Die Schnellnavigation für Überschriften bestimmter Ordnung funktioniert nun auch dann korrekt, wenn die Ebene der Überschrift aus Gründen der Barrierefreiheit mittels Aria-Level festgelegt wurde. Dies betrifft Internet Explorer und MSHTML-Dokumente. (#5434)
* In Spotify springt der Fokus nicht mehr regelmäßig auf unbekannte Objekte. (#5439)
* Wenn Sie von einer anderen Anwendung aus zurück zu Spotify wechseln, wird der Fokus korrekt wiederhergestellt. (#5439)
* Das Ein- und Ausschalten des Lesemodus wird nun auch in Braille angezeigt. (#5239)
* Der Schalter "Start" auf der Taskleiste wird nicht mehr als Liste oder als "Ausgewählt" ausgegeben. (#5178)
* Wenn Sie in Microsoft Outlook Nachrichten schreiben, werden meldungen wie "eingefügt" nicht mehr angezeigt. (#5486)
* Wenn Sie in einem Editorfenster Text markieren, scrollt die Braillezeile korrekt weiter. (#5410)
* NVDA stürzt nicht mehr ab, wenn Sie eine Eingabeaufforderung in Windows 10 mit Alt+F4 schließen. (#5343)
* Wenn Sie in der Elementliste im Lesemodus den Elementtyp ändern, wird das Suchfeld automatisch geleert. (#5511)
* Wenn Sie in Mozilla-Anwendungen die Maus auf ein Eingabefeld bewegen, wird nicht mehr der gesamte Feldinhalt gelesen, sondern (wie erwartet) das Wort, die Zeile etc. unter dem Mauszeiger. (#5535)
* Wenn Sie in Mozilla-Anwendungen die Maus innerhalb von Eingabefeldern bewegen, wird das Lesen nicht bei Elementen unterbrochen, die sich innerhalb der zu lesenden Einheit (Wort, Zeile etc.) befinden. (#2160, #5535)
* Wenn Sie die Webseite shoprite.com mit dem Internet Explorer aufsuchen, wird deren Inhalt nun erwartungsgemäß angezeigt. (Hierbei werden insbesondere ungültig gesetzte Sprachenauszeichnungen besser verarbeitet.) (#5569)
* In Microsoft Word werden Änderungen am Dokument nur dann durch NVDA mitgeteilt, wenn sie auch tatsächlich im Dokument ausgezeichnet werden. Hierzu zählen beispielsweise Meldungen über eingefügten oder gelöschten Text. (#5566)
* Wenn ein Umschalter fokussiert wird, gibt NVDA aus, wenn dieser von gedrückt zu nicht gedrückt wechselt. (#5441)
* Die Ansage bei Änderung der Form des Mauszeigers funktioniert nun ordnungsgemäß. (#5595)
* Bei der Ansage von Zeileneinrückungen werden geschützte Leerzeichen nun wie normale Leerzeichen behandelt. Dies führte zuvor zu Ansagen wie "Leerzeichen Leerzeichen Lerzeichen" anstatt von 3 Leerzeichen. (#5610)
* Beim Schließen der Liste der Schriftsätze bei der Eingabe komplexer Sonderzeichen wird der Fokus korrekt wiederhergestellt. (#4145)
* Wenn die Menübänder in Office 2013 und neuer so eingestellt werden, dass sie nur Registerkarten anzeigen, werden sie von NVDA wie erwartet dargestellt, wenn eine Registerkarte aktiviert wird. (#5504)
* Korrekturen und Verbesserungen beim Erkennen und Einbinden von Touch-Screen-Gesten: (#5652)
* Wischgesten werden in der Eingabehilfe nicht mehr erkannt. (#5652)
* Wenn sich in Microsoft Excel ein Kommentar auf eine verbundene Zelle bezieht, wird er korrekt erkannt. (#5704)
* Fehler behoben, wonach NVDA in sehr seltenen Fällen den Inhalt von Tabellenblättern in Excel nicht angezeigt hat, während die Option "Spalten- und Reihenüberschriften von Tabellen ansagen" aktiviert ist. (#5705)
* Fehler bei der Braille-Anzeige von koreanischen Zeichen behoben. (#5640)
* Die Eingabe von asiatischen Sonderzeichen in Google Chrome funktioniert nun erwartungsgemäß. (#4080)
* Beim Durchsuchen von Apple Music im Itunes Store wird der Lesemodus korekt aktualisiert. (#5659)
* Wenn Sie in Microsoft Excel mit Umschalt+F11 ein neues Tabellenblatt erstellen, wird die Cursorposition im Tabellenblatt korrekt angezeigt. (#5689)

### Änderungen für Entwickler

* Sie können die neue Klasse audioDucking.audioDucker verwenden, wenn Sie beim Wiedergeben von Audiomaterial die Lautstärke anderer Audioquellen reduzieren wollen. (#3830)
* Der Konstruktor von nvwave.WavePlayer besitzt nun ein Argument namens wantDucking, mit dessen Hilfe Sie angeben können, ob während der Wiedergabe die Lautstärke anderer Audioquellen reduziert werden soll. (#3830)
 * Wenn die Funktion aktiviert (ist Standard), sollte zu gegebener Zeit WavePlayer.idle aufgerufen werden.
* Die Brailleausgabe wurde verbessert: (#5609)
 * Threadsichere Braillezeilen-Treiber können sich über das Attribut BrailleDisplayDriver.isThreadSafe als solche deklarieren. Ein Treiber muss threadsicher sein, um von den folgenden Leistungsmerkmalen zu profitieren.
 * Die Leistung des Treibers wird verbessert, weil Daten im hintergrund geschrieben werden
 * HwIo.Serial erweitert pyserial, um eine Callable beim Empfang von Daten aufzurufen, anstatt dass Treiber Polling durchführen müssen.
 * hwIo.Hid unterstützt Braillezeilen, die über USB HID kommunizieren.
 * hwPortUtils und hwIo können optional ein detailliertes Debug-Logging anbieten, einschließlich der gefundenen Geräte und aller gesendeten und empfangenen Daten.
* Neue Eigenschaften für Touchscreen-Gesten: (#5652)
 * Das Objekt MultitouchTracker enthält nun eine Eigenschaft namens childTrackers. Hier werden die einzelnen Teile einer Mehrfachgeste gespeichert. Ein doppeltes Tippen mit zwei Fingern enthält z. B. zwei Zweifinger-Tippgesten. Die Zweifinger-Tippgesten enthalten ihrerseits zwei Tippgesten.
 * MultiTouchTracker-Objekte enthalten außerdem eine Eigenschaft rawSingleTouchTracker, falls der Tracker das Ergebnis einer Geste ist, die mit einem Finger ausgeführt wird. Der Tracker gestattet Ihnen den Zugriff auf die vom Betriebssystem zurückgegebene ID des Fingers. Er erlaub Ihnen außerdem festzustellen, ob der Finger momentan (noch) den Bildschirm berührt.
 * TouchInputGestures enthalten nun X- und Y-Koordinaten. Dadurch ist es nicht länge nötig, auf den Tracker zuzugreifen.
 * TouchInputGestures enthalten nun eine Eigenschaft namens preheldTracker. Diese Eigenschaft gibt über Finger auskunft, die auf dem Bildschirm gehalten werden.
* Es werden zwei neue Touchscreen-Gesten erkannt: (#5652)
 * Mehrfachgesten mit Tippen und Halten (Beispiel: Zweifaches Tippen und halten).
 * Die Angabe losgelassener Finger wurde verallgemeinert (z. B. Halten+Wischen für ein Halten und Wischen mit einem Finger).

## 2015.4

Schwerpunkte dieser Version sind u. a. Leistungsverbesserungen in Windows 10; Unterstützung für das Center für erleichterte Bedienungen in Windows 8 und neuer; Verbesserungen an Microsoft Excel wie z. B. das Auflisten und umbenennen von Tabellenblättern und der Zugriff auf gesperrte zellen in geschützten Arbeitsblättern; sowie die Unterstützung erweiterter Eingabefelder in Mozilla Firefox, Google Chrome und Mozilla Thunderbird.

### Neue Features

* Unter Windows 8 und neuer taucht NVDA nun im Center für erleichterte Bedienungen auf. (#308)
* Beim Navigieren zwischen Zellen in Excel werden Änderungen an Textformatierungen ausgegeben, sofern die entsprechenden Optionen in den Einstellungen für Textformatierungen aktiviert sind. (#4878)
* Eine neue Option zum Ansagen von betontem Text hinzugefügt. Dies betrifft momentan nur die html-Tags em und strong im Internet Explorer und anderen MSHTML-Elementen. (#4920)
* Falls die Ansage von Dokumentänderungen in den Einstellungen für Dokument-Formatierungen aktiviert ist, werden nun auch eingefügte und gelöschte Textpassagen ausgegeben. Dies betrifft momentan den Internet Explorer und MSHTML-Dokumente. (#4920)
* Wenn Sie sich mit Hilfe der Elementliste die Änderungen im Dokument anzeigen lassen, werden jetzt mehr Informationen angezeigt. (#4920)
* Sie können in Microsoft Excel nun die Elementliste (NVDA+F7) verwenden, um Tabellenblätter aufzulisten oder umzubenennen. (#4630, #4414)
* Sie können im Dialogfeld für die Aussprache von Symbolen und Sonderzeichen festlegen, ob Symbole unbehandelt an die Sprachausgabe gesendet werden sollen (um beispielsweise eine Sprechpause oder eine andere Betonung zu erhalten). (#5234)
* In Microsoft Excel meldet NVDA nun alle vom Blattautor gesetzten Eingabemeldungen auf Zellen. (#5051)
* Unterstützung für Baum Pronto! V4 und VarioUltra Braillezeilen bei Bluetooth-Verbindungen. (#3717)
* Unterstützung für erweiterte Eingabefelder in Mozilla-Anwendungen wie z. B. Google Docs bei Verwendung einer Braillezeile in Mozilla Firefox und HTML-Mail in Mozilla Thunderbird. (#1668)
* Unterstützung für erweiterte Eingabefelder in Google Chrome und Chrome-basierten Browsern wie z. B. Google Docs unter Verwendung einer Braillezeile. (#2634)
 * Erforderlich ist Chrome Version 47 oder neuer.
* Im Lesemodus in Microsoft Excel können Sie nun zu gesperrten Zellen in geschützten Arbeitsblättern navigieren. (#4952)

### Änderungen

* Die Option "Dokumentänderungen ausgeben " in den Einstellungen für Dokument-Formatierungen ist nun standardmäßig aktiviert. (#4920)
* Beim Zeichenweisen Navigieren in Word-Dokumenten werden nun weniger Informationen angezeigt, sofern die Option zum Verfolgen von Änderungen aktiviert ist. Dies erlaubt eine flüssigere Navigation. Um mehr Informationen über Änderungen im Dokument zu erhalten, verwenden Sie die elementliste. (#4920)
* Der Braille-Übersetzer LibLouis wurde auf 2.6.4 aktualisiert. (#5341)
* Einige Sonderzeichen (einschließlich grundlegende mathematische zeichen) wurden in die Ebene einige verschoben, sodass sie standardmäßig ausgesprochen werden. (#3799)
* Sofern die Sprachausgabe dies unterstützt, wird jetzt bei Runden Klammern und beim Strich (–) eine Sprechpause eingelegt. (#3799)
* Beim Markieren von Text wird jetzt der (de)markierte Text vor dem Ausdruck (de)markiert gesprochen. (#1707)

### Fehlerbehebungen

* Erhebliche Leistungsverbesserungen beim Navigieren in der Nachrichtenliste von Outlook 2010/2013. (#5268)
* Die Navigation in Tabellenblättern mit Diagrammen funktioniert nun korrekt. Dies betrifft z. B. den Wechsel zwischen Tabellenblättern mit Strg+Seite Auf/Ab. (#5336)
* Verbesserungen im Erscheinungsbild. Dies betrifft Schalter in einer Warnung, die beim Abwerten auf eine frühere NVDA-Version angezeigt wurde. (#5325)
* In Windows 8 und neuer startet NVDA nun wesentlich früher, wenn es so konfiguriert wird, dass es nach der Anmeldung ausgeführt wird. (#308)
 * Wenn die Option zum Start nach der Anmeldung mit einer vorherigen Version aktiviert wurde, müssen Sie sie aus- und wieder einschalten, damit die Änderungen wirksam werden. Folgen Sie dieser Anleitung:
  1. Öffnen Sie die allgemeinen Einstellungen.
  1. Deaktivieren Sie die Option "NVDA automatisch nach der Anmeldung starten".
  1. Betätigen Sie den Schalter "OK".
  1. Öffnen Sie die Allgemeinen Einstellungen erneut.
  1. Aktivieren Sie die Option "NVDA automatisch nach der Anmeldung starten".
  1. Betätigen Sie den Schalter "OK".
* Leistungsverbesserungen der UIA einschließlich Windows-Explorer und Task-Manager. (#5293)
* NVDA schaltet nun korrekt in den Fokusmodus um, wenn Sie sich mit Tab auf schreibgeschützte Aria-Elemente bewegen. Dies betrifft Firefox und andere Gecko-Anwendungen. (#5118)
* Wenn Sie mit einem Touchscreen arbeiten, zeigt NVDA nun korrekterweise "kein voriges Objekt" an, wenn sie vom ersten objekt auf dem Bildschirm aus nach links streichen.
* Problem behoben, wenn Sie im Dialogfeld "Einstellungen" -> "Eingaben" mehrere Wörter in das Suchfeld eingeben. (#5426)
* NVDA wird nun nicht mehr abstürzen, wenn Sie eine Humanware bi/b-Braillezeile über usb erneut anschließen. (#5406)
* In languages with conjunct characters, character descriptions now work as expected for upper case English characters. (#5375) (en)
* Beim Aufruf des Startmenüs von Windows 10 sollte NVDA nun nicht mehr abstürzen. (#5417)
* In Skype für Desktop werden Benachrichtigungen, welche angezeigt werden, bevor die vorangegangenene Benachrichtigung verschwindet, nun ausgegeben. (#4841, #5405)
* Benachrichtigungen werden in Skype für Desktop7.12 und neuer richtig ausgegeben. (#5405)
* NVDA behandelt nun das Schließen von Kontextmenüs in Anwendungen wie Jarte korrekt. (#5302)
* In Windows 7 und neuer werden Farben in Anwendungen wie Wordpad richtig ausgegeben. (#5352)
* Wenn Sie in Microsoft PowerPoint während der Bearbeitung von Text die Eingabetaste drücken, wird automatisch hinzugefügter Text (wie z. B. Aufzählungen oder Numerierungen) ausgegeben. (#5360)

## 2015.3

Schwerpunkte dieser Version sind anfängliche Unterstützung von Windows 10, die Möglichkeit Schnellnavigationstasten des Lesemodus zu deaktivieren (sinnvoll in bestimmten Internet-Anwendungen), Verbesserungen für den Internet Explorer sowie die Behebung von Fehlern, die beim schreiben in bestimmten Programmen zu verfälschtem Text geführt haben, wenn eine Braillezeile in Betrieb war.

### Neue Features

* In Eingabefeldern in Internet Explorer und anderen MSHTML-Dokumenten werden Rechtschreibfehler korrekt erkannt. (#4174)
* Verbesserte Erkennung von mathematischen Unicode-Sonderzeichen. (#3805)
* Suchvorschläge im Startbildschirm von Windows 10 werden automatisch ausgegeben. (#5049)
* Unterstützung der Braillezeillen EcoBraille 20, EcoBraille 40, EcoBraille 80 und EcoBraille Plus. (#4078)
* Im Lesemodus können Sie nun die Schnellnavigation mittels NVDA+Umschalt+Leertaste ein- und ausschalten. Bei ausgeschalteter Schnellnavigation werden Buchstaben an die aktive Anwendung weitergereicht. Dies ist in einigen Internet-Anwendungen wie GMail, Twitter und Facebook hilfreich. (#3203)
* Neue Braille-Übersetzungstabellen: Finnisch 6-Punkt, Irische Vollschrift, Irische Kurzschrift, Koreanische Vollschrift (2006), Koreanische Kurzschrift (2006). (#5137, #5074, #5097)
* Die Qwertz-Tastatur der Braillezeile BRAILLEX Live Plus von Papenmeier wird nun unterstützt. (#5181)
* Experimentelle Unterstützung für den Web-Browser Microsoft Edge sowie dessen Unterbau in Windows 10. (#5212)
* Neue Sprache: Kanadisch.

### Änderungen

* Der Braille-Übersetzter wurde auf Version 2.6.3 aktualisiert. (#5137)
* Wenn Sie versuchen, eine ältere NVDA-Version über eine aktuelle Version zu installieren wird eine Warnung angezeigt. Dies wird nicht empfohlen. NVDA sollte vollständig deinstalliert werden, bevor Sie eine ältere Version installieren. (#5037)

### Fehlerbehebungen

* Wenn Sie die Schnellnavigationstasten verwenden, werden Listeneinträge ignoriert, die zu Gestaltungszwecken eingefügt wurden. (#4204)
* In Firefox erstellt NVDA keine Beschreibungen mehr für ARIA-Registerkarten, die den gesamten Inhalt der Registerkarte enthalten. (#4638)
* Wenn Sie im Internet Explorer oder anderen MSHTML-Elementen in einen Abschnitt, einen Artikel oder einen Dialog navigieren, wird nicht mehr der gesamte Inhalt als Name angezeigt. (#5021, #5025)
* Wenn Sie eine Braillezeile von Baum, Humanware oder APH verwenden, funktioniert die Brailletastatur wieder, nachdem Sie andere Tasten an der Braillezeile verwendet haben. (#3541)
* Wenn Sie in Windows 10 mittels Alt+Tab bzw. Alt+Umschalt+Tab zwischen Anwendungen wechseln, werden keine überflüssigenInformationen angesagt. (#5116)
* Wenn Sie bestimmte Anwendungen wie Microsoft Outlook mit einer Braillezeile verwenden, wird diese nun nicht mehr verstümmelt dargestellt. (#2953)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden nun sich ändernde Elemente korrekterweise fokussiert. (#5040)
* In Microsoft Word wird nun die Anzeige auf der Braillezeile korrekt aktualisiert, wenn Sie die Schnellnavigation verwenden. (#4968)
* Beim ausgeben der Textformatierung in Braille werden keine überflüssigen Leerzeichen mehr angezeigt. (#5043)
* Wenn Sie den Fokus von einer Anwendung nehmen, die langsam reagiert, sollte NVDA nun in den meisten Fällen schneller reagieren. (#3831)
* Benachrichtigungen in Windows 10 werden nun wie erwartet ausgegeben. (#5136)
* Bestimmte UIA-Kombinationsfelder werden nun korrekt ausgegeben. Dies funktionierte zuvor nicht.
* Im Lesemodus verhält sich NVDA beim Navigieren wie erwartet, wenn Sie mit Umschalt+)Tab in einem Rahmen navigieren. (#5227)
* Der Sperrbildschirm von Windows 10 kann nun mittels Touchscreen erkundet und geschlossen werden. (#5220)
* Wenn Sie in Windows 7 oder neuer Text in Eingabefelder von z. B. WordPad oder Skype eingeben, während Sie eine Braillezeile verwenden, wird die Eingabe nicht mehr verfälscht dargestellt. (#4291)
* Im Sperrbildschirm von Windows 10 ist es nicht mehr möglich mittels des NVDA-Cursors auf laufende Anwendungen zuzugreifen oder die Konfiguration von NVDA zu ändern sowie die Zwischenablage auszulesen. (#5269)

### Änderungen für Entwickler

* Nun können auch Tastenanschläge von Tastaturen verarbeitet werden, die nicht vom Betriebssystem erkannt werden (wie z. B. Tastaturen von Braillezeilen). Verwenden Sie hierzu die neue Funktion keyboardHandler.injectRawKeyboardInput. (#4576)
* Mit der neuen Funktion "eventHandler.requestEvents" können nun Ereignisse abgearbeitet werden, die standardmäßig blockiert werden Hierzu zählen Ereignisse von bestimmten Steuerelementen oder Ereignisse, die im Hintergrund ausgelöst werden. (#3831)
* Anstelle eines einfachen Attributs für i18name enthält synthDriverHandler.SynthSetting nun sowohl displayNameWithAccelerator als auch displayName-Attribute. Hiermit wird verhindert, dass die Namen von Einstellungen im Sprachausgaben-Einstellungsring in einigen Sprachen mitsamt ihren hervorgehobenen Buchstaben angesagt werden (z. B. &Stimme, Ton&höhe, &Lautstärke, etc.).
 * Aus Gründen der Abwärtskompatibilität ist "displayname" optional und wird von "displaynamewithaccelerator" abgeleitet. Wenn Sie jedoch planen, eine Einstellung sowohl in den Stimmen-Einstellungen als auch im Sprachausgaben-Einstellungsring anzubieten, sollten Sie beide Attribute verwenden.
 * Das Attribut i18name ist veraltet und wird in einer der nächsten Versionen entfernt.

## 2015.2

Schwerpunkte dieser Version sind: Diagramme können in Microsoft Excel gelesen werden, Unterstützung für das Lesen und interaktive navigieren in mathematischem Text.

### Neue Features

* In Microsoft Word und Outlook kann man nun mittels Alt+Pfeiltaste nach oben bzw. nach unten Satzweise rück- bzw. vorwärts springen. (#3288)
* Neue Braillezeichensätze für mehrere indische Sprachen. (#4778)
* NVDA meldet in Excel überstehende oder abgeschnittene Zelleninhalte. (#3040)
* In Microsoft Excel können Sie sich mit Hilfe der Elementliste (NVDA+F7) eine Liste aller Formeln, Diagramme oder Kommentare anzeigen lassen. (#1987)
* Diagramme können nun in Microsoft Excel ausgelesen werden. Wählen Sie das Diagramm mit Hilfe der Elementliste (NVDA+F7) aus und bewegen Sie sich anschließend mit den Pfeiltasten zwischen den Datenpunkten. (#1987)
* Mit Hilfe von Mathplayer von Design Science kann NVDA in Webbrowsern, in Microsoft Word und in PowerPoint innerhalb mathematischer Inhalte navigieren. Siehe das kapitel "auslesen mathematischer Inhalte" für weitere informationen. (#4673)
* Im Dialogfeld "Eingaben" können Sie nun Tastenkombinationen, Tastenbefehle, Etc. aller NVDA-Einstellungen sowie Einstellungen zur Dokument-Formatierung zuweisen. (#4898)

### Änderungen

* In den Einstellungen zu Dokument-Formatierungen wurden die Tastenkürzel für die Ausgaben von Listen, Links, Zeilennummern und Schriftartennamen geändert. (#4650)
* In den Maus-Einstellungen von NVDA wurden Tastenkürzel für Audiokoordinaten bei Mausbewegungen wiedergeben sowie Lautstärke der Audiokoordinaten durch Helligkeit kontrollieren hinzugefügt. (#4916)
* Die Ausgabe von Farbnamen wurde verbessert. (#4984)
* Der Braille-Übersetzer LibLouis wurde auf Version 2.6.2 aktualisiert. (#4777)

### Fehlerbehebungen

* Zeichenbeschreibungen für zusammengesetzte Zeichen werden nun für bestimmte indische Sprachen korrekt behandelt. (#4582)
* Wenn die Option "Beim Sprechen von Zeichen und Symbolen die Sprache der Stimme berücksichtigen" in den Stimmen-Einstellungen aktiviert ist, wird beim bearbeiten der Aussprache von Symbolen und Sonderzeichen die korrekte Sprache verwendet. Außerdem wird die verwendete Sprache im Dialogtitel angezeigt. (#4930)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden eingegebene Zeichen nun korrekt ausgegeben. Dies betrifft deaktivierte Kombinationsfelder wie z. B. das Suchfeld auf der Google-Startseite. (#4976)
* Bei der Auswahl von Farben in Microsoft office werden Farbnamen ausgegeben. (#3045)
* Die Brailleausgabe in Dänisch funktioniert wieder. (#4986)
* In PowerPoint-Präsentationen können Sie mit Seite Auf und Seite Ab wieder zwischen den Folien wechseln. (#4850)
* In Skype für Desktops 7.2 oder neuer wird korrekt angegeben, wenn jemand in einer Konversation tippt. Außerdem wurde ein Fehler beim Verlassen einer Konversation behoben. (#4972)
* Problem beim Eingeben bestimmter Sonderzeichen (z. B. Klammern) in das Filter-Suchfeld des Eingaben-Dialogs behoben. (#5060)
* In Internet Explorer und anderen MSHTML-Steuerelementen berücksichtigt die Schnellnavigation über (Umschalt+)G auch Elemente, die aus Gründen der Zugänglichkeit per Aria als Grafik gekennzeichnet wurden. (#5062)

### Änderungen für Entwickler

* brailleInput.handler.sendChars(mychar) filtert keine Zeichen mehr aus, wenn das vorherige Zeichen gleich war. Dies wird erreicht in dem überprüft wird, ob die vorangegangene Taste richtig losgelassen wurde. (#4139)
* Wenn Sie in einem Skript einen neuen Arbeitsmodus für Touchscreens einführen, werden nun die namen der Arbeitsmodi in "touchHandler.touchModeLabels" berücksichtigt. (#4699)
* NVDA-Erweiterungen können nun ihre eigene Darstellung für mathematische Formeln implementieren. Siehe hierzu das paket MathPres für weitere Informationen. (#4509)
* Neue Befehle zum Steuern von Tonhöhe, Sprachgeschwindigkeit und lautstärke. Siehe hierzu BreakCommand, PitchCommand, VolumeCommand und RateCommand im Modul speech. (#4674)
 * Mit der Methode speech.PhonemeCommand können Sie außerdem die Aussprache beeinflussen; momentan werden noch sehr wenige Phoneme unterstützt.

## 2015.1

Schwerpunkte dieser Version sind: LeseModus für Microsoft Word- und Outlook-Dokumente, wesentliche Verbesserungen für die Unterstützung von Skype für Desktop sowie bedeutende Fehlerbehebungen für Internet Explorer

### Neue Features

* Im Dialogfeld "Aussprache von Symbolen und Sonderzeichen" können Sie nun neue Symbole hinzufügen. (#4354)
* Im Dialogfeld "Eingaben" können Sie über das Eingabefeld "Filtern nach" nur diejenigen Eingaben anzeigen, die in ihrer Beschreibung bestimmte Wörter enthalten. (#4458)
* In Mintty gibt NVDA nun neuen Text aus. (#4588)
* Im Suchdialog des Lesemodus gibt es ein Kontrollkästchen, mit dem Sie eine Suche unter Berücksichtigung der Groß-/Kleinschreibung durchführen können. (#4584)
* In Microsoft Word kann nun mittels NVDA+Leertaste der Lesemodus verwendet werden, um mit Hilfe von Schnellnavigationstasten im Dokument zu navigieren. Die Elementliste ist ebenfalls verfügbar. (#2975)
* Das Lesen von HTML-Nachrichten in Outlook 2007 und neuer wurde verbessert, in dem der Lesemodus automatisch für diese Nachrichten aktiviert wird. Sollte dies in seltenen Fällen nicht geschehen, können Sie den Lesemodus mittels NVDA+Leertaste aktivieren. (#2975)
* In Microsoft Word werden Spaltenüberschriften automatisch gelesen, wenn sie in den Tabelleneigenschaften als solche gekennzeichnet wurden. (#4510)
 * Wenn die Tabelle jedoch verbundene Zeilen enthält, funktioniert dies nicht automatisch. Sie können die Spaltenüberschrift manuell mit NVDA setzen. Verwenden Sie hierfür die Tastenkombination NVDA+Umschalt+c.
* In der Desktop-Version von Skype werden Benachrichtigungen angezeigt. (#4741)
* In Skype können Sie die letzten Nachrichten mit NVDA+Strg+1 bis NVDA+Strg+0 anzeigen NVDA+Strg+1 zeigt beispielsweise die letzte eingegebene Nachricht an. (#3210)
* In einer Skype-Konversation wird nun angesagt, wenn jemand tippt. (#3506)
* Bei der Installation von NVDA kann die Anzeige von Meldungen unterdrückt werden. Verwenden Sie hierfür die Kommandozeilenoption --install-silent. (#4206)
* Unterstützung für Papenmeier BRAILLEX Live 20, BRAILLEX Live und BRAILLEX Live Plus. (#4614)

### Änderungen

* Im Dialogfeld für die Dokument-Formatierungen besitzt die Option "Rechtschreibfehler ansagen" nun das Tastenkürzel Alt+R. (#793)
* NVDA verwendet die Sprache der Sprachausgabe bzw. der Stimme, um Namen von Symbolen und Sonderzeichen zu lesen; unabhängig davon, ob "Sprache automatisch wechseln" aktiviert ist. Um dieses Verhalten abzuschalten, sodass NVDA wieder die Standard-Sprache verwendet, deaktivieren Sie in den Stimmen-Einstellungen die neue Option "Beim Vorlesen von Symbolen und Sonderzeichen die Sprache der Stimme berücksichtigen". (#4210)
* Die Unterstützung für Newfon wurde entfernt; Newfon ist jetzt als NVDA-Erweiterung verfügbar. (#3184)
* Skype 7 oder neuer wird nun benötigt; ältere Skype-Versionen werden nicht mehr unterstützt. (#4218)
* Das Herunterladen von NVDA-Aktualisierungen ist nun sicherer. Es erfolgt nun über https. Zudem wird die Datei nach dem Herunterladen mit Hilfe ihres Hash-Wertes auf Korrektheit geprüft. (#4716)
* eSpeak auf Version 1.48.04 aktualisiert. (#4325)

### Fehlerbehebungen

* Wenn in Microsoft Excel die Reihen- oder Spaltenüberschriften aus verbundenen Zellen bestehen, werden diese richtig erkannt. Wenn beispielsweise A1 und A2 verbunden sind, wird in b2 der Inhalt aus a1 und b1 ausgegeben, anstatt die Überschrift zu ignorieren. (#4617)
* Beim Bearbeiten von Text in Eingabefeldern in Microsoft PowerPoint 2003 wird der Inhalt von jeder Zeile richtig ausgegeben. Zuvor wurden Zeilenumbrüche falsch verarbeitet. (#4619)
* Alle NVDA-Dialoge werden zentriert angezeigt, um die Lesbarkeit zu verbessern. (#3148)
* Wenn Sie in Skype eine Nachricht eingeben, um einen Kontakt zu einem Chat einzuladen, funktioniert das Eingeben der Nachricht nun korrekt. (#3661)
* Die Navigation in Baumstrukturen in der Eclipse IDE funktioniert nun korrekt. (#4586)
* Wenn Sie Tastenkombinationen verwenden, um einen Rechtschreibfehler in Microsoft Word zu korrigieren oder zu ignorieren, wird automatisch der nächste Rechtschreibfehler ausgegeben. (#1938)
* In Balabolka-Dokumenten oder dem Terminalfenster von Tera Term Pro funktioniert das Lesen von Text korrekt. (#4229)
* Wenn Sie im Internet Explorer oder anderen MSHTML-Dokumenten innerhalb eines Rahmens Text bearbeitet haben, wird der Fokus korrekt in das Dokument gesetzt, wenn Sie die Bearbeitung abgeschlossen haben. Dies betrifft vor allem Text in ostasiatischen Sprachen wie Koreanisch. (#4045)
* Wenn Sie im Dialogfeld "Eingaben" beim Auswählen eines Tastaturschemas beim Hinzufügen einer Eingabemethode im Tastaturschemen-Menü die Escape-Taste drücken, wird jetzt - wie erwartet - das Menü geschlossen; zuvor wurde der gesamte Dialog geschlossen. (#3617)
* Beim Entfernen einer Erweiterung wird das Verzeichnis der Erweiterung korrekt gelöscht. Zuvor musste NVDA hierfür zwei Mal neu gestartet werden. (#3461)
* Schwerwiegende Probleme mit Skype 7 für Desktop wurden behoben. (#4218)
* Wenn Sie eine Nachricht in Skype schreiben, wird sie nicht mehr doppelt vorgelesen. (#3616)
* In Skype sollte NVDA nicht mehr fälschlicherweise ganze Konversationen lesen. (#4644)
* Problem behoben, wonach NVDA beim Lesen des Datums und der Uhrzeit manchmal die Länder-Einstellungen des Benutzers nicht berücksichtigt hat. (#2987)
* Im Lesemodus werden keine irreführenden Alternativtexte für Grafiken mehr angezeigt. dies betrifft u. a. Base64-kodierte Grafiken in Google Groups. (#4793)
* NVDA sollte nun nicht mehr hängen bleiben, sobald eine Metro-App durch Windows 8 stillgelegt wird. (#4572)
* In Firefox wird das ARIA-Attribut Atomic in Live-Regionen berücksichtigt, wenn sich das Atomic-Element ändert. Zuvor wirkte sich eine Änderung des Atomic-Attributes nur auf enthaltene Elemente aus. (#4794)
* Aktualisierungen von Dokumenten innerhalb von ARIA-Anwendungen werden in Internet Explorer und anderen MSHTML-Dokumenten berücksichtigt. (#4798)
* Wenn sich Text innerhalb von ARIA-Elementen in Internet Explorer und MSHTML-Steuerelementen ändert, wird nur der neu hinzugekommene/geänderte Text ausgegeben. (#4800)
* Das Attribut ARIA-LabeledBy wird korrekt verarbeitet. (#4575)
* Wird in Microsoft Outlook 2013 die Rechtschreibung geprüft, so werden falsch geschriebene Wörter angesagt. (#4848)
* Im Internet Explorer und anderen MSHTML-Elementen werden Elemente, welche durch visibility:hidden versteckt wurden, nicht mehr fälschlicherweise im Lesemodus ausgegeben. (#4839, #3776)
* Im Internet Explorer und anderen MSHTML-Elementen werden Beschriftungen von Formularfeldern nicht mehr durch die Titelbezeichnung verdeckt. (#4491)
* Im Internet Explorer und anderen MSHTML-Elementen ignoriert NVDA das fokusieren von Elementen nicht mehr, wenn dies durch das Atribut aria-activedescendant erfolgte. (#4667)

### Änderungen für Entwickler

* wxPython auf 3.0.2.0 aktualisiert. (#3763)
* Python auf Version 2.7.9 aktualisiert. (#4715)
* Wenn Sie eine Erweiterung entfernen oder aktualisieren, die während der Installation das Modul speechDictHandler importiert hat, wird NVDA nicht mehr abstürzen. (#4496)

## 2014.4

### Neue Features

* Neue Sprachen: Spanisch (Kolumbien) und Pandschabi.
* Sie können NVDA nun auch über den Dialogfeld "Beenden" aus (wahlweise mit deaktivierten Erweiterungen) neu starten. (#4057)
 * Sie können NVDA auch mit deaktivierten Erweiterungen neu starten, indem Sie die Kommandozeilenoption --disable-addons verwenden.
* Sie können in Aussprache-Wörterbüchern angeben, dass ein bestimmtes Muster nur auf ein ganzes Wort passen soll. (#1704)

### Änderungen

* Wenn Sie mit dem Navigator in ein virtuelles Dokument wechseln, wird der Darstellungsmodus auf "Dokument" eingestellt. früher geschah dies nur, wenn Sie den Fokus bewegt haben. (#4369)
* Die Dialoge zum Auswählen von Sprachausgaben oder Braillezeilen werden alphabetisch sortiert; ausgenommen sind hierbei die Einträge "Keine Sprachausgabe" oder "Keine Braillezeile". Diese befinden sich stets an letzter Stelle in der Liste. (#2724)
* Libluis wurde auf Version 2.6.0 aktualisiert. (#4434, #3835)
* Wenn Sie im Lesemodus die Schnellnavigationstasten E und Umschalt+E drücken, werden nun auch bearbeitbare Kombinationsfelder berücksichtigt. Dies betrifft u. a. das Suchfeld in der neuesten Version der Google-Suche. (#4436)
* Wenn Sie mit der linken Maustaste auf das NVDA-Symbol im Infobereich klicken, wird nun das NVDA-Menü geöffnet. (#4459)

### Fehlerbehebungen

* Wenn Sie mit Alt+Tab in ein bereits geöffnetes virtuelles Dokument wechseln, wird der NVDA-Cursor korrekt auf dem virtuellen Cursor und nicht wie bisher auf dem fokusierten Objekt (z. B. einem nahe gelegenen Link) positioniert. (#4369)
* Der NVDA-Cursor verfolgt nun den virtuellen Cursor richtig in PowerPoint-Präsentationen. (#4370)
* In Mozilla Firefox und anderen Gecko-Basierten Browsernwird neuer Inhalt in Live-Regionen korrekt angezeigt. (#4169).
* Im Internet Explorer und anderen MSHTML-Elementen verhindern verschachtelte Rahmen nicht mehr das Navigieren in außerhalb liegende Rahmen. (#4418)
* NVDA stürzt nun nicht mehr ab, wenn es mit einer Handytech-Braillezeile verwendet wird. (#3709)
* Problem in Windows Vista behoben, wonach NVDA mit dem Dialogfeld "Einsprungpunkt nicht gefunden" abstürzte, wenn man es über die Desktop-Verknüpfung oder über die Tastenkombination gestartet hat. (#4235)
* Probleme mit Eingabefeldern in einigen Eclipse-Versionen behoben. (#3872)
* In Microsoft Outlook 2010 wird der System-Cursor im Eingabefeld "Ort" in Besprechungs- und Terminanfragen ordnungsgemäß bewegt. (#4126)
* Innerhalb einer Live-Region wird der Inhalt, der mit "aria-live=off" gekennzeichnet ist, korrekterweise ignoriert. (#4405)
* Bei Statuszeilen, die einen Namen besitzen, wird der Name vom Text abgetrennt. (#4430)
* Wenn die Option "Eingegebene Wörter ansagen" aktiviert ist, werden in Passwort-Eingabefeldern nicht mehr länger Sterne angesagt, wenn Sie ein neues Wort beginnen. (#4402)
* In der Nachrichtenliste von Microsoft Outlook werden Einträge nicht mehr unnötigerweise als Dateneintrag bezeichnet. (#4439)
* Im Code-Editor von Eclipse wird beim Markieren von Text nicht mehr der gesamte markierte Text ausgegeben, wenn sich die Markierung ändert. (#2314)
* Diverse Versionen von Eclipse (wie z. B. die Entwicklungsumgebung für Android-Anwendungen) werden korrekt als Eclipse erkannt. (#4360, #4454)
* Die Mausverfolgung für Internet Explorer sowie viele weitere Anwendungen unter Windows 8 wurden verbessert. Dies betrifft insbesondere die Verwendung höherer Bildschirmauflösungen. (#3494)
* Bei Verwendung der Mausverfolgung im Internet Explorer und anderen mshtml-Dokumenten werden nun mehr Schalter erkannt. (#4173)
* Bei Verwendung einer Papenmeier-Braillezeile mit Brxcom funktionieren die Tasten auf der Braillezeile nun wie erwartet. (#4614)

### Änderungen für Entwickler

* Für Programme, die mehrere unterschiedliche Anwendungen bereitstellen können (wie z. B. javaw.exe) können nun Anwendungsmodule für einzelne Anwendungen geschrieben werden. (#4360)
 * Siehe hierzu die Code-Dokumentation von appModuleHandler.AppModule für weitere Informationen.
 * Unterstützung für javaw.exe ist bereits integriert.

## 2014.3

### Neue Features

* Die Klänge beim Starten und Beenden von NVDA können mit einer neuen Option in den allgemeinen Einstellungen ein- und ausgeschaltet werden. (#834)
* Im Dialogfeld "Erweiterungen verwalten" können Sie eine Hilfeseite zu einer Erweiterung aufrufen, sofern es dies unterstützt. (#2694)
* Unterstützung für den Kalender in Outlook 2007 und neuer (#2943):
 * Wenn Sie sich mit den Pfeiltasten im Kalender bewegen, wird die aktuelle Uhrzeit ausgegeben
 * Es wird benachrichtigt, ob der gewählte Zeitpunkt mit einem Termin kollidiert
 * Der gewählte Termin wird ausgegeben, wenn Sie Tab drücken
 * Das Datum wird nur noch ausgegeben, wenn sich der neu gewählte Termin/Zeitpunkt auf einen anderen Tag bezieht
* Verbesserte Unterstützung für den Posteingang und andere Nachrichtenlisten in Outlook 2010 und neuer. (#3834)
 * Sie können die Anzeige der Spaltenüberschriften (Absender, Betreff, etc.) unterdrücken, indem Sie die Option "Spalten- und Reihenüberschriften von Tabellen ansagen" in den Einstellungen für Dokument-Formatierungen deaktivieren.
 * Sie können die Tabellennavigationsbefehle (Alt+Strg+Pfeiltasten) verwenden, um zwischen den Spalten zu navigieren
* Microsoft Word: Wenn eine eingebundene Grafik keinen Alternativtext besitzt, wird stattdessen der Titel angezeigt, sofern vorhanden. (#4193)
* Microsoft Word: Sie können die Einrückung eines Absatzes automatisch ausgeben lassen, indem Sie die Option "Absatzeinrückungen anzeigen" in den Einstellungen für Dokument-Formatierungen aktivieren. Des weiteren werden Absatzeinrückungen auch mit dem Befehl Dokument-Formatierung ansagen (NVDA+F) ausgegeben. (#4165).
* Wenn Sie in Eingabefeldern oder in Dokumenten die Eingabetaste drücken, wird automatisch eingefügter Text (Tab-, Aufzählungszeichen, Numerierungen) automatisch ausgegeben. (#4185)
* Microsoft Word: Sie können NVDA+Alt+C drücken, um sich den Kommentar in einem Word-Dokument ausgeben zu lassen. (#3528)
* Verbessertes automatisches Anzeigen von Reihen- und Spaltenüberschriften in Microsoft Excel (#3568):
 * Es werden (JAWS-kompatible) definierte Namen verwendet, um Reihen- und Spaltenüberschriften zu identifizieren
 * Die Befehle zum Setzen von Spalten- und Reihenbeschriftungen (NVDA+Umschalt+C und NVDA+Umschalt+R) speichern die Spalten- und Reihenbeschriftungen im Excel-Arbeitsblatt, sodass diese nach einem Neustart von NVDA oder Microsoft Excel wieder zur Verfügung stehen. Solche Reihen-/Spaltenüberschriften sollten von allen Bildschirmlesern ausgewertet werden können, die definierte Namen unterstützen
 * Die Befehle können außerdem mehrmals in einem Arbeitsblatt verwendet werden, um verschiedene Überschriften für unterschiedliche Regionen eines Arbeitsblattes zu definieren.
* Unterstützung für die Anzeige von Reihen- und Spaltenüberschriften in Microsoft Word (#3110):
 * Es werden (JAWS-kompatible) Word-Lesezeichen verwendet, um Reihen- und Spaltenüberschriften zu identifizieren
 * Wenn Sie sich in der ersten Zeile/Spalte einer Tabelle befinden, können Sie diese mit NVDA+Umschalt+C und NVDA+Umschalt+R als Spalten-/Zeilenbeschriftung festlegen. Diese Beschriftungen werden im Word-Dokument gespeichert und stehen allen Bildschirmlesern zur Verfügung, die derartige Lesezeichen unterstützen.
* Microsoft Word: Wenn Sie Tab drücken, wird der Abstand zum linken Seitenrand ausgegeben. (#1353)
* Für die meisten Befehle, die die Formatierungen in einem Word-Dokument verändern (Fett, Kursiv, unterstrichen; Gliederungsebenen, etc.) meldet NVDA die Änderung der Formatierung per Sprache und Braille. (#1353)
* Wenn in einem Arbeitsblatt von Microsoft Excel die aktuelle Zelle einen Kommentar besitzt, können Sie diesen über die Tastenkombination NVDA+Alt+C sich anzeigen lassen. (#2920)
* Wenn Sie in Microsoft Excel den Modus zum Bearbeiten von Kommentaren mit der Tastenkombination Umschalt+F2 einschalten, wird ein NVDA-eigenes Dialogfeld zur Eingabe eines Kommentars angezeigt. (#2920)
* Microsoft Excel: Für etliche Tastenkombinationen, die sich auf das Verschieben von Markierungen beziehen, wurde die Ausgabe in Sprache und Braille verbessert. (#4211)
 * Vertikales seitenweises Verschieben (Seite Auf und Seite Ab)
 * Horizontales seitenweises Verschieben (Alt+Seite Auf und Alt+Seite Ab)
 * Erweitern von Markierungen (die obigen Tastenkombinationen mit der Umschalt-Taste).
 * Markieren der aktuellen Region (Strg+Umschalt+8).
* Microsoft Excel: Wenn die Ansage der Ausrichtung in den Einstellungen für Dokument-Formatierungen aktiviert ist, wird die vertikale und horizontale Ausrichtung der aktuellen Zelle automatisch ausgegeben. Ausgabe derselben mittels Formatierung ausgeben (NVDA+F). (#4212)
* Microsoft Excel: Das Layout einer -Zelle wird ausgegeben, wenn Sie NVDA+F drücken. Dies geschieht automatisch, wenn die Option "Layout ansagen" in den Einstellungen für Dokument-Formatierungen aktiviert ist. (#4213)
* Microsoft PowerPoint: Wenn Sie ein Objekt über eine Folie mit Hilfe der Pfeiltasten bewegen, wird die neue Position ausgegeben. (#4214)
 * Der Abstand zwischen dem Objekt und jedem Rand der Folie wird ausgegeben.
 * Sofern das Objekt ein anderes Objekt überlagert oder überlagert wird, wird die Überlagerung ausgegeben.
 * Verwenden Sie den Befehl "Position anzeigen" (NVDA+Nummernblock Entf), um diese Informationen abzurufen, ohne das objekt zu bewegen.
 * Wenn Sie ein Objekt auf einer Folie auswählen, werden Überlagerungen mit anderen Objekten gemeldet.
* Der Befehl zum Anzeigen der Dimensionen eines Objekts reagiert in einigen Situationen kontextsensitiver. (#4219)
 * In Eingabefeldern und im Lesemodus wird die Cursorposition relativ zum Feldinhalt und in Form von Bildschirmkoordinaten gemeldet.
 * Bei PowerPoint-Objekten wird die Position des Objekts auf der Folie sowie evtl. vorhandene Überlagerungen gemeldet.
 * Wenn Sie die Tastenkombination zweimal drücken, wird die Position dem alten Verhalten entsprechend gemeldet.
* Neue Sprache: Katalanisch.

### Änderungen

* Der Braille-Übersetzer LibLouis wurde auf 2.5.4 aktualisiert. (#4103)

### Fehlerbehebungen

* In Chrome und Chrome-basierten Browsern werden hervorgehobene Dialogtexte nicht mehr doppelt angesagt. (#4066)
* Im Lesemodus in Mozilla-Anwendungen werden Schalter, etc. zuverlässiger mit der Eingabetaste gedrückt. Zuvor wurde ein Schalter nicht bzw. ein anderer Schalter betätigt.dies betrifft z. B. die Schalter oben auf der Facebook-Seite. (#4106)
* Beim Navigieren in Itunes wird nutzlose Information ausgefiltert. (#4128)
* Das Navigieren auf den nächsten Eintrag in Listen wie der Musik-Liste in Itunes funktioniert korrekt, wenn Sie die Objektnavigation verwenden. (#4129)
* Im Internet Explorer werden HTML-Elemente, die Überschriften enthalten, in die Schnellnavigation und in die Elementliste einbezogen. (#4140)
* Das Verfolgen von Links auf der selben Seite funktioniert nun im Internet Explorer korrekt. (#4134)
* In Microsoft Outlook 2010 und neuer wurde die Zugänglichkeit für einige dialoge wie die Einrichtung eines Mail-Kontos verbessert. (#4090, #4091, #4095)
* In Outlook 2010 werden in der Befehls-Symbolleiste in einigen Dialogen keine nutzlosen Informationen mehr angezeigt. (#4096, #3407)
* Wenn Sie in Microsoft Word auf eine leere Zelle in einer Tabelle navigieren, wird nicht mehr fälschlicherweise das Verlassen der Tabelle gemeldet. (#4151)
* Microsoft Word, das erste Zeichen jenseits einer Tabelle wird nun nicht mehr fälschlicherweise in die Tabelle verlegt. (#4152)
* Im Dialogfeld für die Rechtschreibprüfung in Microsoft Word wird nun das falsch geschriebene Wort korrekt angezeigt, anstatt das erste fett gedruckte Wort anzuzeigen. (#3431)
* Lesemodus: Im Internet Explorer und anderen MSHTML-Dokumenten werden die Beschriftungen von Formularfeldern korrekt angezeigt, wenn Sie die Tab-Taste oder die Schnellnavigationstasten zur Navigation im Dokument verwenden. Dies betrifft vor allem Formularfelder, bei denen das HTML-Element Label zur Beschriftung verwendet wurde. (#4170)
* Die Existenz von Kommentaren wird in Microsoft Word zuverlässiger gemeldet. (#3528)
* Der Umgang mit Dialogfeldern in Microsoft Word, Microsoft Excel und Microsoft Outlook wurde verbessert, indem manche Container-Symbolleisten ignoriert werden, die für den Anwender nicht hilfreich sind. (#4198)
* Wenn Sie Microsoft Word oder Microsoft Excel öffnen, werden Aufgabenbereiche wie das Fenster zur Datei-Wiederherstellung oder der Zwischenablagen-Manager nicht mehr versehentlich in den Fokus genommen. (#4199)
* NVDA funktioniert nun ordnungsgemäß auf serbischen Windows-Systemen. (#4203)
* NVDA verhält sich nun korrekt, wenn Sie bei eingeschalteter Eingabehilfe die Taste für den Nummernblock drücken, um den Nummernblock ein- oder auszuschalten. (#4226)
* In Google Chrome wird der Titel des Dokuments gelesen, wenn Sie die Registerkarte wechseln. (#4222)
* In Google Chrome und Chrome-basierten Browsern wird die Adresse des Dokuments nicht mehr gelesen, wenn Sie das Dokument lesen. (#4223)
* Der Treiber für die Sprachausgaben "Keine Sprache" simuliert nun ein vollständiges "Alles Lesen", Dies ist insbesondere für automatisierte Tests nützlich. (#4225)
* Der Dialogfeld zum Bearbeiten von Signaturen in Outlook ist nun voll zugänglich (Incl. Formaterkennung und Cursor-Verfolgung). (#3833)
* Wenn Sie in Microsoft Word die letzte Zeile einer Tabellenzelle lesen, wird nicht mehr die gesamte Zelle gelesen. (#3421)
* In Microsoft Word wird nicht mehr das gesamte Inhaltsverzeichnis gelesen, wenn Sie die erste oder letzte Zeile in einem Inhaltsverzeichnis lesen. (#3421)
* Bei Wörtern während der Eingabe und in einigen anderen Fällen werden indische Wörter, die Vokalzeichen und Virama enthalten, nicht mehr fälschlicherweise zerteilt. (#4254)
* Numerische Eingabefelder in GoldWave werden korrekt verarbeitet. (#670)
* Wenn Sie sich in Microsoft Word absatzweise durch numerierte Listen oder Aufzählungslisten bewegen, müssen Sie die Tastenkonbinationen Strg+Pfeil nach oben/unten nicht mehr zweimal Drücken. (#3290)

### Änderungen für Entwickler

* Die Unterstützung für das Beilegen einer Dokumentation zu NVDA-Erweiterungen wurde vereinheitlicht. Sehen Sie sich den Abschnitt zu Dokumentation für Erweiterungen für weitere Informationen an. (#2694)
* Wenn Sie das Wörterbuch __gestures verwenden, um Skripte an Eingabemethoden zuzuweisen, können Sie als Namen für das Skript das Schlüsselword None angeben, um in einer Basisklasse die Zuweisung für eine Tastenkombination zu löschen. (#4240)
* Es ist nun möglich, die Tastenkombination zum Starten von NVDA zu ändern. In einigen Sprachräumen verursacht die Standard-Tastenkombination Probleme. (#2209)
 * Dies wird über Getext realisiert.
 * Bedenken Sie, dass Sie sowohl den Text für die Option zum Erstellen einer Desktop-Verknüpfung als auch die entsprechenden Passagen im Benutzerhandbuch aktualisieren müssen.

## 2014.2

### Neue Features

* Der markierte Text in Eingabefeldern wird korrekt erkannt, wenn der angezeigte Text (über die API DisplayModel) benutzt werden muss. (#770)
* In zugänglichen Java-Anwendungen werden Positionsinformationen (z. B. in Auswahlschaltern) korrekt angezeigt. (#3754)
* In zugänglichen Java-Anwendungen werden Tastenkombinationen korrekt erkannt. (#3881)
* Im Lesemodus werden Beschriftungen in Sprungmarken korrekt erkannt und in der Elementliste angezeigt. (#1195)
* Im Lesemodus werden benannte Regionen als Sprungmarken erkannt. (#3741)
* Im Internet Explorer werden Live-Regionen unterstützt. Dies erlaubt es Webentwicklern, bestimmte Teile einer Webseite automatisch von NVDA vorlesen zu lassen, sobald sie sich ändern. (#1846)

### Änderungen

* Wenn Sie ein Dialogfeld oder eine Anwendung beenden, der bzw. die sich innerhalb eines Webdokuments befindet, wird der Name und der Typ des Dokumentes nicht mehr angesagt. (#4069)

### Fehlerbehebungen

* In zugänglichen Java-Anwendungen wird das Systemmenü nicht mehr unterdrückt (#3882)
* Zeilenumbrüche werden nicht mehr unterdrückt, wenn Text aus der Bildschirmdarstellung kopiert wird. (#3900)
* Wenn die vereinfachte Darstellung aktiviert ist, werden Objekte ohne Standortinformationen und Beschriftung nicht mehr angezeigt. (#3839)
* Wenn NVDA-Meldungsfenster und -Dialoge erscheinen, wird die Sprache unterbrochen.
* Wenn ein Webentwickler aus Gründen der Barrierefreiheit die Attribute aria-label oder aria-labelledby verwendet hat, um die Beschriftung eines Links oder Schalters zu überschreiben, werden diese Beschriftungen korrekt angezeigt. (#1354)
* Wenn im Lesemodus im Internet Explorer ein Element als gestaltendes Element markiert wurde (indem "aria-presentation" verwendet wird), wird der enthaltene Text nicht mehr ignoriert. (#4031)
* Sie können nun wieder das Programm Unikey verwenden, um vietnamesische Sonderzeichen einzugeben. Deaktivieren Sie hierzu die neu hinzugekommene Option "Tastendrücke anderer Anwendungen verarbeiten" in den Tastatur-Einstellungen. (#4043)
* Im Lesemodus werden aktivierbare menüeinträge (mit und ohne Mehrfachauswahl) innerhalb von anklickbarem Text erkannt. (#4092)
* Wenn ein aktivierbarer Menü-Eintrag (mit oder ohne Mehrfachauswahl) den Fokus erhält, wird nicht mehr vom Fokus- in den Lesemodus gewechselt. (#4092)
* Wenn in Microsoft PowerPoint die wortweise Ansage aktiviert ist, werden gelöschte Zeichen nicht mehr als Teil eines eingegebenen Wortes angesagt. (#3231)
* In den Einstellungen von Microsoft Office 2010 werden Kombinationsfelder korrekt beschriftet. (#4056)
* Die Schnellnavigationsbefehle für Formularfelder und Schalter berücksichtigen in Mozilla-Anwendungen auch die Umschalter. (#4098)
* Hinweisdialoge werden in Mozilla-Anwendungen nicht mehr doppelt angesagt. (#3481)
* Wenn im Lesemodus eine Webseite automatisch aktualisiert wird, werden Sprungmarken und Container-Inhalte nicht doppelt vorgelesen, sobald darin navigiert wird (z. B. Twitter und Facebook). (#2199)
* Wenn Sie den Fokus von einer Anwendung wegschalten, die nicht mehr reagiert, wird sich NVDA zuverlässiger neu starten. (#3825)
* Wenn sich der System-Cursor in einem Eingabefeld befindet, das direkt auf den Bildschirm geschrieben wird, wird die Position des System-Cursors zuverlässiger aktualisiert, wenn Sie die Funktion "Alles Lesen" verwenden. (#4125)

## 2014.1

### Neue Features

* Unterstützung für Microsoft PowerPoint 2013. die geschützte ansicht wird nicht unterstützt. (#3578)
* Wenn Sie in Microsoft Word oder Excel das Dialogfeld zum Einfügen von Sonderzeichen verwenden, kann NVDA nun das ausgewählte Symbol erkennen. (#3538)
* In den Einstellungen zur Dokument-Formatierung können Sie nun festlegen, ob anklickbare Elemente als solche erkannt werden sollen. Diese Option ist standardmäßig aktiviert. Dies entspricht dem Verhalten älterer NVDA-Versionen. (#3556)
* Wenn Sie die Widcomm-Bluetoot-Software verwenden, werden nun auch Braillezeilen korrekt erkannt, die per Bluetooth verbunden sind. (#2418)
* Beim Bearbeiten von Text in PowerPoint werden Links als solche erkannt. (#3416)
* Um ARIA-Dialoge und -Anwendungen im Lesemodus anzuzeigen, können Sie mit NVDA+Leertaste in den Lesemodus wechseln, während Sie eine ARIA-Anwendung verwenden. (#2023)
* In Outlook Express / Windows Mail / Windows Live Mail wird die Existenz von Anhängen oder Kennzeichnungen von Nachrichten angezeigt. (#1594)
* Beim Navigieren innerhalb von Tabellen in zugänglichen Java-Anwendungen werden Reihen- und Spaltennummern sowie Reihen- und Spaltenüberschriften angezeigt. (#3756)

### Änderungen

* Die Befehle zum Umschalten von bzw. in den Bildschirmmodus wurden aus der Tastenbelegung für Papenmeier-Braillezeilen entfernt. Sie können im Dialogfeld "Einstellungen" -> "Eingaben" jedoch eine eigene Tastenkombination zuweisen. (#3652)
* NVDA benötigt nun mindestens VC Runtime Version 11. Das bedeutet, dass nun mindestens Windows XP SP2 oder Windows Server 2003 SP1 benötigt wird.
* In der Satzzeichen- und in der Symbolebene "Einige" werden die Zeichen Stern (*) und Plus (+) angesagt. (#3614)
* eSpeak auf Version 1.48.04 aktualisiert. Dadurch wurden etliche Fehler beseitigt. (#3842, #3739, #3860)

### Fehlerbehebungen

* Beim Navigieren durch und Markieren von Zellen in Microsoft Excel wird der markierte Zellenbereich korrekt erkannt, wenn Microsoft Excel langsam reagiert. (#3558)
* NVDA verhält sich erwartungsgemäß, wenn Sie ein Kombinationsfeld für eine Zelle über das Kontextmenü öffnen. (#3586)
* Im iTunes Store in iTunes 11 wird der Seiteninhalt aktualisiert, wenn Sie innerhalb des Stores einem Link folgen. (#3625)
* Im iTunes Store in iTunes 11 werden die Beschriftungen für die Schalter für Musikvorschau korrekt angezeigt. (#3638)
* Im Lesemodus in Google Chrome werden die Beschriftungen von Kontrollkästchen und Auswahlschaltern korrekt angezeigt. (#1562)
* In InstantBird wird beim Navigieren in der Kontaktliste keine nutzlose Information mehr angezeigt. (#2667)
* Im Lesemodus in Adobe Reader wird die Beschriftung von Schaltern richtig angezeigt, wenn sie durch Minihilfen überschrieben wird. (#3640)
* Im Adobe Reader werden nutzlose Grafiken, die als "mc-ref" beschriftet sind, nicht mehr angezeigt. (#3645)
* In Microsoft Excel werden nicht mehr fälschlicherweise alle Zellen in den Formatierungsinformationen als unterstrichen angezeigt. (#3669)
* Problem behoben, wonach bestimmte Unicode-Zeichen im Lesemodus die anzeige von Beschriftungen für Elemente verhindert haben. (#2963).
* Problem behoben, wonach die Eingabe Ostasiatischer Sonderzeichen in PUTTY fehlschlug (#3432)
* Wenn Sie in einem Dokument im Lesemodus navigieren, nachdem Sie das Vorlesen des Dokuments abgebrochen haben, wird nun nicht mehr fälschlicherweise das Ende eines Containerobjektes (z. B. einer Tabelle) gemeldet (#3688).
* Wenn Sie die Schnellnavigationstasten im Lesemodus verwenden, um das Vorlesen eines Dokumentes zu unterbrechen, während die Option "Navigation während Alles Lesen erlauben" aktiviert ist, wird das aktuelle Element an der neuen Position korrekt angesagt. (#3689)
* Die Navigationsbefehle zum Springen an den Anfang bzw. an das Ende eines Containerobjekts berücksichtigen jetzt die Option "Navigation während Alles Lesen erlauben" (#3675).
* Die Namen der Tastenbefehle werden nun im Dialogfeld "Einstellungen" -> "Eingaben" in übersetzter Form angezeigt. (#3624)
* NVDA wird keine Abstürze mehr verursachen, wenn Sie die Maus über die Dokumentfenster (TRichEdit) mancher Programme bewegen. Dies betrifft u. a. Jarte 5.1 und BRfácil. (#3693, #3603, #3581)
* ARIA-Elemente, die als Präsentation gekennzeichnet sind, werden nicht mehr angezeigt. (#3713)
* In Microsoft Word-Tabellen werden Spalten- und Reiheninformationen nun nicht mehr mehrfach in Braille angezeigt. (#3702)
* In Sprachen, in denen das Leerzeichen als Tausendertrennzeichen verwendet wird, werden Zahlen, die durch Leerzeichen getrennt sind, nicht mehr irrtümlich zusammengezogen (nützlich bei der Ansage von Tabellenzellen, die nur Zahlen enthalten). (#3698)
* Die Anzeige auf der Braillezeile wird nun korrekt aktualisiert, wenn Sie in Microsoft Word 2013 den System-Cursor bewegen. (#3784)
* Wenn Sie sich in Microsoft Word auf dem ersten Zeichen einer Überschrift befinden, wird die Kennzeichnung "Überschrift" (einschließlich der Ebene) in Braille angezeigt. (#3701)
* Ein Konfigurationsprofil, das beim Starten einer Anwendung per Trigger automatisch ausgewählt wird, wird nun deaktiviert, wenn die betreffende Anwendung beendet wird. (#3732)
* Asiatische Sonderzeichen werden nun korrekt angesagt und angezeigt, wenn Sie sie innerhalb von NVDA eingeben (z. B. im Suchdialog im Lesemodus). (#3726)
* Die Registerkarten im Optionsdialog von Outlook 2013 werden korrekt angezeigt. (#3826)
* Verbesserung der Unterstützung von ARIA-Live-Regionen in Mozilla-Anwendungen:
 * Automatische Aktualisierung von Live-Regionen. (#2640)
 * Alternative Texte (z. B. Alt-Attribute) werden verwendet, sofern keine anderweitige Beschriftung vorhanden ist. (#3329)
 * Aktualisierungen in Live-Regionen werden ausgegeben, wenn Sie den Fokus bewegen. (#3777)
* In Firefox und anderen Gecko-Anwendungen werden Elemente, die als ARIA-Presentation gekennzeichnet sind, korrekt im Lesemodus angezeigt. (#3781)
* Leistungsverbesserungen in Microsoft Word, wenn die Ansage von Rechtschreibfehlern aktiviert ist. (#3785)
* Verbesserung der Unterstützung von zugänglichen Java-Anwendungen:
 * Wenn ein Rahmen oder ein Dialogfeld in den Vordergrund gebracht wird, wird das Steuerelement korrekt erkannt, das innerhalb den Fokus erhalten hat. (#3753)
 * Nutzlose Positionsangaben (wie 1 von 1) für Auswahlschalter werden nicht mehr angezeigt. (#3754)
 * Verbesserte Anzeige von Konbinationsfeldern (es wird kein HTML mehr angezeigt; der Status [erweitert/reduziert] wird korrekt erkannt). (#3755)
 * Beim automatischen Vorlesen von Dialogfeldern wird mehr Text angezeigt. (#3857)
 * Die Änderung von Namen, Wert oder Beschreibung des fokussierten Steuerelements wird besser verfolgt. (#3770)
* Problem behoben, wonach NVDA unter Windows 8 manchmal abstürzte, wenn man ein Erweitertes Eingabefeld (wie den Protokollbetrachter oder WinDbg) in den Fokus nimmt. (#3867)
* Auf Systemen mit modernen Monitoren wird nun die Maus nicht mehr an die falsche Stelle gesetzt. (#3758, #3703)
* Problem behoben, wonach NVDA beim Lesen einer Webseite nicht richtig funktioniert. (#3804)
* Eine Papenmeier-Braillezeile kann jetzt problemlos verwendet werden, auch wenn sie zuvor noch nie per USB verbunden war. (#3712)
* NVDA hängt sich nicht mehr auf, wenn Sie versuchen, den Treiber für ältere Papenmeier-Braillezeilen auszuwählen, obwohl keine Braillezeile angeschlossen ist.

### Änderungen für Entwickler

* Alle Anwendungsmodule enthalten nun die Eigenschaften productName und productVersion. Diese Informationen werden auch in der Entwicklerinfo angezeigt, die mit der Tastenkombination NVDA+F1 abgerufen werden kann. (#1625)
* Sie können nun in der Python-Konsole Tab drücken, um den aktuellen Bezeichner zu vervollständigen. (#433)
 * Sollte es mehrere Möglichkeiten zur Autovervollständigung geben, können Sie ein zweites Mal Tab drücken und anschließend den gewünschten Eintrag aus einem Menü auswählen.

## 2013.3

### Neue Features

* In Microsoft Word werden Formularfelder erkannt. (#2295)
* Wenn in Microsoft Word die Funktion "Änderungen verfolgen" aktiviert ist, werden Revisionen angezeigt. Bedenken Sie, dass Sie im Dialogfeld für die Dokument-Formatierungen die Anzeige von Editor-Revisionen aktivieren müssen, damit diese Änderung wirksam wird. Diese Option ist standardmäßig deaktiviert. (#1670)
* Beim Navigieren in und Bearbeiten von Microsoft Excel-Dokumenten werden Kombinationsfelder angezeigt. (#3382)
* Eine neue Option "Navigation während Alles Lesen erlauben" im Dialogfeld für die Tastatur-Einstellungen ermöglicht Ihnen, Schnellnavigationstasten des Lesemodus oder Befehle zum Navigieren zwischen Zeilen und Absätzen zu verwenden, während Sie sich dieses vorlesen lassen. Diese Option ist standardmäßig deaktiviert. (#2766)
* Das Dialogfeld "Eingaben" erlaubt das Ändern von Eingabemöglichkeiten wie Tastenkombinationen für diverse Befehle innerhalb von NVDA. (#1532)
* Mit Hilfe von Konfigurationsprofilen können Sie unterschiedliche Einstellungen für unterschiedliche Situationen laden. Profile können entweder manuell aktiviert oder beim Wechsel in eine bestimmte Anwendung automatisch geladen werden. (#87, #667, #1913)
* In Microsoft Excel werden Zellen als Links erkannt, wenn sie auch Links enthalten. (#3042)
* Kommentare in Microsoft Excel werden nun korrekt erkannt. (#2921)

### Fehlerbehebungen

* Zend Studio funktioniert nun wie Eclipse. (#3420)
* Die Änderungen des Status von Kontrollkästchen im Dialogfeld für Nachrichtenregeln in Microsoft Outlook 2010 werden nun korrekt erkannt. (#3063)
* NVDA erkennt nun den Status "Angeheftet" für angeheftete Steuerelemente, wie z. B. Registerkarten in Mozilla Firefox. (#3372)
* Es ist nun möglich, Skripts an Tastenkombinationen mit Alt- oder der Windows-Taste zuzuweisen. Bisher wurde in solchen Fällen das Startmenü oder die Menüleiste der Anwendung angezeigt. (#3472)
* Das Markieren von Text im Lesemodus mit Strg+Umschalt+End verursacht kein versehentliches Umschalten des Tastaturschemas mehr. (#3472)
* Beim Beenden von NVDA stürzt der Internet Explorer nicht mehr ab. (#3397)
* Physikalisches verschieben, Änderung der Helligkeit sowie andere Ereignisse werden nun nicht mehr fälschlicher weise als Tastendruck erkannt. Zuvor wurde die Sprache gestoppt oder manchmal wurden Befehle für NVDA ausgelößt. (#3468)
* NVDA verhält sich nun in Poedit 1.5.7 erwartungsgemäß. Nutzer von älteren Versionen müssen aktualisieren. (#3485)
* NVDA kann nun geschützte Dokumente in Word 2010 lesen und stürzt nun nicht mehr ab. (#1686)
* Wird ein NVDA-Distributionspaket mit einem ungültigen Kommandozeilen-Parameter aufgerufen, führt dies nicht mehr zu einer endlosen Kette von Fehlermeldungen. (#3463)
* In Microsoft Word wird der Alternativtext für Grafiken korrekt erkannt, wenn er Anführungszeichen enthält. (#3579)
* Die Anzahl der Einträge in horizontalen Listen im Lesemodus wird korrekt erkannt; zuvor wurde fälschlicherweise manchmal die doppelte Anzahl angegeben. (#2151)
* Wenn Sie in einem Microsoft Excel-Tabellenblatt Strg+A drücken, wird nun die Markierung korrekt erkannt. (#3043)
* NVDA kann nun XHTML-Dokumente in Microsoft Internet Explorer und anderen mshtml-Steuerelementen richtig auslesen. (#3542)
* In den Tastatur-Einstellungen muss mindestens eine Taste als NVDA-Taste eingestellt werden. Ist dies nicht der Fall, so wird eine Fehlermeldung angezeigt. (#2871)
* In Microsoft Excel werden nun verbundene Zellen von mehreren markierten Zellen unterschieden. (#3567)
* Wenn Sie im Lesemodus aus einem Dialogfeld oder einer Anwendung ins Dokument zurückkehren, wird der Cursor nun richtig positioniert. (#3145)
* Problem behoben, wonach eine Braillezeile von HumanWare Brailliant BI/B nicht in den Braille-Einstellungen angezeigt wurde, auch wenn sie per Usb angeschlossen war.
* Wenn NVDA beim Wechsel in die Bildschirmdarstellung keine Objektposition erkennen kann, wird der NVDA-Cursor in die obere linke Ecke des Bildschirms gesetzt. (#3454)
* Problem behoben, wonach der Treiber für Braillezeilen von Freedom Scientific den Anschluss nicht richtig erkannt hat, wenn der Anschluss auf "usb" eingestellt war. (#3509, #3662)
* Problem behoben, wonach manchmal bestimmte Tastendrücke an Braillezeilen von Freedom Scientific nicht richtig erkannt wurden. (#3401, #3662)

### Änderungen für Entwickler

* Sie können nun die Skriptkategorie festlegen, die dem Benutzer im Dialogfeld "Einstellungen" -> "Eingaben" angezeigt wird. Verwenden Sie hierzu das Attribut scriptCategory bei SkriptableObject-Klassen oder das Attribut category bei Skriptmethoden. Sehen Sie sich die Dokumentation von baseObject.SkriptableObject für weitere Infos an. (#1532)
* Die Funktion "config.save" ist veraltet und wird in zukünftigen Versionen entfernt. Verwenden Sie stattdessen "config.conf.save". (#667)
* config.validateConfig ist veraltet und wird in einer der nächsten Versionen entfernt. Erweiterungen, die diese Methode benötigen, müssen sie selbst implementieren. (#667, #3632)

## 2013.2

### Neue Features

* Unterstützung für das eingebettete Chromium-Framework, das in einigen Anwendungen zum Einsatz kommt. (#3108)
* Neue eSpeak-Variante: Iven3.
* Wenn sich ein Skype-Chat-Fenster im Vordergrund befindet, werden ankommende Nachrichten automatisch ausgegeben. (#2298)
* Unterstützung für Tween, inkl. der Ausgabe von Registerkartennamen und weniger Ausführlichkeit bei der Ausgabe von Meldungen
* Sie können die Anzeige von Braille-Blitzmeldungen abschalten, indem Sie in den Braille-Einstellungen die anzeigedauer von Meldungen auf 0 setzen. (#2482)
* Im Dialogfeld "Erweiterungen verwalten" gibt es nun einen neuen Schalter "Erweiterungen herunterladen", über den Sie die Webseite für NVDA-Erweiterungen öffnen können. (#3209)
* Im Willkommensdialog, welcher immer beim ersten Start von NVDA geöffnet wird, gibt es ein neues Kontrollkästchen, mit dessen Hilfe Sie festlegen können, ob NVDA nach der Anmeldung automatisch geladen werden soll. (#2234)
* Bei der Verwendung von Dolphin Cicero wird automatisch der Schlafmodus aktiviert. (#2055)
* Unterstützung für die 64-Bit-Versionen für Miranda und Miranda NG. (#3296)
* Im Startbildschirm unter Windows 8.1 werden nun Suchvorschläge automatisch angezeigt. (#3322)
* Unterstützung beim Navigieren und Bearbeiten der Tabellenblätter in Microsoft Excel 2013. (#3360)
* Verbesserte Unterstützung für die Focus 14 Blue, Focus 40 Blue und Focus 80 Blue von Freedom Scientific, wenn diese mit Bluetooth verwendet werden, jedoch zuvor nicht erkannt wurden. (#3307)
* Vorschläge zur Autovervollständigung in Outlook 2010 werden angezeigt. (#2816)
* Neue Braille-Übersetzungstabellen: Computerbraille für Englisch (vereinigtes Königreich), koreanische Kurzschrift, russisches Computerbraille
* Neue Sprache: Farsi. (#1427)

### Änderungen

* Wenn Sie im Objektmodus mit einem Finger nach rechts/links streichen, navigiert NVDA unter Verwendung ALLER Objekte zum nächsten/vorigen Objekt und bezieht sich nicht auf den aktuellen Continer. Streichen Sie mit 2 Fingern nach rechts/links, um unter Berücksichtigung der Objekthierarchie zum nächsten/vorigen Objekt zu navigieren.
* Die Option "Layouttabellen ansagen" wurde in "Layouttabellen einschließen" umbenannt. Hierdurch wird verdeutlicht, dass Layouttabellen nicht angesprungen werden, wenn Sie die Schnellnavigationstasten verwenden, während diese Option deaktiviert ist. (#3140)
* Der Flächenmodus wurde durch die Darstellungsmodi Objektdarstellung, Dokumentdarstellung und Bildschirmdarstellung ersetzt (#2996)
 * Im Objektmodus können Sie sich den Inhalt des aktuellen Navigator-Objekts anzeigen lassen; im Dokumentmodus wird der Inhalt des gesamten Dokuments angezeigt; im Bildschirm-Darstellungsmodus wird der gesamte Bildschirminhalt der aktuellen Anwendung angezeigt
 * Die Befehle zum Wechsel vom/in den Flächenmodus schalten nun zwischen den unterschiedlichen Darstellungsmodi um.
 * Wenn Sie in die Modi Bildschirmdarstellung oder Dokumentdarstellung gewechselt haben und die Befehle zum Betrachten von Text verwenden, wird der Navigator den NVDA-Cursor verfolgen und sich auf das am meisten untergeordnete Objekt setzen.
 * Wenn Sie in den Modus Bildschirmdarstellung gewechselt haben, wird NVDA in diesem Modus bleiben, bis Sie zurück in den Modus Dokumentdarstellung oder Objektdarstellung wechseln.
 * Wenn Sie sich im Dokument- oder Objektmodus befinden, wird NVDA zwischen den beiden Modi automatisch wechseln, abhängig davon, ob Sie sich im Lesemodus befinden oder nicht.
* Der Braille-Übersetzer LibLouis wurde auf 2.5.3 aktualisiert. (#3371)

### Fehlerbehebungen

* Beim Ausführen der Standardaktion mit einem Objekt wird der Name der Standardaktion (wie z. B. "erweitern" oder "reduzieren" bei Einträgen einer Baumstruktur) angegeben, noch bevor die Aktion ausgeführt wird. (#2982)
* Präzise Cursorverfolgung in diversen Eingabefeldern innerhalb von Skype (wie z. B. Unterhaltungen, Suchfelder, etc.). (#1601, #3036)
* Sofern relevant, wird in der Liste der Konversationen in skype die Anzahl der anstehenden Ereignisse (Neue Nachrichten, etc.) angegeben. (#1446)
* Verbesserte Cursorverfolgung für Sprachen mit Rechts-Links-Ausrichtung (wie z. B. Arabisch) in Microsoft Excel. (#1601)
* Bei der Schnellnavigation für Formularfelder und Schalter werden nun auch Links angesprungen, die aus Gründen der Zugänglichkeit als Schalter ausgewiesen wurden. (#2750)
* Im Lesemodus werden nun keine Baumstrukturen mehr verarbeitet, da dies nicht sinnvoll ist. Drücken Sie auf einer Baumstruktur die Eingabetaste, um in den Fokusmodus zu wechseln und mit der Baumstruktur zu interagieren. (#3023)
* Beim Drücken von Alt+Pfeil Ab bzw. Alt+Pfeil Auf zum Erweitern bzw. Reduzieren von Kombinationsfeldern wird nun nicht mehr in den Lesemodus gewechselt. (#2340)
* Im Internet Explorer 10 wird beim Navigieren innerhalb von Tabellen nicht mehr automatisch in den Fokusmodus gewechselt, es sei denn, der Webentwickler hat bestimmte Zellen ausdrücklich als Fokussierbar gekennzeichnet. (#3248)
* NVDA wird nun nicht mehr abstürzen, wenn die Systemzeit auf einen früheren Zeitpunkt eingestellt ist als der Zeitpunkt der letzten Prüfung nach aktualisierungen. (#3260)
* Wenn ein Fortschrittsbalken auf der Braillezeile angezeigt wird, wird die Braillezeile automatisch aktualisiert, wenn sich der Fortschrittsbalken ändert. (#3258)
* In Mozilla-Anwendungen wird die Beschriftung von Tabellen nur noch einmal verarbeitet; außerdem wird die Zusammenfassung von Tabellen korrekt verarbeitet. (#3196)
* Wenn Sie in Windows 8 die Eingabesprache ändern, wird NVDA nun in der richtigen Sprache sprechen.
* NVDA meldet nun eine Änderung des IME-Konvertierungsmodus in Windows 8, sobald Sie ihn ändern.
* NVDA sagt auf dem Desktop keine unsinnigen Zeichen mehr an, wenn die Eingabemetoden Google Japanese oder Atok IME verwendet werden. (#3234)
* Wenn Sie in Windows 7 oder neuer einen Touchscreen oder die Spracherkennung zur Dateneingabe verwenden, wird NVDA keinen Wechsel der Tastatursprache mehr melden.
* Wenn die Ansage eingegebener Zeichen aktiviert ist und Sie drücken in bestimmten Eingabefeldern Strg+Rücktaste, wird NVDA nicht mehr irrtümlich das Steuerzeichen 0x7f ansagen. (#3315)
* NVDA wird nun nicht mehr irrtümlich die Lautstärke, Tonhöhe oder die Sprechgeschwindigkeit ändern, wenn der zu sprechende Text bestimmte Steuerzeichen oder xml-Strukturen enthält. (#3334) (regression von #437)
* In Java-Anwendungen wird eine Änderung der Beschriftung oder des Wertes eines hervorgehobenen Steuerelements korrekt erkannt. (#3119)
* Bei Scintilla-Steuerelementen werden die einzelnen Zeilen nun korrekt angezeigt, wenn der Wortumbruch aktiviert ist. (#885)
* Wenn Sie sich mit Mozilla-Anwendungen auf Twitter.com im Fokusmodus durch die Meldungen bewegen, werden schreibgestützte Einträge nun korrekt erkannt. (#3327)
* Bestätigungsdialoge in Office 2013 werden nun automatisch angezeigt.
* Leistungsverbesserungen beim Navigieren in Tabellen in Microsoft Word (#3326)
* Wenn sich in einer Microsoft-Word-Tabelle eine Zelle über mehrere Zeilen erstreckt, funktionieren nun die Tabellennavigationsbefehle (Strg+alt+Pfeiltasten) korrekt.
* Wenn der Erweiterungs-Manager bereits ausgeführt wird, führt ein erneutes Aktivieren des Erweiterungs-managers (entweder über extras --> Erweiterungen verwalten oder direkt aus dem Explorer heraus durch Öffnen einer ".nvda-addon"-Datei) nicht mehr zu einem Fehler. (#3351)
* NVDA wird nicht mehr abstürzen, wenn Sie eine japanische oder chinesische IME Version von Office 2010 verwenden. (#3064)
* Mehrere leerzeichen werden in Braille nicht mehr zu einem Leerzeichen komprimiert. (#1366)
* Die PHP-Entwicklungswerkzeuge von Eclipse funktionieren nun ähnlich wie Eclipse. (#3353)
* Im Internet Explorer ist es nicht mehr nötig, Tab zu drücken, um mit eingebetteten Objekten wie Flash zu arbeiten. (#3364)
* Beim Bearbeiten von Text in PowerPoint wird die letzte Zeile korrekt erkannt, auch wenn sie leer ist. (#3403)
* In PowerPoint werden Objekte nicht mehr fälschlicherweise zweimal angezeigt, wenn Sie sie auswählen oder bearbeiten wollen. (#3394)
* NVDA bringt den Adobe Reader nun nicht mehr zum Absturz, wenn fehlerhaft gestaltete Pdf-Dokumente geöffnet sind, die Tabellenzeilen außerhalb von Tabellen enthalten. (#3399)
* Wenn Sie in Microsoft PowerPoint in der Miniaturansicht eine Folie löschen, wird nun die nächste Folie korrekt erkannt. (#3415)

### Änderungen für Entwickler

* Mit windowUtils.findDescendantWindow können Sie ein Objekt (angegeben durch seine Zugriffsnummer) nach einem untergeordneten Objekt mit bestimmten Kriterien absuchen (Sichtbarkeit, Steuerelementnummer und/oder Klassenname).
* Die Remote-Python-Konsole beendet sich nun nicht mehr nach 10 Sekunden, wenn sie auf eine Eingabe wartet. (#3126)
* Das Modul bisect ist veraltet und wird demnächst aus dem Binärpaket von NVDA entfernt. (#3368)
 * Erweiterungen, die Bisect (einschließlich urllib2) benötigen, sollten diese Module mitliefern.

## 2013.1.1

Neben anderen Fehlerbehebungen und aktualisierten Übersetzungen wird in dieser NVDA-Version ein Problem behoben, wonach NVDA abgestürzt ist, wenn irisch als Landessprache eingestellt war.

### Fehlerbehebungen

* Wenn in NVDA-Dialogen bei der Eingabe von Zeichen eingabemethoden für koreanisch oder japanisch verwendet werden, werden nun die richtigen Zeichen erzeugt. (#2909)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden Eingabefelder korrekt angezeigt, wenn ungültige Werte eingegeben werden. (#3256)
* NVDA stürzt nun nicht mehr beim Start ab, wenn Irisch als Landessprache eingestellt ist.

## 2013.1

Schwerpunkte dieser Version sind u. a. ein intuitiveres Tastaturschema für Laptops; grundlegende Unterstützung für Microsoft PowerPoint; Unterstützung für lange Beschreibungen in Web-Browsern; sowie die Unterstützung für die Eingabe von Computerbraille mit Hilfe von Braillezeilen, die eine Brailletastatur besitzen.

### Wichtig

#### Neues Laptop-Tastaturschema

Das Laptop-Tastaturschema wurde überarbeitet, sodass es intuitiver und konsistenter wird.
So werden z. B. die Pfeiltasten in Kombination mit der NVDA-Taste und anderen Umschaltern zum Betrachten von Text verwendet.

Folgende Änderungen wurden an häufig verwendeten Befehlen vorgenommen:

| Name |Tastenkombination|
|---|---|
|Alles ansagen |NVDA+A|
|Aktuelle Zeile lesen |NVDA+L|
|Aktuelle Textauswahl lesen |NVDA+Umschalt+S|
|Statuszeile vorlesen |NVDA+Umschalt+Ende|

Zudem wurden die Befehle für die objektnavigation, zum Betrachten von Text, für Mausaktionen sowie der Sprachausgaben-Einstellungsring geändert.
Für weitere Informationen sehen Sie in der [Befehlsreferenz](keyCommands.html) nach.

### Neue Features

* Grundlegende Unterstützung für das Lesen und Bearbeiten von Microsoft PowerPoint-Präsentationen. (#501)
* Unterstützung für den automatischen Sprachenwechsel beim Lesen von Dokumenten in Microsoft Word. (#2047)
* Grundlegende Unterstützung beim Lesen und Schreiben von Nachrichten in Lotus Notes 8.5. (#543)
* Im Lesemodus für MSHTML (z. B. Internet Explorer) und Gecko (z. B. Firefox) wird nun die Existenz langer Beschreibungen gemeldet. Sie können die lange Beschreibung jedoch auch durch Drücken von NVDA+D in einem neuen Fenster öffnen. (#809)
* Im Internet Explorer 9 und neuer werden Benachrichtigungen korrekt ausgegeben (wenn z. B. Inhalte oder herunterzuladene Dateien blockiert werden). (#2343)
* Automatisches Ausgeben von Spalten- und Reihenüberschriften von Tabellen im Internet Explorer und anderen mshtml-Dokumenten wird unterstützt (#778)
* Neue Sprache: Aragonesisch, Irisch
* Neue Braille-Übersetzungstabellen: Dänische Kurzschrift, koreanische Vollschrift. (#2737)
* Unterstützung für Bluetooth-Braillezeilen, die unter Verwendung des Bluetooth-Stacks von Toshiba mit dem Computer verbunden werden. (#2419)
* Unterstützung für die Auswahl des Anschlusses der Braillezeilen von Freedom Scientific (Optionen: Automatisch, USB oder Bluetooth).
* Unterstützung für Notizgeräte der Braillenote Familie von Humanware, wenn diese als Braillezeile für einen Bildschirmleser arbeiten. (#2012)
* Unterstützung für ältere Papenmeier-Braillezeilen. (#2679)
* Unterstützung für die Eingabe von Computer-Braille für Braillezeilen, die eine Braille-Tastatur besitzen. (#808)
* Neue Tastaturoptionen erlauben das Unterbrechen der Sprache beim Eingeben von Zeichen bzw. beim Drücken der Eingabetaste. (#698)
* Unterstützung für zahlreiche Chrome-basierte Browser: Rockmelt, BlackHawk, Comodo Dragon und SRWare Iron. (#2236, #2813, #2814, #2815)

### Änderungen

* Der Braille-Übersetzer LibLouis wurde auf 2.5.2 aktualisiert. (#2737)
* Das Laptop-Tastaturschema wurde komplett überarbeitet, wodurch es intuitiver und konsistenter wird. (#804)
* Die Sprachausgabe eSpeak wurde auf Version 1.47.11 aktualisiert. (#2680, #3124, #3132, #3141, #3143)

### Fehlerbehebungen

* Die Schnellnavigationstasten zum Springen zu Trennlinien funktionieren nun in Internet Explorer und anderen MSHTML-Dokumenten. (#2781)
* Wenn es NVDA einmal nicht gelingen sollte, eine Sprachausgabe zu laden, sodass es auf eSpeak zurückfallen oder die Sprachausgabe gänzlich deaktivieren muss, wird die Konfiguration nun nicht mehr aktualisiert und NVDA wird erneut versuchen, die ursprünglich eingestellte Sprachausgabe zu laden, wenn es neu gestartet wird. (#2589)
* Wenn es NVDA einmal nicht gelingen sollte, eine Braillezeile anzusteuern, sodass es auf keine Braillezeile zurückfällt, wird die Konfiguration nun nicht mehr aktualisiert und NVDA wird erneut versuchen, die ursprünglich eingestellte Braillezeile anzusteuern, wenn es neu gestartet wird. (#2264)
* In Mozilla-Anwendungen werden Aktualisierungen in Tabellen korrekt verarbeitet. So werden beispielsweise Koordinaten von aktualisierten Zellen richtig angegeben; die Navigation sollte ebenfalls korrekt funktionieren. (#2784)
* Im Lesemodus in Internet-Browsern werden anklickbare unbeschriftete Grafiken nun korrekt verarbeitet. (#2838)
* Ältere und neuere Versionen von SecureCRT werden unterstützt. (#2800)
* Die einfachen Punkte (IME) werden nun unter XP beim Lesen korrekt ausgegeben.
* Die Liste der Schriftsätze in den Eingabemethoden von Microsoft Pinyin (Vereinfachtes Chinesisch) unter Windows 7 werden bei Seitenänderungen durch Pfeiltasten nach links/rechts und Pos1 korrekt ausgegeben.
* Beim Speichern der Aussprache benutzerdefinierter Symbole wird das Feld "beibehalten" nicht mehr entfernt. (#2852)
* Wird die automatische Prüfung nach Aktualisierungen deaktiviert, muss NVDA nicht mehr neu gestartet werden, damit die Änderung wirksam wird.
* NVDA wird nun nicht mehr abstürzen, wenn bei der Deinstallation einer Erweiterung deren Ordner nicht gelöscht werden kann, weil er von einem anderen Programm verwendet wird. (#2860)
* Die Beschriftungen der Registerkarten im Einstellungsdialog von Dropbox werden nun im Flächenmodus angezeigt.
* Wenn die Eingabesprache gewechselt wurde, erkennt NVDA diese nun korrekt und kann sie für Befehle und der Eingabehilfe verwenden.
* Für Sprachen wie z. B. Deutsch, bei denen das Pluszeichen (+) eine einzelne Taste ist, ist es nun möglich, das Pluszeichen in Tastenkombinationen zu verwenden, in dem man das Wort "plus" verwendet. (#2898)
* Im Internet Explorer und anderen MSHTML-Elementen werden Zitate nun angesagt, wenn Sie auftauchen. (#2888)
* Der Braillezeilentreiber für die HumanWare Brailliant BI/B serie kann nun ausgewählt werden, wenn die Braillezeile mittels Bluetooth verbunden wurde, aber noch nie über USB verbunden wurde.
* Wenn beim Eingeben eines Filterbegriffs in die Elementliste im lesemodus Großbuchstaben verwendet werden, wird nun ohne Berücksichtigung von Groß-/Kleinschreibung gefiltert (wie beim Eingeben von Kleinbuchstaben) (#2951)
* In Mozilla-Browsern kann nun wieder der Lesemodus verwendet werden, wenn Flash-Inhalte den Fokus haben. (#2546)
* Wenn Sie eine Kurzschrift-Übersetzungstabelle verwenden und die Option zum Ausschreiben des aktuellen Wortes in Computerbraille aktiviert ist, wird der Braille-Cursor nun korrekt gesetzt, wenn er hinter einem Wort steht, das ein Zeichen enthält, das durch mehrere Braille-Zeichen dargestellt wird. (z. B. Großbuchstaben, Zahlenzeichen, etc.). (#2947)
* In Microsoft Word und im Internet Explorer wird markierter Text nun korrekt in Braille angezeigt.
* Wenn Sie eine Braillezeile benutzen, können Sie nun wieder Text rückwärts markieren, wenn Sie sich in Microsoft Word befinden.
* Wenn Sie in Scintilla-Eingabefeldern die Befehle zum Betrachten von Text verwenden oder Zeichen löschen, wird NVDA Multibyte-Zeichen korrekt ausgeben. (#2855)
* Die Installation von NVDA wird nun nicht mehr fehlschlagen, wenn der Name des Benutzerprofilverzeichnisses bestimmte Multibyte-Zeichen enthält. (#2729)
* Bei der Ausgabe von Gruppen in Listen-Steuerelementen (syslistview32) in 64-Bit-Anwendungen kommt es nun nicht mehr zu einem Fehler.
* Im Lesemodus von Mozilla-Anwendungen werden Textinhalte nun nicht mehr fälschlicherweise als deaktiviert angezeigt, auch wenn das selten der Fall ist. (#2959)
* In IBM Lotus Symphony und Apache OpenOffice wird nun der NVDA-Cursor mitgezogen, wenn der System-Cursor bewegt wird.
* Im Internet Explorer unter Windows 8 sind Inhalte mit Adobe Flash nun zugänglich. (#2454)
* Bluetooth-Unterstützung für Papenmeier Braillex Trio korrigiert. (#2995)
* Bestimmte Microsoft SAPI-5-Stimmen wie z. B. Stimmen von Koba Speech konnten von NVDA nicht verwendet werden. Dies wurde nun behoben. (#2629).
* In Java-Anwendungen wird nun die Braille-Anzeige korrekt aktualisiert, wenn Sie sich innerhalb von Textfeldern bewegen. (#3107)
* Unterstützung von Landmark-Formularen. (#2997)
* Bessere Behandlung beim zeichenweises Navigieren mit eSpeak Zeichen aus Fremdsprachen. (#3106)
* Das Kopieren der Benutzerkonfiguration in die Systemkonfiguration funktioniert jetzt auch, wenn der name des Benutzerprofilverzeichnisses nicht-ascii-Zeichen enthält (#3092)
* NVDA wird nun nicht mehr abstürzen, wenn asiatische Zeichen in .net-Anwendungen eingegeben werden. (#3005)
* Im Internet Explorer 10 ist es jetzt auch im Standardmodus möglich den Lesemodus von NVDA zu benutzen (Beispiel: Die Anmeldeseite auf [www.gmail.com](http://www.gmail.com)). (#3151)

### Änderungen für Entwickler

* Braillezeilentreiber unterstützen die Auswahl des Anschlusses (#426)
 * Dies ist für Braillezeilen sinnvoll, die an eine serielle Schnittstelle angeschlossen werden.
 * Hierfür können Sie die Klassenmethode getPossiblePorts aus der Klasse BrailleDisplayDriver verwenden.
* Braille-Eingabe von Braille-Tastaturen wird nun unterstützt (#808)
 * Braille-Eingaben werden in die Klasse brailleInput.BrailleInputGesture oder eine abgeleitete Klasse eingeschlossen.
 * Unterklassen von "braille.BrailleDisplayGesture" (wie sie z. B. in Braillezeilentreibern implementiert sind) können auch von brailleInput.BrailleInputGesture ableiten. Dies ermöglicht die Verarbeitung von Braille-Navigationsbefehlen und Braille-Eingaben von ein und derselben Klasse.
* Sie können nun "comHelper.getActiveObject" verwenden, um ein Com-Objekt von einem normalen Prozess zu erstellen, wenn NVDA mit UIAccess-Berechtigungen ausgeführt wird. (#2483)

## 2012.3

Schwerpunkte in dieser Version sind: Unterstützung für asiatische Eingabemetoden, experimentelle Unterstützung für Touchscreens unter Windows 8, Ansage der Seitenzahlen sowie verbesserte Unterstützung von Tabellen in Adobe Reader, Befehle zur Navigation in Tabellen und Listenansichten im Explorer sowie Unterstützung zahlreicher weiterer Braillezeilen und das Lesen von Zeilen- bzw. Spaltenüberschriften in Microsoft Excel.

### Neue Features

* NVDA unterstützt nun asiatische Zeichen eingabe mittels IME und Eingabemethoden im Textdienst in allen Anwendungen, einschließlich:
 * Ansagen und Navigation der Liste der zeichensätze
 * Ansagen und Navigation der Eingabeketten
 * Ansage der Leseketten
* Unterstrichener oder durchgestrichener Text wird nun in Dokumenten in Adobe Reader korrekt erkannt. (#2410)
* Wenn die Einrastfunktion der Eingabehilfen in Windows aktiviert ist, verhält sich die NVDA-Taste nun wie andere Umschalt-Tasten. Das Heißt, dass Sie die NVDA-Taste nicht mehr gedrückt halten müssen, wenn Sie NVDA-Befehle ausführen möchten. (#230)
* In Microsoft Excel wird nun die automatische Angabe von Spalten- und Reihenüberschriften unterstützt. Drücken Sie NVDA+Umschalt+C, um die Reihe festzulegen, die Spaltenüberschriften enthält; oder NVDA+Umschalt+r um die Spalte festzulegen, die die Reihenbeschriftungen enthält. Drücken Sie die entsprechende Tastenkombination zweimal, um die Zuweisungen zu löschen. (#1519)
* Unterstützung der Braillezeilen Braille Sense, Braille EDGE und SyncBraille der Firma HIMS. (#1266, #1267)
* Wenn in Windows 8 Benachrichtigungen angezeigt werden, werden diese auch von NVDA ausgegeben, sofern die Option "Hilfe-Sprechblasen ansagen" in den Einstellungen zur Objektdarstellung aktiviert ist. (#2143)
* Experimentelle Unterstützung für Touchscreens in Windows 8. Hierzu zählen:
 * Das Ausgeben von Text direkt unter Ihrem Finger, wenn Sie ihn über den Bildschirm bewegen
 * Viele Gesten zur Objektnavigation, zum Betrachten von Text und für andere NVDA-Befehle
* Unterstützung für VipMud. (#1728)
* Wenn in Adobe Reader einer Tabelle eine Zusammenfassung zugewiesen wurde, wird diese nun angezeigt. (#2465)
* In Adobe Reader können nun Reihen und Spaltenüberschriften ausgegeben werden. (#2193, #2527, #2528)
* Neue Sprachen: Nepalesisch, Koreanisch, Amharisch, Slovenisch.
* Bei der Eingabe von E-Mail-Adressen in Outlook 2007 werden Vorschläge zur automatischen Vervollständigung korrekt ausgegeben. (#689)
* Neue eSpeak-Varianten: Gene, Gene2. (#2512)
* In Adobe Reader werden Seitenzahlen nun korrekt ausgegeben. (#2534)
 * In Adobe Reader XI werden nun Seitenbeschriftungen ausgegeben, falls vorhanden, um abweichende Seitennumerierungen für unterschiedliche Abschnitte kenntlich zu machen. Dies ist in früheren Versionen von Adobe Reader nicht möglich; Dort werden nur fortlaufende Seitenzahlen ausgegeben.
* Es ist nun möglich, NVDA auf die Standard-Einstellungen zurückzusetzen. Dies kann entweder durch dreimaliges Drücken von NVDA+Strg+R oder durch Wählen von "Auf Standard-Einstellungen zurücksetzen" im NVDA-Menü erledigt werden. (#2086)
* Unterstützung der Braillezeilen SEIKA Version 3, 4 und 5 sowie Seika80 von Nippon Telesoft. (#2452)
* Bei Braillezeilen PAC Mate und Focus von Freedom Scientific können die Routing-Tasten über dem ersten oder letzten Modul nun zum Rückwärts- oder Vorwärtsscrollen verwendet werden. (#2556)
* Viele weitere Funktionen der Braillezeilen Focus von Freedom Scientific erweiterte Tastenreihe, Daumenräder und bestimmte Punktkombinationen für allgemeine Funktionen werden unterstützt. (#2516)
* In Anwendungen, die IAccessible2 verwenden (wie z. B. Mozilla-Anwendungen) werden nun Spalten- und Zeilenüberschriften auch außerhalb des Lesemodus angezeigt. (#926)
* Vorläufige Unterstützung für die Dokumentsteuerung in Microsoft Word 2013. (#2543)
* Die Ausrichtung von Text kann nun in Anwendungen, die IAccessible2 verwenden ausgegeben werden. Hierzu gehören bspw. Anwendungen von Mozilla. (#2612)
* Wenn eine Liste mehrere Spalten besitzt, können Sie nun die Navigationstasten für Tabellen benutzen, um auf einzelne Spalten zuzugreifen. (#828)
* Neue Braille-Übersetzungstabellen: Estnische Basisschrift, portugiesisches 8-Punkt-Computerbraille, Italienisches 6-Punkt-Computerbraille. (#2319, #2662)
* Wenn NVDA fest installiert ist, kann eine Erweiterung direkt geöffnet werden; entweder vom Explorer aus oder über eine entsprechende Funktion im Browser beim Herunterladen. (#2306)
* Unterstützung für neuere papenmeier-Brailex-Zeilen. (#1265)
* Positionsinformationen (z. B. 1 von 4) in Windows 7 und neuer in Windows explorer werden nun korrekt angegeben. Dies betrifft auch Steuerelemente der UIA, die die benutzerdefinierten Eigenschaften itemIndex und itemCount unterstützen. (#2643)

### Änderungen

* Im Dialogfeld für die NVDA-Cursor-Einstellungen wurde die Einstellung "Tastaturfokus verfolgen" in "System-Fokus verfolgen" umbenannt, um mit anderen Teilen von NVDA zu harmonieren, in denen diese Namensgebung verwendet wird.
* Wenn die Braillezeile an den Navigator gekoppelt ist und gerade ein objekt angezeigt wird, das kein Textobjekt ist (wie z. B. ein Eingabefeld), kann das objekt durch Drücken der Cursorroutingtasten aktiviert werden. (#2386)
* Die Option "Einstellungen beim Beenden speichern" ist bei neuen Konfigurationen nun standardmäßig aktiviert.
* Beim Aktualisieren von NVDA wird die Tastenkombination der Desktop-Verknüpfung nun nicht mehr auf Strg+Alt+N zurückgesetzt, wenn der Anwender diese manuell geändert haben sollte. (#2572)
* Die Liste der Erweiterungen im Dialogfeld "Erweiterungen verwalten" zeigt nun den Namen der Erweiterung vor deren Status an. (#2548)
* Wenn Sie die gleiche Version bzw. eine andere Version einer bereits installierten Erweiterung installieren, werden Sie nun gefragt, ob Sie die Erweiterung aktualisieren möchten. Zuvor wurde einfach eine Fehlermeldung angezeigt und die Installation abgebrochen. (#2501)
* Die Befehle zur Objektnavigation (bis auf den Befehl zur ausgabe des aktuellen objekts) sind nun weniger ausführlich. Sie können aber dennoch weitere Informationen über ein objekt abrufen, indem Sie den Befehl zur Ausgabe des aktuellen Objekts verwenden. (#2560)
* Der Braille-Übersetzer LibLouis wurde auf 2.5.1 aktualisiert (#2319, #2480, #2662, #2672).
* Da die NVDA-Kurztasten- und Befehlsreferenz nun auch Gesten für Touchscreens enthält, wurde sie in "Befehlsreferenz" umbenannt.
* In der Elementliste merkt sich NVDA nun den eingestellten Elementtyp (z. B. Links, überschriften), solange Sie NVDA nicht neu starten. (#365)
* In den meisten Metro-Anwendungen in Windows 8 (wie z. B. Mail oder im Kalender) wird nun nicht mehr der Lesemodus für die gesamte Anwendung aktiviert.
* HandyTech-BraillezeilenTreiber COM-Server auf 1.4.2.0. aktualisiert.

### Fehlerbehebungen

* Wurde der Computer in Windows Vista und neuer mit Windowstaste+L gesperrt und wieder entsperrt, so bleibt die Windows-Taste nun nicht mehr fälschlicherweise hängen. (#1856)
* In Adobe Reader werden Zeilenüberschriften nun richtig als Zellen in einer Tabelle erkannt, sodass z. B. die Zellkoordinaten angesagt werden und durch die Tabellennavigation angesteuert werden können. (#2444)
* In Adobe Reader werden Zellen, die sich über mehr als eine Spalte und/oder Reihe erstrecken, richtig behandelt. (#2437, #2438, #2450)
* Vor der Ausführung des NVDA-Installationspakets wird nun dessen Integrität geprüft. (#2475)
* Wenn das Herunterladen der temporären Kopie von NVDA während einer Aktualisierung fehlschlägt, wird die temporäre Kopie entfernt. (#2477)
* Wird NVDA mit Administratorrechten ausgeführt, kommt es beim Kopieren der Benutzerkonfiguration zur Systemkonfiguration nun nicht mehr zu Abstürzen. (#2485)
* Im Startbildschirm von Windows 8 werden die Kacheln nun weniger ausführlich dargestellt (der Name der Kachel wird nicht mehr doppelt ausgegeben, der Status "nicht ausgewählt" wird nicht mehr ausgegeben). Des Weiteren werden Statusinformationen als Beschreibung ausgegeben (wie z. B. die aktuelle Temperatur in der Wetter-App).
* In Microsoft Outlook und anderen eingabefeldern, die als geschützt gekennzeichnet sind, werden die Kennwörter nun nicht mehr im Klartext ausgegeben. (#2021)
* Im Adobe Reader wirken sich Änderungen an formularfeldern nun auch im Lesemodus korrekt aus. (#2529)
* Verbesserungen an der Unterstützung für die Rechtschreibprüfung in Microsoft Word. Dies betrifft z. B. eine bessere Ausgabe von Rechtschreibfehlern und die Benutzung der Rechtschreibprüfung bei der Verwendung einer installierten NVDA-Version unter Windows Vista und neuer.
* Erweiterungen, die Dateinamen mit nicht-ASCII-codierten Zeichen enthalten, können jetzt ordnungsgemäß installiert werden. (#2505)
* In Adobe Reader geht die Sprach-Einstellung nun nicht mehr verloren, wenn die Seite scrollt oder aktualisiert wird. (#2544)
* Beim Installieren von Erweiterungen wird nun der korrekte (übersetzte) Name angezeigt, sofern vorhanden. (#2422)
* In Anwendungen, die UIA verwenden (wie etwa .net- oder Silverlight-Anwendungen) wurde die Berechnung numerischer Eigenschaften (wie etwa die Positionen von Schiebereglern) korrigiert. (#2417)
* Die Einstellungen für die Ausgabe von Fortschrittsbalken werden nun auch während der Installation von NVDA oder während der Erstellung einer portablen Version berücksichtigt. (#2574)
* Wenn ein Sicherer Desktop (wie etwa ein Sperrbildschirm) angezeigt wird, können nun keine NVDA-Befehle mehr mit einer Braillezeile ausgeführt werden. (#2449)
* Die Brailleausgabe wird nun im Lesemodus korrekt aktualisiert, wenn sich der anzuzeigende Text geändert hat. (#2074)
* In Sicheren Desktops wie etwa in der Benutzerkontensteuerung werden nun Meldungen ignoriert, die über den NVDA-Controller gesprochen werden oder in Braille angezeigt werden.
* Sie können im Lesemodus nun nicht mehr über das Ende des Dokumentes hinaus springen, wenn Sie (z. B. am Ende eines Dokumentes Pfeil Rechts drücken oder wenn sie sich aus einem Container herausbewegen wollen, der sich am Ende eines Dokumentes befindet. (#2463)
* In Web-Anwendungen (speziell in solchen, die ARIA-Dialoge, ohne das Attribut aria-describedby verwenden) wird nun keine belanglose Information mehr angezeigt. (#2390)
* Wenn der Autor einer Webseite ausdrücklich per ARIA eine Fensterklasse angegeben hat, werden in MSHTML-Dokumenten wie z. B. Internet Explorer keine Steuerelemente mehr falsch positioniert oder falsch ausgegeben. (#2435)
* Wenn in Konsolenanwendungen das Sprechen eingegebener Wörter aktiviert ist, wird nun die Rücktaste korrekt verarbeitet. (#2586)
* In Microsoft Excel werden Zellkoordinaten wieder in Braille angezeigt.
* NVDA bleibt nicht mehr in Microsoft Word hängen, wenn in einem Absatz numerische Listen- oder Aufzählungszeichen aufeinander folgen, und man versucht mit Strg+Pfeil links oder Pfeil links herauszunavigieren. (#2402)
* In Mozilla-Anwendungen werden Listenfelder (insbesondere ARIA-Listenfelder) korrekt verarbeitet.
* Im Lesemodus in Mozilla-Anwendungen werden einige falsch erkannte Steuerelemente nun korrekt angezeigt.
* Im Lesemodus wurden einige überflüssige Leerzeichen entfernt, während man sich in Mozilla-Anwendungen befindet.
* Im Lesemodus werden Grafiken korrekterweise ignoriert, die als Platzhalter gekennzeichnet sind (z. B. durch die Angabe von alt="")
* In Webbrowsern verbirgt NVDA nun Inhalte, die vor Bildschirmlesern versteckt gehalten werden sollen. Dies gilt insbesondere für solche Inhalte, die mit dem Attribut "aria-hidden" gekennzeichnet sind. (#2117)
* Negative Währungsangaben (wie z. B. -$123) werden nun unabhängig von der eingestellten Symbolebene korrekt verarbeitet (#2625).
* Während "Alles Lesen" wird nun nicht mehr unerwartet auf die Standardsprache gewechselt, wenn eine Zeile nicht mit einem Satz endet. (#2630)
* Die Schriftarteninformationen werden nun in Adobe Reader 10.1 und neuer korrekt erkannt. (#2175)
* Stellt ein Dokument im Adobe Reader Alternativtexte zur verfügung, so werden diese nun ausschließlich verwendet. Bisher wurden manchmal nutzlose Informationen angezeigt. (#2174)
* Wenn ein Dokument eine Anwendung enthält, wird bei der Navigation im Lesemodus nicht mehr unerwartet in die anwendung gewechselt. Sie können dennoch mit der Anwendung arbeiten. Dies geschieht auf die gleiche Weise wie bei eingebetteten Objekten. (#990)
* In Mozilla-Anwendungen wird nun der Wert eines Drehreglers korrekt erkannt, sobald er sich ändert. (#2653)
* Verbesserte Unterstützung für Adobe Digital Editions funktioniert jetzt auch mit version 2.0. (#2688)
* Wenn in Kombinationsfeldern im Internet Explorer NVDA+Pfeiltaste nach oben gedrückt wird, wird nun korrekterweise der aktuelle Eintrag gelesen, bisher wurden irrtümlich alle Einträge gelesen. (#2337)
* Die Aussprache-Wörterbücher werden korrekt gespeichert, wenn Sie im EingabeFeld "Suchen nach" oder "Ersetzen durch" ein Nummernzeichen "#" verwenden. (#961)
* Im Lesemodus für MSHTML-Dokumente (z. B. Internet Explorer) werden nun sichtbare Inhalte innerhalb verborgener Inhalte korrekt angezeigt. Dies betrifft insbesondere Elemente mit der Formatierung visibility:visible innerhalb von Elementen mit der Formatierung visibility:hidden. (#2097)
* Die Namen von Links im Windows XP-Sicherheitscenter werden nun korrekt angezeigt. (#1331)
* Texteingabefelder der UIA wie z. B. das Suchfeld im Windows-7-Startmenü werden nun korrekt erkannt, wenn Sie die Maus darüberbewegen.
* Der Wechsel des Tastaturschemas wird nun nicht mehr während des Lesens von Dokumenten gemeldet. Dies war bei mehrsprachigen Texten bisher problematisch. (#1676)
* Bei Texteingabefeldern der Benutzerautomatisierung wird nun nicht mehr fälschlicherweise der gesamte Inhalt ausgegeben (z. B. beim Suchfeld im Windows 7/8-startmenü).
* Beim Navigieren zwischen Gruppen im Windows 8-Startbildschirm wird die Navigation beschleunigt, indem bei unbeschrifteten Gruppen der Titel des ersten Eintrags nicht mehr als Gruppenname angegeben wird. (#2658)
* Wenn Sie im Windows 8 den Startbildschirm aufrufen, wird der Fokus korrekt auf den ersten Eintrag gesetzt; nicht mehr auf das Stammobjekt, was die Navigation beeinträchtigt hat. (#2720)
* NVDA wird nun nicht mehr abstürzen, wenn der Ordnername des Benutzerprofils Multibyte-Zeichen enthält. (#2729)
* Im Lesemodus in GoogleChrome wird Text innerhalb von Registerkarten nun korrekt angezeigt.
* Menü-Schalter werden im Lesemodus nun korrekt ausgegeben.
* In Calc (OpenOffice.org sowie in LibreOffice) funktioniert das Lesen von Tabellen nun ordnungsgemäß. (#2765)
* NVDA funktioniert nun in der Listenansicht der Yahoo Mails ordnungsgemäß, wenn Sie mit dem Internet Explorer arbeiten. (#2780)

### Änderungen für Entwickler

* Beim Start von NVDA wird nun das vorherige Protokoll nach "nvda-old.log" kopiert. Sollte NVDA also einmal abstürzen oder neu gestartet werden müssen, steht das Protokoll der vorigen NVDA-Sitzung zu Inspektionszwecken zur Verfügung. (#916)
* Wenn Sie innerhalb einer Methode chooseNVDAObjectOverlayClasses den Objekttyp abrufen wollen, wird dieser nun nicht mehr falsch zurückgegeben, wenn Objekte wie Eingabeaufforderungen oder Scintilla-Steuerelemente den Fokus haben. (#2569)
* Die Untermenüs des NVDA-Menüs sind nun als Attribute von gui.mainFrame.sysTrayIcon verfügbar. Sie heißen preferencesMenu, toolsMenu und helpMenu. Hierdurch ist es für globale Plug-ins einfacher, Einträge in diese Menüs einzufügen.
* Das Skript "navigatorObject_doDefaultAction" aus "globalCommands" wurde in "review_activate" umbenannt.
* Unterstützung für Gettext-Meldungskontexte hinzugefügt. Dies erlaubt mehrere Übersetzungen für eine englische Meldung abhängig vom Kontext. (#1524)
 * Dies wird durch den Funktionsaufruf pgettext(Kontext, Meldung) realisiert.
 * Dies wird sowohl von NVDA selbst als auch von Erweiterungen unterstützt.
 * Sie müssen xgettext und msgfmt aus GNU gettext verwenden, um Mo- und po-dateien zu erstellen. Die Python-Werkzeuge unterstützen Meldungskontexte jedoch nicht.
 * Bei der Verwendung von xgettext müssen Sie den Kommandozeilen-Parameter --keyword=pgettext:1c,2 verwenden, um Meldungskontexte zu berücksichtigen.
 * Weitere Informationen zu Meldungskontexten finden Sie unter https://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts
* Es ist nun möglich, auf NVDA-interne Module zuzugreifen, wenn diese von Drittanbietern überschrieben wurden. Sehen Sie sich das Modul nvdaBuiltin für weitere Informationen an.
* Die Übersetzung von Erweiterungen funktioniert nun auch innerhalb des Moduls für Installationsaufgaben. (#2715)

## 2012.2.1

Diese Version behebt einige potenzielle Sicherheitsprobleme (in dem Python auf die Version 2.7.3 aktualisiert wurde).

## 2012.2

Schwerpunkte dieser Version sind u. a. eine eingebaute Installationsroutine sowie eine Funktion zum einfachen Erstellen portabler Versionen, eine automatische Aktualisierungsfunktion, die einfache Verwaltung neuer Erweiterungen für NVDA, die Erkennung von Grafiken in Microsoft Word, Die unterstützung von Windows-8-Metro-Anwendungen, sowie einige wichtige Fehlerbehebungen.

### Neue Features

* NVDA kann nun nach Aktualisierungen suchen, diese herunterladen und installieren. (#73)
* Der Umgang mit eigenen Treibern und Plug-ins wurde durch die Einführung eines Erweiterungs-Managers stark vereinfacht. Der Erweiterungs-Manager erlaubt das einfache Installieren und deinstallieren von Erweiterungen (Dateien mit der Erweiterung ".nvda-addon"). Sie finden ihn im Menü Extras im NVDA-Menü. Ältere im Benutzer-Konfigurationsverzeichnis abgelegte Plug-ins und Treiber werden im Erweiterungs-Manager jedoch nicht angezeigt. (#213)
* Viele gebräuchliche Funktionen seitens NVDA funktionieren nun in den Metro-Anwendungen von Windows 8, in sofern sie eine installierte NVDA-Version nutzen. Dies schließt das Sprechen von eingegebenen Zeichen sowie den Lesemodus in der Metro-Version Internet Explorer 10 ein. Portable Versionen können nicht auf Metro-Anwendungen zugreifen. (#1801)
* Im Lesemodus (Internet Explorer, Firefox, etc.) können Sie nun mit den Tastenkombinationen Umschalt+, (Komma) und , (Komma) an den Anfang eines Containerobjekts bzw. hinter ein Containerobjekt springen. dies betrifft beispielsweise Listen und Tabellen. (#123)
* Neue Sprache: Griechisch.
* In Microsoft Word-Dokumenten werden nun Grafiken und deren Alternativtexte korrekt erkannt. (#2282, #1541)

### Änderungen

* Die Angabe von Zellkoordinaten in Microsoft Excel erfolgt nun *nach* dem Auslesen des Zellinhalts und erfolgt nur noch, wenn die Optionen "Tabellen ansagen" und "Zellkoordinaten in Tabellen ansagen" in den Einstellungen zur Dokument-Formatierung aktiviert sind. (#320)
* NVDA wird nunmehr in einer einzigen Datei vertrieben. Wenn sie die heruntergeladene Datei ausführen, wird eine temporäre Kopie von NVDA ausgepackt und gestartet und sie werden gefragt, ob Sie NVDAa installieren oder eine portable Version erstellen wollen. (#1715)
* NVDA wird nun immer im Ordner "Programme" installiert. Wenn eine frühere NVDA-Version in einem anderen Ordner installiert wurde, wird NVDA im Zuge der Aktualisierung nach "Programme" verschoben.

### Fehlerbehebungen

* Wenn die automatische Sprachenumschaltung aktiviert ist, werden nun auch Beschriftungen für Steuerelemente und Alternativtexte für Grafiken in Gecko-Anwendungen wie Firefox in der richtigen Sprache angesagt, sofern die Sprachenauszeichnung korrekt ist.
* Die Funktion "Alles Lesen" arbeitet nun in BibleSeeker (und anderen TRxRichEdit-Eingabefeldern) korrekt und bleibt nicht mehr mitten in der Meldung stehen.
* Listen werden in Windows 8 nun korrekt erkannt. Dies gilt für das Register Berechtigungen im Windows-Explorer sowie für Windows-Aktualisierungen.
* Problem behoben, wonach sich NVDA in Microsoft Word aufhängt, wenn es länger als zwei Sekunden gebraucht hat, um Text aus einem Dokument anzufordern (z. B. bei sehr langen Zeilen oder Inhaltsverzeichnissen). (#2191)
* Wortumbrüche werden korrekt erkannt, wenn Leerzeichen oder Tabstopps auf bestimmte Satzzeichen folgen. (#1656)
* In Adobe Reader X funktioniert nun die Navigation zu Überschriften unabhängig von der Ebene sowie die Auswahl einer Überschrift über die Elementliste. (#2181)
* Wenn Sie sich in Winamp zwischen den Einträgen im Wiedergabelisten-Editor bewegen, funktioniert nun die Braille-Ausgabe korrekt. (#1912)
* Die Baumansicht in der Elementliste im Lesemodus wird nun in der richtigen Größe angezeigt, um alle Elemente korrekt darzustellen. (#2276)
* In Anwendungen, die die Java Access Bridge verwenden, werden ausgegraute textfelder nun korrekt in Braille angezeigt. (#2284)
* In Anwendungen, die die Java Access Bridge verwenden, erscheinen bei der Anzeige von Textfeldern nun keine seltsamen Zeichen mehr. (#1892)
* In Anwendungen, die die Java Access Bridge verwenden, wird die aktuelle Zeile nun korrekt angezeigt, wenn Sie sich am Ende eines Textfeldes befinden. (#1892)
* In Anwendungen, die Gecko 14 oder neuer verwenden (wie z. B. Firefox 14) funktioniert nun die Schnellnavigation für Zitate und eingebettete Objekte korrekt. (#2287)
* Wenn sich im Internet Explorer 9 der Fokus innerhalb eines HTML-Abschnittes ("div") bewegt, der entweder hervorhebbar ist oder mit einer ARIA-Sprungmarke gekennzeichnet wurde, wird kein überflüssiger Inhalt mehr ausgegeben.
* Das Symbol für NVDA, welches auf dem Desktop sowie im Startmenü angezeigt wird, wird nun in 64-Bit-Versionen von Windows richtig dargestellt. (#354)

### Änderungen für Entwickler

* Da NSIS durch eine NVDA-interne Installationsroutine ersetzt wurde, werden die Meldungen für die Installationsroutine nun nicht mehr in einer Datei namens "langstrings.txt" gespeichert. Vielmehr werden diese nun in der Sprachdatei von NVDA integriert.

## 2012.1

Die wichtigsten Neuerungen für diese Version beinhalten Funktionen, um Braille flüssiger lesen zu können; Kennzeichnungen für Dokument-Formatierungen in Braille; Zugriff auf viel mehr Formatierungsinformationen und verbesserte Geschwindigkeit in Microsoft Word; und Unterstützung für den iTunes Store.

### Neue Features

* NVDA kann nun die Anzahl führender Tabs und Leerzeichen in der aktuellen Zeile in der Reihenfolge angeben, in der sie eingegeben wurden. Dies kann in den Einstellungen zur Dokument-Formatierung mit der Option "Zeileneinrückungen ansagen" eingestellt werden. (#373)
* NVDA kann nun Tastendrücke erkennen, die mittels Eingabeemulationen wie etwa bildschirmtastaturen oder Spracherkennungssoftware erzeugt wurden.
* Farben in Konsolenanwendungen werden nun korrekt erkannt.
* Wenn Text fett, unterstrichen oder kursiv formatiert ist, wird er nun in Braille mit Hilfe von Zeichen dargestellt, die zur aktuell eingestellten Übersetzungstabelle passen. (#538)
* In Microsoft Word werden mehr Informationen ausgegeben:
 * Zeilen-informationen wie die Nummern von Fuß- und Endnoten, Überschriftsebenen, die Existenz von Kommentaren, den Grad der Verschachtelung von Tabellen, links, sowie Textfarben;
 * Meldungen beim Betreten bzw. verlassen von Abschnitten, Kopf- und Fußzeilen, Endnoten, etc.
* Markierter Text wird nun in Braille unterstrichen mit den Punkten 7 und 8 angezeigt. (#889)
* In Braille werden nun Steuerelemente innerhalb eines Textes als solche dargestellt (wie z. B. Links, Überschriften oder Schalter. (#202)
* Unterstützung für die hedo ProfiLine und MobilLine USB Braillezeilen. (#1863, #1897)
* NVDA bricht nun standardmäßig Wörter in Braille um. Dies kann in den Braille-Einstellungen ausgeschaltet werden. (#1890, #1946)
* Text kann auf der Braillezeile Absatzweise anstatt Zeilenweise angezeigt werden. Dies erlaubt ein flüssigeres Lesen großer Textmengen. Die Einstellung kann über die Option "absatzweise lesen" in den Braille-Einstellungen konfiguriert werden. (#1891)
* Im Lesemodus können Sie nun durch einmaliges Drücken einer Routing-Taste der Braillezeile das Objekt unter dem Cursor aktivieren. Dies bedeutet, dass Sie die Routing-Taste zweimal drücken müssen, falls sich der Cursor noch nicht auf dem Objekt befindet. (#1893)
* Grundlegende Unterstützung für Internet-Bereiche in iTunes wie z. B. der Store. Andere Anwendungen, welche auf WebKit 1 beruhen, werden möglicherweise ebenfalls unterstützt. (#734)
* In Büchern in Adobe Digital Editions 1.8.1 und neuer erfolgt nun ein automatischer Seitenwechsel, wenn Sie die Funktion "Alles Lesen" verwenden. (#1978)
* Neue Braillezeichensätze: Portugiesische Kurzschrift, Isländisches 8-Punkt-Computerbraille, Tamilische Vollschrift, Spanisches 8-Punkt-Computerbraille, Persische Vollschrift. (#2014)
* In den Einstellungen für Dokument-Formatierungen kann nun eingestellt werden, ob Rahmen in Dokumenten angesagt werden sollen. (#1900)
* Bei der Verwendung von OpenBook wird automatisch der Schlafmodus aktiviert. (#1209)
* In Poedit können Übersetzer nun vom Übersetzer selbst erstellte Kommentare sowie automatisch extrahierte Kommentare lesen. Als unklar markierte oder noch nicht übersetzte Meldungen werden mit einem Stern markiert. Zudem wird ein Signalton ausgegeben, wenn Sie darauf Navigieren. (#1811)
* Unterstützung für die HumanWare Brailliant Serien BI und B Braillezeilen. (#1990)
* Neue Sprachen: Norwegisch Bokmål, Traditionelles Chinesisch (Hongkong).

### Änderungen

* Die Befehle zum Beschreiben des aktuellen Zeichens bzw. zum Buchstabieren der aktuellen Zeile und des aktuellen Wortes berücksichtigen die im Dokument hinterlegte Sprache, falls der automatische sprachenwechsel aktiviert ist.
* Die Sprachausgabe eSpeak wurde auf 1.46.02 aktualisiert.
* Wenn bei der Darstellung von Links und Grafiken der Name aus der Adresse ermittelt werden muss, werden Namen abgekürzt, die länger als 30 zeichen sind. Derart lange Namen enthalten meist nutzlose Informationen. (#1989)
* Einige neue verkürzte Klassennamen in Braille hinzugefügt (#1955, #2043)
* Wenn der System-Cursor oder der NVDA-Cursor bewegt wird, wird die Braillezeile so mitbewegt, wie wenn man die Braillezeile manuell weiterbewegen würde. Dies erleichtert das lesen, wenn die Einstellungen Absatzweise lesen und/oder der Wortumbruch aktiviert ist. (#1996)
* Die Braille-Übersetzungstabelle für spanische Vollschrift wurde aktualisiert.
* Der Braille-Übersetzer LibLouis wurde auf die Version 2.4.1 aktualisiert.

### Fehlerbehebungen

* Im Windows-Explorer in Windows 8 wird der Fokus nun nicht mehr unerwartet aus dem Suchfeld springen. Dieser Fehler machte es unmöglich, mit NVDA mit dem Windows-Suchfeld zu arbeiten.
* Optimierungen beim Lesen von und Navigieren in Microsoft Word-Dokumenten, wenn die ausgabe von Formatierungen eingeschaltet ist, sodass man konfortabel die Formatierung o. Ä. prüfen kann. Einige Benutzer werden möglicherweise eine Geschwindigkeitsverbesserung bemerken.
* Für Flash-Inhalte, die im Vollbildmodus dargestellt werden, wird nun der Lesemodus benutzt.
* Probleme mit der Klangqualität in einigen Fällen behoben, in denen als Ausgabegerät etwas anderes eingestellt ist als "Microsoft Sound Mapper". Dies betrifft vor allem Microsoft SAPI Version 5. (#749)
* Die Auswahl von "keine Sprache" im Sprachausgabendialog ist jetzt wieder möglich. Das ist nützlich, falls NVDA nur mit einer Braillezeile oder dem Sprachbetrachter als Ausgabemedium betrieben wird. (#1963)
* Die Befehle zur Objektnavigation geben nun nicht mehr "keine Kinder" bzw. "keine Eltern" aus. Die Meldungen wurden der Dokumentation angepasst. Dies gilt für die englische Benutzeroberfläche!
* Wenn in NVDA eine andere Sprache als englisch eingestellt wurde, wird der Name der Tabulator-Taste nun in der richtigen Sprache angesagt.
* In Gecko-Anwendungen wie Mozilla Firefox wird nun nicht mehr in den Lesemodus gewechselt, wenn Sie innerhalb von Dokumenten in Menüs navigieren. (#2025)
* Wenn im Rechner die Rücktaste gedrückt wird, wird nun der aktualisierte Inhalt der Anzeige angesagt und angezeigt. (#2030)
* Wenn im Lesemodus die Maus zum Navigator-Objekt gezogen wird, wird der mauszeiger nun in die Mitte des Objekts bewegt, was in manchen Fällen bessere Ergebnisse liefert. (#2029)
* Wenn im Lesemodus mit automatischem Wechsel in den Fokusmodus eine Symbolleiste den Fokus erhält, so wird der Lesemodus automatisch verlassen. (#1339)
* In iTunes sind die Informationen zur Objektposition (z. B. 1 von 5) in Listenfeldern nun wieder korrekt.
* Wenn die Option "Bei Änderungen des Fokuses automatisch den Fokusmodus einschalten" aktiviert ist, wird der Fokus-Modus korrekt für fokusierte Tabellenzeilen z. B. in ARIA-Gittern verwendet. (#1763)
* In Adobe Reader werden einige Links nicht mehr fälschlicherweise als schreibgeschützte Eingabefelder erkannt.
* Beim Lesen von Dialogfeldern werden nun keine Beschriftungen für Eingabefelder mehr einbezogen. (#1960)
* Wenn die Ansage von Objektbeschreibungen aktiviert ist, werden nun auch Beschreibungen von Gruppenfeldern vorgelesen.
* In den Laufwerks-Eigenschaften im Windows-Explorer wird nun auch die gerundete laufwerksgröße korrekt ausgelesen.
* Die doppelte Ansage von Texten auf Registerkarten wird in einigen Fällen vermieden. (#218)
* Das Verhalten in einigen Eingabefeldern wurde verbessert, bei denen der Text direkt auf den Bildschirm ausgegeben wird. Dies gilt insbesondere für den Excel-Zelleneditor und für den Nachrichteneditor in Eudora. (#1658)
* In Mozilla Firefox 11 funktioniert der Befehl "Zum Inhalt des Lesemodus zurückkehren" (NVDA+Steuerung+Leertaste) nun ordnungsgemäß und verlässt eingebettete Objekte wie Flasch-Inhalte.
* NVDA startet nun korrekt neu, wenn z. B. die eingestellte Sprache geändert und NVDA in einen Ordner installiert wurde, der keine ASCII-Zeichen enthält. (#2079)
* In Braille werden nun die Einstellungen zur Anzeige von Objektposition, Kurztasten und objektbeschreibungen berücksichtigt.
* In Mozilla-Anwendungen ist das wechseln zwischen Fokus- und Lesemodus nicht mehr so träge, wenn die Braille-Ausgabe aktiviert ist. (#2095)
* Wenn die Routing-Tasten benutzt werden, um den Cursor an ein Leerzeichen zu ziehen, das sich am Ende einer Zeile befindet, funktioniert das Routing nun korrekt; der Cursor wird nun nicht mehr an den Anfang des Textes gezogen. (#2096)
* NVDA arbeitet nun wieder korrekt mit der Sprachausgabe Audioologic TTS3. (#2109)
* Microsoft Word-Dokumente werden korrekt als mehrzeilige Eingabefelder behandelt. Dies wirkt sich vor allem auf die anzeige in Braille aus, wenn ein Word-Dokument den Fokus erhält.
* In Microsoft Internet Explorer treten keine Fehler mehr auf, wenn bestimmte seltene Elemente hervorgehoben werden.(#2121)
* Wenn ein Anwender die Aussprache von Satzzeichen und/oder Symbolen ändert, werden die Änderungen ohne Neustart von NVDA bzw. das Deaktivieren des automatischen Sprachenwechsels übernommen.
* Wenn eSpeak benutzt wird und Sie sich im Dialogfeld "Speichern unter" des Protokollbetrachters befinden, verstummt die Sprachausgabe in einigen Situationen nicht mehr. (#2145)

### Änderungen für Entwickler

* Es gibt nun eine Remote-Python-Konsole. Diese ist für Situationen gedacht, in denen es sinnvoll ist, NVDA über ein Netzwerk hinweg aus der Ferne zu warten. Weitere Informationen hierzu finden Sie im NVDA-Entwicklerhandbuch.
* Aus Gründen der besseren lesbarkeit wird beim Zurückverfolgen von Fehlern in den protokollen der Basispfad aus Dateireferenzen gestrichen. (#1880)
* TextInfo-Objekte haben nun eine Methode namens Activate(), die das Aktivieren der von textinfo zurückgegebenen Position erlaubt.
 * Dies erlaubt das Aktivieren unter Verwendung der Routing-Tasten einer Braillezeile. Hierfür könnte es jedoch in Zukunft andere Methoden geben.
* "TreeInterceptors" und "NVDAObjects", die nur eine Seite beinhalten, können automatischen Seitenwechsel während Alles Lesen unterstützen, wenn sie textInfos.DocumentWithPageTurns verwenden. (#1978)
* Einige Konstanten für Steuerelemente und ausgaben wurden umbenannt oder verschoben. (#228)
 * Die Konstanten "speech.REASON_*" wurden in die Steuerelemente verschoben.
 * Bei den Steuerelementen wurden "speechRoleLabels" und "speechStateLabel" in "roleLabels" bzw. "stateLabels" umbenannt.
* Der Text, welcher auf der Braillezeile angezeigt wird, wird ab der Protokollierungsstufe Ein- / Ausgabe protokolliert. Als erstes wird der unbehandelte Text angezeigt, gefolgt von den Braille-Modulen, die tatsächlich auf der Braillezeile angezeigt werden. (#2102)
* Unterklassen des SAPI5-Treibers können "_getVoiceTokens" überschreiben und "init" erweitern, um benutzerdefinierte "voice tokens" zu unterstützen. So kann mit "sapi.spObjectTokenCategory" eine Stimme von einem benutzerdefinierten Standort in der Registrierungsdatenbank abgerufen werden.

## 2011.3

Die wichtigsten neuerungen sind u. a. das automatische Wechseln der Synthesizersprache passend zur Dokumentsprache; Unterstützung für 64-Bit-Java-Laufzeitumgebungen; Angabe von Textformatierungen im Lesemodus in Mozilla-Gecko-Anwendungen; Bessere Behandlung von Programmabstürzen; sowie anfängliche Unterstützung für Windows 8.

### Neue Features

* NVDA kann nun die Stimmen von eSpeak passend zur Dokumentsprache einstellen. Dies gilt für Web- und Pdf-Dokumente. Die Automatische Umschaltung von Sprachen und Dialekten kann über das Dialogfeld für die Stimmen-Einstellungen konfiguriert werden. (#845)
* Java Access Bridge 2.0.2 wird unterstützt, dies betrifft auch 64-Versionen der Java-Laufzeitumgebung.
* Wenn Sie in Mozilla-Gecko-Anwendungen (wie z. B. Firefox) die Objektnavigation verwenden, werden nun auch die Überschriftsebenen angegeben.
* Wenn Sie in Mozilla-Anwendungen den Lesemodus verwenden, können nun ach Informationen zur Dokument-Formatierung abgerufen werden. (#394)
* Unterstrichener oder Durchgestrichener Text kann nun in Standard-IAccessible2-Textfeldern wie in Anwendungen von Mozilla erkannt und wiedergegeben werden.
* Im Adobe Reader wird nun im Lesemodus die anzahl von Spalten und Zeilen von Tabellen angegeben.
* Unterstützung für Microsoft Speech Platform-Sprachausgaben hinzugefügt. (#1735)
* Zeilen- und Seitennummern werden nun am Cursor in IBM Lotus Symphony angesagt. (#1632)
* Das Maß, in dem die Stimme bei Großbuchstaben angehoben werden soll, kann nun im Dialogfeld "Stimmen-Einstellungen" konfiguriert werden. Die Angabe erfolgt hier in Prozent. Dies ersetzt das alte Kontrollkästchen "Stimme bei Großbuchstaben anheben". Um die Funktion abzuschalten, geben Sie einen wert von 0 an. (#255)
* Text- und Hintergrundfarbe werden nun mit angesagt, wenn man sich in Microsoft Excel die Formatierung der Zellen ansagen lässt. (#1655)
* In Anwendungen, in welchen die Java Access Bridge Verwendung findet, funktioniert nun der Befehl "Aktuelles Navigator-Objekt aktivieren" auf passenden Elementen. (#1744)
* Sprache Tamilisch hinzugefügt.
* Grundlegende Unterstützung für Design Science MathPlayer.

### Änderungen

* NVDA wird sich selbst neu starten, wenn es abstürzt.
* Einige Informationen, welche in Braille angezeigt werden, wurden abgekürzt.. (#1288)
* Das Skript zum Lesen des aktiven Fensters wurde verbessert. Nun werden nutzlose Informationen ausgefiltert. (#1499)
* Im Dialogfeld für den Lesemodus kann nun eingestellt werden, ob ein virtuelles Dokument nach dem Laden automatisch gelesen werden soll. (#414)
* Wenn Sie versuchen, die statuszeile auszulesen (beispielsweise mit der Tastenkombination NVDA+Ende) und es existiert keine Statuszeile, so wird die unterste Zeile des Hauptfensters der aktiven Anwendung ausgelesen. (#649)
* Wenn Sie im lesemodus ein virtuelles Dokument über die Funktion "Alles Lesen" lesen, wird NVDA nun nach Überschriften eine Pause einlegen, anstatt die Überschrift zusammen mit dem nachfolgenden Text als einen langen Satz zu lesen.
* Wenn Sie im Lesemodus auf einer Registerkarte die Leer- oder Eingabetaste drücken, wird diese aktiviert, anstatt in den Fokusmodus zu wechseln. (#1760)
* Sprachausgabe eSpeak auf Version 1.45.47 aktualisiert.

### Fehlerbehebungen

* Im Internet Explorer und anderen MSHTML-Dokumenten werden nun keine Numerierungen oder Aufzählungszeichen mehr angezeigt, wenn der Autor des Dokuments dies ausdrücklich untersagt hat (beispielsweise durch setzen des Attributes "Style" auf "none") (#1671)
* Wenn Sie NVDA neu starten (beispielsweise durch Drücken von Strg+Alt+N wird die laufende Instanz ordnungsgemäß geschlossen, bevor eine neue gestartet wird.
* Das Drücken der Pfeiltasten oder der Rücktaste führt nun nicht mehr zu unerwarteten Ergebnissen. (#1612)
* In Kombinationsfeldern, die keine Texteingabe erlauben und UIA verwenden, wird nun der aktuell ausgewählte Eintrag korrekt angegeben.
* Im Adobe Reader können sie nun innerhalb einer Tabelle von der Überschrift aus zur nächsten Zeile (und umgekehrt) navigieren, indem Sie die Tabellennavigationsbefehle verwenden. Die Überschriften werden auch nicht mehr als "Zeile 0" angegeben. (#1731)
* Im Adobe Reader kann jetzt im Lesemodus auch auf leere Tabellenzellen (und darüber hinaus) navigiert werden.
* In Braille werden keine Positionsangaben mehr ausgegeben, die ins Leere führen (wie z. B. 0 von 0 Ebene 0)
* Wenn die Braillezeile an den Navigator gekoppelt wird, ist sie nun in der Lage, auch Informationen im Flächenmodus anzuzeigen. (#1711)
* In Braille wird nun der Inhalt von Textfeldern nicht mehr doppelt angezeigt (Beispielsweise wenn Sie in wordpad zurückscrollen).
* Wenn Sie im Internet Explorer auf einem Schalter zum Hochladen einer datei die Eingabetaste drücken, wird nun korrekterweise das Dialogfeld zur Datei-Auswahl angezeigt, anstatt einfach in den Fokusmodus zu wechseln.(#1720)
* Wenn der Schlafmodus für eine Konsolenanwendung aktiviert ist, wird nun kein dynamischer Inhalt mehr wiedergegeben. (#1662)
* Im Lesemodus wurde das Verhalten von alt+Pfeil ab oder alt+Pfeil auf zum Öffnen und Schließen von Kombinationsfeldern verbessert. (#1630)
* In nicht mehr reagierenden Anwendungen kann sich NVDA nun in viel mehr Fällen wiederherstellen, welches früher zum kompletten Absturz von NVDA führte. (#1408)
* NVDA wird nun nicht mehr im Firefox an Elementen scheitern, die als display:table ausgewiesen sind. (#1373)
* NVDA gibt nun keine Beschriftungen mehr aus, wenn diese den Fokus erhalten. dies verhindert die doppelte ausgabe der Beschriftungen mancher Steuerelemente in Firefox und Internet Explorer. (#1650)
* NVDA liest nun in Excel Zellen korrekt aus, die mit Strg+V eingefügt wurden. (#1781)
* Wenn Sie sich im Adobe Reader auf ein Steuerelement bewegen, das sich auf einer anderen Seite befindet, werden nun keine störenden Informationen mehr ausgegeben. (#1659)
* In Mozilla-Anwendungen werden nun Umschalter korrekt erkannt, wenn sie den lesemodus verwenden. (#1757)
* In der Entwicklervorschau von Windows 8 wird nun die Addressleiste im Explorer korrekt erkannt.
* In der Entwicklervorschau von Windows 8 wird Wordpad nun nicht mehr abstürzen.
* Wenn in Gecko 10 (z. B. Firefox 10) eine Seite mit einem Zielanker geladen wird, wird der Cursor nun richtig positioniert. (#360)
* In Gecko-Anwendungen wie Firefox werden nun Beschriftungen von Image-map-links korrekt verarbeitet.
* Wenn Sie bei aktivierter mausverfolgung den Mauszeiger in ein Eingabefeld bewegen (wie z. B. in den Einstellungen für Synaptics Pointing Device oder SpeechLab SpeakText) bringt NVDA die Anwendung nicht mehr zum Absturz (#672)
* NVDA wertet nun die Dialogfelder für die Infos zahlreicher Anwendungen korrekt aus, die mit Windows XP mitgeliefert werden, wie z. B. das Info-Dialogfeld des Editors oder von Windows. (#1853, #1855)
* Wortweise Navigation in Eingabefeldern behoben. (#1877)
* Wenn Sie sich mit Pfeil nach links, Pfeil nach oben oder seite rauf aus einem Eingabefeld bewegen, während Sie sich im Fokus Modus befinden, wächselt NVDA nun richtig in den Lesemodus, wenn "Bei Bewegungen des System-Cursors automatisch den Fokusmodus einschalten" aktiviert ist. (#1733)

### Änderungen für Entwickler

* NVDA kann nun Sprachausgaben anweisen, die Sprache in bestimmten Textpassagen zu wechseln.
 * um dies zu unterstützen, müssen die Treiber speech.LangChangeCommand in Sequenzen verarbeiten, die über den Befehl SynthDriver.speak() an den Synthesizer übergeben werden.
 * SynthDriver -Objekte sollten zudem das Attribut language als argument an VoiceInfo-objekte übergeben (oder das language-Attribut überschreiben, um die aktuelle Sprache abzufragen). Andernfalls wird die in NVDA eingestellte sprache für die Benutzeroberfläche verwendet.

## 2011.2

Die wichtigsten Neuerungen in dieser Version beinhalten umfangreiche Verbesserungen im Bereich der Satzzeichen und Symbole, einschließlich einstellbarer Ebenen, selbstwählbare Bezeichnungen und phonetisches Buchstabieren; keine Pausen am Zeilenende während Alles Lesen; verbesserte Unterstützung für ARIA im Internet Explorer; verbesserte Unterstützung für XFA/LiveCycle PDF dokumente in Adobe REader; Zugriff auf Text, der auf den Bildschirm geschriben wurde in mehr Anwendungen; und Zugriff auf Farb- und Formatierungsinformationen für text, der auf den Bildschirm geschrieben wurde.

### Neue Features

* Sie können sich nun jedes Zeichen phonetisch buchstabieren lassen, indem sie die Tastenkombination zum Ansagen des aktuellen Zeichens zweimal schnell hintereinander drücken. Für den deutschsprachigen Raum wird hierbei das deutsche Buchstabieralphabet nach DIN 5009 verwendet. (55)
* In Anwendungen wie Mozilla Thunderbird, die ihre Ausgaben direkt auf den Bildschirm schreiben, wird nun im Flächenmodus mehr Text angezeigt.
* Sie können nun zwischen mehreren Ausführlichkeitsstufen für Satzzeichen und Sonderzeichen wählen. (#332)
* Wenn ein Satzzeichen oder Symbol öfter als viermal auftaucht, wird die Anzahl der Zeichen angegeben, anstatt die Zeichen zu wiederholen. (#43)
* Neue Braille-Übersetzungstabellen: Norwegisches 8-Punkt-Braille, Ethiopische Vollschrift, Slovenische Vollschrift, Serbische Vollschrift. (#1456)
* Bei der Verwendung des Befehls "Alles Lesen" macht die Sprachausgabe keine unnatürlichen Pausen mehr. (#149)
* NVDA sagt nun an, wenn ettwas sortiert wurde (gemäß der "aria-sort-Richtlinie) in Internetbrowsern. (#1500)
* Braillezeichen im Unicode-Format werden jetzt auf der Braillezeile richtig angezeigt. (#1505)
* Wenn sich der Fokus im Internet Explorer und anderen MSHTML-Dokumenten über eine Gruppe von Elementen bewegt, welche von einem Attribut "fieldset" umgeben ist, sagt NVDA den Namen der Gruppe, also die Legende an. (#535)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden jetzt die Eigenschaften "aria-labelledBy" und "aria-describedBy" beachtet.
* Im Internet Explorer und anderen mshtml-Steuerelementen wurde die Unterstützung für ARIA-listen, Aria-Tabellenzellen, Schieberegler und Fortschrittsbalken verbessert.
* Anwender können nun die Aussprache von Satzzeichen und anderen Symbolen ändern, so wie die Symbolebene, ab welcher sie angesagt werden. (#271, #1516)
* In Microsoft Excel wird nun der Name des aktiven Blattes angesagt, wenn sie mit Steuerung+Bild auf bzw. Steuerung+Bild ab zwischen den Blättern wechseln. (#760)
* Beim Navigieren in Microsoft Word-Tabellen mit der Tabulator-Taste, wird NVDA nun die aktuelle Zelle ansagen, wenn sie sich bewegen. (#159)
* Sie können nun im Dialogfeld für die Dokument-Formatierungen einstellen, ob Tabellen-Koordinaten angesagt werden sollen. (#719)
* NVDA kann nun auf Farb- und Formatierungsinformationen von Texten zugreifen, welche direkt ausgegeben wurden.
* In der Nachrichtenansicht von Outlook Express/Windows Mail/Windows Live Mail sagt NVDA nun an, wenn eine Nachricht ungelesen und im Falle einer Nachrichtenkonversation ausgeklappt oder zusammengeschoben ist. (#868)
* eSpeak hat nun eine Einstellung namens Stimmgeschwindigkeit erhöhen, welche die Stimmgeschwindigkeit verdreifacht.
* Unterstützung für die Kalender-Einstellungen im Dialogfeld "Datum und Uhrzeit", erreichbar über die Windows-7-Uhr. (#1637)
* Zusätzliche Tastenkürzel für die Braillezeile Lilli der Firma MDV hinzugefügt. (#241)
* Neue Sprachen: Bulgarisch und Albanisch.

### Änderungen

* Um den System-Cursor zum NVDA-Cursor zu bewegen, führen Sie die Funktion "Fokus zum Navigator ziehen" (desktop NVDA+Umschalt+Nummernblock Minus, Laptop NVDA+Umschalt+Rücktaste) zwei Mal aus. Dies gibt mehr Tastenkombinationen für die künftige Verwendung frei. (#837)
* Um den dezimalen und hexadezimalen Code eines Zeichens zu erfahren, müssen Sie die Funktion "aktuelles zeichen ansagen" nun dreimal ausführen, da zweimaliges Ausführen die phonetische Beschreibung wiedergibt.
* Die Sprachausgabe eSpeak wurde auf 1.45.03 aktualisiert. (#1465)
* Layout-Tabellen werden im Mozilla Gecko-Anwendungen nicht mehr angesagt, während man sich im Fokus-Modus befindet und den Fokus bewegt bzw. außerhalb eines Dokuments.
* In Internet Explorer und anderen MSHTML-Dokumenten funktioniert der Lesemodus nun auch innerhalb von ARIA-Anwendungen. (#1452)
* Der Braille-Übersetzer LibLouis wurde auf 2.3.0 aktualisiert.
* Wenn Sie bei aktiviertem LeseModus mit Hilfe der Schnellnavigation zu einem Steuerelement wechseln, wird dessen Beschreibung ausgegeben, falls vorhanden.
* Ansage der Fortschrittsbalken im Lesemodus.
* Alle Elemente, die in Internet Explorer oder anderen mshtml-Dokumenten mit dem Aria-Attribut presentation gekennzeichnet sind, werden nun beim Navigieren im vereinfachten Modus oder im Fokusmodus ausgefiltert.
* In Dokumentation von NVDA und in der oberfläche ist nun nicht mehr die Rede von virtuellen Puffern oder virtuellen Ansichten, sondern allenfalls noch vom Lesemodus, da der Begriff virtuelle Puffer oder virtuelle ansichten für normale anwender bedeutungslos ist. (#1509)
* Wenn Sie ihre benutzerdefinierten Einstellungen systemweit übernehmen wollen und ihr Konfigurationsverzeichnis enthält eigene Plug-ins, werden Sie nun darauf hingewiesen, dass das systemweite Übernehmen dieser Plug-ins ein sicherheitsrisiko darstellt. (#1426)
* Wenn Sie sich anmelden, wird der NVDA-Dienst NVDA nun nicht mehr starten und beenden.
* Auch wenn die UIA in Windows XP und Windows Vista über eine Aktualisierung nachinstalliert werden kann, macht NVDA unter diesen Systemen keinen Gebrauch davon. Obwohl die Verwendung der UIA die Zugänglichkeit moderner Anwendungen verbessert, kommt es unter Windows XP und Windows Vista sehr oft zu Abstürzen oder Leistungseinbußen. (#1437)
* In Anwendungen, die Gecko 2 und neuer verwenden (z. B. Firefox 4 und neuer) kann ein Dokument nun gelesen werden, noch bevor es vollständig geladen wurde.
* NVDA teilt nun den Status eines Containers mit, sobald sich der Fokus auf ein Steuerelement innerhalb eines Containers bewegt. Wenn Sie z. B. in ein HTML-Dokument springen, noch bevor es vollständig geladen wurde, wird dessen Status als "Beschäftigt" angezeigt.
* Die Benutzeroberfläche und die Dokumentation von NVDA verwenden nun nicht mehr die Begriffe "erstes Kind-Objekt" und "ElternObjekt", da diese im Zusammenhang mit objektnavigation verwirrend sein können.
* Der Status "reduziert" wird nun nicht mehr für Menüpunkte angezeigt, die ein Untermenü besitzen.
* Das Skript "reportCurrentFormatting" (NVDA+F) zeigt nun nicht mehr die Formatierungen am System-cursor, sondern die formatierungen am NVDA-Cursor an. Die meisten Anwender werden keinen Unterschied bemerken, weil der NVDA-Cursor standardmäßig dem System-Cursor folgt. Jetzt ist es jedoch möglich, z. B. im Flächenmodus die Formatierungen bestimmter Bildschirmbereiche abzufragen.

### Fehlerbehebungen

* Wenn Sie mit NVDA+Leertaste den Fokus-modus erzwungen haben und ein Kombinationsfeld schließen, wird nun nicht mehr zurück in den Lesemodus gewechselt (#1386)
* In Gecko-/MShtml-Dokumenten (Firefox bzw. Internet Explorer) wird nun Text korrekt verarbeitet, wenn er auf einer einzigen Zeile steht. Bisher wurde solcher Text immer auf mehrere zeilen verteilt. (#1378)
* Wenn die Braillezeile an den Navigator gekoppelt wird und der Navigator auf einen virtuellen Puffer bewegt wird (entweder manuell oder durch eine Fokusänderung), wird nun der Inhalt des virtuellen Puffers korrekt dargestellt. (#1406, #1407)
* Wenn die aussprache von Satzzeichen deaktiviert ist, kommt es nun nicht mehr zu falsch ausgesprochenen Satzzeichen bei der Verwendung einiger Sprachausgaben. (#332)
* Wenn Sie einen Sprachsynthesizer verwenden, der keine Stimmen-Einstellungen unterstützt (so z. B. audiologic tts3), kommt es nun nicht mehr zu Problemen beim Laden der Konfiguration. (#1347)
* Das Skype-Menü Extras wird nun richtig gelesen. (#648)
* Wenn Sie unter Windows Vista oder unter Windows 7 mit aktiviertem Aero in den Maus-Einstellungen das Kontrollkästchen "Lautstärke der Audiokoordinaten durch Helligkeit kontrollieren" aktiviert haben, sollte es nun nicht mehr zu Problemen kommen. (#1183)
* Bei Verwendung des Laptop-Tastaturschemas arbeitet die Tastenkombination NVDA+Entf jetzt wie dokumentiert und gibt die Größe und Position des aktuellen Navigator-Objekts zurück. (#1498)
* NVDA verarbeitet nun das "aria-selected"-Attribut korrekt.
* Wenn vom Lesemodus in den Fokusmodus gewechselt wird und sich der Fokus auf einem Formularfeld befindet, wird dieses im richtigen Kontext angezeigt. Wenn Sie sich z. B. auf einem Listeneintrag befinden, wird zuerst der name der Liste angezeigt. (#1491)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden Listen nun korrekt als solche behandelt (und nicht als Listeneinträge).
* Wenn ein schreibgeschütztes Eingabefeld den Fokus bekommt, wird es nun korrekt als schreibgeschützt gemeldet. (#1436)
* Im Lesemodus behandelt NVDA schreibgeschützte Eingabefelder nun korrekt.
* Im Lesemodus schaltet NVDA nun nicht mehr in den Fokusmodus um, wenn "aria-activedescendant" gesetzt ist; z. B. wenn die Liste mit den Einträgen zur autovervollständigung bei einem Eingabefeld erscheint, das dies unterstützt).
* Im Adobe Reader werden nun die namen von Steuerelementen korrekt angezeigt, wenn Sie sich im Lesemodus mit Hilfe der Schnellnavigationstasten zwischen ihnen bewegen.
* In XFA-PDF-Dokumenten werden Schalter, Links und Grafiken nun korrekt verarbeitet.
* In XFA-Dokumenten werden nun alle Elemente auf separaten Zeilen dargestellt. Dies wurde eingeführt, da in pdf-Dokumenten manchmal jegliche Strukturen fehlen und dann große Abschnitte oder sogar das gesammte Dokument sonst auf einer einzigen Zeile dargestellt wird.
* Probleme beim Wechsel zu Eingabefeldern in XFA-Pdf-Dokumenten behoben.
* Änderungen in Kombinationsfeldern in XFA-pdf-Dokumenten werden nun korrekt angezeigt.
* Benutzerdefinierte Kombinationsfelder wie z. B. die in Outlook Express, sind nun zugänglich. (#1340)
* In Sprachen, in denen ein Leerzeichen als Tausendertrennzeichen verwendet wird (wie z. B. Französisch oder deutsch) werden die Ziffern nicht mehr zusammengezogen, wenn sie sich auf unterschiedliche Textteile verteilen. Dies war bisher in Tabellenzellen problematisch, die Zahlen enthielten. (#555)
* Im Internet Explorer oder anderen MSHTML-Dokumenten werden Elemente, bei denen per Aria der Typ "Beschreibung" festgelegt wurde, nicht mehr als Eingabefelder, sondern als statischer Text behandelt.
* Verschiedene Probleme behoben, die beim Wechsel von einem virtuellen Dokument in die Adressleiste auftraten. (#720, #1367)
* Wenn Sie beim Lesen von Text auf eine Liste stoßen, sagt NVDA nun z. B. "Liste mit 5 Einträgen" statt "Listemit 5 Einträgen" (#1515)
* Wenn die Eingabehilfe aktiviert ist, werden auch diejenigen Eingabemethoden protokolliert, die die Eingabehilfe passieren (wie z. B. die Navigationstasten zum Brailezeilenlängenweisen Navigieren).
* Wenn bei aktivierter Eingabehilfe eine Umschalttaste gedrückt gehalten wird, wird diese nicht mehr als Modifikator behandelt, der sich selbst modifiziert (wie z. B. NVDA+NVDA).
* Die Schnellnavigation in Adobe Reader funktioniert nun auch für Konbinationsfelder.
* Der Zustand "ausgewählt" wird nun auch für Tabellen korrekt ausgegeben (ähnlich wie bei Listen oder Baumstrukturen)..
* Im Lesemodus können im Firefox nun selbst dann Steuerelemente aktiviert werden, wenn sie sich außerhalb des Bildschirms befinden. (#801)
* Wenn ein Meldungsfenster angezeigt wird, können Sie nun keine NVDA-Einstellungsdialoge mehr aufrufen, weil sich die Einstellungsdialoge sonst festfahren. (#1451)
* In Microsoft Excel fährt sich NVDA nun nicht mehr fest, wenn sie die Tasten(kombinationen) zum Navigieren zwischen bzw. zum Markieren von Zellen in Dauerfunktion verwenden.
* Problem behoben, wonach sich der NVDA-Dienst in sicheren Desktops beendet hat.
* Problem behoben, wonach manchmal der Gesamte Text von der Braillezeile verschwand, wenn er sich auf dem Bildschirm geändert hat. (#1377)
* Das Fenster mit heruntergeladenen und herunterladenden Dateien im Internet explorer 9 kann nun mit NVDA gelesen werden. (#1280)
* Es ist nun nicht mehr möglich, versehentlich mehrere NVDA-Instanzen zu starten. (#507)
* Auf langsamen Systemen zeigt NVDA nun nicht mehr sein Hauptfenster ständig an. (#726)
* Beim Start von WPF-Anwendungen unter Windows XP stürzt NVDA nun nicht mehr ab. (#1437)
* Die Funktionen zum Lesen eines kompletten Dokuments arbeiten nun auch bei Verwendung von UIA korrekt (z. B. in XPS-Dokumenten)
* In einigen Listenfeldern in Outlook Express oder Windows Live Mail (wie z. B. in der Liste der Nachrichtenregeln) werden nun die Kontrollfelder korrekt angezeigt. (#576)
* Kombinationsfeldern wird nun nicht mehr unterstellt, sie hätten ein Untermenü.
* NVDA zeigt nun die Empfänger in den Feldern "Kopie" und "Blindkopie" korrekt an. (#421)
* Problem behoben, wonach im Dialogfeld für die Stimmen-Einstellung manchmal die Bildlaufleisten nicht richtig angezeigt wurden, wenn man Einstellungen geändert hat (#1411)
* NVDA zeigt nun die neue ausgewählte Tabellenzelle korrekt an, nachdem Sie Inhalte über die Zwischenablage ausgeschnitten oder eingefügt haben. (#1567)
* Wenn im Internet Explorer oder anderen MSHTML-Dokumenten eingebettete Rahmen mit dem ARIA-Attribut "presentation" gekennzeichnet sind, werden diese nun korrekt angezeigt. (#1569)
* Problem behoben, wonach im Internet Explorer und anderen MSHTML-Dokumenten der Fokus ständig zwischen dem virtuellen Dokument und einem mehrzeiligen Eingabefeld wechselte. (#1566)
* In Microsoft Word 2010 liest NVDA nun Bestätigungsdialoge automatisch vor. (#1538)
* Wenn Sie in Internet Explorer oder anderen MSHTML-Dokumenten in mehrzeiligen Eingabefeldern Text unterhalb der ersten Zeile markieren, wird dies korrekt erkannt. (#1590)
* die wortweise Navigation wurde verbessert; dies betrifft den Lesemodus sowie etliche Eingabefelder. (#1580)
* Wenn Sie NVDA auf einer Hongkong-Version von Windows Vista oder Windows 7 installieren, zeigt das Installationsprogramm nun keinen unsinnigen Text mehr an. (#1596)
* Das laden von SAPI5-stimmen funktioniert nun auch dann korrekt, wenn zwar die Einstellungen für SAPI5 als Sprachausgabe, jedoch keine Stimmenenstellungen im benutzerspezifischen Konfigurationsverzeichnis existieren. (#1599)
* NVDA fährt sich im Internet explorer oder anderen mshtml-Dokumenten nun nicht mehr in Eingabefeldern fest, wenn Braille aktiviert ist.
* Im Firefox werden nun auch HTML-Elemente mit dem ARIA-Typ "presentation" berücksichtigt.
* In Microsoft Word werden nun auch die Seiten 2 und folgende in Braille korrekt angezeigt. (#1603)
* In Microsoft Word kann jetzt auch Text korrekt in Braille gelesen werden, der in einer Sprache mit Rechts-Links-Ausrichtung geschrieben ist (#627)
* In Microsoft Word arbeitet die funktion zum Lesen eines kompletten Dokumentes jetzt korrekt, wenn das Dokument nicht mit einem abgeschlossenen Satz endet.
* In Windows Live Mail 2011 können nun auch Textnachrichten korrekt gelesen werden.
* In den Dialogen zum Verschieben und kopieren fährt sich NVDA nun nicht mehr fest. (#574)
* NVDA wird nun den Fokus in der Nachrichtenliste von Outlook 2010 korrekt verfolgen. (#1285)
* einige Probleme beim Verbinden der MDV Lili-Braillezeile über USB behoben. (#241)
* Im Internet Explorer und anderen MSHTML-Dokumenten werden nun Leerzeichen, die auf Links folgen, nicht mehr ignoriert.
* Im Internet Explorer und anderen MSHTML-Dokumenten wurden unnötige Zeilenumbrüche entfernt, insbesondere erzeugen html-Elemente mit dem Attribut display=none keinen Zeilenumbruch mehr. (#1685)
* Wenn NVDA nicht starten kann und die Wiedergabe des Klangs für kritische Fehler nicht möglich ist, wird keine Fehlermeldung mehr in die Protokolldatei geschrieben.

### Änderungen für Entwickler

* Entwicklerdokumentation kann nun unter Verwendung von SCons generiert werden. Lesen Sie mehr dazu in der Readme.txt im Stammverzeichnis der Quellcode-Distribution.
* In den unterschiedlichen Sprachräumen können jetzt Beschreibungen für Sonderzeichen bereitgestellt werden. Sehen Sie sich den Abschnitt "Beschreibungen der Sonderzeichen" im NVDA-Entwicklerhandbuch an. (#55)
* In den einzelnen Sprachräumen können nun Regeln für die aussprache von Satzzeichen und anderen Symbolen bereitgestellt werden. Sehen Sie sich den Abschnitt "Aussprache von Symbolen" im NVDA-Entwicklerhandbuch an. (#332)
* Der NVDAHelper kann nun so erstellt werden, dass er zahlreiche Informationen zur Fehlerbehebung enthält. Verwenden Sie hierfür die SCons-variable nvdaHelperDebugFlags. Weitere Informationen hierzu finden Sie in der Datei readme.txt im Stammverzeichnis des Quellcodes (#1390).
* Sprachausgabentreiber übergeben den sprachausgaben nun eine Folge von Befehlen, um die sprachausgabe zusteuern, anstatt einen einfachen Index zu übergeben.
 * Dies erlaubt eingebettete Indizes, Änderungen von Stimmenparametern, etc.
 * Treiber sollten nun SynthDriver.speak() anstelle von SynthDriver.speakText() und SynthDriver.speakCharacter() implementieren.
 * Die alten Methoden werden zwar im Moment noch unterstützt, werden jedoch in zukünftigen Versionen entfernt.
* gui.execute() wurde entfernt. stattdessen sollte wx.CallAfter() verwendet werden.
* gui.scriptUI wurde entfernt.
 * Verwenden Sie für Meldungsfenster wx.CallAfter(gui.messageBox, ...).
 * Für andere Dialoge sollten echte wx Dialoge verwendet werden.
 * Eine neue Funktion gui.runSkriptModalDialog() vereinfacht das Verwenden modaler Dialogfenster innerhalb von Skripten.
* Sprachausgabentreiber unterstützen nun boolsche Eigenschaften. Siehe SynthDriverHandler.BooleanSynthSetting.
* Scons akzeptiert nun eine Variable namens certTimestampServer, die die Adresse eines Timestamping-Servers enthält, um authenticode-signatures mit einem Zeitstempel zu versehen. (#1644)

## 2011.1.1

Dieses Release behebt wichtige Fehler und Sicherheitsprobleme, welche in NVDA 2011.1 gefunden wurden.

### Fehlerbehebungen

* Der Eintrag "Spenden" im Menü ist nun bei sonstigen Sicherheitshinweisen, im Windows Anmeldebildschirm sowie u. a. der Benutzerkontensteuerung ausgeblendet. Dies stellte ein Sicherheitsrisiko dar. (#1419)
* Es ist nun nicht länger möglich die benutzerdefinierte Konfiguration von NVDA während dieser Sicherheitsebenen zu kopieren oder einzufügen. Dies stellt ebenso ein Sicherheitsrisiko dar. (#1421)
* In Firefox 4 funktioniert nun der Befehl `NVDA+Strg+Leertaste` für die eingebetteten Inhalte in der Virtuellen Ansicht. (#1429)
* Bei aktivierter Ansage der Funktionstasten werden nun die großgeschriebenen Zeichen nicht länger falsch angesagt. (#1422)
* Wenn bei aktivierter Ansage der Funktionstasten die Leertaste mit der NVDA-Taste gedrückt wird, wird nun nicht mehr die Taste umgeschaltet, sondern dies auch mitgeteilt. (#1424)
* Die Protokollierungsfunktion wurde bei der Windows-Anmeldung und in sämtlichen Dialogen der Sicherheitshinweisen sowie der Benutzerkontensteuerung und Dialogfeld zum Sperren des Computers komplett ausgeschaltet. Dies stellte ein Sicherheitsrisiko dar. (#1435)
* Bei aktivierter Eingabehilfe werden nun alle Eingaben protokolliert, auch wenn sie nicht an ein Skript zugewiesen wurden. (#1425)

## 2011.1

Zu den wichtigsten Neuerungen gehören das Anzeigen von Farben, sowie die automatische Anzeige von neu erscheinendem Text in mIRC, PuTTY, Tera Term und SecureCRT;
Unterstützung globaler Erweiterungen; die korrekte Anzeige von Aufzählungen und Numerierungen in Microsoft Word; zusätzliche Tastenzuweisungen für Braillezeilen, einschließlich Tasten zum Bewegen zur nächsten/vorigen Zeile; sowie Unterstützung von Braillezeilen von Baum, HumanWare und APH.

### Neue Features

* Die Ausgabe von Farben bei der Angabe der Textformatierung wird nun unterstützt (sowohl automatisch, einstellbar in den Einstellungen zur Dokument-Formatierung) als auch manuell (über die Tastenkombination NVDA+F. Dies betrifft IAccesible-Eingabefelder (wie z. B. in Mozilla-Anwendungen), Richedit-Eingabefelder (wie z. B. in Wordpad) soie Eingabefelder in IBM Lotus Symphony.
* Nun kann in virtuellen Ansichten seitenweise (Umschalt+Seite nach oben/Seite nach unten) oder absatzweise (Umschalt+Strg+Pfeil nach oben/Pfeil nach unten) markiert werden. (#639)
* NVDA zeigt nun neu erscheinenden Text in Terminalfenstern korrekt an. Dies betrifft u. a. mIRC, PuTTY, Tera Term und SecureCRT. (#936)
* Nun kann der Anwender neue NVDA-Tastenkombinationen hinzufügen oder vorhandene ersetzen, in dem er eine einfache Zuordnung von Benutzereingaben bereitstellt. (#194)
* Unterstützung für globale Plugins. Diese können verwendet werden, um NVDA mit neuen Funktionen anwendungsübergreifend zu erweitern. (#281)
* Sie hören jetzt einen kurzen Signalton, wenn die Dauergroßschreibung aktiv ist und Sie Buchstaben mit der Umschalttaste schreiben. Dies kann in der neuen Option in den Tastatur-Einstellungen ausgeschalten werden. (#663)
* Harte Seitenumbrüche werden nun beim zeilenweisen Navigieren in Microsoft Word angesagt. (#758)
* Aufzählungszeichen und Nummerierungen werden nun beim zeilenweisen Navigieren in Microsoft Word angesagt, (#208)
* Es gibt jetzt einen Befehl, um einen "Schlafmodus" für die Aktuelle Anwendung ein- oder auszuschalten (NVDA+Umschalt+S). Der Schlafmodus (bisher bekannt als "Eigene Sprachunterstützung" schaltet innerhalb der aktuellen Anwendung alle Funktionen des Screenreaders ab. Dies ist vorallem nützlich für Anwendungen, die ihre eigene Screenreader- und Sprachfunktionen zur Verfügung stellen. Führen Sie diesen Befehl erneut aus, um den "Schlafmodus" abzuschalten.
* Es wurden einige weitere Zuordnungen der Tasten für Braillezeilen hinzugefügt. Weitere Informationen finden Sie im Handbuch im Kapitel "Unterstützte Braillezeilen". (#209)
* Um Drittentwicklern die Arbeit zu erleichtern, können jetzt sowohl Anwendungsmodule als auch globale Erweiterungen neu geladen werden, ohne dass NVDA neu gestartet werden muss. Verwenden Sie hierzu den Befehl "Plugins neu laden" aus dem Menü "Extras" oder drücken Sie die Tastenkombination NVDA+Strg+F3. (#544)
* NVDA merkt sich nun die aktuelle Position, wenn Sie in einem Web-Browser zur letzten besuchten Seite wechseln. Dies gilt so lange, bis Sie entweder NVDA oder den Browser beenden. (#132)
* Braillezeilen von HandyTech nun auch verwendbar ohne Installation des Universaltreibers. (#854)
* Unterstützung für mehrere Braillezeilen von Baum, HumanWare und APH. (#937)
* Die Statuszeile in Media Player Classic Home Cinema wird nun erkannt.
* Die Focus 40 Blue von Freedom Scientific kann nun auch verwendet werden, wenn Sie per Bluetooth verbunden wird. (#1345)

### Änderungen

* Standardmäßig werden Positionsinformationen nicht mehr angezeigt, weil sie in einigen Anwendungen normalerweise nicht korrekt sind; wie z. B. in den meisten Menüs, in der Symbolleiste "Ausgeführte Anwendungen", im Infobereich, etc. Sie können die Positionsangaben jedoch wieder mit Hilfe einer zusätzlichen Option im Dialogfeld "Objektpräsentation" aktivieren.
* Die Tastaturhilfe wurde in "Eingabehilfe" umbenannt, um dem Umstand Rechnung zu tragen, dass nun auch Eingaben von anderen Quellen als der Tastatur verarbeitet werden.
* Die Eingabehilfe zeigt nun nicht mehr den Speicherort eines Skriptes mittels Sprache und Brailleausgabe an, da dieser für den Anwender kryptisch und irelevant ist. Der Speicherort wird dennoch für Entwickler und erfahrene Anwender mitprotokolliert.
* Wenn NVDA erkennt, dass es "sich aufgehängt hat", werden weiterhin NVDA-Tasten verarbeitet, auch wenn alle anderen Tastenkombinationen an das System weitergereicht werden. Dies verhindert, dass der Anwender unabsichtlich z. B. die Dauergroßschreibung umschaltet. (#939)
* Wenn nach der Verwendung des Kommandos "Nächste Taste durchreichen" eine Tastenkombination gedrückt gehalten wird, werden alle Tastendrücke (einschließlich Wiederholungen) an die Anwendung durchgereicht, bis die letzte Taste losgelassen wird.
* Wenn ein NVDA-Modifikator zwei Mal gedrückt (und beim zweiten Mal gedrückt gehalten) wird, werden alle Tastenanschläge einschließlich Wiederholungen ebenfalls an die anwendung durchgereicht.
* Die Tasten für die lautstärkeregelung und Stummschaltung werden nun in der Eingabehilfe erkannt. Dies könnte hilfreich sein, falls sich Anwender über die Funktionsweise dieser Tasten unsicher sind.
* Im NVDA-Einstellungsmenü wurden die Kurztasten für die Einstellen für Braille und nVDA-Cursor geändert, um Konflikte auszuschließen.

### Fehlerbehebungen

* Beim Hinzufügen eines Eintrags im Aussprache-Wörterbuch lautet nun der Titel des Dialogfelds "Wörterbuch-Eintrag hinzufügen" anstelle "Wörterbuch-Eintrag bearbeiten". (#924)
* Im Dialogfeld des Aussprache-Wörterbuchs werden die Spalten für den Regulären Ausdruck und die Berücksichtigung der Groß- und Kleinschreibung nun in der eingestellten Sprache angezeigt.
* Im AOL Instant Messenger (AIM) werden die Positionsinformationen nun als Baumansicht angesagt.
* Im Dialogfeld für die Stimmen-Einstellungen erhöhen Pfeil nach oben, Seite nach oben und Pos1 nun eine Einstellung, während Pfeil nach unten, Seite nach unten und Ende diese verringern. Vormals war es genau umgekehrt, was zum Einen unlogisch war und zum anderen nicht zu den Einstellungen im Sprachausgaben-Einstellungsring passte. (#221)
* Bei deaktiviertem Bildschirm-Layout in den Virtuellen Ansichten, erscheinen keine weiteren fremden Leerzeilen mehr.
* Wenn ein NVDA-Modifikator zwei Mal schnell hintereinander gedrückt wird, jedoch eine andere Taste zwischendurch gedrückt wird, wird beim 2. Tastendruck des Modifikators nicht die eigendliche Funktion der Taste ausgeführt.
* Satzzeichen werden bei der Eingabehilfe nun berücksichtigt, auch wenn die ansage von Satzzeichen deaktiviert ist. (#977)
* In den Tastatur-Einstellungen werden die namen der Tastaturbelegungen nun in der eingestellten Sprache angezeigt. (#558)
* Problem behoben, wonach einige Teile in Adobe Reader-Dokumenten als Leer angezeigt werden. Dies betrifft z. B. das Inhaltsverzeichnis im Apple iOS 4.1 Benutzerhandbuch
* Der Schalter "Aktuell gespeicherte Einstellungen im Anmeldebildschirm und bei Sicherheitsmeldungen verwenden (erfordert Administrationsberechtigungen!)" im Dialogfeld "Allgemeine Einstellungen" funktioniert nun auch dann, wenn er gleich nach der NVDA-Installation, aber noch vor der anzeige eines Sicherheitshinweises benutzt wird. Vorher zeigte NVDA zwar an, das Kopieren der Einstellungen sei erfolgreich gewesen, tatsächlich hatte der Schalter jedoch keinerlei wirkung. (#1194)
* Es ist nun nicht mehr möglich, mehrere Einstellungsdialoge gleichzeitig zu öffnen. Dies behebt Probleme, die auftreten können, wenn Einstellungsdialoge geöffnet werden, die voneinander abhängen (wie z. B. Öffnen der Sprachausgaben-Einstellungen, während gleichzeitig die Stimmen-Einstellungen geöffnet sind). (#603)
* Wenn Ihr Benutzername ein Leerzeichen enthält, tritt bei aktivierter Benutzerkontensteuerung nach dem Schließen des Dialogfensters keinen Fehler mehr auf, wenn Sie in den Allgemeinen Einstellungen von NVDA den schalter "Momentan gespeicherte Einstellungen für Anmeldedialoge und Sicherheitshinweise verwenden" drücken. (#918)
* Anstatt leere Links anzuzeigen, benutzt NVDA im Internet Explorer und anderen MSHTML-Dokumenten nun die Zieladresse des Dokuments als Linkbeschriftung. (#633)
* In den Menüs vom AOL Instant Messenger 7 ignoriert NVDA nun nicht weiter den Fokus. (#655)
* Bei der Rechtschreibprüfung von Microsoft Word zeigt NVDA nun die korrekte Fehlerbeschreibung an (nicht im Wörterbuch, Gramatikfehler, Zeichensetzung). Bisher wurden alle Rechtschreibfehler als Gramatikfehler gekennzeichnet. (#883)
* Problem behoben, wonach beim Schreiben in Microsoft Word bei Verwendung einer Braillezeile falscher Text erzeugt wurde und Word abstürzte, sobald man eine Routing-Taste drückte. (#1212). Es gibt jedoch eine Einschränkung: In Word 2003 und älter können Sie keine arabischen Texte mehr lesen, wenn Sie eine Braillezeile verwenden. (#627)
* Wenn Sie in einem Eingabefeld die Entfern-Taste drücken, sollte sich die Anzeige auf der Braillezeile nun wie erwartet aktualisieren, um die Änderungen wiederzuspiegeln. (#947)
* Wenn in Gecko2-Dokumenten (Firefox 4) mehrere Registerkarten geöffnet sind, werden Änderungen auf dynamischen Webseiten nun korrekt von NVDA wiedergegeben. Bisher wurden nur Änderungen auf der ersten Registerkarte wiedergegeben. (Mozilla Fehlerbericht 610985)
* NVDA kann jetzt die Vorschläge bei der Grammatik- und Rechtschreibprüfung in Microsoft Word korrekt anzeigen. (#704)
* Im Internet Explorer und anderen MSHTML-Dokumenten zeigt NVDA nun nicht mehr die Anker als normale Links an. Ab sofort sind diese verborgen. (#1326)
* Der Umgang mit Gruppenfelder bei der Objektnavigation ist jetzt ohne Fehler möglich.
* In Mozilla Firefox und anderen Gecko-basierten Dokumenten bleibt NVDA nun nicht mehr hängen, falls ein Rahmen eher geladen wurde als das restliche Dokument.
* Wenn Sie in Zeichen mit der Entf-Taste des Nummernblocks löschen, sagt NVDA nun das nächste zeichen korrekt an. (#286)
* Im der Anmeldung von Windows XP wird der Benutzername nun wieder korrekt ausgegeben, wenn Sie den Benutzer wechseln.
* Problem behoben, das beim Lesen von Text innerhalb von Konsolenanwendungen auftritt, wenn die Ansage von Zeilennummern aktiviert ist.
* Die Dialoge für die Listen der Elemente für Virtuelle Ansichten sind jetzt für Sehende bedienbar. Alle Steuerelemente sind am Bildschirm sichtbar. (#1321)
* Die Liste der Einträge im Dialogfeld des Aussprache-Wörterbuchs ist nun besser für Sehende lesbar. Die Liste ist jetzt zum Anzeigen aller Spalten am Bildschirm groß genug. (#90)
* Die Tasten der Braillezeilen der ALVA-Serien BC640 / BC680 werden von NVDA beim nachfolgenden Tastendrücken nicht länger ignoriert.
* Adobe Reader X stürzt beim Verlassen der unmarkierten Dokumentoptionen nach dem Erscheinen des Fortschrittsbalkens nicht mehr ab. (#1218)
* NVDA schaltet nun auf den vorher eingestellten Treiber der Braillezeile um, wenn Sie die gespeicherte Konfiguration zurücksetzen. (#1346)
* Die Projektverwaltung von Visual Studio 2008 wird wieder korrekt erkannt. (#974)
* NVDA wird nun nicht mehr abstürzen, wenn Sie mit Anwendungen arbeiten, in deren Dateinamen nicht-Ascii-Zeichen vorkommen. (#1352)
* Bei der zeilenweisen Navigation in AkelPad wird NVDA nicht mehr das erste Zeichen der folgenden Zeile lesen, wenn der Wortumbruch aktiviert ist.
* Im Code-Editor von Visual Studio 2005/2008 wird nun nicht mehr der gesamte Inhalt gelesen, wenn ein Zeichen eingegeben wird. (#975)
* Problem behoben, wonach einige Braillezeilen nicht richtig geleert wurden, wenn NVDA beendet oder die Braillezeile gewechselt wurde.
* das fokussierte objekt wird beim Start von NVDA nicht mehr zweimal gelesen. (#1359)

### Änderungen für Entwickler

* SCons wird nun verwendet, um den Quellcode vorzubereiten und eine portable Version oder ein Installationsprogramm zu erstellen. Weitere Informationen finden Sie in der Datei "Readme.txt" im Stammverzeichnis des Quellcodes.
* Die Bezeichnung für Tasten(kombinationen) wurden logischer und benutzerfreundlicher gestaltet. z. B. "upArrow" anstelle von "extendedUp" und "numpadPageUp" anstelle von "prior". Eine Liste aller Tastenbezeichnungen finden Sie im Modul "vKCodes".
* Sämtliche Benutzereingaben werden nun durch eine Instanz namens "inputCore.InputGesture" repräsentiert. (#601)
* Jede Eingabequelle bildet eine Unterklasse von "InputGesture". So werden beispielsweise Tastatureingaben von "keyboardHandler.KeyboardInputGesture" verarbeitet.
* "Input gestures" sind beim "SkriptableObjects" angesiedelt. Verwenden der Methode "SkriptableObject.bindGesture()" gehören zur Instanz der "__gestures dict" oder der Klasse der Skriptnamen, die die Tastenzuordnungen definiert. Lesen Sie mehr im Abschnitt "baseObject.SkriptableObject" für Details.
* Anwendungsmodule besitzen keine Dateien für die Tastenzuweisungen mehr. Alle Zuweisungen der Eingabemethoden müssen in den Anwendungsmodulen selbst erfolgen.
* Alle Skripte verarbeiten nun Instanzen von "imputgesture" anstelle von Tastendrücken.
* Es können nun Tastendrücke an das Betriebssystem gesendet werden, in dem die Methode "send()" eines "gesture"-Objekts verwendet wird.
* Um einen Tastendruck zu senden, müssen Sie zunächst ein Objekt vom Typ "keyboardinputgesture" erstellen. Verwenden Sie z. B. "keyboardinputgesture.fromname()". Benutzen Sie anschließend die Methode "send()" des erstellten Objekts.
* In den einzelnen Gebietsschemen können jetzt individuelle Zuweisungen der Eingabemethoden erstellt werden, die neue Eingabemethoden definieren oder vorhandene überschreiben können. Diese so erstelten Eingabemethodenzuweisungen sind überall in NVDA wirksam. (#810)
* Sprachspezifische Zurordnungen der Eingabemethoden müssen im Ordner "locale\<Sprache>\gestures.ini" liegen, wobei <Sprache> der zweistellige Sprachcode ist (z. B. "en" für Englisch und "de" für Deutsch).
* Lesen Sie im Abschnitt "inputCore.GlobalGestureMap" nach, um mehr über das Dateiformat zu erfahren.
* Das neue "LiveText und Terminal NVDAObject" erleichtert das automatische Ansagen von neuen Texten. Lesen Sie im Abschnitt "NVDAObjects.behaviors" zu diesen Klassen für Details. (#936)
* Die Overlay-Klasse "NVDAObjects.window.DisplayModelLiveText" kann für Objekte verwendet werden, die den anzuzeigenden Text direkt vom Bildschirm abfangen müssen.
* Sehen Sie sich die Anwendungsmodule für "Putty" und "Mirc" für Anwendungsbeispiele an.
* Es gibt jetzt kein Standard-Anwendungsmodul mehr. Anwendungsmodule sollten stattdessen die Klasse "appModuleHandler.AppModule" erben, welche die Basisklasse für alle Anwendungsmodule darstellt.
* Unterstützung für globale Erweiterungen hinzugefügt, die Anwendungsübergreifend Skripte zuweisen, "NVDAObject"-Ereignisse verarbeiten und "NVDAObject"-Overlay-Klassen auswählen können. (#281)
 * Für weitere Details sehen Sie sich "globalPluginHandler.GlobalPlugin" an.
* Die verfügbaren Attribute von "SynthDriver"-Objekte für Einstellungen der Strings (im Allgemeinen "availableVoices" und "availableVariants") werden nun als "OrderedDicts" anstatt Listen bezeichnet.
* Die Klasse "synthDriverHandler.VoiceInfo" akzeptiert nun einen optionalen Parameter namens "language", der die Sprache der Stimme angibt.
* Die "SynthDriver"-Objekte stellen nun ein zusätzliches Attribut language zur Verfügung, das die Sprache der aktuellen Stimme angibt.
* Die Basisimplementierung verwendet die Sprache, die im "VoiceInfo"-Objekt bei availablevoices angegeben ist. Dies trifft für alle Synthesizer zu, die eine Sprache pro Stimme bereitstellen.
* Braillezeilentreiber wurden so erweitert, dass Tasten, Rädchen und andere Steuerelemente an NVDA-Skripte zugewiesen werden können:
 * Treiber können eine globale Eingabemethodenzuweisung bereitstellen, um Zuweisungen für Skripte an beliebiger Stelle inNVDA hinzuzufügen.
 * Die Treiber können auch ihre eigenen Skripte bereitstellen, um Zeilenspezifische Funktionen auszuführen.
 * Sehen Sie sich "braille.BrailleDisplayDriver" für weitere Informationen und vorhandene Treiber von Braillezeilen für Beispiele an.
* Die Eigenschaft "selfvoicing" der Klassen für Anwendungsmodule wurde in "sleepmode" umbenannt.
* Um die Namenskonventionen in Anwendungsmodulen und im Tree-interceptor einheitlich zu halten, wurden die Ereignisse "event_appLoseFocus" und "event_appGainFocus" in "event_appModule_loseFocus" bzw. "event_appModule_gainFocus" umbenannt.
* Alle Treiber von zeilen sollten nun "braille.BrailleDisplayDriver" anstelle von "braille.BrailleDisplayDriverWithCursor" verwenden.
 * Der Cursor wird nun außerhalb des Treibers verwaltet.
 * In bereits vorhandenen Treibern muss nur noch die Klassendefinition entsprechend angepasst und die Methode "_display" in "display" umbenannt werden.

## 2010.2

Besondere Änderungen in dieser Version beinhalten eine sehr vereinfachte Objektnavigation; virtuelle Ansichten für Flash-Inhalte von Adobe; Zugänglichkeit für viele zuvor nicht auslesbare Anwendungen, indem auf dem Bildschirm angezeigten Texte zugegriffen wird; Unterstützung von IBM Lotus Symphony-Dokumenten; Ansage der Reihen- und Spaltenüberschriften für Tabellen in Mozilla Firefox; Verbesserte Dokumentation.

### Neue Features

* Die Navigation durch Objekte mit dem NVDA-Cursor wurde enorm vereinfacht. Der NVDA-Cursor lässt Objekte aus, die dem Anwender nichts bringen. So werden Objekte, die zu Strukturierungszwecken verwendet werden oder nicht verfügbar sind, ausgeblendet.
* In Programmen, in welchen die JAVA Access Bridge Verwendung findet, OpenOffice eingeschlossen, können Formatierungen jetzt in Textfeldern angesagt werden. (#358, #463)
* Wenn Sie die Maus über Zellen in Microsoft Excel bewegen, wird NVDA diese nun ansagen.
* In Anwendungen, in welchen die Java Access Bridge verwendung findet, wird der Text in einem Dialogfeld angesagt, sobald dieser erscheint. (#554)
* Virtuelle Ansichten können verwendet werden, um in Flash-Inhalten von Adobe zu navigieren. Objektnavigation und direkte Bedienung mit den Steuerelementen wird trotzdem unterstützt, wenn der Fokusmodus aktiviert wird. (#453)
* Bearbeitbare Steuerelemente in der IDE von Eclipse, einschließlich dem Code-Editor, sind nun zugänglich. Dazu wird Eclipse Version 3.6 oder neuer vorausgesetzt. (#256, #641)
* Den meisten Text am Bildschirm kann nun NVDA vorlesen. (#40, #643)
 * Dies ermöglicht NVDA, Objektinhalte auch dann auszulesen, wenn sie nicht auf direktem Wege gewonnen werden können.
 * Steuerelemente, die hierdurch zugänglich gemacht werden sind z. B. einige Menüs, bei denen Symbole angezeigt werden (z. B. im Untermenü "Öffnen mit..." des Kontextmenüs von Dateien in Windows XP (#151)), bearbeitbare Textfelder in Windows Live (#200), die Fehlerliste in Outlook Express (#582), bearbeitbare Textfelder in Textpad (#605), Listen in Eudora, Viele Steuerelemente in e-tax und den Vormeleditor in Microsoft Excel.
* Unterstützung für den Code-Editor in Visual Studio 2005 und 2008, erfordert mindestens Visual Studio Standard, funktioniert nicht mit Visual Studio Express (#457)
* Unterstützung für IBM Lotus Symphony-Dokumente.
* Frühe, experimentelle Unterstützung von Google Crome. Bitte bedenken Sie, dass Google Chromes Unterstützung für Bildschirmleser noch in der Entwicklungsphase steckt. Auch NVDA-seitig ist noch Arbeit nötig, um Google Crome zu unterstützen. Sie benötigen die neueste Entwicklerversion von Google Chrome.
* Der Status der Dauergroßschreibtaste, Nummernblock und Scrollen blockieren werden beim Betätigen nun in Braille angezeigt. (#620)
* Hilfesprechblasen werden beim Erscheinen nun in Braille angezeigt. (#652)
* Der Treiber für die Braillezeile MDV Lilli wurde hinzugefügt. (#241)
* Beim Auswählen ganzer Zeilen bzw. Spalten in Microsoft Excel mit Umschalt+Leertaste und Strg+Leertaste wird nun die neue Auswahl wiedergegeben. (#759)
* Zeilen- und Spaltenköpfe von Tabellen können angesagt werden. Dies ist im Einstellungsdialog der Dokument-Formatierungen konfigurierbar.
 * Dies wird momentan in Mozilla-Anwendungen, wie Firefox Version 3.6.11 und Thunderbird 3.1.5 oder neuer, unterstützt. (#361)
* Befehle für Flächenmodus eingeführt. (#58)
 * NVDA+Nummerntaste 7 schaltet in den Flächenmodus um und positioniert den NVDA-Cursor an die Stelle des aktuellen Objekts. Dies ermöglicht bildschirmorientierte Navigation im gesamten Bildschirm oder im aktuellen Dokument mit Hilfe der Kommandos für die Textnavigation.
 * NVDA+Nummerntaste 1 zieht den NVDA-Cursor zum objektbasierten Text der Position vom Anzeige-Cursor, um so das Navigieren des Objekts an dieser Stelle zu ermöglichen.
* Aktuelle Benutzer-Einstellungen können zur Benutzung des Anmeldebildschirms und Sicherheitshinweise der Benutzerkontensteuerung im Einstellungsdialog aus kopiert werden. (#730)
* Unterstützung für Mozilla Firefox 4.
* Unterstützung für Internet Explorer 9.

### Änderungen

* Die Funktionen "Alle Objekte vorlesen" (NVDA+Nummernblocktaste), rekursiv zum nächsten Navigator-Objekt springen (NVDA+Umschalt+Nummerntaste 6) und rekursiv zum vorigen Objekt springen (NVDA+Umschalt+Nummerntaste 4) wurden entfernt, da sie fehlerhaft arbeiteten und um die Tastenkombinationen für andere Funktionen freizugeben.
* Im Dialogfeld "Sprachausgaben" wird nun lediglich noch der Anzeigename einer Sprachausgabe angezeigt. Bisher wurde ihm der Treibername vorangestellt, was jedoch nur intern relevant ist.
* In eingebetteten Anwendungen oder Virtuellen Ansichten (z. B. Adobe Flash) können Sie jetzt NVDA+Strg+Leertaste drücken, um aus der eingebetteten Anwendung oder der Virtuellen Ansicht in das übergeordnete Dokument zu wechseln. bisher wurde NVDA+Leertaste hierfür verwende. Jetzt dient NVDA+Leertaste nur noch dazu, zwischen Fokus- und Lesemodus umzuschalten.
* Wenn der Sprachbetrachter (aktiviert im Menü "Extras") den Fokus erhält, wird auf dem Bildschirm neu erscheinender Text im Fenster des Sprachbetrachters nicht angezeigt, bis er den Fokus wieder verliert. Dies erlaubt das einfachere Markieren von Text (um ihn beispielsweise anschließend zu kopieren).
* Die Protokollansicht und die Python-Konsole werden beim Aufruf nun maximiert.
* Wenn Sie in Microsoft Excel auf ein Arbeitsblatt wechseln, auf dem mehr als eine Zelle markiert ist, wird nun von NVDA der gesamte markierte Bereich angezeigt und nicht nur die aktive Zelle. (#763)
* Speichern der Konfiguration und bearbeiten einiger Einstellungen ist nun in Sicherheitshinweisen und Benutzerkontensteuerung sowie dem Anmeldebildschirmen nicht mehr möglich.
* Die Sprachausgabe eSpeak wurde auf Version 1.44.03 aktualisiert.
* Wenn NVDA bereits läuft, wird es beim Anklicken des Desktop-Symbols oder Drücken der Tastenkombination Strg+Alt+N neu gestartet.
* Das Kontrollfeld "Objekt unter Mauszeiger ansagen" (NVDA+M) wurde in "Mausverfolgung einschalten" umbenannt.
* Die Tastaturbelegung für Laptops wurde aktualisiert, sodass alle TastenBelegungen, die es in der Tastaturbelegung für Desktops gibt, ebenfalls verfügbar sind. Des weiteren können nun alle Befehle auf nicht-englischen Tastaturen ausgeführt werden. (#798, #800)
* Wichtige Verbesserungen und Aktualisierungen im Benutzerhandbuch; d. h., die Tastenkürzel für Laptops wurden integriert. Des weiteren wurde die Kurztasten- und Befehlsreferenz mit dem Benutzerhandbuch synchronisiert. (#455)
* Der Braille-Übersetzer LibLouis wurde auf Version 2.1.1 aktualisiert. Dies behebt einige Fehler in der Chinesischen Braille-Übersetzung sowie Zeichen, die nicht in der Brailletabelle vorhanden waren. (#484, #499)

### Fehlerbehebungen

* Wenn in uTorrent ein Menü geöffnet ist, bleibt der Fokus nicht mehr in der Torrent-Liste hängen oder der aktuell hervorgehobene Eintrag wird nicht mehr wiederholg angezeigt.
* In µTorrent werden nun die Dateinamen in der Torrent-Liste angesagt.
* In Programmen von Mozilla wird der Fokus nun richtig erkannt, wenn er auf einer leeren Tabelle bzw. einer leeren Baumstruktur landet.
* In Mozilla-Anwendungen wird der Status "nicht aktiviert" nun für mehr Steuerelemente korrekt ausgageben (beispielsweise für aktivierbare Tabellenzellen). (#571)
* In Mozilla-Anwendungen wird in korrekt implementierten Aria-Dialogen neu erscheinender Text nun nicht mehr ignoriert sondern korrekt angezeigt. (#630)
* In Internet explorer und anderen MSHTML-Dokumenten wird das ARIA-Level-Attribut nun korrekt ausgewertet
* Um eine korrektere Darstellung von ARIA-Dokumenten zu erreichen, werden in Internet Explorer und anderen MSHTML-Dokumenten ARIA-level-Attribute vor allen anderen Objekttyp-Informationen ausgewertet.
* Seltener Fehler im Internet Explorer beim Navigieren durch die Rahmen und unsichtbare Rahmen behoben.
* In Microsoft Word-Dokumenten kann nun auch Text mit Rechts-Links-Ausrichtung wie z. B. Arabisch wieder angezeigt werden. (#627)
* Wenn in 64-Bit-Konsolenanwendungen viel Text erscheint, wurde der Umfang des Protokolls drastisch reduziert. (#622)
* Wenn Skype bereits läuft, während NVDA gestartet wird, ist es nun nicht mehr nötig, Skype neu zu starten, um die Barrierefreiheits-Optionen zu aktivieren. Dies könnte auch auf andere Anwendungen zutreffen, die abfragen können, ob ein bildschirmleser läuft.
* Wenn Sie in Office-Anwendungen die Tastenkombination NVDA+B drücken oder durch Symbolleisten navigieren, wird NVDA nun nicht mehr abstürzen. (#616)
* Falsche Ansagen von Zahlen (z. B. 1,023), die eine 0 nach dem Trennzeichen ausweisen, behoben. (#593)
* Adobe Acrobat Pro und Reader 9 werden nicht mehr abstürzen, wenn sie ein Dokument schließen. (#613)
* In Microsoft Word und in Eingabefeldern wird nun der gesamte markierte Text ausgegeben, wenn Sie Strg+A drücken. (#761)
* Wenn Sie sich In Scintilla-Steuerelementen wie notepad++ den gesamten Text vorlesen lassen und NVDA den System-Cursor bewegt, wird nun kein Text mehr markiert. (#746)
* Es ist nun wieder möglich, sich mit dem NVDA-internen Cursor den Inhalt von Tabellenzellen in Microsoft Excel anzeigen zu lassen.
* In einigen problematischen mehrzeiligen Eingabefeldern in Internet Explorer 8 kann NVDA nun den Text zeilenweise auslesen. (#467)
* Windows Live Messenger 2009 stürzt nun nicht mehr nach dem Start ab, wenn NVDA läuft. (#677)
* Im Web-Browser müssen Sie nun nicht mehr länger die Tabulatortaste drücken, um mit einem eingebetteten Objekt, wie z. B. einem Flash-basierter Film zu starten, nachdem Sie die Eingabetaste betätigt haben, um in das Objekt zu gelangen. (#775)
* In Notepad++ werden lange Zeilen wieder richtig in Braille angezeigt. Ebenso wird der Zeilenanfang nicht mehr abgeschnitten, wenn über den Bildschirmrand hinausgescrollt wird.
* In LoudTalks ist nun die Kontaktliste zugänglich.
* Im Internet Explorer 8 und anderen MSHTML-Dokumenten wird nun die Adresse des Dokuments und "MSAAHTML Registered Handler" fälschlicherweise nicht mehr angezeigt. (#811)
* In Baumstrukturen in Eclipse wird nun nicht mehr der vorher ausgewählte Eintrag angezeigt, wenn sich der Fokus auf einen neuen Eintrag bewegt.
* NVDA funktioniert nun im System korrekt, wo das Arbeitsverzeichnis des Suchpfades für Programmbibliotheken entfernt wurde (). (einzustellen im Registrierungseintrag "CWDIllegalInDllSearch" auf "0xFFFFFFFF"). Beachten Sie, dass dies nicht für die meisten Nutzer relevant ist. (#907)
* Wenn Sie die Navigationsbefehle für Tabellen außerhalb von Tabellen in Microsoft Word verwenden, wird nun nicht mehr "Rand der Tabelle" angezeigt, nachdem bereits die Meldung "Nicht in einer Tabelle" erschienen ist. (#921)
* Wenn die Befehle zur Tabellennavigation nicht ausgeführt werden können, weil sich der Cursor an einer Ecke der Tabelle in Microsoft Word befindet, sagt NVDA "Ecke der Tabelle" in der eingestellten Sprache und nicht mehr in englisch an. (#921)
* In Outlook Express, Windows Mail und Windows Live Mail werden nun bei der Liste der Nachrichtenregeln der Status der Kontrollkästchen angesagt. (#576)
* Die Beschreibung der Nachrichtenregeln können nun in Windows Live Mail 2010 ausgelesen werden.

## 2010.1

Diese Version enthält überwiegend Fehlerbehebungen und Verbesserungen

### Neue Features

* Auf Systemen ohne jegliche Audio-Ausgabe schlägt der Start von NVDA jetzt nicht mehr fehl. In solchen Fällen benötigen Sie entweder eine Braillezeile oder den Dummy-Synthesizer "Keine Sprachausgabe" im Zusammenspiel mit dem Sprachbetrachter, um NVDA effektiv nutzen zu können. (#425)
* Die Option "Sprungmarken anzeigen" wurde im Dialogfeld für die Dokument-Formatierungen hinzugefügt, um Sprungmarken auf Webseiten anzukündigen. Aus Kompatibilitätsgründen ist die option standardmäßig aktiviert.
* Wenn die Ansage von Funktionstasten aktiviert ist, erkennt NVDA jetzt auch Multimedia-Tasten wie Abspielen, Anhalten, Nächster bzw. Vorheriger Track, etc. (#472)
* In Eingabefeldern, die dies unterstützen, sagt NVDA beim Löschen mit Strg+Rücktaste das gelöschte Wort an. (#491)
* Im Fenster des Webformators können nun die Pfeiltasten zum Lesen des Textes verwendet werden. (#452)
* Das Adressbuch von Microsoft Office Outlook wird nun auch unterstützt.
* Bessere Unterstützung der eingebetteten Eingabefelder (Design Mode) im Internet Explorer. (#402)
* Ein neues Skript (NVDA+Umschalt+Nummerntaste Minus) kann verwendet werden, um den System-Cursor zum aktuellen Navigator-Objekt zu ziehen.
* Neue Skripte zum Sperren und Entsperren der Maustasten hinzugefügt. Dies ist nützlich, um Operationen, wie "Ziehen und Fallen lassen" auszuführen. Umschalt+Nummernblock Stern sperrt bzw. entsperrt die linke Maustaste. Umschalt+Nummernblock Schrägstrich sperrt bzw. entsperrt die rechte Maustaste.
* Neue Brailletabellen: Deutsches 8-Punkt-Computerbraille, Deutsche Kurzschrift, Finnisches 8-Punkt-Computerbraille, Chinesisch (Hongkong, Kantonesisch), Chinesich (Taiwan, Mandarin). (#344, #369, #415, #450)
* Es ist nun möglich, bei der Installation von NVDA die Erstellung der Desktop-Verknüpfung zu verhindern. (#518)
* NVDA kann nun iAccessible2 auch auf 64-Bit-Systemen verwenden, sofern es dort verfügbar ist. (#479)
* Unterstützung für Live-Regionen in Mozilla-Anwendungen erweitert. (#246)
* Die NVDA-API wird nun bereitgestellt, was es Programmierern erlaubt, NVDA zu Steuern. Hierzu gehören z. B.: Das Sprechen von Text, das Stummschalten der Sprache, das Anzeigen von Blitzmeldungen, etc.
* In den Anmeldefenstern von Windows Vista und Windows 7 werden nun auch informationen und Fehlermeldungen ausgelesen. (#506)
* In Adobe Reader werden nun auch interaktive Formulare ausgelesen, sofern sie mit Adobe LiveCycle erstellt wurden. (#475)
* Wenn die Anzeige dynamischer Inhalte aktiviert ist, werden nun auch in Miranda IM neu eintreffende Nachrichten in Unterhaltungsfenstern angezeigt. Zudem können die drei letzten Nachrichten abgerufen werden (NVDA+Strg+Ziffer). (#546)
* In Flash-Inhalten werden nun auch Text-Eingabefelder unterstützt. (#461)

### Änderungen

* Die extrem ausführliche Hilfemeldung des Windows 7-Startmenüs wird nun nicht mehr ausgelesen.
* Der Synthesizer "display" wurde durch den Sprachbetrachter ersetzt. um ihn zu aktivieren, wählen sie "sprachbetrachter" aus dem Menü Extras. Der Sprachbetrachter kann verwendet werden, unabhängig davon, welche Sprachausgabe Sie tatsächlich nutze. (#44)
* Blitzmeldungen verschwinden nun von der Braillezeile, wenn Sie eine Taste drücken, die eine Änderung des Fokuses zur Folge hat. Bisher blieben die Meldungen grundsätzlich für die konfigurierte Zeitspanne angezeigt.
* Die Kopplung der Braillezeile (NVDA+Strg+T) kann nun auch in den Braille-Einstellung eingestellt werden. Diese Einstellung wird nun auch in der benutzerspezifischen Konfiguration gespeichert.
* Die Sprachausgabe eSpeak wurde auf Version 1.43 aktualisiert.
* Der Braille-Übersetzer LibLouis wurde auf Version 1.8.0 aktualisiert.
* In virtuellen Ansichten wurde die wort- und zeichenweise Navigation enorm verbessert. Zuvor hatte sie sich stark von der zeilenweisen Navigation unterschieden. (#490)
* Die Strg-Taste hält nun die Sprache an, so wie alle anderen Tasten auch, anstatt sie nur zu unterbrechen. Um die Sprache zu unterbrechen, drücken Sie die Umschalt-Taste.
* Bei Änderungen des Fokuses wird die Anzahl von Spalten und Zeilen nicht mehr angezeigt, da diese Informationen nicht sinnvoll sind.

### Fehlerbehebungen

* Der Start von NVDA wird nun nicht mehr fehlschlagen, wenn UIA zwar vorhanden ist, dessen Iinitialisierung jedoch aus irgendeinem Grund fehlschlug. (#483)
* Es wird nun nicht mehr der gesamte Tabelleninhalt angezeigt, wenn sie sich in Mozilla-anwendungen zwischen Tabellenzellen bewegen. (#482)
* NVDA wird sich nun nicht mehr aufhängen, wenn sie einen Baumknoten erweitern, der sehr viele Unterknoten enthält.
* Im Synthesizer-Einstellungsring und im Dialogfeld für die Stimmen-Einstellungen werden nun fehlerhaft installierte SAPI5-Stimmen von der Auswahl ausgeschlossen. Vormals konnte der SAPI5-Treiber nicht geladen werden, wenn auch nur eine Stimme fehlerhaft installiert war.
* Die Einstellung "Tastenkombinationen anzeigen" greift nun auch in virtuellen Ansichten. (#486)
* Wenn die Ankündigung von Tabellen deaktiviert ist, werden Zeilen- und Spaltenkoordinaten nun nicht mehr irrtümlich angezeigt.
* In virtuellen Puffern werden die Koordinaten von Reihen und Spalten nun korrekt angezeigt, wenn Sie aus einer Tabelle heraus, und wieder hineinspringen, ohne zuvor innerhalb der Tabelle navigiert zu haben (z. B. wenn Sie in der ersten Zeile einer Tabelle Pfeil auf und anschließend wieder Pfeil ab drücken. (#378)
* In Microsoft Word und in mehrzeiligen Eingabefeldern in HTML werden jetzt auch Leerzeilen korrekt angezeigt. Bisher wurde immer der aktuelle Satz und nicht die aktuelle Zeile angezeigt. (#420)
* Mehrere Sicherheitsprobleme beim Ausführen von NVDA in Anmeldefenstern oder sicheren Desktops behoben. (#515)
* Wenn Sie sich in Eingabefeldern oder in Microft Word das gesamte Dokument vorlesen lassen, wird nun die Cursorposition richtig aktualisiert, wenn sich der Cursor über den Bildschirmrand hinaus bewegt. (#418)
* Wenn in einem virtuellen Dokument innerhalb von Links oder klickbaren Elementen Grafiken existieren, die als für Bildschirmleser irrelevant markiert wurden, wird nun kein Text mehr angezeigt. (#423)
* Korrekturen am Laptop-Tastaturschema. (#517)
* Wenn die Braillezeile an die Anzeige (den Navigator) gekoppelt wird, kann nun auch innerhalb von Konsolenanwendungen korrekt navigiert werden.
* In Teamtalk 3 und Teamtalk 4 Classic wird die Aussteuerungsanzeige nun nicht mehr irrtümlich aktualisiert. Ebenso werden jetzt Sonderzeichen in Unterhaltungsfenstern korrekt angezeigt.
* Einträge im Windows-7-Startmenü werden nun nicht mehr doppelt angesagt. (#474)
* Wenn Sie in Firefox 3.6 Links aktivieren, deren Ziel sich auf der selben Seite befindet (z. B. Links zum Überspringen von Navigationsleisten), platziert NVDA nun den Cursor an die richtige Stelle im virtuellen Dokument.
* Problem behoben, wonach in manchen PDF-Dokumenten der Text nicht richtig aufbereitet wurde.
* Zahlen, die durch einen Bindestrich getrennt sind, werden nun nicht mehr falsch ausgesprochen z. B. 500-1000. (#547)
* Wenn Sie in Windows Update unter Windows XP Kontrollkästchen aktivieren, bleibt NVDA nun nicht mehr hängen. (#477)
* Problem behoben, wonach es auf manchen Systemen zu Abstürzen kam, wenn sich Sprache und Signaltöne überlagerten. Dies war am ehesten zu merken, wenn Sie eSpeak verwendeten und beispielsweise im Windows Explorer viele Dateien kopieren.
* NVDA sagt nun nicht mehr an, wenn firefox beschäftigt ist (z. B. wenn eine Seite oder der Browser aktualisiert wird) während sich das betreffende Dokument im Hintergrund befindet. Dies bewirkte eine irrtümliche Ansage der Statuszeile der aktiven Anwendung.
* Wenn Sie mit Alt+Umschalt bzw. Strg+Umschalt das Tastaturschema ändern, zeigt NVDA das neu eingestellte schema nun auch in Braille an. Bisher wurde das Schema nur angesagt.
* Wenn die Ansage von Tabellen deaktiviert ist, werden Tabelleninformationen nicht mehr angesagt, wenn sich der Fokus ändert.
* Einige Baumstrukturen in 64-Bit-Anwendungen wie z. B. das Inhaltsverzeichnis in Microsoft HTML Help) sind nun zugänglich. (#473)
* Problem behoben, wonach das Protokollieren von Meldungen auf nicht-englischsprachigen Systemen fehlschlug, wenn die Meldungen nicht-ascii-Zeichen enthielten. (#581)
* Der Dialogfeld "Über NVDA" erscheint nun in der benutzerspezifischen Sprache. (#586)
* Bei der Verwendung des Synthesizer-Einstellungsrings kommt es nun nicht mehr zu Problemen, wenn Sie eine Stimme auswählen, die weniger Einstellungen anbietet als die vorher eingestellte Stimme.
* In Skype 4.2 werden Kontakte nun nicht mehr doppelt angesagt.
* Speicherprobleme in der Benutzeroberfläche und in Virtuellen Ansichten behoben. (#590, #591)
* Fehler in einigen fehlerhaften SAPI4-Treibern umgangen, wonach NVDA regelmäßig abstürzte. (#597)

## 2009.1

Die wichtigsten Neuerungen dieser Version sind u. a. die Unterstützung von 64-Bit-Versionen von Windows, verbesserte Unterstützung von Internet Explorer und Adobe Reader-Dokumenten, Unterstützung von Windows 7; Das Auslesen von Windows-Anmeldung und Benutzerkontensteuerung sowie die Unterstützung von Java- und Flash-Anwendungen. Einige grundlegende Verbesserungen und Problembehebungen hinsichtlich der Stabilität wurden ebenfalls implementiert.

### Neuerungen

* Offizielle Unterstützung von 64-Bit-Versionen von Windows (#309)
* Unterstützung für den neuen Newfon-Sprachsynthesizer hinzugefügt. Bedenken sie, dass dies eine spezielle Version von newfon erfordert (#206)
* Fokus- und Lesemodus werden nun durch Klänge anstelle gesprochener meldungen angekündigt. Dies ist standardmäßig aktiviert. Die Funktion kann jedoch im Dialogfeld "Lesemodus" konfiguriert werden. (#244)
* NVDA unterbricht nun nicht mehr die Sprache, wenn Sie die Tasten zur lautstärkeregelung drücken. Dies erlaubt Ihnen, die lautstärke einzustellen und das eigentliche Ergebnis zu hören. (#287)
* Die Unterstützung in Dokumenten für Internet Explorer und Adobe Reader wurde komplett erneuert. Diese Unterstützung wurde mit der Unterstützung für Mozilla Gecko vereinheitlicht. Auf diese weise werden Leistungsmerkmale wie die schnelle Verarbeitung des Dokuments, Schnellnavigation, die Linkliste, das Markieren von Text, automatischer Fokusmodus und Braille-Unterstützung in solchen Dokumenten verfügbar.
* Verbesserte Unterstützung für das Steuerelement zur Datumsauswahl im Dialogfeld für Datum/Uhrzeit unter Windows Vista.
* Verbesserte Unterstützung für das moderne Startmenü von Windows XP und Windows Vista. Speziell im Untermenü "alle Programme2 wird nun ach die Baumebene mi angegeben.
* Die Menge an Text, die beim Bewegen der Maus angegeben werden soll, kann in den Maus-Einstellungen konfiguriert werden. Hier kann zwischen Zeichen, Wort, Zeile oder Absatz ausgewählt werden.
* In Microsoft Word werden Rechtschreibfehler korrekt erkannt.
* Unterstützung der Rechtschreibprüfung in Microsoft Word 2007. In früheren Versionen von Microsoft Word wird sie ebenfalls teilweise unterstützt.
* Bessere Unterstützung von Windows Live Mail. Klartext-Nachrichten können gelesen sowie text- und HTML-Nachrichten verfasst werden.
* Wenn Sie sich im Windows Vista auf einem sicheren Desktop befinden (wie z. B. die Benutzerkontensteuerung oder wenn Sie Strg+Alt+Entf drücken), wird NVDA dies nun melden.
* In der Eingabeaufforderung kann NVDA nun den Text unter dem Mauszeiger ansagen.
* Unterstützung der UIA in Windows 7.
* NVDA kann nun so konfiguriert werden, dass NVDA nach der Anmeldung automatisch startet. Die entsprechende Option befindet sich im Einstellungsdialog "Allgemein".
* NVDA kann nun auch geschützte Desktops auslesen (Anmeldebildschirm, Benutzerkontensteuerung, etc.). Die Optionen zum Aktivieren von NVDA für die Anmeldung sind im Einstellungsdialog "Allgemein" zu finden. (#97)
* Treiber für Optelec ALVA BC6 Braillezeilen hinzugefügt.
* Auf Internetseiten kann nun mit N und Umschalt+N vor bzw. hinter einen Block aus Links gesprungen werden.
* In Dokumenten kann nun mit D und Umschalt+D vorwärts bzw. rückwärts zwischen ARIA-Sprungmarken navigiert werden. (#192)
* Die Linkliste wurde in eine Elementliste geändert. Hiermit können Links, sprungmarken und Überschriften aufgelistet werden. Überschriften und Sprungmarken werden hierarchisch aufgelistet. (#363)
* Das Dialogfeld "Elementliste" enthält ein Eingabefeld "Filtern nach", mit dem Elemente ausgefiltert werden können, die einen angegebenen Text enthalten. (#173)
* Portable NVDA-Versionen suchen nun im Unterordner "userconfig" nach ihrer benutzerspezifischen Konfiguration. Die trennt - wie bei der fest installierten Version - die Benutzerdefinierte Konfiguration von NVDA.
* Der Benutzer kann nun in seinem Konfigurationsverzeichnis eigene Anwendungsmodule, Sprachausgabentreiber und Braillezeilentreiber speichern. (#337)
* Virtuelle Dokumente werden nun im Hintergrund verarbeitet. dies erlaubt es dem Benutzer, mit dem Dokument zu arbeiten, während es noch geladen wird. Wenn das Laden des Dokuments länger als eine Sekunde dauert, wird dies von NVDA gemeldet.
* Fährt sich NVDA aus irgendeinem Grund fest, werden alle Tastenanschläge an die anwendung durchgereicht, sodass der Anwender die Möglichkeit hat, das System wiederherzustellen.
* Unterstützung für "Ziehen und Ablegen" in ARIA-Dokumenten in Firefox (#239)
* Wenn Sie in ein virtuelles Dokument wechseln, werden dokumenttitel und aktuell markierter Text gesprochen. Hiermit stimmt das Verhalten von NVDA in virtuellen Dokumenten mit dem in normalen Dokumentobjekten überein. (#210)
* Wenn Sie in einem virtuellen Dokument die Eingabetaste drücken, während sich der Fokus auf einem Objekt befindet, können Sie nun mit eingebetteten Objekten interagieren. Falls das Objekt zugänglich ist, können Sie sich mit Tab und umschalt+tab hindurchbewegen. Um zurück in das virtuelle Dokument zu wechseln, drücken Sie NVDA+Leertaste. (#431)
* In virtuellen Dokumenten können Sie nun mit O und Umschalt+O zwischen eingebetteten Objekten wechseln.
* In Windows Vista und neuer kann NVDA nun auch auf Anwendungen zugreifen, die Sie als Administrator ausführen. Sie müssen eine offizielle NVDA-Version installieren, damit dies funktioniert. Es funktioniert nicht mit tragbaren Versionen oder Entwicklerversionen. (#397)

### Änderungen

* Wenn NVDA startet, sagt er nicht mehr "NVDA ist bereit".
* Zum Abspielen der Klänge beim starten und beenden von NVDA wird nun das eingestellte audio-Ausgabegerät verwendet, und nicht mehr das Windows-Standardaudiogerät. (#164)
* Die Ansage von Fortschrittsbalken wurde verbessert. Sie können nun NVDA so konfigurieren, dass Fortschrittsbalken sowohl durch Signaltöne als auch durch Sprache angekündigt werden.
* Einige allgemeingültige Fensterklassen wie Felder oder Anwendungsfenster werden nun nicht mehr benannt, es sei denn, sie sind unbenannt.
* Der Befehl NVDA+F10 schließt nun die aktuelle Position des NVDA-Cursors beim Kopieren mit ein. Hierdurch ist es nun nach möglich, das letzte Zeichen einer Zeile mitzukopieren, was vorher nicht möglich war. (#430)
* Das Skript navigatorObject_where (Strg+NVDA+Nummernblock 5) wurde entfernt. Die Tastenkonbination hat auf einigen Tastaturen nicht funktioniert. Außerdem war dieses Skript auch nicht besonders nützlich.
* Das Skript "navigatorObject_currentDimentions" wurde an NVDA+Nummernblock Entf zugewiesen. die alte Tastenkombinationen funktionierte auf einigen Tastaturen nicht. Das Skript gibt nun die Breite und Höhe des aktuellen Objekts anstelle der Koordinaten für die rechte untere Ecke zurück.
* Beim Abspielen schnell aufeinanderfolgender Signaltöne (z. B. beim Abspielen der Signaltöne für Mauskoordinaten) wurde die Leistung verbessert. Dies ist besonders auf Netbooks spürbar. (#396)
* Der Klang für Fehler wird in offiziellen NVDA-Versionen nicht mehr abgespielt, Fehler werden aber dennoch protokolliert.

### Fehlerbehebungen

* Wenn NVDA von einem Pfad mit kurzem Dateinamen asgeführt, jedoch in einen Pfad mit langem Dateinamen installiert wurde (z. B. PROGRA~1 vs. Programme) findet er nun seine benutzerspezifischen Einstellungen.
* Wenn Sie sich in einem Menü befinden, funktioniert NVDA+T (Titel lesen) nun korrekt.
* In Braille werden keine nutzlosen Informationen über unbeschriftete Felder mehr angezeigt.
* In Java oder Lotus-Anwendungen werden nun keine nutzlosen informationen über Hauptfenster oder Schichtfelder mehr angezeigt.
* Das Eingabefeld zur Stichwortsuche in kmpilierten HTML-Dateien funktioniert nun korrekt.
* Die anzeige von Seitenzahlen in Microsoft Word funktioniert nun korrekt.
* In Microsoft Word-Dialogfeldern (wie z. B. in der Schriftartenauswahl) funktioniert nun die Navigation mit den Pfeiltasten in Eingabefeldern korrekt.
* Bessere Unterstützung die Eingabeaufforderung. Wenn Sie Strg+Pause drücken, wird NVDA nicht mehr beendet.
* In Windows Vista und neuer wird NVDA nun mit normalen Benutzerrechten gestartet, wenn Sie angewiesen haben, NVDA nach der Installation zu starten.
* Beim Drücken der Rücktaste funktioniert nun auch das Wortecho korrekt. (#306)
* Im Windows Explorer werden nun einige Kontextmenüs nicht mehr fälschlicherweise als Startmenü bezeichnet. (#257)
* Wenn es keine anderen nützlichen Inhalte in Firefox-Dokumenten gibt, werden nun ARIA-Beschriftungen korrekt behandelt. (#156)
* Wenn Sie auf Webseiten wie https://tigerdirect.com/ der Fokus bewegen und ein Eingabefeld dadurch seinen Wert ändert, schaltet NVDA nun nicht mehr irrtümlich in den Fokusmodus um. (#220)
* NVDA versucht nun, sich aus manchen Situationen zu retten, in denen er sich früher komplett festgefahren hat. Eine derartige Rettungsaktion kann bis zu 10 Sekunden dauern.
* Wenn Sie die NVDA-Sprache auf "Benutzerspezifische Standard-Einstellung" gesetzt haben, wird nun die anzeigesprache anstelle der Länder-Einstellung verwendet. (#353)
* NVDA erkennt nun auch die Steuerelemente in AIM 7.
* Beim ausführen des Befehls zum Speichern von Tastenanschlägen bleiben nun keine Umschalttasten mehr hängen. Früher musste NVDA in einer solchen Situation neu gestartet werden. (#413)
* Wenn die Taskleiste den Fokus erhält, wird dies nicht mehr länger igoriert. dies geschieht oft, wenn sie eine Anwendung beenden. Früher verhielt sich NVDA so, als hätte sich der Fokus überhaupt nicht bewegt.
* Wenn die ansage von Zeilennummern aktiviert ist, arbeitet NVDA nun auch in Eingabefeldern von Java-Anwendungen wie OpenOffice.org korrekt.
* Der Befehl NVDA+F10 behandelt nun auch den Fall korrekt, wenn die endmarke vor der Startmarke gesetzt wird. Früher führte dies in Anwendungen wie Notepad++ zu Abstürzen.
* Das Steuerzeichen 0x1 verursacht nun kein merkwürdiges Verhalten von eSpeak mehr (Änderungen in lautstärke oder Stimmhöhe). (#437)
* Der Befehl NVDA+Umschalt+Pfeil hoch (markierten Text vorlesen) behandelt nun auch den Fall korrekt, wenn er auf Objekte angewendet wird, die das Markieren von Text nicht unterstützen.
* Problem behoben, wonach NVDA abstürzte, wenn man im Miranda-im bestimmte Schaltflächen drückt. (#440)
* Wenn das aktuelle Navigator-Objekt kopiert oder buchstabiert wird, wird nun der aktuell markierte Text berücksichtigt.
* Windows-Problem umgangen, wonach Links im (Internet) Explorer nicht korrekt verarbeitet wurden. (#451)
* Problem mit der Datums-/Uhrzeitanzeige behoben, wonach die Datumsanzeige auf manchen Systemen verkürzt wurde. (#471)
* Problem behoben, wonach der System-indikator für bildschirmleser unvorhersehbar deaktiviert wurde, sobald ein sicherer Desktop geschlossen wirde. Dies führte in Anwendungen wie Skype, Adobe Reader und Jart zu Problemen, wenn Sie nach dem Systemindikator suchen wollten. (#462)
* In Kombinationsfeldern im Internet Explorer 6 wird nun der aktuelle Eintrag korrekt ausgegeben, wenn Sie navigieren. (#342)

## 0.6p3

### Neuerungen

* Da die Formularleiste von Microsoft Excel unzugänglich ist, stellt NVDA ein eigenes Dialogfeld zum Bearbeiten von Zell-Inhalten bereit, wenn Sie F2 drücken.
* Unterstützung von Formatierungen in iAccessible2-Steuerelementen wie z. B. Mozilla-Anwendungen
* Wenn möglich werden nun Rechtschreibfehler ausgegeben. Dies kann in den Einstellungen zur Dokument-Formatierung konfiguriert werden.
* NVDA kann nun so konfiguriert werden, dass entweder alle oder nur sichtbare Fortschrittsanzeigen durch Signaltöne angezeigt werden. Alternativ kann auch eingestellt werden, dass der Fortschritt alle 10% angesagt wird.
* In Richedit-steuerelementen können nun auch Links erkannt werden.
* Die maus kann nun auf das Zeichen unter dem NVDA-Cursor bewegt werden. Zuvor konnte die Maus lediglich in die Mitte eines Objekts bewegt werden.
* In virtuellen Puffern bezieht sich nun die NVDA-Corsor-Navigation auf den Inhalt des virtuellen Puffers und nicht mehr auf den Inhalt des aktuellen Navigator-Objekts. Das bedeutet, dass Sie die Tasten(Konbinationen) zur Navigation innerhalb eines Objekts auch innerhalb virtueller Dokumente benutzen können.
* Einige neue Zustände von Java-Steuerelementen werden nun erkannt.
* Wird der Befehl "Titel ansagen" NVDA+T zweimal ausgeführt, wird der Titel buchstabiert. Wird er dreimal ausgeführt, wird der Titel in die Zwischenablage kopiert.
* Die Tastaturhilfe sagt nun auch die Namen von Umschalttasten korrekt an.
* Die von der Tastaturhilfe angesagten Tastennamen sind nun überse5tzbar.
* Unterstützung für das Eingabefeld mit dem Erkannten Text in SiRecognizer. (#198)
* Unterstützung für Braillezeilen.
* NVDA+C hinzugefügt, das den Inhalt der Zwischenablage zurückgibt. (#193)
* Wenn NVDA in virtuellen Puffern automatisch in den Fokusmodus wechselt, können Sie durch Drücken von ESC wieder in den Lesemodus wechseln. Die Tastenkombination NVDA+Leertaste existiert aber trotzdem noch.
* Je nachdem, auf welche Art von Steuerelement der Fokus beim Navigieren in virtuellen Puffern trifft, schaltet NVDA nun in den Fokus- bzw. Lesemodus um. Dies kann in den Einstellungen für virtuelle Puffer konfiguriert werden. (#157)
* Der Treiber für SAPI4 wurde neu geschrieben und beseitigt damit Probleme, die den alten Treibern noch inne wohnten.
* Die Anwendung NVDA enthält nun ein Manifest, d. h., sie wird unter Windows Vista nicht mehr im Kompatibilitätsmodus ausgeführt.
* Die Konfigurationsdateien und Wörterbücher werden nun im benutzerspezifischen Konfigurationsverzeichnis gespeichert, wenn NVDA installiert wird. Dies ist einerseits unter Windows Vista nötig geworden, ermöglicht andererseits mehreren Benutzern, eine individuelle NVDA-Konfiguration zu unterhalten.
* Unterstützung für Positionsinformationen von iAccessible2-Steuerelementen.
* Möglichkeit des Kopierens von Text mit Hilfe des NVDA-Cursors hinzugefügt: NVDA+F9 setzt an der aktuellen Position eine Startmarke, NVDA+F10 kopiert den Text zwischen der Startmarke und der aktuellen Position des NVDA-Cursors in die Zwischenablage. (#240)
* Unterstützung einiger Eingabefelder in der TV-Software von Pinnacle.
* Wurden mehr als 512 Zeichen markiert, sagt NVDA die Anzahl der markierten Zeichen an, anstatt den gesamten Text vorzulesen. (#249)

### Änderungen

* Wenn NVDA so eingestellt wird, dass er das Windows-Standardaudiogerät benutzen soll (Microsoft Windows sound mapper), schaltet er automatisch auf das neue Ausgabegerät um, wenn es sich ändert (wenn Sie z. B. ein USB-Audiogerät anschließen).
* Leistung von eSpeak im Zusammenhang mit einigen audiotreibern unter Vista verbessert.
* Die ansage von Links, Überschriften und zitatblöcken erfolgt nun im dialog für Dokument-Formatierungen. Früher erfolge diese im dialog für virtuelle Puffer; nicht alle Dokumentobjekte werteten diese Konfiguration aus.
* Die Geschwindigkeit ist nun die Standard-Einstellung im Synthesizer-Einstellungsring.
* Laden und Entladen von Anwendungsmodulen wurde verbessert.
* Der Befehl zum Ansagen des Fenstertitels sagt jetzt nur den Fenstertitel an und nicht mehr das gesamte Objekt. Falls das Vordergrundobjekt keinen Namen besitzen sollte, wird der Prozessname verwendet.
* Anstatt "Durchreichen für virtuellen Puffer an" oder "... aus" anzusagen, wird nun "Fokusmodus" oder "Lesemodus" angesagt.
* In der Konfiguration wird die Stimme nun nicht mehr als Index, sondern als ID gespeichert. Dies macht die Stimmen-Einstellungen zuverlässiger. Dies betrifft vor allem Systemwechsel oder Änderungen in der Konfiguration. (#19)
* Die Baumebene wird nun in Baumstrukturen aller Art erkannt. Früher funktionierte dies nur für Windows-eigene baumstrukturen (systreeview32).

### Fehlerbehebungen

* Wenn NVDA auf einem Remote desktop-Server benutzt wird, wird das Ende der Audioausgabe nun nicht mehr abgeschnitten.
* Probleme beim Speichern von Stimmenwörterbüchern behoben.
* Probleme beim Navigieren in Mozilla-Gecko-Dokumenten in größeren Texteinheiten (wortweise, zeilenweise, etc.) behoben. (#155)
* Wenn die aussprache von Wörtern aktiviert ist, greift diese Funktion nun auch beim Drücken der Eingabetaste (beim Zeilenwechsel).
* Zeichensatzspezifische Probleme in RichEdit-Dokumenten behoben.
* Der NVDA-Protokollbetrachter benutzt nun ein RichEdit-Eingabefeld anstelle eines normalen Eingabefeldes. dies erleichtert das wortweise lesen.
* Probleme mit eingebetteten Objekten in RichEdit-Objekten behoben.
* NVDA liest nun die Seitenzahlen in Microsoft word. (#120)
* Wenn Sie in Gecko-Dokumenten mit Tab auf ein aktiviertes Kontrollkästchen wechseln und dieses mit der Leertaste deaktivieren, wird dies nun korrekt angezeigt.
* Teilweise aktivierte Kontrollfelder werden in Firefox nun korrekt erkannt.
* Wenn sich die Markierung in einem eingabefeld in beide Richtungen erweitert bzw. reduziert, wird der markierte Text nun in einem Stück gelesen.
* Das Lesen von Text in Gecko-Eingabefeldern mit Hilfe der Maus sollte nun funktionieren.
* "Alles Lesen" sollte nun keine SAPI5-Sprachausgaben mehr zum Absturz bringen.
* Problem behoben, wonach das Lesen von markiertem Text in Eingabefeldern unmittelbar nach dem Start von NVDA nicht funktionierte.
* Fokusverfolgung in Java-Objekten verbessert (#185)
* Einträge in Java-Baumansichten werden nicht mehr länger als reduziert angezeigt.
* Wenn eine Java-anwendung in den Vordergrund geholt wird, wird nun das Objekt angezeigt, das den Fokus hat. Früher wurde lediglich das Anwendungsobjekt angezeigt.
* Ein einzelner Fehler bringt eSpeak nicht mehr länger zum Schweigen.
* Wenn die Stimmen-Einstellungen über den Einstellungsring geändert werden, werden die Einstellungen jetzt ordnungsgemäß in der Konfiguration gespeichert.
* Das Sprechen von Zeichen und Wörtern während der Eingabe wurde verbessert.
* Neu erscheinender Text in einigen Konsolenanwendungen wie z. B. Textspielen) wird nun korrekt gesprochen.
* NVDA ignoriert nun Fokusänderungen im Hintergrund. Früher wurden diese so behandelt, als hätte sich der echte Fokus geändert.
* Fokuserkennung beim Verlassen von Kontextmenüs verbessert. Früher hat NVDA überhaupt nicht mehr reagiert, wenn Sie ein Kontextmenü verlassen haben.
* NVDA erkennt nun, wenn Sie innerhalb des Startmenüs ein Kontextmenü öffnen.
* Das klassische Startmenü wird nun als Startmenü erkannt, nicht mehr als Anwendungsmenü.
* Das Lesen von Hinweismeldungen im Firefox wurde verbessert. Diese sollten nun nicht mehr mehrfach gelesen werden. (#248)
* Beim Lesen von dialogen werden hervorhebbare, schreibgeschützte Eingabefelder nicht mehr berücksichtigt. Dies verhindert das Lesen des Lizenzvewrtrages in manchen Installationsprogrammen.
* NVDA sagt nun nicht mehr das Demarkieren von Text an (z. B. in der Adressleiste von Internet Explorer oder in Adressfeldern von Thunderbird 3).
* In Outlook Express und Windows Mail wird der Fokus nun ordnungsgemäß in das Eingabefeld für die Nachricht gesetzt, wenn Sie eine Nachricht lesen wollen. Früher musste der Anwender noch in die Nachricht klicken.
* Einige Fehler mit der Funktion "Funktionstasten ansagen" behoben.
* NVDA liest nun Eingabefelder mit mehr als 65535 Zeichen korrekt (z. B. große Dateien im Editor).
* Das Lesen von MSHTML-Eingabefeldern wurde verbessert (z. B. Eingabefelder in html-Dokumenten im Internet Explorer).
* NVDA stürzt nun nicht mehr ab, wenn Sie Text in OpenOffice.org bearbeiten. (#148, #180)

## 0.6p2

* Die Standard-eSpeak-Stimme wurde verbessert.
* Laptop-Tastaturschema hinzugefügt. Tastaturschemen können über die Tastatur-Einstellungen konfiguriert werden. (#60)
* Unterstützung von Gruppierungen bei Listeneinträgen; hauptsächlich in Windows Vista. (#27)
* In Systreeview32-Steuerelementen wird nun auch der Zustand "aktiviert" erkannt.
* Tastenkombinationen für viele Konfigurationsdialoge von NVDA hinzugefügt.
* Unterstützung von iAccessible2-Anwendungen wie Firefox hinzugefügt, wenn NVDA von einem tragbaren Medium aus gestartet wird, ohne DLL-Dateien registrieren zu müssen.
* Problem behoben, wonach in virtuellen Gecko-Dokumenten (Firefox) die Linkliste abstürzte. (#48)
* NVDA sollte im Zusammenhang mit Gecko-Anwendungen wie Firefox oder Thunderbird nicht mehr abstürzen, wenn es mit anderen Rechten ausgeführt wird als die Anwendung selbst.
* Aussprache-Wörterbücher können nun die Groß- und Kleinschreibung berücksichtigen. Optional kann das Suchmuster als Regulärer Ausdruck betrachtet werden. (#39)
* Im Dialogfeld für die virtuelle Ansicht kann nun eingestellt werden, ob NVDA ein Bildschirmlayout verwenden soll oder nicht.
* Anker ohne Referenz werden in Gecko-Dokumenten nicht mehr als Links erkannt. (#47)
* Der NVDA-Suchbefehl NVDA+Strg+f merkt sich nun den letzten Suchbegriff anwendungsübergreifend. (#53)
* Problem behoben, wonach der Status aktiviert von Kontrollfeldern und Auswahlschaltern in virtuellen Puffern nicht erkannt wurde.
* Der Fokusmodus in virtuellen Puffern arbeitet nun dokumentspezifisch und nicht mehr global. (#33)
* Probleme behoben, wonach auf langsamen Systemen und bei Systemen, die aus dem Standby erwacht sind die aussprache bei Fokusänderungen nicht richtig funktionierte.
* Verbesserte Unterstützung von Kombinationsfeldern in Firefox. die Befehle für virtuelle Puffer funktionieren jetzt korrekt, wenn sich der Fokus auf einem Kombinationsfeld befindet..
* Auffinden der Statuszeile in vielen Anwendungen verbessert. (#8)
* Interaktive NVDA-Python-Konsole hinzugefügt, die es Entwicklern ermöglicht, NVDA's Interna zu manipulieren.
* Die Skripte sayAll, reportSelection und reportCurrentLine funktionieren jetzt auch im Fokusmodus innerhalb virtueller Puffer korrekt. (#52)
* Die Skripte "increaserate" und "decreaserate" wurden entfernt. Anwender sollten den Einstellungsring (Strg+NVDA+Pfeiltasten) oder das Dialogfeld für Stimmen-Einstellungen verwenden.
* Die Skalierung und der Frequenzbereich der Signaltöne für Fortschrittsbalken wurden verbessert.
* Neue Navigations-Schnelltasten für virtuelle Puffer hinzugefügt: l für list, i für Listeneinträge, e für Eingabefelder, b für Schaltflächen, x für Kontrollkästchen, r für Auswahlschalter, g für Grafiken, q für Zitatblöcke, c für Kombinationsfelder, 1 bis 6 für Überschriften entsprechender Ordnung, s für Trennlinien, m für Rahmen, (#67, #102, #108)
* Wird im Firefox das Laden eines neuen Dokuments abgebrochen, kann der Anwender den virtuellen Puffer des alten Dokuments immer noch verwenden, das Dokument wird also nicht mehr entladen. (#63)
* Wortweise Navigation in virtuellen Puffern verbessert: Beim wortweisen Navigieren wird nicht mehr versehentlich Text aus mehreren Feldern gesprochen. (#70)
* Fokusverfolgung in Gecko-Dokumenten verbessert.
* Das Skript "findPrevious" (NVDA+Umschalt+F3) für die Verwendung in virtuellen Dokumenten hinzugefügt.
* Probleme behoben, wonach NVDA in Gecko-Dialogen (Firefox und Thunderbird) träge reagierte. (#66)
* NVDA-Protokollbetrachter zum menü Extras hinzugefügt.
* Das Skript zur Ansage von Datum und Uhrzeit verwendet die aktuell eingestellte Sprache für die korrekte Formatierung von Datum und Uhrzeit.
* Das Konbinationsfeld "Sprache" in den allgemeinen Einstellungen zeigt nun die vollständigen Sprachennamen an.
* Beim Navigieren innerhalb des aktuellen Navigator-Objekts wird der Inhalt laufend aktualisiert, z. B. ein hervorgehobener Eintrag im Task-Manager. (#15)
* Beim Navigieren mit der Maus funktioniert nun das Lesen des Absatzes unter der Maus korrekt, es wird nun nicht mehr das ganze Objekt gelesen. Das Abspielen von Audiokoordinaten und die Ansage des Objekttyps unter dem Mauszeiger funktionieren ebenfalls korrekt.
* Unterstützung für das lesen von Text mit der Maus in Microsoft Word.
* Problem behoben, wonach nach dem Verlassen der Menüleiste von wordpad der markierte Text nicht gelesen wurde.
* In Winamp wird der Titel der aktuell abgespielten Datei nicht mehr wiederholt angesagt, wenn Grndfunktionen wie Pause, Anhalten oder die Navigation zum vorigen/nächsten Titel ausgeführt werden.
* In Winamp funktioniert jetzt das Ansagen des Status und das Umschalten von Zufallswiedergabe und Wiederholung. Dies betrifft das Hauptfenster und den Wiedergabelisten-Editor.
* Das Aktivieren von Feldern in Gecko-Dokumenten wurde verbessert. Dies betrifft anklickbare Grafiken, Links, die Absätze enthalten und andere Absurditäten
* Problem beim Öffnen von NVDA-Dialogen af einigen Systemen behoben. (#65)
* Unterstützung für Total Commander hinzugefügt.
* Problem in SAPI4 behoben, wonach die Tonhöhe Beispielsweise nach dem Lesen von Großbuchstaben hängen blieb. (#89)
* HTML-Elemente mit gesetztem OnClick-Attribut werden als Anklickbar erkannt. (#91)
* Bei der Navigation in virtuellen Dokumenten wird nun der sichtbare Bereich nachgezogen, was sehenden die Orientierung erleichtert. (#57)
* Grundlegende Unterstützung für ARIAa Live-Regionen hnzugefügt. In Chatzilla werden neu Eintreffende Nachrichten jetzt automatisch gelesen.
* Verbesserte Unterstützung von Webseiten, die ARIA verwenden (wie Google Docs).
* Beim Kopieren von Text aus virtuellen Puffern werden keine Leerzeilen mehr hinzugefügt.
* Die Leertaste aktiviert nun nicht mehr einen Link in der Linkliste, stattdessen kann sie wie jeder andere Buchstabe verwendet werden, um nach einem Link zu suchen.
* Das Skript moveMouseToNavigator (NVDA+Nummernblock Schrägstrich) bewegt den Mauszeiger nun zur Mitte des Objekts und nicht mehr zur oberen linken Ecke.
* Skripts zum Klicken mit der linken und rechten Maustaste (Nummernblock Schrägstrich bzw. Nummernblock Stern) hinzugefügt.
* Zugriff auf den Infobereich verbessert. Der Fokus sollte hoffentlich nicht mehr auf ein bestimmtes Symbol springen. Zur Erinnerung: Verwenden Sie die Tastenkombination Windows-Taste+B, um in den Infobereich zu wechseln. (#10)
* Leistung von NVDA in Eingabefeldern verbessert: NVDA sagt nun keinen zusätzlichen Text mehr an, wenn der cursor beim Navigieren in eingabefeldern am Ende angekommen ist.
* Probleme mit Abstürzen einiger Synthesizer behoben. (#117)
* Unterstützung für den Audiologic TTS3-Sprachsynthesizer hinzugefügt, der von Gianluca Casalino vertrieben wird. (#105)
* Leistungsverbesserung beim Navigieren in Microsoft Word-Dokumenten
* Verbesserung der Genauigkeit beim Lesen von Meldungsfenstern in Gecko-Anwendungen.
* Abstürze beim Speichern der Konfiguration auf nicht-englischen Windows-Versionen beseitigt. (#114)
* Willkommensbildschirm hinzugefügt. Der Willkommensbildschirm stellt grundlegende Informationen für neue NVDA-Nutzer zur Verfügung und erlaubt es außerdem, die Dauergroßschreibtaste als NVDA-Taste zu verwenden. Er wir beim ersten Start angezeigt und blebt so lange aktiv, bis er abgeschaltet wird.
* Unterstützung von Adobe Reader verbessert, sodass jetzt auch Dokumente mit den Versionen 8 und 9 von Adobe reader gelesen werden können.
* Probleme behoben, wonach es zu Fehlern beim Niederhalten mancher Tasten kam, noch bevor NVDA ordnungsgemäß gestartet war.
* Wenn NVDA so konfiguriert wird, dass die Konfiguration beim Beenden gespeichert wird, wird jetzt sichergestellt, dass die Konfiguration beim Beenden von Windows oder beim Abmelden eines Benutzers ordnungsgemäß gespeichert wird.
* Akustisches NVDA-Logo beim Start der Installation hinzugefügt. Dank an Victor Tsaran.
* NVDA sollte jetzt das Symbol im Infobereich beim Beenden ordnungsgemäß entfernen.
* Die Beschriftungen von Standard-Steuerelementen wie "OK" oder "Abbrechen" erscheinen jetzt in der in NVDA eingestellten Sprache - nicht mehr nur in Englisch.
* Das NVDA-Programmsymbol wird jetzt anstelle eines Standardsymbols für die Verknüpfungen im Startmenü und auf dem Desktop verwendet.
* Beim Navigieren in Excel mit Tab und Umschalt+Tab werden die Zellen jetzt ordnungsgemäß gelesen. (#146)
* Doppelte Ansagen in einigen Listen in Skype behoben.
* Verfolgung des System-Cursors in iAccessible2- und Java-Steuerelementen (wie OpenOffice.org und Lotus Symphony) behoben. NVDA wartet nun ab, bis sich der System-Cursor verschoben hat, anstatt versehentlich falsche Wörter, Zeilen oder Absätze zu lesen. (#119)
* Unterstützung für Akeledit-Steuerelemente hinzgefügt, die z. B. in akelpad 4.0 zu finden sind.
* NVDA hängt sich nun nicht mehr auf, wenn Sie in Lotus Symphony vom Dokument in die Menüleiste wechseln.
* NVDA fährt sich nun nicht mehr im dialog "Programme ändern/entfernen" fest, während eine Deinstallation ausgeführt wird. (#30)
* NVDA fährt sich nun nicht mehr beim Öffnen von Spybot Search & Destroy fest.

## 0.6p1

### Zugriff auf Web-Steuerelemente mit Hilfe neuer virtueller Puffer; Unterstützung von Gecko-Anwendungen wie Firefox3 und Thunderbird3

* Die Ladezeit wurde fast um den Faktor 30 verringert. Sie müssen nun nicht mehr warten, bi die Seite in den Puffer geladen wurde.
* Linkliste hinzugefügt (NVDA+F7).
* Verbesserungen am NVDA-Suchdialog (NVDA+Strg+F). Er führt jetzt eine Suche ohne Beachtung der Groß-/Kleinscheibung durch; einige Fokus-relevante Probleme wurden ebenfalls behoben.
* Es ist nun möglich, Text innerhalb virtueller Puffer zu markieren und zu kopieren.
* Die neuen virtuellen Puffer zeigen die Elemente jetzt so an, wie sie auf dem Bildschirm angeordnet sind d. h. sie werden nicht auf separaten Zeilen angeordnet, es sei denn, sie sind auch visuell auf getrennten Zeilen dargestellt. Dieses Verhalten kann mit NVDA+V zur Laufzeit geändert werden.
* Sie können nun absatzweise mit Strg+Pfeil auf bzw. ab navigieren.
* Unterstützung für dynamische Inhalte verbessert.
* Lesen von Zeilen und Feldern beim Navigieren mit den Pfeiltasten verbessert.

### Internationalisierung

* Es ist nun möglich, Akzentzeichen einzugeben, während NVDA ausgeführt wird.
* NVDA meldet nun einen Wechsel des Tastaturschemas, wenn Sie Alt+Rechte Umschalttaste drücken.
* Die Funktionen zum Ansagen von Datum umd Uhrzeit benutzen nun die im Benutzerkonto hinterlegte Regions- und Sprach-Einstellung.
* Tschechische Übersetzungen hinzugefügt (erstellt von Tomas Valusek mit Unterstützung von Jaromir Vit).
* Vietnamesische Übersetzung von Dang Hoai Phuc hinzugefügt.
* Afrikanische Übersetzung von Willem van der Walt hinzugefügt.
* Russische Übersetzungen von Dmitry Kaslin.
* Polnische Übersetzung von Dorota Czajka hinzugefügt.
* Japanische Übersetzung von Katsutoshi Tsuji hinzugefügt.
* Thailändische Übersetzung von Amorn Kiattikhunrat hinzugefügt.
* Kroatische Übersetzung von Mario Percinic und Hrvoje Katic hinzugefügt.
* Spanische Übersetzung (Galicien) von Juan C. buno hinzugefügt.
* Ukrainische Übersetzung von Aleksey Sadovoy.

### Sprache

* NVDA wird nun mit eSpeak 1.33 ausgeliefert, welches u. a. benannte Varianten zur verfügung stellt. Außerdem wurde das Sprechtempo heraufgesetzt.
* Der Dialogfeld für die Stimmen-Einstellungen bieten jetzt auch eine Einstellung für die Variante, falls der Synthesizer des unterstützt. Unter Varianten werden übrlicherweise Variationen der aktuell eingestellten Stimme verstanden.
* Einstellung für die Betonung hinzugefügt, falls der Synthesizer dies unterstützt (wie z. B. eSpeak).
* Die Positionsangabe (z. B. 1 von 4) kann jetzt abgeschaltet werden. Diese Einstellung ist im Dialogfeld "Objektpräsentation" zu finden.
* NVDA kann nun einen Signalton ausgeben, wenn Sie einen Großbuchstaben eingeben. Ebenso wurde eine Option für das Anheben der Stimme bei Großbuchstaben hinzugefügt.
* Möglichkeit zum Unterbrechen der Sprache hinzugefügt (wie im VoiceOver bei Mac OS X). Sie können die Sprache wie gewohnt mit Strg oder Umschalt abbrechen. Wenn sie danach jedoch Umschalt drücken (ohne zwischendurch eine andere Taste zu drücken) wird die Sprache an der unterbrochenen Stelle fortgesetzt.
* Virtueller Sprachsynthesizer hinzugefügt, der den Text nicht spricht, sondern ihn stattdessen in einem Fenster anzeigt. Dies könnte für sehende Entwickler interessant sein, die normalerweise keine Sprachausgabe benutzen.
* NVDA spricht standardmäßig keine Satzzeichen mehr, die Ansage von Satzzeichen kann jedoch mit NVDA+P eingeschaltet werden.
* eSpeak spricht standardmäßig etwas langsamer, wodurch es für neue Anwender einfacher ist, espeak zu verstehen, wenn Sie NVDA nach der Installation das erste mal nutzen.
* Wörterbücher hinzugefügt. Diese erlauben es, die aussprache bestimmter Wörter oder regulärer Ausdrücke zu modifizieren. Es gibt drei Arten von Wörterbüchern: Das Standardwörterbuch, Stimmenwörterbücher und ein temporäres Wörterbuch. Das Standardwörterbuch bezieht sich auf alle Stimmen, die Stimmenwörterbücher beziehen sich nur auf bestimmte Stimmen und das temporäre Wörterbuch arbeitet nur in der aktuellen Sitzung und wird geleert, sobald Sie NVDA beenden.
* Sprachausgaben können nun jedes im System installierte Audio-Ausgabegerät verwenden. Das Ausgabegerät kann im Dialogfeld für die Sprachausgabe eingestellt werden.

### Leistung

* NVDA beansprucht jetzt nicht mehr so viel speicher, wenn Sie in MSHTML-Sterelemente Text eingeben.
* Die Leistung wurde für Steuerelemente verbessert, die eigentlich keinen Cursor besitzen. Dies betrifft u. a. das Verlaufsfenster in MSN Messenger, Listen oder Baumansichten.
* Leistung in Richedit-Dokumenten verbessert.
* NVDA sollte jetzt nicht mehr ohne Grund Systemspeicher verbrauchen.
* Problem behoben, wonach NVDA dazu neigte, abzustürzen, wenn ein Dos-Fenster mehr als dreimal fokussiert wurde.

### Tastaturbefehle

* NVDA+Umschalt+Nummernblock6 und NVDA+Umschalt+Nummernblock4 bewegen den Navigator rekursiv zum nächsten/vorigen Objekt. Dies macht es möglich, allein mit diesen zwei Tastaturbefehlen eine Anwendung zu erkunden, ohne in der Objekthierarchie auf- und abzusteigen.
* Sie können die Stimmen-Einstellungen nun ändern, ohne das Dialogfeld öffnen zu müssen. Hierzu dient der Synthesizer-Einstellungsring, mit NVDA+Strg+Pfeil links/rechts können Sie zwischen den Einstellungen wechseln. Die Einstellungen werden mit NVDA+Strg+Pfeil auf/ab geändert.
* Befehl zum Ansagen des markierten Textes in Eingabefeldern (NVDA+Umschalt+Pfeil auf) hinzugefügt
* Einige Befehle, die Text sprechen, können nun zweimal ausgeführt werden, um den entsprechenden Text zu buchstabieren.
* Die Dauergroßschreibtaste, die Einfügetaste der erweiterten Tastatur sowie die Einfügetaste des Nummernblocks können jetzt als NVDA-Tasten eingestellt werden. Wenn eine dieser Tasten zweimal gedrückt wird, wird der Tastendruck an das Betriebssystem weitergereicht, sodass die Taste die normale Funktion ausführt. Die NVDA-Taste kann im Dialogfeld für Tastatur-Einstellungen geändert werden.

### Unterstützung von Anwendungen

* Die Unterstützung für Firefox3 und Thunderbird 3 wurde verbessert. Die Ladezeiten wurden um den Faktor 30 verkürzt, ein Bildschirm-Layout wird jetzt standardmäßig benutzt, das jedoch mit NVDA+V deaktiviert werden kann. Eine Linkliste (NVDA+F7) wurde hinzugefügt, der Suchdialog (Strg+NVDA+F) arbeitet nun ohne Berücksichtigung der Groß- und Kleinschreibung, die Unterstützung für dynamische Inhalte wurde verbessert, Das Markieren und Kopieren von Text ist nun möglich.
* In den Verlaufsfenstern von Windows Live Messenger und MSN Messenger ist nun das Markieren und Kopieren von Text möglich.
* Verbesserte Unterstützung von Audacity.
* Unterstützung für die neuen Eingabefelder in Skype hinzugefügt.
* Verbesserte Unterstützung für Miranda IM.
* Probleme beim Öffnen von Nachrichten in Outlook Express behoben.
* Die Nachrichtenfenster in Brettnachrichten in Outlook Express werden nun korrekt beschriftet.
* In Eingabefeldern wie An, Kopie, von oder Blindkopie in Outlook Express können die Adressen jetzt gelesen werden.
* Verhalten beim Löschen von Nachrichten in Outlook Express verbessert.

### Programmierschnittstellen und Komponentenbausätze

* Navigation durch MSAA-Objekte verbessert: Wenn ein Fenster ein Systemmenü, eine Titelzeile oder Bildlaufleisten besitzt, können Sie nun dorthin navigieren.
* Unterstützung für iAccessible2 hinzugefügt. Dadurch werden mehr Steuerelementtypen erkannt. Ebenso ist es jetzt möglich, in Anwendungen wie Firefox oder Thunderbird zu navigieren, Text zu markieren oder zu editieren.
* Unterstützung für Scintilla-Eingabefelder hinzugefügt. Solche Eingabefelder sind z. B. in notepad++ oder in tortoise svn.
* Unterstützung für Java-Anwendungen via Java Access Bridge hinzugefügt. Dies stellt grundlegende Unterstützung für alleinstehende Java-Anwendungen sowie für OpenOffice.org zur Verfügung, falls Java aktiviert ist. Bedenken Sie, dass Anwendungen, die innerhalb des Webbrowsers ausgeführt werden, noch nicht funktionieren.

### Maus

* Das Lesen von Text unter dem Mauszeiger wurde verbessert. Die Funktion arbeitet nun viel schneller und kann jetzt auch in Steuerelemente wie standard-Eingabefelder oder Java-Anwendungen hineingreifen. Hierdurch wird in solchen Anwendungen tatsächlich das aktuelle Wort vorgelesen, und nicht das gesamte Objekt. Die könnte für sehgeschädigte Anwender interessant sein, die die Maus benutzen wollen, um den Bildschirminhalt zu erkunden.
* Option zum Abspielen von Audiokoordinaten bei Mausbewegugen hinzugefügt. Hiermit wird ein 40 ms langer Singalton jedesmal abgespielt, wenn Sie die Maus bewegen. Die Frequenz (zwischen 220 und 1760 hz) repräsentiert die Position des Mauszeigers auf der y-Achse. Die Position des Mauszeigers in x-Richtung wird durch die Position des Signaltons im Stereofeld repräsentiert. Dies gibt Ihnen eine Vorstellung davon, wo sich der mauszeiger auf dem Bildschirm befindet. Diese Funktion st direkt abhängig von der Funktion "Objekt unter maus vorlesen". Wenn Sie beide Funktionen schnell ein-/ausschalten wollen, drücken Sie NVDA+M. Außerdem wird die Lautstärke der Signaltöne durch die Helligkeit an der jeweiligen bildschirmposition beeinflusst.

### Objektdarstellung und Interaktion

* Unterstützung für die häufigsten Baumstrukturen verbessert. NVDA teilt ihnen nun mit, wie viele Einträge ein Zwig hat, wenn Sie ihn erweitern. Außerdem wird Ihnen die Ebene mitgeteilt, wenn sie zwischen Einträgen navigieren. Außerdem beziehen sich die Positionsangaben (Nummer des aktuellen Eintrags und Anzahl der Einträge) nicht mehr auf den gesamten Baum sondern nur noch auf den aktuellen Zweig.
* Verhalten von NVDA bei der Navigation durch das Betriebssystem optimiert. Wenn sich der Fokus auf ein Objekt bewegt, werden nun auch übergeordnete Objekte mit angesagt/angezeigt. Wenn der Fokus beispielsweise auf einer Schaltfläche landet, die sich innerhalb einer Gruppe befindet, wird der name der Gruppe ebenfalls angezeigt.
* NVDA versucht nun Meldungen anzuzeigen, die sich innerhalb von Dialogfeldern befinden. Dies funktioniert zwar meistens, dennoch gibt es einige Dialogfelder, die noch nicht zufriedenstellend gelesen werden.
* Kontrollfeld "Objektbeschreibungen ansagen" hinzugefügt. Fortgeschrittene Anwender werden diese Option jedoch deaktivieren, insbesondere bei Java-Anwendungen, bei denen die Beschreibungen sehr lang werden können.
* NVDA sagt nun den markierten Text in Eingabefeldern an, so bald diese den Fokus erhalten. Falls kein Text markiert ist, wird - wie gewohnt - die aktuelle Zeile angesagt.
* Beim Abspielen von Signaltönen für Fortschrittsbalken ist NVDA jetzt wesentlich umsichtiger.

### Benutzeroberfläche

* Das NVDA-Hauptfenster wurde durch ein Popup-Menü ersetzt.
* Die Einstellungen zur Benutzeroberfläche wurden in "Allgemeine Einstellungen" umbenannt. Das Dialogfeld enthält außerdem ein Kombinationsfeld für den Protokollumfang, mit dem eingestellt werden kann, welche Informationen im NVDA-Protokoll festgehalten werden soll. Die Protokoll-Datei wurde zudem von "debug.log" in "nvda.log" umbenannt.
* Da die Behandlung von Gruppennamen unterschiedlich (je nach Objekttyp) gehandhabt wird, wurde die Option "Gruppennamen ansagen" aus dem Dialogfeld "Objektdarstellung" entfernt.

## 0.5

* NVDA bringt jetzt den integrierten Synthesizer eSpeak mit, der von Jonathan Duddington entwickelt wurde. Espeak ist Schnell, klein und unterstützt viele unterschiedliche Sprachen. SAPI-Sprachen werden zwar immer noch unterstützt, eSpeak wird jedoch standardmäßig verwendet.
 * eSpeak ist unabhängig von jeglicher installierter Software und kann z. B. von einem USB-Speichermedium aus verwendet werden.
 * Weitere Informationen zu eSpeak finden Sie in englischer Sprache unter https://espeak.sourceforge.net/.
* Problem behoben, wonach beim Löschen eines Zeichens aus Eingabefeldern in Internet Explorer oder Outlook Express ein falsches Zeichen angesagt wurde.
* Unterstützung für weitere Eingabefelder in Skype hinzugefügt.
* Die virtuellen Puffer werden nur geladen, wenn sich der Fokus auch wirklich auf dem entsprechenden Fenster befindet. Dies behebt Probleme, wenn in Outlook Express das Vorschaufenster aktiviert ist.
* Kommandozeilen-Parameter zu NVDA hinzugefügt:
 * -m, --minimal: Spielt weder Klänge beim Starten und beenden ab, noch wird ein Willkommensbildschirm angezeigt.
 * -q, --quit: Beendet jegliche laufende NVDA-Instanzen.
 * -s, --stderr-file Dateiname: Gibt eine Datei an, in der nicht abgefangene Fehler und ausnahmen protokolliert werden sollen.
 * -d, --debug-file Dateiname: Gibt eine Datei an, in der Meldungen zur Fehlerbehebung festgehalten werden sollen.
 * -c, --config-file: Gibt eine alternative Konfigurationsdatei an.
 * -h, --help: Zeigt eine Hilfe an, das die Kommandozeilen-Parameter auflistet.
* Problem behoben, wonach Satzzeichen nicht übersetzt wurden, wenn Sie eine andere Sprache als Englisch eingestellt haben und wenn die Aussprache eingegebener Zeichen aktiviert ist.
* Sprachdatei für Slovakisch hinzugefügt, Dank an Peter Vágner.
* Dialogfeld zum Einstellen virtueller Ansichten oder der Dokument-Formatierungen hinzugefügt.
* Französische Sprach-Datei hinzugefügt, Dank an Michel Such.
* Skript zum Ein-/Ausschalten der Signaltöne für Fortschrittsbalken hinzugefügt (NVDA+U).
* Mehr Meldungen für Übersetzer zugänglich gemacht, beinhaltet u. a. die Meldungen der Tastaturhilfe.
* Im Internet Explorer können Sie jetzt mit Strg+F einen Suchdialog aufrufen und damit innerhalb des aktuellen virtuellen Dokuments nach einer Zeichenfolge suchen. Drücken von F3 sucht nach dem nächsten Vorkommen der zeichenkette.
* Wenn die aussprache eingegebener Zeichen aktiviert ist, werden jetzt mehr Zeichen gesprochen. Rein technisch betrifft das die Zeichen mit Ascii-Werten von 32 bis 255.
* Zur besseren Verständlichkeit wurden einige Steuerelementtypen umbenannt.
* Wenn Sie in einer Liste oder in einer Baumstruktur navigieren, werden die Elementtypen Listeneintrag und Baumknoten nicht mehr angesagt, um die Navigation zu beschleunigen.
* Die Ansage für Menüs, die ein Untermenü enthalten, wurde in "Untermenü" geändert.
* Da in einigen Sprachen die Taste AltGr bzw. die Kombination alt+strg zum Eingeben von Sonderzeichen benutzt werden, werden solche Zeichen jetzt auch korrekt angesagt, wenn die Aussprache eingegebener Zeichen aktiviert ist.
* Probleme beim Lesen von statischem Text behoben.
* Dank an Coscell Kao für die Sprachdatei für traditionelles chinesisch.
* Wichtige Teile des Quellcodes wurden neu geschrieben, um etliche Probleme (u. a. mit den NVDA-Dialogen und der Benutzeroberfläche) zu lösen.
* SAPI4-Unterstützung hinzugefügt. im Moment gibt es zwei Treiber, einen auf der Grundlage von Code von Serotek Corporation, und einen, der das ActiveVoice.ActiveVoice com-Interface benutzt. Beide Treiber haben Probleme, Ausprobieren ist also anzuraten.
* Wenn eine NVDA-Instanz gestartet wird, während eine andere bereits läuft, wird die neu hinzugekommene NVDA-Instanz sofort wieder beendet. Dies behebt Probleme, wonach das System sehr instabil wird, sobald mehrere Instanzen von NVDA laufen.
* Der Titel der NVDA-Benutzeroberfläche wurde von "NVDA-Benutzeroberfläche" in NVDA geändert.
* Problem behoben, wonach das Drücken der rücktaste am Anfang einer Zeile Fehler verursacht hat.
* Skript zur ansage des akkustatus bei Notebooks hinzugefügt (NVDA+Umschalt+B)
* Neuer Synthesizer "Keine Sprache" hinzugefügt. Dieser Treiber bringt NVDA komplett zum Schweigen. Der Treibe könnte zusammen mit Braillezeilen sinnvoll sein, sobald die Braille-Unterstützung funktioniert.
* Einstellung zum Anheben der Stimme bei Großbuchstaben hinzugefügt.
* Skript zum ein-/Ausschalten der Mausverfolgung dahingehend geändert, dass jetzt auch di Textbausteine "an"/"aus" beim ein-/Ausschalten der Mausverfolgung verwendet werden, anstatt zwei unterschiedliche Meldungen zu sprechen.
* Dank an Juan C. buo für die spanischen Sprachdateien.
* Dank an Tamas Gczy für die ungarischen Sprachdateien.
* Dank an Rui Batista für die portugiesische Übersetzung.
* Die Stimmen-Einstellungen wurden dahingehend korrigiert, dass beim Wechsel des Synthesizers die Werte für Lautstärke, Stimmhöhe und Geschwindigkeit an die Skala des neuen Synthesizers angepasst werden, anstatt dem neuen Synthesizer den alten Wert aufzuzwingen.
* Problem behoben, wonach entweder die Sprache abbrach oder NVDA abstürzte, sobald eine Eingabeaufforderung geöffnet wurde.
* Wenn unter Windows eine bestimmte Sprache eingestellt ist, die NVDA unterstützt, wird er diese auch automatisch benutzen. Die Sprache kann aber trotzdem noch manuell geändert werden.
* Skript "toggleReportDynamicContentChanges" (NVDA+5) hinzugefügt. Dies schaltet die ansage von neu erscheinendem Text oder dynamischen Inhalten um. Momentan funktioniert das nur in dos-Fenstern.
* Skript "toggleCaretMovesReviewCursor" (NVDA+6) hinzugefügt. Hiermit wird festgelegt, ob der NVDA-Cursor automatisch dem System-Cursor folgen soll. Dies kann beim Lesen von DOS-Fenstern sinnvoll sein, deren Inhalt schnell aktualisiert wird.
* Skript "toggleFocusMovesNavigatorObject" (NVDA+7) hinzugefügt. Hermit legen Sie fest, ob der Navigator automatisch nachgezogen werden soll, wenn sich der Fokus ändert.
* Dokumentation in einigen Sprachen hinzugefügt (u. a. Französisch, Spanisch und Finnisch.
* Entwicklerdokumentation aus den Binären Distributionen von NVDA entfernt, im Quellcode ist sie aber immer noch enthalten.
* Problem in Windows Live Messenger und MSN Messenger behoben, wonach die Navigation innerhalb der Kontaktliste Fehler verursacht hat.
* Neu eintreffende Nachrichten werden im Windows Live Messenger automatisch gelesen (funktioniert bis jetzt nur mit der englischen Version).
* Das Verlaufsfenster in Windows Live Messenger kann jetzt auch mit den Pfeiltasten gelesen werden. Funktionier bis jetzt nur in der englischen Version.
* Skript "passNextKeyThrough" (NVDA+F2) hinzugefügt. Wenn Sie diese Tastenkombination drücken, können Sie danach eine Tastenkombination drücken, die durch NVDA durch an Windows weitergereicht werden soll. Dies ist sinnvoll, Wenn Sie eine Tastenkombination an das Betriebssystem durchreichen wollen, die normalerweise durch NVDA reserviert wird.
* NVDA fährt sich nun nicht mehr eine Minute und länger fest, wenn sehr große Dokumente in ms word geöffnet werden.
* Fehler im Word behoben, wonach die Zellen nicht mehr vorgelesen werden, wenn Sie eine Tabelle verlassen und wieder hineinnavigieren.
* Wenn NVDA mit einer Sprachausgabe gestartet wird, die nicht existiert, wird zunächst versucht, SAPI5 zu laden. Schlägt auch dies fehl, so wird keine sprache benutzt.
* Die Skripte zum erhöhen/verringern der Sprechgeschwindigkeit erlaubt keine Werte <0 oder >100 mehr.
* Falls es beim Wechsel der Sprache zu einem Fehler kommt, wird der anwender darüber informiert.
* NVDA fragt nun nach, ob nach einem Sprachenwechsel die Konfiguration gespeichert und neu gestartet werden soll. Ein Neustart von NVDA ist nach einem sprachenwechsel notwendig.
* Wenn bei der Auswahl eines Synthesizers aus dem Sprachausgabendialog dieser nicht geladen werden kann, wird der Anwender darüber informiert.
* Wird eine Sprachausgabe das erste mal geladen, wird nach einer passenden Stimme gesucht bzw. passende Werte für Geschwindigkeit, Lautstärke und Stimmhöhe eingestellt. Dies behebt Probleme mit den sapi4-Versionen von Eloquence und viavoice, die bisher zu schnell gesprochen haben.
