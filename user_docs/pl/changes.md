# Co nowego w NVDA

## 2024.4

W tej wersji dodano dużo poprawek dla Microsoft Office, brajla, i wsparcie formatowania dokumentów.

W programach Word i Excel, można dwukrotnie nacisnąć skrót klawiszowy dla odczytu komentarza lub notatki, w celu pokazania zawartości w trybie czytania.
Od teraz można używać poleceń do zaznaczania za pomocą kursora przeglądu w programie Powerpoint.
NVDA więcej nie pokazuje bezsensowne znaki podczas wyświetlania tekstu nagłówka wiersza lub kolumny w tabelach w programie Word podczas używania modelu obiektowego.

Od teraz można konfigurować oddzielnie zgłaszanie atrybutów czcionki mową i brajlem.

Dodano nowe ustawienie, pozwalające ustawić czas wygasania do wypełnienia polecenia wymagającego wielokrotnego naciskania klawisza, takiego jak wymawianie daty i czasu.

Od teraz można ustawić sposó, w jaki NVDA wyświetli formatowanie tekstu, a także jak mają być wyświetlane początek i koniec akapitu.
NVDA od teraz może wymawiać znak pod kursorem podczas naciskania klawisza routing.
Niezawodność klawiszy routing zostałą ulepszona, a także dodano ich wsparcie w programie Powerpoint.
Wszystkie linie komórek od teraz będą używane podczas używania wielowierszowego monitora brajlowskiego za pomocą protokołu Hid braille.
NVDA już nie jest niestabilny po ponownym uruchomieniu podczas automatycznego skanowania monitorów brajlowskich używających Bluetooth.

Minimalna wymagana wersja programu Poedit działająca z NVDA od teraz to wersja 3.5.

eSpeak NG został zaktualizowany z dodanymi językami farerski i Xextan.

LibLouis został zaktualizowany, dodając nowe tablice brajlowskie dla tajskiego i międzynarodowego greckiego z akcentowanymi literami w jednej komórce.

Naprawiono także dużo błędów, włączając w to błędy z śledzeniem myszy w programie Firefox, a także trybem mowy na żądanie.

### Nowe funkcje

* Nowe funkcje brajla:
  * Możliwa jest teraz zmiana sposobu, w jaki NVDA wyświetla niektóre atrybuty formatowania tekstu w brajlu.
    Dostępne opcje to:
    * Liblouis (domyślnie): Używa znaczników formatowania zdefiniowanych w wybranej tablicy brajlowskiej.
    * Znaczniki: Używa znaczników początkowych i końcowych do oznaczania początku i końca określonych atrybutów czcionki. (#16864)
  * Gdy włączona jest opcja "Czytaj akapitami", NVDA może być teraz skonfigurowana tak, aby wskazywała początek akapitów w alfabecie Braille'a. (#16895, @nvdaes)
  * Podczas naciskania klawisza routing, NVDA może teraz automatycznie wymawiać znak znajdujący się pod kursorem. (#8072, @LeonarddeR)
    * Ta opcja jest domyślnie wyłączona.
      Możesz włączyć opcję "wymawiaj znak gdy naciśnięty jest klawisz routing" w ustawieniach brajla NVDA.
* Polecenie komentarza w programie Microsoft Word i polecenie notatek w programie Microsoft Excel można teraz nacisnąć dwukrotnie, aby wyświetlić komentarz lub notatkę w wiadomości, którą można przeglądać. (#16800, #16878, @Cary-Rowen)
* NVDA można teraz skonfigurować tak, aby zgłąszać atrybuty czcionek mową i brajlem oddzielnie. (#16755)
* Limit czasu na wykonanie wielu naciśnięć jest teraz konfigurowalny; Może to być szczególnie przydatne dla osób z zaburzeniami zręczności. (#11929, @CyrilleB79)

### Zmiany

* Opcje wiersza poleceń '-c'/'--config-path' i '--disable-addons' są teraz respektowane podczas uruchamiania aktualizacji z poziomu NVDA. (#16937)
* Aktualizacje komponentów:
  * Zaktualizowano LibLouis Braille translator do wersji [3.31.0](https://github.com/liblouis/liblouis/releases/tag/v3.31.0). (#17080, @LeonarddeR, @codeofdusk)
    * Poprawiono tłumaczenie liczb w hiszpańskim brajlu.
    * Nowe tablice brajlowskie:
      * Tajski pismo pełne
      * Grecki alfabet Braille'a (jednokomórkowe litery akcentowane)
    * Zmieniono nazwy tablic brajlowskich:
      * Nazwa "tajski sześciopunktowy" została zmieniona na "Tajski pismo podstawowe" ze względu na spójność.
      * Istniejąca tablica "Grecki międzynarodowy alfabet Braille'a" została przemianowana na "Grecki międzynarodowy alfabet Braille'a (2-komórkowe litery akcentowane)", aby wyjaśnić różnicę między dwoma systemami zapisu greki.
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit '961454ff'. (#16775)
    * Dodano nowe języki: farerski i xextan.
* W przypadku korzystania z wielowierszowego monitora brajlowskiego za pośrednictwem standardowego sterownika brajlowskiego HID, używane będą wszystkie wiersze komórek. (#16993, @alexmoon)
* Stabilność obsługi Poedit w NVDA została poprawiona z efektem ubocznym, że minimalną wymaganą wersją Poedit jest od teraz wersja 3.5. (#16889, @LeonarddeR)

### Poprawki błędów

* Poprawki brajla:
  * Od teraz jest możliwe używanie klawiszy routing monitora brajlowskiego do przesuwania kursora tekstowego w programie Microsoft PowerPoint. (#9101)
  * Podczas uzyskiwania dostępu do programu Microsoft Word bez automatyzacji interfejsu użytkownika, NVDA nie wyprowadza już znaków śmieci w nagłówkach tabeli zdefiniowanych za pomocą poleceń ustawiania wiersza i nagłówka kolumny. (#7212)
  * Sterownik Seika Notetaker teraz poprawnie generuje dane wejściowe Braille'a dla spacji, backspace i kropek z gestami spacji/backspace. (#16642, @school510587)
  * Klawisze routing są teraz znacznie bardziej niezawodne, gdy wiersz zawiera jeden lub więcej selektorów odmian Unicode lub zdekomponowanych znaków. (#10960, @mltony, @LeonarddeR)
  * NVDA nie zgłasza już błędu podczas przesuwania monitora brajlowskiego do przodu w niektórych pustych pól edycyjnych. (#12885)
  * NVDA nie jest już niestabilna po ponownym uruchomieniu NVDA podczas automatycznego skanowania Bluetooth w poszukiwaniu monitorów brajlowskich. (#16933)
* Teraz można używać poleceń do zaznaczania tekstu kursora przeglądu w programie Microsoft PowerPoint. (#17004)
* W trybie mowy na żądanie, NVDA nie mówi już, gdy wiadomość jest otwierana w Outlooku, gdy nowa strona jest ładowana w przeglądarce lub gdy wyświetla nowy slajd w pokazie slajdów PowerPoint. (#16825, @CyrilleB79)
* W przeglądarce Mozilla Firefox przesunięcie kursora myszy nad tekstem przed lub po linku teraz niezawodnie informuje o tekście. (#15990, @jcsteh)
* NVDA nie powoduje już sporadycznych niepowodzeń w otwieraniu wiadomości, które można przeglądać (np. dwukrotne naciśnięcie "NVDA+f"). (#16806, @LeonarddeR)
* Gdy NVDA jest aktualizowana, a aktualizacje dodatków są w toku, nie powoduje już usunięcia dodatku. (#16837)
* Teraz można wchodzić w interakcje z listami rozwijanymi sprawdzania poprawności danych w programie Microsoft Excel 365. (#15138)
* NVDA nie jest już tak powolna podczas przewijania dużych plików w górę i w dół w VS Code. (#17039)
* NVDA nie przestaje odpowiadać po długim przytrzymaniu strzałki w trybie przeglądania, szczególnie w programach Microsoft Word i Microsoft Outlook. (#16812)
* NVDA nie czyta już ostatniego wiersza, gdy kursor znajduje się na przedostatnim wierszu wielowierszowej kontrolki edycji w aplikacjach Java. (#17027)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Aktualizacje komponentów:
  * Zaktualizowano py2exe do wersji 0.13.0.2 (#16907, @dpy013)
  * Zaktualizowano setuptools do wersji 72.0 (#16907, @dpy013)
  * Zaktualizowano Ruffa do wersji 0.5.6. (#16868, @LeonarddeR)
  * Zaktualizowano nh3 do wersji 0.2.18 (#17020, @dpy013)
* Dodano plik '.editorconfig' do repozytorium NVDA, aby kilka IDE mogło domyślnie pobierać podstawowe reguły stylu kodu NVDA. (#16795, @LeonarddeR)
* Dodano obsługę niestandardowych słowników symboli mowy. (#16739, #16823, @LeonarddeR)
  * Słowniki mogą być dostępne w folderach specyficznych dla ustawień regionalnych w pakiecie dodatkowym, np. 'locale\en'.
  * Metadane słownika można dodać do opcjonalnej sekcji "symbolDictionaries" w manifeście dodatku.
  * Aby uzyskać więcej informacji, zapoznaj się z sekcją [Słowniki niestandardowych symboli mowy w przewodniku dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSymbolDictionaries).
* Możliwe jest teraz przekierowywanie obiektów pobranych ze współrzędnych na ekranie za pomocą metody "NVDAObject.objectFromPointRedirect". (#16788, @Emil-18)
* Uruchomienie SCons z parametrem "--all-cores" automatycznie wybierze maksymalną liczbę dostępnych rdzeni procesora. (#16943, #16868, @LeonarddeR)
* Informacje dla deweloperów zawierają teraz informacje o architekturze aplikacji (takiej jak AMD64) dla obiektu navigator. (#16488, @josephsl)

#### Przestarzałe

* Klucz konfiguracji "bool" "[documentFormatting][reportFontAttributes]" jest przestarzały do usunięcia w 2025.1, zamiast tego użyj "[fontAttributeReporting]". (#16748)
  * Nowy klucz ma wartość "int" pasującą do "enum" "OutputMode" z opcjami mowy, brajla, mowy i braille'a oraz off.
  * Użytkownicy interfejsu API mogą używać wartości "bool", tak jak poprzednio, lub sprawdzić wartość "OutputMode", jeśli obsługuje konkretnie mowę lub alfabet Braille'a.
  * Te klucze są obecnie synchronizowane do wersji 2025.1.
* Wartość "NVDAObjects.UIA.InaccurateTextChangeEventEmittingEditableText" jest przestarzała bez zastępowania. (#16817, @LeonarddeR)

## 2024.3.1

Jest to wydanie poprawki mające na celu naprawienie błędu z automatycznym powiadomieniem o aktualizacji dodatku.

### Poprawki błędów

* Podczas automatycznego sprawdzania dostępności aktualizacji dodatków, NVDA nie zawiesza się już przy słabych połączeniach. (#17036)

## 2024.3

Sklep z dodatkami powiadomi Cię teraz, jeśli jakiekolwiek aktualizacje dodatków są dostępne podczas uruchamiania NVDA.

Dostępne są teraz opcje zastosowania normalizacji Unicode do wyjścia mowy i alfabetu Braille'a.
Może to być przydatne podczas odczytywania znaków, które są nieznane określonemu syntezatorowi mowy lub tablicy Braille'a i które mają kompatybilną alternatywę, taką jak pogrubienie i kursywa powszechnie używane w mediach społecznościowych.
Umożliwia także odczytywanie równań w edytorze równań Microsoft Word.

Monitory brajlowskie Help Tech Activator Pro są teraz obsługiwane.

Dodano nieprzypisane polecenia do przewijania kółka myszy w pionie i poziomie.

Istnieje kilka poprawek błędów, szczególnie w przypadku panelu emotikonów systemu Windows 11 i historii schowka.
W przypadku przeglądarek internetowych wprowadzono poprawki dotyczące raportowania komunikatów o błędach, rysunków, podpisów, etykiet tabel i elementów menu pól wyboru/przycisków radiowych.

LibLouis został zaktualizowany, dodając nowe tabele Braille'a dla cyrylicy serbskiej, jidysz, kilku starożytnych języków, tureckiego i międzynarodowego alfabetu fonetycznego.
eSpeak został zaktualizowany, dodając obsługę języka Karakałpak.
Zaktualizowano również Unicode CLDR.

### Nowe funkcje

* Nowe komendy klawiszowe:
  * Dodano nieprzypisane polecenia do przewijania kółka myszy w pionie i poziomie, aby usprawnić nawigację na stronach internetowych i aplikacjach z dynamiczną zawartością, takich jak Dism++. (#16462, @Cary-Rowen)
* Dodano obsługę normalizacji Unicode do wyjścia mowy i brajla. (#11570, #16466 @LeonarddeR).
  * Może to być przydatne podczas odczytywania znaków, które są nieznane określonemu syntezatorowi mowy lub tablicy Braille'a i które mają kompatybilną alternatywę, taką jak pogrubienie i kursywa powszechnie używane w mediach społecznościowych.
  * Umożliwia także odczytywanie równań w edytorze równań Microsoft Word. (#4631)
  * Możesz włączyć tę funkcję zarówno dla mowy, jak i alfabetu Braille'a w odpowiednich kategoriach ustawień w oknie dialogowym Ustawienia NVDA.
* Domyślnie, po uruchomieniu NVDA, zostaniesz powiadomiony, jeśli dostępne są jakiekolwiek aktualizacje dodatków. (#15035)
  * Można to wyłączyć w kategorii ustawień "Sklep z dodatkami".
  * NVDA codziennie sprawdza dostępność aktualizacji dodatków.
  * Sprawdzane będą tylko aktualizacje w ramach tego samego kanału (np. zainstalowane dodatki w wersji beta będą powiadamiać o aktualizacjach tylko w kanale beta).
* Dodano obsługę wyświetlaczy Help Tech Activator Pro. (#16668)

### Zmiany

* Aktualizacje komponentów:
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit '54ee11a79'. (#16495)
    * Dodano nowy język Karakałpak.
  * Zaktualizowano Unicode CLDR do wersji 45.0. (#16507, @OzancanKaratas)
  * Zaktualizowano fast_diff_match_patch (używany do wykrywania zmian w terminalach i innej zawartości dynamicznej) do wersji 2.1.0. (#16508, @codeofdusk)
  * Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0). (#16652, @codeofdusk)
    * Nowe tablice brajlowskie:
      * Cyrylica serbska.
      * Jidysz.
      * niektóre języki starożytne: hebrajski biblijny, akadyjski, syryjski, ugarycki i transliterowany tekst pisma klinowego.
      * Tureckie skróty. (#16735)
      * Międzynarodowy alfabet fonetyczny. (#16773)
  * Zaktualizowano NSIS do wersji 3.10 (#16674, @dpy013)
  * Zaktualizowano znaczniki Markdown do wersji 3.6 (#16725, @dpy013)
  * Zaktualizowano nh3 do wersji 0.2.17 (#16725, @dpy013)
* Zastępcza tabela wejściowa brajlowska jest teraz równa rezerwowej tabeli wyjściowej, która jest ujednoliconym angielskim kodem Braille'a klasy 1. (#9863, @JulienCochuyt, @LeonarddeR)
* NVDA będzie teraz raportować dane bez dostępnych elementów podrzędnych, ale z etykietą lub opisem. (#14514)
* Podczas czytania wierszy w trybie przeglądania "podpis" nie jest już podawany w każdym wierszu długiego podpisu rysunku lub tabeli. (#14874)
* W konsoli Pythona ostatnie niewykonane polecenie nie zostanie już utracone podczas przechodzenia w historii danych wejściowych. (#16653, @CyrilleB79)
* Unikalny anonimowy identyfikator jest teraz wysyłany w ramach opcjonalnego zbierania statystyk użycia NVDA. (#16266)
* Domyślnie podczas tworzenia kopii przenośnej zostanie utworzony nowy folder.
Zostanie wyświetlony komunikat ostrzegawczy, jeśli spróbujesz zapisać dane do niepustego katalogu. (#16686)

### Poprawki błędów

* Poprawki systemu Windows 11:
  * NVDA nie będzie już sprawiać wrażenia, że zacina się po zamknięciu historii schowka i panelu emoji. (#16346, #16347, @josephsl)
  * NVDA ponownie ogłosi widocznych kandydatów po otwarciu interfejsu IME. (#14023, @josephsl)
  * NVDA nie będzie już dwukrotnie ogłaszać "historii schowka" podczas przechodzenia przez elementy menu panelu emoji. (#16532, @josephsl)
  * NVDA nie będzie już ucinać mowy i alfabetu Braille'a podczas przeglądania kaomoji i symboli w panelu emotikonów. (#16533, @josephsl)
* Poprawki w przeglądarkach internetowych:
  * Komunikaty o błędach, do których odwołuje się "aria-errormessage", są teraz zgłaszane w przeglądarkach Google Chrome i Mozilla Firefox. (#8318)
  * Jeśli jest obecna, NVDA będzie teraz używać 'aria-labelledby', aby zapewnić dostępne nazwy dla tabel w Mozilla Firefox. (#5183)
  * NVDA będzie poprawnie informować o elementach menu radiowego i pola wyboru przy pierwszym wejściu do podmenu w Google Chrome i Mozilla Firefox. (#14550)
  * Funkcja wyszukiwania w trybie przeglądania NVDA jest teraz dokładniejsza, gdy strona zawiera emotikony. (#16317, @LeonarddeR)
  * W przeglądarce Mozilla Firefox, NVDA teraz poprawnie zgłasza bieżący znak, słowo i linię, gdy kursor znajduje się w punkcie wstawiania na końcu wiersza. (#3156, @jcsteh)
  * Nie powoduje już awarii przeglądarki Google Chrome podczas zamykania dokumentu lub wychodzenia z niej. (#16893)
* NVDA poprawnie ogłosi sugestie autouzupełniania w Eclipse i innych środowiskach opartych na Eclipse w systemie Windows 11. (#16416, @thgcode)
* Poprawiono niezawodność automatycznego odczytu tekstu, szczególnie w aplikacjach terminalowych. (#15850, #16027, @Danstiv)
* Po raz kolejny możliwe jest niezawodne zresetowanie konfiguracji do ustawień fabrycznych. (#16755, @Emil-18)
* NVDA poprawnie ogłosi zmiany zaznaczenia podczas edycji tekstu komórki w programie Microsoft Excel. (#15843)
* W aplikacjach korzystających z Java Access Bridge, NVDA będzie teraz poprawnie odczytywać ostatnią pustą linię tekstu, zamiast powtarzać poprzednią linię. (#9376, @dmitrii-Drobotov)
* W LibreOffice Writer (wersja 24.8 i nowsze), podczas przełączania formatowania tekstu (pogrubienie, kursywa, podkreślenie, indeks dolny/górny, wyrównanie) za pomocą odpowiedniego skrótu klawiaturowego, NVDA ogłasza nowy atrybut formatowania (np. "Pogrubienie włączone", "Pogrubienie wyłączone"). (#4248, @michaelweghorn)
* Podczas nawigacji za pomocą kursora w polach tekstowych w aplikacjach, które korzystają z automatyzacji interfejsu użytkownika, NVDA nie zgłasza już czasami błędnego znaku, słowa itp. (#16711, @jcsteh)
* Podczas wklejania do kalkulatora systemu Windows 10/11, NVDA teraz poprawnie zgłasza pełną wklejoną liczbę. (#16573, @TristanBurchett)
* Mowa nie jest już cicha po rozłączeniu się z sesją pulpitu zdalnego i ponownym nawiązaniu z nią połączenia. (#16722, @jcsteh)
* Dodano obsługę poleceń przeglądu tekstu dla nazwy obiektu w Visual Studio Code. (#16248, @Cary-Rowen)
* Odtwarzanie dźwięków NVDA nie kończy się już niepowodzeniem na monofonicznym urządzeniu audio. (#16770, @jcsteh)
* NVDA będzie raportować adresy podczas przechodzenia przez pola Do/CC/BCC w outlook.com / Modern Outlook. (#16856)
* NVDA radzi sobie teraz z błędami instalacji dodatków bardziej wdzięcznie. (#16704)

### Zmiany dla deweloperów

* NVDA używa teraz Ruff zamiast flake8 do lintingu. (#14817)
* Naprawiono system kompilacji NVDA, aby działał poprawnie podczas korzystania z programu Visual Studio 2022 w wersji 17.10 lub nowszej. (#16480, @LeonarddeR)
* Czcionka o stałej szerokości jest teraz używana w Log Viewer i w konsoli NVDA Python, dzięki czemu kursor pozostaje w tej samej kolumnie podczas nawigacji pionowej.
Jest to szczególnie przydatne do odczytywania znaczników lokalizacji błędów w śledzeniach zwrotnych. (#16321, @CyrilleB79)
* Dodano obsługę niestandardowych tabel brajlowskich. (#3304, #16208, @JulienCochuyt, @LeonarddeR)
  * Tabele mogą być dostępne w folderze 'brailleTables' w pakiecie dodatkowym.
  * Metadane tabeli można dodać do opcjonalnej sekcji 'brailleTables' w manifeście dodatku lub do pliku '.ini' o tym samym formacie, który znajduje się w podkatalogu brailleTables w katalogu podręcznej.
  * Aby uzyskać więcej informacji, zapoznaj się z sekcją [tabele tłumaczeń brajlowskich w podręczniku dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#BrailleTables).
* Gdy zdarzenie "gainFocus" jest umieszczane w kolejce z obiektem, który ma prawidłową właściwość "focusRedirect", obiekt wskazywany przez właściwość "focusRedirect" jest teraz przechowywany przez obiekt "eventHandler.lastQueuedFocusObject", a nie przez obiekt pierwotnie umieszczony w kolejce. (#15843)
* NVDA zaloguje swoją architekturę wykonywalną (x86) podczas uruchamiania. (#16432, @josephsl)
* 'wx. CallAfter', który jest opakowany w 'monkeyPatches/wxMonkeyPatches.py', zawiera teraz poprawne wskazanie 'functools.wraps'. (#16520, @XLTechie)
* Pojawił się nowy moduł do planowania zadań 'utils.schedule', wykorzystujący moduł 'schedule'. (#16636)
  * Możesz użyć 'scheduleThread.scheduleDailyJobAtStartUp', aby automatycznie zaplanować zadanie, które ma miejsce po uruchomieniu NVDA, a następnie co 24 godziny.
  Zadania są planowane z opóźnieniem, aby uniknąć konfliktów.
  * Wartości "scheduleThread.scheduleDailyJob" i "scheduleJob" mogą służyć do planowania zadań w niestandardowych godzinach, w których zostanie zgłoszony błąd "JobClashError" w przypadku znanego konfliktu planowania zadań.
* Teraz można tworzyć moduły aplikacji dla aplikacji hostujących kontrolki Edge WebView2 (msedgewebview2.exe). (#16705, @josephsl)

## 2024.2

Pojawiła się nowa funkcja o nazwie podział dźwięku.
Pozwala to na rozdzielenie dźwięków NVDA na jeden kanał (np. lewy), podczas gdy dźwięki ze wszystkich innych aplikacji są kierowane do drugiego kanału (np. prawego).

Dodano nowe polecenia do modyfikowania ustawień w pierścieniu ustawień mowy, tym samym umożliwiając użytkownikowi przemieszczanie sie od pierwszego do ostatniego ustawienia, a także do zmniejszania lub zwiększania ustawień w większych krokach.
Dodano także nowe polecenia do szybkiej nawigacji, umożliwiając użytkownikowi przemieszczanie się pomiędzy: akapitami, pionowo wyrównanymi akapitami, tekstem tego samego stylu, tekstem różnego stylu, elementami menu, przyciskami przełączania, paskami postępu, figurami, i formułami matematycznymi.

Wprowadzono wiele nowych funkcji alfabetu Braille'a i poprawek błędów.
Dodano nowy tryb brajlowski o nazwie "wyświetl wyjście mowy".
Gdy monitor brajlowski jest aktywny, pokazuje dokładnie to, co mówi NVDA.
Dodano również obsługę monitorów BrailleEdgeS2 i BrailleEdgeS3.
LibLouis został zaktualizowany, dodając nowe szczegółowe (z zaznaczonymi wielkimi literami) białoruskie i ukraińskie tablice Braille'a, tabelę laotańską i hiszpańską tabelę do czytania tekstów greckich.

eSpeak został zaktualizowany, dodając nowy język Tigrinya.

Istnieje wiele drobnych poprawek błędów dla aplikacji, takich jak Thunderbird, Adobe Reader, przeglądarki internetowe, Nudi i Geekbench.

### Nowe funkcje

* Nowe komendy klawiszowe:
  * Nowe polecenie szybkiej nawigacji "p" do przeskakiwania do następnego/poprzedniego akapitu tekstu w trybie przeglądania. (#15998, @mltony)
  * Nowe nieprzypisane polecenia szybkiej nawigacji, których można użyć do przeskoczenia do następnego/poprzedniego:
    * Rysunek (#10826)
    * Akapit wyrównany w pionie (#15999, @mltony)
    * Pozycja menu (#16001, @mltony)
    * Przycisk przełączania (#16001, @mltony)
    * Pasek postępu (#16001, @mltony)
    * Formuła matematyczna (#16001, @mltony)
    * Tekst w tym samym stylu (#16000, @mltony)
    * Tekst w innym stylu (#16000, @mltony)
  * Dodano komendy do przeskakiwania pierwszego, ostatniego, do przodu i do tyłu przez pierścień ustawień syntezatora. (#13768, #16095, @rmcpantoja)
    * Ustawienie pierwszego/ostatniego ustawienia w pierścieniu ustawień syntezatora nie ma przypisanego gestu. (#13768)
    * Zmniejsz i zwiększ bieżące ustawienie pierścienia ustawień syntezatora w większym kroku (#13768):
      * Dla komputerów stacjonarnych: `NVDA+control+pageUp` or `NVDA+control+pageDown`.
      * Dla komputerów przenośnych: `NVDA+control+shift+pageUp` or `NVDA+control+shift+pageDown`.
  * Dodano nowy, nieprzypisany gest wejściowy, aby przełączać raportowanie rysunków i podpisów. (#10826, #14349)
* Przywołuje monitor brajlowski do komórki brajlowskiej |`routing`
  * Dodano obsługę monitorów BrailleEdgeS2 i BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * Dodano nowy tryb brajlowski o nazwie "wyświetl wyjście mowy". (#15898, @Emil-18)
    * Gdy monitor brajlowski jest aktywny, pokazuje dokładnie to, co mówi NVDA.
    * można go włączać lub wyłączać za pomocą skrótu `NVDA+alt+t`, lub z okna dialogowego ustawień brajla.
* Podział dźwięku: (#12985, @mltony)
  * Umożliwia dzielenie dźwięków NVDA na jeden kanał (np. lewy), podczas gdy dźwięki ze wszystkich innych aplikacji są kierowane do drugiego kanału (np. prawego).
  * Przełączane przez 'NVDA+alt+s'.
* Raportowanie nagłówków wierszy i kolumn jest teraz obsługiwane w edytowalnych elementach HTML. (#14113)
* Dodano opcję wyłączenia raportowania rysunków i podpisów w ustawieniach formatowania dokumentu. (#10826, #14349)
* W systemie Windows 11 NVDA ogłosi alerty z pisania głosowego i sugerowane działania, w tym górną sugestię podczas kopiowania danych, takich jak numery telefonów, do schowka (aktualizacja Windows 11 2022 i nowsze). (#16009, @josephsl)
* NVDA utrzyma urządzenie audio w stanie czuwania po ustaniu mowy, aby zapobiec przycięciu początku następnej mowy za pomocą niektórych urządzeń audio, takich jak słuchawki Bluetooth. (#14386, @jcsteh, @mltony)
* Przeglądarka HP Secure Browser jest teraz obsługiwana. (#16377)

### Zmiany

* Sklep z dodatkami:
  * Minimalna i ostatnia testowana wersja NVDA dla dodatku są teraz wyświetlane w obszarze "inne szczegóły". (#15776, @Nael-Sayegh)
  * Akcja Opinie społeczności będzie dostępna we wszystkich zakładkach sklepu. (#16179, @nvdaes)
* Aktualizacje komponentów:
  * Zaktualizowano LibLouis Braille translator do wersji [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Nowe szczegółowe (z zaznaczonymi wielkimi literami) białoruskie i ukraińskie tablice brajlowskie.
    * Nowa hiszpańska tabela do czytania tekstów greckich.
    * Nowy stół dla Lao Grade 1. (#16470)
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit 'cb62d93fd7'. (#15913)
    * Dodano nowy język tigrinia.
* Zmieniono kilka gestów dla urządzeń BrailleSense, aby uniknąć konfliktów ze znakami francuskiej tablicy Braille'a. (#15306)
  * "alt+strzałka w lewo" jest teraz mapowana na "kropka2+kropka7+spacja"
  * Wartości "alt+strzałka w prawo" są teraz mapowane na "kropka5+kropka7+spacja".
  * "alt+strzałka w górę" jest teraz mapowana na "kropka2+kropka3+punkt7+spacja"
  * "alt+strzałka w dół" jest teraz mapowana na "kropka5+punkt6+punkt7+spacja"
* Dopełnienie kropek często używane w spisach treści nie jest już zgłaszane na niskich poziomach interpunkcji. (#15845, @CyrilleB79)

### Poprawki błędów

* Poprawki systemu Windows 11:
  * NVDA po raz kolejny ogłosi sugestie dotyczące wprowadzania danych z klawiatury sprzętowej. (#16283, @josephsl)
  * W wersji 24H2 (aktualizacja 2024 i Windows Server 2025) interakcja za pomocą myszy i dotyku może być używana w szybkich ustawieniach. (#16348, @josephsl)
* Sklep z dodatkami:
  * Po naciśnięciu "ctrl+tab" fokus zostanie prawidłowo przeniesiony do nowego tytułu bieżącej karty. (#14986, @ABuffEr)
  * Jeśli pliki pamięci podręcznej nie są poprawne, NVDA nie będzie się już uruchamiać ponownie. (#16362, @nvdaes)
* Poprawki dla przeglądarek opartych na silniku Chromium gdy są używane z Uia:
  * Naprawiono błędy powodujące zawieszanie się NVDA. (#16393, #16394)
  * Klawisz Backspace od teraz działa  prawidłowo w polach edycji logowania w Gmailu. (#16395)
* Backspace działa teraz poprawnie podczas korzystania z Nudi 6.1 z włączonym ustawieniem NVDA "Handle keys from other applications". (#15822, @jcsteh)
* Naprawiono błąd polegający na tym, że współrzędne audio były odtwarzane, gdy aplikacja jest w trybie uśpienia, gdy włączona jest opcja "Odtwarzaj współrzędne dźwiękowe, gdy mysz się porusza". (#8059, @hwf1324)
* W programie Adobe Reader NVDA nie ignoruje już tekstu alternatywnego ustawionego w formułach w plikach PDF. (#12715)
* Naprawiono błąd powodujący, że NVDA nie odczytywał wstążki i opcji w Geekbench. (#16251, @mzanm)
* Naprawiono rzadki przypadek, w którym zapisywanie konfiguracji mogło nie spowodować zapisania wszystkich profili. (#16343, @CyrilleB79)
* W przeglądarkach opartych na Firefoksie i Chromium, NVDA poprawnie przejdzie w tryb ostrości po naciśnięciu Enter, gdy zostanie umieszczony na liście prezentacyjnej (ul / ol) wewnątrz edytowalnej treści. (#16325)
* Zmiana stanu kolumny jest teraz poprawnie zgłaszana podczas wybierania kolumn do wyświetlenia na liście wiadomości Thunderbirda. (#16323)
* Przełącznik wiersza poleceń '-h'/'--help' znów działa poprawnie. (#16522, @XLTechie)
* Wsparcie dla programu Poedit używanego do tłumaczenia w wersji 3.4 lub nowszej, działa poprawnie podczas tłumaczenia na języki z jedną lub dwie formy liczby mnogiej (na przykład, dla chińskiego i polskiego). (#16318)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Tworzenie wystąpienia obiektów "winVersion.WinVersion" z nieznanymi wersjami systemu Windows powyżej 10.0.22000, takimi jak 10.0.25398, zwraca wartość "Windows 11 nieznany" zamiast "Windows 10 nieznany" jako nazwę wydania. (#15992, @josephsl)
* Ułatw proces kompilacji AppVeyor dla rozwidleń NVDA, dodając konfigurowalne zmienne w appveyor.yml do wyłączania lub modyfikowania określonych części skryptów kompilacji NV Access. (#16216, @XLTechie)
* Dodano dokument instruktażowy, wyjaśniający proces budowania forków NVDA na AppVeyor. (#16293, @XLTechie)

## 2024.1

Dodano nowy tryb mowy "na żądanie".
Gdy mowa jest na żądanie, NVDA nie mówi automatycznie (np. podczas przesuwania kursora), ale nadal mówi, gdy wywołuje polecenia, których celem jest jawne zgłoszenie czegoś (np. tytuł okna raportu).
W kategorii Mowa w ustawieniach NVDA można teraz wykluczyć niechciane tryby mowy z polecenia Przełącz tryby mowy ('NVDA+s').

Nowy tryb wyboru natywnego (przełączany przez 'NVDA+shift+f10') jest teraz dostępny w trybie przeglądania NVDA dla przeglądarki Mozilla Firefox.
Gdy ta opcja jest włączona, zaznaczanie tekstu w trybie przeglądania będzie również manipulować natywnym wyborem Firefoksa.
Kopiowanie tekstu za pomocą 'control+c' przejdzie prosto do Firefoksa, kopiując w ten sposób bogatą treść, a nie reprezentację zwykłego tekstu NVDA.

Sklep z dodatkami obsługuje teraz działania zbiorcze (np. instalowanie, włączanie dodatków) poprzez wybranie wielu dodatków
Dostępna jest nowa akcja umożliwiająca otwarcie strony z recenzjami dla wybranego dodatku.

Opcje urządzenia wyjściowego audio i trybu wyciszania zostały usunięte z okna dialogowego "Wybierz syntezator".
Można je znaleźć w panelu ustawień audio, który można otworzyć za pomocą 'NVDA+control+u'.

Zaktualizowano eSpeak-NG, tłumacza brajlowskiego LibLouis i Unicode CLDR.
Dostępne są nowe stoły brajlowskie w językach tajskim, filipińskim i rumuńskim.

Wprowadzono wiele poprawek, szczególnie w Sklepie z dodatkami, alfabecie Braille'a, Libre Office, Microsoft Office i audio.

### Ważne wskazówki

* Ta wersja zapewnia zgodność z istniejącymi dodatkami.
* Systemy Windows 7 i Windows 8 nie są już obsługiwane.
Windows 8.1 to minimalna obsługiwana wersja systemu Windows.

### Nowe funkcje

* Sklep z dodatkami:
  * Sklep z dodatkami obsługuje teraz działania zbiorcze (np. instalowanie, włączanie dodatków) poprzez wybranie wielu dodatków. (#15350, #15623, @CyrilleB79)
  * Dodano nową akcję umożliwiającą otwarcie dedykowanej strony internetowej w celu wyświetlenia lub przekazania opinii na temat wybranego dodatku. (#15576, @nvdaes)
* Dodano obsługę monitorów brajlowskich Bluetooth Low Energy HID. (#15470)
* Nowy tryb wyboru natywnego (przełączany przez 'NVDA+shift+f10') jest teraz dostępny w trybie przeglądania NVDA dla przeglądarki Mozilla Firefox.
Gdy ta opcja jest włączona, zaznaczanie tekstu w trybie przeglądania będzie również manipulować natywnym wyborem Firefoksa.
Kopiowanie tekstu za pomocą 'control+c' przejdzie prosto do Firefoksa, kopiując w ten sposób bogatą treść, a nie reprezentację zwykłego tekstu NVDA.
Zauważ jednak, że ponieważ Firefox obsługuje rzeczywistą kopię, NVDA nie zgłosi komunikatu "kopiuj do schowka" w tym trybie. (#15830)
* Podczas kopiowania tekstu w programie Microsoft Word z włączonym trybem przeglądania NVDA, formatowanie jest teraz również uwzględniane.
Ubocznym skutkiem tego jest to, że NVDA nie będzie już zgłaszać komunikatu "kopiuj do schowka" po naciśnięciu "control+c" w trybie przeglądania Microsoft Word / Outlook, ponieważ teraz aplikacja obsługuje kopię, a nie NVDA. (#16129)
* Dodano nowy tryb mowy "na żądanie".
Gdy mowa jest na żądanie, NVDA nie mówi automatycznie (np. podczas przesuwania kursora), ale nadal mówi, gdy wywołuje polecenia, których celem jest jawne zgłoszenie czegoś (np. tytuł okna raportu). (#481, @CyrilleB79)
* W kategorii Mowa w ustawieniach NVDA można teraz wykluczyć niechciane tryby mowy z polecenia Przełącz tryby mowy ('NVDA+s'). (#15806, @lukaszgo1)
  * Jeśli obecnie korzystasz z dodatku NoBeepsSpeechMode, rozważ jego odinstalowanie i wyłączenie trybów "sygnały dźwiękowe" i "na żądanie" w ustawieniach.

### Zmiany

* NVDA nie obsługuje już systemów Windows 7 i Windows 8.
Windows 8.1 to minimalna obsługiwana wersja systemu Windows. (#15544)
* Aktualizacje komponentów:
  * Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Dodano nowe tabele brajlowskie w językach tajskim, rumuńskim i filipińskim.
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit '530bf0abf'. (#15036)
  * Adnotacje emoji i symboli CLDR zostały zaktualizowane do wersji 44.0. (#15712, @OzancanKaratas)
  * Zaktualizowano Java Access Bridge do wersji 17.0.9+8Zulu (17.46.19). (#15744)
* Kluczowe polecenia:
  * Następujące polecenia obsługują teraz dwa i trzy naciśnięcia w celu przeliterowania zgłaszanych informacji i pisowni z opisami postaci: wybór raportu, tekst schowka raportu i skoncentrowany obiekt raportu. (#15449, @CyrilleB79)
  * Polecenie przełączenia kurtyny ekranu ma teraz domyślny gest: 'NVDA+control+escape'. (#10560, @CyrilleB79)
  * Po czterokrotnym naciśnięciu polecenie wyboru raportu pokazuje teraz wybór w wiadomości, którą można przeglądać. (#15858, @Emil-18)
* Microsoft Office:
  * Podczas żądania informacji o formatowaniu w komórkach programu Excel, obramowania i tło będą zgłaszane tylko wtedy, gdy istnieje takie formatowanie. (#15560, @CyrilleB79)
  * NVDA nie będzie już raportować nieoznaczonych grup, takich jak w najnowszych wersjach menu Microsoft Office 365. (#15638)
* Opcje urządzenia wyjściowego audio i trybu wyciszania zostały usunięte z okna dialogowego "Wybierz syntezator".
Można je znaleźć w panelu ustawień audio, który można otworzyć za pomocą 'NVDA+control+u'. (#15512, @codeofdusk)
* Nazwa opcji "Zgłoś rolę, gdy mysz wejdzie w obiekt" w kategorii ustawień myszy NVDA została zmieniona na "Zgłoś obiekt, gdy mysz do niego wejdzie".
Ta opcja ogłasza teraz dodatkowe istotne informacje o obiekcie, gdy mysz do niego wejdzie, takie jak stany (zaznaczone/naciśnięte) lub współrzędne komórki w tabeli. (#15420, @LeonarddeR)
* Dodano nowe przedmioty do menu Pomoc na stronie "Uzyskaj pomoc" i w sklepie NV Access. (#14631)
* Wsparcie NVDA dla [Poedit](https://poedit.net) zostało przerobione dla Poedit w wersji 3 i wyższych.
Użytkownicy Poedit 1 są zachęcani do aktualizacji do Poedit 3, jeśli chcą polegać na ulepszonej dostępności w Poedit, takiej jak skróty do czytania notatek i komentarzy tłumacza. (#15313, #7303, @LeonarddeR)
* Przeglądarka brajlowska i przeglądarka mowy są teraz wyłączone w trybie bezpiecznym. (#15680)
* Podczas nawigacji po obiektach wyłączone (niedostępne) obiekty nie będą już ignorowane. (#15477, @CyrilleB79)
* Dodano spis treści do dokumentu poleceń klawiszowych. (#16106)

### Poprawki błędów

* Sklep z dodatkami:
  * Gdy stan dodatku zostanie zmieniony, gdy jest on aktywny, np. zmiana z "pobieranie" na "pobrano", zaktualizowany element jest teraz poprawnie ogłaszany. (#15859, @LeonarddeR)
  * Podczas instalowania dodatków monity o instalację nie są już nakładane na okno dialogowe ponownego uruchamiania. (#15613, @lukaszgo1)
  * Podczas ponownej instalacji niekompatybilnego dodatku nie jest on już wyłączany na siłę. (#15584, @lukaszgo1)
  * Wyłączone i niekompatybilne dodatki można teraz aktualizować. (#15568, #15029)
  * NVDA teraz odzyskuje sprawność i wyświetla błąd w przypadku, gdy dodatek nie zostanie poprawnie pobrany. (#15796)
  * NVDA nie uruchamia się już sporadycznie ponownie po otwarciu i zamknięciu sklepu z dodatkami. (#16019, @lukaszgo1)
* Dźwięk:
  * NVDA nie zawiesza się już na chwilę, gdy wiele dźwięków jest odtwarzanych w krótkich odstępach czasu. (#15311, #15757, @jcsteh)
  * Jeśli urządzenie wyjściowe audio jest ustawione na coś innego niż domyślne i to urządzenie stanie się ponownie dostępne po tym, jak było niedostępne, NVDA przełączy się z powrotem na skonfigurowane urządzenie, zamiast kontynuować korzystanie z urządzenia domyślnego. (#15759, @jcsteh)
  * NVDA wznawia teraz dźwięk, jeśli zmieni się konfiguracja urządzenia wyjściowego lub inna aplikacja zwolni wyłączną kontrolę nad urządzeniem. (#15758, #15775, @jcsteh)
* Przywołuje monitor brajlowski do komórki brajlowskiej |`routing`
  * Wielowierszowe monitory brajlowskie nie powodują już awarii sterownika BRLTTY i są traktowane jako jeden ciągły wyświetlacz. (#15386)
  * Wykrywanych jest więcej obiektów zawierających przydatny tekst, a treść tekstowa jest wyświetlana w alfabecie Braille'a. (#15605)
  * Kontrowane wejście brajlowskie znów działa poprawnie. (#15773, @aaclause)
  * Alfabet Braille'a jest teraz aktualizowany podczas przenoszenia obiektu nawigatora między komórkami tabeli w większej liczbie sytuacji (#15755, @Emil-18)
  * Wynik raportowania bieżącego fokusu, bieżącego obiektu nawigatora i bieżących poleceń wyboru jest teraz wyświetlany w alfabecie Braille'a. (#15844, @Emil-18)
  * Sterownik brajlowski Albatross nie obsługuje już mikrokontrolera Esp32 jako wyświetlacza Albatross. (#15671)
* LibreOffice:
  * Słowa usunięte za pomocą skrótu klawiaturowego "control+backspace" są teraz poprawnie ogłaszane, gdy po usuniętym słowie następują białe znaki (np. spacje i tabulatory). (#15436, @michaelweghorn)
  * Ogłaszanie paska stanu za pomocą skrótu klawiaturowego "NVDA+end" działa teraz również w przypadku okien dialogowych w LibreOffice w wersji 24.2 i nowszych. (#15591, @michaelweghorn)
  * Wszystkie oczekiwane atrybuty tekstu są teraz obsługiwane w LibreOffice w wersji 24.2 i nowszych.
  Sprawia to, że ogłaszanie błędów pisowni działa podczas ogłaszania wiersza w programie Writer. (#15648, @michaelweghorn)
  * Ogłaszanie poziomów nagłówków działa teraz również w LibreOffice w wersji 24.2 i nowszych. (#15881, @michaelweghorn)
* Microsoft Office:
  * W Excelu z wyłączoną funkcją UIA alfabet Braille'a jest aktualizowany, a zawartość aktywnej komórki jest odczytywana po naciśnięciu "control+y", "control+z" lub "alt+backspace". (#15547)
  * W programie Word z wyłączoną funkcją UIA brajl jest aktualizowany po naciśnięciu 'control+v', 'control+x', 'control+y', 'control+z', 'alt+backspace', 'backspace' lub 'control+backspace'.
  Jest również aktualizowany z włączoną funkcją UIA, gdy wpisywanie tekstu i alfabet Braille'a jest podłączony do przeglądania, a przegląd następuje po karetce. (#3276)
  * W programie Word komórka docelowa będzie teraz poprawnie raportowana podczas korzystania z natywnych poleceń programu Word do nawigacji po tabeli "alt+home", "alt+end", "alt+pageUp" i "alt+pageDown". (#15805, @CyrilleB79)
* Ulepszono raportowanie skrótów do obiektów. (#10807, #15816, @CyrilleB79)
* Syntezator SAPI4 teraz poprawnie obsługuje zmiany głośności, szybkości i wysokości dźwięku wbudowane w mowę. (#15271, @LeonarddeR)
* Stan wielu wierszy jest teraz poprawnie raportowany w aplikacjach korzystających z Java Access Bridge. (#14609)
* NVDA ogłosi zawartość okna dialogowego dla większej liczby okien dialogowych Windows 10 i 11. (#15729, @josephsl)
* NVDA nie będzie już przerywać odczytu nowo załadowanej strony w Microsoft Edge podczas korzystania z automatyzacji interfejsu użytkownika. (#15736)
* W przypadku użycia poleceń powiedz wszystko lub przeliterowujących tekst przerwy między zdaniami lub znakami nie zmniejszają się już stopniowo z czasem. (#15739, @jcsteh)
* NVDA nie zawiesza się już czasami podczas czytania dużej ilości tekstu. (#15752, @jcsteh)
* Podczas uzyskiwania dostępu do przeglądarki Microsoft Edge za pomocą automatyzacji interfejsu użytkownika, NVDA jest w stanie aktywować więcej elementów sterujących w trybie przeglądania. (#14612)
* NVDA nie uruchomi się już dłużej, gdy plik konfiguracyjny jest uszkodzony, ale przywróci konfigurację do ustawień domyślnych, tak jak to miało miejsce w przeszłości. (#15690, @CyrilleB79)
* Naprawiono obsługę kontrolek widoku listy systemowej ("SysListView32") w aplikacjach Windows Forms. (#15283, @LeonarddeR)
* Nie jest już możliwe nadpisanie historii konsoli NVDA w Pythonie. (#15792, @CyrilleB79)
* NVDA powinna reagować w przypadku zalania wieloma zdarzeniami automatyzacji interfejsu użytkownika, np. gdy duże fragmenty tekstu są drukowane na terminalu lub podczas słuchania wiadomości głosowych w komunikatorze WhatsApp. (#14888, #15169)
  * To nowe zachowanie można wyłączyć za pomocą nowego ustawienia "Użyj ulepszonego przetwarzania zdarzeń" w zaawansowanych ustawieniach NVDA.
* NVDA jest ponownie w stanie śledzić fokus w aplikacjach działających w ramach Windows Defender Application Guard (WDAG). (#15164)
* Tekst mowy nie jest już aktualizowany po poruszeniu myszą w przeglądarce mowy. (#15952, @hwf1324)
* NVDA ponownie przełączy się z powrotem w tryb przeglądania podczas zamykania pól kombi za pomocą "escape" lub "alt+strzałka w górę" w Firefoksie lub Chrome. (#15653)
* Naciskanie strzałek w górę i w dół w polach kombi w iTunes nie będzie już nieprawidłowo przełączać z powrotem do trybu przeglądania. (#15653)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Uwaga: jest to wersja niezgodna z interfejsem API dodatku.
Dodatki będą musiały zostać ponownie przetestowane i mieć zaktualizowany manifest.
* Kompilowanie NVDA wymaga teraz programu Visual Studio 2022.
Zapoznaj się z [NVDA docs](https://github.com/nvaccess/nvda/blob/release-2024.1/projectDocs/dev/createDevEnvironment.md), aby uzyskać szczegółową listę składników programu Visual Studio. (#14313)
* Dodano następujące punkty rozszerzenia:
  * "treeInterceptorHandler.post_browseModeStateChange". (#14969, @nvdaes)
  * 'speech.speechAnulowano'. (#15700, @LeonarddeR)
  * "_onErrorSoundRequested" (należy pobrać metodę "logHandler.getOnErrorSoundRequested())" (#15691, @CyrilleB79)
* Możliwe jest teraz używanie liczby mnogiej w tłumaczeniach dodatku. (#15661, @beqabeqa473)
* Zawarte w dystrybucji binarnej python3.dll do użytku przez dodatki z zewnętrznymi bibliotekami wykorzystującymi [stabilne ABI](https://docs.python.org/3.11/c-api/stable.html). (#15674, @mzanm)
* Klasa bazowa "BrailleDisplayDriver" ma teraz właściwości "numRows" i "numCols", które dostarczają informacji o wielowierszowych monitorach brajlowskich.
Ustawienie "numCells" jest nadal obsługiwane dla jednowierszowych monitorów brajlowskich, a "numCells" zwróci całkowitą liczbę komórek dla wielowierszowych monitorów brajlowskich. (#15386)
* Zaktualizowano BrlAPI dla BRLTTY do wersji 0.8.5, a odpowiadający mu moduł Pythona do kompilacji zgodnej z Pythonem 3.11. (#15652, @LeonarddeR)
* Dodano funkcję 'speech.speakSsml', która pozwala na zapisywanie sekwencji mowy NVDA za pomocą [SSML](https://www.w3.org/TR/speech-synthesis11/). (#15699, @LeonarddeR)
  * Następujące znaczniki są obecnie obsługiwane i tłumaczone na odpowiednie polecenia głosowe NVDA:
    * "Prosody" ("wysokość", "szybkość" i "głośność"). Obsługiwane jest tylko mnożenie (np. "200%").
    * "powiedz jako" z atrybutem "interpret" ustawionym na "znaki"
    * 'voice' z 'xml:lang' ustawionym na język XML
    * 'break' z atrybutem 'time' ustawionym na wartość w milisekundach, np. '200ms'
    * "mark" z atrybutem "name" ustawionym na nazwę znaku, np. "mark1", wymaga podania wywołania zwrotnego
  * Przykład: 'speech.speakSsml('<speak><prosody pitch="200%">hello</prosody><break j="1/"><prosody rate="50%">John</prosody></break></speak>')"
  * Możliwości analizowania SSML są wspierane przez klasę "SsmlParser" w module "speechXml".
* Zmiany w bibliotece klienta kontrolera NVDA:
  * Nazwy plików biblioteki nie zawierają już sufiksu oznaczającego architekturę, np. 'nvdaControllerClient32/64.dll' nazywa się teraz 'nvdaControllerClient.dll'. (#15718, #15717, @LeonarddeR)
  * Dodano przykład, aby zademonstrować użycie nvdaControllerClient.dll z Rusta. (#15771, @LeonarddeR)
  * Dodano następujące funkcje do klienta kontrolera: (#15734, #11028, #5638, @LeonarddeR)
    * 'nvdaController_getProcessId': Aby uzyskać identyfikator procesu (PID) bieżącej instancji NVDA, której używa klient kontrolera.
    * 'nvdaController_speakSsml': Aby poinstruować NVDA, aby mówiła zgodnie z podanym SSML. Ta funkcja obsługuje również:
      * Podanie poziomu symbolu.
      * Zapewnienie pierwszeństwa mowy, która ma być wypowiedziana.
      * Mówienie zarówno synchronicznie (blokowanie), jak i asynchronicznie (natychmiastowy powrót).
    * "nvdaController_setOnSsmlMarkReachedCallback": aby zarejestrować wywołanie zwrotne typu "onSsmlMarkReachedFuncType", które jest wywoływane w trybie synchronicznym dla każdego tagu "<mark />" napotkanego w sekwencji SSML podanej do "nvdaController_speakSsml".
  * Uwaga: nowe funkcje w kliencie kontrolera obsługują tylko NVDA 2024.1 i nowsze.
* Zaktualizowane zależności "include":
  * detours to `4b8c659f549b0ab21cf649377c7a84eb708f5e68`. (#15695)
  * IA2 na '3d8c7f0b833453f761ded6b12d8be431507BFE0b'. (#15695)
  * Sonic na '8694c596378c24e340c09ff2cd47c065494233f1'. (#15695)
  * w3c-aria-practices na '9a5e55ccbeb0f1bf92b6127c9865da8426d1c864'. (#15695)
  * wil na '5e9be7b2d2fe3834a7107f430f7d4c0631f69833'. (#15695)
* Informacje o urządzeniu dostarczone przez "hwPortUtils.listUsbDevices" zawierają teraz zgłoszony przez magistralę opis urządzenia USB (klucz "busReportedDeviceDescription"). (#15764, @LeonarddeR)
* For USB serial devices, `bdDetect.getConnectedUsbDevicesForDriver` and `bdDetect.getDriversForConnectedUsbDevices` now yield device matches containing a `deviceInfo` dictionary enriched with data about the USB device, such as `busReportedDeviceDescription`. (#15764, @LeonarddeR)
* Gdy plik konfiguracyjny "nvda.ini" jest uszkodzony, kopia zapasowa jest zapisywana przed jego ponowną inicjalizacją. (#15779, @CyrilleB79)
* Podczas definiowania skryptu za pomocą dekoratora skryptu można określić argument logiczny "speakOnDemand", aby kontrolować, czy skrypt powinien mówić w trybie mowy "na żądanie". (#481, @CyrilleB79)
  * Skrypty, które dostarczają informacji (np. tytuł okna, czas/data raportu) powinny mówić w trybie "na żądanie".
  * Skrypty, które wykonują jakąś akcję (np. przesunięcie kursora, zmianę parametru) nie powinny mówić w trybie "na żądanie".
* Naprawiono błąd polegający na tym, że usunięcie plików śledzonych przez git podczas "scons -c" powodowało brak interfejsów COM UIA podczas przebudowy. (#7070, #10833, @hwf1324)
* Naprawiono usterkę polegającą na tym, że niektóre zmiany kodu nie były wykrywane podczas kompilowania "dist", co uniemożliwiało wyzwolenie nowej kompilacji.
Teraz 'dist' zawsze się odbudowuje. (#13372, @hwf1324)
* Element 'gui.nvdaControls.MessageDialog' z domyślnym typem standardu nie zgłasza już wyjątku konwersji None, ponieważ nie jest przypisany żaden dźwięk. (#16223, @XLTechie)

#### Zmiany powodujące niezgodność interfejsu API

Są to zmiany w interfejsie API powodujące niezgodność.
Otwórz problem z usługą GitHub, jeśli Twój dodatek ma problem z aktualizacją do nowego interfejsu API.

* NVDA jest teraz zbudowany w Pythonie 3.11. (#12064)
* Zaktualizowane zależności:
  * configobj to 5.1.0dev commit `e2ba4457c4651fa54f8d59d8dcdd3da950e956b8`. (#15544)
  * Łączy się z wersją 1.2.0. (#15513, @codeofdusk)
  * Flake8 do 4.0.1. (#15636, @lukaszgo1)
  * py2exe do 0.13.0.1dev commit '4e7b2b2c60face592e67cb1bc935172a20fa371d'. (#15544)
  * robotframework do wersji 6.1.1. (#15544)
  * SCons do 4.5.2. (#15529, @LeonarddeR)
  * sfinks do 7.2.6. (#15544)
  * wxPython do zatwierdzenia 4.2.2a '0205c7c1b9022a5de3e3543f9304cfe53a32b488'. (#12551, #16257)
* Usunięto zależności:
  * typing_extensions, powinny one być obsługiwane natywnie w języku Python 3.11 (#15544)
  * nose, zamiast tego unittest-xml-reporting jest używany do generowania raportów XML. (#15544)
* Usunięto element "IAccessibleHandler.SecureDesktopNVDAObject".
Zamiast tego, gdy NVDA jest uruchomiony na profilu użytkownika, śledź istnienie bezpiecznego pulpitu za pomocą punktu rozszerzenia: 'winAPI.secureDesktop.post_secureDesktopStateChange'. (#14488)
* "Alfabet Braille'a. BrailleHandler.handlePendingCaretUpdate' został usunięty bez publicznego zastąpienia. (#15163, @LeonarddeR)
* `bdDetect.addUsbDevices and bdDetect.addBluetoothDevices` have been removed.
Sterowniki monitorów brajlowskich powinny zamiast tego implementować metodę klasy 'registerAutomaticDetection'.
Metoda ta odbiera obiekt "DriverRegistrar", na którym można użyć metod "addUsbDevices" i "addBluetoothDevices". (#15200, @LeonarddeR)
* The default implementation of the check method on `BrailleDisplayDriver` now requires both the `threadSafe` and `supportsAutomaticDetection` attributes to be set to `True`. (#15200, @LeonarddeR)
* Passing lambda functions to `hwIo.ioThread.IoThread.queueAsApc` is no longer possible, as functions should be weakly referenceable. (#14627, @LeonarddeR)
* Plik "IoThread.autoDeleteApcReference" został usunięty. (#14924, @LeonarddeR)
* Aby obsługiwać zmiany wysokości dźwięku wielkich liter, syntezatory muszą teraz jawnie zadeklarować swoje wsparcie dla "PitchCommand" w atrybucie "supportedCommands" na sterowniku. (#15433, @LeonarddeR)
* `speechDictHandler.speechDictVars` has been removed. Use `NVDAState.WritePaths.speechDictsDir` instead of `speechDictHandler.speechDictVars.speechDictsPath`. (#15614, @lukaszgo1)
* Usunięto 'languageHandler.makeNpgettext' i 'languageHandler.makePgettext'.
'npgettext' i 'pgettext' są teraz obsługiwane natywnie. (#15546)
* Moduł aplikacji dla [Poedit](https://poedit.net) został znacznie zmieniony. Funkcja 'fetchObject' została usunięta. (#15313, #7303, @LeonarddeR)
* Następujące nadmiarowe typy i stałe zostały usunięte z "hwPortUtils": (#15764, @LeonarddeR)
  * "PCWSTR"
  * 'HWND' (zastąpiony przez 'ctypes.wintypes.HWND')
  * "ULONG_PTR"
  * 'ULONGLONG'
  * "NULL"
  * "GUID" (zastąpiony przez "comtypes. Identyfikator GUID')
* Plik 'gui.addonGui.AddonsDialog' został usunięty. (#15834)
* Element "touchHandler.TouchInputGesture.multiFingerActionLabel" został usunięty bez zastępowania. (#15864, @CyrilleB79)
* Znak "NVDAObjects.IAccessible.winword.WordDocument.script_reportCurrentHeaders" został usunięty bez zastępstwa. (#15904, @CyrilleB79)
* Następujące moduły aplikacji zostaną usunięte.
Kod, który importuje z jednego z nich, powinien zamiast tego zostać zaimportowany z modułu zastępczego. (#15618, @lukaszgo1)

| Usunięto nazwę modułu |Moduł zastępczy|
|---|---|
|'azardi-2.0' |'azardi20'|
|'AzureDataStudio' |'kod'|
|'AzureDataStudio-insiders' |'kod'|
|'CalculatorApp' |'Kalkulator'|
|'code - insiders' |'kod'|
|'commsapps' |'hxmail'|
|'dbeaver' |'zaćmienie'|
|'digitaleditionspreview' |'digitaleditions'|
|'esybraille' |'esysuite'|
|'hxoutlook' |'hxmail'|
|'Miranda64' |'Miranda32'|
|'mpc-hc' |'mplayerc'|
|'mpc-hc64' |'mplayerc'|
|'notepad++' |'notepadPlusPlus'|
|'searchapp' |'searchui'|
|'searchhost' |'searchUI'|
|'springtoolsuite4' |'zaćmienie'|
|'sts' |'zaćmienie'|
|`teamtalk3` |`teamtalk4classic`|
|'textinputhost' |'windowsinternal_composableshell_experiences_textinput_inputapp'|
|'totalcmd64' |'totalcmd'|
|'win32calc' |'calc'|
|'winmail' |'msimn'|
|'zend-eclipse-php' |'zaćmienie'|
|'zendstudio' |'zaćmienie'|

#### Przestarzałe

* Używanie "watchdog.getFormattedStacksForAllThreads" jest przestarzałe - zamiast tego użyj "logHandler.getFormattedStacksForAllThreads". (#15616, @lukaszgo1)
* Plik "easeOfAccess.canConfigTerminateOnDesktopSwitch" został uznany za przestarzały, ponieważ stał się przestarzały, ponieważ system Windows 7 nie jest już obsługiwany. (#15644, @LeonarddeR)
* Parametr "winVersion.isFullScreenMagnificationAvailable" został uznany za przestarzały — zamiast niego należy użyć parametru "visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart". (#15664, @josephsl)
* Następujące stałe wydania systemu Windows zostały uznane za przestarzałe z modułu winVersion (#15647, @josephsl):
  * 'winVersion.WIN7'
  * "winVersion.WIN7_SP1"
  * 'winVersion.WIN8'
* Stałe "bdDetect.KEY_*" zostały uznane za przestarzałe.
Zamiast tego użyj "bdDetect.DeviceType.*". (#15772, @LeonarddeR).
* Stałe "bdDetect.DETECT_USB" i "bdDetect.DETECT_BLUETOOTH" zostały uznane za przestarzałe i nie zostały zastąpione publicznie. (#15772, @LeonarddeR).
* Korzystanie z 'gui. ExecAndPump' jest przestarzały - zamiast tego użyj 'systemUtils.ExecAndPump'. (#15852, @lukaszgo1)

## 2023.3.4

Jest to poprawka mająca na celu rozwiązanie problemu z zabezpieczeniami i instalatora.
Prosimy o odpowiedzialne ujawnianie problemów związanych z bezpieczeństwem zgodnie z [polityką bezpieczeństwa](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki zabezpieczeń

* Zapobiega ładowaniu konfiguracji niestandardowej, gdy wymuszony jest tryb bezpieczny.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Poprawki błędów

* Naprawiono błąd, który powodował, że proces NVDA nie kończył się poprawnie. (#16123)
* Naprawiono błąd polegający na tym, że jeśli poprzedni proces NVDA nie zakończył się poprawnie, instalacja NVDA mogła zakończyć się nieodwracalnym stanem. (#16122)

## 2023.3.3

Jest to poprawka mająca na celu rozwiązanie problemu z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie problemów związanych z bezpieczeństwem zgodnie z [polityką bezpieczeństwa](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki zabezpieczeń

* Zapobiega możliwemu odbiciu ataku XSS ze spreparowanej zawartości, który mógłby spowodować wykonanie dowolnego kodu.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Jest to poprawka mająca na celu rozwiązanie problemu z zabezpieczeniami.
Poprawka zabezpieczeń w 2023.3.1 nie została poprawnie usunięta.
Prosimy o odpowiedzialne ujawnianie problemów związanych z bezpieczeństwem zgodnie z [polityką bezpieczeństwa](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki zabezpieczeń

* Poprawka zabezpieczeń w 2023.3.1 nie została poprawnie usunięta.
Zapobiega możliwemu dostępowi do systemu i wykonaniu dowolnego kodu z uprawnieniami systemowymi dla nieuwierzytelnionych użytkowników.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

Jest to poprawka mająca na celu rozwiązanie problemu z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie problemów związanych z bezpieczeństwem zgodnie z [polityką bezpieczeństwa](https://github.com/nvaccess/nvda/blob/master/security.md).

### Poprawki zabezpieczeń

* Zapobiega możliwemu dostępowi do systemu i wykonaniu dowolnego kodu z uprawnieniami systemowymi dla nieuwierzytelnionych użytkowników.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

To wydanie zawiera ulepszenia wydajności, responsywności i stabilności wyjścia audio.
Dodano opcje do kontrolowania głośności dźwięków i sygnałów dźwiękowych NVDA, lub do podążania za głośnością głosu, którego używasz.

NVDA może teraz okresowo odświeżać wyniki OCR, odczytując nowy tekst w miarę jego pojawiania się.
Można to skonfigurować w kategorii OCR systemu Windows w oknie ustawień NVDA.

Wprowadzono kilka poprawek w alfabecie Braille'a, poprawiając wykrywanie urządzeń i ruch karetki higienicznej.
Teraz można zrezygnować z automatycznego wykrywania niechcianych sterowników, aby poprawić wydajność automatycznego wykrywania.
Dostępne są również nowe komendy BRLTTY.

Wprowadzono również poprawki błędów w sklepie z dodatkami, pakiecie Microsoft Office, menu kontekstowych przeglądarki Microsoft Edge i Kalkulatorze systemu Windows.

### Nowe funkcje

* Ulepszone zarządzanie dźwiękiem:
  * Nowy panel Ustawienia dźwięku:
    * Można to otworzyć za pomocą 'NVDA+control+u'. (#15497)
    * Opcja w ustawieniach dźwięku, aby głośność dźwięków i sygnałów dźwiękowych NVDA była zgodna z ustawieniem głośności głosu, którego używasz. (#1409)
    * Opcja w ustawieniach audio do oddzielnej konfiguracji głośności dźwięków NVDA. (#1409, #15038)
    * Ustawienia zmiany urządzenia wyjściowego audio i przełączania wyciszania dźwięku zostały przeniesione do nowego panelu ustawień audio z okna dialogowego Wybierz syntezator.
    Te opcje zostaną usunięte z okna dialogowego "wybierz syntezator" w 2024 roku.1. (#15486, #8711)
  * NVDA będzie teraz wyprowadzać dźwięk za pośrednictwem interfejsu API Windows Audio Session (WASAPI), co może poprawić responsywność, wydajność i stabilność mowy i dźwięków NVDA. (#14697, #11169, #11615, #5096, #10185, #11061)
  * Uwaga: WASAPI jest niekompatybilny z niektórymi dodatkami.
  Kompatybilne aktualizacje są dostępne dla tych dodatków, prosimy o ich aktualizację przed aktualizacją NVDA.
  Niekompatybilne wersje tych dodatków zostaną wyłączone podczas aktualizacji NVDA:
    * Tony's Enhancements w wersji 1.15 lub starszej. (#15402)
    * Rozszerzenie globalnych poleceń NVDA 12.0.8 lub starsze. (#15443)
* NVDA jest teraz w stanie stale aktualizować wynik podczas optycznego rozpoznawania znaków (OCR), czytając nowy tekst w miarę jego pojawiania się. (#2797)
  * Aby włączyć tę funkcję, włącz opcję "Okresowo odświeżaj rozpoznaną zawartość" w kategorii OCR systemu Windows w oknie dialogowym ustawień NVDA.
  * Po włączeniu tej opcji możesz przełączać się między nowymi zmianami w treści, przełączając dynamiczne zmiany zawartości raportu (naciskając 'NVDA+5').
* Podczas korzystania z automatycznego wykrywania monitorów brajlowskich można teraz wyłączyć wykrywanie sterowników w oknie dialogowym wyboru monitora brajlowskiego. (#15196)
* Nowa opcja w ustawieniach formatowania dokumentu, "Ignoruj puste wiersze w raportowaniu wcięć wierszy". (#13394)
* Dodano nieprzypisany gest do nawigowania według grupowania kart w trybie przeglądania. (#15046)

### Zmiany

* Przywołuje monitor brajlowski do komórki brajlowskiej |`routing`
  * Gdy tekst w terminalu zmieni się bez aktualizacji daszka, tekst na monitorze brajlowskim będzie teraz poprawnie aktualizowany po umieszczeniu w zmienionym wierszu.
  Dotyczy to również sytuacji, w których pismo Braille'a jest powiązane z recenzją. (#15115)
  * Więcej powiązań BRLTTY jest teraz mapowanych na polecenia NVDA (#6483):
    * 'learn': przełącza pomoc przy wprowadzaniu NVDA
    * 'prefmenu': otwórz menu NVDA
    * 'prefload'/'prefsave': Wczyt/zapisz konfigurację NVDA
    * 'time': Pokaż czas
    * "say_line": Odczyt bieżącego wiersza, w którym znajduje się kursor recenzji
    * "say_below": Powiedz wszystko za pomocą kursora recenzji
  * Sterownik BRLTTY jest dostępny tylko wtedy, gdy uruchomiona jest instancja BRLTTY z włączonym interfejsem BrlAPI. (#15335)
  * Zaawansowane ustawienie włączające obsługę alfabetu Braille'a HID zostało usunięte na rzecz nowej opcji.
  Można teraz wyłączyć określone sterowniki do automatycznego wykrywania monitora brajlowskiego w oknie dialogowym wyboru monitora brajlowskiego. (#15196)
* Sklep z dodatkami: Zainstalowane dodatki będą teraz wyświetlane na karcie Dostępne dodatki, jeśli są dostępne w sklepie. (#15374)
* Niektóre skrótów zostały zaktualizowane w menu NVDA. (#15364)

### Poprawki błędów

* Microsoft Office:
  * Naprawiono awarię w programie Microsoft Word, gdy opcje formatowania dokumentu "nagłówki raportu" oraz "komentarze i notatki raportu" nie były włączone. (#15019)
  * W programach Word i Excel wyrównanie tekstu będzie poprawnie raportowane w większej liczbie sytuacji. (#15206, #15220)
  * Naprawia ogłaszanie niektórych skrótów formatowania komórek w programie Excel. (#15527)
* Microsoft Edge:
  * NVDA nie będzie już przeskakiwać z powrotem do ostatniej pozycji trybu przeglądania po otwarciu menu kontekstowego w Microsoft Edge. (#15309)
  * NVDA po raz kolejny jest w stanie odczytywać menu kontekstowe pobranych plików w Microsoft Edge. (#14916)
* Przywołuje monitor brajlowski do komórki brajlowskiej |`routing`
  * Kursor brajlowski i wskaźniki wyboru będą teraz zawsze poprawnie aktualizowane po wyświetleniu lub ukryciu odpowiednich wskaźników za pomocą gestu. (#15115)
  * Naprawiono błąd, który sprawiał, że monitory brajlowskie Albatross próbowały się zainicjować, mimo że podłączone było inne urządzenie brajlowskie. (#15226)
* Sklep z dodatkami:
  * Naprawiono błąd, który powodował, że odznaczenie opcji "uwzględnij niekompatybilne dodatki" powodowało, że niekompatybilne dodatki nadal były wyświetlane w sklepie. (#15411)
  * Dodatki zablokowane ze względu na kompatybilność powinny być teraz poprawnie filtrowane podczas przełączania filtra dla stanu włączonego/wyłączonego. (#15416)
  * Naprawiono błąd uniemożliwiający uaktualnienie lub zastąpienie nadpisanych włączonych niekompatybilnych dodatków za pomocą zewnętrznego narzędzia instalacyjnego. (#15417)
  * Naprawiono błąd, który sprawiał, że NVDA nie mówiła, dopóki nie została ponownie uruchomiona po instalacji dodatku. (#14525)
  * Naprawiono błąd polegający na tym, że nie można było zainstalować dodatków, jeśli poprzednie pobieranie nie powiodło się lub zostało anulowane. (#15469)
  * Naprawiono problemy z obsługą niekompatybilnych dodatków podczas aktualizacji NVDA. (#15414, #15412, #15437)
* NVDA po raz kolejny ogłasza wyniki obliczeń w kalkulatorze Windows 32bit w wersjach Server, LTSC i LTSB systemu Windows. (#15230)
* NVDA nie ignoruje już zmian fokusu, gdy zagnieżdżone okno (wielkie okno podrzędne) jest aktywne. (#15432)
* Naprawiono potencjalną przyczynę zawieszania się gry podczas uruchamiania NVDA. (#15517)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Nazwy 'braille.handler.handleUpdate' i 'braille.handler.handleReviewMove' zostały zmienione tak, aby nie aktualizowały się natychmiast.
Przed tą zmianą, gdy którakolwiek z tych metod była wywoływana bardzo często, pochłaniało to wiele zasobów.
Te metody teraz zamiast tego kolejkują aktualizację na koniec każdego cyklu podstawowego.
Powinny być również bezpieczne wątkowo, aby można było je wywoływać z wątków w tle. (#15163)
* Dodano oficjalne wsparcie dla rejestracji niestandardowych sterowników monitorów brajlowskich w procesie automatycznego wykrywania monitorów brajlowskich.
Zapoznaj się z dokumentem "Braille'a. Dokumentacja klasy BrailleDisplayDriver, aby uzyskać więcej informacji.
Most notably, the `supportsAutomaticDetection` attribute must be set to `True` and the `registerAutomaticDetection` `classmethod` must be implemented.  (#15196)

#### Przestarzałe

* "Alfabet Braille'a. BrailleHandler.handlePendingCaretUpdate' jest teraz przestarzały i nie ma go publicznie zastępowane.
Zostanie usunięty w 2024 roku.1. (#15163)
* Importing the constants `xlCenter`, `xlJustify`, `xlLeft`, `xlRight`, `xlDistributed`, `xlBottom`, `xlTop` from `NVDAObjects.window.excel` is deprecated.
Zamiast tego użyj wyliczeń "XlHAlign" lub "XlVAlign". (#15205)
* Mapowanie "NVDAObjects.window.excel.alignmentLabels" jest przestarzałe.
Zamiast tego należy użyć metod 'displayString' wyliczeń 'XlHAlign' lub 'XlVAlign'. (#15205)
* Pliki "bdDetect.addUsbDevices" i "bdDetect.addBluetoothDevices" zostały uznane za przestarzałe.
Sterowniki monitorów brajlowskich powinny zamiast tego implementować metodę klasy 'registerAutomaticDetection'.
Metoda ta odbiera obiekt "DriverRegistrar", na którym można użyć metod "addUsbDevices" i "addBluetoothDevices". (#15200)
* Domyślna implementacja metody sprawdzania w 'BrailleDisplayDriver' używa 'bdDetect.driverHasPossibleDevices' dla urządzeń, które są oznaczone jako bezpieczne wątkowo.
Począwszy od NVDA 2024.1, aby metoda podstawowa używała "bdDetect.driverHasPossibleDevices", atrybut "supportsAutomaticDetection" musi być również ustawiony na wartość "True". (#15200)

## 2023.2

W tym wydaniu wprowadzono Sklep z dodatkami, który zastąpi Menedżera dodatków.
W sklepie z dodatkami możesz przeglądać, wyszukiwać, instalować i aktualizować dodatki społecznościowe.
Możesz teraz ręcznie zastąpić problemy z niekompatybilnością z nieaktualnymi dodatkami na własne ryzyko.

Dostępne są nowe funkcje, polecenia i obsługa monitorów w alfabecie Braille'a.
Dostępne są również nowe gesty wejściowe dla OCR i spłaszczonej nawigacji po obiektach.
Ulepszono formatowanie nawigacji i raportowania w pakiecie Microsoft Office.

Istnieje wiele poprawek błędów, szczególnie w alfabecie Braille'a, pakiecie Microsoft Office, przeglądarkach internetowych i systemie Windows 11.

Zaktualizowano eSpeak-NG, tłumacza brajlowskiego LibLouis i Unicode CLDR.

### Nowe funkcje

* Sklep z dodatkami został dodany do NVDA. (#13985)
  * Przeglądaj, wyszukuj, instaluj i aktualizuj dodatki społecznościowe.
  * Ręcznie zastąp problemy z niekompatybilnością za pomocą przestarzałych dodatków.
  * Menedżer dodatków został usunięty i zastąpiony przez sklep z dodatkami.
  * Aby uzyskać więcej informacji, przeczytaj zaktualizowany podręcznik użytkownika.
* Nowe gesty wprowadzania:
  * Niepowiązany gest do przełączania między dostępnymi językami dla OCR systemu Windows. (#13036)
  * Niepowiązany gest do przełączania między trybami wiadomości pokazu Braille'a. (#14864)
  * Niepowiązany gest do przełączania pokazujący wskaźnik zaznaczenia dla brajla. (#14948)
  * Dodano domyślne przypisania gestów klawiaturowych w celu przechodzenia do następnego lub poprzedniego obiektu w spłaszczonym widoku hierarchii obiektów. (#15053)
    * Pulpit: 'NVDA+numpad9' i 'NVDA+numpad3', aby przejść odpowiednio do poprzedniego i następnego obiektu.
    * Laptop: 'shift+NVDA+[' i 'shift+NVDA+]', aby przejść odpowiednio do poprzedniego i następnego obiektu.
* Nowe funkcje alfabetu Braille'a:
  * Dodano obsługę monitora brajlowskiego Help Tech Activator. (#14917)
  * Nowa opcja przełączania pokazującego wskaźnik zaznaczenia (punkty 7 i 8). (#14948)
  * Nowa opcja opcjonalnego przesuwania kursora systemowego lub fokusu podczas zmiany pozycji kursora przeglądania za pomocą przywoływania w alfabecie Braille'a. (#14885, #3166)
  * Po trzykrotnym naciśnięciu "numpad2" w celu wyświetlenia wartości numerycznej znaku w miejscu kursora podglądu, informacje są teraz wyświetlane również w alfabecie Braille'a. (#14826)
  * Dodano obsługę atrybutu ARIA 1.3 'aria-brailleroledescription', co pozwala autorom stron internetowych na nadpisanie typu elementu wyświetlanego na monitorze brajlowskim. (#14748)
  * Sterownik brajlowski Baum: dodano kilka gestów akordu Braille'a do wykonywania typowych poleceń klawiaturowych, takich jak "windows+d" i "alt+tab".
  Zapoznaj się z Podręcznikiem użytkownika NVDA, aby uzyskać pełną listę. (#14714)
* Dodano wymowę symboli Unicode:
  * Symbole brajlowskie, takie jak '⠐⠣⠃⠗⠇⠐⠜'. (#13778)
  * Symbol opcji Mac '⌥'. (#14682)
* Dodano gesty dla monitorów brajlowskich Tivomatic Caiku Albatross. (#14844, #15002)
  * Wyświetlanie okna dialogowego Ustawienia brajla
  * Uzyskiwanie dostępu do paska stanu
  * Przełączanie kształtu kursora brajlowskiego
  * Przełączanie w trybie pokazywania wiadomości brajlowskich
  * Włączanie/wyłączanie kursora Braille'a
  * Przełączanie stanu "Wskaźnik zaznaczenia brajlowskiego wyświetlacza"
  * Przełączanie w trybie "Braille Move System Daret podczas kursora przeglądu routingu". (#15122)
* Funkcje pakietu Microsoft Office:
  * Gdy w dokumencie jest włączone formatowanie wyróżnionego tekstu, kolory podświetlenia są teraz raportowane w programie Microsoft Word. (#7396, #12101, #5866)
  * Gdy kolory są włączone Formatowanie dokumentu, kolory tła są teraz raportowane w programie Microsoft Word. (#5866)
  * W przypadku korzystania ze skrótów programu Excel do przełączania formatu, takiego jak pogrubienie, kursywa, podkreślenie i przekreślenie komórki w programie Excel, wynik jest teraz raportowany. (#14923)
* Eksperymentalne ulepszone zarządzanie dźwiękiem:
  * NVDA może teraz wyprowadzać dźwięk za pośrednictwem interfejsu API Windows Audio Session (WASAPI), co może poprawić responsywność, wydajność i stabilność mowy i dźwięków NVDA. (#14697)
  * Korzystanie z WASAPI można włączyć w ustawieniach zaawansowanych.
  Dodatkowo, jeśli funkcja WASAPI jest włączona, można również skonfigurować następujące ustawienia zaawansowane.
    * Opcja, aby głośność dźwięków i sygnałów dźwiękowych NVDA była zgodna z ustawieniem głośności używanego głosu. (#1409)
    * Opcja oddzielnej konfiguracji głośności dźwięków NVDA. (#1409, #15038)
  * Istnieje znany problem z przerywanymi awariami, gdy włączona jest funkcja WASAPI. (#15150)
* W przeglądarkach Mozilla Firefox i Google Chrome, NVDA zgłasza teraz, kiedy kontrolka otwiera okno dialogowe, siatkę, listę lub drzewo, jeśli autor określił to za pomocą 'aria-haspopup'. (#8235)
* Możliwe jest teraz używanie zmiennych systemowych (takich jak '%temp%' lub '%homepath%') w specyfikacji ścieżki podczas tworzenia przenośnych kopii NVDA. (#14680)
* W aktualizacji systemu Windows 10 z maja 2019 r. i nowszych NVDA może ogłaszać nazwy pulpitów wirtualnych podczas ich otwierania, zmieniania i zamykania. (#5641)
* Dodano parametr dla całego systemu, aby umożliwić użytkownikom i administratorom systemu wymuszenie uruchomienia NVDA w trybie bezpiecznym. (#10018)

### Zmiany

* Aktualizacje komponentów:
  * eSpeak NG został zaktualizowany do wersji 1.52-dev commit 'ed9a7bcf'. (#15036)
  * Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)
  * CLDR został zaktualizowany do wersji 43.0. (#14918)
* Zmiany w LibreOffice:
  * Podczas raportowania położenia kursora recenzji bieżące położenie kursora/kursora jest teraz podawane względem bieżącej strony w programie LibreOffice Writer 7.6 i nowszych, podobnie jak w przypadku programu Microsoft Word. (#11696)
  * Ogłaszanie paska stanu (np. uruchamianego przez 'NVDA+end') działa dla LibreOffice. (#11698)
  * Po przejściu do innej komórki w LibreOffice Calc NVDA nie odczytuje już nieprawidłowo współrzędnych poprzednio aktywowanej komórki, gdy ogłaszanie współrzędnych komórki jest wyłączone w ustawieniach NVDA. (#15098)
* Zmiany w alfabecie Braille'a:
  * W przypadku korzystania z monitora brajlowskiego za pomocą standardowego sterownika brajlowskiego HID, pad kierunkowy może być używany do emulacji strzałek i Enter.
  Ponadto "spacja+punkt1" i "spacja+punkt4" są teraz mapowane odpowiednio na strzałki w górę i w dół. (#14713)
  * Aktualizacje dynamicznej zawartości internetowej (dynamiczne regiony ARCHI) są teraz wyświetlane w alfabecie Braille'a.
  Można tę opcję wyłączyć w panelu Ustawienia zaawansowane. (#7756)
* Symbole myślnika i pauzy zawsze będą wysyłane do syntezatora. (#13830)
* Odległość podawana w programie Microsoft Word będzie teraz uwzględniać jednostkę zdefiniowaną w opcjach zaawansowanych programu Word, nawet jeśli dostęp do dokumentów programu Word jest używany przez interfejs użytkownika. (#14542)
* NVDA reaguje szybciej podczas przesuwania kursora w kontrolkach edycji. (#14708)
* Skrypt do raportowania miejsca docelowego łącza teraz raportuje z pozycji kursora / fokusu, a nie z obiektu nawigatora. (#14659)
* Przenośne tworzenie kopii nie wymaga już wprowadzania litery dysku jako części ścieżki bezwzględnej. (#14680)
* Jeśli system Windows jest skonfigurowany do wyświetlania sekund w zegarze zasobnika systemowego, użycie 'NVDA+f12' do raportowania czasu teraz uwzględnia to ustawienie. (#14742)
* NVDA będzie teraz raportować nieoznaczone grupy, które zawierają przydatne informacje o pozycji, takie jak w najnowszych wersjach menu Microsoft Office 365. (#14878)

### Poprawki błędów

* Przywołuje monitor brajlowski do komórki brajlowskiej |`routing`
  * Kilka poprawek stabilności wejścia/wyjścia dla monitorów brajlowskich, co skutkuje rzadszymi błędami i awariami NVDA. (#14627)
  * NVDA nie będzie już niepotrzebnie przełączać się na brak brajla wiele razy podczas automatycznego wykrywania, co skutkuje czystszym dziennikiem i mniejszym obciążeniem. (#14524)
  * NVDA przełączy się teraz z powrotem na USB, jeśli urządzenie HID Bluetooth (takie jak HumanWare Brailliant lub APH Mantis) zostanie automatycznie wykryte i połączenie USB stanie się dostępne.
  Wcześniej działało to tylko w przypadku portów szeregowych Bluetooth. (#14524)
  * Jeśli żaden monitor brajlowski nie jest podłączony, a przeglądarka brajlowska zostanie zamknięta przez naciśnięcie Alt+F4 lub kliknięcie przycisku zamykania, rozmiar wyświetlacza w podsystemie brajlowskim zostanie ponownie zresetowany do zera komórek. (#15214)
* Przeglądarki internetowe:
  * NVDA nie powoduje już sporadycznie awarii przeglądarki Mozilla Firefox lub nie przestaje odpowiadać. (#14647)
  * W przeglądarkach Mozilla Firefox i Google Chrome wpisywane znaki nie są już zgłaszane w niektórych polach tekstowych, nawet jeśli opcja Czytaj wpisane znaki jest wyłączona. (#8442)
  * Możesz teraz korzystać z trybu przeglądania w Chromium Embedded Controls, gdzie wcześniej nie było to możliwe. (#13493, #8553)
  * W przeglądarce Mozilla Firefox przesunięcie kursora myszy nad tekst po kliknięciu linku niezawodnie informuje o tekście. (#9235)
  * Miejsce docelowe linków graficznych jest teraz w większej liczbie przypadków dokładnie raportowane w Chrome i Edge. (#14783)
  * Podczas próby zgłoszenia adresu URL linku bez atrybutu href, NVDA nie jest już cicha.
  Zamiast tego NVDA informuje, że łącze nie ma miejsca docelowego. (#14723)
  * W trybie przeglądania, NVDA nie będzie już niepoprawnie ignorować fokusu przenoszącego się do kontrolki nadrzędnej lub podrzędnej, np. przejścia z kontrolki do jej nadrzędnego elementu listy lub komórki siatki. (#14611)
    * Należy jednak pamiętać, że ta poprawka ma zastosowanie tylko wtedy, gdy opcja Automatycznie ustaw ostrość na elementy, na których można ustawić ostrość" w ustawieniach trybu przeglądania jest wyłączona (co jest ustawieniem domyślnym).
* Poprawki dla systemu Windows 11:
  * NVDA może po raz kolejny ogłaszać zawartość paska stanu Notatnika. (#14573)
  * Przełączanie między kartami ogłosi nazwę i pozycję nowej karty w Notatniku i Eksploratorze plików. (#14587, #14388)
  * NVDA po raz kolejny ogłosi pozycje kandydujące podczas wprowadzania tekstu w językach takich jak chiński i japoński. (#14509)
  * Ponownie możliwe jest otwarcie pozycji Współtwórcy i Licencja w menu Pomocy NVDA. (#14725)
* Poprawki pakietu Microsoft Office:
  * Podczas szybkiego przechodzenia między komórkami w programie Excel, NVDA jest teraz mniej prawdopodobne, że zgłosi niewłaściwą komórkę lub zaznaczenie. (#14983, #12200, #12108)
  * Po wylądowaniu na komórce programu Excel spoza arkusza roboczego pismo Braille'a i zakreślacz ostrości nie są już niepotrzebnie aktualizowane do obiektu, który wcześniej był aktywny. (#15136)
  * NVDA nie przerywa już ogłaszania skupienia pól haseł w programach Microsoft Excel i Outlook. (#14839)
* W przypadku symboli, które nie mają opisu symbolu w bieżących ustawieniach regionalnych, zostanie użyty domyślny poziom symbolu angielskiego. (#14558, #14417)
* Teraz można użyć znaku odwrotnego ukośnika w polu zastępczym wpisu słownika, gdy typ nie jest ustawiony na wyrażenie regularne. (#14556)
* W Kalkulatorze Windows 10 i 11 przenośna kopia NVDA nie będzie już nic robić ani odtwarzać dźwięków błędów podczas wprowadzania wyrażeń w standardowym kalkulatorze w trybie kompaktowej nakładki. (#14679)
* NVDA ponownie odzyskuje sprawność po wielu innych sytuacjach, takich jak aplikacje, które przestają odpowiadać, co wcześniej powodowało całkowite zamrożenie. (#14759)
* Podczas wymuszania obsługi UIA z niektórymi terminalami i konsolami, naprawiany jest błąd, który powodował zawieszanie się i spamowanie pliku dziennika. (#14689)
* NVDA nie będzie już odmawiać zapisania konfiguracji po zresetowaniu konfiguracji. (#13187)
* Podczas uruchamiania tymczasowej wersji z programu uruchamiającego, NVDA nie wprowadzi użytkowników w błąd, myśląc, że mogą zapisać konfigurację. (#14914)
* NVDA teraz ogólnie reaguje nieco szybciej na polecenia i zmiany fokusu. (#14928)
* Wyświetlanie ustawień OCR nie zakończy się już niepowodzeniem w niektórych systemach. (#15017)
* Naprawiono błąd związany z zapisywaniem i wczytywaniem konfiguracji NVDA, w tym przełączaniem syntezatorów. (#14760)
* Naprawiono błąd powodujący, że gest dotykowy "przesuń w górę" recenzji tekstu przesuwał strony, a nie przechodził do poprzedniego wiersza. (#15127)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Sugerowane konwencje zostały dodane do specyfikacji manifestu dodatku.
Są one opcjonalne ze względu na zgodność z NVDA, ale są zalecane lub wymagane do przesłania do Sklepu z dodatkami. (#14754)
  * Użyj "małych liter Camel" w polu nazwy.
  * Za pomocą przycisku '<major>.<minor>. <patch>' dla pola wersji (wymagany w przypadku dodatkowego magazynu danych).</patch></minor></major>
  * Użyj wartości "https://" jako schematu dla pola adresu URL (wymagany w przypadku dodatkowego magazynu danych).
* Dodano nowy typ punktu rozszerzenia o nazwie "Łańcuch", który może być używany do iteracji po iteracjach zwracanych przez zarejestrowane programy obsługi. (#14531)
* Dodano punkt rozszerzenia "bdDetect.scanForDevices".
Można rejestrować programy obsługi, które dają pary "BrailleDisplayDriver/DeviceMatch", które nie pasują do istniejących kategorii, takich jak USB lub Bluetooth. (#14531)
* Dodano punkt rozszerzenia: 'synthDriverHandler.synthChanged'. (#14618)
* Pierścień ustawień syntezatora NVDA buforuje teraz dostępne wartości ustawień za pierwszym razem, gdy są potrzebne, a nie podczas ładowania syntezatora. (#14704)
* Teraz możesz wywołać metodę eksportu na mapie gestów, aby wyeksportować ją do słownika.
Ten słownik można zaimportować w innym geście, przekazując go do konstruktora "GlobalGestureMap" lub do metody update na istniejącej mapie. (#14582)
* "hwIo.base.IoBase" i jego pochodne mają teraz nowy parametr konstruktora, który przyjmuje "hwIo.ioThread.IoThread".
Jeśli nie zostanie podany, używany jest gwint domyślny. (#14627)
* "hwIo.ioThread.IoThread" ma teraz metodę "setWaitableTimer" do ustawiania licznika czasu oczekiwania za pomocą funkcji Pythona.
Podobnie, nowa metoda 'getCompletionRoutine' pozwala na bezpieczne przekształcenie metody Pythona w procedurę uzupełniania. (#14627)
* "Offsety. OffsetsTextInfo._get_boundingRects' powinien teraz zawsze zwracać wartość "List[locationHelper.rectLTWH]" zgodnie z oczekiwaniami dla podklasy "textInfos.TextInfo". (#12424)
* "Highlight-color" jest teraz atrybutem pola formatu. (#14610)
* NVDA powinna dokładniej określić, czy zarejestrowana wiadomość pochodzi z rdzenia NVDA. (#14812)
* NVDA nie będzie już rejestrować niedokładnych ostrzeżeń lub błędów dotyczących przestarzałych modułów aplikacji. (#14806)
* Wszystkie punkty rozszerzeń NVDA są teraz krótko opisane w nowym, dedykowanym rozdziale w Przewodniku dla programistów. (#14648)
* 'scons checkpot' nie będzie już sprawdzać podfolderu 'userConfig'. (#14820)
* Przetłumaczalne ciągi znaków mogą być teraz definiowane w liczbie pojedynczej i mnogiej za pomocą 'ngettext' i 'npgettext'. (#12445)

#### Przestarzałe

* Przekazywanie funkcji lambda do "hwIo.ioThread.IoThread.queueAsApc" jest przestarzałe.
Zamiast tego funkcje powinny mieć słabe odwołania. (#14627)
* Importowanie pliku "LPOVERLAPPED_COMPLETION_ROUTINE" z pliku "hwIo.base" jest przestarzałe.
Zamiast tego zaimportuj z 'hwIo.ioThread'. (#14627)
* Element "IoThread.autoDeleteApcReference" jest przestarzały.
Został wprowadzony w NVDA 2023.1 i nigdy nie miał być częścią publicznego API.
Dopóki nie zostanie usunięty, zachowuje się jak no-op, czyli menedżer kontekstu, który nic nie daje. (#14924)
* "Graficzny interfejs użytkownika. MainFrame.onAddonsManagerCommand" jest przestarzałe, użyj "gui". MainFrame.onAddonStoreCommand'. (#13985)
* Element "speechDictHandler.speechVars.speechDictsPath" jest przestarzały, zamiast niego należy użyć parametru "NVDAState.WritePaths.speechDictsDir". (#15021)
* Importowanie plików "voiceDictsPath" i "voiceDictsBackupPath" z pliku "speechDictHandler.dictFormatUpgrade" jest przestarzałe.
Zamiast tego użyj "WritePaths.voiceDictsDir" i "WritePaths.voiceDictsBackupDir" z "NVDAState". (#15048)
* Wartość "config.CONFIG_IN_LOCAL_APPDATA_SUBKEY" jest przestarzała.
Zamiast tego użyj 'config. RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY". (#15049)

## 2023.1

Dodano nową opcję, "Styl akapitu" w "Nawigacji po dokumencie".
Można tego używać z edytorami tekstu, które nie obsługują natywnie nawigacji po akapitach, takimi jak Notatnik i Notepad++.

Pojawiło się nowe globalne polecenie informujące o miejscu docelowym łącza, odwzorowane na 'NVDA+k'.

Ulepszono obsługę zawartości sieci Web z adnotacjami (takiej jak komentarze i przypisy).
Naciśnij 'NVDA+d', aby przełączać się między podsumowaniami, gdy zgłaszane są adnotacje (np. "ma komentarz, ma przypis").

Monitory brajlowskie Tivomatic Caiku Albatross 46/80 są teraz obsługiwane.

Ulepszono obsługę wersji ARM64 i AMD64 systemu Windows.

Istnieje wiele poprawek błędów, w szczególności poprawki systemu Windows 11.

Zaktualizowano eSpeak, LibLouis, Sonic rate boost i Unicode CLDR.
Pojawiły się nowe tablice brajlowskie w językach gruzińskim, suahili (Kenia) i Chichewa (Malawi).

Uwaga:

* Ta wersja zapewnia zgodność z istniejącymi dodatkami.

### Nowe funkcje

* Microsoft Excel za pośrednictwem automatyzacji interfejsu użytkownika: Automatyczne raportowanie nagłówków kolumn i wierszy w tabelach. (#14228)
  * Uwaga: Odnosi się to do tabel sformatowanych za pomocą przycisku "Tabela" w okienku Wstawianie na Wstążce.
  "Pierwsza kolumna" i "Wiersz nagłówka" w "Opcjach stylu tabeli" odpowiadają odpowiednio nagłówkom kolumn i wierszy.
  * Nie odnosi się to do nagłówków specyficznych dla czytnika ekranu za pośrednictwem nazwanych zakresów, które obecnie nie są obsługiwane przez automatyzację interfejsu użytkownika.
* Dodano nieprzypisany skrypt do przełączania opóźnionych opisów postaci. (#14267)
* Dodano eksperymentalną opcję wykorzystującą obsługę powiadomień UIA w terminalu Windows do zgłaszania nowego lub zmienionego tekstu w terminalu, co skutkuje poprawą stabilności i responsywności. (#13781)
  * Zapoznaj się z podręcznikiem użytkownika, aby zapoznać się z ograniczeniami tej eksperymentalnej opcji.
* W systemie Windows 11 ARM64 tryb przeglądania jest teraz dostępny w aplikacjach AMD64, takich jak Firefox, Google Chrome i 1Password. (#14397)
* Dodano nową opcję, "Styl akapitu" w "Nawigacji po dokumencie".
Dodaje to obsługę nawigacji po akapitach z pojedynczym podziałem wiersza (normalnym) i wieloma podziałami wierszy (blok).
Można tego używać z edytorami tekstu, które nie obsługują natywnie nawigacji po akapitach, takimi jak Notatnik i Notepad++. (#13797)
* Obecność wielu adnotacji jest teraz zgłaszana.
'NVDA+d' teraz cyklicznie raportuje podsumowanie każdego celu adnotacji dla źródeł z wieloma celami adnotacji.
Na przykład, gdy z tekstem jest skojarzony komentarz i przypis dolny. (#14507, #14480)
* Dodano obsługę monitorów brajlowskich Tivomatic Caiku Albatross 46/80. (#13045)
* Nowe polecenie globalne: Miejsce docelowe łącza raportu ('NVDA+k').
Jednokrotne naciśnięcie spowoduje odczytanie/alfabet Braille'a miejsca docelowego łącza, które znajduje się w obiekcie nawigatora.
Dwukrotne naciśnięcie spowoduje wyświetlenie go w oknie, w celu bardziej szczegółowego przeglądu. (#14583)
* Nowe niezmapowane polecenie globalne (kategoria Narzędzia): Miejsce docelowe łącza raportu w oknie.
To samo, co dwukrotne naciśnięcie 'NVDA+k', ale może być bardziej przydatne dla użytkowników brajla. (#14583)

### Zmiany

* Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Duże zmiany w węgierskim, UEB i chińskim bopomofo braille.
  * Obsługa duńskiego standardu Braille'a 2022.
  * Nowe tablice brajlowskie dla gruzińskiego alfabetu Braille'a, suahili (Kenia) i Chichewa (Malawi).
* Zaktualizowano bibliotekę Sonic Rate Boost, aby zatwierdziła '1d70513'. (#14180)
* CLDR został zaktualizowany do wersji 42.0. (#14273)
* eSpeak NG został zaktualizowany do wersji 1.52-dev commit 'f520fecb'. (#14281, #14675)
  * Poprawiono raportowanie dużych liczb. (#14241)
* Aplikacje Java z kontrolkami korzystającymi ze stanu wybieralnego będą teraz informować, kiedy element nie jest wybrany, a nie gdy element jest wybrany. (#14336)

### Poprawki błędów

* Poprawki systemu Windows 11:
  * NVDA ogłosi najważniejsze informacje wyszukiwania po otwarciu menu Start. (#13841)
  * W usłudze ARM aplikacje x64 nie są już identyfikowane jako aplikacje ARM64. (#14403)
  * Można uzyskać dostęp do elementów menu historii schowka, takich jak "element kodu PIN". (#14508)
  * W systemie Windows 11 22H2 i nowszych wersjach, od teraz znowu możliwa jest interakcja za pomocą myszy i klawiatury z elementami takie jak obszar powiadomień dodatkowych i okno dialogowe "otwórz za pomocą". (#14538, #14539)
* Sugestie są zgłaszane podczas wpisywania @mention w komentarzach programu Microsoft Excel. (#13764)
* Na pasku adresu Google Chrome elementy sterujące sugestiami (przełącz na kartę, usuń sugestię itp.) są teraz raportowane po wybraniu. (#13522)
* Podczas żądania informacji o formatowaniu kolory są teraz jawnie zgłaszane w programie Wordpad lub przeglądarce dzienników, a nie tylko w "Kolorze domyślnym". (#13959)
* W przeglądarce Firefox aktywacja przycisku "Pokaż opcje" na stronach problemów GitHub działa teraz niezawodnie. (#14269)
* Kontrolki selektora daty w oknie dialogowym wyszukiwania zaawansowanego programu Outlook 2016 / 365 teraz zgłaszają swoją etykietę i wartość. (#12726)
* Elementy sterujące przełącznikami ARIA są teraz raportowane jako przełączniki w przeglądarkach Firefox, Chrome i Edge, a nie pola wyboru. (#11310)
* NVDA automatycznie ogłosi stan sortowania w nagłówku kolumny tabeli HTML, gdy zostanie zmieniony przez naciśnięcie wewnętrznego przycisku. (#10890)
* Nazwa punktu orientacyjnego lub regionu jest zawsze automatycznie wypowiadana podczas przeskakiwania do środka z zewnątrz za pomocą szybkiej nawigacji lub ustawiania ostrości w trybie przeglądania. (#13307)
* Gdy opcje Odtwarzaj dźwięk, oraz lub wymawiaj 'duże' przed dużymi literami są włączone w kombinacji z opisami po nazwie liter, NVDA więcej nie odtworzy sygnał dźwiękowy lub odczyta 'duże' dwukrotnie. (#14239)
* Kontrolki w tabelach w aplikacjach Java będą teraz dokładniej ogłaszane przez NVDA. (#14347)
* Niektóre ustawienia nie będą się już nieoczekiwanie różnić w przypadku korzystania z wielu profili. (#14170)
  * Zajęto się następującymi ustawieniami:
    * Wcięcie wiersza w ustawieniach formatowania dokumentu.
    * Obramowania komórek w ustawieniach formatowania dokumentu
    * Pokazywanie wiadomości w ustawieniach brajla
    * Tether Braille w ustawieniach brajlowskich
  * W niektórych, rzadkich przypadkach, te ustawienia używane w profilach mogą zostać nieoczekiwanie zmodyfikowane podczas instalacji tej wersji NVDA.
  * Prosimy o sprawdzenie tych opcji w swoich profilach po aktualizacji NVDA do tej wersji.
* Emotikony powinny być teraz zgłaszane w większej liczbie języków. (#14433)
* W przypadku niektórych elementów w alfabecie Braille'a nie brakuje już adnotacji. (#13815)
* Naprawiono problem polegający na tym, że zmiany konfiguracji nie zapisywały się poprawnie po przełączeniu między opcją "Domyślna" a wartością opcji "Domyślna". (#14133)
* Podczas konfiguracji NVDA zawsze będzie istniał co najmniej jeden klucz zdefiniowany jako klucz NVDA. (#14527)
* Podczas uzyskiwania dostępu do menu NVDA poprzez obszar powiadomień, NVDA nie będzie już sugerować oczekującej aktualizacji, jeśli żadna aktualizacja nie jest dostępna. (#14523)
* Pozostały czas, który upłynął i całkowity jest teraz poprawnie raportowany dla plików audio w ciągu jednego dnia w foobar2000. (#14127)
* W przeglądarkach internetowych, takich jak Chrome i Firefox, alerty, takie jak pobranie plików, są wyświetlane w alfabecie Braille'a, a nie tylko są wypowiadane. (#14562)
* Naprawiono błąd podczas przechodzenia do pierwszej i ostatniej kolumny w tabeli w Firefoksie (#14554)
* Gdy NVDA zostanie uruchomiony z parametrem '--lang=Windows', ponownie możliwe jest otwarcie okna dialogowego ustawień ogólnych NVDA. (#14407)
* NVDA nie przerywa już kontynuowania czytania w Kindle na PC po przewróceniu strony. (#14390)

### Zmiany dla deweloperów

Uwaga: jest to wersja niezgodna z interfejsem API dodatku.
Dodatki będą musiały zostać ponownie przetestowane i mieć zaktualizowany manifest.
Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Testy systemowe powinny teraz zakończyć się powodzeniem, gdy są uruchamiane lokalnie w systemach innych niż angielski. (#13362)
* W systemie Windows 11 na usłudze ARM aplikacje x64 nie są już identyfikowane jako aplikacje ARM64. (#14403)
* Nie jest już konieczne używanie "SearchField" i "SuggestionListItem", "UIA", "NVDAObjects" w nowych scenariuszach automatyzacji interfejsu użytkownika, w których automatyczne raportowanie sugestii wyszukiwania i gdzie wpisywanie zostało uwidocznione za pośrednictwem automatyzacji interfejsu użytkownika ze wzorcem "controllerFor".
Ta funkcja jest teraz dostępna ogólnie za pośrednictwem "zachowań". EditableText" i podstawę "NVDAObject" odpowiednio. (#14222)
* Kategoria rejestrowania debugowania UIA, gdy jest włączona, generuje teraz znacznie więcej rejestrów dla programów obsługi zdarzeń UIA i narzędzi. (#14256)
* Zaktualizowano standardy kompilacji NVDAHelper. (#13072)
  * Teraz używa standardu C++20, był C++17.
  * Now uses the `/permissive-` compiler flag which disables permissive behaviors, and sets the `/Zc` compiler options for strict conformance.
* Niektóre obiekty wtyczek (np. sterowniki i dodatki) mają teraz bardziej informacyjny opis w konsoli NVDA Pythona. (#14463)
* NVDA can now be fully compiled with Visual Studio 2022, no longer requiring the Visual Studio 2019 build tools. (#14326)
* More detailed logging for NVDA freezes to aid debugging. (#14309)
* Singletonowa klasa 'braille._BgThread' została zastąpiona przez 'hwIo.ioThread.IoThread'. (#14130)
  * Pojedyncza instancja 'hwIo.bgThread' (w rdzeniu NVDA) tej klasy zapewnia tło i/o dla bezpiecznych wątkowo sterowników monitorów brajlowskich.
  * Ta nowa klasa nie jest singletonem z założenia, autorzy dodatków są zachęcani do używania własnej instancji podczas wykonywania sprzętowych operacji we/wy.
* Architekturę procesora dla komputera można sprawdzić z atrybutu "winVersion.WinVersion.processorArchitecture". (#14439)
* Dodano nowe punkty rozszerzeń. (#14503)
  * "inputCore.decide_executeGesture"
  * "tones.decide_beep"
  * "nvwave.decide_playWaveFile"
  * "braille.pre_writeCells"
  * "braille.filter_displaySize"
  * "braille.decide_enabled"
  * 'braille.displayZmieniono'
  * 'braille.displaySizeChanged'
* Możliwe jest ustawienie useConfig na False na obsługiwanych ustawieniach sterownika syntezatora. (#14601)

#### Zmiany powodujące niezgodność interfejsu API

Są to zmiany w interfejsie API powodujące niezgodność.
Otwórz problem z usługą GitHub, jeśli Twój dodatek ma problem z aktualizacją do nowego interfejsu API.

* Specyfikacja konfiguracji została zmieniona, klucze zostały usunięte lub zmodyfikowane:
  * W sekcji "[documentFormatting]" (#14233):
    * "reportLineIndentation" przechowuje wartość int (od 0 do 3) zamiast wartości logicznej
    * Usunięto element "reportLineIndentationWithTones".
    * Wartości "reportBorderStyle" i "reportBorderColor" zostały usunięte i zostały zastąpione przez "reportCellBorders".
  * W sekcji '[braille]' (#14233):
    * Wartość "noMessageTimeout" została usunięta i zastąpiona wartością wartości "showMessages".
    * Parametr "messageTimeout" nie może już przyjmować wartości 0, zastępowanej wartością parametru "showMessages".
    * Usunięto opcję 'autoTether'; 'tetherTo' może teraz przyjąć wartość "auto".
  * W sekcji "[klawiatura]" (#14528):
    * `useCapsLockAsNVDAModifierKey`, `useNumpadInsertAsNVDAModifierKey`, `useExtendedInsertAsNVDAModifierKey` have been removed.
    Są one zastępowane przez 'NVDAModifierKeys'.
* Klasa "NVDAHelper.RemoteLoader64" została usunięta bez zastępstwa. (#14449)
* Następujące funkcje w pliku "winAPI.sessionTracking" są usuwane bez zastępowania. (#14416, #14490)
  * "isWindowsLocked" (Jest zablokowany)
  * 'handleSessionChange' (zmiana sesji)
  * "Wyrejestruj się"
  * "Rejestr"
  * "isLockStateSuccessfullyTracked" (IsLockStateSuccessfullyTracked)
* Nie jest już możliwe włączenie/wyłączenie obsługi brajla poprzez ustawienie 'braille.handler.enabled'.
Aby programowo wyłączyć obsługę brajla, zarejestruj ją w pozycji "braille.handler.decide_enabled". (#14503)
* Nie jest już możliwe zaktualizowanie rozmiaru wyświetlacza modułu obsługi poprzez ustawienie 'braille.handler.displaySize'.
To update the displaySize programatically, register a handler to `braille.handler.filter_displaySize`.
Zapoznaj się z 'BrailleViewer', aby dowiedzieć się, jak to zrobić. (#14503)
* Wprowadzono zmiany w użyciu elementu "addonHandler.Addon.loadModule". (#14481)
  * "loadModule" oczekuje teraz kropki jako separatora, a nie ukośnika odwrotnego.
  Na przykład "lib.example" zamiast "lib\example".
  * "loadModule" zgłasza teraz wyjątek, gdy nie można załadować modułu lub występują błędy, zamiast dyskretnie zwracać wartość "None" bez podawania informacji o przyczynie.
* Następujące symbole zostały usunięte z pliku 'appModules.foobar2000' bez bezpośredniego zastąpienia. (#14570)
  * 'statusBarTimes' (Czasy statusBar)
  * "ParseIntervalToTimestamp"
  * 'getOutputFormat' (Format wyjściowy)
  * 'getParsingFormat' (Format analizy)
* Następujące elementy nie są już singletonami - ich metoda get została usunięta.
Użycie 'Example.get()' to teraz 'Example()'. (#14248)
  * "UIAHandler.customAnnotations.CustomAnnotationTypesCommon"
  * 'UIAHandler.customProps.CustomPropertiesCommon'
  * "NVDAObjects.UIA.excel.ExcelCustomProperties"
  * "NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes" (NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes)

#### Przestarzałe

* Plik "NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA" jest przestarzały i jego użycie jest zabronione. (#14047)
* Plik "config.addConfigDirsToPythonPackagePath" został przeniesiony.
Zamiast tego użyj polecenia "addonHandler.packaging.addDirsToPythonPackagePath". (#14350)
* "Alfabet Braille'a. BrailleHandler.TETHER_*" są przestarzałe.
Zamiast tego użyj "configFlags.TetherTo.*.value". (#14233)
* Plik "utils.security.postSessionLockStateChanged" jest przestarzały.
Use `utils.security.post_sessionLockStateChanged` instead. (#14486)
* Elementy "NVDAObject.hasDetails", "NVDAObject.detailsSummary", "NVDAObject.detailsRole" zostały uznane za przestarzałe.
Zamiast tego użyj "NVDAObject.annotations". (#14507)
* Ciąg "keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS" jest przestarzały i nie ma go bezpośrednio zastępować.
Zamiast tego rozważ użycie klasy "config.configFlags.NVDAKey". (#14528)
* "Graficzny interfejs użytkownika. MainFrame.evaluateUpdatePendingUpdateMenuItemCommand" jest przestarzałe.
Użyj 'gui. MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand". (#14523)

## 2022.4

To wydanie zawiera kilka nowych poleceń klawiszowych, w tym polecenia table say all.
Sekcja "Skrócona instrukcja obsługi" została dodana do Podręcznika użytkownika.
Istnieje również kilka poprawek błędów.

eSpeak został zaktualizowany, a LibLouis został zaktualizowany.
Pojawiły się nowe tablice brajlowskie w językach chińskim, szwedzkim, luganda i kinyarwanda.

### Nowe funkcje

* Dodano sekcję "Skrócona instrukcja obsługi" do Podręcznika użytkownika. (#13934)
* Wprowadzono nowe polecenie sprawdzania skrótu klawiaturowego bieżącego fokusu. (#13960)
  * Pulpit: 'shift+klawiatura numeryczna2'.
  * Laptop: 'NVDA+ctrl+shift+.'.
* Wprowadzono nowe polecenia umożliwiające przesuwanie kursora recenzji według strony, na której jest to obsługiwane przez aplikację. (#14021)
  * Przejdź do poprzedniej strony:
    * Pulpit: 'NVDA+pageUp'.
    * Laptop: 'NVDA+shift+pageUp'.
  * Przejdź do następnej strony:
    * Pulpit: 'NVDA+pageDown'.
    * Laptop: 'NVDA+shift+pageDown'.
* Dodano następujące polecenia tabeli. (#14070)
  * Powiedz wszystko w kolumnie: 'NVDA+control+alt+strzałka w dół'
  * Powiedz wszystko w wierszu: 'NVDA+control+alt+rightArrow'
  * Przeczytaj całą kolumnę: 'NVDA+control+alt+strzałka w górę'
  * Przeczytaj cały wiersz: 'NVDA+control+alt+strzałka w lewo'
* Microsoft Excel za pośrednictwem automatyzacji interfejsu użytkownika: NVDA informuje teraz o wyjściu z tabeli w arkuszu kalkulacyjnym. (#14165)
* Nagłówki tabel raportowania można teraz konfigurować osobno dla wierszy i kolumn. (#14075)

### Zmiany

* eSpeak NG został zaktualizowany do wersji 1.52-dev commit '735ecdb8'. (#14060, #14079, #14118, #14203)
  * Poprawiono raportowanie znaków łacińskich podczas korzystania z języka mandaryńskiego. (#12952, #13572, #14197)
* Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
  * Dodano tabele brajlowskie:
    * Wspólny chiński alfabet Braille'a (uproszczone znaki chińskie)
    * Kinyarwanda brajl literacki
    * Luganda brajl literacki
    * Szwedzkie pismo podstawowe
    * Szwedzkie pismo pełne
    * Szwedzkie skróty
    * Chiński (Chiny, mandaryński) Aktualny system Braille'a (bez tonów) (#14138)
* NVDA zawiera teraz architekturę systemu operacyjnego w ramach śledzenia statystyk użytkowników. (#14019)

### Poprawki błędów

* Podczas aktualizowania NVDA za pomocą interfejsu wiersza polecenia Menedżera pakietów Windows (aka winget), wydana wersja NVDA nie jest już zawsze traktowana jako nowsza niż jakakolwiek zainstalowana wersja alfa. (#12469)
* NVDA będzie teraz poprawnie ogłaszać pola grup w aplikacjach Java. (#13962)
* Caret poprawnie podąża za tekstem mówionym podczas "powiedz wszystko" w aplikacjach takich jak Bookworm, WordPad lub przeglądarka dzienników NVDA. (#13420, #9179)
* W programach korzystających z UI Automation częściowo zaznaczone pola wyboru będą raportowane poprawnie. (#13975)
* Poprawiono wydajność i stabilność w programie Microsoft Visual Studio, terminalu Windows i innych aplikacjach opartych na automatyzacji interfejsu użytkownika. (#11077, #11209)
  * Te poprawki dotyczą systemu Windows 11 Sun Valley 2 (wersja 22H2) i nowszych.
  * Selektywna rejestracja zdarzeń i zmian właściwości automatyzacji interfejsu użytkownika jest teraz domyślnie włączona.
* Raportowanie tekstu, dane wyjściowe brajlem i pomijanie haseł działają teraz zgodnie z oczekiwaniami w osadzonej kontrolce terminala systemu Windows w programie Visual Studio 2022. (#14194)
* NVDA rozpoznaje teraz DPI podczas korzystania z wielu monitorów.
Istnieje kilka poprawek dotyczących korzystania z ustawienia DPI wyższego niż 100% o na wielu monitorach.
Problemy mogą nadal występować w wersjach systemu Windows starszych niż Windows 10 1809.
Aby te poprawki działały, aplikacje, z którymi NVDA wchodzi w interakcję, również muszą być świadome DPI.
Pamiętaj, że nadal występują znane problemy z Chrome i Edge. (#13254)
  * Wizualne ramki podświetlania powinny być teraz poprawnie rozmieszczone w większości aplikacji. (#13370, #3875, #12070)
  * Interakcja z ekranem dotykowym powinna być teraz dokładna dla większości aplikacji. (#7083)
  * Śledzenie myszy powinno teraz działać w większości aplikacji. (#6722)
* Zmiany orientacji (pozioma/pionowa) są teraz poprawnie ignorowane, gdy nie ma żadnych zmian (np. zmiany monitora). (#14035)
* NVDA ogłosi przeciąganie elementów na ekranie w miejscach takich jak zmiana kolejności kafelków menu Start systemu Windows 10 i wirtualnych pulpitów w systemie Windows 11. (#12271, #14081)
* W ustawieniach zaawansowanych opcja "Odtwórz dźwięk dla zarejestrowanych błędów" jest teraz poprawnie przywracana do wartości domyślnej po naciśnięciu przycisku "Przywróć domyślne". (#14149)
* NVDA może teraz zaznaczać tekst za pomocą skrótu klawiaturowego 'NVDA+f10' w aplikacjach Java. (#14163)
* NVDA nie będzie już zacinać się w menu podczas przechodzenia w górę i w dół wątków rozmów w Microsoft Teams. (#14355)

### Zmiany dla deweloperów

Zapoznaj się z [Przewodnikiem dla programistów](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API), aby uzyskać informacje na temat procesu wycofywania i usuwania API NVDA.

* Utworzono listę mailingową [NVDA API Announcement](https://groups.google.com/a/nvaccess.org/g/nvda-api/about). (#13999)
* NVDA nie przetwarza już zdarzeń 'textChange' dla większości aplikacji do automatyzacji interfejsu użytkownika ze względu na ich ekstremalnie negatywny wpływ na wydajność. (#11002, #14067)

#### Przestarzałe

* "core.post_windowMessageReceipt" jest przestarzałe, zamiast tego użyj "winAPI.messageWindow.pre_handleWindowMessage".
* Wartość "winKernel.SYSTEM_POWER_STATUS" jest przestarzała i odradza się jej używanie, została przeniesiona do wartości "winAPI._powerTracking.SystemPowerStatus".
* Stałe "winUser.SM_*" są przestarzałe, zamiast tego użyj "winAPI.winUser.constants.SystemMetrics".

## 2022.3.3

Jest to niewielka wersja, która rozwiązuje problemy z wersjami 2022.3.2, 2022.3.1 i 2022.3.
Rozwiązuje to również problem z zabezpieczeniami.

### Poprawki zabezpieczeń

* Uniemożliwia możliwy dostęp do systemu (np. konsoli NVDA Python) dla nieuwierzytelnionych użytkowników.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Poprawki błędów

* Naprawiono błąd polegający na tym, że jeśli NVDA zawiesza się podczas blokowania, NVDA zezwala na dostęp do pulpitu użytkownika na ekranie blokady systemu Windows. (#14416)
* Naprawiono błąd, który powodował, że jeśli NVDA zawiesza się podczas blokowania, NVDA nie będzie zachowywać się poprawnie, tak jakby urządzenie było nadal zablokowane. (#14416)
* Rozwiązano problemy z ułatwieniami dostępu w procesie "zapomniałem kodu PIN" systemu Windows i aktualizacją/instalacją systemu Windows. (#14368)
* Naprawiono błąd podczas próby instalacji NVDA w niektórych środowiskach Windows, np. Windows Server. (#14379)

### Zmiany dla deweloperów

#### Przestarzałe

* Plik "utils.security.isObjectAboveLockScreen(obj)" jest przestarzały, zamiast tego należy użyć "obj.isBelowLockScreen". (#14416)
* Następujące funkcje w "winAPI.sessionTracking" są przestarzałe do usunięcia w 2023.1. (#14416)
  * "isWindowsLocked" (Jest zablokowany)
  * 'handleSessionChange' (zmiana sesji)
  * "Wyrejestruj się"
  * "Rejestr"
  * "isLockStateSuccessfullyTracked" (IsLockStateSuccessfullyTracked)

## 2022.3.2

Jest to niewielka wersja, która ma na celu naprawienie regresji w wersji 2022.3.1 i rozwiązanie problemu z zabezpieczeniami.

### Poprawki zabezpieczeń

* Uniemożliwia możliwy dostęp na poziomie systemu nieuwierzytelnionym użytkownikom.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Poprawki błędów

* Naprawiono regresję z wersji 2022.3.1, w której niektóre funkcje były wyłączone na bezpiecznych ekranach. (#14286)
* Naprawiono regresję z 2022.3.1, w której niektóre funkcje były wyłączane po zalogowaniu, jeśli NVDA uruchamiał się na ekranie blokady. (#14301)

## 2022.3.1

Jest to niewielka wersja, która ma na celu rozwiązanie kilku problemów z zabezpieczeniami.
Prosimy o odpowiednie zgłoszenie incydentów bezpieczeństwa na adres <info@nvaccess.org>.

### Poprawki zabezpieczeń

* Naprawiono eksploit za pomocą którego można było podnieść uprawnienia z użytkownika do systemu.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Naprawiono problem z zabezpieczeniami umożliwiający dostęp do konsoli Pythona na ekranie blokady poprzez warunek wyścigu dla uruchamiania NVDA.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Rozwiązano problem polegający na tym, że tekst przeglądarki mowy był buforowany podczas blokowania systemu Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Poprawki błędów

* Uniemożliwia nieuwierzytelnionemu użytkownikowi aktualizowanie ustawień przeglądarki mowy i alfabetu Braille'a na ekranie blokady. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

Znaczna część tego wydania została wniesiona przez społeczność programistów NVDA.
Obejmuje to opóźnione opisy postaci i ulepszoną obsługę konsoli Windows.

To wydanie zawiera również kilka poprawek błędów.
Warto zauważyć, że aktualne wersje programu Adobe Acrobat/Reader nie będą się już zawieszać podczas odczytywania dokumentu PDF.

Zaktualizowano eSpeak, który wprowadza 3 nowe języki: białoruski, luksemburski i Totontepec Mixe.

### Nowe funkcje

* Na hoście konsoli systemu Windows używanym przez wiersz polecenia, program PowerShell i podsystem Windows dla systemu Linux w systemie Windows 11 w wersji 22H2 (Sun Valley 2) lub nowszej:
  * Znacznie poprawiona wydajność i stabilność. (#10964)
  * Po naciśnięciu "control+f" w celu znalezienia tekstu, pozycja kursora recenzji jest aktualizowana tak, aby podążała za znalezionym terminem. (#11172)
  * Raportowanie wpisanego tekstu, który nie pojawia się na ekranie (np. haseł), jest domyślnie wyłączone.
Można go ponownie włączyć w panelu ustawień zaawansowanych NVDA. (#11554)
  * Tekst, który został przewinięty poza ekran, można przeglądać bez przewijania okna konsoli. (#12669)
  * Dostępne są bardziej szczegółowe informacje na temat formatowania tekstu. ([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))
* Dodano nową opcję Mowy, która umożliwia odczytywanie opisów postaci po pewnym czasie. (#13509)
* Dodano nową opcję Braille'a, która określa, czy przewijanie wyświetlacza do przodu/do tyłu powinno przerywać mowę. (#2124)

### Zmiany

* eSpeak NG został zaktualizowany do wersji 1.52-dev commit '9de65fcb'. (#13295)
  * Dodane języki:
    * Białoruski
    * luksemburski
    * Totontepec Mixe
* Podczas korzystania z automatyzacji interfejsu użytkownika w celu uzyskania dostępu do kontrolek arkusza kalkulacyjnego programu Microsoft Excel, NVDA może teraz raportować, kiedy komórka jest scalana. (#12843)
* Zamiast zgłaszania "zawiera szczegóły" w miarę możliwości uwzględnia się cel szczegółów, na przykład "zawiera komentarz". (#13649)
* Rozmiar instalacji NVDA jest teraz wyświetlany w sekcji Programy i funkcje systemu Windows. (#13909)

### Poprawki błędów

* 64-bitowy program Adobe Acrobat / Reader nie będzie się już zawieszał podczas odczytywania dokumentu PDF. (#12920)
  * Należy pamiętać, że aby uniknąć awarii, wymagana jest również najnowsza wersja programu Adobe Acrobat / Reader.
* Pomiary rozmiaru czcionki są teraz tłumaczalne w NVDA. (#13573)
* Ignoruj zdarzenia programu Java Access Bridge, w których nie można znaleźć uchwytu okna dla aplikacji Java.
Poprawi to wydajność niektórych aplikacji Java, w tym IntelliJ IDEA. (#13039)
* Ogłaszanie zaznaczonych komórek w programie LibreOffice Calc jest bardziej wydajne i nie powoduje już zawieszania się programu Calc, gdy zaznaczonych jest wiele komórek. (#13232)
* W przypadku uruchamiania przez innego użytkownika przeglądarka Microsoft Edge nie jest już niedostępna. (#13032)
* Gdy podwyżka kursu jest wyłączona, stawka eSpeak nie spada już między stawkami 99% a i 100%. (#13876)
* Naprawiono błąd, który pozwalał na otwarcie 2 okien dialogowych gestów wprowadzania. (#13854)

### Zmiany dla deweloperów

* Zaktualizowano komtypy do wersji 1.1.11. (#12953)
* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * Można to zmienić, zmieniając ustawienie "Obsługa konsoli Windows" w panelu ustawień zaawansowanych NVDA.
  * Aby znaleźć poziom interfejsu API NVDA konsoli systemu Windows, ustaw opcję "Obsługa konsoli systemu Windows" na "UIA, gdy jest dostępna", a następnie sprawdź dziennik NVDA+F1 otwarty z uruchomionej instancji konsoli systemu Windows.
* Wirtualny bufor Chromium jest teraz ładowany nawet wtedy, gdy obiekt dokumentu ma "STATE_SYSTEM_BUSY" MSAA ujawnione za pośrednictwem IA2. (#13306)
* Typ specyfikacji konfiguracyjnej 'featureFlag' został stworzony do użytku z eksperymentalnymi funkcjami NVDA. Zobacz 'devDocs/featureFlag.md', aby uzyskać więcej informacji. (#13859)

#### Przestarzałe

W 2022 r. nie są proponowane żadne wycofania.3.

## 2022.2.4

Jest to poprawka mająca na celu rozwiązanie problemu z zabezpieczeniami.

### Poprawki błędów

* Naprawiono exploit, w którym można było otworzyć konsolę NVDA Pythona za pomocą przeglądarki dziennika na ekranie blokady.
([GHSA-585m-rpvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

Jest to poprawka naprawiająca przypadkowe uszkodzenie interfejsu API wprowadzone w wersji 2022.2.1.

### Poprawki błędów

* Naprawiono błąd, który sprawiał, że NVDA nie ogłaszało "Bezpieczny pulpit" po wejściu na bezpieczny pulpit.
Powodowało to, że zdalny NVDA nie rozpoznawał bezpiecznych pulpitów. (#14094)

## 2022.2.2

Jest to poprawka naprawiająca błąd wprowadzony w 2022.2.1 dotyczący gestów wejściowych.

### Poprawki błędów

* Naprawiono błąd polegający na tym, że gesty wejściowe nie zawsze działały. (#14065)

## 2022.2.1

Jest to drobna wersja, która ma na celu rozwiązanie problemu z zabezpieczeniami.
Prosimy odpowiedzialnie zgłaszać problemy z bezpieczeństwem na adresie <info@nvaccess.org>.

### Poprawki zabezpieczeń

* Naprawiono exploit, w którym można było uruchomić konsolę Pythona z ekranu blokady. (GHSA-rmq3-vvhq-gp32)
* Naprawiono błąd, w wyniku którego można było uciec z ekranu blokady za pomocą nawigacji po obiektach. (GHSA-rmq3-vvhq-gp32)

### Zmiany dla deweloperów

#### Przestarzałe

Te wycofania nie są obecnie zaplanowane do usunięcia.
Przestarzałe aliasy pozostaną do odwołania.
Przetestuj nowy interfejs API i przekaż swoją opinię.
W przypadku autorów dodatków otwórz problem z usługą GitHub, jeśli te zmiany uniemożliwiają interfejsowi API spełnianie Twoich potrzeb.

* `appModules.lockapp.LockAppObject` should be replaced with `NVDAObjects.lockscreen.LockScreenObject`. (GHSA-rmq3-vvhq-gp32)
* Ciąg "appModules.lockapp.AppModule.SAFE_SCRIPTS" powinien zostać zastąpiony przez ciąg "utils.security.getSafeScripts()". (GHSA-rmq3-vvhq-gp32)

## 2022.2

To wydanie zawiera wiele poprawek błędów.
Warto zauważyć, że wprowadzono znaczące ulepszenia w aplikacjach opartych na Javie, monitorach brajlowskich i funkcjach systemu Windows.

Wprowadzono nowe polecenia nawigacji po tabelach.
Zaktualizowano standard Unicode CLDR.
Zaktualizowano bibliotekę LibLouis, która zawiera nową niemiecką tabelę brajlowską.

### Nowe funkcje

* Obsługa interakcji ze składnikami pętli Microsoft w produktach pakietu Microsoft Office. (#13617)
* Dodano nowe polecenia nawigacji po tabelach. (#957)
 * 'control+alt+home/end', aby przejść do pierwszej/ostatniej kolumny.
 * 'control+alt+pageUp/pageDown', aby przejść do pierwszego/ostatniego wiersza.
* Dodano nieprzypisany skrypt do przełączania między trybami przełączania języka i dialektu. (#10253)

### Zmiany

* NSIS został zaktualizowany do wersji 3.08. (#9134)
* CLDR został zaktualizowany do wersji 41.0. (#13582)
* Zaktualizowano tłumacza brajlowskiego LibLouis do wersji [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nowa tablica brajlowska: niemiecka klasa 2 (szczegółowa)
* Dodano nową rolę dla elementów sterujących "wskaźnikiem zajętości". (#10644)
* NVDA informuje teraz, kiedy nie można wykonać akcji NVDA. (#13500)
  * Dotyczy to sytuacji, gdy:
    * Korzystanie z wersji NVDA Windows Store.
    * W bezpiecznym kontekście.
    * Oczekiwanie na odpowiedź na modalne okno dialogowe.

### Poprawki błędów

* Poprawki dla aplikacji opartych na Javie:
  * NVDA będzie teraz ogłaszać stan tylko do odczytu. (#13692)
  * NVDA będzie teraz poprawnie ogłaszać stan wyłączony/włączony. (#10993)
  * NVDA będzie teraz informować o skrótach funkcyjnych. (#13643)
  * NVDA może teraz emitować sygnał dźwiękowy lub mówić na paskach postępu. (#13594)
  * NVDA nie będzie już nieprawidłowo usuwać tekstu z widżetów podczas prezentacji dla użytkownika. (#13102)
  * NVDA ogłosi teraz stan przycisków przełączania. (#9728)
  * NVDA będzie teraz identyfikować okno w aplikacji Java z wieloma oknami. (#9184)
  * NVDA będzie teraz ogłaszać informacje o pozycji dla kontrolek zakładek. (#13744)
* Poprawki w alfabecie Braille'a:
  * Naprawiono wyjście brajlowskie podczas nawigowania po określonym tekście w elementach sterujących edycją Mozilli, takich jak redagowanie wiadomości w Thunderbirdzie. (#12542)
  * Gdy pismo Braille'a jest automatycznie podłączane na uwięzi, a mysz jest poruszana z włączonym śledzeniem myszy,
   Polecenia przeglądu tekstu aktualizują teraz monitor brajlowski o treść mówioną. (#11519)
  * Możliwe jest teraz przesuwanie monitora brajlowskiego przez zawartość po użyciu poleceń przeglądu tekstu. (#8682)
* Instalator NVDA może być teraz uruchamiany z katalogów ze znakami specjalnymi. (#13270)
* W Firefoksie NVDA nie zgłasza już elementów na stronach internetowych, gdy atrybuty aria-rowindex, aria-colindex, aria-rowcount lub aria-colcount są nieprawidłowe. (#13405)
* Kursor nie przełącza już wiersza ani kolumny podczas nawigacji po tabeli w celu nawigowania po scalonych komórkach. (#7278)
* Podczas odczytywania nieinterakcyjnych plików PDF w programie Adobe Reader typ i stan pól formularza (takich jak pola wyboru i przyciski radiowe) są teraz raportowane. (#13285)
* Opcja "Zresetuj konfigurację do ustawień fabrycznych" jest teraz dostępna w menu NVDA w trybie bezpiecznym. (#13547)
* Wszystkie zablokowane myszy zostaną odblokowane po wyjściu z NVDA, wcześniej przycisk myszy pozostawał zablokowany. (#13410)
* Program Visual Studio raportuje teraz numery wierszy. (#13604)
  * Zauważ, że aby raportowanie numerów wierszy działało, pokazywanie numerów wierszy musi być włączone w Visual Studio i NVDA.
* Program Visual Studio teraz poprawnie zgłasza wcięcia wierszy. (#13574)
* NVDA po raz kolejny ogłosi szczegóły wyników wyszukiwania w menu Start w najnowszych wersjach Windows 10 i 11. (#13544)
* W Kalkulatorze Windows 10 i 11 w wersji 10.1908 lub nowszej
NVDA ogłosi wyniki, gdy zostanie naciśniętych więcej poleceń, takich jak polecenia z trybu naukowego. (#13383)
* W systemie Windows 11 ponownie możliwa jest nawigacja i interakcja z elementami interfejsu użytkownika,
takie jak pasek zadań i widok zadań za pomocą myszy i interakcji dotykowej. (#13506)
* NVDA ogłosi zawartość paska stanu w Notatniku systemu Windows 11. (#13688)
* Podświetlenie obiektu Nawigatora pojawia się teraz natychmiast po aktywacji funkcji. (#13641)
* Naprawiono odczytywanie elementów widoku listy z pojedynczą kolumną. (#13659, #13735)
* Naprawiono automatyczne przełączanie języka eSpeak na angielski i francuski z powrotem na brytyjski angielski i francuski (Francja). (#13727)
* Napraw automatyczne przełączanie języka OneCore podczas próby przełączenia się na poprzednio zainstalowany język. (#13732)

### Zmiany dla deweloperów

* Kompilowanie zależności NVDA za pomocą programu Visual Studio 2022 (17.0) jest teraz obsługiwane.
W przypadku kompilacji deweloperskich i wydawniczych program Visual Studio 2019 jest nadal używany. (#13033)
* Podczas pobierania liczby wybranych dzieci za pomocą accSelection,
przypadek, w którym ujemny identyfikator podrzędny lub IDispatch jest zwracany przez "IAccessible::get_accSelection", jest teraz obsługiwany poprawnie. (#13277)
* Do modułu "appModuleHandler" dodano nowe funkcje "registerExecutableWithAppModule" i "unregisterExecutable".
Mogą być używane do korzystania z pojedynczego modułu aplikacji z wieloma plikami wykonywalnymi. (#13366)

#### Przestarzałe

Są to proponowane zmiany powodujące niezgodność interfejsu API.
Przestarzała część interfejsu API będzie nadal dostępna do określonej wersji.
Jeśli nie określono zwolnienia, oznacza to, że plan usunięcia nie został określony.
Pamiętaj, że plan usuwania jest "dołożony wszelkich starań" i może ulec zmianie.
Przetestuj nowy interfejs API i przekaż swoją opinię.
W przypadku autorów dodatków otwórz problem z usługą GitHub, jeśli te zmiany uniemożliwiają interfejsowi API spełnianie Twoich potrzeb.

* Parametr "appModuleHandler.NVDAProcessID" jest przestarzały, zamiast niego należy użyć parametru "globalVars.appPid". (#13646)
* 'gui.quit' jest przestarzały, użyj 'wx. CallAfter(mainFrame.onExitCommand, None)' zamiast. (#13498)
  -
* Niektóre aliasy appModules są oznaczone jako przestarzałe.
Kod, który importuje z jednego z nich, powinien zamiast tego zostać zaimportowany z modułu zastępczego.  (#13366)

| Usunięto nazwę modułu |Moduł zastępczy|
|---|---|
|AzureDataStudio |kod|
|AzureDataStudio-insiders |kod|
|Kalkulator | Kalkulator|
|code - niejawni testerzy |kod|
|commsapps |hxmail|
|dbeaver |zaćmienie|
|digitaleditionspreview |digitaleditions|
|esybraille |esysuite|
|hxoutlook |hxmail|
|miranda64 |miranda32 powiedział:|
|mpc-hc |mplayerc|
|mpc-hc64 |mplayerc powiedział:|
|notepad++ |notatnikPlusPlus|
|searchapp |searchui|
|searchhost |searchUI|
|springtoolsuite4 |zaćmienie|
|sts |zaćmienie|
|teamtalk3 |teamtalk4klasyczny|
|textinputhost |windowsinternal_composableshell_experiences_textinput_inputapp|
|totalcmd64 |totalcmd|
|win32calc |calc|
|Winmail |msimn powiedział:|
|zend-eclipse-php |zaćmienie|
|Zendstudio |Eclipse|

## 2022.1

To wydanie zawiera znaczące ulepszenia w obsłudze UIA z pakietem MS Office.
W przypadku pakietu Microsoft Office 16.0.15000 i nowszych w systemie Windows 11 NVDA domyślnie użyje automatyzacji interfejsu użytkownika w celu uzyskania dostępu do dokumentów Microsoft Word.
Zapewnia to znaczną poprawę wydajności w porównaniu ze starym dostępem do modelu obiektowego.

Wprowadzono ulepszenia sterowników monitorów brajlowskich, w tym Seika Notetaker, Papenmeier i HID Braille.
Istnieją również różne poprawki błędów systemu Windows 11 dla aplikacji takich jak Kalkulator, Konsola, Terminal, Poczta i Panel emotikonów.

eSpeak-NG i LibLouis zostały zaktualizowane, dodając nowe tabele japońskie, niemieckie i katalońskie.

Uwaga:

 * Ta wersja zapewnia zgodność z istniejącymi dodatkami.

### Nowe funkcje

* Obsługa raportowania notatek w MS Excel z włączoną automatyzacją interfejsu użytkownika w systemie Windows 11. (#12861)
* W ostatnich kompilacjach programu Microsoft Word za pośrednictwem automatyzacji interfejsu użytkownika w systemie Windows 11 istnienie zakładek, komentarzy roboczych i rozwiązanych komentarzy jest teraz zgłaszane zarówno w mowie, jak i w alfabecie Braille'a. (#12861)
* Nowy parametr wiersza poleceń '--lang' pozwala na nadpisanie skonfigurowanego języka NVDA. (#10044)
* NVDA ostrzega teraz o parametrach wiersza poleceń, które są nieznane i nie są używane przez żadne dodatki. (#12795)
* W programie Microsoft Word, do którego dostęp można uzyskać za pośrednictwem automatyzacji interfejsu użytkownika, NVDA będzie teraz korzystać z mathPlayer do odczytywania i nawigowania po równaniach matematycznych pakietu Office. (#12946)
  * Aby to zadziałało, musisz korzystać z programu Microsoft Word 365/2016 w kompilacji 14326 lub nowszej.
  * Równania MathType należy również ręcznie przekonwertować na program Office Math, zaznaczając każde z nich, otwierając menu kontekstowe, wybierając pozycję Opcje równania, Konwertuj na matematykę pakietu Office.
* Raportowanie "ma szczegóły" i powiązane polecenie podsumowujące relację szczegółów zostały zaktualizowane tak, aby działały w trybie koncentracji uwagi. (#13106)
* Seika Notetaker może być teraz automatycznie wykrywany po podłączeniu przez USB i Bluetooth. (#13191, #13142)
  * Dotyczy to następujących urządzeń: MiniSeika (16, 24 ogniwa), V6 i V6Pro (40 ogniw)
  * Obsługiwany jest również ręczny wybór portu COM bluetooth.
* Dodano polecenie przełączania przeglądarki brajla; Nie ma domyślnego skojarzonego gestu. (#13258)
* Dodano polecenia do jednoczesnego przełączania wielu modyfikatorów za pomocą monitora brajlowskiego (#13152)
* Okno dialogowe Słownik mowy zawiera teraz przycisk "Usuń wszystko", który pomaga wyczyścić cały słownik. (#11802)
* Dodano obsługę kalkulatora systemu Windows 11. (#13212)
* W programie Microsoft Word z włączoną automatyzacją interfejsu użytkownika w systemie Windows 11 można teraz raportować numery wierszy i numery sekcji. (#13283, #13515)
* W przypadku pakietu Microsoft Office 16.0.15000 i nowszych w systemie Windows 11 NVDA domyślnie użyje automatyzacji interfejsu użytkownika do uzyskiwania dostępu do dokumentów Microsoft Word, zapewniając znaczną poprawę wydajności w porównaniu ze starym dostępem do modelu obiektowego. (#13437)
 * Obejmuje to dokumenty w samym programie Microsoft Word, a także czytnik wiadomości i edytor w programie Microsoft Outlook.

### Zmiany

* Espeak-ng został zaktualizowany do wersji 1.51-dev commit '7e5457f91e10'. (#12950)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
  * Dodano nową tabelę brajlowską: japoński (Kantenji) literacki alfabet Braille'a.
  * Dodano nową niemiecką tabelę brajlowską z 6 punktami.
  * Dodano katalońską tabelę brajlowską stopnia 1. (#13408)
* NVDA będzie raportować zaznaczenie i scalone komórki w LibreOffice Calc 7.3 i nowszych. (#9310, #6897)
* Zaktualizowano repozytorium danych ujednoliconych w standardzie ujednoliconym (CLDR) do wersji 40.0. (#12999)
* 'NVDA+Numpad Delete' domyślnie informuje o lokalizacji kursora lub obiektu aktywnego. (#13060)
* 'NVDA+Shift+Numpad Delete' informuje o położeniu kursora przeglądania. (#13060)
* Dodano domyślne powiązania do przełączania modyfikatorów na wyświetlaczach Freedom Scientific (#13152)
* "Linia bazowa" nie jest już raportowana za pomocą polecenia formatowania tekstu raportu ("NVDA+f"). (#11815)
* Aktywacja długiego opisu nie ma już przypisanego domyślnego gestu. (#13380)
* Podsumowanie szczegółów raportu ma teraz domyślny gest ('NVDA+d'). (#13380)
* NVDA musi zostać ponownie uruchomiony po zainstalowaniu MathPlayera. (#13486)

### Poprawki błędów

* Okienko menedżera schowka nie powinno już nieprawidłowo kraść fokusu podczas otwierania niektórych programów pakietu Office. (#12736)
* W systemie, w którym użytkownik zdecydował się zamienić główny przycisk myszy z lewej na prawą, NVDA nie będzie już przypadkowo wyświetlać menu kontekstowego zamiast aktywować element, w aplikacjach takich jak przeglądarki internetowe. (#12642)
* Podczas przesuwania kursora recenzji poza koniec kontrolek tekstu, na przykład w programie Microsoft Word z automatyzacją interfejsu użytkownika, w większej liczbie sytuacji "dół" jest poprawnie zgłaszany. (#12808)
* NVDA może raportować nazwę i wersję aplikacji dla plików binarnych umieszczonych w system32, gdy działa pod 64-bitową wersją systemu Windows. (#12943)
* Poprawiono spójność odczytu danych wyjściowych w programach terminalowych. (#12974)
  * Należy pamiętać, że w niektórych sytuacjach, podczas wstawiania lub usuwania znaków w środku wiersza, znaki po daszku mogą zostać ponownie odczytane.
* MS word z UIA: szybka nawigacja nagłówka w trybie przeglądania nie zacina się już na ostatnim nagłówku dokumentu, ani ten nagłówek nie jest wyświetlany dwukrotnie na liście elementów NVDA. (#9540)
* W systemie Windows 8 i nowszych pasek stanu Eksploratora plików można teraz pobrać za pomocą standardowego gestu NVDA+end (komputer stacjonarny) / NVDA+shift+end (laptop). (#12845)
* Wiadomości przychodzące na czacie programu Skype dla firm są ponownie zgłaszane. (#9295)
* NVDA może ponownie wyciszyć dźwięk podczas korzystania z syntezatora SAPI5 w systemie Windows 11. (#12913)
* W kalkulatorze systemu Windows 10 NVDA ogłosi etykiety dla elementów historii i listy pamięci. (#11858)
* Gesty, takie jak przewijanie i routing, ponownie działają z urządzeniami brajlowskimi HID. (#13228)
* Poczta systemu Windows 11: Po przełączeniu fokusu między aplikacjami, podczas czytania długiej wiadomości e-mail, NVDA nie zacina się już na wierszu wiadomości e-mail. (#13050)
* Pismo Braille'a HID: gesty akordowe (np. "spacja+punkt4") mogą być z powodzeniem wykonywane z monitora brajlowskiego. (#13326)
* Naprawiono problem polegający na tym, że można było otworzyć wiele okien dialogowych ustawień w tym samym czasie. (#12818)
* Naprawiono problem polegający na tym, że niektóre monitory brajlowskie Focus Blue przestawały działać po wybudzeniu komputera z trybu uśpienia. (#9830)
* "Linia bazowa" nie jest już fałszywie raportowana, gdy aktywna jest opcja "indeks górny i dolny raportu". (#11078)
* W systemie Windows 11 NVDA nie będzie już uniemożliwiać nawigacji w panelu emoji podczas wybierania emotikonów. (#13104)
* Zapobiega usterce powodującej podwójne raportowanie podczas korzystania z konsoli systemu Windows i terminala. (#13261)
* Rozwiązano kilka przypadków, w których elementy listy nie mogły być zgłaszane w aplikacjach 64-bitowych, takich jak REAPER. (#8175)
* W menedżerze pobierania Microsoft Edge, NVDA automatycznie przełączy się w tryb skupienia, gdy element listy z ostatnio pobranym plikiem stanie się aktywny. (#13221)
* NVDA nie powoduje już zawieszania się 64-bitowych wersji Notepad++ 8.3 i nowszych. (#13311)
* Program Adobe Reader nie ulega już awarii podczas uruchamiania, jeśli włączony jest tryb chroniony programu Adobe Reader. (#11568)
* Naprawiono błąd, który sprawiał, że wybranie sterownika monitora brajlowskiego Papenmeier powodowało awarię NVDA. (#13348)
* W programie Microsoft Word z interfejsem użytkownika: numer strony i inne formatowanie nie są już nieprawidłowo ogłaszane podczas przechodzenia z pustej komórki tabeli do komórki z treścią lub z końca dokumentu do istniejącej zawartości. (#13458, #13459)
* NVDA nie będzie już ignorować tytułu strony i automatycznie odczytywać, gdy strona ładuje się w Google Chrome 100. (#13571)
* NVDA nie ulega już awarii podczas resetowania konfiguracji NVDA do domyślnych ustawień fabrycznych, gdy włączone są poleceń mów. (#13634)

### Zmiany dla deweloperów

* Uwaga: jest to wersja niezgodna z interfejsem API dodatku. Dodatki będą musiały zostać ponownie przetestowane i mieć zaktualizowany manifest.
* Mimo że NVDA nadal wymaga programu Visual Studio 2019, kompilacje nie powinny już kończyć się niepowodzeniem, jeśli nowsza wersja programu Visual Studio (np. 2022) jest zainstalowana wraz z 2019 rokiem. (#13033, #13387)
* Zaktualizowano SCons do wersji 4.3.0. (#13033)
* Zaktualizowano py2exe do wersji 0.11.1.0. (#13510)
* Usunięto plik 'NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable'. Zamiast tego użyj "apiLevel". (#12955, #12660)
* Element "TVItemStruct" został usunięty z pliku "sysTreeView32". (#12935)
* Element "MessageItem" został usunięty z modułu aplikacji Outlook. (#12935)
* Stałe "audioDucking.AUDIODUCKINGMODE_*" są teraz "DisplayStringIntEnum". (#12926)
  * użycia powinny zostać zastąpione przez "AudioDuckingMode.*"
  * uzytkowniki 'audioDuckingModes' powinny zostac zamienione na 'AudioDuckingMode.*.displayString'
* Użycie stałych 'audioDucking.ANRUS_ducking_*' powinno zostać zastąpione przez 'ANRUSDucking.*'. (#12926)
* Zmiany w pliku "synthDrivers.sapi5" (#12927):
  * Użycia "SPAS_*" powinny zostać zastąpione przez "SPAudioState.*"
  * 'stałe. Użycie SVSF*" powinno zostać zastąpione przez "SpeechVoiceSpeakFlags.*"
    * Uwaga: "SVSFlagsAsync" należy zastąpić ciągiem "SpeechVoiceSpeakFlags.Async", a nie "SpeechVoiceSpeakFlags.lagsAsync"
  * 'stałe. Użycia SVE*" powinny zostać zastąpione przez "SpeechVoiceEvents.*"
* Moduł aplikacji 'soffice' ma następujące klasy i funkcje, usunięte 'JAB_OOTableCell', 'JAB_OOTable', 'gridCoordStringToNumbers'. (#12849)
* – Rdzeń. CallCancelled" to teraz "wyjątki". CallCancelled'. (#12940)
* Wszystkie stałe rozpoczynające się od RPC z "core" i "logHandler" są przenoszone do wyliczenia "RPCConstants.RPC". (#12940)
* Zaleca się, aby funkcje 'mouseHandler.doPrimaryClick' i 'mouseHandler.doSecondaryClick' były używane do klikania myszą w celu wykonania logicznej akcji, takiej jak aktywacja (podstawowa) lub pomocnicza (pokaż menu kontekstowe),
zamiast używać "executeMouseEvent" i określać konkretnie lewy lub prawy przycisk myszy.
Gwarantuje to, że kod będzie honorował ustawienie użytkownika systemu Windows dotyczące zamiany podstawowego przycisku myszy. (#12642)
* Plik "config.getSystemConfigPath" został usunięty — nie ma zamiennika. (#12943)
* 'shlobj. SHGetFolderPath' został usunięty - użyj 'shlobj. SHGetKnownFolderPath'. (#12943)
* Stałe 'shlobj' zostały usunięte. Utworzono nowe wyliczenie, 'shlobj. FolderId" do użycia z "SHGetKnownFolderPath". (#12943)
* "diffHandler.get_dmp_algo" i "diffHandler.get_difflib_algo" zastąpiono odpowiednio liczbami "diffHandler.prefer_dmp" i "diffHandler.prefer_difflib". (#12974)
* 'languageHandler.curLang' został usunięty - aby uzyskać aktualny język NVDA, użyj 'languageHandler.getLanguage()'. (#13082)
* Metoda 'getStatusBarText' może być zaimplementowana w appModule, aby dostosować sposób, w jaki NVDA pobiera tekst z paska stanu. (#12845)
* Plik "globalVars.appArgsExtra" został usunięty. (#13087)
  * Jeśli Twój dodatek musi przetworzyć dodatkowe argumenty wiersza poleceń, zapoznaj się z dokumentacją "addonHandler.isCLIParamKnown" i przewodnikiem dla programistów, aby uzyskać szczegółowe informacje.
* Moduł obsługi UIA i inne moduły wsparcia UIA są teraz częścią pakietu UIAHandler. (#10916)
  * "UIAUtils" to teraz "UIAHandler.utils"
  * "UIABrowseMode" to teraz "UIAHandler.browseMode"
  * "_UIAConstants" to teraz "UIAHandler.constants"
  * "_UIACustomProps" to teraz "UIAHandler.customProps"
  * "_UIACustomAnnotations" to teraz "UIAHandler.customAnnotations"
* Stałe "IAccessibleHandler" "IA2_RELATION_*" zostały zastąpione wyliczeniem "IAccessibleHandler.RelationType". (#13096)
  * Usunięto "IA2_RELATION_FLOWS_FROM"
  * Usunięto "IA2_RELATION_FLOWS_TO"
  * Usunięto "IA2_RELATION_CONTAINING_DOCUMENT"
* Wartości "LOCALE_SLANGUAGE", "LOCALE_SLIST" i "LOCALE_SLANGDISPLAYNAME" są usuwane z elementu "languageHandler" — zamiast tego należy użyć elementów członkowskich elementu "languageHandler.LOCALE". (#12753)
* Przełączono z Minhook na Microsoft Detours jako bibliotekę przechwytującą dla NVDA. Podpinanie za pomocą tej biblioteki służy głównie do wspomagania modelu wyświetlania. (#12964)
* Skreśla się "winVersion.WIN10_RELEASE_NAME_TO_BUILDS". (#13211)
* SCons ostrzega teraz o konieczności kompilacji z liczbą zadań równą liczbie procesorów logicznych w systemie.
Może to znacznie skrócić czas kompilacji w systemach wielordzeniowych. (#13226, #13371)
* Stałe 'characterProcessing.SYMLVL_*' są usuwane - zamiast tego użyj 'characterProcessing.SymbolLevel.*'. (#13248)
* Funkcje 'loadState' i 'saveState' są usuwane z addonHandler - zamiast tego użyj 'addonHandler.state.load' i 'addonHandler.state.save'. (#13245)
* Przeniesiono warstwę interakcji UWP/OneCore NVDAHelper [z C++/CX do C++/Winrt](https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx). (#10662)
* Aby z niego korzystać, konieczne jest teraz użycie podklasy 'DictionaryDialog'. (#13268)
* 'config. RUN_REGKEY', 'config. NVDA_REGKEY' są przestarzałe, użyj 'config. RegistryKey.RUN', 'config. RegistryKey.NVDA'. Zostaną one usunięte w 2023 roku. (#13242)
* "easeOfAccess.ROOT_KEY", "easeOfAccess.APP_KEY_PATH" są przestarzałe, zamiast tego użyj "easeOfAccess.RegistryKey.ROOT", "easeOfAccess.RegistryKey.APP". Zostaną one usunięte w 2023 roku. (#13242)
* Parametr "easeOfAccess.APP_KEY_NAME" został uznany za przestarzały i ma zostać usunięty w 2023 roku. (#13242)
* Pliki "DictionaryDialog" i "DictionaryEntryDialog" zostały przeniesione z "gui.settingsDialogs" do "gui.speechDict". (#13294)
* Relacje IAccessible2 są teraz wyświetlane w informacjach dla programistów dla obiektów IAccessible2. (#13315)
* Usunięto ciąg "languageHandler.windowsPrimaryLCIDsToLocaleNames", zamiast tego należy użyć adresu "languageHandler.windowsLCIDToLocaleName" lub "winKernel.LCIDToLocaleName". (#13342)
* Właściwość "UIAAutomationId" dla obiektów UIA powinna być preferowana w stosunku do wartości "cachedAutomationId". (#13125, #11447)
  * Identyfikator "cachedAutomationId" może być używany, jeśli jest uzyskiwany bezpośrednio z elementu.
* Plik "NVDAObjects.window.scintilla.CharacterRangeStruct" został przeniesiony do pliku "NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct". (#13364)
* Wartość logiczna "gui.isInMessageBox" jest usuwana, zamiast tego użyj funkcji "gui.message.isModalMessageBoxActive". (#12984, #13376)
* Parametr 'controlTypes' został podzielony na różne podmoduły. (#12510, #13588)
  * "ROLE_*" i "STATE_*" zostały zastąpione przez "Rola.*" i "Państwo.*".
  * Mimo że nadal są dostępne, następujące elementy należy uznać za przestarzałe:
    * "ROLE_*" i "STATE_*", zamiast tego użyj "Role.*" i "State.*".
    * 'roleLabels', 'stateLabels' i 'negativeStateLabels', użycia takie jak 'roleLabels[ROLE_*]' powinny zostać zastąpione ich odpowiednikami "Role.*.displayString" lub "State.*.negativeDisplayString".
    * "processPositiveStates" i "processNegativeStates" powinny zamiast tego używać "processAndLabelStates".
* Stałe stanu komórki programu Excel ("NVSTATE_*") są teraz wartościami w wyliczeniu "NvCellState", dublowanymi w wyliczeniu "NvCellState" w "NVDAObjects/window/excel.py" i mapowanymi na "controlTypes.State" za pośrednictwem _nvCellStatesToStates. (#13465)
* Element członkowski struktury "EXCEL_CELLINFO" to teraz "nvCellStates".
* 'mathPres.ensureInit' został usunięty, MathPlayer jest teraz inicjowany po uruchomieniu NVDA. (#13486)

## 2021.3.5

Jest to drobna wersja, która ma na celu rozwiązanie problemu z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki zabezpieczeń

* Usunięto błąd w poradniku bezpieczeństwa "GHSA-xc5m-v23f-pgr7".
  * Okno dialogowe wymowy symboli jest teraz wyłączone w trybie bezpiecznym.

## 2021.3.4

Jest to niewielka wersja, która ma na celu naprawienie kilku zgłoszonych problemów z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki zabezpieczeń

* Usunięto błąd w poradniku zabezpieczeń "GHSA-354r-wr4v-cx28". (#13488)
  * Usunięto możliwość uruchamiania NVDA z włączonym rejestrowaniem debugowania, gdy NVDA działa w trybie bezpiecznym.
  * Usunięto możliwość aktualizacji NVDA, gdy NVDA działa w trybie bezpiecznym.
* Usunięto błąd w poradniku zabezpieczeń "GHSA-wg65-7r23-h6p9". (#13489)
  * Usuń możliwość otwierania okna dialogowego gestów wejściowych w trybie bezpiecznym.
  * Usunięto możliwość otwierania domyślnych, tymczasowych i głosowych okien dialogowych słownika w trybie bezpiecznym.
* Usunięto błąd w poradniku bezpieczeństwa "GHSA-mvc8-5rv9-w3hx". (#13487)
  * Narzędzie do inspekcji graficznego interfejsu użytkownika wx jest teraz wyłączone w trybie bezpiecznym.

## 2021.3.3

Ta wersja jest identyczna z wersją 2021.3.2.
W NVDA 2021.3.2 istniał błąd, w którym błędnie identyfikował się jako 2021.3.1.
Ta wersja poprawnie identyfikuje się jako 2021.3.3.

## 2021.3.2

Jest to niewielka wersja, która ma na celu naprawienie kilku zgłoszonych problemów z zabezpieczeniami.
Prosimy o odpowiedzialne ujawnianie <info@nvaccess.org> problemów związanych z bezpieczeństwem.

### Poprawki błędów

* Poprawka zabezpieczeń: Zapobiegaj nawigacji po obiektach poza ekranem blokady w systemach Windows 10 i Windows 11. (#13328)
* Poprawka bezpieczeństwa: Okno dialogowe menedżera dodatków jest teraz wyłączone na bezpiecznych ekranach. (#13059)
* Poprawka bezpieczeństwa: Pomoc kontekstowa NVDA nie jest już dostępna na bezpiecznych ekranach. (#13353)

## 2021.3.1

Jest to niewielka wersja, która ma na celu rozwiązanie kilku problemów w wersji 2021.3.

### Zmiany

* Nowy protokół brajlowski HID nie jest już preferowany, gdy można użyć innego sterownika monitora brajlowskiego. (#13153)
* Nowy protokół HID Braille można wyłączyć za pomocą ustawień w panelu ustawień zaawansowanych. (#13180)

### Poprawki błędów

* Punkt orientacyjny jest znowu skrócony na monitorze brajlowskim. #13158
* Naprawiono niestabilne automatyczne wykrywanie dla monitorów brajlowskich Humanware Brailliant i APH Mantis Q40, gdy używany jest bluetooth. (#13153)

## 2021.3

W tym wydaniu wprowadzono obsługę nowej specyfikacji HID Braille'a.
Specyfikacja ta ma na celu ujednolicenie obsługi monitorów brajlowskich bez konieczności stosowania indywidualnych sterowników.
Wprowadzono aktualizacje eSpeak-NG i LibLouis, w tym nowe tabele Russian i Tshivenda.
Dźwięki błędów można włączyć w stabilnych wersjach NVDA za pomocą nowej opcji ustawień zaawansowanych.
Opcja Powiedz wszystko w programie Word przewija teraz widok, aby bieżąca pozycja była widoczna.
Podczas korzystania z pakietu Office z interfejsem użytkownika wprowadzono wiele ulepszeń.
Jedną z poprawek UIA jest to, że program Outlook ignoruje teraz więcej typów tabel układu w wiadomościach.

Ważne notatki:

Ze względu na aktualizację naszego certyfikatu bezpieczeństwa, niewielka liczba użytkowników otrzymuje błąd, gdy NVDA 2021.2 sprawdza dostępność aktualizacji.
NVDA prosi teraz system Windows o aktualizację certyfikatów bezpieczeństwa, co zapobiegnie temu błędowi w przyszłości.
Użytkownicy, których dotyczy problem, będą musieli pobrać tę aktualizację ręcznie.

### Nowe funkcje

* Dodaje gest wejściowy do przełączania ustawień raportowania stylu obramowań komórek. (#10408)
* Obsługa nowej specyfikacji HID Braille'a, która ma na celu standaryzację obsługi monitorów brajlowskich. (#12523)
  * Urządzenia, które obsługują tę specyfikację, będą automatycznie wykrywane przez NVDA.
  * Szczegóły techniczne na temat implementacji tej specyfikacji przez NVDA można znaleźć w https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Dodano obsługę urządzenia brajlowskiego VisioBraille Vario 4. (#12607)
* Powiadomienia o błędach mogą być włączone (ustawienia zaawansowane) podczas korzystania z dowolnej wersji NVDA. (#12672)
* W systemie Windows 10 i nowszych NVDA ogłosi liczbę sugestii podczas wprowadzania wyszukiwanych haseł w aplikacjach, takich jak Ustawienia i Microsoft Store. (#7330, #12758, #12790)
* Nawigacja po tabelach jest teraz obsługiwana w kontrolkach siatki utworzonych przy użyciu polecenia cmdlet Out-GridView w programie PowerShell. (#12928)

### Zmiany

* Espeak-ng został zaktualizowany do wersji 1.51-dev commit '74068b91bcd578bd7030a7a6cde2085114b79b44'. (#12665)
* NVDA domyślnie wybierze eSpeak, jeśli żaden z zainstalowanych głosów OneCore nie obsługuje preferowanego języka NVDA. (#10451)
* Jeśli głosy OneCore stale nie mówią, powróć do eSpeak jako syntezatora. (#11544)
* Podczas czytania paska stanu z 'NVDA+end', kursor przeglądania nie jest już przesuwany na swoje miejsce.
Jeśli potrzebujesz tej funkcjonalności, przypisz gest do odpowiedniego skryptu w kategorii Nawigacja po obiektach w oknie dialogowym Gesty wprowadzania. (#8600)
* Podczas otwierania okna dialogowego ustawień, które jest już otwarte, NVDA skupia się na istniejącym oknie dialogowym, zamiast zgłaszać błąd. (#5383)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Nowe tablice brajlowskie: rosyjski stopień 1, Tshivenda stopień 1, Tshivenda stopień 2
* Zamiast "oznaczona treść" lub "mrkd", "highlight" lub "hlght" będą ogłaszane odpowiednio dla mowy i alfabetu Braille'a. (#12892)
* NVDA nie będzie już próbowało wyjść, gdy okna dialogowe oczekują na wymagane działanie (np. Potwierdź/Anuluj). (#12984)

### Poprawki błędów

* Modyfikatory klawiatury śledzenia (takie jak Control lub Insert) są bardziej niezawodne, gdy watchdog jest odzyskiwany. (#12609)
* Po raz kolejny możliwe jest sprawdzenie dostępności aktualizacji NVDA w niektórych systemach; np. czyste instalacje systemu Windows. (#12729)
* NVDA poprawnie odczytuje puste komórki tabeli w programie Microsoft Word podczas korzystania z automatyzacji interfejsu użytkownika. (#11043)
* W komórkach siatki danych ARIA w Internecie Escape będzie teraz przekazywany do siatki i nie będzie już bezwarunkowo wyłączał trybu ostrości. (#12413)
* Podczas odczytywania komórki nagłówka tabeli w Chrome popraw dwukrotne ogłaszanie nazwy kolumny. (#10840)
* NVDA nie podaje już wartości liczbowej dla suwaków UIA, które mają zdefiniowaną tekstową reprezentację ich wartości. (UIA ValuePattern jest teraz preferowany w stosunku do RangeValuePattern). (#12724)
* NVDA nie traktuje już wartości suwaków UIA jako zawsze procentowej.
* Raportowanie lokalizacji komórki w programie Microsoft Excel po uzyskaniu dostępu za pośrednictwem automatyzacji interfejsu użytkownika ponownie działa poprawnie w systemie Windows 11. (#12782)
* NVDA nie ustawia już nieprawidłowych ustawień regionalnych Pythona. (#12753)
* Jeśli wyłączony dodatek zostanie odinstalowany, a następnie ponownie zainstalowany, zostanie ponownie włączony. (#12792)
* Naprawiono błędy związane z aktualizacją i usuwaniem dodatków, w których folder dodatków został zmieniony lub mają otwarte pliki. (#12792, #12629)
* Podczas korzystania z automatyzacji interfejsu użytkownika w celu uzyskania dostępu do kontrolek arkusza kalkulacyjnego programu Microsoft Excel, NVDA nie informuje już nadmiarowo, kiedy zaznaczona jest pojedyncza komórka. (#12530)
* Większa część tekstu okna dialogowego jest automatycznie odczytywana w programie LibreOffice Writer, na przykład w oknach dialogowych potwierdzenia. (#11687)
* Czytanie/nawigowanie w trybie przeglądania w programie Microsoft Word za pomocą automatyzacji interfejsu użytkownika zapewnia teraz, że dokument jest zawsze przewijany tak, aby bieżąca pozycja trybu przeglądania była widoczna, a pozycja kursora w trybie koncentracji uwagi poprawnie odzwierciedlała pozycję trybu przeglądania. (#9611)
* Podczas wykonywania czynności Powiedz wszystko w programie Microsoft Word za pomocą automatyzacji interfejsu użytkownika dokument jest teraz automatycznie przewijany, a pozycja karetki jest poprawnie aktualizowana. (#9611)
* Podczas czytania wiadomości e-mail w Outlooku, a NVDA uzyskuje dostęp do wiadomości za pomocą automatyzacji interfejsu użytkownika, niektóre tabele są teraz oznaczone jako tabele układu, co oznacza, że nie będą już domyślnie raportowane. (#11430)
* Naprawiono rzadki błąd występujący przy zmianie urządzeń audio. (#12620)
* Wprowadzanie danych z literackimi tabelami brajlowskimi powinno zachowywać się bardziej niezawodnie w polach edycji. (#12667)
* Podczas nawigacji po kalendarzu w zasobniku systemowym Windows, NVDA podaje teraz dzień tygodnia w całości. (#12757)
* W przypadku korzystania z chińskiej metody wprowadzania, takiej jak Tajwan - Microsoft Quick w programie Microsoft Word, przewijanie monitora brajlowskiego do przodu i do tyłu nie powoduje już nieprawidłowego powrotu do pierwotnej pozycji karetki higienicznej. (#12855)
* Podczas uzyskiwania dostępu do dokumentów Microsoft Word za pośrednictwem interfejsu użytkownika nawigacja według zdania (alt+strzałka w dół / alt+strzałka w górę) jest ponownie możliwa. (#9254)
* Podczas uzyskiwania dostępu do MS Word za pomocą UIA, wcięcia akapitów są teraz zgłaszane. (#12899)
* Podczas uzyskiwania dostępu do MS Word za pomocą UIA, polecenie śledzenia zmian i niektóre inne zlokalizowane polecenia są teraz zgłaszane w programie Word . (#12904)
* Poprawiono zduplikowanie brajla i mowy, gdy "opis" pasuje do "treści" lub "nazwy". (#12888)
* W programie MS Word z włączoną funkcją UIA dokładniejsze odtwarzanie błędów ortograficznych podczas pisania. (#12161)
* W systemie Windows 11 NVDA nie będzie już ogłaszać "okienka" po naciśnięciu Alt + Tab w celu przełączania między programami. (#12648)
* Nowy panel ścieżki bocznej Modern Comments jest teraz obsługiwany w MS Word, gdy nie uzyskujesz dostępu do dokumentu za pośrednictwem interfejsu użytkownika. Naciśnij alt+f12, aby przechodzić między bocznym panelem ścieżki a dokumentem. (#12982)

### Zmiany dla deweloperów

* Kompilowanie NVDA wymaga teraz programu Visual Studio 2019 16.10.4 lub nowszego.
Aby dopasować produkcyjne środowisko kompilacji, zaktualizuj program Visual Studio, aby zachować synchronizację z [bieżącą wersją używaną przez AppVeyor](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019). (#12728)
* Plik "NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable" został uznany za przestarzały do usunięcia w wersji 2022.1. (#12660)
  * Zamiast tego użyj 'apiLevel' (zobacz komentarze na '_UIAConstants.WinConsoleAPILevel', aby uzyskać szczegółowe informacje).
* Przezroczystość koloru tła tekstu pochodzącego z aplikacji GDI (za pośrednictwem modelu wyświetlania) jest teraz widoczna dla dodatków lub modułów aplikacji. (#12658)
* Wartości "LOCALE_SLANGUAGE", "LOCALE_SLIST" i "LOCALE_SLANGDISPLAYNAME" są przenoszone do wyliczenia "LOCALE" w languageHandler.
Są one nadal dostępne na poziomie modułu, ale są przestarzałe i mają zostać usunięte w NVDA 2022.1. (#12753)
* Użycie funkcji "addonHandler.loadState" i "addonHandler.saveState" powinno zostać zastąpione ich odpowiednikami "addonHandler.state.save" i "addonHandler.state.load" przed 2022.1. (#12792)
* Wyjście brajlowskie można teraz sprawdzić w testach systemowych. (#12917)

## 2021.2

W tej wersji wprowadzono wstępną obsługę systemu Windows 11.
Chociaż system Windows 11 nie został jeszcze wydany, ta wersja została przetestowana w wersjach zapoznawczych systemu Windows 11.
Obejmuje to ważną poprawkę dla kurtyny ekranowej (patrz ważne uwagi).
Narzędzie do naprawy rejestracji COM może teraz rozwiązać więcej problemów podczas korzystania z NVDA.
Wprowadzono aktualizacje syntezatora eSpeak i tłumacza brajlowskiego LibLouis.
Istnieją również różne poprawki błędów i ulepszenia, w szczególności dotyczące obsługi alfabetu Braille'a i terminali Windows, kalkulatora, panelu emoji i historii schowka.

### Ważne wskazówki

Ze względu na zmianę w interfejsie API powiększania systemu Windows kurtyna ekranowa musiała zostać zaktualizowana, aby obsługiwała najnowsze wersje systemu Windows.
Użyj NVDA 2021.2, aby aktywować kurtynę w systemie Windows 10 21H2 (10.0.19044) lub nowszym.
Obejmuje to niejawnych testerów systemu Windows 10 i systemu Windows 11.
Ze względów bezpieczeństwa w przypadku korzystania z nowej wersji systemu Windows należy uzyskać wizualne potwierdzenie, że kurtyna sprawia, że ekran jest całkowicie.

### Nowe funkcje

* Eksperymentalne wsparcie dla adnotacji ARIA:
  * Dodaje polecenie do odczytu podsumowania szczegółów obiektu za pomocą aria-details. (#12364)
  * Dodaje opcję w preferencjach zaawansowanych, aby raportować, czy obiekt ma szczegóły w trybie przeglądania. (#12439)
* W systemie Windows 10 w wersji 1909 i nowszych (w tym Windows 11) NVDA ogłosi liczbę sugestii podczas wyszukiwania w Eksploratorze plików. (#10341, #12628)
* W Microsoft Word, NVDA ogłasza teraz wynik skrótów do wcięć i zawieszania się po ich wykonaniu. (#6269)

### Zmiany

* Espeak-ng został zaktualizowany do wersji 1.51-dev commit 'ab11439b18238b7a08b965d1d5a6ef31cbb05cbb'. (#12449, #12202, #12280, #12568)
* Jeśli artykuł jest włączony w preferencjach użytkownika do formatowania dokumentu, NVDA ogłasza "article" po treści. (#11103)
* Zaktualizowano tłumacz brajlowski liblouis do wersji [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Nowe tablice brajlowskie: bułgarski 1, birmański 1, birmański 2, kazachski 1, khmerski 0, 1 stopień sepedi, 2 stopień sepedi, 1 stopień sesotho, 1 stopień sesotho, stopień 1 sesotho, stopień 2 w setswana, stopień 1 w setswanie, stopień 1 w języku tatarskim, stopień 1 w języku tatarskim, w języku wietnamskim 0, w języku wietnamskim 2, w stopniu 1 w Wietnamie Południowym, w stopniu 1 w języku Xhosa,  Xhosa stopień 2, jakucki stopień 1, zulu stopień 1, zulu stopień 2
* Nazwa OCR systemu Windows 10 została zmieniona na Windows OCR. (#12690)

### Poprawki błędów

* W Kalkulatorze Windows 10 NVDA ogłosi wyrażenia kalkulatora na monitorze brajlowskim. (#12268)
* W programach terminalowych w systemie Windows 10 w wersji 1607 lub nowszej podczas wstawiania lub usuwania znaków w środku wiersza znaki po prawej stronie karetki nie są już odczytywane. (#3200)
  * Poprawka Diff Match jest teraz domyślnie włączona. (#12485)
* Wprowadzanie brajlowskie działa poprawnie z następującymi tabelami skróconymi: arabski - ocena 2, hiszpański - ocena 2, urdu - ocena 2, chiński (Chiny, mandaryński) - ocena 2. (#12541)
* Narzędzie do naprawiania rejestracji COM rozwiązuje teraz więcej problemów, zwłaszcza w 64-bitowym systemie Windows. (#12560)
* Ulepszenia obsługi przycisków w urządzeniu Braille Seika Notetaker firmy Nippon Telesoft. (#12598)
* Ulepszenia ogłaszania panelu emotikonów systemu Windows i historii schowka. (#11485)
* Zaktualizowano opisy znaków w alfabecie bengalskim. (#12502)
* NVDA kończy się bezpiecznie, gdy uruchamiany jest nowy proces. (#12605)
* Ponowne wybranie sterownika monitora brajlowskiego Handy Tech w oknie dialogowym Wybierz monitor brajlowski nie powoduje już błędów. (#12618)
* System Windows w wersji 10.0.22000 lub nowszej jest rozpoznawany jako Windows 11, a nie Windows 10. (#12626)
* Obsługa kurtyn ekranowych została poprawiona i przetestowana dla wersji systemu Windows do 10.0.22000. (#12684)
* Jeśli podczas filtrowania gestów wejściowych nie są wyświetlane żadne wyniki, okno dialogowe konfiguracji gestów wejściowych będzie nadal działać zgodnie z oczekiwaniami. (#12673)
* Naprawiono błąd, który sprawiał, że pierwsza pozycja menu podmenu nie była ogłaszana w niektórych kontekstach. (#12624)

### Zmiany dla deweloperów

* Stałe "characterProcessing.SYMLVL_*" powinny zostać zastąpione ich odpowiednikiem "SymbolLevel.*" przed 2022 rokiem.1. (#11856, #12636)
* Parametr "controlTypes" został podzielony na różne podmoduły, symbole oznaczone jako przestarzałe muszą zostać zastąpione przed 2022 rokiem.1. (#12510)
  * Stałe "ROLE_*" i "STATE_*" powinny zostać zastąpione ich odpowiednikami "Rola.*" i "Stan.*".
  * Nazwy "roleLabels", "stateLabels" i "negativeStateLabels" zostały wycofane, a ich odpowiedniki takie jak "roleLabels[ROLE_*]" powinny zostać zastąpione ich odpowiednikami "Role.*.displayString" lub "State.*.negativeDisplayString".
  * Elementy "processPositiveStates" i "processNegativeStates" zostały uznane za przestarzałe do usunięcia.
* W systemie Windows 10 w wersji 1511 lub nowszej (w tym kompilacjach Insider Preview) bieżąca nazwa wydania aktualizacji funkcji systemu Windows jest uzyskiwana z rejestru systemu Windows. (#12509)
* Przestarzałe: "winVersion.WIN10_RELEASE_NAME_TO_BUILDS" zostanie usunięty w 2022 r.1, nie ma bezpośredniego zamiennika. (#12544)

## 2021.1

Ta wersja zawiera opcjonalną eksperymentalną obsługę UIA w przeglądarkach Excel i Chromium.
Wprowadzono poprawki dla kilku języków oraz dla dostępu do linków w alfabecie Braille'a.
Wprowadzono aktualizacje CLDR Unicode, symboli matematycznych i biblioteki LibLouis.
A także wiele poprawek błędów i ulepszeń, w tym w pakiecie Office, programie Visual Studio i kilku językach.

Uwaga:

 * Ta wersja zapewnia zgodność z istniejącymi dodatkami.
 * W tym wydaniu porzuca się również obsługę Adobe Flash.

### Nowe funkcje

* Wczesne wsparcie dla UIA w przeglądarkach opartych na Chromium (takich jak Edge). (#12025)
* Opcjonalna eksperymentalna obsługa programu Microsoft Excel za pośrednictwem automatyzacji interfejsu użytkownika. Zalecane tylko dla programu Microsoft Excel w wersji 16.0.13522.10000 lub nowszej. (#12210)
* Łatwiejsza nawigacja po danych wyjściowych w konsoli NVDA Python. (#9784)
  * Alt+góra/dół przeskakuje do poprzedniego/następnego wyniku wyjściowego (dodaj przesunięcie do wyboru).
  * Control+L czyści panel Wyjście.
* NVDA raportuje teraz kategorie przypisane do terminu w programie Microsoft Outlook, jeśli takie istnieją. (#11598)
* Obsługa monitora brajlowskiego Seika Notetaker firmy Nippon Telesoft. (#11514)

### Zmiany

* W trybie przeglądania elementy sterujące mogą być teraz aktywowane za pomocą przekierowywania kursora brajlowskiego na ich deskryptor (np. "lnk" dla linku). Jest to szczególnie przydatne do aktywacji np. pola wyboru bez etykiet. (#7447)
* NVDA uniemożliwia teraz użytkownikowi wykonanie OCR systemu Windows 10, jeśli włączona jest kurtyna ekranowa. (#11911)
* Zaktualizowano repozytorium danych ujednoliconych w standardzie CLDR (Common Locale Data Repository) do wersji 39.0. (#11943, #12314)
* Dodano więcej symboli matematycznych do słownika symboli. (#11467)
* Podręcznik użytkownika, plik zmian i lista poleceń klawiszowych mają teraz odświeżony wygląd. (#12027)
* "Nieobsługiwany" jest teraz zgłaszany przy próbie przełączenia układu ekranu w aplikacjach, które go nie obsługują, takich jak Microsoft Word. (#7297)
* Opcja "Próba anulowania mowy w przypadku wygasłych zdarzeń fokusu" w panelu ustawień zaawansowanych jest teraz domyślnie włączona. (#10885)
  * To zachowanie można wyłączyć, ustawiając tę opcję na "Nie".
  * Aplikacje internetowe (np. Gmail) nie odczytują już nieaktualnych informacji podczas szybkiego przełączania ostrości.
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Nowe tablice brajlowskie: białoruski alfabet literacki, białoruski brajl komputerowy, urdu klasa 1, urdu klasa 2.
* Wsparcie dla treści Adobe Flash zostało usunięte z NVDA ze względu na aktywne odradzanie korzystania z Flasha przez firmę Adobe. (#11131)
* NVDA zakończy działanie nawet przy otwartych oknach, proces zamykania zamyka teraz wszystkie okna i okna dialogowe NVDA. (#1740)
* Przeglądarkę mowy można teraz zamknąć za pomocą "alt+F4" i ma standardowy przycisk zamykania ułatwiający interakcję z użytkownikami urządzeń wskazujących. (#12330)
* Przeglądarka Braille'a ma teraz standardowy przycisk zamykania, który ułatwia interakcję z użytkownikami urządzeń wskazujących. (#12328)
* W oknie dialogowym Lista elementów przyspieszenia na przycisku "Aktywuj" został usunięty w niektórych lokalizacjach, aby uniknąć kolizji z etykietą przycisku radiowego typu elementu. Jeśli jest dostępny, przycisk jest nadal domyślny w oknie dialogowym i jako taki może być nadal wywoływany, po prostu naciskając enter z samej listy elementów. (#6167)

### Poprawki błędów

* Lista wiadomości w programie Outlook 2010 jest ponownie czytelna. (#12241)
* W programach terminalowych w systemie Windows 10 w wersji 1607 lub nowszej podczas wstawiania lub usuwania znaków w środku wiersza znaki po prawej stronie karetki nie są już odczytywane. (#3200)
  * Ta eksperymentalna poprawka musi być ręcznie włączona w panelu ustawień zaawansowanych NVDA poprzez zmianę algorytmu różnicowania na Diff Match Patch.
* W MS Outlook niewłaściwe raportowanie odległości po przesunięciu shift+tab z treści wiadomości do pola tematu nie powinno już występować. (#10254)
* W konsoli Pythona wstawianie tabulatora w celu wcięcia na początku niepustego wiersza wejściowego i uzupełnianie tabulatora w środku wiersza wejściowego jest teraz obsługiwane. (#11532)
* Informacje o formatowaniu i inne wiadomości, które można przeglądać, nie zawierają już nieoczekiwanych pustych wierszy, gdy układ ekranu jest wyłączony. (#12004)
* Możliwe jest teraz czytanie komentarzy w MS Word z włączonym UIA. (#9285)
* Poprawiono wydajność podczas interakcji z programem Visual Studio. (#12171)
* Napraw błędy graficzne, takie jak brakujące elementy podczas korzystania z NVDA z układem od prawej do lewej. (#8859)
* Szanuj kierunek układu GUI oparty na języku NVDA, a nie na ustawieniach regionalnych systemu. (#638)
  * Znany problem dla języków pisanych od prawej do lewej: prawa krawędź grupowania klipów z etykietami/kontrolkami. (#12181)
* Ustawienia regionalne języka python są ustawione tak, aby odpowiadały językowi wybranemu w preferencjach i będą występować w przypadku korzystania z języka domyślnego. (#12214)
* TextInfo.getTextInChunks nie zawiesza się już po wywołaniu kontrolek Rich Edit, takich jak przeglądarka dziennika NVDA. (#11613)
* Po raz kolejny możliwe jest używanie NVDA w językach zawierających podkreślenia w nazwie ustawień regionalnych, takich jak de_CH w systemach Windows 10, 1803 i 1809. (#12250)
* W programie WordPad konfiguracja raportowania indeksu górnego/dolnego działa zgodnie z oczekiwaniami. (#12262)
* NVDA nie przerywa już ogłaszania nowo skoncentrowanej zawartości na stronie internetowej, jeśli stary fokus zniknie i zostanie zastąpiony nowym fokusem w tej samej pozycji. (#12147)
* Formatowanie przekreślenia, indeksu górnego i dolnego dla całych komórek programu Excel jest teraz raportowane, jeśli odpowiednia opcja jest włączona. (#12264)
* Naprawiono kopiowanie konfiguracji podczas instalacji z kopii przenośnej, gdy domyślny docelowy katalog konfiguracyjny jest pusty. (#12071, #12205)
* Naprawiono błędne ogłaszanie niektórych liter z akcentami lub znakami diakrytycznymi, gdy zaznaczona jest opcja "Powiedz wielką literę przed wielkimi literami". (#11948)
* Naprawiono błąd zmiany wysokości dźwięku w syntezatorze mowy SAPI4. (#12311)
* Instalator NVDA teraz honoruje również parametr wiersza poleceń '--minimal' i nie odtwarza dźwięku uruchamiania, postępując zgodnie z tym samym udokumentowanym zachowaniem, co zainstalowany lub przenośny plik wykonywalny NVDA. (#12289)
* W MS Word lub Outlook szybkiej nawigacji po tabeli może teraz przeskoczyć do tabeli układu, jeśli opcja "Uwzględnij tabele układu" jest włączona w ustawieniach trybu przeglądania. (#11899)
* NVDA nie będzie już ogłaszać "↑↑↑" dla emotikonów w poszczególnych językach. (#11963)
* Espeak ponownie obsługuje język kantoński i mandaryński. (#10418)
* W nowej przeglądarce Microsoft Edge opartej na Chromium pola tekstowe, takie jak pasek adresu, są teraz ogłaszane, gdy są puste. (#12474)
* Napraw sterownik Braille'a Seika. (#10787)

### Zmiany dla deweloperów

* Uwaga: jest to wersja niezgodna z interfejsem API dodatku. Dodatki będą musiały zostać ponownie przetestowane i mieć zaktualizowany manifest.
* System budowania NVDA pobiera teraz wszystkie zależności Pythona za pomocą i przechowuje je w wirtualnym środowisku Pythona. Wszystko to odbywa się w przejrzysty sposób.
  * Aby zbudować NVDA, SCony powinny być nadal używane w zwykły sposób. Np. wykonywanie scons.bat w katalogu głównym repozytorium. Uruchamianie 'py -m SCons' nie jest już obsługiwane, a 'scons.py' również zostało usunięte.
  * Aby uruchomić NVDA ze źródeł, zamiast bezpośrednio wykonywać 'source/nvda.pyw', programista powinien teraz użyć 'runnvda.bat' w katalogu głównym repozytorium. Jeśli spróbujesz uruchomić plik 'source/nvda.pyw', pojawi się komunikat informujący, że nie jest już obsługiwany.
  * Aby wykonać testy jednostkowe, wykonaj polecenie "rununittests.bat [<extra unittest discover options>]"</extra>
  * Aby przeprowadzić testy systemu: wykonaj polecenie "runsystemtests.bat [<extra robot options>]"</extra>
  * Aby wykonać linting, wykonaj polecenie 'runlint.bat <base branch>'
  * Więcej informacji można znaleźć w readme.md.
* Następujące zależności języka Python również zostały uaktualnione:
  * COMTYPES zaktualizowane do wersji 1.1.8.
  * pySerial zaktualizowany do wersji 3.5.
  * wxPython zaktualizowany do wersji 4.1.1.
  * Py2exe zaktualizowano do wersji 0.10.1.0.
* Usunięto "LiveText._getTextLines". (#11639)
  * Zamiast tego przesłoń ciąg "_getText", który zwraca ciąg całego tekstu w obiekcie.
* Obiekty "LiveText" mogą teraz obliczać różnice według znaków. (#11639)
  * Aby zmienić zachowanie różnic dla jakiegoś obiektu, nadpisz właściwość 'diffAlgo' (szczegóły w docstring).
* Podczas definiowania skryptu za pomocą dekoratora skryptu można określić argument logiczny "allowInSleepMode", aby kontrolować, czy skrypt jest dostępny w trybie uśpienia, czy nie. (#11979)
* Następujące funkcje są usuwane z modułu konfiguracyjnego. (#11935)
  * canStartOnSecureScreens — zamiast tego użyj pliku config.isInstalledCopy.
  * hasUiAccess i execElevated - użyj ich z modułu systemUtils.
  * getConfigDirs — zamiast tego użyj globalVars.appArgs.configPath.
* Stałe na poziomie modułu REASON_* są usuwane z controlTypes — zamiast tego należy użyć controlTypes.OutputReason. (#11969)
* REASON_QUICKNAV została usunięta z browseMode - zamiast tego użyj controlTypes.OutputReason.QUICKNAV. (#11969)
* Właściwość "isCurrent" "NVDAObject" (i pochodne) teraz ściśle zwraca klasę wyliczeniową "controlTypes.IsCurrent". (#11782)
  * Wartość "isCurrent" nie jest już opcjonalna, a zatem nie zwraca wartości None.
    * Gdy obiekt nie jest aktualny, zwracane jest "controlTypes.IsCurrent.NO".
* Mapowanie "controlTypes.isCurrentLabels" zostało usunięte. (#11782)
  * Zamiast tego użyj właściwości "displayString" dla wartości wyliczenia "controlTypes.IsCurrent".
    * Na przykład: "controlTypes.IsCurrent.YES.displayString".
* Plik 'winKernel.GetTimeFormat' został usunięty - zamiast niego użyj pliku 'winKernel.GetTimeFormatEx'. (#12139)
* Usunięto 'winKernel.GetDateFormat' - zamiast tego użyj 'winKernel.GetDateFormatEx'. (#12139)
* "Graficzny interfejs użytkownika. DriverSettingsMixin' został usunięty - użyj 'gui. Automatyczne ustawieniaMieszanie. (#12144)
* Usunięto "speech.getSpeechForSpelling" - użyj "speech.getSpellingSpeech". (#12145)
* Poleceń nie można bezpośrednio importować z mowy jako "importuj mowę; przemówienie. ExampleCommand()" lub "import speech.manager; speech.manager.ExampleCommand()' - zamiast tego użyj 'from speech.commands import ExampleCommand'. (#12126)
* 'speakTextInfo' nie będzie już wysyłać mowy przez 'speakWithoutPauses', jeśli powodem jest 'SAYALL', ponieważ 'SayAllHandler' robi to teraz ręcznie. (#12150)
* Moduł 'synthDriverHandler' nie jest już importowany do 'globalCommands' i 'gui.settingsDialogs' - zamiast tego użyj 'from synthDriverHandler import synthFunctionExample'. (#12172)
* Wartość "ROLE_EQUATION" została usunięta z controlTypes — zamiast tego użyj wartości "ROLE_MATH". (#12164)
* Klasy 'autoSettingsUtils.driverSetting' są usuwane z 'driverHandler' - użyj ich z 'autoSettingsUtils.driverSetting'. (#12168)
* Klasy 'autoSettingsUtils.utils' są usuwane z 'driverHandler' - proszę ich używać z 'autoSettingsUtils.utils'. (#12168)
* Obsługa "TextInfo", które nie dziedziczą po "contentRecog.BaseContentRecogTextInfo" jest usuwana. (#12157)
* 'speech.speakWithoutPauses' został usunięty - zamiast tego użyj 'speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses'. (#12195, #12251)
* Znak "speech.re_last_pause" został usunięty - zamiast niego użyj "speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause". (#12195, #12251)
* 'WelcomeDialog', 'LauncherDialog' i 'AskAllowUsageStatsDialog' są przenoszone do 'gui.startupDialogs'. (#12105)
* Plik 'getDocFilePath' został przeniesiony z 'gui' do modułu 'documentationUtils'. (#12105)
* Moduł gui.accPropServer oraz klasy AccPropertyOverride i ListCtrlAccPropServer z modułu gui.nvdaControls zostały usunięte na rzecz natywnej obsługi WX dla nadpisywania właściwości ułatwień dostępu. Aby zwiększyć dostępność kontrolek WX, zaimplementuj wx. Zamiast tego dostępne. (#12215)
* Pliki w katalogu "source/comInterfaces/" są teraz łatwiej wykorzystywane przez narzędzia programistyczne, takie jak IDE. (#12201)
* Do modułu winVersion dodano wygodne metody i typy służące do pobierania i porównywania wersji systemu Windows. (#11909)
  * Usunięto funkcję isWin10 znajdującą się w module winVersion.
  * klasa winVersion.WinVersion jest porównywalnym i możliwym do uporządkowania typem hermetyzującym informacje o wersji systemu Windows.
  * Funkcja winVersion.getWinVer została dodana w celu uzyskania winVersion.WinVersion reprezentującego aktualnie uruchomiony system operacyjny.
  * Dla znanych wersji systemu Windows dodano stałe wygody, zobacz stałe winVersion.WIN*.
* IAccessibleHandler nie importuje już gwiazdą wszystkiego z interfejsów IAccessible i IA2 COM - użyj ich bezpośrednio. (#12232)
* Obiekty TextInfo mają teraz właściwości początkowe i końcowe, które można matematycznie porównywać z operatorami, takimi jak < <= == != >= >. (#11613)
  * Np. ti1.start <= ti2.end
  * To użycie jest teraz preferowane zamiast ti1.compareEndPoints(ti2,"startToEnd") <= 0
* Właściwości początkowe i końcowe TextInfo mogą być również ustawiane względem siebie. (#11613)
  * Np. ti1.start = ti2.end
  * To użycie jest preferowane zamiast ti1. SetEndPoint(ti2;"startToEnd")
* 'wx. CENTRE_ON_SCREEN" i "wx. CENTER_ON_SCREEN' są usuwane, użyj 'self'. CentreOnScreen()'. (#12309)
* Plik 'easeOfAccess.isSupported' został usunięty, NVDA obsługuje tylko wersje systemu Windows, w których wartość ta ma wartość "True". (#12222)
* Plik "sayAllHandler" został przeniesiony do pliku "speech.sayAll". (#12251)
  * 'speech.sayAll.SayAllHandler' udostępnia funkcje 'stop', 'isRunning', 'readObjects', 'readText', 'lastSayAllMode'.
  * "SayAllHandler.stop" resetuje również instancję "SpeechWithoutPauses" "SayAllHandler".
  * "CURSOR_REVIEW" i "CURSOR_CARET" zostały zastąpione przez "CURSOR. RECENZJA" i "KURSOR. CARET".
* – Mowa. SpeechWithoutPauses" został przeniesiony do "speech.speechWithoutPauses.SpeechWithoutPauses". (#12251)
* Nazwa 'speech.curWordChars' została zmieniona na 'speech._curWordChars'. (#12395)
* następujące elementy zostały usunięte z "speech" i można uzyskać do nich dostęp za pośrednictwem "speech.getState()". Są to teraz wartości tylko do odczytu. (#12395)
  * speechMode (tryb mowy)
  * speechMode_beeps_ms
  * beenCanceled (Anulowano)
  * isPaused (Wstrzymany)
* Aby zaktualizować "speech.speechMode", użyj "speech.setSpeechMode". (#12395)
* Następujące elementy zostały przeniesione do sekcji "Mowa. SpeechMode". (#12395)
  * "speech.speechMode_off" staje się "mową". SpeechMode.off'
  * "speech.speechMode_beeps" staje się "mową". SpeechMode.sygnały dźwiękowe"
  * "speech.speechMode_talk" staje się "mową". SpeechMode.talk"
* "IAccessibleHandler.IAccessibleObjectIdentifierType" to teraz "IAccessibleHandler.types.IAccessibleObjectIdentifierType". (#12367)
* Następujące elementy w pliku "NVDAObjects.UIA.WinConsoleUIA" zostały zmienione (#12094)
  * Nazwa "NVDAObjects.UIA.winConsoleUIA.is21H1Plus" została zmieniona na "NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable".
  * Nazwa 'NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo' została zmieniona tak, aby nazwa klasy zaczynała się wielkimi literami.
  * Nazwa "NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1" została zmieniona na "NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive"
    * Implementacja działa wokół obu punktów końcowych, które są włącznie (w zakresach tekstu) przed [microsoft/terminal PR 4018](https://github.com/microsoft/terminal/pull/4018)
    * Obejścia dla opcji "rozwiń", "zwiń", "porównaj punkty końcowe", "ustaw punkt końcowy" itp

## 2020.4

To wydanie zawiera nowe metody wprowadzania w języku chińskim, aktualizację Liblouis, a lista elementów (NVDA+f7) działa teraz w trybie fokusu.
Pomoc kontekstowa jest teraz dostępna po naciśnięciu F1 w oknach dialogowych NVDA.
Ulepszenia reguł wymowy symboli, słownika mowy, wiadomości w alfabecie Braille'a i czytania poślizgowego.
Poprawki błędów i ulepszenia w programach Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
W sieci wprowadzono ulepszenia w Dokumentach Google i większą obsługę ARIA.
A także wiele innych ważnych poprawek błędów i ulepszeń.

### Nowe funkcje

* Od teraz naciśnięcie klawisza F1 w oknach dialogowych NVDA spowoduje otwarcie pomocy podręcznej dla obecnie podświetlonej sekcji.  (#7757)
* Dodano wsparcie dla technologii Intelli Sense w programach Microsoft SQL Server i Microsoft Visual Studio 2017 i nowszych. (#7504)
* Wymowa symboli: Dodano wsparcie dla grupowania referencji w zasadach zamiany. Powoduje to że zamiany są prostrze i bardziej funkcjonalne. (#11107)
* • Od teraz generowane jest powiadomienie przy próbie utworzenia wpisu słownika zawierającego błędne wyrażenia regularne. (#11407)
  * W szczególności dotyczy to błędów grupowania.
* Dodano wsparcie dla nowej metody wprowadzania języka Chińskiego uproszczonego i tradycyjnego w systemie Windows 10. (#11562)
* Nagłówki zakładek są od teraz traktowane jako pola formularzy podczas szybkiej nawigacji przy pomocy klawisza F. (#10432)
* Dodano polecenie przełączające odczytywanie oznaczonego tekstu. Wymagane jest ręczne przypisanie gestu. (#11807)
* Dodano parametr wiersza poleceń --copy-portable-config pozwalający na przeniesienie konfiguracji przenośnej do konta użytkownika podczas cichej instalacji NVDA. (#9676)
* Klawisz routing jest od teraz wspierany w podglądzie brajla dla użytkowników korzystających z myszy. Aby przenieść kursor do komórki, kliknij myszą w odpowiednie miejsce. (#11804)
* NVDA automatycznie wykrywa urządzenia Humanware Brailliant BI 40X i 20X zarówno przez USB, jak i przez bluetooth. (#11819)

### Zmiany

* Zaktualizowano Liblouis do wersji 3.16.1:
 * Naprawiono krytyczne błędy.
 * Dodano tablicę brajlowską dla baszkirskiego pisma pełnego.
 * Dodano ośmiopunktową tablicę brajlowską dla języka koptyjskiego.
 * Dodano tablice brajlowskie: Rosyjski Literacki i Rosyjski Literacki Szczegółowy.
 * Dodano tablicę brajlowską dla Afrykanerskich skrótów.
 * Usunięto tablicę brajlowską Rosyjski pismo pełne.
* Podczas czytania przy pomocy funkcji "czytaj wszystko" w trybie przeglądania, polecenia "znajdź następny" i "znajdź poprzedni" nie zatrzymują już czytania, gdy funkcja "zezwalaj na czytanie poglądowe" jest włączona. (#11563)
* Dla monitorów brajlowskich Hims F3 od teraz wywoływane jest przez naciśnięcie kombinacji klawiszy spacja +kropki 1, 4, 8. (#11710)
* Ulepszono prezentację opcji "Czas wyświetlania wiadomości brajlowskich" i "Pokazuj wiadomości brajlowskie w nieskończoność". (#11602)
* W przeglądarkach internetowych i innych aplikacjach wspierających tryb przeglądania, możliwe jest teraz wywołanie listy elementów (NVDA+F7) w trybie fokusu. (#10453)
* Zmiany w regionach ARIA nie są odczytywane, jeżeli ogłaszanie dynamicznych zmian treści jest wyłączone. (#9077)
* NVDA od teraz zgłasza status skopiowania przed skopiowanym tekstem. (#6757)
* Ulepszono prezentację widoku graficznego w menedżerze dysków systemu Windows. (#10048)
* Etykiety dla kontrolek są od teraz wyłączone (wyszarzone) kiedy kontrolka jest nieaktywna. (#11809)
* Zaktualizowano bazę danych Emoji CLDR do wersji 38. (#11817)
* Wbudowana funkcja "podświetlanie fokusu" zmieniła nazwę na "podświetlacz wizualny". (#11700)

### Poprawki błędów

* NVDA ponownie działa poprawnie w polach edycyjnych w programie Fast Log Entry. (#8996)
* Od teraz, jeżeli nie możliwe jest uzyskanie całkowitego czasu trwania pliku w programie Foobar 2000, ogłaszany jest teraz czas, który upłynął od rozpoczęcia odtwarzania. (#11337)
* NVDA od teraz wspiera atrybut aria-roledescription w polach edycyjnych na stronach internetowych. (#11607)
* NVDA nie ogłasza już słowa 'lista' dla każdej linii listy w Google Docs lub jakiejkolwiek innej edytowalnej treści w Google Chrome. (#7562)
* Podczas przechodzenia po znakach lub słowach z jednego elementu listy do drugiego, zmiana jest od teraz ogłaszana. (#11569)
* NVDA od teraz odczytuje poprawną linię jeżeli kursor ustawiony jest na końcu linku, który znajduje się na końcu elementu listy w Google Docs lub innych edytowalnych treściach internetowych. (#11606)
* Na Windows 7, otwarcie i zamknięcie menu start z pulpitu ustawia kursor w odpowiednim miejscu. (#10567)
* Kiedy opcja "Próba anulowania mowy dla wygasłych zdarzeń" jest włączona, tytuł karty jest wymawiany podczas przełączania kart w przeglądarce Mozilla firefox. (#11397)
* NVDA od teraz poprawnie odczytuje element listy wybrany poprzez używanie nawigacji literowej podczas korzystania z syntezatora mowy Ivona. (#11651)
* Ponownie możliwe jest korzystanie z trybu przeglądania w programie Poczta Dla Windows 10. 16005.13110 i późniejsze. (#11439)
* Podczas korzystania z głosów Ivona firmy Harpo Software, NVDA ponownie może zapisywać swoje ustawienia, dokonywać zmian syntezatora i uruchamiać się ponownie. (#11650)
* Od teraz możliwe jest wpisanie cyfry 6 w brajlu komputerowym z klawiatury brajlowskiej monitora brajlowskiego Hims. (#11710)
* Znaczne poprawki wydajności w programie Azure Data Studio. (#11533, #11715)
* Kiedy włączona jest opcja "Próba anulowania mowy dla wygasłych zdarzeń" tytuł okna wyszukiwania NVDA jest od teraz oznajmiany. (#11632)
* Naprawiono błąd powodujący zawieszanie się NVDA w sytuacji gdy po wybudzeniu komputera ze stanu uśpienia kursor lądował w dokumencie programu Microsoft Edge. (#11576)
* • Nie jest już wymagane wciśnięcie klawisza tab lub przesunięcie kursora po zamknięciu menu kontekstowego w przeglądarce Microsoft Edge, w celu przywrócenia poprawnego działania trybu przeglądania. (#11202)
* NVDA od teraz poprawnie odczytuje elementy list w 64-bitowych aplikacjach, takich jak Tortoise SVN. (#8175)
* Siatki aria są od teraz renderowane jak zwykłe tabele, zarówno w przeglądarce Google Chrome, jak i Mozilla Firefox. (#9715)
* Od teraz możliwe jest przeszukiwanie wstecz (NVDA+SHIFT+F3). (#11770)
* Skrypty NVDA nie są traktowane jako powtórzone, jeżeli pomiędzy ich gestami wykonany zostanie inny gest. (#11388)
* Tagi Strong i emphasis w przeglądarce Internet Explorer mogą być pominięte przy czytaniu przy wyłączeniu opcji zgłaszaj style w ustawieniach formatowania. (#11808)
* Występujące u niewielkiej liczby użytkowników kilkusekundowe zawieszanie się programu Microsoft Excel podczas nawigacji po komurkach nie powinno już występować. (#11818)
* W aplikacji Microsoft Teams, wersji 1.3.00.28xxx, NVDA ponownie poprawnie odczytuje wiadomości czatów prywatnych i grupowych. (#11821)
* Tekst oznaczony jako błąd gramatyczny i pisowni zarazem w Google Chrome, jest od teraz poprawnie ogłaszany przez NVDA. (#11787)
* Podczas korzystania z programu Microsoft Outlook w języku francuskim, skrót CTRL+SHIFT+R ponownie działa. (#11196)
* W programie Microsoft Visual Studio, dymki podpowiedzi funkcji Intellisense są wypowiadane tylko raz. (#11611)
* W kalkulatorze systemu Windows 10, NVDA nie ogłasza już postępu obliczeń gdy czytanie wpisywanych znaków jest wyłączone. (#9428)
* Przy wyświetlaniu adresów URL z NVDA ustawionym na tablicę brajlowską Angielski US skróty i włączoną opcją rozwiń słowo pod kursorem do brajla komputerowego, NVDA się już nie wysypuje. (#11754)
* Ponownie możliwe jest raportowanie informacji o formatowaniu dla aktywnej komórki programu Excel przy użyciu NVDA+F. (#11914)
* Wejście QWERTY na monitorach brajlowskich Papenmeier, które go obsługują, ponownie działa i nie powoduje już losowego zawieszania się NVDA. (#11944)
* W przeglądarkach opartych na Chromium rozwiązano kilka przypadków, w których nawigacja po tabelach nie działała, a NVDA nie zgłaszała liczby wierszy/kolumn tabeli. (#12359)

### Zmiany dla deweloperów

* Testy systemowe mogą teraz wysyłać klucze za pomocą spy.emulateKeyPress, który pobiera identyfikator klucza zgodny z własnymi nazwami kluczy NVDA i domyślnie blokuje również do momentu wykonania akcji. (#11581)
* NVDA nie wymaga już, aby bieżący katalog był katalogiem aplikacji NVDA, aby mógł działać. (#6491)
* Ustawienie grzeczności aria live dla aktywnych regionów można teraz znaleźć w obiektach NVDA za pomocą właściwości liveRegionPoliteness. (#11596)
* Teraz możliwe jest zdefiniowanie oddzielnych gestów dla dokumentu Outlook i Word. (#11196)

## 2020.3

To wydanie zawiera kilka dużych ulepszeń stabilności i wydajności, szczególnie w aplikacjach pakietu Microsoft Office. Dostępne są nowe ustawienia przełączania obsługi ekranu dotykowego i raportowania grafiki.
Istnienie oznaczonych (podświetlonych) treści można zgłaszać w przeglądarkach, a także pojawiły się nowe niemieckie tablice brajlowskie.

### Nowe funkcje

* Możesz teraz przełączać raportowanie grafiki z ustawień formatowania dokumentu NVDA. Zauważ, że wyłączenie tej opcji nadal będzie skutkowało odczytaniem alternatywnych tekstów grafik. (#4837)
* Możesz teraz przełączać obsługę ekranu dotykowego NVDA. Do panelu Interakcja dotykowa została dodana opcja ustawień NVDA. Domyślnym gestem jest NVDA+control+alt+t. (#9682)
* Dodano nowe niemieckie tabele brajlowskie. (#11268)
* NVDA wykrywa teraz tekstowe kontrolki UIA tylko do odczytu. (#10494)
* Istnienie oznaczonych (wyróżnionych) treści jest zgłaszane zarówno w mowie, jak i w alfabecie Braille'a we wszystkich przeglądarkach internetowych. (#11436)
 * Można to włączać i wyłączać za pomocą nowej opcji formatowania dokumentów NVDA do podświetlania.
* Nowe emulowane klawiatury systemowej mogą być dodawane z okna dialogowego Gesty wejściowe NVDA. (#6060)
  * Aby to zrobić, naciśnij przycisk dodawania po wybraniu kategorii Emulowane klawiatury systemowej.
* Obsługiwany jest teraz Handy Tech Active Braille z joystickiem. (#11655)
* Ustawienie "Tryb automatycznego ustawiania ostrości dla ruchu karetka" jest teraz kompatybilne z wyłączeniem opcji "Automatycznie ustaw ostrość na elementy, na których można ustawić ostrość". (#11663)

### Zmiany

* Skrypt formatowania raportu (NVDA+f) został teraz zmieniony tak, aby raportował formatowanie na daszku systemowym, a nie w pozycji kursora recenzji. Aby zgłosić formatowanie w pozycji kursora recenzji, teraz użyj NVDA+shift+f. (#9505)
* NVDA nie ustawia już automatycznie fokusu systemu na elementy, na których można ustawić ostrość w trybie przeglądania, co poprawia wydajność i stabilność. (#11190)
* CLDR zaktualizowano z wersji 36.1 do wersji 37. (#11303)
* Zaktualizowano eSpeak-NG do wersji 1.51-dev, commit 1fb68ffffea4
* Teraz można korzystać z nawigacji w tabelach w polach list z elementami listy do sprawdzenia, gdy dana lista ma wiele kolumn. (#8857)
* W menedżerze dodatków, po wyświetleniu monitu o potwierdzenie usunięcia dodatku, opcja "Nie" jest teraz domyślna. (#10015)
* W programie Microsoft Excel okno dialogowe Lista elementów przedstawia teraz formuły w ich zlokalizowanej formie. (#9144)
* NVDA podaje teraz poprawną terminologię dla notatek w MS Excel. (#11311)
* Podczas korzystania z polecenia "przesuń kursor recenzji do fokusu" w trybie przeglądania, kursor recenzji jest teraz ustawiony w pozycji wirtualnego karetki. (#9622)
* Informacje zgłaszane w trybie przeglądania, takie jak informacje o formatowaniu za pomocą NVDA+F, są teraz wyświetlane w nieco większym oknie wyśrodkowanym na ekranie. (#9910)

### Poprawki błędów

* NVDA teraz zawsze mówi, gdy nawigujesz za pomocą słowa i lądujesz na dowolnym pojedynczym symbolu, po którym następuje biała spacja, niezależnie od ustawień szczegółowości. (#5133)
* W aplikacjach korzystających z QT 5.11 lub nowszej opisy obiektów są ponownie raportowane. (#8604)
* Podczas usuwania słowa za pomocą control+delete, NVDA nie pozostaje już cicha. (#3298, #11029)
  * Teraz ogłaszane jest słowo po prawej stronie usuniętego słowa.
* W panelu ustawień ogólnych lista języków jest teraz posortowana poprawnie. (#10348)
* W oknie dialogowym Gesty wejściowe znacznie poprawiono wydajność podczas filtrowania. (#10307)
* Możesz teraz wysyłać znaki Unicode poza U+FFFF z monitora brajlowskiego. (#10796)
* NVDA ogłosi zawartość okna dialogowego Otwórz za pomocą w aktualizacji systemu Windows 10 z maja 2020 r. (#11335)
* Nowa opcja eksperymentalna w ustawieniach zaawansowanych (Włącz selektywną rejestrację dla zdarzeń automatyzacji interfejsu użytkownika i zmian właściwości) może zapewnić znaczną poprawę wydajności w programie Microsoft Visual Studio i innych aplikacjach opartych na UIAutomation, jeśli są włączone. (#11077, #11209)
* W przypadku elementów listy do sprawdzenia wybrany stan nie jest już anonsowany nadmiarowo, a jeśli ma to zastosowanie, zamiast tego jest ogłaszany stan niezaznaczony. (#8554)
* W aktualizacji systemu Windows 10 z maja 2020 r. NVDA wyświetla teraz Microsoft Sound Mapper podczas przeglądania urządzeń wyjściowych z okna dialogowego syntezatora. (#11349)
* W programie Internet Explorer numery są teraz poprawnie anonsowane dla list uporządkowanych, jeśli lista nie zaczyna się od 1. (#8438)
* W Google Chrome NVDA będzie teraz zgłaszać, że nie jest zaznaczone dla wszystkich możliwych do zaznaczenia elementów sterujących (nie tylko pól wyboru), które nie są obecnie zaznaczone. (#11377)
* Po raz kolejny możliwe jest poruszanie się po różnych kontrolkach, gdy język NVDA jest ustawiony na aragoński. (#11384)
* NVDA nie powinien już czasami zawieszać się w Microsoft Word podczas szybkiego przechodzenia w górę i w dół lub wpisywania znaków z włączonym alfabetem Braille'a. (#11431, #11425, #11414)
* NVDA nie dodaje już nieistniejącej spacji końcowej podczas kopiowania bieżącego obiektu nawigatora do schowka. (#11438)
* NVDA nie aktywuje już profilu Powiedz wszystko, jeśli nie ma nic do odczytania. (#10899, #9947)
* NVDA nie jest już w stanie odczytać listy funkcji w Menedżerze Internetowych usług informacyjnych (IIS). (#11468)
* NVDA utrzymuje teraz urządzenie audio w pozycji otwartej, poprawiając wydajność na niektórych kartach dźwiękowych (#5172, #10721)
* NVDA nie będzie się już zawieszać ani zamykać po przytrzymaniu Control+Shift+strzałka w dół w programie Microsoft Word. (#9463)
* Stan rozwinięty/zwinięty katalogów w widoku drzewa nawigacji na drive.google.com jest teraz zawsze raportowany przez NVDA. (#11520)
* NVDA automatycznie wykryje monitor brajlowski NLS eReader Humanware przez Bluetooth, ponieważ jego nazwa Bluetooth to teraz "NLS eReader Humanware". (#11561)
* Znaczne ulepszenia wydajności w Visual Studio Code. (#11533)

### Zmiany dla deweloperów

* Pomocnik GUI BoxSizerHelper.addDialogDismissButtons obsługuje nowy argument słowa kluczowego "oddzielony", służący do dodawania standardowego separatora poziomego do okien dialogowych (innych niż komunikaty i okna dialogowe z pojedynczym wejściem). (#6468)
* Do modułów aplikacji dodano dodatkowe właściwości, w tym ścieżkę do pliku wykonywalnego (appPath), aplikację ze Sklepu Windows (isWindowsStoreApp) i architekturę komputera dla aplikacji (appArchitecture). (#7894)
* Teraz można tworzyć moduły aplikacji dla aplikacji hostowanych w systemie wwahost.exe w systemie Windows 8 i nowszych. (#4569)
* Fragment dziennika może być teraz rozdzielony, a następnie skopiowany do schowka za pomocą NVDA+control+shift+F1. (#9280)
* Obiekty specyficzne dla NVDA, które są znajdowane przez cykliczny garbage collector Pythona, są teraz rejestrowane podczas usuwania przez kolektor, aby pomóc w usuwaniu cykli referencyjnych z NVDA. (#11499)
 * Większość klas NVDA jest śledzona, w tym NVDAObjects, appModules, GlobalPlugins, SynthDrivers i TreeInterceptors.
 * Klasa, która musi być śledzona, powinna dziedziczyć z garbageHandler.TrackedObject.
* Znaczące rejestrowanie debugowania dla zdarzeń MSAA można teraz włączyć w ustawieniach zaawansowanych NVDA. (#11521)
* Zdarzenia winEvents MSAA dla aktualnie uaktywnionego obiektu nie są już odfiltrowywane wraz z innymi zdarzeniami, jeśli liczba zdarzeń dla danego wątku zostanie przekroczona. (#11520)

## 2020.2

Najważniejsze cechy tego wydania to obsługa nowego monitora brajlowskiego firmy Nattiq, lepsza obsługa graficznego interfejsu użytkownika programu antywirusowego ESET i terminala Windows, ulepszenia wydajności w 1Password oraz syntezator Windows OneCore. A także wiele innych ważnych poprawek błędów i ulepszeń.

### Nowe funkcje

* Obsługa nowych monitorów brajlowskich:
  * Nattiq nBraille (#10778)
* Dodano skrypt otwierający katalog konfiguracyjny NVDA (brak domyślnego gestu). (#2214)
* Lepsza obsługa graficznego interfejsu użytkownika programu antywirusowego ESET. (#10894)
* Dodano obsługę terminala Windows. (#10305)
* Dodano polecenie zgłaszania aktywnego profilu konfiguracji (bez domyślnego gestu). (#9325)
* Dodano polecenie do przełączania raportowania indeksów dolnych i górnych (brak domyślnego gestu). (#10985)
* Aplikacje internetowe (np. Gmail) nie odczytują już nieaktualnych informacji podczas szybkiego przełączania ostrości. (#10885)
  * Tę eksperymentalną poprawkę należy włączyć ręcznie za pomocą opcji "Próba anulowania mowy w przypadku wygasłych zdarzeń fokusu" w panelu ustawień zaawansowanych.
* Do słownika symboli domyślnych dodano o wiele więcej symboli. (#11105)

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis z wersji 3.12 do [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (#10832, #11221)
* Raportowanie indeksów górnych i dolnych jest teraz kontrolowane oddzielnie od raportowania atrybutów czcionek. (#10919)
* Ze względu na zmiany wprowadzone w VS Code, NVDA nie wyłącza już domyślnie trybu przeglądania w Kodzie. (#10888)
* NVDA nie raportuje już komunikatów "góra" i "dół" podczas przesuwania kursora recenzji bezpośrednio do pierwszej lub ostatniej linii bieżącego obiektu nawigatora za pomocą skryptów kursora przeglądu przejścia na górę i przejścia na dół. (#9551)
* NVDA nie raportuje już komunikatów "w lewo" i "w prawo" podczas bezpośredniego przesuwania kursora recenzji do pierwszego lub ostatniego znaku wiersza dla bieżącego obiektu nawigatora z odpowiednio skryptami kursora przeglądu przejścia na początek wiersza i przejścia na koniec wiersza. (#9551)

### Poprawki błędów

* NVDA uruchamia się teraz poprawnie, gdy nie można utworzyć pliku dziennika. (#6330)
* W ostatnich wydaniach Microsoft Word 365, NVDA nie będzie już informować o "usuń wstecz słowo" po naciśnięciu Control+Backspace podczas edycji dokumentu. (#10851)
* W Winampie, NVDA po raz kolejny ogłosi stan przełączania odtwarzania losowego i powtarzania. (#10945)
* NVDA nie jest już ekstremalnie powolny podczas poruszania się po liście elementów w 1Password. (#10508)
* Syntezator mowy Windows OneCore nie pozostaje już w tyle między wypowiedziami. (#10721)
* NVDA nie zawiesza się już po otwarciu menu kontekstowego 1Password w obszarze powiadomień systemowych. (#11017)
* W pakiecie Office 2013 i starszych:
  * Wstążki są ogłaszane, gdy fokus zostanie na nie przeniesiony po raz pierwszy. (#4207)
  * Elementy menu kontekstowego są ponownie poprawnie raportowane. (#9252)
  * Sekcje wstążki są konsekwentnie ogłaszane podczas nawigowania za pomocą Control+strzałki. (#7067)
* W trybie przeglądania w przeglądarkach Mozilla Firefox i Google Chrome tekst nie jest już nieprawidłowo wyświetlany w osobnym wierszu, gdy zawartość internetowa korzysta z wyświetlania CSS: inline-flex. (#11075)
* W trybie przeglądania z wyłączoną opcją Automatycznie ustaw fokus systemu na elementy, na których można ustawić fokus, można teraz aktywować elementy, na których nie można ustawić fokusu.
* W trybie przeglądania z wyłączoną opcją Automatycznie ustaw fokus systemu na elementy, na których można ustawić fokus, można teraz aktywować elementy, do których można dotrzeć, naciskając Tab. (#8528)
* W trybie przeglądania, gdy opcja Automatycznie ustaw fokus systemu na elementy, na których można ustawić fokus, aktywacja niektórych elementów nie jest już klikana w niewłaściwym miejscu. (#9886)
* Dźwięki błędów NVDA nie są już słyszalne podczas uzyskiwania dostępu do kontrolek tekstowych DevExpress. (#10918)
* Podpowiedzi ikon w zasobniku systemowym nie są już raportowane podczas nawigacji za pomocą klawiatury, jeśli ich tekst jest równy nazwie ikon, aby uniknąć podwójnego ogłaszania. (#6656)
* W trybie przeglądania z wyłączoną opcją "Automatycznie ustaw fokus systemu na elementy z możliwością ustawiania ostrości", przełączenie do trybu ostrości z NVDA+spacja teraz skupia element pod karetką. (#11206)
* Po raz kolejny możliwe jest sprawdzenie dostępności aktualizacji NVDA w niektórych systemach; np. czyste instalacje systemu Windows. (#11253)
* Fokus nie jest przenoszony w aplikacji Java, gdy zaznaczenie jest zmieniane w nieuaktywnionym drzewie, tabeli lub liście. (#5989)

### Zmiany dla deweloperów

* execElevated i hasUiAccess zostały przeniesione z modułu konfiguracyjnego do modułu systemUtils. Użycie za pośrednictwem modułu konfiguracyjnego jest przestarzałe. (#10493)
* Zaktualizowano configobj do wersji 5.1.0dev commit f9a265c4. (#10939)
* Automatyczne testowanie NVDA z Chrome i próbką HTML jest teraz możliwe. (#10553)
* IAccessibleHandler został przekonwertowany na pakiet, OrderedWinEventLimiter został wyodrębniony do modułu i dodano testy jednostkowe (#10934)
* Zaktualizowano BrlApi do wersji 0.8 (BRLTTY 6.1). (#11065)
* Pobieranie paska stanu można teraz dostosować za pomocą modułu AppModule. (#2125, #4640)
* NVDA nie nasłuchuje już IAccessible EVENT_OBJECT_REORDER. (#11076)
* Uszkodzony obiekt ScriptableObject (taki jak GlobalPlugin, w którym brakuje wywołania metody init swojej klasy bazowej) nie przerywa już obsługi skryptów NVDA. (#5446)

## 2020.1

Najważniejsze cechy tego wydania obejmują obsługę kilku nowych monitorów brajlowskich od HumanWare i APH, a także wiele innych ważnych poprawek błędów, takich jak możliwość ponownego czytania matematyki w programie Microsoft Word za pomocą MathPlayer / MathType.

### Nowe funkcje

* Aktualnie zaznaczony element w listboxach jest ponownie prezentowany w trybie przeglądania w Chrome, podobnie jak w NVDA 2019.1. (#10713)
* Możesz teraz wykonywać kliknięcia prawym przyciskiem myszy na urządzeniach dotykowych, dotykając i przytrzymując jednym palcem. (#3886)
* Obsługa nowych monitorów brajlowskich: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2 i NLS eReader. (#10830)

### Zmiany

* NVDA zapobiegnie blokowaniu się systemu lub przechodzeniu w stan uśpienia, gdy jest w środku, powiedzmy wszystkim. (#10643)
* Obsługa pozaprocesowych ramek iframe w przeglądarce Mozilla Firefox. (#10707)
* Zaktualizowano tłumacz brajlowski liblouis do wersji 3.12. (#10161)

### Poprawki błędów

* Naprawiono NVDA, który nie ogłaszał symbolu minus Unicode (U+2212). (#10633)
* Podczas instalowania dodatku z menedżera dodatków nazwy plików i folderów w oknie przeglądania nie są już raportowane dwukrotnie. (#10620, #2395)
* W Firefoksie, podczas ładowania Mastodona z włączonym zaawansowanym interfejsem internetowym, wszystkie osie czasu renderują się teraz poprawnie w trybie przeglądania. (#10776)
* W trybie przeglądania, NVDA zgłasza teraz "niezaznaczone" dla niezaznaczonych pól wyboru, w których czasami nie występowało wcześniej. (#10781)
* Elementy sterujące przełącznikiem ARIA nie wyświetlają już mylących informacji, takich jak "nie wciśnięto zaznaczone" lub "naciśnięto zaznaczone". (#9187)
* Głosy SAPI4 nie powinny już odmawiać wypowiadania określonego tekstu. (#10792)
* NVDA może ponownie odczytywać i wchodzić w interakcje z równaniami matematycznymi w programie Microsoft Word. (#10803)
* NVDA ponownie ogłosi odznaczenie tekstu w trybie przeglądania, jeśli naciśniesz strzałki, gdy tekst jest zaznaczony. (#10731).
* NVDA nie kończy się już, jeśli wystąpi błąd inicjalizacji eSpeak. (#10607)
* Błędy spowodowane przez Unicode w tłumaczeniach skrótów nie zatrzymują już instalatora, łagodzone przez powrót do tekstu w języku angielskim. (#5166, #6326)
* Strzałka w kierunku wyjścia i odejścia od list i tabel w sayAll z włączonym odczytem skimingowym nie informuje już w sposób ciągły o wyjściu z listy lub tabeli. (#10706)
* Napraw śledzenie myszy dla niektórych elementów MSHTML w programie Internet Explorer. (#10736)

### Zmiany dla deweloperów

* Dokumentacja programisty jest teraz tworzona przy użyciu sphinxa. (#9840)
* Kilka funkcji mowy zostało podzielonych na dwie części. (#10593)
  Wersja speakX pozostaje, ale teraz zależy od funkcji getXSpeech, która zwraca sekwencję mowy.
  * Funkcja speakObjectProperties korzysta teraz z funkcji getObjectPropertiesSpeech
  * speakObject opiera się teraz na getObjectSpeech
  * speakTextInfo opiera się teraz na getTextInfoSpeech
  * speakWithoutPauses został przekonwertowany na klasę i refaktoryzowany, ale nie powinien naruszyć zgodności.
  * getSpeechForSpelling jest przestarzały (choć nadal dostępny), zamiast tego użyj getSpellingSpeech.
  Prywatne zmiany, które nie powinny mieć wpływu na twórców dodatków:
  * _speakPlaceholderIfEmpty jest teraz _getPlaceholderSpeechIfTextEmpty
  * _speakTextInfo_addMath jest teraz _extendSpeechSequence_addMathForTextInfo
* Mowa "powód" został przekonwertowany na wyliczenie, zobacz controlTypes.OutputReason klasę. (#10703)
  * Stałe "REASON_*" na poziomie modułu są przestarzałe.
* Kompilowanie zależności NVDA wymaga teraz programu Visual Studio 2019 (16.2 lub nowszego). (#10169)
* Zaktualizowano SCons do wersji 3.1.1. (#10169)
* Ponownie zezwalaj behaviors._FakeTableCell na brak zdefiniowanej lokalizacji (#10864)

## 2019.3

NVDA 2019.3 to bardzo ważne wydanie zawierające wiele ukrytych zmian, w tym aktualizację Pythona 2 do Pythona 3 i poważne przepisanie podsystemu mowy NVDA.
Chociaż te zmiany zrywają kompatybilność ze starszymi dodatkami NVDA, aktualizacja do Pythona 3 jest konieczna ze względów bezpieczeństwa, a zmiany w mowie pozwalają na kilka ekscytujących innowacji w najbliższej przyszłości.
 Inne nowości w tym wydaniu to 64-bitowa obsługa maszyn wirtualnych Java, funkcja Screen Curtain i Focus Highlight, obsługa większej liczby monitorów brajlowskich i nowa przeglądarka Braille'a oraz wiele innych poprawek błędów.

### Nowe funkcje

* Poprawiono dokładność polecenia przenieś mysz do obiektu nawigatora w polach tekstowych w aplikacjach Java. (#10157)
* Dodano obsługę następujących monitorów brajlowskich Handy Tech (#8955):
 * Podstawowy alfabet Braille'a Plus 40
 * Podstawowy alfabet Braille'a Plus 32
 * Podłącz alfabet Braille'a
* Wszystkie gesty zdefiniowane przez użytkownika można teraz usunąć za pomocą nowego przycisku "Przywróć ustawienia fabryczne" w oknie dialogowym Gesty wprowadzania. (#10293)
* Raportowanie czcionek w programie Microsoft Word obejmuje teraz informacje o tym, czy tekst jest oznaczony jako ukryty. (#8713)
* Dodano polecenie przesunięcia kursora przeglądania do pozycji poprzednio ustawionej jako znacznik początkowy dla zaznaczenia lub kopiowania: NVDA+shift+F9. (#1969)
* W przeglądarkach Internet Explorer, Microsoft Edge oraz najnowszych wersjach przeglądarek Firefox i Chrome punkty orientacyjne są teraz raportowane w trybie koncentracji uwagi i nawigacji po obiektach. (#10101)
* W przeglądarkach Internet Explorer, Google Chrome i Mozilla Firefox można teraz nawigować według artykułów i grupować za pomocą skryptów szybkiej nawigacji. Skrypty te są domyślnie niepowiązane i można je przypisać w oknie dialogowym Gesty wprowadzania, gdy okno dialogowe jest otwierane z dokumentu w trybie przeglądania. (#9485, #9227)
 * Podano również dane liczbowe. Są one traktowane jako obiekty i dlatego można się po nich poruszać za pomocą szybkiej nawigacji.
* W przeglądarkach Internet Explorer, Google Chrome i Mozilla Firefox elementy artykułów są teraz raportowane podczas nawigacji po obiektach i opcjonalnie w trybie przeglądania, jeśli jest włączony w ustawieniach formatowania dokumentu. (#10424)
* Dodano kurtynę ekranu, która po włączeniu sprawia, że cały ekran jest w systemie Windows 8 i nowszych. (#7857)
 * Dodano skrypt włączający kurtynę ekranu (do następnego restartu za pomocą jednego naciśnięcia, lub zawsze, gdy NVDA jest uruchomiona za pomocą dwóch naciśnięć), nie jest przypisany żaden domyślny gest.
 * Może być włączony i skonfigurowany za pomocą kategorii "wizja" w oknie ustawień NVDA.
* Dodano funkcję podświetlania ekranu do NVDA. (#971, #9064)
 * Podświetlanie fokusu, obiektu nawigatora i pozycji karetki trybu przeglądania można włączyć i skonfigurować za pomocą kategorii "wizja" w oknie ustawień NVDA.
 * Uwaga: Ta funkcja jest niekompatybilna z dodatkiem Focus Highlight, jednak dodatek może być nadal używany, gdy wbudowany zakreślacz jest wyłączony.
* Dodano narzędzie Braille Viewer, które umożliwia przeglądanie danych brajlowskich za pomocą okna ekranowego. (#7788)

### Zmiany

* Podręcznik użytkownika opisuje teraz, jak korzystać z NVDA w konsoli systemu Windows. (#9957)
* Uruchomienie nvda.exe teraz domyślnie zastępuje już uruchomioną kopię NVDA. Parametr wiersza polecenia -r|--replace jest nadal akceptowany, ale ignorowany. (#8320)
* W systemie Windows 8 i nowszych NVDA będzie teraz raportować nazwę produktu i informacje o wersji dla hostowanych aplikacji, takich jak aplikacje pobrane ze sklepu Microsoft Store, korzystając z informacji dostarczonych przez aplikację. (#4259, #10108)
* Podczas włączania i wyłączania zmian ścieżki za pomocą klawiatury w programie Microsoft Word, NVDA ogłosi stan ustawienia. (#942)
* Numer wersji NVDA jest teraz rejestrowany jako pierwsza wiadomość w dzienniku. Dzieje się tak nawet wtedy, gdy rejestrowanie zostało wyłączone z poziomu graficznego interfejsu użytkownika. (#9803)
* Okno dialogowe ustawień nie pozwala już na zmianę skonfigurowanego poziomu dziennika, jeśli został on zastąpiony z wiersza poleceń. (#10209)
* W programie Microsoft Word NVDA ogłasza teraz stan wyświetlania znaków niedrukowalnych po naciśnięciu skrótu przełączającego Ctrl+Shift+8 . (#10241)
* Zaktualizowano tłumacza brajlowskiego Liblouis, aby zawierał wpis 58d67e63. (#10094)
* Gdy włączone jest raportowanie znaków CLDR (w tym emotikonów), są one ogłaszane na wszystkich poziomach interpunkcji. (#8826)
* Pakiety Pythona innych firm zawarte w NVDA, takie jak comtypes, teraz rejestrują swoje ostrzeżenia i błędy w dzienniku NVDA. (#10393)
* Zaktualizowano adnotacje emoji Unicode Common Locale Data Repository do wersji 36.0. (#10426)
* Podczas ustawiania fokusu grupy w trybie przeglądania opis jest teraz również odczytywany. (#10095)
* Mostek Java Access Bridge jest teraz dołączony do NVDA, aby umożliwić dostęp do aplikacji Java, w tym dla 64-bitowych maszyn wirtualnych Java. (#7724)
* Jeśli program Java Access Bridge nie jest włączony dla użytkownika, NVDA automatycznie włącza go podczas uruchamiania NVDA. (#7952)
* Zaktualizowano eSpeak-NG do wersji 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Poprawki błędów

* Emotikony i inne 32-bitowe znaki Unicode zajmują teraz mniej miejsca na monitorze brajlowskim, gdy są wyświetlane jako wartości szesnastkowe. (#6695)
* W systemie Windows 10 NVDA będzie ogłaszać podpowiedzi z aplikacji uniwersalnych, jeśli NVDA jest skonfigurowana do raportowania podpowiedzi w oknie dialogowym prezentacji obiektów. (#8118)
* W rocznicowej aktualizacji systemu Windows 10 i nowszych wpisany tekst jest teraz zgłaszany w Mintty. (#1348)
* W przypadku rocznicowej aktualizacji systemu Windows 10 i nowszych dane wyjściowe w konsoli systemu Windows, które pojawiają się w pobliżu karety, nie są już przeliterowane. (#513)
* Elementy sterujące w oknie dialogowym kompresora Audacitys są teraz odczytywane podczas poruszania się po oknie dialogowym. (#10103)
* NVDA nie traktuje już spacji jako słów w przeglądzie obiektów w edytorach opartych na Scintilla, takich jak Notepad++. (#8295)
* NVDA zapobiegnie przejściu systemu w tryb uśpienia podczas przewijania tekstu za pomocą gestów monitora brajlowskiego. (#9175)
* W systemie Windows 10 pismo Braille'a będzie teraz podążać za edycją zawartości komórek w programie Microsoft Excel i w innych kontrolkach tekstowych UIA, w których pozostawało w tyle. (#9749)
* NVDA po raz kolejny zgłosi sugestie w pasku adresu Microsoft Edge. (#7554)
* NVDA nie jest już cichy podczas skupiania nagłówka kontrolki karty HTML w Internet Explorerze. (#8898)
* W przeglądarce Microsoft Edge opartej na EdgeHTML, NVDA nie będzie już odtwarzać dźwięku sugestii wyszukiwania, gdy okno zostanie zmaksymalizowane. (#9110, #10002)
* Pola kombi ARIA 1.1 są teraz obsługiwane w przeglądarkach Mozilla Firefox i Google Chrome. (#9616)
* NVDA nie będzie już raportować zawartości wizualnie ukrytych kolumn dla elementów listy w kontrolkach SysListView32. (#8268)
* W oknie dialogowym ustawień nie jest już wyświetlane "info" jako bieżący poziom dziennika w trybie bezpiecznym. (#10209)
* W menu Start dla rocznicowej aktualizacji systemu Windows 10 i nowszych NVDA ogłosi szczegóły wyników wyszukiwania. (#10340)
* W trybie przeglądania, jeśli przesunięcie kursora lub użycie szybkiej nawigacji spowoduje zmianę dokumentu, NVDA nie będzie już w niektórych przypadkach odczytywać nieprawidłowej treści. (#8831, #10343)
* Poprawiono niektóre nazwy punktorów w programie Microsoft Word. (#10399)
* W aktualizacji systemu Windows 10 z maja 2019 r. i nowszych NVDA po raz kolejny ogłosi pierwszy wybrany emoji lub element schowka, gdy otworzy się odpowiednio panel emoji i historia schowka. (#9204)
* W Poedit po raz kolejny można zobaczyć niektóre tłumaczenia dla języków pisanych od prawej do lewej. (#9931)
* W aplikacji Ustawienia w aktualizacji systemu Windows 10 z kwietnia 2018 r. i nowszych, NVDA nie będzie już ogłaszać informacji o pasku postępu dla mierników głośności znajdujących się na stronie System/Dźwięk. (#10412)
* Niepoprawne wyrażenia regularne w słownikach mowy nie powodują już całkowitego uszkodzenia mowy w NVDA. (#10334)
* Podczas odczytywania elementów punktowanych w programie Microsoft Word z włączoną funkcją UIA punktor z następnego elementu listy nie jest już nieprawidłowo ogłaszany. (#9613)
* Rozwiązano kilka rzadkich problemów z tłumaczeniem brajlowskim i błędów związanych z liblouis. (#9982)
* Aplikacje Java uruchomione przed NVDA są teraz dostępne bez konieczności ponownego uruchamiania aplikacji Java. (#10296)
* W przeglądarce Mozilla Firefox, gdy element fokusu zostanie oznaczony jako bieżący (aria-current), ta zmiana nie będzie już wypowiadana wiele razy. (#8960)
* NVDA będzie teraz traktować niektóre złożone znaki Unicode, takie jak e-sharp, jako pojedynczy znak podczas poruszania się po tekście. (#10550)
* Pakiet narzędzi Spring Tool Suite w wersji 4 jest teraz obsługiwany. (#10001)
* Nie wymawiaj dwukrotnie imienia, gdy celem relacji jest aria nazwana przez cel relacji. (#10552)
* W systemie Windows 10 w wersji 1607 lub nowszej znaki wpisywane z klawiatur brajlowskich są wypowiadane w większej liczbie sytuacji. (#10569)
* Podczas zmiany urządzenia wyjściowego audio, dźwięki odtwarzane przez NVDA będą teraz odtwarzane przez nowo wybrane urządzenie. (#2167)
* W przeglądarce Mozilla Firefox przesuwanie fokusu w trybie przeglądania jest szybsze. Dzięki temu przesuwanie kursora w trybie przeglądania w wielu przypadkach jest bardziej responsywne. (#10584)

### Zmiany dla deweloperów

* Zaktualizowano język Python do wersji 3.7. (#7105)
* Zaktualizowano pySerial do wersji 3.4. (#8815)
* Zaktualizowano wxPython do wersji 4.0.3, aby obsługiwała język Python 3.5 i nowsze. (#9630)
* Zaktualizowano sześć do wersji 1.12.0. (#9630)
* Zaktualizowano py2exe do wersji 0.9.3.2 (w trakcie opracowywania, commit b372a8e z albertosottile/py2exe#13). (#9856)
* Zaktualizowano moduł UIAutomationCore.dll comtypes do wersji 10.0.18362. (#9829)
* Uzupełnianie tabulatora w konsoli języka Python sugeruje atrybuty rozpoczynające się od podkreślenia tylko wtedy, gdy podkreślenie jest wpisane po raz pierwszy. (#9918)
* Narzędzie do lintingu Flake8 zostało zintegrowane z SCons odzwierciedlając wymagania kodu dla Pull Requestów. (#5918)
* Ponieważ NVDA nie jest już zależna od pyWin32, moduły takie jak win32api i win32con nie są już dostępne dla dodatków. (#9639)
 * Wywołania Win32API można zastąpić bezpośrednimi wywołaniami funkcji DLL Win32 za pośrednictwem ctypes.
 * Stałe win32con powinny być zdefiniowane w twoich plikach.
* Nazwa argumentu "async" w pliku nvwave.playWaveFile została zmieniona na "asynchroniczny". (#8607)
* Metody speakText i speakCharacter w obiektach synthDriver nie są już obsługiwane.
 * Ta funkcja jest obsługiwana przez SynthDriver.speak.
* Klasy SynthSetting w synthDriverHandler zostały usunięte. Teraz zamiast tego użyj klas driverHandler.DriverSetting.
* Klasy SynthDriver nie powinny już uwidaczniać indeksu za pośrednictwem właściwości lastIndex.
 * Zamiast tego powinni powiadomić akcję synthDriverHandler.synthIndexReached o indeksie, gdy wszystkie poprzednie dźwięki zakończą odtwarzanie przed tym indeksem.
* Klasy SynthDriver muszą teraz powiadamiać akcję synthDriverHandler.synthDoneSpeaking po zakończeniu odtwarzania całego dźwięku z wywołania SynthDriver.speak.
* Klasy SynthDriver muszą obsługiwać mowę. PitchCommand w ich metodzie mówienia, ponieważ zmiany wysokości dźwięku dla pisowni mówienia zależą teraz od tej funkcjonalności.
* Nazwa funkcji mowy getSpeechTextForProperties została zmieniona na getPropertiesSpeech. (#10098)
* Nazwa funkcji brajlowskiej getBrailleTextForProperties została zmieniona na getPropertiesBraille. (#10469)
* Kilka funkcji mowy zostało zmienionych w celu zwrócenia sekwencji mowy. (#10098)
 * getControlFieldSpeech (Mowa w Polu)
 * getFormatFieldSpeech (Mowa w polie)
 * getSpeechTextForProperties nazywa się teraz getPropertiesSpeech
 * getIndentationSpeech (Mowa wcięcia)
 * getTableInfoSpeech
* Dodano moduł textUtils, aby uprościć różnice między ciągami Pythona 3 a ciągami Unicode systemu Windows. (#9545)
 * Zapoznaj się z dokumentacją modułu i modułem textInfos.offsets, aby zapoznać się z przykładowymi implementacjami.
* Usunięto przestarzałe funkcje. (#9548)
 * Usunięto AppModules:
  * Rejestrator dźwięku w systemie Windows XP.
  * Klango Player, który jest porzuconym oprogramowaniem.
 * Usunięto opakowanie configobj.validate.
  * Nowy kod powinien używać from configobj import validate zamiast import validate
 * textInfos.Point i textInfos.Rect zastąpione odpowiednio przez locationHelper.Point i locationHelper.RectLTRB.
 * Braille'a. BrailleHandler._get_tether i alfabet Braille'a. BrailleHandler.set_tether zostały usunięte.
 * config.getConfigDirs został usunięty.
 * konfiguracji. ConfigManager.getConfigValidationParameter został zastąpiony przez getConfigValidation
 * Właściwość inputCore.InputGesture.logIdentifier została usunięta.
   * Zamiast tego użyj _get_identifiers w inputCore.InputGesture.
 * synthDriverHandler.SynthDriver.speakText/speakCharacter zostały usunięte.
 * Usunięto kilka klas synthDriverHandler.SynthSetting.
   * Wcześniej zachowane w celu zapewnienia zgodności z poprzednimi wersjami (#8214), teraz uważane za przestarzałe.
   * Sterowniki, które korzystały z klas SynthSetting, powinny zostać zaktualizowane w celu korzystania z klas DriverSetting.
 * Część starszego kodu została usunięta, w szczególności:
  * Obsługa listy wiadomości programu Outlook sprzed 2003 roku.
  * Klasa nakładki dla klasycznego menu Start, dostępna tylko w systemie Windows Vista i wcześniejszych.
  * Porzucono wsparcie dla Skype 7, ponieważ zdecydowanie już nie działa.
* Dodano platformę do tworzenia dostawców poprawiających wizję; moduły, które mogą zmieniać zawartość ekranu, opcjonalnie na podstawie danych wejściowych z NVDA o lokalizacjach obiektów. (#9064)
 * Dodatki mogą łączyć własnych dostawców w folderze visionEnhancementProviders.
 * Zapoznaj się z modułami vision i visionEnhancementProviders, aby zapoznać się z implementacją struktury i przykładami.
 * Dostawcy ulepszeń wzroku są włączani i konfigurowani za pomocą kategorii "wizja" w oknie dialogowym ustawień NVDA.
* Właściwości klasy abstrakcyjnej są teraz obsługiwane w obiektach, które dziedziczą po baseObject.AutoPropertyObject (np. NVDAObjects i TextInfos). (#10102)
* Wprowadzono displayModel.UNIT_DISPLAYCHUNK jako stałą jednostki textInfos specyficzną dla DisplayModelTextInfo. (#10165)
 * Ta nowa stała umożliwia przechodzenie po tekście w elemencie DisplayModelTextInfo w sposób, który bardziej przypomina sposób zapisywania fragmentów tekstu w modelu bazowym.
* displayModel.getCaretRect zwraca teraz instancję klasy locationHelper.RectLTRB. (#10233)
* Stałe UNIT_CONTROLFIELD i UNIT_FORMATFIELD zostały przeniesione z virtualBuffers.VirtualBufferTextInfo do pakietu textInfos. (#10396)
* Dla każdego wpisu w dzienniku NVDA dołączona jest teraz informacja o wątku, z którego pochodzi. (#10259)
* Obiekty UIA TextInfo mogą być teraz przenoszone/rozwijane za pomocą jednostek tekstowych page, story i formatField. (#10396)
* Moduły zewnętrzne (appModules i globalPlugins) są teraz mniej podatne na przerwanie tworzenia NVDAObjects.
 * Wyjątki spowodowane przez metody "chooseNVDAObjectOverlayClasses" i "event_NVDAObject_init" są teraz poprawnie przechwytywane i rejestrowane.
* Nazwa słownika aria.htmlNodeNameToAriaLandmarkRoles została zmieniona na aria.htmlNodeNameToAriaRoles. Teraz zawiera również role, które nie są punktami orientacyjnymi.
* scriptHandler.isCurrentScript został usunięty z powodu braku użycia. Nie ma zamiennika. (#8677)

## 2019.2.1

Jest to niewielka wersja, która naprawia kilka awarii występujących w wersji 2019.2. Poprawki obejmują:

* Rozwiązano kilka problemów z zawieszaniem się gry Gmail zarówno w Firefoksie, jak i Chrome podczas interakcji z określonymi menu podręcznymi, np. podczas tworzenia filtrów lub zmieniania niektórych ustawień Gmaila. (#10175, #9402, #8924)
* W systemie Windows 7 NVDA nie powoduje już awarii Eksploratora Windows, gdy mysz jest używana w menu Start. (#9435)
* Eksplorator Windows w systemie Windows 7 nie ulega już awarii podczas uzyskiwania dostępu do pól edycji metadanych. (#5337)
* NVDA nie zawiesza się już podczas interakcji z obrazami z identyfikatorem URI base64 w przeglądarce Mozilla Firefox lub Google Chrome. (#10227)

## 2019.2

Najważniejsze cechy tego wydania obejmują automatyczne wykrywanie monitorów brajlowskich Freedom Scientific, eksperymentalne ustawienie w panelu Zaawansowane, aby zatrzymać automatyczne przesuwanie ostrości w trybie przeglądania (co może zapewnić poprawę wydajności), opcję zwiększania szybkości dla syntezatora Windows OneCore w celu osiągnięcia bardzo szybkich szybkości i wiele innych poprawek błędów.

### Nowe funkcje

* Obsługa NVDA Miranda NG działa z nowszymi wersjami klienta. (#9053)
* Możesz teraz domyślnie wyłączyć tryb przeglądania, wyłączając nową opcję "Włącz tryb przeglądania podczas ładowania strony" w ustawieniach trybu przeglądania NVDA. (#8716)
 * Zauważ, że gdy ta opcja jest wyłączona, nadal możesz włączyć tryb przeglądania ręcznie, naciskając NVDA+spacja.
* Możesz teraz filtrować symbole w oknie dialogowym wymowy znaków interpunkcyjnych/symboli, podobnie jak działa filtrowanie w oknie dialogowym listy elementów i gestów wejściowych. (#5761)
* Dodano polecenie zmiany rozdzielczości jednostki tekstu myszy (ile tekstu zostanie wypowiedziane podczas ruchu myszy), nie przypisano mu domyślnego gestu. (#9056)
* Syntezator OneCore dla systemu Windows ma teraz opcję zwiększania szybkości, co pozwala na znacznie szybszą mowę. (#7498)
* Opcja Rate Boost jest teraz konfigurowalna z poziomu pierścienia ustawień syntezatora dla obsługiwanych syntezatorów mowy. (Obecnie eSpeak-NG i Windows OneCore). (#8934)
* Profile konfiguracyjne można teraz aktywować ręcznie za pomocą gestów. (#4209)
 * Gest należy skonfigurować w oknie dialogowym "Gesty wprowadzania".
* W środowisku Eclipse dodano obsługę autouzupełniania w edytorze kodu. (#5667)
 * Dodatkowo, informacje Javadoc mogą być odczytywane z edytora, gdy są obecne, za pomocą NVDA+d.
* Do panelu Ustawienia zaawansowane dodano opcję eksperymentalną, która pozwala zatrzymać fokus systemu przed podążaniem za kursorem trybu przeglądania (Automatycznie ustaw fokus systemu na elementy, na których można ustawić fokus). (#2039) Chociaż wyłączenie tego może nie być odpowiednie dla wszystkich witryn, może to rozwiązać:
 * Efekt gumki: NVDA sporadycznie cofa ostatnie naciśnięcie w trybie przeglądania, przeskakując do poprzedniej lokalizacji.
 * Pola edycji kradną fokus systemu podczas przechodzenia przez nie strzałką w dół na niektórych stronach internetowych.
 * Naciśnięcia w trybie przeglądania reagują powoli.
* W przypadku sterowników monitorów brajlowskich, które go obsługują, ustawienia sterownika można teraz zmienić z kategorii ustawień brajla w oknie ustawień NVDA. (#7452)
* Monitory brajlowskie Freedom Scientific są teraz obsługiwane przez automatyczne wykrywanie monitorów brajlowskich. (#7727)
* Dodano polecenie pokazujące zamiennik symbolu pod kursorem recenzji. (#9286)
* Dodano eksperymentalną opcję do panelu Ustawienia zaawansowane, która pozwala wypróbować nową, trwającą nad pracami przeróbkę obsługi konsoli Windows NVDA przy użyciu interfejsu API automatyzacji interfejsu użytkownika firmy Microsoft. (#9614)
* W konsoli języka Python pole wejściowe obsługuje teraz wklejanie wielu wierszy ze schowka. (#9776)

### Zmiany

* Głośność syntezatora jest teraz zwiększana i zmniejszana o 5 zamiast o 10 podczas korzystania z pierścienia ustawień. (#6754)
* Poprawiono tekst w menedżerze dodatków, gdy NVDA jest uruchamiany z flagą --disable-addons. (#9473)
* Zaktualizowano adnotacje emoji Unicode Common Locale Data Repository do wersji 35.0. (#9445)
* Skrót klawiszowy dla pola filtru na liście elementów w trybie przeglądania został zmieniony na alt+y. (#8728)
* Gdy automatycznie wykrywany monitor brajlowski jest podłączony przez Bluetooth, NVDA będzie nadal szukać wyświetlaczy USB obsługiwanych przez ten sam sterownik i przełączy się na połączenie USB, jeśli stanie się ono dostępne. (#8853)
* Zaktualizowano eSpeak-NG do zatwierdzenia 67324cc.
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.10.0. (#9439, #9678)
* NVDA będzie teraz zgłaszać słowo "wybrane" po zgłoszeniu tekstu, który użytkownik właśnie wybrał. (#9028, #9909)
* W Microsoft Visual Studio Code NVDA jest domyślnie w trybie koncentracji uwagi. (#9828)

### Poprawki błędów

* NVDA nie ulega już awarii, gdy katalog dodatków jest pusty. (#7686)
* Znaki LTR i RTL nie są już raportowane w alfabecie Braille'a ani w mowie na znak podczas uzyskiwania dostępu do okna właściwości. (#8361)
* Podczas przechodzenia do pól formularzy za pomocą szybkiej nawigacji w trybie przeglądania ogłaszane jest teraz całe pole formularza, a nie tylko pierwszy wiersz. (#9388)
* NVDA nie będzie już cichnąć po zamknięciu aplikacji Poczta systemu Windows 10. (#9341)
* NVDA nie uruchamia się już bez uruchamiania, gdy ustawienia regionalne użytkownika są ustawione na ustawienia regionalne nieznane NVDA, takie jak angielski (Holandia). (#8726)
* Gdy tryb przeglądania jest włączony w programie Microsoft Excel i przełączysz się do przeglądarki w trybie koncentracji uwagi lub odwrotnie, stan trybu przeglądania jest teraz odpowiednio raportowany. (#8846)
* NVDA teraz poprawnie raportuje linię przy kursorze myszy w Notepad++ i innych edytorach opartych na Scintilla. (#5450)
* W Dokumentach Google (i innych edytorach internetowych) w alfabecie Braille'a nie jest już czasami błędnie wyświetlany napis "lst end" przed kursorem w środku elementu listy. (#9477)
* W aktualizacji systemu Windows 10 z maja 2019 r. NVDA nie wyświetla już wielu powiadomień o głośności, jeśli zmienia głośność za pomocą przycisków sprzętowych, gdy Eksplorator plików ma fokus. (#9466)
* Wczytywanie okna dialogowego wymowy znaków interpunkcyjnych/symboli jest teraz znacznie szybsze w przypadku korzystania ze słowników symboli zawierających ponad 1000 haseł. (#8790)
* W kontrolkach Scintilla, takich jak Notepad++, NVDA może odczytać poprawną linię, gdy włączone jest zawijanie słów. (#9424)
* W programie Microsoft Excel lokalizacja komórki jest ogłaszana po jej zmianie w wyniku gestów shift+enter lub shift+numpadEnter. (#9499)
* W programie Visual Studio 2017 lub nowszym w oknie Eksplorator obiektów wybrany element w drzewie obiektów lub drzewie elementów członkowskich z kategoriami jest teraz poprawnie zgłaszany. (#9311)
* Dodatki o nazwach, które różnią się tylko wielkością liter, nie są już traktowane jako osobne dodatki. (#9334)
* W przypadku głosów systemu Windows OneCore szybkość ustawiona w NVDA nie ma już wpływu na szybkość ustawioną w ustawieniach mowy systemu Windows 10. (#7498)
* Dziennik można teraz otworzyć za pomocą NVDA+F1, gdy nie ma informacji o programiście dla bieżącego obiektu nawigatora. (#8613)
* Ponownie możliwe jest korzystanie z poleceń nawigacji po tabelach NVDA w Google Docs, Firefoksie i Chrome. (#9494)
* bumpera działają teraz poprawnie na monitorach brajlowskich Freedom Scientific. (#8849)
* Podczas odczytywania pierwszego znaku dokumentu w Notepad++ 7.7 X64, NVDA nie zawiesza się już na maksymalnie dziesięć sekund. (#9609)
* HTCom może być teraz używany z monitorem brajlowskim Handy Tech w połączeniu z NVDA. (#9691)
* W przeglądarce Mozilla Firefox aktualizacje regionu dynamicznego nie są już zgłaszane, jeśli region aktywny znajduje się na karcie w tle. (#1318)
* Okno dialogowe wyszukiwania NVDA w trybie przeglądania nie przestaje działać, jeśli okno dialogowe NVDA About jest aktualnie otwarte w tle. (#8566)

### Zmiany dla deweloperów

* Teraz możesz ustawić właściwość "disableBrowseModeByDefault" w modułach aplikacji, aby domyślnie wyłączyć tryb przeglądania. (#8846)
* Rozszerzony styl okna okna jest teraz uwidoczniany za pomocą właściwości "extendedWindowStyle" w obiektach Window i ich pochodnych. (#9136)
* Zaktualizowano pakiet comtypes do wersji 1.1.7. (#9440, #8522)
* W przypadku korzystania z polecenia info modułu raportu kolejność informacji została zmieniona, aby moduł był prezentowany jako pierwszy. (#7338)
* Dodano przykład, aby zademonstrować użycie nvdaControllerClient.dll z języka C#. (#9600)
* Dodano nową funkcję isWin10 do modułu winVersion, która zwraca informację, czy ta kopia NVDA jest uruchomiona na (przynajmniej) dostarczonej wersji systemu Windows 10 (takiej jak 1903). (#9761)
* Konsola NVDA Python zawiera teraz więcej użytecznych modułów w swojej przestrzeni nazw (takich jak appModules, globalPlugins, config i textInfos). (#9789)
* Wynik ostatniego wykonanego polecenia w konsoli NVDA Pythona jest teraz dostępny ze zmiennej _ (line). (#9782)
 * Zauważ, że zasłania to funkcję tłumaczenia gettext, zwaną również "_". Aby uzyskać dostęp do funkcji tłumaczenia: del _

## 2019.1.1

W tym wydaniu punktowym naprawiono następujące błędy:

* NVDA nie powoduje już awarii programu Excel 2007 ani nie odmawia raportowania, jeśli komórka zawiera formułę. (#9431)
* Google Chrome nie ulega już awarii podczas interakcji z niektórymi listami. (#9364)
* Rozwiązano problem, który uniemożliwiał kopiowanie konfiguracji użytkownika do profilu konfiguracji systemu. (#9448)
* W programie Microsoft Excel NVDA ponownie używa zlokalizowanej wiadomości podczas raportowania lokalizacji scalonych komórek. (#9471)

## 2019.1

Najważniejsze cechy tej wersji obejmują poprawę wydajności podczas uzyskiwania dostępu zarówno do programu Microsoft Word, jak i Excel, ulepszenia stabilności i zabezpieczeń, takie jak obsługa dodatków z informacjami o zgodności wersji oraz wiele innych poprawek błędów.

Należy pamiętać, że począwszy od tego wydania NVDA, niestandardowe appModules, globalPlugins, sterowniki monitorów brajlowskich i sterowniki syntezatorów nie będą już automatycznie ładowane z katalogu konfiguracyjnego użytkownika NVDA.
Powinny one być raczej instalowane jako część dodatku NVDA. Dla tych, którzy tworzą kod do dodatku, kod do testowania może być umieszczony w nowym katalogu dewelopera w katalogu konfiguracji użytkownika NVDA, jeśli opcja Szkicownik programisty jest włączona w nowym panelu ustawień zaawansowanych NVDA.
Te zmiany są konieczne, aby lepiej zapewnić kompatybilność niestandardowego kodu, tak aby NVDA nie uległa awarii, gdy ten kod stanie się niekompatybilny z nowszymi wersjami.
Zapoznaj się z poniższą listą zmian, aby uzyskać więcej informacji na ten temat oraz dowiedzieć się, w jaki sposób dodatki są teraz lepiej wersjonowane.

### Nowe funkcje

* Nowe tablice brajlowskie: afrikaans, arabski 8-punktowy komputerowy alfabet Braille'a, arabski ocena 2, hiszpański klasa 2. (#4435, #9186)
* Dodano opcję do ustawień myszy NVDA, aby NVDA obsługiwała sytuacje, w których mysz jest kontrolowana przez inną aplikację. (#8452)
 * Umożliwi to NVDA śledzenie myszy, gdy system jest sterowany zdalnie za pomocą TeamViewer lub innego oprogramowania do zdalnego sterowania.
* Dodano parametr wiersza poleceń '--enable-start-on-logon', aby umożliwić skonfigurowanie, czy ciche instalacje NVDA ustawiają NVDA tak, aby uruchamiało się przy logowaniu do systemu Windows, czy nie. Określ wartość true, aby rozpocząć logowanie, lub false, aby nie rozpoczynać się przy logowaniu. Jeśli argument --enable-start-on-logon nie jest w ogóle podany, NVDA domyślnie uruchomi się przy logowaniu, chyba że został już skonfigurowany tak, aby nie był już skonfigurowany przez poprzednią instalację. (#8574)
* Możliwe jest wyłączenie funkcji logowania NVDA poprzez ustawienie poziomu logowania na "wyłączony" w panelu ustawień ogólnych. (#8516)
* Obecność formuł w arkuszach kalkulacyjnych LibreOffice i Apache OpenOffice jest teraz zgłaszana. (#860)
* W przeglądarkach Mozilla Firefox i Google Chrome tryb przeglądania wyświetla teraz zaznaczony element w listach i drzewach.
 * Działa to w Firefoksie 66 i nowszych.
 * Nie działa to w przypadku niektórych pól listy (kontrolek wyboru HTML) w Chrome.
* Wczesne wsparcie dla aplikacji, takich jak Mozilla Firefox, na komputerach z procesorami ARM64 (np. Qualcomm Snapdragon). (#9216)
* Nowa kategoria Ustawienia zaawansowane została dodana do okna dialogowego Ustawienia NVDA, w tym opcja wypróbowania nowego wsparcia NVDA dla Microsoft Word za pośrednictwem Microsoft UI Automation API. (#9200)
* Dodano obsługę widoku graficznego w przystawce Zarządzanie dyskami systemu Windows. (#1486)
* Dodano obsługę alfabetów Braille'a Handy Tech Connect i Basic Braille 84. (#9249)

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.8.0. (#9013)
* Autorzy dodatków mogą teraz wymusić minimalną wymaganą wersję NVDA dla swoich dodatków. NVDA odmówi instalacji lub załadowania dodatku, którego minimalna wymagana wersja NVDA jest wyższa niż bieżąca wersja NVDA. (#6275)
* Autorzy dodatków mogą teraz określić ostatnią wersję NVDA, na której dodatek został przetestowany. Jeśli dodatek został przetestowany tylko z wersją NVDA niższą niż bieżąca, NVDA odmówi instalacji lub załadowania dodatku. (#6275)
* Ta wersja NVDA pozwoli na instalację i ładowanie dodatków, które nie zawierają jeszcze informacji o minimalnej i ostatnio testowanej wersji NVDA, ale aktualizacja do przyszłych wersji NVDA (np. 2019.2) może automatycznie spowodować wyłączenie tych starszych dodatków.
* Polecenie przeniesienia myszy do obiektu nawigatora jest teraz dostępne w programie Microsoft Word, a także w kontrolkach interfejsu użytkownika, w szczególności w przeglądarce Microsoft Edge. (#7916, #8371)
* Ulepszono raportowanie tekstu pod myszą w przeglądarce Microsoft Edge i innych aplikacjach UIA. (#8370)
* Gdy NVDA jest uruchamiany z parametrem wiersza poleceń '--portable-path', podana ścieżka jest automatycznie wypełniana podczas próby utworzenia przenośnej kopii NVDA za pomocą menu NVDA. (#8623)
* Zaktualizowano ścieżkę do norweskiej tabeli brajlowskiej, aby odzwierciedlić standard z roku 2015. (#9170)
* Podczas nawigacji za pomocą akapitu (control+strzałki w górę lub w dół) lub za pomocą komórki tabeli (control+alt+strzałki), istnienie błędów ortograficznych nie będzie już ogłaszane, nawet jeśli NVDA jest skonfigurowane do ogłaszania ich automatycznie. Dzieje się tak, ponieważ akapity i komórki tabel mogą być dość duże, a wykrywanie błędów ortograficznych w niektórych aplikacjach może być bardzo kosztowne. (#9217)
* NVDA nie ładuje już automatycznie niestandardowych modułów aplikacji, globalPluginów oraz sterowników brajla i syntezatora z katalogu konfiguracyjnego użytkownika NVDA. Ten kod powinien być zamiast tego spakowany jako dodatek z poprawnymi informacjami o wersji, zapewniając, że niekompatybilny kod nie zostanie uruchomiony z aktualnymi wersjami NVDA. (#9238)
 * Dla programistów, którzy muszą testować kod w trakcie jego tworzenia, włącz katalog szkicownika NVDA w kategorii Zaawansowane ustawień NVDA i umieść swój kod w katalogu "scratchpad" znajdującym się w katalogu konfiguracji użytkownika NVDA, gdy ta opcja jest włączona.

### Poprawki błędów

* W przypadku korzystania z syntezatora mowy OneCore w systemie Windows 10 z aktualizacją z kwietnia 2018 r. i nowszych duże fragmenty ciszy nie są już wstawiane między wypowiedziami mowy. (#8985)
* Podczas przechodzenia według znaku w kontrolkach zwykłego tekstu (takich jak Notatnik) lub w trybie przeglądania, 32-bitowe znaki emoji składające się z dwóch punktów kodowych UTF-16 (takich jak 🤦 ) będą teraz odczytywane poprawnie. (#8782)
* Ulepszono okno dialogowe potwierdzenia restartu po zmianie języka interfejsu NVDA. Tekst i etykiety przycisków są teraz bardziej zwięzłe i mniej mylące. (#6416)
* Jeśli nie uda się załadować syntezatora mowy innej firmy, NVDA powróci do syntezatora mowy Windows OneCore w systemie Windows 10, a nie do espeak. (#9025)
* Usunięto wpis "Okno dialogowe powitania" w menu NVDA na bezpiecznych ekranach. (#8520)
* Podczas korzystania z Tab lub szybkiej nawigacji w trybie przeglądania legendy na panelach kart są teraz wyświetlane w bardziej spójny sposób. (#709)
* NVDA będzie teraz informować o zmianach wyboru dla niektórych selektorów czasu, takich jak w aplikacji Alarmy i Zegar w systemie Windows 10. (#5231)
* W Centrum akcji systemu Windows 10 NVDA ogłosi komunikaty o stanie podczas przełączania szybkich działań, takich jak jasność i wspomaganie ostrości. (#8954)
* W Centrum akcji w aktualizacji systemu Windows 10 z października 2018 r. i wcześniejszych, NVDA rozpozna kontrolkę szybkiej akcji jasności jako przycisk, a nie przycisk przełączania. (#8845)
* NVDA ponownie będzie śledzić kursor i informować o usuniętych znakach w programie Microsoft Excel, przechodząc do pól edycji i je znajdując. (#9042)
* Naprawiono rzadką awarię trybu przeglądania w Firefoksie. (#9152)
* NVDA nie zgłasza już błędnego zgłaszania fokusu dla niektórych kontrolek na wstążce pakietu Microsoft Office 2016 po zwinięciu.
* NVDA nie zgłasza już sugerowanego kontaktu podczas wprowadzania adresów w nowych wiadomościach w programie Outlook 2016. (#8502)
* Kilka ostatnich przywoływania kursora na 80-komórkowych monitorach eurobrajlowskich nie kieruje już kursora do pozycji na początku lub tuż po początku linii brajlowskiej. (#9160)
* Poprawiono nawigację po tabeli w widoku wątków w Mozilla Thunderbird. (#8396)
* W przeglądarkach Mozilla Firefox i Google Chrome przełączanie w tryb ostrości działa teraz poprawnie dla niektórych pól listy i drzew (gdzie pole/drzewo listy nie jest samo w sobie zogniskowane, ale jego elementy są). (#3573, #9157)
* Tryb przeglądania jest teraz poprawnie włączony domyślnie podczas czytania wiadomości w programie Outlook 2016/365, jeśli korzystasz z eksperymentalnej obsługi automatyzacji interfejsu użytkownika NVDA dla dokumentów programu Word. (#9188)
* NVDA jest teraz mniej podatny na zawieszanie się w taki sposób, że jedynym sposobem na ucieczkę jest wylogowanie się z bieżącej sesji systemu Windows. (#6291)
* W aktualizacji systemu Windows 10 z października 2018 r. i nowszych, podczas otwierania historii schowka w chmurze z pustym schowkiem, NVDA ogłosi stan schowka. (#9103)
* W aktualizacji systemu Windows 10 z października 2018 r. i nowszych, podczas wyszukiwania emotikonów w panelu emotikonów, NVDA ogłosi najlepszy wynik wyszukiwania. (#9105)
* NVDA nie zawiesza się już w głównym oknie Oracle VirtualBox 5.2 i nowszych. (#9202)
* Responsywność programu Microsoft Word podczas nawigacji po wierszu, akapicie lub komórce tabeli może zostać znacznie poprawiona w niektórych dokumentach. Przypomnienie, że aby uzyskać najlepszą wydajność, po otwarciu dokumentu należy ustawić program Microsoft Word na widok roboczy za pomocą alt+w,e. (#9217)
* W przeglądarkach Mozilla Firefox i Google Chrome puste alerty nie są już zgłaszane. (#5657)
* Znaczna poprawa wydajności podczas nawigowania po komórkach w programie Microsoft Excel, szczególnie gdy arkusz kalkulacyjny zawiera komentarze i/lub listy rozwijane walidacji. (#7348)
* Nie powinno być już konieczne wyłączanie edycji w komórce w opcjach programu Microsoft Excel, aby uzyskać dostęp do kontrolki edycji komórki za pomocą NVDA w programie Excel 2016/365. (#8146).
* Naprawiono zawieszanie się przeglądarki Firefox, które czasami pojawiało się podczas szybkiej nawigacji po punktach orientacyjnych, jeśli używany był dodatek Enhanced Aria. (#8980)

### Zmiany dla deweloperów

* NVDA można teraz budować ze wszystkimi edycjami programu Microsoft Visual Studio 2017 (nie tylko z edycją Community). (#8939)
* Możesz teraz dołączyć dane wyjściowe dziennika z liblouis do dziennika NVDA, ustawiając flagę boolean louis w sekcji debugLogging konfiguracji NVDA. (#4554)
* Autorzy dodatków mogą teraz podawać informacje o zgodności wersji NVDA w manifestach dodatków. (#6275, #9055)
 * minimumNVDAVersion: Minimalna wymagana wersja NVDA, aby dodatek działał poprawnie.
 * lastTestedNVDAVersion: Ostatnia wersja NVDA, z którą został przetestowany dodatek.
* Obiekty OffsetsTextInfo mogą teraz implementować metodę _getBoundingRectFromOffset, aby umożliwić pobieranie prostokątów ograniczających na znaki, a nie punkty. (#8572)
* Dodano właściwość boundingRect do obiektów TextInfo w celu pobrania prostokąta ograniczającego zakresu tekstu. (#8371)
* Właściwości i metody w klasach mogą być teraz oznaczone jako abstrakcyjne w NVDA. Te klasy zgłoszą błąd, jeśli zostanie utworzone wystąpienie. (#8294, #8652, #8658)
* NVDA może rejestrować czas od wprowadzenia tekstu, co pomaga w pomiarze odczuwalnej responsywności. Można to włączyć, ustawiając ustawienie timeSinceInput na True w sekcji debugLog konfiguracji NVDA. (#9167)

## 2018.4.1

To wydanie naprawia awarię podczas uruchamiania, jeśli język interfejsu użytkownika NVDA jest ustawiony na aragoński. (#9089)

## 2018.4

Najważniejsze cechy tego wydania to poprawa wydajności w najnowszych wersjach przeglądarki Mozilla Firefox, ogłoszenie emotikonów ze wszystkimi syntezatorami, raportowanie statusu odpowiedzi/przesłanych dalej w Outlooku, raportowanie odległości kursora od krawędzi strony Microsoft Word i wiele poprawek błędów.

### Nowe funkcje

* Nowe tablice brajlowskie: chiński (Chiny, mandaryński) ocena 1 i klasa 2. (#5553)
* Stan Udzielono odpowiedzi / Przesłano dalej jest teraz raportowany dla elementów poczty na liście wiadomości programu Microsoft Outlook. (#6911)
* NVDA jest teraz w stanie odczytywać opisy emoji, a także innych znaków, które są częścią repozytorium danych Unicode Common Locale Data Repository. (#6523)
* W programie Microsoft Word odległość kursora od górnej i lewej krawędzi strony można podać, naciskając NVDA+numpadDelete. (#1939)
* W Arkuszach Google z włączonym trybem brajla NVDA nie ogłasza już "wybrane" w każdej komórce podczas przenoszenia fokusu między komórkami. (#8879)
* Dodano obsługę programów Foxit Reader i Foxit Phantom PDF. (#8944)
* Dodano obsługę narzędzia bazy danych DBeaver. (#8905)

### Zmiany

* Nazwa "Dymki pomocy raportu" w oknie dialogowym Prezentacje obiektów została zmieniona na "Powiadomienia raportu", aby uwzględnić raportowanie wyskakujących powiadomień w systemie Windows 8 i nowszych. (#5789)
* W ustawieniach klawiatury NVDA, pola wyboru do włączania lub wyłączania modyfikujących NVDA są teraz wyświetlane na liście, a nie jako osobne pola wyboru.
* NVDA nie będzie już wyświetlać nadmiarowych informacji podczas odczytywania zasobnika systemowego zegara w niektórych wersjach systemu Windows. (#4364)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.7.0. (#8697)
* Zaktualizowano eSpeak-NG w celu zatwierdzenia 919f3240cbb.

### Poprawki błędów

* W programie Outlook 2016/365 kategoria i stan flagi są raportowane dla wiadomości. (#8603)
* Gdy NVDA jest ustawione na języki takie jak kirgiski, mongolski lub macedoński, nie wyświetla już okna dialogowego podczas uruchamiania z ostrzeżeniem, że język nie jest obsługiwany przez system operacyjny. (#8064)
* Przesunięcie myszy na obiekt nawigatora spowoduje teraz znacznie dokładniejsze przesunięcie myszy do pozycji trybu przeglądania w przeglądarkach Mozilla Firefox, Google Chrome i Acrobat Reader DC. (#6460)
* Ulepszono interakcję z polami kombi w Internecie w przeglądarkach Firefox, Chrome i Internet Explorer. (#8664)
* Jeśli działa na japońskiej wersji systemu Windows XP lub Vista, NVDA wyświetla teraz komunikat o wymaganiach dotyczących wersji systemu operacyjnego zgodnie z oczekiwaniami. (#8771)
* Poprawiono wydajność podczas nawigacji po dużych stronach z wieloma dynamicznymi zmianami w przeglądarce Mozilla Firefox. (#8678)
* W alfabecie Braille'a atrybuty czcionki nie są już wyświetlane, jeśli zostały one wyłączone w ustawieniach formatowania dokumentu. (#7615)
* NVDA nie zawodzi już w śledzeniu fokusu w Eksploratorze plików i innych aplikacjach korzystających z automatyzacji interfejsu użytkownika, gdy inna aplikacja jest zajęta (np. przetwarzanie wsadowe dźwięku). (#7345)
* W menu ARIA w Internecie Escape będzie teraz przekazywany do menu i nie będzie już bezwarunkowo wyłączał trybu ostrości. (#3215)
* W nowym interfejsie internetowym Gmaila, podczas korzystania z szybkiej nawigacji w wiadomościach podczas ich czytania, cała treść wiadomości nie jest już raportowana po elemencie, do którego właśnie przeszedłeś. (#8887)
* Po zaktualizowaniu NVDA przeglądarki takie jak Firefox i Google Chrome nie powinny się już zawieszać, a tryb przeglądania powinien nadal poprawnie odzwierciedlać aktualizacje wszystkich aktualnie załadowanych dokumentów. (#7641)
* NVDA nie zgłasza już klikania wiele razy z rzędu podczas nawigowania po klikalnej zawartości w trybie przeglądania. (#7430)
* Gesty wykonywane na monitorach brajlowskich baum Vario 40 nie będą już przerywać się wykonywaniu. (#8894)
* W Google Slides z Mozilla Firefox NVDA nie raportuje już zaznaczonego tekstu w każdym formancie, na którym znajduje się fokus. (#8964)

### Zmiany dla deweloperów

* gui.nvdaControls zawiera teraz dwie klasy do tworzenia list z ułatwieniami dostępu z polami wyboru. (#7325)
 * CustomCheckListBox jest dostępną podklasą wx. Pole wyboru.
 * AutoWidthColumnCheckListCtrl dodaje dostępne pola wyboru do AutoWidthColumnListCtrl, który sam jest oparty na wx. ListCtrl.
* Jeśli chcesz udostępnić widżet wx, który jeszcze tego nie zrobił, możesz to zrobić za pomocą instancji gui.accPropServer.IAccPropServer_impl. (#7491)
 * Aby uzyskać więcej informacji, zobacz implementację gui.nvdaControls.ListCtrlAccPropServer.
* Zaktualizowano configobj do wersji 5.1.0dev commit 5b5de48a. (#4470)
* Akcja config.post_configProfileSwitch przyjmuje teraz opcjonalny argument słowa kluczowego prevConf, co pozwala programom obsługi na podejmowanie działań na podstawie różnic między konfiguracją przed i po przełączeniu profilu. (#8758)

## 2018.3.2

Jest to drobna wersja, która ma na celu obejście awarii przeglądarki Google Chrome podczas nawigowania po tweettach w systemie [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Jest to drobne wydanie mające na celu naprawienie krytycznego błędu w NVDA, który powodował awarię 32-bitowych wersji przeglądarki Mozilla Firefox. (#8759)

## 2018.3

Najważniejsze cechy tej wersji to automatyczne wykrywanie wielu monitorów brajlowskich, obsługa nowych funkcji systemu Windows 10, w tym panelu wprowadzania emotikonów systemu Windows 10, oraz wiele innych poprawek błędów.

### Nowe funkcje

* NVDA będzie zgłaszać błędy gramatyczne, gdy zostaną odpowiednio ujawnione przez strony internetowe w przeglądarkach Mozilla Firefox i Google Chrome. (#8280)
* Treści oznaczone jako wstawione lub usunięte na stronach internetowych są teraz zgłaszane w przeglądarce Google Chrome. (#8558)
* Dodano obsługę BrailleNote QT i kółka przewijania Apex BT, gdy BrailleNote jest używany jako monitor brajlowski z NVDA. (#5992, #5993)
* Dodano skrypty do raportowania upływającego czasu i całkowitego czasu bieżącej ścieżki w Foobar2000. (#6596)
* Symbol poleceń Maca (⌘) jest teraz odczytywany podczas czytania tekstu za pomocą dowolnego syntezatora. (#8366)
* Niestandardowe role za pomocą atrybutu aria-roledescription są teraz obsługiwane we wszystkich przeglądarkach internetowych. (#8448)
* Nowe tablice brajlowskie: czeski 8 punktów, środkowokurdyjski, esperanto, węgierski, szwedzki 8-punktowy komputerowy brajl braille'a. (#8226, #8437)
* Dodano obsługę automatycznego wykrywania monitorów brajlowskich w tle. (#1271)
 * Obecnie obsługiwane są monitory ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille i HumanWare BrailleNote oraz Brailliant BI/B.
 * Możesz włączyć tę funkcję, wybierając opcję automatyczną z listy monitorów brajlowskich w oknie dialogowym wyboru monitora brajlowskiego NVDA.
 * Aby uzyskać dodatkowe informacje, zapoznaj się z dokumentacją.
* Dodano obsługę różnych nowoczesnych funkcji wprowadzania danych wprowadzonych w najnowszych wersjach systemu Windows 10. Należą do nich panel emoji (Fall Creators Update), dyktowanie (Fall Creators Update), sugestie wprowadzania danych z klawiatury sprzętowej (aktualizacja z kwietnia 2018 r.) i wklejanie schowka w chmurze (aktualizacja z października 2018 r.). (#7273)
* Treść oznaczona jako cytat blokowy za pomocą ARIA (role blockquote) jest teraz obsługiwana w przeglądarce Mozilla Firefox 63. (#8577)

### Zmiany

* Lista dostępnych języków w Ustawieniach Ogólnych NVDA jest teraz sortowana na podstawie nazw języków, a nie kodów ISO 639. (#7284)
* Dodano domyślne gesty dla Alt+Shift+Tab i Windows+Tab dla wszystkich obsługiwanych monitorów brajlowskich Freedom Scientific. (#7387)
* W przypadku wyświetlaczy ALVA BC680 i konwerterów protokołów możliwe jest teraz przypisanie różnych funkcji do lewego i prawego inteligentnego pada, kciuka i eTouch. (#8230)
* W przypadku wyświetlaczy ALVA BC6 kombinacja sp2+sp3 będzie teraz ogłaszać aktualną datę i godzinę, podczas gdy sp1+sp2 emuluje Windows. (#8230)
* Użytkownik jest pytany raz po uruchomieniu NVDA, czy jest zadowolony z wysyłania statystyk użytkowania do NV Access podczas sprawdzania dostępności aktualizacji NVDA. (#8217)
* Podczas sprawdzania dostępności aktualizacji, jeśli użytkownik wyraził zgodę na wysyłanie statystyk użycia do NV Access, NVDA wyśle teraz nazwę aktualnie używanego sterownika syntezatora i monitora brajlowskiego, aby pomóc w lepszym ustaleniu priorytetów dla przyszłych prac nad tymi sterownikami. (#8217)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.6.0. (#8365)
* Zaktualizowano ścieżkę do poprawnej rosyjskiej tabeli brajlowskiej z ośmioma kropkami. (#8446)
* Zaktualizowano eSpeak-ng do wersji 1.49.3dev commit 910f4c2. (#8561)

### Poprawki błędów

* Etykiety z ułatwieniami dostępu dla kontrolek w przeglądarce Google Chrome są teraz łatwiej zgłaszane w trybie przeglądania, gdy etykieta sama w sobie nie jest wyświetlana. (#4773)
* Powiadomienia są teraz obsługiwane w Zoom. Obejmuje to na przykład stan wyciszenia/wyłączenia wyciszenia i wiadomości przychodzące. (#7754)
* Przełączenie prezentacji kontekstu brajlowskiego w trybie przeglądania nie powoduje już, że wyjście brajlowskie przestaje podążać za kursorem w trybie przeglądania. (#7741)
* Monitory brajlowskie ALVA BC680 nie mają już sporadycznych problemów z inicjalizacją. (#8106)
* Domyślnie wyświetlacze ALVA BC6 nie będą już wykonywać emulowanych klawiatury systemowej po naciśnięciu kombinacji obejmujących sp2+sp3 w celu uruchomienia funkcji wewnętrznej. (#8230)
* Naciśnięcie sp2 na wyświetlaczu ALVA BC6 w celu emulacji alt działa teraz zgodnie z reklamą. (#8360)
* NVDA nie ogłasza już nadmiarowych zmian w układzie klawiatury. (#7383, #8419)
* Śledzenie myszy jest teraz znacznie dokładniejsze w Notatniku i innych kontrolkach edycji zwykłego tekstu, gdy znajduje się w dokumencie zawierającym więcej niż 65535 znaków. (#8397)
* NVDA rozpozna więcej okien dialogowych w systemie Windows 10 i innych nowoczesnych aplikacjach. (#8405)
* W systemie Windows 10 z października 2018 r. oraz Server 2019 i nowszych NVDA nie zawodzi już w śledzeniu fokusu systemu, gdy aplikacja zawiesza się lub zalewa system zdarzeniami. (#7345, #8535)
* Użytkownicy są teraz informowani o próbie odczytania lub skopiowania pustego paska stanu. (#7789)
* Rozwiązano problem polegający na tym, że stan "niesprawdzony" w kontrolkach nie jest zgłaszany w mowie, jeśli kontrolka została wcześniej sprawdzona w połowie. (#6946)
* Na liście języków w Ustawieniach Ogólnych NVDA, nazwa języka birmańskiego jest wyświetlana poprawnie w systemie Windows 7. (#8544)
* W Microsoft Edge NVDA ogłosi powiadomienia, takie jak dostępność widoku do odczytu i postęp ładowania strony. (#8423)
* Podczas przechodzenia do listy w sieci, NVDA będzie teraz zgłaszać jej etykietę, jeśli autor strony ją podał. (#7652)
* Podczas ręcznego przypisywania funkcji do gestów na konkretnym monitorze brajlowskim, gesty te są teraz zawsze wyświetlane jako przypisane do tego monitora. Wcześniej były one wyświetlane tak, jakby były przypisane do aktualnie aktywnego ekranu. (#8108)
* Obsługiwana jest teraz 64-bitowa wersja programu Media Player Classic. (#6066)
* Kilka ulepszeń obsługi alfabetu Braille'a w programie Microsoft Word z włączoną automatyzacją interfejsu użytkownika:
 * Podobnie jak w przypadku innych wielowierszowych pól tekstowych, po umieszczeniu na początku dokumentu w alfabecie Braille'a ekran jest teraz przesuwany w taki sposób, że pierwszy znak dokumentu znajduje się na początku ekranu. (#8406)
 * Zmniejszono zbyt szczegółową prezentację fokusu zarówno w mowie, jak i alfabecie Braille'a podczas koncentracji fokusu na dokumencie programu Word. (#8407)
 * Routing kursora w alfabecie Braille'a działa teraz poprawnie na liście w dokumencie programu Word. (#7971)
 * Nowo wstawione punktory/numery w dokumencie programu Word są poprawnie zgłaszane zarówno w mowie, jak i w alfabecie Braille'a. (#7970)
* W systemie Windows 10 1803 i nowszych można teraz instalować dodatki, jeśli włączona jest funkcja "Użyj Unicode UTF-8 do obsługi języków na całym świecie". (#8599)
* NVDA nie będzie już sprawiać, że iTunes 12.9 i nowsze będą całkowicie bezużyteczne do interakcji. (#8744)

### Zmiany dla deweloperów

* Dodano scriptHandler.script, który może funkcjonować jako dekorator skryptów na obiektach skryptowalnych. (#6266)
* Wprowadzono ramy testowania systemu dla NVDA. (#708)
* Wprowadzono pewne zmiany w module hwPortUtils: (#1271)
 * listUsbDevices zwraca teraz słowniki z informacjami o urządzeniu, w tym hardwareID i devicePath.
 * Słowniki dostarczane przez listComPorts zawierają teraz również wpis usbID dla portów COM z informacjami USB VID/PID w ich identyfikatorze sprzętowym.
* Zaktualizowano wxPython do wersji 4.0.3. (#7077)
* Ponieważ NVDA obsługuje teraz tylko Windows 7 SP1 i nowsze, klucz "minWindowsVersion" używany do sprawdzania, czy UIA powinien być włączony dla określonej wersji systemu Windows, został usunięty. (#8422)
* Możesz teraz zarejestrować się, aby otrzymywać powiadomienia o akcjach zapisywania/resetowania konfiguracji za pośrednictwem nowych akcji config.pre_configSave, config.post_configSave, config.pre_configReset i config.post_configReset. (#7598)
 * config.pre_configSave jest używany do powiadamiania, gdy konfiguracja NVDA ma zostać zapisana, a config.post_configSave jest wywoływany po zapisaniu konfiguracji.
 * config.pre_configReset i config.post_configReset zawiera flagę ustawień fabrycznych, która określa, czy ustawienia mają być ponownie ładowane z dysku (false), czy resetowane do domyślnych (true).
* Nazwa config.configProfileSwitch została zmieniona na config.post_configProfileSwitch, aby odzwierciedlić fakt, że ta akcja jest wywoływana po przełączeniu profilu. (#7598)
* Interfejsy automatyzacji interfejsu użytkownika zaktualizowane do aktualizacji systemu Windows 10 z października 2018 r. i serwera 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)

## 2018.2.1

To wydanie zawiera aktualizacje tłumaczeń spowodowane usunięciem w ostatniej chwili funkcji, która powodowała problemy.

## 2018.2

Najważniejsze cechy tego wydania to obsługa tabel w Kindle dla komputerów PC, obsługa monitorów brajlowskich HumanWare BrailleNote Touch i BI14, ulepszenia syntezatorów mowy Onecore i Sapi5, ulepszenia w programie Microsoft Outlook i wiele innych.

### Nowe funkcje

* Rozpiętość wierszy i kolumn dla komórek tabeli jest teraz podawana w mowie i alfabecie Braille'a. (#2642)
* Polecenia nawigacji po tabelach NVDA są teraz obsługiwane w Google Docs (z włączonym trybem Braille'a). (#7946)
* Dodano możliwość czytania i nawigowania po tabelach w Kindle na PC. (#7977)
* Obsługa monitorów brajlowskich HumanWare BrailleNote touch i Brailliant BI 14 zarówno przez USB, jak i Bluetooth. (#6524)
* W systemie Windows 10 Fall Creators Update i nowszych NVDA może ogłaszać powiadomienia z aplikacji takich jak Kalkulator i Windows Store. (#7984)
* Nowe tabele tłumaczeń brajlowskich: litewski 8 punktów, ukraiński, mongolski klasa 2. (#7839)
* Dodano skrypt do raportowania informacji o formatowaniu tekstu w określonej komórce brajlowskiej. (#7106)
* Podczas aktualizacji NVDA możliwe jest teraz odłożenie instalacji aktualizacji na późniejszy moment. (#4263)
* Nowe języki: mongolski, szwajcarski niemiecki.
* Możesz teraz przełączać się między Control, Shift, Alt, Windows i NVDA za pomocą klawiatury brajlowskiej i łączyć te modyfikatory z wprowadzaniem brajlowskim (np. naciśnij control+s). (#7306)
 * Te nowe przełączniki modyfikatorów można przypisać za pomocą poleceń znajdujących się w sekcji Emulowane klawiatury systemowej w oknie dialogowym Gesty wprowadzania.
* Przywrócono obsługę wyświetlaczy Handy Tech Braillino i Modular (ze starym oprogramowaniem). (#8016)
* Data i godzina dla obsługiwanych urządzeń Handy Tech (takich jak Active Braille i Active Star) będą teraz automatycznie synchronizowane przez NVDA, gdy brak synchronizacji będzie trwały dłużej niż pięć sekund. (#8016)
* Można przypisać gest wejściowy, aby tymczasowo wyłączyć wszystkie wyzwalacze profilu konfiguracji. (#4935)

### Zmiany

* Kolumna stanu w menedżerze dodatków została zmieniona, aby wskazać, czy dodatek jest włączony czy wyłączony, a nie uruchomiony lub zawieszony. (#7929)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.5.0. (#7839)
* Nazwa litewskiej tablicy brajlowskiej została zmieniona na litewską z 6 kropkami, aby uniknąć pomyłek z nową tabelą z 8 kropkami. (#7839)
* Francuskie (Kanada) tabele oceny 1 i klasy 2 zostały usunięte. Zamiast tego zostaną użyte odpowiednio francuskie (ujednolicone) 6-punktowe tabele komputerowe w alfabecie Braille'a i Grade 2. (#7839)
* Dodatkowe przyciski przywoływania w monitorach brajlowskich Alva BC6, EuroBraille i Papenmeier teraz informują o formatowaniu tekstu pod komórką brajlowską tego przycisku. (#7106)
* Tabele brajlowskie z kontrakcjami automatycznie powrócą do trybu bez kontrakcji w przypadkach nieedytowalnych (np. kontrolki, w których nie ma kursora lub w trybie przeglądania). (#7306)
* NVDA jest teraz mniej szczegółowy, gdy termin lub przedział czasowy w kalendarzu Outlooka obejmuje cały dzień. (#7949)
* Wszystkie preferencje NVDA można teraz znaleźć w jednym oknie ustawień w menu NVDA -> Preferencje -> Ustawienia, zamiast rozsiane po wielu oknach dialogowych. (#577)
* Domyślny syntezator mowy podczas działania w systemie Windows 10 to teraz jedenPodstawowa mowa zamiast eSpeak. (#8176)

### Poprawki błędów

* NVDA nie czyta już aktywnych elementów sterujących na ekranie logowania do konta Microsoft w Ustawieniach po wprowadzeniu adresu e-mail. (#7997)
* NVDA nie czyta już strony po powrocie do poprzedniej strony w Microsoft Edge. (#7997)
* NVDA nie będzie już nieprawidłowo ogłaszać końcowego znaku kodu PIN logowania do systemu Windows 10 podczas odblokowywania komputera. (#7908)
* Etykiety pól wyboru i przycisków radiowych w przeglądarkach Chrome i Firefox nie są już zgłaszane dwukrotnie podczas wciskania Tab lub korzystania z szybkiej nawigacji w trybie przeglądania. (#7960)
* aria-current o wartości false zostanie ogłoszona jako "false" zamiast "true". (#7892).
* Funkcja Głosy OneCore systemu Windows nie ładuje się już, jeśli skonfigurowany głos został odinstalowany. (#7553)
* Zmiana głosów w Windows OneCore Voices jest teraz znacznie szybsza. (#7999)
* Poprawiono zniekształcone dane wyjściowe brajla dla kilku tabel brajlowskich, w tym wielkie znaki w duńskim brajlu z 8 kropkami. (#7526, #7693)
* NVDA może teraz zgłaszać więcej typów punktorów w programie Microsoft Word. (#6778)
* Naciśnięcie skryptu formatowania raportu nie powoduje już niepoprawnego przesuwania elementu reviewPosition, a zatem wielokrotne naciśnięcie go nie daje już różnych wyników. (#7869)
* Wprowadzanie brajlem nie pozwala już na używanie brajla z kontrakcjami w przypadkach, gdy nie jest on obsługiwany (np. całe słowa nie będą już wysyłane do systemu poza treścią tekstową i w trybie przeglądania). (#7306)
* Rozwiązano problemy ze stabilnością połączenia dla monitorów Braille'a Handy Tech Easy i Braille Wave. (#8016)
* W systemie Windows 8 i nowszych, NVDA nie będzie już informować o "nieznanym" po otwarciu menu szybkiego łącza (Windows + X) i wybraniu pozycji z tego menu. (#8137)
* Specyficzne dla modelu gesty do przycisków na wyświetlaczach Hims działają teraz zgodnie z reklamą w podręczniku użytkownika. (#8096)
* NVDA będzie teraz próbowało rozwiązać problemy z rejestracją COM systemu, powodując, że programy takie jak Firefox i Internet Explorer stają się niedostępne i zgłaszają "Nieznany" przez NVDA. (#2807)
* Usunięto błąd w Menedżerze zadań, który powodował, że NVDA nie pozwalała użytkownikom na dostęp do zawartości określonych szczegółów dotyczących procesów. (#8147)
* Nowsze głosy Microsoft SAPI5 nie powodują już opóźnień na końcu mowy, dzięki czemu nawigacja za pomocą tych głosów jest znacznie bardziej wydajna. (#8174)
* NVDA nie raportuje już (znaczników LTR i RTL) w alfabecie Braille'a ani mowy na znak podczas uzyskiwania dostępu do zegara w najnowszych wersjach systemu Windows. (#5729)
* Wykrywanie przewijania na wyświetlaczach Hims Smart Beetle po raz kolejny nie jest już zawodne. (#6086)
* W niektórych kontrolkach tekstowych, szczególnie w aplikacjach Delphi, informacje o edycji i nawigacji są teraz znacznie bardziej niezawodne. (#636, #8102)
* W systemie Windows 10 RS5 NVDA nie zgłasza już dodatkowych nadmiarowych informacji podczas przełączania zadań za pomocą alt+tab. (#8258)

### Zmiany dla deweloperów

* Informacje dla programistów dla obiektów UIA zawierają teraz listę dostępnych wzorców UIA. (#5712)
* Moduły aplikacji mogą teraz wymusić na niektórych oknach, aby zawsze korzystały z UIA, implementując metodę isGoodUIAWindow. (#7961)
* Ukryta flaga logiczna "outputPass1Only" w sekcji brajlowskiej konfiguracji została ponownie usunięta. Liblouis nie obsługuje już danych wyjściowych tylko z przepustką 1. (#7839)

## 2018.1.1

Jest to specjalna wersja NVDA, która usuwa błąd w sterowniku syntezatora mowy Onecore Windows Speech, który powodował, że mówił on z wyższym tonem i szybkością w systemie Windows 10 Redstone 4 (1803). (#8082)

## 2018.1

Najważniejsze cechy tego wydania to obsługa wykresów w programach Microsoft Word i PowerPoint, obsługa nowych monitorów brajlowskich, w tym Eurobraille i konwerter protokołu Optelec, ulepszona obsługa monitorów brajlowskich Hims i Optelec, poprawa wydajności przeglądarki Mozilla Firefox 58 i nowszych oraz wiele innych.

### Nowe funkcje

* Teraz możliwa jest interakcja z wykresami w programach Microsoft Word i Microsoft PowerPoint, podobnie jak w przypadku istniejącej obsługi wykresów w programie Microsoft Excel. (#7046)
 * W programie Microsoft Word: W trybie przeglądania przesuń kursor na osadzony wykres i naciśnij Enter, aby wejść z nim w interakcję.
 * W programie Microsoft PowerPoint podczas edytowania slajdu: przejdź Tab do obiektu wykresu i naciśnij Enter lub spację, aby wejść w interakcję z wykresem.
 * Aby zatrzymać interakcję z wykresem, naciśnij Escape.
* Nowy język: kirgiski.
* Dodano obsługę półki na książki VitalSource. (#7155)
* Dodano obsługę konwertera protokołu Optelec, urządzenia pozwalającego na korzystanie z monitorów Braille Voyager i Satellite za pomocą protokołu komunikacyjnego ALVA BC6. (#6731)
* Teraz możliwe jest korzystanie z wejścia brajlowskiego z monitorem brajlowskim ALVA 640 Comfort. (#7733)
 * Funkcja wprowadzania brajlowskiego NVDA może być używana z tymi, jak również innymi monitorami BC6 z oprogramowaniem układowym 3.0.0 i nowszym.
* Wczesne wsparcie dla Arkuszy Google z włączonym trybem Braille'a. (#7935)
* Obsługa monitorów brajlowskich Eurobraille Esys, Esytime i Iris. (#7488)

### Zmiany

* Sterowniki monitorów brajlowskich HIMS Braille Sense/Braille EDGE/Smart Beetle i Hims Sync zostały zastąpione jednym sterownikiem. Nowy sterownik zostanie automatycznie aktywowany dla byłych użytkowników sterownika syncBraille. (#7459)
 * Niektóre, w szczególności przewijania, zostały ponownie przypisane, aby były zgodne z konwencjami używanymi przez produkty Hims. Zapoznaj się z instrukcją obsługi, aby uzyskać więcej informacji.
* Podczas pisania za pomocą klawiatury ekranowej za pomocą interakcji dotykowej domyślnie musisz teraz dwukrotnie nacisnąć każdy w taki sam sposób, w jaki aktywujesz każdy inny element sterujący. (#7309)
 * Aby skorzystać z istniejącego trybu "pisania dotykowego", w którym wystarczy oderwać palec od, aby go aktywować, włącz tę opcję w nowym oknie dialogowym ustawień interakcji dotykowej, które znajduje się w menu Preferencje.
* Nie jest już konieczne wyraźne wiązanie brajla w celu skupienia lub przeglądania, ponieważ domyślnie dzieje się to automatycznie. (#2385)
 * Należy pamiętać, że automatyczne tethering z recenzją będzie miał miejsce tylko w przypadku korzystania z kursora recenzji lub polecenia nawigacji po obiektach. Przewijanie nie aktywuje tego nowego zachowania.

### Poprawki błędów

* Komunikaty, które można przeglądać, takie jak wyświetlanie bieżącego formatowania po dwukrotnym szybkim naciśnięciu NVDA+f, nie kończą się już niepowodzeniem, gdy NVDA jest zainstalowany na ścieżce ze znakami spoza ASCII. (#7474)
* Fokus jest teraz ponownie poprawnie przywracany po powrocie do Spotify z innej aplikacji. (#7689)
* W aktualizacji Windows 10 Fall Creaters Update NVDA nie aktualizuje się już, gdy kontrolowany dostęp do folderów jest włączony z Windows Defender Security Center. (#7696)
* Wykrywanie przewijania na wyświetlaczach Hims Smart Beetle nie jest już zawodne. (#6086)
* Nieznaczna poprawa wydajności podczas renderowania dużych ilości treści w przeglądarce Mozilla Firefox 58 i nowszych. (#7719)
* W programie Microsoft Outlook czytanie wiadomości e-mail zawierających tabele nie powoduje już błędów. (#6827)
* Gesty monitora brajlowskiego, które emulują modyfikatory klawiatury systemowej, mogą być teraz łączone z innymi emulowanymi klawiatury systemowej, jeśli jeden lub więcej z nich jest specyficznych dla modelu. (#7783)
* W przeglądarce Mozilla Firefox tryb przeglądania działa teraz poprawnie w wyskakujących okienkach utworzonych przez rozszerzenia takie jak LastPass i bitwarden. (#7809)
* NVDA nie zawiesza się już czasami przy każdej zmianie fokusu, jeśli Firefox lub Chrome przestały odpowiadać, na przykład z powodu zawieszenia lub awarii. (#7818)
* W klientach Twittera, takich jak Chicken Nugget, NVDA nie będzie już ignorować ostatnich 20 znaków z 280-znakowych tweetów podczas ich czytania. (#7828)
* NVDA używa teraz poprawnego języka podczas ogłaszania symboli, gdy zaznaczony jest tekst. (#7687)
* W najnowszych wersjach usługi Office 365 ponownie możliwe jest poruszanie się po wykresach programu Excel za pomocą strzałek. (#7046)
* W przypadku mowy i wyjścia brajlowskiego stany kontrolne będą teraz zawsze podawane w tej samej kolejności, niezależnie od tego, czy są dodatnie, czy negatywne. (#7076)
* W aplikacjach takich jak Windows 10 Mail, NVDA nie będzie już zawodzić w ogłaszaniu usuniętych znaków po naciśnięciu Backspace. (#7456)
* Wszystkie w monitorach Hims Braille Sense Polaris działają teraz zgodnie z oczekiwaniami. (#7865)
* NVDA nie uruchamia się już w systemie Windows 7, skarżąc się na wewnętrzną bibliotekę dll api-ms, gdy określona wersja pakietów redystrybucyjnych Visual Studio 2017 została zainstalowana przez inną aplikację. (#7975)

### Zmiany dla deweloperów

* Dodano ukrytą flagę logiczną do sekcji brajlowskiej w konfiguracji: "outputPass1Only". (#7301, #7693, #7702)
 * Ta flaga ma wartość domyślną true. Jeśli wartość jest fałszywa, do wyprowadzania alfabetu Braille'a zostaną użyte reguły wieloprzebiegowe liblouis.
* Nowy słownik (brajl. RENAMED_DRIVERS) został dodany, aby umożliwić płynne przejście dla użytkowników korzystających ze sterowników, które zostały zastąpione przez inne. (#7459)
* Zaktualizowano pakiet comtypes do wersji 1.1.3. (#7831)
* Zaimplementowano ogólny system w alfabecie Braille'a. BrailleDisplayDriver do obsługi monitorów, które wysyłają pakiety potwierdzenia/potwierdzenia. Zobacz sterownik monitora brajlowskiego handyTech jako przykład. (#7590, #7721)
* Nowa zmienna "isAppX" w module konfiguracyjnym może być używana do wykrywania, czy NVDA jest uruchomiona jako aplikacja Windows Desktop Bridge Store. (#7851)
* W przypadku implementacji dokumentów, takich jak NVDAObjects lub browseMode, które mają textInfo, istnieje teraz nowa klasa documentBase.documentWithTableNavigation, z której można dziedziczyć w celu uzyskania standardowych skryptów nawigacji po tabelach. Zapoznaj się z tą klasą, aby zobaczyć, które metody pomocnicze muszą być dostarczone przez implementację, aby nawigacja po tabelach działała. (#7849)
* Plik wsadowy scons radzi sobie teraz lepiej, gdy zainstalowany jest również Python 3, wykorzystując program uruchamiający do uruchamiania Pythona 2.7 32-bitowego. (#7541)
* hwIo.Hid pobiera teraz dodatkowy parametr wyłączny, który domyślnie ma wartość True. Jeśli ustawiona jest wartość False, inne aplikacje mogą komunikować się z urządzeniem, gdy jest ono podłączone do NVDA. (#7859)

## 2017.4

Najważniejsze cechy tej wersji obejmują wiele poprawek i ulepszeń obsługi sieci Web, w tym domyślny tryb przeglądania dla okien dialogowych sieci Web, lepsze raportowanie etykiet grup pól w trybie przeglądania, obsługę nowych technologii systemu Windows 10, takich jak Windows Defender Application Guard i Windows 10 na ARM64 oraz automatyczne raportowanie orientacji ekranu i stanu baterii.
Należy pamiętać, że ta wersja NVDA nie obsługuje już systemu Windows XP ani Windows Vista. Minimalnym wymaganiem dla NVDA jest teraz Windows 7 z dodatkiem Service Pack 1.

### Nowe funkcje

* W trybie przeglądania można teraz przeskakiwać obok/do początku punktów orientacyjnych za pomocą poleceń przeskocz do końca/początku kontenera (przecinek/shift+przecinek). (#5482)
* W przeglądarkach Firefox, Chrome i Internet Explorer szybka nawigacja do edycji pól i pól formularzy obejmuje teraz edytowalną zawartość tekstu sformatowanego (tj. contentEditable). (#5534)
* W przeglądarkach internetowych Lista elementów może teraz zawierać listę pól formularzy i przycisków. (#588)
* Początkowa obsługa systemu Windows 10 w architekturze ARM64. (#7508)
* Wczesne wsparcie dla czytania i interaktywnej nawigacji po zawartości matematycznej dla książek Kindle z ułatwieniami dostępu do matematyki. (#7536)
* Dodano obsługę czytnika e-booków Azardi. (#5848)
* Informacje o wersji dodatków są teraz raportowane podczas aktualizacji. (#5324)
* Dodano nowe parametry wiersza poleceń, aby utworzyć przenośną kopię NVDA. (#6329)
* Obsługa przeglądarki Microsoft Edge działającej w ramach funkcji Windows Defender Application Guard w aktualizacji Windows 10 Fall Creators Update. (#7600)
* Jeśli działa na laptopie lub tablecie, NVDA będzie teraz raportować, kiedy ładowarka jest podłączona/odłączona i kiedy zmieni się orientacja ekranu. (#4574, #4612)
* Nowy język: macedoński.
* Nowe tabele tłumaczeń brajlowskich: chorwacki 1., wietnamski 1. (#7518, #7565)
* Dodano obsługę monitora brajlowskiego Actilino firmy Handy Tech. (#7590)
* Obsługiwane jest teraz wprowadzanie brajlowskie dla monitorów brajlowskich Handy Tech. (#7590)

### Zmiany

* Minimalnym obsługiwanym systemem operacyjnym dla NVDA jest teraz Windows 7 Service Pack 1 lub Windows Server 2008 R2 Service Pack 1. (#7546)
* Okna dialogowe w przeglądarkach Firefox i Chrome teraz automatycznie korzystają z trybu przeglądania, chyba że znajdują się w aplikacji internetowej. (#4493)
* W trybie przeglądania wciskanie Tab i przechodzenie za pomocą poleceń szybkiej nawigacji nie informuje już o wyskakiwaniu z kontenerów, takich jak listy i tabele, co sprawia, że nawigacja jest bardziej wydajna. (#2591)
* W trybie przeglądania w przeglądarkach Firefox i Chrome nazwy grup pól formularzy są teraz ogłaszane podczas przechodzenia do nich za pomocą szybkiej nawigacji lub podczas korzystania z Tab. (#3321)
* W trybie przeglądania polecenie szybkiej nawigacji dla obiektów osadzonych (o i shift+o) zawiera teraz elementy audio i wideo, a także elementy z aplikacją ról arii i oknem dialogowym. (#7239)
* Espeak-ng został zaktualizowany do wersji 1.49.2, rozwiązując niektóre problemy z tworzeniem kompilacji wydań. (#7385, #7583)
* Przy trzeciej aktywacji polecenia 'odczyt paska stanu' jego zawartość jest kopiowana do schowka. (#1785)
* Przypisując gesty do na monitorze Baum, można je ograniczyć do modelu używanego monitora brajlowskiego (np. VarioUltra lub Pronto). (#7517)
* Skrót klawiszowy dla pola filtru na liście elementów w trybie przeglądania został zmieniony z alt+f na alt+e. (#7569)
* Dodano niepowiązane polecenie dla trybu przeglądania, aby przełączać dołączanie tabel układu w locie. To polecenie można znaleźć w kategorii Tryb przeglądania w oknie dialogowym Gesty wprowadzania. (#7634)
* Zaktualizowano translator brajlowski liblouis do wersji 3.3.0. (#7565)
* Skrót klawiszowy przycisku radiowego wyrażenia regularnego w oknie dialogowym słownika został zmieniony z alt+r na alt+e. (#6782)
* Pliki słowników głosowych są teraz wersjonowane i zostały przeniesione do katalogu "speechDicts/voiceDicts.v1". (#7592)
* Modyfikacje wersjonowanych plików (konfiguracja użytkownika, słowniki głosowe) nie są już zapisywane, gdy NVDA jest uruchamiany z programu uruchamiającego. (#7688)
* Monitory brajlowskie Braillino, Bookworm i Modular (ze starym oprogramowaniem) firmy Handy Tech nie są już obsługiwane po wyjęciu z pudełka. Zainstaluj uniwersalny sterownik Handy Tech i dodatek NVDA, aby korzystać z tych wyświetlaczy. (#7590)

### Poprawki błędów

* Łącza są teraz oznaczone alfabetem Braille'a w aplikacjach takich jak Microsoft Word. (#6780)
* NVDA nie staje się już zauważalnie wolniejsza, gdy otwartych jest wiele kart w przeglądarkach Firefox lub Chrome. (#3138)
* Routing kursora dla monitora brajlowskiego MDV Lilli nie przesuwa już nieprawidłowo jednej komórki brajlowskiej przed miejscem, w którym powinna się znajdować. (#7469)
* W programie Internet Explorer i innych dokumentach MSHTML atrybut HTML5 required jest teraz obsługiwany w celu wskazania wymaganego stanu pola formularza. (#7321)
* Monitory brajlowskie są teraz aktualizowane podczas wpisywania znaków arabskich w dokumencie WordPad wyrównanym do lewej. (#511)
* Dostępne etykiety kontrolek w przeglądarce Mozilla Firefox są teraz łatwiej zgłaszane w trybie przeglądania, gdy etykieta sama w sobie nie jest wyświetlana. (#4773)
* W systemie Windows 10 Creaters Update, NVDA może ponownie uzyskać dostęp do Firefoksa po ponownym uruchomieniu NVDA. (#7269)
* Po ponownym uruchomieniu NVDA z fokusem Mozilla Firefox, tryb przeglądania będzie ponownie dostępny, chociaż może być konieczne naciśnięcie Alt+Tab i z powrotem. (#5758)
* Teraz można uzyskać dostęp do treści matematycznych w Google Chrome w systemie bez zainstalowanej przeglądarki Mozilla Firefox. (#7308)
* System operacyjny i inne aplikacje powinny być bardziej stabilne bezpośrednio po zainstalowaniu NVDA przed ponownym uruchomieniem, w porównaniu z instalacjami poprzednich wersji NVDA. (#7563)
* Podczas korzystania z polecenia rozpoznawania treści (np. NVDA+r), NVDA zgłasza teraz komunikat o błędzie zamiast nic, jeśli obiekt nawigatora zniknął. (#7567)
* Poprawiono funkcję przewijania do tyłu dla monitorów brajlowskich Freedom Scientific zawierających lewy bumper barwy. (#7713)

### Zmiany dla deweloperów

* "Scons tests" sprawdza teraz, czy ciągi znaków do przetłumaczenia mają komentarze tłumacza. Możesz również uruchomić to samodzielnie za pomocą "scons checkPot". (#7492)
* Dostępny jest teraz nowy moduł extensionPoints, który zapewnia ogólną strukturę umożliwiającą rozszerzalność kodu w określonych punktach kodu. Dzięki temu zainteresowane strony mogą zarejestrować się, aby otrzymywać powiadomienia o wystąpieniu jakiejś akcji (extensionPoints.Action), modyfikować określony rodzaj danych (extensionPoints.Filter) lub uczestniczyć w podejmowaniu decyzji, czy coś zostanie zrobione (extensionPoints.Decider). (#3393)
* Teraz możesz zarejestrować się, aby otrzymywać powiadomienia o przełącznikach profilu konfiguracji za pośrednictwem config.configProfileSwitched Action. (#3393)
* Gesty monitora brajlowskiego, które emulują modyfikatory klawiatury systemowej (takie jak control i alt), mogą być teraz łączone z innymi emulowanymi klawiatury systemowej bez wyraźnej definicji. (#6213)
 * Na przykład, jeśli masz na wyświetlaczu powiązany z alt, a inny wyświetlacza z downArrow, połączenie tych spowoduje emulację alt+downArrow.
* Alfabet Braille'a. Klasa BrailleDisplayGesture ma teraz dodatkową właściwość modelu. Jeśli jest dostępny, naciśnięcie spowoduje wygenerowanie dodatkowego, specyficznego dla modelu identyfikatora gestu. Dzięki temu użytkownik może wiązać gesty ograniczone do określonego modelu monitora brajlowskiego.
 * Zobacz sterownik baum jako przykład tej nowej funkcji.
* NVDA jest teraz skompilowany przy użyciu programu Visual Studio 2017 i zestawu Windows 10 SDK. (#7568)

## 2017.3

Najważniejsze cechy tego wydania obejmują wprowadzanie kontrowanych głosów Braille'a, obsługę nowych głosów Windows OneCore dostępnych w systemie Windows 10, wbudowaną obsługę OCR systemu Windows 10 oraz wiele istotnych ulepszeń dotyczących alfabetu Braille'a i Internetu.

### Nowe funkcje

* Dodano ustawienie brajlowskie "pokazuj wiadomości w nieskończoność". (#6669)
* Na listach wiadomości programu Microsoft Outlook, NVDA informuje teraz, czy wiadomość jest oflagowana. (#6374)
* W programie Microsoft PowerPoint podczas edycji slajdu podawany jest teraz dokładny typ kształtu (np. trójkąt, okrąg, wideo lub strzałka), a nie tylko "kształt". (#7111)
* Treści matematyczne (dostarczane jako MathML) są teraz obsługiwane w przeglądarce Google Chrome. (#7184)
* NVDA może teraz mówić przy użyciu nowych głosów Windows OneCore (znanych również jako głosy Microsoft Mobile) zawartych w systemie Windows 10. Dostęp do nich można uzyskać, wybierając głosy Windows OneCore w oknie dialogowym syntezatora NVDA. (#6159)
* Pliki konfiguracyjne użytkownika NVDA mogą być teraz przechowywane w lokalnym folderze danych aplikacji użytkownika. Jest to możliwe za pomocą ustawienia w rejestrze. Aby uzyskać więcej informacji, zobacz "Parametry całego systemu" w Podręczniku użytkownika. (#6812)
* W przeglądarkach internetowych, NVDA raportuje teraz wartości symboli zastępczych dla pól (w szczególności aria-placeholder jest teraz obsługiwany). (#7004)
* W trybie przeglądania w programie Microsoft Word można teraz przechodzić do błędów pisowni za pomocą szybkiej nawigacji (w i shift+w). (#6942)
* Dodano obsługę kontrolki Selektor daty, która znajduje się w oknach dialogowych terminów programu Microsoft Outlook. (#7217)
* Aktualnie wybrana sugestia jest teraz raportowana w polach Poczta do/cc systemu Windows 10 i w polu wyszukiwania Ustawienia systemu Windows 10. (#6241)
* Odtwarzany jest teraz dźwięk wskazujący pojawienie się sugestii w niektórych polach wyszukiwania w systemie Windows 10 (np. ekran startowy, wyszukiwanie ustawień, pola poczty do/DW systemu Windows 10). (#6241)
* NVDA teraz automatycznie raportuje powiadomienia w programie Skype dla firm Desktop, na przykład gdy ktoś rozpoczyna z Tobą rozmowę. (#7281)
* NVDA teraz automatycznie raportuje przychodzące wiadomości czatu podczas konwersacji w programie Skype dla firm. (#7286)
* NVDA teraz automatycznie zgłasza powiadomienia w Microsoft Edge, na przykład o rozpoczęciu pobierania. (#7281)
* Możesz teraz pisać zarówno z kontrakcjami, jak i bez nich na monitorze brajlowskim z klawiaturą brajlowską. Szczegółowe informacje można znaleźć w rozdziale Wprowadzanie brajlowskie w Podręczniku użytkownika. (#2439)
* Możesz teraz wprowadzać znaki brajlowskie Unicode z klawiatury brajlowskiej na monitorze brajlowskim, wybierając opcję Braille Unicode jako tabelę wejściową w ustawieniach brajla. (#6449)
* Dodano obsługę monitora brajlowskiego SuperBraille używanego na Tajwanie. (#7352)
* Nowe tabele tłumaczeń brajlowskich: duński 8-punktowy komputerowy brajl, litewski, perski 8-punktowy alfabet komputerowy Braille'a, perski stopień 1, słoweński 8-punktowy komputerowy brajl komputerowy. (#6188, #6550, #6773, #7367)
* Ulepszono komputerową tabelę brajlowską w języku angielskim (USA) z 8 punktami, w tym obsługę punktorów, znaku euro i liter akcentowanych. (#6836)
* NVDA może teraz korzystać z funkcji OCR zawartej w systemie Windows 10 do rozpoznawania tekstu obrazów lub niedostępnych aplikacji. (#7361)
 * Język można ustawić w nowym oknie dialogowym OCR systemu Windows 10 w preferencjach NVDA.
 * Aby rozpoznać zawartość bieżącego obiektu nawigatora, naciśnij NVDA+r.
 * Więcej informacji można znaleźć w sekcji Rozpoznawanie zawartości w Podręczniku użytkownika.
* Możesz teraz wybrać, jakie informacje kontekstowe mają być wyświetlane na monitorze brajlowskim, gdy obiekt jest aktywny, korzystając z nowego ustawienia "Prezentacja kontekstu ostrości" w oknie dialogowym Ustawienia brajla. (#217)
 * Na przykład opcje "Wypełnij ekran w celu zmiany kontekstu" i "Tylko podczas przewijania do tyłu" mogą sprawić, że praca z listami i menu będzie bardziej wydajna, ponieważ elementy nie będą stale zmieniać swojego położenia na wyświetlaczu.
 * Więcej informacji i przykładów można znaleźć w sekcji dotyczącej ustawienia "Prezentacja kontekstowa ostrości" w Podręczniku użytkownika.
* W Firefoksie i Chrome, NVDA obsługuje teraz złożone dynamiczne siatki, takie jak arkusze kalkulacyjne, w których tylko część treści może być załadowana lub wyświetlona (w szczególności atrybuty aria-rowcount, aria-colcount, aria-rowindex i aria-colindex wprowadzone w ARIA 1.1). (#7410)

### Zmiany

* Dodano nieprzypisane polecenie, aby ponownie uruchomić NVDA na żądanie. Można go znaleźć w kategorii Różne w oknie dialogowym Gesty wprowadzania. (#6396)
* Układ klawiatury można teraz ustawić w oknie dialogowym NVDA Welcome. (#6863)
* Wiele innych typów i stanów kontrolnych zostało skróconych do alfabetu Braille'a. Skrócono również punkty orientacyjne. Pełna lista znajduje się w sekcji "Typ kontrolki, stan i skróty punktów orientacyjnych" w alfabecie Braille'a w Podręczniku użytkownika. (#7188, #3975)
* Zaktualizowano eSpeak NG do wersji 1.49.1. (#7280)
* Listy tabel wyjściowych i wejściowych w oknie dialogowym Ustawienia brajla są teraz posortowane alfabetycznie. (#6113)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.2.0. (#6935)
* Domyślna tabela brajlowska to teraz Unified English Braille Code grade 1. (#6952)
* Domyślnie, NVDA pokazuje teraz tylko te części informacji kontekstowej, które uległy zmianie na monitorze brajlowskim, gdy obiekt staje się aktywny. (#217)
 * Wcześniej zawsze pokazywał jak najwięcej informacji kontekstowych, niezależnie od tego, czy wcześniej widziałeś te same informacje kontekstowe.
 * Możesz powrócić do starego zachowania, zmieniając nowe ustawienie "Prezentacja kontekstowa ostrości" w oknie dialogowym Ustawienia Braille'a na "Zawsze wypełniaj ekran".
* W przypadku korzystania z alfabetu Braille'a kursor może być skonfigurowany tak, aby miał inny kształt, gdy jest podłączony do fokusu lub recenzji. (#7122)
* Logo NVDA zostało zaktualizowane. Zaktualizowane logo NVDA to stylizowane połączenie liter NVDA w kolorze białym, na jednolitym fioletowym tle. Dzięki temu będzie widoczny na każdym kolorowym tle i wykorzystuje fiolet z logo NV Access. (#7446)

### Poprawki błędów

* Edytowalne elementy div w Chrome nie mają już etykiety zgłaszanej jako wartość w trybie przeglądania. (#7153)
* Naciśnięcie przycisku End w trybie przeglądania pustego dokumentu programu Microsoft Word nie powoduje już błędu w czasie wykonywania. (#7009)
* Tryb przeglądania jest teraz poprawnie obsługiwany w przeglądarce Microsoft Edge, w której dokumentowi przypisano określoną rolę ARIA dokumentu. (#6998)
* W trybie przeglądania można teraz zaznaczyć lub odznaczyć do końca wiersza za pomocą shift+end, nawet jeśli daszek znajduje się na ostatnim znaku wiersza. (#7157)
* Jeśli okno dialogowe zawiera pasek postępu, tekst okna dialogowego jest teraz aktualizowany w alfabecie Braille'a, gdy pasek postępu ulega zmianie. Oznacza to na przykład, że pozostały czas można teraz odczytać w oknie dialogowym NVDA "Pobieranie aktualizacji". (#6862)
* NVDA ogłosi teraz zmiany wyboru dla niektórych pól kombi systemu Windows 10, takich jak Autoodtwarzanie w Ustawieniach. (#6337).
* Bezsensowne informacje nie są już ogłaszane podczas przechodzenia do okien dialogowych tworzenia spotkania/terminu w programie Microsoft Outlook. (#7216)
* Sygnał dźwiękowy dla nieokreślonych okien dialogowych paska postępu, takich jak sprawdzanie aktualizacji, tylko wtedy, gdy dane wyjściowe paska postępu są skonfigurowane tak, aby zawierały sygnały dźwiękowe. (#6759)
* W programach Microsoft Excel 2003 i 2007 komórki są ponownie raportowane podczas umieszczania strzałek w arkuszu. (#7243)
* W aktualizacji Windows 10 Creators Update i nowszych tryb przeglądania jest ponownie automatycznie włączany podczas czytania wiadomości e-mail w programie Poczta systemu Windows 10. (#7289)
* Na większości monitorów brajlowskich z klawiaturą brajlowską punkt 7 wymazuje ostatnio wprowadzoną komórkę lub znak brajlowski, a punkt 8 naciska Enter. (#6054)
* W edytowalnym tekście, podczas przesuwania kursora (np. za pomocą kursora lub Backspace), głosowe sprzężenie zwrotne NVDA jest teraz w wielu przypadkach dokładniejsze, szczególnie w Chrome i aplikacjach terminalowych. (#6424)
* Zawartość edytora podpisów w programie Microsoft Outlook 2016 można teraz odczytać. (#7253)
* W aplikacjach Java Swing NVDA nie powoduje już czasami awarii aplikacji podczas nawigowania po tabelach. (#6992)
* W aktualizacji Windows 10 Creators Update NVDA nie będzie już wielokrotnie ogłaszać wyskakujących powiadomień. (#7128)
* W menu Start w systemie Windows 10 naciśnięcie Enter w celu zamknięcia menu Start po tym, jak wyszukiwanie nie powoduje już, że NVDA ogłasza tekst wyszukiwania. (#7370)
* Szybka nawigacja do nagłówków w przeglądarce Microsoft Edge jest teraz znacznie szybsza. (#7343)
* W przeglądarce Microsoft Edge nawigacja w trybie przeglądania nie pomija już dużych części niektórych stron internetowych, takich jak motyw Wordpress 2015. (#7143)
* W przeglądarce Microsoft Edge punkty orientacyjne są poprawnie zlokalizowane w językach innych niż angielski. (#7328)
* Pismo Braille'a teraz poprawnie podąża za zaznaczeniem podczas zaznaczania tekstu poza szerokością wyświetlacza. Na przykład, jeśli zaznaczysz wiele wierszy za pomocą shift+strzałka w dół, pismo Braille'a pokaże teraz ostatnią zaznaczoną linię. (#5770)
* W Firefoksie, NVDA nie zgłasza już kilka razy fałszywie "section" podczas otwierania szczegółów tweeta na twitter.com. (#5741)
* Polecenia nawigacji po tabelach układu nie są już dostępne dla tabel układu w trybie przeglądania, chyba że jest włączone raportowanie tabel układu. (#7382)
* W przeglądarkach Firefox i Chrome polecenia nawigacji po tabelach w trybie przeglądania pomijają teraz ukryte komórki tabeli. (#6652, #5655)

### Zmiany dla deweloperów

* Sygnatury czasowe w dzienniku obejmują teraz milisekundy. (#7163)
* NVDA musi być teraz skompilowany za pomocą programu Visual Studio Community 2015. Program Visual Studio Express nie jest już obsługiwany. (#7110)
 * Narzędzia systemu Windows 10 i zestaw SDK są teraz również wymagane, które można włączyć podczas instalowania programu Visual Studio.
 * Aby uzyskać dodatkowe informacje, zobacz sekcję Zainstalowane zależności w pliku readme.
* Obsługa aparatów rozpoznawania treści, takich jak OCR i narzędzia do opisu obrazów, może być łatwo zaimplementowana za pomocą nowego pakietu contentRecog. (#7361)
* Pakiet json języka Python jest teraz dołączany do kompilacji binarnych NVDA. (#3050)

## 2017.2

Najważniejsze cechy tej wersji obejmują pełną obsługę wyciszania dźwięku w aktualizacji Windows 10 Creators Update; Poprawki kilku problemów z zaznaczaniem w trybie przeglądania, w tym problemów z zaznaczaniem wszystkiego; znaczące ulepszenia w obsłudze przeglądarki Microsoft Edge; oraz ulepszenia w sieci, takie jak wskazanie elementów oznaczonych jako aktualne (za pomocą aria-current).

### Nowe funkcje

* Informacje o obramowaniu komórki można teraz zgłaszać w programie Microsoft Excel przy użyciu NVDA+f. (#3044)
* W przeglądarkach internetowych NVDA wskazuje teraz, kiedy element został oznaczony jako bieżący (w szczególności za pomocą atrybutu aria-current). (#6358)
* Automatyczne przełączanie języka jest teraz obsługiwane w przeglądarce Microsoft Edge. (#6852)
* Dodano obsługę kalkulatora systemu Windows w systemie Windows 10 Enterprise LTSB (Long-Term Servicing Branch) i Server. (#6914)
* Trzykrotne wykonanie polecenia przeczytaj bieżący wiersz powoduje szybkie przeliterowanie wiersza z opisami znaków. (#6893)
* Nowy język: birmański.
* Strzałki w górę i w dół Unicode oraz symbole ułamków są teraz odczytywane poprawnie. (#3805)

### Zmiany

* Podczas nawigacji za pomocą prostego przeglądu w aplikacjach korzystających z automatyzacji interfejsu użytkownika więcej obcych obiektów jest teraz ignorowanych, co ułatwia nawigację. (#6948, #6950)

### Poprawki błędów

* Elementy menu strony internetowej mogą być teraz aktywowane w trybie przeglądania. (#6735)
* Naciśnięcie Escape, gdy aktywne jest okno dialogowe profilu konfiguracji "Potwierdź usunięcie", powoduje teraz zamknięcie okna dialogowego. (#6851)
* Naprawiono niektóre awarie w przeglądarce Mozilla Firefox i innych aplikacjach Gecko, w których włączona jest funkcja wielu procesów. (#6885)
* Raportowanie koloru tła w przeglądzie ekranu jest teraz dokładniejsze, gdy tekst został narysowany z przezroczystym tłem. (#6467)
* Ulepszona obsługa opisów formantów udostępnianych na stronach internetowych w programie Internet Explorer 11 (w szczególności obsługa aria-describedby w ramkach iframe i gdy podano wiele identyfikatorów). (#5784)
* W aktualizacji Windows 10 Creators Update wyciszanie dźwięku NVDA ponownie działa tak, jak w poprzednich wersjach systemu Windows; tj. Kaczka z mową i dźwiękami, zawsze kaczka i bez kaczenia są dostępne. (#6933)
* NVDA nie będzie już błądzić w nawigowaniu lub zgłaszaniu pewnych kontrolek (UIA), w których skrót klawiaturowy nie jest zdefiniowany. (#6779)
* Dwie puste spacje nie są już dodawane w informacjach o skrótach klawiaturowych dla niektórych kontrolek (UIA). (#6790)
* Niektóre kombinacje na wyświetlaczach HIMS (np. spacja+kropka4) nie zawodzą już sporadycznie. (#3157)
* Naprawiono problem występujący podczas otwierania portu szeregowego w systemach używających niektórych języków innych niż angielski, co w niektórych przypadkach powodowało niepowodzenie połączenia z monitorami brajlowskimi. (#6845)
* Zmniejszono prawdopodobieństwo uszkodzenia pliku konfiguracyjnego podczas zamykania systemu Windows. Pliki konfiguracyjne są teraz zapisywane w pliku tymczasowym przed zastąpieniem rzeczywistego pliku konfiguracyjnego. (#3165)
* Podczas szybkiego wykonywania polecenia szybkiego odczytu bieżącego wiersza dwa razy w celu przeliterowania wiersza, dla pisanych znaków używany jest teraz odpowiedni język. (#6726)
* Nawigacja po linii w przeglądarce Microsoft Edge jest teraz do trzech razy szybsza w aktualizacji Windows 10 Creators Update. (#6994)
* NVDA nie ogłasza już "grupowania Web Runtime" podczas skupiania się na dokumentach Microsoft Edge w aktualizacji Windows 10 Creators Update. (#6948)
* Wszystkie istniejące wersje SecureCRT są teraz obsługiwane. (#6302)
* Program Adobe Acrobat Reader nie ulega już awarii w niektórych dokumentach PDF (w szczególności tych, które zawierają puste atrybuty ActualText). (#7021, #7034)
* W trybie przeglądania w przeglądarce Microsoft Edge tabele interaktywne (siatki ARIA) nie są już pomijane podczas przechodzenia do tabel z t i shift+t. (#6977)
* W trybie przeglądania naciśnięcie shift+home po wybraniu opcji do przodu powoduje teraz usunięcie zaznaczenia na początku wiersza zgodnie z oczekiwaniami. (#5746)
* W trybie przeglądania zaznaczanie wszystkiego (control+a) nie powoduje już niepowodzenia w zaznaczaniu całego tekstu, jeśli daszek nie znajduje się na początku tekstu. (#6909)
* Naprawiono kilka innych rzadkich problemów z zaznaczaniem w trybie przeglądania. (#7131)

### Zmiany dla deweloperów

* Argumenty wiersza poleceń są teraz przetwarzane za pomocą modułu argparse Pythona, a nie optparse. Pozwala to na wyłączną obsługę niektórych opcji, takich jak -r i -q. (#6865)
* core.callLater teraz kolejkuje wywołanie zwrotne do głównej kolejki NVDA po podanym opóźnieniu, zamiast budzić rdzeń i wykonywać go bezpośrednio. Zapobiega to możliwym zawieszaniu się gry spowodowanym przypadkowym przejściem rdzenia w stan uśpienia po przetworzeniu wywołania zwrotnego, w trakcie wywołania modalnego, takiego jak odtworzenie okna komunikatu. (#6797)
* Właściwość InputGesture.identifiers została zmieniona w taki sposób, że nie jest już znormalizowana. (#6945)
 * Podklasy nie muszą już normalizować identyfikatorów przed zwróceniem ich z tej właściwości.
 * Jeśli chcesz znormalizować identyfikatory, istnieje teraz właściwość InputGesture.normalizedIdentifiers, która normalizuje identyfikatory zwracane przez właściwość identifiers.
* Właściwość InputGesture.logIdentifier jest teraz przestarzała. Zamiast tego obiekty wywołujące powinny używać InputGesture.identifiers[0]. (#6945)
* Usunięto niektóre przestarzałe kody:
 * – Mowa. REASON_*': zamiast tego należy użyć 'controlTypes.REASON_*'. (#6846)
 * 'i18nName' dla ustawień syntezatora: zamiast tego należy użyć 'displayName' i 'displayNameWithAccelerator'. (#6846, #5185)
 * 'config.validateConfig'. (#6846, #667)
 * 'config.save': Zamiast tego należy użyć 'config.conf.save'. (#6846, #667)
* Lista uzupełnień w menu kontekstowym autouzupełniania konsoli języka Python nie pokazuje już żadnej ścieżki obiektu prowadzącej do ukończenia ostatniego symbolu. (#7023)
* Obecnie istnieje framework do testów jednostkowych dla NVDA. (#7026)
 * Testy jednostkowe i infrastruktura znajdują się w katalogu tests/unit. Aby uzyskać szczegółowe informacje, zobacz docstring w pliku tests\unit\init.py.
 * Testy można uruchamiać za pomocą "scons tests". Szczegółowe informacje można znaleźć w sekcji "Uruchamianie testów" w readme.md.
 * Jeśli przesyłasz żądanie ściągnięcia dla NVDA, powinieneś najpierw uruchomić testy i upewnić się, że zakończą się pomyślnie.

## 2017.1

Najważniejsze cechy tego wydania obejmują raportowanie sekcji i kolumn tekstowych w programie Microsoft Word; Obsługa czytania, nawigacji i dodawania adnotacji do książek w Kindle na PC; i ulepszoną obsługę przeglądarki Microsoft Edge.

### Nowe funkcje

* W programie Microsoft Word można teraz raportować typy podziałów sekcji i numery sekcji. Jest to możliwe za pomocą opcji "Numery stron raportu" w oknie dialogowym Formatowanie dokumentu. (#5946)
* W programie Microsoft Word można teraz raportować kolumny tekstowe. Jest to możliwe za pomocą opcji 'Numery stron raportu' w oknie dialogowym formatowania dokumentu. (#5946)
* Automatyczne przełączanie języka jest teraz obsługiwane w programie WordPad. (#6555)
* Polecenie wyszukiwania NVDA (NVDA+control+f) jest teraz obsługiwane w trybie przeglądania w przeglądarce Microsoft Edge. (#6580)
* Szybka nawigacja po przyciskach w trybie przeglądania (b i shift+b) jest teraz obsługiwana w przeglądarce Microsoft Edge. (#6577)
* Podczas kopiowania arkusza w programie Microsoft Excel zapamiętywane są nagłówki kolumn i wierszy. (#6628)
* Obsługa czytania i nawigacji po książkach w Kindle na PC w wersji 1.19, w tym dostęp do linków, przypisów, grafiki, podświetlonego tekstu i notatek użytkownika. Więcej informacji można znaleźć w sekcji Kindle dla komputerów PC w Podręczniku użytkownika NVDA. (#6247, #6638)
* Nawigacja po tabelach w trybie przeglądania jest teraz obsługiwana w przeglądarce Microsoft Edge. (#6594)
* W programie Microsoft Excel polecenie lokalizacji kursora przeglądu raportu (pulpit: NVDA+numpadDelete, laptop: NVDA+delete) podaje teraz nazwę arkusza roboczego i lokalizację komórki. (#6613)
* Dodano opcję do okna dialogowego wyjścia, aby ponownie uruchomić z rejestrowaniem na poziomie debugowania. (#6689)

### Zmiany

* Minimalna częstotliwość kursora brajlowskiego wynosi teraz 200 ms. Jeśli wcześniej była ustawiona na niższą, zostanie zwiększona do 200 ms. (#6470)
* Do okna dialogowego ustawień brajla dodano pole wyboru, które umożliwia włączanie/wyłączanie kursora brajlowskiego. Poprzednio do tego celu używano wartości zero. (#6470)
* Zaktualizowano eSpeak NG (commit e095f008, 10 stycznia 2017 r.). (#6717)
* Ze względu na zmiany w aktualizacji Windows 10 Creators Update, tryb "Zawsze się wyciszaj" nie jest już dostępny w ustawieniach wyciszania dźwięku NVDA. Jest nadal dostępny w starszych wersjach systemu Windows 10. (#6684)
* Ze względu na zmiany w aktualizacji Windows 10 Creators Update, tryb "Duck podczas wyprowadzania mowy i dźwięków" nie może już zapewnić, że dźwięk został całkowicie wyciszony przed rozpoczęciem mówienia, ani nie utrzyma dźwięku wystarczająco długo po mówieniu, aby zapobiec podskakiwaniu głośności rappida. Te zmiany nie mają wpływu na starsze wersje systemu Windows 10. (#6684)

### Poprawki błędów

* Naprawiono zawieszanie się programu Microsoft Word podczas przechodzenia według akapitu przez duży dokument w trybie przeglądania. (#6368)
* Tabele w programie Microsoft Word, które zostały skopiowane z programu Microsoft Excel, nie są już drzewiaste jako tabele układu i dlatego nie są już ignorowane. (#5927)
* Podczas próby pisania w programie Microsoft Excel w widoku chronionym, NVDA wydaje teraz dźwięk, a nie wypowiada znaki, które w rzeczywistości nie zostały wpisane. (#6570)
* Naciśnięcie Escape w programie Microsoft Excel nie powoduje już nieprawidłowego przełączenia w tryb przeglądania, chyba że użytkownik wcześniej przełączył się do trybu przeglądania jawnie za pomocą NVDA+spacja, a następnie przeszedł do trybu aktywnego dostępu, naciskając Enter w polu formularza. (#6569)
* NVDA nie zawiesza się już w arkuszach kalkulacyjnych Microsoft Excel, w których scalany jest cały wiersz lub kolumna. (#6216)
* Raportowanie przyciętego/przepełnionego tekstu w komórkach programu Microsoft Excel powinno być teraz dokładniejsze. (#6472)
* NVDA teraz informuje, kiedy pole wyboru jest tylko do odczytu. (#6563)
* Program uruchamiający NVDA nie będzie już wyświetlał okna dialogowego z ostrzeżeniem, gdy nie będzie mógł odtworzyć dźwięku logo z powodu braku dostępnego urządzenia audio. (#6289)
* Formanty na wstążce programu Microsoft Excel, które są niedostępne, są teraz zgłaszane jako takie. (#6430)
* NVDA nie będzie już ogłaszać "okienka" podczas minimalizowania okien. (#6671)
* Wpisywane znaki są teraz wypowiadane w aplikacjach platformy uniwersalnej systemu Windows (UWP) (w tym w przeglądarce Microsoft Edge) w aktualizacji Windows 10 Creators Update. (#6017)
* Śledzenie myszy działa teraz na wszystkich ekranach na komputerach z wieloma monitorami. (#6598)
* NVDA nie staje się już bezużyteczne po wyjściu z programu Windows Media Player, gdy jest skupiony na suwaku. (#5467)

### Zmiany dla deweloperów

* Profile i pliki konfiguracyjne są teraz automatycznie uaktualniane, aby spełnić wymagania modyfikacji schematu. Jeśli wystąpi błąd podczas aktualizacji, zostanie wyświetlone powiadomienie, konfiguracja zostanie zresetowana, a stary plik konfiguracyjny będzie dostępny w dzienniku NVDA na poziomie "Info". (#6470)

## 2016.4

Najważniejsze cechy tej wersji obejmują ulepszoną obsługę przeglądarki Microsoft Edge; tryb przeglądania w aplikacji Poczta systemu Windows 10; oraz znaczące ulepszenia okien dialogowych NVDA.

### Nowe funkcje

* NVDA może teraz wskazywać wcięcie linii za pomocą tonów. Można to skonfigurować za pomocą pola kombi "Raportowanie wcięć linii" w oknie dialogowym preferencji formatowania dokumentu NVDA. (#5906)
* Obsługa monitora brajlowskiego Orbit Reader 20. (#6007)
* Dodano opcję otwierania okna przeglądarki mowy podczas uruchamiania. Można to włączyć za pomocą pola wyboru w oknie przeglądarki mowy. (#5050)
* Po ponownym otwarciu okna przeglądarki mowy lokalizacja i wymiary zostaną teraz przywrócone. (#5050)
* Pola odsyłaczy w programie Microsoft Word są teraz traktowane jak hiperłącza. Są one zgłaszane jako linki i mogą być aktywowane. (#6102)
* Obsługa monitorów brajlowskich Baum SuperVario2, Baum Vario 340 i HumanWare Brailliant2. (#6116)
* Początkowa obsługa rocznicowej aktualizacji przeglądarki Microsoft Edge. (#6271)
* Tryb przeglądania jest teraz używany podczas czytania wiadomości e-mail w aplikacji pocztowej systemu Windows 10. (#6271)
* Nowy język: litewski.

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 3.0.0. Obejmuje to znaczące ulepszenia ujednoliconego alfabetu Braille'a w języku angielskim. (#6109, #4194, #6220, #6140)
* W Menedżerze dodatków przyciski Wyłącz dodatek i Włącz dodatek mają teraz skróty klawiaturowe (odpowiednio alt+d i alt+e). (#6388)
* Rozwiązano różne problemy z dopełnieniem i wyrównaniem w oknach dialogowych NVDA. (#6317, #5548, #6342, #6343, #6349)
* Okno dialogowe formatowania dokumentu zostało dostosowane tak, aby zawartość się przewijała. (#6348)
* Dostosowano układ okna dialogowego wymowy symboli tak, aby lista symboli była używana na całej szerokości okna dialogowego. (#6101)
* W trybie przeglądania w przeglądarkach internetowych jednoliterowe polecenia nawigacyjne pola edycji (e i shift+e) oraz pola formularza (f i shift+f) mogą być teraz używane do przechodzenia do pól edycji tylko do odczytu. (#4164)
* W ustawieniach formatowania dokumentów NVDA, nazwa "Ogłaszaj zmiany formatowania po kursorze" została zmieniona na "Formatowanie raportu zmienia się po kursorze", ponieważ ma to wpływ zarówno na alfabet Braille'a, jak i mowę. (#6336)
* Dostosowano wygląd okna dialogowego "Witamy" NVDA. (#6350)
* Okna dialogowe NVDA mają teraz przyciski "ok" i "anuluj" wyrównane do prawej strony okna dialogowego. (#6333)
* Elementy sterujące wirowaniem są teraz używane w numerycznych polach wprowadzania, takich jak ustawienie "Procent zmiany wysokości kapitału" w oknie dialogowym ustawień głosowych. Możesz wprowadzić żądaną wartość lub użyć strzałek w górę i w dół, aby dostosować wartość. (#6099)
* Sposób, w jaki raportowane są ramki IFrames (dokumenty osadzone w dokumentach), został ujednolicony we wszystkich przeglądarkach internetowych. Ramki IFrames są teraz zgłaszane jako "ramka" w przeglądarce Firefox. (#6047)

### Poprawki błędów

* Naprawiono rzadki błąd podczas wychodzenia z NVDA, gdy przeglądarka mowy była otwarta. (#5050)
* Mapy obrazów są teraz renderowane zgodnie z oczekiwaniami w trybie przeglądania w przeglądarce Mozilla Firefox. (#6051)
* W oknie dialogowym słownika naciśnięcie Enter powoduje teraz zapisanie wszelkich wprowadzonych zmian i zamknięcie okna dialogowego. Wcześniej naciśnięcie Enter nic nie dało. (#6206)
* Wiadomości są teraz wyświetlane w alfabecie Braille'a po zmianie trybów wprowadzania dla metody wprowadzania (natywne wprowadzanie/alfanumeryczne, pełnowymiarowe/półkształtne itp.). (#5892, #5893)
* Po wyłączeniu, a następnie natychmiastowym ponownym włączeniu dodatku lub na odwrót, stan dodatku jest teraz poprawnie przywracany do poprzedniego stanu. (#6299)
* Podczas korzystania z programu Microsoft Word można teraz odczytywać pola numerów stron w nagłówkach. (#6004)
* Mysz może być teraz używana do przenoszenia fokusu między listą symboli a polami edycji w oknie dialogowym wymowy symboli. (#6312)
* W trybie przeglądania w programie Microsoft Word rozwiązano problem, który uniemożliwiał wyświetlanie listy elementów, gdy dokument zawiera nieprawidłowe hiperłącze. (#5886)
* Po zamknięciu za pomocą paska zadań lub skrótu alt+F4, pole wyboru przeglądarki mowy w menu NVDA będzie teraz odzwierciedlać rzeczywistą widoczność okna. (#6340)
* Polecenie przeładowania wtyczek nie powoduje już problemów z uruchomionymi profilami konfiguracyjnymi, nowymi dokumentami w przeglądarkach internetowych i przeglądaniem ekranu. (#2892, #5380)
* Na liście języków w oknie dialogowym Ustawienia ogólne NVDA, języki takie jak aragoński są teraz wyświetlane poprawnie w systemie Windows 10. (#6259)
* Emulowane klawiatury systemowej (np. przycisk na monitorze brajlowskim, który emuluje naciśnięcie Tab) są teraz prezentowane w skonfigurowanym języku NVDA w pomocy dla wprowadzania i oknie dialogowym Gesty wprowadzania. Wcześniej były one zawsze prezentowane w języku angielskim. (#6212)
* Zmiana języka NVDA (z okna dialogowego Ustawienia ogólne) nie ma teraz żadnego efektu, dopóki NVDA nie zostanie ponownie uruchomiona. (#4561)
* Nie można już pozostawić pustego pola Wzorzec dla nowego wpisu słownika mowy. (#6412)
* Naprawiono rzadki problem podczas skanowania w poszukiwaniu portów szeregowych w niektórych systemach, który sprawiał, że niektóre sterowniki monitorów brajlowskich nie nadawały się do użytku. (#6462)
* W programie Microsoft Word numerowane punktory w komórkach tabeli są teraz odczytywane podczas przechodzenia według komórek. (#6446)
* Możliwe jest teraz przypisywanie gestów do poleceń sterownika monitora brajlowskiego Handy Tech w oknie dialogowym Gesty wejściowe NVDA. (#6461)
* W programie Microsoft Excel naciśnięcie Enter lub NumpadEnter podczas nawigowania po arkuszu kalkulacyjnym teraz poprawnie informuje o nawigacji do następnego wiersza. (#6500)
* iTunes nie zawiesza się już na zawsze podczas korzystania z trybu przeglądania w iTunes Store, Apple Music itp. (#6502)
* Naprawiono awarie w 64-bitowych aplikacjach Mozilla i Chrome. (#6497)
* W Firefoksie z włączonym wieloprocesowym trybem przeglądania i edytowalnymi polami tekstowymi działają teraz poprawnie. (#6380)

### Zmiany dla deweloperów

* Teraz możliwe jest udostępnianie modułów aplikacji dla plików wykonywalnych zawierających kropkę (.) w swoich nazwach. Kropki są zastępowane podkreśleniami (_). (#5323)
* Nowy moduł gui.guiHelper zawiera narzędzia upraszczające tworzenie graficznych interfejsów użytkownika wxPython, w tym automatyczne zarządzanie odstępami. Ułatwia to lepszy wygląd i spójność wizualną, a także ułatwia tworzenie nowych graficznych interfejsów użytkownika dla niewidomych programistów. (#6287)

## 2016.3

Najważniejsze cechy tej wersji obejmują możliwość wyłączania poszczególnych dodatków; obsługa pól formularzy w programie Microsoft Excel; znaczące ulepszenia w raportowaniu kolorów; poprawki i ulepszenia związane z kilkoma monitorami brajlowskimi; oraz poprawki i ulepszenia obsługi programu Microsoft Word.

### Nowe funkcje

* Tryb przeglądania może być teraz używany do czytania dokumentów PDF w przeglądarce Microsoft Edge w rocznicowej aktualizacji systemu Windows 10. (#5740)
* Przekreślenie i podwójne przekreślenie są teraz zgłaszane w razie potrzeby w programie Microsoft Word. (#5800)
* W programie Microsoft Word tytuł tabeli jest teraz raportowany, jeśli został podany. Jeśli istnieje opis, można uzyskać do niego dostęp za pomocą polecenia open long description (NVDA+d) w trybie przeglądania. (#5943)
* W Microsoft Word, NVDA teraz raportuje informacje o pozycji podczas przenoszenia akapitów (alt+shift+strzałka w dół i alt+shift+strzałka w górę). (#5945)
* W programie Microsoft Word odstępy między wierszami są teraz raportowane za pomocą polecenia formatowania raportu NVDA, podczas zmiany go za pomocą różnych skrótów Microsoft Word oraz podczas przechodzenia do tekstu z różnymi odstępami między wierszami, jeśli interlinia raportu jest włączona w ustawieniach formatowania dokumentu NVDA. (#2961)
* W przeglądarce Internet Explorer elementy strukturalne HTML5 są teraz rozpoznawane. (#5591)
* Raportowanie komentarzy (np. w Microsoft Word) można teraz wyłączyć za pomocą pola wyboru Zgłoś komentarze w oknie dialogowym ustawień formatowania dokumentu NVDA. (#5108)
* Teraz można wyłączyć poszczególne dodatki w Menedżerze dodatków. (#3090)
* Dodano dodatkowe przypisania dla monitorów brajlowskich ALVA serii BC640/680. (#5206)
* Pojawiło się polecenie przesunięcia monitora brajlowskiego do bieżącego punktu skupienia. Obecnie tylko seria ALVA BC640/680 ma przypisany do tego polecenia, ale w razie potrzeby można go przypisać ręcznie do innych wyświetlaczy w oknie dialogowym Gesty wprowadzania. (#5250)
* W programie Microsoft Excel można teraz wchodzić w interakcje z polami formularzy. Przechodzisz do pól formularza za pomocą listy elementów lub nawigacji jednoliterowej w trybie przeglądania. (#4953)
* Teraz możesz przypisać gest wejściowy, aby przełączyć prosty tryb przeglądania za pomocą okna dialogowego Gesty wprowadzania. (#6173)

### Zmiany

* NVDA raportuje teraz kolory przy użyciu podstawowego, dobrze zrozumiałego zestawu 9 odcieni kolorów i 3 odcieni, z różnicami jasności i bladości. Dzieje się tak, a nie używanie bardziej subiektywnych i mniej zrozumiałych nazw kolorów. (#6029)
* Istniejące zachowanie NVDA+F9, a następnie NVDA+F10 zostało zmodyfikowane tak, aby zaznaczać tekst przy pierwszym naciśnięciu F10. Dwukrotne naciśnięcie F10 (w krótkich odstępach czasu) powoduje skopiowanie tekstu do schowka. (#4636)
* Zaktualizowano eSpeak NG do wersji Master 11b1a7b (22 czerwca 2016 r.). (#6037)

### Poprawki błędów

* W trybie przeglądania w programie Microsoft Word kopiowanie do schowka zachowuje teraz formatowanie. (#5956)
* W programie Microsoft Word, NVDA teraz poprawnie raportuje podczas korzystania z własnych poleceń nawigacji po tabelach Worda (alt+home, alt+end, alt+pageUp i alt+pageDown) oraz poleceń wyboru tabeli (do poleceń nawigacji dodano przesunięcie). (#5961)
* W oknach dialogowych Microsoft Word, nawigacja po obiektach NVDA została znacznie ulepszona. (#6036)
* W niektórych aplikacjach, takich jak Visual Studio 2015, skrótów (np. control+c dla kopiowania) są teraz raportowane zgodnie z oczekiwaniami. (#6021)
* Naprawiono rzadki problem podczas skanowania w poszukiwaniu portów szeregowych w niektórych systemach, który sprawiał, że niektóre sterowniki monitorów brajlowskich nie nadawały się do użytku. (#6015)
* Raportowanie kolorów w programie Microsoft Word jest teraz dokładniejsze, ponieważ uwzględniane są teraz zmiany w motywach pakietu Microsoft Office. (#5997)
* Tryb przeglądania dla przeglądarki Microsoft Edge i obsługa sugestii wyszukiwania w menu Start jest ponownie dostępna w kompilacjach systemu Windows 10 po kwietniu 2016 r. (#5955)
* W programie Microsoft Word automatyczne odczytywanie nagłówków tabeli działa lepiej, gdy mamy do czynienia ze scalonymi komórkami. (#5926)
* W aplikacji Poczta systemu Windows 10 NVDA nie odmawia już treści wiadomości. (#5635)
* Gdy funkcja Mów poleceń jest włączona, blokady, takie jak Caps Lock, nie są już ogłaszane dwukrotnie. (#5490)
* Okna dialogowe Kontroli konta użytkownika systemu Windows są ponownie poprawnie odczytywane w rocznicowej aktualizacji systemu Windows 10. (#5942)
* We wtyczce Web Conference (takiej jak używana w out-of-sight.net) NVDA nie emituje już sygnału dźwiękowego i nie informuje o aktualizacjach paska postępu związanych z wejściem mikrofonu. (#5888)
* Wykonanie polecenia Znajdź następny lub Znajdź poprzedni w trybie przeglądania spowoduje teraz poprawne wyszukiwanie z uwzględnieniem wielkości liter, jeśli w oryginalnym Znajdź rozróżniana była wielkość liter. (#5522)
* Podczas edytowania wpisów w słowniku są teraz przekazywane informacje zwrotne dotyczące nieprawidłowych wyrażeń regularnych. NVDA nie ulega już awarii, jeśli plik słownika zawiera nieprawidłowe wyrażenie regularne. (#4834)
* Jeśli NVDA nie jest w stanie komunikować się z monitorem brajlowskim (np. z powodu odłączenia), automatycznie wyłączy korzystanie z monitora. (#1555)
* W niektórych przypadkach nieznacznie poprawiono wydajność filtrowania na liście elementów trybu przeglądania. (#6126)
* W programie Microsoft Excel nazwy wzorców tła zgłaszane przez NVDA są teraz zgodne z tymi używanymi przez program Excel. (#6092)
* Ulepszona obsługa ekranu logowania do systemu Windows 10, w tym ogłaszanie alertów i aktywacja pola hasła za pomocą dotyku. (#6010)
* NVDA teraz poprawnie wykrywa dodatkowe przyciski przywoływania w monitorach brajlowskich ALVA serii BC640/680. (#5206)
* NVDA może ponownie zgłaszać wyskakujące powiadomienia systemu Windows w ostatnich kompilacjach systemu Windows 10. (#6096)
* NVDA nie przestaje już od czasu do czasu rozpoznawać naciśnięć na monitorach brajlowskich kompatybilnych z Baum i HumanWare Brailliant B. (#6035)
* Jeśli raportowanie numerów linii jest włączone w preferencjach formatowania dokumentów NVDA, numery linii są teraz wyświetlane na monitorze brajlowskim. (#5941)
* Gdy tryb mowy jest wyłączony, obiekty raportowania (takie jak naciśnięcie NVDA+tab w celu zgłoszenia fokusu) są teraz wyświetlane w przeglądarce mowy zgodnie z oczekiwaniami. (#6049)
* Na liście wiadomości programu Outlook 2016 skojarzone informacje o wersji roboczej nie są już raportowane. (#6219)
* W Google Chrome i przeglądarkach opartych na Chrome w języku innym niż angielski tryb przeglądania nie zawodzi już w wielu dokumentach. (#6249)

### Zmiany dla deweloperów

* Rejestrowanie informacji bezpośrednio z właściwości nie powoduje już cyklicznego wywoływania właściwości w kółko. (#6122)

## 2016.2.1

W tej wersji naprawiono awarie w programie Microsoft Word:

* NVDA nie powoduje już awarii programu Microsoft Word natychmiast po uruchomieniu w systemie Windows XP. (#6033)
* Usunięto zgłaszanie błędów gramatycznych, ponieważ powoduje to awarie w programie Microsoft Word. (#5954, #5877)

## 2016.2

Najważniejsze cechy tej wersji obejmują możliwość wskazywania błędów ortograficznych podczas pisania; obsługa zgłaszania błędów gramatycznych w programie Microsoft Word; oraz ulepszenia i poprawki obsługi pakietu Microsoft Office.

### Nowe funkcje

* W trybie przeglądania w programie Internet Explorer i innych kontrolkach MSHTML nawigacja za pomocą pierwszej litery w celu przechodzenia według adnotacji (a i shift+a) powoduje teraz przejście do wstawionego i usuniętego tekstu. (#5691)
* W programie Microsoft Excel NVDA informuje teraz o poziomie grupy komórek, a także o tym, czy jest ona zwinięta, czy rozwinięta. (#5690)
* Dwukrotne naciśnięcie polecenia formatowania tekstu raportu (NVDA+f) powoduje wyświetlenie informacji w trybie przeglądania, dzięki czemu można je przejrzeć. (#4908)
* W programie Microsoft Excel 2010 i nowszych wersjach jest teraz raportowane cieniowanie komórek i wypełnianie gradientem. Automatyczne raportowanie jest kontrolowane przez opcję Kolory raportu w preferencjach formatowania dokumentu NVDA. (#3683)
* Nowa tabela tłumaczeń brajlowskich: greka koine. (#5393)
* W przeglądarce dziennika możesz teraz zapisać dziennik za pomocą skrótu control+s. (#4532)
* Jeśli raportowanie błędów pisowni jest włączone i obsługiwane w kontrolce fokusu, NVDA odtworzy dźwięk, aby ostrzec Cię o błędzie pisowni popełnionym podczas pisania. Można to wyłączyć za pomocą nowej opcji "Odtwarzaj dźwięk dla błędów ortograficznych podczas pisania" w oknie dialogowym Ustawienia klawiatury NVDA. (#2024)
* Błędy gramatyczne są teraz zgłaszane w programie Microsoft Word. Można to wyłączyć za pomocą nowej opcji "Zgłoś błędy gramatyczne" w oknie dialogowym preferencji formatowania dokumentu NVDA. (#5877)

### Zmiany

* W trybie przeglądania i edytowalnych polach tekstowych, NVDA traktuje teraz numpadEnter tak samo, jak główny Enter. (#5385)
* NVDA przestawiła się na syntezator mowy eSpeak NG. (#5651)
* W programie Microsoft Excel NVDA nie ignoruje już nagłówka kolumny dla komórki, gdy między komórką a nagłówkiem znajduje się pusty wiersz. (#5396)
* W programie Microsoft Excel współrzędne są teraz ogłaszane przed nagłówkami, aby wyeliminować niejednoznaczność między nagłówkami a treścią. (#5396)

### Poprawki błędów

* W trybie przeglądania, podczas próby użycia nawigacji jednoliterowej w celu przejścia do elementu, który nie jest obsługiwany w dokumencie, NVDA zgłasza, że nie jest to obsługiwane, zamiast zgłaszać, że nie ma żadnego elementu w tym kierunku. (#5691)
* Podczas wyświetlania listy arkuszy na liście elementów w programie Microsoft Excel uwzględniane są teraz arkusze zawierające tylko wykresy. (#5698)
* NVDA nie zgłasza już zbędnych informacji podczas przełączania okien w aplikacji Java z wieloma oknami, takiej jak IntelliJ lub Android Studio. (#5732)
* W edytorach opartych na Scintilla, takich jak Notepad++, pismo Braille'a jest teraz poprawnie aktualizowane podczas przesuwania kursora za pomocą monitora brajlowskiego. (#5678)
* NVDA nie zawiesza się już czasami podczas włączania wyjścia brajlowskiego. (#4457)
* W programie Microsoft Word wcięcia akapitów są teraz zawsze podawane w wybranej przez użytkownika jednostce miary (np. centymetry lub cale). (#5804)
* Podczas korzystania z monitora brajlowskiego, wiele wiadomości NVDA, które wcześniej były tylko wypowiadane, jest teraz również brajlowanych. (#5557)
* W dostępnych aplikacjach Java poziom elementów widoku drzewa jest teraz raportowany. (#5766)
* Naprawiono awarie w Adobe Flash w Mozilla Firefox w niektórych przypadkach. (#5367)
* W Google Chrome i przeglądarkach opartych na Chrome dokumenty w oknach dialogowych lub aplikacjach można teraz czytać w trybie przeglądania. (#5818)
* W Google Chrome i przeglądarkach opartych na Chrome możesz teraz zmusić NVDA do przełączenia się w tryb przeglądania w oknach dialogowych lub aplikacjach internetowych. (#5818)
* W programie Internet Explorer i innych kontrolkach MSHTML przeniesienie fokusu do niektórych kontrolek (w szczególności tam, gdzie jest używana aria-activedescendant) nie jest już niepoprawnie przełączane do trybu przeglądania. Działo się tak na przykład podczas przechodzenia do sugestii w polach adresu podczas tworzenia wiadomości w Gmailu. (#5676)
* W programie Microsoft Word NVDA nie zawiesza się już w dużych tabelach, gdy włączone jest raportowanie nagłówków wierszy/kolumn tabeli. (#5878)
* W Microsoft Word NVDA nie zgłasza już błędnie tekstu z poziomem konspektu (ale nie wbudowanym stylem nagłówka) jako nagłówka. (#5186)
* W trybie przeglądania w programie Microsoft Word polecenia Przenieś poza koniec/do początku kontenera (przecinek i shift+przecinek) działają teraz dla tabel. (#5883)

### Zmiany dla deweloperów

* Komponenty C++ NVDA są teraz zbudowane przy użyciu Microsoft Visual Studio 2015. (#5592)
* Teraz możesz przedstawić użytkownikowi wiadomość tekstową lub HTML w trybie przeglądania za pomocą polecenia ui.browseableMessage. (#4908)
* W Podręczniku użytkownika, gdy polecenie <!-- KC:setting jest używane dla ustawienia, które ma wspólny klucz dla wszystkich układów, może być teraz umieszczony po dwukropku o pełnej szerokości (:), a także po zwykłym dwukropku (:). (#5739) -->

## 2016.1

Najważniejsze cechy tego wydania to możliwość opcjonalnego obniżenia głośności innych dźwięków; ulepszenia w zakresie wyjścia brajlowskiego i obsługi monitorów brajlowskich; kilka istotnych poprawek do obsługi pakietu Microsoft Office; i poprawki trybu przeglądania w iTunes.

### Nowe funkcje

* Nowe tabele tłumaczeń brajlowskich: polski 8-punktowy komputerowy brajl, mongolski. (#5537, #5574)
* Możesz wyłączyć kursor brajlowski i zmienić jego kształt, korzystając z nowych opcji Pokaż kursor i Kształt kursora w oknie dialogowym Ustawienia brajla. (#5198)
* NVDA może teraz łączyć się z monitorem brajlowskim HIMS Smart Beetle przez Bluetooth. (#5607)
* NVDA może opcjonalnie zmniejszyć głośność innych dźwięków, gdy jest zainstalowany w systemie Windows 8 i nowszych. Można to skonfigurować za pomocą opcji Tryb wyciszania dźwięku w oknie dialogowym syntezatora NVDA lub naciskając NVDA+shift+d. (#3830, #5575)
* Obsługa APH Refreshabraille w trybie HID oraz Baum VarioUltra i Pronto! po podłączeniu przez USB. (#5609)
* Obsługa monitorów brajlowskich HumanWare Brailliant BI/B, gdy protokół jest ustawiony na OpenBraille. (#5612)

### Zmiany

* Raportowanie wyróżnienia jest teraz domyślnie wyłączone. (#4920)
* W oknie dialogowym Lista elementów w programie Microsoft Excel skrót do formuł został zmieniony na alt+are, aby różnił się od skrótu do pola Filtr. (#5527)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.6.5. (#5574)
* Słowo "tekst" nie jest już zgłaszane po przeniesieniu kursora fokusu lub recenzji na obiekty tekstowe. (#5452)

### Poprawki błędów

* W programie iTunes 12 tryb przeglądania jest teraz poprawnie aktualizowany po załadowaniu nowej strony w sklepie iTunes Store. (#5191)
* W programie Internet Explorer i innych formantach MSHTML przechodzenie do określonych poziomów nagłówków z nawigacją jednoliterową działa teraz zgodnie z oczekiwaniami, gdy poziom nagłówka jest zastępowany ze względu na ułatwienia dostępu (w szczególności, gdy poziom ARIA zastępuje poziom znacznika h). (#5434)
* W Spotify ostrość nie ląduje już często na "nieznanych" obiektach. (#5439)
* Fokus jest teraz poprawnie przywracany po powrocie do Spotify z innej aplikacji. (#5439)
* Podczas przełączania między trybem przeglądania a trybem koncentracji uwagi, tryb jest podawany zarówno w alfabecie Braille'a, jak i w mowie. (#5239)
* Przycisk Start na pasku zadań nie jest już zgłaszany jako lista i/lub wybrany w niektórych wersjach systemu Windows. (#5178)
* Wiadomości, takie jak "wstawione", nie są już zgłaszane podczas tworzenia wiadomości w programie Microsoft Outlook. (#5486)
* W przypadku korzystania z monitora brajlowskiego i zaznaczenia tekstu w bieżącym wierszu (np. podczas wyszukiwania w edytorze tekstu tekstu, który znajduje się w tym samym wierszu), monitor brajlowski zostanie w razie potrzeby przewinięty. (#5410)
* NVDA nie zamyka się już po cichu po zamknięciu konsoli poleceń systemu Windows za pomocą alt+f4 w systemie Windows 10. (#5343)
* Na liście elementów w trybie przeglądania, po zmianie typu elementu, pole Filtruj według jest teraz wyczyszczone. (#5511)
* W edytowalnym tekście w aplikacjach Mozilli ponowne poruszenie myszą powoduje odczytanie odpowiedniego wiersza, słowa itp. zgodnie z oczekiwaniami, a nie całej zawartości. (#5535)
* Podczas przesuwania myszą po edytowalnym tekście w aplikacjach Mozilli czytanie nie zatrzymuje się już na elementach, takich jak linki w czytanym słowie lub wierszu. (#2160, #5535)
* W programie Internet Explorer witryna shoprite.com może być teraz odczytywana w trybie przeglądania, a nie zgłaszana jako pusta. (W szczególności zniekształcone atrybuty lang są teraz obsługiwane z wdziękiem). (#5569)
* W programie Microsoft Word prześledzone zmiany, takie jak "wstawione", nie są już raportowane, gdy nie jest wyświetlany znacznik śledzenia zmian. (#5566)
* Gdy przycisk przełączania jest aktywny, NVDA teraz informuje, kiedy jest zmieniany z wciśniętego na niewciśnięty. (#5441)
* Raportowanie zmian kształtu myszy ponownie działa zgodnie z oczekiwaniami. (#5595)
* Podczas odczytywania wcięć wierszy spacje nierozdzielające są teraz traktowane jako normalne spacje. Wcześniej mogło to powodować komunikaty, takie jak "przestrzeń kosmiczna" zamiast "3 spacje". (#5610)
* Podczas zamykania nowoczesnej listy kandydatów na metody wprowadzania firmy Microsoft fokus jest poprawnie przywracany do kompozycji wejściowej lub dokumentu źródłowego. (#4145)
* W pakiecie Microsoft Office 2013 i nowszych, gdy wstążka jest ustawiona tak, aby pokazywała tylko karty, elementy na wstążce są ponownie raportowane zgodnie z oczekiwaniami po uaktywnieniu karty. (#5504)
* Poprawki i ulepszenia wykrywania gestów na ekranie dotykowym i przypisywania. (#5652)
* Najechanie kursorem na ekran dotykowy nie jest już zgłaszane w pomocy do wprowadzania. (#5652)
* NVDA nie powoduje już niepowodzenia w wyświetlaniu komentarzy na liście elementów dla Microsoft Excel, jeśli komentarz znajduje się w scalonej komórce. (#5704)
* W bardzo rzadkich przypadkach NVDA nie odmawia już treści arkusza w programie Microsoft Excel z włączonym raportowaniem nagłówków wierszy i kolumn. (#5705)
* W przeglądarce Google Chrome nawigowanie w kompozycji wejściowej podczas wpisywania znaków wschodnioazjatyckich działa teraz zgodnie z oczekiwaniami. (#4080)
* Podczas przeszukiwania Apple Music w iTunes tryb przeglądania dokumentu wyników wyszukiwania jest teraz aktualizowany zgodnie z oczekiwaniami. (#5659)
* W programie Microsoft Excel naciśnięcie shift+f11 w celu utworzenia nowego arkusza powoduje teraz wyświetlenie informacji o nowej pozycji, a nie zgłaszanie niczego. (#5689)
* Naprawiono problemy z wyświetlaniem monitora brajlowskiego podczas wprowadzania znaków koreańskich. (#5640)

### Zmiany dla deweloperów

* Nowa klasa audioDucking.AudioDucker pozwala kodowi, który wyprowadza dźwięk, wskazać, kiedy dźwięk w tle powinien zostać wyciszony. (#3830)
* nvwave. Konstruktor WavePlayer ma teraz argument słowa kluczowego wantDucking, który określa, czy dźwięk w tle powinien być wyciszony podczas odtwarzania dźwięku. (#3830)
 * Gdy ta opcja jest włączona (co jest ustawieniem domyślnym), ważne jest, aby WavePlayer.idle był wywoływany w razie potrzeby.
* Ulepszone I/O dla monitorów brajlowskich: (#5609)
 * Bezpieczne wątkowo sterowniki monitorów brajlowskich mogą deklarować się jako takie, korzystając z atrybutu BrailleDisplayDriver.isThreadSafe. Sterownik musi być bezpieczny wątkowo, aby można było korzystać z następujących funkcji.
 * Dane są zapisywane w bezpiecznych wątkowo sterownikach monitorów brajlowskich w tle, co poprawia wydajność.
 * hwIo.Serial rozszerza pyserial tak, aby wywoływał obiekt po odebraniu danych, zamiast gdy sterowniki muszą odpytywać.
 * hwIo.Hid zapewnia wsparcie dla monitorów brajlowskich komunikujących się za pomocą USB HID.
 * hwPortUtils i hwIo mogą opcjonalnie zapewnić szczegółowe rejestrowanie debugowania, w tym znalezione urządzenia oraz wszystkie wysłane i odebrane dane.
* Istnieje kilka nowych właściwości dostępnych z gestów ekranu dotykowego: (#5652)
 * Obiekty MultitouchTracker zawierają teraz właściwość childTrackers, która zawiera obiekty MultiTouchTrackers, z których składał się moduł śledzący. Na przykład dwukrotne stuknięcie 2 palcami ma moduły śledzące dla dwóch stuknięć 2 palcami. Same stuknięcia 2-palcowe mają podrzędne urządzenia śledzące na dwa dotknięcia.
 * Obiekty MultiTouchTracker zawierają teraz również właściwość rawSingleTouchTracker, jeśli moduł śledzący powstał w wyniku dotknięcia, przesunięcia lub najechania kursorem na jeden palec. SingleTouchTracker umożliwia dostęp do podstawowego identyfikatora przypisanego do palca przez system operacyjny oraz do tego, czy palec jest nadal w kontakcie w danym momencie.
 * Gesty TouchInputGestures mają teraz właściwości x i y, eliminując potrzebę uzyskiwania dostępu do trackera w trywialnych przypadkach.
 * Gesturs TouchInputGesturs zawierają teraz właściwość preheldTracker, która jest obiektem MultitouchTracker reprezentującym inne palce trzymane podczas wykonywania tej czynności.
* Można emitować dwa nowe gesty ekranu dotykowego: (#5652)
 * Dotknięcie i przytrzymanie w liczbie mnogiej (np. dwukrotne stuknięcie i przytrzymanie)
 * Uogólniony identyfikator z usuniętą liczbą palców dla przytrzymań (np. przytrzymanie+najechanie kursorem na 1finger_hold+najechanie kursorem).

## 2015.4

Najważniejsze cechy tej wersji obejmują ulepszenia wydajności w systemie Windows 10; włączenie do Centrum ułatwień dostępu w systemie Windows 8 i nowszych; ulepszenia programu Microsoft Excel, w tym wyświetlanie listy i zmiana nazw arkuszy oraz dostęp do zablokowanych komórek w chronionych arkuszach; oraz obsługa edycji tekstu sformatowanego w przeglądarkach Mozilla Firefox, Google Chrome i Mozilla Thunderbird.

### Nowe funkcje

* NVDA pojawia się teraz w Centrum ułatwień dostępu w systemie Windows 8 i nowszych. (#308)
* Podczas poruszania się między komórkami w programie Excel, zmiany formatowania są teraz automatycznie zgłaszane, jeśli odpowiednie opcje są włączone w oknie dialogowym Ustawienia formatowania dokumentu NVDA. (#4878)
* Opcja Podkreślenia raportu została dodana do okna dialogowego ustawień formatowania dokumentu NVDA. Domyślnie ta opcja pozwala NVDA automatycznie zgłaszać obecność wyróżnionego tekstu w dokumentach. Do tej pory jest to obsługiwane tylko w przypadku tagów em i strong w trybie przeglądania dla programu Internet Explorer i innych kontrolek MSHTML. (#4920)
* Istnienie wstawionego i usuniętego tekstu jest teraz zgłaszane w trybie przeglądania dla Internet Explorera i innych kontrolek MSHTML, jeśli włączona jest opcja Wersje edytora raportów NVDA. (#4920)
* Podczas przeglądania zmian ścieżek na liście elementów NVDA dla programu Microsoft Word, wyświetlanych jest teraz więcej informacji, takich jak właściwości formatowania, które zostały zmienione. (#4920)
* Microsoft Excel: wyświetlanie i zmiana nazw arkuszy jest teraz możliwa z listy elementów NVDA (NVDA+f7). (#4630, #4414)
* Teraz można skonfigurować, czy rzeczywiste symbole są wysyłane do syntezatorów mowy (np. w celu spowodowania pauzy lub zmiany fleksji) w oknie dialogowym Wymowa symboli. (#5234)
* W programie Microsoft Excel NVDA raportuje teraz wszystkie komunikaty wejściowe ustawione przez autora arkusza w komórkach. (#5051)
* Wsparcie dla Baum Pronto! Monitory brajlowskie V4 i VarioUltra po połączeniu przez Bluetooth. (#3717)
* Obsługa edycji tekstu sformatowanego w aplikacjach Mozilli, takich jak Google Docs, z włączoną obsługą alfabetu Braille'a w przeglądarce Mozilla Firefox i kompozycji HTML w Mozilla Thunderbird. (#1668)
* Obsługa edycji tekstu sformatowanego w Google Chrome i przeglądarkach opartych na Chrome, takich jak Dokumenty Google, z włączoną obsługą alfabetu Braille'a. (#2634)
 * Wymaga to przeglądarki Chrome w wersji 47 lub nowszej.
* W trybie przeglądania w programie Microsoft Excel możesz przechodzić do zablokowanych komórek w chronionych arkuszach. (#4952)

### Zmiany

* Opcja Wersje edytora raportów w oknie dialogowym ustawień formatowania dokumentu NVDA jest teraz domyślnie włączona. (#4920)
* Podczas poruszania się według znaków w programie Microsoft Word z włączoną opcją Wersje edytora raportów NVDA, mniej informacji jest teraz zgłaszanych do śledzenia zmian, co sprawia, że nawigacja jest bardziej wydajna. Aby wyświetlić dodatkowe informacje, użyj listy elementów. (#4920)
* Zaktualizowano tłumacz brajlowski liblouis do wersji 2.6.4. (#5341)
* Niektóre symbole (w tym podstawowe symbole matematyczne) zostały przeniesione na wyższy poziom, tak aby były wypowiadane domyślnie. (#3799)
* Jeśli syntezator to obsługuje, mowa powinna teraz zostać wstrzymana dla nawiasów i półpauzy (–). (#3799)
* Podczas zaznaczania tekstu tekst jest raportowany przed wskazaniem zaznaczenia, a nie po. (#1707)

### Poprawki błędów

* Znaczna poprawa wydajności podczas nawigowania po liście wiadomości programu Outlook 2010/2013. (#5268)
* Na wykresie w programie Microsoft Excel nawigacja za pomocą niektórych (takich jak zmienianie arkuszy za pomocą control+pageUp i control+pageDown) działa teraz poprawnie. (#5336)
* Poprawiono wygląd przycisków w oknie dialogowym ostrzeżenia, które jest wyświetlane przy próbie obniżenia wersji NVDA. (#5325)
* W Windows 8 i nowszych, NVDA uruchamia się teraz znacznie wcześniej, gdy jest skonfigurowany do uruchamiania po zalogowaniu się do Windows. (#308)
 * Jeśli włączyłeś tę funkcję za pomocą poprzedniej wersji NVDA, będziesz musiał ją wyłączyć i włączyć ponownie, aby zmiana zaczęła obowiązywać. Postępuj zgodnie z tą procedurą:
  1. Otwórz okno dialogowe Ustawienia ogólne.
  1. Odznacz pole wyboru Automatycznie uruchamiaj NVDA po zalogowaniu się do systemu Windows.
  1. Naciśnij przycisk OK.
  1. Otwórz ponownie okno dialogowe Ustawienia ogólne.
  1. Zaznacz pole wyboru Automatycznie uruchamiaj NVDA po zalogowaniu się do systemu Windows.
  1. Naciśnij przycisk OK.
* Ulepszenia wydajności automatyzacji interfejsu użytkownika, w tym Eksploratora plików i Podglądu zadań. (#5293)
* NVDA teraz poprawnie przełącza się w tryb skupienia podczas przełączania na kontrolki siatki ARIA tylko do odczytu w trybie przeglądania dla przeglądarki Mozilla Firefox i innych kontrolek opartych na Gecko. (#5118)
* NVDA teraz poprawnie wyświetla komunikat "brak poprzedniego" zamiast "brak następnego", gdy nie ma już żadnych obiektów po przesunięciu w lewo na ekranie dotykowym.
* Rozwiązano problemy podczas wpisywania wielu słów w polu filtru w oknie dialogowym Gesty wprowadzania. (#5426)
* NVDA nie zawiesza się już w niektórych przypadkach po ponownym podłączeniu do wyświetlacza HumanWare Brailliant z serii BI/B przez USB. (#5406)
* W językach ze znakami koniunkcyjnymi opisy znaków działają teraz zgodnie z oczekiwaniami dla wielkich liter angielskich. (#5375)
* NVDA nie powinien już od czasu do czasu zawieszać się podczas otwierania menu Start w systemie Windows 10. (#5417)
* W Skypie dla komputerów stacjonarnych powiadomienia, które są wyświetlane przed zniknięciem poprzedniego powiadomienia, są teraz raportowane. (#4841)
* Powiadomienia są teraz poprawnie raportowane w Skypie dla komputerów stacjonarnych w wersji 7.12 i nowszych. (#5405)
* NVDA teraz poprawnie zgłasza fokus po zamknięciu menu kontekstowego w niektórych aplikacjach, takich jak Jart. (#5302)
* W systemie Windows 7 i nowszych kolor jest ponownie zgłaszany w niektórych aplikacjach, takich jak Wordpad. (#5352)
* Podczas edycji w programie Microsoft PowerPoint naciśnięcie Enter powoduje teraz wyświetlenie automatycznie wprowadzonego tekstu, takiego jak punktor lub numer. (#5360)

## 2015.3

Najważniejsze cechy tej wersji obejmują wstępną obsługę systemu Windows 10; możliwość wyłączenia nawigacji po pojedynczych literach w trybie przeglądania (przydatne w przypadku niektórych aplikacji internetowych); ulepszenia w przeglądarce Internet Explorer; oraz poprawki zniekształconego tekstu podczas pisania w niektórych aplikacjach z włączonym alfabetem Braille'a.

### Nowe funkcje

* Informacja o występowaniu błędów pisowni jest ogłaszana w edytowalnych polach programu Internet Explorer i innych formantach programu MSHTML. (#4174)
* Wiele innych symboli matematycznych Unicode jest teraz wypowiadanych, gdy pojawiają się w tekście. (#3805)
* Sugestie wyszukiwania na ekranie startowym systemu Windows 10 są zgłaszane automatycznie. (#5049)
* Obsługa monitorów brajlowskich EcoBraille 20, EcoBraille 40, EcoBraille 80 i EcoBraille Plus. (#4078)
* W trybie przeglądania możesz teraz włączać i wyłączać nawigację po pojedynczych literach, naciskając NVDA+shift+spacja. Gdy ta opcja jest wyłączona, do aplikacji przekazywane są jednoliterowe klucze, co jest przydatne w przypadku niektórych aplikacji internetowych, takich jak Gmail, Twitter i Facebook. (#3203)
* Nowe tabele tłumaczeń brajlowskich: fiński 6 punktów, irlandzki ocena 1, irlandzki stopień 2, koreański stopień 1 (2006), koreański stopień 2 (2006). (#5137, #5074, #5097)
* Klawiatura QWERTY w monitorze brajlowskim Papenmeier BRAILLEX Live Plus jest teraz obsługiwana. (#5181)
* Eksperymentalna obsługa przeglądarki internetowej Microsoft Edge i silnika przeglądania w systemie Windows 10. (#5212)
* Nowy język: Kannada.

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.6.3. (#5137)
* Podczas próby zainstalowania wcześniejszej wersji NVDA niż jest obecnie zainstalowana, zostaniesz ostrzeżony, że nie jest to zalecane i że NVDA powinien zostać całkowicie odinstalowany przed kontynuowaniem. (#5037)

### Poprawki błędów

* W trybie przeglądania programu Internet Explorer i innych kontrolek MSHTML szybka nawigacja według pola formularza nie zawiera już niepoprawnie elementów listy prezentacyjnej. (#4204)
* W Firefoksie NVDA nie zgłasza już nieprawidłowo zawartości panelu kart ARIA po przeniesieniu fokusu do jego wnętrza. (#4638)
* W programie Internet Explorer i innych formantach MSHTML przechodzenie Tab do sekcji, artykułów lub okien dialogowych nie powoduje już nieprawidłowego raportowania całej zawartości kontenera. (#5021, #5025)
* W przypadku korzystania z monitorów brajlowskich Baum/HumanWare/APH z klawiaturą brajlowską, wprowadzanie brajlowskie nie przestaje działać po naciśnięciu innego typu na wyświetlaczu. (#3541)
* W systemie Windows 10 zbędne informacje nie są już zgłaszane po naciśnięciu Alt+Tab lub Alt+Shift+Tab w celu przełączania się między aplikacjami. (#5116)
* Wpisywany tekst nie jest już zniekształcony podczas korzystania z niektórych aplikacji, takich jak Microsoft Outlook z monitorem brajlowskim. (#2953)
* W trybie przeglądania w programie Internet Explorer i innych formantach MSHTML poprawna zawartość jest teraz zgłaszana, gdy element pojawia się lub zmienia i jest natychmiast aktywny. (#5040)
* W trybie przeglądania w programie Microsoft Word nawigacja jednoliterowa aktualizuje teraz monitor brajlowski i kursor recenzowania zgodnie z oczekiwaniami. (#4968)
* W alfabecie Braille'a obce spacje nie są już wyświetlane między lub po wskaźnikach elementów sterujących i formatowania. (#5043)
* Gdy aplikacja odpowiada powoli i odchodzisz od niej, NVDA jest teraz w większości przypadków znacznie bardziej responsywna w innych aplikacjach. (#3831)
* Wyskakujące powiadomienia systemu Windows 10 są teraz zgłaszane zgodnie z oczekiwaniami. (#5136)
* Wartość jest teraz raportowana w miarę jej zmian w niektórych polach kombi (automatyzacja interfejsu użytkownika), w których wcześniej nie działało.
* W trybie przeglądania w przeglądarkach internetowych naciśnięcie Tab działa teraz zgodnie z oczekiwaniami po przejściu do dokumentu ramki za pomocą Tab. (#5227)
* Ekran blokady systemu Windows 10 można teraz zamknąć za pomocą ekranu dotykowego. (#5220)
* W systemie Windows 7 i nowszych tekst nie jest już zniekształcony podczas pisania w niektórych aplikacjach, takich jak Wordpad i Skype z monitorem brajlowskim. (#4291)
* Na ekranie blokady systemu Windows 10 nie można już odczytać schowka, uzyskać dostępu do uruchomionych aplikacji za pomocą kursora przeglądania, zmienić konfiguracji NVDA itp. (#5269)

### Zmiany dla deweloperów

* Możesz teraz wstrzykiwać nieprzetworzone dane wejściowe z klawiatury systemowej, która nie jest natywnie obsługiwana przez system Windows (np. klawiatury QWERTY na monitorze brajlowskim) za pomocą nowej funkcji keyboardHandler.injectRawKeyboardInput. (#4576)
* eventHandler.requestEvents został dodany w celu żądania określonych zdarzeń, które są domyślnie blokowane; Np. pokazuj zdarzenia z określonej kontrolki lub określone zdarzenia nawet w tle. (#3831)
* Zamiast pojedynczego atrybutu i18nName, synthDriverHandler.SynthSetting ma teraz oddzielne atrybuty displayNameWithAccelerator i displayName, aby uniknąć raportowania akceleratora w pierścieniu ustawień syntezatora w niektórych językach.
 * W celu zapewnienia zgodności z poprzednimi wersjami w konstruktorze displayName jest opcjonalna i będzie pochodzić od displayNameWithAccelerator, jeśli nie zostanie podana. Jeśli jednak zamierzasz mieć akcelerator dla ustawienia, należy zapewnić oba te elementy.
 * Atrybut i18nName jest przestarzały i może zostać usunięty w przyszłej wersji.

## 2015.2

Najważniejsze cechy tego wydania to możliwość odczytywania wykresów w programie Microsoft Excel oraz obsługa czytania i interaktywnej nawigacji po treściach matematycznych.

### Nowe funkcje

* Przechodzenie do przodu i do tyłu za pomocą zdań w programach Microsoft Word i Outlook jest teraz możliwe odpowiednio za pomocą alt + strzałka w dół i alt + strzałka w górę. (#3288)
* Nowe tabele tłumaczeń brajlowskich dla kilku języków indyjskich. (#4778)
* W programie Microsoft Excel NVDA informuje teraz, kiedy komórka ma przepełnioną lub przyciętą zawartość. (#3040)
* W programie Microsoft Excel można teraz korzystać z listy elementów (NVDA+f7), aby umożliwić wyświetlanie listy wykresów, komentarzy i formuł. (#1987)
* Obsługa odczytywania wykresów w programie Microsoft Excel. Aby z tego skorzystać, wybierz wykres za pomocą listy elementów (NVDA+f7), a następnie użyj strzałek, aby przejść między punktami danych. (#1987)
* Korzystając z MathPlayer 4 firmy Design Science, NVDA może teraz czytać i interaktywnie nawigować po treściach matematycznych w przeglądarkach internetowych oraz w programach Microsoft Word i PowerPoint. Szczegółowe informacje można znaleźć w sekcji "Czytanie treści matematycznych" w Podręczniku użytkownika. (#4673)
* Teraz możliwe jest przypisywanie gestów wejściowych (poleceń klawiaturowych, gestów dotykowych itp.) do wszystkich okien dialogowych preferencji NVDA i opcji formatowania dokumentu za pomocą okna dialogowego Gesty wprowadzania. (#4898)

### Zmiany

* W oknie dialogowym Formatowanie Dokumentu NVDA zmieniono skróty klawiaturowe dla list raportów, linków do raportów, numerów wierszy raportu i nazwy czcionki raportu. (#4650)
* W oknie dialogowym ustawień myszy NVDA dodano skróty klawiaturowe do odtwarzania współrzędnych audio, gdy mysz się porusza, a jasność kontroluje głośność współrzędnych dźwięku. (#4916)
* Znacznie ulepszono raportowanie nazw kolorów. (#4984)
* Zaktualizowano tłumacz brajlowski liblouis do wersji 2.6.2. (#4777)

### Poprawki błędów

* Opisy znaków są teraz obsługiwane poprawnie dla znaków koniunkcyjnych w niektórych językach indyjskich. (#4582)
* Jeśli włączona jest opcja "Ufaj językowi głosu podczas przetwarzania znaków i symboli", okno dialogowe Wymowa znaków interpunkcyjnych/symboli teraz poprawnie używa języka głosu. Ponadto język, dla którego jest edytowana wymowa, jest pokazany w tytule okna dialogowego. (#4930)
* W programie Internet Explorer i innych formantach MSHTML wpisywane znaki nie są już nieprawidłowo ogłaszane w edytowalnych polach kombi, takich jak pole wyszukiwania Google na stronie głównej Google. (#4976)
* Podczas wybierania kolorów w aplikacjach pakietu Microsoft Office są teraz raportowane nazwy kolorów. (#3045)
* Duński alfabet Braille'a znów działa. (#4986)
* PageUp/pageDown może być ponownie używany do zmieniania slajdów w pokazie slajdów programu PowerPoint. (#4850)
* W Skypie dla komputerów stacjonarnych 7.2 i nowszych powiadomienia o pisaniu są teraz zgłaszane, a problemy natychmiast po przeniesieniu fokusu z konwersacji zostały naprawione. (#4972)
* Naprawiono problemy podczas wpisywania niektórych znaków interpunkcyjnych/symboli, takich jak nawiasy, w polu filtra w oknie dialogowym Gesty wprowadzania. (#5060)
* W Internet Explorerze i innych kontrolkach MSHTML naciśnięcie g lub Shift+g w celu przejścia do grafiki obejmuje teraz elementy oznaczone jako obrazy w celu ułatwień dostępu (np. ARIA role img). (#5062)

### Zmiany dla deweloperów

* brailleInput.handler.sendChars(mychar) nie będzie już filtrować znaku, jeśli jest równy poprzedniemu znakowi, upewniając się, że wysłany klucz został poprawnie zwolniony. (#4139)
* Skrypty do zmiany trybów dotyku będą teraz uwzględniać nowe etykiety dodane do touchHandler.touchModeLabels. (#4699)
* Dodatki mogą zapewniać własne implementacje prezentacji matematycznych. Zobacz pakiet mathPres, aby uzyskać szczegółowe informacje. (#4509)
* Zaimplementowano polecenia głosowe, aby wstawić przerwę między słowami oraz zmienić wysokość, głośność i szybkość. Zobacz BreakCommand, PitchCommand, VolumeCommand i RateCommand w module mowy. (#4674)
 * Jest też mowa. PhonemeCommand, aby wstawić określoną wymowę, ale obecne implementacje obsługują tylko bardzo ograniczoną liczbę fonemów.

## 2015.1

Najważniejsze cechy tej wersji obejmują tryb przeglądania dokumentów w programach Microsoft Word i Outlook; znaczne ulepszenia obsługi Skype'a dla komputerów stacjonarnych; oraz znaczące poprawki dla przeglądarki Microsoft Internet Explorer.

### Nowe funkcje

* Teraz można dodawać nowe symbole w oknie dialogowym Wymowa symboli. (#4354)
* W oknie dialogowym Gesty wejściowe możesz użyć nowego pola "Filtruj według", aby wyświetlić tylko gesty zawierające określone słowa. (#4458)
* NVDA teraz automatycznie zgłasza nowy tekst w miętowym kolorze. (#4588)
* W oknie dialogowym Znajdź w trybie przeglądania dostępna jest teraz opcja wyszukiwania z uwzględnieniem wielkości liter. (#4584)
* Szybka nawigacja (naciśnięcie h, aby poruszać się według nagłówka itp.) i lista elementów (NVDA+f7) są teraz dostępne w dokumentach Microsoft Word po włączeniu trybu przeglądania za pomocą NVDA+spacja. (#2975)
* Odczytywanie wiadomości HTML w programie Microsoft Outlook 2007 i nowszych wersjach zostało znacznie ulepszone, ponieważ tryb przeglądania jest automatycznie włączany dla tych wiadomości. Jeśli tryb przeglądania nie jest włączony w rzadkich sytuacjach, możesz go wymusić za pomocą NVDA+spacja. (#2975)
* Nagłówki kolumn tabeli w programie Microsoft Word są automatycznie raportowane dla tabel, w których wiersz nagłówka został jawnie określony przez autora za pomocą właściwości tabeli programu Microsoft Word. (#4510)
 * Jednak w przypadku tabel, w których wiersze zostały scalone, nie będzie to działać automatycznie. W tej sytuacji nadal możesz ręcznie ustawić nagłówki kolumn w NVDA za pomocą NVDA+shift+c.
* W Skypie dla komputerów stacjonarnych powiadomienia są teraz raportowane. (#4741)
* W Skypie dla komputerów stacjonarnych można teraz zgłaszać i przeglądać ostatnie wiadomości przy użyciu NVDA+control+1 do NVDA+control+0; np. NVDA+control+1 dla najnowszej wiadomości i NVDA+control+0 dla dziesiątej najnowszej. (#3210)
* W konwersacji w Skypie dla komputerów stacjonarnych NVDA zgłasza teraz, kiedy kontakt pisze. (#3506)
* NVDA może być teraz zainstalowany po cichu za pomocą wiersza poleceń bez uruchamiania zainstalowanej kopii po instalacji. Aby to zrobić, użyj opcji --install-silent. (#4206)
* Obsługa monitorów brajlowskich Papenmeier BRAILLEX Live 20, BRAILLEX Live i BRAILLEX Live Plus. (#4614)

### Zmiany

* W oknie dialogowym ustawień formatowania dokumentu NVDA, opcja zgłaszania błędów ortograficznych ma teraz skrótu (alt+r). (#793)
* NVDA będzie teraz używać języka syntezatora/głosu do przetwarzania znaków i symboli (w tym nazw interpunkcyjnych/symboli), niezależnie od tego, czy włączone jest automatyczne przełączanie języka. Aby wyłączyć tę funkcję, aby NVDA ponownie używała swojego języka interfejsu, odznacz nową opcję w ustawieniach Voice o nazwie Język Trust Voice podczas przetwarzania znaków i symboli. (#4210)
* Wsparcie dla syntezatora Newfon zostało usunięte. Newfon jest teraz dostępny jako dodatek do NVDA. (#3184)
* Skype dla komputerów stacjonarnych w wersji 7 lub nowszej jest teraz wymagany do użytku z NVDA; Wcześniejsze wersje nie są obsługiwane. (#4218)
* Pobieranie aktualizacji NVDA jest teraz bezpieczniejsze. (W szczególności informacje o aktualizacji są pobierane za pośrednictwem protokołu https, a skrót pliku jest weryfikowany po jego pobraniu). (#4716)
* eSpeak został zaktualizowany do wersji 1.48.04 (#4325)

### Poprawki błędów

* W programie Microsoft Excel scalone komórki nagłówka wiersza i kolumny są teraz obsługiwane poprawnie. Na przykład, jeśli A1 i B1 zostaną scalone, B2 będzie teraz miał A1 i B1 raportowane jako nagłówek kolumny, a nie nic. (#4617)
* Podczas edytowania zawartości pola tekstowego w programie Microsoft PowerPoint 2003, NVDA poprawnie raportuje zawartość każdego wiersza. Wcześniej w każdym akapicie wiersze coraz częściej różniły się o jeden znak. (#4619)
* Wszystkie okna dialogowe NVDA są teraz wyśrodkowane na ekranie, co poprawia prezentację wizualną i użyteczność. (#3148)
* W Skypie dla komputerów stacjonarnych podczas wprowadzania wiadomości wprowadzającej w celu dodania kontaktu wprowadzanie tekstu i poruszanie się po nim działa teraz poprawnie. (#3661)
* Gdy fokus zostanie przeniesiony do nowego elementu w widokach drzewa w środowisku IDE Eclipse, jeśli poprzednio skoncentrowany element jest polem wyboru, nie jest już niepoprawnie ogłaszany. (#4586)
* W oknie dialogowym sprawdzania pisowni programu Microsoft Word następny błąd zostanie automatycznie zgłoszony, gdy ostatni błąd zostanie zmieniony lub zignorowany za pomocą odpowiednich skrótów. (#1938)
* Tekst może być ponownie poprawnie odczytany w miejscach takich jak okno terminala Tera Term Pro i dokumenty w Balabolce. (#4229)
* Fokus teraz poprawnie powraca do edytowanego dokumentu po zakończeniu tworzenia tekstu w języku koreańskim i innych językach wschodnioazjatyckich podczas edytowania w ramce w programie Internet Explorer i innych dokumentach MSHTML. (#4045)
* W oknie dialogowym Gesty wprowadzania, podczas wybierania układu klawiatury dla dodawanego gestu klawiatury, naciśnięcie Escape powoduje teraz zamknięcie menu zgodnie z oczekiwaniami, a nie zamknięcie okna dialogowego. (#3617)
* Podczas usuwania dodatku, katalog z dodatkiem jest teraz poprawnie usuwany po ponownym uruchomieniu NVDA. Wcześniej trzeba było dwukrotnie uruchamiać ponownie. (#3461)
* Rozwiązano poważne problemy podczas korzystania ze Skype'a dla komputerów stacjonarnych 7. (#4218)
* Gdy wysyłasz wiadomość w Skypie dla pulpitu, nie jest ona już odczytywana dwukrotnie. (#3616)
* W Skypie dla Desktopa NVDA nie powinno już od czasu do czasu pozorować zalewu wiadomości (być może nawet całej rozmowy). (#4644)
* Naprawiono błąd, który powodował, że polecenie Zgłoś datę/godzinę NVDA w niektórych przypadkach nie uwzględniało ustawień regionalnych określonych przez użytkownika. (#2987)
* W trybie przeglądania bezsensowny tekst (czasami obejmujący kilka wierszy) nie jest już wyświetlany w przypadku niektórych grafik, takich jak znalezione w Grupach dyskusyjnych Google. (W szczególności wystąpiło to w przypadku obrazów zakodowanych w formacie base64). (#4793)
* NVDA nie powinien się już zawieszać po kilku sekundach po przeniesieniu fokusu z aplikacji ze Sklepu Windows, gdy zostaje ona zawieszona. (#4572)
* Atrybut aria-atomic w obszarach aktywnych w przeglądarce Mozilla Firefox jest teraz honorowany nawet wtedy, gdy zmienia się sam pierwiastek atomowy. Wcześniej dotyczyło to tylko elementów potomnych. (#4794)
* Tryb przeglądania będzie odzwierciedlał aktualizacje, a regiony dynamiczne będą ogłaszane dla dokumentów w trybie przeglądania w aplikacjach ARIA osadzonych w dokumencie w programie Internet Explorer lub innych kontrolkach MSHTML. (#4798)
* Gdy tekst jest zmieniany lub dodawany w obszarach dynamicznych w programie Internet Explorer i innych formantach MSHTML, w których autor określił, że tekst jest istotny, ogłaszany jest tylko zmieniony lub dodany tekst, a nie cały tekst w elemencie zawierającym. (#4800)
* Zawartość wskazywana przez atrybut aria-labelledby w elementach programu Internet Explorer i innych formantach MSHTML poprawnie zastępuje oryginalną zawartość tam, gdzie jest to właściwe. (#4575)
* Podczas sprawdzania pisowni w programie Microsoft Outlook 2013 błędnie napisany wyraz jest teraz ogłaszany. (#4848)
* W programie Internet Explorer i innych formantach MSHTML zawartość wewnątrz elementów ukrytych za pomocą opcji visibility:hidden nie jest już nieprawidłowo prezentowana w trybie przeglądania. (#4839, #3776)
* W programie Internet Explorer i innych formantach MSHTML atrybut title w formantach formularza nie ma już nieprawidłowo pierwszeństwa przed innymi skojarzeniami etykiet. (#4491)
* W Internet Explorerze i innych kontrolkach MSHTML, NVDA nie ignoruje już fokusu elementów ze względu na atrybut aria-activedescendant. (#4667)

### Zmiany dla deweloperów

* Zaktualizowano wxPython do wersji 3.0.2.0. (#3763)
* Zaktualizowano język Python do wersji 2.7.9. (#4715)
* NVDA nie zawiesza się już podczas ponownego uruchamiania po usunięciu lub zaktualizowaniu dodatku, który importuje speechDictHandler do swojego modułu installTasks. (#4496)

## 2014.4

### Nowe funkcje

* Nowe języki: kolumbijski hiszpański, pendżabski.
* Teraz możliwe jest ponowne uruchomienie NVDA lub ponowne uruchomienie NVDA z wyłączonymi dodatkami z poziomu okna wyjścia NVDA. (#4057)
 * NVDA może być również uruchomiona z wyłączonymi dodatkami za pomocą opcji wiersza poleceń --disable-addons.
* W słownikach mowy można teraz określić, że wzorzec powinien być zgodny tylko wtedy, gdy jest całym słowem; tzn. nie występuje jako część większego słowa. (#1704)

### Zmiany

* Jeśli obiekt, do którego przeniesiono nawigację po obiektach, znajduje się w dokumencie w trybie przeglądania, ale obiekt, na którym wcześniej się znajdowałeś, nie znajdował się w nim, tryb recenzji zostanie automatycznie ustawiony na dokument. Wcześniej działo się tak tylko wtedy, gdy obiekt nawigatora został przesunięty z powodu zmiany fokusu. (#4369)
* Listy monitora brajlowskiego i syntezatora w odpowiednich oknach dialogowych ustawień są teraz posortowane alfabetycznie, z wyjątkiem opcji Brak alfabetu Braille'a/Brak mowy, które znajdują się teraz na dole. (#2724)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.6.0. (#4434, #3835)
* W trybie przeglądania naciśnięcia e i shift+e w celu przejścia do pól edycji zawierają teraz edytowalne pola kombi. Dotyczy to również pola wyszukiwania w najnowszej wersji wyszukiwarki Google. (#4436)
* Kliknięcie ikony NVDA w obszarze powiadomień lewym przyciskiem myszy otwiera teraz menu NVDA, zamiast nic nie robić. (#4459)

### Poprawki błędów

* Podczas przenoszenia fokusu z powrotem do dokumentu w trybie przeglądania (np. alt+tabbing do już otwartej strony internetowej) kursor recenzji jest prawidłowo umieszczony na wirtualnym kursorze, a nie na aktywnej kontrolce (np. na pobliskim łączu). (#4369)
* W pokazach slajdów programu PowerPoint kursor recenzji prawidłowo podąża za wirtualnym karetką. (#4370)
* W Mozilla Firefox i innych przeglądarkach opartych na Gecko, nowa zawartość w aktywnym regionie będzie ogłaszana, nawet jeśli nowa zawartość ma użyteczny typ ARIA live inny niż nadrzędny region live; Np. gdy treść oznaczona jako asertywna zostanie dodana do aktywnego regionu oznaczonego jako uprzejma. (#4169)
* W programie Internet Explorer i innych formantach MSHTML niektóre przypadki, gdy dokument znajduje się w innym dokumencie, nie uniemożliwiają już użytkownikowi dostępu do części zawartości (w szczególności zestawów ramek wewnątrz zestawów ramek). (#4418)
* NVDA nie zawiesza się już w niektórych przypadkach przy próbie użycia monitora brajlowskiego Handy Tech. (#3709)
* W systemie Windows Vista fałszywe okno dialogowe "Nie znaleziono punktu wejścia" nie jest już wyświetlane w kilku przypadkach, takich jak uruchamianie NVDA ze skrótu na pulpicie lub za pomocą skrótu. (#4235)
* Naprawiono poważne problemy z edytowalnymi kontrolkami tekstu w oknach dialogowych w najnowszych wersjach Eclipse. (#3872)
* W programie Outlook 2010 przeniesienie daszka działa teraz zgodnie z oczekiwaniami w polu lokalizacji terminów i wezwań na spotkania. (#4126)
* Wewnątrz aktywnego regionu zawartość oznaczona jako nieaktywna (np. aria-live="off") jest teraz poprawnie ignorowana. (#4405)
* Podczas zgłaszania tekstu paska stanu, który ma nazwę, nazwa jest teraz poprawnie oddzielona od pierwszego słowa tekstu paska stanu. (#4430)
* W polach wprowadzania haseł z włączoną funkcją mówienia wpisywanych słów wiele gwiazdek nie jest już bezsensownie zgłaszanych podczas rozpoczynania nowych słów. (#4402)
* Na liście wiadomości programu Microsoft Outlook elementy nie są już bezsensownie ogłaszane jako elementy danych. (#4439)
* Podczas zaznaczania tekstu w kontrolce edycji kodu w środowisku IDE Eclipse całe zaznaczenie nie jest już ogłaszane za każdym razem, gdy zaznaczenie ulega zmianie. (#2314)
* Różne wersje Eclipse, takie jak Spring Tool Suite i wersja zawarta w pakiecie Android Developer Tools, są teraz rozpoznawane jako Eclipse i odpowiednio obsługiwane. (#4360, #4454)
* Śledzenie myszy i eksploracja dotykiem w programie Internet Explorer i innych kontrolkach MSHTML (w tym w wielu aplikacjach systemu Windows 8) jest teraz znacznie dokładniejsze na wyświetlaczach o wysokiej rozdzielczości lub po zmianie powiększenia dokumentu. (#3494)
* Śledzenie myszy i eksploracja dotyku w programie Internet Explorer oraz inne kontrolki MSHTML będą teraz informować o etykietach większej liczby przycisków. (#4173)
* Podczas korzystania z monitora brajlowskiego Papenmeier BRAILLEX z BrxCom, na wyświetlaczu działają teraz zgodnie z oczekiwaniami. (#4614)

### Zmiany dla deweloperów

* W przypadku plików wykonywalnych, które hostują wiele różnych aplikacji (np. javaw.exe), można teraz podać kod w celu załadowania określonych modułów aplikacji dla każdej aplikacji zamiast ładowania tego samego modułu aplikacji dla wszystkich hostowanych aplikacji. (#4360)
 * Aby uzyskać szczegółowe informacje, zapoznaj się z dokumentacją kodu dla appModuleHandler.AppModule .
 * Wdrożono wsparcie dla javaw.exe.

## 2014.3

### Nowe funkcje

* Dźwięki odtwarzane podczas uruchamiania i wychodzenia NVDA można wyłączyć za pomocą nowej opcji w oknie dialogowym Ustawienia ogólne. (#834)
* Dostęp do pomocy dotyczącej dodatków można uzyskać w Menedżerze dodatków, aby uzyskać dostęp do dodatków, które obsługują tę funkcję. (#2694)
* Obsługa kalendarza w programie Microsoft Outlook 2007 i nowszych (#2943), w tym:
 * Komunikat o aktualnym czasie podczas poruszania się za pomocą strzałek.
 * Wskazanie, czy wybrana godzina mieści się w którymś z terminów.
 * Ogłoszenie wybranego terminu po naciśnięciu Tab.
 * Inteligentne filtrowanie daty, aby ogłosić datę tylko wtedy, gdy nowo wybrana godzina lub termin przypada na inny dzień niż ostatni.
* Ulepszona obsługa skrzynki odbiorczej i innych list wiadomości w programie Microsoft Outlook 2010 i nowszych (#3834), w tym:
 * Możliwość wyciszenia nagłówków kolumn (od, temat itp.) poprzez wyłączenie opcji Nagłówki wierszy i kolumn tabeli raportu w ustawieniach formatowania dokumentu.
 * Możliwość korzystania z poleceń nawigacji po tabeli (control + alt + strzałki) do poruszania się po poszczególnych kolumnach.
* Microsoft word: Jeśli obraz w wierszu nie ma ustawionego tekstu alternatywnego, NVDA zamiast tego poda tytuł obrazu, jeśli autor go podał. (#4193)
* Microsoft Word: NVDA może teraz raportować wcięcia akapitów za pomocą polecenia formatowania raportu (NVDA+f). Może być również raportowany automatycznie, gdy w ustawieniach formatowania dokumentu jest włączona nowa opcja wcięcia akapitu raportu. (#4165)
* Zgłaszanie automatycznie wstawionego tekstu, takiego jak nowy punktor, wcięcie numeru lub tabulatora po naciśnięciu Enter w edytowalnych dokumentach i polach tekstowych. (#4185)
* Microsoft word: Naciśnięcie NVDA+alt+c spowoduje wyświetlenie tekstu komentarza, jeśli kursor znajduje się w jego obrębie. (#3528)
* Ulepszona obsługa automatycznego odczytywania nagłówków kolumn i wierszy w programie Microsoft Excel (#3568), w tym:
 * Obsługa zakresów nazw zdefiniowanych przez program Excel w celu identyfikacji komórek nagłówka (kompatybilna z czytnikiem ekranu Jaws).
 * Polecenia ustaw nagłówek kolumny (NVDA+shift+c) i ustaw nagłówek wiersza (NVDA+shift+r) przechowują teraz ustawienia w arkuszu, dzięki czemu są dostępne przy następnym otwarciu arkusza i będą dostępne dla innych czytników ekranu obsługujących zdefiniowany schemat zakresu nazw.
 * Te polecenia mogą być teraz używane wiele razy na arkuszu, aby ustawić różne nagłówki dla różnych regionów.
* Obsługa automatycznego odczytywania nagłówków kolumn i wierszy w programie Microsoft Word (#3110), w tym:
 * Obsługa zakładek Microsoft Word do identyfikacji komórek nagłówka (kompatybilna z czytnikiem ekranu Jaws).
 - ustaw komendy nagłówka kolumny (NVDA+shift+c) i ustaw nagłówek wiersza (NVDA+shift+r) podczas gdy na pierwszej komórce nagłówka w tabeli pozwalają powiedzieć NVDA, że te nagłówki powinny być raportowane automatycznie.  Ustawienia są przechowywane w dokumencie, dzięki czemu są dostępne przy następnym otwarciu dokumentu i będą dostępne dla innych czytników ekranu obsługujących schemat zakładek.
* Microsoft Word: Podaj odległość od lewej krawędzi strony po naciśnięciu Tab. (#1353)
* Microsoft Word: przekazywanie informacji zwrotnych w mowie i alfabecie Braille'a dla większości dostępnych skrótów formatowania (pogrubienie, kursywa, podkreślenie, wyrównanie, poziom konspektu, indeks górny, indeks dolny i rozmiar czcionki). (#1353)
* Microsoft Excel: Jeśli zaznaczona komórka zawiera komentarze, można je teraz zgłosić, naciskając NVDA+alt+c. (#2920)
* Microsoft Excel: Udostępnij okno dialogowe specyficzne dla NVDA, aby edytować komentarze w aktualnie wybranej komórce po naciśnięciu polecenia Excela shift + f2 w celu przejścia do trybu edycji komentarzy. (#2920)
* Microsoft Excel: informacje zwrotne dotyczące mowy i alfabetu Braille'a dla wielu innych skrótów ruchu zaznaczania (#4211), w tym:
 * Pionowy ruch strony (pageUp i pageDown);
 * Poziome przesuwanie strony (alt+pageUp i alt+pageDown);
 * Rozszerz zaznaczenie (powyższe z dodanym Shift); i
 * Wybieranie bieżącego regionu (control+shift+8).
* Microsoft Excel: Wyrównanie komórek w pionie i poziomie można teraz raportować za pomocą polecenia formatowania raportu (NVDA+f). Może być również raportowany automatycznie, jeśli jest włączona opcja Wyrównanie raportu w ustawieniach formatowania dokumentu. (#4212)
* Microsoft Excel: Styl komórki może być teraz raportowany za pomocą polecenia formatowania raportu (NVDA+f). Może być również raportowany automatycznie, jeśli jest włączona opcja Styl raportu w ustawieniach formatowania dokumentu. (#4213)
* Microsoft PowerPoint: podczas przenoszenia kształtów wokół slajdu za pomocą strzałek jest teraz zgłaszana bieżąca lokalizacja kształtu (#4214), w tym:
 * Podana jest odległość między kształtem a każdą z krawędzi suwaka.
 * Jeśli kształt zakrywa inny kształt lub jest przez niego pokryty, podawana jest odległość nakładająca się i nakładający się kształt.
 * Aby zgłosić te informacje w dowolnym momencie bez przesuwania kształtu, naciśnij polecenie lokalizacji raportu (NVDA+delete).
 * Podczas wybierania kształtu, jeśli jest on zakryty przez inny kształt, NVDA poinformuje, że jest on zasłonięty.
* Polecenie lokalizacji raportu (NVDA+delete) jest w niektórych sytuacjach bardziej zależne od kontekstu. (#4219)
 * W standardowych polach edycyjnych i trybie przeglądania podawana jest pozycja kursora w procentach przez zawartość i jej współrzędne ekranu.
 * W przypadku kształtów w prezentacjach programu PowerPoint jest raportowane położenie kształtu względem slajdu i innych kształtów.
 * Dwukrotne naciśnięcie tego polecenia spowoduje wcześniejsze działanie polegające na raportowaniu informacji o lokalizacji dla całego elementu sterującego.
* Nowy język: kataloński.

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.5.4. (#4103)

### Poprawki błędów

* W Google Chrome i przeglądarkach opartych na Chrome niektóre fragmenty tekstu (np. te z wyróżnieniem) nie są już powtarzane podczas zgłaszania tekstu alertu lub okna dialogowego. (#4066)
* W trybie przeglądania w aplikacjach Mozilli naciśnięcie Enter na przycisku itp. nie powoduje już jego aktywacji (lub aktywuje niewłaściwą kontrolkę) w niektórych przypadkach, takich jak przyciski u góry Facebooka. (#4106)
* Bezużyteczne informacje nie są już ogłaszane podczas wchodzenia w stan tabletu w iTunes. (#4128)
* Na niektórych listach w programie iTunes, takich jak lista Muzyka, przechodzenie do następnej rzeczy za pomocą nawigacji po obiektach działa teraz poprawnie. (#4129)
* Elementy HTML traktowane jako nagłówki ze względu na znaczniki WAI ARIA są teraz uwzględniane na liście elementów w trybie przeglądania i szybkiej nawigacji w dokumentach programu Internet Explorer. (#4140)
* Podążanie za linkami do tej samej strony w najnowszych wersjach programu Internet Explorer teraz poprawnie powoduje przejście do pozycji docelowej w dokumentach w trybie przeglądania i raportowanie jej. (#4134)
* Microsoft Outlook 2010 i nowsze wersje: Poprawiono ogólny dostęp do bezpiecznych okien dialogowych, takich jak Nowe profile i okna dialogowe konfiguracji poczty. (#4090, #4091, #4095)
* Microsoft Outlook: Zmniejszono bezużyteczną szczegółowość pasków narzędzi poleceń podczas przechodzenia przez niektóre okna dialogowe. (#4096, #3407)
* Microsoft Word: Naciśnięcie Tab do pustej komórki w tabeli nie powoduje już błędnego powiadomienia o zamknięciu tabeli. (#4151)
* Microsoft Word: Pierwszy znak znajdujący się za końcem tabeli (w tym nowy pusty wiersz) nie jest już błędnie uznawany za znajdujący się wewnątrz tabeli. (#4152)
* Okno dialogowe sprawdzania pisowni w programie Microsoft Word 2010: Zgłaszany jest rzeczywisty błędnie napisany wyraz, a nie tylko pierwszy pogrubiony wyraz. (#3431)
* W trybie przeglądania w programie Internet Explorer i innych formantach MSHTML naciśnięcie Tab lub użycie nawigacji jednoliterowej w celu przejścia do pól formularza powoduje ponowne wyświetlenie etykiety w wielu przypadkach, w których tak nie było (w szczególności tam, gdzie są używane elementy etykiety HTML). (#4170)
* Microsoft Word: Zgłaszanie istnienia i umieszczania komentarzy jest dokładniejsze. (#3528)
* Nawigacja w niektórych oknach dialogowych w produktach MS Office, takich jak Word, Excel i Outlook, została ulepszona poprzez zaprzestanie raportowania określonych pasków narzędzi kontenerów kontrolnych, które nie są przydatne dla użytkownika. (#4198)
* Okienka zadań, takie jak menedżer schowka lub Odzyskiwanie plików, nie wydają się już przypadkowo skupiać podczas otwierania aplikacji, takiej jak Microsoft Word lub Excel, co czasami powodowało, że użytkownik musiał przełączać się z aplikacji i wracać do niej, aby korzystać z dokumentu lub arkusza kalkulacyjnego.  (#4199)
* NVDA nie działa już nieprawidłowo w najnowszych systemach operacyjnych Windows, jeśli język Windows użytkownika jest ustawiony na serbski (łaciński). (#4203)
* Naciśnięcie numlock w trybie pomocy wprowadzania danych teraz poprawnie przełącza numlock, zamiast powodować brak synchronizacji klawiatury i systemu operacyjnego w odniesieniu do stanu tego. (#4226)
* W przeglądarce Google Chrome tytuł dokumentu jest ponownie zgłaszany podczas przełączania kart. W NVDA 2014.2 nie występowało to w niektórych przypadkach. (#4222)
* W Google Chrome i przeglądarkach opartych na Chrome adres URL dokumentu nie jest już podawany podczas zgłaszania dokumentu. (#4223)
* Podczas uruchamiania say all z zaznaczoną opcją Brak syntezatora mowy (przydatne w testach automatycznych) powiedz, że wszystko zostanie teraz ukończone, zamiast zatrzymywać się po kilku pierwszych wierszach. (#4225)
* Okno dialogowe Podpis programu Microsoft Outlook: Pole edycji podpisu jest teraz dostępne, co pozwala na pełne śledzenie kursora i wykrywanie formatu. (#3833)
* Microsoft Word: Podczas odczytywania ostatniego wiersza komórki tabeli cała komórka tabeli nie jest już odczytywana. (#3421)
* Microsoft Word: Podczas czytania pierwszego lub ostatniego wiersza spisu treści cały spis treści nie jest już czytany. (#3421)
* Podczas wypowiadania słów pisanych na maszynie i w niektórych innych przypadkach słowa nie są już nieprawidłowo łamane przy znakach, takich jak znaki samogłoskowe i virama w językach indyjskich. (#4254)
* Numeryczne edytowalne pola tekstowe w GoldWave są teraz obsługiwane poprawnie. (#670)
* Microsoft Word: podczas przechodzenia według akapitu za pomocą control+strzałka w dół / control+strzałka w górę, nie trzeba już naciskać ich dwukrotnie, jeśli poruszasz się po listach punktowanych lub numerowanych. (#3290)

### Zmiany dla deweloperów

* NVDA ma teraz ujednolicone wsparcie dla dokumentacji dodatków. Szczegółowe informacje można znaleźć w sekcji Dokumentacja dodatku w Podręczniku programisty. (#2694)
* Podczas dostarczania powiązań gestów w obiekcie ScriptableObject za pośrednictwem __gestures można teraz podać słowo kluczowe None jako skrypt. Spowoduje to usunięcie powiązania gestu we wszystkich klasach bazowych. (#4240)
* Możliwa jest teraz zmiana skrótu używanego do uruchamiania NVDA dla lokalizacji, w których normalny skrót powoduje problemy. (#2209)
 * Odbywa się to za pomocą gettext.
 * Zauważ, że tekst opcji Utwórz skrót na pulpicie w oknie dialogowym Zainstaluj NVDA, a także skrótu w Podręczniku użytkownika, również muszą zostać zaktualizowane.

## 2014.2

### Nowe funkcje

* Ogłaszanie wyboru tekstu jest teraz możliwe w niektórych niestandardowych polach edycji, w których używane są informacje wyświetlane. (#770)
* W dostępnych aplikacjach Java informacje o położeniu są teraz ogłaszane dla przycisków radiowych i innych kontrolek, które uwidaczniają informacje o grupie. (#3754)
* W dostępnych aplikacjach Java skróty klawiaturowe są teraz ogłaszane dla kontrolek, które je zawierają. (#3881)
* W trybie przeglądania są teraz raportowane etykiety punktów orientacyjnych. Są one również zawarte w oknie dialogowym Lista elementów. (#1195)
* W trybie przeglądania oznaczone regiony są teraz traktowane jako punkty orientacyjne. (#3741)
* W dokumentach i aplikacjach Internet Explorer obsługiwane są teraz obszary dynamiczne (część standardu W3c ARIA), dzięki czemu autorzy stron internetowych mogą oznaczać określoną zawartość, która ma być automatycznie odczytywana w miarę jej zmian. (#1846)

### Zmiany

* Po zamknięciu okna dialogowego lub aplikacji w dokumencie w trybie przeglądania nazwa i typ dokumentu w trybie przeglądania nie są już ogłaszane. (#4069)

### Poprawki błędów

* Standardowe menu systemu Windows nie jest już przypadkowo wyciszone w aplikacjach Java. (#3882)
* Podczas kopiowania tekstu z podglądu ekranu podziały wierszy nie są już ignorowane. (#3900)
* Bezsensowne białe znaki nie są już zgłaszane w niektórych aplikacjach, gdy zmienia się fokus lub gdy używana jest nawigacja po obiektach z włączonym prostym przeglądaniem. (#3839)
* Okna komunikatów i inne okna dialogowe tworzone przez NVDA ponownie powodują, że poprzednia mowa jest anulowana przed ogłoszeniem okna dialogowego.
* W trybie przeglądania etykiety kontrolek, takich jak łącza i przyciski, są teraz poprawnie renderowane tam, gdzie etykieta została zastąpiona przez autora ze względu na ułatwienia dostępu (w szczególności przy użyciu aria-label lub aria-labelledby). (#1354)
* W trybie przeglądania w Internet Explorerze tekst zawarty w elemencie oznaczonym jako prezentacyjny (ARIA role="presentation") nie jest już niewłaściwie ignorowany. (#4031)
* Teraz znów można pisać tekst w języku wietnamskim za pomocą oprogramowania Unikey. Aby to zrobić, odznacz nowe pole wyboru Handle keys from other applications (Przełącz z innych aplikacji) w oknie dialogowym ustawień klawiatury NVDA. (#4043)
* W trybie przeglądania elementy menu radia i wyboru są zgłaszane jako kontrolki, a nie tylko tekst, który można kliknąć. (#4092)
* NVDA nie przełącza się już nieprawidłowo z trybu ostrości na tryb przeglądania, gdy zogniskowany jest element menu radia lub wyboru. (#4092)
* W programie Microsoft PowerPoint z włączoną funkcją mówienia o wpisanych słowach znaki wymazane za pomocą Backspace nie są już ogłaszane jako część wpisywanego słowa. (#3231)
* W oknach dialogowych opcji pakietu Microsoft Office 2010 etykiety pól kombi są poprawnie raportowane. (#4056)
* W trybie przeglądania w aplikacjach Mozilli używanie poleceń szybkiej nawigacji w celu przejścia do następnego lub poprzedniego przycisku lub pola formularza zawiera teraz przyciski przełączania zgodnie z oczekiwaniami. (#4098)
* Treść alertów w aplikacjach Mozilli nie jest już raportowana dwukrotnie. (#3481)
* W trybie przeglądania kontenery i punkty orientacyjne nie są już nieprawidłowo powtarzane podczas nawigacji w ich obrębie w tym samym czasie, gdy zmienia się zawartość strony (np. poruszanie się po witrynach Facebook i Twitter). (#2199)
* NVDA przywraca działanie w większej liczbie przypadków po przełączeniu się z aplikacji, które przestają odpowiadać. (#3825)
* Daszek (punkt wstawiania) jest ponownie poprawnie aktualizowany podczas wykonywania polecenia sayAll w edytowalnym tekście narysowanym bezpośrednio na ekranie. (#4125)

## 2014.1

### Nowe funkcje

* Obsługa programu Microsoft PowerPoint 2013. Należy pamiętać, że widok chroniony nie jest obsługiwany. (#3578)
* W programach Microsoft Word i Excel, NVDA może teraz odczytać wybrany symbol podczas wybierania symboli za pomocą okna dialogowego Wstaw symbole. (#3538)
* Teraz można wybrać, czy zawartość w dokumentach ma być identyfikowana jako klikalna, za pomocą nowej opcji w oknie dialogowym ustawień formatowania dokumentu. Ta opcja jest domyślnie włączona zgodnie z poprzednim zachowaniem. (#3556)
* Obsługa monitorów brajlowskich podłączonych przez Bluetooth na komputerze z oprogramowaniem Widcomm Bluetooth. (#2418)
* Podczas edytowania tekstu w programie PowerPoint są teraz zgłaszane hiperłącza. (#3416)
* W aplikacjach ARIA lub oknach dialogowych w Internecie można teraz zmusić NVDA do przełączenia w tryb przeglądania za pomocą NVDA+space, co pozwala na nawigację w stylu dokumentu aplikacji lub okna dialogowego. (#2023)
* W programie Outlook Express / Windows Mail / Windows Live Mail NVDA informuje teraz, czy wiadomość zawiera załącznik lub jest oflagowana. (#1594)
* Podczas nawigowania po tabelach w dostępnych aplikacjach Java raportowane są teraz współrzędne wierszy i kolumn, w tym nagłówki kolumn i wierszy, jeśli istnieją. (#3756)

### Zmiany

* W przypadku monitorów brajlowskich Papenmeier usunięto polecenie przejścia do płaskiego podglądu/ostrości. Użytkownicy mogą przypisywać własne za pomocą okna dialogowego Gesty wprowadzania. (#3652)
* NVDA opiera się teraz na środowisku uruchomieniowym Microsoft VC w wersji 11, co oznacza, że nie można go już uruchomić w systemach operacyjnych starszych niż Windows XP Service Pack 2 lub Windows Server 2003 Service Pack 1.
* Poziom interpunkcji Niektórzy będą teraz mówić znakami gwiazdki (*) i plus (+). (#3614)
* Zaktualizowano eSpeak do wersji 1.48.04, która zawiera wiele poprawek językowych i naprawia kilka awarii. (#3842, #3739, #3860)

### Poprawki błędów

* Podczas przesuwania lub zaznaczania komórek w Microsoft Excel, NVDA nie powinno już niewłaściwie ogłaszać starej komórki zamiast nowej komórki, gdy Microsoft Excel wolno przesuwa zaznaczenie. (#3558)
* NVDA poprawnie obsługuje otwieranie listy rozwijanej dla komórki w programie Microsoft Excel za pomocą menu kontekstowego. (#3586)
* Nowa zawartość strony na stronach sklepu iTunes 11 jest teraz wyświetlana poprawnie w trybie przeglądania po kliknięciu łącza w sklepie lub po początkowym otwarciu sklepu. (#3625)
* Przyciski do podglądu utworów w sklepie iTunes 11 pokazują teraz ich etykiety w trybie przeglądania. (#3638)
* W trybie przeglądania w przeglądarce Google Chrome etykiety pól wyboru i przycisków radiowych są teraz poprawnie renderowane. (#1562)
* W Instantbird NVDA nie zgłasza już bezużytecznych informacji za każdym razem, gdy przechodzisz do kontaktu na liście kontaktów. (#2667)
* W trybie przeglądania w programie Adobe Reader renderowany jest teraz prawidłowy tekst dla przycisków itp., w których etykieta została zastąpiona za pomocą podpowiedzi lub w inny sposób. (#3640)
* W trybie przeglądania w programie Adobe Reader obca grafika zawierająca tekst "mc-ref" nie będzie już renderowana. (#3645)
* NVDA nie raportuje już wszystkich komórek w programie Microsoft Excel zgodnie z podkreśleniami w ich informacjach o formatowaniu. (#3669)
* Nie są już wyświetlane bezsensowne znaki w dokumentach trybu przeglądania, takich jak te znalezione w zakresie prywatnego użycia Unicode. W niektórych przypadkach uniemożliwiało to wyświetlanie bardziej użytecznych etykiet. (#2963)
* Kompozycja wejściowa do wprowadzania znaków wschodnioazjatyckich nie kończy się już niepowodzeniem w programie PuTTY. (#3432)
* Poruszanie się po dokumencie po anulowaniu powiedz wszystko nie powoduje już, że NVDA czasami błędnie informuje, że pozostawiłeś pole (takie jak tabela) niżej w dokumencie, w którym powiedzenie wszystko nigdy nie zostało wypowiedziane. (#3688)
* Podczas korzystania z poleceń szybkiej nawigacji w trybie przeglądania, powiedzmy, z włączonym odczytem skim, NVDA dokładniej ogłasza nowe pole; Np. teraz mówi, że nagłówek jest nagłówkiem, a nie tylko jego tekstem. (#3689)
* Polecenia szybkiej nawigacji z przeskokiem do końca lub początku kontenera honorują teraz odczyt odtłuszczania podczas, powiedzmy wszystkiego, ustawienia; Oznacza to, że nie będą już anulować bieżącego powiedzenia wszystkiego. (#3675)
* Nazwy gestów dotykowych wymienione w oknie dialogowym Gesty wejściowe NVDA są teraz przyjazne i zlokalizowane. (#3624)
* NVDA nie powoduje już zawieszania się niektórych programów po najechaniu myszą na ich elementy sterujące edycją bogatą (TRichEdit). Programy obejmują Jarte 5.1 i BRfácil. (#3693, #3603, #3581)
* W programie Internet Explorer i innych formantach MSHTML kontenery, takie jak tabele oznaczone przez ARIA jako prezentacja, nie są już raportowane do użytkownika. (#3713)
* w Microsoft Word, NVDA nie powtarza już nieprawidłowo wielokrotnie informacji o wierszach i kolumnach tabeli dla komórki na monitorze brajlowskim. (#3702)
* W językach, w których spacja jest separatorem grup cyfr/tysięcy, takich jak francuski i niemiecki, liczby z oddzielnych fragmentów tekstu nie są już wymawiane jako pojedyncza liczba. Było to szczególnie problematyczne w przypadku komórek tabeli zawierających liczby. (#3698)
* Pismo Braille'a nie aktualizuje się już czasami po przeniesieniu daszka systemowego w programie Microsoft Word 2013. (#3784)
* Po umieszczeniu na pierwszym znaku nagłówka w programie Microsoft Word tekst komunikujący go jako nagłówek (łącznie z poziomem) nie znika już z monitora brajlowskiego. (#3701)
* Gdy dla aplikacji zostanie wyzwolony profil konfiguracyjny i ta aplikacja zostanie zamknięta, NVDA nie może już czasami dezaktywować profilu. (#3732)
* Podczas wprowadzania danych azjatyckich do kontrolki w samym NVDA (np. w oknie dialogowym Znajdź w trybie przeglądania), "NVDA" nie jest już niepoprawnie zgłaszane w miejsce kandydata. (#3726)
* Karty w oknie dialogowym opcji programu Outlook 2013 są teraz raportowane. (#3826)
* Ulepszona obsługa regionów ARIA Live w Firefoksie i innych aplikacjach Mozilla Gecko:
 * Obsługa aktualizacji aria-atomic i filtrowanie aktualizacji aria-zajętych. (#2640)
 * Tekst alternatywny (taki jak atrybut alt lub aria-label) jest dołączany, jeśli nie ma innego użytecznego tekstu. (#3329)
 * Aktualizacje regionu dynamicznego nie są już wyciszane, jeśli występują w tym samym czasie, co ruch fokusu. (#3777)
* Niektóre elementy prezentacji w Firefoksie i innych aplikacjach Mozilla Gecko nie są już nieprawidłowo wyświetlane w trybie przeglądania (w szczególności, gdy element jest oznaczony jako aria-presentation, ale można go również skupić). (#3781)
* Poprawa wydajności podczas nawigowania po dokumencie w programie Microsoft Word z włączonymi błędami ortograficznymi. (#3785)
* Kilka poprawek w obsłudze dostępnych aplikacji Java:
 * Początkowo aktywna kontrolka w ramce lub oknie dialogowym nie jest już niezgłaszana, gdy ramka lub okno dialogowe znajdzie się na pierwszym planie. (#3753)
 * Nieprzydatne informacje o pozycji nie są już ogłaszane dla przycisków opcji (np. 1 z 1). (#3754)
 * Lepsze raportowanie kontrolek JComboBox (html nie jest już raportowany, lepsze raportowanie stanów rozwiniętych i zwiniętych). (#3755)
 * Podczas raportowania tekstu okien dialogowych uwzględniany jest teraz tekst, którego wcześniej brakowało. (#3757)
 * Zmiany nazwy, wartości lub opisu ukierunkowanej kontrolki są teraz raportowane dokładniej. (#3770)
* Naprawiono awarię NVDA występującą w systemie Windows 8 podczas skupiania się na niektórych kontrolkach RichEdit zawierających duże ilości tekstu (np. przeglądarka dzienników NVDA, windbg). (#3867)
* W systemach z ustawieniem wyświetlania o wysokiej rozdzielczości DPI (co występuje domyślnie dla wielu nowoczesnych ekranów), NVDA nie kieruje już myszy w niewłaściwe miejsce w niektórych aplikacjach. (#3758, #3703)
* Naprawiono sporadyczny problem podczas przeglądania sieci, w którym NVDA przestawała działać poprawnie do momentu ponownego uruchomienia, mimo że nie ulegała awarii ani nie zawieszała się. (#3804)
* Monitor brajlowski Papenmeier może być teraz używany nawet wtedy, gdy monitor Papenmeier nigdy nie był podłączony przez USB. (#3712)
* NVDA nie zawiesza się już, gdy monitor brajlowski Papenmeier BRAILLEX starszego modelu jest wybrany bez podłączonego monitora.

### Zmiany dla deweloperów

* AppModules zawierają teraz właściwości productName i productVersion. Te informacje są teraz również zawarte w informacjach dla programistów (NVDA+f1). (#1625)
* W konsoli języka Python możesz teraz nacisnąć Tab, aby ukończyć bieżący identyfikator. (#433)
 * Jeśli istnieje wiele możliwości, możesz nacisnąć Tab po raz drugi, aby wybrać z listy.

## 2013.3

### Nowe funkcje

* Pola formularzy są teraz raportowane w dokumentach programu Microsoft Word. (#2295)
* NVDA może teraz ogłaszać informacje o poprawkach w programie Microsoft Word, gdy włączona jest funkcja śledzenia zmian. Zauważ, że wersje edytora raportów w oknie dialogowym ustawień dokumentu NVDA (domyślnie wyłączone) muszą być również włączone, aby mogły być ogłaszane. (#1670)
* Listy rozwijane w programie Microsoft Excel od 2003 do 2010 są teraz ogłaszane po otwarciu i nawigacji. (#3382)
* nowa opcja "Zezwalaj na czytanie przeglądane w Powiedz wszystko" w oknie dialogowym Ustawienia klawiatury umożliwia nawigację po dokumencie za pomocą trybu szybkiej nawigacji i poleceń przesuwania wierszy / akapitów, pozostając w trybie powiedz wszystko. Ta opcja jest domyślnie wyłączona. (#2766)
* Dodano okno dialogowe Gesty wprowadzania, które umożliwia prostsze dostosowywanie gestów wejściowych (takich jak na klawiaturze) dla poleceń NVDA. (#1532)
* Teraz możesz mieć różne ustawienia dla różnych sytuacji za pomocą profilów konfiguracji. Profile mogą być aktywowane ręcznie lub automatycznie (np. dla konkretnego zastosowania). (#87, #667, #1913)
* W programie Microsoft Excel komórki, które są łączami, są teraz ogłaszane jako łącza. (#3042)
* W programie Microsoft Excel użytkownik jest teraz informowany o istnieniu komentarzy w komórce. (#2921)

### Poprawki błędów

* Zend Studio działa teraz tak samo jak Eclipse. (#3420)
* Zmieniony stan niektórych pól wyboru w oknie dialogowym reguł wiadomości programu Microsoft Outlook 2010 jest teraz raportowany automatycznie. (#3063)
* NVDA będzie teraz raportować stan przypiętych elementów sterujących, takich jak karty w przeglądarce Mozilla Firefox. (#3372)
* Teraz możliwe jest powiązanie skryptów z gestami klawiaturowymi zawierającymi Alt i/lub Windows jako modyfikatory. Wcześniej, jeśli zostało to zrobione, wykonanie skryptu spowodowało aktywację menu Start lub paska menu. (#3472)
* Zaznaczanie tekstu w dokumentach w trybie przeglądania (np. za pomocą Control+Shift+End) nie powoduje już przełączenia układu klawiatury w systemach z zainstalowanymi wieloma układami klawiatury. (#3472)
* Internet Explorer nie powinien się już zawieszać ani stawać się bezużyteczny po zamknięciu NVDA. (#3397)
* Ruch fizyczny i inne zdarzenia na niektórych nowszych komputerach nie są już traktowane jako niewłaściwe naciśnięcia. Poprzednio wyciszało to mowę i czasami uruchamiało polecenia NVDA. (#3468)
* NVDA zachowuje się teraz zgodnie z oczekiwaniami w Poedit 1.5.7. Użytkownicy korzystający z wcześniejszych wersji będą musieli dokonać aktualizacji. (#3485)
* NVDA może teraz odczytywać chronione dokumenty w programie Microsoft Word 2010, nie powodując już awarii programu Microsoft Word. (#1686)
* Jeśli podczas uruchamiania pakietu dystrybucyjnego NVDA zostanie podany nieznany przełącznik wiersza poleceń, nie powoduje to już niekończącej się pętli okien dialogowych z komunikatami o błędach. (#3463)
* NVDA nie zgłasza już tekstu alternatywnego grafiki i obiektów w Microsoft Word, jeśli tekst alternatywny zawiera cudzysłowy lub inne niestandardowe znaki. (#3579)
* Liczba elementów dla niektórych list poziomych w trybie przeglądania jest teraz poprawna. Wcześniej mogła to być dwukrotność rzeczywistej kwoty. (#2151)
* Po naciśnięciu control+a w arkuszu programu Microsoft Excel zostanie teraz zgłoszony zaktualizowany wybór. (#3043)
* NVDA może teraz poprawnie odczytywać dokumenty XHTML w Microsoft Internet Explorer i innych kontrolkach MSHTML. (#3542)
* Okno dialogowe ustawień klawiatury: jeśli żaden nie został wybrany jako NVDA, użytkownik otrzymuje komunikat o błędzie podczas zamykania okna dialogowego. Do poprawnego korzystania z NVDA musi zostać wybrany co najmniej jeden klucz. (#2871)
* W programie Microsoft Excel NVDA informuje teraz o scalonych komórkach inaczej niż o wielu zaznaczonych komórkach. (#3567)
* Kursor trybu przeglądania nie jest już umieszczany nieprawidłowo po opuszczeniu okna dialogowego lub aplikacji w dokumencie. (#3145)
* Naprawiono błąd, który powodował, że sterownik monitora brajlowskiego HumanWare Brailliant z serii BI/B nie był wyświetlany jako opcja w oknie dialogowym Ustawienia brajla w niektórych systemach, mimo że taki monitor był podłączony przez USB.
* NVDA nie przerywa już przełączania się na podgląd ekranu, gdy obiekt nawigatora nie ma rzeczywistego położenia na ekranie. W tym przypadku kursor recenzji jest teraz umieszczony w górnej części ekranu. (#3454)
* Naprawiono błąd, który w niektórych okolicznościach powodował awarię sterownika monitora brajlowskiego Freedom Scientific, gdy port był ustawiony na USB. (#3509, #3662)
* Naprawiono błąd, który powodował, że na monitorach brajlowskich Freedom Scientific nie były wykrywane w niektórych okolicznościach. (#3401, #3662)

### Zmiany dla deweloperów

* Kategorię, która ma być wyświetlana użytkownikowi dla skryptów, można określić przy użyciu atrybutu scriptCategory w klasach ScriptableObject i atrybutu kategorii w metodach skryptu. Aby uzyskać więcej informacji, zapoznaj się z dokumentacją baseObject.ScriptableObject . (#1532)
* config.save jest przestarzały i może zostać usunięty w przyszłej wersji. Zamiast tego użyj pliku config.conf.save. (#667)
* config.validateConfig jest przestarzały i może zostać usunięty w przyszłej wersji. Dodatki, które tego wymagają, powinny zapewnić własną implementację. (#667, #3632)

## 2013.2

### Nowe funkcje

* Obsługa Chromium Embedded Framework, który jest kontrolką przeglądarki internetowej używaną w kilku aplikacjach. (#3108)
* Nowy wariant głosowy eSpeak: Iven3.
* W Skypie nowe wiadomości czatu są zgłaszane automatycznie, gdy konwersacja jest skoncentrowana. (#2298)
* Obsługa Tween, w tym raportowanie nazw kart i mniejsza szczegółowość podczas czytania tweetów.
* Można teraz wyłączyć wyświetlanie wiadomości NVDA na monitorze brajlowskim, ustawiając limit czasu wiadomości na 0 w oknie dialogowym Ustawienia brajla. (#2482)
* W Menedżerze dodatków znajduje się teraz przycisk Pobierz dodatki, aby otworzyć stronę internetową dodatków NVDA, gdzie możesz przeglądać i pobierać dostępne dodatki. (#3209)
* W oknie dialogowym NVDA Welcome, które pojawia się zawsze przy pierwszym uruchomieniu NVDA, możesz teraz określić, czy NVDA ma być uruchamiane automatycznie po zalogowaniu się do systemu Windows. (#2234)
* Tryb uśpienia jest automatycznie włączany podczas korzystania z Dolphin Cicero. (#2055)
* Wersja Miranda IM/Miranda NG dla systemu Windows x64 jest teraz obsługiwana. (#3296)
* Sugestie wyszukiwania na ekranie startowym systemu Windows 8.1 są zgłaszane automatycznie. (#3322)
* Obsługa nawigacji i edycji arkuszy kalkulacyjnych w programie Microsoft Excel 2013. (#3360)
* Monitory brajlowskie Freedom Scientific Focus 14 Blue i Focus 80 Blue, a także Focus 40 Blue w niektórych konfiguracjach, które wcześniej nie były obsługiwane, są teraz obsługiwane po połączeniu przez Bluetooth. (#3307)
* Sugestie autouzupełniania są teraz raportowane w programie Outlook 2010. (#2816)
* Nowe tabele tłumaczeń brajlowskich: angielski (Wielka Brytania) komputerowy brajl, koreański klasa 2, rosyjski brajl dla kodu komputerowego.
* Nowy język: perski. (#1427)

### Zmiany

* Na ekranie dotykowym wykonanie jednego ruchu palcem w lewo lub w prawo w trybie obiektu powoduje teraz przejście do przodu lub do następnego przez wszystkie obiekty, a nie tylko te w bieżącym kontenerze. Użyj szybkiego ruchu 2 palcami w lewo lub w prawo, aby wykonać oryginalną czynność przejścia do poprzedniego lub następnego obiektu w bieżącym kontenerze.
* Nazwa pola wyboru Tabele układu raportu znajdująca się w oknie dialogowym Ustawienia trybu przeglądania została teraz zmieniona na Uwzględnij tabele układu, aby odzwierciedlić, że szybka nawigacja również ich nie zlokalizuje, jeśli pole wyboru nie jest zaznaczone. (#3140)
* Płaski podgląd został zastąpiony trybami recenzji obiektów, dokumentów i ekranu. (#2996)
 * Przegląd obiektów przegląda tekst tylko w obiekcie nawigatora, przegląd dokumentu przegląda cały tekst w dokumencie w trybie przeglądania (jeśli istnieje), a przegląd ekranu przegląda tekst na ekranie dla bieżącej aplikacji.
 * Polecenia, które wcześniej przenosiły się do/z recenzji płaskiej, teraz przełączają się między tymi nowymi trybami recenzji.
 * Obiekt nawigatora automatycznie podąża za kursorem recenzji, tak że pozostaje najgłębszym obiektem w miejscu kursora recenzji w trybie recenzji dokumentu lub ekranu.
 * Po przełączeniu w tryb podglądu ekranu, NVDA pozostanie w tym trybie, dopóki jawnie nie przełączysz się z powrotem do trybu podglądu dokumentu lub obiektu.
 * W trybie przeglądania dokumentów lub obiektów, NVDA może automatycznie przełączać się między tymi dwoma trybami w zależności od tego, czy poruszasz się po dokumencie w trybie przeglądania, czy nie.
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.5.3. (#3371)

### Poprawki błędów

* Aktywacja obiektu ogłasza teraz akcję przed aktywacją, a nie akcję po aktywacji (np. rozwinięcie podczas rozwijania, a nie zwijania). (#2982)
* Dokładniejsze odczytywanie i śledzenie kursora w różnych polach wejściowych najnowszych wersji Skype'a, takich jak pola czatu i wyszukiwania. (#1601, #3036)
* Na liście ostatnich konwersacji w Skypie liczba nowych wydarzeń jest teraz odczytywana dla każdej konwersacji, jeśli jest to istotne. (#1446)
* Ulepszenia śledzenia kursora i kolejności czytania tekstu pisanego od prawej do lewej na ekranie; np. edycja tekstu arabskiego w programie Microsoft Excel. (#1601)
* Szybka nawigacja do przycisków i pól formularzy będzie teraz lokalizować łącza oznaczone jako przyciski w celu ułatwień dostępu w programie Internet Explorer. (#2750)
* W trybie przeglądania zawartość wewnątrz widoków drzewa nie jest już renderowana, ponieważ spłaszczona reprezentacja nie jest przydatna. Możesz nacisnąć Enter w widoku drzewa, aby wejść z nim w interakcję w trybie ostrości. (#3023)
* Naciśnięcie alt+strzałka w dół lub alt+strzałka w górę w celu rozwinięcia pola kombi w trybie koncentracji uwagi nie powoduje już nieprawidłowego przełączania w tryb przeglądania. (#2340)
* W programie Internet Explorer 10 komórki tabeli nie aktywują już trybu koncentracji uwagi, chyba że zostały jawnie ustawione z fokusem przez autora sieci Web. (#3248)
* NVDA nie uruchamia się już bez zmian, jeśli czas systemowy jest wcześniejszy niż ostatnie sprawdzenie dostępności aktualizacji. (#3260)
* Jeśli na monitorze brajlowskim wyświetlany jest pasek postępu, jest on aktualizowany po zmianie paska postępu. (#3258)
* W trybie przeglądania w aplikacjach Mozilli podpisy tabel nie są już renderowane dwukrotnie. Ponadto podsumowanie jest renderowane, gdy istnieje również podpis. (#3196)
* Podczas zmiany języków wprowadzania w Windows 8, NVDA mówi teraz w poprawnym języku, a nie w poprzednim.
* NVDA ogłasza teraz zmiany w trybie konwersji IME w systemie Windows 8.
* NVDA nie ogłasza już śmieci na pulpicie, gdy używane są metody wprowadzania IME Google Japanese lub Atok. (#3234)
* W Windows 7 i nowszych NVDA nie ogłasza już nieprawidłowo rozpoznawania mowy lub wprowadzania dotykowego jako zmiany języka klawiatury.
* NVDA nie ogłasza już określonego znaku specjalnego (0x7f) po naciśnięciu Control+Backspace w niektórych edytorach, gdy włączone jest odczytywanie znaków pisanych. (#3315)
* eSpeak nie zmienia już nieprawidłowo tonacji, głośności itp., gdy NVDA odczytuje tekst zawierający określone znaki kontrolne lub XML. (#3334) (regresja #437)
* W aplikacjach Java zmiany etykiety lub wartości kontrolki fokusu są teraz ogłaszane automatycznie i są odzwierciedlane podczas kolejnego wykonywania zapytania dotyczącego kontrolki. (#3119)
* W kontrolkach Scintilla wiersze są teraz poprawnie raportowane, gdy włączone jest zawijanie wierszy. (#885)
* W aplikacjach Mozilli nazwy elementów listy tylko do odczytu są teraz poprawnie raportowane; Np. podczas nawigowania po tweetach w trybie skupienia na twitter.com. (#3327)
* Zawartość okien dialogowych potwierdzenia w pakiecie Microsoft Office 2013 jest teraz automatycznie odczytywana po ich wyświetleniu.
* Ulepszenia wydajności podczas nawigowania po niektórych tabelach w programie Microsoft Word. (#3326)
* Polecenia NVDA do nawigacji po tabelach (control+alt+strzałki) działają lepiej w niektórych tabelach Microsoft Word, gdzie komórka rozciąga się na wiele wierszy.
* Jeśli Menedżer dodatków jest już otwarty, jego ponowna aktywacja (z menu Narzędzia lub poprzez otwarcie pliku dodatku) nie kończy się już niepowodzeniem ani nie uniemożliwia zamknięcia Menedżera dodatków. (#3351)
* NVDA nie zawiesza się już w niektórych oknach dialogowych, gdy używany jest edytor IME pakietu Office 2010 w języku japońskim lub chińskim. (#3064)
* Na monitorach brajlowskich wiele spacji nie jest już kompresowanych do jednej spacji. (#1366)
* Zend Eclipse PHP Developer Tools działa teraz tak samo jak Eclipse. (#3353)
* W przeglądarce Internet Explorer nie jest konieczne naciskanie Tab, aby wchodzić w interakcję z osadzonym obiektem (takim jak zawartość Flash) po naciśnięciu Enter. (#3364)
* Podczas edytowania tekstu w programie Microsoft PowerPoint ostatni wiersz nie jest już raportowany jako wiersz powyżej, jeśli ostatni wiersz jest pusty. (#3403)
* W programie Microsoft PowerPoint obiekty nie są już czasami wypowiadane dwukrotnie po ich zaznaczeniu lub edycji. (#3394)
* NVDA nie powoduje już zawieszania się lub zawieszania programu Adobe Reader w przypadku niektórych źle uformowanych dokumentów PDF zawierających wiersze poza tabelami. (#3399)
* NVDA teraz poprawnie wykrywa następny slajd z fokusem podczas usuwania slajdu w widoku miniatur programu Microsoft PowerPoint. (#3415)

### Zmiany dla deweloperów

* windowUtils.findDescendantWindow został dodany w celu wyszukania okna podrzędnego (HWND) pasującego do określonej widoczności, identyfikatora kontrolki i/lub nazwy klasy.
* Zdalna konsola języka Python nie przekracza już limitu czasu po 10 sekundach podczas oczekiwania na dane wejściowe. (#3126)
* Dołączanie modułu bisect do kompilacji binarnych jest przestarzałe i może zostać usunięte w przyszłej wersji. (#3368)
 * Dodatki, które są zależne od bisect (w tym moduł urllib2) powinny zostać zaktualizowane o ten moduł.

## 2013.1.1

To wydanie rozwiązuje problem polegający na tym, że NVDA ulegało awarii po uruchomieniu, jeśli zostało skonfigurowane do używania języka irlandzkiego, a także zawiera aktualizacje tłumaczeń i kilka innych poprawek błędów.

### Poprawki błędów

* Poprawne znaki są tworzone podczas pisania w interfejsie użytkownika NVDA przy użyciu koreańskiej lub japońskiej metody wprowadzania, podczas gdy jest to metoda domyślna. (#2909)
* W programie Internet Explorer i innych formantach MSHTML pola oznaczone jako zawierające nieprawidłowy wpis są teraz obsługiwane poprawnie. (#3256)
* NVDA nie zawiesza się już po uruchomieniu, jeśli jest skonfigurowana do używania języka irlandzkiego.

## 2013.1

Najważniejsze cechy tej wersji to bardziej intuicyjny i spójny układ klawiatury laptopa; podstawowa obsługa programu Microsoft PowerPoint; obsługa długich opisów w przeglądarkach internetowych; oraz obsługa wprowadzania brajla komputerowego dla monitorów brajlowskich wyposażonych w klawiaturę brajlowską.

### Ważne

#### Nowy układ klawiatury laptopa

Układ klawiatury laptopa został całkowicie przeprojektowany, aby był bardziej intuicyjny i spójny.
Nowy układ używa strzałek w połączeniu z NVDA i innymi modyfikatorami dla poleceń przeglądu.

Zwróć uwagę na następujące zmiany w często używanych poleceniach:

| Nazwa |Klucz|
|---|---|
|Powiedz wszystko |NVDA+a|
|Czytaj bieżącą linię |NVDA+l|
|Odczytywanie bieżącego zaznaczenia tekstu |NVDA+shift+s|
|Pasek stanu raportu |NVDA+shift+koniec|

Ponadto, między innymi, zmieniły się wszystkie polecenia pierścienia nawigacji po obiektach, przeglądania tekstu, kliknięcia myszą i ustawień syntezatora.
Zapoznaj się z dokumentem [Krótki przewodnik po poleceniach](keyCommands.html), aby zapoznać się z nowymi kluczami.

### Nowe funkcje

* Podstawowa obsługa edycji i czytania prezentacji programu Microsoft PowerPoint. (#501)
* Podstawowa obsługa odczytywania i zapisywania wiadomości w programie Lotus Notes 8.5. (#543)
* Obsługa automatycznego przełączania języka podczas czytania dokumentów w programie Microsoft Word. (#2047)
* W trybie przeglądania dla MSHTML (np. Internet Explorer) i Gecko (np. Firefox) ogłaszane jest teraz istnienie długich opisów. Możliwe jest również otwarcie długiego opisu w nowym oknie, naciskając NVDA+d. (#809)
* Powiadomienia w przeglądarce Internet Explorer 9 i nowszych wersjach są teraz odczytywane (takie jak blokowanie zawartości lub pobieranie plików). (#2343)
* Automatyczne raportowanie nagłówków wierszy i kolumn tabeli jest teraz obsługiwane w dokumentach trybu przeglądania w programie Internet Explorer i innych kontrolkach MSHTML. (#778)
* Nowy język: aragoński, irlandzki
* Nowe tabele tłumaczeń brajlowskich: duński stopień 2, koreański stopień 1. (#2737)
* Obsługa monitorów brajlowskich podłączonych przez Bluetooth na komputerze z zainstalowanym oprogramowaniem Bluetooth Stack for Windows firmy Toshiba. (#2419)
* Obsługa wyboru portu podczas korzystania z wyświetlaczy Freedom Scientific (Automatic, USB lub Bluetooth).
* Obsługa rodziny notatników BrailleNote od HumanWare, gdy działają jako terminal brajlowski dla czytnika ekranu. (#2012)
* Obsługa starszych modeli monitorów brajlowskich Papenmeier BRAILLEX. (#2679)
* Obsługa wprowadzania brajla komputerowego dla monitorów brajlowskich wyposażonych w klawiaturę brajlowską. (#808)
* Nowe ustawienia klawiatury, które pozwalają wybrać, czy NVDA ma przerywać mowę dla wpisanych znaków i/lub Enter. (#698)
* Obsługa kilku przeglądarek opartych na Google Chrome: Rockmelt, BlackHawk, Comodo Dragon i SRWare Iron. (#2236, #2813, #2814, #2815)

### Zmiany

* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.5.2. (#2737)
* Układ klawiatury laptopa został całkowicie przeprojektowany, aby był bardziej intuicyjny i spójny. (#804)
* Zaktualizowano syntezator mowy eSpeak do wersji 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

### Poprawki błędów

* szybkiej nawigacji służące do przechodzenia do następnego lub poprzedniego separatora w trybie przeglądania działają teraz w programie Internet Explorer i innych kontrolkach MSHTML. (#2781)
* Jeśli NVDA powróci do eSpeak lub nie będzie mowy z powodu awarii skonfigurowanego syntezatora mowy podczas uruchamiania NVDA, skonfigurowany wybór nie jest już automatycznie ustawiany na syntezator awaryjny. Oznacza to, że teraz oryginalny syntezator zostanie ponownie wypróbowany przy następnym uruchomieniu NVDA. (#2589)
* Jeśli NVDA powróci do stanu braku alfabetu Braille'a z powodu awarii skonfigurowanego monitora brajlowskiego podczas uruchamiania NVDA, skonfigurowany monitor nie jest już automatycznie ustawiany na brak alfabetu Braille'a. Oznacza to, że teraz oryginalny ekran zostanie ponownie wypróbowany przy następnym uruchomieniu NVDA. (#2264)
* W trybie przeglądania w aplikacjach Mozilli aktualizacje tabel są teraz renderowane poprawnie. Na przykład w zaktualizowanych komórkach raportowane są współrzędne wierszy i kolumn, a nawigacja po tabeli działa tak, jak powinna. (#2784)
* W trybie przeglądania w przeglądarkach internetowych niektóre klikalne grafiki bez etykiet, które nie były wcześniej renderowane, są teraz renderowane poprawnie. (#2838)
* Obsługiwane są teraz wcześniejsze i nowsze wersje SecureCRT. (#2800)
* W przypadku metod wprowadzania, takich jak Easy Dots IME w XP, odczytywany ciąg jest teraz poprawnie raportowany.
* Lista kandydatów w chińskiej uproszczonej metodzie wprowadzania Microsoft Pinyin w systemie Windows 7 jest teraz poprawnie odczytywana podczas zmiany stron za pomocą strzałek w lewo i w prawo oraz przy pierwszym otwarciu jej za pomocą strony głównej.
* Po zapisaniu informacji o wymowie symbolu niestandardowego zaawansowane pole "zachowaj" nie jest już usuwane. (#2852)
* Po wyłączeniu automatycznego sprawdzania dostępności aktualizacji, NVDA nie musi być już ponownie uruchamiane, aby zmiana w pełni weszła w życie.
* NVDA nie uruchamia się już, jeśli dodatek nie może zostać usunięty, ponieważ jego katalog jest aktualnie używany przez inną aplikację. (#2860)
* Etykiety kart w oknie dialogowym preferencji DropBox są teraz widoczne za pomocą recenzji płaskiej.
* Jeśli język wprowadzania zostanie zmieniony na inny niż domyślny, NVDA teraz poprawnie wykrywa dla poleceń i trybu pomocy przy wprowadzaniu.
* W przypadku języków takich jak niemiecki, w których znak + (plus) jest pojedynczym na klawiaturze, można teraz powiązać z nim polecenia za pomocą słowa "plus". (#2898)
* W programie Internet Explorer i innych formantach MSHTML cudzysłowy blokowe są teraz raportowane tam, gdzie jest to potrzebne. (#2888)
* Sterownik monitora brajlowskiego HumanWare Brailliant z serii BI/B można teraz wybrać, gdy monitor jest podłączony przez Bluetooth, ale nigdy nie był podłączony przez USB.
* Filtrowanie elementów na liście elementów trybu przeglądania za pomocą wielkich liter w tekście filtru zwraca teraz wyniki bez uwzględniania wielkości liter, tak jak małe litery, a nie nic. (#2951)
* W przeglądarkach Mozilla tryb przeglądania może być ponownie używany, gdy zawartość Flash jest aktywna. (#2546)
* W przypadku korzystania z tabeli brajlowskiej z kontrakcjami i rozwinięcia do alfabetu Braille'a komputerowego dla słowa znajdującego się przy kursorze, kursor brajlowski jest teraz umieszczony poprawnie, gdy znajduje się po słowie, w którym znak jest reprezentowany przez wiele komórek brajlowskich (np. wielka litera, litera, cyfra itp.). (#2947)
* Zaznaczenie tekstu jest teraz poprawnie wyświetlane na monitorze brajlowskim w aplikacjach, takich jak Microsoft Word 2003 i kontrolki edycji Internet Explorer.
* Ponownie możliwe jest zaznaczanie tekstu w kierunku wstecz w programie Microsoft Word, gdy włączony jest alfabet Braille'a.
* Podczas przeglądania, cofania lub usuwania znaków W kontrolkach edycji Scintilla, NVDA poprawnie odczytuje znaki wielobajtowe. (#2855)
* Instalacja NVDA nie będzie już kończyć się niepowodzeniem, gdy ścieżka profilu użytkownika zawiera określone znaki wielobajtowe. (#2729)
* Raportowanie grup dla kontrolek widoku listy (SysListview32) w aplikacjach 64-bitowych nie powoduje już błędu.
* W trybie przeglądania w aplikacjach Mozilli zawartość tekstowa nie jest już niepoprawnie traktowana jako edytowalna w niektórych rzadkich przypadkach. (#2959)
* W programach IBM Lotus Symphony i OpenOffice przesunięcie karetki powoduje teraz przesunięcie kursora recenzji, jeśli jest to konieczne.
* Zawartość Adobe Flash jest teraz dostępna w programie Internet Explorer w systemie Windows 8. (#2454)
* Poprawiono obsługę Bluetooth dla Papenmeier Braillex Trio. (#2995)
* Naprawiono niemożność korzystania z niektórych głosów interfejsu API Microsoft Speech w wersji 5, takich jak głosy Koba Speech 2. (#2629)
* W aplikacjach korzystających z mostka Java Access Bridge monitory brajlowskie są teraz poprawnie aktualizowane, gdy karetka przesuwa się w edytowalnych polach tekstowych. (#3107)
* Obsługa formularza punktu orientacyjnego w dokumentach w trybie przeglądania, które obsługują punkty orientacyjne. (#2997)
* Sterownik syntezatora eSpeak obsługuje teraz czytanie według znaków w bardziej odpowiedni sposób (np. ogłaszanie nazwy lub wartości obcej litery, a nie tylko jej dźwięku lub nazwy ogólnej). (#3106)
* NVDA nie kopiuje już ustawień użytkownika do użycia na ekranach logowania i innych bezpiecznych ekranach, gdy ścieżka profilu użytkownika zawiera znaki spoza ASCII. (#3092)
* NVDA nie zawiesza się już podczas korzystania z wprowadzania znaków azjatyckich w niektórych aplikacjach .NET. (#3005)
* teraz można korzystać z trybu przeglądania stron w przeglądarce Internet Explorer 10 w trybie standardowym; np. strona logowania [www.gmail.com](http://www.gmail.com). (#3151)

### Zmiany dla deweloperów

* Sterowniki monitora brajlowskiego mogą teraz obsługiwać ręczny wybór portów. (#426)
 * Jest to najbardziej przydatne w przypadku monitorów brajlowskich, które obsługują połączenie przez starszy port szeregowy.
 * Odbywa się to za pomocą metody klasy getPossiblePorts w klasie BrailleDisplayDriver.
* Obsługiwane jest teraz wprowadzanie brajlowskie z klawiatur brajlowskich. (#808)
 * Wprowadzanie brajlowskie jest objęte klasą BrailleInput.BrailleInputGesture lub jej podklasą.
 * Podklasy alfabetu Braille'a. BrailleDisplayGesture (zaimplementowany w sterownikach monitorów brajlowskich) może również dziedziczyć po BrailleInput.BrailleInputGesture. Dzięki temu polecenia wyświetlania i wprowadzanie brajlowskie mogą być obsługiwane przez tę samą klasę gestów.
* Możesz teraz użyć comHelper.getActiveObject, aby pobrać aktywny obiekt COM z normalnego procesu, gdy NVDA jest uruchomiona z uprawnieniem UIAccess. (#2483)

## 2012.3

Najważniejsze cechy tego wydania to obsługa wprowadzania znaków azjatyckich; eksperymentalna obsługa ekranów dotykowych w systemie Windows 8; raportowanie numerów stron i ulepszona obsługa tabel w programie Adobe Reader; polecenia nawigacji po tabelach w wierszach tabeli z fokusem i kontrolkach widoku listy systemu Windows; obsługa kilku dodatkowych monitorów brajlowskich; oraz raportowanie nagłówków wierszy i kolumn w programie Microsoft Excel.

### Nowe funkcje

* NVDA może teraz obsługiwać wprowadzanie znaków azjatyckich przy użyciu IME i metod wprowadzania usługi tekstowej we wszystkich aplikacjach, w tym:
 * Raportowanie i nawigacja po listach kandydatów;
 * Raportowanie i nawigacja po ciągach kompozycji; i
 * Raportowanie ciągów odczytu.
* Obecność podkreślenia i przekreślenia jest teraz zgłaszana w dokumentach programu Adobe Reader. (#2410)
* Gdy funkcja Lepkie systemu Windows jest włączona, modyfikujący NVDA będzie teraz zachowywał się jak inne modyfikujące. Pozwala to na korzystanie z modyfikującego NVDA bez konieczności przytrzymywania go podczas naciskania innych. (#230)
* Automatyczne raportowanie nagłówków kolumn i wierszy jest teraz obsługiwane w programie Microsoft Excel. Naciśnij NVDA+shift+c, aby ustawić wiersz zawierający nagłówki kolumn i NVDA+shift+r, aby ustawić kolumnę zawierającą nagłówki wierszy. Naciśnij dowolne polecenie dwa razy w krótkich odstępach czasu, aby wyczyścić ustawienie. (#1519)
* Obsługa monitorów brajlowskich HIMS Braille Sense, Braille EDGE i SyncBraille. (#1266, #1267)
* Gdy pojawią się wyskakujące powiadomienia systemu Windows 8, NVDA zgłosi je, jeśli włączone jest raportowanie dymków pomocy. (#2143)
* Eksperymentalna obsługa ekranów dotykowych w systemie Windows 8, w tym:
 * Czytanie tekstu bezpośrednio pod palcem podczas przesuwania go
 * Wiele gestów do wykonywania nawigacji po obiektach, przeglądania tekstu i innych poleceń NVDA.
* Wsparcie dla VIP Mud. (#1728)
* W programie Adobe Reader, jeśli tabela zawiera podsumowanie, jest ono teraz prezentowane. (#2465)
* W programie Adobe Reader można teraz raportować nagłówki wierszy i kolumn tabeli. (#2193, #2527, #2528)
* Nowe języki: amharski, koreański, nepalski, słoweński.
* NVDA może teraz odczytywać sugestie autouzupełniania podczas wprowadzania adresów e-mail w programie Microsoft Outlook 2007. (#689)
* Nowe warianty głosu eSpeak: Gene, Gene2. (#2512)
* W programie Adobe Reader można teraz raportować numery stron. (#2534)
 * W programie Reader XI etykiety stron są zgłaszane tam, gdzie są obecne, odzwierciedlając zmiany w numeracji stron w różnych sekcjach itp. We wcześniejszych wersjach nie było to możliwe i podawane są tylko kolejne numery stron.
* Teraz możliwe jest zresetowanie konfiguracji NVDA do ustawień fabrycznych poprzez szybkie naciśnięcie NVDA+control+r trzy razy lub wybranie opcji Przywróć ustawienia fabryczne z menu NVDA. (#2086)
* Obsługa monitorów brajlowskich Seika w wersji 3, 4 i 5 oraz Seika80 firmy Nippon Telesoft. (#2452)
* Pierwszy i ostatni górny przycisk przywoływania w monitorach brajlowskich Freedom Scientific PAC, Mate i Focus może być teraz używany do przewijania do tyłu i do przodu. (#2556)
* Monitory brajlowskie Freedom Scientific Focus obsługują wiele innych funkcji, takich jak paski wyprzedzające, belki kołyskowe i niektóre kombinacje kropek dla typowych czynności. (#2516)
* W aplikacjach korzystających z IAccessible2, takich jak aplikacje Mozilli, nagłówki wierszy i kolumn tabeli mogą być teraz raportowane poza trybem przeglądania. (#926)
* Wstępna obsługa formantu dokumentów w programie Microsoft Word 2013. (#2543)
* Wyrównanie tekstu może być teraz raportowane w aplikacjach korzystających z IAccessible2, takich jak aplikacje Mozilli. (#2612)
* Gdy wiersz tabeli lub standardowa kontrolka widoku listy systemu Windows z wieloma kolumnami jest aktywna, można teraz używać poleceń nawigacji po tabeli, aby uzyskać dostęp do poszczególnych komórek. (#828)
* Nowe tabele tłumaczeń brajlowskich: estoński klasy 0, portugalski 8-punktowy komputerowy brajl, włoski 6-punktowy komputerowy brajl. (#2319, #2662)
* Jeśli NVDA jest zainstalowany w systemie, bezpośrednie otwarcie pakietu dodatkowego NVDA (np. z Eksploratora Windows lub po pobraniu w przeglądarce internetowej) spowoduje zainstalowanie go w NVDA. (#2306)
* Obsługa nowszych modeli monitorów brajlowskich Papenmeier BRAILLEX. (#1265)
* Informacje o pozycji (np. 1 z 4) są teraz raportowane dla elementów listy Eksploratora Windows w systemie Windows 7 i nowszych. Obejmuje to również wszystkie kontrolki UIAutomation, które obsługują właściwości niestandardowe itemIndex i itemCount. (#2643)

### Zmiany

* W oknie dialogowym preferencji kursora przeglądu NVDA, opcja Śledź fokus klawiatury została zmieniona na Podążaj za fokusem systemu, aby zachować spójność z terminologią używaną w innych miejscach w NVDA.
* Gdy alfabet Braille'a jest podłączony do przeglądania, a kursor znajduje się na obiekcie, który nie jest obiektem tekstowym (np. edytowalnym polu tekstowym), przywoływania kursora aktywują teraz obiekt. (#2386)
* Opcja Zapisz ustawienia przy wyjściu jest teraz domyślnie włączona dla nowych konfiguracji.
* Podczas aktualizacji poprzednio zainstalowanej kopii NVDA, skrótu na pulpicie nie jest już zmuszany do powrotu do control+alt+n, jeśli został ręcznie zmieniony na coś innego przez użytkownika. (#2572)
* Lista dodatków w Menedżerze dodatków pokazuje teraz nazwę pakietu przed jego stanem. (#2548)
* Jeśli instalujesz tę samą lub inną wersję aktualnie zainstalowanego dodatku, NVDA zapyta, czy chcesz zaktualizować dodatek, zamiast po prostu wyświetlić błąd i przerwać instalację. (#2501)
* Polecenia nawigacji po obiektach (z wyjątkiem polecenia raportowania bieżącego obiektu) są teraz raportowane z mniejszą szczegółowością. Nadal można uzyskać dodatkowe informacje za pomocą polecenia zgłoś bieżący obiekt. (#2560)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.5.1. (#2319, #2480, #2662, #2672)
* Nazwa dokumentu Skrócony przewodnik po poleceniach klawiszowych NVDA została zmieniona na Skrócona instrukcja poleceń, ponieważ zawiera teraz polecenia dotykowe, a także polecenia klawiaturowe.
* Lista elementów w trybie przeglądania będzie teraz zapamiętywać ostatnio wyświetlany typ elementu (np. linki, nagłówki lub punkty orientacyjne) za każdym razem, gdy okno dialogowe jest wyświetlane w ramach tej samej sesji NVDA. (#365)
* Większość aplikacji Metro w systemie Windows 8 (np. Poczta, Kalendarz) nie aktywuje już trybu przeglądania dla całej aplikacji.
* Zaktualizowano Handy Tech BrailleDriver COM-Server do wersji 1.4.2.0.

### Poprawki błędów

* W systemie Windows Vista i nowszych, NVDA nie traktuje już błędnie Windows jako przytrzymanego podczas odblokowywania systemu Windows po zablokowaniu go przez naciśnięcie Windows+l. (#1856)
* W programie Adobe Reader nagłówki wierszy są teraz poprawnie rozpoznawane jako komórki tabeli; Oznacza to, że współrzędne są raportowane i można uzyskać do nich dostęp za pomocą poleceń nawigacji w tabeli. (#2444)
* W programie Adobe Reader komórki tabeli obejmujące więcej niż jedną kolumnę i/lub wiersz są teraz obsługiwane poprawnie. (#2437, #2438, #2450)
* Pakiet dystrybucyjny NVDA sprawdza teraz swoją integralność przed uruchomieniem. (#2475)
* Tymczasowe pliki do pobrania są teraz usuwane, jeśli pobieranie aktualizacji NVDA nie powiedzie się. (#2477)
* NVDA nie będzie się już zawieszać, gdy jest uruchomiony jako administrator podczas kopiowania konfiguracji użytkownika do konfiguracji systemu (do użycia na logowaniu do systemu Windows i innych bezpiecznych ekranach). (#2485)
* Kafelki na ekranie startowym systemu Windows 8 są teraz lepiej prezentowane w mowie i alfabecie Braille'a. Nazwa nie jest już powtarzana, niezaznaczone nie jest już raportowane na wszystkich kafelkach, a informacje o stanie na żywo są prezentowane jako opis kafelka (np. bieżąca temperatura dla kafelka Pogoda).
* Hasła nie są już ogłaszane podczas odczytywania pól haseł w programie Microsoft Outlook i innych standardowych kontrolek edycji, które są oznaczone jako chronione. (#2021)
* W programie Adobe Reader zmiany w polach formularzy są teraz poprawnie odzwierciedlane w trybie przeglądania. (#2529)
* Ulepszenia obsługi modułu sprawdzania pisowni w programie Microsoft Word, w tym dokładniejsze odczytywanie bieżącego błędu pisowni oraz możliwość obsługi modułu sprawdzania pisowni podczas uruchamiania zainstalowanej kopii NVDA w systemie Windows Vista lub nowszym.
* Dodatki, które zawierają pliki zawierające znaki spoza alfabetu angielskiego, mogą być teraz w większości przypadków instalowane poprawnie. (#2505)
* W programie Adobe Reader język tekstu nie jest już tracony po jego zaktualizowaniu lub przewinięciu. (#2544)
* Podczas instalowania dodatku okno dialogowe potwierdzenia wyświetla teraz poprawnie zlokalizowaną nazwę dodatku, jeśli jest dostępna. (#2422)
* W aplikacjach korzystających z automatyzacji interfejsu użytkownika (takich jak aplikacje .NET i Silverlight) poprawiono obliczanie wartości liczbowych dla kontrolek, takich jak suwaki. (#2417)
* Konfiguracja raportowania pasków postępu jest teraz honorowana dla nieokreślonych pasków postępu wyświetlanych przez NVDA podczas instalacji, tworzenia przenośnej kopii, itp. (#2574)
* Polecenia NVDA nie mogą być już wykonywane z monitora brajlowskiego, gdy aktywny jest bezpieczny ekran systemu Windows (taki jak ekran blokady). (#2449)
* W trybie przeglądania pismo Braille'a jest teraz aktualizowane, jeśli zmienia się wyświetlany tekst. (#2074)
* Na bezpiecznym ekranie systemu Windows, takim jak ekran blokady, wiadomości z aplikacji mówiących lub wyświetlających alfabet Braille'a bezpośrednio przez NVDA są teraz ignorowane.
* W trybie przeglądania nie można już spaść z dolnej krawędzi dokumentu za pomocą strzałki w prawo, gdy znajduje się ostatni znak, ani przeskakując na koniec kontenera, gdy ten kontener jest ostatnim elementem w dokumencie. (#2463)
* Niepotrzebna treść nie jest już niepoprawnie uwzględniana podczas raportowania tekstu okien dialogowych w aplikacjach internetowych (w szczególności w oknach dialogowych ARIA bez atrybutu aria-describedby). (#2390)
* NVDA nie raportuje już błędnie ani nie lokalizuje niektórych pól edycyjnych w dokumentach MSHTML (np. Internet Explorer), szczególnie tam, gdzie autor strony internetowej użył jawnej roli ARIA. (#2435)
* Backspace jest teraz poprawnie obsługiwany podczas wypowiadania wpisywanych słów w konsolach poleceń systemu Windows. (#2586)
* Współrzędne komórek w programie Microsoft Excel są teraz ponownie wyświetlane w alfabecie Braille'a.
* W Microsoft Word NVDA nie pozostawia już utknięcia na akapicie z formatowaniem listy podczas próby przejścia nad punktorem lub numerem za pomocą strzałki w lewo lub Control + strzałka w lewo. (#2402)
* W trybie przeglądania w aplikacjach Mozilli elementy w niektórych listach (w szczególności w polach listy ARIA) nie są już niepoprawnie renderowane.
* W trybie przeglądania w aplikacjach Mozilli niektóre kontrolki, które były renderowane z nieprawidłową etykietą lub tylko białymi znakami, są teraz renderowane z poprawną etykietą.
* W trybie przeglądania w aplikacjach Mozilli niektóre zbędne białe znaki zostały wyeliminowane.
* W trybie przeglądania w przeglądarkach internetowych niektóre grafiki, które są jawnie oznaczone jako prezentacyjne (w szczególności z atrybutem alt="") są teraz poprawnie ignorowane.
* W przeglądarkach internetowych, NVDA ukrywa teraz zawartość, która jest oznaczona jako ukryta przed czytnikami ekranu (konkretnie, używając atrybutu aria-hidden). (#2117)
* Ujemne kwoty w walucie (np. -123 USD) są teraz poprawnie odczytywane jako ujemne, niezależnie od poziomu symbolu. (#2625)
* Podczas mówienia wszystkiego, NVDA nie będzie już niepoprawnie przywracać domyślnego języka, w którym wiersz nie kończy zdania. (#2630)
* Informacje o czcionkach są teraz poprawnie wykrywane w programie Adobe Reader 10.1 i nowszych wersjach. (#2175)
* Jeśli w programie Adobe Reader zostanie podany tekst zastępczy, renderowany będzie tylko ten tekst. Wcześniej czasami dołączano zbędny tekst. (#2174)
* Jeśli dokument zawiera aplikację, zawartość aplikacji nie jest już uwzględniana w trybie przeglądania. Zapobiega to nieoczekiwanemu poruszaniu się wewnątrz aplikacji podczas nawigacji. Możesz wchodzić w interakcje z aplikacją w taki sam sposób, jak w przypadku obiektów osadzonych. (#990)
* W aplikacjach Mozilli wartość przycisków pokrętła jest teraz poprawnie raportowana, gdy się zmienia. (#2653)
* Zaktualizowano obsługę programu Adobe Digital Editions, aby działał w wersji 2.0. (#2688)
* Naciśnięcie NVDA+strzałka w górę podczas korzystania z listy rozwijanej w Internet Explorerze i innych dokumentach MSHTML nie będzie już niepoprawnie odczytywać wszystkich elementów. Zamiast tego zostanie odczytany tylko aktywny element. (#2337)
* Słowniki mowy będą teraz poprawnie zapisywane w przypadku użycia znaku cyfry (#) w polach wzorca lub zamiany. (#961)
* Tryb przeglądania dokumentów MSHTML (np. Internet Explorer) teraz poprawnie wyświetla widoczną zawartość zawartą w ukrytej zawartości (w szczególności elementy o stylu visibility:visible wewnątrz elementu ze stylem visibility:hidden). (#2097)
* Łącza w Centrum zabezpieczeń systemu Windows XP nie zawierają już losowych wiadomości-śmieci po swoich nazwach. (#1331)
* Kontrolki tekstowe automatyzacji interfejsu użytkownika (np.  pole wyszukiwania w menu Start systemu Windows 7) są teraz poprawnie ogłaszane po najechaniu na nie myszą, zamiast milczeć.
* Zmiany układu klawiatury nie są już zgłaszane podczas mówienia wszystkiego, co było szczególnie problematyczne w przypadku dokumentów wielojęzycznych, w tym tekstu arabskiego. (#1676)
* Cała zawartość niektórych edytowalnych kontrolek tekstowych automatyzacji interfejsu użytkownika (np. pola wyszukiwania w menu Start systemu Windows 7/8) nie jest już ogłaszana za każdym razem, gdy ulega zmianie.
* Podczas przechodzenia między grupami na ekranie startowym systemu Windows 8 grupy bez etykiet nie ogłaszają już swojego pierwszego kafelka jako nazwy grupy. (#2658)
* Podczas otwierania ekranu startowego systemu Windows 8 fokus jest prawidłowo umieszczany na pierwszym kafelku, a nie przeskakuje do katalogu głównego ekranu startowego, co może zmylić nawigację. (#2720)
* NVDA nie będzie już uruchamiać się nieprawidłowo, gdy ścieżka profilu użytkownika zawiera określone znaki wielobajtowe. (#2729)
* W trybie przeglądania w przeglądarce Google Chrome tekst kart jest teraz renderowany poprawnie.
* W trybie przeglądania przyciski menu są teraz poprawnie raportowane.
* W OpenOffice.org/LibreOffice Calc odczytywanie komórek arkusza kalkulacyjnego działa teraz poprawnie. (#2765)
* NVDA może ponownie funkcjonować na liście wiadomości Yahoo! Mail, gdy jest używany z Internet Explorera. (#2780)

### Zmiany dla deweloperów

* Poprzedni plik dziennika jest teraz kopiowany do nvda-old.log podczas inicjalizacji NVDA. W związku z tym, jeśli NVDA ulegnie awarii lub zostanie ponownie uruchomiona, informacje o rejestrowaniu z tej sesji są nadal dostępne do wglądu. (#916)
* Pobranie właściwości roli w chooseNVDAObjectOverlayClasses nie powoduje już, że rola jest niepoprawna, a tym samym nie jest raportowana w fokusie dla niektórych obiektów, takich jak konsole poleceń systemu Windows i kontrolki Scintilla. (#2569)
* Menu Preferencje, Narzędzia i Pomoc NVDA są teraz dostępne jako atrybuty na gui.mainFrame.sysTrayIcon o nazwach preferencesMenu, toolsMenu i helpMenu, odpowiednio. Dzięki temu wtyczki mogą łatwiej dodawać elementy do tych menu.
* Nazwa skryptu navigatorObject_doDefaultAction w globalCommands została zmieniona na review_activate.
* Konteksty wiadomości Gettext są teraz obsługiwane. Pozwala to na zdefiniowanie wielu tłumaczeń dla jednej wiadomości w języku angielskim w zależności od kontekstu. (#1524)
 * Odbywa się to za pomocą funkcji pgettext(context, message).
 * Jest to obsługiwane zarówno przez samo NVDA, jak i dodatki.
 * xgettext i msgfmt z GNU gettext muszą być użyte do utworzenia dowolnych plików PO i MO. Narzędzia języka Python nie obsługują kontekstów komunikatów.
 * Dla xgettext przekaż argument wiersza poleceń --keyword=pgettext:1c,2, aby umożliwić dołączanie kontekstów komunikatów.
 * Zobacz http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts, aby uzyskać więcej informacji.
* Teraz możliwy jest dostęp do wbudowanych modułów NVDA, w których zostały one nadpisane przez moduły innych firm. Zobacz moduł nvdaBuiltin, aby uzyskać szczegółowe informacje.
* Obsługa tłumaczenia dodatków może być teraz używana w module installTasks dodatku. (#2715)

## 2012.2.1

W tej wersji rozwiązano kilka potencjalnych problemów z zabezpieczeniami (poprzez uaktualnienie języka Python do wersji 2.7.3).

## 2012.2

Najważniejsze cechy tego wydania to wbudowany instalator i funkcja przenośnego tworzenia, automatyczne aktualizacje, łatwe zarządzanie nowymi dodatkami NVDA, zapowiedź grafiki w programie Microsoft Word, obsługa aplikacji w stylu Windows 8 Metro i kilka ważnych poprawek błędów.

### Nowe funkcje

* NVDA może teraz automatycznie sprawdzać, pobierać i instalować aktualizacje. (#73)
* Rozszerzenie funkcjonalności NVDA stało się łatwiejsze dzięki dodaniu Menedżera dodatków (znajdującego się w menu Narzędzia w menu NVDA), który pozwala na instalowanie i odinstalowywanie nowych pakietów dodatków NVDA (plików .nvda-addon) zawierających wtyczki i sterowniki. Zwróć uwagę, że menedżer dodatków nie pokazuje starszych niestandardowych wtyczek i sterowników ręcznie skopiowanych do katalogu konfiguracyjnego. (#213)
* Wiele bardziej popularnych funkcji NVDA działa teraz w aplikacjach w stylu Windows 8 Metro podczas korzystania z zainstalowanej wersji NVDA, w tym mówienie o wpisanych znakach i tryb przeglądania dokumentów internetowych (w tym obsługa wersji Metro Internet Explorera 10). Przenośne kopie NVDA nie mogą uzyskać dostępu do aplikacji w stylu metra. (#1801)
* W dokumentach w trybie przeglądania (Internet Explorer, Firefox itp.) można teraz przeskakiwać do początku i za koniec niektórych elementów zawierających (takich jak listy i tabele) za pomocą odpowiednio shift+ i , . (#123)
* Nowy język: grecki.
* Grafika i tekst alternatywny są teraz raportowane w dokumentach programu Microsoft Word. (#2282, #1541)

### Zmiany

* Ogłaszanie współrzędnych komórek w programie Microsoft Excel odbywa się teraz po zawartości, a nie przed nią, i jest teraz uwzględniane tylko wtedy, gdy w oknie dialogowym Ustawienia formatowania dokumentu są włączone ustawienia tabel raportu i współrzędnych komórki tabeli raportu. (#320)
* NVDA jest teraz dystrybuowany w jednym pakiecie. Zamiast oddzielnych wersji przenośnych i instalacyjnych, jest teraz tylko jeden plik, który po uruchomieniu uruchomi tymczasową kopię NVDA i pozwoli ci zainstalować lub wygenerować przenośną dystrybucję. (#1715)
* NVDA jest teraz zawsze instalowany w Program Files na wszystkich systemach. Aktualizacja poprzedniej instalacji spowoduje również automatyczne przeniesienie jej, jeśli nie była tam wcześniej zainstalowana.

### Poprawki błędów

* Po włączeniu automatycznego przełączania języków, zawartość, taka jak tekst alternatywny dla grafiki i etykiety dla innych elementów sterujących w Mozilla Gecko (np. Firefox), jest teraz raportowana w odpowiednim języku, jeśli jest odpowiednio oznaczona.
* Polecenie SayAll w BibleSeeker (i innych kontrolkach TRxRichEdit) nie zatrzymuje się już w środku fragmentu.
* Listy znajdujące się we właściwościach pliku Eksploratora Windows 8 (karta Zezwolenia) oraz w usłudze Windows Update systemu Windows 8 są teraz odczytywane poprawnie.
* Naprawiono możliwe zawieszanie się gry w MS Word, które powodowało, że pobieranie tekstu z dokumentu zajmowało więcej niż 2 sekundy (bardzo długie wiersze lub spisy treści). (#2191)
* Wykrywanie podziałów wyrazów działa teraz poprawnie, gdy po białych znakach następuje pewna interpunkcja. (#1656)
* W trybie przeglądania w programie Adobe Reader można teraz nawigować do nagłówków bez poziomu za pomocą szybkiej nawigacji i listy elementów. (#2181)
* W Winampie alfabet Braille'a jest teraz poprawnie aktualizowany po przejściu do innego elementu w edytorze list odtwarzania. (#1912)
* Drzewo na liście elementów (dostępne dla dokumentów w trybie przeglądania) ma teraz prawidłowy rozmiar, aby pokazać tekst każdego elementu. (#2276)
* W aplikacjach korzystających z mostka Java Access Bridge edytowalne pola tekstowe są teraz poprawnie prezentowane w alfabecie Braille'a. (#2284)
* W aplikacjach korzystających z programu Java Access Bridge edytowalne pola tekstowe nie zawierają już w pewnych okolicznościach dziwnych znaków. (#1892)
* W aplikacjach korzystających z mostka Java Access Bridge, gdy znajduje się na końcu edytowalnego pola tekstowego, bieżący wiersz jest teraz poprawnie raportowany. (#1892)
* W trybie przeglądania w aplikacjach korzystających z Mozilla Gecko 14 i nowszych (np. Firefox 14) szybka nawigacja działa teraz dla cytatów blokowych i osadzonych obiektów. (#2287)
* W Internet Explorerze 9 NVDA nie odczytuje już niechcianej zawartości, gdy fokus przesuwa się wewnątrz pewnych punktów orientacyjnych lub elementów nadających się do skupienia (w szczególności elementu div, który jest zogniskowany lub pełni rolę punktu orientacyjnego ARIA).
* Ikona NVDA dla skrótów NVDA Desktop i Start Menu jest teraz wyświetlana poprawnie w 64-bitowych wersjach systemu Windows. (#354)

### Zmiany dla deweloperów

* Ze względu na zastąpienie poprzedniego instalatora NSIS dla NVDA wbudowanym instalatorem w Pythonie, nie jest już konieczne, aby tłumacze utrzymywali plik langstrings.txt dla instalatora. Wszystkie ciągi lokalizacyjne są teraz zarządzane przez pliki gettext po.

## 2012.1

Najważniejsze cechy tego wydania obejmują funkcje umożliwiające płynniejsze czytanie alfabetu Braille'a; wskazanie formatowania dokumentu w alfabecie Braille'a; dostęp do znacznie większej ilości informacji o formatowaniu i poprawiona wydajność w programie Microsoft Word; i obsługa sklepu iTunes Store.

### Nowe funkcje

* NVDA może ogłaszać liczbę początkowych tabulatorów i spacji w bieżącym wierszu w kolejności, w jakiej zostały wprowadzone. Można to włączyć, wybierając wcięcie wiersza raportu w oknie dialogowym formatowania dokumentu. (#373)
* NVDA może teraz wykrywać naciśnięcia generowane przez alternatywną emulację danych wejściowych klawiatury, taką jak klawiatury ekranowe i oprogramowanie do rozpoznawania mowy.
* NVDA może teraz wykrywać kolory w konsolach poleceń Windows.
* Pogrubienie, kursywa i podkreślenie są teraz oznaczone w alfabecie Braille'a za pomocą znaków odpowiednich dla skonfigurowanej tabeli tłumaczeń. (#538)
* Znacznie więcej informacji jest teraz podawanych w dokumentach programu Microsoft Word, w tym:
 * Informacje w tekście, takie jak numery przypisów dolnych i końcowych, poziomy nagłówków, istnienie komentarzy, poziomy zagnieżdżenia tabeli, łącza i kolor tekstu;
 * Raportowanie podczas wprowadzania sekcji dokumentu, takich jak komentarze, artykuły, przypisy dolne i końcowe oraz historie nagłówka i stopki.
* Alfabet Braille'a oznacza teraz zaznaczony tekst za pomocą punktów 7 i 8. (#889)
* Alfabet Braille'a informuje teraz o kontrolkach w dokumentach, takich jak łącza, przyciski i nagłówki. (#202)
* Obsługa monitorów brajlowskich hedo ProfiLine i MobilLine USB. (#1863, #1897)
* NVDA unika teraz domyślnego dzielenia słów w brajlu, jeśli jest to możliwe. Można to wyłączyć w oknie dialogowym Ustawienia brajla. (#1890, #1946)
* Możliwe jest teraz wyświetlanie alfabetu Braille'a w akapitach zamiast w wierszach, co może pozwolić na płynniejsze czytanie dużych ilości tekstu. Można to skonfigurować za pomocą opcji Czytane według akapitów w oknie dialogowym Ustawienia brajla. (#1891)
* W trybie przeglądania można aktywować obiekt znajdujący się pod kursorem za pomocą monitora brajlowskiego. Odbywa się to poprzez naciśnięcie przywoływania kursora w miejscu, w którym znajduje się kursor (co oznacza dwukrotne naciśnięcie go, jeśli kursor jeszcze się tam nie znajduje). (#1893)
* Podstawowa obsługa obszarów internetowych w programie iTunes, takich jak Sklep. Obsługiwane mogą być również inne aplikacje korzystające z WebKit 1. (#734)
* W książkach w programie Adobe Digital Editions 1.8.1 i nowszych stronach strony są teraz przewracane automatycznie po użyciu opcji powiedz wszystko. (#1978)
* Nowe tabele tłumaczeń brajlowskich: portugalski (ocena 2), islandzki (8 punktów) komputerowy (Braille), tamilski (1), hiszpański (8 punktów) i perski (1). (#2014)
* Teraz można skonfigurować, czy ramki w dokumentach mają być raportowane z okna dialogowego Preferencje formatowania dokumentu. (#1900)
* Tryb uśpienia jest automatycznie włączany podczas korzystania z OpenBook. (#1209)
* W Poedit tłumacze mogą teraz odczytywać dodane i automatycznie wyodrębnione komentarze tłumacza. Wiadomości, które są nieprzetłumaczone lub rozmyte, są oznaczone gwiazdką, a po przejściu do nich słychać sygnał dźwiękowy. (#1811)
* Obsługa wyświetlaczy HumanWare Brailliant BI i serii B. (#1990)
* Nowe języki: norweski bokmål, chiński tradycyjny (Hongkong).

### Zmiany

* Polecenia opisujące bieżący znak lub przeliterowujące bieżące słowo lub wiersz będą teraz pisane w odpowiednim języku zgodnie z tekstem, jeśli automatyczne przełączanie języka jest włączone i dostępne są odpowiednie informacje o języku.
* Zaktualizowano syntezator mowy eSpeak do wersji 1.46.02.
* NVDA będzie teraz obcinać bardzo długie (30 znaków lub więcej) nazwy odgadnięte z graficznych i linkowych adresów URL, ponieważ najprawdopodobniej są to śmieci, które przeszkadzają w czytaniu. (#1989)
* Niektóre informacje wyświetlane w alfabecie Braille'a zostały skrócone. (#1955, #2043)
* Gdy kursor kursora lub recenzji się porusza, pismo Braille'a jest przewijane w taki sam sposób, jak podczas przewijania ręcznego. To sprawia, że jest to bardziej odpowiednie, gdy brajl jest skonfigurowany do czytania akapitów i/lub unikania dzielenia słów. (#1996)
* Zaktualizowano do nowej tabeli tłumaczeń brajlowskich klasy 1 z języka hiszpańskiego.
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.4.1.

### Poprawki błędów

* W systemie Windows 8 fokus nie jest już nieprawidłowo przenoszony z pola wyszukiwania Eksploratora Windows, które nie pozwalało NVDA na interakcję z nim.
* Znaczna poprawa wydajności podczas czytania i nawigacji w dokumentach Microsoft Word, gdy włączone jest automatyczne raportowanie formatowania, dzięki czemu sprawdzanie formatowania odczytu itp. jest teraz całkiem wygodne. Wydajność może być również ogólnie poprawiona dla niektórych użytkowników.
* Tryb przeglądania jest teraz używany dla pełnoekranowej zawartości Adobe Flash.
* Naprawiono niską jakość dźwięku w niektórych przypadkach podczas korzystania z głosów interfejsu API Microsoft Speech w wersji 5 z urządzeniem wyjściowym audio ustawionym na wartość inną niż domyślna (Microsoft Sound Mapper). (#749)
* Ponownie zezwól na używanie NVDA z syntezatorem "no speech", polegając wyłącznie na alfabecie Braille'a lub przeglądarce mowy. (#1963)
* Polecenia nawigacji po obiektach nie informują już o komunikatach "Brak elementów podrzędnych" i "Brak elementów nadrzędnych", ale zamiast tego zgłaszają komunikaty zgodne z dokumentacją.
* Gdy NVDA jest skonfigurowany do używania języka innego niż angielski, nazwa Tab jest teraz podawana w odpowiednim języku.
* W Mozilla Gecko (np. Firefox) NVDA nie przełącza się już sporadycznie w tryb przeglądania podczas poruszania się po menu w dokumentach. (#2025)
* W Kalkulatorze Backspace informuje teraz o zaktualizowanym wyniku, a nie o niczym. (#2030)
* W trybie przeglądania polecenie przeniesienia myszy do bieżącego obiektu nawigatora jest teraz kierowane do środka obiektu przy kursorze przeglądania, a nie w lewym górnym rogu, co w niektórych przypadkach zwiększa jego dokładność. (#2029)
* W trybie przeglądania z włączonym trybem automatycznego ustawiania ostrości dla zmian ostrości ustawianie ostrości na pasku narzędzi przełączy się teraz w tryb ostrości. (#1339)
* Polecenie tytułu raportu znów działa poprawnie w programie Adobe Reader.
* Po włączeniu trybu automatycznego ustawiania ostrości dla zmian ostrości, tryb ostrości jest teraz poprawnie używany dla komórek tabeli fokusu; np. w siatkach ARIA. (#1763)
* W programie iTunes informacje o pozycji na niektórych listach są teraz poprawnie raportowane.
* W programie Adobe Reader niektóre łącza nie są już traktowane jako zawierające edytowalne pola tekstowe tylko do odczytu.
* Etykiety niektórych edytowalnych pól tekstowych nie są już nieprawidłowo uwzględniane podczas raportowania tekstu okna dialogowego. (#1960)
* Opis grupowania jest ponownie raportowany, jeśli włączone jest raportowanie opisów obiektów.
* Rozmiary czytelne dla człowieka są teraz uwzględniane w tekście okna dialogowego właściwości dysku Eksploratora Windows.
* W niektórych przypadkach podwójne raportowanie tekstu strony właściwości zostało pominięte. (#218)
* Ulepszono śledzenie daszka w edytowalnych polach tekstowych, które opierają się na tekście zapisanym na ekranie. W szczególności usprawnia to edycję w edytorze komórek programu Microsoft Excel i edytorze wiadomości Eudora. (#1658)
* W Firefoksie 11 przejście do polecenia zawierającego wirtualny bufor (NVDA+control+spacja) działa teraz tak, jak powinno, aby uciec od osadzonych obiektów, takich jak zawartość Flash.
* NVDA teraz poprawnie restartuje się (np. po zmianie skonfigurowanego języka), gdy znajduje się w katalogu, który zawiera znaki spoza ASCII. (#2079)
* Alfabet Braille'a poprawnie uwzględnia ustawienia raportowania skrótów do obiektów, informacji o pozycji i opisów.
* W aplikacjach Mozilli przełączanie między trybami przeglądania i ostrości nie jest już powolne przy włączonym alfabecie Braille'a. (#2095)
* Przekierowywanie kursora do spacji na końcu wiersza/akapitu za pomocą routingu kursora Braille'a w niektórych edytowalnych polach tekstowych działa teraz poprawnie, zamiast kierowania do początku tekstu. (#2096)
* NVDA ponownie działa poprawnie z syntezatorem Audiologic Tts3. (#2109)
* Dokumenty programu Microsoft Word są poprawnie traktowane jako wielowierszowe. Powoduje to, że pismo Braille'a zachowuje się bardziej odpowiednio, gdy dokument jest skoncentrowany.
* W przeglądarce Microsoft Internet Explorer nie występują już błędy podczas skupiania się na niektórych rzadkich kontrolkach. (#2121)
* Zmiana wymowy znaków interpunkcyjnych/symboli przez użytkownika będzie teraz obowiązywać od razu, zamiast wymagać ponownego uruchomienia NVDA lub wyłączenia automatycznego przełączania języka.
* Podczas korzystania z eSpeak, w niektórych przypadkach mowa nie milknie w oknie dialogowym Zapisz jako w przeglądarce dzienników NVDA. (#2145)

### Zmiany dla deweloperów

* Dostępna jest teraz zdalna konsola języka Python dla sytuacji, w których przydatne jest zdalne debugowanie. Szczegółowe informacje można znaleźć w Podręczniku programisty.
* Podstawowa ścieżka kodu NVDA jest teraz usuwana ze śladów zwrotnych w dzienniku, aby poprawić czytelność. (#1880)
* Obiekty TextInfo mają teraz metodę activate() do aktywowania pozycji reprezentowanej przez obiekt TextInfo.
 * Jest to używane przez brajl do aktywacji pozycji za pomocą przywoływania kursora na monitorze brajlowskim. Jednak w przyszłości mogą pojawić się inni rozmówcy.
* TreeInterceptory i NVDAObjects, które udostępniają tylko jedną stronę tekstu na raz, mogą obsługiwać automatyczne przewracanie stron podczas, powiedzmy wszystko, przy użyciu mieszanki textInfos.DocumentWithPageTurns. (#1978)
* Nazwy kilku stałych kontrolnych i wyjściowych zostały zmienione lub przeniesione. (#228)
 * przemówienie. REASON_* stałe zostały przeniesione do controlTypes.
 * W controlTypes, speechRoleLabels i speechStateLabels zostały zmienione nazwy odpowiednio na roleLabels i stateLabels.
* Wyjście brajlowskie jest teraz rejestrowane na poziomie wejścia/wyjścia. Najpierw rejestrowany jest nieprzetłumaczony tekst ze wszystkich regionów, a następnie wyświetlane są komórki brajlowskie okna. (#2102)
* podklasy synthDriver sapi5 mogą teraz zastępować _getVoiceTokens i rozszerzać init w celu obsługi niestandardowych tokenów głosowych, takich jak sapi.spObjectTokenCategory w celu pobrania tokenów z niestandardowej lokalizacji rejestru.

## 2011.3

Najważniejsze cechy tej wersji obejmują automatyczne przełączanie języka mowy podczas czytania dokumentów z odpowiednimi informacjami o języku; obsługa 64-bitowych środowisk Java Runtime Environments; raportowanie formatowania tekstu w trybie przeglądania w aplikacjach Mozilli; lepsza obsługa awarii i zawieszania się aplikacji; i początkowe poprawki dla systemu Windows 8.

### Nowe funkcje

* NVDA może teraz zmieniać język syntezatora eSpeak w locie podczas czytania niektórych dokumentów internetowych/pdf z odpowiednimi informacjami o języku. Automatyczne przełączanie języka/dialektu można włączać i wyłączać w oknie dialogowym Ustawienia głosu. (#845)
* Obsługiwany jest teraz program Java Access Bridge 2.0.2, który obejmuje obsługę 64-bitowych środowisk wykonawczych Java.
* W Mozilla Gecko (np. Firefox) poziomy nagłówków są teraz ogłaszane podczas korzystania z nawigacji po obiektach.
* Formatowanie tekstu może być teraz zgłaszane podczas korzystania z trybu przeglądania w Mozilla Gecko (np. Firefox i Thunderbird). (#394)
* Tekst z podkreśleniem i/lub przekreśleniem może być teraz wykrywany i raportowany w standardowych kontrolkach tekstowych IAccessible2, takich jak w aplikacjach Mozilli.
* W trybie przeglądania w programie Adobe Reader liczba wierszy i kolumn tabeli jest teraz raportowana.
* Dodano obsługę syntezatora Microsoft Speech Platform. (#1735)
* Numery stron i wierszy są teraz raportowane dla karetki w programie IBM Lotus Symphony. (#1632)
* Procentowy udział w tym, jak bardzo zmienia się wysokość dźwięku podczas wypowiadania wielkiej litery, można teraz skonfigurować w oknie dialogowym ustawień głosu. Zastępuje to jednak starsze pole wyboru podbicia dla wielkich liter (dlatego, aby wyłączyć tę funkcję, ustaw wartość procentową na 0). (#255)
* Kolor tekstu i tła jest teraz uwzględniany w raportowaniu formatowania komórek w programie Microsoft Excel. (#1655)
* W aplikacjach korzystających z mostka Java Access Bridge polecenie activate current navigator object działa teraz na formantach tam, gdzie jest to potrzebne. (#1744)
* Nowy język: tamilski.
* Podstawowa obsługa Design Science MathPlayer.

### Zmiany

* NVDA uruchomi się teraz ponownie, jeśli ulegnie awarii.
* Niektóre informacje wyświetlane w alfabecie Braille'a zostały skrócone. (#1288)
* Skrypt aktywnego okna odczytu (NVDA+b) został ulepszony, aby odfiltrować nieprzydatne kontrolki, a także jest teraz znacznie łatwiejszy do wyciszenia. (#1499)
* Automatyczne mówienie wszystkiego po załadowaniu dokumentu w trybie przeglądania jest teraz opcjonalne za pomocą ustawienia w oknie dialogowym ustawień trybu przeglądania. (#414)
* Podczas próby odczytania paska stanu (Desktop NVDA+end), jeśli nie można zlokalizować rzeczywistego obiektu paska stanu, NVDA zamiast tego ucieknie się do użycia dolnej linii tekstu zapisanego na wyświetlaczu dla aktywnej aplikacji. (#649)
* Podczas czytania dokumentów w trybie przeglądania, NVDA będzie teraz zatrzymywać się na końcu nagłówków i innych elementów na poziomie bloku, zamiast wypowiadać tekst razem z następną partią tekstu jako jedno długie zdanie.
* W trybie przeglądania naciśnięcie Enter lub spacji na karcie aktywuje ją teraz zamiast przełączania w tryb ostrości. (#1760)
* Zaktualizowano syntezator mowy eSpeak do wersji 1.45.47.

### Poprawki błędów

* NVDA nie pokazuje już punktorów ani numeracji dla list w Internet Explorerze i innych kontrolkach MSHTML, gdy autor zaznaczył, że nie powinny być one wyświetlane (np. styl listy to "brak"). (#1671)
* Ponowne uruchomienie NVDA, gdy się zawiesiło (np. przez naciśnięcie control+alt+n) nie powoduje już wyjścia z poprzedniej kopii bez rozpoczęcia nowej.
* Naciśnięcie Backspace lub strzałek w konsoli poleceń systemu Windows nie powoduje już w niektórych przypadkach dziwnych wyników. (#1612)
* Wybrany element w polach kombi WPF (i prawdopodobnie niektórych innych polach kombi uwidocznionych przy użyciu automatyzacji interfejsu użytkownika), które nie zezwalają na edycję tekstu, jest teraz poprawnie zgłaszany.
* W trybie przeglądania w programie Adobe Reader zawsze można przejść do następnego wiersza z wiersza nagłówka i odwrotnie za pomocą poleceń przenieś do następnego wiersza i przejdź do poprzedniego wiersza. Ponadto wiersz nagłówka nie jest już raportowany jako wiersz 0. (#1731)
* W trybie przeglądania w programie Adobe Reader można teraz przechodzić do pustych komórek w tabeli (a tym samym przechodzić obok nich).
* Bezsensowne informacje o pozycji (np. 0 z 0 poziom 0) nie są już podawane w alfabecie Braille'a.
* Gdy pismo Braille'a jest podłączone do recenzji, może teraz wyświetlać treść w wersji płaskiej. (#1711)
* W niektórych przypadkach tekst kontrolki tekstowej nie jest już wyświetlany dwukrotnie na monitorze brajlowskim, np. podczas przewijania wstecz od początku dokumentów programu Wordpad.
* W trybie przeglądania w przeglądarce Internet Explorer naciśnięcie Enter na przycisku przesyłania pliku teraz poprawnie wyświetla okno dialogowe wyboru pliku do przesłania zamiast przełączania w tryb koncentracji uwagi. (#1720)
* Dynamiczne zmiany zawartości, na przykład w konsolach Dos, nie są już ogłaszane, jeśli tryb uśpienia dla danej aplikacji jest aktualnie włączony. (#1662)
* W trybie przeglądania ulepszono działanie kombinacji alt+strzałka w górę i alt+strzałka w dół do zwijania i rozwijania. (#1630)
* NVDA odzyskuje sprawność po wielu innych sytuacjach, takich jak aplikacje, które przestają odpowiadać, co wcześniej powodowało całkowite zamrożenie. (#1408)
* Dla dokumentów w trybie przeglądania Mozilla Gecko (Firefox itp.) NVDA nie będzie już odmawiać renderowania tekstu w bardzo specyficznej sytuacji, gdy element jest stylizowany na display:table. (#1373)
* NVDA nie będzie już informować o kontrolkach etykiet, gdy fokus przesunie się w ich wnętrzu. Zatrzymuje podwójne zapowiedzi etykiet dla niektórych pól formularza w przeglądarkach Firefox (Gecko) i Internet Explorer (MSHTML). (#1650)
* NVDA nie czyta już komórki w programie Microsoft Excel po wklejeniu do niej za pomocą control+v. (#1781)
* W programie Adobe Reader zbędne informacje o dokumencie nie są już ogłaszane po przejściu do formantu na innej stronie w trybie koncentracji uwagi. (#1659)
* W trybie przeglądania w aplikacjach Mozilla Gecko (np. Firefox) przyciski przełączania są teraz poprawnie wykrywane i raportowane. (#1757)
* NVDA może teraz poprawnie odczytywać pasek adresu Eksploratora Windows w Windows 8 Developer Preview.
* NVDA nie będzie już powodować awarii aplikacji, takich jak winver i wordpad w Windows 8 Developer Preview, z powodu złych tłumaczeń glifów.
* W trybie przeglądania w aplikacjach korzystających z Mozilla Gecko 10 i nowszych (np. Firefox 10) kursor jest częściej ustawiany poprawnie podczas ładowania strony z kotwicą docelową. (#360)
* W trybie przeglądania w aplikacjach Mozilla Gecko (np. Firefox) etykiety map graficznych są teraz renderowane.
* Przy włączonym śledzeniu myszy przesuwanie myszy nad niektórymi edytowalnymi polami tekstowymi (takimi jak w ustawieniach urządzenia wskazującego Synaptics i SpeechLab SpeakText) nie powoduje już awarii aplikacji. (#672)
* NVDA działa teraz poprawnie w kilku oknach dialogowych w aplikacjach dystrybuowanych z Windows XP, w tym w oknie dialogowym Informacje w Notatniku i oknie dialogowym O systemie Windows. (#1853, #1855)
* Naprawiono recenzowanie według programu Word w kontrolkach edycji systemu Windows. (#1877)
* Wychodzenie z edytowalnego pola tekstowego za pomocą leftArrow, upArrow lub pageUp w trybie koncentracji uwagi teraz poprawnie przełącza się w tryb przeglądania, gdy włączony jest automatyczny tryb ostrości dla ruchu kursora. (#1733)

### Zmiany dla deweloperów

* NVDA może teraz instruować syntezatory mowy, aby przełączały języki dla określonych sekcji mowy.
 * Aby to umożliwić, kierowcy muszą obsługiwać mowę. LangChangeCommand w sekwencjach przeszłych do SynthDriver.speak().
 * Obiekty SynthDriver powinny również dostarczać argument language do obiektów VoiceInfo (lub zastępować atrybut language w celu pobrania bieżącego języka). W przeciwnym razie używany będzie język interfejsu użytkownika NVDA.

## 2011.2

Najważniejsze cechy tego wydania to znaczne ulepszenia dotyczące interpunkcji i symboli, w tym konfigurowalne poziomy, niestandardowe etykiety i opisy postaci; brak pauz na końcu wierszy podczas mówienia wszystkiego; ulepszona obsługa ARIA w Internet Explorerze; lepsza obsługa dokumentów PDF XFA/LiveCycle w programie Adobe Reader; dostęp do tekstu zapisanego na ekranie w większej liczbie aplikacji; oraz dostęp do informacji o formatowaniu i kolorach tekstu zapisywanego na ekranie.

### Nowe funkcje

* Możliwe jest teraz wysłuchanie opisu dowolnej postaci, naciskając przycisk przeglądu bieżącego skryptu postaci dwa razy w krótkim odstępie czasu.  W przypadku znaków angielskich jest to standardowy angielski alfabet fonetyczny. W przypadku języków piktograficznych, takich jak chiński tradycyjny, podano co najmniej jedną przykładową frazę z użyciem podanego symbolu. Również trzykrotne naciśnięcie przycisku przejrzyj bieżące słowo lub przejrzyj bieżący wiersz spowoduje przeliterowanie słowa/wiersza przy użyciu pierwszego z tych opisów. (#55)
* Więcej tekstu można zobaczyć w płaskiej recenzji dla aplikacji takich jak Mozilla Thunderbird, które zapisują swój tekst bezpośrednio na wyświetlaczu jako glify.
* Teraz można wybierać spośród kilku poziomów interpunkcji i ogłaszania symboli. (#332)
* Gdy znaki interpunkcyjne lub inne symbole są powtarzane więcej niż cztery razy, liczba powtórzeń jest teraz ogłaszana zamiast wypowiadania powtarzających się symboli. (#43)
* Nowe tabele tłumaczeń brajlowskich: norweski 8-punktowy komputerowy alfabet Braille'a, etiopski stopień 1, słoweński 1, serbski 1. punkt. (#1456)
* Mowa nie zatrzymuje się już w nienaturalny sposób na końcu każdego wiersza podczas używania polecenia powiedz wszystko. (#149)
* NVDA będzie teraz informować, czy coś jest posortowane (zgodnie z właściwością aria-sort) w przeglądarkach internetowych. (#1500)
* Wzorce brajlowskie Unicode są teraz poprawnie wyświetlane na monitorach brajlowskich. (#1505)
* W Internet Explorerze i innych kontrolkach MSHTML, gdy fokus porusza się wewnątrz grupy kontrolek (otoczonych zestawem pól), NVDA będzie teraz ogłaszać nazwę grupy (legendę). (#535)
* W programie Internet Explorer i innych formantach MSHTML właściwości aria-labelledBy i aria-describedBy są teraz honorowane.
* w programie Internet Explorer i innych formantach MSHTML ulepszono obsługę kontrolek ARIA list, gridcell, slider i progressbar.
* Użytkownicy mogą teraz zmieniać wymowę znaków interpunkcyjnych i innych symboli, a także poziom symboli, na którym są one wypowiadane. (#271, #1516)
* W programie Microsoft Excel nazwa aktywnego arkusza jest teraz podawana podczas przełączania arkuszy za pomocą control+pageUp lub control+pageDown. (#760)
* Podczas poruszania się po tabeli w programie Microsoft Word za pomocą Tab, NVDA będzie teraz informować o bieżącej komórce podczas ruchu. (#159)
* Teraz można skonfigurować, czy współrzędne komórek tabeli mają być raportowane w oknie dialogowym Preferencje formatowania dokumentu. (#719)
* NVDA może teraz wykrywać formatowanie i kolor tekstu zapisanego na ekranie.
* Na liście wiadomości w programie Outlook Express/Windows Mail/Windows Live Mail NVDA będzie teraz informować o tym, że wiadomość jest nieprzeczytana, a także o tym, czy jest rozwinięta lub zwinięta w przypadku wątków konwersacji. (#868)
* eSpeak ma teraz ustawienie zwiększania szybkości, które potraja szybkość mówienia.
* Obsługa kontrolki kalendarza znajdującej się w oknie dialogowym Informacje o dacie i godzinie, do którego można uzyskać dostęp z zegara systemu Windows 7. (#1637)
* Dodano dodatkowe przypisania dla monitora brajlowskiego MDV Lilli. (#241)
* Nowe języki: bułgarski, albański.

### Zmiany

* Aby przesunąć kursor do kursora przeglądania, naciśnij teraz skrypt obiektu przenieś fokus do nawigatora (pulpit NVDA+shift+numpadMinus, laptop NVDA+shift+backspace) dwa razy w krótkim odstępie czasu. Spowoduje to zwolnienie większej liczby na klawiaturze. (#837)
* Aby usłyszeć dziesiętną i szesnastkową reprezentację znaku pod kursorem recenzji, teraz naciśnij przycisk przejrzenia bieżącego znaku trzy razy, a nie dwa razy, ponieważ teraz dwa razy wypowiada opis znaku.
* Zaktualizowano syntezator mowy eSpeak do wersji 1.45.03. (#1465)
* Tabele układu nie są już ogłaszane w aplikacjach Mozilla Gecko podczas przesuwania fokusu w trybie skupienia lub poza dokumentem.
* W przeglądarce Internet Explorer i innych kontrolkach MSHTML tryb przeglądania działa teraz dla dokumentów w aplikacjach ARIA. (#1452)
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 2.3.0.
* W trybie przeglądania i przeskakiwaniu do kontrolki z szybką nawigacją lub fokusem opis kontrolki jest teraz ogłaszany, jeśli ją posiada.
* Paski postępu są teraz ogłaszane w trybie brwi.
* Węzły oznaczone rolą prezentacji ARIA w programie Internet Explorer i innych kontrolkach MSHTML są teraz odfiltrowywane z prostego przeglądu i pochodzenia fokusu.
* Interfejs użytkownika i dokumentacja NVDA odnoszą się teraz do wirtualnych jako trybu przeglądania, ponieważ termin "wirtualny bufor" jest raczej bez znaczenia dla większości użytkowników. (#1509)
* Gdy użytkownik chce skopiować swoje ustawienia użytkownika do profilu systemowego w celu użycia na ekranie logowania itp., a jego ustawienia zawierają niestandardowe wtyczki, jest teraz ostrzegany, że może to stanowić zagrożenie bezpieczeństwa. (#1426)
* Usługa NVDA nie uruchamia już i nie zatrzymuje NVDA na pulpitach użytkownika.
* W systemach Windows XP i Windows Vista, NVDA nie korzysta już z automatyzacji interfejsu użytkownika, nawet jeśli jest ona dostępna za pośrednictwem aktualizacji platformy. Chociaż korzystanie z automatyzacji interfejsu użytkownika może poprawić dostępność niektórych nowoczesnych aplikacji, w systemach XP i Vista było zbyt wiele zawieszeń, awarii i ogólnie utraty wydajności podczas korzystania z niego. (#1437)
* W aplikacjach korzystających z Mozilla Gecko 2 i nowszych (takich jak Firefox 4 i nowsze) dokument może być teraz czytany w trybie przeglądania przed pełnym zakończeniem ładowania.
* NVDA ogłasza teraz stan kontenera, gdy fokus przesuwa się do kontrolki w nim (np. jeśli fokus przesuwa się wewnątrz dokumentu, który wciąż się ładuje, zgłosi go jako zajęty).
* Interfejs użytkownika i dokumentacja NVDA nie używają już terminów "pierwsze dziecko" i "rodzic" w odniesieniu do nawigacji po obiektach, ponieważ terminy te są mylące dla wielu użytkowników.
* Zwinięte nie jest już zgłaszane w przypadku niektórych elementów menu, które mają podmenu.
* Skrypt reportCurrentFormatting (NVDA+f) teraz raportuje formatowanie w pozycji kursora przeglądu, a nie w systemowym kursorze/fokusu. Ponieważ domyślnie kursor recenzji podąża za daszkiem, większość osób nie powinna zauważyć różnicy. Jednak teraz umożliwia to użytkownikowi znalezienie formatowania podczas przesuwania kursora recenzji, na przykład w recenzji płaskiej.

### Poprawki błędów

* Zwijanie pól kombi w dokumentach w trybie przeglądania, gdy tryb skupienia został wymuszony za pomocą NVDA+spacja, nie przełącza się już automatycznie z powrotem do trybu przeglądania. (#1386)
* W dokumentach Gecko (np. Firefox) i MSHTML (np. Internet Explorer), NVDA teraz poprawnie renderuje pewien tekst w tym samym wierszu, który wcześniej był renderowany w oddzielnych wierszach. (#1378)
* Gdy pismo Braille'a jest podłączone do recenzji, a obiekt nawigatora zostanie przeniesiony do dokumentu w trybie przeglądania, ręcznie lub z powodu zmiany fokusu, pismo Braille'a odpowiednio wyświetli zawartość trybu przeglądania. (#1406, #1407)
* Gdy mówienie o interpunkcji jest wyłączone, niektóre znaki interpunkcyjne nie są już niepoprawnie wypowiadane podczas korzystania z niektórych syntezatorów. (#332)
* Problemy nie występują już podczas ładowania konfiguracji dla syntezatorów, które nie obsługują ustawień głosowych, takich jak Audiologic Tts3. (#1347)
* Menu Dodatki Skype'a jest teraz odczytywane poprawnie. (#648)
* Zaznaczenie pola wyboru Głośność elementów sterujących jasnością w oknie dialogowym Ustawienia myszy nie powinno już powodować dużego opóźnienia w przypadku sygnałów dźwiękowych podczas poruszania myszą po ekranie w systemie Windows Vista/Windows 7 z włączonym interfejsem Aero. (#1183)
* Gdy NVDA jest skonfigurowane do korzystania z układu klawiatury laptopa, NVDA+delete działa teraz zgodnie z dokumentacją, aby raportować wymiary bieżącego obiektu nawigatora. (#1498)
* NVDA teraz prawidłowo honoruje atrybut wybrany przez arię w dokumentach Internet Explorera.
* Gdy NVDA automatycznie przełącza się w tryb skupienia w dokumentach w trybie przeglądania, teraz ogłasza informacje o kontekście fokusu. Na przykład, jeśli element pola listy zostanie aktywny, pole listy zostanie ogłoszone jako pierwsze. (#1491)
* W programie Internet Explorer i innych formantach MSHTML formanty pola listy ARIA są teraz drzewione jako listy, a nie jako elementy listy.
* Gdy kontrolka edytowalnego tekstu tylko do odczytu jest aktywna, NVDA zgłasza teraz, że jest ona tylko do odczytu. (#1436)
* W trybie przeglądania, NVDA zachowuje się teraz poprawnie w odniesieniu do edytowalnych pól tekstowych tylko do odczytu.
* W dokumentach w trybie przeglądania, NVDA nie przełącza już niepoprawnie trybu skupienia, gdy ustawiona jest aria-activedescendant; Na przykład, gdy lista uzupełniania pojawiła się w niektórych kontrolkach autouzupełniania.
* W programie Adobe Reader nazwa elementów sterujących jest teraz podawana podczas przesuwania fokusu lub korzystania z szybkiej nawigacji w trybie przeglądania.
* W dokumentach XFA PDF w programie Adobe Reader przyciski, łącza i grafika są teraz renderowane poprawnie.
* W dokumentach XFA PDF w programie Adobe Reader wszystkie elementy są teraz renderowane w osobnych wierszach. Zmiana ta została wprowadzona, ponieważ duże sekcje (czasami nawet cały dokument) były renderowane bez przerw ze względu na ogólny brak struktury w tych dokumentach.
* Rozwiązano problemy z przenoszeniem fokusu do lub z edytowalnych pól tekstowych w dokumentach XFA PDF w programie Adobe Reader.
* W dokumentach XFA PDF w programie Adobe Reader będą teraz raportowane zmiany wartości aktywnego pola kombi.
* Pola kombi narysowane przez właściciela, takie jak te do wybierania kolorów w programie Outlook Express, są teraz dostępne za pomocą NVDA. (#1340)
* W językach, w których spacja jest separatorem grup cyfr/tysięcy, takich jak francuski i niemiecki, liczby z oddzielnych fragmentów tekstu nie są już wymawiane jako pojedyncza liczba. Było to szczególnie problematyczne w przypadku komórek tabeli zawierających liczby. (#555)
* węzły z rolą opisu ARIA w programie Internet Explorer i innych formantach MSHTML są teraz klasyfikowane jako tekst statyczny, a nie pola edycji.
* Rozwiązano różne problemy występujące podczas naciskania Tab, gdy fokus znajduje się na dokumencie w trybie przeglądania (np. nieprawidłowe przenoszenie Tab do paska adresu w przeglądarce Internet Explorer). (#720, #1367)
* Podczas wchodzenia na listy podczas czytania tekstu, NVDA mówi teraz na przykład "lista z 5 pozycjami" zamiast "lista z 5 elementami". (#1515)
* W trybie pomocy wprowadzania gesty są rejestrowane, nawet jeśli ich skrypty pomijają pomoc wejściową, taką jak polecenia przewijania ekranu brajlowskiego do przodu i do tyłu.
* W trybie pomocy przy wprowadzaniu, gdy modyfikator jest przytrzymany na klawiaturze, NVDA nie zgłasza już modyfikatora tak, jakby sam się modyfikował; np. NVDA+NVDA.
* W dokumentach programu Adobe Reader naciśnięcie c lub shift+c w celu przejścia do pola kombi działa teraz.
* Wybrany stan wierszy tabeli do wyboru jest teraz raportowany w taki sam sposób, jak w przypadku elementów widoku listy i drzewa.
* Elementy sterujące w Firefoksie i innych aplikacjach Gecko mogą być teraz aktywowane w trybie przeglądania, nawet jeśli ich zawartość została usunięta poza ekran. (#801)
* Nie można już wyświetlać okna dialogowego ustawień NVDA, gdy wyświetlane jest okno dialogowe komunikatu, ponieważ w tym przypadku okno dialogowe ustawień zostało zawieszone. (#1451)
* W programie Microsoft Excel nie ma już opóźnień podczas przytrzymywania lub szybkiego naciskania w celu przechodzenia między komórkami lub zaznaczania ich.
* Naprawiono sporadyczne awarie usługi NVDA, co oznaczało, że NVDA przestała działać na bezpiecznych ekranach Windows.
* Naprawiono problemy, które czasami występowały w przypadku monitorów brajlowskich, gdy zmiana powodowała znikanie wyświetlanego tekstu. (#1377)
* Okno pobierania w Internet Explorerze 9 można teraz nawigować i odczytywać za pomocą NVDA. (#1280)
* Nie jest już możliwe przypadkowe uruchomienie wielu kopii NVDA w tym samym czasie. (#507)
* Na wolnych systemach, NVDA nie powoduje już nieprawidłowo wyświetlania swojego głównego okna przez cały czas podczas działania. (#726)
* NVDA nie ulega już awarii w systemie Windows xP podczas uruchamiania aplikacji WPF. (#1437)
* Powiedz wszystko i powiedz wszystko z recenzją mogą teraz pracować w kontrolkach tekstowych automatyzacji interfejsu użytkownika, które obsługują wszystkie wymagane funkcje. Na przykład można teraz używać opcji "powiedz wszystko" z recenzją w dokumentach przeglądarki plików XPS.
* NVDA nie klasyfikuje już nieprawidłowo niektórych elementów listy w oknie dialogowym Zastosuj teraz reguł wiadomości programu Outlook Express / Windows Live Mail jako pól wyboru. (#576)
* Pola kombi nie są już zgłaszane jako posiadające podmenu.
* NVDA jest teraz w stanie odczytywać odbiorców w polach To, CC i BCC w programie Microsoft Outlook. (#421)
* Naprawiono problem w oknie dialogowym ustawień głosu NVDA, w którym wartość suwaków czasami nie była zgłaszana po zmianie. (#1411)
* NVDA nie zawodzi już w ogłaszaniu nowej komórki podczas przenoszenia w arkuszu kalkulacyjnym Excel po wycięciu i wklejeniu. (#1567)
* NVDA nie staje się już gorsza w odgadywaniu nazw kolorów, im więcej kolorów ogłasza.
* W Internet Explorerze i innych kontrolkach MSHTML naprawiono niemożność odczytania części rzadkich stron, które zawierają ramki iframe oznaczone rolą prezentacji ARIA. (#1569)
* W programie Internet Explorer i innych kontrolkach MSHTML rozwiązano rzadki problem polegający na tym, że fokus przeskakiwał w nieskończoność między dokumentem a wielowierszowym edytowalnym polem tekstowym w trybie koncentracji uwagi. (#1566)
* W programie Microsoft Word 2010 NVDA będzie teraz automatycznie odczytywać okna dialogowe potwierdzenia. (#1538)
* W wielowierszowych edytowalnych polach tekstowych w programie Internet Explorer i innych formantach MSHTML zaznaczenie wierszy po pierwszym jest teraz poprawnie raportowane. (#1590)
* Ulepszone przechodzenie za pomocą słowa w wielu przypadkach, w tym tryb przeglądania i kontrolki edycji systemu Windows. (#1580)
* Instalator NVDA nie wyświetla już zniekształconego tekstu dla hongkońskich wersji Windows Vista i Windows 7. (#1596)
* NVDA nie może już załadować syntezatora Microsoft Speech API w wersji 5, jeśli konfiguracja zawiera ustawienia dla tego syntezatora, ale brakuje ustawienia głosowego. (#1599)
* W edytowalnych polach tekstowych w Internet Explorerze i innych kontrolkach MSHTML, NVDA nie opóźnia się ani nie zawiesza, gdy włączony jest alfabet Braille'a.
* W trybie przeglądania Firefoksa, NVDA nie odmawia już dołączania treści, która znajduje się w węźle z możliwością skupienia z rolą prezentacji ARIA.
* W programie Microsoft Word z włączonym alfabetem Braille'a wiersze na stronach po pierwszej stronie są teraz poprawnie raportowane. (#1603)
* W programie Microsoft Word 2003 wiersze tekstu pisanego od prawej do lewej można ponownie czytać z włączoną obsługą alfabetu Braille'a. (#627)
* W programie Microsoft Word powiedz, że wszystko działa teraz poprawnie, gdy dokument nie kończy się końcem zdania.
* Podczas otwierania zwykłej wiadomości tekstowej w programie Windows Live Mail 2011, NVDA poprawnie skupi się na dokumencie wiadomości, umożliwiając jego odczytanie.
* NVDA nie zawiesza się już tymczasowo ani nie odmawia mówienia w oknach dialogowych Przenieś do / Kopiuj do w Windows Live Mail. (#574)
* W Outlooku 2010 NVDA będzie teraz poprawnie śledzić fokus na liście wiadomości. (#1285)
* Rozwiązano niektóre problemy z połączeniem USB w monitorze brajlowskim MDV Lilli. (#241)
* W programie Internet Explorer i innych formantach MSHTML spacje nie są już ignorowane w trybie przeglądania w niektórych przypadkach (np. po linku).
* W programie Internet Explorer i innych formantach MSHTML niektóre zbędne znaki końca wiersza zostały wyeliminowane w trybie przeglądania. W szczególności elementy HTML ze stylem wyświetlania Brak nie wymuszają już podziału wiersza. (#1685)
* Jeśli NVDA nie może się uruchomić, niepowodzenie w odtworzeniu dźwięku zatrzymania krytycznego systemu Windows nie powoduje już zagłuszania komunikatu o błędzie krytycznym w pliku dziennika.

### Zmiany dla deweloperów

* Dokumentacja programisty może być teraz generowana za pomocą SCons. Aby uzyskać szczegółowe informacje, zobacz readme.txt w katalogu głównym dystrybucji źródłowej, w tym skojarzone zależności.
* Lokalizacje mogą teraz zawierać opisy postaci. Więcej informacji można znaleźć w sekcji "Opisy postaci" w podręczniku dla twórców. (#55)
* Ustawienia regionalne mogą teraz dostarczać informacji o wymowie określonych znaków interpunkcyjnych i innych symboli. Szczegółowe informacje można znaleźć w sekcji Wymowa symboli w Podręczniku programisty. (#332)
* Teraz możesz zbudować NVDAHelper z kilkoma opcjami debugowania przy użyciu zmiennej nvdaHelperDebugFlags SCons. Aby uzyskać szczegółowe informacje, zobacz readme.txt w katalogu głównym dystrybucji źródłowej. (#1390)
* Sterowniki syntezatora otrzymują teraz sekwencję poleceń tekstowych i głosowych do mówienia, a nie tylko tekst i indeks.
 * Pozwala to na osadzanie indeksów, zmiany parametrów itp.
 * Sterowniki powinny implementować SynthDriver.speak() zamiast SynthDriver.speakText() i SynthDriver.speakCharacter().
 * Stare metody będą używane, jeśli SynthDriver.speak() nie jest zaimplementowany, ale są przestarzałe i zostaną usunięte w przyszłej wersji.
* gui.execute() została usunięta. wx. Zamiast tego należy użyć metody CallAfter().
* gui.scriptUI został usunięty.
 * W przypadku okien dialogowych komunikatów użyj polecenia wx. CallAfter(gui.messageBox, ...).
 * W przypadku wszystkich innych okien dialogowych należy zamiast tego używać rzeczywistych okien dialogowych wx.
 * Nowa funkcja gui.runScriptModalDialog() upraszcza korzystanie z modalnych okien dialogowych ze skryptów.
* Sterowniki syntezatora mogą teraz obsługiwać ustawienia logiczne. Zobacz SynthDriverHandler.BooleanSynthSetting.
* SCons akceptuje teraz zmienną certTimestampServer określającą adres URL serwera znaczników czasowych, który ma być używany do oznaczania podpisów authenticode znacznikiem czasu. (#1644)

## 2011.1.1

To wydanie naprawia kilka problemów związanych z bezpieczeństwem i innych ważnych problemów znalezionych w NVDA 2011.1.

### Poprawki błędów

* Opcja Przekaż darowiznę w menu NVDA jest teraz wyłączona, gdy jest uruchamiana na ekranach logowania, blokady, UAC i innych bezpiecznych ekranów systemu Windows, ponieważ stanowi to zagrożenie bezpieczeństwa. (#1419)
* Teraz nie można kopiować ani wklejać w interfejsie użytkownika NVDA na bezpiecznych komputerach stacjonarnych (ekran blokady, ekran UAC i logowanie do systemu Windows), ponieważ stanowi to zagrożenie bezpieczeństwa. (#1421)
* W Firefoksie 4 polecenie przejścia do zawierającego wirtualny bufor (NVDA+control+spacja) działa teraz tak, jak powinno, aby uniknąć osadzonych obiektów, takich jak zawartość Flash. (#1429)
* Gdy mówienie o poleceń jest włączone, przesunięte znaki nie są już niepoprawnie wypowiadane jako poleceń. (#1422)
* Gdy mówienie o poleceń jest włączone, naciśnięcie spacji z modyfikatorami innymi niż shift (takimi jak control i alt) jest teraz zgłaszane jako polecenia. (#1424)
* Rejestrowanie jest teraz całkowicie wyłączone podczas uruchamiania na ekranach logowania, blokady, UAC i innych bezpiecznych ekranów systemu Windows, ponieważ stanowi to zagrożenie bezpieczeństwa. (#1435)
* W trybie pomocy wprowadzania gesty są teraz rejestrowane, nawet jeśli nie są powiązane ze skryptem (zgodnie z podręcznikiem użytkownika). (#1425)

## 2011.1

Najważniejsze cechy tego wydania obejmują automatyczne raportowanie nowych danych wyjściowych tekstu w mIRC, PuTTY, Tera Term i SecureCRT; obsługa wtyczek globalnych; ogłoszenie punktorów i numeracji w programie Microsoft Word; dodatkowe przypisania dla monitorów brajlowskich, w tym do przechodzenia do następnej i poprzedniej linii; obsługa kilku monitorów brajlowskich Baum, HumanWare i APH; oraz raportowanie kolorów dla niektórych formantów, w tym formantów tekstowych IBM Lotus Symphony.

### Nowe funkcje

* Kolory mogą być teraz zgłaszane dla niektórych elementów sterujących. Automatyczne ogłaszanie można skonfigurować w oknie dialogowym Preferencje formatowania dokumentu. Można go również zgłaszać na żądanie za pomocą polecenia formatowania tekstu raportu (NVDA+f).
 * Początkowo jest to obsługiwane w standardowych edytowalnych kontrolkach tekstowych IAccessible2 (takich jak w aplikacjach Mozilla), kontrolkach RichEdit (takich jak w Wordpadzie) i kontrolkach tekstowych IBM Lotus Symphony.
* W wirtualnych można teraz wybierać według strony (za pomocą shift+pageDown i shift+pageUp) i akapitu (za pomocą shift+control+strzałki w dół i shift+control+strzałki w górę). (#639)
* NVDA teraz automatycznie raportuje nowy tekst wyjściowy w mIRC, PuTTY, Tera Term i SecureCRT. (#936)
* Użytkownicy mogą teraz dodawać nowe przypisania lub nadpisywać istniejące dla dowolnego skryptu w NVDA, dostarczając mapę gestów wejściowych pojedynczego użytkownika. (#194)
* Wsparcie dla wtyczek globalnych. Globalne wtyczki mogą dodawać nowe funkcje do NVDA, które działają we wszystkich aplikacjach. (#281)
* Cichy sygnał dźwiękowy jest teraz słyszalny podczas wpisywania znaków za pomocą Shift, gdy włączony jest CapsLock. Można to wyłączyć, usuwając zaznaczenie odpowiedniej nowej opcji w oknie dialogowym Ustawienia klawiatury. (#663)
* Sztywne podziały stron są teraz ogłaszane podczas przechodzenia po wierszach w programie Microsoft Word. (#758)
* Punktory i numeracja są teraz odczytywane w programie Microsoft Word podczas przechodzenia wierszem. (#208)
* Polecenie przełączania trybu uśpienia dla bieżącej aplikacji (NVDA+shift+s) jest już dostępne. Tryb uśpienia (wcześniej znany jako tryb self-voiki) wyłącza wszystkie funkcje czytania ekranu w NVDA dla określonej aplikacji. Bardzo przydatne w przypadku aplikacji, które udostępniają własne funkcje mowy i/lub czytania ekranu. Naciśnij to polecenie ponownie, aby wyłączyć tryb uśpienia.
* Dodano kilka dodatkowych przypisań monitora brajlowskiego. Szczegółowe informacje można znaleźć w rozdziale Obsługiwane monitory brajlowskie w Podręczniku użytkownika. (#209)
* Dla wygody zewnętrznych programistów, moduły aplikacji, a także globalne wtyczki mogą być teraz ponownie ładowane bez ponownego uruchamiania NVDA. Użyj narzędzi -> Załaduj ponownie wtyczki w menu NVDA lub NVDA+control+f3. (#544)
* NVDA zapamiętuje teraz pozycję, w której się znajdowałeś podczas powrotu do poprzednio odwiedzanej strony internetowej. Ma to zastosowanie do momentu zamknięcia przeglądarki lub NVDA. (#132)
* Monitory brajlowskie Handy Tech mogą być teraz używane bez instalowania uniwersalnego sterownika Handy Tech. (#854)
* Obsługa kilku monitorów brajlowskich Baum, HumanWare i APH. (#937)
* Pasek stanu w programie Media Player Classic Home Cinema jest teraz rozpoznawany.
* Monitor brajlowski Freedom Scientific Focus 40 Blue może być teraz używany po podłączeniu przez Bluetooth. (#1345)

### Zmiany

* Informacje o pozycji nie są już domyślnie raportowane w niektórych przypadkach, gdy zwykle były nieprawidłowe; np. większość menu, pasek uruchomionych aplikacji, obszar powiadomień itp. Można ją jednak ponownie włączyć za pomocą dodanej opcji w oknie dialogowym Ustawienia prezentacji obiektu.
* Nazwa pomocy klawiatury została zmieniona na pomoc wejściowa, aby odzwierciedlić, że obsługuje ona dane wejściowe ze źródeł innych niż klawiatura.
* Pomoc przy wprowadzaniu nie informuje już o lokalizacji kodu skryptu za pomocą mowy i alfabetu Braille'a, ponieważ jest ona tajemnicza i nieistotna dla użytkownika. Jednak teraz jest on rejestrowany dla programistów i zaawansowanych użytkowników.
* Gdy NVDA wykryje, że coś się zawiesiło, kontynuuje przechwytywanie kluczy modyfikujących NVDA, mimo że przekazuje wszystkie inne klucze do systemu. Zapobiega to przypadkowemu przełączeniu Caps Lock itp., jeśli użytkownik naciśnie modyfikujący NVDA, nie zdając sobie sprawy, że NVDA się zawiesił. (#939)
* Jeśli zostaną przytrzymane po użyciu polecenia "przekaż następny przez", wszystkie (w tym powtórzenia) są teraz przekazywane, dopóki ostatni nie zostanie zwolniony.
* Jeśli modyfikujący NVDA zostanie naciśnięty dwa razy w krótkim odstępie czasu, aby go przepuścić, a drugie naciśnięcie zostanie przytrzymane, wszystkie powtórzenia również zostaną przepuszczone.
* zwiększania, zmniejszania głośności i wyciszania są teraz zgłaszane w pomocy wejściowej. Może to być pomocne, jeśli użytkownik nie ma pewności, jakie są te klucze.
* Skrót klawiszowy dla elementu Review Cursor w menu Preferencji NVDA został zmieniony z r na c, aby wyeliminować konflikt z elementem Ustawienia Braille'a.

### Poprawki błędów

* Podczas dodawania nowego wpisu słownika mowy tytuł okna dialogowego brzmi teraz "Dodaj wpis słownika" zamiast "Edytuj wpis słownika". (#924)
* W oknach dialogowych słownika mowy zawartość kolumn Wyrażenie regularne i Wielkość liter na liście wpisów słownika jest teraz prezentowana w skonfigurowanym języku NVDA, a nie zawsze w języku angielskim.
* W AIM informacje o pozycji są teraz ogłaszane w widokach drzewa.
* Na suwakach w oknie dialogowym Ustawienia głosu, strzałka w górę/strona w górę/strona główna zwiększa teraz ustawienie, a strzałka w dół/strona w dół/koniec zmniejsza je. Wcześniej działo się odwrotnie, co nie jest logiczne i jest niespójne z pierścieniem ustawień syntezatora. (#221)
* W wirtualnych z wyłączonym układem ekranu nie pojawiają się już niektóre zbędne puste wiersze.
* Jeśli modyfikujący NVDA zostanie naciśnięty dwa razy szybko, ale nastąpi naciśnięcie w międzyczasie, modyfikatora NVDA nie będzie już przekazywany przy drugim naciśnięciu.
* interpunkcyjne są teraz odczytywane w pomocy wejściowej, nawet jeśli mówienie o interpunkcji jest wyłączone. (#977)
* W oknie dialogowym Ustawienia klawiatury, nazwy układów klawiatury są teraz prezentowane w skonfigurowanym języku NVDA, a nie zawsze w języku angielskim. (#558)
* Naprawiono problem polegający na tym, że niektóre elementy były renderowane jako puste w dokumentach programu Adobe Reader; np. linki w spisie treści Podręcznika użytkownika Apple iPhone IOS 4.1.
* Przycisk "Użyj aktualnie zapisanych ustawień na ekranie logowania i innych bezpiecznych ekranów" w oknie dialogowym ustawień ogólnych NVDA działa teraz, jeśli jest używany natychmiast po zainstalowaniu NVDA, ale przed pojawieniem się bezpiecznego ekranu. Wcześniej NVDA informowała, że kopiowanie powiodło się, ale w rzeczywistości nie przyniosło żadnego efektu. (#1194)
* Nie jest już możliwe, aby dwa okna dialogowe ustawień NVDA były otwarte jednocześnie. Rozwiązuje to problemy polegające na tym, że jedno otwarte okno dialogowe zależy od innego otwartego okna dialogowego; np. zmiana syntezatora, gdy otwarte jest okno dialogowe Ustawienia głosu. (#603)
* W systemach z włączonym UAC, przycisk "Użyj aktualnie zapisanych ustawień na logowaniu i innych bezpiecznych ekranach" w oknie dialogowym ustawień ogólnych NVDA nie kończy się już niepowodzeniem po wyświetleniu monitu UAC, jeśli nazwa konta użytkownika zawiera spację. (#918)
* W Internet Explorerze i innych kontrolkach MSHTML, NVDA używa teraz adresu URL jako ostatniej deski ratunku do określenia nazwy linku, zamiast prezentowania pustych linków. (#633)
* NVDA nie ignoruje już fokusu w menu AOL Instant Messenger 7. (#655)
* Poinformuj o poprawnej etykiecie błędów w oknie dialogowym Sprawdzanie pisowni programu Microsoft Word (np. Brak w słowniku, Błąd gramatyczny, interpunkcja). Wcześniej wszystkie były ogłaszane jako błąd gramatyczny. (#883)
* Pisanie w programie Microsoft Word podczas korzystania z monitora brajlowskiego nie powinno już powodować wpisywania zniekształconego tekstu, a rzadki błąd zawieszania się gry po naciśnięciu przywoływania brajlowskiego w dokumentach programu Word został naprawiony. (#1212) Ograniczeniem jest jednak to, że tekstu arabskiego nie można już czytać w programie Word 2003 i starszych wersjach podczas korzystania z monitora brajlowskiego. (#627)
* Po naciśnięciu usuwania w polu edycji, tekst/kursor na monitorze brajlowskim powinien być teraz zawsze odpowiednio aktualizowany, aby odzwierciedlić zmianę. (#947)
* Zmiany na dynamicznych stronach w dokumentach Gecko2 (np. Firefox 4), gdy otwartych jest wiele kart, są teraz poprawnie odzwierciedlane przez NVDA. Poprzednio odzwierciedlone były tylko zmiany w pierwszej zakładce. (Błąd Mozilli 610985)
* NVDA może teraz poprawnie ogłaszać sugestie błędów gramatycznych i interpunkcyjnych w oknie dialogowym sprawdzania pisowni w programie Microsoft Word. (#704)
* W Internet Explorerze i innych kontrolkach MSHTML, NVDA nie prezentuje już kotwic docelowych jako pustych linków w swoim wirtualnym buforze. Zamiast tego te kotwice są ukryte tak, jak powinny. (#1326)
* Nawigacja po obiektach wokół standardowych okien grupy i w ich obrębie nie jest już przerywana i asymetryczna.
* W Firefoksie i innych kontrolkach opartych na Gecko, NVDA nie będzie się już zacinać w ramce podrzędnej, jeśli zakończy ładowanie przed zewnętrznym dokumentem.
* NVDA teraz poprawnie ogłasza następny znak podczas usuwania znaku za pomocą numpadDelete. (#286)
* Na ekranie logowania systemu Windows XP nazwa użytkownika jest ponownie zgłaszana po zmianie wybranego użytkownika.
* Naprawiono problemy podczas odczytywania tekstu w konsolach poleceń systemu Windows z włączonym raportowaniem numerów wierszy.
* Okno dialogowe Lista elementów dla wirtualnych jest teraz dostępne dla użytkowników widzących. Wszystkie elementy sterujące są widoczne na ekranie. (#1321)
* Lista wpisów w oknie dialogowym Słownik mowy jest teraz bardziej czytelna dla użytkowników widzących. Lista jest teraz wystarczająco duża, aby wyświetlić wszystkie jej kolumny na ekranie. (#90)
* Na monitorach brajlowskich ALVA BC640/BC680 NVDA nie ignoruje już wyświetlacza, które są nadal przytrzymywane po zwolnieniu innego.
* Program Adobe Reader X nie ulega już awarii po pozostawieniu nieoznakowanych opcji dokumentu przed wyświetleniem okna dialogowego przetwarzania. (#1218)
* NVDA przełącza się teraz na odpowiedni sterownik monitora brajlowskiego po powrocie do zapisanej konfiguracji. (#1346)
* Kreator projektu programu Visual Studio 2008 jest ponownie odczytywany poprawnie. (#974)
* NVDA nie działa już całkowicie w aplikacjach, które zawierają znaki spoza ASCII w swojej nazwie wykonywalnej. (#1352)
* Podczas czytania po wierszu w AkelPad z włączonym zawijaniem wierszy, NVDA nie czyta już pierwszego znaku następnego wiersza na końcu bieżącego wiersza.
* W edytorze kodu Visual Studio 2005/2008 NVDA nie odczytuje już całego tekstu po każdym wpisanym znaku. (#975)
* Naprawiono błąd, który powodował, że niektóre monitory brajlowskie nie były poprawnie czyszczone po zamknięciu NVDA lub zmianie wyświetlacza.
* Początkowy fokus nie jest już czasami wypowiadany dwa razy, gdy NVDA się uruchamia. (#1359)

### Zmiany dla deweloperów

* SCons jest teraz używany do przygotowania drzewa źródłowego i tworzenia kompilacji binarnych, przenośnych archiwów, instalatorów itp. Zobacz readme.txt w katalogu głównym dystrybucji źródłowej, aby uzyskać szczegółowe informacje.
* Nazwy kluczy używane przez NVDA (w tym kluczowe mapy) zostały uczynione bardziej przyjaznymi/logicznymi; np. upArrow zamiast extendedUp i numpadPageUp zamiast prior. Listę można znaleźć w module vkCodes.
* Wszystkie dane wejściowe od użytkownika są teraz reprezentowane przez inputCore.InputGesture wystąpienie. (#601)
 * Każde źródło danych wejściowych tworzy podklasy klasy bazowej InputGesture.
 * Naciśnięcia na klawiaturze systemowej są objęte klasą keyboardHandler.KeyboardInputGesture.
 * Naciśnięcia przycisków, pokręteł i innych elementów sterujących na monitorze brajlowskim są objęte podklasami alfabetu Braille'a. BrailleDisplayGesture, klasa. Te podklasy są dostarczane przez każdy sterownik monitora brajlowskiego.
* Gesty wejściowe są powiązane z obiektami ScriptableObjects za pomocą metody ScriptableObject.bindGesture() w instancji lub __gestures dict w klasie, która mapuje identyfikatory gestów na nazwy skryptów. Aby uzyskać szczegółowe informacje, zobacz baseObject.ScriptableObject .
* Moduły aplikacji nie mają już plików map kluczy. Wszystkie powiązania gestów wejściowych muszą być wykonane w samym module aplikacji.
* Wszystkie skrypty przyjmują teraz instancję InputGesture zamiast naciśnięcia.
 * Gesty KeyboardInputGestures mogą być wysyłane do systemu operacyjnego przy użyciu metody send() gestu.
* Aby wysłać dowolne naciśnięcie, należy teraz utworzyć gest KeyboardInputGesture za pomocą metody KeyboardInputGesture.fromName(), a następnie użyć jego metody send().
* Ustawienia regionalne mogą teraz udostępniać plik mapy gestów wejściowych, aby dodać nowe powiązania lub nadpisać istniejące powiązania dla skryptów w dowolnym miejscu w NVDA. (#810)
 * Mapy gestów ustawień regionalnych powinny być umieszczone w locale\LANG\gestures.ini, gdzie LANG jest kodem języka.
 * Zobacz inputCore.GlobalGestureMap, aby uzyskać szczegółowe informacje na temat formatu pliku.
* Nowe zachowania LiveText i Terminal NVDAObject ułatwiają automatyczne raportowanie nowego tekstu. Aby uzyskać szczegółowe informacje, zobacz te klasy w NVDAObjects.behaviors. (#936)
 * Klasa nakładki NVDAObjects.window.DisplayModelLiveText może być używana dla obiektów, które muszą pobierać tekst zapisany na ekranie.
 * Zobacz moduły aplikacji mirc i putty, aby zapoznać się z przykładami użycia.
* Nie ma już modułu aplikacji _default. Moduły aplikacji powinny zamiast tego tworzyć podklasy appModuleHandler.AppModule (podstawowa klasa AppModule).
* Obsługa globalnych wtyczek, które mogą globalnie wiązać skrypty, obsługiwać zdarzenia NVDAObject i wybierać klasy nakładek NVDAObject. (#281) Aby uzyskać szczegółowe informacje, zobacz globalPluginHandler.GlobalPlugin.
* W obiektach SynthDriver dostępne* atrybuty dla ustawień ciągów (np. availableVoices i availableVariants) są teraz OrderedDicts z kluczem ID, a nie listami.
* synthDriverHandler.VoiceInfo przyjmuje teraz opcjonalny argument języka, który określa język głosu.
* Obiekty SynthDriver udostępniają teraz atrybut języka, który określa język bieżącego głosu.
 * Implementacja podstawowa używa języka określonego w obiektach VoiceInfo w availableVoices. Jest to odpowiednie dla większości syntezatorów, które obsługują jeden język na głos.
* Sterowniki monitorów brajlowskich zostały ulepszone, aby umożliwić powiązanie przycisków, kółek i innych elementów sterujących ze skryptami NVDA:
 * Sterowniki mogą dostarczyć globalną mapę gestów wejściowych, aby dodać powiązania dla skryptów w dowolnym miejscu w NVDA.
 * Mogą również udostępniać własne skrypty do wykonywania określonych funkcji wyświetlania.
 * Zobacz alfabet Braille'a. BrailleDisplayDriver w celu uzyskania szczegółowych informacji i istniejących sterowników monitora brajlowskiego w celu zapoznania się z przykładami.
* Nazwa właściwości "selfVoicing" w klasach AppModule została teraz zmieniona na "sleepMode".
* Nazwy zdarzeń modułu aplikacji event_appLoseFocus i event_appGainFocus zostały teraz zmienione na event_appModule_loseFocus i event_appModule_gainFocus, aby konwencja nazewnictwa była spójna z modułami aplikacji i interceptorami drzew.
* Wszystkie sterowniki monitorów brajlowskich powinny teraz używać alfabetu Braille'a. BrailleDisplayDriver zamiast brajla. BrailleDisplayDriverWithCursor.
 * Kursor jest teraz zarządzany poza sterownikiem.
 * Istniejące sterowniki muszą tylko odpowiednio zmienić instrukcję class i zmienić nazwę metody _display do wyświetlenia.

## 2010.2

Godne uwagi funkcje tego wydania obejmują znacznie uproszczoną nawigację po obiektach; wirtualne dla treści Adobe Flash; dostęp do wielu wcześniej niedostępnych elementów sterujących poprzez pobieranie tekstu zapisanego na ekranie; płaski przegląd tekstu na ekranie; obsługa dokumentów IBM Lotus Symphony; raportowanie nagłówków wierszy i kolumn tabeli w przeglądarce Mozilla Firefox; i znacznie ulepszoną dokumentację użytkownika.

### Nowe funkcje

* Nawigacja między obiektami za pomocą kursora recenzji została znacznie uproszczona. Kursor recenzji wyklucza teraz obiekty, które nie są przydatne dla użytkownika; tj. obiekty używane tylko do celów układu i obiekty niedostępne.
* W aplikacjach korzystających z mostka Java Access Bridge (w tym OpenOffice.org) formatowanie może być teraz raportowane w kontrolkach tekstowych. (#358, #463)
* Po najechaniu myszką na komórki w programie Microsoft Excel, NVDA odpowiednio je ogłosi.
* W aplikacjach korzystających z mostka Java Access Bridge tekst okna dialogowego jest teraz raportowany po jego wyświetleniu. (#554)
* VirtualBuffer może być teraz używany do nawigacji po zawartości Adobe Flash. Nawigacja po obiektach i bezpośrednia interakcja z kontrolkami (poprzez włączenie trybu ostrości) jest nadal obsługiwana. (#453)
* Edytowalne kontrolki tekstowe w środowisku IDE Eclipse, w tym edytor kodu, są teraz dostępne. Musisz używać środowiska Eclipse 3.6 lub nowszego. (#256, #641)
* NVDA może teraz pobrać większość tekstu zapisanego na ekranie. (#40, #643)
 * Pozwala to na odczytywanie kontrolek, które nie ujawniają informacji w bardziej bezpośredni/wiarygodny sposób.
 * Formanty dostępne za pomocą tej funkcji obejmują: niektóre elementy menu, które wyświetlają ikony (np. menu Otwórz za pomocą plików w systemie Windows XP) (#151), edytowalne pola tekstowe w aplikacjach Windows Live (#200), listę błędów w programie Outlook Express (#582), edytowalną kontrolkę tekstową w programie TextPad (#605), listy w programie Eudora, wiele kontrolek w australijskim e-podatku oraz pasek formuły w programie Microsoft Excel.
* Obsługa edytora kodu w programach Microsoft Visual Studio 2005 i 2008. Wymagany jest co najmniej program Visual Studio Standard; Nie działa to w edycjach Express. (#457)
* Obsługa dokumentów IBM Lotus Symphony.
* Wczesna eksperymentalna obsługa przeglądarki Google Chrome. Należy pamiętać, że obsługa czytnika ekranu w Chrome jest daleka od ukończenia i może być również wymagana dodatkowa praca w NVDA. Aby tego spróbować, będziesz potrzebować najnowszej wersji rozwojowej Chrome.
* Stan przełączania (Caps Lock, Num Lock i Scroll Lock) jest teraz wyświetlany w alfabecie Braille'a po ich naciśnięciu. (#620)
* Balony pomocy są teraz wyświetlane w alfabecie Braille'a, gdy się pojawią. (#652)
* Dodano sterownik monitora brajlowskiego MDV Lilli. (#241)
* Po zaznaczeniu całego wiersza lub kolumny w programie Microsoft Excel za pomocą skrótu shift+spacja i control+spacja, nowy wybór jest teraz raportowany. (#759)
* Można teraz raportować nagłówki wierszy i kolumn tabeli. Można to skonfigurować w oknie dialogowym Preferencje formatowania dokumentu.
 * Obecnie jest to obsługiwane w dokumentach w aplikacjach Mozilli, takich jak Firefox (wersja 3.6.11 i nowsze) oraz Thunderbird (wersja 3.1.5 i nowsze). (#361)
* Wprowadzono polecenia dla płaskiego przeglądu: (#58)
 * NVDA+klawiatura numeryczna7 przełącza się na płaski przegląd, umieszczając kursor recenzji w pozycji bieżącego obiektu, co pozwala na przejrzenie ekranu (lub dokumentu, jeśli się w nim znajduje) za pomocą poleceń przeglądu tekstu.
 * NVDA+klawiatura numeryczna1 przesuwa kursor recenzji do obiektu reprezentowanego przez tekst w miejscu kursora recenzji, umożliwiając nawigację po obiekcie od tego punktu.
* Bieżące ustawienia użytkownika NVDA można skopiować do użycia na bezpiecznych ekranach systemu Windows, takich jak ekrany logowania i UAC, naciskając przycisk w oknie dialogowym Ustawienia ogólne. (#730)
* Wsparcie dla przeglądarki Mozilla Firefox 4.
* Obsługa przeglądarki Microsoft Internet Explorer 9.

### Zmiany

* Komendy sayAll by Navigator object (NVDA+numpadAdd), navigator object next in flow (NVDA+shift+numpad6) i navigator object previous in flow (NVDA+shift+numpad4) zostały na razie usunięte z powodu błędów i w celu zwolnienia dla innych możliwych funkcji.
* W oknie dialogowym syntezatora NVDA wyświetlana jest teraz tylko nazwa wyświetlana syntezatora. Wcześniej był poprzedzony imieniem i nazwiskiem kierowcy, które ma znaczenie tylko wewnętrznie.
* Gdy jesteś w osadzonych aplikacjach lub wirtualnych wewnątrz innego virtualBuffera (np. Flash), możesz teraz nacisnąć nvda+control+spacja, aby wyjść z wbudowanej aplikacji lub wirtualnego bufora do zawierającego dokumentu. Poprzednio używano do tego celu nvda+space. Teraz nvda+space służy tylko do przełączania trybów przeglądania/ostrości w virtualBuffers.
* Jeśli przeglądarka mowy (włączona w menu narzędzi) zostanie aktywna (np. została kliknięta), nowy tekst nie pojawi się w kontrolce, dopóki fokus nie zostanie przeniesiony. Pozwala to na łatwiejsze zaznaczanie tekstu (np. do kopiowania).
* Przeglądarka dziennika i konsola języka Python są maksymalizowane po aktywacji.
* W przypadku skoncentrowania się na arkuszu w programie Microsoft Excel, w którym zaznaczona jest więcej niż jedna komórka, ogłaszany jest zakres zaznaczenia, a nie tylko aktywna komórka. (#763)
* Zapisywanie konfiguracji i zmiana poszczególnych wrażliwych opcji jest teraz wyłączona podczas uruchamiania na ekranach logowania, UAC i innych bezpiecznych ekranów systemu Windows.
* Zaktualizowano syntezator mowy eSpeak do wersji 1.44.03.
* Jeśli NVDA jest już uruchomione, aktywacja skrótu NVDA na pulpicie (co obejmuje naciśnięcie Control+Alt+n) spowoduje ponowne uruchomienie NVDA.
* Usunięto pole wyboru raportu pod myszą z okna dialogowego Ustawienia myszy i zastąpiono je polem wyboru Włącz śledzenie myszy, które lepiej pasuje do skryptu przełączania śledzenia myszy (NVDA+m).
* Zaktualizowano układ klawiatury komputera przenośnego, tak aby zawierał wszystkie polecenia dostępne w układzie pulpitu i działał poprawnie na klawiaturach innych niż angielski. (#798, #800)
* Znaczące ulepszenia i aktualizacje dokumentacji użytkownika, w tym dokumentacja poleceń klawiaturowych laptopa oraz synchronizacja podręcznego przewodnika poleceń klawiaturowych z podręcznikiem użytkownika. (#455)
* Zaktualizowano tłumacz brajlowski liblouis do wersji 2.1.1. Warto zauważyć, że rozwiązuje to niektóre problemy związane z chińskim brajlem, a także znakami, które nie są zdefiniowane w tabeli tłumaczeń. (#484, #499)

### Poprawki błędów

* W μTorrent aktywny element na liście torrentów nie zgłasza już wielokrotnie ani nie kradnie fokusu, gdy otwarte jest menu.
* W programie μTorrent są teraz raportowane nazwy plików na liście zawartości torrentów.
* W aplikacjach Mozilli fokus jest teraz poprawnie wykrywany, gdy ląduje na pustej tabeli lub drzewie.
* W aplikacjach Mozilli komunikat "niezaznaczone" jest teraz poprawnie zgłaszany dla kontrolek, które można sprawdzić, takich jak sprawdzalne komórki tabeli. (#571)
* W aplikacjach Mozilli tekst poprawnie zaimplementowanych okien dialogowych ARIA nie jest już ignorowany i będzie teraz zgłaszany, gdy pojawi się okno dialogowe. (#630)
* w programie Internet Explorer i innych formantach MSHTML atrybut poziomu ARIA jest teraz poprawnie honorowany.
* W programie Internet Explorer i innych formantach MSHTML rola ARIA jest teraz wybierana zamiast informacji o innych typach, aby zapewnić znacznie bardziej poprawne i przewidywalne środowisko ARIA.
* Zatrzymano rzadką awarię programu Internet Explorer podczas przechodzenia między ramkami lub elementami iFrame.
* W dokumentach programu Microsoft Word wiersze pisane od prawej do lewej (takie jak tekst arabski) można ponownie odczytać. (#627)
* Znacznie zmniejszono opóźnienia, gdy duże ilości tekstu są wyświetlane w konsoli poleceń systemu Windows w systemach 64-bitowych. (#622)
* Jeśli Skype jest już uruchomiony w momencie uruchomienia NVDA, nie jest już konieczne ponowne uruchamianie Skype'a, aby włączyć dostępność. Może to być również prawdą w przypadku innych aplikacji, które sprawdzają flagę czytnika ekranu systemu.
* W aplikacjach pakietu Microsoft Office NVDA nie ulega już awarii po naciśnięciu przycisku mów pierwszy plan (NVDA+b) lub podczas nawigowania po niektórych obiektach na paskach narzędzi. (#616)
* Naprawiono niepoprawne mówienie liczb zawierających 0 po separatorze; np. 1 023. (#593)
* Programy Adobe Acrobat Pro i Reader 9 nie powodują już awarii podczas zamykania pliku lub wykonywania niektórych innych zadań. (#613)
* Zaznaczenie jest teraz ogłaszane po naciśnięciu Control + a w celu zaznaczenia całego tekstu w niektórych edytowalnych kontrolkach tekstu, takich jak program Microsoft Word. (#761)
* W kontrolkach Scintilla (np. Notepad++) tekst nie jest już niepoprawnie zaznaczony, gdy NVDA przesuwa karetkę, np. podczas mówienia wszystkiego. (#746)
* Ponownie możliwe jest przejrzenie zawartości komórek w programie Microsoft Excel za pomocą kursora przeglądania.
* NVDA może ponownie odczytywać wiersze w niektórych problematycznych polach textArea w Internet Explorerze 8. (#467)
* Program Windows Live Messenger 2009 nie jest już zamykany natychmiast po uruchomieniu, gdy działa NVDA. (#677)
* W przeglądarkach internetowych nie jest już konieczne naciskanie Tab, aby wejść w interakcję z osadzonym obiektem (takim jak zawartość Flash) po naciśnięciu Enter na osadzonym obiekcie lub powrocie z innej aplikacji. (#775)
* W kontrolkach Scintilla (np. Notepad++) początek długich wierszy nie jest już obcinany po przewinięciu poza ekran. Ponadto te długie linie będą poprawnie wyświetlane w alfabecie Braille'a, gdy zostaną zaznaczone.
* W Loudtalks można teraz uzyskać dostęp do listy kontaktów.
* Adres URL dokumentu i "Zarejestrowany program obsługi MSAAHTML" nie są już czasami fałszywie zgłaszane w programie Internet Explorer i innych formantach MSHTML. (#811)
* W widokach drzewa w środowisku IDE Eclipse poprzednio skoncentrowany element nie jest już niepoprawnie ogłaszany, gdy fokus zostanie przeniesiony do nowego elementu.
* NVDA działa teraz poprawnie w systemie, w którym bieżący katalog roboczy został usunięty ze ścieżki wyszukiwania DLL (poprzez ustawienie wpisu rejestru CWDIllegalInDllSearch na 0xFFFFFFFF). Pamiętaj, że nie dotyczy to większości użytkowników. (#907)
* Gdy polecenia nawigacji po tabeli są używane poza tabelą w programie Microsoft Word, "krawędź tabeli" nie jest już wypowiadana po "nie ma w tabeli". (#921)
* Gdy polecenia nawigacji po tabeli nie mogą się poruszać, ponieważ znajdują się na krawędzi tabeli w programie Microsoft Word, "krawędź tabeli" jest teraz wypowiadana w skonfigurowanym języku NVDA, a nie zawsze w języku angielskim. (#921)
* W programach Outlook Express, Poczta systemu Windows i Poczta usługi Windows Live jest teraz raportowany stan pól wyboru na listach reguł wiadomości. (#576)
* Opis reguł wiadomości można teraz odczytać w programie Poczta usługi Windows Live 2010.

## 2010.1

Ta wersja koncentruje się przede wszystkim na poprawkach błędów i ulepszeniach środowiska użytkownika, w tym kilku istotnych poprawkach stabilności.

### Nowe funkcje

* NVDA nie uruchamia się już w systemie bez urządzeń wyjściowych audio. Oczywiście w tym przypadku do wyjścia będzie konieczne użycie monitora brajlowskiego lub syntezatora Silence w połączeniu z przeglądarką mowy. (#425)
* Do okna dialogowego Ustawienia formatowania dokumentu dodano pole wyboru punktów orientacyjnych raportu, które pozwala skonfigurować, czy NVDA ma ogłaszać punkty orientacyjne w dokumentach internetowych. Aby zapewnić zgodność z poprzednią wersją, opcja jest domyślnie włączona.
* Jeśli włączone jest odczytywanie poleceń, NVDA będzie teraz ogłaszać nazwy multimedialnych (np. play, stop, strona główna, itp.) na wielu klawiaturach po ich naciśnięciu. (#472)
* NVDA ogłasza teraz, że słowo jest usuwane po naciśnięciu control+backspace w kontrolkach, które je obsługują. (#491)
* strzałek mogą być teraz używane w oknie formatora internetowego do nawigacji i czytania tekstu. (#452)
* Lista wpisów w książce adresowej programu Microsoft Office Outlook jest teraz obsługiwana.
* NVDA lepiej obsługuje osadzone edytowalne (w trybie projektowania) dokumenty w Internet Explorerze. (#402)
* nowy skrypt (nvda+shift+numpadMinus) pozwala na przeniesienie fokusu systemowego na bieżący obiekt nawigatora.
* Nowe skrypty do blokowania i odblokowywania lewego i prawego przycisku myszy. Przydatne do wykonywania operacji przeciągania i upuszczania. shift+klawiatura numerycznaPodziel, aby zablokować/odblokować lewą, shift+klawiatura numerycznaPomnóż, aby zablokować/odblokować prawą.
* Nowe tabele tłumaczeń brajlowskich: niemiecki 8-punktowy komputerowy brajl, niemiecki klasa 2, fiński 8-punktowy komputerowy brajl, chiński (Hongkong, kantoński), chiński (Tajwan, Manderin). (#344, #369, #415, #450)
* Teraz można wyłączyć tworzenie skrótu na pulpicie (a tym samym skrótu) podczas instalacji NVDA. (#518)
* NVDA może teraz korzystać z IAccessible2, gdy jest obecny w aplikacjach 64-bitowych. (#479)
* Ulepszona obsługa aktywnych regionów w aplikacjach Mozilli. (#246)
* Interfejs API klienta kontrolera NVDA jest teraz dostępny, aby umożliwić aplikacjom kontrolowanie NVDA; np. do czytania tekstu, wyciszania mowy, wyświetlania wiadomości w alfabecie Braille'a itp.
* Informacje i komunikaty o błędach są teraz odczytywane na ekranie logowania w systemach Windows Vista i Windows 7. (#506)
* W programie Adobe Reader obsługiwane są teraz interaktywne formularze PDF opracowane za pomocą programu Adobe LiveCycle. (#475)
* W Miranda IM, NVDA automatycznie odczytuje przychodzące wiadomości w oknach czatu, jeśli włączone jest raportowanie dynamicznych zmian zawartości. Dodano również komendy informujące o trzech ostatnich wiadomościach (NVDA+kontrolka+numer). (#546)
* Pola tekstu wejściowego są teraz obsługiwane w zawartości Adobe Flash. (#461)

### Zmiany

* Niezwykle szczegółowy komunikat pomocy klawiatury w menu Start systemu Windows 7 nie jest już zgłaszany.
* Syntezator Display został zastąpiony nową przeglądarką mowy. Aby ją aktywować, wybierz polecenie Przeglądarka mowy z menu Narzędzia. Przeglądarka mowy może być używana niezależnie od używanego syntezatora mowy. (#44)
* Wiadomości na monitorze brajlowskim zostaną automatycznie odrzucone, jeśli użytkownik naciśnie, który spowoduje zmianę, taką jak przesunięcie ostrości. Wcześniej wiadomość zawsze pozostawała dostępna przez skonfigurowany czas.
* Ustawienie, czy brajl powinien być przywiązany do fokusa, czy kursora przeglądania (NVDA+control+t) można teraz również ustawić w oknie dialogowym ustawień brajla i jest ono teraz również zapisywane w konfiguracji użytkownika.
* Zaktualizowano syntezator mowy eSpeak do wersji 1.43.
* Zaktualizowano tłumacza brajlowskiego liblouis do wersji 1.8.0.
* W wirtualnych znacznie poprawiono raportowanie elementów podczas poruszania się po znaku lub słowie. Wcześniej zgłaszano wiele nieistotnych informacji, a raportowanie bardzo różniło się od tego w przypadku przemieszczania się liniowego. (#490)
* Control teraz po prostu zatrzymuje mowę, tak jak inne, zamiast wstrzymywać mowę. Aby wstrzymać/wznowić mowę, użyj Shift.
* Liczba wierszy i kolumn tabeli nie jest już ogłaszana podczas zgłaszania zmian fokusu, ponieważ ten komunikat jest raczej rozwlekły i zwykle nieprzydatny.

### Poprawki błędów

* NVDA nie uruchamia się już, jeśli obsługa automatyzacji interfejsu użytkownika wydaje się być dostępna, ale z jakiegoś powodu nie można się zainicjować. (#483)
* Cała zawartość wiersza tabeli nie jest już czasami raportowana podczas przenoszenia fokusu do komórki w aplikacjach Mozilli. (#482)
* NVDA nie pozostaje już w tyle przez długi czas podczas rozwijania elementów widoku drzewa, które zawierają bardzo dużą liczbę podelementów.
* Podczas wyświetlania listy głosów SAPI 5, NVDA próbuje teraz wykryć błędne głosy i wyklucza je z okna dialogowego ustawień głosu i pierścienia ustawień syntezatora. Wcześniej, gdy był tylko jeden problematyczny głos, sterownik SAPI 5 NVDA czasami nie uruchamiał się.
* wirtualne uwzględniają teraz ustawienie skrótów obiektu raportu, które można znaleźć w oknie dialogowym Prezentacja obiektu. (#486)
* W wirtualnych współrzędne wierszy/kolumn nie są już niepoprawnie odczytywane dla nagłówków wierszy i kolumn, gdy raportowanie tabel jest wyłączone.
* W wirtualnych współrzędne wierszy/kolumn są teraz poprawnie odczytywane po opuszczeniu tabeli, a następnie ponownym wejściu do tej samej komórki tabeli bez uprzedniego odwiedzania innej komórki; np. naciskając strzałkę w górę, a następnie strzałkę w dółStrzałka w pierwszej komórce tabeli. (#378)
* Puste wiersze w dokumentach programu Microsoft Word i kontrolkach edycji Microsoft HTML są teraz prawidłowo wyświetlane na monitorach brajlowskich. Poprzednio NVDA wyświetlała bieżące zdanie na wyświetlaczu, a nie bieżącą linię w takich sytuacjach. (#420)
* Wiele poprawek bezpieczeństwa podczas uruchamiania NVDA podczas logowania do systemu Windows i na innych bezpiecznych komputerach stacjonarnych. (#515)
* Pozycja kursora (daszek) jest teraz poprawnie aktualizowana podczas wykonywania polecenia Powiedz wszystko, które wychodzi poza dolną część ekranu, w standardowych polach edycji systemu Windows i dokumentach programu Microsoft Word. (#418)
* W wirtualnych tekst nie jest już nieprawidłowo dołączany do obrazów w linkach i klikalnych elementach, które są oznaczone jako nieistotne dla czytników ekranu. (#423)
* Poprawki w układzie klawiatury laptopa. (#517)
* Gdy pismo Braille'a jest podłączone do recenzji po uaktywnieniu się na oknie konsoli Dos, kursor recenzji może teraz prawidłowo nawigować po tekście w konsoli.
* Podczas pracy z TeamTalk3 lub TeamTalk4 Classic, pasek postępu miernika VU w oknie głównym nie jest już ogłaszany podczas aktualizacji. Ponadto znaki specjalne mogą być poprawnie odczytywane w oknie przychodzącego czatu.
* Elementy nie są już wypowiadane dwukrotnie w menu Start systemu Windows 7. (#474)
* Aktywacja linków do tej samej strony w Firefoksie 3.6 odpowiednio przesuwa kursor w virtualBuffer we właściwe miejsce na stronie.
* Rozwiązano problem polegający na tym, że część tekstu nie była renderowana w programie Adobe Reader w niektórych dokumentach PDF.
* NVDA nie wypowiada już niepoprawnie pewnych liczb oddzielonych myślnikiem; np. 500-1000. (#547)
* W systemie Windows XP NVDA nie powoduje już zawieszania się przeglądarki Internet Explorer podczas przełączania pól wyboru w usłudze Windows Update. (#477)
* Podczas korzystania z wbudowanego syntezatora eSpeak jednoczesna mowa i sygnały dźwiękowe nie powodują już sporadycznych zawieszeń w niektórych systemach. Było to najbardziej zauważalne na przykład podczas kopiowania dużych ilości danych w Eksploratorze Windows.
* NVDA nie informuje już, że dokument Firefoksa stał się zajęty (np. z powodu aktualizacji lub odświeżenia), gdy ten dokument działa w tle. Spowodowało to również, że pasek stanu aplikacji na pierwszym planie był fałszywie ogłaszany.
* Podczas przełączania układów klawiatury systemu Windows (za pomocą Control+Shift lub Alt+Shift) pełna nazwa układu jest podawana zarówno w mowie, jak i w alfabecie Braille'a. Wcześniej było to zgłaszane tylko w mowie, a alternatywne układy (np. Dvorak) nie były w ogóle zgłaszane.
* Jeśli raportowanie tabel jest wyłączone, informacje o tabeli nie są już ogłaszane po zmianie fokusu.
* Niektóre standardowe formanty widoku drzewa w aplikacjach 64-bitowych (np. widok drzewa Zawartość w Pomocy Microsoft HTML) są teraz dostępne. (#473)
* Naprawiono niektóre problemy z rejestrowaniem wiadomości zawierających znaki spoza ASCII. W niektórych przypadkach może to powodować fałszywe błędy w systemach innych niż angielskie. (#581)
* Informacje w oknie dialogowym O NVDA pojawiają się teraz w języku skonfigurowanym przez użytkownika, a nie zawsze w języku angielskim. (#586)
* Problemy nie występują już podczas korzystania z dzwonka ustawień syntezatora po zmianie głosu na taki, który ma mniej ustawień niż poprzedni głos.
* W Skypie 4.2 nazwy kontaktów nie są już wymawiane dwukrotnie na liście kontaktów.
* Naprawiono kilka potencjalnie poważnych wycieków pamięci w graficznym interfejsie użytkownika i wirtualnych. (#590, #591)
* Rozwiązano problem z nieprzyjemnym błędem w niektórych syntezatorach SAPI 4, który powodował częste błędy i awarie w NVDA. (#597)

## 2009.1

Główne zalety tej wersji to obsługa 64-bitowych wersji systemu Windows; znacznie ulepszona obsługa dokumentów Microsoft Internet Explorer i Adobe Reader; wsparcie dla systemu Windows 7; odczytywanie ekranów logowania do systemu Windows, control+alt+delete i kontroli konta użytkownika (UAC); oraz możliwość interakcji z treściami Adobe Flash i Sun Java na stronach internetowych. Wprowadzono również kilka istotnych poprawek stabilności i ulepszeń ogólnego doświadczenia użytkownika.

### Nowe funkcje

* Oficjalne wsparcie dla 64-bitowych wersji systemu Windows! (#309)
* Dodano sterownik syntezatora dla syntezatora Newfon. Należy pamiętać, że wymaga to specjalnej wersji Newfon. (#206)
* W wirtualnych tryb koncentracji uwagi i tryb przeglądania mogą być teraz raportowane za pomocą dźwięków zamiast mowy. Jest to domyślnie włączone. Można go skonfigurować w oknie dialogowym wirtualne. (#244)
* NVDA nie anuluje już mowy po naciśnięciu regulacji głośności na klawiaturze, co pozwala użytkownikowi na zmianę głośności i natychmiastowe odsłuchanie rzeczywistych wyników. (#287)
* Całkowicie przepisana obsługa dokumentów Microsoft Internet Explorer i Adobe Reader. Ta obsługa została ujednolicona z podstawową obsługą używaną w Mozilla Gecko, więc funkcje takie jak szybkie renderowanie stron, rozbudowana szybka nawigacja, lista linków, zaznaczanie tekstu, tryb automatycznego ustawiania ostrości i obsługa alfabetu Braille'a są teraz dostępne w tych dokumentach.
* Ulepszono obsługę kontrolki wyboru daty znajdującej się w oknie dialogowym właściwości daty/godziny systemu Windows Vista.
* ulepszona obsługa menu Start programu Modern XP/Vista (w szczególności menu Wszystkie programy i Miejsca). Odpowiednie informacje o poziomie są teraz ogłaszane.
* Ilość tekstu, która jest ogłaszana podczas poruszania myszą, można teraz skonfigurować w oknie dialogowym Ustawienia myszy. Można dokonać wyboru akapitu, wiersza, słowa lub znaku.
* informować o błędach ortograficznych pod kursorem w programie Microsoft Word.
* obsługa modułu sprawdzania pisowni w programie Microsoft Word 2007. Częściowa obsługa może być dostępna dla wcześniejszych wersji programu Microsoft Word.
* Lepsza obsługa programu Poczta usługi Windows Live. Wiadomości tekstowe mogą być teraz odczytywane i można używać zarówno zwykłego tekstu, jak i edytora wiadomości HTML.
* W systemie Windows Vista, jeśli użytkownik przejdzie na bezpieczny pulpit (albo z powodu pojawienia się okna dialogowego kontroli UAC, albo z powodu naciśnięcia control+alt+delete), NVDA ogłosi fakt, że użytkownik znajduje się teraz na bezpiecznym pulpicie.
* NVDA może odczytywać tekst pod myszą w oknach konsoli dos.
* Obsługa automatyzacji interfejsu użytkownika za pośrednictwem interfejsu API klienta automatyzacji interfejsu użytkownika dostępnego w systemie Windows 7, a także poprawki poprawiające działanie NVDA w systemie Windows 7.
* NVDA można skonfigurować tak, aby uruchamiała się automatycznie po zalogowaniu się do systemu Windows. Opcja znajduje się w oknie dialogowym Ustawienia ogólne.
* NVDA może odczytywać bezpieczne ekrany systemu Windows, takie jak ekrany logowania do systemu Windows, control+alt+delete i kontroli konta użytkownika (UAC) w systemie Windows XP i nowszych. Odczytywanie ekranu logowania systemu Windows można skonfigurować w oknie dialogowym Ustawienia ogólne. (#97)
* Dodano sterownik dla monitorów brajlowskich Optelec ALVA serii BC6.
* Podczas przeglądania dokumentów internetowych możesz teraz nacisnąć n i shift+n, aby przeskoczyć odpowiednio do przodu i do tyłu obok bloków linków.
* Podczas przeglądania dokumentów internetowych punkty orientacyjne ARIA są teraz raportowane i można poruszać się po nich do przodu i do tyłu, używając odpowiednio d i shift+d. (#192)
* Okno dialogowe Lista łączy dostępne podczas przeglądania dokumentów internetowych stało się teraz oknem dialogowym Lista elementów, w którym można wyświetlać łącza, nagłówki i punkty orientacyjne. Nagłówki i punkty orientacyjne są prezentowane hierarchicznie. (#363)
* Nowe okno dialogowe Lista elementów zawiera pole "Filtruj według", które umożliwia filtrowanie listy tak, aby zawierała tylko te elementy, w tym tekst, który został wpisany. (#173)
* Przenośne wersje NVDA szukają teraz konfiguracji użytkownika w katalogu 'userConfig' wewnątrz katalogu NVDA. Podobnie jak w przypadku wersji instalatora, dzięki temu konfiguracja użytkownika jest oddzielona od samego NVDA.
* Niestandardowe moduły aplikacji, sterowniki monitora brajlowskiego i sterowniki syntezatora mogą być teraz przechowywane w katalogu konfiguracyjnym użytkownika. (#337)
* wirtualne są teraz renderowane w tle, co pozwala użytkownikowi na pewną interakcję z systemem podczas procesu renderowania. Użytkownik zostanie powiadomiony, że dokument jest renderowany, jeśli trwa to dłużej niż sekundę.
* Jeśli NVDA wykryje, że z jakiegoś powodu zawiesił się, automatycznie przekaże wszystkie naciśnięcia, aby użytkownik miał większą szansę na odzyskanie systemu.
* Obsługa przeciągania i upuszczania ARIA w Mozilla Gecko. (#239)
* Tytuł dokumentu i bieżący wiersz lub zaznaczenie są teraz odczytywane po przeniesieniu fokusu do bufora wirtualnego. Sprawia to, że zachowanie podczas przenoszenia fokusu do wirtualnych jest spójne z zachowaniem normalnych obiektów dokumentów. (#210)
* W wirtualnych można teraz wchodzić w interakcje z obiektami osadzonymi (takimi jak zawartość Adobe Flash i Sun Java), naciskając Enter na obiekcie. Jeśli jest dostępny, możesz go omijać Tab, jak każdą inną aplikację. Aby przywrócić fokus na dokumencie, naciśnij NVDA+spacja. (#431)
* W wirtualnych o i shift+o przesuwają odpowiednio do następnego i poprzedniego osadzonego obiektu.
* NVDA może teraz w pełni korzystać z aplikacji działających jako administrator w systemie Windows Vista i nowszych. Aby to zadziałało, musisz zainstalować oficjalne wydanie NVDA. Nie działa to w przypadku wersji przenośnych i migawek. (#397)

### Zmiany

* NVDA nie informuje już o uruchomieniu NVDA podczas uruchamiania.
* Dźwięki uruchamiania i wychodzenia są teraz odtwarzane przy użyciu skonfigurowanego urządzenia wyjściowego audio NVDA zamiast domyślnego urządzenia wyjściowego audio systemu Windows. (#164)
* Ulepszono raportowanie na pasku postępu. Przede wszystkim możesz teraz skonfigurować NVDA tak, aby ogłaszała zarówno za pomocą mowy, jak i sygnałów dźwiękowych w tym samym czasie.
* Niektóre role ogólne, takie jak okienko, aplikacja i ramka, nie są już raportowane w punkcie koncentracji uwagi, chyba że kontrolka nie ma nazwy.
* Polecenie recenzji kopii (NVDA+f10) kopiuje tekst od znacznika początkowego do bieżącej pozycji recenzji i włącznie, zamiast wykluczać bieżącą pozycję. Pozwala to na skopiowanie ostatniego znaku wiersza, co wcześniej nie było możliwe. (#430)
* skrypt navigatorObject_where (ctrl+NVDA+numpad5) został usunięty. Ta kombinacja nie działała na niektórych klawiaturach, ale skrypt okazał się tak przydatny.
* skrypt navigatorObject_currentDimentions został ponownie zmapowany na NVDA+numpadDelete. Stara kombinacja nie działała na niektórych klawiaturach. Ten skrypt podaje teraz również szerokość i wysokość obiektu zamiast współrzędnych prawej/dolnej.
* Poprawiono wydajność (szczególnie na netbookach), gdy wiele sygnałów dźwiękowych pojawia się w krótkich odstępach czasu; Np. szybki ruch myszy z włączonymi współrzędnymi dźwiękowymi. (#396)
* Dźwięk błędu NVDA nie jest już odtwarzany w wersjach kandydujących i ostatecznych. Należy pamiętać, że błędy są nadal rejestrowane.

### Poprawki błędów

* Gdy NVDA jest uruchamiany ze ścieżki 8.3 dos, ale jest zainstalowany w powiązanej długiej ścieżce (np. progra~1 verses program files), NVDA poprawnie zidentyfikuje, że jest to zainstalowana kopia i poprawnie załaduje ustawienia użytkownika.
* Wypowiadanie tytułu bieżącego okna na pierwszym planie za pomocą NVDA+T działa teraz poprawnie w menu.
* Pismo Braille'a nie pokazuje już bezużytecznych informacji w kontekście fokusu, takich jak nieoznaczone okienka.
* Przestań ogłaszać niektóre bezużyteczne informacje, gdy zmienia się fokus, takie jak panele główne, panele warstwowe i panele przewijania w aplikacjach Java lub Lotus.
* Spraw, aby pole wyszukiwania słów kluczowych w przeglądarce Pomocy systemu Windows (CHM) było znacznie bardziej użyteczne. Z powodu błędów w tej kontrolce bieżące słowo kluczowe nie mogło zostać odczytane, ponieważ ciągle się zmieniało.
* zgłaszać poprawne numery stron w programie Microsoft Word, jeśli numeracja stron została specjalnie przesunięta w dokumencie.
* Lepsza obsługa pól edycyjnych znajdujących się w oknach dialogowych Microsoft Word (np. okno dialogowe Czcionka). Teraz można poruszać się po tych elementach sterujących za pomocą strzałek.
* lepsza obsługa konsol Dos. W szczególności: NVDA może teraz odczytywać zawartość określonych konsol, które zawsze uważała za puste. Naciśnięcie control+break nie powoduje już zakończenia NVDA.
* W systemie Windows Vista i nowszych, instalator NVDA uruchamia teraz NVDA z normalnymi uprawnieniami użytkownika, gdy zostanie poproszony o uruchomienie NVDA na ekranie końcowym.
* Backspace jest teraz poprawnie obsługiwany podczas wypowiadania wpisywanych słów. (#306)
* Nie zgłaszaj błędnie "Menu Start" dla niektórych menu kontekstowych w Eksploratorze Windows/powłoce systemu Windows. (#257)
* NVDA teraz poprawnie obsługuje etykiety ARIA w Mozilla Gecko, gdy nie ma żadnej innej użytecznej zawartości. (#156)
* NVDA nie włącza już automatycznie trybu skupienia dla edytowalnych pól tekstowych, które aktualizują swoją wartość po zmianie fokusu; np. http://tigerdirect.com/. (#220)
* NVDA będzie teraz próbowała odzyskać sprawność po niektórych sytuacjach, które wcześniej powodowały całkowite zamrożenie. Może minąć do 10 sekund, zanim NVDA wykryje i odzyska sprawność po takim zamrożeniu.
* Gdy język NVDA jest ustawiony na "Domyślny dla użytkownika", użyj ustawienia języka wyświetlania systemu Windows zamiast ustawień regionalnych systemu Windows. (#353)
* NVDA uznaje teraz istnienie kontroli w AIM 7.
* Polecenie "Przepuść przez" nie zacina się już, jeśli jest wciśnięty. Poprzednio, NVDA przestawało akceptować polecenia, jeśli to wystąpiło i musiało zostać zrestartowane. (#413)
* Pasek zadań nie jest już ignorowany po otrzymaniu fokusu, co często ma miejsce podczas zamykania aplikacji. Poprzednio NVDA zachowywała się tak, jakby ostrość w ogóle się nie zmieniła.
* Podczas odczytywania pól tekstowych w aplikacjach korzystających z Java Access Bridge (w tym OpenOffice.org), NVDA działa teraz poprawnie, gdy włączone jest raportowanie numerów linii.
* Polecenie review copy (NVDA+f10) z wdziękiem obsługuje przypadek, w którym jest używane na pozycji przed znacznikiem początkowym. Wcześniej mogło to powodować problemy, takie jak awarie w Notepad ++.
* Określony znak kontrolny (0x1) nie powoduje już dziwnego zachowania eSpeak (takich jak zmiany głośności i tonu), gdy napotka go w tekście. (#437)
* Polecenie wyboru tekstu raportu (NVDA+shift+strzałka w górę) teraz uprzejmie informuje, że nie ma zaznaczenia w obiektach, które nie obsługują zaznaczania tekstu.
* Naprawiono błąd, który powodował, że naciśnięcie Enter na niektórych przyciskach lub linkach Miranda-IM powodowało zawieszanie się NVDA. (#440)
* Bieżąca linia lub zaznaczenie jest teraz prawidłowo uwzględniane podczas sprawdzania pisowni lub kopiowania bieżącego obiektu nawigatora.
* Udało się obejść błąd systemu Windows, który powodował wymawianie śmieci po nazwie kontrolek linków w oknach dialogowych Eksploratora Windows i Internet Explorera. (#451)
* Naprawiono problem z poleceniem daty i godziny raportu (NVDA+f12). Wcześniej raportowanie dat było obcinane w niektórych systemach. (#471)
* Rozwiązano problem polegający na tym, że flaga czytnika ekranu systemu była czasami nieprawidłowo czyszczona po interakcji z bezpiecznymi ekranami systemu Windows. Może to powodować problemy w aplikacjach, które sprawdzają flagę czytnika ekranu, w tym Skype, Adobe Reader i Jart. (#462)
* W polu kombi programu Internet Explorer 6 aktywny element jest teraz zgłaszany po jego zmianie. (#342)

## 0.6p3

### Nowe funkcje

* Ponieważ pasek formuły programu Microsoft Excel jest niedostępny dla NVDA, udostępnij okno dialogowe specyficzne dla NVDA do edycji, gdy użytkownik naciśnie f2 w komórce.
* Obsługa formatowania w kontrolkach tekstowych IAccessible2, w tym w aplikacjach Mozilli.
* Błędy ortograficzne można teraz zgłaszać tam, gdzie to możliwe. Można to skonfigurować w oknie dialogowym Preferencje formatowania dokumentu.
* NVDA może być skonfigurowane tak, aby emitowało sygnał dźwiękowy dla wszystkich lub tylko widocznych pasków postępu. Alternatywnie można go skonfigurować tak, aby odczytywał wartości paska postępu co 10%.
* Łącza można teraz identyfikować w kontrolkach edycji rozszerzonej.
* Mysz można teraz przesunąć do znaku znajdującego się pod kursorem recenzji w większości edytowalnych kontrolek tekstowych. Wcześniej mysz można było przesunąć tylko na środek kontrolki.
* W wirtualnych kursor recenzji przegląda teraz tekst bufora, a nie tylko tekst wewnętrzny obiektu navigatora (który często nie jest przydatny dla użytkownika). Oznacza to, że można nawigować po buforze wirtualnym hierarchicznie przy użyciu nawigacji po obiektach, a kursor recenzji zostanie przeniesiony do tego punktu w buforze.
* Obsługa niektórych dodatkowych stanów w kontrolkach Java.
* Jeśli dwukrotnie zostanie naciśnięte polecenie title (NVDA+t), zostanie napisane hasło. Jeśli zostanie naciśnięty trzykrotnie, zostanie skopiowany do schowka.
* Pomoc klawiatury odczytuje teraz nazwy modyfikujących, gdy są wciśnięte samodzielnie.
* Nazwy ogłaszane za pomocą klawiatury są teraz tłumaczalne.
* Dodano obsługę rozpoznanego pola tekstowego w SiRecognizer. (#198)
* Obsługa monitorów brajlowskich!
* Dodano polecenie (NVDA+c) do zgłaszania tekstu w schowku Windows. (#193)
* W virtualBuffers, jeśli NVDA automatycznie przełącza się w tryb skupienia, możesz użyć Escape, aby przełączyć się z powrotem do trybu przeglądania. NVDA+space może być nadal używany.
* W wirtualnych, gdy zmienia się fokus lub karetka jest przesuwana, NVDA może automatycznie przełączyć się w tryb skupienia lub tryb przeglądania, odpowiednio do kontrolki pod karetką. Jest to konfigurowane w oknie dialogowym wirtualne. (#157)
* Przepisany sterownik syntezatora SAPI4, który zastępuje sterowniki sapi4serotek i sapi4activeVoice i powinien naprawić problemy napotkane z tymi sterownikami.
* Aplikacja NVDA zawiera teraz manifest, co oznacza, że nie działa już w trybie zgodności w systemie Windows Vista.
* Plik konfiguracyjny i słowniki mowy są teraz zapisywane w katalogu danych aplikacji użytkownika, jeśli NVDA została zainstalowana za pomocą instalatora. Jest to konieczne dla systemu Windows Vista, a także pozwala wielu użytkownikom na indywidualne konfiguracje NVDA.
* Dodano obsługę informacji o położeniu dla kontrolek IAccessible2.
* Dodano możliwość kopiowania tekstu do schowka za pomocą kursora recenzji. NVDA+f9 ustawia znacznik początkowy na bieżącą pozycję kursora przeglądania. NVDA+f10 pobiera tekst między znacznikiem początkowym a bieżącą pozycją kursora recenzji i kopiuje go do schowka. (#240)
* Dodano obsługę niektórych kontrolek edycji w oprogramowaniu pinacle tv.
* Podczas ogłaszania zaznaczonego tekstu dla długich zaznaczeń (512 znaków lub więcej), NVDA teraz odczytuje liczbę zaznaczonych znaków, a nie całe zaznaczenie. (#249)

### Zmiany

* Jeśli urządzenie wyjściowe audio jest ustawione na korzystanie z domyślnego urządzenia Windows (Microsoft Sound Mapper), NVDA przełączy się teraz na nowe domyślne urządzenie dla eSpeak i tonów, gdy zmieni się domyślne urządzenie. Na przykład, NVDA przełączy się na urządzenie audio USB, jeśli automatycznie stanie się urządzeniem domyślnym po podłączeniu.
* Poprawiono wydajność funkcji eSpeak z niektórymi sterownikami audio systemu Windows Vista.
* Raportowanie linków, nagłówków, tabel, list i cytatów blokowych można teraz skonfigurować w oknie dialogowym ustawień formatowania dokumentu. Wcześniej, aby skonfigurować te ustawienia dla wirtualnych, używano okna dialogowego ustawień bufora wirtualnego. Teraz wszystkie dokumenty współużytkują tę konfigurację.
* Szybkość jest teraz domyślnym ustawieniem w pierścieniu ustawień syntezatora mowy.
* Usprawnij ładowanie i rozładowywanie modułów appModules.
* Polecenie title (NVDA+t) teraz informuje tylko tytuł, a nie cały obiekt. Jeśli obiekt pierwszoplanowy nie ma nazwy, używana jest nazwa procesu aplikacji.
* Zamiast włączania i wyłączania wirtualnego bufora, NVDA raportuje teraz tryb skupienia (przekazywanie włączone) i tryb przeglądania (przekazywanie wyłączone).
* Głosy są teraz przechowywane w pliku konfiguracyjnym według identyfikatora, a nie indeksu. Dzięki temu ustawienia głosowe są bardziej niezawodne we wszystkich systemach i zmianach konfiguracji. Ustawienia głosu nie zostaną zachowane w starych konfiguracjach, a przy pierwszym użyciu syntezatora może zostać zarejestrowany błąd. (#19)
* Poziom elementu widoku drzewa jest teraz ogłaszany jako pierwszy, jeśli zmienił się w stosunku do poprzednio aktywnego elementu dla wszystkich widoków drzewa. Wcześniej występowało to tylko w przypadku natywnych widoków drzewa systemu Windows (SysTreeView32).

### Poprawki błędów

* Ostatni fragment dźwięku nie jest już ucinany podczas korzystania z NVDA z eSpeak na serwerze zdalnego pulpitu.
* Rozwiązano problemy z zapisywaniem słowników mowy dla niektórych głosów.
* Wyeliminuj opóźnienia podczas poruszania się po jednostkach innych niż znak (słowo, wiersz itp.) w kierunku dołu dużych dokumentów tekstowych w wirtualnych Mozilla Gecko. (#155)
* Jeśli włączona jest opcja mów wpisane słowa, ogłoś słowo po naciśnięciu Enter.
* Rozwiązano niektóre problemy z zestawem znaków w dokumentach richedit.
* Przeglądarka dzienników NVDA używa teraz richedit, a nie tylko edit, aby wyświetlić dziennik. Poprawia to czytanie słów za pomocą NVDA.
* Rozwiązano niektóre problemy związane z obiektami osadzonymi w kontrolkach edycji rozszerzonej.
* NVDA odczytuje teraz numery stron w programie Microsoft Word. (#120)
* Naprawiono problem polegający na tym, że naciśnięcie Tab do zaznaczonego pola wyboru w wirtualnym buforze Mozilla Gecko i naciśnięcie spacji nie informowało, że pole wyboru zostało odznaczone.
* Poprawnie zgłaszaj częściowo zaznaczone pola wyboru w aplikacjach Mozilli.
* Jeśli zaznaczenie tekstu rozszerza się lub zmniejsza w obu kierunkach, odczytaj zaznaczenie jako jeden fragment, a nie dwa.
* Podczas czytania za pomocą myszy, tekst w polach edycyjnych Mozilla Gecko powinien być teraz odczytywany.
* Powiedzmy, że wszystko nie powinno już powodować zawieszania się niektórych syntezatorów SAPI5.
* Naprawiono błąd, który powodował, że zmiany zaznaczenia tekstu nie były odczytywane w standardowych kontrolkach edycji systemu Windows przed pierwszą zmianą fokusu po uruchomieniu NVDA.
* Naprawiono śledzenie myszy w obiektach Java. (#185)
* NVDA nie zgłasza już elementów widoku drzewa Javy bez dzieci jako zwiniętych.
* Ogłoś obiekt z fokusem, gdy okno Java pojawi się na pierwszym planie. Wcześniej ogłaszano tylko obiekt Java najwyższego poziomu.
* Sterownik syntezatora eSpeak nie przestaje już całkowicie mówić po pojedynczym błędzie.
* Naprawiono problem polegający na tym, że zaktualizowane parametry głosu (szybkość, wysokość itp.) nie były zapisywane, gdy głos został zmieniony z pierścienia ustawień syntezatora.
* Ulepszono odczytywanie wpisywanych znaków i słów.
* Niektóre nowe teksty, które wcześniej nie były wypowiadane w tekstowych aplikacjach konsolowych (takich jak niektóre tekstowe gry przygodowe), są teraz odczytywane.
* NVDA ignoruje teraz zmiany fokusu w oknach działających w tle. Wcześniej zmiana ostrości tła mogła być traktowana tak, jakby zmieniła się rzeczywista ostrość.
* Poprawiono wykrywanie fokusu podczas opuszczania menu kontekstowego. Poprzednio, NVDA często w ogóle nie reagowała po opuszczeniu menu kontekstowego.
* NVDA informuje teraz, kiedy menu kontekstowe jest aktywowane w menu Start.
* Klasyczne menu Start jest teraz ogłaszane jako menu Start, a nie menu aplikacji.
* Poprawiono odczytywanie alertów, takich jak te napotkane w przeglądarce Mozilla Firefox. Tekst nie powinien być już czytany wiele razy, a inne zbędne informacje nie będą już czytane. (#248)
* Tekst pól edycyjnych tylko do odczytu, z możliwością fokusu, nie będzie już uwzględniany podczas pobierania tekstu okien dialogowych. Naprawia to na przykład automatyczne odczytywanie całej umowy licencyjnej w instalatorach.
* NVDA nie informuje już o usunięciu zaznaczenia tekstu po pozostawieniu niektórych elementów sterujących edycją (np. pasek adresu Internet Explorer, pola adresu e-mail w Thunderbirdzie 3).
* Podczas otwierania wiadomości e-mail w postaci zwykłego tekstu w programach Outlook Express i Poczta systemu Windows fokus jest prawidłowo umieszczany w wiadomości, aby użytkownik mógł ją przeczytać. Wcześniej użytkownik musiał nacisnąć Tab lub kliknąć wiadomość, aby użyć kursora do jej odczytania.
* Naprawiono kilka poważnych błędów związanych z funkcją "Mów poleceń".
* NVDA może teraz odczytywać tekst powyżej 65535 znaków w standardowych kontrolkach edycji (np. duży plik w Notatniku).
* Ulepszono odczytywanie wierszy w polach edycji MSHTML (edytowalne wiadomości programu Outlook Express i pola wprowadzania tekstu w programie Internet Explorer).
* NVDA nie zawiesza się już całkowicie podczas edycji tekstu w OpenOffice. (#148, #180)

## 0.6p2

* Poprawiono domyślny głos ESpeak w NVDA
* Dodano układ klawiatury laptopa. Układy klawiatury można skonfigurować w oknie dialogowym ustawień klawiatury NVDA. (#60)
* Obsługa grupowania elementów w kontrolkach SysListView32, które można znaleźć głównie w systemie Windows Vista. (#27)
* Zgłaszanie sprawdzonego stanu elementów widoku drzewa w kontrolkach SysTreeview32.
* Dodano skrótów dla wielu okien konfiguracji NVDA
* Obsługa aplikacji obsługujących IAccessible2, takich jak Mozilla Firefox, podczas uruchamiania NVDA z nośnika przenośnego, bez konieczności rejestrowania jakichkolwiek specjalnych plików Dll
* Naprawiono awarię z listą linków virtualBuffers w aplikacjach Gecko. (#48)
* NVDA nie powinno już powodować awarii aplikacji Mozilla Gecko, takich jak Firefox i Thunderbird, jeśli NVDA działa z wyższymi uprawnieniami niż aplikacja Mozilla Gecko. Np. NVDA działa jako Administrator.
* W słownikach mowy (wcześniej słownikach użytkownika) może być teraz rozróżniana wielkość liter lub nie, a wzorce mogą opcjonalnie być wyrażeniami regularnymi. (#39)
* To, czy NVDA używa trybu "układu ekranu" dla dokumentów z wirtualnym buforem, można teraz skonfigurować w oknie dialogowym ustawień
* Nie zgłaszaj już tagów kotwic bez href w dokumentach Gecko jako linków. (#47)
* Polecenie wyszukiwania NVDA zapamiętuje teraz to, czego ostatnio szukałeś we wszystkich aplikacjach. (#53)
* Rozwiązano problemy polegające na tym, że stan zaznaczenia nie był ogłaszany dla niektórych pól wyboru i przycisków radiowych w virtualBuffers
* Tryb przekazywania VirtualBuffer jest teraz specyficzny dla każdego dokumentu, a nie dla NVDA globalnie. (#33)
* Naprawiono pewne spowolnienie ze zmianami ostrości i nieprawidłowymi przerwami w mowie, które czasami występowały podczas korzystania z NVDA na systemie, który był w trybie czuwania lub był raczej powolny
* Ulepszono obsługę pól kombi w przeglądarce Mozilla Firefox. Zwłaszcza, gdy strzałka wokół nich nie powtarza się, a podczas wyskakiwania z nich, kontrolki przodków nie są niepotrzebnie ogłaszane. Również polecenia virtualBuffer działają teraz, gdy są skupione na jednym z nich, gdy jesteś w virtualBuffer.
* Poprawiono dokładność znajdowania paska stanu w wielu aplikacjach. (#8)
* Dodano interaktywną konsolę NVDA w Pythonie, aby umożliwić programistom przeglądanie i manipulowanie wewnętrznymi elementami NVDA podczas jej działania
* Skrypty sayAll, reportSelection i reportCurrentLine działają teraz poprawnie w trybie przekazywania virtualBuffer. (#52)
* Usunięto skrypty zwiększające i zmniejszające współczynnika. Użytkownicy powinni korzystać ze skryptów pierścieniowych ustawień syntezatora (control+nvda+strzałki) lub okna dialogowego ustawień głosu
* Popraw zakres i skalę sygnałów dźwiękowych paska postępu
* Dodano więcej szybkich do nowego virtualBuffers: l dla listy, i dla elementu listy, e dla pola edycji, b dla przycisku, x dla pola wyboru, r dla przycisku radiowego, g dla grafiki, q dla cytatu blokowego, c dla pola kombi, od 1 do 6 dla odpowiednich poziomów nagłówków, s dla separatora, m dla ramki. (#67, #102, #108)
* Anulowanie wczytywania nowego dokumentu w przeglądarce Mozilla Firefox pozwala teraz użytkownikowi na dalsze korzystanie z wirtualnego bufora starego dokumentu, jeśli stary dokument nie został jeszcze zniszczony. (#63)
* Nawigacja za pomocą słów w virtualBuffers jest teraz dokładniejsza, ponieważ słowa nie zawierają przypadkowo tekstu z więcej niż jednego pola. (#70)
* Poprawiono dokładność śledzenia ostrości i aktualizacji ostrości podczas nawigacji w wirtualnych Mozilla Gecko.
* Dodano skrypt findPrevious (shift+NVDA+f3) do użycia w nowych virtualBuffers
* Poprawiono spowolnienie w oknach dialogowych Mozilla Gecko (w Firefoksie i Thunderbirdzie). (#66)
* Dodano możliwość przeglądania bieżącego pliku dziennika dla NVDA. można go znaleźć w menu NVDA -> Narzędzia
* Skrypty, takie jak np. godzina i data, uwzględniają teraz bieżący język; Interpunkcja i kolejność słów odzwierciedla teraz język
* Lista rozwijana języka w oknie dialogowym ustawień ogólnych NVDA pokazuje teraz pełne nazwy języków, co ułatwia korzystanie z niego
* Podczas przeglądania tekstu w bieżącym obiekcie nawigatora tekst jest zawsze aktualny, jeśli zmienia się dynamicznie. Np. przeglądanie tekstu elementu listy w Menedżerze zadań. (#15)
* Podczas poruszania się za pomocą myszy ogłaszany jest teraz bieżący akapit tekstu pod myszą, a nie cały tekst w tym konkretnym obiekcie lub tylko bieżące słowo. Również współrzędne dźwiękowe i ogłaszanie ról obiektów jest opcjonalne, są one domyślnie wyłączone
* Obsługa czytania tekstu za pomocą myszy w programie Microsoft Word
* Naprawiono błąd, który powodował, że opuszczenie paska menu w aplikacjach takich jak Wordpad powodowało, że wybór tekstu nie był już ogłaszany
* W Winampie tytuł utworu nie jest już ogłaszany raz za razem podczas przełączania ścieżek lub wstrzymywania/wznawiania/zatrzymywania odtwarzania.
* W Winampie dodano możliwość ogłaszania stanu odtwarzania losowego i powtarzania elementów sterujących po ich przełączeniu. Działa w oknie głównym i w edytorze list odtwarzania
* Poprawiono możliwość aktywacji poszczególnych pól w wirtualnych Mozilla Gecko. Może zawierać klikalną grafikę, linki zawierające akapity i inne dziwne struktury
* Naprawiono początkowe opóźnienie podczas otwierania okien dialogowych NVDA na niektórych systemach. (#65)
* Dodano specjalne wsparcie dla aplikacji Total Commander
* Naprawiono błąd w sterowniku sapi4serotek, który powodował, że wysokość dźwięku mogła zostać zablokowana na określonej wartości, tj. utrzymywała się na wysokim poziomie po przeczytaniu wielkiej litery. (#89)
* Ogłaszaj klikalny tekst i inne pola jako klikalne w Mozilla Gecko VirtualBuffers. Na przykład.  pole, które ma atrybut HTML onclick. (#91)
* Podczas poruszania się po wirtualnych Mozilla Gecko, przewiń bieżące pole do środka - jest to przydatne, aby widzący rówieśnicy mieli pojęcie, gdzie użytkownik znajduje się w dokumencie. (#57)
* Dodano podstawową obsługę wydarzeń pokazów regionu na żywo ARIA w aplikacjach obsługujących IAccessible2. Przydatne w aplikacji IRC Chatzilla, nowe wiadomości będą teraz odczytywane automatycznie
* Kilka drobnych ulepszeń ułatwiających korzystanie z aplikacji internetowych obsługujących ARIA, np. Google Docs
* Przestań dodawać dodatkowe puste wiersze do tekstu podczas kopiowania go z virtualBuffer
* Zatrzymaj spacji przed aktywowaniem łącza na liście łączy. Teraz można go używać jak innych liter, aby rozpocząć wpisywanie nazwy konkretnego linku, do którego chcesz przejść
* Skrypt moveMouseToNavigator (NVDA+numpadSlash) przenosi teraz mysz do środka obiektu nawigatora, a nie do lewego górnego rogu.
* Dodano skrypty do klikania lewym i prawym przyciskiem myszy (odpowiednio numpadSlash i numpadStar)
* Popraw dostęp do zasobnika systemowego Windows. Miejmy nadzieję, że skupienie nie powinno już sprawiać wrażenia, że wraca do jednego konkretnego przedmiotu. Przypomnienie: aby dostać się do zasobnika systemowego, użyj polecenia Windows WindowsKey+b. (#10)
* Zwiększ wydajność i przestań ogłaszać dodatkowy tekst po przytrzymaniu kursora w polu edycji i osiągnięciu końca
* Wyłącz możliwość zmuszania użytkownika do czekania przez NVDA, aż określone wiadomości zostaną wypowiedziane. Naprawia niektóre awarie/zawieszanie się niektórych syntezatorów mowy. (#117)
* Dodano obsługę syntezatora mowy Audiologic Tts3, współautor Gianluca Casalino. (#105)
* Prawdopodobnie poprawiono wydajność podczas poruszania się po dokumentach w programie Microsoft Word
* Poprawiono dokładność podczas odczytywania tekstu alertów w aplikacjach Mozilla Gecko
* Zatrzymaj możliwe awarie podczas próby zapisania konfiguracji w wersjach systemu Windows innych niż angielska. (#114)
* Dodaj okno powitalne NVDA. To okno dialogowe ma na celu dostarczenie niezbędnych informacji dla nowych użytkowników i pozwala na skonfigurowanie CapsLocka jako modyfikującego NVDA. To okno dialogowe będzie wyświetlane, gdy NVDA jest domyślnie uruchomione, dopóki nie zostanie wyłączone.
* Naprawiono podstawową obsługę programu Adobe Reader, aby możliwe było odczytywanie dokumentów w wersjach 8 i 9
* Napraw niektóre błędy, które mogły wystąpić podczas przytrzymywania przed poprawną inicjalizacją NVDA
* Jeśli użytkownik skonfigurował NVDA tak, aby zapisywał konfigurację przy wyjściu, upewnij się, że konfiguracja jest poprawnie zapisana podczas zamykania lub wylogowywania się z systemu Windows.
* Dodano dźwięk logo NVDA na początku instalatora, wniesiony przez Victer Tsaran
* NVDA, zarówno uruchomiony w instalatorze, jak i w inny sposób, powinien poprawnie wyczyścić ikonę w zasobniku systemowym po zamknięciu
* Etykiety standardowych elementów sterujących w oknach dialogowych NVDA (takich jak przyciski Ok i Anuluj) powinny teraz być wyświetlane w języku, na który NVDA jest ustawione, a nie tylko pozostawać w języku angielskim.
* Ikona NVDA powinna być teraz używana dla skrótów NVDA w menu Start i na pulpicie, a nie jako domyślna ikona aplikacji.
* Czytaj komórki w MS Excel podczas poruszania się za pomocą Tab i Shift+Tab. (#146)
* Napraw podwójne mówienie na określonych listach w Skypie.
* Ulepszone śledzenie karetki w aplikacjach IAccessible2 i Java; np. w Open Office i Lotus Symphony, NVDA poprawnie czeka na przesunięcie się karetki w dokumentach, zamiast przypadkowo przeczytać niewłaściwe słowo lub wiersz na końcu niektórych akapitów. (#119)
* Obsługa kontrolek AkelEdit w Akelpad 4.0
* NVDA nie blokuje się już w Lotus Synphony podczas przechodzenia z dokumentu do paska menu.
* NVDA nie zawiesza się już w aplecie Dodaj/Usuń programy systemu Windows XP podczas uruchamiania deinstalatora. (#30)
* NVDA nie zawiesza się już po otwarciu Spybot Search and Destroy

## 0.6p1

### Dostęp do treści internetowych z nowymi wirtualnymi w procesie (do tej pory dla aplikacji Mozilla Gecko, w tym Firefox3 i Thunderbird3)

* Czas ładowania został poprawiony prawie trzydziestokrotnie (nie trzeba już w ogóle czekać, aż większość stron internetowych załaduje się do bufora)
* Dodano listę linków (NVDA+f7)
* Ulepszono okno dialogowe wyszukiwania (control+nvda+f) tak, aby wykonywało wyszukiwanie z uwzględnieniem wielkości liter, a także naprawiono kilka problemów z fokusem w tym oknie dialogowym.
* Teraz możliwe jest zaznaczanie i kopiowanie tekstu w nowym virtualBuffers
* Domyślnie nowe virtualBuffers reprezentują dokument w układzie ekranu (linki i kontrolki nie znajdują się w osobnych wierszach, chyba że są naprawdę widoczne wizualnie). Możesz przełączyć tę funkcję za pomocą NVDA+v.
* Możliwe jest poruszanie się po akapicie za pomocą control+strzałka w górę i control+strzałka w dół.
* Ulepszona obsługa zawartości dynamicznej
* Poprawiono dokładność odczytywania linii i pól podczas naciskania strzałek w górę i w dół.

### Internacjonalizacji

* Możliwe jest teraz wpisywanie znaków akcentowanych, które opierają się na "martwym znaku", podczas gdy NVDA jest uruchomiona.
* NVDA informuje teraz, kiedy układ klawiatury zostanie zmieniony (po naciśnięciu alt+shift).
* Funkcja ogłaszania daty i godziny uwzględnia teraz bieżące opcje regionalne i językowe systemu.
* dodano czeskie tłumaczenie (autorstwa Tomasa Valuška z pomocą Jaromira Vit)
* dodano tłumaczenie na język wietnamski autorstwa Dang Hoai Phuc
* Dodano tłumaczenie Afrykanów (af_ZA) autorstwa Willema van der Walta.
* Dodano rosyjskie tłumaczenie autorstwa Dmitrija Kaslina
* Dodano polskie tłumaczenie autorstwa DOROTY CZAJKI i przyjaciół.
* Dodano japońskie tłumaczenie autorstwa Katsutoshi Tsuji.
* dodano tajskie tłumaczenie autorstwa Amorn Kiattikhunrat
* dodano chorwackie tłumaczenie autorstwa Mario Percinica i Hrvoje Katic
* Dodano galicyjskie tłumaczenie autorstwa Juana C. buno
* dodano ukraińskie tłumaczenie autorstwa Aleksieja Sadowoja

### Mowa

* NVDA jest teraz dostarczana w pakiecie z eSpeak 1.33, który zawiera wiele ulepszeń, wśród nich są ulepszone języki, nazwane warianty, możliwość szybszego mówienia.
* Okno dialogowe ustawień głosu pozwala teraz na zmianę wariantu syntezatora, jeśli go obsługuje. Wariant jest zazwyczaj niewielką wariacją na temat obecnego głosu. (eSpeak obsługuje różne warianty).
* Dodano możliwość zmiany przegięcia głosu w oknie dialogowym ustawień głosu, jeśli bieżący syntezator to obsługuje. (eSpeak obsługuje fleksję).
* Dodano możliwość wyłączenia mówienia o położeniu obiektu (np. 1 z 4). Opcja ta znajduje się w oknie dialogowym Ustawienia prezentacji obiektów.
* NVDA może teraz emitować sygnał dźwiękowy podczas wypowiadania wielkiej litery. Można to włączać i wyłączać za pomocą pola wyboru w oknie dialogowym ustawień głosowych. Dodano również pole wyboru podbicia dla wielkich liter, aby skonfigurować, czy NVDA faktycznie powinno wykonywać swoje normalne podnoszenie tonu dla wielkich liter. Więc teraz możesz podnieść ton, powiedzmy cap, lub sygnał dźwiękowy dla wielkich liter.
* Dodano możliwość wstrzymywania mowy w NVDA (tak jak w Voice Over dla komputerów Mac). Kiedy NVDA coś mówi, możesz nacisnąć Control lub Shift, aby wyciszyć mowę tak jak zwykle, ale jeśli następnie ponownie naciśniesz Shift (o ile nie nacisnąłeś żadnego innego), mowa będzie kontynuowana dokładnie od miejsca, w którym została przerwana.
* Dodano wirtualny sterownik syntezatora, który wyświetla tekst w oknie zamiast mówić za pośrednictwem syntezatora mowy. Powinno to być przyjemniejsze dla widzących programistów, którzy nie są przyzwyczajeni do syntezy mowy, ale chcą wiedzieć, co mówi NVDA. Prawdopodobnie nadal są jakieś błędy, więc opinie są zdecydowanie mile widziane.
* NVDA nie mówi już domyślnie znaków interpunkcyjnych, możesz włączyć mówienie o interpunkcji za pomocą NVDA+p.
* Domyślnie eSpeak mówi teraz znacznie wolniej, co powinno ułatwić pracę osobom, które korzystają z niego po raz pierwszy, podczas instalacji lub rozpoczęcia korzystania z NVDA.
* Dodano słowniki użytkownika do NVDA. Pozwalają one na sprawienie, że NVDA będzie inaczej odczytywać określony tekst. Dostępne są trzy słowniki: domyślny, głosowy i tymczasowy. Wpisy, które dodasz do domyślnego słownika, będą się pojawiać cały czas w NVDA. Słowniki głosowe są specyficzne dla bieżącego syntezatora i głosu, który aktualnie ustawiłeś. A słownik tymczasowy jest na te momenty, kiedy szybko chcesz ustawić regułę podczas wykonywania określonego zadania, ale nie chcesz, aby była trwała (zniknie, jeśli zamkniesz NVDA). Na razie reguły są wyrażeniami regularnymi, a nie tylko zwykłym tekstem.
* Syntezatory mogą teraz korzystać z dowolnego urządzenia wyjściowego audio w systemie, ustawiając pole kombi urządzenia wyjściowego w oknie dialogowym Syntezator przed wybraniem żądanego syntezatora.

### Wydajność

* NVDA nie zajmuje już ogromnej ilości pamięci systemowej podczas edycji wiadomości w kontrolkach edycji mshtml
* Poprawiono wydajność podczas przeglądania tekstu w wielu kontrolkach, które w rzeczywistości nie mają prawdziwego kursora. np. okno historii MSN Messenger, elementy widoku drzewa, elementy widoku listy itp.
* Poprawiono wydajność w dokumentach do edycji sformatowanej.
* NVDA nie powinno już powoli zwiększać rozmiaru pamięci systemowej bez powodu
* Naprawiono błędy występujące przy próbie skupienia się na oknie konsoli systemu dos więcej niż trzy razy. NVDA miała tendencję do całkowitego zawieszania się.

### Polecenia kluczowe

* NVDA+shift+klawiatura numeryczna6 i NVDA+shift+klawiatura numeryczna4 umożliwiają nawigację do następnego lub poprzedniego obiektu w przepływie. Oznacza to, że możesz nawigować w aplikacji, używając tylko tych dwóch, bez konieczności martwienia się o przechodzenie w górę przez rodzica lub w dół do pierwszego elementu podrzędnego podczas poruszania się po hierarchii obiektów. Na przykład w przeglądarce internetowej, takiej jak Firefox, możesz nawigować po dokumencie po obiekcie, używając tylko tych dwóch. Jeśli następny w przepływie lub poprzedni w przepływie przenosi Cię w górę i na zewnątrz obiektu lub w dół do obiektu, uporządkowane sygnały dźwiękowe wskazują kierunek.
* Możesz teraz skonfigurować ustawienia głosu bez otwierania okna dialogowego ustawień głosu, korzystając z pierścienia ustawień syntezatora. Pierścień ustawień syntezatora to grupa ustawień głosu, które możesz przełączać, naciskając control+NVDA+prawo i control+NVDA+lewo. Aby zmienić ustawienie, użyj control+NVDA+góra i control+NVDA+dół.
* Dodano komendę informującą o bieżącym zaznaczeniu w polach edycyjnych (NVDA+shift+strzałka w górę).
* Sporo poleceń NVDA, które odczytują tekst (takich jak raport, bieżąca linia itp.), może teraz przeliterować tekst, jeśli zostanie szybko naciśnięte dwa razy.
* CapsLock, wkładka numeryczna i wkładka rozszerzona mogą być używane jako modyfikujący NVDA. Ponadto, jeśli jeden z tych jest używany, dwukrotne naciśnięcie bez naciskania innych spowoduje wysłanie do systemu operacyjnego, tak jak w przypadku naciśnięcia bez uruchomionego NVDA. Aby jeden z tych był modyfikującym NVDA, zaznacz jego pole wyboru w oknie dialogowym Ustawienia klawiatury (kiedyś nazywanym oknem dialogowym echa klawiatury).

### Wsparcie aplikacyjne

* Ulepszona obsługa dokumentów Firefox3 i Thunderbird3. Czas ładowania został poprawiony prawie trzydziestokrotnie, domyślnie używany jest układ ekranu (naciśnij nvda+v, aby przełączać się między tym a brakiem układu ekranu), lista linków (dodano nvda+f7), okno dialogowe wyszukiwania (control+nvda+f) jest teraz bez uwzględniania wielkości liter, znacznie lepsza obsługa dynamicznej zawartości, możliwe jest teraz zaznaczanie i kopiowanie tekstu.
* W oknach historii programów MSN Messenger i Windows Live Messenger można teraz zaznaczać i kopiować tekst.
* Ulepszona obsługa aplikacji audacity
* Dodano obsługę kilku kontrolek edycji/tekstu w Skypie
* Ulepszona obsługa komunikatora Miranda
* Rozwiązano niektóre problemy z fokusem podczas otwierania wiadomości HTML i zwykłego tekstu w programie Outlook Express.
* Pola wiadomości grupy dyskusyjnej programu Outlook Express są teraz poprawnie oznaczone etykietami
* NVDA może teraz odczytywać adresy w polach wiadomości programu Outlook Express (do/z/cc itp.)
* NVDA powinno być teraz bardziej precyzyjne w ogłaszaniu następnej wiadomości w out look express podczas usuwania wiadomości z listy wiadomości.

### Interfejsy API i zestawy narzędzi

* Ulepszono nawigację po obiektach MSAA. Jeśli okno ma menu systemowe, pasek tytułu lub paski przewijania, możesz teraz do nich przejść.
* Dodano obsługę interfejsu API ułatwień dostępu IAccessible2. Jest to część możliwości ogłaszania większej liczby typów kontrolek, która umożliwia również NVDA dostęp do kursora w aplikacjach takich jak Firefox 3 i Thunderbird 3, umożliwiając nawigację, zaznaczanie lub edytowanie tekstu.
* Dodano wsparcie dla kontrolek edycji Scintilla (takie kontrolki można znaleźć w Notepad++ lub Tortoise SVN).
* Dodano obsługę aplikacji Java (za pośrednictwem Java Access Bridge). Może to zapewnić podstawową obsługę pakietu Open Office (jeśli jest włączona wersja języka Java) i dowolnej innej autonomicznej aplikacji Java. Pamiętaj, że aplety Java z przeglądarką internetową mogą jeszcze nie działać.

### Myszka

* Ulepszono obsługę odczytywania tego, co znajduje się pod wskaźnikiem myszy podczas jego ruchu. Jest teraz znacznie szybszy, a także ma teraz możliwość odczytu bieżącego słowa, a nie tylko bieżącego obiektu w niektórych kontrolkach, takich jak standardowe pola edycji, kontrolki Java i IAccessible2. Może to być spowodowane przez osoby niedowidzące, które chcą po prostu przeczytać określony fragment tekstu za pomocą myszy.
* Dodano nową opcję konfiguracji, która znajduje się w oknie dialogowym ustawień myszy. Odtwarzaj dźwięk, gdy mysz porusza się, po zaznaczeniu odtwarza sygnał dźwiękowy 40 ms za każdym razem, gdy mysz się porusza, przy czym jego wysokość (od 220 do 1760 Hz) reprezentuje oś y, a głośność lewy/prawy reprezentuje oś x. Dzięki temu osoba niewidoma może z grubsza zorientować się, gdzie na ekranie znajduje się mysz podczas jej poruszania. Ta funkcja zależy również od tego, czy funkcja reportObjectUnderMouse jest również włączona. Oznacza to, że jeśli szybko chcesz wyłączyć zarówno sygnały dźwiękowe, jak i ogłaszanie obiektów, po prostu naciśnij NVDA+m. Sygnały dźwiękowe są również głośniejsze lub cichsze w zależności od tego, jak jasny jest ekran w tym momencie.

### Prezentacja i interakcja z obiektem

* Ulepszono obsługę najpopularniejszych kontrolek widoku drzewa. NVDA informuje teraz o liczbie elementów znajdujących się w gałęzi, gdy ją rozwiniesz. Informuje również o poziomie podczas wchodzenia i wychodzenia z gałęzi. I ogłasza bieżący numer elementu i liczbę elementów, zgodnie z bieżącą gałęzią, a nie całym widokiem drzewa.
* Ulepszono to, co jest ogłaszane, gdy fokus zmienia się podczas poruszania się po aplikacjach lub systemie operacyjnym. Teraz zamiast po prostu słyszeć kontrolkę, na której lądujesz, słyszysz informacje o wszystkich kontrolkach, w których ta kontrolka jest umieszczona. Na przykład, jeśli wciśniesz Tab i wylądujesz na przycisku w polu grupy, pole grupy również zostanie ogłoszone.
* NVDA próbuje teraz wypowiedzieć wiadomość w wielu oknach dialogowych, tak jak się pojawiają. Jest to dokładne w większości przypadków, chociaż nadal istnieje wiele dialogów, które nie są tak dobre, jak mogłyby być.
* Dodano pole wyboru opisów obiektów raportu do okna dialogowego ustawień prezentacji obiektów. Zaawansowani użytkownicy mogą czasami chcieć odznaczyć tę opcję, aby NVDA przestało ogłaszać wiele dodatkowych opisów na poszczególnych kontrolkach, takich jak aplikacje Java.
* NVDA automatycznie odczytuje zaznaczony tekst w kontrolkach edycji, gdy fokus zostanie na nie przeniesiony. Jeśli nie ma zaznaczonego tekstu, po prostu ogłasza bieżący wiersz jak zwykle.
* NVDA jest teraz o wiele bardziej ostrożny, gdy odtwarza sygnały dźwiękowe wskazujące zmiany na pasku postępu w aplikacjach. Nie wariuje już w aplikacjach Eclipse, takich jak Lotus Notes/Symphony i Accessibility Probe.

### Interfejs

* Usunięto okno interfejsu NVDA i zastąpiono je prostym menu podręcznym NVDA.
* Okno dialogowe ustawień interfejsu użytkownika NVDA nazywa się teraz Ustawienia ogólne. Zawiera również dodatkowe ustawienie: pole kombi do ustawiania poziomu dziennika, dla którego wiadomości powinny trafiać do pliku dziennika NVDA. Zauważ, że plik dziennika NVDA nazywa się teraz nvda.log nie debug.log.
* Usunięto pole wyboru nazw grup obiektów raportu z okna dialogowego ustawień prezentacji obiektów, raportowanie nazw grup jest teraz obsługiwane inaczej.

## 0.5

* NVDA ma teraz wbudowany syntezator o nazwie eSpeak, opracowany przez Jonathana Duddington.It jest bardzo responsywny i lekki oraz obsługuje wiele różnych języków. Syntezatory Sapi mogą być nadal używane, ale eSpeak będzie używany domyślnie.
 * eSpeak nie wymaga instalacji żadnego specjalnego oprogramowania, więc może być używany z NVDA na dowolnym komputerze, na pendrive'ie USB lub w dowolnym miejscu.
 * Aby uzyskać więcej informacji na temat eSpeak lub znaleźć inne wersje, przejdź do http://espeak.sourceforge.net/.
* Naprawiono błąd polegający na tym, że niewłaściwy znak był ogłaszany po naciśnięciu delete w edytowalnych panelach Internet Explorer / Outlook Express.
* Dodano obsługę większej liczby pól edycji w Skypie.
* wirtualne są ładowane tylko wtedy, gdy fokus znajduje się na oknie, które ma zostać załadowane. Rozwiązuje to niektóre problemy, gdy okienko podglądu jest włączone w programie Outlook Express.
* Dodano argumenty wiersza poleceń do NVDA:
 * -m, --minimal: nie odtwarza dźwięków uruchamiania/wyjścia i nie pokazuje interfejsu podczas uruchamiania, jeśli jest to ustawione.
 * -q, --quit: zamyka wszystkie inne już uruchomione instancje NVDA, a następnie kończy działanie
 * -s, --stderr-file nazwa_pliku: określa, gdzie NVDA powinna umieszczać nieprzechwycone błędy i wyjątki
 * -d, --debug-file nazwa_pliku: określ, gdzie NVDA powinna umieszczać komunikaty debugowania
 * -c, --config-file: określ alternatywny plik konfiguracyjny
 * -h, -help: pokazuje komunikat pomocy z listą argumentów wiersza poleceń
* Naprawiono błąd polegający na tym, że symbole interpunkcyjne nie były tłumaczone na odpowiedni język, gdy używano języka innego niż angielski i gdy włączono mów znaki pisane.
* Dodanie plików w języku słowackim dzięki Peterowi Vagnerowi
* Dodano okno dialogowe ustawień bufora wirtualnego i okno dialogowe ustawień formatowania dokumentu od Petera Vagnera.
* Dodano francuskie tłumaczenie dzięki Michel Such
* Dodano skrypt do włączania i wyłączania sygnału dźwiękowego pasków postępu (insert+u). Napisane przez Petera Vagnera.
* Sprawiono, że więcej wiadomości w NVDA można przetłumaczyć na inne języki. Obejmuje to opisy skryptów w pomocy klawiatury.
* Dodano okno dialogowe wyszukiwania do virtualBuffers (Internet Explorer i Firefox). Naciśnięcie control+f podczas przeglądania strony powoduje wyświetlenie okna dialogowego, w którym można wpisać tekst do znalezienia. Naciśnięcie Enter spowoduje wyszukanie tego tekstu i umieszczenie kursora virtualBuffer w tym wierszu. Naciśnięcie f3 spowoduje również wyszukanie następnego wystąpienia tekstu.
* Gdy włączona jest opcja Mów wpisane znaki, powinno być teraz wymawianych więcej znaków. Technicznie rzecz biorąc, teraz można mówić znakami ascii od 32 do 255.
* Zmieniono nazwy niektórych typów kontrolek, aby były bardziej czytelne. Edytowalny tekst jest teraz edytowany, kontur jest teraz widokiem drzewa, a przycisk jest teraz przyciskiem.
* Podczas przechodzenia strzałką po elementach listy na liście lub elementach widoku drzewa w widoku drzewa typ formantu (element listy, element widoku drzewa) nie jest już odczytywany, aby przyspieszyć nawigację.
* Ma wyskakujące okienko (wskazujące, że menu ma podmenu) jest teraz wypowiadane jako podmenu.
* Tam, gdzie niektóre języki używają control i alt (lub altGR) do wprowadzenia znaku specjalnego, NVDA będzie teraz mówić tymi znakami, gdy włączone jest mówienie o wpisanych znakach.
* Rozwiązano niektóre problemy z przeglądaniem kontrolek tekstu statycznego.
* Dodano tłumaczenie na język chiński tradycyjny, dzięki Coscell Kao.
* Zmieniono strukturę ważnej części kodu NVDA, co powinno teraz naprawić wiele problemów z interfejsem użytkownika NVDA (w tym oknami dialogowymi ustawień).
* Dodano obsługę Sapi4 do NVDA. Obecnie istnieją dwa sterowniki sapi4, jeden oparty na kodzie dostarczonym przez Serotek Corporation, a drugi korzystający z interfejsu com ActiveVoice.ActiveVoice. Oba te sterowniki mają problemy, sprawdź, który z nich jest dla Ciebie najlepszy.
* Teraz, gdy próbujesz uruchomić nową kopię NVDA, podczas gdy starsza kopia jest nadal uruchomiona, spowoduje to po prostu zamknięcie nowej kopii. Rozwiązuje to poważny problem polegający na tym, że uruchamianie wielu kopii NVDA sprawia, że system jest bardzo bezużyteczny.
* Zmieniono nazwę interfejsu użytkownika NVDA z NVDA Interface na NVDA.
* Naprawiono usterkę w programie Outlook Express, która powodowała, że naciśnięcie Backspace na początku edytowalnej wiadomości powodowało błąd.
* Dodano łatkę od Rui Batisty, która dodaje skrypt do raportowania aktualnego stanu baterii w laptopach (insert+shift+b).
* Dodano sterownik syntezatora o nazwie Silence. Jest to sterownik syntezatora, który nic nie mówi, dzięki czemu NVDA pozostaje całkowicie cicha przez cały czas. Ostatecznie może to być używane razem z obsługą alfabetu Braille'a, gdy już ją mamy.
* Dodano ustawienie capitalPitchChange dla syntezatorów dzięki J.J. Meddaughowi
* Dodano poprawkę od J.J. Meddaugha, która sprawia, że przełączanie obiektów raportu pod skryptem myszy jest bardziej podobne do innych skryptów przełączających (mówiąc włącz/wyłącz, a nie zmieniając całą instrukcję).
* Dodano hiszpańskie tłumaczenie (es) dostarczone przez Juana C. buo.
* Dodano plik w języku węgierskim od Tamas Gczy.
* Dodano plik w języku portugalskim od Rui Batista.
* Zmiana głosu w oknie dialogowym ustawień głosu ustawia teraz suwaki szybkości, wysokości i głośności na nowe wartości zgodnie z syntezatorem, zamiast wymuszać ustawienie syntezatora na stare wartości. Rozwiązuje to problemy, w których syntezator, taki jak Eloquence lub Viavoice, wydaje się mówić znacznie szybciej niż wszystkie inne syntezatory.
* Naprawiono błąd, który powodował, że albo mowa się zatrzymywała, albo NVDA całkowicie się zawieszała, gdy była w oknie konsoli Dos.
* Jeśli istnieje wsparcie dla określonego języka, NVDA może teraz automatycznie wyświetlać swój interfejs i wypowiadać wiadomości w języku, na który ustawiony jest Windows. Określony język można również wybrać ręcznie w oknie dialogowym ustawień interfejsu użytkownika.
* Dodano skrypt 'toggleReportDynamicContentChanges' (wstaw+5). To przełącza, czy nowy tekst lub inne dynamiczne zmiany mają być automatycznie ogłaszane. Jak na razie działa to tylko w systemie Windows konsoli Dos.
* Dodano skrypt 'toggleCaretMovesReviewCursor' (wstaw+6). Powoduje to przełączenie, czy kursor recenzji powinien być automatycznie zmieniany po przesunięciu karetki systemowej. Jest to przydatne w oknach konsoli Dos podczas próby odczytania informacji podczas aktualizacji ekranu.
* Dodano skrypt 'toggleFocusMovesNavigatorObject' (wstaw+7). Powoduje to przełączenie, czy obiekt nawigatora ma być przenoszony na obiekt, na którym znajduje się fokus w miarę jego zmian.
* Dodano dokumentację przetłumaczoną na różne języki. Do tej pory jest francuski, hiszpański i fiński.
* Usunięto część dokumentacji deweloperskiej z binarnej dystrybucji NVDA, jest ona teraz tylko w wersji źródłowej.
* Naprawiono możliwą usterkę w komunikatorach Windows Live Messanger i MSN Messenger, która powodowała, że strzałkowanie w górę i w dół listy kontaktów powodowało błędy.
* Nowe wiadomości są teraz automatycznie wypowiadane podczas konwersacji za pomocą programu Windows Live Messenger. (na razie działa tylko w wersjach angielskich)
* Okno historii konwersacji w programie Windows Live Messenger można teraz odczytać za pomocą strzałek. (Na razie działa tylko w wersjach angielskich)
* Dodano skrypt 'passNextKeyThrough' (insert+f2). Naciśnij ten, a następny naciśnięty zostanie przekazany prosto do systemu Windows. Jest to przydatne, jeśli musisz nacisnąć określony w aplikacji, ale NVDA używa tego do czegoś innego.
* NVDA nie zawiesza się już na dłużej niż minutę podczas otwierania bardzo dużych dokumentów w MS Word.
* Naprawiono błąd polegający na tym, że wyjście z tabeli w MS Word, a następnie ponowne wprowadzenie, powodowało, że bieżące numery wierszy/kolumn nie były wypowiadane w przypadku powrotu do dokładnie tej samej komórki.
* Podczas uruchamiania NVDA z syntezatorem, który nie istnieje lub nie działa, syntezator sapi5 będzie próbował zostać załadowany zamiast niego, a jeśli sapi5 nie działa, mowa zostanie ustawiona na ciszę.
* Skrypty zwiększające i zmniejszające szybkość nie mogą już zwiększać szybkości powyżej 100 lub poniżej 0.
* Jeśli wystąpi błąd z językiem podczas wybierania go w oknie dialogowym Ustawienia interfejsu użytkownika, użytkownik zostanie poproszony o wyświetlenie komunikatu.
* NVDA teraz, czy powinien zapisać konfigurację i zrestartować się, jeśli użytkownik właśnie zmienił język w oknie dialogowym ustawień interfejsu użytkownika. NVDA musi zostać zrestartowany, aby zmiana języka w pełni weszła w życie.
* Jeśli syntezator nie może zostać załadowany, podczas wybierania go z okna dialogowego syntezatora, okno komunikatu informuje użytkownika o tym fakcie.
* Podczas ładowania syntezatora po raz pierwszy, NVDA pozwala syntezatorowi wybrać najbardziej odpowiednie parametry głosu, szybkości i wysokości, zamiast zmuszać go do ustawień domyślnych, które uważa za ok. Rozwiązuje to problem polegający na tym, że syntezatory sapi4 Eloquence i Viavoice po raz pierwszy zaczynają mówić zbyt szybko.
