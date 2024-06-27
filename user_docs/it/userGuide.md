# NVDA NVDA_VERSION Manuale utente

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Guida rapida ai comandi  -->



## Introduzione {#Introduction}

Benvenuti in NVDA!

NVDA (NonVisual desktop access) è uno screen reader completamente libero e gratuito per i sistemi operativi Windows.
Il prodotto permette ad un non vedente di interagire con il computer, ricevendo le informazioni attraverso una sintesi vocale o un display braille e permettendo quindi l'accesso al sistema operativo ed a numerose applicazioni di terze parti senza costi aggiuntivi, allo stesso modo delle persone vedenti. 
Lo screen reader è sviluppato da [NV Access](https://www.nvaccess.org/), con contributi dalle varie comunità.

### Caratteristiche principali {#GeneralFeatures}

NVDA permette alle persone non vedenti di accedere ed interagire con il sistema operativo Windows e con diverse applicazioni di terze parti.

Un breve video di presentazione in inglese, ["What is NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) is available from the NV Access YouTube channel.

Le caratteristiche principali possono essere riassunte nei seguenti punti:

* Supporto alle applicazioni più comuni come browser web, posta elettronica, wordProcessor e software per chattare.
* sintesi vocale incorporata capace di parlare più di 80 lingue
* annuncio della formattazione del testo , ove disponibile, come nome e dimensione del carattere, errori di stile e di ortografia
* Annuncio automatico del testo sul quale è posizionato il mouse, con possibilità opzionale di conoscere la posizione del mouse stesso sullo schermo
* Supporto per molti Display Braille, compresa la possibilità di immettere testo usando la tastiera della barra braille se presente, e il riconoscimento automatico di un gran numero di modelli di barre.
* Capacità di funzionare interamente da una chiavetta USB o altri dispositivi portatili senza bisogno di installazione
* Installazione guidata semplice ed intuitiva tramite sintesi vocale
* Tradotto in 54 lingue
* Supporto ai sistemi operativi più moderni, comprese le edizioni a 32 e 64 bit
* Gestione delle schermate di accesso utente e quelle [relative alla sicurezza](#SecureScreens)
* Supporto al prompt dei comandi di Windows e alle applicazioni lanciate da console
* Lettura di testo e controlli mentre si utilizza un touch screen.
* Supporto alle interfacce più comuni per l'accessibilità, come Microsoft Active Accessibility, Java Access Bridge, IAccessible2 e UI Automation.
* Capacità di evidenziare il focus di sistema.

### Requisiti di sistema {#SystemRequirements}

* Sistemi operativi: tutte le versioni a 32 e 64 bit dei Sistemi Windows8.1, Windows10, Windows11 e tutte le edizioni Server a partire da Windows Server 2012 r2.
  * sono supportate entrambe le varianti AMD64 e ARM64 di Windows.
* Circa 150 Megabytes di spazio disco.

### Internazionalizzazione {#Internationalization}

è importante che tutte le persone del mondo, indipendentemente dalla loro nazionalità e dalla lingua parlata, abbiano eguale accesso alle informazioni.
Oltre all'inglese, NVDA è stato tradotto in 54 lingue ossia Afrikaans, Albanese, Amharico, Arabo, Aragonese, Bulgaro, Burmese, Catalano, Cinese (semplificato e tradizionale), croato, Ceco, Coreano, Danese, Olandese, persiano, finlandese, Francese, Galiziano, Georgiano, tedesco (svizzero e tedesco, Greco, Ebraico, Hindi, Ungherese, Islandese, Irlandese, italiano, giapponese, Kannada, Coreano, Kyrgy, Lituano, Macedone, Mongolo, Nepalese, Norvegese, Polacco, portoghese (brasiliano e portoghese), Punjabi, Rumeno, russo, Serbo, slovacco, sloveno, Spagnolo (colombiano e spagnolo), Svedese, Tamil, Thai, Turco, ucraino e vietnamita.

### Sintesi vocali supportate {#SpeechSynthesizerSupport}

Oltre a presentare i messaggi e l'interfaccia in svariate lingue, NVDA fornisce all'utente la possibilità di accedere ai contenuti di qualsiasi linguaggio, a patto che l'utente sia in possesso della sintesi vocale che parla quella determinata lingua.

NVDA viene distribuito con [eSpeak NG](https://github.com/espeak-ng/espeak-ng), una sintesi vocale gratuita, opensource e multilingue.

Per informazioni sul funzionamento di altre Sintesi Vocali con NVDA si veda la sezione [Sintesi Vocali Supportate](#SupportedSpeechSynths).

### Supporto Braille {#BrailleSupport}

NVDA è in grado di gestire moltissimi Display Braille, permettendo agli utenti che ne possiedono uno di usufruire anche di questa tecnologia.
NVDA utilizza il traduttore braille open source [LibLouis](https://liblouis.io/) per generare sequenze braille dal testo.
è anche possibile immettere il testo direttamente dalla riga braille purché munita di tastiera, sfruttando la modalità classica o quella a braille contratto, diffuso soprattutto in Stati Uniti e Inghilterra.
Inoltre, da impostazioni predefinite NVDA è in grado di riconoscere la presenza di un gran numero di display braille.
Per il funzionamento di barre Braille con NVDA fare riferimento alla sezione [Display Braille supportati](#SupportedBrailleDisplays).

NVDA inoltre supporta moltissimi tipi di tabelle braille, permettendo quindi un utilizzo del Braille nella lingua scelta dall'utente. Molte lingue sono fornite di tabelle grado 1 e grado 2, Braille contratto o Computer Braille.

### Licenza e Copyright {#LicenseAndCopyright}

NVDA è copyright NVDA_COPYRIGHT_YEARS NVDA contributors.

NVDA è coperto dalla GNU General Public License versione 2, con due eccezioni speciali.
Le eccezioni sono descritte nel documento di licenza nelle sezioni "Non-GPL Components in Plugins and Drivers" e "Microsoft Distributable Code".
NVDA include e utilizza anche componenti resi disponibili con diverse licenze gratuite e open source.
Siete liberi di condividere e modificare questo programma come volete, a patto che voi distribuiate la licenza assieme al software e rendiate disponibile il sorgente a chiunque ne faccia richiesta. 
Questo si applica a copie originali e modificate del software ed a qualsiasi programma che utilizzi codice proveniente da questo software.

Per maggiori informazioni è possibile [Leggere l'intera licenza.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Per i dettagli relativi alle eccezioni, accedere al documento di licenza dal menu NVDA nella sezione "Guida".

## Guida rapida di NVDA {#NVDAQuickStartGuide}

Questa guida rapida contiene tre sezioni principali: download, configurazione iniziale ed esecuzione di NVDA.
Seguiranno poi informazioni sulla regolazione delle preferenze, su come partecipare alla community e ottenere aiuto.
Le informazioni in questa guida rapida fanno riferimento a ciò che viene indicato nel presente manuale in forma estesa.
Fare riferimento alla Guida utente completa per informazioni più dettagliate su ciascun argomento.

### Scaricare NVDA {#GettingAndSettingUpNVDA}

NVDA è completamente gratuito all'uso da parte di chiunque.
Non ci sono chiavi di licenza di cui preoccuparsi o abbonamenti costosi da pagare.
NVDA viene aggiornato, in media, quattro volte all'anno.
L'ultima versione di NVDA è sempre disponibile alla "pagina di Download" del [sito web NVAccess](NVDA_URL).

NVDA funziona con tutte le versioni recenti di Microsoft Windows.
Controllare la sezione sui [Requisiti di sistema](#SystemRequirements) per tutti i dettagli.

#### Procedimento passo passo per scaricare NVDA {#StepsForDownloadingNVDA}

Questi passaggi presuppongono una certa familiarità con la navigazione in una pagina web.

* Aprire il browser web (Premere il tasto `Windows`, digitare la parola "browser" senza le virgolette, e premere `invio`)
* Caricare l'apposita pagina web di download di NV Access (Premere `alt+d`, digitare l'indirizzo seguente e premere `invio`): 
https://www.nvaccess.org/download 
* Attivare il pulsante "download"
* Il browser potrebbe richiedere o meno un'azione inerente il download, accettare la richiesta ed avviare lo scaricamento
* A seconda del browser, il file potrebbe essere eseguito automaticamente dopo il download
* Se il file deve essere avviato manualmente, premere `alt+n` per passare all'area di notifica, quindi `alt+e` per eseguire il file (o i passaggi per il proprio browser)

### Configurazione di NVDA {#SettingUpNVDA}

L'esecuzione del file appena scaricato avvierà una copia temporanea di NVDA.
Verrà quindi chiesto se si desidera installare NVDA, creare una copia portable o semplicemente continuare a utilizzare la copia temporanea.

NVDA non ha bisogno dell'accesso a Internet per l'esecuzione o l'installazione una volta che si è scaricato il programma.
Se disponibile, la connessione ad Internet consente a NVDA di verificare periodicamente la presenza di aggiornamenti.

#### Procedimento passo passo per eseguire il programma d'avvio appena scaricato {#StepsForRunningTheDownloadLauncher}

Il file di installazione è chiamato "nvda_2022.1.exe" o simile.
L'anno e la versione sono diversi ad ogni aggiornamento in modo da adeguarsi man mano alle nuove release.

1. Eseguire il file scaricato.
Viene riprodotta una breve introduzione sonora durante il caricamento di una copia temporanea di NVDA.
Una volta caricato, NVDA parlerà per l'intera durata della procedura.
1. Viene visualizzata la finestra di NVDA con il contratto di licenza.
Premere `freccia giù` per leggere il contratto di licenza, se lo si desidera.
1. Premere `tab` per passare alla casella di controllo "Accetto", quindi premere la `barra spaziatrice` per selezionarla.
1. Premere `tab` per spostarsi tra le opzioni, quindi premere `invio` sull'opzione desiderata.

Le opzioni sono:

* "Installa NVDA su questo computer": questa è l'opzione principale che la maggior parte degli utenti seleziona per un utilizzo facile ed immediato di NVDA.
* "Crea copia portable": consente di configurare ed estrarre NVDA in una cartella qualsiasi senza installarlo.
Questo è utile su computer senza diritti di amministratore o su un supporto di memoria da portare con sè.
Una volta selezionato, NVDA segue i passaggi per creare una copia portable.
La cosa principale che NVDA deve conoscere è la cartella in cui impostare la copia portable.
* "Continua l'esecuzione": Ciò mantiene in esecuzione la copia temporanea di NVDA.
Risulta utile per testare le funzionalità in una nuova versione prima di installarla.
Quando viene selezionata, la finestra di avvio si chiude e la copia temporanea di NVDA continua a funzionare finché non viene chiusa o il PC viene spento.
Si noti che le modifiche alle impostazioni non vengono salvate.
* "Annulla": questo chiude NVDA senza eseguire alcuna azione.

Se si prevede di utilizzare sempre NVDA sul computer, è decisamente consigliabile installare NVDA.
L'installazione di NVDA consentirà funzionalità aggiuntive come l'avvio automatico dopo l'accesso, la possibilità di leggere le schermate di login e di accesso a Windows e [schermate protette](#SecureScreens).
Tali caratteristiche non sono disponibili con copie portatili e temporanee.
Per conoscere tutte le limitazioni durante l'esecuzione di una copia portable o temporanea di NVDA, vedere [Restrizioni delle copie portable e temporanee](#PortableAndTemporaryCopyRestrictions).

L'installazione offre anche la creazione di una voce nel menu avvio e dei collegamenti sul desktop, oltre a consentire l'avvio di NVDA con `control+alt+n`.

#### Procedura passo passo per installare NVDA dal programma appena scaricato {#StepsForInstallingNVDAFromTheLauncher}

Questi passaggi illustrano le opzioni di configurazione più comuni.
Per maggiori dettagli sulle opzioni disponibili, vedere [Opzioni di installazione](#InstallingNVDA).

1. Dal programma di installazione, assicurarsi che la casella di controllo per accettare la licenza sia selezionata.
1. Spostarsi con il tasto `Tab` e attivare il pulsante "Installa NVDA su questo computer".
1. Successivamente, ci sono le opzioni per utilizzare NVDA durante l'accesso a Windows e per creare un collegamento sul desktop.
Esse sono già selezionate per impostazione predefinita.
Se lo si desidera, premere `tab` e `barra spaziatrice` per modificare una qualsiasi di queste opzioni, o lasciarle al valore predefinito.
1. Premere `invio` per continuare.
1. Viene visualizzata una finestra di dialogo "Controllo account utente (UAC)" di Windows con una richiesta simile a questa: "Vuoi consentire a questa app di apportare modifiche al tuo PC?".
1. Premere `alt+s` per accettare.
1. Durante l'installazione di NVDA, apparirà una barra di avanzamento che si riempie sino al termine.
Durante questo processo NVDA emette un segnale acustico sempre più acuto.
Questo processo è spesso veloce e potrebbe non essere notato.
1. Viene visualizzata una finestra di dialogo per confermare che l'installazione di NVDA è andata a buon fine.
Il messaggio consiglia di "Premere OK per avviare la copia installata".
Premere `invio` per avviare la copia installata.
1. Viene visualizzata la finestra di dialogo "Benvenuto in NVDA" e lo screen reader ne leggerà il contenuto.
Il focus si trova sulla casella combinata "Layout tastiera".
Per impostazione predefinita, il layout della tastiera "Desktop" utilizza il tastierino numerico per alcune funzioni.
Se lo si desidera, premere `freccia giù` per scegliere il layout della tastiera "Laptop" in modo da assegnare automaticamente le funzioni del tastierino numerico ad altri tasti.
1. Premere `tab` per spostarsi su  "Utilizza `Blocca maiuscole` come tasto NVDA".
Per impostazioni predefinita, il tasto NVDA è assegnato a `Insert`.
Premere `Barra spazio` per selezionare `blocca maiuscole` come tasto NVDA.
Si noti che le impostazioni sul layout della tastiera funzionano separatamente rispetto al tasto NVDA.
Il tasto NVDA e il layout della tastiera possono essere modificati in seguito dalle Impostazioni tastiera.
1. Utilizzare `tab` e `barra spazio` per regolare le altre opzioni su questa schermata.
Si tratta di stabilire se NVDA debba avviarsi automaticamente.
1. Premere `invio` per chiudere la finestra di dialogo con NVDA ora in esecuzione.

### Esecuzione di NVDA {#RunningNVDA}

La guida utente completa di NVDA contiene tutti i comandi del lettore di schermo, suddivisi in diverse sezioni per ottenere un facile riferimento.
Le tabelle dei comandi sono disponibili anche nella "Guida rapida ai comandi".
In inglese è stato prodotto del materiale formativo a pagamento che include esempi e ulteriori dettagli.
"Il materiale formativo di base per NVDA" è disponibile in inglese dal [negozio NV Access](http://www.nvaccess.org/shop).

Ecco alcuni comandi di base che vengono utilizzati frequentemente.
Tutti i comandi sono configurabili, quindi queste sono le sequenze di tasti predefinite per queste funzioni.

#### Il tasto funzione NVDA {#NVDAModifierKey}

Per impostazioni predefinite il tasto funzione NVDA è assegnato allo `zero del tastierino numerico`, (con `tastierino` spento), oppure al tasto `insert`, vicino al gruppo di sei tasti dove si trovano anche `cancella`, `inizio` e `fine`.
Il tasto funzione NVDA può anche essere assegnato al `blocca maiuscole`.

#### Aiuto immissione {#InputHelp}

Per imparare ed esercitarsi sulla posizione dei tasti, premere `NVDA+1` per attivare l'Aiuto immissione.
Con la modalità di aiuto immissione attivata, sarà possibile eseguire qualsiasi gesto (sia pressione di tasti o azioni sul touch screen) e lo screen reader annuncerà ciò che è stato premuto e la relativa azione associata (se presente).
I comandi effettivi non verranno eseguiti nella modalità di aiuto immissione.

#### Avviare e chiudere NVDA {#StartingAndStoppingNVDA}

| Nome |Tasto Desktop |tasto Laptop |Descrizione|
|---|---|---|---|
|Eseguire NVDA |`control+alt+n` |`control+alt+n` |Avvia o riavvia NVDA|
|Uscire da NVDA |`NVDA+q`, poi `invio` |`NVDA+q`, poi `invio` |Esce da NVDA|
|Pausa sintesi vocale |`maiusc` |`maiusc` |Mette in pausa all'istante la sintesi vocale. Ripremendo il tasto riprende da dove si era interrotto|
|Stop Sintesi vocale |`control` |`control` |Ferma immediatamente la sintesi vocale|

#### Leggere il testo {#ReadingText}

| Nome |Tasto Desktop |Tasto Laptop |Descrizione|
|---|---|---|---|
|Dire Tutto |`NVDA+Freccia Giù` |`NVDA+a` |Inizia a leggere dalla posizione del cursore di sistema sino alla fine del documento, spostando il cursore man mano che la lettura continua|
|Legge Riga Corrente |`NVDA+freccia su` |`NVDA+l` |Legge la riga sulla quale si trova il cursore di sistema. Premendo la combinazione due volte viene effettuato lo spelling della riga. La tripla pressione effettuerà lo spelling utilizzando la descrizione dei caratteri (ancona, bari, como, domodossola, etc|
|Legge Selezione corrente |`NVDA+Shift+freccia su` |`NVDA+shift+s` |Legge il testo selezionato, se presente. Premendo la combinazione due volte viene effettuato lo spelling della riga. La tripla pressione effettuerà lo spelling utilizzando la descrizione dei caratteri (ancona, bari, como, domodossola, etc|
|Legge testo negli appunti |`NVDA+c` |`NVDA+c` |Annuncia il testo contenuto negli appunti, se presente. Premendo la combinazione due volte viene effettuato lo spelling della riga. La tripla pressione effettuerà lo spelling utilizzando la descrizione dei caratteri (ancona, bari, como, domodossola, etc|

#### informazioni su posizione ed altro {#ReportingLocation}

| Nome |Tasto Desktop |Tasto Laptop |Descrizione|
|---|---|---|---|
|Legge il titolo |`NVDA+t` |`NVDA+t` |Legge il titolo della finestra attiva in quel momento. Premendo la combinazione due volte ne verrà fatto lo spelling. Premendo per tre volte il contenuto verrà copiato negli appunti.|
|Legge il focus |`NVDA+tab` |`NVDA+tab` |Annuncia l'oggetto o il controllo attualmente focalizzato. Premendo la combinazione due volte viene effettuato lo spelling della riga. La tripla pressione effettuerà lo spelling utilizzando la descrizione dei caratteri (ancona, bari, como, domodossola, etc|
|Legge la Finestra Attiva |`NVDA+b` |`NVDA+b` |Legge il contenuto della finestra in primo piano (utile nelle finestre di dialogo).|
|Legge la barra di stato |`NVDA+fine` |`NVDA+maiusc+fine` |Legge la barra di stato nel caso in cui NVDA sia in grado di individuarla. Una doppia pressione provocherà lo spelling delle informazioni. Una tripla pressione copierà il contenuto della barra di stato negli appunti|
|Legge la data e l'Ora |`NVDA+f12` |`NVDA+f12` |Premendo una volta viene annunciato l'orario corrente, mentre premendo due volte verrà annunciata la data. L'ora e la data sono riportate nel formato specificato nelle impostazioni di Windows per l'orologio della barra delle applicazioni.|
|Legge la formattazione |`NVDA+f` |`NVDA+f` |Legge la formattazione del testo; Una doppia pressione visualizzerà le informazioni in una finestra di dialogo|
|Legge la destinazione di un link |`NVDA+k` |`NVDA+k` |Una pressione leggerà l'URL di destinazione del collegamento alla posizione del focus. Una doppia pressione lo visualizzerà in una finestra per un controllo più dettagliato|

#### Stabilire quali informazioni NVDA debba leggere {#ToggleWhichInformationNVDAReads}

| Nome |Tasto Desktop |Tasto Laptop |Descrizione|
|---|---|---|---|
|Legge i caratteri digitati |`NVDA+2` |`NVDA+2` |Quando abilitato, NVDA annuncerà tutti i caratteri digitati sulla tastiera.|
|Legge le parole digitate |`NVDA+3` |`NVDA+3` |Quando abilitato, NVDA annuncerà tutte le parole digitate sulla tastiera.|
|Legge i tasti di comando |`NVDA+4` |`NVDA+4` |Quando attivato, NVDA leggerà tutti i tasti digitati che non rappresentano un carattere. Ciò comprende anche combinazioni di tasti quali control e un'altra lettera.|
|Abilita tracciamento del mouse |`NVDA+m` |`NVDA+m` |Quando attivata, istruisce NVDA ad annunciare il testo sul quale è posizionato il puntatore, mentre ci si sposta con esso sullo schermo. Questo permette di individuare gli elementi con una rappresentazione fisica e reale su come essi siano disposti sul video, piuttosto che utilizzare la navigazione ad oggetti.|

#### Impostare al volo il sintetizzatore {#TheSynthSettingsRing}

| Nome |Tasto Desktop |Tasto Laptop |Descrizione|
|---|---|---|---|
|Spostarsi al parametro successivo del sintetizzatore |`NVDA+control+FrecciaDestra` |`NVDA+Maiusc+control+FrecciaDestra` |Si sposta al prossimo parametro disponibile inerente la sintesi vocale e nel caso si sia raggiunto l'ultimo dell'elenco tornerà al primo|
|Spostarsi al parametro precedente del sintetizzatore |`NVDA+control+FrecciaSinistra` |`NVDA+Maiusc+control+FrecciaSinistra` |Si sposta al parametro precedente disponibile inerente la sintesi vocale e nel caso si sia raggiunto l'ultimo dell'elenco tornerà al primo|
|Aumentare il parametro corrente del sintetizzatore |`NVDA+Control+Freccia su` |`NVDA+Maiusc+Control+Freccia su` |Aumenta il valore del parametro sul quale si è posizionati. Ad esempio si aumenta la velocità, poi ci si sposta all'impostazione successiva, si aumenta il volume etc|
|Aumentare il parametro corrente del sintetizzatore con un incremento maggiore |`NVDA+control+pagina su` |`NVDA+shift+control+pagina su` |Aumenta il valore del parametro del sintetizzatore su cui si è posizionati con un incremento maggiore. Ad esempio, se ci si trova nelle impostazioni per scegliere la voce, avanzerà di 20 valori alla volta invece che uno soltanto; oppure, se ci si trova nei cursori di avanzamento (velocità, tono, etc) incrementerà il valore fino al 20%|
|Diminuire il parametro corrente del sintetizzatore |`NVDA+Control+Freccia giù` |`NVDA+Shift+Control+Freccia giù` |Diminuisce il valore del parametro sul quale si è posizionati. Ad esempio si diminuisce la velocità, poi ci si sposta all'impostazione successiva, si diminuisce il volume etc|
|Diminuire il parametro corrente del sintetizzatore con un decremento maggiore |`NVDA+control+pagina giù` |`NVDA+shift+control+pagina giù` |Diminuisce il valore del parametro del sintetizzatore su cui si è posizionati con un decremento maggiore. Ad esempio, se ci si trova nelle impostazioni per scegliere la voce, tornerà indietro di 20 valori alla volta invece che uno soltanto; oppure, se ci si trova nei cursori di avanzamento (velocità, tono, etc) diminuirà il valore fino al 20%|

È anche possibile impostare il primo o l'ultimo valore del parametro corrente del sintetizzatore assegnando gesti personalizzati nella [Finestra tasti e gesti di immissione](#InputGestures), nella categoria Voce.
Ciò significa, ad esempio, che se ci si trova nelle impostazioni della velocità, imposterà il valore a 0 o 100.
Se ci si trova invece nelle impostazioni per scegliere la voce, imposterà la prima o l'ultima voce.

#### Navigazione web {#WebNavigation}

L'elenco completo dei tasti di navigazione a lettere singole è disponibile nella sezione [Modalità di navigazione](#BrowseMode) della guida utente.

| Comando |tasto |Descrizione|
|---|---|---|
|Intestazione |`h` |Va all'intestazione successiva|
|Livello intestazione 1, 2, o 3 |`1`, `2`, `3` |Va all'intestazione successiva del livello specificato|
|Campo form |`f` |Va al campo form successivo (campo editazione, pulsante, etc)|
|Link |`k` |Va al prossimo link|
|Punto di riferimento |`d` |Va al prossimo punto di riferimento|
|Elenco |`l` |Va all'elenco successivo|
|Tabella |`t` |Va alla tabella successiva|
|Spostarsi all'indietro |`Maiusc+lettera` |Premere `maiusc` e una qualsiasi delle lettere viste sopra per passare all'elemento precedente di quel tipo|
|Elenco elementi |`NVDA+f7` |Elenca vari tipi di elementi, come collegamenti e intestazioni|

### Preferenze {#Preferences}

La maggior parte delle funzioni di NVDA può essere abilitata o modificata tramite le impostazioni del lettore di schermo.
Le impostazioni e altre opzioni sono disponibili tramite il menu di NVDA.
Per aprire il menu di NVDA, premere `NVDA+n`.
Per aprire direttamente la finestra di dialogo delle impostazioni generali di NVDA, premere `NVDA+control+g`.
Molte schermate delle impostazioni hanno sequenze di tasti per aprirle direttamente, come `NVDA+control+s` per sintetizzatore o `NVDA+control+v` per altre opzioni inerenti la voce.

### Gli Add-on {#Addons}
I componenti aggiuntivi, o add-on, sono pacchetti software che forniscono funzionalità innovative o vanno a modificare alcune caratteristiche di NVDA.
Vengono sviluppati dalla community di NVDA e da organizzazioni esterne quali fornitori commerciali o programmatori.
Come con qualsiasi software, è importante avere la massima fiducia nello sviluppatore di un componente aggiuntivo prima di utilizzarlo.
Fare riferimento a [Installazione degli add-on](#AddonStoreInstalling) per informazioni su come verificare i componenti aggiuntivi prima dell'installazione.

La prima volta che si apre lo store dei componenti aggiuntivi, NVDA visualizzerà un avviso importante.
Gli add-on non sono di responsabilità della NV Access e potrebbero disporre di funzioni e accesso alle informazioni illimitati.
Premere la `barra spaziatrice` se l'avviso risulta chiaro e non si necessita di rileggerlo in futuro.
Premere `tab` per raggiungere il pulsante "OK", poi `invio` per accettare l'avviso e procedere all'Add-on Store.
La sezione "[Componenti aggiuntivi e add-on store](#AddonsManager)" della Guida utente, come suggerisce il nome,  contiene informazioni su ogni funzionalità dello store e della gestione degli add-on.

Lo si trova dal menu strumenti di NVDA.
Premere `NVDA+n` per aprire il menu NVDA, quindi `t` per Strumenti, poi `a` per add-on store.
Una volta aperto l'add-on store, verranno mostrati i componenti aggiuntivi disponibili, nel caso in cui non sia ancora stato installato un add-on.
Invece, se è stato installato almeno un componente aggiuntivo, allora lo store si aprirà sulla scheda add-on installati.

#### Add-on disponibili {#AvailableAddons}
Quando la finestra si apre per la prima volta, il caricamento dei componenti aggiuntivi potrebbe richiedere alcuni secondi.
NVDA leggerà il nome del primo add-on una volta terminato il caricamento dell'elenco.
I componenti aggiuntivi disponibili vengono visualizzati in ordine alfabetico in un elenco a più colonne.
Ecco come sfogliare la lista e trovare un-addon specifico:

1. Utilizzare i tasti freccia o premere la prima lettera del nome di un componente aggiuntivo per spostarsi nell'elenco.
1. Premere `tab` una volta per passare alla descrizione dell'add-on attualmente selezionato.
1. Utilizzare i [tasti di lettura](#ReadingText) o i tasti freccia per leggere la descrizione completa.
1. Premere `tab` fino al pulsante "Azioni", che può essere utilizzato, tra le altre cose, per installare l'add-on.
1. Premere `tab` su "Altri dettagli", per ottenere informazioni quali l'editore, la versione e la home page.
1. Per tornare all'elenco dei componenti aggiuntivi, premere `alt+a` o `shift+tab` fino a raggiungere l'elenco.

#### Cercare tra gli add-on {#SearchingForAddons}
Oltre a sfogliare tutti i componenti aggiuntivi disponibili, è anche possibile filtrare gli add-on visualizzati.
Per effettuare la ricerca, premere `alt+s` per passare al campo "Cerca" e digitare quindi il testo da cercare.
La ricerca verifica le corrispondenze nei campi ID componente aggiuntivo, nome visualizzato, editore, autore e descrizione.
L'elenco si aggiorna man mano che si digitano i termini di ricerca.
Una volta terminato, premere `tab` per accedere all'elenco filtrato dei componenti aggiuntivi e sfogliare i risultati.

#### Installare un add-on {#InstallingAddons}

Per installare un componente aggiuntivo:

1. Con il focus sull'add-on che si desidera installare, premere `invio`.
1. Si aprirà il menu azioni con un elenco di voci; la prima azione è "Installa".
1. Per installare il componente aggiuntivo, premere la lettera `i`, oppure la `frecciaGiù` per andare su "Installa" e premere `invio`.
1. Il focus ritornerà sull'add-on nell'elenco e NVDA ne leggerà i dettagli.
1. Le informazioni sullo "Stato" annunciate da NVDA cambiano da "Disponibile" a "Download in corso".
1. Una volta terminato il download, lo stato del componente aggiuntivo cambierà in "Scaricato. Installazione in attesa".
1. Ripetere l'operazione per tutti gli altri componenti aggiuntivi che si desidera installare contemporaneamente.
1. Una volta terminato, premere `tab` fino a che il focus raggiungerà il pulsante "Chiudi", quindi premere `invio`.
1. I componenti aggiuntivi scaricati avvieranno il processo di installazione una volta chiuso l'Add-on Store.
Durante il processo di installazione, i componenti aggiuntivi potrebbero visualizzare finestre di dialogo a cui si dovrà rispondere.
1. Una volta installati i componenti aggiuntivi, verrà visualizzata una finestra di dialogo che informa che sono state apportate modifiche e sarà necessario riavviare NVDA.
1. Premere `invio` per riavviare lo screen reader.

#### Gestione dei componenti aggiuntivi installati {#ManagingInstalledAddons}
Premere `control+tab` per spostarsi tra le schede dell'add-on store.
Le schede includono: "add-on installati", "Add-on aggiornabili", "Add-on disponibili" e "Add-on incompatibili installati".
Ciascuna scheda è strutturata in modo simile alle altre, con un elenco di componenti aggiuntivi, un pannello che fornisce maggiori dettagli e un pulsante per eseguire azioni per il componente aggiuntivo selezionato.
Il menu delle azioni per gli add-on installati contiene le voci "Disabilita" e "Rimuovi" anziché "Installa".
La disattivazione di un componente aggiuntivo impedisce a NVDA di caricarlo, ma lo lascia installato.
Per riattivare un add-on disabilitato, utilizzare la voce "Abilita" dal menu azioni.
Dopo aver abilitato, disabilitato o rimosso gli add-on, verrà richiesto di riavviare NVDA alla chiusura dell-addon store..
Queste modifiche avranno effetto solo una volta riavviato NVDA.
Si tenga presente che nella finestra dell'add-on store, il tasto `escape` funziona allo stesso modo del pulsante Chiudi.

#### Aggiornamento dei componenti aggiuntivi {#UpdatingAddons}
Quando è disponibile un aggiornamento per un componente aggiuntivo installato, verrà mostrato nella scheda "add-on aggiornabili".
Premere `control+tab` per accedere a questa scheda da qualsiasi punto dell'add-on store.
Lo stato del componente aggiuntivo verrà visualizzato come "Aggiornamento disponibile".
L'elenco mostrerà la versione attualmente installata e la versione disponibile.
Premere `invio` sull'add-on per aprire il menu azioni; scegliere "Aggiorna".

### Comunità {#Community}

NVDA dispone di una vivace comunità di utenti.
In primo luogo, esiste il [gruppo di discussione in italiano](https://groups.io/g/nvda-it), [quello internazionale](https://nvda.groups.io/g/nvda) oltre ad una pagina con [le liste di discussione in varie lingue](https://github.com/nvaccess/nvda-community/wiki/Connect).
La NV Access, ossia chi sviluppa NVDA, è molto attiva su [Twitter](https://twitter.com/nvaccess) e [Facebook](https://www.facebook.com/NVAccess).
Inoltre questa organizzazione dispone di un [blog con le ultime novità](https://www.nvaccess.org/category/in-process/).

Esiste, sempre in inglese, un programma per acquisire la [certificazione di esperto NVDA](https://certification.nvaccess.org/).
Si tratta di un esame online che è possibile completare per dimostrare le proprie competenze con NVDA.
[Gli esperti in NVDA con questo certificato](https://certification.nvaccess.org/) hanno la possibilità di inserire i loro contatti e altre informazioni aziendali.

### Ottenere aiuto {#GettingHelp}

Per ottenere aiuto su NVDA, premere `NVDA+n` per aprire il menu, quindi `a` per aiuto.
Da questo sottomenu sarà possibile consultare il presente manuale, un documento contenente tutti i comandi rapidi, oppure la cronologia delle nuove funzionalità e altro ancora.
Queste prime tre opzioni si aprono nel browser Web predefinito.
Esiste anche del materiale aggiuntivo solo in inglese nel [Negozio NV Access](https://www.nvaccess.org/shop).

In merito a tale materiale, risulta sicuramente utile quello denominato "Basic Training for NVDA module".
Tale modulo copre diversi concetti a partire dalle prime operazioni di base con NVDA, passando poi per l'esplorazione web fino alla navigazione ad oggetti.
è disponibile in:

* [Testo elettronico](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), che include i formati Word DOCX, pagine Web HTML, eBook ePub e Kindle KFX.
* [Letto da voce umana, audio MP3](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Copia cartacea in braille inglese unificato ueb](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) con consegna inclusa ovunque nel mondo.

Altri moduli, oltre al [Pacchetto produttività NVDA](https://www.nvaccess.org/product/nvda-productivity-bundle/) scontato, sono reperibili nel [Negozio NV Access](https://www.nvaccess.org/shop/).

La NV Access rivende anche il [supporto telefonico in inglese](https://www.nvaccess.org/product/nvda-telephone-support/), in blocchi o come parte del [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Il supporto telefonico include i numeri locali in Australia e negli Stati Uniti.

I [gruppi di utenti e-mail](https://github.com/nvaccess/nvda-community/wiki/Connect) sono un'ottima fonte di aiuto per la comunità, così come gli [esperti con certificazione NVDA](https://certification.nvaccess.org/).

Si possono segnalare bug o richiedere nuove caratteristiche tramite [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
Le [linee guida per il contributo](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) contengono informazioni preziose per collaborare con la comunità.

## Altre opzioni di configurazione {#MoreSetupOptions}
### Opzioni di installazione {#InstallingNVDA}

Se si installa NVDA direttamente dall'eseguibile appena scaricato, premere il pulsante Installa NVDA.
Se invece è già stata chiusa questa finestra di dialogo o si desidera eseguire l'installazione da una copia portable, scegliere la voce di menu Installa NVDA situata in Strumenti nel menu NVDA.

La finestra di dialogo che appare consente di stabilire se si desidera installare NVDA ed effettuerà un controllo nel caso in cui questa installazione debba aggiornare una versione precedente.
Premendo il pulsante Continua verrà avviata l'installazione di NVDA.
Ci sono anche alcune opzioni in questa finestra di dialogo che sono spiegate di seguito.
Una volta completata l'installazione, verrà visualizzato un messaggio che informa del buon esito dell'operazione.
A questo punto, premendo OK si riavvierà la copia di NVDA appena installata.

#### Avviso sui componenti aggiuntivi non compatibili {#InstallWithIncompatibleAddons}

Se vi sono già installati componenti aggiuntivi, è possibile che venga visualizzato un messaggio che avverte l'utente dell'imminente disabilitazione dei componenti non compatibili.
Prima di poter premere il pulsante continua, è necessario selezionare la casella di controllo che indica che l'utente ha compreso che gli addon non compatibili saranno disattivati.
è presente anche un pulsante che consente di controllare quali componenti aggiuntivi verranno disabilitati.
Si veda la [sezione componenti aggiuntivi non compatibili](#incompatibleAddonsManager) per maggiori informazioni su questo pulsante.
Dopo l'installazione, è possibile riattivare i componenti aggiuntivi incompatibili a proprio rischio e pericolo dall'[Add-on Store](#AddonsManager).

#### Utilizza NVDA durante l'accesso {#StartAtWindowsLogon}

Questa opzione permette di stabilire se NVDA debba automaticamente avviarsi o meno alla finestra di accesso a Windows, prima di inserire la password.
Inoltre, questo permette la lettura delle finestre controllo account utente e di [altri controlli sulla sicurezza](#SecureScreens).
Questa opzione è abilitata di default per le nuove installazioni.

#### Crea collegamento per il desktop e il tasto rapido (Control+alt+n) {#CreateDesktopShortcut}

Questa opzione permette di selezionare se NVDA debba creare o meno un collegamento nel desktop per lanciare lo screen reader.
Inoltre, se viene creato tale collegamento, verrà assegnato un tasto rapido corrispondente alla combinazione `Control+alt+n`, che permetterà di eseguire NVDA da qualsiasi punto ci si trovi.

#### Copia la configurazione portable nelle impostazioni dell'utente attuale {#CopyPortableConfigurationToCurrentUserAccount}

Questa opzione permette di selezionare se NVDA debba copiare o meno la configurazione utente, dalla copia in esecuzione di NVDA, nelle impostazioni dell'utente loggato per la copia installata dello screen reader.
Tali impostazioni non verranno copiate per eventuali altri utenti, e nemmeno per la configurazione di sistema, ossia tutto ciò che riguarda il logon di Windows e le [schermate inerenti la sicurezza](#SecureScreens).
L'opzione è disponibile soltanto quando si installa da una copia portable, non quindi se si installa direttamente dal pacchetto scaricato.

### Creazione di una copia portable {#CreatingAPortableCopy}

Se si desidera creare una copia portable dal pacchetto principale, premere il pulsante "Crea copia portable".
Se invece si vuole creare una copia portable da una versione già installata di NVDA, sarà sufficiente andare al menu strumenti e selezionare la voce "Crea copia Portable".

La finestra di dialogo che apparirà richiede la selezione della cartella nella quale inserire la versione portable.
Può trattarsi di una cartella presente nel disco fisso, oppure dell'unità di una penna USB o di un altro dispositivo rimovibile.
Esiste un'altra opzione, che permette di stabilire se NVDA debba copiare o meno la configurazione dell'utente attualmente loggato nella nuova versione portable che si desidera creare.
Questa opzione è disponibile solo quando si vuole creare una copia portable a partire da una versione installata, non quando la si crea dal pacchetto scaricato.
La pressione del pulsante "Continua" darà inizio al processo di creazione della versione portable.
Una volta terminata l'operazione, apparirà un messaggio di conferma.
Premere a questo punto il pulsante OK per chiudere questa finestra.

### Restrizioni nelle versioni portable o temporanee {#PortableAndTemporaryCopyRestrictions}

Se si desidera copiare NVDA in un supporto rimovibile come una chiavetta USB e portarlo con sé, si consiglia di creare una copia portable.
La copia installata è anche in grado di creare una copia portable di se stessa in qualsiasi momento.
Allo stesso modo, la copia portable dispone anche della capacità di installarsi su qualsiasi computer in un secondo momento.
Tuttavia, se invece si desidera copiare NVDA su un supporto di sola lettura come un CD, si dovrà semplicemente copiare il file contenente il pacchetto scaricato in precedenza.
Si tenga presente che non è possibile al momento eseguire una versione portable in un supporto di sola lettura.

[L'installer di NVDA](#StepsForRunningTheDownloadLauncher) può essere utilizzato come copia temporanea dello screen reader.
Le copie temporanee non consentono di salvare le impostazioni del lettore di schermo.
A ciò va aggiunta l'impossibilità di servirsi dell'[Add-on Store](#AddonsManager).

Le versioni temporanee o portable di NVDA presentano le seguenti limitazioni:

* Impossibilità di avviarsi automaticamente durante e/o dopo l'accesso.
* Incapacità di interagire con programmi eseguiti con privilegi di amministratore, a meno che naturalmente lo stesso NVDA non venga eseguito con privilegi amministrativi (non consigliato).
* Impossibilità di leggere le schermate del controllo Utente (UAC), quando si cerca di avviare un'applicazione con privilegi amministrativi.
* Impossibilità di gestire la scrittura o qualsiasi operazione effettuata tramite Touch Screen.
* Impossibilità di fornire le caratteristiche di ripetizione dei caratteri digitati e l'utilizzo della modalità navigazione in Windows Store.
* La funzione di attenuazione audio non è supportata.

## Utilizzare NVDA {#GettingStartedWithNVDA}
### Avviare NVDA {#LaunchingNVDA}

Se si è installato NVDA tramite l'installer, per avviarlo basta premere semplicemente control+alt+n, o scegliere la voce NVDA dal menu NVDA sotto programmi del menu avvio. 
In alternativa è possibile digitare NVDA dalla finestra di dialogo esegui e premere invio.
Se NVDA è già in esecuzione, verrà riavviato.
Inoltre risulta possibile servirsi di alcuni [parametri a riga di comando](#CommandLineOptions) che permettono di uscire (-q), disattivare i componenti aggiuntivi (--disable-addons) etc.

Nelle versioni installate, NVDA salva i file di configurazione nella cartella roaming application data del profilo utente (ad esempio "`C:\Users\<user>\AppData\Roaming`").
è possibile modificare questo parametro in modo tale che NVDA carichi la configurazione dalla cartella local application data.
Vedere la sezione inerente [parametri di sistema](#SystemWideParameters) per maggiori dettagli.

Per avviare la versione portable, spostarsi nella cartella nella quale si è scompattato NVDA e premere invio o far doppio click su NVDA.exe.
Se NVDA risulta già in esecuzione, esso verrà chiuso e poi sarà eseguita la copia portable.

Appena NVDA si avvia, si udiranno una serie di suoni ascendenti (segno che NVDA si sta caricando). Si dovrebbe poi sentire il messaggio“NVDA attivato. 
A seconda della velocità del proprio computer o che si stia lanciando NVDA da una chiavetta USB o da qualsiasi altro supporto lento, NVDA potrebbe richiedere più tempo per avviarsi. 
In questo caso dovrebbe venir annunciato "caricamento in corso, attendere prego".

Nel caso questo non avvenga o si senta il suono d'errore di sistema o una serie di suoni discendenti, significa che si è verificato un errore in NVDA ed è necessario comunicare possibilmente il bug agli sviluppatori. 
Consultare il sito di NVDA su come procedere per farlo.

#### Finestra di benvenuto {#WelcomeDialog}

Quando NVDA si avvia per la prima volta, sarete accolti da una finestra di benvenuto che fornirà informazioni basilari sulle impostazioni del tasto funzione "NVDA" e sul menu. 
Si vedano le sezioni successive di questo documento per ulteriori dettagli. 
La finestra di dialogo contiene una casella combinata e tre caselle di controllo.
La casella combinata consente di selezionare il layout tastiera.
La prima casella di controllo permette di stabilire se NVDA debba usare il tasto "Blocca Maiuscole" come tasto funzione "NVDA".
La seconda permette di specificare se NVDA debba avviarsi automaticamente dopo l'accesso a Windows ed è disponibile solo per le copie installate dello screen reader.
La terza invece permette di decidere se questa finestra debba presentarsi ad ogni avvio dello Screen Reader.

#### Finestra di dialogo statistiche sull'utilizzo dei dati {#UsageStatsDialog}

A partire da NVDA 2018.3, viene chiesto all'utente il consenso alll'invio dei dati di utilizzo a NV Access al fine di contribuire a migliorare NVDA in futuro.
Quando si avvia NVDA per la prima volta, viene visualizzata una finestra di dialogo dove si richiede di accettare l'invio di dati a NV Access durante l'utilizzo dello screen reader.
È possibile leggere ulteriori informazioni riguardo i dati raccolti da NV Access nella sezione impostazioni generali, [Consenti a NVAccess di raccogliere statistiche sull'utilizzo dello screen reader](#GeneralSettingsGatherUsageStats).
Nota: premendo "sì" o "no" l'impostazione verrà salvata e la finestra di dialogo non verrà più visualizzata se non si reinstalla NVDA.
Tuttavia, è possibile abilitare o disabilitare manualmente il processo di raccolta dei dati nelle impostazioni generali di NVDA. Per modificare questa impostazione, selezionare o deselezionare la casella di controllo denominata [Consenti al progetto NVDA di raccogliere statistiche sull'utilizzo dello screen reader](#GeneralSettingsGatherUsageStats).

### Sui comandi da tastiera di NVDA {#AboutNVDAKeyboardCommands}
#### Il tasto funzione NVDA {#TheNVDAModifierKey}

La maggior parte dei comandi da tastiera di NVDA è costituita dalla combinazione del tasto funzione NVDA più qualsiasi altro tasto o serie di tasti. 
Fanno eccezione i tasti di revisione del testo che utilizzano i soli tasti del tastierino numerico.

NVDA può essere configurato in modo tale che sia il tasto Insert del tastierino numerico, sia l'Insert della tastiera estesa e il tasto Blocca Maiuscole agiscano contemporaneamente come tasto funzione NVDA.
Da impostazioni predefinite entrambi i tasti Insert, della tastiera estesa e del tastierino, sono configurati come tasti funzione di NVDA.

Se si desidera che uno dei tasti funzione NVDA agisca usando la sua funzione originale (ad esempio si potrebbe volere attivare il BloccaMaiuscole che però è stato impostato come tasto funzione NVDA) sarà sufficiente premere quel tasto due volte in rapida successione.

#### Layout Tastiera {#KeyboardLayouts}

Al momento NVDA viene distribuito con due set di comandi per le tastiere. Esiste infatti un layout denominato "desktop", utile per i computer fissi, ed uno chiamato "laptop", più consono ai pc portatili.
Da impostazioni predefinite, NVDA utilizza il layout Desktop, tuttavia sarà sempre possibile modificare questo parametro accedendo alla categoria Tastiera nelle [impostazioni di NVDA](#NVDASettings), situate sotto la voce Preferenze del menu di NVDA.

Il Layout Desktop fa un uso massiccio del tastierino numerico (con NumLock impostato su spento).
Sebbene molti portatili non siano in possesso di un tastierino numerico fisico, molti di essi possono emularne le funzioni tenendo premuto il tasto FN e premendo lettere e numeri sulla parte destra della tastiera (7 8 9 u i o j k l etc).
Se il portatile in proprio possesso non è in grado di compiere questa operazione, o non permette di impostare il tasto Numlock su spento, può risultare conveniente passare al layout Laptop.

### Gesti di NVDA nei dispositivi a tocco {#NVDATouchGestures}

Se si sta eseguendo NVDA in un dispositivo dotato di touch screen, è possibile controllare lo screen reader direttamente dallo schermo.
Quando NVDA è in esecuzione, a meno che il supporto per l'interazione al tocco non sia stato disattivato, tutti i gesti di immissione a tocco verranno diretti a NVDA.
Tenere presente che le azioni che normalmente funzionerebbero senza NVDA non saranno disponibili.
<!-- KC:beginInclude -->
Per attivare o disattivare il supporto TouchScreen di NVDA, premere NVDA+control+alt+t.
<!-- KC:endInclude -->
è anche possibile attivare o disattivare il [supporto al touch screen](#TouchSupportEnable) dalla categoria tocco delle impostazioni di NVDA.

#### Esplorazione dello schermo {#ExploringTheScreen}

La caratteristica più basilare che ci si può aspettare toccando un touch screen è l'annuncio dei controlli o del testo presenti sullo schermo. 
Per fare questo, posizionare un dito in un punto qualsiasi di quest'ultimo.
è anche possibile mantenere il dito sullo schermo e iniziare a spostarsi, mentre lo screen reader leggerà gli oggetti o il testo che si incontrerà man mano.

#### Gesti touch {#TouchGestures}

Nella descrizione dei comandi che si incontrerà più avanti in questo manuale, si parlerà anche di gesti a tocco che possono venir utilizzati per attivare quel comando sul touch screen.
Di seguito vengono riportate alcune istruzioni di massima per utilizzare correttamente i comandi a tocco.

##### Tap {#Taps}

Toccare lo schermo velocemente con uno o più dita.

Il gesto di toccare una volta con un dito viene comunemente chiamato tocco, in inglese tap.
Il gesto di toccare una volta con due dita viene chiamato tocco con due dita, e così via.

Se un tap viene eseguito in rapida successione, NVDA lo interpreterà come un gesto multitocco.
Toccare velocemente per due volte viene chiamato doppio tap e così via.
Toccare velocemente per tre volte viene chiamato triplo tap, e così via.
Naturalmente, nei gesti multi-tocco viene riconosciuto anche il numero di dita che si utilizza, per cui possiamo avere gesti del tipo "triplo tocco con due dita", tap con quattro dita, etc.

##### Scorrimento {#Flicks}

Scorrere velocemente il dito sullo schermo, in inglese flick.

Vi sono quattro gesti di scorrimento che dipendono dalla direzione: scorrimento a destra, scorrimento a sinistra, scorrimento in alto e scorrimento in basso.

Esattamente come nei tap, il gesto può essere eseguito con più di un dito.
Per cui, risulta possibile compiere gesti come lo scorrimento in alto con due dita o lo scorrimento a sinistra con quattro dita.

#### Modalità di tocco {#TouchModes}

Poiché esistono molti più comandi di NVDA rispetto ai gesti che possono essere eseguiti, NVDA permette di passare tra diverse modalità di tocco per far sì che possano essere impartiti il maggior numero di comandi attraverso i gesti.
Le due modalità previste sono la modalità testo e quella a oggetti.
Alcuni comandi di NVDA elencati in questa guida possono prevedere una modalità di tocco particolare, scritta tra parentesi, dopo il gesto.
Ad esempio, scorrimento verso l'alto (modo testo), significa che il gesto sarà eseguito soltanto se ci si trova nella modalità di tocco testo.
Se il comando non presenta una modalità di tocco, funzionerà in ogni circostanza.

<!-- KC:beginInclude -->
Per cambiare la modalità di tocco, eseguire un tocco con tre dita.
<!-- KC:endInclude -->

#### Tastiera a tocco {#TouchKeyboard}

La tastiera a tocco viene utilizzata per inserire testo e comandi da un touch screen.
Quando ci si trova in un campo editazione, è possibile servirsi della tastiera a tocco effettuando un doppio tap sull'icona della tastiera virtuale sulla parte bassa dello schermo.
Per quel che concerne i tablet come il Microsoft Surface Pro, la tastiera a tocco è sempre disponibile non appena si rimuove la tastiera dall'alloggiamento.
Per chiudere la tastiera a tocco, effettuare un doppio tap sulla medesima icona oppure spostarsi dal campo editazione.

Mentre la tastiera touch è attiva, per individuare le varie lettere, spostare le dita nella posizione in cui è situata la tastiera touch (generalmente nella parte inferiore dello schermo), ed esplorarla con un dito.
Una volta individuato il tasto desiderato, per attivarlo è sufficiente effettuare un doppio tap oppure rilasciare il tasto, ciò dipende da come sono state configurate le opzioni della [categoria impostazioni interazione al tocco](#TouchInteraction) nelle impostazioni di NVDA.

### Modalità Aiuto immissione {#InputHelpMode}

La maggior parte dei comandi verrà citata in seguito nella presente guida, ma una maniera pratica per conoscerli, è di attivare l'aiuto immissione.

Per farlo basta premere NVDA+1.
Per disattivarlo basta ripremerlo nuovamente.
Durante tale modalità, verranno annunciate le funzionalità associate ai vari tasti o gesti se presenti senza però eseguirle. 
Si è perciò liberi di premere ciò che si desidera senza preoccuparsi degli effetti.

### Il menu di NVDA {#TheNVDAMenu}

Il menu di NVDA consente di controllare le impostazioni dello screen reader, accedere all'aiuto in linea, salvare/ricaricare le configurazioni, modificare i dizionari per le sintesi vocali, leggere i file di log e uscire dal programma.

Per accedere al menu di NVDA da qualsiasi punto ci si trovi in Windows mentre NVDA è in esecuzione, eseguire una delle seguenti operazioni:

* Premere la combinazione di tasti `NVDA+n` sulla tastiera.
* effettuare un doppio tap con due dita sul touch screen.
* premere `Windows+B` per raggiungere la system tray, scorrere con la `frecciaGiù` sino ad arrivare alla voce NVDA e premere `invio`.
* In alternativa, accedere alla system tray premendo `Windows+b`, `freccia giù` sino a giungere sull'icona NVDA e aprire il menu contestuale premendo il tasto `applicazioni` situato accanto al tasto control destro sulla maggior parte delle tastiere.
Se la tastiera è sprovvista di tasto `applicazioni`, premere `Maiusc+f10`.
* Fare clic con il tasto destro sull'icona NVDA situata nella system tray di Windows

Una volta che il menu appare, è possibile scorrerlo con le frecce direzionali, mentre per attivare un elemento come sempre è sufficiente premere `invio`.

### Comandi di base da tastiera {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Nome |Tasto Desktop |Tasto laptop |Tocco |Descrizione|
|---|---|---|---|---|
|Esegue o Riavvia NVDA |Control+alt+n |Control+alt+n |none |Esegue o riavvia NVDA dal desktop, se durante il processo di installazione di NVDA si è scelto di creare un collegamento. Si tratta di un collegamento specifico di Windows e pertanto non può essere riassegnato nella finestra di dialogo dei gesti di immissione.|
|Interrompe la Sintesi Vocale |Control |Control |tocco con due dita |Ferma immediatamente la Sintesi Vocale|
|Pausa Sintesi Vocale |Shift |shift |Nessuno |Mette in pausa immediatamente la Sintesi Vocale. Premendo nuovamente il tasto la sintesi vocale riprenderà a parlare dal punto in cui era stata fermata (sempre che questo sia supportato dal sintetizzatore utilizzato, in genere non dovrebbe costituire un problema)|
|Menu NVDA |NVDA+n |NVDA+n |Doppio tocco con due dita |Mostra il Menu di NVDA per permettere di accedere alle Preferenze, agli strumenti, all'Aiuto etc|
|Commuta Modalità Aiuto Immissione |NVDA+1 |NVDA+1 |Nessuno |in questa modalità sarà possibile premere qualsiasi tasto e ne verrà annunciato il nome e la propria funzione in NVDA|
|Uscire da NVDA |NVDA+q |NVDA+q |Nessuno |Esce da NVDA|
|Passa Tasto Successivo a |NVDA+f2 |NVDA+f2 |Nessuno |Questo comando istruisce NVDA a passare la combinazione di tasti successiva all'applicazione attiva, anche se si tratta di un comando di NVDA.|
|Attiva/disattiva modalità riposo |NVDA+shift+s |NVDA+Shift+z |Nessuno |La modalità riposo, sleep mode disabilita tutti i comandi di NVDA e l'output tramite voce/braille per l'applicazione corrente. Risulta utile se si ha a che fare con programmi che forniscono direttamente indicazioni vocali (audiogame, centralini telefonici, etc). Ripremere la combinazione di tasti per disattivare questa funzione.|

<!-- KC:endInclude -->

### Conoscere Informazioni di sistema {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Annuncia data/Ora |NVDA+f12 |Premendo una volta questa combinazione di tasti viene annunciato l'orario corrente, mentre premendola due volte verrà annunciata la data|
|Annuncia stato batteria |NVDA+shift+b |Annuncia elementi come la percentuale di carica della batteria, se il computer è collegato alla corrente, etc.|
|Legge testo negli appunti |NVDA+c |Annuncia il testo contenuto negli appunti, se presente.|

<!-- KC:endInclude -->

### Modalità di voce {#SpeechModes}

La modalità vocale determina il modo in cui il contenuto dello schermo, le notifiche, le risposte ai comandi e altri output vengono pronunciati durante il funzionamento di NVDA.
L'impostazione predefinita è "parla", che poi è quello che qualsiasi utente di screen reader si aspetta, ossia una sintesi vocale che legge il contenuto quando necessario.
Tuttavia, in determinate circostanze, o quando si eseguono programmi particolari, ci si può avvalere di una delle altre modalità elencate di seguito.

Le quattro modalità vocali disponibili sono:

* Parlare (Default): NVDA parlerà normalmente reagendo ai cambiamenti dello schermo, alle notifiche e ad azioni come lo spostamento del focus o l'invio di comandi.
* Su richiesta: NVDA parlerà solo quando si utilizzano comandi con funzione di segnalazione (ad esempio leggere il titolo di una finestra); invece, non parlerà con azioni come lo spostamento del focus o del cursore.
* Spenta: NVDA non dirà nulla, tuttavia, a differenza della modalità riposo, reagirà silenziosamente ai comandi.
* Beep: NVDA sostituirà il parlato normale con brevi segnali acustici.

La modalità Beep può essere utile ad esempio nelle finestre di terminale quando c'è tantissimo testo che scorre ininterrottamente; a quel punto, può essere importante sapere che il testo sta scorrendo, piuttosto che leggere tutte le informazioni. Quando non si sentono più bip, significa che probabilmente si può ricominciare ad operare.

La modalità su richiesta può essere utile quando non si ha bisogno di un feedback costante su ciò che accade sullo schermo o sul computer, ma si necessita periodicamente di controllare cose particolari utilizzando comandi di revisione, oppure in concomitanza con l'uso del display braille.
Alcuni esempi possono riguardare una registrazione audio, oppure quando si utilizza l'ingrandimento dello schermo, o durante una riunione o una chiamata o come alternativa alla modalità beep.

Esiste un comando rapido che permette di passare tra le varie modalità:
<!-- KC:beginInclude -->

| Nome |tasto |Descrizione|
|---|---|---|
|Passa tra le modalità di voce |`NVDA+s` |Passa tra le modalità di voce.|

<!-- KC:endInclude -->

Se si desidera avvalersi solo di alcune di queste modalità eliminando le altre, vedere [Modalità disponibili nel comando Passa tra le modalità di voce](#SpeechModesDisabling).

## Esplorare lo schermo con NVDA {#NavigatingWithNVDA}

NVDA permette di navigare ed esaminare il sistema in vari modi, sia in maniera diretta e convenzionale, sia in modalità esplorazione.

### Oggetti {#Objects}

Ciascuna applicazione ed anche il sistema operativo stesso consistono in un'insieme di oggetti.
Un oggetto è un elemento singolo come un pezzo di testo, un bottone, una casella di controllo, un cursore di avanzamento, un elenco o un campo di testo editabile.

### Esplorare con il focus di sistema {#SystemFocus}

Il focus di sistema, conosciuto semplicemente anche come focus, è l' [oggetto](#Objects) che riceve la pressione dei tasti sulla tastiera.
Ad esempio, se si sta scrivendo in un campo editazione, quel campo editazione ha il focus.

Il modo più comune di esplorare le finestre con NVDA è proprio quello di utilizzare i normali comandi da tastiera come tab e shift tab per muoversi avanti ed indietro attraverso i vari controlli, alt per accedere alla barra dei menu quindi le frecce per esplorare i menu stessi ed alt-tab per spostarsi tra le applicazioni in esecuzione.
Così facendo, NVDA fornirà informazioni sull'oggetto sul quale è posizionato il focus, come il suo nome, tipo, valore, stato, descrizione, tasto caldo e informazioni sulla posizione.
Quando [l'evidenziatore focus](#VisionFocusHighlight) è attivato, viene evidenziata sullo schermo la posizione corrente del focus di sistema.

Esistono alcuni comandi da tastiera utili per seguire il focus:
<!-- KC:beginInclude -->

| Nome |Tasto desktop |Tasto laptop |Descrizione|
|---|---|---|---|
|Legge il focus |NVDA+tab |NVDA+tab |Annuncia l'oggetto o il controllo attualmente focalizzato. Premendo la combinazione due volte ne verrà fatto lo spelling|
|Legge il Titolo |NVDA+t |NVDA+t |Legge il titolo della finestra attiva in quel momento. Premendo la combinazione due volte ne verrà fatto lo spelling. Premendo per tre volte il contenuto verrà copiato negli appunti.|
|Legge la Finestra Attiva |NVDA+b |NVDA+b |Legge il contenuto della finestra in primo piano (utile nelle finestre di dialogo).|
|Legge la barra di stato |NVDA+fine |NVDA+shift+fine |Legge la barra di stato nel caso in cui NVDA sia in grado di individuarla. Una doppia pressione provocherà lo spelling delle informazioni. Una tripla pressione copierà il contenuto della barra di stato negli appunti|
|Legge tasto di scelta rapida |`maiusc+numpad2` |`NVDA+control+maiusc+.` |Legge il tasto di scelta rapida dell'oggetto su cui si trova il focus|

<!-- KC:endInclude -->

### Esplorare con il cursore di sistema {#SystemCaret}

Quando un [oggetto](#Objects) che permette l'esplorazione o la modifica del testo è [focalizzato](#SystemFocus), ci si può spostare nel testo utilizzando il cursore di sistema, conosciuto anche semplicemente come cursore.

Quando il focus si trova in un oggetto che contiene il cursore di sistema, si possono utilizzare i tasti di direzione, pagina su, pagina giù, inizio, fine, etc per muoversi nel testo.
Naturalmente se il controllo lo prevede sarà anche possibile modificare il testo.
NVDA leggerà non appena ci si sposterà per caratteri, parole e righe, notificando inoltre il testo selezionato o deselezionato. 

NVDA fornisce i seguenti comandi quando si lavora con il cursore di sistema:
<!-- KC:beginInclude -->

| Nome |Tasto desktop |Tasto laptop |Descrizione|
|---|---|---|---|
|Dire Tutto |NVDA+Freccia Giù |NVDA+a |Inizia a leggere dalla posizione del cursore di sistema sino alla fine del documento, spostando il cursore man mano che la lettura continua|
|Legge Riga Corrente |NVDA+freccia su |NVDA+l |Legge la riga sulla quale si trova il cursore di sistema. Premendo la combinazione due volte viene effettuato lo spelling della riga. La tripla pressione effettuerà lo spelling utilizzando la descrizione dei caratteri (ancona, bari, como, domodossola, etc|
|Legge Selezione corrente |NVDA+Shift+freccia su |NVDA+shift+s |Legge il testo selezionato ammesso che ve ne sia uno.|
|Annuncia formattazione testo |NVDA+f |NVDA+f |Legge la formattazione del testo alla posizione del cursore di sistema. Una doppia pressione visualizzerà le informazioni in modalità navigazione|
|Legge destinazione link |`NVDA+k` |`NVDA+k` |Premendo una volta verrà letto l'URL di destinazione del collegamento alla posizione del cursore o del focus. La doppia pressione mostrerà il contenuto in una finestra per poterlo analizzare più comodamente|
|Legge posizione cursore |NVDA+Canc tastierino numerico |NVDA+canc |Fornisce informazioni inerenti il testo o l'oggetto su cui è situato il cursore di sistema. Ad esempio, ciò potrebbe includere la percentuale in un documento, la distanza dal bordo della pagina o la posizione esatta dello schermo. Premendo due volte si possono ottenere ulteriori dettagli.|
|frase successiva |alt+freccia Giù |alt+freccia Giù |Sposta il cursore sulla frase successiva e la legge. (Supportato solo in Microsoft Word e Outlook)|
|frase precedente |alt+freccia Su |alt+freccia Su |Sposta il cursore sulla frase precedente e la legge. (Supportato solo in Microsoft Word e Outlook)|

Se ci si trova all'interno di una tabella, sono disponibili i seguenti comandi:

| Nome |Tasto |Descrizione|
|---|---|---|
|Spostarsi alla colonna precedente |control+alt+freccia sinistra |Sposta il cursore di sistema alla colonna precedente della riga|
|Spostarsi alla colonna successiva |control+alt+freccia destra |Sposta il cursore di sistema alla colonna successiva della riga|
|Spostarsi alla riga precedente |control+alt+Freccia Su |Sposta il cursore di sistema alla riga precedente (Rimanendo nella stessa colonna)|
|Spostarsi alla riga successiva |control+alt+Freccia Giù |Sposta il cursore di sistema alla riga successiva (Rimanendo nella stessa colonna)|
|Spostarsi alla prima colonna |control+alt+inizio |Sposta il cursore di sistema sulla prima colonna (rimanendo nella stessa riga)|
|Spostarsi all'ultima colonna |control+alt+fine |Sposta il cursore di sistema sull'ultima colonna (rimanendo nella stessa riga)|
|Spostarsi alla prima riga |control+alt+PaginaSu |Sposta il cursore di sistema alla prima riga (rimanendo nella stessa colonna)|
|Spostarsi all'ultima riga |control+alt+PaginaGiù |Sposta il cursore di sistema all'ultima riga (rimanendo nella stessa colonna)|
|Dire tutto per colonna |`NVDA+control+alt+frecciagiù` |Legge la colonna verticalmente dalla cella corrente verso il basso fino all'ultima cella della colonna.|
|Dire tutto per riga |`NVDA+control+alt+frecciaDestra` |Legge la riga orizzontalmente dalla cella corrente verso destra fino all'ultima cella della riga.|
|Legge colonna intera |`NVDA+control+alt+frecciaSu` |Legge la colonna corrente verticalmente dall'alto verso il basso senza spostare il cursore di sistema.|
|Legge riga intera |`NVDA+control+alt+frecciaSinistra` |Legge la riga corrente orizzontalmente da sinistra a destra senza spostare il cursore di sistema.|

<!-- KC:endInclude -->

### Navigazione ad oggetti {#ObjectNavigation}

Il più delle volte, l'utente interagisce con l'applicazione utilizzando comandi che spostano direttamente il [focus](#SystemFocus) e il [cursore](#SystemCaret).
Vi sono però alcune circostanze nelle quali può essere utile esaminare l'applicazione corrente o il sistema operativo senza però spostare il focus o il cursore.
Inoltre potrebbe essere necessario lavorare con [oggetti](#Objects) che non possono essere normalmente raggiunti utilizzando la tastiera.
In questi casi, si può utilizzare la navigazione ad oggetti.

Essa permette di ottenere informazioni e spostarsi tra singoli [oggetti](#Objects).
Quando ci si sposta su un oggetto, NVDA lo annuncerà allo stesso modo come avviene con il focus di sistema.
Se invece si desidera esplorare il testo così come appare sullo schermo, è possibile utilizzare la [navigazione in linea](#ScreenReview).

Onde evitare di doversi muovere indietro ed avanti tra ogni singolo oggetto del sistema, gli oggetti sono raggruppati in maniera gerarchica.
Questo significa che alcuni oggetti contengono altri oggetti e che bisogna spostarvisi all'interno per ottenerne le informazioni.
Per esempio, come sappiamo un elenco contiene vari elementi, per cui bisognerà spostarsi all'interno dell'elenco per ottenere accesso ai suoi elementi.
Se ci si è portati su un elemento di un elenco, i comandi per andare all'oggetto successivo o precedente faranno in modo che ci si sposti all'elemento successivo o precedente dell'elenco.
Se invece ci si sposta all’oggetto che contiene l’elemento di un elenco, si torna nell’elenco stesso.
Ci si potrà poi spostare prima o dopo l’elenco per raggiungere altri oggetti.
Allo stesso modo, se si incontra una barra degli strumenti, bisogna entrare all'interno di essa per accedere ai controlli che la compongono.

Tuttavia, se si desidera spostarsi avanti e indietro tra i vari oggetti del sistema, è sempre possibile andare all'oggetto successivo/precedente servendosi dei comandi messi a disposizione dalla modalità in linea, che presenterà gli oggetti senza alcun tipo di gerarchia.
Ad esempio, se ci si sposta sull'oggetto successivo in modalità in linea e l'oggetto corrente contiene altri oggetti, NVDA si sposterà automaticamente sul primo oggetto figlio.
In alternativa, se l'oggetto corrente non contiene alcun oggetto, NVDA passerà all'oggetto successivo allo stesso livello della gerarchia.
Nel caso in cui non esista un oggetto successivo, NVDA cercherà di trovare altri oggetti seguendo la gerarchia fino a quando non ci saranno più oggetti verso cui spostarsi.
Le stesse regole si applicano per la navigazione all'indietro nella gerarchia.

L'oggetto che attualmente viene esplorato è quello su cui si trova il navigatore ad oggetti.
Una volta che viene raggiunto un oggetto, è possibile esplorarlo utilizzando i [comandi di esplorazione testo](#ReviewingText) in [modalità navigazione ad oggetti](#ObjectReview).
Quando [l'evidenziatore del focus](#VisionFocusHighlight) è attivato, viene evidenziata sullo schermo la posizione corrente del navigatore ad oggetti.
Da impostazioni predefinite, il navigatore ad oggetti si sposta in concomitanza con il focus di sistema, tuttavia questo comportamento può essere modificato, attivando o disattivando la relativa opzione.

Nota: le opzioni braille inerenti l'inseguimento del focus e la navigazione ad oggetti possono essere configurate tramite le funzioni di [Inseguimento Braille](#BrailleTether).

Per navigare ad oggetti, utilizzare i tasti seguenti:

<!-- KC:beginInclude -->

| Nome |layout Desktop |layout Laptop |Tocco |Descrizione|
|---|---|---|---|---|
|Legge l'oggetto corrente |NVDA+5 del tastierino numerico |NVDA+shift+o |Nessuno |Annuncia l'oggetto corrente. Premendolo due volte ne fa lo spelling, mentre premendolo tre volte copia il nome dell'oggetto ed il suo valore negli appunti|
|Spostarsi all'oggetto contenitore |NVDA+8 del tastierino numerico |NVDA+Shift+freccia su |Scorrimento in alto (modo oggetti) |ci si sposta all'oggetto che contiene l'oggetto corrente|
|Spostarsi all'oggetto precedente |NVDA+4 del tastierino numerico |NVDA+shift+freccia sinistra |nessuno |ci si Sposta all'oggetto precedente rispetto a quello attuale, sullo stesso livello|
|Spostarsi all'oggetto precedente in modalità lineare |NVDA+9 del tastierino numerico |NVDA+shift+à |scorrimento a sinistra (modo oggetti) |Ci si sposta all'oggetto precedente in una modalità lineare che non tiene conto della gerarchia|
|Spostarsi all'oggetto successivo |NVDA+6 del tastierino numerico |nessuno |NVDA+shift+freccia destra |ci si Sposta all'oggetto successivo rispetto a quello attuale, sullo stesso livello)|
|Spostarsi all'oggetto successivo in modalità lineare |NVDA+3 del tastierino numerico |NVDA+shift+ù |scorrimento a destra (modo oggetti) |Ci si sposta all'oggetto successivo in una modalità lineare che non tiene conto della gerarchia|
|Spostarsi al primo oggetto contenuto |NVDA+2 del tastierino numerico |NVDA+shift+freccia giù |Scorrimento in basso (modo oggetti) |Ci si sposta al primo oggetto contenuto nell'oggetto attuale|
|Spostarsi all'oggetto focalizzato |NVDA+Meno del tastierino numerico |NVDA+Backspace |Nessuno |Sposta il navigatore ad oggetti sull'oggetto che attualmente ha il focus di sistema, e porta anche il cursore di controllo in quella posizione, se il cursore di sistema è visualizzato|
|Attivare l'oggetto corrente |NVDA+Invio del tastierino numerico |NVDA+Invio |Doppio tap |Attiva l'oggetto corrente (l'equivalente di cliccare col mouse o premere la barra spazio in presenza del focus)|
|Spostare il focus o il cursore di sistema sull'oggetto corrente |NVDA+Shift+meno del tastierino numerico |NVDA+Shift+Backspace |Nessuno |Sposta il focus di sistema alla posizione del navigatore ad oggetti se possibile, mentre se premuto due volte sposta il cursore di sistema alla posizione del cursore di controllo|
|Legge posizione cursore di controllo |NVDA+shift+Canc tastierino numerico |NVDA+shift+canc |none |Fornisce informazioni inerenti il testo o l'oggetto su cui è situato il cursore di controllo. Ad esempio, ciò potrebbe includere la percentuale in un documento, la distanza dal bordo della pagina o la posizione esatta dello schermo. Premendo due volte si possono ottenere ulteriori dettagli.|
|Sposta il cursore di controllo sulla barra di stato |nessuno |nessuno |nessuno |Legge il contenuto della barra di stato, se individuata. Inoltre sposta il navigatore ad oggetti su quella posizione.|

<!-- KC:endInclude -->

Nota, Per utilizzare il tastierino numerico, il tasto NumLock deve essere impostato su spento.

### Controllare il testo {#ReviewingText}

NVDA consente di leggere il contenuto dello [schermo/navigazione in linea](#ScreenReview), del [documento corrente](#DocumentReview) o dell'[oggetto](#ObjectReview) per carattere, parola o riga.
Questo risulta utile principalmente nel prompt dei comandi di Windows o in tutte quelle situazioni dove il [cursore di sistema](#SystemCaret) non esiste o ha funzioni limitate.
Ad esempio, può venir buono nel leggere il contenuto di lunghi testi in una finestra di dialogo.

Quando si sposta il cursore di controllo, il cursore di sistema non lo segue, cosicché sarà possibile esplorare il testo senza perdere la propria posizione.
Comunque, da impostazioni predefinite, quando il cursore di sistema si sposta, il cursore di controllo lo segue. 
Tale impostazione può essere modificata attivandola o disattivandola.

Nota: è possibile gestire il modo in cui il display braille si aggancia al cursore di controllo attraverso le opzioni [Inseguimento Braille](#BrailleTether).

Sono disponibili i seguenti tasti caldi per esplorare il testo:
<!-- KC:beginInclude -->

| Nome |layout Desktop |layout Laptop |Tocco |Descrizione|
|---|---|---|---|---|
|Spostarsi alla prima riga |shift+7 del tastierino numerico |NVDA+control+home |Nessuno |Sposta il cursore di controllo alla prima riga del testo|
|Spostarsi alla riga precedente, modalità esplorazione |7 del tastierino numerico |NVDA+freccia su |Scorrimento in alto (modo testo) |Sposta il cursore di controllo alla riga di testo precedente|
|Legge la riga corrente, modalità esplorazione |8 del tastierino numerico |NVDA+shift+. |Nessuno |Annuncia la riga di testo sulla quale è posizionato il cursore di controllo. Se premuto due volte ne fa lo spelling. Premuto tre volte effettua lo spelling con la descrizione dei caratteri|
|Spostarsi alla riga successiva, modalità esplorazione |9 del tastierino numerico |NVDA+freccia giù |Scorrimento in basso (modo testo) |Sposta il cursore di controllo alla riga di testo successiva|
|Spostarsi all'ultima riga, modalità esplorazione |shift+9 del tastierino numerico |NVDA+control+fine |Nessuno |Sposta il cursore di controllo all'ultima riga del testo|
|Spostarsi alla parola precedente, modalità esplorazione |4 del tastierino numerico |NVDA+control+freccia sinistra |Scorrimento a sinistra con due dita (modo testo) |Sposta il cursore di controllo alla parola precedente nel testo|
|Legge la parola corrente, modalità esplorazione |5 del tastierino numerico |NVDA+control+. |Nessuno |Annuncia la parola del testo sulla quale è posizionato il cursore di controllo. Se premuto due volte ne fa lo spelling. Premuto tre volte effettua lo spelling con la descrizione dei caratteri|
|Spostarsi alla parola successiva, modalità esplorazione |6 del tastierino numerico |NVDA+control+freccia destra |Scorrimento a destra con due dita (modo testo) |Sposta il cursore di controllo alla parola successiva nel testo|
|Spostarsi all'inizio della riga, modalità esplorazione |shift+1 del tastierino numerico |NVDA+inizio |Nessuno |Sposta il cursore di controllo all'inizio della riga|
|Spostarsi al carattere precedente, modalità esplorazione |1 del tastierino numerico |NVDA+freccia sinistra |Scorrimento a sinistra (modo testo) |Sposta il cursore di controllo al carattere precedente nella riga corrente di testo|
|Legge il carattere corrente, modalità esplorazione |2 del tastierino numerico |NVDA+. |Nessuno |Annuncia il carattere del testo sul quale è posizionato il cursore di controllo. Se premuto due volte effettua lo spelling mediante la sua descrizione. Se premuto tre volte fornisce il valore numerico del carattere in decimale e esadecimale.|
|Spostarsi al carattere successivo, modalità esplorazione |3 del tastierino numerico |NVDA+freccia destra |Scorrimento a destra (modo testo) |Sposta il cursore di controllo al carattere di testo successivo nella riga corrente|
|Spostarsi alla fine della riga, modalità esplorazione |shift+3 del tastierino numerico |NVDA+fine |Nessuno |Sposta il cursore di controllo alla fine della riga di testo corrente|
|Spostarsi alla pagina precedente, modalità esplorazione |`NVDA+paginaSu` |`NVDA+maiusc+paginaSu` |nessuno |Sposta il cursore di controllo alla pagina precedente contenente testo se supportato dall'applicazione|
|Spostarsi alla pagina successiva, modalità esplorazione |`NVDA+paginaGiù` |`NVDA+maiusc+paginaGiù` |nessuno |Sposta il cursore di controllo alla pagina successiva contenente testo se supportato dall'applicazione|
|Dire tutto, modalità esplorazione |Più del tastierino numerico |NVDA+shift+a |Scorrimento in basso con tre dita (modo testo) |Legge il testo dalla posizione attuale del cursore di controllo, spostando tale cursore man mano che la lettura continua|
|Selezionare e poi copiare dalla posizione del cursore di controllo |NVDA+f9 |NVDA+f9 |Nessuno |Dà inizio al processo di selezione e copia a partire dalla posizione del cursore di controllo. Si noti che NVDA non effettuerà alcuna operazione fino a quando non verrà specificato il punto di fine|
|Selezionare e copiare fino al cursore di controllo |NVDA+f10 |NVDA+f10 |Nessuno |Una singola pressione seleziona il testo dalla posizione iniziale impostata in precedenza fino alla posizione attuale del cursore di controllo, incluso il carattere in cui si trova. Se possibile, il cursore di sistema si sposterà al testo selezionato. Una seconda pressione copierà il testo negli appunti di Windows|
|Spostare il cursore di controllo al marcatore iniziale per la copia |NVDA+shift+f9 |NVDA+shift+f9 |nessuno |Sposta il cursore di controllo alla posizione precedentemente impostata come marcatore iniziale per la copia|
|Annuncia formattazione testo |NVDA+SHIFT+f |NVDA+shift+f |nessuno |Legge la formattazione del testo alla posizione del cursore di controllo. Una doppia pressione visualizzerà le informazioni in modalità navigazione|
|Annuncia sostituzione simbolo corrente |Nessuno |Nessuno |nessuno |Legge il simbolo situato alla posizione del cursore di controllo. Una doppia pressione visualizza il simbolo accompagnato dal testo ad esso dedicato in modalità navigazione.|

<!-- KC:endInclude -->

Si noti che per un corretto funzionamento il tasto Numlock del tastierino numerico deve essere impostato su spento.

Per aiutare l'utente a ricordare queste combinazioni di tasti, si tenga presente che i comandi di base di controllo del testo sono organizzati in una griglia di tre per tre, dove dall'alto verso il basso abbiamo righe, parole e caratteri, mentre da sinistra a destra abbiamo precedente, attuale e successivo.
Il layout può essere descritto come segue:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|riga precedente |riga corrente |riga successiva|
|parola precedente |parola corrente |parola successiva|
|carattere precedente |carattere corrente |carattere successivo|

### Le Modalità di esplorazione {#ReviewModes}

I [comandi di navigazione di NVDA](#ReviewingText) permettono di esplorare il contenuto all'interno di un oggetto, del documento corrente o dello schermo, a seconda della modalità di esplorazione selezionata.

Si possono utilizzare i comandi seguenti per passare da una modalità all'altra:
<!-- KC:beginInclude -->

| Nome |Layout Desktop |Layout Laptop |Tocco |Descrizione|
|---|---|---|---|---|
|Passa alla modalità di esplorazione successiva |NVDA+7 del tastierino numerico |NVDA+pagina su |Scorrimento in alto con due dita |Passa alla modalità di esplorazione successiva.|
|Passa alla modalità di esplorazione precedente |NVDA+1 del tastierino numerico |NVDA+pagina giù |Scorrimento in basso con due dita |Passa alla modalità di esplorazione precedente.|

<!-- KC:endInclude -->

#### Navigazione ad oggetti {#ObjectReview}

Quando ci si trova in modalità navigazione ad oggetti, è possibile esplorare il contenuto del [navigatore ad oggetti](#ObjectNavigation).
Per oggetti come campi editazione o altri controlli di base di un documento, il contenuto corrisponde in genere al testo stesso.
Per altri oggetti, può corrispondere al loro nome o al valore.

#### Esplorazione documento {#DocumentReview}

Quando il [navigatore ad oggetti](#ObjectNavigation) si trova all'interno di un documento in modalità navigazione (ad esempio pagine web) o un altro documento complesso contenente numerosi oggetti (come documenti Lotus Symphony), è possibile passare alla modalità di esplorazione documento.
La modalità di esplorazione documento consente di navigare all'interno del testo del documento.

Quando si passa dalla modalità navigazione ad oggetti all'esplorazione documento, il cursore di controllo viene posizionato all'interno del documento, esattamente dove si trova il nnavigatore ad oggetti.
Quando ci si sposta all'interno del documento con i comandi di esplorazione, la posizione del navigatore ad oggetti viene automaticamente aggiornata in concomitanza con l'oggetto individuato dal cursore di controllo.

Si noti che NVDA passerà automaticamente dalla navigazione ad oggetti all'esplorazione documento quando ci si sposta in modalità navigazione.

#### Esplorazione schermo (modalità in linea) {#ScreenReview}

La modalità di navigazione in linea, o esplorazione schermo, permette di intercettare qualsiasi testo visibile a schermo all'interno dell'applicazione corrente.
è una funzione molto simile alla navigazione col mouse o con cursori speciali presente in altri screen reader, ad esempio cursore Jaws, cursore WE, etc.

Quando si passa alla modalità in linea, il cursore di controllo viene posto alla posizione del [navigatore ad oggetti](#ObjectNavigation).
Se ci si sposta sullo schermo con il cursore di controllo, la posizione del navigatore ad oggetti verrà aggiornata di conseguenza.

Si noti che in alcune applicazioni più recenti, NVDA potrebbe non intercettare tutto o parte del testo messo a disposizione da tali programmi, a causa delle nuove tecnologie usate per disegnare i caratteri, attualmente impossibili da gestire.

### Esplorare con il mouse {#NavigatingWithTheMouse}

Quando si sposta il mouse, NVDA di default leggerà sempre il testo che si trova alla posizione del mouse stesso, man mano che esso viene spostato. 
Laddove supportato, NVDA leggerà il paragrafo contenente il testo, sebbene alcuni controlli saranno disponibili esclusivamente con la lettura riga per riga.

NVDA può anche essere configurato in modo tale da leggere il tipo di controllo o l'[oggetto](#Objects) sul quale è posizionato il mouse (ad esempio elenchi, bottoni, etc).
Ciò può risultare utile ad utenti totalmente privi di vista, laddove le informazioni fornite dal solo testo non sono sufficientemente chiare.

NVDA fornisce agli utenti una metodologia per comprendere la posizione del puntatore in relazione alle dimensioni dello schermo, emettendo dei segnali acustici che descrivono le coordinate del mouse.
Più il mouse si troverà in alto sullo schermo, più acuto sarà il segnale acustico emesso. 
Allo stesso modo, più a destra o sinistra si troverà il puntatore, più verso destra o verso sinistra si sposterà il suono nelle casse, presumendo naturalmente che l'utente si trovi difronte agli altoparlanti in posizione centrale.

Queste caratteristiche aggiuntive riguardanti il mouse non sono attivate di Default.
Se le si vuole provare sarà sufficiente configurarle dalla categoria [impostazioni mouse](#MouseSettings), raggiungibile dalla finestra di dialogo delle [Impostazioni di NVDA](#NVDASettings).

Sebbene un mouse o un trackpad risultino la maniera migliore per esplorare lo schermo in tale modalità, NVDA mette a disposizione qualche comando relativo al mouse:
<!-- KC:beginInclude -->

| Nome |tasto Desktop |tasto Laptop |tocco |Descrizione|
|---|---|---|---|---|
|Click tasto sinistro del mouse |Barra del tastierino numerico |NVDA+è |nessuno |Effettua un click con il tasto sinistro del mouse. Per operare un doppio click premere il tasto due volte in rapida successione|
|Blocca tasto sinistro del mouse |Shift+Barra del tastierino numerico |NVDA+control+è |nessuno |Blocca il tasto sinistro del mouse. Premere di nuovo tale combinazione per rilasciarlo. Per trascinare il mouse, premere la sequenza di tasti per bloccare il tasto sinistro e quindi spostare il mouse o fisicamente oppure con gli appositi comandi relativi al mouse|
|Click tasto destro del mouse |Asterisco del tastierino numerico |NVDA++ |Tap lungo |Effettua un click con il bottone destro del mouse, utilizzato per lo più per aprire i menu di contesto alla posizione del mouse|
|Blocca tasto destro del mouse |Shift+Asterisco del tastierino numerico |NVDA+control++ |nessuno |Blocca il tasto destro del mouse. Premere di nuovo tale combinazione per rilasciarlo. Per trascinare il mouse, premere la sequenza di tasti per bloccare il tasto destro e quindi spostare il mouse o fisicamente oppure con gli appositi comandi relativi al mouse|
|Spostare il mouse alla posizione del navigatore ad oggetti |NVDA+Barra del tastierino numerico |NVDA+Shift+m |nessuno |Sposta il mouse alla posizione del navigatore ad oggetti e quindi del cursore di controllo|
|Spostare il navigatore ad oggetti sul mouse |NVDA+Asterisco del tastierino numerico |NVDA+Shift+n |nessuno |Sposta il navigatore ad oggetti sull'oggetto situato nella posizione del mouse|

<!-- KC:endInclude -->

## Modalità navigazione {#BrowseMode}

NVDA si serve della modalità navigazione per presentare all'utente documenti complessi di sola lettura, come ad esempio le pagine web.
Tale modalità funziona nelle applicazioni seguenti:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Messaggi HTML in Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* I libri supportati in Amazon Kindle for PC

Inoltre, la modalità navigazione risulta disponibile anche per la gestione dei documenti in Microsoft Word.

Nella modalità navigazione, il contenuto del documento è reso disponibile tramite una rappresentazione lineare, che può essere esplorata con i comuni tasti dedicati al cursore, come se si trattasse di un normale documento.
Tutte le combinazioni di tasti di NVDA dedicate al [cursore di sistema](#SystemCaret) funzioneranno regolarmente, ad esempio dire tutto, annuncia formattazione, comandi per esplorare le tabelle, etc.
Quando [l'evidenziatore del focus](#VisionFocusHighlight) è attivato, viene evidenziata sullo schermo anche la posizione corrente di questo particolare cursore.
Verranno annunciate anche le informazioni inerenti il tipo di controllo su cui ci si trova, ad esempio link, intestazioni, etc.

Talvolta, risulterà necessario anche interagire direttamente con i controlli presenti in questi documenti.
Ad esempio, si può aver bisogno di questo nei campi editazione o negli elenchi in modo che sia possibile digitare i caratteri ed utilizzare i tasti cursore per lavorare con i controlli.
Questo viene effettuato attivando la modalità focus, dove tutti i tasti verranno passati direttamente ai controlli.
Se ci si trova nella modalità navigazione e si preme tab o si fa click su un controllo, NVDA attiverà automaticamente la modalità Focus se tale controllo lo richiede.
Da notare che la pressione del tasto invio o spazio in questo tipo di controlli attiverà comunque la modalità focus.
Se NVDA è passato automaticamente alla modalità Focus, la pressione del tasto tab o il click su un oggetto che non richiede questa modalità (come un link o una parte di testo) provocherà la riattivazione della modalità navigazione.
Anche la pressione del tasto Esc farà in modo che NVDA attivi la modalità navigazione, nel caso l'attivazione della modalità focus sia avvenuta automaticamente.
è possibile anche passare tra le due modalità in modo manuale. Tuttavia se si imposta la modalità focus manualmente, NVDA non ritornerà più in maniera automatica alla modalità navigazione, fino a quando l'utente non deciderà diversamente.

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Commuta modalità focus/navigazione |NVDA+Spazio |Commuta tra le modalità focus e navigazione|
|Abbandona modalità focus |escape |Ritorna alla modalità navigazione se la modalità focus era stata impostata precedentemente in maniera automatica|
|Aggiorna documento in modalità navigazione |NVDA+f5 |Ricarica il contenuto del documento attuale (utile nel caso certi contenuti della pagina non sembrano essere presenti. Funzione non disponibile in Microsoft Word e Outlook)|
|Trova |NVDA+Control+f |Apre una finestra di dialogo che consente di cercare del testo all'interno del documento. Fare riferimento alla sezione [Cercare del testo](#SearchingForText) per ulteriori informazioni.|
|Trova successivo |NVDA+f3 |Trova la stringa successiva di testo precedentemente cercata nel documento|
|Trova precedente |NVDA+Shift+f3 |Trova la stringa precedente di testo nel documento cercata con control+NVDA+f|

<!-- KC:endInclude -->

### Navigare con le lettere {#SingleLetterNavigation}

Per avere una maggiore velocità nell'esplorazione, NVDA fornisce alcuni tasti per muoversi fra i vari campi quando si utilizza la modalità navigazione.
Si noti che non tutti questi comandi sono supportati in ogni tipo di documento.

<!-- KC:beginInclude -->
I seguenti tasti premuti da soli portano al campo successivo, tenendo premuto Maiusc invece portano al campo precedente.

* h: intestazione
* l: elenco
* i: elemento di elenco
* t: tabella
* k: link
* n: Testo senza link
* f: campo form
* u: link non visitato
* v: link visitato
* e: campo editazione
* b: bottone
* x: casella di controllo
* c: casella combinata
* r: pulsante radio
* q: blocco tra virgolette
* s: separatore
* m: frame
* g: grafico
* d: Punto di riferimento
* o: oggetto incorporato (audio e video player, applicazione, finestra di dialogo, etc.)
* numeri da 1 a 6: intestazioni da 1 a 6
* a: annotazioni (commenti, revisioni degli autori, etc.)
* `p`: paragrafo di testo
* w: errori di ortografia

Per spostarsi all'inizio e alla fine degli elementi contenuti in elenchi e tabelle,:

| Nome |Tasto |Descrizione|
|---|---|---|
|Spostarsi all'inizio del contenitore |punto e virgola |Si sposta al primo elemento presente negli elenchi o nelle tabelle, e vi posiziona il cursore|
|Spostarsi alla fine del contenitore |virgola |Si sposta all'ultimo elemento presente negli elenchi o nelle tabelle, e vi posiziona il cursore|

<!-- KC:endInclude -->

Alcune applicazioni web come Gmail, Twitter e Facebook utilizzano lettere singole come tasti di scelta rapida.
Se si desidera utilizzare questi tasti e allo stesso tempo essere in grado di muoversi con le frecce in modalità navigazione, è possibile disabilitare temporaneamente la modalità di navigazione a lettere singole di NVDA.
<!-- KC:beginInclude -->
Per attivare o disattivare la navigazione a lettere singole per il documento corrente, premere NVDA + shift + spazio.
<!-- KC:endInclude -->

#### Comandi di navigazione tra i paragrafi di testo {#TextNavigationCommand}

è possibile saltare al paragrafo di testo successivo o precedente premendo `p` o `shift+p`.
I paragrafi di testo sono definiti da un gruppo di frasi scritte in forma completa.
Questo può essere utile per trovare l'inizio di un contenuto leggibile su varie pagine web, come ad esempio:

* Siti web di notizie
* Forum
* Post di blog

Questi comandi possono essere utili anche per saltare alcuni tipi di elementi superflui, come ad esempio:

* Annunci
* Menu
* Intestazioni

Si tenga presente, tuttavia, che sebbene NVDA faccia del suo meglio per identificare i paragrafi di testo, l'algoritmo non è perfetto e a volte può commettere errori.
Inoltre, i comandi di navigazione tra i paragrafi di testo sono diversi dai comandi di navigazione tra paragrafi `control+freccia giù/freccia su`.
Infatti, I primi saltano da un paragrafo di testo all'altro, mentre i secondi portano il cursore al paragrafo successivo o precedente, indipendentemente dal fatto che in esso sia contenuto del testo o meno.

#### Altri comandi di navigazione {#OtherNavigationCommands}

Oltre ai comandi di navigazione rapida sopra elencati, NVDA dispone di comandi a cui non sono assegnati tasti predefiniti.
Per utilizzare questi comandi, è necessario prima assegnare loro dei gesti utilizzando la [finestra di dialogo Gesti e tasti di immissione](#InputGestures).
Ecco un elenco dei comandi disponibili:

* Articolo
* Figura
* Gruppo
* Scheda
* Voce di menu
* Interruttore
* Barra di avanzamento
* Formula matematica
* Paragrafo allineato verticalmente
* Testo con stesso stile
* Testo con stile diverso

Si tenga presente che esistono due comandi per ogni tipo di elemento, per andare avanti nel documento e indietro nel documento, perciò bisogna assegnare dei gesti a entrambi i comandi per poter navigare velocemente in entrambe le direzioni.
Ad esempio, se si vuole utilizzare i tasti `y` / `Maiusc+y` per navigare rapidamente tra le schede, procedere come segue:

1. Aprire la finestra di dialogo gesti e tasti di immissione dalla modalità navigazione.
1. Cercare l'elemento "Vai alla scheda successiva" nella sezione modalità navigazione.
1. Assegnare il tasto `y` al gesto.
1. Cercare l'elemento "Vai alla scheda precedente.
1. Assegnare `Maiusc+y` al gesto.

### Elenco elementi {#ElementsList}

La lista degli elementi consente l'accesso ad un elenco di vari tipi di elementi presenti sul documento, a seconda dell'applicazione in uso.
Per esempio, in una pagina web potremmo trovare un elenco dei link, delle intestazioni, campi editazione, pulsanti o punti di riferimento presenti nel documento.
I pulsanti radio permettono di ciclare tra questi tipi di informazioni.
è presente anche un campo editazione, utile a filtrare tale lista per permettere una ricerca più rapida.
Una volta selezionato l'elemento, si possono utilizzare i bottoni che si trovano nella finestra di dialogo, per spostarvisi o attivarlo.
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Elenco elementi modalità navigazione |NVDA+f7 |Elenca vari tipi di elementi presenti nel documento corrente|

<!-- KC:endInclude -->

### Cercare del testo {#SearchingForText}

Questa finestra di dialogo consente di cercare del testo all'interno del documento corrente.
Comparirà una casella di testo con la dicitura "digitare il testo da cercare".
Esiste anche una casella di controllo chiamata "distingui tra maiuscole e minuscole", che consente di stabilire se la ricerca debba tener conto o meno di questa caratteristica.
Perciò, con la casella selezionata, cercare nvaccess sarà diverso che cercare NvAccess. 
Utilizzare i seguenti tasti per eseguire ricerche:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Trova testo |NVDA+control+f |Apre la finestra di ricerca|
|Trova successivo |NVDA+f3 |cerca la prossima occorrenza del termine appena digitato|
|Trova precedente |NVDA+shift+f3 |cerca l'occorrenza precedente del termine appena digitato|

<!-- KC:endInclude -->

### Oggetti incorporati {#ImbeddedObjects}

Le pagine web possono essere strutturate con diverse tecnologie al proprio interno, ad esempio contenuti di tipo Sun Java e html5, applicazioni o finestre di dialogo. 
Quando NVDA incontra tali elementi in modalità navigazione, lo screen reader li annuncerà rispettivamente come oggetti, applicazioni o finestre di dialogo.
è possibile spostarsi rapidamente tra gli oggetti premendo i comandi di navigazione veloce o oppure Shift-o.
Sarà possibile interagire con tali elementi premendo il tasto Invio
Se risulterà accessibile, premere il tasto tab o comunque muoversi all'interno di esso come se si trattasse di una normale applicazione. 
è stato previsto un tasto caldo per tornare alla pagina originale che contiene l'oggetto:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Ritornare alla modalità navigazione |NVDA+control+spazio |Sposta il focus dall'oggetto incorporato alla modalità navigazione|

<!-- KC:endInclude -->

### Modalità di selezione nativa {#NativeSelectionMode}

Per impostazione predefinita, quando si seleziona il testo con i tasti `shift+freccia` in modalità Navigazione, la selezione viene effettuata solo all'interno della rappresentazione virtuale del documento di NVDA e non all'interno dell'applicazione stessa.
Ciò significa che la selezione non è visibile sullo schermo e la copia del testo con `control+c` copierà solo la rappresentazione in testo semplice del contenuto di NVDA. Significa che non sarà copiata la formattazione del testo, o quella delle tabelle, o gli attributi che compongono un link , ma soltanto il testo semplice.
Tuttavia, NVDA dispone di una modalità di selezione nativa che può essere attivata in documenti particolari in modalità navigazione (finora solo Mozilla Firefox) che fa sì che la selezione nativa del documento segua la selezione della modalità navigazione di NVDA.

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Attiva e disattiva la modalità di selezione nativa |`NVDA+shift+f10` |Attiva e disattiva la modalità di selezione nativa|

<!-- KC:endInclude -->

Quando la modalità di selezione nativa è attivata, la copia della selezione con `control+c` utilizzerà anche la funzionalità di copia propria dell'applicazione, il che significa che tutto il contenuto compresa la formattazione verrà copiato negli appunti, anziché solo il testo semplice.
Ciò significa che se incolleremo il contenuto in programmi come Word o Excel, riusciremo ad ottenere non soltanto il testo semplice,ma anche la formattazione di tabelle o collegamenti..
Si tenga presente, tuttavia, che nella modalità di selezione nativa, alcune etichette accessibili o altre informazioni generate da NVDA nella modalità di navigazione non verranno incluse.
Inoltre, anche se l'applicazione farà del suo meglio per far corrispondere la selezione nativa alla selezione della modalità di navigazione di NVDA, potrebbe non essere sempre completamente accurata.
Tuttavia, per scenari in cui si desidera copiare un'intera tabella o un paragrafo ricco di contenuti e formattazione, questa funzionalità dovrebbe rivelarsi utile.

## Lettura della matematica {#ReadingMath}

NVDA è in grado di leggere ed interagire con la matematica sia sul web che in altre applicazioni, consentendo di fornire accesso alle informazioni tramite braille e sintesi vocale..
Affinché ciò sia possibile, è necessario installare un add-on relativo alla matematica per NVDA.
Sono disponibili diversi add-on nello store di NVDA che forniscono supporto per la matematica, come l'add-on[MathCAT NVDA](https://nsoiffer.github.io/MathCAT/) e [Access8Math https://github](.com/tsengwoody/Access8Math).
Fare riferimento alla [sezione Add-on Store](#AddonsManager) per sapere come sfogliare e installare i componenti aggiuntivi in NVDA.
NVDA può anche utilizzare il vecchio software [MathPlayer](https://info.wiris.com/mathplayer-info) di Wiris se presente sul sistema, sebbene questo programma non sia più sviluppato.

### Formati di matematica supportati {#SupportedMathContent}

Dopo aver installato un add-on appropriato allo scopo, NVDA sarà in grado di supportare la matematica nei seguenti formati:

* MathML in Mozilla Firefox, Microsoft Internet Explorer e Google Chrome.
* Le equazioni generate tramite lo strumento apposito di Microsoft Word 365 con UI automation attiva:
NVDA è in grado di leggere e interagire con le equazioni matematiche in Microsoft Word 365/2016 build 14326 e versioni successive.
Si noti tuttavia che qualsiasi equazione creata in precedenza con MathType dovrà essere convertita nel formato Office.
Ciò può essere effettuato selezionandola e scegliendo opzioni equazione - converti in matematica Office, dal menu contestuale.
è bene assicurarsi di disporre dell'ultima versione di MathType prima di farlo.
Microsoft Word ora fornisce anche la navigazione in linea delle formule basata su simboli e supporta l'immissione di matematica utilizzando diverse sintassi, incluso LateX.
Per ulteriori informazioni, si veda [Equazioni in formato Lineare che usano UnicodeMath e LaTeX in Word https://support.microsoft.com/it-it/office/equazioni-in-formato-lineare-che-usano-unicodemath-e-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8#:~:text=Equazioni%20in%20formato%20Lineare%20che%20usano%20UnicodeMath%20e%20LaTeX%20in%20Word,-Word%20per%20Microsoft&text=Per%20inserire%20un'equazione%20usando,usando%20Correzione%20automatica%20simboli%20matematici.]
* Microsoft Powerpoint, e le versioni meno recenti di Microsoft Word: 
NVDA è in grado di leggere e di navigare tra le equazioni Mathtype sia in Powerpoint che in Microsoft Word.
Si noti che MathType dev'essere installato affinché il supporto funzioni correttamente.
è sufficiente anche la versione di prova.
Può essere scaricato dalla [Pagina di presentazione di MathType](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Si noti che questo non è ancora uno standard ufficiale, per cui attualmente non esiste per il pubblico un software disponibile che possa produrre questo contenuto.
* Kindle Reader per PC:
NVDA può leggere e navigare tra i contenuti di tipo matematico in Kindle per PC su libri con matematica accessibile.

Durante la lettura di un documento, NVDA sarà in grado di leggere qualsiasi contenuto di tipo matematico supportato.
Se si utilizza un display braille, verrà visualizzato regolarmente anche in Braille.

### Esplorazione interattiva {#InteractiveNavigation}

Nel caso in cui si stia lavorando con la sintesi vocale, potrebbe essere molto più comodo ascoltare un'espressione riducendola in piccoli segmenti, piuttosto che doversi ascoltare tutto il contenuto in una sola volta.

Se ci si trova in modalità navigazione, sarà sufficiente spostare il cursore di controllo dove inizia la parte matematica e premere semplicemente invio.

Se non ci si trova in modalità navigazione:

1. Spostare il cursore di controllo in un contenuto di tipo matematico.
Da impostazioni predefinite, il cursore di controllo segue il cursore di sistema, sicché sarà sufficiente muoversi col cursore standard alla posizione desiderata.
1. Poi, utilizzare il comando seguente:

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Interagire con matematica |NVDA+alt+m |Inizia l'interazione con contenuto di tipo matematico.|

<!-- KC:endInclude -->

A questo punto, è possibile utilizzare i tasti freccia per esplorare l'espressione.
Ad esempio, ci si potrà spostare attraverso l'espressione con i tasti freccia sinistra e destra, per poi evidenziare una parte dell'espressione, come una frazione utilizzando il tasto freccia verso il basso.

Quando si desidera tornare al documento, è sufficiente premere il tasto Esc.

Per ulteriori informazioni sui comandi disponibili e sulle preferenze per la lettura e la navigazione all'interno dei contenuti matematici, fare riferimento alla documentazione del componente matematico specifico installato.

* [Documentazione MathCAT](https://nsoiffer.github.io/MathCAT/users.html)
* [Documentazione Access8Math](https://github.com/tsengwoody/Access8Math)
* [Documentazione MathPlayer](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

A volte il contenuto matematico può essere visualizzato come un pulsante o altri tipi di elementi che, se attivati, possono visualizzare una finestra di dialogo o ulteriori informazioni relative alla formula.
Per attivare il pulsante o l'elemento contenente la formula, premere ctrl + invio.

### Installazione di MathPlayer {#InstallingMathPlayer}

Sebbene sia generalmente consigliato utilizzare uno dei componenti aggiuntivi più recenti per gestire la matematica in NVDA, in alcuni scenari particolari MathPlayer potrebbe comunque risultare una scelta più adatta.
Per esempio, MathPlayer potrebbe supportare una lingua o un codice Braille che non è ancora presente negli add-on più recenti.
MathPlayer è disponibile gratuitamente dal sito Web Wiris.
[Scarica MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Dopo aver installato MathPlayer, è necessario riavviare NVDA.
Tenere presente che le informazioni su MathPlayer potrebbero indicare che il supporto esiste solo per browser meno recenti come Internet Explorer 8.
Ciò si riferisce solo quando si utilizza MathPlayer per mostrare visivamente il contenuto matematico, gli utenti di NVDA possono ignorare questa informazione.

## Braille {#Braille}

Se si possiede un Display Braille, NVDA sarà in grado di mostrare le informazioni sulla riga braille.
Nel caso inoltre la barra braille sia dotata di tastiera perkins, è anche possibile servirsi della stessa per immettere il testo, sia in modalità standard che contratta (utile in Stati Uniti e Regno Unito).
Un'altra possibilità è quella di visualizzare a schermo il contenuto del display braille servendosi della funzione [Visualizzatore Braille](#BrailleViewer).

Si prega di fare riferimento alla sezione [display braille supportati](#SupportedBrailleDisplays) per ulteriori informazioni.
Inoltre questa sezione contiene informazioni sui modelli di Display Braille che supportano la rilevazione automatica in background da parte dello screen reader.
è possibile modificare i parametri braille andando alla [categoria Braille](#BrailleSettings) della finestra [Impostazioni NVDA](#NVDASettings).

### Tipo di controlli, stato e abbreviazioni per i punti di riferimento {#BrailleAbbreviations}

Per far stare più informazioni possibili su di un display braille, sono state definite le seguenti abbreviazioni per indicare il tipo di controllo e di stato, come pure i punti di riferimento.

| Abbreviazione |tipo di controllo|
|---|---|
|app |applicazione|
|art |articolo|
|bqt |blocco tra virgolette|
|btn |bottone|
|drbtn |Pulsante a discesa|
|spnbtn |Pulsante spin|
|splbtn |Pulsante dividi|
|intbtn |Interruttore|
|didscl |Didascalia|
|cbo |casella combinata|
|chk |casella di controllo|
|dlg |finestra di dialogo|
|doc |documento|
|edt |campo editazione|
|pwdedt |edit password|
|ogg |oggetto|
|enote |Fine nota|
|fnote |nota a piè di pagina|
|fig |figura|
|gra |grafico|
|grp |raggruppamento|
|cN |numero colonna n di una tabella, ad esempio c1, c2.|
|rN |numero riga n di una tabella, ad esempio r1, r2.|
|hN |intestazione di livello n, ad esempio h1, h2.|
|hlp |fumetto d'aiuto|
|lnk |link|
|vlnk |link visitato|
|lst |elenco|
|prf |punto di riferimento|
|mnu |menu|
|mnubar |barra dei menu|
|mnubtn |Pulsante menu|
|mnuitem |Elemento menu|
|Riq |Riquadro|
|prgbar |Barra di avanzamento|
|bsyind |indicatore di occupato|
|rbtn |pulsante radio|
|scrlbar |barra di scorrimento|
|sect |sezione|
|stbar |barra di stato|
|tabctl |Scheda|
|tb |tabella|
|term |terminale|
|tlbar |barra degli strumenti|
|tltip |suggerimento|
|tv |visualizzazione ad albero|
|tvbtn |pulsante visualizzazione ad albero|
|tvitem |elemento visualizzazione ad albero|
|lv N |un elemento in visualizzazione ad albero con livello di gerarchia N|
|wnd |finestra|
|⠤⠤⠤⠤⠤ |separatore|
|mrkd |contenuto contrassegnato|

Sono altresì definiti i seguenti indicatori di stato:

| Abbreviazione |indicatore di stato|
|---|---|
|... |visualizzato quando un oggetto supporta l'autocompletamento|
|⢎⣿⡱ |visualizzato quando un oggetto (ad esempio un interruttore) è premuto|
|⢎⣀⡱ |visualizzato quando un oggetto (ad esempio un interruttore) non è premuto|
|⣏⣀⣹ |visualizzato quando un oggetto (ad esempio una casella di controllo) non è selezionato|
|⣏⣿⣹ |visualizzato quando un oggetto (ad esempio una casella di controllo) è selezionato|
|⣏⣸⣹ |visualizzato quando un oggetto (come una casella di controllo) risulta parzialmente attivato|
|- |visualizzato quando un oggetto (ad esempio un elemento di una visualizzazione ad albero) è riducibile|
|+ |visualizzato quando un oggetto (ad esempio un elemento di una visualizzazione ad albero) è espandibile|
|*** |visualizzato quando si incontra un controllo o un campo di testo protetto|
|clk |visualizzato quando un oggetto è cliccabile|
|cmnt |visualizzato in presenza di un commento per una cella di un foglio di calcolo o un pezzo di testo in un documento|
|frml |visualizzato in presenza di una formula in una cella di un foglio di calcolo|
|invalid |visualizzato quando è stato inserito un valore non valido|
|ldesc |visualizzato quando un oggetto (in genere un grafico) contiene una descrizione|
|mln |visualizzato quando un campo editazione consente l'inserimento di più righe di testo come i campi dei commenti nei siti web|
|req |visualizzato quando un valore è richiesto in un form|
|ro |visualizzato quando un oggetto (ad esempio un campo editazione) è di sola lettura|
|sel |visualizzato quando un oggetto è selezionato|
|nsel |visualizzato quando un oggetto non è selezionato|
|sorted asc |visualizzato quando un oggetto è ordinato in modo ascendente|
|sorted desc |visualizzato quando un oggetto è ordinato in modo discendente|
|submnu |visualizzato quando un oggetto contiene un popup (in genere un sottomenu)|

Infine, sono state definite le seguenti abbreviazioni per i punti di riferimento:

| Abbreviazione |Punto di riferimento|
|---|---|
|bnnr |banner|
|cinf |Informazioni contenuto|
|cmpl |complementare|
|form |form|
|main |principale|
|navi |navigazione|
|srch |ricerca|
|rgn |regione|

### Immissione Braille {#BrailleInput}

NVDA supporta l'immissione di caratteri tramite la tastiera stile perkins presente sui Display Braille.
è possibile selezionare la tabella di traduzione per inserire il testo tramite la casella combinata [immissione braille](#BrailleSettingsInputTable) nella categoria braille della finestra [Impostazioni NVDA](#NVDASettings).Quando viene utilizzato il braille non contratto (ossia quello classico presente in Italia), il testo viene inserito nel momento in cui si digitano i caratteri.

Quando si utilizza il Braille non contratto, il testo viene inserito non appena viene immesso.
Quando invece si usa il braille contratto, il testo viene inserito alla pressione della barra spaziatrice oppure premendo invio alla fine di una parola.
Si noti che il processo di traduzione funziona soltanto sulla parola digitata, non può quindi prendere in considerazione altro testo eventualmente esistente.
Per esempio, se si utilizza un codice braille che prevede il segnanumero e poi un numero, nel caso si prema Backspace sarà necessario ridigitare il segnanumero per inserire altre cifre.

<!-- KC:beginInclude -->
Punto 7 elimina l'ultimo carattere o segno braille.
Punto 8 elabora il braille inserito e aggiunge un invio.
Tasto 7 + tasto 8 elabora il braille inserito, senza l'aggiunta di un invio o di uno spazio..
<!-- KC:endInclude -->

#### Immissione di scorciatoie da tastiera {#BrailleKeyboardShortcuts}

NVDA supporta l'immissione di scorciatoie da tastiera e l'emulazione della pressione dei tasti utilizzando il display braille.
Tale emulazione può avvenire in due modi: assegnando una combinazione braille corrispondente alla pressione dei tasti desiderati, oppure servendosi dei tasti modificatori virtuali.

I tasti comunemente usati, come le frecce o la pressione di Alt per accedere ai menu, possono essere mappati direttamente alle combinazioni di immissione braille.
Il driver di ogni display Braille è già dotato di alcune di queste assegnazioni.
è possibile modificare tali assegnazioni o aggiungere nuove emulazioni di tasti dalla [Finestra tasti e gesti di immissione](#InputGestures).

Sebbene questo approccio risulti utile per tasti singoli o comunque premuti di frequente (ad esempio Tab), si potrebbe non voler assegnare un set univoco di tasti a ciascuna scorciatoia da tastiera.
Per consentire l'emulazione di combinazioni per le quali è necessario tener premuti i tasti modificatori, NVDA fornisce comandi per attivare/disattivare control, alt, shift, windows, eNVDA, oltre ad altri comandi per alcune combinazioni di quei tasti.
Per utilizzare questi interruttori, innanzitutto è necessario attivare il comando (o la sequenza di comandi) per i tasti modificatori che si desidera rimangano premuti.
Quindi, inserire il carattere che fa parte della scorciatoia da tastiera voluta.
Per esempio, per ottenere control+f, usare il comando "attiva/disattiva tasto control" e poi digitare una f,
e per inserire control+alt+t, servirsi o dei comandi "attiva/disattiva tasto control" e "Attiva/disattiva tasto alt", nell'ordine che si preferisce, oppure del comando "Attiva/disattiva tasti control e alt", per poi digitare la t.

Se si attivano o disattivano accidentalmente i tasti modificatori, basterà rieseguire il comando per tornare alla situazione di partenza..

Quando si digita in Braille contratto, l'attivazione/disattivazione dei tasti modificatori farà tradurre l'input proprio come se si avesse premuto i punti 7+8.
Inoltre, la pressione dei tasti emulati non può rispecchiare il Braille digitato prima della pressione del tasto modificatore.
Ciò significa che, per digitare alt+2 con un codice Braille che utilizza un segnanumero, bisogna prima attivare Alt e quindi digitare il segna numero.

## Visione {#Vision}

Nonostante NVDA rimanga uno screen reader per persone non vedenti che si servono della sintesi vocale e/o di un display braille per utilizzare il computer, fornisce anche alcune funzioni che modificano l'aspetto del contenuto dello schermo.
Tale caratteristica viene chiamata servizio di miglioramento visivo.

NVDA fornisce al proprio interno una serie di servizi che andremo ad esaminare a breve.
è possibile aggiungere ulteriori servizi relativi al miglioramento dell'aspetto visivo tramite il [gestore componenti aggiuntivi di NVDA](#AddonsManager).

Le impostazioni di visione possono essere modificate nella [categoria visione](#VisionSettings) della [finestra impostazioni di NVDA](#NVDASettings).

### Evidenziatore del focus {#VisionFocusHighlight}

L'evidenziazione del focus può risultare molto utile nell'individuare velocemente la posizione del [cursore di sistema](#SystemFocus), del [navigatore ad oggetti](#ObjectNavigation) e della [modalità navigazione](#BrowseMode).
Queste posizioni sono evidenziate tramite un contorno rettangolare colorato.

* Il blu viene usato per evidenziare il cursore di sistema e il navigatore ad oggetti quando sono insieme e hanno la medesima posizione (grazie alla funzione [il navigatore ad oggetti segue il cursore di sistema](#ReviewCursorFollowFocus)), cosa che generalmente accade quasi sempre. 
* Il blu tratteggiato viene utilizzato per mostrare solo la posizione dell'oggetto su cui si trova il cursore di sistema.
* Il rosa mostra la posizione del navigatore ad oggetti.
* Il giallo infine serve a visualizzare la posizione del cursore virtuale, ad esempio durante la navigazione di pagine web.

Quando l'evidenziatore focus viene attivato nella [categoria visione](#VisionSettings) della [finestra impostazioni di NVDA](#NVDASettings), è possibile [stabilire se evidenziare o meno il focus, il navigatore ad oggetti o il cursore virtuale della modalità navigazione](#VisionSettingsFocusHighlight)

### Tenda schermo {#VisionScreenCurtain}

Vi sono alcune circostanze in cui un utente non vedente può preferire che il contenuto dello schermo non sia visualizzato.
Inoltre, potrebbe essere difficile garantire che non ci sia qualcuno che stia guardando ciò che si sta facendo.
Per questi motivi, NVDA è fornito di una caratteristica chiamata "tenda schermo" che può essere attivata in modo che lo schermo diventi nero.

è possibile attivare la tenda schermo nella [categoria visione](#VisionSettings) della [Finestra impostazioni](#NVDASettings).

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Attiva o disattiva la tenda schermo |`NVDA+control+escape` |Abilita per rendere lo schermo nero o disabilita per mostrare il contenuto dello schermo. Premuto una volta, la tenda schermo rimane attiva fino al riavvio di NVDA. Premuto due volte, la tenda schermo rimane abilitata finché non la si disabilita.|

<!-- KC:endInclude -->

Quando la tenda schermo è attiva, è possibile che alcune operazioni che si basano su ciò che appare a schermo non possano essere portate a termine, come la funzione di [OCR](#Win10Ocr) o l'acquisizione di uno screenshot. 

A causa di alcuni cambiamenti nelle api dell'ingranditore di Windows, è risultato necessario aggiornare la tenda schermo in modo che potesse funzionare correttamente.
Perciò, è obbligatorio servirsi di NVDA 2021.2 per attivare la tenda schermo con versioni di Windows 10 21H2 (10.0.19044) o successive.
Per sicurezza, sarebbe meglio avere una conferma da una persona vedente che lo schermo sia effettivamente oscurato quando si aggiorna Windows ad una nuova versione.

Si tenga presente che quando è attiva la lente d'ingrandimento di Windows e vengono utilizzati colori invertiti dello schermo, non può essere attivata la tenda schermo.

## OCR: Riconoscimento del contenuto {#ContentRecognition}

Un utente non vedente può trovarsi di fronte a contenuti completamente inaccessibili, in quanto gli autori degli stessi non forniscono allo screen reader le informazioni necessarie affinché quest'ultimo possa gestirle correttamente (esempio, pdf immagine).
NVDA supporta la funzionalità di OCR (riconoscimento ottico dei caratteri) già inclusa in Windows10 e versioni successive per riconoscere il testo contenuto nelle immagini.
Tramite i componenti aggiuntivi sarà anche possibile interfacciarsi con NVDA fornendogli altri metodi di riconoscimento.

Quando ci si serve del comando di riconoscimento OCR, NVDA riconosce il contenuto presente all'interno del [navigatore ad oggetti](#ObjectNavigation).
Per impostazioni predefinite, il navigatore ad oggetti segue il cursore di sistema, o direttamente la modalità navigazione nel caso si stia utilizzando un sito internet o app che ne permettono l'uso(ad esempio Adobe Reader), perciò sarà possibile semplicemente spostare il focus o il cursore dove si desidera.
Ad esempio, se ci si trova in una pagina web e ci si posiziona su un grafico, l'attivazione dell'OCR riconoscerà il testo contenuto in quel grafico.
Tuttavia è anche possibile servirsi della navigazione ad oggetti per riconoscere il contenuto di un'intera finestra, basterà spostarsi sull'oggetto desiderato, in questo caso la finestra dell'app.

Una volta terminato il processo di riconoscimento, basterà utilizzare i tasti freccia per esplorare il documento.
è possibile anche attivare (che nel 90% delle volte significa cliccare) un punto desiderato spostandosi con le frecce e poi premendo il tasto invio o la barra spaziatrice. Questo risulta utile nel caso si voglia raggiungere un pulsante non etichettato, sia esso di un sito web o di un programma.
Premere il tasto Esc per uscire dal documento riconosciuto.

### OCR di Windows {#Win10Ocr}

Windows10 e versioni successive includono al suo interno un sistema di OCR per molte lingue.
NVDA si serve di questa caratteristica per riconoscere il testo contenuto nelle immagini o in applicazioni non accessibili.

è possibile impostare la lingua di riconoscimento dalla [categoria OCR Windows](#Win10OcrSettings) della finestra [Impostazioni NVDA](#NVDASettings).
Si possono installare altre lingue aprendo il menu avvio, scegliendo poi Impostazioni, Ora e Lingua -> Paese e Lingua e quindi aggiungi lingua.

Quando si desidera controllare contenuti in continua evoluzione, ad esempio un video con i sottotitoli, è possibile attivare l'aggiornamento automatico del contenuto riconosciuto.
Ciò può anche essere effettuato nella [Categoria OCR di Windows](#Win10OcrSettings) delle [Impostazioni di NVDA](#NVDASettings) dialog.

La funzione OCR di Windows potrebbe risultare non pienamente compatibile con gli [strumenti di visione](#Vision) o altri componenti che influenzano la visualizzazione a schermo. Sarà necessario disabilitare questo genere di applicazioni prima di procedere al riconoscimento OCR.

<!-- KC:beginInclude -->
Per riconoscere il testo presente alla posizione del navigatore ad oggetti con l'OCR di Windows, premere NVDA+r.
<!-- KC:endInclude -->

## Funzioni speciali per le applicazioni {#ApplicationSpecificFeatures}

NVDA fornisce alcuni comandi o funzioni per certe applicazioni in modo da facilitare gli utenti nello svolgimento di operazioni che, altrimenti, risulterebbero molto complesse e poco accessibili.

### Microsoft Word {#MicrosoftWord}
#### Lettura automatica delle intestazioni di riga e colonna {#WordAutomaticColumnAndRowHeaderReading}

NVDA è in grado di leggere automaticamente le intestazioni delle righe e delle colonne quando si esplora una tabella in Microsoft Word.
Per far questo, è necessario che l'opzione "Leggi le intestazioni riga/colonna delle tabelle", situata nella finestra formattazione documento delle [Impostazioni NVDA](#NVDASettings) sia attiva.

Se si utilizza [UI Automation per accedere ai controlli dei documenti Microsoft Word](#MSWordUIA), che è predefinito nelle ultime versioni di Word e Windows, le celle della prima riga verranno automaticamente considerate come intestazioni di colonna; analogamente, le celle della prima colonna verranno automaticamente considerate come intestazioni di riga.

Di contro, se non si utilizza [Tale funzione](#MSWordUIA), si dovrà indicare a NVDA quale riga o colonna contiene le intestazioni di una determinata tabella.
Dopo essersi spostati nella prima cella della colonna o della riga che contiene le intestazioni, utilizzare uno dei comandi sottostanti:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Imposta intestazioni colonna |NVDA+shift+c |Imposta il riconoscimento dell'intestazione colonna per la prima cella, consentendo la lettura automatica delle intestazioni successive. La doppia pressione cancellerà tale impostazione.|
|Imposta intestazioni riga |NVDA+shift+r |Imposta il riconoscimento dell'intestazione riga per la prima cella, consentendo la lettura automatica delle intestazioni successive. La doppia pressione cancellerà tale impostazione.|

<!-- KC:endInclude -->
Queste impostazioni saranno memorizzate nel documento come segnalibri, in un formato compatibile con altri screen reader, ad esempio Jaws.
Ciò significa che se si utilizza un altro screen reader e si apre quel documento successivamente, le intestazioni di righe e colonne saranno già impostate.

#### Modalità navigazione in Microsoft Word {#BrowseModeInMicrosoftWord}

Allo stesso modo delle pagine web, la modalità navigazione può essere utilizzata in Microsoft Word per poter servirsi di funzioni quali la navigazione veloce con tasti rapidi o l'elenco elementi.
<!-- KC:beginInclude -->
Per attivare o disattivare la modalità navigazione in Microsoft Word, servirsi della combinazione NVDA+spazio.
<!-- KC:endInclude -->
Per ulteriori informazioni sulla modalità navigazione e sulla navigazione veloce, vedere la [sezione modalità Navigazione](#BrowseMode).

##### L'elenco elementi {#WordElementsList}

<!-- KC:beginInclude -->
Quando ci si trova in modalità navigazione in Microsoft Word, si può accedere all'elenco elementi tramite la combinazione di tasti NVDA+f7
<!-- KC:endInclude -->
L'elenco degli elementi può elencare titoli, link, annotazioni (che comprende commenti e il tener traccia delle modifiche) e gli errori, per il momento limitato agli errori di ortografia.

#### Leggere i commenti {#WordReportingComments}

<!-- KC:beginInclude -->
Per far in modo che NVDA legga i commenti alla posizione corrente del cursore, premere NVDA+alt+c.
<!-- KC:endInclude -->
Si noti che tutti i commenti del documento, oltre che lo storico delle modifiche, può essere raggiunto tramite l'elenco elementi, selezionando annotazioni nella casella tipo.

### Microsoft Excel {#MicrosoftExcel}
#### Lettura automatica delle intestazioni di riga e colonna {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA è in grado di leggere automaticamente le intestazioni delle righe e delle colonne quando si esplora un foglio di lavoro in Microsoft Excel.
Per far questo, per prima cosa è necessario che l'opzione "Leggi le intestazioni riga/colonna delle tabelle", situata nella finestra formattazione documento delle [Impostazioni NVDA](#NVDASettings) sia attiva.
In secondo luogo, NVDA ha bisogno di conoscere quale riga o colonna contenga le intestazioni.
Dopo essersi spostati nella prima cella della colonna o della riga che contiene le intestazioni, utilizzare uno dei comandi sottostanti:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Imposta intestazioni colonna |NVDA+shift+c |Imposta il riconoscimento dell'intestazione colonna per la prima cella, consentendo la lettura automatica delle intestazioni successive. La doppia pressione cancellerà tale impostazione.|
|Imposta intestazioni riga |NVDA+shift+r |Imposta il riconoscimento dell'intestazione riga per la prima cella, consentendo la lettura automatica delle intestazioni successive. La doppia pressione cancellerà tale impostazione.|

<!-- KC:endInclude -->
Queste impostazioni saranno memorizzate nel documento come segnalibri, in un formato compatibile con altri screen reader, ad esempio Jaws.
Ciò significa che se si utilizza un altro screen reader e si apre quel foglio di lavoro successivamente, le intestazioni di righe e colonne saranno già impostate.

#### L'elenco elementi {#ExcelElementsList}

Un po' come accade per le pagine web, NVDA è provvisto di un elenco elementi per Microsoft Excel che permette di accedere ad un molteplice numero di informazioni.
<!-- KC:beginInclude -->
Per accedere all'elenco elementi in Microsoft Excel, utilizzare NVDA+f7.
<!-- KC:endInclude -->
I vari tipi di informazioni disponibili nell'elenco elementi sono:

* Grafici: Elenca tutti i grafici nel foglio di lavoro attivo.
Selezionando un grafico e premendo invio o utilizzando il bottone Vai evidenzia il grafico per poter essere esplorato con i tasti freccia.
* Commenti: elenca tutte le celle del foglio di lavoro contenenti commenti.
Per ciascuna cella sarà mostrato l'indirizzo e i relativi commenti.
Premendo il tasto Invio o il pulsante Vai in presenza di un commento ci si sposterà a quella determinata cella.
* Formule: Elenca tutte le celle del foglio di lavoro contenenti formule.
Per ciascuna cella sarà mostrato l'indirizzo e le relative formule.
Premendo il tasto Invio o il pulsante Vai in presenza di una formula ci si sposterà a quella determinata cella.
* Fogli: Elenca tutti i fogli della cartella di lavoro.
La pressione del tasto f2 nell'elenco dei fogli permette di rinominare il foglio selezionato.
Premendo il tasto Invio o il pulsante Vai in presenza di un foglio ci si sposterà a quel determinato foglio.
* Campi: elenca tutti i campi del form contenuti nella cartella di lavoro attiva.
Per ciascun campo, l'elenco elementi visualizza il testo alternativo del campo assieme all'indirizzo delle celle che lo riguardano. 
Selezionando un campo premendo invio o utilizzando il pulsante "vai a" provocherà lo spostamento in quel campo in modalità navigazione.

#### Leggere le note {#ExcelReportingComments}

<!-- KC:beginInclude -->
Per far in modo che NVDA legga note e commenti della cella evidenziata, premere NVDA+alt+c.
In Microsoft 2016, 365 e successivi, i commenti classici in Microsoft Excel sono stati rinominati "note".
<!-- KC:endInclude -->
Si noti che tutte le note del foglio di lavoro possono essere raggiunte anche dall'elenco elementi premendo NVDA+f7.

NVDA può anche visualizzare una finestra di dialogo specifica per l'aggiunta o la modifica di una determinata nota.
NVDA va a modificare il campo editazione messo a disposizione da MS Excel per aggirare un problema di accessibilità, ma la combinazione di tasti messa a disposizione funziona indipendentemente dal fatto che NVDA sia in esecuzione o meno.
<!-- KC:beginInclude -->
Per aggiungere o modificare una determinata nota, in una cella focalizzata, premere shift+f2.
<!-- KC:endInclude -->

Questa combinazione di tasti non può essere modificata e non compare nella finestra tasti e gesti di immissione di NVDA.

Nota: è possibile aprire l'area di modifica delle note in MS Excel anche dal menu contestuale di qualsiasi cella del foglio di lavoro.
Tuttavia, questa operazione farà comparire la regione di modifica inaccessibile, non quella messa a punto da NVDA..

In Microsoft Office 2016, 365 e successivi, è stata aggiunta una nuova finestra di dialogo per i commenti sullo stile.
Questa finestra di dialogo è accessibile e fornisce più funzioni come la risposta ai commenti, ecc.
Può anche essere aperta dal menu contestuale di una determinata cella.
I commenti aggiunti alle celle tramite la finestra di dialogo del nuovo stile non sono correlati alle "note".

#### Lettura di celle protette {#ExcelReadingProtectedCells}

Se una cartella di lavoro è stata protetta, potrebbe non essere possibile portare il focus in alcune celle che non possono essere modificate.
<!-- KC:beginInclude -->
Per spostarsi in una cella protetta, passare alla modalità navigazione premendo NVDA+Spazio, dopodiché utilizzare i comandi standard di Excel come le frecce per spostarsi tra le celle del foglio di lavoro.
<!-- KC:endInclude -->

#### Campi {#ExcelFormFields}

Le cartelle di lavoro di Excel possono includere i campi.
è possibile accedervi attraverso l'elenco elementi oppure premendo i tasti di navigazione rapida per lettera f o shift+f.
Una volta raggiunto un campo in modalità navigazione, premere invio o la barra spaziatrice per attivarlo o per interagire con esso in modalità focus.
Per ulteriori informazioni sulla modalità di navigazione e i caratteri singoli, si veda la [sezione modalità navigazione](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Commuta lettura note |control+shift+s |Quando una presentazione è in esecuzione, questo comando permetterà di alternare tra le note del relatore della diapositiva e il contenuto della diapositiva stessa. Questo riguarda solo ciò che NVDA legge, non ciò che è visualizzato sullo schermo.|

<!-- KC:endInclude -->

### foobar	2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Annuncia tempo rimanente |control+shift+r |Annuncia il tempo restante della traccia attualmente in esecuzione, se ve n'è una.|
|Annuncia tempo trascorso |control+shift+e |Annuncia il tempo trascorso della traccia attualmente in esecuzione, se ve n'è una.|
|Annuncia lunghezza traccia |control+shift+t |Annuncia la lunghezza della traccia attualmente in esecuzione, se ve n'è una.|

<!-- KC:endInclude -->

Nota: Questi tasti caldi funzionano soltanto se la barra di stato di Foobar ha il formato predefinito.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Annuncia messaggi recenti |NVDA+control+1-4 |Annuncia uno degli ultimi messaggi, a seconda del numero premuto; ad esempio NVDA+control+2 legge il secondo messaggio più recente.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA offre un supporto avanzato per Poedit 3.4 o versioni successive.

<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Legge le note per traduttori |`control+shift+a` |Legge ogni nota presente per traduttori. La doppia pressione mostrerà il contenuto in una finestra navigabile.|
|Legge commenti |`control+shift+c` |Legge qualsiasi commento all'interno della finestra commenti. La doppia pressione mostrerà il contenuto in una finestra navigabile|
|Legge il vecchio testo sorgente |`control+shift+o` |Legge il vecchio testo sorgente, se presente. La doppia pressione mostrerà il contenuto in una finestra navigabile|
|Legge avvisi di traduzione |`control+shift+w` |Segnala un avviso di traduzione, se presente. La doppia pressione mostrerà il contenuto in una finestra navigabile|

<!-- KC:endInclude -->

### Kindle per PC {#Kindle}

NVDA supporta la lettura e la navigazione dei libri in Amazon Kindle per PC.
Questa funzionalità è disponibile solo nei libri Kindle in cui è integrata la funzione "supporto per screen reader", cosa che è possibile controllare alla pagina dettagli per il libro. La stragrande maggioranza dei testi supporta questa funzione.

Per la lettura dei libri viene usata la modalità navigazione.
Si attiverà automaticamente non appena si apre un libro, o si posiziona il focus nell'area contenente il testo.
Sempre automaticamente verranno girate le pagine sia con lo spostamento del cursore, sia con la modalità dire tutto.
<!-- KC:beginInclude -->
è possibile utilizzare manualmente i tasti pagina su o pagina giù per spostarsi tra le pagine.
<!-- KC:endInclude -->

La navigazione veloce con le lettere è supportata per link e grafici, ma soltanto per la pagina corrente.
La navigazione per link comprende anche le note a piè di pagina.

NVDA fornisce un supporto iniziale per la lettura e la navigazione interattiva di contenuti matematici per i libri accessibili per la matematica.
Si prega di consultare la sezione [lettura della matematica](#ReadingMath) per ulteriori informazioni.

#### Selezionare il testo {#KindleTextSelection}

Kindle consente di eseguire varie operazioni sul testo selezionato, come l'ottenimento di una definizione dal dizionario, l'aggiunta di note ed evidenziazioni, copiare il testo negli appunti e la ricerca sul web.
Per fare questo, per prima cosa selezionare il testo come sempre in modalità navigazione (ad esempio tenendo premuto shift e spostandosi con i tasti freccia).
<!-- KC:beginInclude -->
Dopo aver selezionato il testo, premere il tasto applicazioni o maiusc+f10 per visualizzare le opzioni disponibili per operare con la selezione.
<!-- KC:endInclude -->
Se si esegue questa operazione senza aver selezionato alcun testo, verranno visualizzate le opzioni inerenti la parola sotto al cursore.

#### Note dell'utente {#KindleUserNotes}

È possibile aggiungere una nota riguardo una parola o un passaggio di testo.
Per fare questo, per prima cosa selezionare il testo più rilevante, successivamente accedere alle opzioni di selezione come spiegato nel paragrafo precedente.
Quindi, scegliere Aggiungi Nota.

Durante la lettura in modalità navigazione, NVDA chiamerà questo genere di note con il termine "commenti".

Per visualizzare, modificare o eliminare una nota:

1. Spostare il cursore sul testo contenente la nota.
1. Accedere alle opzioni inerenti la selezione come descritto sopra.
1. Scegliere Modifica Nota.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Quando ci si trova nella visualizzazione della tabella dei libri aggiunti:

| Nome |Tasto |Descrizione|
|---|---|---|
|Invio |invio |Apre il libro selezionato.|
|Menu di contesto |applicazioni |Apre il menu di contesto per il libro selezionato.|

<!-- KC:endInclude -->

### Windows Console {#WinConsole}

NVDA fornisce supporto per la console di Windows utilizzata da Prompt dei comandi, PowerShell e il sottosistema Windows per Linux.
La finestra della console ha dimensioni fisse, in genere molto più piccole del buffer che contiene l'output.
Man mano che viene aggiunto del testo, il contenuto scorre verso l'alto e il testo precedente non è più visibile.
Nelle versioni di Windows precedenti a Windows11 22H2, NVDA non è in grado di leggere il testo che non risulta più visibile nella finestra con i comandi standard di revisione.
Pertanto, è necessario scorrere la finestra della console per rileggere del testo precedente.
Nelle versioni più recenti della console e nel terminale di Windows, è possibile riesaminare l'intero buffer di testo liberamente senza la necessità di scorrere la finestra.
<!-- KC:beginInclude -->
Le seguenti scorciatoie da tastiera integrate nella Console possono essere utili quando si [esplora del testo](#ReviewingText) con NVDA nelle versioni precedenti della console di Windows:

| Nome |Tasto |Descrizione|
|---|---|---|
|Scorri verso l'alto |control+freccia su |Scorre la finestra della console verso l'alto, in modo da poter leggere il testo precedente.|
|Scorri verso il basso |control+freccia giù |Scorre la finestra della console verso il basso, in modo da poter leggere il testo successivo.|
|Vai all'inizio |control+inizio |Fa scorrere la finestra della console all'inizio del buffer|
|Vai alla fine |control+fine |Fa scorrere la finestra della console alla fine del buffer|

<!-- KC:endInclude -->

## Configurare NVDA {#ConfiguringNVDA}

è possibile accedere alla maggior parte delle configurazioni servendosi delle finestre di dialogo presenti al sottoMenu preferenze del menu principale di NVDA.
Tali impostazioni sono situate nella [finestra di dialogo multipagina impostazioni di NVDA](#NVDASettings).
In tutte le finestre di dialogo di NVDA, premere il tasto OK per accettare i cambiamenti effettuati.
Per annullare invece premere il bottone Annulla o il tasto Esc.
Per alcune finestre di dialogo, è possibile premere il pulsante "Applica" affinché le impostazioni abbiano effetto immediatamente senza dover chiudere la finestra.
La maggior parte delle finestre di dialogo di NVDA supporta l'aiuto contestuale.
<!-- KC:beginInclude -->
All'interno di una finestra di dialogo, premendo `f1` si aprirà la Guida utente al paragrafo relativo all'impostazione in cui si trova il focus o alla finestra di dialogo corrente.
<!-- KC:endInclude -->
Alcune impostazioni possono anche essere cambiate utilizzando dei tasti rapidi, che verranno elencati nelle sezioni successive.

### Impostazioni di NVDA {#NVDASettings}

<!-- KC:settingsSection: || Name | Desktop key | Laptop key | Description | -->
NVDA fornisce diversi parametri di configurazione che possono essere modificati utilizzando la finestra di dialogo delle impostazioni.
Per semplificare la ricerca del tipo di impostazioni che si desidera modificare, tale finestra visualizza un elenco di categorie di configurazione tra cui scegliere.
Quando si seleziona una categoria, tutte le impostazioni ad essa correlate vengono mostrate nella finestra di dialogo.
Per muoversi tra le categorie, servirsi di `tab` o `shift+tab` per raggiungere l'elenco, quindi spostarsi con i tasti freccia su e giù per scorrere le voci che lo compongono.
Da qualsiasi punto della finestra, è possibile anche passare alla categoria successiva premendo `ctrl+tab`, o tornare indietro premendo `shift+ctrl+tab`.

Dopo aver modificato una o più impostazioni, si può utilizzare il pulsante applica, nel qual caso la finestra di dialogo rimarrà aperta, consentendo di effettuare ulteriori modifiche o scegliere un'altra categoria.
Se si desidera salvare le impostazioni e chiudere la finestra di dialogo Impostazioni di NVDA, è possibile utilizzare il pulsante OK.

Alcune categorie di impostazioni dispongono di un tasto rapido.
Se premuto, il tasto rapido aprirà la finestra di dialogo impostazioni di NVDA in quella particolare categoria.
Da impostazioni predefinite, non tutte le categorie dispongono di un tasto rapido personalizzato.
Se si accede spesso a categorie che non dispongono di tasti di scelta rapida dedicati, si consiglia di utilizzare la [finestra di dialogo Gesti e tasti di immissione](#InputGestures) per aggiungere un comando rapido o un gesto a tocco. .

Qui di seguito vengono descritte le categorie presenti nella finestra impostazioni di NVDA..

#### Generale {#GeneralSettings}

<!-- KC:setting -->

##### Apri impostazioni Generali {#OpenGeneralSettings}

tasto: `NVDA+control+g`

La categoria generale delle impostazioni di NVDA contiene soprattutto opzioni inerenti il cambio della lingua dello screen reader e se debba essere effettuato un controllo automatico della presenza di aggiornamenti.
Questa categoria contiene le seguenti opzioni:

##### Lingua {#GeneralSettingsLanguage}

Una casella combinata dove è possibile selezionare la lingua di visualizzazione dei messaggi dell'interfaccia utente.
Vi sono parecchie lingue, tuttavia l'opzione predefinita è chiamata "User Default, Windows". 
Questa scelta istruisce NVDA ad utilizzare le impostazioni della lingua di Windows salvate nel pannello di controllo.

Si noti che NVDA deve essere riavviato dopo una nuova selezione della lingua
Quando viene visualizzata la finestra di conferma, selezionare "riavvia ora" o "riavvia in seguito" a seconda se si desidera utilizzare la nuova lingua ora o in un secondo momento. Se viene selezionato "riavvia in seguito", la configurazione deve essere salvata (o manualmente, o utilizzando la funzionalità Salva configurazione all'uscita).

##### Salva la configurazione all'uscita {#GeneralSettingsSaveConfig}

Una casella di controllo che se attivata permette a NVDA di salvare automaticamente la configurazione all'uscita dal programma.

##### Mostra opzioni all'uscita di NVDA {#GeneralSettingsShowExitOptions}

Una casella di controllo che permette di decidere se, alla chiusura di NVDA, debbano comparire opzioni aggiuntive per decidere come chiudere il programma.
Se attivata, quando si cerca di chiudere NVDA apparirà una finestra di dialogo che chiederà se uscire, riavviare lo screen reader, riavviarlo senza componenti aggiuntivi o installare gli aggiornamenti in sospeso.
Se non la si attiva, NVDA uscirà immediatamente.

##### Riproduci un suono all'avvio o all'uscita di NVDA {#GeneralSettingsPlaySounds}

Questa opzione è costituita da una casella di controllo che, se attivata, permette a NVDA di riprodurre un suono quando si avvia e quando viene terminato.

##### Livello di logging {#GeneralSettingsLogLevel}

Una casella combinata che permette di stabilire l'ammontare delle informazioni che NVDA scriverà sul suo file di log. 
La maggior parte degli utenti non avrà bisogno di modificare questo parametro.
Tuttavia, nel caso si vogliano segnalare bug, può essere una buona idea alzare il livello di log; naturalmente è anche possibile disattivare completamente la funzione.

I livelli di log disponibili sono i seguenti:

* Disabilitato: al di là di un breve messaggio di avvio, NVDA non loggherà nulla durante l'esecuzione.
* info: NVDA loggherà informazioni di base quali messaggi di avvio e informazioni utili agli sviluppatori.
* Debug warning: Verranno loggati i messaggi di avviso che non sono causati da errori gravi.
* Input/output: verranno loggati i tasti premuti, sia della tastiera che del display braille, nonché i messaggi provenienti dalla sintesi vocale e dalla barra braille. 
Se vi sono problemi con la privacy, non abilitare mai questa funzione.
* Debug: Oltre alle informazioni, agli avvisi e ai messaggi di input / output, verranno loggati ulteriori messaggi di debug. 
Proprio come input / output, Se vi sono problemi con la privacy, non abilitare mai questa funzione.

##### Esegui NVDA dopo l'accesso {#GeneralSettingsStartAfterLogOn}

Una casella di controllo che, se attivata, permetterà a NVDA di avviarsi subito dopo che l'utente avrà inserito i propri dati nella schermata di accesso al sistema.
Questa opzione è disponibile soltanto nelle versioni Installer.

##### Utilizza NVDA nella finestra di Accesso, richiede privilegi di amministratore {#GeneralSettingsStartOnLogOnScreen}

Se si dispone di un sistema nel quale bisogna inserire nome e password per accedere al sistema, attivare questa casella di controllo per fare in modo che NVDA sia in grado di leggere questo tipo di informazioni.
Questa opzione è disponibile soltanto nelle versioni Installer.

##### Utilizza le impostazioni salvate nella finestra di Accesso {#GeneralSettingsCopySettings}

La pressione di questo tasto copierà le proprie impostazioni utente di NVDA nella cartella delle configurazioni di sistema, di modo che NVDA le possa utilizzare nelle schermate di Accesso utente, nei controlli UAC e nelle altre [schermate di sicurezza](#SecureScreens).
Per precauzione, se si vuole essere certi che le proprie impostazioni vengano copiate correttamente, conviene salvare la configurazione con il comando Control+NVDA+c, oppure andare alla voce Salva Configurazione nel menu di NVDA.
Questa opzione è disponibile soltanto nelle versioni Installer.

##### Controlla automaticamente la presenza di aggiornamenti di NVDA {#GeneralSettingsCheckForUpdates}

Se attivata, NVDA controllerà automaticamente la presenza di nuove versioni e notificherà l'utente della loro disponibilità.
è anche possibile controllare manualmente, selezionando la voce controllo presenza aggiornamenti, situata all'interno del menu aiuto.
A prescindere dal metodo scelto per controllare la presenza di aggiornamenti, è necessario che NVDA invii al server alcune informazioni in modo da ricevere l'aggiornamento corretto per il proprio sistema.
Verranno sempre inviate le seguenti informazioni:

* Versione di NVDA
* Versione del sistema operativo in uso
* Se il sistema operativo è a 64 o a 32 bit

##### Consenti a NV Access di raccogliere statistiche sull'utilizzo dello screen reader {#GeneralSettingsGatherUsageStats}

Se questa funzione è attivata, la Nv Access utilizzerà le informazioni provenienti dal server che gestisce gli aggiornamenti per raccogliere alcune informazioni di carattere demografico sugli utenti di NVDA, ossia sistema operativo e nazione d'origine.
Si noti comunque che sebbene venga utilizzato l'indirizzo IP per calcolare lo stato di provenienza dell'utente, tale indirizzo IP non verrà mai salvato sui server.
Oltre alle informazioni obbligatorie usate per controllare gli aggiornamenti, saranno inviati anche i seguenti dati:

* Lingua dell'interfaccia di NVDA
* Se la copia attualmente in uso è installer o portable
* Nome della sintesi vocale in uso (compreso il nome del driver del componente aggiuntivo e la sua provenienza)
* Nome del Display braille in uso (compreso il nome del driver del componente aggiuntivo e la sua provenienza)
* Tabella di lettura corrente (solo se si usa il braille)

Queste informazioni risultano di grandissimo aiuto a Nv Access per dare priorità a rami specifici di sviluppo di NVDA

##### Notifica aggiornamenti in sospeso all'avvio {#GeneralSettingsNotifyPendingUpdates}

Se la funzione è attivata, NVDA avviserà l'utente nel caso vi sia un aggiornamento in sospeso all'avvio, dando la possibilità di effettuare l'installazione.
è anche possibile installare l'aggiornamento in sospeso manualmente dalla finestra di uscita di NVDA (se attivata), dal menu di NVDA, o quando si esegue un nuovo controllo dal menu aiuto.

#### Impostazioni voce {#SpeechSettings}

<!-- KC:setting -->

##### Apri Impostazioni Voce {#OpenSpeechSettings}

Tasto: `NVDA+control+v`

La categoria voce nella finestra impostazioni di NVDA contiene opzioni che permettono di modificare il sintetizzatore da utilizzare nonché le caratteristiche delle varie voci come tono, velocità, etc.
Per informazioni su come modificare molti di questi parametri da qualunque punto ci si trovi, si veda la sezione [modificare al volo le Impostazioni del sintetizzatore](#SynthSettingsRing).

La categoria impostazioni voce contiene le seguenti opzioni:

##### Cambia sintetizzatore {#SpeechSettingsChange}

La prima opzione della categoria voce è il pulsante cambia... Premendolo, si attiverà la finestra [Selezione sintetizzatore](#SelectSynthesizer), che consente di scegliere la famiglia di voci attiva e la periferica d'uscita.
Questa finestra si aprirà in cima alla schermata di impostazioni di NVDA.
Per tornare alla finestra impostazioni di NVDA sarà sufficiente salvare o annullare.

##### Voce {#SpeechSettingsVoice}

Una casella combinata che elenca tutte le voci del sintetizzatore selezionato. 
è possibile scorrere la lista ed ascoltarla con le frecce.
In particolare la freccia giù e la freccia sinistra sposteranno verso il basso dell'elenco, mentre la freccia su e la freccia destra sposteranno verso l'alto.

##### Variante {#SpeechSettingsVariant}

Una casella combinata che permette di selezionare con quale variante il sintetizzatore debba parlare. 
Al momento, soltanto Espeak NG supporta questa impostazione. 
Le varianti in Espeak sono simili alle voci, esse modificano i parametri e gli attributi della voce originale, per cui ad esempio potremmo avere voci simili a quelle maschili o femminili.
Nel caso si utilizzi una sintesi vocale di terze parti, la funzione è disponibile solo se il sintetizzatore supporta le varianti.

##### Velocità {#SpeechSettingsRate}

Questa opzione permette di modificare la velocità della voce. 
Si tratta di un controllo che va da 0 a 100, (dove 0 indica il limite più lento e 100 il massimo della velocità).

##### Aumento velocità {#SpeechSettingsRateBoost}

Abilitando questa opzione si aumenterà in modo significativo la velocità del parlato, se supportato dal sintetizzatore corrente.

##### Tono {#SpeechSettingsPitch}

Questa opzione permette di modificare l'altezza della voce corrente. 
Si tratta di un controllo che va da 0 a 100, (0 rappresenta l'altezza minima, 100 la massima).

##### Volume {#SpeechSettingsVolume}

Un controllo che va da 0 a 100, (0 indica il volume più basso, 100 il più alto).

##### Inflessione {#SpeechSettingsInflection}

Un controllo che permette di selezionare con quanta inflessione (aumento e decadimento del pitch) la sintesi vocale debba parlare. Al momento soltanto Espeak NG fornisce questa funzionalità.

##### Cambio automatico della lingua {#SpeechSettingsLanguageSwitching}

Questa casella di controllo permette di stabilire se NVDA debba cambiare al volo la lingua con cui parla, nel caso all'interno del testo che si sta leggendo siano presenti i marcatori appositi.
Questa opzione risulta abilitata di default.

##### cambiamento automatico dialetti (quando supportato) {#SpeechSettingsDialectSwitching}

Se l'impostazione cambio automatico della lingua è attiva, questa casella di controllo farà in modo che NVDA modifichi anche il dialetto della lingua in uso.
Ad esempio, potrebbe essere possibile passare da un "american English" ad un "british English".
L'impostazione è disabilitata di default.

<!-- KC:setting -->

##### Livello di punteggiatura/simboli {#SpeechSettingsSymbolLevel}

Tasto: NVDA+p

Questa opzione permette di stabilire la quantità di punteggiatura e di altri simboli che dovranno essere annunciati in parole.
Ad esempio, se impostata su tutto, tutti i simboli verranno annunciati in parole.
Questa impostazione viene applicata a tutti i sintetizzatori, non soltanto a quello usato al momento.

##### Considera attendibile la lingua della voce corrente nel processare caratteri e simboli {#SpeechSettingsTrust}

Da impostazioni predefinite, questa funzione risulta attiva e consente di stabilire se NVDA debba ritenere affidabile la lingua della voce corrente nel processare simboli e caratteri.
Se per qualche motivo ci si accorge che NVDA sta leggendo la punteggiatura con un sintetizzatore o voce particolare in una lingua sbagliata, si consiglia di disattivare questa opzione, per forzare NVDA ad utilizzare le impostazioni globali per quella lingua.

##### Includi dati del consorzio Unicode (comprese le emoji) nel processare caratteri e simboli {#SpeechSettingsCLDR}

Quando questa casella di controllo è attiva, NVDA si servirà di ulteriori dizionari per pronunciare caratteri e simboli.
Tali dizionari contengono le descrizioni per molti simboli (in particolare le emoji) che sono fornite dal [Consorzio Unicode](http://www.unicode.org/consortium/) come parte del [Common Locale Data Repository](http://cldr.unicode.org/).
Se si desidera che NVDA sia in grado di leggere le descrizioni di simboli ed emoji fornite da questo servizio, è necessario attivare la casella di controllo.
In ogni caso, si consiglia di disattivare questa opzione nella circostanza in cui si disponga di una sintesi vocale in grado di leggere le emoji nativamente.

Si noti che le descrizioni dei caratteri aggiunte manualmente vengono salvate nella propria configurazione utente.
Perciò, se si modifica la descrizione di un'emoji, essa verrà letta a prescindere dal fatto che l'opzione sia attiva o meno.
è possibile aggiungere, rimuovere o modificare le descrizioni dei simboli nella finestra [Pronuncia punteggiatura/simboli](#SymbolPronunciation).

Per attivare o disattivare l'inclusione dei dati del consorzio Unicode da qualsiasi punto ci si trovi, assegnare un gesto personalizzato usando la [Finestra di dialogo Tasti e gesti di immissione](#InputGestures).

##### Percentuale di cambio tono per lettere maiuscole {#SpeechSettingsCapPitchChange}

Questo campo editazione permette di digitare un numero che sarà equivalente alla variazione di altezza (pitch) effettuato dalla sintesi vocale in presenza di lettere maiuscole.
Questo valore lavora in percentuale, perciò un valore negativo abbasserà il pitch, mentre uno positivo lo alzerà.
Per non effettuare alcuna modifica, digitare 0.
Di solito, NVDA aumenta leggermente il tono per qualsiasi lettera maiuscola, ma alcuni sintetizzatori potrebbero non supportare in maniera ottimale questa funzione.
Nel caso in cui il cambiamento del tono per le lettere maiuscole non sia ben supportato, si consiglia di servirsi delle opzioni [Leggi "cap" prima delle maiuscole](#SpeechSettingsSayCapBefore) e/o [ Emetti un beep per le maiuscole](#SpeechSettingsBeepForCaps) instead.

##### Leggi Cap prima delle Maiuscole {#SpeechSettingsSayCapBefore}

Una casella di controllo che, se attivata, istruisce NVDA a dire la parola "CAP" in presenza di una lettera maiuscola, se raggiunta scorrendo il testo con le frecce o se digitata a mano. 

##### Emetti un beep per le maiuscole {#SpeechSettingsBeepForCaps}

Se questa casella di controllo viene attivata, NVDA emetterà un leggero beep ogni qualvolta verrà incontrata una lettera maiuscola. 

##### Utilizza la modalità spelling se supportata {#SpeechSettingsUseSpelling}

Alcune parole sono costituite soltanto da un singolo carattere, ma talvolta, la pronuncia può risultare diversa se il carattere viene annunciato da solo (come quando viene fatto lo spelling), oppure come una parola.
Ad esempio, in inglese, "a" è sia una lettera che una parola e viene pronunciata in maniera diversa in entrambe i casi.
Questa opzione permette ai sintetizzatori di operare una differenziazione tra i due casi, se il sintetizzatore è in grado di supportarlo.
La maggior parte dei sintetizzatori supportano questa funzione.

Generalmente, si consiglia di abilitare questa impostazione.
Talvolta, può succedere che alcune sintesi Microsoft Speech Api si comportino in modo strano nell'eseguire lo spelling.
In caso ciò avvenga, consigliamo di disattivare questa caratteristica.

##### Descrizione ritardata dei caratteri al movimento del cursore {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Predefinita |Disattivata|
|Opzioni |Attivata, Disattivata|

Quando questa impostazione viene attivata, NVDA pronuncerà una descrizione del carattere man mano che ci si sposta lettera per lettera.

Per esempio, se si sta esaminando una riga carattere per carattere, e ci troviamo sulla lettera b, NVDA pronuncerà "Bologna" dopo un secondo di ritardo.
Questo può essere utile nel caso in cui si incontrino difficoltà nella comprensione dei simboli, o per le persone con problemi di udito..

Tale funzione verrà inibita nel caso in cui venga letto del testo durante il secondo di ritardo, oppure se viene premuto il tasto `control`.

##### Opzioni disponibili per il comando passa tra le modalità di voce {#SpeechModesDisabling}

Questo elenco di caselle di controllo consente di selezionare le [modalità di voce](#SpeechModes) da includere quando si passa da una all'altra utilizzando la combinazione di tasti `NVDA+s`.
Le modalità che saranno deselezionate verranno escluse dalle scelte possibili.
Per impostazione predefinita sono incluse tutte le modalità.

Ad esempio, se non si desidera utilizzare le modalità "beep" e "spenta", sarà sufficiente deselezionarle, mantenendo selezionati sia "parla" che "su richiesta".
Si noti che è necessario mantenere attivate almeno due modalità.

#### Selezionare un sintetizzatore {#SelectSynthesizer}

<!-- KC:setting -->

##### Apre la finestra di dialogo Seleziona sintetizzatore {#OpenSelectSynthesizer}

Tasto: `NVDA+control+s`

Questa opzione, che può essere aperta attivando il pulsante Cambia... dalla categoria voce della finestra impostazioni di NVDA, permette di selezionare il sintetizzatore che NVDA utilizzerà per parlare. 
Una volta selezionato il sintetizzatore preferito, premere Ok e NVDA lo utilizzerà come richiesto.
Se si verifica un errore durante il caricamento del sintetizzatore, NVDA avviserà l'utente con un messaggio e continuerà a utilizzare quello precedente.

##### Sintetizzatore {#SelectSynthesizerSynthesizer}

Questa opzione permette di selezionare il sintetizzatore che NVDA utilizzerà per parlare. 

Per un elenco di tutte le sintesi vocali supportate da NVDA, si veda la sezione [Sintesi vocali supportate](#SupportedSpeechSynths).

Un elemento speciale che sarà sempre disponibile in questo elenco è chiamato "nessun sintetizzatore", che permette di utilizzare NVDA senza alcun riscontro vocale.
Ciò può venir incontro a quegli utenti che preferiscono avvalersi esclusivamente del supporto braille, oppure a qualche sviluppatore vedente che desidera utilizzare solo la funzionalità "visualizzatore sintesi vocale".

#### Modificare al volo le impostazioni del sintetizzatore {#SynthSettingsRing}

Se si vogliono modificare i parametri della voce senza dover aprire la finestra inerente tali impostazioni, esistono alcuni tasti rapidi che consentono di spostarsi tra i parametri più comuni da qualunque punto ci si trovi:
<!-- KC:beginInclude -->

| Nome |Layout Desktop |Layout Laptop |Descrizione|
|---|---|---|---|
|Spostarsi al parametro successivo del sintetizzatore |NVDA+Control+Freccia destra |NVDA+Shift+Control+Freccia destra |Si sposta al prossimo parametro disponibile inerente la sintesi vocale e nel caso si sia raggiunto l'ultimo dell'elenco tornerà al primo|
|Spostarsi al parametro precedente del sintetizzatore |NVDA+Control+Freccia sinistra |NVDA+Shift+Control+Freccia sinistra |Si sposta al parametro precedente disponibile inerente la sintesi vocale e nel caso si sia raggiunto l'ultimo dell'elenco tornerà al primo|
|Aumentare il parametro corrente del sintetizzatore |NVDA+Control+Freccia su |NVDA+Shift+Control+Freccia su |Aumenta il valore del parametro sul quale si è posizionati. Ad esempio si aumenta la velocità, poi ci si sposta all'impostazione successiva, si aumenta il volume etc|
|Aumentare il parametro corrente del sintetizzatore con un incremento maggiore |`NVDA+control+pagina su` |`NVDA+shift+control+pagina su` |Aumenta il valore del parametro del sintetizzatore su cui si è posizionati con un incremento maggiore. Ad esempio, se ci si trova nelle impostazioni per scegliere la voce, avanzerà di 20 valori alla volta invece che uno soltanto; oppure, se ci si trova nei cursori di avanzamento (velocità, tono, etc) incrementerà il valore fino al 20%|
|Diminuire il parametro corrente del sintetizzatore |NVDA+Control+Freccia giù |NVDA+Shift+Control+Freccia giù |Diminuisce il valore del parametro sul quale si è posizionati. Ad esempio si diminuisce la velocità, poi ci si sposta all'impostazione successiva, si diminuisce il volume etc|
|Diminuire il parametro corrente del sintetizzatore con un decremento maggiore |`NVDA+control+pagina giù` |`NVDA+shift+control+pagina giù` |Diminuisce il valore del parametro del sintetizzatore su cui si è posizionati con un decremento maggiore. Ad esempio, se ci si trova nelle impostazioni per scegliere la voce, tornerà indietro di 20 valori alla volta invece che uno soltanto; oppure, se ci si trova nei cursori di avanzamento (velocità, tono, etc) diminuirà il valore fino al 20%|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

La categoria Braille nelle impostazioni di NVDA contiene opzioni che permettono di modificare diversi aspetti inerenti le tabelle in ingresso e in uscita, nonché svariati parametri del proprio display braille.
Questa categoria contiene le seguenti opzioni:

##### Cambia display braille {#BrailleSettingsChange}

Il pulsante cambia... nella categoria braille delle impostazioni di NVDA attiva la finestra [Selezione display Braille](#SelectBrailleDisplay), che consente di scegliere il display braille da usare.
Questa finestra si aprirà in cima alla schermata di impostazioni di NVDA.
Per tornare alla finestra impostazioni di NVDA sarà sufficiente salvare o annullare.

##### Tabella lettura {#BrailleSettingsOutputTable}

L'opzione successiva che si raggiunge in questa categoria è rappresentata dalla casella combinata Tabella Braille lettura.
In questa casella combinata, vengono elencate tabelle braille per svariate lingue, tipi e gradi di braille.
La tabella scelta verrà utilizzata per tradurre il testo in braille da presentare poi sulla barra.
è possibile spostarsi da una tabella braille all'altra utilizzando le frecce.

##### Tabella scrittura {#BrailleSettingsInputTable}

Similmente all'opzione vista in precedenza, l'impostazione successiva è chiamata Tabella braille scrittura.
La tabella selezionata verrà utilizzata per tradurre i caratteri braille inseriti tramite tastiera perkins in testo.
Ci si può spostare da una tabella all'altra utilizzando le frecce.

Si noti che questa opzione è utile solo se il display braille possiede una tastiera in stile Perkins e se il driver supporta tale caratteristica.
Nel caso il display braille che si vuole adoperare sia dotato di tastiera perkins, e NVDA non sia ancora in grado di supportarla, questo verrà evidenziato nella [sezione Display Braille supportati](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Modalità Braille {#BrailleMode}

Tasto: `NVDA+alt+t`

Questa opzione consente di selezionare tra le modalità braille disponibili.

Attualmente, sono supportate due modalità Braille: "Inseguimento cursori" e "Output sintesi vocale".

Quando si seleziona inseguimento cursori, il display braille si aggancerà al cursore di sistema/focus o al navigatore ad oggetti/cursore di controllo, a seconda della situazione e della configurazione braille. 

Quando invece risulta selezionata l'opzione "output sintesi vocale", nel display braille apparirà ciò che NVDA invia al sintetizzatore nella modalità "parlare".

##### Espandi la parola sotto il cursore utilizzando il Braille Computer {#BrailleSettingsExpandToComputerBraille}

Questa opzione permette la visualizzazione della parola sotto il cursore nel formato Computer Braille non contratto.

##### Mostra cursore {#BrailleSettingsShowCursor}

Questa opzione permette di attivare o disattivare la visualizzazione del cursore braille.
Si applica al cursore di sistema e al cursore di controllo, ma non agli indicatori di selezione.

##### Cursore lampeggiante {#BrailleSettingsBlinkCursor}

Questa opzione consente al cursore braille di lampeggiare.
Se il lampeggìo viene disattivato, il cursore braille sarà sempre visibile, senza che i puntini corrispondenti si alzino e abbassino ritmicamente.
L'indicatore della selezione non viene influenzato da questa opzione, per cui i puntini 7 e 8 rimarranno sempre stabili, senza alcun lampeggìo.

##### Velocità lampeggio cursore (ms) {#BrailleSettingsBlinkRate}

Si tratta di un campo numerico che permette di modificare la velocità di lampeggio del cursore in millisecondi.

##### Forma del cursore focus {#BrailleSettingsCursorShapeForFocus}

Questa opzione permette di selezionare la forma, in punti braille, del cursore braille quando il braille segue il focus.
L'indicatore della selezione non è affetto da questa funzione.

##### Forma del cursore di controllo {#BrailleSettingsCursorShapeForReview}

Questa opzione permette di selezionare la forma, in punti braille, del cursore braille quando il braille segue il cursore di controllo.
L'indicatore della selezione non è affetto da questa funzione.

##### Mostra Messaggi {#BrailleSettingsShowMessages}

Si tratta di una casella combinata che stabilisce se NVDA debba visualizzare o meno messaggi in braille e la loro durata in secondi sul display, prima che essi scompaiano automaticamente.

Per attivare o disattivare la visualizzazione dei messaggi da qualsiasi posto, assegnare un gesto personalizzato utilizzando la [finestra di dialogo Gesti e tasti di immissione](#InputGestures).

##### Timeout dei messaggi(sec) {#BrailleSettingsMessageTimeout}

Si tratta di un campo numerico che controlla per quanto tempo i messaggi di NVDA saranno mostrati sul Display Braille.
Il messaggio sparirà immediatamente non appena si preme un cursor routing sulla barra braille, ma lo si potrà rileggere se si preme una combinazione di tasti che attivano il messaggio.
L'opzione è visibile soltanto se "mostra messaggi" è impostato su "usa timeout".

<!-- KC:setting -->

##### Inseguimento Braille {#BrailleTether}

Tasto: NVDA+control+t

Questa impostazione permette di decidere se il display braille seguirà il focus di sistema, il navigatore ad oggetti (cursore di controllo) o entrambi.
Quando è selezionata "automatico", il braille seguirà il focus e il cursore di sistema.
Tuttavia, nel momento in cui l'utente compie un'azione esplicita cambiando la posizione del cursore di controllo o del navigatore ad oggetti, il braille inizierà temporaneamente a seguire quest'ultimi, fino a quando non verrà modificata la posizione del cursore di sistema.
Se si desidera che il braille segua sempre il focus/cursore di sistema, configurare questa funzione su "Braille segue Focus".
Così facendo, il braille non seguirà mai il navigatore ad oggetti o il cursore di controllo.
Se si desidera che il braille segua sempre il cursore di controllo o il navigatore ad oggetti, configurare questa funzione su "Braille segue cursore di controllo".
Così facendo, il braille non seguirà mai il focus / cursore di sistema.

##### Sposta il cursore di sistema con cursor routing anche se il braille segue il cursore di controllo {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Default (Mai), Mai, Solo quando l'inseguimento è su automatico, Sempre|
|Predefinito |Mai|

Questa impostazione determina se anche il cursore di sistema debba essere spostato con la pressione di un cursor routing.
Il valore predefinito dell'impostazione è mai, il che significa che la pressione di un cursor routing non sposterà mai il cursore di sistema quando il braille segue il cursore di controllo.

Quando questa opzione è impostata su Sempre, e [l'inseguimento braille](#BrailleTether) è impostato su "automaticamente" o "al cursore di controllo", la pressione di un cursor routing sposterà anche il cursore di sistema..
Se invece ci troviamo nella [Modalità in linea](#ScreenReview), non esiste un cursore fisico.
In questo caso, NVDA tenterà di portare il focus al testo su cui è stato premuto il cursor routing.
Lo stesso accade per la [navigazione ad oggetti](#ObjectReview).

è anche possibile impostare l'opzione in modo da spostare il cursore se l'inseguimento è settato su automaticamente.
In tal caso, la pressione di un cursor routing sposterà il cursore di sistema solo quando l'inseguimento è impostato su automaticamente, mentre non farà nulla nel caso in cui l'inseguimento sia impostato manualmente su cursore di controllo.

Questa opzione è visibile soltanto se "[l'inseguimento braille](#BrailleTether)" è impostato su "Automaticamente" o "al cursore di controllo".

Per attivare e disattivare questa funzione da qualsiasi luogo ci si trovi,, si prega di assegnare un gesto personalizzato utilizzando la [Finestra tasti e gesti di immissione](#InputGestures).

##### Lettura per paragrafi {#BrailleSettingsReadByParagraph}

Se attivata, il braille verrà visualizzato per paragrafi invece che per righe.
Inoltre, i comandi per spostarsi alla riga precedente/successiva andranno al paragrafo precedente/successivo.
Questo significa che non sarà necessario utilizzare lo scrolling ogni volta che ci si trova alla fine di una riga.
La lettura dovrebbe risultare più fluente in presenza di grosse porzioni di testo.
L'opzione risulta disabilitata da impostazioni predefinite.

##### Evita di spezzare le parole se possibile {#BrailleSettingsWordWrap}

Se abilitata, l'opzione farà in modo che parole troppo grandi non vengano spezzate su due righe del display braille.
Invece, vi sarà un po' di spazio vuoto verso la fine della barra.
Quando si sposterà il display alla riga successiva, sarà possibile leggere la parola per intero.
Talvolta questa funzione è chiamata a capo automatico.
Si noti che nel caso in cui la parola sia troppo grande per starci sul display, verrà per forza divisa.

Se invece la funzione è disabilitata, verrà mostrato il più possibile della parola, mentre il rimanente finirà sulla riga successiva.
Scorrendo il display, sarà possibile leggere il resto della parola.

L'attivazione di questa funzione permetterà una lettura molto più fluida, ma richiederà di scorrere il display braille molto più spesso.

##### Presentazione delle informazioni contestuali per il focus {#BrailleSettingsFocusContextPresentation}

Questa impostazione permette di stabilire quali informazioni di contesto NVDA mostrerà sul display braille quando un oggetto riceve il focus.
Le informazioni di contesto fanno riferimento alla gerarchia di oggetti che contengono il focus.
Per esempio, quando il focus si trova in un elemento di un elenco, quell'elemento è parte dell'elenco stesso.
Questo elenco a sua volta può essere contenuto all'interno di una finestra di dialogo, etc.
Si prega di consultare la sezione [Navigazione ad oggetti](#ObjectNavigation) per ulteriori informazioni sulla gerarchia che viene applicata agli oggetti in NVDA.

Quando questa opzione viene impostata su "riempi il display al cambiamento del contesto", NVDA cercherà di mostrare la maggior quantità possibile di informazioni di contesto sul Display Braille, ma soltanto per le parti di contesto che sono cambiate.
Ritornando all'esempio sopra esposto, questo significa che nel momento in cui il focus va a posizionarsi sull'elenco, NVDA mostrerà l'elemento dell'elenco sul display braille.
Inoltre, se vi è spazio sufficiente sulla barra braille, NVDA cercherà di mostrare che quell'elemento è parte di un elenco.
Se poi ci si inizia a spostare con le frecce all'interno dell'elenco, si presume che l'utente sia perfettamente consapevole di trovarsi all'interno dell'elenco.
Per cui, per gli altri elementi dell'elenco che verranno focalizzati, NVDA mostrerà soltanto il nome di questi elementi, senza ulteriori informazioni.
Se si desidera rileggere le informazioni di contesto nuovamente (ossia che ci si trova all'interno di un elenco che a sua volta è contenuto in una finestra di dialogo), è necessario scorrere indietro con il display braille.

Quando invece questa opzione è impostata su "riempi sempre il display", NVDA cercherà di mostrare la maggior quantità possibile di informazioni di contesto sulla barra braille, senza tener conto del fatto che queste informazioni sono già state presentate all'utente.
Questo comporta un vantaggio, ossia che NVDA riempirà sempre il display con il maggior numero di informazioni possibile.
Lo svantaggio è che la posizione iniziale del focus sul display braille sarà sempre diversa rispetto alla posizione del dito.
Potrebbe quindi risultare complicato gestire un numero elevato di elementi, in quanto è sempre necessario spostare di continuo il dito per individuare la posizione iniziale dell'elemento.
Questo è stato il comportamento predefinito in NVDA fino alla versione 2017.2.

Se invece si imposta l'opzione di presentazione delle informazioni di contesto su "solo scorrendo indietro", NVDA non mostrerà mai alcun tipo di informazione di contesto.
Così, sempre riferendosi all'esempio di prima, NVDA visualizzerà che è stato focalizzato un elemento di un elenco.
Comunque, se si desidera leggere il contesto (ossia che ci si trova in un elenco e che tale elenco fa parte di una finestra di dialogo), sarà necessario scorrere il proprio display braille indietro.

Per modificare la presentazione delle informazioni di contesto da qualsiasi punto ci si trovi, è necessario assegnare un nuovo gesto o tasto rapido utilizzando la [finestra di dialogo tasti e gesti di immissione](#InputGestures).

##### Interrompi la voce durante lo scorrimento {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Predefinito (Attivato), Attivato, Disattivato|
|Predefinito |Attivato|

Questa impostazione determina se la sintesi vocale debba interrompersi quando si scorre il display braille indietro o avanti..
I comandi riga precedente/successiva interrompono sempre la sintesi.

Per alcune persone la voce che legge di continuo potrebbe essere fonte di distrazione se si è concentrati sul braille.
Per questo motivo l'opzione è abilitata di default, interrompendo il parlato durante lo scorrimento del braille.

La disattivazione di questa opzione consente di ascoltare la sintesi indipendentemente dallo scorrimento del display braille.

##### Mostra selezione {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Default (Attivato), Attivato, disattivato|
|Default |Attivato|

Questa impostazione determina se l'indicatore di selezione (punti 7 e 8) debba essere visualizzato nel display braille.
L'opzione è abilitata per impostazione predefinita, quindi viene visualizzato l'indicatore di selezione.
L'indicatore di selezione potrebbe essere una distrazione durante la lettura.
La disattivazione di questa opzione può migliorare la leggibilità.

Per attivare o disattivare i punti 7 e 8 per la selezione da qualsiasi posto, si prega di assegnare un gesto personalizzato utilizzando la [finestra di dialogo tasti e gesti di immissione](#InputGestures).

#### Selezione display braille {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Apri la finestra di dialogo Seleziona display Braille {#OpenSelectBrailleDisplay}

Tasto: `NVDA+control+a`

La finestra di dialogo Selezione display Braille, che si apre tramite il pulsante "cambia..." nella categoria Braille delle impostazioni di NVDA, permette di scegliere quale barra braille NVDA dovrà usare.
Una volta selezionato il proprio display braille, premere OK per fare in modo che NVDA lo carichi e si possa iniziare ad utilizzarlo.
Se si verifica un errore durante il caricamento della barra braille, NVDA avviserà l'utente con un messaggio per poi continuare ad usare quella precedente, se esistente.

##### Display Braille {#SelectBrailleDisplayDisplay}

Si tratta di una casella combinata formata da svariati elementi, a seconda dei driver installati sul proprio sistema. 
Spostarsi con le frecce verticali per selezionarne uno.

L'opzione "automatico" consente a NVDA di cercare in background la presenza di un gran numero di modelli di Display Braille.
Quando questa funzione è abilitata e si collega un display supportato tramite USB o Bluetooth, NVDA si connetterà automaticamente a quel display.

Nessun display braille significa che non si sta utilizzando il Braille.

Si veda la sezione [Display Braille supportati](#SupportedBrailleDisplays) per maggiori informazioni sui modelli disponibili e su quali è possibile servirsi della rilevazione automatica.

##### Display da rilevare automaticamente {#SelectBrailleDisplayAutoDetect}

Quando display braille è impostato su "Automatico", le caselle di controllo in questo elenco consentono di abilitare e disabilitare i driver che saranno coinvolti nel processo di rilevamento automatico.
Ciò consente di escludere i driver di barre braille che non si utilizzano regolarmente.
Ad esempio, se si possiede solo un display che richiede il funzionamento del driver Baum, si può abilitare soltanto quello, disabilitando gli altri in modo da velocizzare e migliorare le operazioni di rilevamento.

Per impostazione predefinita, tutti i driver che supportano il rilevamento automatico sono abilitati.
Anche qualsiasi nuovo driver, proveniente ad esempio da una nuova versione di NVDA o da un componente aggiuntivo, sarà abilitato per impostazione predefinita.

è possibile consultare la documentazione del proprio display Braille nella sezione [Display Braille supportati](#SupportedBrailleDisplays) per verificare se il modello supporta il rilevamento automatico. 

##### Porta {#SelectBrailleDisplayPort}

Questa opzione, se disponibile, permette di scegliere la porta, oppure il tipo di connessione da utilizzare per comunicare con il display braille selezionato.
Si tratta di una casella combinata che contiene le scelte possibili riferite al proprio display braille.

Per impostazioni predefinite, NVDA supporta il riconoscimento automatico della porta, il che significa che la connessione con il dispositivo braille sarà stabilita automaticamente tramite la scansione dei dispositivi presenti nel sistema via USB e Bluetooth.
Comunque, per alcuni display braille, sarà anche possibile stabilire manualmente la porta da utilizzare.
Le opzioni più comuni sono "automatica", per far sì che NVDA stabilisca da solo la porta esatta da utilizzare, "USB", "bluetooth", e seriale, se il display braille supporta questo tipo di comunicazione.

Quest'ultima opzione non sarà disponibile se il display braille supporta soltanto il riconoscimento automatico delle porte.

Si consiglia di consultare la documentazione presente nella sezione [Display braille supportati](#SupportedBrailleDisplays) per avere maggiori informazioni sulle porte e le connessioni disponibili per il display braille che si sta utilizzando.

Nota: se si collegano contemporaneamente al computer più display Braille che utilizzano lo stesso driver (ad es. due display braille Seika),
risulta attualmente impossibile far sapere a NVDA quale display usare.
Pertanto si consiglia di collegare al pc un solo Display Braille di un determinato tipo/produttore alla volta.

#### Audio {#AudioSettings}

<!-- KC:setting -->

##### Apri impostazioni audio {#OpenAudioSettings}

Tasto: `NVDA+control+u`

La categoria Audio nella finestra di dialogo Impostazioni NVDA contiene opzioni che consentono di modificare diversi aspetti della periferica audio di uscita.

##### Periferica audio da utilizzare {#SelectSynthesizerOutputDevice}

Questa opzione permette di selezionare la scheda audio che NVDA utilizzerà per mandare i messaggi al sintetizzatore.

<!-- KC:setting -->

##### Modalità attenuazione audio {#SelectSynthesizerDuckingMode}

Tasto: `NVDA+shift+d`

Questa funzione consente di decidere se NVDA debba abbassare il volume delle altre applicazioni quando NVDA sta parlando, o per tutto il tempo in cui NVDA è in esecuzione.

* Nessuna attenuazione: NVDA non abbasserà mai il volume di altre applicazioni.
* Attenua quando vengono riprodotti altri suoni: NVDA abbasserà il volume di altri flussi audio soltanto quando la sintesi vocale sta parlando. Si noti che potrebbe non funzionare per tutti i sintetizzatori.
* Attenua sempre: NVDA manterrà gli altri flussi audio sempre con un volume più basso per tutto il tempo in cui NVDA è in esecuzione.

Questa funzione è disponibile soltanto se NVDA è stato installato nel sistema.
Non è possibile supportare l'attenuazione audio in versioni portable o temporanee di NVDA.

##### Il volume dei suoni di NVDA segue il volume della voce {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Disattivato, Attivato|
|Predefinito |Disattivato|

Quando questa opzione è abilitata, il volume dei suoni e dei segnali acustici di NVDA seguirà l'impostazione del volume della voce in uso.
Se si riduce il volume della voce, anche il volume dei suoni diminuirà.
Allo stesso modo, se si aumenta il volume della voce, aumenterà anche quello dei suoni..
Inoltre, ha effetto solo quando l'impostazione [Usa WASAPI per l'output audio](#WASAPI) è abilitata.

##### Volume dei suoni di NVDA {#SoundVolume}

Questo cursore di avanzamento consente di impostare il volume dei suoni e dei segnali acustici di NVDA.
L'impostazione ha effetto solo quando l'opzione "Il volume dei suoni di NVDA segue il volume della voce" è disabilitata.
La funzione non risulta disponibile se NVDA è stato avviato con l'impostazione [WASAPI disattivato per l'uscita audio](#WASAPI) nelle Impostazioni avanzate.

##### bilanciamento audio {#SelectSoundSplitMode}

La funzione di bilanciamento audio consente agli utenti di utilizzare i propri dispositivi di uscita stereo, come cuffie e altoparlanti.
In questo modo, si potrà portare la voce di NVDA in un canale (ad esempio sinistro) e tutte le altre applicazioni nell'altro canale (ad esempio destro).
Per impostazione predefinita la funzione di bilanciamento audio è disabilitata, il che significa che tutte le applicazioni, incluso NVDA, riprodurranno i suoni sia sul canale sinistro che su quello destro.
Un gesto consente di passare tra le varie modalità di bilanciamento audio:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Passa tra le modalità di bilanciamento audio |`NVDA+alt+s` |Passa tra le modalità di bilanciamento audio.|

<!-- KC:endInclude -->

Per impostazione predefinita, questo comando passerà tra le seguenti modalità:

* bilanciamento disattivato: sia NVDA che altre applicazioni trasmettono l'audio ai canali sinistro e destro.
* NVDA a sinistra e applicazioni a destra: NVDA parlerà nel canale sinistro, mentre le altre applicazioni riprodurranno i suoni nel canale destro.
* NVDA a sinistra e applicazioni su entrambe i canali: NVDA parlerà nel canale sinistro, mentre le altre applicazioni riprodurranno i suoni sia nel canale sinistro che destro.

Sono disponibili modalità di bilanciamento audio più avanzate nella casella combinata delle impostazioni NVDA.
Tra queste, una menzione particolare merita l'opzione "NVDA in entrambi i canali e applicazioni in entrambi i canali", che impone che tutti i suoni siano diretti su entrambi i canali.
Tale funzione si comporta in maniera differente rispetto a "bilanciamento disattivato", nel caso in cui altre elaborazioni audio interferiscano con i volumi dei canali.

Tenere sempre presente che la modalità bilanciamento audio di NVDA non è un mixer..
Ad esempio, se un'applicazione riproduce una traccia stereo, e il bilanciamento è configurato con "NVDA a sinistra e applicazioni a destra", si ascolterà solo il canale destro della traccia audio, mentre il canale sinistro rimarrà dedicato a NVDA..

Questa opzione non risulta disponibile se NVDA è stato avviato con [Usa Wasapi per l'output audio](#WASAPI) disabilitato nelle impostazioni avanzate.

Inoltre, prestare attenzione al fatto che se NVDA si arresta in modo anomalo, non sarà in grado di ripristinare il volume dei suoni dell'applicazione, per cui l'audio continuerebbe ad essere riprodotto in un solo canale.
Per mitigare questo problema, riavviare NVDA.

##### Personalizzazione delle modalità di bilanciamento audio {#CustomizeSoundSplitModes}

Questo elenco di caselle di controllo permette di selezionare quali modalità di bilanciamento audio saranno disponibili tramite il comando `NVDA+alt+s`.
Le modalità deselezionate saranno escluse.
Per impostazioni predefinite, sono incluse solo tre modalità.

* Bilanciamento audio disabilitato: NVDA e le applicazioni riproducono suoni sia nei canali sinistro che destro.
* NVDA sul canale sinistro e tutte le altre applicazioni sul canale destro.
* NVDA sul canale sinistro e tutte le altre applicazioni su entrambe i canali.

Tenere presente che è necessario selezionare almeno una modalità.
Questa opzione non risulta disponibile se NVDA è stato avviato con [Usa Wasapi per l'output audio](#WASAPI) disabilitato nelle impostazioni avanzate.

##### Tempo di funzionamento del dispositivo audio dopo la sintesi {#AudioAwakeTime}

Questo campo editazione specifica per quanto tempo NVDA mantiene attivo il dispositivo audio dopo che la sintesi ha parlato.
Ciò consente a NVDA di evitare alcuni problemi con la sintesi vocale, come la perdita di parti di parole.
Questo può accadere perché i dispositivi audio (in particolare Bluetooth e wireless) entrano in modalità standby.
La funzione potrebbe essere utile anche in altri casi d'uso, come quando si esegue NVDA all'interno di una macchina virtuale (ad esempio Citrix Virtual Desktop) o su alcuni laptop.

Valori più bassi potrebbero causare interruzioni dell'audio più frequenti, poiché il dispositivo tenderà ad entrare in modalità standby troppo presto, tagliando l'inizio della frase successiva.
Invece, impostare un valore troppo alto potrebbe portare allo scaricamento più veloce della batteria del dispositivo audio, poiché rimarrà attivo più a lungo anche quando non viene emesso alcun suono.

È possibile impostare il tempo su zero per disabilitare questa funzione.

#### Visione {#VisionSettings}

La categoria visione nelle impostazioni di NVDA consente di attivare, disattivare e configurare i [miglioramenti visivi](#Vision).

Si noti che le opzioni disponibili in questa categoria possono essere estese dai [Componenti aggiuntivi di NVDA](#AddonsManager).
Per impostazione predefinita, questa categoria di impostazioni contiene le seguenti opzioni:

##### Evidenziatore del Focus {#VisionSettingsFocusHighlight}

Le caselle di controllo presenti in questo gruppo di opzioni attivano o disattivano le funzionalità interne dell'[Evidenziatore focus](#VisionFocusHighlight).

* Abilita evidenziazione: attiva o disattiva l'evidenziazione del focus.
* Evidenzia Focus di sistema: attiva o disattiva l'evidenziazione del [focus di sistema](#SystemFocus).
* Evidenzia navigatore ad oggetti: attiva o disattiva l'evidenziazione del [navigatore ad oggetti](#ObjectNavigation).
* Evidenzia il cursore in modalità navigazione: attiva o disattiva l'evidenziazione del [cursore virtuale in modalità navigazione](#BrowseMode)

Si noti che selezionando e deselezionando la casella di controllo principale "Abilita evidenziazione", si cambierà anche lo stato delle altre tre caselle di controllo.
Va da sé che se la casella di controllo è disattivata e la si attiva, verranno attivate anche le altre tre.
Se si desidera abilitare soltanto il focus e mantenere disabilitato il navigatore ad oggetti e il cursore virtuale, lo stato della casella di controllo "abilita evidenziazione" risulterà parzialmente attivato.

##### Tenda Schermo {#VisionSettingsScreenCurtain}

è possibile attivare la [Tenda Schermo](#VisionScreenCurtain) selezionando la "casella di controllo Rendi lo schermo nero (effetto immediato).
Verrà visualizzato un avviso che lo schermo diventerà nero dopo l'attivazione.
Prima di continuare (selezionando "Sì"), assicurarsi di aver abilitato la sintesi vocale o il display braille, di essere insomma in grado di controllare il computer senza l'aiuto dello schermo.
Selezionare "No" se non si desidera più abilitare la tenda schermo.
Se si è sicuri, scegliere il pulsante Sì per abilitare la tenda schermo.
Nel caso in cui non si desideri essere avvisati con questo messaggio tutte le volte, è possibile modificare questo comportamento nella stessa finestra di dialogo.
Se invece si volesse ripristinare la visualizzazione del messaggio, attivare la casella di controllo che si trova vicina all'opzione "Rendi lo schermo nero (effetto immediato".

Per impostazioni predefinite, viene emesso un segnale acustico all'attivazione o disattivazione della tenda schermo.
Se si desidera modificare questo comportamento, è sufficiente deselezionare la casella di controllo "Riproduci un suono quando si attiva o disattiva la tenda schermo".

##### Impostazioni per miglioramenti visivi di terze parti {#VisionSettingsThirdPartyVisualAids}

in NVDA si possono aggiungere ulteriori miglioramenti visivi tramite [i componenti aggiuntivi](#AddonsManager).
Nel caso in cui siano presenti impostazioni regolabili, esse verranno visualizzate in questa sezione, nel gruppo dedicato a quel determinato miglioramento visivo.
Fare riferimento alla documentazione del miglioramento visivo in merito alla spiegazioni delle sue impostazioni.

#### Tastiera {#KeyboardSettings}

<!-- KC:setting -->

##### Apri impostazioni tastiera {#OpenKeyboardSettings}

Tasto: `NVDA+control+k`

La categoria impostazioni tastiera della finestra impostazioni di NVDA contiene opzioni che modificano il comportamento dello screen reader quando l'utente digita i caratteri sulla tastiera.
Questa categoria Contiene le seguenti opzioni:

##### Layout tastiera {#KeyboardSettingsLayout}

Questa casella combinata permette di selezionare quale layout di tastiera NVDA debba utilizzare. Al momento è possibile scegliere tra desktop e laptop, ossia tra tastiere per pc fissi e portatili.

##### Seleziona il tasto funzione NVDA {#KeyboardSettingsModifiers}

Le caselle di controllo presenti in questo elenco consentono di stabilire quali tasti debbano essere usati come [Tasti funzione di NVDA](#TheNVDAModifierKey). è possibile scegliere tra le seguenti possibilità:

* Il tasto blocca maiuscole
* Il tasto insert del tastierino numerico
* Il tasto insert della tastiera estesa (in genere situato nel gruppo di sei tasti vicino a inizio e fine)

Se non viene selezionato alcun tasto che agisca come tasto NVDA, potrebbe risultare impossibile accedere ad alcuni comandi dello screen reader, perciò è necessario impostarne almeno uno.

<!-- KC:setting -->

##### Leggi i caratteri digitati {#KeyboardSettingsSpeakTypedCharacters}

Tasto: NVDA+2

Una casella di controllo che, se attivata, fa in modo che NVDA pronunci tutti i caratteri che vengono digitati sulla tastiera.

<!-- KC:setting -->

##### Leggi le parole digitate {#KeyboardSettingsSpeakTypedWords}

Tasto: NVDA+3

Una casella di controllo che, se attivata, fa in modo che NVDA pronunci tutte le parole che vengono digitate sulla tastiera.

##### I caratteri digitati interrompono la voce {#KeyboardSettingsSpeechInteruptForCharacters}

Questa opzione, se attiva, interrompe la lettura della sintesi vocale non appena viene premuto un tasto. L'opzione è attivata di default.

##### Il tasto invio interrompe la voce {#KeyboardSettingsSpeechInteruptForEnter}

Questa opzione, se attiva, interrompe la lettura della sintesi vocale non appena viene premuto il tasto invio. L'opzione è attivata di default.

##### Consentire navigazione rapida in modalità dire tutto {#KeyboardSettingsSkimReading}

Se attivata, alcuni tasti di navigazione (ad esempio i comandi di navigazione rapida nei browser, oppure lo spostarsi per righe o paragrafi) non fermeranno più la lettura, che continuerà dalla nuova posizione raggiunta.

##### Emetti un beep alla scrittura di lettere minuscole quando il tasto blocca maiuscole è attivo {#KeyboardSettingsBeepLowercase}

Quando abilitato, si udirà un segnale acustico ogni qualvolta verrà digitata una lettera assieme al tasto Shift (maiuscolo) quando il blocca maiuscole è attivo.
In genere, scrivere le lettere con il tasto Shift mentre la funzione di Blocca Maiuscole è attivata non è prassi comune e si presume sia non intenzionale, magari perché ci si è scordati di averla abilitata in precedenza.
In ogni caso, può essere d'aiuto saperlo.

<!-- KC:setting -->

##### Leggi i tasti di comando {#KeyboardSettingsSpeakCommandKeys}

Tasto: NVDA+4

Una casella di controllo che, se attivata, fa in modo che NVDA pronunci tutte le combinazioni di tasti che non siano singoli caratteri che vengono digitati, ad esempio premendo il tasto control seguito da una lettera.

##### Riproduci un suono in caso di errori di ortografia mentre si scrive {#KeyboardSettingsAlertForSpellingErrors}

Se attivata, verrà emesso un segnale acustico nel caso in cui la parola che si è terminato di scrivere contenga un errore di ortografia.
Questa funzione risulta disponibile soltanto se l'opzione Leggi errori di ortografia è attivata nella finestra di NVDA [Impostazioni formattazione documento](#DocumentFormattingSettings).

##### Gestisci tasti da altre applicazioni {#KeyboardSettingsHandleKeys}

Quest'opzione permette all'utente di controllare se le pressioni di tasti, generate da programmi che si basano sul riconoscimento vocale o sulle tastiere a schermo, debbano essere processate da NVDA.
L'opzione risulta attiva di default, sebbene alcuni utenti che utilizzano la lingua di immissione Vietnamita dovrebbero disattivare questa funzione nel caso si servano del software di scrittura Unikey.

#### Mouse {#MouseSettings}

<!-- KC:setting -->

##### Apri impostazioni mouse {#OpenMouseSettings}

Tasto: `NVDA+control+m`

La categoria Mouse della finestra impostazioni di NVDA permette di attivare o meno il tracciamento del mouse, ascoltarne la posizione con segnali audio e altre opzioni aggiuntive.
Contiene le seguenti opzioni:

##### Leggi i cambiamenti del puntatore del mouse {#MouseSettingsShape}

Una casella di controllo che, se attivata, istruisce NVDA ad annunciare i cambiamenti dell'aspetto del puntatore. 
In Windows il puntatore può cambiare forma in concomitanza con certi eventi, ad esempio in presenza di campi editazione o durante il caricamento di un'applicazione, etc.

<!-- KC:setting -->

##### Abilita tracciamento del mouse {#MouseSettingsTracking}

Tasto: NVDA+m

Una casella di controllo che, se attivata, istruisce NVDA ad annunciare il testo sul quale è posizionato il puntatore, mentre ci si sposta con esso sullo schermo. Questo permette di individuare gli elementi con una rappresentazione fisica e reale su come essi siano disposti sul video, piuttosto che utilizzare la navigazione ad oggetti.

##### Parte di testo letta {#MouseSettingsTextUnit}

Se NVDA è configurato per annunciare il testo man mano che si sposta il Mouse, questa opzione permette di stabilire la quantità di testo che verrà vocalizzato dallo Screen Reader. 
Le scelte disponibili sono Carattere, Parola, riga e Paragrafo.

Per modificare la quantità di testo letta da qualsiasi punto ci si trovi, si prega di assegnare un gesto personalizzato usando la [finestra di dialogo Tasti e gesti di immissione](#InputGestures).

##### Leggi l'oggetto sotto il mouse {#MouseSettingsRole}

Se questa casella di controllo è attivata, NVDA leggerà le informazioni sugli oggetti man mano che il mouse si sposta al loro interno.
Ciò comprende il ruolo (tipo) dell'oggetto nonché gli stati (selezionato/premuto), le coordinate delle celle nelle tabelle, ecc.
Tenere presente che la lettura di alcuni dettagli dell'oggetto potrebbe dipendere da come sono regolate altre impostazioni, ad esempio nelle categorie [presentazione oggetti](#ObjectPresentationSettings) o [Formattazione documento](#DocumentFormattingSettings).

##### Coordinate audio quando il mouse si sposta {#MouseSettingsAudio}

Attivando questa casella di controllo si farà in modo che NVDA emetta dei segnali acustici man mano che il mouse si sposta, in modo che l'utente possa farsi un'idea della sua posizione in relazione allo schermo.
Più in alto è la posizione del mouse sullo schermo, più acuti saranno i toni dei beep emessi.
Spostando il mouse a sinistra o a destra si otterrà lo spostamento del suono nelle direzioni corrispondenti sugli altoparlanti, a patto che si abbiano a disposizione degli altoparlanti stereo.

##### La luminosità controlla il volume delle coordinate audio {#MouseSettingsBrightness}

Se la casella di controllo "coordinate audio quando il mouse si sposta" è attiva, allora, attivando quest'opzione, il volume dei beep delle coordinate audio è controllato dal livello di luminosità dello schermo, riferito alla posizione attuale del mouse. 
Questa caratteristica viene disattivata di default.

##### Ignora il mouse se gestito da altre applicazioni {#MouseSettingsHandleMouseControl}

Questa funzione permette all'utente di non tener conto dei movimenti del mouse (sia i movimenti che i bottoni premuti) generati da altre applicazioni quali TeamViewer o software di controllo remoto.
La caratteristica viene disattivata di default.
Se si attiva questa opzione e la funzione "abilita tracciamento del mouse" risulta attivata, NVDA non leggerà più ciò che si trova alla posizione del mouse quando esso viene spostato da altre applicazioni.

#### Impostazioni per il tocco {#TouchInteraction}

Questa categoria, disponibile soltanto nei computer con un touch screen a bordo, consente di stabilire come NVDA debba interagire con tale touch screen.
Contiene le seguenti opzioni:

##### Attiva supporto al tocco {#TouchSupportEnable}

Questa casella di controllo attiva il supporto al tocco da parte di NVDA.
Se abilitata, è possibile servirsi delle dita per navigare e interagire con gli elementi sullo schermo utilizzando un dispositivo touchscreen.
Se disabilitata, il supporto del touchscreen verrà disattivato come se NVDA non fosse in esecuzione.
Questa impostazione può anche essere attivata / disattivata utilizzando NVDA + control + alt + t.

##### Modalità di digitazione a tocco {#TouchTypingMode}

Questa casella di controllo permette di specificare il metodo da usare quando si desidera inserire del testo tramite una tastiera a tocco, o tastiera virtuale.
Se la casella è attivata, allora sarà sufficiente rilasciare il dito dalla posizione corrente per inserire la lettera appena individuata.
Se invece la si lascia disattivata, per inserire il carattere stabilito bisogna effettuare un doppio tap su di esso.

#### Cursore di Controllo {#ReviewCursorSettings}

Questa categoria determina il comportamento del cursore di controllo in svariati aspetti.
Contiene le seguenti opzioni:

<!-- KC:setting -->

##### Segue il focus della tastiera {#ReviewCursorFollowFocus}

Tasto: NVDA+7 |

Quando questa casella di controllo è attiva, il cursore di controllo verrà sempre posizionato sul medesimo oggetto del focus di sistema man mano che esso cambia.

<!-- KC:setting -->

##### Segue Cursore di sistema {#ReviewCursorFollowCaret}

Tasto: NVDA+6

Quando questa casella di controllo è attiva, il cursore di controllo verrà automaticamente spostato alla posizione del cursore di sistema man mano che esso si sposta.

##### Segue il Mouse {#ReviewCursorFollowMouse}

Quando questa casella di controllo è attiva, il cursore di controllo seguirà il mouse man mano che si sposta.

##### Modalità semplice {#ReviewCursorSimple}

Quando questa casella di controllo è attiva, NVDA filtrerà la gerarchia di oggetti che possono essere raggiunti col navigatore ad oggetti, in modo da escludere oggetti di poco interesse per l'utente; ad esempio, oggetti invisibili o che sono usati esclusivamente per il layout.

Per abilitare o disabilitare la modalità semplice da qualsiasi punto ci si trovi, assegnare un gesto personalizzato servendosi della [finestra gesti e tasti di immissione](#InputGestures).

#### Presentazione oggetti {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Apri le impostazioni presentazione oggetti {#OpenObjectPresentationSettings}

Tasto: `NVDA+control+o`

La categoria presentazione oggetti delle impostazioni di NVDA è utilizzata per impostare la quantità di informazioni che dovranno essere fornite in merito ai controlli quali descrizione, informazioni sulla posizione, e così via.
Queste opzioni in genere non si applicano alla modalità di navigazione.
Esse si riferiscono agli annunci inerenti il focus e la navigazione ad oggetti di NVDA, ma non alla lettura del testo, come può avvenire per le modalità usate sul web che implicano l'uso del cursore virtuale.

##### Leggi i suggerimenti {#ObjectPresentationReportToolTips}

Una casella di controllo che, se attivata, istruisce NVDA ad annunciare i suggerimenti man mano che appaiono.
Molte finestre o controlli visualizzano dei messaggi o suggerimenti quando si sposta il mouse o il focus su di essi, NVDA non farà altro che vocalizzarli.

##### Annuncia notifiche {#ObjectPresentationReportNotifications}

Questa casella di controllo, se attivata, istruisce NVDA ad annunciare i fumetti d'aiuto e le notifiche a scomparsa quando appaiono. 

* I fumetti assomigliano ai suggerimenti (tool-tips), ma in genere sono più larghi come dimensioni e vengono associati ad eventi di sistema come ad esempio il collegamento o scollegamento di un cavo di rete oppure avvisi inerenti la sicurezza.
* Le notifiche a scomparsa sono state introdotte in Windows10 e appaiono nel centro notifiche del system tray, informando su diversi eventi (ad es. se è stato scaricato un aggiornamento, se è arrivata una nuova e-mail nella posta in arrivo, ecc.).

##### Leggi i tasti di scelta rapida degli oggetti {#ObjectPresentationShortcutKeys}

Quando questa casella di controllo è attivata, NVDA pronuncerà il tasto caldo dell'oggetto o del controllo focalizzato. 
Ad esempio, molti menu sono forniti di scorciatoie, tanto per citarne una delle più comuni, il menu file è spesso accompagnato dalla scorciatoia alt+f.

##### Leggi informazioni sulla posizione dell'oggetto {#ObjectPresentationPositionInfo}

Questa casella di controllo permette di stabilire se si desideri che NVDA riporti le informazioni sulla posizione dell'oggetto, ad esempio 1 di 4, 2 di 4, etc quando ci si sposta con il cursore di sistema o con il navigatore ad oggetti.

##### Tenta di indovinare le informazioni sulla posizione dell'oggetto quando non sono disponibili {#ObjectPresentationGuessPositionInfo}

Se questa impostazione viene attivata, NVDA cercherà di individuare le informazioni sulla posizione degli oggetti quando esse non risultano disponibili per un determinato controllo.

Se attiva, NVDA annuncerà informazioni sulla posizione di molti controlli come barre dei menu o barre degli strumenti, ma si tenga presente che potrebbero rivelarsi poco precise. 

##### Leggi le descrizioni degli oggetti {#ObjectPresentationReportDescriptions}

Disattivare questa casella di controllo se non si desidera ascoltare la descrizione degli oggetti.

<!-- KC:setting -->

##### Aggiornamento barre di avanzamento {#ObjectPresentationProgressBarOutput}

Tasto: NVDA+u |

Quest'opzione è costituita da una casella ad elenco la cui funzione è controllare la modalità con la quale NVDA informerà l'utente sullo stato delle barre di avanzamento. 

Contiene i seguenti valori:

* Disattivato: Lo stato delle barre di avanzamento non verrà riportato.
* Leggi: NVDA annuncerà la percentuale dello stato delle barre di avanzamento, riportandone il valore in base al loro grado di avanzamento.
* Emetti un Beep: NVDA emetterà un segnale acustico in concomitanza dei cambiamenti delle barre di avanzamento. Più acuto sarà il beep, più sarà vicina la barra di avanzamento alla sua fase di completamento.
* Leggi ed emetti un beep: selezionando questa opzione, NVDA emetterà segnali acustici e annuncerà allo stesso tempo la percentuale dello stato di avanzamento delle barre di avanzamento.

##### Leggi le barre di avanzamento in Background {#ObjectPresentationReportBackgroundProgressBars}

Si tratta di una casella di controllo che, se attivata, istruisce NVDA a continuare a fornire informazioni sulle barre di avanzamento che non sono fisicamente in primo piano sullo schermo. 
Se ad esempio un'applicazione che contiene una barra di avanzamento viene minimizzata, o semplicemente si cambia finestra lavorando quindi con un altro programma, NVDA continuerà a fornire informazioni sull'avanzamento della barra di avanzamento dell'applicazione precedente, permettendo nel frattempo di svolgere altre attività.

<!-- KC:setting -->

##### Leggi i cambiamenti dei contenuti dinamici {#ObjectPresentationReportDynamicContent}

Tasto: NVDA+5

Permette di attivare o disattivare la lettura di alcuni contenuti, in particolare nelle applicazioni che fanno uso di terminali o la cronologia delle chat.

##### Emette un beep alla comparsa di suggerimenti automatici {#ObjectPresentationSuggestionSounds}

Attiva o disattiva l'annuncio dei suggerimenti automatici, e se attivato, verrà emesso un segnale acustico da NVDA per indicarne la presenza.
I suggerimenti automatici sono elenchi di valori suggeriti in base a ciò che è stato scritto in determinati campi editazione o documenti.
Ad esempio, quando si inserisce del testo nel campo di ricerca del menu avvio presente da Windows Vista in poi, Windows visualizza una serie di suggerimenti basati su ciò che è stato digitato.
Per alcuni campi editazione come i campi di ricerca presenti in varie app di Windows10, NVDA notificherà la presenza di un elenco di suggerimenti che appare quando si digita il testo.
L'elenco dei suggerimenti automatici si chiuderà non appena ci si sposta dal campo editazione corrente, e per alcuni campi, NVDA sarà in grado di avvertire l'utente.

#### composizione nell'immissione {#InputCompositionSettings}

Questa categoria permette di controllare la modalità con cui NVDA annuncia la composizione di caratteri asiatici, come IME o servizi di immissione testo.
Si noti che a causa delle grandi differenze esistenti nelle caratteristiche disponibili per ciascun metodo di immissione, è caldamente consigliato configurare tutte le opzioni in maniera accurata per ciascun servizio di immissione, in modo da ottenere le prestazioni migliori.

##### Annuncia automaticamente tutti i caratteri suggeriti {#InputCompositionReportAllCandidates}

Questa opzione, attivata di default, permette di stabilire se debbano essere annunciati tutti i suggerimenti visibili, quando appare un elenco di questi elementi.
risulta molto utile mantenere questa impostazione attiva specie per i tipi di immissione pittografici come il nuovo Cinese ChangJie, o Boshiami, in quanto si possono ascoltare automaticamente tutti i simboli e i loro numeri, permettendo poi di scegliere uno di questi.
Comunque, per i metodi d'immissione fonetica ad esempio del nuovo cinese, può essere conveniente disattivare questa impostazione, in quanto tutti i simboli hanno il medesimo suono e si è costretti ad utilizzare le frecce per esplorarli ed ottenere maggiori informazioni dalla descrizione del carattere di ciascun suggerimento.

##### Leggi suggerimento selezionato {#InputCompositionAnnounceSelectedCandidate}

Questa opzione, attiva di default, permette di stabilire se NVDA debba leggere il suggerimento selezionato quando appare un'elenco di caratteri o quando la selezione viene modificata.
Questo risulta necessario per quei metodi di immissione laddove la selezione può essere modificata con le frecce (come il Chinese New Phonetic), ma per altri metodi di immissione può essere più conveniente scrivere disattivando questa opzione.
Si noti che il cursore di controllo verrà comunque posizionato sul carattere suggerito, perciò sarà sempre possibile utilizzare tutti i comandi relativi alla navigazione ad oggetti.

##### Includi sempre una breve descrizione del carattere durante la lettura dei suggerimenti {#InputCompositionCandidateIncludesShortCharacterDescription}

questa opzione, attiva di default, permette di stabilire se NVDA debba fornire una breve descrizione per ciascun carattere suggerito, sia se viene selezionato, sia se viene letto quando appare il suggerimento.
si noti che per alcune lingue come il cinese, tale opzione non ha effetto.
Risulta invece molto utile per coreano e giapponese.

##### Annuncia i cambiamenti alla stringa di lettura {#InputCompositionReadingStringChanges}

Alcuni metodi di immissione come il nuovo cinese fonetico o il ChangJie hanno una stringa di lettura (talvolta conosciuta come stringa di precomposizione).
è possibile stabilire se NVDA debba annunciare o meno i caratteri che compaiono in questo tipo di stringhe.
Questa opzione è attiva da impostazioni predefinite.
Si noti che alcuni vecchi metodi di composizione come il cinese ChangJie potrebbero non faruso della stringa di lettura, ma usare invece la stringa di composizione diretta. Si veda l'opzione successiva per maggiori informazioni.

##### Annuncia i cambiamenti alla stringa di composizione {#InputCompositionCompositionStringChanges}

Dopo che i dati di precomposizione sono stati associati ad un simbolo pittografico, la maggior parte dei metodi di composizione mette questo simbolo in una stringa di composizione per salvare temporaneamente il contenuto assieme ad altri simboli prima che essi siano inseriti definitivamente nel documento.
Questa opzione permette di stabilire se NVDA debba o meno annunciare i nuovi simboli man mano che compaiono nella stringa di composizione.
L'opzione è attiva di default.

#### Modalità navigazione {#BrowseModeSettings}

<!-- KC:setting -->

##### Apri impostazioni modalità navigazione {#OpenBrowseModeSettings}

Tasto: `NVDA+control+b`

Questa categoria di impostazioni consente di stabilire come NVDA si debba comportare nella navigazione ed esplorazione di documenti o pagine complesse, come ad esempio le pagine web.
Contiene le seguenti opzioni:

##### Numero massimo di caratteri per riga {#BrowseModeSettingsMaxLength}

Questo campo imposta la lunghezza massima di una riga in caratteri quando si utilizza il buffer virtuale.

##### Numero di righe per pagina {#BrowseModeSettingsPageLines}

Sebbene il buffer virtuale non sia costituito da pagine, questo campo modifica il numero di righe assegnato quando ci si deve spostare con i tasti pagina su e pagina giù.

<!-- KC:setting -->

##### Usa il layout dello schermo, quando supportato {#BrowseModeSettingsScreenLayout}

Tasto: NVDA+v

Questa opzione consente di specificare se, in modalità navigazione, elementi quali pulsanti, link e campi debbano occupare un'unica riga o se debbano mantenere per quanto possibile il flusso di testo più simile alla visualizzazione reale.
Tenere presente che questa opzione non si applica alle app di Microsoft Office come Outlook e Word, che utilizzano sempre il layout dello schermo.
In sostanza, se la casella di controllo viene attivata, tali elementi vengono presentati all'utente esattamente come essi sono visualizzati sullo schermo.
Ad esempio, una riga che visivamente è formata da più collegamenti verrà presentata in braille o tramite sintesi vocale con tutti i link nella stessa riga.
Se invece la casella di controllo è disattivata, ciascun elemento sarà posto in una riga differente.
Questo per alcuni utenti si traduce in una navigazione più comoda ma meno simile alla disposizione reale degli oggetti.

##### Attiva modalità navigazione al caricamento della pagina {#BrowseModeSettingsEnableOnPageLoad}

Questa casella abilita o disabilita la modalità navigazione automatica al caricamento di una pagina.
Quando questa opzione è disabilitata, la modalità di navigazione può ancora essere attivata manualmente sulle pagine o nei documenti in cui essa è supportata.
Si veda la [sezione modalità navigazione](#BrowseMode) per l'elenco delle applicazioni compatibili.
è importante tener presente che questa opzione non si applica alle situazioni in cui la modalità di navigazione è sempre facoltativa, ad es. in Microsoft Word.
Risulta attiva da impostazioni predefinite.

##### Dire tutto Automaticamente al caricamento di una pagina web {#BrowseModeSettingsAutoSayAll}

Questa casella di controllo commuta la lettura automatica delle pagine web una volta caricate.
Essa risulta attiva da impostazioni predefinite.

##### leggi le tabelle di layout {#BrowseModeSettingsIncludeLayoutTables}

Questa opzione ha effetto su come NVDA debba gestire le tabelle utilizzate esclusivamente a scopo di impaginazione.
Quando la casella di controllo è attiva, NVDA le tratterà come tabelle normali, annunciandole secondo le impostazioni [formattazione documento](#DocumentFormattingSettings) e individuandole con i tasti di navigazione veloce.
Quando è disattiva, non verranno annunciate né individuate con la navigazione veloce.
In ogni caso, il contenuto delle tabelle sarà comunque annunciato come testo normale.
Questa opzione è disattivata di default.

Per poter cambiare al volo la lettura delle tabelle di layout da qualsiasi parte ci si trovi, si prega di assegnare un gesto personalizzato utilizzando la [finestra gesti personalizzati](#InputGestures).

##### Configurare l'annuncio di campi come link e intestazioni {#BrowseModeLinksAndHeadings}

Si vedano le opzioni della sezione [Impostazioni formato documento](#DocumentFormattingSettings) alla finestra di dialogo [Inpostazioni NVDA](#NVDASettings) per configurare i campi che verranno annunciati quando si naviga, come link, intestazioni e tabelle

##### Modalità focus automatica per i cambiamenti del focus {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Questa opzione permette l'attivazione della modalità di inseguimento del focus non appena si raggiunge un apposito campo, ad esempio un campo editazione. 
In sostanza, quando ci si trova in una pagina web e premiamo il tasto tab, se l'elemento successivo è un campo appartenente ad un form e questa opzione è attivata, la modalità focus verrà attivata automaticamente, disattivando temporaneamente il buffer virtuale.

##### Modalità focus automatica per i movimenti del cursore {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Quest'opzione, quando attivata, permette a NVDA di abilitare/disabilitare la modalità focus quando si utilizzano i tasti freccia.
Per esempio, se si naviga in una pagina web e, scorrendo con il cursore, si incontra un campo editazione, NVDA attiverà subito la modalità focus, permettendo quindi in questa circostanza di scrivere del testo.
Se si continua a scorrere la pagina web con le frecce e si esce dal campo editazione, NVDA ripristinerà la modalità navigazione.

##### indicazione audio delle modalità focus e buffer virtuale {#BrowseModeSettingsPassThroughAudioIndication}

Attivando questa casella di controllo, NVDA emetterà dei segnali acustici al passaggio tra la modalità navigazione e la modalità focus, piuttosto che annunciarli a parole.

##### Inibisci tutti i gesti che non rappresentano un comando {#BrowseModeSettingsTrapNonCommandGestures}

Attivata da impostazioni predefinite, questa funzione permette di stabilire se, ai gesti (come le pressioni di un tasto) che non rappresentano comandi di NVDA e non sono considerati tasti caldi in generale, debba essere impedito di raggiungere il documento sul quale è posizionato il focus.
Ad esempio, se abilitata, premendo la lettera "j", a questa verrebbe impedito di raggiungere il documento, nonostante non sia un comando veloce di navigazione o possa essere un comando dell'applicazione stessa.
Ogni qualvolta questo accade, Windows emetterà un suono predefinito di avviso.

<!-- KC:setting -->

##### Spostamento automatico del focus sugli elementi raggiungibili durante la navigazione {#BrowseModeSettingsAutoFocusFocusableElements}

Tasto: NVDA+8

Disabilitata per impostazione predefinita, questa opzione consente di scegliere se il focus di sistema debba essere impostato automaticamente su elementi raggiungibili dal focus stesso (collegamenti, campi modulo, ecc.) quando si utilizza la modalità navigazione.
Lasciando l'impostazione disattiva, si farà in modo che questi elementi non saranno più attivati quando vengono selezionati con il cursore virtuale..
Ciò potrebbe comportare un'esperienza di navigazione più rapida e una migliore reattività in modalità di navigazione.
Il focus verrà ancora aggiornato sull'elemento quando si interagisce con esso (ad esempio premendo un pulsante, selezionando una casella di controllo).
L'abilitazione di questa opzione può migliorare il supporto per alcuni siti Web a scapito delle prestazioni e della stabilità.

#### Formato documento {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Apri Impostazioni formattazione documento {#OpenDocumentFormattingSettings}

Tasto: `NVDA+control+d`

la maggior parte delle opzioni in questa categoria servono a configurare quali informazioni inerente la formattazione NVDA dovrà pronunciare quando si scorre un documento con le frecce. 
Ad esempio, se attiviamo la casella di controllo "Leggi il nome del font", NVDA annuncerà tale cambiamento ogni qualvolta se ne incontrerà uno, muovendosi con i tasti cursore in un documento.

Le opzioni di formattazione documento sono divise in gruppi.
è possibile configurare la lettura automatica dei seguenti elementi:

* Carattere 
  * nome carattere
  * dimensione carattere
  * attributi carattere
  * Apici e pedici
  * Testo enfatizzato
  * Evidenziato (testo contrassegnato)
  * Stile
  * Colori
* Informazioni documento
  * Commenti
  * Segnalibri
  * Revisioni
  * Errori ortografici
* Pagine e spaziatura
  * Numeri di pagina
  * Numeri di riga
  * Annuncio rientro righe [(disattivo, voce, toni, voce e toni)](#DocumentFormattingSettingsLineIndentation)
  * Ignora righe vuote nel segnalare i rientri
  * Rientro paragrafi (ad esempio rientro prima riga)
  * Spaziatura righe (singola, doppia etc)
  * Allineamento
* Informazioni tabella
  * tabelle
  * intestazioni riga/colonna (disattivato, righe, colonne, righe e colonne)
  * Coordinate delle celle delle tabelle
  * Bordi delle celle [(Disattivo, stili, sia colori che stili)
* Elementi
  * collegamenti
  * intestazioni
  * Grafici
  * elenchi
  * Blocchi tra virgolette
  * Punti di riferimento
  * Gruppi
  * Articoli
  * Frame
  * Figure e didascalie
  * Quando qualcosa è cliccabile

Per modificare queste impostazioni da qualsiasi luogo ci si trovi, servirsi della finestra [tasti e gesti di immissione](#InputGestures) ed assegnare un gesto o tasto rapido personalizzato per quella funzione.

##### Notifica cambiamenti di formattazione dopo il cursore {#DocumentFormattingDetectFormatAfterCursor}

Se abilitata, questa impostazione istruisce NVDA a intercettare tutti i cambiamenti di formattazione in una riga e a leggerli, anche se questo porerà ad un rallentamento nelle prestazioni di NVDA.

Da impostazioni predefinite, NVDA ricava le informazioni di formattazione dalla posizione del cursore di sistema / cursore di controllo, ed in alcune circostanze può riuscire ad intercettare i cambiamenti di formattazione nell'intera riga, a patto che questo non vada a causare un rallentamento dello Screen Reader.

Abilitare questa opzione quando si vogliono correggere documenti e si usano applicazioni come Wordpad, dove la formattazione risulta importante.

##### Annuncia rientro righe {#DocumentFormattingSettingsLineIndentation}

Questa opzione consente di configurare come NVDA debba annunciare i rientri all'inizio delle righe.
La casella combinata "annuncia rientro righe con," è costituita da quattro opzioni:

* Disattivato: NVDA non tratterà i rientri righe in modo speciale.
* Voce: se è selezionata l'opzione voce, man mano che i rientri aumentano, NVDA dirà qualcosa tipo "dodici spazi" o "quattro tab."
* Beep: se è selezionato beep, man mano che i rientri aumentano, dei beep indicheranno il quantitativo di cambiamenti dei rientri.
Il segnale acustico aumenterà di altezza ad ogni spazio, mentre per una tabulazione, aumenterà in altezza per l'equivalente di quattro spazi.
* Sia voce che beep: con questa opzione attiva i rientri saranno letti utilizzando entrambi i metodi spiegati sopra.

Se si seleziona la casella di controllo "Ignora le righe vuote nel segnalare i rientri", i cambiamenti per i rientri non saranno annunciati per le righe vuote.
Ciò può essere utile quando si legge un documento in cui vengono utilizzate righe vuote per separare blocchi di testo rientrati, come nel codice sorgente di programmazione.

#### Navigazione documento {#DocumentNavigation}

Questa categoria consente di regolare vari aspetti della navigazione del documento.

##### Stile Paragrafo {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Predefinito (Gestito dall'applicazione), Gestito dall'applicazione, Interruzione riga singola, Interruzione di più righe|
|Predefinito |Gestito dall'applicazione|

Questa casella combinata permette di selezionare lo stile del paragrafo da utilizzare quando si naviga tra gli stessi tramite `control+freccia su` e `control+freccia giù`.
Gli stili di paragrafo disponibili sono:

* Gestito dall'applicazione: NVDA consentirà all'applicazione di determinare il paragrafo precedente o successivo; conseguentemente lo screen reader leggerà il nuovo paragrafo durante la navigazione.
Questo stile funziona al meglio quando l'applicazione supporta nativamente la navigazione tra paragrafi ed è l'impostazione predefinita.
* Interruzione riga singola: NVDA tenterà di determinare il paragrafo precedente o successivo utilizzando un'interruzione di una sola riga come indicatore di paragrafo.
Questo stile funziona meglio quando si leggono documenti in un'applicazione che non supporta nativamente la navigazione tra paragrafi, e i paragrafi nel documento sono contrassegnati da una singola pressione del `tasto invio`.
* Interruzione di più righe: NVDA tenterà di determinare il paragrafo precedente o successivo utilizzando almeno una riga vuota (due pressioni del tasto `invio`) come indicatore di paragrafo.
Questo stile funziona meglio quando si lavora con documenti che utilizzano paragrafi a blocchi.
Si noti che questo stile di paragrafo non può essere utilizzato in Microsoft Word o Microsoft Outlook, a meno che non si utilizzi UIA per accedere ai controlli di Microsoft Word.

è possibile passare tra gli stili di paragrafo disponibili da qualsiasi luogo assegnando una combinazione di tasti nella finestra [Tasti e gesti di immissione](#InputGestures).

#### OCR Windows {#Win10OcrSettings}

Questa categoria di impostazioni permette di configurare [l'OCR di Windows](#Win10Ocr).
Contiene le seguenti opzioni:

##### Lingua di riconoscimento {#Win10OcrSettingsRecognitionLanguage}

Questa casella combinata permette di scegliere la lingua da utilizzare per il riconoscimento del testo.
Per scorrere tra le lingue disponibili ovunque ci si trovi, assegnare un gesto personalizzato utilizzando la [finestra di dialogo Gesti e tasti di immissione](#InputGestures).

##### Aggiorna periodicamente il contenuto riconosciuto {#Win10OcrSettingsAutoRefresh}

Quando questa casella è abilitata, NVDA aggiornerà automaticamente il contenuto riconosciuto non appena si verifica un cambiamento nell'area di riconoscimento.
Ciò può essere molto utile quando si desidera monitorare contenuti in continua evoluzione, ad esempio un video con i sottotitoli.
L'aggiornamento avviene ogni secondo e mezzo.
Questa opzione è disabilitata di default.

#### Impostazioni avanzate {#AdvancedSettings}

Attenzione! Le impostazioni in questa categoria sono per utenti esperti e potrebbero causare il mancato funzionamento di NVDA se configurate in modo errato.
Si prega di modificare i vari parametri solo nel caso in cui si sono ricevute istruzioni da uno sviluppatore oppure se si è perfettamente consapevoli di ciò che si sta facendo.

##### Modificare le impostazioni avanzate {#AdvancedSettingsMakingChanges}

Se si desidera effettuare cambiamenti alle impostazioni avanzate, è necessario prima di tutto selezionare la casella di controllo specifica, "Sono consapevole che la modifica di queste impostazioni potrebbe causare il malfunzionamento di NVDA".

##### Ritornare alle impostazioni predefinite {#AdvancedSettingsRestoringDefaults}

Il pulsante ripristinerà i valori predefiniti per le impostazioni, anche se la casella di controllo di conferma non è selezionata.
Dopo aver modificato le impostazioni, si potrebbe voler ripristinare i valori predefiniti.
Ciò può anche essere utile nel caso in cui non si è sicuri se si siano effettuati cambiamenti o meno.

##### Consenti il caricamento di moduli in sviluppo dalla cartella Scratchpad {#AdvancedSettingsEnableScratchpad}

Quando si sviluppano componenti aggiuntivi per NVDA, è utile poter testare il codice man mano che lo si scrive.
Se la funzione è attivata, NVDA sarà in grado di caricare app module personalizzati, globalPlugins, brailleDisplayDrivers, servizi di miglioramento visivo e synthDrivers da una cartella speciale di sviluppo chiamata scratchpad, situata all'interno della cartella impostazioni utente di NVDA.
Come accade per gli addon, questi moduli vengono caricati all'avvio di NVDA oppure, nel caso di appModules e globalPlugins, al [ricaricamento dei plugin](#ReloadPlugins).
La funzionalità risulta disattivata di default, di modo che NVDA non eseguirà mai codice personalizzato senza che l'utente ne sia consapevole.
Se si desidera distribuire codice personalizzato ad altri, è necessario creare un pacchetto in formato nvda-addon ed utilizzare le funzioni messe a disposizione per i componenti aggiuntivi.

##### Apri la cartella scratchpad dello sviluppatore {#AdvancedSettingsOpenScratchpadDir}

Questo pulsante apre la cartella all'interno della quale è possibile inserire il codice personalizzato mentre si sviluppa.
Il bottone risulta attivo solo nel caso in cui NVDA sia configurato per caricare codice personalizzato dalla cartella scratchpad dello sviluppatore.

##### Registrazione per eventi UI Automation e cambiamenti di proprietà {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Automatica, Selettiva, Globale|
|Default |Automatica|

Questa opzione modifica il modo in cui NVDA registra gli eventi attivati dall'API di accessibilità di Microsoft UI Automation.
La casella combinata "Registrazione per eventi UI Automation e cambiamenti di proprietà" contiene tre opzioni:

* Automatica: "selettiva" per Windows 11 Sun Valley 2 (versione 22H2) e successive, altrimenti "globale".
* Selettiva: NVDA si limiterà a tener conto degli eventi UIA che riguardano unicamente il focus.
Nel caso in cui si riscontrino problemi di stabilità o di prestazioni, si consiglia di attivare la funzione per vedere se il problema può risolversi.
Tuttavia, nelle versioni più vecchie di Windows, NVDA potrebbe avere problemi a seguire il focus in alcuni controlli (come il task manager e il pannello emoji).
* Globale: NVDA terrà traccia di molti eventi UIA, che per lo più sono gestiti e scartati da NVDA stesso.
Sebbene la gestione del focus risulti più affidabile, questo può risultare molto dispendioso in termini di risorse soprattutto in applicazioni quali Microsoft Visual Studio.

##### Utilizza UI Automation per accedere ai controlli dei documenti Microsoft Word {#MSWordUIA}

Stabilisce se NVDA debba utilizzare o meno l'API di accessibilità UI Automation per accedere ai documenti di Microsoft Word, anziché il vecchio modello a oggetti precedente.
Questo vale per i documenti in Microsoft Word stesso, oltre ai messaggi in Microsoft Outlook.
Questa impostazione contiene i seguenti valori:

* Predefinito (se appropriato)
* Solo quando necessario: nel caso in cui il modello ad oggetti di Word non sia disponibile in nessuna circostanza
* Ove opportuno: Microsoft Word version 16.0.15000 o superiore, o nel caso in cui il modello ad oggetti di Word non è disponibile
* Sempre: ovunque sia disponibile la tecnologia UI automation in Microsoft word (non importa quanto completa).

##### Utilizza UI Automation per accedere ai controlli dei fogli di calcolo di Microsoft Excel quando disponibile {#UseUiaForExcel}

Quando questa opzione è abilitata, NVDA proverà ad utilizzare le API di accessibilità di Microsoft UI Automation per recuperare le informazioni dai controlli del foglio di calcolo di Microsoft Excel.
Si tratta di una funzionalità sperimentale e alcune caratteristiche di Microsoft Excel potrebbero non essere disponibili in questa modalità.
Per esempio, non si potrà usare l'elenco elementi di formule e commenti, oltre alla capacità di saltare rapidamente nei campi modulo in modalità navigazione.
Tuttavia, per l'esplorazione e la modifica di base del foglio di calcolo, questa opzione può fornire un notevole miglioramento delle prestazioni.
Al momento è consigliabile per la maggior parte degli utenti di non attivare questa funzione sperimentale, tuttavia sono ben accetti i feedback di quelle persone che dispongono della versione di Microsoft Excel build 16.0.13522.10000 o superiore.
L'implementazione di Ui automation in Excel è in costante fase di modifica, perciò le versioni di Office inferiori alla 16.0.13522.10000 potrebbero non fornire informazioni sufficienti.

##### Utilizza l'elaborazione avanzata degli eventi {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Predefinito (Attivato), Disattivato, Attivato|
|Predefinito |Attivato|

Quando questa opzione è abilitata, NVDA dovrebbe rimanere reattivo anche quando viene letteralmente sommerso da molti eventi di UI Automation, ad es. grandi quantità di testo in un terminale.
Dopo aver modificato questa opzione, sarà necessario riavviare NVDA affinché la modifica abbia effetto.

##### Supporto alla Console di Windows {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Automatico, UIA se disponibile, Meno recenti|
|Default |Automatico|

Questa opzione permette di selezionare la modalità con cui NVDA interagisce con la console di Windows utilizzata dal prompt dei comandi, PowerShell e il sottosistema Windows per Linux.
Non influisce sul più moderno Terminale di Windows.
In Windows 10 versione 1709, Microsoft [ha aggiunto il supporto per la sua UI Automation API alla console](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), offrendo prestazioni e stabilità notevolmente migliorate per gli screen reader che lo supportano.
Nelle situazioni in cui l'interfaccia UIA non risulti disponibile oppure offra un'esperienza utente non soddisfacente, NVDA passerà automaticamente al supporto più vecchio per le console..
La casella combinata supporto di Windows Console ha tre opzioni:

* Automatico: Utilizza UIA Automation nella versione di Windows Console inclusa con Windows 11 versione 22H2 e successive.
Questa opzione è consigliata e impostata per impostazione predefinita.
* UIA quando disponibile: Utilizza UI Automation nella console se disponibile, anche per versioni incompatibili o con bug conosciuti..
Sebbene questa funzionalità limitata possa essere utile (e sufficiente per un utilizzo standard), l'uso di questa opzione è interamente a proprio rischio e non verrà fornito alcun supporto per essa.
* Meno recente: verrà completamente disabilitato l'uso di UI Automation nella console di Windows..
Si tenga presente che in questo modo il supporto a UI Automation non verrà mai usato, anche quando l'esperienza utente sarebbe migliore.
Pertanto, la selezione di questa opzione non è consigliata a meno che non si sappia ciò che si sta facendo.

##### Utilizza UIA con Microsoft Edge e altri Browser basati su Chromium quando disponibile {#ChromiumUIA}

Consente di specificare se servirsi della tecnologia UIA quando disponibile nei browser basati su Chromium come Microsoft Edge.
Il supporto UIA per i browser basati su Chromium è in fase di sviluppo e potrebbe non fornire lo stesso livello di accessibilità di IA2.
Nella casella combinata sono presenti le opzioni seguenti:

* Predefinito (Solo se necessario): è al momento l'impostazione di default per NVDA. è possibile che con l'avanzare della tecnologia l'impostazione potrà essere modificata in futuro.
* Solo se necessario: nel caso in cui NVDA non riesca ad avvalersi delle risorse fornite dalla tecnologia IA2 per il browser, lo screen reader passerà a UIA, se disponibile..
* Sì: Se il browser rende disponibile la tecnologia UIA, NVDA la utilizzerà da subito..
* No: Non verrà mai utilizzata UIA, anche quando NVDA non sarà in grado di agganciarsi al processo attivo. Ciò può essere utile per gli sviluppatori che eseguono il debug di problemi con IA2 e vogliano essere certi che NVDA non si serva di UIA.

##### Annotazioni {#Annotations}

Questo gruppo di opzioni viene utilizzato per abilitare le funzionalità che aggiungono il supporto sperimentale per le annotazioni ARIA.
Alcune di queste funzionalità potrebbero essere incomplete.

<!-- KC:beginInclude -->
Per "Leggere il riassunto di tutti i dettagli di un'annnotazione alla posizione del cursore di sistema", premere NVDA+d.
<!-- KC:endInclude -->

Sono disponibili le seguenti opzioni:

* "Annuncia 'con dettagli' per le annotazioni strutturate": ne abilita la segnalazione qualora il testo o il controllo contenga ulteriori dettagli.
* "Annuncia sempre descrizioni-aria":
  Quando la fonte di `accDescription` è aria-description, viene sempre annunciata la descrizione.
  Questo è utile per le annotazioni sul web.
  Nota:
  * Ci sono molte fonti per `accDescription`, molte hanno una semantica mista o inaffidabile.
    Storicamente AT non è stato in grado di differenziare le fonti di `accDescription`, in genere non venivano pronunciate a causa della semantica mista.
  * Questa opzione è in fase di sviluppo molto prematuro, si basa su funzionalità del browser non ancora ampiamente disponibili.
  * Ci si aspetta un funzionamento completo con Chromium 92.0.4479.0+

##### Segnala regioni live {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Default (Attivato), Disattivato, Attivato|
|Default |Attivato|

Questa opzione stabilisce se NVDA debba segnalare i cambiamenti in alcuni contenuti web dinamici in Braille.
Disabilitare questa opzione equivale al tornare al comportamento di NVDA nelle versioni 2023.1 e precedenti, che riportava questi cambiamenti di contenuto solo in voce.

##### Leggi password in tutti i terminali avanzati {#AdvancedSettingsWinConsoleSpeakPasswords}

Questa impostazione controlla il comportamento di due funzioni di NVDA, ossia [Leggi i caratteri digitati](#KeyboardSettingsSpeakTypedCharacters) e [leggi le parole digitate](#KeyboardSettingsSpeakTypedWords) in situazioni in cui lo schermo non si aggiorna, per esempio durante l'immissione di password nel prompt dei comandi con il supporto UI Automation attivo o Mintty.
Per motivi di sicurezza, questa impostazione dovrebbe essere lasciata disabilitata.
Tuttavia, è possibile abilitarla se si verificano problemi di prestazioni o instabilità con la digitazione di caratteri e / o parole durante l'utilizzo del nuovo supporto sperimentale di NVDA alla Console.

##### Utilizza il nuovo supporto ai caratteri digitati nelle Console meno recenti di Windows quando disponibile {#AdvancedSettingsKeyboardSupportInLegacy}

Questa opzione attiva un metodo alternativo per la rilevazione dei caratteri digitati nelle console di Windows meno recenti.
Se da un lato migliora sensibilmente le prestazioni e previene alcuni errori di gestione del testo, può risultare non compatibile con alcuni programmi di terminale.
Questa funzionalità è disponibile e abilitata per impostazione predefinita nelle versioni di Windows 10 1607 e successive quando UI Automation non è disponibile o è disabilitata.
Attenzione: con questa opzione abilitata, i caratteri digitati che non compaiono sullo schermo, come le password, verranno letti ugualmente.
In ambienti non sicuri, è preferibile disattivare temporaneamente [Leggi i caratteri digitati](#KeyboardSettingsSpeakTypedCharacters) e [leggi le parole digitate](#KeyboardSettingsSpeakTypedWords) durante l'inserimento di password.

##### Algoritmo Diff {#DiffAlgo}

Questa impostazione controlla il modo in cui NVDA tratta il nuovo testo da pronunciare nel terminale.
La casella combinata algoritmo Diff contiene tre opzioni:

* Automatico: Questa opzione fa sì che NVDA utilizzi Diff Match Patch nella maggior parte delle situazioni, ma si serva di Difflib in applicazioni problematiche, come le versioni precedenti di Windows Console e Mintty.
* Diff Match Patch: Questa opzione fa in modo che NVDA calcoli le modifiche al testo del terminale in base al carattere, anche in quelle situazioni in cui non è consigliato.
Può migliorare le prestazioni quando vengono scritti grandi volumi di testo sulla console e consentire una segnalazione più accurata delle modifiche apportate a metà delle righe.
Tuttavia, potrebbe essere incompatibile con alcune applicazioni, con la lettura del testo che potrebbe risultare frammentaria o intermittente.
* Difflib: questa opzione fa in modo che NVDA calcoli le modifiche al testo del terminale per riga, anche in quelle situazioni in cui non è consigliato.
È identico al comportamento di NVDA nelle versioni 2020.4 e precedenti.
Questa impostazione può rendere più stabile la lettura del testo in arrivo per alcune applicazioni.
Tuttavia, nei terminali, quando si inserisce o si elimina un carattere nel mezzo di una riga, verrà sempre letto anche il testo situato dopo il cursore.

##### Leggi nuovo testo in Windows Terminal tramite {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Default (Diffing), Diffing, Notifiche UIA|
|Predefinito |Diffing|

Questa opzione determina il metodo utilizzato da NVDA per stabilire quale testo risulti "nuovo" (e quindi cosa pronunciare quando l'opzione "Leggi i cambiamenti dei contenuti dinamici" è abilitata) nella finestra del terminale di Windows e nel controllo WPF Windows Terminal utilizzato in Visual Studio 2022.
Non influisce sulla console di Windows (`conhost.exe`).
La casella combinata Leggi nuovo testo nel terminale di Windows ha tre opzioni:

* Default: Questa opzione è attualmente equivalente a "diffing", ma si prevede che verrà cambiata una volta sviluppato ulteriormente il supporto per le notifiche UIA.
* Diffing: Questa opzione utilizza l'algoritmo diff selezionato per calcolare le modifiche ogni volta che il terminale esegue il rendering di un nuovo testo.
Questo risulta identico al comportamento di NVDA nelle versioni 2022.4 e precedenti.
* Notifiche UIA: Questa opzione lascia il compito di gestire cosa dovrà essere letto al terminale di Windows stesso, il che significa che NVDA non dovrà più controllare e calcolare quale testo risulti "nuovo" sullo schermo.
Ciò dovrebbe migliorare notevolmente le prestazioni e la stabilità di Windows Terminal, ma questa funzionalità non è ancora completa.
In particolare, quando questa opzione è selezionata, vengono letti i caratteri digitati che non sono visualizzati sullo schermo, come le password.
Inoltre, gli intervalli contigui di output di oltre 1.000 caratteri potrebbero non essere segnalati in modo accurato.

##### Tenta di non leggere informazioni obsolete concernenti il focus {#CancelExpiredFocusSpeech}

Questa funzione cerca di inibire la lettura di informazioni obsolete che riguardano il focus di sistema.
In particolare, lo spostamento rapido tra i messaggi in Gmail mentre si utilizza Chrome rischia di far leggere a NVDA informazioni non più accurate. Questa opzione cerca di risolvere il problema.
Questa funzionalità è attiva per impostazione predefinita a partire da NVDA 2021.1.

##### Timeout Movimento cursore (in MS) {#AdvancedSettingsCaretMoveTimeout}

Questa opzione consente di impostare per quanti millisecondi NVDA dovrà attendere un movimento del cursore nei campi editazione.
Se ci si rende conto che NVDA sembra aver difficoltà nel seguire il cursore (ad esempio è sempre un carattere indietro oppure ripete la stessa riga), si può provare ad aumentare questo valore.

##### Annuncia trasparenza per i colori {#ReportTransparentColors}

Questa opzione consente di segnalare quando i colori sono trasparenti, utile per gli sviluppatori di addon/appModule che raccolgono informazioni per migliorare l'esperienza dell'utente con un'applicazione di terze parti.
Alcune applicazioni GDI evidenzieranno il testo con un colore di sfondo, NVDA (tramite l'intercettatore video) tenta di leggere questo colore.
In alcuni casi, lo sfondo del testo potrebbe essere completamente trasparente, con il testo sovrapposto a qualche altro elemento della GUI.
Con diverse API GUI storicamente popolari, il testo può essere visualizzato con uno sfondo trasparente, ma visivamente il colore di sfondo è accurato.

##### Usa WASAPI per l'output audio {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Opzioni |Default (Disattivato), Disattivato, Attivato|
|Default |Disattivato|

Questa opzione attiva la gestione dell'audio attraverso un sistema chiamato Windows Audio Session API (WASAPI).
WASAPI è un framework audio più moderno che può migliorare la reattività, le prestazioni e la stabilità dell'audio di NVDA, compresi sia il parlato che i suoni.
Dopo aver modificato questa opzione, sarà necessario riavviare NVDA affinché i cambiamenti abbiano effetto.
Se si disattiva il supporto a Wasapi, anche le seguenti opzioni verranno disabilitate:

* [Il volume dei suoni di NVDA segue il volume della voce](#SoundVolumeFollowsVoice)
* [Volume dei suoni di NVDA](#SoundVolume)

##### Categorie Debug Logging {#AdvancedSettingsDebugLoggingCategories}

Le caselle di controllo presenti in questo elenco consentono di abilitare categorie specifiche di messaggi log di NVDA.
Si tenga presente che il log di questi messaggi può comportare un calo delle prestazioni e file di registro di grandi dimensioni.
Attivare quindi le caselle di controllo soltanto se viene richiesto da uno sviluppatore.

##### Riproduci un suono per gli errori loggati {#PlayErrorSound}

Questa opzione consente di specificare se NVDA riprodurrà un suono di errore nel caso in cui venga registrato un errore.
Scegliendo Solo nelle versioni di prova (impostazione predefinita) viene emesso un suono di errore solo se la versione corrente di NVDA è una versione di prova (alpha, beta o eseguita dai sorgenti).
Scegliendo Sì, è possibile abilitare i suoni di errore qualunque sia la versione attuale di NVDA.

##### Espressione regolare per il rilevamento dei paragrafi di testo in modalità navigazione {#TextParagraphRegexEdit}

Questo campo consente agli utenti di personalizzare l'espressione regolare per rilevare i paragrafi di testo in modalità navigazione.
Il [comando di navigazione tra paragrafi di testo](#TextNavigationCommand) cerca i paragrafi corrispondenti a questa espressione regolare.

### Impostazioni varie {#MiscSettings}

Oltre alla finestra [Impostazioni NVDA](#NVDASettings), il sottomenu preferenze del menu di NVDA contiene molti altri elementi che sono elencati qui di seguito.

#### Dizionari {#SpeechDictionaries}

La voce Dizionari situata nel menu preferenze contiene delle finestre di dialogo che consentono all'utente di controllare il modo con cui NVDA pronuncia certe parole o frasi. 
Vi sono tre tipi differenti di Dizionari.
Essi sono:

* predefinito: Le regole in questo dizionario hanno effetto in qualsiasi circostanza.
* voce: Le regole di questo tipo di dizionario hanno effetto esclusivamente sulla voce in uso.
* Temporaneo: Le regole in questo dizionario hanno effetto in qualsiasi circostanza, ma soltanto per la sessione corrente di NVDA. Tali regole andranno perse non appena NVDA verrà chiuso o riavviato.

Per aprire questi dizionari da qualsiasi luogo ci si trovi, servirsi della finestra [tasti e gesti di immissione](#InputGestures) ed assegnare un gesto o tasto rapido personalizzato per quella funzione.

Tutte le finestre di dialogo contengono un elenco di regole che verrà utilizzato per processare il parlato. 
L'interfaccia comprende anche i bottoni aggiungi, modifica, rimuovi e rimuovi tutto.

Per aggiungere una nuova regola al dizionario, premere il bottone Aggiungi e compilare i campi che si presentano nella finestra di dialogo, dopodiché cliccare sul bottone ok. 
La regola appena creata sarà visualizzata all'interno dell'elenco regole.
Tuttavia, per essere sicuri che tale regola venga applicata, premere nuovamente il bottone OK quando si avrà terminato di inserire o modificare le regole. In questo modo si uscirà completamente dalla finestra di dialogo inerente i dizionari.

Le regole dei dizionari di NVDA permettono di modificare una stringa di caratteri in un'altra. 
Vediamo un semplice esempio, supponendo di voler fare in modo che, ogni qualvolta NVDA incontri la parola nebbia, pronunci la parola Uccello. 
Dopo aver premuto il bottone Aggiungi, scrivere la parola nebbia sul primo campo, chiamato voce, spostarsi con il tasto tab sul secondo campo chiamato voce in sostituzione, e scrivere la parola uccello. 
è possibile anche compilare il campo commento, per fornire una descrizione alla nostra regola, ad esempio cambio nebbia in uccello.

Si noti che in realtà le regole inerenti i dizionari possono essere molto più complesse di quella mostrata a titolo esemplificativo. 
Vi sono infatti alcune opzioni quando si compila una nuova regola, la prima, permette di distinguere tra maiuscole e minuscole.
Di default NVDA non effettua questa distinzione.

In fine, una serie di pulsanti radio consente di stabilire se l'occorrenza inserita debba essere valutata ovunque, oppure solo come parola intera, o se invece si tratta di un'espressione regolare.
Impostare questa opzione su parola intera significa che non verranno presi in esame porzioni di parola.
Questa condizione è soddisfatta se i caratteri immediatamente prima e dopo la parola sono qualcosa di diverso da una lettera, un numero o un carattere di sottolineatura o se non ci sono affatto caratteri.
Per tornare all'esempio precedente, se scrivessimo UccelloMarino, e abbiamo selezionato di prendere in esame soltanto le parole intere, questa stringa verrebbe scartata.

Le espressioni regolari sono strumenti molto potenti per manipolare porzioni di testo.
Esse non verranno trattate in questo manuale a causa della loro complessità.
Per un tutorial introduttivo, fare riferimento alla [Guida alle espressioni regolari di Python](https://docs.python.org/3.11/howto/regex.html).

#### Livello di punteggiatura/simboli {#SymbolPronunciation}

Questa finestra di dialogo permette di modificare il modo ed il livello in cui i segni di punteggiatura e altri simboli vengono annunciati.

Nel titolo della finestra verrà visualizzata anche la lingua per la quale si sta modificando la pronuncia dei simboli.
Si noti che questa finestra di dialogo rispetta le impostazioni dell'opzione "Considera attendibile la lingua della voce corrente nel processare caratteri e simboli", situata alla [categoria voce](#SpeechSettings) della [finestra Impostazioni NVDA](#NVDASettings); per esempio, verrà utilizzata la lingua della voce piuttosto che la lingua generale di NVDA, quando questa opzione è attiva.

Per modificare un simbolo, dapprima selezionarlo nell'elenco simboli.
è possibile filtrare i risultati inserendo il nome del simbolo o parte di esso all'interno del campo editazione filtra per.

* Il campo "voce in sostituzione" permette di cambiare il testo che deve essere pronunciato in corrispondenza di quel simbolo.
* Utilizzando il campo "livello", è possibile stabilire il livello più basso dal quale il simbolo dovrà essere annunciato (nessuno, qualcosa, molta o tutta)..
è anche possibile impostare il livello su carattere; in quel caso il simbolo non sarà mai annunciato indipendentemente dal livello simboli in uso, con le seguenti due eccezioni:
  * Durante la navigazione carattere per carattere.
  * Quando NVDA effettua lo spelling di un testo contenente quel simbolo.
* Il campo invia questo simbolo al sintetizzatore specifica le condizioni per cui  lo stesso simbolo debba essere processato dalla sintesi vocale, non tenendo conto quindi del testo in sostituzione.
Ciò risulta utile nel caso in cui il simbolo provochi una pausa o un'inflessione nella voce del sintetizzatore.
Ad esempio, una virgola provoca una pausa nel sintetizzatore.
Ci sono tre opzioni:
  * Mai: il simbolo non sarà mai inviato al sintetizzatore.
  * Sempre: il simbolo verrà sempre inviato al sintetizzatore.
  * Soltanto al di sotto del livello simboli: invia il simbolo solo se il livello configurato per i simboli è al di sotto di quello settato per il simbolo attuale.
  Ad esempio, si potrebbe fare in modo che il simbolo venga gestito con la propria sostituzione, quindi senza pause, per i livelli più alti, mentre verranno effettuate pause per i livelli inferiori.

è possibile aggiungere un nuovo simbolo servendosi del pulsante Aggiungi.
Nella finestra di dialogo che appare, inserire il simbolo e premere il pulsante Ok.
Poi, modificare i campi rimanenti secondo le proprie esigenze.

Sarà sempre possibile eliminare un simbolo aggiunto in precedenza tramite il pulsante "Rimuovi".

Una volta terminate le modifiche, premere il pulsante OK per salvare i cambiamenti oppure il bottone Annulla per annullare l'operazione.

Nel caso di simboli complessi, potrebbe essere necessario includere dei segnaposti nel campo In Sostituzione. Ad esempio, per una data, potremmo avere \1, \2 o \3, che poi saranno i vari componenti della data.
In ragione di questo, se appaiono delle vere barre inverse nel simbolo, dovranno necessariamente essere raddoppiate. Ad esempio, se vogliamo scrivere "a\b", dovremo raddoppiare la controbarra, scrivendo "a\\b".

#### Tasti e gesti di immissione {#InputGestures}

In questa finestra di dialogo, è possibile personalizzare i gesti di immissione quali tasti della tastiera, pulsanti di un display braille, etc, per i comandi di NVDA.

è importante notare che saranno mostrati e quindi applicabili soltanto i comandi appartenenti all'applicazione che si stava usando prima di aprire questa finestra di dialogo.
Ad esempio, se si volessero personalizzare i comandi relativi alla modalità navigazione, sarà necessario aprire la finestra di dialogo "tasti e gesti di immissione" mentre ci si trova in modalità navigazione.

La visualizzazione ad albero di questo elenco mostra tutti i comandi di NVDA applicabili, raggruppati per categorie.
è possibile filtrarli inserendo una o più parole del nome del comando nella casella editazione "filtra per".
Eventuali gesti associati a un comando sono elencati sotto il comando stesso.

Per aggiungere un gesto d'immissione per un comando, selezionare il comando e premere il pulsante Aggiungi.
Quindi, eseguire il gesto diimmissione che si desidera associare, ad esempio, premere un tasto sulla tastiera o un pulsante su un display braille.
Spesso, un gesto può essere interpretato in svariati modi.
Ad esempio, se viene premuto un tasto sulla tastiera, lo si potrebbe voler associare al layout desktop, oppure a quello laptop, o a entrambi.
In questo caso, viene visualizzato un menu che consente di selezionare l'opzione desiderata.

Per rimuovere un gesto da un comando, selezionare il gesto e premere il pulsante Rimuovi.

La categoria emulazione tasti di sistema contiene comandi di NVDA che simulano la tastiera fisica.
In sostanza, si può utilizzare questa funzione per gestire la tastiera del pc attraverso un display braille.
Per aggiungere un gesto di emulazione, selezionare la categoria emulazione tasti di sistema e premere il pulsante aggiungi.
Quindi, premere il tasto sulla tastiera che si desidera emulare.
Dopodiché, il tasto sarà disponibile nella categoria emulazione tasti di sistema e si potrà assegnargli un gesto di input come descritto sopra.

Nota:

* Ai tasti simulati deve essere assegnato un gesto , altrimenti andranno persi nella finestra di salvataggio/chiusura.
* Potrebbe non essere possibile mappare un gesto di immissione con tasto modificatore ad un tasto emulato senza modificatore. 
Per esempio, se vogliamo mappare al tasto `a` la combinazione emulata `ctrl-m`, il risultato finale potrebbe essere `ctrl-a`.

Al termine delle modifiche, premere il pulsante OK per salvarle, o il tasto Annulla per non modificare alcunché.

### Salvare e caricare la configurazione {#SavingAndReloading}

NVDA salva automaticamente le impostazioni correnti all'uscita.
Si noti che comunque è possibile modificare questo comportamento tramite l'opzione presente nelle impostazioni generali del menu preferenze.
Per salvare le impostazioni manualmente, scegliere la voce salva Configurazione dal menu di NVDA.

Se è stato commesso un errore nelle impostazioni e si desidera tornare indietro a quelle salvate in precedenza, scegliere la voce "torna alla configurazione salvata dal menu NVDA.
è anche possibile resettare le impostazioni ai valori predefiniti, scegliendo la voce "Ripristina la configurazione ai valori di fabbrica", presente sul menu principale di NVDA.

I seguenti tasti rapidi risultano molto utili:
<!-- KC:beginInclude -->

| Nome |Tasto Desktop |Tasto Laptop |Descrizione|
|---|---|---|---|
|Salva Configurazione |NVDA+Control+c |NVDA+Control+c |Salva la configurazione attuale in modo che non venga persa all'uscita da NVDA|
|Torna alla configurazione salvata |NVDA+Control+r |NVDA+Control+r |Ripristina la configurazione di NVDA risalente all'ultima volta che essa è stata salvata. Premere tre volte in rapida successione per ripristinare le impostazioni di configurazione predefinite|

<!-- KC:endInclude -->

### Profili di configurazione {#ConfigurationProfiles}

Talvolta, può accadere di aver bisogno di impostazioni differenti in base a cosa si stia usando o cosa si stia facendo.
Ad esempio, si potrebbe volere che NVDA legga i rientri mentre si sta modificando un documento, oppure annunci gli errori di ortografia durante la correzione.
NVDA permette di effettuare questo genere di operazioni tramite la funzione profili di configurazione.

Un profilo di configurazione contiene soltanto quelle impostazioni che sono state cambiate mentre si modificava il profilo.
La maggior parte delle impostazioni può essere modificata nei profili, ad eccezione di quelle nella categoria generale della finestra [Impostazioni NVDA](#NVDASettings), in quanto influiscono sul comportamento totale di NVDA.

I profili possono essere anche attivati manualmente, o da una finestra di dialogo oppure utilizzando gesti aggiuntivi personalizzati.
Inoltre essi possono venir attivati automaticamente nel caso si verifichino degli eventi, come l'apertura di un programma particolare.

#### Gestione di base {#ProfilesBasicManagement}

è possibile gestire i profili di configurazione attraverso la voce "profili di configurazione..." nel menu di NVDA.
è attivabile anche con un tasto caldo:
<!-- KC:beginInclude -->

* NVDA+control+p: Visualizza la finestra profili di configurazione.

<!-- KC:endInclude -->

Il primo controllo in questa finestra di dialogo è l'elenco profili dal quale è possibile selezionare uno dei profili disponibili.
Quando si apre la finestra di dialogo, viene selezionato il profilo che si sta modificando.
Vengono visualizzate anche ulteriori informazioni per i profili attivi, che indicano il relativo stato, se in fase di modifica, se vi sono eventi associati e se si tratta di un profilo manuale.

Per rinominare o eliminare un profilo, premere rispettivamente i pulsanti Rinomina o Elimina.

Premere il pulsante Chiudi per chiudere la finestra.

#### Creazione di un profilo {#ProfilesCreating}

Per creare un profilo, premere il pulsante Nuovo.

Nella finestra di dialogo Nuovo profilo, è possibile immettere un nome per il profilo stesso.
È anche possibile selezionare come dovrebbe essere utilizzato questo profilo.
Se si desidera utilizzarlo solo manualmente, selezionare Attivazione manuale, che è l'impostazione predefinita.
In caso contrario, selezionare un evento che dovrebbe attivare automaticamente questo profilo.
Per comodità, se non è stato immesso un nome per il profilo, esso sarà generato assieme all'evento che verrà associato.
Si veda [più sotto](#ConfigProfileTriggers) per ulteriori informazioni sugli eventi.

Premendo infine il pulsante OK, il profilo sarà creato, la finestra di dialogo chiusa, permettendo quindi la modifica del profilo stesso.

#### Attivazione manuale {#ConfigProfileManual}

È possibile attivare manualmente un profilo selezionandolo e premendo il pulsante attivazione manuale.
Una volta attivato, potranno essere attivati anche altri profili nel caso si verifichino eventi ad essi associati, ma qualsiasi impostazione presente nel profilo attivato manualmente sovrascrive e ha la precedenza rispetto agli altri.
Ad esempio, se un profilo è configurato per attivarsi con l'applicazione corrente e l'annuncio dei link è abilitato in quel profilo, ma non in quello attivato manualmente, i link non saranno letti.
Tuttavia, se è stata cambiata la voce nel profilo che si attiva automaticamente in base agli eventi, e quel parametro non è stato toccato nel profilo che si abilita in modo manuale, verrà regolarmente utilizzata la voce del profilo automatico.
Tutte le impostazioni modificate verranno salvate nel profilo attivato manualmente.
Per disattivare un profilo attivato manualmente, selezionarlo nella finestra di dialogo Profili di configurazione e premere il pulsante disattivazione manuale.

#### Eventi {#ConfigProfileTriggers}

La pressione del pulsante Eventi nella finestra di dialogo Profili di configurazione consente di modificare i profili che devono essere attivati automaticamente per vari eventi.

La lista Eventi mostra gli eventi disponibili, che sono i seguenti:

* Applicazione corrente: attivato quando si passa all'applicazione corrente.
* Dire tutto: attivato durante la lettura in modalità dire tutto.

Per cambiare il profilo che dovrebbe essere attivato automaticamente per un evento, selezionare l'evento e quindi scegliere il profilo desiderato dall'elenco Profili.
È possibile selezionare (configurazione normale) se non si desidera utilizzare alcun profilo.

Premere il pulsante Chiudi per tornare alla finestra di dialogo Profili di configurazione.

#### Modifica di un profilo {#ConfigProfileEditing}

Se è stato attivato manualmente un profilo, le impostazioni modificate verranno salvate per quel profilo.
In caso contrario, le impostazioni modificate verranno salvate nel profilo attivato automaticamente più di recente.
Ad esempio, se si è associato un profilo con l'applicazione Blocco note e si passa a Blocco note, le impostazioni modificate verranno salvate per quel profilo.
Infine, se non vi è né un profilo attivato manualmente, né uno attivato con eventi, le impostazioni modificate vengono salvate nella configurazione normale.

Per modificare il profilo associato alla modalità dire tutto, è necessario [attivare manualmente](#ConfigProfileManual) quel profilo.

#### Disattivazione temporanea degli eventi {#ConfigProfileDisablingTriggers}

Talvolta, può risultare utile disattivare tutti gli eventi.
Ad esempio, si potrebbe voler modificare un profilo attivato manualmente o la configurazione generale di NVDA senza che gli eventi interferiscano.
è possibile farlo marcando la casella di controllo Disattiva temporaneamente tutti gli eventi nella finestra di dialogo Profili di configurazione.

Per fare in modo che gli eventi possano essere disabilitati da qualsiasi posto, si prega di assegnare un gesto o una combinazione di tasti personalizzata nella [Finestra gesti di immissione](#InputGestures).

#### Attivare un profilo utilizzando gesti di immissione {#ConfigProfileGestures}

Per ogni profilo che si aggiunge, è possibile assegnare uno o più gesti di immissione per attivarlo.
Da impostazioni predefinite, ai profili non viene assegnato alcun gesto.
è possibile aggiungere gesti per attivare un profilo servendosi della [finestra Tasti e gesti di immissione](#InputGestures).
A ciascun profilo corrisponde una voce sotto la categoria profili di configurazione.
Quando si rinomina un profilo, qualsiasi gesto aggiunto in precedenza sarà ancora disponibile.
La rimozione di un profilo eliminerà automaticamente i gesti ad esso associati.

### Posizione dei file di configurazione {#LocationOfConfigurationFiles}

Le versioni portabili di NVDA registrano tutte le impostazioni, i moduli personalizzati per le applicazioni e i driver in una cartella chiamata userConfig, situata nella directory di NVDA.

Le versioni installer di NVDA registrano tutte le impostazioni, i moduli personalizzati per le applicazioni e i driver in una cartella speciale situata nei profili utente di Windows. 
Ciò significa che ciascun utente del sistema potrà avere le proprie impostazioni. 
Per accedere a tale cartella da qualsiasi punto ci si trovi, è possibile servirsi della [Finestra di dialogo Tasti e Gesti di immissione](#InputGestures) per aggiungere un gesto personalizzato.
Inoltre, solo per le versioni di NVDA installate nel sistema, sarà sufficiente aprire il menu avvio, selezionare programmi - NVDA- esplora le impostazioni utente.

Le impostazioni di NVDA per quanto riguarda il proprio funzionamento nelle schermate di Logon o UAC sono salvate nella cartella systemConfig situata nella directory di installazione di NVDA.
In genere questa configurazione non dovrebbe essere modificata.
Per cambiare la configurazione di NVDA nelle schermate di Logon o UAC, impostare lo screen reader a proprio piacimento una volta loggati in Windows, dopodiché utilizzare il bottone presente all'interno della categoria generale della finestra [Impostazioni NVDA](#NVDASettings) per copiare la configurazione corrente nelle schermate di logon.

## Componenti aggiuntivi e Add-on Store {#AddonsManager}

I componenti aggiuntivi, o add-on, sono pacchetti software che forniscono funzionalità innovative o vanno a modificare alcune caratteristiche di NVDA.
Vengono sviluppati dalla community di NVDA e da organizzazioni esterne quali fornitori commerciali o programmatori.
Gli add-on possono eseguire diverse operazioni, tra le quali:

* Aggiungere o migliorare il supporto per determinate applicazioni.
* Fornire supporto per display Braille e o sintetizzatori vocali aggiuntivi.
* Aggiungere o modificare funzioni in NVDA.

L'Add-on Store di NVDA consente di sfogliare e gestire i pacchetti aggiuntivi.
Tutti i componenti aggiuntivi disponibili nell'Add-on Store possono essere scaricati gratuitamente.
Tuttavia, alcuni di essi potrebbero richiedere agli utenti di pagare una licenza o un software aggiuntivo prima di poter essere utilizzati.
Un esempio di questo tipo di add-on è costituito dalle sintesi vocali commerciali. 
Se si installa un add-on con componenti a pagamento e si cambia idea sull'utilizzo, esso può essere facilmente rimosso.

L'Add-on Store è accessibile dal sottomenu Strumenti del menu NVDA.
Per accedere all'Add-on Store da qualsiasi posto, assegnare un gesto personalizzato utilizzando la [finestra di dialogo Tasti e Gesti di immissione](#InputGestures).

### Navigare tra gli add-on {#AddonStoreBrowsing}

Una volta aperto, l'Add-on Store visualizza un elenco di componenti aggiuntivi.
Se non sono presenti componenti aggiuntivi installati, , l'add-on store mostrerà un elenco di add-on disponibili all'installazione..
Se invece sono stati già installati componenti aggiuntivi, l'elenco mostrerà gli add-on attualmente installati.

Selezionando un componente aggiuntivo tramite i tasti freccia su e giù, verranno visualizzati i dettagli dell'add-on stesso.
I componenti aggiuntivi hanno azioni associate a cui è possibile accedere tramite un [menu azioni](#AddonStoreActions), come installa, aiuto, disabilita e rimuovi.
Tali azioni cambieranno in base allo stato del componente aggiuntivo, installato, disinstallato, abilitato o disabilitato.

#### Le visualizzazioni dell'elenco componenti aggiuntivi {#AddonStoreFilterStatus}

Esistono diverse visualizzazioni per i componenti aggiuntivi: installati, aggiornabili, disponibili e incompatibili.
è possibile utilizzare `ctrl+tab`.per passare tra le varie visualizzazioni.
Come previsto dalla maggior parte dei programmi, è anche possibile usare il tasto `tab` per posizionarsi sulla parte in cui vi sono le schede delle varie voci, e spostarsi quindi tra di esse servendosi della `frecciaSinistra` e della `frecciaDestra`.

#### Filtraggio per componenti aggiuntivi abilitati o disabilitati {#AddonStoreFilterEnabled}

Normalmente, un componente aggiuntivo installato sarà anche "abilitato", nel senso che è in esecuzione e disponibile all'interno di NVDA.
Tuttavia, alcuni add-on installati potrebbero essere impostati sullo stato "disabilitato".
Ciò significa che non verranno utilizzati e le loro funzioni non saranno disponibili durante la sessione corrente di NVDA.
Per esempio, Si potrebbe aver disabilitato un componente aggiuntivo perché andava in conflitto con un altro add-on o con una determinata applicazione.
NVDA può anche disabilitare da solo alcuni componenti aggiuntivi, nel caso in cui risultassero incompatibili durante un aggiornamento dello screen reader; naturalmente, si verrà avvisati di questo.
Gli add-on possono anche essere disabilitati nel caso in cui si è certi di non usarli per un lungo periodo di tempo, ma non li si vuole disinstallare perché si prevede di volerli di nuovo in futuro.

L'elenco dei componenti aggiuntivi installati e incompatibili può essere filtrato in base al loro stato: abilitato o disabilitato.
L'impostazione predefinita mostra i componenti aggiuntivi abilitati e disabilitati.

#### Includere componenti aggiuntivi incompatibili {#AddonStoreFilterIncompatible}

Gli add-on disponibili e aggiornabili possono essere filtrati in modo da includere [i componenti aggiuntivi incompatibili](#incompatibleAddonsManager) disponibili per l'installazione.

#### Filtrare i componenti aggiuntivi per canale {#AddonStoreFilterChannel}

I componenti aggiuntivi possono essere distribuiti attraverso un massimo di quattro canali:

* Stabile: lo sviluppatore lo ha rilasciato come add-on testato con una versione stabile di NVDA..
* Beta: Questo componente aggiuntivo potrebbe richiedere ulteriori test, ma viene rilasciato in modo che gli utenti possano fornire suggerimenti e feedback..
Consigliato per gli utenti più esperti..
* Dev: canale riservato per lo più agli sviluppatori che potranno testare funzionalità delle API non ancora rilasciate..
I tester delle versioni alpha di NVDA potrebbero aver bisogno di utilizzare una versione "Dev" dei loro add-on.
* Esterno: componenti aggiuntivi installati da fonti esterne, al di fuori dello store dei componenti aggiuntivi.

Per elencare i componenti aggiuntivi solo per canali specifici, modificare la selezione del filtro "Canale".

#### Ricerca di add-on {#AddonStoreFilterSearch}

Per cercare componenti aggiuntivi, utilizzare la casella di testo "Cerca".
è possibile raggiungerla premendo `shift+tab` dall'elenco dei componenti aggiuntivi.
Digitare una o due parole chiave per il tipo di componente aggiuntivo che si sta cercando, quindi un colpo di `tab` per andare agli add-on.
NVDA cercherà il testo appena inserito in vari campi, quali ID, Nome visualizzato, publisher, autore o descrizione, dopodiché mostrerà un elenco di add-on relativi alla ricerca effettuata.

### Azioni sugli add-on {#AddonStoreActions}

I componenti aggiuntivi possiedono azioni associate, come installa, aiuto, disabilita e rimuovi.
È possibile accedere al menu delle azioni per un add-on in vari modi: premendo il tasto `applicazioni`, oppure `invio`, facendo clic con il pulsante destro del mouse o facendo doppio clic sul componente aggiuntivo.
C'è anche un pulsante Azioni nei dettagli del componente aggiuntivo selezionato che permette l'accesso al menu.

#### Installazione degli add-on {#AddonStoreInstalling}

Solo per il fatto che un componente aggiuntivo è disponibile nell'Add-on Store di NVDA, non significa che sia stato approvato o controllato da NV Access o da chiunque altro.
È molto importante installare solo componenti aggiuntivi da fonti attendibili.
La funzionalità degli add-on è illimitata all'interno di NVDA.
Ciò potrebbe includere l'accesso ai propri dati personali o persino all'intero sistema.

è possibile installare e aggiornare i componenti aggiuntivi [navigando tra gli add-on disponibili](#AddonStoreBrowsing).
Selezionare un componente aggiuntivo dalla scheda "add-on disponibili" o "add-on aggiornabili".
Dopodiché servirsi delle azioni Aggiorna, installa, o sostituisci per iniziare l'installazione.

è anche possibile installare più componenti aggiuntivi contemporaneamente.
Ciò può essere effettuato selezionando più componenti aggiuntivi nella scheda degli add-on disponibili, quindi attivare il menu contestuale e scegliere l'azione "Installa componenti aggiuntivi selezionati".

Per installare un componente aggiuntivo ottenuto al di fuori dell'Add-on Store, premere il pulsante "Installa da una fonte esterna".
Ciò consentirà di cercare un (file con estensione `.nvda-addon`) da qualche parte sul computer o su una rete.
Una volta aperto il pacchetto aggiuntivo, inizierà il processo di installazione.

Se NVDA è installato e in esecuzione sul sistema, si può anche aprire un add-on direttamente dal browser o dal file system per iniziare il processo di installazione.

Quando un componente aggiuntivo viene installato da una fonte esterna, NVDA chiederà di confermare l'installazione.
Una volta installato il componente, NVDA deve essere riavviato affinché l'add-on possa funzionare, anche se è possibile posticipare il riavvio nel caso in cui vi siano altri add-on da installare o aggiornare.

#### Rimozione di componenti aggiuntivi {#AddonStoreRemoving}

Per rimuovere un componente aggiuntivo, selezionare l'add-on dall'elenco e utilizzare l'azione Rimuovi.
NVDA chiederà di confermare la rimozione.
Come per l'installazione, NVDA necessita di un riavvio per rimuovere completamente l'add-on.
Fino a quando non si effettua tale operazione, all'interno dell'elenco add-on lo stato del componente sarà marcato come "In attesa di rimozione".
Come per l'installazione, è possibile anche rimuovere più componenti aggiuntivi contemporaneamente.

#### Disattivazione e Attivazione dei componenti aggiuntivi {#AddonStoreDisablingEnabling}

Per disabilitare un componente aggiuntivo, utilizzare l'azione "disabilita".
Per abilitare un componente aggiuntivo precedentemente disabilitato, utilizzare l'azione "abilita".
È possibile disabilitare un componente aggiuntivo se lo stato dell'add-on indica che è "attivato" oppure abilitarlo se il componente aggiuntivo è "disattivato".
Per ogni utilizzo dell'azione abilita/disabilita, lo stato del componente aggiuntivo cambia per indicare cosa accadrà al riavvio di NVDA.
Se il componente aggiuntivo è stato precedentemente "disabilitato", lo stato mostrerà "abilitato dopo il riavvio".
Se l'add-on era precedentemente "abilitato", lo stato mostrerà "disabilitato dopo il riavvio".
Esattamente come accade per l'installazioneo la rimozione dei componenti aggiuntivi, è necessario riavviare NVDA affinché le modifiche abbiano effetto.
è possibile anche abilitare o disabilitare più componenti aggiuntivi contemporaneamente selezionando più add-on nella scheda dei componenti aggiuntivi disponibili, quindi attivare il menu contestuale e scegliendo l'azione appropriata.

#### Il sistema di recensione degli add-on {#AddonStoreReviews}

Prima di installare un componente aggiuntivo, potrebbe essere interessante leggere le recensioni lasciate da altri utenti..
Oppure, esiste la possibilità di lasciare recensioni dopo aver provato un add-on, in modo da facilitare altre persone.
Per leggere le recensioni riguardo un componente aggiuntivo, selezionarne uno dall'elenco degli add-on disponibili o aggiornabili, dopodiché usare l'azione "Recensioni dalla Community".
Ciò aprirà un collegamento ad una pagina Web di discussione GitHub, dove si potrà leggere e scrivere recensioni per il componente aggiuntivo.
Si tenga presente che ciò non sostituisce la comunicazione diretta con gli sviluppatori degli add-on.
Lo scopo di questa funzionalità è invece quello di condividere feedback per aiutare gli utenti a decidere se un componente aggiuntivo può essere utile per loro.

### Add-on incompatibili {#incompatibleAddonsManager}

Alcuni componenti aggiuntivi meno recenti potrebbero non essere più compatibili con la versione di NVDA in uso.
Vale anche il contrario, quindi nel caso in cui si stia utilizzando una vecchia versione dello screen reader, alcuni nuovi add-on potrebbero non funzionare.
Se si cercherà di installare un componente aggiuntivo incompatibile si otterrà come risultato un errore che spiega il motivo per il quale l'add-on è considerato incompatibile.

Per i componenti aggiuntivi meno recenti, si può ignorare l'incompatibilità a proprio rischio e pericolo.
Gli add-on incompatibili potrebbero non funzionare con la versione di NVDA in uso e causare comportamenti instabili o imprevisti, inclusi arresti anomali.
è possibile ignorare la compatibilità quando si abilita o installa un componente aggiuntivo.
Nel caso in cui l'add-on incompatibile causa problemi in un secondo momento, sarà sempre possibile disabilitarlo o rimuoverlo.

Se si riscontrano problemi durante l'esecuzione di NVDA, ed è stato aggiornato o installato un add-on di recente, soprattutto se si tratta di un componente incompatibile, è consigliabile provare ad eseguire NVDA con i componenti aggiuntivi temporaneamente disabilitati.
Per riavviare NVDA con tutti i componenti aggiuntivi disabilitati, sceglire l'opzione appropriata all'uscita di NVDA.
In alternativa, servirsi dell'[opzione a riga di comando](#CommandLineOptions) `--disable-addons`.

Si può navigare tra gli add-on non compatibili tramite le [schede add-on disponibili e aggiornabili](#AddonStoreFilterStatus).
Inoltre, si può navigare tra gli add-on installati non compatibili tramite la [scheda add-on incompatibili](#AddonStoreFilterStatus).

## Strumenti aggiuntivi {#ExtraTools}
### Visualizzatore log {#LogViewer}

Il visualizzatore log, situato alla voce strumenti del menu di NVDA, permette di mostrare tutte le informazioni di log dell'ultima sessione di NVDA.

Oltre a leggere il contenuto, è possibile anche salvare una copia del file di log, o aggiornare il visualizzatore in modo da caricare le ultime informazioni che NVDA ha fornito dall'ultima volta che è stato aperto lo strumento.
Queste azioni sono disponibili dal menu Log del visualizzatore.

Il file mostrato quando si apre il visualizzatore log viene salvato sul computer alla posizione `%temp%\nvda.log`.
Ogni qualvolta NVDA viene eseguito, sarà creato un nuovo file di log.
Quando ciò accade, il vecchio file di log della sessione precedente di NVDA viene spostato in `%temp%\nvda-old.log`.

è anche possibile copiare negli appunti un frammento del file di log senza aprire il visualizzatore..
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Apri visualizzatore log |`NVDA+f1` |Apre il visualizzatore log e mostra informazioni utile agli sviluppatori sull'oggetto corrente del navigatore.|
|Copia un frammento di log negli appunti |`NVDA+control+shift+f1` |Alla prima pressione, viene impostato un punto di inizio per il contenuto del log che deve essere catturato. La seconda pressione copierà negli appunti il contenuto del log, partendo naturalmente dal punto di inizio impostato poco prima.|

<!-- KC:endInclude -->

### Visualizzatore sintesi vocale {#SpeechViewer}

Per sviluppatori vedenti di programmi o persone che stanno dimostrando le funzionalità di NVDA ad un'utenza vedente, è disponibile una finestra che mostra tutto il testo che NVDA manda alla sintesi vocale.

Per abilitare il visualizzatore sintesi vocale, attivare la voce apposita che si trova nel menu strumenti di NVDA.
Disabilitare la voce di menu per disattivare tale caratteristica.

La finestra del visualizzatore sintesi vocale contiene una casella di controllo etichettata "Mostra il visualizzatore sintesi vocale all'avvio".
Se selezionata, il visualizzatore sintesi vocale si aprirà all'avvio di NVDA.
La finestra tenterà di aprirsi con le medesime dimensioni e conservando l'esatta posizione dell'ultima volta in cui è stata chiusa.

Mentre il visualizzatore sintesi vocale è attivo, il contenuto della finestra si aggiornerà in tempo reale per mostrare di continuo le informazioni che NVDA invia al sintetizzatore.
Comunque, se si fa passare il mouse sulla finestra o la si evidenzia, NVDA fermerà temporaneamente l'aggiornamento di modo da permettere la selezione del testo e l'eventuale copia dello stesso.

Per abilitare/disabilitare il visualizzatore sintesi vocale da qualsiasi punto ci si trovi, servirsi della finestra [tasti e gesti di immissione](#InputGestures) ed assegnare un gesto o tasto rapido personalizzato per quella funzione.

### Visualizzatore Braille {#BrailleViewer}

Per sviluppatori vedenti di programmi o persone che stanno dimostrando le funzionalità di NVDA, è disponibile una finestra che mostra ciò che la persona non vedente sta leggendo sulla propria riga braille, ed il testo equivalente per ciascun carattere braille.
Il visualizzatore Braille può essere utilizzato contemporaneamente a un display Braille fisico, il numero di celle corrisponderà al numero effettivo di quelle della barra braille.
Quando questa caratteristica è attiva, il contenuto della finestra si aggiornerà in tempo reale per mostrare di continuo le informazioni che NVDA invia al display braille.

Per abilitare il visualizzatore braille, attivare la voce apposita che si trova nel menu strumenti di NVDA.
Deselezionare la voce di menu per disattivare il visualizzatore braille.

I display Braille fisici in genere sono provvisti di pulsanti per scorrere avanti o indietro; per abilitare lo scorrimento con il visualizzatore Braille, utilizzare la finestra di dialogo [Gesti e tasti di immissione](#InputGestures) per assegnare le scorciatoie da tastiera appropriate alle funzioni "Scorre display braille indietro" e "Scorre display braille avanti".

La finestra visualizzatore braille contiene una casella di controllo chiamata "Mostra visualizzatore braille all'avvio".
Se tale casella è selezionata, il visualizzatore braille si caricherà all'avvio di NVDA.
La finestra cercherà sempre di riaprirsi con le stesse dimensioni e posizione di quando è stata chiusa in precedenza.

Un'altra casella di controllo presente all'interno della finestra è chiamata "il passaggio del mouse attiva i cursor routing"
Se selezionata, basterà posizionare il mouse su di una cella per simulare la pressione del cursor routing di quella cella sulla barra braille.
Ciò viene spesso usato per spostare il cursore o attivare l'azione per un controllo.
Questo può essere utile per testare che NVDA sia in grado di invertire correttamente la mappatura a da una cella braille.
Per impedire che il comando venga eseguito involontariamente, esso viene ritardato.
Il mouse deve rimanere fermo finché la cella non diventa verde.
La cella avrà dapprima un colore tendente al giallo chiaro, effettuerà una transizione all'arancio, per poi diventare improvvisamente verde.

Per attivare o disattivare il visualizzatore braille da qualsiasi parte, assegnare un gesto personalizzato utilizzando la [finestra di dialogo tasti e gesti di immissione](#InputGestures).

### Console Python {#PythonConsole}

La Console Python di NVDA, situata nel menu strumenti, è uno strumento per sviluppatori che risulta utile in fase di debug, di diagnosi delle funzioni interne di NVDA o di analisi della gerarchia degli oggetti accessibili presenti in un'applicazione.
Per ulteriori informazioni, si veda la [guida agli sviluppatori per NVDA](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html), in lingua inglese.

### Add-on Store {#AddonStoreMenuItem}

Consente di aprire l'[Add-on Store di NVDA](#AddonsManager).
Per maggiori informazioni, leggere la sezione di approfondimento: [Componenti aggiuntivi e l'Add-on Store](#AddonsManager).

### Crea copia portable {#CreatePortableCopy}

Verrà visualizzata una finestra di dialogo che consente di creare una copia portable di NVDA a partire dalla versione installata.
Di contro, quando si esegue una copia portable di NVDA, nel sottomenu strumenti la voce di menu sarà chiamata "installa NVDA su questo PC" invece di "crea copia portable).

In questa finestra, verrà chiesto di selezionare la cartella in cui lo screen reader dovrà essere copiato o installato.

Inoltre è possibile attivare o disattivare le seguenti opzioni:

* Copia la configurazione utente corrente (ciò comprende i file presenti in %appdata%\roaming\NVDA, o quelli della configurazione utente della copia portable, oltre a componenti aggiuntivi e altri moduli)
* Avvia la nuova copia portable dopo la creazione o avvia NVDA dopo l'installazione, le due funzioni si spiegano da sé.)

### Esegui Utility risoluzione registrazioni Com di sistema... {#RunCOMRegistrationFixingTool}

L'installazione e la disinstallazione di programmi su un computer può, in alcuni casi, causare l'annullamento della registrazione dei file DLL COM.
Dato che le interfacce Com, come Iaccessible, dipendono dalla corretta registrazione delle dll, si possono verificare problemi nel caso in cui tale registrazione sia stata persa o non sia stata effettuata correttamente..

Ciò può accadere, ad esempio, dopo aver installato e disinstallato Adobe Reader, Math Player e altri programmi.

La mancata registrazione può causare problemi a browser, app desktop, barra delle applicazioni e altre interfacce.

In particolare, i seguenti problemi possono essere risolti eseguendo questo strumento:

* NVDA dice "sconosciuto" durante la navigazione in browser come Firefox, Thunderbird ecc.
* NVDA non riesce a passare dalla modalità focus alla modalità navigazione
* NVDA è molto lento nei browser quando si cerca di navigare
* E probabilmente altri problemi.

### Ricarica componenti aggiuntivi {#ReloadPlugins}

Questa voce, una volta attivata, ricarica tutti i plugin e i moduli specifici per le applicazioni senza riavviare NVDA. Risulta utile per gli sviluppatori.
Gli appModule gestiscono il modo in cui NVDA interagisce con applicazioni specifiche.
Invece, i plugin globali gestiscono il modo in cui NVDA interagisce con tutte le applicazioni.

Potrebbero essere utili anche i seguenti comandi da tastiera di NVDA:
<!-- KC:beginInclude -->

| Nome |Tasto |Descrizione|
|---|---|---|
|Ricarica plugin |`NVDA+control+f3` |Ricarica i plugin globali e gli appModule di NVDA.|
|Annuncia il modulo dell'app caricato e l'eseguibile |`NVDA+control+f1` |Annuncia il nome del modulo dell'app, se presente, e il nome dell'eseguibile associato all'applicazione su cui è attivo il focus della tastiera.|

<!-- KC:endInclude -->

## Sintesi vocali supportate {#SupportedSpeechSynths}

Questa sezione contiene informazioni sui sintetizzatori vocali supportati da NVDA.
Per una panoramica esaustiva dei sintetizzatori compatibili, sia gratuiti che a pagamento, si veda la [pagina sulle voci aggiuntive in inglese](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### Espeak NG {#eSpeakNG}

La sintesi vocale [eSpeak NG](https://github.com/espeak-ng/espeak-ng) è incorporata direttamente in NVDA, per cui non è necessario alcun driver o componente per farla funzionare. 
In Windows 8.1, da impostazioni predefinite NVDA si avvia utilizzando Espeak NG, mentre su Windows10 e successive la sintesi vocale di default è [Windows OneCore](#OneCore).
Poiché questa sintesi è incorporata in NVDA, risulta molto comoda per utilizzare il prodotto da una chiavetta USB o in altri sistemi.

Ciascuna voce presente in Espeak NG parla una lingua diversa.
Sono oltre 43 le lingue supportate da questa sintesi vocale.

Vi sono anche numerose varianti che possono essere usate per modificare il timbro della voce.

### Microsoft Speech API versione 4 (SAPI 4) {#SAPI4}

Sapi4 è una vecchia tecnologia Microsoft da usare nei programmi di sintesi vocale.
NVDA supporta ancora questo tipo di sintetizzatore nel caso l'utente disponga di uno di questi.
Tuttavia, è importante sottolineare che Microsoft non supporta più questa tecnologia e che i componenti necessari non sono più resi disponibili dall'azienda.

Quando vengono utilizzate queste sintesi vocali con NVDA, le voci disponibili (accessibili attraverso [la categoria voci](#SpeechSettings) della finestra [Impostazioni NVDA](#NVDASettings) oppure con le [modifiche al volo dei parametri del sintetizzatore](#SynthSettingsRing)) conterranno tutte le voci installate dalle tecnologie Sapi4 individuate nel proprio pc.

### Microsoft Speech API versione 5 (SAPI 5) {#SAPI5}

Sapi5 è uno standard Microsoft da usare nei programmi di sintesi vocale.
Molti di questi sintetizzatori possono essere acquistati o scaricati liberamente da varie aziende o siti web, inoltre generalmente almeno una di queste voci risulta già installata sul proprio sistema. (nota del traduttore: la voce preinstallata è in inglese].
Quando vengono utilizzate queste sintesi vocali con NVDA, le voci disponibili (accessibili attraverso [la categoria voci](#SpeechSettings) della finestra [Impostazioni NVDA](#NVDASettings) oppure con le [modifiche al volo dei parametri del sintetizzatore](#SynthSettingsRing)) conterranno tutte le voci installate dalle tecnologie Sapi5 individuate nel proprio pc.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

La piattaforma Microsoft Speech fornisce supporto per diverse lingue, e generalmente è utilizzata nello sviluppo di applicazioni lato server.
Queste voci possono essere utilizzate anche con NVDA.

Per usare queste voci, è necessaria l'installazione di due componenti:

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Questa pagina contiene diversi file sia per il riconoscimento vocale sia per la sintesi vocale stessa.
 Selezionare i file che si desiderano, a seconda del TTS e della lingua che si vuole utilizzare.
 Ad esempio, il file MSSpeech_TTS_en-US_ZiraPro.msi è una voce inglese Stati Uniti.

### Voci Windows OneCore {#OneCore}

In Windows10 e versioni successive sono presenti nuove voci conosciute come "OneCore", oppure come "mobile".
Tali voci sono disponibili in diverse lingue e risultano più reattive rispetto alle classiche Sapi5.
In Windows10 e versioni successive NVDA utilizza queste voci come sintesi vocale predefinita, mentre [[eSpeak NG](#eSpeakNG) viene usata in altre versioni di Windows.

Per aggiungere nuove voci Windows OneCore, andare in "Impostazioni sintesi vocale", dalle impostazioni di sistema di Windows. 
Servirsi dell'opzione "Aggiungi voci" e cercare la lingua desiderata.
Molte lingue includono più varianti.
"Regno Unito" e "Australia" sono due delle varianti inglesi.
"Francia", "Canada" e "Svizzera" sono varianti francesi disponibili.
Cercare la lingua più conosciuta (come l'inglese o il francese), quindi individuare la variante nell'elenco.
Selezionare le lingue desiderate e utilizzare il pulsante "aggiungi".
Una volta aggiunte, riavviare NVDA.

Consultare l'articolo [Lingue e voci supportate](https://support.microsoft.com/en-us/windows/appendix-a-supported-linguals-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) per un elenco delle voci disponibili voci.

## Display braille supportati {#SupportedBrailleDisplays}

Questa sezione contiene informazioni sulle barre braille supportate da NVDA.

### Display che supportano la rilevazione automatica in background {#AutomaticDetection}

NVDA è in grado di rilevare automaticamente un gran numero di Display Braille, sia via bluetooth che tramite USB.
Questa funzionalità la si attiva selezionando la voce "automatico" dalla [Finestra Impostazioni Braille](#BrailleSettings).
L'opzione è già selezionata per impostazioni predefinite.

Segue l'elenco di tutti i display braille che supportano il rilevamento automatico:

* Display Handy Tech
* Display Baum/Humanware/APH/Orbit
* Brailliant Humanware serie BI/B
* BrailleNote di Humanware
* SuperBraille
* Alva serie 6 di Optelec
* modelli Braille Sense/Braille EDGE/Smart Beetle/Sync della Hims.
* Display Esys/Esytime/Iris di Eurobraille
* Display Braille Nattiq serie N
* I modelli Notetaker di Seika: MiniSeika (16, 24 celle), V6, e V6Pro (40 celle)
* I modelli Tivomatic Caiku Albatross 46/80
* Qualsiasi display che supporti il protocollo Braille standard HID

### Freedom Scientific Serie Focus/PAC Mate {#FreedomScientificFocus}

Sono supportati Tutti i Display Braille Focus e Pac Mate prodotti da [Freedom Scientific](https://www.freedomscientific.com/), sia USB che Bluetooth.
per un corretto funzionamento è necessario avere installati nel proprio sistema i driver per display Braille Freedom Scientific.
Nel caso non si sia in possesso di tali driver, è possibile ottenerli dalla [pagina Driver Braille Focus Blue](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Sebbene nella pagina sia nominata solo la barra Focus Blue, il driver funzionerà per tutti i modelli Freedom.

Per impostazioni predefinite, NVDA è in grado di individuare e connettersi automaticamente a questi display via USB o Bluetooth.
Comunque, sarà anche possibile selezionare la sola connessione USB o Bluetooth, per restringere il tipo di connessioni da utilizzare.
Questo potrebbe essere utile ad esempio se si vuole usare la Focus con NVDA via Bluetooth, ma si desidera caricare la batteria tramite la connessione USB.
Il rilevamento automatico barre braille di NVDA riconosce anche il display su USB o Bluetooth.

Segue un elenco dei tasti associati con NVDA:
Si prega di consultare la documentazione della propria barra braille per avere informazioni sulla loro posizione.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri Display Braille indietro |topRouting1 (prima cella del Display)|
|Scorri Display Braille avanti |topRouting20/40/80 (ultima cella del Display)|
|Scorri display braille indietro |barraAvanzamentoSinistra|
|Scorri display Braille avanti |barraAvanzamentoDestra|
|Commuta inseguimento braille |leftGDFButton+rightGDFButton|
|Toggle left wiz wheel action |leftWizWheelPress|
|Move back using left wiz wheel action |leftWizWheelUp|
|Move forward using left wiz wheel action |leftWizWheelDown|
|Toggle right wiz wheel action |rightWizWheelPress|
|Move back using right wiz wheel action |rightWizWheelUp|
|Move forward using right wiz wheel action |rightWizWheelDown|
|Route to braille cell |routing|
|tasti shift+tab |spazio+punto1+punto2|
|tasto tab |spazio+punto4+punto5|
|freccia su |spazio+punto1|
|freccia giù |spazio+punto4|
|control+freccia sinistra |spazio+punto2|
|control+freccia destra |spazio+punto5|
|freccia sinistra |spazio+punto3|
|freccia destra |spazio+punto6|
|tasto inizio/home |spazio+punto1+punto3|
|tasto fine |spazio+punto4+punto6|
|control+home/inizio |spazio+punto1+punto2+punto3|
|control+fine |spazio+punto4+punto5+punto6|
|tasto alt |spazio+punto1+punto3+punto4|
|alt+tab |spazio+punto2+punto3+punto4+punto5|
|alt+shift+tab |Spazio+punto1+punto2+punto5+punto6|
|windows+tab |Spazio+punto2+punto3+punto4|
|tasto esc |spazio+punto1+punto5|
|tasto windows |spazio+punto2+punto4+punto5+punto6|
|spazio |spazio|
|Attiva/disattiva tasto control |spazio+punto3+punto8|
|Attiva/disattiva tasto alt |Spazio+punto6+punto8|
|Attiva/disattiva tasto windows |Spazio+punto4+punto8|
|Attiva/disattiva tasto NVDA |Spazio+punto5+punto8|
|Attiva/disattiva tasto shift |Spazio+punto7+punto8|
|Attiva/disattiva tasti control e shift |Spazio+punto3+punto7+punto8|
|Attiva/disattiva tasti alt e shift tasti |Spazio+punto6+punto+punto8|
|Attiva/disattiva tasti windows e shift |Spazio+punto4+punto7+punto8|
|Attiva/disattiva tasti NVDA e shift |Spazio+punto5+punto7+punto8|
|Attiva/disattiva tasti control e alt |Spazio+punto3+punto6+punto8|
|Attiva/disattiva tasti control, alt, e shift |Spazio+punto3+punto6+punto7+punto8|
|tasto windows+d (riduce a icona tutte le applicazioni) |spazio+punto1+punto2+punto3+punto4+punto5+punto6|
|annuncia riga corrente |spazio+punto1+punto4|
|NVDA menu |spazio+punto1+punto3+punto4+punto5|

Per i modelli più recenti di Focus (focus 40, focus 80 e focus blue):

| Nome |Tasto|
|---|---|
|Sposta display Braille alla riga precedente |leftRockerBarUp, rightRockerBarUp|
|Sposta Display Braille alla riga successiva |leftRockerBarDown, rightRockerBarDown|

Solo per Focus 80:

| Nome |Tasto|
|---|---|
|Scorri display braille indietro |leftBumperBarUp, rightBumperBarUp|
|Scorri display Braille avanti |leftBumperBarDown, rightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA serie 6/protocol converter {#OptelecALVA}

Sono supportati sia i modelli BC640 che BC680 prodotti dalla [Optelec](https://www.optelec.com/) sia con connessione usb che bluetooth.
In alternativa , è possibile connettere un display Optelec più vecchio, ad esempio il Braille Voyager, servendosi di un convertitore di protocolli prodotto dalla stessa Optelec.
Per un corretto funzionamento non si avrà bisogno di alcun driver aggiuntivo.
Semplicemente collegare la Barra Braille e configurare NVDA selezionando tale dispositivo.

Nota: NVDA potrebbe non essere in grado di connettersi via bluetooth con un display Alva BC6 quando l'accoppiamento viene effettuato tramite l'utility Alva Bluetooth.
Nel caso si sia associato il dispositivo tramite questa utility e si riscontra che NVDA non è in grado di connettersi o di riconoscere il dispositivo, si consiglia di utilizzare la procedura standard di accoppiamento presente nelle impostazioni bluetooth di Windows. 

Nota: Poiché la maggior parte di questi display possiedono una tastiera braille, essi gestiscono autonomamente la procedura di traduzione dal braille al testo.
Pertanto, le impostazioni di immissione tabella braille in NVDA non sono rilevanti.
Per i display Alva con un firmware recente, è possibile disabilitare la simulazione tastiera HID servendosi di un gesto di immissione.

Segue un elenco dei tasti associati con NVDA:
Si prega di consultare la documentazione della propria barra braille per avere informazioni sulla loro posizione.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorrimento display braille indietro |t1 o etouch1|
|Sposta il display braille alla riga precedente |t2|
|Spostarsi alla posizione attuale del focus |t3|
|Sposta il Display Braille alla riga successiva |t4|
|Scorrimento Display Braille avanti |t5 o etouch3|
|Portare cursore sulla cella braille |routing|
|Mostra informazioni di formattazione testo sulla cella braille |cursor routing secondario|
|Alterna simulazione tastiera HID |t1+spEnter|
|spostarsi all'inizio della riga in modalità in linea |t1+t2|
|Spostarsi alla fine della riga in modalità in linea |t4+t5|
|Commuta inseguimento braille |t1+t3|
|Leggi titolo |etouch2|
|Leggi barra di stato |etouch4|
|Tasto shift+tab |sp1|
|Tasto alt |sp2|
|Tasto esc |sp3|
|Tasto tab |sp4|
|Freccia su |spUp|
|Freccia giù |spDown|
|Freccia sinistra |spLeft|
|Freccia destra |spRight|
|Tasto invio |spEnter, Enter|
|leggere data/ora |sp2+sp3|
|Menu NVDA |sp1+sp3|
|Tasto windows+d (ridurre ad icona tutte le applicazioni) |sp1+sp4|
|tasto windows+b (focus sul system tray) |sp3+sp4|
|Tasto windows |sp1+sp2, Windows|
|Tasto alt+tab |sp2+sp4|
|tasto control+home |t3+spUp|
|tasto control+end |t3+spDown|
|Tasto home |t3+spLeft|
|Tasto end |t3+spRight|
|Tasto control |control|

<!-- KC:endInclude -->

### Modelli Handy Tech {#HandyTech}

NVDA supporta gran parte dei modelli di barre braille prodotte dalla [Handy Tech](https://www.handytech.de/), siaUSB, seriali che Bluetooth. 
Per alcuni modelli vecchi USB bisogna installare i driver USB fatti dalla Handy Tech.

I seguenti display braille non sono supportati in maniera nativa, ma possono essere comunque usati installando il [driver universale Handy Tech](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) e il componente aggiuntivo:

* Braillino
* Bookworm
* display modulari con versione firmware 1.13 o inferiore. Si noti che il firmware di queste barre braille può essere aggiornato.

Seguono i tasti che sono stati assegnati con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scorre Display Braille indietro |left, up, b3|
|Scorre Display Braille avanti |right, down, b6|
|Sposta il display braille alla riga precedente |b4|
|Sposta il display braille alla riga successiva |b5|
|Route to braille cell |routing|
|Tasto shift+tab |esc, left triple action key up+down|
|Tasto alt |b2+b4+b5|
|Tasto esc |b4+b6|
|tasto tab |enter, right triple action key up+down|
|tasto invio |esc+enter, left+right triple action key up+down, joystickAction|
|tasto freccia su |joystickUp|
|tasto freccia giù |joystickDown|
|tasto freccia sinistra |joystickLeft|
|tasto freccia destra |joystickRight|
|Menu NVDA |b2+b4+b5+b6|
|Commuta inseguimento cursore braille |b2|
|Commuta cursore braille |b1|
|Commuta presentazione del focus in base al contesto |b7|
|Commuta immissione braille |spazio+b1+b3+b4 (spazio+B maiuscola)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

NVDA supporta la barra Braille Lilli prodotta dalla [MDV](https://www.mdvbologna.it/). 
Per un corretto funzionamento non si avrà bisogno di alcun driver aggiuntivo. 
Semplicemente collegare la Barra Braille e configurare NVDA selezionando tale dispositivo.

Questi modelli non supportano ancora la funzione di rilevazione automatica in background.

Seguono i tasti che sono stati assegnati con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorre Display Braille indietro |LF|
|Scorre Display Braille avanti |RG|
|Sposta il display braille alla riga precedente |UP|
|Sposta il display braille alla riga successiva |DN|
|Route to braille cell |routing|
|Tasto shift+tab |SLF|
|Tasto tab |SRG|
|Tasto alt+tab |SDN|
|Tasto alt+shift+tab |SUP|

<!-- KC:endInclude -->

### Display Braille Baum/Humanware/APH/Orbit Reader {#Baum}

Molti Display Braille della [Baum](https://www.baum.de/cms/en/), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) e [Orbit](https://www.orbitresearch.com/) sono supportati sia tramite USB, Bluetooth o porta seriale.
Essi includono:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Altre barre Braille della Baum potrebbero funzionare, tuttavia non sono stati fatti test in tal senso.

Nel caso di connessione tramite USB con display braille che non utilizzano la tecnologia HID (human interface device), è necessario installare i driver forniti dal produttore.
I modelli VarioUltra e Pronto! utilizzano HID.
I modelli Refreshabraille e Orbit Reader 20 possono utilizzare HID se configurati correttamente.

La modalità di connessione porta seriale su USB del modello Orbit Reader 20 è supportata soltanto in Windows10 e versioni successive.
è consigliabile servirsi della modalità USB HID quando possibile.

Seguono i tasti che sono stati assegnati con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorre Display Braille indietro |`d2`|
|Scorre Display Braille avanti |`d5`|
|Sposta il display braille alla riga precedente |`d1`|
|Sposta il display braille alla riga successiva |`d3`|
|Route to braille cell |`routing`|
|tasti `shift+tab` |`spazio+punto1+punto3`|
|tasto `tab` |`spazio+punto4+punto6`|
|tasti `alt` |`spazio+punto1+punto3+punto4` (`spazio+m`)|
|tasto `escape` |`spazio+punto1+punto5` (`spazio+e`)|
|tasto `windows` |`spazio+punto3+punto4`|
|tasti `alt+tab` |`spazio+punto2+punto3+punto4+punto5` (`spazio+t`)|
|Menu NVDA |`spazio+punto1+punto3+punto4+punto5` (`spazio+n`)|
|tasti `windows+d` (ridurre ad icona tutte le applicazioni) |`spazio+punto1+punto4+punto5` (`spazio+d`)|
|Dire tutto |`spazio+punto1+punto2+punto3+punto4+punto5+punto6`|

Per i modelli che possiedono un Joystick:

| Nome |Tasto|
|---|---|
|FrecciaSu |up|
|Frecciagiù |down|
|FrecciaSinistra |left|
|FrecciaDestra |right|
|Tasto Invio |select|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

Il modello hedo ProfiLine USB prodotto dalla [hedo Reha-Technik](https://www.hedo.de/) è pienamente supportato.
E' necessario prima installare i driver USB forniti dal costruttore.

Questo modello non supportano ancora la funzione di rilevazione automatica in background.

Di seguito, ecco l'elenco dell'assegnazione dei tasti per questa riga braille con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri display braille indietro |K1|
|Scorri display braille avanti |K3|
|Sposta display braille alla riga precedente |B2|
|Sposta Display Braille alla riga successiva |B5|
|Route to braille cell |routing|
|Commuta inseguimento Braille |K2|
|Dire tutto |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

La Barra Braille hedo MobilLine USB prodotta dalla hedo Reha-Technik https://www.hedo.de/] è pienamente supportata.
E' prima necessario installare i driver USB forniti dal produttore.

Questo modello non supportano ancora la funzione di rilevazione automatica in background.

Di seguito, ecco l'elenco dell'assegnazione dei tasti per questa riga braille con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri Display Braille indietro |K1|
|Scorri Display Braille avanti |K3|
|Sposta Display Braille alla riga precedente |B2|
|Sposta Display Braille alla riga successiva |B5|
|Route to braille cell |routing|
|Commuta inseguimento Braille |K2|
|Dire tutto |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Series / BrailleNote Touch {#HumanWareBrailliant}

Le Barre Braille Brailliant Serie BI e B prodotte dalla [HumanWare](https://www.humanware.com/), comprese BI 14, Bi 20, Bi 20x, BI 40, Bi40x e B 80, sono supportate quando connesse tramite USB o Bluetooth.
In caso di connessione tramite USB con protocollo impostato su Humanware, è necessario prima installare i driver sviluppati dal produttore.
Non è richiesto alcun driver USB invece nel caso in cui il protocollo sia impostato su OpenBraille.

Sono supportati anche i dispositivi seguenti e non necessitano dell'installazione di alcun driver:

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Di seguito, ecco l'elenco dell'assegnazione dei tasti per queste righe braille con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.

#### Assegnazione tasti per tutti i modelli {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri Display Braille indietro |Sinistra|
|Scorri Display Braille avanti |Destra|
|Sposta Display Braille alla riga precedente |Su|
|Sposta Display Braille alla riga successiva |Giù|
|Route to braille cell |routing|
|Commuta inseguimento Braille |su+giù|
|Tasto Freccia su |spazio+punto1|
|Tasto Freccia giù |spazio+Punto4|
|Tasto Freccia Sinistra |spazio+punto3|
|Tasto Freccia Destra |spazio+punto6|
|shift+Tasto tab |spazio+punto1+punto3|
|Tasto tab |spazio+punto4+punto6|
|Tasto alt |spazio+punto1+punto3+punto4 (spazio+m)|
|Tasto esc |spazio+punto1+punto5 (spazio+e)|
|Tasto Invio |punto8|
|Tasto windows |spazio+punto3+punto4|
|Tasto alt+tab |spazio+punto2+punto3+punto4+punto5 (spazio+t)|
|Menu NVDA |spazio+punto1+punto3+punto4+punto5 (spazio+n)|
|Tasti windows+d (Riduce a icona tutte le applicazioni) |spazio+punto1+punto4+punto5 (spazio+d)|
|Dire Tutto |punto1+punto2+punto3+punto4+punto5+punto6|

<!-- KC:endInclude -->

#### Assegnazione tasti per Brailliant BI 32, BI 40 e B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Menu NVDA |c1+c3+c4+c5 (command n)|
|Tasti Windows+d (riduce a icona tutte le applicazioni) |c1+c4+c5 (command d)|
|Dire tutto |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Assegnazione tasti per Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Freccia su |joystick su|
|Freccia giù |joystick giù|
|Freccia sinistra |joystick sinistra|
|Freccia destra |joystick destra|
|Tasto invio |joystick action|

<!-- KC:endInclude -->

### HIMS serie Braille Sense/Braille EDGE/Smart Beetle/Sync Braille {#Hims}

NVDA supporta i modelli Braille Sense, Braille EDGE,  SmartBeetle e SyncBraille prodotti dalla [Hims](https://www.hims-inc.com/) quando connessi tramite USB o bluetooth.
In caso di connessione tramite USB, è necessario installare i [driver USB da HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) sul sistema.

Di seguito, ecco l'elenco dell'assegnazione dei tasti per queste righe braille con NVDA.
Si legga la documentazione della propria barra Braille per ottenere informazioni su dove sono situati i vari tasti.
<!-- KC:beginInclude -->

| Nome |tasto|
|---|---|
|Route to braille cell |routing|
|Scorri display braille indietro |ScorriSuLatoSinistro, ScorriSuLatoDestro, scorriLatoSinistro|
|Scorri display braille avanti |ScorriGiùLatoSinistro, ScorriGiùLatoDestro, ScorriGiù|
|Sposta display braille alla riga precedente |ScorriSuLatoSinistro+ScorriSuLatoDestro|
|Sposta display braille alla riga successiva |ScorriGiuLatoSinistro+ScorriGiùLatoDestro|
|Sposta alla riga precedente in modalità revisione |FrecciaSuLatoDestro|
|Sposta alla riga successiva in modalità revisione |FrecciaGiùLatoDestro|
|Sposta al carattere precedente in modalità revisione |frecciaSinistraLatoDestro|
|Sposta al carattere successivo in modalità revisione |frecciaDestraLatoDestro|
|Move to current focus |ScorriSuLatoSinistro+ScorriGiuLatoSinistro, ScorriSuLatoDestro+ScorriGiùLatoDestro, ScorriLatoSinistro+ScorriLatoDestro|
|tasto control |smartbeetle:f1, brailleedge:f3|
|tasto windows |f7, smartbeetle:f2|
|tasto alt |punto1+punto3+punto4+spazio, f2, smartbeetle:f3, brailleedge:f4|
|tasto shift |f5|
|tasto insert |punto2+punto4+spazio, f6|
|tasto applicazioni |punto1+punto2+punto3+punto4+spazio, f8|
|tasto blocca maiuscole |punto1+punto3+punto6+spazio|
|tasto tab |punto4+punto5+spazio, f3, brailleedge:f2|
|tasto shift+alt+tab |f2+f3+f1|
|tasto alt+tab |f2+f3|
|tasto shift+tab |punto1+punto2+spazio|
|tasto fine |punto4+punto6+spazio|
|tasto control+fine |punto4+punto5+punto6+spazio|
|tasto inizio |punto1+punto3+spazio, smartbeetle:f4|
|tasto control+inizio |punto1+punto2+punto3+spazio|
|tasto alt+f4 |punto1+punto3+punto5+punto6+spazio|
|tasto freccia sinistra |punto3+spazio, frecciaSinistraLatoSinistro|
|tasto control+shift+freccia sinistra |punto2+punto8+spazio+f1|
|tasto control+frecciaSinistra |punto2+spazio|
|tasto shift+alt+frecciaSinistra |punto2+punto7+f1|
|tasto `alt+frecciaSinistra` |`punto2+punto7+spazio`|
|tasto frecciaDestra |punto6+spazio, frecciaDestraLatoSinistro|
|tasto control+shift+frecciaDestra |punto5+punto8+spazio+f1|
|tasto control+frecciaDestra |punto5+spazio|
|tasto shift+alt+frecciaDestra |punto5+punto7+f1|
|tasto `alt+frecciaDestra` |`punto5+punto7+spazio`|
|tasto paginaSu |punto1+punto2+punto6+spazio|
|tasto control+paginaSu |punto1+punto2+punto6+punto8+spazio|
|tasto frecciaSu |punto1+spazio, frecciaSuLatoSinistro|
|tasto control+shift+frecciaSu |punto2+punto3+punto8+spazio+f1|
|tasto control+frecciaSu |punto2+punto3+spazio|
|tasto shift+alt+frecciaSu |punto2+punto3+punto7+f1|
|tasto `alt+frecciaSu` |`punto2+punto3+punto7+spazio`|
|tasto shift+frecciaSu |ScorriGiuLatoSinistro+spazio|
|tasto PaginaGiù |punto3+punto4+punto5+spazio|
|tasto control+paginaGiù |punto3+punto4+punto5+punto8+spazio|
|tasto frecciaGiù |punto4+spazio, frecciaGiùLatoSinistro|
|tasto control+shift+frecciaGiù |punto5+punto6+punto8+spazio+f1|
|tasto control+frecciaGiù |punto5+punto6+spazio|
|tasto shift+alt+frecciaGiù |punto5+punto6+punto7+f1|
|tasto `alt+frecciaGiù` |`punto5+punto6+punto7+spazio`|
|tasto shift+frecciaGiù |spazio+ScorriGiùLatoDestro|
|tasto escape |punto1+punto5+spazio, f4, brailleedge:f1|
|tasto canc |punto1+punto3+punto5+spazio, punto1+punto4+punto5+spazio|
|tasto f1 |punto1+punto2+punto5+spazio|
|tasto f3 |punto1+punto4+punto8+spazio|
|tasto f4 |punto7+f3|
|tasto windows+b |punto1+punto2+f1|
|tasto windows+d |punto1+punto4+punto5+f1|
|tasto control+insert |smartbeetle:f1+scorriLatoDestro|
|tasto alt+insert |smartbeetle:f3+scorriLatoDestro|

<!-- KC:endInclude -->

### Display Braille Seika {#Seika}

Sono supportati i seguenti display Braille Seika prodotti da Nippon Telesoft in due gruppi con funzionalità diverse:

* [Seika Versione 3, 4, e 5 (40 celle), Seika80 (80 celle), conosciuti in Italia come Touchme](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 celle), V6, e V6Pro (40 celle), conosciuti in Italia come Luce e ArgoBraille](#SeikaNotetaker)

Si possono reperire maggiori informazioni sui display nella loro [pagina di download di demo e driver](https://en.seika-braille.com/down/index.html).

#### Seika Versione 3, 4, e 5 (40 celle), Seika80 (80 celle) {#SeikaBrailleDisplays}

* Questi display non supportano ancora la funzionalità di rilevamento automatico del display braille in background di NVDA.
* Quindi, bisogna selezionare "Seika Braille Displays" per configurarli manualmente
* È necessario installare un driver per il dispositivo prima di utilizzare Seika v3/4/5/80.
I driver sono [forniti dal produttore](https://en.seika-braille.com/down/index.html).

Seguono le assegnazioni dei tasti del display Braille Seika.
Si prega di consultare la documentazione del display per le descrizioni di dove si trovano fisicamente i tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri indietro il display braille |left|
|Scorri display braille in avanti |right|
|Sposta il display braille alla riga precedente |b3|
|Sposta il display braille alla riga successiva |b4|
|Commuta inseguimento braille |b5|
|Dire tutto |b6|
|tab |b1|
|shift+tab |b2|
|alt+tab |b1+b2|
|Menu NVDA |left+right|
|Route to braille cell |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 celle), V6, e V6Pro (40 celle) {#SeikaNotetaker}

* La funzionalità di rilevamento automatico del display braille in background di NVDA è supportata tramite USB e Bluetooth.
* Selezionare "Seika Notetaker" o "automatico" per configurare questi display braille.
* Non sono richiesti driver aggiuntivi quando si utilizza un display braille Seika Notetaker.

Seguono le assegnazioni dei tasti per i display Braille Seika Notetaker.
Si prega di consultare la documentazione del display per le descrizioni di dove si trovano fisicamente i tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri indietro il display braille |left|
|Scorri display braille in avanti |right|
|Dire tutto |spazio+Backspace|
|Menu NVDA |Left+Right|
|Sposta il display braille alla riga precedente |LJ up|
|Sposta il display braille alla riga successiva |LJ down|
|Commuta inseguimento braille |LJ center|
|tab |LJ right|
|shift+tab |LJ left|
|Freccia su |RJ up|
|Freccia giù |RJ down|
|Freccia sinistra |RJ left|
|Freccia destra |RJ right|
|Route to braille cell |routing|
|shift+freccia su |Spazio+RJ up, Backspace+RJ up|
|shift+freccia giù |Spazio+RJ down, Backspace+RJ down|
|shift+freccia sinistra |Spazio+RJ left, Backspace+RJ left|
|shift+freccia destra |Spazio+RJ right, Backspace+RJ right|
|Tasto invio |RJ center, punto8|
|Tasto esc |Spazio+RJ center|
|Tasto windows |Backspace+RJ center|
|Spazio |Spazio, Backspace|
|backspace |punto7|
|pagina su |spazio+LJ right|
|pagina giù |spazio+LJ left|
|inizio |spazio+LJ up|
|fine |spazio+LJ down|
|control+home |backspace+LJ up|
|control+end |backspace+LJ down|

### Nuovi modelli Papenmeier BRAILLEX {#Papenmeier}

Sono supportati i seguenti display braille: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB e bluetooth)
* BRAILLEX Live 20, BRAILLEX Live e BRAILLEX Live Plus (USB e bluetooth)

Questi modelli non supportano ancora la funzione di rilevamento automatica in background.
C'è un'opzione nel driver USB del display che può causare problemi con il caricamento della barra braille.
Provare quanto segue:

1. Assicurarsi di aver installato [il driver più recente](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Aprire gestione dispositivi di Windows.
1. Scorrere l'elenco fino a "Controller USB" o "Dispositivi USB".
1. Selezionare "Dispositivo USB Papenmeier Braillex".
1. Aprire le proprietà e passare alla scheda "Avanzate".
A volte la scheda "Avanzate" non viene visualizzata.
In questo caso, scollegare la barra Braille dal computer, uscire da NVDA, attendere qualche istante e ricollegare il display Braille.
Se necessario, ripetere l'operazione 4-5 volte.
Se la scheda "Avanzate" ancora non viene visualizzata, riavviare il computer.
1. Disabilitare l'opzione "Carica VCP".

La maggior parte dei dispositivi è dotata di una barra di navigazione facilitata (EAB) che permette di svolgere le operazioni in una modalità molto più rapida ed intuitiva..
Questa barra può essere spostata in quattro direzioni e ciascuna direzione ha due posizioni.
la serie C e la serie Live sono le uniche eccezioni a questa regola.

Tali serie ed alcuni altri display presentano due file di cursor routing dove la riga superiore viene utilizzata per ottenere informazioni sulla formattazione.
Tenendo premuto uno dei tasti della fila superiore e spostando la barra di accesso rapido nella serie C, si simula la seconda posizione della EAB.
Mantenendo premuti i tasti su, giù, destra e sinistra (o EAB) permetterà di ripetere l'azione corrispondente..
I display della serie Live hanno solo una riga di cursor routing e la EAB si sposta di un solo scatto per ciascuna direzione.
Il secondo scatto può essere emulato premendo uno dei tasti di routing e premendo l'EAB nella direzione corrispondente.

In genere, sono disponibili i seguenti tasti in questi display braille::

| Nome |Tasto|
|---|---|
|l1 |Tasto sinistro frontale|
|l2 |Tasto sinistro posteriore|
|r1 |tasto destro frontale|
|r2 |tasto destro posteriore|
|up |uno scatto in su|
|up2 |2 scatti in su|
|left |1 scatto a sinistra|
|left2 |2 scatti a sinistra|
|right |1 Scatto a destra|
|right2 |2 Scatti a destra|
|dn |1 Scatto in basso|
|dn2 |2 Scatti in basso|

Seguono i comandi per i Display Papenmeier associati con NVDA:
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri Display braille indietro |left|
|Scorri Display Braille avanti |right|
|Sposta Display Braille alla riga precedente |up|
|Sposta Display Braille alla riga successiva |dn|
|Route to braille cell |routing|
|Annuncia il carattere attuale sul cursore di controllo |l1|
|Attiva l'oggetto corrente |l2|
|Commuta inseguimento Braille |r2|
|Annuncia Titolo |l1+up|
|Annuncia barra di stato |l2+down|
|Spostarsi all'oggetto contenitore |up2|
|Spostarsi al primo oggetto contenuto |dn2|
|Spostarsi all'oggetto precedente |left2|
|Spostarsi all'oggetto successivo |right2|
|Mostra formattazione testo sulle celle braille |Riga cursor routing superiore|

<!-- KC:endInclude -->

I modelli Trio dispongono di ulteriori quattro tasti aggiuntivi presenti sulla parte frontale della tastiera braille.
Partendo da sinistra verso destra, essi sono:

* left thumb key (lt)
* spazio
* spazio
* right thumb key (rt)

Attualmente, il tasto right Thumb key non viene utilizzato.
I tasti più interni svolgono la funzione di barra spaziatrice.

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|escape |spazio con punto 7|
|Freccia su| spazio con punto 2|
|Freccia sinistra |spazio con punto 1|
|Freccia Destra |spazio con punto 4|
|Freccia giù |spazio con punto 5|
|control |lt+punto2|
|alt |lt+punto3|
|control+escape |spazio con punto 1 2 3 4 5 6|
|tab |spazio con punto 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BRAILLEX vecchi modelli {#PapenmeierOld}

Sono supportati i seguenti display braille:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Si noti che questi display braille si possono connettere solo tramite porta seriale.
Per questo motivo, questi modelli non supportano la funzione di rilevamento automatica in background.
è quindi necessario selezionare la porta esatta alla quale la barra braille è connessa, dopo aver scelto il driver dalla finestra [Selezione Display Braille](#SelectBrailleDisplay). 

La maggior parte dei dispositivi è dotata di una barra di navigazione facilitata (EAB) che permette di svolgere le operazioni in una modalità molto più rapida ed intuitiva..
Questa barra può essere spostata in quattro direzioni e ciascuna direzione ha due posizioni.
La pressione prolungata verso l'alto, basso, destra o sinistra dei tasti o della EAB fa in modo che l'azione corrispondente venga ripetuta.
I dispositivi più vecchi non sono equipaggiati con la EAB. Vengono utilizzati i tasti frontali.

In genere, sono disponibili i seguenti tasti in questi display braille::

| Nome |Tasto|
|---|---|
|l1 |Tasto sinistro frontale|
|l2 |Tasto sinistro posteriore|
|r1 |tasto destro frontale|
|r2 |tasto destro posteriore|
|up |uno scatto in su|
|up2 |2 scatti in su|
|left |1 scatto a sinistra|
|left2 |2 scatti a sinistra|
|right |1 Scatto a destra|
|right2 |2 Scatti a destra|
|dn |1 Scatto in basso|
|dn2 |2 Scatti in basso|

Seguono i comandi per i Display Papenmeier associati con NVDA:

<!-- KC:beginInclude -->
Dispositivi con EAB

| Nome |Tasto|
|---|---|
|Scorri Display braille indietro |left|
|Scorri Display Braille avanti |right|
|Sposta Display Braille alla riga precedente |up|
|Sposta Display Braille alla riga successiva |dn|
|Route to braille cell |routing|
|Annuncia il carattere attuale sul cursore di controllo |l1|
|Attiva l'oggetto corrente |l2|
|Annuncia Titolo |l1+up|
|Annuncia barra di stato |l2+down|
|Spostarsi all'oggetto contenitore |up2|
|Spostarsi al primo oggetto contenuto |dn2|
|Spostarsi all'oggetto precedente |left2|
|Spostarsi all'oggetto successivo |right2|
|Mostra formattazione testo sulle celle braille |Riga cursor routing superiore|

BRAILLEX Tiny:

| Nome |Tasto|
|---|---|
|Annuncia carattere attuale in modalità navigazione |l1|
|Attiva oggetto corrente |l2|
|Scorri display braille indietro |left|
|Scorri display braille avanti |right|
|Sposta display braille alla riga precedente |up|
|Sposta display braille alla riga successiva |dn|
|Commuta inseguimento braille |r2|
|Spostarsi all'oggetto contenitore |r1+up|
|Spostarsi al primo oggetto contenuto |r1+dn|
|Spostarsi all'oggetto precedente |r1+left|
|Spostarsi all'oggetto successivo |r1+right|
|Annuncia formattazione testo |reportf|
|Leggi titolo |l1+up|
|Leggi barra di stato |l2+down|

BRAILLEX 2D Screen:

| Nome |Tasto|
|---|---|
|Annuncia carattere attuale in modalità navigazione |l1|
|Attiva oggetto corrente |l2|
|Commuta inseguimento braille |r2|
|Annuncia formattazione testo |reportf|
|Sposta display braille alla riga precedente |up|
|Sposta display braille indietro |left|
|Sposta display braille avanti |right|
|Sposta display braille alla riga successiva |dn|
|Spostarsi all'oggetto successivo |left2|
|Spostarsi all'oggetto contenitore |up2|
|Spostarsi al primo oggetto contenuto |dn2|
|Spostarsi all'oggetto precedente |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA supporta la famiglia di barre Braillenote della [Humanware](https://www.humanware.com) quando configurati per operare come terminali per screen reader.
Sono supportati i seguenti modelli:

* BrailleNote Classic (solo connessione seriale)
* BrailleNote PK (Connessione seriale e bluetooth )
* BrailleNote MPower (connessione seriale e bluetooth)
* BrailleNote Apex (connessione USB e Bluetooth)

Per il BrailleNote Touch, si prega di fare riferimento alla [sezione [Brailliant BI Series / BrailleNote Touch](#HumanWareBrailliant).

Ad eccezione del BrailleNote Pk, sono supportate sia tastiere braille (bt) che qwerty (qt).
Per il BrailleNote QT, non è supportata l'emulazione tastiera pc.
è anche possibile inserire i punti braille utilizzando la tastiera Qwerty.
Si prega di consultare la sezione terminale del manuale del BrailleNote per ulteriori informazioni.

Se il proprio dispositivo supporta più di un tipo di connessione, quando si connette il Braillenote a NVDA, è necessario impostare la porta nelle opzioni terminale braille del Braillenote.
Si prega di consultare il manuale del Braillenote per maggiori informazioni.
In NVDA, potrebbe anche essere necessario impostare la porta nella finestra [Selezione Display Braille](#SelectBrailleDisplay). 
Se ci si connette via USB o bluetooth, è possibile impostare la porta su "Automatico", "USB" o "Bluetooth", a seconda delle scelte disponibili.
Se ci si collega tramite una porta seriale (o un convertitore da USB a seriale) o se nessuna delle opzioni precedenti è disponibile, è necessario scegliere la porta di comunicazione da utilizzare dall'elenco delle porte hardware.

Prima di collegare il BrailleNote Apex utilizzando la sua interfaccia USB, è necessario installare i driver forniti da HumanWare.

Nel BrailleNote Apex BT, è possibile usare la rotella di scorrimento, situata tra i punti 1 e 4, per vari comandi di NVDA.
La rotella è formata da quattro punti direzionali, un pulsante centrale per cliccare e una rotella che gira in senso orario o in senso antiorario.

Seguono i tasti che sono stati assegnati con NVDA a Braillenote.
Si prega di consultare la documentazione del BrailleNote per informazioni su dove siano situati i tasti.

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorre Display Braille indietro |back|
|Scorre Display Braille avanti |advance|
|Sposta Display Braille alla riga precedente |previous|
|Sposta display braille alla riga successiva |next|
|Route to braille cell |routing|
|Menu NVDA |spazio+punto1+punto3+punto4+punto5 (spazio+n)|
|Commuta inseguimento braille |previous+next|
|Freccia su |spazio+punto1|
|Freccia giù |spazio+punto4|
|Freccia sinistra |spazio+punto3|
|Freccia destra |spazio+punto6|
|Pagina su |spazio+punto1+punto3|
|Pagina giù |spazio+punto4+punto6|
|Tasto Home |spazio+punto1+punto2|
|Tasto End |spazio+punto4+punto5|
|Control+home |spazio+punto1+punto2+punto3|
|Control+end |spazio+punto4+punto5+punto6|
|Spazio |spazio|
|Invio |spazio+punto8|
|Backspace |spazio+punto7|
|Tasto Tab| spazio+punto2+punto3+punto4+punto5 (spazio+t)|
|Shift+tab |spazio+punto1+punto2+punto5+punto6|
|Tasto Windows |spazio+punto2+punto4+punto5+punto6 (spazio+w)|
|Tasto Alt |spazio+punto1+punto3+punto4 (spazio+m)|
|Commuta aiuto immissione |spazio+punto2+punto3+punto6 (spazio+h abbassata)|

Di seguito i comandi relativi al BrailleNote QT quando non è impostato in modalità immissione braille.

| Nome |Tasto|
|---|---|
|menu NVDA |read+n|
|Tasto Freccia su |FrecciaSu|
|Tasto Freccia giù |FrecciaGiù|
|Tasto Freccia sinistra |FrecciaSinistra|
|Tasto freccia destra |FrecciaDestra|
|Tasto pagina su |function+frecciaSu|
|Tasto pagina giù |function+frecciaGiù|
|Tasto Home |function+frecciaSinistra|
|Tasto End |function+frecciaDestra|
|Control+home |read+t|
|Control+end |read+b|
|Tasto Invio |Invio|
|Tasto Backspace |backspace|
|Tasto Tab |tab|
|Shift+tab |shift+tab|
|Tasto Windows |read+w|
|Tasto Alt |read+m|
|Attiva/disattiva aiuto immissione |read+1|

Di seguito i comandi assegnati alla rotella di scorrimento:

| Nome |Tasto|
|---|---|
|Tasto Freccia su |FrecciaSu|
|Tasto Freccia giù |FrecciaGiù|
|Tasto Freccia sinistra |FrecciaSinistra|
|Tasto freccia destra |FrecciaDestra|
|Tasto Invio |Pulsante centrale|
|Tasto Tab |rotella senso orario|
|Shift+tab |rotella senso antiorario|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA supporta i Display Braille EcoBraille prodotti da [ONCE](https://www.once.es/).
Sono supportati i seguenti modelli:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

In NVDA, è possibile impostare la porta seriale a cui il display braille è collegato nella finestra di dialogo [Selezione Display Braille](#SelectBrailleDisplay). 
Questi modelli non supportano la funzione di rilevazione automatica in background.

Di seguito sono riportati i tasti assegnati per il display EcoBraille.
Si prega di consultare la [documentazione EcoBraille](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) per una descrizione sulla posizione dei tasti.

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorrimento indietro |T2|
|Scorrimento avanti |T4|
|Spostarsi alla riga precedente |T1|
|Spostarsi alla riga successiva |T5|
|Route to braille cell |Routing|
|Attivare oggetto corrente |T3|
|Modalità revisione successiva |F1|
|Spostarsi all'oggetto contenitore |F2|
|Modalità revisione precedente |F3|
|Spostarsi all'oggetto precedente |F4|
|Annunciare oggetto corrente |F5|
|Spostarsi all'oggetto successivo |F6|
|Spostarsi all'oggetto che ha il focus |F7|
|Spostarsi al primo oggetto contenuto |F8|
|Spostare il cursore di sistema alla posizione corrente del cursore di controllo |F9|
|Leggi la posizione del cursore di controllo |F0|
|Commuta inseguimento braille |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

Il dispositivo SuperBraille, conosciuto soprattutto in Taiwan, può essere connesso o tramite USB o porta seriale.
Dato che la barra braille non dispone di tasti di immissione per la scrittura o pulsanti per lo scorrimento, qualsiasi funzione deve essere inserita attraverso la tastiera del pc.
A causa di ciò, e per mantenere una buona compatibilità con altri screen reader in Taiwan, sono stati previste in NVDA due combinazioni di tasti per scorrere con la barra braille:
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorrimento display braille indietro |Meno del tastierino numerico|
|Scorrimento display braille avanti |Più del tastierino numerico|

<!-- KC:endInclude -->

### Display Eurobraille {#Eurobraille}

I display b.book, b.note, Esys, Esytime e Iris di Eurobraille sono supportati da NVDA.
Queste barre braille dispongono di una tastiera braille con dieci tasti.
Fare riferimento alla documentazione del display per le descrizioni di questi tasti.
Dei due tasti disposti come una barra spaziatrice, il tasto sinistro corrisponde al tasto indietro e il tasto destro al tasto spazio.

Questi dispositivi sono collegati tramite USB e dispongono di una tastiera USB autonoma.
È possibile abilitare o disabilitare tale tastiera assegnando un gesto personalizzato per la voce "Simulazione tastiera HID".
Le funzioni della tastiera braille descritte di seguito prevedono che la "simulazione della tastiera HID" sia disabilitata.

#### Funzioni tastiera braille {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Cancella l'ultima cella o carattere braille inserito |`backspace`|
|Transcodifica qualsiasi input braille e premi il tasto Invio |`backspace+space`|
|Attiva/disattiva il tasto `NVDA` |`punto3+punto5+spazio`|
|tasto `insert` |`punto1+punto3+punto5+spazio`, `punto3+punto4+punto5+spazio`|
|tasto `cancella` |`punto3+punto6+spazio`|
|Tasto `inizio` |`punto1+punto2+punto3+spazio`|
|Tasto `fine` |`punto4+punto5+punto6+spazio`|
|Tasto `freccia sinistra` |`punto2+spazio`|
|Tasto `freccia destra` |`punto5+spazio`|
|Tasto `freccia su` |`punto1+spazio`|
|Tasto `freccia giù` |`punto6+spazio`|
|Tasto `pagina su` |`punto1+punto3+spazio`|
|Tasto `pagina giù` |`punto4+punto6+spazio`|
|Tasto `1 del tastierino numerico` |`punto1+punto6+backspace`|
|Tasto `2 del tastierino numerico` |`punto1+punto2+punto6+backspace`|
|Tasto `3 del tastierino numerico` |`punto1+punto4+punto6+backspace`|
|Tasto `4 del tastierino numerico` |`punto1+punto4+punto5+punto6+backspace`|
|Tasto `5 del tastierino numerico` |`punto1+punto5+punto6+backspace`|
|Tasto `6 del tastierino numerico` |`punto1+punto2+punto4+punto6+backspace`|
|Tasto `7 del tastierino numerico` |`punto1+punto2+punto4+punto5+punto6+backspace`|
|Tasto `8 del tastierino numerico` |`punto1+punto2+punto5+punto6+backspace`|
|Tasto `9 del tastierino numerico` |`punto2+punto4+punto6+backspace`|
|Tasto `Insert del tastierino numerico` |`punto3+punto4+punto5+punto6+backspace`|
|Tasto `punto del tastierino numerico` |`punto2+backspace`|
|Tasto `barra del tastierino numerico` |`punto3+punto4+backspace`|
|Tasto `asterisco del tastierino numerico` |`punto3+punto5+backspace`|
|Tasto `meno del tastierino numerico` |`punto3+punto6+backspace`|
|Tasto `più del tastierino numerico` |`punto2+punto3+punto5+backspace`|
|Tasto `invio del tastierino numerico` |`punto3+punto4+punto5+backspace`|
|tasto `escape` |`punto1+punto2+punto4+punto5+spazio`, `l2`|
|Tasto `tab` |`punto2+punto5+punto6+spazio`, `l3`|
|Tasti `maiusc+tab` |`punto2+punto3+punto5+spazio`|
|Tasto `printScreen` |`punto1+punto3+punto4+punto6+spazio`|
|Tasto `pausa` |`punto1+punto4+spazio`|
|Tasto `applicazioni` |`punto5+punto6+backspace`|
|Tasto `f1` |`punto1+backspace`|
|Tasto `f2` |`punto1+punto2+backspace`|
|Tasto `f3` |`punto1+punto4+backspace`|
|Tasto `f4` |`punto1+punto4+punto5+backspace`|
|Tasto `f5` |`punto1+punto5+backspace`|
|Tasto `f6` |`punto1+punto2+punto4+backspace`|
|Tasto `f7` |`punto1+punto2+punto4+punto5+backspace`|
|Tasto `f8` |`punto1+punto2+punto5+backspace`|
|Tasto `f9` |`punto2+punto4+backspace`|
|Tasto `f10` |`punto2+punto4+punto5+backspace`|
|Tasto `f11` |`punto1+punto3+backspace`|
|Tasto `f12` |`punto1+punto2+punto3+backspace`|
|Tasto `Windows` |`punto1+punto2+punto4+punto5+punto6+spazio`|
|Attiva/disattiva tasto `windows` |`punto1+punto2+punto3+punto4+backspace`, `punto2+punto4+punto5+punto6+spazio`|
|Tasto `capsLock` |`punto7+backspace`, `punto8+backspace`|
|Tasto `blocnum` |`punto3+backspace`, `punto6+backspace`|
|Tasto `shift` |`punto7+spazio`|
|Attiva/disattiva tasto `shift` |`punto1+punto7+spazio`, `punto4+punto7+spazio`|
|Tasto `control` |`punto7+punto8+spazio`|
|Attiva/disattiva tasto `control` |`punto1+punto7+punto8+spazio`, `punto4+punto7+punto8+spazio`|
|Tasto `alt` |`punto8+spazio`|
|Attiva/disattiva tasto `alt` |`punto1+punto8+spazio`, `punto4+punto8+spazio`|
|Attiva/Disattiva simulazione tastiera HID |`switch1Left+joystick1Giù`, `switch1Right+joystick1giù`|

<!-- KC:endInclude -->

#### comandi da tastiera b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri il display braille indietro |`indietro`|
|Scorri il display braille in avanti |`avanti`|
|Vai al focus attuale |`indietro+avanti`|
|Route to braille cell |`routing`|
|Tasto `freccia sinistra` |`joystick2sinistra`|
|Tasto `freccia destra` |`joystick2Destra`|
|Tasto `freccia su` |`joystick2Su`|
|Tasto `freccia giù` |`joystick2Giù`|
|tasto `invio` |`joystick2Center`|
|tasto `escape` |`c1`|
|Tasto `tab` |`c2`|
|Attiva/disattiva tasto `shift` |`c3`|
|Attiva/disattiva tasto `control` |`c4`|
|Attiva/disattiva tasto `alt` |`c5`|
|Attiva/disattiva tasto `NVDA` |`c6`|
|Tasto `control+Inizio` |`c1+c2+c3`|
|Tasto `control+Fine` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### Comandi da tastiera b.note {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri il display braille indietro |`leftKeypadLeft`|
|Scorri il display braille in avanti |`leftKeypadRight`|
|Route to braille cell |`routing`|
|Annuncia formattazione del testo sotto la cella braille |`doubleRouting`|
|Vai alla riga successiva in modalità cursore di controllo| `leftKeypadDown`|
|Passa alla modalità revisione precedente |`leftKeypadLeft+leftKeypadUp`|
|Passa alla modalità revisione successiva |`leftKeypadRight+leftKeypadDown`|
|tasto `frecciaSinistra` |`rightKeypadLeft`|
|Tasto `freccia Destra` |`rightKeypadRight`|
|tasto `frecciaSu` |`rightKeypadUp`|
|Tasto `frecciaGiù` |`rightKeypadDown`|
|Tasto `control+inizio` |`rightKeypadLeft+rightKeypadUp`|
|Tasto `control+fine` |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Comandi da tastiera Esys {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri il display braille indietro |`switch1Left`|
|Scorri il display braille avanti |`switch1Right`|
|Vai al focus corrente |`switch1Center`|
|Route to braille cell |`routing`|
|Annuncia formattazione del testo sotto la cella braille |`doubleRouting`|
|Vai alla riga precedente con cursore di controllo |`joystick1Up`|
|Vai alla riga successiva con cursore di controllo |`joystick1Down`|
|Vai al carattere precedente con cursore di controllo |`joystick1Left`|
|Passa al carattere successivo con cursore di controllo |`joystick1Right`|
|Tasto `frecciasinistra` |`joystick2Left`|
|Tasto `frecciaDestra` |`joystick2Right`|
|Tasto `frecciaSu` |`joystick2Su`|
|Tasto `frecciaGiù` |`joystick2Down`|
|tasto `invio` |`joystick2Center`|

<!-- KC:endInclude -->

#### Comandi tastiera Esytime {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri il display braille indietro |`l1`|
|Scorri il display braille avanti |`l8`|
|Vai al focus corrente |`l1+l8`|
|Route to braille cell |`routing`|
|Annuncia formattazione del testo sotto la cella braille |`doubleRouting`|
|Vai alla riga precedente con cursore di controllo |`joystick1Up`|
|Vai alla riga successiva con cursore di controllo |`joystick1Down`|
|Vai al carattere precedente con cursore di controllo |`joystick1Left`|
|Vai al carattere successivo con cursore di controllo |`joystick1Right`|
|Tasto `frecciaSinistra` |`joystick2Left`|
|Tasto `frecciaDestra` |`joystick2Right`|
|Tasto `frecciaSu` |`joystick2Up`|
|Tasto `frecciaGiù` |`joystick2Down`|
|tasto `invio` |`joystick2Center`|
|tasto `escape` |`l2`|
|Tasto `tab` |`l3`|
|Attiva/disattiva tasto `shift` |`l4`|
|Attiva/disattiva tasto `control` |`l5`|
|Attiva/disattiva tasto `alt` |`l6`|
|Attiva/disattiva tasto `NVDA` |`l7`|
|Tasto `control+inizio` |`l1+l2+l3`, `l2+l3+l4`|
|Tasto `control+fine` |`l6+l7+l8`, `l5+l6+l7`|
|Attiva/Disattiva simulazione Tastiera HID |`l1+joystick1Giù`, `l8+joystick1Giù`|

<!-- KC:endInclude -->

### Display Braille Nattiq serie N {#NattiqTechnologies}

NVDA supporta i display braille prodotti dalla [Nattiq Technologies](https://www.nattiq.com/) se connessi via USB.
Windows 10 e versioni successive rileva automaticamente la barra braille non appena connessa, mentre è necessario installare i driver manualmente nel caso si utilizzi una versione di Windows più vecchia di Windows10.
è possibile scaricare i driver dal sito web dell'azienda.

Seguono i tasti che sono stati associati per questi modelli a NVDA.
Consultare la documentazione della barra braille per informazioni sulla posizione dei tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri display braille indietro back |su|
|Scorri Display Braille avanti |giù|
|Sposta display braille alla riga precedente |sinistra|
|Sposta Display Braille alla riga successiva |destra|
|Funzioni di cursor routing |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.com) è un programma a parte del quale è possibile avvalersi per avere supporto per molte altre barre braille. 
Per poterlo utilizzare, è necessario installare [BRLTTY per Windows](https://www.brltty.com/download.htm).
Si deve scaricare ed installare l'ultimo pacchetto Installer, che è chiamato, ad esempio, brltty-win-4.2-2.exe. 
Quando si configura la Barra Braille e la porta da utilizzare, si prega di fare attenzione alle istruzioni presentate a schermo, specialmente in caso si possieda un modello USB e sono già installati nel sistema i Driver prodotti dalla casa madre.

Per i display che possiedono già una tastiera braille, Brltty gestisce autonomamente la procedura di immissione e traduzione del testo dal braille.
Pertanto, le impostazioni tabella braille di immissione non sono rilevanti.

BRLTTY non è coinvolto nelle funzioni di rilevamento automatico display braille di NVDA.

Seguono i tasti che sono stati assegnati con NVDA a Brltty.
Si legga la [tabella dei tasti di Brltty](http://mielke.cc/brltty/doc/KeyBindings/) per comprendere come i comandi di Brltty sono mappati sul Display Braille.
<!-- KC:beginInclude -->

| Nome |comando BRLTTY|
|---|---|
|Scorre Display Braille indietro |`fwinlt` (va indietro di una finestra)|
|Scorre Display Braille avanti |`fwinrt` (va avanti di una finestra)|
|Sposta il Display Braille alla riga precedente |`lnup` (va su di una riga)|
|Sposta il Display Braille alla riga successiva |`lndn` (va giù di una riga)|
|Route to braille cell |`route` (porta il cursore al carattere)|
|Attiva / disattiva aiuto tastiera |`learn` (entra/esce dalla modalità apprendimento comandi)|
|Apre il menu di NVDA |`prefmenu` (Entra/esce dal menu preferenze)|
|Ripristina la configurazione |`prefload` (ripristina le preferenze dal disco)|
|Salva configurazione |`prefsave` (salva le preferenze su disco)|
|Annuncio orario |`time` (mostra la data e l'ora correnti)|
|Legge la riga alla posizione del cursore di controllo |`say_line` (Legge la riga corrente)|
|Dire tutto usando il cursore di controllo |`say_below` (Legge dalla posizione della riga corrente fino a fine schermo)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

I dispositivi Caiku Albatross, prodotti da Tivomatic e disponibili in Finlandia, possono essere collegati tramite USB o seriale.
Non è necessario installare alcun driver specifico per utilizzare questi display.
è sufficiente collegare il display e configurare NVDA per usarli.

Nota: la velocità di trasmissione (baudrate) 19200 è fortemente consigliata.
Se necessario, impostare il valore di velocità baud su 19200 dal menu del dispositivo braille.
Sebbene il driver supporti una velocità di trasmissione di 9600, non vi è modo modo di controllare la velocità di trasmissione utilizzata dal display.
Poiché 19200 è il baud rate predefinito dalla barra, il driver utilizzerà quello come valore standard.
Se le velocità in baud non sono le stesse, il driver potrebbe comportarsi in modo imprevisto.

Seguono i tasti che sono stati associati per questi modelli a NVDA.
Consultare la documentazione della barra braille per informazioni sulla posizione dei tasti.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Va alla prima riga in modalità cursore di controllo |`home1`, `home2`|
|Va all'ultima riga in modalità cursore di controllo |`end1`, `end2`|
|Porta il navigatore ad oggetti sul focus attuale |`eCursor1`, `eCursor2`|
|Va al focus attuale |`cursor1`, `cursor2`|
|Sposta il mouse alla posizione del navigatore ad oggetti |`home1+home2`|
|Sposta il navigatore ad oggetti alla posizione del mouse e la legge |`end1+end2`|
|Sposta il focus sull'oggetto del navigatore |`eCursor1+eCursor2`|
|Commuta inseguimento braille |`cursor1+cursor2`|
|Sposta il display braille alla riga precedente |`up1`, `up2`, `up3`|
|Sposta il display braille alla riga successiva |`down1`, `down2`, `down3`|
|Scorre display braille indietro |`left`, `lWheelLeft`, `rWheelLeft`|
|Scorre display braille avanti |`right`, `lWheelRight`, `rWheelRight`|
|Route to braille cell |`routing`|
|Visualizza la formattazione del testo sulla cella braille |`secondary routing`|
|Cambia il modo in cui le informazioni contestuali sono presentate in braille |`attribute1+attribute3`|
|Passa tra le modalità parlare |`attribute2+attribute4`|
|Passa alla modalità di revisione precedente (oggetto, documento o schermo) |`f1`|
|Passa alla modalità di revisione successiva (oggetto, documento o schermo) |`f2`|
|Sposta il navigatore ad oggetti sull'oggetto che lo contiene |`f3`|
|Sposta il navigatore ad oggetti sul primo oggetto al proprio interno |`f4`|
|Sposta il navigatore ad oggetti sull'oggetto precedente |`f5`|
|Sposta il navigatore ad oggetti sull'oggetto successivo |`f6`|
|Legge l'oggetto attuale del navigatore |`f7`|
|Legge informazioni sulla posizione del testo o dell'oggetto in corrispondenza del cursore di controllo |`f8`|
|Mostra impostazioni braille |`f1+home1`, `f9+home2`|
|Legge la barra di stato e vi sposta il navigatore ad oggetti |`f1+end1`, `f9+end2`|
|Scorre tra le forme del cursore braille |`f1+eCursor1`, `f9+eCursor2`|
|Attiva o disattiva il cursore braille |`f1+cursor1`, `f9+cursor2`|
|Passa tra le modalità di visualizzazione messaggi in braille |`f1+f2`, `f9+f10`|
|Attiva o disattiva la visualizzazione della selezione in braille |`f1+f5`, `f9+f14`|
|Passa tra le scelte possibili della funzione "sposta il cursore di sistema con cursor routing anche quando il braille segue il cursore di controllo" |`f1+f3`, `f9+f11`|
|Esegue l'azione predefinita sull'oggetto attuale del navigatore |`f7+f8`|
|Legge data/ora |`f9`|
|Annuncia lo stato della batteria e il tempo rimanente se l'alimentazione non è collegata in |`f10`|
|Legge il titolo |`f11`|
|Legge la barra di stato |`f12`|
|Legge la riga corrente sul cursore dell'applicazione |`f13`|
|Dire tutto |`f14`|
|Legge il carattere corrente alla posizione del cursore di controllo |`f15`|
|Legge la riga del navigatore ad oggetti su cui si trova il cursore di controllo |`f16`|
|Legge la parola del navigatore ad oggetti su cui si trova il cursore di controllo |`f15+f16`|
|Sposta il cursore di controllo alla riga precedente del navigatore ad oggetti e la legge |`lWheelUp`, `rWheelUp`|
|Sposta il cursore di controllo alla riga precedente del navigatore ad oggetti e la legge |`lWheelDown`, `rWheelDown`|
|Tasto `Windows+d` (riduce a icona tutte le applicazioni) |`attribute1`|
|`Tasto Windows+e` (questo pc) |`attribute2`|
|Tasto `Windows+b` (Porta il focus sulla system tray) |`attribute3`|
|`Tasto Windows+i` (Impostazioni Windows) |`attribute4`|

<!-- KC:endInclude -->

### Display Standard HID Braille {#HIDBraille}

Questo è un driver sperimentale per la nuova specifica standard HID Braille, concordata nel 2018 da Microsoft, Google, Apple e diverse società di tecnologie assistive, tra cui NV Access.
La speranza è che tutti i modelli futuri di display Braille creati da qualsiasi produttore utilizzino questo protocollo standard che eliminerà la necessità di driver Braille specifici.

Il rilevamento automatico display braille di NVDA riconoscerà anche qualsiasi barra che supporti questo protocollo.

Di seguito sono riportate le assegnazioni dei tasti per questi display.
<!-- KC:beginInclude -->

| Nome |Tasto|
|---|---|
|Scorri il display braille indietro |pan left or rocker up|
|Scorri il display braille avanti |pan right or rocker down|
|Route to braille cell |routing set 1|
|Attiva/disattiva inseguimento braille |su+giù|
|Tasto freccia su |joystick su, dpad up o spazio+punto1|
|Tasto freccia giù |joystick giù, dpad down o spazio+punto4|
|Tasto freccia sinistra |spazio+punto3, joystick sinistra o dpad left|
|Tasto freccia destra |spazio+punto6, joystick destra o dpad right|
|tasto MAIUSC+TAB |spazio+punto1+punto3|
|Tasto tab |spazio+punto4+punto6|
|tasto alt |spazio+punto1+punto3+punto4 (spazio+m)|
|tasto esc |spazio+punto1+punto5 (spazio+e)|
|tasto invio |punto8, centro del joystick o dpad center|
|tasto windows |spazio+punto3+punto4|
|tasto alt+tab |spazio+punto2+punto3+punto4+punto5 (spazio+t)|
|Menu NVDA |spazio+punto1+punto3+punto4+punto5 (spazio+n)|
|tasto windows+d (minimizzare tutte le applicazioni) |spazio+punto1+punto4+punto5 (spazio+d)|
|Dire tutto |spazio+punto1+punto2+punto3+punto4+punto5+punto6|

<!-- KC:endInclude -->

## Argomenti avanzati {#AdvancedTopics}
### Modalità protetta {#SecureMode}

Gli amministratori di sistema potrebbero voler configurare NVDA per limitare l'accesso non autorizzato al computer.
NVDA consente l'installazione di componenti aggiuntivi personalizzati, che possono eseguire codice arbitrario, anche quando NVDA è elevato ai privilegi di amministratore.
Lo screen reader consente inoltre agli utenti di eseguire codice arbitrario tramite la console Python di NVDA.
La modalità protetta di NVDA impedisce agli utenti di modificare la propria configurazione e limita l'accesso non autorizzato al sistema.

NVDA viene avviato in modalità protetta quando eseguito nelle [schermate protette](#SecureScreens), a meno che non sia abilitato il [parametro a livello di sistema](#SystemWideParameters) `serviceDebug`..
Per forzare l'avvio di NVDA sempre in modalità protetta, usare il [parametro a livello di sistema](#SystemWideParameters) `forceSecureMode`. 
Si può avviare NVDA in modalità protetta anche tramite [l'opzione a riga di comando](#CommandLineOptions) `-s`.

La modalità protetta disabilita:

* Il salvataggio della configurazione e di altre impostazioni su disco
* Il salvataggio di gesti personalizzati su disco
* Le funzionalità dei [profili di configurazione](#ConfigurationProfiles) come la creazione, l'eliminazione, la ridenominazione dei profili, etc.
* Il caricamento delle cartelle di configurazione personalizzate utilizzando [l'opzione della riga di comando `-c`](#CommandLineOptions)
* L'aggiornamento di NVDA e creazione di copie portable
* l'[Add-on Store](#AddonsManager)
* La [console Python di NVDA](#PythonConsole)
* Il [visualizzatore log](#LogViewer) e le funzionalità di log
* Il [Visualizzatore braille](#BrailleViewer) e [visualizzatore sintesi vocale](#SpeechViewer)
* L'apertura di documenti esterni dal menu di NVDA, come la guida per l'utente o il file dei collaboratori.

Le copie installate di NVDA salvano la loro configurazione, inclusi i componenti aggiuntivi, in `%APPDATA%\nvda`.
Per impedire agli utenti di modificare direttamente la propria configurazione o i componenti aggiuntivi, dev'essere limitato anche l'accesso a questa cartella.

La modalità protetta non si può applicare per le copie portable di NVDA.
Questo vale anche per la copia temporanea di NVDA che viene eseguita all'avvio del programma di installazione.
Negli ambienti protetti, un utente in grado di lanciare un eseguibile portable comporta lo stesso rischio per la sicurezza indipendentemente dalla modalità protetta.
Si lascia agli amministratori di sistema il compito di limitare l'esecuzione di software non autorizzato sui propri sistemi, comprese le copie portable di NVDA.

Si tenga presente che ogni utente tende a configurare lo screen reader in modo diverso, cercando di creare un profilo il più adatto possibile alle proprie esigenze..
Ciò spesso include l'installazione e la configurazione di add-on personalizzati, che andranno valutati indipendentemente dallo screen reader.
La modalità protetta blocca le modifiche alla configurazione di NVDA, perciò prima di attivarla, è necessario assicurarsi che lo screen reader sia configurato correttamente.

### Schermate protette {#SecureScreens}

NVDA viene avviato in [modalità protetta](#SecureMode) quando eseguito nelle schermate protette, a meno che non sia abilitato il [parametro a livello di sistema](#SystemWideParameters) `serviceDebug`..

Quando NVDA è in modalità protetta, lo screen reader utilizza un particolare profilo di sistema per le preferenze.
Le preferenze dell'utente possono essere copiate [per essere utilizzate nelle schermate protette](#GeneralSettingsCopySettings).

Le schermate protette comprendono:

* La schermata di accesso di Windows
* La finestra di dialogo Controllo accesso utente, attiva quando si esegue un'azione come amministratore
  * Ciò comprende l'installazione di programmi

### Opzioni a riga di comando {#CommandLineOptions}

NVDA è in grado di accettare alcune opzioni a riga di comando per modificarne il comportamento all'avvio.
Si possono inserire tutti i parametri che si desiderano.
Queste opzioni possono essere digitate sia dalla finestra esegui di Windows, sia nelle proprietà di un collegamento sul desktop o semplicemente nella console prompt dei comandi.
Le opzioni devono essere separate da spazi, come del resto è consuetudine.
Per esempio, Un parametro molto utile è `--disable-addons`, che permette di sospendere tutti i componenti aggiuntivi all'avvio di NVDA.
Ciò permette di stabilire se un determinato problema è causato da un componente aggiuntivo e in quel caso poterlo risolvere senza che gli addon vengano eseguiti.

Per fare un esempio, è possibile uscire da NVDA digitando la stringa seguente nella finestra esegui di Windows:

    NVDA -q

Alcuni parametri possiedono una versione breve e lunga, altri invece soltanto una lunga.
Per quelli che possiedono solo la versione breve, si possono unire nel modo seguente:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |NVDA si avvierà con il messaggio e il suono iniziale disattivati, e con la configurazione specificata|
|`nvda -mc CONFIGPATH --disable-addons` |Come sopra, ma con i componenti aggiuntivi disattivati|

Alcune delle opzioni della riga di comando accettano parametri aggiuntivi; ad esempio quanto dettagliato debba essere il log oppure la cartella inerente il profilo di configurazione utente.
Questi parametri devono essere collocati dopo l'opzione, separati da essa da uno spazio in cui si utilizza la versione corta o un segno di uguale (`=`) quando si utilizza la versione lunga; ad esempio .:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Dice a NVDA di avviarsi con il log impostato su debug|
|`nvda --log-file=c:\nvda.log` |Dice a NVDA di scrivere il log in `c:\nvda.log`|
|`nvda --log-level=20 -f c:\nvda.log` |Dice a NVDA di avviarsi con livello di log impostato su info e di scrivere il log in `c:\nvda.log`|

Ecco l'elenco dei parametri a riga di comando di NVDA:

| Breve |Lungo |Descrizione|
|---|---|---|
|`-h` |`--help` |Visualizza l'aiuto sulla riga di comando ed esce|
|`-q` |`--quit` |Chiude eventuali copie in esecuzione di NVDA|
|`-k` |`--check-running` |Notifica se NVDA è in esecuzione tramite exit code; 0 se in esecuzione, 1 se non lo è|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |Il file nel quale verrà scritto il log. Le funzioni di log saranno sempre disabilitate se ci si trova in modalità protetta.|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |Il livello più basso di un messaggio loggato (debug 10, input/output 12, debug warning 15, info 20, disabled 100). Le funzioni di log saranno sempre disabilitate se ci si trova in modalità protetta.|
|`-c CONFIGPATH` |`--config-path=CONFIGPATH` |Il percorso ove sono salvate tutte le impostazioni di NVDA. Se ci si trova in modalità protetta verrà forzato il valore predefinito.|
|None |`--lang=LANGUAGE` |Sovrascrive la lingua configurata per NVDA. Impostarla a "Windows" per la lingua predefinita dell'utente, "en" per Inglese, etc.|
|`-m` |`--minimal` |Niente suoni, niente interfaccia, niente messaggio all'avvio etc|
|`-s` |`--secure` |Avvia NVDA in [modalità protetta](#SecureMode)|
|None |`--disable-addons` |I componenti aggiuntivi non avranno alcun effetto|
|None |`--debug-logging` |Abilita il debug nei log solo per la presente istanza. Questa impostazione ha la precedenza su qualsiasi altro livello di log ( `--loglevel`, `-l`), compresa la funzione no logging|
|None |`--no-logging` |Disabilita completamente le funzioni di log durante l'uso di NVDA. Questa impostazione può essere sovrascritta se viene specificato un livello di log ( `--loglevel`, `-l`) dalla riga di comando o se la funzione debug logging è attiva.|
|None |`--no-sr-flag` |Non modifica il flag Screen Reader per il sistema|
|None |`--install` |Installa NVDA (avviando la copia appena installata)|
|None |`--install-silent` | Installa NVDA (non avviando la copia appena installata)|
|None |`--enable-start-on-logon=True|False` |Durante l'installazione, abilita [l'avvio di NVDA alla schermata di logon](#StartAtWindowsLogon)|
|None |`--copy-portable-config` |Durante l'installazione, copia la configurazione portable dal percorso specificato (`--config-path`, `-c`) all'account utente corrente|
|None |`--create-portable` |Crea una copia portable di NVDA (avviando la copia appena creata). Richiede `--portable-path` da specificare|
|None |`--create-portable-silent` |Crea una copia portable di NVDA (non avvia la nuova copia appena creata). Richiede `--portable-path` da specificare|
|None |`--portable-path=PORTABLEPATH` |Il percorso in cui verrà creata la copia portable di NVDA|

### Parametri di sistema {#SystemWideParameters}

NVDA consente di impostare alcuni valori nel registro di sistema che andranno ad influenzare il comportamento dello screen reader.
Tali valori sono salvati nel registro in una delle seguenti chiavi:

* sistemi a 32-bit: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* Sistemi a 64-bit: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

Di seguito vengono elencati i valori modificabili con queste chiavi di registro:

| Nome |Tipo |Valori ammessi |Descrizione|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (predefinito) per disabilitare, 1 per abilitare |Se attivato, salva la configurazione utente di NVDA nella cartella locale dell'applicazione invece che in roaming application data|
|`serviceDebug` |DWORD |0 (predefinito) per disabilitare, 1 per abilitare |Se abilitata, disattiva la [Modalità protetta](#SecureMode) nelle [Schermate protette](#SecureScreens). A causa di diverse importanti implicazioni sulla sicurezza, l'uso di questa opzione è fortemente sconsigliato|
|`forceSecureMode` |DWORD |0 (predefinito) per disabilitare, 1 per abilitare |Se attivata, forza l'attivazione della [Modalità protetta](#SecureMode) all'avvio di NVDA.|

## Ulteriori Informazioni {#FurtherInformation}

Se si vogliono trovare maggiori informazioni o richiedere assistenza riguardo NVDA, si prega di consultare il [Sito internazionale di NVDA in lingua inglese](NVDA_URL), oppure quello relativo alla comunità italiana all'indirizzo [www.nvda.it](http://www.nvda.it).
In entrambe i siti web sarà possibile reperire documentazione aggiuntiva, supporto tecnico e risorse varie come forum o mailing list.
In particolare, per quanto concerne il sito italiano, esiste una lista di discussione alla quale chiunque può iscriversi mandando un messaggio a: <nvda-request@groups.io> e nell'oggetto del messaggio scrivere la parola "subscribe" senza le virgolette. Rispondere poi al messaggio di conferma. I messaggi che transitano nella mailing list sono tutti consultabili anche dal sito nvda.it, nel riquadro ultime notizie dal forum. Non esitate a contattarci in caso di problemi.