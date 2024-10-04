# Co nowego w NVDA?

## 2024.3

Add-on store od teraz powiadamia o dostępności aktualizacji dodatków po uruchomieniu NVDA.

Dodano opcje do włączenia normalizacji unicode, obejmującą mowę i brajl.
To może być użyteczne podczas czytania znaków,  nierozpoznawalnych przez syntezator mowy albo znaków niezdefiniowanych w tablicy brajlowskiej. Takie znaki zazwyczaj posiadają zgodną alternatywę. Są to na przykład litery pogrubione lub kursywne, zazwyczaj używane w mediach społecznościowych.
Ta opcja także umożliwia czytanie równań w edytorze równań programu Microsoft Word.

Monitory brajlowskie Help Tech Activator Pro od teraz są wspierane.

Dodano nieprzydzielone skróty klawiszowe do pionowej i poziomej nawigacji kółkiem myszy.

Naprawione niektóre błędy ogólnie w panelu Emoji w systemie Windows 11 i historii schowka.
Naprawiono błędy także w przeglądarkach internetowych.  Poprawki dotyczą komunikatów o zgłaszaniu błędów, odczytu figur i podpisów, oznaczeń tabel a także elementów meni pól wyboru/przycisków opcji.

Liblouis został zaktualizowany z dodanymi nowymi tablicami brajlowskimi dla serbskiej cyrylicy, Jidysz, kilka starożytnych języków, tureckiego i międzynarodowego alfabetu fonetycznego.
eSpeak został zaktualizowany z dodanym wsparciem dla języka karakałpackiego.
Unicode CLDR także został zaktualizowany.

### Nowości

