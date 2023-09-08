Qué bi ha de Nuevo en o NVDA


%!includeconf: ../changes.t2tconf

= 2021.3 =
Ista versión introduz lo suporte pa la nueva especificación braille HID.
Ixa especificación pretende estandarizar lo suporte d'as linias braille sin a necesidat de controladors individuals.
Bi ha actualizacions pa lo eSpeak-NG y lo LibLouis, incluyindo tablas nuevas pa ruso y Tshivenda.
Los sons d'error pueden enchegar-sen en as compilacions estables d'o NVDA a traviés d'una opción nueva en as opcions abanzadas.
Charrar-lo tot en o Word agora desplaza la envista pa mantener vistera la posición actual.
Bi ha calders de milloras en utilizar l'Office con l'UIA.
Una d'as correccions de l'UIA ye que agora l'Outlook ignora mas tipos de tablas de disenyo en os mensaches.

Notas importants:

A causa d'una actualización d'o nuestro certificau de seguranza, un chico numero d'usuarios obtiene una error en que lo NVDA 2021.2 mira actualizacions.
Lo NVDA agora demanda a lo Windows que esvielle los certificaus de seguranza, lo que privará ixa error en o futuro.
Los usuarios afectaus habrán de descargar ista actualización a man.


== Nuevas Caracteristicas ==
- S'ha anyadiu un cenyo de dentrada pa commutar opcions pa anunciar lo estilo d'os cantos d'as celdas. (#10408)
- Suporte pa la nueva especificación HID braille que pretende estandarizar lo suporte pa las linias Braille. (#12523)
  - Lo NVDA autodetectará los dispositivos que admitan ixa especificación.
  - Pa mas detalles tecnicos sobre la implementación d'o NVDA d'ixa especificación, mira-te https://github.com/nvaccess/nvda/blob/master/devdocs/hidbrailletechnicalnotes.md
  -
- S'ha anyadiu lo suporte pa lo dispositivo braille VisioBraille Vario 4. (#12607)
- Se puet enchegar las notificacions d'error (opcions abanzadas) en que s'emplegue qualsiquier versión d'o NVDA. (#12672)
- En o Windows 10 y posteriors, lo NVDA anunciará lo recuento de sucherencias en introducir termins de busca en as aplicacions como la configuración y la Botiga de Microsoft. (#7330, #12758, #12790)
- La navegación por tablas ye agora compatible con os controls de quadricula creyaus por meyo d'o cmdlet Out-GridView en o PowerShell. (#12928)
-


== Cambeos ==
- Lo Espeak-ng s'ha esviellau ta 1.51-dev commit ``74068b91bcd578bd7030a7a6cde2085114b79b44``. (#12665)
- Lo NVDA emplegará por defecto lo eSpeak si no bi ha voces OneCore instaladas que admitan l'idioma preferiu en o NVDA. (#10451)
- Si las voces OneCore no charran con consistencia se torna a emplegar lo eSpeak como sintetizador. (#11544)
- En leyer la barra d'estau con ``NVDA+fin``, lo cursor de revisión ya no se mueve t'a suya localización.
Si te fa falta ixa funcionalidat por favor asigna un cenyo a lo script apropiau en a categoría de navegador d'obchectos en o dialogo de cenyos de dentrada. (#8600)
- En ubrir un quadro de dialogo d'opcions que ya estase ubierto, lo NVDA mete lo foco en o quadro de dialogo existent en cuenta de chenerar una error. (#5383)
- S'ha esviellau lo transcriptor braille liblouis ta [3.19.0 https://github.com/liblouis/liblouis/releases/tag/v3.19.0]. (#12810)
  - Nuevas tablas braille: Ruso grau 1, Tshivenda grau 1, Tshivenda grau 2
  -
- En cuenta de "conteniu marcau" u "mar", s'anunciará "resaltau" u "rsalt" pa la voz y lo braille respectivament. (#12892)
- Lo NVDA ya no mirará de salir-ne en que los dialogos sigan alguardando una acción reqiesta (eix.: Confirmar/cancelar). (#12984)
-


== Corrección d'errors ==
- Lo seguimiento d'as teclas modificaderas (como Control, u Ficar) ye mas robusto quan lo watchdog se siga recuperando. (#12609)
- Torna a estar posible comprebar las actualizacions d'o NVDA en bells sistemas; por eixemplo, en as instalacions limpias d'o Windows. (#12729)
- Lo NVDA anuncia correctament las celdas d'a tabla en blanco en o Microsoft Word quan s'emplega l'UI automation. (#11043)
- En as celdas d'a quadricula de datos ARIA en a web, la tecla d'escape agora se pasará t'a quadricula y ya no desenchegará lo modo de foco incondicionalment. (#12413)
- En leyer una celda de capitero d'una tabla en o Chrome, se corriche que lo nombre d'a columna s'anuncie dos veces. (#10840)
- Lo NVDA ya no informa d'una valor numerica pa los eslizadors UIA que tiengan definida una representación textual d'a suya valor. (Agora se prefiere UIA ValuePattern que no RangeValuePattern). (#12724)
- Lo NVDA ya no tracta la valor d'os eslizadors de UIA como si estase siempre percentual.
- La notificación d'a ubicación d'una celda en o Microsoft Excel quan s'accede a traviés de l'UI Automation torna a marchar correctament en o Windows 11. (#12782)
- Lo NVDA ya no estableix configuracions rechionals de Python no validas. (#12753)
- Si se desinstala un complemento desenchegau y se torna a instalar, se torna a enchegar. (#12792)
- S'ha correchiu las errors relacionadas con l'actualización y eliminación de complementos quan la carpeta de complementos s'haiga renombrau u tienga fichers ubiertos. (#12792, #12629)
- En utilizar l'UI automation pa acceder t'os controls d'as fuellas de calculo d'o Microsoft Excel, lo NVDA ya no anuncia de forma redundant quan se triga una sola celda. (#12530)
- Se leye automaticament mas texto de dialogo en o LibreOffice Writer, como en os dialogos de confirmación. (#11687)
- La lectura y navegación con o modo de navegación en o Microsoft Word a traviés de l'UI automation agora guarencia que lo documento siempre se desplace pa que la posición actual d'o modo de navegación siga vistera, y que la posición d'o cursor en o modo de foco refleixa correctament la posición d'o modo de navegación. (#9611)
- En rializar la función "Charrar-lo tot" en o Microsoft Word por meyo de l'UI automation, lo documento se desplaza automaticament y la posición d'o cursor s'esviella correctament. (#9611)
- Quan se leye correus electronicos en l'Outlook y lo NVDA ye accedendo t'o mensache con l'UI automation, bellas tablas se marcan agora como tablas de disenyo, lo que significa que ya no s'anunciarán por defecto. (#11430)
- S'ha correchiu una error poco freqüent en cambiar los dispositivos d'audio. (#12620)
- La dentrada con tablas braille literarias habría de comportar-se de forma mas fidable quan se tracta de campos d'edición. (#12667)
- En navegar por lo calandario d'a servilla d'o sistema d'o Windows, lo NVDA agora anuncia lo día d'a semana en a suya totalidat. (#12757)
- En utilizar un metodo de dentrada en chino como Taiwán - Microsoft Quick en o Microsoft Word, lo desplazamiento d'a linia braille enta debant y enta zaga ya no blinca incorrectament t'a posición orichinal d'o cursor. (#12855)
- En acceder ta documentos d'o Microsoft Word a traviés de l'UIA, torna a estar posible la navegación por frases (alt+flecha abaixo / alt+flecha alto). (#9254)
- En acceder t'o MS Word con l'UIA, agora s'anuncia la sangría d'os paragrafos. (#12899)
- En acceder t'o MS Word con l'UIA, agora s'anuncia la orden de seguimiento d'os cambeos y belatras ordens localizadas en o Word . (#12904)
- S'ha correchiu los duplicaus en braille y voz quan la 'descripción' coincida con o 'conteniu' u lo 'nombre'. (#12888)
- En o MS Word con l'UIA enchegau, bi ha una reproducción mas precisa d'os sons d'errors ortograficas mientras s'escribe. (#12161)
- En o Windows 11, lo NVDA ya no anunciará "panel" en pretar Alt+Tab pa cambiar de programa. (#12648)
- Lo nuevo panel lateral de seguimiento de comentarios modernos agora ye compatible con o MS Word quan no s'acceda t'o documento a traviés de l'UIA. Preta alt+f12 pa mover-te entre lo panel lateral de seguimiento y lo documento. (#12982)
-


== Cambeos pa los Desembolicadors ==
- Compilar lo NVDA agora requiere d'o Visual Studio 2019 16.10.4 u posterior.
Pa que coincida con l'entorno de compilación de producción, esviella lo Visual Studio pa que siga sincronizau con a [versión actual que AppVeyor ye emplegando https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019]. (#12728)
- ``NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable`` son estaus marcaus como obsoletos y s'eliminarán en 2022.1. (#12660)
  - En cuenta emplega ``apiLevel`` (mira-te los comentarios  en ``_UIAConstants.WinConsoleAPILevel`` pa mas detalles).
  -
- La transparencia d'a color de fundo d'o texto procedent d'as aplicacions GDI (a traviés d'o modelo de visualización), ye agora exposada pa los complementos u appModules. (#12658)
- ``LOCALE_SLANGUAGE``, ``LOCALE_SLIST`` y ``LOCALE_SLANGDISPLAYNAME`` s'han moviu t'o enum de ``LOCALE`` en languageHandler.
Encara son disponibles a libel de modulo, pero son obsoletos y s'eliminarán en o NVDA 2022.1. (#12753)
- L'uso d'as funcions ``addonHandler.loadState`` y ``addonHandler.saveState`` ha de substituyir-se por los suyos equivalents ``addonHandler.state.save`` y ``addonHandler.state.lobatz`` antis de 2022.1. (#12792)
- La salida braille agora se puet comprebar en prebas d'o sistema. (#12917)
-


= 2021.2 =
Ista versión introduz lo suporte preliminar pa lo Windows 11.
Encara que lo Windows 11 agún no ye estau lanzau, ista versión s'ha prebau en versions preliminars d'o Windows 11.
S'incluye una corrección important pa la Cortina de Pantalla (consulta Notas importants).
La ferramienta d'apanyo d'o rechistro COM agora puede resolver mas problemas en que s'executa lo NVDA.
Bi ha actualizacions pa lo sintetizador eSpeak y pa lo transcriptor braille LibLouis.
Tamién bi ha quantas correccions d'errors y milloras, en particular pa lo suporte de braille y pa las terminals d'o Windows, pa la calculadera, lo panel d'emoticonos y pa lo historial d'o portafuellas.


== Notas importants ==
A causa d'un cambio en l'API de magnificación d'o Windows, la Cortina de Pantalla habió d'estar esviellada pa admitir las versions mas nuevas d'o Windows.
Fe servir lo NVDA 2021.2 pa enchegar la Cortina de Pantalla con o Windows 10 21H2 (10.0.19044) u posteriors.
Ixo incluye lo Windows 10 Insiders y lo Windows 11.
Por razons de seguranza, en fer servir una versión nueva d'o Windows, obtiene una confirmación visual de que la Cortina de Pantalla fa que la pantalla siga negra de raso.


== Nuevas caracteristicas ==
- Suporte experimental pa anotacions ARIA:
  - S'anyade una orden pa leyer un resumen de detalles d'un obchecto con aria-details. (#12364)
  - S'anyade una opción en as preferencias abanzadas pa anunciar si un obchecto tien detalles en o modo de navegación. (#12439) 
  -
- En o Windows 10 Versión 1909 y posteriors (incluyindo lo Windows 11), lo NVDA anunciará lo recuento de sucherencias en rializar buscas en o Explorador de Fichers. (#10341, #12628)
- En o Microsoft Word, lo NVDA agora anuncia lo resultau d'os alcorces de sangría y sangría francesa en que s'executen. (#6269)
-


== Cambeos ==
- Lo Espeak-ng s'ha esviellau ta 1.51-dev commit ``ab11439b18238b7a08b965d1d5a6ef31cbb05cbb``. (#12449, #12202, #12280, #12568)
- Si s'enchega articlo en as preferencias d'usuario pa formatiau de documentos, lo NVDA anuncia "articlo" dimpués d'o conteniu. (#11103)
- S'ha esviellau lo transcriptor braille liblouis ta [3.18.0 https://github.com/liblouis/liblouis/releases/tag/v3.18.0]. (#12526)
  - Nuevas tablas braille: Bulgaro grau 1, Birmano grau 1, Birmano grau 2, Cazaco grau 1, Jemer grau 1, Kurdo nortenco grau 0, Sepedi grau 1, Sepedi grau 2, Sesotho grau 1, Sesotho grau 2, Setswana grau 1, Setswana grau 2, Tartaro grau 1, Vietnamita grau 0, Vietnamita grau 2, Vietnamita sudenco grau 1, Xhosa grau 1, Xhosa grau 2, Yakut grau 1, Zulú grau 1, Zulú grau 2
  -
- L'OCR d'o Windows 10 pasa a clamar-se OCR d'o Windows. (#12690)
-


== Corrección d'Errors ==
- En a Calculadera d'o Windows 10, lo NVDA anunciará las expresions d'a calculadera sobre la linia braille. (#12268)
- En os programas de terminal en o Windows 10 versión 1607 y posteriors, en ficar u eliminar caracters en o meyo d'una linia, ya no se leye los caracters a la dreita d'o cursor. (#3200)
  - Agora lo Diff Match Patch s'enchega por defecto. (#12485)
  -
- La dentrada braille marcha correctament con as siguients tablas contraitas: Arabe grau 2, Espanyol grau 2, Urdu grau 2, Chino (China, Mandarín) grau 2. (#12541)
- La Ferramienta d'apanyo d'o rechistro COM agora resuelve mas problemas, en especial en o Windows de 64 bit. (#12560)
- S'ha feito milloras pa lo maneyo de botons pa lo dispositivo braille Seika Notetaker de Nippon Telesoft. (#12598)
- S'ha feito milloras pa anunciar lo panel d'emoticonos d'o Windows y lo historial d'o portafuellas. (#11485)
- S'ha esviellau las descripcions d'os caracters de l'alfabeto Bengalí. (#12502)
- Lo NVDA sale de traza segura en que s'inicie un nuevo proceso. (#12605)
- Tornar a trigar lo controlador d'a linia braille Handy Tech dende lo dialogo de trigar una linia Braille ya no prevoca errors. (#12618)
- La versión de Windows 10.0.22000 u posterior se reconoix como Windows 11, no pas como Windows 10. (#12626)
- S'ha correchiu y prebau la compatibilidat d'a cortina de pantalla pa las versions d'o Windows dica la 10.0.22000. (#12684)
- Si no s'amuestra resultaus en filtrar los cenyos de dentrada, lo dialogo de configuración de cenyos de dentrada sigue marchando como s'asperaba. (#12673)
- S'ha correchiu un fallo en que lo primer elemento de menú d'un submenú no s'anuncia en qualques contextos. (#12624)
-


== Cambeos pa los Desembolicadors ==
- La constant ``characterProcessing.SYMLVL_`` habría de substituir-se fendo servir lo suyo equivalent ``SymbolLevel.`` antis d'o 2022.1. (#11856, #12636)
- ``controlTypes`` s'ha trestallau en quantos submodulos, los simbolos marcaus como esfasaus han de reemplazar-se antis d'o 2022.1. (#12510)
  - Las constants ``ROLE_`` y ``STATE_`` habrían de reemplazar-se por los suyos equivalents ``Role.`` y ``State.``.
  - Las constants ``roleLabels``, ``stateLabels`` y ``negativeStateLabels`` han quedau esfasadas, los usos tals como ``roleLabels[ROLE_]`` habrían de reemplazar-se por los suyos equivalents ``Role.*.displayString`` u ``State.*.negativeDisplayString``.
  - Las etiquetas ``processPositiveStates`` y ``processNegativeStates`` han quedau esfasadas pa la suya eliminación.
  -
- En o Windows 10 Versión 1511 y posterior (incluyindo compilacions Insider Preview), lo nombre actual d'a versión d'a caracteristica d'actualización d'o Windows s'obtién d'o Rechistro d'o Windows. (#12509)
- Esfasau: winVersion.WIN10_RELEASE_NAME_TO_BUILDS s'eliminará en o 2022.1, no bi'n ha un reemplazo dreito. (#12544)
-


= 2021.1 =
Ista versión inclui suporte experimental opcional pa l'UIA en l'Excel y los navegadors Chromium.
Bi ha correccions pa quantos idiomas y pa acceso t'os vinclos en braille.
Bi ha actualizacions pa l'Unicode CLDR, pa los simbolos matematicos y pa lo LibLouis.
Asinas como muitas atras correccions y milloras incluyindo-bi l'Office, lo Visual Studio y quantos idiomas.

Nota:
 - Ista versión creba la compatibilidat con os complementos existents.
 - Ista versión tamién deixa d'estar compatible con l'Adobe Flash.
 -
 

== Nuevas Caracteristicas ==
- Suporte preliminar pa l'UIA con os navegadors basaus en Chromium (como l'Edge). (#12025)
- Suporte experimental opcional pa lo Microsoft Excel a traviés de l'UI Automation. Nomás se recomienda pa lo Microsoft Excel compilación 16.0.13522.10000 u superior. (#12210)
- Navegación mas facil d'a salida en a Consola Python d'o NVDA. (#9784)
  - alt+alto/abaixo blinca t'o resultau anterior/siguient (anyade-bi mayus pa trigar-ne).
  - control+l borra lo panel de salida.
- Lo NVDA agora anuncia las categorías asignadas a una cita en o Microsoft Outlook si bi'n ha. (#11598)
- Suporte pa la linia braille de l'Anotador Electronico Seika de Nippon Telesoft. (#11514)


== Cambeos ==
- En o modo de navegación, los controls agora pueden activar-sen con os sensors de seguimiento braille sobre lo suyo descriptor (Eix.: "vnc" pa un vinclo). Ixo ye especialment util pa activar, por eixemplo, caixetas de verificación sin etiquetas. (#7447)
- Lo NVDA agora priva que l'usuario realice l'OCR d'o Windows 10 si la cortina de pantalla ye enchegada. (#11911)
- S'ha esviellau lo repositorio d'Unicode Common Locale Data (CLDR) ta 39.0. (#11943), #12314)
- S'ha anyadiu mas signos matematicos en o diccionario de simbolos. (#11467)
- La guida de l'usuario, lo fichero de cambios y lo listau de teclas d'ordens agora tienen un aspecto renovau. (#12027)
- Agora s'anuncia "no suportau" en mirar de cambiar lo disenyo d'a pantalla en as aplicacions que no l'admitan tals como lo Microsoft Word. (#7297)
- La opción de 'mirar de cancelar la voz pa los eventos d'o foco caducaus' en o panel d'opcions abanzadas agora ye enchegada por defecto. (#10885)
  - Ixe comportamiento se puede desenchegar configurando ista opción como "No".
  - Las aplicacions web (Eix.: lo Gmail) ya no verbalizan información obsoleta quan se mueva lo foco rapidament.
- S?ha esviellau lo transcriptor braille liblouis ta [3.17.0 https://github.com/liblouis/liblouis/releases/tag/v3.17.0]. (#12137)
  - Nuevas tablas braille: braille literario bielorruso, braille computerizau bielorruso, Urdu grau 1, Urdu grau 2.
- Lo suporte pa conteniu d'Adobe Flash s'ha eliminau d'o NVDA a causa que Adobe  desaconsella activament l'uso d'o Flash. (#11131)
- Lo NVDA saldrá mesmo con finestras encara ubiertas, lo proceso de salida agora zarra todas las finestras y dialogos d'o NVDA. (#1740)
- Lo Visor d'a Voz agora puede zarrar-se con ``alt+F4`` y tiene un botón estandar de zarrar pa una interacción mas facil con os usuarios de dispositivos sinyaladors. (#12330)
- Lo visor braille agora tiene un botón estandar de zarrar pa una interacción mas facil con usuarios de dispositivos sinyaladors. (#12328)
- En o quadro de dialogo de lista d'elementos, s'ha eliminau la tecla rapida d'o botón d'"activar" en qualques localizacions pa privar la colisión con a etiqueta d'o botón d'opción d'o tipo d'elemento. Quan siga disponible, lo botón sigue estando lo predeterminau d'o dialogo y, como tal, puede seguir estando invocau simplament pretando intro dende la propia lista d'elementos. (#6167)


== Corrección d'errors ==
- La lista de mensaches en l'Outlook 2010 torna a estar leyible. (#12241)
- En programas de terminal en o Windows 10 versión 1607 y posteriors, en ficar u eliminar caracters en meyo d'una linia, ya no se leyen los caracters a la dreita d'o cursor. (#3200)
  - ixa corrección experimental ha d'enchegar-se manualment en o panel d'opcions abanzadas d'o NVDA cambiando l'algorismo diff a Diff Match Patch.
- En o MS Outlook, ya no habría de producir-se un anunciau de distancia inadequada en que se faga mayus+tabulador dende lo cuerpo d'o mensache t'o campo d'afer. (#10254)
- En a consola de Python, agora s'admite la inserción d'un tabulador pa la sangría a lo prencipio d'una linia de dentrada no lasa y la rialización d'un tabulador en meyo d'una linia de dentrada. (#11532)
- La información d'o formato y atros mensaches navegables ya no presientan linias en blanco inasperadas quan lo disenyo de pantalla siga desenchegau. (#12004)
- Agora ye posible leyer comentarios en o MS Word con l'UIA enchegau. (#9285)
- S'ha amillorau lo rendimiento a lo interactuar con o Visual Studio. (#12171)
- S'ha correchiu errors graficas como la falta d'elementos en utilizar lo NVDA con un disenyo de dreita ta zurda. (#8859)
- Se respecta l'adreza d'a disposición d'a GUI basada en l'idioma d'o NVDA, no pas en a configuración rechional d'o sistema. (#638)
  - Problema conoixiu pa idiomas de dreita ta zurda: lo canto dreito d'os grupos se retalla con as etiquetas y controls. (#12181)
- La configuración rechional de Python s'estableix pa que coincida con l'idioma trigau en as preferencias de forma consistent, y ocurrirá en utilizar l'idioma por defecto. (#12214)
- TextInfo.getTextInChunks ya no se conchela quan se clame a controls d'edición enriquida como lo visor de rechistro de NVDA. (#11613)
- Torna a estar posible utilizar lo NVDA en idiomas que contiengan guións baixos en o nombre d'a configuración rechional, como de_CH, en o Windows 10 1803 y 1809. (#12250)
- En o WordPad, la configuración de l'anunciau de superindiz y subindiz funciona como s'asperaba. (#12262)
- Lo NVDA ya no falla en anunciar lo conteniu recientment enfocau en una pachina web si l'antigo foco desapareix y ye reemplazau por lo nuevo foco en a mesma posición. (#12147)
- Lo rayau, lo superindiz y lo subindiz d'as celdas enteras de l'Excel agora s'anuncian si la opción correspondient ye enchegada. (#12264)
- S'ha correchiu la copia d'a configuración entre la instalación dende una copia portatil quan lo directorio de configuración de destín por defecto ye laso. (#12071, #12205)
- S'ha correchiu l'anuncio incorrecto de qualques letras con accentos u diacriticos quan la opción de 'Decir mayus antis d'as mayusclas' ye marcada. (#11948)
- S'ha correchiu lo fallo de cambio de ton en o sintetizador de voz SAPI4. (#12311)
- L'instalador d'o NVDA agora tamién respecta lo parametro de linia de comandos ``--minimal`` y no reproduz lo son d'inicio, seguindo lo mesmo comportamiento documentau que un executable d'o NVDA instalau u con copia portable. (#12289)
- En o MS Word u l'Outlook, la tecla rapida de navegación d'a tabla agora puede blincar t'a tabla de disenyo si la opción d'"incluyir las tablas de disenyo" ye enchegada en a configuración d'o modo de navegación. (#11899)
- Lo NVDA ya no anunciará "↑↑↑" pa emojis en idiomas en particular. (#11963)
- Lo Espeak agora admite de nuevas lo cantonés y lo mandarín. (#10418)
- En o nuevo Microsoft Edge basau en Chromium los campos de texto tals como la barra d'adrezas agora s'anuncian quan sigan lasos. (#12474)
- S'ha correchiu lo controlador braille de Seika. (#10787)


== Cambios pa los Desembolicadors ==
- Nota: Ista ye una versión que creba la compatibilidat con l'API d'os complementos. Los complementos habrán de tornar a prebar-sen y actualizar lo suyo manifiesto.
- Lo sistema de compilación d'o NVDA agora obtiene todas las pendencias de Python con pip y las almagazena en un entorno virtual de Python. Tot ixo se fa de forma transparent.
  - Pa compilar lo NVDA, s'ha de seguir utilizando SCons d'a forma habitual. Por eixemplo, executando scons.bat en a radiz d'o repositorio. Executar ``py -m SCons`` ya no s'admite, y ``scons.py`` tamién s'ha eliminau.
  - Pa executar lo NVDA dende lo codigo fuent, en cuenta d'executar ``source/nvda.pyw`` dreitament, lo desembolicador agora ha d'utilizar ``runnvda.bat`` en a radiz d'o repositorio. Si se mira d'executar ``source/nvda.pyw``, un quadro de mensache te alvertirá que ixo ya no s'admite.
  - Pa rializar prebas unitarias, executa ``rununittests.bat [<extra unittest discover options>]>]``.
  - Pa rializar prebas d'o sistema: executa ``runsystemtests.bat extra robot options>]``
  - Pa rializar linting, executa ``runlint.bat <base branch>`.
  - Por favor, mira-te lo fichero readme.md pa mas detalles.
- Tamién s'ha esviellau las siguients pendencias de Python:
  - Lo comtypes s'ha esviellau ta 1.1.8.
  - Lo pySerial s'ha esviellau ta 3.5.
  - Lo wxPython s'ha esviellau ta 4.1.1.
  - Lo Py2exe s'ha esviellau ta 0.10.1.0.
- S'ha eliminau ``LiveText._getTextLines``. (#11639)
  - En cuenta, sobrescribe ``_getText`` que torna una cadena de tot lo texto de l'obchecto.
- Los obchectos ``LiveText`` agora pueden calcular las diferencias por caracter. (#11639)
  - Pa alterar lo comportamiento d'as diferencias pa bell obchecto, sobrescribe la propiedat ``diffAlgo`` (mira-te lo docstring pa mas detalles).
- En definir un script con o decorador de script, se puede especificar l'argumento booleano 'allowInSleepMode' pa controlar si un script ye disponible en modo de suspensión u no pas. (#11979)
- S'ha eliminau las siguients funcions d'o modulo de configuración. (#11935)
  - canStartOnSecureScreens - utiliza config.isInstalledCopy en cuenta.
  - hasUiAccess y execElevated - utiliza-las dende lo modulo systemUtils.
  - getConfigDirs - utiliza globalVars.appArgs.configPath en cuenta.
- Las constants Module level REASON_* s'han eliminau de controlTypes - utiliza en cuenta controlTypes.OutputReason. (#11969)
- S'ha eliminau REASON_QUICKNAV de browseMode - utiliza controlTypes.OutputReason.QUICKNAV en cuenta. (#11969)
- La propiedat ``NVDAObject`` (y derivaus) agora torna estrictament la clase Enum ``controlTypes.IsCurrent``. (#11782)
  - La propiedat ``isCurrent`` ya no ye Opcional, y por tanto no tornará cosa.
    - Quan un obchecto no siga actual, se torna ``controlTypes.IsCurrent.NO``.
- S'ha eliminau l'asignación ``controlTypes.isCurrentLabels``. (#11782)
  - En cuenta, utiliza la propiedat ``displayString`` en una valor d'o enum ``controlTypes.IsCurrent``. EG ``controlTypes.IsCurrent.YES.displayString``
    - Eix.: ``controlTypes.IsCurrent.YES.displayString``
- S'ha eliminau ``winKernel.GetTimeFormat`` - s'ha d'utilizar ``winKernel.GetTimeFormatEx``. 
- S'ha eliminau ``winKernel.GetDateFormat`` - s'utiliza ``winKernel.GetDateFormatEx`` en cuenta. (#12139)
- S'ha eliminau ``gui.DriverSettingsMixin`` - utiliza ``gui.AutoSettingsMixin``. (#12144)
- S'ha eliminau ``speech.getSpeechForSpelling`` - utiliza ``speech.getSpellingSpeech``. (#12145)
- Los comandos no se pueden importar dreitament dende speech como ``import speech; speech.ExampleCommand()`` u ``import speech.manager; speech.manager.ExampleCommand()`` - utiliza ``from speech.commands import ExampleCommand`` en cuenta. (#12126)
- ``speakTextInfo`` ya no ninviará la voz a traviés de ``speakWithoutPauses`` si lo motivo ye ``SAYALL``, ya que ``SayAllHandler`` lo fa agora manualment. (#12150)
- Lo modulo ``synthDriverHandler`` ya no s'importa por defecto en ``globalCommands`` y ``gui.settingsDialogs`` - utiliza ``from synthDriverHandler import synthFunctionExample`` en cuenta. (#12172)
- S'ha eliminau ``ROLE_EQUATION`` de controlTypes - utiliza ``ROLE_MATH`` en cuenta. (#12164)
- S'ha eliminau las clases ``autoSettingsUtils.driverSetting`` de ``driverHandler`` - utiliza-las dende ``autoSettingsUtils.driverSetting``. (#12168)
- S'ha eliminau las clases ``autoSettingsUtils.utils`` de ``driverHandler`` - por favor, utiliza-las dende ``autoSettingsUtils.utils``. (#12168)
- S'ha eliminau lo suporte d'os ``TextInfo`` que no heredan de ``contentRecog.BaseContentRecogTextInfo``. (#12157)
- S'ha eliminau ``speech.speakWithoutPauses`` - por favor, utiliza ``speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses`` en cuenta. (#12195, #12251)
- S'ha eliminau ``speech.re_last_pause`` - por favor, utiliza ``speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause`` en cuenta. (#12195, #12251)
- Los dialogos ``WelcomeDialog``, ``LauncherDialog`` y ``AskAllowUsageStatsDialog`` s'han tresladau ta ``gui.startupDialogs``. (#12105)
- S'ha moviu ``getDocFilePath`` de ``gui`` t'o modulo ``documentationUtils``. (#12105)
- Lo modulo gui.accPropServer, asinas como las clases AccPropertyOverride y ListCtrlAccPropServer d'o modulo gui.nvdaControls s'han eliminau en favor d'o suporte nativo de WX pa anular las propiedatz d'accesibilidat. En amillorar l'accesibilidat d'os controls WX, implementa wx.Accessible en cuenta. (#12215)
- Los fichers en ``source/comInterfaces/`` son agora mas facilment consumibles por las ferramientas de desembolique, como los IDE. (#12201)
- S'ha anyadiu metodos y tipos convenients a lo modulo winVersion pa obtener y comparar versions d'o Windows. (#11909)
  - S'ha eliminau la función isWin10 que se trobaba en o modulo winVersion.
  - La clase winVersion.WinVersion ye un tipo comparable y ordenable que encapsula la información d'a versión d'o Windows.
  - S'ha anyadiu la función winVersion.getWinVer pa obtener una winVersion.WinVersion que represiente lo sistema operativo que se ye executando actualment.
  - S'ha anyadiu constants de conveniencia pa las versions conoixidas d'o Windows, se veiga winVersion.WIN* constants.
- IAccessibleHandler ya no importa de forma estelar tot lo de las interficies IAccessible y IA2 COM - por favor, utiliza-las dreitament. (#12232)
- Los obchectos TextInfo tienen agora propiedatz d'inicio y fin que pueden comparar-sen matematicament con operadors como < <= == != >= >. (#11613)
  - Por eixemplo, ti1.start <= ti2.end
  - Agora se prefiere ixe uso en cuenta de ti1.compareEndPoints(ti2, "startToEnd") <= 0
- Las propiedatz d'inicio y fin de TextInfo tamién pueden establir-sen entre ell. (#11613)
  - Por eixemplo, ti1.start = ti2.end
  - Se prefiere ixe uso en cuenta de ti1.SetEndPoint(ti2, "startToEnd")
- S'elimina ``wx.CENTRE_ON_SCREEN`` y ``wx.CENTER_ON_SCREEN``, en cuenta s'utiliza ``self.CentreOnScreen()``. (#12309)
- S'ha eliminau ``easeOfAccess.isSupported``, lo NVDA nomás admite versions d'o Windows en as qualas s'avalúa como ``True``. (#12222)
- S'ha moviu ``sayAllHandler`` ta ``speech.sayAll``. (#12251)
  - ``speech.sayAll.SayAllHandler`` exposa las funcions ``stop``, ``isRunning``, ``readObjects``, ``readText``, ``lastSayAllMode``.
  - Lo comando ``SayAllHandler.stop`` tamién reinicia la instancia ``SayAllHandler`` ``SpeechWithoutPauses``.
  - S'ha substituyiu ``CURSOR_REVIEW`` y ``CURSOR_CARET`` por ``CURSOR.REVIEW`` y ``CURSOR.CARET``.
- S'ha moviu ``speech.SpeechWithoutPauses`` ta ``speech.speechWithoutPauses.SpeechWithoutPauses``. (#12251)
- S'ha cambeau lo nombre de ``speech.curWordChars`` ta ``speech._curWordChars``. (#12395)
- s'ha eliminau de ``speech`` y se puede acceder ta ellas a traviés de ``speech.getState()``. Agora son valors nomás de lectura. (#12395)
  - speechMode
  - speechMode_beeps_ms
  - beenCanceled
  - isPaused
- pa actualizar ``speech.speechMode`` emplega ``speech.setSpeechMode``. (#12395)
- s'ha moviu lo siguient ta ``speech.SpeechMode``. (#12395)
  - ``speech.speechMode_off`` se convierte en ``speech.SpeechMode.off``.
  - ``speech.speechMode_beeps`` pasa a estar ``speech.SpeechMode.beeps``
  - speechMode_talk" pasa a estar "speech.Speech.SpeechMode.talk".
- ``IAccessibleHandler.IAccessibleObjectIdentifierType`` ye agora ``IAccessibleHandler.types.IAccessibleObjectIdentifierType``. (#12367)
- Han cambeau ``NVDAObjects.UIA.WinConsoleUIA`` (#12094)
  - ``NVDAObjects.UIA.winConsoleUIA.is21H1Plus`` s'ha renombrau como ``NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable``.
  - ``NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo`` s'ha renombrau como lo nombre d'a clase d'inicio en mayusclas.
  - ``NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1`` s'ha renombrau como ``NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive``
    - La implementación marcha en totz dos estando incluyius los puntos finals (en rangos de texto) antis de [microsoft/terminal PR 4018 https://github.com/microsoft/terminal/pull/4018]
    - Solucions pa ``expand``, ``collapse``, ``compareEndPoints``, ``setEndPoint``, etc


= 2020.4 =
Ista versión inclui metodos nuevos de dentrada de chinés, una actualización d'o Liblouis y la Lista d'Elementos (NVDA+f7) agora marcha en o modo de foco.
L'aduya sensible a lo contexto agora ye disponible en pretar F1 en dialogos d'o NVDA.
Milloras pa las reglas de pronuncia de simbolos, diccionarios d'a fabla, mensaches braille y lectura superficial.
Corrección d'errors y milloras pa Mail, Outlook, Teams, Visual Studio, Azure Data Studio, Foobar2000.
En a web, bi ha milloras pa lo Google Docs y muito millor suporte pa l'ARIA.
Mas muitas atras importants correccions d'errors  y milloras.

== Nuevas Caracteristicas ==
- En pretar F1 adintro d'os dialogos d'o NVDA agora s'ubrirá lo fichero d'aduya pa la sección mas relevant. (#7757)
- Suporte pa l'autocompletau de sucherencias (IntelliSense) en o Microsoft SQL Server Management Studio mas Visual Studio 2017 y superiors. (#7504)
- Pronuncia de simbolos: suporte pa agrupacions en una definición de simbolos compleixa y suporte de referencias de grupo en una regla de substitución que los fa mas sencillos y mas poderosos. (#11107)
- Agora se notifica a los usuarios en que intenten creyar dentradas de diccionarios d'a fabla con substitucions invalidas d'expresions regulars. (#11407)
  - Especificament agora se detecta errors d'agrupación.
- S'ha anyadiu lo suporte pa los nuevos metodos de dentrada pa lo chinés tradicional rapido y pa lo Pinyin en o Windows 10. (#11562)
- Los capiters de pestanya agora se consideran campos de formulario con a tecla de navegación rapida f. (#10432)
- S'ha anyadiu un comando pa commutar l'anunciau d'o texto marcau (resaltau); No bi ha garra cenyo asociau por defecto. (#11807)
- S'ha anyadiu lo parametro de linia de comandos --copy-portable-config que te permite copiar automaticament la configuración furnida a la cuenta d'usuario en que s'instala lo NVDA en silencio. (#9676)
- Agora s'admite lo enrutamiento Braille con o visualizador braille pa usuarios de churi, desplazando-se pa enrotar ta una celda braille. (#11804)
- Lo NVDA agora detectará automaticament los dispositivos Humanware Brailliant BI 40X y 20X a traviés d'USB y Bluetooth. (#11819)


== Cambios ==
- S'ha esviellau lo transcriptor braille liblouis t'a versión 3.16.1
- S'aborda multiples penchadas
- S'anyade la tabla braille grau 1 de baskir
- S'anyade la tabla braille copto computerizau de 8 puntos.
- S'anyade tablas de braille literario ruso y braille literario ruso (detallau)
- S'anyade la tabla de braille Africano grau 2
- S'elimina la tabla braille rusa de grau 1.
- En leyer con leyer-lo tot en o modo de navegación, los comandos de buscar lo siguient y l'anterior no aturan la lectura si la opción de permitir la lectura superficial ye enchegada; leyer-lo tot reprene a partir de dimpués d'o termin siguient u anterior trobau. (#11563)
- Pa las linias braille HIMS s'ha remapiau F3 ta Espacio + puntos 148. (#11710)
- Milloras pa lo UX d'as opcions "Tiempo d'aspera d'o mensache braille" y "amostrar los mensaches indefinidament". (#11602)
- En navegadors web y atras aplicacions que suporten lo modo de navegación, lo dialogo de lista d'elementos (NVDA+F7) agora puede clamar-se en estar en o modo de foco. (#10453)
- Las actualizacions d'as rechions ARIA live agora se suprimen quan se desenchegue l'anunciau d'os cambios en o conteniu dinamico. (#9077)
- Lo NVDA agora anunciará "copiau en o portafuellas" antis d'o texto copiau. (#6757)
- S'ha amillorau la presentación d'a tabla d'envistas graficas en o chestor de discos. (#10048)
- Las etiquetas d'os controls agora son desenchegadas (en griso) quan lo control ye desenchegau. (#11809)
- S'ha esviellau l'anotación emoji de CLDR t'a versión 38. (#11817)
- La funcionalidat incorporada de "resaltau d'o foco" s'ha renombrau ta "resaltau visual". (#11700)


== Corrección d'errors ==
- Lo NVDA torna a marchar correctament con os campos d'edición en utilizar l'aplicación Fast Log Entry. (#8996)
- S'anuncia lo tiempo transcorriu en Foobar2000 si no se disposa d'un tiempo total (por eixemplo, en que se reproduz bella transmisión en dreito). (#11337)
- Lo NVDA agora respecta l'atributo aria-roledescription en os elementos en conteniu editable en as pachinas web. (#11607)
- Ya no s'anuncia 'lista' en cada linia d'una lista en o Google Docs u belatro conteniu editable en o Google Chrome. (#7562)
- En navegar con as flechas por caracters u parolas dende un elemento de lista ta unatro en o conteniu editable en a web, agora s'anuncia la dentrada en o nuevo elemento de lista. (#11569)
- Lo NVDA agora leye la linia correcta quan lo cursor se cala en o final d'un vinclo en o final d'un elemento de lista en o Google Docs u belatro conteniu editable en a web. (#11606)
- En o Windows 7, en ubrir u zarrar lo menú d'inicio dende lo escritorio agora se mete lo foco correctament. (#10567)
- En activar lo "intentar cancelar los eventos d'o foco asperaus", lo titol d'a pestanya agora s'anuncia unatra vez en cambiar las pestanyas en o Firefox. (#11397)
- Lo NVDA ya no falla en anunciar un elemento de lista dimpués d'escribir un caracter en una lista en que se charra con as voces Ivona SAPI5 . (#11651)
- Ye posible de nuevas emplegar lo modo de navegación en leyer correus electronicos en o Windows 10 Mail 16005.13110 y posteriors. (#11439)
- En que s'use las voces  Ivona SAPI5 dende harposoftware.com, lo NVDA agora ye capaz d'alzar la configuración, cambiar de sintetizador y ya no se quedará en silencio dimpués de reenchegar-se. (#11650)
- Agora ye posible ficar lo numero 6 en braille computerizau dende un teclau braille en as linias HIMS. (#11710)
- Milloras importants en o rendimiento en Azure Data Studio. (#11533, #11715)
- Con o "intentar cancelar la voz pa los eventos d'o foco expiraus" enchegau lo titol d'o dialogo mirar d'o NVDA s'anuncia de nuevo. (#11632)
- Lo NVDA ya no habría de chelar-se en que se dispierte l'ordinador y lo foco aterrice en un documento d'o Microsoft Edge. (#11576)
- Ya no ye menester pretar lo tabulador u mover lo foco dimpués de zarrar un menú de contexto en o MS Edge pa que lo modo de navegación torne a estar funcional de nuevas. (#11202)
- Lo NVDA ya no falla en leyer elementos en envistas de lista dentro d'una aplicación de 64 bits tal como Tortoise SVN. (#8175)
- Los ARIA treegrids agora s'exposan como tablas normals en o modo de navegación tanto en o Firefox como en o Chrome. (#9715)
- Agora se puede empecipiar una busca inversa con 'buscar l'anterior' a traviés de NVDA+mayus+F3 (#11770)
- Un script de NVDA ya no se considera repetiu si ocurre una pretada de tecla no relacionada entre las dos execucions d'o script. (#11388) 
- Puede tornar-se a suprimir l'anunciau d'as etiquetas strong y emphasis en l'Internet Explorer desenchegando l'anunciar l'enfasi en as opcions de formatiau de documentos d'o NVDA. (#11808)
- Ya no habría de producir-se una cheladura de quantos segundos experimentau por una chicota cantidat d'usuarios en pasar entre las celdas de l'Excel. (#11818)
- En as compilacions de Microsoft Teams con numers de versión como 1.3.00.28xxx, NVDA ya no falla en leyer mensaches en os chats u en as canals de Teams a causa d'un menú enfocau incorrectament. (#11821)
- Lo NVDA anunciará apropiadament como error ortografica y gramatical Lo texto marcau de vez como error ortografica y gramatical en o Google Chrome. (#11787)
- En emplegar l'Outlook (localización t'o francés), l'alcorce pa "Responder a totz" (control+mayus+R) torna a marchar. (#11196)
- En o Visual Studio, los consellos d'a ferramienta IntelliSense que furnen detalles adicionals sobre l'elemento IntelliSense trigau actualment nomás s'anuncian una vez. (#11611)
- En a calculadera d'o Windows 10, lo NVDA no anunciará lo progreso d'os calculos si se desenchega lo verbalizar los caracters en escribir-los. (#9428)
- Lo NVDA ya no se bloca en que s'utilice l'anglés grau 2 d'Estaus unius y se desancha ta braille computerizau en que siga sobre lo cursor en amostrar bell conteniu como una URL en braille. (#11754)
- Torna a estar posible anunciar información de formato pa la celda enfocada de l'Excel fendo servir NVDA+F. (#11914)
- La dentrada QWERTY en as linias braille de Papenmeier que lo suportan torna a marchar y ya no causa que lo NVDA se chele aliatoriament. (#11944)


== Cambios pa los Desembolicadors ==
- Las prebas de sistema agora pueden ninviar teclas utilizando spy.emulateKeyPress, que prene un identificador de tecla que s'achusta a los propios nombres de tecla d'o NVDA y por defecto tamién la bloca dica que s'execute l'acción. (#11581)
- Lo NVDA ya no requiere que lo directorio actual siga lo directorio de l'aplicación NVDA pa marchar. (#6491)
- La opción aria live politeness pa rechions vivas agora puede trobar-se en obchectos d'o NVDA que fagan servir la propiedat liveRegionPoliteness. (#11596)
- Agora ye posible definir cenyos deseparaus pa los documentos de l'Outlook y d'o Word. (#11196)


= 2020.3 =
Ista versión incluye quantas grans milloras pa la estabilidat y lo rendimiento, especialment en as aplicacions d'o Microsoft Office. Bi ha nuevas opcions pa commutar lo suporte d'as pantallas tactils y de l'anunciau d'os graficos.
La existencia de conteniu marcau (resaltau) puede anunciar-se en os navegadors, y bi ha nuevas tablas braille alemanas.

== Nuevas Caracteristicas ==
- Agora puetz conmutar l'anunciau d'os graficos dende las opcions de Formatiau de Documentos d'o NVDA.  Tiene en cuenta que desenchegando ista opción encara leyerá lo texto alternativo d'os graficos. (#4837)
- Agora puetz commutar lo suporte de pantallas tactils d'o NVDA. S'ha anyadiu una opción a lo panel d'interacción tactil d'as opcions d'o NVDA. Lo cenyo predeterminau ye NVDA+control+alt+t. (#9682)
- S'ha anyadiu nuevas tablas braille pa l'alemán. (#11268)
- Lo NVDA agora detecta controls de texto de nomás lectura de UIA. (#10494)
- La existentcia de conteniu marcau (resaltau) s'informa tanto en voz como en braille en totz los navegadors web. (#11436)
 - Ixo puede enchegar-se y desenchegar-se con una nueva opción de formatiau de documento d'o NVDA pa resaltau.
- Se puede anyadir nuevas teclas a lo sistema de teclau emulau dende lo dialogo de cenyos de dentrada d'o NVDA. (#6060)
  - Pa fer-lo, preta lo botón d'anyadir dimpués que haigas seleccionau la categoría de teclas de sistema de teclau emulau.
- Agora se suporta la Handy Tech Active Braille con ceprén. (#11655)
- Agora la opción "modo de foco Automatico pa lo movimiento d'o cursor" ye compatible con lo desenchegau de "meter lo foco Automaticament a los elementos enfocables". (#11663)


== Cambios ==
- Lo programa d'anunciar lo formato (NVDA+f) agora s'ha cambiau pa anunciar lo formato en o cursor d'o sistema en cuenta d'en a posición d'o cursor de revisión.  Pa anunciar lo formato en a posición d'o Cursor de Revisión agora emplega NVDA+mayus+f. (#9505)
- Lo NVDA ya no mete automaticament lo foco d'o sistema en os elementos enfocables por defecto en o modo de navegación, amillorando lo rendimiento y la estabilidat. (#11190)
- S'ha esviellau lo CLDR dende la versión 36.1 t'a versión 37. (#11303)
- S'ha esviellau lo eSpeak-NG ta 1.51-dev, commit 1fb68ffffea4
- Agora puetz fer servir la navegación de tablas en os quadros de lista con elementos de lista marcables quan una lista en particular tienga quantas columnas. (#8857)
- En l'administrador de complementos, en que se te pregunte por confirmar la eliminación de bell complemento, agora  "No", ye lo predeterminau. (#10015)
- En o Microsoft Excel, lo dialogo de lista d'elementos agora presienta formulas en a suya forma localizada. (#9144)
- Lo NVDA agora anuncia la terminolochía correcta pa las notas en o MS Excel. (#11311)
- En fer servir la orden "mover lo cursor de revisión t'o foco" en o modo de navegación, lo cursor de revisión agora se mete en a posición d'o cursor virtual. (#9622)
- La información anunciada en o modo de navegación, como la información de formato con NVDA+F, s'amuestra agora en una finestra licherament mas gran centrada en a pantalla. (#9910)


== Corrección d'Errors ==
- Lo NVDA agora charra siempre en navegar por parolas y aterriza en qualsiquier simbolo seguiu por un espacio en blanco, qualsiquiera que sigan las opcions de verbosidad. (#5133)
- En las aplicacions que fagan servir lo QT 5.11 u mas modernas, las descripcions d'os obchectos s'anuncian unatra vez. (#8604)
- En eliminar una parola con control+suprimir, lo NVDA ya no remaneix en silencio. (#3298, #11029)
  - Agora s'anuncia la parola a la dreita d'a eliminada.
- En o panel d'opcions chenerals, la lista d'idiomas agora s'ordena correctament. (#10348)
- En o dialogo de cenyos de Dentrada, s'ha amillorau significativament lo rendimiento mientras se filtra. (#10307)(
- Agora puetz ninviar caracters Unicode dillá d'U+FFFF dende una linia braille. (#10796)
- Lo NVDA anunciará dialogo ubierto Con conteniu en l'actualización de mayo de 2020 d'o Windows 10. (#11335)
- Una opción nueva experimental en as opcions abanzadas (enchegar lo rechistro selectivo pa eventos y cambios de propiedat de l'UI Automation) puede furnir mayors milloras de rendimiento en o Microsoft Visual Studio y atras aplicacions basadas en l'UIAutomation d'enchegar-se. (#11077, #11209)
- Pa los elementos marcables de listas, lo estau trigau ya no s'anuncia redundantment, y si ye aplicable, s'anuncia lo estau desmarcau en cuenta. (#8554)
- En l'actualización de mayo d'o 2020 d'o Windows 10, lo NVDA agora amuestra lo Mapiador de Son de Microsoft en revisar los dispositivos de salida dende lo dialogo de sintetizador. (#11349)
- En l'Internet Explorer, los numers agora s'anuncian correctament pa las listas ordenadas si la lista no prencipia con 1. (#8438)
- En o Google chrome, lo NVDA agora anunciará no marcau pa totz los controls marcables (no nomás caixetas de verificación) que actualment no sigan marcaus. (#11377)
- Unatra vez ye posible navegar por quantos controls quan l'idioma de NVDA siga meso en aragonés. (#11384)
- Lo NVDA ya no habría de chelar-se a veces en o Microsoft Word en mover rapidament las flechas alto y abaixo u en escribir caracters con o Braille enchegau. (#11431, #11425, #11414)
- Lo NVDA ya no anyade un espacio no existent en l'arrociegue en copiar lo navegador d'obchectos actual en o portafuellas. (#11438)
- Lo NVDA ya no enchega lo perfil de leyer-lo tot si no bi ha cosa que leyer. (#10899, #9947)
- Lo NVDA ya no ye incapaz de leyer la lista de caracteristicas en l'administrador Internet Information Services (IIS). (#11468)
- Lo NVDA agora mantiene lo dispositivo d'audio ubierto amillorando lo rendimiento en qualques tarchetas de son (#5172, #10721)
- Lo NVDA ya no se chelará ni s'amortará en que mantiengas preto control+mayus+flecha abaixo en o Microsoft Word. (#9463)
- Agora lo NVDA siempre anuncia Lo estau desplegau/plegau d'os directorios en l'arbol de navegación de drive.google.com. (#11520)
- Lo NVDA detectará automaticament la linia braille NLS eReader Humanware a traviés de Bluetooth, ya que lo suyo nombre Bluethooth ye agora "NLS eReader Humanware". (#11561)
- Grans milloras en o rendimiento de Visual Studio Code. (#11533)


== Cambios pa los Desembolicadors ==
- Lo GUI Helper'#s BoxSizerHelper.addDialogDismissButtons suporta una nueva parola clau d'argumento "separated", pa anyadir un separador horizontal estandard a los dialogos (que no sigan mensaches y dialogos de dentrada simples). (#6468)
- S'ha anyadiu propiedatz adicionals a los app modules, incluyindo la rota pa l'executable (appPath), ye una app d'almagazenamiento d'o Windows (isWindowsStoreApp), y arquitectura de maquina pa la app (appArchitecture). (#7894)
- Agora ye posible creyar app modules pa apps hospedadas adintro de wwahost.exe en o Windows 8 y posteriors. (#4569)
- Agora se puede delimitar un fragmento d'o rechistro y dimpués copiar-lo en o portafuellas fendo servir NVDA+control+mayus+F1. (#9280)
- Los obchectos especificos d'o NVDA que lo replegador de vasuera ciclica d'o Python troba por agora se rechistran en que lo replegador los borra pa aduyar en a eliminación d'os ciclos de referencia d'o NVDA. (#11499)
 - La mayoría d'as clases de NVDA se rastreyan incluyindo NVDAObjects, appModules, GlobalPlugins, SynthDrivers, y TreeInterceptors.
 - Una clase que cal rastriar ha d'heredar de garbageHandler.TrackedObject.
- Lo rechistro de depuración significativo pa los eventos de MSAA agora puede enchegar-se en a configuración abanzada d'o NVDA. (#11521)
- Los eventos de MSAA pa l'obchecto enfocau actualment ya no se filtran de conchunta con atros eventos si se sobreix la cuenta d'eventos pa un filo determinau. (#11520)


= 2020.2 =
Lo resinyable d'ista versión inclui lo suporte d'una nueva linia braille de Nattiq, un suporte millor pa la interficie grafica d'usuario d'o antivirus ESET y la Terminal de Windows, milloras de rendimiento de 1Password y con o sintetizador Windows OneCore. Amás de muitas atras importants milloras y correccions d'errors.

== Nuevas Caracteristicas ==
- Suporte pa nuevas linias braille:
  - Nattiq nBraille (#10778)
- S'ha anyadiu un programa pa ubrir lo directorio de configuración d'o NVDA (sin cenyo predeterminau). (#2214)
- Millor suporte pa la interficie grafica d'usuario d'o antivirus ESET. (#10894)
- S'ha anyadiu suporte pa la Terminal d'o Windows. (#10305)
- S'ha anyadida un comando pa anunciar lo perfil de configuración activo (sin cenyo predeterminau). (#9325)
- S'ha anyadiu un comando pa enchegar y desenchegar l'anunciau de subindices y superindices (sin cenyo predeterminau). (#10985)
- Las aplicacions web (p. eix. lo Gmail) ya no charran información incorrecta quan se mueva lo foco rapedament. (#10885)
  - Ixa solución experimental ha d'enchegar-se manualment a traviés d'a opción d'intentar cancelar la voz pa los eventos d'enfoque acotolaus  en o panel d'opcions abanzadas.
- S'ha anyadiu mas simbolos a lo diccionario de simbolos predeterminau. (#11105)


== Cambios ==
- S'ha esviellau lo transcriptor braille liblouis de 3.12 ta [3.14.0 https://github.com/liblouis/liblouis/releases/tag/v3.14.0] (from 3.12.0). (#10832, #11221)
- L'anunciau de superindices y subindices agora se controla por deseparau a l'anunciau d'atributos d'a fuent. (#10919)
- A causa de cambios feitos en o VS Code, lo NVDA ya no desenchega lo modo de navegación en Code por defecto. (#10888)
- Lo NVDA ya no anuncia los mensaches "cobalto" y "cobaixo" en mover lo cursor de revisión dreitament t'a primer u zaguer linia de l'actual navegador d'obchectos con os programas de mover lo cursor de revisión t'alto u t'abaixo respectivament. (#9551)
- Lo NVDA ya no anuncia los mensaches "cucha" y "dreita" en mover lo cursor de revisión dreitament t'o primer u zaguer caracter de l'actual navegador d'obchectos con os programas de mover lo cursor de revisión t'a zurda u t'a dreita respectivament. (#9551)


== Corrección d'Errors ==
- Lo NVDA agora ranca correctament quan lo fichero de rechistro no se puet creyar. (#6330)
- En as versions recients d'o Microsoft Word 365, lo NVDA ya no anunciará "borrar la parola de dezaga" en que se prete control+recule mientras s'edita un documento. (#10851)
- En o Winamp, lo NVDA torna a anunciar lo estau d'aliatorio u de repetir. (#10945)
- Lo NVDA ya no ye extremadament lento en mover-te dentro d'a lista d'elementos en 1Password. (#10508)
- Lo sintetizador de voz Windows OneCore ya no tiene retardo entre las frases. (#10721)
- Lo NVDA ya no se chela en ubrir lo menú  de contexto pa 1Password en l'aria de notificacions d'o sistema. (#11017)
- En l'Office 2013 y anteriors:
  - Las cintas s'anuncian quan lo foco se mueva ta ellas por primer vez. (#4207)
  - Los elementos d'o menú de contexto tornan a anunciar-sen apropiadament. (#9252)
  - Las seccions d'as cintas s'anuncian consistentment en navegar con control+flechas. (#7067)
- En o modo de navegación en o Mozilla Firefox y lo Google Chrome, lo texto ya  no amaneix incorrectament en una linia deseparada quan lo conteniu web emplega en o CSS display: inline-flex. (#11075)
- En o modo de navegación con o foco automatico d'o sistema configurau a elementos enfocables desenchegau, agora ye posible enchegar elementos que no sigan enfocables.
- En o modo de navegación con o foco automatico d'o sistema configurau a elementos enfocables desenchegau, agora ye posible enchegar elementos adubibles pretando la tecla tabulador. (#8528)
- En o modo de navegación con o foco automatico d'o sistema configurau a elementos enfocables desenchegau, enchegar bells elementos ya no fa clic en un puesto incorrecto. (#9886)
- Ya no s'escuita los sons d'error d'o NVDA en acceder ta controls de texto de DevExpress. (#10918)
- Los consellos d'os iconos en a servilla d'o sistema ya no s'anuncian en navegar con o teclau si lo suyo texto ye igual a lo suyo nombre, pa privar un anunciau duplicau. (#6656)
- En o modo de navegación con o foco automatico d'o sistema configurau a elementos enfocables desenchegau, cambear t'o modo de foco con NVDA+espacio agora enfoca l'elemento baixo lo cursor. (#11206)
- Torna a estar posible mirar actualizacions d'o NVDA en bells sistemas. p. eix. en as instalacions limpias d'o Windows. (#11253)
- Lo foco no se mueve en una aplicación Java quan la selección se cambie en un arbol, tabla u lista no enfocable. (#5989)


== Cambios pa los Desembolicadors ==
- execElevated y hasUiAccess se son movius d'o modulo  config t'o modulo systemUtils. La utilización a traviés d'o modulo config ye obsoleta. (#10493)
- S'ha esviellau lo configobj ta 5.1.0dev commit f9a265c4. (#10939)
- Agora ye posible la comprebación automatizada d'o NVDA con o Chrome y un eixemplo HTML. (#10553)
- Lo IAccessibleHandler s e ye convertiu en un paquet, l'OrderedWinEventLimiter se ye extraito ta un modulo y s'ha anyadiu prebas d'unidat (#10934)
- S'ha esivellau lo BrlApi t'a versión 0.8 (BRLTTY 6.1). (#11065)
- La recuperación d'a barra d'estau agora puet estar personalizada por un AppModule. (#2125, #4640)
- Lo NVDA ya no escuita a lo IAccessible EVENT_OBJECT_REORDER. (#11076)
- Un ScriptableObject esmarchinau (tal como un GlobalPlugin que pierda una clamada a la suya clase base ' metodo __init__ ) ya no creba lo maneyo de programas d'o NVDA. (#5446)


= 2020.1 =
Lo resinyable d'ista versión inclui l'admisión de quantas nuevas linias braille de HumanWare y d'APH, mas muitas atras correccions importants de fallos tals como la capacidat de leyer de nuevo matematicas en o Microsoft Word fendo servir lo MathPlayer y lo MathType.

== Nuevas Caracteristicas ==
- L'elemento actualment trigau en quadros de lista se presienta atra vez en o modo de navegación en o Chrome, semellant a NVDA 2019.1. (#10713)
- Agora puetz fer clics con o botón dreito d'o churi en dispositivos tactils tocando con un dido y mantenendo-lo. (#3886)
- Suporte pa linias braille nuevas: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, y NLS eReader. (#10830)


== Cambeos ==
- Lo NVDA privará que lo sistema se bloque u se suspenda quan siga leyendo-lo tot. (#10643)
- Suporte pa iframes difuera de proceso en o Mozilla Firefox. (#10707)
- S'ha esviellau lo transcriptor braille liblouis t'a versión 3.12. (#10161)


== Corrección d'errors ==
- S'ha correchiu lo no anunciau d'o simbolo Unicode menos (U+2212) (#10633)
- En instalar complementos dende l'administrador de complementos los nombres d'os fichers y carpetas en a finestra d'exploración ya no s'anuncian dos veces. (#10620, #2395)
- En o Firefox, en cargar Mastodon con a interficie de web abanzada enchegada, agora todas las cronolochías se procesan correctament en modo de navegación. (#10776)
- En o modo de navegación, lo NVDA agora anuncia "no marcau" pa caixetas de verificación no marcadas que no lo i feba en ocasions anteriorment. (#10781)
- Los controls ARIA switch ya no anuncian información trafuquera tal como "no pretau marcau" u "pretau marcau". (#9187)
- Las voces SAPI4 ya no habrían de refusar charrar cierto texto. (#10792)
- Lo NVDA puede leyer y interactugar de nuevas con equacions matematicas en o Microsoft Word. (#10803)
- Lo NVDA anunciará unatra vez lo texto que se deseleccione en o modo de navegación si se preta una flecha mientras lo texto se triga. (#10731).
- Lo NVDA ya no sale si bi ha una error inicializando lo eSpeak. (#10607)
- Las errors causadas por unicode en traduccions pa alcorces ya no aturan l'instalador, fizconiadas por la tornada t'o texto en anglés. (#5166, #6326)
- Lo feito de salir  d'as listas y tablas en Leyer-lo tot con a lectura superficial enchegada ya no anuncia de contino la salida d'a lista u tabla. (#10706)


== Cambeos pa los Desembolicadors ==
- Agora se compila la documentación pa lo desembolicador fendo servir lo Sphinx. (#9840)
- S'ha trestallau en dos quantas funcions d'a fabla. (#10593)
 La versión speakX remaneix, pero agora pende en una función getXSpeech la quala torna una seqüencia de voz.
  - speakObjectProperties agora se basa en getObjectPropertiesSpeech
  - speakObject agora se basa en getObjectSpeech
  - speakTextInfo agora se basa en getTextInfoSpeech
  - speakWithoutPauses s'ha convertiu en una clase, y s'ha refactorizau, pero no habría de crebar la retrocompatibilidad.
  - getSpeechForSpelling ye obsoleta (encara que agún disponible) fendo servir getSpellingSpeech en o suyo puesto.
  Cambeos privaus que no habrían d'afectar a los desembolicadors de complementos:
  - _speakPlaceholderIfEmpty agora ye _getPlaceholderSpeechIfTextEmpty
  - _speakTextInfo_addMath agora ye _extendSpeechSequence_addMathForTextInfo
- Speech 'reason' s'ha convertiu en un Enum, Consulta la clase controlTypes.OutputReason. (#10703)
  - Las constants Module level 'REASON_' son obsoletas.
- Las pendencias de compilación d'o NVDA agora requieren lo Visual Studio 2019 (16.2 u mas recient). (#10169)
- S'ha esviellau lo SCons t'a versión 3.1.1. (#10169)
- Se torna a permitir a behaviors._FakeTableCell no tener una localización definida (#10864)


= 2019.3 =
Lo NVDA 2019.3 ye una versión bien significativa que contién a saber-los cambios en o nuclio incluindo l'esvielle d'o Python 2 t'o Python 3, y una reescritura mayor d'o subsistema de fabla d'o NVDA.
Anque ixos cambios creban la compatibilidat con os complementos mas antigos d'o NVDA, l'esvielle t'o Python 3 ye menester por seguridat, y los cambios en a fabla permiten bellas innovacions emocionants en o futuro cercano.
Atras cosas resinyables en ista versión incluyen lo suporte de 64 bits pa las maquinas virtuals d'o Java, la cortina de pantalla y la funcionalidat de resalte d'o foco, suporte pa mas linias braille y un nuevo visor d'o braille, y muitismas atras correccions d'errors.

== Nuevas Caracteristicas ==
- S'ha amillorau la precisión d'o comando pa mover lo churi t'o navegador d'obchectos en os campos de texto en as aplicacions Java. (#10157)
- S'ha anyadiu lo suporte pa las siguients linias braille d'Handy Tech (#8955):
 - Basic Braille Plus 40
 - Basic Braille Plus 32
 - Connect Braille
- Agora se puet eliminar totz los cenyos definius por l'usuario  a traviés d'un nuevo botón "Restablir las valors predeterminadas de fabrica" en o quadro de dialogo de cenyos de dentrada. (#10293)
- L'anunciau d'a fuent en o Microsoft Word agora inclui si lo texto se marca como amagau. (#8713)
- S'ha anyadiu un comando pa mover lo cursor de revisión t'a posición achustada anteriorment como marca de prencipio d'a selección u copia: NVDA+mayus+F9. (#1969)
- En l'Internet Explorer, lo Microsoft Edge y versions recients d'o Firefox y lo Chrome, las rechions agora s'anuncian en o modo de foco y en o navegador d'obchectos. (#10101)
- En l'Internet Explorer, lo Google Chrome y lo Mozilla Firefox, agora puetz navegar por articlos y grupos fendo servir los programas de navegación rapeda. Ixos programas no son vinculaus por defecto y pueden asignar-sen en o dialogo de cenyos de dentrada en ubrir lo dialogo dende un documento en o modo de navegación. (#9227)
- Agora s'anuncia las figuras. Se consideran obchectos y, por tanto, navegables con a tecla de navegación rapeda o.
- En l'Internet Explorer, lo Google Chrome y lo Mozilla Firefox, agora s'anuncia los articlos con o navegador d'obchectos, y opcionalment, en o modo de navegación si s'ha activau en as opcions de formatiau de documentos. (#10424)
- S'ha anyadiu una Cortina de Pantalla que, en activar-se, fa que toda la pantalla se torne negra en o Windows 8 y posteriors. (#7857)
 - S'ha anyadiu un programa pa enchegar la cortina de pantalla (dica lo siguient renchegue con una sola pretada, u siempre mientras lo NVDA siga en execución con dos pretadas), no se i asigna garra cenyo predeterminau.
 - Puet enchegar-se y configurar-se a traviés d'a categoría 'visión' en o dialogo d'opcions d'o NVDA.
- S'ha anyadiu a lo NVDA la funcionalidat de resaltau de pantalla. (#971, #9064)
 - Lo resaltau d'o foco, d'o navegador d'obchectos y d'a posición d'o cursor d'o modo de navegación puet enchegar-se y configurar-se a traviés d'a categoría 'visión' en o dialogo d'opcions d'o NVDA.
 - Nota: Ixa caracteristica ye incompatible con o complemento focus highlight, manimenos, lo complemento encara puet emplegar-se mientras lo resaltador incorporau siga desenchegau.
- S'ha anyadiu la ferramienta visualizador d'o braille, que permite veyer la salida braille a traviés d'una finestra sobre la pantalla. (#7788)


== Cambios ==
- La Guida de l'Usuario agora describe cómo fer servir lo NVDA en a consola d'o Windows. (#9957)
- La execución de nvda.exe agora ye predeterminada pa reemplazar una copia ya en execución d'o NVDA. Lo parametro de linia de comandos -r|--replace encara s'accepta, pero s'ignora. (#8320)
- En o Windows 8 y posteriors, lo NVDA agora anunciará la información de nombre d'o producto y de versión pa las aplicacions nativas tals como las aplicacions descargadas d'a Botiga de Microsoft fendo servir información furnida por l'aplicación. (#4259, #10108)
- En activar y desactivar los cambios de seguimiento con o teclau d'o Microsoft Word, lo NVDA anunciará lo estau d'a configuración. (#942) 
- Lo numero de versión d'o NVDA agora se rechistra como lo primer mensache en o rechistro. Ixo ocurre mesmo si s'ha desenchegau lo rechistro dende la Interficie Grafica d'Usuario. (#9803)
- Lo dialogo d'opcions ya no permite cambiar lo libel d'o rechistro configurau si s'ha substituiu dende la linia de comandos. (#10209)
- En o Microsoft Word, lo NVDA agora anuncia lo estau de visualización d'os caracters no imprimibles en pretar l'alcorce commutable Ctrl+mayus+8. (#10241)
- Sh'a esviellau lo transcriptor braille Liblouis t'a confirmación 58d67e63. (#10094)
- Quan l'anunciau de caracters CLDR (incluyindo los emoticonos) siga enchegau, s'anuncia en os libels de toda la puntuación. (#8826)
- Los paquetz python de tercers incluyius en o NVDA como comtypes, agora rechistran las suyas alvertencias y errors en o rechistro d'o NVDA. (#10393)
- S'ha esviellau l'Unicode Common Locale Data Repository emoji annotations t'a versión 36.0. (#10426)
- En enfocar un grupo en o modo de navegación, agora tamién se leye la descripción. (#10095)
- Agora s'inclui lo Java Access Bridge con o NVDA pa permitir l'acceso a aplicacions Java, mesmo pa maquinas Java de 64 bits. (#7724)
- Si lo Java Access Bridge no ye enchegau pa l'usuario, lo NVDA l'enchega automaticament en rancar. (#7952)
- S'ha esviellau lo eSpeak-NG ta 1.51-dev, confirmación ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)


== Corrección d'errors ==
- Los Emoticonos y atros caracters unicode de 32 bits agora ocupan menos espacio en as linias braille quan s'amuestran como valors hexadecimals. (#6695)
- En o Windows 10, lo NVDA anunciará los consellos d'as aplicacions universals si lo NVDA se configura pa anunciar los consellos en o dialogo de presentación d'obchectos. (#8118)
- En o Windows 10 versión 1607 y posteriors, agora s'anuncia lo texto escrito en Mintty. (#1348)
- En o Windows 10 versión 1607 y posteriors, la salida en a consola d'o Windows que amaneixca amán d'o cursor ya no se letreya. (#513)
- Los controls en o dialogo compresor de l'Audacity agora s'anuncian en navegar por ell. (#10103)
- Lo NVDA ya no tracta los espacios como parolas en revisión d'obchectos en editors basaus en o Scintilla tals como lo Notepad++. (#8295)
- Lo NVDA privará que lo sistema dentre en o modo adurmient en desplazar-se por lo texto con cenyos d'a linia braille. (#9175)
- En o Windows 10, lo braille agora seguirá en editar conteniu de celdas en o Microsoft Excel y en atros controls de texto UIA en do se quedaba dezaga. (#9749)
- Lo NVDA tornará a anunciar las sucherencias en a barra d'adreza d'o Microsoft Edge. (#7554)
- Lo NVDA ya no se silencia en que s'enfoque bell control de capitero de pestanya HTML en l'Internet Explorer. (#8898)
- En o Microsoft Edge basau en EdgeHTML, lo NVDA ya no reproducirá lo son de sucherencia de busca en maximizar la finestra. (#9110, #10002)
- Los quadros combinaus d'ARIA 1.1 agora s'admiten en o Mozilla Firefox y en o Google Chrome. (#9616)
- Lo NVDA ya no anunciará lo conteniu d'as columnas visualment amagau  pa los elementos de lista en controls SysListView32. (#8268)
- Lo dialogo d'opcions ya no amuestra "info" como lo libel de rechistro actual quan se siga en o modo seguro. (#10209)
- En o menú inicio d'o Windows 10 Anniversary Update y posteriors, lo NVDA anunciará los detalles d'os resultaus d'a busca. (#10232)
- En o modo de navegación, si en mover lo cursor u en emplegar la navegación rapeda se produz bell cambio en o documento, lo NVDA ya no charra conteniu incorrecto en qualques casos. (#8831, #10343)
- S'ha correchiu qualques nombres de viñetas en o Microsoft Word. (#10399)
- En l'actualización de mayo de 2019 d'o Windows 10 y posteriors, lo NVDA anunciará unatra vez lo primer emoticono u elemento d'o portafuellas trigau en que s'ubra lo panel d'emoticonos y lo historial d'o portafuellas respectivament. (#9204)
- En o Poedit, torna a estar posible veyer qualques traduccions pa los idiomas de dreita ta zurda. (#9931)
- En l'aplicación de configuración de l'actualización d'abril de 2018 d'o Windows 10 y posteriors, lo NVDA ya no anunciará la información d'as barras de progreso d'os mesuradors de volumen que se troba en a pachina de sistema/Son. (#10284)
- Las expresions regulars invalidas en os diccionarios d'a fabla ya no aturan de raso la voz en o NVDA. (#10334)
- En que se leye elementos con viñetas en o Microsoft Word con l'UIA activau, la viñeta d'o siguient elemento d'a lista ya no s'anuncia de traza inadequada. (#9613)
- S'ha resuelto qualques problemas raros de transcripción braille y errors con o liblouis. (#9982)
- Las aplicacions Java enchegadas antis que no lo NVDA agora son accesibles sin a necesidat de renchegar l'aplicación Java. (#10296)
- En o Mozilla Firefox, quan l'elemento enfocau se marca como actual (aria-current), ixe cambio ya no se charra quantas veces. (#8960)
- Lo NVDA agora tractará bells caracters de composición unicode tals como e-acute como un solo caracter en mover-se por lo texto. (#10550)
- Agora se suporta lo Spring Tool Suite Versión 4. (#10001)
- No se diz lo nombre por duplicau quan l'aria-labelledby relation target ye un elemento interior. (#10552)
- En o Windows 10 versión 1607 y posteriors, los caracters escritos dende teclaus Braille se charran en mas situgacions. (#10569)
- En cambiar lo dispositivo de salida d'audio, los tons reproducius por lo NVDA agora se reproducirán por lo dispositivo recientment trigau. (#2167)
- En o Mozilla Firefox, mover lo foco en o modo de navegación ye mas rapedo. Ixo fa que mover lo cursor en o modo de navegación siga mas achil en muitos casos. (#10584)


== Cambios pa los Desembolicadors ==
- S'ha esviellau lo Python ta 3.7. (#7105)
- S'ha esviellau lo pySerial t'a versión 3.4. (#8815)
- S'ha esviellau lo wxPython ta 4.0.3 pa suportar lo Python 3.5+ (#9630)
- S'ha esviellau lo six t'a versión 1.12.0 (#9630)
- S'ha esviellau lo py2exe t'a versión 0.9.3.2 (en desembolique, confirmación b372a8e d'albertosottile/py2exe#13). (#9856)
- S'ha esviellau lo modulo comtypes de l'UIAutomationCore.dll t'a versión 10.0.18362. (#9829)
- Lo completau con tabulación en a consola d'o Python nomás suchiere atributos que prencipien con un guión baixo si lo guión baixo s'escribe antis. (#9918)
- La ferramienta Flake8 s'ha integrau con o SCons pa reflectar los requisitos d'o codigo pa Pull Requests. (#5918)
- Como lo NVDA ya no pende de modulos pyWin32, tals como lo win32api y lo win32con ya no son disponibles pa los complementos. (#9639)
 - Las clamadas a win32api pueden reemplazar-sen con clamadas directas a funcions win32 dll a traviés de ctypes.
 - Las constants win32con habrían de definir-sen en os tuyos fichers.
- L'argumento "async" en o nvwave.playWaveFile se ye renombrau como "asynchronous". (#8607)
- ya no s'admite Los metodos speakText y speakCharacter en os obchectos synthDriver.
 - Ixa funcionalidat se maneya con SynthDriver.speak.
- s'ha eliminau Las clases SynthSetting en synthDriverHandler. Agora emplega las clases driverHandler.DriverSetting en cuenta.
- Las clases SynthDriver ya no habrían d'exposar indices a traviés d'a propiedat lastIndex.
 - En cuenta, habrían de notificar  l'acción synthDriverHandler.synthIndexReached con l'indiz, una vez que tot l'audio anterior siga rematau de reproducir-se antis d'ixe indiz.
- Las clases SynthDriver agora han de notificar l'acción synthDriverHandler.synthDoneSpeaking, una vez que tot l'audio d'una clamada a SynthDriver.speak siga rematau de reproducir-se.
- Las clases SynthDriver han d'admitir speech.PitchCommand en o suyo metodo speak, ya que los cambios en o ton d'a fabla d'o letreyo agora penden d'ixa funcionalidat.
- La función de fabla getSpeechTextForProperties se ye renombrada como getPropertiesSpeech. (#10098)
- La función de braille getBrailleTextForProperties se ye renombrada como getPropertiesBraille. (#10469)
- S'ha cambiau quantas funcions d'a fabla pa tornar seqüencias de fabla. (#10098)
 - getControlFieldSpeech
 - getFormatFieldSpeech
 - getSpeechTextForProperties clamada agora getPropertiesSpeech
 - getIndentationSpeech
 - getTableInfoSpeech
- Sh'a anyadiu un modulo textUtils pa fer simples las diferencias de cadena entre las cadenas d'o Python 3 y las cadenas d'o Windows unicode. (#9545)
 - Mira-te la documentación d'o modulo y lo modulo textInfos.offsets pa eixemplos d'implementacions.
- Agora s'ha eliminau funcionalidat obsoleta. (#9548)
 - AppModules eliminaus:
  - Windows XP sound recorder.
  - Klango Player, lo qual ye  un software albandonau.
 - S'ha eliminau lo configobj.validate wrapper.
  - Habría d'emplegar-se lo codigo nuevo configobj import validate en cuenta d'import validate
 - S'ha reemplazau textInfos.Point y textInfos.Rect por locationHelper.Point y locationHelper.RectLTRB respectivament.
 - S'ha eliminau braille.BrailleHandler._get_tether y braille.BrailleHandler.set_tether.
 - S'ha eliminau config.getConfigDirs.
 - S'ha reemplazau config.ConfigManager.getConfigValidationParameter por getConfigValidation
 - S'ha eliminau la propiedat inputCore.InputGesture.logIdentifier.
   - Emplega _get_identifiers in inputCore.InputGesture en cuenta.
 - S'ha eliminau synthDriverHandler.SynthDriver.speakText/speakCharacter.
 - S'ha eliminau quantas clases synthDriverHandler.SynthSetting
   - Conservadas anteriorment pa conpatibilidad con versions anteriors (#8214), agora se consideran obsoletas.
   - Los controladors que empleguen las clases SynthSetting habrían d'actualizar-sen pa emplegar las clases DriverSetting.
 - S'ha eliminau bell codigo heredau, en particular:
  - Suporte pa la lista de mensaches de l'Outlook pre 2003.
  - Una clase de superposición pa lo menú d'Inicio clasico, que nomás se troba en Windows Vista y anteriors.
  - S'ha sacau la compatibilidat pa lo Skype 7, ya que definitivament ya no funciona.
- S'ha anyadiu Un marco de treballo que permite a los desembolicadors creyar furnidors d'amilloras visuals; modulos que pueden cambiar lo conteniu d'a pantalla, opcionalment basaus en a dentrada d'o NVDA sobre localizacions d'os obchectos. (#9064)
 - Los complementos pueden agrupar los suyos propios furnidors en una carpeta visionEnhancementProviders.
 - Mira-te los modulos vision y visionEnhancementProviders pa la implementación d'o marco de treballo y eixemplos, respectivament.
 - Los furnidors d'amillora d'a visión s'enchegan y configuran a traviés d'a categoría 'visión' en o dialogo d'opcions d'o NVDA.
- Las propiedatz d'a clase Abstract agora se suportan en obchectos que heredan de baseObject.AutoPropertyObject (eix.:. NVDAObjects y TextInfos). (#10102)
- S'ha introduciu displayModel.UNIT_DISPLAYCHUNK como una constant d'unidat textInfos especifica pa DisplayModelTextInfo. (#10165)
 - Ixa nueva constant permite navegar sobre lo texto en un DisplayModelTextInfo de traza que s'asemella mas a cómo s'alza los trozos de texto en o modelo subchacent.
- displayModel.getCaretRect agora torna una instancia de locationHelper.RectLTRB. (#10233)
- Las constants UNIT_CONTROLFIELD y UNIT_FORMATFIELD se son movidas dende virtualBuffers.VirtualBufferTextInfo a lo paquet textInfos. (#10396)
- Pa cada dentrada en o rechistro d'o NVDA, agora s'inclui información sobre lo filo orichinal. (#10259)
- Los obchectos UIA TextInfo agora pueden mover-sen/expandir-sen por la pachina, historico y unidatz de texto formatField. (#10396)
- Los modulos externos (appModules y globalPlugins) agora ye menos probable que puedan crebar la creyación de NVDAObjects. 
 - Las excepcions causadas por los metodos "chooseNVDAObjectOverlayClasses" y "event_NVDAObject_init" agora son correctament capturadas y rechistradas.
- Lo diccionario aria.htmlNodeNameToAriaLandmarkRoles se ye renombrau agora como aria.htmlNodeNameToAriaRoles. Tamién contiene rols que no son rechions.
- Lo scriptHandler.isCurrentScript s'ha eliminau a causa d'a falta d'uso. No bi'n ha reemplazo. (#8677)


= 2019.2.1 =
Esta ye una versión menor pa correchir quantos bloqueyos presents en 2019.2. Las correccions incluyen:
- Se solucionaron varios problemas en Gmail que s'observoron tanto en Firefox como en Chrome a lo interactuar con determinaus menús emerchents tals como en creyar filtros u en cambiar bellas opcions de Gmail. (#10175, #9402, #8924)
- En Windows 7, NVDA ya no fa que lo explorador de fichers de Windows se bloque quan s'utilice lo rato en o menú Encieto. (#9435) 
- Lo Explorador de Fichers de Windows en Windows 7 ya no se bloca en acceder a los campos d'edición d'os metadatos. (#5337) 
- NVDA ya no se pencha a lo interactuar con imachens con una URI en base 64 en Mozilla Firefox u en Google Chrome. (#10227)


= 2019.2 =
Lo resinyable d'ista versión inclui la detección automatica de linias braille de Freedom Scientific, una opción experimental en o panel Abanzau pa aturar lo modo de navegación dende lo movimiento automatico d'o foco (lo qual podría fer milloras de rendimiento), una opción d'alzau brusco pa lo sintetizador Windows OneCore pa aconseguir velocidatz muito rapedas, y muitas atras correccions de fallos.

== Nuevas Caracteristicas ==
- Lo dialogo de busca agora inclui un historial con as zaguers 20 buscas. (#8482)
 - Lo historial de busca se borra quan se reenchegue lo NVDA u se'n salga.
- Lo suporte d'o NVDA pa lo Miranda NG marcha con as versions mas recients d'o client. (#9053) 
- Agora puetz desenchegar lo modo de navegación de traza predeterminada desenchegando la nueva opción d'"enchegar lo modo de navegación en cargar la pachina" en a configuración d'o modo de navegación d'o NVDA. (#8716) 
 - Tiene en cuenta que en que ixa opción siga desenchegada, encara puetz activar lo modo de navegación manualment pretando NVDA+espacio.
- Agora puetz tresminar simbolos en o quadro de dialogo de pronuncia de puntuación y simbolos, de traza parellana a como marcha lo tresminau en a lista d'elementos y en o quadro de dialogo de cenyos de dentrada. (#5761)
- S'ha anyadiu una orden pa cambiar la resolución d'a unidat de texto d'o churi (quánto texto se charrará en mover-se lo churi), no se le ha asignau un cenyo predeterminau. (#9056)
- Lo sintetizador OneCore d'o Windows tien agora una opción d'aumento de velocidat, que permite una fabla significativament mas rapeda. (#7498)
- Agora La opción de charrar a escape ye configurable dende l'aniello d'achustes de sintetizador pa sintetizadors de voz compatibles. (Actualment lo eSpeak-NG y lo Windows OneCore). (#8934)
- Los perfils de configuración agora se pueden enchegar manualment con cenyos. (#4209)
 - Lo cenyo s'ha de configurar en o quadro de dialogo de "cenyos de dentrada".
- En lo Eclipse s'ha adhibiu suporte pa lo autocompletau en l'editor de codigo. (#5667)
 - Amás, la información d'o Javadoc puede leyer-se dende lo editor quan ye present fendo servir NVDA+d.
- S'ha adhibiu una opción experimental en o panel de configuración abanzada que te permite aturar lo foco d'o sistema pa que no siga a lo cursor d'o modo de navegación (calar automaticament lo foco d'o sistema en os elementos enfocables). (#2039) Encara que puede no estar adequau desactivar ixo en totz los puestos web, ixo podría apanyar: 
 - Lo efecto de goma elastica: Lo NVDA desfá esporadicament la zaguer pretada de tecla d'o modo de navegación brincando t'a ubicación anterior.
 - Los quadros d'edición sacan lo foco d'o sistema quan se mueva a traviés d'ells en qualques puestos web.
 - Las pretadas de teclas d'o modo de navegación son lentas de respuesta.
- Pa los controladors de linia braille que l'admitan, agora se puede cambiar las opcions d'o controlador dende la categoría d'opcions braille en o quadro de dialogo d'opcions d'o NVDA. (#7452)
- Agora las linias braille de Freedom Scientific admiten la detección automatica de linias braille. (#7727)


== Cambios ==
- Lo volumen d'o sintetizador s'agrandeix y s'achiqueix de 5 en 5 en cuenta de 10  en 10 en emplegar l'aniello d'opcions. (#6754)
- S'ha aclariu lo texto en l'administrador de complementos en rancar lo NVDA con l'indicador --disable-addons. (#9473)
- S'ha esviellau las anotacions d'emoticonos Unicode Common Locale Data Repository t'a versión 35.0. (#9445)
- S'ha esviellau lo transcriptor de braille liblouis t'a versión 3.9.0. (#9439)
- En anglés, la tecla d'acceso directo pa lo campo de tresminar en a lista d'elementos en o modo de navegación ha cambiau ta alt+y. (#8728)
- En connectar una linia braille autodetectada a traviés d'o Bluetooth, lo NVDA seguirá mirando linias USB compatibles con o mesmo controlador y cambiará ta una connexión USB si ye disponible. (#8853)


== corrección d'errors ==
- Lo NVDA ya no se bloca en que bell directorio de complementos siga laso. (#7686)
- Las marcas LTR y RTL ya no s'anuncian en Braille u en voz por caracters quan s'accede t'a finestra de propiedatz. (#8361)
- Quan se brinque t'os campos de formulario con a navegación rapeda d'o modo de navegación, agora s'anuncia tot lo campo de formulario en cuenta de nomás la primera linia. (#9388)
- Lo NVDA ya no se silenciará dimpués de salir de l'aplicación Windows 10 Mail. (#9341)
- Lo NVDA ya no falla en enchegar-se quan los achustes rechionals d'os usuarios s'estableixcan en una ubicación desconoixida pa lo NVDA, como por eixemplo inglés (Países Baixos). (#8726)
- Quan lo modo de navegación siga enchegau en o Microsoft Excel y se cambie ta bell navegador en o modo de foco u viceversa, lo estau d'o modo de navegación agora se notifica adequadament. (#8846)
- Lo NVDA agora anuncia correctament la linia en o cursor d'o churi en o Notepad++ y atros editors basaus en o Scintilla. (#5450)
- En o Google Docs (y atros editors basaus en web), lo braille ya no amuestra a veces de traza incorrecta "lst end" antis d'o cursor en meyo d'un elemento d'a lista. (#9477)
- En l'actualización de mayo de 2019 d'o Windows 10, lo NVDA ya no diz muitas notificacions de volumen si se cambia lo volumen con os botons de hardware quan lo Explorador de fichers tienga lo foco. (#9466)
- La carga d'o dialogo de pronuncia de cenyos de puntuación y simbolos agora ye muito mas rapeda quan s'utilice diccionarios de simbolos que contiengan mas d'1.000 dentradas. (#8790)
- En os controls d'o Scintilla como lo Notepad++, lo NVDA puede leyer la linia correcta quan l'achuste de linia siga enchegau. (#9424)
- En o Microsoft Excel, la ubicación d'a celda s'anuncia dimpués que cambie a causa d'os cenyos mayus+intro u mayus+intro d'o teclau numerico. (#9499)
- Dende lo Visual Studio 2017 en adebant, en a finestra d'o Explorador d'obchectos, l'elemento trigau en l'arbol d'obchectos u en l'arbol de miembros con categorías agora s'anuncia correctament. (#9311)
- Los complementos con nombres que nomás difieran en as mayusclas ya no se tractan como complementos deseparaus. (#9334)
- En o caso d'as voces d'o Windows OneCore, la velocidat establida en o NVDA ya no se veye afectada por la velocidat establida en a configuración de voz d'o Windows 10. (#7498)
- Lo rechistro se puede ubrir agora con NVDA+F1 quan no bi ha información d'o desembolicador pa l'obchecto de navegador actual. (#8613)
- Tamién ye posible fer servir los comandos de navegación de tabla d'o NVDA en o Google Docs, en o Firefox y en o Chrome. (#9494)
- Las teclas frontals agora funcionan correctament en as linias braille de Freedom Scientific. (#8849)
- En leyer lo primer caracter d'un documento en o Notepad++ 7.7 X64, lo NVDA ya no se conchela entre un maximo de diez segundos. (#9609)


== Cambios pa los Desembolicadors ==
- Agora puetz configurar la propiedat "disableBrowseModeByDefault" en os modulos de l'aplicación pa que deixe lo modo de navegación desenchegau por defecto. (#8846)
- Lo estilo extendiu de finestra d'una finestra  agora s'exposa utilizando la propiedat `extendedWindowStyle` en obchectos finestra y los suyos derivaus. (#9136)
- S'ha esviellau lo paquet comtypes ta 1.1.7. (#9440, #8522)
- En emplegar lo comando report module info, l'orden d'a información s'ha cambiau pa presentar lo modulo en primeras. (#7338)
- S'ha anyadiu un eixemplo pa contrimostrar l'uso de nvdaControllerClient.dll dende C#. (#9600)


= 2019.1 =
Lo resinyable d'ista versión inclui la rialización de milloras en acceder to Microsoft word y t'o Excel, milloras d'estabilidat y de seguranza tals como l'admisión de complementos con información de compatibilidat de versión, y muitas atras correccions d'errors.

Por favor para cuenta que dende ista versión d'o NVDA los modulos d'aplicación, los complementos globals, los controladors de linias braille y los controladors de sintetizador personals ya no se cargarán automaticament dende lo tuyo directorio de configuración d'usuario d'o NVDA. 
En cuenta deberían instalar-sen como parti d'un complemento d'o NVDA. Pa qui desemboliquen codigo pa bell complemento, lo codigo pa prebas se puet calar en un nuevo directorio scratchpad pa desembolicadors en o directorio de configuración d'usuarios d'o NVDA,  si la opción de desembolicador scratchpad ye enchegada en o nuevo panel d'opcions Abanzadas d'o NVDA.
Ixos cambios fan falta pa guarenciar una millor compatibilidat d'o codigo personalizau, de modo que lo NVDA no se crebe quan ixe codigo se torne incompatible con versions más nuevas.
Por favor, mira-te la lista de cambios mas t'abaixo pa obtener mas detalles sobre ixo y de cómo se versionan agora millor los complementos.

== Nuevas caracteristicas ==
- Nuevas tablas braille: Africano, braille computerizau arabe de 8 puntos, arabe grau 2, espanyol grau 2. (#4435, #9186)
- S'ha anyadiu una opción a las opcions d'o churi d'o NVDA pa fer que lo NVDA maneye situgacions en que lo rato siga controlau por unatra aplicación. (#8452) 
 - Ixo permitirá a lo NVDA rastriar lo churi quan un sistema siga controlau remotament fendo servir lo TeamViewer u atros programas de control remoto.
- S'ha anyadiu lo parametro de linia de comandos `--enable-start-on-logon` pa permitir configurar que las instalacions silenciosas d'o NVDA ranquen en a pantalla d'inicio de sesión u no pas. Especifica verdadero pa rancar en a pantalla d'inicio u falso pa no fer-lo. Si no se define lo parametro --enable-start-on-logon allora lo NVDA ranca por defecto en a pantalla d'inicio de sesión, difuera que ya estase configurau a no por bella instalación previa. (#8574)
- Ye posible desenchegar las funcions de rechistro d'o NVDA configurando lo libel de rechistro a "desenchegau" dende lo panel d'opcions chenerals. (#8516)
- Agora s'anuncia la presencia de formulas en as fuellas de calculo d'o LibreOffice y l'Apache openOffice. (#860)
- En o Mozilla Firefox y lo Google Chrome, lo modo de navegación agora anuncia l'elemento trigau en os quadros de lista y en os arbols.
 - Ixo marcha en o Firefox 66 y posteriors.
 - Ixo no marcha pa bells quadros de lista (controls HTML select) en o Chrome.
- Suporte preliminar pa aplicacions tals como lo Mozilla Firefox en os ordinadors con procesadors ARM64 (p.eix.: Qualcom Snapdragon). (#9216)
- S'ha anyadiu una nueva categoría d'opcions abanzadas en o dialogo d'opcions d'o NVDA, incluyindo una opción pa prebar lo nuevo suporte d'o NVDA pa lo Microsoft Word a traviés de l'API d'o Microsoft UI Automation. (#9200)
- S'ha anyadiu lo suporte pa la envista grafica en l'Administrador de Discos d'o Windows. (#1486)
- S'ha anyadiu lo suporte d'Handy Tech Connect Braille y Basic Braille 84. (#9249)


== Cambios ==
- S'ha esviellau lo transcriptor braille liblouis t'a versión 3.8.0. (#9013)
- Los autors de complementos agora pueden fer complir una versión minima requiesta d'o NVDA pa los suyos complementos. Lo NVDA refusará instalar u cargar un complemento que la suya versión minima   requiesta d'o NVDA  ye posterior que no la versión actual d'o NVDA. (#6275)
- Los autors de complementos agora pueden especificar la zaguer versión d'o NVDA contra la quala s'ha prebau lo complemento. Si bell complemento  no s'ha prebau que con una versión d'o NVDA anterior que no la versión actual, allora lo NVDA refusará instalar u cargar lo complemento. (#6275)
- Ista versión d'o NVDA permitirá la instalación y carga de complementos que agún no contiengan la información d'a versión minima d'o NVDA y la zaguera prebada, pero l'actualización ta versions venideras d'o NVDA (por eixemplo 2019.2) puet fer que ixos complementos mas antigos se desencheguen automaticament.
- Lo comando de mover lo churi t'o navegador d'obchectos agora ye disponible tanto en o Microsoft Word como en os controls UIA, especialment en o Microsoft Edge. (#7916, #8371)
- S'ha amillorau l'anunciau d'o texto baixo lo churi adintro d'o Microsoft Edge y atras aplicacions UIA. (#8370)
- Quan s'encieta lo NVDA con o parametro de linia de comandos `--portable-path`, la rota furnida se replena automaticament en que se mira de creyar una copia portable d'o NVDA fendo servir lo menú d'o NVDA. (#8623)
- S'ha esviellau la rota t'a tabla braille noruega pa refleixar lo estandard a partir de l'anyo 2015. (#9170)
- Quan se navega por paragrafos (control+flechas alto u abaixo) u se navega por celdas de tablas (control+alt+flechas), la existencia d'errors d'ortografía ya no s'anunciará, mesmo si lo NVDA ye configurau pa anunciar-las automaticament. Ixo ye porque los paragrafos y las celdas de tabla pueden estar pro grans, y calcular las errors d'ortografía en qualques aplicacions puede estar bien costoso. (#9217)
- Lo NVDA ya no carga automaticament appModules, globalPlugins y controladors braille y de sintetizador dende lo directorio de configuración de l'usuario d'o NVDA. Ixe codigo habría d'estar empaquetau en cuenta como un complemento con información correcta de versión, guarenciando que lo codigo incompatible no s'execute con as versions actuals d'o NVDA. (#9238)
 - Pa los desembolicadors que lis faga falta prebar lo codigo seguntes se desembolica, s'ha habilitau lo directorio developer scratchpad d'o NVDA en a categoría d'abanzau d'as opcions d'o NVDA, y colocar lo codigo en o directorio 'scratchpad' trobau en o directorio de configuración de l'usuario quan ixa opción siga enchegada.


== Corrección d'errors ==
- En emplegando lo sintetizador de voz OneCore en l'actualización d'abril d'o 2018 d'o Windows 10 y posteriors, ya no se fica grans trozos de silencio entre las expresions orals. (#8985)
- Quan te muevas por caracters en controls de texto plano (tals como lo Notepad) u en o modo de navegación, los caracters emoticonos de 32 bits que pendan en dos puntos de codigo UTF-16 (tals como ðŸ¤¦) agora se leyerán apropiadament. (#8782)
- S'ha amillorau lo dialogo de confirmación de reenchegue dimpués de cambiar l'idioma d'a interficie d'o NVDA. Lo texto y las etiquetas d'os botons son agora mas breus y menos trafucaderas. (#6416)
- Si bell sintetizador de voz de tercers no se carga lo NVDA recorrerá a lo Windows OneCore en o Windows 10, en cuenta d'espeak. (#9025)
- S'ha eliminau la dentrada d'o dialogo de bienvenida en o menú d'o NVDA en as pantallas seguras. 
- A lo tabular u en emplegar la navegación rapeda en o modo de navegación, las lechendas en os panels de pestanyas s'informan agora de forma mas coderent. (#709)
- Lo NVDA anunciará agora los cambios de selección pa determinaus selectors de tiempo tals como en as Alarmas y en l'aplicación d'o reloch en o Windows 10. (#5231)
- En o Centro d'actividatz d'o Windows 10 lo NVDA anunciará los mensaches d'estau a lo alternar entre accions rapidas como lo brilo y l'enfoque. (#8954)
- En o centro d'actividatz en l'actualización d'o Windows 10 d'octubre de 2018 y versions anteriors lo NVDA reconoixerá lo control de brilo d'acción rapeda como un botón en cuenta de como un botón commutable. (#8845)
- Lo NVDA tornará a rastriar lo cursor y anunciará los caracters eliminaus en o Microsoft Excel y buscará los campos d'edición. (#9042)
- S'ha correchiu una error rara en o modo de navegación en o Firefox. (#9152)
- Lo NVDA ya no falla en anunciar l'enfoque de qualques controls en a cinta d'o Microsoft Office 2016 quan ye contraita.
- Lo NVDA ya no falla en anunciar lo contacto sucheriu en ficar adrezas en os nuevos mensaches de l'Outlook 2016. (#8502)
- Las zagueras teclas d'enrotamiento d'o cursor en as linias eurobraille de 80 celdas ya no endrezan lo cursor ta una posición en u chusto dimpués de l'inicio d'a linia braille. (#9160)
- S'ha correchiu la navegación de tablas en a envista en filo d'o Mozilla Thunderbird. (#8396)
- En o Mozilla Firefox y lo Google Chrome, cambiar t'o modo foco agora funciona correctament pa bells quadros de lista y arbols (en do lo quadro de lista u arbol no siga en o mesmo enfocable pero los suyos elementos sí en sigan). (#3573, #9157)
- Lo modo de navegación s'enchega agora correctament de traza predeterminada quan se leye mensaches en l'Outlook 2016/365 si s'usa la compatibilidat con o suporte experimental de l'UI Automation d'o NVDA pa los documentos d'o Word. (#9188)
- Agora ye menos prebable que lo NVDA se chele de tal traza que la sola forma d'eslampar-ne siga zarrar la sesión actual d'o Windows. (#6291)
- En l'actualización d'octubre d'o 2018 d'o Windows 10 y las versions posteriors, en ubrir lo historial d'o portafuellas d'a boira con o portafuellas vuedo, lo NVDA anunciará lo estau d'o portafuellas. (#9103)
- En l'actualización d'octubre d'o 2018 d'o Windows 10 y las versions posteriors, en buscar emoticonos en o panel d'emoticonos, lo NVDA anunciará lo millor resultau. (#9105)
- Lo NVDA ya no se chela en a finestra prencipal de l'Oracle VirtualBox 5.2 y superiors. (#9202)
- La respuesta en o Microsoft Word en navegar por linias, paragrafos u celdas de tabla puede amillorar-se significativament en qualques documentos. Se recuerda que pa un millor rendimiento, s'establirá la envista de borrador en o Microsoft Word con alt+w,y dimpués d'ubrir un documento. (#9217) 
- En o Mozilla Firefox y lo Google Chrome, las alertas vuedas ya no se notifican. (#5657)
- Milloras significativas en o rendimiento en navegar por las celdas d'o Microsoft Excel, especialment quan la fuella de calculo contienga comentarios y/u listas desplegables de validación. (#7348)
- Ya no habría d'estar necesario desenchegar la edición en a celda en as opcions d'o Microsoft Excel pa acceder t'o control d'edición de celdas con o NVDA en l'Excel 2016/365. (#8146).
- S'ha apanyau una cheladura en o Firefox vista a veces en emplegando la navegación rapida por marcapachinas, si se ye usando lo complemento Enhanced Aria. (#8980)


== Cambios pa los Desembolicadors ==
- Lo NVDA agora puede compilar-se con totas las edicions d'o Microsoft Visual Studio 2017 (no nomás con a edición Community). (#8939)
- Agora puetz incluyir la salida d'o rechistro d'o liblouis en o rechistro d'o NVDA configurando la bandera booleana louis en a sección debugLogging d'a configuración d'o NVDA. (#4554)
- Los autors de complementos agora pueden furnir información sobre la compatibilidat d'as versions d'o NVDA en os manifests d'os complementos. (#6275, #9055)
 - minimumNVDAVersion: La versión minima reqiesta d'o NVDA pa que un complemento marche como cal.
 - lastTestedNVDAVersion: La zaguer versión d'o NVDA con a quala ye estau prebau bell complemento.
- OffsetsTextInfo agora puede implementar lo metodo _getBoundingRectFromOffset pa permitir la recuperación de rectanglos delimitadors por caracters en cuenta de puntos. (#8572)
- S'ha anyadiu una propiedat boundingRect a los obchectos TextInfo pa recuperar lo rectanglo delimitador d'un rango de texto. (#8371)
- Las propiedatz y metodos adintro d'as clases agora pueden estar marcadas como abstractas en o NVDA. Ixas clases chenerarán una error si se instancian. (#8294, #8652, #8658)
- Lo NVDA puede rechistrar lo tiempo transcorriu dende que s'introdució lo texto, lo que aduya a medir la capacidat de respuesta percita. Esto puede activar-se configurando la opción timeSinceInput como True en a sección debugLog d'a configuración d'o NVDA. (#9167)


= 2018.4.1 =
Ista versión apanya una crebadura en rancar si l'idioma d'a interficie d'usuario d'o NVDA ye establiu en aragonés. (#9089)


= 2018.4 =
Lo mas resinyable d'ista versión inclui las milloras en o rendimiento d'as zaguers versions d'o Mozilla Firefox, l'anunciau d'emoticonos con totz los sintetizadors, l'anunciau d'as respuestas y ninvios en l'Outlook, la información d'a distancia d'o cursor a lo canto d'una pachina d'o Microsoft Word y muitas correccions de fallos.

== Nuevas Caracteristicas ==
- Nuevas tablas braille: Chino (China, Mandarín) grau 1 y grau 2. (#5553)
- Agora s'anuncia los estaus respondiu y reninviau en elementos de correu en a lista de mensaches d'o Microsoft Outlook. (#6911)
- Lo NVDA agora puet leyer descripcions pa emoticonos asinas como atros caracters que fan parti d'o repositorio Unicode Common Locale Data. (#6523)
- En o Microsoft Word, la distancia d'o cursor dende los cantos superior y cucho d'a pachina puet anunciar-se  pretando NVDA+suprimir d'o teclau numerico. (#1939)
- En as fuellas de Google con o modo de braille enchegau lo NVDA ya no anuncia 'trigau' en cada celda en mover lo foco entre ellas. (#8879)
- S'ha anyadiu lo suporte pa Foxit Reader y pa Foxit Phantom PDF (#8944)
- S'ha anyadiu lo suporte pa la utilidat de base de datos DBeaver. (#8905)


== Cambios ==
- "Anunciar los globos d'aduya" en o dialogo de presentación d'obchectos s'ha renombrau como "Anunciar las notificacions" pa incluir l'anunciau d'as notificacions d'o sistema en o Windows 8 y posteriors. (#5789)
- EN AS opcions d'o teclau d'o NVDA las caixetas de verificación pa enchegar u desenchegar las teclas modificaderas d'o NVDA agora s'amuestran en una lista en cuenta d'en caixetas de verificación deseparadas.
- Lo NVDA ya no presienta información redundant en leyer lo reloch d'a servilla d'o sistema en qualques versions d'o Windows. (#4364)
- S'ha esviellau lo transcriptor braille liblouis t'a versión 3.7.0. (#8697)
- S'ha esviellau lo eSpeak-NG t'a confirmación 919f3240cbb.


== Corrección d'Errors ==
- En l'Outlook 2016 y 365, s'anuncia la categoría y lo estau d'a marca pa los mensaches. (#8603)
- Quan lo NVDA se configura pa idiomas tals como Kirgyz, Mongol u Macedonio, ya no amuestra un dialogo en un aviso en rancar que l'idioma no s'admite por lo sistema operativo. (#8064)
- En mover lo churi t'o navegador d'obchectos agora será muito mas preciso mover lo churi t'a posición d'o modo de navegación en o Mozilla Firefox, lo Google Chrome y l'Acrobat Reader DC. (#6460)
- S'ha amillorau l'interactuar con os quadros combinaus en a web en o Firefox, lo Chrome y l'Internet Explorer. (#8664)
- Si s'executa en a versión chaponesa d'o Windows XP u Vista, lo NVDA agora amuestra l'alerta d'os requisitos d'a versión d'o Sistema Operativo seguntes s'asperaba. (#8771)
- S'aumenta lo rendimiento en o Mozilla Firefox en navegar por pachinas grans con muitos cambios dinamicos. (#8678)
- Lo braille ya no amuestra atributos de fuent si se desenchegoron en as  opcions de formatiau de documentos. (#7615)
- Lo NVDA ya no falla en seguir a lo foco en o Explorador de Fichers y atras aplicacions que fagan servir l'UI Automation quan unatra aplicación siga ocupada (tal como lo procesamiento por lotes de l'audio). (#7345)
- En os menús ARIA en a web, la tecla d'escape agora se pasará a traviés d'o menú y ya no desenchegará lo modo de foco incondicionalment. (#3215)
- En a interficie nueva d'o Gmail, en emplegar la navegación rapeda adintro de mensaches mientras se leye, ya no s'anuncia tot lo cuerpo d'o mensache dimpués de l'elemento t'o que acabas de navegar. (#8887)
- Dimpués d'esviellar lo NVDA los navegadors tals como lo Firefox y lo google Chrome ya no habrían de trencar-sen, y lo modo de navegación habría de seguir reflectando correctament las actualizacions de qualsiquier documento cargau actualment. (#7641) 
- Lo NVDA ya no informa que se puet fer clic quantas veces en una ringlera en navegar por conteniu clicable en o Modo de navegación. (#7430)
- Los cenyos realizaus en las linias braille baum Vario 40 ya no fallarán en executar-sen. (#8894)
- En o Google Slides con o Mozilla Firefox, lo NVDA ya no anuncia lo texto trigau en cada control con o foco. (#8964)


== Cambios pa los Desembolicadors ==
- gui.nvdaControls agora contiene dos clases pa creyar listas accesibles con caixetas de verificación. (#7325)
 - CustomCheckListBox ye una sub-clase accesible de wx.CheckListBox.
 - AutoWidthColumnCheckListCtrl anyade caixetas de verificación accesibles a un AutoWidthColumnListCtrl, lo qual ye basau en si mísmo en wx.ListCtrl.
- Si te fa falta fer un wx widget accesible que no'n ye encara, ye posible fer-lo fendo servir una instancia de gui.accPropServer.IAccPropServer_impl. (#7491)
 - Mira-te la implementación de gui.nvdaControls.ListCtrlAccPropServer pa mas información.
- S'ha esviellau lo configobj ta 5.1.0dev confirmación 5b5de48a. (#4470)
- L'acción config.post_configProfileSwitch agora prene l'argumento opcional prevConf keyword, permitindo a los maniadors prener una acción basada en diferencias entre la configuración dinantes y dimpués d'o cambio de perfil. (#8758)


= 2018.3.2 =
Ista ye una versión menor pa privar una penchada en o Google Chrome en navegar por tuits en www.twitter.com. (#8777)


= 2018.3.1 =
Ista ye una versión menor pa correchir una error critica en o NVDA que feba que las versions de 32 bits d'o Mozilla Firefox se penchasen. (#8759)


= 2018.3 =
Lo resinyable d'ista versión inclui la detección automatica de muitas linias Braille, l'admisión pa qualques caracteristicas nuevas d'o Windows 10 incluindo lo panel de dentrada d'emojis de Windows 10, y muitas atras correccions d'errors.

== Nuevas Caracteristicas ==
- Lo NVDA anunciará las errors gramaticals quan las pachinas web en o Mozilla Firefox y lo Google Chrome las exposen apropiadament. (#8280)
- Lo conteniu que se marca como estando borrau u ficau en as pachinas web agora s'anuncia en o Google Chrome. (#8558)
- S'ha adhibiu lo suporte pa las ruedas de desplazamiento d'o BrailleNote QT y l'Apex BT quan s'emplega lo BrailleNote como una linia braille con o NVDA. (#6316)
- S'ha adhibiu programas pa anunciar lo tiempo trescorriu y lo tiempo total d'a pista actual en o Foobar2000. (#6596)
- Lo simbolo d'a tecla de comando d'o Mac (⌘) agora s'anuncia en leyer texto con qualsiquier sintetizador. (#8366)
- Agora s'admite los rols personalizaus a traviés de l'atributo aria-roledescription attribute en o Firefox, lo Chrome y l'Internet Explorer. (#8448)
- Nuevas tablas braille: braille sueco computerizau de 8 puntos, Curdo central, Esperanto, Hungaro y checo. (#8226, #8437)
- S'ha adhibiu lo suporte pa la detección automatica de linias braille en segundo plan. (#1271)
 - Se suporta actualment las linias ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille y HumanWare BrailleNote y Brailliant BI/B.
 - Puetz habilitar ista caracteristica trigando la opción d'automatico dende la lista de linias braille en o dialogo de seleccionar linia braille d'o NVDA.
 - Por favor mira-te la documentación pa detalles adicionals.
- S'ha adhibiu lo suporte pa quantas caracteristicas de dentrada modernas introducidas en las versions recients d'o Windows 10. Istas incluyen lo panel d'emoji (actualización Fall Creators), dictau (actualización Fall Creators), sucherencias de dentrada d'o teclau fisico (actualización d'abril d'o 2018), y apegar en o portafuellas en a boira (actualización d'octubre d'o 2018). (#7273)
- Lo conteniu marcau como bloque de cita fendo servir l'ARIA (role blockquote) agora se suporta en o Mozilla Firefox 63. (#8577)


== Cambios ==
- La lista d'idiomas disponibles en o dialogo d'opcions chenerals agora s'ordena basando-se en os nombres d'os idiomas en cuenta d'en os codigos ISO 639. (#7284)
- S'ha adhibiu cenyos predeterminaus pa alt mayus tabulador y windows tabulador con totas las linias braille compatibles de Freedom Scientific. (#7387)
- Pa l'ALVA BC680 y linias con conversor de protocolo, agora ye posible assignar funcions diferents a los smart pad cucho y dreito, a lo thumb y a las teclas etouch. (#8230)
- Pa las linias ALVA BC6, la combinación de teclas sp2+sp3 agora anunciará la hora y la calendata actuals, mientras que sp1+sp2 emula la tecla Windows. (#8230)
- Agora se le pregunta a l'usuario una vez en o ranque d'o NVDA si ye d'alcuerdo en ninviar estatisticas d'uso ta NV Access quan se mire actualizacions automaticament. (#8217)
- En mirar actualizacions, si l'usuario ye d'alcuerdo en permitir lo ninvio d'estatisticas d'uso ta NV Access, lo NVDA agora ninviará lo nombre d'o controlador d'o sintetizador actual y d'a linia braille en uso, pa aduyar a establir un millor orden de prioridatz pa lo treballo futuro d'ixos controladors. (#8217)
- S'ha esviellau lo transcriptor braille liblouis t'a versión 3.6.0. (#8365)
- S'ha esviellau la rota t'a tabla braille rusa de 8 puntos correcta. (#8446)
- S'ha esviellau l'eSpeak-ng ta 1.49.3dev confirmación 910f4c2 (#8561)


== Corrección d'Errors ==
- Las etiquetas accesibles pa los controls en o Google Chrome agora s'anuncian mas leyiblement en o modo de navegación quan la etiqueta no i amaneix como conteniu. (#4773)
- Agora se suporta las notificacions en o Zoom. Por eixemplo, ixo inclui silenciar u desilenciar o estau, y los mensaches dentrants. (#7754)
- Cambiar la presentación d'o contexto braille quan se siga en o modo de navegación ya no causa que la salida braille deixe de seguir lo cursor d'o modo de navegación. (#7741)
- Las linias braille ALVA BC680 ya no fallan intermitentment en inicializar-sen. (#8106)
- Por defecto, las linias ALVA BC6 ya no executarán teclas emuladas d'o sistema en pretar combinacions de teclas que tiengan a veyer con sp2+sp3 pa disparar funcionalidatz internas. (#8230)
- En pretar lo sp2 en una linia ALVA BC6 pa emular la tecla alt agora funciona tal como s'anuncia. (#8360)
- Lo NVDA ya no anuncia cambios redundants d'a distribución de teclau. (#7383, #8419)
- Lo seguimiento d'o churi agora ye muito mas preciso en o bloque de notas y en atros controls d'edición de texto sin formato quan se trobe en un documento con mas de 65535 caracters. (#8397)
- Lo NVDA reconoixerá mas dialogos en o Windows 10 y atras aplicacions modernas. (#8405)
- En l'actualización d'octubre d'o 2018 d'o Windows 10 y d'o Server 2019 y posteriors lo NVDA ya no falla en seguir a lo foco d'o sistema quan una aplicación se conchela u engarona a lo sistema d'escayecimientos. (#7345, #8535)
- Agora s'informa a los usuarios quan miren de leyer u copiar una barra d'estau lasa. (#7789)
- S'ha correchiu un caso en do lo estau de "no marcau" en os controls no s'anunciaba en voz si lo control yera estau parcialment marcau anteriorment. (#6946)
- En a lista d'idiomas en as opcions chenerals d'o NVDA lo nombre pa l'idioma birmano s'amuestra correctament en o Windows 7. (#8544)
- En o Microsoft Edge lo NVDA anunciará notificacions tals como leyer la disponibilidat d'a envista y lo progreso d'a carga d'a pachina. (#8423)
- En navegar por una lista en a web lo NVDA agora anunciará la suya etiqueta si l'autor d'a pachina en ha furniu una. (#7652)
- Quan s'asigna manualment funcions a cenyos pa una linia braille en particular, ixos cenyos agora siempre amaneixen como asignaus a ixa linia. Anteriorment s'amostraban como si estasen asignaus a la linia activa en ixe momento. (#8108)
- Agora s'admite la versión de 64 bits d'o Meya Player Classic. (#6066)
- Quantas milloras a lo suporte braille en o Microsoft Word con l'UI Automation enchegau:
 - De traza semellant a atros campos de texto multilínea, quan se cale a lo comienzo d'un documento en Braille, la linia agora se desplaza de tal forma que lo primer caracter d'o documento se trobe a lo prencipio d'a linia. (#8406)
 - Reducción d'a presentación masiau ampla d'o foco tanto en voz como en braille quan s'enfoque bell documento d'o Word. (#8407)
 - Lo enrotamiento d'o cursor en braille agora funciona correctament quan se ye en una lista en un documento d'o Word. (#7971)
 - Las viñetas u numers ficaus recientment en un documento d'o Word s'anuncian correctament tanto en voz como en braille. (#7970)
- En o Windows 10 1803 y posteriors, agora ye posible d'instalar complementos si ye enchegada la caracteristica d'"utilizar Unicode UTF-8 pa lo suporte d'idioma en totz". (#8599)


== Cambios pa los Desembolicadors ==
- S'ha adhibiu scriptHandler.script, lo qual puet funcionar como un decorador pa programas en os obchectos programables. (#6266)
- S'ha ficau un marco de treballo de sistema de prebas pa lo NVDA. (#708)
- S'ha rializau qualques cambios en o modulo hwPortUtils: (#1271)
 - Lo listUsbDevices agora chenera diccionarios con información de dispositivo incluindo hardwareID y devicePath.
 - Los diccionarios cheneraus por lo listComPorts agora tamién contienen una dentrada usbID pa los puertos COM con información USB VID/PID en o suyo ITZ d'hardware.
- S'ha esviellau lo wxPython ta 4.0.3. (#7077)
- Dau que lo NVDA agora nomás ye compatible con o Windows 7 SP1 y posteriors, s'ha eliminau la clau "minWindowsVersion" utilizada pa comprebar si l'UIA habría d'enchegar-se pa una versión en particular d'o Windows. (#8422)
- Agora te puetz rechistrar pa que se te notifique sobre accions d'alzar u reenchegar la configuración a traviés d'as nuevas accions config.pre_configSave, config.post_configSave, config.pre_configReset, y config.post_configReset. (#7598)
 - config.pre_configSave s'emplega pa que se te notifique quan la configuración d'o NVDA ye a pocas d'alzar-se, y config.post_configSave se clama dimpués que la configuración s'haiga alzada.
 - config.pre_configReset y config.post_configReset incluyen un indicador de valors predeterminadas  de fabrica pa especificar si las opcions se recargan dende lo disco (false) u se reestableixen t'as valors predeterminadas (true).
- config.configProfileSwitch s'ha renombrau ta config.post_configProfileSwitch pa refleixar lo feito que ixa acción se clama dimpués que lo cambio de perfil tienga efecto. (#7598)
- S'ha esviellau interficies d'UI Automation pa lactualización d'octubre d'o 2018 d'o Windows 10 y Server 2019 (IUIAutomation6 / IUIAutomationElement9). (#8473)


= 2018.2 =

Lo resinyable d'ista versión inclui lo suporte pa tablas en o Kindle pa PC, lo suporte pa pantallas Humanware BrailleNote Touch y BI14 Braille, milloras pa os sintetizadors de voz Onecore y Sapi5, milloras en o Microsoft Outlook y muito mas.

== Nuevas Caracteristicas ==
- Agora s'anuncia lo rango de ringleras y columnas pa celdas de tablas  en voz y braille. (#2642)
- Agora se suporta las ordens de navegación de táblas d'o NVDA en o Google Docs (con o modo de braille enchegau). (#7946)
- S'ha adhibiu a Capacidat pa leyer y navegar por tablas en o Kindle pa PC. (#7977)
- Suporte pa las linias BrailleNote touch y Brailliant BI 14 a traviés tanto d'USB como de bluetooth. (#6524)
- En l'actualización Fall Creators d'o Windows 10 y posteriors lo NVDA puet anunciar notificacions dende aplicacions tals como a calculadora y o Windows Store. (#8045)
- Nuevas tablas de transcripcción braille: Lithuano 8 puntos, ucrainés, Mongol grau 2. (#7839)
- S'ha adhibiu un programa pa anunciar información de formato pa lo texto baixo una celda braille especifica. (#7106)
- En esviellar o NVDA, agora ye posible de posposar a instalación de l'actualización pa un momento posterior. (#4263) 
- Nuevos idiomas: Mongol, Alemán de Suiza.
- Agora puetz commutar control, shift, alt, windows y NVDA dende lo tuyo teclau braille y combinar ixos modificadors con a dentrada braille (eix.: pretar control+s). (#7306) 
 - Puetz asignar ixas nuevas commutacions de modificadors fendo servir a orden que se troba en Teclas de sistema emuladas en o dialogo de cenyos de dentrada.
- S'ha restaurau lo suporte pa las linias Handy Tech Braillino y Modular (con o  firmware antigo). (#8016)
- Agora se sincronizará automaticament con o NVDA la calendata y la hora pa los dispositivos Handy Tech suportaus (tals como l'Active Braille y l'Active Star) quan sigan desincronizaus mas de cinco segundos. (#8016)
- En as listas de mensaches d'o Microsoft Outlook o NVDA agora informa si bel mensache ha estau respondiu u reninviau. (#6911)
- Se puet asignar un cenyo de dentrada pa desenchegar temporalment totz os disparadors d'un perfil de configuración. (#4935)


== Cambios ==
- S'ha cambiau la columna d'estau en l'alministrador de complementos pa indicar si lo complemento ye enchegau u desenchegau amás d'en execución u suspendiu. (#7929)
- S'ha esviellau lo transcriptor braille liblouis ta 3.5.0. (#7839)
- A tabla braille lituana s'ha renombrada ta lituano de 6 puntos pa privar confusions con a nueva tabla de 8 puntos. (#7839)
- As tablas de francés (Canadá) grau 1 y grau 2 s'han eliminadas. En cuenta s'utilizará las tablas de francés (unificau) de 6 puntos y Grau 2 respectivament. (#7839)
- Os sensors secundarios d'as linias braille Alva BC6, EuroBraille y Papenmeier agora anuncian información de formato pa lo texto baixo la celda braille d'ixe sensor. (#7106)
- As tablas de dentrada de braille contraito tornarán automaticament t'o modo no contraito  en casos no editables (ye decir, controls an no bi haiga cursor u en modo de navegación). (#7306)
- O NVDA agora charra menos en o calandario de l'Outlook quan una cita u una francha temporal cubre un día entero. (#7949)
- Agora se puet trobar todas as preferencias d'o NVDA en un unico dialogo d'opcions en o menú NVDA -> Preferencias -> Opcions, en cuenta de deseparar-sen en muitos dialogos. (#7302)
- O sintetizador de voz predeterminau en executar-se en o Windows 10 agora ye l'oneCore speech rather en cuenta de l'eSpeak. (#8176)


== Corrección de fallos ==
- O NVDA ya no falla en leyer controls enfocaus en a pantalla d'inicio de sesión d'a cuenta de Microsoft en Configuración dimpués de calar-bi una adreza de correu. (#7997)
- O NVDA ya no falla en leyer a pachina quan se recula ta bella pachina anterior en o Microsoft Edge. (#7997)
- O NVDA ya no anunciará incorrectament o caracter final d'un PIN d'inicio de sesión d'o windows 10 seguntes a maquina se desbloqueye. (#7908)
- As etiquetas d'as caixetas de verificación y d'os botons d'opción en o Chrome y o Firefox ya no s'anuncian dos veces quan se tabule u s'faga servir a navegación rapeda en o modo de navegación. (#7960)
- Se maneya aria-current con una valor de false como false en cuenta de true (#7892).
- O controlador d'o sintetizador Windows Onecore Voices ya no falla en cargar si a voz configurada s'ha desinstalada. (#7999)
- Cambiar as voces en o controlador d'o sintetizador Windows Onecore Voices agora ye muito mas rapedo. (#7999)
- S'ha apanyau a malformación d'a salida braille pa quantas tablas braille, incluindo signos en mayusclas en o braille danés contraito de 8 puntos. (#7526, #7693)
- O NVDA agora puet anunciar mas tipos de vinyetas en o Microsoft Word. (#6778)
- En pretar lo programa d'anunciar a información ya no se mueve incorrectament a posición de revisión y por tanto en pretar-lo quantas veces ya no fa resultaus diferents. (#7869)
- A dentrada braille ya no te permitirá d'utilizar braille contraito en casos que no i siga suportau (ye decir, ya no se ninviará parolas enteras t'o sistema difuera d'o conteniu de texto y en o modo de navegación). (#7306)
- S'ha apanyau problemas d'estabilidat de connexión pa las linias braille Handy Tech Easy Braille y Braille Wave. (#8016)
- En o Windows 8 y posterior, o NVDA ya no anunciará "desconoixiu" en ubrir o menú rapedo de vinclos (Windows+X) y en trigar elementos d'ixe menú. (#8137)
- Os cenyos especificos d'o modelo pa botons en as pantallas Hims agora funcionan tal como s'anuncia en a Guida de l'Usuario. (#8096)
- O NVDA mirará agora de correchir os problemas de rechistro COM d'o sistema que causan que programas como lo Firefox y l'Internet Explorer se tornen inaccesibles y anuncien "Desconoixiu" por o NVDA. (#2807).
- S'ha treballau en a solución d'un fallo en l'alministrador de fayenas fendo que o NVDA no permita a os usuarios accedir t'os contenius de detalles especificos sobre os procesos. (#8147)
- As voces mas nuevas d'o Microsoft SAPI5 ya no se retardan a la fin d'a verbalización, lo que fa que siga muito mas eficient navegar con istas voces. (#8174)
- O NVDA ya no anuncia (marcas LTR y  RTL) en Braille u en a verbalización por caracters en accedir t'o reloch en as versions recients d'o Windows. (#5729)
- A detección d'as teclas de desplazamiento en as linias Hims Smart Beetle ya no ye fulera. (#6086)
- En qualques controls de texto, particularment en as aplicacions Delphi, a información furnida en a edición y en a navegación agora ye muito mas fiable. (#636, #8102)


== Cambios pa os Desembolicadors ==
- A información pa os desembolicadors pa os obchectos UIA agora contién una lista d'os patrons UIA disponibles. (#5712)
- Os modulos d'aplicación agora pueden aforzar bellas finestras pa fer servir siempre UIA implementando lo metodo isGoodUIAWindow. (#7961)
- A bandera booleana amagada "outputPass1Only" en a sección braille d'a configuración s'ha eliminada unatra vez. O Liblouis ya no suporta pasar 1 solo en a salida. (#7839)


= 2018.1 =
Lo resiñable d'ista versión inclui o suporte pa graficos en o Microsoft word y o PowerPoint, o suporte pa nuevas linias braille incluindo as Eurobraille y o conversor de protocolo d'Optelec, s'ha amillorau lo suporte pa las linias braille Hims y Optelec, milloras de rendimiento pa o Mozilla Firefox 58 y posteriors y muito mas.

== Nuevas Caracteristicas ==
- Agora ye posible d'interactuar con os graficos en o Microsoft Word y o Microsoft PowerPoint, semellant a lo suporte existent pa os graficos en o Microsoft Excel. (#7046)
 - En o Microsoft Word: quan se siga en o modo de navegación, mete o cursor en un grafico integrau y preta l'intro pa interactuar con ell.
 - En o Microsoft Powerpoint quan s'edite una diapositiva: tabula ta un obchecto grafico, y preta l'intro u lo espacio pa interactuar con o grafico.
 - Pa aturar la interacción con un grafico, preta lo escape.
- Nuevo idioma: Kyrgyz.
- S'ha adhibiu o suporte pa o VitalSource Bookshelf. (#7155)
- S'ha adhibiu lo suporte pa o protocolo convertidor Optelec , un dispositivo que te permite d'utilizar as linias Braille Voyager y Satellite fendo servir o protocolo de comunicación d'as ALVA BC6. (#6731)
- Agora ye posible d'emplegar a dentrada braille con una linia braille ALVA 640 Comfort. (#7733) 
 - A funcionalidat de dentrada braille d'o NVDA puet emplegar-se tanto con istas como con atras linias BC6 con o firmware 3.0.0 y anteriors.
 - Suporte inicial pa lo Google Sheets con o modo de braille encehgau. (#7935)
 - Suporte pa las linias braille Eurobraille Esys, Esytime y Iris. (#7488)


== Cambios ==
- S'ha reemplazau los controladors de linias braille HIMS Braille Sense/Braille EDGE/Smart Beetle y Hims Sync por un solo controlador. O nuevo controlador s'activará automaticament pa os antigos usuarios d'o controlador syncBraille. (#7459) 
 - Qualques teclas, especialment as teclas de desplazamiento, s'han reasignadas pa seguir as convencions emplegadas por os productos d'Hims. Mira-te la guida de l'usuario pa mas detalles.
- En escribir con o teclau en pantalla a traviés d'a interacción tactil, por defecto agora has de fer dople tap en cada tecla d'o mesmo modo en que activarías qualsiquier atro control. (#7309)
 - Pa emplegar o modo d'escritura tactil existent en que ye prau con sacar o dido d'a tecla pa activar-la, enchega ixa opción en o nuevo dialogo d'opcions d'interacción tactil que se troba en o menú de preferencias. (#7309)
- Ya no ye menister que lo braille siga explicitament a o foco u a la revisión, ya que ixo ocurrirá automaticament por defecto. (#2385) 
 - Para cuenta que lo seguimiento automatico a la revisión no ocurrirá que en emplegar un cursor de revisión u orden de navegación d'obchectos. O desplazamiento no activará ixe nuevo comportamiento.


== Corrección d'errors ==
- Os mensaches explorables tals como amostrar o formato actual en pretar NVDA+f dos veces a escape ya no fallan quan o NVDA s'instala en una rota con caracters que no sigan ASCII. (#7474)
- O foco agora se restaura correctament atra vez quan se torna t'o Spotify dende belatra aplicación. (#7689)
- En l'actualización Fall Creators d'o Windows 10 o NVDA ya no falla en esviellar-se quan l'acceso controlau a la carpeta ye enchegau dende o Windows Defender Security Center. (#7696)
- A detección d'as teclas de desplazamiento en as linias Hims Smart Beetle ya no ye fulera. (#6086)
- Una lichera millora en o rendimiento en procesar grans cantidatz de conteniu en o Mozilla Firefox 58 y posteriors. (#7719)
- En o Microsoft Outlook,  leyer correus electronicos que contiengan tablas ya no causa errors. (#6827)
- Os cenyos d'as linias braille que emulan as teclas modificaderas d'o teclau d'o sistema agora pueden combinar-sen tamién con atras teclas emuladas d'o teclau d'o sistema si un u mas d'os cenyos embrecaus son especificos d'o modelo. (#7783)
- En o Mozilla Firefox o modo de navegación agora funciona correctament en as finestras emerchents creyadas por extensions tals como LastPass y bitwarden. (#7809)
- O NVDA ya no se conchela a veces en cada cambio d'o foco si o Firefox u lo Chrome han deixau de responder a causa d'una conchelación u una penchada. (#7818)
- En clients de twitter tals como lo Chicken Nugget o NVDA ya no ignorará los zaguers 20 caracters de tuits con 280 caracters en leyer-los. (#7828)
- O NVDA agora fa servir l'idioma correcto en anunciar os simbolos en que se seleccione texto. (#7687)
- En versions recients de l'Office 365 ye nuevament posible navegar por graficos de l'Excel fendo servir as teclas d'as flechas. (#7046)
- En as salidas de voz y braille os estaus d'os controls agora siempre s'anuncian en o mesmo orden, sin importar si son positivos u negativos. (#7076)
- En aplicacions tals como lo Mail d'o Windows 10 o NVDA ya no fallará en anunciar os caracters eliminaus quan se prete o recule. (#7456)
- Agora todas as teclas en as linias Hims Braille Sense Polaris funcionan como se'n alguarda. (#7865)
- O NVDA ya no falla en rancar en o Windows 7 ronyando sobre una dll interna d'api quan unatra aplicación haiga instalau una versión particular d'os redistribuibles d'o Visual Studio 2017. (#7975)


== Cambios pa os Desembolicadors ==
- S'ha adhibiu una bandera booleana amagada en a sección d'o braille en a configuración: "outputPass1Only". (#7301, #7693, #7702) 
 - Ixa bandera ye por defecto a verdadero. Si ye a falso s'emplegará las reglas liblouis multi pass pa la salida braille.
- S'ha adhibiu un nuevo diccionario (braille.RENAMED_DRIVERS) pa permitir una transición sin  problemas a los usuarios que utilizan controladors que sigan estaus substituius por atros. (#7459)
- S'ha esviellau lo paquet comtypes ta 1.1.3. (#7831)
- S'ha implementau un sistema chenerico en braille.BrailleDisplayDriver pa tractar con as linias que ninvian paquetz de confirmación/acuse de recibimiento. Mira-te o controlador d'as linias braille handyTech como un eixemplo. (#7590, #7721)
- Se puet emplegar una nueva variable "isAppX" en o modulo config pa detectar si o NVDA se ye executando como una aplicación Windows Desktop Bridge Store. (#7851)
- Pa implementacions de documento tals como lo NVDAObjects u lo browseMode que tiengan un textInfo, agora bi ha una nueva clase documentBase.documentWithTableNavigation que puet heredar-se pa obtener scripts de navegación estandar de tabla. Por favor mira-te ixa clase pa veyer qué metodos helper han de furnir-sen pa la tuya implementación pa que marche a navegación de tabla. (#7849)
- O fichero por lotes scons agora se maneya millor quan o Python 3 tamién ye instalau, fendo l'uso d'o lanzador pa lanzar especificament o python 2.7 de 32 bits. (#7541)
- hwIo.Hid agora prene un parametro adicional exclusivo que por defecto ye verdadero. Si se mete como falso, se permite a atras aplicacions de comunicar-sen con un dispositivo entre que siga connectau a lo NVDA. (#7859)


= 2017.4 =
Lo resinyable d'ista versión inclui muitas correccions y milloras pa lo suporte web incluindo lo modo de navegación pa dialogos web por defecto, millor anunciau d'as etiquetas d'os grupos de campos en o modo de navegación, lo suporte pa tecnolochías nuevas de Windows 10 tals como l'aplicación Windows Defender Guard y Windows 10 en ARM64, y l'anunciau automatico d'a orientación d'a pantalla y o estau d'a batería.  
Por favor tiene en cuenta que ista versión d'o NVDA ya no suporta o Windows XP u lo Windows Vista. O requisito minimo pa o NVDA agora ye o windows 7 con o Service Pack 1.


== Nuevas Caracteristicas ==
- En o modo de navegación agora ye posible blincar ta l'inicio d'os puntos de referencia fendo servir as ordens blincar t'a fin u t'o prencipio d'o contenedor (coma u mayus+coma). (#5482)
- En o Firefox, o Chrome y l'Internet Explorer, a navegación rapeda por campos d'edición y campos de formulario agora inclui conteniu de texto enriquiu editable (p. eix.: contentEditable). (#5534)
- En os navegadors web a Lista d'Elementos agora puet listar campos de formulario y botons. (#588)
- Suporte inicial pa o Windows 10 en ARM64. (#7508)
- Suporte preliminar pa la lectura y la navegación interactiva de conteniu matematico pa os libros Kindle con matematicas accesibles. (#7536)
- S'ha adhibiu suporte pa o lector de libros dichitals Azardi. (#5848)
- A información de versión pa complementos agora s'anuncia quan se sigan actualizando. (#5324)
- S'ha adhibiu lo suporte pa nuevos parametros de linia de comandos pa creyar una copia portable d'o NVDA. (#6329)
- Suporte pa o Microsoft Edge executando-se dentro de Windows Defender Application Guard (#7600)
- Si s'executa en un portatil u en una tableta o NVDA agora anunciará quan se connecte/desconnecte un cargador y quan la orientación d'a pantalla cambeye. (#4574, #4612)
- Idioma nuevo: Macedonio.
- Nuevas tablas de transcripción braille: Crovata grau 1, Vietnamita grau 1. (#7518, #7565)
- S'ha adhibiu lo suporte pa la pantalla braille Actilino de Handy Tech. (#7590)
- Agora se suporta la dentrada braille pa las pantallas braille Handy Tech. (#7590)


== Cambios ==
- O menor Sistema Operativo suportau por o NVDA agora ye o Windows 7 con o Service Pack 1, u lo Windows Server 2008 R2 con o Service Pack 1. (#7546)
- Os dialogos web en os navegadors Firefox y Chrome agora emplegan o modo de navegación automaticament, fueras que se siga en una aplicación web. (#4493)
- En o modo de navegación en tabular u mover-se-ne con as ordens de teclas de navegación rapida ya no anuncia salindo de contenedors tals como listas y tablas, Lo qual fa la navegación mas eficaz. (#2591)
- En o modo de navegación pa o Firefox y o Chrome agora s'anuncia os nombres de grupos de campos de formulario en mover-se-ne adentro d'ells con a navegación rapeda u quan se tabula. (#3321)
- En o modo de navegación as ordens de navegación rapeda pa os obchectos integraus (u y mayus+u) agora incluyen elementos d'audio y vidio asinas como elementos con os papers aria application y dialog. (#7239)
- S'ha esviellau o Espeak-ng ta 1.49.2),, ixo resuelve qualques problemas con a producción de versions. (#7385)
- En a tercer activación d'o comando de leyer a barra d'estau lo suyo conteniu se copia en o portafuellas. (#1785)
- En asignar cenyos a teclas en una pantalla Baum, puetz limitar-las a lo modelo d'a pantalla braille en uso (p. eix.: VarioUltra u Pronto). (#7517)
- A tecla rapeda pa lo campo tresminar en a lista d'elementos en o modo de navegación s'ha cambiau de alt+f t'alt+y. (#7569)
- S'ha adhibiu un comando pa desvincular a lo modo de navegación pa commutar a inclusión de tablas de disenyo a lo vuelo. Puetz trobar ixe comando en a categoría de modo de navegación  d'o dialogo de cenyos de dentrada. (#7634)
- S'ha esviellau lo transcriptor braille ta 3.3.0. (#7565)
- A tecla rapeda pa lo botón d'opción Expresión regular en o dialogo diccionario s'ha cambiau de alt+r a alt+y. (#6782)
- Los fichers d'os diccionarios d'a fabla agora s'han versionaus y se'n son movius t'o directorio 'speechDicts/voiceDicts.v1'. (#7592)
- As modificacions d'os fichers versionaus (configuración de l'usuario, diccionarios d'a fabla) ya no s'alzan quan o NVDA s'executa dende o lanzador. (#7688)


== Corrección d'Errors ==
- Os vinclos agora s'indican en braille en aplicacions tals como lo Microsoft Word. (#6780)
- O NVDA ya no se torna notablement mas lento quan siga ubiertas muitas pestanyas en os navegadors web Firefox u Chrome. (#3138)
- O enrutamiento de cursor pa las pantallas MDV Lilli Braille ya no mueve incorrectament una celda braille antis de do habría d'estar. (#7469)
- En l'Internet Explorer y atros documentos MSHTML, l'atributo HTML5 requeriu agora se suporta pa indicar lo estau requeriu d'un campo de formulario. (#7321)
- As linias braille agora s'actualizan en escribir caracters arábigos en un documento de WordPad aliniau t'a cucha. (#511).
- As etiquetas accesibles pa controls en o Mozilla Firefox agora s'anuncian mas facilment en o modo de navegación quan a etiqueta no amaneixca como conteniu por si mesma. (#4773)
- En l'actualización Creators d'o windows 10 lo NVDA puet accedir de nuevas ta Firefox dimpués d'un renchegue d'o NVDA. (#7269)
- Quan se renchegue o NVDA con o Mozilla Firefox enfocau, o modo de navegación será disponible nuevament, encara que ye posible que haigas de pretar alt+tab y tornar a pretar-lo de nuevas. (#5758)
- Agora ye posible accedir ta conteniu matematico en o Google Chrome en un sistema sin o Mozilla Firefox instalau. (#7308)
- O sistema operativo y atras aplicacions habrían d'estar mas estables dreitament dimpués d'instalar o NVDA antis de no renchegar en contimparanza con as instalacions  de versions anteriors d'o NVDA. (#7563)
- En emplegar una orden de reconoixencia de conteniu (eix.: NVDA+r), agora o NVDA anuncia un mensache d'error en cuenta de no fer cosa si o navegador d'obchectos ye desapareixiu. (#7567)
- A funcionalidat de desplazamiento enta zaga s'ha correchiu pa linias de freedom Scientific que contiengan una garnela cucha. (#7713)
- As linias braille Braillino, Bookworm y Modular (con firmware antigo) de Handy Tech ya no se suportan en quitar-las d'a caixa. Instala o controlador universal de Handy Tech y o complemento d'o NVDA pa emplegar las linias. (#7590)


== Cambios pa os Desembolicadors ==
- "scons tests" agora mira que as cadenas traducibles tiengan comentarios pa os traductors. Tamién puetz executar ixo nomás con "scons checkPot". (#7492)
- Agora bi ha un nuevo modulo extensionPoints que furne un framework chenerico pa permitir a extensibilidad de codigo en puntos especificos en o codigo. Ixo permite que as partis intresadas se rechistren pa estar notificadas quan ocurra bella acción (extensionPoints.Action), pa modificar un tipo especifico de dato (extensionPoints.Filter) u pa participar en a decisión de si se ferá bella cosa (extensionPoints.Decider). (#3393)
- Agora puetz rechistrar-te pa estar notificau sobre los cambeos de perfils de configuración a traviés de l'acción config.configProfileSwitched. (#3393)
- Os cenyos de linia braille que emulan teclas modificaderas d'o teclau d'o sistema (tals como control y alt) agora pueden conbinar-sen con atras teclas emuladas d'o teclau d'o sistema sin definición explicita. (#6213) 
 - Por eixemplo: si tiens una tecla d'a pantalla vinculada a la tecla alt y unatra tecla d'a pantalla a flecha abaixo, en combinar estas teclas resultará la emulación de alt+flecha abaixo.
- A clase braille.BrailleDisplayGesture agora tiene una propiedat de modelo extra. Si se furne, pretando una tecla chenerará un texto especifico d'identificador de modelo adicional, ixo permite a un usuario vincular cenyos limitaus a un modelo de linia braille especifico. 
 - Mira-te o controlador de baum como un eixemplo pa ixa funcionalidat nueva.
- O NVDA agora se compila con o Visual Studio 2017 y o SDK d'o Windows 10. (#7568)


= 2017.3 =
Lo resinyable d'ista versión inclui a dentrada d'o braille contraito, o suporte pa las nuevas voces Windows OneCore disponibles en o Windows 10, o suporte pa l'OCR integrau en o Windows 10 y muitas milloras significativas referents a o Braille y a la web.

== Nuevas Caracteristicas ==
- S'ha adhibiu una opción Braille a "amostrar os mensaches indefinidament". (#6669)
- En a lista de mensaches d'o Microsoft Outlook, o NVDA agora anuncia si bell mensache ye marcau. (#6374)
- En o Microsoft PowerPoint agora s'anuncia o tipo exacto d'una forma en que s'edita una diapositiva tal como trianglo, cerclo, vidio, flecha, en cuenta de nomás "forma". (#7111)
- O conteniu matematico (furniu como MathML) agora se suporta en o Google Chrome. (#7184)
- O NVDA agora puet charrar fendo servir as nuevas voces Windows OneCore (tamién conoixidas como voces mobils) incluidas en o Windows 10. Accedes ta ellas trigando Voces Windows OneCore en o dialogo de sintetizadors d'o NVDA. (#6159)
- Os fichers de configuración de l'usuario d'o NVDA agora se pueden almagazenar en o directorio local de datos d'aplicación de l'usuario. Ixo s'activa a traviés d'una propiedat en o rechistro. Mira-te 'parametros d'o sistema' en a guida de l'usuario pa mas detalles. (#6812)
- En os navegadors web o NVDA agora anuncia as valors d'os marcadors de posición d'os campos (especificament, agora se suporta aria-placeholder). (#7004)
- En o modo de navegación pa o Microsoft Word agora ye posible navegar por as  errors d'ortografía fendo servir a navegación rapeda (w y mayus+w) (#6942)
- S'ha adhibiu suporte pa o control selector de data trobau en os dialogos d'escayecimiento d'o Microsoft Outlook. (#7217)
- A sucherencia actualment seleccionada agora s'anuncia en os campos pa y cc d'o correu d'o Windows 10 y o campo de busca d'o Windows 10. (#6241)
- Agora se reproduz un son pa endicar l'aparición d'as sucherencias en bells campos de busca en o Windows 10 (p. eix. pantalla d'inicio, opcions de busca, campos pa y cc d'o correu d'o Windows 10). (#6241)
- O NVDA agora anuncia automaticament as Notificacions en o Skype de negocio pa l'escritorio  tals como quan belún prencipia una conversa con tu.  (#7281)
- O NVDA agora anuncia automaticament os mensaches de conversa dentrants entre que se siga en una conversa en o Skype pa negocios. (#7286)
- O NVDA agora anuncia automaticament as notificacions en o Microsoft Edge tals como quan prencipia bella descarga.  (#7281)
- Agora puetz escribir tanto en braille contraito como en no contraito en una linia braille con un teclau braille. Mira-te a secciónde dentrada braille d'a guida de l'usuario pa detalles. (#2439)
- Agora puetz ficar caracters braille Unicode dende o teclau braille en una linia braille seleccionando braille Unicode como a tabla de dentrada en as opcions d'o braille. (#6449)
- S'ha adhibiu o suporte pa la linia braille SuperBraille emplegada en Taiwán. (#7352)
- Nuevas tablas de transcripción braille: braille danés computerizau de 8 puntos, Lituano, braille persa computerizau de 8 puntos, Persa grau 1, braille Esloveno computerizau de 8 puntos. (#6188, #6550, #6773, #7367)
- S'ha amillorau a tabla d'o braille anglés computerizau de 8 puntos (U.S.), incluindo o suporte pa vinyetas, o signo d'euro y as letras accentugadas. (#6836)
- O NVDA agora puet emplegar a funcionalidat OCR incluida en o Windows 10 pa reconoixer o texto d'imachens u d'aplicacions inaccesibles. (#7361)
 - L'idioma se puet configurar dende o nuevo dialogo OCR d'o Windows 10 en as preferencias d'o NVDA.
 - Pa reconoixer o conteniu d'o navegador d'obchectos actual preta NVDA+r.
 - Consulta la sección de reconoixencia de Contenius d'a Guida de l'usuario pa detalles adicionals.
- Agora puetz esleyir qué información de contexto s'amuestra en una linia braille quan bell obchecto tien o foco fendo servir a nueva opción "Presentación de contexto d'o foco" en o dialogo d'opcions d'o Braille. (#217)
 - Por eixemplo, as opcions "replenar a pantalla pa cambios de contexto" y "nomás en desplazar-se-ne enta zaga" pueden fer que treballar con as listas y menús siga mas eficient, ya que os elementos no cambiarían continament a suya posición en a linia.
 - Consulta la sección en a opción "Presentación de contexto d'o foco" en a Guida de l'usuario pa detalles adicionals y eixemplos.
- En o Firefox y o Chrome o NVDA agora suporta reixetas dinamicas compleixas tals como fuellas de cálculo end que nomás se puet cargar u amostrar una parti d'o conteniu (especificament os atributos aria-rowcount, aria-colcount, aria-rowindex y aria-colindex introducius en ARIA 1.1). (#7410)


== Cambios ==
- S'ha adhibiu una orden no vinculada (script_restart) pa permitir renchegar o NVDA rapedament. Puetz trobar-la en a categoría Miscelania d'o dialogo de cenyos de dentrada. (#6396)
- A distribución d'o teclau agora se puet configurar dende o dialogo de bienvenida d'o NVDA. (#6863)
- S'ha abreviau muitos más tipos de controls y estaus en braille. Os puntos de referencia tamién s'han abreviaus. Porfavor consulta "Tipo de control, estau y abreviaduras de Puntos de Referencia" en Braille en a guida de l'usuario pa una lista completa. (#7188, #3975)
- S'ha esviellau l'eSpeak-ng ta 1.49.1 (#7280).
- As listas de tablas de dentrada y de salida en o dialogo d'opcions d'o Braille agora s'ordinan alfabeticament. (#6113)
- S'ha esviellau o transcriptor braille liblouis ta 3.2.0. (#6935)
- A tabla braille predeterminada agora ye braille anglés unificau codigo Grau 1. (#6952)
- Por defecto lo NVDA agora no amuestra que as partis d'a información d'o contexto que haigan cambiadas en una linia braille en que s'enfoque un obchecto. (#217)
 - Anteriorment amostraba siempre tanta información como estase posible independientment de si hebas visto a mesma información d'o contexto antis.
 - Puetz tornar ta l'anterior cambiando a nueva opción "Presentación d'o Contexto d'o Foco" en o dialogo d'opcions d'o Braille ta "replenar Siempre a pantalla".
- En emplegar o braille, o cursor se puet configurar pa tener una forma diferent en seguir a lo foco u a la revisión. (#7112)
- O logo d'o NVDA s'ha esviellau. O logo esviellau d'o NVDA ye una mezcla estilizada d'as letras NVDA en blanco sobre un fondo soliu purpura. Ixo asegura que será visible en qualsiquier color de fundo, y ferá servir a color purpura d'o logo de NV Access. (#7446)


== Corrección d'errors ==
- Os elementos div editables en o Chrome ya no tienen a suya etiqueta anunciada como a suya valor entre que se siga en o modo de navegación. (#7153)
- Pretar a fin entre que se ye en o modo de navegación d'un documento laso d'o Microsoft Word ya no fa una error en tiempo d'execución. (#7009)
- O modo de navegación agora se suporta correctament en o Microsoft Edge quan a un documento se l'haiga dau bel rol ARIA especifico de documento. (#6998)
- En o modo de navegación agora puetz seleccionar u deseleccionar dica la fin d'a linia fendo servir mayus+fin mesmo quan o cursor siga sobre o zaguer caracter d'a linia. (#7157)
- Si bell dialogo contién una barra de progreso, o texto d'o dialogo agora s'esviella en braille en que a barra de progreso cambeye. Ixo significa, por eixemplo, que o tiempo restant agora puet leyer-se en o dialogo d'o NVDA "Se son descargando Actualizacions". (#6862)
- O NVDA agora anunciará os cambios de selección pa bells quadros combinaus d'o Windows 10 tals como as opcions d'autoreproducción. (#6337).
- A información inservible ya no s'anuncia en dentrar en dialogos de creyación de conferencias u escayecimientos en o Microsoft Outlook. (#7216)
- Os chuflius pa dialogos de barra de progreso indeterminada tals como o comprebador d'actualizacions nomás quan a salida de barras de progreso ye configurada pa includir chuflius. (#6759)
- En o Microsoft Excel 2007 y 2003 se torna a anunciar as celdas en mover-se-ne por una fuella de treballo. (#8243)
- En l'actualización Windows 10 Creators y posteriors s'asegura que o modo de navegación s'activa de nuevas automaticament en leyer correus electronicos en o correu d'o Windows 10. (#7289)
- En a mas gran parti de linias braille con un teclau braille, o punto 7 agora borra a zaguera celda u caracter braille ficau, y o punto 8 preta a tecla intro. (#6054)
- En o texto editable, en mover o cursor (p. eix. con as teclas d'o cursor u retroceso), a respuesta charrada d'o NVDA agora ye mas precisa en muitos casos, especialment en o Chrome y as aplicacions de terminal. (#6424)
- Agora se puet leyer o conteniu de leditor de sinyaturas en o Microsoft Outlook 2016. (#7253)
- En as aplicacions de Java Swing o NVDA ya no fa que l'aplicación se penche bella vez en navegar por as tablas. (#6992)
- En l'actualización Windows 10 Creators, o NVDA ya no anunciará las notificacions de birosta qualques veces. (#7128)
- En o menú Inicio d'o Windows 10 en pretar l'intro pa zarrar-lo dimpués d'una busca ya no se produz que o NVDA anuncie mirar texto. (#7370)
- Fer a navegación rapeda por capiters agora ye significativament mas rapedo en o Microsoft Edge. (#7343)
- En o Microsoft Edge a navegación en o modo de navegación ya no se brinca seccions largas de bellas pachinas web tals como o tema WordPress 2015. (#7143)
- En o Microsoft Edge os puntos de referencia se localizan correctament en atros idiomas diferents a l'anglés. (#7328)
- O braille agora sigue correctament a selección en seleccionar texto dillá de l'amplo d'a pantalla. Por eixemplo, si seleccionas qualques linias con mayus+flecha abaixo, o braille agora amuestra la zaguera linia que seleccionés. (#5770)
- En o Firefox o NVDA ya no anuncia falsament "sección" qualques veces en ubrir os detalles pa un tuit en o twitter.com. (#5741)
- Os comandos de navegación de tabla ya no son disponibles pa las tablas de disenyo en o modo de navegación, fueras que l'anunciau d'as tablas de disenyo siga activau. (#7382)
- En o Firefox y o Chrome os comandos de navegación de tablas en o modo de navegación agora omiten as celdas ocultas d'a tabla. (#6652, #5655)


== Cambios pa os desembolicadors ==
 - As calendatas en o rechistro agora incluyen os milisegundos. (#7163)
- O NVDA agora s'ha de construir con Visual Studio Community 2015. O Visual Studio Express ya no se suporta. (#7110)
 - Tamién se requiere agora as ferramientas y o SDK d'o Windows 10  que se pueden activar en instalar o Visual Studio.
 - Mira-te a sección de dependencias instaladas d'o leye-me pa detalles adicionals.
- O suporte pa reconoixedors de conteniu tals como as ferramientas OCR y descripción d'imachen pueden implementar-se facilament fendo servir o nuevo paquete contentRecog. (#7361)
- Agora s'inclui o paquete de Python json package en as compilacions binarias d'o NVDA. (#3050)


= 2017.2 =
Lo resinyable d'ista versión inclui suporte completo pa l'achiquida d'audio en l'actualización Creators d'o Windows 10, apanyos pa qualques problemas de selección en o modo de navegación, incluindo problemas con seleccionar-lo tot, milloras significants en o suporte d'o Microsoft Edge y milloras en a web tals como a indicación d'elementos marcaus como actuals (fendo servir aria-current).

== Nuevas Caracteristicas ==
- Agora se puet anunciar a información d'os cantos d'a celda en o Microsoft Excel fendo servir `NVDA+f`. (#3044)
- En os navegadors web o NVDA agora indica quan bell elemento ye marcau como actual (especificament, fendo servir l'atributo aria-current). (#6358)
- Agora se suporta o cambio automatico d'idioma en o Microsoft Edge. (#6852)
- S'ha adhibiu suporte pa la calculadera d'o Windows en o Windows 10 Enterprise LTSB (Long-Term Servicing Branch) y Server. (#6914)
- Fendo lo comando de leyer a linia actual tres veces a escape letreya a linia con descripcions de caracter. (#6893)
- Nuevo idioma: Birmán.
- As flechas d'alto y abaixo y os simbolos Unicode fraccionals agora se charran apropiadament. (#3805)


== Cambios ==
- En navegar con a revisión simpla en as aplicacions que fan servir l'UI Automation agora s'ignora mas obchectos extranios fendo a navegación mas facil. (#6948, #6950) 


== Corrección d'errors ==
- Agora se puet activar elementos de menú d'as pachinas web estando en o modo de navegación. (#6735)
- Pretar o escape entre que o dialogo "confirmar a eliminación" d'o perfil de configuración ye activo agora zarra o dialogo. (#6851)
- S'ha apanyau bella crebadura en o Mozilla Firefox y atras aplicacions Gecko en que a caracteristica de multiproceso ye activada. (#6885)
- L'anunciau d'a color de fundo en a revisión de pantalla agora ye mas precisa quan o texto se dibuixó con un fundo transparent. (#6467) 
- S'ha amillorau o suporte pa as descripcions de control furnidas en as pachinas web en l'Internet Explorer 11 (especificament, o suporte pa aria-describedby adintro d'iframes y quan se furneix qualques IDs). (#5784)
- En l'actualización Creators d'o Windows l'achiquida d'audio d'o NVDA marcha unatra vez como en versions anteriors d'o Windows (p.eix. achiquir en que salga voz y sons, achiquir siempre y no achiquir nunca, son todas disponibles). (#6933)
- O NVDA ya no fallará en navegar u en anunciar qualques controls (UIA) en que no bi ha definiu garra alcorce de teclau. (#6779)
- Ya no s'adhibe dos espacios lasos en a información d'os alcorces de teclau pa bells controls (UIA). (#6790)
- Bellas combinacions de teclas en linias HIMS (p.eix. espacio+punto4) ya no fallan intermitentment. (#3157)
- S'ha apanyau un problema en ubrir bell puerto serie en sistemas que fan servir bell idioma diferent de l'anglés que feba que fallase a connexión con as linias braille en bells casos. (#6845)
- S'ha achiquiu a prebabilidat que os fichers de configuración se corrompan en apagar-se o Windows. Os fichers de Configuración agora s'escriben en un fichero temporal antis de no reemplazar o fichero de configuración real. (#3165)
- En fer o comando de leyer a linia actual dos veces a escape pa letreyar a linia agora s'emplega l'idioma apropiau pa os caracters letreyaus. (#6726)
- Navegar por linias en o Microsoft Edge agora ye mas de 3 veces mas rapedo en l'actualización Creators d'o Windows 10. (#6994)
- O NVDA ya no anuncia "Web Runtime grouping" en enfocar documentos d'o Microsoft Edge en l'actualización Creators d'o Windows 10. (#6948)
- Agora se suporta todas as versions existents d'o SecureCRT. (#6302)
- L'Adobe Acrobat Reader ya no se creba en bells documentos PDF (especificament, ixos que contienen atributos ActualText lasos). (#7021, #7034)
- En o modo de navegación en o Microsoft Edge, as tablas interactivas (ARIA grids) ya no se brincan en navegar ta tablas con t y mayus+t. (#6977)
- En o modo de navegación, pretar mayus+inicio dimpués de seleccionar agora torna deseleccionando t'o prencipio d'a linia como s'aspera. (#5746)
- En o modo de navegación, seleccionar-lo tot (control+a) ya no falla en seleccionar tot o texto si o cursor no ye en o prencipio d'o texto. (#6909)
- S'ha apanyau belatros preblemas extranios de selección en o modo de navegación. (#7131)


== Cambios pa os desembolicadors ==
- Os argumentos d'a linia de comandos agora se procesan con o modulo argparse d'o Python en cuenta de l'optparse. Ixo permite bellas opcions como -r y -q pa estar manullada exclusivament (#6865)
- O core.callLater agora mete en coda la tornada de clamada a la coda prencipal d'o NVDA dimpués d'a tardanza dada en cuenta d'eixecutar-la dreitament dispertando a o nuclio. Ixo atura posibles crebaduras debidas a que o nuclio se'n vaiga a adormir accidentalment dimpués de procesar una clamada, en meyo d'una clamada modal tal como lamostrau de bell quadro de mensache. (#6797) 
- A propiedat InputGesture.identifiers s'ha cambiau de tal traza que ya no se normaliza. (#6945)
 - A las subclases ya no les fa falta normalizar os identificadors antis de no tornar-los dende ista propiedat.
 - Si quiers normalizar os identificadors agora bi ha una propiedat InputGesture.normalizedIdentifiers que normaliza os identificadors tornaus por a propiedat identifiers.
- A propiedat InputGesture.logIdentifier agora ye obsoleta. As clamadas habrían a fer servir InputGesture.identifiers[0] en cuenta. (#6945)
- S'ha borrau bell codigo obsoleto:
 - As constans `speech.REASON_*`: S'habría de fer servir en cuenta `controlTypes.REASON_*`. (#6846)
 - `i18nName` pa las opcions de sintetizador: S'habría de fer servir en cuenta `displayName` y `displayNameWithAccelerator`. (#6846, #5185)
 - `config.validateConfig`. (#6846, #667)
 - `config.save`: S'habría de fer servir en cuenta `config.conf.save`. (#6846, #667)
- A lista de completacions en o menu contextual d'autocompletau d'o PythonConsole ya no amuestra  qualsiquier rota d'obchecto que leve t'o simbolo final que ye estando completau. (#7023)
- Agora bi ha una biblioteca de prebas unitarias pa o NVDA. (#7026)
 - As prebas unitarias y a infraestructura se troba en o directorio tests/unit. Mirar-se o texto de documentación en o fichero tests\unit\__init__.py pa mas detalles.
 - Puetz correr prebas fendo servir "scons tests". Mirar-se a sección "Running Tests" d'o readme.md pa mas detalles.
 - Si yes puyando una petición de pull pa o NVDA en primeras has de correr as prebas y asegurar-te que pasan.


= 2017.1 =
O resinyable d'ista versión inclui l'anunciau de seccions y columnas de texto en o Microsoft Word, Suporte pa leyer, navegar y anotar libros en o Kindle pa PC y suporte amillorau pa o Microsoft Edge.

== Nuevas Caracteristicas ==
- En o Microsoft Word Agora se puet anunciar os tipos de brincos de sección y os numers de sección. Ixo s'enchega con a opción "anunciar os numers de pachina" en o dialogo de formatiau de documentos. (#5946)
- En o Microsoft Word agora se puet anunciar as columnas de texto. Ixo s'activa con a opción "anunciar os numers de pachina" en o dialogo de formatiau de documentos. (#5946)
- Agora se suporta o cambio automatico d'idioma en o WordPad. (#6555)
- O comando de busca d'o NVDA (NVDA+control+f) agora se suporta en o modo de navegación en o Microsoft Edge. (#6580)
- A navegación rapeda pa os botons en o modo de navegación (b y mayus+b) agora se suporta en o Microsoft Edge. (#6577)
- Se remera os capiters de columna y ringlera en copiar bella fuella en o Microsoft Excel. (#6628)
- Suporte pa leyer y navegar por libros en a versión 1.19 d'o Kindle pa PC, incluindo acceso t'os vinclos, notas a o piet, graficos, texto resaltau y notas d'usuario. Mira-te a sección d'o Kindle pa PC d'a guida de l'usuario d'o NVDA pa información mas detallada. (#6247, #6638)
- Agora se suporta a navegación por tablas en o modo de navegación en o Microsoft Edge. (#6594)
- En o Microsoft Excel, o comando pa anunciar a ubicación d'o cursor de revisión (escritorio: NVDA+suprimir d'o teclau numerico, portatil: NVDA+suprimir) agora anuncia o nombre d'a fuella de treballo y a ubicación d'a celda. (#6613)
- S'ha adhibiu una opción a lo dialogo de salida pa reenchegar con libel de rechirstro de depuración. (#6689)


== Cambios ==
- A velocidat minima d'o esparpello d'o cursor braille agora ye de 200 ms. Si s'establió anteriorment por debaixo d'ixo se puyará ta 200 ms. (#6470)
- S'ha adhibiu una caixeta de verificación a lo dialogo d'opcions d'o braille pa permitir enchegar u desenchegar o esparpello d'o cursor braille. Anteriorment se feba servir una valor de 0 pa aconseguir ixo. (#6470)
- S'ha esviellau o eSpeak-NG (verificación e095f008, 10 de chinero d'o 2017). (#6717)
- A causa de cambios en l'actualización Creators d'o Windows 10 o modo "achiquir siempre" ya no ye disponible en as opcions d'achiquida d'audio d'o NVDA. Agún ye disponible en versions anteriors d'o windows 10. (#6684)
- A causa de cambios en l'actualización Creators d'o Windows 10 o modo "achiquir en que salga voz y sons" ya no puet guarenciar que l'audio s'achica de tot antis de no empecipiar a charrar ni que se mantienga achiquiu o tiempo suficient dimpués de charrar pa aturar a recutida rapeda en o volumen. Ixos cambios no afectan a  versions anteriors d'o windows 10. (#6684)


== Corrección d'errors ==
- S'ha apanyau a conchelación d'o Microsoft Word en mover-se-ne por paragrafos a traviés d'un documento largo entre que se ye en o modo de navegación. (#6368)
- As tablas en o Microsoft Word que s'haigan copiadas dende o Microsoft Excel ya no se tractan como tablas de disenyo y por ixo ya no s'ignoran. (#5927)
- En mirar d'escribir en o Microsoft Excel estando en una envista protechida, o NVDA agora fa un son en cuenta de dicir os caracters que realment no s'han escritos. (#6570)
- Pretar o escape en o Microsoft Excel ya no cambia incorrectament t'o modo de navegación, difuera que l'usuario haiga cambiau previament t'o modo de navegación explicitament con NVDA+espacio y siga dentrau to modo de foco pretando l'intro en un campo de formulario. (#6569) 
- O NVDA ya no se conchela en fuellas de calculo d'o Microsoft Excel en que se mezcle bella ringlera u columna completa. (#6216)
- L'anunciau de texto retallau u sobreixiu  en celdas d'o Microsoft Excel habría a estar mas preciso. (#6472)
- O NVDA agora anuncia quan bella caixeta de verificación ye de nomás lectura. (#6563)
- O disparador d'o NVDA ya no amostrará un dialogo d'alvertencia quan no se pueda reproducir o son d'inicio debiu a que o dispositivo d'audio no siga disponible. (#6289)
- Os Controls en a cingla d'o Microsoft Excel que no sigan disponibles agora s'anuncian como tals. (#6430)
- O NVDA ya no anunciará "panel" en minimizar finestras. (#6671)
- Agora se charra os caracters escritos en as aplicacions d'a plataforma universal d'o Windows (UWP) (incluindo lo Microsoft Edge) en l'actualización Creators d'o Windows 10. (#6017)
- O seguimiento d'o churi agora marcha a traviés de todas as pantallas en os ordinadors con qualques monitors. (#6598)
- O NVDA ya no esdeviene inemplegable dimpués de salir d'o Windows Media Player entre que o foco ye en bell control eslizant. (#5467)


== Cambios pa os desembolicadors ==
- Os perfils y os fichers de configuración agora s'esviellan automaticament pa meter-ie os requisitos d'as modificacions d'o esquema. Si bi ha bella error mientras l'actualización s'amuestra una notificación, a configuración se reenchega y o viello fichero de configuración ye disponible en o rechistro d'o NVDA en libel 'Info'. (#6470)


= 2016.4 =
Lo resinyable d'ista versión inclui a millora d'o refirme pa o Microsoft Edge, modo de navegación en l'aplicación Correo d'o Windows 10 y milloras significativas en os dialogos d'o NVDA.

== Nuevas caracteristicas ==
- O NVDA agora puet endicar a sangría de linia fendo servir tons. Ixo se puet configurar fendo servir o quadro combinau d'anunciar a sangría de linia en o dialogo de preferencias de formatiau de documentos d'o NVDA. (#5906)
- Refirme pa la linia braille Orbit Reader 20. (#6007)
- S'ha adhibiu una opción pa ubrir a finestra d'o visor d'a voz en rancar. Ixo se puet enchegar a traviés d'una caixeta de verificación en a finestra d'o visor d'a voz. (#5050)
- Agora se restaurará la ubicación y as dimensions en reubrir a finestra d'o visor d'a voz. (#5050)
- Os campos de referencia cruzada en o Microsoft Word agora se tractan como hipervinclos. S'anuncian como vinclos y pueden estar activaus. (#6102)
- Refirme pa las linias braille Baum SuperVario2, Baum Vario 340 y HumanWare Brailliant2. (#6116)
- Refirme Inicial pa l'actualización Anniversary d'o Microsoft Edge. (#6271)
- Agora s'emplega o modo de navegación quan se leye correus electronicos en l'aplicación Correo d'o Windows 10. (#6271)
- Nuevo idioma: Lituán.


== Cambeos ==
- Esviellau lo transcriptor braille liblouis t'o 3.0.0. Ixo inclui milloras significativas pa lo braille anglés unificau. (#6109, #4194, #6220, #6140)
- En l'administrador de complementos os botons de desenchegar complemento y enchegar complemento agora tienen alcorces de teclau (alt+d y alt+e respectivament). (#6388)
- S'ha resuelto qualques problemas de repleno y aliniación en os dialogos d'o NVDA. (#6317, #5548, #6342, #6343, #6349)
- S'ha achustau o dialogo de formatiau de documentos de traza que o conteniu s'eslice. (#6348)
- S'ha achustau a distribución d'o dialogo de pronuncia de simbolos de traza que l'amplo completo d'o dialogo s'emplegue pa la lista de simbolos. (#6101)
- os comandos de navegación d'una sola letra pa campos d'edición (e y mayus+e) y pa campos de formulario (f y mayus+f) agora se pueden fer servir pa mover-se-ne ta campos d'edición de nomás lectura en o modo de navegación en os navegadors web. (#4164)
- En o dialogo de formatiau de documentos d'o NVDA "Anunciar os cambeos dimpués d'o cursor" s'ha renombrau pa que afecte tanto a lo braille como a la voz (en a traducción aragonesa no bi ha diferencia). (#6336)
- S'ha achustau l'apariencia d'o dialogo de bienvenida d'o NVDA. (#6350)
- Os quadros de dialogo d'o NVDA agora tienen os botons d'acceptar y cancelar aliniaus a la dreita d'o dialogo. (#6333)
- Agora s'emplega controls de chiro pa os campos de texto numericos como a opción "porcentache de cambeo en o ton pa las mayusclas" en o dialogo d'opcions de voz. Puetz ficar-ie a valor desiada u fer servir as teclas de flecha alto u abaixo pa achustar-ie a valor. (#6099)
- O modo d'anunciar os IFrames (documentos integraus adintro de documentos) s'ha feito mas consistent pa os navegadors web. Os IFrames agora s'anuncian como "bastida" en o Firefox. (#6047)


== Corrección d'errors ==
- S'ha apanyau una error rara en salir d'o NVDA entre que o visor d'a voz ye ubierto. (#5050)
- Os mapas d'imachen agora se procesan como s'aspera en o modo de navegación en o Mozilla Firefox. (#6051)
- Estando en o dialogo d'o diccionario, pretar a tecla intro agora alza qualsiquier cambio que haigas feito y zarra o dialogo. Antis pretar-ie l'intro no feba cosa. (#6206)
- Agora s'amuestra en braille mensaches en cambiar os modos de dentrada pa bell metodo de dentrada (dentrada nativa/alfanumerica, forma completa/meya forma, etc.). (#5892, #5893)
- En desenchegar y reenchegar immediatament, u viceversa,  bell complemento agora o suyo estau torna correctament t'o que yera anteriorment. (#6299)
- Quan s'emplega o Microsoft Word agora se puet leyer os campos de numero de pachina en as capiteras. (#6004)
- Agora se puet fer servir o churi pa mover o foco entre a lista de simbolos y os campos d'edición en o dialogo de pronuncia de simbolos. (#6312)
- En o modo de navegación en o Microsoft Word s'ha apanyau un problema que feba que deixase d'apareixer a lista d'elementos quan un documento conteneba un hipervinclo invaliu. (#5886)
- Dimpués d'haber-se zarrau a traviés d'a barra de quefers u l'alcorce alt+F4, a caixeta de verificación d'o visualizador d'a voz en o menú d'o NVDA refleixará a visibilidat real d'a finestra. (#6340)
- O comando de reenchegar complementos ya no causa problemas pa os perfils de configuración disparaus, os nuevos documentos en os navegadors web y a revisión de pantalla. (#2892, #5380)
- En a lista d'idiomas en o dialogo d'opcions chenerals d'o NVDA, idiomas como l'aragonés agora s'amuestran correctament en o Windows 10. (#6259)
- As teclas emuladas d'o teclau d'o sistema (p. eix. un botón en una linia braille que emula pretar a tecla tabulador) agora se presentan en l'idioma configurau n o NVDA en l'aduya de dentrada y en o dialogo de cenyos de dentrada. Anteriorment siempre se presentaban en anglés. (#6212)
- Agora cambiar l'idioma d'o NVDA (dende o dialogo d'opcions chenerals) no fa efecto dica que se reenchega o NVDA. (#4561)
- O campo "patrón" ya no se puet deixar laso pa una nueva dentrada de diccionario. (#6412)
- S'ha apanyau un problema raro en escaniar os puertos serie en bels sistemas que feba inemplegables bells controladors de linias braille. (#6462)
- En o Microsoft Word agora se leye as vinyetas Numeradas en celdas de tabla en mover-se-ne por celdas. (#6446)
- Agora ye posible asignar cenyos a comandos pa o controlador d'a linia braille Handy Tech en o dialogo de cenyos de dentrada d'o NVDA. (#6461)
- En o Microsoft Excel pretar l'intro u l'intro d'o teclau numerico mientras se navega por una fuella de calculo agora anuncia correctament a navegación t'a siguient ringlera. (#6500)
- L'iTunes ya no se cala intermitentment pa cutio quan s'emplega o modo de navegación pa l'iTunes Store, Apple Music, etc. (#6502)
- S'ha apanyau crebaduras en as aplicacions de 64 bits basadas en Mozilla y Chrome. (#6497)
- En o Firefox con o multiproceso enchegau o modo de navegación y os campos de texto editable agora marchan correctament. (#6380)


== Cambeos pa Desembolicadors ==
- Agora ye posible furnir modulos d'aplicación pa executables que contiengan un punto (.) en os suyos nombres. Os puntos s'han reemplazau por guions baixos (_). (#5323)
- O nuevo modulo gui.guiHelper inclui utilidatz pa fer simpla la creyación de GUIs de wxPython, incluindo a chestión automatica d'o espaciau. Ixo fa muito mas facil l'apariencia visual y a consistencia, igual como a creyación facil de nuevas GUIs pa desembolicadors ciegos. (#6287)


= 2016.3 =
O resinyable d'ista versión inclui a capacidat de desenchegar complementos individuals, refirme pa campos de formulario en o Microsoft Excel, importants milloras en l'anunciau d'as colors, apanyos y milloras referents a qualques linias braille y apanyos y milloras pa o refirme d'o Microsoft Word.

== Nuevas caracteristicas ==
- O modo de navegación agora se puet fer servir pa leyer documentos PDF en o Microsoft Edge. (#5740)
- Agora s'anuncia a rayadura y a dople rayadura  si ye apropiau en o Microsoft Word. (#5800)
- En o Microsoft Word agora s'anuncia o titol d'una tabla si se'n ha furniu un. Si bi ha bella descripción se puet accedir ta ella fendo servir o comando d'ubrir a descripción luenga (NVDA+d) en o modo de navegación. (#5943)
- En o Microsoft Word o NVDA agora anuncia a información de posición en mover paragrafos (alt+mayus+flecha abaixo y alt+mayus+flecha alto). (#5945)
- En o Microsoft Word agora s'anuncia o espaciau de linia a traviés d'o comando d'o NVDA d'anunciar o formato quan se cambeye con qualques alcorces de teclau d'o Microsoft word y quan te'n muevas ta texto con diferent espaciau de linia si l'anunciau d'o espaciau de linia ye enchegau en as opcions de formatiau de documentos d'o NVDA. (#2961)
- En l'Internet Explorer agora se reconoix os elementos HTML 5 estructurals. (#6044)
- Agora se puet desenchegar l'anunciau de comentarios (como en o Microsoft Word) a traviés d'a caixeta de verificación d'anunciar os comentarios en o dialogo de formatiau de documentos d'o NVDA. (#5108)
- Agora ye posible desenchegar complementos individuals en l'administrador de complementos. (#3090)
- S'ha adhibiu asignacions de teclas adicionals pa las linias braille d'as series ALVA BC640/680. (#5206)
- Agora bi ha un comando pa mover a linia braille t'o foco actual. Actualment, nomás as series ALVA BC640/680 tienen una tecla asignada pa ixe comando, pero se puet asignar manualment pa atras linias en o dialogo de cenyos de dentrada si se deseya. (#5250)
- En o Microsoft Excel agora puetz interactuar con os campos de formulario. Mueve-te-ne ta campos de formulario usando a lista d'elementos u a navegación d'una sola letra en o modo de navegación. (#4953)
- Agora puetz asignar un cenyo de dentrada pa cambiar o modo de revisión simpla fendo servir o dialogo de cenyos de dentrada. (#6173)
- En a lista de mensaches de l'Outlook 2016 ya no s'anuncia la información de borrador asociada. (#6219)


== Cambeos ==
- O NVDA agora anuncia as colors fendo servir un conchunto basico de 9 tons de color y 3 matices de buen entender con variacions de brilo y esbufalera. Ixo ye millor que no fer servir nombres de color mas subchectivos y menos replecables. (#6029)
- S'ha modificau o comportamiento existent de NVDA+F9 y dimpués  NVDA+F10 pa seleccionar texto en a primer pretada de F10. Quan se preta F10 dos veces (en sucesión rapeda) se copia o texto en o portafuellas. (#4636)
- S'ha esviellau o eSpeak NG t'a versión Master 11b1a7b (22 de chunyo de 2016). (#6037)


== Corrección d'errors ==
- En o modo de navegación en o Microsoft Word agora se conserva o formato en copiar t'o portafuellas. (#5956)
- En o Microsoft Word o NVDA agora informa apropiadament quan se fa servir os comandos propios de navegación de tablas d'o Word (alt+inicio, alt+fin, alt+re.pach y alt+av.pach) y os comandos de selección de tablas (mayus adhibiu a os comandos de navegación). (#5961)
- En os quadros de dialogo d'o Microsoft Word s'ha amillorau a saber-lo a navegación d'obchectos d'o NVDA. (#6036)
- En qualques aplicacions como lo Visual Studio 2015 agora s'anuncia como s'asperaba os alcorces de navegación (p. eix. control+c pa copiar). (#6021)
- S'ha apanyau un problema raro en escaniar os puertos serie en bells sistemas que feba inutilizables bells controladors de linias braille. (#6015)
- L'anunciau de colors en o Microsoft Word agora ye mas preciso igual como agora se tién en cuenta os cambeos en os temas d'o Microsoft Office. (#5997)
- O modo de navegación pa o Microsoft Edge y o refirme pa las sucherencias de busca d'o menú d'inicio son unatra vez disponibles en compilacions d'o Windows 10 posteriors a abril de 2016. (#5955)
- En o Microsoft Word, a lectura automatica de capiters de tabla marcha millor quan se treballa con celdas combinadas. (#5926)
- En l'aplicacion Mail d'o Windows 10, o NVDA ya no falla en leyer o conteniu d'os mensaches. (#5635) 
- Ya no s'anuncia dos veces as teclas de bloqueyo como lo bloqueyo de mayusclas en estar enchegau o charrar as teclas d'ordens. (#5490)
- Os dialogos de control de cuentas d'usuario d'o Windows se leye correctament unatra vez en l'actualización Anniversary d'o Windows 10. (#5942)
- En o complemento Web Conference (como l'usau en out-of-sight.net) o NVDA ya no chufla y charra as actualizacions d'a barra de progreso referents a la dentrada d'o microfón. (#5888)
- En realizar un comando de buscar o siguient u buscar l'anterior en o modo de navegación agora se fará correctament una busca sensible a mayusclas si a busca orichinal yera sensible a las mayusclas. (#5522)
- En editar dentradas de diccionario agora s'obtién respuesta pa expresions regulars invalidas. O NVDA ya no se cala si un fichero de diccionario contién una expresión regular invalida. (#4834)
- Si o NVDA no ye capable de comunicar-se con una linia braille (p. eix. porque s'ha desconnectau) se desenchegará automaticament l'uso d'a linia. (#1555)
- S'ha amillorau licherament a realización de tresminaus en a lista d'elementos d'o modo de navegación en bells casos. (#6126)
- En o Microsoft Excel os nombres d'os patrons de fondo anunciaus por o NVDA agora coinciden con os usaus por l'Excel. (#6092)
- S'ha amillorau o refirme pa la pantalla d'inicio de sesión d'o Windows 10, incluindo l'anunciau d'alertas y l'activación d'o campo de clau con toque. (#6010)
- O NVDA agora detecta correctament os botons secundarios de seguimiento en as linias braille d'as series ALVA BC640/680. (#5206)
- O NVDA puet anunciar unatra vez as notificacions rustidas d'o Windows en compilacions recients d'o Windows 10. (#6096)
- O NVDA ya no deixa de reconoixer ocasionalment as pretadas de teclas en linias braille Baum compatible y HumanWare Brailliant B. (#6035)
- Si ye enchegau l'anunciau d'os numers de linia en as opcions de formatiau de documentos d'o NVDA agora s'amuestra os numers de linia en una linia braille. (#5941)
- Quan o modo de voz yed desactivau, l'anunciau d'obchectos (como pretar NVDA+tabulador pa anunciar o foco) agora amaneix en o visor d'a voz como s'asperaba. (#6049)
- En o Google Chrome y navegadors basaus en o Chrome en un idioma diferent de l'anglés o modo de navegación ya no deixa de marchar en qualques documentos. (#6249)


== Cambeos pa Desembolicadors ==
- A información d'inicio de sesión dreitament dende una propiedat ya no resulta en que a propiedat  siga clamada recursivament una y unatra vez. (#6122)


= 2016.2.1 =
Ista versión apanya penchaduras en o Microsoft Word:

- O NVDA ya no causa que o Microsoft Word se penche immediatament dimpués de rancar en o Windows XP. (#6033)
- S'ha retirau l'anunciau d'errors gramaticals ya que ixo causa penchaduras en o Microsoft Word. (#5954, #5877)


= 2016.2 =
O resinyable d'ista versión inclui a capacidat d'indicar as errors d'ortografía entre que s'escribe, refirme pa l'anunciau d'errors gramaticals en o Microsoft Word y milloras y apanyos pa o refirme d'o Microsoft Office.

== Nuevas caracteristicas ==
- En o modo de navegación en l'Internet Explorer y atros controls MSHTML, fendo servir a navegación con a primer letra pa mover-se-ne por as anotacións (a y mayus+a) agora se'n mueve t'o texto ficau y borrau. (#5691)
- En o Microsoft Excel, o NVDA agora anuncia o libel d'un grupo de celdas, asinas como si ye plegau u desplegau. (#5690)
- En pretar dos vegadas o comando d'anunciar o formato de texto (NVDA+f) se presienta la información en o modo de navegación y asinas se puet revisar. (#4908)
- En o Microsoft Excel 2010 y posteriors agora s'anuncia o uembrau de celdas y o degradau de repleno. L'anunciau automatico se controla con a opción d'anunciar as colors en as preferencias de Formatiau de Documentos d'o NVDA. (#3683)
- Nueva tabla de transcripción braille: Griego Koiné. (#5393)
- En o visor d'o rechistro agora puetz alzar o rechistro fendo servir l'alcorce de teclau control+s. (#4532)
- Si ye enchegau l'anunciau d'errors d'ortografía y suportau en o control enfocau, o NVDA reproducirá un son t'alvertir-te d'una error d'ortografía feita en ir escribindo. Ixo puet desenchegar-se fendo servir a nueva opción "Reproducir son pa las errors d'ortografía entre que s'escribe" en o dialogo d'opcions de teclau d'o NVDA. (#2024)
- Agora s'anuncia as errors gramaticals en o Microsoft Word. Ixo puet desenchegar-se fendo servir a nueva opción "Anunciar as errors gramaticals" en o dialogo d'opcions de formatiau de documentos d'o NVDA. (#5877)


== Cambeos ==
- En o modo de navegación y os campos de texto editable o NVDA agora tracta l'intro d'o teclau numerico igual como a tecla intro prencipal. (#5385)
- O NVDA ha cambiau t'o sintetizador de voz eSpeak NG. (#5651)
- En o Microsoft Excel o NVDA ya no ignora o capitero de columna pa una celda quan bi ha una ringlera en blanco entre a celda y o capitero. (#5396)
- En o Microsoft Excel agora s'anuncia las coordinadas antis d'os capiters pa eliminar l'ambiguedat entre os capiters y o conteniu. (#5396)


== Corrección d'errors ==
- En o modo de navegación, quan se mira de fer servir a navegación con una sola letra pa mover-se-ne ta un elemento que no se suporta en o documento, o NVDA anuncia que ixo no se suporta en cuenta de anunciar que no bi ha elemento en ixa adreza. (#5691)
- Quan se lista fuellas en a lista d'elementos en o Microsoft Excel, agora s'inclui as fuellas que nomás contiengan graficos. (#5698)
- O NVDA ya no anuncia información rara quan se cambie entre finestras en una aplicación Java con qualques finestras tals como l'IntelliJ u l'Android Studio. (#5732)
- En os editors basaus en Scintilla tals como lo Notepad++ o braille agora s'esviella correctament en mover o cursor fendo servir una linia braille. (#5678)
- O NVDA ya no peta de cabo ta quan en enchegar a salida braille. (#4457)
- En o Microsoft Word, a sangría de paragrafo agora s'anuncia siempre en a unidat de mida esleyida por l'usuario (p.eix. centimetros u pulgadas). (#5804)
- En usar una linia braille muitos mensaches d'o NVDA que antis nomás se charraban agora se meten en braille como cal. (#5557)
- En as aplicacions Java accesibles agora s'anuncia o libel d'os elementos d'as anvistas d'arbol. (#5766)
- Apanyadas as crebaduras en l'Adobe Flash en o Mozilla Firefox en bells casos. (#5367)
- En o Google Chrome y os navegadors basaus en o Chrome agora se puet leyer en o modo de navegación os documentos adintro de dialogos u aplicacions. (#5818)
- En o Google Chrome y os navegadors basaus en o Chrome agora puetz aforzar o NVDA a cambiar t'o modo de navegación en dialogos u aplicacions web. (#5818)
- En l'Internet Explorer y atros controls MSHTML mover o foco ta qualques controls (especificament, an que s'emplega aria-activedescendant) ya no cambia incorrectament t'o modo de navegación. Ixo ocurriba, por eixemplo, en mover-se-ne ta sucherencias en campos d'adreza quan se redacta un mensache en Gmail. (#5676)
- En o Microsoft Word o NVDA ya no se conchela en tablas grans quan l'anunciau de capiters de ringlera y columna ye enchegau. (#5878)
- En o Microsoft word o NVDA ya no anuncia incorrectament texto con unn libel d'esquema (pero no pas un estilo de capitero encorporau) como un capitero. (#5186)
- En o modo de navegación en o Microsoft Word agora marchan os comandos pa mover-se-ne t'a fin u lo prencipio d'o contenedor (coma y mayus+coma) pa las tablas. (#5883)


== Cambios pa Desembolicadors ==
- Os components de c++ d'o NVDA agora se compilan con o Microsoft Visual Studio 2015. (#5592)
- Agora puetz presentar un texto u mensache HTML a l'usuario en o modo de navegación fendo servir ui.browseableMessage. (#4908)
- En a guida de l'usuario, quan s'emplega una opción %kc command pa una opción que tien una tecla común pa todas as distribucions, a tecla agora se puet meter dimpués de dos puntos d'amplo completo (：) asinas como os dos puntos normals (:). (#5739)


= 2016.1 =
O resinyable d'ista versión inclui a capacidat de baixar opcionalment o volumen d'atros sons, milloras pa la salida de braille y suporte pa linias braille, qualques apanyos significants pa o suporte d'o Microsoft Office y apanyos pa o modo de navegación en l'iTunes.

== Nuevas caracteristicas ==
- Nuevas tablas de transcripción braille: Braille polaco computerizau de 8 puntos, Mongol. (#5537, #5574)
- Puetz desenchegar o cursor braille y cambiar a suya forma usando as nuevas opcions amostrar o cursor y forma d'o cursor en o dialogo d'opcions de braille. (#5198)
- O NVDA agora puet connectar-se a una linia braille HIMS Smart Beetle a traviés de bluetooth. (#5607)
- O NVDA puet opcionalment baixar o volumen d'atros sons si ye instalau en o Windows 8 u superiors. Ixo se puet configurar fendo servir a opción modo d'achiquida d'audio en o dialogo d'o sintetizador d'o NVDA u pretando NVDA+mayus+d. (#3830, #5575)
- Suporte pa l'APH Refreshabraille en o modo HID y a Baum VarioUltra y Pronto! en que se connecta a traviés d'USB. (#5609)
- Suporte pa las linias braille HumanWare Brailliant BI/B quan o protocolo s'estableix t'OpenBraille. (#5612)


== Cambios ==
- L'anunciau d'o enfasi agora ye desenchegau por defecto. (#4920)
- En o dialogo de lista d'elementos en o Microsoft Excel l'alcorz pa Formulas s'ha cambiau a alt+r asinas ye  diferent de  l'alcorz pa lo campo de tresminau. (#5527)
- Esviellau o transcriptor braille liblouis ta 2.6.5. (#5574)
- A parola "texto" ya no s'anuncia en mover o foco u lo cursor de revisión t'obchectos de texto. (#5452)


== Corrección d'errors ==
- En l'iTunes 12, o modo de navegación agora s'esviella correctament en que se carga una pachina nueva en a botiga de l'iTunes. (#5191)
- En l'Internet Explorer y atros controls MSHTML mover-se-ne ta libels especificos de capitero con a navegación d'una sola letra agora se comporta como s'aspera quan o libel d'un capitero ye sobreescrito pa propositos d'accesibilidat (especificament quan aria-level sobreescribe o libel d'una etiqueta h). (#5434)
- En o Spotify o foco ya no aterriza freqüentment en obchectos "desconoixius". (#5439)
- O foco agora s'esviella correctament en tornar t'o Spotify dende unatra aplicación. (#5439)
- En cambiar entre o modo de navegación y o modo de foco lo modo s'anuncia en braille igual como en fabla. (#5239)
- O botón d'inicio en a barra de quefers ya no s'anuncia como una lista y/u como seleccionau en bellas versions d'o Windows. (#5178)
- Os mensaches tals como "ficau" ya no s'anuncia en a redacción de mensaches en o Microsoft Outlook. (#5486)
- En usar una linia braille y seleccionar texto en a linia actual (p.eix. en mirar en un editor de texto texto que coincide en a mesma linia), a linia braille se posicionará si cal. (#5410)
- O NVDA ya no sale silenciosament en zarrar una consola de comandos d'o Windows con alt+f4 en o Windows 10. (#5343)
- En a lista d'elementos en o modo de navegación, en cambiar a mena d'elemento, agora s'escosca o campo "tresminar por". (#5511)
- En texto editable en as aplicacions de Mozilla, mover o churi leye unatra vegada a linia, parola, etc. apropiada como s'aspera en cuenta d'o conteniu entero. (#5535)
- En mover o churi en texto editable en aplicacions de Mozilla, a lectura ya no atura en elementos tals como vinclos adintro d'a parola u linia que ye estando leyida. (#2160, #5535)
- En l'Internet Explorer, o puesto web shoprite.com agora se puet leyer en o modo de navegación en cuenta d'anunciar-se como blanco. (especificament, os atributos malformaus d'o luengache agora se maneyan apropiadament.) (#5569)
- En o Microsoft Word, os cambeos seguius como "ficau" ya no s'anuncia quan no s'amostra a marca de seguimiento de cambeos. (#5566)
- En que un botón conmutable s'enfoca o NVDA agora anuncia en que cambie de pretau ta no pretau. (#5441)
- L'anunciau d'os cambeos d'a forma d'o churi torna a marchar como s'aspera. (#5595)
- En charrar o sangrau de linia os espacios de no crebadura agora se tractan como espacios normals. Anteriorment, ixo podeba causar anuncios tals como "espacio espacio espacio" en cuenta de  "3 espacios". (#5610)
- En zarrar una lista de metodos candidatos de dentrada de Microsoft moderno lo foco se restaura correctament ya siga t'a redacción de dentrada u t'o documento subchacent. (#4145)
- En o Microsoft Office 2013 y superiors, quan a cinta ye configurada pa amostrar nomás pestanyas, os elementos d'a cinta s'anuncian unatra vegada como s'aspera en que s'activa una pestanya. (#5504)
- Apanyos y milloras pa la detección y o enlazau de cenyos de pantalla tactil. (#5652)
- Os "hovers" d'a pantalla tactil ya no s'anuncia en l'aduya de dentrada. (#5652)
- O NVDA ya no falla en listar comentarios en a lista d'Elementos pa o Microsoft Excel si un comentario ye  en una celda combinada. (#5704)
- En un caso muit raro, o NVDA ya no falla en leyer o conteniu d'una fuella en o Microsoft Excel con l'anunciau de capiters de celda y columna enchegau (#5705)
- En o Google Chrome a navegación adintro d'una redacción de dentrada quan se fica caracters d'Asia de l'este ya no falla con una error. (#4080)
- En a busca d'Apple Music en l'iTunes o modo de navegación pa o documento d'os resultaus d'a busca agora s'esviella como s'aspera. (#5659)
- En o Microsoft Excel pretando mayus+f11 pa creyar una nueva fuella agora s'anuncia a tuya nueva posición en cuenta de no anunciar cosa. (#5689)
- Apanyaus problemas con a salida d'as linias braille en ficar caracters coreans. (#5640)


== Cambios pa Desembolicadors ==
- A nueva clase audioDucking.AudioDucker permit codigo que quita audio pa endicar dó habría d'achiquir-se l'audio de fundo. (#3830)
- O constructor d'o nvwave.WavePlayer agora tien a parola clau wantDucking como argumento que especifica si l'audio de fondo habría d'achiquir-se entre que se reproduce audio. (#3830)
 - Quan ixo siga enchegau (lo qual ye predeterminau), ye esencial que WavePlayer.idle se clame quan siga apropiau.
 - Amillorada la dentrada/salida pa linias braille: (#5609)
 - Os controladors Thread-safe d'as linias braille pueden declarar-sen como tals fendo servir l'atributo BrailleDisplayDriver.isThreadSafe. Un controlador debe estar thread-safe pa esquimenar-se d'as siguients caracteristicas:
 - Os datos s'escriben t'o controlador de linias braille thread-safe en segundo plan, amillorando asinas o rendimiento.
 - hwIo.Serial extendilla pyserial pa clamar un clamable en que os datos se reciben en cuenta de que os controladors haigan de mirar-los.
 - hwIo.Hid amane suporte pa que as linias braille se comuniquen a traviés d'USB HID.
 - hwPortUtils y hwIo pueden amanir opcionalment o rechistro detallau de depuración, incluindo os dispositivos trobaus y totz os datos ninviaus y recibius.
 - Bi ha qualques nuevas propiedatz accesibles en os cenyos de pantallas tactils: (#5652)
 - Os obchectos MultitouchTracker agora contienen una propiedat childTrackers que contién os MultiTouchTrackers d'os que o rastriador se composa. Por eixemplo, o truco dople con dos didos tien rastriadors fillos pa dos trucos con dos didos. Os trucos con dos didos tienen  rastriadors fillos pa dos trucos.
 - Os obchectos MultiTouchTracker agora contienen tamién una propiedat rawSingleTouchTracker si o rastriador estió lo resultau d'un solo dido que fa truco , raspiada u "hover". o SingleTouchTracker permit acceso ta l'ID subchacent asignau a lo dido por o sistema operativo y endica si o dido encara ye en contacto en o momento actual u no pas.
 - TouchInputGestures agora tien as propiedatz x y y, sacando a necesidat d'accedir t'o rastriador pa casos trivials.
 - TouchInputGestures agora contién una propiedat preheldTracker, que ye un obchecto MultitouchTracker que representa os atros didos mantenius entre que ista acción se ye fendo.
- Dos nuevos cenyos de pantalla tactil se puet emitir: (#5652)
 - Trucos plurals y mantener (p. eix. truco dople y mantener)
 - Un identificador cheneralizau con cuenta de didos borrau pa mantenimientos (p. eix. mantener+"hover" pa 1finger_hold+hover).


= 2015.4 =
O resinyable d'ista versión inclui milloras de rendimiento en o Windows 10, a inclusión en o centro d'accesibilidat en o Windows 8 y superiors, milloras t'o Microsoft Excel incluindo lo listau y renombramiento de fuellas y l'acceso ta celdas blocadas en fuellas protechidas y suporte t'a edición de texto rico en o Mozilla Firefox, o Google Chrome y o Mozilla Thunderbird.

== Nuevas Caracteristicas ==
- O NVDA agora amaneix en o centro d'accesibilidat en o Windows 8 y superiors. (#308)
- En mover-se-ne por as celdas en l'Excel os cambeos de formato agora s'anuncian automaticament si as opcions apropiadas son enchegadas en o dialogo d'opcions de formatiau de documentos d'o NVDA. (#4878)
- S'ha adhibiu una opción t'anunciar o enfasi en o dialogo d'opcions de Formatiau de Documentos d'o NVDA. Enchegada por defecto, ixa opción permit a lo NVDA anunciar automaticament a existencia de texto enfatizau en os documentos. Por agora no ye suportau que t'as etiquetas em y strong en o modo de navegación ta l'Internet Explorer y atros controls MSHTML. (#4920)
- A existencia de texto ficau y borrau s'anuncia agora en o modo de navegación ta l'Internet Explorer y atros controls MSHTML, si a opción d'o NVDA d'anunciar as revisións de l'editor ye activada. (#4920)
- En veyer o seguimiento  de cambeos en a lista d'elementos d'o NVDA t'o Microsoft Word agora s'amuestra más información tal como qué propiedatz d'o formato han cambiau. (#4920)
- Microsoft Excel: Agora ye posible listar y renombrar as fuellas dende a lista d'elementos d'o NVDA (NVDA+f7). (#4630, #4414)
- Agora ye posible configurar si os simbolos reals se ninvian t'o sintetizador d'a fabla (p.eix. ta causar una aturada u cambeo en a entonación) en o dialogo de pronuncia de simbolos. (#5234)
- En o Microsoft Excel o NVDA agora anuncia qualsiquier mensache de dentrada establiu por l'autor d'a fuella en as celdas. (#5051)
- Suporte t'as linias braille Baum Pronto! V4 y VarioUltra quan se connectan a traviés d'o Bluetooth. (#3717)
- Suporte t'a edición de texto rico en as aplicacions de Mozilla tals como lo Google Docs con o suporte braille activau en o Mozilla Firefox y a composición HTML en o Mozilla Thunderbird. (#1668)
- Suporte t'a edición de texto rico en o Google Chrome y os navegadors basaus en o Chrome tals como lo Google Docs con o suporte braille activau. (#2634)
 - Ixo requier a versión 47 d'o Chrome u superior.
- En o modo de navegación en o Microsoft Excel puetz navegar ta celdas blocadas en fuellas protechidas. (#4952)


== Cambeos ==
- A opción d'anunciar as Revisions de l'editor en o dialogo d'opcions de formatiau de documentos d'o NVDA agora s'enchega por defecto. (#4920)
- En mover-se-ne por os caracters en o Microsoft Word con a opción d'anunciar as revisions de l'editor d'o NVDA enchegada agora s'anuncia menos información  t'os cambeos de seguimiento, o que fa más eficient a navegación. Ta veyer a información extra fe servir a lista d'elementos. (#4920)
- Esviellau o transcriptor braille liblouis ta 2.6.4. (#5341)
- Quantos simbolos (incluindo simbolos matematicos basicos) se son movius t'o libel beluna ta que se leigan por defecto. (#3799)
- Si o sintetizador lo suporta, agora a fabla habría de pausar-se t'os parenthesis y o guión curto (–). (#3799)
- En seleccionar texto, o texto s'anuncia antis que no a indicación de selección en cuentas de dimpués. (#1707)


== Corrección d'errors ==
- Grans milloras de rendimiento  en navegar por a lista de mensaches de l'Outlook 2010 y 2013. (#5268)
- En un grafico en o Microsoft Excel, en navegar con qualques teclas (tals como cambiar de fuella con control+rePach y control+avPach) agora marcha correctament. (#5336)
- Apanyada l'aparencia visual d'os botons en o dialogo d'alvertencia que s'amuestra quan miras de baixar de versión o NVDA. (#5325)
- En o Windows 8 y superiors o NVDA agora ranca a saber-lo más rapedo quan ye configurau ta rancar dimpués d'encetar a sesión en o Windows. (#308)
 - Si activés ixo fendo servir una versión anterior d'o NVDA amenistarás desactivar-lo y activar-lo de nuevas ta que o cambeo tienga efecto. Sigue o siguient procedimiento:
  + Ubre o dialogo d'opcions chenerals.
  + Desmarca la caixeta encetar o NVDA automaticament dimpués d'autentificar-se en Windows.
  + Preta o botón d'acceptar.
  + Ubre o dialogo d'opcions chenerals unatra vegada.
  + Marca la caixeta encetar o NVDA automaticament dimpués d'autentificar-se en Windows.
  + Preta o botón d'acceptar.
- Milloras de rendimiento ta l'UI Automation incluindo explorador de fichers y visor de fainas. (#5293)
- O NVDA agora cambia correctament t'o modo de foco en que se tabula ta controls read-only ARIA grid en o modo de navegación t'o Mozilla Firefox y atros controls basaus en Gecko. (#5118)
- O NVDA agora anuncia correctament "no bi ha anterior" en cuenta de "no bi ha siguient" quan no bi ha más obchectos en  fer un truquet ent'a cucha en una pantalla tactil.
- Apanyaus problemas en escribir qualques parolas en o campo de tresmín en o dialogo de cenyos de dentrada. (#5426)
- O NVDA ya no se conchela en bells casos en reconnectar-se-ne a una linia HumanWare Brailliant BI/B series a traviés de l'USB. (#5406)
- En idiomas con caracters conchuntos as descripcions de caracters agora marchan como s'asperaba ta caracters angleses en mayuscla. (#5375)
- O NVDA ya no habría de conchelar-se ocasionalment en desplegar o menú d'inicio en o Windows 10. (#5417)
- En o Skype t'o escritorio as notificacions que s'amuestra antis que una notificación anterior no desapareixca agora s'anuncia. (#4841)
- As notificacions agora s'anuncia correctament en o Skype t'o escritorio 7.12 y superiors. (#5405)
- O NVDA agora anuncia correctament o foco en desplegar un menú contextual en bellas aplicacions como lo Jart. (#5302)
- En o Windows 7 y superiors a Color s'anuncia de nuevas en qualques aplicacions como lo Wordpad. (#5352)
- En editar en o Microsoft PowerPoint  pretar l'intro agora anuncia o texto ficau automaticament como una vinyeta u numero. (#5360)


= 2015.3 =
O resinyable d'ista versión inclui refirme inicial t'o Windows 10, a capacidat ta desenchegar a navegación d'una sola letra en o modo de navegación (util ta bellas aplicacions web), milloras en l'Internet Explorer y apanyos ta texto ilechible en escribir en qualques aplicacions con o braille enchegau.

== Nuevas Caracteristicas ==
- A existencia d'errors d'ortografía s'anuncia en os campos editables ta l'Internet Explorer y atros controls MSHTML. (#4174)
- Agora se leye muitos más simbolos matematicos unicode en que amaneixen en os textos. (#3805)
- As sucherencias de busca en a pantalla d'inicio d'o Windows 10 s'anuncia automaticament. (#5049)
- Refirme t'as linias braille EcoBraille 20, EcoBraille 40, EcoBraille 80 y EcoBraille Plus. (#4078)
- En o modo de navegación agora puetz enchegar y desenchegar a navegación d'una sola letra  pretando NVDA+mayus+espacio. Quan siga desenchegada as teclas d'una letra se pasan ta l'aplicación que ye util ta bellas aplicacions web tals como lo Gmail, o Twitter y o Facebook. (#3203)
- Nuevas tablas de transcripción braille; finlandés de 6 puntos, irlandés grau 1, irlandés grau 2, coreán grau 1 (2006), coreán grau 2 (2006). (#5137, #5074, #5097)
- Agora se suporta o teclau QWERTY en a linia braille Papenmeier BRAILLEX Live Plus. (#5181)
- Refirme experimental t'o navegador web Microsoft Edge y o motor de buscas en o Windows 10. (#5212)
- Nuevo idioma: Canadá.


== Cambeos ==
- Esviellau o transcriptor braille liblouis ta 2.6.3. (#5137)
- Quan mires d'instalar una versión más viella d'o NVDA que l'actualment  instalada, agora te s'alvertirá que ixo no ye recommendau y que o NVDA habrá de desinstalar-se de raso antis de no i proceder. (#5037)


== Corrección d'errors ==
- En o modo de navegación ta l'Internet Explorer y atros controls MSHTML, a navegación rapeda por campos de formularios ya no inclui incorrectament elementos de listas presentacionals. (#4204)
- En o Firefox o NVDA ya no anuncia inapropiadament o conteniu d'o panel de pestanyas ARIA en que o foco se'n mueve t'adintro d'ell. (#4638)
- En l'Internet Explorer y atros controls MSHTML en tabular enta seccions, articlos u dialogos  ya no s'anuncia inapropiadament tot o conteniu d'o contenedor. (#5021, #5025) 
- En fer servir linias braille Baum, HumanWare u APH con un teclau braille a dentrada braille ya no deixa de funcionar dimpués de pretar unatra mena de tecla en a linia. (#3541)
- En o Windows 10 ya no s'anuncia información rariza en pretar alt+tabulador u alt+mayus+tabulador ta cambiar entre aplicacions. (#5116)
- O texto escrito ya no ye ilechible en fer servir qualques aplicacions tals como lo Microsoft Outlook con una linia braille. (#2953)
- En o modo de navegación en l'Internet Explorer y atros controls MSHTML agora s'anuncia o conteniu correcto malas que un elemento amaneix u cambia y s'enfoca inmediatament. (#5040)
- En o modo de navegación en o Microsoft Word a navegación d'una sola letra agora esviella la linia braille y o cursor de revisión  como s'aspera. (#4968)
- En o braille ya no s'amuestran espacios rarizos entre u dimpués d'os indicadors ta controls y formato. (#5043)
- Quan una aplicación ye respondendo lentament y cambias difuera d'ixa aplicación o NVDA responde muito millor en atras aplicacions en a mayoría d'os casos. (#3831)
- Agora s'anuncia as notificacions rustidas d'o Windows 10 como s'aspera. (#5136)
- Agora s'anuncia la valor malas que cambia en bells quadros combinaus (UI Automation) án ixo anteriorment no i marchaba.
- En o modo de navegación en os navegadors web agora o tabular se comporta como s'aspera dimpués de tabular ta un documento de bastida. (#5227)
- A pantalla de bloqueyo d'o Windows 10 agora se puet despachar fendo servir una pantalla tactil. (#5220)
En o Windows 7 y posteriors o texto ya no ye ilechible en escribir en qualques aplicacions tals como lo Wordpad y o Skype con una linia braille.
- En a pantalla de bloqueyo d'o Windows 10 ya no ye posible leyer o portafuellas, accedir t'as aplicacions en marcha con o cursor de revisión, cambiar a configuración d'o NVDA, etc. (#5269)


== Cambeos ta desembolicadors ==
- Agora puetz xaringar a dentrada pura dende un teclau de sistema que no se maneye nativament en o Windows (p.eix. Un teclau QWERTY en una linia braille) fendo servir a nueva función keyboardHandler.injectRawKeyboardInput. (#4576)
- S'ha adhibiu eventHandler.requestEvents ta solicitar eventos particulars que son blocaus por defecto; p.eix. amostrar os eventos dende un control especifico u qualques eventos siempre que se siga en o fundo. (#3831)
- En cuenta d'un solo atributo i18nName, synthDriverHandler.SynthSetting agora tien os atributos  displayNameWithAccelerator y displayName deseparaus ta privar l'anuncio de l'accelerador en l'aniello  d'opcions d'o sintetizador en qualques idiomas.
 - Por compatibilidat con versions anteriors, en o constructor displayName ye opcional y se deribará de displayNameWithAccelerator si no se proporciona. Sin d'embargo si miras de tener un accelerador ta una opción en habría de proporcionar-sen totz dos.
 - L'atributo i18nName ye obsoleto y se podría eliminar en bella versión futura.


= 2015.2 =
O resinyable d'ista  versión inclui a capacidat de leyer graficos en  o Microsoft Excel y l'emparo t'a lectura y t'a navegación interactiva de conteniu matematico.

== Nuevas Caracteristicas ==
- Agora ye posible mover-se-ne enta devant u enta dezaga por as frases en o Microsoft Word y l'Outlook con alt+flecha abaixo y alt+flecha alto respectivament. (#3288)
- Nuevas tablas de transcripción braille ta quantos idiomas Indicos. (#4778)
- En o Microsoft Excel o NVDA agora anuncia quan una celda tien conteniu desbordant u tallau. (#3040)
- En o Microsoft Excel agora puetz fer servir a lista d'elementos (NVDA+f7) ta permitir un listau de graficos, comentarios y formulas. (#1987)
- Suporte ta leyer graficos en o Microsoft Excel. Ta fer servir ixo Selecciona o grafico fendo servir a lista d'elementos (NVDA+f7) y allora fe servir as teclas de flecha ta mover-te-ne entre os puntos de datos. (#1987)
- Fendo servir o MathPlayer 4 de Design Science, o NVDA agora puet leyer y navegar interactivament por conteniu matematico en os navegadors web y en o Microsoft Word y PowerPoint. Mira-te a sección "Leyer conteniu mathematico" en a Guida de l'usuario  ta detalles. (#4673)
- Agora ye posible asignar cenyos de dentrada (comandos de teclau, cenyos tactils, etc.) Ta totz os dialogos de preferencias d'o NVDA y as opcions de formatiau de documentos fendo servir o dialogo de Cenyos de Dentrada. (#4898)


== Cambeos ==
- En o dialogo de formatiau de documentos d'o NVDA os alcorces de teclau t'anunciar as listas, anunciar os vinclos, anunciar os numeros de Línea y anunciar o Nombre d'a fuent s'ha cambiau. (#4650)
- En o dialogo Opcions d'o churi d'o NVDA s'ha adhibiu alcorces de teclau ta reproducir as coordenadas d'audio en que se mueve o churi y o brilo controla o volumen d'as coordenadas d'audio. (#4916)
- S'ha amillorau significativament l'anunciau d'os nombres d'as colors. (#4984)
- Esviellau o transcriptor braille liblouis ta 2.6.2. (#4777)


== Corrección d'errors ==
- As descripcions d'os caracters agora se maneyan correctament t'os conchuntos de caracters en qualques idiomas Indicos. (#4582)
- Si a opción "Confidar en l'idioma d'a voz en procesar caracters y simbolos" ye activada, o dialogo de pronuncia de puntuación y simbolos  agora fa servir correctament l'idioma d'a voz. Tamién l'idioma  que a suya pronuncia se ye editando s'amuestra en o titol d'o dialogo. (#4930)
-En l'Internet Explorer y atros controls MSHTML os caracters tipaus ya no s'anuncian inapropiadament en os quadros combinaus editables tals como o campo de busca de Google en a pachina prencipal d'o Google. (#4976)
- En que se seleccionan colors en as aplicacions d'o Microsoft Office agora s'anuncian os nombres d'as colors. (#3045)
- A salida braille en danés agora marcha de nuevas. (#4986)
- l'avPach y o RePach se pueden fer servir unatra vegada ta cambiar as diapositivas adintro d'una presentación d'o PowerPoint. (#4850)
- En o Skype ta escritorio 7.2 y superior, as notificacions d'escritura agora s'anuncian y s'han apanyau os problemas inmediatament dimpués de mover o foco ta difuera d'una conversa. (#4972)
- S'han apanyau problemas en escribir qualques puntuacións y simbolos tals como gafetz en o campo de tresmín en o dialogo de cenyos de dentrada. (#5060)
- En l'Internet Explorer y atros controls MSHTML, pretar g u mayus+g ta navegar ta graficos agora inclui os elementos marcaus como imachens ta propositos d'accesibilidat (p.eix. ARIA role img). (#5062)


== Cambeos ta desembolicadors ==
- brailleInput.handler.sendChars(mychar) ya no tresminará un caracter si ye igual que o caracter anterior guarenciando-se que a tecla ninviada  s'ha liberau correctament. (#4139)
- Os scripts ta cambiar os modos tactils agora cumplen con as nuevas etiquetas adhibidas ta touchHandler.touchModeLabels. (#4699)
- Os complementos pueden furnir as suyas propias implementacions de presentación matematica. Mira-te o paquet mathPres ta detalles. (#4509)
- S'han implementau comandos de fabla  ta ficar una crebadura entre parolas y ta cambiar o ton, volumen y velocidat. Mira-te BreakCommand, PitchCommand, VolumeCommand y RateCommand en o modulo d'a fabla. (#4674)
 - Bi ha tamién speech.PhonemeCommand ta ficar pronuncias especificas, pero  as implementacions actuals no suportan que un numero muito limitau de fonemas.


= 2015.1 =
O resinyable d'ista versión inclui o modo de navegación t'os documentos en o Microsoft Word y l'Outlook; milloras mayors t'o suporte t'o Skype t'o escritorio; y significants correccions t'o Microsoft Internet Explorer.

== Nuevas Caracteristicas ==
- Agora se pueden adhibir nuevos simbolos en o dialogo de Pronuncia de Simbolos. (#4354)
- En o dialogo de cenyos de dentrada se puet fer servir o nuevo campo "Tresminar-ne por" t'amostrar nomás os cenyos que contengan parolas specificas. (#4458)
- O NVDA agora anuncia automaticament o nuevo texto en o mintty. (#4588)
- En o dialogo de busca d'o modo de navegación agora bi ha una opción ta fer buscas que diferencien as mayusclas y as minusclas. (#4584)
- A  navegación rapida (pretar la h ta mover-se-ne por os capiters etc.) y a Lista d'Elementos (NVDA+f7) agora son disponibles en os documentos d'o Microsoft Word activando lo modo de navegación con NVDA+espacio. (#2975)
- O leyer mensaches HTML en o Microsoft Outlook 2007 y posteriors s'ha amillorau muito en que s'activa automaticament o modo de navegación ta ixos mensaches. Si o modo de navegación no s'habilita en qualques situacions raras puetz aforzar-lo con NVDA+espacio. (#2975) 
- Os capiters de columna de Tabla en o Microsoft word s'anuncian automaticament t'as tablas que o suyo autor haiga specificau explicitament un capitero de ringlera   a traviés d'as propiedatz de tabla d'o Microsoft word. (#4510) 
 - Sin d'embargo, t'as tablas que as ringleras sigan estadas fusionadas ixo no marchará automaticament. En ista situgación encara puetz fixar os capiters de columna manualment en o NVDA con NVDA+mayus+c.
- En o Skype t'o escritorio agora s'anuncian as notificacions. (#4741)
- En o Skype t'o escritorio agora puetz  anunciar y revisar os mensaches recients  fendo servir dende NVDA+control+1 dica NVDA+control+0; p.eix. NVDA+control+1 t'o mensache más recient  y NVDA+control+0 t'o deceno más recient. (#3210)
- En una conversa en o Skype t'o escritorio lo NVDA agora anuncia quan un contacto ye escribindo. (#3506)
- Agora se puet instalar o NVDA silenciosament a traviés d'a linia de comandos sin que ixo ranque a copia instalada dimpués d'a instalación. Ta fer ixo fe servir a opción --install-silent. (#4206)
- Suporte t'as linias braille Papenmeier BRAILLEX Live 20, BRAILLEX Live y BRAILLEX Live Plus. (#4614)


== Cambeos ==
- En o dialogo d'opcions de formatiau de documentos d'o NVDA la opción t'anunciar as errors d'ortografía agora tien un alcorce de teclau (alt+r). (#793)
- O NVDA agora ferá servir l'idioma d'a voz d'o sintetizador en procesar caracters y simbolos (incluindo os nombres d'os simbolos y a puntuación) sin mirar que siga enchegau o cambeo automatico d'idioma. Ta desenchegar ista caracteristica ta que o NVDA torne a fer servir l'idioma d'interficie d'ell desmarca a nueva opción clamada Confidar en l'idioma d'a voz en procesar caracters y simbolos en as opcions d'a voz. (#4210)
- S'ha eliminau o suporte t'o sintetizador Newfon . O Newfon agora ye disponible como un complemento d'o NVDA. (#3184)
- Agora se requier o Skype t'o escritorio 7 u superior ta fer-se servir con o NVDA; as versions anteriors no son suportadas. (#4218)
- Descargar actualizacions d'o NVDA agora ye más seguro. (Specificament a información de l'actualización se recupera a traviés d'o https y l'hash d'o fichero se verifica dimpués de descargau.) (#4716)
- O eSpeak s'ha esviellau t'a versión 1.48.04 (#4325)


== Corrección d'errors ==
- En o Microsoft Excel agora se maneya correctament que as celdas de capitero de ringlera y columna sigan mezcladas. P.eix. si A1 y B1 son mezcladas allora B2 será anunciada con A1 y B1 como lo suyo capitero de columna en cuenta d'absolutament cosa. (#4617)
- En editar o conteniu d'un quadro de texto en o Microsoft PowerPoint 2003 o NVDA anunciará correctament o conteniu de cada linia. Anteriorment en cada paragrafo as linias se'n iban incrementando un. (#4619)
- Totz os dialogos d'o NVDA son agora centraus en a pantalla amillorando a presentación visual y a usabilidat. (#3148)
- En o Skype t'o escritorio, en ficar un mensache introductorio t'adhibir un contacto, agora marcha bien o escribir y mover-se-ne a traviés d'o texto. (#3661)
- En que o foco se'n mueve ta un nuevo elemento en as anvistas d'arbol en l'IDE Eclipse , si l'anterior elemento enfocau ye una caixeta de verificación, ya no s'anuncia incorrectament. (#4586)
- En o dialogo d'o corrector d'ortografía d'o Microsoft Word a error siguient s'anunciará automaticament en que a zaguera s'haiga cambiau u ignorau fendo servir as respectivas teclas d'alcorce. (#1938)
- O texto se puet leyer correctament unatra vegada en as finestras como a finestra d'a terminal d'o Teraterm Pro y os documentos d'o Balabolka. (#4229)
- O foco agora torna correctament t'o documento en edición en que se remate a redacción de dentrada en textos en coreán y atros idiomas de l'este asiatico mientras s'edita adintro d'un marco en l'Internet Explorer y atros documentos MSHTML. (#4045)
- En o dialogo de cenyos de dentrada en trigar una distribución de teclau ta un cenyo de teclau que se ye adhibindo pretar o escape agora zarra o menú como s'aspera en cuenta de zarrar o dialogo. (#3617)
- En eliminar un complemento lo directorio d'ell agora se borra correctament dimpués de reenchegar o NVDA. Anteriorment hebas de reenchegar-lo dos vegadas. (#3461)
- S'ha apanyau Problemas mayors en usar o Skype t'o escritorio 7. (#4218)
- En que ninvias un mensache en o Skype t'o escritorio ya no se leye dos vegadas. (#3616)
- En o Skype t'o escritorio lo NVDA ya no habría de leyer ocasionalment 	 un gran fluxo de mensaches (talment mesmo una conversación entera). (#4644)
- Apanyau un problema que o comando de l'anunciau de calendata y hora d'o NVDA no feba honra a las opcions rechionals especificadas por l'usuario en bells casos. (#2987)
- En o modo de navegación ya no se presenta texto absurdo (bellas vegadas abastando quantas linias) ta ciertos graficos tals como los trobaus en o Google Groups. (Specificament isto ocurre con imachens codificadas en base64.) (#4793)
- O NVDA ya no habría de conchelar-se dimpués d'uns pocos segundos en mover o foco difuera d'una aplicación d'a tienda de Windows que ha plegau a suspender-se. (#4572)
- L'atributo aria-atomic en rechions vivas en o Mozilla Firefox agora se tien en cuenta mesmo anque o mesmo elemento atomic cambee. Anteriorment no afectaba que a elementos descendients. (#4794) 
- O modo de navegación refleixará as actualizacions y as rechions vivas s'anunciarán t'os documentos en o modo de navegación adintro d'as aplicacions ARIA contenidas en un documento en l'Internet Explorer u atros controls MSHTML. (#4798)
- En que o texto cambee u s'adhiba a rechions vivas en l'Internet Explorer y atros controls MSHTML que o suyo autor haiga marcau que o texto ye relevant no s'anunciará que o texto cambiau u adhibiu, en cuenta de tot o texto en l'elemento contenedor. (#4800)
- O conteniu indicau por l'atributo aria-labelledby en elementos en l'Internet Explorer y atros controls MSHTML substitui correctament o conteniu orichinal  do siga apropiau de fer-se. (#4575)
- En comprebar a ortografía en o Microsoft Outlook 2013 a parola con falta d'ortografía agora s'anuncia. (#4848)
- En l'Internet Explorer y atros controls MSHTML  o conteniu adintro d'elementos amagaus con visibility:hidden ya no se presienta inapropiadament en o modo de navegación. (#4839, #3776)
- En l'Internet Explorer y atros controls MSHTML l'atributo title  en controls de formulario  ya no pren preferencia inapropiadament sobre atras asociacions d'etiqueta. (#4491)
- En l'Internet Explorer y atros controls MSHTML o NVDA ya no ignora l'enfocau  d'elementos a causa de l'atributo aria-activedescendant. (#4667)


== Cambeos ta desembolicadors ==
- Esviellau lo wxPython ta 3.0.2.0. (#3763)
- Esviellau lo Python to 2.7.9. (#4715)
- O NVDA ya no se creba en reenchegar-se dimpués de borrar u esviellar un complemento que importa speechDictHandler en o modulo installTasks  d'ell. (#4496)


= 2014.4 =

== Nuevas Caracteristicas ==
- Nuevos idiomas: Espanyol de Colombia , Panyabí.
- Agora ye posible reenchegar o NVDA  u reenchegar-lo con os complementos desenchegaus dende o dialogo de salida d'o NVDA. (#4057)
 - O NVDA tamién puet enchegar-se  con os complementos desenchegaus fendo servir a opción de linia de comandos --disable-addons.
- En os diccionarios d'a fabla agora ye posible especificar que un patrón debe coincidir nomás si en ye una parola completa; p.eix. isto no pasa si en ye parti d'una parola  larga. (#1704)


== Cambeos ==
- Si un obchecto t'o que t'has moviu con a navegación d'obchectos ye adintro d'un documento en o modo de navegación pero l'obchecto an yeras antis no'n yera s'estableix automaticament o modo de revisión a lo documento	.Antis isto nomás pasaba  si o navegador d'obchectos se movía dimpués que cambiase o foco. (#4369) 
- As listas de linias braille y sintetizadors en os respectives dialogos d'opcions son agora ordenaus alfabeticament fueras de Sin braille  y Sin voz que son agora a la fin. (#2724)
- Esviellau o transcriptor braille liblouis ta 2.6.0. (#4434, #3835)
- En o modo de navegación pretar e y mayus+e ta navegar ta campos d'edición agora inclui os quadros combinaus editables. Ixo inclui o quadro de busca en a zaguera versión d'a busca de Google. (#4436)
- En fer clic en l'icono d'o NVDA en l'aria de Notificacions con o botón cucho d'o churi agora s'ubre o menú d'o NVDA en cuenta de no'n fer cosa. (#4459)


== Corrección d'errors ==
- En que o foco torna ta un documento en o modo de navegación (p. eix. pasando con l'alt y o tabulador ta una pachina web ya ubierta) o cursor de revisión se mete apropiadament en o puntero virtual en cuenta d'o control enfocau (p. eix. un amán de vinclo). (#4369)
- En as presentacions de diapositivas d'o Powerpoint o cursor de revisión sigue correctament a lo puntero virtual. (#4370)
- En o Mozilla Firefox y atros navegadors basaus en Gecko lo nuevo conteniu adintro d'una rechión viva s'anunciará mesmo si o nuevo conteniu tien una mena diferent d'ARIA viva usable que a rechión viva pai. P. eix.: Quan o conteniu marcau como assertive s'adhibe a una rechión viva marcada como polite. (#4169)
- En l'Internet Explorer y atros controls MSHTML en bells casos an un documento ye conteniu adintro d'unatro documento ya no se priva a l'usuario d'accedir  ta belún d'o conteniu, especificament os conchuntos de marcos adintro de conchuntos de marcos. (#4418)
- O NVDA ya  no se creba en prebar a  fer servir una linia braille d'Handy Tech en qualques casos. (#3709)
- En o Windows Vista, ya no s'amuestra un dialogo falso "No s'ha trobau punto de dentrada" en qualques casos tals como quan se ranca o NVDA dende l'icono d'o escritorio u atraviés de l'alcorce de teclau. (#4235)
- S'han apanyau problemas serios con os controls de texto editable en dialogos en versions recients de l'Eclipse. (#3872)
- En l'Outlook 2010, mover o cursor agora funciona comos'aspera en o campo d'ubicación de citas y peticions de reunión. (#4126)
- Adintro d'una rechión viva o conteniu que ye marcau como que no ye vivo (p. eix. aria-live="off") agora s'ignora correctament. (#4405)
- En que s'anuncia o texto d'una barra d'estau que tien un nombre, o nombre agora se desepara correctament d'a primera parola d'o texto d'a barra d'estau. (#4430)
- En campos de dentrada de clau con a fabla de parolas escritas activada ya no s'anuncian inutilment muitos asteriscos en que empecipian parolas nuevas. (#4402)
- En a lista de mensaches d'o Microsoft Outlook os elementos ya no s'anuncian desustanciadament como elementos de datos. (#4439)
- En que se selecciona texto en o control d'edición de codigo de l'IDE Eclipse ya no s'anuncia a selección completa cada vegada que a selección cambea. (#2314)
- Qualques versions de l'Eclipse, como a suite de ferramientas de Spring y versión incluida en o conchunto de ferramientas de desembolique de l'Android, agora son reconoixidas como l'Eclipse y maniadas apropiadament. (#4360)
- O seguimiento d'o churi y a exploración tactil en l'Internet Explorer y atros controls MSHTML (incluindo muitas aplicacions d'o Windows 8) agora ye muito mas preciso en pantallas d'alta DPI u quan se cambea l'ampliación d'o documento. (#3494) 
- O seguimiento d'o churi y a exploración tactil en l'Internet Explorer y atros controls MSHTML agora anuncia la etiqueta de mas botons. (#4173)
- Quan s'usa una linia braille Papenmeier BRAILLEX con o BrxCom as teclas en a linia agora marchan como s'aspera. (#4614)


== Cambeos ta desembolicadors ==
T'os executables que ahuespan muitas aplicacions diferents (por eixemplo, javaw.exe), o codigo agora se puet furnir ta cargar os modulos d'aplicacions especificas ta cada aplicación en cuenta de cargar o mesmo modulo d'aplicación ta todas as aplicacions ahuespadas. (# 4360)
 - Gollar a documentación  d'o codigo d'appModuleHandler.AppModule ta detalles.
 - O suporte t'o javaw.exe ye implementau.


= 2014.3 =

== Nuevas Caracteristicas ==
- Os sons reproducius en que o NVDA s'enchega y desenchega se pueden desactivar a traviés d'una nueva opción en o dialogo d'as opcions chenerals. (#834)
- Se puet acceder ta l'aduya d'os complementos dende l'administrador de complementos ta complementos que suporten isto. (#2694)
- Suporte t'o calandario en o Microsoft Outlook 2007 y superiors (#2943) incluindo: Posibilidat de desactivar l'anuncio d'os capiters de columna en a servilla de dentrada y atras listas de mensaches ta l'Outlook 2010 y superiors. (#3834)
 - Anuncio d'a hora actual en mover-se arredol con as teclas de flecha.
 - Indicación si a hora seleccionada ye adintro de bella cita.
 - Anuncio d'a cita seleccionada en pretar o tabulador.
 - Filtrau intelichent d'a calendata de traza que nomás se'n anuncia si a nueva hora u cita seleccionada ye en un diya diferent t'o zaguer.
- Amillorau o suporte t'a servilla de dentrada y atras listas de mensaches en o Microsoft Outlook 2010 y superiors (#3834) incluindo:
 - Posibilidat de silenciar os capiters de columna (de, afer, etc) desactivando a opción anunciar capiters de ringlera y columna  de tabla en as opcions de formatiau de documentos.
  - Posibilidat de fer servir os comandos de navegación de tablas (control + alt +flechas) ta mover-se a traviés d'as columnas individuals
- Microsoft word: Si una imachen en linia no tien establiu garra texto alternativo lo NVDA anunciará en cuenta o titol d'a imachen si l'autor en proporcionó un. (#4193)
- Microsoft Word: O NVDA agora puet anunciar o sangrau d'o paragrafo con o comando d'anuncio de formato (NVDA+f). En puet estar anunciau automaticament quan a nueva opción anunciar a sangría de  paragrafos   ye activada en as opcions d'o formatiau de documentos. (#4165).
- Anunciar o texto insertau automaticament tal como una nueva vinyeta, numero u tabulación de sangría en pretar l'intro en os documentos y campos de texto editables. (#4185)
- Microsoft word: Pretar NVDA+alt+c anunciará  o texto d'un comentario si o cursor en i ye adintro. (#3528)
- Amillorau o suporte t'a lectura automatica d'os capiters de columna y ringlera en o Microsoft Excel (#3568) incluindo:
 - Suporte d'os rangos de nombres definius de l'Excel ta identificar as celdas de capitero (compatible con o lector de pantalla Jaws) .
 - Os comandos d'establir o capitero de columna (NVDA+shift+c) y establir o capitero de ringlera (NVDA+shift+r) agora almagazenan as opcions en a fuella de treballo asinas que en serán disponibles a siguient vegada que s'ubra la fuella, y en serán disponibles t'atros lectors de pantalla que suporten o esquema de rangos de nombres definius.
 - Istos comandos tamién se pueden fer servir agora quantas vegadas por fuella ta establir capiters diferents ta diferents rechions.
 - Suporte t'a lectura automatica d'os capiters de columna y ringlera en o Microsoft Word (#3110) incluindo:
 - Suporte d'os marcapachinas d'o Microsoft Word ta identificar as celdas de capitero(compatible con o lector de pantalla Jaws).
 -  Os comandos d'establir  o capitero de columna (NVDA+shift+c) y establir o capitero de ringlera (NVDA+shift+r) entre que sigan en a primera celda de capitero en una tabla te permite dicir-le a lo NVDA que istos capiters pueden anunciar-se automaticament.  As opcions serán almagazenadas en o documento asinas que en serán disponibles a siguient vegada que o documento s'ubra, y en serán disponibles t'atros lectors de pantalla que suporten o esquema de marcapachinas.
 - Microsoft Word: s'anuncia a distancia dende o canto cucho d'a pachina en pretar a tecla tabulador. (#1353)
 - Microsoft Word: Se proporciona información por fabla y braille t'a mayor parti d'os alcorces de teclau disponibles de formato  (negreta, cursiva, subrayau, aliniacions, libel d'esquema, superindiz, subindiz y mida d'a fuent). (#1353)
 - Microsoft Excel: Si a celda seleccionada contién comentarios agora en podrán estar anunciaus pretando NVDA+alt+c. (#2920)
- Microsoft Excel: Se proporciona un dialogo especifico d'o NVDA pa editar os comentarios en a celda seleccionada actualment en pretar o comando d'Excel mayus+f2 ta dentrar en o modo d'edición de comentarios. (#2920)
- Microsoft Excel: información por fabla y braille  ta muitos mas alcorces de teclau t'os movimientos de selección (#4211) incluindo:
 - Movimiento de pachina Vertical (Re Pach y Av Pach);
 - Movimiento de pachina Horizontal (alt+RePach y alt+AvPach);
 - Enamplar a selección (as teclas anteriors adhibindo o mayus);
 - Selección d'a rechión actual (control+mayus+8).
 - Microsoft Excel: Agora se pueden anunciar as aliniacions vertical y horizontal  t'as celdas con o comando d'anunciau de formato (NVDA+f). En puet estar anunciau automaticament si a opción d'anunciar l'aliniación ye activada en as opcions de formatiau de documentos. (#4212)
 - Microsoft Excel: Agora se puet anunciar o estilo d'una celda con o comando d'anunciau de formato (NVDA+f). En puet estar anunciau automaticament si a opción danunciar o estilo ye activada en as opcions de formatiau de documentos. (#4213)
 - Microsoft PowerPoint: En que  se mueven as formas d'una diapositiva con as teclas de flecha agora s'anuncia a ubicación actual d'a forma (#4214) incluindo:
 - S'anuncia a distancia entre a forma y cadagún d'os cantos d'a diapositiva .
 - Si a forma cubre u ye cubierta por unatra forma, allora la distancia supermesa y a forma cubierta s'anuncian. 
 - T'anunciar ista información en qualsiquier inte sin mover una forma, preta o comando d'anunciar a localización (NVDA+suprimir).
 - En seleccionar una forma, si ye cubierta por unatra forma, o NVDA anunciará que'n ye amagada.
 - O comando d'anunciar a localización (NVDA+suprimir) ye mas especifico a lo contexto en qualques situacions. (#4219)
  - En os campos d'edición estandar y en o modo d'exploración s'anuncia la posición d'o cursor como un porcentache d'o conteniu y as suyas coordenadas de pantalla .
   - En as formas en as presentacions d'o PowerPoint s'anuncia a posición d'a forma relativa a la diapositiva  y atras formas.
   - En pretar   iste comando dos vegadas se producirá l'anterior comportamiento de l'anunciau d'a información de localización ta tot o control.
   - Nuevo idioma: Catalán


== Cambeos ==
- Esviellau o transcriptor braille liblouis ta 2.5.4. (#4103)


== Corrección d'errors ==
- En o Google Chrome y os navegadors basaus en o Chrome qualques bloques  de texto (tals como ixos con enfasi) ya no se repiten en que s'anuncie o texto d'una alvertencia u d'un dialogo. (#4066)
- En o modo de navegación en as aplicacions de Mozilla pretar l'intro sobre un botón, etc. ya no falla en activar-lo (u activa un control erronio) en qualques casos tals como os botons en l'alto d'o Facebook. (#4106)
- Ya no s'anuncia información inutil a lo tabular por o iTunes. (#4128)
- En qualques listas en o iTunes tals como a lista de mosica agora funciona correctament o mover-se  t'o siguient elemento fendo servir a navegación d'obchectos . (#4129)
- Os elementos HTML se consideran capiters  a causa que as marcas WAI ARIA agora son incluidas en a lista d'elementos d'o modo navegación y a navegación rapida d'os documentos de l'Internet Explorer. (#4140)
- A lo seguir vinclos t'a mesma pachina en as versions recients de l'Internet Explorer agora se i mueve correctament y s'anuncia la posición de destín en os documentos en o modo navegación. (#4134)
- Microsoft Outlook 2010 y superiors: S'ha amillorau lacceso cheneral t'os dialogos seguros tals como os nuevos perfils y quadros de dialogo de configuración de correu. (#4090, #4091, #4095)
- Microsoft Outlook: S'ha disminuiu a verbosidat inutil en as barras de ferramientas de comando en navegar a traviés de qualques quadros de dialogo. (#4096, #3407)
- Microsoft word: En tabular por una celda en blanco en una tabla ya no s'anuncia incorrectament salindo d'a tabla. (#4151)
- Microsoft Word: O primer caracter dillá d'a fin d'una tabla (incluindo una nueva linia en blanco), ya no se considera incorrectament que siga adintro d'a tabla. (4152)
- Dialogo d'o corrector ortografico d'o Microsoft Word 2010:  S'anuncia l'actual parola incorrecta en cuenta de anunciar inapropiadament nomás  a primera parola en negreta. (#3431)
- En o modo de navegación en l'Internet Explorer y atros controls MSHTML tabulando u fendo servir a navegación d'una sola letra pa ir t'os campos de formulario atra vegada s'anuncia la etiqueta en muitos casos que no se feba (especificament an se fan servir elementos d'a etiqueta HTML). (#4170)
- Microsoft Word: Anunciar a existencia y  ubicación d'os comentarios ye mas preciso. (#3528)
- S'ha amillorau a navegación de qualques dialogos en os productos d'o MS Office tals como lo Word, l'Excel y l'Outlook deixando d'anunciar particulars barras de ferramientas contenederas de controls que no son utils ta l'usuario. (#4198) 
- Os panels de quefers tals como l'administrador d'o portafuellas u de recuperación de fichers ya no pareixen obtener o foco accidentalment en ubrir una aplicación tal como lo Microsoft Word u l'Excel, o que a vegadas causaba que l'usuario hese de salir y tornar ta l'aplicación ta fer servir o documento u fuella de calculo.  (#4199)
- O NVDA ya no falla en executar-se en os zaguers sistemas operativos Windows, si l'idioma de Windows de l'usuario s'estableix en Serbio (Latino). (#4203) 
- En pretar o Bloqueyo numerico mientras se siga en o modo d'Aduya de Dentrada agora se conmutará o bloqueyo numerico correctament en cuenta de que o teclau y o sistema operativo se desincronicen respective a lo estau d'ista tecla. (#4226)
- En o Google Chrome s'anuncia unatra vegada o titol d'o documento en cambiar de pestanyas. En o NVDA 2014.2 isto no ocurriba en qualques casos. (#4222)
- En o Google Chrome y os navegadors basaus en o Chrome a URL d'o documento ya no s'anuncia en anunciar o documento. (#4223)
- En executar o charrar-lo tot con o sintetizador sin voz seleccionau (util ta pruebas automaticas) agora se charrará tot completo en cuenta de aturar-se dimpués d'unas pocas primeras linias. (#4225)
- Dialogo de sinyatura d'o Microsoft Outlook: O campo editable de sinyatura agora ye accesible permitindo seguimiento completo d'o cursor y detección d'o formato. (#3833) 
- Microsoft Word: En leyer a zaguera linia d'una celda de tabla ya no se leye a celda completa . (#3421)
- Microsoft Word: En leyer a primera u a zaguera linia d'una tabla de contenius ya no se leye a tabla de contenius completa. (#3421) 
- En charrar parolas escritas y en belatros casos, as parolas ya no se deseparan incorrectament en marcas tals como sinyals vocalicas y virama en Idiomas d'a India. (#4254)
- Os campos numericos  de texto editable en o GoldWave agora se manean correctament. (#670)
- Microsoft Word: en mover-se por un paragrafo con control+flecha abaixo / control+flecha alto, ya no ye necesario pretar-los dos vegadas si nos movemos por listas numeradas u de viñetas. (#3290)


== Cambeos ta desembolicadors ==
- O NVDA agora ha unificau o suporte t'a documentación d'os complementos. Vei a sección d'a documentación de complementos d'a guida de l'usuario ta mas detalles. (#2694)
- En furnir vinclos chestuals en un obchecto programable a traviés de __gestures agora ye posible no furnir garra parola  como lo script. Isto desvincula o cenyo en cualsiquier clase base. (#4240)
- Agora ye posible cambiar l'alcorce de teclau que se fa servir ta enchegar o NVDA t'as localizacions que l'alcorce de teclau normal fa problemas. (#2209)
 - Isto se fa a traviés de gettext.
 - Para cuenta que o texto d'a opción Crear acceso dreito d'o escritorio en o quadro de dialogo Instalar o NVDA asinas como a tecla d'acceso dreito en a Guida de l'usuario, tamién s'han d'esviellar.


= 2014.2 =

== Nuevas Caracteristicas ==
- Agora ye posible l'anunciau d'a selección de texto en qualques campos d'edición personalizada an se fa servir información d'a pantalla. (#770)
- En as aplicacions  Java accesibles agora s'anuncia a información de posición t'os botons d'opción y atros controls que exposan información de grupo. (#3754)
- En as aplicacions Java accesibles agora s'anuncian os alcorces de teclau t'os controls que'n tiengan. (#3881)
- En o modo navegación as etiquetas  en os puntos de referencia agora s'anuncian. Tamién s'incluyen en o dialogo Lista d'Elementos. (#1195)
- En o modo navegación as rechions etiquetadas agora se tractan como puntos de referencia. (#3741)
- En os documentos y as aplicacions de l'Internet Explorer, agora se suportan as rechions vivas (parti d'o estandar ARIA d'o W3c), permitindo asinas a los authors d'as webs marcar conteniu particular ta estar charrau automaticament en que cambie. (#1846)


== Cambeos ==
- A lo salir d'un quadro de dialogo u l'aplicación adentro d'un documento d'o modo navegación o nombre y mena de documento d'o modo navegación ya no s'anuncian. (#4069)


== Corrección d'errors ==
- O menú estandar d'o sistema Windows ya no se silencia accidentalment en as aplicacions Java. (#3882)
- En que se copia texto dende a revisión de pantalla os blincos de linia ya no s'ignoran. (#3900)
- Os obchectos d'espacio en blanco sin sentiu ya no s'anuncian en qualques aplicacions en que o foco  cambee u en que se faiga servir a navegación d'obchectos con a revisión simpla enchegada. (#3839)
- Os quadros de mensache y belatros dialogos producius por o NVDA causan atra vegada a cancelación d'a fabla anterior antis d'anunciar o dialogo. 
- En o modo navegación as etiquetas de controls tals como vinclos y botons agora se procesan correctament quan a etiqueta s'haiga substituiu por l'autor con fins d'accesibilidat (especificament, l'emplego d'aria-label u d'aria-labelledby). (#1354)
- En o modo navegación en l'Internet Explorer, Ya no s'ignora inapropiadament o texto conteniu adintro d'un elemento marcau como de presentación (ARIA role="presentation"). (#4031)
- Agora torna a estar posible escribir texto vietnamita fendo servir o software Unikey. Ta fer ixo, desmarca a nueva caixeta de verificación Teclas de maneyo d'atras aplicacions, en o dialogo d'opcions de teclau d'o NVDA. (#4043) 
- En o modo navegación os elementos de menú que son botons d'opción u caixetas de verificación s'anuncian como controls en cuenta de  nomás texto clicable. (#4092)
- O NVDA ya no cambea incorrectament dende o modo foco t'o modo navegación en que se triga un elemento de menú que siga botón d'opción u caixeta de verificación. (#4092)
- En o Microsoft PowerPoint con l'anuncio d'as parolas escritas activau, os caracters eliminaus con a tecla de borrau ya no s'anuncian como una parti d'a parola escrita. (#3231)
- En os dialogos d'opcions d'o Microsoft Office 2010 as etiquetas d'os quadros combinaus s'anuncian correctament. (#4056)
- En o modo navegación en as aplicacions de Mozilla fendo servir a navegación rapida, os comandos ta mover-se t'o siguient u l'anterior botón u campo de formulario agora incluyen botons de conmutación como s'asperaba. (#4098)
- Ya no s'anuncia dos vegadas o conteniu d'as alertas en as aplicacions de Mozilla. (#3481)
- En o modo navegación os contenedors y puntos de referencia ya no son repetius inapropiadament entre que se navega adentro d'ells a lo mesmo tiempo que o conteniu d'a pachina ye cambiando (p. eix. navegando en as pachinas d'o Facebook y o Twitter). (#2199)
- O NVDA se recupera en mas casos en que se cambia difuera d'as aplicacions que han deixau de responder. (#3825)
- O cursor (punto d'inserción) s'esviella correctament unatra vegada en que se fa un comando Charrar-loTot entre que se ye en texto editable dibuixau dreitament en a pantalla. (#4125)


= 2014.1 =

== Nuevas Caracteristicas ==
- Suporte t'o Microsoft PowerPoint 2013. Se note que l'anvista protechida no ye suportada. (#3578)
- En o Microsoft Word y l'Excel o NVDA agora puet leyer o simbolo trigau en que s'esleigan simbolos en o dialogo Ficar simbolo. (#3538)
- Agora ye posible trigar si o conteniu en documentos puet identificar-se como clicable a traviés d'una nueva opción en o dialogo d'opcions de formatiau de documentos. Ista  opción ye enchegada por defecto d'alcuerdo con o comportamiento anterior. (#3556)
- Suporte t'as pantallas braille connectadas a traviés de Bluetooth a un ordinador executando lo software de Widcomm Bluetooth. (#2418)
- Agora s'anuncian os hipervinclos en editar texto en o PowerPoint. (3416)
- Quan se siga en aplicacions ARIA u dialogos en a web, agora ye posible aforzar a lo NVDA ta que cambee t'o modo navegación con NVDA+espacio seguindo a navegación d'estilos de documento de l'aplicación u d'o dialogo. (3#2023)
- En l'Outlook Express / Windows Mail / Windows Live Mail, o NVDA agora anuncia si un mensache tien un adchunto u ye marcau. (#1594)
- En navegar por tablas en aplicacions Java accesibles agora s'anuncian as coordinadas de ringlera y columna, incluindo  os capiters de columna y ringlera si existen. (#3756)


== Cambeos ==
- Ta las pantallas braille Papenmeier, s'ha eliminau a orden mover a revisión plana/foco. Os usuarios pueden asignar as suyas propias teclas usando o dialogo de cenyos de dentrada. (#3652)
- O NVDA agora se basa en a versión 11 d'o Microsoft VC runtime, o que significa que ya no puet executar-se en sistemas operativos anteriors a lo Windows XP Service Pack 2 u lo Windows Server 2003 Service Pack 1.
- O libel de puntuación beluna agora diz os caracters asterisco (*) y mas (+). (#3614)
- Esviellau o eSpeak Ta la versión 1.48.04, que inclui muitas correccions d'idiomas y corriche quantos problemas. (#3842, #3739)


== Corrección d'errors ==
- En que te muevas u selecciones  celdas en o Microsoft Excel, NVDA ya no habría d'anunciar  inadequadament l'antiga celda en cuenta d'a nueva celda quan o Microsoft Excel siga lento en mover a selección. (#3558)
- O NVDA manella adequadament a obridura d'una lista desplegable en una celda en o Microsoft Excel por meyo d'o menú contextual. (#3586)
- Agora s'amuestra apropiadament o Nuevo conteniu d'a pachina en as pachinas d'a botiga en l'iTunes 11 en o modo navegación quan se siga un vinclo en a botiga u en ubrir-la inicialment. (#3625)
- Os botons ta l'anvista previa d'as cantas en a botiga de l'iTunes 11 agora amuestran a suya etiqueta en o modo navegación. (#3638)
- En o modo navegación en o Google Chrome, as etiquetas d'as caixetas de verificación y d'os botons d'opción agora se procesan correctament. (#1562)
- En l'Instantbird, o NVDA ya no anuncia información inutil cada vegada que te muevas ta un contacto d'a lista de contactos. (#2667)
- En o modo navegación en l'Adobe Reader, agora se procesa o texto correcto t'os botons, etc. an a etiqueta s'ha substituiu por l'uso d'un tooltip u unatro recurso. (#3640)
- En o modo navegación en l'Adobe Reader, os graficos extranyos que contienen o texto "mc-ref" ya no se procesan. (#3645)
- O NVDA ya no anuncia todas as celdas en o Microsoft Excel como subrayadas en a información de formato d'ellas. (#3669)
- Ya no s'amuestran caracters desustanciaus  en os documentos en o modo navegación tals como os que se troban en o rango d'uso privau  de l'Unicode. En bells casos istos aturaban l'a lectura d'etiquetas mas utils. (#2963).
- A composición de dentrada t'a introducción de caracters  asiaticos de l'este ya no falla en o PuTTY. (#3432)
- A lo navegar por un documento dimpués d'una cancelación de Verbalizar-lo tot ya no fa que o NVDA anuncie a vegadas incorrectament que s'ha abandonau un campo (tal como una tabla) mas abaixo en o documento en que Verbalizar-lo tot nunca no estió charrando en realidat (#3688)
- Quan se faigan servir ordens rapidas d'o modo navegación mientras se siga en verbalizar-lo tot con a lectura superficial activada, o NVDA anuncia con mas precisión o nuevo campo (por eixemplo, agora diz que un capitero ye un capitero, y no pas nomás o texto). (#3689)
- En o blinco t'a fin u t'o prencipio d'un contenedor as ordens de navegación rapida agora afectan a la opción lectura superficial entre verbalizar-lo tot (ye decir, que ya no cancelarán o verbalizar-lo tot actual). (#3675)
- Os nombres d'os cenyos tactils listaus en o dialogo Cenyos de dentrada d'o NVDA agora son mas amigables y son traducius. (#3624)
- O NVDA ya no fa que bells programas se bloquen quan se mueva o puntero d'o churi sobre os controls d'edición enriquius d'ell (TRichEdit). Programas incluindo Jarte 5.1 y BRfácil. (#3693, #3603, #3581)
- En l'Internet Explorer y atros controls MSHTML, os contenedors tals como tablas marcadas como presentación por ARIA ya no s'anuncian a l'usuario. (#3713)
- En o Microsoft Word, o NVDA ya no repite inapropiadament a información de ringlera y columna de tabla  ta una celda en una linia braille quantas vegadas. (#3702)
- En os idiomas que fan servir un espacio como un separador de grupos de cien en os dichitos como lo francés y l'alemán, os trozos de texto separaus de numers ya no se pronuncian como un solo numero. Isto estié particularment problematico t'as celdas de tablas  que contienen numeros . (#3698)
- O Braille ya no falla a vegadas a lo esviellar-se en que se mueve o cursor d'o sistema en o Microsoft Word 2013. (#3784)
- En posicionar-se en o primer caracter d'un capitero en o Microsoft Word, o texto que se comunica ye un capitero (incluindo o libel) ya no desapareix d'una linia braille. (#3701)
- En que  se dispara un perfil de configuración ta una aplicación y se sale d'ixa aplicación, NVDA ya no falla a vegadas en desactivar o perfil. (#3732)
- En que s'escribe con a dentrada Asiatica en un control adentro d'o propio NVDA (eix.: en o dialogo Mirar en o modo navegación), "NVDA" ya no s'anuncia incorrectament en cuenta d'o candidato. (#3726)
- Agora s'anuncian as pestanyas en o dialogo d'opcions de l'Outlook 2013. (#3826)
- Amillorau o suporte  ta  rechions ARIA live en Firefox y atras aplicacions Gecko de Mozilla:
- Suporte t'actualizacions aria-atomic y tresminaus d'actualizacions  aria-busy (#2640)
- O texto alternativo (como l'atributo alt u l'aria-label) se inclui si no bi ha unatro texto usable. (#3329)
- As actualizacions Live Region ya no se silencian si occurren a lo mesmo tiempo que se mueve lo foco. (#3777)
- Qualques elementos de presentación en o Firefox y atras aplicacions Mozilla Gecko ya no  s'amuestran inapropiadament en o modo navegación (especificament quan l'elemento ye marcau con aria-presentation y en ye  tamién enfocable). (#3781)
- Una millora en o rendimiento en navegar por un documento en o Microsoft Word con as errors d'ortografía enchegadas. (#3785)
- Qualques apanyos pa o suporte d'aplicacions Java accesibles:
 - Ya no falla o control enfocau inicialment en un marco u dialogo  en estar anunciau en que o marco u dialogo pasa t'o primer plan. (#3753)
 - A información de posición inusable ya no se anuncia t'os botons d'opción (p. eix. 1 de 1). (#3754)
 - Millor informe d'os controls JComboBox (l'html ya no s'anuncia, millor informe de os estaus de desplegau y plegau). (#3755)
 - En anunciar o texto d'os dialogos, agora s'inclui bell texto que antis mancaba . (#3757)
 - Agora s'anuncian os cambeos d'o nombre, a valor u a descripción d'o control enfocau de traza mas precisa. (#3770)
 - S'Apanya  un penche en o NVDA visto en o Windows 8 en enfocar bells controls RichEdit que contienen grans cantidatz de texto(por eixemplo en o Visualizador de rechistro d'o NVDA, windbg). (#3867)
- En os sistemas con una configuración de pantalla d'alta DPI (que se produz de traza predeterminada ta muitas pantallas modernas), o NVDA ya no leva o churi t'o puesto entivocau en qualques aplicacions. (#3758, #3703)
- S'ha correchiu un problema ocasional en navegar por a web an o NVDA deixaba de funcionar correctament dica que se reenchegaba, tot y que no se blocaba u se conchelaba. (# 3804)
- Agora Se puet emplegar una pantalla bralle Papenmeier mesmo si nunca s'hese connectau a traviés d'USB. (#3712)
- O NVDA ya no se conchela en que se trigan linias braille d'os modelos antigos de Papenmeier BRAILLEX sin una pantalla connectada.


== Cambeos ta desembolicadors ==
- Os AppModules agora contienen as propiedatz productName y productVersion. Ista información tamién s'incluye agora en a información d'o desembolicador (NVDA+f1). (#1625)
- En a consola Python, agora puetz pretar o tabulador ta completar l'identificador actual. (#433)
 - Si bi ha quantas posibilidatz, puetz pretar o tabulador unatra vegada ta trigar-lo dende una lista.


= 2013.3 =

== Nuevas Caracteristicas ==
- Os campos de formulario  agora s'anuncian en os documentos de Microsoft word. (#2295)
- As listas desplegables en Microsoft Excel 2003 dica lo 2010 agora s'anuncian en que s'ubren y navegan. (#3382)
- Una nueva opción 'Permitir a Lectura superficial en charrar-lo Tot' en o dialogo Opcions de Teclau permite a navegación por un documento con as ordens de navegación rapida d'o modo navegación y movimientos de linia / paragrafo, mientras remaneix leyendo-lo tot. Ista opción ye desactivada de traza predeterminada. (#2766) 
- Agora bi ha un dialogo Cenyos de Dentrada ta permitir a facil personalización d'os cenyos de dentrada(tals como teclas en o teclau) ta ordens de NVDA. (#1532)
- Agora puetz tener diferents opcions ta diferents situacions fendo servir perfils de configuración. Os perfils se pueden enchegar de traza manual u automatica(eix.: ta una aplicación en particular). (#87, #667, #1913)
- En o Microsoft Excel, as celdas que son vinclos agora s'anuncian como vinclos. (#3042)
- En o Microsoft Excel, os comentarios que bi haiga en as celdas agora se l'anuncian a l'usuario. (#2921)


== Corrección d'errors ==
- O Zend Studio agora funciona igual que l'Eclipse. (#3420)
- O cambeo d'estau de bellas caixetas de verificación en o dialogo de reglas de correu de Microsoft Outlook 2010 agora s'anuncia automaticament. (#3063)
- NVDA agora anunciará o estau fixau ta controls fixos tals como  pestanyas en Mozilla Firefox. (#3372)
- NVDA agora puet anunciar a información de revisión en Microsoft Word quan o Control de Cambeos  siga habilitau. para cuenta que Anunciar as revisions d'o editor debe estar habilitau en o dialogo de formatiau de documentos de NVDA (desactivau predeterminadament) tamién ta que sigan anunciaus. (#1670)
- Agora ye posible vincular scripts a cenyos de teclau que contiengan as teclas Alt y/u Windows como modificaderas. Anteriorment, si se feba isto, a execución d'o script causaba l'activación d'o menú Encieto u d'a barra de menú. (#3472)
- A lo seleccionar texto en documentos en modo navegación (por eixemplo a lo emplegar control+shift+fin) ya no causa que se cambee a distribución de teclau en sistemas con quantas distribucions de teclau instaladas. (#3472)
- Internet Explorer ya no habría a penchar-se u tornar-se inusable  quan se zarra NVDA. (#3397)
- O movimiento fisico y atros eventos en qualques ordinadors modernos ya  no se tracta como pulsacions de teclas inadequadas. Anteriorment, isto silenciaba a voz y qualques vegadas feba funcionar ordens de NVDA. (#3468)
- O NVDA agora se comporta como s'asperaba enPoedit 1.5.7. Os usuarios que en faigan servir versions anteriors amenesterán actualizar-ne. (#3485)
- O NVDA agora puet leyer documentos protechius en Microsoft Word 2010,  no causando ya que se'n bloque. (#1686)
- Si se da un parametro de linia de comando desconoixiu en executar o paquet de distribución de NVDA, ya no se provoca un bucle sin fin de dialogos de mensaches d'error. (#3463).
-O NVDA ya no falla en anunciar o texto alternativo d'os graficos y obchectos en Microsoft Word si o texto alternativo contién cometas u atros caracters no estandar. (#3579)
- O numero d'elementos de bellas listas horizontals en modo navegación agora ye correcto. Anteriorment podeba haber estau o dople d'a cantidat real. (#2151)
- A lo pretar control+e en una fuella de calculo de Microsoft Excel, agora s'anunciará a selección esviellada. (#3043)
- NVDA agora puet leyer correctament os documentos XHTML en Microsoft Internet Explorer y belatros controls 	MSHTML. (#3542)
- Dialogo d'Opcions de teclau: si no s'ha seleccionau garra tecla ta fer-la servir como a tecla NVDA, se presienta una error a l'usuario en  que se zarra o dialogo. A lo menos cal seleccionar una d'as teclas ta l'emplego apropiau de NVDA. (#2871)
- En o Microsoft Excel, agora o NVDA anuncia as celdas mezcladas de traza diferent que as celdas multiples seleccionadas. (#3567)
- O cursor de modo navegación  ya no se mete incorrectament quan se deixa un dialogo u una aplicación adentro d'o documento. (#3145)
- S'ha apanyau un problema por o qual o controlador de pantalla HumanWare Brailliant BI / B series braille no s'amostraba como una opción en o quadro de dialogo Configuración de Braille en bells sistemas, anque dita pantalla se connectase a traviés de l'USB.
- O NVDA ya no falla  en que s'esleye a revisión de pantalla quan o navegador d'obchectos  no i tien un puesto real. En iste caso o cursor de revisión agora se  mete en l'alto d'a pantalla. (#3454)


== Cambeos ta Desembolicadors ==
- Puetz especificar a categoría a amostrar a l'usuario por os scripts fendo servir l'atributo scriptCategory en clases ScriptableObject y l'atributo category en metodos de script. Mira la documentación ta baseObject.ScriptableObject ta mas detalles. (#1532)
- O config.save ye obsoleto y talment s'esborre en bella versión esvenidera. Fe servir o config.conf.save en cuenta. (#667)
- O config.validateConfig ye obsoleto y talment s'esborre en bella versión esvenidera. Os complementos que l'amenestan pueden 	furnir a suya propia implementación. (#667, #3632)


= 2013.2 =

== Nuevas Caracteristicas ==
- Suporte t'o Chromium Embedded Framework, que ye un control de navegador web utilizau en quantas aplicacions. (3108)
- Nueva variant de voz d'eSpeak: Iven3.
- En Skype, s'anuncian automaticament os mensaches nuevos de chat mientras a conversación siga enfocada. (2298)
- Suporte ta Tween, incluindo l'anunciau d'os nombres de pestanya y menor ran de detalle quan se leigan os twits.
- Agora puetz deshabilitar l'amostrau de mensaches de NVDA en una linia braille configurando a durada d'o mensache a 0 en o dialogo d'Opcions de Braille. (2482)
- En l'administrador de complementos, agora bi ha un botón Obtener Complementos ta ubrir o puesto web de Complementos de NVDA an puetz examinar y descargar os complementos disponibles. (3209)
- En o dialogo de bienvenida de NVDA que siempre amaneix a primera vegada que  executas NVDA, agora puetz especificar si NVDA s'encieta automaticament dimpués d'autentificar-te en Windows. (2234)
- O modo silencioso s'habilita automaticament quan s'emplegue Dolphin Cicero. (2055)
- Agora se suporta a versión Windows x64 de Miranda IM/Miranda NG. (3296)
- Agora s'anuncian automaticament as sucherencias de busca en  a pantalla d'inicio de  Windows 8.1. (3322)
- Suporte ta navegar y editar fuellas de calculo en Microsoft Excel 2013. (3360)
- As linias braille Freedom Scientific Focus 14 Blue y Focus 80 Blue, asinas como a Focus 40 Blue en bellas configuracions que no se suportaba previament, agora se suporta quan se connecten a traviés de Bluetooth. (3307)
- Agora s'anuncian as sucherencias d'autocompletau en l'Outlook 2010. (2816)
- Nuevas tablas de transcripción braille: Braille computerizau anglés (U.K.), Coreán grau 2, braille ruso ta codigo informatico.
- Nuevo idioma: Farsi. (1427)


== Cambeos ==
- En una pantalla tactil, realizando un eslizamiento con un solo dido a la cucha u a la dreita quan se siga en modo obchecto, agora te mueves enta zaga u enta abant por  totz os obchectos y no solament por aquells que sigan en o mesmo contenedor. Fe servir  un eslizamiento con 2 didos a la cucha u a la dreita ta realizar l'acción orichinal d'anterior/siguient obchecto limitau a l'actual contenedor.
- A caixeta de verificación Anunciar tablas de disenyo que se troba en o dialogo Opcions de Modo Navegación  agora s'ha renombrau como Incluir Tablas de Disenyo ta refleixar que a navegación rapida no las localizará si a caixeta ye desmarcada. (3140)
- Realizando un eslizamiento a la cucha u a la dreita con un solo dido quan se siga en modo obchecto agora se mueve a anterior u siguient en una anvista plana d'a navegación d'obchectos. Fe servir un eslizamiento con 2 didos a la cucha u a la dreita ta levar a cabo a orden orichinal d'obchecto anterior/siguient limitada a lo ran  actual.
- A revisión plana ha estau reemplazada por os modos de revisión d'obchectos, documentos y pantalla. (2996)
 - A revisión d'obchectos revisa o texto nomás adentro d'o navegador d'obchectos, a revisión de documentos revisa tot o texto en un documento en modo navegación (si bi'n ha belún) y a revisión de pantalla revisa o texto en a pantalla ta l'aplicación actual.
- As ordens que antis moveban a u dende revisión plana agora cambean entre istos nuevos modos de revisión.
 - O navegador d'obchectos sigue automaticament a lo cursor de revisión de tal traza que sigue estando l'obchecto mas profundo en a posición d'o cursor de revisión quan se ye en modos de revisión de documentos u de pantalla.
- Dimpués de cambiar t'o modo revisión de pantalla, NVDA remanirá en iste modo dica que tornes explicitament t'os modos de revisión de documentos u d'obchectos.
 - Quan se siga en o modo de revisión de documentos u d'obchectos, NVDA podrá cambiar automaticament entre istos dos modos dependendo de si yes movendo-te por un documento d'o modo navegación u no pas.
- Esviellau lo transcriptor braille liblouis a 2.5.3. (3371)


== Corrección d'errors ==
- L'activación d'un obchecto agora anuncia l'acción antis de l'activación, en cuenta de l'acción dimpués de l'activación (eix.: desplegar quan se desplega en cuenta de plegar). (2982)
- Una lectura y seguimiento d'o cursor mas precisos en diversos campos de dentrada t'as zagueras versions de Skype, tals como chat y campos de busca. (1601, 3036)
- En a lista de conversacions recients de Skype, o numero de nuevos eventos agora se leye en cada conversación, si cal. (1446)
- Milloras en o control d'o cursor y l'orden de lectura de texto de dreita a cucha en a pantalla. Eix.: Edición de texto en arabe en Microsoft Excel. (1601) 
- A navegación rapida en botons y campos de formulario agora localizará os vinclos marcaus como botons ta propositos d'accesibilidat en Internet Explorer. (2750)
- En o modo navegación, o conteniu en l'interior d'anvistas en arbol ya no se procesa como una representación plana, no ye util. Puetz pretar Intro sobre una anvista en arbol ta  interactuar con ella en  o modo foco. (3023)
- A lo Pretar alt+flecha abaixo u alt+flecha alto ta desplegar un quadro combinau mientras se siga en modo foco ya no cambea incorrectament t'o modo navegación. (2340)
- En Internet Explorer 10, as celdas d'a tabla ya no activan o modo foco, de no estar que l'autor d'a web las haiga feitas enfocables explicitament.  (3248)
- NVDA ya no falla en rancar si a hora d'o sistema ye anterior a la zaguera revisión d'una actualización. (3260)
- Si una barra de progreso s'amuestra en una linia Braille, o Braille s'esviella quan cambee a barra de progreso. (3258)
- En o modo navegación en aplicacions de Mozilla, os titols d'as tablas ya no se procesan dos vegadas. Amás, l'indiz se procesa quan bi ha tamién un titol. (3196)
- A lo cambiar l'idioma de dentrada de Windows 8, NVDA agora charra en l'idioma correcto en cuenta d'en l'anterior.
- NVDA agora anuncia os cambeos en o modo de conversión de IME en Windows 8.
- NVDA ya no anuncia a vasuera en o escritorio quan os metodos de dentrada chaponeses Google u IME ATOK son en uso. ;(# 3234)
- En Windows 7 y superiors, NVDA ya no anuncia indebidament a reconoixencia de voz u a dentrada tactil como un cambeo d'idioma d'o teclau.
 - NVDA ya no anuncia un caracter especial (0x7f) en pretar control+retroceso en qualques editors mientras Charrar os Caracters en Escribir siga enchegau. (3315)
- espeak ya no fa cambeos inadequaus en o ton, volumen, etc. quan NVDA leiga texto que contienga bells caracters de control u XML. (3334) (regresión de 437)
- En as aplicacions Java, os cambeos en o ran u en a valor d'o control enfocau agora s'anuncian automaticament, y se refleixan con a subsiguient salida d'o control. (3119)
- En os controls Scintilla, as linias agora s'anuncian correctament quan o tallo de parolas ye habilitau. (885)
- En as aplicacions de Mozilla, o nombre d'os elementos de lista de nomás lectura agora s'anuncia correctament; eix.: quan se navega por twits en modo foco en twitter.com. (3327)
- En os dialogos de Confirmación en Microsoft Office 2013 agora se leye o suyo conteniu automaticament quan amaneixcan. 
- Milloras en o rendimiento quan se navega por bellas tablas en Microsoft Word. (3326)
- As ordens de navegación de tablas de NVDA (control+alt+flechas) funcionan millor en qualques tablas de Microsoft Word quan una celda abarca quantas ringleras.
- Si l'administrador de complemenhtos ye ya ubierto, activar-lo de nuevo (u dende o menú Ferramientas u ubrindo un fichero de complemento) ya no falla u no imposibilita zarrar dito administrador de complementos. (3351)
- NVDA ya no se pencha en bells dialogos quan se siga utilizando o IME en Office 2010 con o chaponés u lo chino. (3064)
- Os espacios multiples ya no se comprimen a un solo espacio en as linias braille. (1366)
- As Zend Eclipse PHP Developer Tools agora funcionan igual que l'Eclipse. (3353)
- En Internet Explorer, ya no cal pretar de nuevas o tab ta interactuar con un obchecto integrau (tal como o conteniu Flash) dimpués de pretar intro sobre ell. (3364)
- A l'editar texto en Microsoft PowerPoint, a zaguera linia ya no se presienta como a linia anterior si a zaguera linia ye en blanco. (3403)
- En Microsoft PowerPoint, os obchectos ya no se  verbalizan a vegadas  dos vegadas quan los seleccionas u trigas ta editar. (3394)
- NVDA ya no causa que l'Adobe Reader se bloque u se penche ta bells documentos PDF mal formaus que contiengan ringleras difuera d'as tablas. (3399)
- NVDA agora detecta correctament a siguient diapositiva con o foco quan s'elimine una en  la  vista de miniaturas en Microsoft PowerPoint. (3415)


== Cambeos ta Desembolicadors ==
- S'ha adhibiu windowUtils.findDescendantWindow ta buscar una finestra descendent (HWND) localizando a visivilidad especificada, identificador d'o control y/u nombre de clase.
- A consola de python remota ya no aspera dimpués de 10 segundos mientras aguarda por a dentrada. (3126)
- A inclusión d'o modulo bisect en compilacions binarias ye en desuso y podrá eliminar-se en una versión futura. (3368)
 - Os complementos que dependan de bisect (incluindo o modulo urllib2) habrían d'actualizar-se ta incluir iste modulo.


= 2013.1.1 =
Ista versión apanya lo problema que feba crebar NVDA  en rancar quan yera configurau ta fer servir l'idioma irlandés.

== Corrección d'errors ==
- Se producen caracters correctos en escribir en a interficie d'usuario propia de NVDA entre que s'usa un metodo de dentrada coreano u chaponés, mientras siga o metodo por defecto. (# 2909)
- En Internet Explorer y atros controls MSHTML, os campos marcaus como que contienen una dentrada no valida agora se manean correctament. (# 3256)
- NVDA ya no se creba en rancar quan s'ha configurau l'idioma irlandés.


= 2013.1 =
Os aspectos mas destacaus d'ista versión incluyen un disenyo de teclau portatil mas intuitivo y consistent, suporte basico ta Microsoft PowerPoint, l'emparo a las descripcions largas en os navegadors web, y l'emparo t'a dentrada de braille d'ordinador ta linias braille que tienen un teclau braille.

== Important ==

=== Nueva Distribución de Teclau Portatil ===
A distribución de teclau portatil s'ha redisenyau por completo ta fer-la mas intuitiva y consistent.
A nueva distribución emplega as teclas de cursor en combinación con a tecla NVDA y atras modificaderas ta ordens de revisión.

Por favor tien en cuenta os siguients  cambeos ta ordens comunament emplegadas:
|| Nombre | Tecla |
| Leyer-lo tot | NVDA+a |
| Leyer a linia actual | NVDA+l |
| Leyer a selección de texto actual | NVDA+shift+s |
| Anunciar a barra d'estau | NVDA+shift+fin |
Amás, entre atros cambeos, han variau as ordens ta toda a navegación d'obchectos, revisión de texto, clic d'o churi y grupos d'opcions d'o sintetizador.
Por favor uella-te o documento [Referencia Rapida d'Ordens keyCommands.html] t'as nuevas teclas.


== Nuevas Caracteristicas ==
- Suporte basico ta editar y leyer presentacions de Microsoft PowerPoint. (#501)
- Suporte basico ta leyer y escribir mensaches en Lotus Notes 8.5. (#543)
- Suporte t'o cambeo automatico d'idioma quan se leyen documentos en Microsoft Word. (# 2047)
- En modo Navegación ta MSHTML (eix.: Internet Explorer) y Gecko (eix.: Firefox), agora s'anuncia a existencia de descripcions largas. Tamién ye posible ubrir a descripción larga en una finestra nueva pretando NVDA+d. (#809)
- As notificacions en Internet Explorer 9 y superior agora se charran (tals como conteniu bloqueyau u descargas de fichers). (#2343)
- L'anunciau automatico d'os capiters de ringlera y columna agora se suporta ta documentos en modo navegación en Internet Explorer y atros controls MSHTML. (#778)
- Nuevo idioma: Aragonés, irlandés
- Nuevas tablas de transcripción braille:  Danés grau 2, Coreán grau 1.
- Suporte ta linias braille connectadas a traviés de bluetooth en un ordinador executando o Bluetooth Stack for Windows de Toshiba. (#2419)
- Suporte t'a selección de puerto quan s'emplegan linias Freedom Scientific (automatico, USB u Bluetooth).
- Suporte t'a familia BrailleNote de anotadors de HumanWare en actuar como un terminal de Braille ta un lector de pantalla. (# 2012)
- Suporte ta  modelos antigos d'as linias braille Papenmeier BRAILLEX. (#2679)
- Suporte t'a dentrada de braille computerizau ta linias braille que tiengan un teclau braille. (#808)
- Nuevas opcions de teclau que permiten a esleción de si NVDA habría d'interrumpir o discurso de caracters escritos y/u la tecla Intro. (# 698)
 - Suporte ta quantos navegadors basaus ​​en Google Chrome: Rockmelt, BlackHawk, Comodo Dragon y SRWare Iron. (# 2236, # 2813, # 2814, # 2815)


== Cambeos ==
- Esviellau o transcriptor braille liblouis a 2.5.2. (#2737)
- A distribución de teclau portatil s'ha redisenyau por completo ta fer-la mas intuitiva y consistent. (#804)
- Esviellau o sintetizador de voz eSpeak t'a versión 1.47.11. (#2680, #3124, #3132, #3141, #3143, #3172)

== Corrección de Fallos ==
				- As teclas de navegación rapida ta blincar a o siguient u anterior separador en modo Navegación agora funcionan en Internet Explorer y atros controls MSHTML. (#2781)
- Si NVDA se reenchega sin eSpeak u no bi ha voz a causa d'a falta d'un sintetizador de voz configurau quan NVDA ranca, a opción configurada ya no s'estableix automaticament en o sintetizador de reserva. Isto significa que agora, se prebará de nuevo o sintetizador orichinal a proxima vegada que s'enciete NVDA. (# 2589)2589)
- Si NVDA se configura sin braille porque falla a linia Braille configurada quan NVDA ranca, a linea configurada ya no se configura automaticament sin braille. Isto significa que agora, a visualización orichinal s'intentará de nuevo a proxima vegada que s'enciete NVDA. (# 2264)
- En modo navegación en aplicacions de Mozilla, as actualizacions d'as tablas agora se procesan correctament. Por eixemplo, en actualización de celdas, as coordenadas de ringlera y columna s'anuncian y a navegación d'a tabla funciona como habría de. (#2784)
- En modo navegación en navegadors web, bells graficos cliqueables no etiquetados que no se procesaban anteriorment agora se procesan correctament. (#2838)
- As versions anteriors y actuals (tals como a 6.1.1) agora se suportan. (#2800)
- Ta metodos de dentrada tals como Easy Dots IME baixo XP, a cadena de lectura agora s'anuncia correctament.
- A lista de candidatos d'o metodo de dentrada Chino Simplificau Microsoft Pinyin baixo Windows 7 agora se leye correctament quan se cambean pachinas con as flechas cucha y dreita, y quan le la ubre en primeras con Inicio.
- Quan s'alza a información de pronuncia personalizada de simbolos , o campo abanzau "preserve" ya no s'elimina. (#2852)
- Quan se desactiva a detección automatica d'actualizacions, NVDA ya no ha d'estar reiniciau ta que totz os cambeos tiengan efecto.
- NVDA ya no falla en encetar-se si un complemento no se puet eliminar a causa que o suyo directorio se siga utilizando actualment por unatra aplicación. (#2860)
- As etiquetas de pestanyas en o dialogo de preferencias de DropBox agora pueden veyer-se con a Revisión Plana. 
- Si l'idioma de dentrada se cambea a belatro que o predeterminau, NVDA agora detecta as teclas correctament ta ordens y o modo d'aduya de dentrada.
- Ta idiomas tals como l'alemán an o signo + (mas) ye una  tecla sola en o teclau, agora ye posible vincular-le ordens utilizando a parola "plus". (#2898)
- En Internet Explorer y atros controls  MSHTML, as cometas agora s'anuncian do proceda. (#2888)
- O controlador d'as linias HumanWare Brailliant BI/Bbraille agora puet  seleccionar-se quan as linias sigan connectadas a traviés de Bluetooth pero nunca no s'haigan connectau a traviés d'USB.
- O tresminau d'elementos en a Lista d'Elementos d'o modo navegación con o tresmín de texto en mayusclas agora torna resultaus no sensibles a las mayusclas igual que en minusclas en cuenta de brenca en absoluto. (#2951)
- En navegadors de Mozilla, o modo navegación puet utilizar-se de nuevo quan s'enfoque conteniu Flash. (#2546)
- Quan s'utilice una tabla de braille contraito y sía habilitada a opción expandir a braille computerizau t'a parola en o cursor , o cursor braille agora se coloca correctament quan se trobe dimpués d'una  parola an un caracter se  represiente con quantas celdas braille (eix.: signo de mayusclas, signo de dialogo, signo de numero, etc.). (#2947)
- A selección de texto agora s'amuestra correctament en una linia braille en aplicacions tals como controls d'edición de Microsoft word 2003 y Internet Explorer.
- Ye posible de nuevo seleccionar texto en una adreza enta zaga en Microsoft Word mientras siga habilitau o Braille.
- Quan se siga en revisión,  eliminando caracters con retroceso u suprimir en controls d'edición de Scintilla, NVDA anuncia correctament os caracters multibyte. (#2855)
- NVDA ya no fallará en instalar quan a rota d'o perfil d'usuario contienga bells caracters multibyte. (#2729)
- L'anunciau de grupos ta controls Vista de Lista (SysListview32) en aplicacions de 64 bit ya no causa una error.
- En modo navegación en aplicacions de Mozilla, o conteniu de texto ya no se tracta incorrectament como editable en qualques casos extranyos. (#2959)
- En IBM Lotus Symphony y OpenOffice, movendo lo cursor agora se mueve o cursor de revisión si cal
- O conteniu d'Adobe Flash ye agora accesible en Internet Explorer ta Windows 8. (# 2454)	
- Suporte fixo ta Bluetooth Papenmeier Trio Braillex. (# 2995)
- Apanyada la imposibilidat d'emplegar qualques voces de Microsoft Speech API versión 5 como as voces d'a fabla Koba 2(# 2629)
- En as aplicacions que emplegan o Java Access Bridge, as linias braille agora se esviellan correctament quan o cursor se mueve en os campos de texto editables. (# 3107)
- Suporte t'os marcadors d'os formularios en os documentos en modo navegación  que suportan marcadors (# 2997)
- O controlador d'o sintetizador eSpeak agora s'encarga d'a lectura de caracter mas apropiada (por eixemplo, una letra anunciando lo nombre extranchero u d'a suya valor y no solament o suyo son u lo nombre chenerico). (# 3106)
- NVDA ya no falla en copiar a configuración de l'usuario ta usar l'inicio de sesión y atras pantallas seguras quan a rota d'o perfil de l'usuario contién caracters que no son ASCII. (# 3092)	
- NVDA ya no se conchela en emplegar a dentrada de caracters asiaticos en qualques aplicacions .NET. (# 3005)


== Cambeos ta Desembolicadors ==
- Os controladors de linia Braille agora pueden suportar a selección manual de puertos. (#426)
 - Isto ye mayoritariament util ta linias braille que suporten connexión a traviés d'un puerto serie.
 - Isto se fa utilizando o metodo d'a clase getPossiblePorts en a clase BrailleDisplayDriver.
- Agora se suporta a dentrada braille  dende teclaus braille. (#808)
 - A dentrada braille s'abarca por a clase brailleInput.BrailleInputGesture u una subclase d'a mesma.
 - As subclases de braille.BrailleDisplayGesture (seguntes s'implementaron en os controladors d'as linias braille) tamién pueden heredar de brailleInput.BrailleInputGesture. Isto permite amostrar ordens  y que a dentrada braille se manelle por a mesma clase gesture.
- Agora se puet usar comHelper.getActiveObject ta obtener un obchecto COM activo d'un proceso normal quan NVDA s'executa con o privilechio UIAccess. (# 2483)


= 2012.3 =
Lo subrayable d'ista versión incluye o suporte t'a dentrada de caracters asiaticos; suporte experimental ta pantallas tactils en Windows 8; anunciau de numeros de pachina y suporte amillorau ta tablas en Adobe Reader; ordens de navegación de tabla en ringleras de tabla enfocadas y controls de vista en lista de Windows; suporte ta qualques linias braille mas; y capiters de columna en Microsoft Excel.

== Nuevas Caracteristicas ==
- NVDA agora puet suportar dentrada de caracters asiaticos utilizando IME y metodos de servicio de dentrada de texto en todas as aplicacions, incluindo:
 - anunciau y navegación de listas candidatas;
 - Anunciau y navegación de cadenas de composición; y 
 - Anunciau de lectura de cadenas.
- A presencia de subrayaus y rayaus agora s'anuncia en documentos d'Adobe Reader. (#2410)
- Quan a función Windows Sticky Keys ye activada, a tecla modificadera de NVDA agora se comportará como as atras teclas modificaderas. Isto te permite utilizar a tecla modificadera de NVDA sin a necesidat de mantener pretada mientras pretas atras teclas. (#230)
- Agora se suporta l'anunciau automatico de capiters de columna y de ringlera en Microsoft Excel. Preta NVDA+shift+c ta configurar a ringlera que contienga capiters de columna y NVDA+shift+r t'a columna que contienga capiters de ringlera. Preta o script dos vegadas en succesión rapida ta limpiar a opción. (#1519)
- Suporte t'as linias braille HIMS Braille Sense, Braille EDGE y SyncBraille. (#1266, #1267)
- Quan as Notificacions de Windows 8 amaneixcan, NVDA las anunciará si l'anunciau de globos d'aduya ye habilitau. (#2143)
- Suporte experimental ta pantallas Tactils en Windows 8, incluindo:
 - Lectura de texto dreitament baixo o tuyo dido mientras lo mueves
 - Muitos cenyos ta levar a cabo a navegación por obchectos, revisión de texto, y atras ordens de NVDA.
- Suporte ta VIP Mud. (#1728)
- En Adobe Reader, si una tabla tien un resumen, agora se presienta. (#2465)
- En Adobe Reader, os capiters de ringlera y columna de tabla agora pueden anunciar-se. (#2193 #2527 #2528)
- Nuevos idiomas: Amárico, Coreán, Nepalí, Esloveno.
- NVDA agora puet leyer sucherencias d'autocompletau quan s'introduzcan adrezas de correu en Microsoft Outlook 2007. (#689)
- Nuevas variants de voz d'eSpeak: Gene, Gene2. (#2512)
- En Adobe Reader, agora pueden anunciar-se os numeros de pachina. (#2534)
- En Reader XI, as etiquetas de pachina s'anuncian do sigan presents, reflexando cambeos en a numeración de pachinas en seccions diferents, etc. en versions anteriors, isto no ye posible y solament os numeros de pachinas seqüencials s'anunciaban.
- Agora ye posible reiniciar a configuración de NVDA a las valors predeterminadas de fabrica pretando NVDA+control+r tres vegadas rapidament u trigando Reiniciar a las Valors Predeterminadas de Fabrica dende o menú NVDA (#2086).
- Suporte t'as linias braille Seika Versión 3, 4 y 5 y Seika80 de Nippon Telesoft. (#2452)
- O primer y o zaguer d'os sensors superiors d'as linias braille Freedom Scientific Pacmate y Focus agora pueden utilizar-se ta desplazar enta zaga u abance. (#2556).
- Se suportan muitas mas caracteristicas en as linias braille Freedom Scientific Focus tals como barras abanzadas, barras de garnelas y bellas combinacions de puntos t'accions comunas. (#2516)
- En aplicacions que utilicen IAccessible2 tals como aplicacions de Mozilla, os capiters de ringlera y columna de tabla agora pueden anunciar-se estase d'o modo Navegación. (#926)
- Suporte preliminar t'o control de documento en Microsoft Word 2013. (#2543)
- L'aliniación de texto agora puet anunciar-se en aplicacions que utilizan IAccessible2 tals como aplicacions de Mozilla. (#2612)
- Quan s'enfoca una ringlera de tabla u un control estandar vista en lista de Windows con multiples columnas, agora puetz utilizar as ordens de navegación por tablas t'accedir a las celdas individuals. (#828)
- Nuevas tablas de transcripción braille: Estonio grau 0, braille computerizau Portugués de 8 puntos y braille italián computerizau de 6 puntos. (#2319, #2662)
- Si NVDA s'instala en o sistema, a obridura directa d'un paquet de complemento de NVDA (ye decir dende l'explorador de Windows u dimpués de descargar-lo d'un navegador web) lo instalará en NVDA. (#2306)
- Suporte t'os modelos mas modernos d'as linias de Papenmeier BRAILLEX. (#1265)
- A información de posición (eix.: 1 de 4) agora s'anuncia t'os elementos de lista de Windows Explorer en Windows 7 y posterior. Isto tamién incluye qualsiquier control UIAutomation que suporte as propiedatz personalizables itemIndex y itemCount. (#2643)


== Cambeos ==
- En o dialogo Preferencias d'o Cursor de Revisión de NVDA, a opción Siguir foco d'o teclau ha estau renombrada a Siguir a o foco d'o sistema ta consistencia con a terminolochía utilizada en atras partes en NVDA.
- Quan o braille siga siguindo a la revisión y o cursor siga sobre un obchecto que no siga un obchecto de texto (eix.: un campo de texto editable), as teclas d'os sensores d'o cursor agora activarán l'obchecto. (#2386)
- A opción Alzar a Configuración en Salir agora ye activada de traza predeterminada ta nuevas configuracions.
- Quan s'actualiza una copia de NVDA instalada anteriorment, a tecla d'alcorce d'o escritorio ya no se forza a control+alt+n si estió cambiada manualment a belatra diferent por l'usuario. (#2572)
- A lista de complementos en l'Administrador de Complementos agora amuestra o nombre d'o paquet antis d'o suyo estau. (#2548)
- A lo instalar a mesma u unatra versión d'un complemento instalau actualment, NVDA te preguntará si deseyas actualizar o complemento antigo primer, en cuenta d'amostrar una error y abortar a instalación. (#2501)
- As ordens de navegación d'obchectos (fueras d'a orden anunciar obchecto actual) agora anuncian con menos verbosidad. Encara puetz obtener a información extra utilizando a orden d'anunciar obchecto actual. (#2560)
- Actualizau o transcriptor braille liblouis a 2.5.1.
- O documento Referencia Rapida d'Ordens de teclau de NVDA ha estau renombrau a Referencia Rapida d'Ordens, asinas agora incluye tanto ordens tactils como ordens de teclau.
- A Lista d'elementos en Modo Navegación agora recordará o zaguer tipo d'elemento amostrau (eix.: vinclos, capiters u zonas) cada vegada que s'amuestre o dialogo dentro d'a mesma sesión de NVDA. (#365)
- A mayoría d'as aplicacions Metro en Windows 8 (eix.: Mail, Calendar) ya no activan o Modo Navegación ta toda l'aplicación.
- Actualizau l'Handy Tech BrailleDriver COM-Server a 1.4.2.0.


== Corrección de Fallos ==
- En Windows Vista y posterior, NVDA ya no tracta incorrectament a tecla Windows como ye en mantener-la pretada quan se desbloqueya Windows dimpués de bloqueyar-la pretando Windows+l. (#1856)
- En Adobe Reader, os capiters de ringlera agora se reconoixen correctament como celdas de tabla; ye decir, as coordenadas s'anuncian y se pueden accedir utilizando ordens de navegación de tabla. (#2444)
- En Adobe Reader, as celdas de tabla que abarquen mas d'una columna y/u ringlera agora se manellan correctament. (#2437)
- O paquet de distribución de NVDA agora verifica a suya integridat antis d'executar-se. (#2475)
- Os fichers descargaus temporalment agora s'eliminan si se descarga un fichero d'actualización de NVDA. (#2477)
- NVDA ya no se penchará quan se siga executando como un administrador mientras se copia a configuración de l'usuario a la configuración d'o sistema (ta utilizar-la en l'autentificación de Windows y en atras pantallas seguras). (#2485)
- Os mosaicos en a Pantalla d'inicio de Windows 8 agora se presientan millor en voz y braille. O nombre ya no se repite, ya no s'anuncia no seleccionau en totz os mosaicos, y a información d'estau en directo se presienta seguntes a descripción d'o mosaico (eix.: temperatura actual t'o mosaico d'o Tiempo).
- As claus ya no s'anuncian quan se leigan campos de clau en Microsoft Outlook y atros controls d'edición estandar que sigan marcaus como protechius. (#2021)
- En Adobe Reader, os cambeos ta campos de formulario agora se reflexan correctament en modo navegación. (#2529)
- Milloras en o suporte t'o corrector d'ortografía de Microsoft Word, incluindo a lectura mas precisa d'a error ortografica actual, y a capacidat de suportar o corrector d'ortografía quan s'execute una copia instalada de NVDA en Windows Vista u superior.
- Os complementos que incluigan fichers contenendo caracters que no sigan en anglés agora pueden instalar-se correctament en a mayoría d'os casos. (#2505)
- En Adobe Reader, l'idioma d'o texto ya no se pierde quan s'actualiza u se desplaza. (#2544)
- Quan s'instala un complemento, o dialogo de confirmación agora amuestra correctament o nombre traduciu d'o complemento si ye disponible. (#2422)
- En aplicacions que utilizan UI Automation (tals como aplicacions de .net y Silverlight), o calculo de valors numericas ta controls tals como eslizadors s'ha correchiu. (#2417)
- A configuración ta l'anunciau de barras de progreso agora se reconoixe ta barras de progreso indeterminadas amostradas por NVDA quan se ye instalando, creyando una copia portable, etc. (#2574)
- As ordens de NVDA ya no pueden executar-se dende una linia braille entre que una pantalla segura de Windows (tal como a pantalla de desbloqueyo) siga activa. (#2449)
- En modo navegación, o braille agora s'actualiza si o texto que ye estando desplazau cambea. (#2074)
- Quan se ye en pantallas seguras de  Windows tals como a pantalla de desbloqueo, os mensaches d'as aplicacions que son charrando u amostrando braille dreitament a traviés de NVDA agora s'ignoran.
- En modo navegación, ya no ye posible sobreixer a parti inferior d'o documento con a tecla flecha dreita quan se ye en o caracter final, u blincando a fin d'un contenedor quan ixe contenedor ye o zaguer elemento d'o documento. (#2463)
- Ya no s'incluye incorrectament conteniu extranyo quan s'anuncia o texto de dialogos en aplicacions web (especificament, dialogos ARIA sin l'atributo aria-describedby). (#2390)
- NVDA ya no localiza u anuncia incorrectament bells campos d'edición en documentos MSHTML (eix.: Internet Explorer), especificament an s'haiga utilizau un paper ARIA explicito por l'autor d'a pachina web. (#2435)
- A tecla retroceso agora se manea correctament quan se verbalizan parolas en escribir en consolas d'ordens de Windows. (#2586)
- As coordenadas d'as celdas agora s'amuestran de nuevo en Braille en Microsoft Excel.
- En Microsoft Word, NVDA ya no te deixa enganchau en un paragrafo con formato de lista quan tractas de navegar por una vinyeta u numero con flecha cucha u control + flecha cucha. (#2402)
- En modo navegación en aplicacions de Mozilla, os elementos en bells quadros de lista (especificament, quadros de lista d'ARIA) ya no se procesan incorrectament.
- En modo navegación en aplicacions de Mozilla, bells controls que estioron procesaus con una etiqueta incorrecta u como espacio en blanco agora se procesan con a etiqueta correcta.
- En modo navegación en aplicacions de Mozilla, s'han eliminau espacios en blanco extranyos.
- En modo navegación en navegadors web, bells graficos que se marcoron explicitament como presentables (especificament, con un atributo alt="") agora s'ignoran correctament.
- En navegadors web, NVDA agora amaga conteniu que se marcó como amagau ta lectors de pantalla (especificament, utilizando l'atributo aria-hidden). (#2117)
- As cantidatz negativas en moneda (eix.: -$123) agora se charran correctament como negativos, independientment d'o libel de simbolos. (#2625)
- Entre leyer tot, NVDA ya no tornará incorrectament a a l'idioma predeterminau si una linia no finaliza una frase. (#2630)
- Agora se detecta correctament a información de fuent en Adobe Reader 10.1 y posteriors. (#2175)
- En Adobe Reader, si se proporciona texto alternativo, solament se procesará ixe texto. Anteriorment, qualques vegadas s'incluiba texto extranyo. (#2174)
- Do un documento contienga una aplicación, o conteniu de l'aplicación ya no s'incluye en modo navegación. Isto apreviene de movimientos inasperaus dentro de l'aplicación quan se navega. Puetz interactuar con l'aplicación d'o mesmo modo que t'os obchectos integraus. (#990)
- En aplicacions de Mozilla, a valor d'os botons de flecha agora s'anuncia correctament quan cambean. (#2653)
- Actualizau o suporte d'Adobe Dichital Editions ta que funcione en a versión 2.0. (#2688)
- En pretar NVDA+flecha alto mientras se siga en un quadro combinau en Internet Explorer y atros documentos MSHTML ya no se leyerán incorrectament totz os elementos. Por lo contrario, solament se leyerá l'elemento activo. (#2337)
- Os diccionarios d'a fabla agora s'alzarán apropiadament quan s'emplegue un signo de numero (#) dentro d'os campos d'edición patrón u reemplazar. (#961)
- O modo navegación ta documentos MSHTML (eix.: Internet Explorer) agora amuestra correctament o conteniu visible que bi ha dentro d'o conteniu amagau. Especificament: elementos con un estilo visibility:visible en un elemento con estilo visibility:hidden. (#2097)
- Os vinclos en o Centro de Seguranza de Windows XP ya no anuncian vasuera aleatoriament dimpués d'os suyos nombres. (#1331)
- Os controls de texto UI Automation eix.:  o campo de busca en o menú d'inicio de Windows 7 agora s'anuncian correctament quan se mueva o churi sobre ells en cuenta de remanir en silencio.
- Os cambeos de distribución d'o teclau ya no s'anuncian entre leyer tot, o qual yera especialment problematico ta documentos multilingües incluindo texto arabe. (#1676)
- Tot o conteniu de qualques controls de texto editable UI Automation (eix.: o quadro de busca en o menú d'inicio de Windows 7/8) ya no s'anuncia cada vegada que cambee.
- Quan te muevas entre grupos en a pantalla d'inicio de Windows 8, os grupos no etiquetados ya no anunciarán o suyo primer mosaico como o nombre d'o grupo. (#2658)
- A lo ubrir a pantalla d'inicio de Windows 8, o foco se coloca correctament sobre o primer mosaico en cuenta de blincar a la radiz d'a pantalla d'inicio, o qual puet confundir en a navegación. (#2720)
- NVDA ya no fallará en rancar quan a rota de perfils de l'usuario contienga bells caracters multibyte. (#2729)
- En modo navegación en Google Chrome, o texto d'as pestanyas agora se procesa correctament.
- En modo navegación, os botons de menú agora s'anuncian correctament.
- En Calc d'OpenOffice.org/LibreOffice, a lectura d'as celdas d'as fuellas de calculo agora funciona correctament. (#2765)
- NVDA puet funcionar de nuevo en a lista de mensaches de Yahoo! Mail quan s'utiliza dende Internet Explorer. (#2780)


== Cambeos ta Desembolicadors ==
- L'anterior fichero log agora se copia en nvda-old.log en a inicialización de NVDA. Por tanto, si NVDA se bloca u se reinicia, o rechistro d'información  d'ixa sesión encara ye accesible t'a suya inspección. (#916)
- A obtención d'a propiedat de paper en chooseNVDAObjectOverlayClasses ya no causa que o paper siga incorrecto y por tanto no s'anuncie en foco ta bells obchectos tals como consolas d'ordens de Windows y controls de Scintilla. (#2569)
- Os menús de NVDA Preferencias, Ferramientas y Aduya agora son accesibles como atributos en gui.mainFrame.sysTrayIcon clamando-se preferencesMenu, toolsMenu y helpMenu, respectivament. Isto permite a os plugins adhibir elementos muito mas facilment a istos menús.
- O script navigatorObject_doDefaultAction en globalCommands ha estau renombrau a review_activate.
- Agora se suportan os mensaches contextuals de Gettext. Isto permite que sigan definidas multiples traduccions ta un solament mensache en Inglés dependendo d'o contexto. (#1524)
 - Isto se fa utilizando a función pgettext(context, message).
 - Isto se suporta tanto ta NVDA mesmo como t'os complementos.
 - Han d'utilizar-se xgettext y msgfmt de GNU gettext ta creyar qualsiquier fichero PO y MO. As ferramientas de Python no suportan mensaches contextuals.
 - Ta xgettext, pasa l'argumento de linia d'ordens --keyword=pgettext:1c,2 ta habilitar a inclusión de mensaches contextuals.
 - Mira https://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts ta mas información.
- Agora ye posible accedir a os modulos compilaus de NVDA an haigan estau sobrescritos por modulos de tercers. Mira o modulo nvdaBuiltin ta detalles.
- Agora puet utilizar-se o suporte de traducción de complementos dentro d'o modulo installTasks d'o complemento. (#2715)


= 2012.2.1 =
Ista versión aborda quantos problemas de seguranza potencials (por meyo de l'actualización de Python a 2.7.3).

  
= 2012.2 =
Lo resenyable d'ista versión incluye una caracteristica que integra l'instalador y a creyación d'o portable, un auto actualizador, administración facil d'os nuevos complementos de NVDA, anunciau de graficos en Microsoft Word, suporte t'o estilo d'aplicacions de Windows 8 Metro, y quantas correccions de fallos importants. 

== Nuevas Caracteristicas ==
- NVDA agora puet buscar automaticament, descargar y instalar actualizacions. (#73)
- S'ha feito mas sencilla a extensión d'a funcionalidat de NVDA con l'adición d'un Administrador de Complementos (que se troba baixo Ferramientas en o menú NVDA) permitindo-te instalar y desinstalar paquetz de complementos de NVDA (fichers .nvda-addon) que contiengan plugins y controladors. Tiene en cuenta que l'Administrador de Complementos no habría d'amostrar os antigos plugins personals y controladors copiaus manualment en o tuyo directorio de configuración. (#213)
- Agora funcionan Muitas mas caracteristicas comunas de NVDA en o estilo d'aplicacions de Windows 8 Metro quan s'utiliza una versión instalada de NVDA, incluindo a verbalización de caracters en escribir y modo navegación ta documentos web (s'incluye suporte t'a versión metro d'Internet Explorer 10). Las copias portables de NVDA no pueden accedir a o estilo d'aplicacions metro. (#1801) 
- En documentos en modo Navegación (Internet Explorer, Firefox etc.) agora puetz blincar a o comienzo, u pasar a la fin, de bells elementos contenedors (incluindo listas y tablas) con shift+, y , respectivament. (#123) 
- Nuevo idioma: Griego.
- Agora s'anuncian os graficos y textos alternativos en documentos de Microsoft Word. (#2282, #1541)


== Cambeos ==
- L'anunciau de coordenadas de celda en Microsoft Excel agora se fa dimpués d'o conteniu en cuenta d'antis, y agora solament s'incluye si as opcions d'anunciau de tablas y d'anunciau de coordenadas d'a celda d'a tabla son activadas en as opcions d'o dialogo Formato de Documento. (#320)
- NVDA agora se distribuye en un paquet. En cuenta d'una versión portable y una instalable, agora solament bi ha un fichero que quan s'execute, encetará una copia temporal de NVDA, y te permitirá instalar, u chenerar una distribución portable. (#1715)
- NVDA agora siempre s'instala en Program Files en totz os sistemas. A lo actualizar una instalación tamién le la moverá automaticament si anteriorment no s'instaló astí.


== Corrección de Fallos ==
- Con o Cambeo automatico d'idioma activau, o Conteniu tal como o texto alternativo ta graficos y etiquetas ta bells atros controls en Mozilla Gecko (eix.: Firefox) agora s'anuncian en l'idioma correcto si se marcó apropiadament.
- Leyer tot en BibleSeeker (y atros controls TRxRichEdit) ya no se detiene en o meyo d'un pasaje.
- As listas que se troban en as propiedatz de fichero en Windows 8 Explorer (pestanya permisos) y en Windows 8 Windows Update agora se leyen correctament.
- Correchius posibles penches en MS Word que podrían ocurrir quan le prenió mas de dos segundos extrayer texto  dende un documento (linias extremadament largas u tablas de conteniu). (#2191)
- A detección de partición de parolas agora funciona correctament an un espacio en blanco siga seguiu por bella puntuación. (#1656)
- En modo navegación en Adobe Reader, agora ye posible navegar por capiters difuera d'un ran utilizando navegación rapida y a Lista d'Elementos. (#2181)
- En Winamp, o braille agora s'actualiza correctament quan te mueves a un elemento diferent en l'Editor de listas de reproducción. (#1912)
- L'arbol en os Elementos de Lista (disponible ta documentos en modo navegación) agora se dimensiona apropiadament t'amostrar o texto de cada elemento. (#2276)
- En aplicacions que utilicen Java Access Bridge, os campos de texto editable agora se presientan correctament en braille. (#2284)
- En aplicacions que utilicen Java Access Bridge, os campos de texto editable ya no informan de caracters extranyos en bellas circumstancias. (#1892)
- En aplicacions que utilicen Java Access Bridge, quan se siga a la fin d'un campo de texto editable, a linia actual  agora s'anuncia correctament. (#1892)
- En modo navegación en aplicacions que utilicen Mozilla Gecko 14 y posterior (eix.: Firefox 14), agora a navegación rapida funciona en bloques de citas y obchectos integraus. (#2287)
- En Internet Explorer 9 NVDA ya no leye conteniu indeseyau quan o foco se mueve dentro de bellas zonas u elementos enfocables (especificament un elemento div que ye enfocable u que tien un paper de zona ARIA). 
- Os iconos t'os alcorces ta NVDA en o Escritorio y en o Menú d'Inicio agora s'amuestran correctament en edicions de 64 bit de Windows. (#354)


== Cambeos ta Desembolicadors ==
- A causa d'a substitución de l'instalador anterior NSIS ta NVDA por un compilau en Python, ya no ye necesario t'os traductors mantener un fichero langstrings.txt ta l'instalador. Todas as cadenas de localización agora s'administran con fichers po de gettext.


= 2012.1 =
Lo subrayable d'ista versión incluye caracteristicas ta una lectura mas fluída en braille; indicación de formato de documento en braille; acceso a muita mas información de formato y millora d'o rendimiento en Microsoft Word; y suporte t'a Store d'iTunes.

== Nuevas Caracteristicas ==
- NVDA puet anunciar o numero d'os tabuladors u espacios a l'inicio en a linia actual en l'orden en que s'introducioron. Isto puet activar-se seleccionando anunciar sangrau de linia en o dialogo Formateado de documento. (#373)
- NVDA agora puet detectar a pulsación de teclas cheneradas dende a emulación de dentrada de teclau tal como en programas de teclau en pantalla u de reconoixencia de voz.
- NVDA agora puet detectar colors en finestras ordens de consola.
- As negretas, cursivas y subrayaus agora s'indican en braille utilizando signos apropiaus a la tabla de transcripción configurada. (#538)
- Agora s'anuncia  muita mas información en documentos de Microsoft Word, incluindo: 
 - Información en linia tal como numeros de capiters y notas a o piet, rans de capitero, a existencia de comentarios, rans d'anidamiento de tabla, vinclos, y color de texto;
 - S'anuncia quan se dentra a las seccions d'o documento tals como a l'historico de comentarios, a l'historico de notas a o piet y notas finals, y a os historicos de capiters y pietz.
- O braille agora indica texto seleccionau utilizando os puntos 7 y 8. (#889)
- O braille agora anuncia información sobre controls dentro de documentos tals como vinclos, botons y capiters. (#202)
- Suporte ta linias braille hedo ProfiLine USB y MobilLine. (#1863, #1897)
- NVDA agora priva a deseparación de parolas en braille quan siga posible de forma predeterminada.  Isto puet desactivar-se en o dialogo Opcions de Braille. (#1890, #1946)
- Agora ye posible amostrar braille por paragrafos en cuenta de linias, o qual podría permitir mas fluidez en leyer grans cantidatz de texto. Isto ye configurable utilizando a opción Leyer por paragrafos en o dialogo d'Opcions de Braille. (#1891)
- En modo navegación, puetz activar l'obchecto baixo o cursor utilizando una linia braille. Isto se fa pretando a tecla de guiau de cursor an se localice o cursor (o qual significa pretar-lo dos vegadas si o cursor no ye encara allí). (#1893)
- Suporte basico t'arias web en iTunes tal como en a Store. Atras aplicacions que utilicen WebKit 1 tamién podrían suportar-se. (#734)
- En libros en Adobe Dichital Editions 1.8.1 y posteriors, agora as pachinas se pasan automaticament quan s'utiliza leyer tot.  (#1978)
- Nuevas tablas de transcripción braille: Portugués grau 2, braille islandés computerizau de 8 puntos, tamil grau 1, Braille espanyol computerizau de 8 puntos, persa grau 1. (#2014)
- Agora puetz configurar si s'anuncian os marcos en documentos dende o dialogo de preferencias de Formato de Documentos. (#1900)
- O modo durmiente s'activa automaticament quan s'utiliza OpenBook. (#1209)
- En Poedit, os traductors agora pueden leyer os comentarios adhibius y extraitos automaticament t'o traductor. Os mensaches que sigan sin traducir u provisionals se marcan con un asterisco y s'escuita un pitido quan se navegue sobre ells (#1811).
- Suporte t'as linias braille d'HumanWare Brailliant series BI y B. (#1990)
- Nuevo idioma: Noruego Bokmål.


== Cambeos ==
- As ordens ta describir o caracter actual u ta letreyar a parola u linia actual agora letreyarán en l'idioma apropiau d'alcuerdo con o texto, si o cambeo automatico d'idioma ye activau y a información d'idioma adequada ye disponible.
- Actualizau o sintetizador de voz eSpeak a 1.46.02.
- Agora NVDA tresminará os nombres extremadament largos (30 caracters u mas) deducius d'URLs de gráfícos y vinclos dau que lo mas prebable ye que sigan vasuera que obstaculice a lectura. 
- S'ha abreviau bella información amostrada en braille. (#1955, #2043)
- Quan os cursors de sistema u de revisión se mueven, agora o braille se desplaza d'igual modo como si se desplazase manualment. Isto lo fa mas apropiau quan o braille se configuró ta leyer por paragrafos y/u ta privar partición de parolas. (#1996)
- Actualizau a una nueva tabla de transcripción braille Espanyola de grau 1. 
- Actualizau o transcriptor braille liblouis a 2.4.1.


== Corrección de Fallos ==
- En Windows 8, o foco ya no se mueve incorrectament d'o campo de Busca de Windows Explorer, o qual no permitiba a NVDA interactuar con ell.
- Milloras en o rendimiento quan se leye y se navega por documentos de Microsoft word mientras l'anunciau automatico d'o formato ye activau, asinas agora ye un poquet mas confortable prebar a leyer o formato etc. O rendimiento tamién podría amillorar-se sobre tot ta qualques usuarios.
- O modo navegación agora s'utiliza ta tot o conteniu de pantalla d'Adobe Flash.
- Correchida a mala calidat d'audio en qualques casos quan s'utilizan voces de Microsoft Speech API version 5 con o dispositivo de salida d'audio configurau a belatro que o predeterminau (Microsoft Sound Mapper). (#749)
- Se permite de nuevo a NVDA utilizar o sintetizador "no speech", confiando solament en o braille u en elVisualizador de Voz. (#1963)
- As ordens de navegación d'obchectos ya no anuncian "Sin fillos" y "Sin pais", pero en cambeo anuncian mensaches consistents con a documentación.
- Quan NVDA se configuró ta utilizar unatro idioma que l'Anglés, o nombre d'a tecla tab agora s'anuncia en l'idioma adequau. 
- En Mozilla Gecko (eix.: Firefox), NVDA ya no cambea intermitentment a modo navegación mientras se navega por menús en documentos. (#2025)
- En a Calculadera, a tecla retroceso agora anuncia o resultau actualizau en cuenta de no anunciar cosa. (#2030)
- En modo navegación, a orden mover o rato a o navegador d'obchectos actual agora se mueve a o centro de l'obchecto en o cursor de revisión en cuenta d'a2 a cantonada cucha superior, fendo-lo mas preciso en qualques casos. (#2029)
- En modo navegación con o modo foco automatico ta cambeos d'o foco activau, l'enfocau d'una barra de ferramientas agora cambiará a modo foco. (#1339)
- A orden anunciar titol funciona correctament de nuevo en Adobe Reader.
- Con o modo foco automatico ta cambeos d'o foco activau, o modo foco agora s'utiliza correctament t'as celdas de tabla enfocadas; eix.: en regillas ARIA. (#1763
- En iTunes, a información de posición en bellas listas agora s'anuncia correctament.
- En Adobe Reader, qualques vinclos ya no se tractan como contenendo campos de texto editable de solament lectura.
- As etiquetas de qualques campos de texto editable ya no s'incluyen incorrectament quan s'anuncia o texto d'un dialogo. (#1960)
- A descripción de grupos s'anuncia una vegada de nuevo si l'anunciau de descripcions d'obchecto ye activau.
- As grandarias leyibles agora s'incluyen en o texto d'o dialogo de propiedatz d'a unidat en Windows Explorer.
- L'anunciau dople de texto en pachinas de propiedatz ha estau suprimiu en qualques casos. (#218)
- Amillorau o seguimiento d'o cursor d'o sistema en campos de texto editable que confían en texto escrito en a pantalla. En particular, isto amillora a edición en l'editor de celdas de Microsoft Excel y l'editor de mensaches d'Eudora. (#1658)
- En Firefox 11, a orden mover a conteniu de modo virtual (NVDA+control+espacio) agora funciona como habría de ta2 salir d'obchectos integraus tals como conteniu Flash.
- NVDA agora se reinicia correctament (eix.: dimpués de cambiar l'idioma configurau) quan se localice en un directorio con contenius de caracters no ASCII. (#2079)
- O Braille respecta correctament as opcions ta l'anunciau de teclas d'alcorce d'os obchectos, información de posición y descripcions.
- En aplicacions Mozilla, o cambeo entre modos navegación y foco ya no s'enlentece con o braille activau. (#2095)
- Guiar o cursor a o espacio en o final d'a linia/paragrafo utilizando os sensores d'o cursor braille en qualques campos de texto editable agora funciona correctament en cuenta de levar a o comienzo d'o texto. (#2096)
- NVDA funciona de nuevo correctament con o sintetizador Audiologic Tts3. (#2109)
- Os documentos de Microsoft Word se tractan correctament como multi-linia. Isto causa que o braille se comporte de traza mas adequada quan un documento s'enfoque.
- En Microsoft Internet Explorer, ya no ocurren errors quan s'enfoca sobre bells controls raros. (#2121)
- Cambiar a puntuación y simbolos por l'usuario agora tendrá efecto immediato, en cuenta de requerir un reinicio de NVDA, u que se desactive o cambeo automatico d'idioma.
- Quan s'utiliza eSpeak, a voz ya no queda en silencio en qualques casos en o dialogo Alzar Como... d'o Visualizador de Log de NVDA. (#2145)


== Cambeos ta desembolicadors ==
- Agora bi ha una Consola Python remota ta situacions an a depuración remota ye util. Mira a Developer Guide ta detalles.
- A rota base d'o codigo de NVDA agora se sacó d'os tracebacks en o log t'amillorar legibilidad. (#1880)
- Os obchectos TextInfo agora tienen un metodo activate() t'activar a posición representada por o TextInfo.
 - Isto s'utiliza por o braille t'activar a posición utilizando teclas de guiau d'o cursor en una linia braille. Manimenos, podría haber atras gritadas en o futuro.
- Os treeInterceptors y os NVDAObjects que solament exposan una pachina de texto a la vegada pueden suportar o cambeo automatico de pachina entre leyer tot utilizando o textInfos.DocumentWithPageTurns mezclau. (#1978)
- S'han moviu u cambiau os nombres de quantos controls y constants de salida. (#228)
- As constants speech.REASON_* s'han moviu a controlTypes.
- S'han renombrau controlTypes, speechRoleLabels y speechStateLabels solament a roleLabels y stateLabels, respectivament.
- Agora a salida braille se rechistra en o ran input/output. En primeras, o texto sin transcribir de todas as rechions se rechistra, seguiu por as celdas braille d'a finestra que son estando amostradas. (#2102)
- As subclasses d'o synthDriver sapi5  agora pueden sobrescribir-se _getVoiceTokens y extender __init__ ta suportar fichas de voces personalizadas tals como con sapi.spObjectTokenCategory ta obtener fichas d'un rechistro personalizau.


= 2011.3 =
Lo subrayable en ista versión incluye o cambeo automatico d'idioma d'a voz quan se leyen documentos con a información d'idioma apropiada;  suporte t'ambients Java Runtime de 64 bit; anunciau de formato de texto en Modo navegación en aplicacions de Mozilla; millor maneo de rupturas y penches d'aplicacions; y correccions inicials ta Windows 8.


== Nuevas Caracteristicas ==
- NVDA agora puet cambiar l'idioma d'o sintetizador eSpeak a o vuelo quan leye bells documentos web/pdf con a información d'idioma apropiada. O cambeo automatico d'idioma/dialecto puet activar-se u desactivar-se dende o dialogo Opcions de Voz. (#845) 
- En Mozilla Gecko (eix.: Firefox) os rans de capitero agora s'anuncian quan s'utiliza a navegación d'obchectos.
- O formato de texto agora se puet anunciar quan s'utiliza o modo navegación en Mozilla Gecko (eix.: Firefox y Thunderbird). (#394)
- O texto con subrayau y/u rayau agora puet detectar-se y anunciar-se en controls de texto estandar IAccessible2 tal como en aplicacions de Mozilla.
- NVDA agora se reiniciará si se pencha.
- En modo Navegación en Adobe Reader, agora s'informa d'a cuenta d'as ringleras y as columnas.
- S'adhibió suporte t'a Plataforma de Sintesi de Voz de Microsoft. (#1735)
- Os numeros de linia y de pachina agora s'anuncian t'o cursor en IBM Lotus Symphony. (#1632)
- O porcentaje de quánto cambea o ton quan se verbalice una letra mayuscla agora ye configurable dende o dialogo Opcions de voz. Por tanto, isto reemplaza l'antiga caixeta de verificación elevar o ton ta mayusclas (por tanto ta desactivar ista caracteristica mete o porcentaje a 0). (#255)
- A color de texto y fondo agora s'incluyen en l'anunciau de formato ta celdas en Microsoft Excel. (#1655)
- En aplicacions que utilizen o Java Access Bridge, a orden activar actual navegador d'obchectos agora funciona en controls an siga apropiau. (#1744)
- Suporte basico ta Design Science MathPlayer.


== Cambeos ==
- NVDA agora se reiniciará si se pencha.
- Bella información amostrada en braille ha estau abreviada. (#1288)
- O script Leyer Finestra activa (NVDA+b) ha estau amillorau ta tresminar controls inutils y agora tamién ye muito mas facil de silenciar. (#1499)
- Leyer Tot automaticament quan se carga un documento en Modo Navegación agora ye opcional a traviés d'una opción en o dialogo Opcions de Modo Navegación. (#414)  
- Quan se tractan de leyer barras d'estau (Sobremesa NVDA+fin), si no se puet localizar un obchecto de barra d'estau real, NVDA recurrirá en o suyo puesto a utilizar a linia final de texto escrita en a pantalla de l'aplicación activa. (#649)
- Quan se leye con leyer tot en documentos en modo navegación, NVDA agora ferá una pausa en o final de capiters y atros elementos de ran de bloque, en cuenta de verbalizar o texto de conchunta con o siguient bloque como si ise una frase larga.
- En modo navegación, presionando intro u espacio en una pestanya agora l'activa en cuenta de cambiar a modo foco. (#1760)
- Actualizau o sintetizador de voz eSpeak a 1.45.46.


== Corrección de Fallos ==
- NVDA ya no amuestra vinyetas u numeración ta listas en Internet Explorer y atros controls MSHTML quan l'autor ha indicau que istas no deberíam amostrar-se (ye decir, o estilo de lista ye "none"). (#1671)
- Reiniciar NVDA quan s'ha penchau (eix.: presionando control+alt+n) ya no sale de la copia previa sin prencipiar unatra nueva.
- Pretar retroceso u flechas en una consola d'ordens de Windows ya no causa resultaus extranyos en qualques casos. (#1612)
- L'elemento seleccionau en quadros combinaus WPF (y posiblement belatros quadros combinaus amostraus utilizando UI Automation) que no permiten edición de texto agora s'anuncia correctament.
- En modo Navegación en Adobe Reader, agora siempre ye posible mover-te a la siguient ringlera dende a ringlera de capitero y viceversa utilizando as ordens mover-se a la siguient ringlera y mover-se a la ringlera anterior. Tamién,  a ringlera de capitero ya no s'anuncia como ringlera 0. (#1731)
- En modo navegación en Adobe Reader, agora ye posible mover a (y por tanto pasar) celdas vuedas en una tabla.
- Información de posición sin sentiu  (eix.: 0 de 0 ran 0) ya no s'anuncia en braille.
- Quan o braille siga a la revisión, agora podrá amostrar-se conteniu en revisión planan. (#1711)
- Un texto d'o control de texto ya no se presienta dos vegadas en una linia braille en qualques casos, eix.: desplazando-se dezaga dende o comienzo de documentos de Wordpad.
- En modo navegación en Internet Explorer, pretando intro sobre un botón de puyar un fichero agora se presienta correctament o dialogo ta trigar un fichero ta puyar en cuenta de cambiar a modo foco.  (#1720)
- Os cambeos de conteniu dinamico tals como en consolas d'o Dos ya no s'anuncian si  o modo durmiente ta ixa aplicación ye actualment activau. (#1662)
- En modo navegación, o comportamiento d'alt+flecha alto y alt+flecha abaixo ta contrayer y expandir quadros combinaus ha estau amillorau. (#1630)
- NVDA agora se recupera de muitas mas situacions tals como aplicacions que deixan de responder en as qualas anteriorment causaba un penche completo. (#1408)
- Ta documentos en modo navegación de Mozilla Gecko (Firefox etc.) NVDA ya no fallará en interpretar texto en una situación muit especifica an un elemento is styled as display:table. (#1373)
- NVDA ya no anunciará controles etiqueta quan o foco se mueva por ells. Detiene l'anunciau dople d'etiquetas ta qualques campos de formulario en Firefox (Gecko) y Internet Explorer (MSHTML). (#1650)
- NVDA ya no falla en leyer una celda en Microsoft Excel dimpués d'apegar con control+v. (#1781)
- En Adobe Reader, ya no s'anuncia información extranya sobre o documento quan se mueva a un control en una pachina diferent en modo foco. (#1659)
- En modo navegación en aplicacions de Mozilla Gecko (eix.: Firefox), os botons de comnutación agora se detectan y anuncian correctament. (#1757)
- NVDA agora puet leyer correctament a barra d'adrezas de l'Explorador de Windows en Windows 8 developer preview.
- NVDA ya no pencha aplicacions tals como winver y wordpad en Windows 8 developer preview a causa de malas traduccions de glyph.
- En modo navegación en aplicacions que utilizan Mozilla Gecko 10 y posteriors (eix.: Firefox 10), o cursor se coloca correctament mas amenudo quan se carga una pachina con un ancora. (#360)
- En Modo navegación en aplicacions Mozilla Gecko (eix.: Firefox), as etiquetas ta mapas d'imachen agora s'interpretan.
- Con o seguimiento d'o rato activau, en mover o rato sobre bells campos de texto editable (tal como en Synaptics Pointing Device Settings y SpeechLab SpeakText) ya no causa que l'aplicación se penche. (#672)
- NVDA agora funciona correctament en quantos dialogos Sobre... en aplicacions distribuídas con Windows XP, incluindo o dialogo de sobre... en Notepad y o dialogo de sobre  en Windows. (#1853, #1855)
- Correchida a revisión por parolas en controls d'edición de Windows. (#1877)
- Mover-se difuera d'un campo de texto editable con flecha cucha, flecha alto u avpág mientras se ye en modo foco agora cambea correctament a modo navegación quan ye habilitau o modo foco automatico ta movimientos d'o cursor. (#1733)


== Ccambios ta Desembolicadors ==
- NVDA agora puet instruir a os sintetizadores de voz ta cambiar os idiomas ta seccions en particular de voz.
 - Ta suportar isto, os controladors han de maniar speech.LangChangeCommand en seqüencias pasadas a SynthDriver.speak().
 - Os obchectos SynthDriver tamién habrían de proporcionar l'argumento d'idioma a obchectos VoiceInfo (u sobrescribir l'atributo d'idioma ta capturar l'idioma actual). d'unatro modo, l'idioma d'a interface d'usuario de NVDA será utilizau.

 
= 2011.2 =
Lo subrayable en ista revisión incluye milloras mayors concernients a la puntuación y simbolos, incluindo rans configurables, etiquetado y descripcions de caracters personalizaus; sin pausas a la fin d'as linias entre a lectura completa; suporte amillorau ta ARIA en Internet Explorer; y muito millor suporte ta documentos PDF XFA/LiveCycle en Adobe Reader; acceso a texto escrito en a pantalla en mas aplicacions; y acceso a formato y información de color ta texto escrito en a pantalla.

== Nuevas Caracteristicas ==
- Agora ye posible escuitar a descripción ta qualsiquier caracter dau presionando o script revisar caracter actual dos vegadas en succesión rapida.  Ta caracters en Inglés isto ye l'alfabeto fonetico anglés estandar. Ta idiomas pictográficos tals como o Chino Mandarín, se proporcionan una u mas frases d'eixemplo utilizando o simbolo dau. Tamién presionando revisar parola actual u revisar linia actual tres vegadas letreyará a parola/linia utilizando a primera d'istas descripcions. En espanyol s'utiliza l'alfabeto de letreyo radioaficionau licherament modificau(#55)
- Puede veyer-se mas texto en revisión plana t'aplicacions tals como Mozilla Thunderbird que escriben o suyo texto dreitament a la pantalla como glyphs.
- Agora ye posible trigar quantos rans d'anunciau de puntuación y simbolos. (#332)
- Quan a puntuación u atros simbolos se repiten mas d'una vegada, agora s'anuncia o numero de repeticions  en cuenta de verbalizar os simbolos repetidament. (#43)
- Una nueva tabla de transcripción braille: braille computerizau noruego de 8 puntos. (#1456)
- A voz ya no fa pausas antinaturals a la fin de cada linia quan s'utiliza a orden ta leyer tot. (#149)
- NVDA agora anunciará si bella cosa s'ordena (d'alcuerdo con a propiedat aria-sort) en navegadors Web. (#1500)
- Os patrones Braille unicode agora s'amuestran correctament en as linias braille. (#1505)
- En Internet Explorer y atros controls MSHTML quan o foco se mueve dentro d'un grupo de controls (surrounded by a fieldset), NVDA agora anunciará o nombre d'o grupo (the legend). (#535)
- En Internet Explorer y atros controls MSHTML, as propiedatz aria-labelledBy y aria-describedBy are now honoured.
- En Internet Explorer y atros controls MSHTML, ha estau amillorau o suporte ta controls ARIA list, gridcell, slider y progressbar.
- Os usuarios agora pueden cambiar a pronuncia de puntuación y atros simbolos, asinas como o ran en que se verbalicen. (#271, #1516)
- En Microsoft Excel, o nombre d'a fuella activa agora s'anuncia quan se cambee de pachina con control+rePág u control+avPág. (#760)
- Quan se navega por una tabla en Microsoft Word con a tecla tab NVDA agora anunciará a celda actual seguntes te muevas. (#159)
- Agora puetz configurar si as coordenadas d'una celda de tabla s'anuncian dende o dialogo de preferencias de formato de documento. (#719)
- NVDA agora puet detectar formato y color ta texto escrito en a pantalla.
- En a lista de mensaches d'Outlook Express/Windows Mail/Windows Live Mail, NVDA agora anunciará o feito que un mensache siga no leito y tamién si ye expandiu u contraito en o caso de filos de conversación. (#868)
- eSpeak agora tien una opción de taxa d'aumento que triplica a velocidat d'a voz.
- Suporte t'o control calandario que se troba en o dialogo d'Información de Fhecha y Hora accediu dende o reloch de Windows 7. (#1637)
- S'han adhibiu combinacions de teclas adicionals t'a linia braille MDV Lilli. (#241)
- Nuevos idiomas: Búlgaro, Albanés.


== Cambeos ==
- Ta mover o cursor d'o sistema a o cursor de revisión, agora presiona o script mover foco a o navegador d'obchectos (Sobremesa NVDA+shift+menos teclau numerico, portatil NVDA+shift+retroceso) dos vegadas en succesión rapida. Isto libera mas teclas en o teclau. (#837)
- Ta escuitar a representación decimal y hexadecimal d'o caracter baixo o cursor de revisión, agora presiona revisar caracter actual tres vegadas en cuenta de dos vegadas, ya que dos vegadas agora verbaliza a descripción d'o caracter.
- Actualizau o sintetizador de voz eSpeak a 1.45.03. (#1465)
- As tablas de  disenyo ya no s'anuncian  en aplicacions de Mozilla Gecko mientras se mueve o foco quan se ye en modo foco u difuera d'un documento.
- En Internet Explorer y atros controls  MSHTML, o modo navegación agora funciona t'os documentos dentro d'aplicacions ARIA. (#1452)
- Actualizau o transcriptor braille  liblouis a 2.3.0.
- Quan se ye en modo navegación y se blinca a un control con quicknav u foco, a descripción d'o control agora s'anuncia si tien un.
- As barras de progreso agora s'anuncian en modo navegación.
- Os nodos marcaus  con un paper ARIA de presentación en Internet Explorer y atros controls MSHTML agora se filtran difuera d'a revisión simpla y l'ancestro d'o foco.
- A interface d'usuario y a documentación de NVDA agora se refieren a os modos virtuals como modo navegación , ya que o termin "virtual buffer" ye menos comprensible t'a mayoría d'os usuarios. (#1509)
- Quan l'usuario deseye copiar as suyas opcions d'usuario a o perfil d'o sistema ta utilizar-las en pantallas d'autentificación, etc., y as suyas opcions contiengan plugins personals, agora serán advertius que isto podría suposar un risgo de seguranza. (#1426)
- O servicio NVDA ya no encieta y detiene a NVDA en escritorios de dentrada d'usuario.
- En Windows XP y Windows Vista, NVDA ya no fa uso de UI Automation encara si ye disponible a traviés de l'actualización d'a plataforma. Encara que utilizando UI Automation se puet amillorar l'accesibilidat de qualques aplicacions modernas, en XP y Vista i heba muitos penches, rupturas y se perdeba toda a buena funcionalidat utilizando-lo. (#1437)
- En aplicacions que utilizan Mozilla Gecko 2 y posterior (tals como Firefox 4 y posterior), agora puet leyer-se un documento en modo navegación antis que a carga finalice completament.
- NVDA anuncia agora o estau d'un contenedor quan o foco se mueva a un control dentro d'ell (eix.: si o foco se mueve dentro d'un documento que encara se siga cargando l'anunciará como ocupau).
 - A interface d'usuario y documentación de NVDA ya no utiliza os termins "primer fillo" y "pai" respective a navegación d'obchectos, pus istos termins son confusos ta muitos usuarios.
 - Ya no s'anuncia contraito ta qualques elementos de menú que tienen submenús.
- O script reportCurrentFormatting (NVDA+f) agora anuncia o formato en a posición d'o cursor de revisión antis que o cursor d'o sistema / foco. Ya que de forma predeterminada o cursor de revisión sigue a o d'o sistema, a mayor parti d'a chent no habría de notar a diferencia.  Manimenos isto agora posibilita a l'usuario mirar o formato quan se mueva o cursor de revisión, tal como en a revisión plana.


== Corrección de fallos ==
- Contrayer quadros combinaus en documentos en modo navegación quan o modo foco ha estau forzau con NVDA+espacio ya no retorna automaticament a modo navegación. (#1386)
- En documentos Gecko (eix.: Firefox) y MSHTML (eix.: Internet Explorer), NVDA agora procesa correctament  cierto texto en a mesma linia que previament estió procesau en linias separadas. (#1378)
- Quan o Braille sigue a la revisión y o navegador d'obchectos se mueve a un documento en modo navegación, u manualment u a causa d'un cambeo de foco, o braille amostrará adequadament o conteniu d'o modo de navegación. (#1406, #1407)
- Quan a verbalización d'a puntuación siga desactivada, bella puntuación ya no se verbaliza incorrectament quan s'utilicen qualques sintetizadores. (#332)
- Ya no ocurren problemas quan se carga a configuración ta sintetizadores que no suportan a opción de voz tals como Audiologic Tts3. (#1347)
- O menú de Skype Extras agora se leye correctament. (#648)
- Marcando a caixeta de verificación Brilo Controla o Volumen en o dialogo Opcions de Rato ya no habría de causar un retardo mayor ta pitidos quan se mueve o rato a lo largo d'a pantalla en Windows Vista/Windows 7 con Aero activau. (#1183)
- Quan NVDA se configura ta utilizar a distribución de teclau portatil, NVDA+suprimir agora funciona como se documentó t'anunciar as dimensions d'o navegador d'obchectos actual. (#1498)
- NVDA agora cumple apropiadament con l'atributo aria-selected en documentos d'Internet Explorer.
- quan NVDA cambea automaticament a modo foco en documentos de modo navegación, agora anuncia información sobre o contexto d'o foco. Por eixemplo, si un elemento d'un quadro de lista recive o foco, o quadro de lista s'anunciará primer. (#1491)
- En Internet Explorer y atros controls MSHTML, os controls ARIA listbox agora se tractan como listas, en cuenta de como elementos de lista.
- Quan un control editable de texto de solament lectura recibe o foco, NVDA agora informa que ye de solament lectura. (#1436)
- En modo navegación, NVDA agora funciona correctament respective a campos de texto editable de solament lectura.
- En documentos en modo navegación, NVDA ya no cambea incorrectament de modo foco quan aria-activedescendant ye configurau; eix.: quan a finalización d'a lista amaneixe en qualques controls con autocompletado.
- En Adobe Reader, o nombre de controls agora s'anuncia quan se mueve o foco u s'utiliza navegación rapida en modo navegación.
- En documentos XFA PDF en Adobe Reader, botons, vinclos y graficos agora se procesan correctament.
- En documentos XFA PDF en Adobe Reader, totz os elementos agora se procesan en linias por separau.  Iste cambeo se fació porque as seccions grans (a vegadas tot o documento) se procesaban sin saltos a causa d'o retardo cheneral d'a estructura en istos documentos.
- Correchius problemas quan se mueve o foco dende campos de texto editable en documentos XFA PDF en Adobe Reader.
- En documentos XFA PDF en Adobe Reader, os cambeos a la valor d'un quadro combinau enfocau agora s'anunciarán.
- Os quadros combinaus Owner-drawn tals como os de trigar colors en Outlook Express agora son accesibles con NVDA. (#1340)
- En idiomas que utilizan un espacio como separador de grupo de milar tals como francés y alemán, os numeros de grupos separaus de texto ya no se pronuncian como un solament numero. Isto yera particularment problematico ta celdas de tablas que contiengan numeros. (#555)
- Os nodos con un paper de descripción d'ARIA en Internet Explorer y atros controls MSHTML agora se clasifican como texto estatico, no como campos d'edición.
- Correchius quantos problemas quan se presiona tab mientras o foco ye en un documento en modo navegación (eix.: tab se mueve inadequadament a la barra d'adrezas en Internet Explorer). (#720, #1367)
- Quan se dentra en listas mientras se leye texto, NVDA agora diz, por eixemplo, "lista con 5 elementos" en cuenta de "listacon 5 elementos". (#1515)
- En o modo d'aduya de dentrada, os cenyos son en o sistema encara si os suyos scripts deixan pasar la aduya de dentrada tals como as ordens de desplazamiento d'a linia braille enta debant y dezaga.
- En o modo d'aduya de dentrada, quan una modificadera se mantiene pretada en o teclau, NVDA ya no anuncia a modificadera como si se modificase a ell mesma; eix.: NVDA+NVDA.
- En documentos d'Adobe Reader, o presionado de c u shift+c ta navegar a un quadro combinau agora funciona.
- O estau seleccionau de ringleras de tabla seleccionables agora s'anuncia d'o mesmo modo que t'os elementos de lista y arbol.
- Os controls en Firefox y atras aplicacions Gecko agora pueden activar-se mientras se ye en modo navegación encara si o suyo conteniu ha estau flotando difuera de pantalla. (#801)
- Ya no se puet amostrar un dialogo d'opcions de NVDA mientras se ye amostrando un mensache de dialogo, ya que o dialogo d'opcions se penchaba en iste caso. (#1451)
- Reinstaurado o dialogo editor de celdas d'Excell de NVDA que s'heba desactivau accidentalment en NVDA 2011.1.
- En Microsoft Excel, ya no bi ha un retardo quan se manteneban pretadas u se pretaban teclas rapidament ta mover-se entre celdas u seleccionar-las.
- Correchidas rupturas d'o servicio NVDA que significaban que NVDA aturaba d'executar-se en en finestras seguras de Windows.
- Correchius problemas que ocurriban a vegadas con linias braille quan un cambeo causaba que o texto que yera amostrando-se desapareixese.
- A finestra de descargas en Internet Explorer 9 agora puet navegar-se y leyer-se con NVDA. (#1280)
- Ya no ye posible encetar accidentalment multiples copias de NVDA a o mesmo tiempo. (#507)
- En sistemas lentos, NVDA ya no causa que a suya finestra prencipal s'amuestre inadequadament tot o tiempo mientras s'executa. (#726)
- NVDA ya no se trenca en Windows xP quan s'encieta una aplicación WPF. (#1437)
- Leyer tot y leyer tot con cursor de revisión agora podrá funcionar en qualques controls de texto UI automation que suporten totz os metodos necesarios. (eix.: agora puetz utilizar verbalizar toda a revisión en documentos de XPS Viewer).
- NVDA ya no clasifica inadequadament qualques elementos de lista en l'aplique de reglas de mensaches en Outlook Express / Windows Live Mail agora o dialogo ye como caixetas de verificación. (#576)
- Os quadros combinaus ya no s'anuncian como tenendo un submenú.
- NVDA agora podrá leyer o recipiente en os campos ta2, CC y CCO en Microsoft Outlook. (#421)
- Correchiu o fallo en o dialogo d'Opcions de Voz de NVDA an a valor d'as barras de desplazamiento  a vegadas no s'anunciaba quan cambiaban. (#1411)
- NVDA ya no falla en anunciar a celda nueva quan se mueve en una fuella Excel dimpués de tallar y apegar. (#1567)
- NVDA ya no lo fa tant mal endevinando os nombres d'as colors anunciando a mayoría d'os mesmos.
- En Internet Explorer y atros controls MSHTML, se corrichió a incapacidat ta leyer partes de pachinas extranyas que contienen iframes marcaus con un paper ARIA de presentación. (#1569)
- En Internet Explorer y potros controls MSHTML, se corrichió un problema extranyo an o foco remaniba rebotando infinitament entre o documento y un campo editable de texto multilínea en modo foco. (#1566)
- En Microsoft Word 2010 NVDA agora leyerá automaticament os dialogos de confirmación. (#1538)
- En campos editables multilínea de texto en Internet Explorer y atros controls MSHTML, a selección en linias dimpués d'o primer agora s'anuncia correctament. (#1590)
- Amillorau o movimiento por parolas en muitos casos, incluindo modo navegación y controls d'edición de Windows. (#1580)
- L'instalador de NVDA ya no amuestra texto confuso ta versions ta Hong Kong de Windows Vista y Windows 7. (#1596)
- NVDA ya no falla en cargar o sintetizador de Microsoft Speech API versión 5 si a configuración contiene opcions ta ixe sintetizador pero falta a opción d'a voz. (#1599)
- En o modo navegación de firefox, NVDA ya no se niega a incluir conteniu que siga dentro d'un nodo enfocable con un paper ARIA de presentación.
- En Microsoft Word con o braille activau, as linias en pachinas dimpués d'a primera pachina agora s'anuncian correctament. (#1603)
- En Microsoft Word 2003, as linias de texto de dreita a cucha pueden leyer-se una vegada de nuevo con o braille activau. (#627)
- En Microsoft Word, leyer tot agora funciona correctament quan o documento no finaliza con un final de frase.
- Quan s'ubre un mensache de texto plano en Windows Live Mail 2011, NVDA enfocará correctament o documento de mensache permitindo que se leiga.
- NVDA ya no se pencha u se niega a charrar temporalment quan ye en os dialogos Mover a / Copiar a en Windows Live Mail. (#574)
- En Outlook 2010, NVDA agora seguirá correctament o foco en a lista de mensaches. (#1285)
- S'han resuelto qualques problemas de connexión d'USB con a linia braille MDV Lilli. (#241)
- En Internet explorer y atros controls MSHTML, os espacios ya no s'ignoran en modo navegación en bells casos (ye decir dimpués d'un vinclo).
- En Internet Explorer y atros controls MSHTML, han estau eliminaus qualques extranyos cambeos de linia en modo navegación. Especificament, elementos HTML con un estilo de pantalla None ya no forza un blinco de linia. (#1685)
- Si NVDA no ye capaz d'encetar-se, o fracaso ta reproducir o son d'aturada critica de Windows ya no anula o mensache d'error critica en o fichero de log.


== Cambeos ta Desembolicadors ==
- A documentación de desembolicadors agora puet chenerar-se utilizando SCons. mira readme.txt en a radiz d'a distribución fuent ta detalles, incluindo dependencias asociadas.
- As Localizacions agora pueden proporcionar descripcions ta caracters. Mira a sección Character Descriptions d'a Developer Guide ta detalles. (#55)
- As Localizacions agora pueden proporcionar información sobre a pronuncia de puntuación especifica y atros simbolos. Mira a sección Symbol Pronunciation d'a Developer Guide ta detalles. (#332)
- Agora puetz compilar NVDAHelper con quantas opcions de depuración utilizando a variable nvdaHelperDebugFlags SCons. Mira readme.txt en a radiz d'a distribución de fuents de ta2 detalles. (#1390)
- Os controladors de sintesis agora se pasan como una seqüencia de texto y ordens de voz a verbalizar, en cuenta de solament texto y un indiz.
 - Isto permite indices integraus, cambeos de parametros, etc.
 - Os controladors habrían d'implementar SynthDriver.speak() en cuenta de SynthDriver.speakText() y SynthDriver.speakCharacter().
 - Os metodos antigos s'utilizarán si SynthDriver.speak() no s'implementó, pero han quedau en desuso y s'eliminarán en una versión futura.
- S'ha eliminau gui.execute(). Habría d'utilizar-se wx.CallAfter() en o suyo puesto.
- Ha estau eliminau gui.scriptUI .
 - Ta dialogos de mensache, utiliza wx.CallAfter(gui.messageBox, ...).
 - Ta totz os de demás dialogos, habrían d'utilizar-se os dialogos propios de wx en o suyo puesto.
 - Una nueva función gui.runScriptModalDialog() simplifica a utilización de dialogos modals de scripts.
- Agora os controladors de sintetizador pueden suportar opcions booleanas.  Mira SynthDriverHandler.BooleanSynthSetting.
- SCons agora accepta una variable certTimestampServer especifycando a URL d'un servidor timestamping ta utilizar unas marcas timestamp authenticode. (#1644)


= 2011.1.1 =
Ista versión corriche quantos problemas de seguranza y atros importants trobaus en NVDA 2011.1.

== Corrección de Fallos ==
- L'elemento Donar en o menú NVDA agora se desactiva quan s'executa en l'autentificación, bloqueyo, UAC y atras Finestras de pantallas seguras, ya que isto ye un risgo de seguranza. (#1419)
- Agora ye imposible copiar u apegar dentro d'a finestra d'interface de l'usuario de NVDA mientras se ye en escritorios seguros (Pantalla blocada, pantalla d'o UAC y autentificación de windows) ya que isto ye un risgo de seguranza. (#1421)
- En Firefox 4, a orden mover a o conteniu d'o modo virtual (NVDA+control+espacio) agora funciona como habría d'escapar d'obchectos empotrados tals como conteniu Flash. (#1429)
- Quan verbalizar teclas d'ordens siga activau, os caracters mayusculados ya no se verbalizan incorrectament como teclas d'ordens. (#1422)
- Quan verbalizar teclas d'ordens siga activau,, presionando espacio con atros modificadors que shift (tals como control y alt) agora s'anuncian como una tecla d'ordens. (#1424)
- O Logging agora se desactiva completament quan s'execute dende l'autentificación, bloqueyo, UAC y atras finestras seguras, ya que isto ye un risgo de seguranza. (#1435)
- En o modo d'aduya de dentrada, os cenyos agora se connectan encara si no son vinculaus a un script (d'alcuerdo con la guía de l'usuario. (#1425)


= 2011.1 =
Lo subrayable en ista versión incluye l'anunciau de colors ta qualques controls; anunciau automatico d'a salida de texto nuevo en mIRC, PuTTY, Tera Term y SecureCRT; suporte ta plugins globals; anunciau de vinyetas  y numeración en Microsoft Word; combinacions de teclas adicionals ta linias braille, incluindo teclas ta mover-se a la linia siguient y anterior; y suporte ta quantas linias braille Baum, HumanWare y APH.

== Nuevas Caracteristicas ==
- Agora se pueden anunciar as colors ta qualques controls. L'anunciau automatico se puet configurar en o dialogo de preferencias de formateado de documentos. Tamién se pueden anunciar baixo demanda utilizando a orden d'anunciau de formato de texto (NVDA+f).
 - Inicialment, isto se suporta en controls de texto estandar IAccessible2 (tals como en aplicacions de Mozilla), controls RichEdit (tals como en Wordpad) y controls de texto d'IBM Lotus Symphony.
- En os modos virtuals, agora puetz seleccionar por pachina (utilizando shift+AvPág y shift+RePág) y por paragrafos(utilizando shift+control+Flecha Abaixo y shift+control+Flecha Alto). (#639)
- NVDA agora anuncia a salida de texto nuevo en mIRC, PuTTY, Tera Term y SecureCRT. (#936)
- Os usuarios agora pueden adhibir nuevas combinacions de teclas u u sobrescribir as existents ta qualsiquier script en NVDA proporcionando un sencillo mapa de movimientos de dentrada de l'usuario. (#194)
- Suporte ta plugins globals. Os plugins globals pueden adhibir nueva funcionalidat a NVDA que funcione en todas as aplicacions. (#281)
- Agora s'escuita un chicot pitido quan se teclean caracters con a tecla shift entre que o BloqMayus siga activau. Isto se puet desactivar desmarcando a nueva opción relacionada en o dialogo d'Opcions de Teclau . (#663)
- Agora s'anuncian os saltos de pachina quan nos movemos por linias en Microsoft Word. (#758)
- As vinyetas y a numeración se verbalizan agora en Microsoft Word quan nos movemos por linias. (#208)  
- Agora ye disponible una orden t'activar u desactivar o modo Durmiente ta l'aplicación actual (NVDA+shift+s). O Modo Durmiente (anteriorment conoixiu como modo de voz propia) desactiva toda a funcionalidat de lectura d'a pantalla en NVDA ta una aplicación en particular. Muit util t'aplicacions que proporcionan a suya propia voz y u caracteristicas de lectura de pantalla. Presiona ista orden de nuevo ta desactivar o Modo Durmiente.
- S'adhibioron qualques combinacions de teclas adicionals ta linias braille. Mira a sección Linias braille Suportadas de la Guía de l'Usuario ta detalles. (#209)
- Ta conveniencia de desembolicadors de terceras partes, os app modules asinas como os plugins globals agora se pueden recargar sin reinicializar NVDA. Utiliza Ferramientas -> Recargar plugins en o menú de NVDA u NVDA+control+f3. (#544)
- NVDA agora recuerda a posición an yeras quan tornas a una pachina anteriorment visitada. Isto s'aplica dica que u o navegador u NVDA sigan zarraus. (#132)
- As linias braille Handy Tech agora pueden utilizar-se sin instalar o controlador universal d'Handy Tech. (#854)
- Suporte ta quantas linias braille Baum, HumanWare y APH. (#937)
- Agora se reconoixe a barra d'estau en Meya Player Classic Home Cinema.
- Agora a linia braille Freedom Scientific Focus 40 Blue puet utilizar-se quan se connecte a traviés de bluetooth. (#1345)

 
== Cambeos ==
- A información de posición ya no s'anuncia de traza predeterminada en qualques casos án yera normalment incorrecto; eix.: a mayoría d'os menús, a barra d'aplicacions en execución, l'aria de notificacions, etc. Manimenos, isto puet activar-se de nuevo con una opción adhibida en o dialogo d'Opcions de presentación d'obchectos.
- Aduya de Teclau s'ha renombrau a Aduya de dentrada ta reflejar que se manea dentrada dende atras fuents que o teclau.
- A localización d'un script en o codigo ya no s'anuncia en la aduya de dentrada meso que ye irrelevant y criptica ta l'usuario.
- Quan NVDA detecta que s'ha penchau, contina interceptando  as teclas modificaderas de NVDA, encara que deixa pasar todas as de demás teclas d'o sistema. Isto apreviene a l'usuario de commutar inintencionalmente o BlogMayus, etc. Si presionan una tecla modificadera de NVDA sin realising NVDA has frozen. (#939)
- Si as teclas se mantienen pretadas dimpués d'utilizar a orden de deixar pasar, todas as teclas (incluindo repeticions de teclas) agora se pasan dica que a zaguera tecla  siga soltada.
- Si una tecla modificadera de NVDA se presiona dos vegadas en succesión rapida ta pasar-la y a segunda presionada ye pretada, todas as teclas repetidas agora se pasarán tamién.
- As teclas puyar, baixar volumen y silenciar agora s'anuncian  en la Aduya de Dentrada. Isto podría estar d'utilidat si l'usuario no sabe qué fan ixas teclas.
- A tecla rapida ta l'elemento Cursor de Revisión en o menú de Preferencias de NVDA ha estau cambiau de r a c ta eliminar o conflicto con l'elemento d'Opcions de Braille.


== Corrección de Fallos ==
- Quan s'adhibe una nueva dentrada d'o diccionario d'o fabla, o titol d'o dialogo agora ye "Adhibir Dentrada de Diccionario" en cuenta de "Editar dentrada de diccionario". (#924)
- En os dialogos d'o diccionario d'o fabla, o conteniu d'as columnas d'a Expresión Regular y sensible a las mayusclas d'a lista de dentradas de diccionario  se presienta agora en l'idioma configurau en NVDA en cuenta de siempre en Inglés.
- En AIM, a información de posición agora s'anuncia en arbols.
- En barras d'eslizamiento en o dialogo Opcions de Voz, flecha alto/rePág/inicio agora incrementan a opción y flecha abaixo/AvPág/fin a decrementan. Anteriorment, ocurriba l'opuesto, o qual no ye lochico y ye inconsistent con as opcions d'o grupo synth. (#221)
- En modos virtuals con a distribución de pantalla deshabilitada, ya no amaneixen qualques extranyas linias en blanco.
- Si una tecla modificadera de NVDA se presiona dos vegadas rapidament pero bi ha una tecla presionada intervenindo, a tecla modificadera de NVDA ya no pasa en a segunda presión.
- As teclas de puntuación agora se verbalizan en la aduya de dentrada quan a verbalización d'a puntuación siga desactivada. (#977)
- En o dialogo Opcions de Teclau, os nombres de distribución de teclau agora se presientan en l'idioma configurau ta NVDA en cuenta de siempre en Inglés. (#558)
- Correchiu un problema an qualques elementos se renderizaban como vuedos en documentos d'Adobe Reader; eix.: os vinclos en a tabla de conteniu de la Guía de l'usuario de l'Apple iPhone IOS 4.1.
- O botón "Utilizar opcions actuals alzadas en o logon y atras pantallas seguras" en o dialogo d'Opcions Chenerals de NVDA, funciona si s'utilizó immediatament dimpués que NVDA siga instalau nuevament pero antis que una pantalla segura haiga amaneixiu.  Anteriorment, NVDA anunciaba que o copiau tenió exito, pero actualment no teneba efecto. (#1194)
- Ya no ye posible tener dos dialogos d'opcions de NVDA ubiertos simultaniament. Isto corriche errors an un dialogo ubierto depende d'unatro dialogo ubierto; ye decir, cambiar o sintetizador mientras o dialogo Opcions de Voz ye ubierto. (#603)
- En sistemas con UAC activau, o botón "Utilizar opcions actualment alzadas en o logon y pnatallas seguras" en o dialogo d'Opcions Chenerals d'o NVDA, ya no falla dimpués d'o UAC si o nombre d'a cuenta de l'usuario contiene un espacio. (#918)
- En Internet Explorer y atros controls MSHTML, NVDA utiliza agora a URL como un zaguer resorte ta determinar o nombre d'un vinclo, mas que presentar vinclos vuedos. (#633)
- NVDA ya no ignora o foco en os menús d'AOL Instant Messenger 7. (#655)
- Anunciar a etiqueta correcta ta errors en o dialogo d'o corrector d'ortografía de Microsoft Word (eix.: No en diccionario, error gramatical, puntuación). Anteriorment totz s'anunciaban como error gramatical. (#883)
- Tecleando en Microsoft Word mientras s'utiliza una linia braille ya no habría de causar que siga tecleado texto ilechible, y un extranyo penche quan se presiona un sensor de seguimiento braille en documentos de Word ha estau correchiu. (#1212) No osstante una limitación ye que o texto en arabe puet no leyer-se ya en Word 2003 y superior, mientras s'utiliza una linia braille. (#627)
- Quan se presiona a tecla supr en un campo d'edición, o texto/cursor en una linia braille agora habría d'actualizar-se siempre apropiadament ta reflejar o cambeo. (#947)
- Os cambeos en pachinas en documentos Gecko2 (Eix.: Firefox 4) mientras s'ubren multiples pestanyas agora se refleja adequadament por NVDA. Anteriorment solament os cambeos en a primera pestanya se reflejaban. (Mozilla bug 610985)
- NVDA agora puet anunciar apropiadament as sucherencias ta errors gramaticals y de puntuación en o dialogo d'o corrector d'ortografía de Microsoft Word. (#704)
- En Internet Explorer y atros controls MSHTML, NVDA ya no presienta ancoras de destín como vinclos vuedos en o suyo modo virtual. En o suyo puesto, istas ancoras s'amagan seguntes habría d'estar. (#1326)
- A navegación d'obchectos sobre y dentro de brupos estandar de windows ya no trenca y asymmetrical.
- En Firefox y atros controls basaus en Gecko, NVDA ya no se queda apegau en un submarco si finaliza cargando antis d'unatro documento.
- NVDA agora anuncia apropiadament o siguient caracter quan s'elimina un caracter con suprimir d'o teclau numerico. (#286)
- En a pantalla d'autentificación de Windows XP, o nombre d'usuario s'anuncia una vegada de nuevo quan l'usuario seleccionau se cambió.
- Correchius problemas quan en leyer texto en consolas d'ordens de Windows l'anunciau de numeros de linia ye activau.
- O dialogo de lista d'elementos ta modos virtuals agora ye utilizable por usuarios videntes.  Totz os controls son visibles en pantalla. (#1321)
- A lista de dentradas en o dialogo Diccionarios d'o Fabla, agora ye mas leyible por usuarios videntes.  A lista agora ye pro gran t'amostrar todas as suyas columnas en pantalla. (#90)
- En linias braille ALVA BC640/BC680 NVDA ya no fa caso omiso d'as teclas d'a linia que encara son estando pretadas dimpués que unatra tecla siga liberada.
- Adobe Reader X ya no se trenca quan se zarra un documento sin opcions no etiquetadas antis que amaneixca o dialogo de procesamiento. (#1218)
- NVDA agora cambea a o controlador de linia braille apropiau quan tornes a la configuración alzada. (#1346)
- L'asistent de prochecto de Visual Studio 2008 se leye correctament nuevament. (#974)
- NVDA ya no falla completament en treballar en aplicacions que contiengan caracters no ASCII en o suyo nombre de l'executable. (#1352)
- Quan se leye por linias en AkelPad con o blinco de parolas activau, NVDA ya no leye o primer caracter d'a linia siguient en o final d'a linia actual.
- En l'editor de codigo de Visual Studio 2005/2008, NVDA ya no leye tot o texto dimpués de cada caracter tecleado. (#975)
- Correchiu o problema an qualques linias braille no se limpiaban correctament quan NVDA se zarraba u se cambiaba a linia braille.
- O foco inicial ya no se verbaliza en qualques ocasions dos vegadas quan NVDA ranca. (#1359)


== Cambeos ta Desembolicadors ==
- SCons agora s'utiliza ta preparar l'arbol fuent y creyar compilacions binarias, fichers portables, instaladores, etc. Mira readme.txt en a radiz d'a distribución fuent ta detalles.
- Os nonbres de teclas utilizaus por NVDA (incluindo mapas de teclas) han estau feitos mas amigables/lochicos; eix.: upArrow en cuenta d'extendedUp y numpadPageUp en cuenta de prior. Mira o modulo vkCodes ta una lista.
- Toda a salida de l'usuario agora se represienta por una instancia inputCore.InputGesture. (#601)
 - Cada fuent d'a dentrada ye una subclase d'a clase base InputGesture.
 - A pulsación de teclas en o teclau d'o sistema s'incluye en a clase keyboardHandler.KeyboardInputGesture.
 - A pulsación de botons, ruedas y atros controls en una linia braille s'incluye en as subclases d'a clase braille.BrailleDisplayGesture . Istas subclases se proporcionan por cada controlador de linia braille.
- Os cenyos de dentrada se vinculan a ScriptableObjects utilizando o metodo ScriptableObject.bindGesture() en una instancia u un diccionario __gestures en a clase que os suyos identificadors de mapas de cenyos a nombres de scripts. Mira baseObject.ScriptableObject ta detalles.
- Os modulos d'aplicación ya no tienen fichero de mapa de teclas. Totz os vinclos de dentrada de cenyos han de fer-se en l'appModule mesmo.
- Totz os scripts agora prenen una sentencia InputGesture en cuenta d'una pulsación de tecla.
 - Pueden ninviar-se keyboardInputGestures a o TOS utilizando o metodo send() d'o cenyo.
- Ta ninviar una pulsación de tecla arbitrariament, agora has de creyar un KeyboardInputGesture utilizando KeyboardInputGesture.fromName() y dimpués utilizar o suyo metodo send().
- As localizacions agora podrán proporcionar un fichero de mapa de cenyo de dentrada t'adhibir nuevos vinclos u sobrescribir os vinclos existents t'os scripts en qualsiquier puesto de NVDA. (#810)
 - Locale gesture maps should be placet in locale\LANG\gestures.ini, where LANG is the language code.
 - See inputCore.GlobalGestureMap for details of the file format.
- The new LiveText and Terminal NVDAObject behaviors facilitate automatic reporting of new text. See those classes in NVDAObjects.behaviors for details. (#936)
 - The NVDAObjects.window.DisplayModelLiveText overlay class can be used for objects which must retrieve text written to the display.
 - See the mirc and putty app modules for usage examples.
- There is no longer an _default app module. App modules should instead subclass appModuleHandler.AppModule (the base AppModule class).
- Support for global plugins which can globally bind scripts, handle NVDAObject events and choose NVDAObject overlay classes. (#281) See globalPluginHandler.GlobalPlugin for details.
- On SynthDriver objects, the available* attributes for string settings (y.g. availableVoices and availableVariants)  are now OrderedDicts keyed by IT instead of lists.
- synthDriverHandler.VoiceInfo now takes an optional language argument which specifies the language of the voice.
- SynthDriver objects now provide a language attribute which specifies the language of the current voice.
 - The base implementation uses the language specified on the VoiceInfo objects in availableVoices. This is suitable for most synthesisers which support one language per voice.
- Braille display drivers have been enhanced to allow buttons, wheels and other controls to be bound to NVDA scripts:
 - Drivers can provide a global input gesture map to add bindings for scripts anywhere in NVDA.
 - They can also provide their own scripts to perform display specific functions.
 - See braille.BrailleDisplayDriver for details and existing braille display drivers for examples.
- The 'selfVoicing' property on AppModule classes has now been renamed to 'sleepMode'.
- the appModule events: event_appLoseFocus and event_appGainFocus have now been renamed to event_appModule_loseFocus and event_appModule_gainFocus respectivly, in order to keep the naming sintax the same between appModules and treeInterceptors etc.
- All braille display drivers should now use braille.BrailleDisplayDriver instead of braille.BrailleDisplayDriverWithCursor.
 - The cursor is now managed outside of the driver.
 - Existing drivers need only change their class statement accordingly and rename their _display method to display.

 
= 2010.2 =
As caracteristicas mas notables d'ista versión incluyen una gran simplificación d'a navegación d'obchectos; modos virtuals ta conteniu d'Adobe Flash; acceso a muitos controls anteriorment inaccesibles capturando texto escrito a la pantalla; revisión plana de texto en pantalla; suporte ta documentos d'IBM Lotus Symphony; anunciau de capiters de ringlera y columna de tabla en Mozilla Firefox; una millora significativa d'a documentación de l'usuario.

== Nuevas Caracteristicas ==
- A navegación por obchectos con o cursor de revisión ha estau muit simplificada. O cursor de revisión agora excluye obchectos que no sigan utils ta l'usuario; ye decir, obchectos solament utilizaus ta propositos de disenyo y obchectos no disponibles.
- En aplicacions que utilizan o Java Access Bridge (incluindo OpenOffice.org), o formato agora puet informar-se en controls de texto. (#358, #463)
- Quan se mueve o rato sobre celdas en Microsoft Excel, NVDA las anunciará apropiadament.
- En aplicacions que utilizan o Java Access Bridge, o texto d'un dialogo agora s'anuncia quan o dialogo amaneixca. (#554)
- Agora se puet utilizar un modo virtual ta navegar por o conteniu d'adobe Flash. Navegar por obchectos y interactuar con os controls dreitament (activando o modo foco) ya se suporta. (#453)
- Os controls de texto editable en l'IDE Eclipse, incluindo l'editor de codigo, agora son accesibles. Has d'utilizar Eclipse 3.6 u superior. (#256, #641)
- NVDA agora puet recuperar a mayoría de texto escrito en a pantalla. (#40, #643)
	- Isto permite a lectura de controls que no exposan información en formas mas directas/fiables.
	- Os controls que s'accesibilizan por ista caracteristica incluyen: qualques elementos de menú que amuestran iconos (eix.: o menú Ubrir con en fichers en Windows XP) (#151), campos de texto editables en aplicacions Windows Live (#200), a lista d'errors en Outlook Express (#582), o control de texto editable en TextPad (#605), listas en Eudora, muitos controls en Australian Y-tax y a barra de formulas en Microsoft Excel.
- Suporte ta l'editor de codigo en Microsoft Visual Studio 2005 y 2008. A lo menos se requiere Visual Studio Standard; isto no funciona en as edicions Express. (#457)
- Suporte ta documentos en IBM Lotus Symphony.
- Suporte primario y experimental paraGoogle Chrome. Por favor tien en cuenta que o suporte ta lectors de pantalla de Chrome ye luen de completar-se y requerirá treballo adicional tamién en NVDA. Amenesterás una compilación de desembolique recient de Chrome ta prebar isto.
- O estau d'as teclas commutables (Bloq Mayus, bloq núm y bloqueyo de desplazamiento) agora s'amuestra en braille quan son pretadas. (#620)
- Os globos d'aduya agora s'amuestran en braille quan amaneixcan. (#652)
- Adhibiu un controlador t'a linia braille MDV Lilli. (#241)
- Quan se selecciona una ringlera u una columna completa en MS Excel con as teclas d'alcorce shift+espacio y control+espacio, a nueva selección agora s'anuncia. (#759)
- Os capiters de ringlera y columna agora pueden anunciar-se. Isto ye configurable dende o dialogo de preferencias de formato de documento.
 - Actualment, isto se suporta en documentos en aplicacions de Mozilla tals como Firefox y Thunderbird. (#361)
- Introducidas ordens t'a revisión plana: (#58)
 - NVDA+7 teclau numerico cambea a revisión plana, colocando o cursor de revisión en a posición de l'obchecto actual, permitindo-te revisar a pantalla (u un documento si se ye dentro d'un) con as ordens de revisión de texto.
 - NVDA+1 teclau numerico mueve o cursor de revisión a l'obchecto representau por o texto en a posición d'o cursor de revisión, permitindo-te navegar por obchectos dende ixe punto.
- As opcions d'usuario actuals de NVDA pueden copiar-se ta utilizar-se en as pantallas d'autentificación/UAC, presionando un botón en o dialogo Opcions Chenerals.


== Ccambios ==
- Leyer tot en o navegador d'obchectos  (NVDA+mas d'o teclau numerico), siguient obchecto en fluxo d'o navegador d'obchectos (NVDA+shift+6 d'o teclau numerico) y anterior obchecto en fluxo en o navegtador d'obchectos (NVDA+shift+4 d'o teclau numerico) han estau eliminaus de momento, a causa de fallos y ta liberar as teclas t'atras posibles caracteristicas.
- En o dialogo de sintetizadores de NVDA, agora solament s'amuestra o sintetizador listau. Anteriorment, se prefixaba con o nombre d'o controlador, que solament ye relevant internament.
- Quan se ye en aplicacions empotradas u modos virtuals dentro d'unatro modo virtual (eix.: Flash), agora puetz presionar nvda+control+espacio ta salir de l'aplicación empotrada u modo virtual, a o documento prencipal. Anteriorment, nvda+espacio  s'utilizaba ta isto. Agora nvda+espacio ye solament especificament ta commutar os modos revisión/foco en os modos virtuals.
- Si a o visor de voz (activable en o menú Ferramientas) se le dió o foco (eix.: it se fació clic) o texto nuevo no amaneixerá en o control dica que o foco se mueva. Isto se permite ta seleccionar o texto con mayor facilidat (eix.: ta copiar).
- O visualizador de Log y a consola de Python se maximizan quan s'activen.
- Quan s'enfoca una fuella de calculo en MS Excel, y bi ha mas d'una celda seleccionada, s'anuncia l'aconsiga d'a selección, en cuenta de solament a celda activa. (#763)
- L'alzau d'a configuración, y o cambeo d'opcions sensibles en particular, agora se desactiva quan s'execute en modo seguro (en as pantallas d'autentificación/UAC).
- Actualizau o sintetizador de voz eSpeak a 1.44.01.
- Si NVDA ya ye executando-se, activando l'alcorce de teclau de NVDA en o escritorio (que ye o presionado de control+alt+n) reiniciará a NVDA.
- S'elimina a caixeta de verificación anunciar texto baixo o rato d'o dialogo Opcions de Rato y se reenplaza con una caixeta de verificación Activar seguimiento d'o Rato, que amillora l'emparellau d'o commutau d'o script de seguimiento d'o rato (NVDA+m). 
- S'actualiza a distribución de teclau laptop tal que incluiga todas as ordens disponibles en a distribución desktop y funciona correctament en teclaus no angleses. (#798, #800)
- Milloras significativas y actualizacions a la documentación de l'usuario, incluindo documentación d'as ordens de teclau laptop y sincronización d'a Referencia Rapida d'Ordens de Teclau con la Guía de l'Usuario. (#455)
- Actualizau o transcriptor braille liblouis a la versión 2.1.0. Notablement, isto corriche qualques problemas relacionaus con o Braille Chino 


== Corrección de Fallos ==
- En µTorrent, l'elemento enfocau en a lista de torrents ya no informa repetidament u escamotea o foco quan s'ubre un menú.
- En aplicacions de Mozilla, agora o foco se detecta correctament quan aterriza en una tabla vueda u arbol.
- En aplicacions de Mozilla, "no verificau" agora s'informa correctament ta controls marcables tals como celdas de tabla marcables. (#571)
- En aplicacions de Mozilla, o texto de dialogos aria correctament implementados ya no s'ignora y agora s'informará quan o dialogo amaneixca.
- En Internet Explorer y atros controls MSHTML, l'atributo ran d'ARIA agora se cumple correctament.
- En Internet Explorer y atros controls MSHTML, o paper ARIA agora se triga sobre unatro tipo d'información ta dar una experiencia d'ARIA muito mas correcta y predecible.
- Deteniu un raro penche en Internet Explorer quan se navega por marcos u iFrames.
- En documentos de Microsoft Word, as linias de dreita a cucha (tals como en o texto arabe) pueden leyer-se de nuevo. (#627)
- Fuerte reducción de retardo quan grans cantidatz de texto s'amostraban en una consola d'ordens de Windows en sistemas de 64 bits. (#622)
- En aplicacions de Microsoft Office, NVDA ya no se pencha quan se presionó verbalizar primer plano (NVDA+b) u quan se navegan qualques obchectos en barras de ferramientas. (#616)
- Correchida a verbalización incorrecta de numeros que contienen un 0 dimpués d'un separador; eix.: 1.023. (#593)
- Adobe Acrobat Pro y Reader 9 ya no se penchan quan se zarra un fichero u se levan a cabo atras bells quefers. (#613)
- A selección s'anuncia agora quan se presiona control+a ta seleccionar tot o texto en qualques controls de texto editables tals como en Microsoft Word. (#761)
- En os controls de Scintilla (eix.: Notepad++), o texto ya no se selecciona incorrectament quan NVDA mueve o cursor d'o sistema tal como entre leyer tot. (#746)
- Ye posible de nuevo revisar o conteniu de celdas en MS Excel con o cursor de revisión.
- NVDA puet leyer de nuevo por linias en bells campos d'aria de texto problematicos en Internet Explorer 8. (#467)
- Windows Live Messenger 2009 ya no se zarra immediatament dimpués d'encetar-se mientras NVDA s'executa. (#677)
- En os navegadors web, ya no ye necesario presionar tab ta interactuar con un obchecto empotrado (tal como conteniu Flash) dimpués de presionar intro en l'obchecto empotrado u tornando dende unatra aplicación. (#775)
- En controls de Scintilla (eix.: Notepad++), o comienzo de linias largas ya no se talla quan sobreixen a pantalla. Tamién, istas linias largas s'amostrarán correctament en braille quan se seleccionen.
- En Loudtalks, agora ye posible accedir a la lista de contactos.
- A URL d'o documento y "MSAAHTML Registered Handler" ya no s'anuncia a vegadas falso en Internet Explorer y atros controls MSHTML. (#811)
- En arbols en en l'IDE d'Eclipse,  l'elemento enfocau anteriorment ya no s'anuncia incorrectament quan o foco se mueve a un nuevo elemento.


= 2010.1 =
Ista revisión s'enfoca prencipalment en corrección de fallos y milloras a la experiencia de l'usuario, incluindo qualques correccions significativas d'estabilidat.


== Nuevas caracteristicas ==
- NVDA ya no falla en rancar en un sistema sin dispositivos de salida d'audio. Obviament, será necesario utilizar una linia braille u o Display synthesiser t'a salida en iste caso. (#425)
- Ha estau adhibida una caixeta de verificación Anunciar Zonas a o dialogo d'Opcions de formato de Documento que te permite configurar si NVDA habría d'anunciar zonas en documentos web. Ta compatibilidat con a versión anterior, a opción ye activada de forma predeterminada.
- Si verbalizar teclas d'ordens ye activada NVDA agora anunciará os nombres d'as teclas multimedia (ex.: reproducir, detener, pachina d'inicio, etc.) quan sigan presionadas. (#472)
- NVDA agora anuncia a parola que siga estando eliminada quan se presiona control+retroceso en controls que lo suporten. (#491)
- As flechas de cursor agora pueden estar utilizadas en a finestra d'o formateador Web ta navegar y leyer o texto. (#452)
- Millor suporte de documentos empotrados editables de NVDA (modo de disenyo) en Internet Explorer. (#402)
- Un script nuevo (nvda+shift+menos d'o teclau numerico) te permite mover o foco d'o sistema a o navegador d'obchectos actual.
- Nuevos scripts ta blocar y desbloquiar os botons cucho y dreito d'o rato. Util ta levar a cabo operacions d'arrocegar y soltar. shift+dividir d'o teclau numerico ta blocar/desbloquiar o cucho, shift+multiplicar d'o teclau numerico ta blocar/desbloquiar o dreito.
- Nuevas tablas de transcripción braille: braille computerizau alemán de 8 puntos, Alemán grau 2, braille computerizau Finlandés de 8 puntos, Chino (Hong Kong, Cantonés), Chino (Taiwan, Mandarín). (#344, #369, #415, #450)
- Agora ye posible desactivar a creyación de l'alcorce d'o escritorio (y asinas a tecla d'alcorce) quan s'instala NVDA. (#518)
- NVDA agora puet utilizar IAccessible2 quan se presienta en aplicacions de 64 bit. (#479)
- L'API NVDA Controller Client agora se proporciona ta permitir a las aplicacions controlar a NVDA; eix.: ta verbalizar texto, silenciar a voz, amostrar un mensache en Braille, etc.
- Os mensaches d'información y error agora se leyen en a pantalla d'o logon en Windows Vista y Windows 7. (#506)
- En Adobe Reader, os formularios PDF interactivos desembolicaus con Adobe LiveCycle agora son suportaus. (#475)
- En Miranda IM, NVDA agora leye automaticament os mensaches de dentrada en finestras de chat si l'anunciau de cambeos de conteniu dinamico s'activó. Tamién, han estau adhibidas as ordens t'anunciar os tres mensaches mas recients (NVDA+control+numero). (#546)
- Agora se suportan campos de dentrada de texto en conteniu d'Adobe Flash. (#461)


== Cambeos ==
- O mensache d'aduya de teclau extremadament verboso en o menú d'Inicio de Windows 7 ya no s'anuncia.
- O sintetizador Display agora ha estau reemplazau con un nuevo Visualizador de Fabla. Ta activar-lo, triga Visor de Fabla dende o menú Ferramientas. O Visualizador de Fabla puet estar utilizau independientment de con qué unatro sintetizador de voz sigas treballando.
- Os mensaches en a linia braille serán refusaus automaticament si l'usuario presiona una tecla que signifique un cambeo tal como o movimiento d'o foco. Anteriorment o mensache siempre remaniría seguntes o suyo tiempo configurau.
- A Opción t'achustar o braille a o foco u a o cursor de revisión (NVDA+control+t) agora puet estar tamién configurada dende o dialogo d'opcions braille, y agora tamién s'alza en a configuración de l'usuario.
- Actualizau o sintetizador de voz eSpeak a 1.42.04.
- Actualizau o transcriptor braille liblouis a 1.8.0.
- En os modos virtuals, l'anunciau d'elementos quan se mueve por caracters u parolas ha estau muit amillorau. Anteriorment, yera anunciada una gran cantidat d'información irrelevant y l'anunciau yera muit diferent a ixo quan se mueve por linias. (#490)
- A tecla Control agora simplament detiene a voz como atras teclas, en cuenta de pausar a voz. Ta pausar/reprener a voz, utiliza a tecla shift.
- Ya no s'anuncia a cuenta de ringleras y columnas de tabla quan s'anuncian os cambeos d'o foco, ya que iste anunciau ye masiau verboso y normalment no ye util.


== Corrección de Fallos ==
- NVDA ya no falla en rancar si o suporte UI Automation pareixe estár disponible pero falla en inicializar-se por bella razón. (#483)
- Tot o conteniu d'una ringlera d'una tabla ya no ye anunciau a vegadas quan se mueve o foco entre celdas en aplicacions de Mozilla. (#482)
- NVDA ya no se retarda entre un tiempo largo quan s'expanden elementos de la vista en arbol que contiengan una cantidat muit gran de sub-elementos.
- Quan se listan voces SAPI 5, NVDA agora intenta detectar voces defectuosas y excluir-las d'o dialogo d'Opcions de Voz y d'o grupo d'Opcions de Sintetizador. Anteriorment, quan i heba una voz problematica, o controlador SAPI 5 de NVDA fallaba qualques vegadas en encetar-se.
- Os modos virtuals agora anuncian as teclas d'alcorce de l'obchecto opción que se troba en o dialogo Presentación d'Obchectos. (#486)
- En os modos virtuals, as coordenadas de ringlera/columna ya no se leyen incorrectament por capiters de ringlera y columna quan l'anunciau de tablas ye desactivau.
- En os modos virtuals, as coordenadas de ringlera/columna agora son correctament leitas quan abandonas una tabla y dimpués tornas a dentrar en a mesma celda d'a tabla sin visitar unatra celda en primeras; eix.: presionando flecha alto y dimpués flecha abaixo sobre a primera celda d'una tabla. (#378)
- As linias en blanco en documentos de Microsoft Word y de controls d'edición de Microsoft HTML agora son amostradas apropiadament en linias braille. Anteriorment NVDA amostraba a frase actual en a linia, no a linia actual ta istas situacions. (#420)
- Multiples correccions de seguranza quan s'executa NVDA en o Logon de Windows y en atros Escritorios Seguros.
- A posición d'o cursor (cursor d'o sistema) agora s'actualiza correctament quan se leva a cabo una Lectura Completa que se pase d'o final d'a pantalla, en campos d'edición estandar de Windows y documentos de Microsoft Word. (#418)
- En os modos virtuals, o texto ya no ye incluído incorrectament por imachens dentro de vinclos y cliqueables que son marcaus como irrelevants t'os lectors de pantalla. (#423)
- Correccions t'a distribución de teclau laptop. (#517)
- Quan o braille ye siguindo a la revisión quan enfocas en una finestra de consola d'o dos, o cursor de revisión agora puet navegar apropiadament por o texto en a consola.
- Mientres se treballa con TeamTalk3 u TeamTalk4 Classic VU a barra de progreso contador en a finestra prencipal ya no s'anuncia seguntes s'actualiza. Tamién os caracters especials pueden leyer-se apropiadament en a finestra de dentrada de chat.
- Os elementos ya no son verbalizados dos vegadas en o menú d'inicio de Windows 7. (#474)
- Activando vinclos a la mesma pachina en Firefox 3.6 appropriately se mueve o cursor apropiadament en o modo virtual a o puesto correcto en a pachina.
- Correchiu o problema an bell texto no yera proporcionau en Adobe Reader en bells documentos PDF.
- NVDA ya no verbaliza incorrectament bells numeros separaus por un guión; eix.: 500-1000. (#547)
- En Windows XP, NVDA ya no causa que Internet Explorer se penche quan se commutan caixetas de verificación en Windows Update. (#477)
- Quan s'utiliza en o sintetizador eSpeak incorporau, simultaniament voz y pitidos ya no causa penches intermitents en qualques sistemas. Isto yera mas evident, por eixemplo, quan se copian cantidatz grans de datos en Windows Explorer.
- NVDA ya no anuncia que un documento de Firefox s'ha empliu (eix.: a causa d'una actualización u refresco) quan ixe documento ye en segundo plano. Isto tamién causaba que a barra d'estau de l'aplicación en primer plano siga anunciada falsament.
- Quan se cambean distribucions de teclau de Windows (con control+shift u alt+shift), o nombre completo d'a distribución s'anuncia en voz y braille. Anteriorment solament s'anunciaba en voz, y distribucions alternativas (eix.: Dvorak) no s'anunciaban.
- Si l'anunciau de tablas se desactivó, a información de tabla ya no s'anuncia quan o foco ccambie.


= 2009.1 =
Lo mas resaltable d'ista release incluye o suporte ta edicions de 64 bit de Windows; suporte muit amillorau t'os documentos de Microsoft Internet Explorer y d'Adobe Reader; suporte ta Windows 7; a lectura d'as pantallas de  logon de Windows, control+alt+supr y o control de cuentas d'usuario (UAC); y a capacidat ta interactuar con contenius d'Adobe Flash y de Sun Java en pachinas web. Tamién hemos teniu quantas correccions significativas d'estabilidat y milloras a la experiencia d'usuario cheneral.

== Nuevas Caracteristicas ==
- Suporte oficial ta edicions de 64 bit de Windows! (#309)
- Adhibiu un controlador de sintetizador t'o sintetizador Newfon. Nota que isto requiere una versión especial de Newfon. (#206)
- En os modos virtuals, o modo foco y o modo revisión agora pueden estar anunciaus utilizando sons en cuenta d'a voz. Isto ye activau predeterminadament. Puede estar configurau dende o dialogo de Modo Virtual. (#244)
- NVDA ya no cancela a voz quan as teclas de control d'o volumen son presionadas en o teclau, permitindo a l'usuario cambiar o volumen y escuitar os resultaus actuals immediatament. (#287)
- Rescrito Completament o suporte ta documentos de Microsoft Internet Explorer y Adobe Acrobat. Iste suporte ha estau unificau con o suporte interno utilizau por Mozilla Gecko, asinas caracteristicas tals como a interpretación mas rapida de pachina, navegación extensa y rapida, lista de vinclos, selección de texto, modo foco automatico y suporte de braille son agora disponibles con istos documentos.
- Amillorau o suporte t'o control de selección de calendata trobau en o dialogo  de propiedatz de Calendata / Hora en Windows Vista.
- Amillorau o suporte t'o menú d'inicio Moderno XP/Vista (especificament os menús Totz os programas y puestos). A información de ran apropiada ye agora anunciada.
- A cantidat de texto que ye anunciada con o movimiento d'o rato, ye agora configurable dende o dialogo Opcions d'o Rato. Una esleción de paragrafo, linia, parola u caracter puet estar feita.
- s'anuncian errors d'ortografía baixo o cursor en Microsoft Word.
- suporte t'a corrección ortografica en Microsoft Word 2007. Suporte Parcial podría estar disponible ta versions anteriors de Microsoft Word.
- suporte ta Windows Live Mail (especificament agora os mensaches de texto plano pueden estar leitos).
- En Windows Vista, si l'usuario se mueve a o escritorio seguro (u porque un dialogo de control d'o UAC amaneixe, u porque estió presionado control+alt+supr), NVDA anunciará o feito que l'usuario agora ye en o escritorio seguro.
- NVDA puet anunciar texto baixo o rato dentro de finestras d'a consola d'o dos.
- Suporte ta UI Automation a traviés de l'API client UI Automation disponible en Windows 7, tanto como s'amillora a experiencia de NVDA en Windows 7.
- NVDA puet estar configurau ta encetar-se automaticament dimpués que t'identifiques en Windows. a opción ye en o dialogo Opcions Chenerals.
- NVDA puet leyer pantallas seguras de Windows tals como l'autentificación de Windows (logon), control+alt+suprimir y pantallas d'o UAC en Windows XP y posteriors. A lectura d'as pantallas d'autentificación de Windows (logon) puet estar configurada dende o dialogo d'Opcions Chenerals. (#97)
- Adhibiu un controlador t'as linias braille d'a serie Optelec ALVA BC6.
- Quan se navega por documentos web, agora puetz presionar n y shift+n ta blincar abance y dezaga pasando bloques de vinclos, respectivament.
- Quan se navega por documentos web, os marcadors d'ARIA agora son anunciaus, y puetz mover-te abance y dezaga a traviés d'ells utilizando d y shift+d, respectivament. (#192)
- O dialogo de lista de vinclos disponible quan s'exploran documentos web s'ha convertiu agora en un dialogo Lista d'Elementos o qual puet listar vinclos, capiters y marcadors. Os capiters y marcadors son presentaus hierarquicament. (#363)
- O nuevo dialogo Lista d'Elementos filtra a lista seguntes escribas ta contener solament aquells elementos incluído o texto que estió tecleado. Puetz presionar retroceso ta limpiar o filtro tal que totz os elementos sigan presentaus nuevament. (#173)
- As versions portatils de NVDA agora buscan en o directorio 'userConfig' dentro d'o directorio de NVDA, as configuracions de l'usuario. Como a versión de l'instalador, isto mantiene a configuración de l'usuario deseparada de NVDA.  
- Os modulos personals d'apps, os controladors de linias braille y os controladors de sintetizadores agora pueden estar almagazenaus en o directorio d'a configuración de l'usuario. (#337)
- Os modos virtuals agora son interpretaus en segundo plano, permitindo a l'usuario interactuar con o sistema dica cierto punto entre o proceso d'interpretau. L'usuario será notificau que o documento ye estando interpretau si le ocupará mas d'un segundo.
- Si NVDA detecta que s'ha penchau por bella razón, Pasará automaticament por todas as pulsacions ta que l'usuario tienga una millor posibilidat de recuperación d'o sistema.
- Suporte t'arrocegar y soltar en ARIA en Mozilla Gecko. (#239)
- A selección de titol de documento y linia actual agora ye verbalizada quan muevas o foco dentro d'un modo virtual. Isto fa que o comportamiento quan se mueve o foco en os modos virtuals siga consistent como en un documento normal. (#210)
- En os modos virtuals, agora puetz interactuar con obchectos empotrados (tals como contenius Adobe Flash y Sun Java) presionando intro sobre l'obchecto. Si ye accesible, puetz alavez tabular por ell como qualsiquier atra aplicación. Ta tornar o foco a o documento, presiona NVDA+espacio. (#431)
- En os modos virtuals, u y shift+u mueven a o siguient y a l'anterior obchecto empotrado, respectivament.


== Cambeos ==
- NVDA ya no anuncia "NVDA activau" quan ranca.
- Os sons de ranque y finalización agora son reproducius utilizando o dispositivo de salida d'audio configurau en NVDA en cuenta d'o dispositivo d'audio predeterminau de Windows. (#164)
- l'anunciau d'as barras de progreso ha estau amillorau. Lo mas notable ye que agora puetz configurar a NVDA t'anunciar-las a traviés de voz y pitidos a o mesmo tiempo.
- Qualques papers chenericos, tals como panel, aplicación y marco, ya no son anunciaus en o foco de no estar que o control no tienga nombre.
- A orden de copia de revisión (NVDA+f10) copia o texto dende dencima de la marca de comienzo y incluye a posición actual de revisión, en cuenta d'excluir a posición actual. Isto permite que o zaguer caracter d'una linia estar copiau, o qual no yera posible anteriorment. (#430)
- O script  navigatorObject_where (ctrl+NVDA+numpad5) ha estau eliminau. Ista combinación de teclas no funcionaba en qualques teclaus, ni o script yera trobau util.
- O script navigatorObject_currentDimentions ha estau remapeado a NVDA+supr d'o teclau numerico. L'antiga combinación de teclas no funcionaba en qualques teclaus. Iste script agora tamién anuncia l'amplaria y l'altura de l'obchecto en cuenta d'as coordenadas dreita/inferior.
- Amillorau o rendimiento (especialment en netbooks) quan ocurren muitos pitidos en succesión rapida; eix.: movimientos rapidos con o rato con as coordenadas d'audio activadas. (#396)


== Corrección de Fallos ==
- Quan NVDA ye executando-se dende una rota de DOS 8.3, pero ye instalau en a rota larga relacionada (eix.: progra1 versus program files) NVDA identificará correctament que ye una copia instalada y carga apropiadament as opcions d'usuario.
- A verbalización d'o titol d'a finestra actual en primer plano con nvda+t funciona agora correctament quan se ye en os menús.
- o braille ya no amuestra información innecesaria en a suya contexto de foco tal como panels no etiquetados.
- se detiene l'anunciau de bella información innecesaria quan o foco cambea tal como panels radiz, panels solapaus y panels deslizables en aplicacions Java u Lotus.
- Se fa que o campo de busca de parolas clau en o visualizador d'Aduya de Windows (CHM) siga muito mas usable. A causa d'a cantidat de fallos en ixe control, a parola clau actual no podría estar leita ya que sería de contino cambiando.
- s'anuncian os numeros correctos de pachina en Microsoft Word si a numeración de pachina ha estau especificament configurada en o documento.
- Millor suporte ta campos d'edición trobaus en dialogos de Microsoft Word (eix.: o dialogo Fuentes). Agora ye posible navegar istos controls con as flechas.
- millor suporte ta consolas d'o Dos. especificament: NVDA agora puet leyer o conteniu de consolas particulars que Siempre se pensó que yeran en blanco. Presionando control+break ya no amortan a NVDA.
- En Windows Vista, l'instalador de NVDA agora ranca a NVDA con privilechios d'un usuario normal quan se requiera ta executar a NVDA en a pantalla final.
- O Retroceso agora ye maniau correctament quan se verbalizan parolas en escribir. (#306)
- No s'anuncia incorrectament "Menú encieto" ta bells menús de contexto en Windows Explorer/Windows shell. (#257)
- NVDA agora manea correctament etiquetas d'ARIA en Mozilla Gecko quan no bi ha unatro conteniu util. (#156)
- NVDA ya no activa incorrectament o modo foco automaticament ta campos de texto editable que actualizan a suya valor quan o foco cambea; eix.: https://tigerdirect.com/. (#220)
- NVDA agora intentará recuperar-se de qualques situacions que anteriorment causarían que secolgase completament. Podrá prener sobre 10 segundos ta que NVDA detecte y se recupere de tals penches.
- Quan l'idioma de NVDA ye achustau a "User default", utiliza l'idioma de l'usuario de Windows configurau en cuenta d'o local de windows.
- NVDA agora reconoixe a existencia de controls en AIM 7.
- A orden de deixar pasar a tecla ya no se queda atascada si una tecla ye mantenida presionada. Anteriorment, NVDA deteneba l'acceptau d'ordens si isto ocurriba y heba d'estar reiniciau. (#413)
- A barra de quefers ya no ye ignorada quan recibe o foco, o que amenudo ocurre quan se sale d'una aplicación. Anteriorment, NVDA se comportaba como si o foco no huviera cambiau.
- Quan se leyen campos de texto en aplicacions que utilizan o Java Access Bridge (incluindo OpenOffice.org), NVDA agora funciona correctament quan l'anunciau de numeros de linia ye activau.
- A orden de copia en revisión (NVDA+f10) manea elegantment o caso an siga utilizau en una posición antis d'o marcador d'inicio. Anteriorment, isto podeba causar problemas tals como penches en Notepad++.
- Bell caracter de control (0x1) ya no causa una extranya conducta en eSpeak (tal como cambeos en o volumen ton) quan se le troba en un texto. (#437)


= 0.6p3 =


== Nuevas Caracteristicas ==
- Como a barra de formulas de Microsoft Excel ye inaccesible ta NVDA, se proporciona un quadro de dialogo especifico de NVDA ta editar quan l'usuario presione f2 sobre una celda. 
- Suporte ta formato en controls de texto de IAccessible2, incluindo aplicacions de Mozilla.
- Letreyar errors puet estar anunciau agora an siga posible. Isto ye configurable dende o dialogo de preferencias Formato de Documentos.
- NVDA puet estar configurau ta pitar ta todas u solament t'as barras de progreso visibles. Alternativament, puet estar configurau ta verbalizar as valors d'as barras de progreso cada 10%.
- Os vinclos pueden agora estar identificaus en controls d'edición multilínea.
- O rato puet agora estar moviu a o caracter baixo o cursor de revisión en a mayoría d'os controls de texto editables. Previament, o rato solament podeba estar moviu a o centro d'o control.
- En os modos virtuals, o cursor de revisión agora revisa o texto d'o modo, antis que solament o texto interno d'o navegador d'obchectos (o qual amenudo no ye util ta l'usuario). Isto significa que puetz navegar o modo virtual hierarquicament utilizando navegación d'obchectos y o cursor de revisión moverá a ixe punto en o modo.
- Maneo de qualques estaus adicionals en controls de Java.
- Si a orden de titol (NVDA+t) ye presionada dos vegadas rapidament, letreya o titol. Si se presionó tres vegadas, ye copiau a o portafuellas.
- La aduya de teclau agora leye os nombres d'as teclas modificaderas quan se presionaron solas.
- Os nombres de tecla anunciaus por la aduya de teclau son agora traducidas.
- Adhibiu suporte t'o texto reconoixiu en campos de SiRecognizer. (#198)
- Suporte ta linias braille!
- Adhibida una orden (NVDA+c) t'anunciar o texto en o portafuellas de Windows. (#193)
- Agora puetz presionar escape quan yes en modo foco ta tornar a modo revisión.
- En os modos virtuals, quan o foco cambea u o cursor ye moviu, NVDA puet cambiar automaticament amodo foco u modo revisión seguntes proceda t'o control baixo o cursor. Isto ye configurau dende o dialogo de Modo virtual. (#157)
- Rescrito o controlador de sintetizador SAPI4 o qual reemplaza a os controladors sapi4serotek y sapi4activeVoice y habría de solucionar os problemas trobaus con istos controladors.
- L'aplicación NVDA agora incluye un manifiesto, o qual significa que no s'executará mas en modo de compatibilidat en Windows Vista.
- O fichero de configuración y os diccionarios d'o fabla son alzaus agora en o directorio de datos de l'usuario si NVDA estió instalau utilizando l'instalador. Isto ye necesario ta Windows Vista y tamién permite a multiples usuarios tener configuracions individuals ta NVDA.
- Adhibiu suporte ta información de posición ta controls IAccessible2.
- Adhibida a capacidat ta copiar texto a o portafuellas utilizando o cursor de revisión. NVDA+f9 achusta la marca d'inicio en a posición actual d'o cursor de revisión. NVDA+f10 recupera o texto entre la marca d'inicio y a posición actual d'o cursor de revisión y lo copia a o portafuellas. (#240)
- Adhibiu suporte ta qualques controls d'edición en o programa pinacle tv.
- Quan s'anuncian texto seleccionau ta seleccions largas (512 caracters u mas), NVDA vervaliza agora o numero de caracters seleccionaus, en cuenta de verbalizar toda a selección. (#249)


== Cambeos ==
- Si o dispositivo de salida d'audio ye achustau ta utilizar o dispositivo predeterminau de Windows (Microsoft Sound Mapper), NVDA cambiará agora a o nuevo dispositivo predeterminau ta eSpeak y tons quan o dispositivo predeterminau cambee. Por eixemplo, NVDA cambiará a un dispositivo d'audio USB si se fa dispositivo predeterminau automaticament quan se connecte.
- S'amillora o rendimiento d'eSpeak con qualques controladors d'audio en Windows Vista.
- Leyer por frase en controls de texto enriquiu si ye posible.
- L'anunciau de vinclos, capiters, listas y citas en documentos ye configurau agora en o dialogo de 	* A velocidat ye agora a opción predeterminada en o grupo d'as opcions de voz d'o sintetizador.
- S'amillora a carga y descarga d'os appModules.
- A orden de titol (NVDA+t) agora solament informa d'o titol en cuenta de tot l'obchecto. Si l'obchecto en primer plano no tien nombre, o nombre de proceso de l'aplicación ye utilizau.
- En cuenta d'activar y desactivar o paso a traviés d'o modo virtual, NVDA agora anuncia modo foco (paso por modo virtual activau) y modo revisión (paso por modo virtual desactivau).
- As voces agora son alzadas en o fichero de configuración por IT en cuenta de por index. Isto fa as opcions de voz mas seguras a traviés d'os cambeos d'os sistemas y as configuracions. A opción de voz no será preservada en todas as configuracions y una error podrá estar amostrau en o log a primera vegada que un sintetizador siga utilizau. (#19)
- O ran d'un elemento de vista d'arbol agora ye anunciau en primeras si ha cambiau dende l'elemento enfocau anteriorment ta todas las vistas en arbol. Anteriorment, isto solament ocurriba para vistas en arbol nativas de Windows (SysTreeView32).


== Corrección de Fallos ==
- O zaguer trozo d'audio no ye tallau ya quan s'utilice NVDA con eSpeak en un servidor d'escritorio remoto.
- Se corrichen problemas con l'alzau de diccionarios de voz ta bellas voces.
- Eliminación de retardo quan se mueva por atras unidatz que no sigan caracter (parola, linia, etc.) ent'o final d'os documentos de texto plano largos en os modos virtuals de Mozilla Gecko. (#155)
- Si verbalizar parolas en escribir ye habilitau, anuncia a parola quan se presione intro.
- Correchius qualques grupos de succesions de caracters en documentos enriquius. preferencias de Formato de Documentos. Isto incluye modos virtuals de Mozilla Gecko.
- O visualizador de log de NVDA agora utiliza quadros multilínea en cuenta de solament editar t'amostrar o log. Isto amillora a lectura por parolas con NVDA y le permite leyer o texto d'o log dillá d'os 65535 bytes.
- Correchius qualques fallos relacionaus con obchectos empotrados en controls d'edición multilínea.
- NVDA agora leye os numeros de pachina en Microsoft Word. (#120)
- Se corriche o fallo quan tabulando a una caixeta de verificación verificada en un modo virtual de Mozilla Gecko y presionando espacio no anunciaba que a caixeta de verificación yera estando desverificada.
- Informa correctament as caixetas de verificación parcialment verificadas en aplicacions Mozilla.
- Si a selección de texto s'expande u se contraye en todas dos direcciónes, leye a selección como un trozo en cuenta de dos.
- Quan se leye con o rato, o texto en os campos d'edición de Mozilla Gecko habría d'estar agora leito.
- Leyer tot no habría de causar que bells sintetizadores SAPI5 se penchen.
- Correchiu un fallo o qual significaba que cambeos en a selección de texto no estasen estando leitos en controls estandars d'edición de Windows antis d'o primer cambeo d'o foco dimpués que NVDA estase encetau.
- Correchiu o seguimiento d'o rato en obchectos Java. (#185)
- NVDA ya no anuncia os elementos d'os arbols Java sin fillos como si estasen contraitos.
- Anuncia l'obchecto con o foco quan una finestra Java ye traita a primer plano. Anteriorment, solament l'obchecto de ran superior Java yera anunciau.
- O controlador d'o sintetizador eSpeak no se detiene ya completament mientras charra dimpués d'una simpla error.
- Se corriche o fallo por meyo d'o qual actualizar parametros de voz (velocidat, ton, etc.) no estió alzau quan a voz estió cambiada dende o grupo d'as opcions de sintetizador.
- Amillorada a verbalización de caracters y parolas escritos.
- Bell texto nuevo que anteriorment no yera verbalizado en aplicacions d'a consola de texto (tals como bell texto de chuegos conversacionals) ye agora verbalizado.
- NVDA agora ignora cambeos d'o foco en finestras en segundo plano. Anteriorment, un cambeo d'o foco en segundo plano podeba estar tractau como si o foco real cambiase.
- Amillorada a detección d'o foco quan s'abandonan os menús de contexto. Anteriorment, NVDA amenudo no reaccionaba d'o tot quan s'abandonaba un menú de contexto.
- NVDA agora anuncia quan o menú de contexto ye activau en o menú d'Inicio.
- O menú d'Inicio clasico agora ye anunciau como Menú d'Inicio en cuenta de Menú Aplicación.
- Amillorada a lectura d'alertas tals como aquellas trobadas en Mozilla Firefox. O texto no habría d'estar leito ya multiples vegadas y unatra información extranya no será ya leita. (#248)
- O texto enfocable, campos d'edición de solament lectura no serán ya incluídos quan se replegue o texto de dialogos. Isto corriche, por eixemplo, a lectura automatica de toda l'acceptación d'a licencia en os instaladores.
- NVDA ya no anuncia a deselección de texto quan s'abandonen qualques controls d'edición (eixemplo: barra d'adreza en Internet Explorer, campos d'adreza en correu electronico en Thunderbird 3 ).
- Quan s'ubran correus en texto plano  en Outlook Express y Windows Mail, o foco ye correctament colocau en o mensache listo ta que l'usuario lo leiga. Anteriorment l'usuario heba de presionar tab u fer clic sobre o mensache tocant a utilizar as teclas d'o cursor ta leyer-lo.
- Correchius quantos problemas mayors con a funcionalidat "Vervalizar Teclas d'Ordens".
- NVDA agora puet leyer texto que pase de 65535 caracters en controls estandar d'edición (eix.: un fichero gran en Notepad).
- Amillorada a lectura de linias en campos d'edición de MSHTML (mensaches editables d'Outlook Express y campos de dentrada de texto en Internet Explorer).
- NVDA ya no se pencha a vegadas completament quan s'edita texto en OpenOffice. (#148, #180)


= 0.6p2 =


- Amillorada a voz predeterminada d'ESpeak en NVDA
- Adhibida una disposición de teclau ta ordinadors portatils. As disposicions de teclau pueden estar configuradas dende o dialogo d'Opcions de teclau de NVDA. (#60)
- Suporte ta grupos d'elementos en controls SysListView32, trobaus prencipalment en Windows Vista. (#27)
- Informar d'o estau verificau d'elementos de vista en arbol en controls SysTreeview32.
- Adhibidas teclas d'alcorce ta muitos d'os dialogos de configuración de NVDA
- Suporte ta IAccessible2 habilitau t'aplicacions tals como Mozilla Firefox quan s'executa a NVDA dende un meyo portatil, sin haber de rechistrar garra fichero Dll en especial
- Correchiu un penche con a lista de vinclos d'o modo virtual en aplicacions Gecko. (#48)
- NVDA no habría de penchar-se ya con aplicacions Mozilla Gecko tals como Firefox y Thunderbird si NVDA ye executando-se con privilechios mas altos que os de l'aplicación Mozilla Gecko. Eix. NVDA ye executando-se como Administrador.
- Diccionarios d'o fabla (anteriorment diccionarios d'usuario) agora pueden estar u sensibles a las mayusclas u insensibles, y os patrones pueden estar opcionalment expresions regulars. (#39)
- Si u no NVDA utiliza un 'modo de disposición de pantalla' t'os documentos d'o modo virtual puet agora estar configurau dende un dialogo d'opcions 
- No s'informa mas sobre ancorache d'etiquetas sin href en documentos Gecko como vinclos. (#47)
- A orden buscar de NVDA agora recuerda qué ye lo zaguer que se buscó, a traviés de todas as aplicacions. (#53)
- Correchius problemas an o estau verificau no yera anunciau en qualques caixetas de verificación y botons d'opción en os modos virtuals 
- O modo de paso a traviés d'o modo virtual ye especifico agora ta cada documento, en cuenta de globalment ta NVDA. (#33)
- Correchius bella lentitut con os cambeos d'o foco y interrupción incorrecta d'a voz que qualques vegadas ocurriba quan s'utiliza NVDA en un sistema que heba estau en sobre aviso u yera mas bien lento
- Amillora o suporte ta quadros combinaus en Mozilla Firefox. Especificament quan se navegando con as flechas por os suyos textos no ye repetiu, y quan blincando difuera d'ells, os controls ancestros no son anunciaus innecesariament. Agora tamién as ordens d'o modo virtual funcionan quan reciben o foco en un quan yes en un modo virtual.
- Amillora a precisión d'a busca d'a barra d'estau en muitas aplicacions. (#8)
- Adhibida a ferramienta d'a consola de python interactiva de NVDA, ta habilitar a os desembolicadors ta mirar y manipular qüestions internas de NVDA seguntes ye executando-se
- Os scripts DecirTodo, AnunciarSelección y anunciarLíneaActual funcionan agora apropiadament quan se ye en o modo pasar a traviés d'o modo virtual. (#52)
- Os scripts incrementar velocidat y decrementar velocidat han estau eliminaus. Os usuarios habrían d'utilizar os scripts d'o grupo d'as opcions de sintetizador (control+nvda+flechas) u o dialogo d'opcions de Voz
- S'amillora o rango y la escala d'os pitidos d'a barra de progreso 
- Adhibidas mas teclas rapidas a o nuevo modo virtual:  l ta lista, i ta elemento de lista, y ta campo d'edición, b ta botón, x ta caixeta de verificación, r ta botón d'opción, g ta grafico, q para citas, c ta quadro combinau, 1 a 6 t'os respectivos rans de capitero, s ta separador, m para marco. (#67, #102, #108)
- A cancelación d'a carga d'un nuevo documento en Mozilla Firefox permite agora a l'usuario siguir utilizando l'antigo documento d'o  modo virtual si o viello documento no ha estau realment destruiu encara. (#63)
- Navegar por parolas en os modos virtuals ye agora mas exacto entre que as parolas no contiengan accidentalment texto de mas d'un campo. (#70)
- Amillorada a exactitut d'o seguimiento d'o foco y l'actualización d'o foco quan se navega en modos virtuals de Mozilla Gecko.
- Adhibiu un script encontrarAnterior (shift+NVDA+f3) ta utilizar en o nuevo modo virtual 
- Amillorada a lentitut en dialogos Mozilla Gecko (en Firefox y Thunderbird). (#66)
- Adhibida a capacidat ta veyer o fichero log actual ta NVDA. Puede estar trobau en o menú NVDA -> Ferramientas
- Scripts tals como decir calendata y hora tienen en cuenta agora l'idioma actual; puntuación y ordinamiento d'as parolas agora reflejan l'idioma
- O quadro combinau d'idioma en o dialogo d'Opcions Chenerals de NVDA amuestra agora os nombres d'idioma completo ta facilidat d'uso
- Quan se revisa texto en o navegador d'obchectos actual, o texto ye siempre actualizau si cambea dinamicament. Eix.: revisando o texto d'un elemento de lista en a Servilla de Quefers. (#15)
- Quan te mueves con o rato, o paragrafo actual de texto baixo o rato agora ye anunciau, en cuenta de tot o texto en ixe obchecto particular u solament a parola actual. Tamién as coordenadas d'audio, y l'anunciau d'os papers de l'obchecto ye opcional, son desactivaus predeterminadament
- Suporte ta lectura de texto con o rato en Microsoft Word
- Correchiu una error an en abandonar a barra de menú en aplicacions tals como Wordpad podría causar que a selección de texto no siga anunciada nunca mas
- En Winamp, o titol  d'a pista no ye ya anunciau la una y l'atra vegada quan se cambea de pistas, u a o pausar/reprener/detener a reproducción.
- En Winamp, adhibida a capacidat d'anunciar o estau d'os controls Aleatorio y repetición seguntes son activaus. Funciona en a finestra prencipal y en l'editor de listas de reproducción
- Amillorada a capacidat t'activar campos particulars en os modos virtuals de Mozilla Gecko. Podrá incluir graficos clicables, vinclos que contiengan paragrafos, y atras estructuras raras
- Correchiu un retardo inicial quan s'ubren dialogos de NVDA en qualques sistemas. (#65)
- Adhibiu suporte especifico ta l'aplicación Total Commander
- Correchiu un fallo en o controlador sapi4serotek an o ton se blocaba en una valor particular, ye decir, se quedaba alto dimpués de leyer una letra en mayuscla. (#89)
- S'anuncia texto cliqueable y atros campos como cliqueables en modos virtuals de Mozilla Gecko. eix.:  a campo que tienga un atributo onclick HTML. (#91)
- Quan nos movemos por modos virtuals de Mozilla Gecko, se desplaza o campo actual ta veyer -- util ta que os pars videntes tiengan una ideya d'án ye l'usuario en o documento (#57)
- S'adhibe suporte basico ta ela aria de rechions activas amuestre eventos en aplicacions habilitadas ta IAccessible2 Util en l'aplicación d'IRC Chatzilla, Os mensaches nuevos serán agora leitos automaticament 
- Qualques milloras chicotas t'aduyar a utilizar aplicacions web con capacidat d'ARIA,  eix.: Google Docs
- Se detiene l'adición de linias en blanco extra a o texto quan se copia dende un modo virtual 
- Se detiene a tecla espacio d'activar un vinclo en a lista de vinclos.  Agora puet estar utilizau como atras letras tocant a encetar o tecleo d'o nombre d'un vinclo en particular a o que deseyes ir
- O script moveMouseToNavigator (NVDA+barra d'o teclau numerico) agora mueve o rato a o centro d'o navegador d'obchectos, en cuenta d'a  cantonada superior cucha 
- Adhibius scripts ta fer clic en os botons cucho y dreito d'o rato (barra y asterisco d'o teclau numerico respectivament)
- Amillorau l'acceso a la Servilla d'o Sistema de Windows. Con esperanza que o foco ya no habría de pareixer quedar-se dezaga en un elemento en particular. Recordatorio: ta ir a la Servilla d'o sistema utiliza a orden de Windows Tecla Windows+b. (#10)
- S'amillora o rendimiento y aturada d'anunciau de texto extra quan se mantiene pretau una tecla de cursor en un campo d'edición y aconsigue o final
- Se detiene a capacidat de NVDA ta fer que l'usuario aguarde mientras mensaches en particular son charraus. Apanya beluns penches con sintetizados de voz en particular. (#117)
- Adhibiu suporte t'o sintetizador de voz Audiologic Tts3, contribución de Gianluca Casalino. (#105)
- Posiblement amillora de rendimiento quan se navega por os documentos en Microsoft Word
- Amillorada precisión quan se leye texto d'avisos en aplicacions de Mozilla Gecko
- Se detienen posibles penches quan se tracta d'alzar a configuración en versions no en anglés de Windows. (#114)
- S'adhibe un dialogo de bienvenida de NVDA. Iste dialogo ye disenyado ta proporcionar información esencial ta nuevos usuarios y permite a o BloqMayus estar configurau como una tecla modificadera de NVDA. Iste dialogo será amostrau quan NVDA siga encetau predeterminadament dica que se deshabilite.
- Correchiu suporte basico ta Adobe Reader tal que ye posible leyer documentos en  versions 8 y 9
- Correchius qualques errors que podrían haber ocurriu quan se mantienen pretadas teclas antis que NVDA siga apropiadament inicializau
- Si l'usuario ha configurau NVDA t'alzar a configuración en salir, s'asegura que a configuración ye apropiadament alzada quan s'amorta u se sale de Windows.
- Adhibiu un son de logo de NVDA a l'inicio de l'instalador, contribuído por Victor Tsaran
- NVDA, tanto en executar-se en l'instalador como d'unatra traza, habría de sacar apropiadament o suyo icono d'a servilla d'o sistema quan salga
- Etiquetas ta controls estandar en dialogos de NVDA (tals como botons Acceptar y cancelar) habrían d'amostrar-se agora en l'idioma en que NVDA ye achustau, en cuenta de solament quedar-se en Inglés.
- L'icono de NVDA habría d'estar agora utilizau por as teclas d'alcorce de NVDA en o menú d'inicio y en o escritorio, en cuenta d'un icono d'aplicación predeterminau.
- Leyer celdas en MS Excel quan te mueves con tab y shift+tab. (#146)
- Correchidas qualques verbalizaciones duplicadas en listas en particular en Skype.
- Amillorau o seguimiento d'o cursor en aplicacions IAccessible2 y Java; eix.: en Open Office y Lotus Symphony, NVDA aguarda adequadament que o cursor se mueva en documentos en cuenta de leyer accidentalment a parola incorrecta u linia en o final de qualques paragrafos. (#119)
- Suporte ta controls AkelEdit trobaus en Akelpad 4.0
- NVDA ya no se bloca en Lotus Synphony quan te mueves dende o documento a la barra de menú.
- NVDA ya no se pencha en os applets de programas Add/Remove en Windows XP quan se lanza un desinstalador. (#30)
- NVDA ya no se pencha quan s'ubre Spybot Search and Destroy
 

= 0.6p1 =

== Acceso a o conteniu d'a web con os nuevos modos virtuals en proceso (dica aquí t'aplicacions Mozilla Gecko incluindo Firefox3 y Thunderbird3) ==
- Os tiempos de carga han estau amilloraus quasi por un factor de trenta (ya no has d'aguardar en toda a mayor parti d'as pachinas web ta cargar-se en o modo virtual)
- Adhibida una lista de vinclos (NVDA+f7)
- Amillorau o dialogo buscar (control+nvda+f) asinas que leva a cabo una busca insensible a las mayusclas, mas apanyo d'uns pocos problemas con o foco con ixe quadro de dialogo.
- Agora ye posible seleccionar y copiar texto en os nuevos modos virtuals 
- De forma predeterminada os nuevos modos virtuals represientan o documento en una disposición de pantalla (vinclos y controls no son en linias separadas de no estar que realment sigan visualment asinas). Puetz commutar ista caracteristica con NVDA+v.
- Ye posible mover-se por paragrafos con control+flecha alto y control+flecha abaixo.
- Amillorau o suporte ta conteniu dinamico
- Amillorau por  dencima toda a precisión d'a lectura de linias y campos quan se puya u se baixa con as flechas. 


== Internacionalización ==
- Agora ye posible teclear caracters accentuaus que  dependen d'un "caracter chusto", mientras NVDA ye executando-se.
- NVDA anuncia agora quan a distribución de teclau ye cambiada (quan se presiona alt+shift).
- A caracteristica d'anunciau de calendata y hora prene agora as opcions rechional y d'idioma actuals d'o sistema.
- Adhibida traducción a o Checo (por Tomas Valusek con aduya de Jaromir Vit)
- adhibida traducción a o vietnamita por Dang Hoai Phuc
- Adhibida ttraducción a l'Africaans (af_ZA), por Willem van der Walt.
- Adhibida traducción a o ruso por Dmitry Kaslin 
- Adhibida traducción a o polaco por DOROTA CZAJKA y amigos.
- Adhibida traducción a o chaponés por Katsutoshi Tsuji.
- Adhibida tradución a o tailandés por Amorn Kiattikhunrat
- Adhibida traducción a o crovata por Mario Percinic y Hrvoje Katic  
- Adhibida traducción a o gallego por Juan C. bunyo 
- Adhibida traducción a l'ucrainés por Aleksey Sadovoy 


== Voz ==
- NVDA viene agora con eSpeak 1.33 empaquetau que contiene muitas milloras, entre as qualas son idiomas amilloraus, variants nombradas, capacidat ta charrar mas rapido.
- O dialogo d'opcions de voz agora te permite cambiar a variant d'un sintetizador si lo suporta. A variant ye normalment una lichera variación d'a voz actual. (eSpeak suporta variants).
- Adhibida a capacidat ta cambiar a inflexión d'una voz en o dialogo d'Opcions de Voz si o sintetizador actual lo suporta. (eSpeak suporta inflexión).
- Adhibida a capacidat ta detener a verbalización d'a información de posición de l'obchecto (eix.:. 1 de 4). Ista opción puet estar trobada en o dialogo d'Opcions de Presentación d'obchectos.
- NVDA puet pitar agora quan verbalice una letra en mayusclas. Isto puet estar activau y desactivau con una caixeta de verificación en o dialogo d'Opcions de Voz. Tamién s'adhibió una caixeta de verificación d'elevación d'o ton ta mayusclas ta configurar si NVDA actualment habría de tener a suya elevación de ton normal t'as mayusclas. Asinas agora puetz tener u ton elevau, decir mayus, u pitar, ta mayusclas.
- Adhibida a capacidat ta pausar a voz en NVDA (como a trobada en Voice Over t'o Mac). Quan NVDA ye verbalizando bella cosa, puetz presionar as teclas control u shift ta silenciar a voz normalment, pero si alavez pretas a tecla shift de nuevo (tanto malas que no haigas presionado qualsiquier atra tecla) a voz continará exactament dende an l'hebanos deixau.
- Adhibiu un controlador de sintetizador virtual o qual quita texto a una finestra en cuenta de verbalizarla a traviés d'un sintetizador de voz. Isto habría d'estar mas agradable t'os desembolicadors videntes que no son usuarios de sintesis de voz pero quieren saber qué ye verbalizando NVDA. Encara bi ha prebablement qualques fallos, asinas que a retroalimentación ye mas bienvenida si culle.
- NVDA ya no verbaliza predeterminadament a puntuación, puetz habilitar a verbalización de puntuación con NVDA+p.
- eSpeak predeterminadament agora charra un poquet mas a bonico, o qual habría de fer-lo mas facil ta chent que van a utilizar eSpeak por primera vegada, quan instalan u prencipian a utilizar NVDA.
- Adhibius diccionarios d'usuario a NVDA. Istos te permiten fer que NVDA verbalice cierto texto de modo diferent. Bi ha tres diccionarios: predeterminau, voz, y temporal. As dentradas que anyadas a o diccionario predeterminau succederán tot o tiempo en NVDA. Os diccionarios por voz son especificos a o sintetizador actual y a voz que actualment tiengas achustada. Y o diccionario temporal ye t'aquellas ocasions que quieras fixar rapidament una regla mientras vas a fer un quefer en particular, pero no quiers que siga permanent (desapareixerá si zarras NVDA). Por agora as reglas son expresions regulars, no solament texto normal.
- Os sintetizadores pueden agora utilizar qualsiquier dispositivo audio de salida en o tuyo sistema, achustando o quadro combinau de dispositivo de salida en o dialogo Sintetizador antis de seleccionar o sintetizador que quieras.


== Rendimiento ==
- NVDA ya no prene una gran cantidat de memoria d'o sistema, quan s'editan mensaches en controls d'edición mshtml
- Amillorau o rendimiento quan se revisa texto dentro de muitos controls que no tienen actualment un cursor real. Eix.: finestra d'historicos de MSN Messenger, elementos de vistas en arbol, elementos de vista de lista etc.
- Amillorau o rendimiento en documentos enriquius.
- NVDA ya no habría d'enlentecerse consumindo grandaria de memoria d'o sistema sin razón
- Correchius fallos quan se mete o foco en una finestra de consola d'o dos mas de tres vegadas u asinas. NVDA teneba una tendencia a penchar-se completament.


== Teclas d'ordens ==
- NVDA+shift+numpad6 y NVDA+shift+numpad4 te permiten navegar a o siguient u anterior obchecto en fluxo respectivament. Isto significa que puetz navegar en una aplicación solament utilizando istas dos teclas sin preocupar-se sobre puyar a o pai, u baixar a o primer fillo seguntes te muevas a traviés d'a hierarquía d'obchectos. Por eixemplo en un navegador web tal como firefox, podrías navegar o documento por obchectos, solament utilizando istas dos teclas. Si o siguient en fluxo u l'anterior en fluxo t'amana y te quita d'un obchecto, u down en un obchecto, mandará pitidos indicando l'adreza.
- Agora puetz configurar opcions de voz sin ubrir o dialogo opcions de voz, utilizando o grupo d'opcions de sintetizador. O grupo d'opcions d'o sintetizador ye un grupo d'opcions de voz que puetz commutar a traviés d'a pulsación de control+NVDA+dreita y control+NVDA+cucha. Ta cambiar una opción utiliza control+NVDA+alto y control+NVDA+abaixo.
- Adhibida una orden t'anunciar a selección actual en campos d'edición (NVDA+shift+flecha alto).
- Un buen numero d'ordens de NVDA que verbalizan texto (tals como anunciar linia actual etc.) agora pueden letreyar o texto si se presionan dos vegadas rapidament.
- O BloqMayus, insert d'o teclau numerico y insert de l'extendiu pueden estar totz utilizaus como a tecla modificadera de NVDA. Tamién si una d'istas teclas ye utilizada, presionándola dos vegadas rapidament sin presionar garra unatra tecla ninviará a tecla a o sistema operativo, como si presionases a tecla sin NVDA executando-se. Ta fer que una d'istas teclas siga a modificadera de NVDA, verifica a suya caixeta de verificación en o dialogo d'Opcions de Teclau (utilizau ta estar clamau o dialogo d'eco de teclau).


== Suporte d'aplicacions ==
- Amillorau o suporte ta documentos de Firefox3 y Thunderbird3. Os tiempos de carga han estau amilloraus quasi por un factor de trenta, una distribución de pantalla ye utilizada predeterminadament (presiona nvda+v t'activar u desactivar ista distribución de pantalla), Una lista de vinclos (nvda+f7 ha estau adhibida), o dialogo buscar (control+nvda+f) ye agora insensible a las mayusclas, muito millor suporte ta conteniu dinamico, a selección y copiau de texto ye agora posible.
- En as finestras d'os historicos d'o MSN Messenger y Windows Live Messenger, agora ye posible seleccionar y copiar texto.
- Amillorau o suporte ta l'aplicación audacity
- Adhibiu suporte ta uns pocos controls edit/text en Skype
- Amillorau o suporte ta l'aplicación Miranda instant messenger 
- Correchius qualques problemas d'o foco quan s'ubren mensaches html y de texto planno en Outlook Express. 
- Os campos de mensaches de noticias d'Outlook express son agora etiquetados correctament
- NVDA agora puet leyer as adrezas en os campos de mensaches d'Outlook Express (para/de/cc etc.)
- NVDA agora habría d'estár mas preciso en anunciar o siguient mensache en out look express quan s'elimina un mensache dende a lista de mensaches.


== APIs y toolkits ==
- Amillorada a navegación d'obchectos por os obchectos de for MSAA. Si una finestra como un menú d'o sistema, barra de titol, u barras de desplazamiento, agora puetz navegar por ellas.
- Adhibiu suporte ta l'API d'accesibilidat IAccessible2. Una parti d'a capacidat t'anunciar mas tipos de controls, isto tamién permite a NVDA accedir a o cursor en aplicacions tals como Firefox 3 y Thunderbird 3, permitindo-te navegar, seleccionar u editar texto.
- Adhibiu suporte ta controls d'edición de Scintilla (tals controls pueden estar trobaus en Notepad++ u Tortoise SVN).
- Adhibiu suporte t'aplicacions Java (a traviés d'o Java Access Bridge). Isto puet proporcionar suporte basico ta Open Office (si Java ye activau), y qualsiquier atra aplicación autonoma Java. Nota que os Applets de java dentro d'un navegador web no podrá funcionar encara.


== Rato ==
- Amillorau o suporte t'a lectura d'o que ye baixo o puntero d'o rato seguntes se mueve. Agora ye muito mas rapido, y agora tamién tien a capacidat en qualques controls tals como campos d'edición estandars, controls Java y IAccessible2, ta leyer a parola actual, no solament l'obchecto actual. Isto podrá estar de bell uso a personas con deficiencia visual que solament quieran leyer un trozo especifico de texto con o rato.
- Adhibida una nueva opción de configuración, trobada en o dialogo Opcions de Rato. Reproducir audio quan o rato se mueve, quan ye verificada, reproduz un pitido de 40 ms cada vegada que o rato se mueve, con o suyo ton (entre 220 y 1760 hz) representando l'eixe y, y o volumen cucha/dreita, representando l'eixe x. Isto capacita a una persona enciega aconseguir una ideya aproximada d'án ye o rato en a pantalla seguntes ye estando moviu. Ista caracteristica tamién depende que reportObjectUnderMouse tamién vaiga a estar activau. Asinas isto significa que si amenestes deshabilitar rapidament tanto o pitado como l'anunciau d'obchectos, alavez solament presiona NVDA+m. Os pitidos tamién son mas altos u mas baixos dependendo de cómo brile a pantalla en ixe punto.


== Presentación d'obchectos y interacción ==
- Amillorau o suporte t'a mayoría d'os controls comuns de vista en arbol. NVDA te diz agora quántos elementos son en a rama quan la expandes. Tamién anuncia o ran quan te mueves en y difuera d'as ramas. Y, anuncia o numero de l'elemento actual y o numero d'elementos, d'alcuerdo con l'actual rama, no l'arbol entero.
- Amillorau qué ye anunciau quan o foco cambea seguntes te mueves por aplicacions u o sistema Operativo. Agora en cuenta de solament escuitar o control en o qual aterrizas, escuitas información interna sobre qualsiquier control sobre o qual iste control siga posicionau. Por eixemplo si tabulas y aterrizas sobre un botón dentro d'un grupo, o grupo tamién será anunciau.
- NVDA agora tracta de verbalizar o mensache interior de muitos quadros de dialogo seguntes amaneixen. Isto ye exacto a mayor parti d'as ocasions, encara que encara bi ha muitos dialogos que no son tant buenos como habrían d'estar.
- Adhibida una caixeta de verificación anunciar descripcions de l'obchecto a o dialogo d'Opcions de presentación d'obchectos. Os usuarios abanzaus podrán en ocasions desverificar isto ta detener l'anunciau de NVDA d'un montón de descripcions extra en controls en particular, tals como en aplicacions Java.
- NVDA anuncia automaticament texto seleccionau en controls d'edición quan o foco se mueve a ells. Si no bi ha garra texto seleccionau, alavez solament anuncia a linia actual como normalment.
- NVDA ye muito mas cudiadoso agora quan reproduz pitidos ta indicar cambeos en as barras de progreso en aplicacions. Ya no se torna loco en aplicacions d'Eclipse tals como Lotus Notes/Symphony, y Accessibility Probe.


== Interface de l'Usuario ==
- Eliminada a finestra d'interface de NVDA, y reemplazada con un simple menú de NVDA desplegable.
- O dialogo opcions d'Interface de NVDA ye agora clamau Opcions Chenerals. Tamién contiene una opción extra: un quadro combinau t'achustar o ran d'o log, ta que os mensaches puedan ir a o fichero de log de NVDA. Nota que o fichero de log de NVDA ye agora clamau nvda.log no debug.log.
- Eliminada a caixeta de verificación Anunciar nombres de grupos d'obchectos d'o dialogo Opcions de presentación d'obchectos, l'anunciau de nombres d'obchectos ye agora maniau diferentment.


= 0.5 =
- NVDA tien agora un sintetizador incorporau llammado eSpeak, desembolicau por Jonathan Duddington. Ye muit achil y lichero, y tien suporte ta muitos idiomas diferents. Os sintetizadores Sapi encara pueden estar utilizaus, pero eSpeak será utilizau predeterminadament. eSpeak no depende de garra software especial ta estar instalau, asinas que puet estar utilizau con NVDA en qualsiquier ordinador, en un lapiz de memoria USB, u qualsiquier unatro. Ta mas información sobre eSpeak, u ta trobar atras versions, veye a https://espeak.sourceforge.net/.
- Corrección d'o fallo an yera anunciau o caracter incorrecto quan se presionaba Suprimir en panels editables d'Internet Explorer / Outlook Express.
- adhibiu suporte ta mas campos d'edición en Skype.
- Os modos virtuals solament se cargan quan o foco ye sobre a finestra que ameneste estar cargada. Isto apanya qualques problemas quan o panel anterior ye activau en Outlook Express.
- Adhibius argumentos de linia d'ordens a NVDA:
 - -m, --minimal: no reproduz os sons d'inicio/salir y no amuestra a interface en rancar si s'achustó a tal coseta.
 - -q, --quit: abandona qualsiquier atra instancia ya en execución de NVDA y dimpués sale
 - -s, --stderr-file nombreFichero: especifica án habría de colocar NVDA as errors y excepcions 
 - -d, --debug-file nombreFichero: especifica án habría de colocar NVDA os mensaches de depuración 
 - -c, --config-file: especifica un fichero de configuración alternativo  
 - -h, -help: amuestra un mensache d'aduya listando os argumentos de linia d'ordens
- Correchiu un fallo an os simbolos de puntuación no habrían d'estar traducius a l'idioma apropiau, quan s'utiliza unatro idioma que l'anglés, y quan verbalizar caracters en escribir estase activau.
- Adhibius fichers de l'idioma Eslovaco gracias a Peter Vagner 
- Adhibiu o dialogo d'Opcions de Modo virtual y un dialogo d'opcions de formato de documento, de Peter Vagner.
- Adhibida traducción a o francés gracias a Michel Such 
- Adhibiu un script t'activar y desactivar o pitido d'as barras de progreso (insert+u). Colaboración de Peter Vagner.
- Se fa que mas mensaches en NVDA sigan traducibles t'atros idiomas. Isto incluye descripcions de script quan se ye en la aduya de teclau.
- Adhibiu un dialogo de busca a os modos virtuals (internet Explorer y Firefox). Presionando control+f quan se ye en una pachina desplega un dialogo en o qual puetz teclear bell texto a trobar. Presionando intro dimpués buscará iste texto y colocará o cursor d'o modo virtual sobre ista linia. Presionando f3 tamién buscarás a siguient ocurrencia d'o texto.
- Quan Verbalizar caracters en escribir ye activau, mas caracters habrían d'estar verbalizados agora. Tecnicament, agora os caracters ascii dende o 32 a o 255 pueden estar verbalizados.
- Renombraus qualques tipos de controls ta una millor legibilidad. Texto editable ye agora edición, outline ye agora arbol y botón pulsable ye agora botón.
- Quan se navega a lo largo d'os elementos d'una lista, u elementos d'arbol en un arbol, o tipo de control (elemento de lista, elemento d'arbol) ya no ye verbalizado, ta una navegación rapida.
- Tiene desplegable (ta indicar que un menú tien un submenú) ye agora verbalizado como submenú.
- Quan qualques idiomas utilizan control y alt (u altGR) ta introducir un caracter especial, NVDA verbalizará agora istos caracters quan Verbalizar caracters en escribir siga activau.
- Apanyaus qualques problemas con a revisión de controls con texto estatico.
- Adhibida traducción a o Chino Tradicional, gracias a Coscell Kao.
- Reestructurado una parti important d'o codigo de NVDA, que habría de correchir agora muitos fallos con a interface d'usuario de NVDA (incluindo opcions de dialogos).
- Adhibiu suporte Sapi4 ta NVDA. Actualment bi ha dos controladors sapi4, un basau en codigo escrito por Serotek Corporation, y unatro utilizando a interface ActiveVoice.ActiveVoice com. Totz dos controladors tienen problemas, mira quál funciona millor ta tu.
- Agora quan se tracta d'executar una nueva copia de NVDA mientras una copia anterior ye encara executando-se causará que a nueva copia salga. Isto apanya un problema mayor quan s'executan multiples copias de NVDA fendo que o tuyo sistema siga muit inusable.
- Renombrau o titol d'a interface d'usuario de NVDA d'Interface de NVDA a NVDA. 
- Correchiu un fallo en Outlook Express quan en pretar Retroceso en l'inicio d'un mensache editable causaba una error.
- Adhibiu un parche de Rui Batista que adhibe un script t'anunciar l'actual estau d'a batería en portatils (insert+shift+b).
- Adhibiu un controlador de sintetizador clamau Silence. Este ye un controlador de sintetizador que no verbaliza brenca, permitindo a NVDA remanir completament silencioso tot o rato. Eventualment isto sería utilizau de conchunta con o suporte Braille, quan lo tiengamos.
- Adhibida opción capitalPitchChange ta sintetizadores gracias a J.J. Meddaugh
- Adhibiu parche de J.J. Meddaugh que fa que o script commutar anunciau d'obchectos baixo o rato siga mas pareixiu a atros scripts commutables (decindo activau/desactivau en cuenta de cambiando o tot o estau).
- Adhibida traducción a o espanyol (ye) colaboración de Juan C. bunyo.
- Adhibiu fichero d'idioma Húmgaro de Tamas Gczy.
- Adhibiu fichero d'idioma portugués de Rui Batista.
- O cambeo de voz en o dialogo Opcions de voz achusta agora os eslizadors de velocidat, ton y volumen a os nuevos d'alcuerdo con o sintetizador, en cuenta de forzar a o sintetizador a estar achustau a las valors anteriors. Isto apanya fallos quan un sintetizador como eloquence u viavoice pareixen charrar a una velocidat muito mas rapida que totz os atros sintetizadores.
- Correchiu un fallo an o sintetizador de voz se deteneba, u NVDA se penchaba completament, quan se yera en una finestra d'a2 consola d'o Dos.
- Si existe suporte ta un idioma en particular, NVDA agora puet amostrar automaticament o suyo interface y verbalizar os suyos mensaches en l'idioma en que Windows siga achustau. Un idioma particular puet encara estar trigau manualment dende o dialogo Opcions d'Interface d'Usuario como tamién.
- Adhibiu un script 'toggleReportDynamicContentChanges' (insert+5). Isto commuta si o texto nuevo, u atros cambeos dinamicos habrían d'estar anunciaus automaticament. Dica aquí isto solament funcionaba en finestras de consola d'o Dos.
- Adhibiu o script 'toggleCaretMovesReviewCursor' (insert+6). Isto commuta si o cusros de revisión habría d'estar reposicionado automaticament quan o cursor d'o sistema se mueve. Isto ye util en Finestras de Consola d'o Dos quan se tracta de leyer información quan a pantalla se ye actualizando.
- Adhibiu o script 'toggleFocusMovesNavigatorObject' (insert+7). Isto commuta si o navegador d'obchectos ye reposicionado sobre l'obchecto con o foco quan cambea.
- Adhibida bella documentación traducida en quantos idiomas. Dica aquí bi ha Francés, Espanyol y Finlandés.
- Eliminada bella documentación de desembolicadors d'a distribución binaria de NVDA, agora solament ye en a versión d'os fuents.
- Correchiu un posible fallo en Windows Live Messanger y MSN Messenger an en navegar alto y abaixo por a lista de contactos causaba errors.
- Nuevos mensaches son agora verbalizados automaticament quan se ye en una conversación utilizando Windows Live Messenger. (solament funciona ta versions en Inglés dica agora)
- A finestra d'historicos en una conversación en Windows Live Messenger agora puet estar leita utilizando as teclas de flechas. (Solament funciona ta versions en Inglés dica o momento) 
- Adhibiu o script 'passNextKeyThrough' (insert+f2). Presiona ista tecla, y alavez a siguient tecla presionada será pasada dreitament a Windows. Isto ye util si has de presionar una tecla en una aplicación pero NVDA utiliza ixa tecla ta bella cosa.
- NVDA ya no se conjela por mas d'un menuto quan s'habren documentos muit grans en MS Word.
- Correchiu un fallo quan se mueve difuera d'una tabla en MS Word, y dimpués se torna a ella, causaba que os numeros de l'actual ringlera/columna no sigan verbalizados si tornas exactament a la mesma celda.
- Quan s'encieta NVDA con un sintetizador que no existe, u no ye funcionando, o sintetizador sapi5 tractará d'estar cargau en o suyo puesto, u si sapi5 no ye funcionando, alavez a voz será achustada a silence.
- Os scripts d'Incrementar y decrementar a velocidat ya no pueden prener a velocidat por alto de 100 u por baixo de 0.
- Si bi ha una error con un idioma quan se trigue en o dialogo Opcions d'Interface d'Usuario, un quadro de mensache alertará a l'usuario d'o feito.
- NVDA agora pregunta si habría d'alzar a configuración y reiniciar si l'usuario ha cambiau l'idioma en o dialogo Opcions d'Interface d'Usuario. NVDA debe estar reiniciau ta que o cambeo d'idioma tienga un efecto completo.
- Si un sintetizador no puet estar cargau, quan le lo selecciona dende o dialogo Sintetizadores, Un quadro de mensache alerta a l'usuario d'o feito.
- Quan se carga un sintetizador por primera vegada, NVDA permite a o sintetizador trigar a voz mas convenient, os parametros de velocidat y ton, en cuenta de forzar-lo a deixar-lo como piense que ye bien. Isto corriche un problema an os sintetizadores sapi4 Eloquence y Viavoice prencipian a charrar d'un modo pro rapido ta una primera vegada.


