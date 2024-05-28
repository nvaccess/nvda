# Guía do Usuario do NVDA NVDA_VERSION

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Referencia Rápida de Ordes -->



## Introdución {#Introduction}

¡Benvido ao NVDA!

NonVisual Desktop Access (NVDA) é un lector de pantalla libre e de código aberto  para o Sistema Operativo  Microsoft Windows.
Proporcionando retroalimentación a través de voz sintética e Braille, posibilita á xente cega ou deficiente visual aceder a computadores executando o Windows por un custo non maior ao dunha persoa vidente.
NVDA está desenvolvido por [NV Access](https://www.nvaccess.org/), con  colaboracións da comunidade.

### Características Xerais {#GeneralFeatures}

Proporcionando un apoio de voz sintética, NVDA permite ás persoas cegas e deficientes visuais acceder e interactuar co Sistema Operativo Windows e moitas aplicacións de terceiros. 

Un vídeo curto de demostración (en inglés) ["What is NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) está dispoñible na canle NV Access YouTube.

O máis subliñable inclúe: 

* Soporte para aplicacións populares incluíndo navegadores web, clientes de correo, programas de chat en internet e suites de oficiña
* Sintetizador de voz incorporado que soporta sobre das 80 linguas
* Anunciado do formato de texto onde estea dispoñible como nome e tamano da fonte, estilo e erros de ortografía
* Anunciado automático do texto baixo o rato e indicación opcional audible  da posición do mesmo
* Soporte para moitas pantallas de braille efímero incluíndo a capacidade de detectar automáticamente moitas delas así como a entrada de braille computerizado para pantallas braille que tenñan un teclado braille
* Capacidade para executarse compretamente dende unha memoria USB ou outros medios portables sen a necesidade de instalación
* Instalador parlante sinxelo de utilizar
* Traducido a 54 linguas
* Soporte para Sistemas Operativos Windows modernos incluíndo variantes de 32 e 64 bit
* Capacidade para executarse durante o inicio de Windows e [noutras pantallas seguras](#SecureScreens).
* Anunciado de controis e texto mentres se usan xestos tactiles
* Soporte para interfaces comuns de accesibilidade como Microsoft Active Accessibility, Java Access Bridge, IAccessible2 e UI Automation
* Soporte para o símbolo do sistema de Windows e aplicacións de consola
* A capacidade de resaltar o foco do sistema

### Requerimentos do Sistema {#SystemRequirements}

* Sistemas operativos: todas as edicións de 32 e 64 bits do Windows 8.1, Windows 10 Windows 11 e todos os sistemas operativos servidor comezando dende o Windows Server 2008 R2..
 * As variantes AMD64 e ARM64 de Windows están soportadas.
* - Polo menos 150 MB de espazo de almacenamento.

### Internacionalización {#Internationalization}

É importante que calquera persoa no mundo, sen importar que lingua fale, teña igual acceso á tecnoloxía. 
Actualmente NVDA foi traducido a 54linguas ademáis da lingua inglesa incluíndo: Afrikáans, Albanés, Alemán (Alemania e Suiza), aragonés, Birmano, Búlgaro, catalán, Checo, Chinese Mandarín Chinese cantonés, Coreano, Croata, Danés, eslovaco, Esloveno, Español, Español de Colombia, Farsi, Finlandés, Francés, Galego, Grego, Hebreo, Hindi, Holandés, Húngaro, Irlandés, Islandés, Italiano, Kannada, Kirguistaní, Lituano, Nepalí, Noruego, Macedonio, Mongol, Polaco, Portugués, Portugués do Brasil, Punjabi, Rumano, Ruso, Servio, Sueco, Ucraniano, Tamil, Tailandés,, turco, Vietnamita, Xaponés e xeorxiano.

### Soporte da Síntesis de Voz {#SpeechSynthesizerSupport}

Ademáis de proporcionar as súas mensaxes e interface en varias linguas, NVDA tamén pode capacitar ao usuario para ler contidos en calquera lingua, tanto en canto teñan un sintetizador de voz que poida falar esa lingua en particular. 

NVDA ven integrado co [eSpeak NG](https://github.com/espeak-ng/espeak-ng), un sintetizador de voz multilingüe, libre, de código aberto.

Pódese atopar información acerca doutros sintetizadores de voz que soporta o NVDA na sección [Sintetizadores de Voz soportados](#SupportedSpeechSynths).

### Soporte Braille {#BrailleSupport}

Para usuarios que posúan unha pantalla de braille efímero, NVDA pode amosar a súa información en braille. 
O NVDA usa o transcriptor braille de código aberto [LibLouis](https://liblouis.io/) para xerar secuencias braille de texto.
Tamén se soporta tanto a entrada de braille sin contraer comacontraída a través dun teclado braille.
Ademáis, o NVDA detectará moitas pantallas braille automáticamente por defecto.
Por favor consulta a sección [Pantallas Braille Soportadas](#SupportedBrailleDisplays) para información acerca das liñas braille soportadas.

NVDA soporta códigos braille para moitas linguas,  incluíndo códigos braille contraído, non contraído e computerizado.

### Licencia e Copyright {#LicenseAndCopyright}

NVDA é copyright NVDA_COPYRIGHT_YEARS polos colaboradores do NVDA.

O NVDA está dispoñible baixo a GNU General Public License (Versión 2) con dúas excepcións especiais. 
As excepcións están dispoñibles en liña no documento de licencia nas secións "Non-GPL Components in Plugins and Drivers" e "Microsoft Distributable Code".
O NVDA tamén inclúe e usa  componentes que están dispoñibles baixo diferentes licencias libres e de código aberto.
es libre para compartir ou modificar este programa de calquer xeito que queras aíndaque debes distribuir a licencia xunto co programa, e facer todo o código fonte dispoñible a quen o queira. 
Esto aplícase ao orixinal e ás copias modificadas do programa, máis calquer software que utilice código tomado dende este programa. 

Para máis detalles, podes [ver a licencia completa.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
Para obter detalles sobre as escepcións, acesa ao documento de licencia dende o menú NVDA na seción "axuda".

## Guía de Inicio Rápido de NVDA {#NVDAQuickStartGuide}

Esta guía de inicio rápido contén tres secións principais: descargar, configuración inicial e executar o NVDA.
Éstas séguense por información sobre o axuste de preferencias, a participación na comunidade e a obtención de axuda.
A información nesta guía é un condensado de outras partes da guía do usuario de NVDA.
Por favor consulta a guía compreta do usuario para información máis detallada sobre cada tema.

### Descargar NVDA {#GettingAndSettingUpNVDA}

O NVDA é compretamente libre para quen o use.
Non hai que preocuparse por unha chave de licenza nin pagar unha custosa subscripción.
O NVDA actualízase, por termo medio, catro veces por ano.
A última versión do NVDA sempre está dispoñible dende a páxina de "Descargas" do [sitio web de NV Access](NVDA_URL).

O NVDA funciona con todas as versións recentes de Microsoft Windows.
Verifica os [Requerimentos do Sistema](#SystemRequirements) para todos os detalles.

#### Pasos para Descargar o NVDA {#StepsForDownloadingNVDA}

Estos pasos asumen algunha familiaridade coa navegación por unha páxina web.

* Abre o teu navegador web (Preme a tecla `Windows`, escrebe a palabra "internet" sen comiñas e preme `intro`)
* Carga a páxina de descargas de NV Access (Preme `alt+d`, escrebe o seguinte enderezo e preme `intro`): 
https://www.nvaccess.org/download 
* Activa o botón "download"
* O navegador pode ou non indicarche unha acción despois de descargar, e despois comeza a descarga
* Dependiendo do navegador, o ficheiro pode executarse automáticamente despois de que se descargue
* Se o ficheiro necesita lanzarse manualmente, preme `alt+n` para moverte á área de notificacións, entón `alt+r` para executar o ficheiro (ou os pasos para o teu navegador)

### Configurar o NVDA {#SettingUpNVDA}

Executando o ficheiro que descargaches comezará unha copia temporal do NVDA.
Entón preguntarásechete se queres instalar NVDA, crear unha copia portable, ou só continuar utilizando a copia temporal.

O NVDA non necesita acesar ao Internet para se executar ou para se instalar unha vez que o lanzador se descargou.
Se está dispoñible, unha conexión ao internet capacita ao NVDA a procurar actualizacións periódicamente.

#### Pasos para executar o lanzador descargado {#StepsForRunningTheDownloadLauncher}

O ficheiro de instalación chámase "nvda_2022.1.exe" ou similar.
O ano e a versión cambian entre actualizacións para refrectir a versión actual.

1. Executa o ficheiro descargado.
Reprodúcese unha música mentres unha copia temporal do NVDA se carga.
Unha vez cargada, o NVDA falará durante o resto do proceso.
1. A ventá do lanzador do NVDA aparece co acordo de licenza.
Preme `frecha Abaixo` para ler o acordo de licenza se o desexas.
1. Preme `tab` para desprazarte cara a caixa de verificación "Acepto", entón preme a `barra espaciadora` para marcala.
1. Preme `tab` para desprazarte polas opcións, entón preme `intro` sobre a opción desexada.

As opcións son: 

* "Instalar NVDA neste coputador": esta é a opción principal que a maioría dos usuarios do NVDA queren usar. 
* "Crear copia portable": esto permite que o NVDA se copie en calquera cartafol sen instalarse. 
Esto é útil en computadores sen dereitos de administrador, ou nunha memoria USB para levala contigo.
Ao se seleccionar, o NVDA segue os pasos para crear unha copia portable.
A principal cousa que o NVDA necesita coñecer é o cartafol para poñer a copia portable. 
* "Continuar executando": esto mantén a copia temporal do NVDA en execución.
Testo é útil para probar características nunha versión nova antes de instalala.
Ten en conta que os cambios nas opcións non se gardan. 
Ao se seleccionar, péchase a ventá do lanzador e a copia temporal do NVDA continúa executándose ate que se peche ou o PC se apague.
* "Cancelar": esto pecha o NVDA sen realizar ningunha ación.

Se prantexas usar sempre o NVDA neste coputador, quererás escoller instalar o NVDA.
Instalar o NVDA permitirache funcionalidades adicionais coma o arranque automático despois de autentificarte, a capacidade de ler a ventá do inicio de sesión de windows  e [pantallas seguras](#SecureScreens).
Esto non se pode facer con copias temporais ou portables.
Para detalles compretos das limitacións ao executar unha copia portable ou temporal do NVDA, por favor consulta [Restricións de copia Portable e temporal](#PortableAndTemporaryCopyRestrictions).

A instalación tamén che ofrece a creación de accesos directos para o menú Inicio e para o escritorio, e permite ao NVDA seren iniciado con `control+alt+n`.

#### Pasos para Instalar  o NVDA dende o lanzador {#StepsForInstallingNVDAFromTheLauncher}

Estos pasos percorren as opcións máis comúns.
Para máis detalles sobre as opcións dispoñibles, por favor consulta [Opcións de instalación](#InstallingNVDA).

1. Dende o lanzador, asegúrate de que a caixa de verificación para aceptar a licenza estea marcada.
1. Preme `Tab` e activa o botón "Instalar NVDA neste computador".
1. Seguidamente, van as opcións para que o NVDA use durante o inicio de sesión de windows e para crear un acceso directo no escritorio.
Están marcadas predeterminadamente.
1. Preme `intro` para continuar .
Se o desexas, preme `tab` e `barra espaciadora` para cambiar calquera destas opcións, ou déixaas como están por omisión.
1. Aparece un diálogo de Windows "Control de Conta de Usuario (UAC en inglés)" preguntándoche "¿Quere permitir que esta app faga cambios ao seu computador?".
1. Preme `alt+s` para aceptar o indicativo do UAC.
1. Rechéase unha barra de progreso según o NVDA se instale.
Durante este proceso o NVDA emite un pitido cada vez máis agudo.
Este proceso de cotío é rápido e pode non seren notificado.
1. Aparece una caixa de diálogo confirmando que a instalación do NVDA foi exitosa.
A mensaxe avísache de que "Premas Aceptar para arrancar a copia instalada".
Preme `intro` para iniciar a copia instalada.
1. Aparece o diálogo "Benvido a NVDA", e o NVDA le unha mensaxe de benvida.
O foco está na caixa combinada "Disposición do Teclado".
Por defecto, a disposición de teclado "Escritorio" usa o teclado numérico para algunhas funcións.
Se o desexas, preme `frecha abaixo` para escoller a disposición de teclado "Portátil" para reasignar as funcións do teclado numérico a outras teclas.
1. Preme `tab` para desprazarte cara "Usar `bloqMaius` coma unha tecla modificadora de NVDA".
`Insert` configúrase como a tecla modificadora de NVDA predeterminada.
Preme `barra espaciadora` para selecionar `bloqMaius` coma unha tecla modificadora alternativa.
Ten en conta que a disposición de teclado configúrase separadamente da tecla modificadora do NVDA.
A tecla NVDA e a disposición de teclado poden cambiarse máis tarde dende as opcións de teclado.
1. Usa `tab` e `barra espaciadora` para axustar as outras opcións nesta pantalla.
Estas estabrecen se o NVDA arranca automáticamente.
1. Preme `intro` para pechar a caixa de diálogo co NVDA agora en execución.

### Executar o NVDA {#RunningNVDA}

A guía compreta de usuario de NVDA ten todas as ordes de NVDA divididas en diferentes secións para a súa consulta.
As táboas de ordes tamén están dispoñibles na "Referencia Rápida de ordes".
O módulo "Formación Básica de NVDA" profundiza en cada orden con actividades paso a paso.
"Formación Básica de NVDA" está dispoñible dende a [tenda de NV Access](http://www.nvaccess.org/shop).

Aquí van algunhas ordes básicas que se usan a cotío.
Todas as ordes son configurables, polo que estas son as pulsacións predeterminadas para estas funcións.

#### A Tecla modificadora NVDA {#NVDAModifierKey}

A tecla modificadora predeterminada do NVDA é ou o `cero do teclado numérico`, (co `bloqNum` desactivado), ou a tecla `insert`, próxima ás teclas `supr`, `inicio` e `fin`.
A tecla modificadora do NVDA tamén pode configurarse na tecla `bloqMaius`.

#### Axuda de Entrada {#InputHelp}

Para deprender e practicar a localización das teclas, preme `NVDA+1` para activar a Axuda de Entrada.
Mentres se estea no modo Axuda de entrada, a realización de calquera xesto de entrada (coma premer unha tecla ou realizar un xesto táctil) anunciará a acción e describirá que fai (se fai algo).
As ordes reais non se executarán mentres se estea en modo axuda de entrada. 

#### Iniciar e deter o NVDA {#StartingAndStoppingNVDA}

| Nome |tecla de escritorio |Tecla de portátil |Descripción|
|---|---|---|---|
|Arrancar o NVDA |`control+alt+n` |`control+alt+n` |Inicia ou reinicia o NVDA|
|Saír do NVDA |`NVDA+q`, logo `intro` |`NVDA+q`, logo `intro` |Sae do NVDA|
|Pausar ou reiniciar a voz |`shift` |`shift` |Pausa instantáneamente a voz. Preméndoa de novo continuará falando onde se detivo|
|Deter voz |`control` |`control` |Detén instantáneamente a voz|

#### Ler texto {#ReadingText}

| Nome |Tecla de escritorio |Tecla de portátil |Descripción|
|---|---|---|---|
|Ler todo |`NVDA+frecha abaixo` |`NVDA+a` |Comeza a ler dende a posición actual, movéndose sobre a marcha|
|Ler liña actual |`NVDA+frecha arriba` |`NVDA+l` |Le a liña. Preméndoas dúas veces deletrea a liña. Preméndoas tres veces deletrea a liña usando a descripción de caracteres (Alfa, Bravo, Charlie, etc)|
|Ler a seleción. Premendo dúas veces deletreará a información. Premendo tres veces deletrearáa usando descripción de caracteres |`NVDA+shift+frecha arriba` |`NVDA+shift+s` |Le calquera texto selecionado|
|Ler texto do portapapeis |`NVDA+c` |`NVDA+c` |Le calquera texto no portapapeis. Premendo dúas veces deletreará a información. Premendo tres veces deletrearáa usando descripción de caracteres|

#### Anunciar localización e outra información {#ReportingLocation}

| Nome |Tecla de escritorio |Tecla de portátil |Descripción|
|---|---|---|---|
|Título de ventá |`NVDA+t` |`NVDA+t` |Anuncia o título da ventá actualmente activa. Preméndoo dúas veces deletreará a información. Preméndoo tres veces copiaráa ao portapapeis|
|Anunciar foco |`NVDA+tab` |`NVDA+tab` |Anuncia o control actual que teña o foco. Preméndoo dúas veces deletreará a información. Premendo tres veces deletrearáa usando descripción de caracteres|
|Ler ventá |`NVDA+b` |`NVDA+b` |Le toda a ventá actual (útil para diálogos)|
|Ler barra de estado |`NVDA+fin` |`NVDA+shift+fin` |Anuncia a Barra de Estado se o NVDA atopa unha. Preméndoo dúas veces deletreará a información. Preméndoo tres veces copiaráa ao portapapeis|
|Ler hora |`NVDA+f12` |`NVDA+f12` |Preméndoo unha vez anuncia a hora actual, preméndoo dúas veces anuncia a data. A hora e a data anúncianse no formato especificado na configuración de Windows para o reloxo da bandexa do sistema.|
|Anunciar formato de texto |`NVDA+f` |`NVDA+f` |Anuncia o formato do texto. Preméndoo dúas veces amosa a información nunha ventá|
|Anunciar destiño da ligazón |`NVDA+k` |`NVDA+k` |Premendo unha vez fala a URL de destiño da ligazón na posición actual do cursor do sistema ou do foco. Premendo dúas veces amósao nunha ventá para unha revisión máis cuidadosa|

#### Conmutar que información le o NVDA {#ToggleWhichInformationNVDAReads}

| Nome |Tecla de escritorio |Tecla de Portátil |Descripción|
|---|---|---|---|
|Falar caracteres ao se escreber |`NVDA+2` |`NVDA+2` |Cando se activa, o NVDA anunciará todos os caracteres que escrebas no teclado.|
|Falar palabras ao se escreber |`NVDA+3` |`NVDA+3` |Cando se habilita, o NVDA anunciará as palabras que escrebas no teclado.|
|Falar teclas de ordes |`NVDA+4` |`NVDA+4` |Cando se habilita, o NVDA anunciará todas as teclas que non sexan caracteres que escrebas no teclado. Esto inclúe combinacións de teclas coma control máis calquera outra letra.|
|Habilitar seguemento do rato |`NVDA+m` |`NVDA+m` |Cando se habilita, o NVDA anunciará o texto actualmente baixo o punteiro do rato según o despraces pola pantalla. Esto permíteche atopar cousas na pantalla, movendo físicamente o rato, a cambio de intentar atopalos coa navegación de obxectos.|

#### O anel de opcións do sintetizador {#TheSynthSettingsRing}

| Nome |Tecla de escritorio |Tecla de portátil |Descripción|
|---|---|---|---|
|Moverse á seguinte opción do anel do sintetizador |`NVDA+control+frecha dereita` |`NVDA+shift+control+frecha dereita` |Desprázase á seguinte opción de voz dispoñible despois da actual, voltando á primeira opción de novo tras a última|
|Moverse á anterior opción do anel do sintetizador |`NVDA+control+frecha esquerda` |`NVDA+shift+control+frecha esquerda` |Desprázase á seguinte opción de voz dispoñible antes da actual, voltando á última opción tras a primeira|
|Aumentar a opción actual do sintetizador |`NVDA+control+frecha arriba` |`NVDA+shift+control+frecha arriba` |Aumenta a opción de voz actual na que esteass. Ex.: aumenta a velocidade, escolle a seguinte voz, aumenta o volume|
|Aumentar a opción actual en pasos longos | ``NVDA+control+rePáx`` | ``NVDA+shift+control+rePáx`` | aumenta o valor da actual opción de voz sobre a que esteas en pasos grandes. Ex.: cando esteas sobre unha opción de voz, saltarás cara adiante cada 20 voces; cando esteas en opcións dun deslizador (velocidade, ton, etc) saltará adiante o valor de 20% |
|Disminuir a opción actual do sintetizador |`NVDA+control+frecha abaixo` |`NVDA+shift+control+frecha abaixo` |Disminúe a opción de voz actual na que esteas. Ex.: disminúe a velocidade, escolle a voz anterior, disminúe o volume|
|Diminuir a actual opción do sintetizador nun paso longo | ``NVDA+control+avPáx`` | ``NVDA+shift+control+avPáx`` | Diminúe o valor da actual opción de voz sobre a que esteas en pasos máis longos. ex.: cando esteas sobre unha opción de voz, saltará cara atrás cada 20 voces; cando esteas sobre unha opción de deslizador, saltará atrás o valor de 20%. |

Tamén é posible estabrecer o primeiro ou o último valor da actual opción do sintetizador asignando xestos persoalizados no [diálogo Xestos de Entrada #InputGestures], na categoría voz.
Esto significa, por exemplo, que cando esteas sobre unha opción de velocidade, estabreceráa a 0 ou a 100.
Cando esteas sobre unha opción de voz, estabrecerá a primeira ou a última voz.

#### Navegación Web {#WebNavigation}

A listaxe compreta das teclas de navegación cunha soa letra está na seción [Modo Navegación](#BrowseMode) da guía do usuario.

| Orden |Pulsación de tecla |Descripción|
|---|---|---|
|Cabeceira |`h` |Despraza á seguinte cabeceira|
|Cabeceira de nivel 1, 2, ou 3 |`1`, `2`, `3` |Despraza á seguinte cabeceira no nivel especificado|
|Campo de formulario |`f` |Despraza ao seguinte campo de formulario (caixa de edición, botón, etc)|
|Ligazón |`k` |Despraza á seguinte ligazón|
|Rexión |`d` |Despraza á seguinte rexión|
|Listaxe |`l` |Despraza á seguinte listaxe|
|Táboa |`t` |Despraza á seguinte táboa|
|Desprazarse atrás |`shift+letra` |Preme `shift` e calquera das letras de enriba para desprazarte ao elemento anterior dese tipo|
|Listaxe de elementos |`NVDA+f7` |Enumera varios tipos de elementos, coma ligas e cabeceiras|

### Preferencias {#Preferences}

A maioría das funcións do NVDA poden habilitarse ou cambiarse a través da configuración do NVDA.
A configuración e outras opcións están dispoñibles a través do menú NVDA.
Para abrir o menú NVDA, preme `NVDA+n`.
Para abrir directamente o diálogo Opcións Xerais de NVDA, preme `NVDA+control+g`.
Moitas pantallas de opcións teñen pulsacións de teclas para abrilas directamente, como `NVDA+control+s` para Sintetizador, ou `NVDA+control+v` para outras opcións de voz.

### Comunidade {#Community}

O NVDA ten unha vibrante comunidade de usuarios.
Hai unha [listaxe principal de correo electrónico en inglés](https://nvda.groups.io/g/nvda) e unha páxina compreta de [grupos locais de linguas](https://github.com/nvaccess/nvda-community/wiki/Connect).
NV Access, os constructores do NVDA, están activos en [Twitter](https://twitter.com/nvaccess) e en [Facebook](https://www.facebook.com/NVAccess).
NV Access tamén ten un [blog In-Process](https://www.nvaccess.org/category/in-process/).

Tamén hai unha [certificación de Experto en NVDA](https://certification.nvaccess.org/) program.
Este é un exame en liña que podes compretar para demostrar as túas habilidades en NVDA.
[NVDA Certified Experts](https://certification.nvaccess.org/) pode enumerar o seu contacto e datos relevantes da empresa.

### Obter axuda {#GettingHelp}

Para obter axuda para o NVDA, preme `NVDA+n` para abrir o menú, despois `a` para axuda.
Dende este submenú podes acesar á Guía do Usuario, a unha referencia rápida de ordes, a un historial de novas características e máis.
Estas primeiras tres opcións ábrense no navegador predeterminado.
Tamén hai material de formación máis compreto dispoñible na [tenda de NV Access](https://www.nvaccess.org/shop).

Recomendamos comezar co "módulo de Formación Básica para NVDA".
Este módulo trata conceptos dende cómo comezar a navegar pola web a usar a navegación de obxectos.
Está dispoñible en:

* [Texto electrónico](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), que inclúe os formatos Word DOCX, páxina Web HTML, eBook ePub e Kindle KFX.
* [Lector humán, audio MP3](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [UEB en papel Braille](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) coa entrega incluída en calquera parte do mundo.

Outros módulos e o desconto  [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/), están dispoñibles na [tenda de NV Access](https://www.nvaccess.org/shop/).

NV Access tamén comercializa  [soporte telefónico](https://www.nvaccess.org/product/nvda-telephone-support/), xa sexa en bloques, xa como parte do [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/).
O soporte telefónico inclúe números locais en Australia e en USA.

O [grupo de usuarios de correo](https://github.com/nvaccess/nvda-community/wiki/Connect) é unha gran fonte de axuda da comunidade, ao igual que [os expertos certificados en NVDA](https://certification.nvaccess.org/).

Podes informar de fallos ou solicitar características a través de [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
As [directrices de colaboración](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) conteñen información valiosa para colaborar coa comunidade.

## Máis Opcións de Configuración {#MoreSetupOptions}
### Opcións de Instalación {#InstallingNVDA}

Se instalas o NVDA directamente dende o lanzador de NVDA descargado, preme o botón Instalar NVDA.
Se xa pechaches este diálogo, ou queres instalar dende unha copia portable, por favor escolle o elemento de menú Instalar NVDA que se atopa baixo Ferramentas no menú NVDA.

O diálogo de instalación que aparece confirmará se queres instalar NVDA, e tamén dirache se esta instalación actualizará unha instalación anterior.
Premendo o botón Continuar comezará a Instalación do NVDA.
Hai tamén algunhas opcións neste diálogo que se explican máis abaixo.
Unha vez se completara a instalación, aparecerá una mensaxe dicíndoche que foi satisfactoria.
Premendo Aceptar neste punto reiniciarase a copia nova instalada do NVDA.

#### Aviso sobre complementos incompatibles {#InstallWithIncompatibleAddons}

Se xa tes complementos instalados tamén pode haber un aviso de que se deshabilitarán os complementos incompatibles.
Antes de poder premer o botón Continuar terás que usar a caixa de verificación para confirmar que entendes que estos complementos serán desactivados.
Tamén haberá presente un botón para revisar os complementos que se deshabilitarán.
Consulta a [seción diálogo complementos incompatibles](#incompatibleAddonsManager) para máis axuda sobre este botón.
Despois da instalación, podes voltar a habilitar os complementos incompatibles baixo a túa propria responsabilidade dende a [Tenda de Complementos](#AddonsManager).

#### Usar o NVDA no Inicio de Sesión {#StartAtWindowsLogon}

Esta opción permíteche escoller se NVDA debería arrancar automáticamente ou non mentres está na pantalla de autentificación de Windows, antes de introducir unha clave.
Esto tamén inclúe o control da conta de usuario e [outras pantallas seguras](#SecureScreens).
Esta opción está habilitada por defecto para instalacións novas.

#### Crear Atallos do Escritorio (ctrl+alt+n) {#CreateDesktopShortcut}

Esta opción permíteche escoller se NVDA debería crear ou non un atallo no escritorio para comezar o NVDA. 
Se se creou, a este atallo tamén se lle asignará unha tecla de atallo control+alt+n permitíndoche arrincar ao NVDA en calquera ocasión con esta combinación de teclas.

#### Copiar Configuración Portable da Actual Conta do Usuario {#CopyPortableConfigurationToCurrentUserAccount}

Esta opción permíteche escoller se NVDA debería copiar ou non a configuración do usuario do actual NVDA en execución na configuración para o usuario actualmente autentificado, para a copia instalada do NVDA. 
Esto non copiará a configuración para calquera outro usuario deste sistema nin para a configuración do sistema para se utilizar durante o inicio de sesión de Windows e [noutras pantallas seguras](#SecureScreens).
Esta opción só está dispoñible cando se instala dende unha copia portable, non cando se instala directamente dende o paquete Lanzador descargado.

### Crear unha Copia Portable {#CreatingAPortableCopy}

Se se crea unha copia portable directamente dende o paquete descargado do NVDA, só preme o botón Crear Copia Portable.
Se xa pechaches este diálogo ou estás a executar unha copia instalada do NVDA, escolle o elemento de menú Crear Copia Portable que se atopa baixo Ferramentas no menú NVDA.

O diálogo que aparece permíteche escoller onde debería crearse a copia portable.
Esto pode ser un directorio no teu disco duro, ou un lugar nun lapis USB ou outro medio portátil.
Tamén hai unha opción para escoller se NVDA debería copiar a sesión de configuración actual do usuario do NVDA para utilizala coa nova copia portable creada.
Esta opción só está dispoñible cando se crea unha copia portable dende unha copia instalada, non cando se crea dende o paquete descargado.
Premendo Continuar crearás a copia portable.
Unha vez a creación estea compretada, aparecerá unha mensaxe dicíndoche que foi exitosa.
Preme Aceptar para pechar este diálogo.

### Restricións das Copias portable e Temporal {#PortableAndTemporaryCopyRestrictions}

Se queres ter unha copia do NVDA contigo nunha memoria USB ou outro medio escrebible, entón deberías escoller o crear unha copia portable.
A copia instalada tamén pode crear unha copia portable de si mesma en calquera intre. 
A copia portable tamén ten a capacidade de instalarse a si mesma en calquera computador nun intre posterior.
Sen embargo, se desexas copiar o NVDA en medios de só lectura coma un CD, só deberías copiar o paqquete descargado.
A execución da versión portable directamente dende un medio de só lectura non se admite neste intre.

O  [instalador do NVDA](#StepsForRunningTheDownloadLauncher) pode usarse coma unha copia temporal do NVDA.
As copias temporais impiden gardar a configuración do NVDA.
Esto inclúe a desactivación do uso da [Tenda de Complementos](#AddonsManager).

As copias portables e temporais do NVDA teñen as seguintes restricións:

* A incapacidade de arrancar automáticamente durante e/ou despois da autentificación.
* A incapacidade de interactuar con aplicacións que se executen con privilexios de administrador, de non ser que, por suposto, o mesmo NVDA se executara tamén con estos privilexios (non recomendado).
* A incapacidade de ler as pantallas do Control de Contas de Usuario (UAC) ao tentar arrancar unha aplicación con privilexios de administrador.
* A incapacidade de admitir a entrada dende una pantalla táctil.
* A incapacidade de proporcionar características coma o modo navegación e a fala de caracteres ao se escreber nas aplicacións da Tenda de Windows.
* A atenuación de audio non está admitida.

## Utilizar o NVDA {#GettingStartedWithNVDA}
### Lanzar o NVDA {#LaunchingNVDA}

Se instalaches o NVDA co instalador, entón iniciar NVDA é tan sinxelo coma ou premer control+alt+n, ou elexir NVDA dende o menú NVDA no Menú Inicio, submenú Programas. 
Adicionalmente podes teclear NVDA no diálogo Executar e premer Intro. 
Se o NVDA xa se está a executar, reiniciarase.
Tamén podes pasar algunhas [opcións de liña de ordes](#CommandLineOptions) que che permiten saír (-q), desactivar complementos (--disable-addons), etc.

Para as copias instaladas, NVDA almacena a configuración no cartafol roaming application data do usuario actual por omisión (ex.: "C:\Users\<user>\AppData\Roaming").
É posible cambiar esto de xeito que o NVDA cargue a súa configuración dende o cartafol local de datos de aplicación no seu lugar.
Consulta a seción acerca de [parámetros do sistema](#SystemWideParameters) para máis detalles.

Para iniciar a versión portátil, vai ao directorio onde descomprimiches ao NVDA, e preme intro ou fai doble clic sobre nvda.exe.
Se o NVDA xa se estaba a executar, deterase automáticamente despois de arrancar a versión portable.

Cando o NVDA arrinca, primeiro escoitarás un grupo ascendente de tons (que che din que NVDA se está a cargar). 
Dependendo como de rápido sexa o teu computador, ou se estás executándo o NVDA dende un lapis USB ou outro medio máis lento, poderá retrasarse un pouco mentres arrinca. 
Se está tardando un tempo extra longo, NVDA debería dicir "Cargando NVDA. Agarda por favor...”

Se non escoitas nada de esto, ou escoitas o son de erro de Windows, ou un grupo descendente de tons, entón esto significa que o NVDA ten un erro, e posiblemente necesitarás informar dun fallo ós desenvolvedores. 
Por favor investiga no sitio web de NVDA para saber como facer esto.

#### Diálogo de Benvida {#WelcomeDialog}

Cando o NVDA arrinque por primeira vez, daráseche a benvida mediante unha caixa de diálogo que che proporciona algunha información básica acerca da tecla modificadora de NVDA e do menú de NVDA. 
(Consulta por favor seccións subseguintes acerca de estos temas). 
A caixa de diálogo tamén contén unha caixa combinada e tres caixas de verificación. 
A caixa combinada permíteche selecionar a distribución de teclado.
A primeira caixa de verificación permíteche controlar se NVDA debería utilizar BloqMayus como unha tecla modificadora do NVDA.
A segunda especifica se NVDA debería arrincar automáticamente despois de autentificarte en Windows e só está dispoñible para copias instaladas do NVDA.
A terceira permíteche controlar se esta caixa de benvida debería aparecer cada vez que o NVDA arranque.

#### Diálogo Estadísticas de Datos de Uso {#UsageStatsDialog}

A partir do NVDA 2018.3, pregúntase ao usuario se quere permitir que os datos de uso se envíen a NV Access para axudar a melloralo no futuro. 
Ao comezar NVDA por primeira vez, aparecerá un diálogo que che preguntará se queres aceptar o envío de datos a NV Access mentres o usas.
Podes ler máis información sobre a recopilación de datos por NV Access na seción Opcións Xerais, [Permitir a NV Access recopilar estadísticas de uso do NVDA](#GeneralSettingsGatherUsageStats).
Nota: ao premer en "si" ou "non" gardarase este axuste e o diálogo non aparecerá nunca máis a menos que reinstales o NVDA.
Sen embargo, podes activar ou desactivar o proceso de recopilación de datos manualmente no panel das opcións xerais do NVDA. Para cambiar esta opción manualmente, podes marcar ou desmarcar a caixa de verificación chamada [Permitir ao proxecto de NVDA recolectar estadísticas de uso do NVDA](#GeneralSettingsGatherUsageStats).

### Acerca de Ordes de teclado de NVDA {#AboutNVDAKeyboardCommands}
#### A Tecla Modificadora NVDA {#TheNVDAModifierKey}

A maioría das ordes específicas de teclado do NVDA consisten normalmente na pulsación da tecla modificadora de NVDA, xunto cunha ou máis teclas. 
Unha notable excepción desto son as ordes de revisión de texto para a distribución de teclado de escritorio que só utiliza as teclas do teclado numérico por si mesmas, pero hai algunhas outras excepcións tamén.. 

NVDA pode configurarse tal que ou a tecla Insert do teclado numérico, ou a Insert do extendido, e/ou a BloqMayus podan utilizarse como a tecla modificadora do NVDA.
De xeito predeterminado tanto o insert do teclado numérico como o do teclado extendido poden utilizarse como teclas modificadoras.

Se desexas facer que unha das teclas modificadoras do NVDA se comporte como normalmente o faría sen estar NVDA en funcionamento (por exemplo desexas activar BloqMayus cando tes configurada BloqMayus para que sexa unha tecla modificadora do NVDA) podes premer a tecla dúas veces en sucesión rápida.

#### Distribucións de Teclado {#KeyboardLayouts}

Actualmente NVDA ven con dous conxuntos de  teclas de ordes coñecidos como distribucións. A distribución sobremesa e a distribución portátil.
De xeito predeterminado, o NVDA está configurado para se usar a disposición de escritorio, aindque podes cambiar á de portátil na categoría Teclado da caixa de diálogo [Opcións do NVDA](#NVDASettings) en Preferencias no menú NVDA.

A disposición escritorio fai un uso amplo do teclado numérico (co bloqueo numérico desactivado).
Aíndaque a maioría dos portátiles non teñen un teclado numérico físico, algúns portátiles poden emular un mantendo pulsada a tecla FN e premendo letras e números na man dereita do teclado (7 8 9 u i o j k l etc).
Se o teu portátil non pode facer esto, ou non che permite desactivar o bloqueo numérico, poderás querer cambiar á distribución Portátil no seu lugar.

### Xestos tactiles do NVDA {#NVDATouchGestures}

Se estás a executar o NVDA nun dispositivo cunha pantalla tactil tamén podes controlar ao NVDA directamente a través de ordes tactiles.
Mentres NVDA estea en execución, ao menos que o soporte de interacción estea deshabilitado, toda a entrada tactil irá directamente ao NVDA. 
Polo tanto, as accións que poidan efectuarse normalmente sen o NVDA non funcionarán.
<!-- KC:beginInclude -->
Para conmutar o soporte da interación táctil, preme NVDA+control+alt+t.
<!-- KC:endInclude -->
Tamén podes habilitar ou deshabilitar o [soporte de interación táctil](#TouchSupportEnable) dende a categoría Interación táctil das opcións do NVDA.

#### Explorar a Pantalla {#ExploringTheScreen}

A maioría das accións básicas que podes realizar ca pantalla tactil son anunciar o control ou o texto en calquera punto na pantalla.
Para facer esto, pon un dedo en calqera lugar sobre da pantalla.
Tamén podes manter o teu dedo sobre da pantalla e movelo arredor para ler outros controis e texto sobre o que vaias movéndoo.

#### Xestos Tactiles {#TouchGestures}

Cando se describan as ordes do NVDA de agora en diante nesta guía do usuario, poderán listar un xesto tactil que se pode utilizar para activar esa orde ca pantalla tactil.
Seguidamente van algunhas instruccións sobre cómo levar a cabo varios xestos tactiles.

##### Toques {#toc45}

Tocar a pantalla brevemente con un ou máis dedos.

Ao tocar unha vez cun dedo conóceselle  como tocar.
Tocar con dous dedos ao mesmo tempo é un toque de 2 dedos, e así sucesivamente.

Se o mesmo toque se realiza unha ou máis veces en sucesión rápida, NVDA veráo en cambio como un xesto especial multi-toque.
Tocar dúas veces resultará en un doble toque.
Tocar tres veces resultará en un tripple toque, e así sucesivamente.
Por suposto estos xestos multi-toque tamén recoñecen cantos dedos foron utilizados, así é posible ter xestos como un 2 dedos con tripla toque, ou un toque con 4 dedos, etc. 

##### Deslizamentos {#toc46}

Deslizar o teu dedo rápidamente pola pantalla.

Hai 4 xestos de deslizamento posibles dependendo da direción: deslizar á esquerda, deslizar á dereita, deslizar arriba e deslizar abaixo.

Ao igual que cos toques, pódese utilizar máis dun dedo para realizar o xesto.
Polo tanto, xestos como deslizar dous dedos arriba ou deslizar 4 dedos á esquerda son todos posibles.

#### Modos Tactiles {#TouchModes}

Ao igual como hai moitas ordes do NVDA tamén hai outros tantos xestos tactiles, NVDA ten varios modos tactiles entre os que podes cambiar, que fan dispoñibles certos subconxuntos de ordes.
Os dous modos que existen polo de agora son modo texto e modo obxecto. 
Certas ordes do NVDA amosadas neste documento poderán ter un modo tactil amosado entre paréntesis despois do xesto tactil.
Por exemplo: deslizar arriba (modo texto) significa que a orde realizarase se deslizas arriba, pero só mentres esteas en modo texto.
Se a orde non ten un modo asociado con ela, funcionará en calquera modo.

<!-- KC:beginInclude -->
Para conmutar entre os dous modos, realiza un toque con 3 dedos.
<!-- KC:endInclude -->

#### Teclado Tactil {#TouchKeyboard}

O teclado tactil úsase para introducir texto e ordes dende unha pantalla tactil.
Cando se enfoque un campo de edición, podes despregar o teclado tactil tocando dúas veces sobre o icono do teclado tactil na parte inferior da pantalla.
Para tablets como a Microsoft Surface Pro, o teclado tactil sempre está dispoñible cando se desbloquea o teclado.
Para pechar o teclado tactil, toca dúas veces o icono do teclado tactil ou sae fora do campo de edición.

Mentres o teclado tactil estea activo, para localizar as teclas no teclado tactil, move o dedo cara o lugar onde se atope o teclado tactil (normalmente na parte inferior da pantalla), e, entón, desprázate polo teclado cun dedo.
Cando atopes a tecla que desexes premer, toca dúas veces a tecla ou levanta o dedo, segundo as opcións escollidas dende [a categoría Opcións de Interación Tactil](#TouchInteraction).

### Modo de Axuda de Entrada {#InputHelpMode}

Moitas ordes de teclado e xestos menciónanse ao longo do resto desta guía do usuario, pero unha maneira sinxela de explorar todas as diferentes ordes é activar a axuda de entrada.

Para activar a axuda de entrada, preme NVDA+1.
Para desactivala, preme NVDA+1 de novo.
Mentres esteas na axuda de entrada, premendo calquera tecla ou realizando calquer xesto tactil anunciarase a acción e describirase que fai (se é que fai algo).
As ordes actuais non se executarán mentres se esté no modo de axuda de entrada.

### O Menú NVDA {#TheNVDAMenu}

O menú NVDA permíteche controlar as opcións do NVDA, aceder á axuda, gardar/voltar á túa configuración, Modificar os diccionarios da fala, ler o ficheiro do rexistro, e saír do NVDA.

Para aceder ao menú NVDA dende calquera parte de Windows mentres o NVDA estea en execución, podes facer calquera das seguintes accións:

* premer `NVDA+n` no teclado.
* Realizar un dobre toque con dous dedos na pantalla tactil.
* Aceder á bandexa do sistema premendo `Windows+b`, `frecha abaixo` ate a icona do NVDA e premer `intro`.
* Alternativamente, acede á bandexa do sistema premendo `Windows+b`, `frecha abaixo` ate a icona do NVDA e abre o menú de contexto premendo a tecla `aplicacións` situada preto á tecla control dereito na maioría dos teclados.
Nun teclado sen unha tecla `aplicacións`, preme `shift+F10` a cambio.
* Fai clic co botón dereito sobre a icona do NVDA situado na bandexa do sistema de Windows

Cando apareza o menú, podes usar as frechas para navegar por el e a tecla `intro` para activalo.

### Ordes Básicas do NVDA {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Nome |Tecla escritorio |Tecla portátil |Tactil |Descripción|
|---|---|---|---|---|
|Arrancar ou reiniciar o NVDA |Control+alt+n |Control+alt+n |non |Arranca ou reinicia o NVDA dende o Escritorio, se este atallo de Windows se habilita durante o proceso de instalación do NVDA. Este é un atallo específico de Windows e polo tanto non se pode reasignar no diálogo Xestos de Entrada.|
|Deter voz |Control |control |toque con 2 dedos |Detén a voz instantáneamente|
|Pausar Voz |Shift |shift |non |Pausa a voz instantáneamente, preméndoa novamente continuará falando onde se detivo (se o pausado se soporta polo sintetizador actual)|
|Menú NVDA |NVDA+n |NVDA+n |doble toque con 2 dedos |desprega o menú NVDA para permitirche acceder ás preferencias, ferramentas, axuda, etc|
|Conmutar Modo Axuda de entrada |NVDA+1 |NVDA+1 |non |Premendo calquera tecla  neste modo anunciarase a tecla, e a descripción de calquer orde de NVDA asociada con ela|
|Saír do NVDA |NVDA+q |NVDA+q |non |Sae do NVDA|
|Deixar pasar seguinte tecla |NVDA+f2 |NVDA+f2 |non |Di ao NVDA que deixe pasar a seguinte tecla premeda directamente á aplicación activa, se está normalmente tratada como unha tecla de ordes de NVDA|
|activar e desactivar modo aplicación durminte |NVDA+shift+s |NVDA+shift+z |non |O modo durminte desactiva todas as ordes de NVDA e a saída de voz/braille para a aplicación actual. Esto é máis útil en aplicacións que proporcionan a súa propria voz ou características de lectura de pantalla. Preme esta orde novamente para desactivar o modo durminte.|

<!-- KC:endInclude -->

### Anunciar Información do Sistema {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Nome |tecla |Descripción|
|---|---|---|
|Anunciar data/hora |NVDA+f12 |Preméndoa  unha vez anuncia a hora actual, preméndoa dúas veces anuncia a data.|
|Anunciar estado da batería |NVDA+shift+b |Anuncia o estado da batería, é dicir se a electricidade se está a utilizar ou a porcentaxe actual da carga.|
|Anunciar o texto no portapapeis |NVDA+c |Anuncia o Texto no portapapeis se hai algún.|

<!-- KC:endInclude -->

### Modos de voz {#SpeechModes}

O modo de voz goberna como se fala o contido da pantalla, notificacións, respostas a ordes e outra saída fálanse durante a operación de NVDA.
O modo predeterminado é "fhalar", o que fala nas situacións que se espera cando se usa un lector de pantalla.
Sen embargo, baixo certas circunstancias, ou ao se executar programas en particular, podes atopar valioso un dos outros modos de fala.

Os catro modos de voz dispoñibles son:

* Falar (predeterminado): NVDA falará normalmente reaccionando aos cambios da pantalla, notificacións e acións coma o movemento do foco ou a emisión de ordes.
* Baixo demanda: o NVDA só falará cando utilices ordes cunha función de anunciado (ex. anunciar o título da xanela); pero non falará reaccionando a acións coma o movemento do foco ou do cursor.
* Desactivado: o NVDA non lerá nada, sen embargo a diferencia do modo silencioso, reaccionará caladamente ás ordes.
* Pitidos: o NVDA remprazará a fala normal con pitidos curtos.

O modo Pitidos pode ser útil cando unha saída moi verbosa se desprace por unha xanela de terminal, pero non che importa o que sexa, só que continúa desprazándose; ou noutras circunstancias nas que o feito de que haxa saída sexa máis importante que a saída en si.

O modo Baixo demanda pode ser valioso cando non necesites información constante sobre o que ocorra na pantalla ou no computador, pero necesitas comprobar periódicamente cousas concretas usando ordes de revisión, etc.
Por exemplo mentres grabas audio, cando utilizas a ampliación de pantalla, durante unha reunión ou unha chamada, ou como alternativa ao modo pitidos.

Un xesto permite percorrer os distintos modos de fala:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Percorrer modos de voz |`NVDA+s` |Percorre os modos de voz.|

<!-- KC:endInclude -->

Se só necesitas cambiar entre un subconxunto limitado de modos de voz, consulta [Modos dispoñibles na orden percorrer modos de voz](#SpeechModesDisabling) para un xeito de deshabilitar modos non desexados.

## Navegar co NVDA {#NavigatingWithNVDA}

NVDA permíteche explorar e navegar o sistema de varios xeitos, incluíndo interacción normal e revisión.

### Obxectos {#Objects}

Cada Aplicación e o proprio sistema operativo constan de moitos obxectos.
Un obxecto é un simple elemento coma un anaco de texto, botón, caixa de verificación, deslizador, lista ou campo de texto editable .

### Navegar co Foco do sistema {#SystemFocus}

O foco do sistema, tamén coñecido simplemente como o foco, é o [obxecto](#Objects) que recibe teclas escrebidas no teclado.
Por exemplo, se estás a escrebir nun campo de texto editable, o campo de texto editable ten o foco.

O modo máis común de navegar por Windows co NVDA, é só moverse cas ordes de teclado normais, como tab. e shift tab. Para moverse adiante e atrás entre controis, premendo Alt. Para despregar a barra de menú e logo utilizando as teclas de cursor para navegar polos menús, utilizando Alt.-tab. Para moverse entre aplicacións en execución. 
Cando fagas esto, NVDA anunciará información sobre o que ten o foco, como o seu nome, tipo, valor, estado, descripción, atallo de teclado e información posicional.
Cando [Resaltado Visual](#VisionFocusHighlight) estea activado, a localización do foco do sistema actual tamén se expón visualmente.

Hai algunhas ordes de teclado útis cando nos movamos co foco:
<!-- KC:beginInclude -->

| Nome |tecla escritorio |tecla portátil |Descripción|
|---|---|---|---|
|Anunciar foco actual |NVDA+tab |NVDA+tab |anuncia o obxecto actual ou control que teña o foco do sistema. Premendo dúas veces deletreará a información|
|Anunciar título |NVDA+t |NVDA+t |Anuncia o título da ventá activa actualmente. Premendo dúas veces deletreará a información. Premendo tres veces copiaráa ao portapapeis|
|Ler a ventá activa |NVDA+b |NVDA+b |le todos os controis na ventá actualmente activa (útil para diálogos)|
|Anunciar Barra de Estado |NVDA+fin |NVDA+shift+fin |Anuncia a barra de estado se NVDA atopa unha. preméndo dúas veces deletreará a información. Premendo tres veces copiaráa ao portapapeis|
|Anunciar tecla de aceso directo |`shift+2 do teclado numérico` |`NVDA+control+shift+.` |Anuncia a tecla de aceso directo (aceleradora) do elemento actualmente enfocado|

<!-- KC:endInclude -->

### Navegar co Cursor do Sistema {#SystemCaret}

Cando un [obxecto](#Objects) que permite navegación e/ou edición de texto se [enfoca](#SystemFocus), podes moverte a traverso do texto utilizando o cursor do sistema, tamén coñecido como o cursor de edición.

Cando o foco estea sobre un obxecto que teña un cursor de edición, podes moverte cas frechas, retroceso de páxina, avance de páxina, comezo, fin, etc., para moverte ao longo do texto. 
Tamén podes cambiar o texto se o control soporta edición.
O NVDA anunciará segundo te movas por carácteres, palabras, liñas, e tamén anunciará a selección e non selección do texto.

O NVDA proporciona as seguintes teclas de ordes en relación ao cursor do sistema:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Ler todo |NVDA+Frecha Abaixo |NVDA+a |Comeza a lectura dende a posición actual do cursor do sistema, movéndoo segundo se despraza|
|Ler liña actual |NVDA+Frecha Arriba |NVDA+l |Le a liña onde estea situado actualmente o cursor do sistema. Premendo dúas veces deletrea a liña. Premendo tres veces deletrea a liña usando descripcións de caracteres.|
|Ler a selección do texto actual |NVDA+Shift+Frecha Arriba |NVDA+shift+s |Le calquera texto seleccionado actualmente|
|Anunciar formato do texto |NVDA+f |NVDA+f |Anuncia o formato do texto onde estea situado actualmente o cursor. Premendo dúas veces amosa a información no modo Exploración|
|Anunciar destiño da ligazón |`NVDA+k` |`NVDA+k` |Premendo unha vez fala o destiño da URL da ligazón no cursor do sistema actual ou na posición do foco. Premendo dúas veces amósao nunha xanela para unha revisión máis doada|
|Anunciar localización do cursor |NVDA+suprimir do teclado numérico |NVDA+suprimir |non |Anuncia información acerca da localización do texto ou do obxecto na posición do cursor do sistema. Por exemplo, esto podería incluir a porcentaxe do documento, a distancia dende a marxe da páxina oo da posición exacta da pantalla. Premer dúas veces pode proporcionar detalles adicionais.|
|frase seguinte |alt+frecha abaixo |alt+frecha abaixo |Move o cursor á frase seguinte e anúnciaa. (só se soporta no Microsoft Word e Outlook)|
|frase anterior |alt+frecha arriba |alt+frecha arriba |Move o cursor á frase anterior e anúnciaa. (só se soporta no Microsoft Word e Outlook)|

Cando esteas nunha táboa, as seguintes teclas de ordes tamén están dispoñibles:

| Nome |Tecla |Descripción|
|---|---|---|
|Moverse á columna anterior |control+alt+Frecha Esquerda |Move o cursor do sistema á columna anterior (permanecendo na mesma fila)|
|Moverse á columna seguinte |control+alt+Frecha Dereita |Move o cursor do sistema á columna seguinte (permanecendo na mesma fila)|
|Moverse á fila anterior |control+alt+Frecha Arriba| Move o cursor do sistema á fila anterior (permanecendo na mesma columna)|
|Moverse á fila seguinte |control+alt+Frecha Abaixo |Move o cursor do sistema á seguinte fila (permanecendo na mesma columna)|
|Moverse á primeira columna |control+alt+inicio |Move o cursor do sistema á primeira columna (permanecendo na mesma fila)|
|Moverse á última columna |control+alt+fin |Move o cursor do sistema á última columna (permanecendo na mesma fila)|
|Moverse á primeira fila |control+alt+rePáx |Move o cursor do sistema á primeira fila (permanecendo na mesma columna)|
|Moverse á última fila |control+alt+avPáx |Move o cursor do sistema á última fila (permanecendo na mesma columna)|
|Ler todo en columna |`NVDA+control+alt+frecha abaixo` |Le a columna verticalmente dende a celda actual cara abaixo ate a última celda na columna.|
|Ler todo en fila |`NVDA+control+alt+frecha dereita` |Le a fila horizontalmente dende a celda actual cara a dereita ate a última celda na fila.|
|Ler toda a columna |`NVDA+control+alt+frecha arriba` |Le a columna actual verticalmente dende a parte superior á inferior sen mover o cursor do sistema.|
|Ler toda a fila |`NVDA+control+alt+frecha esquerda` |Le a fila actual horizontalmente dende a esquerda á dereita sen mover o cursor do sistema.|

<!-- KC:endInclude -->

### Navegación de Obxectos {#ObjectNavigation}

A maior parte do tempo, traballarás con aplicacións utilizando ordes que moven o [foco](#SystemFocus) e o [cursor](#SystemCaret).
Nembargantes, ás veces, poderías querer explorar a aplicación actual ou o Sistema Operativo sen mover o foco ou o cursor.
Tamén poderías querer traballar con [obxectos](#Objects) que non podan accederse normalmente utilizando o teclado.
Nestos casos, podes utilizar a navegación de obxectos.

A Navegación de obxectos permíteche moverte e obter información acerca de [obxectos](#Objects) individuais.
Cando te movas a un obxecto, o NVDA anunciaráo de xeito similar ao anunciado do foco do sistema.
Para unha maneira de revisar todo o texto segundo apareza na pantalla, podes utilizar no seu lugar [revisión de pantalla](#ScreenReview).

Máis que moverse cara atrás e adiante entre cada simple obxecto no sistema, os obxectos agrúpanse xerárquicamente.
Esto significa que debes moverte dentro dalgúns obxectos para acceder ós obxectos que conteñan.
Por exemplo, unha lista contén elementos de lista, así debes moverte dentro da lista para acceder ós seus elementos.
Se te moveches a un elemento de lista, movendo seguinte e anterior levarache a outros elementos de lista na mesma lista.
Movendo a un elemento de lista que conteña obxectos voltarache á lista.
Tamén podes pasar a lista se desexas acceder a outros obxectos.
De igual xeito, nunha barra de ferramentas que conteñña controis, debes moverte dentro da barra de ferramentas para acceder ós controis na mesma.

Se aínda prefires moverte cara adiante e cara atrás entre cada un dos obxectos do sistema, podes usar ordes para moverte ao obxecto anterior e seguinte nunha vista cha.
Por exemplo, se te mueves ao seguinte obxecto nesta vista cha e o actual contén outros obxectos, o NVDA moverase automáticamente ao primeiro obxecto que o conteña.
Alternativamente, se o obxecto actual non contén ningún, o NVDA moverase ao seguinte obxecto no nivel actual da xerarquía.
Se non hai tal obxecto seguinte, o NVDA tentará atopar o seguinte na xerarquía baseándose en obxectos que o conteñan ate que non haxa máis aos que moverse.
As mesmas regras aplícanse para moverse cara atrás na xerarquía.

O obxecto actualmente en revisión chámase navegador de obxectos.
Unha vez que navegues a un obxecto, podes revisar o seu contido utilizando as [ordes de revisión de texto](#ReviewingText) mentres se estea en [modo revisión de obxectos](#ObjectReview).
Cando [Resaltado Visual](#VisionFocusHighlight) estea activado, a localización do foco do sistema actual tamén se expón visualmente.
De xeito predeterminado, o navegador de obxectos móvese xunto co foco  do Sistema, aíndaque este comportamento pode activarse e desactivarse.

Nota: O seguemento do braille ao Navegador de Obxectos pode configurarse a través de [Braille Segue](#BrailleTether).

Para navegar por obxectos, utiliza as seguintes ordes:

<!-- KC:beginInclude -->

| Nome |Tecla Escritorio |Tecla Portátil |Tactil |Descripción|
|---|---|---|---|---|
|Anunciar obxecto actual |NVDA+5 Teclado numérico |NVDA+shift+o |non |Anuncia o navegador de obxectos actual. Premendo dúas veces deletrea a información e premendo tres veces copia este nome e valor do obxecto ao portapapeis.|
|Navegar ao obxecto contedor |NVDA+8 teclado numérico |NVDA+shift+frecha arriba |deslizar arriba (Modo obxecto) |Navega ao contedor do navegador de obxectos actual|
|Moverse ao obxecto anterior |NVDA+4 teclado numérico |NVDA+shift+frecha esquerda |non |Móvese ao obxecto antes do navegador de obxectos actual|
|Moverse ao anterior obxecto en vista cha |NVDA+9 teclado numérico |NVDA+shift+[ |flic á esquerda (modo obxecto) |Móvese ao obxecto anterior nunha vista cha dos obxectos na xerarquía de navegación|
|Moverse ao seguinte obxecto |NVDA+6 teclado numérico |NVDA+shift+frecha dereita |non |Móvese ao obxecto despois do navegador de obxectos actual|
|Moverse ao seguinte obxecto en vista cha |NVDA+3 teclado numérico |NVDA+shift+] |flic á dereita (modo obxecto) |Móvese ao seguinte obxecto nunha vista cha dos obxectos na xerarquía de navegación|
|Navegar ao primeiro obxecto contido |NVDA+2 teclado numérico |NVDA+shift+frecha abaixo |deslizar abaixo (modo obxecto) |Navega ao primeiro obxecto contido polo actual navegador de obxectos|
|Navegar ao obxecto do foco |NVDA+Menos teclado numérico |NVDA+Retroceso |non |Navega ao obxecto que ten actualmente o foco do sistema, e tamén coloca o cursor de revisión na posición do cursor do Sistema, se é amosado|
|Activar actual navegador de obxectos |NVDA+Intro teclado numérico |NVDA+Intro |doble toque |Activa o actual navegador de obxectos (similar a facer clic co rato ou premer espazo cando ten o foco do sistema)|
|Mover foco do Sistema a actual navegador de obxectos |NVDA+shift+Menos teclado numérico |NVDA+shift+retroceso |non |premedo unha vez Move o foco do Sistema ao navegador de obxectos actual, premedo dúas veces move o cursor do sistema á posición do cursor de revisión|
|Anunciar localización do cursor de revisión |NVDA+shift+Suprimir teclado numérico |NVDA+shift+suprimir |non |Anuncia información acerca da localización do texto ou obxecto no cursor de revisión. Por exemplo, esto podería incluir a porcentaxe do documento, a distancia dende o borde da páxina ou a posición exacta na pantalla. ao se premer dúas veces poderá  proporcionar detalles adicionais.|
|Mover cursor de revisión a barra de estado |non |non |no |Anuncia a Barra de Estado se o NVDA atopa unha.  Tamén move o navegador de obxectos a este lugar.|

<!-- KC:endInclude -->

nota: as teclas do teclado numérico requiren que a tecla BloqNum estea desactivada para funcionar apropriadamente.

### Revisar o Texto {#ReviewingText}

NVDA permíteche ler o contido da [pantalla](#ScreenReview), [documento actual](#DocumentReview) ou [obxecto actual](#ObjectReview) por caracteres, palabras ou liñas.
Esto é principalmente útil en lugares (incluindo consolas de ordes de Windows) onde non hai [cursor do sistema](#SystemCaret).
Por exemplo, utilizaríalo para revisar o texto dunha mensaxe longa de información nun diálogo.

Cando se move o cursor de revisión, o cursor do Sistema non o segue, así podes revisar texto sen perder a posición de edición.
Nemmbargantes, de xeito predeterminado, cando o curssor do Sistema se move, o cursor de revisión sígueo.
Esto pode activarse e desactivarse.

Nota: o seguemento do braille ao Navegador de Obxectos pode configurarse a través de [Braille Segue](#BrailleTether).

As seguintes ordes están dispoñibles para revisión de texto: 
<!-- KC:beginInclude -->

| Nome |Tecla Sobremesa |Tecla Portátil |Tactil |Descripción|
|---|---|---|---|---|
|mover á liña superior en revisión |shift+7 teclado numérico |NVDA+control+inicio |non |Move o cursor de revisión á liña superior do texto|
|Mover á liña anterior en revisión |7 teclado numérico |NVDA+frecha arriba |deslizar arriba (modo texto) |Move o cursor de revisión á liña anterior de texto|
|Anunciar liña actual en revisión |8 teclado numérico |NVDA+shift+. |non |Anuncia a liña actual de texto onde estea colocado o cursor de revisión. Premendo dúas veces deletrea a liña, Preméndoa tres veces deletrea a liña utilizando descripcións de carácteres.|
|Mover á liña seguinte en revisión |9 teclado numérico |NVDA+frecha abaixo |deslizar abaixo (modo texto) |Move o cursor de revisión á liña seguinte de texto|
|Mover á liña inferior en revisión |shift+9 teclado numérico |NVDA+control+fin |non |Move o cursor de revisión á liña inferior de texto|
|Mover á palabra anterior en revisión |4 teclado numérico |NVDA+control+frecha esquerda |deslizar con 2 dedos á esquerda |Move o cursor de revisión á palabra anterior no texto|
|Anunciar palabra actual en revisión |5 teclado numérico |NVDA+control+. |non |Anuncia a palabra actual no texto onde estea posicionado o cursor de revisión. Premendo dúas veces deletrea a palabra, preméndoa tres veces deletrea a palabra utilizando descripcións de carácteres.|
|Mover á seguinte palabra en revisión |6 teclado numérico |NVDA+control+frecha dereita |deslizar con 2 dedos á dereitta (modo texto) |Move o cursor de revisión á seguinte palabra no texto|
|mover ao comezo da liña en revisión |shift+1 teclado numérico |NVDA+inicio |non |Move o cursor de revisión ao comezo da liña actual no texto|
|Mover ao carácter anterior en revisión |1 teclado numérico |NVDA+frecha esquerda |deslizar á esquerda (modo texto) |Move o cursor de revisión ao carácter anterior na liña actual no texto|
|Anunciar caracter actual en revisión |2 teclado numérico |NVDA+. |non |Anuncia o carácter actual na liña de texto onde estea posicionado o cursor de revisión. Premendo dúas veces anuncia unha descripción ou exemplo dese carácter.Preméndoa tres veces anuncia o valor numérico do caracter en decimal e hexadecimal.|
|Mover ao seguinte carácter en revisión |3 teclado numérico |NVDA+frecha dereita |deslizar á dereita (modo texto) |Move o cursor de revisión ao seguinte carácter na liña actual de texto|
|Mover ao final da liña en revisión |shift+3 teclado numérico |NVDA+fin |non |Move o cursor de revisión ao final da liña actual de texto|
|Mover á páxina anterior en revisión |`NVDA+rePáx` |`NVDA+shift+rePáx` |non |Move o cursor de revisión á páxina anterior de texto se se admite pola aplicación|
|Mover á páxina seguinte en revisión |`NVDA+avPáx` |`NVDA+shift+avPáx` |non |Move o cursor de revisión á páxina seguinte de texto se se admite pola aplicación|
|Ler todo con revisión |Máis teclado numérico |NVDA+shift+a |deslizar con 3 dedos abaixo (modo texto) |Le dende a posición actual do cursor de revisión, movéndoo segundo baixa|
|Selecionar logo Copiar dende cursor de revisión |NVDA+f9 |NVDA+f9 |none |Comeza a seleción logo procesa a copia dende a posición actual do cursor de revisión. A acción actual non se leva a cabo ata que digas ao NVDA onde está o final do rango de texto|
|Seleccionar logo Copiar a cursor de revisión |NVDA+f10 |NVDA+f10 |none |Na primeira pulsación, o texto seleciónase dende enriba da posición previamente fixada coma a marca de comezo e incluindo a posición actual do cursor de revisión. Logo de premer esta tecla unha segunda vez, o texto copiarase ao portapapeis de Windows|
|Mover a marca de inicio para copiar na revisión |NVDA+shift+f9 |NVDA+shift+f9 |non |Move o cursor de revisión á posición axustada previamente como marca de comezo para copiar|
|Anunciar formato do texto |NVDA+shift+f |NVDA+shift+f |non |Informa do formato do texto onde estea situado actualmente o cursor de revisión. Premendo dúas veces amosa a información en modo exploración|
|Anunciar reemplazo de símbolo actual |Non |Non |non |Fala o símbolo onde estea colocado o cursor de revisión. Premido dúas veces, amosa o símbolo e o texto usado para falalo no modo exploración.|

<!-- KC:endInclude -->

nota: as teclas do teclado numérico requiren que a tecla BloqNum sexa desactivada para funcionar apropriadamente.

Unha boa maneira Para lembrar  as ordes básicas de revisión de texsto cando se utiliza a distribución de escritorio é maxinalas nunha rexiña de tres por tres, indo de superior a inferior ca liña, palabra e caracter e indo de esquerda a dereita   con anterior, actual e seguinte.
A disposición está ilustrada como segue:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Liña anterior |Liña actual |Liña seguinte|
|Palabra anterior |Palabra actual |Palabra seguinte|
|Caracter anterior |Caracter actual |Caracter seguinte|

### Modos de Revisión {#ReviewModes}

As ordes de revisión de texto do NVDA poden revisar o contido dentro do navegador de obxectos actual, documento actual, ou pantalla, dependendo do modo de revisión selecionado.

As ordes que seguen cambian entre os modos de revisión:
<!-- KC:beginInclude -->

| Nome |Tecla Escritorio |Tecla Portátil |Tactil |Descripción|
|---|---|---|---|---|
|Cambiar ao  modo de revisión seguinte |NVDA+7 teclado numérico |NVDA+repáx |deslizar 2 dedos arriba |cambia ao seguinte modo de revisión dispoñible.|
|cambiar ao modo de revisión anterior |NVDA+1 teclado numérico |NVDA+avPáx |deslizar 2 dedos cara abaixo |Cambia ao seguinte modo de revisión dispoñible.|

<!-- KC:endInclude -->

#### Revisión de Obxectos {#ObjectReview}

Mentres se estea en modo revisión de obxectos, só poderás revisar o contido do actual [navegador de obxectos](#ObjectNavigation).
Para obxectos coma campos de edición ou outros controis básicos de documento, Esto será xeralmente o contido de texto.
Para outros obxectos, esto será o nome e ou valor.

#### Revisión de Documentos {#DocumentReview}

Cando o [navegador de obxectos](#ObjectNavigation) estea dentro dun documento en modo navegación (ex.: páxina web) ou outro documento complexo que conteña moitos obxectos (ex.: documentos de Lotus Symphony), é posible cambiar ao modo revisión de documentos.
O modo revisión de documentos permíteche revisar o texto do documento enteiro.

Cando se cambie dende revisión de obxectos á revisión de documentos, o cursor de revisión colócase no documento na posición do navegador de obxectos.
Ao se mover polo documento cas ordes de revisión, o navegador de obxectos actualízase automáticamente ao obxecto que se atopa na posición actual do cursor de revisión.

Ten en conta que o NVDA cambiará á revisión de documentos dende a revisión de obxectos automáticamente cando te movas polos documentos en modo navegación.

#### Revisión de Pantalla {#ScreenReview}

O modo revisión de pantalla permíteche revisar o texto segundo apareza visiblemente na pantalla dentro da aplicación actual.
Esto é semellante á funcionalidade de revisión de pantalla ou cursor do rato en moitos outros lectores de pantalla para Windows.

 Cando se cambia ao modo revisión de pantalla, o cursor de revisión colócase na posición de pantalla do actual [navegador de obxectos](#ObjectNavigation).
 Cando nos movamos pola pantalla cas ordes de revisión, o navegador de obxectos actualízase automáticamente ao obxecto atopado na posición da pantalla do cursor de revisión.

 Ten en conta que nalgunhas aplicacións modernas, NVDA podería non ver algún ou todo o texto dispoñible na pantalla, debido ao uso das recentes tecnoloxías de dibuxo na pantalla que son imposibles de soportar nestos intres.

### Navegar co Rato {#NavigatingWithTheMouse}

Cando moves o rato, NVDA informa de xeito predeterminado do texto que está directamente baixo o punteiro do mesmo, segundo se mova sobre el. 
Onde estea soportado, NVDA lerá o valor dun parágrafo de texto, aíndaque algúns controis só poderán lerse por liñas.

NVDA tamén pode configurarse para anunciar o tipo de control ou obxecto sobre o que estea actualmente o rato segundo se mova (ex.: lista, botón etc). 
Esto poderá ser útil para usuarios cegos totais cando algunhas veces o texto non abonde.

NVDA proporciona un modo para que os usuarios comprendan onde está o rato con respecto ás dimensións da pantalla, facendo soar as coordinadas actuais do rato segundo o audio pite. 
Canto máis alto o rato estea máis arriba na pantalla, o ton será máis alto nos pitidos. 
Canto máis á esquerda ou á dereita estea o rato na pantalla, máis á esquerda ou á dereita parecerá ir o son (asumindo que o usuario teña altavoces estereofónicos).

Estas características extra do rato non están activadas de forma predeterminada no NVDA.
Se desexas tirar partido delas, podes configuralas dende a categoría [Opcións do Rato](#MouseSettings) do diálogo [Opcións do NVDA](#NVDASettings) que se atopa no menú Preferencias do NVDA.

Se ben se poderían usar un rato físico ou un trackpad para navegar co rato, NVDA proporciona algunhas ordes relacionadas con el:
<!-- KC:beginInclude -->

| Nome |Tecla Escritorio |Tecla Portátil |Tactil |Descripción|
|---|---|---|---|---|
|Clic botón esquerdo do rato |Dividir teclado numérico |NVDA+` (acento grave) |non |Fai clic no botón esquerdo do rato unha vez. O típipo doble clic pode realizarse premendo esta tecla dúas veces en sucesión rápida|
|Bloquear botón esquerdo do rato |shift+Dividir teclado numérico |NVDA+control+` (acento grave) |Non |Mantén premedo o botón esquerdo do rato. Prémeo de novo para liberalo. Para arrastrar o rato, preme esta tecla para bloquear o botón esquerdo e entón move o rato físicamente ou usa unha das outras ordes de movemento do rato|
|Clic botón dereito do rato |Multiplicar teclado numérico |NVDA++ (signo máis) |Tap e manter |Fai clic no botón dereito do rato unha vez, principalmente útil para abrir un menú de contexto na posición do rato.|
|Bloquear botón dereito do rato |shift+Multiplicar teclado numérico |NVDA+control++ (signo máis) |Non |Mantén premedo o botón dereito do rato. Preme outra vez para liberalo. Para arrastrar o rato, preme esta tecla  para bloquear o botón dereito e entón move o rato físicamente ou usa unha das outras ordes de movemento do rato|
|Mover rato a navegador de obxectos actual |NVDA+Dividir teclado numérico |NVDA+shift+m |Non |Move o rato á posición do navegador de obxectos actual e cursor de revisión|
|navegar ao obxecto baixo o rato |NVDA+Multiplicar teclado numérico |NVDA+shift+n |Non |Pon o navegador de obxectos no obxecto localizado na posición do rato|

<!-- KC:endInclude -->

## Modo Navegación {#BrowseMode}

Os documentos complexos de só lectura, como páxinas web, son representados no NVDA cun Modo Navegación. 
Esto inclúe documentos nas seguintes aplicacións:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Mmensaxes HTML en Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Libros admitidos en Amazon Kindle for PC

O modo Exploración tamén está dispoñible opcionalmente para documentos de Microsoft Word.

No Modo Navegación, o contido do documento faise dispoñible mediante unha representación chan de contido como unha páxina Web, polo que te podes mover cas teclas de cursor. 
Todas as teclas de ordes do [cursor do sistema](#SystemCaret) do NVDA funcionarán neste modo; ex.: ler todo, anunciar formato, ordes de navegación de táboa, etc.
Cando [Resaltado Visual](#VisionFocusHighlight) estea activado, a localización do foco do sistema actual tamén se expón visualmente.
A información tal como se un texto é unha liga, cabeceira etc anúnciase xunto co texto segundo te movas.

Ás veces, necesitarás interactuar directamente con controis nestos documentos.
Por exemplo, necesitarás facer esto para campos de texto editable e listas así que podes teclear carácteres e utilizar as teclas de cursor para traballar co control.
Fai esto para cambiar a modo foco, onde case todas as teclas se pasan ao control.
Cando se está en modo Navegación, por defecto, NVDA cambiará automáticamente a modo foco se tabulas cara ou fas clic sobre un control en particular que o requira.
En cambio, tabulando ou facendo clic sobre un control que non requira modo foco voltará a modo navegación.
Tamén podes premer intro ou espazo para cambiar a modo foco en controis que o requiran.
Premendo escape voltarás ao modo navegación.
Ademáis, podes forzar manualmente o modo foco, despois permanecerá efectivo ata que escollas desactivalo.

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Conmutar modos Navegación/foco |NVDA+espazo |Conmuta entre modo foco e modo navegación|
|Saír de modo foco |escape |Cambia a modo navegación se o modo foco anteriormente estaba cambiado automáticamente|
|Refrescar documento en modo Navegación |NVDA+f5 |Recarga o contido do documento actual (útil se certos contidos parecen estar desaparecidos da páxina. Non dispoñible en Microsoft Word e Outlook)|
|Procurar |NVDA+control+f |Desprega un diálogo no que podes teclear algún texto a atopar no  documento actual. Consulta [procurar texto](#SearchingForText) para máis información.|
|Procurar seguinte |NVDA+f3 |Atopa a seguinte  ocurrencia do texto no documento que buscaches anteriormente|
|Procurar anterior |NVDA+shift+f3 |Atopa a ocurrencia anterior do texto no documento buscado anteriormente|

<!-- KC:endInclude -->

### Navegación con unha Soa Letra {#SingleLetterNavigation}

Mentres se está en modo revisión, para unha navegación máis rápida NVDA tamén proporciona teclas dun so caracter para saltar cara certos campos no documento.
Ten en conta que non todas estas ordes se soportan en cada tipo de documento.

<!-- KC:beginInclude -->
A seguintes teclas elas soas saltan ao seguinte campo, ca tecla shift saltan ao anterior campo.

* h: Cabeceira
* l: lista
* i: elemento de lista
* t: táboa
* k: liga
* n: texto que non é liga
* f: campo de formulario
* u: liga non visitada
* v: liga visitada
* e: campo de edición
* b: botón
* x: caixa de verificación
* c: caixa combinada
* r: botón de opción
* q: cita
* s: separador
* m: marco
* g: gráfico
* d: rexión
* o: obxecto empotrado (reproductor de audio e vídeo, aplicación, diálogo, etc.)
* 1 a 6: cabeceiras da 1 á 6 respectivamente
* a: anotación (comentario, revisión do editor, etc.)
* ``p``: parágrafo de texto
* w: erro de ortografía

Para te mover cara o comezo ou o remate de elementos contedores como listas e táboas:

| Nome |Tecla |Descripción|
|---|---|---|
|Mover ao comezo dun contedor |shift+coma |Móvese ao comezo do contedor (lista, táboa etc) onde estea situado o cursor|
|Mover ao final do contedor |coma |Móvese ao final do contedor (lista, táboa etc) onde estea situado o cursor|

<!-- KC:endInclude -->

Algunhas aplicacións web coma Gmail, Twitter e Facebook usan letras soas como atallos de teclado.
Se queres utilizar éstas aínda poderás usar as teclas de cursor para ler en modo exploración, podes desactivar temporalmente  as teclas de navegación cunha soa letra do NVDA.
<!-- KC:beginInclude -->
Para activar ou desactivar a navegación cunha soa letra para o documento actual, preme NVDA+shift+espazo.
<!-- KC:endInclude -->

#### Orde de navegación de parágrafos de texto {#TextNavigationCommand}

Podes saltar ao seguinte ou ao anterior parágrafo de texto premendo `p` ou `shift+p`.
Os parágrafos de texto defínense por un grupo de texto que semella estar escrebido con frases compretas.
Esto pode seren útil para atopar o comezo de contido lexible en varias páxinas web, como:

* Sitios web de novas
* Foros
* Publicacións de Blog

Estas ordes tamén poden seren útiles para saltarse certos tipos de desórdenes, como:

* Anuncios
* Menús
* Cabeceiras

Ten en conta, sen embargo, que mentres o NVDA fai todo o posible por identificar os parágrafos de texto, o algoritmo non é perfecto e ás veces pode cometer erros.
Ademáis, esta orde é diferente das ordes de navegación por parágrafos `control+frecha abaixo ou frecha arriba`.
A navegación de parágrafos de texto só salta entre parágrafos de texto, mentres que as ordes de navegación por parágrafos levan o cursor aos parágrafos anterior e posterior independentemente de se conteñen texto ou non.

#### Outras ordes de navegación {#OtherNavigationCommands}

Ademáis das ordes enumeradas enriba, o NVDA ten ordes que non teñen teclas predeterminadas asignadas.
Para usar estas ordes, primeiro necesitas asignarlles xestos usando o [diálogo Xestos de Entrada](#InputGestures).
Aquí tes unha listaxe das ordes dispoñibles

* Artigo
* Figura
* Grupo
* Pestana
* Elemento de menú
* Botón conmutable
* Barra de progreso
* Fórmula matemática
* Parágrafo aliñado verticalmente
* Mesmo estilo de texto
* Diferente estilo de texto

Ten en conta que hai dúas ordes para cada tipo de elemento, para avanzar e para retroceder no documento, e debes asignar xestos para ambas ordes para poder navegar rápidamente en ambas direcións.
Por exemplo, se queres usar as teclas `y` / `shift+y` para navegar rápidamente polas pestanas, farías o seguinte

1. Abre o diálogo Xestos de entrada dende o modo exploración.
1. Procura o elemento "move á seguinte pestana" na seción modo Exploración.
1. Asigna a tecla `y` para o xesto atopado.
1. Procura o elemento "move á pestana anterior".
1. Asigna `shift+y` para o xesto atopado.

### A Listaxe de Elementos {#ElementsList}

A listaxe de elementos proporciona acceso a unha listaxe de varios tipos de elementos no documento segundo sexa apropriado para a aplicación.
Por exemplo, nos navegadores web, a listaxe de elementos pode listar ligas, cabeceiras, campos de formulario, botóns ou rexións.
Os botóns de opción permítenche cambiar entre os diferentes tipos de elementos.
Proporciónase tamén un campo de edición no diálogo o que che permite filtrar a lista para axudarche a buscar un elemento en particular na páxina. 
Unha vez escollas un elemento, podes utilizar os botóns proporcionados no diálogo para moverte cara, ou activar, ese elemento.
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Lista de elementos do Modo Navegación |NVDA+f7 |Lista  varios tipos de elementos no documento actual|

<!-- KC:endInclude -->

### Procurar texto {#SearchingForText}

Este diálogo permíteche buscar termos no documento actual.
No campo "Teclear o texto que desexes atopar", pode introducirse o texto a procurar.
A caixa de verificación "Sensible ás maiúsculas" fai que a busca considere letras en maiúsculas e en minúsculas de xeito diferente.
Por exemplo, con "Sensible ás maiúsculas" selecionada podes atopar "NV Access" pero non "nv access".
Usa as seguintes teclas para realizar buscas:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Procurar texto |NVDA+control+f |Abre o diálogo procurar|
|Procurar seguinte |NVDA+f3 |Busca a seguinte ocurrencia do termo buscado actual|
|Procurar anterior |NVDA+shift+f3 |Busca a ocurrencia anterior do termo buscado actual|

<!-- KC:endInclude -->

### Obxectos Empotrados {#ImbeddedObjects}

As páxinas poden incluir contido enriquecido utilizando tecnoloxías como Oracle Java e HTML5, así coma aplicacións e diálogos.
onde estas se atopen nun modo virtual, NVDA anunciará "obxecto integrado", "aplicación" ou "diálogo", respectivamente.
Podes moverte rápidamente cara eles usando as teclas de navegación dunha soa tecla de obxectos integrados o e shift+o.
Para interactuar con estos obxectos, podes premer intro sobre eles.
Se é acesible, entón podes tabular por eles e interactuar como con calquera outra aplicación. 
Proporciónase unha orde de teclado para voltar á páxina.
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Mover ao contido do modo Navegación |NVDA+control+espazo |Move o foco fora do actual obxecto empotrado e pono dentro do documento que o contén|

<!-- KC:endInclude -->

### Modo de Seleción Nativa {#NativeSelectionMode}

Por defecto ao selecionar texto con `shift+frechas` en modo exploración, só se fai unha seleción dentro da representación do modo exploración do  NVDA do documento, e non dentro da aplicación mesma.
Esto significa que a seleción non é visible na pantalla, e copiar texto con `control+c` só copiará a representación cha de texto do NVDA do contido. É dicir, o formato das táboas, ou se algo é unha ligazón non se copiará.
Sen embargo, o NVDA ten un modo seleción nativa que pode activarse en documentos en modo exploración en particular (ate o de agora só en Mozilla Firefox) que provocan que a seleción nativa do documento  sega á seleción do modo exploración de NVDA.

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Activar e Desactivar o modo Seleción Nativa |`NVDA+shift+f10` |Activa ou desactiva o modo seleción nativa|

<!-- KC:endInclude -->

Cando se activa o modo seleción nativa, copiar a seleción con `control+c` tamén usará a funcionalidade propria da aplicación, o que significa que o contido enriquecido copiarase ao portapapeis, en lugar de texto cha.
Esto significa que ao pegar este contido nun programa como Microsoft Word ou Excel, o formato como táboas, ou se algo é unha ligazón incluirase.
Ten en conta, sen embargo, que no modo seleción nativa, non se incluirán algunhas etiquetas  accesibles ou outra información que o NVDA xenera en modo exploración.
Tamén, aíndaque a aplicación fará todo o posible para facer coincidir a seleción nativa coa seleción do modo exploración de NVDA, pode que non sempre sexa de todo precisa.
Sen embargo, para situacións nas que desexes copiar unha táboa enteira ou un parágrafo de contido enriquecido, esta función debería resultar útil.

## Ler Contido Matemático {#ReadingMath}

O NVDA pode ler e navegar polo contido matemático na web e noutras aplicacións, proporcionando acceso en braille e voz. 
Non obstante, para que o NVDA lea e interactúe co contido matemático, primeiro necesitarás instalar un componente de matemáticas para o NVDA.
Hai varios complementos de NVDA dispoñibles na Tenda de Complementos de NVDA que proporcionan soporte para matemáticas, incluindo o [complemento de NVDA MathCAT](https://nsoiffer.github.io/MathCAT/) e [Access8Math](https://github.com/tsengwoody/Access8Math). 
Por favor consulta a [seción Tenda de Complementos](#AddonsManager) para deprender como explorar e instalar complementos dispoñibles no NVDA.
NVDA tamén pode facer uso do vello software [MathPlayer](https://info.wiris.com/mathplayer-info) de Wiris se se atopa no teu sistema, aíndaque este software xa non se mantén.

### Contido de matemáticas soportado {#SupportedMathContent}

Cun compoñente de matemáticas adecuado instalado, o NVDA admite os seguintes tipos de  contido matemático:

* MathML en Mozilla Firefox, Microsoft Internet Explorer e Google Chrome.
* Microsoft Word 365 Modern Math Equations a través de UI automation:
O NVDA é capaz de ler e interactuar con ecuacións matemáticas en Microsoft Word 365/2016 compilación 14326 e superiores.
Ten en conta, polo tanto, que calquera ecuación previa MathType creada debe primeiro converterse a Office Math.
Esto faise selecionando cada unha e escollendo Opcións de Ecuación -> Convertir a Office Math no menú de contexto.
Asegúrate de que a túa versión de MathType sexa a última antes de facer esto.
Microsoft Word tamén proporciona agora unha navegación baseada en símbolos en liña polas proprias ecuacións e admite a introdución de matemáticas usando varias sintaxis, incluida LateX.
Para máis detalles, por favor consulta [Ecuacións con formato liñal usando UnicodeMath e LaTeX en Word](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint e versións vellas de Microsoft Word: 
O NVDA pode ler e navegar ecuacións MathType tanto en Microsoft Powerpoint coma en Microsoft word.
MathType necesita estaren instalado para que esto funcione.
A versión trial é suficiente.
Pode descargarse dende  a [Páxina de presentación de MathType](https://www.wiris.com/en/mathtype/).
* Adobe Reader.
Ten en conta que esto non é un estándar official aínda, así que non hai actualmente software dispoñible para o público que poda producir este contido.
* Kindle Reader para PC:
O NVDA pode ler e navegar matemáticas en Kindle para PC para libros con matemáticas acesibles.

Ao ler un documento, NVDA falará calquera contido matemático soportado onde apareza.
Se estás a utilizar unha pantalla braille, tamén se amosará en braille.

### Navegación Interactiva {#InteractiveNavigation}

Se estás traballando principalmente con voz, na maioría dos casos, probablemente desexarás examinar a expresión en segmentos máis pequenos, en lugar de escoitar a expresión enteira dunha vez.

Se estás en modo exploración, podes facer esto movendo o cursor ao contido matemático e ppremendo intro.

Se non estás en modo exploración:

1. move o cursor de revisión ao contido matemático.
Por omisión, o cursor de revisión segue ao cursor do sistema, así podes utilizar normalmente o cursor do sistema para moverte ao contido decidido.
1. Logo, activa a seguinte orde:

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Interactuar co contido matemático |NVDA+alt+m |Comeza a interactuación co contido matemático.|

<!-- KC:endInclude -->

Neste punto, o NVDA entrará en modo matemáticas, onde podes usar ordes como as frechas para explorar a expressión.
Por exemplo, podes moverte a través da expresión cas teclas de frecha  esquerda ou dereita e achegarte a unha porción da expresión como unha fracción utilizando a tecla de frecha abaixo.

Cando desexes voltar ao documento, simplemente preme a tecla escape.

Para máis información sobre as ordes dispoñibles e preferencias para ler e navegar dentro do contido matemático, por favor consulta a documentación para o teu compoñente de matemáticas particular que teñas instalado.

* [Documentación de MathCAT](https://nsoiffer.github.io/MathCAT/users.html)
* [Documentación de Access8Math](https://github.com/tsengwoody/Access8Math)
* [Documentación de MathPlayer](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Ás veces o contido matemático podería  amosarse coma un botón ou outro tipo de elemento que, ao se activar, pode amosar un diálogo ou máis información relacionada coa fórmula.
Para activar o botón ou o elemento que contén a fórmula, preme ctrl+intro.

### Instalar MathPlayer {#InstallingMathPlayer}

Aíndaque xeralmente recoméndase usar un dos novos complementos de NVDA para soportar matemáticas en NVDA, en certas ocasións limitadas MathPlayer pode ser unha opción máis adecuada.
Ex.: MathPlayer pode admitir unha lingua ou un código braille en particular que non estea soportado nos complementos máis novos.
MathPlayer está dispoñible gratuitamente no sitio web de Wiris.
[Descargar MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
Despois de instalar MathPlayer, necesitarás reiniciar o NVDA. 
Ten en conta que a información sobre MathPlayer pode indicar que é só para navegadores antigos coma o Internet Explorer 8.
Esto só se refire ao uso de MathPlayer para amosar contido matemático visualmente e pode ignorarse por aqueles  que o usen para ler ou navegar por matemáticas con NVDA.

## Braille {#Braille}

Se tes unha pantalla braille, NVDA pode amosar información en braille.
Se a túa pantalla braille ten un teclado tipo Perkins, tamén podes introducir braille contraído ou sen contraer.
O Braille tamén pode amosarse en pantalla usando o [Visualizador de Braille](#BrailleViewer) no seu lugar, ou ao mesmo tempo, usando unha pantalla braille física.

Por favor consulta a seción [Pantallas Braille soportadas](#SupportedBrailleDisplays) para información  acerca das pantallas braille soportadas.
Esta seción tamén contén información sobre que pantallas son compatibles coa función de detección automática de pantallas braille do NVDA.
Podes configurar o braille usando a [categoría Opcións de Braille](#BrailleSettings) do diálogo [Opcións do NVDA](#NVDASettings).

### Abreviaturas de tipos de Control, estado e rexións {#BrailleAbbreviations}

Co fin de ter a maior cantidade de información posible nunha pantalla braille, definíronse as seguintes abreviaturas para indicar o tipo de control e o estado así como as rexións.

| Abreviatura |Tipo de Control|
|---|---|
|apl |aplicación|
|art |artigo|
|cit |cita|
|bt |botón|
|btdsp |botón despregable|
|btrot |botón rotatorio|
|btdiv |botón divisor|
|btcom |botón conmutable|
|tlo |título|
|cc |caixa combinada|
|cv |caixa de verificación|
|dlg |diálogo|
|doc |documento|
|ce |campo de texto editable|
|pwdedt |edición de contrasinal|
|integrado |obxecto integrado|
|notaf |nota final|
|fig |figura|
|notap |nota ao pe|
|gra |gráfico|
|grp |grupo|
|enN |cabeceira de nivel n, ex.: h1, h2.|
|axd |grobo de axuda|
|rex |rexión|
|lig |liga|
|ligv |liga visitada|
|lst |listaxe|
|mn |menú|
|bmn |barra de menú|
|btmn |botón de menú|
|elmn |elemento de menú|
|pnl |panel|
|barprg |barra de progreso|
|bsyind |indicador de ocupado|
|bto |botón de opción|
|bardsp |barra de desprazamento|
|sec |seción|
|barst |barra de estado|
|ctrtab |control tab|
|tb |táboa|
|cN |número de columna de táboa n, ex.: c1, c2.|
|fN |número de fila de táboa n, ex.: r1, r2.|
|term |terminal|
|barfer |barra de ferramentas|
|cons |consellos|
|vár |vista en árbore|
|btvár |botón de vista en árbore|
|elvár |elemento de vista en árbore|
|nv N |un elemento de vista en árbore que ten un nivel xerárquico N||
|vt |ventá|
|~~-~~ |separador|
|cmr |contido marcado|

Os seguintes indicadores de estado  tamén están definidos:

| Abreviatura |Estado de Control|
|---|---|
|... |amosado cando un obxecto soporta autocompretado|
|⢎⣿⡱ |amosado cando un opbxecto  (ex. un botón conmutable) está premedo|
|⢎⣀⡱ |amosado cando un obxecto (ex. un botón conmutable) non está premedo|
|⣏⣿⣹ |amosado cando un obxecto (ex. unha caixa de verificación) está marcado|
|⣏⣸⣹ |amosado cando un obxecto (ex. unha caixa de verificación) está parcialmente marcado|
|⣏⣀⣹ |amosado cando un obxecto (ex. unha caixa de verificación) non está marcado|
|- |amosado cando un obxecto (ex.: un elemento de vista en árbore) é contraíble|
|+ |amosado cando un obxecto (ex.: un elemento de vista de árbore) é Expandible|
|*** |amosado cando se atopa un control ou un documento protexido|
|clk |amosado cando un obxecto é clicable|
|cmnt |Amosado cando hai un comentario para unha celda nunha folla de cálculo ou nunha peza de texto nun documento|
|frml |amosado cando hai unah fórmula nunha celda dunha folla de cálculo|
|invalid |amosado cando se fixo unha entrada inválida|
|ldesc |amosado cando un obxecto (normalmente un gráfico) ten unha descripción longa|
|mln |amosado cando un campo de edición permite escrebir varias liñas de texto coma campos de comentarios en sitios web|
|req |amosado cando se atopa un campo de edición obrigatorio|
|ro |amosado cando un obxecto (ex.: un campo de texto editable) é de só lectura|
|sel |amosado cando un obxecto está selecionado|
|nsel |amosado cando un obxecto non está selecionado|
|ordeado asc |amosado cando un obxecto se ordea ascendentemente|
|ordeado desc |amosado cando un obxecto se ordea descendentemente|
|submnu |amosado cando un obxecto ten un despregable (normalmente un submenú)|

Finalmente, definíronse as seguintes abreviaturas para rexións:

| Abreviatura |Rexión|
|---|---|
|tlo |título|
|cinf |info de contido|
|cmpl |complementario|
|form |formulario|
|main |principal|
|nav |navegación|
|busq |procura|
|rxn |rexión|

### Entrada Braille {#BrailleInput}

NVDA soporta a entrada de braille  contraído e sen contraer a través dun teclado braille.
Podes selecionar a táboa de transcripción usada para transcribir braille no texto usando a opción [Táboa de entrada](#BrailleSettingsInputTable) na categoría de braille no diálogo [Opcións do NVDA](#NVDASettings).

Cando se estea usando braille sen contraer, o texto insértase tan pronto como se introduce.
Cando se estea usando braille contraído, o texto insértase ao premer espazo ou intro ao final dunha palabra.
Ten en conta que a transcripción pode reflectir só a palabra braille que esteas a escrebir e non se pode considerar o texto existente.
Por exempro, se estás usando un código braille que comeza os números cun signo de número e premes retroceso para moverte ao remate dun número, necesitarás teclear o signo de número de novo para introducir números adicionais.

<!-- KC:beginInclude -->
Ao premer o punto 7 borras a última celda ou carácter introducido.
O punto 8 transcribe calquera entrada braille e preme a tecla intro.
Premendo os puntos 7 + 8 transcribe calquera entrada braille, pero sen engadir un espazo ou premendo intro.
<!-- KC:endInclude -->

#### Introducir atallos de teclado {#BrailleKeyboardShortcuts}

O NVDA admite a introdución de atallos de teclado e a emulación do premedo de teclas mediante a pantalla braille.
Esta emulación preséntase en dous xeitos: asignando unha entrada braille directamente a algunha pulsación de tecla e usando as teclas modificadoras virtuais.

As teclas de uso común, como as teclas de cursor ou a pulsación de Alt para acesar aos menús, poden asignarse directamente á entrada braille.
O controlador para cada pantalla braille ven preequipado con algunhas destas asignacións.
Podes cambiar estas asignacións ou engadir algunhas teclas novas emuladas dende o [diálogo Xestos de Entrada](#InputGestures).

Aíndaque este enfoque é útil para as teclas que se premen con frecuencia ou as únicas (como Tab), é posible que non desexes asignar un conxunto único de teclas a cada atallo de teclado.
Para permitir a emulación das pulsacións das teclas modificadoras , o NVDA proporciona ordes para conmutar as teclas control, alt, shift, windows e NVDA, xunto con ordes para algunhas combinacións desas teclas.
Para usar esos conmutadores, primeiro preme a orde (ou secuencia de ordes) das teclas modificadoras que se desexe premer.
Logo introduce o carácter que forma parte do atallo de teclado que se desexe introducir.
Por exemplo, para producir control+f, usa a orde "conmutador tecla control" e entón teclea unha f,
e para introducir control+alt+t, usa ou as ordes "conmutar tecla control" e "conmutar tecla alt", en calquera orde, ou a orde "Conmutar teclas control e alt", seguido de escreber unha t.

Se conmutas accidentalmente as teclas modificadoras, executando a orde conmutar outra vez eliminarás a modificadora.

Cando se escreba en braille contraído, o uso das teclas modificadoras conmutables causará que a túa entrada sexa transcrita só se huberas pulsaras os puntos 7+8.
Ademáis, a pulsación de teclas emulada non pode reflectir o braille escrebido antes da tecla modificadora.
Esto significa que, para teclear alt+2 cun código braille que utilice un signo de número, primeiro debes conmutar Alt e despois teclear un signo de número.

## Visión {#Vision}

Mentres que o NVDA está dirixido principalmente a persoas cegas ou con problemas de visión que usen principalmente a voz e/ou o braille para manexar un computador, tamén ofrece funcións incorporadas para cambiar o contido da pantalla.
Dentro do NVDA, esta axuda visual noméase proveedor de mellora de visión.

O NVDA ofrece varios provedores de mellora de visión incorporados que se describen  a siña.
Pódense proporcionar provedores adicionais de mellora de visión en [complementos de NVDA](#AddonsManager).

As opcións de visión do NVDA poden cambiarse na [categoría visión](#VisionSettings) do diálogo [Opcións do NVDA](#NVDASettings).

### Resaltado Visual {#VisionFocusHighlight}

O resaltado visual pode axudar a identificar as posicións do [foco do sistema](#SystemFocus), [do navegador de obxectos](#ObjectNavigation) e [do modo Exploración](#BrowseMode).
Estas posicións resáltanse cun rectángulo de cor.

* O azul sólido resalta unha combinación da localización do navegador de obxectos e do foco do sistema (ex.: porque [o navegador de obxectos sega ao foco do sistema](#ReviewCursorFollowFocus)).
* O azul discontínuo resalta só o obxecto do foco do sistema.
* O rosa sólido resalta só o navegador de obxectos.
* O amarelo sólido resalta o cursor virtual usado en modo Exploración (onde non hai cursor físico coma nos navegadores web).

Cando Resaltado Visual estea activado na [categoría visión](#VisionSettings) do diálogo [Opcións de NVDA](#NVDASettings), [podes cambiar se desexas ou non resaltar o cursor do foco, do navegador de obxectos ou do modo Exploración](#VisionSettingsFocusHighlight)

### Cortina de Pantalla {#VisionScreenCurtain}

Como usuario cego ou con problemas de visión, a menudo non é posible ou necesario ver o contido da pantalla.
Ademáis, pode seren difícil asegurarte de que non haxa ninguén mirando por enriba do teu hombro.
Para esta situación, o NVDA contén unha característica chamada "Cortina de Pantalla" que pode activarse para facer que a pantalla sexa negra.

Podes activar a Cortina de Pantalla na [categoría visión](#VisionSettings) do diálogo [Opcións do NVDA](#NVDASettings).

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Conmutar estado da cortina de pantalla |`NVDA+control+escape` |Habilita facer que a pantalla se poña negra ou deshabilita o amosado dos contidos da pantalla. Premedo unha vez, habilítase a cortina de pantalla ate que reinicies o NVDA. Premedo dúas veces, a cortina de pantalla habilítase ate que ti a deshabilites.|

<!-- KC:endInclude -->

Cando a Cortina de Pantalla estea activa algunhas tarefas baseadas directamente no que aparece sobre a pantalla como a realización do [OCR](#Win10Ocr) ou a toma dunha captura non se poden lograr.

Debido a un cambio na API Windows Magnification, a Cortina de Pantalla tivo que actualizarse para admitir as versións máis novas de Windows.
Usa o NVDA 2021.2 para activar a Cortina de Pantalla con Windows 10 21H2 (10.0.19044) ou posteriores.
Por razóns de seguridade, ao usar unha versión nova de Windows, obtén unha confirmación visual de que a Cortina de Pantalla faga a esta totalmente negra.

Por favor ten en conta que mentres o magnificador de Windows estea en execución e se estean a usar as cores invertidas da pantalla,  a cortina de pantalla non pode habilitarse.

## Recoñecemento de Contidos {#ContentRecognition}

Cando os autores non proporcionan suficiente información para que un usuario de lector de pantalla determine o contido de algo, poden usarse varias ferramentas para tentar recoñecer o contido dende unha imaxe.
O NVDA soporta a funcionalidade de recoñecemento óptico de caracteres (OCR) integrada en Windows 10 e posteriores para recoñecer texto dende imaxes.
Poden proporcionarse recoñecedores de contido adicionais en complementos do NVDA.

Cando uses unha orde de recoñecemento de contido, o NVDA recoñece contido dende o [navegador de obxectos](#ObjectNavigation) actual.
Por omisión, o navegador de obxectos segue ao foco do sistema ou ao cursor do modo exploración, así podes mover normalmente o foco ou o cursor do modo exploración onde desexes.
Por exemprlo, se moves  o cursor do modo exploración a un gráfico, o recoñecemento recoñecerá o contido dende o gráfico por omisión.
Polo tanto, poderás desexar usar a navegación de obxectos directamente para, por exemplo, recoñecer o contido de toda unha ventá de aplicación.

Unha vez o recoñecemento se complete, o resultado presentarase nun documento semellante ao modo exploración, permitíndote ler a información coas teclas do cursor, etc.
Premendo intro ou espazo activará (normalmente un clic) o texto no cursor se é posible.
Premendo escape descartas o resultado do recoñecemento.

### OCR de Windows {#Win10Ocr}

Windows 10 e posteriores inclúen un OCR para moitas linguas.
O NVDA pode usar esto para recoñecer texto dende imaxes ou aplicacións inaccesibles.

Podes configurar a lingua a usar para o recoñecemento de texto na [categoría OCR de Windows](#Win10OcrSettings)do diálogo [Opcións do NVDA](#NVDASettings).
Poden instalarse linguas adicionais abrindo o menú Inicio, escollendo Configuración, selecionando Hora e lingua -> Rexión e lingua e logo escollendo Engadir unha Lingua.

Cando queras monitorizar contido que cambie constantemente, coma cando ves un vídeo con subtítulos, opcionalmente podes habilitar o refrescado automático do contido recoñecido.
Esto pode facerse tamén na [categoría OCR de Windows](#Win10OcrSettings) do diálogo [Opcións de NVDA](#NVDASettings).

O OCR de Windows pode ser total ou parcialmente incompatible coas [Melloras visuais de NVDA](#Vision) ou outras axudas visuais externas. Terás que deshabilitar estas axudas antes de proceder cun recoñecemento.

<!-- KC:beginInclude -->
Para recoñecer o texto no actual navegador de obxectos usando o OCR do Windows, preme NVDA+r.
<!-- KC:endInclude -->

## Características Específicas para Aplicación {#ApplicationSpecificFeatures}

NVDA proporciona as súas proprias características extra para algunhas aplicacións para facer máis sinxelas certas tarefas ou para proporcionar acceso a funcionalidade que de outra maneira non está accesible para os usuarios do lector de pantalla.

### Microsoft Word {#MicrosoftWord}
#### Lectura Automática de Cabeceiras de Columna e Fila {#WordAutomaticColumnAndRowHeaderReading}

NVDA poderá anunciar automáticamente  a cabeceira apropriada de fila e columna ao navegar a través de táboas no Microsoft Word.
Esto require que a opción Anunciar  Cabeceiras de Filas e columnas nas opcións de NVDA Formateado de Documentos, que se atopa no diálogo [Opcións do NVDA](#NVDASettings), estea activada.

Se usas [UIA para aceder a documentos de Word](#MSWordUIA), o que é o predeterminado nas versións recentes de Word e Windows, as celdas da primeira fila consideraranse automáticamente como cabeceiras de columna; de modo similar, as celdas da primeira columna consideraranse automáticamente como cabeceiras da fila.

Pola contra, se non usas [UIA para aceder a documentos de Word](#MSWordUIA), terás que indicar ao NVDA que fila ou columna contén as cabeceiras en calquera táboa dada.
Despois de moverse á primeira celda na columna ou fila que conteña as cabeceiras, utiliza unha das ordes seguintes:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Fixar cabeceiras de columna |NVDA+shift+c |Premendo esto unha vez dis ao NVDA que esta é a primeira celda de cabeceira na fila que contén cabeceira de columna, que debería seren anunciada automáticamente ao se mover entre columnas por enbaixo desta fila. Premendo dúas veces eliminarás a opción.|
|Fixar cabeceiras de fila |NVDA+shift+r |Premendo esto unha vez dis ao NVDA que esta é a primeira celda de cabeceira na columna que contén cabeceiras de fila, a que debería anunciarse automáticamente ao se mover entre filas despois desta columna. Premendo dúas veces eliminarás a opción.|

<!-- KC:endInclude -->
Estas opcións gardaranse no documento como marcadores, compatibles con outros lectores de pantalla coma Jaws.
Esto significa que outros usuarios de lectores de pantalla que abran este documento máis tarde terán automáticamente as cabeceiras de fila e columna xa postas. 

#### Modo Exploración en Microsoft Word {#BrowseModeInMicrosoftWord}

De xeito similar á web, o modo exploración pode usarse en Microsoft Word para permitirche utilizar características coma navegación rápida e a Lista de Elementos.
<!-- KC:beginInclude -->
Para activar ou desactivar o modo Exploración en Microsoft Word, preme NVDA+espazo.
<!-- KC:endInclude -->
Para información adicional acerca do modo Exploración e a Navegación Rápida, consulta a [sección Modo Exploración](#BrowseMode).

##### A Lista de Elementos {#WordElementsList}

<!-- KC:beginInclude -->
Mentres se estea no modo Exploración en Microsoft Word, podes acceder á Lista de Elementos premendo NVDA+f7.
<!-- KC:endInclude -->
A Lista de Elementos pode listar cabeceiras, ligas, anotacións (as que inclúen comentarios e seguemento de cambios) e erros (actualmente limitados a erros de ortografía).

#### Anunciado de Comentarios {#WordReportingComments}

<!-- KC:beginInclude -->
Para anunciar calquera comentario na posición actual do cursor de edición, preme NVDA+alt+c.
<!-- KC:endInclude -->
Todos os comentarios para o documento con outro seguemento de cambios tamén poden listarse na Lista de Elementos do NVDA ao seleccionar Anotacións segundo se teclea.

### Microsoft Excel {#MicrosoftExcel}
#### Lectura Automática de Cabeceira de Columna e fila {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA poderá anunciar automáticamente as cabeceiras apropriadas de fila e columna ao navegar a través das follas de cálculo de Excel.
Primeiramente esto require que a opción Anunciar Cabeceiras de Fila e Columna de táboa nas opcións de NVDA Formateado de documentos, que se atopa no diálogo [Opcións de NVDA](#NVDASettings), estea activado.
En segundo lugar, NVDA necesita saber que fila ou columna contén as cabeceiras.
Despois de moverse á primeira celda na columna ou fila que conteña as cabeceiras, usa unha das seguintes ordes:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Fixar cabeceira de columnas |NVDA+shift+c |Ao premer esto unha vez dis ao NVDA que é a primeira celda de cabeceira da fila que contén as cabeceiras de columna, que debería ser anunciado automáticamente cando te despraces entre as columnas por embaixo desta fila. Premendo dúas veces eliminarase a opción.|
|Fixar cabeceira de filas |NVDA+shift+r |Ao premer esto unha vez dis ao NVDA que é a primeira celda da cabeceira da columna que contén as cabeceiras de fila, que debería ser anunciado automáticamente cando te despraces entre as filas despois desta columna. Premendo dúas veces eliminarás a opción.|

<!-- KC:endInclude -->
Estas opcións gardaranse na folla de cálculo coma rangos de nomes definidos, compatibles con outros lectores de pantalla coma Jaws.
Esto significa que outros usuarios de lectores de pantalla que abran esta folla de cálculo máis tarde terán automáticamente as cabeceiras de fila e columna xa postas. 

#### A Lista de Elementos {#ExcelElementsList}

De xeito similar á web, NVDA ten unha Lista de Elementos para Microsoft Excel, que che permite listar e aceder a varios tipos diferentes de información.
<!-- KC:beginInclude -->
Para aceder á Lista de Elementos en Excel, preme NVDA+f7.
<!-- KC:endInclude -->
Os diversos tipos de información dispoñible na Lista de Elementos son:

* Gráficos: esto lista todos os gráficos na folla de cálculo activa.
Selecionando un gráfico e premendo Intro ou o botón Mover A enfoca o gráfico para navegar e ler cas teclas de cursor.
* Comentarios: esto lista todas as celdas na folla de cálculo activa que conteñan comentarios. 
O enderezo da celda xunto cos seus comentarios amósase para cada celda. 
Premendo Intro ou o botón Mover a cando se estea sobre un comentario listado moverase directamente a esa celda.
* Fórmulas: esto lista todas as celdas na folla de cálculo activa que conteñan unha fórmula. 
O enderezo da celda xunto ca súa fórmula amósase para cada celda.
Premendo Intro ou o botón Mover A sobre unha fórmula listada moverase directamente a esa celda. 
* Follas: esto lista todas as follas no libro de traballo. 
Premendo f2 cando se estea sobre unha folla listada permíteche renomear a folla. 
Premendo Intro ou o botón Mover A mentres se estea sobre a folla listada cambiará a esa folla.
* Campos de formulario: esto lista todos os campos de formulario na folla de cálculo activa.
Para cada campo de formulario, a Lista de Elementos amosa o texto alternativo do campo xunto cos enderezos das celdas que cubra.
Ao selecionar un campo de formulario e ao premer intro ou o botón Mover móveste a ese campo en modo exploración.

#### Anunciar Notas {#ExcelReportingComments}

<!-- KC:beginInclude -->
Para anunciar calquera nota para a celda actualmente enfocada, preme NVDA+alt+c.
En Microsoft 2016, 365 e máis recentes, os clásicos comentarios en Microsoft Excel renomeáronse como "notas".
<!-- KC:endInclude -->
Todas as notas para a folla de cálculo tamén poden listarse na Lista de Elementos do NVDA premendo F7.

O NVDA tamén pode amosar un diálogo específico para engadir ou editar unha nota.
O NVDA sobreescribe a nota nativa de MS Excel editando a rexión debido a limitacións de acesibilidade, pero o atallo de teclado para amosar o diálogo érdase do MS Excel e polo tanto tamén funciona fora da execución do NVDA.
<!-- KC:beginInclude -->
Para engadir ou editar unha nota dada, nunha celda enfocada, preme shift+f2.
<!-- KC:endInclude -->

Este atallo de teclado non aparece e non se pode cambiar no diálogo Xestos de Entrada do NVDA.

Nota: tamén é posible abrir a rexión de edición de notas en MS Excel dende o menú de contexto de calquera celda da folla de cálculo.
Polo tanto, esto abrirá a rexión inaccesible de notas e non un diálogo específico de edición de notas do NVDA.

En Microsoft Office 2016, 365 e máis recente, engadiuse un novo diálogo estilo de comentario.
Este diálogo é accesible e proporciona máis características como respostas aos comentarios, etc.
Tamén pode abrirse dende o menú de contexto dunha celda determinada.
Os comentarios engadidos ás celdas a través do novo diálogo estilo de comentario non están relacionados coas "notas".

#### Ler Celdas Protexidas {#ExcelReadingProtectedCells}

Se un libro de traballo foi protexido, podería non seren posible mover o foco a celdas en particular que foran bloqueadas para edición.
<!-- KC:beginInclude -->
Para permitir o movemento a celdas bloqueadas, cambia a modo Exploración premendo NVDA+espazo, e entón usa as ordes estándar de movemento de Excel  como as teclas de cursor para moverte por todas as celdas na folla de cálculo actual.
<!-- KC:endInclude -->

#### Campos de Formulario {#ExcelFormFields}

As follas de cálculo de Excel poden incluir campos de formulario.
Podes aceder a éstos usando a Lista de Elementos ou as teclas de navegación cunha soa letra para campos de formulario f e shift+f.
Unha vez te movas a un campo de formulario en modo exploración, podes premer intro ou espazo para activalo ou cambiar a modo foco para poder interactuar con el, dependendo do control.
Para información adicional acerca do modo exploración e da navegación cunha soa tecla, consulta a [sección Modo Exploración](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|conmutar lectura de notas do orador |control+shift+s |Cando se está nunha presentación en execución, esta orde conmutará entre as notas do orador para a diapositiva e o contido da diapositiva. Esto só afecta ao que le NVDA, non ao que se amosa na pantalla.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Anunciar o tempo restante |control+shift+r |Anuncia o tempo restante da pista actualmente en reproducción, se hai algunha.|
|Anunciar o tempo transcorrido |control+shift+e |Anuncia o tempo transcorrido da pista actual en reprodución, se a hai.|
|Anunciar a lonxitude da pista |control+shift+t |Anuncia a lonxitude da pista actual en reprodución, se a hai.|

<!-- KC:endInclude -->

Nota: os atallos de teclado de arriba só funcionan coa cadea de formato predeterminada para a liña de estado de foobar.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Anunciar mensaxe recente |NVDA+control+1-4 |Anuncia unha das mensaxes recentes, dependendo do número premedo; ex.: NVDA+control+2 le a segunda mensaxe máis recente.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

O NVDA ofrece soporte mellorado para Poedit 3.4 ou máis recentes.

<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Anunciar notas para traductores |`control+shift+a` |Anuncia calquera nota para traductores. Se se preme dúas veces, presenta as notas en modo exploración|
|Anunciar Comentario |`control+shift+c` |Anuncia calquera comentario na xanela de comentarios. Se se preme dúas veces, presenta o comentario en modo exploración|
|Anunciar Texto Fonte Vello |`control+shift+o` |Anuncia o texto fonte vello, se o hai. Se se preme dúas veces, presenta o texto en modo exploración|
|Anunciar Advertencias de Traducción |`control+shift+w` |Anuncia unha advertencia de traducción, se a hai. Se se preme dúas veces, presenta a advertencia en modo exploración|

<!-- KC:endInclude -->

### Kindle para PC {#Kindle}

NVDA soporta a lectura e a navegación de libros no Amazon Kindle para PC.
Esta funcionalidade só está dispoñible en libros de Kindle designados con "Lector de Pantalla: Soportado" o que podes verificar na páxina de detalles para o libro.

Utilízase o modo exploración para ler libros.
Habilítase automáticamente ao se abrir un libro ou ao se enfocar o área do libro.
A páxina pasarase automáticamente segundo proceda cando movas o cursor ou uses a orde ler todo.
<!-- KC:beginInclude -->
Podes pasar á seguinte páxina manualmente coa tecla avPáx e voltar á anterior coa tecla rePáx.
<!-- KC:endInclude -->

Sopórtase a navegación cunha soa tecla para ligas e gráficos, pero só dentro da páxina actual.
A navegación por ligas tamén inclúe notas ao pé.

O NVDA proporciona soporte preliminar para a lectura e a navegación interactiva de contido matemático para libros coas matemáticas accesibles.
Por favor consulta a seción [Lendo Contido Matemático](#ReadingMath) para información adicional.

#### Seleción de Texto {#KindleTextSelection}

Kindle permíteche realizar varias funcións no texto selecionado, incluindo obter unha definición de diccionario, engadir notas e facer resaltados, copiar o texto ao portapapeis e procurar na web.
Para facer esto, primeiro seleciona texto coma o farías normalmente en modo exploración; ex.: usando shift e as teclas de cursor.
<!-- KC:beginInclude -->
Unha vez selecionaras o texto, preme a tecla aplicacións ou shift+f10 para amosar as opcións dispoñibles para traballar coa seleción.
<!-- KC:endInclude -->
Se fas esto sen texto selecionado, as opcións que se amosarán serán para a palabra no cursor.

#### Notas de Usuario {#KindleUserNotes}

Podes engadir unha nota con referencia a unha palabra ou a unha pasaxe de texto.
Para facer esto, primeiro seleciona o texto pertinente e accede ás opcións da seleción segundo se descrebiu arriba.
Logo, escolle Engadir Nota.

Ao ler no modo exploración, NVDA refírese a estas notas coma comentarios.

Para ver, editar ou borrar unha nota:

1. Move o cursor ao texto que conteña a nota.
1. Accede ás opcións para a seleción segundo se descrebiu arriba.
1. Escolle Editar Nota.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
Cando se estea na táboa de vista de libros engadidos:

| Nome |Tecla |Descripción|
|---|---|---|
|Entrar |intro |Abre o libro selecionado.|
|Menú de Contexto |aplicacións |Abre o menú de contexto para o libro selecionado.|

<!-- KC:endInclude -->

### Consola de Windows {#WinConsole}

O NVDA proporciona compatibilidade para a consola de ordes de Windows utilizada polo indicativo do sistema, PowerShell, e o subsistema Windows para Linux.
A ventá da consola é de tamano fixo, normalmente moito máis pequena que o búfer que contén a saída.
Segundo se escrebe un novo texto, o contido desprázase cara arriba e o texto anterior xa non é visible.
En versións de Windows anteriores a Windows 11 22H2, o texto que non se amosa visiblemente na ventá non é acesible cos comandos de revisión de texto do NVDA.
Polo tanto, é necesario desprazarse pola ventá da consola para ler o texto anterior.
Nas novas versións da consola e no Terminal de Windows, é posible revisar todo o búfer de texto libremente sen necesidade de desprazar a ventá.
<!-- KC:beginInclude -->
Os seguintes métodos abreviados de teclado incorporados na Consola de Windows poden seren útiles ao [revisar texto](#ReviewingText) co NVDA:

| Nome |Tecla |Descripción|
|---|---|---|
|Desprazar arriba |control+frecha arriba |Despraza a ventá da consola cara arriba, así pódese ler o texto anterior.|
|Desprazar abaixo |control+frecha abaixo |Despraza a ventá da consola cara abaixo, así pódese ler o texto posterior.|
|Desprazar ao comezo |control+inicio |Despraza a ventá da consola ao comezo do búfer.|
|Desprazar ao final |control+fin |Despraza a ventá da consola ao final do búfer.|

<!-- KC:endInclude -->

## Configurar o NVDA {#ConfiguringNVDA}

A maior parte da configuración pode realizarse usando caixas de diálogo ás que se accede mediante o submenú Preferencias do menú NVDA.
Moitas destas opcións poden atoparse na caixa de diálogo multipáxina [Opcións do NVDA](#NVDASettings).
En todas as caixas de diálogo, preme o botón Aceptar para acceptar calquera cambio que fixeras.
Para cancelar calquera cambio, preme o botón Cancelar ou a tecla escape.
Para certas caixas de diálogo, podes premer o botón aplicar para facer que as opcións teñan lugar imediatamente sen pechalo.
A maioría dos diálogos do NVDA soportan axuda de contexto.
<!-- KC:beginInclude -->
Cando se estea nun diálogo, premer `f1` abre a Guía do Usuario no parágrafo relativo á opción ou diálogo actual enfocado.
<!-- KC:endInclude -->
Algunhas opcións tamén poden cambiarse utilizando teclas de atallo,  que se listan onde sexan relevantes nas seccións subseguintes.

### Opcións do NVDA {#NVDASettings}

<!-- KC:settingsSection: || Nome | Tecla Escritorio | Tecla Portátil | Descripción | -->
O NVDA proporciona moitos parámetros de configuración que poden cambiarse usando o diálogo opcións.
Para que sexa máis doado atopar o tipo de opcións que queres cambiar, o diálogo amosa unha listaxe de categorías de configuración para escoller.
Cando seleciones unha categoría, amósanse na caixa de diálogo todas as opcións relacionadas con ela.
Para desprazarte polas categorías, usa `tab` ou `shift+tab` para aceder á listaxe de categorías, e logo usa as frechas arriba e abaixo para navegar pola listaxe.
Dende calquera parte do diálogo, tamén podes avanzar unha categoría premendo `ctrl+tab`, ou retroceder a outra premendo `shift+ctrl+tab`.

Unha vez modificada unha ou máis opcións, estas poden aplicarse usando o botón Aplicar, en tal caso que o diálogo permanecerá aberto, permitíndoche cambiar máis opcións ou escoller outra categoría.
Se desexas gardar a configuración e pechar a caixa de diálogo Opcións do NVDA, podes usar o botón Aceptar.

Algunhas categorías de opcións teñen un atallo de teclado dedicado.
Se se preme, este atallo de teclado abrirá  o diálogo Opcións do NVDA directamente nesa categoría en particular.
De xeito predeterminado, non se pode acesar a todas as categorías con ordes de teclado.
Se acedes con frecuencia a categorías que non teñan atallos de teclado dedicados, podes usar a [caixa de diálogo Xestos de Entrada](#InputGestures) para engadir un xesto personalizado coma unha orde de teclado ou un xesto tactil para esa categoría.

As varias categorías  de opcións que se atopan na caixa de diálogo Opcións do NVDA describiranse a continuación..

#### Xeral {#GeneralSettings}

<!-- KC:setting -->

##### Abrir Opcións Xerais {#toc109}

Tecla: `NVDA+control+g`

A categoría Xeral da caixa de diálogo Opcións do NVDA establece o comportamento xeral do NVDA, como a lingua da interfaz e se debería ou non comprobar as actualizacións.
Esta categoría contén as seguintes opcións:

##### Lingua {#GeneralSettingsLanguage}

Esta é unha caixa combinada que che permite seleccionar a lingua na que debería amosarse a interface do usuario e as mensaxes do NVDA. 
Hai moitas linguas, nembargantes a derradeira elección na lista chámase "Predeterminado para o usuario". 
Esta elección dirá ao NVDA que utilice a lingua na que Windows estea actualmente axustado. 

Por favor ten en conta que NVDA debe reiniciarse cando se cambie a lingua. 
Cando apareza o diálogo de confirmación, seleciona "reiniciar agora" ou "reiniciar máis tarde" se desexas usar a lingua nova agora ou nun momento posterior, respectivamente. Se está selecionado "reiniciar máis tarde", a configuración debe gardarse (ou manualmente ou usando a funcionalidade gardar ao saír).

##### Gardar Configuración ao Saír {#GeneralSettingsSaveConfig}

Esta opción é unha caixa de verificación que, cando se marca, di ao NVDA que garde automáticamente a actual configuración cando saias do NVDA. 

##### Amosar opcións de saída ao saír do NVDA {#GeneralSettingsShowExitOptions}

Esta opción é unha caixa de verificación que che permite escoller se aparece ou non un diálogo ao saír do NVDA que che pregunta sobre que acción queres lebar a cabo.
Cando se marque, aparecerá un diálogo ao intentar saír do NVDA preguntándoche se queres saír, reiniciar, reiniciar cos complementos deshabilitados ou instalar actualizacións pendentes se as hai.
Cando se desmarque, o NVDA sairá inmediatamente.

##### Reproducir sons ao iniciar ou saír do NVDA {#GeneralSettingsPlaySounds}

Esta Opción é unha caixa de verificación que, cando está marcada, di ao NVDA que reproduza sons cando se inicie ou saia.

##### nivel do Rexistro {#GeneralSettingsLogLevel}

Este é unha caixa combinada que che permite elexir canto NVDA porá no rexistro segundo se executa. 
Xeralmente os usuarios non deberían necesitar tocar esto xa que non é demasiado amigable. 
Sen embargo, se desexas proporcionar información nun informe de fallos, ou habilitar ou deshabilitar todo o rexistro, entón poderá seren unha opción útil.

Os niveis dispoñibles do rexistro son:

* Deshabilitado: aparte dunha curta mensaxe de inicio, o NVDA non rexistrará nada mentres se execute.
* Información: O NVDA rexistrará información básica coma mensaxes de inicio e información útil para os desenvolvedores.
* Aviso de depuración: rexistraranse mensaxes de aviso que non sexan causados por erros graves.
* Entrada/saída: rexistraranse as entradas das pantallas braille e dos teclados, así como a saída da voz e do braille.
* Se che preocupa a privacidade, non configures a esta opción de nivel de rexistro.
* Depuración: ademáis das mensaxes de información, aviso e entrada/saída, rexistraranse mensaxes de depuración adicionais.
* Ao igual que coa Entrada/saída, se che preocupa a privacidade, non deberías configurar o nivel de rexistro nesta opción.

##### Arrancar o NVDA despois de que inicie sesión {#GeneralSettingsStartAfterLogOn}

Se esta opción está activada, NVDA arrancará automáticamente tan pronto como inicies sesión en Windows. 
Esta opción só está dispoñible para copias instaladas do NVDA.

##### Usar o NVDA no inicio de sesión (require privilexios de administrador) {#GeneralSettingsStartOnLogOnScreen}

Se te autentificas en Windows proporcionando un nome de usuario e un contrasinal, entón activando esta opción farás que o NVDA se inicie automáticamente na pantalla de autentificación cando Windows se inicie. 
Esta opción só está dispoñible para copias instaladas do NVDA.

##### Utilizar Opcións gardadas actualmente durante o inicio de sesión e en pantallas seguras {#GeneralSettingsCopySettings}

Premendo este botón copias a túa configuración de usuario do NVDA actualmente gardada ao directorio de sistema de configuración do NVDA, tal que NVDA utilizaráo cando se execute durante o inicio de sesión, Control de Contas de Usuario (UAC) e outras pantallas seguras de Windows.
Para asegurarte de que todas as túas opcións se transfiren, asegúrate de gardar primeiramente a túa configuración con control+NVDA+c ou gardar a configuración no menú NVDA.
Esta opción só está dispoñible para copias instaladas do NVDA.

##### Procurar actualizacións para NVDA automáticamente {#GeneralSettingsCheckForUpdates}

Se esto está activado, NVDA procurará automáticamente versións actualizadas e informarache cando unha actualización estea dispoñible.
Tamén podes procurar actualizacións manualmente seleccionando Procurar Actualizacións baixo o menú Axuda no menú NVDA.
Cando se procuren actualizacións manual ou automáticamente, é necesario para NVDA enviar algunha información ao servidor de actualizacións para recibir a actualización correcta para o teu sistema.
Envíase sempre a seguinte información: 

* Versión actual do NVDA
* Versión do Sistema Operativo
* Se o Sistema Operativo é de 64 ou de 32 bits

##### Permitir a NV Access Recoller Estadísticas de Uso do NVDA {#GeneralSettingsGatherUsageStats}

Se esto está activado, NV Access usará a información das procuras de actualizacións para seguir o número de usuarios do NVDA incluíndo datos demográficos particulares coma o Sistema Operativo e o país de orixe.
Ten en conta que aíndaque o teu enderezo IP usarase para calcular o teu país durante a procura de actualizacións, o enderezo IP nunca se conservará.
Ademáis da información obrigatoria necesaria para procurar actualizacións, tamén se envía a seguinte información adicional actualmente:

* Lingua da interfaz do NVDA
* Se esta copia do NVDA é portable ou instalada
* O nome do sintetizador de voz actual en uso (incluíndo o nome do complemento que ven co controlador)
* O nome da pantalla Braille actual en uso (incluíndo o nome do complemento que ven co controlador)
* A táboa de saída braille actual (se o Braille está en uso)

Esta información axuda enormemente a NV Access a priorizar o desenvolvemento futuro do NVDA.

##### Notificar actualizacións pendentes ao comezar {#GeneralSettingsNotifyPendingUpdates}

Se esto está habilitado, o NVDA informarache cando hai unha actualización pendente ao comezar, ofrecéndoche a posibilidade de instalala.
Tamén podes instalar manualmente a actualización pendente dende o diálogo Saír do NVDA (se está habilitado), dende o menú NVDA, ou ao se realizar unha nova procura dende o menú Axuda.

#### Opcións de Voz {#SpeechSettings}

<!-- KC:setting -->

##### Abre opcións de Voz {#toc122}

Tecla: `NVDA+control+v`

A categoría voz na caixa de diálogo Opcións do NVDA contén axustes que che permiten cambiar o sintetizador de voz así como características da voz para o sintetizador escollido.
Para un xeito alternativo rápido de controlar os parámetros de voz dende calquer lugar, por favor mira a sección [Grupo de Opcións de Sintetizador](#SynthSettingsRing).

A categoría Opcións de voz contén os seguintes axustes:

##### Cambiar Sintetizador {#SpeechSettingsChange}

O primeiro axuste na categoría Opcións de Voz é o botón Cambiar... Este botón activa a caixa de diálogo [Selecionar Sintetizador](#SelectSynthesizer), o que che permite selecionar o sintetizador de voz activo e o dispositivo de son.
Este diálogo ábrese por enriba da caixa de diálogo Opcións do NVDA.
Gardando ou descartando as opcións na caixa de diálogo Selecionar Sintetizador voltarás ao diálogo Opcións do NVDA.

##### Voz {#SpeechSettingsVoice}

A opción voz é unha caixa combinada que enumera todas as voces do sintetizador actual que instalaches.
Podes utilizar as teclas de cursor para escoitar todas as varias eleccións. 
As frechas esquerda e arriba suben pola lista, mentres que as frechas dereita e abaixo baixan pola lista.

##### Variante {#SpeechSettingsVariant}

Se estás a usar o sintetizador Espeak NG empaquetado xunto co NVDA, esta é unha caixa combinada que che permite seleccionar a variante ca que o sintetizador debería falar. 
As variantes de Espeak NG son bastante parecidas ás voces, pero proporcionan atributos lixeiramente diferentes para a voz de ESpeak NG. 
Algunhas variantes soarán como un home, algunhas como unha muller, e algunhas como se tiveran ronqueira.
Se usas un sintetizador de terceiros, tamén poderás cambiar este valor se a voz escollida o admite.

##### Velocidade {#SpeechSettingsRate}

Esta opción permíteche cambiar a velocidade da voz. 
Esta é unha barra de desprazamento que vai dende 0 ata 100, (sendo 0 a velocidade máis lenta e sendo 100 a máis rápida).

##### Aumento da Velocidade {#SpeechSettingsRateBoost}

Habilitar esta opción aumentará significativamente a velocidade da voz se está admitida polo sintetizador actual.

##### Ton {#SpeechSettingsPitch}

Esta opción permíteche cambiar o ton da voz. 
Esta é unha barra de desprazamento que vai dende 0 ata 100, (sendo 0 o ton máis baixo e sendo 100 o máis alto). 

##### Volume {#SpeechSettingsVolume}

Esta opción é unha barra de desprazamento que vai dende 0 ata 100, (sendo 0 o volume máis baixo e sendo 100 o máis alto).

##### Entoación {#SpeechSettingsInflection}

Esta opción é unha barra de desprazamento que che permite elexir canta entoación (subida e caída no ton) o sintetizador debería utilizar para falar. (Soamente o sintetizador Espeak NG proporciona esta opción actualmente).

##### Cambio Automático de Lingua {#SpeechSettingsLanguageSwitching}

Esta caixa de verificación permíteche activar ou desactivar se NVDA debería cambiar automáticamente as linguas do sintetizador de voz se o texto a se ler o especifica.
Esta opción está activada de maneira predeterminada.

##### Cambio Automático de Dialecto {#SpeechSettingsDialectSwitching}

Esta caixa de verificación permíteche activar ou desactivar  se os cambios de dialecto deberíanse facer, en lugar de só cambiar a lingua actual. 
Por Exemplo Se se está lendo nunha voz Inglés U.S. pero partes dun documento teñen algún texto en Inglés U.K. entón se esta característica está activada o sintetizador cambiará o seu acento.
Esta opción está desactivada de forma predeterminada.

<!-- KC:setting -->

##### Nivel de Puntuación e símbolos {#SpeechSettingsSymbolLevel}

Tecla: NVDA+p

Esto permíteche escoller a cantidade de puntuación e outros símbolos que deberían dicirse como palabras.
Por exemplo, cando se configura a toda, todos os símbolos diranse como palabras.
Esta opción aplícase a todos os sintetizadores, non só ao sintetizador activo actualmente.

##### Confiar na Linguaxe da voz ao procesar símbolos e caracteres {#SpeechSettingsTrust}

Activada de xeito predeterminado, esta opción di ao NVDA se a lingua da voz actual pode ser de confianza ao procesar símbolos e caracteres.
Se notas que o NVDA está lendo a puntuación nunha lingua incorrecta para un sintetizador ou voz en particular, poderás querer desactivar esta opción para forzar ao NVDA a usar a súa lingua global configurada no su lugar.

##### Incluir datos Unicode Consortium (incluindo emoji) ao procesar caracteres e símbolos {#SpeechSettingsCLDR}

Cando esta caixa de verificación estea activada, o NVDA incluirá os diccionarios de pronunciación de símbolos adicional cando pronuncie caracteres e símbolos.
Estos dicionarios conteñen descripcións para símbolos (en particular emoji) que se proporcionan polo [Unicode Consortium](https://www.unicode.org/consortium/) como parte do seu [Common Locale Data Repository](http://cldr.unicode.org/).
Se queres que o NVDA fale descripcións de caracteres emoji baseados nestes datos, deberías habilitar esta opción.
Polo tanto, se estás a usar un sintetizador de voz que admita a fala de descripcións de emoji nativamente, deberías desactivar esto.

Ten en conta que as descripcións de caracteres engadidas ou editadas manualmente gárdanse como parte das túas opcións de usuario.
Polo tanto, se cambias a descripción dun emoji en particular, a túa descripción persoalizada falarase para ese emoji sen importar se esta opción está habilitada.
Podes engadir, editar ou borrar descripcións de símbolos no [diálogo de pronunciación de puntuación e símbolos](#SymbolPronunciation) do NVDA.

Para activar ou desactivar a inclusión de Unicode Consortium data dende calquera sitio, por favor asigna un xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

##### Cambio da Porcentaxe de Ton para Maiúsculas {#SpeechSettingsCapPitchChange}

Este campo de edición permíteche teclear a cantidade na que o ton da voz cambiará cando se fale unha letra maiúscula.
Este valor é unha porcentaxe, onde un valor negativo baixa o ton e un valor positivo súbeo.
Para non cambiar o ton utilizarías o 0.
Normalmente, o NVDA sube o ton lixeiramente para calquera letra en maiúsculas, pero algúns sintetizadores poden non admitir esto ben.
En caso de que non se admita o cambio de ton para as maiúsculas, considera usar [Falar "maius" antes de maiúsculas](#SpeechSettingsSayCapBefore) e/ou [Pitar  para maiúsculas](#SpeechSettingsBeepForCaps) no seu lugar.

##### Dicir Maius" antes de Maiúsculas {#SpeechSettingsSayCapBefore}

Esta opción é unha caixa de verificación, que cando está marcada di ao NVDA que diga a palabra "maius" antes de calquera letra en maiúscula, cando se navega sobre ela ou falándoo cando está sendo escribida.

##### Pitar para Maiúsculas {#SpeechSettingsBeepForCaps}

Se esta caixa de verificación está marcada, NVDA emitirá un pequeno pitido cada vez que estea falando un caracter en maiúscula. 

##### Utilizar funcionalidade de deletreo se está soportada {#SpeechSettingsUseSpelling}

Algunhas palabras consisten en só un carácter, pero a pronunciación é diferente dependendo de se o carácter vai ser falado como un carácter individual (como cando se deletrea) ou unha palabra.
Por exemplo, en galego, "e" é tanto unha letra como una palabra e pronúnciase de modo diferente en cada caso.
Esta opción permite ao sintetizador diferenciar entre estos dous casos se o sintetizador o soporta.
A maioría dos sintetizadores sopórtano.

Esta opción xeralmente debería activarse.
Nembargantes, algúns sintetizadores Microsoft Speech API non implementan esto correctamente e funciona anómalamente cando se activa.
Se estás a ter problemas ca pronunciación de carácteres individuais,  proba desactivando esta opción.

##### Descripcións retrasadas para caracteres en movementos do cursor {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
| Predeterminada |Deshabilitada|
|---|---|
| Opcións |Habilitada, Deshabilitada|
|---|---|

Cando esta opción está marcada, o NVDA dirá a descipción do carácter cando te movas por caracteres.

Por exemplo, mentres revisas unha liña por caracteres, cando se lea a letra "b" o NVDA dirá "Bravo" tras 1 segundo de retraso.
Esto pode seren útil se che costa distinguir entre la pronunciación dos símbolos, ou para usuarios con dificultades auditivas.

A descripción retrasada de caracteres cancelarase se se fala outro texto durante ese tiempo, ou se ti premes a tecla `control`.

##### Modos dispoñibles na orde percorrer modos de voz {#SpeechModesDisabling}

Esta listaxe marcable permite selecionar que [modos de voz](#SpeechModes) se inclúen ao percorrer entre eles usando `NVDA+s`.
Os modos que estean desmarcados exclúense.
Por defecto inclúense todos os modos.

Por exemplo se non necesitas usar o modo "pitidos" e "desactivado" deberías desmarcalos, e conservar marcados "falar" e "baixo demanda".
Ten en conta que é necesario polo menos marcar dous modos.

#### Selecionar Sintetizador {#SelectSynthesizer}

<!-- KC:setting -->

##### Abrir o diálogo Selecionar Sintetizador {#toc143}

Tecla: `NVDA+control+s`

A caixa de diálogo Sintetizador, o que pode abrirse activando o botón Cambiar... na categoría voz do diálogo Opcións do NVDA, permíteche selecionar que Sintetizador debería usar o NVDA para falar.
Unha vez selecionaras o sintetizador da túa eleción, podes premer Aceptar e o NVDA cargará o sintetizador selecionado.
Se hai un erro cargando o sintetizador, o NVDA diracho cunha mensaxe, e continuará usando o anterior.

##### Sintetizador {#SelectSynthesizerSynthesizer}

Esta opción permíteche escoller o sintetizador que desexes que use o NVDA para a saída de voz.

Para unha listaxe dos sintetizadores que soporta o NVDA, consulta a seción [Sintetizadores de voz admitidos](#SupportedSpeechSynths).

Un elemento especial que sempre aparecerá nesta listaxe é "sen voz", que che permite usar o NVDA sen saída de voz.
Esto pode ser útil para alguén que desexe só usar o NVDA con braille, ou quizáis para desenvolvedores videntes que só queran usar o Visualizador de voz.

#### Anel de Opcións do Sintetizador {#SynthSettingsRing}

Se desexas cambiar rápidamente opcións de voz  sen ir á categoría Voz do diálogo Opcións do NVDA, hai algunhas teclas de ordes do NVDA que che permiten moverte a través das opcións de voz máis comúns, dende calquer lugar mentres se executa NVDA:
<!-- KC:beginInclude -->

| Nome |Tecla Sobremesa |Tecla Portátil |Descripción|
|---|---|---|---|
|Mover á seguinte opción de sintetizador |NVDA+control+Frecha dereita |NVDA+shift+control+Frecha dereita |Móvese á seguinte opción de voz dispoñible despois da actual, pasando pola primeira opción de novo despois da derradeira|
|Mover á opción de sintetizador anterior |NVDA+control+Frecha esquerda |NVDA+shift+control+Frecha esquerda |Móvese á opción de voz anterior dispoñible despois da actual, pasando pola primeira opción de novo despois da derradeira|
|Incrementar actual opción de sintetizador |NVDA+control+Frecha arriba |NVDA+shift+control+Frecha arriba |incrementa a opción de voz actual sobre a que esteas. Ex.: incrementa a velocidade, elixe a seguinte voz, incrementa o volume|
|Decrementar actual opción de sintetizador |NVDA+control+Frecha abaixo |NVDA+shift+control+Frecha abaixo |decrementa a opción de voz actual sobre a que esteas. Ex.: decrementa a velocidade, elixe  a voz anterior, decrementa o volume|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

A categoría Braille no diálogo Opcións do NVDA contén axustes que che permiten cambiar varios aspectos da entrada e saída braille.
Esta categoría contén as seguintes opcións:

##### Cambiar pantalla braille {#BrailleSettingsChange}

O botón Cambiar... na categoría Braille da caixa de diálogo Opcións do NVDA activa o diálogo [Selecionar Pantalla Braille](#SelectBrailleDisplay), o que che permite selecionar a pantalla braille activa.
Esta caixa de diálogo ábrese sobre o diálogo Opcións do NVDA.
Gardando ou descartando as opcións no diálogo Selecionar Pantalla Braille voltarás á caixa de diálogo Opcións do NVDA.

##### Táboa de Saída {#BrailleSettingsOutputTable}

A seguinte opción que virá nesta categoría é a caixa combinada da táboa de saída braille.
Nesta caixa combinada, atoparás táboas braille, estándares braille e graos para diferentes linguas.
A táboa escollida utilizarase para transcribir texto a braille para presentalo na pantalla braille.
Podes moverte entre as táboas braille na lista utilizando as teclas do cursor.

##### Táboa de Entrada {#BrailleSettingsInputTable}

Comprementariamente coa opción anterior, o seguinte axuste que atoparás é a caixa combinada da táboa de entrada braille.
A táboa escollida utilizarase para transcribir a texto o braille introducido no teclado tipo perkins da liña braille.
Podes moverte entre as táboas braille na lista utilizando as teclas de cursor.

Ten en conta que esta opción só é útil se a túa pantalla braille ten un teclado tipo Perkins e se esta característica se soporta polo controlador da liña braille.
Se a entrada non se soporta nunha pantalla que teña un teclado braille, esto notificarase na sección [Pantallas Braille Soportadas](#SupportedBrailleDisplays).

<!-- KC:setting -->

##### Modo Braille {#BrailleMode}

Tecla: `NVDA+alt+t`

Esta opción permíteche selecionar entre os modos braille dispoñibles.

Actualmente admítense dous modos braille, "seguir cursores" e "amosar saída de fala".

Cando estea selecionado seguir cursores, a pantalla braille seguirá ou ao foco e ao cursor do sistema ou ao navegador de obxectos e ao cursor de revisión, dependendo a que sega o braille.

Cando estea selecionado amosar saída de fala, a pantalla braille amosará o que fhale o NVDA, ou o que tería falado se o modo de fala estivera en "fhalar".

##### Expandir a braille de ordenador para a palabra no cursor {#BrailleSettingsExpandToComputerBraille}

Esta opción permite á palabra que está baixo o cursor seren amosada en braille de ordenador non contraído.

##### Amosar Cursor {#BrailleSettingsShowCursor}

Esta opción permite ao cursor braille activarse e desactivarse.
Aplícase ao cursor do sistema e ao cursor de revisión, pero non ao indicador de seleción.

##### Parpadeo de Cursor {#BrailleSettingsBlinkCursor}

Esta opción permite ao cursor braille parpadear.
Se o parpadeo está desactivado, o cursor braille estará constantemente na posición "subida".
O indicador de seleción non está afectado por esta opción, sempre é cos puntos 7 e 8 sen parpadear.

##### Velocidade de Parpadeo do Cursor (ms) {#BrailleSettingsBlinkRate}

Esta opción é un campo numérico que che permite cambiar a velocidade de palpebreo do cursor en milésimas de segundo.

##### Forma do Cursor para o Foco {#BrailleSettingsCursorShapeForFocus}

Esta opción permíteche escoller a forma (patrón de puntos) do cursor braille cando o braille sega ao foco.
O indicador de seleción non está afectado por esta opción, sempre son os puntos 7 e 8 sen palpebrar.

##### Forma do Cursor para a Revisión {#BrailleSettingsCursorShapeForReview}

Esta opción permíteche escoller a forma (patrón de puntos) do cursor braille cando o braille sega á revisión.
O indicador de seleción non está afectado por esta opción, sempre son os puntos 7 e 8 sen palpebrar.

##### Amosar Mensaxes {#BrailleSettingsShowMessages}

Este é unha caixa combinada que che permite selecionar se o NVDA debería amosar as mensaxes braille e cando deberían desaparecer automáticamente.

Para conmutar amosar mensaxes dende calquera lugar, por favor asigna un xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

##### Duración da Mensaxe (en seg) {#BrailleSettingsMessageTimeout}

Esta opción é un campo numérico que controla durante canto tempo se amosan as mensaxes do sistema na pantalla braille.
A mensaxe do NVDA péchase inmediatamente ao se premer un sensor na pantalla braille, pero aparece de novo ao se premer a correspondente tecla que o disparou.
Esta opción só se amosa se se pon "Amosar Mensaxes" en "Usar Tempo de Espera".

<!-- KC:setting -->

##### Braille Segue {#BrailleTether}

Tecla: NVDA+control+t

Esta opción permíteche escoller se a pantalla braille seguirá ao foco do sistema ou ao cursor, ou se seguirá ao navegador de obxectos / cursor de revisión, ou a ambos.
Cando se selecione "automáticamente", o NVDA seguirá ao foco e ao cursor do sistema por omisión.
Neste caso, cando se cambie a posición do navegador de obxectos ou do cursor de revisión mediante unha interacción explícita do usuario, o NVDA seguirá á revisión temporalmente, ata que o foco ou o cursor cambie.
Se o queres seguindo ao foco e cursor só, necesitas configurar o braille para que sega ao foco.
Neste caso, o braille non seguerá ao navegador de obxectos do NVDA durante a navegación de obxectos ou ao cursor de revisión durante a revisión.
Se queres que o braille sega á navegación de obxectos e á revisión de texto no  seu lugar, necesitas configurar  o braille para que sega á revisión.
Neste caso, o Braille non seguerá ao foco del sistema e ao cursor.

##### Mover o cursor do sistema ao enrutar o cursor de revisión {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminada (Nunca), Nunca, só cando segue automáticamente, Sempre|
| Predeterminada |Nunca|

Esta opción determina se o cursor do sistema tamén debería moverse ao premer un sensor de enrutamento.
Esta opción está configurada a nunca por defecto, o que significa que o enrutamento nunca moverá o cursor do sistema ao enrutar o cursor de revisión.

Cando esta opción estea configurada a Sempre, e o [seguemento do braille](#BrailleTether) estea configurado a "automáticamente" ou "a revisar", ao premer un sensor do cursor sempre se moverá o cursor do sistema ou o foco cando estea admitido.
Cando o modo de revisión actual sexa [Revisión de pantalla](#ScreenReview), non hai cursor do sistema físico.
Neste caso, o NVDA tenta enfocar o obxecto baixo o texto ao que se estea dirixindo.
O mesmo aplícase á [revisión de obxectos](#ObjectReview).

Tamén podes configurar esta opción a mover só o cursor do sistema cando se sega automáticamente.
Nese caso, premer un sensor de enrutamento  só moverá o cursor do sistema ou o foco cando o NVDA estea seguindo ao cursor de revisión automáticamente, mentres que non se producirá ningún movemento cando o sega manualmente.

Esta opción só se amosa se "[seguir ao braille](#BrailleTether)" está configurado a "Automáticamente" ou "a revisión".

Para conmutar mover o cursor do sistema ao enrutar o cursor de revisión dende calquera lugar, por favor asigna un xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

##### Ler por Parágrafo {#BrailleSettingsReadByParagraph}

Se está activada, o braille amosarase por parágrafos en lugar de por liñas.
Tamén, as ordes de liña seguinte e anterior moverán por parágrafos en concordancia.
Esto significa que non tes que desprazar a pantalla ao final de cada liña incluso onde haia máis texto do que cabe na pantalla.
Esto podería permitir unha mayor fluidez lendo longas cantidades de texto.
Está desactivada de xeito predeterminado.

##### Evitar separación de palabras cando sexa posible {#BrailleSettingsWordWrap}

Se esto está habilitado, unha palabra que sexa demasiado longa para coller no final da pantalla braille non se separará.
No seu lugar, haberá algúns espazos en branco ao final da pantalla.
Cando despraces a pantalla, poderás ler toda a palabra.
Esto chámase en ocasións "axuste de liña".
Ten en conta que se a palabra é demasiado longa para coller na pantalla incluso por si mesma, a palabra aínda debe ser partida.

Se esto está deshabilitado, amosarase tanto como sexa posible da palabra, pero o resto cortarase.
Cando despraces a pantalla, entón poderás ler o resto da palabra.

Habilitar esto podería permitir unha maior fluidez na lectura, pero normalmente require desprazar a pantalla máis.

##### Presentación de Contexto do Foco {#BrailleSettingsFocusContextPresentation}

Esta opción permíteche escoller que información de contexto amosará o NVDA na pantalla braille cando un obxecto obteña o foco.
A información de contexto refírese á xerarquía de obxectos que conteñan o foco.
Por exemplo, cando enfoques un elemento de lista, este elemento de lista é parte dunha lista.
Esta lista podería estar contida nun diálogo, etc.
Por favor consulta a seción acercqa de [navegación de obxectos](#ObjectNavigation) para máis información acerca da xerarquía que se aplica aos obxectos no NVDA.

Cando se configure en rechear pantalla para cambios de contexto, o NVDA tentará amosar tanta información de contexto como lle sexa posible na pantalla braille, pero só para as partes do contexto que cambiaran.
Para o exemplo de enriba, esto siñifica que cando o foco cambie pola lista, o NVDA amosará o elemento de lista na pantalla braille.
Ademáis, se queda espazo suficiente na pantalla braille, o NVDA tentará amosar que o elemento de lista é parte dunha lista.
Se, a continuación, comezas a moverte pola lista coas teclas de cursor, suponse que eres consciente de estar aínda na lista.
Polo tanto, para os elementos de lista restantes que enfoques, o NVDA só amosará o elemento de lista enfocado na pantalla.
Para ler o contexto de novo (é dicir, que estás nunha lista e que a lista é parte dun diálogo), terás que desprazar a túa pantalla braille cara atrás.

Cando esta opción estea configurada a rechear sempre a pantalla, o NVDA tentará amosar tanta información de contexto como lle sexa posible na pantalla braille, independentemente de se viches a mesma información de contexto antes.
Esto ten a ventaxa de que o NVDA axustará tanta información coma sexa posible na pantalla.
Polo tanto, a desventaxa é que sempre hai unha diferencia na posición onde comeza o enfoque na pantalla braille.
Esto pode facer difícil andar por unha lista longa de elementos, por exemplo, xa que terás que mover contínuamente o dedo para atopar o comezo do elemento.
Este era o conmportamento predeterminado para o NVDA 2017.2 e anteriores.

Cando configures a opción presentación de contexto do foco en amosar só a información de contexto ao desprazarse cara atrás, o NVDA nunca amosa información de contexto na pantalla braille por omisión.
Así, no exemplo anterior, o NVDA amosará que enfocaches un elemento de lista.
Polo tanto, para ler o contexto (é dicir, que estás nunha lista e que esta lista é parte dun diálogo), terás que desprazar a pantalla braille cara atrás.

Para conmutar a presentación de contexto do foco dende calquera lugar, por favor asigna un xesto personalizado usando o [diálogo Xestos de Entrada](#InputGestures).

##### Interrumpir fala  mentres se despraza {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminada (Habilitada), Habilitada, Deshabilitada|
| Predeterminada |Habilitada|

Esta opción determina se a voz debería interrumpirse cando a pantalla Braille se desprace cara adiante ou cara atrás.
As ordes de liña anterior e seguinte sempre interrumpen a fala.

A voz falando podería seren unha distración mentres se le en Braille.
Por esta razón a opción está habilitada por defecto, interrumpindo a voz ao desprazar o braille.

Deshabilitar esta opción permite que a voz se escoite mentres se le en braille simultáneamente.

##### Amosar seleción {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminada (Habilitada), Habilitada, Deshabilitada|
| Predeterminada |Habilitada|

Esta opción determina se se amosa o indicador de seleción (puntos 7 e 8) na pantalla braille.
A opción está habilitada por defecto para que se amose o indicador de selección.
O indicador de seleción podería seren unha distración durante a lectura.
Deshabilitar esta opción pode mellorar a lexibilidade.

Para conmutar amosar seleción dende calquera lugar, por favor asigna un xesto persoalizado usando o [diálogo Xestos de entrada](#InputGestures).

#### Selecionar Pantalla Braille {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Abrir o diálogo Selecionar Pantalla Braille {#toc166}

Tecla: `NVDA+control+a`

A caixa de diálogo Selecionar Pantalla Braille, o que se pode abrir activando o botón Cambiar... na categoría Braille do diálogo Opcións do NVDA, permíteche selecionar que pantalla braille debería usar o NVDA para a saída braille.
Unha vez selecionaras a pantalla braille da túa eleción, podes premer Aceptar e o NVDA cargará a pantalla selecionada.
Se hai un erro carghando o controlador da pantalla, o NVDA notificaracho cunha mensaxe, e continuará usando a pantalla anterior, se hai algunha.

##### Pantalla Braille {#SelectBrailleDisplayDisplay}

Esta caixa combinada preséntaseche con varias opcións dependendo de que controladores de pantalla braille estean dispoñibles no teu sistema.
Móvete entre estas opcións coas teclas de frechas.

A opción automático permitirá ao NVDA procurar moitas pantallas braille admitidas de fondo.
Cando esta característica estea activada e conectes unha pantalla admitida usando USB ou bluetooth, o NVDA conectará automáticamente con ela.

Sen braille significa que non estás usando braille.

Por favor consulta a seción [Pantallas Braille Admitidas](#SupportedBrailleDisplays) para máis información sobre de ditas pantallas braille e de cales delas admiten a conexión automática.

##### Pantallas a se detectar automáticamente {#SelectBrailleDisplayAutoDetect}

Cando a pantalla braille está configurada en "Automático", as caixas de verificación neste control de listaxe permítenche habilitar e deshabilitar os controladores de pantalla que participarán no proceso de detección automática.
Esto permíteche excluir os controladores das pantallas braille que non uses de cotío.
Por exemplo, se só tes unha pantalla que necesite o controlador Baum para funcionar, podes deixar activado dito controlador e desactivar os demáis.

Por omisión, todos os controladores compatibles coa detección automática están habilitados.
Calquera controlador engadido, por exemplo nunha versión futura do NVDA ou nun complemento, tamén se ahbilitará por defecto.

Podes consultar a documentación para a túa pantalla braille na seción [Pantallas Braille Admitidas](#SupportedBrailleDisplays) para comprobar se o controlador soporta a detección automática de pantallas.

##### Porto {#SelectBrailleDisplayPort}

Esta opción, se está dispoñible, permíteche escoller que porto ou tipo de conexión se usará para comunicar coa pantalla braille que selecionaches.
É unha caixa combinada que contén as elecións posibles para a túa pantalla braille.

Por omisión, o NVDA emprega a deteción de porto automática,  o que significa que a conexión co dispositivo braille se estabrecerá automáticamente buscando os dispositivos USB e bluetooth no teu sisttema.
Polo tanto, para algunhas pantallas braille, poderás escoller explícitamente que porto debería usarse.
As opcións comúns son "Automático" (a que di ao NVDA que empregue o procedemento de seleción de porto automático predeterminado), "USB", "Bluetooth" e portos serie herdados se a túa pantalla braille admite este tipo de comunicación.

Esta opción non estará dispoñible se a túa pantalla braille só admite detección automática de portos.

Podes consultar a documentación para a túa pantalla braille na seción [Pantallas Braille Admitidas](#SupportedBrailleDisplays) para procurar máis detalles sobre os tipos compatibles de comunicación e portos dispoñibles.

Nota importante: se conectas varias Pantallas Braille a túa máquina ao mesmo tempo que usan o mesmo controlador (Ex.: connectar dúas pantallas Seika),
actualmente é imposible decirlle ao NVDA que pantalla debe usr.
Polo tanto, recoméndase conectar só unha Pantalla Braille dun determinado tipo de fabricante a túa máquina ao mesmo tempo.

#### Audio {#AudioSettings}

<!-- KC:setting -->

##### Abrir Opcións de Audio {#toc171}

Tecla: `NVDA+control+u`

A categoría Audio no diálogo de configuración do NVDA contén opcións que che permiten cambiar varios aspectos da saída de audio.

##### Dispositivo de Saída {#SelectSynthesizerOutputDevice}

Esta opción permíteche escoller a tarxeta de son que o NVDA debería indicar para que o sintetizador selecionado fale.

<!-- KC:setting -->

##### Modo Atenuación de Audio {#SelectSynthesizerDuckingMode}

Key: NVDA+shift+d

Esta opción permíteche escoller se o NVDA debería reducir o volume de outras aplicacións mentres estea falando, ou todo o tempo mentres o NVDA se estea a executar.

* Sen Atenuación: o NVDA nunca reducirá o volume do outro audio. 
* Atenuar cando saian voz e sons: o NVDA só reducirá o volume do outro audio cando o NVDA estea falando ou reproducindo sons. Esto pode non funcionar para todos os sintetizadores. 
* Atenuar Sempre: o NVDA manterá o volume do outro audio reducido durante todo o tempo no que estea en execución.

Esta opción só estará dispoñible se se instalou o NVDA.
Non é posible o soporte da atenuación de audio para as copias portable e temporal do NVDA.

##### O volume dos sons do NVDA segue ao volume da voz {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Deshabilitada, Habilitada|
| Predeterminada |Deshabilitada|

Cando esta opción está activada, o volume dos sons e os pitidos do NVDA seguerán a configuración de volume da voz que esteas a usar.
Se disminúes o volume da voz, o volume dos sons diminuirá.
Do mesmo xeito, se aumentas o volume da voz, o volume dos sons aumentará.
Esta opción non está dispoñible se arancaches o NVDA co [WASAPI deshabilitado para a saída de audio](#WASAPI) nas Opcións Avanzadas.

##### Volume dos sons do NVDA {#SoundVolume}

Este deslizador permíteche configurar o volume dos sons e os pitidos do NVDA.
Esta opción só ten efecto  cando "Usar WASAPI para a saída de audio" estea habilitado e "O Volume dos sons do NVDA segue ao volume da voz" estea deshabilitado.
Esta opción non está dispoñible se arancaches o NVDA co [WASAPI deshabilitado para a saída de audio](#WASAPI) nas Opcións Avanzadas.

##### Tempo para manter o dispositivo de audio desperto tras a fala {#AudioAwakeTime}

Esta caixa de edición especifica canto tempo mantén o NVDA o dispositivo de audio desperto despois de que deixe de falar.
Esto permite ao NVDA evitar certos fallos da fala coma partes de palabras soltas.
Esto pode ocorrer debido a que os dispositivos de audio (especialmente dispositivos Bluetooth e wireless) entren en modo de espera.
Esto tamén podería seren útil noutros casos de uso, coma cando se executa o NVDA dentro dunha máquina virtual (ex.: Citrix Virtual Desktop), ou en certos portátiles.

Os valores máis baixos poden permitir que o audio se corte máis de cotío, xa que un dispositivo pode entrar en modo de espera demasiado cedo, facendo que  o comezo da seguinte fala se curte.
Un valor demasiado alto pode facer que a batería do dispositivo de saída de son se descargue máis rápidamente, xa que permanece activo durante máis tempo mentres non se envía son.

Podes estabrecer o tempo a cero para deshabilitar esta característica.

##### Separación de son {#SelectSoundSplitMode}

A característica separación de son permite aos usuarios usar os seus dispositivos de saída en estéreo, como auriculares e altavoces.
A separación de son fai posible que o NVDA fale nunha canle (ex.: a esquerda) e ter as outras aplicacións reproducindo o seu son na outra canle (ex.: a dereita).
Por defecto a separación de son está deshabilitada, o que significa que todas as aplicacións incluíndo ao NVDA reproducirán o son en ambas as dúas canles.
Un xesto permite percorrer os distintos modos de separación de son:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Modo Cíclico de Separación de Son |`NVDA+alt+s` |percorre os modos de separación de son.|

<!-- KC:endInclude -->

Por defecto esta orde percorrerá os seguintes modos:

* Separación de son deshabilitada: o NVDA e as demáis aplicacións sacan os sons por ambas canles.
* NVDA na esquerda e as aplicacións na dereita: o NVDA falará pola canle esquerda, mentres as outras aplicacións reproducirán o son pola canle da dereita.
* NVDA na dereita e as aplicacións na esquerda: o NVDA falará pola canle da dereita, mentres as outras aplicacións reproducirán o son pola canle da esquerda.

Hai máis modos avanzados de separación de son dispoñibles na caixa combinada nas opcións do NVDA.
Ten en conta que a separación de son non funciona coma un mixturador.
Por exemplo, se unha aplicación está reproducindo unha pista de son estéreo mentres a división de son está configurada a "NVDA na esquerda e as aplicacións na dereita", entón só oirás a canle dereita da pista de son, mentres a canle esquerda da pista de son estará silenciada.

Esta opción non está dispoñible se arrancaches o NVDA con [WASAPI deshabilitado para a saída de audio](#WASAPI) nas opcións avanzadas.

Ten en conta que se o NVDA se bloquea, entón non poderás restaurar o volume dos sons da aplicación, e esas aplicacións poderían seguir emitindo o son só nunha canle tras o bloqueo do NVDA.
Para mitigar esto, por favor reinicia o NVDA.

##### Persoalizar modos de Separación de Son {#CustomizeSoundSplitModes}

Esta listaxe marcable permite selecionar que modos de separación de son se inclúen ao percorrer entre eles usando `NVDA+alt+s`.
Os modos que estean desmarcados esclúense.
Por defecto só se inclúen tres modos.

* Separación de son deshabilitada: NVDA e as aplicacións reproducen o son en ambas canles.
* NVDA na canle esquerda e as outras aplicacións na dereita.
* NVDA na canle dereita e as outras aplicacións na esquerda.

Ten en conta que é necesario marcar polo menos un modo.
Esta opción non está dispoñible se iniciaches o NVDA con [WASAPI deshabilitado para a saída de audio](#WASAPI) nas opcións avanzadas.

#### Visión {#VisionSettings}

A categoría Visión no diálogo opcións do NVDA permíteche activar, desactivar e configurar [axudas visuais](#Vision).

Ten en conta que as opcións dispoñibles nesta categoría poderían ampliarse con [complementos do NVDA](#AddonsManager).
Por defecto, esta categoría de axustes contén as seguintes opcións:

##### Resaltado Visual {#VisionSettingsFocusHighlight}

As caixas de verificación no grupo Resaltado Visual controlan o comportamento da función integrada [Resaltar Foco](#VisionFocusHighlight) do NVDA.

* Activar Resaltado: activa e desactiva o resaltado visual.
* Resaltar foco do sistema: conmutará se se resalta ou non o [foco do sistema](#SystemFocus).
* Resaltar navegador de obxectos: conmuta se se resaltará ou non o [navegador de obxectos](#ObjectNavigation).
* Resaltar cursor de modo Exploración: conmuta se se resaltará ou non o [cursor virtual do modo Exploración](#BrowseMode).

Ten en conta que marcar e desmarcar a caixa de verificación "activar Resaltado" tamén cambiará o estado das outras caixas de verificación da árbore en concordancia.
Polo tanto, se "Activar Resaltado" está desactivada e a marcas, as outras tres caixas de verificación tamén se marcarán automáticamente.
Se só queres resaltar o foco e deixar as caixas navegador de obxectos e modo Exploración desmarcadas, o estado da caixa de verificación "Activar Resaltado" será semi marcado.

##### Cortina de Pantalla {#VisionSettingsScreenCurtain}

Podes activar a [Cortina de Pantalla](#VisionScreenCurtain) marcando a caixa de verificación "por a pantalla en negro (efecto inmediato)".
Aparecerá unha advertencia de que a pantalla voltarase negra despois da activación.
Antes de continuar (selecionando "Si"), asegúrate de ter activados a voz e o braille e poderás controlar o teu computador sen usar a pantalla.
Seleciona "Non" se xa non desexas activar a Cortina de Pantalla.
Se estás seguro, podes escoller o botón Si para activar a Cortina de Pantalla.
Se xa non queres ver esta mensaxe de advertencia cada vez, podes cambiar este comportamento no diálogo que o amosa.
Sempre podes restaurar a advertencia marcando a caixa de verificación "Amosar sempre unha advertencia cando se cargue a Cortina de Pantalla" xunto á caixa de verificación "Por a pantalla en negro".

Por defecto, reprodúcense sons cando a Cortina de Pantalla se conmute.
Cando queiras cambiar este comportamento, podes desmarcar a caixa de verificación "Reproducir son ao conmutar a Cortina de Pantalla".

##### Opcións para Axudas Visuais de Terceiros {#VisionSettingsThirdPartyVisualAids}

Pódense proporcionar proveedores de mellora de visión adicionais en [complementos do NVDA](#AddonsManager).
Cando estos proveedores teñan opcións axustables, amosaranse nesta categoría de opcións en grupos separados.
Para obter máis información acerca da configuración de cada proveedor, por favor consulta a documentación dese proveedor.

#### Teclado {#KeyboardSettings}

<!-- KC:setting -->

##### Abrir opcións de Teclado {#toc181}

Tecla: `NVDA+control+k`

A categoría Teclado na caixa de diálogo Opcións do NVDA contén axustes que establecen o comportamento do NVDA cando usas e escrebes no teu teclado.
Esta categoría Opcións contén os seguintes axustes: 

##### Disposición do Teclado {#KeyboardSettingsLayout}

Esta caixa combinada permíteche escoller que tipo de distribución de teclado debería utilizar NVDA. Actualmente os dous que veñen co NVDA son Sobremesa e Portátil.

##### Selecionar Teclas Modificadoras do NVDA {#KeyboardSettingsModifiers}

As caixas de verificación nesta listaxe controlan que teclas poden usarse coma [teclas modificadoras do NVDA](#TheNVDAModifierKey). As seguintes teclas están disppoñibles para se escoller:

* A tecla bloqueo de maiúsculas
* A tecla insertar no tecládo numérico
* A tecla insertar extendida (atopada normalmente enriba das teclas de frecha, preto de inicio e fin)

Se non se escolle ningunha tecla como tecla de NVDA será imposible acceder a moitas ordes do NVDA, polo que se che requerirá que polo menos marques unha das modificadoras.

<!-- KC:setting -->

##### Falar caracteres ao se escrebir {#KeyboardSettingsSpeakTypedCharacters}

Tecla: NVDA+2

Cando está marcada significa que NVDA anunciará todos os caracteres segundo os escrebas no teclado. 

<!-- KC:setting -->

##### Falar palabras ao se escrebir {#KeyboardSettingsSpeakTypedWords}

Tecla: NVDA+3

Cando está marcada significa que NVDA anunciará todas as palabras ao se escrebir no teclado. 

##### Interrupción de Voz para Caracteres Escrebidos {#KeyboardSettingsSpeechInteruptForCharacters}

Se está activada, esta opción causará que a voz se interrumpa cada vez que se escreba un carácter. Esto está activado de maneira predeterminada.

##### Interrupción de Voz para a Tecla Intro {#KeyboardSettingsSpeechInteruptForEnter}

Se está activada, esta opción causará que a voz se interrumpa cada vez que se prema a tecla Intro. Esto está activado de maneira predeterminada.

##### Permitir lectura superficial en Falar Todo {#KeyboardSettingsSkimReading}

Se está activada, certas ordes de navegación (como a navegación rápida en modo navegación ou o movemento por liñas ou por parágrafos) non deteñen  Falar Todo, en cambio  Falar Todo salta  á nova posición e continúa a ler.

##### Pitar se se Teclean Letras Minúsculas Cando BloqMaius está Activado {#KeyboardSettingsBeepLowercase}

Cando está activada, escoitarase un pitido de aviso se se escrebe unha letra ca tecla shift mentres BloqMaius está activada.
Xeralmente, escrebir letras en maiúsculas co BloqMaius é inintencionado e normalmente é debido a non revisar que o BloqMaius estea activado.
Polo tanto, pode ser bastante útil seres avisado acerca de esto.

<!-- KC:setting -->

##### Falar teclas de ordes {#KeyboardSettingsSpeakCommandKeys}

Tecla: NVDA+4

Cando está marcada significa que NVDA anunciará todas as teclas que non sexan caracteres ao se escrebir no teclado. Esto inclúe combinacións de teclas como control más calquera outra letra. 

##### Reproducir son para Erros de Ortografía mentres se escrebe {#KeyboardSettingsAlertForSpellingErrors}

Ao habilitarse, reproducirase unha sinal acústica curta cando unha palabra que esteas escrebindo conteña un erro de ortografía.
Esta opción só está dispoñible se o anunciado de erros de ortografía está habilitado no diálogo de NVDA [Opcións de Formateado de Documento](#DocumentFormattingSettings), atopada na caixa de diálogo Opcións do NVDA.

##### Manexar teclas dende outras aplicacións {#KeyboardSettingsHandleKeys}

Esta opción permite ao usuario controlar se a pulsación das teclas xerada por aplicacións como teclados en pantalla e polo software de recoñecemento da fala debería procesarse polo NVDA. 
Esta opción está activada por defecto aínda que algúns usuarios poderían desexar deshabilitala, como aqueles que escreban en vietnamita co programa de escritura Unikey xa que fará que a entrada de caracteres sexa incorrecta.

#### Rato {#MouseSettings}

<!-- KC:setting -->

##### Abre as opcións do Rato {#toc194}

Tecla: `NVDA+control+m`

A categoría Rato da caixa de diálogo Opcións do NVDA permite ao NVDA realizar un seguemento do rato, reproducir pitidos das súas cordinadas  e configurar outras opcións de uso do rato.
Esta categoría contén os seguintes axustes:

##### Anunciar Cambios na Forma do Rato {#MouseSettingsShape}

Unha caixa de verificación, que cando se marca significa que NVDA anunciará a forma do punteiro do rato cada vez que cambie. 
O punteiro do rato no Windows cambia a súa forma para comunicar certa información tal como cando algo é editable, ou cando algo é cargable etc.

<!-- KC:setting -->

##### Habilitar Seguemento do Rato {#MouseSettingsTracking}

Tecla: NVDA+m |

Cando está marcada significa que NVDA anunciará o texto actualmente baixo o punteiro do rato, segundo se mova pola pantalla. Esto permíteche atopar cousas na pantalla, movendo físicamente o rato, en lugar de tratar de atopalas a través do navegador de obxectos.

##### Resolución de Unidade de Texto {#MouseSettingsTextUnit}

Se NVDA está configurado para anunciar o texto baixo o rato segundo se mova, esta opción permíteche escoller  exactamente canto texto será falado. 
As opcións son caracter, palabra, liña e parágrafo.

Para cambiar a unidade de resolución de texto dende calquera sitio, por favor asigna un xesto personalizado usando o [Diálogo Xestos de entrada](#InputGestures).

##### Anunciar obxecto cando o rato entre nel {#MouseSettingsRole}

Se esta caixa está marcada, o NVDA anunciará información sobre os obxectos según o rato se mova a eles.
Esto inclúe o rol (tipo) do obxecto así coma os estados (marcado/premedo), cordinadas de celda en táboas, etc.
Ten en conta que o anunciado de algúns detalles dos obxectos poderían depender de como outras opcións estean configuradas, como nas  categorías [presentación de obxectos](#ObjectPresentationSettings) ou [formateado de documentos](#DocumentFormattingSettings).

##### Reproducir audio cando se mova o rato {#MouseSettingsAudio}

Marcando esta caixa de verificación fas que o NVDA reproduza pitidos cando o rato se mova, así que o usuario poda resolver onde está o rato con respecto ás dimensións da pantalla.
Canto máis alto está o rato na pantalla, máis alto é o ton dos pitidos.
Canto máis estea situado o rato á esquerda ou á dereita  na pantalla, o son reproducirase máis á esquerda ou á dereita (asumindo que o usuario teña uns altavoces ou auriculares estéreo).

##### O Brilo controla o volume do audio {#MouseSettingsBrightness}

Se a caixa de verificación 'reproducir audio cando o rato se mova' está marcada, entón marcando esta caixa de verificación significa que o volume dos pitidos de audio está controlado por cómo o brilo da pantalla estea baixo o rato. 
Esto poderá causar algúns problemas de rendemento en Windows Vista, así que está desverificado de xeito predeterminado.

##### Ignorar a entrada do rato dende outras aplicacións {#MouseSettingsHandleMouseControl}

Esta opción permite ao usuario ignorar os eventos do rato (incluindo o movemento do rato e as pulsacións de botóns) xerados por outras aplicacións como TeamViewer e outros programas de control remoto.
Esta opción está desmarcada por defecto.
Se marcas esta opción e tes activada a opción "Habilitar seguemento do rato", o NVDA non anunciará o que hai por enbaixo do rato se este é movido por outra aplicación.

#### Interación Tactil {#TouchInteraction}

Esta categoría de opcións, só dispoñible en computadores con capacidades tactiles, permítenche configurar o xeito no que NVDA interactúa con pantallas tactiles.
Esta categoría contén as seguintes opcións:

##### Habilitar soporte de interacción táctil {#TouchSupportEnable}

Esta caixa de verificación habilita o soporte de interacción táctil do NVDA.
Se se habilita, podes usar os teus dedos para navegar e interactuar cos elementos na pantalla usando un dispositivo táctil.
Se se deshabilita, o soporte de pantalla táctil desactivarase coma se o NVDA non estivera funcionando.
Esta opción tamén pode conmutarse usando NVDA+control+alt+t. 

##### Modo de escritura tactil {#TouchTypingMode}

Esta caixa de verificación permíteche especificar o método que desexas usar ao introducir texto usando o teclado tactil.
Se esta caixa de verificación está marcada, cando localices unha tecla no teclado tactil, podes levantar o dedo e a tecla selecionada premerase.
Se está desmarcada, deberás tocar dúas veces a tecla na pantalla para premer a tecla.

#### Cursor de Revisión {#ReviewCursorSettings}

A categoría Cursor de Revisión na caixa de diálogo Opcións do NVDA úsase para configurar o comportamento do cursor de revisión do NVDA.
Esta categoría contén as seguintes opcións:

<!-- KC:setting -->

##### Seguir ao Foco Do sistema {#ReviewCursorFollowFocus}

Tecla: NVDA+7

Cando se activa, o cursor de revisión sempre se colocará no mesmo obxecto que o actual foco do sistema sempre que este cambie.

<!-- KC:setting -->

##### Seguir ao Cursor do Sistema {#ReviewCursorFollowCaret}

Tecla: NVDA+6

Cando se activa, o cursor de revisión moverase automáticamente á posición do cursor do Sistema cada vez que se mova.

##### Seguir ao Cursor do Rato {#ReviewCursorFollowMouse}

Cando se activa, o cursor de revisión seguirá ao rato segundo se mova.

##### Modo de Revisión Sinxelo {#ReviewCursorSimple}

Cando se activa, NVDA filtrará a xerarquía de obxectos que pode navegarse, para excluir calquer obxecto que non sexa do interese para o usuario; ex.: obxectos invisibles e obxectos utilizados só con propósitos de deseño.

Para conmutar o modo de revisión sinxela dende calquera lado, por favor asigna un Xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

#### Presentación de Obxectos {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Abrir as opcións de Presentación de Obxectos {#toc211}

Tecla: `NVDA+control+o`

A categoría Presentación de obxectos na caixa de diálogo Opcións do NVDA úsase para establecer a cantidade de información que o NVDA presentará sobre controis como descripción, información de posición, etc.
Estas opcións non acostuman a se aplicar ao modo exploración.
Estas opcións acostuman a se aplicar ao anunciado do foco e ao navegador de obxectos de NVDA, pero non á lectura de contido de texto, por exemplo, no modo exploración.

##### Anunciar Consellos {#ObjectPresentationReportToolTips}

Unha caixa de verificación que cando está marcada di ao NVDA que anuncie consellos segundo aparezan. 
Moitas ventás e controis amosan unha pequena mensaxe (ou consello) cando moves o punteiro do rato sobre eles, ou algunhas veces cando te moves co foco por eles.

##### Anunciar notificacións {#ObjectPresentationReportNotifications}

Esta caixa de verificación, cando está marcada, di ao NVDA que anuncie os globos de axuda e as notificacións segundo aparezan.

* Os globos de axuda son coma consellos, pero normalmente son de maior tamaño e están asociados con eventos do sistema como a desconexión dun cable de rede, ou tal vez para alertarte sobre problemas de seguridade de Windows.
* As notificacións se introducíronse en Windows 10 e aparecen no centro de notificacións na bandexa do sistema, informando sobre varios eventos (por exemplo: se se descargou unha actualización, apareceu un novo correo electrónico na túa bandexa de entrada, etc.).

##### Anunciar Teclas de Atallo dos Obxectos {#ObjectPresentationShortcutKeys}

Cando esta caixa de verificación está marcada, NVDA incluirá a tecla de atallo que estea asociada con certo obxecto ou control cando sexa anunciado. 
Por exemplo o menú Archivo nunha barra de menú poderá ter unha tecla de atallo alt+a.

##### Anunciar Información da Posición do Obxecto {#ObjectPresentationReportDescriptions}

Esta opción permíteche escoller onde desexas ter unha posición do obxecto anunciada (ex.: 1 de 4) cando te moves ao obxecto co foco ou o navegador de obxectos.

##### Deducir a información de Posición do Obxecto cando non estea dispoñible {#ObjectPresentationGuessPositionInfo}

Se o anunciado de información de posición do obxecto está desactivada, esta opción permite ao NVDA deducir a información de posición do obxecto cando non estea dispoñible para un control en particular.

Cando estea activada, NVDA anunciará información de posición para máis controis como menús e barras de ferramentas, non obstante esta información poderá ser lixeiramente incorrecta. 

##### Anunciar Descripcións de Obxectos {#ObjectPresentationReportDescriptions}

Desmarca esta caixa de verificación se coidas que non necesitas escoitar a descripción anunciada xunto cos obxectos (é dicir, suxerencias de búsqueda, anunciado de toda a ventá de diálogo xusto despois de que se abra o diálogo, etc.).

<!-- KC:setting -->

##### Saída nas Barras de Progreso {#ObjectPresentationProgressBarOutput}

Tecla: NVDA+u

Esta opción preséntaseche cunha caixa combinada que controla como nvda anuncia as actualizacións das barras de progreso. 

Ten as seguintes opcións:

* Desactivado: as barras de progreso non serán anunciadas segundo cambien.
* Falar: Esta opción di ao nvda que fale as barras de progreso en porcentaxes. Cada vez que a barra de progreso cambie, nvda falará o valor novo. 
* Pitar: Esto di ao nvda que pite cada vez que a barra de progreso cambie. Para un pitido máis alto, o compretado da barra de progreso está máis próximo
* Pitar e falar: Esta opción di ao nvda que pite e fale cando se actualiza unha barra de progreso.

##### Anunciar Barras de Progreso de fondo {#ObjectPresentationReportBackgroundProgressBars}

Esta é unha opción que, cando está marcada, di ao nvda que manteña o anunciado de unha barra de progreso, aínda se non está físicamente no primeiro plano. 
Se minimizas ou cambias a outra ventá que conteña unha barra de progreso, o nvda manterá a pista dela, permitíndoche facer outras cousas mentres nvda segue á barra de progreso.

<!-- KC:setting -->

##### Anunciar cambios de contido dinámico {#ObjectPresentationReportDynamicContent}

Tecla: NVDA+5

Conmuta o anunciado de contido novo en obxectos particulares como terminais e o control de histórico en programas de chat.

##### Reproducir un son ao aparecer autosuxerencias {#ObjectPresentationSuggestionSounds}

Conmuta o anunciado da aparición de autosuxerencias, e se está habilitado, NVDA reproducirá un son para indicar esto.
As autosuxerencias son listas de entradas suxeridas baseadas en texto introducido en certos campos de edición e documentos.
por exempro, cando introduzas texto na caixa de procura no menú inicio en Windows Vista e posterior, Windows amosa unha lista de suxerencias baseadas no que escribiches.
Para algúns campos de edición  coma campos de procura en varias aplicacións de Windows 10, NVDA pode notificarte que apareceu unha lista de suxerencias ao se escrebir texto.
A lista de autosuxerencias pecharase unha vez te movas polo campo de edición, e para algúns campos, NVDA pode notificarte de esto cando elo ocorra.

#### Composición de Entrada {#InputCompositionSettings}

A categoría Composición de Entrada permíteche controlar cómo anuncia NVDA a entrada de Caracteres Asiáticos, como co IME ou métodos de Servizo de entrada de texto .
Ten en conta que debido ao feito de que os métodos de entrada varían en grande medida polas súas características dispoñibles e por cómo transmiten a información, o máis probable será que sexa necesario configurar estas opcións de xeito diferencial para cada método de entrada para obter a experiencia de escritura máis eficiente.

##### Anunciar Automáticamente todas as Candidatas Dispoñibles {#InputCompositionReportAllCandidates}

Esta opción, que está activada de xeito predeterminado, permíteche escoller se todas as candidatas visibles deberían anunciarse automáticamente cando apareza unha lista de candidatas ou a súa páxina cambie.
Ter esta opción activada para métodos de entrada pictográfica como chinese Novo ChangJie ou Boshiami, é útil pois podes escoitar todos os símbolos automáticamente e os seus números e podes escoller un inmediatamente.
Sen embargo, para os métodos de entrada fonéticos como chinese Novo Fonético, Podería ser mais útil desactivar esta opción xa que todos os símbolos soarán igual e terás que utilizar as teclas de cursor para navegar polos elementos da lista individualmente para obter mais información da descripción de caracteres para cada candidata.

##### Anunciar Candidato Seleccionado {#InputCompositionAnnounceSelectedCandidate}

Esta Opción, que está activada por omisión, permíteche escoller se o NVDA debería anunciar o candidato seleccionado cando aparece unha lista de candidatos ou cando a selección se cambiou.
Para os métodos de entrada onde a selección se pode cambiar cas teclas de frechas (como Chinese Nova Fonética) esto é necesario, pero para algúns métodos de entrada podería ser máis eficiente teclear con esta opción desactivada.
Ten en conta que aínda con esta opción desactivada, o cursor de revisión aínda se colocará sobor do candidato seleccionado permitíndoche utilizar a navegación de obxectos para revisar manualmente para ler este ou outros candidatos.

##### Incluir sempre descripcións curtas de caracteres para os candidatos {#InputCompositionCandidateIncludesShortCharacterDescription}

Esta Opción, que está activada por omisión, permíteche escoller se NVDA debería proporcionar ou non unha descripción curta para cada carácter nun candidato, ou cando se seleccioe ou cando se lea automáticamente cando apareza a lista de candidatos.
Ten en conta que para localizacións como Chinese, o anunciado de descripcións extra de caracteres para o candidato seleccionado non está afectado por esta opción.
Esta opción podería seren útil para os métodos de entrada Coreano e xaponés.

##### Anunciar Cambios para a Cadea de Lectura {#InputCompositionReadingStringChanges}

Algúns métodos de entrada como Chinese Novo Fonético e Novo ChangJie teñen unha cadea de lectura (coñecida ás veces como unha cadea de precomposición).
Podes escoller se o NVDA debería anunciar caracteres novos ao seren tecleados nesta cadea de lectura con esta opción.
Esta opción está activada de xeito predeterminado.
Ten en conta que algúns métodos de entrada antigos como Chinese ChangJie poderían non utilizar a cadea de lectura para conter os caracteres de precomposición, no seu lugar utilizar a cadea de composición directamente. Por favor mira a seguinte opción para configurar o anunciado da cadea de composición.

##### Anunciar Cambios á cadea de composición {#InputCompositionCompositionStringChanges}

Despois de que a lectura ou os datos de precomposición foran combinados dentro dun símbolo pictográfico válido, a maioría dos métodos de entrada colocan este símbolo dentro dunha cadea de composición para un almacenamento temporal xunto con outros símbolos combinados antes de que finalmente se inserten dentro do documento.
Esta Opción permíteche escoller se o NVDA debería anunciar ou non símbolos novos segundo aparezan na cadea de composición.
Esta opción está activada por omisión.

#### Modo Exploración {#BrowseModeSettings}

<!-- KC:setting -->

##### Abrir as opcións de modo Exploración {#toc229}

Tecla: `NVDA+control+b`

A categoría Modo Exploración na caixa de diálogo Opcións do NVDA úsase para configurar o comportamento do NVDA ao ler e navegar por documentos comprexos coma páxinas web.
Esta categoría contén as seguintes opcións:

##### Máximo Número de Caracteres nunha Liña {#BrowseModeSettingsMaxLength}

Este campo pon a anchura máxima dunha liña do modo navegación (en caracteres).

##### Máximo número de Liñas por Páxina {#BrowseModeSettingsPageLines}

Este campo axusta a cantidade de liñas que moverás cando premas Avance de páxina ou Retroceso de páxina mentres esteas no modo navegación.

<!-- KC:setting -->

##### Utilizar deseño de pantalla {#BrowseModeSettingsScreenLayout}

Tecla: NVDA+v

Esta opción permítech especificar se o modo exploración debería colocar o contido no que se pode facer clic (ligazóns, botóns e campos) na súa propria liña, ou se debería mantelo no fluxo de texto tal coma se amosa visualmente.
Ten en conta que esta opción non se aplica ás aplicacións de Microsoft Office, coma Outlook e Word, que sempre usan o deseño de pantalla.
Cando o deseño de pantalla está activado, os elementos da páxina manteranse tal como se amosan visualmente.
Por exemplo, unha liña visual de múltiples ligazóns presentarase en voz e braille como múltiples ligazóns na mesma liña.
Se se desactiva, os elementos da páxina colocaranse nas súas proprias liñas.
Esto pode seren máis sinxelo de entender durante a navegación da páxina liña por liña, e pode facer que os elementos sexan máis sinxelos de interactuar para algúns usuarios.

##### Habilitar modo Exploración ao cargar Páxina {#BrowseModeSettingsEnableOnPageLoad}

Esta caixa de verificación conmuta se se debería habilitar automáticamente o modo exploración ao cargar unha páxina.
Cando esta opción estea deshabilitada, o modo exploración aínda pode activarse manualmente en páxinas ou en documentos onde se admita o modo exploración.
Consulta a [Seción modo Exploración](#BrowseMode) para unha listaxe das aplicacións admitidas polo modo Exploración.
Ten en conta que esta opción non se aplica a situacións onde o modo exploración sexa sempre opcional, por exemplo, en Microsoft Word.
Esta opción está habilitada por defecto.

##### Falar Todo Automáticamente ao Cargar a Páxina {#BrowseModeSettingsAutoSayAll}

Esta caixa de verificación conmuta a fala automática dunha páxina despois de cargala en modo navegación.
Esta opción está activada por defecto.

##### Incluir Táboas de Deseño {#BrowseModeSettingsIncludeLayoutTables}

Esta opción afecta a cómo NVDA manella as tablas utilizadas exclusivamente con fins de deseño.
Cando está activada, NVDA trátaas como táboas normais, anunciándoas basándose nas [Opcións de Formato de Documento](#DocumentFormattingSettings) e localizándoas coas ordes de navegación rápida.
Cando está desactivada, non se anuncian nin se atopan coa navegación rápida.
Sen embargo, o contido das táboas aínda se incluirá como texto normal.
Esta opción está desactivada de xeito predeterminado.

Para conmutar a inclusión de táboas de deseño dende calquera lugar, por favor asigna un xesto personalizado usando o diálogo [Xestos de entrada](#InputGestures).

##### Configurar o anunciado de campos como ligas e cabeceiras {#BrowseModeLinksAndHeadings}

Por favor consulta as opcións na  [categoría Formateado de Documentos](#DocumentFormattingSettings) do diálogo [Opcións do NVDA](#NVDASettings) para configurar os campos que se anuncian cando se navega, coma ligas, cabeceiras e táboas.

##### Modo de foco automático para cambios do foco {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Esta opción permite ao modo foco chamarse se o foco cambia. 
Por exemplo, cando estás nunha páxina web, se premes tab e caes sobre un formulario, se esta opción está verificada, o modo foco chamaráse automáticamente.

##### Modo foco automático para movemento do cursor {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Esta opción, cando está marcada, permite ao NVDA entrar en e abandoar o modo foco cando se utilizan as frechas. 
Por exemplo, se se vai premendo frecha abaixo por unha páxina web e caes sobre unha caixa de edición, NVDA activará automáticamente o modo foco. 
Se premes as frechas para saír da caixa de edición, NVDA voltaráche a poñer no modo Navegación.

##### Indicación de Audio dos modos Foco e Navegación {#BrowseModeSettingsPassThroughAudioIndication}

Se esta opción está activada, NVDA reproducirá sons especiales cando cambie entre modo Navegación e modo foco, en lugar de falar o cambio.

##### Capturar os Xestos que non Sexan de Ordes  para que non Alcancen o  Documento {#BrowseModeSettingsTrapNonCommandGestures}

Habilitada de modo predeterminado, esta opción permíteche escoller se os xestos (como a pulsación de teclas) que non sexan unha orde do NVDA e que non se considere que sexa unha tecla de orde en xeral, deberían capturarse para non pasar ao documento que estea no foco actualmente. 
Como un exemplo, ao estar activada, se se premeu a letra j, debería capturarse para non alcanzar o documento, xa que non é nin unha tecla de navegación rápida nin é probable que sexa unha orde da mesma aplicación.
Neste caso, o NVDA pedirá a Windows que reproduza un son predeterminado cada vez que se prema unha tecla que quede atrapada.

<!-- KC:setting -->

##### Poñer o Foco do Sistema Automáticamente nos Elementos Enfocables {#BrowseModeSettingsAutoFocusFocusableElements}

Tecla: NVDA+8

Desactivada por defecto, esta opción permíteche escoller se o foco do sistema debería poñerse automáticamente en elementos que podan ter o foco do sistema (ligas, campos de formulario, etc.) ao navegar por contidos co cursor do modo Exploración.
Deixando esta opción deshabilitada non se enfocarán automáticamente os elementos enfocables  cando se selecionen co cursor do modo Exploración.
Esto podería dar coma resultado unha experiencia de navegación máis rápida e unha mellor resposta no modo Exploración.
O foco aínda se actualizará no elemento en particular cando se interactúe con el (ex.: premendo un botón ou marcando unha caixa de verificación).
Habilitar esta opción pode mellorar o soporte para algúns sitios web a costa do rendemento e da estabilidade.

#### Formateado de Documento {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Abrir as opcións de Formateado de Documento {#toc243}

Tecla: `NVDA+control+d`

A maioría das caixas de verificación neste diálogo son para configurar que tipo de formato desexas escoitar automáticamente cando movas o cursor polos documentos. 
Por Exemplo, se verificas a caixa de verificación anunciar o nome da fonte, cada vez que navegues polo texto cunha fonte diferente, o nome da fonte serache anunciado.

As opcións de formateado de documento organízanse en grupos.
Podes configurar o anunciado de:

* Fonte
  * Nome de fonte
  * Tamano de fonte
  * Atributos de fonte
  * Superíndices e subíndices
  * Énfase
  * Resaltado (texto marcado)
  * Estilo
  * Cores
* Información de documento
  * Comentarios
  * marcas
  * Revisións do editor
  * Erros de ortografía
* Páxinas e espaciado
  * Números de páxina
  * Números de liña
  * Anunciado de sangría de liña [(Desactivado, voz, Tons, voz e tons)](#DocumentFormattingSettingsLineIndentation)
  * Sangría de parágrafo (ex.: sangría, sangría de primeira liña)
  * Ignorar liñas en branco para anunciado de sangría de liña
  * Espaciado de liña (simple, doble etc)
  * Alineamento
* Información de táboa
  * Táboas
  * Cabeceiras de fila/columna (desactivado, filas, Columnas, filas e columnas)
  * Coordenadas de celda
  * Bordes de celdas (desactivado, Estilos, Ambos Colores e Estilos)
* Elementos
  * Cabeceiras
  * Ligazóns
  * Gráficos
  * Listaxes
  * Citas
  * Grupos
  * Rexións
  * Artigos
  * Marcos
  * Figuras e pes de foto
  * Admite clic

Para conmutar estas  opcións dende calquera lugar, por favor asigna xestos persoalizados utilizando o [diálogo Xestos de Entrada](#InputGestures).

##### Anunciar cambios de formato despois do cursor {#DocumentFormattingDetectFormatAfterCursor}

Se está activada, esta opción di ao NVDA que probe e detecte todos os cambios de formato nunha liña segundo a anuncie, se se fai esto podería enlentecerse a resposta do NVDA.

De xeito predeterminado, NVDA detectará o formato na posición do cursor do Sistema / Revisión, e en algúns casos podería detectar o formato no resto da liña, só se non está causando un decremento da resposta.

Activa esta opción mentres comprobas a lectura de documentos en aplicacións coma Worpad, onde o formato sexa importante.

##### Anunciado de sangría de liñas {#DocumentFormattingSettingsLineIndentation}

Esta opción permíteche configurar cómo debe lerse a sangría do comezo das liñas.
A caixa combinada Anunciar sangría de liñas con ten catro opcións.

* Desactivado: NVDA non tratará a sangría especialmente.
* Voz: se se seleciona voz, cando a cantidade de sangrado cambie, NVDA falará algo como "doce espazos" ou "catro tabuladores."
* Tons: se se seleciona Tons, cando a cantidade de sangrado cambie, os tons indican a cantidade de cambios na sangría.
O ton incrementarase en intensidade para cada espazo, e para o tabulador,incrementarase en intensidade equivalente de 4 espazos.
* Voz e Tons: esta opción le a sangría usando ambo-los dous métodos de máis arriba.

Se marcas a caixa de verificación "Ignorar liñas en branco para anunciado de sangría de liña", entón non se anunciarán os cambios de sangría nas liñas en branco.
Esto pode ser útil ao ler un documento no que as liñas en branco se usen para separar bloques de texto con sangría, coma no código fonte de programación.

#### Navegación de Documento {#DocumentNavigation}

Esta categoría permíteche axustar varios aspectos da navegación de documento.

##### Estilo de Parágrafo {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminado (manexado pola aplicación), Manexado pola aplicación, salto de unha única liña, salto multiliña|
| Predeterminado |Manexado pola aplicación|

Esta caixa combinada permíteche selecionar o estilo de parágrafo a usar cando se navegue por parágrafos con `control+frecha arriba` e `control+frecha abaixo`.
Os estilos de parágrafo dispoñibles son:

* Manexado pola aplicación: O NVDA permitirá á aplicación determinar o parágrafo anterior ou posterior, e o NVDA lerá o parágrafo novo ao navegar.
Este estilo funciona mellor cando a aplicación admite a navegación por parágrafos nativamente, e é o predeterminado.
* Salto de unha única liña: O NVDA tentará determinar o parágrafo anterior e posterior usando o salto de unha única liña coma indicador de parágrafo.
Este estilo funciona mellor cando se lean documentos nunha aplicación que non admita a navegación de parágrafos nativamente, e os parágrafos márcanse no documento cunha única pulsación da tecla `intro`.
* Salto multiliña: O NVDA tentará determinar o parágrafo anterior e posterior usando polo menos unha liña en branco (dúas pulsacións da tecla `intro`) coma indicador de parágrafo.
Este estilo funciona mellor cando se traballe con documentos que usen bloques de parágrafos.
Ten en conta que este estilo de parágrafo non pode usarse en Microsoft Word ou Microsoft Outlook, a menos que esteas usando UIA para acesar a controis de Microsoft Word.

Podes cambiar entre os estilos de parágrafo dispoñibles dende calquera lugar asignando unha tecla no [diálogo Xestos de Entrada](#InputGestures).

#### Opcións do OCR de Windows {#Win10OcrSettings}

As opcións nesta categoría permítenche configurar [o OCR de Windows](#Win10Ocr).
Esta categoría contén as seguintes opcións:

##### Lingua de Recoñecemento {#Win10OcrSettingsRecognitionLanguage}

Esta caixa combinada permíteche escoller a lingua para usar co recoñecemento de texto.
Para percorrer as linguas dispoñibles dende calquera sitio, por favor asigna un xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

##### Refrescado periódico de contido recoñecido {#Win10OcrSettingsAutoRefresh}

Cando esta caixa estea habilitada, o NVDA refrescará automáticamente o contido recoñecido cando un resultado dun recoñecemento teña o foco.
Esto pode ser moi útil cando queiras monitorizar contido que cambia constantemente, coma cando ves un vídeo con subtítulos.
O refrescado ocorre cada segundo e medio.
Esta opción está deshabilitada por defecto.

#### Opcións Avanzadas {#AdvancedSettings}

¡Advertencia! As opcións nesta categoría son para usuarios avanzados e poden causar que o NVDA non funcione correctamente se se configura de xeito incorrecto.
Realiza cambios nestas opcións únicamente se estás seguro de que sabes o que estás a facer ou se recibiches as instrucións específicas dun desenvolvedor do NVDA.

##### Facer cambios a opcións avanzadas {#AdvancedSettingsMakingChanges}

Para realizar cambios nas Opcións Avanzadas, os controis deben estar habilitados confirmando coa caixa de verificación, que entendes os resgos de modificar estas opcións.

##### Reestablecer as opcións predeterminadas {#AdvancedSettingsRestoringDefaults}

O botón reestablece os valores predeterminados para as opcións, incluso se a caixa de confirmación non está marcada.
Despois de cambiar as opcións é posible que desexes voltar aos valores predeterminados.
Este tamén pode ser o caso se non estás seguro de que se cambiaran as opcións.

##### Habilitar a carga de código persoalizado dende o directorio Developer Scratchpad {#AdvancedSettingsEnableScratchpad}

Ao desenvolver complementos para o NVDA, é útil poder probar o código a medida que o escrebes.
Esta opción cando está habilitada, permite ao NVDA cargar appModules persoalizados, Plugins globais, controladores de pantallas braille, controladores de sintetizadores e proporcionadores de melloras visuais, dende un directorio especial de desenvolvedores scratchpad do teu directorio de configuración de usuario do NVDA.
Ao igual que os seus equivalentes en complementos, estos módulos cárganse ao arrancar o NVDA ou, no caso de appModules e de Plugins globais, ao [se recargar plugins](#ReloadPlugins).
Esta opción está desactivada de xeito predeterminado, o que garante que nunca se execute ningún código non probado no NVDA sen o coñecemento explícito do usuario.
Se desexas distribuir código persoalizado a outros, debes empaquetalo coma un complemento de NVDA.

##### Abrir o directorio Developer Scratchpad {#AdvancedSettingsOpenScratchpadDir}

Este botón abre o directorio onde podes colocar o código persoalizado mentres o desenvolves.
Este botón só está habilitado se o NVDA está configurado para permitir a carga de código persoalizado dende o directorio de desenvolvedores do Scratchpad.

##### Rexistro para eventos UI Automation e cambios de propiedade {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Automático, Selectivo, Global|
| Por defecto |Automático|

Esta opción cambia o xeito no que o NVDA rexistra os eventos lanzados pola API de accesibilidade Microsoft UI Automation.
A caixa combinada Rexistro para eventos UI Automation e cambios de propiedade ten tres opcións:

* Automático: "selectivo" en Windows 11 Sun Valley 2 (versión 22H2) e posteriores, pola contra "global".
* Selectivo: o NVDA limitará o rexistro de eventos ao foco do sistema para a maioría dos eventos.
Se sofres problemas de rendemento nunha ou máis aplicacións, recomendámosche que probes esta funcionalidade para ver se o rendemento mellora.
Polo tanto, en versións vellas de Windows, o NVDA pode ter  problemas en seguer ao foco nalgúns controis (coma o administrador de tarefas e o panel de emoji).
* Global: o NVDA rexistra moitos eventos UIA que se procesan e se descartan dentro do mesmo NVDA.
Aíndaque o seguemento do foco é máis fiable en máis situacións, o rendemento degrádase significativamente, especialmente en aplicacións como Microsoft Visual Studio.

##### Usar UI automation para aceder a controis de documento de Microsoft Word {#MSWordUIA}

Configura se o NVDA debería usar ou non a API de acesibilidade UI Automation para aceder a documentos de Microsoft Word, en lugar do vello modelo de obxectos de Microsoft Word.
Esto aplícase aos documentos no mesmo Microsoft word, ademáis das mensaxes en Microsoft Outlook.
Esta opción contén os seguintes valores:

* Por defecto (cando sexa adecuado)
* Só cando sexa necesario: cando o modelo de obxectos de Microsoft Word non estea dispoñible en absoluto
* Cando sexa adecuado: Microsoft Word version 16.0.15000 ou posteriores, ou cando non estea dispoñible o modelo de obxectos de Microsoft Word
* Sempre: cando a UI automation estea dispoñible en Microsoft word (sen importar cómo de compreta sexa).

##### Usar UI automation para acesar a controis en follas de cálculo de Microsoft  Excel cando estea dispoñible {#UseUiaForExcel}

Cando esta opción está activada, o NVDA tentará usar a API de accesibilidade Microsoft UI Automation  para obter información dos controis das follas de cálculo de Microsoft Excel.
Esta é unha funcionalidade experimental e algunhas caraterísticas de Microsoft Excel poden non estaren dispoñibles neste modo.
Por exemplo, as características da Listaxe de Elementos do NVDA para enumerar fórmulas e comentarios e a tecla rápida de navegación do modo Explorarción saltar campos de formulario nunha folla de cálculo non están dispoñibles.
Sen embargo, para a navegación e edición básica das follas de cálculo, esta opción pode proporcionar unha grande mellora de rendemento.
Aínda non recomendamos que a maioría dos usuarios activen esta opción por defecto, aíndaque invitamos aos usuarios de Microsoft Excel  compilación 16.0.13522.10000 ou superior a que proben esta función e nos den a súa opinión.
A implementación de UI automation de Microsoft Excel cambia constantemente e é posible que as versións de Microsoft Office anteriores á 16.0.13522.10000 podan non expoñer suficiente información para que esta opción sexa útil.

##### Usar proceso mellorado de eventos {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminada (Habilitada), Deshabilitada, Habilitada|
| Predeterminada |Habilitada|

Cando esta opción está habilitada, o NVDA debería seguir respondento cando se lle inunda con moitos eventos UI Automation, ex.: grandes cantidades de texto nunha terminal.
Despois de cambiar esta opción, necesitarás reiniciar o NVDA para que o cambio teña efecto.

##### Soporte para Consola de Windows {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Automático, UIA cando estea dispoñible, herdado|
| Predeterminado |Automático|

Esta opción seleciona coma o NVDA interactúa coa Consola de Windows usada polo símbolo do sistema, polo PowerShell e polo subsistema de Windows para Linux.
Non afecta á Terminal moderna de Windows.
En Windows 10 versión 1709, Microsoft [engadiu soporte para a súa API UI Automation á consola](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), dando un rendemento e unha estabilidade moi mellorados para lectores de pantalla que o admitan.
En situacións nas que UI Automation non estea dispoñible ou que se sepa que a experiencia de usuario sexa inferior, o soporte da consola herdada do NVDA está dispoñible como alternativa.
A caixa combinada Soporte para a Consola de Windows ten tres opcións:

* Automático: usa UI Automation na versión da Consola de Windows incluída con Windows 11 versión 22H2 e posterior.
Esta opción recoméndase e é a predeterminada.
* UIA cando estea dispoñible: usa UI Automation en consolas se está dispoñible, incluso para versións con implementacións incompletas ou con erros.
Aíndaque esta funcionalidade limitada pode seren útil (e incluso suficiente para o teu uso), a utilización desta opción é totalmente baixo o teu proprio resgo e non se proporcionará soporte para ela.
* Herdado: UI Automation na Consola de Windows deshabilitarase compretamente.
O sistema herdado usarase sempre incluso en situacións nas que UI Automation proporcionaría unha experiencia de usuario superior.
Polo tanto, selecionar esta opción non é recomendable ao menos que sepas o que estás a facer.

##### Utilizar UIA con Microsoft Edge e outros navegadores baseados en Chromium cando estea dispoñible {#ChromiumUIA}

Permite especificar que se utilizará UIA cando estea dispoñible en navegadores baseados en Chromium como Microsoft Edge.
O soporte UIA para os navegadores baseados en Chromium está nunha fase primitiva de desenvolvemento e pode que non ofreza o mesmo nivel de aceso que IA2.
A caixa combinada ten as seguintes opcións:

* Por defecto (Só cando é necesario): o valor por defecto do NVDA, actualmente é "Só cando sexa necesario". Este valor por defecto pode cambiar no futuro a medida que a tecnoloxía madureza.
* Só cando sexa necesario: cando o NVDA non poda inxectar no proceso do navegador para usar IA2 e UIA estea dispoñible, entón o NVDA voltará a usar UIA.
* Sí: se o navegador fai acesible a UIA, o NVDA usaráo.
* Non: non usa UIA, incluso se o NVDA non pode inxectar no proceso. Esto pode seren útil para os desenvolvedores que depuren problemas con IA2 e queren asegurarse de que o NVDA non volte a usar UIA.

##### Anotacións {#Annotations}

Este grupo de opcións úsanse para habilitar as características que engaden soporte experimental para as anotacións ARIA.
Algunhas destas características poden estar incompretas.

<!-- KC:beginInclude -->
Para "Anunciar resumo de calquera anotación de detalles no cursor do sistema", preme NVDA+d.
<!-- KC:endInclude -->

Existen as seguintes opcións: 

* "Anunciar 'ten detalles' para anotacións estructuradas ": habilita o anunciado se o texto ou o control ten máis detalles.
* "Informar sempre de aria-description":
  Cando a fonte de `accDescription` é aria-description, anúnciase a descripción.
  Esto é útil para as anotacións na web.
  Nota:
 * Hai moitas fontes para `accDescription` varias teñen unha semántica mixta ou puoco fiable.
   Históricamente AT non foi quen de diferenciar as fontes de `accDescription` típicamente non se falaba debido á semántica mixta.
 * Esta opción está nun desenvolvemento moi primitivo, baséase nas características do navegador que aínda non están ampliamente dispoñibles.
 * Espérase que funcione con Chromium 92.0.4479.0+

##### Anunciar rexións activas {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Deshabilitado, Habilitado|
| Predeterminado |Habilitado|

Esta opción seleciona se o NVDA anuncia cambios nalgúns contidos web dinámicos en Braille.
Deshabilitar esta opción equivale ao comportamento do NVDA en versións 2023.1 e anteriores, que só anunciaban estos cambios de contenidos en voz.

##### Falar contrasinais en todas as terminais melloradas {#AdvancedSettingsWinConsoleSpeakPasswords}

Esta opción controla se se falan os caracteres mediante [falar caracteres ao se escreber](#KeyboardSettingsSpeakTypedCharacters) ou [falar palabras ao se escreber](#KeyboardSettingsSpeakTypedWords) en situacións onde a pantalla non se actualiza (como a entrada de contrasinais) nalgúns programas de terminal, como a consola de Windows co soporte para UI automation habilitado e Mintty.
Por motivos de seguridade, esta opción debería permanecer desactivada.
Sen embargo, é posible que desexes habilitala se experimentas problemas de rendemento ou inestabilidade co anunciado de caracteres ou palabras escrebidas na consola ou se traballas en entornos de confianza e prefires o anunciado de contrasinais.

##### Usar o soporte de caracteres ao escreber mellorado na Consola de Windows herdada cando estea dispoñible {#AdvancedSettingsKeyboardSupportInLegacy}

Esta opción habilita un método alternativo para detectar caracteres escrebidos nas Consolas de Windows herdadas.
Aíndaque mellora o rendemento e evita que se especifique a saída da consola, pode ser incompatible con algúns programas de terminal.
Esta característica está dispoñible e activada por omisión en versións de Windows 10 1607 ou posteriores cando UI Automation non estea dispoñible ou desactivado.
Advertencia: con esta opción activada, os caracteres escrebidos que non aparezan en pantalla, como contrasinais, non se suprimirán.
En entornos non confiables, poderás desactivar temporalmente [falar caracteres ao se escrebir](#KeyboardSettingsSpeakTypedCharacters) e [falar palabras ao se escrebir](#KeyboardSettingsSpeakTypedWords) ao introducir contrasinais.

##### Algoritmo Diff {#DiffAlgo}

Esta opción controla o xeito no que o NVDA determina o novo texto para falar en terminais.
A caixa combinada do algoritmo diff ten tres opcións:

* Automático: esta opción fai que o NVDA prefira Diff Match Patch na maioría das situatións, pero volta a Difflib en aplicacións problemáticas, coma versións vellas da Consola de Windows e Mintty.
* Diff Match Patch: esta opción fai que o NVDA calcule cambios no texto da terminal por caracteres, incluso en situacións onde non sexa recomendable.
Pode mellorar o rendemento cando se escriban grandes volúmenes de texto na consola e permite un anunciado máis preciso dos cambios realizados no medio das liñas.
Sen embargo, nalgunhas aplicacións, a lectura de texto novo pode ser entrecortada ou inconsistente.
* Difflib: esta opción fai que o NVDA calcule os cambios no texto da terminal por liñas, incluso en situacións onde non sexa recomendable.
É idéntico ao comportamento do NVDA na versión 2020.4 e anteriores.
Esta opción pode estabilizar a lectura do texto entrante nalgunhas aplicacións.
Sen embargo, nas terminais, ao insertar ou borrar un carácter no medio dunha liña, lerase o texto despois do cursor.

##### Falar texto novo na Terminal de Windows {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Difusión, notificacións UIA|
| Predeterminado |Difusión|

Esta opción seleciona como determina o NVDA que texto é "novo" (e que falar cando "anunciar cambios de contido dinámico" estea habilitado) na Terminal de Windows e no control WPF da Terminal de Windows utilizado en Visual Studio 2022.
Non afecta á Consola de Windows (`conhost.exe`).
A caixa combinada falar texto novo na Terminal de Windows ten tres opcións:

* Predeterminado: esta opción actualmente equivale a "difusión", pero prevese que cambie unha vez que se desenvolva máis a compatibilidade coas notificacións UIA.
* Difusión: esta opción usa o algoritmo diff selecionado para calcular os cambios cada vez que a terminal amose o novo texto.
Esto é idéntico ao comportamento do NVDA nas versións 2022.4 e anteriores.
* Notificacións UIA: esta opción desvía a responsabilidade de determinar que texto falar á propria Terminal de Windows, o que significa que o NVDA xa non ten que determinar que texto é actualmente "novo" en pantalla.
Esto debería mellorar notablemente o rendemento e a estabilidade da Terminal de Windows, pero esta función aínda non está compreta.
En particular, os caracteres escrebidos que non se amosen en pantalla, coma as contrasinais, anúncianse cando esta opción estea selecionada.
Ademáis, é posible que os tramos contiguos de saída de máis de 1000 caracteres non se anuncien con exactitude.

##### Tentar cancelar voz para eventos de foco caducados {#CancelExpiredFocusSpeech}

Esta opción habilita o comportamento que tenta cancelar a voz para eventos de foco caducados.
En particular moverse rápidamente polas mensaxes  en Gmail con Chrome pode facer que o NVDA fale información obsoleta.
Esta funcionalidade está predeterminada a partires do NVDA 2021.1.

##### Tempo de espera para o movemento do cursor (en MS) {#AdvancedSettingsCaretMoveTimeout}

Esta opción permíteche configurar o número de milésimas de segundo que o NVDA esperará a que o cursor (punto de inserción) se mova nos controis de texto editables.
Se ves que o NVDA semella estar seguindo incorrectamente o cursor, por exemplo, parece estar sempre un carácter por detrás ou repetindo liñas, entón podes tentar aumentar este valor.

##### Anunciar transparencia das cores {#ReportTransparentColors}

Esta opción permite anunciar cando as cores son transparentes, útil para os desenvolvedores de complementos e módulos de aplicación que reúnen información para mellorar a experiencia do usuario cunha aplicación de terceiros.
Algunhas aplicacións GDI resaltan o texto cunha cor de fondo, o NVDA (a través do modelo de visualización) tenta informar desta cor.
Nalgunhas situacións, o fondo do texto pode ser compretamente transparente, co texto en capas sobre algún outro elemento da GUI.
Con varias APIs de GUI históricamente populares, o texto pode seren renderizado cun fondo transparente, pero visualmente a cor de fondo é precisa.

##### Usar WASAPI para a saída de audio {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
| Opcións |Predeterminada (habilitada), Deshabilitada, Habilitada|
| predeterminada |Habilitada|

Esta opción habilita a saída de audio a través da API Windows Audio Session (WASAPI).
WASAPI é un framework de audio máis moderno que pode mellorar a resposta, o rendemento e a estabilidade da saída de audio do NVDA, incluíndo a voz e os sons.
Despois de cambiar esta opción, necesitarás reiniciar o NVDA para que o cambio teña efecto.
Deshabilitar WASAPI desactivará as seguintes opcións:

* [O volume dos sons do NVDA segue ao volume da voz](#SoundVolumeFollowsVoice)
* [Volume dos sons do NVDA](#SoundVolume)

##### Categorías de rexistro de depuración {#AdvancedSettingsDebugLoggingCategories}

As caixas de verificación desta listaxe permíteche habilitar categorías específicas de mensaxes de depuración no rexistro do NVDA.
O rexistro destas mensaxes pode incurrir nun menor rendemento e en arquivos de rexistro de gran tamaño.
Activa só un deles se un desenvolvedor do NVDA che dou instrucións específicas, por exemplo, ao depurar por que un controlador de pantalla braille non está funcionando correctamente.

##### Reproducir un son para os erros rexistrados {#PlayErrorSound}

Esta opción permite especificar se o NVDA reproducirá un son de erro en caso de que se rexistre un erro.
Escollendo Só en versións de proba (por defecto) fai que o NVDA reproduza sons de erro só se a versión actual do NVDA é unha versión de proba (alfa, beta ou executada dende o código fonte).
Escollendo Si permite habilitar os sons de erro calquera que sexa a versión actual do NVDA.

##### Expresión regular para ordes de navegación rápida de parágrafos de texto {#TextParagraphRegexEdit}

Este campo permite aos usuarios persoalizar a expresión regular para detectar parágrafos  de texto en modo exploración.
A [orde de navegación de parágrafos de texto](#TextNavigationCommand) procura parágrafos emparellados por esta expresión regular.

### Miscelánea de Opcións {#MiscSettings}

Ademáis da caixa de diálogo [Opcións do NVDA](#NVDASettings), o submenú Preferencias do menú NVDA contén outros elementos que se describen a continuación.

#### Diccionarios da Fala {#SpeechDictionaries}

O menú de Diccionarios da fala, (atopado no menú Preferencias) contén diálogos que che permiten controlar o modo no que NVDA pronuncia palabras ou frases particulares. 
Hai actualmente tres tipos diferentes de diccionarios da fala. 
son:

* Predeterminado: as regras neste diccionario afectan a todas as voces no NVDA.
* Voz: un diccionario cuias regras afectan á voz para o sintetizador que actualmente estea sendo utilizado.
* Temporal: as regras neste diccionario afectan a todas as voces en NVDA, pero só para a sesión actual. Estas regras son temporales e perderanse se NVDA é reiniciado

Necesitas asignar xestos persoalizados utilizando o [diálogo Xestos de Entrada](#InputGestures) se desexas abrir calqera destos diálogos de diccionario dende calquera lugar.

Todos os diálogos de diccionario conteñen unha lista de regras que serán utilizadas para procesar a voz. 
O diálogo tamén contén os botóns Engadir, Editar, borrar e Borrar todo.

Para engadir unha nova regra ao diccionario, preme o botón Engadir, e recubre os campos da caixa de diálogo que aparezan e entón preme Aceptar. 
Entón verás a túa nova regra na lista de regras. 
Asimismo para asegurarte de que a túa regra está actualmente gardada, asegúrate de premer Aceptar para saír completamente do diálogo de diccionario Unha vez finalizaras de engadir/editar regras.

As regras para os diccionarios de voz de NVDA permítenche cambiar unha cadena de caracteres por outra. 
Un exemplo simple sería que quixeras ter a NVDA dicindo a palabra ra cada vez que tivera que dicir a palabra paxaro. 
No diálogo de engadir regra, o modo máis sinxelo de facer esto é teclear a palabra paxaro no campo Patrón, e a palabra ra no campo de reemprazar. 
poderías tamén querer teclear unha descripción da regra no campo Comentario (algo como: cambiar paxaro por ra).

Os diccionarios da fala de NVDA asimesmo son moito máis poderosos que un sinxelo reemplazo de palabras. 
O diálogo de Engadir regras tamén contén Unha caixa de verificación que di se queres ou non que a regra sexa sensible ás maiúsculas (significando que NVDA debería ter en conta se os caracteres están en maiúsculas ou en minúsculas. 
NVDA ignora os casos de xeito predeterminado). 

Finalmente, un conxunto de botóns de opción permítenche dicir ao NVDA se o teu patrón debería compararse con calquera cousa, ou só debería compararse se é unha palabra completa ou se debería tratarse como unha "Expresión Regular".
Axustar o patrón para comparar como unha palabra completa significa que o reemplazo só se fará se o patrón non ocurre como parte dunha palabra máis longa.
Esta condición cómprese se os caracteres inmediatamente anteriores ou posteriores á palabra son calquera outra cousa que unha letra, un número, ou un guión baixo, ou se non hai ningún carácter.
Polo tanto, utilizando o exemplo anterior da sustitución da palabra "paxaro" con "ran", se foras  facer desto un reemplazo de palabra completa, non se compararía "paxaros" ou "paxaroAzul".

Unha expresión regular é un patrón que contén símbolos especiais que che permiten emparellar máis de un caracter ao mesmo tempo, ou emparellar so números, ou so letras, segundo uns poucos exemplos. 
As expresións regulares non están cubertas nesta Guía do Usuario.
Para un titorial introductorio, por favor consulta a [Guía de Expresións regulares de Python](https://docs.python.org/3.11/howto/regex.html).

#### Pronunciación de puntuación/símbolos {#SymbolPronunciation}

Este diálogo permíteche cambiar o modo no que se pronuncian a puntuación e outros símbolos, así como o nivel dos símbolos no que se falan. 

A lingua cuia pronuncia de símbolo vai a seren editada amosarase No título do diálogo.
Ten en conta que este diálogo respeta a opción "Confiar na lingua da voz ao se procesar símbolos e caracteres" que se atopa na [Categoría Voz](#SpeechSettings) do diálogo [Opcións do NVDA](#NVDASettings) é dicir, usa a lingua da voz en lugar da opción da lingua global do NVDA cando esta opción estea habilitada.

Para cambiar un símbolo, primeiro selecciónao na lísta de Símbolos.
Podes filtrar os símbolos introducindo o símbolo ou unha parte da súa sustitución no cuadro de edición Filtrar por.

* O campo Reemprazar permíteche cambiar o texto que debería falarse en lugar deste símbolo.
Tamén podes axustar o nivel a carácter; neste caso o símbolo non se falará independentemente do nivel de símbolo en uso, coas seguintes dúas excepcións:
 * Ao navegar por caracteres.
 * Cando o NVDA estea a deletrear calquera texto que conteña ese símbolo.
* Utilizando o campo Nivel, podes axustar o nivel máis baixo do símbolo ao que este símbolo se debería falar (non, algún, a maioría ou todos).
* O campo Enviar símbolo actual ao sintetizador especifica cando o proprio símbolo (en contraposición co seu reemplazamento) debería enviarse ao sintetizador.
Esto é útil se o símbolo causa que o sintetizador faga unha pausa ou cambie a entoación da voz.
Por exemplo, unha coma causa que o sintetizador faga unha pausa.
Hai tres opcións:
  * nunca: nunca envía o símbolo actual ao sintetizador.
  * Sempre: envía sempre o símbolo actual ao sintetizador.
  * só baixo nivel dos símbolos: Envía o símbolo actual só se o nivel de voz do símbolo configurado é máis baixo que o nivel posto por este símbolo.
Por exemplo, poderías utilizar esto tal que un símbolo terá o seu reemplazamento falado en niveis máis altos sen pausar, mentres aínda estea indicado cunha pausa nos niveis máis baixos.

Podes engadir símbolos novos premendo o botón Engadir.
No diálogo que apareza, introduce o símbolo e preme o botón Aceptar.
Entón, cambia os campos para o símbolo novo como o farías para outros símbolos.

Podes eliminar un símbolo que engadiches anteriormente premendo o botón Eliminar.

Cando remates, preme o botón Aceptar para gardar os teus cambios ou o botón Cancelar para descartalos.

No caso de símbolos comprexos, o campo Reemprazar pode ter que incluir algunhas referencias de grupo do texto coincidente. Por exemplo, para un patrón que coincida cunha data compreta, \1, \2, e \3 tería que aparecer no campo, para seren reemprazado polas partes correspondentes da data.
Polo tanto, as barras inversas normais no campo Reemprazar deberían duplicarse, por exemplo, "a\\b" debería escribirse para obter o reemprazo "a\b".

#### Xestos de Entrada {#InputGestures}

En este diálogo, podes persoalizar os xestos de entrada (teclas no teclado, botóns na pantalla braille, etc.) para ordes de NVDA.

Só se amosan as ordes que se apliquen inmediatamente antes de que o diálogo se abra.
Por exemplo, se queres persoalizar ordes relacionadas co modo navegación, deberías abrir o diálogo Xestos de entrada mentres esteas no modo navegación.

A árbore nesta caixa de diálogo amosa todas as ordes do NVDA aplicables agrupadas por categoría.
Podes filtralos introducindo unha ou máis palabras dende o nome das ordes dentro da caixa de edición Filtrar por... en calquera orde.
Calquer xesto asociado cunha orde lístase baixo a orde.

Para engadir un xesto de entrada a unha orde, selecciona a orde e preme o botón Engadir.
A continuación, fai o xesto de entrada que desexes asociar, por exemplo, preme unha tecla do teclado ou un botón nunha pantalla Braille.
De cotío, un xesto pode interpretarse de máis dunha maneira.
Por exemplo, se premeches unha tecla no teclado, pode que desexes que sexa específica para a distribución de teclado actual (por exemplo, de escritorio ou portátil) ou pode que desexes que se aplique a todas as distribucións.
Neste caso, aparecerá un menú que che permite seleccionar a opción desexada.

Para borrar un xesto de unha orde, selecciona o xesto e preme o botón Eliminar.

A categoría Teclas do Sistema de Teclado Emuladas contén ordes do NVDA que emulan teclas do teclado do sistema.
Estas teclas emuladas do teclado do sistema poden usarse para controlar un teclado do sistema directamente dende a túa pantalla braille.
Para engadir un xesto de entrada emulado, seleciona a categoría Teclas do Sistema de Teclado Emuladas e preme o botón Engadir.
Entón, preme a tecla no teclado que desexes emular.
Despois deso, a tecla estará dispoñible dende a categoría Teclas do Sistema de Teclado Emuladas e poderás asignarlle un xesto de entrada según se descrebeu anteriormente.

Notas:

* As teclas asignadas deben ter xestos asignados para persistir cando se garden ou se peche o diálogo.
* Un xesto de entrada con teclas modificadoras pode non seren capaz de mapearse a un xesto emulado sen teclas modificadoras.
Por exemplo, configurar a entrada emulada 'a' e configurar un xesto de entrada de 'ctrl+m', pode resultar
en que a aplicación reciba un 'ctrl+a'.

Cando teñas rematado de facer cambios, preme o botón Aceptar para gardalos ou o botón Cancelar para descartalos.

### Gardar e Recargar a configuración {#SavingAndReloading}

De xeito predeterminado NVDA gardará automáticamente as túas opcións ao saír.
Ten en conta, non obstante, que esta opción predeterminada pode ser cambiada baixo as opcións xerais no menú preferencias. 
Para gardar as opcións manualmente en calquera ocasión, escolle o elemento Gardar configuración no menú NVDA.

Se te trucas coas túas opcións e necesitas voltar ás opcións gardadas, podes escoller o elemento "voltar á configuración gardada" no menú NVDA.
Tamén podes reiniciar as túas opcións aos seus valores predeterminados de fábrica orixinais escollendo Reiniciar Configuración aos Valores Predeterminados de Fábrica, que tamén se atopa no menú NVDA.

As seguintes teclas de ordes de NVDA tamén son útiles:
<!-- KC:beginInclude -->

| Nome |Tecla Sobremesa |Tecla Portátil |Descripción|
|---|---|---|---|
|Gardar configuración |NVDA+control+c |NVDA+control+c |Garda a túa configuración actual tal que non se perda cando saias do NVDA|
|Reverter configuración |NVDA+control+r |NVDA+control+r |Premendo unha vez reinicia a túa configuración a cando a gardaches por derradeira vez. Premendo tres veces reiniciaráa ós valores predeterminados de fábrica.|

<!-- KC:endInclude -->

### Perfiles de Configuración {#ConfigurationProfiles}

Ás veces, é posible que desexes ter diferentes configuracións para diferentes situacións.
Por exemplo, é posible que desexes ter o anunciado de sangría habilitado mentres estás editando ou o anunciado dos atributos da fonte activado mentres estás correxindo.
O NVDA permíteche facer esto utilizando perfiles de configuración.

Un perfil de configuración contén só as opcións que se cambian mentres que o perfil estea a ser editado.
A maioría das opcións pódense cambiar nos perfís de configuración con excepción de aquelas que estean na categoría Xeral da caixa de diálogo [Opcións do NVDA #NVDASettings, as que se aplican á totalidade do NVDA.

Os perfís de configuración pódense activar manualmente, sexa dende unha caixa de diálogo ou usando xestos engadidos persoalizados.
Tamén se poden activar de forma automática debido aos disparadores como o cambio a unha aplicación en particular.

#### Manexo Básico {#ProfilesBasicManagement}

Manexas os perfís de configuración seleccionando "Perfís de Configuración" no menú NVDA.
Tamén podes facer esto utilizando unha orde de teclado:
<!-- KC:beginInclude -->

* NVDA+control+p: Amosa a caixa de diálogo Perfiles de configuración.

<!-- KC:endInclude -->

O primeiro control de este diálogo é a lista de perfís na que se pode seleccionar un dos perfís dispoñibles.
Cando abras o diálogo, selecciónase o perfil que esteas a editar actualmente.
Tamén se amosa información adicional para perfís activos, indicando se se activaron manualmente, se se dispararon e/ou se están sendo editados.

Para cambiar o nome dun perfil ou eliminalo, preme os botóns Renomear ou Eliminar, respectivamente.

Preme o botón Pechar para pechar o diálogo.

#### Crear un Perfil {#ProfilesCreating}

Para crear un perfil, preme o botón Novo.

Na caixa de diálogo Novo perfil, podes introducir un nome para o perfil.
Taménn podes selecionar cómo se debe usar este perfil.
Se só desexas utilizar este perfil manualmente, selecciona Activación manual, que é o valor predeterminado.
Pola contra, selecciona o disparador que debería activar automáticamente este perfil.
Para maior comodidade, se non se introducíu un nome para o perfil, ao seleccionar un disparador rechearáse un nome en consecuencia.
Mira [máis abaixo](#ConfigProfileTriggers) para máis información acerca dos disparadores.

Premendo Aceptar crearase o perfil e pecharase a caixa de diálogo de configuración de perfiles para que podas editalo.

#### Activación Manual {#ConfigProfileManual}

Podes activar manualmente un perfil seleccioanndo un perfil e premendo o botón Activación Manual.
Unha vez activado, aínda se poden activar outros perfiles debido aos disparadores, pero as opcións do perfil activado manualmente teñen prioridade.
Por exemplo, se un perfil se dispara para a aplicación actual e o anunciado de ligas está activado nese perfil, pero desactivado no perfil activado manualmente, as ligas non se anunciarán.
Sen embargo, se cambiaches a voz no perfil disparado, pero nunca se cambióu no perfil activado manualmente, utilizarase a voz a partires do perfil disparado.
Os valores que se modifiquen gardaranse no perfil activado manualmente.
Para desactivar un perfil activado manualmente, selecciónao na caixa de diálogo Perfiles de configuración e preme o botón desactivar Manual.

#### Disparadores {#ConfigProfileTriggers}

Ao premer o botón de Disparadores na caixa de diálogo Perfiles de configuración permíteche cambiar os perfiles que deben ser activados automáticamente por diversos disparadores.

A lista de disparadores amosa os disparadores dispoñibles, que son os seguintes:

* Aplicación actual: dispárase cando se cambie á aplicación actual.
* Falar todo: dispárase durante a lectura coa orde falarr Todo.

Para cambiar o perfil que debe ser activado automáticamente por un disparador, selecciona o disparador e logo selecciona o perfil desexado na lista de perfís.
Podes seleccionar (configuración normal) se non queres utilizar un perfil.

Preme o botón pechar para voltar á caixa de diálogo de perfiles de configuración.

#### Editar un Perfil {#ConfigProfileEditing}

Se activaches manualmente un perfil, as opcións que modifiques gardaranse nese perfil.
Pola contra, as opcións que se modifiquen gardaranse no perfil disparado máis recentemente.
Por exemplo, se asociaches un perfil ca aplicación Bloc de notas e cambias ao Bloc de notas, as opcións modificadas gardaranse nese perfil.
Por último, se non hai nin un perfil activado manualmente nin un disparado, as opcións que se modifiquen gardaranse na configuración normal.

Para editar o perfil asociado a falar todo, debes [activar manualmente](#ConfigProfileManual) ese perfil.

#### Deshabilitar Temporalmente Disparadores {#ConfigProfileDisablingTriggers}

Ás veces, é útil desactivar temporalmente todos os disparadores.
Por exemplo, poderías desexar editar un perfil activado manualmente ou a configuración normal, sen perfiles disparadores interfirindo.
Podes facer esto marcando a caixa de verificación Desactivar Temporalmente Todos os Disparadores na caixa de diálogo  de perfís de configuración.

Para activar ou desactivar os disparadores dende calquera sitio, por favor asigna un xesto personalizado usando o [Diálogo Xestos de Entrada](#InputGestures).

#### Activar un perfil usando xestos de entrada {#ConfigProfileGestures}

Para cada perfil que engadas, poderás asignar un ou máis xestos de entrada para activalo.
Por defecto, os perfís de configuración non teñen xestos de entrada asignados.
Podes engadir xestos para activar un perfil usando o [diálogo Xestos de Entrada](#InputGestures).
Cada perfil ten a súa propria entrada na categoría perfís de configuración.
Cando renomees un perfil, calquera xesto que engadiras con anterioridade aínda estará dispoñible.
Borrar un perfil eliminará automáticamente o xesto asociado con él.

### Ubicación dos Ficheiros de Configuración {#LocationOfConfigurationFiles}

As versións portátiles do NVDA almacenan todas as súas opcións e complementos nun directorio chamado userConfig, que se atopa no directorio de NVDA.

As versións instaladas do NVDA almacenan todas as súas opcións e complementos nun directorio especial de NVDA localizado no teu perfil de usuario de Windows. 
Esto significa que cada usuario no sistema pode ter as súas proprias opcións de NVDA. 
Para abrir o teu directorio de configuracións dende calquer sitio podes usar [o diálogo Xestos de Entrada](#InputGestures) para engadir un xesto persoalizado.
Ademáis nunha versión instalada do NVDA, no menú Inicio podes ir a programas -> NVDA -> explorar directorio de configuración do usuario.

As opcións para NVDA cando se executa durante o inicio de sesión ou no UAC almacénanse no directorio SystemConfig no directorio de instalación do NVDA.
Normalmente esta configuración non debería ser tocada.
Para cambiar como se configura o NVDA durante o inicio de sesión ou nas pantallas UAC, configura ao NVDA como desexes mentres iniciaches sesión en Windows, garda a configuración e logo preme o botón "Usar axustes gardados actualmente durante o inicio de sesión e en pantallas seguras na categoría Xeral do diálogo [Opcións do NVDA](#NVDASettings) .

## Complementos e a Tenda de Complementos {#AddonsManager}

Os complementos son paquetes de software que proporcionan funcionalidade nova ou modificada para o NVDA.
Desenvólvense pola comunidade de NVDA e por organizacións externas coma vendedores comerciais.
Os complementos poden facer o que segue:

* Engadir ou mellorar o soporte para certas aplicacións.
* Proporcionar soporte para pantallas braille ou para sintetizadores de voz adicionais.
* Engadir ou cambiar características ao NVDA.

A tenda de complementos de NVDA permíteche procurar e xestionar paquetes de complementos.
Todos os complementos dispoñibles na Tenda poden descargarse de valde.
Sen embargo, algúns deles poden requerir dos usuarios que paguen unha licenza ou software adicional antes de poder utilizalos.
Os sintetizadores de voz comerciais son un exemplo deste tipo de complementos.
Se instalas un complemento con compoñentes de pago e cambias de opinión sobre o seu uso, o complemento pode borrarse doadamente.

Acédese á Tenda de Complementos dende o submenú Ferramentas do menú de NVDA.
Para aceder á Tenda de Complementos dende calquera lugar, asigna un xesto persoalizado usando o [diálogo Xestos de Entrada](#InputGestures).

### Navegar polos Complementos {#AddonStoreBrowsing}

Cando se abre, a Tenda de Complementos amosa unha listaxe de complementos.
Se non instalaches ningún complemento antes, a Tenda de Complementos abrirase cunha listaxe dos dispoñibles para instalar.
Se instalaches complementos, a listaxe amosará os instalados actualmente.

Selecionar un complemento desprazándote coas frechas arriba e abaixo, amosará os detalles para el.
Os complementos teñen accións asociadas ás que se pode aceder a través dun [menú de accións](#AddonStoreActions), como instalar, axuda, deshabilitar e borrar.
As accións dispoñibles cambiarán en función de se o complemento está instalado ou non, e de se está habilitado ou deshabilitado.

#### Vistas de Listaxe de Complementos {#AddonStoreFilterStatus}

Hai diferentes vistas para os complementos: instalados, actualizables, dispoñibles e incompatibles.
Para cambiar a vista dos complementos, cambia a pestana activa da listaxe de complementos usando `ctrl+tab`.
Tamén podes premer `tab` ate a listaxe de vistas e desprazarte por ela coa `frecha esquerda` e `frecha dereita`.

#### Filtrar por complementos habilitados e deshabilitados {#AddonStoreFilterEnabled}

Normalmente, un complemento instalado está "habilitado", o que significa que se está executando e que está dispoñible no NVDA.
Sen embargo, algúns dos complementos instalados poden estar en estado"deshabilitado".
Esto significa que non serán usados, e que as súas funcións non estarán dispoñibles durante a sesión actual de NVDA.
Podes ter deshabilitado un complemento debido a que entraba en confricto con outro, ou con certa aplicación.
O NVDA tamén pode deshabilitar certos complementos se se descobre que son incompatibles durante unha actualización do programa; aíndaque avisaráseche se esto fora a ocorrer.
Os complementos tamén poden deshabilitarse se só non os necesitas durante un período longo, pero non queres desinstalalos porque esperas voltar a necesitalos no futuro.

As listaxes de complementos instalados e incompatibles poden filtrarse polo seu estado de habilitación ou deshabilitación.
Por defecto amósanse tanto os complementos habilitados como os deshabilitados.

#### Incluir complementos incompatibles {#AddonStoreFilterIncompatible}

Os complementos dispoñibles e actualizables poden filtrarse para incluir [complementos incompatibles](#incompatibleAddonsManager) que están dispoñibles para instalar.

#### Filtrar complementos por canle {#AddonStoreFilterChannel}

Os complementos pódense distribuir por ate catro canles:

* Estable: o desenvolvedor publicouno coma complemento probado cunha versión lanzada do NVDA.
* Beta: Este complemento podería necesitar máis probas, pero libérase para que os usuarios podan dar a súa retroalimentación.
Suxerido para usuarios entusiastas.
* Dev: esta canle está suxerida para que os desenvolvedores o usen para probar cambios na API non publicados aínda.
Os probadores alpha de NVDA poden necesitar usar as versións "Dev" dos seus complementos.
* Externo: complementos instalados dende fontes externas, fora da Tenda de Complementos.

Para enumerar complementos só para canles específicas, cambia a seleción do filtro de "Canle".

#### Procurar complementos {#AddonStoreFilterSearch}

Para procurar complementos, usa a caixa de texto "Procurar".
Podes aceder a ela premendo `shift+tab` dende a listaxe de complementos, ou premendo `alt+p` dende calquera lugar na interface da Tenda de Complementos.
Escribe unha ou dúas palabras chave para 	o tipo de complemento que buscas e logo volta á listaxe.
Os complementos listaranse se o texto buscado pode atoparse no ID do complemento, no nome amosado, no editor, no autor ou na descripción.

### Accións do complemento {#AddonStoreActions}

Os complementos teñen accións asociadas como instalar, axuda, deshabilitar e borrar.
Para un complemento na listaxe de complementos, pódese aceder a estas accións a través dun menú que se abre premendo a tecla `aplicacións`, `intro`, clic dereito ou dobre clic.
Este menú tamén pode ser acesado a través dun botón Accións nos detalles do complemento selecionado.

#### Instalar complementos {#AddonStoreInstalling}

O feito de que un complemento estea dispoñible na Tenda de Complementos de NVDA non significa que fora aprobado por NV Access nin por ninguén.
É moi importante que só instales complementos de fontes nas que confíes.
A funcionalidade dos complementos non ten restricións dentro do NVDA. 
Esto podería incluir o aceso aos teus datos persoais ou incluso a todo o sistema.

Podes instalar e actualizar complementos [navegando polos complementos dispoñibles](#AddonStoreBrowsing).
Seleciona unha das pestanas "Complementos dispoñibles" ou "Complementos actualizables".
Logo usa a acción actualizar, instalar ou remprazar para comezar a instalación.

Tamén podes instalar varios complementos de unha soa vez.
Esto pode facerse selecionando varios complementos na pestana Complementos dispoibles, logo activando o menú de contexto sobre a seleción e escollendo a ación "Instalar complementos selecionados".

Para instalar un complemento que obtiveras fora da Tenda de complementos, preme o botón "Instalar dende unha fonte externa".
Esto permitirache buscar un paquete de complementos (ficheiro `.nvda-addon`) nalgún lugar do teu computador ou da rede.
Unha vez que abras o paquete de complementos, comezará o proceso de instalación.

Se o NVDA está instalado e executándose no teu sistema, tamén podes abrir un ficheiro de complemento directamente dende o navegador ou dende o sistema de arquivos para comezar o proceso de instalación.

Cando se instala un complemento dende unha fonte externa, o NVDA pedirache que confirmes a instalación.
Unha vez que o complemento estea instalado, o NVDA debe reiniciarse para que comece a funcionar, aíndaque podes pospor o reinicio se tes outros para instalar ou para actualizar.

#### Borrar Complementos {#AddonStoreRemoving}

Para borrar un complemento, seleciónao da listaxe e usa a Acción Borrar.
O NVDA pedirache que confirmes o borrado.
Ao igual que coa instalación, o NVDA debe reiniciarse para que o complemento se borre compretamente.
Ate que o fagas, amosarase un estado "Pendente de borrado" para ese complemento na listaxe.
Ao igual que coa instalación, tamén podes eliminar varios complementos á vez.

#### Deshabilitar e Habilitar Complementos {#AddonStoreDisablingEnabling}

Para deshabilitar un complemento, usa a acción "deshabilitar".
Para habilitar un complemento anteriormente deshabilitado, ussa a acción "habilitar".
Podes deshabilitar un complemento se o seu estado indica que está "habilitado", ou habilitalo se o complemento está "deshabilitado".
Para cada uso da acción habilitar/deshabilitar, o estado do complemento cambia para indicar qué sucederá cando o NVDA se reinicie.
Se o complemento estaba anteriormente "deshabilitado", o estado amosará "habilitado despois de reiniciar".
Se o complemento estaba anteriormente "habilitado", o estado amosará "deshabilitado despois de reiniciar".
Ao igual que cando instalas ou borras complementos, necesitas reiniciar o NVDA para que os cambios teñan efecto.
Tamén podes habilitar ou deshabilitar varios complementos á vez seleccionando varios complementos na pestana Complementos dispoñibles, logo activando o menú de contexto sobre a seleción e escollendo a acción apropriada.

#### Reseñar complementos e ler as reseñas {#AddonStoreReviews}

Antes de instalar un complemento, podes querer ler reseñas doutros.
Tamén, pode ser útil que outros usuarios teñan retroalimentación sobre os complementos que probaras.
Para ler reseñas dun complemento, seleciona un dende as pestanas Complementos Dispoñibles ou Actualizables e usa a acción "Reseñas da comunidade".
Esto liga a unha páxina web de discusión en GitHub, onde poderás ler e escrebir reseñas para o complemento.
Ten en conta que esto non substitúe a comunicación directa cos desenvolvedores de complementos.
A cambio, o propósito desta característica é compartir retroalimentación para axudar aos usuarios que decidan se un complemento pode serlles útil.

### Complementos Incompatibles {#incompatibleAddonsManager}

Algúns complementos antigos poden non seren compatibles coa versión de NVDA que teñas.
Se estás usando unha versión antiga de NVDA, algúns complementos modernos poden non seren compatibles tampouco.
Ao tentar instalar un complemento incompatible aparecerá unha mensaxe de erro explicando por qué o complemento considérase incompatible.

Para complementos máis antigos, podes anular a incompatibilidade baixo a túa propria responsabilidade.
Os complementos incompatibles poden non funcionar coa túa versión de NVDA, e poden provocar un comportamento inestable ou inesperado incluíndo o colgue.
Podes anular a compatibilidade ao activar ou instalar un complemento.
Se o complemento incompatible provoca problemas máis tarde, podes deshabilitalo ou borralo.

Se tes problemas executando  NVDA, e actualizaches ou instalaches recentemente un complemento, especialmente se é un incompatible, podes tentar executar o NVDA temporalmente con todos os complementos deshabilitados.
Para reiniciar o NVDA con todos os complementos deshabilitados, escolle a opción apropriada ao saír do programa.
Alternativamente, usa a [opción de liña de ordes](#CommandLineOptions) `--disable-addons`.

Podes examinar os complementos incompatibles dispoñibles usando a [pestana complementos dispoñibles e actualizables](#AddonStoreFilterStatus).
Podes examinar os complementos incompatibles instalados usando a [pestana complementos incompatibles](#AddonStoreFilterStatus).

## Ferramentas Extra {#ExtraTools}
### Visualizador do Rexistro {#LogViewer}

O visualizador do rexistro, que se atopa en Ferramentas no menú NVDA, permíteche ver a saída de rexistro que ocorreu hdende que a última sesión de NVDA se iniciou.

Ademáis de ler o contido, tamén podes Gardar unha copia do ficheiro do rexistro, ou refrescar o visualizador que cargue nova saída de rexistro xerada despois de que o Visualizador do rexistro fora aberto.
Estas acións están dispoñibles no menú Rexistro no visualizador do rexistro.

O ficheiro que se amosa cando abres o visualizador do rexistro gárdase no teu computador na localización de ficheiro `%temp%\nvda.log`.
Créase un novo ficheiro de rexistro cada vez que o NVDA se inicia.
Cando esto ocorre, o ficheiro de rexistro da sesión anterior do NVDA móvese a `%temp%\nvda-old.log`.

Tamén podes copiar un fragmento  do ficheiro de rexistro actual ao portapapeis sen abrir o visualizador do rexistro.
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Abrir Visualizador de rexistro |`NVDA+f1` |Abre o visualizador do rexistro e amosa información de desenvolvemento sobre o actual navegador de obxectos.|
|Copiar un fragmento do rexistro ao portapapeis |`NVDA+control+shift+f1` |Cando se preme esta orde unha vez, establece un punto de inicio para o contido do rexistro que vai ser capturado. Cando se preme unha segunda vez, cópiase o contido do rexistro dende o punto de inicio ao portapapeis.|

<!-- KC:endInclude -->

### Visualizador de Voz {#SpeechViewer}

Para desenroladores de Software videntes ou xente demostrando NVDA a unha audiencia vidente, está dispoñible unha ventá flotante que che permite ver todo o texto que NVDA estea falando actualmente.

Para activar o visualizador de voz, marca o elemento de menú "Visualizador de Voz" baixo Ferramentas no menú NVDA.
Desmarca o elemento de menú para desactivalo.

A ventá do visualizador de voz contén unha caixa de verificación etiquetada "Amosar visualizador de voz ao arrancar".
Se esta está marcada, o visualizador de voz abrirase cando NVDA arranque.
A ventá do visualizador de voz sempre tentará reabrirse coas mesmas dimensións e localización que cando se pechou.

Mentres o visualizador de voz estea activado, actualízase constantemente para amosarche o texto máis recente que está a ser falado.
Non obstante, se pasas o rato por enriba ou colocas o foco dentro do visualizador,  NVDA deterá temporalmente a actualización do texto, tal que poderás seleccionar ou copiar sinxelamente o contido existente.

Para conmutar o visualizador de voz dende calquera lugar, por favor asigna un xesto persoalizado utilizando o [diálogo Xestos de Entrada](#InputGestures).

### Visualizador Braille {#BrailleViewer}

Para os desenvolvedores de software videntes ou as persoas que fagan demostracións do NVDA para audiencias con visión, hai dispoñible unha ventá frotante que lles permite ver a saída braille e o texto equivalente para cada carácter braille.
O Visualizador Braille pode usarse ao mesmo tempo que unha pantalla braille física, o que coincidirá co número de celdas do dispositivo físico.
Mentres o Visualizador Braille estea activado, actualízase constantemente para amosarche o braille que se amosaría na pantalla Braille física.

Para activar o Visualizador Braille, marca o elemento de menú "Visualizador Braille" en Ferramentas no menú NVDA.
Desmarca o elemento de menú para desactivalo.

As pantallas braille físicas soen ter botóns para desprazarse cara adiante ou cara atrás, para activar el desprazamento coa ferramenta Visualizador Braille usa o [diálogo Xestos de Entrada](#InputGestures) para asignar atallos de teclado que "Desprace a pantalla braille atrás" e "Desprace a pantalla braille adiante"

A ventá do Visualizador Braille contén unha caixa de verificación etiquetada "Amosar Visualizador de Braille ao comezar".
Se esta opción está marcada, o Visualizador Braille abrirase cando se inicie o NVDA.
A ventá do Visualizador Braille sempre tentará voltar a abrirse coas mesmas dimensións e colocación que cando se pechou.

A ventá do Visualizador Braille contén unha caixa de verificación etiquetada coma "Desprazar para enrutamento de celda", por omisión está desmarcada.
Se se marca, pasar o rato sobre unha celda braille activará unha orde "enrutar a celda braille" para esa celda.
De cotío úsase esto para mover o cursor ou activar a acción dun control.
Esto pode ser útil para comprobar que o NVDA sexa capaz de revertir correctamente o mapa dunha celda braille.
Para evitar o enrutamento involuntario ás celdas, a orde ten un retraso.
O rato debe sobrevoar ata que a celda se volte verde.
A celda comezará cunha cor marela crara, pasará a ser laranxa, e de repente convertirase en verde.

Para conmutar o visualizador braille dende calquera parte, por favor asigna un xesto persoalizado usando o [diálogo Xestos de entrada](#InputGestures).

### Consola de Python {#PythonConsole}

A consola de Python do NVDA, atopada baixo Ferramentas no menú NVDA, é unha ferramenta de desenvolvemento que é útil para depuración, inspección xeral do interior  do NVDA ou inspeción da xerarquía de accesibilidade de unha aplicación.
Para máis información, por favor olla a Guía do desenvolvedor dispoñible na [sección de desenvolvemento da páxina web do NVDA](https://community.nvda-project.org/wiki/Development).

### Tenda de Complementos {#toc306}

Esto abrirá a [Tenda de Complementos de NVDA](#AddonsManager).
Para máis información, le o capítulo en profundidade: [Complementos e a Tenda de Complementos](#AddonsManager).

### Crear copia portable {#CreatePortableCopy}

Esto abrirá un diálogo que che permite crear unha copia portable do NVDA a partires da versión instalada.
De calquer xeito, ao executar unha copia portable do NVDA, no submenú Ferramentas extra o elemento de menú chamarase "instalar NVDA neste PC" en lugar de "crear copia portable).

O diálogo para crear unha copia portable do NVDA ou para instalar NVDA neste PC indicarache para selecionar unha ruta do cartafol na que debería crear a copia portable ou na que o NVDA debería instalarse.

Neste diálogo podes habilitar ou deshabilitar o seguinte:

* Copiar a configuración actual do usuario (esto inclúe os ficheiros en %appdata%\roaming\NVDA ou na configuración do usuario da túa copia portable e tamén inclúe os complementos e outros módulos)
* Arrancar a nova copia portable despois da creación ou arrancar o NVDA despois da instalación (inicia o NVDA automáticamente despois da creación da copia portable ou da instalación)

### Executar a ferramenta COM registration fixing... {#RunCOMRegistrationFixingTool}

A instalación ou desinstalación de programas nunha computadora pode, en certos casos, producir que os ficheiros COM DLL non se rexistren.
Dado que as COM Interfaces como IAccessible dependen dos rexistros correctos de COM DLL, poden aparecer problemas en caso de que falte o rexistro correcto.

Esto pode suceder, por exemplo, despois de instalar e desinstalar Adobe Reader, Math Player e outros programas.

O rexistro faltante pode causar problemas nos navegadores, aplicacións de escritorio, barra de tarefas e outras interfaces.

Específicamente, os seguintes problemas poden resolverse executando esta ferramenta:

* O NVDA anuncia "descoñecido" ao navegar con navegadores coma Firefox, Thunderbird etc.
* O NVDA falla ao cambiar entre modo foco e modo exploración
* O NVDA é moi lento ao navegar cos navegadores mentres se usa o modo exploración
* E posiblemente outros fallos.

### Recargar plugins {#ReloadPlugins}

Este elemento, unha vez activado, recarga app modules e plugins globais sen reiniciar ao NVDA, o cal é útil para desenvolvedores.
Os App modules xestionan como o NVDA interactúa coas aplicacións específicas.
Os plugins globais xestionan como o NVDA interactúa con todas as aplicacións.

As seguintes teclas de ordes de NVDA tamén poden ser útiles:
<!-- KC:beginInclude -->

| Nome |Tecla |Descripción|
|---|---|---|
|Recargar plugins |`NVDA+control+f3` |Recarga os plugins globais e os app modules do NVDA.|
|Anunciar o app module cargado e o executable |`NVDA+control+f1` |Anuncia o nome do app module, se o hai, e o nome do executable asociado coa aplicación que ten o foco do teclado.|

<!-- KC:endInclude -->

## Sintetizadores de Voz Soportados {#SupportedSpeechSynths}

Esta sección contén información acerca dos sintetizadores de voz soportados polo NVDA.
Para unha lista máis extensa dos sintetizadores libres e comerciais que podes mercar e descargar para utilizar co NVDA, por favor consulta a [páxina de voces extra](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

O sintetizador [eSpeak NG](https://github.com/espeak-ng/espeak-ng) compílase directamente no NVDA e non require ningún outro controlador ou componente especial para instalarse.
En Windows 8.1, o NVDA usa Espeak NG de xeito predeterminado ([Windows OneCore](#OneCore) úsase en Windows 10 e posteriores por defecto).
Como este sintetizador compilouse en NVDA, é unha gran elección para cando se executa NVDA nunha memoria USB ou nun CD noutros sistemas.

Cada voz que ven co eSpeak NG fala unha lingua diferente.
Hai unhas 43 linguas diferentes soportadas polo eSpeak NG.

Tamén hai moitas variantes que poden escollerse para alterar o son da voz.

### Microsoft Speech API versión 4 (SAPI 4) {#SAPI4}

SAPI 4 é un antigo estándar de Microsoft para sintetizadores de voz software.
NVDA aínda soporta esto para usuarios que teñan sintetizadores SAPI 4 instalados.
Non obstante, Microsoft xa non soporta esto e necesítanse compoñentes que xa non están dispoñibles dende Microsoft.

Cando uses este sintetizador co NVDA, as voces dispoñibles (ás que se acede dende a  [categoría Voz](#SpeechSettings) da caixa de diálogo [Opcións do NVDA](#NVDASettings) ou polo [Anel de Opcións do Sintetizador](#SynthSettingsRing)) conterán todas as voces de todos os motores instalados SAPI 4 atopados no teu sistema.

### Microsoft Speech API versión 5 (SAPI 5) {#SAPI5}

SAPI 5 é un estándar de Microsoft para sintetizadores de voz software.
Moitos sintetizadores de voz que cumpren con este estándar poderán comprarse ou descargarse gratuitamente dende varias compañías e sitios web, aíndaque probablemente o teu sistema xa virá con ao menos unha voz SAPI 5 preinstalada.
Cando se usa este sintetizador co NVDA, as voces dispoñibles (ás que se accede dende a [categoría Voz](#SpeechSettings) da caixa de diálogo [Opcións do NVDA](#NVDASettings) ou polo [Anel de Opcións do Sintetizador](#SynthSettingsRing)) conterán todas as voces de todos os motores SAPI 5 instalados atopados no teu sistema.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

Microsoft Speech Platform proporciona voces para moitas linguas que se utilizan habitualmente no desenvolvemento de aplicacións basadas en servidores de fala. 
Estas voces tamén poden utilizarse co NVDA.

Para utilizar estas voces, necesitarás instalar dous compoñentes:

* Microsoft Speech Platform - Runtime (Versión 11) , x86: https://www.microsoft.com/download/en/details.aspx?id=27225
* Microsoft Speech Platform - Runtime Languages (Versión 11): https://www.microsoft.com/download/en/details.aspx?id=27224
  * Esta páxina inclúe moitos ficheiros tanto de recoñecemento coma de texto a voz.
 Escolle os ficheiros que conteñan os datos TTS para as linguas/voces desexadas.
 Por exemplo, o ficheiro MSSpeech_TTS_en-US_ZiraPro.msi é unha voz inglesa U.S..

### Voces Windows OneCore {#OneCore}

Windows 10 ou posteriores inclúen novas voces coñecidas coma voces "OneCore" ou "mobile".
Proporciónanse voces para moitas linguas e son máis lixeiras que as voces Microsoft disponibles ao se usar Microsoft Speech API versión 5.
En Windows 10 ou posteriores, o NVDA usa voces Windows OneCore por defecto ([[eSpeak NG](#eSpeakNG) úsase noutras versións).

Para engadir voces Windows OneCore novas, vai a "Narrador", dentro das opcións de Accesibilidade. 
Usa a opción "Engadir voces" e procura a lingua desexada.
Moitas linguas inclúen múltiples variantes.
"Reino Unido" e "Australia" son dúas das variantes do inglés.
"Francia", "Canadá" e "Suiza" son variantes do francés dispoñibles.
Procura a familia da lingua (como inglés ou Francés), logo localiza a variante na listaxe.
Seleciona calquera lingua desexada e usa o botón "Engadir" para engadila.
Unha vez engadida, reinicia o NVDA.

Por favor consulta [Linguas soportadas e voces](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) para unha listaxe de voces dispoñibles.

## Pantallas Braille Soportadas {#SupportedBrailleDisplays}

Esta sección contén información acerca das pantallas braille soportadas polo NVDA.

### Pantallas que admiten a detección automática {#AutomaticDetection}

O NVDA ten a capacidade para detectar moitas pantallas braille de fondo automáticamente, ou a través do USB ou do bluetooth.
Este comportamento lógrase selecionando a opción Automático como a pantalla braille preferida dende a [caixa de diálogo Opcións de Braille](#BrailleSettings) do NVDA.
Esta opción está selecionada predeterminadamente.

As seguintes pantallas admiten esta funcionalidade de detección automática.

* Pantallas Handy Tech
* Pantallas Baum/Humanware/APH/Orbit braille
* Series das HumanWare Brailliant BI/B
* HumanWare BrailleNote
* SuperBraille
* Series das Optelec ALVA 6
* Series das HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille
* Pantallas Eurobraille Esys/Esytime/Iris
* Pantallas Nattiq nBraille
* Seika Notetaker: MiniSeika (16, 24 celdas V6, e6Pro (40 celdas
* Pantallas Tivomatic Caiku Albatross 46/80
* Calquera Pantalla que admita o protocolo braille estándar HID

### Series das Freedom Scientific Focus/PAC Mate {#FreedomScientificFocus}

Todas as pantallas Focus e PAC Mate de [Freedom Scientific](https://www.freedomscientific.com/) sopórtanse.
Necesitarás os controladores de pantallas braille de Freedom Scientific instalados no teu sistema.
Se non os tes aínda, podes obtelos da [Páxina do controlador da pantalla braille  Focus Blue](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Aíndaque esta páxina só mencione a pantalla Focus 40 Blue, o controlador soporta todas as pantallas Focus e Pacmate de Freedom Scientific.

Predeterminadamente, NVDA pode detectar automáticamente e conectarse a estas pantallas tanto a través do USB como do bluetooth.
Non obstante, cando se configura a pantalla, podes seleccionar explícitamente os portos "USB" ou "Bluetooth" para restrinxir o tipo de conexión a utilizar.
Esto podería ser útil se queres conectar a pantalla focus ao NVDA utilizando bluetooth, e todavía poderías cargala utilizando a enerxía do USB dende o teu ordenador.
A deteción automática de pantallas braille do NVDA tamén recoñecerá a pantalla en USB ou en Bluetooth.

Seguidamente van as asociacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |tecla|
|---|---|
|Desprazar pantalla braille atrás |sensorSuperior1 (primeira celda na liña)|
|Desprazar pantalla braille adiante |sensorSuperior20/40/80 (última celda na liña)|
|Desprazar pantalla braille atrás |barraDeAvance esquerda|
|Desprazar pantalla braille adiante |barraDeAvance dereita|
|Conmutar seguemento de braille |leftGDFButton+rightGDFButton|
|Conmutar acción de roda esquerda |premer roda esquerda|
|Moverse cara atrás utilizando acción de roda esquerda |roda esquerda cara arriba|
|Moverse cara adiante utilizando acción de roda esquerda |roda esquerda cara abaixo|
|Conmutar acción de roda dereita |premer roda dereita|
|Moverse cara atrás utilizando acción de roda dereita |roda dereita cara arriba|
|Moverse cara adiante utilizando acción de roda dereita |roda dereita cara abaixo|
|Guiar cara a celda braille |sensor|
|tecla shift+tab |barra espaciadora braille+punto1+punto2|
|tecla tab |barra espaciadora braille+punto4+punto5|
|tecla frecha abaixo |barra espaciadora braille+punto1|
|tecla frecha arriba |barra espaciadora braille+punto4|
|tecla control+frecha esquerda |barra espaciadora braille+punto2|
|tecla control+frecha dereita |barra espaciadora braille+punto5|
|tecla frecha esquerda |barra espaciadora braille+punto3|
|tecla frecha dereita |barra espaciadora braille+punto6|
|tecla inicio |barra espaciadora braille+punto1+punto3|
|tecla fin |barra espaciadora braille+punto4+punto6|
|tecla control+inicio |barra espaciadora braille+punto1+punto2+punto3|
|tecla control+fin |barra espaciadora braille+punto4+punto5+punto6|
|tecla alt |barra espaciadora braille+punto1+punto3+punto4|
|tecla alt+tab |barra espaciadora braille+punto2+punto3+punto4+punto5|
|tecla alt+shift+tab |barra espaciadorabraille+punto1+punto2+punto5+punto6|
|tecla windows+tab |barra espaciadora braille+punto2+punto3+punto4|
|tecla escape |barra espaciadora braille+punto1+punto5|
|tecla windows |barra espaciadora braille+punto2+punto4+punto5+punto6|
|tecla espazo |barra espaciadora braille|
|Conmutar tecla control |Barra espaciadora braille+punto3+punto8|
|conmutar tecla alt |barra espaciadora braille+punto6+punto8|
|conmutar tecla windows |barra espaciadora braille+punto4+punto8|
|conmutar tecla NVDA |barra espaciadora braille+punto5+punto8|
|conmutar tecla shift |barra espaciadora braille+punto7+punto8|
|conmutar teclas control e shift |barra espaciadora braille+punto3+punto7+punto8|
|conmutar teclas alt e shift |barra espaciadora braille+punto6+punto7+punto8|
|conmutar teclas windows e shift |barra espaciadora braille+punto4+punto7+punto8|
|conmutar teclas NVDA e shift |barra espaciadora braille+punto5+punto7+punto8|
|conmutar teclas control e alt |barra espaciadora braille+punto3+punto6+punto8|
|conmutar teclas control, alt e shift |barra espaciadora braille+punto3+punto6+punto7+punto8|
|tecla windows+d (minimizar todas as aplicacións) |barra espaciadora braille+punto1+punto2+punto3+punto4+punto5+punto6|
|Anunciar Liña Actual |barra espaciadora braille+punto1+punto4|
|Menú NVDA |barra espaciadora braille+punto1+punto3+punto4+punto5|

Para os modelos máis recentes da Focus que conteñen teclas de balancíns (focus 40, focus 80 e focus blue):

| Nome |Tecla|
|---|---|
|Mover pantalla braille á liña anterior |balancín esquerdo arriba, balancín dereito arriba|
|Mover pantalla braille á liña seguinte |balancín esquerdo abaixo, balancín dereito abaixo|

Só para a Focus 80:

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille atrás |barra frontal esquerda arriba, barra frontal dereita arriba|
|Desprazar pantalla braille adiante |barra frontal esquerda abaixo, barra frontal dereita abaixo|

<!-- KC:endInclude -->

### Series da Optelec ALVA 6/conversor de protocolo {#OptelecALVA}

Ambas pantallas ALVA BC640 e BC680 de [Optelec](https://www.optelec.com/) sopórtanse.
Alternativamente, podes conectar unha pantalla vella de Optelec, coma unha Braille Voyager, usando un conversor de protocolo suministrado por Optelec.
Non necesitas instalar ningún controlador en especial para utilizar estas pantallas.
Só enchufa a pantalla e configura o NVDA para utilizalas.

Nota: O NVDA podería non seren capaz de usar unha pantalla ALVA BC6 co Bluetooth cando se emparella usando a utilidade ALVA Bluetooth.
Cando emparellaras o teu dispositivo usando a súa utilidade e o NVDA non poda detectalo, recomendámosche enparellar a túa pantalla ALVA do xeito ordinario usando as opcións de Bluetooth de Windows.

Nota: dado que algunhas destas pantallas teñen un teclado braille, manexan a transcripción de braille a texto por si mesmas por omisión.
Esto siñifica que o sistema de entrada braille do NVDA non se está a usar nunha situación predeterminada (é dicir, a táboa de entrada braille configurada non ten efecto).
Para pantallas ALVA co firmware recente, é posible deshabilitar esta simulación de teclado HID usando un xesto de entrada.

Seguidamente van as asignacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |t1, etouch1|
|Mover a pantalla braille á liña anterior |t2|
|Mover ao foco actual |t3|
|Mover a pantalla braille á a liña seguinte |t4|
|Desprazar pantalla braille cara adiante |t5, etouch3|
|Guiar á celda braille |sensor|
|Anunciar formato de texto baixo a celda braille |sensores secundarios|
|Conmutar a simulación de teclado HID |t1+spEnter|
|Mover á liña superior en revisión |t1+t2|
|Mover á liña inferior en revisión |t4+t5|
|Conmutar o seguemento braille |t1+t3|
|Anunciar o título |etouch2|
|Anunciar a barra de estado |etouch4|
|tecla shift+tab |sp1|
|tecla alt |sp2, alt|
|tecla escape |sp3|
|tecla tab |sp4|
|tecla frecha arriba |spUp|
|tecla frecha abaixo |spDown|
|tecla frecha esquerda |spLeft|
|tecla frecha dereita |spRight|
|tecla intro |spEnter, intro|
|Anunciar data/hora |sp2+sp3|
|menú NVDA |sp1+sp3|
|tecla windows+d (minimizar todas as aplicacións) |sp1+sp4|
|Tecla windows+b (enfocar a bandexa do sistema) |sp3+sp4|
|tecla windows |sp1+sp2, windows|
|tecla alt+tab |sp2+sp4|
|tecla control+inicio |t3+spArriba|
|tecla control+fin |t3+spAbaixo|
|tecla inicio |t3+spEsquerda|
|tecla fin |t3+spDereita|
|tecla control |control|

<!-- KC:endInclude -->

### Pantallas Handy Tech {#HandyTech}

O NVDA soporta a maioría das pantallas de [Handy Tech](https://www.handytech.de/) cando se conecten por USB, porto serie ou bluetooth.
Para algunhas pantallas antigas USB, necesitarás instalar os controladores USB de Handy Tech no teu sistema.

As seguintes pantallas non se soportan ao se sacarlas da caixa, pero poden usarse a través do [controlador universal de Handy Tech](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) e o complemento do NVDA:

* Braillino
* Bookworm
* Pantallas modulares coa versión do firmware 1.13 ou inferior. Por favor ten en conta que o firmware destas pantallas pode actualizarse.

Seguidamente van as asignacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar a pantalla braille cara atrás |esquerda, arriba, b3|
|Desprazar a pantalla braille cara adiante |Dereita, abaixo, b6|
|Mover a pantalla braille á liña anterior |b4|
|Mover a pantalla braille á liña seguinte |b5|
|Guiar á celda braille |sensor|
|tecla shift+tab |esc, triple ación  da tecla esquerda arriba+abaixo|
|tecla alt |b2+b4+b5|
|tecla escape |b4+b6|
|tecla tab |enter, triple ación  da tecla dereita arriba+abaixo|
|tecla intro |esc+enter, triple ación  da tecla dereita arriba+abaixo, ación joystick|
|tecla frecha arriba |joystick arriba|
|tecla frecha abaixo |joystick abaixo|
|tecla frecha esquerda |joystick esquerda|
|tecla frecha dereita |joystick dereita|
|menú NVDA |b2+b4+b5+b6|
|Conmutar seguemento do braille |b2|
|Conmutar o cursor braille |b1|
|Conmutar a presentación de contexto do foco |b7|
|Conmutar entrada braille |espazo+b1+b3+b4 (espazo+B maiúscula)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

A pantalla braille Lilli dispoñible dende [MDV](https://www.mdvbologna.it/) sopórtase.
Non necesitas instalar ningún controlador específico para utilizar esta pantalla.
Só enchufa a pantalla e configura o NVDA para utilizala.

Esta pantalla aínda non admite a funcionalidade de detección automática do NVDA.

Seguen as asignacións das teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille atrás |LF|
|Desprazar pantalla braille adiante |RG|
|Mover pantalla braille á liña anterior |UP|
|Mover pantalla braille á liña seguinte |DN|
|Enrutar cara a celda braille |route|
|Tecla shift+tab |SLF|
|Tecla tab |SRG|
|Tecla alt+tab |SDN|
|Tecla alt+shift+tab |SUP|

<!-- KC:endInclude -->

### Pantallas braille Baum/Humanware/APH/Orbit {#Baum}

Varias pantallas braille de [Baum](https://www.baum.de/cms/en/), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) e [Orbit](https://www.orbitresearch.com/) están soportadas cando se conectan a través dos portos USB, bluetooth ou serie.
Estas inclúen:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Algunhas outras pantallas manufacturadas por Baum tamén poderían funcionar, aíndaque non foron probadas.

Se conectas a través do USB outras pantallas que non usen HID, primeiro debes instalar os controladores USB proporcionados polo fabricante.
A VarioUltra e a Pronto! usan HID.
A Refreshabraille e a Orbit Reader 20 poden usar HID se se configuran apropriadamente.

O modo serie USB da Orbit Reader 20 actualmente só se soporta no Windows 10 e posteriores
Xeralmente debería usarse USB HID  no seu lugar.

Seguidamente van as asignacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla braille para descripcións de onde se poden atopar estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |d2|
|Desprazar pantalla braille cara adiante |d5|
|Mover a pantalla braille á liña anterior |d1|
|Mover a liña brailla á liña seguinte |d3|
|Guiar á celda braille |sensor|
|teclas shift+tab |espazo+punto1+punto3|
|tecla tab |espazo+punto4+punto6|
|tecla alt |espazo+punto1+punto3+punto4 (espazo+m)|
|tecla escape |espazo+punto1+punto5 (espazo+e)|
|tecla windows |espazo+punto3+punto4|
|teclas alt+tab |espazo+punto2+punto3+punto4+punto5 (espazo+t)|
|Menú NVDA |espazo+punto1+punto3+punto4+punto5 (espazo+n)|
|teclas windows+d (minimizar todas as aplicacións) |espazo+punto1+punto4+punto5 (espazo+d)|
|Falar todo |espazo+punto1+punto2+punto3+punto4+punto5+punto6|

Para liñas que teñan un joystick:

| Nome |Tecla|
|---|---|
|Tecla frecha arriba |arriba|
|Tecla frecha abaixo |abaixo|
|Tecla frecha esquerda |esquerda|
|Tecla frecha dereita |dereita|
|Tecla intro |seleccionar|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

A hedo ProfiLine USB de [hedo Reha-Technik](https://www.hedo.de/) está soportada.
Primeiro debes instalar os controladores USB proporcionados polo fabricante.

Esta pantalla aínda non admite a funcionalidade de detección automática do NVDA.

Seguidamente van as asignacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar a pantalla braille cara atrás |K1|
|Desprazar a pantalla braille cara adiante |K3|
|Mover a pantalla braille a liña anterior |B2|
|Mover a pantalla braille a seguinte liña |B5|
|Ir a celda braille |routing|
|Conmutar seguemento braille |K2|
|Ler todo |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

Sopórtase a hedo MobilLine USB de [hedo Reha-Technik](https://www.hedo.de/).
Primeiro debes instalar os controladores USB proporcionados polo fabricante.

Esta pantalla aínda non admite a funcionalidade de detección automática do NVDA.

Seguidamente van as asignacións de teclas para esta pantalla co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille atrás |K1|
|Desprazar pantalla braille adiante |K3|
|Mover pantalla braille a liña anterior |B2|
|Mover pantalla braille a seguinte liña |B5|
|Ir a celda braille |sensores|
|Conmutar seguemento de braille |K2|
|Ler todo |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant Series BI/B / BrailleNote Touch {#HumanWareBrailliant}

As pantallas braille Brailliant series BI e B de [HumanWare](https://www.humanware.com/), incluíndo BI 14, BI 32, BI 20X, BI 40, BI 40X e B 80, están soportadas cando se conectan a través do USB ou bluetooth.
Se a conectas a través de USB co protocolo configurado a HumanWare, primeiro debes instalar os controladores USB proporcionados polo fabricante.
Non se requiren os controladores USB se o protocolo se configura a OpenBraille.

Tamén se admiten os seguintes dispositivos extra (e non requiren ningún controlador en especial para seren instalados):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Seguidamente van as asignacións de teclas para as pantallas Brailliant BI/B e BrailleNote touch co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse estas teclas.

#### Asignacións de teclas para todos os modelos {#toc326}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |esquerda|
|Desprazar pantalla braille cara adiante |dereita|
|Mover pantalla braille á liña anterior |arriba|
|Mover pantalla braille á liña seguinte |abaixo|
|Guiar ata a celda braille |sensores|
|Activar/desactivar seguemento de braille |arriba+abaixo|
|tecla frecha arriba |espazo+punto1|
|tecla frecha abaixo |espazo+punto4|
|tecla frecha esquerda |espazo+punto3|
|tecla frecha dereita |espazo+punto6|
|tecla shift+tab |espazo+punto1+punto3|
|tecla tab |espazo+punto4+punto6|
|tecla alt |espazo+punto1+punto3+punto4 (espazo+m)|
|tecla escape |espazo+punto1+punto5 (espazo+e)|
|tecla intro |punto8|
|tecla windows |espazo+punto3+punto4|
|tecla alt+tab |espazo+punto2+punto3+punto4+punto5 (espazo+t)|
|Menú NVDA |espazo+punto1+punto3+punto4+punto5 (espazo+n)|
|tecla windows+d (minimizar todas las aplicaciones) |espacio+punto1+punto4+punto5 (espacio+d)|
|Ler todo |espazo+punto1+punto2+punto3+punto4+punto5+punto6|

<!-- KC:endInclude -->

#### Asignacións de teclas para Brailliant BI 32, BI 40 e B 80 {#toc327}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Menú NVDA |c1+c3+c4+c5 (comando n)|
|tecla windows+d (minimizar todas as aplicacións) |c1+c4+c5 (comando d)|
|Ler todo |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Asignacións de teclas para Brailliant BI 14 {#toc328}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|tecla frecha arriba |joystick arriba|
|tecla frecha abaixo |joystick abaixo|
|tecla frecha esquerda |joystick esquerda|
|tecla frecha dereita |joystick dereita|
|tecla intro |accionar joystick|

<!-- KC:endInclude -->

### Series das HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille {#Hims}

O NVDA soporta as pantallas Braille Sense, Braille EDGE, Smart Beetle e Sync Braille de [Hims](https://www.hims-inc.com/) cando se conectan a través do USB ou bluetooth. 
Se se conecta a través de USB, necesitarás instalar os [controladores USB de HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) no teu sistema.

Seguidamente van as asignacións de teclas para estas pantallas co NVDA.
Por favor consulta a documentación das pantallas para descripcións de onde poden atoparse estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Ir á celda braille |sensores|
|Desprazar pantalla braille atrás |leftSideScrollUp, rightSideScrollUp, leftSideScroll|
|Desprazar pantalla braille adiante |leftSideScrollDown, rightSideScrollDown, rightSideScroll|
|Mover pantalla braille á liña anterior |leftSideScrollUp+rightSideScrollUp|
|Mover pantalla braille á liña seguinte |leftSideScrollDown+rightSideScrollDown|
|Mover á liña anterior en revisión |rightSideUpArrow|
|Mover á liña seguinte en revisión |rightSideDownArrow|
|Mover ao carácter  anterior en revisión |rightSideLeftArrow|
|Mover ao carácter seguinte en revisión |rightSideRightArrow|
|Mover ao foco actual |leftSideScrollUp+leftSideScrollDown, rightSideScrollUp+rightSideScrollDown, leftSideScroll+rightSideScroll|
|Tecla control |smartbeetle:f1, brailleedge:f3|
|Tecla windows |f7, smartbeetle:f2|
|tecla alt |punto1+punto3+punto4+espazo, f2, smartbeetle:f3, brailleedge:f4|
|tecla shift |f5|
|tecla insert |punto2+punto4+espazo, f6|
|tecla aplicacións |punto1+punto2+punto3+punto4+espazo, f8|
|tecla bloqueo de maiúsculas |punto1+punto3+punto6+espazo|
|tecla tab |punto4+punto5+espazo, f3, brailleedge:f2|
|teclas shift+alt+tab |f2+f3+f1|
|teclas alt+tab |f2+f3|
|teclas shift+tab |punto1+punto2+espazo|
|tecla fin |punto4+punto6+espazo|
|teclas control+fin |punto4+punto5+punto6+espazo|
|tecla inicio |punto1+punto3+espazo, smartbeetle:f4|
|teclas control+inicio |punto1+punto2+punto3+espazo|
|teclas alt+f4 |punto1+punto3+punto5+punto6+espazo|
|tecla frecha esquerda |punto3+espazo, leftSideLeftArrow|
|teclas control+shift+frecha esquerda |punto2+punto8+espazo+f1|
|teclas control+frecha esquerda |punto2+espazo|
|teclas shift+frecha esquerda |punto2+punto7+f1|
|teclas alt+frecha esquerda |punto2+punto7|
|tecla frecha dereita |punto6+espazo, leftSideRightArrow|
|teclas control+shift+frecha dereita |punto5+punto8+espazo+f1|
|teclas control+frecha dereita |punto5+espazo|
|teclas shift+alt+frecha dereita |punto5+punto7+f1|
|teclas alt+frecha dereita |punto5+punto7|
|tecla rePáx |punto1+punto2+punto6+espazo|
|teclas control+rePáx |punto1+punto2+punto6+punto8+espazo|
|tecla frecha arriba |punto1+espazo, leftSideUpArrow|
|teclas control+shift+frecha arriba |punto2+punto3+punto8+espazo+f1|
|teclas control+frecha arriba |punto2+punto3+espazo|
|teclas shift+alt+frecha arriba |punto2+punto3+punto7+f1|
|teclas alt+frecha arriba |punto2+punto3+punto7|
|teclas shift+frecha arriba |leftSideScrollDown+espazo|
|tecla avPáx |punto3+punto4+punto5+espazo|
|teclas control+avPáx |punto3+punto4+punto5+punto8+espazo|
|tecla frecha abaixo |punto4+espazo, leftSideDownArrow|
|teclas control+shift+frecha abaixo |punto5+punto6+punto8+espazo+f1|
|teclas control+frecha abaixo |punto5+punto6+espazo|
|teclas shift+alt+frecha abaixo |punto5+punto6+punto7+f1|
|teclas alt+frecha abaixo |punto5+punto6+punto7|
|teclas shift+frecha abaixo |espacio+rightSideScrollDown|
|tecla escape |punto1+punto5+espazo, f4, brailleedge:f1|
|tecla borrar |punto1+punto3+punto5+espazo, punto1+punto4+punto5+espazo|
|tecla f1 |punto1+punto2+punto5+espazo|
|tecla f3 |punto1+punto4+punto8+espazo|
|tecla f4 |punto7+f3|
|teclas windows+b |punto1+punto2+f1|
|teclas windows+d |punto1+punto4+punto5+f1|
|teclas control+insert |smartbeetle:f1+rightSideScroll|
|teclas alt+insert |smartbeetle:f3+rightSideScroll|

<!-- KC:endInclude -->

### Pantallas Braille Seika {#Seika}

As seguintes pantallas braille Seika de Nippon Telesoft admítense en dous grupos con funcionalidade diferente:

* [Seika Version 3, 4 e 5 (40 celdas), Seika80 (80 celdas)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 celdas), V6, e V6Pro (40 celdas)](#SeikaNotetaker)

Podes atopar máis información sobre as pantallas na súa [Páxina de descarga de demostracións e controladores](https://en.seika-braille.com/down/index.html).

#### Seika Versión 3, 4, e 5 (40 celdas), Seika80 (80 celdas) {#SeikaBrailleDisplays}

* Estas pantallas aínda non admiten a función de detección automática de pantallas braille do NVDA.
* Seleciona "Pantallas Braille Seika" para configuarlas manualmente
* Deben instalarse controladores de dispositivo antes de usar Seika v3/4/5/80.
Os controladores [proporciónanse polo fabricante](https://en.seika-braille.com/down/index.html).

Seguen as asignacións de teclas das pantallas braille Seika.
Por favor consulta a documentación da pantalla para descripcióms de onde se atopan estas teclas.
<!-- KC:beginInclude -->

| Nome |tecla|
|---|---|
|Desprazar pantalla braille atrás |esquerda|
|Desprazar pantalla braille adiante |dereita|
|Mover pantalla braille á liña anterior |b3|
|Mover pantalla braille á seguinte liña |b4|
|Conmutar seguemento do braille |b5|
|Ler todo |b6|
|tab |b1|
|shift+tab |b2|
|alt+tab |b1+b2|
|Menú NVDA |esquerda+dereita|
|Ir á celda braille |sensores|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 celdas), V6 e V6Pro (40 celdas) {#SeikaNotetaker}

* A funcionalidade de detección automática de pantallas braille do NVDA é compatible a través de USB e Bluetooth.
* Seleciona "Seika Notetaker" ou "auto" para configurar.
* Non se requiren conroladores adicionais cando se usa unha pantalla braille Seika Notetaker.

As asignacións de teclas da Seika son as que seguen.
Por favor consulta a documentación da pantalla para descripcións de onde se poden atopar estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar atrás pantalla braille |Esquerda|
|Desprazar adiante pantalla braille |dereita|
|Ler todo |espazo+retroceso|
|Menú NVDA |Esquerda+dereita|
|Mover pantalla braille á liña anterior |LJ arriba|
|Mover pantalla braille á seguinte liña |LJ abaixo|
|Conmutar seguemento braille |LJ centro|
|tab |LJ dereita|
|shift+tab |LJ esquerda|
|frecha arriba |RJ arriba|
|frecha abaixo |RJ abaixo|
|frecha esquerda |RJ esquerda|
|frecha dereita |RJ dereita|
|Enrutar a celda braille |sensores|
|shift+frecha arriba |espazo+RJ arriba, retroceso+RJ arriba|
|shift+frecha abaixo |espazo+RJ abaixo, Retroceso+RJ abaixo|
|shift+frecha esquerda |espazo+RJ esquerda, Retroceso+RJ esquerda|
|shift+frecha dereita |Espazo+RJ dereita, Retroceso+RJ dereita|
|intro |RJ centro, punto8|
|escape |Espazo+RJ centro|
|tecla windows |Retroceso+RJ centro|
|espazo |Espazo, Retroceso|
|retroceso |punto7|
|retroceso de páxina |espazo+LJ dereita|
|avance de páxina |Espazo+LJ esquerda|
|inicio |Espazo+LJ arriba|
|fin |Espazo+LJ abaixo|
|control+inicio |Retroceso+LJ arriba|
|control+fin |Retroceso+LJ abaixo|

### Modelos máis novos da Papenmeier BRAILLEX {#Papenmeier}

Sopórtanse as seguintes pantallas Braille: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB e bluetooth)
* BRAILLEX Live 20, BRAILLEX Live e BRAILLEX Live Plus (USB e bluetooth)

Estas pantallas non admiten a funcionalidade de detección automática do NVDA.
Hai unha opción no controlador USB da pantalla que pode causar un problema coa carga da pantalla.
Por favor proba o seguinte:

1. Asegúrate de que instalaches o [derradeiro controlador](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Abre o administrador de dispositivos de Windows.
1. Desprázate cara abaixo pola listaxe ate "Controladores USB" ou "Dispositivos USB".
1. Seleciona "dispositivo Papenmeier Braillex USB".
1. Abre as propriedades e cambia á pestana "Avanzadas".
Ás veces a pestana "Avanzadas" non aparece.
Se é este o caso, desconecta a pantalla braille do computador, sae do NVDA, espera un intre e reconecta a pantalla braille.
Repite esto 4 ou 5 veces se fora necesario.
Se a pestana "Avanzadas" aínda non se amosa, por favor reinicia o computador.
1. Deshabilita a opción "Cargar VCP".

A maioría dos dispositivos teñen unha Barra de Acceso sinxelo (EAB) que permite operar rápida e intuitivamente.
A EAB pode moverse en catro direccións onde en xeral cada dirección ten dúas posicións.
A serie c é a única excepción a esta regra.

A serie c e algunhas outras liñas teñen dúas filas de sensores polo que a fila superior utilízase para anunciar información de formato.
Mantendo premeda unha das teclas superiores e premendo a EAB nos dispositivos da serie c emúlase a segunda posición.
As series das pantallas live teñen unha fila de sensores só e a EAB ten un paso por dirección.
O segundo paso poderá emularse premendo unha das teclas de sensor e premendo a EAB na dirección correspondente.
Premendo e mantendo as teclas arriba, abaixo, dereita e esquerda (ou a EAB) cáusase que a acción correspondente se repita. 

Xeralmente, as seguintes teclas están dispoñibles nestas pantallas braille:

| Nome |Tecla|
|---|---|
|l1 |Tecla esquerda frontal|
|l2 |Tecla esquerda traseira|
|r1 |Tecla dereita frontal|
|r2 |Tecla dereita traseira|
|arriba |1 paso arriba|
|arriba2 |2 pasos arriba|
|izquierda |1 paso á esquerda|
|izquierda2 |2 pasos á esquerda|
|derecha |1 paso á dereita|
|derecha2 |2 pasos á dereita|
|dn |1 paso abaixo|
|dn2 |2 pasos abaixo|

Seguidamente van as asignacións de ordes da Papenmeier para o NVDA:
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille atrás |esquerda|
|Desprazar pantalla braille adiante |dereita|
|Mover pantalla braille á liña anterior |arriba|
|Mover pantalla braille á liña seguinte |dn|
|Ir á celda braille |sensores|
|Anunciar carácter actual en revisión |l1|
|Activar actual navegador de obxectos |l2|
|Activar ou desactivar seguemento do braille |r2|
|Anunciar título |l1+arriba|
|Anunciar barra de estado |l2+abaixo|
|Mover ao obxecto contido |arriba2|
|Mover ao primeiro obxecto contido |dn2|
|Mover ao obxecto anterior |dereita2|
|Mover ao seguinte obxecto |esquerda2|
|Anunciar formato de texto baixo a celda braille |fila de sensores superior|

<!-- KC:endInclude -->

O modelo Trio ten catro teclas adicionais que están diante do teclado braille.
Estas son (ordeadas de esquerda a dereita):

* tecla de pulgar esquerdo (lt)
* espazo
* espazo
* tecla de pulgar dereito (rt)

Actualmente, a tecla pulgar dereito non se utiliza.
As teclas interiores mapéanse a espazo.

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|tecla escape |espazo co punto 7|
|tecla frecha arriba |espazo co punto  2|
|tecla frecha esquerda |espazo co punto 1|
|tecla frecha dereita |espazo co punto 4|
|tecla frecha abaixo |espazo co punto 5|
|tecla control |lt+punto2|
|tecla alt |lt+punto3|
|tecla control+escape |espazo cos puntos 1 2 3 4 5 6|
|tecla tab |espazo cos puntos 3 7|

<!-- KC:endInclude  -->

### Modelos Antigos Papenmeier Braille BRAILLEX {#PapenmeierOld}

Sopórtanse as seguintes pantallas Braille: 

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Ten en conta que estas pantallas só se poden conectar a través dun porto serie.
Debido a esto, estas pantallas non admiten a funcionalidade de detección automática do NVDA.
Deberías selecionar o porto ao que está conectada a pantalla despois de ter escolleito este controlador na caixa de diálogo [Selecionar pantalla Braille](#SelectBrailleDisplay).

Algúns destes dispositivos teñen unha barra de acceso rápido (EAB) que permite un accionamento rápido e intuitivo.
O EAB pódese mover en catro direccións onde, xeralmente, cada dirección ten dous movementos.
Premendo e mantendo as teclas Arriba, abaixo, dereita e esquerda (ou EAB) faise que a acción correspondente sexa repetida.
Os dispositivos máis antigos non teñen unha EAB; utilízanse, no seu lugar, teclas frontais .

Xeralmente, as seguintes teclas están dispoñibles nas pantallas braille:

| Nome |Tecla|
|---|---|
|l1 |Tecla frontal esquerda|
|l2 |Tecla traseira esquerda|
|r1 |Tecla frontal dereita|
|r2 |Tecla traseira dereita||
|up |1 paso arriba||
|up2 |2 pasos arriba|
|left |1 paso á esquerda|
|left2 |2 pasos á esquerda|
|right |1 paso á dereita|
|right2 |2 pasos á dereita|
|dn |1 paso abaixo|
|dn2 |2 pasos abaixo|

Seguidamente van as asignacións de ordes das Papenmeier para o NVDA:

<!-- KC:beginInclude -->
Dispositivos co EAB:

| Nome |Tecla|
|---|---|
|Desprazar a pantalla braille atrás |esquerda|
|Desprazar a pantalla braille adiante |dereita|
|Mover a pantalla braille á liña anterior |arriba|
|Mover a pantalla braille á li´ña seguinte |abaixo|
|Ir á celda braille |sensores|
|Anunciar carácter actual en revisión |l1|
|Activar navegador de obxectos actual |l2|
|Anunciar título |l1up|
|Anunciar Barra de Estado| l2down|
|Moverse ao obxecto contedor |up2|
|Moverse ao primeiro obxecto contido |dn2|
|Moverse ao seguinte obxecto |left2|
|Moverse ao obxecto anterior |right2|
|Anunciar formato de texto baixo a celda braille |Upper routing strip|

BRAILLEX Tiny:

| Nome |Tecla|
|---|---|
|Anunciar carácter actual en revisión |l1|
|Activar navegador de obxectos actual |l2|
|Desprazar pantalla braille atrás |left|
|Desprazar pantalla braille adiante |right|
|Mover pantalla braille á liña anterior |up|
|Mover pantalla braille á liña seguinte |dn|
|Activar e desactivar seguemento do braille |r2|
|Moverse ao obxecto contedor |r1+up|
|Moverse ao primeiro obxecto contido |r1+dn|
|Moverse ao obxecto anterior |r1+left|
|Moverse ao seguinte obxecto |r1+right|
|Anunciar formato de texto baixo a celda braille |sensores superior|
|Anunciar título |l1+arriba|
|Anunciar barra de estado |l2+abaixo|

BRAILLEX 2D Screen:

| Nome |Tecla|
|---|---|
|Anunciar carácter actual en revisión |l1|
|Activar navegador de obxectos actual |l2|
|Activar ou desactivar seguemento do braille |r2|
|Anunciar formato de texto baixo a celda braille |sensores superior|
|Mover pantalla braille á liña anterior| up|
|Desprazar pantalla braille atrás |left|
|Desprazar pantalla braille adiante |right|
|Mover pantalla braille á liña seguinte |dn|
|Moverse ao obxecto seguinte |left2|
|Moverse ao obxecto contedor |up2|
|Moverse ao primeiro obxecto contido |dn2|
|Moverse ao obxecto anterior |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

O NVDA soporta os anotadores electrónicos BrailleNote de [Humanware](https://www.humanware.com) cando actúen como un terminal braille para un lector de pantalla.
Sopórtanse os seguintes modelos:

* BrailleNote Classic (só conexión serie)
* BrailleNote PK (Conexións serie e bluetooth)
* BrailleNote MPower (Conexións serie e bluetooth)
* BrailleNote Apex (Conexións USB e Bluetooth)

Para o BrailleNote Touch, por favor consulta a seción [series das Brailliant BI / BrailleNote Touch](HumanWareBrailliant).

Excepto para o BrailleNote PK, admítense ambos teclados braille (BT) e QWERTY (QT).
Para o BrailleNote QT, non se admite a emulación do teclado do PC.
Tamén podes introducir puntos braille usando o teclado QT.
Por favor consulta a seción de terminal braille da guía de manual do BrailleNote para detalles.

Se o teu dispositivo soporta máis dun tipo de conexión, cando conectes o teu BrailleNote ao NVDA, debes configurar o porto da terminal braille nas opcións de terminal braille.
Por favor consulta o manual do BrailleNote para detalles.
No NVDA, tamén poderías necesitar configurar o porto na caixa de diálogo [Selecionar Pantalla Braille](#SelectBrailleDisplay).
Se te estás a conectar a través de USB ou bluetooth, podes configurar o porto a "Automático", "USB" ou "Bluetooth", dependendo das opcións dispoñibles.
Se te estás a conectar utilizando un porto serie (ou un conversor de USB a serie) ou se non aparece ningunha das opcións anteriores, debes escoller explícitamente o porto de comunicación a se utilizar dende a lista de portos hardware.

Antes de conectar o teu BrailleNote Apex utilizando o seu cliente de interface USB, debes instalar os controladores proporcionados por HumanWare.

No BrailleNote Apex BT, podes usar a roda de desprazamento ubicada entre os puntos 1 e 4 para varias ordes do NVDA.
A roda consiste en  catro puntos direcionais, un clic no botón central, e unha roda que xira no sentido ou contra do sentido das agullas do reloxo.

Seguidamente van as asignacións de ordes do BrailleNote para o NVDA.
Por favor consulta a documentación do BrailleNote para atopar onde se localizan estas teclas.

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar atrás pantalla braille |retroceder|
|Desprazar adiante pantalla braille |avanzar|
|Mover pantalla braille á liña anterior |anterior|
|Mover pantalla braille á liña seguinte |seguinte|
|Levar á celda braille |sensores|
|menú NVDA |espazo+punto1+punto3+punto4+punto5 (espazo+n)|
|Activar e desactivar seguemento do braille |anterior+seguinte|
|Tecla frecha arriba |espazo+punto1|
|Tecla frecha abaixo |espazo+punto4|
|Tecla frecha esquerda |espazo+ponmto3|
|Tecla frecha dereita |espazo+punto6|
|Tecla retroceso de páxina |espazo+punto1+punto3|
|Tecla avance de páxina |espazo+punto4+punto6|
|Tecla inicio |espazo+punto1+punto2|
|Tecla Fin |espazo+punto4+punto5|
|teclas Control+inicio |espazo+punto1+punto2+punto3|
|Teclas Control+fin |espazo+punto4+punto5+punto6|
|tecla espazo |espazo|
|Intro |espazo+punto8|
|Retroceso |espazo+punto7|
|Tecla Tab |espazo+punto2+punto3+punto4+punto5 (espazo+t)|
|Teclas Shift+tab |espazo+punto1+punto2punto5+punto6|
|Tecla Windows |espazo+punto2+punto4+punto5+punto6 (espazo+w)|
|Tecla Alt |espazo+punto1+punto3+punto4 (espazo+m)|
|Activar e desactivar axuda de entrada |espazo+punto2+punto3+punto6 (espazo+h abaixo)|

Seguidamente van as ordes asignadas ao BrailleNote QT cando non está en modo de entrada braille.

| Nome |Tecla|
|---|---|
|Menú NVDA |ler+n|
|Tecla frecha arriba |frecha arriba|
|Tecla frecha abaixo |frecha abaixo|
|Tecla frecha esquerda |frecha esquerda|
|Tecla frecha dereita |frecha dereita|
|Tecla retroceso de páxina |función+frecha arriba|
|Tecla avance de páxina |función+frecha abaixo|
|Tecla inicio |función+frecha esquerda|
|Tecla fin |función+frecha dereita|
|Control+teclas inicio |ler+t|
|Control+teclas fin |ler+b|
|Tecla intro |intro|
|Tecla retroceso |retroceso|
|Tecla tab |tab|
|Teclas Shift+tab |shift+tab|
|Tecla Windows |ler+w|
|Tecla Alt |ler+m|
|Conmutar axuda de entrada |ler+1|

Seguidamente van as ordes asignadas á roda de desprazamento:

| Nome |Tecla|
|---|---|
|Tecla frecha arriba |frecha arriba|
|Tecla frecha abaixo |frecha abaixo|
|Tecla frecha esquerda |frecha esquerda|
|Tecla frecha dereita |frecha dereita|
|Tecla intro |botón central|
|Tecla Tab |desprazar a roda no sentido das agullas do reloxo|
|tecla Shift+tab |desprazar a roda no sentido contrario ás agullas do reloxo|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

O NVDA soporta pantallas EcoBraille de [ONCE](https://www.once.es/).
Sopórtanse os seguintes modelos:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

No NVDA, podes configurar o porto serie ao que se conecta a pantalla na caixa de diálogo [Selecionar Pantalla Braille](#SelectBrailleDisplay).
Estas pantallas non admiten a funcionalidade de detección automática do NVDA.

Seguidamente van as asignacións de teclas para as pantallas EcoBraille.
Por favor consulta a [documentación para EcoBraille](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) para descripcións de onde se poden atopar estas teclas.

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar atrás pantalla braille |T2|
|Desprazar adiante pantalla braille |T4|
|Mover pantalla braille a liña anterior |T1|
|Mover pantalla braille a seguinte liña |T5|
|Levar á celda braille |Sensores|
|Activar actual navegador de obxectos |T3|
|Cambiar  a seguinte modo de revisión |F1|
|Mover a obxecto contedor |F2|
|Cambiar  a anterior modo de revisión |F3|
|Mover a obxecto anterior |F4|
|Anunciar obxecto actual |F5|
|Mover a obxecto seguinte |F6|
|Mover a obxecto enfocado |F7|
|Mover a primeiro obxecto contido |F8|
|Mover foco do sistema ou cursor a posición de revisión actual |F9|
|Anunciar posición do cursor de revisión |F0|
|conmutar o braille sigue a |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

O dispositivo SuperBraille, dispoñible principalmente en Taiwan, pode conectarse ou por USB ou por serie.
Como o SuperBraille non ten ningunha tecla física para escrebir ou botóns de desprazamento, toda a entrada debe facerse a través dun teclado estándar de computador.
Debido a esto, e para manter compatibilidade con outros lectores de pantalla en Taiwan, proporciónanse dúas combinacións de teclas para desprazamento da pantalla braille:
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar atrás pantalla braille |Menos teclado numérico|
|Desprazar adiante pantalla braille |Máis teclado numérico|

<!-- KC:endInclude -->

### Pantallas Eurobraille {#Eurobraille}

As pantallas b.book, b.note, Esys, Esytime e Iris de Eurobraille están admitidas polo NVDA.  
Estos dispositivos teñen un teclado braille con 10 teclas. 
Por favor consulta a documentación da pantalla para descripcións destas teclas.
Das dúas teclas colocadas como barra espaciadora, a tecla da esquerda correspóndese coa tecla retroceso e a tecla dereita coa barra espaciadora.

Estos dispositivos conéctanse mediante USB e teñen un teclado USB independente. 
É posible habilitar e deshabilitar este teclado conmutando "Simulación de Teclado HID" usando un xesto de entrada.
As funcións do teclado braille que se describen a continuación realízanse cando a "Simulación de teclado HID" está desactivada.

#### Funcións de Teclado Braille {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Borrar a última celda braille introducida ou carácter |`retroceso`|
|Transcribir calquera entrada braille e premer intro |`retroceso+espazo`|
|Conmutar tecla `NVDA` |`punto3+punto5+espazo`|
|`insert` |`punto1+punto3+punto5+espazo`, `punto3+punto4+punto5+espazo`|
|`suprimir` |`punto3+punto6+espazo`|
|`inicio` |`punto1+punto2+punto3+espazo`|
|`fin` |`punto4+punto5+punto6+espazo`|
|`frecha esquerda` |`punto2+espazo`|
|`frecha dereita` |`punto5+espazo`|
|`frecha arriba` |`punto1+espazo`|
|`frecha abaixo` |`punto6+espazo`|
|`rePáx` |`punto1+punto3+espazo`|
|`avPáx` |`punto4+punto6+espazo`|
|`1 teclado numérico` |`punto1+punto6+retroceso`|
|`2 teclado numérico` |`punto1+punto2+punto6+retroceso`|
|`3 teclado numérico` |`punto1+punto4+punto6+retroceso`|
|`4 teclado numérico` |`punto1+punto4+punto5+punto6+retroceso`|
|`5 teclado numérico` |`punto1+punto5+punto6+retroceso`|
|`6 teclado numérico` |`punto1+punto2+punto4+punto6+retroceso`|
|`7 teclado numérico` |`punto1+punto2+punto4+punto5+punto6+retroceso`|
|`8 teclado numérico` |`punto1+punto2+punto5+punto6+retroceso`|
|`9 teclado numérico` |`punto2+punto4+punto6+retroceso`|
|`Insert teclado numérico` |`punto3+punto4+punto5+punto6+retroceso`|
|`Punto Decimal teclado numérico` |`punto2+retroceso`|
|`dividir teclado numérico` |`punto3+punto4+retroceso`|
|`multiplicar teclado numérico` |`punto3+punto5+retroceso`|
|`menos teclado numérico` |`punto3+punto6+retroceso`|
|`máis teclado numérico` |`punto2+punto+punto+retroceso`|
|`intro teclado numérico` |`punto3+punto4+punto5+retroceso`|
|`escape` |`punto1+punto2+punto4+punto5+espazo`, `l2`|
|`tab` |`punto2+punto5+punto6+espazo`, `l3`|
|`shift+tab` |`punto2+punto3+punto5+espazo`|
|`imprimir pantalla` |`punto1+punto3+punto4+punto6+espazo`|
|`pausa` |`punto1+punto4+espazo`|
|`aplicacións` |`punto5+punto6+retroceso`|
|`f1` |`punto1+retroceso`|
|`f2` |`punto1+punto2+retroceso`|
|`f3` |`punto1+punto4+retroceso`|
|`f4` |`punto1+punto4+punto5+retroceso`|
|`f5` |`punto1+punto5+retroceso`|
|`f6` |`punto1+punto2+punto4+retroceso`|
|`f7` |`punto1+punto2+punto4+punto5+retroceso`|
|`f8` |`punto1+punto2+punto5+retroceso`|
|`f9` |`punto2+punto4+retroceso`|
|`f10` |`punto2+punto4+punto5+retroceso`|
|`f11` |`punto1+punto3+retroceso`|
|`f12` |`punto1+punto2+punto3+retroceso`|
|`windows` |`punto1+punto2+punto4+punto5+punto6+espazo`|
|Conmutar tecla `windows` |`punto1+punto2+punto3+punto4+retroceso`, `punto2+punto4+punto5+punto6+espazo`|
|`bloq mayus` |`punto7+retroceso`, `punto8+retroceso`|
|`bloq num` |`punto3+retroceso`, `punto6+retroceso`|
|`shift` |`punto7+espazo`|
|Conmutar `shift` |`punto1+punto7+espazo`, `punto4+punto7+espazo`|
|`control` |`punto7+punto8+espazo`|
|Conmutar `control` |`punto1+punto7+punto8+espazo`, `punto4+punto7+punto8+espazo`|
|`alt` |`punto8+espazo`|
|Conmutar `alt` |`punto1+punto8+espazo`, `punto4+punto8+espazo`|
|Conmutar simulación de teclado HID |`switch1Esquerda+joystick1Abaixo`, `switch1Dereita+joystick1Abaixo`|

<!-- KC:endInclude -->

#### Ordes de teclado b.book {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |`backward`|
|Desprazar pantalla braille cara adiante |`forward`|
|Mover ao foco actual |`backward+forward`|
|Ir a celda braille |`sensores`|
|`frecha esquerda` |`joystick2Esquerda`|
|`frecha dereita` |`joystick2dereita`|
|`frecha arriba` |`joystick2arriba`|
|`frecha abaixo` |`joystick2abaixo`|
|`intro` |`joystick2Centro`|
|`escape` |`c1`|
|`tab` |`c2`|
|Conmutar `shift` |`c3`|
|Conmutar `control` |`c4`|
|Conmutar `alt` |`c5`|
|Conmutar `NVDA` |`c6`|
|`control+Inicio` |`c1+c2+c3`|
|`control+fin` |`c4+c5+c6`|

<!-- KC:endInclude -->

#### Ordes de teclado b.note {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |`leftKeypadESquerda`|
|Desplazar pantalla braille cara adiante |`leftKeypadDereita`|
|Ir a celda braille |`sensores`|
|Anunciar formato de texto baixo a celda braille |`dobleSensor`|
|Moverse á seguinte liña en revisión |`leftKeypadAbaixo`|
|Cambiar a anterior modo de revisión |`leftKeypadEsquerda+leftKeypadArriba`|
|Cambiar a seguinte modo de revisión |`leftKeypadDereita+leftKeypadAbaixo`|
|`frecha esquerda` |`rightKeypadEsquerda`|
|`frecha dereitha` |`rightKeypadDereita`|
|`Frecha arriba` |`rightKeypadArriba`|
|`Frecha abaixo` |`rightKeypadAbaixo`|
|`control+inicio` |`rightKeypadEsquerda+rightKeypadArriba`|
|`control+fin` |`rightKeypadEsquerda+rightKeypadAbaixo`|

<!-- KC:endInclude -->

#### Ordes de teclado de Esys {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |`switch1Esquerda`|
|Desprazar pantalla braille cara adiante |`switch1Dereita`|
|Mover ao foco actual |`switch1Centro`|
|Ir a celda braille |`sensores`|
|Anunciar formato de texto baixo a celda braille |`doble sensores`|
|Mover á liña anterior en revisión |`joystick1Arriba`|
|Mover á seguinte liña en revisión |`joystick1Abaixo`|
|Mover ao carácter  anterior en revisión |`joystick1Esquerda`|
|Mover ao seguinte carácter en revisión |`joystick1Dereita`|
|`frecha esquerda` |`joystick2Esquerda`|
|`frecha dereita` |`joystick2Dereita`|
|`frecha arriba` |`joystick2Arriba`|
|`Frecha abaixo` |`joystick2Abaixo`|
|`intro` |`joystick2Centro`|

<!-- KC:endInclude -->

#### Ordes de teclado de Esytime {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |`l1`|
|Desprazar pantalla braille cara adiante |`l8`|
|Mover ao foco actual |`l1+l8`|
|Ir a celda braille |`sensores`|
|Anunciar formato de texto baixo a celda braille |`doble sensores`|
|Mover á liña anterior en revisión |`joystick1Arriba`|
|Mover á seguinte liña en revisión |`joystick1Abaixo`|
|Mover ao carácter anterior en revisión |`joystick1Esquerda`|
|Mover ao carácter seguinte en revisión |`joystick1Dereita`|
|`frecha esquerda` |`joystick2Esquerda`|
|`frecha dereita` |`joystick2Dereita`|
|`frecha arriba` |`joystick2Arriba`|
|`Frecha abaixo` |`joystick2Abaixo`|
|`intro` |`joystick2Centro`|
|`escape` |`l2`|
|`tab` |`l3`|
|Conmutar `shift` |`l4`|
|Conmutar `control` |`l5`|
|Conmutar `alt` |`l6`|
|Conmutar `NVDA` |`l7`|
|`control+inicio` |`l1+l2+l3`, `l2+l3+l4`|
|`control+fin` |`l6+l7+l8`, `l5+l6+l7`|
|Conmutar simulación de teclado HID |`l1+joystick1Abaixo`, `l8+joystick1Abaixo`|

<!-- KC:endInclude -->

### Pantallas Nattiq nBraille {#NattiqTechnologies}

O NVDA admite pantallas de [Nattiq Technologies](https://www.nattiq.com/) cando se conecten a través do USB.
Windows 10 e posteriores detectan as pantallas Braille unha vez conectadas, podes necesitar instalar controladores USB se usas versións vellas de Windows (anteriores a Win10).
Podes obtelos do sitio web do fabricante.

Seguidamente van as asignacións de teclas para pantallas Nattiq Technologies co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde poden atoparse esas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar pantalla braille cara atrás |arriba|
|Desprazar pantalla braille cara adiante |abaixo|
|Mover pantalla braille á liña anterior |esquerda|
|Mover pantalla braille á liña seguinte |dereita|
|Ir á celda braille |sensores|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.com/) é un programa por separado que pode utilizarse para soportar moitas pantallas braille.
Para utilizar esto, necesitas instalar [BRLTTY for Windows](https://www.brltty.com/download.html).
Deberías descargar e instalar o último paquete instalable, que se chamará, por exemplo, brltty-win-4.2-2.exe.
Cando configures a pantalla e porto a utilizar,  asegúrate de prestar gran atención ás instruccións, especialmente se estás utilizando unha pantalla USB e xa tes os controladores do fabricante instalados.

Para pantallas que teñan un teclado braille, BRLTTY actualmente manexa a entrada braille por si mesmo.
Polo tanto, a opción táboa braille de entrada de NVDA é irrelevante.

O BRLTYY non está involucrado na funcionalidade de detección automática de pantallas braille de NVDA.

Seguidamente van as asignacións a ordes BRLTTY para NVDA.
Por favor consulta as [listas de claves de vínculos de BRLTTY](http://mielke.cc/brltty/doc/KeyBindings/) para información acerca de como se mapean as ordes de BRLTTY para controlar as pantallas braille.
<!-- KC:beginInclude -->

| Nome |orde de BRLTTY|
|---|---|
|Desprazar pantalla braille cara atrás |fwinlt (vai á esquerda unha ventá)|
|Desprazar pantalla braille cara a dereita |fwinrt (vai unha ventá cara a dereita)|
|Mover a pantalla braille á liña anterior |lnup (vai unha liña cara arriba)|
|Mover pantalla braille á seguinte liña |lndn (vai unha liña cara abaixo)|
|Guiar á celda braille |route (leva o cursor ao caracter)|
|Conmutar entrada de axuda |learn (entra e sae do modo aprendizaxe de orde)|
|Abrir o menú NVDA |prefmenu (entra e sae do menú preferencias)|
|Revertir configuración |prefload (restaura as preferencias dende o disco)|
|Gardar configuración |prefsave (garda as preferencias no disco)|
|Anunciar hora |time (amosa a data e a hora actuais)|
|Falar a liña onde estea o cursor de revisión |say_line (fala a liña actual)|
|Falar todo usando o cursor de revisión |say_below (fala dende a liña actual ate o fondo da pantalla)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Os dispositivos Caiku Albatross, que foron fabricados por Tivomatic e están dispoñibles en Finlandia, poden conectarse ou por USB ou por serie.
Non necesitas ningún controlador en especial a instalar para usar estas pantallas.
Só enchufa a pantalla e configura ao NVDA para usala.

Nota: recoméndase encarecidamente unha velocidade de 19200 baudios.
Se se require, cambia o valor da opción de velocidade a 19200 baudios dende o menú do dispositivo braille.
Aíndaque o controlador admite unha velocidade de 9600 baudios, non ten xeito de controlar a velocidade que usa a pantalla.
Dado que 19200 é a velocidade en baudios predeterminada da pantalla, o controlador inténtao ao comezo.
Se as velocidades en baudios non son as mesmas, o controlador pode comportarse de xeito inesperado.

Seguidamente van as asignacións de teclas para estas pantallas co NVDA.
Por favor consulta a documentación da pantalla para descripcións de onde se atopan estas teclas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Moverse á liña superior en revisión |`inicio1`, `inicio2`|
|Moverse á liña inferior en revisión |`fin1`, `fin2`|
|Poñer o navegador de obxectos no foco actual |`eCursor1`, `eCursor2`|
|Moverse ao foco actual |`cursor1`, `cursor2`|
|Mover o punteiro do rato ao navegador de obxectos actual |`inicio1+inicio2`|
|poñer o navegador de obxectos no obxecto actual baixo o punteiro do rato e falalo |`fin1+fin2`|
|Mover o foco ao navegador de obxectos actual |`eCursor1+eCursor2`|
|Conmutar o seguemento do braille |`cursor1+cursor2`|
|Mover pantalla braille á liña anterior |`arriba1`, `arriba2`, `arriba3`|
|Mover pantalla braille á liña seguinte |`abaixo1`, `abaixo2`, `abaixo3`|
|Desprazar a pantalla braille cara atrás |`esquerda`, `lRodaEsquerda`, `rRodaEsquerda`|
|Desprazar a pantalla braille cara adiante |`dereita`, `lRodaDereita`, `rRodaDereita`|
|Ir á celda braille |`sensor`|
|Anunciar formato de texto baixo a celda braille |`sensor secundario`|
|Conmutar a forma de presentar a información de contexto en braille |`attributo1+attributo3`|
|Percorrer entre modos de voz |`attributo2+attributo4`|
|Cambiar ao modo de revisión anterior (por exemplo, obxecto, documento ou pantalla) |`f1`|
|Cambiar ao modo de revisión seguinte (por exemplo, obxecto, documento ou pantalla) |`f2`|
|Mover o navegador de obxectos ao obxecto que o contén |`f3`|
|Mover o navegador de obxectos ao primeiro obxecto dentro del |`f4`|
|Mover o navegador de obxectos ao obxecto anterior |`f5`|
|Mover o navegador de obxectos ao obxecto seguinte |`f6`|
|Anunciar o navegador de obxectos actual |`f7`|
|Anunciar información acerca da localización do texto ou obxecto no cursor de revisión |`f8`|
|Amosar opcións braille |`f1+inicio1`, `f9+inicio2`|
|Ler a barra de estado e mover o navegador de obxectos a ela |`f1+fin1`, `f9+fin2`|
|Percorrer as formas do cursor braille |`f1+eCursor1`, `f9+eCursor2`|
|Activar e desactivar o cursor braille |`f1+cursor1`, `f9+cursor2`|
|Percorrer os modos de amosar mensaxes braille |`f1+f2`, `f9+f10`|
|Percorrer os estados de amosar selección braille |`f1+f5`, `f9+f14`|
|Percorrer os estados "O braille move o cursor do sistema ao enrutar o cursor de revisión" |`f1+f3`, `f9+f11`|
|Realizar a ación predeterminada no navegador de obxectos actual |`f7+f8`|
|Anunciar data e hora |`f9`|
|Anunciar estado da batería e tempo restante se a alimentación non está enchufada |`f10`|
|Anunciar título |`f11`|
|Anunciar barra de estado |`f12`|
|Anunciar a liña actual baixo o cursor da aplicación |`f13`|
|Falar todo |`f14`|
|Anunciar o carácter actual baixo o cursor de revisión |`f15`|
|Anunciar a liña do navegador de obxectos actual onde estea situado o cursor de revisión |`f16`|
|Falar a palabra do navegador de obxectos actual onde  estea situado o cursor de revisión |`f15+f16`|
|Mover o cursor de revisión á liña anterior do navegador de obxectos actual e falala |`lRodaArriba`, `rRodaArriba`|
|Mover o cursor de revisión á seguinte liña do actual navegador de obxectos e falala |`lRodaAbaixo`, `rRodaAbaixo`|
|Tecla `Windows+d` (minimizar todas as aplicacións) |`attributo1`|
|Tecla `Windows+e` (este equipo) |`attributo2`|
|Tecla `Windows+b` (foco á bandexa do sistema) |`attributo3`|
|Tecla `Windows+i` (configuración de Windows) |`attributo4`|

<!-- KC:endInclude -->

### Pantallas HID Braille estándar {#HIDBraille}

Este é un controlador experimental para a nova Especificación Estándar HID Braille, acordada en 2018 por Microsoft, Google, Apple e varias empresas de tecnoloxía de asistencia, incluindo NV Access. 
A esperanza é que todos os futuros modelos de pantallas Braille creados por calquer fabricante, usen este protocolo estándar que eliminará a necesidade de controladores Braille específicos do fabricante.

A detección automática de pantallas braille do NVDA tamén recoñecerá calquera pantalla que soporte este protocolo.

Seguidamente van as asignacións de teclas actuales para estas pantallas.
<!-- KC:beginInclude -->

| Nome |Tecla|
|---|---|
|Desprazar a pantalla braille cara atrás |pan á esquerda ou balancín arriba|
|Desprazar a pantalla braille cara adiante |pan á dereita ou balancín abaixo|
|Levar á celda braille |conxunto de sensores de enrutamento 1||
|Alternar o seguemento de braille |arriba+abaixo|
|Tecla frecha arriba |joystick arriba, dpad arriba ou espazo+punto1|
|Tecla frecha abaixo |joystick cara abaixo, dpad cara abaixo ou espazo+punto4|
|Tecla frecha esquerda |espazo+punto3, joystick esquerdo ou dpad a esquerda||
|Tecla frecha dereita |espazo+punto6, joystick dereita ou dpad dereita|
|Teclas shift+tab |espazo+punto1+punto3|
|tecla tab |espazo+punto4+punto6|
|tecla alt |espazo+punto1+punto3+punto4 (espazo+m)|
|tecla escape |espazo+punto1+punto5 (espazo+e)|
|tecla intro |punto8, intro do joystick ou dpad intro|
|tecla windows |espazo+punto3+punto4|
|teclas alt+tab |espazo+punto2+punto3+punto4+punto5 (espazo+t)|
|Menú NVDA |espazo+punto1+punto3+punto4+punto5 (espazo+n)|
|teclas windows+d (minimizar todas as aplicacións) |espazo+punto1+punto4+punto5 (espazo+d)|
|Falar todo |espazo+punto1+punto2+punto3+punto4+punto5+punto6|

<!-- KC:endInclude -->

## Temas Avanzados {#AdvancedTopics}
### Modo Seguro {#SecureMode}

Os administradores do sistema poden configurar o NVDA para restrinxir o aceso  non autorizado ao sistema.
O NVDA permite a instalación de complementos persoalizados, os que poden executar código arbitrario, incluso cando o NVDA se eleva a privilexios de administrador.
O NVDA tamén permite aos usuarios executar código arbitrario a través da consola Python de NVDA.
O modo seguro de NVDA evita que os usuarios modifiquen a súa configuración e limita o acceso non autorizado ao sistema.

O NVDA corre en modo seguro cando se execute en [pantallas seguras](#SecureScreens), de non ser que o [parámetro de todo o sistema](#SystemWideParameters) `serviceDebug` estea activado.
Para forzar ao NVDA a que sempre arranque en modo seguro, pon o [parámetro para todo o sistema](#SystemWideParameters) `forceSecureMode`.
O NVDA tamén pode iniciarse en modo seguro coa [opción de liña de ordes](#CommandLineOptions) `-s`.

O modo seguro deshabilita:

* O gardado da configuración e outras opcións en disco
* O gardado do mapa de xestos en disco
* Características dos [perfís de configuración](#ConfigurationProfiles) como a creación, a eliminación, o renomeado de perfís etc.
* A carga de cartafois da configuración persoalizada usando [a opción de liña de ordes `-c`](#CommandLineOptions)
* A actualización do NVDA e a creación de copias portables
* A [Tenda de Complementos](#AddonsManager)
* A [consola de Python de NVDA](#PythonConsole)
* O [Visualizador do Rexistro](#LogViewer) e a autentificación
* O [Visualizador Braille](#BrailleViewer) e o [Visualizador de Voz](#SpeechViewer)
* Abrir documentos esternos dende o menú do NVDA, como a Guía do Usuario ou o ficheiro de contribuintes.

As copias instaladas do NVDA almacenan a súa configuración incluindo os complementos en `%APPDATA%\nvda`.
Para evitar que os usuarios do NVDA modifiquen a súa configuración ou complementos directamente, o seu aceso a este cartafol tamén debe estar restrinxido.

O modo seguro non é efectivo para copias portables do NVDA.
Esta limitación tamén se aplica á copia temporal do NVDA que se executa ao se lanzar o instalador.
En ambientes seguros, que un usuario poda correr un executable portable é o mesmo risco de seguridade independentemente do modo seguro.
Espérase que os administradores de sistemas restrinxan a execución de software non autorizado nos seus sistemas, incluidas as copias portables do NVDA.

Os usuarios do NVDA de cotío confían en configurar o seu perfil de NVDA para adaptalo ás sçúas necesidades.
Esto pode incluir a instalación e configuración de complementos persoalizados, que deberían ser examinados independentemente  de NVDA.
O modo seguro conxela os cambios na configuración do NVDA, así que por favor asegúrate de que o NVDA estea configurado adecuadamente antes de forzar o modo seguro.

### Pantallas Seguras {#SecureScreens}

O NVDA corre en [modo seguro](#SecureMode) cando se execute en pantallas seguras de non ser que o [parámetro de todo o sistema](#SystemWideParameters) `serviceDebug` estea habilitado.

Cando se execute dende unha pantalla segura, o NVDA usa un perfil do sistema para as preferencias.
As preferencias de usuario do NVDA poden copiarse [para utilizalas en pantallas seguras](#GeneralSettingsCopySettings).

As pantallas seguras inclúen:

* A pantalla de inicio de sesión de Windows
* O diálogo de Control de Acceso de Usuarios, activo cando se realice unha acción como administrador
  * Esto inclúe instalar programas

### Opcións de Liña de Ordes {#CommandLineOptions}

O NVDA pode aceptar unha ou máis opcións adicionais ao arrancar que alteren o seu comportamento.
Podes pasar tantas opcións como necesites.
Estas opcións poden pasarse ao arrancar dende un atallo de teclado (nas propiedades do atallo de teclado), dende o diálogo Executar(Menú Inicio -> Executar ou Windows+r) ou dende unha consola de ordes de Windows.
As opcións deberían separarse do nome do ficheiro executable do NVDA e de outras opcións por espazos.
Por exemplo, unha opción útil é --disable-addons, que di ao NVDA que suspenda todos os complementos en execución.
Esto permíteche determinar se un problema é causado por un complemento e recuperarte de problemas serios causados por complementos.

Como un exemplo, podes saír da copia actualmente en execución do NVDA introducindo o seguinte no diálogo Executar:

    nvda -q

Algunhas das opcións de liña de ordes teñen unha versión curta e unha longa, mentras outras só teñen unha versión longa.
Para aquelas que teñan unha versión curta, podes combinalas así:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Esto iniciará o NVDA con sons de arranque e a mensaxe desactivada, e a configuración especificada|
|`nvda -mc CONFIGPATH --disable-addons` |O mesmo que a de arriba, pero con complementos desactivados|

Algunhas das opcións de liña de ordes aceptan parámetros adicionais; ex.: cómo debería ser o grado de detalle do rexistro ou a vía para o directorio de configuración do usuario.
Esos parámetros deberían colocarse despois da opción, separados da opción por un espazo cando se utiliza a versión ou un signo igual (=) cando se utiliza  a versión longa; ex.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |di ao NVDA que se inicie co nivel de rexistro posto en depuración|
|`nvda --log-file=c:\nvda.log` |Di ao NVDA que escriba o seu rexistro en c:\nvda.log|
|`nvda --log-level=20 -f c:\nvda.log` |Di ao NVDA que inicie co nivel de rexistro posto en info e que escreba o seu  rexistro en c:\nvda.log|

Seguidamente van as opcións de liña de ordes para o NVDA:

| Curta |Longa |Descripción|
|---|---|---|
|`-h` |`--help` |Amosa a axuda en liña de ordes e sae|
|`-q` |`--quit` |Sae da copia que xa se estea a executar do NVDA|
|`-k` |`--check-running` |Informa se NVDA está en execución a través do código de saída; 0 se está en execución, 1 se non está en execución|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |O ficheiro onde se deberían escrebir as mensaxes do rexistro.  O rexistro sempre está desactivado se o modo seguro está habilitado.|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |O nivel máis baixo da mensaxe rexistrada (debug 10, input/output 12, debug warning 15, info 20, disabled 100). O rexistro está sempre deshabilitado se o modo seguro está habilitado.|
|`-c CONFIGPATH` |`--config-path=CONFIGPATH` |A ruta onde se almacenan todas as opcións do NVDA. O valor predeterminado fórzase se o modo seguro está habilitado.|
|`No` |`--lang=LANGUAGE` |Sobrescribe a lingua configurada do NVDA. Estabrece "Windows" para o usuario actual por defecto, "en" para Inglés, etc.|
|`-m` |`--minimal` |Sen sons, sen interface, sen mesaxe de inicio etc|
|`-s` |`--secure` |Inicia o NVDA en [Modo Seguro](#SecureMode)|
|`Non` |`--disable-addons` |Os complementos non terán efecto|
|`Non` |`--no-sr-flag` |Non cambia a bandeira global do sistema do lector de pantalla|
|`Non` |`--debug-logging` |Habilita o nivel de rexistro de depuración só para esta execución. Esta configuración sobreescribirá calquera outro nivel de rexistro ( --loglevel, -l) argumento dado, incluindo a opción non rexistro.|
|`Non` |`--no-logging` |Deshabilita o rexistro durante o uso do NVDA. Esta opción pode sobreescribirse se se especifica un nivel de rexistro ( --loglevel, -l) dende a liña de ordes ou se o rexistro de depuración está activado.|
|`Non` |`--install` |Instálase o NVDA comezando a nova copia instalada|
|`Non` |`--install-silent` |Instala en silenzo NVDA (Non comeza a nova copia instalada)|
|`Non` |`--enable-start-on-logon=True|False` |Ao instalar, habilita [arrancar na pantalla de inicio](#StartAtWindowsLogon) do NVDA|
|`Non` |`--copy-portable-config` |Ao instalar, copia a configuración portable dende a ruta proporcionada (--config-path, -c) á actual conta de usuario|
|`Non` |`--create-portable` |Crea unha copia portable do NVDA (comezando a copia recentemente creada). Require especificarse --portable-path|
|`Non` |`--create-portable-silent` |Crea unha copia portable do NVDA (non comeza a copia recentemente instalada). Require expecificarse --portable-path|
|`Non` |`--portable-path=PORTABLEPATH` |A ruta onde se creará unha copia portable|

### Parámetros do Sistema {#SystemWideParameters}

NVDA permite configurar algúns valores no rexistro do sistema que alteran o comportamento de todo o sistema do NVDA.
Estos valores almacénanse no rexistro do sistema baixo unha das seguintes claves:

* Sistema de 32 bits: "HKEY_LOCAL_MACHINE\SOFTWARE\nvda"
* Sistema de 64 bits: "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda"

Os seguintes valores poden configurarse baixo estas claves do rexistro:

| Nome |Tipo |Valores Posibles |Descripción|
|---|---|---|---|
|configInLocalAppData |DWORD |0 (predeterminado) para deshabilitado, 1 para habilitado |Se está habilitado, almacena a configuración do usuario do NVDA no cartafol local de datos de aplicación en lugar da roaming application data|
|serviceDebug |DWORD |0 (predeterminado) para deshabilitar, 1 para habilitar |Se se habilita, deshabilita o [Modo Seguro](#SecureMode) nas [pantallas segura](#SecureScreens).  do windows, permitindo o uso da consola de Python e do visualizador do Rexistro. Debido a varias implicacións importantes de seguridade, o uso desta opción está altamente desaconsellada|
|`forceSecureMode` |DWORD |0 (predeterminado) para deshabilitar, 1 para habilitar |Se está habilitado, forza [Modo Seguro](#SecureMode) para habilitarse ao executar o NVDA.|

## Información Adicional {#FurtherInformation}

Se requires información adicional ou asistencia referente ao NVDA, por favor visita o [sitio web do NVDA](NVDA_URL).
Aquí, podes atopar documentación adicional,  así como soporte técnico e recursos para a comunidade. 
Este sitio tamén proporciona información e recursos concernintes ao desenrolo do NVDA.