* Nowe skróty klawiszowe:
  * Dodano nieprzydzielone polecenia do przewijania kółka myszy w lewo, prawo górę i w dół w celu ulepszenia nawigacji po web stronach i aplikacjach z treścią dynamiczną, takich jak Dism++. (#16462, @Cary-Rowen)
* Dodano opcje do normalizacji unicode, obejmującą mowę i brajl. (#11570, #16466 @LeonarddeR).
  * To może być użyteczne podczas czytania znaków,  nierozpoznawalnych przez syntezator mowy albo znaków niezdefiniowanych w tablicy brajlowskiej. Takie znaki zazwyczaj posiadają zgodną alternatywę. Są to na przykład litery pogrubione lub kursywne, zazwyczaj używane w mediach społecznościowych.
  * Ta opcja także umożliwia czytanie równań w edytorze równań programu Microsoft Word. (#4631)
  * Tą opcje można włączyć oddzielnie dla brajla i mowy w przeznaczonych do tego kategoriach w ustawieniach NVDA.
* Od teraz, domyślnie po uruchomieniu NVDA, wyświetli się powiadomienie o dostępnych aktualizacjach dodatków. (#15035)
  * To można wyłączyć w kategorii "Add-on Store" ustawień.
  * NVDA sprawdza aktualizacje dodatków dziennie.
  * Aktualizacje dodatków będą sprawdzane z jednego kanału. Na przykład, zainstalowane dodatki z kanału beta będą sprawdzane z kanału beta.
* Dodano wsparcie dla monitorów brajlowskich Help Tech Activator Pro. (#16668)

### Zmiany

* Aktualizacje komponentów:
  * eSpeak NG został zaktualizowany do 1.52-dev commit `54ee11a79`. (#16495)
    * Dodany nowy język karakałpacki.
  * Zaktualizowano Unicode CLDR do wersji 45.0. (#16507, @OzancanKaratas)
  * Zaktualizowano fast_diff_match_patch (używany do wykrywania zmian w aplikacjach konsolowych i innych treściach dynamicznych) do wersji 2.1.0. (#16508, @codeofdusk)
  * Zaktualizowano LibLouis braille translator to [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0). (#16652, @codeofdusk)
    * Nowe tablice brajlowskie:
      * Serbski cyrylica.
      * Jidysz.
      * niektóre języki starożytne: hebrajski biblijny, akadyjski, syryjski, ugarycki i transliterowany tekst pisma klinowego.
      * tureckie skróty. (#16735)
      * międzynarodowy alfabet fonetyczny. (#16773)
  * Zaktualizowano NSIS do wersji 3.10 (#16674, @dpy013)
  * Zaktualizowano markdown do wersji 3.6 (#16725, @dpy013)
  * Zaktualizowano nh3 to 0.2.17 (#16725, @dpy013)
* Alternatywna tablica brajlowska do wpisywania znaków na monitorze brajlowskim od teraz jest taka sama jak alternatywna tablica brajlowska wyświetlania. Jest to Ujednolicony brajl angielski (UEB) pismo pełne. (#9863, @JulienCochuyt, @LeonarddeR)
* Figury bez dostępnych obiektów podrzędnych, ale z dostępną oznaką lub opisem będą odczytywane przez NVDA. (#14514)
* Podczas czytania po wierszach w trybie czytania, słowo "podpis" nie jest już wymawiane w każdej linii długiej figury lub podpisu tabeli. (#14874)
* W konsoli  Pythona ostatnie niewypełnione polecenie nie będzie stracone podczas przemieszczania się po historii wejścia. (#16653, @CyrilleB79)
* Od teraz podczas zbierania statystyk do NV access wysyłany jest unikatowy identyfikator użytkownika. (#16266)
* Podczas tworzenia przenośnej kopii, będzie tworzony nowy katalog.
Od teraz, jeżeli zostanie podjęta próba pisania do pełnego katalogu, będzie pokazane ostrzeżenie. (#16686)

### Poprawki błędów

* Poprawki dla Windowsa 11:
  * NVDA już nie będzie się zawieszała podczas zamykania panelu emoji i historii schowka. (#16346, #16347, @josephsl)
  * NVDA znowu będzie czytała widoczne kandydaty podczas otwarzania interfejsu Ime. (#14023, @josephsl)
  * NVDA nie będzie czytała dwukrotnie "historia schowka" podczas poruszania się po elementach meni panelu emoji. (#16532, @josephsl)
  * NVDA już nie będzie wycinała mowę i brajl podczas przeglądu symboli i kaomoji w panelu emoji. (#16533, @josephsl)
* Poprawki dla przeglądarek internetowych:
  * Komunikaty o błędach z odwołaniem do atrybutu  `aria-errormessage` od teraz są czytane w przeglądarkach Google Chrome i Mozilla firefox. (#8318)
  * Jeżeli są dostępne, NVDA będzie używała atrybutu `aria-labelledby` aby dostarczyć dostępne nazwy dla tabel w przeglądarce Mozilla Firefox. (#5183)
  * NVDA od teraz poprawnie będzie czytać elementy meni w postaci przycisków opcji i pól wyboru podczas pierwszego wejścia do meni rozwijanego w przeglądarkach Google Chrome i Mozilla Firefox. (#14550)
  * Funkcja wyszukiwania NVDA od teraz jest bardziej dokładniejsza gdy strona internetowa zawiera znaki emoji. (#16317, @LeonarddeR)
  * W przeglądarce  Mozilla Firefox, NVDA od teraz poprawnie odczytuje bieżący znak, słowo oraz wiersz gdy kursor znajduje się w punkcie wstawiania na końcu wiersza. (#3156, @jcsteh)
  * Google chrome już nie wysypuje się w procesie zamykania. (#16893)
* NVDA od teraz prawidłowo czyta podpowiedzi autouzupełniania w Eclipse i innych środowiskach opartych na Eclipse w systemie Windows 11. (#16416, @thgcode)
* Ulepszona niezawodność automatycznego odczytu, ogólnie w aplikacjach konsolowych. (#15850, #16027, @Danstiv)
* Przywracanie konfiguracji stało się bardziej niezawodne. (#16755, @Emil-18)
* NVDA poprawnie odczyta zmiany zaznaczenia podczas edycji tekstu komórki w programie Microsoft Excel. (#15843)
* W programach wykorzystujących technologię Java Access Bridge, NVDA poprawnie przeczyta ostatni pusty wiersz tekstu zamiast powtarzania przedostatniego. (#9376, @dmitrii-drobotov)
* W programie LibreOffice Writer (wersji 24.8 i nowszych), podczas włączania lub wyłączania formatowania tekstu (pogrubienie, kursywa, podkreślenie, indeks dolny/indeks górny, wyrównanie) używając odpowiednich skrótów klawiszowych, NVDA przeczyta włączony atrybut formatowania (np. "pogrubienie tak", "pogrubienie nie"). (#4248, @michaelweghorn)
* Podczas poruszania się klawiszami strzałek w polach edycyjnych w programach używających interfejsu UI Automation, NVDA już nie odczytuje błędnego znaku, słowa, itd. (#16711, @jcsteh)
* Podczas wklejania do Kalkulatora w systemach Windows 10/11 NVDA od teraz przeczyta pełną liczbę. (#16573, @TristanBurchett)
* Mowa już nigdy więcej nie zniknie podczas ponownego podłączenia do sesji pulpitu zdalnego. (#16722, @jcsteh)
* Dodano wsparcie poleceń przeglądu tekstu dla nazwy obiektu w Visual Studio Code. (#16248, @Cary-Rowen)
* Od teraz dźwięk będzie poprawnie odtwarzany na audiourządzeniach mono. (#16770, @jcsteh)
* NVDA od teraz przeczyta adresy podczas nawigacji po polach do/dw/UDW w programach outlook.com i współczesnym Outlooku. (#16856)
* NVDA od teraz lepiej radzi z niepoprawnie zainstalowanymi dodatkami. (#16704)

### Changes for Developers

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

Dodano nową funkcję "podzielony dźwięk".
Ta funkcja umożliwia rozdzielenie dźwięku NVDA na przykład w lewym kanale gdy dźwięki z innych programów będą przekierowane do innego kanału na przykład prawego.

Dodano nowe polecenia do modyfikowania ustawień w pierścieniu ustawień mowy, tym samym umożliwiając użytkownikowi przemieszczanie sie od pierwszego do ostatniego ustawienia, a także do zmniejszania lub zwiększania ustawień w większych krokach.
Dodano także nowe polecenia do szybkiej nawigacji, umożliwiając użytkownikowi przemieszczanie się pomiędzy: akapitami, pionowo wyrównanymi akapitami, tekstem tego samego stylu, tekstem różnego stylu, elementami menu, przyciskami przełączania, paskami postępu, figurami, i formułami matematycznymi.

Dodano dużo nowych funkcji brajla, wraz z poprawkami błędów.
Nowy tryb brajla "wyświetlanie mowy" został dodany.
Gdy jest aktywny, monitor brajlowski dokładnie pokazuje, co NVDA wymówi.
Dodano także wsparcie do monitorów brajlowskich BrailleEdgeS2, BrailleEdgeS3.
Zaktualizowano LibLouis dodając nowe tablice brajlowskie z włączonym pokazywaniem wielkich liter dla języków białoruskiego i ukraińskiego, nową tablicę brajlowską do jezyka laotańskiego, a także   tablicę brajlowską dla języka hiszpańskiego ze wsparciem odczytu greki.

eSpeak został zaktualizowany z dodanym nowym językiem Tigrinya.

Naprawiono dużo błędó w aplikacjach, takich jak Thunderbird, Adobe Reader, przeglądarkach internetowych, Nudi i Geekbench.

### Nowości

* Nowe skróty klawiszowe:
  * Nowy skrót szybkiej nawigacji `p` do przemieszczania się po akapitach tekstu w trybie czytania. (#15998, @mltony)
  * Nowe nieprzydzielone skróty szybkiej nawigacjido przemieszczania się po:
    * figurach (#10826)
    * pionowo wyrównanych akapitach (#15999, @mltony)
    * elementach menu (#16001, @mltony)
    * przyciskach przełączania (#16001, @mltony)
    * paskach postępu (#16001, @mltony)
    * formułach matematycznych (#16001, @mltony)
    * tekstach tego samego stylu (#16000, @mltony)
    * tekstach o różnych stylach (#16000, @mltony)
  * Dodano polecenia do przemieszczania się po pierwszym i ostatnim ustawieniu pierścienia mowy. (#13768, #16095, @rmcpantoja)
    * Ten skrót nie jest domyślnie skojarzony. (#13768)
    * Zmniejszanie lub zwiększanie ustawień pierścienia mowy większymi krokami (#13768):
      * dla komputerów stacjonarnych: `NVDA+control+pageUp` or `NVDA+control+pageDown`.
      * dla komputerów przenośnych: `NVDA+control+shift+pageUp` or `NVDA+control+shift+pageDown`.
  * Dodano nowy nieprzydzielony skrót do regulacji odczytu figur i podpisów. (#10826, #14349)
* Brajl:
  * Dodano wsparcie dla monitorów brajlowskich BrailleEdgeS2 i BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * Dodano nowy tryb brajla "wyświetlanie mowy". (#15898, @Emil-18)
    * Gdy jest aktywny, monitor brajlowski wyświetla to, co NVDA wymawia.
    * można go włączać lub wyłączać za pomocą skrótu `NVDA+alt+t`, lub z okna dialogowego ustawień brajla.
* Tryb podzielonego dźwięku: (#12985, @mltony)
  * Ta funkcja umożliwia rozdzielenie dźwięku NVDA na przykład w lewym kanale gdy dźwięki z innych programów będą przekierowane do innego kanału na przykład prawego.
  * Można przełączać za pomocą `NVDA+alt+s`.
* Odczyt nagłówków wierszy i kolumn w HTML elementach contenteditable. (#14113)
* Dodano opcję do wyłączenia odczytu figur i podpisów w ustawieniach formatowania dokumentów. (#10826, #14349)
* W systemie Windows 11, NVDA będzie odczytywała alerty pochodzące od wpisywania głosowego, a także sugerowane działania, wraz z działaniem o kopiowaniu danych, takich jak numerów telefonów do schowka (Windows 11 aktualizacja 2022 i nowsze). (#16009, @josephsl)
* NVDA zostawi włączone i obudzone urządzenie dźwiękowe po zatrzymaniu mowy, w celu zapobiegania cięcia następnej wypowiedzi na niektórych urządzeniach audio takich jak słuchawki Bluetooth. (#14386, @jcsteh, @mltony)
* HP Secure Browser jest od teraz wspierany. (#16377)

### Zmiany

* Add-on Store:
  * Minimalna i ostatnia testowana wersja są wyświetlane w rozdziale dla każdego dodatku "inne szczegóły" . (#15776, @Nael-Sayegh)
  * Działanie recenzji społeczności  będzie dostępne we wszystkich kartach właściwości add-on store. (#16179, @nvdaes)
* Aktualizacje komponentów:
  * Zaktualizowano LibLouis Braille translator do wersji [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Nowe tablice brajlowskie z możliwością wyświetlania wielkich liter dla języków białoruskiego i ukraińskiego.
    * Nowa tablica brajlowska dla języka hiszpańskiego ze wsparciem odczytu greki.
    * Nowa tablica brajlowska dla języka laotańskiego, pismo pełne. (#16470)
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit `cb62d93fd7`. (#15913)
    * Dodano nowy język Tigrinya. 
* Zmieniono kilka skrótów klawiszowych dla urządzeń BrailleSense w celu zapobiegania konfliktów ze znakami w tablicy brajlowskiej dla języka francuzkiego. (#15306)
  * `alt+strzałka w lewo` została skojarzona z  `punkt2+punkt7+spacja`
  * `alt+strzałka w prawo` została skojarzona z `punkt5+punkt7+spacja`
  * `alt+strzałka w górę` została skojarzona z `punkt2+punkt3+punkt7+spacja`
  * `alt+strzałka w dół` została skojarzona z `punkt5+punkt6+punkt7+spacja`
* Kropki, najczęściej używane w spisach treści nie są wymawiane na nizkich poziomach symboli. (#15845, @CyrilleB79)

### Poprawki błędów

* Poprawki błędów dla Windows 11:
  * NVDA ponownie może wymawiać podpowiedzi podczas wpisywania na klawiaturze sprzętowej. (#16283, @josephsl)
  * W wersji 24H2 (aktualizacja 2024 i Windows Server 2025), mysz i interakcja dotykiem mogą być używane w szybkich ustawieniach. (#16348, @josephsl)
* Add-on Store:
  * Gdy skrót klawiszowy`ctrl+tab` jest naciśnięty, fokus poprawnie się przemieszcza do nowego bieżącego tytułu karty właściwości. (#14986, @ABuffEr)
  * NVDA nie będzie się ponownie uruchamiała gdy pliki pamięci podręcznej są nieprawidłowe. (#16362, @nvdaes)
* Poprawki dla przeglądarek opartych na silniku Chromium gdy są używane z Uia:
  * Naprawiono błędy, powodujące zawieszanie się NVDA. (#16393, #16394)
  * Klawisz Backspace od teraz działa  prawidłowo w polach edycji logowania w Gmailu. (#16395)
* Klawisz backspace od teraz działa prawidłowo podczas używania programu Nudi 6.1 z włączoną opcją "Przetwarzaj klawisze z innych aplikacji". (#15822, @jcsteh)
* Naprawiono błąd gdy współrzędne dźwiękowe zostaną odtworzone gdy aplikacje znajdują się w trybie uśpienia, a opcja "Sygnalizuj dźwiękiem położenie myszy" jest włączona. (#8059, @hwf1324)
* W programie Adobe Reader, NVDA już nie ignoruje tekstu alternatywnego w formułach ustawionych w plikach Pdf. (#12715)
* Naprawiono błąd, który skutkował niemożliwością odczytu wstążki w programie Geekbench przez NVDA. (#16251, @mzanm)
* Naprawiono rzadki błąd przez który nie wszystkie profile konfiguracji były zachowane. (#16343, @CyrilleB79)
* W Firefoxie i w przeglądarkach opartych na Chromium, NVDA poprawnie wejdzie do trybu fokusu w polach edycyjnych w listach prezentacyjnych (ul / ol). (#16325)
* Stan kolumn jest automatycznie odczytywany podczas zaznaczania kolumn w liście wiadomości w Thunderbirdzie. (#16323)
* Opcja wiersza poleceń `-h`/`--help` ponownie działa prawidłowo. (#16522, @XLTechie)
* Wsparcie dla programu Poedit używanego do tłumaczenia w wersji 3.4 lub nowszej, działa poprawnie podczas tłumaczenia na języki z jedną lub dwie formy liczby mnogiej (na przykład, dla chińskiego i polskiego). (#16318)

### Changes for Developers

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Added a how-to document, explaining the process of building NVDA forks on AppVeyor. (#16293, @XLTechie)

## 2024.1

Dodano nowy tryb mowy "na żądanie".
Gdy tryb mowy na żądanie jest ustawiony, NVDA Nie mówi automatycznie (na przykład, podczas poruszania się strzałkami) ale mówi podczas naciskania skrótów klawiszowych,  które mają za cel wymawianie poszczególnej informacji (na przykład, odczyt tytułu okna).
Od teraz jest możliwe wykluczenie trybów mowy, których nie potrzebujemy z poziomu ustawień mowy w ustawieniach NVDA podczas używania polecenia przełącz tryb mowy (`NVDA+s`).

Od teraz dostępny jest nowy tryb kopiowania z zachowaniem formatowania w trybie czytania , który można przełączać za pomocą skrótu `NVDA+shift+f10`).
Gdy jest włączony, będzie używany tryb zaznaczania Firefoxu.
Polecenie kopiowania tekstu za pomocą skrótu `control+c` zostanie przekierowane do Firefoxa. To spowoduje kopiowane formatowania zamiast czystego tekstu.

Add-on Store wspiera wielokrotne działania (na przykład instalowanie, włączanie dodatków) zaznaczając wiele dodatków
Dodano nowe działanie do otwierania strony z recenzjami dodatku.

Opcje "Karta dźwiękowa" i "tryb przyciszania audio" zostały usunięte z okna dialogowego"wybór syntezatora".
Można je znaleźć w ustawieniach dźwięku, które można otworzyć za pomocą skrótu `NVDA+control+u`.

eSpeak-NG, LibLouis braille translator, i repozytorium znaków Unicode zostały zaktualizowane.
Nowe tablice brajlowskie dla Tajskiego, filipińskiego i rumuńskiego zostały dodane.

Naprawiono dużo błędów, szczególnie z Add-on Storem, wsparciem brajla, wsparciem dla Libre Office, Microsoft Office i wsparciem dźwięku.

### Uwagi

* Ta wersja nie jest zgodna z istniejącymi dodatkami.
* Systemy operacyjne Windows 7 i Windows 8 nie są więcej wspierane.
Windows 8.1 jest minimalną wspieraną wersją systemu Windows.

### Nowości

* Add-on Store:
  * Add-on Store od teraz wspiera wielokrotne działania (na przykład instalowanie, włączanie i wyłączanie dodatków) zaznaczając więcej dodatków. (#15350, #15623, @CyrilleB79)
  * Dodano nowe działanie służace do otwierania  dedykowanej strony do zaopiniowania lub czytania recenzji o dodatku. (#15576, @nvdaes)
* Dodano wsparcie dla Bluetooth niskonapięciowych monitorów brajlowskich HID. (#15470)
* Nowy tryb kopiowania z zachowaniem formatowania przełączany za pomocą  skrótu `NVDA+shift+f10` jest dodany do trybu czytania dla Mprzeglądarki Mozilla firefox.
Gdy jest włączony, zaznaczanie będzie sterowane z poziomu przeglądarki Mozilla firefox.
Polecenie kopiowania tekstu za pomocą skrótu `control+c` zostanie przekierowane do Firefoxa. To spowoduje kopiowanie formatowania zamiast czystego tekstu.
Miewajcie na uwadze, że gdy Firefox steruje kopiowaniem, NVDA nie będzie wymawiała komunikatu "skopiowano do schowka" w tym trybie. (#15830)
* Podczas kopowania tekstu w Programie Microsoft Word w trybie czytania NVDA, formatowanie jest także brane pod uwagę.
Skutek uboczny tej funkcji jest niemożliwość wymawiania komunikatu  "skopiowano do schowka" przez NVDA podczas naciskania skrótu `control+c` w trybie przeglądu Microsoft Word / Outlook, ponieaż te programy sterują kopiowaniem, nie sama NVDA. (#16129)
* Nowy tryb mowy "na żądanie" został dodany.
Gdy ten tryb mowy jest włączony, NVDA nie mówi automatycznie (na przykład, podczas poruszania się kursorem) ale mówi podczas wciskania skrótów klawiszowych, które mają za cel wimawianie konkretnej informacji (na przykład wymawiaj tytuł okna). (#481, @CyrilleB79)
* Od teraz jest możliwe wykluczenie trybów mowy z listy trybów podczas przełączania za pomocą skrótu `NVDA+s`, w ustawieniach NVDA. (#15806, @lukaszgo1)
  * Jeżeli aktualnie używasz dodatku NoBeepsSpeechMode usuń go i wyłącz tryby "dźwięki" i "na żadanie" w ustawieniach.

### Zmiany

* NVDA więcej nie wspiera wersji systemów operacyjnych Windows 7 i Windows 8.
Windows 8.1 jest minimalną wspieraną wersją. (#15544)
* Aktualizacje komponentów:
  * Zaktualizowano LibLouis braille translator do wersji [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Dodano nowe tablice brajlowskie dla tajskiego, rumuńskiego i filipińskiego.
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit `530bf0abf`. (#15036)
  * Tłumaczenie symboli i emoji z repozytorium Cldr zostały zaktualizowane do wersji 44.0. (#15712, @OzancanKaratas)
  * Zaktualizowano Java Access Bridge do wersji 17.0.9+8Zulu (17.46.19). (#15744)
* Skróty klawiszowe:
  * Następujące skróty od teraz wspierają dwukrotne i trzykrotne naciśnięcia dla literowania informacji , a także literowania fonetycznego: odczyt zaznaczenia, odczyt tekstu z schowka i odczyt obiektu w fokusie. (#15449, @CyrilleB79)
  * Od teraz polecenie do włączania i wyłączania kurtyny posiada domyślny skrót klawiszowy: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * Gdy jest naciśnięte czterokrotnie, polecenie do odczytu zaznaczenia od teraz pokazuje zaznaczoną treść w trybie czytania. (#15858, @Emil-18)
* Microsoft Office:
  * Podczas odpytywania o formatowanie komórek w programie Excel, ramki i tło będą odczytywane jeżeli istnieje takie formatowanie. (#15560, @CyrilleB79)
  * NVDA już nie będzie odczytywała nieoznaczone grupowania, takie jak w wstążkach Microsoft Office 365. (#15638)
* Opcje "karta dźwiękowa" i "tryb przyciszania" zostały usunięte z okna dialogowego "wybór syntezatora".
Można je teraz znaleźć w panelu ustawień dźwieku, którego można wywołać za pomocą skrótu `NVDA+control+u`. (#15512, @codeofdusk)
* Nazwa opcji "Oczytaj rolę obiektu podczas poruszania się myszą" w ustawieniach myszy NVDA zostala zmieniona na "Odczytaj obiekt podczas wejścia do niego za pomocą myszy".
Ta opcja od teraz odczytuje inne ważne informacje o obiekcie podczas wejścia do niego myszą, takie jak stan, (zaznaczony /wciśnięty) lub współrzędne komórki z tabeli. (#15420, @LeonarddeR)
* Nowe elementy zostały dodane do meni pomoc "szkolenie i wsparcie" i "sklep NV access". (#14631)
* Wsparcie NVDA dla programu  [Poedit](https://poedit.net) zostało przepisane dla wersji 3 i nowszych.
Użytkownicy programu Poedit 1 są zachęcani do aktualizacji do Poedit 3 jeżeli chcą używać ulepszeń dostępnosci dla programu Poedit, takich jak skróty do odczytu notatek dla tłumaczy i komentarzy. (#15313, #7303, @LeonarddeR)
* Przegląd brajla i mowy od teraz są wyłączone w trybie bezpiecznym. (#15680)
* Podczas używania nawigacji obiektowej, wyłączone, niedostępne obiekty od teraz nie będą więcej ignorowane. (#15477, @CyrilleB79)
* Dodano spis treści do wykazu poleceń. (#16106)

### Poprawki błędów

* Add-on Store:
  * Podczas zmiany stanu aktualnie wybranego dodatku, na przykład zmiana z stanu "pobieranie" na "pobrano", odświeżony element będzie oznajmiany poprawnie. (#15859, @LeonarddeR)
  * Podczas instalacji dodatków, instrukcje instalacji nie nakładają się na okno dialogowe ponownego uruchomienia. (#15613, @lukaszgo1)
  * Podczas ponownej instalacji niezgodnego dodatku taki dodatek już nie jest automatycznie wyłączany. (#15584, @lukaszgo1)
  * Wyłączone i niezgodne dodatki teraz mogąbyć aktualizowane. (#15568, #15029)
  * NVDA od teraz odzyskuje swój proces i pokazuje błąd w przypadku nieudanego pobierania dodatku. (#15796)
  * NVDA od teraz już nie uruchamia się ponownie bez powodu po otwarciu i zamknięciu Add-on store. (#16019, @lukaszgo1)
* Dźwięk:
  * NVDA już nie zawiesza się na długi okres czasu gdy więcej dźwięków odtwarza się bardzo szybko. (#15311, #15757, @jcsteh)
  * Jeżeli karta dźwiękowa jest ustawiona na inną niżdomyślnąwartość,  a ta karta stanie sięponownie dostępna,  po czasie niedostępności, NVDA NVDA przełączy się na skonfigurowaną kartę dźwiękową, zamiast przywracania na domyślne urządzenie. (#15759, @jcsteh)
  * NVDA teraz ponownie odtwarza dźwięk jeżeli konfiguracja karty dźwiękowej konfiguracja zmieni sięlub inna aplikacja nie używa tej karty w trybie wyłączności. (#15758, #15775, @jcsteh)
* Brajl:
  * Wielowierszowe monitory brajlowskie już nie spowodują wysypke sterownika BRLTTY. Te monitoryy traktowane są jako jeden nieskończony monitor brajlowski. (#15386)
  * Od teraz wykrywano jest więcej korzystnych obiektów, a ich treść wyświetlana jest w brajlu. (#15605)
  * Wprowadzanie brajla za pomocą skrótów brajlowskich od teraz znowu działa. (#15773, @aaclause)
  * Brajl jest od teraz odświeżany podczas przemieszczania obiektu nawigatora po komórkach tabeli w więcej przypadkach (#15755, @Emil-18)
  * Wynik odczytu poleceń dla aktualnego obiektu nawigatora, pod kursorem przeglądu i aktualnego zaznaczenia pokazywane są w brajlu. (#15844, @Emil-18)
  * Sterownik Albatross już nie rozpoznaje Esp32 mikroukładu jako monitor brajlowski Albatross. (#15671)
* LibreOffice:
  * Słowa skasowane za pomocą skrótu `control+backspace` od teraz są także wymawiane, jeżeli po słowie następuję biała spacja taka jak spacja i tabulator. (#15436, @michaelweghorn)
  * Oznajmianie paska statusu używając skrótu `NVDA+end` od teraz działą w oknach dialogowych LibreOffice od wersji 24.2 and i nowszych. (#15591, @michaelweghorn)
  * od teraz wszystkie właściwości tekstu w LibreOffice od wersji 24.2 i nowszych są wspierane.
  Ta zmiana spowodowała, że od teraz oznajmianie błędów pisowni działa podczas odczytu wiersza w LibreOffice Writerze. (#15648, @michaelweghorn)
  * Oznajmianie nagłówków od teraz działą w LibreOffice wersji 24.2 i nowszych. (#15881, @michaelweghorn)
* Microsoft Office:
  * w Excelu z wyłączonym wsparciem UIA, brajl jest odświeżany, a bieżaca treść komórki zostanie przeczytana po naciśnięciu `control+y`, `control+z` lub `alt+backspace` . (#15547)
  * W Wordzie z wyłączonym  UIA brajl jest odświeżany po naciśnięciu skrótó `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace` lub `control+backspace`.
  Brajl jest także odświeżany z włączonym UIA, podczas wpisywania tekstu gdy brajl jest ustawiony na przegląd a kursor przeglądu śledzi fokus. (#3276)
  * W Wordzie, początkowe komórki będąwymawiane po naciśnięciu jednej z powyższych poleceń do nawigacji po tabelach `alt+home`, `alt+end`, `alt+pageUp` i `alt+pageDown`. (#15805, @CyrilleB79)
* Odczyt skrótów klawiszowych został ulepszony. (#10807, #15816, @CyrilleB79)
* Syntezator mowy SAPI4 od teraz poprawnie wspiera polecenia zmiany głośnosci , prędkości i wysokości zawarte w mowie. (#15271, @LeonarddeR)
* Stan wielowierszowej kontrolki od teraz jest prawidłowo wymawiany w aplikacjach  używajacych Java Access Bridge. (#14609)
* NVDA potrafi odczytać więcej okien dialogowych w systemie Windows 10 i 11. (#15729, @josephsl)
* NVDA od teraz przeczyta załadowaną stronę w przeglądarce Microsoft Edge podczas używania interfejsu dostępności UI Automation. (#15736)
* Podczas używania polecenia czytaj wszystko oraz poleceń do literowania informacji, pauzy jużnie zmniejszająsię z czasem. (#15739, @jcsteh)
* NVDA już nie zawiesza się w niektóych przypadkach podczas wymawiania dużej ilosci tekstu. (#15752, @jcsteh)
* Podczas używania przeglądarki Microsoft Edge za pomocą interfejsu UI Automation, NVDA od teraz potrafi aktywować więcej kotrolek w trybie czytania. (#14612)
* NVDA od teraz ponownie sięuruchomi gdy konfiguracja zostanie uszkodzona, a konfiguracja zostanie zresetowana, przywracając stan z poprzednich wersji NVDA. (#15690, @CyrilleB79)
* Naprawiono wsparcie dla System List view (`SysListView32`) kontrolek w aplikacjach Windows Forms. (#15283, @LeonarddeR)
* Od teraz już nie jest możliwe nadpisywanie historii NVDA konsssssssoli Python. (#15792, @CyrilleB79)
* NVDA nadal będzie responsywny gdy dostanie dużo zdarzeń  UI automation, na przykład podczas wyświetlania dużej ilości tekstu w konsoli oraz podczas słuchania Whatsappie. (#14888, #15169)
  * To nowe zachowanie można wyłączyć używając nowej opcji "używaj ulepszone przetwarzanie zdarzeń" w zaawansowanych ustawieniach NVDA.
* NVDA od teraz ponownie potrafi śledzić fokus w  aplikachach, uruchomionych wewnątrz Windows Defender Application Guard (WDAG). (#15164)
* Wymówiony tekst już nie jest zaktualizowania podczas poruszania się myszą w przeglądzie mowy. (#15952, @hwf1324)
* NVDA przełączy się ponownie do trybu czytania po zamknięciu list rozwijanych za pomocą `escape` lub `alt+strzałkiWgórę` w Firefoxie lub Chromie. (#15653)
* Poruszanie sięstrzałkami w góręi w dół w iTunes już nie spowoduje niechciane przełączenie do trybu czytania. (#15653)

### Changes for Developers

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

To jest wersja naprawiająca łuki bezpieczeństwa i problem z instalatorem.
Prosimy odpowiedzialnie zgłaszać łuki bezpieczeństwa zgodnie z [Politykąbezpieczeństwa NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki bezpieczeństwa

* Już nie jest możliwe uruchamianie gdy tryb bezpieczny jest wymuszony.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Poprawki błędów

* Naprawiono błąd z niepoprawnym zakończeniem procesu NVDA. (#16123)
* Naprawiono błąd, podczas którego proces programu NVDA mógł niepoprawnie zostać zamknięty, tym samym skutkując w nieodzyskiwalnej instalacji. (#16122)

## 2023.3.3

Jest to wersja naprawiająca łukę bezpieczeństwa.
Prosimy odpowiednio zgłaszać  łuki bezpieczeństwa, śledząc [Politykę bezpieczeństva NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki bezpieczeństwa

* Od teraz zapobiegany jest zwracany atak XSS zbudowanej treści powodujący arbitrarne uruchamianie kodu.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

To jest wersja naprawiająca łukę bezpieczeństwa.
Poprawka bezpieczeństwaw w wersji 2023.3.1 nie została poprawnie wdrożona.
Prosimy odpowiednio zgłaszać  łuki bezpieczeństwa, śledząc [Politykę bezpieczeństva NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki bezpieczeństwa

* Poprawka bezpieczeństwaw w wersji 2023.3.1 nie została poprawnie wdrożona.
Uniemożliwia uruchamianie dowolnego kodu z podwyższonymi uprawnieniami do nieuwierzytelnionych użytkowników.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

To jest wersja naprawiająca łukę bezpieczeństwa.
Prosimy odpowiednio zgłaszać  łuki bezpieczeństwa, śledząc [Politykę bezpieczeństva NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki bezpieczenstwa

* Uniemożliwia uruchamianie dowolnego kodu z podwyższonymi uprawnieniami do nieuwierzytelnionych użytkowników.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Ta wersja zawiera ulepszenia wydajności, responsywności i stabilności dźwięku.
Dodano opcje do kontrolowania głośności dźwięków NVDA, oraz do ich ujednolicania z głośnością mowy.

NVDA potrafi od czasu do czasu odświeżać tekst rozpoznany za pomocą Ocr, wymawiając go po jego natychmiastowym pojawieniu się.
Tą opcję można włączyć w kategorii Windows OCR w oknie dialogowym ustawień NVDA.

Naprawiono kilka problemów z brajlem, naprawiając jednocześnie wykrywanie ruchów kursora i automatyczne wykrywanie monitorów brajlowskich.
W celu ulepszenia wydajności automatycznego wykrywania monitorów brajlowskich, od teraz istnieje możliwość wyłączania niektórych sterowników z tego procesu.
Dodano także nowe polecenia BRLTTY.

Naprawiono błędy w Add-on Store, pakiecie Microsoft Office, menu kontekstowych Microsoft Edge, i kalkulatorze Windows.

### Nowe funkcje

* Ulepszone zarządzanie dźwiękiem:
  * Nowy panel ustawień dźwięku:
    * Można go otworzyć używając skrótu `NVDA+control+u`. (#15497)
    * Dodano opcje, która umożliwia ustawienie spójności głośności dźwięków NVDA. (#1409)
    * Dodano opcję do oddzielnej konfiguracji głośności dźwięków NVDA. (#1409, #15038)
    * Opcje do wyboru karty dźwiękowej i przełączania przyciszania dźwięku zostały przeniesione do nowej kategorii dźwięk w ustawieniach NVDA z okna dialogowego "wybór syntezatora".
    Te opcje będą usunięte z okna dialogowego "wybór syntezatora" w wersji 2024.1. (#15486, #8711)
  * NVDA od teraz będzie dosyłał dźwięk za pomocą interfejsu Windows Audio Session API (WASAPI), co może wpłynąć na stabilność, responsywność i wydajność mowy i dźwięków NVDA. (#14697, #11169, #11615, #5096, #10185, #11061)
  * Uwaga: WASAPI jest niezgodny z niektórymi dodatkami.
  Zgodne aktualizacje dostępne są dla tych dodatków. Zanim zaktualizujesz NVDA, prosimy zaktualizować te dodatki.
  Niezgodne wersje tych dodatków będą wyłączone podczas aktualizacji NVDA:
    * Tony's Enhancements wersja 1.15 lub starsza. (#15402)
    * NVDA global commands extension 12.0.8 lub starsza. (#15443)
* NVDA od teraz potrafi aktualizować wynik OCR, wymawiając nowy tekst gdy się pojawi. (#2797)
  * Aby włączyć tę funkcję, włącz opcję "Od czasu do czasu odświeżaj  treść rozpoznawaną" w kategorii windows Ocr w ustawieniach NVDA.
  * Kiedy ta opcja jest włączona, możesz regulować wymawianie nowego tekstu za pomocą opcji informuj o zmianach treści dynamicznych  (naciskając `NVDA+5`).
* Podczas używania automatycznego wykrywania monitorów brajlowskich, możliwe jest wykluczenie monitorów brajlowskich z procesu automatycznego wykrywania z poziomu okna dialogowego wybór monitora brajlowskiego. (#15196)
* Nowa opcja została dodana do ustawień formatowania dokumentów: "Ignoruj puste linie podczas odczytu wcięć". (#13394)
* Dodano nieprzydzielone zdarzenie wejścia do poruszania się po kartach właściwości w trybie czytania. (#15046)

### Zmiany

* Brajl:
  * Gdy tekst w terminalu zmieni się bez aktualizacji kursora systemowego, monitor brajlowski zostanie poprawnie odświeżony, gdy znajduje się na tej linii.
  To obejmuje sytuacje, podczas któych brajl jest przywiązany do przeglądu. (#15115)
  * Więcej poleceń BRLTTY dostało zdarzenia wejścia NVDA (#6483):
    * `learn`: włącza i wyłącza pomoc klawiatury
    * `prefmenu`: otwiera NVDA menu
    * `prefload`/`prefsave`: przywracanie i zapisywanie konfiguracji NVDA
    * `time`: pokaż czas
    * `say_line`: Wymawia bieżącą linię pod kursorem przeglądu
    * `say_below`: Czyta wszystko za pomocą kursora przeglądu
  * Sterownik BRLTTY jest dostępny tylko gdy kopia BRLTTY jest uruchomiona z uruchomionym BRLAPI. (#15335)
  * Usunięto ustawienie do wyłączenia wsparcia monitorów brajlowskich HID, zastępując je nową opcją.
  Możesz wyłączyć określone sterowniki monitorów brajlowskich z procesu automatycznego wykrywania z okna dialogowego wybór monitora brajlowskiego. (#15196)
* Add-on Store: zainstalowane dodatki będą pokazane na karcie właściwości zainstalowane, jeżeli są dostępne w Add-on store. (#15374)
* Niektóre skróty klawiszowe w NVDA menu zostały zaktualizowane. (#15364)

### Poprawki błędów

* Microsoft Office:
  * Naprawiono sytuacje, w których Microsoft word zawieszał się  gdy opcje "odczytuj nagłówki" i "odczytuj komentarze i notatki" w opcjach formatowania dokumentów nie były włączone. (#15019)
  * W programach Word i Excel, wyrównanie tekstu będzie poprawnie odczytywane w więcej przypadkach. (#15206, #15220)
  * Naprawiono odczyt niektórych skrótów do formatowania komórek w programie Excel. (#15527)
* Microsoft Edge:
  * NVDA już nie będzie skakała z powrotem do poprzedniej pozycji w trybie czytania podczas otwierania menu kontekstowego w Microsoft Edge. (#15309)
  * NVDA znowu potrafi czytać menu kontekstowe pobierania w przeglądarce Microsoft Edge. (#14916)
* Brajl:
  * Kursory brajlowskie i komórki pokazujące zaznaczenie będą zawsze aktualizowane poprawnie podczas ich włączania lub wyłączania skrótem klawiszowym. (#15115)
  * Naprawiono błąd próby inicjalizacji monitorów brajlowskich Albatross, gdy inny monitor brajlowski jest podłączony. (#15226)
* Add-on Store:
  * Naprawiono błąd, który skutkował pokazywaniem niezgodnych dodatków w Add-on store, nawet gdy opcja"Uwzględnij dodatki niezgodne" była wyłączona. (#15411)
  * Dodatki zablokowane z powodów niezgodności powinne być filtrowane poprawnie podczas przełączania  stanu włączonych lub wyłączonych dodatków. (#15416)
  * Naprawiono błąd, który zapobiegał aktualizacjom nadpisanych lub zamienionych dodatków używając narzędzia do zewnętrznej instalacji. (#15417)
  * Naprawiono błąd, podczas którego NVDA nie mówiła do póki nie będzie ponownie uruchomiona po instalacji dodatków. (#14525)
  * Naprawiono błąd, podczas którego dodatki nie mogły być instalowane jeżeli poprzednie pobieranie zostało anulowane, lub instalacja nie powiodła się. (#15469)
  * Naprawiono błędy zarządzania niezgodnymi dodatkami podczas aktualizacji NVDA. (#15414, #15412, #15437)
* NVDA znowu potrafi czytać wyniki w kalkulatorze w jego 32-bitowej wersji w następujących wydaniach systemu operacyjnego windows:Server, LTSC and LTSB. (#15230)
* NVDA więcej nie ignoruje zmian fokusu gdy okno podrzędne dostaje fokus. (#15432)
* Naprawiono potencjalną wysypkę podczas uruchamiania NVDA. (#15517)

### Changes for Developers

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

W tej wersji została wprowadzona funkcja Add-on store, która zamienia menedżer dodatków.
W Add-on Store można przeglądać, wyszukiwać, instalować dodatki stworzone przez społeczność.
Istnieje możliwość ręcznej zmiany zgodności przestarzałych dodatków na własną odpowiedzialność.

Dodano nowe funkcje dotyczące brajla, włączając w to polecenia i wsparcie monitorów brajlowskich.
Dodano nowe skróty klawiszowe do optycznego rozpoznawania znaków  i do spłaszczonego widoku nawigacji obiektowej.
Ulepszono nawigację i odczyt formatowania w Microsoft Office .

Zostały wdrożone liczne poprawki błędów, ogólnie do wsparcia brajla, pakietu Microsoft Office, przeglądarek internetowych i systemu Windows 11.

eSpeak-NG, LibLouis braille translator i Unicode CLDR zostały zaktualizowane.

### Nowości

* Funkcja Add-on Store została dodana do NVDA. (#13985)
  * Przeglądaj, szukaj, instaluj i aktualizuj dodatki napisane przez społeczność.
  * Ręcznie rozwiąż problemy ze zgodnością przestarzałych dodatków.
  * Menedżer dodatków został zamieniony przez Add-on Store.
  * Po więcej informacji, zajrzyj do odświerzonego podręcznika użytkownika.
* Nowe zdarzenia wejścia:
  * Nieprzydzielone zdarzenie wejścia do przełączania się między dostępnymi językami w Windows OCR. (#13036)
  * Nieprzydzielone zdarzenie wejścia do przełącznia się między trybami pokazywania wiadomości na monitorze brajlowskim. (#14864)
  * Nieprzydzielone zdarzenie wejścia do włączania i wyłączania trybu wyświetlania stanu zaznaczenia na monitorze brajlowskim. (#14948)
  * Dodano domyślne zdarzenie wejścia do przemieszczania się między następnym i poprzednim obiektem w spłaszczonym widoku chierachii obiektów. (#15053)
    * Do komputerów stacjonarnych: `NVDA+numeryczne9` i `NVDA+numeryczny3` do przełączania się między poprzednim i następnym obiektem.
    * do komputerów przenośnych: `shift+NVDA+[` i `shift+NVDA+]` do przełączania się między poprzednim i następnym obiektem.
* Nowe funkcje dotyczące brajla:
  * Dodano wsparcie dla monitora brajlowskiego Help Tech Activator. (#14917)
  * Została dodana nowa opcja do włączania i wyłączania pokazywania stanu zaznaczenia (kropki 7 i 8). (#14948)
  * Dodana nowa opcja do nieobowiązkowego przemieszczania kursora systemu oraz fokusu podczas zmiany kursora przeglądu za pomocą przycisków routing. (#14885, #3166)
  * Informacja jest pokazywana w brajlu podczas trzykrotnego naciskania skrótu klawiszowego`numeryczny2` do odczytu wartości numerycznej znaku pod kursorem przeglądu. (#14826)
  * Dodano wsparcie do atrybutu ARIA 1.3 `aria-brailleroledescription,` który umożliwia autorom nadpisywanie typu elementu wyświetlanego na monitorze brajlowskim. (#14748)
  * Sterownik do linijek brajlowskich firmy Baum: dodano kilka skrótów klawiszowych ze spacją do wykonywania niektórych kombinacji klawiszy takich jak `windows+d` i `alt+tab`.
  Aby zobaczyć pełną listę, przeczytaj podręcznik użytkownika. (#14714)
* Dodano wymowę następujących znaków unicode:
  * znaków brajlowskich, takich jak `⠐⠣⠃⠗⠇⠐⠜`. (#13778)
  * Mac klawisza option `⌥`. (#14682)
* Dodano skróty klawiszowe dla monitorów brajlowskich Tivomatic Caiku Albatross. (#14844, #15002)
  * Do pokazywania ustawień brajlowskich
  * Do odczytu paska stanu
  * Do przełączania kształtu kursora brajlowskiego
  * Do przełączania pokazywania komunikatów na monitorze brajlowskim
  * Do włączania lub wyłączania kursora brajlowskiego
  * Do włączania lub wyłączania pokazywania stanu zaznaczenia
  * Do włączania i wyłączania opcji "Przenoś kursor systemowy podczas przywoływania kursoru przeglądu". (#15122)
* Funkcje Microsoft Office:
  * Gdy opcja podświetlony tekst jest włączona w opcjach formatowania, kolor podświetlenia jest  wymawiany w Microsoft Word. (#7396, #12101, #5866)
  * Gdy włączony jest odczyt kolorów w opcjach formatowania dokumentu, kolory tła są odczytywane w Microsoft Word. (#5866)
  * Podczas używania skrótów w programie Microsoft Excel przeznaczonych do formatowania takich jak pogrubienie, kursywa, podkreślenie i przekreślenie komórki, wynik polecenia jest odczytywany. (#14923)
* Experymentalne zarządzanie dźwiękiem:
  * NVDA potrafi odtwarzać audio za pomocą interfejsu Windows Audio Session API (WASAPI), co może polepszyć responsywność, wydajność i stabilność mowy i dźwięków NVDA . (#14697)
  * Używanie WASAPI można włączyć w ustawieniach zaawansowanych.
  Jeżeli  WASAPI jest włączone, można włączyć następujące dodatkowe ustawienia.
    * Opcję do wyrównywania głośności mowy i dźwięków NVDA. (#1409)
    * Opcję do oddzielnego konfigurowania dźwięków NVDA. (#1409, #15038)
  * Istnieje znany problem periodycznego wysypywania się gdy  Wasapi jest włączony. (#15150)
* W przeglądarkach Mozilla Firefox i Google Chrome, NVDA NVDA odczytuje otwarcie dialogu, siatki, listy lub drzewa przez kontrolkę jeżeli autor to określił używając atrybutu `aria-haspopup`. (#8235)
* Od teraz możliwe jest określenie zmiennej takiej jak `%temp%` lub `%homepath%`) w ścieżkach podczas tworzenia kopii przenośnych NVDA. (#14680)
* W systemie operacyjnym Windows 10 aktualizacji z maja 2019 i nowszych wersjach, NVDA potrafi czytać nazwy pulpitów wirtualnych podczas ich otwierania, zmieniania i zamykania. (#5641)
* Dodano ogólnosystemowy parametr umożliwiający użytkownikom i administratorom systemowym wymuszone uruchamianie NVDA w trybie bezpiecznym. (#10018)

### Zmiany

* Zmiany komponentów:
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit `ed9a7bcf`. (#15036)
  * Zaktualizowano LibLouis braille translator do wersji [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR został zaktualizowany do wersji 43.0. (#14918)
* Zmiany w LibreOffice:
  * Podczas odczytywania pozycji kursoru przeglądu, aktualna pozycja kursoru systemowego jest teraz odczytywana względem aktualnej strony w programie LibreOffice Writer 7.6 i nowszych wersjach, podobno do zachowania w programie Microsoft Word. (#11696)
  * Odczyt paska stanu (na przykład wyyzwalany przez skrót klawiszowy `NVDA+end`) funkcjonuje w LibreOffice. (#11698)
  * Podczas przemieszczania się do innej komórki w programie LibreOffice Calc, NVDA już nie odczytuje wspólrzędne  komórki w nieprawidłowy sposób gdy odczyt wspólrzędnych w ustawieniach NVDA jest wyłączony. (#15098)
* Zmiany dotyczące brajla:
  * Podczas używania monitora brajlowskiego za pomocą standardowego sterownika brajlowskiego HID, klawisze dpad mogą być używane symulacji strzałek i entera.
  Skróty klawiszowe `spacja+punkt1` i `spacja+punkt4` od teraz są używane do strzałek. (#14713)
  * Aktualizowana treść dynamiczna na stronach internetowych (aria żywe regiony) od teraz jest wyświetlana w brajlu.
  Można to wyłączyć w panelu ustawien zaawansowanych. (#7756)
* Znaki minus i półpauza zawsze będą wysyłane do syntezatora mowy. (#13830)
* Odczyt dystansu w programie Microsoft Word od teraz będzie respektował jednostkę pomiaru zdefiniowaną w ustawieniach zaawansowanych programu Microsoft Word, nawet podczas używania UIA do odczytu dokumentów Microsoft Word. (#14542)
* NVDA reaguje szybciej podczas nawigacji strzałkami w polach edycyjnych. (#14708)
* Skrót do odczytu docelowej lokalizacji linku od teraz odczytuje z pozycji fokusu a nie z obiektu nawigatora. (#14659)
* Tworzenie kopii przenośnej nie wymaga wpisywania  litery dysku jako części ścieżki absolutnej. (#14680)
* Jeżeli system Windows jest ustawiony tak, że sekundy są pokazywane w zegarze znajdującym sie w zasobniku systemowym, podczas używania  `NVDA+f12` do odczytu czasu od teraz sekundy będą odczytywane. (#14742)
* NVDA od teraz odczyta nieoznaczone grupowania zawierające przydatną informację o pozycji, takie jak menu w ostatnich wersjach pakietu Microsoft Office 365. (#14878)

### Poprawki błędów

* Brajl:
  * Pare usprawnień stabilności dla wprowadzania/wyświetlania brajla, które powodują mniejsze wysypywanie się NVDA. (#14627)
  * NVDA już nie będzie przełączała się niepotrzebnie na monitor brajlowski "bez brajla" wiele razy podczas automatycznego wykrywania, co poskutkuje mniejszym dziennikiem i wązkim gardłem informacyjnym. (#14524)
  * NVDA się teraz przełączy do portu USB jeżeli HID Bluetooth urządzenie (takie jak HumanWare Brailliant lub APH Mantis) jest zostanie automatycznie wykryte a połączenie USB stanie się dostępne.
  To działało tylko do portów szeregowych. (#14524)
  * Gdy nie ma podlączonego monitora brajlowskiego a przegląd brajla jest zamknięty za pomocą klawiszy `alt+f4` oraz klikając przycisk zamknij, wielkość monitora brajlowskiego będzie zresetowana do zera. (#15214)
* Przeglądarki internetowe:
  * NVDA już nie powoduje rzadkie wysypywanie się oraz zawieszanie przeglądarki Mozilla Firefox. (#14647)
  * W przeglądarkach Mozilla Firefox i Google Chrome, wpisywane znaki nie są już odczytywane w niektórych polach edycyjnych nawet gdy czytanie pisanycch znaków jest wyłączone. (#8442)
  * Od teraz możliwe jest używanie trybu czytania w wbudowanych kontrolkach Chromium gdzie poprzednio nie było to możliwe. (#13493, #8553)
  * W przeglądarce Mozilla Firefox, przemieszczanie wskaźnika myszy do okoła tekstu spoza linkami od teraz dokładniej wymawia tekst. (#9235)
  * Docelowa lokalizacja linków graficznych od teraz jest wymawiana dokłądniej w więcej przypadkach w  przeglądarkach Chrome i Edge. (#14783)
  * Podczas próby odczytu adresu URL dla linku bez atrybutu a href NVDA nie staje się cicha.
  Zamiast tego, NVDA poda komunikat o braku adresu docelowego. (#14723)
  * W trybie czytania, NVDA już nie będzie ignorowała fokusu podczas próby przeniesienia się do poprzedniej lub następnej kontrolki na przykłąd przemieszczanie się od kontrolki i jej nadrzędnym elemencie listy lub komórki siatki. (#14611)
    * Miewaj jednak na uwadze, że ta poprawka działa gdy opcja "automatycznie ustaw fokus do elementów fokusowalnych " w ustawieniach trybu przeglądu jest wyłączona (co jest opcją domyślna).
* Poprawki błędów dla Windows 11:
  * NVDA potrafi znowu czytać treść paska stanu w programie Notepad. (#14573)
  * Przełączanie między kartami właściwości spowoduje odczyt nazwy nowej karty właściwości w programach Notepad i File Explorer. (#14587, #14388)
  * NVDA ponownie potrafi czytać elementy kandydatów podczas wprowadzania tekstu w językach takich jak chiński i japoński. (#14509)
  * Znowu jest możliwe otwarcie elementów licencja i wspóltworcy w menu NVDA/pomoc. (#14725)
* Poprawki błędów Microsoft Office:
  * Podczas szybkiego przemieszczania się pomiędzy komórkami w programie Microsoft Excel, istnieje mniejsze prawdopodobieństwo że NVDA przeczyta błędne współrzędne komórki. (#14983, #12200, #12108)
  * Podczas pozycjonowania na komórkę w programie Microsoft excel spoza skoroszytu, Brajl i podświetlacz fokusu już nie są bezpotrzebnie aktualizowane do obiektó, który poprzednio był we fokusie. (#15136)
  * NVDA Od teraz prawidłowo będzie wymawiała fokusowane pola haseł w programach Microsoft Excel i Outlook. (#14839)
* Dla symboli które nie posiadają aktualnego opisu w aktualnie użytym języku, będzie używany domyślny poziom symboli. (#14558, #14417)
* Od teraz jest możliwe używanie znaku bekslesz w polu zamiany  wpisu słownikowego, gdy typ nie jest ustawiony na wyrażenie regularne. (#14556)
* W kalkulatorze w systemach operacyjnych Windows 10 i 11, kopia przenośna już niczego nie zrobi oraz odtworzy dźwięk błędu podczas wpisywania wyrażenia matematycznego w w trybie kompaktowym. (#14679)
* NVDA Znowu potrafi odzyskiwać się w więcej sytuacjach takich jak zawieszające się programy, które spowodowały kompletne zawieszenie NVDA. (#14759) 
* Podczas wymuszania wsparcia UIA z niektórymi wierszami poleceń, naprawiono błąd powodujący zawieszenie się NVDA i przepełnienie pliku dziennika. (#14689)
* NVDA już nie odmówi zapisywania konfiguracji po resetowaniu konfiguracji. (#13187)
* Podczas uruchamiania tymczasowej wersji z instalatora, NVDA już nie oszuka użytkownika faktem, że można zzapisać konfigurację. (#14914)
* NVDA reaguje troszeczkę szybciej na polecenia i zmiany fokusu. (#14928)
* Pokazywanie ustawień Ocr od teraz jest możliwe  w systemach, gdzie to nie było możliwe. (#15017)
* Naprawiono bląd związany z zapisywaniem i przywracaniem konfiguracji NVDA, włączając to przełączanie między syntezatorami mowy. (#14760)
* Naprawiono błąd gestu przeglądu tekstu "pociągnięcie do góry" który powodował, że wykonywanie gestu powodowało poruszanie się po stronach, zamiast po liniach. (#15127)

### Changes for Developers

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Suggested conventions have been added to the add-on manifest specification.
These are optional for NVDA compatibility, but are encouraged or required for submitting to the Add-on Store. (#14754)
  * Use `lowerCamelCase` for the name field.
  * Use `<major>.<minor>.<patch>` format for the version field (required for add-on datastore).
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

Dodano nową opcję do kategorii "nawigacja po dokumencie", "styl akapitu".
Ta opcja może być używana w edytorach tekstu, niewspierających nawigację po akapitach natywnie, na przykład Notepad i Notepad plus plus.

Dodano polecenie globalne do odczytu docelowej lokalizacji linku, `NVDA+k`.

Ulepszone wsparcie dla adnotowanej treści webowej (takiej jak komentarze i przypisy końcowe).
Naciśnij `NVDA+d` aby przemieszczać się po streszczeniach gdy adnotacje są odczytywane (na przykład: "ma komentarz, ma przypis końcowy").

Monitory brajlowskie Tivomatic Caiku Albatross 46/80 są od teraz wspierane.

Ulepszono wsparcie dla architektur ARM64 i AMD64 wersji systemu operacyjnego Windows.

Naprawiono liczne błędy, zwłaszcza w systemie operacyjnym Windows 11.

eSpeak, LibLouis, Sonic rate boost i Unicode CLDR zostały zaktualizowane.
Dodano nowe tablice brajlowskie dla języków:  gruzińskiego, Swahili (Kenia) i Cziczewa (Malawi).

Uwaga:

* W tej wersji istniejące wersje dodatków są niezgodne.

### Nowe funkcje

* Microsoft Excel z UI Automation: Automatyczny odczyt nagłówków kolumn i wierszy w tabelach. (#14228)
  * Uwaga: dotyczy to tabel formatowanych za pomocą  przycisku "tabela" na karcie właściwości wstaw wstążki.
  Opcje "pierwsza kolumna" i "nagłówek wiersza" w "opcjach stylu tabeli" równoznaczne są z nagłówkami kolumn i wierszy.
  * Nie odnosi się to do nagłówków specyficznych dla czytnika ekranu, które używają nazwanych  rozpiętości.
* Dodano nieprzydzielone zdarzenie wejścia do włączania i wyłączania opisów znaków po ruchu kursora. (#14267)
* Dodano eksperymentalną opcję do używania wsparcia powiadomie UIA w programie Windows terminal w celu odczytu nowego oraz zmienionego tekstu w konsoli, skutkując lepszą stabilnością i wydajnością. (#13781)
  * O ograniczeniach tej opcji można przeczytać w podręczniku użytkownika.
* W systemie Windows 11 ARM64, tryb czytania od teraz jest dostępny w aplikacjach AMD64 takich jak Firefox, Google Chrome i 1Password. (#14397)
* Dodano nową opcję, "styl akapitu" w kategorii "nawigacja po dokumentach".
To dodaje wsparcie dla nawigacji po akapitach w stylach pojedyńczej nowej linii (normalnej) i wieloliniowej przerwy (blokowej).
Ta opcja może być używana z edytorami tekstu, które nie wspierają  natywną nawigację po akapitach, takimi jak Notepad i Notepad++. (#13797)
* Istnienie wielu adnotacji teraz jest odczytywane.
`nvda+d` od teraz przełącza pomiędzy odczytu streszczenia każdego celu adnotacji dla więcej źródeł celnych.
Na przykład, gdy tekst zawiera komentarz i przypis końcowy związany z nim. (#14507, #14480)
* Dodano wsparcie dla monitorów brajlowskich Tivomatic Caiku Albatross 46/80. (#13045)
* Nowe polecenie globalne: odczytaj docelową lokalizacje linku (`NVDA+k`).
Gdy skrót jest naciśnięty jeden raz lokalizacja linku w obiekcie nawigatora będzie pokazana na monitorze brajlowskim i wymówiona.
Gdy skrót jest naciśnięty dwukrotnie, docelowa lokalizacja będzie pokazana w oknie w celu dokładniejszego odczytu. (#14583)
* Dodano nowe nieprzydzielone polecenie (kategoria narzędzia): pokaż lokalizację linku w oknie.
To polecenie jest równoważne dwukrotnym naciśnięciem skrótu `NVDA+k` ale z tą różnicą, że może być bardziej użyteczne dla użytkowników monitorów brajlowskich. (#14583)

### Zmiany

* Zaktualizowano LibLouis tłumacz brajla do [wersji 3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Drastycznie zaktualizowano tablice brajlowskie dla węgierskiego, ujednoliconego angielskiego brajla, i chińskiego bopomofo.
  * Wsparcie dla nowego duńskiego standartu brajla wydanego w 2022 roku.
  * Nowe tablice brajlowskie dla gruzińskiego brajla literackiego, Swahili (Kenia) i Chichewa (Malawi).
* Zaktualizowano bibliotekę do przyśpieszania mowy Sonic  do wersji commit `1d70513`. (#14180)
* Baza znaków unicode CLDR została zaktualizowana do wersji 42.0. (#14273)
* eSpeak NG zostałzaktualizowany do wersji 1.52-dev commit `f520fecb`. (#14281, #14675)
  * Naprawiono odczyt wielkich liczb. (#14241)
* Aplikacje java z kontrolkami używającymi  stanu zaznaczenia od teraz będą zgłaszały stan elementu niezaznaczony zamiast stanu zaznaczonego. (#14336)

### Poprawki błędów

* Poprawki Windows 11:
  * NVDA od teraz odczyta podpowiedzi wyszukiwania podczas otwierania menu start. (#13841)
  * Na architekturze ARM, aplikacje x64 już nie są identyfikowane jako aplikacje ARM64. (#14403)
  * Elementy menu historii schowka , takie jak ""przypnij element" od teraz są osiągalne. (#14508)
  * W systemie Windows 11 22H2 i nowszych wersjach, od teraz znowu możliwa jest interakcja za pomocą myszy i klawiatury z elementami takie jak obszar powiadomień dodatkowych i okno dialogowe "otwórz za pomocą". (#14538, #14539)
* Od teraz dostępne są podpowiedzi podczas wpisywania @wzmianek w komentarzach Microsoft Excel. (#13764)
* Na pasku adresu Google Chrome, kontrolki podpowiedzi takie jak (przełącz do karty, usuń podpowiedź itd.) od teraz są odczytywane po zaznaczeniu. (#13522)
* Podczas dostarczania informacji o formatowaniu, kolory są ściśle odczytywane w programach Wordpad i podglądzie logu, co jest lepsze niż odczyt "kolor domyślny". (#13959)
* W przeglądarce Firefox, aktywowanie przycisku "Show options" na stronach problemów Github od teraz działa niezawodnie. (#14269)
* Kontrolki wyboru daty w oknie dialogowym zaawansowanego wyszukiwania programu Outlook 2016 / 365 od teraz są odczytywane z właściwymi oznakami i wartościami. (#12726)
* Kontrolki ARIA przełączników od teraz są rozpoznawane jako przełączniki w przeglądarkach Firefox, Chrome i Edge, co jest dokładniejsze w porównaniu z odczytem tych kontrolek jako pola wyboru. (#11310)
* NVDA od teraz automatycznie przeczyta stan sortowania w nagłówku kolumny tabeli HTML po zmianie naciskając przycisk wewnętrzny. (#10890)
* Nazwa regionu oraz punktu orientacyjnego jest automatycznie wymawiana podczas przeskakiwania wewnątrz regionu z zewnątrz używając klawiszy szybkiej nawigacji . (#13307)
* Gdy opcje Odtwarzaj dźwięk, oraz lub wymawiaj 'duże' przed dużymi literami są włączone w kombinacji z opisami po nazwie liter, NVDA więcej nie odtworzy sygnał dźwiękowy lub odczyta 'duże' dwukrotnie. (#14239)
* Od teraz kontrolki tabel w aplikacjach Java będą odczytywane precyzyjniej przez NVDA. (#14347)
* Od teraz niektóre ustawienia już nie będą inne podczas używania więcej profili. (#14170)
  * Następujące ustawienia zostały naprawione:
    * Wcięcie linii w ustawieniach formatowania.
    * Obramowania komórek w ustawieniach formatowania
    * Pokazywanie wiadomości w ustawieniach brajla
    * Przywiązanie brajla w ustawieniach brajla
  * W niektórych rzadkich przypadkach, te ustawienia, gdy używane są w profilach mogą być nieoczekiwanie zmodyfikowane gdy ta wersja NVDA zostanie zainstalowana.
  * Prosimy sprawdzić te ustawienia w profilach po zaktualizowaniu NVDA do tej wersji.
* Znaki emoji będą odczytywane w coraz więcej języków. (#14433)
* Istnienie adnotacji od teraz jest pokazywane także w brajlu dla niektórych elementów. (#13815)
* Naprawiono błąd który spowodował nie zapisywanie zmian w poprawny sposób, gdy zmieniamy opcje "domyślną" i wartość opcji "domyślnej". (#14133)
* Podczas konfiguracji NVDA zawsze będzie zdefiniowany jeden klawisz modyfikatora NVDA. (#14527)
* Podczas otwierania  menu NVDA używając obszaru powiadomień, NVDA już nie pokaże nieistniejącej oczekującej aktualizacji. (#14523)
* W Foobarze 2000, Pozostały, upłyneły i całkowity czas jest od teraz odczytywany prawidłowo w przypadku plików audio trwających ponad jeden dzień. (#14127)
* W przeglądarkach, takich jak Chrome i Firefox, alerty o pobieraniu pliku będą także wyświetlane na monitorze brajlowskim. Dotyczy to także innych alertów aria. (#14562)
* Naprawiono błąd niemożliwej nawigacji pomiędzy pierwszej i ostatniej  kolumny w tabelach w przeglądarce Firefox (#14554)
* Gdy NVDA jest uruchomiony z parametrem `--lang=Windows`, otwieranie ustawień ogólnych jest znowu możliwe. (#14407)
* NVDA już nie przestaje czytać w programie Kindle for PC po przewracaniu strony. (#14390)

### Changes for Developers

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

To wydanie w sobie zawiera kilka nowych skrótów klawiszowych, włączając w to skróty do czytania całych tabel.
Do podręcznika użytkownika został dodany roździał "szybki start".
Naprawiono także niektóre błędy.

Liblouis i Espeak-ng zostały zaktualizowane.
Dodano nowe tablice brajlowskie dla chińskiego, szwedzkiego, języka luganda i języka Kinyarwanda.

### Nowe funkcje

* Dodano rozdział "szybki start" do podręcznika użytkownika. (#13934)
* Dodano nowy skrót klawiszowy do sprawdzania skrótu klawiszowego bieżącego obiektu pod fokusem. (#13960)
  * Skrót dla komputerów stacjonarnych: `shift+numeryczny2`.
  * Skrót dla komputerów przenośnych: `NVDA+ctrl+shift+.`.
* Dodano nowe skróty do przemieszczania kursoru przeglądu po stronie gdzie jest to wspierane przez program. (#14021)
  * Przechodzi do poprzedniej strony:
    * Skrót dla komputerów stacjonarnych: `NVDA+pageUp`.
    * Skrót dla komputerów przenośnych: `NVDA+shift+pageUp`.
  * Przechodzi do następnej strony:
    * Skrót dla komputerów stacjonarnych: `NVDA+pageDown`.
    * Skrót dla komputerów przenośnych: `NVDA+shift+pageDown`.
* Dodano następujące skróty klawiszowe do tabel. (#14070)
  * Czytaj wszystko w kolumnie: `NVDA+control+alt+strzałka w dół`
  * Czytaj wszystko w wierszu: `NVDA+control+alt+strzałka w prawo`
  * Czytaj całą kolumnę: `NVDA+control+alt+strzałka w górę`
  * Czytaj cały wiersz: `NVDA+control+alt+Strzałka w lewo`
* W Microsoft Excel który jest używany za pomocą interfejsu Ui Automation, NVDA od teraz ogłasza przemieszczenie spoza tabelą arkusza kalkulacyjnego. (#14165)
* Czytanie nagłówków tabeli od teraz może być oddzielnie konfigurowane dla kolumn i wierszy. (#14075)

### Zmiany

* eSpeak NG został zaktualizowany do wersji 1.52-dev commit `735ecdb8`. (#14060, #14079, #14118, #14203)
  * Naprawiono czytanie znaków alfabetu łacińskiego podczas używania języka mandaryńskiego. (#12952, #13572, #14197)
* Zaktualizowany LibLouis tłumacz znaków brajlowskich do wersji [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Dodano następujące tablice brajlowskie:
    * Chiński ogólny alfabet Braille'a (uproszczone chińskie znaki)
    * Kinyarwanda brajl literacki
    * Luganda brajl literacki
    * Szwedzkie pismo podstawowe
    * Szwedzkie pismo pełne
    * Szwedzkie skróty
    * Chiński (Chiny, mandaryński) aktualny standard brajlowski (bez tonów) (#14138)
* NVDA od teraz włącza do statystyki użytkowania architekturę systemu operacyjnego. (#14019)

### Poprawki błędów

* Podczas aktualizowania NVDA przy użyciu menedżeru pakietów systemu Windows z poziomu wiersza poleceń, czyli winget, stabilna wersja NVDA więcej nie jest zawsze traktowana jako nowsza niż jakakolwiek wersja Alpha zainstalowana w systemie. (#12469)
* NVDA od teraz poprawnie odczytuje grupowania w aplikacjach Java. (#13962)
* Kursor od teraz sprawnie śledzi wymawiany tekst podczas ciągłego czytania w aplikacjach takich jak Bookworm, WordPad, lub NVDA podglądu loga. (#13420, #9179)
* W programach używających UI Automation, połowicznei zaznaczone pola wyboru od teraz będą zgłaszane poprawnie. (#13975)
* Ulepszona wydajność i stabilność w programach: Microsoft Visual Studio, Windows Terminal, a także innych programach używających interfejsu UI automation. (#11077, #11209)
  * Te poprawki błędów stosowane są do wersji Windows 11 Sun Valley 2 (versja 22H2) i nowszych.
  * Rejestracja selektywna dla zmian właściwości i zdarzeń UIA od teraz jest domyślnie włączona.
* Odczytywanie tekstu, wyjście brajla, a także nieodczytywanie haseł od teraz działają poprawnie w zagnieżdżonej kontrolce Windows terminal w programie Visual Studio 2022. (#14194)
* NVDA od teraz jest DPI świadomy podczas używania więcej niż jednego monitora.
Wdrożono kilka poprawek dla używania ustawienia DPI wyższego niż 100% oraz używania więcej monitorów.
Mogą jeszcze pojawiać się problemy w wersjach systemu operacyjnego Windows starszych niż Windows 10 1809.
Aby te poprawki działały, aplikacje z którymi NVDA współpracuje także powinne być DPI świadome.
Trzeba mieć na uwadzę, że nadal istnieją problemy z przeglądarkami Chrome i Edge. (#13254)
  * Ramki podświetlenia wizualnego od teraz powinny się poprawnie umieszczać w większości aplikacji. (#13370, #3875, #12070)
  * Współpraca z ekranami dotykowymi od teraz powina być dokładniejsza dla większości programów. (#7083)
  * Śledzenie myszy od teraz powinno być dokładniejsze dla większości programów. (#6722)
* Zmiany stanu orientacji (pionowa/pozioma) od teraz są poprawnie ignorowane gdy nie ma żadnych zmian (na przykład, zmiany monitora). (#14035)
* NVDA od teraz będzie oznajmiał przeciąganie elementów na ekranie w miejscach, takich jak przemieszczanie kafelek w Menu start w systemie operacyjnym Windows 10 i pulpitów wirtualnych w systemie Windows 11. (#12271, #14081)
* W ustawieniach zaawansowanych, opcja "Odtwarzaj dźwięk do zapisanych błędów" jest teraz prawidłowo resetowana do domyślnej wartości po naciśnięciu przycisku "Przywróć do ustawień domyślnych". (#14149)
* NVDA od teraz może zaznaczać tekst używając skrótu `NVDA+f10` w aplikacjach Java. (#14163)
* NVDA od teraz nie będzie się zawieszac w menu podczas poruszania się strzałkami w górę i w dół w konwersachach wątkowanych w programie  Microsoft Teams. (#14355)

### Changes for Developers

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* The [NVDA API Announcement mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) was created. (#13999)
* NVDA no longer processes `textChange` events for most UI Automation applications due to their extreme negative performance impact. (#11002, #14067)

#### Deprecations

* `core.post_windowMessageReceipt` is deprecated, use `winAPI.messageWindow.pre_handleWindowMessage` instead.
* `winKernel.SYSTEM_POWER_STATUS` is deprecated and usage is discouraged, this has been moved to `winAPI._powerTracking.SystemPowerStatus`.
* `winUser.SM_*` constants are deprecated, use `winAPI.winUser.constants.SystemMetrics` instead.

## 2022.3.3

Jest to pomniejsze wydanie naprawiające problemy wersji 2022.3.2, 2022.3.1 i 2022.3.
To wydanie także naprawia błędy bezpieczeństwa.

### Poprawki bezpieczeństwa

* Zapobiega niechcianemu dostępowi dla nieautoryzowanych użytkowników do np. konsoli python.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Poprawki błędów

* Naprawiono błąd podczas zamrażania NVDA na ekranie blokady, przy którym NVDA umożliwi dostęp do pulpitu użytkownika z poziomu ekranu blokady. (#14416)
* Naprawiono błąd podczas którego NVDA się NVDA zawiesza podczas logowania i NVDA się zachowa niepoprawnie, tak jak by użądzenie było jeszcze zablokowane. (#14416)
* Naprawiono błędy dostępności z Windows doświadczeniami "zapomniałem numer Pin" i instalacji Windows Update. (#14368)
* Naprawiono błąd podczas próby instalacji NVDA w niektórych środowiskach Windows, Np. Windows Server. (#14379)

### Changes for Developers

#### Deprecations

* `utils.security.isObjectAboveLockScreen(obj)` is deprecated, instead use `obj.isBelowLockScreen`. (#14416)
* The following functions in `winAPI.sessionTracking` are deprecated for removal in 2023.1. (#14416)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`

## 2022.3.2

Jest to pomniejsze wydanie naprawiające regresje z wersji 2022.3.1 i naprawiające incydenty bezpieczeństwa.

### Poprawki bezpieczeństwa

* Zapobiega możliwemu dostępowi na poziomie systemowym dla użytkowników nieuwierzytelnionych.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Poprawki błędów

* Naprawiono regresję z wersji NVDA 2022.3.1 w której większość wyłączono na bezpiecznych ekranach. (#14286)
* Naprawiono regresję z wersji NVDA 2022.3.1 w której większość funkcjonalności było wyłączone po zalogowaniu, jeżeli NVDA została uruchomiona na ekranie blokady. (#14301)

## 2022.3.1

Jest to pomniejsze wydanie naprawiające kilka incydentów bezpieczeństwa.
Prosimy o odpowiednie zgłoszenie incydentów bezpieczeństwa na adres <info@nvaccess.org>.

### Poprawki bezpieczeństwa

* Naprawiono eksploit za pomocą którego można było podnieść uprawnienia z użytkownika do systemu.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Naprawiono incydent bezpieczeństwa umożliwiający dostępu do konsoli Pythona na ekranie logowania poprzez hazard uruchomienia NVDA.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Naprawiono problem w którym tekst przeglądu mowy był przechowywany w pamięci poczas blokowania systemu operacyjnego.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Poprawki błędów

* Od teraz zapobiegane jest zmienianie ustawień  przeglądu brajla i mowy na ekranie blokady przez nieuprawnionego użytkownika. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Znaczna część tej wersji została opracowana przez społeczność programistów NVDA.
Zawiera ona opisy liter po ich nazwach  oraz poprawione wsparcie dla konsoli systemu operacyjnego Windows.

Dodano również kilka poprawek błędów.
Najistotniejsza poprawka błędów dla najnowszych wersji programów Adobe Acrobat/Reader zapobiega niespodziewanemu zamykaniu się programu z raportem o błędzie podczas wyświetlania dokumentu PDF.

Do najnowszej wersji syntezatora mowy eSpeak dodano 3 nowe języki: białoruski, luksemburski i Totontepec Mixe.

### Nowe funkcje

* W Hoście konsoli używanym przez wiersz poleceń, PowerShell oraz podsystem Linux dla systemu Windows 11 w wersji 22H2 (Sun Valley 2) i nowszych:
  * znacząco poprawiono wydajność i stabilność. (#10964)
  * Po naciśnięciu `control+f`, aby znaleźć tekst, pozycja kursora recenzji jest aktualizowana zgodnie ze znalezionym terminem. (#11172)
  * Raportowanie wpisanego tekstu, który nie pojawia się na ekranie (np. hasła), jest domyślnie wyłączone.
Można go ponownie włączyć w panelu ustawień zaawansowanych NVDA. (#11554)
  * Tekst, który został przewinięty poza ekranem, można przeglądać bez przewijania okna konsoli.. (#12669)
  * Dostępne są bardziej szczegółowe informacje o formatowaniu tekstu ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Dodano nową opcję Mowy, aby czytać opisy znaków po literowaniu. (#13509)
* Dodano nową opcję alfabetu Braille'a, aby określić, czy przewijanie wyświetlacza do przodu/do tyłu powinno przerywać mowę. (#2124)

### Zmiany

* eSpeak NG został zaktualizowany do wersji 1.52-dev commit `9de65fcb`. (#13295)
  * Dodane języki:
    * Białoruski
    * Luksemburgski
    * Totontepec Mixe
* Używając Uia w celu uzyskania dostępu do kontrolek arkusza kalkulacyjnego programu Microsoft Excel, NVDA może teraz raportować, kiedy komórka jest scalona. (#12843)
* Zamiast zgłaszania "ma szczegóły" cel szczegółów jest zawarty tam, gdzie to możliwe, na przykład "ma komentarz". (#13649)
* Rozmiar instalacji NVDA jest teraz wyświetlany w sekcji Programy i funkcje systemu Windows. (#13909)-

### Poprawki błędów

* Adobe Acrobat / Reader 64 bit nie będzie już ulegać awarii podczas czytania dokumentu PDF. (#12920)
  * Należy pamiętać, że najbardziej aktualna wersja programu Adobe Acrobat / Reader jest również wymagana, aby uniknąć awarii.
* Pomiary rozmiaru czcionki są od teraz przetłumaczone w NVDA. (#13573)
* Ignorowane są zdarzenia Java Access Bridge, w których nie można znaleźć uchwytu okna dla aplikacji Java.
Poprawi to wydajność niektórych aplikacji Java, w tym IntelliJ IDEA. (#13039)
* Ogłaszanie wybranych komórek dla programu LibreOffice Calc jest bardziej wydajne i nie powoduje już zamrożenia programu Calc po zaznaczeniu wielu komórek. (#13232)
* Podczas uruchamiania pod innym użytkownikiem Microsoft Edge nie jest już niedostępny. (#13032)
* Gdy zwiększenie szybkości jest wyłączone, prędkość eSpeak nie spada już między wartościami prędkości 99% a 100%. (#13876)
* Naprawiono błąd, który pozwalał na otwarcie 2 dialogów gestów wejściowych. (#13854)

### Changes for Developers

* Updated Comtypes to version 1.1.11. (#12953)
* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * This can be overridden by changing the "Windows Console support" setting in NVDA's advanced settings panel.
  * To find your Windows Console's NVDA API level, set "Windows Console support" to "UIA when available", then check the NVDA+F1 log opened from a running Windows Console instance.
* The Chromium virtual buffer is now loaded even when the document object has the MSAA `STATE_SYSTEM_BUSY` exposed via IA2. (#13306)
* A config spec type `featureFlag` has been created for use with experimental features in NVDA. See `devDocs/featureFlag.md` for more information. (#13859)

#### Deprecations

There are no deprecations proposed in 2022.3.

## 2022.2.4

Jest to wydanie łatka, naprawiające problem bezpieczeństwa.

### Poprawki błędów

* Naprawiono eksploit za pomocą którego było możliwe wejście do konzoli pythona z poziomu podglądu logów na zablokowanym ekranie.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Jest to wersja naprawiająca niechcianą niezgodność w API wprowadzoną w wersji 2022.2.1.

### Poprawki błędów

* Naprawiono błąd w którym NVDA nie zgłaszał "bezpieczny pulpit" podczas wejścia do bezpiedcznego pulpitu.
To skutkowało, że NVDA remote nie rozpoznawał bezpiecznych pulpitów. (#14094)

## 2022.2.2

Jest to wersja naprawiająca błąd w wersji 2022.2.1 dotyczący zdarzeń wejścia.

### Poprawki błędów

* Naprawiono błąd, w którym zdarzenia wejścia nie działały zawsze. (#14065)

## 2022.2.1

Jest to pomniejsza wersja naprawiająca problemy bezpieczeństwa.
Prosimy odpowiedzialnie zgłaszać problemy z bezpieczeństwem na adresie <info@nvaccess.org>.

### Poprawki bezpieczeństwa

* Naprawiono eksploit za pomocą którego było możliwe uruchomienie konzoli pythona z zablokowanego ekranu. (GHSA-rmq3-vvhq-gp32)
* Naprawiono eksploit za pomocą którego było możliwe wyjście z ekranu blokowania używając nawigacji obiektowej. (GHSA-rmq3-vvhq-gp32)

### Changes for Developers

#### Deprecations

These deprecations are currently not scheduled for removal.
The deprecated aliases will remain until further notice.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModules.lockapp.LockAppObject` should be replaced with `NVDAObjects.lockscreen.LockScreenObject`. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS` should be replaced with `utils.security.getSafeScripts()`. (GHSA-rmq3-vvhq-gp32)

## 2022.2

To wydanie zawiera wiele poprawek błędów.
Warto zauważyć, że wprowadzono znaczące ulepszenia dla aplikacji opartych na Javie, monitorów brajlowskich i funkcji systemu Windows.

Wprowadzono nowe polecenia nawigacji po tabeli.
Unicode CLDR został zaktualizowany.
LibLouis został zaktualizowany. Zawiera on nową niemiecką tablicę brajlowską.

### Nowe funkcje

* Obsługa interakcji ze składnikami Microsoft Loop w produktach Microsoft Office. (#13617)
* Dodano nowe polecenia nawigacji po tabeli. (#957)
 * `control+alt+home/end`, aby przejść do pierwszej/ostatniej kolumny.
 * `control+alt+pageUp/pageDown`, aby przejść do pierwszego/ostatniego wiersza.
* Dodano nieprzypisany skrypt do przełączania między trybami przełączania języka i dialektu. (#10253)-

### Zmiany

* NSIS został zaktualizowany do wersji 3.08. (#9134)
* CLDR został zaktualizowany do wersji 41.0. (#13582)
* Zaktualizowano translator alfabetu Braille'a LibLouis do [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nowa tablica brajlowska: niemiecki skróty (dwukierunkowe)
* Dodano nową rolę dla kontrolek "wskaźnika zajętości". (#10644)
* NVDA ogłasza teraz, kiedy nie można wykonać akcji NVDA. (#13500)
  * Obejmuje to, przypadki gdy:
    * używamy wersję NVDA ze Sklepu Windows.
    * używamy NVDA w bezpiecznym kontekście.
    * oczekujemy na odpowiedź w modalnym oknie dialogowym.

### Poprawki błędów

* Poprawki dla aplikacji opartych na Javie:
  * NVDA ogłosi teraz stan tylko do odczytu. (#13692)
  * NVDA będzie teraz poprawnie ogłaszać stan wyłączony/włączony. (#10993)
  * NVDA od teraz będzie  czytać skróty funkcyjne. (#13643)
  * NVDA może teraz emitować sygnał dźwiękowy lub mówić na paskach postępu. (#13594)
  * NVDA nie będzie już niepoprawnie usuwać tekstu z widżetów podczas prezentacji dla użytkownika. (#13102)
  * NVDA będzie czytać stan przełączników. (#9728)
  * NVDA zidentyfikuje teraz okno w aplikacji Java z wieloma oknami. (#9184)
  * NVDA będzie teraz czytać informacje o pozycji dla kontrolek kart właściwosci. (#13744)
* Poprawki Braille'a:
  * Naprawiono wyjście brajla podczas nawigacji po pewnym tekście w kontrolkach edycji w aplikacjach mozilla, takich jak sporządzanie wiadomości w Thunderbirdzie. (#12542)
  * Gdy alfabet Braillea jest automatycznie powiązany, a mysz jest poruszana z włączonym śledzeniem myszy,
   Polecenia przeglądania tekstu aktualizują teraz monitor brajlowski zawartoscią mówioną. (#11519)
  * Możliwe jest teraz przesuwanie wyświetlacza brajlowskiego po treści za pomocą poleceń przeglądania tekstu. (#8682)
* Instalator NVDA może teraz uruchamiać się z katalogów ze znakami specjalnymi. (#13270)
* W Firefoksie NVDA nie zgłasza już elementów na stronach internetowych, gdy atrybuty aria-rowindex, aria-colindex, aria-rowcount lub aria-colcount są nieprawidłowe. (#13405)
* Kursor nie przełącza już wiersza ani kolumny podczas korzystania z nawigacji po tabeli do nawigacji po scalonych komórkach. (#7278)
* Podczas czytania nieinteraktywnych plików PDF w programie Adobe Reader typ i stan pól formularza (takich jak pola wyboru i przyciski opcji) są teraz raportowane. (#13285)
* "Resetuj konfigurację do ustawień fabrycznych" jest teraz dostępny w menu NVDA w trybie bezpiecznym. (#13547)
* Wszelkie zablokowane przyciski myszy zostaną odblokowane po wyjściu z NVDA, wcześniej przyciski myszy pozostawały zablokowany. (#13410)
* Program Visual Studio zgłasza teraz numery wierszy. (#13604)
  * Zauważ, że aby raportowanie numerów wierszy działało, pokazywanie numerów wierszy musi być włączone w Visual Studio i NVDA.
* Program Visual Studio teraz poprawnie zgłasza wcięcia linii. (#13574)
* NVDA po raz kolejny ogłosi szczegóły wyników wyszukiwania w menu Start w ostatnich wydaniach Windows 10 i 11. (#13544)
* W Windows 10 i 11 Calculator w wersji 10.1908 i nowszych,
NVDA ogłosi wyniki po naciśnięciu większej liczby poleceń, takich jak polecenia z trybu naukowego. (#13383)
* W systemie Windows 11 ponownie można nawigować i wchodzić w interakcje z elementami interfejsu użytkownika,
takich jak Pasek zadań i Widok zadań za pomocą myszy i interakcji dotykowej. (#13506)
* NVDA ogłosi zawartość paska stanu w Notatniku Windows 11. (#13688)
* Podświetlanie obiektów Navigator pojawia się natychmiast po aktywacji funkcji. (#13641)
* Naprawiono czytanie elementów widoku listy jednokolumnowej. (#13659, #13735)
* Naprawiono automatyczne przełączanie języka eSpeak na angielski i francuski z powrotem na brytyjski angielski i francuski (Francja). (#13727)
* Naprawiono automatyczne przełączanie języka OneCore podczas próby przejścia na wcześniej zainstalowany język. (#13732)

### Changes for Developers

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

To wydanie zawiera główne ulepszenia obsługi UIA w MS Office.
W przypadku pakietu Microsoft Office 16.0.15000 lub nowszego w systemie Windows 11 NVDA domyślnie używa automatyzacji interfejsu użytkownika do uzyskiwania dostępu do dokumentów programu Microsoft Word.
Zapewnia to znaczną poprawę wydajności w porównaniu ze starym dostępem do modelu obiektów.

Wprowadzono ulepszenia sterowników monitorów brajlowskich, w tym Seika Notetaker, Papenmeier i HID Braille. 
Istnieją również różne poprawki błędów systemu Windows 11 dla aplikacji takich jak Kalkulator, Konsola, Terminal, Poczta i Panel Emoji.

eSpeak-NG i LibLouis zostały zaktualizowane, dodając nowe tabele japońskie, niemieckie i katalońskie.

Uwaga:

 * To wydanie przerywa kompatybilność z istniejącymi dodatkami. -

### Nowości

* Obsługa notatek raportowania w MS Excel z włączoną UIA w systemie Windows 11. (#12861)
* W ostatnich kompilacjach programu Microsoft Word za pośrednictwem UIA w systemie Windows 11 istnienie zakładek, komentarzy roboczych i rozwiązanych komentarzy jest teraz zgłaszane zarówno w mowie, jak i alfabecie Braille'a. (#12861)
* Nowy parametr wiersza poleceń `--lang` umożliwia zastąpienie skonfigurowanego języka NVDA. (#10044)
* NVDA ostrzega teraz o parametrach wiersza poleceń, które są nieznane i nie są używane przez żadne dodatki. (#12795)
* W programie Microsoft Word dostępnym za pośrednictwem automatyzacji interfejsu użytkownika, NVDA będzie teraz korzystać z mathPlayer do czytania i poruszania się po równaniach matematycznych pakietu Office. (#12946)
  * Aby to zadziałało, musisz mieć uruchomiony program Microsoft Word 365/2016 kompilacja 14326 lub nowszy. 
  * Równania MathType muszą być również ręcznie konwertowane na Office Math, wybierając każde z nich, otwierając menu kontekstowe, wybierając Opcje równań, Konwertuj na Office Math.
* Raportowanie "ma szczegóły" i powiązane polecenie podsumowujące relację szczegółów zostały zaktualizowane do pracy w trybie fokusu. (#13106)
* Seika Notetaker może być teraz automatycznie wykrywany po podłączeniu przez USB i Bluetooth. (#13191, #13142)
  * Dotyczy to następujących urządzeń: MiniSeika (16, 24 komórek), V6 i V6Pro (40 komórek)
  * Ręczne wybieranie portu COM Bluetooth jest teraz również obsługiwane.
* Dodano polecenie przełączania przeglądu brajla; nie ma domyślnie skojarzonego gestu. (#13258)
* Dodano polecenia do przełączania wielu modyfikatorów jednocześnie z wyświetlaczem Braille'a (#13152)
* Okno dialogowe Słownik mowy zawiera teraz przycisk "Usuń wszystko", aby pomóc wyczyścić cały słownik. (#11802)
* Dodano obsługę Kalkulatora Windows 11. (#13212)
* W programie Microsoft Word z włączonym UIA w systemie Windows 11 NVDA teraz czyta numery wierszy i numery sekcji. (#13283, #13515)
* W przypadku pakietu Microsoft Office 16.0.15000 i nowszych wersji w systemie Windows 11 NVDA domyślnie UIA użytkownika do uzyskiwania dostępu do dokumentów Microsoft Word, zapewniając znaczną poprawę wydajności w porównaniu ze starym dostępem do modelu obiektowego. (#13437)
 * Obejmuje to dokumenty w samym programie Microsoft Word, a także czytnik i kompozytor wiadomości w programie Microsoft Outlook. 

### Zmiany

* Espeak-ng został zaktualizowany do 1.51-dev commit `7e5457f91e10`. (#12950)
* Zaktualizowano liblouis Braille translator do [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Dodano nową tablicę brajlowską: japoński (Kantenji) brajl literacki.
  * Dodano nową niemiecką sześciopunktową komputerową tablicę brajlowską.
  * Dodano katalońską tablicę brajlowską pismo pełne. (#13408)
* - NVDA zgłosi wybór i scalone komórki w LibreOffice Calc 7.3 i nowszych. (#9310, #6897)
* Zaktualizowano repozytorium danych regionalnych Unicode Common Locale Data Repository (CLDR) do wersji 40.0. (#12999)
* `NVDA+Numpad Delete` domyślnie zgłasza lokalizację karetki lub obiektu skupionego. (#13060)
* `NVDA+Shift+Numpad Delete` zgłasza lokalizację kursora recenzji. (#13060)
* Dodano domyślne powiązania do przełączania klawiszy modyfikatorów do wyświetlaczy Freedom Scientific (#13152)
* "Baseline" nie jest już zgłaszany za pomocą polecenia formatowania tekstu raportu (`NVDA+f`). (#11815)
* Aktywuj długi opis nie ma już przypisanego domyślnego gestu. (#13380)
* Podsumowanie szczegółów raportu ma teraz domyślny gest (`NVDA+d`). (#13380)
* NVDA musi zostać ponownie uruchomiony po zainstalowaniu MathPlayer. (#13486)-

### Poprawki błędów

* Okienko menedżera schowka nie powinno już niepoprawnie brać fokusu podczas otwierania niektórych programów pakietu Office. (#12736)
* W systemie, w którym użytkownik zdecydował się zamienić główny przycisk myszy z lewej na prawą, NVDA nie będzie już przypadkowo wyświetlać menu kontekstowego zamiast aktywować element w aplikacjach takich jak przeglądarki internetowe. (#12642)
* Podczas przesuwania kursora recenzji poza koniec kontrolek tekstowych, takich jak Microsoft Word z UIA, "dół" jest poprawnie zgłaszany w większej liczbie sytuacji. (#12808)
* NVDA może zgłaszać nazwę i wersję aplikacji dla plików binarnych umieszczonych w system32 podczas pracy w 64-bitowej wersji systemu Windows. (#12943)
* Poprawiono spójność odczytu wyjściowego w wiersza poleceń. (#12974)
  * Zauważ, że w niektórych sytuacjach, podczas wstawiania lub usuwania znaków w środku linii, znaki po kursorze mogą być ponownie odczytywane.
* MS word z UIA: nagłówek quick nav w trybie przeglądania nie utknie już na końcowym nagłówku dokumentu, ani ten nagłówek nie jest wyświetlany dwukrotnie na liście elementów NVDA. (#9540)
* W systemie Windows 8 i nowszych pasek stanu Eksploratora plików można teraz przeczytać za pomocą standardowego gestu NVDA + end (pulpit) / NVDA + shift + end (laptop). (#12845)
* Wiadomości przychodzące na czacie programu Skype dla firm są ponownie czytane. (#9295)
* NVDA może ponownie przyciszać dźwięk podczas korzystania z syntezatora SAPI5 w systemie Windows 11. (#12913)
* W kalkulatorze Windows 10 NVDA ogłosi etykiety dla elementów historii i listy pamięci. (#11858)
* Gesty, takie jak przewijanie i routing, ponownie działają z urządzeniami Braille'a HID. (#13228)
* Poczta systemu Windows 11: Po przełączeniu ostrości między aplikacjami, podczas czytania długiej wiadomości e-mail, NVDA nie utknie już w linii wiadomości e-mail. (#13050)
* HID Braille: gesty akordowe (np. `spacja+kropka4`) mogą być z powodzeniem wykonywane z wyświetlacza Braille'a. (#13326)
* Rozwiązano problem polegający na tym, że w tym samym czasie mogło być otwieranych wiele okien dialogowych ustawień. (#12818)
* Rozwiązano problem polegający na tym, że niektóre monitory Braille'a Focus Blue przestawały działać po wybudzeniu komputera ze stanu uśpienia. (#9830)
* "Baseline" nie jest już fałszywie zgłaszany, gdy aktywna jest opcja "zgłoś indeks górny i dolny". (#11078)
* W systemie Windows 11 NVDA nie będzie już uniemożliwiać nawigacji w panelu emoji podczas wybierania emotikonów. (#13104)
* Zapobiega występowaniu błędu powodującego podwójne raportowanie podczas korzystania z konsoli i terminala systemu Windows. (#13261)
* Naprawiono kilka przypadków, w których nie można było czytać elementów listy w aplikacjach 64-bitowych, takich jak REAPER. (#8175)
* W menedżerze pobierania Microsoft Edge NVDA automatycznie przełączy się w tryb koncentracji uwagi, gdy element listy z najnowszym pobraniem zyska fokus. (#13221)
* NVDA nie powoduje już awarii 64-bitowych wersji Notepad ++ 8.3 i nowszych. (#13311)
* Program Adobe Reader nie ulega już awarii podczas uruchamiania, jeśli włączony jest tryb chroniony programu Adobe Reader. (#11568)
* Naprawiono błąd, który powodował, że wybranie sterownika Papenmeier Braille Display Driver powodowało awarię NVDA. (#13348)
* W programie Microsoft Word z UIA: numer strony i inne formatowanie nie jest już niewłaściwie ogłaszane podczas przechodzenia z pustej komórki tabeli do komórki z zawartością lub z końca dokumentu do istniejącej zawartości. (#13458, #13459)
* NVDA nie będzie już nie zgłaszać tytułu strony i zacznie automatycznie czytać, gdy strona załaduje się w Google Chrome 100. (#13571)
* NVDA nie ulega już awarii podczas resetowania konfiguracji NVDA do ustawień fabrycznych, gdy poleceń Speak są włączone. (#13634)-

### Changes for Developers

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

Jest to niewielka wersja mająca na celu rozwiązanie problemu z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki bezpieczeństwa

* Rozwiązano problem z poradnikiem bezpieczeństwa `GHSA-xc5m-v23f-pgr7`.
  * Okno dialogowe wymowy symbolu jest teraz wyłączone w trybie bezpiecznym.

## 2021.3.4

Jest to niewielka wersja mająca na celu naprawienie kilku zgłoszonych problemów z bezpieczeństwem.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki bezpieczeństwa

* Rozwiązano problem z poradnikiem bezpieczeństwa `GHSA-354r-wr4v-cx28`. (#13488)
  * Usuń możliwość uruchamiania NVDA z włączonym rejestrowaniem debugowania, gdy NVDA działa w trybie bezpiecznym.
  * Usuń możliwość aktualizacji NVDA, gdy NVDA działa w trybie bezpiecznym.
* Rozwiązano problem z poradnikiem bezpieczeństwa `GHSA-wg65-7r23-h6p9`. (#13489)
  * Usuń możliwość otwierania okna dialogowego gestów wejściowych w trybie bezpiecznym.
  * Usuń możliwość otwierania domyślnych, tymczasowych i głosowych okien dialogowych słownika w trybie bezpiecznym.
* Rozwiązano problem z poradnikiem bezpieczeństwa `GHSA-mvc8-5rv9-w3hx`. (#13487)
  * wx narzędzie do inspekcij okien jest od teraz wyłączone w trybie bezpiecznym.

## 2021.3.3

Ta wersja jest identyczna z 2021.3.2.
Błąd istniał w NVDA 2021.3.2, gdzie błędnie identyfikował się jako 2021.3.1.
To wydanie poprawnie identyfikuje się jako 2021.3.3.

## 2021.3.2

Jest to niewielka wersja mająca na celu naprawienie kilku zgłoszonych problemów z bezpieczeństwem.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki błędów

* Poprawka zabezpieczeń: Zapobiegaj nawigacji po obiektach poza ekranem blokady w systemach Windows 10 i Windows 11. (#13328)
* Poprawka zabezpieczeń: Okno dialogowe menedżera dodatków jest teraz wyłączone na bezpiecznych ekranach. (#13059)
* Poprawka zabezpieczeń: Pomoc kontekstowa NVDA nie jest już dostępna na bezpiecznych ekranach. (#13353)

## 2021.3.1

Jest to niewielka wersja mająca na celu naprawienie kilku problemów w 2021.3.

### Zmiany

* Nowy protokół brajlowski HID nie jest już preferowany, gdy można użyć innego sterownika monitora brajlowskiego. (#13153)
* Nowy protokół Braille'a HID można wyłączyć poprzez ustawienie w panelu ustawień zaawansowanych. (#13180)

### Bug Fixes

* Landmark is once again abbreviated in braille. #13158
* Fixed unstable braille display auto detection for Humanware Brailliant and APH Mantis Q40 braille displays when using Bluetooth. (#13153)

## 2021.3

To wydanie wprowadza wsparcie dla nowej specyfikacji brajlowskiej HID.
Celem tej specyfikacji jest zapewnienie uniwersalnego standardu wsparcia wszystkich monitorów brajlowskich bez konieczności instalowania dodatkowych sterowników.
Zaktualizowano też eSpeak-NG i LibLouis. Dodane zostały m.in. nowa tablica dla rosyjskiego i języka Tshivenda.
Do ustawień zaawansowanych dodano opcję, która pozwala włączyć Dźwięki błędu również w wersjach stabilnych NVDA.
Opcja "Czytaj wszystko" w programie Microsoft Word od teraz przewija widok tak, aby aktualna pozycja kursora zawsze była widoczna.
Dodano liczne ulepszenia dotyczące interakcji z pakietem Microsoft Office  przy użyciu UIA.
Na przykład, dzięki jednej z poprawek UIA, Outlook ignoruje więcej typów tabel układu treści w wiadomościach.

Ważne uwagi:

Po aktualizacji naszego certyfikatu bezpieczeństwa, u niektórych użytkowników pojawia się błąd gdy NVDA 2021.2 sprawdza swoje aktualizacje.
Od teraz NVDA automatycznie uzyskuje od systemu Windows aktualizacje certyfikatów bezpieczeństwa, co zapobiegnie pojawianiu się tego błędu w przyszłości.
Użytkownicy, u których występuje ten problem, powinni pobrać ręcznie aktualizacje certyfikatów.

### Nowe funkcje

* Dodano zdarzenie wejścia dla przełączania ustawień ogłaszania stylu obramowań komórki. (#10408)
* Wsparcie dla nowej specyfikacji brajlowskiej HID, którego celem jest zapewnienie uniwersalnego standardu wsparcia monitorów brajlowskich. (#12523)
  * Monitory brajlowskie, które wspierają tę specyfikację, będą automatycznie wykrywane przez NVDA.
  * Szczegóły techniczne dotyczące wprowadzenia specyfikacji HID do NVDA, są dostępne tutaj. https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Dodano wsparcie dla monitora brajlowskiego VisioBraille Vario 4. (#12607)
* Powiadomienia o błędach można włączyć w każdej wersji NVDA z poziomu ustawień zaawansowanych. (#12672)
* W systemie Windows 10 i nowszych, NVDA będzie ogłaszać ilość podpowiedzi wyszukiwania podczas wpisywania szukanych fraz w aplikacjach, takich jak Ustawienia lub Microsoft Store. (#7330, #12758, #12790)
* Od teraz wspierane jest nawigowanie po tabelach dla kontrolek tabeli utworzonych za pomocą Out-GridView cmdlet w PowerShell. (#12928)

### Zmiany

* Espeak-ng został zaktualizowany do wersji 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* Gdy w systemie nie ma zainstalowanego wsparcia dla Głosów Mobilnych Windows w preferowanym języku, NVDA automatycznie wybierze eSpeak. (#10451)
* Jeżeli Głosy Mobilne Windows w dalszym ciągu nie działają, należy z powrotem przełączyć syntezator na Espeak. (#11544)
* Podczas odczytywania paska stanu poleceniem `NVDA+end`, punkt przeglądu nie jest już przenoszony do miejsca, gdzie znajduje się ten pasek.
Aby nadal móc przenosić punkt przeglądu do pasków stanu, należy przypisać polecenie do odpowiedniego skryptu w Zdarzeniach Wejścia, w kategorii Nawigacja Obiektowa. (#8600)
* Przy próbie dwókrotnego otwarcia tego samego dialogu, NVDA ustawia kursor na już otwartym dialogu, zamiast wyświetlać błąd. (#5383)
* Zaktualizowano Liblouis do wersji [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Nowe tablice brajlowskie: Rosyjski skróty, Tshivenda pismo pełne, Tshivenda skróty
* Komunikaty "zaznaczone" lub "mrkd" i "podkreślone" lub "hlght" będą ogłaszane zarówno brajlem, jak i mową. (#12892)
* NVDA nie będzie się już wyłączać, gdy pewne dialogi czekają na reakcję użytkownika (np. Potwierdź/Anuluj). (#12984)

### Poprawki błędów

* Śledzenie klawiszy modyfikatorów, takich jak Control lub Insert, jest bardziej wydajne gdy rdzeń wznawia pracę. (#12609)
* Znów możliwe jest sprawdzanie aktualizacji NVDA na niektórych systemach, takich jak czyste wersje instalacyjne Windows. (#12729)
* NVDA poprawnie ogłasza puste komórki tabeli w programie Microsoft Word przy włączonym wsparciu UI automation. (#11043)
* W tabeli ARIA, klawisz Escape zostanie przekierowany do tabeli i nie wyłączy już trybu czytania niezależnie od kontekstu. (#12413)
* Naprawiono błąd, przez który w przeglądarce Google Chrome, nazwa komórki będącej nagłówkiem kolumny w tabeli była ogłaszana dwókrotnie. (#10840)
* NVDA nie wymawia więcej wartość numeryczną suwaków UIA które mają zdefiniowaną tekstualną wartość. (UIA ValuePattern jest od teraz preferowany nad RangeValuePattern). (#12724)
* NVDA nie traktuje więcej wartość suwaków UIA jako oparte na procentowych wartościach.
* Wymawianie lokalizacji komórek w programie Microsoft Excel używane za pomocą UI Automation ponownie działą poprawnie w Windows 11. (#12782)
* NVDA więcej nie ustawia nieprawidłowego języka pythona. (#12753)
* Jeżeli wyłączony dodatek został usunięty a potem ponownie zainstalowany ten sam dodatek będzie ponownie włączony. (#12792)
* Naprawiono błędy dotyczące usuwania oraz instalacji dodatków w przypadkach, gdy foldery dodatków zostały usunięte lub pliko zostało otwarte. (#12792, #12629)
* Używając UI Automation dla dostępu do tabel Microsoft Excel, NVDA więcej nie ogłasza wielokrotnie stan zaznaczania komórek. (#12530)
* Od teraz więcej tekstu będzie odczytywane w LibreOffice Writer, na przykłąd, w oknach dialogowych potwierdzenia. (#11687)
* czytanie / nawigacja za pomocą trybu czytania w programie Microsoft Word za pomocą UI automation od teraz zapewnia poprawne przewijanie dokumentu co wpływa na widoczność aktualnej pozycji w dokumencie, co także wpływa na poprawną synchronizacje widocznej pozycji w trybie czytania i trybie edycji. (#9611)
* Przy odczytywaniu całego dokumentu w programie Microsoft Word uzywając UI automation, dokument jest automatycznie przewijany, a pozycja kursoru aktualizowana. (#9611)
* Przy odczytywaniu wiadomości e-mail w Outlooku a NVDA ma dostęp do kontrolki wiadomości za pomocą UI Automation, większość tabel od teraz jest oznaczona jako tabele wyglądu, co oznacza, że nie będą oczytywane domyślnie. (#11430)
* Naprawiono rzadki błąd przy zmianie urządzeń audio. (#12620)
* Wprowadzanie za pomocą tablic brajlowskich pisma pełnego będzie poprawne. (#12667)
* Przy nawigacji po kalendarzu w obszarze powiadomień, NVDA od teraz wymawia pełną nazwę dnia w tygodniu. (#12757)
* Przy używaniu metod wprowadzania dla języka chińskiego, takich jak Taiwan - Microsoft Quick w programie Microsoft Word, przewijanie w tył i w przód nie powoduje powrót do oryginalnej lokalizacji kursora. (#12855)
* Używając  Microsoft Word za pomocą UIA, nawigacja po zdaniach (alt+strzałka w dół / alt+strzałka w górę) jest pownie możliwa. (#9254)
* Uzywając MS Word za pomocą UIA, od teraz są wymawiane wcięcia akapitów (#12899)
* Używając MS Word za pomocą  UIA, polecenie do śledzenia zmian i niektóre inne lokalizowane polecenia od teraz są wymawiane w programie Word . (#12904)
* Naprawiony błąd przy podwójnym pokazywaniem w brajlu oraz wymawianiem  'opisu gdy opis zgadza sie z  'treścią' lub 'nazwą'. (#12888)
* W MS Word z włączonym wsparciem UIA, od teraz oznajmianie błędów jest bardziej prawidłowe. (#12161)
* W Windowsie 11, NVDA już nie będzie wymawiała "okno" podczas naciskania klawiszy Alt+Tab podczzas przełączania okien. (#12648)
* Nowoczesna strona komentarzy jest od teraz wspierana w programie MS Word gdy dokument nie jest używany za pomocą UIA. Naciśnij alt+f12 aby się przemieszczac pomiędzy stroną komentarzy i dokumencie. (#12982)

### Changes for Developers

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

W tej wersji wprowadzono wstępne wsparcie dla systemu Windows 11.
W związku z tym, że system Windows 11 nie został jeszcze oficjalnie wydany, ta wersja NVDA została przetestowana na wersjach z niejawnego programu testów systemu Windows 11.
Ta wersja zawiera ważną poprawkę dla Kurtyny (Patrz ważne uwagi).
Narzędzie naprawy błędów rejestracji COM od teraz potrafi rozwiązać więcej problemów podczas uruchamiania NVDA.
Zaktualizowano syntezator mowy eSpeak i translator brajla LibLouis.
Naprawiono również liczne błędy i ulepszono m.in. wsparcie brajla, wiersze poleceń systemu Windows, kalkulator, panel emoji oraz historię schowka.

### Ważne uwagi

Z powodu zmiany w API Lupy Systemu Windows, należało zaktualizować Kurtynę, aby wspierała najnowsze wersje systemu Windows.
Użyj NVDA 2021.2 aby włączyć Kurtynę w systemie Windows 10 21H2 (10.0.19044) lub nowszych.
To wydanie zawiera wersje niejawnego programu testów systemu Windows 10 i Windows 11.
Jeśli używasz nowej wersji systemu Windows, dla bezpieczeństwa upewnij się, że przy włączonej Kurtynie ekran jest zupełnie czarny.

### Nowe funkcje

* Eksperymentalne wsparcie dla adnotacji ARIA:
  * Dodaje polecenie służące do odczytu podsumowania szczegółów obiektu z aria-details. (#12364)
  * Dodaje do ustawień zaawansowanych opcję ogłaszania, czy obiekt posiada szczegóły w trybie przeglądu. (#12439) 
* W systemie Windows 10 w Wersji 1909 i nowszych (włącznie z systemem Windows 11), NVDA będzie ogłaszać liczbę sugestii podczas wyszukiwania w Eksploratorze Plików. (#10341, #12628)
* W programie Microsoft Word od teraz NVDA ogłasza wynik wcięcia i skróty wysunięcia gdy zostaną naciśnięte. (#6269)

### Zmiany

* Espeak-ng został zaktualizowany do wersji 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Jeśli włączona została opcja "artykuły" w ustawieniach użytkownika dotyczących formatowania dokumentów, NVDA ogłasza "artykuł" po odczytaniu treści. (#11103)
* Zaktualizowano liblouis braille translator do wersji [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Nowe tablice brajlowskie: Bułgarski pismo pełne, Birmański pismo pełne, Birmański skróty, Kazachski pismo pełne, Khmerski pismo pełne, Północnokurdyjski pismo podstawowe, Północny Sotho pismo pełne, Północny Sotho skróty, Południowy Sotho pismo pełne, Południowy Sotho skróty, Setswana pismo pełne, Setswana skróty, Tatarski pismo pełne, Wietnamski pismo podstawowe, Wietnamski skróty, Południowy wietnamski pismo pełne, Xhosa pismo pełne, Xhosa skróty, Jakucki pismo pełne, Zulu pismo pełne, Zulu skróty
* Windows 10 OCR zmienił nazwę na Windows OCR. (#12690)

### Poprawki błędów

* W Kalkulatorze systemu Windows 10 NVDA będzie wyświetlać wyrażenia kalkulatora na monitorze brajlowskim. (#12268)
* Podczas wprowadzania lub usuwania znaków ze środka linii w programach konsolowych, znaki po prawej stronie kursora systemowego nie będą już czytane w systemie Windows 10 od wersji 1607 i nowszych. (#3200)
  * Diff Match Patch jest od teraz domyślnie włączony. (#12485)
* Wprowadzanie brajla działa prawidłowo z następującymi tablicami skrótów: Arabski skróty, Hiszpański skróty, Urdu skróty, Chiński (Chiny, Mandaryński) bez tonów. (#12541)
* Narzędzie naprawy błędów rejestracji COM od teraz rozwiązuje więcej problemów, zwłaszcza w 64 bitowym systemie Windows. (#12560)
* Poprawa zarządzania przyciskami dla monitorów brajlowskich Seika Notetaker braille device firmy Nippon Telesoft. (#12598)
* Poprawa ogłaszania panelu emoji i historii schowka w systemie Windows. (#11485)
* Zaktualizowano opisy znaków alfabetu bengalskiego. (#12502)
* NVDA zamyka się bezpiecznie podczas uruchamiania nowego procesu. (#12605)
* Ponowne wybranie sterownika monitora brajlowskiego Handy Tech z dialogu "Wybór monitora brajlowskiego" nie powoduje już błędów. (#12618)
* System Windows w wersji 10.0.22000 lub nowszych jest rozpoznawany jako Windows 11, a nie Windows 10. (#12626)
* Wsparcie Kurtyny zostało naprawione i przetestowane dla systemu Windows w wersjach do 10.0.22000. (#12684)
* Jeśli podczas filtrowania zdarzeń wejścia nie wyświetlają się żadne wyniki, ustawienia zdarzeń wejścia nadal działają tak jak powinny. (#12673)
* Naprawiono błąd, przez który pierwszy element w menu rozwijanym nie jest ogłaszany w niektórych kontekstach. (#12624)

### Changes for Developers

* `characterProcessing.SYMLVL_*` constants should be replaced using their equivalent `SymbolLevel.*` before 2022.1. (#11856, #12636)
* `controlTypes` has been split up into various submodules, symbols marked for deprecation must be replaced before 2022.1. (#12510)
  * `ROLE_*` and `STATE_*` constants should be replaced to their equivalent `Role.*` and `State.*`.
  * `roleLabels`, `stateLabels` and `negativeStateLabels` have been deprecated, usages such as `roleLabels[ROLE_*]` should be replaced to their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
  * `processPositiveStates` and `processNegativeStates` have been deprecated for removal.
* On Windows 10 Version 1511 and later (including Insider Preview builds), the current Windows feature update release name is obtained from Windows Registry. (#12509)
* Deprecated: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` will be removed in 2022.1, there is no direct replacement. (#12544)

## 2021.1

To wydanie zawiera opcjonalne, eksperymentalne wsparcie interfejsu UIA w programie Microsoft Excel i przeglądarkach opartych na silniku Chromium.
Wprowadzono poprawki dla kilku języków. Od teraz możliwy jest też dostęp do linków za pomocą monitora brajlowskiego.
Zaktualizowano symbole matematyczne, Unicode CLDR i LibLouis.
Poprawiono też liczne błędy i dodano ulepszenia dla programów takich jak Microsoft Office lub Visual Studio, a także dla kilku języków.

Uwaga!

 * Od tego wydania obecnie używane dodatki tracą zgodność z NVDA.
 * Kończy się też wsparcie technologii Adobe Flash.

### Nowości

* Wstępne wsparcie interfejsu UIA w przeglądarkach opartych na silniku Chromium, takich jak Microsoft Edge. (#12025)
* Opcjonalne, eksperymentalne wsparcie programu Microsoft Excel poprzez interfejs UI Automation. Zalecane tylko dla programu Microsoft Excel w kompilacji 16.0.13522.10000 lub nowszej. (#12210)
* Łatwiejsza nawigacja po treści wyniku w konsoli Pythona NVDA. (#9784)
  * Alt+strzałka w górę/w dół przechodzi do poprzedniego/następnego wyniku. Dodaj shift, aby rozpocząć zaznaczanie.
  * Control+l czyści pole wyników.
* Od teraz NVDA ogłasza kategorie przypisane do zdarzenia w kalendarzu programu Microsoft Outlook, jeśli jakieś są. (#11598)
* Wsparcie dla monitora brajlowskiego Seika Notetaker firmy Nippon Telesoft. (#11514)

### Zmiany

* W trybie przeglądu, kontrolki można od teraz aktywować za pomocą przycisków routingu na opisie danej kontrolki, np. "ln" dla linku. Jest to szczególnie przydatne do aktywowania np. niezaetykietowanych pól wyboru. (#7447)
* NVDA zapobiega używaniu Windows 10 OCR gdy włączona jest kurtyna. (#11911)
* Zaktualizowano bazę danych Emoji (CLDR) do wersji 39.0. (#11943, #12314)
* Dodano więcej symboli matematycznych do słownika symboli. (#11467)
* Odświeżono wygląd podręcznika użytkownika, listy zmian oraz wykazu poleceń klawiszowych. (#12027)
* NVDA ogłasza "Niewspierane" przy próbie przełączenia układu ekranu w aplikacjach, które nie wspierają tej funkcji, np. w programie Microsoft Word. (#7297)
* Opcja 'Próba anulowania mowy dla wygasłych zdarzeń' w panelu ustawień zaawansowanych jest od teraz domyślnie włączona. (#10885)
  * Można wyłączyć to zachowanie ustawiając tę opcję na "Nie".
  * Aplikacje webowe, takie jak Gmail, nie odczytują już nieaktualnych informacji podczas szybkiego przemieszczania kursora.
* Zaktualizowano liblouis braille translator do wersji [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Nowe tablice brajlowskie: Białoruski brajl literacki, Białoruski brajl komputerowy, Urdu pismo pełne, Urdu skróty.
* Wsparcie treści Adobe Flash zostało usunięte z NVDA w związku z porzuceniem tej technologii przez Adobe. (#11131)
* Od teraz NVDA zamyka się nawet gdy okna czytnika ekranu są nadal otwarte. Proces zamykania programu obejmuje wszystkie okna dialogowe NVDA. (#1740)
* Podgląd mowy można zamknąć skrótem `alt+F4`. Ponad to posiada on standardowy przycisk zamykania, aby łatwiej było go zamknąć przy użyciu urządzeń wskazujących. (#12330)
* Przegląd brajla posiada standardowy przycisk zamykania, aby łatwiej było go zamknąć przy użyciu urządzeń wskazujących. (#12328)
* W liście elementów, skrót klawiszowy do przycisku "aktywuj" został usunięty dla niektórych języków aby zapobiec konflikty z przyciskiem opcji filtruj według. When available, the button is still the default of the dialog and as such can still be invoked by simply pressing enter from the elements list itself. (#6167)

### Poprawki błędów

* Lista wiadomości w programie Outlook 2010 jest ponownie czytana. (#12241)
* W programach terminalowych w  Windows 10 wersji 1607 i nowszych, przy wstawianiu oraz usuwaniu znaków w środku linii, znaki z prawa od kursa już nie są czytane. (#3200)
  * Ta eksperymentalna poprawka musi być włączona ręcznie w panelu NVDA ustawień zaawansowanych zmieniając śledzenie zmian konsoli  na Diff Match Patch.
* W MS Outlooku, niechciana odczytywanie dystansu przy naciśnięciu klawiszy shift+tab nie powinno mieć miejsca. (#10254)
* W konsoli Python, wstawianie tabulatora w celu zrobienia wcięcia na początku wypełnionej tekstem linii i wywoływania autouzupełniania w środku linii od teraz jest wspierane. (#11532)
* Informacje o formatowaniu i inne wiadomości w trybue przeglądania nie pokazują pustych linii gdy włączony jest przegląd ekranu. (#12004)
* Od teraz jest możliwe odczytywanie komentarzy w programie MS Word z włączonym interfejsem UIA. (#9285)
* Wydajność przy interakcji z Visual Studio została ulepszona. (#12171)
* Naprawione błędy graficzne takie jak brakujące elementy przy użyciu NVDA w wyglądu z prawo na lewo. (#8859)
* Respektowany jest wygląd okien zależnie od języka . (#638)
  * Znany problem dla języków pisanych z prawa na lewo: prawa granica grupowań rozmywa sie z kontrolkami. (#12181)
* Język Pythona jest ustawiony żeby był zgodny z językiem oznaczonym w ustawieniach, co też jest zastosowane w języku domyślnym. (#12214)
* TextInfo.getTextInChunks już się nie zawiesza na kontrolach wzbotgaconego tekstu takich jak NVDA przegląd logu. (#11613)
* Znowu jest możliwe używanie NVDA w językach zawierających podkreślniki w swoim kodzie Np. de_CH W windowsie 10 1803 i 1809. (#12250)
* W WordPadzie, konfiguracja czytania indeksów gornych oraz dolnych działą jak powinna. (#12262)
* NVDA już  ogłąsza nową treść na stronach internetowych jeżeli stary fokus znika, a na jego miejscu pojawia się nowy. (#12147)
* Przekreślanie, indeks górny i indeks dolny są teraz ogłaszane w Microsoft Excelu jeżeli odpowiednia opcja została włączona. (#12264)
* Naprawiono kopiowanie konfiguracji podczas instalacji kopii przenośnej kiedy domyślny folder konfiguracji jest pusty. (#12071, #12205)
* naprawiono błędne oznajmianie liter z akcentami lub diakrytyków przy włączonej opcji'mów duże przy dużych literach'. (#11948)
* Naprawiono błąd zmiany wysokości w syntezatorach SAPI4. (#12311)
* Instalator NVDA honoruje parametr `--minimal` i nie pdtwarza dźwięk uruchamiania, śledząc to samo dokumentowane zachowanie. (#12289)
* W MS Word lub Outlooku, klawisz szybkiej nawigacji do tabel może służyć do przeskakiwania do tabel wyglądu jeżeli opcja "dołączaj tabele wyglądu" jest włączona w ustawieniach trybu przeglądu. (#11899)
* NVDA już nie będzie wymawiał "↑↑↑" dla emoji w niektórych językach. (#11963)
* Espeak teraz wspeira ponownie kantoński i Mandaryński. (#10418)
* W nowym Microsoft Edgeopartym na siliniku Chromium, pola tekstowe, takie jak pasek adresu są wymawiane gdy są puste. (#12474)
* Naprawiony sterownik dla monitorów brajlowskich Seika. (#10787)

### Changes for Developers

* Note: this is an Add-on API compatibility breaking release. Add-ons will need to be re-tested and have their manifest updated.
* NVDA's build system now fetches all Python dependencies with pip and stores them in a Python virtual environment. This is all done transparently.
  * To build NVDA, SCons should continue to be used in the usual way. E.g. executing scons.bat in the root of the repository. Running `py -m SCons` is no longer supported, and `scons.py` has also been removed.
  * To run NVDA from source, rather than executing `source/nvda.pyw` directly, the developer should now use `runnvda.bat` in the root of the repository. If you do try to execute `source/nvda.pyw`, a message box will alert you this is no longer supported.
  * To perform unit tests, execute `rununittests.bat [<extra unittest discover options>]`
  * To perform system tests: execute `runsystemtests.bat [<extra robot options>]`
  * To perform linting, execute `runlint.bat <base branch>`
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
* TextInfo objects now have start and end properties which can be compared mathematically with operators such as < <= == != >= >. (#11613)
  * E.g. ti1.start <= ti2.end
  * This usage is now prefered instead of ti1.compareEndPoints(ti2,"startToEnd") <= 0
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

This release includes new Chinese Input methods, an update to Liblouis and the elements list (NVDA+f7) now works in focus mode.
Context sensitive help is now available when pressing F1 in NVDA dialogs.
Improvements to symbol pronunciation rules, speech dictionary, Braille message and skim reading.
Bug fixes and improvements to Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
On the web, there are improvements to Google Docs, and greater support for ARIA.
Plus many other important bug fixes and improvements.

### New Features

* Pressing F1 inside NVDA dialogs will now open the help file to most relevant section. (#7757)
* Support for auto complete suggestions (IntelliSense) in Microsoft SQL Server Management Studio plus Visual Studio 2017 and higher. (#7504)
* Symbol pronunciation: Support for grouping in a complex symbol definition and support group references in a replacement rule making them simpler and more powerful. (#11107)
* Users are now notified when attempting to create Speech Dictionary entries with invalid regular expression substitutions. (#11407)
  * Specifically grouping errors are now detected.
* Added support for the new chinese Traditional Quick and Pinyin Input methods in Windows 10. (#11562)
* Tab headers are now considered form fields with quick navigation f key. (#10432)
* Added a command to toggle reporting of marked (highlighted) text; There is no default associated gesture. (#11807)
* Added the --copy-portable-config command line parameter that allows you to automatically copy the provided configuration to the user account when silently installing NVDA. (#9676)
* Braille routing is now supported with the Braille Viewer for mouse users, hover to route to a braille cell. (#11804)
* NVDA will now automatically detect the Humanware Brailliant BI 40X and 20X devices via both USB and Bluetooth. (#11819)

### Changes

* Updated liblouis braille translator to version 3.16.1:
 * Addresses multiple crashes
 * Adds Bashkir grade 1 Braille table
 * Adds Coptic 8 dot computer braille table
 * Adds Russian literary braille and Russian literary braille (detailed) tables
 * Adds Added Afrikaans grade 2 braille table
 * Removes the Russian grade 1 Braille table
* When reading with say all in browse mode, the find next and find previous commands do not stop reading anymore if Allow skim reading option is enabled; say all rather resumes from after the next or previous found term. (#11563)
* For HIMS braille displays F3 has been remapped to Space + dots 148. (#11710)
* Improvements to the UX of the "braille message timeout" and "Show messages indefinitely" options. (#11602)
* In web browsers and other applications that support browse mode, the Elements List dialog (NVDA+F7) can now be invoked when in focus mode. (#10453)
* Updates to ARIA live regions are now suppressed when reporting of dynamic content changes is disabled. (#9077)
* NVDA will now report "Copied to clipboard" before the copied text. (#6757)
* Presentation of graphical view table in disk management has been improved. (#10048)
* Labels for controls are now disabled (greyed out) when the control is disabled. (#11809)
* Updated CLDR emoji annotation to version 38. (#11817)
* The inbuilt "Focus Highlight" feature has been renamed "Vision Highlight". (#11700)

### Bug Fixes

* NVDA once again works correctly with edit fields when using the Fast Log Entry application. (#8996)
* Report elapsed time in Foobar2000 if no total time is available (e.g. when playing a live stream). (#11337)
* NVDA now honors the aria-roledescription attribute on elements in editable content in web pages. (#11607)
* 'list' is no longer announced on every line of a list in Google Docs or other editable content in Google Chrome. (#7562)
* When arrowing by character or word from one list item to another in editable content on the web, entering the new list item is now announced. (#11569)
* NVDA now reads the correct line when the caret is placed at the end of a link on the end of a list item in Google Docs or other editable content on the web. (#11606)
* On Windows 7, opening and closing the start menu from the desktop now sets focus correctly. (#10567)
* When "attempt to cancel expired focus events" is enabled, the title of the tab is now announced again when switching tabs in Firefox. (#11397)
* NVDA no longer fails to announce a list item after typing a character in a list when speaking with the SAPI5 Ivona voices. (#11651)
* It is again possible to use browse mode when reading emails in Windows 10 Mail 16005.13110 and later. (#11439)
* When using the SAPI5 Ivona voices from harposoftware.com, NVDA is now able to save configuration, switch synthesizers, and no longer will stay silent after restarting. (#11650)
* It is now possible to enter number 6 in computer braille from a braille keyboard on HIMS displays. (#11710)
* Major performance improvements in Azure Data Studio. (#11533, #11715)
* With "Attempt to Cancel speech for expired focus events" enabled the title of the NVDA Find dialog is announced again. (#11632)
* NVDA should no longer freeze when waking the computer and focus lands in a Microsoft Edge document. (#11576)
* It is no longer necessary to press tab or move focus after closing a context menu in MS Edge for browse mode to be functional again. (#11202)
* NVDA no longer fails to read items in list views within a 64-bit application such as Tortoise SVN. (#8175)
* ARIA treegrids are now exposed as normal tables in browse mode in both Firefox and Chrome. (#9715)
* A reverse search can now be initiated with 'find previous' via NVDA+shift+F3 (#11770)
* An NVDA script is no longer treated as being repeated if an unrelated key press happens in between the two executions of the script. (#11388) 
* Strong and emphasis tags in Internet Explorer can again be suppressed from being reported by turning off Report Emphasis in NVDA's Document Formatting settings. (#11808)
* A freeze of several seconds experienced by a small amount of users when arrowing between cells in Excel should no longer occur. (#11818)
* In Microsoft Teams builds with version numbers like 1.3.00.28xxx, NVDA no longer fails reading messages in chats or Teams channels due to an incorrectly focused menu. (#11821)
* Text marked both as being a spelling and grammar error at the same time in Google Chrome will be appropriately announced as both a spelling and grammar error by NVDA. (#11787)
* When using Outlook (French locale), the shortcut for 'Reply all' (control+shift+R) works again. (#11196)
* In Visual Studio, IntelliSense tool tips that provide additional details about the currently selected IntelliSense item are now only reported once. (#11611)
* In Windows 10 Calculator, NVDA will not announce progress of calculations if speak typed characters is disabled. (#9428)
* NVDA no longer crashes when using English US grade 2 and expand to computer Braille at the cursor is on, when displaying certain content such as a URL in Braille. (#11754)
* It is again possible to report formatting information for the focused Excel cell using NVDA+F. (#11914)
* QWERTY input on Papenmeier braille displays that support it again works and no longer causes NVDA to randomly freeze. (#11944)
* In Chromium based browsers, several cases were solved where table navigation didn't work and NVDA didn't report the number of rows/columns of the table. (#12359)

### Changes for Developers

* System tests can now send keys using spy.emulateKeyPress, which takes a key identifier that conforms to NVDA's own key names, and by default also blocks until the action is executed. (#11581)
* NVDA no longer requires the current directory to be the NVDA application directory in order to function. (#6491)
* The aria live politeness setting for live regions can now be found on NVDA Objects using the liveRegionPoliteness property. (#11596)
* It is now possible to define separate gestures for Outlook and Word document. (#11196)

## 2020.3

This release includes several large improvements to stability and performance particularly in Microsoft Office applications. There are new settings to toggle touchscreen support and graphics reporting.
The existence of marked (highlighted) content can be reported in browsers, and there are new German braille tables.

### New Features

* You can now toggle reporting of graphics from NVDA's document formatting settings. Note that disabling this option will still read the alternative texts of graphics. (#4837)
* You can now toggle NVDA's touchscreen support. An option has been added to the Touch Interaction panel of NVDA's settings. The default gesture is NVDA+control+alt+t. (#9682)
* Added new German braille tables. (#11268)
* NVDA now detects read-only text UIA controls. (#10494)
* The existence of marked (highlighted) content is reported in both speech and braille in all web browsers. (#11436)
 * This can be toggled on and off by a new NVDA Document Formatting option for Highlighting.
* New emulated system keyboard keys can be added from NVDA's Input gestures dialog. (#6060)
  * To do this, press the add button after you selected the Emulated system keyboard keys category.
* Handy Tech Active Braille with joystick is now supported. (#11655)
* "Automatic focus mode for caret movement" setting is now compatible with disabling "Automatically set focus to focusable elements". (#11663)

### Changes

* The Report formatting script (NVDA+f) has now been changed to report the formatting at the system caret rather than at the review cursor position. To report formatting at the review cursor position now use NVDA+shift+f. (#9505)
* NVDA no longer automatically sets the system focus to focusable elements by default in browse mode, improving performance and stability. (#11190)
* CLDR updated from version 36.1 to version 37. (#11303)
* Updated eSpeak-NG to 1.51-dev, commit 1fb68ffffea4
* You can now utilize table navigation in list boxes with checkable list items when the particular list has multiple columns. (#8857)
* In the Add-ons manager, when prompted to confirm removal of an add-on, "No" is now the default. (#10015)
* In Microsoft Excel, the Elements List dialog now presents formulas in their localized form. (#9144)
* NVDA now reports the correct terminology for notes in MS Excel. (#11311)
* When using the "move review cursor to focus" command in browse mode, the review cursor is now set at the position of the virtual caret. (#9622)
* Information reported in browse mode, such as the formatting info with NVDA+F, are now displayed in a slightly bigger window centered on screen. (#9910)

### Bug Fixes

* NVDA now always speaks when navigating by word and landing on any single symbol followed by white space, whatever the verbosity settings. (#5133)
* In applications using QT 5.11 or newer, object descriptions are again reported. (#8604)
* When deleting a word with control+delete, NVDA no longer remains silent. (#3298, #11029)
  * Now the word to the right of the deleted word is announced.
* In general settings panel, the language list is now sorted correctly. (#10348)
* In the Input Gestures dialog, significantly improved performance while filtering. (#10307)
* You can now send Unicode characters beyond U+FFFF from a braille display. (#10796)
* NVDA will announce Open With dialog content in Windows 10 May 2020 Update. (#11335)
* A new experimental option in Advanced settings (Enable selective registration for UI Automation events and property changes) can provide major performance improvements in Microsoft Visual Studio and other UIAutomation based applications if enabled. (#11077, #11209)
* For checkable list items, the selected state is no longer announced redundantly, and if applicable, the unselected state is announced instead. (#8554)
* On Windows 10 May 2020 Update, NVDA now shows the Microsoft Sound Mapper when viewing output devices from synthesizer dialog. (#11349)
* In Internet Explorer, numbers are now announced correctly for ordered lists if the list does not start with 1. (#8438)
* In Google chrome, NVDA will now report not checked for all checkable controls (not just check boxes) that are currently not checked. (#11377)
* It is once again possible to navigate in various controls when NVDA's language is set to Aragonese. (#11384)
* NVDA should no longer sometimes freeze in Microsoft Word when rapidly arrowing up and down or typing characters with Braille enabled. (#11431, #11425, #11414)
* NVDA no longer appends nonexistent trailing space when copying the current navigator object to the clipboard. (#11438)
* NVDA no longer activates the Say All profile if there is nothing to read. (#10899, #9947)
* NVDA is no longer unable to read the features list in Internet Information Services (IIS) Manager. (#11468)
* NVDA now keeps the audio device open improving performance on some sound cards (#5172, #10721)
* NVDA will no longer freeze or exit when holding down control+shift+downArrow in Microsoft Word. (#9463)
* The expanded / collapsed state of directories in the navigation treeview on drive.google.com is now always reported by NVDA. (#11520)
* NVDA will auto detect the NLS eReader Humanware braille display via Bluetooth as its Bluetooth name is now "NLS eReader Humanware". (#11561)
* Major performance improvements in Visual Studio Code. (#11533)

### Changes For Developers

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

Highlights of this release include support for a new braille display from Nattiq, better support for ESET antivirus GUI and Windows Terminal, performance improvements in 1Password, and with Windows OneCore synthesizer. Plus many other important bug fixes and improvements.

### New Features

* Support for new braille displays:
  * Nattiq nBraille (#10778)
* Added script to open NVDA configuration directory (no default gesture). (#2214)
* Better support for ESET antivirus GUI. (#10894)
* Added support for Windows Terminal. (#10305)
* Added a command to report the active configuration profile (no default gesture). (#9325)
* Added a command to toggle reporting of subscripts and superscripts (no default gesture). (#10985)
* Web applications (E.G. Gmail) no longer speak outdated information when moving focus rapidly. (#10885)
  * This experimental fix must be manually enabled via the 'Attempt to cancel speech for expired focus events' option in the advanced settings panel.
* Many more symbols have been added to the default symbols dictionary. (#11105)

### Changes

* Updated liblouis braille translator from 3.12 to [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* The reporting of superscripts and subscripts is now controlled separately to the reporting of font attributes. (#10919)
* Due to changes made in VS Code, NVDA no longer disables browse mode in Code by default. (#10888)
* NVDA no longer reports "top" and "bottom" messages when moving the review cursor directly to the first or last line of the current navigator object with the move to top and move to bottom review cursor scripts respectively. (#9551)
* NVDA no longer reports  "left" and "right" messages when directly moving the review cursor to the first or last character of the line for the current navigator object with the move to beginning of line and move to end of line review cursor scripts respectively. (#9551)

### Bug Fixes

* NVDA now starts correctly when the log file cannot be created. (#6330)
* In recent releases of Microsoft Word 365, NVDA will no longer announce "delete back word" when Control+Backspace is pressed while editing a document. (#10851)
* In Winamp, NVDA will once again announce toggle status of shuffle and repeat. (#10945)
* NVDA is no longer extremely sluggish when moving within the list of items in 1Password. (#10508)
* The Windows OneCore speech synthesizer no longer lags between utterances. (#10721)
* NVDA no longer freezes when you open the context menu for 1Password in the system notification area. (#11017)
* In Office 2013 and older:
  * Ribbons are announced when focus moves to them for the first time. (#4207)
  * Context menu items  are once again reported properly. (#9252)
  * Ribbon sections are consistently announced when navigating with Control+arrows. (#7067)
* In browse mode in Mozilla Firefox and Google Chrome, text no longer incorrectly appears on a separate line when web content uses CSS display: inline-flex. (#11075)
* In browse mode with Automatically set system focus to focusable elements disabled, it is now possible to activate elements that aren't focusable.
* In browse mode with Automatically set system focus to focusable elements disabled, it is now possible to activate elements reached by pressing the tab key. (#8528)
* In browse mode with Automatically set system focus to focusable elements disabled, activating certain elements no longer clicks in an incorrect location. (#9886)
* NVDA error sounds are no longer heard when accessing DevExpress text controls. (#10918)
* The tool-tips of the icons in the system tray are no longer reported upon keyboard navigation if their text is equal to the name of the icons, to avoid double announcing. (#6656)
* In browse mode with 'Automatically set system focus to focusable elements' disabled, switching to focus mode with NVDA+space now focuses the element under the caret. (#11206)
* It is once again possible to check for NVDA updates on certain systems; e.g. clean Windows installs. (#11253)
* Focus is not moved in Java application when the selection is changed in an unfocused tree, table or list. (#5989)

### Changes For Developers

* execElevated and hasUiAccess have moved from config module to systemUtils module. Usage via config module is deprecated. (#10493)
* Updated configobj to 5.1.0dev commit f9a265c4. (#10939)
* Automated testing of NVDA with Chrome and a HTML sample is now possible. (#10553)
* IAccessibleHandler has been converted into a package, OrderedWinEventLimiter has been extracted to a module and unit tests added (#10934)
* Updated BrlApi to version 0.8 (BRLTTY 6.1). (#11065)
* Status bar retrieval may now be customized by an AppModule. (#2125, #4640)
* NVDA no longer listens for IAccessible EVENT_OBJECT_REORDER. (#11076)
* A broken ScriptableObject (such as a GlobalPlugin missing a call to its base class' init method) no longer breaks NVDA's script handling. (#5446)

## 2020.1

Highlights of this release include support for several new braille displays from HumanWare and APH, plus many other important bug fixes such as the ability to again read math in Microsoft Word using MathPlayer / MathType.

### New Features

* The currently selected item in listboxes is again presented in browse mode in Chrome, similar to NVDA 2019.1. (#10713)
* You can now perform right mouse clicks on touch devices by doing a one finger tap and hold. (#3886)
* Support for New braille displays: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, and NLS eReader. (#10830)

### Changes

* NVDA will prevent the system from locking or going to sleep when in say all. (#10643)
* Support for out-of-process iframes in Mozilla Firefox. (#10707)
* Updated liblouis braille translator to version 3.12. (#10161)

### Bug Fixes

* Fixed NVDA not announcing Unicode minus symbol (U+2212). (#10633)
* When installing add-on from add-ons manager, names of files and folders in the browse window are no longer reported twice. (#10620, #2395)
* In Firefox, when loading Mastodon with the advanced web interface enabled, all timelines now render correctly in browse mode. (#10776)
* In browse mode, NVDA now reports "not checked" for unchecked check boxes where it sometimes didn't previously. (#10781)
* ARIA switch controls no longer report confusing information such as "not pressed checked" or "pressed checked". (#9187)
* SAPI4 voices should no longer refuse to speak certain text. (#10792)
* NVDA can again read and interact with math equations in Microsoft Word. (#10803)
* NVDA will again announce text being unselected in browse mode if pressing an arrow key while text is selected. (#10731).
* NVDA no longer exits if there is an error initializing eSpeak. (#10607)
* Errors caused by unicode in translations for shortcuts no longer stop the installer, mitigated by falling back to the English text. (#5166, #6326)
* Arrowing out and away from lists and tables in sayAll with skim reading enabled no longer continuously announces exiting the list or table. (#10706)
* Fix mouse tracking for some MSHTML elements in Internet Explorer. (#10736)

### Changes for Developers

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

NVDA 2019.3 is a very significant release containing many under-the-hood changes including the upgrade of Python 2 to Python 3, and a major re-write of NVDA's speech subsystem.
Although these changes do break compatibility with older NVDA add-ons, the upgrade to Python 3 is necessary for security, and the changes to speech allow for  some exciting innovations in the near future.
 Other highlights in this release include 64 bit support for Java VMs, Screen Curtain and Focus Highlight functionality, support for more braille displays and a new Braille viewer, and many many other bug fixes.

### New Features

* The accuracy of the move mouse to navigator object command has been improved in text fields in Java applications. (#10157)
* Added support for  the following Handy Tech Braille displays (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* All user-defined gestures can now be removed via a new "Reset to factory defaults" button in the Input Gestures dialog. (#10293)
* Font reporting in Microsoft Word now includes if text is marked as hidden. (#8713)
* Added a command to move the review cursor to the position previously set as start marker for selection or copy: NVDA+shift+F9. (#1969)
* In Internet Explorer, Microsoft Edge and recent versions of Firefox and Chrome, landmarks are now reported in focus mode and object navigation. (#10101)
* In Internet Explorer, Google Chrome and Mozilla Firefox, You can now navigate by article and grouping using quick navigation scripts. These scripts are unbound by default and can be assigned in the Input Gestures dialog when the dialog is opened from a browse mode document. (#9485, #9227)
 * Figures are also reported. They are considered objects and therefore navigable with the o quick navigation key.
* In Internet Explorer, Google Chrome and Mozilla Firefox, article elements are now reported with object navigation, and optionally in browse mode if turned on in Document Formatting settings. (#10424)
* Added screen curtain, which when enabled, makes the whole screen black on Windows 8 and later. (#7857)
 * Added a script to enable screen curtain (until next restart with one press, or always while NVDA is running with two presses), no default gesture is assigned.
 * Can be enabled and configured via the 'vision' category in NVDA's settings dialog.
* Added screen highlight functionality to NVDA. (#971, #9064)
 * Highlighting of the focus, navigator object, and browse mode caret position can be enabled and configured via the 'vision' category in NVDA's settings dialog.
 * Note: This feature is incompatible with the focus highlight add-on, however, the add-on can still be used while the built-in highlighter is disabled.
* Added Braille Viewer tool, allows viewing braille output via an on-screen window. (#7788)

### Changes

* The user guide now describes how to use NVDA in the Windows Console. (#9957)
* Running nvda.exe now defaults to replacing an already running copy of NVDA. The -r|--replace command line parameter is still accepted, but ignored. (#8320)
* On Windows 8 and later, NVDA will now report product name and version information for hosted apps such as apps downloaded from Microsoft Store using information provided by the app. (#4259, #10108)
* When toggling track changes on and off with the keyboard in Microsoft Word, NVDA will announce the state of the setting. (#942) 
* The NVDA version number is now logged as the first message in the log. This occurs even if logging has been disabled from the GUI. (#9803)
* The settings dialog no longer allows for changing the configured log level if it has been overridden from the command line. (#10209)
* In Microsoft Word, NVDA now announces the display state of non printable characters when pressing the toggle shortcut Ctrl+Shift+8 . (#10241)
* Updated Liblouis braille translator to commit 58d67e63. (#10094)
* When CLDR characters (including emojis) reporting is enabled, they are announced at all punctuation levels. (#8826)
* Third party python packages included in NVDA, such as comtypes, now log their warnings and errors to the NVDA log. (#10393)
* Updated Unicode Common Locale Data Repository emoji annotations to version 36.0. (#10426)
* When focussing a grouping in browse mode, the description is now also read. (#10095)
* The Java Access Bridge is now included with NVDA to enable access to Java applications, including for 64 bit Java VMs. (#7724)
* If the Java Access Bridge is not enabled for the user, NVDA automatically enables it at NVDA startup. (#7952)
* Updated eSpeak-NG to 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Bug Fixes

* Emoji and other 32 bit unicode characters now take less space on a braille display when they are shown as hexadecimal values. (#6695)
* In Windows 10, NVDA will announce tooltips from universal apps if NVDA is configured to report tooltips in object presentation dialog. (#8118)
* On Windows 10 Anniversary Update and later, typed text is now reported in Mintty. (#1348)
* On Windows 10 Anniversary Update and later, output in the Windows Console that appears close to the caret is no longer spelled out. (#513)
* Controls in Audacitys compressor dialog are now announced when navigating the dialog. (#10103)
* NVDA no longer treats spaces as words in object review in Scintilla based editors such as Notepad++. (#8295)
* NVDA will prevent the  system from entering sleep mode when scrolling through text with braille display gestures. (#9175)
* On Windows 10, braille will now follow when editing cell contents in Microsoft Excel and in other UIA text controls where it was lagging behind. (#9749)
* NVDA will once again report suggestions in the Microsoft Edge address bar. (#7554)
* NVDA is no longer silent when focusing an HTML tab control header in Internet Explorer. (#8898)
* In Microsoft Edge based on EdgeHTML, NVDA will no longer play search suggestion sound when the window becomes maximized. (#9110, #10002)
* ARIA 1.1 combo boxes are now supported in Mozilla Firefox and Google Chrome. (#9616)
* NVDA will no longer report content of visually hidden columns for list items in SysListView32 controls. (#8268)
* The settings dialog no longer shows "info" as the current log level when in secure mode. (#10209)
* In Start menu for Windows 10 Anniversary Update and later, NVDA will announce details of search results. (#10340)
* In browse mode, if moving the cursor or using quick navigation causes the document to change, NVDA no longer speaks incorrect content in some cases. (#8831, #10343)
* Some bullet names in Microsoft Word have been corrected. (#10399)
* In Windows 10 May 2019 Update and later, NVDA will once again announce first selected emoji or clipboard item when emoji panel and clipboard history opens, respectively. (#9204)
* In Poedit, it is once again possible to view some translations for right to left languages. (#9931)
* In the Settings app in Windows 10 April 2018 Update and later, NVDA will no longer announce progress bar information for volume meters found in the System/Sound page. (#10412)
* Invalid regular expressions in speech dictionaries no longer completely break speech in NVDA. (#10334)
* When reading bulleted items in Microsoft Word with UIA enabled, the bullet from the next list item is no longer inappropriately announced. (#9613)
* Some rare braille translation issues and errors with liblouis have been resolved. (#9982)
* Java applications started before NVDA are now accessible without the need to restart the Java app. (#10296)
* In Mozilla Firefox, when the focused element becomes marked as current (aria-current), this change is no longer spoken multiple times. (#8960)
* NVDA will now treat certain composit unicode characters such as e-acute as one single character when moving through text. (#10550)
* Spring Tool Suite Version 4 is now supported. (#10001)
* Don't double speak name when aria-labelledby relation target is an inner element. (#10552)
* On Windows 10 version 1607 and later, typed characters from Braille keyboards are spoken in more situations. (#10569)
* When changing the audio output device, tones played by NVDA will now play through the newly selected device. (#2167)
* In Mozilla Firefox, moving focus in browse mode is faster. This makes moving the cursor in browse mode more responsive in many cases. (#10584)

### Changes for Developers

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
* scriptHandler.isCurrentScript has been removed due to lack of use. There is no replacement. (#8677)

## 2019.2.1

This is a minor release to fix several crashes present in 2019.2. Fixes include:

* Addressed several crashes in Gmail seen in both Firefox and Chrome when interacting with particular popup menus such as when creating filters or changing certain Gmail settings. (#10175, #9402, #8924)
* In Windows 7, NVDA no longer causes Windows Explorer to crash when the mouse is used in the start menu. (#9435) 
* Windows Explorer on Windows 7 no longer crashes when accessing metadata edit fields. (#5337) 
* NVDA no longer freezes when interacting with images with a base64 URI in Mozilla Firefox or Google Chrome. (#10227)

## 2019.2

Highlights of this release include auto detection of Freedom Scientific braille displays, an experimental setting in the Advanced panel to stop browse mode from automatically moving focus (which may provide performance improvements), a rate boost option for the Windows OneCore synthesizer to achieve very fast rates, and many other bug fixes.

### New Features

* NVDA's Miranda NG support  works with newer versions of the client. (#9053) 
* You can now disable browse mode by default by disabling the new "Enable browse mode on page load" option in NVDA's browse mode settings. (#8716) 
 * Note that when this option is disabled, you can still enable browse mode manually by pressing NVDA+space.
* You can now filter symbols in the punctuation/symbol pronunciation dialog, similar to how filtering works in the elements list and input gestures dialog. (#5761)
* A command has been added to change the mouse text unit resolution (how much text will be spoken when the mouse moves), it has not been assigned a default gesture. (#9056)
* The windows OneCore synthesizer now has a rate boost option, which allows for significantly faster speech. (#7498)
* The Rate Boost option is now configurable from the Synth Settings Ring for supported speech synthesizers. (Currently eSpeak-NG and Windows OneCore). (#8934)
* Configuration profiles can now be manually activated with gestures. (#4209)
 * The gesture must be configured in the "Input gestures" dialog.
* In Eclipse, added support for autocompletion in code editor. (#5667)
 * Additionally, Javadoc information can be read from the editor when it is present by using NVDA+d.
* Added an experimental option to the Advanced Settings panel that allows you to stop the system focus from following the browse mode cursor (Automatically set system focus to focusable elements). (#2039) Although this may not be suitable to turn off for all websites, this may fix: 
 * Rubber band effect: NVDA sporadically undoes the last browse mode keystroke by jumping to the previous location.
 * Edit boxes steal system focus when arrowing down through them on some websites.
 * Browse mode keystrokes are slow to respond.
* For braille display drivers that support it, driver settings can now be changed from the braille settings category in NVDA's settings dialog. (#7452)
* Freedom Scientific braille displays are now supported by braille display auto detection. (#7727)
* Added a command to show the replacement for the symbol under the review cursor. (#9286)
* Added an experimental option to the Advanced Settings panel that allows you to try out a new, work-in-progress rewrite of NVDA's Windows Console support using the Microsoft UI Automation API. (#9614)
* In the Python Console, the input field now supports pasting multiple lines from the clipboard. (#9776)

### Changes

* Synthesizer volume is now increased and decreased by 5 instead of 10 when using the settings ring. (#6754)
* Clarified the text in the add-on manager when NVDA is launched with the --disable-addons flag. (#9473)
* Updated Unicode Common Locale Data Repository emoji annotations to version 35.0. (#9445)
* The hotkey for the filter field in the elements list in browse mode has changed to alt+y. (#8728)
* When an auto detected braille display is connected via Bluetooth, NVDA will keep searching for USB displays supported by the same driver and switch to a USB connection if it becomes available. (#8853)
* Updated eSpeak-NG to commit 67324cc.
* Updated liblouis braille translator to version 3.10.0. (#9439, #9678)
* NVDA will now report the word 'selected' after reporting the text a user has just selected.(#9028, #9909)
* In Microsoft Visual Studio Code, NVDA is in focus mode by default. (#9828)

### Bug Fixes

* NVDA no longer crashes when an add-on directory is empty. (#7686)
* LTR and RTL marks are no longer reported in Braille or per-character speech when accessing the properties window. (#8361)
* When jumping to form fields with Browse Mode quick navigation, the entire form field is now announced rather than just the first line. (#9388)
* NVDA will no longer become silent after exiting the Windows 10 Mail app. (#9341)
* NVDA no longer fails to start when the users regional settings are set to a locale unknown to NVDA, such as English (Netherlands). (#8726)
* When browse mode is enabled in Microsoft Excel and you switch to a browser in focus mode or vice versa, browse mode state is now reported appropriately. (#8846)
* NVDA now properly reports the line at the mouse cursor in Notepad++ and other Scintilla based editors. (#5450)
* In Google Docs (and other web-based editors), braille no longer sometimes incorrectly shows "lst end" before the cursor in the middle of a list item. (#9477)
* In the Windows 10 May 2019 Update, NVDA no longer speaks many volume notifications if changing the volume with hardware buttons when File Explorer has focus. (#9466)
* Loading the punctuation/symbol pronunciation dialog is now much faster when using symbol dictionaries containing over 1000 entries. (#8790)
* In Scintilla controls such as Notepad++, NVDA can read the correct line when wordwrap is enabled. (#9424)
* In Microsoft Excel, the cell location is announced after it changes due to the shift+enter or shift+numpadEnter gestures. (#9499)
* In Visual Studio 2017 and up, in the Objects Explorer window, the selected item in objects tree or members tree with categories is now reported correctly. (#9311)
* Add-ons with names that only differ in capitalization are no longer treated as separate add-ons. (#9334)
* For Windows OneCore voices, the rate set in NVDA is no longer affected by the rate set in Windows 10 Speech Settings. (#7498)
* The log can now be opened with NVDA+F1 when there is no developer info for the current navigator object. (#8613)
* It is again possible to use NVDA's table navigation commands in Google Docs, in Firefox and Chrome. (#9494)
* The bumper keys now work correctly on Freedom Scientific braille displays. (#8849)
* When reading the first character of a document in Notepad++ 7.7 X64, NVDA no longer freezes for up to ten seconds. (#9609)
* HTCom can now be used with a Handy Tech Braille display in combination with NVDA. (#9691)
* In Mozilla Firefox, updates to a live region are no longer reported if the live region is in a background tab. (#1318)
* NVDA's browse mode Find dialog no longer fails to function if NVDA's About dialog is currently open in the background. (#8566)

### Changes for Developers

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

This point release fixes the following bugs:

* NVDA no longer causes Excel 2007 to crash or refuses to report if a cell has a formula. (#9431)
* Google Chrome no longer crashes when interacting with certain listboxes. (#9364)
* An issue has been fixed which prevented copying a users configuration to the system configuration profile. (#9448)
* In Microsoft Excel, NVDA again uses the localized message when reporting the location of merged cells. (#9471)

## 2019.1

Highlights of this release include performance improvements when accessing both Microsoft word and Excel, stability and security improvements such as support for add-ons with version compatibility information, and many other bug fixes.

Please note that starting from this release of NVDA, custom appModules, globalPlugins, braille display drivers and synth drivers will no longer be automatically loaded from your NVDA user configuration directory. 
Rather these  should be installed as part of an NVDA add-on. For those developing code for an add-on, code for testing can be placed in a new developer scratchpad directory in the NVDA user configuration directory,  if the Developer scratchpad option  is turned on in NVDA's new Advanced settings panel.
These changes are necessary to better ensure compatibility of custom code, so that NVDA does not break when this code becomes incompatible with newer releases.
Please refer to the list of changes further down for more details on this and how add-ons are now better versioned.

### New Features

* New braille tables: Afrikaans, Arabic 8 dot computer braille, Arabic grade 2, Spanish grade 2. (#4435, #9186)
* Added an option to NVDA's mouse settings to make NVDA handle situations where the mouse is controlled by another application. (#8452) 
 * This will allow NVDA to track the mouse when a system is controlled remotely using TeamViewer or other remote control software.
* Added the `--enable-start-on-logon` command line parameter to allow configuring whether silent installations of NVDA set NVDA to start at Windows logon or not. Specify true to start at logon or false to not start at logon. If the --enable-start-on-logon argument is not specified at all then NVDA will default to starting at logon, unless it was  already configured not to by a previous installation. (#8574)
* It is possible to turn NVDA's logging features off by setting logging level to "disabled" from General settings panel. (#8516)
* The presence of formulae in LibreOffice and Apache OpenOffice spreadsheets is now reported. (#860)
* In Mozilla Firefox and Google Chrome, browse mode now reports the selected item in list boxes and trees.
 * This works in Firefox 66 and later.
 * This does not work for certain list boxes (HTML select controls) in Chrome.
* Early support for apps such as Mozilla Firefox on computers with ARM64 (e.g. Qualcomm Snapdragon) processors. (#9216)
* A new Advanced Settings category has been added to NVDA's Settings dialog, including an option to try out NVDA's new support for Microsoft Word via the Microsoft UI Automation API. (#9200)
* Added support for the graphical view in Windows Disk Management. (#1486)
* Added support for Handy Tech Connect Braille and Basic Braille 84. (#9249)

### Changes

* Updated liblouis braille translator to version 3.8.0. (#9013)
* Add-on authors now can enforce a minimum required NVDA version for their add-ons. NVDA will refuse to install or load an add-on whose minimum required NVDA version is higher than the current NVDA version. (#6275)
* Add-on authors can now specify the last version of NVDA the add-on has been tested against. If an add-on has been only tested against a  version of NVDA lower than the current version, then NVDA will refuse to install or load the add-on. (#6275)
* This version of NVDA will allow installing and loading of add-ons  that do not yet contain Minimum and Last Tested NVDA version information, but upgrading to future versions of NVDA (E.g. 2019.2) may automatically cause these older add-ons to be disabled.
* The move mouse to navigator object command is now available in Microsoft Word as well as for UIA controls, particularly Microsoft Edge. (#7916, #8371)
* Reporting of text under the mouse has been improved within Microsoft Edge and other UIA applications. (#8370)
* When NVDA is started with the `--portable-path` command line parameter, the provided path is automatically filled in when trying to create a portable copy of NVDA using the NVDA menu. (#8623)
* Updated the path to the Norwegian braille table to reflect the standard from the year 2015. (#9170)
* When navigating by paragraph (control+up or down arrows) or navigating by table cell (control+alt+arrows), the existence of spelling errors will no longer be announced, even if NVDA is configured to announce these automatically. This is because paragraphs and table cells can be quite large, and detecting spelling errors in some applications can be very costly. (#9217)
* NVDA no longer automatically loads custom appModules, globalPlugins and braille and synth drivers from the NVDA user configuration directory. This code should be instead packaged as an add-on with correct version information, ensuring that incompatible code is not run with current versions of NVDA. (#9238)
 * For developers who need to test code as it is being developed,  enable NVDA's developer scratchpad directory in the Advanced category of NVDA settings, and place your code in the 'scratchpad' directory found in the NVDA user configuration directory when this option is enabled.

### Bug Fixes

* When using OneCore speech synthesizer on Windows 10 April 2018 Update and later, large chunks of silence are no longer inserted between speech utterances. (#8985)
* When moving by character in plain text controls (such as Notepad) or browse mode, 32 bit emoji characters consisting of two UTF-16 code points (such as 🤦) will now read properly. (#8782)
* Improved restart confirmation dialog after changing NVDA's interface language. The text and the button labels are now more concise and less confusing. (#6416)
* If a 3rd party speech synthesizer fails to load, NVDA will fall back to Windows OneCore speech synthesizer on Windows 10, rather than espeak. (#9025)
* Removed the "Welcome Dialog" entry in the NVDA menu while on secure screens. (#8520)
* When tabbing or using quick navigation in browse mode, legends on tab panels are now reported more consistently. (#709)
* NVDA will now announce selection changes for certain time pickers such as in the Alarms and Clock app in Windows 10. (#5231)
* In Windows 10's Action Center, NVDA will announce status messages when toggling quick actions such as brightness and focus assist. (#8954)
* In action Center in Windows 10 October 2018 Update and earlier, NVDA will recognize brightness quick action control as a button instead of a toggle button. (#8845)
* NVDA will again track cursor and announce deleted characters in the Microsoft Excel  go to and find edit fields. (#9042)
* Fixed a rare browse mode crash in Firefox. (#9152)
* NVDA no longer fails to report the focus for some controls in the Microsoft Office 2016 ribbon when collapsed.
* NVDA no longer fails to report the suggested contact when entering addresses in new messages in Outlook 2016. (#8502)
* The last few cursor routing keys on 80 cell eurobraille displays no longer route the cursor to a position at or just after the start of the braille line. (#9160)
* Fixed table navigation in threaded view in Mozilla Thunderbird. (#8396)
* In Mozilla Firefox and Google Chrome, switching to focus mode now works correctly for certain list boxes and trees (where the list box/tree is not itself focusable but its items are) . (#3573, #9157)
* Browse mode is now correctly turned on by default when reading messages in Outlook 2016/365 if using NVDA's experimental UI Automation support for Word Documents. (#9188)
* NVDA is now less likely to freeze in such a way that the only way to escape is signing out from your current windows session. (#6291)
* In Windows 10 October 2018 Update and later, when opening cloud clipboard history with clipboard empty, NVDA will announce clipboard status. (#9103)
* In Windows 10 October 2018 Update and later, when searching for emojis in emoji panel, NVDA will announce top search result. (#9105)
* NVDA no longer freezes in the main window of Oracle VirtualBox 5.2 and above. (#9202)
* Responsiveness in Microsoft Word when navigating by line, paragraph or table cell may be significantly improved in some documents. A reminder that for best performance, set Microsoft Word to Draft view with alt+w,e after opening a document. (#9217) 
* In Mozilla Firefox and Google Chrome, empty alerts are no longer reported. (#5657)
* Significant performance improvements when navigating cells in Microsoft Excel, particularly when the spreadsheet contains comments and or validation dropdown lists. (#7348)
* It should be no longer necessary to turn off in-cell editing in Microsoft Excel's options to access the cell edit control with NVDA in Excel 2016/365. (#8146).
* Fixed a freeze in Firefox sometimes seen when quick navigating by landmarks, if the Enhanced Aria add-on is in use. (#8980)

### Changes for Developers

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

This release fixes a crash at start up if NVDA's user interface language is set to Aragonese. (#9089)

## 2018.4

Highlights of this release include performance improvements in recent Mozilla Firefox versions, announcement of emojis with all synthesizers, reporting of replied/forwarded status in Outlook, reporting the distance of the cursor to the edge of a Microsoft Word page, and many bug fixes.

### New Features

* New braille tables: Chinese (China, Mandarin) grade 1 and grade 2. (#5553)
* Replied / Forwarded status is now reported on mail items in the Microsoft Outlook message list. (#6911)
* NVDA is now able to read descriptions for emoji as well as other characters that are part of the Unicode Common Locale Data Repository. (#6523)
* In Microsoft Word, the cursor's distance from the top and left edges of the page can be reported by pressing NVDA+numpadDelete. (#1939)
* In Google Sheets with braille mode enabled, NVDA no longer announces 'selected' on every cell when moving focus between cells. (#8879)
* Added support for Foxit Reader and Foxit Phantom PDF. (#8944)
* Added support for the DBeaver database tool. (#8905)

### Changes

* "Report help balloons" in the Object Presentations dialog has been renamed to "Report notifications" to include reporting of toast notifications in Windows 8 and later. (#5789)
* In NVDA's keyboard settings, the checkboxes to enable or disable NVDA modifier keys are now displayed in a list rather than as separate checkboxes.
* NVDA will no longer present redundant information when reading clock system tray on some versions of Windows. (#4364)
* Updated liblouis braille translator to version 3.7.0. (#8697)
* Updated eSpeak-NG to commit 919f3240cbb.

### Bug Fixes

* In Outlook 2016/365, the category and flag status are reported for messages. (#8603)
* When NVDA is set to languages such as Kirgyz, Mongolian or Macedonian, it no longer shows a dialog on start-up warning that the language is not supported by the Operating System. (#8064)
* Moving the mouse to the navigator object will now much more accurately move the mouse to the browse mode position in Mozilla Firefox, Google Chrome and Acrobat Reader DC. (#6460)
* Interacting with combo boxes on the web in Firefox, Chrome and Internet Explorer has been improved. (#8664)
* If running on the Japanese version of Windows XP or Vista, NVDA now displays OS version requirements message as expected. (#8771)
* Performance improvements when navigating large pages with lots of dynamic changes in Mozilla Firefox. (#8678)
* Braille no longer shows font attributes  if they have been disabled in  Document Formatting settings. (#7615)
* NVDA no longer fails to track focus in File Explorer and other applications using UI Automation when another app is busy (such as batch processing audio). (#7345)
* In ARIA menus on the web, the Escape key will now be passed through to the menu and no longer turn off focus mode unconditionally. (#3215)
* In the new Gmail web interface, when using quick navigation inside messages while reading them, the entire body of the message is no longer reported after the element to which you just navigated. (#8887)
* After updating NVDA, Browsers such as Firefox and google Chrome should no longer crash, and browse mode should continue to correctly reflect updates to any currently loaded documents. (#7641) 
* NVDA no longer reports clickable multiple times in a row when navigating clickable content in Browse Mode. (#7430)
* Gestures performed on baum Vario 40 braille displays will no longer fail to execute. (#8894)
* In Google Slides with Mozilla Firefox, NVDA no longer reports selected text on every control with focus. (#8964)

### Changes for Developers

* gui.nvdaControls now contains two classes to create accessible lists with check boxes. (#7325)
 * CustomCheckListBox is an accessible subclass of wx.CheckListBox.
 * AutoWidthColumnCheckListCtrl adds accessible check boxes to an AutoWidthColumnListCtrl, which itself is based on wx.ListCtrl.
* If you need to make a wx widget accessible which isn't already, it is possible to do so by using an instance of gui.accPropServer.IAccPropServer_impl. (#7491)
 * See the implementation of gui.nvdaControls.ListCtrlAccPropServer for more info.
* Updated configobj to 5.1.0dev commit 5b5de48a. (#4470)
* The config.post_configProfileSwitch action now takes the optional prevConf keyword argument, allowing handlers to take action based on differences between configuration before and after the profile switch. (#8758)

## 2018.3.2

This is a minor release to work around a crash in Google Chrome when navigating tweetts on [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

This is a minor release to fix a critical bug in NVDA which caused 32 bit versions of Mozilla Firefox to crash. (#8759)

## 2018.3

Highlights of this release include automatic detection of many Braille displays, support for new Windows 10 features including the Windows 10 Emoji input panel, and many other bug fixes.

### New Features

* NVDA will report grammar errors when appropriately exposed by web pages in Mozilla Firefox and Google Chrome. (#8280)
* Content marked as being either inserted or deleted in web pages is now reported in Google Chrome. (#8558)
* Added support for BrailleNote QT and Apex BT's scroll wheel when BrailleNote is used as a braille display with NVDA. (#5992, #5993)
* Added scripts for reporting elapsed and total time of current track in Foobar2000. (#6596)
* The Mac command key symbol (⌘) is now announced when reading text with any synthesizer. (#8366)
* Custom roles via the aria-roledescription attribute are now supported in all web browsers. (#8448)
* New braille tables: Czech 8 dot, Central Kurdish, Esperanto, Hungarian, Swedish 8 dot computer braille. (#8226, #8437)
* Support has been added to automatically detect braille displays in the background. (#1271)
 * ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille and HumanWare BrailleNote and Brailliant BI/B displays are currently supported.
 * You can enable this feature by selecting the automatic option from the list of braille displays in NVDA's braille display selection dialog.
 * Please consult the documentation for additional details.
* Added support for various modern input features introduced in recent Windows 10 releases. These include emoji panel (Fall Creators Update), dictation (Fall Creators Update), hardware keyboard input suggestions (April 2018 Update), and cloud clipboard paste (October 2018 Update). (#7273)
* Content marked as a block quote using ARIA (role blockquote) is now supported in Mozilla Firefox 63. (#8577)

### Changes

* The list of available languages in NVDA's General Settings is now sorted based on language names instead of ISO 639 codes. (#7284)
* Added default gestures for Alt+Shift+Tab and Windows+Tab with all supported Freedom Scientific braille displays. (#7387)
* For ALVA BC680 and protocol converter displays, it is now possible to assign different functions to the left and right smart pad, thumb and etouch keys. (#8230)
* For ALVA BC6 displays, the key combination sp2+sp3 will now announce the current date and time, whereas sp1+sp2 emulates the Windows key. (#8230)
* The user is asked once when NVDA starts if they are happy sending usage statistics to NV Access when checking for NVDA updates. (#8217)
* When checking for updates, if the user has agreed to allow sending usage statistics to NV Access, NVDA will now send the name of the current synth driver and braille display in use, to aide in better prioritization for future work on these drivers. (#8217)
* Updated liblouis braille translator to version 3.6.0. (#8365)
* Updated the path to the correct Russian eight-dots Braille table. (#8446)
* Updated eSpeak-ng to 1.49.3dev commit 910f4c2. (#8561)

### Bug Fixes

* Accessible labels for controls in Google Chrome are now more readily reported in browse mode when the label does not appear as content itself. (#4773)
* Notifications are now supported in Zoom. For example, this includes mute/unmute status, and incoming messages. (#7754)
* Switching braille context presentation when in browse mode no longer causes braille output to stop following browse mode cursor. (#7741)
* ALVA BC680 braille displays no longer intermittently fail to initialize. (#8106)
* By default, ALVA BC6 displays will no longer execute emulated system keyboard keys when pressing key combinations involving sp2+sp3 to trigger internal functionality. (#8230)
* Pressing sp2 on an ALVA BC6 display to emulate the alt key now works as advertised. (#8360)
* NVDA no longer announces redundant keyboard layout changes. (#7383, #8419)
* Mouse tracking is now much more accurate in Notepad and other plain text edit controls when in a document with more than 65535 characters. (#8397)
* NVDA will recognize more dialogs in Windows 10 and other modern applications. (#8405)
* On Windows 10 October 2018 Update and Server 2019 and above, NVDA no longer fails to track the system focus when an application freezes or floods the system with events. (#7345, #8535)
* Users are now informed when attempting to read or copy an empty status bar. (#7789)
* Fixed an issue where the "not checked" state on controls is not reported in speech if the control has previously been half checked. (#6946)
* In the list of languages in NVDA's General Settings, language name for Burmese is displayed correctly on Windows 7. (#8544)
* In Microsoft Edge, NVDA will announce notifications such as reading view availability and page load progress. (#8423)
* When navigating into a list on the web, NVDA will now report its label if the web author has provided one. (#7652)
* When manually assigning functions to gestures for a particular braille display, these gestures now always show up as being assigned to that display. Previously, they showed up as if they were assigned to the currently active display. (#8108)
* The 64-bit version of Media Player Classic is now supported. (#6066)
* Several improvements to braille support in Microsoft Word with UI Automation enabled:
 * Similar to other multiline text fields, When positioned at the start of a document in Braille, the display is now panned such that the first character of the document is at the start of the display. (#8406)
 * Reduced overly verbose focus presentation in both speech and braille when focusing a Word document. (#8407)
 * Cursor routing in braille now works correctly when in a list in a Word document. (#7971)
 * Newly inserted bullets/numbers in a Word document are correctly reported in both speech and braille. (#7970)
* In Windows 10 1803 and later, it is now possible to install add-ons if the "Use Unicode UTF-8 for worldwide language support" feature is enabled. (#8599)
* NVDA will no longer make iTunes 12.9 and newer completely unusable to interact with. (#8744)

### Changes for Developers

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

This release includes translation updates due to last-minute removal of a feature which caused problems.

## 2018.2

Highlights of this release include Support for tables in Kindle for PC, support for HumanWare BrailleNote Touch and BI14 Braille displays, Improvements to both Onecore and Sapi5 speech synthesizers, improvements in Microsoft Outlook and much more.

### New Features

* row and column span for table cells is now reported in speech and braille. (#2642)
* NVDA table navigation commands are now supported in Google Docs (with Braille mode enabled). (#7946)
* Added ability to read and navigate tables in Kindle for PC. (#7977)
* Support for HumanWare BrailleNote touch and Brailliant BI 14 braille displays via both USB and bluetooth. (#6524)
* In Windows 10 Fall Creators Update and later, NVDA can announce notifications from apps such as Calculator and Windows Store. (#7984)
* New braille translation tables: Lithuanian 8 dot, Ukrainian, Mongolian grade 2. (#7839)
* Added a script to report formatting information for the text under a specific braille cell. (#7106)
* When updating NVDA, it is now possible to postpone the installation of the update to a later moment. (#4263) 
* New languages: Mongolian, Swiss German.
* You can now toggle control, shift, alt, windows and NVDA from your braille keyboard and combine these modifiers with braille input (e.g. press control+s). (#7306) 
 * You can assign these new modifier toggles using the commands found under Emulated system keyboard keys in the Input gestures dialog.
* Restored support for Handy Tech Braillino and Modular (with old firmware) displays. (#8016)
* Date and time for supported Handy Tech devices (such as Active Braille and Active Star) will now automatically be synchronized by NVDA when out of sync more than five seconds. (#8016)
* An input gesture can be assigned to temporarily disable all configuration profile triggers. (#4935)

### Changes

* The status column in the addons manager has been changed to indicate if the addon is enabled or disabled rather than running or suspended. (#7929)
* Updated liblouis braille translator to 3.5.0. (#7839)
* The Lithuanian braille table has been renamed to Lithuanian 6 dot to avoid confusion with the new 8 dot table. (#7839)
* The French (Canada) grade 1 and grade 2 tables have been removed. Instead, the French (unified) 6 dot computer braille and Grade 2 tables will be used respectively. (#7839)
* The secondary routing buttons on Alva BC6, EuroBraille and Papenmeier braille displays now report formatting information for the text under the braille cell of that button. (#7106)
* Contracted braille input tables will automatically fall back to uncontracted mode in non-editable cases (i.e. controls where there is no cursor or in browse mode). (#7306)
* NVDA is now less verbose when an appointment or time slot in the Outlook calendar covers an entire day. (#7949)
* All of NVDA's Preferences can now be found in one settings dialog under NVDA Menu -> Preferences -> Settings, rather than scattered throughout many dialogs. (#577)
* The default speech synthesizer when running on Windows 10 is now oneCore speech rather than eSpeak. (#8176)

### Bug Fixes

* NVDA no longer fails to read focused controls in the Microsoft Account sign-in screen in Settings after entering an email address. (#7997)
* NVDA no longer fails to read the page when going back to a previous page in Microsoft Edge. (#7997)
* NVDA will no longer incorrectly announce the final character of a windows 10 sign-in PIN as the machine unlocks. (#7908)
* Labels of checkboxes and radio buttons in Chrome and Firefox are no longer reported twice when tabbing or using quick navigation in Browse mode. (#7960)
* aria-current with a value of false will be announced as "false" instead of "true". (#7892).
* Windows OneCore Voices no longer fails to load if the configured voice has been uninstalled. (#7553)
* Changing voices in the Windows OneCore Voices is now a lot faster. (#7999)
* Fixed malformed braille output for several braille tables, including capital signs in 8 dot contracted Danish braille. (#7526, #7693)
* NVDA can now report more bullet types in Microsoft Word. (#6778)
* Pressing the report formatting script no longer incorrectly moves the reviewPosition and therefore pressing it multiple times no longer gives different results. (#7869)
* Braille input no longer allows you to use contracted braille in cases where it is not supported (i.e. whole words will no longer be sent to the system outside text content and in browse mode). (#7306)
* Fixed connection stability issues for Handy Tech Easy Braille and Braille Wave displays. (#8016)
* On Windows 8 and later, NVDA will no longer announce "unknown" when opening quick link menu )Windows+X) and selecting items from this menu. (#8137)
* Model specific gestures to buttons on Hims displays are now working as advertised in the user guide. (#8096)
* NVDA will now try to correct system COM registration issues causing programs such as Firefox and Internet Explorer to become inaccessible and report "Unknown" by NVDA. (#2807)
* Worked around a bug in Task Manager causing NVDA to not allow users to access the contents of specific details about processes. (#8147)
* Newer Microsoft SAPI5 voices no longer lag at the end of speech, making it much more efficient to navigate with these voices. (#8174)
* NVDA no longer reports (LTR and RTL marks) in Braille or per-character speech when accessing the clock in recent versions of Windows. (#5729)
* Detection of scroll keys on Hims Smart Beetle displays is once more no longer unreliable. (#6086)
* In some text controls, particularly in Delphi applications, the information provided about editing and navigating is now much more reliable. (#636, #8102)
* In Windows 10 RS5, NVDA no longer reports extra redundant information when switching tasks with alt+tab. (#8258)

### Changes for developers

* The developer info for UIA objects now contains a list of the UIA patterns available. (#5712)
* App modules can now force certain windows to always use UIA by implementing the isGoodUIAWindow method. (#7961)
* The hidden boolean flag "outputPass1Only" in the braille section of the configuration has again been removed. Liblouis no longer supports pass 1 only output. (#7839)

## 2018.1.1

This is a special release of NVDA which addresses   a bug in the Onecore Windows Speech synthesizer driver, which was causing it to speak with a higher pitch and speed in Windows 10 Redstone 4 (1803). (#8082)  

## 2018.1

Highlights of this release include  support for charts in Microsoft word and PowerPoint, support for new braille displays including Eurobraille and the Optelec protocol converter, improved support for Hims and Optelec braille displays, performance improvements for Mozilla Firefox 58 and higher, and much more.

### New Features

* It is now possible to interact with charts in Microsoft Word and Microsoft PowerPoint, similar to the existing support for charts in Microsoft Excel. (#7046)
 * In Microsoft Word:  When in browse mode, cursor to an embedded chart and press enter to interact with it.
 * In Microsoft PowerPoint when editing a slide: tab to a chart object, and press enter or space to interact with the chart.
 * To stop interacting with a chart, press escape.
* New language: Kyrgyz.
* Added support for VitalSource Bookshelf. (#7155)
* Added support for the Optelec protocol converter, a device that allows one to use Braille Voyager and Satellite displays using the ALVA BC6 communication protocol. (#6731)
* It is now possible to use braille input with an ALVA 640 Comfort braille display. (#7733) 
 * NVDA's braille input functionality can be used with these as well as other BC6 displays with firmware 3.0.0 and above.
* Early support for Google Sheets with Braille mode enabled. (#7935)
* Support for Eurobraille Esys, Esytime and Iris braille displays. (#7488)

### Changes

* The HIMS Braille Sense/Braille EDGE/Smart Beetle and Hims Sync Braille display drivers have been replaced by one driver. The new driver will automatically be activated for former syncBraille driver users. (#7459) 
 * Some keys , notably scroll keys, have been reassigned to follow the conventions used by Hims products. Consult the user guide for more details.
* When typing with the on-screen keyboard via touch interaction, by default you now need to double tap each key the same way you would activate any other control. (#7309)
 * To use the existing "touch typing" mode where simply lifting your finger off the key is enough to activate it, Enable this option in the new Touch Interaction settings dialog found in the Preferences menu.
* It is no longer necessary to explicitly tether braille to focus or review, as this will happen automatically by default. (#2385) 
 * Note that automatic tethering to review will only occur when using a review cursor or object navigation command. Scrolling will not activate this new behavior.

### Bug Fixes

* Browseable messages such as showing current formatting when pressing NVDA+f twice quickly no longer fails when NVDA is installed on a path with non-ASCII characters. (#7474)
* Focus is now once again restored correctly when returning to Spotify from another application. (#7689)
* In Windows 10 Fall Creaters Update, NVDA no longer fails to update when Controlled Folder Access is enabled from Windows Defender Security Center. (#7696)
* Detection of scroll keys on Hims Smart Beetle displays is no longer unreliable. (#6086)
* A slight performance improvement when rendering large amounts of content in Mozilla Firefox 58 and later. (#7719)
* In Microsoft Outlook, reading emails containing tables no longer causes errors. (#6827)
* Braille display gestures that emulate system keyboard key modifiers can now also be combined with other emulated system keyboard keys if one or more of the involved gestures are model specific. (#7783)
* In Mozilla Firefox, browse mode now works correctly in pop-ups created by extensions such as LastPass and bitwarden. (#7809)
* NVDA no longer sometimes freezes on every focus change if Firefox or Chrome have stopped responding such as due to a freeze or crash. (#7818)
* In twitter clients such as Chicken Nugget, NVDA will no longer ignore the last 20 characters of 280 character tweets when reading them. (#7828)
* NVDA now uses the correct language when announcing symbols when text is selected. (#7687)
* In recent versions of Office 365, it is again possible to navigate Excel charts using the arrow keys. (#7046)
* In speech and braille output, control states will now always be reported in the same order, regardless whether they are positive or negative. (#7076)
* In apps such as Windows 10 Mail, NVDA will no longer fail to announce deleted characters when pressing backspace. (#7456)
* All keys on the Hims Braille Sense Polaris displays are now working as expected. (#7865)
* NVDA no longer fails to start on Windows 7 complaining about an internal api-ms dll, when a particular version of the Visual Studio 2017 redistributables have been installed by another application. (#7975)

### Changes for developers

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

Highlights of this release include many  fixes and enhancements to web support including browse mode for web dialogs by default, better reporting of field group labels in browse mode, support for new Windows 10 technologies such as Windows Defender Application Guard and Windows 10 on ARM64, and automatic reporting of screen orientation and battery status.
Please note that this version of NVDA no longer supports Windows XP or Windows Vista. The minimum requirement for NVDA is now windows 7 with Service Pack 1.

### New Features

* In browse mode, it is now possible to skip past/to the start of landmarks using the skip to end/beginning of container commands (comma/shift+comma). (#5482)
* In Firefox, Chrome and Internet Explorer, quick navigation to edit fields and form fields now includes editable rich text content (I.e. contentEditable). (#5534)
* In web browsers, the Elements List can now list form fields and buttons. (#588)
* Initial support for Windows 10 on ARM64. (#7508)
* Early support for reading and interactive navigation of mathematical content for Kindle books with accessible math. (#7536)
* Added support for Azardi e-book reader. (#5848)
* Version information for add-ons is now reported when being updated. (#5324)
* Added new command line parameters to create a portable copy of NVDA. (#6329)
* Support for Microsoft Edge running within Windows Defender Application Guard in Windows 10 Fall Creators Update. (#7600)
* If running on a laptop or tablet, NVDA will now report when a charger is connected/disconnected, and when the screen orientation changes. (#4574, #4612)
* New language: Macedonian.
* New braille translation tables: Croatian grade 1, Vietnamese grade 1. (#7518, #7565)
* Support for the Actilino braille display from Handy Tech has been added. (#7590)
* Braille input for Handy Tech braille displays is now supported. (#7590)

### Changes

* The minimum supported Operating System for NVDA is now Windows 7 Service Pack 1, or Windows Server 2008 R2 Service Pack 1. (#7546)
* Web dialogs in Firefox and Chrome web browsers now automatically use browse Mode, unless inside of a web application. (#4493)
* In browse mode, tabbing and moving with quick navigation commands no longer announces jumping out of containers such as lists and tables, which makes navigating more efficient. (#2591)
* In Browse mode for Firefox and Chrome, the name of form field groups are now announced when moving into them with quick navigation or when tabbing. (#3321)
* In browse mode, the quick navigation command for embedded objects (o and shift+o) now includes audio and video elements as well as elements with the aria roles application and dialog. (#7239)
* Espeak-ng has been updated to 1.49.2, resolving some issues with producing release builds. (#7385, #7583)
* On the third activation of the 'read status bar' command, its contents is copied to the clipboard. (#1785)
* When assigning gestures to keys on a Baum display, you can limit them to the model of the braille display in use (e.g. VarioUltra or Pronto). (#7517)
* The hotkey for the filter field in the elements list in browse mode has changed from alt+f to alt+e. (#7569)
* An unbound command has been added for browse mode to toggle the inclusion of layout tables on the fly. You can find this command in the Browse mode category of the Input Gestures dialog. (#7634)
* Upgraded liblouis braille translator to 3.3.0. (#7565)
* The hotkey for the regular expression radio button in the dictionary dialog has changed from alt+r to alt+e. (#6782)
* Voice dictionary files are now versioned and have been moved to the 'speechDicts/voiceDicts.v1' directory. (#7592)
* Versioned files (user configuration, voice dictionaries) modifications are no longer saved when NVDA is run from the launcher. (#7688)
* The Braillino, Bookworm and Modular (with old firmware) braille displays from Handy Tech are no longer supported out of the box. Install the Handy Tech Universal Driver and NVDA add-on to use these displays. (#7590)

### Bug Fixes

* Links are now indicated in braille in applications such as Microsoft Word. (#6780)
* NVDA no longer becomes noticeably slower when many tabs are open in either Firefox or Chrome web browsers. (#3138)
* Cursor routing for the MDV Lilli Braille display no longer incorrectly moves one braille cell ahead of where it should be. (#7469)
* In Internet Explorer and other MSHTML documents, the HTML5 required attribute is now supported to indicate the required state of a form field. (#7321)
* Braille displays are now updated when typing Arabic characters in a left-aligned WordPad document. (#511)
* Accessible labels for controls in Mozilla Firefox are now more readily reported in browse mode when the label does not appear as content itself. (#4773)
* On windows 10 Creaters Update, NVDA can again access Firefox after a restart of NVDA. (#7269)
* When restarting NVDA with Mozilla Firefox in focus, browse mode will again be available, though you may need to alt+tab away and back again. (#5758)
* It is now possible to access math content in Google Chrome on a system with out Mozilla Firefox installed. (#7308)
* The Operating System and other applications should be more stable directly after installing NVDA before rebooting, as compaired with installs of previous NVDA versions. (#7563)
* When using a content recognition command (e.g. NVDA+r), NVDA now reports an error message instead of nothing if the navigator object has disappeared. (#7567)
* Backward scrolling functionality has been fixed for Freedom Scientific braille displays containing a left bumper bar. (#7713)

### Changes for Developers

* "scons tests" now checks that translatable strings have translator comments. You can also run this alone with "scons checkPot". (#7492)
* There is now a new extensionPoints module which provides a generic framework to enable code extensibility at specific points in the code. This allows interested parties to register to be notified when some action occurs (extensionPoints.Action), to modify a specific kind of data (extensionPoints.Filter) or to participate in deciding whether something will be done (extensionPoints.Decider). (#3393)
* You can now register to be notified about configuration profile switches via the config.configProfileSwitched Action. (#3393)
* Braille display gestures that emulate system keyboard key modifiers (such as control and alt) can now be combined with other emulated system keyboard keys without explicit definition. (#6213) 
 * For example, if you have a key on your display bound to the alt key and another display key to downArrow, combining these keys will result in the emulation of alt+downArrow.
* The braille.BrailleDisplayGesture class now has an extra model property. If provided, pressing a key will generate an additional, model specific gesture identifier. This allows a user to bind gestures limited to a specific braille display model. 
 * See the baum driver as an example for this new functionality.
* NVDA is now compiled with Visual Studio 2017 and the Windows 10 SDK. (#7568)

## 2017.3

Highlights of this release include input of contracted braille, support for new Windows OneCore voices available on Windows 10, in-built support for Windows 10 OCR, and many significant improvements regarding Braille and the web.

### New Features

* A Braille setting has been added to "show messages indefinitely". (#6669)
* In Microsoft Outlook message lists, NVDA now reports if a message is flagged. (#6374)
* In Microsoft PowerPoint, the exact type of a shape is now reported when editing a slide (such as triangle, circle, video or arrow), rather than just "shape". (#7111)
* Mathematical content (provided as MathML) is now supported in Google Chrome. (#7184)
* NVDA can now speak using the new Windows OneCore voices (also known as Microsoft Mobile voices) included in Windows 10. You access these by selecting Windows OneCore voices in NVDA's Synthesizer dialog. (#6159)
* NVDA user configuration files can now be stored in the user's local application data folder. This is enabled via a setting in the registry. See "System Wide Parameters" in the User Guide for more details. (#6812)
* In web browsers, NVDA now reports placeholder values for fields (specifically, aria-placeholder is now supported). (#7004)
* In Browse mode for Microsoft Word, it is now possible to navigate to spelling  errors using quick navigation (w and shift+w). (#6942)
* Added support for the Date picker control found in Microsoft Outlook Appointment dialogs. (#7217)
* The currently selected suggestion is now reported in Windows 10 Mail to/cc fields and the Windows 10 Settings search field. (#6241)
* A sound is now playd to indicate the  appearance of suggestions in certain search fields in Windows 10 (E.g. start screen, settings search, Windows 10 mail to/cc fields). (#6241)
* NVDA now automatically reports notifications in Skype for Business Desktop, such as when someone starts a conversation with you. (#7281)
* NVDA now automatically reports incoming chat messages while in a Skype for Business conversation. (#7286)
* NVDA now automatically reports notifications in Microsoft Edge, such as when a download starts. (#7281)
* You can now type in both contracted and uncontracted braille on a braille display with a braille keyboard. See the Braille Input section of the User Guide for details. (#2439)
* You can now enter Unicode braille characters from the braille keyboard on a braille display by selecting Unicode braille as the input table in Braille Settings. (#6449)
* Added support for the SuperBraille braille display used in Taiwan. (#7352)
* New braille translation tables: Danish 8 dot computer braille, Lithuanian, Persian 8 dot computer braille, Persian grade 1, Slovenian 8 dot computer braille. (#6188, #6550, #6773, #7367)
* Improved English (U.S.) 8 dot computer braille table, including support for bullets, the euro sign and accented letters. (#6836)
* NVDA can now use the OCR functionality included in Windows 10 to recognize the text of images or inaccessible applications. (#7361)
 * The language can be set from the new Windows 10 OCR dialog in NVDA Preferences.
 * To recognize the content of the current navigator object, press NVDA+r.
 * See the Content Recognition section of the User Guide for further details.
* You can now choose what context information is shown on a braille display when an object gets focus using the new "Focus context presentation" setting in the Braille Settings dialog. (#217)
 * For example, the "Fill display for context changes" and "Only when scrolling back" options can make working with lists and menus more efficient, since the items won't continually change their position on the display.
 * See the section on the "Focus context presentation" setting in the User Guide for further details and examples.
* In Firefox and Chrome, NVDA now supports complex dynamic grids such as spreadsheets where only some of the content might be loaded or displayed (specifically, the aria-rowcount, aria-colcount, aria-rowindex and aria-colindex attributes introduced in ARIA 1.1). (#7410)

### Changes

* An unbound command has been added to restart NVDA on demand. You can find it in the Miscelaneous category of the Input Gestures dialog. (#6396)
* The keyboard layout can now be set from the NVDA Welcome dialog. (#6863)
* Many more control types and states have been abbreviated for braille. Landmarks have also been abbreviated. Please see "Control Type, State and Landmark Abbreviations" under Braille in the User Guide for a complete list. (#7188, #3975)
* Updated eSpeak NG to 1.49.1. (#7280)
* The output and input table lists in the Braille Settings dialog are now sorted alphabetically. (#6113)
* Updated liblouis braille translator to 3.2.0. (#6935)
* The default braille table is now Unified English Braille Code grade 1. (#6952)
* By default, NVDA now only shows the parts of the context information that have changed on a braille display when an object gets focus. (#217)
 * Previously, it always showed as much context information as possible, regardless of whether you have seen the same context information before.
 * You can revert to the old behaviour by changing the new "Focus context presentation" setting in the Braille Settings dialog to "Always fill display".
* When using Braille, the cursor can be configured to be a different shape when tethered to focus or review. (#7122)
* The NVDA logo has been updated. The updated NVDA logo is a stylised blend of the letters NVDA in white, on a solid purple background. This ensures it will be visible on any colour background, and uses the purple from the NV Access logo. (#7446)

### Bug Fixes

* Editable div elements in Chrome no longer have their label reported as their value while in browse mode. (#7153)
* Pressing end while in browse mode for an empty Microsoft Word document no longer causes a runtime error. (#7009)
* Browse mode is now correctly   supported in Microsoft Edge where a document has been given a specific ARIA role of document. (#6998)
* In browse mode, you can now select or unselect to the end of the line using shift+end even when the caret is on the last character of the line. (#7157)
* If a dialog contains a progress bar, the dialog text is now updated in braille when the progress bar changes. This means, for example, that the remaining time can now be read in NVDA's "Downloading Update" dialog. (#6862)
* NVDA will now announce selection changes for certain Windows 10 combo boxes such as AutoPlay in Settings. (#6337).
* Pointless information is no longer announced when entering Meeting / Appointment creation dialogs in Microsoft Outlook. (#7216)
* Beeps for indeterminate progress bar dialogs such as the update checker only when progress bar output is configured to include beeps. (#6759)
* In Microsoft Excel 2003 and 2007, cells are again reported when arrowing around a worksheet. (#7243)
* In Windows 10 Creators Update and later, browse mode is again automatically enabled when reading emails in Windows 10 Mail. (#7289)
* On most braille displays with a braille keyboard, dot 7 now erases the last entered braille cell or character, and dot 8 presses the enter key. (#6054)
* In editable text, when moving the caret (e.g. with the cursor keys or backspace), NVDA's spoken feedback is now more accurate in many cases, particularly in Chrome and terminal applications. (#6424)
* The content of the Signature Editor in Microsoft Outlook 2016 can now be read. (#7253)
* In Java Swing applications, NVDA no longer sometimes causes the application to crash when navigating tables. (#6992)
* In Windows 10 Creators Update, NVDA will no longer announce toast notifications multiple times. (#7128)
* In The start menu in Windows 10, pressing Enter to close the start menu after a search no longer causes NVDA to announce search text. (#7370)
* Performing quick navigation to headings in Microsoft Edge is now significantly faster. (#7343)
* In Microsoft Edge, navigating in browse mode no longer skips large parts of certain web pages such as the Wordpress 2015 theme. (#7143)
* In Microsoft Edge, landmarks are correctly localized in languages other than English. (#7328)
* Braille now correctly follows the selection when selecting text beyond the width of the display. For example, if you select multiple lines with shift+downArrow, braille now shows the last line you selected. (#5770)
* In Firefox, NVDA no longer spuriously reports "section" several times when opening details for a tweet on twitter.com. (#5741)
* Table navigation commands are no longer available for layout tables in Browse Mode unless reporting of layout tables is enabled. (#7382)
* In Firefox and Chrome, Browse Mode table navigation commands now skip over hidden table cells. (#6652, #5655)

### Changes for Developers

* Timestamps in the log now include milliseconds. (#7163)
* NVDA must now be built with Visual Studio Community 2015. Visual Studio Express is no longer supported. (#7110)
 * The Windows 10 Tools and SDK are now also required, which can be enabled when installing Visual Studio.
 * See the Installed Dependencies section of the readme for additional details.
* Support for content recognizers such as OCR and image description tools can be easily implemented using the new contentRecog package. (#7361)
* The Python json package is now included in NVDA binary builds. (#3050)

## 2017.2

Highlights of this release include full support for audio ducking in the Windows 10 Creators Update; fixes for several selection issues in browse mode, including problems with select all; significant improvements in Microsoft Edge support; and improvements on the web such as indication of elements marked as current (using aria-current).

### New Features

* Cell border information can now be reported in Microsoft Excel by using NVDA+f. (#3044)
* In web browsers, NVDA now indicates when an element has been marked as current (specifically, using the aria-current attribute). (#6358)
* Automatic language switching is now supported in Microsoft Edge. (#6852)
* Added support for Windows Calculator on Windows 10 Enterprise LTSB (Long-Term Servicing Branch) and Server. (#6914)
* Performing the read current line command three times quickly spells the line with character descriptions. (#6893)
* New language: Burmese.
* Unicode up and down arrows and fraction symbols are now spoken appropriately. (#3805)

### Changes

* When navigating with simple review  in applications using UI Automation, more extraneous objects are now ignored, making navigation easier. (#6948, #6950)

### Bug Fixes

* Web page menu items can now be activated while in browse mode. (#6735)
* Pressing escape while the configuration profile "Confirm Deletion" dialog is active now dismisses the dialog. (#6851)
* Fixed some crashes in Mozilla Firefox and other Gecko applications where the multi-process feature is enabled. (#6885)
* Reporting of background color in screen review is now more accurate when  text was drawn with a transparent background. (#6467)
* Improved support for control descriptions provided on web pages in Internet Explorer 11 (specifically, support for aria-describedby within iframes and when multiple IDs are provided). (#5784)
* In the Windows 10 Creators Update, NVDA's audio ducking again works as in previous Windows releases; i.e. Duck with speech and sounds, always duck and no ducking are all available. (#6933)
* NVDA will no longer fail to navigate to or report certain (UIA) controls where a keyboard shortcut is not defined. (#6779)
* Two empty spaces are no longer added in keyboard shortcut information for certain (UIA) controls. (#6790)
* Certain combinations of keys on HIMS displays (e.g. space+dot4) no longer fail intermittently. (#3157)
* Fixed an issue when opening a serial port on systems using certain languages other than English which caused connecting to braille displays to fail in some cases. (#6845)
* Reduced the chance of the configuration file being corrupted when Windows shuts down. Configuration files are now written to a temporary file before replacing the actual configuration file. (#3165)
* When performing the read current line command twice quickly to spell the line, the appropriate language is now used for the spelled characters. (#6726)
* Navigating by line in Microsoft Edge is now up to three times faster in the Windows 10 Creators Update. (#6994)
* NVDA no longer announces "Web Runtime grouping" when focusing Microsoft Edge documents in the Windows 10 Creators Update. (#6948)
* All existing versions of SecureCRT are now supported. (#6302)
* Adobe Acrobat Reader no longer crashes in certain PDF documents (specifically, those containing empty ActualText attributes). (#7021, #7034)
* In browse mode in Microsoft Edge, interactive tables (ARIA grids) are no longer skipped when navigating to tables with t and shift+t. (#6977)
* In browse mode, pressing shift+home after selecting forward now unselects to the beginning of the line as expected. (#5746)
* In browse mode, select all (control+a) no longer fails to select all text if the caret is not at the start of the text. (#6909)
* Fixed some other rare selection problems in browse mode. (#7131)

### Changes for Developers

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

Highlights of this release include reporting of sections and text columns in Microsoft Word; Support for reading, navigating and annotating books in Kindle for PC; and improved support for Microsoft Edge.

### New Features

* In Microsoft Word, the types of section breaks and section numbers can now be reported. This is enabled with the "Report page numbers" option in the Document Formatting dialog. (#5946)
* In Microsoft Word, text columns can now be reported. This is enabled with the "Report page numbers" option in the document formatting dialog. (#5946)
* Automatic language switching is now supported in WordPad. (#6555)
* The NVDA find command (NVDA+control+f) is now supported in browse mode in Microsoft Edge. (#6580)
* Quick navigation for buttons in browse mode (b and shift+b) is now supported in Microsoft Edge. (#6577)
* When copying a sheet in Microsoft Excel, column and row headers are remembered. (#6628)
* Support for reading and navigating books in Kindle for PC version 1.19, including access to links, footnotes, graphics, highlighted text and user notes. Please see the Kindle for PC section of the NVDA User Guide for further information. (#6247, #6638)
* Browse mode table navigation is now supported in Microsoft Edge. (#6594)
* In Microsoft Excel, the report review cursor location command (desktop: NVDA+numpadDelete, laptop: NVDA+delete) now reports the name of the worksheet and the cell location. (#6613)
* Added an option to the exit dialog to restart with debug level logging. (#6689)

### Changes

* The minimum braille cursor blink rate is now 200 ms. If this was previously set lower, it will be increased to 200 ms. (#6470)
* A check box has been added to the braille settings dialog to allow enabling/disabling braille cursor blinking. Previously a value of zero was used to achieve this. (#6470)
* Updated eSpeak NG (commit e095f008, 10 January 2017). (#6717)
* Due to changes In the Windows 10 Creators Update, the "Always duck" mode is no longer available in NVDA's Audio ducking settings. It is still available on older windows 10 releases. (#6684)
* Due to changes in the  Windows 10 Creators Update, the "Duck when outputting speech and sounds" mode can no longer ensure audio has ducked fully before starting to speak, nor will it keep audio ducked long enough after speaking to stop rappid bouncing in volume. These changes do not   affect older windows 10 releases. (#6684)

### Bug Fixes

* Fixed freeze in Microsoft Word when moving by paragraph through a large document while in browse mode. (#6368)
* Tables in Microsoft Word that have been copied from Microsoft Excel are no longer treeted as layout tables and therefore are no longer ignored. (#5927)
* When trying to type in Microsoft Excel while in protected view, NVDA now makes a sound rather than speaking characters that were not actually typed. (#6570)
* Pressing escape in Microsoft Excel no longer incorrectly switches to browse mode, unless the user has previously switched to browse mode explicitly with NVDA+space and then entered focus mode by pressing enter on a form field. (#6569) 
* NVDA no longer freezes in Microsoft Excel spreadsheets where an entire row or column is merged. (#6216)
* Reporting of cropped/overflowed text in Microsoft Excel cells should now be more accurate. (#6472)
* NVDA now reports when a check box is read-only. (#6563)
* The NVDA launcher will no longer show a warning dialog when it can't play the logo sound due to no audio device being available. (#6289)
* Controls in the Microsoft Excel Ribbon that are unavailable are now reported as such. (#6430)
* NVDA will no longer announce "pane" when minimizing windows. (#6671)
* Typed characters are now spoken in Universal Windows Platform (UWP) apps (including Microsoft Edge) in the Windows 10 Creators Update. (#6017)
* Mouse tracking now works across all screens on computers with multiple monitors. (#6598)
* NVDA no longer becomes unusable after exiting Windows Media Player while focused on a slider control. (#5467)

### Changes for Developers

* Profiles and configuration files are now automatically upgraded to meet the requirements of schema modifications. If there is an error during upgrade, a notification is shown, the configuration is reset and the old configuration file is available in the NVDA log at 'Info' level. (#6470)

## 2016.4

Highlights of this release include improved support for Microsoft Edge; browse mode in the Windows 10 Mail app; and significant improvements to NVDA's dialogs.

### New Features

* NVDA can now indicate line indentation using tones. This can be configured using the "Line indentation reporting" combo box in NVDA's Document Formatting preferences dialog. (#5906)
* Support for the Orbit Reader 20 braille display. (#6007)
* An option to open the speech viewer window on startup has been added. This can be enabled via a check box in the speech viewer window. (#5050)
* When re-opening the speech viewer window, the location and dimensions will now be restored. (#5050)
* Cross-reference fields in Microsoft Word are now treated like hyperlinks. They are reported as links and can be activated. (#6102)
* Support for the Baum SuperVario2, Baum Vario 340 and HumanWare Brailliant2 braille displays. (#6116)
* Initial support for the Anniversary update of Microsoft Edge. (#6271)
* Browse mode is now used when reading emails in the Windows 10 mail app. (#6271)
* New language: Lithuanian.

### Changes

* Updated liblouis braille translator to 3.0.0. This includes significant enhancements to Unified English Braille. (#6109, #4194, #6220, #6140)
* In the Add-ons Manager, the Disable add-on and Enable add-on buttons now have keyboard shortcuts (alt+d and alt+e, respectively). (#6388)
* Various padding and alignment issues in NVDA's dialogs have been resolved. (#6317, #5548, #6342, #6343, #6349)
* The document formatting dialog has been adjusted so that the contents scrolls. (#6348)
* Adjusted the layout of the Symbol Pronunciation dialog so the full width of the dialog is used for the symbols list. (#6101)
* In browse mode in web browsers, the edit field (e and shift+e) and form field (f and shift+f) single letter navigation commands can now be used to move to read-only edit fields. (#4164)
* In NVDA's Document Formatting settings, "Announce formatting changes after the cursor" has been renamed to "Report formatting changes after the cursor", as it affects braille as well as speech. (#6336)
* Adjusted the appearance of the NVDA "Welcome dialog". (#6350)
* NVDA dialog boxes now have their "ok" and "cancel" buttons aligned to the right of the dialog. (#6333)
* Spin Controls are now used for numeric input fields such as the "Capital pitch change percentage" setting  in the Voice Settings dialog. You can enter the desired value or use the up and down arrow keys to adjust the value. (#6099)
* The way IFrames (documents embedded within documents) are reported has been made more consistent across web browsers. IFrames are now reported as "frame" in Firefox. (#6047)

### Bug Fixes

* Fixed a rare error when exiting NVDA while the speech viewer is open. (#5050)
* Image maps now render as expected in browse mode in Mozilla Firefox. (#6051)
* While in the dictionary dialog, pressing the enter key now saves any changes you have made and closes the dialog. Previously, pressing enter did nothing. (#6206)
* Messages are now displayed in braille when changing input modes for an input method (native input/alphanumeric, full shaped/half shaped, etc.). (#5892, #5893)
* When disabling and then immediately re-enabling an add-on or vice versa, the add-on status now correctly reverts to what it was previously. (#6299)
* When using Microsoft Word, page number fields in headers can now be read. (#6004)
* The mouse can now be used to move focus between the symbol list and the edit fields in the symbol pronunciation dialog. (#6312)
* In browse mode in Microsoft Word, Fixed an issue that stops the elements list from appearing when a document contains an invalid hyperlink. (#5886)
* After being closed via the task bar or the alt+F4 shortcut, the speech viewer check box in the NVDA menu will now reflect the actual visibility of the window. (#6340)
* The reload plugins command no longer causes problems for triggered configuration profiles, new documents in web browsers and screen review. (#2892, #5380)
* In the list of languages in NVDA's General Settings dialog, languages such as Aragonese are now displayed correctly on Windows 10. (#6259)
* Emulated system keyboard keys (e.g. a button on a braille display which emulates pressing the tab key) are now presented in the configured NVDA language in input help and the Input Gestures dialog. Previously, they were always presented in English. (#6212)
* Changing the NVDA language (from the General Settings dialog) now has no effect until NVDA is restarted. (#4561)
* It is no longer possible to leave the Pattern field blank for a new speech dictionary entry. (#6412)
* Fixed a rare issue when scanning for serial ports on some systems which made some braille display drivers unusable. (#6462)
* In Microsoft Word, Numbered bullets in table cells are now read  when moving by cell. (#6446)
* It is now possible to assign gestures to commands for the Handy Tech braille display driver in the NVDA Input Gestures dialog. (#6461)
* In Microsoft Excel, pressing enter or numpadEnter when navigating a spreadsheet now correctly reports navigation to the next row. (#6500)
* iTunes no longer intermittently freezes forever when using browse mode for the iTunes Store, Apple Music, etc. (#6502)
* Fixed crashes in 64 bit Mozilla and Chrome-based applications. (#6497)
* In Firefox with multi-process enabled, browse mode and editable text fields now function correctly. (#6380)

### Changes for Developers

* It is now possible to provide app modules for executables containing a dot (.) in their names. Dots are replaced with underscores (_). (#5323)
* The new gui.guiHelper module includes utilities to simplify the creation of wxPython GUIs, including automatic management of spacing. This facilitates better visual appearance and consistency, as well as easing creation of new GUIs for blind developers. (#6287)

## 2016.3

Highlights of this release include the ability to disable individual add-ons; support for form fields in Microsoft Excel; significant improvements to reporting of colors; fixes and improvements related to several braille displays; and fixes and improvements to support for Microsoft Word.

### New Features

* Browse mode can now be used to read PDF documents in Microsoft Edge in the Windows 10 Anniversary Update. (#5740)
* Strikethrough and double-strikethrough are now reported if appropriate in Microsoft Word. (#5800)
* In Microsoft Word, the title of a table is now reported if one has been provided. If there is a description, it can be accessed using the open long description command (NVDA+d) in browse mode. (#5943)
* In Microsoft Word, NVDA now reports position information when moving paragraphs (alt+shift+downArrow and alt+shift+upArrow). (#5945)
* In Microsoft Word, line spacing is now reported via NVDA's report formatting command, when changing it with various Microsoft word shortcut keys, and when moving to text with different line spacing if Report Line Spacing is turned on in NVDA's Document Formatting Settings. (#2961)
* In Internet Explorer, HTML5 structural elements are now recognised. (#5591)
* Reporting of comments (such as in Microsoft Word) can now be disabled via a Report Comments checkbox in NVDA's Document Formatting settings dialog. (#5108)
* It is now possible to disable individual add-ons in the Add-ons Manager. (#3090)
* Additional key assignments have been added for ALVA BC640/680 series braille displays. (#5206)
* There is now a command to move the braille display to the current focus. Currently, only the ALVA BC640/680 series has a key assigned to this command, but it can be assigned manually for other displays in the Input Gestures dialog if desired. (#5250)
* In Microsoft Excel, you can now interact with form fields. You move to form fields using the Elements List or single letter navigation in browse mode. (#4953)
* You can now assign an input gesture to toggle simple review mode using the Input Gestures dialog. (#6173)

### Changes

* NVDA now reports colors using a basic well-understood set of 9 color hues and 3 shades, with brightness and paleness variations. This is rather than using more subjective and less understood color names. (#6029)
* The existing NVDA+F9 then NVDA+F10 behavior has been modified to select text on the first press of F10. When F10 is pressed twice (in quick succession) the text is copied to the clipboard. (#4636)
* Updated eSpeak NG to version Master 11b1a7b (22 June 2016). (#6037)

### Bug Fixes

* In browse mode in Microsoft Word, copying to the clipboard now preserves formatting. (#5956)
* In Microsoft Word, NVDA now reports appropriately when using Word's own table navigation commands (alt+home, alt+end, alt+pageUp and alt+pageDown) and table selection commands (shift added to the navigation commands). (#5961)
* In Microsoft Word dialog boxes, NVDA's object navigation has been greatly improved. (#6036)
* In some applications such as Visual Studio 2015, shortcut keys (e.g. control+c for Copy) are now reported as expected. (#6021)
* Fixed a rare issue when scanning for serial ports on some systems which made some braille display drivers unusable. (#6015)
* Reporting colors in Microsoft Word is now more accurate as changes in Microsoft Office Themes are now taken into account. (#5997)
* Browse mode for Microsoft Edge and support for Start Menu search suggestions is again available on Windows 10 builds after April 2016. (#5955)
* In Microsoft Word, automatic table header reading works better when dealing with merged cells. (#5926)
* In the Windows 10 Mail app, NVDA no longer fails to read the content of messages. (#5635) 
* When speak command keys is on, lock keys such as caps lock are no longer announced twice. (#5490)
* Windows User Account Control dialogs are again read correctly in the Windows 10 Anniversary update. (#5942)
* In the Web Conference Plugin (such as used on out-of-sight.net) NVDA no longer beeps and speaks progress bar updates related to microphone input. (#5888)
* Performing a Find Next or Find Previous command in Browse Mode will now correctly do a  case sensitive search if the original Find was case sensitive. (#5522)
* When editing dictionary entries, feedback is now given for invalid regular expressions. NVDA no longer crashes if a dictionary file contains an invalid regular expression. (#4834)
* If NVDA is unable to communicate with a braille display (e.g. because it has been disconnected), it will automatically disable use of the display. (#1555)
* Slightly improved performance of filtering in the Browse Mode Elements List in some cases. (#6126)
* In Microsoft Excel, the background pattern names reported by NVDA now match those used by Excel. (#6092)
* Improved support for the Windows 10 logon screen, including announcement of alerts and activating of the password field with touch. (#6010)
* NVDA now correctly detects the secondary routing buttons on ALVA BC640/680 series braille displays. (#5206)
* NVDA can again report Windows Toast notifications in recent builds of Windows 10. (#6096)
* NVDA no longer occasionally stops recognising key presses on Baum compatible and HumanWare Brailliant B braille displays. (#6035)
* If reporting of line numbers is enabled in NVDA's Document Formatting preferences, line numbers are now shown on a braille display. (#5941)
* When speech mode is off, reporting objects (such as pressing NVDA+tab to report the focus) now appears in the Speech Viewer as expected. (#6049)
* In the Outlook 2016 message list,  associated draft information is no longer reported. (#6219)
* In Google Chrome and Chrome-based browsers in a language other than English, browse mode no longer fails to work in many documents. (#6249)

### Changes for Developers

* Logging information directly from a property no longer results in the property  being called recursively over and over again. (#6122)

## 2016.2.1

This release fixes crashes in Microsoft Word:

* NVDA no longer causes Microsoft Word to crash immediately after it starts in Windows XP. (#6033)
* Removed reporting of grammar errors, as this causes crashes in Microsoft Word. (#5954, #5877)

## 2016.2

Highlights of this release include the ability to indicate spelling errors while typing; support for reporting grammar errors in Microsoft Word; and improvements and fixes to Microsoft Office support.

### New Features

* In browse mode in Internet Explorer and other MSHTML controls, using first letter navigation to move by annotation (a and shift+a) now moves to inserted and deleted text. (#5691)
* In Microsoft Excel, NVDA now reports the level of a group of cells, as well as whether it is collapsed or expanded. (#5690)
* Pressing the Report text formatting command (NVDA+f) twice presents the information in browse mode so it can be reviewed. (#4908)
* In Microsoft Excel 2010 and later, cell shading and gradient fill is now reported. Automatic reporting is controlled by the Report colors option in NVDA's Document Formatting preferences. (#3683)
* New braille translation table: Koine Greek. (#5393)
* In the Log Viewer, you can now save the log using the shortcut key control+s. (#4532)
* If reporting of spelling errors is enabled and supported in the focused control, NVDA will play a sound to alert you of a spelling error made while typing. This can be disabled using the new "Play sound for spelling errors while typing" option in NVDA's Keyboard Settings dialog. (#2024)
* Grammar errors are now reported in Microsoft Word. This can be disabled using the new "Report grammar errors" option in NVDA's Document Formatting preferences dialog. (#5877)

### Changes

* In browse mode and editable text fields, NVDA now treats numpadEnter the same as the main enter key. (#5385)
* NVDA has switched to the eSpeak NG speech synthesizer. (#5651)
* In Microsoft Excel, NVDA no longer ignores a column header for a cell when there is a blank row between the cell and the header. (#5396)
* In Microsoft Excel, coordinates are now announced before headers to eliminate ambiguity between headers and content. (#5396)

### Bug Fixes

* In browse mode, when attempting to use single letter navigation to move to an element which isn't supported for the document, NVDA reports that this isn't supported rather than reporting that there is no element in that direction. (#5691)
* When listing sheets in the Elements List in Microsoft Excel, sheets containing only charts are now included. (#5698)
* NVDA no longer reports extraneous information when switching windows in a Java application with multiple windows such as IntelliJ or Android Studio. (#5732)
* In Scintilla based editors such as Notepad++, braille is now updated correctly when moving the cursor using a braille display. (#5678)
* NVDA no longer sometimes crashes when enabling braille output. (#4457)
* In Microsoft Word, paragraph indentation is now always reported in the measurement unit chosen by the user (e.g. centimeters or inches). (#5804)
* When using a braille display, many NVDA messages that were previously only spoken are now brailled as well. (#5557)
* In accessible Java applications, the level of tree view items is now reported. (#5766)
* Fixed crashes in Adobe Flash in Mozilla Firefox in some cases. (#5367)
* In Google Chrome and Chrome-based browsers, documents within dialogs or applications can now be read in browse mode. (#5818)
* In Google Chrome and Chrome-based browsers, you can now force NVDA to switch to browse mode in web dialogs or applications. (#5818)
* In Internet Explorer and other MSHTML controls, moving focus to certain controls (specifically, where aria-activedescendant is used) no longer incorrectly switches to browse mode. This occurred, for example, when moving to suggestions in address fields when composing a message in Gmail. (#5676)
* In Microsoft Word, NVDA no longer freezes in large tables when reporting of table row/column headers is enabled. (#5878)
* In Microsoft word, NVDA no longer incorrectly reports text with an outline level (but not a built-in heading style) as a heading. (#5186)
* In browse mode in Microsoft Word, the Move past end/to start of container commands (comma and shift+comma) now work for tables. (#5883)

### Changes for Developers

* NVDA's C++ components are now built with Microsoft Visual Studio 2015. (#5592)
* You can now present a text or HTML message to the user in browse mode using ui.browseableMessage. (#4908)
* In the User Guide, when a <!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) -->

## 2016.1

Highlights of this release include the ability to optionally lower the volume of other sounds; improvements to braille output and braille display support; several significant fixes to Microsoft Office support; and fixes to browse mode in iTunes.

### New Features

* New braille translation tables: Polish 8 dot computer braille, Mongolian. (#5537, #5574)
* You can turn off the braille cursor and change its shape using the new Show cursor and Cursor shape options in the Braille Settings dialog. (#5198)
* NVDA can now connect to a HIMS Smart Beetle braille display via Bluetooth. (#5607)
* NVDA can optionally lower the volume of other sounds when installed on Windows 8 and later. This can be configured using the Audio ducking mode option in the NVDA Synthesizer dialog or by pressing NVDA+shift+d. (#3830, #5575)
* Support for the APH Refreshabraille in HID mode and the Baum VarioUltra and Pronto! when connected via USB. (#5609)
* Support for HumanWare Brailliant BI/B braille displays when the protocol is set to OpenBraille. (#5612)

### Changes

* Reporting of emphasis is now disabled by default. (#4920)
* In the Elements List dialog in Microsoft Excel, the shortcut for Formulas has been changed to alt+r so that it is different to the shortcut for the Filter field. (#5527)
* Updated liblouis braille translator to 2.6.5. (#5574)
* The word "text" is no longer reported when moving the focus or review cursor to text objects. (#5452)

### Bug Fixes

* In iTunes 12, browse mode now updates correctly when a new page loads in the iTunes Store. (#5191)
* In Internet Explorer and other MSHTML controls, moving to specific heading levels with single letter navigation now behaves as expected when the level of a heading is overridden for accessibility purposes (specifically, when aria-level overrides the level of an h tag). (#5434)
* In Spotify, focus no longer frequently lands on "unknown" objects. (#5439)
* Focus is now restored correctly when returning to Spotify from another application. (#5439)
* When toggling between browse mode and focus mode, the mode is reported in braille as well as speech. (#5239)
* The Start buttn on the Taskbar is no longer reported as a list and/or as selected in some versions of Windows. (#5178)
* Messages such as "inserted" are no longer reported when composing messages in Microsoft Outlook. (#5486)
* When using a braille display and text is selected on the current line (e.g. when searching in a text editor for text which occurs on the same line), the braille display will be scrolled if appropriate. (#5410)
* NVDA no longer silently exits when closing a Windows command console with alt+f4 in Windows 10. (#5343)
* In the Elements List in browse mode, when you change the type of element, the Filter by field is now cleared. (#5511)
* In editable text in Mozilla applications, moving the mouse again reads the appropriate line, word, etc. as expected instead of the entire content. (#5535)
* When moving the mouse in editable text in Mozilla applications, reading no longer stops at elements such as links within the word or line being read. (#2160, #5535)
* In Internet Explorer, the shoprite.com website can now be read in browse mode instead of reporting as blank. (Specifically, malformed lang attributes are now handled gracefully.) (#5569)
* In Microsoft Word, tracked changes such as "inserted" are no longer reported when track changes markup is not displayed. (#5566)
* When a toggle button is focused, NVDA now reports when it is changed from pressed to not pressed. (#5441)
* Reporting of mouse shape changes again works as expected. (#5595)
* When speaking line indentation, non-breaking spaces are now treated as normal spaces. Previously, this could cause announcements such as "space space space" instead  of "3 space". (#5610)
* When closing a modern Microsoft input method candidate list, focus is correctly restored to either the input composition or the underlying document. (#4145)
* In Microsoft Office 2013 and later, when the ribbon is set to show only tabs, items in the ribbon are again reported as expected when a tab is activated. (#5504)
* Fixes and improvements to touch screen gesture detection and binding. (#5652)
* Touch screen hovers are no longer reported in input help. (#5652)
* NVDA no longer fails to list comments in the Elements List for Microsoft Excel if a comment is  on a merged cell. (#5704)
* In a very rare case, NVDA no longer fails to read sheet content in Microsoft Excel with reporting of row and column headers enabled. (#5705)
* In Google Chrome, navigating within an Input composition when entering east Asian characters now works as expected. (#4080)
* When searching Apple Music in iTunes, browse mode for the search results document is now updated as expected. (#5659)
* In Microsoft Excel, pressing shift+f11 to create a new sheet now reports your new position instead of reporting nothing. (#5689)
* Fixed problems with braille display output when entering Korean characters. (#5640)

### Changes for Developers

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

Highlights of this release include performance improvements in Windows 10; inclusion in the Ease of Access Center in Windows 8 and later; enhancements for Microsoft Excel, including listing and renaming of sheets and access to locked cells in protected sheets; and support for editing of rich text in Mozilla Firefox, Google Chrome and Mozilla Thunderbird.

### New Features

* NVDA now appears in the Ease of Access Center in Windows 8 and later. (#308)
* When moving around cells in Excel, formatting changes are now automatically reported if the appropriate options are turned on in NVDA's Document Formatting Settings dialog. (#4878)
* A Report Emphasis option has been added to NVDA's Document formatting settings dialog. On by default, this option allows NVDA to automatically report the existence of emphasised text in documents. So far, this is only supported for em and strong tags in Browse Mode for Internet Explorer and other MSHTML controls. (#4920)
* The existence of inserted and deleted text is now reported in Browse Mode for Internet Explorer and other MSHTML controls if NVDA's Report Editor Revisions option is enabled. (#4920)
* When viewing track changes in NVDA's Elements List for Microsoft Word, more information such as what formatting properties were changed is now displayed. (#4920)
* Microsoft Excel: listing and renaming of sheets is now possible from NVDA's Elements List (NVDA+f7). (#4630, #4414)
* It is now possible to configure whether actual symbols are sent to speech synthesizers (e.g. to cause a pause or change in inflection) in the Symbol Pronunciation dialog. (#5234)
* In Microsoft Excel, NVDA now reports any input messages set by the sheet author on cells. (#5051)
* Support for the Baum Pronto! V4 and VarioUltra braille displays when connected via Bluetooth. (#3717)
* Support for editing of rich text in Mozilla applications such as Google Docs with braille support enabled in Mozilla Firefox and HTML composition in Mozilla Thunderbird. (#1668)
* Support for editing of rich text in Google Chrome and Chrome-based browsers such as Google Docs with braille support enabled. (#2634)
 * This requires Chrome version 47 or later.
* In browse mode in Microsoft Excel, you can navigate to locked cells in protected sheets. (#4952)

### Changes

* The Report Editor Revisions option in NVDA's Document formatting settings dialog is now turned on by default. (#4920)
* When moving by character in Microsoft Word with NVDA's Report Editor Revisions option enabled, less information is now reported for track changes, which makes navigation more efficient. To view the extra information, use the Elements List. (#4920)
* Updated liblouis braille translator to 2.6.4. (#5341)
* Several symbols (including basic mathematical symbols) have been moved to level some so that they are spoken by default. (#3799)
* If the synthesizer supports it, speech should now pause for parentheses and the en dash (–). (#3799)
* When selecting text, the text is reported before the indication of selection instead of after. (#1707)

### Bug Fixes

* Major performance improvements when navigating the Outlook 2010/2013 message list. (#5268)
* In a chart in Microsoft Excel, navigating with certain keys (such as changing sheets with control+pageUp and control+pageDown) now works correctly. (#5336)
* Fixed the visual appearance of the buttons in the warning dialog which is displayed when you attempt to downgrade NVDA. (#5325)
* In Windows 8 and later, NVDA now starts a lot earlier when configured to start after logging on to Windows. (#308)
 * If you enabled this using a previous version of NVDA, you will need to disable it and enable it again in order for the change to take effect. Follow this procedure:
  1. Open the General Settings dialog.
  1. Uncheck the Automatically start NVDA after I log on to Windows checkbox.
  1. Press the OK button.
  1. Open the General Settings dialog again.
  1. Check the Automatically start NVDA after I log on to Windows checkbox.
  1. Press the OK button.
* Performance enhancements for UI Automation including  File Explorer and Task Viewer. (#5293)
* NVDA now correctly switches to focus mode when tabbing to read-only ARIA grid controls in Browse Mode for Mozilla Firefox and other Gecko-based controls. (#5118)
* NVDA now correctly reports "no previous" instead of "no next" when there are no more objects when flicking left on a touch screen.
* Fixed problems when typing multiple words into the filter field in the Input Gestures dialog. (#5426)
* NVDA no longer freezes in some cases when reconnecting to a HumanWare Brailliant BI/B series display via USB. (#5406)
* In languages with conjunct characters, character descriptions now work as expected for upper case English characters. (#5375)
* NVDA should no longer occasionally freeze when bringing up the Start Menu in Windows 10. (#5417)
* In Skype for Desktop, notifications which are displayed before a previous notification disappears are now reported. (#4841)
* Notifications are now reported correctly in Skype for Desktop 7.12 and later. (#5405)
* NVDA now correctly reports the focus when dismissing a context menu in some applications such as Jart. (#5302)
* In Windows 7 and later, Color is again reported in certain applications such as Wordpad. (#5352)
* When editing in Microsoft PowerPoint, pressing enter now reports automatically entered text such as a bullet or number. (#5360)

## 2015.3

Highlights of this release include initial support for Windows 10; the ability to disable single letter navigation in browse mode (useful for some web apps); improvements in Internet Explorer; and fixes for garbled text when typing in certain applications with braille enabled.

### New Features

* The existence of spelling errors is announced in editable fields for Internet Explorer and other MSHTML controls. (#4174)
* Many more Unicode math symbols are now spoken when they appear in text. (#3805)
* Search suggestions in the Windows 10 start screen are automatically reported. (#5049)
* Support for the EcoBraille 20, EcoBraille 40, EcoBraille 80 and EcoBraille Plus braille displays. (#4078)
* In browse mode, you can now toggle single letter navigation on and off by pressing NVDA+shift+space. When off, single letter keys are passed to the application, which is useful for some web applications such as Gmail, Twitter and Facebook. (#3203)
* New braille translation tables: Finnish 6 dot, Irish grade 1, Irish grade 2, Korean grade 1 (2006), Korean grade 2 (2006). (#5137, #5074, #5097)
* The QWERTY keyboard on the Papenmeier BRAILLEX Live Plus braille display is now supported. (#5181)
* Experimental support for the Microsoft Edge web browser and browsing engine in Windows 10. (#5212)
* New language: Kannada.

### Changes

* Updated liblouis braille translator to 2.6.3. (#5137)
* When attempting to install an earlier version of NVDA than is currently installed, you will now be warned that this is not recommended and that NVDA should be completely uninstalled before proceeding. (#5037)

### Bug Fixes

* In browse mode for Internet Explorer and other MSHTML controls, quick navigation by form field no longer incorrectly includes presentational list items. (#4204)
* In Firefox, NVDA no longer inappropriately reports the content of an ARIA tab panel when focus moves inside it. (#4638)
* In Internet Explorer and other MSHTML controls, tabbing into sections, articles or dialogs  no longer inappropriately reports all content in the container. (#5021, #5025)
* When using Baum/HumanWare/APH braille displays with a braille keyboard, braille input no longer stops functioning after pressing another type of key on the display. (#3541)
* In Windows 10, extraneous information is no longer reported when pressing alt+tab or alt+shift+tab to switch between applications. (#5116)
* Typed text is no longer garbled when using certain applications such as Microsoft Outlook with a braille display. (#2953)
* In browse mode in Internet Explorer and other MSHTML controls, the correct content is now reported when an element appears or changes and is immediately focused. (#5040)
* In browse mode in Microsoft Word, single letter navigation now updates the braille display and the review cursor as expected. (#4968)
* In braille, extraneous spaces are no longer displayed between or after indicators for controls and formatting. (#5043)
* When an application is responding slowly and you switch away from that application, NVDA is now much more responsive in other applications in most cases. (#3831)
* Windows 10 Toast notifications are now reported as expected. (#5136)
* The value is now reported as it changes in certain (UI Automation) combo boxes where this was not working previously.
* In browse mode in web browsers, tabbing now behaves as expected after tabbing to a frame document. (#5227)
* The Windows 10 lock screen can now be dismissed using a touch screen. (#5220)
* In Windows 7 and later, text is no longer garbled when typing in certain applications such as Wordpad and Skype with a braille display. (#4291)
* On the Windows 10 lock screen, it is no longer possible to read the clipboard, access running applications with the review cursor, change NVDA configuration, etc. (#5269)

### Changes for Developers

* You can now inject raw input from a system keyboard that is not handled natively by Windows (e.g. a QWERTY keyboard on a braille display) using the new keyboardHandler.injectRawKeyboardInput function. (#4576)
* eventHandler.requestEvents has been added to request particular events that are blocked by default; e.g. show events from a specific control or certain events even when in the background. (#3831)
* Rather than a single i18nName attribute, synthDriverHandler.SynthSetting now has separate displayNameWithAccelerator and displayName attributes to avoid reporting of the accelerator in the synth settings ring in some languages.
 * For backwards compatibility, in the constructor, displayName is optional and will be derived from displayNameWithAccelerator if not provided. However, if you intend to have an accelerator for a setting, both should be provided.
 * The i18nName attribute is deprecated and may be removed in a future release.

## 2015.2

Highlights of this release include the ability to read charts in Microsoft Excel and support for reading and interactive navigation of mathematical content.

### New Features

* Moving forward and backward by sentence in Microsoft Word and Outlook is now possible with alt+downArrow and alt+upArrow respectively. (#3288)
* New braille translation tables for several Indian languages. (#4778)
* In Microsoft Excel, NVDA now reports when a cell has overflowing or cropped content. (#3040)
* In Microsoft Excel, you can now use the Elements List (NVDA+f7) to allow listing of charts, comments and formulas. (#1987)
* Support for reading charts in Microsoft Excel. To use this, select the chart using the Elements List (NVDA+f7) and then use the arrow keys to move between the data points. (#1987)
* Using MathPlayer 4 from Design Science, NVDA can now read and interactively navigate mathematical content in web browsers and in Microsoft Word and PowerPoint. See the "Reading Mathematical Content" section in the User Guide for details. (#4673)
* It is now possible to assign input gestures (keyboard commands, touch gestures, etc.) for all NVDA preferences dialogs and document formatting options using the Input Gestures dialog. (#4898)

### Changes

* In NVDA's Document Formatting dialog, the keyboard shortcuts for Report lists, Report links, Report line numbers and Report font name have been changed. (#4650)
* In NVDA's Mouse Settings dialog, keyboard shortcuts have been added for play audio coordinates when mouse moves and brightness controls audio coordinates volume. (#4916)
* Significantly improved reporting of color names. (#4984)
* Updated liblouis braille translator to 2.6.2. (#4777)

### Bug Fixes

* Character descriptions are now handled correctly for conjunct characters in certain Indian languages. (#4582)
* If the "Trust voice's language when processing characters and symbols" option is enabled, the Punctuation/Symbol pronunciation dialog now correctly uses the voice language. Also, the language for which pronunciation is being edited is shown in the dialog's title. (#4930)
* In Internet Explorer and other MSHTML controls, typed characters are no longer inappropriately announced in editable combo boxes such as the Google search field on the Google home page. (#4976)
* When selecting colors in Microsoft Office applications, color names are now reported. (#3045)
* Danish braille output now works again. (#4986)
* PageUp/pageDown can again be used to change slides within a PowerPoint slide show. (#4850)
* In Skype for Desktop 7.2 and later, typing notifications are now reported and problems immediately after moving focus out of a conversation have been fixed. (#4972)
* Fixed problems when typing certain punctuation/symbols such as brackets into the filter field in the Input Gestures dialog. (#5060)
* In Internet Explorer and other MSHTML controls, pressing g or shift+g to navigate to graphics now includes elements marked as images for accessibility purposes (i.e. ARIA role img). (#5062)

### Changes for Developers

* brailleInput.handler.sendChars(mychar) will no longer filter out a character if it is equal to the previous character by ensuring that the key sent is correctly released. (#4139)
* Scripts for changing touch modes will now honor new labeles added to touchHandler.touchModeLabels. (#4699)
* Add-ons can provide their own math presentation implementations. See the mathPres package for details. (#4509)
* Speech commands have been implemented to insert a break between words and to change the pitch, volume and rate. See BreakCommand, PitchCommand, VolumeCommand and RateCommand in the speech module. (#4674)
 * There is also speech.PhonemeCommand to insert specific pronunciation, but the current implementations only support a very limited number of phonemes.

## 2015.1

Highlights of this release include browse mode for documents in Microsoft Word and Outlook; major enhancements to support for Skype for Desktop; and significant fixes for Microsoft Internet Explorer.

### New Features

* You can now add new symbols in the Symbol Pronunciation dialog. (#4354)
* In the Input Gestures dialog, you can use the new "Filter by" field to show only gestures containing specific words. (#4458)
* NVDA now automatically reports new text in mintty. (#4588)
* In the browse mode Find dialog, there is now an option to perform a case sensitive search. (#4584)
* Quick navigation (pressing h to move by heading, etc.) and Elements List (NVDA+f7) are now available in Microsoft Word documents by turning on browse mode with NVDA+space. (#2975)
* Reading HTML messages in Microsoft Outlook 2007 and later has been majorly improved as Browse mode is automatically enabled for these messages. If browse mode is not enabled in some rare situations, you can force it on with NVDA+space. (#2975)
* Table column headers in Microsoft word are automatically reported for tables where a header row has been explicitly specified by the author via Microsoft word's table properties. (#4510)
 * However, For tables where rows have been merged, this will not work automatically. In this situation, you can still set column headers manually in NVDA with NVDA+shift+c.
* In Skype for Desktop, notifications are now reported. (#4741)
* In Skype for Desktop, you can now report and review recent messages using NVDA+control+1 through NVDA+control+0; e.g. NVDA+control+1 for the most recent message and NVDA+control+0 for the tenth most recent. (#3210)
* In a conversation in Skype for Desktop, NVDA now reports when a contact is typing. (#3506)
* NVDA can now be installed silently via the command line without starting the installed copy after installation. To do this, use the --install-silent option. (#4206)
* Support for the Papenmeier BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus braille displays. (#4614)

### Changes

* In NVDA's Document Formatting settings dialog, the option to report spelling errors now has a shortcut key (alt+r). (#793)
* NVDA will now use the synthesizer/voice's language for character and symbol processing (including punctuation/symbol names), regardless of whether automatic language switching is turned on. To turn off this feature so that NVDA again uses its interface language, uncheck the new option in Voice settings called Trust Voice's language when processing characters and symbols. (#4210)
* Support for the Newfon synthesizer has been removed. Newfon is now available as an NVDA add-on. (#3184)
* Skype for Desktop 7 or later is now required for use with NVDA; earlier versions are not supported. (#4218)
* Downloading of NVDA updates is now more secure. (Specifically, the update information is retrieved via https and the hash of the file is verified after it is downloaded.) (#4716)
* eSpeak has been upgraded to version 1.48.04 (#4325)

### Bug Fixes

* In Microsoft Excel, merged row and column header cells are now handled correctly. For example, if A1 and B1 are merged, then B2 will now have A1 and B1 reported as its column header rather than nothing at all. (#4617)
* When editing the content of a text box in Microsoft PowerPoint 2003, NVDA will correctly report the content of each line. Previously, in each paragraph, lines would increasingly be off by one character. (#4619)
* All of NVDA's dialogs are now centred on the screen, improving visual presentation and usability. (#3148)
* In Skype for desktop, when entering an introductory message to add a contact, entering and moving through the text now works correctly. (#3661)
* When focus moves to a new item in tree views in the Eclipse IDE, if the previously focused item is a check box, it is no longer incorrectly announced. (#4586)
* In the Microsoft Word spell check dialog, the next error will be automatically reported when the last one has been changed or ignored using respective shortcut keys. (#1938)
* Text can again be read correctly in places such as Tera Term Pro's terminal window and documents in Balabolka. (#4229)
* Focus now correctly returns to the document being edited When finishing input composition of text in Korean and other east Asian languages while editing within a frame in Internet Explorer and other MSHTML documents. (#4045)
* In the Input Gestures dialog, when selecting a keyboard layout for a keyboard gesture being added, pressing escape now closes the menu as expected instead of closing the dialog. (#3617)
* When removing an add-on, the add-on directory is now correctly deleted after restarting NVDA. Previously, you had to restart twice. (#3461)
* Major problems have been fixed when using Skype for Desktop 7. (#4218)
* When you send a message in Skype for Desktop, it is no longer read twice. (#3616)
* In Skype for Desktop, NVDA should no longer occasionally spuriously read a large flood of messages (perhaps even an entire conversation). (#4644)
* fixed a problem where NVDA's Report date/time command did not honor the regional settings specified by the user in some cases. (#2987)
* In browse mode, nonsensical text (sometimes spanning several lines) is no longer presented for certain graphics such as found on Google Groups. (Specifically, this occurred with base64 encoded images.) (#4793)
* NVDA should no longer freeze after a few seconds when moving focus away from a Windows Store app as it becomes suspended. (#4572)
* The aria-atomic attribute on live regions in Mozilla Firefox is now honored even when the atomic element itself changes. Previously, it only affected descendant elements. (#4794)
* Browse mode will reflect updates, and live regions will be announced, for   browse mode documents within ARIA applications embedded in a document in Internet Explorer or other MSHTML controls. (#4798)
* When text is changed or added in live regions in Internet Explorer and other MSHTML controls where the author has specified that text is relevant, only the changed or added text is announced, rather than all of the text in the containing element. (#4800)
* Content indicated by the aria-labelledby attribute on elements in Internet Explorer and other MSHTML controls correctly replaces the original content  where it is appropriate to do so. (#4575)
* When checking spelling in Microsoft Outlook 2013, the misspelled word is now announced. (#4848)
* In Internet Explorer and other MSHTML controls, content inside elements hidden with visibility:hidden is no longer inappropriately presented in browse mode. (#4839, #3776)
* In Internet Explorer and other MSHTML controls, the title attribute on form controls no longer inappropriately takes preference over other label associations. (#4491)
* In Internet Explorer and other MSHTML controls, NVDA no longer ignores focusing  of elements  due to the aria-activedescendant attribute. (#4667)

### Changes for Developers

* Updated wxPython to 3.0.2.0. (#3763)
* Updated Python to 2.7.9. (#4715)
* NVDA no longer crashes when restarting after removing or updating an add-on which imports speechDictHandler in its installTasks module. (#4496)

## 2014.4

### New Features

* New languages: Colombian Spanish, Punjabi.
* It is now possible to restart NVDA or restart NVDA with add-ons disabled from NVDA's exit dialog. (#4057)
 * NVDA can also be started with add-ons disabled by using the --disable-addons command line option.
* In speech dictionaries, it is now possible to specify that a pattern should only match if it is a whole word; i.e. it does not occur as part of a larger word. (#1704)

### Changes

* If an object you have moved to with object navigation is inside a browse mode document, but the object you were on previously was not, the review mode is automatically set to document. Previously, this only happened if the navigator object was moved due to the focus changing. (#4369)
* The Braille display and Synthesizer lists in the respective settings dialogs are now alphabetically sorted except for No braille/No speech, which are now at the bottom. (#2724)
* Updated liblouis braille translator to 2.6.0. (#4434, #3835)
* In browse mode, pressing e and shift+e to navigate to edit fields now includes editable combo boxes. This includes the search box in the latest version of Google Search. (#4436)
* Clicking the NVDA icon in the Notification Area with the left mouse button now opens the NVDA menu instead of doing nothing. (#4459)

### Bug Fixes

* When moving focus back to a browse mode document (e.g. alt+tabbing to an already opened web page), the review cursor is properly positioned at the virtual caret, rather than the focused control (e.g. a nearby link). (#4369)
* In PowerPoint slide shows, the review cursor correctly follows the virtual caret. (#4370)
* In Mozilla Firefox and other Gecko-based browsers, new content within a live region will be announced even if the new content has a usable ARIA live type different to the parent live region; e.g. when content marked as assertive is added to a live region marked as polite. (#4169)
* In Internet Explorer and other MSHTML controls, some cases where a document is contained within another document no longer prevent the user from accessing some of the content (specifically, framesets inside framesets). (#4418)
* NVDA no longer crashes when attempting to use a Handy Tech braille display in some cases. (#3709)
* In Windows Vista, a spurious "Entry Point Not Found" dialog is no longer displayed in several cases such as when starting NVDA from the Desktop shortcut or via the shortcut key. (#4235)
* Serious problems with editable text controls in dialogs in recent versions of Eclipse have been fixed. (#3872)
* In Outlook 2010, moving the caret now works as expected in the location field of appointments and meeting requests. (#4126)
* Inside a live region, content which is marked as not being live (e.g. aria-live="off") is now correctly ignored. (#4405)
* When reporting the text of a status bar that has a name, the name is now correctly separated from the first word of the status bar text. (#4430)
* In password entry fields with speaking of typed words enabled, multiple asterisks are no longer pointlessly reported when beginning new words. (#4402)
* In the Microsoft Outlook message list, items are no longer pointlessly announced as Data Items. (#4439)
* When selecting text in the code editing control in the Eclipse IDE, the entire selection is no longer announced every time the selection changes. (#2314)
* Various versions of Eclipse, such as Spring Tool Suite and the version included in the Android Developer Tools bundle, are now recognised as Eclipse and handled appropriately. (#4360, #4454)
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls (including many Windows 8 applications) is now much more accurate  on high DPI displays or when document zoom is changed. (#3494) 
* Mouse tracking and touch exploration in Internet Explorer and other MSHTML controls will now announce the label of more buttons. (#4173)
* When using a Papenmeier BRAILLEX braille display with BrxCom, keys on the display now work as expected. (#4614)

### Changes for Developers

* For executables which host many different apps (e.g. javaw.exe), code can now be provided to load specific app modules for each app instead of loading the same app module for all hosted apps. (#4360)
 * See the code documentation for appModuleHandler.AppModule for details.
 * Support for javaw.exe is implemented.

## 2014.3

### New Features

* The sounds played when NVDA starts and exits can be disabled via a new option in the General Settings dialog. (#834)
* Help for add-ons can be accessed from the Add-ons Manager for add-ons which support this. (#2694)
* Support for the Calendar in Microsoft Outlook 2007 and above (#2943) including:
 * Announcement of the current time when moving around with the arrow keys.
 * Indication if the selected time is within any appointments.
 * announcement of the selected appointment when pressing tab.
 * Smart filtering of the date so as to only announce the date if the new selected time or appointment is on a different day to the last.
* Enhanced support for the Inbox and other message lists in Microsoft Outlook 2010 and above (#3834) including:
 * The ability to silence column headers (from, subject, etc.) by turning off the Report Table row and column headers option in Document Formatting settings.
 * The ability to use table navigation commands (control + alt + arrows) to move through the individual columns. 
* Microsoft word: If an inline image has no alternative text set, NVDA will instead report the title of the image if the author has provided one. (#4193)
* Microsoft Word: NVDA can now report paragraph indenting with  the report formatting command (NVDA+f). It can also be reported automatically when the new Report Paragraph indenting option is enabled in Document Formatting settings. (#4165)
* Report automatically inserted text such as a new bullet, number or tab indent when pressing enter in editable documents and text fields. (#4185)
* Microsoft word: Pressing NVDA+alt+c will report  the text of a comment if the cursor is within one. (#3528)
* Improved support for automatic column and row header reading in Microsoft Excel (#3568) including:
 * Support of Excel defined name ranges to identify header cells (compatible with Jaws screen reader) .
 * The set column header (NVDA+shift+c) and set row header (NVDA+shift+r) commands now store the settings in the worksheet so that they are available the next time the sheet is opened, and will be available to other screen readers that support the defined name range scheme.
 * These commands can also now be used multiple times per sheet to set different headers for different regions.
* Support for automatic column and row header reading in Microsoft Word (#3110) including:
 * Support of Microsoft Word bookmarks to identify header cells (compatible with Jaws screen reader).
 -  set column header (NVDA+shift+c) and set row header (NVDA+shift+r) commands  while on the first header cell in a table allow you to tell NVDA that these headers should be reported automatically.  Settings are stored in the document so that they are available the next time the document is opened, and will be available to other screen readers that support the bookmark scheme.
* Microsoft Word: Report the distance from the left edge of the page when the tab key is pressed. (#1353)
* Microsoft Word: provide feedback in speech and braille for most available formatting shortcut keys (bold, italic, underline, alignment, outline level, superscript, subscript and font size). (#1353)
* Microsoft Excel: If the selected cell contains comments, they can be now reported by pressing NVDA+alt+c. (#2920)
* Microsoft Excel: Provide an NVDA-specific dialog to edit the comments on the currently selected cell when pressing Excel's shift+f2 command to enter comment editing mode. (#2920)
* Microsoft Excel: speech and braille feedback for many more selection movement shortcuts (#4211) including:
 * Vertical page movement (pageUp and pageDown);
 * Horizontal page movement (alt+pageUp and alt+pageDown);
 * Extend selection (the above keys with Shift added); and
 * Selecting the current region (control+shift+8).
* Microsoft Excel: The vertical and horizontal  alignment for cells can now be reported with the report formatting command (NVDA+f). It can also be reported automatically if the Report alignment option in Document Formatting settings is enabled. (#4212)
* Microsoft Excel: The style of a cell can now be reported with the report formatting command (NVDA+f). It can also be reported automatically if the Report Style option in Document formatting settings is enabled. (#4213)
* Microsoft PowerPoint: when moving shapes around a slide with the arrow keys, the shape's current location is now reported (#4214) including:
 * The distance between the shape and each of the  slide edges is reported.
 * If the shape covers or is covered by another shape, then the distance overlapped and the overlapped shape are reported.
 * To report this information at any time without moving a shape, press the report location command (NVDA+delete).
 * When selecting a shape, if it is covered by another shape, NVDA will report that it is obscured.
* The report location command (NVDA+delete) is more context specific in some situations. (#4219)
 * In standard edit fields and browse mode, the cursor position as a percentage through the content and its screen coordinates are reported.
 * On shapes in PowerPoint Presentations, position of the shape relative to the slide and other shapes is reported.
 * Pressing this command twice will produce the previous behaviour of reporting the location information for the entire control.
* New language: Catalan.

### Changes

* Updated liblouis braille translator to 2.5.4. (#4103)

### Bug Fixes

* In Google Chrome and Chrome-based browsers, certain chunks of text (such as those with emphasis) are no longer repeated when reporting the text of an alert or dialog. (#4066)
* In browse mode in Mozilla applications, pressing enter on a button, etc. no longer fails to activate it (or activates the wrong control) in certain cases such as the buttons at the top of Facebook. (#4106)
* Useless information is no longer announced when tabbing in iTunes. (#4128)
* In certain lists in iTunes such as the Music list, moving to the next item using object navigation now works correctly. (#4129)
* HTML elements considered headings because of WAI ARIA markup are now included in the Browse mode Elements list and quick navigation for Internet Explorer documents. (#4140)
* Following same-page links in recent versions of Internet Explorer now correctly moves to and reports the destination position in browse mode  documents. (#4134)
* Microsoft Outlook 2010 and above: Overall access to secure dialogs such as the New profiles and mail setup dialogs has been improved. (#4090, #4091, #4095)
* Microsoft Outlook: Useless verbosity has been decreased in command toolbars when navigating through  certain dialogs. (#4096, #3407)
* Microsoft word: Tabbing to a blank cell in a table no longer incorrectly announces exiting the table. (#4151)
* Microsoft Word: The first character past the end of a table (including a new blank line) is no longer incorrectly considered to be inside the table. (#4152)
* Microsoft Word 2010 spell check dialog: The actual misspelled word is reported rather than  inappropriately reporting just the first bold word. (#3431)
* In browse mode in Internet Explorer and other MSHTML controls, tabbing or using single letter navigation to move to form fields again reports the label in many cases where it didn't (specifically, where HTML label elements are used). (#4170)
* Microsoft Word: Reporting the existence and placement of comments is more accurate. (#3528)
* Navigation of certain dialogs in MS Office products such as Word, Excel and Outlook has been improved by no longer reporting particular control container toolbars which are not useful to the user. (#4198) 
* Task panes such as clipboard manager or File recovery no longer accidentilly seem to gain focus when opening an application such as Microsoft Word or Excel, which was sometimes causing the user to have to switch away from and back to the application to use the document or spreadsheet.  (#4199)
* NVDA no longer fails to run on recent Windows Operating Systems if the user's Windows language is set to Serbian (Latin). (#4203)
* Pressing numlock while in input help mode now correctly toggles numlock, rather than causing the keyboard and the Operating System to become out of sync in regards to the state of this key. (#4226)
* In Google Chrome, the title of the document is again reported when switching tabs. In NVDA 2014.2, this did not occur in some cases. (#4222)
* In Google Chrome and Chrome-based browsers, the URL of the document is no longer reported when reporting the document. (#4223)
* When running say all with the No speech synthesizer selected (useful for automated testing), say all will now complete instead of stopping after the first few lines. (#4225)
* Microsoft Outlook's Signature dialog: The Signature editing field is now accessible, allowing for full cursor tracking and format detection. (#3833)
* Microsoft Word: When reading the last line of a table cell, the entire table cell is no longer read. (#3421)
* Microsoft Word: When reading the first or last line of a table of contents, the entire table of contents is no longer read. (#3421)
* When speaking typed words and in some other cases, words are no longer incorrectly broken at marks such as vowel signs and virama in Indic languages. (#4254)
* Numeric editable text fields in GoldWave are now handled correctly. (#670)
* Microsoft Word: when moving by paragraph with control+downArrow / control+upArrow, it is no longer necessary to press them twice if moving through bulleted or numbered lists. (#3290)

### Changes for Developers

* NVDA now has unified support for add-on documentation. See the Add-on Documentation section of the Developer Guide for details. (#2694)
* When providing gesture bindings on a ScriptableObject via __gestures, it is now possible to provide the None keyword as the script. This unbinds the gesture in any base classes. (#4240)
* It is now possible to change the shortcut key used to start NVDA for locales where the normal shortcut causes problems. (#2209)
 * This is done via gettext.
 * Note that the text for the Create desktop shortcut option in the Install NVDA dialog, as well as the shortcut key in the User Guide, must also be updated.

## 2014.2

### New Features

* Announcement of text selection is now possible in some custom edit fields where display information is used. (#770)
* In accessible Java applications, position information is now announced for radio buttons and other controls that expose group information. (#3754)
* In accessible Java applications, keyboard shortcuts are now announced for controls that have them. (#3881)
* In browse mode, labels on landmarks are now reported. They are also included in the Elements List dialog. (#1195)
* In browse mode, labelled regions are now treated as landmarks. (#3741)
* In Internet Explorer documents and applications, Live Regions (part of the W3c ARIA standard) are now supported, thus allowing web authors to mark particular content to be automatically spoken as it changes. (#1846)

### Changes

* When exiting a dialog or application within a browse mode document, the browse mode document's name and type is no longer announced. (#4069)

### Bug Fixes

* The standard Windows System menu is no longer accidentally silenced in Java applications. (#3882)
* When copying text from screen review, line breaks are no longer ignored. (#3900)
* Pointless whitespace objects are no longer reported in some applications when the focus changes or when using object navigation with simple review enabled. (#3839)
* Message boxes and other dialogs produced by NVDA again cause previous speech to be canceled before announcing the dialog.
* In browse mode, the labels of controls such as links and buttons are now rendered correctly where the label has been overridden by the author for accessibility purposes (specifically, using aria-label or aria-labelledby). (#1354)
* In Browse mode in Internet Explorer, text contained within an element marked as presentational (ARIA role="presentation") is no longer inappropriately ignored. (#4031)
* It is now again possible to type Vietnamese text using the Unikey software. To do this, uncheck the new Handle keys from other applications checkbox in NVDA's Keyboard settings dialog. (#4043)
* In browse mode, radio and check menu items are reported as controls instead of just clickable text. (#4092)
* NVDA no longer incorrectly switches from focus mode to browse mode when a radio or check menu item is focused. (#4092)
* In Microsoft PowerPoint with speaking of typed words enabled, characters erased with backspace are no longer announced as part of the typed word. (#3231)
* In Microsoft Office 2010 Options dialogs, the labels of combo boxes are reported correctly. (#4056)
* In browse mode in Mozilla applications, using quick navigation commands to move to the next or previous button or form field now includes toggle buttons as expected. (#4098)
* The content of alerts in Mozilla applications is no longer reported twice. (#3481)
* In browse mode, containers and landmarks are no longer inappropriately repeated while navigating within them at the same time as page content is changing (e.g. navigating the Facebook and Twitter websites). (#2199)
* NVDA recovers in more cases when switching away from applications that stop responding. (#3825)
* The caret (insertion point) again correctly updates when doing a sayAll command while in editable text drawn directly to the screen. (#4125)

## 2014.1

### New Features

* Support for Microsoft PowerPoint 2013. Note that protected view is not supported. (#3578)
* In Microsoft word and Excel, NVDA can now read the selected symbol when choosing symbols using the Insert Symbols dialog. (#3538)
* It is now possible to choose if content in documents should be identified as clickable via a new option in the Document Formatting settings dialog. This option is on by default in accordance with the previous behavior. (#3556)
* Support for braille displays connected via Bluetooth on a computer running the Widcomm Bluetooth Software. (#2418)
* When editing text in PowerPoint, hyperlinks are now reported. (#3416)
* When in ARIA applications or dialogs on the web, it is now possible to force NVDA to switch to browse mode with NVDA+space allowing document-style navigation of the application or dialog. (#2023)
* In Outlook Express / Windows Mail / Windows Live Mail, NVDA now reports if a message has an attachment or is flagged. (#1594)
* When navigating tables in accessible Java applications, row and column coordinates are now reported, including  column and  row headers if they exist. (#3756)

### Changes

* For Papenmeier braille displays, the move to flat review/focus command has been removed. Users can assign their own keys using the Input Gestures dialog. (#3652)
* NVDA now relies  on the Microsoft VC runtime version 11, which means it can no longer be run on Operating systems older than Windows XP Service Pack 2 or Windows Server 2003 Service Pack 1.
* Punctuation level Some will now speak star (*) and plus (+) characters. (#3614)
* Upgraded eSpeak to version 1.48.04 which includes many language fixes and fixes several crashes. (#3842, #3739, #3860)

### Bug Fixes

* When moving around or selecting cells in Microsoft Excel, NVDA should no longer inappropriately announce the old cell rather than the new cell when Microsoft Excel is slow to move the selection. (#3558)
* NVDA properly handles opening a dropdown list for a cell in Microsoft Excel via the context menu. (#3586)
* New page content in iTunes 11 store pages is now shown properly in browse mode when following a link in the store or when opening the store initially. (#3625)
* Buttons for previewing songs in the iTunes 11 store now show their label in browse mode. (#3638)
* In browse mode in Google Chrome, the labels of check boxes and radio buttons are now rendered correctly. (#1562)
* In Instantbird, NVDA no longer reports useless information every time you move to a contact in the Contacts list. (#2667)
* In browse mode in Adobe Reader, the correct text is now rendered for buttons, etc. where the label has been overridden using a tooltip or other means. (#3640)
* In browse mode in Adobe Reader, extraneous graphics containing the text "mc-ref" will no longer be rendered. (#3645)
* NVDA no longer reports all cells in Microsoft Excel as underlined in their formatting information. (#3669)
* No longer show meaningless characters in browse mode documents such as those found in the Unicode private usage range. In some cases these were stopping more useful labels from being shown. (#2963)
* Input composition for entering east-asian characters no longer fails in PuTTY. (#3432)
* Navigating in a document after a canceled say all no longer results in NVDA sometimes incorrectly announcing that you have left a field (such as a table) lower in the document that the say all never actually spoke. (#3688)
* When using browse mode quick navigation commands  while in say all with skim reading enabled, NVDA more accurately announces the new field; e.g. it now says a heading is a heading, rather than just its text. (#3689)
* The jump to end or start of container quick navigation commands now honor the skim reading during say all setting; i.e. they will no longer cancel the current say all. (#3675)
* Touch gesture names listed in NVDA's Input Gestures dialog are now friendly and localized. (#3624)
* NVDA no longer causes certain programs to crash when moving the mouse over their rich edit (TRichEdit) controls. Programs include Jarte 5.1 and BRfácil. (#3693, #3603, #3581)
* In Internet Explorer and other MSHTML controls, containers such as tables marked as presentation by ARIA are no longer reported to the user. (#3713)
* in Microsoft Word, NVDA no longer inappropriately repeats table row and column information for a cell on a braille display multiple times. (#3702)
* In languages which use a space as a digit group/thousands separator such as French and German, numbers from separate chunks of text are no longer pronounced as a single number. This was particularly problematic for table cells containing numbers. (#3698)
* Braille no longer sometimes fails to update when the system caret is moved in Microsoft Word 2013. (#3784)
* When positioned on the first character of a heading in Microsoft Word, the text communicating it is a heading (including the level) no longer disappears off a braille display. (#3701)
* When a configuration profile is triggered for an application and that application is exited, NVDA no longer sometimes fails to deactivate the profile. (#3732)
* When entering Asian input into a control within NVDA itself (e.g. the browse mode Find dialog), "NVDA" is no longer incorrectly reported in place of the candidate. (#3726)
* The tabs in the Outlook 2013 options dialog are now reported. (#3826)
* Improved support for ARIA live regions in Firefox and other Mozilla Gecko applications:
 * Support for aria-atomic updates and filtering of aria-busy updates. (#2640)
 * Alternative text (such as alt attribute or aria-label) is included if there is no other useful text. (#3329)
 * Live region updates are no longer silenced if they occur at the same time as the focus moves. (#3777)
* Certain presentation elements in Firefox and other Mozilla Gecko applications are no longer inappropriately shown in browse mode (specifically, when the element is marked with aria-presentation but it is also focusable). (#3781)
* A performance improvement when navigating a document in Microsoft Word with spelling errors enabled. (#3785)
* Several fixes to the support for accessible Java applications:
 * The initially focused control in a frame or dialog no longer fails to be reported when the frame or dialog comes to the foreground. (#3753)
 * Unuseful position information is no longer announced for radio buttons (e.g. 1 of 1). (#3754)
 * Better reporting of JComboBox controls (html no longer reported, better reporting of expanded and collapsed states). (#3755)
 * When reporting the text of dialogs, some text that was previously missing is now included. (#3757)
 * Changes to the name, value or description of the focused control is now reported more accurately. (#3770)
* Fix a crash in NVDA seen in Windows 8 when focusing on certain RichEdit controls containing large amounts of text (e.g. NVDA's log viewer, windbg). (#3867)
* On systems with a high DPI display setting (which occurs by default for many modern screens), NVDA no longer routes the mouse to the wrong location in some applications. (#3758, #3703)
* Fixed an occasional problem when browsing the web where NVDA would stop working correctly until restarted, even though it didn't crash or freeze. (#3804)
* A Papenmeier braille display can now be used even if a Papenmeier display has never been connected via USB. (#3712)
* NVDA no longer freezes when the Papenmeier BRAILLEX older models braille display is selected without a display connected.

### Changes for Developers

* AppModules now contain productName and productVersion properties. This info is also now included in Developer Info (NVDA+f1). (#1625)
* In the Python Console, you can now press the tab key to complete the current identifier. (#433)
 * If there are multiple possibilities, you can press tab a second time to choose from a list.

## 2013.3

### New Features

* Form fields are now reported in Microsoft word documents. (#2295)
* NVDA can now announce revision information in Microsoft Word when Track Changes is enabled. Note that Report editor revisions in NVDA's document settings dialog (off by default) must be enabled also for them to be announced. (#1670)
* Dropdown lists in Microsoft Excel 2003 through 2010 are now announced when opened and navigated around. (#3382)
* a new 'Allow Skim Reading in Say All' option in the Keyboard settings dialog allows navigating through a document with browse mode quick navigation and line / paragraph movement commands, while remaining in say all. This option is off by default. (#2766) 
* There is now an Input Gestures dialog to allow simpler customization of the input gestures (such as keys on the keyboard) for NVDA commands. (#1532)
* You can now have different settings for different situations using configuration profiles. Profiles can be activated manually or automatically (e.g. for a particular application). (#87, #667, #1913)
* In Microsoft Excel, cells that are links are now announced as links. (#3042)
* In Microsoft Excel, the existence of comments on a cell is now reported to the user. (#2921)

### Bug Fixes

* Zend Studio now functions the same as Eclipse. (#3420)
* The changed state of certain checkboxes in the Microsoft Outlook 2010 message rules dialog are now reported automatically. (#3063)
* NVDA will now report the pinned state for pinned controls such as tabs in Mozilla Firefox. (#3372)
* It is now possible to bind scripts to keyboard gestures containing Alt and/or Windows keys as modifiers. Previously, if this was done, performing the script would cause the Start Menu or menu bar to be activated. (#3472)
* Selecting text in browse mode documents (e.g. using control+shift+end) no longer causes the keyboard layout to be switched on systems with multiple keyboard layouts installed. (#3472)
* Internet Explorer should no longer crash or become unusable when closing NVDA. (#3397)
* Physical movement and other events on some newer computers are no longer treated as inappropriate key presses. Previously, this silenced speech and sometimes triggered NVDA commands. (#3468)
* NVDA now behaves as expected in Poedit 1.5.7. Users using earlier versions will need to update. (#3485)
* NVDA can now read protected documents in Microsoft Word 2010,  no longer causing Microsoft Word to crash. (#1686)
* If an unknown command line switch is given when launching the NVDA distribution package, it no longer causes an endless loop of error message dialogs. (#3463)
* NVDA no longer fails to report alt text of graphics and objects in Microsoft Word if the alt text contains quotes or other non-standard characters. (#3579)
* The number of items for certain horizontal lists in Browse mode is now correct. Previously it may have been double the actual amount. (#2151)
* When pressing control+a in a Microsoft Excel worksheet, the updated selection will now be reported. (#3043)
* NVDA can now correctly read XHTML documents in Microsoft Internet Explorer and other MSHTML controls. (#3542)
* Keyboard settings dialog: if no key has been chosen to be used as the NVDA key, an error is presented to the user when dismissing the dialog. At least one key must be chosen for proper usage of NVDA. (#2871)
* In Microsoft Excel, NVDA now announces merged cells differently to multiple selected cells. (#3567)
* The browse mode cursor is no longer positioned incorrectly when leaving a dialog or application inside the document. (#3145)
* Fixed an issue where the HumanWare Brailliant BI/B series braille display driver wasn't presented as an option in the Braille Settings dialog on some systems, even though such a display was connected via USB.
* NVDA no longer fails  to switch to screen review when the navigator object has no actual screen location. In this case the review cursor is now placed at the top of the screen. (#3454)
* Fixed an issue which caused the Freedom Scientific braille display driver to fail when the port was set to USB in some circumstances. (#3509, #3662)
* Fixed an issue where keys on Freedom Scientific braille displays weren't detected in some circumstances. (#3401, #3662)

### Changes for Developers

* You can specify the category to be displayed to the user for scripts using the scriptCategory attribute on ScriptableObject classes and the category attribute on script methods. See the documentation for baseObject.ScriptableObject for more details. (#1532)
* config.save is deprecated and may be removed in a future release. Use config.conf.save instead. (#667)
* config.validateConfig is deprecated and may be removed in a future release. Add-ons which need this should provide their own implementation. (#667, #3632)

## 2013.2

### New Features

* Support for the Chromium Embedded Framework, which is a web browser control used in several applications. (#3108)
* New eSpeak voice variant: Iven3.
* In Skype, new chat messages are reported automatically while the conversation is focused. (#2298)
* Support for Tween, including reporting of tab names and less verbosity when reading tweets.
* You can now disable displaying of NVDA messages on a braille display by setting the message timeout to 0 in the Braille Settings dialog. (#2482)
* In the Add-ons Manager, there is now a Get Add-ons button to open the NVDA Add-ons web site where you can browse and download available add-ons. (#3209)
* In the NVDA Welcome dialog which always appears the first time you run NVDA, you can now specify whether NVDA starts automatically after you log on to Windows. (#2234)
* Sleep mode is automatically enabled when using Dolphin Cicero. (#2055)
* The Windows x64 version of Miranda IM/Miranda NG is now supported. (#3296)
* Search suggestions in the Windows 8.1 Start Screen are automatically reported. (#3322)
* Support for navigating and editing spreadsheets in Microsoft Excel 2013. (#3360)
* The Freedom Scientific Focus 14 Blue and Focus 80 Blue braille displays, as well as the Focus 40 Blue in certain configurations that weren't supported previously, are now supported when connected via Bluetooth. (#3307)
* Auto complete suggestions are now reported in Outlook 2010. (#2816)
* New braille translation tables: English (U.K.) computer braille, Korean grade 2, Russian braille for computer code.
* New language: Farsi. (#1427)

### Changes

* On a touch screen, performing a single finger flick left or right when in object mode now moves previous or next through all objects, not just those in the current container. Use 2-finger flick left or right to perform the original action of moving to the previous or next object in the current container.
* the Report layout tables checkbox found in the Browse Mode settings dialog has now been renamed to Include layout tables to reflect that quick navigation also will not locate them if the checkbox is unchecked. (#3140)
* Flat review has been replaced with object, document and screen review modes. (#2996)
 * Object review reviews text just within the navigator object, document review reviews all text in a browse mode document (if any) and screen review reviews text on the screen for the current application.
 * The commands that previously move to/from flat review now toggle between these new review modes.
 * The navigator object automatically follows the review cursor such that it remains the deepest object at the position of the review cursor when in document or screen review modes.
 * After switching to screen review mode, NVDA will stay in this mode until you explicitly switch back to document or object review mode.
 * When in document or object review mode, NVDA may automatically switch between these two modes depending on whether you are moving around a browse mode document or not.
* Updated liblouis braille translator to 2.5.3. (#3371)

### Bug Fixes

* Activating an object now announces the action before the activation, rather than the action after the activation (e.g. expand when expanding rather than collapse). (#2982)
* More accurate reading and cursor tracking in  various input fields for recent versions of Skype, such as chat and search fields. (#1601, #3036)
* In the Skype recent conversations list, the number of new events is now read for each conversation if relevant. (#1446)
* Improvements to cursor tracking and reading order for right-to-left text written to the screen; e.g. editing Arabic text in  Microsoft Excel. (#1601) 
* Quick navigation to buttons and form fields will now locate links marked as buttons for accessibility purposes in Internet Explorer. (#2750)
* In browse mode, the content inside tree views is no longer rendered, as a flattened representation isn't useful. You can press enter on a tree view to interact with it in focus mode. (#3023)
* Pressing alt+downArrow or alt+upArrow to expand a combo box while in focus mode no longer incorrectly switches to browse mode. (#2340)
* In Internet Explorer 10, table cells no longer activate focus mode, unless they have been explicitly made focusable by the web author. (#3248)
* NVDA no longer fails to start if the system time is earlier than the last check for an update. (#3260)
* If a progress bar is shown on a braille display, the braille display is updated when the progress bar changes. (#3258)
* In browse mode in Mozilla applications, table captions are no longer rendered twice. In addition, the summary is rendered when there is also a caption. (#3196)
* When changing input languages in Windows 8, NVDA now speaks the correct language rather than the previous one.
* NVDA now announces IME conversion mode changes in Windows 8.
* NVDA no longer announces garbage on the Desktop when the Google Japanese or Atok IME input methods are in use. (#3234)
* In Windows 7 and above, NVDA no longer inappropriately announces speech recognition or touch input as a keyboard language change.
* NVDA no longer announces a particular special character (0x7f) when pressing control+backspace in some editors when speak typed characters is enabled. (#3315)
* eSpeak no longer inappropriately changes in pitch, volume, etc. when NVDA reads text containing certain control characters or XML. (#3334) (regression of #437)
* In Java applications, changes to the label or value of the focused control are now announced automatically, and are reflected when subsequently querying the control. (#3119)
* In Scintilla controls, lines are now reported correctly when word wrap is enabled. (#885)
* In Mozilla applications, the name of read-only list items is now correctly reported; e.g. when navigating tweets in focus mode on twitter.com. (#3327)
* Confirmation dialogs in Microsoft Office 2013 now have their content automatically read when they appear. 
* Performance improvements when navigating certain tables in Microsoft Word. (#3326)
* NVDA's table navigation commands (control+alt+arrows) function better in certain Microsoft Word tables where a cell spans multiple rows.
* If the Add-ons Manager is already open, activating it again (either from the Tools menu or by opening an add-on file) no longer fails or makes it impossible to close the Add-ons Manager. (#3351)
* NVDA no longer freezes in certain dialogs when Japanese or Chinese Office 2010 IME is in use. (#3064)
* Multiple spaces are no longer compressed to just one space on braille displays. (#1366)
* Zend Eclipse PHP Developer Tools now functions the same as Eclipse. (#3353)
* In Internet Explorer, It is again not necessary to press tab to interact with an embedded object (such as Flash content) after pressing enter on it. (#3364)
* When editing text in Microsoft PowerPoint, the last line is no longer reported as the line above, if the final line is blank. (#3403)
* In Microsoft PowerPoint, objects are no longer sometimes spoken twice when you select them or choose to edit them. (#3394)
* NVDA no longer causes Adobe Reader to crash or freeze for certain badly formed PDF documents containing rows outside of tables. (#3399)
* NVDA now correctly detects the next slide with focus when deleting a slide in Microsoft PowerPoint's thumbnails view. (#3415)

### Changes for Developers

* windowUtils.findDescendantWindow has been added to search for a descendant window (HWND) matching the specified visibility, control ID and/or class name.
* The remote Python console no longer times out after 10 seconds while waiting for input. (#3126)
* Inclusion of the bisect module in binary builds is deprecated and may be removed in a future release. (#3368)
 * Add-ons which depend on bisect (including the urllib2 module) should be updated to include this module.

## 2013.1.1

This release fixes the problem where NVDA crashed when started if configured to use the Irish language, as well as including updates to translations and some other bug fixes.

### Bug Fixes

* Correct characters are produced when typing in NVDA's own user interface while using a Korean or Japanese input method while it is the default method. (#2909)
* In Internet Explorer and other MSHTML controls, fields marked as containing an invalid entry are now handled correctly. (#3256)
* NVDA no longer crashes when started if it is configured to use the Irish language.

## 2013.1

Highlights of this release include a more intuitive and consistent laptop keyboard layout; basic support for Microsoft PowerPoint; support for long descriptions in web browsers; and support for input of computer braille for braille displays which have a braille keyboard.

### Important

#### New Laptop Keyboard Layout

The laptop keyboard layout has been completely redesigned in order to make it more intuitive and consistent.
The new layout uses the arrow keys in combination with the NVDA key and other modifiers for review commands.

Please note the following changes to commonly used commands:

| Name |Key|
|---|---|
|Say all |NVDA+a|
|Read current line |NVDA+l|
|Read current text selection |NVDA+shift+s|
|Report status bar |NVDA+shift+end|

In addition, among other changes, all of the object navigation, text review, mouse click and synth settings ring commands have changed.
Please see the [Commands Quick Reference](keyCommands.html) document for the new keys.

### New Features

* Basic support for editing and reading Microsoft PowerPoint presentations. (#501)
* Basic support for reading and writing messages in Lotus Notes 8.5. (#543)
* Support for automatic language switching when reading documents in Microsoft Word. (#2047) 
* In Browse mode for MSHTML (e.g. Internet Explorer) and Gecko (e.g. Firefox), the existence of long descriptions are now announced. It's also possible to open the long description in a new window by pressing NVDA+d. (#809)
* Notifications in Internet Explorer 9 and above are now spoken (such as content blocking or file downloads). (#2343)
* Automatic reporting of table row and column headers is now supported for browse mode documents in Internet Explorer and other MSHTML controls. (#778)
* New language: Aragonese, Irish
* New braille translation tables: Danish grade 2, Korean grade 1. (#2737)
* Support for braille displays connected via bluetooth on a computer running the Bluetooth Stack for Windows by Toshiba. (#2419)
* Support for port selection when using Freedom Scientific displays (Automatic, USB or Bluetooth).
* Support for the BrailleNote family of notetakers from HumanWare when acting as a braille terminal for a screen reader. (#2012)
* Support for older models of Papenmeier BRAILLEX braille displays. (#2679)
* Support for input of computer braille for braille displays which have a braille keyboard. (#808)
* New keyboard settings that allow  the choice for whether NVDA should interrupt speech for typed characters and/or the Enter key. (#698)
* Support for several browsers based on Google Chrome: Rockmelt, BlackHawk, Comodo Dragon and SRWare Iron. (#2236, #2813, #2814, #2815)

### Changes

* Updated liblouis braille translator to 2.5.2. (#2737)
* The laptop keyboard layout has been completely redesigned in order to make it more intuitive and consistent. (#804)
* Updated eSpeak speech synthesizer to 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Bug Fixes

* The quick navigation keys for jumping to the next or previous separator in Browse Mode now work in Internet Explorer and other MSHTML controls. (#2781)
* If NVDA falls back to eSpeak or no speech due to the configured speech synthesizer failing when NVDA starts, the configured choice is no longer automatically set to the fallback synthesizer. This means that now, the original synthesizer will be tried again next time NVDA starts. (#2589)
* If NVDA falls back to no braille due to the configured braille display failing when NVDA starts, the configured display is no longer automatically set to no braille. This means that now, the original display will be tried again next time NVDA starts. (#2264)
* In browse mode in Mozilla applications, updates to tables are now rendered correctly. For example, in updated cells, row and column coordinates are reported and table navigation works as it should. (#2784)
* In browse mode in web browsers, certain clickable unlabelled graphics which weren't previously rendered are now rendered correctly. (#2838)
* Earlier and newer versions of SecureCRT are now supported. (#2800)
* For input  methods such as Easy Dots IME under XP, the reading string is now correctly reported.
* The candidate list in the Chinese Simplified Microsoft Pinyin input method under Windows 7 is now correctly read when changing pages with left and right arrow, and when first opening it with Home.
* When custom symbol pronunciation information is saved, the advanced "preserve" field is no longer removed. (#2852)
* When disabling automatic checking for updates, NVDA no longer has to be restarted in order for the change to fully take effect.
* NVDA no longer fails to start if an add-on cannot be removed due to its directory currently being in use by another application. (#2860)
* Tab labels in DropBox's preferences dialog can now be seen with Flat Review.
* If the input language is changed to something other than the default, NVDA now detects keys correctly for commands and input help mode.
* For languages such as German where the + (plus) sign is a single key on the keyboard, it is now possible to bind commands to it by using the word "plus". (#2898)
* In Internet Explorer and other MSHTML controls, block quotes are now reported where appropriate. (#2888)
* The HumanWare Brailliant BI/B series braille display driver can now be selected when the display is connected via Bluetooth but has never been connected via USB.
* Filtering elements in the Browse Mode Elements list with uppercase filter text now returns case-insensitive results just like lowercase rather than nothing at all. (#2951)
* In Mozilla browsers, browse mode can again be used when Flash content is focused. (#2546)
* When using a contracted braille table and expand to computer braille for the word at the cursor is enabled, the braille cursor is now positioned correctly when located after a word wherein a character is represented by multiple braille cells (e.g. capital sign, letter sign, number sign, etc.). (#2947)
* Text selection is now correctly shown on a braille display in applications such as Microsoft word 2003 and Internet Explorer edit controls.
* It is again possible to select text in a backward direction in Microsoft Word while Braille is enabled.
* When reviewing,  backspacing or deleting characters  In Scintilla edit controls, NVDA correctly announces multibyte characters. (#2855)
* NVDA will no longer fail to install when the user's profile path contains certain multibyte characters. (#2729)
* Reporting of groups for List View controls (SysListview32) in 64-bit applications no longer causes an error.
* In browse mode in Mozilla applications, text content is no longer incorrectly treated as editable in some rare cases. (#2959)
* In IBM Lotus Symphony and OpenOffice, moving the caret now moves the review cursor if appropriate.
* Adobe Flash content is now accessible in Internet Explorer in Windows 8. (#2454)
* Fixed Bluetooth support for Papenmeier Braillex Trio. (#2995)
* Fixed inability to use certain Microsoft Speech API version 5 voices such as Koba Speech 2 voices. (#2629)
* In applications using the Java Access Bridge, braille displays are now updated correctly when the caret moves in editable text fields . (#3107)
* Support the form landmark in browse mode documents that support landmarks. (#2997) 
* The eSpeak synthesizer driver now handles reading by character more appropriately (e.g. announcing a foreign letter's name or value rather than just its sound or generic name). (#3106)
* NVDA no longer fails to copy user settings for use on logon and other secure screens when the user's profile path contains non-ASCII characters. (#3092)
* NVDA no longer freezes when using Asian character input in some .NET applications. (#3005)
* it is now possible to use browse mode for pages in Internet Explorer 10 when in standards mode; e.g. [www.gmail.com](http://www.gmail.com) login page. (#3151)

### Changes for Developers

* Braille display drivers can now support manual port selection. (#426)
 * This is most useful for braille displays which support connection via a legacy serial port.
 * This is done using the getPossiblePorts class method on the BrailleDisplayDriver class.
* Braille input from braille keyboards is now supported. (#808)
 * Braille input is encompassed by the brailleInput.BrailleInputGesture class or a subclass thereof.
 * Subclasses of braille.BrailleDisplayGesture (as implemented in braille display drivers) can also inherit from brailleInput.BrailleInputGesture. This allows display commands and braille input to be handled by the same gesture class.
* You can now use comHelper.getActiveObject to get an active COM object from a normal process when NVDA is running with the UIAccess privilege. (#2483)

## 2012.3

Highlights of this release include support for Asian character input; experimental support for touch screens on Windows 8; reporting of page numbers and improved support for tables in Adobe Reader; table navigation commands in focused table rows and Windows list-view controls; support for several more braille displays; and reporting of row and column headers in Microsoft Excel.

### New Features

* NVDA can now support Asian character input using IME and text service input methods in all applications, Including:
 * Reporting and navigation of candidate lists;
 * Reporting and navigation of composition strings; and
 * Reporting of reading strings.
* The presence of underline and strikethrough is now reported in Adobe Reader documents. (#2410)
* When the Windows Sticky Keys function is enabled, the NVDA modifier key will now behave like other modifier keys. This allows you to use the NVDA modifier key without needing to hold it down while you press other keys. (#230)
* Automatic reporting of column and row headers is now supported in Microsoft Excel. Press NVDA+shift+c to set the row containing column headers and NVDA+shift+r to set the column containing row headers. Press either command twice in quick succession to clear the setting. (#1519)
* Support for HIMS Braille Sense, Braille EDGE and SyncBraille braille displays. (#1266, #1267)
* When Windows 8 Toast notifications appear, NVDA will report them if reporting of help balloons is enabled. (#2143)
* Experimental support for Touch screens on Windows 8, including:
 * Reading text directly under your finger while moving it around
 * Many gestures for performing object navigation, text review, and other NVDA commands.
* Support for VIP Mud. (#1728)
* In Adobe Reader, if a table has a summary, it is now presented. (#2465)
* In Adobe Reader, table row and column headers can now be reported. (#2193, #2527, #2528)
* New languages: Amharic, Korean, Nepali, Slovenian.
* NVDA can now read auto complete suggestions when entering email addresses in Microsoft Outlook 2007. (#689)
* New eSpeak voice variants: Gene, Gene2. (#2512)
* In Adobe Reader, page numbers can now be reported. (#2534)
 * In Reader XI, page labels are reported where present, reflecting changes to page numbering in different sections, etc. In earlier versions, this is not possible and only sequential page numbers are reported.
* It is now possible to reset NVDA's configuration to factory defaults either by pressing NVDA+control+r three times quickly or by choosing Reset to Factory Defaults from the NVDA menu. (#2086)
* Support for the Seika Version 3, 4 and 5 and Seika80 braille displays from Nippon Telesoft. (#2452)
* The first and last top routing buttons on Freedom Scientific PAC Mate and Focus Braille displays can now be used to scroll  backward and forward. (#2556)
* Many more features are supported on Freedom Scientific Focus Braille displays such as advance bars, rocker bars and certain dot combinations for common actions. (#2516)
* In applications using IAccessible2 such as Mozilla applications, table row and column headers can now be reported outside of browse mode. (#926)
* Preliminary support for the document control in Microsoft Word 2013. (#2543)
* Text alignment can now be reported in applications using IAccessible2 such as Mozilla applications. (#2612)
* When a table row or standard Windows list-view control with multiple columns is focused, you can now use the table navigation commands to access individual cells. (#828)
* New braille translation tables: Estonian grade 0, Portuguese 8 dot computer braille, Italian 6 dot computer braille. (#2319, #2662)
* If NVDA is installed on the system, directly opening an NVDA add-on package (e.g. from Windows Explorer or after downloading in a web browser) will install it into NVDA. (#2306)
* Support for newer models of Papenmeier BRAILLEX braille displays. (#1265)
* Position information (e.g. 1 of 4) is now reported for Windows Explorer list items on Windows 7 and above. This also includes any UIAutomation controls that support the itemIndex and itemCount custom properties. (#2643)

### Changes

* In the NVDA Review Cursor preferences dialog, the Follow keyboard focus option has been renamed to Follow system focus for consistency with terminology used elsewhere in NVDA.
* When braille is tethered to review and the cursor is on an object which is not a text object (e.g. an editable text field), cursor routing keys will now activate the object. (#2386)
* The Save Settings On Exit option is now on by default for new configurations.
* When updating a previously installed copy of NVDA, the desktop shortcut key is no longer forced back to control+alt+n if it was manually changed to something different by the user. (#2572)
* The add-ons list in the Add-ons Manager now shows the package name before its status. (#2548)
* If installing the same or another version of a currently installed add-on, NVDA will ask if you wish to update the add-on, rather than just showing an error and aborting installation. (#2501)
* Object navigation commands (except the report current object command) now report with less verbosity. You can still obtain the extra information by using the report current object command. (#2560)
* Updated liblouis braille translator to 2.5.1. (#2319, #2480, #2662, #2672)
* The NVDA Key Commands Quick Reference document has been renamed to Commands Quick Reference, as it now includes touch commands as well as keyboard commands.
* The Elements list in Browse mode will now remember the last element type shown (e.g. links, headings or landmarks) each time the dialog is shown within the same session of NVDA. (#365)
* Most Metro apps in Windows 8 (e.g. Mail, Calendar) no longer activate Browse Mode for the entire app.
* Updated Handy Tech BrailleDriver COM-Server to 1.4.2.0.

### Bug Fixes

* In Windows Vista and later, NVDA no longer incorrectly treats the Windows key as being held down when unlocking Windows after locking it by pressing Windows+l. (#1856)
* In Adobe Reader, row headers are now correctly recognised as table cells; i.e. coordinates are reported and they can be accessed using table navigation commands. (#2444)
* In Adobe Reader, table cells spanning more than one column and/or row are now handled correctly. (#2437, #2438, #2450)
* The NVDA distribution package now checks its integrity before executing. (#2475)
* Temporary download files are now removed if downloading of an NVDA update fails. (#2477)
* NVDA will no longer freeze when it is running as an administrator while copying the user configuration to the system configuration (for use on Windows logon and other secure screens). (#2485)
* Tiles on the Windows 8 Start Screen are now presented better in speech and braille. The name is no longer repeated, unselected is no longer reported on all tiles, and live status information is presented  as the description of the tile (e.g. current temperature for the Weather tile).
* Passwords are no longer announced when reading password fields in Microsoft Outlook and other standard edit controls that are marked as protected. (#2021)
* In Adobe Reader, changes to form fields are now correctly reflected in browse mode. (#2529)
* Improvements to support for the Microsoft Word Spell Checker, including more accurate reading of the current spelling error, and the ability to support the spell checker when running an Installed copy of NVDA on Windows Vista or higher.
* Add-ons which include files containing non-English characters can now be installed correctly in most cases. (#2505)
* In Adobe Reader, the language of text is no longer lost when it is updated or scrolled to. (#2544)
* When installing an add-on, the confirmation dialog now correctly shows the localized name of the add-on if available. (#2422)
* In applications using UI Automation (such as .net and Silverlight applications), the calculation of numeric values for controls such as sliders has been corrected. (#2417)
* The configuration for reporting of progress bars is now honoured for the indeterminate progress bars displayed by NVDA when installing, creating a portable copy, etc. (#2574)
* NVDA commands can no longer be executed from a braille display while a secure Windows screen (such as the Lock screen) is active. (#2449)
* In browse mode, braille is now updated if the text being displayed changes. (#2074)
* When on a secure Windows screen such as the Lock screen, messages from applications speaking or displaying braille directly via NVDA are now ignored.
* In Browse mode, it is no longer possible to  fall off the bottom of the document with the right arrow key when on the final character, or by jumping to the end of a container when that container is the last item in the document. (#2463)
* Extraneous content is no longer incorrectly included when reporting the text of dialogs in web applications (specifically, ARIA dialogs with no aria-describedby attribute). (#2390)
* NVDA no longer incorrectly reports or locates certain edit fields in MSHTML documents (e.g. Internet Explorer), specifically where an explicit ARIA role has been used by the web page author. (#2435)
* The backspace key is now handled correctly when speaking typed words in Windows command consoles. (#2586)
* Cell coordinates in Microsoft Excel are now shown again in Braille.
* In Microsoft Word, NVDA no longer leaves you stuck on a paragraph with list formatting when trying to navigate out over a bullet or number with left arrow or control + left arrow. (#2402)
* In browse mode in Mozilla applications, the items in certain list boxes (specifically, ARIA list boxes) are no longer incorrectly rendered.
* In browse mode in Mozilla applications, certain controls that were rendered with an incorrect label or just whitespace are now rendered with the correct label.
* In browse mode in Mozilla applications, some extraneous whitespace has been eliminated.
* In browse mode in web browsers, certain graphics that are explicitly marked as presentational (specifically, with an alt="" attribute) are now correctly ignored.
* In web browsers, NVDA now hides content which is marked as hidden from screen readers (specifically, using the aria-hidden attribute). (#2117)
* Negative currency amounts (e.g. -$123) are now correctly spoken as negative, regardless of symbol level. (#2625)
* During say all, NVDA will no longer incorrectly revert to the default language where a line does not end a sentence. (#2630)
* Font information is now correctly detected in Adobe Reader 10.1 and later. (#2175)
* In Adobe Reader, if alternate text is provided, only that text will be rendered. Previously, extraneous text was sometimes included. (#2174)
* Where a document contains an application, the content of the application is no longer included in browse mode. This prevents unexpectedly moving inside the application when navigating. You can interact with the application in the same way as for embedded objects. (#990)
* In Mozilla applications, the value of spin buttons is now correctly reported when it changes. (#2653)
* Updated support for Adobe Digital Editions so that it works in version 2.0. (#2688)
* Pressing NVDA+upArrow while on a combo box in Internet Explorer and other MSHTML documents will no longer incorrectly read all items. Rather, just the active item will be read. (#2337)
* Speech dictionaries will now properly save when using a number (#) sign within the pattern or replacement fields. (#961)
* Browse mode for MSHTML documents (e.g. Internet Explorer) now correctly displays visible content contained within hidden content (specifically, elements with a style of visibility:visible inside an element with style visibility:hidden). (#2097)
* Links in Windows XP's Security Center no longer report random junk after their names. (#1331)
* UI Automation text controls (e.g.  the search field in the Windows 7 Start Menu) are now  correctly announced when moving the mouse over them rather than staying silent.
* Keyboard layout changes are no longer reported during say all, which was particularly problematic for multilingual documents including Arabic text. (#1676)
* The entire content of some UI Automation editable text controls (e.g. the Search Box in the Windows 7/8 Start Menu) is no longer announced every time it changes.
* When moving between groups on the Windows 8 start screen, unlabeled groups no longer announce their first tile as the name of the group. (#2658)
* When opening the Windows 8 start screen, the focus is correctly placed on the first tile, rather than jumping to the root of the start screen which can confuse navigation. (#2720)
* NVDA will no longer fail to start when the user's profile path contains certain multibyte characters. (#2729)
* In browse mode in Google Chrome, the text of tabs is now rendered correctly.
* In browse mode, menu buttons are now reported correctly.
* In OpenOffice.org/LibreOffice Calc, reading spreadsheet cells now works correctly. (#2765)
* NVDA can again function in the Yahoo! Mail message list when used from Internet Explorer. (#2780)

### Changes for Developers

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

This release addresses  several potential security issues (by upgrading Python to 2.7.3).

## 2012.2

Highlights of this release include an in-built installer and  portable  creation feature, automatic updates, easy management of new NVDA add-ons, announcement of graphics in Microsoft Word, support for Windows 8 Metro style apps, and several important bug fixes. 

### New Features

* NVDA can now automatically check for, download and install updates. (#73)
* Extending NVDA's functionality  has been made easier with the addition of an Add-ons Manager (found under Tools in the NVDA menu) allowing you to install and uninstall new NVDA add-on packages (.nvda-addon files) containing plugins and drivers. Note the Add-on manager does not show older custom plugins and drivers manually copied in to your configuration directory. (#213)
* Many more common NVDA features now work in Windows 8 Metro style apps when using an installed release  of NVDA, including speaking of typed characters, and browse mode for web documents (includes support for metro version of Internet Explorer 10). Portable copies of NVDA cannot access metro style apps. (#1801) 
* In browse mode documents (Internet Explorer, Firefox, etc.), you can now  jump to the start and past the end of certain containing elements (such as lists and tables) with shift+, and , respectively. (#123)
* New language: Greek.
* Graphics and alt text are now reported in Microsoft Word Documents. (#2282, #1541)

### Changes

* Announcement of cell coordinates in Microsoft Excel is now after the content rather than before, and is now only included   if the report tables and report table cell coordinates settings are enabled in the Document formatting settings dialog. (#320)
* NVDA is now distributed in one package. Rather than separate portable and installer versions, there is now just one file that, when run, will start a temporary copy of NVDA and will allow you to install or generate a portable distribution. (#1715)
* NVDA is now always installed in to Program Files on all systems. Updating a previous install will also automatically move it if it was not previously installed there.

### Bug Fixes

* With auto language switching enabled, Content such as alt text for graphics and labels for other certain controls in Mozilla Gecko (e.g. Firefox) are now reported in the correct language if marked up appropriately.
* SayAll in BibleSeeker (and other TRxRichEdit controls) no longer stops in the middle of a passage.
* Lists found in the Windows 8 Explorer file properties (permitions tab) and in Windows 8 Windows Update now read correctly.
* Fixed possible freezes in MS Word which would result when it took more than 2 seconds to fetch text from a document (extremely long lines or tables of contents). (#2191)
* Detection of word breaks now works correctly where whitespace is followed by certain punctuation. (#1656)
* In browse mode in Adobe Reader, it is now possible to navigate to headings without a level using quick navigation and the Elements List. (#2181)
* In Winamp, braille is now correctly updated when you move to a different item in the Playlist Editor. (#1912)
* The tree in the Elements List (available for browse mode documents) is now properly sized to show  the text of each element. (#2276)
* In applications using the Java Access Bridge, editable text fields are now presented correctly in braille. (#2284)
* In applications using the java Access Bridge, editable text fields no longer report strange characters in certain circumstances. (#1892)
* In applications using the Java Access Bridge, when at the end of an editable text field, the current line is now reported correctly. (#1892)
* In browse mode in applications using Mozilla Gecko 14 and later (e.g. Firefox 14), quick navigation now works for block quotes and embedded objects. (#2287)
* In Internet Explorer 9, NVDA no longer reads unwanted content when focus moves inside certain landmarks or focusable elements (specifically, a div element which is focusable or has an ARIA landmark role).
* The NVDA icon for the NVDA Desktop and Start Menu shortcuts is now displayed correctly on 64 bit editions of Windows. (#354)

### Changes for Developers

* Due to the replacement of the previous NSIS installer for NVDA with a built-in installer in Python, it is no longer necessary for translaters to maintain a langstrings.txt file for the installer. All localization strings are now managed by gettext po files.

## 2012.1

Highlights of this release include features for more fluent reading of braille; indication of document formatting in braille; access to much more formatting information and improved performance in Microsoft Word; and support for the iTunes Store.

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
* For the convenience of third party developers, app modules as well as global plugins can now be reloaded without restarting NVDA. Use tools -> Reload plugins in the NVDA menu or NVDA+control+f3. (#544)
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
* Add the ability to view the current log file for NVDA. it can be found in the NVDA menu -> Tools
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
