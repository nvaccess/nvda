# NVDA NVDA_VERSION Benutzerhandbuch

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Kurzübersicht der Befehle -->



## Einleitung {#Introduction}

Willkommen bei NVDA!

NVDA (NonVisual Desktop Access) ist ein freier und quell offener Screenreader für das Microsoft Windows-Betriebssystem.
Es bietet Feedback via synthetischer Sprache und Braille. Dabei erhalten Blinde und hochgradig sehbehinderte Menschen kostenlos gleichermaßen Zugriff auf Windows wie ein Sehender.
Entwickelt wird NVDA von [NV Access](https://www.nvaccess.org/) und allen Mitwirkenden aus der Commune.

### Allgemeine Features {#GeneralFeatures}

Mit NVDA wird blinden und sehbehinderten Menschen das Arbeiten mit zahlreichen Anwendungen von Drittanbietern unter Windows ermöglicht.

Eine kurze Video-Demonstration ["Was ist NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) ist auf dem NV Access YouTube-Kanal verfügbar.

Zu den wichtigsten Funktionen gehören:

* Unterstützung der am weitesten verbreiteten Anwendungen einschließlich Web-Browser, E-Mail-Clients, Programme für Internet-Chats und Office-Anwendungen.
* Integrierte Sprachausgabe, die über 80 Landessprachen unterstützt.
* Rückmeldungen von Textformatierungen und Rechtschreibfehlern.
* Automatische Ansage der Mausposition und optionaler Audio-Koordinaten.
* Unterstützung für viele Braillezeilen, einschließlich der Möglichkeit, viele davon automatisch zu erkennen sowie Braille-Eingabe auf Braillezeilen mit einer Braille-Tastatur.
* Ausführen von einem USB-Stick oder anderen transportablen Medien.
* Einfache Bedienung während der Installation mit Unterstützung durch die Sprachausgabe.
* Übersetzt in mehr als 54 Sprachen.
* Unterstützung für moderne Windows-Betriebssysteme (32- und 64-Bit).
* Lauffähig während der Windows-Anmeldung und [anderen Sicherheitsmeldungen](#SecureScreens).
* Unterstützung für Touchscreens.
* Unterstützung gängiger Schnittstellen zur Barrierefreiheit wie Microsoft Active Accessibility, Java Access Bridge, IAccessible2 und UIA.
* Unterstützung für die Windows-Eingabeaufforderung und -Konsolenanwendungen.
* Möglichkeit, den System-Fokus hervorzuheben.

### System-Voraussetzungen {#SystemRequirements}

* Betriebssysteme: Alle 32-Bit- und 64-Bit-Versionen von Windows 8.1, Windows 10, Windows 11 und alle Server-Versionen ab Windows Server 20012 R2.
  * Es werden sowohl AMD64- als auch ARM64-Varianten von Windows unterstützt.
* Mindestens 150 MB Speicherplatz.

### Internationalisierung {#Internationalization}

Auf der Welt sollten alle Menschen den gleichen Zugang zur Information und zu moderner Technologie erhalten, unabhängig von der Sprache.
Neben Englisch wurde NVDA in mehr als 54 Sprachen übersetzt, darunter: Afrikaans, Albanisch, Amharisch, Arabisch, Aragonesisch, Bulgarisch, Burmesisch, Chinesisch (vereinfacht und traditionell), Dänisch, Deutsch (Deutschland und Schweiz), Farsi, Finnisch, Französisch, Galizisch, Georgisch, Griechisch, Hebräisch, Hindi, Irisch, Isländisch, Italienisch, Japanisch, Kannada, Katalanisch, Kirgisisch, Koreanisch, Kroatisch, Litauisch, Mazedonisch, Mongolisch, Nepalesisch, Niederländisch, Norwegisch, Polnisch, Portugiesisch (Brasilien und Portugal), Punjabi, Rumänisch, Russisch, Schwedisch, Serbisch, Slowakisch, Slowenisch, Spanisch (Kolumbien und Spanien), Tamil, Thai, Tschechisch, Türkisch, Ukrainisch, Ungarisch, Vietnamesisch.

### Sprachausgaben-Unterstützung {#SpeechSynthesizerSupport}

Zusätzlich zur Bereitstellung der Benutzeroberfläche in mehreren Sprachen kann der Benutzer in NVDA Text in jeder Sprache lesen, sofern er eine Sprachausgabe für die entsprechende Sprache installiert hat.

NVDA wird standardmäßig mit der freien multilingualen Sprachausgabe [eSpeak NG](https://github.com/espeak-ng/espeak-ng), ausgeliefert.

Informationen über weitere unterstützte Sprachausgaben, können Sie im Abschnitt [Unterstützte Sprachausgaben](#SupportedSpeechSynths) nachlesen.

### Braillezeilen-Unterstützung {#BrailleSupport}

Für Anwender, die eine Braillezeile besitzen, kann NVDA die Informationen in Blindenschrift ausgeben.
NVDA verwendet den Open-Source-Braille-Übersetzer [LibLouis](https://liblouis.io/), um Braille-Sequenzen aus Text zu generieren.
Die Eingabe von Kurz-, Voll- und Basisschrift über die Braille-Tastatur der Braillezeile wird ebenfalls unterstützt.
Zudem erkennt NVDA standardmäßig viele Braillezeilen automatisch.
Für weitere Informationen lesen Sie bitte im Abschnitt [Unterstützte Braillezeilen](#SupportedBrailleDisplays) nach.

NVDA enthält Braille-Übersetzungstabellen für Computerbraille sowie für Voll- und Kurzschrift diverser Sprachen.

### Lizenzbestimmungen und Copyright {#LicenseAndCopyright}

Copyright NVDA_COPYRIGHT_YEARS NVDA-Mitwirkende.

NVDA ist unter der GNU General Public License Version 2 verfügbar, mit zwei besonderen Ausnahmen.
Die Ausnahmen sind im Lizenz-Dokument unter den Abschnitten "Nicht-GPL-Komponenten in Plugins und Treibern" und "Microsoft Distributable Code" aufgeführt.
NVDA verwendet auch Komponenten, die unter verschiedenen freien und Opensource-Lizenzen zur Verfügung gestellt werden.
Es steht Ihnen frei, diese Software auf jede Art und Weise weiterzugeben oder zu verändern, solange Sie die Lizenz mitliefern und den gesamten Quellcode jedem zur Verfügung stellen.
Dies gilt sowohl für Original- als auch für modifizierte Versionen dieser Software sowie für alle veränderten Versionen.

Für weitere Informationen lesen Sie [die vollständige Lizenz](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) auf Englisch.
Einzelheiten zu Ausnahmen finden Sie im NVDA-Menü unter "Hilfe", "Lizenz".

## NVDA-Schnellstartanleitung {#NVDAQuickStartGuide}

Diese Schnellstartanleitung enthält drei Hauptabschnitte: Herunterladen, Ersteinrichtung und Ausführung von NVDA.
Es folgen Informationen über die Anpassung von Einstellungen, die Teilnahme an der Community und die Inanspruchnahme von Hilfe.
Die Informationen in diesem Handbuch wurden aus anderen Teilen des NVDA-Benutzerhandbuchs zusammengefasst.
Ausführlichere Informationen zu den einzelnen Themen finden Sie im vollständigen Benutzerhandbuch.

### NVDA herunterladen {#GettingAndSettingUpNVDA}

NVDA kann von allen völlig kostenlos genutzt werden.
Sie müssen sich nicht um einen Lizenzschlüssel kümmern oder ein teures Abonnement bezahlen.
NVDA wird im Durchschnitt viermal pro Jahr aktualisiert.
Die neueste NVDA-Version ist immer auf der Seite "Download" der [Webseite von NV Access](NVDA_URL) verfügbar.

NVDA läuft  mit allen aktuellen Versionen von Microsoft Windows.
Unter [Systemvoraussetzungen](#SystemRequirements) finden Sie dazu alle Einzelheiten.

#### Schritte zum Herunterladen von NVDA {#StepsForDownloadingNVDA}

Diese Schritte setzen einen gewissen Umgang mit dem Navigieren auf Webseiten voraus.

* Öffnen Sie einen Web-Browser (drücken Sie die `Windows`-Taste, geben Sie den Namen des gewünschten Web-Browsers ein und drücken Sie dann die `Eingabetaste`).
* Öffnen Sie die Download-Seite von NV Access (Drücken Sie `Alt+D`, geben Sie die folgende Adresse ein und drücken dann die `Eingabetaste`):
https://www.nvaccess.org/download
* Klicken Sie auf die Schaltfläche "Download".
* Es kann sein, dass der Browser nach dem Herunterladen zu einer Aktion auffordert und dann das Herunterladen startet.
* Je nach Browser kann die Datei nach dem Herunterladen automatisch ausgeführt werden.
* Wenn die Datei manuell gestartet werden muss, drücken Sie `Alt+N`, um in den Infobereich zu gelangen, dann `alt+r`, um die Datei zu starten (oder die Schritte für Ihren Browser).

### NVDA einrichten {#SettingUpNVDA}

Wenn Sie die soeben heruntergeladene Datei ausführen, wird NVDA temporär entpackt und gestartet.
Sie werden dann gefragt, ob Sie NVDA installieren, eine portable Version erstellen oder nur temporär weiter verwenden möchten.

NVDA benötigt beim Starten oder Installieren keinen Internetzugang, sobald der Launcher heruntergeladen ist.
Sofern eine Internetverbindung vorhanden ist, kann NVDA in regelmäßigen Abständen nach Updates suchen.

#### Schritte zum Ausführen des heruntergeladenen Launcher {#StepsForRunningTheDownloadLauncher}

Die Setup-Datei heißt "nvda_2022.1.exe" oder so ähnlich.
Das Jahr und die Version ändern sich zwischen den Updates, um die aktuelle Version wiederzugeben.

1. Führen Sie die heruntergeladene Datei aus.
Ein Signalton wird wiedergegeben, während eine temporäre NVDA-Version geladen wird.
Nach dem Laden wird NVDA den Rest während des Prozesses sprechen.
1. Das Fenster des NVDA Launchers wird mit der Lizenzvereinbarung angezeigt.
Drücken Sie `Pfeiltaste nach unten`, um die Lizenzvereinbarung zu lesen, falls gewünscht.
1. Drücken Sie die "Tabulatortaste", um zum Kontrollkästchen "Ich stimme zu" zu gelangen und drücken Sie dann die "Leertaste", um es zu aktivieren.
1. Drücken Sie die `Tab`-Taste, um sich durch die Optionen zu bewegen und drücken Sie dann `Eingabetaste` bei der gewünschten Option.

Die Optionen sind:

* "NVDA auf diesem Computer installieren": Dies ist die Hauptoption, die die meisten Benutzer für eine einfache Verwendung von NVDA wünschen.
* "Portable Version erstellen": Damit kann NVDA ohne Installation in einem beliebigen Ordner installiert werden.
Dies ist auf Computern ohne Administratorrechte oder auf einem Speicherstick zum Mitnehmen nützlich.
Wenn Sie diese Option auswählen, führt NVDA Sie durch die Schritte zur Erstellung einer portablen Version.
Das Wichtigste, was NVDA benötigt, ist der Ordner, in dem diese portable Version eingerichtet werden soll.
* "Weiter ausführen": Damit wird die temporäre NVDA-Version weiter ausgeführt.
Dies ist nützlich, um Funktionen in einer neuen Version zu testen, bevor sie installiert wird.
Wenn Sie diese Option auswählen, wird das Startfenster geschlossen und die temporäre Version von NVDA läuft weiter, bis sie beendet oder der PC heruntergefahren wird.
Beachten Sie, dass Änderungen an den Einstellungen nicht gespeichert werden.
* "Abbrechen": Schließt NVDA, ohne eine Aktion auszuführen.

Wenn Sie vorhaben, NVDA dauerhaft auf diesem Computer zu verwenden, sollten Sie sich für die Installation von NVDA entscheiden.
Die Installation von NVDA ermöglicht zusätzliche Funktionen wie den automatischen Start nach der Anmeldung, die Möglichkeit, die Windows-Anmeldung zu lesen und [sichere Bildschirme](#SecureScreens).
Dies ist bei portablen und temporären Versionen nicht möglich.
Ausführliche Informationen zu den Einschränkungen beim Ausführen einer portablen oder temporären NVDA-Versionen finden Sie unter [Einschränkungen bei einer portablen und temporären Versionen](#PortableAndTemporaryCopyRestrictions).

Die Installation bietet auch die Möglichkeit, Startmenü- und Desktop-Verknüpfungen zu erstellen und NVDA mit `Strg+Alt+N` zu starten.

#### Schritte zur Installation von NVDA über den Launcher {#StepsForInstallingNVDAFromTheLauncher}

Diese Schritte führen Sie durch die gängigsten Setup-Optionen.
Weitere Einzelheiten zu den verfügbaren Optionen finden Sie unter [Installations-Optionen](#InstallingNVDA).

1. Vergewissern Sie sich im Launcher, dass das Kontrollkästchen zum Akzeptieren der Lizenz aktiviert ist.
1. Drücken Sie die `Tab`-Taste und aktivieren Sie die Schaltfläche "NVDA auf diesem Computer installieren".
1. Als Nächstes folgen Optionen zur Verwendung von NVDA bei der Windows-Anmeldung und zum Erstellen einer Desktop-Verknüpfung.
Diese sind standardmäßig aktiviert.
Wenn Sie möchten, können Sie mit den Tasten `Tab` und `Leertaste` eine dieser Optionen ändern oder die Standard-Einstellungen beibehalten.
1. Drücken Sie die `Eingabetaste`, um fortzufahren.
1. Es erscheint ein Windows-Dialogfeld "Benutzerkontensteuerung (UAC)" mit der Abfrage "Möchten Sie dieser Anwendung erlauben, Änderungen an Ihrem PC vorzunehmen?
1. Drücken Sie `Alt+J`, um diese Aufforderung zu akzeptieren.
1. Ein Fortschrittsbalken läuft während der Installation von NVDA durch.
Während dieses Vorgangs gibt NVDA einen immer höher werdenden Signalton von sich.
Dieser Prozess verläuft oft schnell und wird möglicherweise nicht bemerkt.
1. Ein Dialogfeld wird angezeigt, in dem bestätigt wird, dass die Installation von NVDA erfolgreich war.
In dieser Meldung den Schalter "OK" betätigen, um die installierte Version zu starten.
Einfach die `Eingabetaste` drücken, um die installierte Version zu starten.
1. Das Dialogfeld "Willkommen bei NVDA" wird angezeigt, und NVDA liest eine Willkommensmeldung vor.
Die Dropdown-Liste "Tastatur-Layout" wird fokussiert.
Das Tastatur-Layout "Desktop" verwendet standardmäßig den Nummernblock für einige Funktionen.
Falls gewünscht, drücken Sie die `Pfeiltaste nach unten`, um das Tastatur-Layout "Laptop" auszuwählen, um die Funktionen des Nummernblocks anderen Tasten zuzuordnen.
1. Drücken Sie die `Tab`-Taste, um zu "`Dauergroßschreibtaste` als NVDA-Taste verwenden" zu gelangen.
Standardmäßig wird die `Einfügen`-Taste als NVDA-Modifikator-Taste eingestellt.
Drücken Sie `Leertaste`, um die `Dauergroßschreibtaste` als alternative Modifikator-Taste auszuwählen.
Beachten Sie, dass das Tastatur-Layout getrennt von der NVDA-Modifikator-Taste eingestellt wird.
Die NVDA-Taste und das Tastatur-Layout können später in den Tastatur-Einstellungen geändert werden.
1. Benutzen Sie die `Tab`-Taste und die `Leertaste`, um die anderen Optionen auf diesem Bildschirm einzustellen.
Hier wird festgelegt, ob NVDA automatisch gestartet werden soll.
1. Betätigen Sie die `Eingabetaste`, um das Dialogfeld zu schließen, sobald NVDA nun läuft.

### NVDA ausführen {#RunningNVDA}

Das vollständige NVDA-Benutzerhandbuch enthält alle NVDA-Befehle, unterteilt in verschiedene Abschnitte zum Nachschlagen.
Die Befehlstabellen sind auch in der "Befehls-Kurzreferenz" verfügbar.
Das NVDA-Schulungsmodul "Grundschulung für NVDA" geht auf die einzelnen Befehle näher ein und führt Sie Schritt für Schritt durch die Übungen.
Die "Grundschulung für NVDA" ist über den [NV Access Shop](http://www.nvaccess.org/shop) erhältlich.

Nachstehend sind einige grundlegende Befehle aufgeführt, die häufig verwendet werden.
Alle Befehle sind konfigurierbar, daher sind dies die Standardtasten für diese Funktionen.

#### Die NVDA-Modifier-Taste {#NVDAModifierKey}

Die Standard-NVDA-Modifier-Taste ist entweder die `Nummernblock 0`, (mit `Nummernblock` aus), oder die `Einfügen`-Taste, in der Nähe der `Entf`-Taste, `Pos1`- und `Ende`-Tasten.
Die NVDA-Modifier-Taste kann auch auf die `Dauergroßschreibtaste` gelegt werden.

#### Die Eingabehilfe {#InputHelp}

Um die Lage der Tasten zu lernen und zu üben, drücken Sie `NVDA+1`, um die Eingabehilfe einzuschalten.
Im Eingabehilfemodus wird beim Ausführen eines beliebigen Tastenbefehls (z. B. Drücken einer Taste oder Ausführen einer Touch-Geste) die Aktion mitgeteilt und beschrieben, was sie bewirkt (wenn überhaupt).
Die eigentlichen Befehle werden im Eingabehilfemodus nicht ausgeführt.

#### NVDA starten und beenden {#StartingAndStoppingNVDA}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Start NVDA |`control+alt+n` |`control+alt+n` |Starts or restarts NVDA|
|Exit NVDA |`NVDA+q`, then `enter` |`NVDA+q`, then `enter` |Exits NVDA|
|Pause or restart speech |`shift` |`shift` |Instantly pauses speech. Pressing it again will continue speaking where it left off|
|Stop speech |`control` |`control` |Instantly stops speaking|

#### Text vorlesen {#ReadingText}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Alles Lesen |`NVDA+Pfeiltaste nach unten` |`NVDA+A` |Beginnt an der aktuellen Position mit dem Lesen und zieht  den Fokus dabei mit.|
|Aktuelle Zeile vorlesen |`NVDA+Pfeiltaste nach oben` |`NVDA+L` |Liest die Zeile vor. Zweimaliges Drücken buchstabiert die Zeile. Dreimaliges Drücken buchstabiert die Zeile unter Verwendung von Zeichenbeschreibungen (Alpha, Bravo, Charlie, etc.).|
|Auswahl vorlesen |`NVDA+Umschalt+Pfeiltaste nach oben` |`NVDA+Umschalt+S` |Liest markierten Text vor. Zweimaliges Drücken buchstabiert diesen und dreimaliges Drücken buchstabiert ihn phonetisch.|
|Text aus der Zwischenablage vorlesen |`NVDA+C` |`NVDA+C` |Liest beliebigen Text aus der Zwischenablage vor. Zweimaliges Drücken buchstabiert diesen und dreimaliges Drücken buchstabiert ihn phonetisch.|

#### Meldung des Standorts und weiterer Informationen {#ReportingLocation}

| Name |Desktop-Taste |Laptop-Taste |Beschreibung|
|---|---|---|---|
|Fenstertitel mitteilen |`NVDA+T` |`NVDA+T` |Zeigt den Titel des derzeit aktiven Fensters an. Durch zweimaliges Drücken wird die Information buchstabiert. Durch dreimaliges Drücken wird die Information in die Zwischenablage kopiert.|
|Focus mitteilen |`NVDA+Tab` |`NVDA+Tab` |Teilt das aktuelle Steuerelement mit, welches den Fokus hat. Zweimaliges Drücken buchstabiert die Informationen und dreimaliges Drücken buchstabiert diese phonetisch.|
|Fenster vorlesen |`NVDA+B` |`NVDA+B` |Liest den gesamten Inhalt des Fensters vor (nützlich für Dialogfelder).|
|Statusleiste mitteilen |`NVDA+Ende` |`NVDA+Umschalt+Ende` |Teilt den Inhalt der Statusleiste mit, wenn NVDA eine findet. Durch zweimaliges Drücken wird die Information buchstabiert. Durch dreimaliges Drücken wird die Information in die Zwischenablage kopiert.|
|Datum und Uhrzeit mitteilen |`NVDA+F12` |`NVDA+F12` |Durch einmaliges Drücken wird die aktuelle Uhrzeit angesagt, durch zweimaliges Drücken das Datum. Die Uhrzeit und das Datum werden in dem Format angezeigt, das in den Windows-Einstellungen für die Uhr in der Taskleiste festgelegt ist.|
|Textformatierung mitteilen |`NVDA+F` |`NVDA+F` |Teilt die Textformatierung mit. Zweimaliges Drücken zeigt die Informationen in einem Fenster an.|
|Link-Zieladresse mitteilen |`NVDA+K` |`NVDA+K` |Bei einmaligem drücken wird die Zieladresse des Links an der aktuellen Cursor- oder Fokus-Position ausgegeben. Bei zweimaligem Drücken wird sie in einem Fenster zur genaueren Überprüfung angezeigt.|

#### Umschalten, welche Informationen NVDA vorliest {#ToggleWhichInformationNVDAReads}

| Name |Desktop-Taste |Laptop-Taste |Beschreibung|
|---|---|---|---|
|Zeichen während der Eingabe ansagen |`NVDA+2` |`NVDA+2` |Wenn diese Funktion aktiviert ist, liest NVDA alle Zeichen vor, die Sie auf der Tastatur eingeben.|
|Wörter während der Eingabe ansagen |`NVDA+3` |`NVDA+3` |Wenn diese Funktion aktiviert ist, liest NVDA das Wort vor, das Sie auf der Tastatur eingeben.|
|Tastenbefehle ansagen |`NVDA+4` |`NVDA+4` |Wenn diese Funktion aktiviert ist, nennt NVDA alle Tasten, die keine Buchstaben sind und die Sie auf der Tastatur eingeben. Dazu gehören auch Tastenkombinationen wie Steuerung plus ein weiterer Buchstabe.|
|Mausverfolgung einschalten |`NVDA+M` |`NVDA+M` |Wenn diese Funktion aktiviert ist, zeigt NVDA den Text an, der sich unter dem Mauszeiger befindet, wenn Sie ihn auf dem Bildschirm bewegen. So können Sie Dinge auf dem Bildschirm finden, indem Sie die Maus bewegen, anstatt zu versuchen, sie über die Objekt-Navigation zu finden.|

#### Der Sprachausgaben-Einstellungsring {#TheSynthSettingsRing}

| Name |Desktop-Taste |Laptop-Taste |Beschreibung|
|---|---|---|---|
|Zur nächsten Sprachausgaben-Einstellung wechseln |`NVDA+Strg+Pfeiltaste nach rechts` |`NVDA+Umschalt+Strg+Pfeiltaste nach rechts` |Wechselt zur nächsten verfügbaren Spracheinstellung nach der aktuellen und kehrt nach der letzten Einstellung wieder zur ersten Einstellung zurück.|
|Zur vorherigen Sprachausgaben-Einstellung wechseln |`NVDA+Strg+Pfeiltaste nach links` |`NVDA+Umschalt+Strg+Pfeiltaste nach links` |Wechselt zur nächsten verfügbaren Spracheinstellung vor der aktuellen und geht zur letzten Einstellung nach der ersten.|
|Erhöhen der aktuellen Sprachausgaben-Einstellung |`NVDA+Strg+Pfeiltaste nach oben` |`NVDA+Umschalt+Strg+Pfeiltaste nach oben` |Erhöht die aktuelle Spracheinstellung, auf der Sie sich befinden. Erhöht z. B. die Geschwindigkeit, wählt die nächste Stimme aus, erhöht die Lautstärke.|
|Erhöhen der aktuellen Sprachausgaben-Einstellung in größeren Schritten |`NVDA+Strg+Seite nach oben` |`NVDA+Umschalt+Strg+Seite nach oben` |Erhöht den Wert der aktuellen Sprachausgaben-Einstellung, auf der Sie sich befinden, in größeren Schritten. Wenn Sie sich z. B. auf einer Stimmen-Einstellung befinden, springt der Wert alle 20 Stimmen vorwärts; wenn Sie sich auf Schiebereglereinstellungen (Geschwindigkeit, Tonhöhe, etc.) befinden, springt der Wert um bis zu 20 % vorwärts.|
|Verringern der aktuellen Sprachausgaben-Einstellung |`NVDA+Strg+Pfeiltaste nach unten` |`NVDA+Umschalt+Strg+Pfeiltaste nach unten` |Verringert die aktuelle Spracheinstellung, auf der Sie sich befinden. Verringert z. B. die Geschwindigkeit, wählt die vorherige Stimme aus, verringert die Lautstärke.|
|Verringern der aktuellen Sprachausgaben-Einstellung in größeren Schritten |`NVDA+Strg+Seite nach unten` |`NVDA+Umschalt+Strg+Seite nach unten` |Verringert den Wert der aktuellen Sprachausgaben-Einstellung, auf der Sie sich befinden, in größeren Schritten. Wenn Sie sich z. B. auf einer Stimmen-Einstellung befinden, springt der Wert alle 20 Stimmen rückwärts; wenn Sie sich auf einer Schiebereglereinstellung (Geschwindigkeit, Tonhöhe, etc.) befinden, springt der Wert um bis zu 20 % rückwärts.|

Es ist auch möglich, den ersten oder letzten Wert der aktuellen Sprachausgaben-Einstellung zu setzen, indem Sie benutzerdefinierte Tastenbefehle im [Dialogfeld für die Tastenbefehle](#InputGestures), dort die Kategorie "Sprachausgabe" auswählen und diese dann zuweisen.
Das bedeutet, dass zum Beispiel bei der Einstellung einer Geschwindigkeit den Wert auf 0 oder 100 festgelegt wird.
Wenn Sie sich in einer Sprachausgaben-Einstellung befinden, wird die erste oder letzte Stimme eingestellt.

#### Im Web navigieren {#WebNavigation}

Die vollständige Liste der Navigationstasten finden Sie im Abschnitt [Lesemodus](#BrowseMode) des Benutzerhandbuchs.

| Befehl |Tastenkombination |Beschreibung|
|---|---|---|
|Überschrift |`H` |Weiter zur nächsten Überschrift.|
|Überschriftebene 1, 2, oder 3 |`1`, `2`, `3` |Zur nächsten Überschrift auf der angegebenen Ebene wechseln.|
|Formularfeld |`F` |Wechselt zum nächsten Formularfeld (Eingabefeld, Schaltfläche, etc.).|
|Link |`K` |Wechselt zum nächsten Link.|
|Sprungmarke |`D` |Wechselt zur nächsten Sprungmarke.|
|Liste |`L` |Wechselt zur nächsten Liste.|
|Tabelle |`T` |Wechselt zur nächsten Tabelle.|
|Rückwärts gehen |`Umschalt+Buchstabe` |Drücken Sie `Umschalten` und einen der oben genannten Buchstaben, um zum vorherigen Element dieses Typs zu gelangen.|
|Liste der Elemente |`NVDA+F7` |Listet verschiedene Arten von Elementen auf, z. B. Links und Überschriften.|

### Die Einstellungen {#Preferences}

Die meisten NVDA-Funktionen können über die NVDA-Einstellungen aktiviert oder geändert werden.
Einstellungen und andere Optionen sind über das Menü von NVDA verfügbar.
Um das Menü von NVDA zu öffnen, drücken Sie `NVDA+N`.
Um das Dialogfeld mit den allgemeinen Einstellungen von NVDA direkt zu öffnen, drücken Sie `NVDA+Strg+G`.
Viele Einstellungsbereiche haben Tastenkombinationen, um sie direkt zu öffnen, z. B. `NVDA+Strg+S` für Sprachausgaben oder `NVDA+Strg+V` für andere Sprachausgaben-Optionen.

### Die Community {#Community}

NVDA hat eine Community von teils sehr aktiven Nutzern.
Es gibt eine zentrale [englischsprachige Mailing-Liste](https://nvda.groups.io/g/nvda) und eine Seite mit [lokalsprachigen Gruppen](https://github.com/nvaccess/nvda/wiki/Connect).
NV Access, der Hersteller von NVDA, ist auf [Twitter](https://twitter.com/nvaccess) und [Facebook](https://www.facebook.com/NVAccess) aktiv.
NV Access hat auch einen regelmäßigen [In-Process-Blog](https://www.nvaccess.org/category/in-process/).

Es gibt auch das Programm [Zertifizierte NVDA-Experten](https://certification.nvaccess.org/).
Dies ist eine Online-Prüfung, die Sie absolvieren können, um Ihre Kenntnisse in NVDA nachzuweisen.
[NVDA Certified Experts](https://certification.nvaccess.org/) kann ihre Kontaktdaten und relevanten Geschäftsinformationen auflisten.

### Hilfe holen {#GettingHelp}

Um Hilfe für NVDA zu erhalten, drücken Sie `NVDA+N`, um das Menü zu öffnen, dann `H` für Hilfe.
Aus diesem Untermenü können Sie auf das vollständige Benutzerhandbuch zugreifen, eine Kurzreferenz der Befehle, die neuen Funktionen und vieles mehr.
Diese ersten drei Optionen werden im Standard-Webbrowser geöffnet.
Umfassenderes Schulungsmaterial ist auch im [NV Access Shop](https://www.nvaccess.org/shop) erhältlich.

Wir empfehlen, mit dem Modul "Grundausbildung für NVDA" zu beginnen.
Dieses Modul deckt Konzepte von den ersten Schritten bis zum Browsen im Web und der Verwendung der Objektnavigation ab.
Es ist erhältlich in:

* [digitaler Form](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), die die Formate Word DOCX, Webseite HTML, eBook ePub und Kindle KFX umfassen.
* [Von einer Person  vorgelesen, MP3-Audio](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Hardcopy-UEB-Braille-Schrift](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) mit Auslieferung in der ganzen Welt.

Weitere Module und das vergünstigte [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/) sind im [NV Access Shop](https://www.nvaccess.org/shop/) erhältlich.

NV Access bietet auch kostenpflichtigen [Telefonsupport](https://www.nvaccess.org/product/nvda-telephone-support/) an, entweder in Blöcken oder als Teil des [NVDA-Produktivitätspaket](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Der telefonische Support umfasst lokale Nummern in Australien und den USA.

Die [E-Mail-Benutzergruppen](https://github.com/nvaccess/nvda/wiki/Connect) sind eine großartige Quelle für die Hilfe der Community, ebenso wie die [zertifizierten NVDA-Experten](https://certification.nvaccess.org/).

Sie können Fehlerberichte oder Funktionsanfragen über [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md) stellen.
Die [Beitragsrichtlinien](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) enthalten wertvolle Informationen für Beiträge zur Community.

## Weitere Setup-Optionen {#MoreSetupOptions}
### Installations-Optionen {#InstallingNVDA}

Wenn Sie NVDA direkt aus dem heruntergeladenen NVDA-Startprogramm installieren, klicken Sie auf die Schaltfläche NVDA installieren.
Falls Sie den Eingangsdialog bereits geschlossen haben oder NVDA von einer portablen Version aus installieren wollen, wählen Sie den Menüpunkt "NVDA installieren" aus dem Untermenü "Werkzeuge".

In dem daraufhin angezeigten Dialogfeld der Installation wird bestätigt, dass Sie NVDA installieren möchten, und es wird auch angegeben, ob diese Installation eine frühere Installation aktualisieren soll.
Wenn Sie auf den Schalter "Fortfahren" klicken, wird die Installation gestartet.
Es gibt allerdings noch weitere Optionen. Diese werden weiter unten beschrieben.
Nach dem Abschluss der Installation erscheint eine Meldung, die Sie über den erfolgreichen Abschluss der Installation informiert.
Wenn Sie hier "OK" auswählen, wird die soeben installierte NVDA-Version gestartet.

#### Warnung bei inkompatiblen NVDA-Erweiterungen {#InstallWithIncompatibleAddons}

Wenn Sie NVDA-Erweiterungen bereits installiert haben, kann möglicherweise eine Warnung erscheinen, dass inkompatible NVDA-Erweiterungen deaktiviert werden.
Bevor Sie auf die Schaltfläche "Fortfahren" klicken können, müssen Sie zuerst über das Kontrollkästchen bestätigen, dass Sie mit der Deaktivierung inkompatibler NVDA-Erweiterungen einverstanden sind.
Es ist auch eine Schaltfläche zur Überprüfung inkompatibler NVDA-Erweiterungen, welche nach der Installation deaktiviert werden, vorhanden.
Weitere Informationen zu dieser Schaltfläche finden Sie im Abschnitt [Inkompatible NVDA-Erweiterungen](#incompatibleAddonsManager).
Nach der Installation können Sie inkompatible NVDA-Erweiterungen auf eigene Gefahr über den [Store für NVDA-Erweiterungen](#AddonsManager) wieder aktivieren.

#### NVDA bei der Windows-Anmeldung verwenden {#StartAtWindowsLogon}

Mit dieser Option können Sie entscheiden, ob NVDA automatisch gestartet werden soll, während Sie sich in der Windows-Anmeldung befinden, bevor Sie ein Passwort eingegeben haben.
Dies betrifft auch die Benutzerkontensteuerung und [andere Sicherheitsmeldungen](#SecureScreens).
Diese Option ist standardmäßig während einer Neuinstallation aktiviert.

#### Desktop-Verknüpfung erstellen (Strg+Alt+N) {#CreateDesktopShortcut}

Mit dieser Option entscheiden Sie, ob NVDA eine Desktop-Verknüpfung anlegen soll.
Wenn Sie diese Verknüpfung erstellen, wird ihr auch die Tastenkombination `Strg+Alt+N` zugewiesen, so dass Sie NVDA jederzeit mit dieser Tastenkombination starten können.

#### Portable Konfiguration in das aktuelle Benutzerkonto kopieren {#CopyPortableConfigurationToCurrentUserAccount}

Hiermit legen Sie fest, ob NVDA die Konfiguration der momentan laufenden NVDA-Instanz in das Konfigurationsverzeichnis des aktuell angemeldeten Benutzers kopieren soll.
Dadurch wird weder die Konfiguration für andere Benutzer dieses Systems noch die Systemkonfiguration für die Verwendung während der Windows-Anmeldung und [anderer Sicherheitsmeldungen](#SecureScreens) kopiert.
Diese Option ist nur verfügbar, wenn NVDA aus einer portablen Version heraus installiert wird - nicht jedoch beim Ausführen einer heruntergeladenen Version.

### Erstellen einer portablen Version {#CreatingAPortableCopy}

Wenn Sie eine portable Version direkt aus dem NVDA-Downloadpaket erstellen möchten, klicken Sie auf die Schaltfläche "Portable Version erstellen".
Wenn Sie den Willkommensdialog bereits geschlossen haben oder gerade eine installierte NVDA-Version ausführen, können Sie über den Menüpunkt "Portable Version erstellen" aus dem Untermenü "Werkzeuge" eine portable Version anlegen.

Im folgenden Dialogfeld können Sie das Verzeichnis angeben, in dem die portable Version erstellt werden soll.
Dies kann ein Ordner auf einem Speichermedium sein.
Des Weiteren können Sie entscheiden, ob die Benutzer spezifischen Konfigurationsdateien und NVDA-Erweiterungen der aktuell laufenden NVDA-Instanz in die portable Version übernommen werden sollen.
Diese Option ist nur verfügbar, wenn die portable Version von einer installierten Version erstellt wird - nicht jedoch beim Ausführen einer heruntergeladenen Version.
Wenn Sie auf "Fortfahren" klicken, wird die portable Version erstellt.
Nach Abschluss des Vorgangs erscheint eine Meldung, die Sie über die erfolgreiche Erstellung informiert.
Klicken Sie auf "OK", um das Dialogfeld zu schließen.

### Beschränkungen für portable und temporäre Versionen {#PortableAndTemporaryCopyRestrictions}

Wenn Sie NVDA auf einem USB-Stick oder einem anderen beschreibbaren Medium mitnehmen möchten, sollten Sie eine portable Version erstellen.
Die installierte Version kann außerdem jederzeit eine portable Version von sich selbst erstellen.
Die portable Version kann man auch zu einem späteren Zeitpunkt auf einem beliebigen Computer installieren.
Wenn Sie NVDA jedoch auf ein schreibgeschütztes Medium wie eine CD kopieren möchten, sollten Sie nur das Download-Paket kopieren.
Die Ausführung der portablen Version direkt von schreibgeschützten Medien wird derzeit nicht unterstützt.

Die [NVDA-Setup-Datei](#StepsForRunningTheDownloadLauncher) kann als temporäre NVDA-Version verwendet werden.
In den temporär gestarteten NVDA-Versionen werden keine Einstellungen in der Konfiguration gespeichert.
Die Benutzung des [Store für NVDA-Erweiterungen](#AddonsManager) in NVDA ist ebenfalls davon ausgeschlossen.

Für portable und temporäre NVDA-Versionen gelten die folgenden Einschränkungen:

* Die Unfähigkeit, während und/oder nach der Anmeldung automatisch zu starten.
* Die Unfähigkeit, mit Anwendungen zu interagieren, die mit administrativen Rechten laufen, es sei denn, NVDA selbst wurde auch mit diesen Rechten ausgeführt (wird nicht empfohlen).
* Die Unfähigkeit, Bildschirme der Benutzerkontensteuerung (UAC) vorzulesen, sobald versucht wird, eine Anwendung mit administrativen Rechten zu starten.
* Die Unfähigkeit, Eingaben über einen Touchscreen zu unterstützen.
* Die Unfähigkeit, Funktionen wie den Lesemodus und das Vorlesen von Zeichen während der Eingabe in Apps aus dem Windows-Store anzubieten.
* Die Lautstärke anderer Audio-Quellen zu steuern wird nicht unterstützt.

## NVDA benutzen {#GettingStartedWithNVDA}
### NVDA starten {#LaunchingNVDA}

Wenn Sie NVDA bereits installiert haben, können Sie es entweder vom Desktop aus mit Strg+Alt+N aufrufen oder wählen Sie NVDA aus dem Startmenü unter Programme "NVDA" aus.
Optional können Sie auch im Dialogfeld "Ausführen" (Windows-Taste+R) den Befehl "NVDA" (ohne Anführungszeichen) eingeben und mit der Eingabetaste aufrufen.
Wenn NVDA bereits läuft, wird es neu gestartet.
Sie können auch einige [Kommandozeilenparameter](#CommandLineOptions) übergeben, mit denen Sie das Programm beenden (-q), NVDA-Erweiterungen deaktivieren (-disable-addons, etc.) können.

Bei installierten NVDA-Versionen werden die Konfigurationsdateien normalerweise im Roaming-Verzeichnis des aktuell angemeldeten Benutzers gespeichert (z. B. "`C:\Users\<Benutzer>\AppData\Roaming`").
Sie können NVDA jedoch so einstellen, dass die Konfigurationsdateien stattdessen im Lokalen Verzeichnis des aktuellen Benutzers gespeichert werden.
Weitere Informationen dazu finden Sie im Abschnitt [System-Parameter](#SystemWideParameters).

Um die portable NVDA-Version zu starten, wechseln Sie in den Ordner, in welchem Sie die Dateien entpackt haben und starten anschließend die Datei "NVDA.exe" mit der Eingabetaste oder mit einem Doppelklick.
Wenn NVDA bereits ausgeführt wurde, wird es automatisch gestoppt, bevor die portable Version gestartet wird.

Während des Startvorgangs hören Sie als Erstes eine aufsteigende Melodie.
Je nach dem, wie schnell Ihr Computer ist oder wenn Sie NVDA von einem USB-Stick oder einem anderen Medium aus starten, so kann das einen Moment dauern, bis der Prozess abgeschlossen ist.
Sollte der Vorgang dennoch sehr lange dauern, sollte NVDA sagen: "NVDA wird geladen.".

Wenn Sie entweder nichts hören oder von Windows oder NVDA einen Fehlerton oder eine absteigende Melodie hören, bedeutet das, dass eventuell ein Fehler aufgetreten ist.
Bitte lesen Sie erst auf der Homepage nach, ob gegebenenfalls etwas darüber bekannt ist oder wie das Problem zu beheben ist. Ansonsten melden Sie den Fehler bitte den Entwicklern.

#### Willkommensdialog {#WelcomeDialog}

Beim ersten Starten von NVDA wird Ihnen eine Dialogbox mit einigen grundlegenden Informationen über die NVDA-Taste und das NVDA-Menü angezeigt.
(Bitte beachten Sie weitere Themenabschnitte.)
Das Dialogfeld enthält zudem ein Kombinationsfeld und drei Kontrollfelder.
Mit dem Kombinationsfeld wählen Sie das Tastaturschema aus.
Mit dem ersten Kontrollkästchen können Sie steuern, ob NVDA die Dauergroßschreibtaste als NVDA-Taste verwenden soll.
Mit dem zweiten Kontrollkästchen können Sie bestimmen, ob NVDA nach der Anmeldung automatisch gestartet werden soll. Diese Option steht nur bei installierten NVDA-Versionen zur Verfügung.
Mit dem dritten Kontrollkästchen legen Sie fest, ob bei jedem Start der Willkommensdialog angezeigt werden soll.

#### Dialogfeld zur Datennutzungsstatistik {#UsageStatsDialog}

Seit NVDA 2018.3 wird der Benutzer gefragt, ob Nutzungsdaten an NV Access gesendet werden sollen, um in Zukunft zur Verbesserung von NVDA beizutragen.
Beim ersten Start von NVDA erscheint ein Dialogfeld, in dem Sie gefragt werden, ob Sie das Senden der Nutzungsdaten an NV Access während der Verwendung von NVDA akzeptieren möchten.
Weitere Informationen zu den von NV Access erfassten Daten finden Sie im Abschnitt "[NVDA-Nutzungsdaten sammeln und an NV Access übermitteln](#GeneralSettingsGatherUsageStats)" in "Allgemeine Einstellungen".
Hinweis: Durch Klicken auf "Ja" oder "Nein" wird diese Einstellung gespeichert. Das Dialogfeld erscheint nicht wieder, bis Sie NVDA neu installieren.
Sie können den Datenerhebungsprozess jedoch manuell in den NVDA-Einstellungen in der Kategorie "Allgemein" aktivieren oder deaktivieren. Um diese Einstellung manuell zu ändern, können Sie das Kontrollkästchen [NVDA-Nutzungsdaten sammeln und an NV Access übermitteln](#GeneralSettingsGatherUsageStats) aktivieren oder deaktivieren.

### Über die NVDA-Tastenkombinationen {#AboutNVDAKeyboardCommands}
#### Die NVDA-Taste {#TheNVDAModifierKey}

In NVDA bestehen die Tastenkombinationen zumeist aus einer oder mehreren Tasten in Kombination mit der NVDA-Taste.
Die Befehle zum Lesen von Text werden im Desktop-Tastaturschema hingegen mit den Tasten des Nummernblocks bedient. Des Weiteren gibt es einige weitere Ausnahmen.

NVDA kann so konfiguriert werden, dass die Einfüge-Taste des Nummernblocks, Erweiterte Einfüge-Taste und/oder die Dauergroßschreibtaste als NVDA-Taste verwendet werden können.
Die Einfüge-Taste des Nummernblocks sowie die Einfüge-Taste der erweiterten Tastatur sind standardmäßig als NVDA-Taste vordefiniert.

Bei Bedarf können Sie an Stelle der NVDA-Taste die Originalfunktion auslösen, indem Sie die entsprechende Taste zwei Mal kurz hintereinander betätigen. Wenn Sie beispielsweise die Dauergroßschreibtaste dafür festgelegt haben, können Sie diese Taste trotzdem noch ein- und ausschalten, indem Sie sie zweimal drücken.

#### Die Tastaturschemata {#KeyboardLayouts}

NVDA ist derzeit mit zwei Typen von Tastenkombinationen (Tastaturschemata) ausgestattet. Es gibt eines für Desktops und eines für Laptops.
Voreingestellt ist das Tastaturschema Desktop. Sie können natürlich das Schema in den NVDA-Einstellungen unter der Kategorie [Tastatur](#Keyboard) auch auf Laptop umschalten.

Das Desktop-Schema nutzt den Nummernblock (wenn dieser ausgeschaltet ist).
Obwohl die meisten Laptop-Tastaturen keinen physikalischen Nummernblock haben, kann dieser mit Hilfe der FN-Taste in Kombination mit den Tasten des rechten Tastenfeldes emuliert werden. Dies sind die Tasten: 7, 8, 9, u, i, o, j, k, l, etc.).
Wenn Ihr Laptop dies oder die Deaktivierung des Nummernblocks nicht unterstützt, können Sie an Stelle das Tastaturschema auf Laptop umstellen.

### Touchscreen-Bedienung mit NVDA {#NVDATouchGestures}

Wenn Sie NVDA auf einem Gerät mit Touchscreen benutzen, können Sie NVDA auch direkt über Touch-Eingaben bedienen.
Während NVDA läuft, gehen alle Touch-Eingaben direkt an NVDA, es sei denn, die Unterstützung der Touchscreen-Bedienung ist deaktiviert.
Dies bedeutet, dass alle Touch-Eingaben, die ohne NVDA funktioniert hätten, außer Kraft sind, sobald NVDA ausgeführt wird.
<!-- KC:beginInclude -->
Mit NVDA+Strg+Alt+T können Sie die Unterstützung der Touchscreen-Bedienung umschalten.
<!-- KC:endInclude -->
Sie können auch die [Unterstützung der Touchscreen-Bedienung](#TouchSupportEnable) in der Kategorie "Touchscreen-Bedienung" in den NVDA-Einstellungen aktivieren oder deaktivieren.

#### Den Bildschirminhalt erkunden {#ExploringTheScreen}

Zu den grundlegenden Aktionen beim Umgang mit Tastschirmen gehört das Ansagen von Objekten oder Text direkt unter Ihrem Finger.
Hierfür können Sie einfach den Bildschirm an einer beliebigen Stelle berühren.
Sie können den Finger dann auch über den Bildschirm bewegen, um Text und Steuerelemente, auf die Sie treffen, angesagt zu bekommen.

#### Berührungsgesten {#TouchGestures}

Weiter unten im Handbuch finden Sie bei den Beschreibungen zu den NVDA-Befehlen auch Gesten, mit denen die betreffenden Befehle ausgeführt werden können, wenn Sie einen Touchscreen verwenden.
In den folgenden Abschnitten finden Sie Anweisungen, wie bestimmte Gesten mit dem Touchscreen verwendet werden.

##### Tippen {#toc45}

Tippen Sie schnell mit einem oder mehreren Fingern

Einmal Tippen mit einem Finger wird im Folgenden einfach als Tippen bezeichnet.
Gleichzeitiges Tippen mit zwei Fingern wird als Zwei-Finger-Tippen bezeichnet, etc.

Wenn Sie mehrmals in schneller Folge mit einem oder mehreren Fingern tippen, wird NVDA dies als Mehrfach-Tipp-Geste erkennen.
Zweimal Tippen wird als Doppel-Tippen erkannt.
Dreimal Tippen wird als Dreifach-Tippen erkannt, etc.
Dabei werden ebenfalls die Anzahl der verwendeten Finger erkannt. Ein Doppel-Tippen mit drei Fingern wird dabei ebenso erkannt, wie ein einfaches Tippen mit vier Fingern.

##### Wischen {#toc46}

Hierbei müssen Sie schnell über den Bildschirm wischen.

Abhängig von der Richtung gibt es vier Wischgesten: nach links, nach rechts, nach oben und nach unten.

Wie bei den Gesten zum Tippen, können auch hier mehrere Finger gleichzeitig verwendet werden.
Das Wischen mit zwei Fingern nach oben wird dabei ebenso erkannt wie das Wischen mit vier Fingern nach links.

#### Arbeitsmodi {#TouchModes}

Da es weitaus mehr NVDA-Befehle als Touch-Eingaben gibt, wurden mehrere Arbeitsmodi eingeführt, die jeweils eine Untermenge von NVDA-Befehlen zur Verfügung stellen.
Dies ist einerseits der Textmodus und andererseits der Objektmodus.
Einige NVDA-Befehle werden in den Tabellen zusammen mit einer Touch-Eingabe auf dem Touchscreen aufgelistet, gefolgt von einem Arbeitsmodus in Klammern.
Die Angabe "Wischen nach oben (Textmodus)" bedeutet beispielsweise, dass der entsprechende Befehl durch Wischen nach oben mit einem Finger, nur möglich im Textmodus, ausgeführt werden kann.
Ist kein Arbeitsmodus angegeben, so funktioniert der Befehl in allen Arbeitsmodi.

<!-- KC:beginInclude -->
Um zwischen den Arbeitsmodi zu wechseln, tippen Sie einmal mit drei Fingern.
<!-- KC:endInclude -->

#### Die Bildschirm-Tastatur {#TouchKeyboard}

Die Bildschirm-Tastatur wird auf Touchscreens verwendet, um Text und Befehle einzugeben.
Wenn ein Eingabefeld hervorgehoben wird, können Sie die Bildschirmtastatur durch doppeltippen des entsprechenden Symbols am unteren Bildschirmrand aufrufen.
Bei Tablets, wie dem Microsoft Surface Pro, ist die Bildschirm-Tastatur immer verfügbar, wenn die Tastatur nicht verbunden ist.
Um die Bildschirm-Tastatur auszublenden, doppeltippen Sie auf das Symbol der Bildschirm-Tastatur oder wischen Sie vom Eingabefeld weg.

So finden Sie Tasten bei aktiver Bildschirmtastatur: Bewegen Sie Ihren Finger in den unteren Bildschirmbereich. Hier sollten Sie die Tastatur finden. Nun bewegen Sie einen Finger über die Tastatur.
Wenn Sie nun die zu drückende Taste gefunden haben, führen Sie einen Doppeltipp aus, oder heben einfach den Finger an. Das gewünschte verhalten legen Sie in der Kategorie [Touch-Interaktionen](#TouchInteraction) in den NVDA-Einstellungen fest.

### Die Eingabehilfe {#InputHelpMode}

Viele NVDA-Befehle werden in den folgenden Abschnitten des Benutzerhandbuches aufgelistet, können aber allesamt bei eingeschalteter Eingabehilfe abgefragt werden.

Zum Einschalten der Eingabehilfe drücken Sie die Tastenkombination NVDA+1.
Zum Ausschalten betätigen Sie die Tastenkombination erneut.
Bei eingeschalteter Eingabehilfe erhalten Sie bei jeder Eingabe - sei es eine Tastenkombination auf der Tastatur, eine Taste an einer Braillezeile oder eine Geste auf einem Touchscreen - Informationen über deren zugewiesene Funktionen, sofern sie mit einer Funktion belegt sind.
Die Tasten und Tastenkombinationen führen ihre Funktion nicht aus, so lange Sie die Eingabehilfe eingeschaltet haben. Dies bedeutet, dass Sie jede beliebige Tastenkombination betätigen können.

### Das NVDA-Menü {#TheNVDAMenu}

In diesem Menü können Sie alle Einstellungen von NVDA ändern, die Einstellungen speichern oder zurücksetzen, die Hilfe aufrufen, die Wörterbücher für die Aussprache bearbeiten, zusätzliche Funktionen aufrufen und auch NVDA komplett beenden.

Um das NVDA-Menü von einer beliebigen Stelle in Windows zu erreichen, während NVDA läuft, können Sie einen der folgenden Schritte ausführen:

* Drücken Sie `NVDA+N` auf der Tastatur.
* Führen Sie einen Doppeltipp mit zwei Fingern auf dem Touchscreen aus.
* Rufen Sie den Infobereich auf, indem Sie `Windows+B` drücken, mit den Pfeiltasten das NVDA-Symbol auswählen und die `Eingabetaste` drücken.
* Alternativ können Sie den Infobereich aufrufen, indem Sie die Tastenkombination `Windows+B` drücken, mit den Pfeiltaste das NVDA-Symbol auswählen und das Kontextmenü öffnen, indem Sie die `Kontext-Taste` drücken, die sich auf den meisten Tastaturen neben der rechten Strg-Taste befindet.
Auf einer Tastatur ohne `Kontextmenü`-Taste drücken Sie stattdessen `Umschalt+F10`.
* Klicken Sie mit der rechten Maustaste auf das NVDA-Symbol im Infobereich von Windows

Wenn das Menü erscheint, können Sie mit den Pfeiltasten durch das Menü navigieren und mit der `Eingabetaste` einen Eintrag aktivieren.

### Allgemeine NVDA-Befehle {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Geste |Beschreibung|
|---|---|---|---|---|
|NVDA starten oder neustarten |Strg+Alt+N |Strg+Alt+N |Keine |Startet NVDA vom Desktop (neu), sofern diese Tastenkombination während der NVDA-Installation aktiviert wurde. Dies ist eine Windows-spezifische Verknüpfung und kann daher im Dialogfeld für die Tastenbefehle nicht neu zugewiesen werden.|
|Sprachausgabe unterbrechen |Strg |Strg |zwei-Finger-tippen |unterbricht augenblicklich den laufenden Sprechvorgang.|
|Sprachausgabe anhalten/fortsetzen |Umschalt |Umschalt |Keine |Hält sofort den Lesevorgang an oder setzt bei erneutem Drücken den Lesevorgang fort (sofern das von der Sprachausgabe unterstützt wird).|
|NVDA-Menü |NVDA+N |NVDA+N |Zwei-Finger-Doppel-Tippen |Öffnet das NVDA-Menü. Von hier aus können Sie auf die Einstellungen, Werkzeuge, Hilfe, etc. zugreifen.|
|Modus der Eingabehilfe umschalten |NVDA+1 |NVDA+1 |Keine |In diesem Modus wird beim Drücken einer Taste die in NVDA assoziierte Taste und die dazugehörige Beschreibung angesagt und in Braille angezeigt.|
|NVDA beenden |NVDA+Q |NVDA+Q |Keine |Beendet NVDA.|
|Taste durchreichen |NVDA+F2 |NVDA+F2 |Keine |Veranlasst NVDA, dass die nächst betätigte Taste nicht von NVDA abgefangen wird, sondern direkt an die laufende Anwendung weitergereicht wird (sogar, wenn es sich um einen Tastenbefehl von NVDA handelt).|
|Schlafmodus umschalten |NVDA+Umschalt+S |NVDA+Umschalt+Z |Keine |In diesem Modus werden alle NVDA-Befehle und die Sprach- und Braille-Ausgabe für die aktuelle Anwendung deaktiviert. Dies ist besonders nützlich in Anwendungen, die eigene Sprach- oder Bildschirmlesefunktionen zur Verfügung stellen. Drücken Sie diesen Befehl erneut, um den Schlafmodus zu deaktivieren - beachten Sie dabei, dass NVDA nur die Einstellung des Schlafmodus bis zum nächsten Neustart von NVDA beibehält.|

<!-- KC:endInclude -->

### System-Informationen ausgeben {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Datum/Uhrzeit ausgeben |NVDA+F12 |Bei einmal Drücken wird das Datum und bei zweimal Drücken wird die Uhrzeit ausgegeben.|
|Akku-Status ansagen |NVDA+Umschalt+B |Sagt den Ladezustand des Akkus an, sofern ein Akkumulator angeschlossen ist.|
|Text der Zwischenablage ansagen |NVDA+C |Liest den Inhalt der Zwischenablage vor.|

<!-- KC:endInclude -->

### Sprachmodi {#SpeechModes}

Der Sprachmodus regelt, wie Bildschirminhalte, Benachrichtigungen, Reaktionen auf Befehle und andere Ausgaben während des Betriebs von NVDA gesprochen werden.
Der Standardmodus ist „Sprechen“, der in Situationen spricht, die bei der Verwendung eines Screenreaders zu erwarten sind.
Unter bestimmten Umständen oder beim Ausführen bestimmter Programme kann es jedoch sinnvoll sein, einen der anderen Sprachmodi zu verwenden.

Die vier verfügbaren Sprachmodi sind:

* Sprechen (Standard): NVDA reagiert normal auf Bildschirmänderungen, Benachrichtigungen und Aktionen wie das Verschieben des Fokus oder das Erteilen von Befehlen.
* Bei Bedarf: NVDA spricht nur, wenn Sie Befehle mit einer Rückmeldungsfunktion verwenden (z. B. den Titel des Fensters melden). Es wird jedoch nicht als Reaktion auf Aktionen wie das Bewegen des Fokus oder des Cursors gesprochen.
* Aus: NVDA spricht nichts, reagiert jedoch im Gegensatz zum Schlafmodus lautlos auf Befehle.
* Signaltöne: NVDA ersetzt die normale Sprache durch kurze Signaltöne.

Der Modus Signaltöne kann nützlich sein, wenn eine sehr ausführliche Ausgabe in einem Terminalfenster gescrollt wird. In diesen Fällen ist der Inhalt egal und man will nur wissen, dass die Meldungen weiterscrollen. Des Weiteren gibt es auch andere Situationen, in denen der Inhalt nicht wichtig ist, man lediglich wissen will, dass etwas ausgegeben wird.

Der Modus bei Bedarf kann passend sein, wenn Sie kein ständiges Feedback darüber benötigen, was auf dem Bildschirm oder am Computer passiert, Sie aber regelmäßig bestimmte Dinge mithilfe von Überprüfungsbefehlen o. ä. überprüfen müssen.
Beispiele hierfür sind die Audioaufnahme, die Verwendung der Bildschirmvergrößerung, während Besprechungen bzw. Telefonaten oder als Alternative zum Modus Signaltöne.

Mit einer Tastenkombination können Sie zwischen den verschiedenen Sprachmodi wechseln:
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Sprachmodus wechseln |`NVDA+s` |Wechselt zwischen den Sprachmodi.|

<!-- KC:endInclude -->

Wenn Sie nur zwischen einer begrenzten Untergruppe von Sprachmodi wechseln müssen, finden Sie unter [verfügbare Modi im Befehl Sprachmodus wechseln](#SpeechModesDisabling) eine Möglichkeit, unerwünschte Modi zu deaktivieren.

## Mit NVDA navigieren {#NavigatingWithNVDA}

NVDA stellt zahlreiche Werkzeuge zum Erkunden von und Navigieren in Anwendungen bereit, darunter die Objektnavigation und den Bildschirm-Betrachter.

### Die Objekte {#Objects}

Jede Anwendung sowie das Betriebssystem selbst besteht aus vielen Objekten.
Ein Objekt ist ein einzelner Eintrag, wie z. B.: eine Textpassage, ein Schalter, ein Kontrollfeld, ein Regler, eine Liste oder ein Eingabefeld.

### Mit dem System-Fokus navigieren {#SystemFocus}

Der System-Fokus, auch Fokus genannt, ist dasjenige [Objekt](#Objects), welches die Tastendrücke von der Tastatur entgegennimmt.
Ein Beispiel: Wenn Sie einen Text in einem Eingabefeld eingeben, wird dieses hervorgehoben.

Die gebräuchlichste Art, sich in einer Windows-Anwendung zu bewegen sind Windows-Standard-Tastenkombinationen, mit denen der System-Fokus bewegt wird. Beispiele für solche Standard-Tastenkombinationen sind Tab und Umschalt+Tab zum Wechseln zwischen Elementen in einem Dialogfeld, Alt-Taste oder F10 zum Aufrufen der Menüleiste und die Pfeiltasten zur Navigation innerhalb eines Menüs sowie alt+Tab zum Wechseln zwischen laufenden Anwendungen
Wenn Sie auf diese Weise navigieren, wird NVDA verschiedene Informationen über das Objekt ausgeben, welches den Fokus erhält. Hierzu zählen: Name, Beschreibung (erscheint meist als Sprechblase, wenn der Anwender die Maus über das betreffende Objekt zieht), Typ (Schalter, Kontrollkästchen, Eingabefeld, etc.), Wert (z. B., der aktuelle Inhalt eines Eingabefeldes), Positionsangabe (z. B. "1 von 5" in einer Liste oder "1 von 1 Ebene 0" in einer Baumansicht), den Status des Objektes (z. B. aktiviert, hervorgehoben, ausgewählt, etc.).
Wenn [Visuell hervorheben](#VisionFocusHighlight) aktiviert ist, wird die Position des aktuellen System-Fokus auch visuell dargestellt.

Einige nützliche Tastenkombinationen zum Navigieren mit dem System-Fokus sind:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Beschreibung|
|---|---|---|---|
|Aktuellen Fokus ansagen |NVDA+Tabulatortaste |NVDA+Tabulatortaste |Spricht das aktuell hervorgehobene Objekt. Bei zweimal Drücken werden die Informationen buchstabiert.|
|Titelleiste ansagen |NVDA+T |NVDA+T |Liest die Titelleiste der aktuellen Anwendung vor. Bei zweimal Drücken, werden die Informationen buchstabiert. Bei dreimal Drücken wird der Text in die Zwischenablage kopiert. Diese Information wird auch in Braille angezeigt.|
|Aktives Fenster vorlesen |NVDA+B |NVDA+B |Liest alle Steuerelemente im aktiven Fenster vor (hilfreich für Dialogfelder).|
|Statuszeile ausgeben |NVDA+Ende |NVDA+Umschalt+Ende |Liest die Statusleiste vor, falls vorhanden. Durch zweimaliges Drücken werden die Informationen buchstabiert. Durch dreimaliges Drücken werden die Informationen in die Zwischenablage kopiert.|
|Kurztaste ausgeben |`Umschalt+Nummernblock 2` |`NVDA+Strg+Umschalt+Punkt` |Gibt das Tastenkürzel (Taste) des aktuell fokussierten Objekts aus.|

<!-- KC:endInclude -->

### Mit dem System-Cursor navigieren {#SystemCaret}

Wenn ein [Objekt](#Objects) den [Fokus](#SystemFocus) hat, welches das Bearbeiten von Text erlaubt, können Sie sich mit Hilfe des System-Cursors durch dessen Inhalt bewegen. Der System-Cursor wird in diesem Zusammenhang oft auch als Einfügemarke bezeichnet.

Sie können in diesem Fall die Pfeiltasten, Bild Auf, Bild Ab, Pos1, Ende, etc. verwenden, um durch den Text zu navigieren.
Falls das Steuerelement eine Bearbeitung zulässt, können Sie auch den Text verändern.
NVDA wird hierbei jedes Zeichen, jedes Wort oder auch jede Zeile ansagen, wenn Sie sich durch das Eingabefeld bewegen, Text markieren oder die Markierung aufheben.

Folgende Tastenkombinationen stehen im Zusammenhang mit dem System-Cursor zur Verfügung:
<!-- KC:beginInclude -->

| Name |Desktop-Tastenkombination |Laptop-Tastenkombination |Beschreibung|
|---|---|---|---|
|Alles Lesen |NVDA+Pfeil nach unten |NVDA+A |Liest von der aktuellen Position des System-Cursors bis zum Textende und bewegt dabei den System-Cursor mit.|
|Aktuelle Zeile lesen |NVDA+Pfeil nach oben |NVDA+L |Liest die Zeile, auf der sich der System-Cursor befindet. Wird diese Tastenkombination zweimal gedrückt, wird die Zeile buchstabiert, wird die Tastenkombination 3-mal gedrückt, wird die Zeile phonetisch buchstabiert.|
|Markierten Text lesen |NVDA+Umschalt+Pfeil nach oben |NVDA+Umschalt+S |Liest den markierten Text, sofern vorhanden.|
|Textformatierungen ausgeben |NVDA+F |NVDA+F |Gibt die Textformatierungen unter dem System-Cursor aus. Bei zweimal Drücken werden diese Informationen im Lesemodus angezeigt.|
|Linkziel ausgeben |"NVDA+k" |"NVDA+k" |Durch einmaliges Drücken wird die Ziel-Adresse des Links an der aktuellen Cursor- oder Fokusposition ausgegeben. Durch zweimaliges Drücken wird ein Fenster zur genaueren Überprüfung angezeigt|
|Position des System-Cursors mitteilen |NVDA+Nummernblock Entfernen |NVDA+Entf |Meldet Informationen über die Position des Textes oder des Objekts an der Position des System-Cursors. Dies kann z. B. der Prozentsatz im Dokument, der Abstand zum Seitenrand oder die genaue Position auf dem Bildschirm sein. Durch zweimaliges Drücken können weitere Details angezeigt werden.|
|Nächsten Satz lesen |Alt+Pfeiltaste nach unten |Alt+Pfeiltaste nach unten |Zieht die Schreibmarke zum nächsten Satz und gibt ihn aus (nur in Microsoft Word und Microsoft Outlook unterstützt).|
|Vorherigen Satz lesen |Alt+Pfeiltaste nach oben |Alt+Pfeiltaste nach oben |Zieht die Schreibmarke zum vorherigen Satz und gibt ihn aus (nur in Microsoft Word und Microsoft Outlook unterstützt).|

Für die Navigation in Tabellen stehen folgende Tastenkombinationen zur Verfügung:

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Zur vorherigen Spalte navigieren |Strg+Alt+Pfeiltaste nach links |Zieht den System-Cursor zur vorherigen Spalte in der gleichen Zeile.|
|Zur nächsten Spalte navigieren |Strg+Alt+Pfeiltaste nach rechts |Zieht den System-Cursor zur nächsten Spalte in der gleichen Zeile.|
|Zur vorherigen Zeile navigieren |Strg+Alt+Pfeiltaste nach oben |Zieht den System-Cursor zur vorherigen Zeile in der gleichen Spalte.|
|Zur nächsten Zeile navigieren |Strg+Alt+Pfeiltaste nach unten |Zieht den System-Cursor zur nächsten Zeile in der gleichen Spalte.|
|Zur ersten Spalte springen |Strg+Alt+Pos1 |Zieht den System-Cursor in die erste Spalte (bleibt in der gleichen Zeile)|
|Zur letzten Spalte springen |Strg+Alt+Ende |Zieht den System-Cursor in die letzte Spalte (bleibt in der gleichen Zeile)|
|Zur ersten Zeile springen |Strg+Alt+Seite nach oben |Zieht den System-Cursor in die erste Zeile (bleibt in gleichen Spalte)|
|Zur letzten Zeile springen |Strg+Alt+Seite nach unten |Zieht den System-Cursor in die letzte Zeile (bleibt in gleichen  Spalte)|
|Alles Lesen in Spalte |`NVDA+Strg+Alt+Pfeiltaste nach unten` |Liest die Spalte vertikal von der aktuellen Zelle abwärts bis zur letzten Zelle der Spalte vor.|
|Alles Lesen in Zeile |`NVDA+Strg+Alt+Pfeiltaste nach rehcts` |Liest die Zeile horizontal von der aktuellen Zelle nach rechts bis zur letzten Zelle der Zeile vor.|
|Gesamte Spalte vorlesen |`NVDA+Strg+Alt+Pfeiltaste nach oben` |Liest die aktuelle Spalte vertikal von oben nach unten vor, ohne den System-Cursor zu bewegen.|
|Gesamte Zeile vorlesen |`NVDA+Strg+Alt+Pfeiltaste nach links` |Liest die aktuelle Zeile horizontal von links nach rechts vor, ohne den System-Cursor zu bewegen.|

<!-- KC:endInclude -->

### Objekt-Navigation {#ObjectNavigation}

Üblicherweise arbeiten Sie mit Programmen, indem Sie mittels Tastenkürzeln den [Fokus](#SystemFocus) oder den [System-Cursor](#SystemCaret) bewegen.
Manchmal möchten Sie jedoch mit den Objekten einer Anwendung oder des Betriebssystems arbeiten, ohne den Fokus oder den System-Cursor zu bewegen.
Vielleicht wollen Sie mit [Objekten](#Objects) umgehen, die nicht mit den Standard-Tastenkombinationen erreichbar sind (etwa, weil sie nicht in der Tab-Reihenfolge stehen).
In solchen Fällen können Sie die objektorientierte Navigation verwenden. Dabei wird ein NVDA-Fokus (Navigator) die Objekte ansteuern.

Die Objekt-Navigation ermöglicht das Bewegen zwischen Objekten und das Abrufen von Informationen über ein einzelnes [Objekt](#Objects).
Wenn Sie sich zu einem Objekt mittels Navigator bewegen, wird NVDA Ihnen dies auf eine ähnliche Weise mitteilen, als hätten Sie den System-Fokus bewegt. Wenn Sie innerhalb eines Objektes navigieren, dann bewegen Sie den NVDA-Cursor, der sozusagen das Equivalent vom System-Cursor ist.
Um Inhalte so anzuzeigen, wie sie auf dem Bildschirm erscheinen, verwenden Sie stattdessen den [Bildschirm-Betrachter](#ScreenReview).

Die Objekte sind innerhalb des Betriebssystems und der Anwendungen hierarchisch organisiert.
Dies bedeutet, dass Sie in manche Objekte "absteigen" müssen, um deren Inhalt zu sehen.
Eine Liste enthält beispielsweise Objekte, die die einzelnen Einträge darstellen; Sie müssen also in die Liste "absteigen", um die Einträge zu sehen.
Wenn Sie sich auf einem Listeneintrag befinden, können Sie sich zum nächsten/vorherigen Objekt auf der selben Ebene bewegen, um die anderen Einträge zu sehen.
Um von einem Listeneintrag wieder zur Liste zurückzukehren, müssen Sie wieder eine Ebene "aufsteigen".
Nun können Sie sich über die Liste hinausbewegen, um andere Objekte zu sehen.
So ähnlich enthält eine Symbolleiste ebenfalls Steuerelemente und Sie müssen in die Symbolleiste "absteigen", um die einzelnen Elemente zu sehen.

Wenn Sie es dennoch vorziehen, sich zwischen den einzelnen Objekten im System hin und her zu bewegen, können Sie die Befehle verwenden, um zum vorherigen bzw. nächsten Objekt in einer reduzierten Ansicht zu wechseln.
Wenn Sie zum Beispiel zum nächsten Objekt in dieser reduzierten Ansicht wechseln und das aktuelle Objekt andere Objekte enthält, wechselt NVDA automatisch zum ersten Objekt, welches dieses enthält.
Wenn das aktuelle Objekt keine Objekte enthält, wechselt NVDA zum nächsten Objekt auf der aktuellen Ebene der Hierarchie.
Wenn es kein weiteres Objekt gibt, versucht NVDA, das nächste Objekt in der Hierarchie anhand der enthaltenen Objekte zu finden, bis es keine weiteren Objekte mehr gibt, zu denen man wechseln kann.
Die gleichen Regeln gelten für das Zurückgehen in in der Hierarchie.

Das momentan angezeigte Objekt wird als Navigator-Objekt bezeichnet.
Wenn Sie sich zu einem Objekt bewegen und der Modus [Objekt-Betrachter](#ObjectReview) aktiv ist, können Sie sich das Objekt mit den [Befehlen zum Text betrachten](#ReviewingText) anschauen.
Wenn [Visuell hervorheben](#VisionFocusHighlight) aktiviert ist, wird die Position des aktuellen Navigator-Objekts auch visuell dargestellt.
Standardmäßig folgt der Navigator dem System-Fokus, diese Kopplung kann jedoch umgeschaltet werden.

Hinweis: Braille mit anschließender Objekt-Navigation kann über die [Kopplung der Braille-Ausgabe](#BrailleTether) konfiguriert werden.

Mit den folgenden Befehlen navigieren Sie zwischen den Objekten:

<!-- KC:beginInclude -->

| Name |Desktop-Tastenkombination |Laptop-Tastenkombination |Touch-Geste |Beschreibung|
|---|---|---|---|---|
|Aktuelles Objekt mitteilen |NVDA+Nummernblock 5 |NVDA+Umschalt+O |Keine |Teilt das aktuelle Navigator-Objekt mit. Bei zweimal Drücken werden die Informationen buchstabiert und bei dreimal Drücken wird die Information in die Zwischenablage kopiert.|
|Zum übergeordneten Objekt navigieren |NVDA+Nummernblock 8 |NVDA+Umschalt+Pfeiltaste nach oben |Nach oben streichen (Objektmodus) |Navigiert zur übergeordneten Ebene des aktuellen Navigator-Objekts.|
|Zum vorherigen Objekt navigieren |NVDA+Nummernblock 4 |NVDA+Umschalt+Pfeiltaste nach links |Keine |Wechselt zu dem Objekt vor dem aktuellen Navigator-Objekt.|
|Zum vorherigen Objekt in der reduzierten Ansicht wechseln |NVDA+Nummernblock 9 |NVDA+Umschalt+Ü |Nach links streichen (Objektmodus) |Wechselt zum vorherigen Objekt in einer reduzierten Ansicht der Hierarchie der Objekt-Navigation.|
|Zum nächsten Objekt navigieren |NVDA+Nummernblock 6 |NVDA+Umschalt+Pfeiltaste nach rechts |Keine |Wechselt zu dem Objekt nach dem aktuellen Navigator-Objekt.|
|Zum nächsten Objekt in der reduzierten Ansicht wechseln |NVDA+Nummernblock 3 |NVDA+Umschalt+Plus |Nach rechts streichen (Objektmodus) |Wechselt zum nächsten Objekt in einer reduzierten Ansicht der Hierarchie der Objekt-Navigation.|
|Zum ersten untergeordneten Objekt navigieren |NVDA+Nummernblock 2 |NVDA+Umschalt+Pfeiltaste nach unten |Nach unten streichen (Objektmodus) |Navigiert zum ersten untergeordneten Objekt ausgehend vom aktuellen Navigator-Objekt.|
|Zum Fokus-Objekt navigieren |NVDA+Nummernblock-Minus |NVDA+Rücktaste |Keine |Navigiert zum aktuell hervorgehobenen Objekt und zieht den NVDA-Cursor zum System-Cursor, sofern dieser sichtbar ist.|
|Aktuelles Navigator-Objekt aktivieren |NVDA+Nummernblock-Eingabetaste |NVDA+Eingabetaste |Doppeltippen |Aktiviert das aktuelle Navigator-Objekt (ähnlich einem Mausklick oder dem Drücken der Leertaste).|
|System-Cursor zum aktuellen Navigator-Objekt oder die Einfügemarke zum NVDA-Cursor ziehen |NVDA+Umschalt+Nummernblock-Minus |NVDA+Umschalt+Rücktaste |Keine |Wird diese Tastenkombination einmal gedrückt, wird der System-Fokus zum aktuellen Navigator-Objekt gezogen. Wird sie zweimal gedrückt, so wird der System-Cursor zum NVDA-Cursor gezogen.|
|Position des NVDA-cursors mitteilen |NVDA+Umschalt+Nummernblock Komma |NVDA+Umschalt+Entfernen |Keine |Teilt Informationen über die Position des Textes oder Objekts am NVDA-Cursor mit. Dies kann z. B. der Prozentsatz im Dokument, der Abstand zum Seitenrand oder die genaue Position auf dem Bildschirm sein. Durch zweimaliges Drücken können weitere Details angezeigt werden.|
|NVDA-Cursor in die Statusleiste verschieben |Keine |Keine |Keine |Liest die Statusleiste vor, falls vorhanden. Es verschiebt auch das Navigator-Objekt an diese Position.|

<!-- KC:endInclude -->

Hinweis: Um die Tasten auf dem Nummernblock zu benutzen, muss dieser deaktiviert sein!

### Befehle zum Text betrachten {#ReviewingText}

NVDA ermöglicht den [Bildschirminhalt](#ScreenReview), den Inhalt des aktuellen [Dokuments](#DocumentReview) oder das aktuelle [Objekt](#ObjectReview) zeichen-, wort- oder zeilenweise zu betrachten.
Dies ist z. B. in Windows-Konsolenfenstern (wie der Eingabeaufforderung, in der PowerShell) oder in anderen Anwendungen sinnvoll, in denen der [System-Cursor](#SystemCaret) nicht oder nur eingeschränkt verfügbar ist.
Ein weiterer Anwendungsfall ist das Lesen von langen Meldungen in Dialogfeldern.

Wenn Sie den NVDA-Cursor bewegen, bewegt sich der System-Cursor nicht mit, sodass beispielsweise die aktuelle Cursor-Position beim Bearbeiten von Text nicht verloren geht.
Wenn Sie jedoch den System-Cursor bewegen, wird er vom NVDA-Cursor verfolgt.
Diese Kopplung kann ein- und ausgeschaltet werden.

Hinweis: Die Braille-Ausgabe nach dem NVDA-Cursor kann über [Braille-Ausgabe koppen](#BrailleTether) konfiguriert werden.

Die folgenden Tastenkombinationen zum Text betrachten sind verfügbar:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Geste |Beschreibung|
|---|---|---|---|---|
|Zur obersten Zeile navigieren |Umschalt+Nummernblock 7 |NVDA+Strg+Pos1 |Keine |Zieht den NVDA-Cursor in die erste Zeile des Textes.|
|Zur vorherigen Zeile navigieren |Nummernblock 7 |NVDA+Pfeiltaste nach oben |Nach oben streichen (Textmodus) |Zieht den NVDA-Cursor zur vorherigen Zeile des Textes.|
|Aktuelle Zeile unter dem NVDA-Cursor ansagen |Nummernblock 8 |NVDA+Umschalt+Punkt |Keine |Sagt die aktuelle Zeile im Text an, in der sich der NVDA-Cursor befindet. Bei zweimal Drücken wird sie buchstabiert, bei dreimal Drücken wird die Zeile phonetisch buchstabiert.|
|Zur nächsten Zeile navigieren |Nummernblock 9 |NVDA+Pfeiltaste nach unten |Nach unten streichen (Textmodus) |Zieht den NVDA-Cursor zur nächsten Zeile des Textes.|
|Zur untersten Zeile navigieren |Umschalt+Nummernblock 9 |NVDA+Strg+Ende |Keine |Zieht den NVDA-Cursor in die letzte Zeile des Textes.|
|Zum vorherigen Wort navigieren |Nummernblock 4 |NVDA+Strg+Pfeiltaste nach links |Nach links streichen mit zwei Fingern (Textmodus) |Zieht den NVDA-Cursor zum vorherigen Wort im Text.|
|Aktuelles Wort unter dem NVDA-Cursor ansagen |Nummernblock 5 |NVDA+Strg+Punkt |Keine |Sagt das aktuelle Wort im Text an, in dem sich der NVDA-Cursor befindet. Bei zweimal Drücken wird es buchstabiert, bei dreimal Drücken wird das Wort phonetisch buchstabiert.|
|Zum nächsten Wort navigieren |Nummernblock 6 |NVDA+Strg+Pfeiltaste nach rechts |Nach rechts streichen mit zwei Fingern (Textmodus) |Zieht den NVDA-Cursor zum nächsten Wort im Text.|
|Zum Zeilenanfang navigieren |Umschalt+Nummernblock 1 |NVDA+Pos1 |Keine |Zieht den NVDA-Cursor zum Zeilenanfang im Text.|
|Zum vorherigen Zeichen navigieren |Nummernblock 1 |NVDA+Pfeiltaste nach links |Nach links streichen (Textmodus) |Zieht den NVDA-Cursor zum vorherigen Zeichen der aktuellen Zeile im Text.|
|Aktuelles Zeichen unter dem NVDA-Cursor ansagen |Nummernblock 2 |NVDA+Punkt |Keine |Sagt das aktuelle Zeichen in der Zeile im Text an, an dem sich der NVDA-Cursor befindet. Bei zweimal Drücken wird das Zeichen phonetisch buchstabiert. Bei dreimal Drücken werden die numerischen Dezimal- und Hexadezimalwerte angesagt.|
|Zum nächsten Zeichen navigieren |Nummernblock 3 |NVDA+Pfeiltaste nach rechts |Nach rechts streichen (Textmodus) |Zieht den NVDA-Cursor zum nächsten Zeichen der aktuellen Zeile im Text.|
|Zum Zeilenende navigieren |Umschalt+Nummernblock 3 |NVDA+Ende |Keine |Zieht den NVDA-Cursor zum Zeilenende im Text.|
|Zur vorherigen Seite in der Übersicht wechseln |`NVDA+Seite nach oben` |`NVDA+Umschalt+Pfeiltaste nach oben` |Keine |Zieht den NVDA-Cursor auf die vorherige Textseite, sofern dies von der Anwendung unterstützt wird.|
|Zur nächsten  Seite in der Übersicht wechseln |`NVDA+Seite nach unten` |`NVDA+Umschalt+Seite nach unten` |Keine |Zieht den NVDA-Cursor auf die nächste Textseite, sofern dies von der Anwendung unterstützt wird.|
|Alles Lesen |Nummernblock Plus |NVDA+Umschalt+A |Nach unten streichen mit drei Fingern (Textmodus) |Liest von der aktuellen Cursor-Position des NVDA-Cursors den Text vor und bewegt ihn mit.|
|Vom NVDA-Cursor markieren und kopieren |NVDA+F9 |NVDA+F9 |Keine |Setzt eine Startmarke an der aktuellen Position des NVDA-Cursors ab, der markiert oder kopiert werden soll. Die Aktion (Markieren/Kopieren) wird nicht ausgeführt, bis Sie NVDA den Textende mitgeteilt haben.|
|Bis zum NVDA-Cursor markieren und kopieren |NVDA+F10 |NVDA+F10 |Keine |Wird die Tastenkombination einmal gedrückt, markiert NVDA den Text zwischen der zuvor gesetzten Startmarke und der aktuellen Position des NVDA-Cursors. Ist die Startmarke mit dem System-Cursor erreichbar, wird der Fokus dorthin verschoben. Wird die Tastenkombination zweimal gedrückt, wird der markierte Text in die Zwischenablage kopiert.|
|Springt zum markierten Start für die Kopie in der Ansicht |NVDA+Umschalt+F9 |NVDA+Umschalt+F9 |Keine |Zieht den NVDA-Cursor an die zuvor eingestellte Startmarkierung für das Kopieren.|
|Text-Formatting ausgeben |NVDA+Umschalt+F |NVDA+Umschalt+F |Keine |Gibt die Textformatierungen unter dem System-Cursor aus. Bei zweimal Drücken werden diese Informationen im Lesemodus angezeigt.|
|Ansage des aktuellen Symbol-Ersatzes |Keine |Keine |Keine |Spricht das Symbol, an dem sich der NVDA-Cursor befindet. Zweimaliges Drücken zeigt das Symbol und den ausgesprochenen Text in einem virtuellen Fenster an.|

<!-- KC:endInclude -->

Hinweis: Um die Tasten des Nummernblocks benutzen zu können, muss dieser deaktiviert sein!

Um sich bei der Verwendung des Desktop-Tastaturschemas auf hilfreiche Weise die Tastenkombinationen merken zu können, wird dieses Textraster grundsätzlich in drei Mal drei "Felder" angeordnet; von oben nach unten, von links nach rechts sowie zum vorherigen, aktuellen und nächsten.
Das Layout ist wie folgt aufgebaut:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Vorherige Zeile |Aktuelle Zeile |Nächste Zeile|
|Vorheriges Wort |Aktuelles Wort |Nächstes Wort|
|Vorheriges Zeichen |Aktuelles Zeichen |Nächstes Zeichen|

### Die Betrachtungsmodi {#ReviewModes}

Abhängig vom eingestellten Betrachtungsmodus können Sie mit den [Befehlen zum Text betrachten](#ReviewingText) im aktuellen Navigator-Objekt, im angezeigten Dokument oder auf dem Bildschirm navigieren.

Die folgenden Befehle wechseln zwischen den Betrachtungsmodi:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Geste |Beschreibung|
|---|---|---|---|---|
|In den nächsten Betrachtungsmodus wechseln |NVDA+Nummernblock 7 |NVDA+Seite auf |Mit zwei Fingern nach oben streichen |Schaltet in den nächsten Betrachtungsmodus um.|
|In den vorherigen Betrachtungsmodus wechseln |NVDA+Nummernblock1 |NVDA+Seite ab |Mit zwei Fingern nach unten streichen |Schaltet im vorherigen Betrachtungsmodus um.|

<!-- KC:endInclude -->

#### Der Objekt-Betrachter {#ObjectReview}

Wenn Sie mit dem Objekt-Betrachter navigieren, können Sie den Inhalt des aktuellen [Navigator-Objekts](#ObjectNavigation) zeichenweise, wortweise oder zeilenweise betrachten.
Bei Eingabefeldern ist das üblicherweise der eingegebene Text.
Bei anderen Objekten wird hier der Name, die Beschriftung und der Wert des Objekts angezeigt.

#### Der Dokument-Betrachter {#DocumentReview}

Wenn sich das aktuelle Navigator-Objekt in einem virtuellen Dokument (Lotus-Symphony-Dokument, Webseiten, o. ä.) befindet, können Sie mit dem Dokument-Betrachter navigieren.
Im Dokument-Betrachter können Sie sich den Text des gesamten Dokuments anzeigen lassen.

Wenn Sie aus dem Objekt-Betrachter im Dokument-Betrachter wechseln, wird der NVDA-Cursor an die Position des aktuellen Navigator-Objekts gesetzt.
Wenn Sie die Befehle zum Text betrachten verwenden, wird das Navigator-Objekt automatisch aktualisiert.

NVDA wird automatisch zum Dokument-Betrachter wechseln, sobald Sie sich im Lesemodus befinden.

#### Der Bildschirm-Betrachter {#ScreenReview}

In diesem Modus können Sie sich den gesamten Inhalt des Bildschirms vom aktuellen Fenster anzeigen lassen.
Dies ähnelt den Bildschirmdarstellungs- und Mauszeigerfunktionen vieler Screenreader für Windows.

Wenn Sie mit dem Bildschirm-Betrachter über den Inhalt des Bildschirms navigieren, wird der NVDA-Cursor an die Position des aktuellen Navigator-Objekts auf dem Bildschirm gesetzt.
Wenn Sie die Befehle zum Text betrachten verwenden, wird der Navigator automatisch auf das Objekt gesetzt, das sich an der Position des NVDA-Cursors befindet.

Anmerkung: In einigen neueren Anwendungen kann NVDA möglicherweise nicht alle Inhalte im Bildschirm-Betrachter darstellen. Dies liegt daran, dass diese Anwendungen Technologien zum Darstellen des Bildschirminhalts verwenden, die (noch) nicht unterstützt werden.

### Mit der Maus navigieren {#NavigatingWithTheMouse}

Wenn Sie den Mauszeiger über ein Objekt bewegen, gibt NVDA Informationen über dieses Objekt aus.
Sofern möglich, liest NVDA den umgebenden Textabsatz vor, auch wenn sich einige Objekte nur zeilenweise vorlesen lassen.

NVDA kann auch so konfiguriert werden, dass der Typ des [Objektes](#Objects) vorgelesen wird, welches sich unter dem Mauszeiger befindet (wie z. B. Liste, Schalter, etc.).
Dies könnte für blinde Benutzer nützlich sein, denen das bloße Vorlesen des Textes unter der Maus nicht genügt.

Mit Hilfe von Signaltönen, die die aktuelle Position des Mauszeigers darstellt, kann NVDA ihnen zeigen, wo sich die Maus - relativ zur linken oberen Bildschirmecke - befindet.
Je näher sich der Mauszeiger am oberen Bildschirmrand befindet, desto höher ist der Signalton.
Richtig ausgerichtete Stereolautsprecher oder Kopfhörer vorausgesetzt, wird der Signalton umso mehr links oder rechts abgespielt, je weiter links oder rechts sich der Mauszeiger bewegt.

Diese zusätzlichen Mausfunktionen sind in NVDA standardmäßig deaktiviert.
Sie können Sie jedoch in den [Maus-Einstellungen](#MouseSettings) aktivieren, die Sie in den NVDA-Einstellungen in der Kategorie "Maus" finden.

Zum Navigieren mit der Maus sollte eine richtige Maus oder eine Mauskugel benutzt werden. Folgende Tastenbefehle stehen in NVDA zur Verfügung:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Geste |Beschreibung|
|---|---|---|---|---|
|Linksklick |Nummernblock-Schrägstrich |NVDA+Ü |Keine |Führt einen Linksklick aus. Bei zweimal Drücken wird ein Doppelklick ausgeführt.|
|Linke Maustaste feststellen |Umschalt+Nummernblock-Schrägstrich |NVDA+Strg+Ü |Keine |Hält die linke Maustaste gedrückt. Wird die Tastenkombination erneut gedrückt, wird die Maustaste wieder losgelassen. Um "Drag and Drop" durchzuführen, führen Sie diesen Schritt auf einem Objekt aus und wandern anschließend mit der Maus oder auch mit den Navigationstasten für die Simulation der Maus an eine andere Stelle des Bildschirms und lösen die linke Maustaste wieder.|
|Rechtsklick |Nummernblock-Stern |NVDA+Plus |Mit einem Finger tippen und halten |Führt einen Rechtsklick aus.|
|Rechte Maustaste feststellen |Umschalt+Nummernblock-Stern |NVDA+Strg+Plus |Keine |Hält die rechte Maustaste gedrückt. Wird die Tastenkombination erneut gedrückt, wird die Maustaste wieder losgelassen. Um "Drag and Drop" durchzuführen, führen Sie diesen Schritt auf einem Objekt aus und wandern anschließend mit der Maus oder auch mit den Navigationstasten für die Simulation der Maus an eine andere Stelle des Bildschirms und lösen die rechte Maustaste wieder.|
|Die Maus zum aktuellen Navigator-Objekt ziehen |NVDA+Nummernblock-Schrägstrich |NVDA+Umschalt+M |Keine |Zieht die Maus zum aktuellen Standort des Navigator-Objektes oder des NVDA-Cursors.|
|Zum Objekt unter der Maus navigieren |NVDA+Nummernblock-Stern |NVDA+Umschalt+N |Keine |Zieht das Navigator-Objekt zur Objektposition an der Mausposition.|

<!-- KC:endInclude -->

## Der Lesemodus {#BrowseMode}

Dokumente, wie z. B. Webseiten, werden in NVDA im sogenannten Lesemodus dargestellt.
Dies betrifft folgende Anwendungen:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML-Nachrichten in Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Unterstützte Bücher in Amazon Kindle für PC

Der Lesemodus ist optional auch in Microsoft Word- und Microsoft Excel-Dokumenten verfügbar.

Im Lesemodus wird der Inhalt von Dokumenten in einer flächenähnlichen Struktur dargestellt, sodass Sie sich mit den Pfeiltasten durch den Text navigieren können. Dabei wird ein virtueller, nicht sichtbarer Cursor verwendet.
Alle [Befehle zum Navigieren mit dem System-Cursor](#SystemCaret) sind im Lesemodus verfügbar. So z. B. Alles Lesen, Formatierung ansagen, Befehle zur Tabellen-Navigation, etc.
Wenn [Visuell hervorheben](#VisionFocusHighlight) aktiviert ist, wird die Position des virtuellen Cursors im Lesemodus visuell dargestellt.
Informationen darüber, ob der Text beispielsweise ein Link, eine Überschrift, o. ä. ist, wird Ihnen beim Navigieren unmittelbar mitgeteilt.

Manchmal müssen Sie in diesen Dokumenten mit Steuerelementen interagieren.
Dies ist beispielsweise der Fall, wenn Sie Text in ein Eingabefeld schreiben wollen oder wenn Sie mit Hilfe der Pfeiltasten eine Liste oder ein Flash-Objekt bedienen wollen.
Um mit diesen Elementen zu arbeiten, aktivieren Sie den Fokusmodus, in welchem Alle Tasten an das Element weitergegeben werden.
Wenn Sie sich im Lesemodus befinden, wird NVDA standardmäßig automatisch den Fokusmodus aktivieren, sobald Sie mit Tab auf ein Element springen oder darauf klicken, welches den Fokusmodus benötigt.
Entsprechend wechselt NVDA automatisch in den Lesemodus, wenn Sie auf ein Element klicken oder mit der Tab-Taste darauf springen, welches den Fokusmodus nicht benötigt.
Wenn ein Element den Fokusmodus benötigt, können Sie auch die Leertaste oder Eingabetaste drücken, um den Fokusmodus zu aktivieren.
Mit der Escape-Taste wechseln Sie wieder zurück in den Lesemodus.
Zusätzlich können Sie auch den Fokusmodus erzwingen. In diesem Fall bleibt der Fokusmodus so lange aktiv, bis Sie wieder zum Lesemodus zurückkehren.

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Zwischen Lese- und Fokusmodus wechseln |NVDA+Leertaste |Schaltet zwischen Fokus- und Lesemodus um.|
|Fokusmodus schließen |Escape-Taste |Schaltet zurück in den Lesemodus, wenn zuvor der Fokusmodus automatisch aktiviert wurde.|
|Lesemodus aktualisieren |NVDA+F5 |Lädt das aktuelle Dokument neu (das ist sinnvoll, wenn vielleicht einige Elemente auf der Seite fehlen sollten. Dieser Befehl ist in Microsoft Word und Microsoft Outlook nicht verfügbar).|
|Suchen |NVDA+Strg+F |Öffnet einen Dialog, in dem Sie einen Text eingeben können, der im aktuellen Dokument zu finden ist. Weitere Informationen finden Sie unter [Nach Text suchen](#SearchingForText).|
|Vorwärts suchen |NVDA+F3 |Sucht die nächste Zeichenkette des gesuchten Textes im aktuellen Dokument, welche zuvor eingegeben wurde.|
|Rückwärts suchen |NVDA+Umschalt+F3 |Sucht die vorherige Zeichenkette des gesuchten Textes im aktuellen Dokument, die zuvor eingegeben wurde.|

<!-- KC:endInclude -->

### Die Schnellnavigationstasten {#SingleLetterNavigation}

Um im Lesemodus eine schnellere Navigation zu ermöglichen, stellt NVDA die sogenannten Schnellnavigationstasten für das Ansteuern bestimmter Seitenelemente zur Verfügung.
Bitte beachten Sie, dass nicht alle Schnellnavigationstasten in jedem Dokumententyp verfügbar sind.

<!-- KC:beginInclude -->
Folgende Befehle springen ohne Umschalttaste gedrückt zum nächsten Element; zusammen mit der Umschalttaste springen Sie zum vorherigen Objekt.

* `H`: Überschrift
* `L`: Liste
* `I`: Listeneintrag
* `T`: Tabelle
* `K`: Link
* `N`: Nichtverlinkter Text
* `F`: Formularfeld
* `U`: Nicht besuchter Link
* `V`: Besuchter Link
* `E`: Eingabefeld
* `B`: Schalter
* `X`: Kontrollfeld
* `C`: Kombinationsfeld
* `R`: Auswahlschalter
* `Q`: Zitatblock
* `S`: Trennlinie
* `M`: Rahmen
* `G`: Grafik
* `D`: Sprungmarke
* `O`: Eingebettetes Objekt (Anwendung, Dialogfeld, Audio- und Video-Player)
* `1` bis `6`: Überschrift der jeweiligen Ordnung
* `A`: Anmerkung: Kommentar, Dokumentänderung, etc.
* `P`: Absatz
* `W`: Rechtschreibfehler

Verwenden Sie folgende Tastenkombinationen, um zum Beginn oder zum Ende eines Container-Objektes (Listen, Tabellen, etc.) zu springen:

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Zum Beginn des Container-Objekts springen |Umschalt+Komma |Zieht den System-Cursor zum Anfang des Container-Objekts (Liste, Tabelle, etc.) auf dem sich der Cursor befindet.|
|Hinter das Container-Objekt springen |Komma |Zieht den System-Cursor zum Ende des Container-Objekts (Liste, Tabelle, etc.) auf dem sich der Cursor befindet.|

<!-- KC:endInclude -->

Einige Web-Anwendungen verwenden einzelne Buchstaben als Tastenkürzel. Hierzu zählen Twitter, Gmail und Facebook.
Um in solchen Web-Anwendungen eigene Kurztasten verwenden und dennoch mit den Pfeiltasten durch die Web-Anwendung navigieren zu können, können Sie die Schnellnavigation von NVDA ein- oder ausschalten.
<!-- KC:beginInclude -->
Mit NVDA+Umschalt+Leertaste können Sie die Schnellnavigation im aktuellen Dokument ein- oder ausschalten.
<!-- KC:endInclude -->

#### Befehl zur Navigation in Textabschnitten {#TextNavigationCommand}

Sie können zum nächsten oder vorherigen Textabschnitt springen, indem Sie die Taste `P` oder `Umschalt+P` drücken.
Textabsätze sind durch eine Gruppe von Texten definiert, die in vollständigen Sätzen unterteilt werden.
Dies kann nützlich sein, um den Anfang von lesbaren Inhalten auf verschiedenen Webseiten zu finden, z. B:

* Nachrichten
* Foren
* Blogs

Diese Befehle können auch hilfreich sein, um bestimmte Arten von Unordnung zu überspringen, z. B.:

* Werbungen
* Menüs
* Überschriften

Bitte beachten Sie jedoch, dass NVDA zwar sein Bestes tut, um Textabsätze zu erkennen, der Algorithmus jedoch nicht perfekt ist und manchmal Fehler macht.
Außerdem unterscheidet sich dieser Befehl von den Befehlen für die Absatznavigation `Strg+Pfeiltaste nach oben/unten`.
Die Absatznavigation springt nur zwischen Textabschnitten, während die Befehle zur Absatznavigation den Cursor zu den vorherigen/nächsten Absätzen führen, unabhängig davon, ob sie Text enthalten oder nicht.

#### Weitere Navigationsbefehle {#OtherNavigationCommands}

Zusätzlich zu den oben aufgeführten Schnellnavigationsbefehlen verfügt NVDA über Befehle, denen keine Standard-Tasten zugewiesen sind.
Um diese Befehle verwenden zu können, müssen Sie zunächst diese zuweisen, indem Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) aufrufen.
Hier ist eine Liste der verfügbaren Befehle:

* Artikel
* Abbildung
* Gruppierung
* Tab
* Menü
* Umschalter
* Fortschrittsbalken
* Mathematische Formeln
* Vertikal ausgerichteter Absatz
* Text mit gleichem Stil
* Text in einem anderen Stil

Beachten Sie, dass es für jeden Elementtyp zwei Befehle gibt, um sich im Dokument vorwärts und rückwärts zu bewegen, und dass Sie beiden Befehlen diese zuweisen müssen, um schnell in beide Richtungen navigieren zu können.
Wenn Sie zum Beispiel `Y` und `Umschalt+Y` benutzen wollen, um schnell durch die Registerkarten zu navigieren, würden Sie Folgendes tun:

1. Öffnen Sie das Dialogfeld für die Tastenbefehle von Gesten im Lesemodus.
1. Suchen Sie in der Kategorie "Lesemodus" den Eintrag "Zum nächsten Tab navigieren".
1. Weisen Sie hier die Taste `Y` zu.
1. Suchen Sie den Eintrag "Zum vorherigen Tab navigieren".
1. Weisen Sie dann hier die Tastenkombination `Umschalt+Y` zu.

### Die Elementliste {#ElementsList}

Mit Hilfe der Elementliste können Sie - abhängig von der aktiven Anwendung - auf verschiedene Elemente im aktuellen Dokument zugreifen.
In Web-Browsern können Sie hierbei auf links, Überschriften, Formularfelder, Schalter oder Sprungmarken zugreifen.
Mit dem Auswahlschalter können Sie zwischen den unterschiedlichen Elementtypen umschalten.
Mit dem Eingabefeld können Sie auch die Einträge filtern, um sich die Suche auf der Seite zu erleichtern.
Wenn Sie einmal einen Eintrag ausgewählt haben, können Sie mit den Schaltflächen im Dialogfeld entweder den Eintrag aktivieren oder zu diesem gelangen.
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Elementliste des Lesemodus |NVDA+F7 |Zeigt eine Liste bestimmter Elemente im aktuellen Dokument an.|

<!-- KC:endInclude -->

### Nach Text suchen {#SearchingForText}

In diesem Dialogfeld können Sie nach Begriffen im aktuellen Dokument suchen.
Im ersten Feld geben Sie den zu suchende Text ein.
Das Kontrollkästchen "Groß- und Kleinschreibung berücksichtigen" bewirkt, dass die Suche Groß- und Kleinschreibung unterschiedlich beachtet wird.
Wenn Sie beispielsweise "Groß- und Kleinschreibung berücksichtigen" ausgewählt haben, finden Sie "NV Access", nicht aber "nv access".
Verwenden Sie die folgenden Tasten für die Suche:
<!-- KC:beginInclude -->

| Name |Taste |Beschreibung|
|---|---|---|
|Text suchen |NVDA+Strg+F |Öffnet das Suchfeld.|
|Weitersuchen |NVDA+F3 |Sucht das nächste Vorkommen des aktuellen Suchbegriffs.|
|Rückwärtssuchen |NVDA+Umschalt+F3 |Sucht das vorherige Vorkommen des aktuellen Suchbegriffs.|

<!-- KC:endInclude -->

### Eingebettete Objekte {#ImbeddedObjects}

Es gibt zunehmend Internetseiten, die mit Technologien für mediale Inhalte wie Oracle Java oder html5 mit Anwendungen und Dialogen ausgestattet sind.
Wenn Sie im Lesemodus auf einen dieser Inhalte stoßen, meldet NVDA dem entsprechend "Eingebettetes Objekt", "Anwendung" oder "Dialog".
Um zu einem eingebetteten Objekt zu navigieren, betätigen Sie die Schnellnavigationstaste O oder Umschalt+O.
Betätigen Sie anschließend die Eingabetaste, um mit einem Objekt zu interagieren.
Sofern das Objekt barrierefrei gestaltet wurde, können Sie innerhalb dieses Objekts normal mit der Tabulatortaste navigieren und damit wie in einer gewöhnlichen Anwendung arbeiten.
Es gibt eine Tastenkombination, um in die Originalansicht der Seite zurückzukehren:
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Zum Inhalt des Lesemodus zurückkehren |NVDA+Strg+Leertaste |Verlässt den Fokus des eingebetteten Objekts und kehrt in den Lesemodus zurück.|

<!-- KC:endInclude -->

### Native Auswahl {#NativeSelectionMode}

Wenn Sie Text mittels Umschalt+Pfeiltasten im Lesemodus auswählen, erfolgt die Auswahl standardmäßig nur innerhalb der NVDA-Lesemodusdarstellung des Dokuments, jedoch nicht innerhalb der Anwendung selbst.
Das bedeutet, dass die Auswahl nicht auf dem Bildschirm sichtbar ist und durch das Kopieren von Text mittels "Strg+C" nur die Klartextdarstellung des Inhalts von NVDA kopiert wird. D. h. die Formatierung von Tabellen oder ob es sich um einen Link handelt, wird nicht kopiert.
Allerdings verfügt NVDA über eine native Auswahl, welche in bestimmten Dokumenten im Lesemodus aktiviert werden kann. Hiermit folgt die native Auswahl des Dokuments der Auswahl im Lesemodus von NVDA. Dies gilt bisher nur für Mozilla Firefox.

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Native Auswahl ein- und ausschalten |"NVDA+Umschalt+f10" |Schaltet die native Auswahl ein oder aus.|

<!-- KC:endInclude -->

Wenn die native Auswahl aktiviert ist, wird beim Kopieren der Auswahl mit "Strg+C" auch die anwendungseigene Kopierfunktion verwendet, was bedeutet, dass formatierte Inhalte in die Zwischenablage kopiert werden und nicht nur reiner Text.
Dies bedeutet, dass das Einfügen dieses Inhalts in ein Programm wie Microsoft Word oder Excel die Textformatierung wie Tabellen oder ob es sich um einen Link handelt einbezogen wird.
Bitte beachten Sie, dass in der nativen Auswahl einige zugängliche Beschriftungen oder andere Informationen, die NVDA im Lesemodus generiert, nicht enthalten sind.
Auch wenn die Anwendung ihr Möglichstes versucht, die native Auswahl an die Auswahl des NVDA-Lesemodus anzupassen, ist dies möglicherweise nicht immer ganz genau.
In Szenarien, in denen Sie eine ganze Tabelle oder einen ganzen Absatz mit umfangreichen Inhalten kopieren möchten, sollte sich diese Funktion jedoch als nützlich erweisen.

## Mathematische Inhalte auslesen {#ReadingMath}

Sie können MathPlayer 4 von Design Science verwenden, um mit NVDA in mathematischen Inhalten zu navigieren. Die Inhalte werden in Sprache und Braille ausgegeben.
Damit NVDA jedoch mathematische Inhalte lesen und mit ihnen interagieren kann, müssen Sie zunächst eine Mathematikkomponente für NVDA installieren.
Im Store für NVDA-Erweiterungen sind mehrere NVDA-Erweiterungen verfügbar, die Mathematik unterstützen, darunter die Erweiterung [MathCAT](https://nsoiffer.github.io/MathCAT/) und [Access8Math https://github](.com/tsengwoody/Access8Math).
Weitere Informationen zum Durchsuchen und Installieren verfügbarer Erweiterungen in NVDA finden Sie im Abschnitt [Erweiterungs-Store](#AddonsManager).
NVDA kann auch die veraltete Software [MathPlayer](https://info.wiris.com/mathplayer-info) von Wiris nutzen, sofern diese auf Ihrem System vorhanden ist. Diese Software wird jedoch nicht mehr aktuallisiert.

### Unterstützte Mathematik-Inhalte {#SupportedMathContent}

NVDA unterstützt die folgenden mathematischen Inhalte, sofern eine entsprechende Mathematikkomponente installiert wurde:

* MathML in Mozilla Firefox, Microsoft Internet Explorer und Google Chrome.
* Moderne mathematische Gleichungen über UIA in Microsoft Word 365:
NVDA ist in der Lage, mathematische Gleichungen in Microsoft Word 365 / 2016 Build 14326 und neuer auszulesen und mit diesen zu interagieren.
Beachten Sie jedoch, dass alle zuvor erstellten MathType-Gleichungen zunächst in Office Math konvertiert werden müssen.
Dazu markieren Sie die einzelnen Elemente und wählen im Kontextmenü "Gleichungsoptionen" und dann "In Office-Mathematik umwandeln".
Vergewissern Sie sich, dass Ihre Version von MathType aktuell ist, bevor Sie dies tun.
Microsoft Word bietet eine lineare, symbolbasierte Navigation durch die Gleichungen selbst und unterstützt die Eingabe von mathematischen Werten mit verschiedener Syntax, einschließlich LaTeX.
Weitere Einzelheiten finden Sie unter [Linear formatierte Gleichungen mit UnicodeMath und LaTeX in Word](https://support.microsoft.com/de-de/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8).
* Microsoft PowerPoint und ältere Versionen von Microsoft Word:
NVDA kann MathType-Gleichungen sowohl in Microsoft Powerpoint als auch in Microsoft Word lesen und darin navigieren.
Damit dies funktioniert, muss MathType installiert sein.
Die Testversion ist ausreichend.
Sie können die aktuelle Version von der englischsprachigen [MathType-Präsentationsseite](https://www.wiris.com/en/mathtype/) herunterladen.
* Adobe Reader:
Beachten Sie, dass MathML noch kein offizieller Standard ist, deshalb gibt es noch keine öffentlich verfügbare Software, um solche Inhalte zu erzeugen.
* Kindle für PC:
NVDA kann Mathematik in Kindle für PC lesen und navigieren, um Bücher mit zugänglicher Mathematik zu lesen.

Wenn Sie ein Dokument lesen, das mathematischen Inhalt enthält, liest NVDA diesen vor, sofern es von NVDA unterstützt wird.
Falls Sie eine Braillezeile verwenden, wird dieser Inhalt auch in Braille ausgegeben.

### Interaktive Navigation {#InteractiveNavigation}

Wenn Sie NVDA hauptsächlich mit einer Sprachausgabe verwenden, können Sie einen mathematischen Ausdruck in Segmente unterteilt abfragen, anstatt ihn in einem Stück angesagt zu bekommen.

Wenn Sie sich momentan im Lesemodus befinden, können Sie den Cursor auf den Ausdruck stellen und die Eingabetaste drücken.

Wenn Sie sich nicht im Lesemodus befinden, gehen Sie folgendermaßen vor:

1. Bewegen Sie den NVDA-Cursor auf den mathematischen Ausdruck
Standardmäßig ist der NVDA-Cursor an den System-Cursor gekoppelt. Sie können also die Standard-Navigationstasten verwenden, um den NVDA-Cursor auf den mathematischen Inhalt zu bewegen.
1. Führen Sie anschließend den folgenden Befehl aus:

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|In mathematischen Inhalten navigieren |NVDA+Alt+M |Beginnt die Navigation in mathematischen Inhalten|

<!-- KC:endInclude -->

Nun wechselt NVDA in den Mathematikmodus, in dem Sie Befehle wie die Pfeiltasten verwenden können, um den Ausdruck zu erkunden.
Verwenden Sie beispielsweise die Pfeiltasten links und rechts, um zwischen den Teilen eines Ausdrucks zu navigieren. Um in einen Teilausdruck abzusteigen, verwenden Sie die Pfeiltaste nach unten.

Um die Navigation im Ausdruck zu beenden, drücken Sie die Escape-Taste.

Weitere Informationen zu den verfügbaren Befehlen und Einstellungen zum Lesen und Navigieren innerhalb von Mathematikinhalten finden Sie in der Dokumentation zu Ihrer jeweiligen Mathematikkomponente, die Sie installiert haben.

* [MathCAT-Dokumentation](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math-Dockumentation](https://github.com/tsengwoody/Access8Math)
* [MathPlayer-Dokumentation](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Manchmal kann mathematischer Inhalt als Schaltfläche oder eine andere Art von Element angezeigt werden, das, wenn es aktiviert ist, ein Dialogfeld oder weitere Informationen zur Formel anzeigen kann.
Drücken Sie Strg+Eingabe, um die Schaltfläche oder das Element, welches die Formel enthält, zu aktivieren.

### MathPlayer installieren {#InstallingMathPlayer}

Obwohl allgemein empfohlen wird, eine der neueren NVDA-Erweiterungen zur Unterstützung von Mathematik in NVDA zu verwenden, kann MathPlayer in bestimmten und begrenzten Szenarios immer noch die geeignetere Wahl sein.
MathPlayer z. B. unterstützt möglicherweise eine bestimmte Sprache oder einen Braille-Code, der in neueren Add-ons nicht unterstützt wird.
MathPlayer ist kostenlos auf der Webseite von Wiris erhältlich.
[MathPlayer herunterladen](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Nach der Installation von MathPlayer müssen Sie NVDA neu starten.
Bitte beachten Sie, dass in den Informationen zum MathPlayer angegeben sein kann, dass er nur für ältere Browser wie Internet Explorer 8 geeignet ist.
Dies bezieht sich nur auf die Verwendung von MathPlayer zur visuellen Anzeige mathematischer Inhalte und kann von Benutzern ignoriert werden, die ihn zum Lesen oder Navigieren in Mathematik mit NVDA verwenden.

## Braille {#Braille}

Wenn Sie eine Braillezeile besitzen, kann NVDA diese verwenden, um Informationen in Blindenschrift darzustellen.
Falls Ihre Braillezeile eine Tastatur besitzt, können Sie außerdem Kurz-, Voll- oder Basisschrift eingeben.
Die Braillezeile kann auch mit dem [Braille-Btrachter](#BrailleViewer) anstelle oder gleichzeitig mit einer physischen Braille-Zeile auf dem Bildschirm angezeigt werden.

Bitte lesen Sie im Abschnitt [Unterstützte Braillezeilen](#SupportedBrailleDisplays), ob Ihre Braillezeile unterstützt wird.
Dieser Abschnitt enthält auch Informationen darüber, welche Braillezeilen die automatische Braillezeilenerkennung von NVDA unterstützen.
Verwenden Sie die Kategorie "[Braille](#BrailleSettings)" in den NVDA-Einstellungen, um NVDA an Ihre Braillezeile anzupassen.

### Abkürzungen für Steuerelementtypen, Status-Anzeigen und Sprungmarken {#BrailleAbbreviations}

Damit möglichst viele Daten auf der Braillezeile Platz finden, wurden folgende Abkürzungen für Steuerelementtypen, Status-Anzeigen und Sprungmarken festgelegt.

| Abkürzung |Steuerelementtyp|
|---|---|
|app |Anwendung|
|art |Artikel|
|zb |Zitatblock|
|sltr |Schalter|
|aklsltr |Ausklapplistenschalter|
|dsltr |Drehschalter|
|tsltr |Trennschaltfläche|
|umsltr |Umschalter|
|tl |Überschriftentitel|
|kmbf |Konbinationsfeld|
|kf |Kontrollfeld|
|dlg |Dialogfeld|
|dok |Dokument|
|ef |Eingabefeld|
|pef |Passwort-Eingabefeld|
|eo |Eingebettetes Objekt|
|en |Endnote|
|ill |Illustrationen|
|fn |Fußnote|
|grf |Grafik|
|grp |Gruppierung|
|üN |Überschrift der Ordnung N, z. B. ü1, ü2.|
|qi |QuickInfos|
|smk |Sprungmarke|
|lnk |Link|
|bl |Besuchter Link|
|lst |Liste|
|mnü |Menü|
|mnülst |Menüleiste|
|mnüsltr |Menüschalter|
|mnüe |Menüeintrag|
|strg |Steuerung|
|fsb |Fortschrittsbalken|
|besch |Beschäftigt-Status|
|as |Auswahlschalter|
|rb |Rollbalken|
|abs |Abschnitt|
|sz |Statuszeile|
|rk |Registerkarte|
|tbl |Tabelle|
|sN |Tabellenspalte N, z. B. S1, S2.|
|rN |Reihe N in einer Tabelle, z. B. R1, R2.|
|ea |Eingabeaufforderung|
|wl |Werkzeugleiste|
|mh |Minihilfe|
|ba |Baumansicht|
|gldsltr |Gliederungsschalter|
|bae |Eintrag einer Baumstruktur|
|en |Ein Eintrag in einer Baumansicht in der Ebene N|
|fst |Fenster|
|⠤⠤⠤⠤⠤ |Trennlinie|
|mrki |Markierten Inhalt|

Für die folgenden Status-Anzeigen wurden ebenfalls Abkürzungen festgelegt:

| Abkürzung |Status|
|---|---|
|... |Wird angezeigt, wenn ein Objekt automatische Vervollständigung unterstützt.|
|⢎⣿⡱ |Wird angezeigt, wenn ein Schalter gedrückt ist.|
|⢎⣀⡱ |Wird angezeigt, wenn ein Schalter nicht gedrückt wurde.|
|⣏⣿⣹ |Wird angezeigt, wenn ein Objekt (z. B. ein Kontrollfeld) aktiviert ist.|
|⣏⣸⣹ |Wird angezeigt, wenn ein Objekt (z. B. ein Kontrollfeld) teilweise aktiviert ist.|
|⣏⣀⣹ |Wird angezeigt, wenn ein Objekt (z. B. ein Kontrollkästchen) nicht aktiviert ist.|
|- |Wird bei Objekten (z. B. Baum-Einträgen) angezeigt, die reduziert werden können.|
|+ |Wird bei Objekten (z. B. Baum-Einträgen) angezeigt, die erweitert werden können.|
|pef |Wird bei Eingabefeldern für Passwörter angezeigt.|
|klk |Wird bei anklickbaren Elementen angezeigt.|
|kmnt |Wird angezeigt, wenn das aktuelle Objekt ein Kommentar ist.|
|frm |Wird angezeigt, wenn das aktuelle Objekt eine Formel enthält.|
|ungültig |Wird angezeigt, sobald Sie in ein Formularfeld einen ungültigen Wert eingegeben haben.|
|lbesch |Wird angezeigt, wenn das aktuelle Objekt (meist eine Grafik) eine ausführliche Beschreibung enthält.|
|mz |Wird angezeigt, wenn Sie in das Eingabefeld mehrere Zeilen Text eingeben können.|
|erf |Wird angezeigt, wenn in dem Eingabefeld eine Eingabe erforderlich ist.|
|sef |Wird bei Objekten (z. B. Eingabefeldern) angezeigt, die schreibgeschützt sind.|
|(x) |Wird angezeigt, wenn ein Objekt ausgewählt ist.|
|( ) |Wird angezeigt, wenn das aktuelle Objekt nicht ausgewählt ist.|
|auf sortiert |Wird angezeigt, wenn die Liste aufsteigend sortiert ist.|
|ab sortiert |Wird angezeigt, wenn die aktuelle Liste absteigend sortiert ist.|
|-> |Wird angezeigt, wenn ein Objekt ein Untermenü enthält.|

Die folgenden Abkürzungen werden für Sprungmarken verwendet:

| Abkürzung |Sprungmarke|
|---|---|
|bnnr |Banner|
|inh |Inhalt|
|ergz |Ergänzung|
|form |Formular|
|haupt |Haupt|
|navi |Navigation|
|such |Suche|
|rgn |Region|

### Braille-Eingabe {#BrailleInput}

NVDA unterstützt die Eingabe von Kurz-, Voll- und Basisschrift über eine Braille-Tastatur.
Verwenden Sie die Einstellung ["Braille-Eingabetabelle"](#BrailleInputTable) in der Kategorie Braille-Einstellungen, um zu bestimmen, welche Übersetzungstabelle Sie verwenden wollen.

Wenn Sie Basisschrift eingeben, wird der eingegebene Text unmittelbar nach der Eingabe über die Braille-Tastatur in das aktuelle Programm eingefügt.
Wenn Sie Kurz- oder Vollschrift eingeben, wird der Text erst in die aktuelle Anwendung eingefügt, wenn Sie ein Wort mit der Leertaste beenden.
Dies betrifft nur direkt über die Braille-Tastatur eingegebenen Text und bezieht sich nicht auf bereits existierenden Text.
Wenn Sie beispielsweise den Cursor an das Ende einer Zahl bewegt haben, müssen Sie das Zahlenzeichen nochmals eingeben um zusätzliche Stellen anzufügen.

<!-- KC:beginInclude -->
Drücken Sie den Punkt 7, um das letzte Zeichen zu löschen.
Drücken Sie den Punkt 8, um einen Zeilenvorschub einzufügen.
Drücken Sie Punkte 7 und 8, um die eingegebenen Braillezeichen zu übersetzen, ohne einen Zeilenvorschub oder ein Leerzeichen einzufügen.
<!-- KC:endInclude -->

#### Eingabe von Tastaturkürzeln {#BrailleKeyboardShortcuts}

NVDA unterstützt die Eingabe von Tastenkombinationen und die Emulation von Tastendrücken über die Braillezeile.
Diese Emulation gibt es in zwei Formen: Die direkte Zuweisung einer Braille-Eingabe zu einem Tastendruck und die Verwendung der virtuellen Modifikator-Tasten.

Häufig verwendete Tasten, wie die Pfeiltasten oder das Drücken der Alt-Taste zum Aufrufen von Menüs, können direkt mit Braille-Eingaben verknüpft werden.
Der Treiber für jede Braillezeile ist bereits mit einigen dieser Zuordnungen voreingestellt.
Sie können diese Zuweisungen ändern oder neue emulierte Tasten über den [Dialogfeld für die Tastenbefehle](#InputGestures) hinzufügen.

Während dieser Ansatz für häufig gedrückte oder eindeutige Tasten (z. B. Tabulator) nützlich ist, möchten Sie vielleicht nicht jedem Tastaturkürzel einen eindeutigen Satz von Tasten zuweisen.
Zur Emulation von Tastendrücken bei gedrückten Sondertasten bietet NVDA Befehle zum Umschalten der Strg-, Alt-, Umschalt-, Windows- und NVDA-Tasten sowie Befehle für einige Kombinationen dieser Tasten.
Um diese Umschalttasten zu verwenden, drücken Sie zunächst den Befehl (oder die Befehlsfolge) für die Modifikatortasten, die Sie drücken möchten.
Drücken Sie dann den Buchstaben, welcher Teil des gewünschten Tastaturkürzels ist.
Um z. B. Strg+F zu erzeugen, verwenden Sie den Befehl "Strg-Taste umschalten" und geben dann ein F ein,
und um Strg+Alt+T einzugeben, verwenden Sie entweder die Befehle "Strg-Taste umschalten" und "Alt-Taste umschalten" in beliebiger Reihenfolge oder den Befehl "Strg- und Alt-Tasten umschalten" und geben dann ein T ein.

Wenn Sie versehentlich die Modifikatortasten umschalten, können Sie den Befehl "Umschalten" erneut ausführen, um die Modifikatoren wieder zu entfernen.

Wenn Sie in Braille-Schrift tippen, werden Ihre Eingaben mit den Umschalttasten so übersetzt, als ob Sie die Punkte 7+8 gedrückt hätten.
Außerdem kann der emulierte Tastendruck nicht die Braille-Schrift widerspiegeln, die vor dem Drücken der Änderungstaste eingegeben wurde.
Das bedeutet, dass Sie zur Eingabe von Alt+2 mit einem Braille-Code, der ein Zahlenzeichen verwendet, zuerst "Alt umschalten" und dann ein Zahlenzeichen eingeben müssen.

## Visuelle Darstellungen {#Vision}

Während sich NVDA in erster Linie an blinde oder sehbehinderte Menschen richtet, die in erster Linie Sprache und/oder Blindenschrift zur Bedienung eines Computers verwenden, bietet es auch integrierte Möglichkeiten, den Inhalt des Bildschirms zu ändern.
Mit NVDA wird einer solchen Sehhilfe als Quelle zur Bildverbesserung bezeichnet.

NVDA bietet mehrere integrierte Quellen zur Bildverbesserung an, die im Folgenden beschrieben werden.
Zusätzliche Quellen für die Bildverbesserung können über [NVDA-Erweiterungen](#AddonsManager) bereitgestellt werden.

Diese Einstellungen können Sie in den [NVDA-Einstellungen](#NVDASettings), in der Kategorie [Visuelle Darstellungen](#VisionSettings) vornehmen.

### Visuell hervorheben {#VisionFocusHighlight}

Die Funktion "Visuell hervorheben" kann dabei helfen, die Positionen des [System-Fokus](#SystemFokus), des [Navigator-Objekts](#ObjektNavigation) und den [Lesemodus](#BrowseMode) zu identifizieren.
Diese Positionen werden mit einem farbigen Rechteck hervorgehoben.

* Kräftiges Blau markiert die Fokus-Position, wenn sich das Navigator-Objekt an gleicher Stelle befindet (z. B. weil das [Navigator-Objekt dem System-Fokus](#ReviewCursorFollowFocus) folgt).
* Blau gestrichelt markiert nur das Objekt unter dem System-Fokus.
* Kräftiges Rosa hebt nur das Navigatorobjekt hervor.
* Kräftiges Gelb hebt den virtuellen System-Cursor hervor, welcher im Lesemodus verwendet wird. (In diesen Dokumenten gibt es keinen physischen Cursor, wie z. B. in Internet-Browsern).

Wenn Sie Visuell hervorheben in der Kategorie "[Visuelle Darstellungen](#VisionSettings)" der [NVDA-Einstellungen](#NVDASettings) aktiviert haben, können Sie [ändern, ob Sie den Fokus, das Navigator-Objekt oder den Cursor im Lesemodus](#VisionSettingsFocusHighlight) hervorgehoben werden sollen.

### Der Bildschirmvorhang {#VisionScreenCurtain}

Für blinde oder sehbehinderte Benutzer ist es oft nicht möglich oder notwendig, den Inhalt des Bildschirms zu sehen.
Zudem könnte es schwierig sein, sicherzustellen, dass Ihnen niemand über die Schulter schaut.
Dafür gitb es in NVDA den Bildschirmvorhang. Mit dieser Funktion wird der Bildschirm verdunkelt.

Sie können den Bildschirmvorhang in den [NVDA-Einstellungen](#NVDASettings), in der Kategorie [Visuelle Darstellungen](#VisionSettings) aktivieren.

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Bildschirmvorhang ein- oder ausschalten |`NVDA+Strg+Escape` |Aktivieren Sie diesen, um den Bildschirm zu schwärzen oder deaktivieren Sie diesen, um den Bildschirminhalt anzuzeigen. Durch einmaliges Drücken wird der Bildschirmvorhang aktiviert, bis Sie NVDA neu starten. Durch zweimaliges Drücken bleibt der Bildschirmvorhang aktiviert, bis Sie ihn deaktivieren.|

<!-- KC:endInclude -->

Wenn der Bildschirmvorhang aktiv ist, können einige Aufgaben, die direkt auf der Bildschirmanzeige basieren, wie das Ausführen der [Texterkennung](#Win10Ocr) oder das Erstellen eines Screenshots, nicht ausgeführt werden.

Auf Grund einer Änderung in der API für die Windows-Lupe musste die Funktion des Bildschirmvorhangs aktualisiert werden, um die neuesten Versionen von Windows zu unterstützen.
Verwenden Sie NVDA 2021.2, um den Bildschirmvorhang mit Windows 10 Version 21H2 (10.0.19044) oder neuer zu aktivieren.
Wenn Sie eine neue Windows-Version verwenden, erhalten Sie aus Sicherheitsgründen eine visuelle Bestätigung, dass der Bildschirmvorhang den Bildschirm vollständig verdunkelt.

Bitte beachten Sie, dass der Bildschirmvorhang nicht aktiviert werden kann, solange die Windows-Lupe läuft und die invertierten Bildschirmfarben verwendet werden.

## Inhalte erkennen {#ContentRecognition}

Wenn Entwickler von Anwendungen unzureichende Informationen zur Zugänglichkeit bereitstellen, können Sie zahlreiche Tools verwenden, um z. B. Text aus einem Bild auszulesen.
NVDA unterstützt die in Windows 10 und neuer enthaltene Texterkennung, um Text aus Bildern auszulesen.
Über NVDA-Erweiterungen können zusätzliche Tools zur Erkennung von Inhalten bereitgestellt werden.

Wenn Sie ein Tool zur Erkennung von Inhalten verwenden, bezieht sich die Erkennung grundsätzlich auf das aktuelle [Navigator-Objekt](#ObjectNavigation).
Da der Navigator standardmäßig an den Fokus bzw. den Lesemodus gekoppelt ist, können Sie normalerweise einfach den Fokus an die gewünschte Stelle innerhalb der Anwendung oder im Dokument ziehen.
Wenn Sie den Cursor im Lesemodus auf eine Grafik bewegen, wird die Erkennung von Inhalten diese Grafik erkennen.
Sie können jedoch trotzdem die Objektnavigation verwenden, um z. B. den Inhalt eines ganzen Anwendungsfensters zu erkennen.

Wenn die Erkennung abgeschlossen ist, wird das Erkennungsergebnis in einem Dokument ähnlich dem Lesemodus angezeigt, in dem Sie das Erkennungsergebnis mit den Pfeiltasten lesen können.
Drücken Sie die Leertaste oder die Eingabetaste, um den Text (üblicherweise durch Klicken) zu aktivieren.
Drücken Sie die Escape-Taste, um das Fenster mit dem Ergebnis zu schließen.

### Windows-Texterkennung {#Win10Ocr}

Windows 10 und neuer enthält eine optische Zeichenerkennung für viele Sprachen.
Sie können diese Zeichenerkennung verwenden, um Text aus Grafiken oder unzugänglichen Anwendungen auszulesen.

Sie können die Sprache für die Texterkennung in der Kategorie "[Windows-Texterkennung](#Win10OcrSettings)" in den [NVDA-Einstellungen](#NVDASettings) festlegen.
Zusätzliche Sprachen können Sie in den Einstellungen von Windows unter Zeit und Sprache -> Region und Sprache -> Sprache hinzufügen installieren.

Wenn Sie ständig wechselnde Inhalte überwachen möchten, wie z. B. beim Ansehen eines Videos mit Untertiteln, können Sie optional die automatische Aktualisierung erkannter Inhalte aktivieren.
Dies kann auch in der [Kategorie "Windows-Texterkennung"](#Win10OcrSettings) in den [NVDA-Einstellungen](#NVDASettings) erfolgen.

Die integrierte Texterkennung in Windows kann teilweise oder ganz inkompatibel mit [NVDA-Sehhilfen](#Vision) oder anderen externen Sehhilfen sein. Sie müssen diese Hilfen deaktivieren, bevor Sie mit einer Erkennung fortfahren.

<!-- KC:beginInclude -->
Drücken Sie NVDA+R, um den Text im aktuellen NAvigator-Objekt mit Hilfe der Windows-Texterkennung zu erkennen.
<!-- KC:endInclude -->

## Anwendungsspezifische Funktionen {#ApplicationSpecificFeatures}

NVDA stellt für bestimmte Anwendungen zusätzliche Funktionen bereit, um bestimmte Aufgaben zu erleichtern oder um Zugriff auf Funktionalität bereitzustellen, die sonst nicht zugänglich wäre.

### Microsoft Word {#MicrosoftWord}
#### Automatisches Lesen von Zeilen- und Spaltenüberschriften {#WordAutomaticColumnAndRowHeaderReading}

Wenn Sie in Microsoft Word in einer Tabelle navigieren, ist NVDA in der Lage, automatisch die Zeilen- und Spaltenüberschriften zu lesen.
Hierfür muss die Option "Reihen- und Spaltenüberschriften von Tabellen ansagen" unter der Kategorie "Dokumentformatierungen" in den [NVDA-Einstellungen](#NVDASettings) aktiviert sein.

Wenn Sie [UIA für den Zugriff auf Word-Dokumente](#MSWordUIA) verwenden, was in neueren Versionen von Word und Windows Standard ist, werden die Zellen der ersten Zeile automatisch als Spaltenüberschriften betrachtet; Ebenso werden die Zellen der ersten Spalte automatisch als Zeilenüberschriften betrachtet.

Wenn Sie hingegen nicht [UIA für den Zugriff auf Word-Dokumente](#MSWordUIA) verwenden, müssen Sie NVDA mitteilen, welche Zeile oder Spalte die Überschriften in einer bestimmten Tabelle enthält.
Verwenden Sie einen der folgenden Befehle, nachdem Sie sich in die erste Zelle mit der Reihen- und Spaltenüberschrift bewegt haben:
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Spaltenüberschriften festlegen |NVDA+Umschalt+C |Wenn Sie diese Tastenkombination einmal drücken, legen sie die aktuelle Tabellenzelle als erste Zelle mit Spaltenüberschriften fest. Diese Spaltenüberschriften werden dann automatisch gelesen, sobald Sie unterhalb dieser Zeile navigieren. Zweimaliges Drücken dieser Tastenkombination löscht diese Zuweisung wieder.|
|Zeilenüberschriften festlegen |NVDA+Umschalt+R |Wenn Sie diese Tastenkombination einmal drücken, wird die aktuelle Tabellenzelle als erste Zelle mit Zeilenbeschriftung festgelegt. Diese Spaltenüberschriften werden dann automatisch gelesen, sobald Sie unterhalb dieser Zeile navigieren. Zweimaliges Drücken dieser Tastenkombination löscht diese Zuweisung wieder.|

<!-- KC:endInclude -->
Diese Zuweisungen werden im Dokument als Lesezeichen gesetzt. Dies ist kompatibel zu anderen Bildschirmlesern wie JAWS.
Dies bedeutet, dass auch andere Anwender von Bildschirmlesern, die dieses Dokument zu einem späteren Zeitpunkt öffnen, die Spalten- und Zeilenüberschriften gesetzt haben.

#### Lesemodus in Microsoft Word {#BrowseModeInMicrosoftWord}

Ähnlich wie im Netz können Sie in Microsoft Word den Lesemodus sowie die Elementliste oder die Schnellnavigation nutzen.
<!-- KC:beginInclude -->
Um den Lesemodus in Microsoft Word ein- oder auszuschalten, drücken Sie NVDA+Leertaste.
<!-- KC:endInclude -->
Weitere Informationen zum Lesemodus und zur Schnellnavigation finden Sie im [Abschnitt über den Lesemodus](#BrowseMode).

##### Die Elementliste {#WordElementsList}

<!-- KC:beginInclude -->
Wenn Sie sich in Microsoft Word im Lesemodus befinden, können Sie mit der Tastenkombination NVDA+F7 auf die Elementliste zugreifen.
<!-- KC:endInclude -->
Die Elementliste enthält Überschriften, Links, Anmerkungen (einschließlich nachverfolgbarer Änderungen), und Fehler (derzeit auf Rechtschreibfehler limitiert).

#### Ausgeben von Kommentaren {#WordReportingComments}

<!-- KC:beginInclude -->
Verwenden Sie die Tastenkombination NVDA+Alt+C, um sich einen Kommentar an der aktuellen Cursorposition anzeigen zu lassen, sofern vorhanden.
<!-- KC:endInclude -->
Alle Kommentare des aktuellen Dokuments sind außerdem in der Elementliste aufgeführt, wenn Sie als Elementtyp "Anmerkungen" auswählen.

### Microsoft Excel {#MicrosoftExcel}
#### Automatisches Lesen von Zeilen- und Spaltenüberschriften {#ExcelAutomaticColumnAndRowHeaderReading}

Wenn Sie in Microsoft Excel in einer Tabelle navigieren, ist NVDA in der Lage, automatisch die Zeilen- und Spaltenüberschriften zu lesen.
Hierfür muss die Option "Reihen- und Spaltenüberschriften von Tabellen ansagen" unter der Kategorie "Dokumentformatierungen" in den [NVDA-Einstellungen](#NVDASettings) aktiviert sein.
NVDA muss die Reihen oder Spalten mit den Überschriften kennen.
Verwenden Sie einen der folgenden Befehle, nachdem Sie sich in die erste Zelle mit der Reihen- und Spaltenüberschrift bewegt haben:
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Spaltenüberschriften festlegen |NVDA+Umschalt+C |Wenn Sie diese Tastenkombination einmal drücken, legen sie die aktuelle Tabellenzelle als erste Zelle mit Spaltenüberschriften fest. Diese Spaltenüberschriften werden dann automatisch gelesen, sobald Sie unterhalb dieser Zeile navigieren. Zweimaliges Drücken dieser Tastenkombination löscht diese Zuweisung wieder.|
|Zeilenüberschriften festlegen |NVDA+Umschalt+R |Wenn Sie diese Tastenkombination einmal drücken, wird die aktuelle Tabellenzelle als erste Zelle mit Zeilenbeschriftung festgelegt. Diese Spaltenüberschriften werden dann automatisch gelesen, sobald Sie unterhalb dieser Zeile navigieren. Zweimaliges Drücken dieser Tastenkombination löscht diese Zuweisung wieder.|

<!-- KC:endInclude -->
Diese Zuweisungen werden in der Arbeitsmappe als definierte Namensbereiche gesetzt. Dies ist kompatibel zu anderen Screenreadern wie JAWS.
Dies bedeutet, dass auch andere Anwender von Screenreadern, die dieses Dokument zu einem späteren Zeitpunkt öffnen, die Spalten- und Zeilenüberschriften gesetzt haben.

#### Die Elementliste {#ExcelElementsList}

Ähnlich wie im Netz können Sie in Microsoft Excel die Elementliste nutzen, um verschiedene Informationen aufzulisten und um auf diese zuzugreifen.
<!-- KC:beginInclude -->
Verwenden Sie die Tastenkombination NVDA+F7, um auf die Elementliste zuzugreifen.
<!-- KC:endInclude -->
Die Elementliste enthält Elemente der folgenden Typen:

* Diagramme: Listet alle Diagramme auf dem aktuellen Tabellenblatt auf.
Nachdem Sie ein Diagramm mit Eingabe oder dem Schalter wechseln zu ausgewählt haben, können Sie sich mit Hilfe der Pfeiltasten durch dessen Inhalt bewegen.
* Kommentare: Listet alle Zellen auf dem aktuellen Tabellenblatt auf, die Kommentare enthalten.
Es wird die Zellenadresse nebst Kommentar angezeigt.
Wenn Sie innerhalb der Liste den Schalter "wechseln zu" oder die Eingabetaste drücken, wird der Fokus auf die entsprechende Zelle verschoben.
* Formeln: Listet alle Zellen auf dem Tabellenblatt auf, die eine Formel enthalten.
Es wird die Zellenadresse nebst Formel angezeigt.
Wenn Sie innerhalb der Liste den Schalter "Wechseln zu" oder die Eingabetaste drücken, wird der Fokus auf die entsprechende Zelle verschoben.
* Tabellenblätter: Listet alle Tabellenblätter in der Arbeitsmappe auf.
Drücken Sie auf einem der aufgelisteten Tabellenblätter die Taste F2, um dieses umzubenennen.
Drücken Sie auf einem Tabellenblatt die Eingabetaste oder den Schalter "wechseln zu", um es zu öffnen.
* Formularfelder: Listet alle Formularfelder im aktiven Tabellenblatt auf.
NVDA zeigt zu jedem Formularfeld dessen Alternativtext sowie die Adresse der Zelle an, die das Formularfeld enthält.
Wählen Sie ein Formularfeld in der Liste aus und verwenden Sie den Schalter "Wechseln zu", um im Lesemodus auf das Formularfeld zu gelangen.

#### Anmerkungen anzeigen {#ExcelReportingComments}

<!-- KC:beginInclude -->
Verwenden Sie die Tastenkombination NVDA+Alt+C, um sich die Anmerkungen der aktuellen Zelle anzeigen zu lassen, sofern vorhanden.
In Microsoft 2016 / 365 und neuer wurden die klassischen Kommentare in Microsoft Excel in "Anmerkungen" umbenannt.
<!-- KC:endInclude -->
Alle Anmerkungen im Arbeitsblatt können nach Drücken von NVDA+F7 auch in der NVDA-Elementliste aufgelistet werden.

NVDA kann auch ein spezielles Dialogfeld zum Hinzufügen oder Bearbeiten bestimmter Anmerkung anzeigen.
NVDA überschreibt auf Grund von Einschränkungen der Zugänglichkeit den nativen Bearbeitungsbereich für die Anmerkungen in Microsoft Excel, aber die Tastenkombination für das Dialogfeld wird von Microsoft Excel übernommen und funktioniert daher auch ohne NVDA.
<!-- KC:beginInclude -->
Sie können in der aktuellen Zelle Umschalt+F2 drücken, um bestimmte Anmerkungen hinzuzufügen oder zu bearbeiten.
<!-- KC:endInclude -->

Diese Tastenkombination kann nicht im Dialogfeld für die Tastenbefehle geändert werden.

Hinweis: Es ist möglich, den Bereich zur Bearbeitung von Anmerkungen in Microsoft Excel auch über das Kontextmenü einer beliebigen Zelle des Arbeitsblatts zu öffnen.
Dadurch wird jedoch der unzugängliche Bereich zur Bearbeitung von Anmerkungen geöffnet und nicht das NVDA-spezifische Dialogfeld zur Bearbeitung der Anmerkungen.

In Microsoft Office 2016 / 365 und neuer wurde ein Kommentar-Dialogfeld im neuen Stil hinzugefügt.
Dieses Dialogfeld ist besser zugänglich und bietet mehr Funktionen wie die Beantwortung von Kommentaren, etc.
Über das Kontextmenü einer bestimmten Zelle kann dies erreicht werden.
Die Kommentare, die in den Zellen über das Kommentar-Dialogfeld des neuen Stils hinzugefügt werden, haben nichts mit den "Anmerkungen" zu tun.

#### Ausgeben geschützter Zellen {#ExcelReadingProtectedCells}

Wenn ein Excel-Arbeitsblatt geschützt wurde, können manche Zellen für eine Bearbeitung gesperrt sein. Solche Zellen sind dann normalerweise nicht zugänglich.
<!-- KC:beginInclude -->
Um auf gesperrte Zellen zuzugreifen, wechseln Sie zunächst mit NVDA+Leertaste in den Lesemodus und navigieren Sie anschließend mit den Standard-Excel-Tastenkombinationen wie z. B. den Pfeiltasten zu den gewünschten Zellen.
<!-- KC:endInclude -->

#### Formularfelder {#ExcelFormFields}

Excel-Tabellenblätter können Formularfelder enthalten.
Sie können entweder die Elementliste oder die Schnellnavigationstasten f und Umschalt+F verwenden, um auf Formularfelder zuzugreifen.
Anschließend können Sie mit der Leertaste oder mit der Eingabetaste den Fokusmodus aktivieren um mit dem Formularfeld umzugehen.
Weitere Informationen über den Lesemodus und die Schnellnavigationstasten finden Sie im [Abschnitt über den Lesemodus](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Notizen des Vortragenden anzeigen |Strg+Umschalt+S |Mit dieser Tastenkombination können Sie zwischen Ihren Notizen und dem eigentlichen Folieninhalt umschalten, während eine Präsentation abläuft. Dies wirkt sich nicht auf die Anzeige am Bildschirm aus, sondern lediglich auf die Anzeige innerhalb von NVDA.|

<!-- KC:endInclude -->

### Foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Verbleibende Zeit ausgeben |Strg+Umschalt+R |Falls grade ein Titel abgespielt wird, wird die verbleibende Zeit ausgegeben.|
|Verstrichene Zeit ausgeben |Strg+Umschalt+E |Gibt die verstrichene Zeit des aktuellen Titels aus, sofern ein Titel abgespielt wird.|
|Länge des Titels ausgeben |Strg+Umschalt+T |Gibt die Länge des aktuellen Titels aus, sofern ein Titel abgespielt wird.|

<!-- KC:endInclude -->

Hinweis: die obigen Tastenkombinationen funktionieren nur, wenn die Standard-Einstellungen für die Statuszeile gewählt sind.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Letzte Nachricht ausgeben |NVDA+Strg+1 bis 4 |Gibt die zur Nummer passende Nachricht aus; NVDA+Strg+2 gibt beispielsweise die vorletzte Nachricht aus.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA bietet erweiterte Unterstützung für Poedit 3.4 oder neuer.

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Anmerkungen für Übersetzer ausgeben |`Strg+Umschalt+A` |Gibt alle Anmerkungen für Übersetzer aus. Bei zweimaligem Drücken werden die Anmerkungen im Lesemodus angezeigt.|
|Kommentare ausgeben |Strg+Umschalt+C |Gibt alle Kommentare im Kommmentarbereich aus. Zweimaliges Drücken zeigt die Kommentare im Lesemodus.|
|Alten Quelltext ausgeben |`Strg+Umschalt+o` |Gibt den alten Quelltext aus, falls vorhanden. Bei zweimaligem Drücken wird der Text im Lesemodus angezeigt.|
|Übersetzungswarnung ausgeben |`Strg+Umschalt+W` |Gibt evtl. vorhandene Übersetzungswarnung aus. Bei zweimaligem Drücken wird die Warnung im Lesemodus angezeigt|

<!-- KC:endInclude -->

### Amazon Kindle für PC {#Kindle}

NVDA unterstützt das Lesen von und das Navigieren in Büchern in Kindle für PC.
Diese Funktionalität ist nur verfügbar, wenn die Bücher mit der Unterstützung für Screen Reader herausgegeben wurden. Dies können Sie auf der Detailseite des Buches überprüfen.

Der Lesemodus wird beim Lesen von Büchern verwendet.
Er wird automatisch aktiviert, wenn Sie ein Buch öffnen.
Die Seiten werden automatisch umgeblättert, wenn Sie den Cursor im virtuellen Dokument bewegen oder den Befehl zum Vorlesen von Dokumenten verwenden.
<!-- KC:beginInclude -->
Sie können auch manuell zwischen den Seiten blättern. Verwenden Sie hierfür die Tasten Seite auf und Seite ab.
<!-- KC:endInclude -->

Die Schnellnavigation für Links und Grafiken funktioniert auf der aktuellen Seite.
Die Linknavigation beinhaltet auch Fußnoten.

NVDA bietet frühe Unterstützung beim Lesen und interaktiver Navigation von mathematischen Inhalten für Bücher mit barrierefreier Mathematik.
Für weitere Informationen lesen Sie den Abschnitt [Mathematische Inhalte lesen](#ReadingMath)

#### Markieren von Text {#KindleTextSelection}

Mit Kindle können Sie verschiedene Funktionen für den ausgewählten Text ausführen, z. B. eine Wörterbuch-Definition erhalten, Notizen und Hervorhebungen hinzufügen, den Text in die Zwischenablage kopieren und das Web durchsuchen.
Markieren Sie dazu zuerst den Text mit dem im Lesemodus üblichen tasten(Kombinationen) (z. B. umschalt+Richtungstasten).
<!-- KC:beginInclude -->
Nachdem Sie Text markiert haben, drücken Sie die Anwendungstaste oder Umschalt+F10, um die verfügbaren Optionen anzuzeigen.
<!-- KC:endInclude -->
Wenn Sie keinen Text markiert haben, beziehen sich die angezeigten Optionen auf das Wort am Cursor.

#### Notizen {#KindleUserNotes}

Sie können eine Notiz zu einem Wort oder einer ganzen Passage hinzufügen.
Um dies zu tun, markieren Sie den relevanten Text und öffnen die Markierungsoptionen wie oben beschrieben.
Nun wählen Sie Notiz hinzufügen.

Während Sie im Lesemodus lesen, werden Notizen als Kommentare ausgegeben.

Eine Notiz lesen, bearbeiten oder löschen:

1. Bewegen Sie den Cursor zum Text, der die Notiz enthält.
1. Rufen Sie die Markierungsoptionen wie oben beschrieben auf.
1. Wählen Sie Notiz bearbeiten.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Wenn Sie sich in der Tabellenansicht der hinzugefügten Bücher befinden:

| Name |Taste |Beschreibung|
|---|---|---|
|Eingabe |Eingabe |Öffnet das ausgewählte buch.|
|Kontextmenü |Anwendungen |Öffnet das Kontextmenü für das ausgewählte Buch.|

<!-- KC:endInclude -->

### Die Windows-Konsole {#WinConsole}

NVDA bietet Unterstützung für die Windows-Befehlskonsole, die von der Eingabeaufforderung, PowerShell und dem Windows-Subsystem für Linux verwendet wird.
Das Konsolenfenster ist von fester Größe und typischerweise viel kleiner als der Puffer, der die Ausgabe enthält.
Wenn neuer Text erscheint, läuft der Inhalt nach oben aus dem Bildschirm und der vorherige Text ist nicht mehr sichtbar.
Bei Windows-Versionen älter als Windows 11 Version 22H2 ist Text in der Konsole, der nicht sichtbar im Fenster angezeigt wird, nicht mit den Textbefehlen von NVDA zugänglich.
Daher ist es notwendig, im Konsolenfenster zu navigieren, um frühere Texte zu lesen.
In neueren Versionen der Konsole und im Windows-Terminal ist es möglich, die gesamte Textansicht auszulesen, ohne dass das Fenster gescrollt werden muss.
<!-- KC:beginInclude -->
Die folgenden integrierten Tastenkombinationen für die Windows-Konsole können beim [Textlesen](#ReviewingText) mit NVDA in älteren Versionen der Windows-Konsole nützlich sein:

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Nach oben rollen |Strg+Pfeiltaste nach oben |Rollt das Konsolenfenster nach oben, sodass früherer Text gelesen werden kann.|
|Nach unten rollen |Strg+Pfeiltaste nach unten |Rollt das Konsolenfenster nach unten, sodass späterer Text gelesen werden kann.|
|Zum Anfang rollen |Strg+Pos1 |Rollt das Konsolenfenster zum Anfang des Puffers.|
|Zum Ende rollen |Strg+Ende |Rollt das Konsolenfenster zum Ende des Puffers.|

<!-- KC:endInclude -->

## NVDA konfigurieren {#ConfiguringNVDA}

Die meisten NVDA-Einstellungen können über Dialogfelder vorgenommen werden, die im Untermenü des NVDA-Menüs zu finden sind.
Viele Einstellungen können in den mehrseitigen [NVDA-Einstellungen](#NVDASettings) vorgenommen werden.
In allen Einstellungen können Sie auf den Schalter "OK" klicken, um die Einstellung zu übernehmen und das Fenster zu schließen.
Um Einstellungen zu verwerfen, klicken Sie auf den Schalter "Abbrechen" oder drücken die Escape-Taste.
Für manche Einstellungen können Sie auch auf den Schalter "Übernehmen" klicken, um weiterhin in den NVDA-Einstellungen zu bleiben, wobei die Einstellungen aktiv werden.
Die meisten NVDA-Dialoge unterstützen Kontexthilfe.
<!-- KC:beginInclude -->
Wenn Sie in einem Dialog "f1" drücken, wird das Benutzerhandbuch in dem Absatz geöffnet, der sich auf die fokussierte Einstellung oder den aktuellen Dialog bezieht.
<!-- KC:endInclude -->
Einige Einstellungen können auch durch Kurztasten geändert werden. Diese Kurztasten werden in den entsprechenden Abschnitten aufgelistet.

### Die NVDA-Einstellungen {#NVDASettings}

<!-- KC:settingsSection: || Name | Desktop-Tastenkombination | Laptop-Tastenkombination | Beschreibung | -->
NVDA bietet viele Konfigurationsparameter, die über das Dialogfeld für die Einstellungen geändert werden können.
Um die Art der Einstellungen, die Sie ändern möchten, leichter zu finden, zeigt das Dialogfeld eine Liste von Konfigurationskategorien zur Auswahl an.
Wenn Sie eine Kategorie auswählen, werden alle zugehörigen Einstellungen im Dialogfeld dazu angezeigt.
Um sich zwischen den Kategorien zu bewegen, benutzen Sie `Tab` oder `Umschalt+Tab`, um die Liste der Kategorien zu erreichen und dann die Pfeiltasten nach oben oder unten, um in der Liste zu navigieren.
Von überall in diesem Dialogfeld aus können Sie auch mit der Tastenkombination `Strg+Tab` eine Kategorie vorwärts oder mit `Umschalt+Strg+Tab` eine Kategorie zurück gehen.

Sobald Sie eine oder mehrere Einstellungen geändert haben, können Sie die Einstellungen mit der Schaltfläche "Übernehmen" speichern. In diesem Fall bleibt das Dialogfeld geöffnet, so dass Sie weitere Einstellungen ändern oder eine andere Kategorie auswählen können.
Wenn Sie die Einstellungen speichern und das Dialogfeld schließen möchten, verwenden Sie stattdessen den Schalter "OK".

Einige Kategorien besitzen eine Kurztaste für den direkten Aufruf.
Wenn die Tastenkombination gedrückt wird, öffnet sich das Dialogfeld für die Einstellung direkt für die jeweilige Kategorie.
Beachten Sie, dass standardmäßig nicht alle Einstellungskategorien mittels Tastenkombination, Tastenbefehle, etc. aufgerufen werden können.
Wenn Sie häufig auf Kategorien zugreifen, für die es keine eigenen Tastenkombinationen gibt, können Sie im Dialogfeld für die [Tastenbefehle](#InputGestures) einen benutzerdefinierten Tastenbefehl für diese Kategorie hinzufügen.

Weiter unten finden Sie Erläuterungen zu jeder Kategorie aus den NVDA-Einstellungen.

#### Allgemeine Einstellungen {#GeneralSettings}

<!-- KC:setting -->

##### Allgemeine Einstellungen öffnen {#toc110}

Tastenkombination: `NVDA+Strg+G`

Die Kategorie "Allgemein" in den NVDA-Einstellungen legt das allgemeine Verhalten von NVDA fest, wie z. B. die Sprache der Benutzeroberfläche und ob nach Updates gesucht werden soll oder nicht.
Diese Kategorie enthält die folgenden Optionen:

##### Sprache der Oberfläche {#GeneralSettingsLanguage}

In dieser Liste können Sie die Sprache festlegen, in welcher die Benutzeroberfläche und die Meldungen von NVDA ausgegeben werden sollen.
Standardmäßig ist die Option "Benutzerstandard, Windows" ausgewählt. NVDA enthält eine Vielzahl integrierter Sprachen.
Dies besagt, dass NVDA die Sprache verwendet, welche in Windows eingestellt ist.

Bitte beachten Sie: Um die Sprache der Oberfläche zu ändern, muss NVDA neu gestartet werden.
Wenn das Bestätigungsfenster erscheint, wählen Sie "Jetzt neu starten" oder "Später neu starten", wenn Sie die neue Sprache jetzt oder zu einem späteren Zeitpunkt verwenden möchten. Wenn "Später neu starten" ausgewählt ist, muss die Konfiguration gespeichert werden (entweder manuell oder über die Save-On-Exit-Funktion).

##### Einstellungen beim Beenden speichern {#GeneralSettingsSaveConfig}

Diese Option ist ein Kontrollfeld, wenn aktiviert, speichert NVDA jedes Mal beim Beenden automatisch die aktuelle Konfiguration.

##### Optionen zum Beenden von NVDA anzeigen {#GeneralSettingsShowExitOptions}

Mit diesem Kontrollkästchen legen Sie fest, ob beim Beenden von NVDA ein Dialogfeld angezeigt wird. Hier können Sie verschiedene Aktionen auslösen.
Wenn das Kontrollkästchen aktiviert ist, können Sie in diesem Dialogfeld auswählen, ob Sie NVDA beenden, neu starten, mit deaktivierten NVDA-Erweiterungen neu starten oder ein ausstehendes Update installieren möchten.
Wenn das Kontrollkästchen nicht aktiviert ist, wird NVDA sofort beendet.

##### Sounds beim Starten und Beenden von NVDA {#GeneralSettingsPlaySounds}

Dieses Kontrollkästchen legt fest, ob NVDA beim Starten oder Beenden einen Sound wiedergeben soll.

##### Protokollierungsstufe {#GeneralSettingsLogLevel}

Mit diesem Kombinationsfeld können Sie einstellen, wie viel NVDA während der Ausführung protokollieren soll.
Normalerweise müssen Anwender diese Option nicht verändern, weil keine unnötigen Informationen protokolliert werden.
Wenn Sie jedoch Informationen in einem Fehlerbericht bereitstellen oder die Protokollierung ganz aktivieren oder deaktivieren möchten, kann dies eine nützliche Option sein.

Die verfügbaren Protokollierungsstufen sind:

* Ausgeschaltet: Neben einer kurzen Startmeldung protokolliert NVDA während der Ausführung keine weiteren Meldungen.
* Informationen: NVDA protokolliert grundlegende Informationen wie Startmeldungen und Informationen, die für Entwickler nützlich sind.
* Debug-Warnmeldungen: Warnmeldungen, die nicht durch schwere Fehler verursacht werden, werden protokolliert.
* Ein- und Ausgaben: Mit dieser Option werden Eingaben via Tastatur und Braillezeile sowie Ausgaben via Sprachausgabe und Braillezeile protokolliert.
Wenn Sie sich Sorgen um den Datenschutz machen, verwenden Sie diese Option nicht.
* Debug-Meldungen: Zusätzlich zu den Informationen, Warn- und Ein-/Ausgabemeldungen werden weitere Debug-Meldungen protokolliert.
Genau wie bei der Ein-/Ausgabe: Sollten Sie sich um den Datenschutz sorgen, empfielt es sich, diese Option nicht zu benutzen.

##### NVDA automatisch nach der Windows-Anmeldung starten {#GeneralSettingsStartAfterLogOn}

Wenn diese Option aktiviert ist, wird NVDA automatisch gestartet, sobald Sie sich bei Windows anmelden.
Diese Option ist nur in der installierten Version verfügbar!

##### NVDA bei der Windows-Anmeldung verwenden (Administratorrechte sind erforderlich) {#GeneralSettingsStartOnLogOnScreen}

Wenn Sie sich bei Windows mit Ihrem Benutzernamen und Ihrem Passwort anmelden, bewirkt dieses Kontrollfeld, dass NVDA automatisch bereits bei der Anmeldung gestartet wird.
Diese Option ist nur in der installierten Version verfügbar!

##### Aktuell gespeicherte Einstellungen  für die Windows-Anmeldung und bei Sicherheitsmeldungen verwenden (erfordert Administrationsberechtigungen!) {#GeneralSettingsCopySettings}

Mit dieser Schaltfläche wird die aktuell gespeicherte NVDA-Benutzerkonfiguration in das Systemkonfigurationsverzeichnis von NVDA kopiert, sodass NVDA sie bei der Anmeldung und bei der Benutzerkontensteuerung und [anderen Sicherheitsmeldungen](#SecureScreens) verwendet.
Speichern Sie zuvor Ihre Konfiguration, um sicherzustellen, dass auch tatsächlich all Ihre Einstellungen übernommen wurden. Sie können dies im NVDA-Menü oder mit der Tastenkombination NVDA+Strg+C vornehmen.
Diese Option ist nur in der installierten Version verfügbar!

##### Automatisch nach Updates suchen {#GeneralSettingsCheckForUpdates}

Wenn diese Option aktiviert ist, sucht NVDA automatisch nach Updates und informiert Sie, sobald eine neue Version verfügbar ist.
Sie können auch manuell nach neuen Versionen suchen, indem Sie im Hilfe-Menü von NVDA den Eintrag "Nach Updates suchen" auswählen.
Um beim Suchen nach Updates sicherzustellen, dass Sie auch wirklich das passende Update erhalten, ist es erforderlich, einige Informationen an den Update-Server von NV Access zu senden. Dies gilt sowohl für die manuelle als auch für die automatische Suche nach Updates.
Die folgenden Informationen werden dabei gesendet:

* Aktuelle NVDA-Version
* Betriebssystem-Version
* System-Architektur (32- oder 64-Bit)

##### NVDA-Nutzungsdaten sammeln und an NV Access übermitteln {#GeneralSettingsGatherUsageStats}

Ist diese Option aktiviert, sammelt NV Access zusätzliche Informationen wie die Landessprache, das Land oder die geografische Region. Diese Informationen werden benutzt, um Nutzungsstatistiken über die Anzahl der NVDA-Nutzer zu erstellen.
Auch wenn die IP-Adresse zum Ermitteln des (ungefähren) geografischen Standortes verwendet wird, wird sie niemals protokolliert.
Wenn die Option aktiviert ist, werden die folgenden Daten zusätzlich gesendet:

* Eingestellte Landessprache in NVDA.
* Art der NVDA-Instanz (portabel oder installiert).
* Name der verwendeten Sprachausgabe (einschließlich Name der Erweiterung, aus der die Sprachausgabe stammt).
* Name der verwendeten Braillezeile (einschließlich Name der Erweiterung, aus der der Treiber stammt).
* Aktuelle Ausgabetabelle (sofern Braille benutzt wird).

Diese Informationen helfen NV Access bei der zukünftigen Entwicklung von NVDA.

##### Beim NVDA-Start auf ausstehende Updates hinweisen {#GeneralSettingsNotifyPendingUpdates}

Wenn diese Option aktiviert ist, informiert NVDA nach dem Start darüber, falls ein Update noch aussteht, um diese zu installieren.
Sie können ausstehende Updates auch manuell über das NVDA-Menü, das Dialogfeld zum Beenden von NVDA oder durch eine erneute Suche nach Updates aus dem Hilfe-Menü installieren.

#### Die Sprachausgaben-Einstellungen {#SpeechSettings}

<!-- KC:setting -->

##### Einstellungen für Sprachausgaben öffnen {#toc123}

Tastenkombination: `NVDA+Strg+V`

Die Kategorie "Sprachausgabe" in den NVDA-Einstellungen enthält Optionen, mit denen Sie die Sprachausgabe sowie die Sprachmerkmale der ausgewählten Sprachausgabe ändern können.
Für eine schnellere Möglichkeit, Sprachparameter von überall her zu steuern, lesen Sie bitte den Abschnitt [Sprachausgaben-Einstellungsring](#SynthSettingsRing).

Diese Einstellungen enthalten die folgenden Optionen:

##### Sprachausgabe ändern {#SpeechSettingsChange}

Die Option in dieser Kategorie ist der Schalter "Ändern". Dieser Schalter öffnet das Dialogfeld zum [Ändern der Sprachausgabe](#SelectSynthesizer). Dort befinden sich alle verfügbaren Sprachausgaben und Ausgabegeräte, über welche die Sprachausgabe sich steuern lassen.
Dieses Dialogfeld wird zusätzlich zu den Einstellung geöffnet.
Wenn das Dialogfeld zum Ändern der Sprachausgabe mit "OK" oder "Abbrechen" geschlossen wird, erscheinen wieder die NVDA-Einstellungen mit den dazugehörigen Kategorien.

##### Stimme {#SpeechSettingsVoice}

Die Stimmenoption ist eine Ausklappliste mit allen verfügbaren Stimmen der zuvor ausgewählten Sprachausgabe.
Mit den Pfeiltasten können Sie sich die Stimmen testweise anhören.
Die Pfeiltasten nach oben oder nach links verschieben den Fokus nach oben, die Pfeiltasten nach unten oder rechts entsprechend nach unten in der Ausklappliste.

##### Variante {#SpeechSettingsVariant}

Wenn Sie die Sprachausgabe eSpeak NG verwenden, die bei NVDA mitgeliefert wird, handelt es sich um ein Kombinationsfeld, in dem Sie die Variante der Sprachausgabe auswählen können.
Die Varianten von eSpeak NG sind mit Stimmen vergleichbar, weil sie die Eigenschaften von eSpeak NG verändern.
Einige Varianten hören sich weiblich, männlich oder sogar wie ein Frosch an.
Wenn Sie eine Sprachausgabe eines Drittanbieters verwenden, können Sie diesen Wert möglicherweise auch ändern, wenn Ihre gewählte Stimme dies unterstützt.

##### Geschwindigkeit {#SpeechSettingsRate}

Mit dieser Option können Sie die Sprechgeschwindigkeit der Stimme festlegen.
Dies ist ein Schieberegler, der von 0 bis 100 reicht (0 ist sehr langsam, 100 ist sehr schnell).

##### Sprachgeschwindigkeit anheben {#SpeechSettingsRateBoost}

Durch Aktivieren dieser Option wird die Sprachgeschwindigkeit deutlich angehoben, sofern dies von der aktuellen Sprachausgabe unterstützt wird.

##### Stimmhöhe {#SpeechSettingsPitch}

Mit dieser Option können Sie die Stimmhöhe der aktuell ausgewählten Stimme festlegen.
Es ist ein Schieberegler, der von 0 bis 100 reicht (0 ist sehr tief und 100 ist sehr hoch).

##### Lautstärke {#SpeechSettingsVolume}

Diese Option ist ein Schieberegler, der von 0 bis 100 reicht (0 ist sehr leise und 100 ist sehr laut).

##### Betonung {#SpeechSettingsInflection}

Diese Option ist ein Schieberegler, mit dem Sie auswählen können, mit wie viel Flexion (Anstieg und Rückgang der Tonhöhe) Die Sprachausgabe sprechen soll.

##### Sprache automatisch wechseln (falls unterstützt) {#SpeechSettingsLanguageSwitching}

Dieses Kontrollfeld erlaubt Ihnen einzustellen, ob NVDA die Sprache der Sprachausgabe automatisch passend zur angegebenen Dokumentsprache einstellen soll.
Diese Option ist standardmäßig aktiviert.

##### Dialekte automatisch wechseln (falls unterstützt) {#SpeechSettingsDialectSwitching}

Wenn der automatische Sprachenwechsel aktiviert ist, können Sie NVDA mit dieser Option dazu bringen, nicht nur die eigentliche Sprache, sondern auch den Dialekt passend zur Dokumentsprache während des Lesens zu ändern.
Wenn Sie beispielsweise ein amerikanisch-englisches Dokument lesen, in dem Textpassagen als britisch-englisch ausgewiesen sind, wird NVDA automatisch den Dialekt der Sprachausgabe anpassen, sofern diese Option aktiviert ist.
Diese Option ist standardmäßig deaktiviert.

<!-- KC:setting -->

##### Ausführlichkeitsstufe {#SpeechSettingsSymbolLevel}

Tastenkombination: NVDA+P

Hier kann eingestellt werden, ob und wie viele Satz- und Sonderzeichen NVDA als Wort aussprechen soll.
Wenn hier "Alle" ausgewählt ist, spricht NVDA alle Symbole, als wären diese ausgeschrieben.
Diese Option gilt für alle Sprachausgaben, nicht nur für die aktuell ausgewählte.

##### Beim Vorlesen von Symbolen und Sonderzeichen die Sprache der Stimme berücksichtigen {#SpeechSettingsTrust}

Mit dieser standardmäßig aktivierten Option legen Sie fest, ob beim Vorlesen von Symbolen und Sonderzeichen immer die Sprache der momentan eingestellten Stimme berücksichtigt werden soll.
Sollte in NVDA die Aussprache von Symbolen und Sonderzeichen nicht korrekt funktionieren, können Sie diese Option deaktivieren.

##### Unicode-Konsortiumsdaten (einschließlich Emoji) bei der Verarbeitung von Zeichen und Symbolen einbeziehen {#SpeechSettingsCLDR}

Wenn dieses Kontrollkästchen aktiviert ist, wird NVDA bei der Aussprache von Zeichen und Symbolen zusätzliche Wörterbücher für die Aussprache der Symbole einbeziehen.
Diese Wörterbücher enthalten Beschreibungen für Symbole (insbesondere Emoji), die vom [Unicode-Konsortium](https://www.unicode.org/consortium/) als Teil ihres [Common Locale Data Repository](http://cldr.unicode.org/) zur Verfügung gestellt werden.
Wenn Sie möchten, dass NVDA auf Basis dieser Daten Beschreibungen von Emoji-Zeichen vorliest, sollten Sie diese Option aktivieren.
Falls eine Sprachausgabe verwendet wird, die das Vorlesen von Emoji-Beschreibungen nativ unterstützt, können Sie dies abschalten.

Beachten Sie, dass manuell hinzugefügte oder bearbeitete Beschreibungen als Teil Ihrer Benutzereinstellungen gespeichert werden.
Wenn Sie also die Beschreibung eines bestimmten Emoji ändern, wird Ihre benutzerdefinierte Beschreibung für diesen Emoji bevorzugt, unabhängig davon, ob diese Option aktiviert ist.
Sie können die Symbolbeschreibungen in [Interpunktion und Symbol-Aussprache](#SymbolPronunciation) hinzufügen, bearbeiten oder entfernen.

Um die Einbindung von Unicode-Konsortiumsdaten von überall her zu aktivieren, weisen Sie bitte eine Tastenkombination über das Dialogfeld für die [Tastenbefehle](#InputGestures) zu.

##### Stimme bei Großbuchstaben anheben {#SpeechSettingsCapPitchChange}

Dieses Eingabefeld legt fest, wie die Stimme der Ansage bei Großbuchstaben verändert werden soll.
Dieser Wert wird in Prozent angegeben, wobei ein negativer Wert die Stimme senkt und ein positiver Wert die Stimme anhebt.
Um dieses Verhalten auszuschalten, setzen Sie diesen Wert auf 0.
Standardmäßig erhöht NVDA die Stimme für jeden Großbuchstaben leicht, aber einige Synthesizer unterstützen dies möglicherweise nur unzureichend.
Falls die Änderung der Stimme bei der Ansage für Großbuchstaben nicht unterstützt wird, verwenden Sie stattdessen die Optionen "[Bei Großbuchstaben "Groß" ansagen](#SpeechSettingsSayCapBefore)" und/oder "[Signalton bei Großbuchstaben](#SpeechSettingsBeepForCaps)".

##### Bei Großbuchstaben "Groß" ansagen {#SpeechSettingsSayCapBefore}

Dieses Kontrollfeld legt fest, ob beim Navigieren im Text oder beim Schreiben von Großbuchstaben das Wort "Groß" vor Großbuchstaben gesagt werden soll.

##### Signalton bei Großbuchstaben {#SpeechSettingsBeepForCaps}

Wenn dieses Kontrollkästchen aktiviert ist, ertönt jedes Mal ein Signalton bei Großbuchstaben.

##### Buchstabierfunktion verwenden, sofern verfügbar {#SpeechSettingsUseSpelling}

Einige Wörter bestehen aus nur einem einzigen Zeichen. Hierbei unterscheidet sich die Aussprache abhängig davon, ob das Zeichen als Wort oder als einzelnes Zeichen zum Buchstabieren benutzt wird.
Ein Beispiel hierfür ist der Buchstabe "a" im Englischen, der unterschiedlich ausgesprochen wird, je nach dem, ob tatsächlich der Buchstabe "a" oder das Wort "ein/eine" gemeint ist.
Diese Option ermöglicht der Sprachausgabe zwischen diesen beiden Fällen zu unterscheiden, falls dies unterstützt wird.
Die meisten Sprachausgaben unterstützen jedoch dies.

Diese Option sollte im Allgemeinen aktiviert sein.
Es gibt jedoch einige SAPI-Sprachausgaben von Microsoft, bei denen dies nicht korrekt implementiert ist und die sich eigenwillig verhalten, wenn diese Option aktiviert ist.
Wenn Sie Probleme mit der Aussprache mancher Zeichen haben, versuchen Sie, die Option zu deaktivieren.

##### Verzögerte Beschreibungen für Zeichen bei Cursor-Bewegung {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Eingeschaltet, Ausgeschaltet|
|Standard |Ausgeschaltet|

Wenn diese Einstellung aktiviert ist, nennt NVDA die Zeichenbeschreibung, wenn Sie sich zeichenweise bewegen.

Wenn zum Beispiel beim Durchsehen einer Zeile nach Zeichen der Buchstabe "b" vorgelesen wird, nennt NVDA nach einer Verzögerung von einer Sekunde "Bertha".
Dies kann nützlich sein, wenn die Aussprache von Symbolen schwer zu unterscheiden ist, oder auch für hörgeschädigte Benutzer.

Die verzögerte Zeichenbeschreibung wird abgebrochen, wenn während dieser Zeit ein anderer Text vorgelesen wird oder die `Strg`-Taste gedrückt wird.

=== verfügbare Modi im Befehl Sprachmodus wechseln ====[SpeechModesDisabling]
Mit dieser aktivierbaren Liste können Sie festlegen, welche [Sprachmodi](#SpeechModes) enthalten sind, wenn Sie mit NVDA+s zwischen ihnen wechseln.
Nicht aktivierte Modi werden ausgelassen.
Standardmäßig sind alle Modi aktiv.

Wenn Sie beispielsweise die Modi Signaltöne und Aus nicht benötigen, sollten Sie diese beiden deaktivieren und sowohl Sprechen als auch bei Bedarf aktiviert lassen.
Beachten Sie, dass mindestens zwei Modi aktiviert sein müssen.

#### Sprachausgabe auswählen {#SelectSynthesizer}

<!-- KC:setting -->

##### Dialogfeld zum Auswählen der Sprachausgabe öffnen {#toc143}

Tastenkombination: `NVDA+Strg+S`

Das Dialogfeld, welches durch das Betätigen des Schalters "Ändern" geöffnet wird, ermöglicht die Sprachausgabe auszuwählen. Diese wird dann von NVDA dazu genutzt Informationen mittels Sprache zugänglich zu machen.
NVDA wird die Sprachausgabe verwenden, sobald Sie einen Eintrag ausgewählt und den Schalter "OK" betätigt haben.
Wenn ein Fehler auftritt, wird NVDA einen Fehlerton abspielen und die vorherige Sprachausgabe weiterhin verwenden.

##### Sprachausgabe {#SelectSynthesizerSynthesizer}

Diese Option legt fest, welche Sprachausgabe beim Verwenden von NVDA genutzt  werden soll.

Eine Liste aller von NVDA unterstützten Sprachausgaben finden Sie im Abschnitt [Unterstützte Sprachausgaben](#SupportedSpeechSynths).

In der Liste der verfügbaren Sprachausgaben gibt es auch den Eintrag "Keine Sprachausgabe". Damit wird NVDA stumm geschaltet.
Dies ist für Anwender nützlich, die nur mit einer Braillezeile arbeiten möchten. Aber auch Entwickler können davon profitieren, wenn Sie nur den Sprachausgaben-Betrachter für Ihre Tests nutzen möchten.

#### Einstellungsring der Sprachausgabe {#SynthSettingsRing}

Wenn Sie rasch durch die verschiedenen Sprachausgabeneinstellungen schalten möchten, ohne zuvor extra in die Kategorie der NVDA-Einstellungen gehen zu müssen, so gibt es die folgenden Tastenkombinationen in NVDA, die Sie von überall aus benutzen können:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Beschreibung|
|---|---|---|---|
|Zur nächsten Sprachausgabeneinstellung springen |NVDA+Strg+Pfeiltaste nach rechts |NVDA+Strg+Umschalt+Pfeiltaste nach rechts |Springt zur nächsten verfügbaren Sprachausgabeneinstellung ausgehend von der aktuellen Einstellung; beginnt von vorne, nach dem letzten Eintrag.|
|Zur vorherigen Sprachausgabeneinstellung springen |NVDA+Strg+Pfeiltaste nach links |NVDA+Strg+Umschalt+Pfeiltaste nach links |Springt zur vorherigen verfügbaren Sprachausgabeneinstellung ausgehend von der aktuellen Einstellung; beginnt von hinten, nach dem ersten Eintrag.|
|Aktuelle Sprachausgaben-Einstellung erhöhen |NVDA+Strg+Pfeiltaste nach oben |NVDA+Strg+Umschalt+Pfeiltaste nach oben |Erhöht die aktuelle Einstellung (z. B. die Sprechgeschwindigkeit erhöhen, die nächste Stimme auswählen, die Lautstärke erhöhen).|
|Erhöhen der aktuellen Sprachausgaben-Einstellung in größeren Schritten |`NVDA+Strg+Seite nach oben` |`NVDA+Umschalt+Strg+Seite nach oben` |Erhöht den Wert der aktuellen Sprachausgaben-Einstellung, auf der Sie sich befinden, in größeren Schritten, z. B. wenn Sie sich auf einer Stimmen-Einstellung befinden, springt der Wert alle 20 Stimmen vorwärts; wenn Sie sich auf Schieberegler-Einstellungen (Geschwindigkeit, Tonhöhe, etc.) befinden, springt der Wert um bis zu 20 % vorwärts.|
|Aktuelle Sprachausgaben-Einstellung verringern |NVDA+Strg+Pfeiltaste nach unten |NVDA+Strg+Umschalt+Pfeiltaste nach unten |Verringert die aktuelle Einstellung (z. B. die Sprechgeschwindigkeit verringern, wählt die vorherige Stimme aus, verringert die Lautstärke).|
|Verringern der aktuellen Sprachausgaben-Einstellung in größeren Schritten |`NVDA+Strg+Seite nach unten` |`NVDA+Umschalt+Strg+Seite nach unten` |Verringert den Wert der aktuellen Sprachausgaben-Einstellung, auf der Sie sich befinden, in größeren Schritten. Wenn Sie sich z. B. auf einer Stimmen-Einstellung befinden, springt der Wert alle 20 Stimmen rückwärts; wenn Sie sich auf einer Schieberegler-Einstellung befinden, springt der Wert um bis zu 20 % rückwärts.|

<!-- KC:endInclude -->

#### Die Braille-Einstellungen {#BrailleSettings}

Die Kategorie "Braille" in den NVDA-Einstellungen bietet verschiedene Optionen an, um Aspekte der Ein- und -Ausgabe in Braille einzustellen.
Folgende Optionen sind enthalten:

##### Braillezeile ändern {#BrailleSettingsChange}

Mit dem Schalter "Ändern" in den NVDA-Einstellungen in der Kategorie "Braille" wird das Dialogfeld zum [Ändern der Braillezeile](#SelectBrailleDisplay) geöffnet. Dort können Sie die Braillezeile auswählen.
Dieses Dialogfeld wird zusätzlich zu den NVDA-Einstellungen geöffnet.
Wenn das Dialogfeld zum Ändern der Sprachausgabe mit "OK" oder "Abbrechen" geschlossen wird, erscheinen wieder die NVDA-Einstellungen mit den dazugehörigen Kategorien.

##### Ausgabetabelle {#BrailleSettingsOutputTable}

Diese Option ist die Auswahlliste der Braille-Ausgabetabellen.
In diesem Kombinationsfeld finden Sie Brailletabellen für verschiedene Sprachen, Braille-Standards und Kurzschriften.
Die ausgewählte Tabelle wird zur Umwandlung von Text in Braille verwendet, um diesen auf Ihrer Braillezeile darzustellen.
Zwischen den Braille-Tabellen bewegen Sie sich mit den Pfeiltasten.

##### Eingabetabelle {#BrailleSettingsInputTable}

In dieser Option finden Sie das Kombinationsfeld für die Braille-Eingabetabellen.
Bei Verwendung von Braillezeilen mit Braille-Tastatur wird die hier ausgewählte Tabelle zur Umwandlung von Braille nach Text verwendet.
Von Brailletabelle zu Brailletabelle bewegen Sie sich mit den Pfeiltasten.

Diese Option ist nur hilfreich, wenn Sie eine Braillezeile mit Braille-Tastatur verwenden und dieses Feature vom Braillezeilen-Treiber unterstützt wird.
Sollte die Eingabe auf einer Braillezeile mit Braille-Tastatur nicht unterstützt werden, so wird dies im Abschnitt [unterstützte Braillezeilen](#SupportedBrailleDisplays) vermerkt.

<!-- KC:setting -->

##### Braille-Modus {#BrailleMode}

Tastenkombination: `NVDA+Alt+T`

Mit dieser Option können Sie zwischen den verfügbaren Braille-Modi auswählen.

Derzeit werden zwei Braille-Modi unterstützt: "Cursor folgen" und "Sprachausgabenverlauf anzeigen".

Wenn die Option "Cursor folgen" ausgewählt ist, folgt die Braillezeile entweder dem System-Fokus/-Cursor oder dem Navigationsobjekt/NVDA-Cursor, je nachdem, woran die Ausgabe auf der Braillezeile gekoppelt ist.

Wenn die Option "Sprachausgabenverlauf anzeigen" ausgewählt ist, zeigt die Braillezeile an, was NVDA spricht oder gesprochen hätte, wenn der Sprachmodus auf "Sprechen" eingestellt wäre.

##### Aktuelles Wort in Computerbraille ausschreiben {#BrailleSettingsExpandToComputerBraille}

Diese Option legt fest, ob das Wort, welches sich unter dem Cursor befindet, in Computerbraille dargestellt werden soll oder nicht.

##### Cursor anzeigen {#BrailleSettingsShowCursor}

Mit Hilfe dieser Option können Sie die Anzeige des Cursors in Braille ein- und ausschalten.
Dies betrifft den System- und den NVDA-Cursor, nicht jedoch die Kennzeichnung von markiertem Text.

##### Blinkender Cursor {#BrailleSettingsBlinkCursor}

Mit Hilfe dieser Option können Sie das Blinken des Cursors auf der Braillezeile ein- oder ausschalten.
Wenn das Blinken des Cursors deaktiviert ist, wird er ständig angezeigt.
Die Anzeige für Markierungen wird dadurch nicht beeinflusst, Markierungen werden immer durch statische Punkte 7 und 8 angezeigt.

##### Cursor-Blinkgeschwindigkeit {#BrailleSettingsBlinkRate}

Diese Option ist ein numerisches Feld, in dem sich die Cursor-Blinkrate in Millisekunden anpassen lässt.

##### Cursor-Form für Fokus {#BrailleSettingsCursorShapeForFocus}

Hiermit legen Sie das Punktmuster des Cursors fest, welches verwendet werden soll, wenn die Braillezeile an den Fokus gekoppelt wird.
Die Anzeige für Markierungen wird dadurch nicht beeinflusst, Markierungen werden immer durch statische Punkte 7 und 8 dargestellt.

##### Cursor-Form für NVDA-Cursor {#BrailleSettingsCursorShapeForReview}

Hiermit legen Sie das Punktmuster des Cursors fest, welches verwendet werden soll, wenn die Braillezeile an den NVDA-Cursor gekoppelt wird.
Die Anzeige für Markierungen wird dadurch nicht beeinflusst. Markierungen werden immer durch statische Punkte 7 und 8 angezeigt.

##### Meldungen anzeigen {#BrailleSettingsShowMessages}

In diesem Kombinationsfeld können Sie auswählen, ob NVDA Braille-Meldungen auf der Braillezeile anzeigen soll und wann diese automatisch verschwinden sollen.

Um die Anzeige der Meldungen von überall aus einzuschalten, weisen Sie bitte einen benutzerdefinierten Tastenbefehl zu, indem Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden.

##### Anzeigedauer für Meldungen {#BrailleSettingsMessageTimeout}

Dieses numerische Eingabefeld legt fest, wie viele Sekunden die NVDA-Meldungen auf der Braillezeile angezeigt werden sollen. Wenn eine Meldung erscheint, kann diese durch Drücken einer Routing-Taste geschlossen werden. Durch Drücken einer Navigationstaste kann die Anzeigedauer einer Meldung verlängert werden.
Die NVDA-Meldung wird beim Drücken einer Routing-Taste auf der Braillezeile sofort verworfen, erscheint aber wieder, wenn eine entsprechende Taste gedrückt wird, die die Nachricht auslöst.
Diese Option wird nur angezeigt, wenn die Option "Meldungen anzeigen" auf "Zeitüberschreitung verwenden" eingestellt ist.

<!-- KC:setting -->

##### Braillezeile koppeln {#BrailleTether}

Tastenkombination: NVDA+Strg+T

Mit dieser Option können Sie bestimmen, ob die Braillezeile dem System-Fokus / -Cursor, dem Navigator-Objekt / NVDA-Cursor oder beiden folgen soll.
Wenn beiden Navigationsarten gefolgt wird, verfolgt die Braillezeile den Fokus bzw. den System-Cursor, sobald dieser seine Position ändert (z. B. beim Drücken von Tab oder Shift-tab zum Bewegen des Fokus oder beim Drücken der Pfeiltasten zum Bewegen des Cursors in einem Text).
Sobald Sie den Navigator oder die Befehle zum Text betrachten verwenden, wird die Braillezeile automatisch an den NVDA-Cursor gekoppelt, bis sich der Fokus bewegt.
Wenn Sie möchten, dass die Braillezeile nur dem Fokus und dem Cursor folgt, müssen Sie die Braillezeile so konfigurieren, dass sie an den Fokus gekoppelt ist.
In diesem Fall folgt die Braillezeile nicht dem NVDA-Navigator während der Objekt-Navigation oder dem NVDA-Cursor während der Anzeige.
Wenn Sie möchten, dass die Braillezeile stattdessen der Objektnavigation und der Textüberprüfung folgt, müssen Sie die Braillezeile so konfigurieren, dass sie für die Anzeige angekoppelt ist.
In diesem Fall folgt die Braillezeile weder dem System-Fokus, noch dem System-Cursor.

##### Den System-Cursor bei der Weiterleitung des NVDA-Cursors verschieben {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (Niemals), Niemals, Nur bei automatischer Kopplung, Immer|
|Standard |Niemals|

Diese Einstellung legt fest, ob der System-Cursor bei einem Druck auf die Routing-Taste mit verschoben werden soll.
Diese Option ist standardmäßig auf "Niemals" eingestellt, das bedeutet, der Cursor wird bei der Weiterleitung des NVDA-Cursors nicht bewegt.

Wenn diese Option auf Immer eingestellt ist und [Braille-Ausgabe koppeln](#BrailleTether) auf "Automatisch" oder "Zur Ansicht" eingestellt ist, wird durch Drücken einer Cursor-Routing-Taste auch der System-Cursor oder der Fokus bewegt, sofern dies unterstützt wird.
Wenn der aktuelle Darstellungsmodus auf [Bildschirm-Layout](#ScreenReview) eingestellt ist, gibt es keinen physischen Cursor.
In diesem Fall versucht NVDA, das Objekt unter dem Text zu fokussieren, zu dem Sie weitergeleitet werden.
Dasselbe gilt für [Objekt-Darstellungen](#ObjectReview).

Sie können diese Option auch so einstellen, dass die Einfügemarke nur dann bewegt wird, wenn sie automatisch gekoppelt ist.
In diesem Fall führt das Drücken einer Cursor-Routing-Taste nur dann zu einer Verschiebung des System-Cursors oder des Fokus, wenn NVDA automatisch an den NVDA-Cursor gebunden ist, während bei einer manuellen Bindung an den NVDA-Cursor keine Bewegung erfolgt.

Diese Option wird nur angezeigt, wenn "[Braille-Ausgabe koppeln](#BrailleTether)" auf "Automatisch" oder "Zur Ansicht" eingestellt ist.

Um den System-Cursor zu ziehen, wenn Sie den NVDA-Cursor von einer beliebigen Stelle aus weiterleiten, weisen Sie bitte einen benutzerdefinierten Tastenbefehl zu, indem Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden.

##### Absatzweises Vorlesen {#BrailleSettingsReadByParagraph}

Wenn diese Option aktiviert ist, erfolgt die Anzeige in Braille absatzweise statt zeilenweise.
Ebenso bewirken die Tasten zum zeilenweisen Navigieren in diesem Modus eine absatzweise Navigation.
Dies bedeutet, dass Sie die Braillezeile nicht am Ende jeder Zeile weiternavigieren müssen, auch wenn mehr Text auf die Zeile passen würde.
Dies erlaubt Ihnen ein flüssigeres lesen größerer Textmengen.
Diese Option ist standardmäßig deaktiviert.

##### Wortumbruch verhindern (falls möglich) {#BrailleSettingsWordWrap}

Wenn diese Option aktiviert ist, trennt NVDA ein Wort nicht, das für die Darstellung auf der Braillezeile zu lang ist.
Stattdessen bleibt der verbliebene Platz lehr.
Wenn Sie dann auf den nächsten Bereich weiterbewegen, können Sie das Wort im Ganzen lesen.
Dies wird manchmal auch als Wortumbruch bezeichnet.
Bitte beachten Sie: Zu lange Wörter müssen trotzdem getrennt werden, um auf der Braillezeile angezeigt werden zu können.

Wenn diese Option ausgeschaltet ist, zeigt NVDA so viel wie möglich vom Wort an, aber ein Teil kann abgeschnitten sein.
NVDA zeigt dann den Rest des Wortes im nächsten Bereich an.

Das Einschalten dieser Option kann Ihnen ein flüssigeres Lesen ermöglichen, bewirkt aber, dass Sie die Braillezeile öfter weiterschalten müssen.

##### Kontext anzeigen {#BrailleSettingsFocusContextPresentation}

Mit dieser Option können Sie festlegen wann Kontextinformationen angezeigt werden sollen, wenn ein Objekt den Fokus erhält.
Kontextinformationen sind z. B. Informationen über übergeordnete Objekte.
Ein Beispiel: Wenn Sie einen Listeneintrag ansteuern, ist dieser ein Teil einer Liste.
Diese Liste könnte ein Teil eines Dialogs oder ähnliches sein.
Weitere Informationen über die Objekthierarchie finden Sie im Abschnitt über [Objektnavigation](#ObjectNavigation).

Bei der Einstellung "Fülle Zeile bei Kontext-Änderungen" wird die Kontextinformation nur dann angezeigt, wenn sich der Kontext ändert.
Für das obige Beispiel bedeutet das, dass NVDA zunächst so viel Information wie möglich auf der Braillezeile anzeigt, sobald ein Listeneintrag den Fokus erhalten hat.
Sollte noch Platz auf der Braillezeile vorhanden sein, so wird außerdem der Name der Liste angezeigt.
Wenn Sie sich mit den Pfeiltasten durch die Liste bewegen, wird angenommen, dass Sie wissen, dass Sie sich innerhalb einer Liste befinden.
Dies bedeutet, dass nur noch die Listeneinträge auf der Braillezeile angezeigt werden.
Um die Kontext-Informationen anzuzeigen können Sie auf der Braillezeile rückwärts navigieren.

Bei der Einstellung "immer Zeile auffüllen" wird NVDA immer so viel Kontextinformation wie möglich auf der Braillezeile anzeigen, selbst wenn Sie diese Information schon vorher bekommen haben.
Dies hat den Vorteil, dass immer so viel Information wie möglich auf der Braillezeile angezeigt wird.
Andererseits kann es zu einer "springenden Anzeige" kommen, wenn sich die Position des hervorgehobenen Objekts auf der Braillezeile ständig ändert.
Dies kann beim Navigieren durch lange Listen zu Problemen führen, weil Sie mit Ihrem Finger immer wieder den Anfang des Eintrags aufsuchen müssen.
Dies ist das Standardverhalten von NVDA 2017.2 und älter.

Bei der Einstellung "Nur beim Rückwärtsnavigieren" wird NVDA niemals automatisch Kontextinformationen anzeigen.
Für das obige Beispiel bedeutet dies, dass NVDA immer nur den aktuellen Listeneintrag anzeigt.
Wenn Sie dennoch Kontext-Informationen (wie z. B. den Namen der Liste) angezeigt bekommen möchten, müssen Sie auf der Braillezeile rückwärts navigieren.

Um die Einstellung von überall aus zu ändern, weisen Sie eine Tastenkombination mit Hilfe des Dialogs [Tastenbefehle](#InputGestures) zu.

##### Unterbrechen der Sprachausgabe beim Navigieren {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Eingeschaltet, Ausgeschaltet|
|Standard |Eingeschaltet|

Diese Einstellung legt fest, ob die Sprachausgabe unterbrochen werden soll, sobald die Braillezeile vorwärts oder rückwärts gescrollt wird.
Befehle für die vorherige bzw. nächste Zeile unterbricht immer die Sprachausgabe.

Das ständige Vorlesen kann beim Lesen der Braille-Schrift ablenken.
Aus diesem Grund ist die Option standardmäßig aktiviert und unterbricht die Sprachausgabe beim Navigieren auf der Braillezeile.

Wenn Sie diese Option deaktivieren, können Sie die Sprachausgabe hören und gleichzeitig auf der Braillezeile lesen.

##### Auswahl anzeigen {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (eingeschaltet), Eingeschaltet, Ausgeschaltet|
|Standard |Eingeschaltet|

Diese Einstellung legt fest, ob die Auswahlanzeige (Punkte 7 und 8) auf der Braillezeile angezeigt werden.
Die Option ist standardmäßig aktiviert, so dass der Auswahl-Indikator angezeigt wird.
Die Auswahlanzeige kann manchmal beim Lesen auf der braillezeile als störend umpfunden werden.
Das Ausschalten  dieser Option kann eventuell die Lesbarkeit verbessern.

Um die Auswahl von einer beliebigen Stelle aus umzuschalten, weisen Sie bitte einen benutzerdefinierten Tastenbefehl zu, indem Sie das dialogfeld für die [Tastenbefehle](#InputGestures) verwenden.

#### Braillezeile auswählen {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Dialogfeld zum Auswählen der Braillezeile öffnen {#toc167}

Tastenkombination: `NVDA+Strg+A`

Dies ist das Dialogfeld zum Ändern der Braillezeile, welches über den Schalter "Ändern" in der Kategorie "Braille" geöffnet wird. Es ermöglicht die Braillezeile auszuwählen, die NVDA dazu verwendet, Informationen in Punktschrift darzustellen.
NVDA wird die Braillezeile verwenden, sobald Sie einen Eintrag ausgewählt und den Schalter "OK" betätigt haben.
Falls ein Fehler auftritt, wird NVDA einen Fehlerton wiedergeben und die vorherige Braillezeile weiterhin verwenden, sofern vorhanden.

##### Braillezeile {#SelectBrailleDisplayDisplay}

Hier werden Ihnen die zu Verfügung stehenden Auswahlmöglichkeiten aufgelistet, je nachdem, welche Braillezeilen-Treiber auf Ihrem System verfügbar sind.
Jede dieser Braillezeile ist mit den Pfeiltasten zu erreichen.

Die automatische Option ermöglicht NVDA die Suche nach vielen unterstützten Braillezeilen im Hintergrund.
Wenn diese Funktion aktiviert ist und Sie eine unterstützte Braillezeile über USB oder Bluetooth anschließen, verbindet sich NVDA automatisch mit dieser Braillezeile.

Der Eintrag "Keine Braillezeile" bedeutet, dass Sie keine Braillezeile verwenden.

Im Abschnitt [Unterstützte Braillezeilen](#SupportedBrailleDisplays) finden Sie weitere Informationen über unterstützte Braillezeilen und welche davon die automatische Erkennung im Hintergrund unterstützen.

##### Automatische Erkennung von Braillezeilen {#SelectBrailleDisplayAutoDetect}

Wenn die Braillezeile auf "Automatisch" eingestellt ist, können Sie mit den Kontrollkästchen in dieser Liste den Treiber für die Braillezeile aktivieren und deaktivieren, die an der automatischen Erkennung beteiligt sind.
So können Sie die Treiber für Braillezeilen ausschließen, die Sie nicht regelmäßig verwenden.
Wenn Sie z. B. nur einen Bildschirm besitzen, für den der Baum-Treiber erforderlich ist, können Sie den Baum-Treiber aktiviert lassen, während die anderen Treiber deaktiviert werden können.

Alle Treiber, die die automatische Erkennung unterstützen, sind standardmäßig aktiviert.
Jeder neue Treiber, der z. B. in einer zukünftigen NVDA-Version oder in einer NVDA-Erweiterung hinzugefügt wird, wird ebenfalls standardmäßig aktiviert sein.

Sie können in der Dokumentation zu Ihrer Braillezeile im Abschnitt [Unterstützte Braillezeilen](#SupportedBrailleDisplays) nachlesen, ob der Treiber die automatische Erkennung von Braillezeilen unterstützt.

##### Anschluss {#SelectBrailleDisplayPort}

Sofern diese Option verfügbar ist, erlaubt sie Ihnen, den Anschluss auszuwählen, über den die gewählte Braillezeile mit Ihrem Rechner kommunizieren soll.
In diesem Kombinationsfeld werden die möglichen Anschlüsse angezeigt.

Standardmäßig wird NVDA automatisch sämtliche USB-Anschlüsse und Bluetooth-Geräte nach Ihrer Braillezeile absuchen.
Für manche Braillezeilen können Sie jedoch genau festlegen, wie die Zeile angeschlossen ist.
Übliche Auswahlmöglichkeiten sind "automatisch" (die oben beschriebene automatische Suche nach dem Anschluss), "Bluetooth" "USB" oder einer der seriellen Anschlüsse, sofern Ihre Braillezeile diese Verbindungsart unterstützt.

Diese Option ist nicht verfügbar, wenn Ihre Braillezeile nur die automatische Suche nach dem Anschluss unterstützt.

Für weitere Informationen sehen Sie im Abschnitt [Unterstützte Braillezeilen](#SupportedBrailleDisplays), welche Anschlüsse für Ihre Braillezeile zur Verfügung stehen.

Bitte beachten Sie: Wenn Sie mehrere Braillezeilen gleichzeitig an Ihr Gerät anschließen,
die denselben Treiber verwenden (z. B. zwei Seika-Braillezeilen anschließen), ist es derzeit nicht möglich, NVDA mitzuteilen, welche Braillezeile verwendet werden soll.
Es wird daher empfohlen, immer nur eine Braillezeile eines bestimmten Typs / Herstellers an Ihr Gerät anzuschließen.

#### Audio-Einstellungen {#AudioSettings}

<!-- KC:setting -->

##### Audio-Einstellungen öffnen {#toc172}

Tastenkombination: `NVDA+Strg+U`

Die Kategorie "Audio-Einstellungen" in den NVDA-Einstellungen enthält Optionen, mit denen Sie verschiedene Aspekte der Audio-Ausgabe anpassen können.

##### Audio-Ausgabegerät {#SelectSynthesizerOutputDevice}

Mit dieser Option können Sie das Audio-Ausgabegerät auswählen, über welches NVDA die ausgewählte Sprachausgabe verwenden soll.

<!-- KC:setting -->

##### Verringern anderer Audio-Quellen {#SelectSynthesizerDuckingMode}

Tastenkombination: `NVDA+Umschalt+D`

Mit dieser Option legen Sie fest, ob NVDA bei Verwendung der Sprachausgabe die Lautstärke anderer Anwendungen verringern soll oder ständig während NVDA läuft.

* Niemals: NVDA verringert die Lautstärke anderer Audio-Quellen nicht.
* Nur beim Vorlesen und bei Sounds: NVDA verringert die Lautstärke anderer Audio-Quellen nur bei Verwendung der Sprachausgabe oder sofern NVDA-Sounds wiedergegeben werden. Dies funktioniert möglicherweise nicht mit allen Sprachausgaben.
* Immer: NVDA hält die Lautstärke anderer Audio-Quellen während der gesamten Laufzeit von NVDA niedrig.

Diese Option ist nur verfügbar, sofern NVDA installiert wurde.
Die Unterstützung zum Umschalten der Audio-Quellen für portable und temporäre NVDA-Versionen ist nicht möglich.

##### Lautstärke der NVDA-Sounds folgt der Lautstärke der verwendeten Stimme {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Ausgeschaltet, Eingeschaltet|
|Standard |Ausgeschaltet|

Wenn diese Option aktiviert ist, folgt die Lautstärke der NVDA-Sounds und -Signaltöne der Lautstärke-Einstellung der verwendeten Stimme.
Wenn Sie die Lautstärke der Stimme verringern, nimmt auch die Lautstärke der Sounds ab.
Ähnlich verhält es sich, wenn Sie die Lautstärke der Stimme erhöhen, wird auch die Lautstärke der Sounds zunehmen.
Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audio-Ausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

##### Lautstärke der NVDA-Sounds {#SoundVolume}

Mit diesem Schieberegler können Sie die Lautstärke der NVDA-Sounds und -Signaltöne einstellen.
Diese Einstellung ist nur wirksam, sofern die "Lautstärke der NVDA-Sounds folgt der Lautstärke der verwendeten Stimme" deaktiviert ist.
Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audio-Ausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

##### Zeit, um das Audio-Gerät nach dem Sprechen nicht auszublenden {#AudioAwakeTime}

Dieses Eingabefeld legt fest, wie lange NVDA das Audio-Gerät nach Beendigung des Sprechens nicht ausblenden soll.
Dadurch kann NVDA bestimmte Sprachfehler wie ausgelassene Wortteile vermeiden.
Dies kann passieren, wenn Audio-Geräte (insbesondere Bluetooth- und drahtlose Geräte) in den Standby-Modus wechseln.
Dies kann auch in anderen Anwendungsfällen hilfreich sein, z. B. bei der Ausführung von NVDA innerhalb einer virtuellen Maschine (z. B. Citrix Virtual Desktop) oder auf bestimmten Laptops.

Bei niedrigeren Werten kann es vorkommen, dass der Ton oder Wortsilben häufiger abgeschnitten wird, da ein Gerät möglicherweise zu früh in den Standby-Modus wechselt, wodurch der Sprechvorgang ausgeblendet wird.
Ein zu hoher Wert kann dazu führen, dass sich die Batterie eines externen Audio-Geräts (z. B. Kopfhörer) schneller entlädt, da sie länger aktiv bleibt, während kein Ton gesendet wird.

Sie können die Zeitspanne auf 0 setzen, um diese Funktion zu deaktivieren.

##### Sound-Teilung {#SelectSoundSplitMode}

Mit der Sound-Teilung können die Benutzer ihre Stereo-Ausgabegeräte wie Kopfhörer und Lautsprecher nutzen.
Damit können Sie die Sprachausgabe in NVDA auf einen Kanal (z. B. links) und alle anderen Anwendungen auf dem anderen Kanal (z. B. rechts) hören.
Standardmäßig ist die Sound-Teilung deaktiviert, was bedeutet, dass alle Anwendungen, einschließlich NVDA, Töne sowohl im linken als auch im rechten Kanal zu hören sind.
Mit einem Tastenbefehl können Sie zwischen den verschiedenen Modi wechseln:
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Zwischen den Modi für die Sound-Teilung wechseln| `NVDA+Alt+S` |Wechselt zwischen den Modi für die Sound-Teilung.|

<!-- KC:endInclude -->

In der Standard-Einstellung wechselt dieser Befehl zwischen den folgenden Modi:

* Deaktivierte Sound-Teilung: Sowohl NVDA als auch andere Anwendungen sind auf beiden Kanälen zu hören.
* NVDA links und Anwendungen rechts: NVDA spricht im linken Kanal, während andere Anwendungen im rechten Kanal zu hören sind.
* NVDA rechts und Anwendungen links: NVDA spricht im rechten Kanal, während andere Anwendungen im linken Kanal zu hören sind.

In der Einstellungskombination in NVDA sind weitere erweiterte Modi für die Sound-Teilung verfügbar.
Wenn Sie die Lautstärke aller Anwendungen mit Ausnahme von NVDA anpassen möchten, sollten Sie [den speziellen Befehl](#OtherAppVolume) verwenden.
Bitte beachten Sie, dass die Sound-Teilung nicht als Mixer funktioniert.
Wenn beispielsweise eine Anwendung eine Stereo-Tonspur abspielt und die Sound-Teilung auf "NVDA links und Anwendungen rechts" eingestellt ist, dann hören Sie nur den rechten Kanal der Tonspur, während der linke Kanal der Tonspur stummgeschaltet wird.

Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audioausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

Bitte beachten Sie, dass bei einem Absturz von NVDA die Lautstärke der Anwendungstöne nicht wiederhergestellt werden kann und dass diese Anwendungen nach dem Absturz von NVDA den Sound möglicherweise nur noch auf einem Kanal ausgegeben werden.
Um dieses Problem zu beheben, starten Sie bitte NVDA neu.

##### Anpassen der Sound-Teilung {#CustomizeSoundSplitModes}

Über diese Liste können Sie auswählen, welche Sound-Split-Modi enthalten sind, wenn Sie mit `NVDA+Alt+S` zwischen diesen Modi wechseln.
Modi, die nicht markiert sind, sind ausgenommen.
Standardmäßig sind nur drei Modi enthalten.

* Sound-Teilung deaktiviert: Sowohl NVDA als auch Anwendungen sind auf beiden kanälen zu hören.
* NVDA auf dem linken Kanal und alle anderen Anwendungen auf dem rechten Kanal.
* NVDA auf dem rechten Kanal und alle anderen Anwendungen auf dem linken Kanal.

Es ist zu beachten, dass mindestens ein Modus zu prüfen ist.
Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audio-Ausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

##### Lautstärke der sonstigen Anwendungen einstellen {#OtherAppVolume}

Mit diesem Schieberegler können Sie die Lautstärke aller derzeit ausgeführten Anwendungen außer NVDA einstellen.
Diese Lautstärke-Einstellung gilt für alle weiteren Anwendungen, auch wenn sie nach der Änderung dieser Einstellung gestartet werden.
Diese Lautstärke kann auch über die folgenden Tastaturbefehle von überall aus gesteuert werden:

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Erhöhung der Lautstärke der Anwendung |`NVDA+Alt+Seite nach oben` |Erhöht die Lautstärke aller Anwendungen außer NVDA.|
|Verringerung der Lautstärke der Anwendung |`NVDA+Alt+Seite nach unten` |Verringert die Lautstärke aller Anwendungen außer NVDA.|

<!-- KC:endInclude -->

Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audio-Ausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

##### Sonstige Anwendungen stummschalten {#MuteApplications}

Mit diesem Kontrollkästchen können Sie alle anderen Anwendungen außer NVDA stummschalten.
Diese Stummschaltung gilt für alle anderen Anwendungen, die Sounds ausgeben, auch wenn sie nach der Änderung dieser Einstellung gestartet werden.
Der folgende Tastaturbefehl kann auch von überall aus verwendet werden:

<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Sonstige Anwendungen stummschalten |`NVDA+Alt+Entf` |Schaltet alle Anwendungen außer NVDA stumm bzw. deaktiviert sie.|

<!-- KC:endInclude -->

Diese Option ist nicht verfügbar, wenn Sie NVDA mit [WASAPI deaktiviert für Audio-Ausgabe](#WASAPI) in den Erweiterten Einstellungen gestartet haben.

#### Visuelle Darstellungen {#VisionSettings}

Mit der Kategorie "Visuelle Darstellungen" in den NVDA-Einstellungen können Sie[visuelle Verbesserungen](#Vision) aktivieren, deaktivieren und konfigurieren.

Beachten Sie, dass die verfügbaren Optionen in dieser Kategorie durch [NVDA-Erweiterungen](#AddonsManager) erweitert werden können.
Standardmäßig enthält diese Einstellungskathegorie die folgenden Optionen:

##### Visuell hervorheben {#VisionSettingsFocusHighlight}

Die Kontrollkästchen in der Gruppierung "Visuell hervorheben" steuern das Verhalten der in NVDA integrierten Funktion [Visuell hervorheben](#VisionFocusHighlight).

* Hervorhebung aktivieren: Schaltet die visuelle Hervorhebung ein und aus.
* System-Fokus hervorheben: Schaltet um, ob der [System-Fokus](#Systemfokus) hervorgehoben wird.
* Hervorheben des Navigator-Objekts: Schaltet um, ob das [Navigator-Objekt](#ObjectNavigation) hervorgehoben wird.
* Cursor im Lesemodus hervorheben: Schaltet um, ob der [virtuelle Cursor im Lesemodus](#BrowseMode) hervorgehoben wird.

Beachten Sie, dass das Aktivieren und Deaktivieren des Kontrollkästchens "Hervorhebung aktivieren" auch den Zustand der 3 anderen Kontrollkästchen entsprechend ändert.
Wenn also "Hervorhebung aktivieren" ausgeschaltet ist und Sie dieses Kontrollkästchen aktivieren, werden auch die 3 anderen Kontrollkästchen automatisch aktiviert.
Wenn Sie nur den Fokus hervorheben und die Kontrollkästchen Navigatorobjekt und Lesemodus nicht aktivieren möchten, wechselt der Status des Kontrollkästchens "Hervorhebung aktivieren" zum "teilweise aktiviert".

##### Bildschirmvorhang {#VisionSettingsScreenCurtain}

Sie können den [Bildschirmvorhang](#VisionScreenCurtain) aktivieren, indem Sie das Kontrollkästchen "Bildschirm verdunkeln (sofort wirksam)" aktivieren.
Es wird eine Warnung angezeigt, wonach Ihr Bildschirm nach der Aktivierung sich verdunkelt.
Bevor Sie fortfahren (Auswahl von "Ja"), stellen Sie sicher, dass Sie eine Sprachausgabe oder eine Braillezeile verwenden und den Computer ohne Verwendung des Bildschirms steuern können.
Wählen Sie "Nein", wenn Sie den Bildschirmvorhang nicht mehr aktivieren möchten.
Wenn Sie sicher sind, können Sie die Schaltfläche "Ja" auswählen, um den Bildschirmvorhang zu aktivieren.
Wenn Sie diese Warnmeldung nicht länger erhalten möchten, können Sie dieses Verhalten in dem Dialogfeld, der die Meldung anzeigt, ändern.
Sie können die Warnung jederzeit zurücksetzen, indem Sie das Kontrollkästchen "Beim Laden des Bildschirmvorhangs immer eine Warnung anzeigen" unter dem Kontrollkästchen "Bildschirm verdunkeln" aktivieren.

Standardmäßig ist auch ein Sound beim Umschalten des Bildschirmvorhangs zu hören.
Wenn Sie dieses Verhalten ändern möchten, können Sie das Kontrollkästchen "Sound beim Umschalten des Bildschirmvorhangs" deaktivieren.

##### Einstellungen für visuelle Hilfsmittel von Drittanbietern (Verbesserungen visueller Darstellungen) {#VisionSettingsThirdPartyVisualAids}

Zusätzliche Quellen für die Verbesserung der visuellen Darstellungen können mittels [NVDA-Erweiterungen](#AddonsManager) von Drittanbietern bereitgestellt werden.
Wenn diese Quellen über konfigurierbare Einstellungen verfügen, werden sie in dieser Einstellungskategorie in separaten Gruppierungen angezeigt.
Die unterstützten Einstellungen pro Quelle finden Sie in der Dokumentation der jeweiligen Erweiterung.

#### Tastatur-Einstellungen {#KeyboardSettings}

<!-- KC:setting -->

##### Tastatur-Einstellungen öffnen {#toc187}

Tastenkombination: `NVDA+Strg+K`

Die Kategorie "Tastatur" im Dialogfeld NVDA-Einstellungen enthält Optionen, die das Verhalten von NVDA bei der Verwendung und Eingabe auf Ihrer Tastatur festlegen.
Sie enthält die folgenden Optionen:

##### Tastaturschema {#KeyboardSettingsLayout}

In dieser Liste können Sie zwischen dem Schema "Desktop" oder "Laptop" auswählen.

##### NVDA-Tasten auswählen {#KeyboardSettingsModifiers}

Die Kontrollkästchen in dieser Liste legen fest, welche Tasten als [NVDA-Tasten](#TheNVDAModifierKey) verwendet werden können. Die folgenden Tasten stehen zur Auswahl:

* Die Dauergroßschreibtaste
* Die Einfüge-Taste des Nummernblocks
* Die erweiterte Einfüge-Taste (meistens über den Pfeiltasten, nah bei Pos1 und Ende)

Wenn keine Taste als NVDA-Taste festgelegt wird, kann es sein, dass auf viele NVDA-Befehle nicht mehr zugegriffen werden kann. Daher müssen Sie mindestens eine der Modifikatoren festlegen.

<!-- KC:setting -->

##### Eingegebene Zeichen ansagen {#KeyboardSettingsSpeakTypedCharacters}

Tastenkombination: NVDA+2

Wenn dieses Kontrollfeld aktiviert ist, gibt NVDA jedes Zeichen wieder, dass Sie auf der Tastatur eingegeben haben.

<!-- KC:setting -->

##### Eingegebene Wörter ansagen {#KeyboardSettingsSpeakTypedWords}

Tastenkombination: NVDA+3

Wenn dieses Kontrollfeld aktiviert ist, gibt NVDA jedes Wort wieder, dass Sie auf der Tastatur eingegeben haben.

##### Sprachausgabe während der Eingabe unterbrechen {#KeyboardSettingsSpeechInteruptForCharacters}

Wenn diese Option aktiviert ist, wird die Sprache jedes Mal unterbrochen, wenn Sie ein Zeichen eingeben. Diese Option ist standardmäßig aktiviert.

##### Sprachausgabe beim Drücken der Eingabetaste unterbrechen {#KeyboardSettingsSpeechInteruptForEnter}

Ist diese Option aktiviert, so wird die Sprache jedes Mal unterbrochen, wenn Sie die Eingabetaste drücken. Diese Option ist standardmäßig aktiviert.

##### Navigation während "Alles Lesen" erlauben {#KeyboardSettingsSkimReading}

Wenn diese Option aktiviert ist, Unterbrechen Navigationsbefehle nun nicht mehr den Lesevorgang beim Lesen eines Dokuments mit NVDA+Pfeil Ab. Hierzu gehören sowohl die Schnellnavigationstasten als auch die Befehle zum Navigieren zwischen Zeilen und Absätzen. Diese Option ist standardmäßig deaktiviert.

##### Signaltöne während der Eingabe von Kleinbuchstaben bei aktivierter Dauergroßschreibung aktiviert ist {#KeyboardSettingsBeepLowercase}

Wenn aktiviert, hören Sie einen Warnton, wenn Sie einen Buchstaben mit der Umschalttaste drücken, während die Dauergroßschreibung eingeschaltet ist.
Es ist generell nicht gebräuchlich, Buchstaben mittels der Umschalttaste groß zu schreiben, während die Dauergroßschreibung aktiviert ist und geschieht meistens nur deshalb, weil man nicht erkennt, dass die Dauergroßschreibung aktiv ist.
Somit kann es hilfreich sein, wenn man diesbezüglich gewarnt wird.

<!-- KC:setting -->

##### Funktionstasten ansagen {#KeyboardSettingsSpeakCommandKeys}

Tastenkombination: NVDA+4

Wenn dieses Kontrollfeld aktiviert ist, gibt NVDA alle Tasten wieder, die nicht mit einem Zeichen belegt sind. Das können Tastenkombinationen wie z. B. "Strg+Buchstabe" sein.

##### Sound während der Eingabe bei Rechtschreibfehlern {#KeyboardSettingsAlertForSpellingErrors}

Wenn diese Option aktiviert ist, wird ein kurzer Brummton abgespielt, wenn während der Eingebe Rechtschreibfehler auftreten.
Diese Option funktioniert nur, wenn in den NVDA-Einstellungen in der [Kategorie "Dokumentformatierungen"](#DocumentFormattingSettings) die Anzeige bei Rechtschreibfehlern aktiviert ist.

##### Tastendrücke anderer Anwendungen verarbeiten {#KeyboardSettingsHandleKeys}

Mit dieser Option legen Sie fest, ob per Software emulierte Tastendrücke von NVDA verarbeitet werden sollen. Hierzu zählen beispielsweise Tastendrücke auf einer Bildschirmtastatur oder per Spracherkennung erkannte Zeichen.
Diese Option ist standardmäßig aktiviert, obwohl manche Benutzer dies bestimmt deaktivieren, z. B. diejenigen, die Vietnamesisch mit der UniKey-Software schreiben, da dies zu einer falschen Zeicheneingabe führt.

#### Maus-Einstellungen {#MouseSettings}

<!-- KC:setting -->

##### Maus-einstellungen öffnen {#toc200}

Tastenkombination: `NVDA+Strg+M`

Die Kategorie "Maus" in den NVDA-Einstellungen bietet Optionen zur Mausverfolgung, zu akustischer Koordinatenanzeige, etc.
Folgende Optionen sind enthalten:

##### Änderungen der Mauszeigerform ansagen {#MouseSettingsShape}

Dieses Kontrollfeld legt fest, ob NVDA bei Änderung des Mauszeigers die Form mit ansagen soll.
In Windows ändert sich die Form des Mauszeigers, wenn sich dieser Beispielsweise in einem Eingabefeld befindet, oder wenn etwas geladen wird.

<!-- KC:setting -->

##### Maus-Verfolgung einschalten {#MouseSettingsTracking}

Tastenkombination: NVDA+M

Dieses Kontrollfeld weist NVDA an, den Text unter dem Mauszeiger vorzulesen. Das erleichtert Ihnen das Auffinden von Informationen am Bildschirm, wenn Sie mittels der Maus den Mauszeiger über den Bildschirm bewegen.

##### Auflösung der Texteinheit {#MouseSettingsTextUnit}

Wenn die vorherige Option aktiviert ist, können Sie festlegen, wieviel Text angesagt wird, während Sie die Maus bewegen.
Sie können dabei zwischen Zeichen, Wörter, Zeile oder Absätze auswählen.

Um die Auflösung der Texteinheiten von überall her umzuschalten, weisen Sie bitte eine Tastenkombination über das Dialogfeld für die [Tastenbefehle](#InputGestures) zu.

##### Objekt melden, sobald die Maus hineinbewegt wird {#MouseSettingsRole}

Wenn dieses Kontrollkästchen aktiviert ist, gibt NVDA Informationen zu Objekten aus, wenn sich die Maus darin bewegt.
Dazu gehören die Rolle (Typ) des Objekts sowie Zustände (aktiviert/gedrückt), Zellkoordinaten in Tabellen, etc.
Beachten Sie, dass die Ausgabe einiger Objektdetails möglicherweise davon abhängt, wie andere Einstellungen festgelegt sind, z. B. in den Kategorien [Objektpräsentation](#ObjectPresentationSettings) oder [Dokumentformatierung](#DocumentFormattingSettings).

##### Audio-Koordinaten bei Maus-Bewegungen {#MouseSettingsAudio}

Das Aktivieren dieser Option bewirkt, dass NVDA die Position des Mauszeigers durch Signaltöne an Ort und Stelle wiedergibt, sodass der Anwender die Mausposition auf dem Bildschirm akustisch mitverfolgen und selbst ermitteln kann.
Je näher sich der Mauszeiger am oberen Bildschirmrand befindet, desto höher ist der Signalton.
Richtig ausgerichtete Stereolautsprecher oder Kopfhörer vorausgesetzt, wird der Signalton umso mehr links oder rechts abgespielt, je weiter links oder rechts sich der Mauszeiger bewegt.

##### Lautstärke der Audio-Koordinaten durch Helligkeit kontrollieren {#MouseSettingsBrightness}

Wenn die Option "Audio-Koordinaten bei Maus-Bewegungen" und diese Option aktiviert sind, passt NVDA die Lautstärke der Signaltöne an die Helligkeit unter dem Mauszeiger an.
Diese Option ist standardmäßig deaktiviert.

##### Maus-Eingaben anderer Anwendungen ignorieren {#MouseSettingsHandleMouseControl}

Diese Option ermöglicht es dem Benutzer, Mausereignisse (einschließlich Mausbewegungen und Tastendrucke) zu ignorieren, die von anderen Anwendungen wie TeamViewer und anderen Fernsteuerungssoftware erzeugt werden.
Diese Option ist standardmäßig deaktiviert.
Wenn Sie diese Option aktivieren und die Option "Mausverfolgung aktivieren" aktiviert haben, wird NVDA nicht bekannt geben, was sich unter der Maus befindet, wenn die Maus von einer anderen Anwendung bewegt wird.

#### Touch-Interaktion {#TouchInteraction}

Diese Kategorie ist nur auf Computern verfügbar, sofern diese ein Touchscreen besitzen. Hier können Sie einstellen, wie NVDA damit interagiert.
Folgende Optionen sind enthalten:

##### Unterstützung der Touchscreen-Bedienung aktivieren {#TouchSupportEnable}

Dieses Kontrollkästchen aktiviert die NVDA-Unterstützung für die Touchscreen-Bedienung.
Wenn diese Funktion aktiviert ist, können Sie mit Ihren Fingern auf einem Touchscreen navigieren und mit den Elementen auf dem Bildschirm interagieren.
Anderenfalls wird diese Unterstützung deaktiviert.
Diese Einstellung kann auch mit NVDA+Strg+Alt+T umgeschaltet werden.

##### Touch-Tippmodus {#TouchTypingMode}

Dieses Kontrollkästchen legt die Methode fest, die Sie zum Schreiben mit der Bildschirmtastatur verwenden.
Bei aktiviertem Kontrollkästchen können Sie mit Ihrem Finger eine Taste auf dem Bildschirm suchen und diese loslassen, um diese zu betätigen (10-Finger-System).
Bei deaktivierter Option müssen Sie auf der Taste Doppeltippen, um diese zu drücken (Zwei-Finger-System).

#### NVDA-Cursor {#ReviewCursorSettings}

Diese Kategorie beeinflusst das Verhalten des NVDA-Cursors.
Folgende Optionen sind enthalten:

<!-- KC:setting -->

##### System-Fokus verfolgen {#ReviewCursorFollowFocus}

Tastenkombination: NVDA+7

Wenn eingeschaltet, platziert sich der NVDA-Cursor immer auf dem Objekt, das den Fokus besitzt, sobald sich der Fokus ändert.

<!-- KC:setting -->

##### System-Cursor verfolgen {#ReviewCursorFollowCaret}

Tastenkombination: NVDA+6

Bei eingeschalteter Option wird automatisch bei Bewegung der NVDA-Cursor zur Position des System-Cursors gezogen.

##### Mauszeiger verfolgen {#ReviewCursorFollowMouse}

Wenn eingeschaltet, verfolgt der NVDA-Cursor bei Bewegungen die Maus.

##### Einfacher Darstellungsmodus {#ReviewCursorSimple}

Bei eingeschaltetem Modus filtert NVDA nicht wichtige Objekte aus der Hierarchie der navigierbaren Objekte heraus. Dabei werden z. B. unsichtbare Objekte und Objekte, welche nur zu Gestaltungszwecken eingebaut wurden, übersprungen.

Um den einfachen Darstellungsmodus per Tastenkombination ein- und auszuschalten, können Sie den entsprechenden Befehl an eine Tastenkombination zuweisen. Verwenden Sie hierfür das Dialogfeld [Tastenbefehle](#InputGestures).

#### Einstellungen zur Objekt-Darstellung {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Einstellungen zur Objekt-Darstellung öffnen {#toc217}

Tastenkombination: `NVDA+Strg+O`

Hier kann eingestellt werden, inwieweit NVDA über Position, Beschreibungen von Objekten, etc. informieren soll.
Diese Optionen gelten normalerweise nicht für den Lesemodus.
Diese Optionen gelten normalerweise für die Ansage des Fokus und Objekt-Navigation in NVDA, jedoch nicht für das Lesen von Textinhalten, z. B. im Lesemodus.

##### QuickInfos mitteilen {#ObjectPresentationReportToolTips}

Wenn dieses Kontrollkästchen aktiviert ist, teilt NVDA die QuickInfos mit, sobald sie erscheinen.
Viele Windows- und Steuerelemente zeigen eine kleine Meldung an, wenn Sie den Mauszeiger über das Element oder Objekt bewegen, oder manchmal, wenn Sie den Fokus darauf verschieben.

##### Benachrichtigungen mitteilen {#ObjectPresentationReportNotifications}

Wenn dieses Kontrollfeld aktiviert ist, teilt NVDA die Hilfesprechblasen und Toast-Benachrichtigungen mit, sobald diese erscheinen.

* Hilfesprechblasen sind wie QuickInfos, sind aber in der Regel größer und werden mit System-Ereignissen in Verbindung gebracht, wie z. B. dem Trennen eines Netzwerkkabels oder um über Windows-Sicherheitsprobleme zu informieren.
* Toast-Benachrichtigungen wurden in Windows 10 eingeführt und erscheinen im Benachrichtigungs-Center in der Taskleiste, um über mehrere Ereignisse zu informieren (wenn z. B. ein Update heruntergeladen wurde, eine neue E-Mail in Ihrem Posteingang eintrifft, etc.)

##### Kurztasten der Objekte ausgeben {#ObjectPresentationShortcutKeys}

NVDA nennt zu den Einträgen eines Menüs oder Steuerelements zusätzlich die Kurztaste, sofern die Ansage dieser Option auch aktiviert ist.
Zum Beispiel kann das Datei-Menü in einer Menüleiste die Kurztaste "Alt+D" haben.

##### Informationen zur Objektposition ausgeben {#ObjectPresentationPositionInfo}

Diese Option legt fest, ob Sie die Objektposition (z. B. 1 von 4) angesagt bekommen möchten, wenn Sie mit dem Fokus oder der Objektnavigation darauf navigieren.

##### Informationen zur Objektposition bei Nichtverfügbarkeit ermitteln {#ObjectPresentationGuessPositionInfo}

Wenn die Ausgabe der Informationen zur Objektposition aktiviert ist, wird NVDA die Informationen zur Objektposition für bestimmte Steuerelemente ermitteln, falls diese nicht anderweitig verfügbar ist.

Wenn diese aktiviert ist, meldet NVDA Positionsinformationen für weitere Steuerelemente, wie Menüs und Symbolleisten, jedoch können diese Informationen etwas ungenau sein.

##### Objektbeschreibungen ansagen {#ObjectPresentationReportDescriptions}

Deaktivieren Sie dieses Kontrollkästchen, wenn Sie nicht wünschen, dass die Beschreibungen zusammen mit Objekten gemeldet werden sollen (wie z. B. Suchvorschläge, Bericht über das gesamte Dialogfenster direkt nach dem Öffnen des Dialogs, etc.).

<!-- KC:setting -->

##### Ausgabe des Fortschrittsbalkens {#ObjectPresentationProgressBarOutput}

Tastenkombination: NVDA+U

Diese Option kontrolliert, wie NVDA die Aktualisierungen der Fortschrittsbalken ansagen soll.

Die folgenden Optionen stehen zur Auswahl:

* Aus: Bei Änderungen werden keine Fortschrittsmeldungen angesagt.
* Nur Ansage: Diese Option sagt den Fortschritt in Prozent an. Sobald sich der Fortschrittsbalken ändert, sagt NVDA den neuen Wert an.
* Nur Signaltöne: Bei dieser Option ertönt jedes Mal ein Signalton bei einer Änderung. Umso höher der Ton ist, desto näher ist er am Ziel.
* Ansage und Signaltöne: Bei dieser Option ertönt in NVDA beides; der Fortschritt wird mit einem Signalton und gleichzeitig mit der Sprache quittiert.

##### Im Hintergrund befindliche Fortschrittsbalken ausgeben {#ObjectPresentationReportBackgroundProgressBars}

Wenn dieses Kontrollfeld aktiviert ist, hält NVDA Sie über den Fortgang der Aktionen der minimierten Anwendungen trotzdem auf dem Laufenden.
Wenn Sie ein Fenster, welches einen Fortschrittsbalken enthält, minimieren oder zu einer anderen Anwendung wechseln, wird NVDA den Fortschrittsbalken weiterhin verfolgen. Dies erlaubt Ihnen anderes zu tun, während NVDA den Fortschrittsbalken weiterhin ausgibt.

<!-- KC:setting -->

##### Änderungen dynamischer Inhalte ansagen {#ObjectPresentationReportDynamicContent}

Tastenkombination: NVDA+5

Schaltet die Ansage von neuen Inhalten in bestimmten Programmen wie Terminals und Chat-Programme ein oder aus.

##### Sound bei automatischen Vorschlägen {#ObjectPresentationSuggestionSounds}

Wenn diese Option aktiviert ist, spielt NVDA einen Klang ab, wenn eine Vorschlagsliste erscheint bzw. ausgeblendet wird.
Vorschlagslisten sind Listen mit vorgeschlagenen Einträgen basierend auf Text, den Sie in bestimmte Eingabefelder oder Dokumente eingeben.
Ein Beispiel für ein solches Eingabefeld ist das Suchfeld im Startmenü in Windows. Wenn Sie dort einen Suchbegriff eingeben, zeigt Ihnen Windows eine Liste mit Suchvorschlägen, die auf Ihrem Suchbegriff basieren.
Weitere Beispiele für Eingabefelder mit Vorschlagslisten sind Suchfelder in diversen Windows-Anwendungen.
Die Vorschlagsliste wird geschlossen, sobald Sie mit dem Fokus das Eingabefeld verlassen. NVDA kann Sie manchmal darüber informieren, sobald dies geschieht.

#### Eingabemethoden {#InputCompositionSettings}

Mit den Optionen aus dieser Kategorie können Sie steuern, wie NVDA die Eingabe von Zeichen asiatischer sprachen wiedergibt. dies betrifft sowohl IME als auch die Textdienste.
Hinweis: Eingabemethoden variieren sehr in der Verfügbarkeit von Funktionen sowie in der Informationsweitergabe. Somit müssen diese Optionen für die jeweils verwendete Eingabemethode festgelegt werden, um die bestmögliche Effizienz beim Tippen zu erhalten.

##### Verfügbare Zeichensätze automatisch anzeigen {#InputCompositionReportAllCandidates}

Diese Option, die standardmäßig aktiviert ist, legt fest, ob automatisch eine Liste aller sichtbaren Zeichensätze wiedergegeben werden.
Das Aktivieren dieser Option ist z. B. für die Eingabe piktografischer Zeichen wie ChangJie oder Boshiami sinnvoll, weil Sie ein Zeichen nebst seiner zugehörigen Nummer angezeigt bekommen.
Bei phonetischen Eingabemethoden ist es jedoch sinnvoll, die Option abzuschalten, weil Sie das passende Zeichen ohnehin mit den Pfeiltasten auswählen müssen, um es einzufügen.

##### Ausgewählten Schriftsatz angeben {#InputCompositionAnnounceSelectedCandidate}

Diese Option weist NVDA an, den ausgewählten Schriftsatz auszugeben, sobald die Liste der Zeichensätze erscheint oder wenn Sie einen Schriftsatz auswählen.
Für Eingabemethoden, bei denen Sie die Auswahl mit den Pfeiltasten ändern können (wie z. B. Chinese New Phonetic) ist das Aktivieren dieser Option notwendig, bei anderen Eingabemethoden kann es jedoch effektiver sein, diese Option abzuschalten.
Auch wenn Sie diese Option deaktiviert haben, wird der NVDA-Cursor auf den ausgewählten Schriftsatz gesetzt, sodass Sie den Navigator oder die Befehle zum Betrachten von Text benutzen können, um diesen oder andere Schriftsätze zu lesen.

##### Bei Angabe der Schriftsätze immer kurze Zeichenbeschreibungen einbeziehen {#InputCompositionCandidateIncludesShortCharacterDescription}

mit dieser Option, die standardmäßig aktiviert ist, können Sie festlegen, ob NVDA eine kurze Beschreibung für einen zeichensatz ausgeben soll - entweder wenn Sie ihn auswählen oder wenn NVDA die Liste der Schriftsätze ausgibt, sobald diese erscheint.
In einigen Sprachräumen, wie etwa im Chinesischen, hat diese Option jedoch keinen Einfluss auf die Ausgabe der Beschreibungen für die Zeichensätze.
Diese Option ist lediglich für japanische und koreanische Eingabemethoden sinnvoll.

##### Änderungen zu Leseketten ansagen {#InputCompositionReadingStringChanges}

Einige Eingabemethoden wie z. B. Chinese New Phonetic und New ChangJie besitzen einen "reading string (auch als "precomposition string" bezeichnet).
Mit dieser Option teilen Sie NVDA mit, ob neue Zeichen, die in diese Zeichenketten eingegeben werden, zurückgemeldet werden sollen.
Diese Option ist standardmäßig aktiviert.
Bedenken Sie, dass bei einigen älteren Eingabemethoden wie Chinese ChangJie der "composition string" benutzt wird, um diese Informationen bereitzustellen. Lesen Sie den folgenden Abschnitt für weitere Informationen zum "composition string".

##### Änderungen zu Zusammenfassungsketten ansagen {#InputCompositionCompositionStringChanges}

Nachdem die Präcompositionsdaten zu einem gültigen piktografischen Zeichen zusammengeführt wurden, wird dieses zusammen mit weiteren Symbolen in einem composition string gespeichert, bevor dieser in das Dokument geschrieben wird.
Mit dieser Option legen Sie fest, ob NVDA Änderungen an den Symbolen im composition string wiedergeben soll.
Diese Option ist standardmäßig aktiviert.

#### Einnstellungen zum Lesemodus {#BrowseModeSettings}

<!-- KC:setting -->

##### Einstellungen zum Lesemodus öffnen {#toc235}

Tastenkombination: `NVDA+Strg+B`

Hier kann das Verhalten von NVDA in komplexen Dokumenten wie Webseiten beeinflusst werden.
Diese Kategorie enthält die folgenden Optionen:

##### Anzahl Zeichen pro Zeile {#BrowseModeSettingsMaxLength}

Dieses Feld legt die maximale Länge (Zeichen) einer Zeile im Lesemodus fest.

##### Anzahl Zeilen pro Seite {#BrowseModeSettingsPageLines}

Wenn gleich der Lesemodus keine wirklichen Seiten hat, können Sie jedoch hier festlegen, wie viele Zeilen beim Blättern mit den Tasten "Bild nach oben" und "Bild nach unten" auf einmal übersprungen werden sollen.

<!-- KC:setting -->

##### Bildschirm-Layout verwenden {#BrowseModeSettingsScreenLayout}

Tastenkombination: NVDA+V

Mit dieser Option können Sie festlegen, ob der Lesemodus anklickbare Inhalte (Links, Schaltflächen und Felder) in einer eigenen Zeile darstellen soll oder ob sie innerhalb des Textes bleiben sollen, wie sie visuell angezeigt werden.
Beachten Sie, dass diese Option nicht für Microsoft Office-Anwendungen wie Outlook und Word gilt, die immer das Bildschirm-Layout verwenden.
Wenn das Bildschirm-Layout aktiviert ist, bleiben die Seitenelemente so, wie sie visuell dargestellt werden.
Zum Beispiel wird eine visuelle Zeile mit mehreren Links in Sprache und Braille als mehrere Links auf derselben Zeile dargestellt.
Wenn sie deaktiviert ist, werden die Seitenelemente in einer separaten Zeilen dargestellt.
Dies kann bei Bedarf die zeilenweise Seitennavigation übersichtlicher gestalten und die Interaktion mit den Elementen für einige Benutzer erleichtern.

##### Lesemodus beim Laden von Webseiten verwenden {#BrowseModeSettingsEnableOnPageLoad}

Mit diesem Kontrollkästchen legen Sie fest, ob der Lesemodus beim Laden einer Webseite aktiviert werden soll.
Der Lesemodus kann auf Seiten und in Dokumenten, die diesen Modus unterstützen, weiterhin manuell aktiviert werden, auch wenn diese Option deaktiviert ist.
Weitere Informationen, welche Anwendungen den Lesemodus unterstützen, finden Sie im Abschnitt [Lesemodus](#BrowseMode).
Beachten Sie, dass diese Option nicht für Situationen gilt, in denen der Lesemodus immer optional ist, z. B. in Microsoft Word.
Diese Option ist standardmäßig aktiviert und somit wird der Lesemodus automatisch beim Laden von Webseiten verwendet.

##### Webseite nach dem Laden automatisch vorlesen {#BrowseModeSettingsAutoSayAll}

Diese Option steuert, ob Dokumente automatisch vorgelesen werden sollen, sobald sie vollständig geladen werden.
Diese Option ist standardmäßig aktiviert.

##### Layout-Tabellen im Lesemodus einbeziehen {#BrowseModeSettingsIncludeLayoutTables}

Mit dieser Option können Sie bestimmen, wie NVDA mit Tabellen umgeht, die nur zu Gestaltungszwecken verwendet werden.
Wenn die Option aktiviert ist, wird NVDA solche Tabellen auf der Grundlage der [Einstellungen zur Dokumentformatierung](#DocumentFormattingSettings) anzeigen und über die Schnellnavigationstasten zugänglich machen.
Anderenfalls werden Layout-Tabellen weder angezeigt noch über die Schnellnavigationstasten zugänglich gemacht.
Der Inhalt der Tabellen wird aber dennoch normal angezeigt.
Die Option ist standardmäßig deaktiviert.

Um die Ausgabe von Layout-Tabellen schnell ein- oder auszuschalten, müssen Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden, um eine Tastenkombination zuzuweisen.

##### Ansagen für Elemente konfigurieren {#BrowseModeLinksAndHeadings}

Bitte beachten Sie die Optionen in der Kategorie [Dokumentformatierungen](#DocumentFormattingSettings), um festzulegen, welche Elemente wie Links, Überschriften und Tabellen beim Navigieren angesagt werden sollen.

##### Bei Änderungen des Fokusses automatisch den Fokusmodus einschalten {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Diese Option ermöglicht bei Änderungen des Fokusses den Fokusmodus zu aktivieren.
Zum Beispiel: Sie befinden sich auf einer Webseite und landen beim Drücken der Tabulatortaste auf einem Formularfeld, schaltet NVDA in den Fokusmodus um, sofern diese Option eingeschaltet ist.

##### Bei Bewegungen des System-Cursors automatisch den Fokusmodus einschalten {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Wenn diese Option eingeschaltet ist, schaltet NVDA den Fokusmodus beim Navigieren mit den Pfeiltasten automatisch ein oder aus.
Wenn Sie beispielsweise auf eine Webseite nach unten navigieren und auf einem Eingabefeld treffen, schaltet NVDA automatisch in den Fokusmodus um.
Wenn Sie das Eingabefeld verlassen, schaltet NVDA wieder zurück in den Lesemodus um.

##### Akustische Ausgabe von Fokus- und Lesemodus {#BrowseModeSettingsPassThroughAudioIndication}

Bei eingeschalteter Option ertönt in NVDA vor der Ansage über die Änderung ein besonderer Hinweiston, wenn Sie von einem in den anderen Modus wechseln.

##### Nur Tasten im virtuellen Dokument verarbeiten {#BrowseModeSettingsTrapNonCommandGestures}

Wenn diese Option aktiviert ist, werden Tastenkombinationen, die nicht mit Schnellnavigationsbefehlen belegt sind, direkt an die aktuelle Anwendung weitergereicht, wenn Sie diese innerhalb des Lesemodus benutzen.
Wenn beispielsweise der Buchstabe "J" gedrückt wurde und aktiviert ist, würde er vom Erreichen des Dokuments abgefangen, obwohl es sich weder um einen Schnellnavigationsbefehl handelt noch wahrscheinlich um einen Befehl in der Anwendung selbst.
In diesem Fall weist NVDA Windows an, einen Standard-Sound abzuspielen, wenn eine Taste gedrückt wird, die festgestellt wird.

<!-- KC:setting -->

##### Automatisches Bewegen des System-Fokus auf fokussierbare Elemente im Lesemodus {#BrowseModeSettingsAutoFocusFocusableElements}

Tastenkombination: NVDA+8

Wenn diese Option deaktiviert ist, können Sie wählen, ob der Systemfokus automatisch auf Elemente gesetzt werden soll, die den System-Fokus übernehmen können (Links, Formularfelder, etc.), wenn Sie mit dem Cursor im Browse-Modus durch den Inhalt navigieren.
Wenn diese Option deaktiviert bleibt, werden fokussierbare Elemente nicht automatisch fokussiert, wenn sie mit dem Cursor im Browse-Modus ausgewählt werden.
Dies kann zu einem schnelleren Verhalten im Browser und einer verbesserten Reaktionsgeschwindigkeit im Lesemodus führen.
Der Fokus wird noch auf das jeweilige Element aktualisiert, wenn man mit ihm interagiert (z. B. einen Schalter drückt, ein Kontrollkästchen markiert).
Die Aktivierung dieser Option kann die Unterstützung für einige Websites auf Kosten der Leistung und Stabilität verbessern.

#### Einstellungen zur Dokument-Formatierungen {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Einstellungen zur Dokument-formatierung öffnen {#toc249}

Tastenkombination: `NVDA+Strg+D`

Die meisten Optionen in dieser Kategorie dienen dazu, die Art der Formatierung zu konfigurieren, die Sie beim Bewegen des Cursors in den Dokumenten erhalten möchten.
Wenn Sie z. B. das Kontrollkästchen "Schriftartennamen mitteilen" aktivieren und anschließend in einem Text navigieren, wird NVDA jedes Mal den Namen der Schriftart ansagen, sobald sich die Schriftart ändert.

Diese Optionen sind in Gruppen aufgeteilt.
Konfigurieren können Sie die Meldungen von:

* Schriftart
  * Name der Schriftart
  * Schriftgröße
  * Schrift-Attribute
  * Hoch- und tiefgestellte Zeichen
  * Betonter Text
  * Hervorgehobener (markierter) Text
  * Layout
  * Farben
* Informationen über das Dokument
  * Kommentare
  * Lesezeichen
  * Dokument-Änderungen
  * Rechtschreibfehler
* Seiten und Abstände
  * Seitenwechsel
  * Zeilennummern
  * Zeileneinrückungen ausgeben durch: [Aus, Ansage, Signaltöne oder Ansagen und Signaltöne](#DocumentFormattingSettingsLineIndentation)
  * Ignorieren von Leerzeilen bei Mitteilung von Zeileneinrückungen
  * Absatzeinrückungen (z. B. hängender Einzug, Erstzeileneinzug)
  * Zeilenabstand (einfach, doppelt, etc.)
  * Ausrichtung
* Informationen über Tabellen
  * Tabellen
  * Reihen- und Spaltenüberschriften (Aus, Zeilen, Spalten, Zeilen und Spalten)
  * Zellkoordinaten
  * Zellrahmen (Aus, Formatierung, Farben und Formatierung)
* Elemente
  * Überschriften
  * Links
  * Grafiken
  * Listen
  * Zitatblöcke
  * Gruppierungen
  * Sprungmarken
  * Artikel
  * Rahmen
  * Abbildungen und Beschriftungen
  * Anklickbare Elemente

Um diese Einstellungen überall ändern zu können, verwenden Sie bitte das Dialogfeld für die [Tastenbefehle](#InputGestures) um eigene Tastenkombinationen hinzuzufügen.

##### Änderungen der Formatierungen hinter dem Cursor ausgeben {#DocumentFormattingDetectFormatAfterCursor}

Diese Einstellung veranlasst NVDA dazu, ALLE Änderungen in den Formatierungen innerhalb einer Zeile anzusagen, wenn sie eingeschaltet ist. Das kann sehr leistungsintensiv sein.

Standardmäßig erkennt NVDA die Formatierung an der Position des System-Cursors. In einigen Situationen erkennt auch NVDA die Formatierungen der gesamten Zeile. Dies könnte allerdings die Systemleistung beeinträchtigen.

Schalten Sie diese Option nur dann ein, wenn beim Lesen in einem WordPad-Dokument die Ansage notwendig ist.

##### Ausgabe von Zeileneinrückungen {#DocumentFormattingSettingsLineIndentation}

Mit dieser Option legen Sie fest, wie Zeileneinrückungen durch NVDA wiedergegeben werden sollen.
Das Kombinationsfeld enthält vier Einträge:

* Ausgeschaltet: NVDA wird Zeileneinrückungen in keiner Weise gesondert ausgeben
* Sprache: Diese Einstellung bringt NVDA dazu die Anzahl von Zeichen anzusagen, mit denen eine Zeile eingerückt wurde (z. B. 12 Leerzeichen oder 4 Tabulatoren)
* Signaltöne: Diese Einstellung bringt NVDA dazu, die Einrückung mit Hilfe von Signaltönen anzugeben. Wenn sich die Einrückung ändert, wird der Signalton höher, je stärker eine Zeile eingerückt ist.
Die Einrückung um einen Tabulator entspricht hierbei der Einrückung um vier Leerzeichen.
* Sowohl Sprache und Signaltöne: Dies ist eine Kombination der beiden obigen Optionen.

Wenn Sie das Kontrollkästchen "Ignorieren von Leerzeilen bei Mitteilung von Zeileneinrückungen" aktivieren, werden Änderungen der Einrückung für Leerzeilen nicht mitgeteilt.
Dies kann nützlich sein, wenn Sie ein Dokument lesen, in dem Leerzeilen zur Trennung von eingerückten Textblöcken verwendet werden, wie z. B. in einem Programm-Quellcode.

#### Dokument-Navigation {#DocumentNavigation}

In dieser Kategorie können Sie verschiedene Aspekte der Dokument-Navigation anpassen.

##### Absatz-Eigenschaften {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (Wird von der Anwendung behandelt), Wird von der Anwendung behandelt, Einfacher Zeilenumbruch, Mehrfacher Zeilenumbruch|
|Standard |Wird von der Anwendung behandelt|

Dieses Kombinationsfeld ermöglicht die Absatz-Eigenschaft auszuwählen, der bei der Navigation durch Absätze mit `STRG+Pfeiltaste nach oben` und `STRG+Pfeiltaste nach unten` verwendet werden soll.
Die verfügbaren Absatzformate sind:

* Wird von der Anwendung behandelt: NVDA überlässt es der Anwendung, den vorherigen oder nächsten Absatz zu bestimmen, und NVDA liest den neuen Absatz beim Navigieren.
Dies funktioniert am besten, wenn die Anwendung die Absatznavigation von Haus aus unterstützt, und ist die Standardeinstellung.
* Einfacher Zeilenumbruch: NVDA versucht, den vorherigen oder nächsten Absatz anhand eines einzelnen Zeilenumbruchs als Absatz-Indikator zu bestimmen.
Dies funktioniert am besten, wenn Dokumente in einer Anwendung gelesen werden, die nicht von Haus aus die Absatznavigation unterstützt, und Absätze im Dokument durch einmaliges Drücken der `Eingabetaste` markiert werden.
* Mehrfache Zeilenumbrüche: NVDA versucht, den vorherigen oder nächsten Absatz anhand von mindestens einer Leerzeile (zweimaliges Drücken der `Eingabetaste`) als Absatz-Indikator zu bestimmen.
Dies funktioniert am besten bei Dokumente, die Blockabsätze verwenden.
Beachten Sie, dass dieses Absatzformat nicht in Microsoft Word oder Microsoft Outlook verwendet werden kann, es sei denn, Sie verwenden UIA für den Zugriff bei Steuerelementen in Microsoft Word.

Sie können von überall aus zwischen den verfügbaren Absatz-Eigenschaften umschalten, indem Sie eine Taste im Dialogfeld für die [Tastenbefehle](#InputGestures) zuweisen.

#### Einstellungen der Windows-Texterkennung {#Win10OcrSettings}

Mit den Einstellungen in dieser Kategorie können Sie die [Windows-Texterkennung](#Win10Ocr) konfigurieren.
Folgende Optionen sind enthalten:

##### Erkennungssprache {#Win10OcrSettingsRecognitionLanguage}

In diesem Kombinationsfeld können Sie die Sprache festlegen, die für die Zeichenerkennung verwendet werden soll.
Um von überall aus durch die verfügbaren Sprachen zu wechseln, weisen Sie bitte einen Tastenbefehl zu, indem Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden.

##### Regelmäßige Aktualisierung von erkannten Inhalten {#Win10OcrSettingsAutoRefresh}

Wenn dieses Kontrollkästchen aktiviert ist, aktualisiert NVDA den erkannten Inhalt automatisch, sobald ein Ergebnis der Erkennung fokussiert ist.
Dies kann sehr nützlich sein, wenn Sie ständig wechselnde Inhalte überwachen möchten, z. B. bei einem Video mit Untertiteln.
Die Aktualisierung erfolgt alle eineinhalb Sekunden.
Diese Option ist standardmäßig deaktiviert.

#### Erweiterte Einstellungen {#AdvancedSettings}

Achtung! Die Einstellungen in dieser Kategorie sind für fortgeschrittene Benutzer und können dazu führen, dass NVDA bei falscher Konfiguration nicht richtig funktioniert.
Nehmen Sie Änderungen an diesen Einstellungen nur dann vor, wenn Sie sicher sind, dass Sie wissen, was Sie tun oder wenn Sie von einem NVDA-Entwickler ausdrücklich dazu angewiesen wurden.

##### Änderungen in den erweiterten Einstellungen vornehmen {#AdvancedSettingsMakingChanges}

Um Änderungen in den erweiterten Einstellungen vornehmen zu können, müssen die Bedienelemente aktiviert werden, indem Sie mit dem Kontrollkästchen bestätigen, dass Sie die Risiken einer Änderung dieser Einstellungen verstanden haben.

##### Die Standard-Einstellungen wiederherstellen {#AdvancedSettingsRestoringDefaults}

Die Schaltfläche stellt die Standardwerte für die Einstellungen wieder her, auch wenn das Kontrollkästchen zur Bestätigung nicht aktiviert ist.
Nach dem Ändern der Einstellungen können Sie zu den Standardwerten zurückkehren.
Dies kann auch der Fall sein, wenn Sie sich nicht sicher sind, ob die Einstellungen geändert wurden.

##### Laden von benutzerdefiniertem Code aus dem Developer Scratchpad-Verzeichnis aktivieren {#AdvancedSettingsEnableScratchpad}

Bei der Entwicklung von NVDA-Erweiterungen ist es sinnvoll, Code bereits beim Schreiben testen zu können.
Wenn diese Option aktiviert ist, kann NVDA benutzerdefinierte Unterverzeichnisse appModules, globalPlugins, brailleDisplayDrivers, synthDrivers und visionEnhancedProviders aus einem speziellen Entwickler-Scratchpad-Verzeichnis im NVDA-Benutzerkonfigurationsverzeichnis laden.
Äquivalent wie in NVDA-Erweiterungen werden diese Module beim Starten von NVDA oder, im Fall von appModules und globalPlugins, beim [Nachladen von Plugins](#ReloadPlugins) geladen.
Diese Option ist standardmäßig deaktiviert und stellt sicher, dass kein ungetesteter Code ohne explizites Wissen des Benutzers in NVDA ausgeführt wird.
Wenn Sie benutzerdefinierten Code an andere weitergeben möchten, sollten Sie ihn als NVDA-Erweiterungspaket verpacken.

##### Developer Scratchpad-Verzeichnis öffnen {#AdvancedSettingsOpenScratchpadDir}

Diese Schaltfläche öffnet das Verzeichnis, in dem Sie während der Entwicklung benutzerdefinierten Code platzieren können.
Diese Schaltfläche ist nur aktiv, wenn NVDA so konfiguriert ist, dass benutzerdefinierter Code aus dem Developer Scratchpad-Verzeichnis geladen werden kann.

##### Registrierung zu UIA-Ereignissen und Eigenschaftsänderungen {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Automatisch, Ausgewählt, Überall|
|Standard |Automatisch|

Diese Option ändert die Art und Weise, wie NVDA sich für Ereignisse registriert, die von der Microsoft UI Automation Accessibility API ausgelöst werden.
Das Kombinationsfeld "Registrierung für UIA-Ereignisse und Eigenschaftsänderungen" enthält drei Optionen:

* Automatisch: "Ausgewählt" unter Windows 11 Version 22H2 oder 2022 (Sun Valley 2) und höher, ansonsten "Überall".
* Ausgewählt: Bei den meisten Ereignissen beschränkt sich NVDA auf den System-Fokus.
Wenn Sie in einer oder mehreren Anwendungen damit probleme haben sollten, empfehlen wir Ihnen, diese Funktionalität auszuprobieren, um zu sehen, ob sich die leistung dadurch verbessert.
Bei älteren Windows-Versionen hat NVDA jedoch möglicherweise Probleme bei der Verfolgung des Fokus in einigen Steuerelementen (z. B. im Task-Manager und im Emoji-Panel).
* Überall: NVDA registriert viele UIA-Ereignisse, die in NVDA selbst verarbeitet und verworfen werden.
Während die Fokusverfolgung in verschiedenen Situationen zuverlässiger ist, wird die Leistung erheblich beeinträchtigt, insbesondere in Anwendungen wie Microsoft Visual Studio.

##### UIA verwenden, um auf die Steuerelemente in Dokumenten in Microsoft Word zuzugreifen {#MSWordUIA}

Legt fest, ob NVDA für den Zugriff auf Microsoft Word-Dokumente die UIA-API für Barrierefreiheit oder das ältere Objektmodell verwenden soll.
Dies gilt sowohl für Dokumente in Microsoft Word selbst, als auch für Nachrichten in Microsoft Outlook.
Diese Einstellung enthält die folgenden Werte:

* Standard (sofern geeignet).
* Nur bei Bedarf: Wenn das ältere Objektmodell in Microsoft Word überhaupt nicht verfügbar ist.
* Sofern geeignet: Microsoft Word Version 16.0.15000 oder neuer, oder wenn das ältere Objektmodell in Microsoft Word gar nicht verfügbar ist.
* Immer: Wo auch immer UIA in Microsoft Word verfügbar ist (unabhängig davon, wie es funktioniert).

##### UIA verwenden, um auf die Steuerelemente von Microsoft Excel-Tabellen zuzugreifen, sofern verfügbar {#UseUiaForExcel}

Wenn diese Option aktiviert ist, versucht NVDA, die Microsoft UIA-API für Barrierefreiheit zu verwenden, um Informationen aus den Steuerelementen von Microsoft Excel-Tabellen abzurufen.
Dies ist eine experimentelle Funktion, und einige Funktionen von Microsoft Excel sind in diesem Modus möglicherweise nicht verfügbar.
So sind beispielsweise die Liste der Elemente in NVDA zum Auflisten von Formeln und Kommentaren und die Schnellnavigation im Lesemodus zum Springen zu Formularfeldern in einer Kalkulationstabelle nicht verfügbar.
Für die einfache Navigation und Bearbeitung von Tabellenkalkulationen kann diese Option jedoch eine enorme Leistungsverbesserung bedeuten.
Es wird nach wie vor nicht empfohlen, dass die Mehrheit der Benutzer diese Funktion standardmäßig aktiviert, obwohl Benutzer von Microsoft Excel-Version 16.0.13522.10000 oder neuer dazu aufgefordert sind, diese Funktion zu testen und Feedback einzureichen.
Die Implementierung der UIA von Microsoft Excel ändert sich ständig, und Versionen von Microsoft Office, die älter als 16.0.13522.10000 sind, geben möglicherweise nicht genügend Informationen darüber Aus, um diese Option zu nutzen.

##### Erweiterte Ereignisverarbeitung verwenden {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (eingeschaltet), ausgeschaltet, eingeschaltet|
|Standard |eingeschaltet|

Wenn diese Option aktiviert ist, sollte NVDA weiterhin reagieren, wenn es mit vielen UI-Automatisierungsereignissen überflutet wird, z. B. große Textmengen in einem Terminalfenster.
NVDA muss neu gestartet werden, damit die geänderte Einstellung wirksam wird.

##### Unterstützung der Windows-Konsole {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Automatisch, UIA, sofern verfügbar, Legacy|
|Standard |Automatisch|

Diese Option legt fest, wie NVDA mit der Windows-Konsole interagiert, die von der Eingabeaufforderung, der PowerShell und dem Windows-Subsystem für Linux verwendet wird.
Das moderne Windows-Terminal ist davon nicht betroffen.
In Windows 10 Version 1709 hat Microsoft [der Konsole](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/) Unterstützung für seine UI-Automatisierungs-API hinzugefügt und damit die Leistung und Stabilität für Screenreader, die diese unterstützen, erheblich verbessert.
In Situationen, in denen die UIA nicht verfügbar ist oder bekanntermaßen zu einem schlechteren Erlebnis für den Benutzer führt, steht die NVDA-Konsolenunterstützung als Ausweichlösung zur Verfügung.
Das Kombinationsfeld für die Unterstützung der Windows-Konsole enthält drei Optionen:

* Automatisch: Verwendet UIA in der Version der Windows-Konsole, die in Windows 11 Version 22H2 und neuer enthalten ist.
Diese Option wird empfohlen und ist standardmäßig eingestellt.
* UIA verwenden, sofern verfügbar: Verwendet UIA in Konsolen, sofern verfügbar, auch für Versionen mit unvollständigen oder fehlerhaften Implementierungen.
Diese eingeschränkte Funktionalität kann zwar nützlich (und für Ihre Zwecke sogar ausreichend) sein, aber die Nutzung dieser Option erfolgt auf eigene Gefahr, und es wird kein Support dafür angeboten.
* Legacy: Die UIA in der Windows-Konsole wird vollständig deaktiviert.
Der Legacy-Fallback wird immer verwendet, selbst in Situationen, in denen UI Automation eine bessere Benutzererfahrung bieten würde.
Es wird daher nicht empfohlen, diese Option auszuwählen, wenn Sie nicht wissen, was Sie tun.

##### UIA mit Microsoft Edge und anderen Chromium-basierten Browsern verwenden, sofern verfügbar {#ChromiumUIA}

Legt fest, wann UIA verwendet wird, wenn es in Chromium-basierten Browsern wie Microsoft Edge verfügbar ist.
Die UIA-Unterstützung für Chromium-basierte Browser befindet sich noch in einem frühen Entwicklungsstadium und bietet möglicherweise nicht das gleiche Maß an Zugriff wie IA2.
Das Kombinationsfeld hat die folgenden Optionen:

* Standard (nur wenn nötig): Der NVDA-Standard, derzeit ist dies "Nur wenn nötig". Diese Voreinstellung kann sich in Zukunft ändern, wenn die Technologie ausgereift ist.
* Nur wenn nötig: Wenn NVDA nicht in der Lage ist, in den Browser-Prozess einzugreifen, um IA2 zu verwenden, und UIA verfügbar ist, greift NVDA auf die Verwendung von UIA zurück.
* Ja: Wenn der Browser UIA zur Verfügung stellt, wird NVDA es verwenden.
* Nein: UIA wird nicht verwendet, auch wenn NVDA nicht in den Prozess injizieren kann. Dies kann für Entwickler nützlich sein, die Probleme mit IA2 debuggen und sicherstellen wollen, dass NVDA nicht auf UIA zurückgreift.

##### Anmerkungen {#Annotations}

Diese Gruppe der Optionen wird verwendet, um Funktionen zu aktivieren, die experimentelle Unterstützung für ARIA-Anmerkungen ergänzen.
Einige dieser Funktionen sind möglicherweise noch nicht vollständig.

<!-- KC:beginInclude -->
Drücken Sie NVDA+D, um die "Zusammenfassung aller Details der Anmerkungen an der Position des System-Cursors mitzuteilen".
<!-- KC:endInclude -->

Die folgenden Möglichkeiten gibt es:

* "Enthält Details"-Meldung für strukturierte Anmerkungen: Ermöglicht die Meldung, wenn der Text oder das Steuerelement weitere Details enthält.
* "Aria-Beschreibung immer mitteilen":
  Wenn die Quelle von `accDescription` aria-description ist, wird die Beschreibung mitgeteilt.
  Dies ist nützlich für Anmerkungen im Internet.
  Hinweis:
  * Es gibt viele Quellen für `accDescription`, einige haben eine gemischte oder unzuverlässige Semantik.
    Historisch gesehen war AT nicht in der Lage, Quellen von `accDescription` zu unterscheiden, typischerweise wurde es aufgrund der gemischten Semantik nicht gesprochen.
  * Diese Option befindet sich in einer sehr frühen Entwicklungsphase, sie basiert auf Browser-Funktionen, die noch nicht weit verbreitet sind.
  * Funktioniert voraussichtlich ab Chromium 92.0.4479.0

##### Live-Regionen mitteilen {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (eingeschaltet), Ausgeschaltet, Eingeschaltet|
|Standard |Eingeschaltet|

Mit dieser Option können Sie festlegen, ob NVDA die Änderungen in einigen dynamischen Web-Inhalten auf der Braillezeile mitteilt.
Die Deaktivierung dieser Option entspricht dem NVDA-Versionen vor 2023.1, die diese Änderungen der Inhalte nur über die Sprachausgabe mitteilten.

##### Passwörter in allen erweiterten Terminals mitteilen {#AdvancedSettingsWinConsoleSpeakPasswords}

Diese Einstellung steuert, ob Zeichen mit [Zeichen während der Eingabe ansagen](#KeyboardSettingsSpeakTypedCharacters) oder [Wörter während der Eingabe ansagen](#KeyboardSettingsSpeakTypedWords) in Situationen mitgeteilt werden, in denen der Bildschirm nicht aktualisiert wird (z. B. bei der Eingabe eines Kennworts) und zwar in einigen Terminal-Anwendungen wie der Windows-Konsole mit aktivierter Unterstützung für die UIA und Mintty.
Aus Sicherheitsgründen sollte diese Einstellung deaktiviert bleiben.
Sie sollten sie jedoch aktivieren, wenn Sie Leistungsprobleme oder Probleme bei der Stabilität bei der Meldung von eingegebenen Zeichen und/oder Wörtern in Konsolen feststellen oder in vertrauenswürdigen Umgebungen arbeiten und eine Kennwortanzeige dort bevorzugen.

##### Verwendung der erweiterten Unterstützung für eingegebene Zeichen in der alten Windows-Konsole, sofern verfügbar {#AdvancedSettingsKeyboardSupportInLegacy}

Diese Option ermöglicht eine alternative Methode zur Erkennung eingegebener Zeichen in älteren Windows-Konsolen.
Durch das Aktivieren dieser Option wird zwar die Leistung gesteigert und das Buchstabieren mancher Ausgaben in Windows-Konsolen verhindert; es könnten jedoch Probleme mit einigen Terminals auftreten.
Diese Funktion ist verfügbar und seit Windows 10 Version 1607 standardmäßig aktiviert, wenn die UIA nicht verfügbar oder deaktiviert ist.
Das Eingeben von Zeichen, die nicht auf dem Bildschirm erscheinen (z. B. bei Passwörtern) wird nicht unterstützt, wenn diese Option aktiviert ist.
In Umgebungen, die nicht unterstützt werden, können Sie vorübergehend [Zeichen während der Eingabe ansagen](#KeyboardSettingsSpeakTypedCharacters) und [Wörter während der Eingabe ansagen](#KeyboardSettingsSpeakTypedWords) deaktivieren, wenn Sie Passwörter eingeben.

##### Diff-Algorithmus {#DiffAlgo}

Diese Einstellung steuert, wie NVDA neuen Text in Terminals vorlesen soll.
Das Kombinationsfeld "Diff-Algorithmus" hat drei Optionen:

* Automatisch: Diese Option bewirkt, dass NVDA in den meisten Situationen Diff Match Patch bevorzugt, aber bei problematischen Anwendungen, wie z. B. älteren Versionen der Windows-Konsole und Mintty, auf Difflib zurückgreift.
* Diff Match Patch: Diese Option bewirkt, dass NVDA Änderungen am Terminaltext zeichenweise berechnet, auch in Situationen, in denen dies nicht empfohlen wird.
Dies kann die Leistung verbessern, wenn große Textmengen in die Konsole geschrieben werden, und ermöglicht eine genauere Meldung von Änderungen, die in der Mitte von Zeilen vorgenommen wurden.
Bei einigen Anwendungen kann das Lesen von neuem Text jedoch abgehackt oder inkonsistent sein.
* Difflib: Diese Option bewirkt, dass NVDA Änderungen am Terminaltext zeilenweise berechnet, auch in Situationen, in denen dies nicht empfehlenswert ist.
Es ist identisch mit dem Verhalten von NVDA in den Versionen 2020.4 und älter.
Diese Einstellung kann das Lesen von eingehendem Text in einigen Anwendungen stabilisieren.
In Terminals wird jedoch beim Einfügen oder Löschen eines Zeichens in der Mitte einer Zeile der Text nach dem System-cursor vorgelesen.

##### Neuen Text in Windows-Terminal mitteilen via {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (Abweichend), Abweichend, UIA-Benachrichtigungen|
|Standard |Abweichend|

Mit dieser Option wird festgelegt, wie NVDA bestimmt, welcher Text "neu" ist (und somit, was mitgeteilt werden soll, wenn "Änderungen dynamischer Inhalte mitteilen" aktiviert ist) in Windows-Terminal und dem WPF-Windows-Terminal-Steuerelement, das in Visual Studio 2022 verwendet wird.
Die Windows-Konsole (`conhost.exe`) ist davon nicht betroffen.
Dieses Kombinationsfeld hat drei Optionen:

* Standard: Diese Option ist derzeit gleichwertig mit "diffing", wird sich aber voraussichtlich ändern, sobald die Unterstützung für UIA-Benachrichtigungen weiter entwickelt wurde.
* Abweichend: Bei dieser Option wird der ausgewählte Diff-Algorithmus verwendet, um die Änderungen jedes Mal zu berechnen, wenn das Terminal neuen Text rendert.
Dies ist identisch mit dem Verhalten von NVDA in den Versionen 2022.4 und älter.
* UIA-Benachrichtigungen: Mit dieser Option wird die Entscheidung, welcher Text mitgeteilt werden soll, an das Windows-Terminal übertragen, d. h., NVDA muss nicht mehr feststellen, welcher Text auf dem Bildschirm "neu" ist.
Dies sollte die Leistung und Stabilität im Windows-Terminal deutlich verbessern, aber diese Funktion ist noch nicht vollständig.
Insbesondere werden Zeichen während der Eingabe, die nicht auf dem Bildschirm angezeigt werden, wie z. B. Kennwörter, mitgeteilt, wenn diese Option ausgewählt ist.
Außerdem kann es vorkommen, dass zusammenhängende Abschnitte mit mehr als 1.000 Zeichen nicht korrekt mitgeteilt werden.

##### Sprachausgabe unterbrechen, wenn das Ereignis für den Fokus abgelaufen ist: {#CancelExpiredFocusSpeech}

Diese Option aktiviert ein Verhalten, welches bei abgelaufenen Ereignissen des Fokus versucht, die Sprachausgabe abzubrechen.
Insbesondere das schnelle Durchlaufen von Nachrichten in GMail mit Google Chrome kann dazu führen, dass NVDA alte Informationen noch vorliest.
Diese Funktion ist ab NVDA 2021.1 standardmäßig aktiviert.

=== Zeitüberschreitung beim Bewegen des System-Cursors ====[AdvancedSettingsCaretMoveTimeout]
Mit dieser Option können Sie die Anzahl der Millisekunden konfigurieren, die NVDA wartet, bis sich der Cursor (Einfügepunkt) in den editierbaren Textsteuerelementen bewegt.
Wenn Sie feststellen, dass NVDA die Einfügemarke falsch zu verfolgen scheint, z. B., wenn NVDA immer ein Zeichen hinterher liegt oder beim Navigieren manche Zeilen wiederholt, dann sollten Sie versuchen, diesen Wert zu erhöhen.

##### Transparente Farben mitteilen {#ReportTransparentColors}

Diese Option teilt mit, wenn Farben transparent sind. Dies ist nützlich für Entwickler von NVDA-Erweiterungen und Anwendungs-Modulen, die Informationen sammeln, um die Benutzererfahrung mit einer Drittanbieteranwendung zu verbessern.
Einige GDI-Anwendungen heben Text mit einer Hintergrundfarbe hervor, NVDA versucht, diese Farbe mittels des Anzeige-Modells mitzuteilen.
In einigen Situationen kann der Texthintergrund vollständig transparent sein, wobei der Text über einem anderen Element der grafischen Oberfläche liegt.
Bei mehreren historisch beliebten APIs von grafischen Oberflächen kann der Text mit einem transparenten Hintergrund gerendert werden, aber die Hintergrundfarbe ist visuell korrekt.

##### WASAPI für die Audio-Ausgabe verwenden {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Optionen |Standard (Eingeschaltet), Ausgeschaltet, Eingeschaltet|
|Standard |Eingeschaltet|

Diese Option aktiviert die Audio-Ausgabe über die API der Windows-Audio-Session (WASAPI).
Das WASAPI ist ein moderneres Audio-Framework, das die Reaktionsfähigkeit, Leistung und Stabilität der Audio-Ausgabe in NVDA, einschließlich Sprachausgabe und Sounds, verbessern kann.
Nachdem Sie diese Option geändert haben, müssen Sie NVDA neu starten, damit die Änderung wirksam wird.
Wenn Sie WASAPI deaktivieren, werden die folgenden Optionen deaktiviert:

* [Lautstärke der NVDA-Sounds folgt der Lautstärke der Stimme](#SoundVolumeFollowsVoice)
* [Lautstärke der NVDA-Sounds](#SoundVolume)

##### Kategorien der Protokollierungsstufe {#AdvancedSettingsDebugLoggingCategories}

Mit diesen Kontrollkästchen in dieser Liste können Sie bestimmte Kategorien von Debug-Meldungen im Protokoll von NVDA aktivieren.
Das Protokollieren dieser Nachrichten kann zu Leistungseinbußen und großen Protokolldateien führen.
Schalten Sie nur eines davon ein, wenn dies von einem NVDA-Entwickler ausdrücklich angeordnet wurde, z. B. beim Debuggen, warum ein Braille-Treiber nicht ordnungsgemäß funktioniert.

##### Fehler im Protokoll mit einem Sound kennzeichnen {#PlayErrorSound}

Mit dieser Option können Sie festlegen, ob NVDA einen Fehlerton abspielen soll, falls ein Fehler protokolliert wird.
Bei Auswahl von "Nur in Testversionen" (Standard) ertönt nur dann ein NVDA-Wiedergabefehler, wenn die aktuelle NVDA-Version eine Testversion ist (Alpha-, Beta- oder Quellcode).
Wenn Sie "Ja" auswählen, können Sie unabhängig von Ihrer aktuellen NVDA-Version die Fehlertöne aktivieren.

##### Reguläre Ausdrücke für Schnellnavigationsbefehle zu Textabsätzen {#TextParagraphRegexEdit}

In diesem Feld können Benutzer reguläre Ausdrücke für die Erkennung von Textabschnitten im Lesemodus anpassen.
Der [Navigationsbefehl zu Textabsätzen](#TextNavigationCommand) sucht nach Absätzen, die mit diesem regulären Ausdruck übereinstimmen.

### Verschiedene Optionen {#MiscSettings}

Neben den [NVDA-Einstellungen](#NVDASettings), befinden sich weitere Einträge im NVDA-Menü unter "Optionen". Diese werden weiter unten erläutert.

#### Die Aussprache-Wörterbücher {#SpeechDictionaries}

Im Menü Optionen finden Sie den Eintrag Aussprache-Wörterbücher. Dieses Menü enthält Dialogfelder mit deren Hilfe Sie festlegen können, wie NVDA einzelne Wörter oder Satzteile ausspricht.
Derzeit gibt es drei unterschiedliche Formen der Aussprache-Wörterbücher:
Diese sind:

* Standard: Regeln in diesem Wörterbuch haben Einfluss auf alle Aussprachen in NVDA.
* Stimme: Regeln in diesem Wörterbuch haben Einfluss auf die momentan verwendete Stimme der Sprachausgabe in NVDA.
* Temporär: Regeln in diesem Wörterbuch haben nur vorläufigen Einfluss auf alle Stimmen in NVDA (gilt nur für diese Sitzung). Beim nächsten Neustart von NVDA sind diese nicht mehr vorhanden.

Sie müssen den Dialogfeldern eigene Tastenkombinationen zuweisen, falls Sie die Wörterbücher per Tastenkürzel aufrufen wollen. Verwenden Sie hierzu das Dialogfeld für die [Tastenbefehle](#InputGestures).

Alle Wörterbücher enthalten eine Liste von Sprachregeln, welche verwendet werden, um die Sprache zu verbessern.
Die Dialogfelder enthalten die folgenden Schaltflächen: "Hinzufügen", "Bearbeiten", "Entfernen" und "Alles entfernen".

Mit der Schaltfläche "Hinzufügen" erstellen Sie eine neue Regel im Wörterbuch. Anschließend füllen Sie die entsprechenden Felder aus und klicken danach auf "OK".
Sie sehen nun die neu hinzugefügte Regel in der Regelliste.
Um sicherzustellen, dass die neu hinzugefügten oder bearbeiteten Regeln auch tatsächlich gespeichert bleiben, klicken Sie einmal auf die "OK"-Schaltfläche, um damit auch das Dialogfeld der Wörterbücher zu schließen.

Mit den Regeln für die Aussprache-Wörterbücher von NVDA können Sie eine Zeichenkette in eine andere ändern.
Ein einfaches Beispiel wäre, wenn Sie möchten, dass NVDA bei dem Wort "Frosch" jedes Mal "Vogel" sagt.
Der einfachste Weg um dies zu erreichen ist wie folgt: Im Dialogfeld "Wörterbuch-Eintrag hinzufügen" geben Sie im Eingabefeld bei "Suchen nach" das Wort "Frosch" (ohne Anführungszeichen) ein und im Eingabefeld bei "Ersetzen durch" das Wort "Vogel" (ohne Anführungszeichen) ein.
Im Eingabefeld für die Beschreibung können Sie dann "Anpassen des Wortes Frosch durch Vogel" eintragen.

Die leistungsstarken Aussprache-Wörterbücher können weitaus mehr, als nur Wörter ersetzen.
Ferner enthält dieses Dialogfeld auch eine Option zur Berücksichtigung der Groß- und Kleinschreibung des Suchmusters.
Standardmäßig ignoriert NVDA die Groß- und Kleinschreibung.

Schließlich enthält das Dialogfeld auch noch 3 Auswahlschalter, die festlegen, ob die betreffende Regel überall, nur auf ganze Wörter angewendet oder ob reguläre Ausdrücke berücksichtigt werden sollen.
Die Einstellung des Musters auf Übereinstimmung als ganzes Wort bedeutet, dass die Ersetzung nur dann vorgenommen wird, wenn das Muster nicht als Teil eines größeren Wortes vorkommt.
Diese Bedingung ist erfüllt, wenn die Zeichen unmittelbar vor und nach dem Wort etwas anderes sind als ein Buchstabe, eine Zahl oder ein Unterstrich, oder wenn überhaupt keine Zeichen vorhanden sind.
Wenn man also das frühere Beispiel der Ersetzung des Wortes "Vogel" durch "Frosch" verwenden würde, würde das Wort "Vogel" oder "Blauer Vogel" nicht mit "Vögel" oder "Blauer Vogel" übereinstimmen.

Ein sogenannter Regulärer Ausdruck ist ein Muster, welches spezielle Symbole enthält. Dies ermöglicht, dass das Muster auf Zahlen oder Buchstaben generell oder auf mehrere Zeichen gleichzeitig zutrifft.
Reguläre Ausdrücke werden in diesem Benutzerhandbuch nicht behandelt.
Ein Tutorial zur Einführung finden Sie in [Python's Handbuch für regulläre Ausdrücke](https://docs.python.org/3.11/howto/regex.html)..

#### Interpunktion und Symbol-Aussprache {#SymbolPronunciation}

In diesem Dialogfeld können Sie die Interpunktion und Symbol-Aussprache verändern und festlegen, ab welcher Symbolebene dieses angesagt werden soll.

Die Sprache, in der die Aussprache von Sonderzeichen geändert wird, wird im Dialogtitel angezeigt.
Außerdem wird die Option "Beim Sprechen von Zeichen und Symbolen die Sprache der Stimme berücksichtigen" aus der Kategorie [Stimme und Sprachausgabe](#SpeechSettings) in den [NVDA-Einstellungen](#NVDASettings) berücksichtigt; beispielsweise wird hierbei die Sprache der eingestellten Stimme anstelle der NVDA-Sprache verwendet.

Um die Aussprache eines Sonderzeichens zu verändern, wählen Sie es in der Liste der Symbole aus.
Sie können die Symbole auch filtern, indem Sie das Symbol oder einen Teil der Ersetzung des Symbols in das Bearbeitungsfeld "Filter nach" eingeben.

* Das Eingabefeld "Ersetzen durch" ermöglicht den Text zu verändern, der an dieser Stelle des Symbols mitgeteilt wird.
* Im Kombinationsfeld für die Symbolstufe kann eingestellt werden, ab welcher Stufe Satz- und Sonderzeichen angesagt werden sollen (Keine, Einige, Meiste oder Alle).
Sie können die Stufe auch auf Zeichen einstellen; in diesem Fall wird das Symbol unabhängig von der verwendeten Symbolstufe nicht mitgeteilt, mit den folgenden zwei Ausnahmen:
  * Wenn Sie Zeichen für Zeichen navigieren.
  * Wenn NVDA einen Text buchstabiert, der dieses Symbol enthält.
* Im Konbinationsfeld "Aktuelles Symbol an Sprachausgabe senden" kann eingestellt werden, ob das Symbol anstelle seines Ersatztextes an die Sprachausgabe gesendet werden soll.
Dies ist nützlich, wenn das Symbol die Sprachausgabe zu einer Pause oder einer anderen Betonung bringen soll.
Beispielsweise pausiert die Sprachausgabe nach einem Komma.
Dieses Konbinationsfeld enthält drei Optionen:
  * Niemals: Das Sonderzeichen wird niemals an die Sprachausgabe gesendet.
  * Immer: Das Symbol wird immer an die Sprachausgabe gesendet.
  * Unterhalb der Symbolebene: Das Sonderzeichen wird nur an die Sprachausgabe gesendet, wenn die momentan eingestellte Symbolebene niedriger ist, als im Konbinationsfeld "Stufe" (siehe oben)
  Beispielsweise kann ein Symbol bei einer höheren Stufe ohne Pausieren gesprochen werden, während die Sprachausgabe bei einer niedrigeren Stufe pausiert.

Um Symbole hinzuzufügen, benutzen Sie den Schalter "Hinzufügen".
Geben Sie im erscheinenden Dialogfeld das Symbol ein und klicken Sie auf den Schalter "OK".
Ändern Sie anschließend die anderen Optionen nach Ihren Wünschen, wie Sie es bei den anderen Symbolen machen würden.

Über den Schalter "Entfernen" können Sie ein Symbol wieder löschen.

Wenn Sie die gewünschten Änderungen vorgenommen haben, bestätigen Sie die Änderungen mit "OK" oder verwerfen Sie diese mittels "Abbrechen".

Bei komplexen Symbolen muss das Feld Ersetzen möglicherweise einige Gruppenreferenzen des übereinstimmenden Textes enthalten. Beispielsweise müssten für ein Muster, das mit einem ganzen Datum übereinstimmt, \ 1, \ 2 und \ 3 im Feld angezeigt werden, um durch die entsprechenden Teile des Datums ersetzt zu werden.
Normale Backslashes im Feld "Ersetzen" sollten daher verdoppelt werden, z. "a \\ b" sollte eingegeben werden, um den Ersatz "a \ b" zu erhalten.

#### Tastenbefehle {#InputGestures}

In diesem Dialogfeld können Sie Tastenbefehle (Tastenkombinationen, Tasten an einer Braillezeile, Aktionen auf einem Touchscreen) an NVDA-Funktionen zuweisen.

Es werden nur unmittelbar Befehle angezeigt, die zugewiesen werden können.
Wenn Sie beispielsweise einen Befehl neu zuweisen möchten, der sich auf den Lesemodus bezieht, sollten Sie das Dialogfeld aufrufen, während Sie sich im Lesemodus befinden.

In diesem Dialogfeld werden alle verfügbaren NVDA-Funktionen in einer Baumansicht angezeigt, die nach Kategorien sortiert sind.
Über das Eingabefeld "filtern" können Sie die Liste der angezeigten Funktionen einschränken. Geben Sie dazu einen Teil des Funktionsnamens als Suchbegriff ein.
Unterhalb jeder Funktion werden die zugewiesenen Befehle, sofern vorhanden, angezeigt.

um einen Befehl einer Funktion zuzuweisen, wählen Sie die Funktion aus und klicken Sie auf den Schalter "Hinzufügen".
Führen Sie anschließend den zuzuweisenden Befehl durch - Drücken Sie die entsprechende Tastenkombination oder die Tasten an der Braillezeile.
Oft kann eine NVDA-Funktion durch mehr als eine Tastenkombination ausgeführt werden.
Bei Tastenkombinationen kann es beispielsweise sinnvoll sein, das Tastaturschema anzugeben, in dem diese Tastenkombination wirksam werden soll (Desktop/Laptop).
In solchen Fällen wird ein Menü angezeigt, in dem Sie die entsprechende Option auswählen können.

Um eine Tastenkombination von einer Funktion zu entfernen, wählen Sie diese aus und klicken Sie anschließend auf den Schalter "Entfernen".

Die Kategorie "Tasten der emulierten Systemtastatur" enthält NVDA-Befehle, die Tasten auf der Systemtastatur emulieren.
Diese Tasten der emulierten Systemtastatur können zur Steuerung einer Systemtastatur direkt von Ihrer Braillezeile aus verwendet werden.
Um einen emulierten Tastenbefehl hinzuzufügen, wählen Sie in der Kategorie "Tasten der emulierten Systemtastatur" und klicken Sie auf die Schaltfläche "Hinzufügen".
Anschließend drücken Sie die gewünschte, zu emulierende Taste auf der Tastatur.
Danach ist die Taste in der Kategorie "Tasten der emulierten Systemtastatur" verfügbar und Sie können ihr einen Tastenbefehl wie oben beschrieben zuweisen.

Hinweis:

* Emulierte Tasten müssen Tastenbefehlen zugewiesen sein, damit sie beim Speichern und Schließen des Dialogfeldes bestehen bleiben.
* Ein Tastenbefehl mit NVDA-Tasten kann möglicherweise nicht auf einen emulierten Tastenbefehl ohne NVDA-Tasten abgebildet werden.
Zum Beispiel kann das definieren der emulierten Eingabe "a" und das Konfigurieren des Tastenbefehls von "Strg+M" dazu führen,
dass die Anwendung "Strg+A" interpretieren könnte.

Um die Änderungen zu übernehmen, klicken Sie auf den Schalter "OK" oder auf "Abbrechen", um die Änderungen zu verwerfen.

### Konfiguration laden und speichern {#SavingAndReloading}

Standardmäßig speichert NVDA die Einstellungen automatisch beim Beenden.
Sie können dies jedoch im Einstellungsmenü in den Optionen "Allgemein" ändern.
Über "Konfiguration speichern" können Sie im NVDA-Menü die Konfiguration manuell speichern.

Im NVDA-Menü können Sie über den Eintrag "Auf gespeicherte Einstellungen zurücksetzen" diese wiederherstellen.
Wenn Sie die Konfiguration auf die Standard-Einstellungen zurücksetzen möchten, können Sie dies über den Menüpunkt "Auf Standard-Einstellungen zurücksetzen" im NVDA-Menü erreichen.

Die folgenden Tastenbefehle sind auch hilfreich:
<!-- KC:beginInclude -->

| Name |"Desktop"-Tastenkombination |"Laptop"-Tastenkombination |Beschreibung|
|---|---|---|---|
|Konfiguration speichern |NVDA+Strg+C |NVDA+Strg+C |Speichert die Konfiguration ab, sodass sie nicht beim Beenden von NVDA verloren geht.|
|Konfiguration zurücksetzen |NVDA+Strg+R |NVDA+Strg+R |Setzt bei einmal Drücken die NVDA-Einstellungen auf den letzten gespeicherten Stand zurück. Bei dreimal Drücken wird auf die Standard-Einstellung zurückgesetzt.|

<!-- KC:endInclude -->

### Konfigurationsprofile verwalten {#ConfigurationProfiles}

Manchmal möchten Sie unterschiedliche Einstellungen in unterschiedlichen Situationen verwenden.
Zum Korrekturlesen ist es sinnvoll, Einrückungen und Schriftattribute angesagt zu bekommen.
In NVDA können Sie dafür die Konfigurationsprofile verwenden.

Ein Konfigurationsprofil enthält nur die geänderten Einstellungen für das aktuelle Profil.
In Konfigurationsprofilen können die meisten Einstellungen geändert werden. Eine Ausnahme sind die Einstellungen aus der Kategorie "Allgemein" in den [NVDA-Einstellungen](#NVDASettings), da diese NVDA generell betreffen.

Konfigurationsprofile können entweder über einen Dialogfeld oder mit benutzerdefinierten Tastenkürzel manuell aktiviert werden.
Außerdem können Sie solche Profile auch automatisch aktivieren (beispielsweise beim Wechsel in eine bestimmte Anwendung).

#### Grundlegende Profilverwaltung {#ProfilesBasicManagement}

Konfigurationsprofile sind über den Menüpunkt "Konfigurationsprofile verwalten" im NVDA-Menü zu erreichen.
Dieses Dialogfeld ist auch über eine Tastenkombination erreichbar:
<!-- KC:beginInclude -->

* NVDA+Strg+P: Zeigt das Dialogfeld für die Konfigurationsprofile an.

<!-- KC:endInclude -->

Das erste Element in diesem Fenster ist die Profil-Liste, in der Sie eins aus den vorhandenen Profilen auswählen können.
Wenn Sie das Dialogfeld öffnen ist das aktive Profil ausgewählt.
Außerdem werden Ihnen noch zusätzliche Informationen angezeigt, wie z. B. die eingestellte Aktivierungsmethode (manuell oder per Trigger) oder der Bearbeitungsstatus.

Über die Schalter "Umbenennen" oder "Löschen" können Sie ein Profil umbenennen oder löschen.

Über den Schalter "Schließen" können Sie das Dialogfeld schließen.

#### Erstellen eines Konfigurationsprofils {#ProfilesCreating}

Um ein neues Profil zu erstellen, klicken Sie auf den Schalter "Neu".

Über das Dialogfeld können Sie einen Namen für das Profil vergeben.
Außerdem können Sie bestimmen, wie dieses Profil verwendet werden soll.
Wenn Sie vorhaben, das Profil manuell zu aktivieren, wählen Sie "Manuelle Aktivierung" aus.
Wählen Sie anderenfalls einen Trigger aus, durch den das Profil automatisch aktiviert werden soll.
Wenn Sie keinen Namen vergeben und einen Trigger auswählen, wird automatisch ein passender Name für das Profil eingetragen.
Weitere Informationen über die Funktion finden Sie im Abschnitt [Trigger bei Konfigurationsprofilen](#ConfigProfileTriggers).

Wenn Sie das Dialogfeld mit "OK" schließen, wird das Profil erstellt und das Dialogfeld "Konfigurationsprofile verwalten" geschlossen, sodass Sie das Profil bearbeiten können.

#### Manuelle Aktivierung {#ConfigProfileManual}

Sie können ein Konfigurationsprofil manuell aktivieren, indem Sie den Schalter "Manuell aktivieren" verwenden.
Wenn Sie einmal ein Profil manuell aktiviert haben, sind die Trigger für automatisch aktivierte Profile zwar weiterhin aktiv, Einstellungen in manuell aktivierten Profilen haben jedoch Vorrang.
Beispiel 1: Gegeben sei ein automatisch aktiviertes Profil für die aktuelle Anwendung, in dem die Ansage von Links aktiviert ist. Außerdem sei ein manuell aktiviertes Profil gegeben, in dem die Ansage von Links deaktiviert ist. In diesem Fall werden Links nicht angesagt.
Beispiel 2: Sie haben in einem automatisch aktivierten Profil für die aktuelle Anwendung die Stimmeneinstellungen geändert. In einem manuell aktivierten (und momentan aktiven) Profil haben Sie die Stimmeneinstellungen jedoch noch nie aufgerufen. In diesem Fall wird die Stimme ausgelöst durch das automatisch aktivierte Profil geändert.
Jegliche Einstellungen, die Sie ab sofort ändern, werden im manuell aktivierten Profil gespeichert.
Um ein manuell aktiviertes Profil wieder zu deaktivieren, klicken Sie auf den Schalter "Manuell deaktivieren".

#### Trigger bei Konfigurationsprofilen {#ConfigProfileTriggers}

Mit diesem Schalter können Sie einen Trigger bestimmen, über den ein Profil automatisch aktiviert werden soll.

Folgende Trigger stehen zur Verfügung:

* Aktuelle Anwendung; wird ausgelöst, wenn Sie in die aktuelle Anwendung wechseln
* Alles Lesen; wird ausgelöst, sobald Sie den Befehl "Alles Lesen" verwenden.

Um das Profil zu bestimmen, das durch einen bestimmten Trigger aktiviert werden soll, wählen Sie zunächst den Trigger und anschließend das Profil aus.
Wenn Sie nicht möchten, dass ein bestimmtes Profil ausgewählt wird, wählen Sie "Standardkonfiguration" aus.

Über den Schalter "Schließen" können Sie das Dialogfeld für das Konfigurationsprofil schließen.

#### Bearbeiten eines Konfigurationsprofils {#ConfigProfileEditing}

Wenn Sie ein Konfigurationsprofil manuell aktiviert haben, werden sämtliche Einstellungen in diesem Profil gespeichert.
Anderenfalls werden alle Einstellungen in jenem Profil gespeichert, das zuletzt durch einen Trigger aktiviert wurde.
Wenn Sie beispielsweise ein Profil für den Editor erstellt haben und sich momentan im Editor befinden, werden alle Einstellungen in diesem Profil gespeichert.
Wenn Sie weder ein manuell aktiviertes noch ein durch einen Trigger aktiviertes Profil erstellt haben, werden alle Einstellungen in der Standardkonfiguration gespeichert.

Um ein Profil zu bearbeiten, das an den Trigger "Alles Lesen" gekoppelt ist, müssen Sie dieses Profil zuvor [Manuell aktivieren](#ConfigProfileManual).

#### Trigger vorübergehend abschalten {#ConfigProfileDisablingTriggers}

Manchmal ist es hilfreich, temporär alle Trigger zu deaktivieren.
Ein Beispiel: Sie möchten ein manuell aktiviertes Profil bearbeiten oder die Standardkonfiguration bearbeiten, ohne von automatisch aktivierten Profilen gestört zu werden.
Dies erreichen Sie über die Option "Alle Trigger temporär deaktivieren" im Dialogfeld für die Konfigurationsprofile.

Sie können auch eine Tastenkombination dafür im Dialogfeld für die [Tastenbefehle](#InputGestures) definieren.

#### Aktivieren eines Profils mit Befehlen {#ConfigProfileGestures}

Für jedes Profil, das Sie hinzufügen, können Sie eine oder mehrere Befehle zuweisen, um es zu aktivieren.
Standardmäßig sind den Konfigurationsprofilen keine Befehle zugeordnet.
Sie können Tastenbefehle für ein Profil im Dialogfeld für die [Tastenbefehle](#InputGestures) definieren.
Jedes Profil hat einen eigenen Eintrag unter der Kategorie Konfigurationsprofile.
Wenn Sie ein Profil umbenennen, ist jeder Tastenbefehl, die Sie zuvor hinzugefügt haben, weiterhin verfügbar.
Das Entfernen eines Profils löscht automatisch die damit verbundenen Tastenbefehlen.

### Speicherorte für Konfigurationsdateien {#LocationOfConfigurationFiles}

In der portablen NVDA-Version werden sämtliche Einstellungen und NVDA-Erweiterungen im Ordner "userConfig" unterhalb des Stammordners von NVDA abgelegt.

Bei den installierten NVDA-Versionen werden sämtliche Einstellungen und NVDA-Erweiterungen in einem speziellen Ordner in dem Ordner des angemeldeten Benutzers in dessen Windows-Profil abgelegt.
Dies bedeutet, dass jeder Benutzer im System so seine individuellen Einstellungen verwalten kann.
Um das Einstellungs-Verzeichnis von überall her zu öffnen, können Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden, um dieser Funktion eine Taste zuzuordnen.
Zusätzlich können Sie bei einer installierten Version von NVDA im Startmenü zu auf "Programme -> NVDA -> Benutzerkonfigurationsverzeichnis öffnen" gehen.

Die Einstellungen von NVDA für das Anmeldefenster und die Sicherheitsmeldungen der Benutzerkontensteuerung werden im Ordner "systemConfig" im Installationsordner von NVDA abgelegt.
Für gewöhnlich sollte diese Konfiguration unberührt bleiben!
Um die Konfiguration von NVDA während der Anmeldung oder bei Sicherheitsmeldungen zu ändern, konfigurieren Sie NVDA wie gewünscht, während Sie bei Windows angemeldet sind, speichern Sie die Konfiguration und betätigen Sie dann den Schalter "Aktuell gespeicherte Einstellungen während der Anmeldung und bei Sicherheitsmeldungen verwenden" in der Kategorie "Allgemein" der [NVDA-Einstellungen](#NVDASettings).

## NVDA-Erweiterungen und der Store für NVDA-Erweiterungen {#AddonsManager}

NVDA-Erweiterungen sind Software-Pakete, die neue oder geänderte Funktionen für NVDA bereitstellen.
Sie werden von der NVDA-Community und externen Organisationen wie kommerziellen Anbietern entwickelt.
NVDA-Erweiterungen können eine der folgenden Funktionen haben:

* Hinzufügen oder Verbessern der Unterstützung für bestimmte Anwendungen.
* Unterstützung für zusätzliche Braillezeilen oder Sprachausgaben.
* Hinzufügen oder Ändern von Funktionen in NVDA.

Mit dem Store für NVDA-Erweiterungen können Sie Erweiterungspakete durchsuchen und verwalten.
Alle NVDA-Erweiterungen, die im Store für NVDA-Erweiterungen verfügbar sind, können kostenlos heruntergeladen werden.
Einige davon erfordern jedoch, dass die Benutzer für eine Lizenz oder zusätzliche Software bezahlen, bevor sie verwendet werden können.
Kommerzielle Sprachausgaben sind ein Beispiel für diese Art von NVDA-Erweiterungen.
Wenn Sie eine NVDA-Erweiterung mit kostenpflichtigen Komponenten installieren und es dann doch nicht mehr verwenden möchten, kann die NVDA-Erweiterung problemlos entfernt werden.

Der Zugriff auf den Store für NVDA-Erweiterungen erfolgt über das Untermenü Werkzeuge des NVDA-Menüs.
Um von überall aus auf den Store für NVDA-Erweiterungen zuzugreifen, weisen Sie einen benutzerdefinierten Tastenbefehl zu, indem Sie das Dialogfeld für die [Tastenbefehle](#InputGestures) verwenden.

### NVDA-Erweiterungen durchsuchen {#AddonStoreBrowsing}

Wenn Sie den Store für NVDA-Erweiterungen öffnen, wird eine Liste von NVDA-Erweiterungen angezeigt.
Wenn Sie noch keine NVDA-Erweiterung installiert haben, öffnet sich der Store für NVDA-Erweiterungen mit einer Liste von NVDA-Erweiterungen, die Sie installieren können.
Wenn Sie NVDA-Erweiterungen installiert haben, zeigt die Liste die derzeit installierten NVDA-Erweiterungen an.

Wenn Sie eine NVDA-Erweiterung auswählen, indem Sie es mit den Pfeiltasten nach oben oder unten ansteuern, werden die Details der NVDA-Erweiterung angezeigt.
NVDA-Erweiterungen haben zugehörige Aktionen, auf die Sie über ein [Aktionsmenü](#AddonStoreActions) zugreifen können, wie z. B. Installieren, Hilfe, Deaktivieren und Entfernen.
Die verfügbaren Aktionen hängen davon ab, ob die NVDA-Erweiterung installiert ist oder nicht, und ob es aktiviert oder deaktiviert ist.

#### Listenansichten der NVDA-Erweiterungen {#AddonStoreFilterStatus}

Es gibt verschiedene Ansichten für installierte, zu aktualisierende, verfügbare und inkompatible NVDA-Erweiterungen.
Um die Ansicht der NVDA-Erweiterungen zu ändern, wechseln Sie die aktive Registerkarte der Liste der NVDA-Erweiterungen mit `Strg+Tab`.
Sie können auch mit der `Tab`-Taste bis zur Liste der Ansichten wandern und sich mit den `Pfeiltaste nach links` und `Pfeiltaste nach rechts` durch diese navigieren.

#### Aktivierte oder deaktivierte NVDA-Erweiterungen filtern {#AddonStoreFilterEnabled}

Normalerweise ist ein installiertes NVDA-Erweiterung "aktiviert", d. h., es wird ausgeführt und ist in NVDA verfügbar.
Es kann jedoch sein, dass einige der installierten NVDA-Erweiterungen auf den Status "deaktiviert" haben.
Das bedeutet, dass sie nicht verwendet werden und ihre Funktionen während der aktuellen NVDA-Sitzung nicht zur Verfügung stehen.
Möglicherweise haben Sie eine NVDA-Erweiterung deaktiviert, weil es mit einer anderen oder mit einer bestimmten Anwendung in Konflikt stand.
NVDA kann auch bestimmte NVDA-Erweiterungen selbstständig deaktivieren, wenn diese während einer NVDA-Aktualisierung für inkompatibel befunden werden; Sie werden jedoch davor gewarnt, wenn dies vorkommen sollte.
NVDA-Erweiterungen können auch deaktiviert werden, wenn Sie sie über einen längeren Zeitraum nicht benötigen, sie aber nicht deinstallieren möchten, weil Sie sie in Zukunft wieder benötigen könnten.

Die Liste der installierten und inkompatiblen NVDA-Erweiterungen können nach ihrem aktivierten oder deaktivierten Status gefiltert werden.
In der Standard-Einstellung werden sowohl aktivierte als auch deaktivierte NVDA-Erweiterungen angezeigt.

#### Inkompatible NVDA-Erweiterungen filtern {#AddonStoreFilterIncompatible}

Verfügbare und zu aktualisierende NVDA-Erweiterungen können gefiltert werden, um [inkompatible NVDA-Erweiterungen](#incompatibleAddonsManager) einzuschließen, die zur Installation verfügbar sind.

#### NVDA-Erweiterungen nach Kanal filtern {#AddonStoreFilterChannel}

NVDA-Erweiterungen können über bis zu vier Kanäle verteilt werden:

* Stabil: Der Entwickler hat dies als getestete NVDA-Erweiterung mit einer freigegebenen Version von NVDA veröffentlicht.
* Beta: Diese NVDA-Erweiterung muss möglicherweise noch weiter getestet werden, ist aber für Benutzer-Feedback freigegeben.
Empfohlen für Tester:
* Dev: Dieser Kanal ist für Entwickler von NVDA-Erweiterungen gedacht, um noch nicht freigegebene API-Änderungen zu testen.
Die NVDA-Alpha-Tester müssen möglicherweise eine "Dev"-Version ihrer NVDA-Erweiterungen verwenden.
* Extern: NVDA-Erweiterungen, die aus externen Quellen außerhalb des Stores für NVDA-Erweiterungen installiert wurden.

Um NVDA-Erweiterungen nur für bestimmte Kanäle aufzulisten, ändern Sie die Filter-Auswahl "Kanal".

#### Nach NVDA-Erweiterungen suchen {#AddonStoreFilterSearch}

Verwenden Sie für die Suche nach NVDA-Erweiterungen das Textfeld "Suchen".
Sie erreichen es durch Drücken der Tastenkombination `Umschalt+Tab` in der Liste der NVDA-Erweiterungen.
Geben Sie ein oder zwei Schlüsselwörter für die Art der NVDA-Erweiterung ein, die Sie suchen, und betätigen Sie dann die `Tab`-Taste, bis Sie in der Liste der NVDA-Erweiterungen gelangen.
Die NVDA-Erweiterungen werden aufgelistet, wenn der Suchtext im Anzeigenamen, im Herausgeber oder in der Beschreibung auffindbar ist.

### Aktionen für NVDA-Erweiterungen {#AddonStoreActions}

Für NVDA-Erweiterungen stehen Aktionen wie Installieren, Hilfe, Deaktivieren und Entfernen zur Verfügung.
Für eine NVDA-Erweiterung in der Liste der NVDA-Erweiterungen können diese Aktionen über ein Menü aufgerufen werden, das durch Drücken der `Kontextmenü`-Taste, `Eingabetaste`, Rechtsklick oder Doppelklick auf die NVDA-Erweiterung geöffnet wird.
Dieses Menü kann auch über eine Schaltfläche "Aktionen" in den Details der ausgewählten NVDA-Erweiterung aufgerufen werden.

#### NVDA-Erweiterungen installieren {#AddonStoreInstalling}

Nur weil eine NVDA-Erweiterung im Store für NVDA-Erweiterungen verfügbar ist, bedeutet dies nicht, dass es von NV Access oder einer anderen Stelle genehmigt oder geprüft wurde.
Es ist sehr wichtig, dass Sie nur NVDA-Erweiterungen aus offiziellen Quellen installieren, denen Sie auch wirklich vertrauen.
Die Funktionalität von NVDA-Erweiterungen ist innerhalb von NVDA nicht eingeschränkt.
Dies könnte den Zugriff auf Ihre persönlichen Daten oder sogar auf das gesamte System beinhalten.

Sie können NVDA-Erweiterungen installieren und aktualisieren, indem Sie [Verfügbare NVDA-Erweiterungen durchsuchen](#AddonStoreBrowsing).
Wählen Sie eine NVDA-Erweiterung auf der Registerkarte "Verfügbare NVDA-Erweiterungen" oder "Zu aktualisierende NVDA-Erweiterungen" aus.
Starten Sie dann die Installation mit der Aktion "Aktualisieren", "Installieren" oder "Ersetzen".

Sie können auch mehrere Erweiterungen gleichzeitig installieren.
Dies kann erreicht werden, indem Sie auf der Registerkarte "Verfügbare Erweiterungen" mehrere Erweiterungen auswählen, dann das Kontextmenü der Auswahl aktivieren und die Aktion "Ausgewählte Erweiterungen installieren" auswählen.

Um eine NVDA-Erweiterung zu installieren, die Sie außerhalb des Store geladen haben, klicken Sie auf die Schaltfläche "Aus externer Quelle installieren".
Damit können Sie nach einem Erweiterungspaket (`.nvda-addon`-Datei) irgendwo auf Ihrem Computer oder in einem Netzwerk suchen.
Sobald Sie das Erweiterungspaket angeklickt haben, beginnt der Installationsprozess.

Wenn NVDA auf Ihrem System installiert ist und läuft, können Sie diese Datei auch direkt über den Browser oder das Datei-System öffnen, um den Installationsvorgang zu starten.

Wenn eine NVDA-Erweiterung aus einer externen Quelle installiert werden soll, werden Sie von NVDA aufgefordert, diese Installation zu bestätigen.
Nach der Installation der NVDA-Erweiterung muss NVDA neu gestartet werden, damit die NVDA-Erweiterung ausgeführt werden kann. Sie können den Neustart von NVDA jedoch verschieben, wenn Sie weitere NVDA-Erweiterungen installieren oder aktualisieren möchten.

#### NVDA-Erweiterungen entfernen {#AddonStoreRemoving}

Um eine NVDA-Erweiterung zu entfernen, wählen Sie sie aus der Liste aus und verwenden Sie die Aktion "Entfernen".
Von NVDA werden Sie aufgefordert, die Entfernung zu bestätigen.
Wie bei der Installation muss NVDA neu gestartet werden, damit die NVDA-Erweiterung vollständig entfernt wird.
Solange Sie dies nicht tun, wird für diese NVDA-Erweiterung in der Liste der Status "Zur Entfernung ausstehend" angezeigt.
Wie bei der Installation können Sie auch mehrere Erweiterungen gleichzeitig entfernen.

#### NVDA-Erweiterungen ein- oder ausschalten {#AddonStoreDisablingEnabling}

Um eine NVDA-Erweiterung zu deaktivieren, verwenden Sie die Aktion "Deaktivieren".
Um eine zuvor deaktivierte NVDA-Erweiterung zu aktivieren, verwenden Sie die Aktion "Aktivieren".
Sie können eine NVDA-Erweiterung deaktivieren, wenn der Status der NVDA-Erweiterung "Aktiviert" anzeigt oder es aktivieren, wenn die NVDA-Erweiterung den Status "Deaktiviert" hat.
Bei jeder Verwendung der Aktion "Aktivieren/Deaktivieren" ändert sich der Status der NVDA-Erweiterung, um anzuzeigen, was beim Neustart von NVDA passieren wird.
Hatte die NVDA-Erweiterung zuvor den Status "Deaktiviert", wird der Status "Nach Neustart aktiviert" angezeigt.
Hatte die NVDA-Erweiterung zuvor den Status "Aktiviert", wird der Status auf "Nach Neustart deaktiviert" gesetzt.
Genau wie beim Installieren oder Entfernen von NVDA-Erweiterungen müssen Sie NVDA neu starten, damit die Änderungen wirksam werden.
Sie können auch mehrere Erweiterungen gleichzeitig aktivieren oder deaktivieren, indem Sie auf der Registerkarte "Verfügbare Erweiterungen" mehrere Erweiterungen auswählen, dann das Kontextmenü der Auswahl aktivieren und die entsprechende Aktion auswählen.

#### Erweiterungen bewerten und Lesen von Rezensionen {#AddonStoreReviews}

Vielleicht möchten Sie Bewertungen von anderen Nutzern lesen, die bereits Erfahrungen mit einer NVDA-Erweiterung gemacht haben, z. B. bevor Sie es installieren oder während Sie lernen, diese zu benutzen.
Außerdem ist es für andere Nutzer hilfreich, wenn Sie uns Feedback zu den von Ihnen ausprobierten NVDA-Erweiterungen geben.
Um Bewertungen für eine NVDA-Erweiterung zu lesen, wählen Sie sie aus und verwenden Sie die Aktion "Community-Bewertungen".
Dies führt zu einer GitHub-Diskussionsseite, auf der Sie Rezensionen für die Erweiterung lesen und schreiben können.
Bitte beachten Sie, dass dies nicht die direkte Kommunikation mit Erweiterungs-Entwicklern ersetzt.
Stattdessen besteht der Zweck dieser Funktion darin, Feedback zu teilen, um Benutzern bei der Entscheidung zu helfen, ob eine Erweiterung für sie nützlich sein könnte.

### Inkompatible NVDA-Erweiterungen {#incompatibleAddonsManager}

Einige ältere NVDA-Erweiterungen sind möglicherweise nicht mehr mit der verwendeten NVDA-Version kompatibel.
Wenn Sie eine ältere NVDA-Version verwenden, sind möglicherweise auch einige neuere NVDA-Erweiterungen nicht kompatibel.
Wenn Sie versuchen, eine inkompatible NVDA-Erweiterung zu installieren, erhalten Sie eine Fehlermeldung darüber, warum sie als inkompatibel gilt.

Bei älteren NVDA-Erweiterungen können Sie die Inkompatibilität auf eigene Gefahr hin aufheben.
Inkompatible NVDA-Erweiterungen funktionieren möglicherweise nicht mit Ihrer NVDA-Version und können zu instabilem oder unerwartetem Verhalten, einschließlich Abstürzen, führen.
Sie können die Kompatibilität außer Kraft setzen, wenn Sie eine NVDA-Erweiterung aktivieren oder installieren.
Wenn die inkompatible NVDA-Erweiterung später Probleme verursacht, können Sie sie deaktivieren oder entfernen.

Wenn Sie Probleme mit NVDA haben und vor kurzem eine NVDA-Erweiterung aktualisiert oder installiert haben, insbesondere wenn es sich um eine inkompatibles NVDA-Erweiterung handelt, sollten Sie versuchen, NVDA vorübergehend mit deaktivierten NVDA-Erweiterungen zu starten.
Um NVDA mit deaktivierten NVDA-Erweiterungen neu zu starten, wählen Sie die entsprechende Option beim Beenden von NVDA aus.
Alternativ können Sie auch die [Kommandozeilenoption](#CommandLineOptions) `--disable-addons` verwenden.

Sie können die verfügbaren inkompatiblen NVDA-Erweiterungen mit Hilfe der Registerkarte [verfügbare und zu aktualisierende NVDA-Erweiterungen](#AddonStoreFilterStatus) durchsuchen.
Sie können die installierten inkompatiblen NVDA-Erweiterungen über die Registerkarte [Inkompatible NVDA-Erweiterungen](#AddonStoreFilterStatus) durchsuchen.

## Werkzeuge {#ExtraTools}
### Protokoll-Betrachter {#LogViewer}

Den Protokoll-Betrachter finden Sie im NVDA-Menü unter "Werkzeuge". Dieses Werkzeug gibt Ihnen die Möglichkeit, alles was seit dem Start von NVDA intern abläuft, einzusehen.

Neben dem Lesen des Inhalts können Sie auch eine Kopie der Protokolldatei speichern oder den Betrachter aktualisieren, um neue Protokollausgaben zu laden, die nach dem Öffnen des Protokollbetrachters generiert wurden.
Diese Aktionen sind im Menü Protokoll im Protokoll-Betrachter verfügbar.

Beim öffnen des Protokollbetrachters wird die angezeigte Datei am Dateispeicherort "%temp%\nvda.log" gespeichert.
Bei jedem Start von NVDA wird eine neue Protokolldatei erstellt.
In diesem Fall wird die Protokolldatei der vorherigen NVDA-Sitzung nach „%temp%\nvda-old.log“ verschoben.

Sie können auch nur einen Teil der aktuellen Protokolldatei in die Zwischenablage kopieren, ohne den Protokoll-Betrachter zu öffnen.
<!-- KC:beginInclude -->

| Name |Tastenkombination |Beschreibung|
|---|---|---|
|Protokoll-Betrachter öffnen |`NVDA+f1` |Öffnet den Protokoll-Betrachter und zeigt Entwicklerinformationen zum aktuellen Navigatorobjekt an.|
|Teil des Protokolls in die Zwischenablage kopieren |`NVDA+control+Umschalt+f1` |Wenn dieser Befehl einmal gedrückt wird, wird ein Startpunkt zum erfassen des Protokollinhalts festgelegt. Wenn Sie  die Tastenkombination ein zweites Mal drücken, wird der Protokollinhalt seit dem Startpunkt in Ihre Zwischenablage kopiert.|

<!-- KC:endInclude -->

### Sprachausgaben-Betrachter {#SpeechViewer}

Für sehende Softwareentwickler oder für diejenigen, die NVDA anderen Sehenden vorführen möchten, ist ein freischwebendes Fenster verfügbar, dass Ihnen anzeigt, was alles von NVDA gegenwärtig gesprochen wird.

Um den Sprachausgaben-Betrachter einzuschalten, aktivieren Sie den Eintrag "Sprachausgaben-Betrachter", welchen Sie im Untermenü "Werkzeuge" im NVDA-Menü finden.
Deaktivieren Sie den Menüpunkt, um ihn wieder auszuschalten.

Das Fenster des Sprachausgaben-Betrachters enthält das Kontrollkästchen "Sprachausgaben-Betrachter beim Starten anzeigen".
Wenn dieses Kontrollkästchen aktiviert ist, wird der Sprachausgaben-Betrachter geöffnet, sobald NVDA gestartet wird.
Sofern möglich, wird dessen Fenster dieselbe Position sowie die gleiche Größe wie bei der letzten Verwendung einnehmen.

Während der Sprachausgaben-Betrachter eingeschaltet ist, aktualisiert sich sogleich der Text beim Sprechen.
Wenn Sie jedoch mit der Maus über den Betrachter fahren oder den Fokus darauf setzen, unterbricht NVDA augenblicklich die weitere Aktualisierung des vorgelesenen Textes, sodass Sie nun die entsprechenden Einträge markieren und in die Zwischenablage kopieren können.

Um den Sprachausgaben-Betrachter per Tastenkombination ein- oder auszuschalten, müssen Sie über das Dialogfeld für die [Tastenbefehle](#InputGestures) eine eigene Tastenkombination zuweisen.

### Braille-Betrachter {#BrailleViewer}

Für sehende Software-Entwickler oder Personen, die NVDA für ein sehendes Publikum demonstrieren, steht ein schwebendes Fenster zur Verfügung, mit dem Sie die Braille-Ausgabe und das Textäquivalent für jede Braillezeile anzeigen können.
Der Braille-Betrachter kann gleichzeitig mit einer physischen Braillezeile verwendet werden, dieser entspricht der Anzahl der Module auf dem physischen Gerät.
Während der Braille-Betrachter läuft, wird die Anzeige ständig mit der Darstellung auf der Braillezeile synchronisiert.

Um den Braille-Betrachter zu aktivieren, wählen Sie im NVDA-Menü unter "Werkzeuge" den Menüpunkt "Braille-Betrachter" aus.
Deaktivieren Sie den Menüpunkt wieder, um ihn zu deaktivieren.

Braillezeilen haben typischerweise Tasten zum Vorwärts- oder Rückwärtsnavigieren. Um das Scrollen mit dem Braille-Betrachter zu ermöglichen, verwenden Sie das Dialogfeld für die [Tastenbefehle](#InputGestures), um Tastenkombinationen zuzuweisen, welche die "Braillezeile rückwärtsnavigieren" und "Braillezeile vorwärtsnavigieren" simulieren.

Das Fenster des Braille-Betrachters enthält ein Kontrollkästchen mit der Bezeichnung "Braille-Betrachter beim Starten anzeigen".
Wenn dies aktiviert ist, öffnet sich der Braille-Betrachter beim Starten von NVDA.
Sofern möglich, wird dessen Fenster dieselbe Position sowie die gleiche Größe wie bei der letzten Verwendung einnehmen.

Der Braille-Betrachter enthält ein Kontrollkästchen mit der Bezeichnung "Schweben für Zell-Routing", der standardmäßig deaktiviert ist.
Wenn diese Option aktiviert ist, wird durch Bewegen der Maus über eine Braillezelle der Befehl "Route zur Braillezelle" für diese Zelle ausgelöst.
Das wird häufig verwendet, um den System-Cursor zu bewegen oder die Aktion für eine Steuerung auszulösen.
Dies kann zum Testen nützlich sein. NVDA kann die Zuordnung einer Braillezelle korrekt umkehren.
Um ein unbeabsichtigtes Weiterleiten an Zellen zu verhindern, wird der Befehl verzögert.
Die Mauszeiger muss schweben, bis die Zelle grün wird.
Die Zelle beginnt hellgelb, geht in orange über und wird plötzlich grün.

Um den Braille-Betrachter von einer beliebigen Stelle aus umzuschalten, weisen Sie bitte einen benutzerdefinierten Tastenbefehl zu, indem Sie das [Dialogfeld für die Tastenbefehle](#InputGestures) verwenden.

### Python-Konsole {#PythonConsole}

Die Python-Konsole in NVDA, zu finden im Menü "Werkzeuge" im NVDA-Menü, ist ein Entwicklungswerkzeug, das für das Debugging, die allgemeine Inspektion von NVDA-Interna oder die Inspektion der Zugänglichkeitshierarchie einer Anwendung nützlich ist.
Weitere Informationen finden Sie im [NVDA-Entwicklerhandbuch](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Store für NVDA-Erweiterungen {#toc312}

Dadurch wird der [Store für NVDA-Erweiterungen](#AddonsManager) geöffnet.
Für weitere Informationen lesen Sie bitte den ausführlichen Abschnitt: [NVDA-Erweiterungen und der Store für NVDA-Erweiterungen](#AddonsManager).

### Eine portable Version erstellen {#CreatePortableCopy}

Mit dieser Option können Sie eine portable Version aus einer installierten Version erstellen.
Wird die portable Version ausgeführt, erscheint an der gleichen Stelle im Menü "Extras" stattdessen der Eintrag "NVDA auf diesem Computer installieren".

In diesem Dialogfeld werden Sie zur Auswahl des jeweiligen Zielpfads aufgewfordert den Pfad für die portable bzw. für die installierte Version auszuwählen.

In diesem Dialogfeld können Sie Folgendes aktivieren oder deaktivieren:

* Kopieren der aktuellen Benutzerkonfiguration (inklusive der Dateien in "%appdata%\roaming\NVDA" oder in der Benutzerkonfiguration Ihrer portablen Version und NVDA-Erweiterungen oder der Module).
* Starten Sie die neue portable Version nach der Erstellung oder starten Sie NVDA nach der Installation (NVDA startet automatisch nach der Erstellung der portablen Version oder der Installation).

### Behebungstool für die COM-Registrierung ausführen {#RunCOMRegistrationFixingTool}

Das Installieren und Deinstallieren von Programmen auf einem Computer kann in bestimmten Fällen dazu führen, dass COM-DLL-Dateien nicht mehr registriert sind.
Da COM-Schnittstellen wie IAccessible von korrekten COM-DLL-Registrierungen abhängig sind, können Probleme auftreten, sobald diese fehlen.

Dies kann z. B. nach einer Installation und anschließender Deinstallation von Adobe Reader, MathPlayer und anderen Programmen vorkommen.

Die fehlende Registrierung kann zu Problemen in Browsern, Desktop-Anwendungen, der Taskleiste und anderen Schnittstellen führen.

Im Einzelnen können folgende Probleme durch den Einsatz dieses Tools gelöst werden:

* NVDA meldet beim Navigieren in Firefox, Thunderbird, etc. anstelle "Unbekannt".
* In NVDA funktioniert das Umschalten zwischen dem Fokus- und dem Lesemodus nicht mehr richtig.
* NVDA reagiert sehr langsam beim Navigieren im Lesemodus in Web-Browsern.
* Und möglicherweise andere Probleme.

### Plugins erneut laden {#ReloadPlugins}

Dieser Eintrag lädt alle Anwendungsmodule sowie globale Plugins neu, ohne dass NVDA extra neu gestartet wird.
Anwendungsmodule verwalten, wie NVDA mit bestimmten Anwendungen interagiert.
Globale Plugins verwalten, wie NVDA mit allen Anwendungen interagiert.

Die folgenden NVDA-Befehle können ebenfalls nützlich sein:
<!-- KC:beginInclude -->

| Name |Tastenkombinationen |Beschreibung|
|---|---|---|
|Plugins neu laden |`NVDA+control+f3` |Lädt die globalen Plugins und Anwendungsmodule von NVDA neu.|
|Geladenes Anwendungsmodul und Programm ausgeben |`NVDA+control+f1` |Gibt (falls vorhanden) den Namen des Anwendungsmoduls sowie den Namen der ausführbaren Datei aus, die fokusierten der Anwendung zugeordnet ist.|

<!-- KC:endInclude -->

## Unterstützte Sprachausgaben {#SupportedSpeechSynths}

Dieser Bereich beinhaltet Informationen über die in NVDA unterstützten Sprachausgaben.
Eine ausführliche Liste freier und kommerzieller Sprachausgaben, die zusammen mit NVDA verwendet werden können, finden Sie unter [https://github.com/nvaccess/nvda/wiki/ExtraVoices].

### eSpeak NG {#eSpeakNG}

Die in NVDA integrierte Sprachausgabe [eSpeak NG](https://github.com/espeak-ng/espeak-ng) benötigt keine speziellen Treiber oder andere extra installierten Komponenten.
Die Sprachausgabe eSpeak wird unter Windows 8.1 von NVDA standardmäßig verwendet, während unter Windows 10 und neuer [Windows OneCore](#OneCore) standardmäßig verwendet wird.
Das hat den enormen Vorteil, dass NVDA auf einen Betriebssystemen mit einem USB-Stick ohne weiteres betrieben werden kann.

Jede Stimme, die mit eSpeak NG ausgeliefert wird, spricht eine andere Sprache.
Somit werden über 43 unterschiedliche Sprachen unterstützt.

Es gibt auch eine Vielzahl von Varianten, womit der Klang der Stimme geändert werden kann.

### Microsoft Speech API-Version 4 (SAPI 4.0) {#SAPI4}

SAPI 4 ist ein älterer Microsoft-Standard für SoftwareSprachausgaben.
NVDA unterstützt noch die alte Schnittstelle, für all jene, die bereits SAPI 4 Sprachausgaben installiert haben.
Die Treiber hierfür werden von Microsoft schon lange nicht mehr zum Download angeboten.

Wenn diese Sprachausgabe mit NVDA verwendet wird, finden Sie die Stimmen aller SAPI 4 Engines in der Kategorie [Stimme und Sprachausgabe](#SpeechSettings) oder im [Sprachausgaben-Einstellungsring](#SynthSettingsRing).

### Microsoft Speech API-Version 5 (SAPI 5.x) {#SAPI5}

SAPI 5 ist ein Microsoft-Standard für SoftwareSprachausgaben.
Viele Sprachausgaben, die diesem Standard entsprechen, können von verschiedenen Firmen käuflich erworben oder von Internetseiten kostenlos heruntergeladen werden. Ihr System wird wahrscheinlich bereits mindestens eine SAPI5-Stimme vorinstalliert haben.
Wenn Sie diese Sprachausgaben mit NVDA benutzen möchten, werden in der Kategorie [Stimme und Sprachausgabe](#SpeechSettings) oder dem [Einstellungsring der Sprachausgaben](#SynthSettingsRing) alle Stimmen von der SAPI5-Engine aufgelistet, die auf Ihrem System gefunden werden können.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Die "Microsoft Speech Platform" stellt Stimmen für viele Sprachen zur Verfügung, welche normalerweise in der Entwicklung für serverbasierte Sprachanwendungen zum Einsatz kommen.
Diese Stimmen können auch in NVDA eingebunden werden.

Um diese Stimmen verwenden zu können, müssen Sie folgende 2 Komponenten installieren:

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Diese Internetseite enthält viele Dateien für Sprachein- und -ausgabe.
  Suchen Sie sich die TTS-Dateien passend zu der von Ihnen gewünschten Sprache heraus.
  Beispiel: Die Datei MSSpeech_TTS_de-DE_Hedda.msi ist eine deutsche Stimme.

### Stimmen für Windows-OneCore {#OneCore}

Windows 10 und neuer enthält Stimmen, die als "Mobile" oder "OneCore" allgemein hin bekannt sind.
Diese Stimmen sind in vielen Sprachen verfügbar. Sie sind außerdem sehr viel reaktionsfreudiger als die Microsoft SAPI 5-Stimmen in früheren Windows-Versionen.
Unter Windows 10 und neuer verwendet NVDA standardmäßig Windows OneCore-Stimmen ([eSpeak-NG](#eSpeakNG) wird in anderen Windows-Versionen, wie z. B. Windows 7 oder 8 bzw. 8.1, verwendet).

Um neue Stimmen für Windows-OneCore hinzuzufügen, gehen Sie in die Windows-Einstellungen und dort zu den Sprach-Einstellungen.
Verwenden Sie die Option "Stimmen hinzufügen" und suchen Sie die gewünschte Sprache aus.
Viele Sprachen enthalten mehrere Varianten.
Zwei der englischen Varianten sind "Großbritannien" und "Australien".
In französischer Variante sind "Frankreich", "Kanada" und "Schweiz" erhältlich.
Suchen Sie nach der breiteren Sprache (z. B. Englisch oder Französisch) und wählen Sie die entsprechende Variante in der Liste aus.
Anschließend wählen Sie die gewünschte Sprache aus und fügen Sie sie über die Schaltfläche "Hinzufügen" dem Betriebssystem hinzu.
Starten Sie NVDA nach dem Hinzufügen neu.

In Artikel [Unterstützte Sprachen und Stimmen](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) finden Sie eine Liste aller verfügbaren Stimmen.

## Unterstützte Braillezeilen {#SupportedBrailleDisplays}

Dieser Bereich beinhaltet Informationen über Braillezeilen, die mit NVDA betrieben werden können.

### Braillezeilen mit automatischer Erkennung im Hintergrund {#AutomaticDetection}

NVDA ermöglicht, viele Braillezeilen im Hintergrund automatisch zu erkennen, entweder über USB oder Bluetooth.
Dieses Verhalten wird durch die Auswahl der Option "Automatisch als bevorzugte Braillezeile" in den [Braille-Einstellungen](#BrailleSettings) erreicht.
Standardmäßig ist diese Option aktiviert.

Die folgenden Braillezeilen unterstützen diese automatische Erkennung.

* Braillezeilen von HandyTech
* Braillezeilen von Baum/VisioBraille, Humanware, APH, Orbit
* Humanware Brailliant-Serien BI/B
* Humanware BrailleNote
* SuperBraille
* Optelec-Serien ALVA 6
* HIMS-Serien Braille Sense, Braille EDGE, Smart Beetle, Sync Braille
* Braillezeilen von EuroBraille Esys, Esytime, Iris
* Braillezeilen von Nattiq nBraille
* Seika Notetaker: MiniSeika (mit 16 und 24 Modulen), V6 und V6Pro (mit 40 Modulen)
* Tivomatic Caiku Albatross mit 46 bzw. 80 Modulen
* Jede Braillezeile, welches das Standard-HID-Braille-Protokoll unterstützt

### Die Focus und PAC Mate von Freedom Scientific {#FreedomScientificFocus}

Die Braillezeilen Focus 40 Blue und alle PAC Mate von der amerikanischen Firma [Freedom Scientific](https://www.freedomscientific.com/) werden unterstützt.
Die Treiber für die Braillezeilen von Freedom Scientific können bei Bedarf auf Ihrem System vorab installiert sein. Diese sind aber nicht mehr Voraussetzung.
Falls diese noch nicht installiert wurden, können Sie die Treiber von der Seite [Focus Blue Braillezeilentreiber](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver) herunterladen.
Obwohl auf dieser Seite nur Treiber für die Focus 40 Blue aufgeführt sind, werden die Treiber für alle Braillezeilen gleichermaßen von Freedom Scientific unterstützt.

Für gewöhnlich kann NVDA den verwendeten Anschluss automatisch erkennen, gleichgültig ob die Braillezeile via USB oder Bluetooth verbunden ist.
Beim Konfigurieren der Braillezeile können Sie jedoch die Verbindungsart ausdrücklich festlegen, indem Sie für den Anschluss entweder USB oder Bluetooth auswählen.
Dies kann sinnvoll sein, wenn Sie z. B. eine Focus-Braillezeile per Bluetooth mit NVDA verbinden wollen, aber dennoch den USB-Anschluss Ihres Rechners zum Laden der Zeile verwenden.
Die automatische Braillezeilenerkennung von NVDA erkennt auch die Anzeige auf USB oder Bluetooth.

Folgende Tastenkombinationen bei dieser Braillezeile sind für NVDA zugeordnet.
Bitte lesen Sie in der Dokumentation der Braillezeile für weitere Informationen.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |topRouting1 (Erstes Braille-Modul)|
|Auf der Braillezeile vorwärts navigieren |topRouting20/40/80 (Letztes Braille-Modul)|
|Auf der Braillezeile rückwärts navigieren |leftAdvanceBar|
|Auf der Braillezeile vorwärts navigieren |rightAdvanceBar|
|Kopplung der Braille-Anzeige umschalten |leftGDFButton+rightGDFButton|
|Umschalten der Aktion am linken Rollrädchen |Linkes Rollrädchen drücken|
|Rückwärtsnavigieren des verwendeten linken Rollrädchens |Linkes Rollrädchen nach oben|
|Vorwärtsnavigieren des verwendeten linken Rollrädchens |Linkes Rollrädchen nach unten|
|Umschalten der Aktion am rechten Rollrädchen |Rechtes Rollrädchen drücken|
|Rückwärtsnavigieren des verwendeten rechten Rollrädchens |Rechtes Rollrädchen nach oben|
|Vorwärtsnavigieren des verwendeten rechten Rollrädchens |Rechtes Rollrädchen nach unten|
|Zum aktuellen Modul auf der Braillezeile springen |Routing-Taste|
|Umschalt+Tab |Leertaste+Punkt1+Punkt2|
|Tab |Leertaste+Punkt4+Punkt5|
|Pfeil nach oben |Leertaste+Punkt1|
|Pfeil nach unten |Leertaste+Punkt4|
|Strg+Pfeil nach links |Leertaste+Punkt2|
|Strg+Pfeil nach rechts |Leertaste+Punkt5|
|Pfeil nach links |Leertaste+Punkt3|
|Pfeil nach rechts |Leertaste+Punkt6|
|Pos1 |Leertaste+Punkt1+Punkt3|
|Ende |Leertaste+Punkt4+Punkt6|
|Strg+Pos1 |Leertaste+Punkt1+Punkt2+Punkt3|
|Strg+Ende |Leertaste+Punkt4+Punkt5+Punkt6|
|Alt-Taste |Leertaste+Punkt1+Punkt3+Punkt4|
|Alt+Tab |Leertaste+Punkt2+Punkt3+Punkt4+Punkt5|
|Alt+Umschalt+Tab |Leertaste+Punkt1+Punkt2+Punkt5+Punkt6|
|Windows-Taste+Tab |Leertaste+Punkt2+Punkt3+Punkt4|
|Escape-Taste |Leertaste+Punkt1+Punkt5|
|Windows-Taste |Leertaste+Punkt2+Punkt4+Punkt5+Punkt6|
|Leertaste |Leertaste|
|Strg+Taste umschalten |Leertaste+Punkt3+Punkt8|
|Alt-Taste umschalten |Leertaste+Punkt6+Punkt8|
|Windows-Taste umschalten |Leertaste+Punkt4+Punkt8|
|NVDA-Taste umschalten |Leertaste+Punkt5+Punkt8|
|Umschalt-Taste umschalten |Leertaste+Punkt7+Punkt8|
|Strg- und Umschalt-Tasten umschalten |Leertaste+Punkt3+Punkt7+Punkt8|
|Alt- und Umschalt-Tasten umschalten |Leertaste+Punkt6+Punkt7+Punkt8|
|Windows- und Umschalt-Tasten umschalten |Leertaste+Punkt4+Punkt7+Punkt8|
|NVDA- und Umschalt-Tasten umschalten |Leertaste+Punkt5+Punkt7+Punkt8|
|Strg- und Alt-Tasten umschalten |Leertaste+Punkt3+Punkt6+Punkt8|
|Strg-, Alt- und Umschalt-Tasten umschalten |Leertaste+Punkt3+Punkt6+Punkt7+Punkt8|
|Windows-Taste+M (Alle Anwendungen minimieren) |Leertaste+Punkt1+Punkt2+Punkt3+Punkt4+Punkt5+Punkt6|
|Aktuelle Zeile ausgeben |Leertaste+Punkt1+Punkt4|
|NVDA-Menü anzeigen |Leertaste+Punkt1+Punkt3+Punkt4+Punkt5|

Für neuere Modelle, die Kippschalter besitzen (Focus 40, Focus 80 und Focus Blue) sind folgende Tastenzuweisungen verfügbar:

| Name |Tastenkombination|
|---|---|
|Braillezeile zur vorherigen Zeile bewegen |linker Kippschalter oben, rechter Kippschalter oben|
|Braillezeile zur nächsten Zeile bewegen |linker Kippschalter unten, rechter Kippschalter unten|

Nur für Focus 80:

| Name |Tastenkombination|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Linke Navigationskipptaste oben, rechte Navigationskipptaste oben|
|Auf der Braillezeile vorwärts navigieren |Linke Navigationskipptaste unten, rechte Navigationskipptaste unten|

<!-- KC:endInclude -->

### Optelec ALVA 6 Serie/Protokoll-Converter {#OptelecALVA}

Beide Braillezeilen - die BC640 und die BC680 - von [Optelec](https://www.optelec.de/) werden via USB und Bluetooth unterstützt.
Sie können alternativ auch ältere Optelec-Braillezeilen wie beispielsweise das Braille Voyager mit NVDA verwenden. Dazu benötigen Sie den Protokoll-Converter von Optelec.
Sie benötigen keine installierten Treiber, um diese Zeile verwenden zu können.
Sie müssen die Zeile lediglich anschließen und in NVDA konfigurieren.

Hinweis! Die Bluetooth-Verbindung einer ALVA BC6-Braillezeile mit Hilfe des ALVA Bluetooth-Werkzeugs könnte unter NVDA fehlschlagen.
Wenn Sie eine entsprechende Fehlermeldung erhalten, verbinden Sie die Braillezeile über die Bluetooth-Einstellungen von Windows.

Hinweis! Da Diese Braillezeilen eine eigene Braille-Tastatur besitzen (HID-Tastatur),arbeiten sie eingegebene Braillezeichen selbstständig ab. Die eigene Eingabeschnittstelle ist standardmäßig aktiv.
In diesem Fall haben die Einstellungen der Eingabetabelle aus den Braille-Einstellungen keine Wirkung.
Bei ALVA-Breillezeilen mit aktueller Firmware kann die HID-Tastatur über eine Tastenkombination deaktiviert werden.
Bitte lesen Sie in der Dokumentation der Braillezeilen für weitere Details nach.

Folgende Tastenkombinationen für diese Braillezeilen sind in NVDA zugeordnet.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |T1, eTouch1|
|Zur vorherigen Zeile auf der Braillezeile navigieren |T2|
|Zum Fokus wechseln |T3|
|Zur nächsten Zeile auf der Braillezeile navigieren |T4|
|Auf der Braillezeile vorwärts navigieren |T5, eTouch3|
|Zum aktuellen Modul auf der Braillezeile springen |Routing-Taste|
|Textformatierung am aktuellen Modul ausgeben |Obere Routing-Taste|
|HID-Tastatursimulation ein- oder ausschalten |T1+spEingabe|
|NVDA-Cursor zur ersten Zeile bewegen |T1+T2|
|NVDA-Cursor zur letzten Zeile bewegen |T4+T5|
|Kopplung der Braillezeile konfigurieren |T1+T3|
|Titelzeile anzeigen |etouch2|
|Statuszeile anzeigen |etouch4|
|Umschalt+Tab |Sp1|
|Alt-Taste |Sp2, Alt|
|Escape-Taste |Sp3|
|Tab-Taste |Sp4|
|Pfeiltaste nach oben |SpUp|
|Pfeiltaste nach unten |SpDown|
|Pfeiltaste nach links |SpLeft|
|Pfeiltaste nach rechts |SpRight|
|Eingabetaste |SpEingabe, Eingabe|
|Datum/Uhrzeit anzeigen |Sp2+Sp3|
|NVDA-Menü |Sp1+Sp3|
|Windows-Taste+M (alle Anwendungen minimieren) |Sp1+Sp4|
|Windows-Taste+B (Infobereich anzeigen) |Sp3+Sp4|
|Windows-Taste |Sp1+Sp2, Windows|
|Alt+Tab |Sp2+Sp4|
|Strg+Pos1 |T3+SpUp|
|Strg+Ende |T3+SpDown|
|Pos1 |T3+SpLeft|
|Ende |T3+SpRight|
|Strg-Taste |Steuerung|

<!-- KC:endInclude -->

### HandyTech-Braillezeilen {#HandyTech}

Die meisten Braillezeilen der Firma [HandyTech GmbH](https://www.handytech.de/) werden von NVDA via seriellem Port, USB und Bluetooth unterstützt.
bei älteren USB-Braillezeilen werden Sie den Universaltreiber von handy Tech installieren müssen.

Die folgenden Braillezeilenmodelle werden nicht ohne weiteres unterstützt; sie können Sie jedoch unter Zuhilfenahme des [universaltreibers](https://handytech.de/de/service/kundenservice/service-software/universeller-braillezeilentreiber) und der NVDA-Erweiterung verwenden:

* Braillino
* Buchwurm
* Modular-Zeilen mit firmware-version 1.13 oder niedriger. Bitte beachten Sie, dass die Firmware dieser Braillezeilen aktualisiert werden kann.

Folgende Tastenkombinationen bei diesen Braillezeilen sind für NVDA zugeordnet.
Bitte lesen Sie in der Dokumentation der Braillezeile für weitere Details.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Links, nach oben, B3|
|Auf der Braillezeile vorwärts navigieren |Rechts, nach unten, B6|
|Eine Zeile nach oben springen |B4|
|Eine Zeile nach unten springen |B5|
|Zum Braille-Modul springen |Routing-Taste|
|Umschalt+Tabulatortaste |Escape-Taste, Linke Triple-Aktionstaste auf+ab|
|Alt-Taste |B2+B4+B5|
|Escape-Taste |B4+B6|
|Tab-Taste |Eingabe, rechte Triple-Aktionstaste auf+ab|
|Eingabetaste |Escape-Taste+Eingabe, linke+rechte triple-Aktionstaste auf+ab, joystick-Aktion|
|Pfeiltaste nach oben |Joystick auf|
|Pfeiltaste nach unten |Joystick ab|
|Pfeiltaste nach links |Joystick nach links|
|Pfeiltaste nach rechts |Joystick nach rechts|
|NVDA-Menü |B2+B4+B5+B6|
|Kopplung der Braillezeile ändern |B2|
|Braille-Cursor ein-/ausblenden |B1|
|Braille-Kontextanzeige umschalten |B7|
|Braille-Eingabe ein-/ausschalten |Leertaste+B1+B3+B4 (Leertaste+Großbuchstabe B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

Die Lilli-Braillezeile von der italienischen Firma [MDV](https://www.mdvbologna.it/) wird unterstützt.
Sie benötigen keine installierten Treiber, um diese Zeile verwenden zu können.
Sie müssen lediglich die Braillezeile anschließen und in NVDA konfigurieren.

Diese Braillezeile unterstützt nicht die automatische Braillezeilenerkennung im Hintergrund von NVDA.

Folgende Tastenzuweisungen sind in NVDA bei dieser Zeile verfügbar:
Bitte lesen Sie in der Dokumentation zu ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |LF|
|Auf der Braillezeile vorwärts navigieren |RG|
|Braillezeile zur vorherigen Zeile bewegen |UP|
|Braillezeile zur nächsten Zeile bewegen |DN|
|Cursor zum Braille-Modul ziehen |Route|
|Umschalt+Tab-Taste |SLF|
|Tab-Taste |SRG|
|Alt+Tab-Taste |SDN|
|Alt+Umschalt+Tab-Taste |SUP|

<!-- KC:endInclude -->

### Braillezeilen von Baum/VisioBraille, Humanware, APH, Orbit {#Baum}

Mehrere Braillezeilen von [Baum/VisioBraille](https://www.visiobraille.de/index.php?article_id=1&clang=2), [Humanware](https://www.humanware.com/), [APH](https://www.aph.org/) und [Orbit](https://www.orbitresearch.com/) werden unterstützt, sobald sie über USB, Bluetooth oder seriell angeschlossen bzw. verbunden wurden.
Dies sind auch:

* Baum/VisioBraille: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* Humanware: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Einige andere Braillezeilen von der ehemaligen Firma Baum könnten ebenfalls funktionieren, dies wurde allerdings noch nicht getestet.

Wenn Sie die Braillezeile über USB angeschlossen und den USB-Modus nicht auf HID eingestellt haben, müssen Sie zunächst den vom Hersteller bereitgestellten Treiber installieren.
die Braillezeilenmodelle VarioUltra und Pronto! verwenden das HID-Protokoll.
Die Braillezeilen Refreshabraille und Orbit Reader 20 können so eingestellt werden, dass sie das HID-Protokoll verwenden.

Der serielle Modus des orbit Readers 20 wird momentan nur unter Windows 10 und neuer unterstützt.
Sie sollten stattdessen das HID-Protokoll über USB verwenden.

Folgende Tastenzuweisungen sind in NVDA bei diesen Zeilen verfügbar:
Bitte lesen Sie in der Dokumentation der Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der braillezeile rückwärts navigieren |`d2`|
|Auf der braillezeile vorwärts navigieren |`d5`|
|Auf der Braillezeile zur vorherigen Zeile navigieren |`d1`|
|Auf der Braillezeile zur nächsten Zeile navigieren |`d3`|
|Zum aktuellen Braille-Modul springen |`Routing`-Taste|
|`Umschalt+Tab` |`Leertaste+Punkt1+Punkt3`|
|`Tab`-Taste |`Leertaste+Punkt4+Punkt6`|
|`Alt`-Taste |`Leertaste+Punkt1+Punkt3+Punkt4` (`Leertaste+M`)|
|`Escape`-Taste |`Leertaste+Punkt1+Punkt5` (`Leertaste+E`)|
|`Windows`-Taste |`Leertaste+Punkt3+Punkt4`|
|`Alt+Tab` |`Leertaste+Punkt2+Punkt3+Punkt4+Punkt5` (`Leertaste+T`)|
|NVDA-Menü |`Leertaste+Punkt1+Punkt3+Punkt4+Punkt5` (`Leertaste+N`)|
|`Windows+D` (minimiert alle Apps) |`Leertaste+Punkt1+Punkt4+Punkt5` (`Leertaste+D`)|
|Alles Vorlesen |`Leertaste+Punkt1+Punkt2+Punkt3+Punkt4+Punkt5+Punkt6`|

Für Braillezeilen, die einen Joystick besitzen:

| Name |Taste|
|---|---|
|Taste "Pfeil Auf" |Auf|
|Taste "Pfeil Ab" |Ab|
|Taste "Pfeil Links" |Links|
|Taste "Pfeil Rechts" |Rechts|
|Eingabetaste |Auswahl|

<!-- KC:endInclude -->

### Hedo Profiline USB {#HedoProfiLine}

Die Profiline USB der Firma [Hedo Reha-Technik](https://www.hedo.de/) werden unterstützt.
Zuerst müssen Sie den USB-Treiber des Herstellers installieren.

Diese Braillezeile unterstützt nicht die automatische Braillezeilenerkennung im Hintergrund von NVDA.

Die folgenden Tastenkombinationen für diese Braillezeile sind in NVDA verfügbar:
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Tastenkombination|
|---|---|
|Auf der Braillezeile rückwärts navigieren |K1|
|Auf der Braillezeile vorwärts navigieren |K3|
|Braillezeile zur vorherigen Zeile bewegen |B2|
|Braillezeile zur nächsten Zeile bewegen |B5|
|Cursor zum Braille-Modul bewegen |Routing-Taste|
|Kopplung der Braillezeile umschalten |K2|
|Alles Lesen |B6|

<!-- KC:endInclude -->

### Hedo MobilLine USB {#HedoMobilLine}

Die MobilLine USB der Firma [Hedo Reha-Technik](https://www.hedo.de/) werden unterstützt.
Zuerst müssen Sie den USB-Treiber des Herstellers installieren.

Diese Braillezeile unterstützt nicht die automatische Braillezeilenerkennung im Hintergrund von NVDA.

Die folgenden Tastenkombinationen für diese Braillezeile sind in NVDA verfügbar:
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Tastenkombination|
|---|---|
|Auf der Braillezeile rückwärts navigieren |K1|
|Auf der Braillezeile vorwärts navigieren |K3|
|Braillezeile zur vorherigen Zeile bewegen |B2|
|Braillezeile zur nächsten Zeile bewegen |B5|
|Cursor zum Braille-Modul bewegen |Routing-Taste|
|Kopplung der Braillezeile umschalten |K2|
|Alles Lesen |B6|

<!-- KC:endInclude -->

### Humanware Brailliant BI/B-Serie / BrailleNote Touch {#HumanWareBrailliant}

Die Braillezeilen Brailliant BI und B von [Humanware](https://www.humanware.com/), einschließlich BI 14, BI 32, BI 20X, BI 40, BI 40X und B 80, werden unterstützt, wenn sie über USB oder Bluetooth angeschlossen werden.
Wenn Sie die Zeile über USB anschließen wollen während das Übertragungsprotokoll Humanware verwendet wird, müssen Sie zunächst den USB-Treiber des Herstellers installieren.
Verwenden Sie hingegen das Protokoll OpenBraille, wird kein USB-Treiber benötigt.

Die folgenden zusätzlichen Geräte werden ebenfalls unterstützt (und erfordern keine speziellen Treiber, die installiert werden müssen):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Folgende Tastenkombinationen sind bei diesen Braillezeilen verfügbar
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.

#### Tasten für alle Braillezeilenmodelle {#toc332}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur vorherigen Zeile bewegen |Auf|
|Braillezeile zur nächsten Zeile bewegen |Ab|
|Cursor zum Braille-Modul bewegen |Routing-Taste|
|Braillezeile koppeln an |Auf+Ab|
|Taste Pfeil nach oben |Leertaste+Punkt1|
|Taste Pfeil nach unten |Leertaste+Punkt4|
|Taste Pfeil nach links |Leertaste+Punkt3|
|Taste Pfeil nach rechts |Leertaste+Punkt6|
|Umschalt+Tab |Leertaste+Punkt1+Punkt3|
|Tab-Taste |Leertaste+Punkt4+Punkt6|
|Alt-Taste |Leertaste+Punkt1+Punkt3+Punkt4 (Leertaste+M)|
|Escape-Taste |Leertaste+Punkt1+Punkt5 (Leertaste+E)|
|Eingabetaste |Punkt8|
|Windows-Taste |Leertaste+Punkt3+Punkt4|
|Alt+Tab |Leertaste+Punkt2+Punkt3+Punkt4+Punkt5 (Leertaste+T)|
|NVDA-Menü |Lertaste+Punkt1+Punkt3+Punkt4+Punkt5 (Leerttaste+N)|
|Windows-Taste+M (Alle Anwendungen minimieren) |Leertaste+Punkt1+Punkt4+Punkt5 (Leertaste+D)|
|Alles Lesen |Leertaste+Punkt1+Punkt2+Punkt3+Punkt4+Punkt5+Punkt6|

<!-- KC:endInclude -->

#### Tastenzuweisungen für Brailliant BI 32/40 und B 80 {#toc333}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|NVDA-Menü |C1+C3+C4+C5 (Befehl N)|
|Windows-Taste+M (Alle Anwendungen minimieren) |C1+C4+C5 (Befehl D)|
|Alles Lesen |C1+C2+C3+C4+C5+C6|

<!-- KC:endInclude -->

#### Tastenzuweisungen für Brailliant BI 14 {#toc334}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Pfeiltaste nach oben |Joystick auf|
|Pfeiltaste nach unten |Joystick ab|
|Pfeiltaste nach links |Joystick Links|
|Pfeiltaste nach rechts |Joystick Rechts|
|Eingabetaste |Joystick-Aktion|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/SyncBraille-Serien {#Hims}

NVDA unterstützt die Braillezeilenmodelle Braille Sense, Braille EDGE, SyncBraille und Smart Beetle von [HIMS](https://www.hims-inc.com/), wahlweise mit USB- oder Bluetooth-Anbindung.
Wenn Sie die Braillezeile per USB anschließen, müssen Sie noch die [USB-Treiber von HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) auf Ihrem System installieren.

Folgende Tastenkombinationen sind in NVDA verfügbar:
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Cursor zum Braille-Modul ziehen |Routing-Taste|
|Auf der Braillezeile rückwärts navigieren |Rollen oben auf der linken Seite, rollen oben auf der rechten Seite, rollen auf der linken Seite|
|Auf der Braillezeile vorwärts navigieren |Rollen unten auf der linken Seite, rollen unten auf der rechten Seite, rollen auf der rechten Seite|
|Zur vorherigen Zeile bewegen |Rollen oben auf der linken Seite und rollen oben auf der rechten Seite|
|Zur nächsten Zeile bewegen |Rollen unten auf der linken Seite und rollen unten auf der rechten Seite|
|NVDA-Cursor zur vorherigen Zeile bewegen |Pfeil nach oben auf der rechten Seite|
|NVDA-Cursor zur nächsten Zeile bewegen |Pfeil nach unten auf der rechten Seite|
|NVDA-Cursor zum vorherigen Zeichen bewegen |Pfeil nach links auf der rechten Seite|
|NVDA-Cursor zum nächsten Zeichen bewegen |Pfeil nach rechts auf der rechten Seite|
|Zum Fokus wechseln |Scroll oben auf der linken Seite+Scroll unten auf der linken Seite, rollen oben auf der rechten Seite und rollen unten auf der rechten Seite, rollen auf der linken Seite und rollen auf der rechten Seite|
|Strg-Taste |smartbeetle:f1, brailleedge:f3|
|Windows-Taste |F7, smartbeetle:f2|
|Alt-Taste |Punkt1+Punkt3+Punkt4+Leertaste, F2, smartbeetle:f3, brailleedge:f4|
|Umschalt-Taste |F5|
|Einfügetaste |Punkt2+Punkt4+Leertaste, F6|
|Kontextmenütaste |Punkt1+Punkt2+Punkt3+Punkt4+Leertaste, F8|
|Dauergroßschreibtaste |Punkt1+Punkt3+Punkt6+Leertaste|
|Tab-Taste |Punkt4+Punkt5+Leertaste, F3, brailleedge:f2|
|Alt+Umschalt+Tab-Taste |F1+F2+F3|
|Alt+Tab-Taste |F2+F3|
|Umschalt+Tab-Taste |Punkt1+Punkt2+Leertaste|
|Ende |Punkt4+Punkt6+Leertaste|
|Strg+Ende |Punkt4+Punkt5+Punkt6+Leertaste|
|Pos1 |Punkt1+Punkt3+Leertaste, smartbeetle:f4|
|Strg+Pos1 |Punkt1+Punkt2+Punkt3+Leertaste|
|Alt+F4 |Punkt1+Punkt3+Punkt5+Punkt6+Leertaste|
|Pfeiltaste nach links |Punkt3+Leertaste, Pfeil nach links auf der linken Seite|
|Strg+Umschalt+Pfeiltaste nach links |Punkt2+Punkt8+Leertaste+F1|
|Strg+Pfeiltaste nach links |Punkt2+Leertaste|
|Umschalt+Alt+Pfeiltaste nach links |Punkt2+Punkt7+F1|
|`Alt+Pfeiltaste nach links` |`Punkt2+Punkt7+Leertaste`|
|Pfeiltaste nach rechts |Punkt6+Leertaste, Pfeil rechts auf der linken Seite|
|Strg+Umschalt+Pfeiltaste nach rechts |Punkt5+Punkt8+Leertaste+F1|
|Strg+Pfeiltaste nach rechts |Punkt5+Leertaste|
|Umschalt+Alt+Pfeiltaste nach rechts |Punkt5+Punkt7+F1|
|`Alt+Pfeiltaste nach rechts` |`Punkt5+Punkt7+Leertaste`|
|Seite nach oben |Punkt1+Punkt2+Punkt6+Leertaste|
|Strg+Seite nach oben |Punkt1+Punkt2+Punkt6+Punkt8+Leertaste|
|Pfeiltaste nach oben |Punkt1+Leertaste, Pfeil nach oben auf der linken Seite|
|Strg+Umschalt+Pfeiltaste nach oben |Punkt2+Punkt3+Punkt8+Leertaste+F1|
|Strg+Pfeiltaste nach oben |Punkt2+Punkt3+Leertaste|
|Umschalt+Alt+Pfeiltaste nach oben |Punkt2+Punkt3+Punkt7+F1|
|`Alt+Pfeiltaste nach oben` |`Punkt2+Punkt3+Punkt7+Leertaste`|
|Umschalt+Pfeiltaste nach oben |Scroll unten auf der linken Seite + Leertaste|
|Seite nach unten |Punkt3+Punkt4+Punkt5+Leertaste|
|Strg+Seite nach unten |Punkt3+Punkt4+Punkt5+Punkt8+Leertaste|
|Pfeiltaste nach unten |Punkt4+Leertaste, Pfeil ab auf der linken Seite|
|Strg+Umschalt+Pfeiltaste nach unten |Punkt5+Punkt6+Punkt8+Leertaste+F1|
|Strg+Pfeiltaste nach unten |Punkt5+Punkt6+Leertaste|
|Umschalt+Alt+Pfeiltaste nach unten |Punkt5+Punkt6+Punkt7+F1|
|`Alt+Pfeiltaste nach unten` |`Punkt5+Punkt6+Punkt7+Leertaste`|
|Umschalt+Pfeiltaste nach unten |Scroll unten auf der rechten Seite + Leertaste|
|Escape-Taste |Punkt1+Punkt5+Leertaste, F4, brailleedge:f1|
|Entf |Punkt1+Punkt3+Punkt5+Leertaste, Punkt1+Punkt4+Punkt5+Leertaste|
|F1 |Punkt1+Punkt2+Punkt5+Leertaste|
|F3 |Punkt1+Punkt4+Punkt8+Leertaste|
|F4 |Punkt7+F3|
|Windows-Taste+B |Punkt1+Punkt2+F1|
|Windows-Taste+M |Punkt1+Punkt4+Punkt5+F1|
|Strg+Einfg |smartbeetle:F1+Scrollen auf der rechten Seite|
|Alt+Einfg |smartbeetle:F3+Scrollen auf der rechten Seite|

<!-- KC:endInclude -->

### Seika-Braillezeilen {#Seika}

Die folgenden Seika-Braillezeilen von Nippon Telesoft werden in zwei Gruppen mit unterschiedlicher Varianten unterstützt:

* [Seika Version 3, 4 und 5 (mit 40 Modulen), Seika80 (mit 80 Modulen)](#SeikaBrailleDisplays)
* [MiniSeika (mit 16 und 24 Modulen), V6 und V6Pro (mit 40 Modulen)](#SeikaNotetaker)

Weitere Informationen zu den Braillezeilen finden Sie auf der [Demo- und Treiber-Downloadseite](https://en.seika-braille.com/down/index.html).

#### Seika Version 3, 4 und 5 (mit 40 Modulen), Seika80 (mit 80 Modulen) {#SeikaBrailleDisplays}

* Diese Braillezeilen unterstützen noch nicht die automatische Erkennung im Hintergrund durch NVDA.
* Wählen Sie "Seika-Braillezeilen" zur manuellen Konfiguration aus
* Vor der Verwendung von Seika v3/4/5/80 muss ein Gerätetreiber installiert werden.
Die Treiber werden [vom Hersteller bereitgestellt](https://de.seika-braille.com/down/index.html).

Nachfolgend die Tastenbelegungen der Seika-Braillezeile.
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo die entsprechenden Tasten zu finden sind.
<!-- KC:beginInclude -->

| Name |Tastenkombination|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur vorherigen Zeile bewegen |B3|
|Braillezeile zur nächsten Zeile bewegen |B4|
|Kopplung der Braillezeile umschalten |B5|
|Alles Lesen |B6|
|Tab-Taste |B1|
|Umschalt+Tab-Taste |B2|
|Alt+Tab-Taste |B1+B2|
|NVDA-Menü |Links+Rechts|
|Cursor zum Braille-Modul bewegen |Routing-Taste|

<!-- KC:endInclude -->

#### MiniSeika (mit 16 und 24 Modulen), V6 und V6Pro (mit 40 Modulen) {#SeikaNotetaker}

* Die automatische Erkennung im Hintergrund der Braillezeile in NVDA wird über USB und Bluetooth unterstützt.
* Wählen Sie zur Konfiguration "Seika Notetaker" oder "Automatisch" aus.
* Bei Verwendung von Seika Notetaker sind keine zusätzlichen Treiber erforderlich.

Nachfolgend die Tastenbelegungen für Seika Notetaker.
Wo sich diese Tasten befinden, entnehmen Sie bitte der Dokumentation der Braillezeile.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Braillezeile rückwärts scrollen |Links|
|Braillezeile vorwärts scrollen |Rechts|
|Alles Lesen |Leertaste+Rücktaste|
|NVDA-Menü |Links+Rechts|
|Braillezeile zur vorherigen Zeile ziehen |LJ oben|
|Braillezeile zur nächsten Zeile ziehen |LJ unten|
|Braillezeile koppeln umschalten |LJ mittig|
|Tab |LJ rechts|
|Umschalt+Tab |LJ links|
|Pfeiltaste nach oben |RJ oben|
|Pfeiltaste nach unten |RJ unten|
|Pfeiltaste nach links |RJ links|
|Pfeiltaste nach rechts |RJ rechts|
|Zum braille-Modul navigieren |Routing-Taste|
|Umschalt+Pfeiltaste nach oben |Leertaste+RJ oben, Rücktaste+RJ oben|
|Umschalt+Pfeiltaste nach unten |Leertaste+RJ unten, Rücktaste+RJ unten|
|Umschalt+Pfeiltaste nach links |Leertaste+RJ links, Rücktaste+RJ links|
|Umschalt+Pfeiltaste nach rechts |Leertaste+RJ rechts, Rücktaste+RJ rechts|
|Eingabetaste |RJ mittig, Punkt8|
|Escape-Taste |Leertaste+RJ mittig|
|Windows-Taste |Rücktaste+RJ mittig|
|Leertaste |Leertaste, Rücktaste|
|Rücktaste |Punkt7|
|Taste Seite nach oben |Leertaste+LJ rechts|
|Taste Seite nach unten |Leertaste+LJ links|
|Taste Pos1 |Leertaste+LJ oben|
|Taste Ende |Leertaste+LJ unten|
|Strg+Pos1 |Rücktaste+LJ oben|
|Strg+Ende |Rücktaste+LJ unten|

### Papenmeier BrailleX (Neuere Modelle) {#Papenmeier}

Folgende Braillezeilen werden unterstützt:

* BRAILLEX EL 40c, EL 80c, EL 20c, EL60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2D80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB und Bluetooth)
* BRAILLEX Live 20, BRAILLEX Live und BRAILLEX Live Plus (USB und Bluetooth)

Diese Braillezeilen unterstützen nicht die automatische Braillezeilenerkennung im Hintergrund von NVDA.
Es gibt eine Option im USB-Treiber der Braillezeilen, die zu Problemen beim Laden der Braillezeile führen kann.
Bitte versuchen Sie folgendes:

1. Bitte stellen Sie sicher, dass Sie den [neuesten Treiber https://www.papenmeier-rehatechnik.de/service/downloadcenter/software/artikel/software-braille-geräte.html] installiert haben.
1. Öffnen Sie den Windows-Geräte-Manager.
1. Scrollen Sie in der Liste nach unten zu „USB-Controller“ oder „USB-Geräte“.
1. Wählen Sie „Papenmeier Braillex USB-Gerät“ o. ä..
1. Öffnen Sie die Eigenschaften und wechseln Sie zur Registerkarte Erweitert.
Manchmal wird die Registerkarte „Erweitert“ nicht angezeigt.
Wenn dies der Fall ist, trennen Sie die Braillezeile vom Computer, beenden Sie NVDA, warten Sie einen Moment und schließen Sie die Braillezeile wieder an.
Wiederholen Sie dies bei Bedarf 4 bis 5 Mal.
Sollte die Registerkarte „Erweitert“ immer noch nicht angezeigt werden, starten Sie bitte den Computer neu.
1. Deaktivieren Sie die Option VCP laden.

Viele Braillezeilen besitzen eine Navigationsleiste (EAB), die eine intuitive und schnelle Bedienung ermöglicht.
Diese Navigationsleiste kann in vier Richtungen bewegt werden, wobei sie in der Regel zwei Schalterstellungen je Richtung hat.
Ausnahmen bilden die C- und die Live-Serien.

Die Braillezeilen der C-Serie und einige weitere verfügen über eine doppelte Routingreihe, wobei die obere in NVDA verwendet wird, um Formatierungsinformationen über das aktuell gewählte Zeichen anzuzeigen.
Die zweite Schalterstellung der Navigationsleiste wird bei der C-Serie ausgelöst, indem eine Taste der oberen Routing-Tasten gedrückt gehalten und gleichzeitig die EAB betätigt wird.
Die Live-Serien sind nur mit einer Routing-Reihe ausgestattet, die EAB hat in alle Richtungen nur eine Schalterposition.
Die zweite Schalterstellung kann mittels Routing+EAB in die entsprechende Richtung emuliert werden.
Längeres Drücken von Auf, Ab, Links, Rechts, EAB löst die zugehörige Aktion mehrfach aus.

Die folgenden Schalter gibt es auf der Braillezeile:

| Name |Taste|
|---|---|
|L1 |Linke Taster oben|
|L2 |Linke Taster unten|
|R1 |Rechte Taster oben|
|R2 |Rechte Taster unten|
|Auf |Navigationsleiste einmal nach oben|
|Auf2 |Navigationsleiste zweimal nach oben|
|Links |Navigationsleiste einmal nach links|
|Links2 |Navigationsleiste zweimal nach links|
|Rechts |Navigationsleiste einmal nach rechts|
|Rechts2 |Navigationsleiste zweimal nach rechts|
|Ab |Navigationsleiste einmal nach unten|
|Ab2 |Navigationsleiste zweimal nach unten|

Folgende Tastenkombinationen sind bei Papenmeier-Braillezeilen in Kombination mit NVDA verfügbar:
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur vorherigen Zeile bewegen |Auf|
|Braillezeile zur nächsten Zeile bewegen |Ab|
|Cursor zum Braille-Modul ziehen |Routing-Taste|
|Liest das Zeichen unter dem Cursor vor |L1|
|Führt die Standardaktion aus |L2|
|Koppelt Braillezeile wahlweise an Fokus oder Anzeige |R2|
|Liest die Titelzeile des aktiven Fensters vor |L1+Auf|
|Liest die Statusleiste des aktiven Fensters vor |L2+Ab|
|Zieht das Navigator-Objekt zum übergeordneten Objekt |Auf2|
|Zieht das Navigator-Objekt zum ersten beinhaltenden Objekt |Ab2|
|Zieht das Navigator-Objekt zum nächsten Objekt |Rechts2|
|Zieht das Navigator-Objekt zum vorherigen Objekt |Links2|
|Textformatierungen auf dem aktuellen Modul ausgeben |Obere Routing-Taste|

<!-- KC:endInclude -->

Die Braillex Trio besitzt vor der Braille-Tastatur noch vier zusätzliche Tasten.
Dies sind von links nach rechts:

* Nach links springen (LT)
* Leertaste
* Leertaste
* Nach rechts springen (RT)

Die Taste RT wird momentan noch nicht verwendet.
Die inneren Tasten sind als Leertasten belegt.

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Escape-Taste |Leertaste+Punkt7|
|Pfeil nach oben |Leertaste+Punkt2|
|Pfeil nach links |Leertaste+Punkt1|
|Pfeil nach rechts |Leertaste+Punkt4|
|Pfeil nach unten |Leertaste+Punkt5|
|Strg |LT+Punkt2|
|Alt-Taste |LT+Punkt3|
|Strg+Escape-Taste |Leertaste+Punkte 1 2 3 4 5 6|
|Tab-Taste |Leertaste+Punkte 3 7|

<!-- KC:endInclude -->

### Papenmeier BrailleX (Ältere Modelle) {#PapenmeierOld}

Die folgenden Braillezeilen werden unterstützt:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Beachten Sie, dass diese Braillezeilen nur seriell angeschlossen werden können.
Aus diesem Grund unterstützen diese Displays nicht die automatische Braillezeilenerkennung im Hintergrund von NVDA.
Sie sollten den Port auswählen, an den die Braillezeile angeschlossen ist, nachdem Sie diesen Treiber im Dialogfeld "[Braillezeile auswählen](#SelectBrailleDisplay)" ausgewählt haben.

Einige dieser Braillezeilenmodelle besitzen eine Navigationsleiste, die eine schnelle und intuitive Bedienung ermöglicht.
Die Navigationsleiste kann in alle vier Richtungen in jeweils zwei Stufen bewegt werden.
Wenn Sie die Navigationsleiste bewegen und gedrückt halten, wird die entsprechende Navigationsoperation wiederholt ausgeführt.
Bei älteren Modellen, die keine Navigationsleiste besitzen, kommen stattdessen Daumentasten zum Einsatz.

Im Allgemeinen gibt es auf allen Braillezeilen die folgenden Tasten:

| Name |Taste|
|---|---|
|L1 |Linke vordere Taste|
|L2 |Linke hintere Taste|
|R1 |Rechte vordere Taste|
|R2 |Rechte hintere Taste|
|Auf |Einen Schritt nach oben springen|
|Auf2 |Zwei Schritte nach oben springen|
|Links |Einen Schritt nach links springen|
|Links2 |Zwei Schritte nach links springen|
|Rechts |Einen Schritt nach rechts springen|
|Rechts2 |Zwei Schritte nach rechts springen|
|Ab |Einen Schritt nach unten springen|
|Ab2 |Zwei Schritte nach unten springen|

Die folgenden Befehle sind in NVDA verfügbar:

<!-- KC:beginInclude -->
Geräte mit Navigationsleiste

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur vorherigen Zeile bewegen |Auf|
|Braillezeile zur nächsten Zeile bewegen |Ab|
|Cursor zum ausgewählten Braille-Modul bewegen |Routing-Taste|
|Aktuelles Zeichen am NVDA-Cursor ausgeben |L1|
|Aktuelles Navigator-Objekt aktivieren |L2|
|Titelzeile ausgeben |L1+Auf|
|Statuszeile ausgeben |L2+Ab|
|Zum übergeordneten Objekt springen |Auf2|
|Zum ersten untergeordneten Objekt springen |Ab2|
|Zum vorherigen Objekt bewegen |Links2|
|Zum nächsten Objekt bewegen |Rechts2|
|Textformatierung am Modul ausgeben |Obere Routing-Taste|

BRAILLEX Tiny

| Name |Taste|
|---|---|
|Aktuelles Zeichen am NVDA-Cursor ausgeben |L1|
|Aktuelles Navigator-Objekt aktivieren |L2|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur vorherigen Zeile bewegen |Auf|
|Braillezeile zur nächsten Zeile bewegen |Ab|
|Kopplung der Braillezeile konfigurieren |R2|
|Zum übergeordneten Objekt bewegen |R1+Auf|
|Zum ersten untergeordneten Objekt bewegen |R1+Ab|
|Zum vorherigen Objekt bewegen |R1+Links|
|Zum nächsten Objekt bewegen |R1+Rechts|
|Textformatierung am Modul ausgeben |obere Routing-Taste|
|Titelzeile der aktuellen Anwendung anzeigen |L1+Auf|
|Statuszeile anzeigen |L2+Ab|

BRAILLEX 2D Screen

| Name |Taste|
|---|---|
|Aktuelles Zeichen am NVDA-Cursor ausgeben |L1|
|Aktuelles Navigator-Objekt aktivieren |L2|
|Kopplung der Braillezeile konfigurieren |R2|
|Textformatierung am Braille-Modul ausgeben |Obere Routing-Taste|
|Braillezeile zur vorherigen Zeile bewegen |Auf|
|Auf der Braillezeile rückwärts navigieren |Links|
|Auf der Braillezeile vorwärts navigieren |Rechts|
|Braillezeile zur nächsten Zeile bewegen |Ab|
|Zum nächsten Objekt bewegen |Links2|
|Zum übergeordneten Objekt bewegen |Auf2|
|Zum ersten untergeordneten Objekt bewegen |Ab2|
|Zum vorherigen Objekt bewegen |Rechts2|

<!-- KC:endInclude -->

### Humanware BrailleNote {#HumanWareBrailleNote}

NVDA unterstützt die BrailleNote-Modelle von [Humanware](https://www.humanware.com) sofern diese als Braillezeilen betrieben werden.
Die folgenden Modelle werden unterstützt:

* BrailleNote Classic (nur serielle Verbindung)
* BrailleNote PK (Seriell und Bluetooth)
* BrailleNote MPower (Seriell und Bluetooth)
* BrailleNote Apex (Verbunden über USB oder Bluetooth)

Für BrailleNote Touch lesen Sie bitte den Abschnitt [Brailliant BI-Serie / BrailleNote Touch](#HumanWareBrailliant).

Außer beim Braillenote PK werden sowohl Braille BT- und die QT-Tastaturen unterstützt.
Die Emulation der PC-Tastatur von Braillenote QT wird (noch) nicht unterstützt.
Sie können über die QWERTZ-Tastatur auch Braillepunkte eingeben.
Weitere Informationen finden Sie im Abschnitt Braille-terminal des Handbuchs Ihrer Braillezeile.

Wenn Ihre Braillezeile mehr als eine Verbindungsmethode unterstützt, müssen Sie den verwendeten Anschluss in den Braille-Terminal-Einstellungen festlegen.
Bitte sehen Sie in die Dokumentation Ihrer Braillezeile nach für weitere Informationen.
Zudem müssen Sie den verwendeten Anschluss in den Braille-Einstellungen von NVDA festlegen.
Wenn die Braillezeile über USB oder Bluetooth verbunden wird, können Sie "automatisch", "USB" oder "Bluetooth" einstellen.
Wenn Sie einen seriellen Anschluss (oder einen USB-Zu-Seriell-Konverter) verwenden, müssen Sie den verwendeten Anschluss ausdrücklich auswählen.

Bevor Sie die BrailleNote über USB verbinden können, müssen Sie den von Humanware bereitgestellten Treiber installieren.

Bei der Braillenote Apex BT können Sie das Scrollrad für die Ausführung von NVDA-Befehlen verwenden. Es befindet sich zwischen den Punkten 1 und 4.
Das Scrollrad besteht aus 4 punktförmigen Richtungstasten, einer mittleren Taste sowie dem eigentlichen Rad, das Sie mit und gegen den Uhrzeigersinn drehen können.

Folgende BrailleNote-Befehle können Sie in NVDA verwenden:
Bitte sehen Sie in der Dokumentation Ihrer Braillezeile nach, wo sich die entsprechenden Tasten befinden.

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Back|
|Auf der Braillezeile vorwärts navigieren |Advance|
|Zur vorherigen Zeile navigieren |Previous|
|Zur nächsten Zeile navigieren |Next|
|Cursor zum Braille-Modul bewegen |Routing-Taste|
|NVDA-Menü |Leertaste+Punkt1+Punkt3+Punkt4+Punkt5 (Leertaste+N)|
|Kopplung der Braillezeile ändern |Previous+Next|
|Pfeiltaste nach oben |Leertaste+Punkt1|
|Pfeiltaste nach unten |Leertaste+Punkt4|
|Pfeiltaste nach links |Leertaste+Punkt3|
|Pfeiltaste nach rechts |Leertaste+Punkt6|
|Seite nach oben |Leertaste+Punkt1+Punkt3|
|Seite nach unten |Leertaste+Punkt4+Punkt6|
|Pos1 |Leertaste+Punkt1+Punkt2|
|Ende |Leertaste+Punkt4+Punkt5|
|Strg+Pos1 |Leertaste+Punkt1+Punkt2+Punkt3|
|Strg+Ende |Leertaste+Punkt4+Punkt5+Punkt6|
|Leertaste |Leertaste|
|Eingabetaste |Leertaste+Punkt8|
|Rücktaste |Leertaste+Punkt7|
|Tab-Taste |Leertaste+Punkt2+Punkt3+Punkt4+Punkt5 (Leertaste+T)|
|Umschalt+Tab-Taste |Leertaste+Punkt1+Punkt2+Punkt5+Punkt6|
|Windows-Taste |Leertaste+Punkt2+Punkt4+Punkt5+Punkt6 (Leertaste+W)|
|Alt-Taste |Leertaste+Punkt1+Punkt3+Punkt4 (Leertaste+M)|
|Eingabehilfe ein-/ausschalten |Leertaste+Punkt2+Punkt3+Punkt6 (Leertaste+tief gestelltes H)|

Die folgenden Befehle sind im Braillenote QT verfügbar, wenn die Brailleeingabe nicht aktiviert ist:

| Name |Taste|
|---|---|
|NVDA-Menü |Lesen+N|
|Pfeil nach oben |Pfeil auf|
|Pfeil nach unten |Pfeil ab|
|Pfeil nach links |Pfeil links||
|Pfeil nach rechts |Pfeil rechts|
|Seite auf |Funktion+Pfeil auf|
|Seite ab |Funktion+Pfeil ab|
|Pos1 |Funktion+Pfeil links|
|Ende |Funktion+Pfeil rechts|
|Strg+Pos1 |Lesen+T|
|Strg+Ende |Lesen+B|
|Eingabetaste |Eingabe|
|Rücktaste |Rücktaste|
|Tab-Taste |Tab|
|Umschalt+Tab-Taste |Umschalt+Tab|
|Windows-Taste |Lesen+W|
|Alt-Taste |Lesen+M|
|Eingabehilfe ein/ausschalten |Lesen+1|

Die folgenden Befehle können mit dem Scrollrad ausgeführt werden:

| Name |Taste|
|---|---|
|Pfeil nach oben |Pfeil auf|
|Pfeil nach unten |Pfeil ab|
|Pfeil nach links |Pfeil links|
|Pfeil nach rechts |Pfeil rechts|
|Eingabetaste |mittlere Taste|
|Tab-Taste |Rad im Uhrzeigersinn drehen|
|Umschalt+Tab |Rad gegen den Uhrzeigersinn drehen|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA unterstützt die Ecobraille von [ONCE](https://www.once.es/).
Die folgenden Modelle werden unterstützt:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

In dem [Dialogfeld zum Auswählen der Braillezeile](#SelectBrailleDisplay) in den NVDA-Einstellungen können Sie den seriellen Anschluss festlegen, mit dem die Braillezeile verbunden ist.
Diese Braillezeilen unterstützen nicht die automatische Erkennung der Braillezeilen im Hintergrund von NVDA.

Folgende Tastenbelegungen sind bei Verwendung der Ecobraille-Modelle verfügbar:
Bitte sehen Sie in der [Dokumentation zur Ecobraille](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) nach, um zu erfahren, wo die entsprechenden Tasten zu finden sind.

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |T2|
|Auf der Braillezeile vorwärts navigieren |T4|
|Auf der Braillezeile zur vorherigen Zeile navigieren |T1|
|Auf der Braillezeile zur nächsten Zeile navigieren |T5|
|Cursor zum ausgewählten Braille-Modul bewegen |Routing-Taste|
|Aktuelles Navigator-Objekt aktivieren |T3|
|Zum nächsten Betrachter wechseln |F1|
|Zum übergeordneten Objekt navigieren |F2|
|Zum vorherigen Betrachter wechseln |F3|
|Zum vorherigen Objekt navigieren |F4|
|Aktuelles Objekt ausgeben |F5|
|Zum nächsten Objekt navigieren |F6|
|Zum Fokus wechseln |F7|
|Zum ersten untergeordneten Objekt navigieren |F8|
|System-Fokus oder Cursor zum aktuellen Navigator-Objekt navigieren |F9|
|Position des NVDA-Cursors angeben |F0|
|Kopplung der Braillezeile umschalten |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

Die in Taiwan stark verbreitete Braillezeile Superbraille kann entweder seriell oder über USB angeschlossen werden.
Da die SuperBraille weder eine Tastatur noch Navigationstasten besitzt, müssen sämtliche Navigationsaktionen über eine Standardtastatur ausgeführt werden.
Aus Kompatibilitätsgründen wurden deshalb zwei Tastenkombinationen definiert:
<!-- KC:beginInclude -->

| Name |Tastenkombination|
|---|---|
|Auf der Braillezeile rückwärts navigieren |Nummernblock Minus|
|Auf der Braillezeile vorwärts navigieren |Nummernblock plus|

<!-- KC:endInclude -->

### Braillezeilen von EuroBraille {#Eurobraille}

Die Braillezeilen b.book, b.note, Esys, Esytime und Iris von EuroBraille werden von NVDA unterstützt.  
Diese Geräte verfügen über eine Braille-Tastatur mit zehn Tasten. 
Eine Beschreibung dieser Tasten finden Sie in der Dokumentation der Braillezeile vom Hersteller.
Es gibt zwei Tasten, welche wie die leertaste angeordnet sind. Die linke Taste entspricht der Rücktaste, die rechte entspricht der Leertaste.

Diese Geräte werden über USB angeschlossen und verfügen über eine eigenständige USB-Tastatur. 
Es ist möglich, diese Tastatur zu aktivieren oder deaktivieren, indem man die "HID-Tastatur-Simulation" mit einem Tastenbefehl umschaltet.
Die im Folgenden beschriebenen Funktionen der Braille-Tastatur gelten, wenn die "HID-Tastatur-Simulation" deaktiviert ist.

#### Funktionen der Braille-Tastatur {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Löschen des zuletzt eingegebenen Zeichens auf der Braillezeile oder des letzten Zeichens |`backspace`|
|Übersetzt eine beliebige Braille-Eingabe und betätigt die Eingabetaste |`Rücktaste+Leertaste`|
|`NVDA`-Taste umschalten |`Leertaste+Punkt3+Punkt5`|
|`Einfg` |`Leertaste+Punkt1+Punkt3+Punkt5`, `Leertaste+Punkt3+Punkt4+Punkt5`|
|`Entf` |`Leertaste+Punkt3+Punkt6`|
|`Pos1` |`Leertaste+Punkt1+Punkt2+Punkt3`|
|`Ende` |`Leertaste+Punkt4+Punkt5+Punkt6`|
|`Pfeiltaste nach links` |`Leertaste+Punkt2`|
|`Pfeiltaste nach rechts` |`Leertaste+Punkt5`|
|`Pfeiltaste nach oben` |`Leertaste+Punkt1`|
|`Pfeiltaste nach unten` |`Leertaste+Punkt6`|
|`Seite nach oben` |`Leertaste+Punkt1+Punkt3`|
|`Seite nach unten` |`Leertaste+Punkt4+Punkt6`|
|`Nummernblock 1` |`Rücktaste+Punkt1+Punkt6`|
|`Nummernblock 2` |`Rücktaste+Punkt1+Punkt2+Punkt6`|
|`Nummernblock 3` |`Rücktaste+Punkt1+Punkt4+Punkt6`|
|`Nummernblock 4` |`Rücktaste+Punkt1+Punkt4+Punkt5+Punkt6`|
|`Nummernblock 5` |`Rücktaste+Punkt1+Punkt5+Punkt6`|
|`Nummernblock 6` |`Rücktaste+Punkt1+Punkt2+Punkt4+Punkt6`|
|`Nummernblock 7` |`Rücktaste+Punkt1+Punkt2+Punkt4+Punkt5+Punkt6`|
|`Nummernblock 8` |`Rücktaste+Punkt1+Punkt2+Punkt5+Punkt6`|
|`Nummernblock 9` |`Rücktaste+Punkt2+Punkt4+Punkt6`|
|`Nummernblock-Einfügen` |`Rücktaste+Punkt3+Punkt4+Punkt5+Punkt6`|
|`Nummernblock-Dezimalzeichen` |`Rücktaste+Punkt2`|
|`Nummernblock-Schrägstrich` |`Rücktaste+Punkt3+Punkt4`|
|`Nummernblock-Stern` |`Rücktaste+Punkt3+Punkt5`|
|`Nummernblock-Minus` |`Rücktaste+Punkt3+Punkt6`|
|`Nummernblock-Plus` |`Rücktaste+Punkt2+Punkt3+Punkt5`|
|`Nummernblock-Eingabetaste` |`Rücktaste+Punkt3+Punkt4+Punkt5`|
|`Escape`-Taste |`Leertaste+Punkt1+Punkt2+Punkt4+Punkt5`, `l2`|
|`Tab`-Taste |`Leertaste+Punkt2+Punkt5+Punkt6`, `l3`|
|`Umschalt+Tab` |`Leertaste+Punkt2+Punkt3+Punkt5`|
|`Drucken`-Taste |`Leertaste+Punkt1+Punkt3+Punkt4+Punkt6`|
|`Pause`-Taste |`Leertaste+Punkt1+Punkt4`|
|`Kontextmenü`-Taste |`Rücktaste+Punkt5+Punkt6`|
|`F1`-Taste |`Rücktaste+Punkt1`|
|`F2`-Taste |`Rücktaste+Punkt1+Punkt2`|
|`F3`-Taste |`Rücktaste+Punkt1+Punkt4`|
|`F4`-Taste |`Rücktaste+Punkt1+Punkt4+Punkt5`|
|`F5`-Taste |`Rücktaste+Punkt1+Punkt5`|
|`F6`-Taste |`Rücktaste+Punkt1+Punkt2+Punkt4`|
|`F7`-Taste |`Rücktaste+Punkt1+Punkt2+Punkt4+Punkt5`|
|`F8`-Taste |`Rücktaste+Punkt1+Punkt2+Punkt5`|
|`F9`-Taste |`Rücktaste+Punkt2+Punkt4`|
|`F10`-Taste |`Rücktaste+Punkt2+Punkt4+Punkt5`|
|`F11`-Taste |`Rücktaste+Punkt1+Punkt3`|
|`F12`-Taste |`Rücktaste+Punkt1+Punkt2+Punkt3`|
|`Windows`-Taste |`Leertaste+Punkt1+Punkt2+Punkt4+Punkt5+Punkt6`|
|`Windows`-Taste umschalten |`Rücktaste+Punkt1+Punkt2+Punkt3+Punkt4`, `Leertaste+Punkt2+Punkt4+Punkt5+Punkt6`|
|`Dauergroßschreibtaste` |`Rücktaste+Punkt7`, `Rücktaste+Punkt8`|
|`Nummernblock`-Taste |`Rücktaste+Punkt3`, `Rücktaste+Punkt6`|
|`Umschalt`-Taste |`Leertaste+Punkt7`|
|`Umschalt`-Taste umschalten |`Leertaste+Punkt1+Punkt7`, `Leertaste+Punkt4+Punkt7`|
|`Strg`-Taste |`Leertaste+Punkt7+Punkt8`|
|`Strg`-Taste umschalten |`Leertaste+Punkt1+Punkt7+Punkt`, `Leertaste+Punkt4+Punkt7+Punkt8`|
|`Alt`-Taste |`Leertaste+Punkt8`|
|`Alt`-Taste umschalten |`Leertaste+Punkt1+Punkt8`, `Leertaste+Punkt4+Punkt8`|
|HID-Tastatur-Simulation umschalten |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### Tastaturbefehle für EuroBraille b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärts navigieren |`backward`|
|Auf der Braillezeile vorwärts navigieren |`forward`|
|Zum aktuellen Fokus wechseln |`backward+forward`|
|Zum aktuellen Braille-Modul wechseln |`routing`|
|`Pfeiltaste nach links` |`joystick2Left`|
|`Pfeiltaste nach rechts` |`joystick2Right`|
|`Pfeiltaste nach oben` |`joystick2Up`|
|`Pfeiltaste nach unten` |`joystick2Down`|
|`Eingabetaste` |`joystick2Center`|
|`Escape`-Taste |`c1`|
|`Tab`-Taste |`c2`|
|`Umschalt`-Taste umschalten |`c3`|
|`Strg`-Taste umschalten |`c4`|
|`Alt`-Taste umschalten |`c5`|
|`NVDA`-Taste umschalten |`c6`|
|`Strg+Pos1` |`c1+c2+c3`|
|`Strg+Ende` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### b.note-Tastaturbefehle {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der braillezeile rückwärts navigieren |`leftKeypadLeft`|
|Auf der Braillezeile vorwärts navigieren |`leftKeypadRight`|
|Zum aktuellen Braille-Modul wechseln |`routing`|
|Textformatierungen unter dem Braille-Modul ausgeben |`doubleRouting`|
|Zur nächsten Zeile in der Übersicht wechseln |`leftKeypadDown`|
|Zum vorherigen Darstellungsmodus wechseln |`leftKeypadLeft+leftKeypadUp`|
|Zum nächsten Darstellungsmodus wechseln |`leftKeypadRight+leftKeypadDown`|
|`Pfeiltaste nach links` |`rightKeypadLeft`|
|`Pfeiltaste nach rechts` |`rightKeypadRight`|
|`Pfeiltaste nach oben` |`rightKeypadUp`|
|`Pfeiltaste nach unten` |`rightKeypadDown`|
|`Strg+Pos1` |`rightKeypadLeft+rightKeypadUp`|
|`Strg+Ende` |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Esys-Tastaturbefehle {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Braillezeile rückwärts navigieren |`switch1Left`|
|Braillezeile vorwärts navigieren |`switch1Right`|
|Zum aktuellen Fokus wechseln |`switch1Center`|
|Zum aktuellen Braille-Modul wechseln |`routing`|
|Textformatierungen unter dem Braille-Modul ausgeben |`doubleRouting`|
|Zur vorherigen Zeile in der Übersicht wechseln |`joystick1Up`|
|Zur nächsten Zeile in der Übersicht wechseln |`joystick1Down`|
|Zum vorherigen Zeichen in der Übersicht wechseln |`joystick1Left`|
|Zum nächsten Zeichen in der Übersicht wechseln |`joystick1Right`|
|`Pfeiltaste nach links` |`joystick2Left`|
|`Pfeiltaste nach rechts` |`joystick2Right`|
|`Pfeiltaste nach oben` |`joystick2Up`|
|`Pfeiltaste nach unten` |`joystick2Down`|
|`Eingabetaste` |`joystick2Center`|

<!-- KC:endInclude -->

#### Esytime-Tastaturbefehle {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der braillezeile rückwärts navigieren |`l1`|
|Auf der braillezeile vorwärts navigieren |`l8`|
|Zum aktuellen Fokus wechseln |`l1+l8`|
|Zum aktuellen Braille-Modul wechseln |`routing`|
|Textformatierungen auf dem Braille-Modul ausgeben |`doubleRouting`|
|Zur vorherigen Zeile in der Übersicht wechseln |`joystick1Up`|
|Zur nächsten Zeile in der Übersicht wechseln |`joystick1Down`|
|Zum vorherigen Zeichen in der Übersicht wechseln |`joystick1Left`|
|Zum nächsten Zeichen in der Übersicht wechseln |`joystick1Right`|
|`Pfeiltaste nach links` |`joystick2Left`|
|`Pfeiltaste nach rechts` |`joystick2Right`|
|`Pfeiltaste nach oben` |`joystick2Up`|
|`Pfeiltaste nach unten` |`joystick2Down`|
|`Eingabetaste` |`joystick2Center`|
|`Escape`-Taste |`l2`|
|`Tab`-Taste |`l3`|
|`Umschalt`-Taste umschalten |`l4`|
|`Strg`-Taste umschalten |`l5`|
|`Alt`-Taste umschalten |`l6`|
|`NVDA`-Taste umschalten |`l7`|
|`Strg+Pos1` |`l1+l2+l3`, `l2+l3+l4`|
|`Strg+Ende` |`l6+l7+l8`, `l5+l6+l7`|
|HID-Tastatur-Simulation |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Nattiq nBraille {#NattiqTechnologies}

NVDA unterstützt Braillezeilen von [Nattiq Technologies](https://www.nattiq.com/), wenn sie über USB angeschlossen sind.
Windows 10 und neuer erkennt die Braillezeilen, sobald sie angeschlossen sind. Wenn Sie ältere Windows-Versionen (unter Win10) verwenden, müssen Sie eventuell USB-Treiber nachinstallieren.
Diese können Sie von der Website des Herstellers beziehen.

Nachfolgend finden Sie die wichtigsten Zuordnungen für die Braillezeilen von Nattiq Technologies mit NVDA.
Wo diese Tasten zu finden sind, entnehmen Sie bitte der Dokumentation der Braillezeile.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Braillezeile rückwärts navigieren |Aufwärts|
|Braillezeile vorwärts navigieren |Abwärts|
|Braillezeile zur vorherigen zeile navigieren |Nach links|
|Braillezeile zur nächsten Zeile navigieren |nach rechts|
|Cursor zum Braille-Modul bewegen |Routing-Taste|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) ist ein separates Programm, mit dem Sie viele weitere Braillezeilen ansteuern können.
Wenn Sie dies vorhaben, installieren Sie [BRLTTY für Windows](https://www.brltty.app/download.html).
Dazu laden Sie sich das neueste Treiberpaket herunter und installieren es. Der Name sieht in etwa wie folgt aus: "brltty-win-4.2-2.exe".
Bei der Konfiguration der Braillezeile und des zu verwendenden Anschlusses, insbesondere bei USB, seien Sie sicher, dass Sie auch die passenden Treiber vom Hersteller bereits auf Ihrem System installiert haben.

Bei Braillezeilen, die eine eigene Braille-Tastatur besitzen, arbeitet BRLTTY die Eingabe von Braillezeichen selbstständig ab.
Die Einstellung der Braille-Eingabetabelle innerhalb von NVDA ist daher wirkungslos.

BRLTTY ist nicht an der automatischen Erkennung von Braillezeilen im Hintergrund beteiligt.

Folgende BRLTTY-Befehle wurden in NVDA zugewiesen.
Bitte lesen Sie hierzu die [BRLTTY-Dokumentation für Tastaturbelegungen](https://brltty.app/doc/KeyBindings/) für Informationen darüber, wie BRLTTY-Befehle an Braillezeilentasten zugewiesen werden können.
<!-- KC:beginInclude -->

| Name |BRLTTY-Befehl|
|---|---|
|Auf der Braillezeile rückwärts navigieren |`fwinlt` (eine Zeilenlänge nach links navigieren)|
|Auf der Braillezeile vorwärts navigieren |`fwinrt` (eine Zeilenlänge nach rechts navigieren)|
|Auf der Braillezeile zur vorherigen Zeile navigieren |`lnup` (eine Zeile nach oben bewegen)|
|Auf der Braillezeile zur nächsten Zeile navigieren |`lndn` (eine Zeile nach unten bewegen)|
|Cursor zum Braille-Modul wechseln |`routing` (Cursor zum Zeichen navigieren)|
|Eingabehilfe umschalten |`learn` (Modus zum Lernen der Tastenbefehle ein- oder ausschalten)|
|Das NVDA-Menü öffnen |`prefmenu` (Einstellungsmenü öffnen/schließen)|
|Konfiguration zurücksetzen |`prefload` (gespeicherte Einstellungen wiederherstellen)|
|Konfiguration speichern |`prefsave` (Einstellungen speichern)|
|Datum und Uhrzeit mitteilen |`time` (Datum und Uhrzeit anzeigen)|
|Die Zeile mitteilen, in der sich der NVDA-Cursor befindet |`say_line` (aktuelle Zeile mitteilen)|
|Alles Vorlesen, NVDA-Cursor verwenden |`say_below` (von der aktuellen Zeile bis zum unteren Rand des Bildschirms alles vorlesen)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Die von Tivomatic hergestellten und in Finnland erhältlichen Caiku Albatross-Geräte können entweder über USB oder seriell angeschlossen werden.
Für die Verwendung dieser Braillezeilen müssen keine speziellen Treiber installiert werden.
Schließen Sie einfach die Braillezeile an und konfigurieren Sie NVDA dafür.

Hinweis: Die Baudrate 19200 wird dringend empfohlen.
Falls erforderlich, stellen Sie die Baudrate im Menü des Braille-Geräts auf 19200 ein.
Obwohl der Treiber eine Baudrate von 9600 unterstützt, kann nicht die Baudrate von der Braillezeile automatisch erkannt werden.
Da 19200 die Standard-Baudrate der Braillezeile ist, versucht der Treiber es zunächst mit dieser.
Wenn die Baudraten nicht übereinstimmen, kann der Treiber ein unerwartetes Verhalten aufweisen.

Nachfolgend finden Sie die Tastenbelegungen für diese Braillezeilen mit NVDA.
Wo diese Tasten zu finden sind, entnehmen Sie bitte der Dokumentation der Braillezeile.
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Zur obersten Zeile in der Übersicht springen |`home1`, `home2`|
|Zur untersten Zeile in der Übersicht springen |`end1`, `end2`|
|Das Navigator-Objekt auf den aktuellen Fokus setzen |`eCursor1`, `eCursor2`|
|Zum aktuellen Fokus wechseln |`cursor1`, `cursor2`|
|Den Mauszeiger auf das aktuelle Navigator-Objekt verschieben |`home1+home2`|
|Das Navigator-Objekt auf das aktuelle Objekt unter dem Mauszeiger setzen und dieses mitteilen |`end1+end2`|
|Den Fokus auf das aktuelle Navigator-Objekt verschieben |`eCursor1+eCursor2`|
|Die Kopplung der braille-Ausgabe umschalten |`cursor1+cursor2`|
|Auf der Braillezeile in die vorherige Zeile navigieren |`up1`, `up2`, `up3`|
|Auf der Braillezeile in die nächste Zeile navigieren |`down1`, `down2`, `down3`|
|Auf der Braillezeile rückwärts navigieren |`left`, `lWheelLeft`, `rWheelLeft`|
|Auf der Braillezeile vorwärts navigieren |`right`, `lWheelRight`, `rWheelRight`|
|Zum Braille-Modul springen |`routing`|
|Textformatierungen unter dem aktuellen Braille-Modul mitteilen |`secondary routing`|
|Umschalten der Darstellung von Kontextinformationen in Braille-Schrift |`attribute1+attribute3`|
|Zwischen den Sprachmodi umschalten |`attribute2+attribute4`|
|Zum vorherigen Darstellungsmodus wechseln (z. B. Objekt, Dokument oder Bildschirm) |`f1`|
|Zum nächsten Darstellungsmodus wechseln (z. B. Objekt, Dokument oder Bildschirm) |`f2`|
|Das Navigator-Objekt zu dem Objekt verschieben, das es enthält |`f3`|
|Das Navigator-Objekt zum ersten Objekt innerhalb des Objekts verschieben |`f4`|
|Das Navigator-Objekt zum vorherigen Objekt verschieben |`f5`|
|Das Navigator-Objekt zum nächsten Objekt verschieben |`f6`|
|Das aktuelle Navigator-Objekt mitteilen |`f7`|
|Informationen über die Position des Textes oder des Objekts am NVDA-Cursor mitteilen |`f8`|
|Braille_einstellungen anzeigen |`f1+home1`, `f9+home2`|
|Teilt den Inhalt der Statusleiste mit und verschiebt das Navigator-Objekt dorthin |`f1+end1`, `f9+end2`|
|Ring der Braille-cursor-Form |`f1+eCursor1`, `f9+eCursor2`|
|Umschalten des Braille-Cursors |`f1+cursor1`, `f9+cursor2`|
|Modus für die Anzeige von Braille-Meldungen wechseln |`f1+f2`, `f9+f10`|
|Auswahl der Anzeige auf der Braillezeile wechseln |`f1+f5`, `f9+f14`|
|Wechseln der Zustände für System-Cursor auf der Braillezeile verschieben, sobald der NVDA-Cursor weitergeleitet wird |`f1+f3`, `f9+f11`|
|Die Standardaktion für das aktuelle Navigator-Objekt ausführen |`f7+f8`|
|Datum/Uhrzeit mitteilen |`f9`|
|Den Batterie-Status und die verbleibende Zeit anzeigen, sofern der Netzstecker nicht eingesteckt ist |`f10`|
|Titelleiste mitteilen |`f11`|
|Statuszeile mitteilen |`f12`|
|Die aktuelle Zeile unter dem Anwendungs-Cursor mitteilen |`f13`|
|Alles Vorlesen |`f14`|
|Das aktuelle Zeichen unter dem NVDA-Cursor mitteilen |`f15`|
|Die Zeile des aktuellen Navigator-Objekts mitteilen, in der sich der NVDA-Cursor befindet |`f16`|
|Das Wort unter dem aktuellen Navigator-Objekt mitteilen, auf dem sich der NVDA-Cursor befindet |`f15+f16`|
|Den NVDA-Cursor zur vorherigen Zeile des aktuellen Navigator-Objekts ziehen und diese mitteilen |`lWheelUp`, `rWheelUp`|
|Den NVDA-Cursor zur nächsten Zeile des aktuellen Navigator-Objekts ziehen und diese mitteilen |`lWheelDown`, `rWheelDown`|
|`Windows-Taste+D` (Desktop in den Vordergrund holen) |`attribute1`|
|`Windows-Taste+E` (Dieser PC) |`attribute2`|
|`Windows-Taste+B` (Infobereich) |`attribute3`|
|`Windows-Taste+I` (Windows-Einstellungen) |`attribute4`|

<!-- KC:endInclude -->

### Standard-HID-Braillezeilen {#HIDBraille}

Dies ist ein experimenteller Treiber für die neue Standard-HID-Braille-Spezifikation, die 2018 von Microsoft, Google, Apple und weiteren Unternehmen, die Hilfstechnologien verwenden, darunter NV Access, vereinbart wurde.
Es besteht die Hoffnung, dass alle zukünftigen Braille-Display-Modelle aller Hersteller dieses Standardprotokoll verwenden, wodurch herstellerspezifische Braille-Treiber überflüssig werden.

Die automatische Erkennung in NVDA unterstützt auch alle Braillezeilen-Modelle, die dieses Protokoll unterstützen.

Im Folgenden sind die aktuellen Tastenbelegungen für diese Braillezeilen aufgeführt:
<!-- KC:beginInclude -->

| Name |Taste|
|---|---|
|Auf der Braillezeile rückwärtsscrollen |Nach links schwenken oder nach oben|
|Auf der Braillezeile vorwärtsscrollen |Nach rechts schwenken oder nach unten|
|Cursor zum Braille-Modul wechseln |Routing set 1|
|Kopplung der Braillezeile umschalten |Pfeiltaste nach oben/unten|
|Pfeiltaste nach oben |Joystick nach oben, D-Pad nach oben oder Leerzeichen+Punkt1|
|Pfeiltaste nach unten |Joystick nach unten, D-Pad nach unten oder Leerzeichen+Punkt4|
|Pfeiltaste nach links |Leerzeichen+Punkt3, Joystick nach links oder D-Pad nach links|
|Pfeiltaste nach rechts |Leerzeichen+Punkt6, Joystick nach rechts oder D-Pad nach rechts|
|Umschalt+Tab |Leertaste+Punkt1+Punkt3|
|Tab |Leertaste+Punkt4+Punkt6|
|Alt |Leertaste+Punkt1+Punkt3+Punkt4 (Leertaste+M)|
|Escape |Leertaste+Punkt1+Punkt5 (Leertaste+E)|
|Eingabetaste |Punkt8, Joystick mittig oder D-Pad mittig|
|Windows-Taste |Leertaste+Punkt3+Punkt4|
|Alt+Tab |Leertaste+Punkt2+Punkt3+Punkt4+Punkt5 (Leertaste+T)|
|NVDA-Menü |Leertaste+Punkt1+Punkt3+Punkt4+Punkt5 (Leertaste+N)|
|Windows-Taste+D (Desktop in den Vordergrund holen) |Leertaste+Punkt1+Punkt4+Punkt5 (Leertaste+d)|
|Alles Vorlesen |Leertaste+Punkt1+Punkt2+Punkt3+Punkt4+Punkt5+Punkt6|

<!-- KC:endInclude -->

## Erweiterte Themen {#AdvancedTopics}
### Geschützter Modus {#SecureMode}

System-Administratoren können NVDA so konfigurieren, dass der unbefugte Systemzugriff eingeschränkt wird.
NVDA erlaubt die Installation von benutzerdefinierten NVDA-Erweiterungen, die beliebigen Code ausführen können, auch wenn NVDA mit Administratorrechten ausgestattet ist.
NVDA erlaubt es Benutzern auch, beliebigen Code über die integrierte Python-Konsole in NVDA auszuführen.
Der geschützte Modus in NVDA verhindert, dass Benutzer ihre NVDA-Konfiguration ändern können und schränkt den nicht autorisierten Systemzugriff ein.

NVDA läuft im geschützten Modus, wenn es bei [geschützten Sicherheitsmeldungen](#SecureScreens) ausgeführt wird, es sei denn, der [System-Parameter](#SystemWideParameters) `serviceDebug` ist aktiviert.
Um NVDA zu zwingen, immer im geschützten Modus zu starten, setzen Sie den `forceSecureMode` [systemweiter Parameter](#SystemWideParameters).
NVDA kann auch im geschützten Modus mit der [Kommandozeilenoption](#CommandLineOptions) `-s` gestartet werden.

Im geschützten Modus sind folgende Dinge deaktiviert:

* Speichern der Konfiguration und anderer Einstellungen auf dem Speichermedium
* Speichern der Tastenbefehle auf dem Speichermedium
* Aktionen im Dialogfeld für die [Konfigurationsprofile](#ConfigurationProfiles) wie z. B. Erstellen, Löschen, Profile umbenennen, etc.
* Verwenden benutzerdefinierter Einstellungspfade mittels [des `-c`-Kommandozeilenbefehls](#CommandLineOptions)
* Aktualisieren von NVDA und Erstellen portabler Versionen
* Der [Store für NVDA-Erweiterungen](#AddonsManager)
* Die [Python-Konsole in NVDA](#PythonConsole)
* Der [Protokoll-Betrachter](#LogViewer) und die Protokollierung
* Der [Braillebetrachter](#BrailleViewer) und der [Sprachausgabenbetrachter](#SpeechViewer)
* Öffnen von externen Dokumenten über das NVDA-Menü, wie z. B. das Benutzerhandbuch oder die Datei der Mitwirkenden.

Bei installierten NVDA-Versionen werden die Konfiguration (einschließlich der NVDA-Erweiterungen) in `%APPDATA%\NVDA` gespeichert.
Um zu verhindern, dass NVDA-Benutzer die Konfiguration oder NVDA-Erweiterungen direkt anpassen können, muss der Benutzerzugriff auf diesen Ordner ebenfalls eingeschränkt werden.

Der Geschützte Modus funktioniert nicht in portablen NVDA-Versionen.
Diese Einschränkung gilt auch für die temporäre NVDA-Version, die beim Starten des Installationsprogramms ausgeführt wird.
In sicheren Umgebungen stellt die Möglichkeit für einen Benutzer, eine portable ausführbare Datei auszuführen, unabhängig vom Sicherheitsmodus das gleiche Sicherheitsrisiko dar.
Es wird erwartet, dass System-Administratoren die Ausführung nicht autorisierter Software auf ihren Systemen einschränken, einschließlich portabler NVDA-Versionen.

NVDA-Benutzer sind oft darauf angewiesen, ihr NVDA-Profil nach ihren Bedürfnissen zu konfigurieren.
Dies kann die Installation und Konfiguration von benutzerdefinierten NVDA-Erweiterungen beinhalten, die unabhängig von NVDA geprüft werden sollten.
Der Geschützte Modus friert quasi Änderungen an der NVDA-Konfiguration ein. Stellen Sie daher sicher, dass NVDA richtig konfiguriert ist, bevor Sie diesen Modus erzwingen.

### Geschützte Sicherheitsmeldungen {#SecureScreens}

NVDA läuft im [geschützten Modus](#SecureMode), wenn es auf sicheren Bildschirmen ausgeführt wird, es sei denn, der [System-Parameter](#SystemWideParameters) `serviceDebug` ist aktiviert.

Wenn NVDA über einen geschützten Bereich ausgeführt wird, verwendet es ein Systemprofil für die Einstellungen.
NVDA-Benutzereinstellungen können kopiert werden [zur Verwendung in geschützten Sicherheitsmeldungen](#GeneralSettingsCopySettings).

Zu den geschützten Sicherheitsmeldungen gehören:

* Der Fenster der Windows-Anmeldung
* Das Dialogfeld der Benutzerkontensteuerung, welches angezeigt wird, wenn eine Aktion als Administrator ausgeführt wird
  * Dazu gehört die Installation von Programmen

### Befehlszeilenoptionen {#CommandLineOptions}

Mit Hilfe von Befehlszeilenoptionen können Sie das Verhalten von NVDA beeinflussen.
Sie können beliebig viele Optionen angeben.
Sie können die Befehlszeilenoptionen entweder in den Eigenschaften einer Verknüpfung, im Dialogfeld "Ausführen" oder in einer Eingabeaufforderung eingeben.
Kommandozeilenoptionen müssen vom Namen der ausführbaren Datei von NVDA sovie voneinander durch Leerzeichen getrennt werden.
Eine nützliche Option ist beispielsweise "-disable-addons", die NVDA anweist, alle laufenden NVDA-Erweiterungen auszusetzen.
So können Sie beispielsweise feststellen, ob ein Problem durch eine bestimmte Erweiterung verursacht wird.

Mit dem folgenden Befehl können Sie über das Dialogfeld "Ausführen" eine laufende NVDA-Instanz beenden:

    nvda -q

Einige Befehlszeilenoptionen besitzen eine kurze und eine Lange Form und wiederum einige nur eine lange Form.
Die Kurzformen mehrerer Optionen können beispielsweise wie folgt kombiniert werden:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc <Konfigurationspfad>` |Dadurch wird NVDA mit Starttönen und deaktivierter Meldung sowie der angegebenen Konfiguration gestartet.|
|`nvda -mc <Konfigurationspfad> --disable-addons` |Wie zuvor, jedoch mit deaktivierten NVDA-Erweiterungen.|

Einige Optionen akzeptieren zusätzliche Parameter, mit denen Sie z. B. den Umfang der Protokollierung oder den Namen einer Konfigurationsdatei angeben können.
Die Parameter müssen durch ein Leerzeichen von der Option getrennt angegeben werden, wenn Sie die Kurzform verwenden. Wenn Sie die Langform benutzen, müssen Sie den Parameter mit einem Gleichheitszeichen von der Option trennen. Beispiele:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Startet NVDA mit der Protokollierungsstufe "Debug".|
|`nvda --log-file=C:\NVDA.log` |Speichert das Protokoll in der Datei "C:\NVDA.log".|
|`nvda --log-level=20 -f C:\NVDA.log` |Legt die Protokollierungsstufe "Informationen" fest und speichert das Protokoll in der Datei C:\nvda.log.|

Folgende Kommandozeilenoptionen stehen zur Verfügung:

| Kurzform |Langform |Beschreibung|
|---|---|---|
|`-h` |`--help` |Zeigt eine Hilfe zur Befehlszeile an und beendet NVDA.|
|`-q` |`--quit` |Beendet eine laufende Instanz von NVDA.|
|`-k` |`--check-running` |Prüft, ob NVDA bereits ausgeführt wird. Falls ja, wird ein Fehlercode 0 zurückgegeben, anderenfalls wird 1 zurückgegeben.|
|`-f <Protokolldateiname>` |`--log-file=<Protokolldateiname>` |Legt die Datei fest, in der die Protokollierung stattfinden soll. Die Protokollierung ist im geschützten Modus immer deaktiviert.|
|`-l <Protokollierungsstufe>` |`--log-level=<Protokollierungsstufe>` |Die niedrigste Stufe der protokollierten Meldung (Debug 10, Eingabe/Ausgabe 12, Debug-Warnungen 15, Info 20, Ausgeschaltet 100). Die Protokollierung ist im geschützten Modus immer deaktiviert.|
|`-c <Konfigurationspfad>` |`--config-path=<KonfigurationsPfad>` |Gibt den Ordner an, in dem alle NVDA-Einstellungen gespeichert werden sollen. Der Standardwert wird erzwungen, wenn der geschützte Modus aktiviert ist.|
|Keine |`--lang=<Sprache>` |Setzen Sie die konfigurierte NVDA-Sprache außer Kraft. Setzen Sie "Windows" als Standard für den aktuellen Benutzer, "de" für Deutsch, etc.|
|`-m` |`--minimal` |Startet NVDA minimalistisch (keine Klänge, keine Benutzeroberfläche).|
|`-s` |`--secure` |Startet NVDA im [geschützten Modus](#SecureMode)|
|Keine |--disable-addons |Deaktiviert alle NVDA-Erweiterungen.|
|Keine |`--debug-logging` |Aktivieren Sie die Protokollierung nur für diesen `Sitzung. Diese Einstellung überschreibt alle anderen Argumente der Protokollebene ( --loglevel, -l), einschließlich der Option keine Protokollierung.|
|Keine |`--no-logging` |Deaktivieren Sie die Protokollierung vollständig, während Sie NVDA verwenden. Diese Einstellung kann überschrieben werden, wenn eine Protokollebene ("--loglevel"", -l) von der Kommandozeile aus angegeben wird oder wenn die Debug-Protokollierung eingeschaltet ist.|
|Keine |`--no-sr-flag` |Keine Mitteilung in Windows über einen installierten Screenreader.|
|Keine |`--install` |Installiert NVDA ohne Ausgabe von Rückmeldungen und startet die neu installierte Version.|
|Keine |`--install-silent` |Installiert NVDA ohne Ausgabe von Rückmeldungen, startet die Version aber nicht.|
|Keine |`--enable-start-on-logon=True/False` |Aktivieren Sie bei der Installation [NVDA bei der Windows-Anmeldung starten](#StartAtWindowsLogon).|
|Keine |`--copy-portable-config` |Kopieren Sie bei der Installation die portable Konfiguration vom angegebenen Pfad (-c, --config-path) in das aktuelle Benutzerkonto.|
|Keine |`--create-portable` |Erstellt und startet eine neue portable NVDA-Version. Hierfür müssen Sie außerdem den Parameter --portable-path angeben.|
|Keine |`--create-portable-silent` |Erstellt eine neue portable NVDA-Version, ohne diese zu starten. Hierfür müssen Sie außerdem den Parameter --portable-path angeben.|
|Keine |`--portable-path=Ordner` |Gibt den Ordner an, in dem die portable Version erstellt werden soll.|

### Systemweite Parameter {#SystemWideParameters}

Sie können einige Werte in der Registrierungs-Datenbank von Windows verwenden, um das Verhalten von NVDA zu beeinflussen.
Diese Werte werden unter einem der folgenden Schlüssel gespeichert:

* Für 32-Bit-Systeme: `HKEY_LOCAL_MACHINE\SOFTWARE\NVDA`
* Für 64-Bit-Systeme: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\NVDA`

Die folgenden Werte können geändert werden:

| Name |Typ |Mögliche Werte |Beschreibung|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (Standard) zum Deaktivieren, 1 zum Aktivieren |Wenn aktiviert, wird die Benutzerkonfiguration von NVDA in den lokalen Anwendungsdaten statt in den Roaming-Anwendungsdaten gespeichert.|
|`serviceDebug` |DWORD |0 (Standard) zum Deaktivieren, 1 zum Aktivieren |Wenn aktiviert, wird der [Geschützte Modus](#SecureMode) auf [geschützte Sicherheitsmeldungen](#SecureScreens) deaktiviert. Auf Grund mehrerer wichtiger Sicherheitsaspekte wird von der Verwendung dieser Option dringend abgeraten.|
|`forceSecureMode` |DWORD |0 (Standard) zum Deaktivieren, 1 zum Aktivieren |Wenn aktiviert, wird die Aktivierung des [Geschüttzten Modus](#SecureMode) bei der Ausführung von NVDA erzwungen.|

## Weitere Informationen {#FurtherInformation}

Wenn Sie weitere Informationen oder Hilfe bezüglich NVDA benötigen, besuchen Sie bitte die [Internetseite von NVDA](NVDA_URL).
Neben Ressourcen der Community und dem technischen Support finden Sie auch zusätzliche Dokumentationen.
Auf diesen Seiten werden Informationen und Ressourcen zur NVDA-Entwicklung ebenfalls bereitgestellt.

