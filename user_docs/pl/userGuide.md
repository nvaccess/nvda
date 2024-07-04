# Podręcznik użytkownika - NVDA NVDA_VERSION

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Skróty poleceń klawiszowych -->



## Wprowadzenie {#Introduction}

Witaj w NVDA!

NonVisual Desktop Access (NVDA) to darmowy i wolny czytnik ekranu dla systemu operacyjnego Microsoft Windows. 
Odczytując zawartość ekranu mową syntetyczną lub prezentując ją na monitorze brajlowskim, program pozwala osobom niewidomym i niedowidzącym korzystać z komputera bez ponoszenia większych kosztów niż osoby widzące. 
NVDA rozwijany jest przez organizację [NV Access](https://www.nvaccess.org/) oraz społeczność użytkowników.

### Cechy ogólne {#GeneralFeatures}

NVDA pozwala osobom niewidomym korzystać z systemu operacyjnego MS Windows, a także dużej liczby rozmaitych programów działających pod kontrolą tego systemu. 

Krótka demonstracja, ["Co to jest NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) dostępna jest na kanale Youtube organizacji NV Access.

Najważniejsze właściwości NVDA to:

* wsparcie popularnych aplikacji takich jak przeglądarki internetowe, klienty poczty, komunikatory internetowe, pakiety biurowe,
* wbudowany syntezator mowy obsługujący ponad 80 języków,
* ogłaszanie formatowania tekstu, jeśli jest dostępne, takiego jak nazwa i rozmiar czcionki, styl oraz błędy ortograficzne,
* automatyczne ogłaszanie tekstu znajdującego się pod myszką oraz opcjonalna dźwiękowa sygnalizacja jej pozycji,
* wsparcie dla wielu monitorów Brajlowskich uwzględniające możliwość automatycznego wykrywania wielu z nich, oraz wprowadzania tekstu na monitorach z klawiaturą brajlowską,
* możliwość uruchamiania z pamięci USB lub innych nośników przenośnych bez konieczności instalacji,
* łatwy w użyciu udźwiękowiony instalator,
* tłumaczenie na 54 języki,
* wsparcie dla współczesnych systemów operacyjnych Windows, zarówno 32, jak i 64 bitowych,
* możliwość dostępu do ekranu logowania w systemie oraz [innych zabezpieczonych ekranów](#SecureScreens).
* oznajmianie kontrolek i tekstu podczas używania gestów dotykowych
* wsparcie dla ogólnych interfejsów dostępności takich jak Microsoft Active Accessibility, Java Access Bridge, IAccessible2 i UI Automation
* wsparcie dla wiersza poleceń systemu Windows i aplikacji konsolowych.
* możliwość podświetlania fokusu systemowego

### Wymagania systemowe {#SystemRequirements}

* Systemy operacyjne: wsparcie wszystkich 32-bitowych i 64-bitowych wersji systemu Windows 8.1, Windows 10 i Windows 11 (w tym systemów operacyjnych dla serwerów od Windows Server 2012 R2).
  * Obie architektury AMD64 jak i ARM64 systemu Windows są wspierane.
* Co najmniej 150 MB wolnej przestrzeni dyskowej.

### Wersje językowe {#Internationalization}

Ważne jest, by ludzie z całego świata, bez względu na ojczysty język, mogli mieć równy dostęp do technologii.
Poza angielskim, NVDA został przetłumaczony na 54 języki, w tym: afrykanerski, albański, amharski, arabski, aragoński, birmański, bułgarski, chiński tradycyjny i uproszczony, chorwacki, czeski, duński, perski, fiński, francuski, galicyjski, grecki,   gruziński, hebrajski, hindi,  hiszpański (Kolumbia i Hiszpania), holenderski,  irlandzki, islandzki,  japoński, kannada, kataloński, kirgiski, koreański, litewski, macedoński, mandaryński, mongolski, nepalski, niemiecki (Niemcy i Szwajcaria), norweski, pendżabski, polski, portugalski (Brazylia i Portugalia), rosyjski, rumuński,  serbski, słowacki, słoweński, szwedzki, tajski, tamilski, turecki, ukraiński, węgierski, wietnamski i włoski.

### Obsługa syntezatora mowy {#SpeechSynthesizerSupport}

NVDA oferuje wiele wersji językowych interfejsu i daje możliwość odczytywania treści w każdym języku wspieranym przez zainstalowany w systemie syntezator mowy.

Podstawowym, dołączonym do programu, syntezatorem mowy jest darmowy wielojęzyczny syntezator [eSpeak NG](https://github.com/espeak-ng/espeak-ng), który jest wolnym oprogramowaniem.

Informacje o innych syntezatorach mowy, które obsługuje NVDA można znaleźć w rozdziale [Obsługiwane syntezatory mowy](#SupportedSpeechSynths).

### Obsługa brajla {#BrailleSupport}

Użytkownicy, którzy posiadają monitor brajlowski, mogą za pomocą NVDA odczytywać w brajlu informacje z ekranu. 
NVDA używa tłumacza brajlowskiego otwartego kodu źródłowego  [LibLouis](https://liblouis.io/) do przetwarzania tekstu na znaki brajlowskie.
Obsługiwane jest również wprowadzanie brajla z klawiatury brajlowskiej przy pomocy skrótów brajlowskich lub w formie nieskróconej.
Ponadto, NVDA domyślnie automatycznie wykrywa wiele linijek brajlowskich.
Zobacz więcej informacji na temat obsługiwanych monitorów brajlowskich w rozdziale [Obsługiwane monitory brajlowskie](#SupportedBrailleDisplays).

NVDA obsługuje kody brajla dla wielu języków, w tym brajl zwykły, skróty brajlowskie i brajl komputerowy.

### Licencja i prawa autorskie {#LicenseAndCopyright}

NVDA copyright NVDA_COPYRIGHT_YEARS autorzy NVDA.

NVDA jest dostępny pod licencją GNU General Public License (wersja 2) z dwoma specjalnymi wyjątkami.
Wyjątki są zawarte w dokumencie license w rozdziałach "Non-GPL Components in Plugins and Drivers" i "Microsoft Distributable Code". Notatka tłumacza: nazwy rozdziałów pozostały nieprzetłumaczone z powodu cytowania oryginalnego dokumentu.
NVDA także zawiera i używa komponentów które są objęte różnymi innymi bezpłatnymi i otwartoźródłowymi licencjami.
Możesz za darmo udostępniać ten program i dowolnie zmieniać go, pod warunkiem, że dołączysz do niego tę licencję oraz udostępnisz pełny kod źródłowy każdemu zainteresowanemu. 
Dotyczy to zarówno oryginalnej wersji programu, jak i jego zmienionych kopii, a także każdego innego oprogramowania, które korzysta z kodu zaczerpniętego z tego programu. 

Dokładne brzmienie licencji znajdziesz online: [Pełna treść licencji.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Dla szczegółowych informacji dotyczących wyjątków, skonsultuj się z dokumentem dostępnym w menu NVDA w podmenu "pomoc".

## NVDA szybki start {#NVDAQuickStartGuide}

Ten szybki start zawiera trzy główne rozdziały: pobieranie, podstawowe konfigurowanie, i uruchamianie NVDA.
W tych rozdziałach zawarta jest informacja o zmianie ustawień, używaniu dodatków, uczestnictwie w społeczeństwie, a także informacje o tym, jak dostać pomoc.
Informacja w tym szybkim starcie jest zebrana z innych rozdziałów podręcznika użytkownika NVDA.
Prosimy zajrzeć do kompletnego podręcznika użytkownika po więcej informacji o każdym temacie.

### Pobieranie NVDA {#GettingAndSettingUpNVDA}

Czytnik ekranu NVDA jest bezpłatny, i każdy może go używać.
Nie istnieje żaden klucz licencyjny lub droga subskrypcja którą trzeba opłacać.
NVDA jest aktualizowany średnio cztery razy rocznie.
Najnowsza wersja NVDA jest zawsze dostępna ze strony "pobierania" na stronie [NV Access](NVDA_URL).

NVDA działa ze wszystkimi ostatnimi wersjami systemu operacyjnego Microsoft Windows.
Sprawdź [Wymagania systemowe](#SystemRequirements) dla więcej szczegółów.

#### Procedura pobierania NVDA {#StepsForDownloadingNVDA}

Ta procedura wymaga wiedzy poruszania się po stronach internetowych.

* Otwórz swoją przeglądarkę internetową, (naciśnij klawisz `windows`, napisz słowo "internet" bez cudzysłówów, i naciśnij `enter`)
* Otwórz stronę pobierania NV Access (naciśnij `alt+d`, wpisz następujący adres i naciśnij `enter`): 
https://www.nvaccess.org/download 
* Aktywuj przycisk "download"
* Przeglądarka może, ale nie musi zapytać o czynność którą trzeba wykonać po pobieraniu, a potem pobieranie zostanie rozpoczęte
* W zależności od przeglądarki, plik może być uruchomiony po pobieraniu
* Jeżeli istnieje potrzeba ręcznego uruchamiania pliku, naciśnij `alt+n` aby przejść do obszaru powiadomień, a potem `alt+r` żeby uruchomić plik. W przeciwnym razie, wykonaj kroki stosowne do twojej przeglądarki.

### Konfigurowanie NVDA {#SettingUpNVDA}

Uruchomienie pobranego pliku spowoduje start tymczasowej kopii programu. 
Na tym etapie możesz zdecydować, czy chcesz zainstalować program na dysku, utworzyć jego kopię przenośną i umieścić ją np. w pamięci flash, czy kontynuować użycie wersji tymczasowej.

Po pobraniu pliku instalacyjnego, NVDA nie potrzebuje dostępu do internetu żeby go zainstalować lub uruchomić.
Jeżeli dostępne jest połączenie z internetem, istnieje możliwość periodycznego sprawdzania aktualizacji.

#### Procedura uruchamiania pobranego pliku instalacyjnego {#StepsForRunningTheDownloadLauncher}

Plik instalacyjny nosi nazwę pliku "nvda_2022.1.exe" lub podobną.
Rok i wersja  odzwierciedlają zmiany między wersjami.

1. Uruchom pobrany plik.
Podczas uruchamiania tymczasowej kopii NVDA, odtwarzany jest krótki fragment muzyczny.
Po uruchomieniu, mowa będzie aktywna podczas całego procesu.
1. Okno programu uruchamiającego NVDA otwiera się z tekstem umowy licencyjnej.
Jeżeli chcesz, Naciskaj `strzałkę w dół` aby przeczytać umowę licencyjną.
1. Naciskaj klawisz `tab` aby przejść do pola wyboru "zgadzam się", a potem naciśnij `spację` aby go wybrać.
1. Naciskaj `tab` żeby się przemieszczać pomiędzy opcjami, a potem naciśnij `enter` na opcję, którą chcesz aktywować.

Dostępne opcje to: 

* "Zainstaluj NVDA na tym komputerze": To jest główna opcja, którą wybiera większość użytkowników dla prostego używania NVDA. 
* "Utwórz kopię przenośną": ta opcja umożliwia ustawianie NVDA w jakimkolwiek folderze bez instalacji.
Ta opcja jest użyteczna na komputerze bez praw administratora, lub na USB stickach w celu noszenia ze sobą.
Kiedy ta opcja jest zaznaczona, NVDA kieruje użytkownika  w procesie tworzenia przenośnej kopii.
Główną rzecz o której NVDA powinien wiedzieć, to folder do przechowywania konfiguracji przenośnej kopii. 
* "Kontynuuj uruchamianie tymczasowej kopii": ta opcja trzyma uruchomioną tymczasową kopię.
To jest użyteczne w celu testowania funkcji w nowej wersji przed jej instalacją.
Kiedy ta opcja jest wybrana, okno programu uruchamiającego zamyka się, a tymczasowa kopia nadal działa dopóki nie zostanie zamknięta albo komputer zostanie wyłączone.
Miewaj na uwadzę, że konfiguracja nie będzie zachowana. 
* "Zrezygnuj": Ta opcja powoduje zamknięcie NVDA bez wykonywania żadnej czynności.

Jeżeli planujesz używać  NVDA na tym komputerze, zechcesz zainstalować NVDA.
Instalowanie NVDA umożliwi dodatkową funkcjonalność taką jak automatyczne uruchamianie NVDA po zalogowaniu w systemie, możliwość odczytu  ekranu logowania i [bezpiecznych ekranach](#SecureScreens).
Ta funkcjonalność jest niedostępna w przenośnych i tymczasowych kopiach.
Po więcej informacji o ograniczeniach przenośnych i tymczasowych kopii NVDA, prosimy zajrzeć do rozdziału [Ograniczenia przenośnych i tymczasowych kopii](#PortableAndTemporaryCopyRestrictions).

Procedura instalacji także umożliwia skróty w menu start i na pulpicie, a także umożliwia uruchamianie NVDA za pomocą skrótu `control+alt+d`.

#### Proces instalacji NVDA z programu uruchamiającego {#StepsForInstallingNVDAFromTheLauncher}

Te kroki prowadzą przez najbardziej ogólne opcje instalacji.
Po więcej opcji dostępnych podczas instalacji, prosimy zajrzeć do rozdziału [o opcjach instalacji](#InstallingNVDA).

1. Z programu uruchamiającego, proszę się upewnić, że pole wyboru zgody z licencją jest zaznaczone.
1. Naciskaj klawisz `Tab` i aktywuj przycisk "Zainstaluj NVDA na tym komputerze".
1. Dalej, mamy opcje używaj NVDA podczas logowania a także opcje do tworzenia kopii przenośnej.
Te opcje są domyślnie wybrane.
Jeżeli chcesz, naciśnij `tab` i `spacje` na jakiejkolwiek z tych opcji, lub pozostaw wartości domyślne.
1. Naciśnij `enter` aby kontynuować.
1. Pojawi się dialog "kontrola konta użytkownika (UAC)" w którym decydujesz "Czy chcesz, żeby ta aplikacja wykonała zmiany na tym komputerze?".
1. Naciśnij `alt+t` aby zaakceptować.
1. Pasek postępu uzupełnia się podczas instalacji NVDA.
Podczas trwania tego procesu NVDA odtwarza wzrastający wysoki dźwięk.
Ten proces jest szybki i czasem nie można go zauważyć.
1. Pojawi się okno dialogowe potwierdzające udaną instalację NVDA.
W tym komunikacie użytkownikowi jest zalecane "Naciśnij Ok aby uruchomić zainstalowaną kopię".
Naciśnij `enter` aby uruchomić zainstalowaną kopię.
1. Pojawi się okno dialogowe "Witamy w NVDA", a NVDA odczyta wiadomość powitalną.
Fokus znajduje się w liście rozwijanej "układ klawiatury".
Domyślnie, "Desktop" układ klawiatury używa klawiaturę numeryczną dla niektórych funkcji.
Jeżeli chcesz, naciśnij `strzałkę w dół` aby wybrać "Laptop" układ klawiatury aby przypisać funkcje z numerycznego bloku innym klawiszom.
1. Naciśnij `tab` aby się przenieść do opcji "Używaj klawisza `capsLock` jako klawisza modyfikatora".
`Insert` jest ustawiony jako klawisz modyfikatora domyślnie.
Naciśnij `spację` aby zaznaczyć i wybrać `capsLock` jako alternatywny klawisz modyfikatora.
Miewaj na uwadze, że układ klawiatury jest ustawiany oddzielnie od klawisza modyfikatora NVDA.
Klawisz NVDA i układ klawiatury mogą być zmienione później z poziomu ustawień klawiatury.
1. Użyj klawisza `tab` i `spacji` aby ustawić inne opcje na tym ekranie.
Te opcje regulują automatyczne uruchamianie NVDA.
1. Naciśnij `enter` aby zamknąć okno dialogowe z uruchomionym NVDA.

### Uruchamianie NVDA {#RunningNVDA}

Pełny podręcznik użytkownika zawiera wszystkie polecenia NVDA, podzielone w więcej rozdziałów dla łatwego odnajdywania.
Tabele z poleceniami także są dostępne w "szypkim wykazie skrótów klawiszowych".
Moduł "Podstawowe szkolenie z obsługi NVDA" zawiera każde polecenie szczegółowo opisane z aktywnościami krok po kroku.
"Podstawowe szkolenie z obsługi NVDA" dostępne jest w [sklepie NV Access](http://www.nvaccess.org/shop).

Tutaj znajdują się często używane polecenia.
Wszystkie polecenia są konfigurowalne, co oznacza, że są to domyślne skróty klawiszowe dla tych funkcji.

#### Klawisz modyfikatora NVDA {#NVDAModifierKey}

Domyślny klawisz modyfikatora NVDA to  klawisz `numeryczny zero`, (z wyłączonym `numLockiem`), lub klawisz `insert` w pobliżu klawiszy `delete`, `home` i `end`.
Klawisz `capsLock` można także ustawić jako klawisz modyfikatora.

#### Pomoc klawiatury {#InputHelp}

Aby dowiedzieć się, gdzie znajdują się poszczególne klawisze na klawiaturze, naciśnij `NVDA+1` żeby włączyć pomoc klawiatury.
Gdy znajdujesz się w trybie pomocy klawiatury, wykonanie jakiegokolwiek zdarzenia wejścia (takiego jak naciskanie klawisza lub wykonywanie gestu dotykowego) przeczyta akcję i przeczyta opis (jeżeli istnieje).
Polecenia nie będą wykonywane, gdy pomoc klawiatury jest aktywna. 

#### Uruchamianie i zamykanie NVDA {#StartingAndStoppingNVDA}

| Nazwa |Polecenie dla komputerów stacjonarnych |Polecenie dla komputerów przenośnych |opis|
|---|---|---|---|
|Uruchom NVDA |`control+alt+d` |`control+alt+d` |Uruchamia lub ponownie uruchamia NVDA|
|Zamknij NVDA |`NVDA+q`, potem `enter` |`NVDA+q`, potem `enter` |zamyka NVDA|
|Wstrzymuje lub wznawia mowę |`shift` |`shift` |Natychmiastowo wstrzymuje mowę. Po ponownym wciśnięciu mowa będzie wznowiona na miejscu zatrzymania|
|Zatrzymaj mowę |`control` |`control` |Natychmiastowo zatrzymuje mowę|

#### Czytanie tekstu {#ReadingText}

| Nazwa |Polecenie dla komputerów stacjonarnych |Polecenie dla komputerów przenośnych |opis|
|---|---|---|---|
|Czytaj wszystko |`NVDA+strzałka w dół` |`NVDA+a` |Zaczyna czytanie od aktualnej pozycji, przemieszczając się do przodu|
|Czytaj bieżącą linię |`NVDA+strzałka w góre` |`NVDA+l` |Czyta linię. Dwukrotnie naciśnięcie literuje linię. Naciskając trzykrotnie literuję linie fonetycznie (adam, barbara, celina, itd)|
|Czytaj zaznaczenie |`NVDA+shift+strzałka w górę` |`NVDA+shift+s` |czyta każdy zaznaczony tekst Dwukrotne naciśnięcie przeliteruje tekst, Trzykrotne naciśnięcie przeliteruje go fonetycznie.|
|Czytaj tekst w schowku |`NVDA+c` |`NVDA+c` |Czyta jakikolwiek tekst w schowku Dwukrotne naciśnięcie przeliteruje tekst, Trzykrotne naciśnięcie przeliteruje go fonetycznie.|

#### Odczyt położenia i innych informacji {#ReportingLocation}

| Nazwa |Polecenie dla komputerów stacjonarnych |Polecenie dla komputerów przenośnych |opis|
|---|---|---|---|
|Tytuł okna |`NVDA+t` |`NVDA+t` |Czyta tytuł bieżącego aktywnego okna. podwójne naciśnięcie literuje informację. Trzykrotnie naciśnięcie skopiuje informacie do schowka|
|Odczytaj fokus |`NVDA+tab` |`NVDA+tab` |Czyta aktualną kontrolkę w fokusie.  Dwukrotne naciśnięcie przeliteruje informację. Trzykrotne naciśnięcie przeliteruje ją fonetycznie.|
|Odczytaj okno |`NVDA+b` |`NVDA+b` |Czyta całe bieżące okno (użyteczne do okien dialogowych)|
|Czytaj pasek stanu |`NVDA+end` |`NVDA+shift+end` |Odczytuje pasek stanu, jeżeli NVDA go znajdzie. Dwukrotnie naciśnięcie spowoduje literowanie przeczytanej informacji. Potrójne naciśnięcie skopiuje informacje do schowka.|
|Odczytaj czas |`NVDA+f12` |`NVDA+f12` |Naciśnięcie jeden raz spowoduje odczyt aktualnego czasu, dwukrotnie naciśnięcie spowoduje odczyt aktualnej daty. Data i czas odczytywane są zgodnie z formaem określonym ustawieniach dla zegara obszaru powiadomień.|
|Odczytaj formatowanie tekstu |`NVDA+f` |`NVDA+f` |Odczytuje informacje o formatowaniu tekstu. Dwukrotne naciśnięcie spowoduje pokazanie tej informacji w oknie|
|Odczytaj lokalizacje linku |`NVDA+k` |`NVDA+k` |Gdy jest naciśnięte jeden raz, odczytuje adres URL linku pod kursorem systemowym. Gdy jest naciśnięte dwukrotnie, pokazuje w oknie w celu bardziej rzetelnego przeglądu|

#### Kontrola przeczytanej informacji przez NVDA {#ToggleWhichInformationNVDAReads}

| Nazwa |Polecenie dla komputerów stacjonarnych |Polecenie dla komputerów przenośnych |opis|
|---|---|---|---|
|Czytaj wpisane znaki |`NVDA+2` |`NVDA+2` |Gdy włączone, NVDA przeczyta wszystkie wpisane znaki na klawiaturze.|
|Czytaj pisane słowa |`NVDA+3` |`NVDA+3` |gdy włączone, NVDA odczyta każde słowo napisane na klawiaturze.|
|Czytaj klawisze poleceń |`NVDA+4` |`NVDA+4` |Gdy jest włączone, NVDA przeczyta wszystkie klawisze, nie będące znakami które zostaną wprowadzone na klawiaturze. W to są włączone kombinacje takie jak control plus oddzielna litera.|
|Włącz śledzenie myszy |`NVDA+m` |`NVDA+m` |Gdy włączone, NVDA odczyta tekst pod wskaźnikiem myszy podczas ruchu myszą. To umożliwia odnajdywanie elementów na ekranie, fizycznym poruszaniem myszą, co jest lepiej niż szukanie tych elementów nawigacją obiektową.|

#### Ustawienia syntezatora, czyli pierścień syntezatora mowy {#TheSynthSettingsRing}

| Nazwa |Polecenie dla komputerów stacjonarnych |Polecenie dla komputerów przenośnych |opis|
|---|---|---|---|
|przejdź do następnego ustawienia syntezatora |`NVDA+control+strzałka w prawo` |`NVDA+shift+control+strzałka w prawo` |przemieszcza do następnego ustawienia syntezatora, pozwalając krążyć po ustawieniach syntezatora po ostatnim ustawieniu|
|przejdź do poprzedniego ustawienia syntezatora |`NVDA+control+strzałka w lewo` |`NVDA+shift+control+strzałka w lewo` |przemieszcza do poprzedniego ustawienia syntezatora, pozwalając krążyć po ustawieniach syntezatora po ostatnim ustawieniu|
|zwiększ aktualne ustawienie syntezatora |`NVDA+control+strzałka w górę` |`NVDA+shift+control+strzałka w górę` |Zwiększa aktualne ustawienie syntezatora które ustawiasz. Na przykład zwiększa prędkość, wybiera następny głos, zwiększa głośność|
|Zwiększ aktualne ustawienie pierścienia syntezatora mowy większymi krokami |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |zwiększa wartość aktualnego ustawienia mowy na której się znajdujesz larger większymi krokami. Na przykład gdy znajdujesz się na ustawieniu głosu, przeskakiwać będziesz o każdych 20 głosów; gdy znajdujesz się na ustawieniu z suwakiem (prędkość, wysokość, itd) Ustawienie zwiększy się o dwadzieścia procent|
|Zmniejsz aktualne ustawienie syntezatora |`NVDA+control+strzałka w dół` |`NVDA+shift+control+strzałka w dół` |Zmniejsza aktualne ustawienie syntezatora które ustawiasz. Na przykład zmniejsza prędkość, wybiera poprzedni głos, zmniejsza głośność|
|Zmniejsz aktualne ustawienie mowy większymi krokami |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Zmniejsza ustawienie mowy na któym sieznajdujesz mniejszym krokiem. Na przykłąd, gdy znajdujesz sięna ustawieniu głosu, będziesz sieprzemieszczał co dwadzieścia głosów; Gdy znajdujesz się na ustawieniu podobnym od suwaka, wartości zmeini sięo dwadzieścia procent.|

Możesz także ustawić pierwszą lub ostatnią wartość aktualnego ustawienia mowy w pierścieniu ustawień mowy przypisując skrót w [oknie dialogowym zdarzeń wejścia](#InputGestures), w kategorii mowa.
To w praktyce oznacza, że gdy znajdujesz sie na ustawieniu prędkości, to umożliwi ustawienie jej na zero albo sto procent.
Gdy znajdujesz się na ustawieniu głosu, będziesz w stanie ustawić pierwszy lub ostatni głos.

#### Nawigacja po stronach internetowych {#WebNavigation}

Pełną liste skrótów szybkiej nawigacji można znaleźć w roździale [Tryb przeglądania](#BrowseMode) podręcznika użytkownika.

| Polecenie |skrót |opis|
|---|---|---|
|Nagłówek |`h` |przenosi do następnego nagłówka|
|Nagłówek poziomu 1, 2, lub 3 |`1`, `2`, `3` |przenosi do następnego nagłówka określonego poziomu|
|Pole formularza |`f` |Przenosi do następnego pola formularza (pole edycji, przycisk itd)|
|Link |`k` |przenosi do następnego linku|
|Punkt orientacyjny |`d` |Przenosi do następnego punktu orientacyjnego|
|lista |`l` |Przenosi do następnej listy|
|Tabela |`t` |Przenosi do następnej tabeli|
|Przenosi wstecz |`shift+litera` |Naciśnij `shift` i jakąkolwiek z powyższych liter aby przejść do poprzedniego elementu tego typu|
|Lista elementów |`NVDA+f7` |Listuje elementy różnych typów, takie jak linki i nagłówki|

### Ustawienia {#Preferences}

Większość funkcji NVDA mogą być włączone lub zmienione za pomocą ustawień NVDA.
Ustawienia i inne opcje dostępne są w menu programu NVDA.
Aby otworzyć menu programu NVDA, naciśnij `NVDA+n`.
Aby bezpośrednio otworzyć dialog ustawień ogólnych programu NVDA, naciśnij `NVDA+control+g`.
Wielu ekranów ustawień posiada skróty do bezpośredniego otwierania, takie jak na przykład `NVDA+control+s` do zmiany syntezatora, lub `NVDA+control+v` do zmiany innych ustawień głosu.

### Dodatki {#Addons}
Dodatki to programy, dodające nową lub zmienioną funkcjonalność do czytnika ekranu NVDA.
Dodatki są rozwijane przez społeczność NVDA oraz firmy trzecie i nie są powiązane z NV access.
Ważne jest zaufanie do dewelopera dodatku przed jego używaniem, tak jak i z innymi programami.
Prosimy zajrzeć do rozdziału [Instalowanie dodatków](#AddonStoreInstalling) aby się dowiedzieć, o sposobach weryfikacji dodatków.

Po pierwszym otwarciu NVDA add-ons store, komunikat o dodatkach zostanie wyświetlony.
Dodatki nie są sprawdzane przez NV Access  i mogą posiadać nieograniczony dostęp do informacji i danych.
Naciśnij `spację`, jeśli przeczytałeś ostrzeżenie i nie chcesz go widzieć następnym razem.
Naciśnij `tab` aby dotrzeć do przycisku "OK" a potem naciśnij `enter` w celu zaakceptowania ostrzeżenia i kontynuowania do add-on store.
Rozdział "[Dodatki i Add-ons store](#AddonsManager)" podręcznika użytkownika zawiera informacje o każdej funkcji add-on storu.

Add-on Store jest dostępne w w meni Narzędzia.
Naciśnij `NVDA+n` aby otworzyć NVDA meni, potem `n` dla narzędzi, a potem `a` dla add-on storu.
Po opwarciu Add-on storu, zostanie wyświetlona karta właściwości "otkryj dodatki", jeżeli nie ma zainstalowanych dodatków.
Gdy dodatki są zainstalowane, Add-on Store otworzy się na karcie właściwości "zainstalowane dodatki".

#### Otkrywaj dodatki {#AvailableAddons}
Gdy okno otworzy się pierwszy raz,  trzeba poczekać pare sekund, aby dodatki wczytały się.
NVDA przeczyta nazwę pierwszego dodatku po wczytaniu listy dodatków.
Dostępne dodatki są wylistowane alfabetycznie w wielokolumnowej liście.
Aby przeglądać listę i znaleźć informacje o określonym dodatku:

1. Używaj klawiszy strzałek oraz naciśnij pierwszą literę nazwy dodatku, aby się przemieszczać po liście.
1. Naciśnij jeden raz klawisz `tab` aby dotrzeć do opisu zaznaczonego dodatku.
1. Używaj [klawiszy do odczytu](#ReadingText) lub strzałek, aby przeczytać cały opis.
1. Naciśnij `tab` aby dojść do przycisku "działania", który wspośród innych działań umożliwi instalację dodatku.
1. Naciśnij `tab` aby dojść do części okna "więcej szczegółów", w którym podane są takie informacje jak wydawca, wersja i strona internetowa.
1. Aby wrócić do listy dodatków, naciśnij `alt+a`, lub `shift+tab`, dopóki nie wrócisz na listę.

#### Szukanie dodatków {#SearchingForAddons}
Możliwe jest filtrowanie dodatków w taki sam sposób, jak i ich przeglądanie.
Aby wyszukiwać dodatki, naciśnij `alt+s` aby przejść do pola "szukaj" i wpisz szukany tekst.
Pole wyszukiwania może zawierać takie informacje jak: identifikator dodatku, nazwę wyświetlaną, wydawcę, autora lub opis.
Lista się zmienia podczas wpisywania słów kluczowych.
Po zakonczeniu, naciśnij `tab` aby przejść do listy filtrowanej dodatków i przeglądaj wyniki.

#### Instalowanie dodatków {#InstallingAddons}

Aby zainstalować dodatek:

1. Gdy zaznaczyłeś dodatek, którego chcesz zainstalować, naciśnij `enter`.
1. Meni Działania otwiera się z listą działań. Pierwsze działanie to "zainstaluj".
1. Aby zainstalować dodatek, naciśnij `z` lub `Strzałkę w dół` zaznaczyć opcję "zainstaluj" i naciśnij `enter`.
1. Fokus powróci do listy dodatków a NVDA przeczyta szczegóły dodatku.
1. Informacja o "Stanie" przeczytana przez NVDA zmieni się z "dostępny" na "pobieranie".
1. Gdy pobieranie dodatku zostanie zakończone, stan zmieni się na "Pobrany, oczekujący na instalację".
1. Powtórz te kroki z każdym dodatkiem, które chcesz zainstalować.
1. Gdy zakończysz, naciśnij `tab` gdy przejdziesz do przycisku "zamknij", a potem naciśnij `enter`.
1. Proces instalacji pobranych dodatków rozpocznie się po zamknięciu Add-on store.
Podczas instalacji, pokażą się okna dialogowe, które trzeba zatwierdzić.
1. Po instalacji dodatków, pokaże się okno dialogowe, które informuje o koniecznosci ponownego uruchomienia NVDA po wykonanych zmiana i zakończonej instalacji NVDA.
1. Naciśnij `enter` aby ponownie uruchomić NVDA.

#### Zarządzanie zainstalowanymi didatkami {#ManagingInstalledAddons}
Naciśnij `control+tab` aby przemieszczać się pomiędzy kartami właściwości lub częściami Add-on Stora.
Istnieją następujące karty właściwości: "zainstalowane dodatki", "dodatki do zaktualizowania", "otkryj dodatki" i "zainstalowane niezgodne dodatki".
Każda z tych kart właściwości ułożona jest w podobny sposób: jako lista z dodatkami, panel zawierający więcej informacji o wybranym dodatku, i z możliwością wykonania działania na konkretnym dodatku.
Meni "działania umożliwia włączanie i wyłączanie dodatków, a także ich instalację.
Wyłączanie dodatków uniemożliwia ich wczytywanie przez NVDA, ale je pozostawia zainstalowane.
Aby ponownie włączyć wyłączony dodatek, trzeba nacisnąć "włącz" z meni działania.
Po włączeniu, wyłączeniu, oraz usunięciu dodatków, pokaże się komunikat o ponownym uruchomieniu po zamknięciu Add-on store.
Te zmiany zostaną wprowadzone tylko po ponownym uruchomieniu NVDA.
Miewaj na uwadzę, że klawisz `escape` w Add-on store działa w ten sam sposób jak i przycisk zamknij.

#### Aktualizowanie dodatków {#UpdatingAddons}
Gdy aktualizacja zainstalowanego dodatku zostanie wydana, ta pojawi się na karcie właściwości "dodatki do zaktualizowania".
Naciśnij `control+tab` aby się do niej dostać z jakiejkolwiek części Add-on storu.
Stan dodatku w Add-on store zostanie wyświetlony jako "aktualizacja jest dostępna".
Na liście pokaże się informacja o bieżącej i dostępnej wersji.
Naciśnij `enter` na dodatku, aby otworzyć spis działań. Wybierz "Zaktualizuj".

### Społeczność {#Community}

NVDA posiada bardzo aktywną społeczność.  
Istnieje główna [anglojęzyczna lista mailingowa](https://nvda.groups.io/g/nvda) a także   strona listująca [lokalne grupy językowe](https://github.com/nvaccess/nvda-community/wiki/Connect).
NV Access, twórcy programu NVDA, są aktywni na [Twitterze](https://twitter.com/nvaccess) i [Facebooku](https://www.facebook.com/NVAccess).
Pracownicy organizacji NV Access także prowadzą regularnego [Bloga z aktualnościami](https://www.nvaccess.org/category/in-process/).

Istnieje także [Program certyfikacji ekspertów](https://certification.nvaccess.org/).
Jest to egzamin online który można zdać aby pokazać swoje umiejętności z używania NVDA.
[Certyfikowani eksperci NVDA](https://certification.nvaccess.org/) mogą opublikować swoje informacje kontaktowe i potrzebne szczegóły biznesowe.

### Sposoby dostawania pomocy {#GettingHelp}

Aby dostać pomoc dla NVDA, naciśnij `NVDA+n` żeby otworzyć NVDA menu, potem `c` do opcji pomoc.
Z tego miejsca możesz otworzyć Podręcznik użytkownika, Szybki wykaz klawiszy poleceń, historię zmian w nowej wersji i wiele więcej.
Pierwsze trzy opcje otwierają się w przeglądarce internetowej.
Istnieje także bardziej rozszerzony materiał szkoleniowy dostępny w [Sklepie NV Access](https://www.nvaccess.org/shop).

Polecamy zacząć od "modułu podstawego szkolenia z używania NVDA".
Ten moduł obejmuje zagadnienia od początku używania do serfowania internetem i używania nawigacji obiektowej.
Moduł jest dostępny w następujących formatach:

* [Elektroniczny tekst](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), w co włączone są następujące formaty: Word DOCX, Web strona HTML, książka elektroniczna ePub i Kindle KFX.
* [Książka przeczytana przez żywego człowieka w formacie mp3](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Książka brajlowska w standarcie ujednoliconego brajla angielskiego, twarda oprawa](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) z zapewnioną przesyłką do jakiegokolwiek zakątku świata.

Inne moduły, a także obniżony cenowo [Komplet produktywności NVDA](https://www.nvaccess.org/product/nvda-productivity-bundle/), są dostępne w [Sklepie NV Access](https://www.nvaccess.org/shop/).

NV Access także sprzedaje [Wsparcie telefoniczne](https://www.nvaccess.org/product/nvda-telephone-support/), w blokach godzinnych lub jako część [NVDA kompletu produktywności](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Wsparcie telefoniczne dostępne jest w Australii i Stanach zjednoczonych.

[Listy dyskusyjne użytkowników](https://github.com/nvaccess/nvda-community/wiki/Connect) są najlepszym źródłem pomocy społeczności, ponieważ udzielają się tam [Certyfikowany eksperci NVDA](https://certification.nvaccess.org/).

Pomysły na nowe funkcje, oraz raporty o błędach można zgłaszać za pomocą [GitHuba](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
[Wytyczne dla współtwórców](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) zawierają cenne informacje o tym, jak wesprzeć społeczeństwo..

## Więcej opcji konfiguracji {#MoreSetupOptions}
### Opcje instalacji {#InstallingNVDA}

Jeśli chcesz zainstalować NVDA bezpośrednio po uruchomieniu pobranego pakietu, naciśnij przycisk "zainstaluj NVDA". 
Jeśli okno pakietu zostało zamknięte albo uruchamiasz NVDA z wersji przenośnej, kliknij polecenie Zainstaluj NVDA, dostępne w menu narzędzia w menu programu.

Okno dialogowe, które się pojawi, wyświetli pytanie o to, czy na pewno chcesz zainstalować program, oraz będzie zawierać informację, czy ta instalacja zaktualizuje istniejącą kopię NVDA.
Naciśnięcie przycisku "kontynuuj" spowoduje uruchomienie procedury instalacji. 
Na tym etapie jest do wyboru kilka opcji opisanych poniżej.
Po pomyślnej instalacji wyświetlony zostanie odpowiedni komunikat. 
Po wciśnięciu przycisku OK, nastąpi uruchomienie zainstalowanej właśnie kopii programu.

#### Ostrzeżenie o niezgodnych dodatkach {#InstallWithIncompatibleAddons}

Jeśli masz zainstalowane jakieś dodatki,  może pojawić się informacja o wyłączeniu niekompatybilnych dodatków.
Zanim możliwe będzie naciśnięcie przycisku Kontynuuj, należy zaznaczyć pole wyboru potwierdzające przeczytanie informacji o wyłączeniu tych dodatków.
Pojawi się również przycisk umożliwiający przegląd dodatków, które zostaną wyłączone.
Aby uzyskać więcej informacji, zajrzyj do [rozdziału o niezgodnych dodatkach](#incompatibleAddonsManager).
Po instalacji będzie możliwe włączenie niezgodnych dodatków na własną odpowiedzialność z poziomu [Add-on Store](#AddonsManager).

#### Używaj NVDA podczas logowania {#StartAtWindowsLogon}

Ta opcja pozwala określić, czy NVDA ma uruchamiać się na ekranie logowania do systemu Windows, zanim jeszcze wprowadzono hasło.
Dotyczy to również ekranów bezpiecznego pulpitu oraz [innych bezpiecznych ekranów](#SecureScreens).
Opcja domyślnie jest włączona dla nowych instalacji.

#### Utwórz skrót na pulpicie (Ctrl+Alt+d) {#CreateDesktopShortcut}

Ta opcja pozwala określić, czy NVDA ma utworzyć na pulpicie skrót uruchamiający program.
Jeśli tak, to ze skrótem powiązany zostanie klawisz skrótu `Ctrl+Alt+D`.

#### Skopiuj konfigurację przenośną do konta aktualnego użytkownika {#CopyPortableConfigurationToCurrentUserAccount}

Ta opcja pozwala określić, czy NVDA powinien skopiować aktualnie używaną konfigurację jako ustawienia aktualnie zalogowanego użytkownika dla wykonywanej instalacji.
Nie spowoduje to skopiowania konfiguracji dla innych użytkowników systemu ani konfiguracji używanej na ekranie logowania i [innych bezpiecznych ekranach](#SecureScreens).
Ta opcja jest dostępna tylko podczas instalacji z kopii przenośnej, nie pojawi się przy instalacji z pobranego pakietu.

### Tworzenie kopii przenośnej {#CreatingAPortableCopy}

Jeśli chcesz utworzyć kopię przenośną programu bezpośrednio z pobranego pakietu, naciśnij przycisk "Utwórz kopię przenośną". 
Jeśli okno pakietu zostało zamknięte lub korzystasz z już zainstalowanej wersji, wybierz polecenie utwórz kopię przenośną w menu narzędzia w menu NVDA.

Pojawi się okno pozwalające wybrać katalog w którym wersja przenośna ma zostać umieszczona. 
Może to być dowolna lokalizacja na dysku twardym lub na dysku zewnętrznym, pamięci przenośnej itd. 
Można tu również określić, czy program ma skopiować aktualnie używaną konfigurację zalogowanego użytkownika jako konfigurację tworzonej kopii przenośnej.
Ta opcja będzie dostępna tylko, gdy tworzona jest kopia przenośna z wersji zainstalowanej, nie pojawi się przy generowaniu kopii przenośnej z pobranego pakietu.
Wciśnięcie przycisku "Kontynuuj" utworzy wersję przenośną w podanej lokalizacji.
Po zakończeniu tworzenia kopii przenośnej, pojawi się informacja o sukcesie operacji.
Naciśnij "OK" aby zamknąć tę informację.

### Ograniczenia przenośnej i tymczasowej kopii {#PortableAndTemporaryCopyRestrictions}

Jeżeli chcesz nosić NVDA ze sobą na urządzeniu pendrive lub innym urządzeniu zapisywalnym, w takim razie trzeba stworzyć kopię przenośną.
W każdej chwili instalator może stworzyć kopię przenośną. 
Instalacja NVDA także może być wykonana z kopii przenośnej w każdej chwili.
Jednakże, jeżeli chcesz skopiować NVDA na urządzenie tylko do odczytu takie jak CD, powinieneś skopiować tylko pobrany pakiet.
W tej chwili, uruchamianie wersji przenośnej nie jest wspierane z urządzeń tylko do odczytu.

[Instalator programu NVDA](#StepsForRunningTheDownloadLauncher) może być używany jako kopia tymczasowa NVDA.
Te kopie uniemożliwiają zapisywania konfiguracji NVDA.
To także zakłada wyłączenie [Add-on Store](#AddonsManager).

Przenośne i tymczasowe kopie posiadają następujące ograniczenia:

* Brak możliwości automatycznego uruchamiania podczas i po logowaniu.
* Brak możliwości uruchamiania programów wymagających prawa administratora, do póki, oczywiście NVDA nie jest uruchomiony z tymi prawami (niezalecane).
* Brak możliwości odczytu ekranów kontroli konta użytkownika (UAC) podczas próby uruchomienia aplikacji z prawami administratora.
* Brak możliwości wsparcia ekranów dotykowych.
* Brak możliwości dostarczania funkcji takich jak tryb przeglądania i czytanie wpisanych znaków w aplikacjach Microsot store.
* Przyciszanie dźwięku nie jest wspierane.

## Używanie NVDA {#GettingStartedWithNVDA}
### Uruchomienie NVDA {#LaunchingNVDA}

W celu uruchomienia programu zainstalowanego za pomocą instalatora wybierz NVDA z menu Programy w Menu Start lub użyj skrótu Ctrl+Alt+D.
Możesz również wpisać NVDA w oknie Uruchom w menu Start i nacisnąć klawisz Enter, a program zostanie uruchomiony.
Jeżeli NVDA było uruchomione, to zostanie automatycznie zrestartowane.
Możesz również przekazać pewne [argumenty wiersza poleceń](#CommandLineOptions) które pozwalają między innymi zamknąć NVDA (-q), wyłączyć dodatki (--disable-addons), ITD.

Domyślnie, Dla zainstalowanych kopii, NVDA chowa swoją konfiguracje w folderze roaming application data folder aktualnego użytkownika (na przykłąd "`C:\Users\<user>\AppData\Roaming`").
Można to zmienić w taki sposób, że NVDA wczyta konfigurację z lokalnego folderu danych aplikacji.
Więcej w rozdziale o [Parametrach systemu](#SystemWideParameters).

Aby uruchomić wersję przenośną NVDA, przejdź do katalogu, w którym zostały wypakowane pliki, zaznacz plik  "nvda.exe" i naciśnij klawisz Enter lub dwukrotnie kliknij na nim lewym przyciskiem myszy.
Jeżeli NVDA było uruchomione to zostanie ono zamknięte przed uruchomieniem wersji przenośnej.

Po uruchomieniu NVDA usłyszysz coraz wyższe dźwięki wskazujące, że program się ładuje.
Czas uruchamiania zależy od szybkości twojego komputera oraz od prędkości nośnika, jeśli NVDA jest uruchamiane z USB lub innego wolniejszego medium.
Jeśli uruchamianie NVDA trwa długo, zostanie wygenerowany komunikat: "Ładowanie NVDA, Proszę czekać..."

Jeśli podczas uruchamiania programu nie usłyszałeś/aś powyższych komunikatów, ale dźwięk oznaczający błąd systemu Windows lub dźwięki o coraz niższej wysokości, oznacza to, iż NVDA nie działa prawidłowo i należy zgłosić powstały problem do twórców programu. 
Więcej informacji o zgłaszaniu problemów znajdziesz na stronie projektu.

#### Okno powitalne {#WelcomeDialog}

Przy pierwszym uruchomieniu, NVDA wyświetli ekran powitalny z podstawowymi informacjami o klawiszu NVDA i o menu programu.
(Więcej na ten temat znajduje się w sekcjach poniżej.)
Okienko zawiera również listę rozwijaną i 3 pola wyboru.
Lista rozwijana pozwala wybrać układ klawiatury.
Pierwsze pole wyboru pozwala ustalić, czy NVDA będzie używał klawisza CapsLock jako klawisza komend NVDA.
Drugie pozwala włączyć automatyczne uruchamianie programu po zalogowaniu do systemu i jest dostępne tylko dla zainstalowanych kopii NVDA.
Trzecie pole wyboru określa, czy to okienko dialogowe ma się pojawiać przy każdym uruchomieniu programu.

#### Statystyki diagnostyczne {#UsageStatsDialog}

Od wersji programu NVDA 2018.3, użytkownik jest pytany czy czytnik ekranu może wysyłać pewne anonimowe dane diagnostyczne  swoim twórcom, w celu jego ulepszania w przyszłości.
Gdy uruchomisz program po raz pierwszy, zostaniesz zapytany czy chcesz zezwolić fundacji NV Access na zbieranie danych.
Możesz przeczytać więcej informacji o zbieranych danych w rozdziale o ustawieniach ogólnych w [podrozdziale Zezwól NVAccessowi na zbieranie statystyk](#GeneralSettingsGatherUsageStats).
Kiedy wybierzesz jakąś opcję ustawienie zostanie zachowane, a okno dialogowe nigdy więcej się nie pojawi, chyba że dokonasz reinstalacji programu.
Jednakże, możliwe jest ręczne włączenie lub wyłączenie tej opcji w ustawieniach ogólnych w [sekcji jej poświęconej](#GeneralSettingsGatherUsageStats).

### Polecenia klawiszowe w NVDA {#AboutNVDAKeyboardCommands}
#### Klawisz komend NVDA {#TheNVDAModifierKey}

Większość poleceń programu NVDA wymaga naciśnięcia specjalnego klawisza zwanego klawiszem NVDA w połączeniu z innymi klawiszami.
Wyjątkiem są polecenia przeglądu tekstu, które przypisane są do pojedynczych klawiszy numerycznych, oraz niektóre inne polecenia.

Można skonfigurować NVDA tak, by klawisz Insert znajdujący się na klawiaturze numerycznej, klawisz Insert znajdujący się w pobliżu klawiszy strzałek, albo klawisz CapsLock - mogły zostać użyte jako specjalny klawisz poleceń NVDA.
Domyślnie obydwa klawisze Insert są ustawione jako klawisz poleceń NVDA.

Aby którykolwiek z klawiszy poleceń NVDA wykonał oryginalnie przypisaną mu funkcję (np. dla przełączenia CapsLock, gdy jest on wybrany jako klawisz NVDA), należy nacisnąć ten klawisz dwukrotnie w krótkim odstępie czasu.

#### Układy klawiatury {#KeyboardLayouts}

NVDA obecnie obsługuje dwa zestawy poleceń (zwane układami klawiatury): układ dla komputerów stacjonarnych i układ dla laptopów.
NVDA jest domyślnie skonfigurowany do korzystania z układu dla komputera stacjonarnego, ale można przełączyć się do układu klawiatury laptopa w kategorii klawiatura w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.

Układ dla komputera stacjonarnego sprawia, że intensywnie wykorzystujemy klawiaturę numeryczną (z wyłączonym klawiszem NumLock).
Mimo że większość laptopów nie ma fizycznej klawiatury numerycznej, niektóre laptopy mogą emulować ją poprzez przytrzymanie klawisza FN i naciskanie na litery i cyfry z prawej strony klawiatury (7, 8, 9, u, i, o, j, k, l itp.).
Jeśli twój laptop nie może tego zrobić albo nie pozwala wyłączyć klawisza NumLock, możesz przełączyć się na układ laptopa.

### Gesty dotykowe {#NVDATouchGestures}

Jeśli korzystasz z NVDA i posiadasz komputer z ekranem dotykowym, możesz korzystać z gestów dotykowych NVDA.
Podczas działania programu NVDA, chyba że interakcja dotykiem jest wyłączona, wszystkie gesty dotykowe są przekazywane do niego, miast do systemu operacyjnego.
Oznacza to, że gesty wykonywane normalnie nie będą działać, jeśli włączony jest NVDA.
<!-- KC:beginInclude -->
W celu przełączania obsługi gestów naciśnij NVDA+CTRL+ALT+T.
<!-- KC:endInclude -->
Możesz też przełączyć [obsługę gestów](#TouchSupportEnable) z odpowiedniej kategorii w ustawieniach programu.

#### Eksploracja ekranu {#ExploringTheScreen}

Najprostszą rzeczą, którą możesz zrobić z NVDA przy pomocy ekranu dotykowego, jest wypowiedzenie tekstu lub kontrolki w dowolnym punkcie ekranu. 
Umieść jeden palec na dowolnym miejscu ekranu, by usłyszeć dany obiekt.
Przesuwaj palec po ekranie, by usłyszeć inne kontrolki lub tekst pod nim.

#### Gesty dotykowe {#TouchGestures}

Ilekroć w tym podręczniku zostanie wymieniona komenda klawiaturowa NVDA, zostanie podany gest dotykowy, który jest jej odpowiednikiem. 
Poniżej wyjaśnienie, jak wykonywać te gesty.

##### Stuknięcia {#Taps}

Stuknij szybko w ekran jednym lub wieloma palcami.

Jednokrotne stuknięcie pojedynczym palcem jest określane po prostu jako stuknięcie.
Pojedyncze stuknięcie dwoma palcami jest określane jako stuknięcie dwoma palcami. I tak dalej.

Jeśli to samo stuknięcie jest wykonane wielokrotnie w krótkich odstępach czasu, NVDA potraktuje je jako gest wielokrotny.
Stuknięcie dwukrotne będzie podwójnym stuknięciem.
Stuknięcie 3 razy będzie potrójnym stuknięciem. I tak dalej.
Te wielokrotne gesty również uwzględniają ilość użytych palców, więc możliwe są gesty takie jak potrójne stuknięcie dwoma palcami, pojedyncze stuknięcie czterema palcami itd. 

##### Machnięcia {#Flicks}

Przesuń szybko palcem po ekranie.

Zależnie od kierunku istnieją cztery możliwe machnięcia: machnięcie w lewo, machnięcie w prawo, machnięcie do góry i machnięcie w dół.

Podobnie jak ze stuknięciami - więcej niż jeden palec może być użyty przy wykonywaniu gestu.
A zatem możliwe są gesty takie jak machnięcie do góry dwoma palcami albo machnięcie w lewo czterema palcami.

#### Tryby dotyku {#TouchModes}

Ponieważ istnieje więcej komend NVDA możliwych do wprowadzenia z klawiatury niż możliwych do wykonania gestów, NVDA oferuje różne tryby dotyku tyczące się innych podzestawów poleceń. 
Są to tryb obiektowy i tekstowy. 
Niektóre gesty wypisane w tym dokumencie mogą zatem mieć wymienione w nawiasach tryby użycia. 
Np. machnięcie w górę (w trybie tekstowym) oznacza, że aby wprowadzić to polecenie, musisz najpierw aktywować tryb tekstowy, a następnie wykonać właściwy gest.
Jeśli dana komenda nie posiada opisu trybu, oznacza to, że działa w obu trybach.

<!-- KC:beginInclude -->
Aby przełączać tryby dotyku, wykonaj stuknięcie trzema palcami.
<!-- KC:endInclude -->

#### Klawiatura ekranowa {#TouchKeyboard}

Klawiatura ekranowa jest używana do wprowadzania tekstu i komend z ekranu dotykowego.
Gdy fokus znajduje się w polu edycji, możesz przywołać klawiaturę dwukrotnie stukając w ikonę  klawiatury ekranowej na dole ekranu.
Na tabletach takich jak Microsoft Surface Pro, klawiatura ekranowa jest dostępna zawsze, gdy nie jest podłączona fizyczna klawiatura.
Aby wyłączyć klawiaturę ekranową, stuknij dwukrotnie jej ikonę lub wyjdź z pola edycji.

Gdy klawiatura ekranowa jest aktywna, aby zlokalizować jakiś znajdujący się na niej klawisz, przesuń palec do miejsca, gdzie znajduje się ta klawiatura (zwykle na dole ekranu), a następnie przesuwaj palec po klawiaturze.
Gdy znajdziesz poszukiwany klawisz, który chcesz nacisnąć, stuknij go dwukrotnie lub unieś palec, zależnie od opcji wybranej w kategorii interakcji dotykowej w oknie [Preferencji NVDA](#TouchInteraction), znajdującym się w podmenu Ustawienia w menu NVDA.

### Tryb pomocy {#InputHelpMode}

Wiele komend NVDA zostało opisanych w tym dokumencie. Najprostszym sposobem, by samodzielnie je odkrywać, jest aktywacja trybu pomocy.

Aby aktywować tryb pomocy, naciśnij NVDA+1. 
Aby go wyłączyć - ponownie naciśnij NVDA+1.
W trybie pomocy wciśnięcie kombinacji klawiszy lub wykonanie gestu dotykowego spowoduje opisanie, co dana komenda czy gest robi. 
Rzeczywista komenda nie zostanie wtedy wykonana.

### Menu NVDA {#TheNVDAMenu}

Menu NVDA pozwala na zmianę ustawień, dostęp do pomocy, zachowywanie bieżących ustawień lub przywracanie ustawień wcześniej zapisanych, umożliwia dostęp do dodatkowych narzędzi oraz pozwala wyjść z programu.

Aby się dostać do NVDA menu gdy NVDA jest uruchomiony, możesz wykonać jedną z następujących czynności:

* Naciśnij `NVDA+n` na klawiaturze.
* Wykonaj podwójne stuknięcie dwoma palcami na ekranie dotykowym.
* Wejdź do obszaru powiadomień naciskając `Windows+b`, a potem nawiguj `strzalką w dół` do ikony NVDA, i naciśnij `enter`.
* Alternatywnie, otwórz obszar powiadomień naciskając `Windows+b`, nawiguj `strzałką w dół` do ikony NVDA, i otwórz menu kontekstowe naciskając klawisz `kontekstowy` który jest ułożony z lewej strony od prawego klawisza control na większości klawiatur.
Na klawiaturach bez klawisza `kontekstowego` zamiast tego naciśnij `shift+F10`.
* Naciśnij prawy przycisk myszy na ikonie NVDA która znajduje się w obszarze powiadomień systemu Windows

Gdy menu się pojawy, możesz użyć strzałek do nawigacji po nim, i klawisza `enter` aby aktywować element.

### Podstawowe polecenia NVDA {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Działanie |Skrót desktopa |Skrót laptopa |Gest dotykowy |Opis|
|---|---|---|---|---|
|Uruchamia lub restartuje NVDA |Control+alt+d |Control+alt+d |brak |uruchamia lub restartuje NVDA przy pomocy skrótu utworzonego na pulpicie, jeżeli opcja ta została włączona podczas instalacji. Skrót ten jest kontrolowany przez system a nie przez NVDA, czyli nie jest możliwe przemapowanie go w oknie "zdarzenia wejścia".|
|Zatrzymuje mowę |Ctrl |Ctrl |Stuknięcie dwoma palcami |Natychmiast przestaje czytać|
|Pauza mowy |Shift |Shift |Brak |Natychmiast zatrzymuje mowę. Naciskając ponownie, będzie mówić od momentu, w którym zostało przerwane (jeśli wstrzymywanie jest obsługiwane przez syntezator)|
|Menu NVDA |NVDA+n |NVDA+N |Podwójne stuknięcie dwoma palcami |Pojawia się menu NVDA, aby umożliwić dostęp do ustawień, narzędzi, pomocy itp.|
|Przełączanie trybu pomocy |NVDA+1 |NVDA+1|Brak |Naciśnięcie dowolnego klawisza w tym trybie zostanie odczytany klawisz i opis wszelkich poleceń NVDA z nim związanych|
|Zakończ NVDA |NVDA+q |NVDA+q |Brak |Kończy działanie NVDA|
|Przepuść następny klawisz |NVDA+F2 |NVDA+F2 |Brak |Jednorazowo przepuszcza następny naciśnięty klawisz wprost do systemu bez przetwarzania go w NVDA. Nawet jeżeli przepuszczony klawisz posiada w NVDA swoją funkcję, nie zostanie ona wykonana.|
|Włącz/Wyłącz tryb uśpienia dla aktywnej aplikacji |NVDA+Shift+S |NVDA+Shift+Z |Brak |Ustawienie trybu uśpienia dla konkretnej aplikacji sprawia, że NVDA przestaje mówić w jej oknie, nie reaguje na wciskane skróty klawiszowe oraz przestaje wyświetlać tekst na monitorze brajlowskim. Może być to użyteczne w przypadku programów posiadających wbudowane funkcje odczytu interfejsu. Aby wyłączyć tryb uśpienia, w oknie takiej aplikacji należy wcisnąć skrót ponownie.|

<!-- KC:endInclude -->

### Odczyt informacji systemowych {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Działanie |Skrót |Opis|
|---|---|---|
|Odczytaj aktualny czas |NVDA+F12 |Podaje aktualny czas na zegarze systemowym. Podwójne wciśnięcie odczyta aktualną datę.|
|Odczytaj stan baterii |NVDA+Shift+B |Podaje status baterii oraz w procentach poziom energii i pozostały czas pracy akumulatora.|
|Odczytaj tekst w schowku |NVDA+C |Czyta tekst znajdujący się aktualnie w schowku.|

<!-- KC:endInclude -->

### Tryby mowy {#SpeechModes}

Tryby mowy regulują w jaki sposób treść na ekranie, odpowiedzi na polecenia, i inne wyjście  jest wymawiane za pomocą NVDA.
Domyślny tryb to "mowa", która powoduje wymowę w sytuacjach, oczekiwanych dla czytnika ekranu.
Jednakże, w niektórych przypadkach, lub podczas uruchamiania niektórych programów, Niektóe z tych trybów mogą być użyteczne.

Cztery dostępne tryby to:

* Mowa (domyślny): NVDA będzie mówiłą nz podczas każdej zmiany na ekranie, powiadomienia, i działania takie jak przemieszczanie fokusu, lub wywoływanie poleceń.
* Naa żądanie: NVDA będzie mówiła tylko w przypadkach użycia poleceń z funkcją odczytu (na przykłąd odczyt nazwy okna); ale nie będzie mówiła podczas przemieszczania fokusu lub kursora przeglądu.
* wyłączone: NVDA nie będzie wymawiała nic, jednakże, w odróżnieniu od trybu uśpienia, NVDA będzie cicho reagować na polecenia.
* Dźwięki: NVDA zamieni mowę krótkimi sygnałami dźwiękowymi.

Tryb dźwięki może być korzystny podczas dostawania dużej ilości tekstu w terminalu, ale cie nie interesuje, co jest napisane, ale że się przewijalub w innych przypadkach, gdy ważne jest tylko wyjście, a nie treść.

Tryb na żadanie może być użyteczny gdy nie potrzebujesz stałą informacje zwrotną o tym, co się dzieje na ekranie lub na komputerze, ale potrzebujesz sprawdzić coś za pomocą poleceń odczytu, itd.
Na przykład, podczas nagrywania dźwięku, podczas używania lupy, podczas spotkania lub dzwonku, lub jako alternatywa trybu dźwięki.

Istnieje polecenie dla przełączania trybu mowy:
<!-- KC:beginInclude -->

| Nazwa |skrót |Opis|
|---|---|---|
|Przełączaj się między trybami mowy |`NVDA+s` |Przełącza się między trybami mowy.|

<!-- KC:endInclude -->

Jeżeli potrzebujesz przełączać się między ograniczoną ilością trybów mowy, sprawdź [Tryby dostępne podczas przełączania trybów mowy](#SpeechModesDisabling) żeby wyłączyć niepotrzebne tryby.

## Nawigacja z NVDA {#NavigatingWithNVDA}

NVDA pozwala eksplorować i nawigować w systemie na kilka sposobów, uwzględniających normalną interakcję i przeglądanie.

### Obiekty {#Objects}

Każda aplikacja i sam system operacyjny składa się z wielu obiektów.
Obiekt to pojedynczy element, taki jak fragment tekstu, przycisk, pole wyboru, suwak, lista lub pole edycji.

### Nawigacja fokusem {#SystemFocus}

Fokus jest to [obiekt](#Objects), który otrzymuje informację o klawiszach naciskanych na klawiaturze.
Jeśli np. wpisujesz tekst do pola edycji, to pole edycji posiada w tej chwili fokus.

Najczęściej używaną metodą nawigacji wśród okien i formularzy w systemie Windows jest nawigacja przy użyciu fokusu. Gdy naciskasz Tab, by przejść od jednej kontrolki do następnej, Shift+Tab by przejść do poprzedniej kontrolki, Alt by dostać się do menu programu czy też Alt+Tab by przełączać się między działającymi aplikacjami, zmienia się położenie fokusu.
Za każdym razem, gdy wykonujesz te czynności, NVDA będzie informować cię o obiekcie, który aktualnie posiada fokus, podając jego nazwę, typ, zawartość, stan, opis, skrót klawiaturowy i informacje o położeniu.
Podczas gdy  [podświetlacz fokusu](#VisionFocusHighlight) jest włączony, pozycja kursora systemowego jest również pokazywana wizualnie.

Przydatne skróty klawiszowe do nawigacji za pomocą fokusa:
<!-- KC:beginInclude -->

| Działanie |Skrót Desktopa |Skrót laptopa |Opis|
|---|---|---|---|
|Odczytuje aktualny fokus |NVDA+Tab |NVDA+Tab |Odczytuje obiekt posiadający aktualnie fokus. Dwukrotne naciśnięcie literuje informacje|
|Odczytuje tytuł okna |NVDA+t |NVDA+t |Odczytuje tytuł aktualnej aplikacji lub okna. Dwukrotne naciśnięcie literuje tytuł. Trzykrotne naciśnięcie kopiuje tytuł do schowka.|
|Odczytuje aktywne okno |NVDA+b |NVDA+b |Odczytuje zawartość obiektu na pierwszym planie (aktualnie aktywnego okna). Funkcja przydatna zwłaszcza w przypadku okna dialogowego lub komunikatu, którego pojawienie się nie zostało zauważone.|
|Odczytaj pasek stanu |NVDA+End |NVDA+Shift+End |Odczytuje pasek stanu jeśli go znajdzie. Dwukrotne naciśnięcie przeliteruje informację. Trzykrotne naciśnięcie kopiuje ją do schowka.|
|Odczytaj skrót klawiszowy |`shift+numeryczny2` |`NVDA+control+shift+.` |Odczytuje skrót klawiszowy (akcelerator) aktywnego obiektu|

<!-- KC:endInclude -->

### Nawigacja kursorem systemowym {#SystemCaret}

Gdy [obiekt](#Objects), który umożliwia nawigację i/lub edycję tekstu, otrzymuje [fokus](#SystemFocus), możesz przemieszczać się po tekście, używając kursora systemowego, nazywanego także kursorem edycji.

Gdy fokus znajduje się na obiekcie, który posiada kursor systemowy, możesz używać klawiszy strzałek, Page up, Page down, Home, End, etc. do przemieszczania się po tekście.
Możesz również zmieniać tekst, jeśli kontrolka umożliwia edycję.
NVDA będzie czytał, gdy przemieszczasz się po znakach słowach i liniach, będzie również ogłaszał zmiany w zaznaczeniu tekstu.

NVDA wykorzystuje następujące klawisze poleceń do nawigacji kursorem klawiatury:
<!-- KC:beginInclude -->

| Działanie |Skrót desktopa |Skrót laptopa |Opis|
|---|---|---|---|
|Czyta wszystko |NVDA+Strzałka w dół |NVDA+a |Odczytuje od bieżącej pozycji kursora do końca tekstu, przesuwając kursor podczas czytania.|
|Odczytuje aktualną linię |NVDA+Strzałka w górę |NVDA+l |Odczytuje aktualną linię w miejscu kursora. Dwukrotne naciśnięcie literuje aktualną linię. Trzykrotne naciśnięcie literuje linię przy użyciu opisów znaków.|
|Odczytuje aktualne zaznaczenie |NVDA+Shift+Strzałka w górę |NVDA+Shift+S |Odczytuje cały aktualnie zaznaczony tekst|
|Odczytaj formatowanie |NVDA+f |NVDA+f |Odczytuje formatowanie tekstu pod kursorem. Dwukrotne wciśnięcie skrótu pokazuje informacje w trybie przeglądania.|
|Odczytaj cel linku |`NVDA+k` |`NVDA+k` |Naciśnięte jednokrotnie, wymawia adres na który prowadzi link pod kursorem Dwukrotne naciśnięcie pokazuje go w oknie z komunikatem do bliższego zapoznania się|
|Odczytaj położenie kursora |NVDA+numpadDelete |NVDA+delete |Odczytuje informacje o położeniu obiektu oraz tekstu pod kursorem systemowym. Na przykłąd, może to włączać procent odczytanego dokumentu, dystans krawędzi strony lub dokładną pozycje na ekranie. Po dwukrotnym naciśnięciu, można usłyszeć więcej szczegułów.|
|Następne zdanie |Alt+Strzałka w dół |Alt+Strzałka w dół |Przenosi kursor do następnego zdania i odczytuje je (obsługiwane tylko w Microsoft Word i Outlook).|
|Poprzednie zdanie |Alt+Strzałka w górę |Alt+Strzałka w górę |Przenosi kursor do poprzedniego zdania i odczytuje je (obsługiwane tylko w Microsoft Word i Outlook).|

Do poruszania się w strukturze tabel służą następujące klawisze poleceń:

| Działanie |Skrót |Opis|
|---|---|---|
|Przejdź do poprzedniej kolumny |Ctrl+Alt+Strzałka w lewo |Przenosi kursor do poprzedniej kolumny w tej samej linii|
|Przejdź do następnej kolumny |Ctrl+Alt+Strzałka w prawo |Przenosi kursor do następnej kolumny w tej samej linii|
|Przejdź do poprzedniej linii |Ctrl+Alt+Strzałka w górę |Przenosi kursor do linii poprzedniej|
|Przejdź do następnej linii |Ctrl+Alt+Strzałka w dół |Przenosi do następnej linii.|
|Przejdź do pierwszej kolumny |control+alt+home |Przenosi kursor do pierwszej kolumny (pozostając w tym samym wierszu)|
|Przejdź do ostatniej kolumny |control+alt+end |Przenosi kursor do ostatniej kolumny (pozostajac w tym samym wierszu)|
|Przejdź do pierwszego wiersza |control+alt+pageUp |Przenosi kursor do pierwszego wiersza (pozostając w tej samej kolumnie)|
|Przejdź do ostatniego wiersza |control+alt+pageDown |Przenosi kursor do ostatniego wiersza (zostając w tej samej kolumnie)|
|Czytaj wszystko w kolumnie |`NVDA+control+alt+strzałka w dół` |Czyta kolumnę wertykalnie od bieżącej komórki do ostatniej komurki w kolumnie.|
|Czytaj wszystko w wierszu |`NVDA+control+alt+strzałka w prawo` |Czyta wiersz horyzontalnie od bieżącej komórki do ostatniej komórki w wierszu.|
|Czytaj całą kolumnę |`NVDA+control+alt+strzałka w górę` |Czyta bieżącą kolumnę wertykalnie od początku do końca bez poruszania kursoru systemowego.|
|Czytaj cały wiersz |`NVDA+control+alt+strzałka w lewo` |Czyta aktualny wiersz horyzontalnie od lewej do prawej strony bez konieczności przemieszczania kursoru systemowego.|

<!-- KC:endInclude -->

### Nawigacja w hierarchii obiektów {#ObjectNavigation}

Przez większość czasu będziesz pracować z aplikacjami, używając komend przenoszących [fokus](#SystemFocus) i [kursor systemowy](#SystemCaret).
Czasem jednak możesz chcieć eksplorować aktualną aplikację lub system operacyjny bez przemieszczania fokusa lub kursora.
Może się też zdarzyć konieczność pracy z  [obiektami](#Objects), do których nie można uzyskać dostępu przy użyciu klawiatury.
W takich przypadkach, możesz posłużyć się nawigacją w hierarchii obiektów.

Nawigacja w hierarchii obiektów pozwala ci przemieszczać się pomiędzy pojedynczymi [obiektami](#Objects) i uzyskiwać o nich informacje.
Gdy przejdziesz do obiektu, NVDA ogłosi go podobnie jak ogłasza fokus.
Aby obejrzeć tekst w układzie takim, jak jest on rozmieszczony na ekranie, możesz zamiast tego użyć [trybu przeglądania ekranu](#ScreenReview).

Obiekty w systemie są uporządkowane hierarchicznie.
Oznacza to, że pewne obiekty zawierają inne obiekty i musisz wejść do nich, aby obejrzeć zawartość.
Dla przykładu: lista zawiera elementy listy, więc musisz wejść do listy, aby uzyskać dostęp do jej elementów.
Jeśli znajdujesz się na elemencie listy, przejście do poprzedniego i następnego będzie przemieszczać pomiędzy elementami tej listy.
Przejście do obiektu nadrzędnego - spowoduje powrót do obiektu listy.
Możesz wówczas przejść poza tę listę, aby obejrzeć inne obiekty.
Podobnie: pasek narzędzi zawiera kontrolki, więc musisz wejść do tego paska, aby uzyskać dostęp do znajdujących się wewnątrz niego kontrolek.

Jeżeli chcesz przemieszczać się po każdym obiekcie w systemie, Możesz używać poleceń do przemieszczania się po poprzednim/następnym obiekcie w widoku spłaszczonym.
Na przykład, jeżeli przeniesieś się do następnego obiektu w tym widoku, a aktualny obiekt zawiera inne obiekty, NVDA przeniesie się do pierwszego obiektu, który go zawiera.
W przeciwnym razie, jeżeli aktualny obiekt nie zawiera podrzędnych obiektów, NVDA przeniesie się do następnego obiektu na bieżącym poziomie hierarchii.
Jeżeli nie ma takiego następnego obiektu, NVDA spróbuje znaleźć następny obiekt w hierarchii na podstawie obiektów podrzędnych, do póki nie będzie żadnych następnych obiektów.
Te same reguły stosują się do przemieszczania się wstecz w hierarchii.

Obiekt aktualnie przeglądany, jest nazywany obiektem nawigatora.
Gdy dotrzesz do obiektu, możesz przejrzeć jego treść, używając [poleceń przeglądania tekstu,](#ReviewingText) gdy znajdujesz się w [trybie przeglądania obiektu](#ObjectReview).
Podczas gdy [podświetlacz fokusu](#VisionFocusHighlight) jest włączony, aktualna pozycja obiektu nawigatora jest również pokazywana wizualnie.
Domyślnie obiekt nawigatora podąża za fokusem, ale to zachowanie można włączać i wyłączać.

Uwaga: brajl śledzący obiekt nawigatora może być skonfigurowany za pomocą opcji  [Przywiązanie brajla](#BrailleTether).

Poniżej znajdują się skróty klawiszowe do nawigacji w hierarchii obiektów:

<!-- KC:beginInclude -->

| Działanie |Skrót desktopa |Skrót laptopa |Gest dotykowy |Opis|
|---|---|---|---|---|
|Odczytuje aktualny obiekt |NVDA+Numeryczne 5 |NVDA+Shift+O |Brak |Odczytuje aktualny obiekt w hierarchii nawigacji. Dwukrotne naciśnięcie literuje informację, trzykrotne kopiuje nazwę obiektu wraz z zawartością do schowka.|
|Przechodzi do obiektu nadrzędnego |NVDA+Numeryczne 8 |NVDA+Shift+Strzałka w górę |Machnięcie w górę (tryb obiektowy) |Przechodzi do obiektu nadrzędnego, czyli zawierającego aktualny obiekt nawigatora.|
|Przechodzi do poprzedniego obiektu |NVDA+Numeryczne 4 |NVDA+Shift+Strzałka w lewo |brak |Przechodzi do poprzedniego obiektu znajdującego się na tym samym poziomie.|
|Przechodzi do poprzedniego obiektu w wydoku spłaszczonym |NVDA+numeryczny9 |NVDA+shift+[ |machnięcie w lewo (tryb obiektowy) |Przenosi do poprzedniego obiektu w hierarchii za pomocą widoku spłaszczonego|
|Przechodzi do następnego obiektu |NVDA+Numeryczne 6 |NVDA+Shift+Strzałka w prawo |brak |Przechodzi do następnego obiektu znajdującego się na tym samym poziomie.|
|Przechodzi do następnego obiektu w wydoku spłaszczonym |NVDA+numeryczny3 |NVDA+shift+] |Machnięcie w prawo (tryb obiektowy) |Przenosi do następnego obiektu w hierarchii za pomocą widoku spłaszczonego|
|Przechodzi do pierwszego obiektu podrzędnego |NVDA+Numeryczne 2 |NVDA+Shift+Strzałka w dół |Machnięcie w dół (tryb obiektowy) |Przechodzi do pierwszego obiektu zawieranego przez aktualny obiekt nawigatora.|
|Przechodzi do fokusu |NVDA+Numeryczny minus |NVDA+Backspace |Brak |Przechodzi do obiektu, który aktualnie posiada fokus, oraz umieszcza kursor przeglądu na pozycji kursora systemu|
|Aktywuje aktualny obiekt |NVDA+Numeryczny enter |NVDA+Enter |Podwójne stuknięcie |Aktywuje bieżący obiekt (podobnie jak kliknięcie myszą lub naciśnięcie klawisza spacji, gdy ma fokus)|
|Przenosi fokus lub kursor na aktualną pozycję przeglądania |NVDA+Shift+Numeryczny minus |NVDA+Shift+Backspace |Brak |Naciśnięty raz przenosi fokus do aktualnego obiektu nawigatora, naciśnięty dwukrotnie przenosi kursor systemowy do aktualnej pozycji kursora przeglądania|
|Odczytuje położenie kursora przeglądu |NVDA+shift+Numeryczne delete |NVDA+shift+delete |brak |Zgłasza położenie tekstu lub obiektu pod kursorem przeglądu. Może to być wyrażone w procentach w obrębie dokumentu, jako odległość od krawędzi strony lub jako dokładna pozycja na ekranie. Dwukrotne naciśnięcie odczyta dalsze informacje.|
|Przenieś kursor przeglądu do paska stanu |brak |brak |brak |Odczytuje pasek stanu, jeżeli NVDA go znajdzie. Objekt nawigatora będzie przeniesiony do tej lokalizacji.|

<!-- KC:endInclude -->

UWAGA: Aby skróty na klawiaturze numerycznej działały poprawnie, należy wyłączyć klawisz NumLock.

### Przegląd tekstu w aktualnym obiekcie {#ReviewingText}

NVDA pozwala odczytywać treść [ekranu](#ScreenReview), aktualnego [dokumentu](#DocumentReview) lub aktualnego [obiektu](#ObjectReview) znakami, słowami lub liniami.
Funkcja ta jest szczególnie przydatna np. w przypadku aplikacji konsolowych, gdzie nie ma [kursora systemowego](#SystemCaret) lub kursor systemowy ma tylko ograniczone możliwości działania.
Możesz też użyć jej do przeglądania długiego komunikatu w okienku powiadomienia.

Przesuwając kursor przeglądania, nie zmieniasz położenia kursora systemowego, więc możesz przeglądać tekst, nie gubiąc aktualnej pozycji w edytowanym tekście.
Jeśli jednak kursor systemowy zostanie przesunięty, kursor przeglądu domyślnie podąża za nim.
To domyślne zachowanie można wyłączyć.

Uwaga: brajl śledzący za kursorem przeglądu może być skonfigurowany za pomocą opcji [przywiązanie brajla](#BrailleTether).

Do przeglądania tekstu są dostępne następujące polecenia:
<!-- KC:beginInclude -->

| Działanie |Skrót desktopa |Skrót laptopa |Gest dotykowy |Opis|
|---|---|---|---|---|
|Przenosi punkt przeglądu do pierwszej linii |Shift+Numeryczne 7 |NVDA+Ctrl+Home |Brak |Przenosi punkt przeglądu do pierwszej linii w aktualnym obiekcie|
|Przechodzi do poprzedniej linii w przeglądzie |Numeryczne 7 |NVDA+Strzałka w górę |Machnięcie w górę (tryb tekstowy) |Przenosi punkt przeglądu do poprzedniej linii.|
|Odczytuje linię w przeglądzie |Numeryczne 8 |NVDA+Shift+Kropka |Brak |Odczytuje linię, w której jest obecnie punkt przeglądu. Dwukrotne naciśnięcie literuje ją, trzykrotne literuje fonetycznie.|
|Przechodzi do następnej linii w przeglądzie |Numeryczne 9 |NVDA+Strzałka w dół |Machnięcie w dół (tryb tekstowy) |Przenosi punkt przeglądu do następnej linii.|
|Przechodzi do ostatniej linii w przeglądzie |Shift+Numeryczne 9 |NVDA+Ctrl+End |Brak |Przenosi punkt przeglądu do ostatniej linii w aktualnym obiekcie.|
|Przechodzi do poprzedniego wyrazu w przeglądzie |Numeryczne 4 |NVDA+Ctrl+Strzałka w lewo |Machnięcie dwoma palcami w lewo (tryb tekstowy) |Przenosi punkt przeglądu do poprzedniego wyrazu w tekście.|
|Odczytuje aktualny wyraz w przeglądzie |Numeryczne 5 |NVDA+Ctrl+kropka |Brak |Odczytuje aktualny wyraz, na którym jest umieszczony punkt przeglądu. Dwukrotne naciśnięcie literuje wyraz, trzykrotne literuje fonetycznie.|
|Przechodzi do następnego wyrazu w przeglądzie |Numeryczne 6 |NVDA+Ctrl+Strzałka w prawo |Machnięcie dwoma palcami w prawo |Przenosi punkt przeglądu do następnego wyrazu w tekście.|
|Przechodzi na początek wiersza w przeglądzie |Shift+Numeryczne 1 |NVDA+Home |Brak |Przenosi punkt przeglądu na początek aktualnej linii w tekście.|
|Przechodzi do poprzedniego znaku w przeglądzie |Numeryczne 1 |NVDA+lewo |Machnięcie jednym palcem w lewo (tryb tekstowy) |Przenosi kursor przeglądu do poprzedniego znaku aktualnej linii w tekście|
|Odczytuje aktualny znak w przeglądzie |Numeryczne 2 |NVDA+kropka |Brak |Odczytuje aktualny znak w punkcie przeglądu. Dwukrotne wciśnięcie literuje znak. Trzykrotne naciśnięcie podaje wartość kodu ASCII dziesiętnie i szesnastkowo.|
|Przechodzi do następnego znaku w przeglądzie |Numeryczne 3 |NVDA+prawo |Machnięcie jednym palcem w prawo (tryb tekstowy) |Przenosi punkt przeglądu do następnego znaku aktualnej linii.|
|Przechodzi na koniec linii w przeglądzie |Shift+Numeryczne 3 |NVDA+End |Brak |Przenosi punkt przeglądu na koniec aktualnej linii.|
|przechodzi do poprzedniej strony w przeglądzie |`NVDA+pageUp` |`NVDA+shift+pageUp` |brak |Przenosi kursor przeglądu do poprzedniej strony tekstu, jeżeli wspierane przez aplikację|
|przechodzi do następnej strony w przeglądzie |`NVDA+pageDown` |`NVDA+shift+pageDown` |brak |Przenosi kursor przeglądu do następnej strony tekstu, jeżeli jest wspierane przez aplikację|
|Odczytaj wszystko z przeglądu |Numeryczny plus |NVDA+Shift+A |Machnięcie trzema palcami w dół (tryb tekstowy) |Odczytuje od punktu przeglądu do końca tekstu.|
|Zaznacz i skopiuj od kursora przeglądu |NVDA+F9 |NVDA+F9 |Brak |Rozpoczyna proces zaznacz i kopiuj na aktualnej pozycji kursora przeglądu. Akcja nie jest wykonana do momentu wskazania NVDA miejsca końca zakresu tekstu|
|Zaznacz i kopiuj do kursora przeglądu |NVDA+F10 |NVDA+F10 |Brak |Po jednokrotnym naciśnięciu, tekst jest zaznaczany od pozycji poprzednio ustawionej znacznikiem początku do aktualnej pozycji kursora przeglądu włącznie. Po naciśnięciu tego klawisza po raz drugi, tekst zostanie skopiowany do schowka systemowego|
|Przenieś kursor do początku zaznaczenia| NVDA+shift+f9 |NVDA+shift+f9 |none |Przenosi kursor do początku zaznaczenia|
|Odczytaj formatowanie tekstu |NVDA+shift+f |NVDA+shift+f |brak |Odczytuje formatowanie tekstu w pozycji kursora przeglądu. Podwójne wciśnięcie skrótu pokazuje informacje w trybie przeglądania.|
|Zgłoś zamiennik aktualnego symbolu |Brak |Brak |Brak |Wypowiada symbol na pozycji kursora przeglądu. Naciśnięty dwukrotnie, pokazuje w trybie czytania symbol i tekst użyty do jego wypowiedzenia.|

<!-- KC:endInclude -->

UWAGA: Aby skróty na klawiaturze numerycznej działały poprawnie, należy wyłączyć klawisz Num Lock.

Aby ułatwić zapamiętanie tych poleceń w układzie klawiatury dla desktopa, zwróć uwagę, że przegląd podstawowych poleceń tekstowych zorganizowany jest w tabeli trzy kolumny na trzy linie od góry do dołu jest wiersz, słowo, znak, oraz od lewej do prawej poprzedni, aktualny i następny.
Układ został przedstawiony w tabeli poniżej:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Poprzednia linia |Aktualna linia |Następna linia|
|Poprzednie słowo |Aktualne słowo |Następne słowo|
|Poprzedni znak |Aktualny znak |Następny znak|

### Tryby przeglądania {#ReviewModes}

[Polecenia przeglądania tekstu](#ReviewingText) pozwalają przeglądać treść wewnątrz aktualnego obiektu nawigatora, aktualnego dokumentu lub ekranu, zależnie od wybranego trybu przeglądania.

Poniższe komendy przełączają między trybami przeglądania:
<!-- KC:beginInclude -->

| Działanie |Skrót desktopa |Skrót laptopa |Gest dotykowy |Opis|
|---|---|---|---|---|
|Przełącz do następnego trybu przeglądania |NVDA+Numeryczne 7 |NVDA+Page up |Machnięcie dwoma palcami w górę |Przełącza do następnego dostępnego trybu przeglądania|
|Przełącz do poprzedniego trybu przeglądania |NVDA+Numeryczne 1 |NVDA+Page down |Machnięcie dwoma palcami w dół |Przełącza do poprzedniego dostępnego trybu przeglądania|

<!-- KC:endInclude -->

#### Przeglądanie obiektu {#ObjectReview}

W trybie przeglądania obiektu, możesz przeglądać tylko treść aktualnego [obiektu nawigatora](#ObjectNavigation).
Dla obiektów typu pole edycji lub innych kontrolek tekstowych będzie to na ogół tylko tekst danej kontrolki.
Dla innych obiektów może to być nazwa i/lub wartość.

#### Przeglądanie dokumentu {#DocumentReview}

Gdy [obiekt nawigatora](#ObjectNavigation) jest w dokumencie prezentowanym w trybie czytania (np. strona www) lub innym złożonym dokumencie (np. dokument Lotus Symphony), możliwe jest przejście do trybu przeglądania dokumentu.
Ten tryb pozwala na przeglądanie zawartości całego dokumentu.

Po przejściu z trybu przeglądania obiektu do przeglądania dokumentu, punkt przeglądu jest umieszczony w dokumencie na pozycji obiektu nawigatora.
Podczas przechodzenia po dokumencie przy użyciu poleceń przeglądania, obiekt nawigatora automatycznie podąża do aktualnego obiektu w punkcie przeglądania.

Proszę zwrócić uwagę, że NVDA będzie automatycznie przełączał się w tryb przeglądania dokumentu z trybu przeglądania obiektu, gdy przechodzimy między dokumentami udostępnianymi w trybie czytania.

#### Przeglądanie ekranu {#ScreenReview}

Tryb przeglądania ekranu pozwala oglądać rozmieszczenie tekstu w oknie aplikacji analogiczne do tego, jak jest on rozmieszczony wizualnie.
Jest to działanie podobne do przeglądania ekranu lub funkcjonalności myszy dostępnej w wielu innych czytnikach ekranu.

Po przejściu do trybu przeglądania ekranu, punkt przeglądu jest umieszczany na pozycji aktualnego [obiektu nawigatora](#ObjectNavigation).
Podczas przechodzenia po ekranie poleceniami przeglądu, obiekt nawigatora automatycznie podąża do obiektu znajdującego się na pozycji punktu przeglądu.

Uwaga: w niektórych nowszych aplikacjach NVDA może nie widzieć części lub całości tekstu wyświetlanego na ekranie, co jest rezultatem zastosowania w nich nowszych technik rysowania ekranu, których obsługa przez NVDA nie jest możliwa w tym momencie.

### Nawigacja myszą {#NavigatingWithTheMouse}

Gdy poruszasz myszą, NVDA domyślnie odczytuje tekst znajdujący się bezpośrednio pod jej wskaźnikiem.
W zależności od typu okna zawierającego tekst odczytany może zostać cały paragraf lub pojedyncza linia.

Możesz także skonfigurować NVDA w taki sposób, aby oprócz odczytywania tekstu program informował również o typie [obiektu](#Objects) lub kontrolki, nad którym aktualnie znajduje się wskaźnik myszy, np. listach, przyciskach itp. 
Może być to użyteczne dla zupełnie niewidomych użytkowników, jako że czasem sam tekst nie wystarcza.

NVDA może za pomocą dźwięków przekazywać położenie myszy na ekranie.
Im wyżej na ekranie znajduje się wskaźnik, tym wyższy jest generowany dźwięk.
Im dalej z lewej lub prawej strony znajduje się wskaźnik, tym bardziej z lewej lub prawej strony będzie odtwarzany dźwięk (zakładając, że użytkownik posiada stereofoniczne słuchawki lub głośniki).

Wyżej opisane opcje dotyczące nawigacji myszą nie są domyślnie włączone.
Możesz skonfigurować je, korzystając z kategorii [Ustawienia myszy](#MouseSettings) w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.

Do właściwego korzystania z funkcji oferowanych przez urządzenia wskazujące powinno się używać fizycznej myszy lub touch pada, pomimo tego NVDA posiada kilka funkcji które ułatwiają korzystanie z myszy.
<!-- KC:beginInclude -->

| Nazwa |skrót układu desktop |Skrót układu laptop |Gest dotykowy |Opis|
|---|---|---|---|---|
|Lewy przycisk myszy |Numeryczny slesz |NVDA+[ |brak |Wykonuje pojedyncze kliknięcie myszą. Popularny "dwuklik" może być wykonany poprzez dwukrotne szybkie naciśnięcie skrótu.|
|Zablokowanie lewego przycisku myszy |shift+numeryczny slesz |NVDA+kontrol+[ |brak |Blokuje lewy przycisk myszy. Naciśnij ten skrót ponownie, aby go odblokować. W celu przeciągnięcia myszy przesuń fizyczne urządzenie w dane miejsce lub użyj innego przeznaczonego do tego skrótu|
|Prawy przycisk myszy |Numeryczna gwiazdka |NVDA+] |długie naciśnięcie |Wykonuje kliknięcie prawym przyciskiem myszy. Skrót ten jest używany do otwierania menu kontekstowego w niektórych aplikacjach.|
|Zablokowanie prawego przycisku myszy |shift+Numeryczna Gwiazdka |NVDA+kontrol+] |brak |Blokuje prawy przycisk myszy. Naciśnij ten skrót ponownie, aby go odblokować. W celu przeciągnięcia myszy przesuń fizyczne urządzenie w dane miejsce lub użyj innego przeznaczonego do tego skrótu|
|Przeniesienie myszy do aktualnego obiektu nawigatora |NVDA+Numeryczny slesz |NVDA+shift+m |brak |Przenosi kursor myszy do pozycji aktualnego obiektu nawigatora.|
|Przeniesienie pozycji nawigatora do obiektu pod myszą |NVDA+Numeryczna gwiazdka |NVDA+shift+n |brak |Przenosi obiekt nawigatora do aktualnej pozycji myszy.|

<!-- KC:endInclude -->

## Tryb czytania {#BrowseMode}

Złożone dokumenty przeznaczone tylko do odczytywania, na przykład strony internetowe, przedstawiane są w NVDA w trybie czytania.
Dotyczy to dokumentów wyświetlanych w następujących aplikacjach:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Wiadomości HTML w programie Microsoft outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* książki wspierane w Amazon Kindle dla PC

Tryb czytania jest również opcjonalnie dostępny dla dokumentów w programie Microsoft Word. 

W trybie czytania treść dokumentu jest udostępniana w płaskiej reprezentacji, po której można się przemieszczać z użyciem klawiszy kursora tak jak w zwykłych dokumentach tekstowych.
Wszystkie polecenia NVDA dotyczące [fokusa](#SystemCaret) będą działały w tym trybie; np. czytaj wszystko, odczytaj formatowanie, komendy nawigacji wewnątrz tabel, etc.
Podczas gdy [podświetlacz fokusu](#VisionFocusHighlight) jest włączony, pozycja kursora trybu przeglądania jest również pokazywana wizualnie.
Informacja o tym, że tekst jest linkiem, nagłówkiem itd. jest automatycznie anonsowana, gdy się przemieszczasz po dokumencie.

Czasem zachodzi potrzeba interakcji z formularzami znajdującymi się w tych dokumentach. 
Dla przykładu, będziesz musiał to zrobić dla pól edycji i list, aby możliwe stało się wpisywanie znaków i używanie klawiszy kursora do pracy z kontrolką.
Jest to możliwe dzięki trybowi formularza, w którym prawie wszystkie naciskane klawisze są przekazywane do kontrolki.
Domyślnie w trybie czytania NVDA będzie automatycznie przechodzić w tryb formularza, gdy przejdziesz klawiszem Tab lub klikniesz kontrolkę, która tego wymaga.
Odwrotnie - kliknięcie lub przejście Tabem do kontrolki nie wymagającej trybu formularza, spowoduje przejście do trybu czytania.
Możesz również przejść do trybu formularza przy użyciu spacji lub Entera, naciśniętego na kontrolce, która wymaga trybu formularza.
Naciśnięcie klawisza Escape spowoduje powrót do trybu czytania.
Dodatkowo możesz wymusić tryb formularza, który pozostanie wówczas aktywny do chwili ręcznego wyłączenia.

<!-- KC:beginInclude -->

| Działanie |Skróty klawiszowe |Opis|
|---|---|---|
|Przełącz tryb czytania |NVDA+Spacja |Przełącza pomiędzy trybem formularza i trybem czytania|
|Wyjście z trybu formularza |Escape |Przełącza się na tryb czytania, jeśli wcześniej tryb formularza włączył się automatycznie|
|Odśwież zawartość dokumentu |NVDA+F5 |Odświeża aktualny dokument w trybie przeglądania. (przydatne w przypadku, gdy niektórych treści brakuje na stronie. Niedostępne w Microsoft Word i Outlook.)|
|Znajdź |NVDA+Ctrl+F |Pojawia się okno dialogowe, w którym można wpisać tekst, aby przeszukać aktualny dokument. Więcej informacji w rozdziale [Wyszukiwanie tekstu](#SearchingForText).|
|Znajdź następny |NVDA+F3 |Znajduje w dokumencie następne wystąpienie wyszukiwanego wcześniej tekstu|
|Znajdź poprzedni |NVDA+Shift+F3 |Znajduje w dokumencie poprzednie wystąpienie wyszukiwanego wcześniej tekstu|

<!-- KC:endInclude -->

### Nawigacja pojedynczymi literami {#SingleLetterNavigation}

Podczas pracy w trybie czytania można używać pojedynczych liter do przechodzenia pomiędzy kolejnymi elementami określonego typu. 
Zauważ, że nie wszystkie te komendy są dostępne we wszystkich typach dokumentów.

<!-- KC:beginInclude -->
Naciśnięcie litery przechodzi do następnego elementu odpowiedniego typu, natomiast naciśnięcie litery z klawiszem Shift przechodzi do elementu poprzedniego.

* H: nagłówek
* L: lista
* I: element listy
* T: tabela
* K: link
* N: tekst niebędący linkiem
* F: pole formularza
* U: nieodwiedzony link
* V: odwiedzony link
* E: pole edycji
* B: przycisk
* X: pole wyboru
* C: pole rozwijalne
* R: przycisk radiowy
* Q: blok cytatu
* S: separator
* M: ramka
* G: grafika
* D: punkt orientacyjny
* O: obiekt zagnieżdżony (odtwarzacz audio lub wideo, aplikacja, okno dialogowe etc.)
* Cyfry 1 do 6: nagłówki poziomu odpowiednio  od 1 do 6
* A: adnotacja (komentarz, zmiana edytorska, itd.)
* `p`: akapit tekstu
* w: błąd pisowni

Aby przejść na początek lub koniec elementów takich jak listy i tabele:

| Działanie |Skrót |Opis|
|---|---|---|
|Przejdź na początek kontenera |Shift+, |Przechodzi na początek kontenera (listy, tabeli etc.), na którym ustawiony jest kursor|
|Przejdź poza koniec kontenera |Przecinek |Przenosi poza koniec kontenera (listy, tabeli, etc.) na którym znajdował się kursor|

<!-- KC:endInclude -->

Niektóre aplikacje webowe takie jak Gmail, Twitter czy Facebook, używają pojedynczych liter jako klawiszy skrótu.
Jeśli chcesz używać tych skrótów i móc jednocześnie posługiwać się klawiszami strzałek do odczytu treści w trybie czytania, możesz tymczasowo wyłączyć nawigację pojedynczymi literami NVDA.
<!-- KC:beginInclude -->
Aby włączyć i wyłączyć nawigację literami dla aktualnego dokumentu, naciśnij NVDA+Shift+Spacja.
<!-- KC:endInclude -->

#### Skrót nawigacji po akapitach tekstowych {#TextNavigationCommand}

Można się przemieszczać po poprzednim lub następnym akapicie naciskając `p` lub `shift+p`.
Akapity są określone przez grupę tekstu napisaną całymi zdaniami.
To może być praktyczne do zlokalizowania użytecznej treści na stronach internetowych, takich jak:

* gazety internetowe
* Fora
* Wpisy blogowe

To polecenei może takżę być użyteczne do omijania niektórych niepotrzebnych elementów, takich jak:

* reklamy
* meni
* nagłówki

moewajcie na uwadze, że ten algorytm nie jest doskonały, i czasem może nie działać prawidłowo.
W dodatku, to polecenie różni się od polecenia `control+strzałka w dół/w górę`.
Nawigacja po akapitach tekstowych przemieszcza tylko po akapitach tekstowych, gdy polecenie dla nawigacji  po akapicie przemieszcza po akapitach, bez względu na to, czy istnieje tekst lub nie.

#### Inne polecenia do nawigacji {#OtherNavigationCommands}

Oprócz poleceń do szybkiej nawigacji zawartych powyżej, NVDA posiada nieskojarzone polecenia.
Aby je używać, musisz z nimi skojarzyć skrót klawiszowy lub dotykową gestę w [oknie dialogowym zdarzeń wejścia](#InputGestures).
Oto spis dostępnych poleceń

* Artykuł
* Figura
* grupowanie
* Karta właściwości
* Element meni
* Przycisk przełączania
* pasek postępu
* Formuła matematyczna
* pionowo wyrównany akapit
* tekst tego samego stylu
* Tekst różnego stylu

Zauważ, że istnieją dwie akcje dla każdego polecenia, do przemieszczania w przód albo w tyl w dokumencie, i w celu prawidłowej nawigacji w obu kierunkach, muzisz je ustawić.
Na przykład, jeżeli chcesz używać skrótów `y` / `shift+y` do szybkiego przemieszczania się między kartami właściwości, powinieneś wykonać następujące kroki

1. Otwórz okno dialogowe zdarzenia wejścia z któregokolwiek dokumentu HTML.
1. Znajdź element "Przemieszcza do następnej karty właściwości" w rozdziale tryb czytania.
1. Skojarz skrót `y` ze znalezionym poleceniem.
1. Znajdź element "przemieszcza do poprzedniej karty właściwości".
1. Skojarz skrót `shift+y` ze znalezionym poleceniem.

### Lista elementów {#ElementsList}

Lista elementów umożliwia dostęp do listy różnych elementów, znajdujących się w dokumencie, właściwych dla konkretnej aplikacji.
Dla przykładu w przeglądarkach www, lista elementów wymienia linki, nagłówki, pola formularzy, przyciski albo punkty orientacyjne.
Przyciski radiowe pozwalają przełączać się pomiędzy różnymi typami elementów.
Pole edycyjne w oknie dialogowym pozwala na filtrowanie listy, ułatwiając wyszukiwanie danej pozycji na stronie.
Możesz użyć przycisków znajdujących się w okienku, aby przejść do wybranego elementu albo go aktywować.
<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|Wyświetl listę elementów w trybie przeglądania |NVDA+F7 |Wyświetla listę różnych typów elementów znajdujących się w bieżącym dokumencie|

<!-- KC:endInclude -->

### Wyszukiwanie tekstu {#SearchingForText}

To okno pozwala przeszukiwać bieżący dokument.
W polu "Wpisz szukany tekst", można wprowadzić tekst do wyszukania.
Pole wyboru "Uwzględniaj wielkość liter"  sprawia, że wyszukiwanie będzie rozróżniać wielkość liter.
Dla przykładu, po zaznaczeniu tego pola możesz znaleźć "NV Access", ale nie "nv access".
Użyj poniższych klawiszy skrótów dla przeprowadzenia wyszukiwania:
<!-- KC:beginInclude -->

| Polecenie |Klawisz skrótu |Opis|
|---|---|---|
|Znajdź tekst |NVDA+control+f |Otwiera okno wyszukiwania|
|Znajdź następny |NVDA+f3 |Poszukuje następnego wystąpienia ostatnio poszukiwanego tekstu|
|Znajdź poprzedni |NVDA+shift+f3 |Poszukuje poprzedniego wystąpienia ostatnio wyszukiwanego tekstu|

<!-- KC:endInclude -->

### Obiekty zagnieżdżone {#ImbeddedObjects}

Strony mogą zawierać bogate treści, korzystając z technologii takich jak Oracle Java i HTML5 oraz mogą również zawierać aplikacje i okna dialogowe.
Gdy napotkasz taki element w trybie czytania, NVDA odczyta odpowiednio "obiekt zagnieżdżony", "Aplikacja" albo "Dialog".
Możesz przechodzić do nich używając klawiszy szybkiej nawigacji o i shift+o.
Naciśnij klawisz Enter na takim obiekcie w celu interakcji z nim.
Jeśli obiekt jest dostępny dla NVDA, będziesz mógł przemieszczać się w nim klawiszem Tab i pracować tak, jak w innych aplikacjach.
Odpowiednia komenda klawiszowa pozwala na powrót do oryginalnej strony zawierającej aktywowany wcześniej obiekt.
<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|Przechodzi do zawartości strony |NVDA+Ctrl+Spacja |Przenosi fokus z wewnątrz obiektu zagnieżdżonego do dokumentu, który zawierał ten obiekt.|

<!-- KC:endInclude -->

### Tryb kopiowania z zachowanym formatowaniem {#NativeSelectionMode}

Domyślnie podczas zaznaczania tekstu za pomocą  `shift+strzałek` w trybie czytania, zaznaczony jest tylko tekst, ale nie i jego formatowanie.
To oznacza, że zaznaczenie tekstu nie jest widoczne wizualnie, a kopiowanie testu za pomocą skrótu `control+c` spowoduje kopiowanie tylko czystego tekstu. Czyli, że formatowanie tabeli lub właściwości linku nie będą skopiowane.
Jednakże, NVDA posiada tryb kopiowania z zachowanym formatowaniem który może być włączony w poszczególnych dokumentach w trybie do czytania (na razie tylko w Mozilli Firefox) co skutkuje, że tryb kopiowania z zachowanym formatowania będzie śledził zaznaczenie w trybie czytania NVDA.

<!-- KC:beginInclude -->

| Nazwa |Skrót |Opis|
|---|---|---|
|Włącza lub wyłącza tryb kopiowania z zachowanym formatowaniem |`NVDA+shift+f10` |Włącza lub wyłącza tryb kopiowania z zachowanym formatowaniem off|

<!-- KC:endInclude -->

Gdy tryb kopiowania z zachowanym formatowaniem jest włączony, Kopiowanei zaznaczonego tekstu za pomocą `control+c` użyje funkcji kopiowania aplikacji, co oznacza, że formatowanie będzie skopiowane do schowka zamiast czystego tekstu.
To oznacza, że kopiowanie takiej treści do programu, takiego jak Microsoft Word lub Excel, skopiuje formatowanie takie jak tabele i linki.
Miewajcie na uwadze, że tryb kopiowania z zachowanym formatowaniem nie skopiuje jednak niektórych dostępnościowych oznaczeń, oraz informacji generowanych przez NVDA w trybie czytania.
Także, choć aplikacja się postara zachować zgodność formatowania z zaznaczeniem NVDA, to może być nie zawsze dokładne.
Jednakże, w przypadkach, w których musisz skopiować calą tabele lub akapit z formatowaniem, ta funkcja będzie użyteczna.

## Odczyt treści matematycznej {#ReadingMath}

NVDA może czytać treść matematyczną w internecie i w innych aplikacjach, umożliwiając jej odczyt zarówno mową, jak i brajlem. 
Jednakże, aby NVDA mogła czytać treść matematyczna, musisz zainstalować komponent matematyczny.
Istnieje kilka dostępnych dodatków dla NVDA w NVDA addon store, które umożliwiają odczyt treści matematycznej, włączając w to [MathCAT NVDA add-on](https://nsoiffer.github.io/MathCAT/) i [Access8Math](https://github.com/tsengwoody/Access8Math). 
Prosimy przeczytać [rozdział add-on store](#AddonsManager) aby się dowiedzieć, jak instalować i przeglądac dodatki dla  NVDA.
NVDA także może używać starszego program [MathPlayer](https://info.wiris.com/mathplayer-info) firmy Wiris jeżeli jest zainstalowany w systemie, choć ten program już nie jest wspieranyd.

### Wspierana treść matematyczna {#SupportedMathContent}

Z odpowiednio zainstalowanym komponentem matematycznym, NVDA wspiera następujące typy treści matematycznej:

* MathML w Mozilla Firefox, Microsoft Internet Explorer i Google Chrome.
* Microsoft Word 365 współczesne matematyczne równania używając UI automation:
NVDA może czytać i wchodzić w interakcje z równaniami matematycznymi w programie Microsoft Word 365/2016 kompilacji 14326 i nowszymi.
Trzeba jednak mieć na uwadze, że każde już poprzednio stworzone równanie powinniśmy najpierw przekształcić do matematycznego formatu Office.
Można to zrobić zaznaczając każde równanie i wybierając opcje równania -> konwertuj do matematyki Office w menu kontekstowym.
Prosze się upewnić, że uruchamiasz ostatnią wersję MathType przed konwersją równań.
Microsoft Word teraz także daje możliwość nawigacji linearnej po równaniach, a także wspiera wprowadzanie równań za pomocą kilka składni, włączając w to LateX. 
Dla więcej szczegółów, proszę przeczytać artykuł: [Równania w formacie liniowym używając UnicodeMath i LaTeX w programie Word](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint, i starsze wersje programu Microsoft Word: 
NVDA może odczytywać i wchodzić w interakcję z równaniami MathType w programach Microsoft Powerpoint i Microsoft word.
Aby to działało, musi być zainstalowany mathtype.
Wersja próbna jest wystarczająca.
Można ją pobrać z [MathType strony prezentacji](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Nie jest to jeszcze oficjalny standard, nie istnieje publicznie dostępne oprogramowanie które potrafi wytwarzać taką treść.
* Kindle Reader dla PC:
NVDA może odczytywać treść matematyczną w programie Kindle dla PC w książkach z dostępną matematyką.

Podczas odczytywania dokumentu, NVDA wypowie każdą obsługiwaną treść matematyczną tam, gdzie się ona znajduje.
Jeśli używasz monitora brajlowskiego, zostanie ona również wyświetlona w brajlu.

### Nawigacja interaktywna {#InteractiveNavigation}

Jeśli pracujesz głównie z mową, w większości przypadków zechcesz przeczytać wyrażenie w mniejszych segmentach, zamiast odczytu całości od razu.

W trybie czytania można to osiągnąć przez przejście kursorem do treści matematycznej i naciśnięcie Enter.

Poza trybem czytania:

1. Przesuń punkt przeglądu do treści matematycznej.
Domyślnie, punkt przeglądu podąża za kursorem systemowym, więc można użyć kursora systemowego, by przejść do treści.
1. Następnie, aktywuj poniższe polecenie:

<!-- KC:beginInclude -->

| Polecenie |Klawisz |Opis|
|---|---|---|
|Interakcja z treścią matematyczną |NVDA+Alt+M |Rozpoczyna interakcję z treścią matematyczną.|

<!-- KC:endInclude -->

W tym momencie, aktywujesz tryb matematyczny w programie NVDA, w którym możesz używać poleceń takich jak strzałki do chodzeniu po wyrazie.
Dla przykładu: możesz przechodzić po wyrażeniu strzałkami lewo i prawo,  i wejść w głąb fragmentu wyrażenia, np. ułamka,  przy użyciu strzałki w dół.

Aby powrócić do dokumentu, naciśnij klawisz Esc.

Po więcej informacji o nawigacji i interakcji z treścią matematyczną, przeczytaj dokumentację określonego komponentu matematycznego, którego zainstalowałęś.

* [Dokumentacj MathCAT](https://nsoiffer.github.io/MathCAT/users.html)
* [Dokumentacja Access8Math](https://github.com/tsengwoody/Access8Math)
* [Dokumentacja MathPlayer](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Czasem treść matematyczna może być wyświetlana jako przycisk lub inny typ elementu który po aktywacji może być wyświetlany w dialogu w którym wyświetlone zostają informacje związane z formułą.
Aby aktywować przycisk lub element zawierający formułę, naciśnij ctrl+enter.

### Instalowanie MathPlayera {#InstallingMathPlayer}

Chociaż jest rekomendowane używanie nowszych dodatkó dla NVDA do wsparcia treści matematycznej, w niektóych ograniczonych przypadkach MathPlayer może być najbardziej odpowiednią opcja.
Na przykłąd MathPlayer może wspierać określony język lub standart brajla niewspieranego w nowszych dodatkach.
MathPlayer jest dostępny za darmo ze strony firmy Wiris.
[Pobierz MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Po instalacji MathPlayera, musisz ponownie uruchomić NVDA. 
Miewaj na uwadze, że w informacjach o MathPlayerze jest napisane,  że jest to program dla starszych przeglądarek takich jak Internet Explorer 8.
Odnosi się to do wizualnego wyświetlania matetreści matematycznej za pomocą MathPlayea, i może być ignorowane przez używających MathPlayera z NVDA.

## Brajl {#Braille}

Jeśli posiadasz monitor brajlowski, NVDA może wyświetlać informacje w brajlu.
Jeśli twój monitor ma klawiaturę brajlowską, możesz wprowadzać brajla skrótami lub w wersji nieskróconej.
Brajl może być również wyświetlany za pomocą funkcji [podglądu brajla](#BrailleViewer) zamiast lub też w koniunkcji z fizycznym monitorem brajlowskim.

Więcej informacji o obsługiwanych monitorach zawiera rozdział [Obsługiwane monitory brajlowskie](#SupportedBrailleDisplays).
Ten rozdział zawiera również informacje o linijkach brajlowskich obsługiwanych przez NVDA funkcją automatycznego wykrywania urządzeń brajlowskich.
Możesz skonfigurować ustawienia brajlowskie przy użyciu [kategorii ustawień brajla](#BrailleSettings)w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.

### Brajlowskie skróty typu i stanu kontrolki oraz punktów orientacyjnych {#BrailleAbbreviations}

Aby zmieścić jak najwięcej informacji na monitorze brajlowskim, zdefiniowano poniższe skróty określające typ i stan kontrolki oraz punkty orientacyjne.

| Skrót |Typ kontrolki|
|---|---|
|app |aplikacja|
|art |artykuł|
|qt |blok cytatu|
|btn |Przycisk|
|drbtn |przycisk rozwijany|
|spnbx |przycisk pokrętła|
|sbtn |przycisk podziału|
|btn |przycisk przełącznika|
|cap |napis|
|cbo |Lista rozwijana|
|chk |Pole wyboru|
|dlg |Dialog|
|doc |dokument|
|edt |Pole edycji tekstu|
|pwded |pole hasła|
|emb |obiekt zagnieżdżony|
|ent |przypis końcowy|
|fig |figura|
|fnt |przypis dolny|
|gf |Grafika|
|grp |grupowanie|
|hN |Nagłówek poziomu N, np. h1, h2.|
|hlp |dymek pomocy|
|puo |punkt orientacyjny|
|lnk |Link|
|vlnk |Odwiedzony link|
|lst |Lista|
|mnu |Menu|
|mnubar |Pasek menu|
|mnubtn |przycisk menu|
|elmnu |element menu|
|pnl |panel|
|PB |pasek postępu|
|bsyind |okrąg postępu|
|rbtn |Przycisk opcji|
|scrlbar |pasek przewijania|
|sect |sekcja|
|stbar |pasek stanu|
|tab |zakładka|
|tbl |Tabela|
|cN |Kolumna tabeli o numerze n, np. c1, c2.|
|rN |Wiersz tabeli o numerze n, np. r1, r2.|
|term |terminal|
|TB |tool bar|
|tip |dymek|
|tv |Widok drzewa|
|tvbtn |przycisk widoku drzewa|
|tv |element drzewa|
|lv N |Widok drzewa ma hierarchiczny poziom N|
|wnd |okno|
|⠤⠤⠤⠤⠤ |separator|
|mrkd |Treść oznaczona|

Zdefiniowano także poniższe oznaczenia stanu:

| Skrót |Stan kontrolki|
|---|---|
|... |Wyświetlane, gdy obiekt obsługuje autouzupełnianie|
|⢎⣿⡱ |wyświetlane, gdy obiekt (np. przełącznik) jest wciśnięty|
|⢎⣀⡱ |wyświetlane, gdy obiekt (np. przełącznik) jest niewciśnięty|
|⣏⣿⣹ |Wyświetlane, gdy obiekt (np. pole wyboru) jest zaznaczony|
|⣏⣸⣹ |Wyświetlane, gdy obiekt (np. pole wyboru) jest częściowo zaznaczony|
|⣏⣀⣹ |Wyświetlane, gdy obiekt (np. pole wyboru) jest niezaznaczony|
|- |Wyświetlane, gdy obiekt (np. drzewo) można zwinąć|
|+ |Wyświetlane, gdy obiekt (np. drzewo) można rozwinąć|
|*** |wyświetlane dla zabezpieczonych dokumentów lub kontrolek|
|clk |Wyświetlane, gdy obiekt jest klikalny|
|cmnt |wyświetlane dla komentarzy komórki arkusza kalkulacyjnego lub fragmentu tekstu w dokumencie|
|frml |wyświetlane, gdy komórka arkusza zawiera formułę|
|<--> |wyświetlane, gdy wprowadzono nieprawidłową wartość|
|ldesc |wyświetlane, gdy obiekt (na ogół grafika) ma długi opis|
|mled |wyświetlane, gdy pole edycyjne jest wieloliniowe (np. komentarze na stronach)|
|req |wyświetlane dla wymaganych pól formularzy|
|ro |Wyświetlane, gdy obiekt (np. pole edycji) jest tylko do odczytu|
|chk |Wyświetlane, gdy obiekt jest wybrany|
|nchk |wyświetlane, gdy obiekt jest niewybrany|
|-:C |wyświetlane, gdy obiekt jest posortowany rosnąco|
|c:- |wyświetlane, gdy obiekt jest posortowany malejąco|
|submnu |Wyświetlane, gdy obiekt posiada wyskakujące menu (zwykle podmenu)|

Zdefiniowane zostały poniższe skróty dla punktów orientacyjnych:

| Skrót |Punkt orientacyjny|
|---|---|
|bnnr |banner|
|cinf |informacje o treści|
|cmpl |uzupełniające|
|form |formularz|
|main |główne|
|nav |nawigacja|
|srch |szukaj|
|obszar |obszar|

### Wprowadzanie brajla {#BrailleInput}

NVDA obsługuje wprowadzanie brajla skrótami lub w za pomocy pisma pełnego przy użyciu klawiatury brajlowskiej.
Możesz wybrać tablicę tłumaczenia wprowadzanego brajla na tekst przy użyciu opcji [Tablica wejścia](#BrailleSettingsInputTable) w kategorii ustawień brajla w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.

Jeśli używane jest pismo pełne, tekst jest wstawiany od razu po wprowadzeniu.
Jeśli używane są skróty brajlowskie, tekst jest wstawiany po naciśnięciu spacji lub Entera na końcu słowa.
Tłumaczenie może uwzględniać tylko wpisywane słowo i nie bierze pod uwagę istniejącego tekstu.
Dla przykładu, jeśli używasz kodu brajlowskiego, który rozpoczyna liczby znakiem cyfry i naciśniesz Backspace kasując początek liczby, będziesz musiał wpisać znak cyfry ponownie aby wprowadzić następne cyfry.

<!-- KC:beginInclude -->
Naciśnięcie punktu 7 kasuje ostatni znak lub komórkę brajla.
Punkt 8 tłumaczy wprowadzony brajl i naciska klawisz enter.
Naciśnięcie punktu 7 + punktu 8  tłumaczy wprowadzony brajl, ale bez dodawania spacji lub naciskania entera.
<!-- KC:endInclude -->

#### Wprowadzanie skrótów klawiszowych {#BrailleKeyboardShortcuts}

NVDA wspiera wprowadzanie skrótów klawiszowych i emulowanie wciskania klawiszy za pomocą monitora brajlowskiego.
Ta emulacja istnieje w dwóch formach: bezpośrednie przydzielony skrót do kombinacji na monitorze brajlowskim  lub używanie wirtualnych modyfikatorów.

Często używane klawisze, takie jak strzałki lub klawisz alt do otwierania paska menu, mogą być bezpośrednio mapowane do skrótów na monitorze brajlowskim.
Sterownik dla każdego monitora brajlowskiego przychodzi z przedefiniowanymi takimi skrótami.
Można zmieniać te skróty lub dodawać nowe klawisze emulowane z poziomu okna dialogowego [zdarzenia wejścia](#InputGestures).

Chociaż ta metoda jest korzystna dla często naciskanych oraz unikalnych klawiszy (takich jak Tab), może nie chcielibyśmy przydzielić unikatowy set klawiszy dla każdego skrótu klawiszowego.
Żeby umożliwić emulowanie modyfikatorów z przytrzymywaniem modyfikatorów, NVDA posiada polecenia do emulowania klawiszy control, alt, shift, windows, i NVDA, razem z kombinacjami tych klawiszy.
Żeby używać tych przełączników, najpierw trzeba nacisnąć polecenie (lub sekwencję poleceń) dla modyfikatorów których chcesz nacisnąć.
Potem wprowadź znak, który jest częscią skrótu którego chcesz nacisnąć.
Na przykład, aby nacisnąć control+f, użyj "przełącznika do klawisza control" a potem wprowadź f,
i żeby nacisnąć control+alt+t, albo użyj  "przełacznika do klawisza control" i "przełącznika do klawisza alt", niezależnie od porządku, albo "przełącznik do emulowania control i alt" a potem literka t.

Jeżeli niechcący nacisniesz klawisz modyfikatora, naciśnięcie modyfikatora usunie modyfikator.

Gdy używamy skrótów brajlowskich, używanie modyfikatorów skutkuje tłumaczeniem wprowadzonych znaków jako naciśniętych klawiszy kropek 7 i 8.
Warto dodać, że emulowany klawisz nie może wpływać na wpisany brajl przed wprowadzonym modyfikatorem.
To oznacza, że dla wprowadzania kombinacji alt+2 z tablicą brajlowską używającą znaku liczbowego, najpierw trzeba nacisnąć alt a potem wprowadzić znak liczby.

## Widoczność {#Vision}

NVDA jest programem tworzonym głównie z myślą o osobach niewidomych które korzystają z komputera przy pomocy mowy lub/i brajla, mimo tego posiada on funkcje umożliwiające zmianę zawartości ekranu.
Takie ulepszenia nazywane są przez NVDA "dostawcą ulepszenia widoczności".

Czytnik ekranu  posiada kilka takich funkcji. Opis każdej z nich znajduje się poniżej.
Dodatkowi dostawcy mogą być dostarczone w formie [Dodatków dla NVDA](#AddonsManager).

Ustawienia widoczności mogą być zmienione w [kategorii "widoczność"](#VisionSettings) znajdującej się w [ustawieniach głównych programu](#NVDASettings) dialog.

### Podświetlacz fokusu {#VisionFocusHighlight}

Podświetlacz fokusu może pomóc w identyfikacji pozycji [kursora systemowego](#SystemFocus), [aktualnej pozycji nawigatora](#ObjectNavigation) i [pozycji trybu przeglądania](#BrowseMode).
Pozycje te są wyróżnione kolorowym prostokątnym konturem.

* Kolorem niebieskim zaznaczana jest pozycja kursora systemowego połączonego z obiektem nawigatora, na przykład jeżeli kursor systemowy [podąża za nawigatorem](#ReviewCursorFollowFocus)
* Niebieskimi kreskami oznaczana jest pozycja kursora systemowego.
* Kolorem różowym zaznaczany jest obiekt nawigatora.
* Kolor żółty zaś sygnalizuje pozycję wirtualnego kursora przeglądania.

Kiedy podświetlacz fokusu jest włączony w [ustawieniach widoczności](#VisionSettings) w [oknie głównym programu](#NVDASettings) dialog, możesz [zmienić co ma być podświetlane.](#VisionSettingsFocusHighlight)

### Kurtyna {#VisionScreenCurtain}

Użytkownikowi niewidomemu nie zawsze wymagana jest widoczność ekranu.
Co więcej, nie zawsze wiadomo czy ktoś nie patrzy przez twoje ramie.
Specjalnie na takie sytuacje, NVDA posiada funkcję kurtyny, która powoduje że ekran staje się czarny.

Możesz włączyć funkcję kurtyny w ustawieniach [widoczności](#VisionSettings) w [oknie  głównym NVDA](#NVDASettings) dialog.

<!-- KC:beginInclude -->

| Nazwa |Skrót |Opis|
|---|---|---|
|Włącza lub wyłącza kurtynę |`NVDA+control+escape` |Włącza kurtynę dla zaciemnienai ekranu, lub ją wyłącza dla widoczności informacji. Przy jednokrotnym naciśnięciu, kurtyna jest włączona do momentu ponownego uruchomienia NVDA. Przy dwukrotnym naciśnięciu, kurtyna jest włączona do momentu ręcznego wylączenia.|

<!-- KC:endInclude -->

Gdy kurtyna jest aktywna, niektóre zadania bezpośrednio oparte na tym co widzimy na ekranie, takie jak wywoływanie [rozpoznawania tekstu](#Win10Ocr) lub fotografowania treści ekranu nie mogą być wypełnione.

Z powodu zmiany w API Lupy Systemu Windows, należało zaktualizować Kurtynę, aby wspierała najnowsze wersje systemu Windows.
Użyj NVDA 2021.2 aby włączyć Kurtynę w systemie Windows 10 21H2 (10.0.19044) lub nowszych.
Jeśli używasz nowej wersji systemu Windows, dla bezpieczeństwa upewnij się, że przy włączonej Kurtynie ekran jest zupełnie czarny.

Miewajcie na uwadze, że gdy Lupa systemu Windows jest uruchomiona a odwrócone kolory są używane, kurtyne nie można włączyć.

## Rozpoznawanie treści {#ContentRecognition}

Jeśli autorzy nie dostarczają informacji pomocnej użytkownikom ekranu do odczytania treści, rozmaite narzędzia mogą zostać użyte dla rozpoznania tekstowej treści z graficznego obrazu.
NVDA obsługuje funkcjonalność optycznego rozpoznawania znaków (OCR) wbudowaną w system operacyjny Windows 10 i nowsze wersje, aby wydobyć tekst z obrazów.
Dodatkowe narzędzie rozpoznawania treści może zostać dostarczone poprzez dodatki NVDA.

Przy użyciu komendy rozpoznawania treści, NVDA rozpoznaje zawartość aktualnego [obiektu nawigatora](#ObjectNavigation).
Domyślnie, obiekt nawigatora podąża za fokusem systemowym lub kursorem w trybie czytania, więc wystarczy przesunąć fokus lub kursor trybu czytania tam gdzie jest to potrzebne.
Dla przykładu, przesunięcie kursora trybu czytania na obrazek, domyślnie rozpoznanie wydobędzie tekst z tej grafiki.
Można jednak użyć funkcji nawigacji w hierarchii obiektów, aby na przykład rozpoznać zawartość całego okna aplikacji.

Gdy rozpoznanie zostanie zakończone, wynik zostanie zaprezentowany w dokumencie podobnym do trybu czytania, pozwalając odczytać informację klawiszami strzałek, etc.
Naciśnięcie spacji lub entera aktywuje (zwykle przez kliknięcie) tekst pod kursorem, jeśli będzie to możliwe.
Naciśnięcie klawisza Escape spowoduje wyjście z wyniku rozpoznawania.

### OCR Windows {#Win10Ocr}

Windows 10 i nowsze wersje systemu operacyjnego Windows zawierają OCR dla wielu języków.
NVDA może go używać dla rozpoznawania tekstu z obrazków lub okien niedostępnych aplikacji.

Możesz ustawić język, który ma być użyty dla rozpoznawania tekstu w kategorii [Windows OCR](#Win10OcrSettings) w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.
Dodatkowe języki mogą zostać zainstalowane po otwarciu Menu start, wybraniu Ustawienia, wybór daty i języka -> Region i język, a następnie po wybraniu Dodaj język.

Gdy chcesz śledzić zmieniającą się dynamicznie treść, na przykład napisy w filmie, którego oglądasz, Możesz włączyć automatyczne odświeżanie rozpoznanej treści.
Możesz to zrobić w kategorii [Windows OCR](#Win10OcrSettings) [ustawień NVDA](#NVDASettings).

Funkcja Windows OCR może być częsciowo oraz całkowicie niezgodna z [Ulepszeniami wizji NVDA](#Vision) oraz z innymi zewnętrznymi pomocami do ulepszenia widzenia. Przed rospoczęciem rozpoznawania tekstu, trzeba wyłączyć takie narzędzia.

<!-- KC:beginInclude -->
Aby rozpoznać tekst aktualnego obiektu nawigatora przy użyciu OCR systemu Windows, naciśnij NVDA+r.
<!-- KC:endInclude -->

## Funkcje specyficzne dla aplikacji {#ApplicationSpecificFeatures}

NVDA udostępnia dodatkowe funkcje dla niektórych aplikacji, aby uczynić niektóre zadania łatwiejszymi lub udostępnić daną funkcjonalność, która w innym przypadku byłaby niedostępna dla użytkownika oprogramowania czytającego ekran.

### Microsoft Word {#MicrosoftWord}
#### Automatyczny odczyt nagłówków kolumn i wierszy {#WordAutomaticColumnAndRowHeaderReading}

NVDA może automatycznie odczytywać odpowiedni nagłówek wiersza i kolumny podczas nawigacji wewnątrz tabel w Microsoft Word.
To wymaga włączonej opcji "zgłaszanie współrzędnych komórek kolumn i wierszy"  w ustawieniach formatowania dokumentów NVDA w [oknie dialogowym ustawień NVDA](#NVDASettings),.

Jeżeli używasz [UIA w celu uzyskania dostępu do dokumentów Microsoft Word](#MSWordUIA), co jest domyślną opcją w ostatnich wersjach programu Microsoft Word i w systemie Windows, komórki pierwszego wiersza będą uznane za nagłówki. Podobnie, komórki pierwszej kolumny będą uznane za nagłówki.

W przeciwnym razie, jeżeli nie używasz [UIA w celu uzyskania dostępu do dokumentów Microsoft Word](#MSWordUIA), musisz wskazać, który wiersz lub kolumna zawiera nagłówki w każdej tabeli.
Po przejściu do pierwszej komórki wiersza lub kolumny zawierającej nagłówki, użyj poniższych komend:
<!-- KC:beginInclude -->

| Polecenie |Klawisz |Opis|
|---|---|---|
|Ustaw nagłówki kolumny |NVDA+Shift+C |Jednokrotne naciśnięcie informuje NVDA, że jest to pierwsza komórka nagłówkowa w wierszu zawierającym nagłówki kolumny, która powinna być automatycznie odczytywana, gdy przechodzimy między kolumnami poniżej tego wiersza. Dwukrotne naciśnięcie anuluje ustawienie.|
|Ustaw nagłówki wiersza |NVDA+Shift+R |Jednokrotne naciśnięcie informuje NVDA, że jest to pierwsza komórka nagłówkowa w kolumnie zawierającej nagłówki wiersza, która powinna być automatycznie odczytywana podczas przechodzenia po wierszach za tą kolumną. Dwukrotne naciśnięcie anuluje ustawienie.|

<!-- KC:endInclude -->
Te ustawienia zostaną zapisane w dokumencie jako zakładki, kompatybilne z innymi programami czytania ekranu np. Jaws. 
Oznacza to, że inni użytkownicy programów czytających ekran będą automatycznie mieli te nagłówki ustawione po otwarciu danego dokumentu później. 

#### Tryb czytania w Microsoft Word {#BrowseModeInMicrosoftWord}

Podobnie jak do stron internetowych, tryb czytania może być używany w Microsoft Word, co pozwala używać funkcji takich jak szybka nawigacja i lista elementów.
<!-- KC:beginInclude -->
Aby włączyć lub wyłączyć tryb czytania w Microsoft Word, naciśnij NVDA+Spacja.
<!-- KC:endInclude -->
Więcej informacji o trybie czytania i szybkiej nawigacji , znajduje się w rozdziale [Tryb czytania](#BrowseMode).

##### Lista elementów {#WordElementsList}

<!-- KC:beginInclude -->
W trybie czytania w Microsoft Word możesz uzyskać dostęp do listy elementów naciskając NVDA+F7.
<!-- KC:endInclude -->
Lista elementów wyświetla nagłówki, linki, adnotacje (zawierające komentarze i śledzenie zmian), oraz błędy (aktualnie ograniczone do błędów pisowni).

#### Zgłaszanie komentarzy {#WordReportingComments}

<!-- KC:beginInclude -->
Aby odczytać komentarz na pozycji kursora, naciśnij NVDA+Alt+C.
<!-- KC:endInclude -->
Wszystkie komentarze dokumentu oraz inne zmiany, mogą być wymienione na liście elementów NVDA po wybraniu adnotacji jako typu.

### Microsoft Excel {#MicrosoftExcel}
#### Automatyczny odczyt nagłówków kolumn i wierszy {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA może automatycznie odczytywać odpowiedni nagłówek wiersza i kolumny podczas nawigacji wewnątrz arkuszy w Microsoft Excel.
Wymaga to po pierwsze włączenia odczytywania nagłówków tabel w kategorii formatowanie dokumentów w oknie [Preferencji NVDA](#NVDASettings), znajdującym się w podmenu Ustawienia w menu NVDA.
Po drugie, NVDA musi wiedzieć, która linia lub kolumna zawiera nagłówki.
Po przejściu do pierwszej komórki wiersza lub kolumny zawierającej nagłówki, użyj poniższych komend:
<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|Ustaw nagłówki kolumny |NVDA+Shift+C |Jednokrotne naciśnięcie informuje NVDA, że jest to pierwsza komórka nagłówkowa w wierszu zawierającym nagłówki kolumny, która powinna być automatycznie odczytywana, gdy przechodzimy między kolumnami poniżej tego wiersza. Dwukrotne naciśnięcie anuluje ustawienie.|
|Ustaw nagłówki wiersza |NVDA+Shift+R |Jednokrotne naciśnięcie informuje NVDA, że jest to pierwsza komórka nagłówkowa w kolumnie zawierającej nagłówki wiersza, która powinna być automatycznie odczytywana podczas przechodzenia po wierszach za tą kolumną. Dwukrotne naciśnięcie anuluje ustawienie.|

<!-- KC:endInclude -->
Te ustawienia zostaną zapisane w skoroszycie jako nazwane zakresy, kompatybilne z innymi programami czytającymi takimi jak Jaws.
Oznacza to, że inni użytkownicy oprogramowania czytającego ekran, którzy później otworzą ten skoroszyt, będą mieli te nagłówki już ustawione. 

#### Lista elementów {#ExcelElementsList}

Podobnie jak na stronach internetowych, NVDA posiada listę elementów dla Microsoft Excel, która pozwala wyświetlić i uzyskać dostęp do kilku różnych typów informacji.
<!-- KC:beginInclude -->
Aby otworzyć listę elementów w Excel, naciśnij NVDA+F7.
<!-- KC:endInclude -->
Różne typy informacji na liście elementów to:

* Wykresy: wymienia wszystkie wykresy w aktywnym arkuszu. 
Wybranie wykresu i naciśnięcie Enter lub przycisku "idź do" przeniesie fokus do tego wykresu, umożliwiając nawigację i odczyt strzałkami.
* komentarze: wszystkie komórki w aktywnym arkuszu, zawierające komentarze. 
Wyświetlany jest  adres komórki i jej komentarze. 
Naciśnięcie Enter lub przycisku "idź do", przeniesie fokus do wybranej komórki.
* Formuły: Wymienia wszystkie komórki w arkuszu, które zawierają formułę. 
Wyświetlany jest adres komórki, oraz zawarta w niej formuła.
Naciśnięcie Enter lub przycisku "idź do", przeniesie fokus do wybranej komórki.
* Arkusze: wyświetla wszystkie arkusze w skoroszycie. 
Naciśnięcie F2 na liście arkuszy pozwala zmienić nazwę arkusza. 
Naciśnięcie Enter lub przycisku "idź do", przeniesie fokus do wybranego arkusza.
* Pola formularzy: wyświetla wszystkie pola formularzy w aktywnym arkuszu.
Dla każdego pola formularza, lista elementów wyświetla alternatywny tekst pola oraz adresy komórek, które ono zajmuje.
Zaznaczenie pola i naciśnięcie Enter lub przycisku "idź do", przeniesie fokus do wybranego pola.

#### Odczytywanie uwag {#ExcelReportingComments}

<!-- KC:beginInclude -->
Aby odczytać uwagi do aktualnie podświetlonej komórki, naciśnij NVDA+CTRL+C.
W pakiecie Microsoft Office 2016, 365 lub nowszych, komentarze nazywane są teraz uwagami.
<!-- KC:endInclude -->
Wszystkie uwagi można również wyświetlić z okna listy elementów (NVDA+F7).

NVDA może również wyświetlić okno dialogowe w celu dodania uwagi.
NVDA podmienia domyślne okno dialogowe dodawania uwagi przez wzgląd na problemy z dostępnością, jednakże skrót ten jest również dostępny, gdy NVDA nie jest uruchomiony.
<!-- KC:beginInclude -->
Aby dodać lub usunąć uwagę, naciśnij SHIFT+F2.
<!-- KC:endInclude -->

Ten skrót nigdzie nie występuje i nie może być zmieniony z poziomu dialogowego okna "zdarzenia wejścia".

Uwaga! Istnieje również możliwość otwarcia regionu edycji uwag z menu kontekstowego każdej komórki.
Okno to jednak nie będzie dostępne dla NVDA.

W pakiecie Microsoft Office 2016, 365 i nowszych wersjach zostało dodane okno komentarzy stylu.
Okno to jest bardziej dostępne i pozwala M.IN na odpisywanie na komentarze, ETC.
Można je otworzyć z menu kontekstowego każdej komórki.
Uwaga! Komentarze dodane przez to okno nie są równoznaczne z dodaniem uwagi.

#### Odczyt zablokowanych komórek {#ExcelReadingProtectedCells}

Jeśli skoroszyt został zabezpieczony, może nie być możliwe przejście do niektórych komórek, które zostały zablokowane do edycji.
<!-- KC:beginInclude -->
Aby przejść do zablokowanych komórek, przejdź do trybu czytania naciskając NVDA+Spacja, a następnie użyj standardowych klawiszy Excel takich jak klawisze strzałek, aby przechodzić po wszystkich komórkach w aktualnym arkuszu.
<!-- KC:endInclude -->

#### Pola formularzy {#ExcelFormFields}

Arkusze Excel mogą zawierać pola formularzy.
Można uzyskać do nich dostęp przy pomocy listy elementów albo klawiszy nawigacji literami f i Shift+F.
Po przejściu do pola formularza w trybie czytania, można nacisnąć Enter lub Spacja aby je aktywować albo przejść do trybu formularzy dla wykonania dalszej interakcji z polem, zależnie od kontrolki.
Więcej informacji o trybie czytania i nawigacji literami jest dostępne w [rozdziale tryb czytania](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|Przełącz odczyt notatek mówcy |Ctrl+Shift+S |W uruchomionym pokazie slajdów, komenda przełącza między notatkami mówcy albo treścią slajdu. Przełącznik ma wpływ na to co czyta NVDA, nie zmienia treści wyświetlanych na ekranie.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Polecenie |Klawisz |Opis|
|---|---|---|
|Podaj pozostały czas |Ctrl+Shift+R |Podaje czas pozostały do końca aktualnie odtwarzanego utworu.|
|Czas, który upłynął |control+shift+e |Podaje czas, który upłynął w aktualnie odtwarzanej ścieżce.|
|Długość ścieżki |control+shift+t |Podaje długość aktualnie odtwarzanej ścieżki.|

<!-- KC:endInclude -->

Opisane komendy działają tylko dla domyślnego ustawienia formatowania paska stanu odtwarzacza.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|Zgłoś ostatnią wiadomość |NVDA+Ctrl+1-4 |Zgłasza jedną z ostatnich wiadomości, zależnie od naciśniętej cyfry; np. NVDA+Ctrl+2 odczyta przedostatnią wiadomość.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA zawiera rozszerzone wsparcie dla programu Poedit 3.4 lub jego nowszej wersji.

<!-- KC:beginInclude -->

| Działanie |Skrót klawiszowy |Opis|
|---|---|---|
|przeczytaj notatki dla tłumaczy |`control+shift+a` |Odczytuje notatki dla tłumaczy. Po dwukrotnym naciśnięciu, wyświetla notatki w trybie czytania|
|Przeczytaj komentarze |`control+shift+c` |Odczytuje każdy komentarz dła tłumaczy w oknie komentarzy. Po dwukrotnym naciśnięciu, pokazuje komentarz w trybie przeglądu.|
|Czyta stary tekst źródłowy |`control+shift+o` |Czyta stary test źródłowy, jeżeli istnieje. Po dwukrotnym naciśnięciu, pokazuje tekst w trybie przeglądu|
|Czyta uwagi dla tłumaczy |`control+shift+w` |Czyta uwagi dla tłumaczy, jeżeli istnieją. Jeżeli jest naciśnięte dwukrotnie, pokazuje uwagi w trybie przeglądu|

<!-- KC:endInclude -->

### Kindle dla PC {#Kindle}

NVDA obsługuje odczyt i nawigację wewnątrz książek w aplikacji Amazon Kindle dla PC.
Ta funkcjonalność jest dostępna tylko w książkach Kindle zaprojektowanych z właściwością "Czytnik ekranu: obsługiwany", co można sprawdzić na stronie szczegółów książki.

Tryb czytania jest używany do czytania książek.
Jest włączany automatycznie po otwarciu książki lub ustawieniu fokusa na obszarze książki.
Strona zostanie zmieniona automatycznie gdy będzie to konieczne czyli po przesunięciu kursora lub włączeniu polecenia czytaj wszystko.
<!-- KC:beginInclude -->
Ręczne przejście do kolejnej strony nastąpi po wciśnięciu klawisza Page down, a przejście do poprzedniej strony po naciśnięciu Page up.
<!-- KC:endInclude -->

Nawigacja pojedynczymi literami jest obsługiwana dla linków i grafiki, ale wyłącznie w obrębie bieżącej strony.
Nawigacja po linkach uwzględnia również przypisy.

NVDA dostarcza wczesne wsparcie dla odczytu i interaktywnej nawigacji w treści matematycznej dla książek z dostępną matematyką.
Więcej szczegółów w rozdziale [Odczyt treści matematycznej](#ReadingMath).

#### Zaznaczanie tekstu {#KindleTextSelection}

Kindle pozwala na wykonanie różnych akcji na zaznaczonym tekście np. uzyskanie definicji słownikowej, dodanie notatek, skopiowanie tekstu do schowka i przeszukiwanie sieci.
Aby to zrobić, najpierw zaznacz tekst w zwykły sposób dla trybu czytania; np. przy użyciu klawisza Shift i strzałek.
<!-- KC:beginInclude -->
Po zaznaczeniu tekstu, naciśnij klawisz menu kontekstowego albo Shift+F10 aby wyświetlić dostępne opcje pracy z zaznaczeniem.
<!-- KC:endInclude -->
Jeśli to zrobisz bez zaznaczonego tekstu, pokazane zostaną opcje dla słowa pod kursorem.

#### Notatki użytkownika {#KindleUserNotes}

Możesz dodać notatkę dotyczącą słowa lub fragmentu tekstu.
Aby to zrobić, najpierw zaznacz tekst i otwórz opcje zaznaczenia w sposób opisany powyżej.
Następnie wybierz dodanie notatki.

Podczas czytania w trybie czytania, NVDA zgłasza te notatki jako komentarze.

Aby przejrzeć, edytować lub usunąć notatkę:

1. Przesuń kursor do tekstu zawierającego notatkę.
1. Otwórz opcje zaznaczenia w sposób opisany powyżej.
1. Wybierz edycję notatki.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
W widoku tabeli dodanych książek:

| Polecenie |Klawisz |Opis|
|---|---|---|
|Enter |enter |Otwiera wybraną książkę.|
|Menu kontekstowe |klawisz aplikacji |Otwiera menu kontekstowe wybranej książki.|

<!-- KC:endInclude -->

### Konsola systemu Windows {#WinConsole}

NVDA posiada wsparcie dla wiersza poleceń systemu Windows, używanego przez programy takie jak: CMD, Powershell czy podsystem Linuxa.
Okno konsoli posiada stały rozmiar, przeważnie o wiele mniejszy niż bufor wyjściowy.
Gdy nowy tekst jest zapisywany do bufora, okno przewija się w dół co uniemożliwia czytanie tekstu poprzednio widocznego na ekranie.
W wersjach systemu Windows do wersji systemu Windows 11 22H2, tekst w wierszu poleceń, który jest wizualnie niedostępny w oknie nie jest dostępny z poleceniami NVDA do przeglądu tekstu.
A więc, czasami wymagane jest przewijanie okna konsoli.
W nowszych wersjach wiersza poleceń i programie Windows Terminal, istnieje możliwość swobodnego przeglądania bufora konsoli bez konieczności przewijania okna.
<!-- KC:beginInclude -->
Następujące skróty wbudowane w system Windows mogą być przydatne podczas [nawigacji po tekście](#ReviewingText) za pomocą programu NVDA w starszych wersjach wiersza poleceń i konsoli systemu Windows: 

| Nazwa |Skrót klawiszowy |Opis|
|---|---|---|
|Przewiń w górę |CTRL+strzałka w górę |Przewija ekran do góry w celu pokazania wcześniej widocznego tekstu.|
|Przewiń w dół |control+strzałka w dół |Przewija ekran w dół, w celu pokazania późniejszego tekstu.|
|Przewiń do początku bufora |control+home |Przewija ekran na początek bufora|
|Przewiń do końca bufora |control+end |Przewija ekran na koniec bufora.|

<!-- KC:endInclude -->

## Konfigurowanie NVDA {#ConfiguringNVDA}

Większość ustawień NVDA może być zmieniona za pomocą okien dialogowych dostępnych poprzez menu rozwijane opcje z menu NVDA.
Dużą część tych ustawień można znaleźć w wielostronicowym [oknie ustawień NVDA](#NVDASettings).
W oknach dialogowych wszystkich ustawień NVDA, naciśnij przycisk OK, aby zaakceptować zmiany, jakie zostały wprowadzone.
Aby anulować zmiany, naciśnij przycisk Anuluj lub klawisz Escape.
W niektórych oknach można nacisnąć przycisk Zastosuj, aby zmiany zostały uwzględnione natychmiastowo, a okno pozostało otwarte.
Większość ustawień wspiera pomoc kontekstową..
<!-- KC:beginInclude -->
Gdy znajdujesz sie w oknie dialogowym, po naciśnięciu `f1` zostanie otwarty podręcznik użytkownika w odnoszący się do danego ustawienia lub do aktualnego okna dialogowego.
<!-- KC:endInclude -->
Niektóre ustawienia można zmienić również za pomocą klawiszy skrótu, które są wymienione w stosownych rozdziałach poniżej.

### Ustawienia NVDA {#NVDASettings}

<!-- KC:settingsSection: || Działanie | Skróty Klawiszowe Desktopa | Skróty Klawiszowe Laptopa | Opis | -->
NVDA oferuje wiele parametrów konfiguracji, które mogą być zmienione z poziomu okna dialogowego ustawień.
Aby wybór ustawień do zmiany przez użytkownika był łatwiejszy, w oknie dialogowym pokazuje się lista kategorii do wyboru.
Po zaznaczeniu kategorii, wszystkie powiązane ustawienia będą pokazane w dialogu.
Aby przemieszczać się po kategoriach, używaj klawisza `tab` lub `shift+tab` żeby dostać się do listy kategorii, a potem używaj klawiszy strzałek żeby się poruszać po liście.
Po pojedyńczych kategoriach możesz się przemieszczać także o jedną kategorię do przodu naciskając `ctrl+tab`, lub do tyłu naciskając `shift+ctrl+tab`.

Po zmianie jednego lub więcej ustawień, ustawienia mogą być zastosowane używając przycisku zastosuj, a w przypadku jego naciśnięcia okno dialogowe będzie nadal otwarte umożliwiając ci dokonywanie więcej zmian lub wybór innej kategorii.
Aby zapisać ustawienia i zamknąć okno ustawień NVDA, użyj przycisku OK.

Niektóre kategorie ustawień mają przypisane klawisze skrótu.
Po ich naciśnięciu, otwarte zostanie okno ustawień NVDA z wybraną odpowiednią kategorią ustawień.
Domyślnie nie wszystkie kategorie posiadają przypisany skrót klawiszowy.
Jeżeli często używasz kategorii które nie mają przypisanych klawiszy skrótów, możesz użyć [okna dialogowego zdarzenia wejścia](#InputGestures) żeby dodać gest użytkownika, taki jak klawisz skrótu lub gest dotykowy do takiej kategorii.

Kategorie w oknie ustawień NVDA zostaną opisane poniżej.

#### Ogólne {#GeneralSettings}

<!-- KC:setting -->

##### Otwiera ustawienia ogólne {#OpenGeneralSettings}

Skrót: `NVDA+control+g`

Ta kategoria ustawień NVDA  pozwala określić ogólne zachowanie NVDA takie jak język interfejsu i automatyczne sprawdzanie aktualizacji.
Zawiera następujące opcje:

##### Język {#GeneralSettingsLanguage}

Lista rozwijana służąca do wyboru języka komunikatów oraz interfejsu użytkownika NVDA.
Dostępnych jest wiele języków, jednak domyślnie wybrana jest opcja "Domyślne". 
Opcja ta powoduje, że NVDA automatycznie wybiera język interfejsu systemu Windows.

Proszę zauważyć, że NVDA musi zostać zrestartowane po zmianie języka.
Gdy pojawi się okno potwierdzenia, wybierz "uruchom ponownie teraz" lub "Uruchom ponownie później" zależnie od tego, czy chcesz używać nowego języka teraz lub później. Jeśli wybrano "Uruchom ponownie później", ustawienia muszą zostać zapisane (albo ręcznie, albo przy użyciu funkcji zapisywania ustawień przy wyjściu).

##### Zapisz ustawienia przy wyjściu {#GeneralSettingsSaveConfig}

Ta opcja, to pole wyboru. Jeśli jest zaznaczone, to NVDA automatycznie zapisze aktualne ustawienia przy wyjściu z programu.

##### Pokaż opcje przy wyjściu z NVDA {#GeneralSettingsShowExitOptions}

To pole wyboru pozwala zdecydować, czy przy wyjściu z NVDA pojawi się okno dialogowe z pytaniem o akcję, którą chcesz wykonać.
Jeśli zaznaczone, przy próbie wyjścia z NVDA pojawi się pytanie, czy chcesz wyjść, uruchomić ponownie program, uruchomić ponownie z wyłączonymi dodatkami, albo zainstalować oczekujące aktualizacje.
Jeśli niezaznaczone, NVDA zakończy działanie natychmiast.

##### Odtwarzaj dźwięk przy uruchamianiu i zamykaniu NVDA {#GeneralSettingsPlaySounds}

Ta opcja jest polem wyboru, które ustawia odtwarzanie dźwięków przy uruchamianiu i zamykaniu NVDA.

##### Poziom logowania {#GeneralSettingsLogLevel}

Pole rozwijalne pozwalające na ustawienie poziomu logowania (ile czynności wykonanych przez użytkownika ma trafić do pliku logów).
Na ogół użytkownik nie powinien zmieniać tego ustawienia, ponieważ zapisywane jest niezbyt wiele informacji.
Jeśli jednak chcesz przesłać zgłoszenie błędu, albo całkowicie wyłączyć zapisywanie dziennika, ta opcja może być użyteczna.

Dostępne poziomy logowania, to:

* Wyłączone: poza krótką informacją przy uruchamianiu, NVDA nie będzie zapisywał niczego podczas działania.
* Info: NVDA będzie zapisywać podstawowe informacje, takie jak informacje startowe i inne użyteczne dla programistów.
* Ostrzeżenie debugowania: Komunikaty ostrzegawcze, które nie są spowodowane poważnymi błędami, będą zapisywane.
* Wejście/wyjście: wejście z klawiatury a także wyjście mowy i brajla będą logowane.
Jeżeli boisz się o swoją prywatność, nie włączaj tej opcji.
* Debugowanie: Poza wiadomościami debugowania, wejściem klawiatury i mowy dodatkowe informacje będą zapisywane.
Tak samo jak w poprzednim, jeżeli boisz się o swoją prywatność, nie włączaj tej opcji.

##### Automatycznie uruchom NVDA po zalogowaniu się do systemu Windows {#GeneralSettingsStartAfterLogOn}

Jeśli ta opcja jest włączona, NVDA uruchomi się automatycznie zaraz po zalogowaniu się do systemu.
Opcja jest dostępna tylko dla zainstalowanych kopii NVDA.

##### Użyj NVDA podczas logowania Windows (wymaga uprawnień administratora) {#GeneralSettingsStartOnLogOnScreen}

Jeśli logujesz się do systemu podając nazwę użytkownika i hasło, to zaznaczenie tej opcji sprawi, że NVDA będzie uruchamiał się automatycznie na ekranie logowania do systemu.
Ta opcja jest dostępna tylko dla zainstalowanych kopii NVDA.

##### Używaj obecnie zapisanych ustawień na ekranie logowania i innych zabezpieczonych ekranach (wymaga uprawnień administratora) {#GeneralSettingsCopySettings}

Naciśnięcie przycisku "Używaj zapisanych ustawień NVDA na ekranie logowania i innych zabezpieczonych ekranach" kopiuje  zapisane wcześniej ustawienia użytkownika do katalogu systemowej konfiguracji NVDA, której NVDA używa na ekranie logowania do Windows, ekranie kontroli konta użytkownika (UAC), oraz innych [zabezpieczonych ekranach](#SecureScreens).
Aby skopiować w ten sposób wszystkie swoje ustawienia, po pierwsze zapisz aktualną konfigurację przy użyciu klawisza skrótu Ctrl+NVDA+c albo polecenia menu NVDA "Zapisz ustawienia".
Ta opcja jest dostępna tylko dla zainstalowanych kopii NVDA.

##### Sprawdzaj automatycznie, czy jest nowa wersja {#GeneralSettingsCheckForUpdates}

Gdy to pole wyboru jest zaznaczone, NVDA będzie automatycznie sprawdzał dostępność aktualizacji programu i poinformuje, jeżeli jakaś będzie dostępna.
Możesz również sprawdzać dostępność aktualizacji ręcznie, poleceniem "Sprawdź aktualizacje" w menu Pomoc NVDA.
Podczas automatycznego lub ręcznego sprawdzania dostępności aktualizacji, konieczne jest przesyłanie przez NVDA  pewnych informacji do serwera aktualizacji, aby otrzymać prawidłową aktualizację dla konkretnego systemu.
Poniższe informacje są zawsze przesyłane: 

* Aktualna wersja NVDA
* Wersja systemu operacyjnego
* Czy system operacyjny jest 64, czy 32 bitowy

##### Zezwól NVAccessowi na zbieranie statystyk używania programu {#GeneralSettingsGatherUsageStats}

Gdy włączone, NV Access będzie używać informacji przesyłanych przy sprawdzaniu dostępności aktualizacji, dla określania liczby użytkowników NVDA włączając w to informacje demograficzne, takie jak kraj i system operacyjny.
O ile twój adres IP będzie użyty do określenia kraju przy sprawdzaniu aktualizacji, to nie jest przechowywany.
Prócz niezbędnych informacji umożliwiających sprawdzanie aktualizacji,  poniższe dodatkowe informacje są aktualnie przesyłane:

* Język interfejsu NVDA
* Czy dana kopia NVDA jest przenośna czy zainstalowana
* Nazwa aktualnie używanego syntezatora mowy (włączając w to nazwę dodatku, z którego pochodzi sterownik)
* Nazwa aktualnie używanej linijki brajlowskiej (włączając w to nazwę dodatku, z którego pochodzi sterownik)
* Brajlowska tablica wyjścia (jeśli brajl jest używany)

Te informacje znacząco pomagają NV Access w priorytyzowaniu dalszych prac nad NVDA.

##### Powiadamiaj o oczekującej aktualizacji przy starcie {#GeneralSettingsNotifyPendingUpdates}

Gdy zaznaczone, NVDA poinformuje o oczekującej przy starcie aktualizacji, oferując możliwość jej zainstalowania.
Można ręcznie zainstalować oczekującą aktualizację w oknie opcji wyjścia z NVDA (jeśli włączone),  z menu NVDA, lub wykonując sprawdzenie aktualizacji z menu pomoc.

#### Ustawienia mowy {#SpeechSettings}

<!-- KC:setting -->

##### Otwiera ustawienia mowy {#OpenSpeechSettings}

Skrót: `NVDA+control+v`

ustawienia mowy w oknie głównym programu NVDA zawierają zarówno opcje zmiany syntezatora jak i jego parametrów.
Szybszy alternatywny sposób regulacji parametrów mowy z dowolnego miejsca, możesz znaleźć w rozdziale [Szybka zmiana ustawień syntezatora](#SynthSettingsRing).

Ta kategoria ustawień, zawiera następujące ustawienia:

##### Zmień syntezator {#SpeechSettingsChange}

Pierwsza opcja w kategorii ustawień mowy, to przycisk "Zmień...". Przycisk aktywuje [okno wyboru syntezatora](#SelectSynthesizer), pozwalające wybrać aktywny syntezator mowy i urządzenie wyjściowe.
Okno otwiera się na oknie preferencji NVDA.
Zapisanie lub anulowanie wyboru, spowoduje powrót do okna preferencji NVDA.

##### Głos {#SpeechSettingsVoice}

Pole rozwijalne służące do wyboru jednego z głosów dostępnych dla syntezatora aktualnie wybranego w NVDA.
Za pomocą strzałek możesz przechodzić kolejno przez wszystkie głosy słuchając ich brzmienia.
Strzałkami w lewo i w górę przesuwasz się w górę listy, a strzałkami w prawo i w dół przesuwasz się w dół.

##### Wariant {#SpeechSettingsVariant}

Jeśli korzystasz z dołączonego do NVDA syntezatora eSpeak NG, pole rozwijalne Wariant umożliwia zmianę brzmienia dla aktualnie używanego głosu.
Warianty głosu Espeak NG to w zasadzie różne głosy, jako że modyfikują one parametry brzmienia głosu Espeak NG.
Niektóre warianty będą brzmieć jak mężczyzna, inne jak kobieta, a jeszcze inne - jak żaba.
Jeżeli używasz zewnętrznego syntezatora mowy, możliwa może być zmiana tej opcji również dla niego.

##### Prędkość {#SpeechSettingsRate}

Ta opcja pozwala na zmianę prędkości głosu.
Jest to suwak służący do zmiany prędkości czytania w skali od 0 do 100, (0 oznacza tempo najwolniejsze, 100 najszybsze).

##### Podkręć szybkość {#SpeechSettingsRateBoost}

Jeśli ta opcja zostanie włączona, a syntezator mowy ją wspiera, prędkość będzie znacznie zwiększona.

##### Wysokość {#SpeechSettingsPitch}

Ta opcja pozwala na zmianę wysokości aktualnego głosu.
Jest to suwak, który zmienia wysokość głosu w skali od 0 do 100, (0 oznacza głos najniższy, 100 najwyższy).

##### Głośność {#SpeechSettingsVolume}

Jest to suwak służący do zmiany natężenia głosu w skali od 0 do 100, (0 oznacza głos najcichszy, 100 najgłośniejszy).

##### Modulacja {#SpeechSettingsInflection}

Jest to suwak służący do zmiany intonacji (unoszenia i opadania) głosu w skali od 0 do 100, (0 oznacza głos najbardziej monotonny, 100 najbardziej melodyjny). (Zmiana modulacji możliwa jest jedynie w przypadku syntezatora eSpeak NG.)

##### automatycznie zmieniaj język {#SpeechSettingsLanguageSwitching}

To pole wyboru przełącza ustawienie automatycznej zmiany języka syntezatora w locie. Opcja ta działa tylko wówczas, gdy odpowiedni język jest zadeklarowany w kodzie dokumentu. 
Domyślnie pole to jest zaznaczone.

##### Automatycznie zmieniaj dialekt {#SpeechSettingsDialectSwitching}

To pole wyboru pozwala ustalić, czy dialekt powinien być zmieniany w trakcie czytania. 
Dla przykładu, jeśli czytamy dokument angielski głosem angielski amerykański, a dokument zawiera oznaczenia części tekstu jako angielski brytyjski, jeśli ta funkcja jest włączona - syntezator zmieni również sposób akcentowania.
Ta opcja jest domyślnie wyłączona.

<!-- KC:setting -->

##### poziom interpunkcji/symboli {#SpeechSettingsSymbolLevel}

Skrót Klawiszowy: NVDA+p

Ustawienie pozwala wybrać liczbę znaków i symboli, które powinny być wymawiane. 
Jeśli ustawienie ma wartość "Wszystko", wszystkie symbole będą odczytywane.
Dotyczy to wszystkich syntezatorów, nie tylko tego aktywnego w tym momencie.

##### Ufaj językowi głosu przetwarzając znaki i symbole {#SpeechSettingsTrust}

Domyślnie włączona, ta opcja informuje NVDA, że bieżący głos prawidłowo przetwarza znaki i symbole.
Jeśli okaże się, że interpunkcja jest odczytywana w nieprawidłowym języku dla konkretnego głosu lub syntezatora, możesz tę opcję wyłączyć, aby zmusić NVDA do używania globalnie ustawionego języka.

##### Używaj bazy danych Unicode do przetwarzania znaków i symboli (włączając w to emoji) {#SpeechSettingsCLDR}

Gdy to pole wyboru jest zaznaczone, NVDA będzie używał dodatkowych słowników wymowy  symboli.
Te słowniki zawierają opisy symboli (w szczególności emoji) dostarczane przez [Konsorcjum Unicode](https://www.unicode.org/consortium/) jako część ich [wspólnego repozytorium danych lokalnych](http://cldr.unicode.org/).
Jeśli chcesz, by NVDA wymawiał opisy znaków emoji w oparciu o te dane, powinieneś włączyć tę opcję.
Jeśli używasz syntezatora, który obsługuje wypowiadanie emoji, możesz chcieć wyłączyć to pole wyboru.

Ręcznie dodane lub zmienione opisy, są zapisane jako część twoich ustawień użytkownika.
Dlatego, jeśli zmienisz opis konkretnego znaku emoji, twój własny opis będzie wypowiadany dla tego znaku niezależnie czy ta opcja jest włączona.
Możesz dodawać, edytować lub usuwać opisy symboli w oknie NVDA [Wymowa symboli / interpunkcja](#SymbolPronunciation).

W celu przełączenia odczytywania znaków Unicode z dowolnego miejsca, wymagane jest przypisanie odpowiedniego skrótu klawiszowego w oknie [zdarzenia wejścia dialog](#InputGestures).

##### Wyższy głos dla wielkich liter {#SpeechSettingsCapPitchChange}

To pole edycji pozwala ustawić o ile zmieni się wysokość głosu podczas czytania dużej litery. 
Wartość podajemy w procentach - liczba dodatnia oznacza podwyższenie wysokości, liczba ujemna - obniżenie.
Wartość 0 oznacza brak zmiany wysokości.
Przeważnie, NVDA podnosi wysokość głosu w przypadku wykrycia dużej litery, jednakże nie wszystkie syntezatory wspierają tę funkcję.
W przypadku braku wsparcia dla zmiany wysokości możesz użyć funkcji [Czytaj "duże" przed dużymi literami](#SpeechSettingsSayCapBefore) lub/i [ Odtwarzaj dźwięk dla dużych liter](#SpeechSettingsBeepForCaps).

##### Czytaj "duże" przed wielkimi literami {#SpeechSettingsSayCapBefore}

Jeśli zaznaczysz tę opcję, NVDA będzie sygnalizować wielkie litery czytając słowo "Duże", dla każdej litery wypowiadanej jako pojedynczy znak, np. podczas literowania.

##### Dźwięk dla dużych liter {#SpeechSettingsBeepForCaps}

Jeśli zaznaczysz tę opcję, NVDA będzie sygnalizować pojedyncze wielkie litery za pomocą krótkiego dźwięku.

##### wykrywanie wymowy {#SpeechSettingsUseSpelling}

Niektóre słowa zawierają tylko jeden znak, lecz wymowa różni się w zależności od tego, czy wymawiamy daną literę jak słowo, czy jako literę samą w sobie.
Przykładowo w języku angielskim "a" jest literą lub słowem i jest przy tym różnie wymawiana.
To ustawienie sprawia, że syntezatory mowy uwzględniają ten fakt. 
Ta funkcjonalność jest wspierana w większości syntezatorów.

Ta opcja na ogół powinna być włączona.
Niektóre syntezatory pracujące w standardzie Microsoft Speech API (SAPI)  nie obsługują prawidłowo tej funkcjonalności i zachowują się dziwnie, gdy jest ona włączona.
Jeśli napotykasz na problemy z wymową pojedynczych znaków, spróbuj wyłączyć tę opcję.

##### Opisy po nazwie liter podczas ruchu kursora {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Włączone, Wyłączone|
|Domyślnie |Wyłączone|

Gdy ta opcja jest włączona, NVDA wypowie opis znaku podczas poruszania się po znakach.

Na przykład, podczas przeglądu linii po znakach, kiedy litera "b" zostanie przeczytana NVDA powie "barbara" po jednosekundowej przerwie.
To może być użyteczne jeżeli nie można odróżnić wymowę niektórych znaków, albo może to być korzystne użytkownikom z wadami słuchu.

Opóźniony opis znaków nie będzie wypowiedzony jeżeli zostanie wypowiedzony inny tekst w tym czasie, lub jeżeli zostanie naciśnięty klawisz `control`.

##### Tryby dostępne podczas przełączania trybów mowy {#SpeechModesDisabling}

Ta lista z polami wyboru umożliwia regulowanie które [tryby mowy](#SpeechModes) będą dostępne podczas przełączania między nimi za pomocą skrótu `NVDA+s`.
Wyłączone tryby są wykluczone.
Domyślnie, wszystkei tryby są dostępne.

Na przykłąd, jeżeli nie potrzebujesz trybów "dźwięk" i "wyłączone" odznacz je, i zostaw zaznaczone tryby "mowa" i "na żądanie".
Miewaj na uwadze, że powinieneś zaznaczyć dwa tryby.

#### Wybór syntezatora {#SelectSynthesizer}

<!-- KC:setting -->

##### Otwiera okno dialogowe wybór syntezatora {#OpenSelectSynthesizer}

Skrót: `NVDA+control+s`

Okno dialogowe "Syntezator...", pod przyciskiem "Zmień..." w kategorii mowa w oknie preferencji NVDA, pozwala wybrać używany przez NVDA syntezator mowy.
Po zaznaczeniu wybranego syntezatora, naciśnij przycisk "Ok" a NVDA załaduje go.
Jeśli pojawi się błąd przy ładowaniu wybranego syntezatora, program NVDA powiadomi o tym wyświetlając komunikat i będzie używał syntezatora aktywnego poprzednio.

##### Syntezator {#SelectSynthesizerSynthesizer}

Ta opcja pozwala na wybór odpowiedniego syntezatora mowy, który będzie używany przez NVDA.

Listę Syntezatorów, które obsługuje NVDA zobaczysz w rozdziale [Obsługiwane Syntezatory Mowy](#SupportedSpeechSynths).

Jeden specjalny element, który zawsze pojawi się na tej liście, to "bez mowy", który pozwala używać NVDA całkowicie bez komunikatów głosowych.
Może to być przydatne dla kogoś chcącego używać NVDA tylko z monitorem brajlowskim albo dla widzących twórców oprogramowania, którzy chcą używać wyłącznie funkcji "Podgląd mowy".

#### Szybka zmiana ustawień syntezatora {#SynthSettingsRing}

Jeśli chcesz szybko zmienić ustawienia mowy bez wchodzenia do kategorii Mowa okna preferencji NVDA, istnieją klawisze poleceń, które pozwalają w każdej chwili ustawiać najczęściej zmieniane ustawienia mowy:
<!-- KC:beginInclude -->

| Działanie |Skróty Klawiszowe Desktopa |Skróty Klawiszowe Laptopa |Opis|
|---|---|---|---|
|Do następnych ustawień głosu |NVDA+Ctrl+Strzałka w prawo |NVDA+Ctrl+Shift+Strzałka w prawo |Przechodzi do następnego parametru ustawień syntezatora, wracając do pierwszego po przejściu za ostatni.|
|Do poprzednich ustawień głosu |NVDA+Ctrl+Strzałka w lewo |NVDA+Shift+Ctrl+Strzałka w lewo |Przechodzi do poprzedniego parametru ustawień syntezatora wracając do ostatniego po przejściu przed pierwszy.|
|Zwiększ parametr ustawień głosu |NVDA+Ctrl+Strzałka w górę |NVDA+Ctrl+Shift+Strzałka w górę |Zwiększa aktualnie wybrany parametr ustawień syntezatora np. przyśpiesza prędkość, wybiera następny głos, zwiększa głośność.|
|Zwiększ aktualne ustawienie większym krokiem |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Zwiększa wwartość aktualnego ustawienia większym krokiem. Na przykład, gdy znajdujesz się na ustawieniu głosu, zmienisz je o dwadzieścia głosó wprzód; gdy znajdujesz się na ustawieniach suwaka (prędkość, wysokość, itd) wartość zwiększy się o dwadzieścia procent|
|Zmniejsz parametr ustawień głosu |NVDA+Ctrl+Strzałka w dół |NVDA+Ctrl+Shift+Strzałka w dół |Zmniejsza aktualnie wybrany parametr ustawień syntezatora. Na przykład: zmniejsza szybkość, wybiera poprzedni głos, zmniejsza głośność.|
|zmniejsz aktualne ustawienie większym krokiem |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Zmniejsza wwartość aktualnego ustawienia większym krokiem. Na przykład, gdy znajdujesz się na ustawieniu głosu, zmienisz je o dwadzieścia głosó w tył; gdy znajdujesz się na ustawieniach suwaka (prędkość, wysokość, itd) wartość zmniejszy się o dwadzieścia procent|

<!-- KC:endInclude -->

#### Brajl {#BrailleSettings}

Kategoria brajl w oknie ustawień NVDA zawiera opcje umożliwiające zmianę kilku aspektów wprowadzania i wyświetlania brajla.
Ta kategoria zawiera następujące ustawienia:

##### Zmień monitor brajlowski {#BrailleSettingsChange}

Pierwsza opcja w kategorii ustawień brajla, to przycisk "Zmień...". Przycisk aktywuje [okno wyboru monitora brajlowskiego](#SelectBrailleDisplay), pozwalające wybrać aktywną linijkę brajlowską.
Okno otwiera się na oknie preferencji NVDA.
Zapisanie lub anulowanie wyboru, spowoduje powrót do okna preferencji NVDA.

##### Tablica wyjścia {#BrailleSettingsOutputTable}

Następną opcją, na którą natrafisz w tej kategorii preferencji NVDA, jest lista rozwijana "Tabela wyjścia".
Możesz tu znaleźć tablice brajlowskie dla różnych języków, standardów i skrótów brajlowskich.
Wybrana tablica będzie używana do translacji tekstu przed jego wyświetleniem na twoim monitorze brajlowskim.
Między elementami tej listy przełączaj się przy użyciu klawiszy strzałek.

##### Tablica wprowadzania {#BrailleSettingsInputTable}

W uzupełnieniu do poprzedniego ustawienia, następnym znajdującym się po nim jest lista rozwijana "Tabela wprowadzania".
Wybrana tablica będzie używana do translacji na postać tekstu komputerowego znaków wprowadzanych na klawiaturze twojego monitora brajlowskiego.
Między elementami tej listy przełączaj się przy użyciu klawiszy strzałek.

Zwróć uwagę, że ta funkcja jest przydatna tylko wówczas, gdy twój monitor brajlowski posiada klawiaturę w stylu Perkins, a funkcja wprowadzania jest obsługiwana przez sterownik monitora brajlowskiego.
Jeśli wprowadzanie nie jest możliwe na monitorze posiadającym klawiaturę, będzie to zaznaczone w rozdziale [Obsługiwane monitory brajlowskie](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Tryb brajla {#BrailleMode}

Skrót: `NVDA+alt+t`

Ta opcja umożliwia wybór wspośród dostępnych trybów brajla.

W aktualnym momencie dostępne są dwa tryby brajla, "śledzenie kursoru" i "wyświetlanie mowy".

Gdy śledzenie kursoru jest włączone, monitor brajlowski będzie śledził kursor systemu/obiekt nawigatora oraz nawigację obiektową, w zależności od przywiązania brajla.

Gdy "wyświetlanie mowy jest" wybrane, monitor brajlowski wyświetli to, co NVDA wymawia, lub co by wymówił, jeżeli tryb mowy byłby ustawiony na "mowa"

##### Rozwiń słowo pod kursorem do brajla komputerowego {#BrailleSettingsExpandToComputerBraille}

Ta opcja umożliwia wyświetlenie słowa pod kursorem w formie nieskróconego brajla komputerowego.

##### Pokaż kursor {#BrailleSettingsShowCursor}

Ta opcja pozwala włączać i wyłączać kursor brajlowski.
Ma zastosowanie do kursora systemu i kursora przeglądu, ale nie dotyczy oznaczania zaznaczenia.

##### Migotanie kursora {#BrailleSettingsBlinkCursor}

Ta opcja umożliwia migotanie kursora brajlowskiego.
Jeśli migotanie jest wyłączone, punkty tworzące kursor brajlowski będą stale wysunięte.
Ta opcja nie ma wpływu na wskaźnik zaznaczenia, są to zawsze punkty 7 i 8 bez migotania.

##### Tempo migania kursora (ms) {#BrailleSettingsBlinkRate}

Ta opcja jest polem liczbowym, które pozwala zmienić częstotliwość migania kursora wyrażoną w milisekundach.

##### Kształt kursora dla fokusa {#BrailleSettingsCursorShapeForFocus}

Ta opcja pozwala wybrać kształt (wzorzec punktowy) kursora brajlowskiego, gdy brajl jest związany z fokusem.
Ustawienie nie ma wpływu na wskaźnik zaznaczenia, są to zawsze punkty 7 i 8 bez migotania.

##### Kształt kursora dla przeglądu {#BrailleSettingsCursorShapeForReview}

Ta opcja pozwala wybrać kształt (wzorzec punktowy) kursora brajlowskiego, gdy brajl jest związany z kursorem przeglądu.
Ustawienie nie ma wpływu na wskaźnik zaznaczenia, są to zawsze punkty 7 i 8 bez migotania.

##### Pokazuj wiadomości {#BrailleSettingsShowMessages}

Jest to lista rozwijana która umożliwia  włączenie i wyłączenie pokazywania wiadomości na monitorze brajlowskim a także ustawianie czasu, po którym te wiadomości powinny zniknąć.

Aby móc ustawić pokazywanie wiadomości globalnie, przydziel zdarzenie wejścia używając [okna dialogowe zdarzenia wejścia](#InputGestures).

##### Czas wygasania komunikatów {#BrailleSettingsMessageTimeout}

To ustawienie jest polem liczbowym określającym w sekundach, jak długo na monitorze brajlowskim są wyświetlane komunikaty programu NVDA.
Komunikat NVDA znika natychmiast po naciśnięciu klawisza CURSOR ROUTING na monitorze brajlowskim. Ponowne naciśnięcie klawisza przywraca komunikat.
Ta opcja jest widoczna gdy wartość opcji "pokazuj wiadomości" jest ustawiona na "użyj wygasania".

<!-- KC:setting -->

##### Powiązanie brajla {#BrailleTether}

Skrót Klawiszowy: NVDA+Ctrl+T

Ta opcja pozwala wybrać, czy monitor brajlowski będzie podążać za fokusem / kursorem systemowym, czy obiektem nawigatora/punktem przeglądu, albo oboma.
Gdy ustawione jest "automatycznie", NVDA będzie domyślnie podążać za fokusem i kursorem systemu.
W takim przypadku, gdy pozycja obiektu nawigatora lub kursora przeglądu zmieni się na skutek interakcji użytkownika, NVDA tymczasowo powiąże brajl z kursorem przeglądu, do czasu, gdy zmieni się pozycja fokusa lub kursora systemowego.
Jeśli chcesz, żeby NVDA śledziła kursor systemowy wraz z fokusem, Musisz skonfigurować brajl powiązany do fokusu.
W takim przypadku NVDA nie będzie śledziła nawigację obiektową  oraz kursor przeglądu podczas przeglądu obiektów.
Jeśli chcesz żeby NVDA śledziła nawigację obiektową zamiast kursoru systemowego, musisz skonfigurować NVDA tak, żeby brajl był powiązany do przeglądu.
W takim przypadku brajl nie będzie śledził kursora i fokusu systemowego.

##### Przenoś kursor systemowy podczas przywoływania kursoru przeglądu {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (nigdy), nigdy, tylko podczas przywoływania automatycznego, zawsze|
|Domyślnie |Nigdy|

To ustawienie służy do regulowania przemieszczania kursora systemowego za pomocą przycisku routing.
Domyślnie, to ustawienie jest postawione na nigdy, co oznacza, że  klawisz routing nie będzie przenosił kursora systemowego podczas przemieszczania kursora przeglądu.

Kiedy ta opcja jest ustawiona na zawsze, i opcja [przywiązanie brajla](#BrailleTether) jest ustawiona na "automatycznie" lub "do kursora przeglądu", naciśnięcie przycisku routing spowoduje przeniesienie kursora systemowego lub fokusu gdy jest to wspierane.
Gdy aktualnym trybem jest [przegląd ekranu](#ScreenReview), nie istnieje kursor fizyczny.
W takim przypadku, NVDA spróbuje sfokusować  obiekt do którego próbujesz przywołać routing.
To także stosuje się do [przeglądu obiektu](#ObjectReview).

Możesz także ustawić tą opcje żeby kursor się przemieszczał podczas automatycznego przywiązania.
W takim przypadku, naciśnięcie klawisza routing spowoduje przeniesienie kursora systemowego lub do fokusu, gdy NVDA jest przywołana do kursora przeglądu automatycznie. Nie będzie żadnego przemieszczania gdy gdy fokus jest ręcznie przywiązany do do kursoru przeglądu.

Ta opcja pokazuje się tylko jeżeli "[przywiązanie brajla](#BrailleTether)" jest ustawione na "automatyczne" lub "do przeglądu".

Aby ustawić opcję "Przenoś kursor systemowy podczas przywoływania kursoru przeglądu" z jakiegokolwiek miejsca, przydziel gest użytkownika używając okna dialogowego [zdarzenia wejścia dialog](#InputGestures).

##### czytaj akapitami {#BrailleSettingsReadByParagraph}

Gdy zaznaczysz to pole, monitor brajlowski będzie wyświetlać tekst akapitami, nie liniami. 
Ponadto, komendy  przejścia między liniami będą przenosić między akapitami. 
Oznacza to, że nie musisz przewijać wyświetlania na końcu każdej linii, nawet gdy na samym monitorze brajlowskim  zmieści się więcej tekstu. 
Może być to użyteczne do płynnego czytania większych porcji tekstu. 
Opcja domyślnie jest wyłączona.

##### Unikaj rozdzielania słów kiedy możliwe {#BrailleSettingsWordWrap}

Gdy włączone,słowo zbyt długie, aby zmieścić się na końcu wyświetlacza, nie zostanie podzielone.
Zamiast tego, pojawi się kilka spacji na końcu wyświetlacza.
Po przesunięciu wyświetlania, możliwe będzie przeczytanie całego słowa.
Nazywa się to czasem "zawijaniem słów".
Jeśli słowo jest zbyt długie, by samo zmieściło się na wyświetlaczu, musi zostać podzielone.

Jeśli opcja jest wyłączona, wyświetlona zostanie część słowa, tak duża jak to możliwe, a reszta zostanie obcięta.
Po przesunięciu wyświetlacza, możliwe będzie przeczytanie reszty słowa.

Włączenie tej opcji umożliwia bardziej płynne czytanie, ale zmusza do częstszego przewijania wyświetlacza.

##### Kontekstowa prezentacja fokusa {#BrailleSettingsFocusContextPresentation}

Opcja pozwala wybrać, jaką informację kontekstową NVDA zaprezentuje na monitorze brajlowskim, gdy fokus znajdzie się na obiekcie.
Informacja kontekstowa odnosi się do hierarchii obiektów zawierających fokus.
Dla przykładu, jeśli znajdzie się on na elemencie listy, ten element stanie się częścią listy nadrzędnej.
Lista ta może się znajdować wewnątrz okna dialogowego, etc.
Więcej informacji o hierarchii obiektów w NVDA znajduje się w sekcji [Nawigacja w chierarchii obiektów](#ObjectNavigation).

Gdy ustawiono na wypełnianie wyświetlacza zmianami kontekstowymi, NVDA spróbuje wyświetlić tak wiele informacji kontekstowych, ile zmieści się na monitorze brajlowskim, ale tylko dla zmienionych części kontekstu.
W przykładzie powyżej, oznacza to, że zmiana punktu uwagi na listę, spowoduje pokazanie przez NVDA elementu listy na monitorze brajlowskim.
Ponadto, jeśli pozostała wystarczająca ilość miejsca na monitorze brajlowskim, NVDA spróbuje pokazać, że  ten element listy jest częścią listy nadrzędnej.
Jeśli będziesz przemieszczać się po liście klawiszami strzałek, zakłada się, że masz świadomość, iż znajdujesz się ciągle w obrębie tej samej listy nadrzędnej.
Dlatego też, dla pozostałych elementów listy, które otrzymają fokus, NVDA pokaże tylko element listy.
Aby przeczytać kontekst ponownie (np. że jesteś na liście będącej częścią okna dialogowego), musisz przewinąć wyświetlacz brajlowski wstecz.

Jeśli ta opcja jest ustawiona aby zawsze wypełniała wyświetlacz, NVDA będzie próbował dostarczać tak wiele informacji kontekstowej jak to możliwe na używanym monitorze brajlowskim, niezależnie od tego, czy informacja kontekstowa była wyświetlana wcześniej.
Zaletą jest, że NVDA będzie dostarczał maksymalną ilość informacji na monitorze brajlowskim.
Minusem tego rozwiązania jest różnica pozycji na monitorze brajlowskim, w której będzie się wyświetlał fokus.
Może to utrudnić przeglądanie długiej listy elementów, ponieważ będzie konieczne ciągłe poszukiwanie miejsca, gdzie zaczyna się aktualny element.
Było to domyślne zachowanie w NVDA 2017.2 i starszych.

Jeśli ustawisz tę opcję, aby informacja kontekstowa była prezentowana tylko przy przewijaniu monitora wstecz, NVDA nie będzie domyślnie pokazywał informacji kontekstowych.
W przykładzie powyżej, NVDA pokaże, że fokus znajduje się na elemencie listy.
Aby przeczytać informację kontekstową, konieczne będzie przewinięcie monitora brajlowskiego wstecz.

Aby w dowolnym miejscu przełączyć kontekstową prezentację fokusa, można przypisać własne zdarzenie wejścia przy pomocy [okna ustawień zdarzenia wejścia](#InputGestures).

##### Przerwij mowę podczas przewijania {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (włączone), włączone, wyłączone|
|Domyślnie |włączone|

Ta opcja reguluje przerwanie mowy podczas przewijania tekstu na monitorze brajlowskim wstecz albo wprzód.
Polecenia poprzedniego następnego wiersza zawsze przerywają mowę.

Nadchodząca mowa może przeszkadzać podczas czytania brajla.
Z tego powodu opcja jest domyślnie włączona, przerywając mowę podczas przewijania tekstu.

Wyłączenie tej opcji umożliwia słyszenie mowy podczas symultanicznego odczytu tekstu.

##### Pokaż zaznaczenie {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |domyślnie (włączone), włączone, wyłączone|
|Domyślnie |włączone|

Ta opcja reguluje pokazywanie indykatora zaznaczenia na monitorze brajlowskim.
Ta opcja jest domyślnie włączona, co oznacza że indykator jest pokazywany.
Indykator zaznaczenia może zaburzać uwagę podczas czytania.
Wyłączenie tej opcji może poprawić czytelność.

Aby włączać i wyłączać pokazywanei zaznaczenia z jakiegokolwiek miejsca, skojarz zdarzenie wejścia używając [okno dialogowe zdarzeń wejścia](#InputGestures).

#### Wybór monitora brajlowskiego {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Otwiera okno dialogowe wybor monitora brajlowskiego {#OpenSelectBrailleDisplay}

Skrót: `NVDA+control+a`

Okno wyboru monitora brajlowskiego jest otwierane po kliknięciu przycisku "Zmień..."  w kategorii brajl preferencji NVDA, pozwala wybrać, której linijki brajlowskiej NVDA ma używać do generowania komunikatów w brajlu.
Po wybraniu monitora brajlowskiego, naciśnij Ok i NVDA uruchomi wybraną linijkę.
Jeśli wystąpi błąd uruchamiania sterownika, NVDA powiadomi o tym odpowiednim komunikatem i powróci do używania poprzedniego monitora brajlowskiego, jeśli jakiś był wcześniej używany .

##### Monitor brajlowski {#SelectBrailleDisplayDisplay}

Zawartość listy monitorów brajlowskich jest zależna od tego, jakie sterowniki monitorów brajlowskich są zainstalowane w twoim systemie.
Na liście przemieszczasz się między elementami przy użyciu klawiszy strzałek.

Opcja automatyczna pozwoli NVDA wyszukiwać w tle wiele z obsługiwanych linijek.
Gdy ta funkcja jest włączona i podłączysz obsługiwaną linijkę przez USB lub bluetooth, NVDA automatycznie połączy się z tym urządzeniem.

"Bez brajla" oznacza, że nie używasz monitora brajlowskiego.

Więcej na temat obsługiwanych monitorów brajlowskich, oraz informacje, które z nich obsługują automatyczne wykrywanie, znajdziesz w rozdziale [Obsługiwane Monitory Brajlowskie](#SupportedBrailleDisplays).

##### Monitory brajlowskie do automatycznego wykrywania {#SelectBrailleDisplayAutoDetect}

Gdy monitor brajloski jest ustawiony na "automatyczny", pola wyboru na tej liście umożliwią wykluczenie monitorów brajlowskich z procesu automatycznego wykrywania.
To umożliwia wykluczenie monitorów brajlowskich, których nie używasz często.
Na przykład, jeżeli używasz tylko monitora brajlowskiego, który wymaga sterownika baum do jego funkcjonowania, możesz zostawić włączony sterownik baum, ap pozostałe wyłączyć.

Domyślnie włączone są wszystkie sterowniki wspierające automatyczne wykrywanie monitorów brajlowskich.
Każdy nowy sterownik, dodany w nowej wersji NVDA lub dostarczany jako dodatek, będzie domyślnie włączony.

Możesz sprawdzić, czy twój monitor brajlowski wspiera automatyczne wykrywanie monitorów brajlowskich w rozdziale [wspierane monitory brajlowskie](#SupportedBrailleDisplays).

##### port {#SelectBrailleDisplayPort}

Ta opcja, jeśli jest dostępna, pozwala określić jaki port lub typ połączenia będzie użyty do komunikacji z monitorem brajlowskim.
Jest to lista rozwijana, zawierająca elementy zależne od wybranego urządzenia.

Domyślnie NVDA używa automatycznego wykrywania portów, co oznacza, że połączenie z monitorem brajlowskim zostanie nawiązane automatycznie poprzez wyszukanie monitora wśród dostępnych w systemie urządzeń Bluetooth i USB.
Dla niektórych monitorów brajlowskich, będzie możliwe dokonanie wyboru, który port ma być użyty.
Najczęściej spotykane możliwości to "Automatycznie" (opisana powyżej procedura automatycznego wykrywania urządzenia), "USB", "Bluetooth" i porty szeregowe, jeśli twój monitor brajlowski obsługuje ten rodzaj transmisji.

Ta lista rozwijana nie pojawi się, jeśli twój monitor brajlowski obsługuje wyłącznie automatyczne wykrywanie portu.

Możesz zajrzeć do sekcji omawiającej twój monitor brajlowski w rozdziale [Obsługiwane monitory brajlowskie](#SupportedBrailleDisplays) aby poznać więcej szczegółów na temat wspieranych rodzajów komunikacji i dostępnych portów.

Miej na uwadze, że jeżeli podłączasz więcej monitorów brajlowskich w tym samym momencie używających tego samego sterownika Np. podłączenie tych samych monitorów brajlowskich seika,
że teraz jest niemożliwie dokładnie ustawić w NVDA, który monitor brajlowski ma być używany.
Czyli zaleca się podłączać monitor brajlowski określonego typu/producenta na raz.

#### Dźwięk {#AudioSettings}

<!-- KC:setting -->

##### Otwiera ustawienia dźwięku {#OpenAudioSettings}

Skrót: `NVDA+control+u`

Kategoria dźwięk w oknie dialogowym ustawień NVDA pozwala zmieniać niektóre opcje związane z odtwarzaniem dźwięków NVDA.

##### Urządzenie wyjściowe {#SelectSynthesizerOutputDevice}

Ta opcja pozwala na wybór urządzenia dźwiękowego, przez które będzie słychać wybrany syntezator NVDA.

<!-- KC:setting -->

##### Tryb przyciszania audio {#SelectSynthesizerDuckingMode}

Skrót klawiszowy: `NVDA+Shift+D`

Ta opcja pozwala wybrać, czy NVDA powinien obniżać głośność innych aplikacji, gdy NVDA mówi albo przez cały czas, gdy NVDA jest uruchomione.

* Bez przyciszania: NVDA nie będzie nigdy obniżać głośności innych dźwięków. 
* Przycisz podczas generowania mowy i dźwięku: NVDA obniży głośność innych dźwięków tylko wtedy, gdy NVDA mówi albo generuje dźwięk. Może to nie działać dla wszystkich syntezatorów. 
* Zawsze przyciszaj: NVDA będzie obniżał głośność innych dźwięków przez cały czas, gdy NVDA jest uruchomione.

Ta opcja jest dostępna tylko, jeśli NVDA został zainstalowany.
Nie jest możliwe obsługiwanie przyciszania audio w przenośnych i tymczasowych kopiach NVDA.+

##### Głośność dźwięków NVDA jest spójna z głośnością  NVDA {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Wyłączone, włączone|
|Domyślnie |wyłączone|

Gdy ta opcja jest włączona, Głośność dźwięków NVDA będzie śledzić głośność używanego syntezatora mowy.
Jeżeli zmniejszysz głośność syntezatora mowy, głośność dźwięków także będzie zmniejszona.
Podobnie, jeżeli powiększysz głośność syntezatora, głośność dźwięku się zwiększy.
Ta opcja nie jest dostępna jeżeli uruchomiłeś NVDA z wyłączonym [WASAPI do wyjścia audio](#WASAPI) z poziomu ustawień zaawansowanych.

##### Głośność dźwięków NVDA {#SoundVolume}

Ten suwak umożliwia ustawienie głośności dźwięków NVDA razem z sygnałami dźwiękowymi.
To ustawienie odnosi skutek gdy opcja "Używaj WASAPI do wyjścia audio" jest włączona, a opcja "Głośność dźwięków NVDA jest spójna z głośnością  NVDA" jest wyłączona.
Ta opcja nie jest dostępna jeżeli uruchomiłeś NVDA z wyłączonym [WASAPI do wyjścia audio](#WASAPI) z poziomu ustawień zaawansowanych.

##### Tryb podzielonego dźwięku {#SelectSoundSplitMode}

Funkcja podzielonego dźwięku umożliwia użytkownikom używanie pełnej funkcjonalności ich stereourządzeń.
Ta funkcja umożliwia  separowanie dźwięku i mowy NVDA w jeden kanał (na przykład lewy) i innych programów w  inny kanał (na przykład prawy).
Domyślnie funkcja podzielonego dźwięku jest wyłączona.
Skrótem klawiszowym można przełączać się między brybami mowy:
<!-- KC:beginInclude -->

| Nazwa |skrót |Opis|
|---|---|---|
|Przełączanie moędzy trybami mowy |`NVDA+alt+s` |Przełącza między trybami mowy.|

<!-- KC:endInclude -->

Domyślnie, ty skrótem można przełączać się pomiędzy następujacymi trybami:

* Wyłączony podział dźwięku: NVDA nie dzieli dźwięk na kanały.
* NVDA w lewym kanale, a inne programy w prawym: NVDA będzie mówiłą w lewym kanale, gdy inne dźwięki będą odtwarzane w prawym kanale.
* NVDA w lewym a programy w obu kanałach: NVDA będzie mówiła w lewym kanale, gdy programy będą odtwarzały dźwięk w obu kanałąch.

Istnieje więcej dostępnych zaawansowanych trybów podziału dźwięku dostępnych w liście rozwijanej ustawień.
Wspośród tych trybów, tryby "NVDA w obu kanałach i programy w obu kanałach" wymusza przekierowanie wszystkich dźwięków w obu kanałach.
Ten tryb różni się od trybu "podział dźwięku wyłączony" w przypadku zakłóceń innych trybów.

Miewaj na uwadze,, że tryb podzielonego dźwięku nie działa jako mikser.
Na przykład, jeżeli program odtwarza utwór w stereo, a tryb podziału dźwięku jest ustawiony na "NVDA w lewym a aplikacje w prawym", wtedy usłyszysz tylko prawy kanał utworu, a lewy kanał utworu będzie wyciszony.

Ta opcja nie jest dostępna, jeżeli [wasapi](#WASAPI) w zaawansowanych ustawieniach jest wyłączony.

Miewaj na uwadze, jeżeli NVDA się zawiesi, głośność dźwięków dla poszczególnych programów nie będzie można przywrócić, a te programy będa nadal odtwarzały dźwięki w jednym kanale po zawieszeniu się NVDA.
Aby rozwiązać ten problem, uruchom ponownie NVDA i wybierz tryb "NVDA w obu kanałąch i programy w obu kanałach".

##### Dostosowywanie trybów mowy {#CustomizeSoundSplitModes}

Ta lista z polami wyboru umożliwia zaznaczenie które tryby mowy są dostępne podczas przełączania między nimi używając `skrótu `NVDA+alt+s``.
Tryby, które są odznaczone nie są dostępne do przełączania.
Domyślnie, tylko trzy tryby są dostępne.

* Podział dźwięku wyłączony.
* NVDA w lewym kanale a programy w prawym.
* NVDA w lewym kanale a programy w obu kanałach.

Miewaj na uwadze, że musisz zaznaczyć conajmniej jeden tryb.
Ta opcja nie jest dostępna gdy [Wasapi](#WASAPI) jest wyłączony w ustawieniach zaawansowanych.

##### Czas podtrzymywania urządzenia audio podczas nieaktywności {#AudioAwakeTime}

To pole edycji określa, jak długo  NVDA będzie trzymała otwarte urządzenie audio po ostatniej wypowiedzi.
To umożliwia zapobieganie problemów z mową, takich jak odcięte części słów.
To jest skutkowane tym, że w większości urządzenia Bluetoot wchodzą do trybu uśpienia.
Ta opcja także może być pomocna w innych przypadkach, takich jak podczas uruchamiania NVDA w wirtualnej maszynie (na przykład Citrix Virtual Desktop), lub na niektórych komputerach przenośnych.

Mniejsze ustawione wartosci mogą spowodować przycinanie mowy częściej, ponieważ urządzenie wchodzi do trybu uśpienia częściej.
Ustawienie tej wartości na wyższe wartości może spowodować szybsze rozładowanie baterii urządzenia audio, ponieważ dłużej zostaje aktywne, a żaden dźwięk nie jest wysyłany.

Aby wyłączyć tę funkcję, ustaw wartość na zero.

#### Ustawienia widoczności {#VisionSettings}

ustawienia widoczności programu NVDA pozwalają na włączanie, wyłączanie i konfigurowanie poszczególnych [ustawień pomocy wizualnych](#Vision).

Pamiętaj że nowe pomoce wizualne mogą być dodawane w [menedżerze dodatków NVDA](#AddonsManager).
Domyślnie ta kategoria zawiera następujące opcje:

##### Podświetlacz fokusu {#VisionSettingsFocusHighlight}

Pola wyboru w tej kategorii kontrolują zachowanie funkcji [podświetlacza fokusu](#VisionFocusHighlight).

* Włącz podświetlenie: włącza lub wyłącza funkcję.
* Podświetlaj kursor systemowy: kontroluje czy [fokus systemowy](#SystemFocus) będzie podświetlany.
* Podświetlaj obiekt nawigatora: Kontroluje czy [obiekt nawigatora](#ObjectNavigation) będzie podświetlany.
* Podświetlaj kursor trybu przeglądania: kontroluje, czy [wirtualny kursor przeglądania](#BrowseMode) będzie podświetlany.

Pamiętaj że zaznaczenie/odznaczenie głównego pola wyboru zmieni też stan pozostałych pól.
Jeżeli pierwsze pole wyboru zostanie oznaczone to wszystkie pozostałe odziedziczą ten stan.
Jeżeli chcesz tylko podświetlić fokus systemowy, stan pola wyboru będzie ustawiony na "częściowo oznaczony".

##### Kurtyna {#VisionSettingsScreenCurtain}

Możesz włączyć  [Kurtynę](#VisionScreenCurtain) przełączając odpowiednie pole wyboru w ustawieniach.
Zostanie wyświetlony monit o tym że po akceptacji ekran stanie się całkowicie czarny.
Przed kontynuowaniem upewnij się, że mowa lub/i brajl działa i że jesteś w stanie używać komputera bez ekranu.
Wciśnij przycisk "nie", jeżeli jednak nie chcesz włączać kurtyny.
Jeżeli jesteś pewien, wciśnij przycisk "tak".
Jeżeli nie chcesz więcej widzieć powyższej wiadomości zaznacz odpowiednie pole wyboru w tych samych ustawieniach, co ustawienia kurtyny.
Pamiętaj, że zawsze możesz przywrócić powyższy monit korzystając z odpowiedniego pola wyboru.

Domyślnie, odtwarzany jest dźwięk w przypadku włączenia lub wyłączenia kurtyny.
Jeżeli chcesz zmienić to zachowanie, przełącz odpowiednie pole wyboru w sekcji ustawień widoczności poświęconej kurtynie.

##### Ustawienia zewnętrznych usług wsparcia wizualnego {#VisionSettingsThirdPartyVisualAids}

Dodatkowe usługi wsparcia widoczności mogą być dostarczane jako [dodatki dla programu NVDA](#AddonsManager).
Jeżeli mają one swoje własne ustawienia można je edytować w osobnych dla nich grupach.
Po więcej informacji prosimy zajrzeć do pomocy danego rozszerzenia.

#### Klawiatura {#KeyboardSettings}

<!-- KC:setting -->

##### Otwiera ustawienia klawiatury {#OpenKeyboardSettings}

Skrót: `NVDA+control+k`

Kategoria klawiatura w oknie ustawień NVDA pozwala ustawić zachowanie NVDA w trakcie używania klawiatury.
Zawiera następujące ustawienia:

##### Układ klawiatury {#KeyboardSettingsLayout}

Pole rozwijalne pozwalające wybrać układ klawiatury dla NVDA. Obecnie dostępne są dwa układy: laptop i Desktop (komputer stacjonarny).

##### Wybierz klawisze modyfikatora NVDA {#KeyboardSettingsModifiers}

Pola wyboru na tej liście określają, które klawisze będą używane jako [klawisze modyfikujące NVDA](#TheNVDAModifierKey). Dostępne są następujące klawisze:

* Klawisz caps lock
* Insert na klawiaturze numerycznej 
* Dodatkowy Insert (na większości klawiatur znajdujący się nad klawiszami strzałek, obok Home i End)

Jeżeli żaden klawisz nie został wybrany jako klawisz NVDA wywoływanie niektórych poleceń stanie się niemoźliwe, w związku z czym musisz wybrać conajmniej jeden klawisz modyfikatora.

<!-- KC:setting -->

##### Czytaj pisane znaki {#KeyboardSettingsSpeakTypedCharacters}

Skrót Klawiszowy: NVDA+2

Jeśli zaznaczysz to pole, NVDA będzie wymawiać pojedyncze znaki podczas wpisywania ich na klawiaturze.

<!-- KC:setting -->

##### Czytaj pisane słowa {#KeyboardSettingsSpeakTypedWords}

Skrót Klawiszowy: NVDA+3

Jeśli zaznaczysz to pole, NVDA będzie wymawiać całe wyrazy po ich wpisaniu z klawiatury.

##### Przerwij mowę dla wpisywanych znaków {#KeyboardSettingsSpeechInteruptForCharacters}

Jeśli włączona, ta opcja spowoduje przerwanie mowy przy wpisaniu jakiegoś znaku. Opcja domyślnie włączona.

##### Przerwa mowy dla klawisza Enter {#KeyboardSettingsSpeechInteruptForEnter}

Jeśli włączona, ta opcja przerywa mowę za każdym razem, gdy naciśnięto klawisz Enter. Opcja domyślnie włączona.

##### Zezwalaj na przeglądanie w trybie czytaj wszystko {#KeyboardSettingsSkimReading}

Jeśli włączona, niektóre polecenia nawigacyjne (takie jak klawisze szybkiej nawigacji w trybie czytania albo przechodzenie po liniach i akapitach) nie przerywają odczytywania tekstu od kursora do końca dokumentu, a zamiast tego odczyt tekstu przeskakuje do nowej pozycji i jest kontynuowany.

##### Dźwięk dla małych liter przy włączonym CapsLock {#KeyboardSettingsBeepLowercase}

Jeśli opcja jest włączona, krótki dźwięk zostanie wygenerowany za każdym razem, gdy wciśnięto literę z shiftem przy włączonym CapsLock.
Na ogół wpisywanie liter z shiftem przy włączonym CapsLock nie jest zamierzone i wynika z niewiedzy, że CapsLock jest włączony.
A zatem ostrzeżenie o tym fakcie może się okazać pomocne.

<!-- KC:setting -->

##### Czytaj klawisze poleceń {#KeyboardSettingsSpeakCommandKeys}

Skrót Klawiszowy: NVDA+4

Jeśli zaznaczysz to pole, NVDA będzie wypowiadać naciskane klawisze, którym nie odpowiadają znaki pisarskie, na przykład klawisze funkcyjne lub kombinacje Ctrl+litera.

##### Odtwarzaj dźwięk przy błędach pisowni podczas wpisywania {#KeyboardSettingsAlertForSpellingErrors}

Gdy włączone, krótki dźwięk alarmu zostanie odtworzony, gdy słowo, które wpisujesz, zawiera błąd pisowni.
Ta opcja jest dostępna tylko jeśli włączone jest zgłaszanie błędów pisowni w kategorii [Ustawień formatowania](#DocumentFormattingSettings) preferencji NVDA.

##### Przetwarzaj klawisze z innych aplikacji {#KeyboardSettingsHandleKeys}

Ta opcja pozwala kontrolować, czy naciśnięcia klawiszy generowane przez aplikacje takie jak klawiatury ekranowe i aplikacje rozpoznawania mowy, powinny być przetwarzane przez NVDA. 
Opcja jest domyślnie włączona, aczkolwiek niektórzy użytkownicy mogą chcieć ją wyłączyć, np. aby pisać w języku wietnamskim przy użyciu programu UniKey. Pozostawienie jej wówczas włączonej powodowałoby wprowadzanie nieprawidłowych znaków.

#### Mysz {#MouseSettings}

<!-- KC:setting -->

##### Otwiera ustawienia myszy {#OpenMouseSettings}

skrót: `NVDA+control+m`

W tej kategorii ustawień można ustawić m.in. sposób śledzenia myszy przez NVDA, informowanie dźwiękiem o położeniu wskaźnika myszy.
Zawiera następujące ustawienia:

##### Informuj o zmianach kształtu wskaźnika {#MouseSettingsShape}

Jeśli zaznaczysz to pole, NVDA będzie podawać, jaki kształt ma wskaźnik myszy za każdym razem, kiedy dojdzie do jego zmiany.
Wskaźnik myszy w systemie Windows zmienia się, by przekazać dodatkowe informacje, na przykład gdy znajduje się nad edytowalnym tekstem lub gdy system jest zajęty podczas ładowania programu.

<!-- KC:setting -->

##### Włącz śledzenie myszy {#MouseSettingsTracking}

Skrót Klawiszowy: NVDA+m

Jeśli zaznaczysz to pole, NVDA będzie czytać tekst znajdujący się aktualnie pod wskaźnikiem myszy. Opcja ta pozwala na odnajdywanie informacji na ekranie poprzez poruszanie fizyczną myszą bez konieczności nawigowania po hierarchii obiektów.

##### Rozdzielczość tekstu {#MouseSettingsTextUnit}

Jeśli śledzenie myszy jest włączone, ta opcja pozwala dokładnie określić ile tekstu znajdującego się aktualnie pod wskaźnikiem myszy zostanie wypowiedziane.
Dostępne opcje to znak, słowo, wiersz i akapit.

Aby przełączyć ten parametr z dowolnego miejsca, proszę przypisać własne zdarzenie wejścia używając [Okna zdarzenia wejścia](#InputGestures).

##### Odczytaj obiekt podczas wejścia do niego za pomocą myszy {#MouseSettingsRole}

Jeżeli to pole wyboru jest zaznaczone, NVDA przeczyta informacje o obiektach podczas przemieszczania myszą po obiektach.
W to wchodzą typ obiektu tak jak i stan (zaznaczone/wciśnięte), współrzędne komórek w tabelach itd.
Miewj na uwadze, że odczyt niektórych informacji o o niektóych szczegółó obiektów może zależeć od innych ustawień, takich jak [ustawienia prezentacji obiektu](#ObjectPresentationSettings) lub [formatowanie dokumentu](#DocumentFormattingSettings).

##### Sygnalizuj dźwiękiem położenie myszy {#MouseSettingsAudio}

Jeśli zaznaczysz to pole, NVDA będzie generować dźwięki podczas poruszania myszą, ułatwiając określenie pozycji wskaźnika na ekranie.
Im wyżej mysz jest na ekranie, tym wyższy będzie dźwięk.
Im bardziej po lewej lub prawej stronie ekranu znajduje się wskaźnik myszy, tym bardziej po lewej lub prawej stronie będzie słychać dźwięk (jeśli użytkownik ma podłączone stereofoniczne słuchawki lub głośniki).

##### Głośność dźwięku myszy zależy od jasności obrazu {#MouseSettingsBrightness}

Jeśli zaznaczysz to pole, dźwięki sygnalizujące położenie myszy będą tym głośniejsze, im jaśniejszy jest obraz znajdujący się w miejscu wskaźnika. Opcja ta ma znaczenie tylko, jeśli włączona jest funkcja "Sygnalizuj dźwiękiem położenie myszy". 
Funkcja domyślnie jest wyłączona.

##### Ignoruj ruch myszy z innych aplikacji {#MouseSettingsHandleMouseControl}

Ta opcja pozwala na ignorowanie zdarzeń myszy (ruchów myszy i naciskanych przycisków) wygenerowanych przez inne aplikacje, takie jak TeamViewer i inne oprogramowanie kontroli zdalnej.
Opcja domyślnie wyłączona.
Jeśli ją włączysz i masz włączoną opcję  śledzenia myszy, NVDA nie będzie oznajmiać co jest pod myszą jeśli zostanie ona przesunięta przez inną aplikację.

#### Interakcja dotykowa {#TouchInteraction}

Ta kategoria ustawień, dostępna tylko na komputerach z ekranem dotykowym, pozwala skonfigurować w jaki sposób NVDA obsługuje ekrany dotykowe.
Zawiera następujące ustawienia:

##### Włącz wsparcie dotykowe {#TouchSupportEnable}

To pole wyboru przełącza obsługę dotykową NVDA.
Gdy opcja ta jest włączona, możesz używać urządzenia dotykowego do nawigacji.
W przeciwnym razie, urządzenie dotykowe zachowuje się tak, jakby NVDA nie był uruchomiony.
Opcję tę można również przełączyć przy pomocy skrótu NVDA+CTRL+ALT+T.

##### Tryb wpisywania dotykowego {#TouchTypingMode}

To pole wyboru pozwala określić metodę, której chcesz używać do wprowadzania tekstu przy użyciu klawiatury ekranowej.
Jeśli jest zaznaczone, to gdy zlokalizujesz klawisz na klawiaturze ekranowej, możesz podnieść palec i wybrany klawisz zostanie wciśnięty.
Gdy nie jest oznaczone, należy dwukrotnie stuknąć klawisz na klawiaturze ekranowej aby go nacisnąć.

#### Kursor przeglądu {#ReviewCursorSettings}

W tej kategorii ustawień, można określić działanie kursora przeglądu.
Zawiera następujące ustawienia:

<!-- KC:setting -->

##### Śledź fokus {#ReviewCursorFollowFocus}

Skrót Klawiszowy: NVDA+7

Gdy opcja jest włączona, kursor przeglądu zawsze zostanie umieszczony w tym samym obiekcie, w którym znajduje się fokus, gdy aktualny się zmieni.

<!-- KC:setting -->

##### Śledź kursor systemu {#ReviewCursorFollowCaret}

Skrót Klawiszowy: NVDA+6

Gdy opcja jest włączona, kursor przeglądu zostanie automatycznie przeniesiony przy każdym ruchu na pozycję kursora systemu, gdy jego pozycja się zmieni.

##### Śledź wskaźnik myszy {#ReviewCursorFollowMouse}

Gdy opcja jest włączona, kursor przeglądu będzie przesuwać się do wskaźnika myszy przy każdej zmianie jego położenia.

##### Tryb prostego przeglądania {#ReviewCursorSimple}

Gdy opcja jest włączona, NVDA będzie filtrować hierarchię obiektów, którymi można nawigować, aby wykluczyć bezużyteczne obiekty np. obiekty niewidoczne albo używane tylko do tworzenia układu treści.

Aby móc przełączać ten tryb z każdego miejsca, proszę przypisać własne zdarzenie wejścia przy użyciu [okna zdarzeń wejścia](#InputGestures).

#### Prezentacja obiektów {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Otwiera opcje prezentacji obiektów {#OpenObjectPresentationSettings}

Skrót: `NVDA+control+o`

Ta kategoria ustawień NVDA  pozwala określić ilość informacji prezentowanych przez NVDA na temat kontrolek takich jak opis, informacje o położeniu itd.
Te opcje typowo nie są stosowane  do trybu czytania.
Te opcje zazwyczas są zastosowane do czytania fokusu i obiektową nawigację NVDA, ale nie i do czytania tekstowej treści na przykład tryb czytania na stronach webowych.

##### Czytaj dymki podpowiedzi {#ObjectPresentationReportToolTips}

Jeśli zaznaczysz to pole, NVDA będzie czytać pojawiające się dymki podpowiedzi (tooltip).
Są to niewielkie wiadomości wyświetlane często po wskazaniu myszą lub przeniesieniu fokusa na dane okno lub kontrolkę.

##### Czytaj powiadomienia {#ObjectPresentationReportNotifications}

Pole to kontroluje zachowanie NVDA w przypadku napotkania powiadomienia.

* Dymki pomocy są nieco większe od dymków podpowiedzi, i są powiązane ze zdarzeniami systemowymi takimi jak na przykład odłączenie zasilania, kabla sieciowego ITD.
* Powiadomienia toast zostały wprowadzone w systemie Windows 10. Pojawiają się one w centrum akcji i informują o zdarzeniach takich jak nadejście poczty, nowej aktualizacji systemu ITD.

##### Odczytuj klawisze skrótów {#ObjectPresentationShortcutKeys}

Jeśli zaznaczysz to pole, NVDA informując o obiektach, pozycjach menu lub kontrolkach okien dialogowych będzie wypowiadać również związany z nimi klawisz skrótu. 
Dla przykładu, menu plik może mieć przypisany skrót Alt+P.

##### Odczytuj położenie obiektów {#ObjectPresentationPositionInfo}

Ta opcja pozwala zmienić sposób ogłaszania pozycji obiektu po przejściu do obiektu z fokusem lub obiektu nawigacji (np. 1 z 4).

##### odgadnij położenie obiektu, gdy nie dostępne {#ObjectPresentationGuessPositionInfo}

Gdy włączona jest opcja powiadamiania o położeniu obiektu, a z przyczyn technicznych jest ono niedostępne dla NVDA w aktualnej kontrolce, NVDA może próbować je odgadnąć.

Gdy opcja powyższa jest zaznaczona, NVDA może odczytywać informacje o pozycji w większej ilości obiektów, jak niektóre paski narzędziowe czy menu, lecz informacje te mogą być nieco niedokładne.

##### Odczytuj opisy obiektów {#ObjectPresentationReportDescriptions}

Odznacz to pole, jeśli nie chcesz, by program NVDA czytał opisy obiektów.

<!-- KC:setting -->

##### Sygnał paska postępu {#ObjectPresentationProgressBarOutput}

Skrót Klawiszowy: NVDA+u

Ta opcja określa w jaki sposób NVDA sygnalizuje aktualizację paska postępu.

Dostępne są następujące opcje:

* Wyłączone: Nie będzie sygnalizowana żadna zmiana paska postępu.
* Mowa: Ta opcja instruuje NVDA, by zmiany pasków postępu były wypowiadane mową. Po każdej zmianie paska postępu, NVDA będzie wymawiać nową wartość.
* Dźwięk: Oznacza, że NVDA użyje sygnału dźwiękowego przy każdej zmianie paska postępu. Im wyższy dźwięk, tym bliżej jest do końca paska postępu.
* Mowa i dźwięk: Ta opcja oznacza informowanie jednocześnie dźwiękiem i mową, gdy pasek postępu się aktualizuje.

##### Sygnalizuj zmiany na paskach postępu będących w tle {#ObjectPresentationReportBackgroundProgressBars}

Jest to opcja, która - gdy zaznaczona - sprawia, że NVDA śledzi zmiany paska postępu, nawet jeśli fizycznie pasek ten nie jest na pierwszym planie.
Jeśli zminimalizujesz okno zawierające pasek postępu albo przełączysz się do innego okna, NVDA i tak będzie informował o postępach tego paska.

<!-- KC:setting -->

##### Informuj o dynamicznych zmianach treści {#ObjectPresentationReportDynamicContent}

Skrót Klawiszowy: NVDA+5

Przełącza ogłaszanie nowej treści w niektórych obiektach takich jak terminale albo okienko historii w komunikatorach.

##### Odtwórz dźwięk, gdy pojawiają się automatyczne podpowiedzi {#ObjectPresentationSuggestionSounds}

Przełącza oznajmianie pojawiania się automatycznych podpowiedzi. Gdy włączone, NVDA odtworzy dźwięk aby to oznajmić.
Automatyczne podpowiedzi są listą sugerowanych wpisów opartą o tekst wprowadzony w niektórych polach edycyjnych i dokumentach.
Dla przykładu, jeśli wprowadzisz tekst do pola wyszukiwania w Menu start w Windows Vista i nowszych, system wyświetli listę podpowiedzi bazującą na tym co zostało wpisane.
Dla niektórych pól edycyjnych takich jak pola wyszukiwania w różnych aplikacjach Windows 10, NVDA może powiadomić, że po wpisaniu tekstu pojawiła się lista podpowiedzi.
Lista podpowiedzi zostanie zamknięta po wyjściu z pola edycji i dla niektórych pól, NVDA może również o tym powiadomić.

#### Układ wprowadzania {#InputCompositionSettings}

Ta kategoria opcji pozwala określić w jaki sposób NVDA kontroluje wprowadzanie znaków azjatyckich za pomocą  IME lub  usług tekstowych.
Ponieważ metody wprowadzania bardzo się różnią dostępnymi właściwościami oraz sposobem przekazywania informacji, najprawdopodobniej będzie konieczne skonfigurowanie tych opcji indywidualnie dla każdej metody wprowadzania, aby uzyskać największą wygodę pisania.

##### Automatycznie zgłaszaj wszystkie dostępne znaki kandydujące {#InputCompositionReportAllCandidates}

Ta opcja, domyślnie włączona,  pozwala określić czy wszystkie widoczne znaki kandydujące powinny być automatycznie odczytane gdy pojawia się lista znaków kandydujących albo jej strona się zmienia.
Włączenie tej opcji dla piktograficznych metod wprowadzania, takich jak chińska nowa ChangJie albo Boshiami jest przydatne, ponieważ możesz automatycznie usłyszeć wszystkie symbole, ich numery i od razu któryś wybrać.
Natomiast dla fonetycznych metod wprowadzania, takich jak chińska nowa fonetyczna, może okazać się lepsze wyłączenie tej opcji, ponieważ wszystkie symbole będą brzmieć tak samo i będziesz musiał użyć strzałek do przejścia po liście aby uzyskać więcej informacji z opisów znaków każdego kandydata.

##### Czytaj wybrany znak kandydujący {#InputCompositionAnnounceSelectedCandidate}

Ta opcja, domyślnie włączona, pozwala określić czy NVDA powinien ogłaszać wybrany znak kandydujący, gdy pojawia się lista znaków kandydujących lub zaznaczenie się zmieni.
Dla metod wprowadzania, w których zaznaczenie może zostać zmienione klawiszami strzałek (takich jak chińska nowa fonetyczna) jest to konieczne, ale dla innych metod wprowadzania może okazać się wygodniejsze wpisywanie z wyłączoną tą opcją.
Uwaga: nawet po wyłączeniu tej opcji, punkt przeglądu będzie wciąż umieszczany na wybranym znaku kandydującym, pozwalając użyć obiektu nawigacji / przeglądu dla ręcznego odczytania tego lub innych znaków kandydujących.

##### Zawsze ogłaszaj krótki opis znaku kandydującego {#InputCompositionCandidateIncludesShortCharacterDescription}

Ta opcja, domyślnie włączona, pozwala określić czy NVDA powinien odczytać krótki opis każdego znaku kandydującego, gdy zostanie on zaznaczony lub będzie odczytany automatycznie po pojawieniu się listy kandydatów.
Uwaga: dla ustawień regionalnych takich jak chiński, ogłaszanie dodatkowych opisów wybranego znaku kandydującego działa niezależnie od ustawienia tej opcji.
Ta opcja może być użyteczna dla metod wprowadzania koreańskiego lub japońskiego.

##### Ogłaszaj zmiany w łańcuchu czytania {#InputCompositionReadingStringChanges}

Niektóre metody wprowadzania, np. chińska nowa fonetyczna albo nowa ChangJie posiadają łańcuch czytania (czasem znany jako ciąg prekompozycyjny).
Dzięki tej opcji możesz określić, czy nowe znaki dodawane do tego łańcucha powinny być odczytywane przez NVDA.
Opcja jest domyślnie włączona.
Uwaga: niektóre starsze metody wprowadzania, takie jak chińska ChangJie mogą nie używać łańcucha czytania do przechowywania znaków prekompozycyjnych, a zamiast tego bezpośrednio używać łańcucha kompozycyjnego. Następna opcja omawia konfigurowanie odczytu łańcucha kompozycyjnego.

##### Zgłaszaj zmiany w ciągu składowym {#InputCompositionCompositionStringChanges}

Po tym jak dane z łańcucha czytania lub ciągu prekompozycyjnego uformowały prawidłowy symbol piktograficzny, większość metod wprowadzania umieszcza ten symbol w ciągu składowym dla tymczasowego przechowania razem z  innymi utworzonymi symbolami, zanim ostatecznie trafią one do dokumentu.
Ta opcja pozwala określić, czy NVDA powinien ogłaszać nowe znaki dodawane do ciągu składowego.
Opcja jest domyślnie włączona.

#### Tryb czytania {#BrowseModeSettings}

<!-- KC:setting -->

##### Otwiera ustawienia trybu czytania {#OpenBrowseModeSettings}

Skrót: `NVDA+control+b`

Ta kategoria preferencji NVDA określa sposób działania programu podczas czytania skomplikowanych dokumentów, np. stron internetowych.
Zawiera następujące ustawienia:

##### Maksymalna liczba znaków w linii {#BrowseModeSettingsMaxLength}

To pole określa maksymalną długość linii trybu czytania (w znakach).

##### Maksymalna liczba linii na stronie {#BrowseModeSettingsPageLines}

Ustala ilość linii, które zostaną przeskoczone po wciśnięciu Page up lub Page down w trybie czytania.

<!-- KC:setting -->

##### Użyj układu ekranu {#BrowseModeSettingsScreenLayout}

Skrót Klawiszowy: NVDA+v

Ta opcja umożliwia określenie rozmieszczania elementów klikalnych (linków, przycisków i pól) w osobnych liniach, oraz zachowaniu ich w strumieniu tekstu czyli tak, jak wizualnie wyglądają na ekranie.
Trzeba mieć na uwadze, że ta opcja nie stosuje się do programów Microsoft Office takich jak Outlook i Word, które zawsze używają układu ekranu.
Kiedy układ ekranu jest włączony, elementy strony zostaną pokazane w sposób wizualny.
Na przykład, jedna wizualna linia linków będzie pokazana w mowie i w brajlu jako wiele linków w jednej linii.
Jeżeli jest wyłączona, wtedy elementy strony będą pokazane w oddzielnych liniach.
To może być bardziej zrozumiale podczas nawigacji po wierszach na stronie, i może ułatwić interakcje z elementami na stronie dla niektórych użytkowników.

##### Włącz tryb czytania podczas wczytywania strony {#BrowseModeSettingsEnableOnPageLoad}

Ten przełącznik określa, czy tryb czytania powinien być automatycznie włączany podczas ładowania strony.
Jeśli wyłączone, tryb czytania może być aktywowany ręcznie na stronach lub w dokumentach, które wspierają ten tryb.
Zobacz [rozdział o trybie czytania](#BrowseMode) zawierający listę aplikacji obsługujących tryb czytania.
Ta opcja nie ma zastosowania do sytuacji, w których tryb czytania jest zawsze opcjonalny np. w Microsoft Word.
Opcja jest domyślnie włączona.

##### automatycznie czytaj wszystko przy wczytywaniu strony {#BrowseModeSettingsAutoSayAll}

Ta opcja przełącza automatyczne odczytywanie strony po jej załadowaniu w trybie czytania.
Domyślnie opcja jest zaznaczona.

##### Informuj o tabelach układu treści {#BrowseModeSettingsIncludeLayoutTables}

Ta opcja określa jak NVDA traktuje tabele używane wyłącznie do wizualnego rozmieszczenia treści.
Gdy jest włączona, NVDA będzie je traktować jak normalne tabele, zgłaszając je w oparciu o [Ustawienia formatowania dokumentów](#DocumentFormattingSettings) i przechodząc do nich przy użyciu komend szybkiej nawigacji.
Gdy opcja jest wyłączona - nie będą zgłaszane, ani wyszukiwane w szybkiej nawigacji.
Zawartość tych tabel będzie jednak nadal dostępna jako tekst.
Ta opcja jest domyślnie wyłączona.

Aby przełączać dołączanie tabel układu treści z każdego miejsca, należy przypisać temu poleceniu własne zdarzenie wejścia przy użyciu okna [Zdarzenia wejścia](#InputGestures).

##### Konfiguracja ogłaszania pól, takich jak linki i nagłówki {#BrowseModeLinksAndHeadings}

Proszę przejrzeć opcje w [kategorii formatowania dokumentu](#DocumentFormattingSettings) w oknie [ustawień NVDA](#NVDASettings), aby skonfigurować informacje, które są ogłaszane w trakcie nawigacji, takie jak linki, nagłówki i tabele.

##### Automatyczny tryb formularza przy zmianie fokusa {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Ta opcja pozwala na wywołanie trybu formularza z trybu czytania, gdy zmieni się fokus. 
Jeśli poruszając się po stronie internetowej naciskając TAB znajdziesz się we formularzu, a ta opcja zostanie zaznaczona, NVDA automatycznie przejdzie do trybu formularza.

##### Automatyczny tryb formularza przy ruchach kursora {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Opcja ta, gdy zaznaczona, powoduje automatyczne wejście i wyjście z trybu formularza za pomocą klawiszy strzałek.
Na przykład, gdy poruszając się strzałkami po stronie internetowej natrafisz na pole edycyjne, NVDA automatycznie przejdzie w tryb formularza.
Gdy natomiast naciśniesz w formularzu strzałkę w dół i wyjdziesz poza kontrolkę, NVDA powróci do trybu czytania.

##### Sygnalizuj dźwiękiem tryby przeglądania {#BrowseModeSettingsPassThroughAudioIndication}

Jeśli ta opcja jest włączona, NVDA będzie sygnalizować dźwiękiem przełączanie się między trybem czytania i trybem formularza, zamiast ogłaszać te zmiany mową.

##### Nie przekazuj do dokumentu zdarzeń wejścia niebędących poleceniami {#BrowseModeSettingsTrapNonCommandGestures}

Domyślnie włączone, to ustawienie pozwala zdecydować, że zdarzenia wejścia, (takie jak naciskane klawisze) które nie są poleceniami NVDA, ani nie wyglądają na polecenia aplikacji, powinny nie być przekazywane do dokumentu, w którym znajduje się punkt uwagi. 
Dla przykładu: jeśli to ustawienie jest włączone i naciśnięto literę j, zostanie ona zignorowana, ponieważ nie jest komendą szybkiej nawigacji i nie wydaje się być poleceniem aplikacji.
W takim wypadku zostanie odegrany domyślny dźwięk systemowy.

<!-- KC:setting -->

##### Automatycznie ustaw kursor na klikalnym elemencie {#BrowseModeSettingsAutoFocusFocusableElements}

Klawisz: NVDA+8

Opcja ta kontroluje, czy NVDA będzie domyślnie ustawiać kursor systemowy na pierwszym klikalnym elemencie takim jak link, pole wyboru czy przycisk, gdy tryb przeglądania zostanie aktywowany.
Pozostawienie tej opcji wyłączonej sprawi, że NVDA nie będzie ustawiać się na pierwszym klikalnym elemencie po aktywowaniu trybu przeglądania.
Może spowodować to przyspieszenie działania trybu przeglądania.
Kursor będzie przenoszony do pozycji kontrolki w przypadku aktywowania jej.
Włączenie tej opcji może spowodować, że wsparcie pewnych stron internetowych poprawi się, ale kosztem responsywności.

#### Formatowanie dokumentów {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Otwiera ustawienia formatowania dokumentów {#OpenDocumentFormattingSettings}

Skrót: `NVDA+control+d`

Większość opcji w tej kategorii służy do konfiguracji, jaki rodzaj formatowania chcesz usłyszeć automatycznie podczas poruszania się kursorem po dokumentach.
Jeśli np. zaznaczysz pole wyboru "Odczytuj nazwy czcionek", to za każdym razem gdy kursor znajdzie się na tekście z inną czcionką, nazwa tej czcionki zostanie odczytana.

Opcje formatowania dokumentu są pogrupowane.
Możemy w ten sposób skonfigurować odczytywanie:

* Czcionki
  * Nazw czcionek
  * Rozmiaru czcionki
  * Atrybutów czcionki
  * Podkreślenia
  * Podkreślonego, (zaznaczonego tekstu)
  * Stylu tekstu
  * Kolorów
  * Informacji o dokumencie
* Komentarzy
  * Zakłądki
  * Indeksy górne i dolne
  * Zmian edycyjnych
  * Błędów pisowni
* stron i odstępów
  * Numerów stron
  * Numerów linii
  * Wcięć linii [(Wyłączone, Mowa, Dźwięki, Mowa i dźwięki)](#DocumentFormattingSettingsLineIndentation)
  * Ignorowanie pustych linii podczas odczytywania wcięć
  * Wcięć akapitu (np. wysunięcie, wcięcie pierwszej linii)
  * Interlinii (pojedyncza, podwójna etc)
  * Wyrównania tekstu
* Informacji o tabeli
  * Tabel
  * Nagłówków wierszy/kolumn (wyłączone, wiersze, kolumny, wiersze i kolumny)
  * Współrzędnych komórek tabeli
  * Ramek komórek [(Wyłączone, Style, kolory i style)
* Elementów
  * Nagłówków
  * Linków
  * Obrazków
  * List
  * Cytatów
  * Grup
  * Punktów orientacyjnych
  * Artykułów
  * Ramek
  * Figur i podpisów
  * Gdy element jest klikalny

Aby przełączać te ustawienia z każdego miejsca, proszę określić własne zdarzenia wejścia w [oknie zdarzenia wejścia](#InputGestures).

##### Zgłaszaj formatowanie za kursorem {#DocumentFormattingDetectFormatAfterCursor}

Jeśli opcja jest włączona, to NVDA spróbuje wykryć wszystkie zmiany formatowania w odczytywanej linii, nawet jeśli to pogorszy wydajność NVDA.

Domyślnie NVDA wykryje formatowanie na pozycji Kursora Systemu / punktu Przeglądu, a w niektórych przypadkach może wykryć formatowanie reszty wierszy, ale tylko wtedy gdy nie będzie to powodować spadku wydajności.

Włącz tę opcję, by przeprowadzić korektę dokumentów w aplikacjach takich jak Wordpad, gdzie formatowanie jest bardzo ważne.

##### Zgłaszaj wcięcia linii {#DocumentFormattingSettingsLineIndentation}

Ta opcja pozwala ustawić w jaki sposób mają być zgłaszane wcięcia na początku linii.
Lista rozwijana zgłaszania wcięć linii ma cztery opcje.

* Wyłączone: NVDA nie będzie zgłaszał wcięć.
* mowa: gdy zmieni się głębokość wcięcia linii, NVDA wypowie komunikat w stylu "12 spacja" lub "4 tab."
* Dźwięki: przy zmianie głębokości wcięcia linii, dźwięki odzwierciedlą głębokość wcięcia.
Wysokość dźwięku będzie wzrastać dla każdej spacji, a dla tabulatora przyrost wysokości dźwięku będzie równy przyrostowi dla czterech spacji.
* Mowa i dźwięki: ta opcja zgłosi wcięcia przy użyciu obu powyższych metod.

Jeżeli zaznaczysz pole wyboru "Ignoruj puste linie podczas odczytu wcięć" zmiany wcięć nie będą odczytywane w pustych liniach.
To może być użyteczne podczas czytania tekstu z pustymi liniami do rozdzielania bloków tekstu, na przykład w kodzie programu.

#### Nawigacja po dokumencie {#DocumentNavigation}

Ta kategoria umożliwia różne opcje związane z nawigacją po dokumentach.

##### Styl akapitu {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |domyślnie (zarządzane przez aplikacje), zarządzane przez aplikacje, pjjedyńczy podzial wiersza, podział wielowierszowy|
|Domyślnie |zarządzane przez aplikacje|

To pole wyboru umożliwia wybór stylu akapitu, który ma być użyty podczas nawigacji używając skrótów `control+strzałka w górę` i `control+strzałka w dół`.
Dostępne style akapitów to:

* Zarządzane przez aplikacje: NVDA pozwoli aplikacji określanie następnego lub poprzedniego akapitu, a NVDA potem przeczyta następny lub poprzedni akapit podczas nawigacji.
Ten styl działa najlepiej w przypadku natywnego wsparcia nawigacji po akapitach, i jest to opcja domyślna.
* Jeden rozdział wiersza: NVDA spróbuje wykryć poprzedni lub następny akapit używając jednej pustej linii jako indykatora.
Ten styl najlepiej działa w aplikacjach, które nie wspierają natywną nawigację po akapitach, a akapity zostały oznaczone jednym naciśnięciem przycisku `enter`.
* rozdział wielowierszowy: NVDA spróbuje określić poprzebny lub następny akapit używając conajmniej jedną pustą linię (dwa naciśnięcia klawisza `enter` ) jako indykatora akapitu.
Ten styl najlepiej działa gdy pracujemy z dokumentami, w których używane są akapity blokowe.
Miejcie na uwadze, że ten styl akapitu nie może być używany w programach Microsoft Word i Microsoft Outlook, chyba że włączone jest wsparcie UIA dla dostępu do kontrolek Microsoft Word.

Style akapitów można przełączać z jakiegokolwiek miejsca przydzielając skrót klawiszowy w [oknie dialogowym zdarzenia wejścia](#InputGestures).

#### Ustawienia Windows OCR {#Win10OcrSettings}

Ta kategoria ustawień NVDA pozwala skonfigurować [Windows OCR](#Win10Ocr).
Zawiera następujące ustawienia:

##### Język rozpoznawania {#Win10OcrSettingsRecognitionLanguage}

Ta lista rozwijana pozwala wybrać język, używany do rozpoznawania tekstu.
Aby się przemieszczać między dostępnymi językami z każdego miejsca, Przydziel zdarzenie wejścia używając [okno dialogowe zdarzenia wejscia](#InputGestures).

##### Od czasu do czasu odświeżaj  treść rozpoznawaną {#Win10OcrSettingsAutoRefresh}

Gdy to pole wyboru jest zaznaczone, NVDA będzie automatycznie odświeżała rozpoznaną treść kiedy wynik rozpoznawania jest w fokusie.
To może być użyteczne gdy chcesz śledzić stale zmieniającą się treść, taką jak napisy w filmach.
Treść odświeża się co półtora sekundy.
Ta opcja jest domyślnie wyłączona.

#### Ustawienia zaawansowane {#AdvancedSettings}

Uwaga! Ustawienia w tej kategorii są przeznaczone dla zaawansowanych użytkowników i mogą spowodować nieprawidłowe działanie NVDA jeśli zostaną błędnie zmodyfikowane.
Zmieniaj te ustawienia tylko jeśli wiesz co robisz lub zostałeś poinstruowany przez twórcę NVDA.

##### Zmienianie ustawień zaawansowanych {#AdvancedSettingsMakingChanges}

Aby zmienić ustawienia zaawansowane, musi zostać zaznaczone pole wyboru potwierdzenia, że rozumiesz ryzyko wynikające ze zmieniania tych ustawień.

##### Przywracanie ustawień domyślnych {#AdvancedSettingsRestoringDefaults}

Przycisk przywraca domyślne wartości ustawień, nawet jeśli pole wyboru potwierdzenia nie jest zaznaczone.
Po zmianie ustawień, możesz chcieć wrócić do ich wartości domyślnych.
Może również to mieć miejsce jeśli nie jesteś pewien, czy ustawienia zostały zmienione.

##### włącz wczytywanie własnego kodu z piaskownicy dewelopera NVDA {#AdvancedSettingsEnableScratchpad}

Podczas tworzenia dodatków dla NVDA jest istotna możliwość testowania kodu w trakcie jego tworzenia.
Gdy ta opcja jest włączona, umożliwione jest wczytywanie przystosowanych modułów aplikacji, wtyczek globalnych, sterowników monitorów brajlowskich, sterowników syntezatorów mowy i dostawców ulepszenia widoczności z specjalnego folderu dla programistów o nazwie scratchpad z twojego folderu konfiguracji.
Jako równoznaczniki dodatków, te moduły wczytywane są po uruchomieniu NVDA, lub w przypadku modułów aplikacji i wtyczek globalnych podczas [ponownego przeładowywania wtyczek](#ReloadPlugins).
Ta opcja jest domyślnie wyłączona, zapewniając, że nieprzetestowany kod nie będzie uruchamiany przez NVDA  bez wiedzy użytkownika.
Jeśli chcesz rozpowszechniać własny kod do innych, powinieneś spakować go jako dodatek NVDA.

##### Otwórz katalog piaskownicy NVDA {#AdvancedSettingsOpenScratchpadDir}

Ten przycisk otwiera folder, w którym możesz umieszczać własny kod podczas prac nad nim.
Przycisk jest aktywny tylko, gdy NVDA jest ustawione na wczytywanie własnego kodu z piaskownicy programisty.

##### rejestracja zdarzeń i zmian właściwości UIA {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |automatycznie, selektywna, globalna|
|domyślnie |automatyczne|

Ustawienie to kontroluje, w jaki sposób NVDA rejestruje zdarzenia wysyłane przez API Microsoft UI Automation.
Lista rozwijana Rejestracja zdarzeń i zmian właściwosci UIA zawiera trzy opcje:

* Automatycznie: "Selektywnie" w Windows 11 Sun Valley 2 (wersja 22H2) i nowszych wersjach, "globalnie" w przeciwnych wypadkach.
* Selektywnie: NVDA ograniczy rejestracje zdarzeń do fokusu systemowego dla większosci zdarzeń.
Jeżeli doświadczasz znacznych problemów z wydajnością, zalecamy włączenie tego ustawienia.
Jednakże, w starszych wersjach systemu Windows, NVDA może mieć problemy z śledzeniem fokusu w niektórych kontrolkach (takich jak menedżer zadań i panel emoji).
* Globalnie: NVDA rejestruje dużo zdarzeń UIA które są procesowane i niszczone przez sam czytnik ekranu NVDA.
Choć śledzenie fokusu jest niezawodne w wielu przypadkach, wydajność jest znacznie pogorszona, najbardziej w programach takich jak Microsoft Visual Studio.

##### Używaj UI automation w celu uzyskania dostępu do kontrolek dokumentów programu Microsoft Word {#MSWordUIA}

Reguluje sposób w jaki NVDA będzie używała UI automation api dla dostępu do dokumentów Microsoft WOrd, zamiast modelu obiektowego Microsoft Word.
To się stosuje do dokumentów Microsoft word, a także wiadomości w programie Microsoft Outlook.
To ustawienie zawiera następujące wartości:

* Domyślne: (gdy jest to konieczne)
* Tylko wtedy, gdy jest to konieczne: Tam gdzie model obiektowy Microsoft word nie jest wcale dostępny
* w stosownych przypadkach: Microsoft Word wersja 16.0.15000 lub nowsza, oraz tam, gdzie model obiektowy Microsoft Word nie jest dostępny
* Zawsze: gdziekolwiek dostępne jest UIA w programie Microsoft word (niezależnie od tego, na ile wsparcie jest stabilne i kompletne).

##### Użyj interfejsu UI Automation dla dostępu do kontrolek arkuszy kalkulacyjnych w programie Microsoft Excel, gdy jest to możliwe {#UseUiaForExcel}

Gdy ta opcja jest włączona, NVDA NVDA spróbuje używać Microsoft UI Automation accessibility API w celu dostarczania informacji z kontrolek skoroszytów w programie Microsoft Excel.
Jest to funkcja eksperymentalna, i niektóre funkcje programu Microsoft Excel mogą być niedostępne.
Na przykład, niedostępne funkcje to lista elementów NVDA do listowania formuł i komentarzy, i szybka nawigacja w trybie przeglądania do przeskakiwania do pól formularzy w skoroszycie.
Jednakże, dla podstawowej nawigacji  lub edytowania, ta opcja może wprowadzić dużą poprawę wydajności.
Nie polecamy większości użytkowników włączenie tej opcji, ale zapraszamy użytkowników programu Microsoft Excel, w wersji 16.0.13522.10000 lub nowszej do testowania tej funkcjonalności i wysyłania informacji zwrotnej.
Implementacja UIA w programie Microsoft Excel UI automation zmienia się z wersją na wersje, i wersje starsze niż 16.0.13522.10000 mogą nie dostarczać żadnych korzystnych informacji.

##### Używaj ulepszonego przetwarzania zdarzeń {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (włączone), wyłączone, włączone|
|Domyślnie |włączone|

Gdy ta opcja jest włączona, NVDA zostanie responsywna podczas dostawania dużej ilości zdarzeń Uia, na przykład, dużej ilości tekstu w konsoli.
Po zmianie tej opcji, musisz ponownie uruchomić NVDA, aby zmiany zadziałały.

##### Obsługa konsoli systemu Windows {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |automatycznie, UIA gdy jest to możliwe, przestarzałe|
|Domyślnie |automatycznie|

Ta opcja reguluje interakcję z konsolą używaną przez wiersza poleceń, PowerShell, i podsystem Linux dla systemu WIndows.
Ta opcja nie wpłynie na Windows terminal.
W wersji systemu Windows 10 kompilacja 1709, firma Microsoft [dodała wsparcie dla swojego API UI Automation dla wierszy poleceń](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), ulepszając wydajność i stabilność dla czytników ekranu które to api wspierają.
W sytuacjach w których UI Automation jest niedostępne oraz jest znane że spowoduje spadek dobrego doświadczenia użytkownika, wsparcie przestarzałe dla wiersza poleceń systemu Windows dla NVDA jest dostępne jako zapas.
Lista rozwijana wsparcie konsoli systemu Windows posiada trzy opcje:

* automatyczne: używa UI Automation w wersji konsoli systemu Windows dołączonej do Windows 11 wersji 22H2 i nowszych.
Ta opcja jest zalecana i domyślnie ustawiona.
* UIA jeżeli jest dostępne: używa UI Automation w konsolach jeżeli jest to dostępne, nawet z wersjami zawierającymi niekompletne oraz błędne implementacje.
Choć ta opcja moze być korzystna (i nawet dostateczna dla użytku), używanie tej opcji podlega pod ryzyko użytkownika a wsparcie dla tej opcji nie będzie okazywane.
* przestarzałe: UI Automation w konsoli systemu windows będzie kompletnie wyłączone.
Opcja przestarzałe będzie używana jako zapasowa nawet w sytuacjach w których UI Automation będzie działała lepiej dla użytkownika.
Więc, wybór tej opcji jest niezalecany, chyba żę wiesz, co robisz.

##### Użyj UIA z przeglądarką Microsoft Edge i innymi przeglądarkami opartymi na Chromium gdy jest to możliwe {#ChromiumUIA}

Umożliwia definiowanie, kiedy interfejs UIA będzie używany gdy jest dostępny w przeglądarkach opartych na Chromium, takich jak Microsoft Edge.
Wsparcie UIA dla przeglądarek opartych na Chromium jest w wczesnej fazie rozwoju i może nie dostarczać takiego samego poziomu dostępu jak implementacja IA2.
Pole wyboru zawiera następujące opcje:

* Domyślne (tylko wtedy, gdy jest to potrzebne): Opcja domyślna używana w NVDA, aktualnie jest używane "tylko, gdy jest to potrzebne". Ten stan domyślny może się w przyszłości zmienić z czasem postępu rozwoju tej technologii.
* Tylko gdy jest to potrzebne: Gdy NVDA nie może wejsć w interakcje z procesem przeglądarki w celu używania IA2, a jest dostępny interfejs UIA, wtedy NVDA będzie używała UIA.
* Tak: jeżeli przeglądarka udostępnia UIA, NVDA będzie używała tego interfejsu.
* Nie: Nie Używa UIA, nawet gdy NVDA nie może wejść w interakcję z procesem przeglądarki. Ta opcja moze być użyteczna dla deweloperów debugujących problemy z UIA, upewniając się, że interfejs UIA nie będzie używany.

##### Adnotacje {#Annotations}

Ta grupa opcji jest używana do włączania funkcji, które dodają eksperymentalne wsparcie dla adnotacji aria.
Niektóre z tych funkcji mogą być niedopracowane.

<!-- KC:beginInclude -->
Aby "odczytać streszczenie każdej adnotacji pod kursorem systemowym", naciśnij NVDA+d.
<!-- KC:endInclude -->

Istnieją następujące opcje: 

* "Odczytuj 'posiada szczegóły' dla adnotacji strukturalnych": włącza zgłaszanie posiadania więcej szczegułów w tekście lub kontrolce.
* "Zawsze odczytuj aria-description":
  Gdy źródłem `accDescription` jest aria- description, opis jest odczytywany.
  Jest to użyteczne dla adnotacji na stronach www.
  Uwaga:
  * Istnieje wielu źródeł dla `accDescription` niektóre z nich posiadają mieszaną lub nieprzewidywalną semantykę.
    Historycznie, technologie wspomagające nie mogły to rozróźniać źródła `accDescription`i typowo nie były one wymawiane z powodu mieszanej  semantyki.
  * Ta opcja jest w bardzo wczesnym stadium rozwoju, i polega na opcjach przeglądarek, które nie są szeroko dostępne.
  * Oczekiwane jest, że ta funkcja będzie działać z Chromium 92.0.4479.0 i nowszymi wersjami.

##### Odczytuj żywe regiony {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (włączone), wyłaczone, włączone|
|Domyślnie |włączone|

Ta opcja reguluje odczyt zmian w niektórych treściach dynamicznych na stronach internetowych na monitorach brajlowskich.
Wyłączenie tej opcji jest równoznaczne z zachowaniem w wersji 2023.1 i starszych. W starszych wersjach, te zmiany były tylko wymawiane.

##### Wymawiaj hasła w nowoczesnych wierszach poleceń {#AdvancedSettingsWinConsoleSpeakPasswords}

To ustawienie reguluje wymowę znaków przez [opcje czytaj pisane znaki](#KeyboardSettingsSpeakTypedCharacters) lub [czytaj pisane słowa](#KeyboardSettingsSpeakTypedWords) w sytuacjach, w gdy ekran się nie odświeża (takich jak wpisywanei hasłą) w niektórych programach wiersza poleceń, takich jak wiersz poleceń systemu windows z włączonym wsparciem dla UIA lub Mintty.
Dla bezpieczeństwa warto zostawic te opcję wyłączoną.
Jednakże, można ją włączyć jeżeli doświadczasz problemy z wydajnością oraz niestabilnym czytaniem znaków lub słów w wierszach poleceń, lub pracujesz w zaufanych środowiskach i preferujesz wymawianie haseł.

##### Użyj ulepszone wsparcie oznajmiania wpisywanych znaków w wierszach poleceń {#AdvancedSettingsKeyboardSupportInLegacy}

Ta opcja umożliwia alternatywną metodę wykrywania wpisywanych znaków w przestarzałych wierszach poleceń systemu windows.
ustawienie to powoduje znaczne przyspieszenie pracy i poprawia kilka błędów, jednakże może być ono niekompatybilne ze starszymi programami konsolowymi.
Ta funkcja jest dostępna i domyślnie włączona dla systemów operacyjnych Windows 10 1607i nowszych gdy interfejs UI Automation jest niedostępny lub wyłączony.
Uwaga! Gdy ta opcja jest włączona, wpisywane znaki, które nie pojawiają się na ekranie (takie jak hasła), będą odczytywane!
W środowiskach niegodnych zaufania możesz tymczasowo wyłączyć opcję [czytaj pisane znaki](#KeyboardSettingsSpeakTypedCharacters) oraz [czytaj pisane słowa](#KeyboardSettingsSpeakTypedWords) podczas wpisywania haseł.

##### Metoda wykrywania zmian treści w terminalu {#DiffAlgo}

To ustawienie kontroluje wymowę nowego tekstu w programach konsolowych.
Lista rozwijana Metoda wykrywania zmian treści w terminalu zawiera trzy opcji:

* Automatycznie: ta opcja skutkuje preferowanie Diff Match Patch przez NVDA w większości sytuacji, ale używa zapasowo Difflib w aplikacjach problematycznych, takich jak starsze wersje wiersza polecenia systemu Windows i Mintty.
* Diff Match Patch: ta opcja skutkuje przeliczanie zmian przez NVDA tekstu wiersza poleceń po znakach, nawet w sytuacjach, w których jest to niezalecane.
To może usprawnić wydajność gdy w konsoli pojawi się wielka ilość tekstu, a także umożliwia dokłądniejsze ogłaszanie tekstu w środku wiersza.
Jednakże, w niektórych aplikacjach, odczyt nowego tekstu może być częsciowy lub niekonzystentny.
* Difflib: Ta opcja skutkuje przeliczanie przez NVDA zmian w wierszu poleceń po linii, nawed w niezalecanych sytuacjach.
Jest to identyczne zachowywanie z wersjami 2020.4 i starszymi.
To ustawienie może ustabilizować czytanie w niektórych aplikacjach.
Jednakże, w wierszach poleceń, podczas wstawiania lub usuwania znaku w środku wiersza, tekst po kursorze będzie przeczytany.

##### Czytaj nowy tekst w terminalu Windows za pomocą {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (różnicowanie), różnicowanie, Powiadomienia UIA|
|Domyślnie |różnicowanie|

Ta opcja określa, który tekst jest nowy dla NVDA i jaki tekst ma być wymówiony gdy opcja "informuj o dynamicznych zmianach treści" jest włączona) w Windows Terminalu i oknach wpf używanych w Visual Studio 2022.
Nie wplynie to na konsolę systemu windows (`conhost.exe`).
Lista rozwijana Czytaj nowy tekst w terminalu Windows za pomocą posiada trzy opcji:

* Domyślnie: ta opcja jest teraz równoznaczna z "różnicowaniem", ale może się zmienić w momencie, gdy wsparcie dla powiadomień UIA będzie jeszcze bardziej rozbudowane.
* Różnicowanie: Ta opcja używa wybrany algorytm do różnicowania do wyliczania zmian w każdej chwili, w której nowy tekst pokazywany jest w oknie konsoli.
Jest to identyczne z zachowaniem programu NVDA w wersjach 2022.4 i starszych.
* Powiadomienia UIA: ta opcja oddaje odpowiedzialność określania wodczytu nowego tekstu do samej konsoli, co oznacza, że NVDA więcej nie musi określać nowy tekst.
To powinno znacząco polepszyć wydajność i stabilność terminala, ale ta funkcja jeszcze nie jest dokończona.
Ogólnie, wpisywane znaki, któe nie są widoczne na ekranie, takie jak hasła, są odczytywane, gdy ta opcja jest włączona.
Dodatkowo, ciągłe wyjście tekstowe, przekraczające ponad 1000 znaków może być nieprawidłowo odczytane.

##### Próba zatrzymywania mowy dla przestarzałych zdarzeń fokusu {#CancelExpiredFocusSpeech}

Ta opcja włącza zachowanie, które spowoduje próby zatrzymywania mowy dla przestarzałych zdarzeń mowy.
ogólnie może się zdarzyć, że NVDA będzie wymawiała przestarzałą informację w aplikacjach webowych, takich jak Gmail przy szybkim przechodzeniu używając przeglądarki Chrome.
Jest to funkcja domyślna od wersji NVDA 2021.1.

##### Szybkość śledzenia przemieszczania się po polach edycji (w milisekundach) {#AdvancedSettingsCaretMoveTimeout}

Pozwala skonfigurować ilość milisekund, którą  NVDA będzie czekało przed przesunięciem kursora w polach edycji.
Jeśli zauważysz, że NVDA nieprawidłowo śledzi kursor, np.  jest zawsze znak za kursorem lub powtarza linie, możesz próbować zwiększyć tę wartość.

##### Odczytuj przejrzystość kolorów {#ReportTransparentColors}

Ta opcja pozwala odczytywać przejrzystość kolorów, co jest ważne dla deweloperów dodatków oraz modułów aplikacji, którzy zbierają informacje w celu ulepszenia doświatczenia użytkownika.
Niektóre aplikacje GDI będą podkreślać tekst kolorem tłą, NVDA (za pomocą modelu wyświetlania) spróbuje zgłośić ten kolor.
W niektórych sytuacjach, tło tekstowe może być całkowicie przejrzyste, z tekstem pokazanym nad innym elementem okna.
Z niektórymi historycznie popularnymi API do wyświetlania okien, tekst może być pokazywany za pomocą przejrzystego tła, ale wizualnie kolor jest dokładny.

##### Używaj WASAPI do wyjścia audio {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Opcje |Domyślnie (włączone), Wyłączone, Włączone|
|Domyślnie |Włączone|

Ta opcja włącza wsparcie wyjścia dźwięku za pomocą interfejsu windows audio session (WASAPI).
WASAPI to bardziej nowoczesny interfejs audio który może przyśpieszyć odzew, wydajność i stabilność wydawanego dźwięku przez NVDA, włączając w to dźwięki i mowe.
Po zmianie tej opcji, do zastosowania zmian wymagane jest ponowne uruchomienie.
Gdy Wasapi jest wyłączone, zostaną wyłączone następujące opcje:

* [Głośność dźwięków NVDA jest spójna z głośnością  NVDA](#SoundVolumeFollowsVoice)
* [Głośność dźwięków NVDA](#SoundVolume)

##### Włączone kategorie debugowania {#AdvancedSettingsDebugLoggingCategories}

Pola wyboru na tej liście pozwalają włączyć konkretne kategorie informacji debugowania w dzienniku NVDA.
Zapisywanie tych informacji może zmniejszyć wydajność i zwiększyć rozmiar pliku logu.
Włącz określone kategorie tylko, gdy zostaniesz poinstruowany przez programistę NVDA np. w trakcie badania, dlaczego sterownik linijki brajlowskiej nie pracuje prawidłowo.

##### Odtwarzaj dźwięk dla logowanych błędów {#PlayErrorSound}

Ta opcja pozwala określić możliwość odtwarzania dźwięku błędu przez NVDA w przypadku zapisanego błędu.
Wybierając "tylko w wersjach testowych" (domyślnie) spowoduje, że błędy będą odtwarzane tylko w wersjach testowych (alpha, beta lub z wersji uruchomionych z kodu źródłowego).
Wybierając "tak" umożliwia odtwarzanie dźwięku błędu niezależnie od wersji NVDA.

##### Wyrażenie regularne dla nawigacji po  akapitach {#TextParagraphRegexEdit}

To ustawienie umożliwia użytkownikom dostosowywanie wyrażenia regularnego dla wykrywania akapitów w trybie czytania.
Poleceie [nawigacji po akapitach](#TextNavigationCommand) szuka akapitów według tego wyrażenia regularnego.

### Różne ustawienia {#MiscSettings}

Oprócz okna [ustawień NVDA](#NVDASettings), podmenu opcje w menu NVDA zawiera kilka innych elementów, omówionych poniżej.

#### Słowniki wymowy {#SpeechDictionaries}

Menu słowniki wymowy (znajdujące się w menu Ustawienia) zawiera polecenia otwierające okna dialogowe, które pozwalają zarządzać sposobem w jaki NVDA wypowiada określone słowa lub frazy.
Obecnie istnieją trzy rodzaje słowników mowy. 
Są to:

* Słownik domyślny: wpisy tego słownika mają wpływ na całą wymowę w NVDA.
* Słownik głosu: reguły w tym słowniku mowy wpływają na aktualnie używany głos syntezatora
* Słownik Tymczasowy: wpisy tego słownika mają wpływ na całą wymowę w NVDA, ale tylko dla bieżącej sesji. Reguły te są tymczasowe i zostaną utracone, jeśli NVDA zostanie ponownie uruchomiony.

Musisz określić własne zdarzenia wejścia używając [okna zdarzenia wejścia](#InputGestures) jeśli chcesz otwierać któreś z tych okien z każdego miejsca.

Okno dialogowe każdego słownika zawiera listę zdefiniowanych reguł wymowy.
Znajdują się tam również przyciski Dodaj, Edytuj, Usuń i usuń wszystkie.

Aby dodać nową regułę do słownika, naciśnij przycisk Dodaj, a następnie wypełnij pola w wyświetlonym oknie dodawania reguły, i naciśnij przycisk OK.
Nową regułę zobaczysz na liście reguł.
Aby jednak upewnić się, że reguła została zapisana naciśnij przycisk OK, aby zamknąć okno słownika po zakończeniu edycji.

Reguły słowników mowy NVDA pozwalają zamienić jeden ciąg znaków na inny.
Prosty przykład: chcemy, aby zamiast słowa "ptak", NVDA czytał słowo "żaba".
Najprostszym sposobem na to jest wpisanie słowa ptak w polu wzorzec, a słowa żaba w polu Zamiana w oknie dialogowym Dodaj regułę.
Można także wpisać opis reguły w polu komentarz (np. zamiana słowa ptak na żaba).

Słowniki mowy w NVDA mają jednak o wiele więcej możliwości niż tylko proste zamiany słów.
Okno dodawania reguły zawiera pole wyboru "Uwzględniaj wielkość liter", a jego zaznaczenie sprawi, że NVDA będzie przy stosowaniu reguły zwracał uwagę na to, czy tekst jest wpisany dużymi, czy małymi literami. 
Domyślnie NVDA ignoruje różnice w wielkości liter.

Zestaw przycisków opcji pozwala określić, czy wpisany wzorzec powinien pasować gdziekolwiek, tylko jako całe słowo albo powinien być traktowany jako "wyrażenie regularne".
Ustawienie dopasowywania wzorca do caŁego sŁowa oznacza, że wzorzec będzie zamieniony tylkoo jeżeli wzorzec nie występuje jako część większego słowa.
Ten warunek zostaje spełniony jeżeli znaki od razu przed lub po słoowie są wszystko oprócz jednej litery, cyfry, lub podkreślnika, oraz jeżeli w ogóle nie występuje żaden znak.
Wracając do wcześniejszego przykładu zamiany "ptak" na "żaba", jeśli reguła zostałaby ustawiona jako zastąpienie całego słowa, nie zastąpiłaby słowa "ptaki".

Wyrażenie regularne jest to wzorzec zawierający specjalne symbole, które pozwalają na dopasowanie więcej niż jednego znaku jednocześnie, mogą to być np. cyfry lub litery.
Wyrażenia regularne nie będą omawiane w tym podręczniku.
Po więcej informacji, zapraszamy na stronę [Python's Regular Expression Guide](https://docs.python.org/3.11/howto/regex.html).

#### Wymowa znaków i symboli {#SymbolPronunciation}

To okno dialogowe pozwala określić w jaki sposób NVDA wypowiada konkretne znaki czy inne symbole. Pozwala także ustawić poziom interpunkcji, przy którym są one wypowiadane.

Język, którego wymowa jest edytowana, będzie wyświetlony w tytule okna dialogowego.
Uwaga: to okno uwzględnia opcję "Ufaj językowi głosu przetwarzając znaki i symbole" znajdującą się w [kategorii głos](#SpeechSettings)w oknie [Preferencji NVDA](#NVDASettings); tj. gdy ta opcja jest włączona, używa języka głosu zamiast globalnego języka NVDA.

Aby zmienić symbol, najpierw zaznacz go na liście. 
Możesz filtrować symbole wprowadzając symbol lub część zastępującego tekstu w polu edycji sortuj według.

* Pole zamień określa tekst, który powinien być wypowiadany zamiast tego znaku. 
* Używając listy poziom, można regulować najniższy poziom interpunkcji, na którym dany znak będzie wypowiadany: brak, niektóre, większość, wszystko. 
Można także ustawić poziom symbolu na znak. W tym przypadku, symbol nie będzie wymawiany, niezależnie od ustawionego poziomu interpunkcji, z następującymi dwoma wyjątkami:
  * podczas nawigacji po znakach.
  * Gdy NVDA wymawia tekst, zawierający ten symbol.
* Pole wyślij rzeczywisty symbol do syntezatora określa, czy sam symbol (w przeciwieństwie do jego zastępnika) powinien zostać wysłany do syntezatora.
Jest to przydatne, jeśli symbol powoduje pauzę w odczycie albo zmianę intonacji głosu.
Dla przykładu przecinek powoduje krótką pauzę syntezatora.
Istnieją trzy opcje:
  * Nigdy: Nigdy nie wysyłaj rzeczywistego symbolu do syntezatora.
  * zawsze: zawsze wysyłaj rzeczywisty symbol do syntezatora.
  * tylko poniżej poziomu symbolu: wyślij rzeczywisty symbol tylko wtedy, gdy poziom interpunkcji jest niższy niż poziom symbolu.
  Można tego użyć, aby symbol miał tekstowy odpowiednik wypowiadany na wyższych poziomach interpunkcji bez powodowania pauzy, a był identyfikowany pauzą na niższych poziomach.

Możesz dodać nowe symbole po naciśnięciu przycisku "Dodaj".
W okienku, które się pojawi, wprowadź symbol i naciśnij Ok.
Następnie zmodyfikuj pozostałe pola, tak jak przy innych symbolach.

Możesz usunąć symbol, naciskając przycisk "Usuń".

Aby zapisać zmiany naciśnij przycisk ok, aby je odrzucić - naciśnij zrezygnuj.

W przypadku złożonych symboli, pole zamiany powinno zawierać referencję grupową tekstu docelowego. Na przykład, dla wzorca, który stosuje się do całej daty, w polu powinno być napisane \1, \2, i \3, aby zmiana zadziałała dla odpowiednich części daty.
Normalne ukośniki wsteczne powinni być dublowane, na przykład "a\\b" powinno być wpisane właśnie w takim porządku, aby dostać zamianę "a\b".

#### Zdarzenia wejścia {#InputGestures}

W tym oknie dialogowym możesz skonfigurować komendy NVDA uruchamiane przez zdarzenia wejścia (klawisze naciskane na klawiaturze, przyciski na monitorze brajlowskim, etc.).

Pokazywane są tylko polecenia, które mają zastosowanie bezpośrednio przed otwarciem tego okna.
Dla przykładu, jeśli chcesz skonfigurować polecenia związane z trybem czytania, powinieneś otworzyć okno zdarzeń wejścia, gdy znajdujesz się w trybie czytania.

Drzewo w tym oknie wyświetla wszystkie dostępne polecenia NVDA podzielone na kategorie.
Możesz je filtrować wpisując w pole edycyjne filtru jedno lub więcej słów występujących w nazwie polecenia.
Jakiekolwiek zdarzenia wejścia powiązane z poleceniem, są wyświetlone poniżej tego polecenia.

Aby dodać zdarzenie wejścia do polecenia, wybierz polecenie i kliknij przycisk "Dodaj".
Następnie wprowadź zdarzenie wejścia, które chcesz powiązać; np. naciśnij klawisz na klawiaturze albo przycisk na monitorze brajlowskim.
Często zdarzenie wejścia może zostać zinterpretowane na wiele sposobów.
Dla przykładu, jeśli nacisnąłeś klawisz, możesz wymagać, aby był on powiązany z aktualnym układem klawiatury (np. desktop lub laptop) albo stosować go dla wszystkich układów klawiatury.
W takim przypadku pojawi się menu umożliwiające wybór pożądanej opcji.

Aby usunąć powiązanie zdarzenia wejścia z poleceniem, wybierz to zdarzenie i naciśnij przycisk "Usuń".

Kategoria "Emulowane klawisze systemowe" zawiera polecenia emulujące systemowe skróty klawiszowe.
Skróty takie mogą zostać użyte na przykład do kontrolowania aspektów systemu operacyjnego przy pomocy monitora brajlowskiego.
Aby dodać emulowane polecenie, wybierz kategorię "Emulowane klawisze systemowe", a następnie wciśnij przycisk "Dodaj".
Następnie, wciśnij skrót, który chcesz emulować.
Skrót pojawi się potem jako normalne, mapowalne polecenie NVDA.

Uwaga:

* W celu zachowania emulowanych skrótów klawiszowych, należy najpierw przypisać do nich polecenie NVDA.
* Przypisanie polecenia NVDA korzystającego z klawiszy modyfikujących do emulowanego skrótu pozbawionego  modyfikatorów. 
Na przykład, przypisanie emulowanego polecenia `a` do polecenia `CTRL+M` może skończyć się  W aplikacji która dostaje `ctrl+a`.

Po zakończeniu wprowadzania zmian, naciśnij przycisk OK aby je zachować albo przycisk Anuluj, aby odrzucić.

### Zapisywanie i przywracanie ustawień {#SavingAndReloading}

NVDA domyślnie zapisuje ustawienia automatycznie przy wyjściu z programu.
To zachowanie może zostać wyłączone w okienku "Ustawienia ogólne".
Aby ręcznie zapisać ustawienia w każdej chwili, użyj polecenia "Zapisz ustawienia" w menu NVDA.

Jeśli przez pomyłkę zmienisz ustawienia programu, możesz skorzystać z opcji "Przywróć zapisane ustawienia" dostępnej z menu NVDA.
Możesz również przywrócić konfigurację do ustawień fabrycznych, wybierając w menu NVDA polecenie "Zresetuj konfigurację do ustawień fabrycznych".

Przydatne są także następujące klawisze poleceń NVDA:
<!-- KC:beginInclude -->

| Działanie |Skróty Klawiszowe Desktopa |Skróty Klawiszowe Laptopa |Opis|
|---|---|---|---|
|Zapisz ustawienia |NVDA+Ctrl+C |NVDA+Ctrl+C |Zapisuje aktualne ustawienia, tak aby ich nie stracić po zamknięciu NVDA.|
|Przywróć zapisane ustawienia |NVDA+Ctrl+R |NVDA+Ctrl+R |Naciśnięty raz, przywraca ostatnio zapisane ustawienia. Naciśnięty szybko 3-krotnie, przywraca ustawienia fabryczne|

<!-- KC:endInclude -->

### Profile konfiguracji {#ConfigurationProfiles}

Czasem może być przydatne posiadanie różnych ustawień dla różnych sytuacji.
Dla przykładu: możesz chcieć mieć włączone ogłaszanie wcięć podczas edycji albo zgłaszanie atrybutów czcionek podczas poprawiania tekstu.
NVDA pozwala to osiągnąć za pomocą profili konfiguracyjnych.

Profil konfiguracyjny zawiera tylko te ustawienia, które zostały zmienione podczas edycji profilu.
Większość ustawień może być zmieniona w profilach konfiguracyjnych, wyłączając ustawienia znajdujące się w kategorii ogólne w oknie [Preferencji NVDA](#NVDASettings), które mają zastosowanie do całego programu.

Profile konfiguracyjne mogą być aktywowane ręcznie przy użyciu okna, lub własnego zdarzenia wejścia.
Mogą być również aktywowane automatycznie przez wyzwalacze, takie jak przejście do określonej aplikacji.

#### Podstawowe zarządzanie {#ProfilesBasicManagement}

Profilami zarządzasz wybierając polecenie "Profile konfiguracji" w menu NVDA.
Możesz zrobić to również za pomocą skrótu klawiszowego:
<!-- KC:beginInclude -->

* NVDA+Ctrl+p: wyświetl okno profili konfiguracji.

<!-- KC:endInclude -->

Lista w tym oknie dialogowym, zawiera wszystkie dostępne profile.
Po otwarciu okna, domyślnie wybrany jest aktualnie edytowany profil.
Dla profili aktywnych wyświetlane są również dodatkowe informacje, określające, czy są ręcznie aktywowane, aktywowane przez wyzwalacze i/lub będące w trakcie edycji.

Aby zmienić nazwę lub usunąć profil, naciśnij odpowiedni przycisk w oknie dialogowym.

Naciśnij przycisk Zamknij, aby zamknąć okno.

#### Tworzenie profilu {#ProfilesCreating}

Aby utworzyć profil, naciśnij przycisk "Nowy"..

W oknie nowego profilu, możesz określić jego nazwę.
Możesz również wybrać, jak ten profil powinien być używany.
Jeśli chcesz aktywować go tylko ręcznie, wybierz aktywację ręczną (ustawienie domyślne).
W innym wypadku wybierz wyzwalacz, który powinien uruchamiać ten profil.
Dla ułatwienia, jeśli nie wybrałeś nazwy profilu, wybór wyzwalacza automatycznie wypełni pole nazwy.
Zobacz [poniżej](#ConfigProfileTriggers) aby uzyskać więcej informacji o wyzwalaczach.

Naciśnięcie przycisku OK spowoduje utworzenie profilu i zamknięcie okna profili konfiguracji abyś mógł edytować utworzony profil.

#### Ręczna aktywacja {#ConfigProfileManual}

Możesz ręcznie aktywować profil, wybierając go na liście i naciskając przycisk Aktywuj ręcznie.
Po aktywacji, inne profile będą mogły być aktywowane przez wyzwalacze, ale każde ustawienie obecne w profilu ręcznie aktywowanym będzie nadrzędne.
Dla przykładu, jeśli profil został uruchomiony przez wyzwalacz dla aktualnej aplikacji i zgłaszanie linków jest włączone w tym profilu, ale wyłączone w profilu ręcznie aktywowanym, linki nie będą zgłaszane.
Jeśli jednak zmieniłeś głos w profilu uruchomionym przez wyzwalacz, ale nie zmieniałeś głosu w profilu ręcznie aktywowanym, użyty będzie głos z profilu automatycznie aktywowanego przez wyzwalacz.
Wszystkie dokonane zmiany zostaną zapisane w profilu ręcznie aktywowanym.
Aby unieaktywnić ręcznie aktywowany profil, wybierz go w oknie profili konfiguracji i naciśnij przycisk Dezaktywuj.

#### Wyzwalacze {#ConfigProfileTriggers}

Naciśnięcie przycisku Wyzwalacze w oknie profili konfiguracji, pozwala zmienić profile, które powinny być aktywowane automatycznie.

Lista wyzwalaczy wyświetla dostępne wyzwalacze, które są następujące:

* Aktualna aplikacja: uruchamiany, gdy przełączysz się do aktualnej aplikacji.
* Czytaj wszystko: aktywowany podczas czytania poleceniem Czytaj wszystko.

Aby zmienić profil, który powinien być automatycznie aktywowany przez wyzwalacz, wybierz wyzwalacz, a następnie wybierz pożądany profil na liście profili.
Możesz wybrać (konfigurację normalną) jeśli nie chcesz, aby profil był używany.

Naciśnij przycisk Zamknij, aby powrócić do profili konfiguracji.

#### Edycja profilu {#ConfigProfileEditing}

Jeśli aktywowałeś ręcznie jakiś profil, każda zmiana ustawień zostanie zapisana w tym profilu.
W przeciwnym wypadku, każda zmiana ustawień zostanie zapisana do profilu ostatnio aktywowanego przez wyzwalacz.
Dla przykładu: jeśli masz profil konfiguracyjny skojarzony z Notatnikiem i przełączysz się do notatnika, jakiekolwiek zmienione ustawienie zostanie zapisane do profilu.
Jeśli żaden profil nie jest aktywowany ręcznie ani automatycznie, wszystkie zmienione ustawienia zostaną zapisane w normalnym pliku konfiguracyjnym.

Aby edytować profil skojarzony z funkcją czytaj wszystko, musisz [aktywować ręcznie](#ConfigProfileManual) ten profil.

#### Tymczasowe wyłączenie wyzwalaczy {#ConfigProfileDisablingTriggers}

Czasem jest przydatne czasowe wyłączenie wszystkich wyzwalaczy.
Dla przykładu: możesz chcieć edytować profil aktywowany ręcznie,  albo plik normalnej konfiguracji, bez wpływu na to profili aktywowanych przez wyzwalacze.
Możesz to osiągnąć przez oznaczenie pola wyboru Tymczasowo wyłącz wszystkie wyzwalacze w oknie dialogowym profili konfiguracji.

Aby możliwe było wyłączenie wyzwalaczy z każdego miejsca, należy zdefiniować własne zdarzenie wejścia przy użyciu [okna zdarzeń wejścia](#InputGestures).

#### Aktywacja profilu przy użyciu zdarzeń wejścia {#ConfigProfileGestures}

Do każdego dodanego profilu można przypisać jedno lub wiele zdarzeń wejścia,  które będą go aktywować.
Domyślnie, profile konfiguracji nie mają przypisanych zdarzeń wejścia.
Możesz dodać zdarzenie wejścia aktywujące profil przy użyciu [okna zdarzenia wejścia](#InputGestures).
Każdy profil posiada odpowiadający mu wpis w kategorii profile konfiguracji.
Po zmianie nazwy profilu, aktywujące go zdarzenia wejścia będą nadal działać.
Usunięcie profilu automatycznie usunie zdarzenia wejścia przypisane do jego aktywacji.

### Lokalizacja plików konfiguracyjnych {#LocationOfConfigurationFiles}

Wszystkie ustawienia wersji przenośnej NVDA, folder appModules oraz niestandardowe sterowniki znajdują się w katalogu o nazwie userConfig w folderze głównym NVDA.

Instalacyjna wersja NVDA przechowuje wszystkie ustawienia, niestandardowe sterowniki i dodatki w specjalnym katalogu NVDA w profilu użytkownika systemu Windows.
Oznacza to, że każdy użytkownik w systemie może mieć własne ustawienia NVDA.
Aby móc otworzyć katalog konfiguracyjny ustawień NVDA można użyć [okno dialogowe zdarzenia wejścia](#InputGestures) żeby dodać gesty użytkownika.
Na zainstalowanej wersji NVDA dodatkowo otworzyć ten katalog z poziomu menu start, programy -> NVDA -> przeglądaj katalog konfiguracji.

Ustawienia NVDA stosowane na ekranie logowania i ekranie kontroli konta użytkownika, są przechowywane w folderze systemConfig w katalogu instalacyjnym NVDA.
Zwykle folder ten nie powinien być ręcznie modyfikowany.
Aby zmienić konfigurację NVDA na ekranie logowania, ustaw najpierw żądaną konfigurację w NVDA po zalogowaniu do systemu, zapisz ją, a następnie kliknij przycisk "Używaj zapisanych ustawień na ekranie NVDA" w kategorii "Ogólne" w oknie [Preferencji NVDA](#NVDASettings).

## Dodatki i Add-on Store {#AddonsManager}

Dodatki to pakiety oprogramowania dostarczające do NVDA nową lub zmienioną funkcjonalność.
Rozwijane są przez społeczność NVDA i organizacje zewnętrzne, takie jak dostawcy komercyjni.
Dodatki mogą wykonywać następujące czynności:

* Dodawać lub ulepszać wsparcie niektórych aplikacji,
* dostarczać wsparcie dodatkowych monitorów brajlowskich lub syntezatorów mowy,
* zmieniać funkcje NVDA.

NVDA Add-on Store umożliwia przeglądanie i zarządzanie dodatkami.
Wszystkie dodatki dostępne w Add-on store są bezpłatne.
Niektóre jednak mogą wymagać opłaty licencyjnej lub dodatkowego oprogramowania.
Przykładem tego typu dodatków są komercyjne syntezatory mowy.
Jeżeli dodatek z płatnymi komponentami się nie sprawdzi, można go łatwo usunąć.

Add-on store znajduje się w menu NVDA/narzędzia.
Aby wywołać go globalnie, przypisz gest użytkownika w [oknie dialogowym zdarzenia wejścia](#InputGestures).

### Przegląd dodatków {#AddonStoreBrowsing}

Po otwarciu Add-on Store, zobaczysz listę dodatków.
Jeżeli do tej pory nie instalowałeś jeszcze żadnego dodatku, Add-on store zostanie otwarte na liście dostępnych do zainstalowania.
Jeżeli posiadasz już zainstalowane dodatki, pokażą się one na liście zainstalowanych.

Poruszaj się strzałkami w górę i w dół, żeby przeczytać szczegóły każdego dodatku.
Do poszczególnych dodatków przypisane są działania, takie jak zainstaluj, pomoc, wyłącz i usuń, do których możesz dotrzeć używając [menu działań](#AddonStoreActions).
Dostępne działania zmienią się w zależności od tego, czy dodatek jest zainstalowany lub nie. Zależą też od stanu - włączony lub wyłączony.

#### Listy dodatków {#AddonStoreFilterStatus}

Dostępne są cztery listy dodatków: zainstalowane, do zaktualizowania, dostępne i niezgodne.
Aby zmienić listę dodatków, zmień aktywną kartę właściwości używając `ctrl+tab`.
Możesz także klawiszem `tab` przejść do listy kart właściwości, i przemieszczać się między nimi używając `strzałki w lewo` i `strzałki w prawo`.

#### Filtrowanie włączonych i wyłączonych dodatków {#AddonStoreFilterEnabled}

Właściwie zainstalowany dodatek jest "włączony",. Status ten oznacza, że jest uruchomiony i dostępny.
Jednak niektóre zainstalowane dodatki mogą być ustawione w stanie "wyłączony".
To oznacza że nie będą używane, a ich funkcjonalność nie będzie dostępna podczas twojej aktualnej sesji NVDA.
Mogłeś wyłączyć dodatek, ponieważ był w konflikcie z innym dodatkiem albo którąś  aplikacją systemową.
NVDA może samodzielnie wyłączać niektóre dodatki, jeżeli podczas aktualizacji okażą się niezgodne. O takiej sytuacji zostaniesz ostrzeżony.
Dodatki mogą również zostać wyłączone, jeśli nie używasz ich przez dłuższy czas, ale ich nie odinstalowujesz, bo w przyszłości mogą znowu być potrzebne.

Lista niezgodnych lub zainstalowanych dodatków może być filtrowana według ich stanu.
Domyślnie pokazują sie dodatki włączone i wyłączone.

#### Pokazuj niezgodne dodatki {#AddonStoreFilterIncompatible}

Lista dodatków dostępnych i dodatków do zainstalowania może być filtrowana tak, aby pokazywały się  [dodatki niezgodne](#incompatibleAddonsManager) dostępne do instalacji.

#### Filtruj dodatki według kanału {#AddonStoreFilterChannel}

Dodatki mogą być dystrybuowane w czterech kanałach:

* stabilnym - Programista opublikował stabilny dodatek do użytku ze stabilną wersją NVDA,
* Beta - Taki dodatek wymaga dłuższego testovania, ale został opublikowany w celu zbierania informacji zwrotnej od użytkowników,
Kanał polecany ludziom zainteresowanym wersjami beta.
* Dev - Ten kanał jest rekomendowany do użytku przez programistów dodatków do testowania zmian w Api.
Kanał skierowany do testerów wersji alpha NVDA.
* Z pliku: dodatki instalowane z zewnętrznych źródeł, czyli spoza Add-on Store.

Aby pokazywać dodatki tylko z określonych kanałów, zmień wybór w filtrze "kanał".

#### Wyszukiwanie dodatków {#AddonStoreFilterSearch}

Aby wyszukiwać dodatki, używaj pola edycji  "szukaj".
Możesz przejść do niego naciskając `shift+tab` z listy dodatków.
Napisz jedno lub dwa kluczowe słowa, żeby znaleźć żądany typ dodatku którego szukasz, potem `` wróć przyciskiem `tab` do listy dodatków.
Wyszukiwane dodatki pojawią się na liście, jeżeli wpisany przez ciebie tekst zostanie znaleziony w polach identyfikatora dodatku, nazwy wyświetlanej, wydawcy lub  opisu.

### Działania na dodatkach {#AddonStoreActions}

Dodatki posiadają przypisane działania, takie jak instalacja, pomoc, wyłącz i usuń.
Do menu działań konkretnego dodatku można wejść z listy naciskając klawisz `kontekstowy`, `enter`, klikając prawym przyciskiem myszy, lub klikając dwukrotnie jej lewym przyciskiem.
Do tego menu można przejść za pomocą przycisku działania w szczegółach wybranego dodatku.

#### Instalowanie dodatków {#AddonStoreInstalling}

Jeżeli dodatek znajduje się w add-on store, nie oznacza to że został zatwierdzony lub sprawdzony przez organizację NV Access, czy kogokolwiek innego.
Najważniejsze jest to, abyś instalował dodatki z zaufanych źródeł.
Funkcjonalność dodatków jest nieograniczona wewnątrz NVDA. 
To może włączać dostęp do twoich danych osobowych lub nawet twojego systemu.

Możesz instalować dodatki [przeglądając dostępne dodatki](#AddonStoreBrowsing).
Wybierz dodatek z jednej z kart właściwości "otkrywajj" lub "do zaktualizowania".
Potem użyj działania zaktualizuj, zainstaluj, lub zamień, aby rozpocząć instalację.

Także możesz instalować wiecej dodatków od razu.
To można zrobić, zaznaczając więcej dodatków na karcie właściwości otkryj dodatki, a potem aktywując menu kontekstowe na zaznaczeniu i wybierając działanie "Zainstaluj wybrane dodatki".

Aby zainstalować dodatek pobrany spoza add-on store, naciśnij przycisk "zainstaluj z pliku".
To umożliwi poszukiwanie pliku pakietu dodatku (`.nvda-addon`) gdzieś na twoim komputerze lub w sieci.
Gdy otworzysz pakiet dodatku dla NVDA, rozpocznie się instalacja.

Jeżeli NVDA jest już zainstalowana w twoim systemie, możesz także otworzyć plik dodatku bezpośrednio z przeglądarki lub systemu plików, aby rozpocząć proces jego instalacji.

Gdy dodatek jest instalowany z pliku, NVDA zapyta cie o potwierdzenie chęci instalacji dodatku.
Kiedy dodatek zostanie zainstalowany, program NVDA musi być ponownie uruchomiony, aby dodatek zaczął działać. Jeżeli chcesz zainstalować lub zaktualizować inne dodatki, możesz odłożyć ponowne uruchomienie NVDA na później.

#### Usuwanie dodatków {#AddonStoreRemoving}

Aby usunąć dodatek, wybierz go z listy i użyj działania usuń.
NVDA poprosi cię o potwierdzenie usunięcia.
Tak jak w przypadku instalacji, program NVDA musi zostać ponownie uruchomiony, żeby dodatki mogły być usunięte w całości.
Dopóki tej akcji nie wykonasz, stan "oczekiwanie na usunięcie" będzie pokazywany dla tego dodatku na liście.
Tak jak podczas instalacji, możesz usuwać więcej dodatków od razu.

#### Wyłączanie i włączanie dodatków {#AddonStoreDisablingEnabling}

Aby wyłączyć dodatek, użyj działania "wyłącz".
Aby włączyć poprzednio wyłączony dodatek, użyj działania "włącz".
Dodatek możesz wyłączyć, jeżeli jego stan wskazuje  "włączony", lub go włączyć, jeżeli dodatek jest "wyłączony".
Po każdym użyciu działania wyłącz/włącz, zmienia się stan, żeby pokazać, co się stanie z dodatkiem po ponovnym uruchomieniu NVDA.
Jeżeli dodatek został poprzednio wyłączony", stan pokaże "włączony dopiero po ponownym uruchomieniu".
jeżeli dodatek został poprzednio "włączony", stan pokaże "wyłączony dopiero po ponownym uruchomieniu".
Tak jak przy instalacji lub usuwaniu dodatków, musisz ponownie uruchomić NVDA, aby zmiany zadziałały.
Możesz także włączać lub wyłączać  więcej dodatków od razu zaznaczając je na karcie włąściwości otkrywaj dodatki, potem aktywując menu kontekstowe na zaznaczeniu i wybierając odpowiednie działanie.

#### Recenzja dodatków i czytanie recenzji {#AddonStoreReviews}

Możesz zechcieć przeczytać recenzje dodatku innych użytkowników, w celu dowiadywania się o jego użyteczności, albo w procesie nauki używania tego dodatku.
Także pomocne jest dawanie informacji zwrotnych użytkownikom, którzy chcą się dowiedzieć o dodatku.
Aby przeczytać recenzje dla dodatku, zaznacz go, i użyj działania "Recenzje społeczności".
To działanie przekierowuje na stronę dyskusji GitHub, na której możesz przeczytać lub napisać recenzję dodatku.
Miewaj na uwadzę, że ta opcja nie jest zamiennikiem bezpośredniej komunikacji z autorami dodatków.
Zamiast tego, celem tej funkcji jest dzielenie się informacją zwrotną, która ma pomóc użytkownikom zdecydować się czy dodatek jest użyteczny dla nich, czy nie.

### Niezgodne dodatki {#incompatibleAddonsManager}

Niektóre starsze dodatki mogą być niezgodne z wersją NVDA, którą posiadasz.
Jeżeli używasz starszej wersji NVDA, niektóre nowsze dodatki mogą także być niezgodne.
Próba zainstalowania niezgodny dodatek skutkuje błędem objaśniającym, czemu dodatek jest niezgodny.

Dla starszych dodatków, możesz nadpisać zgodność na własną odpowiedzialność.
Niezgodne dodatki mogą nie działać w nowszej wersji NVDA i mogą spowodować niepożądane skutki, włączając w to wysypywanie się.
Możesz nadpisać zgodność przed włączeniem lub instalacją dodatku.
Jeżeli niezgodny dodatek sprawia problemy, możesz go usunąć lub wyłączyć.

Wrazie kłopotów z uruchamianiem NVDA Po niedawnej aktualizacji lub instalacji dodatku, zwłaszcza jeżeli jest to dodatek niezgodny, możesz spróbować uruchomić NVDA tymczasowo z wyłączonymi wszystkimi dodatkami.
Aby uruchomić NVDA ponownie z wszystkimi wyłączonymi dodatkami, wybierz odpowiednią opcję podczas wyłączania NVDA.
ewentualnie użyj [opcji wiersza poleceń](#CommandLineOptions) `--disable-addons`.

Możesz przeglądać dostępne niezgodne dodatki używając którejś z kart właściwości [otkryj i dodatki do zaktualizowania](#AddonStoreFilterStatus).
Możesz przeglądać zainstalowane niezgodne dodatki używając [karty właściwości niezgodne dodatki](#AddonStoreFilterStatus).

## Dodatkowe narzędzia {#ExtraTools}
### Podgląd logu {#LogViewer}

Opcja Podgląd logu, którą można znaleźć w menu narzędzia, umożliwia przegląd dziennika zdarzeń od ostatniego uruchomienia NVDA.

Oprócz odczytu treści, możesz zapisać kopiępliku dziennika, albo odświeżyć dziennik, żeby pokazać nowe zdarzenia.
Te działania dostępne są w menu Log w podglądzie logu.

Plik, który wyświetla się podczas otwarcia podglądu logu, znajduje się na twoim komputerze w następującej lokalizacji: `%temp%\nvda.log`.
Podczas każdego uruchamiania NVDA, tworzony jest nowy plik dziennika.
Gdy to się stanie, poprzedni plik dziennika jest zapisany do pliku `%temp%\nvda-old.log`.

Możesz także skopiować fragment dziennika bez otwierania podglądu logu.
<!-- KC:beginInclude -->

| Nazwa |Skrót |Opis|
|---|---|---|
|Otwórz podgląd logu |`NVDA+f1` |Otwiera podgląd logu i wyświetla informacje dla programistów o aktualnym obiekcie nawigatora.|
|Kopiuj fragment dziennika do schowka |`NVDA+control+shift+f1` |Gdy ten skrót jest naciśnięty raz, ustawiony jest punkt początkowy do przechwytywanego fragmentu dziennika. Naciśnięty drugi raz, it kopiuję dziennik od punktu zaznaczenia do schowka.|

<!-- KC:endInclude -->

### Podgląd mowy {#SpeechViewer}

Dla widzących twórców oprogramowania albo osób demonstrujących działanie NVDA szerszej publiczności osób widzących, dostępne jest ruchome okno wyświetlające to, co NVDA aktualnie wypowiada.

Aby włączyć podgląd mowy, zaznacz pozycję "Podgląd Mowy" w menu Narzędzia. 
Aby wyłączyć tę opcję, usuń zaznaczenie "Podgląd Mowy" w menu .

Okno podglądu mowy zawiera pole wyboru "Pokaż podgląd mowy przy starcie".
Jeśli jest zaznaczone, podgląd mowy otworzy się po starcie NVDA.
Okno podglądu mowy będzie zawsze pojawiało się w tym samym miejscu i w takich samych rozmiarach, jakie ustawione były w chwili jego zamknięcia .

Gdy podgląd mowy jest włączony, jego okienko stale się odświeża by pokazać aktualnie wypowiadany tekst.
Gdy przeniesiesz mysz lub umieścisz fokus wewnątrz podglądu, NVDA tymczasowo zatrzyma aktualizację tekstu, dzięki czemu możesz łatwo zaznaczyć lub skopiować istniejące treści.

Aby przełączać podgląd mowy z każdego miejsca, zdefiniuj własne zdarzenie wejścia używając [okna Zdarzenia wejścia](#InputGestures).

### Podgląd brajla {#BrailleViewer}

Dla widzących deweloperów, czy też dla ludzi pokazujących NVDA społeczności osób widzących program oferuje niewielkie pływające u góry ekranu okienko umożliwiające podglądanie aktualnie wyświetlanego tekstu w alfabecie Braille'a.
Funkcja podglądu brajla może być używana w raz z fizycznym monitorem brajlowskim. W takim wypadku ilość komórek na wirtualnym monitorze stanie się równa ilości komórek na monitorze fizycznym.
Gdy ta funkcja jest włączona, wirtualne wyjście brajla jest ciągle pokazywane, w celu reflektowania najnowszych zmian.

W celu włączenia podglądu brajla, zaznacz odpowiednie pole wyboru w menu narzędzia programu NVDA.
Odznacz to pole, aby podgląd nie był już wyświetlany.

Fizyczne monitory brajlowskie przeważnie posiadają przyciski umożliwiające przewijanie tekstu. Aby włączyć możliwość przewijania wirtualnego monitora korzystającego z funkcji podglądu brajla użyj ekranu [zdarzenia wejścia](#InputGestures) w celu przypisania skrótów klawiszowych "Przewija monitor brajlowski w dół" and "przwija monitor brajlowski w górę".

Okno podglądu brajla zawiera pole wyboru umożliwiające włączanie tej funkcji przy każdym starcie programu NVDA.
Jeżeli zostanie ono zaznaczone, to podgląd brajla będzie ładował się przy każdym starcie programu.
Okno podglądu brajla dokona próby otwarcia się z takimi samymi wymiarami i w takiej samej pozycji, w jakiej zostało ono zamknięte.

Okno przegląd brajla zawiera pole wyboru  "przesuwanie po komórkach brajlowskich za pomocą myszy", które domyślnie jest odznaczone.
Jeżeli to pole wyboru jest zaznaczone, przemieszczanie się po komórce brajlowskiej wywoła polecenie "przenieś się do komórki brajlowskiej" dla wybranej komórki.
Często jest to używane do wywołania akcji oraz do ustawiania kursora na konkretną komórkę.
Jest to korzystne, kiedy testujemy przekształcanie brajlowskich komórek na znaki i odwrotnie.
Aby zapobiec niechciane przywoływanie komórek, polecenie jest opóźnione.
Mysz powinna się ruszać do póki komórka nie stanie się zielona.
Na początku kursor myszy będzie światło żólty, potem kolor zmieni się na pomorańczowy, a potem stanie się zielony.

Aby się dostać do przeglądu brajla z każdego miejsca, prosimy przydzielić zdarzenie wejścia używając [okno dialogowe zdarzeń wejścia](#InputGestures).

### Konsola Pythona {#PythonConsole}

Konsola Pythona NVDA znajduje się w menu Narzędzia  w NVDA. Jest narzędziem dla programistów i jest używana do debugowania, przeglądania wewnątrz NVDA lub sprawdzania hierarchii dostępności aplikacji.
Więcej informacji znajduje się w [podręczniku dla twórców](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Add-on Store {#AddonStoreMenuItem}

Ta opcja otworzy [NVDA Add-on Store](#AddonsManager).
Aby się dowiedzieć więcej, przeczytaj szczegółowy rozdział: [Dodatki i Add-on Store](#AddonsManager).

### Utwórz kopię przenośną {#CreatePortableCopy}

Polecenie to pozwala otworzyć okno, przy pomocy którego można utworzyć kopię przenośną NVDA z zainstalowanej na dysku wersji.
Natomiast w wypadku, gdy NVDA jest już zainstalowane nazwa opcji będzie brzmiała "Zainstaluj przenośną kopię na dysku" zamiast "Utwórz przenośną kopię".

Okno dialogowe tworzenia przenośnej kopii lub instalowania NVDA z przenośnej wersji pozwala wybrać użytkownikowi katalog w którym zostanie utworzona przenośna wersja, albo katalog, w którym program zostanie zainstalowany.

W oknie tym można również zmienić opcje takie jak:

* Skopiuj aktualną konfigurację użytkownika: pozwala skopiować ustawienia, dodatki oraz inne moduły do nowo instalowanej wersji programu.
* Uruchom nowo powstałą kopię przenośną NVDA lub uruchom nowo zainstalowaną kopię NVDA: pozwala uruchomić program po zakończeniu jego instalatora.

### uruchom narzędzie do naprawy błędów rejestracji COM... {#RunCOMRegistrationFixingTool}

W pewnych przypadkach instalacja/deinstalacja programów może doprowadzić pliki .DLL i .COM do wyrejestrowania.
Niektóre interfejsy .COM takie jak IAccessible2 wymagają poprawnej rejestracji innych plików .COM.

Może się tak zdarzyć na przykład po odinstalowaniu programu Adobe Reader lub Math Player.

Niepoprawnie zarejestrowane pliki .COM mogą powodować problemy na pasku zadań, w przeglądarkach, aplikacjach i innych interfejsach.

Następujące problemy mogą zostać poprawione dzięki temu narzędziu:

* NVDA nie odczytuje elementów podczas nawigacji w przeglądarkach Firefox, Thunderbird ETC.
* NVDA nie może przełączać się pomiędzy trybem formularzy i czytania.
* NVDA reaguje bardzo powoli na polecenia w przeglądarkach.
* I inne.

### przeładuj wtyczki {#ReloadPlugins}

Po aktywacji tego polecenia wszystkie moduły aplikacji oraz wtyczki zostaną przeładowane bez potrzeby restartu NVDA. Jest to użyteczne dla programistów.
Moduły aplikacji zarządzają interakcją pomiędzy NVDA i określonymi aplikacjami.
Wtyczki globalne zarządzają interakcją NVDA z wszystkimi aplikacjami.

Następujące polecenia NVDA mogą być użyteczne:
<!-- KC:beginInclude -->

| Nazwa |Skrót |Opis|
|---|---|---|
|Przeładuj wtyczki |`NVDA+control+f3` |Przeladowuje wtyczki globalne i moduły aplikacji NVDA.|
|Przeczytaj wczytany moduł aplikacji i plik wykonywalny |`NVDA+control+f1` |Odczytuję nazwę modułu aplikacji, jeżeli istnieje, i nazwę pliku wykonywalnego skojarzoną z nim.|

<!-- KC:endInclude -->

## Obsługiwane syntezatory mowy {#SupportedSpeechSynths}

Ten rozdział zawiera informacje na temat syntezatorów mowy wspieranych przez NVDA.
Dla jeszcze bardziej rozszerzonej listy darmowych i komercyjnych syntezatorów, które możesz pobrać i zakupić do użytkowania z NVDA, proszę zajrzeć na stronę [extra voices](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

[eSpeak NG](https://github.com/espeak-ng/espeak-ng) jest to syntezator wbudowany bezpośrednio w NVDA i nie wymaga specjalnych sterowników lub innych komponentów, które muszą być zainstalowane. 
W systemie Windows 8.1, NVDA używa domyślnie syntezatora eSpeak NG. ([Głosy Windows OneCore](#OneCore) natomiast, są używane w systemie Windows 10 i nowszych jego wersjach.
Jako że syntezator ten jest wbudowany w NVDA, jest to doskonały wybór przy uruchamianiu NVDA z napędu USB na innych systemach.

Każdy głos eSpeak NG, mówi innym językiem. 
Ponad 43 różne języki są  obsługiwane przez eSpeak NG.

Istnieje również wiele wariantów, które mogą być wybrane do zmiany brzmienia głosu.

### Microsoft Speech API version 4 (SAPI 4) {#SAPI4}

SAPI 4 to starszy standard oprogramowania Microsoftu dla syntezatorów mowy.
NVDA nadal obsługuje ten standard dla użytkowników, którzy już posiadają zainstalowane syntezatory SAPI 4.
Microsoft jednak nie wspiera już tego standardu i potrzebne komponenty nie są już dostępne ze strony Microsoft.

Podczas korzystania przez NVDA z tych syntezatorów, można zmieniać głosy w kategorii [Mowa](#SpeechSettings) w oknie [Preferencji NVDA](#NVDASettings) lub poprzez [Szybką zmianę ustawień syntezatora](#SynthSettingsRing). Dostępne są wszystkie głosy ze wszystkich zainstalowanych silników SAPI4 znalezionych w systemie.

### Microsoft Speech API version 5 (SAPI 5) {#SAPI5}

SAPI 5 to standard Microsoftu dla oprogramowania syntezatorów mowy.
Wiele syntezatorów mowy, które są zgodne z tym standardem można nabyć z różnych firm lub pobrać ze stron internetowych. W twoim systemie jest już prawdopodobnie zainstalowany co najmniej jeden głos SAPI5.
Podczas korzystania przez NVDA z tego syntezatora, dostępne głosy w kategorii [Mowa](#SpeechSettings) w oknie [Preferencji NVDA](#NVDASettings) lub poprzez [Szybką zmianę ustawień syntezatora](#SynthSettingsRing) zawierają wszystkie głosy ze wszystkich zainstalowanych silników SAPI5 znalezionych w systemie.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Ten standard dostarcza głosów dla wielu języków, zwykle używanych  w rozwoju aplikacji korzystających z architektury serwerowej. 
Głosy te mogą także zostać użyte z NVDA.

Aby użyć tych głosów, musisz zainstalować dwa komponenty:

* [Microsoft Speech Platform - Runtime (wersja 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime języki (wersja 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Ta strona zawiera wiele plików dla rozpoznawania mowy i zamiany tekstu na mowę.
 Wybierz pliki TTS (Text-to-speech - tekst na mowę) zawierające dane dla potrzebnych języków i głosów.
 Dla przykładu, plik  MSSpeech_TTS_en-US_ZiraPro.msi jest to głos w języku Angielskim (stany zjednoczone).

### Głosy Windows OneCore {#OneCore}

System operacyjny Windows 10 i nowsze jego wersje zawierają nowe głosy znane jako "OneCore" lub głosy "mobilne".
Dostarczone są głosy dla wielu języków, są bardziej responsywne niż głosy Microsoft dostępne przy użyciu Microsoft Speech API version 5.
W systemie Windows 10 i nowszych jego wersjach, NVDA domyślnie używa głosów Windows One Core ([[eSpeak NG](#eSpeakNG) natomiast, używany jest w innych wydaniach systemu operacyjnego.

Aby dodać nowe Głosy Windows OneCore, proszę wejść do kategorii "mowa", znajdującej się w ustawieniach systemu Windows. 
Trzeba użyć opcji "dodawanie głosu" i znaleźć odpowiedni język.
Większość języków posiada więcej odmian.
Angielski "Zjednoczone królestwo" i angielski "australijski" są dwie odmiany angielskiego.
Dostępne odmiany języka francuskiego to"francuski (Francja)", "Kanadyjski" i "Szwajcarski".
Znajdź szerszą kategorię języka (taką jak angielski lub francuzki), a potem znajdź odmianę na liście.
Wybierz jakikolwiek potrzebny język i naciśnij "przycisk dodaj" aby je dodać.
Po dodaniu języków, ponownie uruchom NVDA.

Aby się dowiedzieć o dostępnych głosach i językach, [Prosimy przeczytać tę listę](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01).

## Obsługiwane monitory brajlowskie {#SupportedBrailleDisplays}

Ten rozdział zawiera informacje na temat monitorów brajlowskich wspieranych przez NVDA.

### Linijki automatycznie wykrywane w tle {#AutomaticDetection}

NVDA może automatycznie wykrywać w tle wiele linijek brajlowskich, podłączonych przez USB lub bluetooth.
To zachowanie ma miejsce, jeśli wybrano opcję automatycznie [w oknie ustawień brajla w NVDA](#BrailleSettings) na liście dostępnych linijek brajlowskich.
Ta opcja jest wybrana domyślnie.

Poniższe linijki brajlowskie mogą być automatycznie wykrywane.

* Handy Tech 
* Baum/Humanware/APH/Orbit 
* HumanWare serie Brailliant BI/B 
* HumanWare BrailleNote
* SuperBraille
* Optelec serii ALVA 6 
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille
* Eurobraille Esys/Esytime/Iris
* Monitory brajlowskie Nattiq nBraille
* Seika Notetaker: MiniSeika (16, 24 znakowe), V6, i V6Pro (40 znakowe)
* Monitory brajlowskie Tivomatic Caiku Albatross 46/80
* Jakikolwiek monitor brajlowski wspierający standardowy HID protokół brajlowski

### Freedom Scientific Focus/PAC Mate Series {#FreedomScientificFocus}

Wszystkie monitory Focus i PAC Mate firmy [Freedom Scientific](https://www.freedomscientific.com/) są obsługiwane w trybie połączeń USB i Bluetooth.
Niezbędne są sterowniki brajlowskie Freedom Scientific zainstalowane w systemie.
Jeżeli jeszcze nie posiadasz tych sterowników możesz je pobrać ze strony [Focus Blue Braille Display Driver page](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Na podanej stronie wymieniony jest tylko sterownik monitora Focus Blue, ale obsługuje on wszystkie monitory Freedom Scientific i Pacmate.

Domyślnie NVDA może wykryć i podłączyć się do tych monitorów przez USB lub bluetooth.
Konfigurując monitor, możesz wymusić połączenie "USB" or "Bluetooth" aby ograniczyć używany typ połączenia.
Może to być przydatne, jeśli chcesz połączyć się z monitorem Focus przez bluetooth, ale móc jednocześnie ładować urządzenie z komputera przez port USB.
Automatyczne wykrywanie linijek brajlowskich przez NVDA  będzie wykrywać urządzenia podłączone przez USB lub Bluetooth.

Poniżej znajdują się klawisze skrótów NVDA dla tego monitora.
Zajrzyj do dokumentacji monitora, aby dowiedzieć się gdzie znajdują się opisywane klawisze.
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |TopRouting1 (pierwsza komórka na wyświetlaczu)|
|Przewiń wyświetlacz brajla w przód |TopRouting20/40/80 (ostatnia komórka na wyświetlaczu)|
|Przewiń wyświetlacz brajla wstecz |Left Advance Bar|
|Przewiń wyświetlacz brajla w przód |Right Advance Bar|
|Przełącz "Brajl związany z..." |Left GDF Button+Right GDF Button|
|Przełącz działanie lewego pokrętła |LeftWizWheelPress|
|Przejdź wstecz używając akcji lewego pokrętła |LeftWizWheelUp|
|Przejdź w przód używając akcji lewego pokrętła |Left Wiz Wheel Down|
|Przełącz akcję prawego pokrętła |Right Wiz Wheel Press|
|Przejdź wstecz używając akcji prawego pokrętła |RightWizWheelUp|
|Przejdź w przód używając akcji prawego pokrętła |RightWizWheelDown|
|Przywołaj do komórki brajla |Routing|
|Klawisz Shift+Tab |Brajlowska spacja+Punkt 1+Punkt 2|
|Klawisz Tab |Brajlowska spacja+Punkt 4+Punkt 5|
|Klawisz strzałki w górę |Brajlowska spacja+Punkt 1|
|Klawisz strzałki w dół |Brajlowska spacja+Punkt 4|
|Klawisz Ctrl+Strzałka w lewo |Brajlowska spacja+Punkt 2|
|Klawisz Ctrl+Strzałka w prawo |Brajlowska spacja+Punkt 5|
|Klawisz Strzałka w lewo |Brajlowska spacja+Punkt 3|
|Klawisz Strzałka w prawo |Brajlowska spacja+Punkt 6|
|Klawisz Home |Brajlowska spacja+Punkt 1+Punkt 3|
|Klawisz End |Brajlowska spacja+Punkt 4+Punkt 6|
|Klawisz Ctrl+Home |Brajlowska spacja+Punkt 1+Punkt 2+Punkt 3|
|Klawisz Ctrl+End |Brajlowska spacja+Punkt 4+Punkt 5+Punkt 6|
|Klawisz Alt |Brajlowska spacja+Punkt 1+Punkt 3+Punkt 4|
|Klawisz Alt+Tab |Brajlowska spacja+Punkt 2+Punkt 3+Punkt 4+Punkt 5|
|Klawisz alt+shift+tab |brajlowska spacja +punkt1+punkt2+punkt5+punkt6|
|Klawisz windows+tab |brajlowska spacja +punkt2+punkt3+punkt4|
|Klawisz Escape |Brajlowska spacja+Punkt 1+Punkt 5|
|Klawisz Windows |Brajlowska spacja+Punkt 2+Punkt 4+Punkt 5+Punkt 6|
|Klawisz spacja |Brajlowska spacja|
|Przełącza klawisz control |spacja+punkt3+punkt8|
|Przełącza klawisz alt |spacja+punkt6+punkt8|
|Przełącza klawisz windows |spacja+punkt4+punkt8|
|przełącza klawisz NVDA |spacja+punkt5+punkt8|
|przełącza klawisz shift |spacja+punkt7+punkt8|
|przełącza control i shift |spacja+punkt3+punkt7+punkt8|
|przełącza alt i shift |spacja+punkt6+punkt7+punkt8|
|przełącza windows i shift |spacja+punkt4+punkt7+punkt8|
|przełącza NVDA i shift |spacja+punkt5+punkt7+punkt8|
|przełącza control i alt |spacja+punkt3+punkt6+punkt8|
|przełącza control, alt, i shift |spacja+punkt3+punkt6+punkt7+punkt8|
|Klawisz Windows+D (minimalizuje wszystkie okna) |Brajlowska spacja+Punkt 1+Punkt 2+Punkt 3+Punkt 4+Punkt 5+Punkt 6|
|Odczytaj bieżącą linię |Brajlowska Spacja+Punkt 1+Punkt 4|
|Menu NVDA |Brajlowska Spacja+Punkt 1+Punkt 3+Punkt 4+Punkt 5|

Dla nowszych modeli Focus posiadających klawisze rocker bar (focus 40, focus 80 i focus blue):

| Działanie |Klawisz skrótu|
|---|---|
|Przenieś wyświetlacz do poprzedniej linii |LeftRockerBarUp, rightRockerBarUp|
|Przenieś wyświetlacz do następnej linii |LeftRockerBarDown, rightRockerBarDown|

Tylko dla Focus 80:

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz wstecz |LeftBumperBarUp, rightBumperBarUp|
|Przewiń wyświetlacz na przód |LeftBumperBarDown, RightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA  serie 6 / konwerter protokołu {#OptelecALVA}

Zarówno model ALVA BC640 i BC680 firmy [Optelec](https://www.optelec.com/) są obsługiwane przy połączeniu przez USB i bluetooth.
Alternatywnie, można podłączyć starszą linijkę Optelec, np. Braille Voyager, przy użyciu konwertera protokołu dostarczanego przez Optelec.
Linijki nie wymagają instalacji żadnych sterowników dla prawidłowego działania.
Wystarczy podłączyć monitor i skonfigurować NVDA aby z niego korzystał.

Uwaga: NVDA może nie być w stanie używać linijki ALVA BC6 podłączonej przez bluetooth, gdy jest ona sparowana przy pomocy narzędzia ALVA Bluetooth utility.
Jeśli sparowano urządzenie przy pomocy tego narzędzia i NVDA nie może go wykryć, zalecamy sparowanie linijki ALVA w zwykły sposób przy użyciu ustawień Bluetooth Windows.

Niektóre z tych monitorów posiadają klawiaturę brajlowską, ale same wykonują proces zamiany brajla na tekst.
Ustawienia tabeli wprowadzania brajla w NVDA nie mają w związku z tym zastosowania.
Dla monitorów ALVA z najnowszym firmware, możliwe jest wyłączenie tej symulacji klawiatury HID przy pomocy zdarzenia wejścia.

Poniżej klawisze monitorów, których możesz używać z NVDA. 
Aby je odnaleźć, zajrzyj do dokumentacji urządzenia.
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń brajl do tyłu |T1, Etouch1|
|Przenieś monitor do poprzedniej linii |T2|
|Przenieś do fokusa |T3|
|Przenieś monitor do następnej linii |T4|
|Przewiń brajl do przodu |T5, Etouch3|
|Przywołaj do komórki brajla |Routing|
|Zgłoś formatowanie tekstu pod komórką brajla |drugi routing|
|Przełącz symulację klawiatury HID |t1+spEnter|
|Przenieś do pierwszej linii w przeglądzie |T1+T2|
|Przenieś do ostatniej linii w przeglądzie |T4+T5|
|Przełącz brajl związany z |T1+T3|
|Odczytaj tytuł |Etouch2|
|Odczytaj pasek stanu |Etouch4|
|Klawisz Shift+Tab |Sp1|
|Klawisz Alt |Sp2, alt|
|Klawisz Escape |Sp3|
|Klawisz Tab |Sp4|
|Klawisz Strzałka w górę |Sp Up|
|Klawisz Strzałka w dół |Sp Down|
|Klawisz Strzałka w lewo |Sp Left|
|Klawisz Strzałka w prawo |Sp Right|
|Klawisz Enter |SpEnter, enter|
|Odczytaj datę/czas |sp2+sp3|
|Menu NVDA |Sp1+Sp3|
|Klawisz Windows+D (minimalizuje wszystkie okna) |Sp1+Sp4|
|Klawisz Windows+B (przejdź do zasobnika systemowego) |Sp3+Sp4|
|Klawisz Windows |sp1+sp2, windows|
|Klawisz Alt+Tab |Sp2+Sp4|
|Klawisz Ctrl+Home |T3+Sp Up|
|Klawisz Ctrl+End |T3+Sp Down|
|Klawisz Home |T3+Sp Left|
|Klawisz End |T3+Sp Right|
|Klawisz control |control|

<!-- KC:endInclude -->

### Monitory Handy Tech {#HandyTech}

NVDA obsługuje większość monitorów firmy [Handy Tech](https://www.handytech.de/) podłączonych przez USB, port szeregowy lub bluetooth.
W przypadku starszych monitorów USB, należy zainstalować sterowniki USB dla Handy Tech w systemie.

Poniższe monitory nie są obsługiwane bezpośrednio, ale mogą być używane przy pomocy [uniwersalnego sterownika Handy Tech](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) i dodatku NVDA:

* Braillino
* Bookworm
* Monitory serii Modular z wersją firmware 1.13 i niższą. Proszę zauważyć, że firmware tych urządzeń może zostać zaktualizowane.

Poniżej skróty klawiszowe dla monitorów Handy tech, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń brajla do tyłu |Left, Up, b3|
|Przewiń brajla do przodu |Right, Down, b6|
|Przenieś monitor do poprzedniej linii |B4|
|Przenieś monitor do następnej linii |B5|
|Przywołaj do komórki brajla |Routing|
|Klawisz Shift+Tab |lewy klawisz potrójnej akcji góra+dół|
|Klawisz Alt |B2+B4+B5|
|Klawisz Escape |B4+B6|
|Klawisz Tab |enter, prawy klawisz potrójnej akcji góra +dół|
|Klawisz Enter |esc+enter, lewo+prawy klawisz potrójnej akcji góra +dół, joystickAction|
|Strzałka w górę |joystick góra|
|Strzałka w dół |joystick dół|
|Strzałka w lewo |joystick lewo|
|Strzałka w prawo |joystick prawo|
|Menu NVDA |B2+B4+B5+B6|
|Przełącz brajl związany z |b2|
|Przełącz kursor brajla |b1|
|Przełącz prezentację kontekstu fokusa |b7|
|Przełącz wprowadzanie brajla |spacja+b1+b3+b4 (spacja+duże B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

Monitor Lilli Braille firmy [MDV](https://www.mdvbologna.it/) jest obsługiwany przez NVDA.
Nie wymaga instalacji żadnych specjalnych sterowników.
Wystarczy podłączyć monitor i skonfigurować NVDA aby go używał.

Ta linijka nie jest obsługiwana przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.

Poniżej skróty klawiszowe dla tego monitora, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |LF|
|Przewiń wyświetlacz brajla w przód |RG|
|Przenieś wyświetlacz brajla do poprzedniej linii |UP|
|Przenieś wyświetlacz brajla do następnej linii |DN|
|Przywołaj do komórki brajla |Route|
|Klawisz Shift+Tab |SLF|
|Klawisz Tab |SRG|
|Klawisz Alt+Tab |SDN|
|Klawisz Alt+Shift+Tab |SUP|

<!-- KC:endInclude -->

### Monitory brajlowskie Baum/Humanware/APH/Orbit {#Baum}

Kilka monitorów firm [Baum](https://www.baum.de/cms/en/), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) i [Orbit](https://www.orbitresearch.com/) jest obsługiwanych przez USB i bluetooth.
Wśród nich:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Niektóre inne monitory produkowane przez Baum mogą również działać, ale nie zostało to przetestowane.

Przy połączeniu przez USB do monitorów, które nie używają HID, musisz najpierw zainstalować sterowniki USB dostarczone przez producenta.
VarioUltra i Pronto! używają HID.
Refreshabraille i Orbit Reader 20 mogą używać HID, jeśli są odpowiednio skonfigurowane.

Tryb szeregowy USB monitora Orbit Reader 20 jest obsługiwany obecnie tylko w Windows 10 i nowszych wersjach systemu operacyjnego Windows.
USB HID zasadniczo powinien być używany zamiast tego.

Poniżej skróty klawiszowe dla tych monitorów, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń monitor brajlowski wstecz |`d2`|
|Przewiń monitor brajlowski w przód |`d5`|
|Przewiń monitor brajlowski do poprzedniej linii |`d1`|
|Przewiń monitor brajlowski do następnej linii |`d3`|
|Przywołaj do komórki brajlowskiej |`routing`|
|`shift+tab` |`spacja+punkt1+punkt3`|
|`tab` |`spacja+punkt4+punkt6`|
|`alt` |`spacja+punkt1+punkt3+punkt4` (`spacja+m`)|
|`escape` |`spacja+punkt1+punkt5` (`spacja+e`)|
|`windows` |`spacja+punkt3+punkt4`|
|`alt+tab` |`spacja+punkt2+punkt3+punkt4+punkt5` (`spacja+t`)|
|Menu NVDA |`spacja+punkt1+punkt3+punkt4+punkt5` (`spacja+n`)|
|`windows+d` (minimalizowanie wszystkich aplikacji) |`spacja+punkt1+punkt4+punkt5` (`spacja+d`)|
|Czytaj wszystko |`spacja+punkt1+punkt2+punkt3+punkt4+[punkt5+punkt6`|

Dla monitorów z joystickiem:

| Działanie |Klawisz skrótu|
|---|---|
|Klawisz Strzałka w górę |Up|
|Klawisz Strzałka w dół |Down|
|Klawisz Strzałka w lewo |Left|
|Klawisz Strzałka w prawo |Right|
|Klawisz Enter |Select|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

Hedo ProfiLine USB produkcji [hedo Reha-Technik](https://www.hedo.de/) jest obsługiwany.
Musisz najpierw zainstalować sterowniki USB dostarczane przez producenta.

Ta linijka nie jest jeszcze obsługiwana przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.

Poniżej skróty klawiszowe dla tego monitora, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |K1|
|Przewiń wyświetlacz brajla w przód |K3|
|Przenieś wyświetlacz brajla do poprzedniej linii |B2|
|Przenieś wyświetlacz brajla do następnej linii |B5|
|Przywołaj do komórki brajla |Routing|
|Przełącz "Brajl związany z..." |K2|
|Czytaj wszystko |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

Hedo MobilLine USB produkcji [hedo Reha-Technik](https://www.hedo.de/) jest obsługiwany.
Musisz najpierw zainstalować sterownik USB dostarczany przez producenta.

Ta linijka nie jest jeszcze obsługiwana przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.

Poniżej skróty klawiszowe dla tego monitora, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |K1|
|Przewiń wyświetlacz brajla w przód |K3|
|Przenieś wyświetlacz brajla do poprzedniej linii |B2|
|Przenieś wyświetlacz brajla do następnej linii |B5|
|Przywołaj do komórki brajla |Routing|
|Przełącz "Brajl związany z..." |K2|
|Czytaj wszystko |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Series/ BrailleNote Touch {#HumanWareBrailliant}

Serie monitorów Brailliant BI i B produkcji [HumanWare](https://www.humanware.com/), włącznie z BI 14, BI 32, BI 20X, BI 40, BI 40X i B 80, są obsługiwane przy połączeniu przez USB i bluetooth.
Przy połączeniu przez USB z protokołem ustawionym na HumanWare, trzeba najpierw zainstalować sterowniki USB dostarczone przez producenta.
Sterowniki USB nie są wymagane, jeśli protokół jest ustawiony na OpenBraille.

Następujące urządzenia również nie wymagają instalacji dodatkowych sterowników USB:

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Poniżej skróty klawiszowe dla Brailliant BI/B i BrailleNote touch, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia.

#### Przypisania klawiszy dla wszystkich modeli {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do poprzedniej linii |Up|
|Przenieś wyświetlacz brajla do następnej linii |Down|
|Przywołaj do komórki brajla |Routing|
|Przełącz "Brajl związany z..." |Up+Down|
|Klawisz Strzałka w górę |Spacja+Punkt 1|
|Klawisz Strzałka w dół |Spacja+Punkt 4|
|Klawisz Strzałka w lewo |Spacja+Punkt 3|
|Klawisz Strzałka w prawo |Spacja+Punkt 6|
|Klawisz Shift+Tab |Spacja+Punkt 1+Punkt 3|
|Klawisz Tab |Spacja+Punkt 4+Punkt 6|
|Klawisz Alt |Spacja+Punkt 1+Punkt 3+Punkt 4 (Spacja+M)|
|Klawisz Escape |Spacja+Punkt 1+Punkt 5 (Spacja+e)|
|Klawisz Enter |Punkt 8|
|Klawisz Windows |Spacja+Punkt 3+Punkt 4|
|Klawisz Alt+Tab |Spacja+Punkt 2+Punkt 3+Punkt 4+Punkt 5 (Spacja+T)|
|Menu NVDA |spacja+punkt 1+punkt 3+punkt 4+punkt 5 (spacja+n)|
|windows+d (minimalizuje wszystkie aplikacje) |spacja+punkt 1+punkt 4+punkt 5 (spacja+d)|
|Czytaj wszystko |spacja+punkt 1+punkt 2+punkt 3+punkt 4+punkt 5+punkt 6|

<!-- KC:endInclude -->

#### Przypisania klawiszy dla Brailliant BI 32, BI 40 and B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Menu NVDA |c1+c3+c4+c5 (command n)|
|windows+d (minimalizuj wszystkie aplikacje) |c1+c4+c5 (command d)|
|Czytaj wszystko |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Przypisania klawiszy dla Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Strzałka w górę |joystick góra|
|Strzałka w dół |joystick dół|
|Strzałka w lewo |joystick lewo|
|Strzałka w prawo |joystick prawo|
|Klawisz enter |joystick akcja|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille {#Hims}

NVDA obsługuje monitory Braille Sense, Braille EDGE, Smart Beetle i Sync Braille produkcji [Hims](https://www.hims-inc.com/) przy połączeniu przez USB i bluetooth. 
Jeżeli podłączasz monitor brajlowski za pomocą portu USB, musisz zainstalować [Sterowniki USB firmy Hims](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) na komputer.

Poniżej skróty klawiszowe dla tych monitorów, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przywołaj do komórki brajla |Routing|
|Przewiń wyświetlacz brajla wstecz |Lewy klawisz przewijania w górę, prawy klawisz przewijania w górę, klawisz przewijania w lewo|
|Przewiń wyświetlacz brajla w przód |Lewy klawisz przewijania w dół, prawy klawisz przewijania w dół, klawisz przewijania w prawo|
|Przenieś wyświetlacz brajla do poprzedniej linii |Lewy klawisz przewijania w górę+prawy klawisz przewijania w górę|
|Przenieś wyświetlacz brajla do następnej linii |Lewy klawisz przewijania w dół+prawy klawisz przewijania w dół|
|Przejdź do poprzedniej linii w przeglądzie |prawy klawisz przewijania w górę|
|Przejdź do następnej linii w przeglądzie |prawy klawisz przewijania w dół|
|Przejdź do poprzedniego znaku w przeglądzie |strzałka w lewo po prawej stronie|
|Przejdź do następnego znaku w przeglądzie |strzałka w prawo po prawej stronie|
|Przejdź do fokusa| lewy klawisz przewijania w górę+lewy klawisz przewijania w dół, prawy klawisz przewijania w górę+prawy klawisz przewijania w dół, lewy klawisz przewijania+prawy klawisz przewijania|
|Klawisz control |smartbeetle:f1, brailleedge:f3|
|Klawisz windows |f7, smartbeetle:f2|
|klawisz alt |punkt 1+punkt 3+punkt 4+spacja, f2, smartbeetle:f3, brailleedge:f4|
|klawisz shift |f5|
|klawisz insert |punkt 2+punkt 4+spacja, f6|
|klawisz aplikacji |punkt 1+punkt 2+punkt 3+punkt 4+spacja, f8|
|klawisz capsLock |punkt 1+punkt 3+punkt 6+spacja|
|klawisz tab |punkt 4+punkt 5+spacja, f3, brailleedge:f2|
|klawisz shift+alt+tab |f2+f3+f1|
|klawisz alt+tab |f2+f3|
|Klawisz Shift+Tab |Punkt 1+Punkt 2+Spacja|
|Klawisz end |punkt 4+punkt 6+spacja|
|Klawisz control+end |punkt 4+punkt 5+punkt 6+spacja|
|Klawisz home |punkt 1+punkt 3+spacja, smartbeetle:f4|
|Klawisz control+home |punkt 1+punkt 2+punkt 3+spacja|
|Klawisz alt+f4 |punkt 1+punkt 3+punkt 5+punkt 6+spacja|
|Klawisz strzałka w lewo |punkt 3+spacja, lewa strzałka w lewo|
|Klawisz control+shift+strzałka w lewo |punkt 2+punkt 8+spacja+f1|
|Klawisz control+strzałka w lewo |punkt 2+spacja|
|Klawisz shift+alt+strzałka w lewo |punkt 2+punkt 7+f1|
|`alt+StrzałkaWLewo` |`punkt2+punkt7+spacja`|
|Klawisz strzałka w prawo |punkt 6+spacja, prawa strzałka w prawo|
|Klawisz control+shift+strzałka w prawo |punkt 5+punkt 8+spacja+f1|
|Klawisz control+strzałka w prawo |punkt 5+spacja|
|Klawisz shift+alt+strzałka w prawo |punkt 5+punkt 7+f1|
|`alt+StrzałkaWPrawo` |`punkt5+punkt7+spacja`|
|Klawisz pageUp |punkt 1+punkt 2+punkt 6+spacja|
|Klawisz control+pageUp |punkt 1+punkt 2+punkt 6+punkt 8+spacja|
|Klawisz strzałka w górę |punkt 1+spacja, lewa strzałka w górę|
|Klawisz control+shift+strzałka w górę |punkt 2+punkt 3+punkt 8+spacja+f1|
|Klawisz control+strzałka w górę |punkt 2+punkt 3+spacja|
|Klawisz shift+alt+strzałka w górę |punkt 2+punkt 3+punkt 7+f1|
|`alt+StrzałkaWGórę` |`punkt2+punkt3+punkt7+spacja`|
|Klawisz shift+strzałka w górę |lewy klawisz przewijania w dół+spacja|
|Klawisz pageDown |punkt 3+punkt 4+punkt 5+spacja|
|Klawisz control+pageDown |punkt 3+punkt 4+punkt 5+punkt 8+spacja|
|Klawisz strzałka w dół |punkt 4+spacja, lewa strzałka w dół|
|Klawisz control+shift+strzałka w dół |punkt 5+punkt 6+punkt 8+spacja+f1|
|Klawisz control+strzałka w dół |punkt 5+punkt 6+spacja|
|Klawisz shift+alt+strzałka w dół |punkt 5+punkt 6+punkt 7+f1|
|`alt+StrzałkaWDół` |`punkt5+punkt6+punkt7+spacja`|
|Klawisz shift+strzałka w dół |spacja+prawy klawisz przewijania w dół|
|Klawisz escape |punkt 1+punkt 5+spacja, f4, brailleedge:f1|
|Klawisz delete |punkt 1+punkt 3+punkt 5+spacja, punkt 1+punkt 4+punkt 5+spacja|
|Klawisz f1 |punkt 1+punkt 2+punkt 5+spacja|
|Klawisz F3 |punkt1+punkt4+punkt8+spacja|
|Klawisz f4 |punkt 7+f3|
|Klawisz windows+b |punkt 1+punkt 2+f1|
|Klawisz windows+d |punkt 1+punkt 4+punkt 5+f1|
|Klawisz control+insert |smartbeetle:f1+prawy klawisz przewijania|
|Klawisz alt+insert |smartbeetle:f3+prawy klawisz przewijania|

<!-- KC:endInclude -->

### Monitory brajlowskie Seika {#Seika}

Następujące monitory brajlowskie firmy  Nippon Telesoft są wspierane w dwóch grupach z różną funkcjonalnością:

* [Seika versja 3, 4, i 5 (40 znakowe), Seika80 (80 znakowy)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 znakowe), V6, i V6Pro (40 znakowe)](#SeikaNotetaker)

Więcej informacji o tych monitorach brajlowskich możesz znaleźć na stronie [Pobierania sterowników i demonstracji](https://en.seika-braille.com/down/index.html).

#### Seika wersja 3, 4, i 5 (40 znakowe), Seika80 (80 znakowe) {#SeikaBrailleDisplays}

* Te monitory brajlowskie jeszcze nie wspierają audomatyczne wykrywanie monitorów brajlowskich NVDA.
* Aby ręcznie skonfigurować te monitory brajlowskie, trzeba wybrać "Seika monitory brajlowskie"
* Sterowniki urządzenia muszą być zainstalowane przed używaniem  Seika v3/4/5/80.
Sterowniki [dostarcza producent](https://en.seika-braille.com/down/index.html).

Następują klawiszy skrótów dla tego monitora brajlowskiego.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do poprzedniej linii |B3|
|Przenieś wyświetlacz brajla do następnej linii |B4|
|Przełącz "Brajl związany z..." |B5|
|Czytaj wszystko |B6|
|Tab |B1|
|Shift+Tab |B2|
|Alt+Tab |B1+B2|
|Menu NVDA |Left+Right|
|Przywołaj do komórki brajla |Routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 znakowe), V6, i V6Pro (40 znakowe) {#SeikaNotetaker}

* Wspierane jest automatyczne wykrywanie monitorów brajlowskich używając USB i Bluetooth.
* Wybierz "Seika Notetaker" lub "automatyczne" aby skonfigurować.
* Nie są wymagane dodatkowe sterowniki podczas używania monitora brajlowskiego Seika Notetaker.

Następują skróty klawiszowe do tego monitora brajlowskiego.
Dla informacji o położeniu tych klawiszy, prosimy zajrzeć do dokumentacji monitora brajlowskiego.
<!-- KC:beginInclude -->

| Nazwa |Skrót|
|---|---|
|Przewiń monitor brajlowski wstecz |left|
|Przewiń monitor brajlowski w przód |right|
|Czytaj wszystko |space+Backspace|
|NVDA Menu |Left+Right|
|Przenieś monitor brajlowski do linii wstecz |LJ up|
|Przenies monitor brajlowski do linii w przód |LJ down|
|Przełącz powiązanie brajla do |LJ center|
|tab |LJ right|
|shift+tab |LJ left|
|Strzałka w górę |RJ up|
|Strzałka w dół |RJ down|
|Strzałka w lewo |RJ left|
|Strzałka w prawo |RJ right|
|Sprowadź do komórki brajlowskiej |routing|
|shift+strzałka w górę key |spacja+RJ up, Backspace+RJ up|
|shift+strzałka w dół key |spacja+RJ down, Backspace+RJ down|
|shift+strzałka w lewo key |spacja+RJ left, Backspace+RJ left|
|shift+strzałka w prawo key |spacja+RJ right, Backspace+RJ right|
|enter key |RJ center, punkt8|
|escape |spacja+RJ center|
|windows |Backspace+RJ center|
|spacja |spacja, Backspace|
|backspace |punkt7|
|pageup |spacja+LJ right|
|pagedown |spacja+LJ left|
|home |spacja+LJ up|
|End |spacja+LJ down|
|control+home |backspace+LJ up|
|control+end |backspace+LJ down|

### Nowsze modele Papenmeier BRAILLEX {#Papenmeier}

Obsługiwane są następujące monitory: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB i bluetooth)
* BRAILLEX Live 20, BRAILLEX Live i BRAILLEX Live Plus (USB i bluetooth)

Te monitory brajlowskie nie są jeszcze obsługiwane przez funkcję NVDA automatycznego wykrywania monitora brajlowskiego.
Istnieje opcja w sterownikach USB tego monitora brajlowskiego, która uniemożliwia inicjalizację monitora brajlowskiego.
Spróbuj zrobić następujące rzeczy:

1. Upewnij się, że masz zainstalowany [ostatni sterownik](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Otwórz menedżer urządzeń systemu Windows.
1. Na liście kategorii znajdź  "Kontrolery USB" lub "Urządzenia USB".
1. Wybierz "Papenmeier Braillex USB Device".
1. Otwórz właściwości, i znajdź kartę "zaawansowane".
W niektórych przypadkach, karta właściwości zaawansowane nie pojawia się.
W takim razie, odłącz monitor brajlowski od komputera, wyłącz NVDA, poczekaj chwilę i i ponownie podłącz monitor brajlowski.
Powtórz te kroki 4 lub 5 razy, jeżeli jest to konieczne.
Jeżeli karta właściwości "zaawansowane" jeszcze nie jest widoczna, uruchom ponownie komputer.
1. Wyłącz opcję "Load VCP".

Większość urządzeń posiada pasek łatwego dostępu(EAB) umożliwiający intuicyjną i szybką obsługę.
EAB może być przesunięty w czterech kierunkach, a każdy kierunek generalnie posiada dwa przełączniki.
Serie c i Live to jedyny wyjątek od tej reguły.

Seria c i niektóre inne monitory posiada dwie linie routingu, z których górna jest używana do ogłaszania formatowania.
Naciśnięcie i przytrzymanie jednego z górnych klawiszy routingowych i naciśnięcie EAB na monitorach serii c emuluje drugi stan przełącznika.
Monitory serii live  posiadają jeden rząd klawiszy routingowych, a EAB - jeden stopień w każdym kierunku.
Drugi stopień może zostać uzyskany poprzez naciśnięcie jednego z klawiszy routingowych i przesunięcie EAB w wybranym kierunku.
Naciśnięcie i przytrzymanie klawisza góra, dół, prawo i lewo (albo EAB) spowoduje powtórzenie powiązanej akcji.

Na ogół, następujące klawisze są dostępne na tych monitorach:

| Nazwa |Klawisz skrótu|
|---|---|
|L1 |Lewy przedni klawisz|
|L2 |Lewy tylny klawisz|
|R1 |Prawy przedni klawisz|
|R2 |Prawy tylny klawisz|
|Up |1 stopień w górę|
|Up2 |2 stopnie w górę|
|Left |1 stopień w lewo|
|Left2 |2 stopnie w lewo|
|Right |1 stopień w prawo|
|Right2 |2 stopnie w prawo|
|Dn |1 stopień w dół|
|Dn2 |2 stopnie w dół|

Poniżej znajdują się komendy Papenmeier dla NVDA:
<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do poprzedniej linii |Up|
|Przenieś wyświetlacz brajla do następnej linii |Dn|
|Przywołaj do komórki brajla |Routing|
|Raportuj aktualny znak w punkcie przeglądu |L1|
|Aktywuj aktualny obiekt nawigatora |L2|
|Przełącz brajl związany z |R2|
|Raportuj tytuł |L1+Up|
|Raportuj pasek stanu |L2+Down|
|Przejdź do obiektu nadrzędnego |Up2|
|Przejdź do pierwszego obiektu podrzędnego |Dn2|
|Przejdź do poprzedniego obiektu |Left2|
|Przejdź do następnego obiektu |Right2|
|Zgłoś formatowanie tekstu pod komórką brajla |Górny rząd klawiszy routingowych|

<!-- KC:endInclude -->

Model Trio posiada 4 dodatkowe klawisze, znajdujące się z przodu klawiatury brajlowskiej.
Są to (w kolejności od lewej do prawej):

* Klawisz lewego kciuka (lt)
* Spacja
* Spacja
* Klawisz prawego kciuka (rt)

Aktualnie klawisz prawego kciuka nie jest używany.
Obydwa wewnętrzne klawisze to Spacja.

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Klawisz Escape |Spacja+Punkt 7|
|Klawisz Strzałka w górę |Spacja+Punkt 2|
|Klawisz Strzałka w lewo |Spacja+Punkt 1|
|Klawisz Strzałka w prawo |Spacja+Punkt 4|
|Strzałka w dół |Spacja+Punkt 5|
|Klawisz Ctrl |Lt+Punkt 2|
|Klawisz Alt |Lt+Punkt 3|
|Klawisz Ctrl+Escape |Spacja+Punkt 1 2 3 4 5 6|
|Klawisz Tab |Spacja+Punkt 3 7|

<!-- KC:endInclude -->

### Starsze modele Papenmeier Braille BRAILLEX {#PapenmeierOld}

Obsługiwane są następujące monitory: 

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Te monitory mogą być podłączone wyłącznie przez port szeregowy.
W związku z tym, te linijki nie są obsługiwane przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.
Po podłączeniu monitora, należy w Ustawieniach Brajla w NVDA wybrać użyty port w oknie [wyboru monitora brajlowskiego](#SelectBrailleDisplay).

Niektóre z tych urządzeń posiadają pasek łatwego dostępu(EAB) umożliwiający intuicyjną i szybką obsługę.
EAB może być przesunięty w czterech kierunkach, a każdy kierunek generalnie posiada dwa przełączniki.
Naciśnięcie i przytrzymanie klawisza góra, dół, prawo i lewo (albo EAB) spowoduje powtórzenie powiązanej akcji.
Starsze urządzenia nie posiadają EAB; zamiast tego używane są przednie klawisze.

Na ogół, następujące klawisze są dostępne na tych monitorach:

| Nazwa |Klawisz skrótu|
|---|---|
|L1 |Lewy przedni klawisz|
|L2 |Lewy tylny klawisz|
|R1 |Prawy przedni klawisz|
|R2 |Prawy tylny klawisz|
|Up |1 stopień w górę|
|Up2 |Dwa stopnie w górę|
|Left |1 stopień w lewo|
|Left2 |2 stopnie w lewo|
|Right |1 stopień w prawo|
|Right2 |2 stopnie w prawo|
|Dn |1 stopień w dół|
|Dn2 |2 stopnie w dół|

Poniżej znajdują się komendy Papenmeier dla NVDA:

<!-- KC:beginInclude -->
Urządzenia z EAB:

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do poprzedniej linii |Up|
|Przenieś wyświetlacz brajla do następnej linii |Dn|
|Przywołaj do komórki brajla |Routing|
|Raportuj aktualny znak w punkcie przeglądu |L1|
|Aktywuj aktualny obiekt nawigatora |L2|
|Raportuj tytuł |L1+Up|
|Raportuj pasek stanu |L2+Down|
|Przejdź do obiektu nadrzędnego |Up2|
|Przejdź do pierwszego obiektu podrzędnego |Dn2|
|Przejdź do następnego obiektu |Right2|
|Przejdź do poprzedniego obiektu |Left2|
|Zgłoś formatowanie tekstu pod komórką brajla |Górny rząd klawiszy routingowych|

BRAILLEX Tiny:

| Działanie |Klawisz skrótu|
|---|---|
|Raportuj aktualny znak w punkcie przeglądu |L1|
|Aktywuj aktualny obiekt nawigatora |L2|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do poprzedniej linii |Up|
|Przenieś wyświetlacz brajla do następnej linii |Dn|
|Przełącz "Brajl związany z..." |R2|
|Przejdź do obiektu nadrzędnego |R1+Up|
|Przejdź do pierwszego obiektu podrzędnego |R1+Dn|
|Przejdź do poprzedniego obiektu |R1+Left|
|Przejdź do następnego obiektu |R1+Right|
|Zgłoś formatowanie tekstu pod komórką brajla |górny rząd routingu|
|Zgłoś tytuł |L1+Up|
|Zgłoś pasek stanu |L2+Down|

BRAILLEX 2D Screen:

| Działanie |Klawisz skrótu|
|---|---|
|Raportuj aktualny znak w punkcie przeglądu |L1|
|Aktywuj aktualny obiekt nawigatora |L2|
|Przełącz "Brajl związany z..." |R2|
|Zgłoś formatowanie tekstu pod komórką brajla |górny rząd routingu|
|Przenieś wyświetlacz brajla do poprzedniej linii |Up|
|Przewiń wyświetlacz brajla wstecz |Left|
|Przewiń wyświetlacz brajla w przód |Right|
|Przenieś wyświetlacz brajla do następnej linii |Dn|
|Przejdź do następnego obiektu |Left2|
|Przejdź do obiektu nadrzędnego |Up2|
|Przejdź do pierwszego obiektu podrzędnego |Dn2|
|Przejdź do poprzedniego obiektu |Right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA obsługuje notatniki BrailleNote produkcji [Humanware](https://www.humanware.com) używane w roli monitora brajlowskiego dla programu czytającego ekran.
Następujące modele są obsługiwane:

* BrailleNote Classic (tylko szeregowe połączenie)
* BrailleNote PK (połączenie szeregowe i bluetooth)
* BrailleNote MPower (połączenie szeregowe i bluetooth)
* BrailleNote Apex (połączenie USB i bluetooth)

Dla informacji o BrailleNote Touch, proszę sprawdzić rozdział [Brailliant serii BI/ BrailleNote Touch](#HumanWareBrailliant).

Z wyjątkiem BrailleNote PK, zarówno klawiatury brajlowskie (BT) i QWERTY (QT) są obsługiwane.
Dla BrailleNote QT, nie jest obsługiwana emulacja klawiatury PC.
Można wprowadzać punkty brajlowskie przy użyciu klawiatury QT.
Więcej szczegółów w rozdziale o terminalach brajlowskich podręcznika BrailleNote.

Jeśli twoje urządzenie obsługuje więcej niż jeden typ połączenia, podłączając notatnik do NVDA, musisz ustawić port terminala brajlowskiego w opcjach terminala brajla.
Więcej na ten temat można znaleźć w podręczniku urządzenia.
W NVDA może okazać się konieczne wybranie portu w oknie [wyboru monitora brajlowskiego](#SelectBrailleDisplay).
Jeśli łączysz się przez USB lub bluetooth, możesz ustawić port na "automatyczny", "USB" lub "Bluetooth", zależnie od dostępnych opcji.
Jeśli łączysz się przy użyciu portu szeregowego, (lub przejściówki USB na port szeregowy) albo jeśli nie pojawia się żadna z poprzednich opcji, musisz ręcznie wybrać używany do komunikacji port na liście portów sprzętowych.

Przed podłączeniem BrailleNote Apex używając jego klienta interfejsu USB, musisz zainstalować sterowniki dostarczane przez HumanWare.

Na BrailleNote Apex BT, dla wywołania różnych komend NVDA, możesz używać kółka przewijania umieszczonego między punktami 1 i 4.
Kółko składa się z czterech kierunkowych kropek, środkowego przycisku kliknięcia, oraz kółka obracającego się zgodnie lub przeciwnie do ruchu wskazówek zegara.

Poniżej skróty klawiszowe dla BrailleNote, które działają w NVDA.
Aby odnaleźć opisywane klawisze, zajrzyj do dokumentacji urządzenia:

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |Back|
|Przewiń wyświetlacz brajla w przód |Advance|
|Przenieś wyświetlacz brajla do poprzedniej linii |Previous|
|Przenieś wyświetlacz brajla do następnej linii |Next|
|Przywołaj do komórki brajla |Routing|
|Menu NVDA |spacja+punkt1+punkt3+punkt4+punkt5 (spacja+n)|
|Przełącz "Brajl związany z..." |Previous+Next|
|Klawisz Strzałka w górę |Spacja+Punkt 1|
|Klawisz Strzałka w dół |Spacja+Punkt 4|
|Klawisz Strzałka w lewo |Spacja+Punkt 3|
|Klawisz Strzałka w prawo |Spacja+Punkt 6|
|Klawisz Page up |Spacja+Punkt 1+Punkt 3|
|Klawisz Page down |Spacja+Punkt 4+Punkt 6|
|Klawisz Home |Spacja+Punkt 1+Punkt 2|
|Klawisz End |Spacja+Punkt 4+Punkt 5|
|Klawisz Ctrl+Home |Spacja+Punkt 1+Punkt 2+Punkt 3|
|Klawisz Ctrl+End |Spacja+Punkt 4+Punkt 5+Punkt 6|
|Klawisz Spacja |Spacja|
|Enter |Spacja+Punkt 8|
|Backspace |Spacja+Punkt 7|
|Klawisz Tab |Spacja+Punkt 2+Punkt 3+Punkt 4+Punkt 5 (Spacja+t)|
|Klawisz Shift+Tab |Spacja+Punkt 1+Punkt 2+Punkt 5+Punkt 6|
|Klawisz Windows |Spacja+Punkt 2+Punkt 4+Punkt 5+Punkt 6 (Spacja+w)|
|Klawisz Alt |Spacja+Punkt 1+Punkt 3+Punkt 4 (Spacja+m)|
|Przełącz tryb pomocy |Spacja+Punkt 2+Punkt 3+Punkt 6 (Spacja+obniżone h)|

Poniżej komendy przypisane do BrailleNote QT, gdy nie jest on w trybie wprowadzania brajla.

| Działanie |Klawisz|
|---|---|
|Menu NVDA |read+n|
|Klawisz strzałka w górę |strzałka w górę|
|Klawisz strzałka w dół |strzałka w dół|
|Klawisz strzałka w lewo |strzałka w lewo|
|Klawisz strzałka w prawo |strzałka w prawo|
|Klawisz Page up |function+strzałka w górę|
|Klawisz Page down |function+strzałka w dół|
|Klawisz Home |function+strzałka w lewo|
|Klawisz End |function+strzałka w prawo|
|Klawisze Control+home |read+t|
|Control+end Klawisze |read+b|
|Klawisz Enter |enter|
|Klawisz Backspace |backspace|
|Klawisz Tab |tab|
|Klawisze Shift+tab |shift+tab|
|Klawisz Windows |read+w|
|Klawisz Alt |read+m|
|Przełącz tryb pomocy wprowadzania |read+1|

Poniżej komendy przypisane do kółka przewijania:

| Działanie |Klawisz|
|---|---|
|Klawisz strzałka w górę |strzałka w górę|
|Klawisz strzałka w dół |strzałka w dół|
|Klawisz strzałka w lewo |strzałka w lewo|
|Klawisz strzałka w prawo |strzałka w prawo|
|Klawisz Enter |środkowy przycisk|
|Klawisz Tab |obrót kółka przewijania  zgodnie z ruchem wskazówek zegara|
|Klawisze Shift+tab |obrót kółka przewijania przeciwnie do ruchu wskazówek zegara|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA obsługuje monitory EcoBraille od [ONCE](https://www.once.es/).
Obsługiwane są następujące modele:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

Możesz ustawić port szeregowy, do którego jest podłączony monitor w oknie [wyboru monitora brajlowskiego](#SelectBrailleDisplay).
Te linijki nie są obsługiwane przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.

Poniżej znajdują się skróty klawiszowe dla monitorów EcoBraille.
Proszę przeczytać [Dokumentację EcoBraille](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) dla uzyskania informacji, gdzie znajdują się te klawisze.

<!-- KC:beginInclude -->

| Działanie |Klawisz skrótu|
|---|---|
|Przewiń wyświetlacz brajla wstecz |T2|
|Przewiń wyświetlacz brajla w przód |T4|
|Przenieś wyświetlacz brajla do poprzedniej linii |T1|
|Przenieś wyświetlacz brajla do następnej linii |T5|
|Przywołaj do komórki brajla |Routing|
|Uaktywnij bieżący obiekt nawigatora |T3|
|Przełącz do następnego trybu przeglądania |F1|
|Przejdź do obiektu nadrzędnego |F2|
|Przełącz do poprzedniego trybu przeglądania |F3|
|Przejdź do poprzedniego obiektu |F4|
|Zgłoś bieżący obiekt |F5|
|Przejdź do następnego obiektu |F6|
|Przejdź do obiektu z fokusem |F7|
|Przejdź do pierwszego obiektu podrzędnego |F8|
|Przenieś kursor lub fokus do aktualnej pozycji kursora przeglądu |F9|
|Zgłoś położenie kursora przeglądu |F0|
|Przełącz "Brajl związany z..." |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

Urządzenie SuperBraille, dostępne głównie na Tajwanie, może zostać połączone przez port szeregowy lub USB.
Ponieważ nie posiada klawiatury brajlowskiej ani przycisków przewijania,  wpisywanie i przewijanie jest wykonywane za pomocą standardowej klawiatury komputerowej.
W związku z powyższym i dla zachowania kompatybilności z innymi czytnikami ekranu na Tajwanie, zdefiniowano dwa klawisze skrótów do przewijania wyświetlacza brajlowskiego:
<!-- KC:beginInclude -->

| Nazwa |Klawisz|
|---|---|
|Przewiń wyświetlacz brajlowski wstecz |numpadMinus|
|Przewiń wyświetlacz brajlowski w przód |numpadPlus|

<!-- KC:endInclude -->

### Monitory brajlowskie Eurobraille {#Eurobraille}

Monitory brajlowskie b.book, b.note, Esys, Esytime i Iris firmy Eurobraille są wspierane przez NVDA.  
Te urządzenia posiadają klawiaturę z dziesięcioma klawiszami. 
Prosimy zajrzeć do dokumentacji po szczegółowy opis tych klawiszy.
Z dwóch klawiszy umieszczonych jak spacja, lewy klawisz odpowiada backspace, a prawy to spacja.

Te urządzenia można połączyć za pomocą usb i posiadają klawiaturę. 
Istnieje możliwość włączenia lub wyłączenia tej klawiatury, przełączając jej stan za pomocą zdarzenia wejścia.
Opisywane tutaj funkcje stosują się do wyłączonej klawiatury.

#### Funkcje klawiatury brajlowskiej {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Nazwa |Klawisz|
|---|---|
|Usuń ostatnią komórkę brajlowską lub znak |`backspace`|
|Przetłumacz ostatnie wejście znaku brajlowskiego i naciśnij enter |`backspace+spacja`|
|Naciśnij klawisz `NVDA` |`punkt3+punkt5+spacja`|
|klawisz `insert` |`punkt1+punkt3+punkt5+spacja`, `punkt3+punkt4+punkt5+spacja`|
|klawisz `delete` |`punkt3+punkt6+spacja`|
|`home` |`punkt1+punkt2+punkt3+spacja`|
|`end` |`punkt4+punkt5+punkt6+spacja`|
|`strzałka w lewo` |`punkt2+spacja`|
|`strzałka w prawo` |`punkt5+spacja`|
|`upArrow` key |`dot1+space`|
|`strzałka w dół` |`kropka6+spacja`|
|`pageUp` |`punkt1+punkt3+spacja`|
|`pageDown` |`punkt4+[punkt6+spacja`|
|`numeryczny1` |`punkt1+punkt6+backspace`|
|`numeryczny2` |`punkt1+punkt2+punkt6+backspace`|
|`numeryczny3` |`punkt1+punkt4+punkt6+backspace`|
|`numeryczny4` |`punkt1+punkt4+punkt5+punkt6+backspace`|
|`numeryczny5` |`punkt1+punkt5+punkt6+backspace`|
|`numeryczny6` |`punkt1+punkt2+punkt4+punkt6+backspace`|
|`numeryczny7` |`punkt1+punkt2+punkt4+punkt5+punkt6+backspace`|
|`numeryczny8` |`punkt1+punkt2+punkt5+punkt6+backspace`|
|`numeryczny9` |`punkt2+punkt4+punkt6+backspace`|
|`numerycznyInsert` |`punkt3+punkt4+punkt5+punkt6+backspace`|
|`numerycznyPrzecinek` key |`punkt2+backspace`|
|`numerycznySlesz` |`punkt3+punkt4+backspace`|
|`NumeryczneMnożenie` |`punkt3+punkt5+backspace`|
|`numerycznyMinus` |`punkt3+punkt6+backspace`|
|`numerycznyPlus` |`punkt2+punkt3+punkt5+backspace`|
|`numerycznyEnter` |`punkt3+punkt4+punkt5+backspace`|
|`escape` |`punkt1+punkt2+punkt4+punkt5+spacja`, `l2`|
|`tab` |`punkt2+punkt5+punkt6+spacja`, `l3`|
|`shift+tab` |`punkt2+punkt3+punkt5+spacja`|
|`printScreen` |`punkt1+punkt3+punkt4+punkt6+spacja`|
|`pause` |`punkt1+punkt4+spacja`|
|`kontekstowy` |`punkt5+punkt6+backspace`|
|`f1` |`punkt1+backspace`|
|`f2` |`punkt1+punkt2+backspace`|
|`f3` |`punkt1+punkt4+backspace`|
|`f4` |`punkt1+punkt4+punkt5+backspace`|
|`f5` |`punkt1+punkt5+backspace`|
|`f6` |`punkt1+punkt2+punkt4+backspace`|
|`f7` |`punkt1+punkt2+punkt4+punkt5+backspace`|
|`f8` |`punkt1+punkt2+punkt5+backspace`|
|`f9` |`punkt2+punkt4+backspace`|
|`f10` |`punkt2+punkt4+punkt5+backspace`|
|`f11` |`punkt1+punkt3+backspace`|
|`f12` |`punkt1+punkt2+punkt3+backspace`|
|`windows` |`punkt1+punkt2+punkt4+punkt5+punkt6+spacja`|
|naciśnij klawisz `windows` |`punkt1+punkt2+punkt3+punkt4+backspace`, `punkt2+punkt4+punkt5+punkt6+spacja`|
|`capsLock` |`punkt7+backspace`, `punkt8+backspace`|
|klawisz `numLock` |`punkt3+backspace`, `punkt6+backspace`|
|`shift` |`punkt7+spacja`|
|naciśnij `shift` |`punkt1+punkt7+spacja`, `punkt4+punkt7+spacja`|
|`control` |`punkt7+punkt8+spacja`|
|Naciśnij `control` |`punkt1+punkt7+punkt8+spacja`, `punkt4+punkt7+punkt8+spacja`|
|`alt` |`punkt8+spacja`|
|naciśnij klawisz `alt` |`punkt1+punkt8+spacja`, `punkt4+punkt8+spacja`|
|Włącz lub wyłącz klawiaturę brajlowską |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### Skróty dla b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Nazwa |Skrót|
|---|---|
|Przewiń monitor brajlowski wstecz |`backward`|
|przewińmonitor brajlowsk w przód |`forward`|
|przenieś do aktualnego fokusu |`backward+forward`|
|Przenieś do komórki brajlowskiej |`routing`|
|`strzałka w lewo` |`joystick2Left`|
|`strzałka w prawo` |`joystick2Right`|
|`strzałka w górę` |`joystick2Up`|
|`strzałka w dół` |`joystick2Down`|
|`enter` |`joystick2Center`|
|`escape` |`c1`|
|`tab` |`c2`|
|naciśnij klawisz `shift` |`c3`|
|naciśnij klawisz `control` |`c4`|
|Naciśnij klawisz `alt` |`c5`|
|Naciśnij klawisz `NVDA` |`c6`|
|`control+Home` |`c1+c2+c3`|
|`control+End` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### Skróty klawiszowe b.note {#Eurobraillebnote}

<!-- KC:beginInclude -->

| nazwa |Klawisz|
|---|---|
|Przeniesz monitor brajlowski w tył |`leftKeypadLeft`|
|Przenieś monitor brajlowski w przód |`leftKeypadRight`|
|Przenieś monitor brajlowski do komórki |`routing`|
|Odczytaj formatowanie tekstu pod kursorem |`podwójny routing`|
|przenieś do następnej linii w przęglądzie |`leftKeypadDown`|
|Przełącz do poprzedniego trybu przeglądu |`leftKeypadLeft+leftKeypadUp`|
|Przenieś do następnego trybu przeglądu |`leftKeypadRight+leftKeypadDown`|
|`strzalka w lewo` |`rightKeypadLeft`|
|`strzałka w prawo` |`rightKeypadRight`|
|`strzałka w górę` |`rightKeypadUp`|
|`strzałka w dół` |`rightKeypadDown`|
|`control+home` |`rightKeypadLeft+rightKeypadUp`|
|`control+end` |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Skróty klawiszowe Esys {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Nazwa |Skrót|
|---|---|
|Przewiń monitor brajlowski wstecz |`switch1Left`|
|Przewiń monitor brajlowski w przód |`switch1Right`|
|Przenieś do bieżącego fokusu |`switch1Center`|
|Przenieś do komórki brajlowskiej |`routing`|
|Odczytaj formatowanie tekstu pod kursorem |`doubleRouting`|
|Przenieś do poprzedniej linii w przeglądzie |`joystick1Up`|
|Przenieś do następnej linii w przeglądzie |`joystick1Down`|
|Przenieś do poprzedniego znaku w przeglądzie |`joystick1Left`|
|Przenieś do następnego znaku w przeglądzie |`joystick1Right`|
|`strzałka w lewo` |`joystick2Left`|
|`Strzałka w prawo` |`joystick2Right`|
|`strzałka w górę` |`joystick2Up`|
|`strzałka w dół` |`joystick2Down`|
|`enter` |`joystick2Center`|

<!-- KC:endInclude -->

#### Skróty klawiszowe Esytime {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Nazwa |Klawisz|
|---|---|
|Przenieś monitor brajlowski wstecz |`l1`|
|Przenieś monitor brajlowski w przód |`l8`|
|Przenieś do bieżącego fokusu |`l1+l8`|
|Przenieś do komórki brajlowskiej |`routing`|
|Odczytaj formatowanie tekstu pod komórką brajlowską |`doubleRouting`|
|Przenieś do poprzedniej linii w przeglądzie |`joystick1Up`|
|Przenieś do następnej linii w przeglądzie |`joystick1Down`|
|Przenieś do poprzedniego znaku w przeglądzie |`joystick1Left`|
|Przenieś do następnego znaku w przeglądzie |`joystick1Right`|
|`strzałka w lewo` |`joystick2Left`|
|`strzałka w prawo` |`joystick2Right`|
|`Strzalka w górę` |`joystick2Up`|
|`strzałka w dół` |`joystick2Down`|
|`enter` |`joystick2Center`|
|`escape` |`l2`|
|`tab` |`l3`|
|Naciśnij `shift` |`l4`|
|Naciśnij `control` |`l5`|
|Naciśnij `alt` |`l6`|
|Naciśnij klawisz `NVDA` |`l7`|
|`control+home` |`l1+l2+l3`, `l2+l3+l4`|
|`control+end` |`l6+l7+l8`, `l5+l6+l7`|
|Włącz lub wyłącz klawiaturę brajlowską |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Monitory brajlowskie Nattiq nBraille {#NattiqTechnologies}

NVDA wspiera monitory brajlowskie firmy [Nattiq Technologies](https://www.nattiq.com/) gdy są podłączone do portuUSB.
W systemie windows 10 i nowszych jego wersji monitor brajlowski jest wykrywany od razu po podłączeniu, do starszych wersji systemu windows trzeba zainstalować sterownik (poniżej windowsa 10).
Można je pobrać ze strony producenta.

Poniżej znajdują się skróty dla monitorów brajlowskich Nattiq Technologies do użycia z NVDA.
Informacje na temat rozmieszczenia tych klawiszy, znajdują się w dokumentacji monitora.
<!-- KC:beginInclude -->

| Nazwa |Klawisz|
|---|---|
|Przenieś wyświetlacz wstecz |up|
|Przenieś wyświetlacz do przodu |down|
|Przenieś monitor brajlowski do poprzedniego wiersza |left|
|Przenieś monitor brajlowski do następnego wiersza |right|
|Przenieś do komórki brajlowskiej |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) jest osobnym programem, który może być wykorzystany do wsparcia wielu monitorów Brajlowskich.
Aby skorzystać z takiej możliwości, należy zainstalować [BRLTTY for Windows](https://www.brltty.app/download.html).
Należy pobrać i zainstalować najnowszy pakiet instalacyjny, który będzie się nazywać na przykład brltty-win-4.2-2.exe.
Podczas konfiguracji monitora i używanych portów, należy zwrócić szczególną uwagę na wskazówki w przypadku korzystania z monitora USB i zainstalowania dostarczonych przez producenta sterowników.

Dla monitorów z klawiaturą brajlowską, BRLTTY aktualnie sam zarządza wprowadzaniem brajla.
W związku z tym, ustawienie w NVDA tabeli wprowadzania nie ma zastosowania.

BRLTTY nie jest obsługiwane przez funkcję NVDA automatycznego wykrywania linijki brajlowskiej.

Poniżej wykaz poleceń brltty dla NVDA. 
Zobacz [tabele klawiszy w dokumentacji brltty](https://brltty.app/doc/KeyBindings/) by dowiedzieć się, jak poszczególne komendy programu wywołać za pomocą klawiszy poszczególnych monitorów.
<!-- KC:beginInclude -->

| Działanie |Komenda brltty|
|---|---|
|Przewiń brajla do tyłu |`fwinlt` (jedno okno w lewo)|
|Przewiń brajla do przodu |`fwinrt` (jedno okno w prawo)|
|Przenieś monitor do poprzedniej linii |`lnup` (jedna linia do góry)|
|Przenieś monitor do następnej linii |`lndn` (jedna linia w dół)|
|Przywołaj do komórki brajla |`route` (przenieś kursor do znaku)|
|Włącz lub wyłącz pomoc klawiatury |`learn` (włącza lub wyłącza tryb samouczka poleceń)|
|Otwórz NVDA menu |`prefmenu` (Otwiera lub zamyka menu ustawień)|
|Przywróć konfiguracje |`prefload` (przywraca ustawienia z dysku)|
|Zapisz ustawienia |`prefsave` (Zapisuje ustawienia na dysk)|
|Odczytaj czas |`time` (pokazuje aktualny czas)|
|Odczytuje bieżącą linię pod kursorem przeglądu |`say_line` (Wymawia bieżącą linię)|
|Czytaj wszystko za pomocą kursora przeglądu |`say_below` (Czyta wszystko od bieżącej linii do końca ekranu)|

<!-- KC:endInclude -->

### Monitory brajlowskie Tivomatic Caiku Albatross 46/80 {#Albatross}

Monitory brajlowskie Caiku Albatross, które były produkowane  i dostępne w Finlandii, mogą być połączone za pomocą portu USB lub portu szeregowego.
Nie są potrzebne sterowniki specjalne żeby używać tych monitoró brajlowskich.
Wystarczy tylko połączyć monitor brajlowski i ustawić NVDA do jego używania.

Uwaga: szybkość transmisji w bodach  19200 jest najbardziej zalecana.
Jeżeli jest to wymagane, przełącz wartość ustawienia szybkość transmisji w bodach na wartość 19200 z poziomu menu monitora brajlowskiego.
Choć sterownik wspiera szybkość transmisji w bodach 9600, nie istnieje możliwość sterowania używaną szybkością transmisji.
Z powodu tego, że domyślną szybkością transmisji w bodach jest 19200, ta szybkość jest najpierw używana przez sterownik.
Jeżeli szybkości transmisji nie są takie same, sterownik może się zachowywać w nieoczekiwany dla nas sposób.

Poniżej podane są przydzielone klawisze dla tego monitora brajlowskiego.
Prisimy zajrzeć do dokumentacji monitora brajlowskiego w celu sprawdzienia opisu i lokalizacji klawiszy.
<!-- KC:beginInclude -->

| Nazwa |Klawisz|
|---|---|
|Przejdź do początkowej linii w przeglądzie |`home1`, `home2`|
|Przejdź do końcowej linii w przeglądzie |`end1`, `end2`|
|Ustawia bieżący obiekt nawigatora do fokusu |`eCursor1`, `eCursor2`|
|Przenosi do bieżącego fokusu |`cursor1`, `cursor2`|
|Przemieszcza wskażnik myszy do bieżącego obiektu nawigatora |`home1+home2`|
|Ustawia bieżacy obiekt nawigatora do bieżącego obiektu pod myszą i wymawia go |`end1+end2`|
|Ustawia fokus do bieżącego obiektu nawigatora |`eCursor1+eCursor2`|
|Przełącza przywiązanie brajla |`cursor1+cursor2`|
|Przemieszcza monitor brajlowski do poprzedniej linii |`up1`, `up2`, `up3`|
|Przemieszcza monitor brajlowski do następnej linii |`down1`, `down2`, `down3`|
|Przemieszcza monitor brajlowski do poprzedniego fragmentu tekstu |`left`, `lWheelLeft`, `rWheelLeft`|
|Przemieszcza monitor brajlowski do następnego fragmentu tekstu |`right`, `lWheelRight`, `rWheelRight`|
|przywołuje monitor brajlowski do komórki brajlowskiej |`routing`|
|Odczytuje formatowanie tekstu pod kursorem brajlowskim |`secondary routing`|
|przełącza między sposobami pokazywania informacji kontekstowej |`attribute1+attribute3`|
|Przełącza między trybami mowy |`attribute2+attribute4`|
|Przełącza do poprzedniego trybu przeglądania (np. obiekt, dokument lub ekran) |`f1`|
|Przełącza do następnego trybu przeglądania (np. obiekt, dokument lub ekran) |`f2`|
|Przenosi obiekt nawigatora na obiekt, któy go zawiera |`f3`|
|przenosi obiekt nawigatora do pierwszego obiektu wewnętrznego |`f4`|
|Przenosi obiekt nawigatora do poprzedniego obiektu |`f5`|
|Przenosi obiekt nawigatora do następnego obiektu |`f6`|
|Odczytuje bieżący obiekt nawigatora |`f7`|
|Odczytuje informację o położeniu tekstu lub obiektu nawigatora pod kursorem przeglądu |`f8`|
|Pokazuje ustawienia brajla |`f1+home1`, `f9+home2`|
|Odczytuje pasek stanu i przenosi obiekt nawigatora |`f1+end1`, `f9+end2`|
|Przełącza między dostępnymi kształtami kursora brajlowskiego |`f1+eCursor1`, `f9+eCursor2`|
|Włącza lub wyłącza kursor brajlowski |`f1+cursor1`, `f9+cursor2`|
|Przemieszcza między trybami pokazywania komunikatów |`f1+f2`, `f9+f10`|
|Przełącza między trybami pokazywania zaznaczenia |`f1+f5`, `f9+f14`|
|Przełącza między elementami opcji "Przenoś kursor systemowy podczas przywoływania kursoru przeglądu" |`f1+f3`, `f9+f11`|
|Wywołuje domyślną akcję na bieżącym obiekcie nawigatora |`f7+f8`|
|odczytuje date/czas |`f9`|
|Odczytuje stan baterii jeżeli ładowarka nie jest włączona |`f10`|
|Odczytuję tytuł okna |`f11`|
|Odczytuje pasek stanu |`f12`|
|Odczytuje bieżącą linię pod kursorem |`f13`|
|Czytaj wszystko |`f14`|
|Odczytuje bieżący znak pod kursorem przeglądu |`f15`|
|Odczytuje bieżącą linie na miejscu na którym znajduje się kursor przeglądu |`f16`|
|Odczytuje słowo na miejscu na którym znajduje się kursor przeglądu |`f15+f16`|
|przenosi kursor przeglądu do poprzedniej linii bieżącego obiektu nawigatora i wymawia ją |`lWheelUp`, `rWheelUp`|
|przenosi kursor przeglądu do następnej linii bieżącego obiektu nawigatora i wymawia ją |`lWheelDown`, `rWheelDown`|
|`Klawisz Windows+d` (minimalizuje wszystkie aplikacje) |`attribute1`|
|klawisz `Windows+e` (ten komputer) |`attribute2`|
|klawisz `Windows+b` (przenosi fokus do obszaru powiadomień) |`attribute3`|
|klawisz `Windows+i` (ustawienia systemu windows) |`attribute4`|

<!-- KC:endInclude -->

### Standardowe monitory brajlowskie HID {#HIDBraille}

Jest to eksperymentalny sterownik dla monitorów brajlowskich zrobionych według specyfikacji HID, którą przyjeli w roku 2018 Microsoft, Google, Apple i niektóre inne firmy produkujące technologie wspomagające włączając w to NV Access. 
Mamy nadzieję, że przyszłe monitory brajlowskie stworzone przez jakiegokolwiek producenta będą wspierać ten protokół, co wyeliminuje potrzebę dla specyficznych sterowników.

Wykrywanie automatyczne brajlowskich monitorów NVDA będzie automatycznie wykrywało monitory brajlowskie według tego standartu.

Oto skróty klawiszowe przydzielone dla tego monitora brajlowskiego.
<!-- KC:beginInclude -->

| nazwanie |klawisz|
|---|---|
|przejście brajlowskiego monitoru wstecz |pan left lub rocker up|
|przejście brajlowskiego monitoru w przód |pan right lub rocker down|
|przemieszczenie do brajlowskiej komórki |routing set 1|
|przełączanie przywiązania brajla do |up+down|
|strzałka w górę |joystick w górę, dpad w górę lub spacja+punkt1|
|strzałka w dół |joystick w dół, dpad w dół lub spacja+punkt4|
|Strzałka w lewo |spacja+punkt3, joystick w lewo  lub dpad w lewo|
|strzałka w prawo |spacja+punkt6, joystick w prawo lub dpad w prawo|
|shift+tab |spacja+kropka1+kropka3|
|tab |spacja+kropka4+kropka6|
|alt |spacja+kropka1+kropka3+kropka4 (spacja+m)|
|escape |spacja+kropka1+kropka5 (spacja+e)|
|enter |punkt8, joystick przyciśnięty środkowo lub dpad środkowy|
|window |spacja+kropka3+kropka4|
|alt+tab |spacja+kropka2+kropka3+kropka4+kropka5 (spacja+t)|
|NVDA Menu |spacja+kropka1+kropka3+kropka4+kropka5 (spacja+n)|
|windows+d (minimalizuje wszystkie aplikacje) |spacja+kropka1+kropka4+kropka5 (spacja+d)|
|czytaj wszystko |spacja+kropka1+kropka2+kropka3+kropka4+kropka5+kropka6|

<!-- KC:endInclude -->

## Dla zaawansowanych {#AdvancedTopics}
### Tryb bezpieczny {#SecureMode}

Administratorzy systemowi zechcą skonfigurować NVDA tak, aby ograniczyć niepowołany dostęp do systemu.
NVDA umożliwia instalację dodatków, które mogą wykonywać różny kod, włączając w to podwyższenie uprawnień NVDA do praw administratora.
NVDA także umożliwia użytkownikom wykonywanie różnego kodu z konsoli Pythona.
Tryb bezpieczny NVDA zapobiega zmianę konfiguracji przez użytkowników i ogranicza niepowołany dostęp do systemu.

NVDA Uruchamia się w trybie bezpiecznym gdy jest uruchomiony na [bezpiecznych ekranach](#SecureScreens), do póki [Parametr ogólnosystemowy](#SystemWideParameters) `serviceDebug`jest włączony.
Aby zmusić uruchamianie NVDA w trybie bezpiecznym, ustaw [parametr ogólnosystemowy](#SystemWideParameters) `forceSecureMode`.
NVDA może także być uruchomiony w trybie bezpiecznym za pomocą [opcji wiersza poleceń](#CommandLineOptions) `-s`.

Tryb bezpieczny wyłącza:

* Zachowywanie konfiguracji i innych ustawień na dysk
* zachowywanie zdarzeń wejścia na dysk
* [Profile konfiguracji](#ConfigurationProfiles) funkcje takie jak tworzenie, usuwanie, zmienianie nazwy profili itd.
* Wczytywanie konfiguracji użytkownika za pomocą polecenia [ `-c`](#CommandLineOptions)
* Aktualizowanie NVDA i tworzenie kopii przenośnych
* [Add-on Store](#AddonsManager)
* [konsolę pythonaNVDA](#PythonConsole)
* [Podgląd logu](#LogViewer) i logowanie
* [Przegląd brajla](#BrailleViewer) i [Przegląd mowy](#SpeechViewer)
* Otwieranie dokumentów zewnętrznych z menu NVDA, takich jak podręcznik użytkownika lub plik z listą współtwórców.

Kopie zainstalowane NVDA zachowują swoją konfigurację i dodatki we folderze `%APPDATA%\nvda`.
Aby zapobiec zmianom konfiguracji i dodatków bezpośrednio przez użytkownika, dostęp użytkownikowi musi być zabroniony.

Tryb bezpieczny jest nieefektywny dla przenośnych kopii NVDA.
To ograniczenie zastosowywane jest także do kopii tymczasowej i instalatora NVDA.
W środowiskach bezpiecznych, użtkownik, który jest w stanie uruchomić program przenośny jest takim samym ryzykiem bezpieczeństwa niezależnie od trybu bezpieczeństwa.
Oczekuje się od administratorów systemu ograniczać uruchamianie nieautoryzowanych programów na ich systemach, włączając w to przenośne kopie NVDA.

Użytkownicy NVDA często polegają na zmianie profili konfiguracyjnych w celu ustawienia NVDA według swoich preferencji.
W to jest włączone także instalowanie dodatków,, sprawdzonych niezależnie od NVDA.
Tryb bezpieczny zamarza konfigurację NVDA. Przed włączaniem trybu bezpiecznego, upewnij się że NVDA jest prawidłowo skonfigurowana.

### Bezpieczne ekrany {#SecureScreens}

NVDA jest uruchomiony w [trybie bezpiecznym](#SecureMode) gdy jest uruchomiony na bezpiecznym ekranie, chyba że parametr `serviceDebug` [ogólnosystemowy](#SystemWideParameters) jest włączony.

Gdy jest uruchomiony z ekranów bezpiecznych, NVDA używa profilu systemowego dla ustawień.
Ustawienia użytkownika NVDA mogą być skopiowane [do użytku na bezpiecznych ekranach](#GeneralSettingsCopySettings).

Ekrany bezpieczne to:

* Ekran logowania do systemu Windows
* Okno dialogowe kontroli konta użytkownika, aktywne podczas dokonywania akcji jako administrator
  * Włączając w to instalowanie programów

### Parametry linii komend {#CommandLineOptions}

NVDA  akceptuje jeden lub więcej przełączników startowych, zmieniających jego zachowanie.
Możesz podać tyle opcji, ile jest potrzebne.
Te opcje mogą być wpisane podczas uruchamiania ze skrótu  (we właściwościach skrótu), w oknie dialogowym "Uruchom"  (Menu start-> Uruchom lub Windows+R) lub w konsoli wiersza poleceń Windows.
Opcje powinny być oddzielone spacjami od nazwy pliku wykonywalnego NVDA, oraz od innych opcji.
Dla przykładu, przełącznik `--disable-addons` pozwala uruchomić NVDA z wyłączonymi dodatkami.
Pozwala to ustalić, czy jakiś problem jest powodowany przez dodatek i szybko go naprawić.

Inny przykład, to zamknięcie aktualnie uruchomionej kopii NVDA poprzez wpisanie:

    nvda -q

Niektóre opcje występują w dwóch wersjach - krótkiej i długiej, inne tylko w długiej wersji.
opcje posiadające krótką wersję, możesz łączyć np.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Ta komenda uruchomi NVDA bez dźwięków oraz wiadomości startowej, oraz z użyciem niestandardowego katalogu konfiguracji.|
|`nvda -mc CONFIGPATH --disable-addons` |Jak powyżej, z wyłączonymi dodatkami.|

Niektóre przełączniki akceptują dodatkowe ustawienia; np. jak szczegółowy powinien być tworzony log albo ścieżkę do katalogu konfiguracyjnego użytkownika.
Te ustawienia powinny być umieszczane po odpowiedniej opcji oddzielone spacją od krótkiej wersji przełącznika lub znakiem równości `(=)` od długiej wersji, np.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Wywołuje NVDA z poziomem logowania ustawionym na Debugowanie|
|`nvda --log-file=c:\nvda.log` |Nakazuje NVDA zapisywać log do pliku `c:\nvda.log`|
|`nvda --log-level=20 -f c:\nvda.log` |Uruchamia NVDA z poziomem logowania ustawionym na info i plikiem logu zapisywanym w `c:\nvda.log`|

Poniżej wymieniono wszystkie opcje linii poleceń dla NVDA:

| Krótka |Długa |Opis|
|---|---|---|
|`-h` |`--help` |Pokaż pomoc wiersza poleceń i wyjdź|
|`-q` |`--quit` |Zakończ aktualnie uruchomioną kopię NVDA|
|`-k` |`--check-running` |Poinformuj kodem wyjścia, czy NVDA jest uruchomiony; 0 jeśli uruchomiony, 1 jeśli nie uruchomiony|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |Plik, do którego powinny być zapisywane informacje logu. Logowanie jest zawsze wyłączone gdy tryb bezpieczny jest włączony.|
|`-l PoziomLogowania` |`--log-level=LOGLEVEL` |Najniższy poziom zapisywanych zdarzeń do podglądu logu (debugowanie 10, wejście/wyjście 12, debugowanie powiadomienie 15, info 20, wyłączone 100). Logowanie jest zawsze wyłączone gdy tryb bezpieczny jest włączony.|
|`-c ścieżka` |`--config-path=ścieżka` |Ścieżka folderu, w którym zapisane są wszystkie ustawienia NVDA. Domyślna wartość to wyłączone gdy tryb bezpieczny jest włączony.|
|Brak |`--lang=LANGUAGE` |Nadpisuje domyślny język NVDA. Ustawiony na "Windows" dla bieżacego użytkownika, "en" dla angielskiego, itd.|
|`-m` |`--minimal` |Bez dźwięku, interfejsu, informacji początkowej etc|
|`-s` |`--secure` |Uruchamia NVDA w [Trybie bezpiecznym](#SecureMode)|
|Brak |`--disable-addons` |Dodatki będą ignorowane|
|Brak |`--debug-logging` |Ustaw poziom logowania na informacje debugowania, dla bieżącego uruchomienia. To ustawienie nadpisze jakiekolwiek ustawienie poziomu logowania ( `--loglevel`, `-l`) z wyłączeniem zapisywania logów włącznie.|
|Brak |`--no-logging` |Wyłącz zapisywanie dziennika podczas używania NVDA. To ustawienie może być nadpisane, gdy poziom logowania ( `--loglevel`, `-l`) jest określony w linii komend lub rejestrowanie debugowania jest włączone.|
|Brak |`--no-sr-flag` |Nie zmieniaj globalnej flagi systemowej czytnika ekranu|
|Brak |`--install` |Po cichu instaluje NVDA i uruchamia zainstalowaną kopię|
|Brak |`--install-silent` |Po cichu instaluje NVDA (nie uruchamia zainstalowanej kopii)|
|Brak |`--enable-start-on-logon=True|False` |Przy instalacji włącz funkcję NVDA [Uruchamiaj na ekranie logowania](#StartAtWindowsLogon)|
|Brak |`copy-portable-config` |Podczas instalacji kopiuję konfigurację wersji przenośnej z określonej ścieżki (`config-path`, `-c`) do aktualnego konta użytkownika|
|Brak |`--create-portable` |Tworzy przenośną kopię NVDA (uruchamiając nowo utworzoną kopię). Wymaga określenia parametru `--portable-path`|
|Brak |`--create-portable-silent` |Tworzy przenośną kopię NVDA (nie uruchamiając nowo utworzonej kopii). Wymaga określenia parametru `--portable-path`|
|Brak |`--portable-path=SCIEZKA` |Ścieżka, w której zostanie utworzona przenośna kopia|

### Parametry systemu {#SystemWideParameters}

NVDA pozwala ustawić pewne wartości w rejestrze Windows, zmieniające zachowanie NVDA dla całego systemu.
Wartości te są ustawiane w poniższych kluczach:

* systemy 32-bitowe: `"HKEY_LOCAL_MACHINE\SOFTWARE\nvda"`
* systemy 64-bitowe: `"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda"`

Następujące wartości mogą zostać ustawione w tym kluczu rejestru:

| Nazwa |Typ |Dozwolone wartości |Opis|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (domyślnie) aby wyłączyć, 1 aby włączyć |Gdy włączone, przechowuje konfigurację użytkownika NVDA w lokalnym folderze danych aplikacji, zamiast w podfolderze Roaming danych aplikacji|
|`serviceDebug` |DWORD |0 (domyślne) żeby wyłączyć, 1 żeby włączyć |jeżeli ten parametr jest włączony, będzie wyłączony [tryb bezpieczny](#SecureMode) na [ekranach bezpiecznych](#SecureScreens). Z powodu kilka implikacji bezpieczeństwa, używanie tej opcji jest mocno niezalecane, wręcz odradza się|
|`forceSecureMode` |DWORD |0 (domyślnie) żeby wyłączyć, 1 żeby włączyć |jeżeli włączone, wymusza [tryb bezpieczny](#SecureMode) podczas uruchamiania NVDA.|

## Dodatkowe informacje {#FurtherInformation}

Jeżeli potrzebujesz więcej informacji odnośnie programu  NVDA lub dodatkowej pomocy, odwiedź stronę [Projektu NVDA](NVDA_URL).
Tutaj można znaleźć dodatkowe dokumenty, jak również wsparcie techniczne i zasoby społecznościowe.
Ta strona zawiera również informacje i materiały dotyczące rozwoju NVDA. Zachęcamy również do odwiedzenia polskiej strony społeczności użytkowników NVDA pod adresem: [www.nvda.pl](http://www.nvda.pl)
