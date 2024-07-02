# Novidades do  NVDA
## Traduzido pela Equipa portuguesa do NVDA


## 2024.2

Há uma nova funcionalidade chamada divisão de som.
O que permite dividir os sons do NVDA num canal (por exemplo, esquerdo), enquanto os sons de todas as outras aplicações são colocados no outro canal (por exemplo, direito).

Há novos comandos para modificar o anel de definições do sintetizador, permitindo aos utilizadores saltar para a primeira ou última definição e aumentar ou diminuir a definição atual num passo maior.
Existem também novos comandos de navegação rápida, que permitem aos utilizadores associar gestos para saltar rapidamente entre: parágrafo, parágrafo alinhado verticalmente, texto do mesmo estilo, texto de estilo diferente, item de menu, botão de alternância, barra de progresso, figura e fórmula matemática.

Foram adicionadas muitas novas funcionalidades braille e correcções de erros.
Foi adicionado um novo modo braille denominado "Apresentar saída de voz".
Quando activo, o dispositivo braille mostra exatamente o que o NVDA anuncia.
Foi também adicionado suporte para os dispositivos Braille BrailleEdgeS2, BrailleEdgeS3.
LibLouis foi actualizada, adicionando novas tabelas Braille bielorrussas e ucranianas detalhadas (com indicação de letras maiúsculas), tabela para Laos e uma tabela espanhola para leitura de textos gregos.

O eSpeak foi atualizado, adicionando o novo idioma Tigrinya.

Existem muitas correcções de erros menores para aplicações, tais como o Thunderbird, Adobe Reader, navegadores Web, Nudi e Geekbench.

### Novas funcionalidades

* Novos comandos de teclas:
  * Novo comando de navegação rápida `p` para saltar para o próximo/anterior parágrafo de texto no modo de navegação. (#15998, @mltony)
  * Novos comandos de Navegação Rápida não atribuídos, que podem ser utilizados para saltar para o seguinte e anterior:
    * figura (#10826)
    * parágrafo alinhado verticalmente (#15999, @mltony)
    * item de menu (#16001, @mltony)
    * botão de alternância (#16001, @mltony)
    * barra de progresso (#16001, @mltony)
    * fórmula matemática (#16001, @mltony)
    * texto com o mesmo estilo (#16000, @mltony)
    * texto de estilo diferente (#16000, @mltony)
  * Adicionados comandos para saltar para primeiro, último, a frente e para trás no anel de definições do sintetizador. (#13768, #16095, @rmcpantoja)
  * Definir a primeira e a última definição no anel de definições de sintetizador não tem nenhum gesto atribuído. (#13768)
  * Diminuir e aumentar a definição atual do anel de definições de sintetizador num passo maior (#13768):
    * Desktop: `NVDA+control+pageUp` ou `NVDA+control+pageDown`.
    * Laptop: `NVDA+controlo+shift+pageUp` ou `NVDA+controlo+shift+pageDown`.
  * Adicionado um novo gesto de entrada não atribuído para alternar o anúncio de figuras e legendas. (#10826, #14349)
* Braille:
  * Adicionado suporte para os dispositivos Braille BrailleEdgeS2 e BrailleEdgeS3. (#16033, #16279, @EdKweon)
  * Foi adicionado um novo modo Braille chamado "Apresentar saída de voz". (#15898, @Emil-18)
    * Quando activo, o dispositivo Braille mostra exatamente o que o NVDA fala.
    * Pode ser alternado pressionando `NVDA+alt+t`, ou a partir do diálogo de configurações braille.
* Divisão de som: (#12985, @mltony)
  * Permite dividir os sons do NVDA em um canal (por exemplo, esquerdo) enquanto os sons de todos os outros aplicativos são colocados no outro canal (por exemplo, direito).
  * Pode ser alternado por `NVDA+alt+s`.
* O anúncio de cabeçalhos de linhas e colunas é agora suportado em elementos HTML com conteúdo. (#14113)
* Adicionada a opção para desactivar o anúncio de figuras e legendas nas definições de formatação do documento. (#10826, #14349)
* No Windows 11, o NVDA anunciará alertas de digitação por voz e acções sugeridas, incluindo a sugestão principal ao copiar dados como números de telefone para a área de transferência (Windows 11 2022 Update e posterior). (#16009, @josephsl)
* O NVDA manterá o dispositivo de áudio aberto depois de a fala parar, para evitar que o início da fala seguinte seja cortado, em alguns dispositivos de áudio, como auscultadores Bluetooth. (#14386, @jcsteh, @mltony)
* O HP Secure Browser é agora suportado. (#16377)

### Alterações

* Loja de extras:
  * A versão mínima e a última versão testada do NVDA para um extra são agora apresentadas na área "outros detalhes". (#15776, @Nael-Sayegh)
  * A ação de revisões da comunidade estará disponível em todos os separadores da loja. (#16179, @nvdaes)
* Actualizações de componentes:
  * Actualização do conversor LibLouis Braille para [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0). (#16259, @codeofdusk)
    * Adicionadas novas tabelas detalhadas (com letras maiúsculas indicadas) de Braille bielorrusso e ucraniano;
    * Nova tabela espanhola para ler textos gregos.
    * Nova tabela para Lao Grau 1. (#16470)
  * O eSpeak NG foi atualizado para a versão 1.52-dev commit `cb62d93fd7`. (#15913)
    * Adicionado novo idioma Tigrinya. 
* Alterados vários comandos para dispositivos BrailleSense para evitar conflitos com caracteres da tabela Braille francesa. (#15306)
  * `alt+seta esquerda` agora é mapeado para `dot2+dot7+espaço`
  * `alt+seta direita` agora é mapeada para `dot5+dot7+espaço`
  * `alt+seta acima` agora é mapeado para `dot2+dot3+dot7+espaço`
  * `alt+seta abaixo` agora está mapeado para `dot5+dot6+dot7+espaço`
* Os pontos de preenchimento normalmente usados em tabelas de conteúdo não são mais reportados em níveis baixos de pontuação. (#15845, @CyrilleB79)

### Correcções de erros

* Correcções para Windows 11:
  * O NVDA volta a anunciar sugestões de entrada de teclado de hardware. (#16283, @josephsl)
  * Na Versão 24H2 (Atualização 2024 e Windows Server 2025), a interação do rato e do toque pode ser utilizada nas definições rápidas. (#16348, @josephsl)
* Loja de extras:
  * Ao pressionar `ctrl+tab`, o foco move-se correctamente para o novo título do separador atual. (#14986, @ABuffEr)
  * Se os ficheiros de cache não estiverem correctos o NVDA já não é reiniciado. (#16362, @nvdaes)
* Correcções para navegadores baseados em Chromium quando usados com UIA:
  * Corrigidos bugs que faziam o NVDA travar. (#16393, #16394)
  * A tecla Backspace está agora a funcionar corretamente nos campos de início de sessão do Gmail. (#16395)
* A tecla Backspace funciona agora corretamente quando se utiliza o Nudi 6.1 com a definição "Tratar teclas enviadas por outras aplicações" do NVDA activada. (#15822, @jcsteh)
* Corrigido um erro em que as coordenadas de áudio eram reproduzidas enquanto a aplicação estava em modo de suspensão quando a opção "Reproduzir coordenadas de áudio quando o rato se mover" estava activada. (#8059, @hwf1324)
* No Adobe Reader, o NVDA já não ignora o texto alternativo definido nas fórmulas em PDFs. (#12715)
* Corrigido um erro que fazia com que o NVDA não conseguisse ler o friso e as opções no Geekbench. (#16251, @mzanm)
* Corrigido um caso raro em que guardar a configuração podia falhar ao guardar todos os perfis. (#16343, @CyrilleB79)
* Nos navegadores baseados no Firefox e no Chromium, o NVDA entrará corretamente no modo de foco ao premir enter quando posicionado numa lista de apresentação (ul /ol) dentro de conteúdo editável. (#16325)
* A alteração do estado da coluna é automaticamente reportada ao selecionar colunas para apresentar na lista de mensagens do Thunderbird.(#16323)
* A opção de linha de comando `-h`/`--help` volta a funcionar. (#16522, @XLTechie)
* O suporte do NVDA para o software  de tradução Poedit, versão 3.4 ou superior, volta a funcionar correctamente ao traduzir idiomas com uma ou mais de duas formas plurais (por exemplo, Chinês e Polaco). (#16318)

### Alterações para programadores

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Added a how-to document, explaining the process of building NVDA forks on AppVeyor. (#16293, @XLTechie)

## 2024.1

Foi adicionado um novo modo de voz "a pedido".
Quando o modo de voz está configurado para "a pedido", o NVDA não fala automaticamente (por exemplo, ao mover o cursor) mas ainda fala ao chamar comandos cujo objetivo é explicitamente anunciar algo (por exemplo, anunciar o título da janela).
Na categoria Voz das configurações do NVDA, passa a ser possível excluir modos de voz não desejados do comando Alternar modos de voz (`NVDA+s`).

Um novo modo de Seleção Nativa (ativado por `NVDA+shift+f10`) está agora disponível no modo de navegação do NVDA para o Mozilla Firefox.
Quando ativado, selecionar texto no modo de navegação também manipulará a seleção nativa do Firefox.
Copiar texto com `control+c` passará diretamente para o Firefox, copiando o conteúdo HTML, em vez da representação em texto simples do NVDA.

A Loja de extras passa a suportar ações em massa (por exemplo, instalar ou activar extras) seleccionando múltiplos extras.
Há uma nova acção para abrir uma página de avaliações para o extra seleccionado.

As opções de dispositivo de saída de áudio e modo de redução de volume foram removidas do diálogo "Seleccionar Sintetizador".
Passam a ser encontradas no painel de configurações de áudio que pode ser aberto com `NVDA+control+u`.

eSpeak-NG, conversor Braille LibLouis e Unicode CLDR foram actualizados.
Disponíveis novas tabelas Braille para Tailandês, Filipino e Romeno.

Muitas correcções de erros, particularmente para a Loja de extras, Braille, Libre Office, Microsoft Office e áudio.

### Notas Importantes

* Esta versão quebra a compatibilidade com add-ons existentes.
* Windows 7 e Windows 8 já não são suportados.
Windows 8.1 é a versão mínima do Windows suportada.

### Novas Funcionalidades

* Loja de Extras:
  * A Loja de Extras agora suporta ações em massa (por exemplo, instalar ou activar extras) seleccionando múltiplos extras. (#15350, #15623, @CyrilleB79)
  * Uma nova acção foi adicionada para abrir uma página dedicada para ver ou fornecer informações sobre o extra seleccionado. (#15576, @nvdaes)
* Suporte adicionado para dispositivos Braille Bluetooth Low Energy HID. (#15470)
* Um novo modo de Selecção Nativa (activado por `NVDA+shift+f10`) está agora disponível no modo de navegação do NVDA para o Mozilla Firefox.
Quando activado, seleccionar texto no modo de navegação também manipula a selecção nativa do Firefox.
Copiar texto com `control+c` passa directamente para o Firefox, copiando o conteúdo HTML, em vez da representação em texto simples do NVDA. (#15830)
Note que como é o Firefox a controlar a função de copiar, o NVDA não anuncia a mensagem de cópia neste modo. (#15830)
* Ao copiar texto no Microsoft Word com o modo de navegação do NVDA activado, a formatação passa a ser incluída. (#16129)
Um efeito colateral disto é que o NVDA deixa de anunciar a mensagem de cópia ao ser pressionado `control+c` no Microsoft Word / Outlook em modo de navegação, por ser a aplicação que controla a função de cópia e não o NVDA. (#16129)
* Um novo modo de voz, "a pedido", foi adicionado.
Quando a voz está configurada para "a pedido" o NVDA não fala automaticamente (por exemplo, ao mover o cursor) mas ainda fala ao activar comandos cujo objectivo é explicitamente anunciar algo (por exemplo, anunciar o título da janela). (#481, @CyrilleB79)
* Na categoria Voz das configurações do NVDA, agora é possível excluir modos de voz não desejados do comando "Alternar modos de voz" (`NVDA+s`). (#15806, @lukaszgo1)
  * Se está actualmente a usar o extra "Modos de voz", considere desinstalá-lo e desactivar os modos "bips" e "a pedido" nas configurações.

### Alterações

* O NVDA deixa de suportar o Windows 7 e o Windows 8.
Windows 8.1 passa a ser a versão mínima do Windows suportada. (#15544)
* Actualização de Componentes:
  * Actualizado o conversor Braille LibLouis para [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0). (#15435, #15876, @codeofdusk)
    * Adicionadas tabelas Braille para Tailandês, Romeno e Filipino.
  * eSpeak NG actualizado para 1.52-dev commit `530bf0abf`. (#15036)
  * Anotações de emoji e símbolos CLDR foram actualizadas para a versão 44.0. (#15712, @OzancanKaratas)
  * Actualizado o Java Access Bridge para 17.0.9+8Zulu (17.46.19). (#15744)
* Comandos de Teclado:
  * Os seguintes comandos passam a suportar duas e três pressões para soletrar a informação anunciada e soletrar com descrição de caracteres: "Anunciar selecção actual", "Anunciar o texto da área de transferência" e "Anunciar o objecto em foco". (#15449, @CyrilleB79)
  * O comando para alternar a cortina de ecrã passa a ser um comando predefinido: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * Quando pressionado quatro vezes, o comando "Anunciar selecção actual" passa a mostrar a informação numa mensagem navegável. (#15858, @Emil-18)
* Microsoft Office:
  * Ao solicitar informações de formatação em células do Excel, bordas e fundo só serão anunciados se houver tal formatação. (#15560, @CyrilleB79)
  * O NVDA volta a não anunciar agrupamentos não etiquetados, como em versões recentes dos menus do Microsoft Office 365. (#15638)
* As opções de dispositivo de saída de áudio e modo de redução de volume foram removidas do diálogo "Seleccionar Sintetizador".
Agora podem ser encontradas no painel de configurações de áudio que pode ser aberto com `NVDA+control+u`. (#15512, @codeofdusk)
* A opção "Anunciar o tipo de controlo quando o rato entrar no objecto" na categoria de configurações do rato do NVDA foi renomeada para "Anunciar objecto quando o rato entra nele".
Esta opção passa a anunciar informações adicionais relevantes sobre o objecto quando o rato entra nele, como estados (marcado/pressionado) ou coordenadas de célula numa tabela. (#15420, @LeonarddeR)
* Novos itens foram adicionados ao menu Ajuda para acesso à página "Ajuda, formação e apoio" e "Loja da NV Access". (#14631)
* O suporte do NVDA para [Poedit](https://poedit.net) foi revisado para a versão 3 e superior.
Os utilizadores do Poedit 1 são incentivados a atualizar para o Poedit 3 se quiserem contar com acessibilidade melhorada no Poedit, como atalhos para ler notas e comentários do tradutor. (#15313, #7303, @LeonarddeR)
* O visualizador de Braille e o visualizador de discurso agora estão desabilitados no modo seguro. (#15680)
* Durante a navegação por objectos, objectos desabilitados (indisponíveis) já não são ignorados. (#15477, @CyrilleB79)
* Adicionado índice ao documento Referência rápida de comandos. (#16106)

### Correcções de erros

* Loja de extras:
  * Quando o estado de um extra é alterado enquanto ele está em foco, por exemplo, uma mudança de "descarregando" para "descarregado", o item atualizado agora é anunciado correctamente. (#15859, @LeonarddeR)
  * Ao instalar extras, os diálogos de instalação já não são sobrepostos pela caixa de diálogo de reinício. (#15613, @lukaszgo1)
  * Ao reinstalar um extra incompatível, ele já não é desactivado automaticamente. (#15584, @lukaszgo1)
  * Os extras desactivados e incompatíveis já podem ser atualizados. (#15568, #15029)
  * O NVDA agora recupera e exibe um erro no caso de um extra não for descarregado correctamente. (#15796)
  * O NVDA já não falha intermitentemente ao reiniciar após abrir e fechar a Loja de extras. (#16019, @lukaszgo1)
* Áudio:
  * O NVDA não congela mais brevemente quando múltiplos sons são reproduzidos em rápida sucessão. (#15311, #15757, @jcsteh)
  * Se o dispositivo de saída de áudio estiver configurado para algo diferente do padrão e esse dispositivo ficar disponível novamente após estar indisponível, o NVDA agora voltará para o dispositivo configurado em vez de continuar usando o dispositivo padrão. (#15759, @jcsteh)
  * O NVDA agora retoma o áudio se a configuração do dispositivo de saída mudar ou outro aplicativo liberar o controle exclusivo do dispositivo. (#15758, #15775, @jcsteh)
* Braille:
  * Dispositivos Braille de várias linhas não causarão mais o crash do driver BRLTTY e são tratados como uma linha contínuo. (#15386)
  * Mais objectos que contêm texto útil são detectados, e o conteúdo de texto é exibido em Braille. (#15605)
  * A introdução de texto em braille contraído volta a funcionar correctamente. (#15773, @aaclause)
  * O Braille agora é actualizado ao mover o objeto de navegação entre células de tabela em mais situações (#15755, @Emil-18)
  * O resultado dos comandos de anunciar foco atual, objeto navegador atual e comandos de seleção atual agora é mostrado em Braille. (#15844, @Emil-18)
  * O driver do dispositivo Braille Albatross não trata mais um microcontrolador Esp32 como um display Albatross. (#15671)
* LibreOffice:
  * Palavras apagadas usando o comando `control+backspace` agora também são anunciadas correctamente quando a palavra deletada é seguida por espaço em branco (como espaços e tabs). (#15436, @michaelweghorn)
  * O anúncio da barra de status usando o comando `NVDA+end` agora também funciona para diálogos na versão 24.2 e mais recente do LibreOffice. (#15591, @michaelweghorn)
  * Todos os atributos de texto esperados agora são suportados nas versões 24.2 e acima do LibreOffice.
  Isto faz com que o anúncio de erros de ortografia funcione ao anunciar uma linha no Writer. (#15648, @michaelweghorn)
  * O anúncio de níveis de cabeçalho agora também funciona para as versões 24.2 e mais recente do LibreOffice. (#15881, @michaelweghorn)
* Microsoft Office:
  * No Excel com UIA desactivado, o braille é atualizado, e o conteúdo da célula ativa é falado, quando `control+y`, `control+z` ou `alt+backspace` são pressionados. (#15547)
  * No Word com UIA desactivado o Braille é actualizado quando `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace` ou `control+backspace` são pressionados.
  Também é actualizado com UIA activado, ao digitar texto e o Braille está ligado à revisão e a revisão segue o cursor. (#3276)
  * No Word, a célula de destino agora será correctamente anunciada ao usar os comandos nativos do Word para navegação em tabelas `alt+home`, `alt+end`, `alt+pageUp` e `alt+pageDown`. (#15805, @CyrilleB79)
* O anúncio de teclas de atalho de objectos foi melhorado. (#10807, #15816, @CyrilleB79)
* O sintetizador SAPI4 agora suporta correctamente mudanças de volume, velocidade e tom embutidas na fala. (#15271, @LeonarddeR)
* O estado de múltiplas linhas agora é correctamente anunciado em aplicações que usam Java Access Bridge. (#14609)
* O NVDA anunciará o conteúdo de diálogos para mais diálogos do Windows 10 e 11. (#15729, @josephsl)
* O NVDA não falhará mais ao ler uma página recém-carregada no Microsoft Edge quando usa UI Automation. (#15736)
* Ao usar Ler tudo, ou comandos que soletram texto, pausas entre frases ou caracteres já não diminuem gradualmente com o tempo. (#15739, @jcsteh)
* O NVDA já não congela às vezes ao falar uma grande quantidade de texto. (#15752, @jcsteh)
* Ao acessar o Microsoft Edge usando UI Automation, o NVDA é capaz de ativar mais controles no modo de navegação. (#14612)
* O NVDA não falhará mais em iniciar quando o arquivo de configuração estiver corrompido, mas restaurará a configuração para o padrão como fazia no passado. (#15690, @CyrilleB79)
* Suporte corrigido para controles System List view (`SysListView32`) em aplicações Windows Forms. (#15283, @LeonarddeR)
* Já não é possível sobrescrever o histórico do console Python do NVDA. (#15792, @CyrilleB79)
* O NVDA deve permanecer responsivo ao ser inundado com muitos eventos de UI Automation, por exemplo, quando grandes pedaços de texto são mostrados  em um terminal ou ao ouvir mensagens de voz no WhatsApp. (#14888, #15169)
  * Esse novo comportamento pode ser desactivado usando a nova configuração "Utilizar o processamento de eventos melhorado" nas configurações avançadas do NVDA.
* O NVDA é novamente capaz de rastrear o foco em aplicações executadas dentro do Windows Defender Application Guard (WDAG). (#15164)
* O texto de fala não é mais atualizado quando o rato se move no Visualizador de discurso. (#15952, @hwf1324)
* O NVDA voltará novamente ao modo de navegação ao fechar caixas de combinação com `escape` ou `alt+upArrow` no Firefox ou Chrome. (#15653)
* Mover para cima e para baixo em caixas de combinação no iTunes não mudará mais inapropriadamente de volta para o modo de navegação. (#15653)

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
  * wxPython to 4.2.1. (#12551)
* Removed pip dependencies:
  * typing_extensions, these should be supported natively in Python 3.11 (#15544)
  * note, instead unittest-xml-reporting is used to generate XML reports. (#15544)
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

Esta é uma versão de correção para resolver uma questão de segurança e outra questão na instalação.
Por favor, divulgue questões de segurança de forma responsável seguindo a [política de segurança do NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Security Fixes

### Correções de Segurança

* Previne o carregamento de configurações específicas quando o modeo seguro é imposto.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### Correcções de erros

* Corrigido o erro que causava que o processo do NVDA não terminasse correctamente. (#16123)
* Corrigido o erro em que se o processo do NVDA não terminasse correctamente, a instalação do NVDA podia falhar e ficar num estado não recuperável. (#16122)

## 2023.3.3

Esta é uma versão de correção para resolver uma questão de segurança.
Por favor, divulgue questões de segurança de forma responsável seguindo a [política de segurança do NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Correções de Segurança

* Previne possível ataque XSS refletido de conteúdo criado para causar execução arbitrária de código.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

Esta é uma versão de correção para resolver uma questão de segurança.
A correção de segurança em 2023.3.1 não foi resolvida corretamente.
Por favor, divulgue questões de segurança de forma responsável seguindo a [política de segurança do NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

### Correções de Segurança

* A correção de segurança em 2023.3.1 não foi resolvida corretamente.
Previne possível acesso ao sistema e execução arbitrária de código com privilégios de sistema para usuários não autenticados.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

= 2023.3.1 =
Esta é uma versão de correção para resolver uma questão de segurança.
Por favor, divulgue questões de segurança de forma responsável seguindo a [política de segurança do NVDA](https://github.com/nvaccess/nvda/blob/master/security.md).

== Correções de Segurança ==
* Previne possível acesso ao sistema e execução arbitrária de código com privilégios de sistema para usuários não autenticados.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

Esta versão inclui melhorias no desempenho, responsividade e estabilidade da saída de áudio.
Foram adicionadas opções para controlar o volume dos sons e bips do NVDA, ou para os fazer seguir o volume da voz que está a utilizar.

O NVDA pode agora actualizar periodicamente os resultados de OCR, anunciando o novo texto à medida que aparece.
Isto pode ser configurado na categoria OCR do Windows nas configurações do NVDA.

Houve várias correcções no Braille, melhorando a detecção de dispositivos e o movimento do cursor.
É agora possível optar por não incluir drivers não desejados na detecção automática, para melhorar o desempenho da autodetecção.
Também existem novos comandos para o BRLTTY.

Também foram corrigidos erros na Loja de Extras, Microsoft Office, menus de contexto do Microsoft Edge e Calculadora do Windows.

### Novas Funcionalidades

* Gestão de som melhorada:
  * Uma nova secção, Áudio nas configurações  do NVDA:
    * Pode ser aberta com `NVDA+control+u`. (#15497)
    * Uma opção nas configurações de áudio para que o volume dos sons e bips do NVDA siga a definição de volume da voz que está a utilizar. (#1409)
    * Uma opção nas configurações de áudio para configurar separadamente o volume dos sons do NVDA. (#1409, #15038)
    * As opções para alterar o dispositivo de saída de áudio e alternar a redução de áudio foram movidas para a nova secção Configurações de áudio a partir da caixa de diálogo Selecionar sintetizador.
    Estas opções serão removidas da caixa de diálogo "selecionar sintetizador" em 2024.1. (#15486, #8711)
  * O NVDA agora emitirá a voz e os sons  através da API de Sessão de Áudio do Windows (WASAPI), o que pode melhorar a responsividade, desempenho e estabilidade da voz e sons do NVDA. (#14697, #11169, #11615, #5096, #10185, #11061)
  -  Nota: WASAPI é incompatível com alguns extras.
  Actualizações compatíveis estão disponíveis para esses extras, actualize-os antes de actualizar o NVDA.
  Versões incompatíveis destes extras serão desactivadas ao actualizar o NVDA:
    * Tony's Enhancements versão 1.15 ou anterior. (#15402)
    * NVDA global commands extension 12.0.8 ou anterior. (#15443)
* O NVDA agora pode actualizar continuamente o resultado ao realizar reconhecimento ótico de caracteres (OCR), anunciando o novo texto à medida que aparece. (#2797)
  * Para activar esta funcionalidade, marque a opção "Actualizar periodicamente os conteúdos reconhecidos" na secção OCR do Windows das configurações do NVDA.
  * Quando activada, pode alternar entre anunciar ou não, alternando o anúncio de alterações em conteúdos dinâmicos, pressionando "NVDA+5").
* Ao usar a detecção automática de dispositivos Braille, é agora possível optar por não incluir drivers na detecção.
* Uma nova opção nas configurações de Formatação de Documento, "Ignorar linhas em branco para anúncio de indentação de linha". (#13394)
* Adicionado um comando sem tteclas associadas para navegar por grupos de separadores em modo de navegação. (#15046)

### Alterações

* Braille:
  * Quando o texto numa janela de terminal muda sem actualizar o cursor, o texto num dispositivo Braille passa a ser actualizado correctamente se estiver na linha que foi alterada.
  Isto inclui as situações em que o Braille está ligado ao cursor de revisão. (#15115)
  * Mais teclas de atalho BRLTTY estão agora mapeadas para comandos NVDA. (#6483):
    * `learn`: Activa ou desactiva a Ajuda de comandos
    * `prefmenu`: Abre o menu do NVDA
    * `prefload`/`prefsave`: Carrega/guarda a configuração do NVDA 
    * `time`: Diz a hora actual
    * `say_line`: Lê a linha actual onde está colocado o cursor de revisão
    * `say_below`: Lê tudo a partir do cursor de revisão

>  - O driver BRLTTY só está disponível quando o BRLTTY está em execução. (#15335)

  * A opção para activar o suporte para HID braille foi removido das configurações avançadas sendo substituído por uma nova opção.
  Agora pode desactivar a detecção automática de dispositivos Braille na janela "Seleccionar linha Braille". (#15196)

* Loja de Extras: Os extras instalados passam a ser também listados no separador Extras Disponíveis, se estiverem disponíveis na loja. (#15374)
* Algumas teclas de atalho do menu do NVDA foram actualizadas. (#15364)

### Correções de Erros

* Microsoft Office:
  * Correção de falha no Microsoft Word quando as opções de Formatação de Documento "Anunciar cabeçalhos" e "Anunciar comentários e notas" estavam desativadas. (#15019)
  * No Word e Excel, o alinhamento do texto já é correctamente anunciado em mais situações. (#15206, #15220)
  * Corrigido o anúncio de alguns atalhos de formatação de células no Excel. (#15527)
* Microsoft Edge:
  * O NVDA já não volta à última posição do modo de navegação ao abrir o menu de contexto no Microsoft Edge. (#15309)
  * O NVDA volta a ler os menus de contexto do gestor de downloads do Microsoft Edge. (#14916)
* Braille:
  * O cursor Braille e os indicadores  de selecção serão sempre actualizados correctamente após mostrar ou ocultar os respectivos indicadores com um comando. (#15115)
  * Corrigido o erro das linhas Braille Albatross tentarem inicializar apesar de outro dispositivo Braille estar ligado. (#15226)
* Loja de extras:
  * Corrigido um erro que ao desmarcar a opção "Incluir extras incompatíveis" resultava em os extras incompatíveis ainda serem mostrados. (#15411)
  * Os extras bloqueados por razões de compatibilidade já devem ser filtrados correctamente quando se alterna o filtro para o estado activados/desactivados. (#15416)
  * Corrigido o erro que impedia extras incompatíveis instalados e activados de serem actualizados ou substtituídos utilizando a funcionalidade de instalar de fonte externa. (#15417)
  * Corrigido o erro que impedia o NVDA de falar até ser reiniciado após a instalação de extras. (#14525)
  * Corrigido o erro em que os add-ons não podiam ser instalados se uma transferência anterior falhasse ou fosse cancelada. (#15469)
  * Corrigidos problemas com o tratamento de complementos incompatíveis ao atualizar o NVDA. (#15414, #15412, #15437)
* O NVDA volta a anunciar os resultados na Calculadora do Windows 32bit nas versões do Windows Server, LTSC ed LTSB. (#15230)
* O NVDA já não ignora as alterações de foco quando uma janela aninhada (janela neta) obtém o foco. (#15432)
* corrigida uma causa provável do cras do NVDA durante o seu início. (#15517)

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

Esta versão introduz a Loja de Extras para substituir o Gestor de Extras.
Na Loja de Extras, pode navegar, pesquisar, instalar e atualizar extras da comunidade.
Agora pode, manualmente, ultrapassar os problemas de incompatibilidade com extras desactualizados por sua própria conta e risco.
Existem novas funcionalidades, comandos e suporte para mais dispositivos Braille.
Também há novos comandos para OCR e navegação usando a revisão plana por objectos.
A navegação e o anúncio de formatação no Microsoft Office foram melhorados.
Há muitas correções de erros, particularmente para braille, Microsoft Office, navegadores web e Windows 11.
O eSpeak-NG, o conversor de braille LibLouis e o Unicode CLDR foram atualizados.

### Novas funcionalidades

* Adicionada a Loja de extras ao NVDA. (#13985)
  * Navegue, pesquise, instale e atualize extras da comunidade.
  * Ignore manualmente problemas de incompatibilidade de extras antigos.
  * Substituído o Gestor de extras pela Loja de extras.[]
  * Para obter mais informações, leia o guia do utilizador atualizado.
* Novos comandos:
  * Um comando não atribuído para alternar entre os idiomas disponíveis para OCR do Windows. (#13036)
  * Um comando não atribuído para alternar entre os modos de exibição de mensagens Braille. (#14864)
  * Um comando não atribuído para alternar entre a exibição ou não do indicador de selecção em Braille. (#14948)
  * Adicionado comandos padrão para mover para o pobjecto anterior ou seguinte em revisão plana da hierarquia de objectos (#15053)
    * Desktop: `NVDA+9 do bloco numérico` e `NVDA+3 do bloco numérico` para mover para o objecto anterior ou seguinte, respectivamente.
    * Laptop: `shift+NVDA+sinal de mais` e `shift+NVDA+agudo` para mover para o objecto anterior ou seguinte, respectivamente.
* Novas funcionalidades Braille:
  * Adicionado suporte para a linha Braille Help Tech Activator. (#14917)
  * Nova opção Braille para alternar a exibição do indicador de seleção (pontos 7 e 8). (#14948)
  * Nova opção para mover opcionalmente o cursor ou foco do sistema ao alterar a posição do cursor de revisão com as teclas de encaminhamento Braille. (#14885, #3166)
  * Ao pressionar "2 do bloco numérico" três vezes para anunciar o valor numérico do caractere na posição do cursor de revisão, as informações também são fornecidas em Braille. (#14826)
  * Adicionado suporte para o atributo ARIA 1.3 `aria-brailleroledescription`, permitindo que autores da web substituam o tipo de um elemento exibido no Braille. (#14748)
  * Driver Braille Baum: adicionados vários comandos Braille para realizar comandos de teclado comuns, como "windows+d", "alt+tab", etc.
  Consulte o guia do utilizador do NVDA para obter uma lista completa. (#14714)
  * Adicionada pronúncia de símbolos Unicode:
    * Símbolos Braille como "⠐⠣⠃⠗⠇⠐⠜". (#14548)
    * Símbolo da tecla Options do Mac "⌥". (#14682)
  * Adicionados comandos para as linhas Braille Tivomatic Caiku Albatross. (#14844, #15002)
    * Mostrar o diálogo de configurações do Braille.
    * Aceder a barra de estado.
    * Alternar a forma do cursor Braille.
    * Alternar o modo de exibição de mensagens Braille.
    * Activar/desactivar o cursor Braille.
    * Alternar o estado do indicador de selecção em Braille.
* Funcionalidades no Microsoft Office:
  * Ao activar o anúncio de texto realçado, as cores de realce passam a ser anunciadas no Microsoft Word. (#7396, #12101, #5866)
  * Ao activar o anúncio das cores, as cores de fundo passam a ser anunciadas no Microsoft Word. (#5866)
  * Ao usar atalhos do Excel para alternar o formato, como negrito, itálico, sublinhado e riscado de uma célula no Excel, o resultado passa a ser anunciado. (#14923)
* Gestão melhorada do som (experimental):
  * O NVDA agora emite áudio através da API de Sessão de Áudio do Windows (WASAPI), o que pode melhorar a capacidade de resposta, desempenho e estabilidade da voz e dos sons do NVDA.
  * Isso pode ser desativado nas configurações avançadas se ocorrerem problemas de áudio. (#14697)
  Adicionalmente, se o uso de WASAPI estiver activado, pode configurar  as seguintes opções avançadas:
    * Ajustar o volume dos sons e bipes do NVDA de acordo com o actual volume da voz. (#1409)
    * Controlar separadamente o volume dos sons do NVDA. (#1409)
  * Há um problema conhecido de falhas frequentes do NVDA com WASAPI activado. (#15150)
* No Mozilla Firefox e no Google Chrome, o NVDA agora informa quando um controle abre um diálogo, grelha, lista ou árvore se o autor especificou isso usando aria-haspopup. (#14709)
* Agora é possível usar variáveis de sistema (como `%temp%` ou `%homepath%`) na especificação do caminho ao criar cópias portáteis do NVDA. (#14680)
* No Windows 10 May 2019 Update e posterior, o NVDA pode anunciar os nomes dos Ambientes de trabalho virtuais ao abri-los, alterá-los e fechá-los. (#5641)
* Foi adicionado um parâmetro de sistema para que utilizadores e administradores de sistema possam forçar o NVDA a iniciar em modo seguro. (#10018)

### Alterações

* Actualização de componentes:
  * O eSpeak NG foi actualizado para a versão 1.52-dev commit `ed9a7bcf`. (#15036)
  * O conversor Braille LibLouis foi atualizado para [3.26.0](https://github.com/liblouis/liblouis/releases/tag/v3.26.0). (#14970)

> > - O CLDR foi atualizado para a versão 43.0. (#14918)

  -

* Alterações no LibreOffice:
  * Ao anunciar a localização do cursor de revisão, a localização actual do cursor passa a ser anunciada em relação à página atual no LibreOffice Writer para as versões do LibreOffice >= 7.6, similar ao que é feito para o Microsoft Word. (#11696)
  * O anúncio da barra de estado (NVDA+End) já funciona no LibreOffice. (#11698)
  * Ao mover para uma célula diferente no LibreOffice Calc, o NVDA já não anuncia incorretamente as coordenadas da célula anteriormente focada quando o anúncio de coordenadas da célula está desativado nas configurações do NVDA. (#15098)
* Alterações no Braille:
  * Ao usar um Dispositivo Braille via driver Braille HID padrão, o D-pad pode ser usado para emular as teclas de seta e Enter. Além
  disso, espaço+ponto1 e espaço+ponto4 agora correspondem, respectivamente, às teclas de seta para cima e para baixo. (#14713)
  * As actualizações no conteúdo dinâmico da web (ARIA live regions) agora são exibidas em braille.
  Isso pode ser desactivado no painel Configurações avançadas. (#7756) 
* Os símbolos de hífen e hífen emparelhado sempre serão enviados para o sintetizador. (#13830)
* A distância anunciada no Microsoft Word passa a respeitar a unidade definida nas opções avançadas do Word, mesmo ao usar o UIA para acessar documentos do Word. (#14542)
* O NVDA responde mais rapidamente ao mover o cursor em controles de edição. (#14708)
* O script para anunciar o destino de um link agora anuncia a partir da posição do cursor/foco em vez do objeto de navegação. (#14659)
* A criação de uma cópia portátil não requer mais a inserção de uma letra de unidade como parte do caminho absoluto. (#14681)
* Se o Windows estiver configurado para exibir segundos no relógio da barra do sistema, "NVDA+f12" para anunciar a hora passa a respeitar essa configuração. (#14742)
* O NVDA passa a anunciar grupos de controlos sem etiqueta, que possuam informações de posição úteis, como em versões recentes dos menus do Microsoft Office 365. (#14878)

### Correcções de erros

* Braille:
  * Várias correções de estabilidade na entrada/saída para linhas Braille, resultando em erros e 
  travamentos menos frequentes do NVDA. (#14627)
  * O NVDA já não muda desnecessariamente para "Sem Braille" várias vezes durante a detecção automática, resultando num registo mais
  limpo. (#14524)
  * O NVDA agora voltará para a conexão USB se um dispositivo Bluetooth HID (como o HumanWare Brailliant ou APH Mantis) for detectado
  automaticamente e uma conexão USB estiver disponível.
  Isso só funcionava para portas seriais Bluetooth antes. (#14524)
  * Quando nenhuma linha braille estiver ligada e o Visualizador Braille for fechado, pressionando `alt+f4` ou clicando no botão fechar,
  o tamanho da linha do subsistema braille será novamente redefinido para nenhuma célula. (#15214)
* Navegadores Web:
  * O NVDA já não causa, ocasionalmente, o travamento ou a parada de resposta do Mozilla Firefox. (#14647)
  * No Mozilla Firefox e Google Chrome, os caracteres digitados já não são relatados em algumas caixas de texto, mesmo quando a opção de
  falar caracteres digitados está desativada. (#14666)
  * Já é possível usar o modo de navegação em Controles Embutidos do Chromium onde antes não era possível. (#13493, #8553)
* No Mozilla Firefox, ao passar o rato sobre o texto, após um link, o NVDA já anuncia correctamente o texto. (#9235)
  * O destino de links gráficos agora é relatado corretamente no Chrome e Edge. (#14779)
  * Ao tentar anunciar a URL de um link sem o atributo href, o NVDA não ficará mais em silêncio.
  Em vez disso, o NVDA informa que o link não tem destino. (#14723)
  * No modo de navegação, o NVDA já não ignora, incorretamente, o movimento do foco para um controle de nível superior ou inferior, por
  exemplo, movendo-se de um elemento para a lista ou grelha que o contém. (#14611)
    * No entanto, observe que essa correção se aplica apenas quando a opção "Definir automaticamente o foco em elementos com foco" nas
    configurações do modo de navegação está desativada (que é a configuração padrão).
* Correções para Windows 11:
  * O NVDA volta a poder anunciar o conteúdo da barra de estado do Bloco de Notas. (#14573)
  * Ao mudar de separadore é anunciado o novo nome, e sua posição, no Bloco de Notas e Explorador de Ficheiros. (#14587, #14388)
  * No Windows 11, é possível abrir novamente os itens Colaboradores e Licença no menu Ajuda do NVDA. (#14725)
  * O NVDA volta a anunciar itens candidatos ao inserir texto em idiomas como chinês e japonês. (#14509)
* Correções para o Microsoft Office:
* Ao mover rapidamente entre células no Excel, o NVDA agora tem menos probabilidade de anunciar a célula ou seleção errada. (#14983, #12200, #12108)

* No Windows 10 e 11 Calculator, uma cópia portátil do NVDA não fará mais nada ou emitirá tons de erro ao inserir expressões no modo de  calculadora padrão em sobreposição compacta. (#14679)
* O NVDA se recupera novamente de muitas situações, como aplicativos que param de responder, que anteriormente causavam travamentos completos. (#14759)
* Ao forçar o suporte UIA com determinado terminal e consoles, um bug foi corrigido que causava congelamento e spam no arquivo de log. (#14689)
* O NVDA não falha mais ao anunciar a focalização de campos de senha no Microsoft Excel e Outlook. (#14839)
* O NVDA não recusará mais salvar a configuração após uma reinicialização da configuração. (#13187)
* Ao executar uma versão temporária a partir do lançador, o NVDA não induzirá os usuários a pensar que podem salvar a configuração. (#14914)
* O anúncio das teclas de atalho do objeto foi melhorada. (#10807)
* O NVDA agora responde de maneira geral um pouco mais rápida aos comandos e mudanças de foco. (#14928)
  -
  * Já é possível usar o caractere de barra invertida no campo de substituição de uma entrada de dicionário, quando o tipo não está definido como expressão regular. (#14556)
* Para símbolos que não têm uma descrição de símbolo no idioma atual, será usada a descrição de símbolo padrão em inglês. (#14558, #14417)

### Changes for Developers

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* Suggested conventions have been added to the add-on manifest specification.
These are optional for NVDA compatibility, but are encouraged or required for submitting to the add-on store.
The new suggested conventions are:
  * Using `lowerCamelCase` for the name field.
  * Using `<major>.<minor>.<patch>` format for the version field (required for add-on datastore).
  * Using `https://` as the schema for the url field (required for add-on datastore).
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
* `speechDictHandler.speechDictVars.speechDictsPath` is deprecated, use `WritePaths.speechDictsDir` instead. (#15021)

## 2023.1

Foi adicionada uma nova opção, "Estilo do Parágrafo" em "Navegação em Documentos".
Esta funcionalidade pode ser utilizada com editores de texto que não suportam a navegação por parágrafo nativamente, tais como o Bloco de Notas e o NotePad++.

Foi adicionado um novo comando global para anunciar o destino de um link, associado a "NVDA+k`".

O suporte para o conteúdo anotado da web (como comentários e notas de rodapé) foi melhorado.
Pressione "NVDA+d" para alternar entre resumos quando as anotações são anunciadas (por exemplo, "tem comentário, tem nota de rodapé").

As linhas Braille Tivomatic Caiku Albatross 46/80 já são suportadas nativamente.

O suporte para as versões ARM64 e AMD64 do Windows foi melhorado.

Feitas muitas correcções de bugs, nomeadamente correcções para o Windows 11.

eSpeak, LibLouis, Sonic rate boost e Unicode CLDR foram actualizados.
Existem novas tabelas Braille da Geórgia, Suaíli (Quénia) e Chichewa (Malawi).

Nota:
Esta versão quebra a compatibilidade com os extras existentes.

### Novas funcionalidades

* Microsoft Excel via UI Automation: Anúncio automático de cabeçalhos de colunas e linhas em tabelas. (#14228)
  * Nota: Isto refere-se a tabelas formatadas através do botão "Tabela" no friso "Inserir";
  "Primeira Coluna" e "Linha de Cabeçalho" em "Opções de Estilo de Tabela" correspondem a cabeçalhos de coluna e linha, respectivamente.
  * Isto não se refere a cabeçalhos específicos do leitor de ecrã através de intervalos nomeados, que actualmente não é suportado através da UI Automation.
* Foi adicionado um comando, não atribuído, para alternar a descrição desfasada de caracteres. (#14267)
* Acrescentada uma opção experimental para aproveitar o suporte de notificações UIA no Terminal Windows para anunciar texto novo ou alterado no terminal, resultando numa maior estabilidade e capacidade de resposta. (#13781);
  * Consultar o guia do utilizador para limitações desta opção experimental.
* No Windows 11 ARM64, o modo de navegação está agora disponível em aplicações AMD64 tais como Firefox, Google Chrome e 1Password. (#14397)
* Foi acrescentada uma nova secção às configurações do NVDA, "Navegação em Documentos".
Esta secção tem como único controlo o "Estilo de Parágrafo", que adiciona suporte para navegação por parágrafo de quebra de linha única (normal) e quebra de linha múltipla (bloco).
Esta funcionalidade pode ser usada com editores de texto que não suportam navegação por parágrafo nativamente, tais como o Bloco de Notas e o Notepad++. (#13797)
* A presença de múltiplas anotações passa a ser anunciada.
"nvda+d" passa agora a alternar o anúncio do resumo de cada anotação para as origens com múltiplas anotações.
Por exemplo, quando o texto tem um comentário e uma nota de rodapé a ele associada. (#14507, #14480)
* Adicionado suporte para as linhas Braille Tivomatic Caiku Albatross 46/80. (#13045)
* Novo comando global: Anúncio de destino do link ("NVDA+k").
Pressionado uma vez anuncia em voz e Braille o destino do link no objecto de navegação.
Pressionando duas vezes, a informação será mostrado numa janela, para uma revisão mais detalhada. (#14583)
* Novo comando global, sem associação de teclas, (Categoria Ferramentas): Anunciar o destino do link numa janela.
O mesmo que pressionar `NVDA+k` duas vezes, mas pode ser mais útil para os utilizadores de braille. (#14583)-

== Alterações ===

* Conversor Braille LibLouis actualizado para [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0). (#14436)
  * Grandes melhorias  no Braille húngaro, UEB e chinês bopomofo;
  * Suporte à norma dinamarquesa de Braile 2022;
  * Novas tabelas Braille para georgiano Braille literário, Suaíli (Quénia) e Chichewa (Malawi).
* A biblioteca Sonic rate boost foi actualizada para o commit "1d70513". (#14180)
* O CLDR foi actualizado para a versão 42.0. (#14273)
* O eSpeak NG foi actualizado para a versão 1,52-dev commit "f520fecb". (#14281, #14675)
  * Corrigido o anúncio de grandes números. (#14241)
* As aplicações Java com controlos utilizando o estado seleccionável anunciarão agora quando um item não está seleccionado e não quando o item está seleccionado. (#14336)

### Correcção de erros

* Correções para  Windows 11:
  * O NVDA passa a anunciar os destaques da pesquisa ao abrir o menu Iniciar. (#13841)
  * Em ARM, as apps x64 já não são identificadas como aplicações ARM64. (#14403)
  * Os itens do menu do histórico do Clipboard, tais como "item pin", podem ser acedidos. (#14508)
  * No Windows 11 22H2 e mais recentes, é novamente possível utilizar o rato e a interacção por toque para interagir com a área de notificação de capacidade excedida da Systray e o diálogo "Abrir Com". (#14538, #14539)
* As sugestões são comunicadas quando se digita uma @menção nos comentários do Microsoft Excel. (#13764)
* Na barra de localização do Google Chrome, os controlos de sugestão (mudar para separador, remover sugestão, etc.) são agora anunciados quando seleccionados. (#13522)
* Ao solicitar informação de formatação, as cores são agora explicitamente anunciadas no Wordpad ou no visualizador de registo, em vez de apenas "Cor por defeito". (#13959)
* No Firefox, a activação do botão "Mostrar opções" nas páginas de edições do GitHub funciona agora de forma fiável. (#14269)
* Os controlos do selector de datas no Diálogo de pesquisa avançada do Outlook 2016 / 365 passam a anunciar a etiqueta e valor. (#12726)
* Os controlos dos alternadores ARIA são agora reportados como alternadores no Firefox, Chrome e Edge, em vez de caixas de verificação. (#11310)
* O NVDA anunciará automaticamente o estado de ordenação no cabeçalho de uma coluna da tabela HTML quando alterada, premindo um botão interior. (#10890)
* O nome de um ponto de referência ou região é sempre falado automaticamente quando se salta do exterior para dentro usando navegação rápida ou foco no modo de navegação. (#13307)
* Quando reproduzir bips ou anunciar maiúscula, para letras maiúsculas está  activado, a descrição desfasada de caracteres  já não emite o bip ou anuncia "maiúscula" duas vezes. (#14239)
* Os controlos em tabelas em aplicações Java serão agora anunciados com maior precisão pelo NVDA. (#14347)
* Algumas configurações deixarão de ser inesperadamente diferentes quando usadas com perfis múltiplos. (#14170)
  * As seguintes configurações foram contempladas:
    * "Anúncio da indentação das linhas:" na secção "Formatação de documentos";
    * "Linhas de grelha da célula:" na secção "Formatação de documentos";
    * "Mostrar mensagens" na secção "Braille";
    * "Braille segue:" na secção "Braille".
  * Em alguns casos raros, estas opções utilizadas em perfis podem ser modificadas inesperadamente aquando da instalação desta versão do NVDA.
  * Por favor verifique estas opções nos seus perfis após actualizar o NVDA para esta versão.
* Os Emojis devem passar a ser anunciados em mais idiomas. (#14433)
* A presença de uma anotação já não deixará de aparecer em Braille para alguns elementos. (#13815)
* Corrigido um problema em que as alterações de configuração não eram guardadas correctamente ao mudar entre uma opção "Predefinição" e o valor da predefinição. (#14133)
* Ao configurar o NVDA ficará sempre definida, pelo menos, uma tecla NVDA. (#14527)
* Ao aceder ao menu do NVDA através da área de notificação, o NVDA não sugerirá mais uma actualização pendente quando esta não exista. (#14523)
* O tempo restante, passado e total é agora anunciado correctamente para ficheiros áudio ao longo de um dia no foobar2000. (#14127)
* Em navegadores web como o Chrome e o Firefox, alertas como downloads de ficheiros são mostrados em braille, para além de serem falados. (#14562)
* Corrigido o erro ao navegar para a primeira ou última coluna numa tabela no Firefox (#14554)
* Quando o NVDA é iniciado com o parâmetro `--lang=Windows``, volta a ser possível abrir o diálogo de Configurações gerais do NVDA. (#14407)

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

Esta versão  tem como principais destaques:

* Vários novos comandos, incluindo leitura contínua em tabelas;
* Adicionada uma secção, "Guia de Início Rápido", ao Manual do Utilizador;
* Várias correcções de bugs;
* Actualizados o eSpeak e o LibLouis;
* Novas tabelas Braille chinesas, suecas, Luganda e Kinyarwanda.

== Novas funcionalidades ==
* Adicionada uma secção, "Guia de Início Rápido", ao Guia do Utilizador. (#13934)
* Introduzido um novo comando para conhecer a tecla de atalho do foco actual. (#13960)
  * Desktop: `shift+numpad2``.
  * Laptop: `NVDA+ctrl+shift+.`.
* Introduzidos novos comandos para mover o cursor de revisão por página quando a aplicação o permite. (#14021)
  * Ir para a página anterior:
    * Desktop: `NVDA+pageUp``.
    * Laptop: `NVDA+shift+pageUp``.
  * Ir para a página seguinte:
    * Desktop: `NVDA+pageDown``.
    * Laptop: `NVDA+shift+pageDown``.
* Adicionados os seguintes comandos de tabela. (#14070)
  * Leitura contínua na coluna: NVDA+control+alt+downArrow````
  * Leitura contínua na linha: `NVDA+control+alt+rightArrow``
  * Ler a coluna inteira: `NVDA+control+alt+upArrow``
  * Ler linha inteira: `NVDA+control+alt+leftArrow``
* Microsoft Excel via UI Automation: O NVDA já anuncia quando sai de uma tabela numa folha de cálculo. (#14165)
* O anúncio de cabeçalhos de tabelas já pode ser configurado separadamente para linhas e colunas. (#14075)

== Alterações ===

* O eSpeak NG foi actualizado para a versão 1.52-dev commit `735ecdb8``. (#14060, #14079, #14118, #14203)
  * Corrigido o anúncio de caracteres latinos quando se utiliza o mandarim. (#12952, #13572, #14197)
* Conversor LibLouis braille actualizado para a [versão 3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0). (#14112)
* Adicionadas as tabelas Braille:
    * Braille chinês comum (caracteres chineses simplificados)
    * Braille literário de Kinyarwanda
    * Braille literário de Luganda
    * Braille sueco não contraído
    * Braille sueco parcialmente contraído
    * Braille sueco contraído
    * Chinês (China, Mandarim) Sistema Braille actual (sem tons) (#14138)
* O NVDA inclui agora a arquitectura do sistema operativo como parte dos dados estatísticos dos utilizadores. (#14019)

### Correcção de erros

* Ao actualizar o NVDA utilizando o Windows Package Manager CLI (aka winget), uma versão definitiva do NVDA já não é tratada como mais recente do que qualquer versão alfa que esteja instalada. (#12469)
* O NVDA irá agora anunciar correctamente as caixas de grupo em aplicações Java. (#13962)
* O cursor segue correctamente o texto falado durante a leitura contínua em aplicações tais como Bookworm, WordPad, ou o visualizador de logs NVDA. (#13420, #9179)
* Nos programas que utilizam a UI Automation, as caixas de verificação parcialmente marcadas serão anunciadas correctamente. (#13975)
* Melhor desempenho e estabilidade no Microsoft Visual Studio, Windows Terminal, e outras aplicações baseadas na UI Automation. (#11077, #11209)
  * Estas correcções aplicam-se ao Windows 11 Sun Valley 2 (versão 22H2) e posteriores;
  * O registo selectivo para eventos da UI Automation e alterações de propriedade passa a ser activado por padrão;
* Anúncio de texto, saída em Braille e supressão de palavra-passe já funcionam como esperado no Terminal Windows incorporado no Visual Studio 2022. (#14194)
* O NVDA passa a estar consciente da DPI quando utiliza múltiplos monitores.
Feitas várias correcções para a utilização de uma definição de DPI superior a 100% ou múltiplos monitores.
Ainda podem existir problemas com versões do Windows mais antigas que Windows 10 1809.
Para que estas correcções funcionem, as aplicações com as quais a NVDA interage também precisam de estar atentas à DPI.
Note-se que ainda existem problemas conhecidos com o Chrome e Edge. (#13254)
  * As molduras de realce visual devem agora ser correctamente colocadas na maioria das aplicações. (#13370, #3875, #12070)
  * A interacção por ecrã táctil já deve ser mais precisa para a maioria das aplicações. (#7083)
  * O seguimento do rato já deve funcionar para a maioria das aplicações. (#6722)
* As alterações da orientação (paisagem/retrato) já são correctamente ignoradas quando não há alterações (por exemplo, mudança de monitor). (#14035)
* O NVDA anunciará o arrasto de itens no ecrã em locais como o rearranjo dos mosaicos do  menu iniciar do Windows 10 e ambientes de trabalho virtuais no Windows 11. (#12271, #14081)
* Em configurações avançadas, a opção "Reproduzir um som para erros registados" é agora correctamente restaurada para o seu valor padrão ao pressionar o botão "Restaurar padrões". (#14149)
* O NVDA já pode seleccionar texto utilizando o atalho de teclado `NVDA+f10` nas aplicações Java. (#14163)
* O NVDA já não fica preso num menu ao nos deslocarmos com as setas pelas conversas agrupadas  no Microsoft Teams. (#14355)

### Alterações para Desenvolvedores

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* The [NVDA API Announcement mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) was created. (#13999)
* NVDA no longer processes `textChange` events for most UI Automation applications due to their extreme negative performance impact. (#11002, #14067)

#### Futuras remoções

* `core.post_windowMessageReceipt` is deprecated, use `winAPI.messageWindow.pre_handleWindowMessage` instead.
* `winKernel.SYSTEM_POWER_STATUS` is deprecated and usage is discouraged, this has been moved to `winAPI._powerTracking.SystemPowerStatus`.
* `winUser.SM_*` constants are deprecated, use `winAPI.winUser.constants.SystemMetrics` instead.

## 2022.3.3

Esta é uma versão menor para corrigir problemas com 2022.3.2, 2022.3.1 e 2022.3.

### Correcção de erros

* Corrigido o bug em que se o NVDA congelar ao bloquear, o NVDA permitirá o acesso ao ambiente de trabalho dos utilizadores enquanto estiver no ecrã de bloqueio do Windows. (#14416)
* Corrigido o bug em que se o NVDA congela ao bloquear, o NVDA não se comportará correctamente, como se o dispositivo ainda estivesse bloqueado. (#14416)
* Corrigidos problemas de acessibilidade com os processos Windows "esqueci-me do meu PIN" e actualização/experiência de instalação do Windows. (#14368)
* Corrigido um erro ao tentar instalar o NVDA em alguns ambientes Windows, por exemplo, Windows Server. (#14379)

### Alterações para Desenvolvedores

#### Deprecations

* `utils.security.isObjectAboveLockScreen(obj)` is deprecated, instead use `obj.isBelowLockScreen`. (#14416)
* The following functions in `winAPI.sessionTracking` are deprecated for removal in 2023.1. (#14416)
  * `isWindowsLocked```
  * "handleSessionChange
  * `unregister`
  * `register`
  * "isLockStateStateSuccessfullyTracked

## 2022.3.2

Esta é uma versão lançada para corrigir regressões na versão 2022.3.1 e resolver uma questão de segurança.

### Security Fixes

* Prevents possible system level access for unauthenticated users.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### Bug Fixes

* Fixes a regression from 2022.3.1 where certain functionality was disabled on secure screens. (#14286)
* Fixes a regression from 2022.3.1 where certain functionality was disabled after sign-in, if NVDA started on the lock screen. (#14301)

## 2022.3.1

Esta é uma versão lançada para corrigir vários problemas de segurança.
Please responsibly disclose security issues to <info@nvaccess.org>.

### Security Fixes

* Fixed exploit where it was possible to elevate from user to system privileges.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* Fixed a security issue allowing access to the python console on the lock screen via a race condition for NVDA startup.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Fixed issue where speech viewer text is cached when locking Windows.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### Bug Fixes

* Prevent an unauthenticated user from updating settings for speech and Braille viewer on the lock screen. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

A comunidade de desenvolvimento do NVDA contribuiu para parte significativa desta versão, incluindo a descrição desfasada dos caracteres e suporte melhorado da consola do Windows.

Esta versão também inclui várias correcções de bugs.
Nomeadamente, as versões actualizadas do Adobe Acrobat/Reader já não crasham ao ler um documento PDF.
O eSpeak foi actualizado, o que introduz 3 novas línguas: Bielorrusso, Luxemburguês e Totontepec Mixe.

### Novas funcionalidades

* Na Consola Windows, utilizada pelo Command Prompt, PowerShell, e o Subsistema Windows para Linux no Windows 11 versão 22H2 (Sun Valley 2) e posteriores:
  * O desempenho e a estabilidade foram amplamente melhorados. (#10964)
  * Ao pressionar "control+f" para localizar texto, a posição do cursor de revisão é actualizada para ir para o termo encontrado. (#11172)
  * A comunicação de texto escrito que não aparece no ecrã (tais como palavras-passe) é desactivada por defeito.
Pode ser reactivada nas configurações do NVDA, secção Avançadas, do NVDA. (#11554)
  * O texto que foi deslocado do ecrã pode ser revisto sem deslocar a janela da consola. (#12669)
  * Está disponível informação mais detalhada sobre a formatação do texto. ([microsoft/PR 10336 terminal](https://github.com/microsoft/terminal/pull/10336))
* Uma nova opção nas configurações do NVDA, secção   voz foi adicionada para ler as descrições dos caracteres após um atraso. (#13509)
* Uma nova opção nas configurações do NVDA, secção Braille foi adicionada para determinar se a rolagem da linha Braille para a frente/ou para trás deve interromper a fala. (#2124)

== Alterações ===

* O eSpeak NG foi actualizado para a versão 1.52-dev commit `9de65fcb``. (#13295)
  * Idiomas adicionados:
    * Bielorrusso
    * Luxemburguês
    * Totontepec Mixe
* Ao utilizar a UI Automation para aceder aos controlos de folha de cálculo do Microsoft Excel, 
o NVDA já anuncia quando uma célula é mesclada. (#12843)
* Em vez de anunciar apenas "tem detalhes", o objectivo dos detalhes é, sempre que possível, também anunciado, por exemplo, "tem comentários". (#13649)
* O tamanho da instalação do NVDA é agora mostrado na secção Programas e Funcionalidades do Windows. (#13909)

### Correcção de erros

* O Adobe Acrobat/Reader 64 bit já não provoca erros ao ler um documento PDF. (#12920)
  * Note que também é necessária a versão mais actualizada do Adobe Acrobat/Reader para evitar os erros.
* As medidas do tamanho da fonte já podem ser traduzidas no NVDA. (#13573)
* Ignorar eventos de Java Access Bridge onde não for possível encontrar nenhum "window handle" para aplicações Java.
Isto irá melhorar o desempenho de algumas aplicações Java, incluindo o IntelliJ IDEA. (#13039)
* O anúncio de células seleccionadas para o LibreOffice Calc é mais eficiente e já não resulta num congelamento do Calc quando muitas células são seleccionadas. (#13232)
* Quando executado sob um utilizador diferente, o Microsoft Edge já não é inacessível. (#13032)
* Quando a opção "Aumento da taxa" está desligada, a velocidade da voz do eSpeak já não desce entre 99% e 100%. (#13876)
* Corrigido o erro que permitia a abertura de 2 janelas "Definir comandos". (#13854)

### Alterações para Desenvolvedores

* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * This can be overridden by changing the "Windows Console support" setting in NVDA's advanced settings panel.
  * To find your Windows Console's NVDA API level, set "Windows Console support" to "UIA when available", then check the NVDA+F1 log opened from a running Windows Console instance.
* The Chromium virtual buffer is now loaded even when the document object has the MSAA `STATE_SYSTEM_BUSY` exposed via IA2. (#13306)
* A config spec type `featureFlag` has been created for use with experimental features in NVDA. See `devDocs/featureFlag.md` for more information. (#13859)

#### Deprecations

There are no deprecations proposed in 2022.3.

## 2022.2.3

Esta é uma versão menor que corrige uma acidental quebra de compatibilidade introduzida na versão 2022.2.1.

### Correcção de erros

* Corrigida uma falha que fazia que o NVDA não anunciasse "Desktop seguro" ao entrar num Desktop seguro.
Isto fazia com que o NVDA remote não reconhecesse ambientes de trabalho seguros. (#14094)

## 2022.2.2

Esta é uma versão de correção de um erro introduzido na versão 2022.2.1.

### Correcção de erros

* Corrigido um erro que permitia que um comando nem sempre funcionasse. (#14065)

## 2022.2.1

Esta é uma versão menor para resolver um problema de segurança.
Por favor, revele responsavelmente as questões de segurança a <info@nvaccess.org>.

### Correcções de segurança

* Exploração fixa onde era possível executar uma consola python a partir do ecrã de fechadura. (GHSA-rmq3-vvhq-gp32)
* Exploração fixa onde era possível escapar ao serralheiro utilizando a navegação por objectos. (GHSA-rmq3-vvhq-gp32)

### Alterações para os Desenvolvedores

Estas depreciações não estão actualmente agendadas para remoção.
Os pseudónimos depreciados permanecerão até nova ordem.
Por favor, testar o novo API e fornecer feedback.
Para autores de add-on, por favor abrir um número GitHub se estas alterações impedirem o API de satisfazer as suas necessidades.

* "appModules.lockapp.LockAppObject"" deve ser substituído por "NVDAObjects.lockscreen.LockScreenObject"". (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS`` deve ser substituído por `utils.security.getSafeScripts()`. (GHSA-rmq3-vvhq-gp32)

## 2022.2

Esta versão inclui muitas correcções de bugs.
Melhorias significativas para aplicações baseadas em Java, dispositivos Braille e funcionalidades do Windows.

Introduzidos novos comandos de navegação em tabelas.
Actualizado o Unicode CLDR.
Actualizado o LibLouis, que inclui uma nova tabela Braille alemã.

### Novas funcionalidades

* Suporte à interacção com Microsoft Loop Components nos produtos Microsoft Office. (#13617)
* Foram adicionados novos comandos de navegação de tabela. (#957)
 * "control+alt+home/end" para se mover para a primeira/última coluna da tabela;
 * "control+alt+pageUp/pageDown" para se mover para a primeira/última linha da tabela;.
* Foi acrescentado um comando, sem tecla de atalho atribuída, para alternar entre os modos de mudança automática de idioma e dialectos. (#10253)

== Alterações ===

* NSIS foi actualizado para a versão 3.08. (#9134)
* CLDR foi actualizado para a versão 41.0. (#13582)
* Conversor LibLouis braille actualizado para [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0). (#13775)
  * Nova tabela braille: Alemão grau 2 (detalhado)
* Adicionado novo "Role" para os controlos de "indicador de ocupado". (#10644)
* O NVDA anuncia agora quando uma acção própria não pode ser executada. (#13500)
  * Isto inclui quando:
    * Se utiliza a versão NVDA Windows Store.
    * Num contexto seguro.
    * está à  espera de uma resposta a um diálogo modal.

### Correcção de erros

* Correcções para aplicações baseadas em Java:
  * O NVDA já anuncia o estado apenas de leitura. (#13692)
  * O NVDA passa a anunciar corretamente o estado desactivado/activado. (#10993)
* O NVDA já anuncia atalhos de teclas de função. (#13643)
  * O NVDA já anuncia as barras de progressão por bips ou voz. (#13594)
  * O NVDA já não remove incorrectamente o texto dos widgets quando os apresentar ao utilizador. (#13102)
  * O NVDA já anuncia o estado dos botões de alternância. (#9728)
  * O NVDA já identifica a janela numa aplicação Java com múltiplas janelas. (#9184)
  * O NVDA já anuncia a informação de posição para controlos de tabulação. (#13744)
* Correcções no Braille:
  * Corrige a saída em braille ao navegar em textos em controlos rich edit  do Mozilla, tais como a redacção de uma mensagem em Thunderbird. (#12542)
  * Quando o Braile segue automaticamente, e o rato é movido com o acompanhamento do rato activado,
   os comandos de revisão de texto já actualizam o que é mostrado no dispositivo Braille com o conteúdo falado. (#11519)
  * Já é possível deslocar o conteúdo da linha Braille através do conteúdo falado pela utilização de comandos de revisão de texto. (#8682)
* O instalador do NVDA já pode funcionar a partir de directórios com caracteres especiais. (#13270)
* No Firefox, o NVDA já não falha ao reportar itens em páginas web quando os atributos aria-rowindex, aria-colindex, aria-rowcount ou aria-colcount são inválidos. (#13405)
* O cursor já não muda de linha ou coluna quando se utiliza a navegação em tabelas para navegar através de células unidas. (#7278)
* Ao ler PDFs não-interactivos no Adobe Reader, o tipo e estado dos campos do formulário (tais como caixas de verificação e botões de rádio) já são reportados. (#13285)
* "Restaurar a configuração para o padrão original" está agora acessível no menu da NVDA durante o modo seguro. (#13547)
* Qualquer botão do rato bloqueado será desbloqueado quando o NVDA terminar, anteriormente o botão do rato permaneceria bloqueado. (#13410)
* No Visual Studio já é anunciado o número das linhas. (#13604)
  * Note-se que para que o anúncio do número das linhas funcione, mostrar os números de linha deve ser activado no Visual Studio e no NVDA.
* No Visual Studio já é correctamente anunciada a indentação da linha. (#13574)
* O NVDA volta a anunciar os detalhes do resultado da pesquisa do menu Iniciar nas versões recentes do Windows 10 e 11. (#13544)
* No Windows 10 e 11, Versão 10.1908 e posteriores da calculadora, o NVDA anunciará os resultados quando mais comandos forem premidos, tais como comandos do modo científico. (#13383)
* No Windows 11, é novamente possível navegar e interagir com os elementos da interface do utilizador, tais como Barra de Tarefas e Vista de Tarefas usando o rato e a interacção por toque. (#13506)
* O NVDA irá anunciar o conteúdo da barra de estado no Bloco de Notas do Windows 11. (#13688)
* O realce visual do objecto de navegação já aparece imediatamente após a activação da funcionalidade. (#13641)
* Corrigida a leitura de itens de visualização de lista de uma coluna. (#13659, #13735)
* Corrigida a mudança automática de idioma do eSpeak para inglês e francês voltando para inglês britânico e francês (França). (#13727)
* Corrigida a mudança automática de idioma OneCore ao tentar mudar para um idioma anteriormente instalado. (#13732)

### Alterações para desenvolvedores

* Compiling NVDA dependencies with Visual Studio 2022 (17.0) is now supported.
For development and release builds, Visual Studio 2019 is still used. (#13033)
* When retrieving the count of selected children via accSelection,
the case where a negative child ID or an IDispatch is returned by `IAccessible::get_accSelection` is now handled properly. (#13277)
* New convenience functions `registerExecutableWithAppModule` and `unregisterExecutable` were added to the `appModuleHandler` module.
They can be used to use a single App Module with multiple executables. (#13366)

#### Futuras remoções

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

Esta versão inclui:

* Grandes melhorias do suporte à UIA no MS Office;
 Para o Microsoft Office, versão 16.0.15000 ou superior, no Windows 11, o NVDA irá utilizar a UI Automation para aceder aos documentos do Microsoft Word, por padrão;
 Isto proporciona uma melhoria significativa do desempenho em relação ao antigo acesso  pelo modelo de objectos.
* Melhorias nos drivers de dispositivos Braille, incluindo blocos de notas Seika, linhas Braille Papenmeier e no driver HID Braille;
* Vvárias correcções de bugs do Windows 11, para aplicações como Calculadora, Consola, Terminal, Correio e Painel de Emoji.
* O eSpeak-NG e o LibLouis foram actualizados, incluindo novas tabelas japonesas, alemãs e catalãs.

Nota importante:
Esta versão quebra a compatibilidade com os add-ons existentes.

### Novas funcionalidades

* Suporte para notas de relatório em MS Excel, com a UI Automation activada no Windows 11. (#12861)
* Em compilações recentes do Microsoft Word, através da UI Automation, no Windows 11 a existência de marcadores de página, comentários de rascunho e comentários resolvidos são agora anunciados tanto em voz como em Braille. (#12861)
* O novo parâmetro de linha de comando "--lang" permite anular o idioma configurado no NVDA. (#10044)
* O NVDA agora avisa sobre parâmetros de linha de comando que são desconhecidos e não são utilizados por quaisquer extras. (#12795)
* No Microsoft Word acedido através da UI Automation, o NVDA irá agora fazer uso do MathPlayer para ler e navegar nas equações matemáticas do Office. (#12946)
  * Para que isto funcione, deve usar o Microsoft Word 365
* O anúncio de "tem detalhes" e o comando associado para resumir a relação de detalhes foram actualizados para trabalhar em modo de foco. (#13106)
* Os Blocos de notas Seika passam a ser automaticamente detectados quando ligados via USB ou Bluetooth. (#13191, #13142)
 * Isto afecta os seguintes dispositivos: MiniSeika (16 e 24 células), V6, e V6Pro (40 células);
 * A selecção manual da porta COM bluetooth também é agora suportada.
* Foi adicionado um comando para alternar o visualizador braille; não há nenhum gesto predefinido. (#13258)
* Adicionados comandos para alternar várias teclas modificadoras simultaneamente com um dispositivo Braille (#13152)
* Os diálogos dos dicionários passam a ter um botão "Remover tudo" para facilitar a eliminação total de um dicionário. (#11802)
* Adicionado suporte para a Calculadora do Windows 11. (#13212)
* No Microsoft Word com a UI Automation activada no Windows 11, os números de linha e de secção podem agora ser reportados. (#13283, #13515)
* Para Microsoft Office 16.0.15000 ou superior no Windows 11, o NVDA utilizará a UI Automation para aceder a documentos do Microsoft Word, por padrão, proporcionando uma melhoria significativa do desempenho em relação ao antigo acesso por modelo de  objectos. (#13437)
 * Isto inclui documentos do Microsoft Word, e também o leitor e compositor de mensagens no Microsoft Outlook. 

### Alterações

* O Espeak-ng foi actualizado para 1.51-dev commit `7e5457f91e10``. (#12950)
* O conversor liblouis braille actualizado para [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0). (#13141, #13438)
 * Adicionada nova tabela Braille: Braille literário japonês (Kantenji).
 * Adicionada nova tabela Braille de computador alemão de 6 pontos.
 * Adicionada tabela Braille catalã de grau 1. (#13408)
* O NVDA passa a anunciar a selecção e união de células em LibreOffice Calc 7.3 e superiores. (#9310, #6897)
* Actualização do Unicode Common Locale Data Repository (CLDR) para 40.0. (#12999)
* "NVDA+Delete do teclado numérico" anuncia a posição do caractere ou objecto focado por padrão. (#13060)
* "NVDA+Shift+Delete do teclado numérico" anuncia a localização do cursor de revisão. (#13060)
* Adicionados comandos padrão para alternância de teclas modificadoras às linhas Braille da Freedom Scientific (#13152)
* A "linha base" já não é anunciada através do comando de anúncio de formatação de texto (`NVDA+f). (#11815)
* Activar a descrição longa já não tem um comando padrão atribuído. (#13380)
* O resumo dos detalhes do relatório tem agora um comando por defeito (`NVDA+d``). (#13380)
* O NVDA precisa de ser reiniciado após a instalação do MathPlayer. (#13486)

### Correcção de erros

* O painel de gestão da da Área de transferência já não deve roubar incorrectamente o foco ao abrir alguns programas do Office. (#12736)
* Num sistema em que o utilizador optou por trocar o botão primário do rato da esquerda para a direita, o NVDA deixará de abrir acidentalmente um menu de contexto em vez de activar um item, em aplicações tais como navegadores web. (#12642)
* Ao mover o cursor de revisão para além do fim dos controlos de texto, tal como no Microsoft Word com UI Automation, "fundo" é correctamente anunciado em mais situações. (#12808)
* O  NVDA pode anunciar o nome da aplicação e a versão para os binários colocados no sistema32 ao correr sob a versão de 64 bits do Windows. (#12943)
* Maior consistência da leitura das informações de resposta dos programas em modo terminal. (#12974)
  * Note-se que em algumas situações, ao inserir ou apagar caracteres no meio de uma linha, os caracteres após o cursor podem ser novamente lidos.
* MS Word com UIA: o comando de navegação rápida para próximo cabeçalho, em modo de navegação, já não fica preso no último cabeçalho de um documento, nem este cabeçalho é mostrado duas vezes na lista de elementos do NVDA. (#9540)
* No Windows 8 e posteriores, a barra de estado do Explorador de ficheiros já pode ser anunciada utilizando o comando padrão NVDA+end (desktop) / NVDA+shift+end (laptop). (#12845)
* As mensagens recebidas no chat do Skype para Empresas são novamente anunciadas automaticamente. (#9295)
* O NVDA pode de novo diminuir o volume quando utiliza o sintetizador SAPI5 no Windows 11. (#12913)
* Na Calculadora do Windows 10, o NVDA anunciará as etiquetas para as listas de itens do histórico e da memória. (#11858)
* Comandos como deslocação da linha e o encaminhamento de células funcionam novamente com dispositivos HID Braille. (#13228)
* Correio do Windows 11: Depois de mudar o foco entre aplicações, enquanto lê um longo e-mail, o NVDA já não fica preso numa linha do e-mail. (#13050)
* Braille HID: comandos com a barra de espaços (por exemplo, "Espaço+ponto 4") podem ser executados com sucesso a partir do dispositivo Braille. (#13326)
* Corrigido um problema em que se podiam abrir vários diálogos de configurações ao mesmo tempo. (#12818)
* Resolvido um problema em que algumas linhas Braille Focus Blue deixavam de funcionar depois de acordar o computador. (#9830)
* A "linha de base" deixa de ser anunciada quando a opção "Anunciar superescrito e subscrito" está activa. (#11078)
* No Windows 11, o NVDA deixará de impedir a navegação no painel emoji ao seleccionar emojis. (#13104)
* Evita que um bug provoque duplicação de anúncios quando se utiliza a Consola e o Terminal do Windows. (#13261)
* Corrigidos vários casos em que os itens da lista não podiam ser anunciados em aplicações de 64 bit, tais como o REAPER. (#8175)
* No gestor de transferências do Microsoft Edge, o NVDA passará agora automaticamente para o modo de foco assim que o item da lista com a transferência mais recente receber o foco. (#13221)
* O NVDA já não faz com que as versões de 64 bits do Notepad++ 8.3 ou superior crachem. (#13311)
* O Adobe Reader já não trava ao arrancar se o modo protegido do Adobe Reader estiver activado. (#11568)
* Corrigido um erro em que a selecção do Driver da linha Braille Papenmeier provocava o crash do NVDA. (#13348)
* No Microsoft Word com UIA: o número de página, ou outra formatação, já não é anunciado de forma inadequada, quando se passa de uma célula de tabela em branco para uma célula com conteúdo, ou do final do documento para o conteúdo existente. (#13458, #13459)
* O NVDA já não deixa de anunciar o título da página e começar a ler automaticamente, quando uma página é carregada no Google chrome 100. (#13571)
* O NVDA já não trava ao restaurar a configuração para o padrão original com anúncio de teclas de comando activado. (#13634)

### Alterações para desenvolvedores

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
* The "soffice" appModule has the following classes and functions removed `JAB_OOTableCell`, `JAB_OOTable`, `gridCoordStringToNumbers`. (#12849)
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

This is a minor release to fix a security issue.
Please responsibly disclose security issues to <info@nvaccess.org>.

### Security Fixes

* Addressed security advisory `GHSA-xc5m-v23f-pgr7`.
  * The symbol pronunciation dialog is now disabled in secure mode.

## 2021.3.4

This is a minor release to fix several security issues raised.
Please responsibly disclose security issues to <info@nvaccess.org>.

### Security Fixes

* Addressed security advisory `GHSA-354r-wr4v-cx28`. (#13488)
  * Remove the ability to start NVDA with debug logging enabled when NVDA runs in secure mode.
  * Remove the ability to update NVDA when NVDA runs in secure mode.
* Addressed security advisory `GHSA-wg65-7r23-h6p9`. (#13489)
  * Remove the ability to open the input gestures dialog in secure mode.
  * Remove the ability to open the default, temporary and voice dictionary dialogs in secure mode.
* Addressed security advisory `GHSA-mvc8-5rv9-w3hx`. (#13487)
  * The wx GUI inspection tool is now disabled in secure mode.

## 2021.3.3

This release is identical to 2021.3.2.
A bug existed in NVDA 2021.3.2 where it incorrectly identified itself as 2021.3.1.
This release correctly identifies itself as 2021.3.3.

## 2021.3.2

This is a minor release to fix several security issues raised.
Please responsibly disclose security issues to <info@nvaccess.org>.

### Bug Fixes

* Security fix: Prevent object navigation outside of the lockscreen on Windows 10 and Windows 11. (#13328)
* Security fix: The addons manager dialog is now disabled on secure screens. (#13059)
* Security fix: NVDA context help is no longer available on secure screens. (#13353)

## 2021.3.1

This is a minor release to fix several issues in 2021.3.

### Changes

* The new HID Braille protocol is no longer preferred when another braille display driver can be used. (#13153)
* The new HID Braille protocol can be disabled via a setting in the advanced settings panel. (#13180)

### Bug Fixes

* Landmark is once again abbreviated in braille. #13158
* Fixed unstable braille display auto detection for Humanware Brailliant and APH Mantis Q40 braille displays when using Bluetooth. (#13153)

## 2021.3

Esta versão introduz, entre muitas novidades:

* Suporte para a nova especificação HID Braille:

> > Esta especificação ambiciona padronizar o suporte às linhas Braille, evitando assim  a necessidade de drivers individuais.

* Actualizações do eSpeak-NG e do LibLouis, incluindo novas tabelas Braille (Russo e Tshivenda).
* Os sons de erro podem ser activados nas versões estáveis do NVDA, via uma nova opção nas configurações avançadas;
* A leitura contínua no Word passa a mover o texto, para que a posição de leitura esteja sempre visível;
* Muitas melhorias ao usar o Office com UIA;

> > Uma das melhorias da UIA é o Outlook passar a ignorar mais tipos de tabelas de formatação nas mensagens.

Nota importante:
Devido a uma actualização do nosso certificado de segurança, alguns utilizadores recebem um erro quando o NVDA 2021.2 verifica se há atualizações. 
O NVDA passa a usar as actualizações dos certificados de segurança do Windows, o que impedirá este erro no futuro.
Os utilizadores afectados terão de descarregar esta actualização manualmente.

### Novas Funcionalidades

* Adicionado um comando para alternar o anúncio do estilo das bordas das células. (#10408)
* Suporte para a nova especificação HID Braille, que ambiciona padronizar o suporte às linhas Braille, evitando assim  a necessidade de drivers individuais. (#12523)
  * Os dispositivos que suportem esta especificação serão automaticamente  detectados pelo NVDA.
  * Para detalhes técnicos sobre a implementação desta especificação pelo NVDA, consulte https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* Adicionado suporte para a linha Braille VisioBraille Vario 4. (#12607)
* As notificações de erro podem ser activadas (nas configurações avançadas) em qualquer versão do NVDA. (#12672)
* No Windows 10 e seguintes, o NVDA anunciará o número de sugestões ao introduzir termos a pesquisar em aplicações como Definições e  Microsoft Store. (#7330, #12758, #12790)
* A navegação em tabelas passa a ser suportada em "grid controls" criados usando o "Out-GridView cmdlet" no PowerShell. (#12928)

### Alterações

* Actualizado o eSpeak-ng para a versão 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`. (#12665)
* O NVDA escolherá o eSpeak como padrão se nenhuma voz do Windows OneCore voices instalada suportar o idioma preferido do NVDA. (#10451)
* Se as vozes Windows OneCore voices consistentemente falharem, o NVDA reverte para o eSpeak. (#11544)
* Ao ler a barra de estado, com "NVDA+end", o cursor de revisão já não é posicionado na sua localização.
Se necessitar desta funcionalidade, associe um comando ao script na secção Navegação por Objectos no diálogo "Definir comandos". (#8600)
* Se abrir um diálogo de configurações que já esteja aberto, o NVDA focar-se-á no diálogo existente em vez de provocar um erro. (#5383)
* Actualizado o conversor Braille liblouis para a versão [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0). (#12810)
  * Novas tabelas Braille: Russo grau 1, Tshivenda grau 1 e Tshivenda grau 2
* Em vez de "conteúdo marcado" ou "mrcd", "realçado" ou "realc" será anunciado por voz ou Braille, respectivamente. (#12892)

### Correcção de erros

* Registar as teclas modificadoras, como Control, ou Insert) está mais robusto, quando o watchdog está a tentar recuperar o NVDA. (#12609)
* É novamente possível verificar por actualizações do NVDA em certos sistemas, por exemplo em  novas instalações de raíz do Windows. (#12729)
* O NVDA anuncia correctamente células em branco de tabelas no Microsoft Word se usar UI automation. (#11043)
* Em células de grelha de dados ARIA na web, a tecla Escape é agora passada para a grelha e já não desliga o modo de foco incondicionalmente. (#12413)
* Ao ler uma célula título de uma tabela no Chrome, já não é lido o o nome da coluna duas vezes. (#10840)
* O NVDA já não anuncia um valor numérico para UIA sliders que possuam uma descrição textual do seu valor. (UIA ValuePattern é agora preferido a RangeValuePattern). (#12724)
* O NVDA já não trata sempre os valores de UIA sliders como percentagem.
* O anúncio da localização de uma célula do Microsoft Excel, acedido via UI Automation, volta a funcionar correctamente no Windows 11. (#12782)
* O NVDA já não define locales Python inválidos. (#12753)
* Se um extra desactivado é desinstalado e depois reinstalado, é automaticamente activado. (#12792)
* Corrigidos vários bugs na actualização e remoção de extras quando a pasta respectiva foi renomeada ou tem ficheiros abertos. (#12792, #12629)
* Ao usar a UI Automation para aceder aos controlos de uma folha do  Microsoft Excel, o NVDA já não anuncia seleccionado quando só está seleccionada uma célula. (#12530)
* Mais texto é lido automaticamente nos  diálogos do LibreOffice Writer, como nos diálogos de confirmação. (#11687)
* Ao ler ou navegar em modo de navegação no Microsoft Word via UI automation o documento é sempre deslizado para que a posição do modo de navegação esteja sempre visível e que a posição do cursor em modo de foco esteja correctamente sincronizada. (#9611)
* Em leitura contínua no Microsoft Word via UI automation, o documento é deslizado para que a posição do cursor esteja sempre visível. (#9611)
* Ao ler e-mails no Microsoft Outlook e com o NVDA acedendo às mensagens com a UI Automation, certas tabelas são marcadas como apenas de formatação e não serão anunciadas. (#11430)
* Um erro raro ao seleccionar outro dispositivo de saída áudio foi corrigido. (#12620)
* A introdução de texto com as tabelas de Braille literário já deve ser mais confiável em campos de edição. (#12667)
* Ao navegar o calendário da área de notificação do Windows, o NVDA já anuncia o dia da semana. (#12757)
* Quando se usa um método de entrada Chinês, como Taiwan - Microsoft Quick no Microsoft Word, deslocar a linha Braille para a frente ou para trás, já não continua a saltar novamente para a posição original do cursor. (#12855)
* Ao acessar os documentos do Microsoft Word via UIA, volta a ser possível navegar por frase (alt+seta abaixo / alt+seta acima). (#9254)
* Ao acessar o Microsoft Word com a UIA, a indentação de parágrafos passa a ser anunciada. (#12899)
* Ao acessar o Microsoft Word com a UIA, alguns comandos traduzíveis passam a ser anunciados pelo próprio Word. (#12904)
* Corrigida a duplicação em Braille e voz quando a 'descrição' é igual ao conteúdo ou ao nome. (#12888)
* No Microsoft Word com a UIA activada, a notificação de erros ortográficos é mais correcta. (#12161)
* No Windows 11, o NVDA já não anuncia "painel" ao pressionar Alt+Tab para alternar entre programas. (#12648)
* O Moderno painel lateral de seguimento de Comentários já é suportado no Microsoft  Word quando não é acessado via UIA. Pressione alt+f12 para se mover entre o painel lateral e o documento. (#12982)

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

Esta versão apresenta um suporte preliminar ao Windows 11.
Apesar de o Windows 11 ainda não ter sido lançado, esta versão foi testada em versões de teste do Windows 11.
Isto inclui uma correcção importante para a cortina de ecrã (consulte "Notas importantes").
A Ferramenta de correcção de registo de DLLs agora resolve mais problemas durante a execução do NVDA.
Há atualizações para o sintetizador eSpeak e o conversor Braille LibLouis.
Há também várias correções de bugs e melhorias, principalmente para suporte Vraille e terminais do Windows, calculadora, painel de emoji e histórico da área de transferência.

### Notas importantes

Devido a alterações na API do Windows Magnification, a  "Cortina de ecrã" teve de ser actualizada para suportar as novas versões do Windows.
Use o NVDA 2021.2 para activar a Cortina de ecrã no Windows 10 21H2 (10.0.19044) ou superior.
Isto inclui o Windows 10 Insiders e o Windows 11.
Para se certificar que está seguro, ao usar uma nova versão do Windows, tente obter confirmação visual de que a "Cortina de ecrã" funciona devidamente nessa versão do Windows.

### Novas funcionalidades

* Suporte para anotações ARIA:
  * adicionado um comando para anunciar o sumário de detalhes dum objecto com aria-details. (#12364)
  * adicionada uma opção na secção Avançadas para anunciar se um objecto tem detalhes no Modo de navegação. (#12439) 
* No Windows 10 Versão 1909 e superiores, (incluindo o Windows 11), o NVDA anunciará a contagem de sugestões ao executar pesquisas no Explorador de ficheiros. (#10341, #12628)
* No Microsoft Word, o NVDA agora anuncia o resultado da indentação e dos atalhos de indentação suspensos quando executados. (#6269)

### Alterações

* Atualizado o Espeak-ng para a versão 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`. (#12449, #12202, #12280, #12568)
* Se nas configurações de Formatação de documentos estiver marcado para anunciar Artigos, o NVDA anunciará "Artigo" após o conteúdo. (#11103)
* Atualizado o conversor Braille liblouis para a versão [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0). (#12526)
  * Novas tabelas  Braille: Búlgaro grau 1, Birmanês grau 1, Birmanês grau 2, Cazaque grau 1, Khmer grau 1, Curdo do Norte grau 0, Sepedi grau 1, Sepedi grau 2, Sesotho grau 1, Sesotho grau 2, Setswana grau 1, Setswana grau 2, Tatar grau 1, Vietnamita grau 0, Vietnamita grau 2, Sulvietnamita grau 1, Xhosa grau 1, Xhosa grau 2, Yakut grau 1, Zulu grau 1, Zulu grau 2
* Windows 10 OCR foi renomeado para Windows OCR. (#12690)

### Correcção de erros

* Na Calculadora do Windows 10, o NVDA passa a mostrar as expressões de cálculo em Braille. (#12268)
* Em programas de  terminal no Windows 10, versão 1607 e seguintes, ao introduzir ou apagar caracteres no meio de uma linha, os caracteres à direita já não são lidos. (#3200)
  * Diff Match Patch passa a predefinição. (#12485)
* A escrita Braille já funciona bem nas seguintes tabelas de grau 2: Árabe, Espanhol, Urdu, Chinês (China, Mandarin). (#12541)
* A ferramenta de correcção de DLL's já resolve mais problemas, eespecialmente em sistemas de 64 bit. (#12560)
* Melhorias no tratamento das teclas dos Notetakers Braille Seika da Nippon Telesoft. (#12598)
* Melhorias no anúncio do Painel de emojis do Windows e do Histórico da Área de transferências. (#11485)
* Actualizadas as descrições dos caracteres alfabéticos Bengali. (#12502)
* O NVDA já é fechado em segurança quando um novo processo é iniciado. (#12605)
* Reseleccionar as linhas Braille Handy Tech pelo diálogo Seleccionar Linha Braille já não causa erros. (#12618)
* O Windows versão 10.0.22000 ou posterior é reconhecido como Windows 11, e não Windows 10. (#12626)
* O suporte à Curtina de ecrã foi corrigido e testado até à versão Windows 10.0.22000. (#12684)
* Se não forem mostrados resultados ao filtrar comandos, o diálogo continuará a funcionar como é devido. (#12673)

### Alterações para desenvolvedores

* `characterProcessing.SYMLVL_*` constants should be replaced using their equivalent `SymbolLevel.*` before 2022.1. (#11856, #12636)
* `controlTypes` has been split up into various submodules, symbols marked for deprecation must be replaced before 2022.1. (#12510)
  * `ROLE_*` and `STATE_*` constants should be replaced to their equivalent `Role.*` and `State.*`.
  * `roleLabels`, `stateLabels` and `negativeStateLabels` have been deprecated, usages such as `roleLabels[ROLE_*]` should be replaced to their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
  * `processPositiveStates` and `processNegativeStates` have been deprecated for removal.
* On Windows 10 Version 1511 and later (including Insider Preview builds), the current Windows feature update release name is obtained from Windows Registry. (#12509)
* Deprecated: winVersion.WIN10_RELEASE_NAME_TO_BUILDS will be removed in 2022.1, there is no direct replacement. (#12544)

## 2021.1

Esta versão inclui, entre muitas outras novidades:

* Suporte opcional, experimental, para UIA no Excel e nos navegadores baseados no Chromium;
* Correcções  para vários idiomas;
* Melhoria no acesso aos links em Braille;
* Actualização ao dicionário CLDR Unicode, símbolos matemáticos e LibLouis;
* Muitas correcções de erros;
* Várias melhorias no Office e Visual Studio.

Notas importantes:

* Esta versão exige uma mudança na API de compatibilidade dos extras.
Os extras terão de ser testados e, pelo menos, reflectir esta mudança no manifest.ini.
* Esta versão termina com o suporte ao Adobe Flash.

### Novas Funcionalidades

* Suporte inicial ao UIA com navegadores baseados em Chromium (como o Edge). (#12025)
* Suporte opcional, experimental, ao Microsoft Excel via UI Automation. Apenas recomendado para Microsoft Excel build 16.0.13522.10000 ou superior. (#12210)
* Navegação facilitada nos resultados na Consola Python do NVDA. (#9784)
  * alt+seta acima/abaixo salta para o anterior/próximo resultado (juntar shift para seleccionar);
  * control+l limpa o painel de resultados;
* O NVDA passa a anunciar as categorias associadas a um compromisso no Microsoft Outlook, se houver algum. (#11598)
* Suporte para os dispositivos Braille Seika da Nippon Telesoft. (#11514)

### Alterações

* No modo de navegação, os controlos já podem ser activados com os cursores de toque da linha Braille na descrição, por exemplo, "lnk" para um link. Isto é especialmente útil para activar uma caixa de verificação sem etiqueta. (#7447)
* O NVDA passa a impedir a execução do OCR do Windows 10 se a cortina de ecrã estiver activa. (#11911)
* Actualizado o Repositório CLDR Unicode para a versão 39.0. (#11943, #12314)
* Adicionados mais símbolos matemáticos ao dicionário de símbolos. (#11467)
* O "Manual do utilizador" e os documentos "O que há de novo" e "Referência rápida de comandos" têm uma aparência melhorada. (#12027)
* Ao tentar alterar a disposição do ecrã, numa aplicação que não o suporte, como o Word, passa a ser anunciado "Não suportado neste documento". (#7297)
* A opção "Tentar cancelar a voz para eventos de foco expirados" da secção Avançadas das configurações do NVDA passa a estar activa por padrão. (#10885)
  * Este comportamento pode ser desactivado definindo a opção para "Não".
  * As aplicações Web, como o GMail, já não anunciam informações atrasadas ao mover o foco rápidamente.
* Actualizado o conversor Braille liblouis para a versão [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0). (#12137)
  * Novas tabelas Braille: Bielorrusso Braille literário, Bielorrusso Braille de computador, Urdu grau 1 e Urdu grau 2.
* O suporte ao conteúdo em Adobe Flash foi removido do NVDA, devido ao seu uso ser activamente desencorajado pela Adobe. (#11131)
* O NVDA será terminado mesmo que exista alguma janela aberta, pois o processo de terminar fechará qualquer janela ou caixa de diálogo do NVDA que ainda esteja aberta. (#1740)
* O Visualizador de discurso já pode ser fechado com "alt+F4" e passa a ter um botão padrão de fechar para facilitar quem usa o rato ou outro dispositivo apontador. (#12330)
* O Visualizador Braille passa a ter um botão padrão de fechar para facilitar quem usa o rato ou outro dispositivo apontador. (#12328)
* Na Lista de Elementos a tecla de atalho para o botão Activar foi removida em alguns idiomas  para não colidir com o atalho para um botão de rádio de tipos de elementos. Quando disponível, o botão conttinua a ser o predefinido, e como tal pode ser activado com Enter. (#6167)

### Correcção de erros

* A lista de mensagens no Outlook 2010 volta a ser possível de ser navegada. (#12241)
* Nos programas de consola no Windows 10 versão 1607 e superiores, ao inserir ou apagar caracteres no meio de uma linha, os caracteres à direita do cursor já não são falados. (#3200)
  * Esta correcção experimental deve ser activada manualmente nas configurações avançadas do NVDA alterando "Algoritmo diff" para "Diff Match Patch".
* No Microsoft Outlook, o anúncio sem sentido da distância ao pressionar shift+tab no corpo da mensagem para o campo "Assunto:" já não deverá acontecer. (#10254)
* Na Consola Python, inserir um tab para fins de indentação no início de uma linha ou completar o número de tabs no meio de uma linha já é suportado. (#11532)
* Informação de formatação e outras mensagens em modo de navegação já não apresentam linhas em branco não esperadas, quando a disposição de ecrã está desactivada. (#12004)
* Já é possível ler comentários no Microsoft Word com a UIA activada. (#9285)
* Melhorada a performance ao interagir com o Visual Studio. (#12171)
* Corrigidos bugs gráficos, tais como elementos em falta ao usar o NVDA com uma interface da direita para a esquerda. (#8859)
* Respeitar a direcção do esquema da interface gráfica baseando-se no idioma do NVDA e não no idioma do sistema. (#638)
  * Problema conhecido nos idiomas da direita para a esquerda: a borda direita de agrupamentos com controlos/etiquetas. (#12181)
* O idioma do python é configurado para coincidir, consistentemente, com o idioma seleccionado nas preferências do NVDA, mesmo que esteja configurado para "Predefinição  do utilizador". (#12214)
* TextInfo.getTextInChunks já não "congela" quando invocado em controlos Rich Edit, tais como o Visualizador de registo  do NVDA. (#11613)
* É novamente possível usar o NVDA em idiomas contendo sublinhados no nome do idioma (locale name) como pt_PT no Windows 10 1803 e 1809. (#12250)
* No WordPad, a configuração de anúncio de superescrito/subscrito já funciona como esperado. (#12262)
* O NVDA já não falha ao anunciar o novo conteúdo focado numa página Web por o foco anterior desaparecer e ser substituido pelo novo na mesma posição. (#12147)
* Já são anunciados os atributos de formatação riscado, superescrito e subscrito para células completas do Excelse a correspondente opção estiver marcada. (#12264)
* Corrigido o erro da cópia das configurações durante a instalação a partir de uma cópia portátil, quando a pasta de destino está vazia. (#12071, #12205)
* Corrigido o anúncio incorrecto de algumas letras com acentos ou diacríticos quando a opção "Anunciar maiúscula antes de letras maiúsculas" está marcada. (#11948)
* Corrigida a falha na alteração da entoação no sintetizador SAPI4. (#12311)
* O instalador do NVDA já respeita o parâmetro de linha de comando "--minimal" e já não toca o som de início, seguindo o que está documentado para o executável das cópias instaladas ou portáteis do NVDA. (#12289)
* No Microsoft Word ou Outlook, a navegação rápida para tabelas já salta para tabelas de formatação, se a opção "Incluir tabelas de formatação", da secção Modo de navegação das configurações do NVDA estiver marcada. (#11899)
* O NVDA já não anunciará "↑↑↑" para emojis em alguns idiomas. (#11963)

### Alterações para desenvolvedores

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
  * Instead use the `displayString` property on a `controlTypes.IsCurrent` enum value. EG `controlTypes.IsCurrent.YES.displayString`
* `NVDAObject` (and derivatives) property `isCurrent` now strictly returns `controlTypes.IsCurrent`. (#11782)
  * `isCurrent` is no longer Optional, and thus will not return None, when an object is not current `controlTypes.IsCurrent.NO` is returned.
* The `controlTypes.isCurrentLabels` has been removed, instead use the `displayString` property on a `controlTypes.IsCurrent` enum value. (#11782)
  * EG `controlTypes.IsCurrent.YES.displayString`
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

Nesta versão destacam-se as seguintes novidades:
Novos métodos de entrada em chinês;
Actualização do conversor Liblouis;
A lista de elementos (NVDA + f7) já funciona em modo de foco;
Ajuda sensível ao contexto disponível ao pressionar F1 nas janelas de configuração do NVDA;
Diversas melhorias em regras de pronúncia de pontuação/símbolo, dicionário de voz, mensagens em Braille e leitura rápida;
Várias correcções e melhorias no Correio, Outlook, Teams, Visual Studio, Azure Data Studio, e Foobar2000;
Na web, há melhorias no Google Docs e maior suporte para ARIA;
Muitas outras correcções e melhorias importantes.

### Novas Funcionalidades

* Ao pressionar F1 nas janelas de configuração do NVDA abre-se o Manual do utilizador na secção apropriada. (#7757)
* Suporte para sugestões de "auto complete" (IntelliSense) no Microsoft SQL Server Management Studio mais Visual Studio 2017 e superior. (#7504)
* Pronúncia de pontuação/símbolo: Suporte para agrupamento na definição dum símbolo complexo e suporte a referências a grupos nas regras de substituição, tornando-os mais simples e poderosos(#11107)
* Os utilizadores passam a ser notificados quando tentam criar entradas de dicionário de voz com substituições de expressão regular inválidas. (#11407)
  * Especificamente, erros de agrupamento passam a ser detectados.
* Adicionado suporte para os novos métodos de entrada rápida e pinyin em chinês tradicional no Windows 10.(#11562)
* Os cabeçalhos de tabelas passam a ser considerados campos de formulário com navegação rápida tecla f. (#10432)
* Adicionado um comando para alternar o anúncio de texto marcado (realçado), sem nenhuma predefinição. (#11807)
* Adicionado o parâmetro de linha de comando --copy-portable-config que permite copiar automaticamente a configuração fornecida para a conta do utilizador ao instalar silenciosamente o NVDA. (#9676)
* Encaminhar para a célula Braille já é possível no Visualizador Braille colocando o rato na célula para onde se quer encaminhar o foco. (#11804)
* O NVDA já detecta automaticamente as linhas Braille Humanware Brailliant BI 40X e 20X via USB e Bluetooth. (#11819)

### Alterações

* Actualizado o conversor braille liblouis para a versão 3.16.1:
 * Resolve múltiplos craches;
 * Adiciona a tabela Braille Bashkir grau 1;
 * adiciona a tabela Braille Copta 8 pontos Braille de computador;
 * adiciona as tabelas Braille literário Russo e Braille literário Russo (detalhado);
 * adiciona a tabela Braille Afrikaans grau 2;
 * Remove a tabela Braille Russo grau 1.
* Em leitura contínua, em modo de navegação, os comandos localizar anterior e localizar próximo já não interrompem a leitura se a opção permitir leitura rápida estiver activada. Em vez disso, a leitura contínua é retomada após a expressão pesquisada. (#11563)
* Nas linhas Braille da HIMS  F3 foi remapeada para Espaço + pontos 148. (#11710)
* Melhoramentos nas opções "Tempo de permanência de mensagens" e "Mostrar mensagens indefinidamente" das configurações de Braille. (#11602)
* Nos navegadores Web e outras aplicações que permitam o modo de navegação, a Lista de elementos (NVDA+F7) já pode ser invocada em modo de foco. (#10453)
* Actualizações de ARIA live regions passam a ser suprimidas quando o anúncio de conteúdo dinâmico estiver desactivado. (#9077)
* O NVDA passa a anunciar "Copiado:" antes do texto copiado. (#6757)
* A apresentação gráfica da tabela da gestão de discos foi melhorada. (#10048)
* As etiquetas para os controlos passam a desactivadas (em cinzento) quando o controlo está desactivado. (#11809)
* Actualizada a lista de emoji CLDR para a versão 38. (#11817)
* A opção nativa "Realce do foco" foi renomeada para "Realces visuais". (#11700)

### Correcção de erros

* O NVDA volta a trabalhar correctamente em campos de edição quando se usa a aplicação Fast Log Entry. (#8996)
* Anúncio do tempo decorrido no Foobar2000 se o tempo total não estiver disponível (como numa emissão ao vivo). (#11337)
* O NVDA passa a respeitar o atributo aria-roledescription em elementos em conteúdo editável em páginas web. (#11607)
* Já não é anunciado "lista" em cada linha duma  lista no Google Docs ou outro conteúdo editável no Google Chrome. (#7562)
* Ao navegar por caracter ou palavra, de um item de lista para outro, em conteúdo editável na web, a entrada no novo item de lista passa a ser anunciada. (#11569)
* O NVDA já lê a linha correcta quando o cursor de inserção é colocado no fim de um  link no fim de um item de lista no Google Docs ou em outro conteúdo editável na web. (#11606)
* No Windows 7, ao abrir ou fechar o Menu Iniciar a partir do Desktop, o foco já é o correcto. (#10567)
* Quando "Tentar cancelar a voz para eventos de foco expirados" está activado, o título dos separadores é novamente anunciado ao mudar de separadores no Firefox. (#11397)
* O NVDA já não falha ao anunciar um item de lista, depois de digitar a primeira letra numa lista usando as vozes SAPI5 Ivona. (#11651)
* Quando se usa as vozes SAPI5 da Ivona, harposoftware.com, o NVDA já pode guardar as configurações, mudar de sintetizador e já não ficará mudo ao reiniciar. (#11650)
* É novamente possível usar o modo de navegação para ler e-mails no Correio do Windows 10 versão 16005.13110 ou superior. (#11439)
* Já é possível escrever o número 6 em Braille de computador com o teclado Braille de uma linha HIMS. (#11710)
* Grandes melhorias na performance no Azure Data Studio. (#11533, #11715)
* Mesmo com a opção "Tentar cancelar a voz para eventos de foco expirados" activada, o título da janela Localizar do NVDA é novamente anunciado. (#11632)
* O NVDA já não deve pausar quando, ao acordar o computador, o foco ficar num documento do Microsoft Edge. (#11576)
* Já não é necessário pressionar "tab" ou mover o foco após fechar um menu de contexto no Microsoft Edge, para que o modo de navegação fique novamente funcional. (#11202)
* O NVDA volta a ler os itens numa vista de lista numa aplicação de 64-bit como o Tortoise SVN. (#8175)
* ARIA treegrids são tratadas como tabelas normais em modo de navegação no Firefox e Chrome. (#9715)
* Uma pesquisa do termo anterior pode ser iniciada com o comando "Localizar anterior via NVDA+shift+F3 (#11770)
* Um comando do NVDA já não é assumido como sendo repetido, se qualquer outra tecla for pressionada no meio dos dois comandos. (#11388) 
* as etiquetas de Realçado e enfatizado no Internet Explorer podem ser novamente marcadas para não serem anunciadas, desmarcando a opção "Enfatisado" na secção Formatação de documentos das configurações do NVDA. (#11808)
* Uma pausa de vários segundos, que ocorria a vários utilizadores, ao percorrerem as células do Excel, usando as setas, já não deverá ocorrer. (#11818)
* No Microsoft Teams, versões 1.3.00.28xxx, o NVDA já lê as mensagens nas conversações ou canais do Teams, o que não acontecia devido a um menu incorrectamente focado. (#11821)
* Texto marcado como erro ortográfico e de gramática, em simultâneo, no Google Chrome será correctamente anunciado pelo NVDA como tendo ambos os tipos de erro. (#11787)
* Quando se usa o Outlook em francês, o atalho para "Responder a todos"' (control+shift+R) volta a funcionar. (#11196)
* No Visual Studio, as dicas IntelliSense, que proporcionam detalhes adicionais sobre o item seleccionado do IntelliSense, já só são anunciadas uma vez. (#11611)
* Na Calculadora do Windows 10 , o NVDA não anuncia o progresso dos cálculos se a opção "Anunciar caracteres escritos" estiver desactivada. (#9428)
* O NVDA já não cracha ao usar a tabela Braille Inglês US grau 2 e a opção "Expandir para Braille de computador palavras sob o cursor" está activada e está a ser mostrado um URL. (#11754)
* É novamente possível anunciar a informação de formatação para a célula em foco do Excel, com NVDA+F. (#11914)

### Alterações para Desenvolvedores

* System tests can now send keys using spy.emulateKeyPress, which takes a key identifier that conforms to NVDA's own key names, and by default also blocks until the action is executed. (#11581)
* NVDA no longer requires the current directory to be the NVDA application directory in order to function. (#6491)
* The aria live politeness setting for live regions can now be found on NVDA Objects using the liveRegionPoliteness property. (#11596)
* It is now possible to define separate gestures for Outlook and Word document. (#11196)

## 2020.3

Os destaques desta versão incluem:

* Várias melhorias significativas na estabilidade e no desempenho, particularmente em aplicações do Microsoft Office;
* Novas configurações para alternar o suporte à interacção táctil e anúncio de gráficos;
* A existência de conteúdo marcado (realçado) pode ser anunciada nos navegadores;
* Novas tabelas braille alemãs.

== Novas Funcionalidades ==
* Já é possível alternar o anúncio de gráficos na secção Formatação de documentos das configurações do NVDA. Note que a desactivação desta opção ainda permite a leitura dos textos alternativos dos gráficos. (# 4837)
* Já é possível alternar a interacção táctil do NVDA. Foi adicionada uma opção à respectiva secção das configurações do NVDA. O comando padrão é NVDA + control + alt + t. (# 9682)
* Adicionadas novas tabelas braille alemãs. (# 11268)
* O NVDA passa a detectar controlos UIA de texto apenas de leitura. (# 10494)
* A existência de conteúdo marcado (realçado) é anunciada em voz e Braille em todos os navegadores Web. (# 11436)
 * Isto pode ser activado e desactivado por uma nova opção, "Conteúdo marcado", em "Formatação de documentos" das configurações do NVDA.
* Já é possível adicionar novas teclas à Simulação de teclas do sistema, a partir da opção "Definir comandos". (# 6060)
  * Para isso, pressione o botão adicionar depois de selecionar a categoria "Simulação de teclas do sistema".
* A HandyTech Active Braille com joystick já é suportada. (# 11655)
* A opção "Modo de foco automático para movimentos do cursor" passa a ser compatível com a desactivação de "Definir automaticamente o foco do sistema para os elementos focáveis".". (# 11663)

== Alterações ==
* A função "Anuncia as informações de formatação do texto sob o cursor de inserção" (NVDA+f) foi alterada para "Anunciar formatação do texto sob o cursor de inserção" em vez de para a posição actual do cursor de revisão. Para a função "Anuncia as informações de formatação da posição actual do cursor de revisão" use NVDA+shift+f. (#9505)
* O NVDA já não define, automaticamente, o foco do sistema para os elementos focáveis, por padrão, em modo de navegação, melhorando a performance e a estabilidade. (#11190)
* O CLDR foi actualizado da versão 36.1 para a versão 37. (#11303)
* Actualizado o eSpeak-NG para a versão 1.51-dev, commit 1fb68ffffea4
* Já é possível utilizar a navegação de tabelas em caixas de listas com elementos marcáveis da lista quando a lista tiver várias colunas. (#8857)
* No Gestor de extras, ao ser solicitada a confirmação da remoção de um extra, o botão "Não" passa a ser o predefinido. (#10015)
* No Microsoft Excel, a Lista de Elementos passa a apresentar as fórmulas na forma localizada. (#9144)
* O NVDA já usa a terminologia correcta para as notas no Excel. (#11311)
* Ao usar o comando "mover cursor de revisão para o foco" no modo de navegação, o cursor de revisão passa a ser posicionado na posição do cursor virtual. (#9622)
* A informação reportada em modo de navegação, como as informações de formatação (NVDA+F), passam a ser mostradas numa janela maior e centrada. (#9910)

### Correcção de erros

* O NVDA já anuncia sempre o símbolo, ao navegar por palavra e ao chegar a um símbolo isolado seguido por um espaço, independentemente do nível de pontuação. (#5133)
* Nas aplicações que usam QT 5.11 ou mais recente, a descrição dos objectos volta a ser anunciada. (#8604)
* Ao apagar uma palavra com Control+delete, o NVDA já não fica silencioso. (#3298, #11029)
  * Agora é anunciada a palavra à direita da que foi apagada.
* Na secção "Geral" das configurações do NVDA, a lista dos idiomas já é ordenada correctamente. (#10348)
* No diálogo "Definir comandos", foi bastante melhorada a performance durante a filtragem. (#10307)
* Já pode enviar caracteres Unicode com código superior a U+FFFF a partir da linha Braille. (#10796)
* No Windows 10, actualização de Maio de 2020, o NVDA já anuncia o conteúdo do diálogo "Abrir com". (#11335)
* Uma nova opção, experimental, na secção Avançadas das configurações do NVDA permite activar o registo selectivo para eventos e mudanças nas propriedades UI Automation o que pode provocar melhorias na performance no Microsoft Visual Studio e outras aplicações baseadas em UIAutomation. (#11077, #11209)
* Para os itens de lista marcáveis o estado Seleccionado já não é anunciado em duplicado e, se aplicável, o estado Não seleccionado é anunciado. (#8554)
* No Windows 10, actualização de Maio de 2020, o NVDA agora anuncia Mapeador de som da Microsoft ao mostrar os dispositivos de saída no diálogo de selecção do sintezizador. (#11349)
* No Internet Explorer, a numeração passa a ser anunciada correctamente em listas ordenadas mesmo que a lista não comece em 1. (#8438)
* No Google chrome, o NVDA já anuncia "não marcado", em todos os controlos marcáveis (não apenas caixas de verificação), que estejam actualmente não marcados. (#11377)
* Já é novamente possível navegar nos vários controlos quando o idioma do NVDA está definido para Aragonês. (#11384)
* O NVDA já não deve parar no Microsoft Word ao se deslocar, rapidamente, com as setas para cima ou para baixo, ou ao escrever com uma linha Braille ligada. (#11431, #11425, #11414)
* O NVDA já não adiciona um espaço inexistente ao copiar o objecto de navegação actual para a área de transferência. (#11438)
* O NVDA já não activa o perfil de leitura contínua quando não há texto para ser lido. (#10899, #9947)
* O NVDA já consegue ler a lista de funcionalidades no Internet Information Services (IIS) Manager. (#11468)
* O NVDA agora mantém o dispositivo áudio aberto para melhorar a performance em algumas placas de som. (#5172, #10721)
* O NVDA já não pára nem é finalizado quando se pressiona control+shift+downArrow no Microsoft Word. (#9463)
* O estado Expandido/Recolhido dos directórios na estrutura hierárquica de navegação em drive.google.com é sempre anunciado pelo NVDA. (#11520)
* O NVDA detectará automaticamente a linha Braille NLS eReader Humanware, ligada via Bluetooth, já que o seu identificador Bluethooth é "NLS eReader Humanware". (#11561)
* Grande melhoria de desempenho no Visual Studio Code. (# 11533)

### Alterações para desenvolvedores

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

* Suporte para uma nova linha Braille da Nattiq;
* Melhor suporte para a GUI do ESET antivírus e do Windows Terminal;
* Melhoras no desempenho com 1Password e o sintetizador Windows OneCore;
* Muitas outras correções e melhorias importantes.

== Novas funcionalidades ==
* Suporte para a nova linha Braille Nattiq nBraille (# 10778)
* Adicionada função para abrir o diretório de configurações do NVDA sem comando definido. (# 2214)
* Melhor suporte para a GUI do ESET antivírus. (# 10894)
* Adicionado suporte para Windows Terminal. (# 10305)
* Adicionado um comando para anunciar o perfil de configurações activo sem comando definido. (# 9325)
* Adicionado um comando para alternar o anúncio de subscrito e sobrescrito sem comando definido. (# 10985)
* As aplicações Web (como o GMail) já não anunciam informações desatualizadas ao mover o foco rapidamente. (# 10885)
  * Esta correção experimental deve ser activada manualmente através da opção "Tentar cancelar a voz para eventos de foco expirados" na secção Avançadas das configurações do NVDA.
* Adicionados mais símbolos ao dicionário. (# 11105)

### Alterações

* Actualizado o conversor Braille Liblouis da versão de 3.12.0) para a [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0). (# 10832, # 11221)
* O anúncio de subscrito e sobrescrito passa a ser controlado separadamente dos atributos da fonte. (# 10919)
* Devido às alterações feitas no VS Code, o NVDA já não desactiva, por padrão, o modo de navegação no Código. (# 10888)
* O NVDA já não anuncia "topo" e "fundo" ao mover o cursor de revisão directamente para a primeira ou última linha do objeto de navegação actual. (# 9551)
* O NVDA já não anuncia "esquerda" e "direita" ao mover o cursor de revisão directamente para o primeiro ou último caractere da linha do objeto de navegação actual. (# 9551)

### Correcção de erros

* O NVDA já inicia correctamente mesmo quando o ficheiro de registo não pode ser criado. (# 6330)
* Nas versões recentes do Microsoft Word 365, o NVDA não anuncia mais "excluir palavra inversa" quando pressionar Control + Backspace ao editar um documento. (# 10851)
* No Winamp, o NVDA volta a anunciar o estado de alternância de reprodução aleatória e repetição. (# 10945)
* O NVDA já não é extremamente lento ao mover-se pela lista de itens do 1Password. (# 10508)
* O sintetizador Windows OneCore já não faz pausas entre as expressões. (# 10721)
* O NVDA já não congela quando se abre o menu de contexto do 1Password na área de notificações do sistema. (# 11017)
* Para o Office 2013 e versões anteriores:
  * Os frisos são anunciados quando são focados pela primeira vez. (# 4207)
  * Os itens do menu de contexto são novamente anunciados correctamente. (# 9252)
  * As secções dos frisos são anunciadas de forma consistente ao navegar com Control mais setas. (# 7067)
* Os sons de erro do NVDA já não são ouvidos ao aceder os controlos de texto do DevExpress. (# 10918)
* As sugestões dos ícones na área de notificações já não são anunciadas, ao navegar com o teclado, se o seu texto for igual ao nome dos ícones, para evitar um duplo anúncio. (# 6656)
* Em Modo de navegação, no Mozilla Firefox e Google Chrome, o texto já não aparece, incorretamente, numa linha separada, quando o conteúdo da web usa o esquema CSS: inline-flex. (# 11075)
* Em Modo de navegação, com a opção "Definir automaticamente o foco do sistema para os elementos focáveis" desactivada, já é possível activar elementos que não são focáveis.
* Em Modo de navegação, com a opção "Definir automaticamente o foco do sistema para os elementos focáveis" desactivada, já é possível activar os elementos alcançados pressionando Tab. (# 8528)
* Em Modo de navegação, com a opção "Definir automaticamente o foco do sistema para os elementos focáveis" desactivada, a activação de certos elementos já não activa um controlo incorreto. (# 9886)
* Em Modo de navegação, com a opção "Definir automaticamente o foco do sistema para os elementos focáveis" desactivada, alternar para o modo de foco, com NVDA+espaço,  já foca o elemento sob o cursor. (# 11206)
* É novamente possível verificar atualizações do NVDA em certos sistemas; por exemplo. instalações limpas do Windows. (# 11253)
* Numa aplicação Java, o foco não é alterado quando a seleção é alterada numa estrutura hierárquica, tabela ou lista não focada. (# 5989)

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

Os destaques desta versão incluem:

* Suporte para várias novas linhas Braille da HumanWare e APH;
* Várias outras importantes correções de bugs, como a capacidade de ler novamente matemática no Microsoft Word usando o MathPlayer / MathType.

### Novas funcionalidades

* O item, actualmente seleccionado, numa caixa de lista, é novamente apresentado no modo de navegação, no Chrome, tal como era até ao NVDA 2019.1. (#10713)
* Já pode executar o clique direito do rato  num ecrã táctil, tocando com um dedo e mantendo. (#3886)
* Suporte para as novas linhas Braille: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, e NLS eReader. (#10830)

### Alterações

* O NVDA impede o sistema de hibernar ou fechar durante a leitura contínua. (#10643)
* Suporte para "out-of-process iframes" no Mozilla Firefox. (#10707)
* actualização do conversor Braille liblouis para a versão 3.12 (#10161)

### Correcção de erros

* Corrigido o não anúncio do símbolo "Unicode minus" (U+2212). (#10633)
* Ao instalar extras pelo Gestor de extras, os nomes dos ficheiros e pastas no diálogo de pesquisa já não são anunciados em duplicado. (#10620, #2395)
* No Firefox, quando se carrega Mastodon com a interface web avançada activada, todas as linhas de tempo já são renderizadas corretamente em modo de navegação. (#10776)
* Em modo de navegação, o NVDA já anuncia "Não marcado" nas caixas de verificação em que antigamente não anunciava. (#10781)
* Os controlos "ARIA switch" já não anunciam informações confusas, como "Não pressionado Marcado" ou "Pressionado marcado". (#9187)
* As vozes SAPI4 já devem conseguir falar certos textos. (#10792)
* O NVDA volta a poder ler e interagir com equações matemáticas no Microsoft Word. (#10803)
* O NVDA volta a anunciar, em modo de navegação, quando o texto que se está a seleccionar é desseleccionado pelo movimento das setas. (#10731).
* O NVDA já não se fecha se existirem erros ao iniciar o eSpeak. (#10607)
* Erros causados pela codificação unicode na traduçãodos atalhos, já não fecham o instalador, mitigado por usar a predefinição do texto em inglês. (#5166, #6326)
* Ao navegar com as setas para fora de listas e tabelas, no modo de leitura contínua com a navegação rápida activada já não é continuamente anunciado o fim de listas e tabelas. (#10706)

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

O NVDA 2019.3 é uma versão muito significativa que contém muitas alterações ocultas, incluindo a actualização do Python 2 para o Python 3 e uma importante reescrita do subsistema de fala do NVDA.
Embora essas alterações quebrem a compatibilidade com os extras mais antigos do NVDA, a actualização para o Python 3 é necessária para a segurança, e as alterações no sistema de a fala permitem algumas inovações interessantes num futuro próximo.
Outros destaques desta versão são:
Suporte a 64 bits para Java VMs;
Funcionalidades de Cortina de ecrã e Realçar foco;
Suporte para mais linhas Braille;
Novo visualizador em Braille;
Muitas outras correções.

### Novas Funcionalidades

* A precisão do comando "Mover o rato para o objecto de navegação" foi melhorada em campos de texto em aplicações Java. (#10157)
* Adicionado suporte para as seguintes linhas Braille da HandyTech (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* Todos os comandos definidos pelo utilizador podem ser removidos através da nova opção "Restaurar para o padrão original" na janela "Definir comandos". (#10293)
* O anúncio do tipo de letra no Microsoft Word agora inclui a marcação como texto oculto. (#8713)
* Adicionado um comando para mover o cursor de revisão para a posição marcada como início do bloco: NVDA+shift+F9. (#1969)
* No Internet Explorer, Microsoft Edge e versões recentes do Firefox e Chrome, as marcas passam a ser anunciadas no modo de foco e navegação por objectos. (#10101)
* No Internet Explorer, Google Chrome e Mozilla Firefox, já pode navegar por artigo e por agrupamento com as teclas de navegação rápida. É necessário atribuir essas teclas na janela "Definir comandos" aberta a partir de um documento em modo de navegação. (#9485, #9227)
 * As figuras também passam a ser anunciadas. São consideradas objectos e portanto navegáveis com a tecla rápida "o".
* No Internet Explorer, Google Chrome e Mozilla Firefox, os artigos passam a ser anunciados na navegação por objectos, e opcionalmente, em modo de navegação se activados na secção Formatação de Documentos. (#10424)
* Adicionada a funcionalidade "Cortina de ecrã" que, quando activada torna o ecrã totalmente preto no Windows 8 e superiores (#7857):
 * Adicionada uma função para activar a cortina até o NVDA ser reiniciado, pressionando uma vez, ou activar sempre que o NVDA esteja em execução. É necessário atribuir uma tecla de atalho na janela "Definir comandos", secção "Visão";
 * Pode ser activada e configurada na secção "Visão" das configurações do NVDA.
* Adicionada a funcionalidade "Realçar foco" (#971, #9064):
 * O realce do foco do sistema, do objecto de navegação, e do cursor em modo de navegação podem ser activados e configurados na secção "Visão" das configurações do NVDA;
 * Nota: Esta funcionalidade é incompatível com o extra focus highlight, mas o extra pode ser usado se a função nativa "Realçar foco" estiver desactivada.
* Adicionada a ferramenta Visualizador Braille, que permite a visualização da saída Braille através de uma janela no ecrã. (# 7788)

== Alterações ==
* O Guia do utilizador já ensina a usar o NVDA na consola Windows. (#9957)
* Executar o nvda.exe desliga uma cópia em execução e activa uma nova cópia. O parâmetro -r|--replace da linha de comando ainda é aceite, mas é ignorado. (#8320)
* No Windows 8 e posteriores o NVDA passa a anunciar a informação do nome e versão dos programas "hosted", tais como os descarregados da loja Microsoft, usando a informação fornecida pelo programa. (#4259, #10108)
* Ao alternar o acompanhamento, ou não, das alterações no Microsoft Word, através do teclado, o NVDA anunciará o estado da configuração. (#942) 
* A identificação da versão do NVDA é agora colocada no início do ficheiro de registo. Isto acontece mesmo com o registo desactivado nas configurações do NVDA. (#9803)
* A janela de configurações do NVDA já não permite alterar o nível de registo se este foi definido pelo parâmetro da linha de comandos. (#10209)
* No Microsoft Word, o NVDA passa a anunciar o estado de mostrar, ou não, os caracteres não imprimíveis, quando se usa o comando Ctrl+Shift+8. (#10241)
* Actualizado o conversor Braille Liblouis para o commit 58d67e63. (#10094)
* Quando o anúncio dos caracters CLDR, (incluindo emojis) está activado, eles serão anunciados em qualquer nível de pontuação. (#8826)
* Pacotes Python de terceiros incluíddos no NVDA, tais como comtypes, passam a registar os seus avisos e erros no registo do NVDA. (#10393)
* Actualizado o Unicode Common Locale Data Repository emoji annotations para a versão 36.0. (#10426)
* Quando se foca um agrupamento em modo de navegação, a descrição é anunciada (#10095)
* O Java Access Bridge passa a ser incluido com o NVDA para activar o acesso a aplicações Java, incluindo para 64 bit Java VMs. (#7724)
* Se o Java Access Bridge não estiver activado para o utilizador, o NVDA, automaticamente, activa-o no arranque. (#7952)
* Actualizado o sintetizador eSpeak-NG para a versão 1.51-dev, commit ca65812ac6019926f2fbd7f12c92d7edd3701e0c. (#10581)

### Correcções

* Os Emojis e outros caracteres unicode 32 bit ocuparão menos espaço na linha Braille quando representados pelo seu código hexadecimal. (#6695)
* No Windows 10, o NVDA anuncia as sugestões das aplicações da plataforma universal (UWP) se o NVDA estiver configurado para as anunciar na secção "Apresentação de objectos" das configurações. (#8118)
* No Windows 10, actualização Anniversary e seguintes, o texto escrito no Mintty já é anunciado. (#1348)
* No Windows 10, actualização Anniversary e seguintes, na Consola Windows, os resultados mostrados perto do cursor já não são soletrados. (#513)
* Os controlos na janela do compressor do  Audacity já são anunciados ao navegar pela janela. (#10103)
* O NVDA já não considera os espaços como palavras na revisão de objectos em editores de texto baseados em  Scintilla, como o Notepad++. (#8295)
* O NVDA impedirá o sistema de hibernar enquanto se estiver a deslocar pelo texto com a linha Braille. (#9175)
* No Windows 10, o Braille já segue o cursor ao editar o conteúdo de uma célula no Microsoft Excel e noutros controlos de texto UIA, onde respondia com atraso. (#9749)
* O NVDA volta a anunciar as sugestões na barra de endereço do Microsoft Edge. (#7554)
* O NVDA já não fica silencioso ao focar um "HTML tab control header" no Internet Explorer. (#8898)
* No Microsoft Edge baseado em EdgeHTML, o NVDA já não reproduz o som de pesquisa quando a janela é maximizada. (#9110, #10002)
* As caixas combinadas de ARIA 1.1 já são suportadas no Mozilla Firefox e Google Chrome. (#9616)
* O NVDA já não anuncia o conteúdo de colunas ocultas para itens de listas em controlos SysListView32. (#8268)
* A janela de configurações do NVDA, secção "Gerais", já não mostra informações  sobre o nível de registo quando é executado em ambientes seguros. (#10209)
* No menu Iniciar do Windows 10, actualização Anniversary e seguintes, o NVDA passa a anunciar os detalhes dos resultados da pesquisa. (#10232)
* No modo de navegação, se quer o movimento com as setas, quer com as teclas de navegação rápida, o documento for alterado, o NVDA, em certos casos,  já não falará incorrectamente o conteúdo. (#8831, #10343)
* Os nomes de algumas marcas (bullets) no Microsoft Word foram corrigidos. (#10399)
* No Windows 10, actualização de Maio 2019 e seguintes, o NVDA volta a anunciar o primeiro Emoji ou item da área de transferência, quando o painel de emojis ou o histórico da área de transferência são abertos. (#9204)
* No Poedit, é outra vez possível ver algumas traduções para idiomas com escrita da direita para a esquerda. (#9931)
* Na aplicação  Definições do Windows 10, actualização de Abril 2018 e seguintes, o NVDA já não anuncia informação sobre a barra de progresso para o volume encontradas na secção Sistema/Som. (#10284)
* Expressões regulares inválidas nos dicionários de voz já não provocam a paragem total da voz no NVDA. (#10334)
* Ao ler itens de listas com marcas (bullets) no Microsoft Word com a UIA activada, a marca do próximo item já não é anunciada. (#9613)
* Alguns casos raros de erros ou problemas de conversão Braille com o  liblouis foram resolvidos. (#9982)
* As aplicações Java iniciadas antes do NVDA já são acessíveis sem ser necessário reiniciá-las. (#10296)
* No Mozilla Firefox, quando o elemento em foco fica marcado como current (aria-current), esta alteração já não é anunciada várias vezes. (#8960)
* O NVDA passa a tratar alguns caracteres unicode compostos, tais como e-acute como um caracter simples ao mover-se pelo texto. (#10550)
* Spring Tool Suite Version 4 já é suportada. (#10001)
* Não anunciar em duplicado o nome quando aria-labelledby relation target é um elemento interior. (#10552)
* No Windows 10 versão 1607 e seguintes, caracteres digitados num teclado Braille passam a ser anunciados em mais situações. (#10569)
* Ao mudar de dispositivo de saída de áudio, os sons reproduzidos pelo NVDA passam a usar o novo dispositivo seleccionado. (#2167)
* No Mozilla Firefox, mover o foco em modo de navegação é mais rápido. Isto faz com que movimentar o cursor virtual tenha, na maior parte dos casos, uma resposta mais rápida. (#10584) 

== Alterações para desenvolvedores ==
* Atualização do Python para  a versão 3.7. (#7105)
* Atualização do pySerial para a versão 3.4. (#8815)
* Atualização do wxPython para a versão 4.0.3 para dar suporte ao Python 3.5 e seguintes. (#9630)
* Atualização do six para a versão 1.12.0. (#9630)
* Atualização do py2exe para a versão 0.9.3.2 (em desenvolvimento, commit b372a8e de albertosottile/py2exe#13). (#9856)
* Atualização do UIAutomationCore.dll, módulo comtypes, para a versão 10.0.18362. (#9829)
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

Esta é uma sub-versão para corrigir vários craches presentes na 2019.2. As correcções incluem:

* Corrigidos vários craches no GMail observados quer no Mozilla Firefox quer no  Google Chrome ao interagir com alguns menus popup, tais como ao criar filtros ou ao alterar algumas opções do GMail. (#10175, #9402, #8924)
* No Windows 7, o NVDA já não causa craches no Windows Explorer quando o rato é usado no menu Iniciar. (#9435) 
* O Windows Explorer no Windows 7 já não cracha ao aceder aos campos de edição de metadata. (#5337) 
* O NVDA já não "congela" ao interagir com imagens com URI base64 no Mozilla Firefox ou Google Chrome. (#10227)

## 2019.2

Os destaques desta versão incluem:

* Ddetecção automática das linhas Braille da Freedom Scientific;
* Uma opção experimental na secção Avançadas das configurações do NVDA para impedir que o modo de navegação mova o foco automaticamente (o que pode trazer melhorias de desempenho);
* Uma opção de "Aumento de velocidade" para o sintetizador Windows OneCore Voices para que se possa utilizar velocidades muito rápidas;
* Muitas outras correções de bugs.

== Novas Funcionalidades ==
* O suporte ao NVDA do Miranda NG já funciona com as novas versões clientes. (#9053) 
* Já pode desactivar o modo de navegação por padrão, desactivando a nova opção "Activar o modo de navegação no carregamento de páginas" nas configurações do modo de navegação do NVDA. (#8716) 
 * Note que mesmo com esta opção desactivada pode activar o modo de navegação, manualmente, pressionando NVDA+barra de espaços.
* Já pode filtrar símbolos no diálogo "Pronúncia de pontuação/símbolo", tal como faz no diálogo "Lista de elementos" ou "Definir comandos". (#5761)
* Foi adicionado um comando para alternar a quantidade de texto lida pelo rato, "Unidade de leitura de texto:", mas sem ter sido atribuido qualquer comando. (#9056)
* Foi adicionada ao sintetizador windows OneCore a opção "Aumento de velocidade", o que permite velocidades bem mais rápidas. (#7498)
* A opção "Aumento de velocidade", para os sintetizadores que a suportem, já pode ser configurada no anel de configurações do sintetizador. (actualmente eSpeak-NG e Windows OneCore voices). (#8934)
* Os perfis de configurações já podem ser activados manualmente através de um comando. (#4209)
 * O comando deve ser configurado no diálogo "Definir comandos".
* No Eclipse, foi adicionado suporte para a autocompletação no editor de código. (#5667)
 * Adicionalmente, a informação Javadoc pode ser lida no editor, se estiver presente, pressionando NVDA+d.
* Adicionada uma opção experimental às configurações Avançadas que permite fazer com que o foco do sistema deixe de seguir o modo de  navegação  (Definir automaticamente o foco do sistema para os elementos focáveis.). (#2039)
Embora possa não ser adequado desactivar em todas as páginas, pode resolver:
 * Efeito elástico: o NVDA esporadicamente anula o último comando em modo de navegação e volta para a localização anterior;
 * As caixas de edição ficam com o foco quando se passa por elas ao navegar com as setas;
 * Lentidão na resposta aos comandos em modo de navegação.
* Para os drivers das linhas Braille que o suportem, as configurações específicas do driver podem ser alteradas nas configurações de Braille do diálogo de configurações do NVDA. (#7452)
* As linhas Braille da Freedom Scientific passam a ser suportadas pela detecção automática de linhas Braille. (#7727)
* Adicionado um comando para mostrar o substituto para um símbolo sob o cursor de revisão. (#9286)
* Adicionada uma opção experimental às configurações Avançadas que permite testar uma, ainda em progresso, versão reescrita do suporte do NVDA à consola do Windows, usando a API Microsoft UI Automation. (#9614)
* Na consola de Python, o campo de edição já suporta a colagem de múltiplas linhas daÁrea de transferência. (#9776)

### Alterações

* O volume do sintetizador passa a ser alterado de 5 em 5% em vez de 10% quando se usa o anel de configurações do sintetizador. (#6754)
* Clarificada a informação no Gestor de extras quando se inicia o NVDA com os extras desactivados. (#9473)
* Actualizado o Unicode Common Locale Data Repository emoji annotations para a versão 35.0. (#9445)
* Actualizado o liblouis braille translator para a versão 3.10.0. (#9439, #9678)
* Actualizado o eSpeak-NG para a versão  commit 67324cc.
* A tecla de atalho, em inglês, para o campo "Filtrar por:", no diálogo "Lista de elementos" foi alterada para alt+y. (#8728)
* Quando uma linha Braille, ligada via Bluetooth, é detectada automaticamente, o NVDA continuará à procura por dispositivos suportados pelo mesmo driver, via USB, e alternará para uma ligação USB, se a encontrar. (# 8853)
* O NVDA passa a anunciar a selecção ou des-selecção após o anúncio do texto respectivo. (#9028, #9909)
* No código do  Microsoft Visual Studio, o modo de navegação é desactivado por padrão. (#9828)

### Correcções

* O NVDA já não cracha quando uma pasta de um extra está vazia. (#7686)
* As marcas LTR e RTL já não são anunciadas em Braille ou em voz ao navegar por caractere ao aceder à janela de propriedades. (#8361)
* Ao saltar para um campo de formulário, em Modo de navegação, o campo será lido na sua totalidade e não apenas a primeira linha. (#9388)
* O NVDA já não fica silencioso após sair do Correio do Windows 10. (#9341)
* O NVDA já não falha ao arrancar com o Windows definido para um idioma que o NVDA não conhece, como por exemplo, Inglês (Holanda). (#8726)
* Quando o Modo de navegação está activado no Microsoft Excel e alterna para um navegador em modo de foco, ou vice versa, o modo de navegação é anunciado correctamente. (#8846)
* O NVDA já anuncia correctamente o número da linha com o ponteiro do rato no Notepad++ e outros editores de texto baseadas em Scintilla. (#5450)
* No Google Docs (e outros editores na Net), já não é anunciado em Braille, antes do cursor, "fim de lst" no meio de um item de lista. (#9477)
* Na actualização de Maio de 2019 do Windows 10, o NVDA já não anuncia as notificações de alteração do volume feitas com teclas de hardware quando o foco está no Explorador de ficheiros. (#9466)
* o carregamento da lista do diálogo "Pronúncia de de pontuação e símbolos" é muito mais rápida mesmo com mais de 1000 entradas. (#8790)
* Nos editores baseados em Scintilla, como o Notepad++, o NVDA já anuncia correctamente o número da linha com a translineação activada. (#9424)
* No Microsoft Excel, as coordenadas da célula já são anunciadas após mudança provocada pelo pressionar de shift+enter ou shift+numpadEnter. (#9499)
* No Visual Studio 2017 e posteriores, na janela do Explorador de Objectos o item seleccionado na estrutura de objectos ou estrutura de membros com categorias já é anunciado correctamente. (#9311)
* Extras cujos nomes sejam apenas diferentes na capitalização já não são tratados como extras separados. (#9334)
* Para o sintetizador Windows OneCore voices, a velocidade configurada no NVDA já não é afectada pela velocidade definida nas configurações de voz do Windows 10. (#7498)
* O ficheiro de log já pode ser aberto com NVDA+F1 quando não exista informações para desenvolvimento para o objecto em foco. (#8613)
* É novamente possível usar os comandos de navegação de tabelas do NVDA no Google Docs, no Firefox e no Chrome. (#9494)
* As teclas "bumper" das linhas Braille da Freedom Scientific já funcionam correctamente. (# 8849)
* Ao ler o primeiro caractere de um documento, no Notepad ++ 7.7 X64, o NVDA já não congela por até dez segundos. (# 9609)
* O HTCom já pode ser usado com uma linha Braille da Handy Tech em conjunto com o NVDA. (#9691)
* No Mozilla Firefox, as actualizações de uma live region já não são anunciadas se a live region estiver numa aba em segundo plano. (#1318)
* O diálogo Localizar do NVDA, em modo de navegação, já não falha, mesmo que o diálogo Sobre o NVDA esteja aberto em segundo plano. (#8566)

### Alterações para desenvolvedores

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

Esta versão pontual corrige os seguintes erros:

* O NVDA já não causa falhas no Excel 2007 nem deixa de informar que uma célula tem fórmulas. (#9431)
* O Google Chrome já não trava ao interagir com determinadas caixas de listas. (#9364)
* Foi corrigido um problema que impedia a cópia de configurações do utilizador para as configurações do sistema. (#9448)
* No Microsoft Excel, o NVDA usa novamente a mensagem traduzida ao informar a localização das células mescladas. (#9471)

= 2019.1 =
Os destaques desta versão incluem:
* Melhorias no desempenho ao utilizar o Microsoft Word e o Excel;
* Maior estabilidade e melhorias de segurança, como suporte para extras com informações de compatibilidade de versão;
* Muitas outras correções de bugs.

Nota importante:
A partir desta versão do NVDA, appModules globalPlugins, brailleDisplayDrivers e synthDrivers personalizados já não serão carregados automaticamente a partir da pasta de configurações do utilizador do NVDA.
Em vez disso, esses módulos devem ser instalados como parte de um extra do NVDA.
Para quem desenvolve código para um extra, o código para teste pode ser colocado na nova pasta scratchpad dentro da pasta de configurações do utilizador do NVDA, se a opção "Activar carregamento de código da pasta Scratchpad" estiver ativada na nova secção Avançadas das Configurações do NVDA.
Estas alterações são necessárias para garantir melhor a compatibilidade do código personalizado, para que o NVDA não crache quando esse código se tornar incompatível com versões mais recentes.
Por favor, consulte a lista de alterações mais abaixo para obter mais detalhes sobre isto e como os os extras são mais controlados em relação às versões do NVDA.

### Novas funcionalidades

* Novas tabelas Braille: Árabe Braille de computador de 8 pontos, Árabe grau 2 e Espanhol grau 2. (#4435)
* Adicionada uma opção às configurações do rato do NVDA, para que o NVDA lide melhor com situações em que o rato é controlado por outra aplicação. (# 8452)
 * Isto permitirá que o NVDA siga o rato, mesmo quando o sistema estiver a ser controlado remotamente usando o TeamViewer ou outro software de controle remoto.
* Adicionado o parâmetro de linha de comando "--disable-start-on-logon" para permitir instalações silenciosas do NVDA que não são executadas, por padrão, na janela de logon. (# 8574)
* É possível desactivar os recursos de registo do NVDA definindo o nível de registo para "desactivado" no painel de configurações gerais. (# 8516)
* A presença de fórmulas nas folhas de cálculo do LibreOffice e do Apache OpenOffice passa a ser anunciada. (# 860)
* No Mozilla Firefox e Google Chrome, o modo de navegação agora anuncia o item selecionado em caixas de listas e estruturas hierárquicas.
 * Isto funciona no Firefox 66 e seguintes;
 * Isto não funciona para certas caixas de listas (HTML select controls) no Chrome.
* Adicionada a tabela Braille Africander. (#9186)
* Suporte inicial para aplicações como o Mozilla Firefox em computadores com processadores ARM64 (por exemplo, Qualcomm Snapdragon). (# 9216)
* Uma nova categoria de Configurações, Avançadas, foi adicionada ao diálogo Configurações do NVDA, incluindo uma opção para testar o novo suporte do NVDA para o Microsoft Word através da API  UI Automation da Microsoft. (# 9200)
* Adicionado suporte para a visualização gráfica na Gestão de Discos do Windows. (# 1486)
* Adicionado suporte às linhas Braille Handy Tech Connect Braille e Basic Braille 84. (#9249)

### Alterações

* Actualizado o conversor Braille liblouis para a versão 3.8.0. (#9013)
* O autor de um extras deve passar a indicar a versão mínima exigida do NVDA para que o extra funcione. O NVDA não instalará ou carregará um extra cuja versão mínima exigida do NVDA seja superior à versão actual do NVDA. (#6275)
* O autor de um extra deve passar a indicar a última versão do NVDA com que foi testado. Se um extra foi testado com uma versão do NVDA inferior à versão actual, o NVDA não instalará ou carregará o extra. (#6275)
* Esta versão do NVDA permitirá a instalação e o carregamento de extras que ainda não contenham informações sobre a versão mínima exigida e última testada do NVDA, mas a actualização para futuras versões do NVDA (por exemplo, 2019.2) poderá fazer com que esses extras mais antigos sejam desactivados.
* O comando Mover o rato  para o objeto de navegação está agora disponível no Microsoft Word, bem como para os controles UIA, especialmente o Microsoft Edge. (# 7916, #8371)
* O anúncio de texto sob o rato foi melhorado no Microsoft Edge e em outros aplicativos UIA. (# 8370)
* Quando o NVDA é iniciado com o parâmetro de linha de comando "--portable-path", o caminho fornecido é automaticamente preenchido ao tentar criar uma cópia portátil do NVDA usando o menu do NVDA. (# 8623)
* Actualizado o caminho para a tabela Braille norueguesa, para reflectir o padrão do ano de 2015. (# 9170)
* Ao navegar por parágrafo (control + setas) ou por células de tabela (control + alt + setas), a existência de erros ortográficos não será mais anunciada, mesmo que o NVDA esteja configurado para anunciá-los automaticamente. Isso ocorre porque os parágrafos e as células de tabela podem ser muito grandes, e o cálculo de erros de ortografia em alguns aplicativos pode ser muito demorado. (# 9217)
* O NVDA deixa de carregar, automaticamente, os appModules, globalPlugins e drivers de linhas Braille e de sintetizadores personalizados do diretório de configurações do utilizador do NVDA. Esse código deve ser incluido num extra, com as informações de versão corretas, garantindo que o código incompatível não seja executado com as versões actuais do NVDA. (# 9238)
 * Para os desenvolvedores que precisam de testar o código, enquanto está a ser desenvolvido, devem activar o diretório "scratchpad" do NVDA na categoria Avançadas das configurações do NVDA, e colocar o código no diretório "scratchpad" encontrado no diretório de configurações do NVDA, quando esta opção está activada.

### Correcções

* Windows OneCore voices do Windows 10 abril de 2018 e posteriores, grandes espaços de silêncio já não são inseridos entre instâncias de voz. (# 8985)
* Ao mover por caractere em controlos de texto sem formatação (como o Bloco de Notas) ou no modo de navegação, os caracteres emoji de 32 bits constituidos por dois pontos de código UTF-16 (como 🤦) passam a ser lidos correctamente. (#8782)
* O diálogo de confirmação de reinicialização após mudar idioma gve a sua interface melhorada. O texto e as etiquetas dos botões estão mais concisos e menos confusos. (# 6416)
* Se um sintetizador de terceiros não for carregado, o NVDA voltará a falar com o Windows OneCore Voices no Windows 10, em vez de falar com o eSpeake. (#9025)
* Removido o "Diálogo de boas-vindas" no menu do NVDA em janelas seguras. (# 8520)
* Ao navegar com Tab ou ao usar a navegação rápida no modo de navegação, as legendas nos painéis de guias passam a ser anunciadas de forma mais consistente. (# 709)
* O NVDA passa a anunciar alterações de seleção para determinados selecionadores de tempo, como no aplicativo Alarmes e Relógio. (# 5231)
* No Centro de Ação do Windows 10, o NVDA passa a anunciar as mudanças de estado ao alternar ações rápidas, como brilho e assistência de foco. (# 8954)
* No Centro de ação no Windows 10 de outubro de 2018 e anteriores, o NVDA passa a reconhecer o controle de ação rápida do brilho como um botão em vez de um botão de alternância. (# 8845)
* O NVDA volta a seguir o cursor, e a anunciar os caracteres excluídos, na edição de células e no diálogo Localizar do Microsoft Excel. (# 9042)
* Corrigida uma falha rara no modo de navegação no Firefox. (# 9152)- Fixed a rare browse mode crash in Firefox. (#9152)
* O NVDA deixa de falhar ao anunciar o foco de alguns controlos, quando recolhidos, nos frisos do Microsoft Office 2016.
* O NVDA deixa de falhar ao informar o contacto sugerido enquanto inserimos endereços em novas mensagens no Outlook 2016. (# 8502)
* As últimas teclas de routing das linhas eurobraille de 80 células já não colocam o cursor para uma posição no início ou logo após o início da nova linha. (#9160)
* A navegação em tabela na vista agrupada por conversação no Mozilla Thunderbird foi corrigida. (#8396)
* No Mozilla Firefox e no Google Chrome, a mudança para o modo de foco já funciona correctamente para determinadas caixas de lista e estruturas hierárquicas (onde a caixa de lista / estrutura hierárquica não é focável, mas os seus itens são). (#3573, #9157)
* O modo de navegação já é correctamente activado por padrão ao ler mensagens no Outlook 2016/365 se estiver a usar o suporte experimental ao UI Automation do NVDA para documentos do Word. (#9188)
* Passa a ser menos provável que o NVDA crache, de tal maneira que seja obrigado a terminar a sessão actual do Windows. (#6291)
* No Windows 10, actualização de outubro de 2018 e seguintes, ao abrir o histórico da área de transferência na nuvem, com a área de transferência vazia, o NVDA anunciará o status da área de transferência. (#9112)
* No Windows 10, actualização de outubro de 2018 e posteriores, ao procurar por emojis no painel de emojis, o NVDA anunciará os melhores resultados da pesquisa. (#9112)
* O NVDA já não pára na janela principal do Virtualbox 5.2 e superiores. (#9202)
* A velocidade de resposta no Microsoft Word ao navegar por linha, parágrafo ou células de tabela, foi bastante melhorada em alguns documentos. Relembramos que, para uma melhor performance, configure o Microsoft Word para a visualização de rascunho com alt+j,r após abrir um documento. (#9217) 
* No Mozilla Firefox e no Google Chrome, os alertas vazios deixam de ser anunciados. (# 5657)
* Melhorias significativas no desempenho ao navegar pelas células no Microsoft Excel, especialmente quando o livro contém comentários e/ou listas suspensas de validação. (# 7348)
* Já não é necessário desactivar a edição na célula nas opções do Microsoft Excel para termos acesso ao campo de edição de célula com o NVDA no Excel 2016/365. (# 8146)
* Corrigida uma paragem no Firefox, que acontecia às vezes, quando se usava a navegação rápida por marcas, se o extra Enhanced Aria estivesse em uso. (# 8980) 

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

Esta versão resolve um crash ao iniciar o NVDA, se o idioma da interface do NVDA estiver configurado para Aragonês. (#9089)

## 2018.4

Os destaques desta versão são:

* Melhorias na performance nas versões  recentes do Mozilla Firefox;
* anúncio de emojis com todos os sintetizadores;
* Anúncio do estado  respondida/Reencaminhada no Microsoft Outlook;
* Anúncio da distância às bordas superiores e esquerda da página no Microsoft Word;
* Muitas correcções de erros.

== Novas Funcionalidades ==
* Novas tabelas Braille: Chinês (China, Mandarin) grau 1 e grau 2. (#5553)
* O NVDA agora pode ler descrições de emoji, bem como outros caracteres que fazem parte do Repositório Unicode Common Locale Data Repository. (#6523)
* No Microsoft Word, a distância do cursor às bordas superior e esquerda da página pode ser anunciada pressionando NVDA+Delete do numérico. (#1939)
* No Google Sheets, com o modo braille ativado, o NVDA não anuncia mais 'selecionado' em todas as células ao mover o foco entre as células. (#8879)
* Adicionado suporte para o Foxit Reader e Foxit Phantom PDF (#8944)
* Adicionado suporte para o DBeaver database tool. (#8905)

### Alterações

* "Anunciar balões de ajuda" no diálogo Apresentação de Objectos foi renomeado para "Anunciar notificações" para incluir o anúncio de notificações (toast) no Windows 8 e seguintes. (#5789)
* No diálogo Teclado as caixas de verificação para activar/desactivar as teclas modificadoras do NVDA passam a estar numa lista, em vez de caixas de verificação separadas.
* O NVDA já não anuncia informação redundante ao ler o relógio na barra de notificações em algumas versões do Windows. (#4364)
* Actualizado o conversor Braille liblouis para a versão 3.7.0. (#8697)
* Atualizado o eSpeak-NG para o commit 919f3240cbb.

### Bug Fixes

* No Outlook 2016/365, os sinalizadores da categoria e do estado das mensagens já são anunciadas. (#8603)
* Quando o NVDA está configurado para idiomas como Kirgyz, Mongol ou Macedónio, já não apresenta um diálogo, no arranque, a avisar que o idioma não é suportado pelo sistema operativo. (#8064)
* O comando para mover o rato para o objecto de navegação move, com mais precisão, o rato para a posição actual no modo de navegação no Mozilla Firefox, Google Chrome and Acrobat Reader DC. (#6460)
* A interacção com caixas combbinadas no Firefox, Chrome e Internet Explorer foi melhorada. (#8664)
* Nas versões  Japonesas do Windows XP ou Vista, o NVDA já apresenta o aviso de requisitos de versão correctamente. (#8771)
* Melhorada a performance no Mozilla Firefox ao navegar por páginas grandes com várias alterações dinâmicas. (#8678)
* Já não é mostrado em Braille os atributos  do tipo de letra, se estiverem desactivados nas configurações de Formatação de Documentos. (#7615)
* O NVDA já não perde o foco no Explorador de ficheiros e outras aplicaçõess usando UI Automation quando outra aplicação está ocupada como, por exemplo, como ao processar grandes lotes de áudio). (#7345)
* Nos menus ARIA, na Web, a tecla Escape é passada para o menu e já não desativa o modo de foco incondicionalmente. (#3215)
* O NVDA já anuncia o foco em páginas Web onde o novo foco substitui um controlo que já não existe. (#6606, #8341)
* No novo GMail, ao usar as teclas de navegação rápida enquanto se lê mensagens, já não é anunciado todo o corpo da mensagem após o elemento para o qual se moveu. (#8887)
* Depois de actualizar o NVDA, navegadores como o Firefox e google Chrome já não devem crachar, e o modo de navegação  deve continuar a reflectir correctamente atualizações para os documentos actualmente carregados. (#7641) 
* O NVDA já não anuncia múltiplas vezes seguidas Clicável ao navegar por conteúdo clicável em modo de navegação. (#7430)
* Comandos executados numa baum Vario 40 já são executados. (#8894)
* No Google Slides com o Mozilla Firefox, o NVDA já não anuncia texto selecionado em todos os controlos em foco. (# 8964)

### Changes for Developers

* gui.nvdaControls now contains two classes to create accessible lists with check boxes. (#7325)
 * CustomCheckListBox is an accessible subclass of wx.CheckListBox.
 * AutoWidthColumnCheckListCtrl adds accessible check boxes to an AutoWidthColumnListCtrl, which itself is based on wx.ListCtrl.
* If you need to make a wx widget accessible which isn't already, it is possible to do so by using an instance of gui.accPropServer.IAccPropServer_impl. (#7491)
 * See the implementation of gui.nvdaControls.ListCtrlAccPropServer for more info.
* Updated configobj to 5.1.0dev commit 5b5de48a. (#4470)
* The config.post_configProfileSwitch action now takes the optional prevConf keyword argument, allowing handlers to take action based on differences between configuration before and after the profile switch. (#8758)

## 2018.3.2

Apenas para corrigir um bug que provocava falhas no Google Chrome ao navegar por tweetts em [www.twitter.com](http://www.twitter.com). (#8777)

## 2018.3.1

Apenas para corrigir um bug que provocava falhas na versão de 32 bit do Mozilla Firefox. (#8759)

## 2018.3

Os destaques desta versão são:

* Detecção automática de várias linhas Braille;
* Suporte para novas funcionalidades do Windows 10 tais como, o painel de introdução de Imojis do Windows 10.

== Novas Funcionalidades ==
* O NVDA passa a anunciar os erros gramaticais, quando reportados pelo Mozilla Firefox em páginas Web. (#8280)
* Conteúdo marcado como sendo inserido ou apagado, em páginas web, passa a ser anunciado no Google Chrome. (#8558)
* Adicionado suporte para as rodas de deslocamento dos BrailleNote QT e Apex BT, quando usados como linha Braille do NVDA. (#6316)
* Adicionado comando para anunciar o tempo total e já reproduzido da pista actual no Foobar2000. (#6596)
* O símbolo da tecla Comando do Mac (⌘) passa a ser anunciada ao ler texto com qualquer sintetizador. (#8366)
* Funções personalizadas via atributos aria-roledescription passam a ser suportados no Firefox, Chrome e Internet Explorer.
* Novas tabelas Braille: Checo 8 pontos, Kurdo Central, Esperanto, Húngaro e Sueco Braille informático de 8 pontos. (#8227)
* Adicionado suporte para detecção automática de linhas braille em segundo plano. (#1271)
 * São já suportadas as linhas ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, HandyTech, Hims, SuperBraille and HumanWare BrailleNote and Brailliant BI/B.
 * Pode activar esta funcionalidade, seleccionando "Automático" na opção "Linha Braille" do diálogo "Seleccionar linha Braille".
 * Por favor, consulte a documentação para mais informações.
* Adicionado suporte para várias formas modernas de introdução de texto, introduzidas em versões recentes do Windows 10. Estão incluidas o painel de emoji (update Fall Creators), ditado (Update Fall Creators), sugestões para o teclado de hardware (Update Abril 2018) e colar do cloud clipboard (Update Outubro 2018). (#7273)
* Conteúdo marcado como citação usando ARIA (role blockquote) passa a ser suportado no Mozilla Firefox 63. (#8577)

### Alterações

* A lista de idiomas disponíveis, na secção "Gerais" das configurações do NVDA, passa a ser ordenada pelo nome do idioma e não pelo código ISO 639. (#7284)
* Adicionados comandos padrão para simular o alt shift tab e windows tab em todas as linhas Braille da Freedom Scientific suportadas. (#7387)
* Para as linhas Braille da ALVA, BC680 e protocol converter, já é possível associar funções diferentes para as teclas smart pad, thumb e etouch  da esquerda e direita. (#8230)
* Para as linhas Braille ALVA BC6, a combinação sp2+sp3 anunciará a data e hora, enquanto que sp1+sp2 simulará a tecla Windows. (#8230)
* O utilizador será questionado, apenas uma vez, no arranque do NVDA se permitem o envio de dados de utilização para a NV Access, ao verificar automaticamente por actualizações. (#8217)
* Ao verificar por actualizações, se o utilizador concordou com a recolha de dados de utilização pela NV Access, o NVDA irá enviar o nome dos drivers do sintetizador e da linha Braille em uso, para ajudar na melhor prioritização do trabalho futuro nesses drivers. (#8217)
* Actualizado o conversor Braille Liblouis para a versão 3.6.0. (#8365)
* Actualizado o caminho para a tabela Braille correcta Russo 8 pontos. (#8446)
* Actualizado o eSpeak-ng to 1.49.3dev (commit 910f4c2). (#8561)

### Correções

* As etiquetas acessíveis de controlos no Google Chrome, quando não fazem parte do conteúdo, são anunciadas mais prontamente em modo de navegação. (#4773)
* As notificações já são suportadas no Zoom. Por exemplo, estado mute/unmute e mensagens recebidas. (#7754)
* Alternar o contexto seguido pela linha Braille em modo de navegação já não provoca a paragem da alternância automática do contexto do Braille. (#7741)
* As linhas Braille ALVA BC680 já não falham, intermitentemente, a inicialização. (#8106)
* Por padrão, as linhas ALVA BC6 já não executam a simulação de teclas do sistema ao pressionar combinações de teclas envolvendo sp2+sp3 para activar funcionalidades internas. (#8230)
* Pressionar sp2 numa linha ALVA BC6 para simular a tecla alt já funciona como previsto. (#8360)
* O NVDA já não anuncia alterações de esquema de teclado redundantes. (#7383, #8419)
* O seguimento do rato é agora mais preciso no Notepad e noutros controlos de edição de texto simples, num documento com mais de 65535 caracteres. (#8397)
* O NVDA passa a reconhecer mais diálogos do Windows 10 e de outras aplicações modernas. (#8405)
* Na actualização de Outubro de 2018 do Windows 10, Server 2019 e seguintes, o NVDA já não perde o seguimento do foco quando uma aplicação congela ou perde o foco. (#7345, #8535)
* O utilizador passa a ser informado se tentar ler ou copiar o conteúdo da barra de estado quando esta se encontrar vazia. (#7789)
* Corrigida a situação em que o estado "Não marcado" de uma caixa de verificação não é anunciado por voz se antes estava parcialmente marcada. (#6946)
* Na lista de idiomas no diálogo Gerais das configurações do NVDA o nome do idioma Birmanês é corretamente anunciado em Windows 7. (#8544)
* No Microsoft Edge, o NVDA passa a anunciar as notificações, tais como a disponibilidade da Vista de leitura ou o progresso de carregamento da página. (#8423)
* Tal como noutros campos de texto multilinha, quando o foco está posicionado no início do texto de um documento, o texto na linha Braille, é posicionado de maneira a que o primeiro caracter do texto ocupe a primeira célula da linha. (#8406)
* Ao navegar numa página, quando se entra numa lista, o NVDA anunciará o nome da lista, se ele foi indicado pelo autor da página. (#7652)
* Ao associar, manualmente, comandos a teclas, para uma linha Braille específica, essas teclas passarão a aparecer como associadas para essa linha, e não para a linha activa no momento. (#8108)
* A versão de 64-bit do Media Player Classic já é suportada. (#6066)
* Melhoramentos no suporte Braille no Microsoft Word com UI Automation activada:
 * Reduzida a verbosidade da apresentação do foco quer em voz quer em Braille, ao focar um documento do Word. (#8407)
 * As teclas routing da linha Braille já funcionam correctamente numa lista de um documento Word. (#7971)
 * As marcas e os números introduzidos num documento Word já são correctamente anunciados em voz e Braille. (#7970)
* No Windows 10 1803 e seguintes, já é possível instalar extras mesmo com a funcionalidade de suporte a  Unicode UTF-8 activa. (#8599)

### Alterações para Desenvolvedores

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

Esta versão apenas corrige alguns problemas de tradução, devido à remoção de uma funcionalidade com problemas.

## 2018.2

Os destaques desta versão são:

* Suporte para tabelas no Kindle for PC;
-  suporte para as linhas Braille BrailleNote Touch e BI14  da Humanware;
* Melhorias nos sintetizadores Windows OneCore e Sapi5;

### Novas Funcionalidades

* A expansão de linhas e colunas numa célula de tabela passa a ser anunciada em voz e Braille. (#2642)
* Os comandos de navegação em tabelas do NVDA já são suportados no Google Docs, com o modo Braille activado. (#7946)
* Possibilidade de ler e navegar por tabelas no Kindle para PC. (#7977)
* Suporte para as linhas BrailleNote touch e Brailliant BI 14 via USB e Bluetooth. (#6524)
* No Windows 10 Fall Creators Update e seguintes, o NVDA já anuncia as notificações de aplicações como a Calculadora e a Loja. (#8045)
* Novas tabelas de conversão Braille: Lituano 8 pontos, Ucraniano, Mongol grau 2. (#7839)
* Introduzido um comando para anunciar as informações de formatação do caracter numa célula Braille. (#7106)
* Ao actualizar o NVDA, já é possível adiar a instalação da versão descarregada para um momento mais opurtuno. (#4263) 
* Novos idiomas: Mongol e Alemão da Suiça.
* Pode agora manter pressionadas, virtualmente, as teclas control, shift, alt, windows e NVDA, a partir do teclado da linha Braille e combinar esses modificadores com letras escritas no teclado Braille, (por exemplo, pressionar Control+s). (#7306);
 * Pode associar estas funcionalidades a comandos através da opção Definir comandos, Simulação de teclas do sistema.
* Reposto o suporte para as linhas Braille Braillino e Modular da HandyTech com firmware antigo. (#8016)
* Nos dispositivos HandyTech suportados, como Active Braille e Active Star, a data e hora serão automaticamente sincronizadas pelo NVDA, sempre que a diferença for superior a cinco segundos. (#8016)
* Pode ser definido um comando para desactivar temporariamente todos os accionadores de perfis. (#4935)

### Alterações

* Os valors da coluna "Estado" do Gestor de extras foi alterado de "Em execução" e "Suspenso", para "Activado" e Desactivado" . (#7929)
* Foram também introduzidos mais dois estados, "Activado após reinício" e "Desactivado após reinício". (#7929)
* Actualizado o liblouis braille translator para a versão 3.5.0. (#7839)
* A tabela Braille Lituano foi renomeada para Lituano 6 pontos, para evitar confusão com a nova tabela de 8 pontos. (#7839)
* As tabelas Braille Francês (Canadá) grau 1 e grau 2 foram removidas. Passam a ser usadas Francês (unificado) braille de computador de 6 pontos e Grau 2, respectivamente. (#7839)
* Os botões da  linha secundária de routing das linhas Braille Alva BC6, EuroBraille e Papenmeier passam a anunciar a informação de formatação do caracter respectivo. (#7106)
* As tabelas de conversão Braille contraído passarão automaticamente para Braille não contraído quando não se está num campo de edição, como controlos onde não haja cursor ou em modo de navegação. (#7306)
* O NVDA está menos falador quando um evento ou um horário no calendário  do Outlook ocupa um dia inteiro. (#7949)
* Todas as opções do NVDA estão agora agrupadas num diálogo de configurações no menu Opções do NVDA, em vez de estarem espalhadas por vários diálogos. (#7302)
* O sintetizador padrão do NVDA, quando executado em Windows 10, passa a ser o Windows OneCore voices, em vez do eSpeak. (#8176)

### Correções

* O NVDA já lê sempre os controlos em foco da janela de login da conta Microsoft após ser introduzido o endereço de e-mail. (#7997)
* O NVDA já não deixa de ler o conteúdo de uma página quando se retrocede para a mesma no Microsoft Edge. (#7997)
* O NVDA já não anuncia, incorrectamente, o último caracter da password, na janela de login do windows 10, ao desbloquear o PC. (#7908)
* As etiquetas de caixas de verificação e botões de rádio já não são anunciadas em duplicado no Chrome e Firefox, ao navegar com Tab ou por caracteres em modo de navegação. (#7960)
* Tratar aria-current com o valor de false como false em vez de true (#7892).
* O driver do sintetizador Windows OneCore Voices já não deixa de carregar pela remoção de uma voz configurada. (#7999)
* A alteração de voz no driver do sintetizador Windows OneCore Voices é agora muito mais rápida. (#7999)
* Corrigidos erros na saída Braille em diversas tabelas Braille, incluindo o sinal de maiúsculas em dinamarquês de 8 pontos. (#7526, #7693)
* O NVDA passa a anunciar mais tipos de bullets no Microsoft Word. (#6778)
* Ao pressionar o comando para anúncio de informações de formatação, a posição de revisão já não é alterada, e por isso já não são fornecidas falsas informações ao pressionar o comando mais de uma vez. (#7869)
* A escrita em Braille já não permite Braille contraído onde não seja suportado, ou seja, as palavras completas só serão enviadas ao sistema em áreas editáveis. (#7306)
* Corrigidos problemas de estabilidade nas ligações das linhas Braille HandyTech Easy Braille e Braille Wave. (#8016)
* Em Windows 8 ou superior, o NVDA já não anunciará "Desconhecido" ao abrir  o menu rápido )Windows+X) e ao seleccionar itens desse menu. (#8137)
* Os comandos específicos de modelos relativos aos botões das linhas Braille da HIMS já funcionam como referido no respectibo manual. (#8096)
* O NVDA passa a tentar corrigir os problemas de registo de DLLs do sistema, causadores de programas como o Firefox e Internet Explorer ficarem parcialmente inacessíveis, causando o anúncio de "Desconhecido" pelo NVDA. (#2807)
* Torneado um bug no Gestor de Tarefas que fazia com que o NVDA impedisse o utilizador de acessar conteúdo de alguns detalhes sobre processos. (#8147)
* As novas vozes Microsoft SAPI5 já não apresentam pausas no fim da fala, sendo assim muito mais eficiente navegar com essas vozes. (#8174)
* O NVDA já não anuncia marcas (LTR e RTL em Braille ou em voz por-caractere, ao acessar o relógio de versões recentes do Windows. (#5729)
* A detecção das teclas de deslocação da linha Smart Beetle  da HIMS volta a ser confiável. (#6086)
* Em alguns controlos de texto, especialmente em aplicações Delphi as informações sobre edição e navegação já é muito mais confiável. (#636, #8102)
* Em Windows 10 RS5, o NVDA já não anuncia informação redundante ao mudar de janela com alt+tab. (#8258)

### Alterações para Desenvolvedores

* The developer info for UIA objects now contains a list of the UIA patterns available. (#5712)
* App modules can now force certain windows to always use UIA by implementing the isGoodUIAWindow method. (#7961)
* The hidden boolean flag "outputPass1Only" in the braille section of the configuration has again been removed. Liblouis no longer supports pass 1 only output. (#7839)

## 2018.1.1

Esta é uma versão especial do NVDA 2018.1 para resolver um problema do driver do sintetizador Windows OneCore voices, que provocava um aumento da entoação e velocidade no Windows 10 Redstone 4 (1803). (#8082)  

## 2018.1

Os destaques desta versão são:

* Suporte para gráficos no Microsoft word e PowerPoint
* Suporte para mais linhas Braille, Eurobraille e Optelec ALVA protocol converter
* Suporte melhorado para as linhas Braille HIMS e Optelec
* Melhorias no desempenho do NVDA no Mozilla Firefox 58 e superiores.

### Novas Funcionalidades

* Já é possível interagir com gráficos no Microsoft Word e Microsoft PowerPoint, de maneira similar ao suporte existente para gráficos no Microsoft Excel. (#7046)
 * No Microsoft Word: Em modo de navegação, navegue com o cursor para um gráfico embutido e pressione Enter  para iniciar a interacção com o gráfico;
 * No Microsoft PowerPoint durante a edição de um slide: Navegue com Tab para um objecto gráfico,  e pressione Enter ou Espaço para iniciar a interacção com esse gráfico;
 * Para terminar a interacção com um gráfico, pressione Escape.
* Novo idioma: Quirguiz.
* Adicionado suporte para VitalSource Bookshelf. (#7155)
* Adicionado suporte para o Optelec protocol converter, um dispositivo que permite usar as linhas Braille Voyager e Satellite com o protocolo de comunicações das ALVA BC6. (#6731)
* Já é possível escrever em Braille com as linhas Braille ALVA 640 Comfort. (#7733) 
 * A funcionalidade de escrita Braille do NVDA pode ser usada com este modelo e com outros da série BC6 com o firmware 3.0.0 ou superior.
* Suporte parcial para o Google Sheets com o modo Braille activado. (#7935)
* Suporte para as linhas Braille Eurobraille Esys, Esytime and Iris. (#7488)

### Alterações

* Os drivers das linhas Braille da HIMS, Braille Sense/ Braille Edge/Smart Beetle e HIMS Sync Braille, foram substituídos por um único driver do NVDA. O novo driver será activado automaticamente para os utilizadores do antigo driver syncBraille. (#7459)
 * Algumas teclas, nomeadamente as teclas de deslocamento, foram alteradas, para seguir as convenções usadas pelos produtos da HIMS. Consulte o Manual do Utilizador, para obter mais detalhes.
* Quando se escreve com o teclado virtual através da interacção por toque, por padrão, é necessário dar dois toques para activar a letra desejada, tal como em qualquer outro controlo.
 * Para usar o modo existente, em que basta levantar o dedo para activar a letra, active a opção nas novas definições da Interação por toque, presente no menu Preferências. (#7309)
* Já não é necessário configurar se o braille segue o cursor do sistema ou da revisão, pois a configuração será feita automaticamente por padrão. (#2385) 
 * Note que o seguimento automático do cursor de revisão só acontecerá quando se utiliza o cursor de revisão ou um comando de navegação por objectos.

### Correções

* As mensagens navegáveis, como a informação de formatação, quando se pressiona NVDA+f duas vezes, já não falha quando o NVDA está instalado numa pasta com caracteres não ASCII. (#7474)
* O foco é novamente restaurado correctamente quando se volta ao Spotify de outra aplicação. (#7689)
* O NVDA já pode ser actualizado num sistema com o Acesso controlado a Pastas activado (disponível no Windows 10 Fall Creators update). (#7696)
* Uma pequena melhoria na performance ao renderizar grandes conteúdos no Mozilla Firefox 58 e seguintes. (#7719)
* Evitados erros ao ler e-mails contendo tabelas, no Microsoft Outlook (#6827)
* A detecção das teclas de deslocamento da linha Braille HIMS Smart Beetle já é fiável. (#6086)
* Os comandos dados pelas linhas Braille que emulam teclas modificadoras de sistema, já podem ser combinados com outras teclas de sistema emuladas, se um ou mais dos comando involvidos for específico do modelo. (#7783)
* No Mozilla Firefox, o Modo de navegação já funciona correctamente em janelas pop-up criadas por extensõess como LastPass e bitwarden. (#7809)
* O NVDA já não tem paragens ocasionais de cada vez que há mudanças de foco no Firefox ou Chrome devidas a paragens ou crashes. (#7818)
* Em clientes twitter, como Chicken Nugget, o NVDA já não ignora os últimos 20 caracteres ao ler tweets  com 280 caracteres. (#7828)
* O NVDA já usa o idioma correcto ao anunciar símbolos e pontuação ao seleccionar texto. (#7687)
* Em versões recentes do Office 365, volta a ser possível navegar com as setas nos gráficos do Excel. (#7046)
-  Em voz e em Braille, o estado dos controlos são sempre anunciados na mesma ordem, independentemente de serem positivos ou negativos. Corrige o bug #7076
* Em aplicações como o Windows 10 Mail, o NVDA já anuncia os caracteres apagados com backspace. (#7456)
* Todas as teclas do HIMS Braille Sense Polaris já funcionam como esperado. (#7865)

### Alterações para Desenvolvedores

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

Os destaques desta versão incluem:

* Muitas correções e melhorias no suporte Web, incluindo modo de navegação, por padrão, , para os diálogos web e melhor anúncio das etiquetas de grupo de campos, no modo de navegação;
* Suporte para as novas tecnologias do Windows 10, como o Windows Defender Application Guard e Windows 10 em ARM64;
* Anúncio automático da orientação do ecrã e estado da bateria.
* Atenção, esta versão do NVDA já não dá suporte ao Windows XP nem ao Windows Vista! O requisito mínimo para esta versão do NVDA é agora o Windows 7, Service Pack 1.

### Novas Funcionalidades

* Em modo de navegação, já é possível saltar para o início de uma região usando o comando (vírgula/shift+vírgula) para saltar para o início ou fim de um contentor. (#5482)
* No Firefox, Chrome e Internet Explorer, a navegação por caractere para campos de formulário e de edição passa a incluir os campos editáveis de Rich Text (I.e. contentEditable). (#5534)
* Nos navegadores web a Lista de Elementos já pode listar os campos de formulários e botões. (#588)
* Suporte inicial para o Windows 10 em ARM64. (#7508)
* Suporte inicial para leitura e navegação interactiva de conteúdo matemático nos livros Kindle com conteúdo matemático acessível. (#7536)
* Adicionado suporte para o leitor de E-Books Azardi. (#5848)
* Informação da versão dos Extras é agora anunciada ao actualizá-los. (#5324)
* Adicionado novo parâmetro à linha de comandos para criar uma cópia portátil do NVDA. (#6329)
* Suporte para o Microsoft Edge em execução através do Windows Defender Application Guard no Windows 10 Fall Creators Update. (#7600)
* Quando executado num computador portátil ou tablet, o NVDA já anuncia quando o carregador é ligado ou desligado, incluindo o nível da bateria, e quando a orientação do ecrã muda. (#4574, #4612)
* Novo idioma: Macedónio.
* Novas tabelas Braille: Croata grau 1 e Vietnamita grau 1. (#7518, #7565)
* Adicionado suporte para a linha Braille Actilino da HandyTech. (#7590)
* Já é suportada a introdução de texto pelas linhas Braille da HandyTech. (#7590)

### Alterações

* O sistema operativo mínimo suportado pelo NVDA passa a ser o Windows 7 Service Pack 1, ou Windows Server 2008 R2 Service Pack 1. (#7546)
* Os diálogos Web no Firefox e Chrome usam automáticamente o Modo de navegação, excepto se dentro duma aplicação web. (#4493)
* Em Modo de navegação, navegando com Tab ou por caracteres já não é anunciada a saída de listas ou tabelas, tornando assim a navegação mais fluída. (#2591)
* Em Modo de navegação no Firefox e Chrome, o nome do grupo de campos de formulários já é anunciado quando são atingidos pela navegação por caracteres ou com Tab. (#3321)
* Em Modo de navegação, usando a navegação por caracteres, o comando para objectos, (o e shift+o) passa a incluir os elementos de áudio e de vídeo e elementos com aria roles application e dialog. (#7239)
* O Espeak-ng foi actualizado para a versão 1.49.2, resolvendo alguns problemas ao produzir novas versões. (#7385, #7583)
* Pressionando três vezes o comando para ler a barra de estado, a informação é copiada para a área de transferência. (#1785)
* Ao associar comandos a teclas duma linha Braille da Baum pode limitá-los ao modelo específico em uso, (p.e. VarioUltra ou Pronto). (#7517)
* O atalho para a opção "Filtrar por:" na Lista de elementos no Modo de navegação mudou de alt+F para alt+P. (#7569)
* Um comando, sem teclas associadas, foi adicionado ao Modo de navegação, para alternar rapidamente a inclusão das tabelas de apresentação. Pode associar teclas a este comando no diálogo Definir comandos, grup Modo de navegação. (#7634)
* Actualizado o liblouis braille translator to 3.3.0. (#7565)
-  Os ficheiros dos Dicionários de voz passam a ser versionados e foram movidos para a pasta 'speechDicts/voiceDicts.v1'. (#7592)
* As alterações aos ficheiros versionados (configurações do utilizador e  dicionários de voz), já não são guardadas se estiver a executar o NVDA a partir do executável. (#7688)
* As linhas Braille Braillino, Bookworm e Modular, com firmware) antigo, da HandyTech) já não são suportadas automaticamente, sendo necessário instalar o Driver Braille Universal e o Extra do NVDA da HandyTech, para as usar. (#7590)

### Correções

* Os links passam a ser indicados em Braille em aplicações como o Microsoft Word. (#6780)
* O NVDA já não se torna notoriamente lento quando muitos separadores estão abertos nos navegadores Firefox ou Chrome. (#3138)
* Nas linhas Braille MDV Lilli os cursores de toque já não movem o cursor para a célula seguinte. (#7469)
* No Internet Explorer e noutros documentos MSHTML, o atributo HTML5 necessário para indicar o estado de um campo de formulário passa a ser suportado. (#7321)
* O Braille passa a ser actualizado quando se está a escrever caracteres árabes num documento do WordPad alinhado à esquerda. (#511)
* As etiquetas acessíveis para controlos no Mozilla Firefox passam a ser anunciadas mais rapidamente em Modo de navegação quando a etiqueta não aparece como conteúdo. (#4773)
* No Windows 10 Creators Update, o NVDA volta a poder aceder ao Firefox após ter sido reiniciado. (#7269)
* Ao reiniciar o NVDA com o Mozilla Firefox em primeiro plano, o Modo de navegação volta a estar disponível, embora talvez necessite de fazer alt+tab e voltar ao Firefox. (#5758)
* Já é possível aceder ao conteúdo matemático no Google Chrome num sistema sem o Mozilla Firefox instalado. (#7308)
* O Sistema operativo e outras aplicações devem ficar mais estáveis, imediatamente após a instalação do NVDA e antes de reiniciar o sistema, em comparação com a instalação de versões anteriores do NVDA. (#7563)
* Ao usar um comando de reconhecimento de conteúdo, como NVDA+r), o NVDA anunciará uma mensagem de erro, em vez de ficar em silêncio, se o objecto de navegação tiver desaparecido. (#7567)
* A funcionalidade de deslocamento da linha para trás  foi corrigida para as linhas Braille da Freedom Scientific que possuem uma left bumper bar. (#7713)

### Alterações para desenvolvedores

* "scons tests" now checks that translatable strings have translator comments. You can also run this alone with "scons checkPot". (#7492)
* There is now a new extensionPoints module which provides a generic framework to enable code extensibility at specific points in the code. This allows interested parties to register to be notified when some action occurs (extensionPoints.Action), to modify a specific kind of data (extensionPoints.Filter) or to participate in deciding whether something will be done (extensionPoints.Decider). (#3393)
* You can now register to be notified about configuration profile switches via the config.configProfileSwitched Action. (#3393)
* Braille display gestures that emulate system keyboard key modifiers (such as control and alt) can now be combined with other emulated system keyboard keys without explicit definition. (#6213) 
 * For example, if you have a key on your display bound to the alt key and another display key to downArrow, combining these keys will result in the emulation of alt+downArrow.
* The braille.BrailleDisplayGesture class now has an extra model property. If provided, pressing a key will generate an additional, model specific gesture identifier. This allows a user to bind gestures limited to a specific braille display model. 
 * See the baum driver as an example for this new functionality.
* NVDA is now compiled with Visual Studio 2017 and the Windows 10 SDK. (#7568)

## 2017.3

Os destaques desta versão são:

* Possibilidade de escrever em Braille abreviado;
* Suporte para as novas vozes Windows OneCore disponíveis no Windows 10;
* Suporte nativo para o OCR do Windows 10;
* Muitas melhorias significativas no que respeita ao Braille e à Web.

### Novas Funcionalidades

* Adicionado  um parâmetro nas definições Braille para permitir mostrar as mensagens indefinidamente. (#6669)
* Na lista de mensagen do Microsoft Outlook passa a ser anunciado se uma mensagem está sinalizada. (#6374)
* Ao editar um slide no Microsoft PowerPoint, o tipo exacto de forma passa a ser anunciado, por exemplo triângulo, círculo, vídeo ou seta, em vez de apenas "forma". (#7111)
* Passa a ser suportado, no Google Chrome, conteúdo matemático, se apresentado em MathML. (#7184)
* O NVDA pode agora utilizar as novas vozes Windows OneCore (também conhecidas por Microsoft Mobile voices) incluídas no Windows 10. Pode utilizá-las seleccionando Windows OneCore voices na janela Sintetizadores do NVDA. (#6159)
* O NVDA pode guardar as configurações do utilizador na pasta appdata\local em alternativa a appdata\roaming. Isto pode ser configurado através de uma entrada no Registo do Windows. Leia mais na secção "Parâmetros do Sistema" no Manual do Utilizador. (#6812)
* Nos navegadores Web, o NVDA agora anuncia os valores dos placeholder para campos (mais especificamente, os aria-placeholder  passam a ser suportados). (#7004)
* No modo de navegação no Microsoft Word, já é possível navegar pelos erros ortográficos usando as teclas de navegação rápida W ou Shift+W. (#6942)
* Adicionado suporte para o controlo de escolha de data do evento no Microsoft Outlook. (#7217)
* A sugestão seleccionada passa a ser anunciada nos campos Para:, CC: e BCC: do Correio do Windows 10 e no campo de  pesquisa das definições do Windows 10. (#6241)
* Agora passa a ser reproduzido um som para anunciar que uma sugestão foi apresentada em certos campos de pesquisa, tais como na pesquisa do menu Iniciar, das definições do Windows 10, e campos Para:, CC; e BCC: do correio do Windows 10. (#6241)
* Anúncio automático das notificações do Skype for Business Desktop, tais como quando alguém inicia uma conversa. (#7281)
* Anúncio automático das notificações do Microsoft Edge, tais como quando começa um download.  (#7281)
* Já pode escrever Braille abreviado usando o teclado Braille da sua linha Braille. Para mais informações, por favor, leia a secção correspondente do Manual do utilizador. (#2439)
* Já pode introduzir caracteres Braille Unicode, a partir do teclado Braille da linha Braille, seleccionando a tabela Braille Unicode como tabela de escrita na janela Definições do Braille. (#6449)
* Adicionado suporte para a linha Braille SuperBraille usada em Taiwan. (#7352)
* Novas tabelas Braille: Dinamarquês Braille informático 8 pontos, Lituano, Persa Braille informático 8 pontos, Persa grau 1, Esloveno Braille informático 8 pontos. (#6188, #6550, #6773, #7367)
* Melhorada a tabela Inglês (Estados Unidos) Braille informático 8 pontos, incluindo suporte para bullets, símbolo do Euro e letras acentuadas. (#6836)
* O NVDA já pode usar a funcionalidade de OCR incluida no Windows 10 Creator para reconhecer texto em imagens ou em aplicações não acessíveis. (#7361)
 * O idioma de reconhecimento pode ser configurado pela nova opção do menu Preferências, Windows 10 OCR;
 * Para reconhecer o conteúdo do objeto de navegação actual, pressione NVDA+R;
 * Para mais informações, por favor, leia a nova secção sobre esta funcionalidade no Manual do utilizador.
* Já pode escolher a informação contextual que é mostrada na linha Braille quando um objecto recebe o foco, usando o novo parâmetro "Apresentação do contexto do foco", na janela de  Definições do Braille. (#217)
 * Por exemplo, as opções "Mostrar máximo de alterações de contexto" e "Mostrar apenas informação de contexto ao deslocar a linha para a esquerda", tornam a leitura de listas e menus mais eficientes, já que os itens não mudarão de posição na linha Braille.
 * Para mais informações, por favor, leia a nova secção sobre esta funcionalidade no Manual do utilizador.
* No Firefox e Chrome, o NVDA agora suporta grelhas dinâmicas complexas, tais como folhas de cálculo onde apenas algum do conteúdo é mostrado, mais concretamente com atributos aria-rowcount, aria-colcount, aria-rowindex e aria-colindex, introduzidos em ARIA 1.1). (#7410)

### Alterações

* Um comando, sem tecla associada (script_restart), foi adicionado para permitir o reinício do NVDA. (#6396)
* O Esquema de teclado a utilizar pode agora ser definido na janela Bem vindo ao NVDA. (#6863)
* Os nomes das marcas são abreviados em Braille como se segue: (#3975)
 * "landmark": "mrc"
 * "banner": "bnr"
 * "complementary": "cmp"
 * "contentinfo": "inf"
 * "main": "pri"
 * "navigation": "nav"
 * "search": "psq"
 * "form": "frm"
 * "region": "reg"
 * Exemplo: Marca de navegação ficará "mrc nav"
* Actualizado o eSpeak NG para a versão 1.49.1. (#7280)
* As listas das tabelas Braille, de leitura e de escrita, na janela de Definições do Braille passaram a ser ordenadas alfabeticamente. (#6113)
* Actualizado o liblouis braille translator para a  versão 3.2.0. (#6935)
* A tabela Braille predefinida passa a ser a Código Braille Unificado Inglês grau 1. (#6952)
* Por padrão, o NVDA passa a mostrar, na linha Braille, apenas a parte da informação contextual alterada quando um objecto recebe o foco. (#217)
 * Antes, mostrava o máximo possível de informação contextual, independentemente dessa informação já ter sido mostrada ou não;
 * Pode voltar ao comportamento anterior, alterando o novo parâmetro "Apresentação do contexto do foco", na janela de Definições do Braille, para ocupar toda a linha.
* Se usa Braille, o aspecto do cursor pode ser configurado para ser diferente quando segue o "foco" ou quando segue o "Cursor de revisão". (#7112)
* Actualizado o logotipo do NVDA. (#7446)

### Correções

* os elementos div editáveis no Chrome já não têm a sua etiqueta anunciada como se fosse o conteúdo em modo de navegação. (#7153)
* Pressionar end em modo de navegação num documento vazio do Microsoft Word já não provoca um erro de runtime. (#7009)
* O modo de navegação é agora correctamente suportado no Microsoft Edge quando um documento tenha um ARIA role de documento. (#6998)
* Em modo de navegação, já pode seleccionar ou desseleccionar até ao fim da linha, usando Shift+End, mesmo que o cursor esteja no último caracter da linha. (#7157)
* Se uma janela contiver uma barra de progresso, o texto da janela passa a ser actualizado em Braille, quando a mesma é alterada. Isto significa, por exemplo, que o tempo restante pode agora ser lido em Braille na janela de download da actualização do NVDA. (#6862)
* O NVDA passa a anunciar as mudanças de selecção para certas caixas combinadas do Windows 10, tais como AutoPlay em Definições. (#6337).
* Já não é anunciada informação desnecessária ao entrar na janela de criação de eventos/reuniões no Microsoft Outlook. (#7216)
* Só serão emitidos bips para barras de progressão indeterminadas, como as da janela de download das actualizações do NVDA, se a configuração do "Anúncio da barra de progresso" incluir os bips. (#6759)
* No Microsoft Excel 2003 e 2007, as células são novamente anunciadas ao navegar uma folha de cálculo com as setas. (#7243)
* No Windows 10 Creators Update e seguintes o modo navegação é novamente ativado automaticamente ao ler uma mensagem no Correio do Windows 10. (#7289)
* Na maioria das linhas Braille com teclado Braille, o ponto 7 apaga o último caracter digitado e o ponto 8 simula o pressionar do Enter. (#6054)
* Num texto editável, quando movemos o cursor de inserção, por exemplo com as setas ou Backspace, o que é anunciado pelo NVDA será mais preciso, particularmente no Chrome e em aplicações tipo terminal. (#6424)
* O conteúdo do Editor de assinaturas no Microsoft Outlook 2016 já é lido. (#7253)
* Em aplicações Java Swing, o NVDA já não provoca ocasionais crashes ao navegar por tabelas. (#6992)
* No Windows 10 Creators Update, o NVDA já não repetirá o anúncio das notificações toast. (#7128)
* No menu Iniciar do Windows 10, ao pressionar Enter para o fechar após uma pesquisa, o NVDA já não anunciará o texto da pesquisa. (#7370)
* A navegação por títulos no no Microsoft Edge é agora significativamente mais rápida. (#7343)
* No Microsoft Edge, navegar em moddo de navegação já não salta partes do texto de certas páginas, como as  do tema 2015 do Wordpress. (#7143)
* No Microsoft Edge, as marcas passam a ser anunciadas correctamente no idioma do Windows. (#7328)
* O Braille segue correctamente a selecção de texto mesmo quando é ultrapassada a dimensão da linha Braille. Por exemplo, se seleccionar várias linhas com Shift+Seta abaixo, o braille agora mostra a última linha seleccionada. (#5770)
* No Firefox, o NVDA já não anuncia, erroneamente, várias vezes "Secção" ao abrir os detalhes de um tweet no twitter.com. (#5741)
* No Modo de navegação, os comandos  de navegação em tabelas passam a só estar disponíveis em tabelas de formatação se o seu anúncio estiver activado. (#7382)
* No Firefox e Chrome, no Modo de navegação, os comandos  de navegação em tabelas passam a ignorar as células ocultas. (#6652, #5655)

### Alterações para desenvolvedores

* Timestamps in the log now include milliseconds. (#7163)
* NVDA must now be built with Visual Studio Community 2015. Visual Studio Express is no longer supported. (#7110)
 * The Windows 10 Tools and SDK are now also required, which can be enabled when installing Visual Studio.
 * See the Installed Dependencies section of the readme for additional details.
* Support for content recognizers such as OCR and image description tools can be easily implemented using the new contentRecog package. (#7361)
* The Python json package is now included in NVDA binary builds. (#3050)

## 2017.2

Os destaques desta versão são:

* Suporte total à diminuição de volume no Windows 10 Creators Update;
* Correcções diversas a problemas de selecção em páginas Web, no modo de navegação, incluindo Seleccionar tudo;
* Melhorias significativas no suporte ao Microsoft Edge;
* Melhoramentos no suporte a páginas Web, tais como indicação de elementos marcados como atual (usando aria-current).

### Novas Funcionalidades

* Informações sobre as linhas de grelha das células passam a poder ser anunciadas no Microsoft Excel, usando NVDA + f. (#3044)
* Adicionado suporte para "Aria-current attributes". (#6358)
* Adicionado suporte à mudança automática de idiomas no Microsoft Edge. (#6852)
* Adicionado suporte à Calculadora do Windows 10 Enterprise LTSB (Long-Term Servicing Branch) e Server. (#6914)
* Ao executar, três vezes rapidamente, o comando "Anunciar linha do objecto de navegação, 8 do numérico, a linha é soletrada com descrição dos caracteres. (#6893)
* Novo idioma: Birmanês.
* Os caracteres Unicode Seta acima e abaixo e símbolos de fracções passam a ser anunciados correctamente. (#3805)

### Alterações

* Ao navegar por aplicações, com UI Automation,, usando a navegação simples, mais controlos sem conteúdo são ignorados, tornando a navegação mais fácil. (#6948, #6950) 

### Correcções

* Itens de menu (como caixas de verificação e botões de opção) em páginas Web já podem ser activados no modo de navegação. (#6735)
* O anúncio do nome de folhas do Excel já se encontra traduzido. (#6848)
* Pressionar Escape na janela para confirmação de eliminação de um perfil activo passa a fechar a janela. (#6851)
* Corrigidos alguns travamentos no Mozilla Firefox e outras aplicações baseadas em Gecko nas quais o multi-processamento esteja activado. (#6885)
* O anúncio das cores de fundo na revisão de ecrã está mais eficaz quando o texto é desenhado sobre um fundo transparente. (#6467) 
* Melhorado o suporte para aria-describedby no Internet Explorer 11, incluindo suporte em iframes e quando múltiplos IDs são fornecidos. (#5784)
* Na versão Creators Update do Windows 10, a diminuição do volume do NVDA já funciona como nas versões anteriores do Windows (I.e. Dininuir com voz e sons, diminuir sempre e não dininuir estão disponíveis). (#6933)
* O NVDA já não falha ao navegar para, ou a anunciar, certos controlos (UIA) sem atalho de teclado. (#6779)
* Já não são adicionados dois espaços na informação de atalhos de teclado para certos controlos (UIA). (#6790)
* Certas combinações de teclas nas linhas da HIMS (por exemplo, espaço+ponto4) já não falham intermitentemente. (#3157)
* Resolvido um problema ao abrir uma porta série, em sistemas, em alguns idiomas diferentes do inglês, que causavam problemas, em certos casos, falhas na ligação a dispositivos Braille. (#6845)
* Reduzidas as hipóteses de corrupção do ficheiro de configurações quando o Windows é desligado. O ficheiro de configurações é agora escrito para um ficheiro temporário antes de substituir o ficheiro corrente de configurações. (#3165)
* Ao pressionar duas vezes o comando para ler a linha actual, a soletração já é feita usando o idioma correcto. (#6726)
* Navegar por linha no Microsoft Edge é agora até três vezes mais rápidono Windows 10 Creators Update. (#6994)
* O NVDA já não anuncia "Web Runtime grouping" ao focar documentos do Microsoft Edge no Windows 10 Creators Update (#6948)
* Todas as versões do SecureCRT passam a ser suportadas. (#6302)
* O Adobe Acrobat Reader já não cracha em certos documentos PDF ( mais concretamente nos que contém o atributo ActualText vazio). (#7021, #7034)
* No Microsoft Edge, em modo de navegação, as tabelas interactivas (ARIA grids) já não são ignoradas ao navegar para tabelas com "T" e "shift+T". (#6977)
* No modo de navegação, pressionando "Shift+Home" após ter seleccionado para a frente, agora desselecciona até ao princípio da linha como seria de esperar. (#5746)
* No modo de navegação, pressionando Control+T (para seleccionar tudo) já não falha quando o cursor não está no início do texto. (#6909)
* Corrigidos outros raros problemas em modo de navegação. (#7131)

### Alterações para desenvolvedores

* Commandline arguments are now processed with Python's argparser module, rather than optparser. This allows certain options such as -r and -q to be handled exclusively. (#6865)
* core.callLater now queues the callback to NVDA's main queue after the given delay, rather than waking the core and executing it directly. This stops possible freezes due to the  core accidentally going to sleep after processing a callback, in the midle of  a modal call such as the desplaying of a message box. (#6797)
* The InputGesture.identifiers property has been changed so that it is no longer normalized. (#6945)
 * Subclasses no longer need to normalize identifiers before returning them from this property.
 * If you want normalized identifiers, there is now an InputGesture.normalizedIdentifiers property which normalizes the identifiers returned by the identifiers property .
* The InputGesture.logIdentifier property is now deprecated. Callers should use InputGesture.identifiers[0] instead. (#6945)
* Deprecated code removed:
 * `speech.REASON_*` constants, `controlTypes.REASON_*` should be used instead. (#6846)
 * `i18nName` for synth settings, `displayName` and `displayNameWithAccelerator` should be used instead. (#6846, #5185)
 * `config.validateConfig`. (#6846, #667)
 * `config.save`. (#6846)
* The list of completions in the autocomplete context menu of the Python Console no longer shows  any object path leading up to the final symbol being completed. (#7023)
* There is now a unit testing framework for NVDA. (#7026)
 * Unit tests and infrastructure are located in the tests/unit directory. See the docstring in the tests\unit\init.py file for details.
 * You can run tests using "scons tests". See the "Running Tests" section of readme.md for details.
 * If you are submitting a pull request for NVDA, you should first run the tests and ensure they pass.

## 2017.1

Os destaques desta versão são:

* Anúncio de secções e colunas no Microsoft Word;
* Suporte à leitura, navegação e anotações em livros no Kindle for PC;
* Suporte melhorado ao Microsoft Edge.

### Novas Funcionalidades

* No Microsoft Word o tipo de quebra de secção e o número da secção passam a poder ser anunciados. Esta opção é activada juntamente com o anúncio do número de página no diálogo Formatação de documentos do NVDA. (#5946)
* No Microsoft Word as colunas de texto passam a poder ser anunciadas. Esta opção é activada juntamente com o anúncio do número de página no diálogo Formatação de documentos do NVDA. (#5946)
* A mudança automática de idioma passa a ser suportada no Wordpad. (#6555)
* O comando Localizar do NVDA (NVDA+control+f) já é suportado no modo de navegação no Microsoft Edge. (#6580)
* Os comandos de navegação rápida para botões, no modo de navegação, (b e shift+b) passam a ser suportados no Microsoft Edge. (#6577)
* Ao copiar uma folha no Microsoft Excel, os cabeçalhos de linhas e colunas são também copiados. (#6628)
* Suporte para ler e navegar livros na versão 1.19 para PC do Kindle, incluindo acesso a links, notas de rodapé, gráficos, texto realçado e notas do utilizador. Por favor, consulte a secção sobre o Kindle para PC do Manual do utilizador para mais informações. (#6247, #6638)
* A navegação em tabelas no modo de navegação  já é suportada no Microsoft Edge. (#6594)
* No Microsoft Excel, o comando Anunciar localização do cursor de revisão (desktop: NVDA+Delete do numérico, laptop: NVDA+delete) passa a anunciar o nome da folha e a localização da célula. (#6613)
* Adicionada uma opção ao diálogo de encerramento do NVDA para reiniciar com o nível de registo definido para Depuração. (#6689)

### Alterações

* O valor mínimo para a intermitência do cursor braille é agora 200 ms. Perfis ou configurações com valores inferiores serão alterados para este novo mínimo. (#6470)
* Foi adicionada, no diálogo Definições do Braille, uma caixa de verificação para poder desligar a intermitência do cursor Braille. Esta opção era antes activada colocando a intermitência do cursor Braille a 0. (#6470)
* Actualizado o eSpeak NG (commit e095f008, 10 de Janeiro de 2017). (#6717)
* Devido a alterações no Windows 10 Creators Update, que quebraram esta funcionalidade, a opção Diminuir sempre foi removida do Modo  de diminuição do volume do NVDA. Ainda está disponível em versões anteriores do windows 10. (#6684)
* Devido a alterações no Windows 10 Creators Update, que quebraram esta funcionalidade, a opção Diminuir quando a emitir voz ou sons já não pode assegurar que o som foi silenciado antes de começar a falar, nem que o áudio fica desligado depois de terminar. Estas alterações não afectam versões anteriores do windows 10. (#6684)

### Correcções

* Corrigida a paragem no Microsoft Word ao mover por parágrafo no modo de navegação num documento grande. (#6368)
* As tabelas copiadas do Microsoft Excel  para o Microsoft Word já não são consideradas como tabelas de formatação e, por isso, já não são ignoradas. (#5927)
* Ao tentar escrever na vista protegida do Microsoft Excel, o NVDA passa a fazer um bip em vez de ecoar as letras que, na realidade, não são escritas. (#6570)
* Pressionar escape no Microsoft Excel já não muda, incorrectamente, para modo de navegação, a menos que o utilizador tenha antes mudado para esse modo, com NVDA+Espaço, e depois tenha mudado para o modo normal ao pressionar enter num campo de formulário. (#6569) 
* O NVDA já não apresenta paragens no Microsoft Excel, quando numa folha, uma linha ou coluna inteira está unida. (#6216)
* O anúncio de texto cortado ou em sobreposição, nas células do Microsoft Excel, está mais preciso. (#6472)
* O NVDA passa a anunciar quando uma caixa de verificação é apenas de leitura. (#6563)
* Ao iniciar o NVDA, já não é mostrado um aviso  quando não é possível emitir sons por falta de um dispositivo de áudio. (#6289)
* Nos frisos do Microsoft Excel os controlos indisponíveis passam agora a ser anunciados como tal. (#6430)
* O NVDA já não anunciará "painel" ao minimizar janelas. (#6671)
* Os caracteres digitados já são falados nas aplicações Universal Windows Platform (UWP) (incluindo Microsoft Edge) no Windows 10 Creators Update. (#6017)
* O acompanhamento do rato já funciona em todos os ecrãs em computadores com múltiplos ecrãs. (#6598)
* O NVDA já não fica inusável depois de sair do Windows Media Player quando focado numa barra deslizante. (#5467)

### Alterações para desenvolvedores

* Os ficheiros de Perfis e configurações serão automaticamente actualizados para acomodar as alterações ao esquema de intermitência do cursor Braille. Se houver um erro na actualização, uma notificaçãon será mostrada e a  configuração será feita por padrão,, ficando a configuração antiga disponível no ficheiro de log do NVDA. (#6470)

## 2016.4

Os destaques desta versão são:

* Suporte melhorado ao Microsoft Edge;
* Modo de navegação no programa Correio do Windows 10;
* Melhorias várias nos diálogos do NVDA.

== Novas Funcionalidades ==
* O NVDA pode agora anunciar a identação das linhas usando sons. Isto pode ser configurado através da caixa combinada Anúnncio da identação das linhas no diálogo de Formatação de documentos das preferências do NVDA. (#5906)
* Foi adicionada uma opção para abrir o Visualizador de discurso no arranque. Esta opção pode ser activada através de uma caixa de verificação na janela do Visualizador de discurso. (#5050)
* Ao reabrir a janela do Visualizador de discurso, a sua localização e dimensão serão restauradas. (#5050)
* As Referências cruzadas no Microsoft Word passam a ser tratadas como Links. Serão anunciadas como links e podem ser activadas. (#6102)
* Suporte para a linha Braille  Orbit Reader 20. (#6007)
* Suporte para as linhas Braille Baum SuperVario2, Baum Vario 340 e HumanWare Brailliant2. (#6116)
* Suporte inicial para a versão Aniversário do Microsoft Edge. (#6271)
* O modo de navegação passa a ser usado ao ler e-mails no correio do Windows 10. (#6271)

### Alterações

* Actualizado o liblouis braille translator para a versão 3.0.0. Isto inclui melhorias significativas no Unified English Braille. (#6109, #4194, #6220, #6140)
* No Gestor de Extras, os botões Desactivar Extra e Activar Extra já possuem tecla de atalho, (alt+d e alt+e, respectivamente. (#6388)
* No diálogo do Gestor de extras diversos problemas de alinhamento e de aspecto foram resolvidos. (#6317, #5548, #6342, #6343, #6349)
* O diálogo de Formatação de documentos foi ajustado para que o conteúdo  possa rolar. (#6348)
* Ajustado o layout do diálogo Pronúncia de pontuação/símbolo, para que toda a sua largura possa ser usada pela lista de símbolos. (#6101)
* No modo de navegação, nos navegadores web, as teclas de navegação rápida, para campos de edição (e e shift+e) e de formulário (f e shift+f) agora também movem para campos de texto só de leitura. (#4164)
* Ajustada a aparência do diálogo de boas vindas ao NVDA. (#6350)
* Os diálogos do NVDA passam a ter os botões "ok" e "cancelar" alinhados à direita. (#6333)
* Passam a ser usadas barras deslizantes para os campos numéricos. (#6099)
* Amaneira como são reportadas as IFrames (documentos integrados em documentos) é agora mais consistente nos vários navegadores web. As IFrames passam a ser reportadas como "frame" no Firefox. (#6047)

### Correcções

* Corrigido um problema raro, ao sair do NVDA enquanto o visualizador de discurso está aberto, causando um erro. (#5050)
* Os "Image maps" são agora apresentados correctamente no modo de navegação no Mozilla Firefox. (#6051)
* Corrigido um problema que causava um aviso no log do NVDA, quando se alternava o estado do capsLock. (#6127)
* No diálogo dos dicionários, ao pressionar enter agora guarda as alterações e sai. (#6206)
* Passam a ser mostradas em Braille as mensagens de alteração do modo de introdução para um modo de introdução (nativo, input/alphanumeric, full shaped/half shaped, etc.). (#5892, #5893)
* Ao desabilitar, e imediatamente voltar a habilitar, um extra, ou vice-versa, o seu estado agora corretamente reverte para o que era anteriormente. (#6299)
* Ao utilizar o Microsoft Word, os campos de número de página nos cabeçalhos já podem ser lidos. (#6004)
* O rato agora pode ser usado para mover o foco entre a lista de símbolos e os campos de edição no diálogo de Pronúncia de pontuação/símbolo. (#6312)
* Corrigido um problema que impedia o aparecimento da lista de elementos quando o documento do Microsoft Word contém um link inválido. (#5886)
* Após fechar o Visualizador de discurso, através da barra de tarefas ou com Alt+F4, a indicação do seu estado no menu do NVDA passa a reflectir a realidade da sua visibilidade. (#6340)
* O comando Recarregar extras não causa mais problemas para os perfis de configuração activados, para os novos documentos em navegadores web nem para a revisão de ecrã. (#2892, #5380)
* Na lista de idiomas no diálogo Definições gerais do NVDA, idiomas como o Aragonês passam a ser exibidos correctamente no Windows 10. (#6259)
* As teclas de sistema emuladas por teclas de uma linha Braille, por exemplo, uma tecla simulando o Tab, passam a ser apresentadas no idioma do NVDA na Ajuda de entrada e no diálogo Definir Comandos. Antes eram sempre apresentadas em inglês. (#6212)
* Alterar o idioma do NVDA a parttir das Definições Gerais apenas tem efeito após reiniciar o NVDA. (#4561)
* O campo Texto original de uma nova entrada de dicionário já não pode ficar em branco. (#6412)
* Corrigido um problema raro, ao pesquisar por portas série em alguns sistemas que impossibilitava o uso de algumas linhas Braille. (#6462)
* No Microsoft Word, a numeração das listas em células de tabelas são agora lidos ao mover por células. (#6446)
* Passa a ser possível associar comandos ao pressionar de teclas das linhas Braille HandyTech através da opção Definir comandos do NVDA. (#6461)
* No Microsoft Excel, ao pressionar enter, ao navegar numa folha, agora é corretamente anunciada a mudança para a linha de baixo. (#6500)
* O iTunes já não crasha intermitentemente ao usar o modo de navegação para a iTunes Store, Apple Music, etc. (#6502)
* Corrigidos crashes em applicações de 64 bit baseadas em Mozilla ou Chrome. (#6497)
* No Firefox com o multi-process activo, o modo de navegação e os campos de edição já funcionam corretamente. (#6380)

### Alterações para desenvolvedores

* Já é possível criar appModules para executáveis que contenham um ponto (.) no seu nome. Os pontos serão substituidos por sublinhados (_). (#5323)
* O novo módulo gui.guiHelper inclui utilitários para simplificar a criação de GUI's do wxPython, incluindo gestão automática do espaçamento, o que facilita a apresentação dum melhor visual e mais consistência, e também facilita a criação de novas GUIs por desenvolvedores cegos. (#6287)

## 2016.3

Os destaques desta versão incluem:

* Possibilidade de desactivar Extras  individualmente;
* Suporte para campos de formulário no Microsoft Excel;
* Melhorias significativas no anúncio de cores;
* Correções e melhorias relacionadas com várias linhas Braille;
* Correções e melhorias no suporte ao Microsoft Word.

### Novas Funcionalidades

* O modo de navegação passou a poder ser usado para ler documentos PDF no Microsoft Edge. (#5740)
* O Rasurado e o Rasurado duplo passam a ser reportados quando apropriado no Microsoft Word. (#5800)
* No Microsoft Word, o título duma tabela passa a ser anunciado, se tiver sido definido. Se houver uma descrição, pode ser acedida usando o comando Abrir descrição longa (NVDA+d) no Modo de navegação. (#5943)
* No Microsoft Word, o NVDA agora anuncia informações de posição ao mover-se por parágrafos (alt+shift+seta abaixo e alt+shift+seta acima). (#5945)
* No Microsoft Word, o espaçamento das linhas passa a ser anunciado através do comando NVDA+F, Anunciar formatação de texto, quando for alterado por um comando do Word e quando nos movermos entre texto com diferentes níveis de espaçamento, se o Anunciar espaçamento de linhas estiver marcado na Formatação de documentos do NVDA. (#2961)
* No Internet Explorer, os elementos estruturais do HTML5 passam a ser reconhecidos. (#5591)
* O anúncio de comentários no Microsoft Word) pode ser desativado através da caixa de verificação Anunciar Comentários na Formatação de documentos do NVDA. (#5108)
* Através do Gestor de Extras é agora possível desativar um Extra específico. (#3090)
* Foram adicionados mais comandos para as linhas da série ALVA BC640/680. (#5206)
* Foi criado um comando para mover a linha Braille para o foco actual. Actualmente, apenas as linhas das séries ALVA BC640/680 têm uma tecla associada a este comando, mas a associação pode ser feita manualmente para qualquer linha através da opção Comandos. (#5250)
* No Microsoft Excel, já é possível interagir com Campos de formulário. Pode mover-se pelos campos de formulário usando a Lista de elementos ou, em Modo de navegação, a navegação por caracter. (#4953)
* Já é possível associar um comando para alternar o Modo de revisão simples usando a opção Definir comandos. (#6173)

### Alterações

* O NVDA passa a anunciar as cores usando um conjunto básico, bem reconhecível e entendível, de 9 cores e 3 graus de claridade. Os desenvolvedores pensam que é melhor que muitos nomes de cores difilmente reconhecíveis por quem nunca viu. (#6029)
* O comportamento de NVDA+F9 seguido de NVDA+F10 foi modificado para seleccionar texto com o primeiro pressionar de NVDA+F10. Quando NVDA+F10 é pressionado duas vezes rapidamente, o texto é copiado para a área de transferência. (#4636)
* Actualizado o eSpeakNG para a versão Master 11b1a7b (22 June 2016). (#6037)

### Correcção de falhas

* No Modo de navegação no Microsoft Word, o copiar para a área de transferência passa a preservar a formatação. (#5956)
* No Microsoft Word, o NVDA passa a anunciar correctamente os comandos de navegação em tabelas (alt+home, alt+end, alt+pageUp e alt+pageDown) e de selecção em tabelas (adicionamdo shift aos comandos de navegação). (#5961)
* Nos diálogos do Microsoft Word a navegação por objectos do  NVDA foi bastante melhorada. (#6036)
* Em algumas aplicações como o Visual Studio 2015, as teclas de atalho (como control+c para Copiar) passam a ser anunciadas como seria esperado. (#6021)
* Corrigida uma eventual falha ao pesquisar por portas série, em alguns sistemas, que tornava os drivers das linhas Braille inutilizáveis. (#6015)
* O anúncio de cores no Microsoft Word é agora mais certeiro, pois as alterações provocadas pelos temas do Microsoft Office são levadas em conta. (#5997)
* O modo de navegação para o Microsoft Edge e o suporte às sugestões da pesquisa no Menu Iniciar está novamente disponível nas versões  do Windows 10 depois de Abril de 2016. (#5955)
* No Microsoft Word, a leitura automática dos cabeçalhos da tabela, quando estes se encontram em células mescladas, funciona melhor. (#5926)
* No Correio do Windows 10 o NVDA já não falha na leitura do conteúdo das mensagens. (#5635) 
* Quando o "Anúncio de teclas de comando" está activado, CapsLock, NumLock e ScrollLock já não são anunciados em duplicado. (#5490)
* Os diálogos do Controlo de Conta do Utilizador do Windows são novamente lidos correctamente na versão Aniversário do Windows 10. (#5942)
* No Plugin Web Conference, como o que é usado no out-of-sight.net, o NVDA já não emite bips nem fala as barras de progressão relativas ao nível do microfone. (#5888)
* Ao executar o Localizar seguinte ou Localizar anterior, no Modo de navegação, passa a ser respeitado o parâmtero Maiúsculas/minúsculas. (#5522)
* Ao editar entradas no dicionário, é dado feedback sobre expressões regulares inválidas. O NVDA já não crasha se o dicionário contiver expressões regulares inválidas. (#4834)
* Se o NVDA não conseguir comunicar com uma linha Braille (por exemplo,  por ter sido desligada), será automaticamente desactivado o uso da linha. (#1555)
* Ligeiramente melhorada, em alguns casos, a performance da filtragem na Lista de elementos no Mode de navegação. (#6126)
* No Microsoft Excel, os nomes dos fundos anunciados pelo NVDA passam a ser os mesmos que os usados pelo Excel. (#6092)
* Suporte melhorado para o ecrã de início de sessão do Windows 10 incluindo o anúncio de alertas e activação do campo de introdução da palavra-passe com ecrã táctil. (#6010)
* O NVDA passa a detectar correctamente a segunda fila de cursores de toque das linhas Braille das séries ALVA BC640/680. (#5206)
* O NVDA volta a anunciar os toast, balões de notificações, nas versões mais recentes do Windows 10. (#6096)
* O NVDA já não deixa de reconhecer o pressionar de teclas nas linhas Braille da Baum e da HumanWare Brailliant B. (#6035)
* Se a opção Anunciar números de página estiver marcada, o os números de linha serão também anunciados em Braille. (#5941)
* Quando o Modo de voz estiver desactivado, o anúncio de objectos (tal como pressionar NVDA+tab para anunciar o objecto em foco) a informação aparece no Visualizador de discurso como esperado. (#6049)
* Na lista de mensagens do Outlook 2016, a informação sobre rascunhos associados já não é anunciada. (#6219)

### Alterações para Desenvolvedores

* Logging uma informação directamente duma propriedade já não resulta na propriedade ser chamada recursiva e infinitamente. (#6122)

## 2016.2.1

Esta versão corrige falhas no Microsoft Word:

* O NVDA já não provoca falhas no Microsoft Word, assim que este é iniciado no Windows XP. (#6033)
* Removido o anúncio de erros gramaticais, por provocar falhas no Microsoft Word. (#5954, #5877)

## 2016.2

Os destaques desta versão incluem a funcionalidade de anunciar os erros ortográficos, à medida que se escreve, e a possibilidade de reportar os erros gramaticais  no Microsoft Word, bem como várias melhorias e correcções  no suporte ao Microsoft Office.

### Novas Funcionalidades

* No modo de navegação no  Internet Explorer e outros controlos MSHTML, usando a navegação por caracter, mover por anotações (a e shift+a) agora também move para texto inserido e apagado. (#5691)
* No Microsoft Excel, o NVDA agora anuncia o nível de um grupo de células, bem como se estão expandidas ou recolhidas. (#5690)
* Ao pressionar, duas vezes, o comando para anunciar a formatação do texto (NVDA+f), é apresentado um diálogo, em modo de navegação, com a informação de modo a poder ser revista. (#4908)
* No Microsoft Excel 2010 e seguintes, o sombreado e o gradiente das células é agora anunciado. O anúncio automático é controlado pela opção Anunciar cores nas preferências do NVDA, Formatação de documentos. (#3683)
* Nova tabela Braille: Grego Koine. (#5393)
* No Visualizador de registo é agora possível gravar o documento usando o comando Control+s. (#4532)
* Se o anúncio de erros ortográficos estiver activado, e se for suportado pelo campo de edição em uso, o NVDA reproduzirá um som para alertar de um erro ortográfico cometido ao escrever. Isto pode ser desactivado com a nova opção "Tocar som para erros ortográficos ao escrever" nas Opções de Teclado do  NVDA. (#2024)
* Os erros gramaticais são agora anunciados no Microsoft Word. Isto pode ser desactivado na nova opção "Anunciar erros gramaticais" na Formatação de documentos das preferências do NVDA. (#5877)

### Alterações

* O NVDA mudou para o sintetizador eSpeak NG. (#5651)
* In browse mode and editable text fields, NVDA now treats numpadEnter the same as the main enter key. (#5385)
* In Microsoft Excel, NVDA no longer ignores a column header for a cell when there is a blank row between the cell and the header. (#5396)
* In Microsoft Excel, coordinates are now announced before headers to eliminate ambiguity between headers and content. (#5396)

### Correcção de falhas

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

### Alterações para Desenvolvedores

* NVDA's C++ components are now built with Microsoft Visual Studio 2015. (#5592)
* You can now present a text or HTML message to the user in browse mode using ui.browseableMessage. (#4908)
* In the User Guide, when a <!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) -->

## 2016.1

Os destaques desta versão são a possibilidade do NVDA, opcionalmente, baixar o volume do som de outros programas, melhorias na apresentação da saída em Braille e  no suporte a algumas linhas Braille, várias correções significativas no suporte ao Microsoft Office e correções no modo de navegação no iTunes.

### Novas Funcionalidades

* Novas tabelas de conversão Braille: Polaco Braille informático 8 pontos e Mongol. (#5537, #5574)
* O cursor Braille pode ser desativado ou alterada a sua aparência através das novas opções "Mostrar cursor" e "Aparência do cursor" nas Definições do Braille. (#5198)
* O NVDA pode, opcionalmente, baixar o volume de outros sons, se instalado em Windows 8 ou superior. Esta opção pode ser configurada usando a nova opção "Modo de diminuição do volume" no menu do NVDA, Preferências, Sintetizador ou pressionando NVDA+shift+d. (#3830, #5575)
* O NVDA já se pode ligar à linha Braille HIMS Smart Beetle via Bluetooth. (#5607)
* Suporte as linhas Braille APH Refreshabraille, no modo HID, e às Baum VarioUltra e Pronto! quando ligadas via USB. (#5609)
* Suporte às linhas Braille HumanWare Brailliant BI/B quando o protocolo está configurado para OpenBraille. (#5612)

### Alterações

* A opção "Anunciar ênfase" passa a estar desmarcada por padrão. (#4920)
* Na "Lista de Elementos" do Microsoft Excel, a tecla de atalho para Fórmulas mudou para alt+r e para Folhas para Alt+L, para ser diferente do atalho do campo "Filtrar por". (#5527)
* Actualizado o liblouis braille translator para a versão 2.6.5. (#5574)
* A palavra "texto" já não é anunciada ao mover-se para o foco ou o cursor de revisão para um objecto texto. (#5452)

### Correcção de falhas

* No  iTunes 12, quando uma página da loja é carregada, o seu conteúdo já é atualizado corretamente no modo de navegação. (#5191)
* No Internet Explorer e outros controlos MSHTML, mover-se para um título de nível específico, com a navegação rápida por caractere, passa a funcionar como esperado, mesmo que esse atributo, H tag, seja sobreposto, para efeitos de acessibilidade, pelo atributo aria-level. (#5434)
* No Spotify, o foco já não é frequentemente associado a objecto desconhecido. (#5439)
* Quando se volta ao Spotify, vindo de outra aplicação, o foco já é corretamente assumido. (#5439)
* Ao alternar entre o modo de navegação e o modo de foco, o modo actual é anunciado em Braille e em voz. (#5239)
* O botão Iniciar na barra de tarefas, já não é anunciado como lista e/ou seleccionado em algumas verrsões do Windows. (#5178)
* Mensagens como "inserido" já não são anunciadas durante a composição de mensagens no Microsoft Outlook. (#5486)
* Quando se está a usar uma linha Braille e é selecionado texto na linha actual, por exemplo, quando se localiza uma expressão que ocorre nessa mesma linha, mas mais à frente, a linha é movida para esse local. (#5410)
* No Windows 10, o NVDA já não é desligado silenciosamente quando se fecha, com Alt+F4, uma janela de linha de comandos. (#5343)
* Na Lista de Elementos no modo de navegação, quando se altera o tipo de elementos, o campo "Filtrar por:" é limpo. (#5511)
* Nas áreas de texto editável das aplicações Mozilla, movendo o rato lê a porção de texto apropriada, em vez de ler o texto todo. (#5535)
* Ao mover o rato num campo de texto editável duma aplicação Mozilla, a leitura já não pára em elementos como links incluídos no texto a ser lido. (#2160, #5535)
* No Internet Explorer, a página shoprite.com já pode ser lida em modo de navegação. (Especificamente os atributos lang mal definidos são tratados apropriadamente.) (#5569)
* No Microsoft Word, alterações rastreáveis como "inserido" já não são anunciadas se a sua marcação não for visível. (#5566)
* Quando um botão de comutação é focado, agora o NVDA anuncia quando o seu estado  é alterado de pressionado para não pressionado. (#5441)
* O anúncio da alteração da forma do rato voltou a funcionar como devido. (#5595)
* Ao anunciar a indentação da linha, os espaços não separáveis são tratados como espaços normais. Antes, isto podia causar anúncios como "espaço espaço espaço" em vez de "3 espaços". (#5610)
* Ao fechar uma lista de candidatos modern Microsoft input method, o foco é correctamente restaurado para a janela de composição ou para o documento. (#4145)
* No Microsoft Office 2013 e superiores, quando os frisos estão configurados para mostrar apenas tabs,os  itens dos frisos são novamente anunciados, como devido, quando algum tab é activado. (#5504)
* Correções e melhorias na deteção de toques no ecrã e suas associações. (#5652)
* O gesto de deslizar deixou de ser mencionado na ajuda. (#5652)
* O NVDA já não falha ao listar comentários na Lista de Elementos para o Microsoft Excel, mesmo que um comentário esteja numa célula mesclada. (#5704)
* O NVDA já não falha ao ler o conteúdode uma folha do Microsoft Excel com a opção "Anunciar títulos da linha/coluna da tabela" activada. (#5705)
* No Google Chrome, ao navigar dentro de uma área de composição, introduzindo caracteres do Extremo Oriente, o NVDA funciona como esperado. (#4080)
* Quando se pesquisa dentro da Apple Music no iTunes, o modo de navegação para o documento dos resultados já é actualizado devidamente. (#5659)
* No Microsoft Excel, ao pressionar shift+f11 para criar uma nova folha, agora é anunciada a posição actual em vez de ficar calado.(#5689)
* Corrigidos problemas com a saída de Braille ao introduzir caracteres Coreanos. (#5640)

### Alterações para Desenvolvedores

* A nova classe audioDucking.AudioDucker permite ao código que emita áudio que indique quando outro áudio deva ser diminuido. (#3830)
* Os nvwave.WavePlayer's constructor agora têm um wantDucking keyword argument que especifica se o audio de outras aplicações deve ser diminuido enquanto o seu áudio é reproduzido. (#3830)
 * Quando isto é activado, o que é o padrão, é essencial que WavePlayer.idle seja chamado quando apropriado.
* Melhorado o I/O para linhas Braille: (#5609)
 * Os drivers de linhas Braille Thread-safe podem declarar-se eles próprios como tal usando o atributo BrailleDisplayDriver.isThreadSafe. Um driver deve ser thread-safe para benefeciar das seguintes funcionalidades:
 * Os dados são escritos em fundo para os drivers Braille thread-safe, aumentando a performance;
 * hwIo.Serial estende pyserial para chamar um chamável quando são recebiddos dados em vez de o driver ter de os captar.
 * hwIo.Hid suporta que as linhas Braille comuniquem via USB HID.
 * hwPortUtils e hwIo podem, opcionalmente, proporcionar logs detalhados incluindo dispositivos encontrados e todos os dados recebidos e enviados.
* Acessíveis várias novas propriedades para comandos de toque: (#5652)
 * os objectos MultitouchTracker contêm uma propriedade  childTrackers que contêm o MultiTouchTrackers que engloba os vários trackers que o compôem. Por exemplo, toque duplo com 2 dedos tem child trackers para Toque com 2 dedos. Toque com 2 dedos, por sua vez, tem child trackers para dois toques.
 * Os objectos MultiTouchTracker também contêm uma propriedade rawSingleTouchTracker se o tracker for o resultado de um toque com um dedo, varrimento ou deslize. The SingleTouchTracker allows access to the underlying ID assigned to the finger by the operating system and whether or not the finger is still in contact at the current time.
 * Os TouchInputGestures agora têm propriedades x e y, removendo a necessidade de aceder ao tracker para casos normais.
 * Os TouchInputGesturs contêm uma propriedade preheldTracker, que é um objecto MultitouchTracker representando os outros dedos mantidos enquanto este comando é efectuado.
* Podem ser feitos dois novos comandos de toque: (#5652)
 * Tocar e manter mútiplo (e.g. toque duplo e manter)
 * Um identificador generalizado com a contagem de dedos removida para quando se mantém os dedos (e.g. hold+hover para 1finger_hold+hover).

## 2015.4

Os destaques desta versão incluem melhorias da performance em Windows 10, inclusão do NVDA no Centro de Facilidades de Acesso  no Windows 8 e superiores, Melhorias no suporte ao Microsoft Excel, incluindo listagem e renomeação de folhas e acesso a células bloqueadas em folhas protegidas, e suporte na edição de conteúdo rich text em Mozilla Firefox, Google Chrome e Mozilla Thunderbird.

### Novas Funcionalidades

* O NVDA já aparece no Centro de Facilidades de Acesso no Windows 8 e seguintes (#308)
* Ao mover-se entre células no Excel, as alterações de formatação são automaticamente anunciadas, se as opções apropriadas estiverem activadas no diálogo "Formatação de documentos" do NVDA (#4878)
* Foi adicionada a opção "Anunciar ênfase" ao diálogo "Formatação de documentos" do NVDA. Activada por padrão, esta opção permite ao NVDA anunciar a existência de texto emfatisado em documentos. Para já, é apenas suportado para etiquetas "em" e "strong" no Modo de navegação  para Internet Explorer e outros controlos MSHTML. (#4920)
* A existência de texto inserido  e apagado é anunciado no modo de navegação no Internet Explorer e outros controlos MSHTML, se a opção  "Anunciar revisões do editor" do NVDA estiver activada. (#4920)
* Na lista de elementos do NVDA, para o Microsoft Word, mais informação é mostrada, como as propriedades de formatação que foram alteradas. (#4920)
* Microsoft Excel: Já é possível listar e renomear folhas na lista de elementos do NVDA (NVDA+f7). (#4630, #4414)
* Agora o NVDA anuncia, no Microsoft Excel, qualquer mensagem de entrada definida pelo autor para a célula. (#5051)
* No modo de navegação no Microsoft Excel, pode navegar para células bloqueadas em folhas protegidas. (#4952)

* Agora é possível configurar se os próprios símbolos são enviados ao sintetizador (e.g. para provocar uma pausa ou mudança de inflexão) no diálogo Pronúncia de pontuação/símbolo. (#5234)
* Suporte para as linhas Braille Baum Pronto! V4 e VarioUltra quando ligadas por Bluetooth. (#3717)
* Suporte para a edição de rich text  em aplicações Mozilla, tais como Documentos Google, com o suporte Braille activado no Mozilla Firefox e na composição em HTML no Mozilla Thunderbird. (#1668)
* Suporte para a edição de rich text em Google Chrome e outros navegadores baseados no Chrome, tais como Documentos do Google com o suporte Braille activado. (#2634)
 * Requer Chrome versão 47 ou superior.

### Alterações

* A opção  "Anunciar revisões do editor" do diálogo "Formatação de Documentos" do NVDA vem agora marcada por predefinição. (#4920)
* Ao mover-se por caractere, no Microsoft Word, com a opção "Anunciar revisões do editor" do NVDA activada, é anunciada menos informação das revisões, o que torna a navegação mais eficiente. Para ver mais informação, use a Lista de Elementos. (#4920)
* Actualizado o liblouis braille translator para a versão 2.6.4. (#5341)
* Vários símbolos (incluindo símbolos matemáticos básicos) foram movidos para o nível Algum, para que sejam falados por padrão. (#3799)
* Se o sintetizador supurtar, a voz deve passar a fazer uma pausa para parênteses e travessão (–). (#3799)
* Ao seleccionar texto, o texto é anunciado antes da indicação de selecção, em vez de o ser depois. (#1707)

### Correcção de falhas

* Grande melhoria na resposta durante a navegação na lista de mensagens do Outlook 2010/2013. (#5268)
* Num gráfico do Microsoft Excel, a navegação com certos comandos, como os de mudança de folha, (control+pageUp e control+pageDown) agora funciona correctamente. (#5336)
* Corrigida a aparência visual dos botões no diálogo que é mostrado ao tentar fazer um downgrade do NVDA. (#5325)
* No Windows 8 e seguintes, o NVDA arranca muito mais cedo quando configurado para iniciar após o início de sessão. (#308)
 * Se activou esta opção com uma versão anterior do NVDA, terá que a desactivar e reactivar novamente em Preferências, opções derais, para que as alterações tenham efeito:
  * Abra a caixa de diálogo Definições Gerais;
  * Desmarque a opção Iniciar o NVDA automaticamente depois de iniciar sessão no Windows;
  -  Pressione o botão OK;
  -  Abra novamente a caixa de diálogo Definições Gerais;
  * Marque a opção Iniciar o NVDA automaticamente depois de iniciar sessão no Windows;
  * Pressione o botão OK.
* Melhoria na performance com a UI Automation, o que se reflecte no Explorador de Ficheiros e Gestor de Tarefas. (#5293)
* O NVDA já alterna correctamente para o modo de  foco, quando após um Tab entra em controlos de grelha read-only ARIA apenas de leitura no modo de navegação no Mozilla Firefox e outros controlos baseados em Gecko. (#5118)
* O NVDA agora anuncia correctamente Sem anterior" em vez de "Sem próximo" quando não há mais objectos quando se varre para a esquerda num ecrã táctil.
* Corrigido o problema ao escrever múltiplas palavras no campo Filtro no diálogo Comandos. (#5426)
* O NVDA já não pára ao religar a uma linha Braille HumanWare Brailliant BI/B series via USB. (#5406)
* Em idiomas com caracteres conjuntos, a descrição dos caracteres já funciona como devido para letras maiúsculas inglesas. (#5375)
* O NVDA já não deve parar ocasionalmente ao abrir o menu Iniciar no Windows 10. (#5417)
* No Skype para Desktop, as notificações que foram mostradas antes da última notificação desaparecer, passam a ser anunciadas. (#4841)
* No Skype para Desktop 7.12 ou superior, as notificações são agora anunciadas correctamente. (#5405)
* O NVDA agora anuncia correctamente o foco quando sai de um menu de contexto em algumas aplicações, tais como Jart. (#5302)
* No Windows 7 ou superior, as cores são novamente anunciadas em algumas aplicações como o Wordpad. (#5352)
* Ao editar no Microsoft PowerPoint, pressionando enter é automaticamente anunciado o texto digitado tal como bullet ou número. (#5360)

## 2015.3

Os destaques desta versão incluem o suporte inicial ao Windows 10, a funcionalidade de poder desactivar a leitura rápida no modo de navegação,(útil para algumas aplicações web), vários melhoramentos no Internet Explorer e solucionado o problema da introdução de texto em certas aplicações com uma linha Braille ligada.

### Novas Funcionalidades

* A existência de erros ortográficos é anunciada em campos editáveis no Internet Explorer e outros controlos MSHTML. (#4174)
* Muitos mais símbolos matemáticos unicode são lidos quando aparecem num texto. (#3805)
* As sugestões de pesquisa no ecrã inicial do Windows 10 são anunciadas automaticamente. (#5049)
* Suporte para as linhas EcoBraille 20, EcoBraille 40, EcoBraille 80 e EcoBraille Plus . (#4078)
* Em modo de navegação, pode activar ou desactivar a Navegação por caracter pressionando NVDA+shift+espaço. Quando desactivada, as letras são passadas à aplicação, o que é útil em algumas aplicações web tais como GMail, Twitter e Facebook. (#3203)
* Novas tabelas Braille: Finlandês 6 pontos, Irlandês grau 1, Irlandês grau 2, Coreano grau 1 (2006) e Coreano grau 2 (2006). (#5137, #5074, #5097)
* O teclado QWERTY da linha Braille Papenmeier BRAILLEX Live Plus já é suportado. (#5181)
* Suporte experimental para o navegador Microsoft Edge e respectivo motor de navegação no Windows 10. (#5212)

### Alterações

* Actualizado o liblouis braille translator para a versão 2.6.3. (#5137)
* Ao tentar instalar uma versão do NVDA anterior à que está instalada, será avisado que isso não é recomendado e que o NVDA deve ser desinstalado antes de continuar. (#5037)

### Correcção de falhas

* No modo de navegação no Internet Explorer e outros controlos MSHTML, as teclas rápidas para campos de formulários já não incuem itens de listas de apresentação. (#4204)
* No Firefox, o NVDA já não tenta criar uma descrição para ARIA tab panels baseada  em todo o texto do painel. (#4638)
* No Internet Explorer e outros controlos MSHTML, pressionando Tab até uma secção, os artigos ou diálogos  já não são anunciado como se fossem o nome. (#5021, #5025) 
* Ao usar linhas Braille Baum/HumanWare/APH com teclado Braille, a escrita Braille já não deixa de funcionar depois de pressionar uma tecla sem ser do teclado. (#3541)
* No Windows 10, informação estranha já não é anunciada ao pressionar alt+tab ou alt+shift+tab para alternar entre aplicações. (#5116)
* O texto introduzido já não fica baralhado ao escrever em aplicações como o Microsoft Outlook, ou no Windows 7 e seguintes, em aplicações como o WordPad, Skype, Windows Live Mail, etc, com umalinha Braille ligada. (#2953 e #4291(
* Em Braille, já não são exibidos espaços estranhos entre, ou depois de, indicadores de controlos e formatação. (#5043)
* Em modo de navegação, no Internet Explorer e noutros controlos MSHTML, o conteúdo correcto é anunciado quando um elemento aparexce ou é alterado, e é imediatamente focado. (#5040)
* Em modo de navegação, no Microsoft Word, a navegação por caracter agora atualiza, como devido, a linha Braille e o cursor de revisão. (#4968)
* Quando uma aplicação não está a responder, ou a responder com lentidão, e muda para outra aplicação, o NVDA, na maior parte dos casos, passa a responder mais normalmente. (#3831)
* As notificações, Toast, do Windows 10 passam a ser anunciadas correctamente. (#5136)
* Em algumas caixas combinadas, (UI Automation) o valor passa a ser anunciado sempre que é alterado.
* Em modo de navegação nos navegadores  web, após atingir uma frame navegando com o Tab, a navegação por Tab continua a funcionar normalmente. (#5227)
* O Ecrã de Bloqueio do Windows 10 pode ser disactivado usando o ecrã táctil. (#5220)
* No Ecrã de Bloqueio do Windows 10, já não é possível ler a área de transferência, aceder às aplicações em execução com o cursor de revisão, alterar as configurações do NVDA, etc. (#5269)

### Alterações para Desenvolvedores

* Agora já pode injectar raw input a partir de um teclado que não seja nativamente controlado pelo Windows (e.g. um teclado QWERTY de uma linha Braille) usando a nova função keyboardHandler.injectRawKeyboardInput. (#4576)
* Foi adicionado o eventHandler.requestEvents para obter eventos que, por predefinição, estão bloqueados; e.g. mostrar eventos de um controlo específico ou certos eventos mesmo que em segundo plano. (#3831)
* Em vez de um único atributo i18nName, synthDriverHandler.SynthSetting tem agora em separado dois atributos, displayNameWithAccelerator e displayName para evitar o anúncio da tecla aceleradora no anel de configurações do sintetizador em alguns idiomas
* Para retrocompatibilidade, no constructor, displayName é opcional e é derivado do displayNameWithAccelerator se não fornecido. Contudo, se pretender ter uma tecla aceleradora para uma configuração, ambos deverão ser fornecidos.
* O atributo  i18nName está obsoleto e poderá ser removido numa versão futura.

## 2015.2

Os destaques desta versão incluem a possibilidade de ler gráficos no Microsoft Excel e suporte para leitura e navegação interactiva de conteúdo matemático no MathPlayer 4.

### Novas Funcionalidades

* Agora é possível mover-se para a frente e para trás por frase, no Microsoft Word, com alt + SetaAbaixo e alt + SetaAcima respectivamente. (#3288)
* Novas tabelas  braille para vários idiomas indianos (#4778)
* No Microsoft Excel, o NVDA agora anuncia quando uma célula tem conteúdo em sobreposição ou obscurecido. (#3040)
* No Microsoft Excel, agora pode usar a Lista de Elementos, NVDA+f7, para listar gráficos, comentários e fórmulas. (#1987)
* Suporte para a leitura de gráficos no Microsoft Excel. Para isso seleccione o gráfico usando a Lista de Elementos, NVDA+f7, e depois use as setas para se mover entre os vários pontos. (#1987)
* Usando o MathPlayer 4 da Design Science, o NVDA pode agora ler e navegar interactivamente conteúdo matemático nos navegadores de Internet, Microsoft Word E PowerPoint. Veja a secção "Leitura de conteúdo matemático" no Manual do utilizador para mais detalhes. (#4673)
* Passa a ser possível associar comandos, (comandos de teclado, comandos de toque, etc.) para todos os diálogos de preferências do NVDA e de formatação de documentos, usando o diálogo Comandos. (#4898)

### Alterações

* No diálogo de Formatação de documentos do NVDA, as teclas de atalho para Anunciar listas, Anunciar links, Anunciar números de linha e Anunciar nome do tipo de letra foram alterados em inglês, mas não em português (#4650)
* No diálogo de Definições do rato do NVDA, foram adicionadas teclas de atalho para Tocar coordenadas de áudio quando o rato se mover e Brilho controla o volume das coordenadas de áudio (#4916)
* Melhorado significativamente o anúncio dos nomes das cores. (#4984)
* Actualizado o liblouis braille translator para a versão 2.6.2. (#4777)

### Correcção de falhas

* As descrições de caracteres passam a ser correctamente tratadas para conjuntos de caracteres em certos idiomas indianos (#4582)
* Se a opção "Usar o idioma da voz ao processar caracteres e símbolos" estiver marcada, o diálogo "Pronúncia de pontuação/símbolo..." usará correctamente o idioma da voz. E também o nome do idioma para o qual estão a ser configurados os símbolos e pontuação estará presente no título do diálogo. (#4930)
* No Internet Explorer e noutros controlos MSHTML, os caracteres digitados já não são anunciados inapropriadamente em caixas combinadas editáveis, tais como o campo de pesquisa Google na página inicial do Google. (#4976)
* Ao seleccionar cores nas aplicações do  Microsoft Office, os nomes das cores passam a ser anunciados. (#3045)
* A tabela Braille de saída em dinamarquês volta a funcionar correctamente. (#4986)
* PageUp/pageDown podem ser usados novamente para mudar de slide numa apresentação PowerPoint. (#4850)
* No Skype para Desktop 7.2 e superiores, a notificação de contacto a escrever é agora anunciada e os problemas imediatamente após o foco sair de uma conversação foram resolvidos. (#4972)
* Resolvido o problema ao digitar alguns símbolos/pontuação, tais como parêntese rectos, no campo "Filtrar por" no diálogo Comandos. (#5060)
   * No Internet Explorer e noutros  controlos MSHTML, pressionando g, ou  shift+g, para  navegar pelos  gráficos, agora são  incluídos os elementos marcados como  imagens para efeitos de acessibilidade (i.e. ARIA role img). (#5062)

### Alterações para Desenvolvedores

* brailleInput.handler.sendChars(mychar) já não filtra o caractere, se for igual ao caractere anterior, por se certificar que a tecla é correctamente levantada.
* Scripts para alterar os modos de toque passam a respeitar os novos nomes adicionados a touchHandler.touchModeLabels. (#4699)
* Os Add-ons podem fornecer as suas próprias implementações de representação matemática. Ver o pacote mathPres para detalhes. (#4509)
* Foram implementados comandos de vvoz para inserir uma pausa entre palavras e para alterar a entoação, volume e velocidade. Ver BreakCommand, PitchCommand, VolumeCommand e RateCommand no módulo speech. (#4674)
* Criado também o speech.PhonemeCommand para inserir pronúncia específica, mas a implementação actual apenas suporta um número limitado de fonemas.

## 2015.1

Os destaques desta versão incluem o modo de navegação para documentos no Microsoft Word e Microsoft Outlook, grandes melhorias no suporte ao Skype para Desktop e correções significativas no suporte ao Microsoft Internet Explorer.

### Novas Funcionalidades

* Passa a ser possível adicionar novos símbolos na caixa de diálogo Pronúncia de pontuação/símbolo. (# 4354)
* Na caixa de diálogo Comandos pode usar o novo campo "Filtrar por:" para mostrar apenas os gestos que contêm as palavras especificadas. (# 4458)
* O NVDA agora anuncia automaticamente novo texto no MinTTY. (# 4588)
* Na caixa de diálogo Localizar do modo de navegação, existe agora uma opção para executar a pesquisa sensível a maiúsculas. (# 4584)
* As teclas de navegação rápida (h para títulos, etc), e a lista de elementos (NVDA + F7) estão agora disponíveis em documentos do Microsoft Word se activarmos o modo de navegação com NVDA + espaço. (# 2975)
* A leitura de mensagens no Microsoft Outlook 2007 e superiores foi bastante melhorada pois o modo de navegação é automaticamente activado para essas mensagens. Se o modo de navegação não for activado em algumas situações raras, pode forçá-lo com NVDA + espaço. (# 2975)
* Os títulos  de coluna de tabelas no Microsoft word são automaticamente anunciados nas  tabelas em que a linha de títulos foi especificamente definida pelo  autor nas propriedades de tabela do Microsoft word. (#4510)
 * Contudo em tabelas com colunas unidas , isto não funcionará automaticamente. Nestas situações, pode definir os títulos de coluna manuamente no NVDA com NVDA+shift+c.
* No Skype for Desktop, as notificações são agora anunciadas. (#4741)
* No  Skype for Desktop, Pode agora ter anunciadas  as várias mensagens antigas usando NVDA+control+1 até NVDA+control+0; por exemplo, NVDA+control+1 para a mensagem mais recente e NVDA+control+0 para a décima mensagem a ter sido recebida. (#3210)
* Numa  conversa no Skype for Desktop, o NVDA agora anuncia quando o outro elemento está a escrever. (#3506)
* O NVDA pode agora ser   instalado silenciosamente via linha de  comandos sem iniciar a cópia após instalação. Para tal, use a opção --install-silent. (#4206)
* Suporte para  as linhas Braille Papenmeier BRAILLEX Live 20, BRAILLEX Live e BRAILLEX Live Plus. (#4614)

### Alterações

* Na caixa de diálogo das Preferências do NVDA, Formatação de documentos, a opção Anunciar erros ortográficos agora tem uma tecla de atalho (Alt + O). (# 793)
* O NVDA passa a usar o idioma da voz/sintetizador para o processamento de caracteres, símbolos e momes dos sinais de pontuação, independentemente da configuração da opção "Alterar o idioma automaticamente". Para desactivar esta funcionalidade, para que o NVDA volte a usar o idioma da interface, desmarque a nova opção nas definições de voz, "Usar o idioma da voz ao processar caracteres e símbolos". (#4210)
* O suporte ao  sintetizador Newfon foi removido. O Newfon está agora disponível como um  extra do NVDA. (#3184)
* As versões 7 ou superiores do Skype for Desktop são agora necessárias para que o suporte do    NVDA funcione. As versões anteriores já não são suportadas. (#4218)
* O download das actualizações do NVDA é agora mais seguro. (Mais especificamente, a informação da actualização é agora  feita via https e a verificação da integridade do ficheiro é feita após download.) (#4716)
* O sintetizador eSpeak foi actualizado para a versão 1.48.04 (#4325)

### Correcção de falhas

* No Microsoft Excel, quando as células de cabeçalho de linha e coluna estão unidas. Por exemplo, se A1 e B1 estão unidas, para B2 terá agora anunciado A1 e B1 como cabeçalho da coluna, em vez de nada. (# 4617)
* Ao editar o conteúdo de uma caixa de texto no Microsoft PowerPoint 2003, o NVDA agora informa corretamente o conteúdo de cada linha. Antes as linhas eram cortadas em 1 caractere por cada novo parágrafo. (#4619)
* Todos os diálogos do NVDA estão agora no centro do ecrã, melhorando a apresentação visual e a usabilidade. (#3148)
* No Skype para desktop, ao introduzir uma mensagem introdutória para adicionar um contacto, introduzir texto e mover-se através dele agora funciona corretamente. (# 3661)
* Quando o foco é movido para um novo itemn numa estrutura em árvore no Eclipse IDE, se o item anteriormente focado for uma caixa de seleção, ele não é mais incorretamente anunciado. (# 4586)
* Na caixa de diálogo de verificação ortográfica do Microsoft Word, o próximo erro será anunciado automaticamente, quando o actual foi alterado ou ignorado através da respectiva tecla de atalho. (# 1938)
* O texto pode ser novamente lido corretamente em lugares como a janela de terminal de TeraTerm Pro e em documentos do Balabolka. (# 4229)
* O foco agora retorna corretamente ao documento que está a ser editado Ao terminar a composição de entrada de texto em coreano e outros idiomas do leste asiático, durante a edição dentro de frames no Internet Explorer e outros documentos MSHTML. (# 4045)
* No diálogo Comandos, ao seleccionar um esquema de teclado para um comando de teclado que está a ser adicionado, ao pressinar escape agora fecha o menu, como eé expectável, em vez de fechar o diálogo. (#3617)
* Ao remover um Extra, a directoria do Extra é correctamente eliminada após o reinício do NVDA. Antes era necessário reiniciar o NVDA por duas vezes. (#3461)
* Os problemas ao usar o Skype for Desktop 7 foram resolvidos. (#4218)
* Quando uma mensagem é enviada no Skype for Desktop, já não é anunciada duas vezes. (#3616)
* No Skype for Desktop, o NVDA já não deve, ocasionalmente, anunciar   continuamente um grande bloco de mensagens (às vezes toda a conversa). (#4644)
* Resolvido  o problema do comando de Anunciar a data/hora do NVDA por vezes não respeitar as definições regionais definidas. (#2987)
* No modo de navegação, para certos gráficos, como algumas imagens  em Google Groups, já não é apresentado texto sem sentido (por vezes estendendo-se por várias linhas). (Mais especificamente, isto ocorria em imagens codificadas em base64.) (#4793)
* O NVDA já não deve bloquear após alguns segundos, depois de mover o foco  de uma app da Windows Store, como se tivesse sido suspenso. (#4572)
* O atributo  aria-atomic em  regiões live no Mozilla Firefox é agora respeitado mesmo que  o próprio elemento atomic  mude. Antes, só afectava elementos descendentes. (#4794)
* O modo de navegação reflectirá actualizações, e as regiões serão anunciadas, em documentos que usem o modo de navegação dentro de aplicações ARIA inseridas em documentos no Internet Explorer, ou outros controlos MSHTML. (#4798)
* Quando é alterado, ou acrescentado, texto em regiões live no Internet Explorer, ou outros controlos MSHTML, em que o autor especificou que o texto é relevante, apenas o texto alterado ou modificado é anunciado, em vez de todo o texto no elemento que o contém. (#4800)
* Conteúdo indicado pelo atributo aria-labelledby em elementos no Internet Explorer, ou outros controlos MSHTML, substitui, quando apropriado, o conteúdo original. (#4575)
* Na verificação ortográfica do Microsoft Outlook 2013, a palavra errada é agora anunciada. (#4848)
* No Internet Explorer, ou outros controlos MSHTML, o conteúdo dentro de elementos ocultos com visibility:hidden já não é indevidamente mostrado no modo de navegação. (#4839, #3776)
* No Internet Explorer, ou outros controlos MSHTML, o atributo title nos controlos de formulário já não, indevidamente, tem preferência sobre outras associações de etiquetas. (#4491)
* No Internet Explorer, ou outros controlos MSHTML, o NVDA já não ignora a focagem de elementos devida ao atributo aria-activedescendant. (#4667)

### Alterações para Desenvolvedores

* Actualizado o wxPython para a versão 3.0.2.0. (#3763)
* Actualizado o Python para a versão 2.7.9. (#4715)
* O NVDA já não apresenta problemas quando é reiniciado após remover ou actualizar um extra que importe speechDictHandler no módulo installTasks. (#4496)

## 2014.4

### Novas Funcionalidades

* Novos idiomas: Castelhano da Colômbia  e Punjabi
* Agora é possível reiniciar o NVDA ou reiniciar o NVDA sem extras a partir da janela de saída do NVDA (#4057)
 * O NVDA também pode ser iniciado com os extras desactivados usando a opção de linha de comando disable-addons.
* Nos dicionários de voz, é agora possível especificar que uma regra só é aplicável se for uma palavra inteira, i.e. ou seja, não ocorre se fizer parte de uma palavra maior. (#1704)

### Alterações

* Caso o objeto para o qual se tenha movido, utilizando a navegação de objetos esteja dentro de um documento do modo de navegação, mas o objeto onde se encontrava anteriormente não estava, o modo de revisão é automaticamente alterado para modo de documento. Anteriormente, isso ocorria apenas quando o objeto de navegação era movido devido à mudança no foco. (#4369)
* As listas de linhas Braille e de Sintetizadores, nas respectivas janelas de configuração, são agora ordenadas alfabeticamente, excepto Sem Braille/Sem voz, que se encontram sempre no fim. (#2724)
* Actualizado o conversor Braille liblouis para a versão 2.6.0. (#4434, #3835)
* No modo de navegação, pressionando "e" e "shift+e", para navegar para o próximo, ou anterior, campo de edição, agora inclui  as caixas combinadas editáveis. Isto inclui o campo de pesquisa da última versão da pesquisa do Google. (#4436)
* Clicando com o botão esquerdo do rato no ícone do NVDA na barra do sistema agora abre o menu do NVDA em vez de não fazer nada. (#4459)

### Correcção de falhas

 * Ao mover o foco de volta para  um documento do modo de navegação (isto é, usando alt+tab para retornar a uma página web já aberta), o cursor de exploração agora é posicionado adequadamente sob o cursor virtual, em lugar de colocar-se sob o controle que tem o foco (isto é, próximo a um link). (#4369)
 * Na Apresentação de diapositivos do Powerpoint, o cursor de revisão agora acompanha corretamente  o cursor virtual. (#4370)
 * No Mozilla Firefox e outros navegadores baseados em Gecko, o novo conteúdo numa região live será anunciado mesmo que o novo conteúdo tenha um tipo usável de ARIA live diferente do região live superior. E.g. Conteúdo marcado  como assertive é adicionado a uma região live marcada como polite. (#4169).
 * No Internet Explorer e outros controlos MSHTML, no caso de um documento estar contido noutro documento já não causa a impedimento de leitura do documento, nomeadamente da frameset inserida noutra frameset (#4418)
 * O NVDA já não cracha ao tentar usar uma linha Braille Handy Tech. (#3709)

* No Windows Vista, um falso diálogo de "Ponto de Entrada Não Encontrado" já não é exibido em várias situações, tais como ao iniciar o NVDA pelo atalho do Desktop ou via pela tecla de atalho. (#4235)
* Problemas sérios com controlos de texto editável em diálogos de versões recentes do Eclipse foram resolvidos. (#3872)
* No Outlook 2010, a movimentação do cursor agora funciona como esperado nos campos de eventos e marcação de reuniões. (#4126)
* Dentro de uma região Live, o conteúdo marcado como não sendo live, (e.g. aria-live="off") é agora correctamente  ignorado. (#4405)
* Ao anunciar o texto de uma barra de estado, que tenha nome, o nome é agora correctamente separado da primeira palavra do texto da barra de estado. (#4430)
* Em campos de edição de palavra-passe, mesmo com o anúncio de palavras escritas ligado, já não são anunciados m asteriscos ao pressionar Tab, Espaço ou Enter. (#4402)
* Na lista de mensagens do  Microsoft Outlook, os itens já não são, sem necessidade, anunciados como Data Items. (#4439)
* Quando se selecciona texto no campo de edição de código, no Eclipse IDE, a totalidade da selecção já não é anunciada de cada vez que a selecçãon muda. (#2314)
* Várias versões do Eclipse, tais como Spring Tool Suite e a versão incluida no Android Developer Tools são agora reconhecidas como Eclipse, e tratadas correctamente. (#4360, #4454)
* O seguimento do rato e a exploração por toque, no Internet Explorer e outros controlos MSHTML (incluindo muitas aplicações Windows 8), é agora muito mais precisa em monitores com alta definição ou quando o Zoom é alterado. (#3494) 
* O seguimento do rato e a exploração por toque, no Internet Explorer e outros controlos MSHTML, agora anunciam a etiqueta de mais botões. (#4173)
* Se usar uma linha Braille Papenmeier BRAILLEX, com o BrxCom, as teclas da linha já funcionam como devido. (#4614)

### Alterações para Desenvolvedores

* Para executáveis que agrupam diferentes apps (e.g. javaw.exe), pode ser agora disponibilizado código numa app modules específica para cada app, em vez de usar o mesmo app module para todas as apps incluidas. (#4360)
 * Ver a documentação do código para appModuleHandler.AppModule para detalhes.
 * Implementado suporte para javaw.exe.

## 2014.3

### Novas características

* Os sons tocados quando o NVDA inicia ou termina podem agora ser desactivados, por meio de uma nova opção no Diálogo de Definições Gerais. (#834)
* A ajuda de extras agora pode ser acedida a partir do gestor de extras para extras que o suportem. (#2694)
* Suporte para o Calendário no Microsoft Outlook 2007 e posteriores (#2943) incluindo:
 * anúncio da hora atual ao mover-se para ela com as setas; - indicação no caso de a hora seleccionada se encontrar dentro de algum compromisso;
 * anúncio do compromisso selecionado ao premir tab;
 * Filtragem inteligente da data, de modo a anunciar a data apenas se a nova hora ou compromisso seleccionado  estiver num dia diferente do anterior.
* Melhorado o suporte para a caixa de entrada e outras listas de mensagens no Outlook 2010 e pusteriores (#3834) incluindo:
 * Possibilidade de silenciar os cabeçalhos das colunas (como por exemplo assunto, de, etc), desativando a opção Anunciar os cabeçalhos de linhas e colunas das tabelas no Diálogo de Definições de Formatação de Documentos;
 * Possibilidade de usar os comandos de navegação de tabelas (control + alt + setas) para se mover pelas colunas separadamente.
* Microsoft word: Quando não houver texto descritivo para uma imagem inserida no texto, o NVDA irá anunciar o título da imagem, caso o autor tenha definido um. (#4193)
* Microsoft Word: Anúncio da indentação do parágrafo através do comando de anúncio de formatação (NVDA+f) automaticamente, caso a nova opção Anunciar indentação de parágrafos esteja activa, nas definições de formatação de documentos. (#4165).
* Anúncio de textos  inseridos automaticamente, tais como um novo marcador, numeração ou indentação com tab ao premir enter em documentos editáveis  e campos de texto. (#4185)
* Microsoft word: ao premir NVDA+alt+c, irá anunciar o texto do comentário caso o cursor esteja sobre um. (#3528)
* Melhorado o suporte para a leitura automática dos cabeçalhos de colunas e linhas no Microsoft Excel (#3568) incluindo:
 * Support para o esquema de intervalo com nome definido no Excel para identificar cabeçalhos de células (compatível com o leitor de ecrã Jaws)
 * Os comandos para definir cabeçalhos de colunas    (NVDA+shift+c) e definir cabeçalhos de linhas (NVDA+shift+r) agora armazenam as configurações   na folha de cálculo, para que  estejam disponíveis da próxima vez que esta for aberta, e estarão disponíveis para outros leitores de ecrã que  suportem o esquema de intervalo com nome definido.
 * Estes comandos também poderão ser usados múltiplas vezes por folha de cálculo para definir diferentes cabeçalhos para diferentes regiões.
* Suporte para leitura automática de cabeçalhos de linhas e colunas das tabelas no Microsoft Word (#3110) incluindo:
 * Suporte para marcadores do MS Word para identificar cabeçalhos das células (compatível com o leitor de ecrã Jaws)
 * Os comandos para definir cabeçalhos de colunas    (NVDA+shift+c) e definir cabeçalhos de linhas (NVDA+shift+r), caso esteja sob a primeira célula do cabeçalho numa tabela, informarão o NVDA que esses cabeçalhos devem ser anunciados automaticamente.
 * As configurações serão armazenadas no documento,de modo a estarem disponíveis da próxima vez que o documento for aberto, e estarão disponíveis para outros leitores de ecrã que suportem o esquema desses marcadores.
* Microsoft Word: Anúncio da distância para a borda esquerda da página quando a tecla tab é premida. (#1353)
* Microsoft Word: obtenção de resposta em voz e braille para grande parte das teclas de atalho disponíveis para formatação  (negrito, itálico, sublinhado, alinhamento e nível de rascunho. ). (#1353)
* Microsoft Excel: Caso haja comentários na célula seleccionada, estes agora podem ser anunciados premindo NVDA+alt+c. (#2920)
* Microsoft Excel: implementado um diálogo específico do NVDA para editar comentários na célula atualmente seleccionada ao premir o comando shift+f2, para entrar no modo de edição de comentários. (#2920)
* Microsoft Excel: resposta em voz e braille para vários atalhos de movimentos de selecção (#4211) incluindo:
 * Movimento de página vertical (pageUp e pageDown);
 * Movimento horizontal de página (alt+pageUp and alt+pageDown);
 * Estender selecção (teclas supracitadas em conjunto com  Shift); e
 * Seleccionar a região atual (control+shift+8).
* Microsoft Excel: O alinhamento vertical e horizontal das células agora podem ser anunciados com o comando  de anunciar formatação (NVDA+f). Isto também pode ser anunciado automaticamente se a opção Anunciar alinhamento nas Definições de Formatação de Documento  estiver activa. (#4212)
* Microsoft Excel:  O estilo das células agora pode ser anunciado com o comando  de anunciar formatação (NVDA+f). Isto também pode ser anunciado automaticamente se a opção Anunciar estilo nas Definições de Formatação de Documento  estiver activa. (#4213)
* Microsoft PowerPoint: Ao mover formas dentro de um slide usando as setas, a localização atual da forma é agora anunciada (#4214) incluindo:
 * A distância entre a forma e cada borda do slide é anunciada.
 * Se uma forma está sobre  outra, ou é coberta por outra, o tamanho da parte sobreposta e a forma que está a ser coberta são anunciadas.
 * Para anunciar essa informação a qualquer momento sem se mover para a forma, prima o comando anunciar localização (NVDA+delete).
 * Ao seleccionar uma forma, caso esta esteja coberta por outra forma, o NVDA anunciará que ela está obscurecida.
* O comando Anunciar localização  (NVDA+delete) agora é mais específico em algumas situações. (#4219)
 * Em campos padrão de edição e no modo de navegação, são anunciadas a posição do cursor como percentagem do conteúdo e também as suas coordenadas no ecrã.
 * Nas formas em apresentações do PowerPoint , é anunciada a posição da forma em relação ao slide e a outras formas.
 * Premindo esse comando duas vezes, produzir-se-á o comportamento anterior e anunciará a informação da localização para o controle completo.
* Novo idioma: Catalão.

== Alterações ==
* Atualizado o transcritor braille liblouispara a versão 2.5.4. (#4103)

== Correcção de falhas ==
* No Google Chrome e navegadores baseados neste, certos blocos de texto (tais como os providos de ênfase) já não são repetidos quando é anunciado o texto de uma alerta ou diálogo. (#4066)
* No modo de navegação em aplicações Mozilla, premindo enter num botão, etc. já não falha para ativá-lo (ou ativa o controle errado) em certos casos, tal como os botões no topo  do Facebook. (#4106)
* Informações inúteis já não são anunciadas ao mover-se com tab no iTunes. (#4128)
* Em certas listas do iTunes tal como a lista Músicas, mover para o próximo item usando a navegação de objetos agora funciona corretamente. (#4129)
* Elementos HTML considerados como cabeçalhos devido a uma marca WAI ARIA agora são incluídos na lista de elementos do modo de navegação,  bem como na navegação rápida para documentos do Internet Explorer. (#4140)
* Ao ativar links para a mesma página em versões recentes do Internet Explorer, agora move para e anuncia corretamente a posição de destino em documentos do modo de navegação. (#4134)
* Microsoft Outlook 2010 e posterior: Foi melhorado o acesso especial a diálogos seguros como o de novos perfis e configuração de e-mail. (#4090, #4091, #4095)
* Microsoft Outlook: Anúncios inúteis foram diminuídos em barras de ferramentas de comandos ao navegar por certos diálogos. (#4096, #3407)
* Microsoft word: Ao mover-se com tab para a célula vazia de uma tabela,já não anuncia incorretamente o fim da mesma. (#4151)
* Microsoft Word: O primeiro caractere depois do fim de uma tabela (incluindo uma nova linha em branco) já não é considerado incorretamente como se estivesse dentro da tabela. (#4152)
* Diálogo de Verificação Ortográfica do Microsoft Word 2010: A atual palavra incorrecta é anunciada em lugar de anunciar incorrectamente a primeira palavra em negrito. (#3431)
* No modo de navegação no Internet Explorer e outros controles MSHTML, ao mover-se com tabb ou usando a navegação com um caractere para mover-se para campos de formulário, é novamente anunciada a etiqueta em muitos casos onde tal não ocorria (especificamente, onde são usadas etiquetas de elementos HTML). (#4170)
* Microsoft Word: O anúncio da existência e da localização de comentários agora é mais preciso. (#3528)
* A navegação de certos diálogos em produtos do MS Office tais como Word, Excel e Outlook foi melhorada de modo que já não anuncia barras de ferramentas que contém controles  sem utilidade particular para o utilizador. (#4198)
* Os painéis de tarefas, como o gestor da área de transferência ou recuperação de ficheiros, não mais aparentam ter ganhado foco ao abrir uma aplicação como o Microsoft Word ou Excel, o que às vezes obrigava o utilizador a alternar para fora e de volta ao a aplicação para usar o documento ou folha de cálculo. (#4199)
* O NVDA já não falha ao ser executado  em versões recentes do Windows   quando o idioma do sistema operativo é configurado para Sérvio (Latino). (#4203)
* Ao premir o numlock estando no modo ajuda de entrada agora alterna correctamente o numlock, ao invés de fazer com que o teclado e o Sistema operativa se descincronizem em relação ao estado dessa tecla. (#4226)
* No Google Chrome, o título do documento volta a ser anunciado quando se alterna separadores. No NVDA 2014.2, isso não ocorria em alguns casos. (#4222)
* No Google Chrome e navegadores baseados no Chrome, a URL do documento já não é anunciada ao anunciar o documento. (#4223)
* Ao executar uma leitura contínua com o sintetizador sem fala selecionado (útil para testes automatizados), a leitura contínua agora é completa ao invés de parar após poucas linhas. (#4225)
* Diálogo de assinatura do Microsoft Outlook: O campo de edição de assinatura agora é acessível, permitindo a completa deteccção do cursor e  da formatação. (#3833)
* Microsoft Word: Ao ler a última linha de uma célula de tabela, a célula já não é lida por completo. (#3421)
* Microsoft Word: Ao ler a primeira ou a última linha de um índice, o mesmo já não é lido por completo. (#3421)
* Ao falar palavras digitadas e em alguns outros casos, as palavras já não são quebradas incorrectamente  em marcas tais como sinais de vogais e virama em idiomas Indianos. (#4254)
* Campos de edição de texto numéricos no GoldWave agora são controlados correctamente. (#670)
* Microsoft Word: ao mover-se por parágrafo usando control+seta abaixo/control+seta acima, já não é necessário premir esses comandos  duas vezes para se mover por listas numeradas ou com marcas. (#3290) 

### Alterações específicas para programadores

Alguns itens ou termos desta secção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para programadores, bem como de difícil tradução exacta para o português. Todavia, os itens que possam ser relevantes para utilizadores comuns, serão traduzidos.

* O NVDA agora possui suporte unificado para a documentação dos seus extras. Consulte a secção Add-on Documentation do Developer Guide para mais detalhes. (#2694)
* When providing gesture bindings on a ScriptableObject via __gestures, it is now possible to provide the None keyword as the script. This unbinds the gesture in any base classes. (#4240)
-     It is now possible to change the shortcut key used to start NVDA for locales where the normal shortcut causes problems. (#2209)
 * This is done via gettext.
 * Note that the text for the Create desktop shortcut option in the Install NVDA dialog, as well as the shortcut key in the User Guide, must also be updated.

## 2014.2

### Novas características

* O anúncio da seleção de texto agora é possível em alguns campos de edição personalizados  onde a informação proveniente da tela é usada. (#770)
* em aplicativos Java acessíveis, a informação da posição agora é anunciada para botões de opção e outros controles que exibem a informação de grupo.. (#3754)
* em aplicativos Java acessíveis, as teclas de atalho agora são anunciadas para controles que os possuam. (#3881)
* No modo de navegação, as etiquetas nas marcas agora são anunciadas. São também incluídas no Diálogo da Lista de Elementos. (#1195)
* No modo de navegação, as regiões etiquetadas agora são tratadas como marcas. (#3741)
* em  documentos do Internet Explorer e aplicativos, Live Regions (partes do padrão ARIA W3c) são agora suportados, permitindo assim aos  autores web marcarem conteúdos particulares para serem anunciados automaticamente quando alterados. (#1846)

### Alterações

* Ao sair de um diálogo ou aplicação contida em um documento do modo de navegação, o nome e tipo do documento do modo de navegação já não são anunciados. (#4069)

### Correção de falhas

* O menu sistema padrão do Windows já não é silenciado acidentalmente em aplicativos Java. (#3882)
* Ao copiar textos via exploração de tela, as quebras de linha já não são ignoradas. (#3900)
* Objetos que constituem-se de espaços em branco sem utilidade já não são anunciados em alguns aplicativos quando o foco muda ou ao usar a navegação de objetos com o modo de revisão simples abilitado. (#3839)
* Caixas de texto e outros diálogos produzidos pelo NVDA voltam a fazer com que a fala anterior  seja cancelada antes do anúncio do diálogo.
* No modo de navegação, as etiquetas dos controles tais como links e botões agora são renderizadas corretamente caso a etiqueta tenha sido substituída pelo autor para propósitos de acessibilidade (especificamente, usando aria-label ou aria-labelledby). (#1354)
* No modo de navegação no Internet Explorer, o texto situado dentro de um elemento marcado como apresentacional (ARIA role="presentation") já não é inapropriadamente ignorado. (#4031)
* Agora é novamente possível digitar texto em Vietnamês usando o software Unikey. Para tanto, desmarque a nova caixa de seleção "Processar teclas de outros aplicativos" no Diálogo de Opções de Teclado do NVDA. (#4043)
* NO modo de navegação, os itens de rádio e itens de menu de seleção são agora anunciados como controles em lugar de o serem apenas como texto clicável. (#4092)
* O NVDA já não alterna incorretamente do modo de foco para o modo de navegação quando um item de radio ou de menu de seleção recebe foco. (#4092)
* No Microsoft PowerPoint com o anúncio de palavras digitadas ativado, caracteres deletados usando backspace já não são anunciados como parte da palavra digitada. (#3231)
* No Diálogo de Opções do Microsoft Office 2010, as etiquetas das caixas de combinação agora são anunciadas corretamente. (#4056)
* No modo de navegação em aplicativos da Mozilla, usando-se os comandos de navegação  rápida para mover-se para o próximo ou anterior botão ou campo de formulário, agora inclui botões de altenância como é esperado. (#4098)
* O conteúdo das alertas em aplicativos da Mozilla  já não é anunciado duas vezes. (#3481)
* No modo de navegação, elementos que contém outros, bem como as marcas já não são repetidas inapropriadamente ao navegar dentro dos mesmos, ao mesmo tempo em que o conteúdo das páginas é alterado  (exemplo, quando se navega pela página do Facebook e do Twitter). (#2199)
* O NVDA agora se recupera em mais casos ao alternar o foco para fora de aplicativos que pararam de responder. (#3825)

## 2014.1

### Novas características

* Suporte para o Microsoft PowerPoint 2013. Note que a visualização protegida não é suportada. (#3578)
* NO Microsoft word e Excel, o NVDA agora pode ler o símbolo selecionado quando se o escolhe usando o Diálogo de Inserção de Símbolos. (#3538)
* Agora é possível escolher se conteúdos em documentos devem ser identificados como clicáveis, por meio de uma nova opção no Diálogo de Opções de Formatação de Documentos. Essa opção está ativada por padrão, conforme o comportamento anterior. (#3556)
* Suporte para linhas braille conectadas via Bluetooth em computadores onde haja  o Software Widcomm Bluetooth. (#2418)
* Quando se edita textos no PowerPoint, os hyperlinks agora são anunciados. (#3416)
* Estando em aplicativos ARIA  ou diálogos na web, agora é possível forçar o NVDA a alternar para o modo de navegação com NVDA+espaço, o que permite navegar como em documentos pelo aplicativo ou diálogo. (#2023)
* No Outlook Express / Windows Mail / Windows Live Mail, o NVDA agora anuncia caso uma mensagem contenha anexo ou seja sinalizada. (#1594)
* Ao navegar em tabelas em aplicativos java acessíveis, são agora anunciadas coordenadas de linha e coluna, incluindo cabeçalhos de linha e coluna caso existam. (#3756)

### Alterações

* Para as linhas braile Papenmeier, o comando mover para a revisão plana/foco  foi removido. Os usuários poderão atribuir suas próprias teclas usando o Diálogo de Gestos de Entrada. (#3652)
* O NVDA agora utiliza-se do Microsoft VC runtime versão 11, o que significa que já não é mais possível executá-lo em sistemas operacionais mais antigos que o Windows XP Service Pack 2 ou o Windows Server 2003 Service Pack 1.
* No nível de Pontuação pouco agora serão falados os caracteres asterisco (*) e mais (+). (#3614)
* Atualizado o sintetizador eSpeak para a versão 1.48.04, o que inclui muitas correções nos idiomas e resolve vários problemas de instabilidades. (#3842, #3739), #3860)

### Correção de falhas

* Ao mover-se ao longo de ou selecionar células no Microsoft Excel, o NVDA já não deve anunciar inapropriadamente a célula anterior ao invés da atual quando o Microsoft Excel é lento ao mover a seleção. (#3558)
* O NVDA agora controla apropriadamente a abertura de listas suspensas para células no Microsoft Excel por meio do menu de contexto. (#3586)
* O conteúdo de uma nova página na página da loja do iTunes 11 agora é exibida adequadamente no modo de navegação ao entrar em um link da loja ou ao abrir a página da loja inicialmente. (#3625)
* Os botões para a pré-visualização de músicas na loja do iTunes 11 agora têm suas etiquetas exibidas no modo de navegação. (#3638)
* No modo de navegação no Google Chrome, as etiquetas  de caixas de seleção e botões de opção agora são renderizadas corretamente. (#1562) 
* No Instantbird, o NVDA já não exibe informações inúteis sempre que você move  para um contato na lista de contatos. (#2667)
* No modo de navegação no Adobe Reader, o texto correto agora é renderizado para botões, etc. onde a etiqueta tenha sido substituída por uma dica de ferramenta  ou afins. (#3640)
* No modo de navegação no Adobe Reader, gráficos estranhos contendo o texto "mc-ref" já não são renderizados. (#3645)
* O NVDA já não anuncia todas as células no Microsoft Excel como sublinhadas em suas informações de formatação. (#3669)
* Não se mostram mais caracteres sem sentido em documentos no modo de navegação, como aqueles encontrados no intervalo para uso privado do Unicode. Em alguns casos eles estavam impedindo etiquetas mais úteis de serem mostradas. (#2963)
* A composição de entrada para a introdução de caracteres asiáticos já não falha no PuTTY. (#3432)
* A navegação em um documento após cancelar a leitura contínua já não resulta em que o NVDA algumas vezes anuncie incorretamente  que você saiu de um campo (tal como uma tabela) no documento que a leitura contínua nunca anunciou. (#3688)
* Ao usar os comandos de navegação rápida do modo de navegação na leitura contínua com a leitura dinâmica abilitada, o NVDA anuncia o novo campo de modo mais acurado; ex.: anuncia um cabeçalho como cabeçalho e não apenas o texto do mesmo. (#3689)
* Os comandos de navegação rápida de pular para o fim ou início de elementos que contêm outros agora respeitam a opção de leitura dinâmica durante a leitura contínua, isto é, já não irão cancelar a leitura contínua atual. (#3675)
* Os nomes de gestos táteis listados no diálogo de gestos para entrada do NVDA agora estão amigáveis e traduzidos. (#3624)
* O NVDA já não faz com que certos programas travem ao mover o mouse por sobre seus controles de edição avançada (TRichEdit). Programas incluem o Jarte 5.1 e o BRFácil. (#3693, #3603, #3581)
* No Internet Explorer e outros controles MSHTML, objetos que contém outros como as tabelas marcadas com ARIA como sendo de leiaute não são mais anunciadas ao usuário. (#3713)
* No Microsoft Word, o NVDA já não repete inapropriadamente informações de linha e coluna de tabela para uma célula numa linha braile várias vezes. (#3702)
* Em idiomas que usam um espaço como indicador de grupo de algarismos/separador de milhar, como Francês e Alemão, números que pertençam a trechos separados de textos já não são pronunciados como um só número. Isso era particularmente problemático em tabelas contendo números. (#3698)
* O Braile já não deixa de atualizar-se algumas vezes quando o cursor do sistema é movido no Microsoft Word 2013. (#3784)
* Estando posicionado no primeiro caractere de um cabeçalho no Microsoft Word, o texto comunicando que se trata de um cabeçalho (incluindo o nível) já não  desaparece numa linha braile. (#3701)  
* Quando um perfil de configuração  é disparado para um aplicativo e aquele aplicativo é fechado, o NVDA já não deixa algumas vezes de desativar o perfio. (#3732)
* Ao inserir entradas Asiáticas num controle dentro do próprio NVDA (por exemplo no diálogo de procura do modo de navegação), "NVDA" já não é incorretamente anunciado no lugar da sugestão. (#3726)
* As guias no diálogo de opções do Outlook 2013 agora são anunciadas. (#3826)
* Melhorado suporte às "ARIA live regions" no Firefox e outros aplicativos Gecko da Mozilla:
 * Suporte a atualizações atômicas de aria e e filtragem de atualizações ocupadas com aria  (#2640)
 * O texto alternativo (como o atributo alt ou a etiqueta aria) é incluído caso não haja outro texto útil. (#3329)
 * As "live regions" não são mais silenciadas caso ocorram ao mesmo tempo que o foco se move. (#3777)
* Certos elementos de leiaute no Firefox e outros aplicativos gecko da Mozilla já não são mostrados inapropriadamente em modo de navegação (em específico, quando o elemento está marcado como aria-presentation mas é também focável). (#3781)
* Melhora na performance ao navegar em um documento no Microsoft Word com o anúncio de erros ortográficos ativado. (#3785) 
* Várias correções no suporte para aplicativos Java acessíveis:
 * O controle inicialmente com foco numa freime ou diálogo já não deixa de ser anunciado quando a freime ou diálogo vem a primeiro plano. (#3753)
 * Informações inúteis de posição já não são anunciadas para botões de opção (ex.: 1 de 1). (#3754)
 * Melhoras no anúncio de controles JComboBox  (html já não é anunciado, um melhor anúncio dos estados expandido e recolhido). (#3755)
 * Ao anunciar o texto de diálogos, alguns textos que anteriormente eram omitidos agora são incluídos. (#3757)
 * Alterações no nome, valor ou descrição do controle sob o foco agora são anunciadas mais precisamente. (#3770)
* Corrigida uma falha no NVDA constatada em Windows 8 ao focar num controle RichEdit contendo grande quantidade de texto (ex.: visualizador de log do NVDA, windbg). (#3867)
* Em sistemas configurados com alta resolução de monitor (que ocorre por padrão em muitas telas modernas), o NVDA já não move o mouse para a posição errada em alguns aplicativos. (#3758, #3703)
* Resolvido um problema ocasional ao navegar na web onde o NVDA poderia deixar de funcionar corretamente depois de reiniciado, ainda que não houvesse travado. (#3804)
* Uma linha braille Papenmeier agora pode ser usada mesmo que uma linha Papenmeier nunca haja sido conectada via USB. (#3712)
* O NVDA já não congela quando o modelo antigo de linha braille Papenmeier BRAILLEX é selecionado sem nenhuma linha conectada.

### Alterações específicas para desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* Os appModules agora contém as propriedades productName and productVersion. Essa informação agora  também é incluída no Developer Info (NVDA+f1). (#1625)
* No Console Python, você agora pode pressionar a tecla tab para completar o identificador atual. (#433)
 * Caso existam múltiplas possibilidads, é possível pressionar tab outra vez para selecionar a partir de uma  lista.

## 2013.3

### Novas características

* Campos de formulário agora são anunciados em documentos do Microsoft word. (#2295)
* O NVDA agora anuncia informações de revisão no Microsoft Word quando monitorar alterações está abilitado. Note que Anunciar revisões de editores, no diálogo de opções de documento do NVDA (desativada por padrão), tem que também estar abilitada para que elas sejam anunciadas. (#1670)
* Listas suspensas no Microsoft Excel 2003 a 2010 são agora anunciadas quando abertas e se navega ao longo delas. (#3382)
* Uma nova opção no diálogo de opções de teclado, "Permitir leitura dinâmica durante a leitura contínua", possibilita navegar ao longo dum documento com os comandos de navegação rápida e linha / parágrafo em modo de navegação e manter-se em leitura contínua. Essa opção está desativada por padrão. (#2766)
* Existe agora um diálogo de gestos de entrada com o fim de possibilitar uma personalização mais simples dos gestos de entrada (tais como as teclas do teclado) para comandos do NVDA. (#1532)
* Agora é possível ter diferentes opções para diferentes situações usando perfis de configuração. Os Perfis podem ser ativados manualmente ou automaticamente (isto é, para um aplicativo em particular). (#87, #667, #1913)
 * No Microsoft Excel, as células que são links agora são anunciadas como links. (#3042)
* No Microsoft Excel, a existência de comentários numa célula agora é anunciada para o usuário. (#2921)

### Correção de falhas

* O Zend Studio agora funciona igual ao Eclipse. (#3420)
* O estado alterado de certas caixas de seleção do diálogo de regras para mensagens do Microsoft Outlook 2010 agora é anunciado automaticamente. (#3063)
* O NVDA vai agora anunciar o estado "pregado" para controles pregados como as abas no Mozilla Firefox. (#3372)
* Agora é possível associar scripts a gestos de teclado que contenham Alt e/ou Windows como teclas modificadoras. Se isso fosse feito anteriormente, executar o script faria com que fosse ativado o Menu Iniciar ou a barra de menus. (#3472)
* Selecionar textos em documentos no modo de navegação (usando por exemplo control+shift+end) já não altera a disposição de teclado em sistemas com várias disposições de teclado instaladas. (#3472)
* O Internet Explorer não deve mais travar ou ficar inutilizado ao fechar o NVDA. (#3397)
* Movimentos físicos e outros eventos em computadores recentes não são mais tratados como pressionamentos inapropriados de teclas. Anteriormente, os mesmos silenciavam a fala e às vezes chamavam comandos do NVDA. (#3468)
* Agora o NVDA se comporta como esperado no Poedit 1.5.7. Usuários de versões mais antigas terão de atualizar. (#3485)
* O NVDA agora consegue ler documentos protegidos no Microsoft Word 2010 sem ffazer com que o Microsoft Word trave. (#1686)
* Caso seja fornecida uma opção de linha de comando desconhecida ao carregar o pacote de distribuição do NVDA, entra não entra mais num ciclo infinito de diálogos de mensagem de erro. (#3463)
* O NVDA já não deixa de anunciar textos de descrições de gráficos e objetos no Microsoft Word caso os mesmos contenham aspas ou outros caracteres não padrão. (#3579)
* O número de itens de certas listas horizontais em modo de navegação agora fica correto. Anteriormente poderia ser o dobro da quantidade real. (#2151)
* Ao pressionar control+a numa planilha do Microsoft Excel, a seleção atualizada agora será anunciada. (#3043)
* O NVDA agora pode ler corretamente documentos XHTML no Microsoft Internet Explorer e em outros controles MSHTML. (#3542)
* Diálogo de opções de teclado: Se nenhuma tecla for escolhida para uso como tecla do NVDA, um erro é apresentado ao usuário ao fechar o diálogo. Deve ser escolhida pelo menos uma tecla para uso adequado do NVDA. (#2871)
* No Microsoft Excel, o NVDA agora anuncia células mescladas de modo diferente de várias células selecionadas. (#3567)
* O cursor do modo de navegação já não é posicionado incorretamente quando se encerra um diálogo ou aplicativo dentro do documento. (#3145)
* Corrigido um problema no qual o driver da linha braile HumanWare Brailliant BI/B series não era apresentado como opção no diálogo de opções de braile em alguns sistemas, mesmo que essa linha estivesse conectada via USB.
* O NVDA já não deixa de alternar para a exploração de tela quando o objeto de navegação atual não possui localização na tela. Nesse caso, o cursor de exploração agora é colocado no topo da tela. (#3454)
* Resolvido um problema que fazia com que o driver para as linhas braille da Freedom Scientific falhasse quando a porta era definida para USB em algumas circunstâncias. (#3509, #3662)
* Resolvido um problema onde as teclas de linhas braile da Freedom Scientific não eram  detectadas em algumas circunstâncias. (#3401, #3662)

### Alterações específicas para desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* Você pode especificar a categoria a ser mostrada ao usuário para scripts usando o atributo scriptCategory em classes  ScriptableObject e o atributo category em métodos script. Consulte a documentação da baseObject.ScriptableObject para mais detalhes. (#1532)
* config.save foi descontinuado e pode ser removido numa versão futura. Use config.conf.save em seu lugar. (#667)
* config.validateConfig foi descontinuado e pode ser removido numa versão futura. Complementos que precisem do mesmo devem prover implementações próprias. (#667, #3632)

## 2013.2

### Novas Características

* Suporte ao Chromium Embedded Framework, que é um controle de navegação web usado em vários aplicativos. (#3108)
* Nova variante de voz do ESpeak: Iven3.
* No Skype, mensagens novas de chat são anunciadas automaticamente quando a conversa está com foco. (#2298)
* Suporte ao Tween, incluindo anúncio dos nomes de abas e menos verbosidade ao ler twites.
* Agora você pode desabilitar a exibição de mensagens do NVDA numa linha braile ajustando o tempo limite de mensagem para 0 na janela de Opções de braile. (#2482)
* No gestor de complementos existe agora um botão Baixar Complementos para abrir a página de complementos do NVDA, onde pode navegar e descarregar complementos. (#3209)
* Na janela de boas vindas do NVDA, que aparece quando se executa o NVDA pela primeira vez, você agora pode determinar se o NVDA inicia automaticamente após fazer logon no Windows. (#2234)
* O modo dormir é ativado automaticamente ao usar o Dolphin Cicero. (#2055)
* A versão x64 do Miranda IM/Miranda NG agora é suportada. (#3296)
* As sugestões de pesquisa na tela inicial do Windows 8.1 agora são anunciadas. (#3322)
* Suporte à navegação e edição de planilhas no Microsoft Excel 2013. (#3360)
* As linhas braile Focus 14 Blue e Focus 80 Blue da Freedom Scientific, bem como a Focus 40 Blue em determinadas configurações que não eram suportadas antes, são agora suportadas quando conectada via bluetooth. (#3307)
* As sugestões de auto completar agora são anunciadas no Outlook 2010. (#2816)
* Novas tabelas de tradução braille: Inglês (U.K.) braille de computador, Coreano grau 2, código braille Russo para computador.
* Novo idioma: Persa. (#1427)

### Alterações

* Em telas táteis, agora varrer com o só dedo para esquerda ou direita estando no modo de objeto vai para o anterior ou o próximo ao longo de todos os objetos e não apenas daqueles no objeto pai atual. Use a varredura com dois dedos para esquerda ou direita para navegar pelo objeto anterior/seguinte da forma original, por aqueles do objeto pai atual.
* A caixa de seleção "Anunciar Tabelas de Leiaute", encontrada no Diálogo de Opções do Modo de Navegação, foi renomeada para "Incluir Tabelas de Leiaute", para enfatizar que as teclas de navegação rápida também não as localizarão se a caixa de seleção estiver desmarcada. (#3140)
* A revisão plana foi substituída pelos modos de exploração de objeto, de documento e de tela. (#2996)
 * A exploração de objeto explora somente o texto contido no objeto de navegação, a exploração de documento explora todo o texto dum documento em modo de navegação (se houver) e a exploração de tela explora o texto na tela relacionado ao aplicativo atual.
 * Os comandos que antes moviam para/da revisão plana agora alternam entre esses modos de exploração.
 * O objeto de navegação segue automaticamente o cursor de exploração de modo a ser sempre o objeto mais ancestral na posição do cursor de exploração quando nos modos de documento e de tela.
 * Após mudar para o modo de exploração de tela, o NVDA permanecerá nesse modo até que você mude explicitamente para o modo de exploração de documento ou o de objeto.
 * No modo de exploração de documento ou de objeto, o NVDA pode trocar entre esses dois modos dependendo se você estiver se movendo por um documento em modo de navegação ou não.
* Atualizado o transcritor braile liblouis para a versão 2.5.3. (#3371)

### Correção de falhas

* Agora ativar um objeto anuncia a ação antes da ativação ao invés de a ação depois da ativação (por exemplo: expandido ao expandir ao invés de recolhido). (#2982)
* Leitura e rastreamento do cursor mais precisos em vários campos de entrada de versões recentes do Skype, como o chat e campos de busca. (#1601, #3036)
* Na lista de conversas recentes do Skype, o número de novos eventos agora é lido para cada conversa caso relevante. (#1446)
* Melhorias no rastreamento do cursor e na ordem de leitura em textos da direita para a esquerda na tela; por exemplo ao editar textos em Árabe no Microsoft Excel. (#1601)
* A navegação rápida para botões e campos de formulário vai agora se posicionar em linques marcados como botões para fins de acessibilidade no Internet Explorer. (#2750)
* No modo de navegação, não se renderiza mais o conteúdo de árvores, já que uma representação plana é inútil. Você pode pressionar Enter numa árvore para interagir com a mesma em modo de foco. (#3023)
* Pressionar Alt+seta baixo ou Alt+seta cima para expandir uma caixa de combinação estando em modo de foco não alterna mais para modo de navegação. (#2340)
* No internet Explorer 10, células de tabela não ativam mais o modo de foco a não ser que elas tenham sido explicitamente marcadas como focáveis pelo autor da página. (#3248)
* O NVDA não se recusa mais a iniciar se a hora do sistema for anterior à última procura por atualizações. (#3260)
* Caso uma barra de progresso seja mostrada numa linha braile, a linha é atualizada quando a barra é alterada. (#3258)
* No modo de navegação em aplicativos Mozilla, legendas  de tabelas não são mais renderizadas duas vezes. Além disso, renderiza-se o sumário quando há uma legenda. (#3196)
* Ao trocar o idioma de entrada no Windows 8, o NVDA agora fala o idioma correto e não o anterior.
* O NVDA agora anuncia mudanças de modos de conversão de IME no Windows 8.
* O NVDA não anuncia mais conteúdo inútil na área de trabalho quando os métodos de entrada IME Google Japonês ou Atok estão em uso. (#3234)
* No Windows 7 e posteriores, o NVDA não mais anuncia de modo inapropriado reconhecimento de voz ou entrada tátil quando se troca o idioma de teclado.
* O NVDA não anuncia mais um caractere especial em particular (0x7f) ao pressionar control+backspace em alguns editores quando falar caracteres digitados estiver abilitado. (#3315)
* O eSpeak não mais muda inapropriadamente de tom, volume, etc. quando o NVDA lê textos que contenham certos caracteres de controle ou XML. (#3334) (regressão do #437)
* Em aplicativos Java, mudanças de rótulo ou valor no controle em foco agora são automaticamente anunciadas e se refletem ao chamar novamente o controle. (#3119)
* Em controles Scintilla as linhas agora são anunciadas de modo correto quando quebrar linhas está abilitado. (#885)
* Em aplicativos Mozilla, os nomes de itens de lista somente-leitura são anunciados corretamente; por exemplo ao navegar por twites em modo de foco no twitter.com. (#3327)
* Diálogos de confirmação no Microsoft Office 2013 agora têm seu conteúdo automaticamente lido quando aparecem.
* Melhorias de desempenho ao navegar em certas tabelas no Microsoft Word. (#3326)
* Os comandos de navegação em tabelas do NVDA (control+alt+setas) funcionam melhor em certas tabelas do Microsoft Word nas quais uma célula abrange várias linhas.
* Caso o gestor de complementos já esteja aberto, ativá-lo de novo (seja pelo menu ferramentas ou abrindo um arquivo de complemento) não mais causa falha nem torna impossível fechar o gestor de complementos. (#3351)
* O NVDA não congela mais em certos diálogos quando o IME Chinês ou Japonês do Office 2010 está em uso. (#3064)
* Vários espaços não são mais comprimidos para um só espaço em linhas braile. (#1366)
* O Zend Eclipse PHP Developer Tools agora funciona da mesma forma que o Eclipse. (#3353)
* No Internet Explorer, voltou a não ser necessário pressionar tab para interagir com um objeto embutido (como o conteúdo Flash) depois de pressionar Enter nele. (#3364)
* Ao editar textos no Microsoft PowerPoint, a última linha não é mais anunciada como a linha acima se a linha final estiver em branco. (#3403)
* No Microsoft PowerPoint, os objetos não são mais falados em dobro às vezes quando você os seleciona ou escolhe editá-los. (#3394)
* O NVDA não faz mais o Adobe Reader encerrar ou congelar em certos documentos PDF mal-feitos que contém linhas fora de tabelas. (#3399)
* O NVDA agora detecta corretamente o próximo slaide com foco ao apagar um slaide no visualizador de miniaturas do Microsoft PowerPoint. (#3415)

### Alterações Específicas Para desenvolvedores

 Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* windowUtils.findDescendantWindow foi adicionado para buscar uma janela descendente (HWND) que corresponda à visibilidade especificada, ID de controle e/ou nome de classe.
* O console Python remoto não tem mais o tempo limite de 10 segundos ao esperar entrada. (#3126)
* A inclusão do módulo bisect compilado em forma binária foi descontinuada e pode ser removido em versões futuras. (#3368)
 * Complementos que dependam do bisect (incluindo o módulo urllib2) devem ser atualizados para incluir esse módulo.

## 2013.1.1

Esta versão corrige o problema de o NVDA travar ao iniciar quando configurado para  usar o idioma Irlandês, bem como inclui atualizações de traduções e outras correções de falhas.

### Correção de Falhas

* São agora produzidos os caracteres corretos quando se digita  na própria interface do usuário do NVDA usando um  método de entrada Coreano ou Japonês e sendo este o método de entrada padrão. (#2909)
* No Internet Explorer e outros controles MSHTML, campos marcados como contendo uma entrada inválida agora são controlados corretamente. (#3256)
* O NVDA não trava mais ao iniciar quando configurado para usar o idioma Irlandês.

## 2013.1

 Entre os destaques desta versão incluem-se um leiaute de teclado mais intuitivo e consistente para laptops; suporte básico  para o Microsoft PowerPoint; suporte para descrições longas  em navegadores web; e suporte para a entrada de braille para computador em linhas que possuam um teclado braille.

### Importante

#### Novo Leiaute de teclado Laptop

O leiaute de teclado laptop foi completamente redesenhado com vista a tornar-se mais intuitivo e consistente.
Esse novo esquema usa as setas em combinação com a tecla NVDA e outras teclas modificadoras para os comandos de exploração e navegação de objetos.

Deve-se notar as seguintes alterações para comandos comumente usados:

| Nome |Tecla|
|---|---|
|Leitura contínua |NVDA+a|
|Ler linha atual |NVDA+l|
|Ler texto atualmente selecionado |NVDA+shift+s|
|Ler a barra de status |NVDA+shift+end|

Addicionalmente, várias outras mudanças, todos os comandos da navegação de objetos, revisão de textos, clique do mouse e anel  de configuração de voz foram alterados.
Por favor consulte o documento da [Referência Rápida de Comandos](keyCommands.html) para as novas teclas.

### Novas Características

* Suporte básico  para a edição e leitura de apresentações no Microsoft PowerPoint. (#501)
* Suporte para alternância automática  de idiomas durante a leitura de documentos no Microsoft Word. (#2047)
* Suporte básico para leitura e escrita de mensagens no Lotus Notes 8.5. (#543)
* No modo de navegação para o MSHTML (como o  Internet Explorer) e Gecko (Firefox), a existência de descrições longas agora é anunciada. Também é possível abrir a descrição longa numa nova janela pressionando NVDA+d. (#809)
* Notificações no Internet Explorer 9 e posteriores (tais como bloqueio de conteúdos ou downloads de arquivos) agora são anunciadas. (#2343) 
* O anúncio automático dos cabeçalhos de linhas e colunas das tabelas agora é suportado para documentos do modo de navegação  no Internet Explorer e outros controles MSHTML. (#778) 
* Novos idiomas: Aragonês, Irlandês.
* Novas tabelas de tradução braille: Dinamarquês grau 2, Coreano grau 1. (#2737)
* Suporte para linhas braille conectadas via bluetooth em computadores que usem dispositivos Bluetooth para o Windows fabricados pela Toshiba. (#2419)
* Novas opções de teclado que permitem escolher se o NVDA deve interromper a fala quando são digitados caracteres e/ou a tecla Enter. (#698)
* Suporte para seleção de porta quando se usa linhas da freedom Scientific  (Automática, USB ou Bluetooth). 
* Suporte para a família de notetakers BrailleNote da Humanware quando usados com função de terminal braille para leitores de telas. (#2012)
* Suporte para modelos antigos das linhas braille Papenmeier BRAILLEX. (#2679)
* Suporte para entrada de braille de computador em  linhas que possuam um teclado braille. (#808)
* Suporte para vários navegadores  baseados no Google Chrome: Rockmelt, BlackHawk, Comodo Dragon e SRWare Iron. (#2236, #2813, #2814, #2815)

### Alterações

* Atualizado o transcritor braille liblouis para a versão 2.5.2. (#2737)
* O leiaute de teclado laptop foi completamente redesenhado com vista a tornar-se mais intuitivo e consistente. (#804)
* Atualizado o sintetizador eSpeak para a versão 1.47.11. (#2680, #3124, #3132, #3141, #3143), , #3172)

### Correção de Falhas

* As teclas de navegação rápida para saltar para o separador anterior e o seguinte no modo de navegação agora funcionam no Internet Explorer e outros controles MSHTML. (#2781)
* Caso o NVDA precise retornar ao eSpeak ou à opção sem fala devido à falha num sintetizador selecionado quando o NVDA é iniciado, a configuração já não é atualizada para definir o sintetizador que o substituiu como o escolhido, o que significa que agora o sintetizador original será novamente testado na próxima vez que o NVDA for iniciado. (#2589) 
* Caso o NVDA volte à configuração sem braille devido a alguma falha na linha braille configurada a quando do início do NVDA, a linha configurada já não é definida automaticamente  para sem braille. Isso significa que agora, a opção original será novamente escolhida na próxima vez que o NVDA for iniciado. (#2264) 
* No modo de navegação em aplicativos da Mozilla, atualizações em tabelas agora são exibidas  corretamente. Por exemplo, em  células atualizadas, as coordenadas das linhas e colunas são anunciadas e a navegação pela tabela funciona como deveria. (#2784) 
* No modo de navegação em navegadores web , certos gráficos clicáveis não etiquetados que anteriormente não eram expostos agora o são corretamente. (#2838) 
* Versões anteriores e mais recentes do SecureCRT agora são suportadas. (#2800) ----
* Em métodos de entrada tais como o Easy Dots IME no Windows XP, a cadeia de leitura agora é anunciada corretamente. 
* A lista de sugestões  no  método de entrada Microsoft Pinyin para Chinês Simplificado no Windows 7 agora é lida corretamente quando se muda  de página com as setas para a direita e esquerda, bem como ao abri-la num primeiro momento com a tecla Home.
* Quando as informações de personalizações de pontuação são salvas, o campo avançado "preserve" já não é removido. (#2852)
* Quando a procura automática por atualização é desabilitada, o NVDA já não precisa ser reiniciado para que a alteração faça efeito completamente. 
* O NVDA já não falha ao iniciar caso um complemento não possa ser removido pelo fato de sua pasta estar sendo usada no momento por outro aplicativo. (#2860) 
* As etiquetas das guias no diálogo de preferências do DropBox agora podem ser vistas usando a revisão plana. 
* Caso o idioma de entrada seja alterado para outro que não o padrão, o NVDA agora detecta corretamente as teclas em comandos e no modo de ajuda de entrada.
* Para idiomas como o alemão onde o sinal de + (plus, mais) consiste de uma única tecla no teclado, agora é possível vincular comandos a este sinal usando a palavra "plus". (#2898)
* No Internet Explorer e outros controles MSHTML, os blocos de citação agora são anunciados apropriadamente. (#2888)
* O driver para as linhas braille HumanWare Brailliant BI/B series agora pode ser selecionado quando a linha é conectada via Bluetooth mas nunca havia sido conectada via USB.
* ao filtrar elementos na lista de elementos do Modo de navegação usando textos que contenham letras maiúsculas, agora retorna resultados de casos insensíveis assim como minúsculas em lugar de não trazer qualquer resultado. (#2951) 
* em navegadores da Mozilla, o modo de navegação volta a poder ser usado quando conteúdo Flash recebe  foco. (#2546) 
* Ao usar uma tabela de braille contraído   e estando ativada a opção expandir para braille de computador a palavra sob o cursor, o cursor braille agora é posicionado corretamente quando colocado depois de uma palavra na qual haja um caractere representado por múltiplas celas braille (como sinal de maiúsculo, sinal de letras, sinal de números, etc.). (#2947) 
* A seleção de Textos agora é exibida corretamente pelas linhas braille nos controles editáveis em aplicativos como o Microsoft word 2003 e Internet Explorer. 
* Volta a ser possível selecionar textos em retrocesso no Microsoft Word enquanto o Braille está ativado. 
* Ao revisar, apagar para trás ou com delete os caracteres em controles editáveis Scintilla, o NVDA agora anuncia corretamente os caracteres multibyte. (#2855)
* o NVDA já não falha ao ser instalado quando o caminho para o perfil do usuário contém certos caracteres multibyte. (#2729) 
* O anúncio de grupos para controles de Visualização de Lista (SysListview32) em aplicativos de 64-bit já não causa um erro. 
* No modo de navegação em aplicativos da Mozilla, conteúdos de texto já não são tratados incorretamente como editáveis em alguns casos raros. (#2959) 
* No IBM Lotus Symphony e OpenOffice, ao mover-se o cursor do sistema agora move o cursor de revisão caso seja apropriado. 
* Conteúdos Flash agora são acessíveis com o Internet Explorer no Windows 8. (#2454) 
* Corrigido o suporte de Bluetooth para a linha braille Papenmeier Braillex Trio. (#2995)
* Corrigida a incapacidade para usar certas vozes Microsoft Speech API versão 5 tais como as vozes Koba Speech 2. (#2629)
* Em aplicações que usam Java Access Bridge, as linhas braille agora são atualizadas corretamente quando o cursor é movido em campos de edição de texto. (#3107)
Suporte para marcas de formulários em documentos no modo de navegação, caso suportem marcas. (#2997) 
 * O driver para o sintetizador eSpeak agora controla a leitura por caractere mais apropriadamente (por exemplo, anuncia o nome de uma letra ou seu valor ao invés de falar apenas seu som ou seu nome genérico). (#3106)
* O NVDA já não falha ao copiar configurações do usuário para uso no logon e outras telas seguras, quando o caminho do perfil do usuário contém caracteres não-ascii. (#3092)
* O NVDA já não trava quando se usa a entrada de caracteres Asiáticos  em alguns aplicativos .NET. (#3005)
* Agora é possível usar o modo de navegação para páginas no Internet Explorer 10 em modos standards; um exemplo é a página de login [www.gmail.com](http://www.gmail.com). (#3151)

### Alterações Específicas para Desenvolvedores

 Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* Os drivers para linhas braille agora podem suportar a seleção manual de portas. (#426)
 * This is most useful for braille displays which support connection via a legacy serial port. 
 * This is done using the getPossiblePorts class method on the BrailleDisplayDriver class. 
* A entrada de Braille a partir de teclados braille agora [e suportada. (#808) 
 * Braille input is encompassed by the brailleInput.BrailleInputGesture class or a subclass thereof. 
 * Subclasses of braille.BrailleDisplayGesture (as implemented in braille display drivers) can also inherit from brailleInput.BrailleInputGesture. This allows display commands and braille input to be handled by the same gesture class. 
* You can now use comHelper.getActiveObject to get an active COM object from a normal process when NVDA is running with the UIAccess privilege. (#2483)

## 2012.3

Entre os destaques desta versão estão inclusos o suporte para entrada de caracteres asiáticos; suporte experimental para touch screens no Windows 8; anúncio do número das páginas e melhoras no suporte para tabelas no Adobe Reader; comandos para navegação por tabelas   em linhas de tabelas enfocadas e controles de listas de visualização  do Windows; suporte para mais uma porção de linhas braille; e anúncio dos cabeçalhos de linhas e colunas no Microsoft Excel. 

### Novas Características

* O NVDA agora pode oferecer suporte à entrada de caracteres asiáticos que usam IME e o serviço de métodos de entrada de textos em todas as aplicações, Incluindo:
 * Anúncio e navegação das listas de sugestões;
 * Anúncio e navegação das cadeias de composição;
 * Anúncio das cadeias de leitura.
* A presença de sublinhado e taxado agora é anunciada em documentos do Adobe Reader. (#2410)
* Quando a função de teclas de aderência  estiver ativada no Windows, a tecla modificadora do NVDA agora se comportará como outras teclas modificadoras. Isto lhe permite usar a tecla modificadora do NVDA sem que precise mantê-la pressionada enquanto pressiona outras teclas. (#230)
* O anúncio automatico dos cabeçalhos das linhas e colunas agora é suportado no Microsoft Excel. Pressione NVDA+shift+c para selecionar a linha que contém os cabeçalhos das colunas e NVDA+shift+r para selecionar a coluna que contém os cabeçalhos das linhas. Pressione esses mesmos comandos duas vezes em rápida sucessão se pretender limpar a configuração feita. (#1519) 
* Suporte para as linhas Braille Sense, Braille EDGE e SyncBraille da HIMS. (#1266, #1267)
* Quando as notificações no Windows 8  aparecem, o NVDA as anuncia e move a navegação de objetos para o local, permitindo uma interação adicional. (#2143)
* Suporte experimental para Touch screens no Windows 8, incluindo:
 * Leitura de textos diretamente por onde você move seus dedos
 * Vários gestos para executar a navegação de objetos, revisão de textos, e outros comandos do NVDA.
* Suporte para o VIP Mud. (#1728)
* No Adobe Reader, caso uma tabela possua um sumário, ele agora será apresentado. (#2465)
* No Adobe Reader, os cabeçalhos de linhas e colunas das tabelas agora podem ser anunciados. (#2193)
* Novos idiomas: amárico, coreano, nepalês, esloveno.
* O NVDA agora pode ler sugestões de auto-completar quando se digita endereços de email no Microsoft Outlook 2007. (#689)
* Novas variantes para o eSpeak: Gene, Gene2. (#2512)
* No Adobe Reader, o número das páginas agora pode ser anunciado. (#2534)
* Agora é possível retornar as configurações do NVDA aos padrões originais pressionando NVDA+control+r três vezes rapidamente ou indo ao menu do NVDA e selecionando Restaurar Configuração aos Padrões Originais. (#2086)
* Suporte para as linhas braille Seika Versões 3, 4 e 5 e Seika80 da Nippon Telesoft. (#2452)
* Nas linhas braille PAC Mate e Focus da Freedom Scientific, o primeiro e o último botões de sensores de cima agora podem ser utilizados para deslocar-se para trás e para a frente. (#2556)
* Muito mais recursos são agora suportados nas Linhas braille Focus da Freedom Scientific, tais como advance bars, rocker bars e certas combinações de pontos para ações comuns. (#2516)
* Em aplicativos que usam IAccessible2 tais como os da Mozilla, os cabeçalhos de linhas e colunas das tabelas agora podem ser anunciados fora do modo de navegação. (#926)
* Suporte primário para o controle de documentos no Microsoft Word 2013. (#2543)
* O alinhamento dos textos agora pode ser anunciado em aplicativos que usam IAccessible2 tais como aplicativos da Mozilla. (#2612)
* Quando uma linha de uma tabela ou um controle de visualização de lista  padrão do Windows que possua  múltiplas colunas recebe foco, você agora pode acessar individualmente as células usando os comandos para navegação de tabelas. (#828)
* Novas tabelas de tradução braille: Estoniano grau 0, braille de 8 pontos Português para computador, braille de 6 pontos italiano para computador. (#2139, #2662)
* Caso o NVDA esteja instalado no computador, ao abrir diretamente um pacote de complemento (isto é, a partir do Windows Explorer ou depois de baixá-lo por um navegador web) instala-lo-á no NVDA. (#2306) 
* Suporte para os novos modelos das linhas braille Papenmeier BRAILLEX. (#1265)
* A informação da posição (isto é 1 de 4)  agora é anunciada para itens de listas do Windows Explorer  no Windows 7 e posteriores. Isto também inclui quaisquer controles UIAutomation que suportem as propriedades itemIndex e itemCount. (#2643) 

### Alterações

* No Diálogo de Opções do   Cursor de Exploração do NVDA , a opção Acompanhar foco do teclado  foi renomeada para Acompanhar foco do sistema para tornar-se consistente com a terminologia comumente empregada no NVDA.
* Quando o braille está vinculado à exploração e o cursor está em um objeto que não é um objeto de texto (isto é, um campo de edição de texto), as teclas sensores agora irão ativar o objeto. (#2386)
* A opção Salvar Configuração ao Sair agora está ativada por padrão para novas configurações.
* Ao atualizar uma cópia anteriormente instalada do NVDA, a tecla de atalho da área de trabalho já não é restaurada para control+alt+n caso tenha sido alterada manualmente para outra diferente pelo usuário. (#2572)
* A lista do gestor de complementos agora mostra o nome do pacote antes de seu status. (#2548)
* caso esteja instalando a mesma  ou outra versão de um complemento atualmente instalado, o NVDA irá perguntar se você deseja remover antes o antigo ao invés de simplesmente exibir uma mensagem de erro e abortar a instalação. (#2501)
* Os comandos da navegação de objetos (exceto o comando anunciar o objeto atual) agora o anuncia com menos verbosidade. Você ainda pode obter informação extra usando o comando anunciar o objeto atual. (#2560)
* Atualizado o transcritor braille liblouis para a versão 2.5.1.
* O documento Referência Rápida de Teclas de Comando foi renomeado para Referência Rápida de Comandos, visto que agora inclui tanto comandos para touch screen como de teclado.
* A lista de elementos no modo de navegação agora relembrará o último tipo de elemento mostrado (isto é, links, cabeçalhos ou marcas) a cada vez que o diálogo for exibido na mesma sessão do NVDA. (#365) 
* Vários aplicativos de estilo Metro no Windows 8 (Mail, Calendário) já não ativam o Modo de navegação para o aplicativo inteiro. 
* Atualizado o Handy Tech BrailleDriver COM-Server para a versão 1.4.2.0. 

### Correção de Falhas

* NO Windows Vista e posteriores, o NVDA já não trata incorretamente a tecla do Windows como se esta estivesse pressionada quando se o desbloqueia depois de bloquiá-lo pressionando Windows+l. (#1856)
* No Adobe Reader, os cabeçalhos das linhas agora são reconhecidos apropriadamente como células de tabelas; ou seja, as coordenadas são anunciadas e os mesmos podem ser acessados usando os comandos de navegação em tabelas. (#2444)
* No Adobe Reader, as células de tabelas que abrangem mais de uma coluna e/ou linha agora são controladas corretamente. (#2437, #2438, #2450)
* O NVDA agora verifica a integridade de seu pacote de distribuição antes de executar. (#2475)
* Os arquivos temporários de download do NVDA agora são removidos caso haja uma falha ao baixar atualizações. (#2477)
* Ao copiar as configurações do usuário para as configurações do sistema (permitindo seu uso no logon do Windows e outras telas seguras) o NVDA já não travará durante esse processo. (#2485) 
* Os mozaicos na tela de início do Windows 8 agora são melhor apresentados em voz e braille. O nome já não é repetido, em todos os mozaicos já não será dito não selecionado, e a informação ao vivo do status é apresentada como a descrição do mozaico (por exemplo, a temperatura para o mozaico do tempo).
* As senhas já não são anunciadas quando se lê campos de senhas no Microsoft Outlook e outros controles padrões de edição que são marcados como protegidos. (#2021)
* No Adobe Reader, as alterações em campos de formulários agora são refletidas corretamente  no modo de navegação. (#2529)
* Melhoras no suporte ao Verificador Ortográfico do Microsoft Word , incluindo uma leitura mais exata do erro ortográfico atual, e suporte à verificação ortográfica quando se executa uma cópia instalada do NVDA no Windows Vista ou posteriores.
* Complementos que contam com arquivos contendo caracteres não ingleses agora podem ser instalados corretamente em maior parte dos casos. (#2505)
* No Adobe Reader, o idioma dos textos já não é perdido quando este é atualizado ou ao se deslocar por ele. (#2544)
* Ao instalar um complemento, o diálogo de confirmação agora exibe corretamente o nome traduzido do mesmo caso disponível. (#2422)
* Em aplicativos que usam UI Automation, (tais como .net and Silverlight), foi corrigido o cáuculo de valores numéricos para controles como barras deslisantes. (#2417)
* A configuração para o anúncio de barras de progresso agora é responsável pelas barras de progresso indeterminadas que o NVDA mostra ao instalar, criar cópia portátil, etc. (#2574)
* Comandos do NVDA já não podem ser executados a partir de uma linha braille enquanto uma tela segura do Windows (como a tela de bloqueio) encontra-se ativa. (#2449)
* NO modo de navegação, o braille agora é atualizado se o texto que está sendo mostrado for alterado. (#2074)
* Estando em uma tela segura do Windows, como por exemplo a tela de bloqueio, as mensagens oriundas de aplicativos em voz ou braille diretamente via NVDA serão agora ignoradas.
* No modo de navegação, já não é possível ir além do final de um documento com a seta a direita caso esteja no último caractere, ou saltando para o fim de uma lista ou tabela quando esta for o último item deste documento. (#2463)
* Conteúdos Estranhos já não são inclusos incorretamente a quando do anúncio do texto de diálogos em aplicativos web (especificamente, diálogos ARIA que não possuem o atributo aria-describedby). (#2390)
* O NVDA já não anuncia ou situa incorretamente determinados campos de edição em documentos MSHTML (tais como Internet Explorer), especificamente onde uma função ARIA explicita tenha sido usada pelo autor da página web. (#2435)
* A tecla backspace agora é controlada corretamente ao falar palavras digitadas em consoles de comando do Windows. (#2586)
* As coordenadas de células no Microsoft Excell voltam a ser mostradas em Braille.
* No Microsoft Word, o NVDA já não lhe deixa preso em um parágrafo com formato de lista ao tentar navegar para fora de uma marca ou numeração com a seta a esquerda ou control + seta a esquerda. (#2402)
* No modo de navegação em aplicativos da Mozilla, os items em determinadas caixas de lista (especificamente em caixas de lista da ARIA) já não são dispostos incorretamente.
* No modo de navegação em aplicativos da Mozilla, certos controles que eram apresentados com uma etiqueta incorreta ou apenas com um espaço em branco agora são apresentados com a etiqueta correta. 
* No modo de navegação em aplicativos da Mozilla, alguns estranhos espaços em branco foram eliminados. 
* No modo de navegação em navegadores web, certos gráficos que estão marcados explicitamente como apresentacionais (especificamente, com um atributo alt="") agora são corretamente ignorados. 
* Em navegadores web, o NVDA agora oculta o conteúdo que está marcado como oculto para leitores de telas (especificamente, usando o atributo aria-hidden). (#2117)
* Quantias negativas de dinheiro (como -$123) agora são anunciadas corretamente  como negativas, independentemente do grau de sinais. (#2625)
* O NVDA já não retorna incorretamente ao idioma padrão durante uma leitura contínua onde uma linha não termina uma sentença. (#2630)
* A informação da fonte agora é detectada corretamente no Adobe Reader 10.1 e posteriores. (#2175)
* No Adobe Reader, caso haja um texto de descrição, somente aquele texto será exibido. Anteriormente, algumas vezes, textos estranhos eram inclusos. (#2174)
* Onde um documento contém uma aplicação, o conteúdo da mesma já não é incluido no modo de navegação. Isso evita que você se mova por dentro da aplicação ao navegar. É possível interagir com a aplicação da mesma forma utilizada com os objetos embutidos. (#990)
* Em aplicativos da Mozilla, os valores dos botões de rotação agora são anunciados corretamente quando alterados. (#2653)
* Atualizado o suporte para o Adobe Digital Editions de forma a possibilitar que funcione com a versão 2.0. (#2688) 
* Pressionando-se NVDA+seta acima dentro de  uma caixa de combinação no Internet Explorer e outros documentos MSHTML já não irá ler incorretamente todos os items. Em lugar disso, apenas o item ativo será lido. (#2337) 
* Os dicionários de fala agora salvarão  apropriadamente as entradas caso seja usado o sinal de cardinal (#) dentro do campo original ou de substituição. (#961) 
* O modo de navegação para documentos MSHTML (como o Internet Explorer) agora mostra corretamente conteúdos visíveis  contidos em conteúdos ocultos (especificamente, elementos com o estilo de visibilidade:visível dentro de um elemento que tenha o estilo de visibilidade:oculto). (#2097) 
* Os links da Central de Segurança do Windows XP já não anunciam porções de textos desnecessários depois de seus nomes. (#1331) 
* Os controles de texto UI Automation (como o campo de pesquisa no Menu Iniciar do Windows 7) agora são anunciados corretamente quando o mouse é movido sobre eles ao invés de permanecer em silêncio. 
* As mudanças nos leiautes de teclado já não são anunciadas durante uma leitura contínua, algo que era particularmente problemático para documentos multilingue, incluindo textos em Árabe. (#1676) 
* o conteúdo inteiro de alguns controles de edição de texto do UI Automation  (como a caixa de pesquisa no  Menu iniciar do Windows 7/8) já não é anunciado a cada vez que ele é alterado. 
* Ao mover-se entre grupos na tela de início do Windows 8, os grupos não etiquetados já não anunciam seu primeiro mozaico como se fosse o nome do grupo. (#2658) 
* Ao abrir a tela de início do Windows 8 , o foco é corretamente colocado no primeiro mozaico, em lugar de ir para a raiz da referida tela, visto que isso tornaria a navegação confusa. (#2720) 
* O NVDA já não falha ao ser iniciado quando o caminho do perfio do usuário contém certos caracteres multibyte. (#2729) 
* No Google Chrome, em modo de navegação, o texto das guias agora é esposto corretamente. 
* No modo de navegação, os botões de menu agora são anunciados corretamente. 
* No OpenOffice.org/LibreOffice Calc, a leitura das células das planilhas agora funciona corretamente. (#2765) 
* O NVDA volta a funcionar na lista de mensagens do Yahoo! Mail quando se o acessa usando o Internet Explorer. (#2780)

### Alterações Específicas para Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* O arquivo contendo o log anterior agora é copiado para nvda-old.log a quando da inicialização do NVDA. Com efeito, caso ele trave ou seja reiniciado, as informações do log daquela sessão continuarão acessíveis para inspeção. (#916)
* Fetching the role property in chooseNVDAObjectOverlayClasses no longer causes the role to be incorrect and thus not reported on focus for certain objects such as Windows command consoles and Scintilla controls. (#2569)
* Os menus Preferências, Ferramentas e Ajuda são agora acessíveis como atributos em gui.mainFrame.sysTrayIcon com as respectivas denominações de preferencesMenu, toolsMenu e helpMenu. Isso permite que plugins adicionem itens mais ´facilmente a esses menus.
* O script navigatorObject_doDefaultAction  em globalCommands foi renomeado para review_activate.
* Mensagens de contexto Gettext agora são suportadas. Isso permite que  múltiplas traduções sejam definidas para uma única mensagem em Inglês de acordo com o contexto. (#1524) 
 * Isso é feito usando a função pgettext(context, message).
 * Recurso suportado tanto pelo próprio NVDA como por seus complementos. 
 * xgettext and msgfmt from GNU gettext must be used to create any PO and MO files. The Python tools do not support message contexts. 
 * For xgettext, pass the --keyword=pgettext:1c,2 command line argument to enable inclusion of message contexts. 
 - Consulte https://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts para mais informações. 
* It is now possible to access built-in NVDA modules where they have been overridden by third party modules. See the nvdaBuiltin module for details. 
* Add-on translation support can now be used within the add-on installTasks module. (#2715) 

## 2012.2.1

Essa versão elimina vários potenciais problemas de segurança (ao atualizar o Python para a versão 2.7.3).

## 2012.2

Os destaques dessa versão incluem um instalador integrado com o recurso de criação de cópia portátil, atualização automática, facilitação do gerenciamento dos novos complementos para o NVDA, anúncio de gráficos no Microsoft Word, suporte para aplicativos de estilo Metro no Windows 8, e várias correções de bugs importantes.

### Novas Características

* O NVDA agora pode procurar, baixar e instalar atualizações automaticamente. (#73)
* Acrescentar funcionalidades ao NVDA tornou-se mais fácil com a adição de um gerenciador de complementos (localizado no submenu ferramentas do menu do NVDA) que lhe permite instalar e desinstalar os novos pacotes de complementos para o NVDA (arquivos .nvda-addon) que contém plugins e drivers. Note que o gerenciador de complementos não mostra os antigos plugins e drivers personalizados copiados manualmente para sua pasta de configurações. (#213) 
* Muito mais recursos comuns do NVDA agora funcionam em aplicativos do estilo Windows 8 Metro quando se usa uma versão oficial instalada, incluindo-se o anúncio de caracteres digitados, e modo de navegação para documentos da web (inclui suporte para a versão metro do Internet Explorer 10). Cópias Portáteis do NVDA não possuem a capacidade para acessar aplicativos de estilo metro. (#1801)
* Em documentos do modo de navegação (Internet Explorer, Firefox etc) você agora pode saltar para o início e para após o final de certos elementos que contém outros (incluindo listas e tabelas) com shift+vírgula e vírgula respectivamente. (#123)
* Novo idioma: grego.
* Novo idioma: grego.
* Gráficos e textos de descrição de imagens agora são anunciados em Documentos do Microsoft Word. (#2282, #1541)

### Alterações

* O anúncio das coordenadas de células no Microsoft Excel agora acontece depois do conteúdo em lugar de ser feito antes, e agora só é incluido se as opções Anunciar Tabelas e Anunciar Coordenadas de Células em Tabelas estiverem abilitadas no Diálogo de Formatação de Documentos. (#320)
* O NVDA agora é distribuído em um único pacote. Ao invés de separar versões portáteis e instaláveis, agora existe um único arquivo que quando executado iniciará uma cópia temporária do NVDA e lhe permitirá instalá-lo ou gerar uma distribuição portátil. (#1715)
* O NVDA agora é sempre instalado na pasta Arquivos de Programas em todos os sistemas. Ao atualizar uma instalação anterior irá também movê-lo se ele anteriormente não estava instalado neste local.

### Correção de Falhas

* Quando a alternância automática de idioma encontra-se ativada, conteúdos como textos de descrição de gráficos e etiquetas para alguns outros controles em Mozilla Gecko (isto é, Firefox) agora são anunciados no idioma correto caso esteja indicado apropriadamente.
* A leitura contínua no BibleSeeker (e outros controles TRxRichEdit) já não é interrompida no meio de uma passagem.
* Listas localizadas no Windows 8, tanto nas propriedades de arquivos do Windows explorer (guia permissões) como no Windows Update agora são lidas corretamente.
* Eliminados possíveis travamentos no Microsoft Word que poderiam acontecer quando ele levava mais que 2 segundos para extrair textos de um documento (linhas extremamente longas ou índices). (#2191)
* A detecção de separação de palavrs agora funciona corretamente onde os espaços são seguidos por determinados sinais de pontuação. (#1656)
* No modo de navegação, no Adobe Reader, agora é possível navegar para cabeçalhos sem nível usando navegação rápida e a  Lista de Elementos. (#2181)
* No Winamp, o braille agora é atualizado corretamente ao mover para um item diferente no editor de listas de reprodução. (#1912)
* A árvore encontrada na Lista de Elementos (disponível para documentos do modo de navegação) agora é calculada corretamente para exibir o texto de cada elemento. (#2276)
* Em aplicativos que usam Java Access Bridge, os campos de edição de texto agora são apresentados corretamente em braille. (#2284)
* Em aplicativos que usam java Access Bridge, os campos de edição de texto já não anunciam caracteres estranhos em determinadas circunstâncias. (#1892)
* Em aplicativos que usam Java Access Bridge, estando no fim de um campo de edição de texto, a linha atual agora é anunciada corretamente. (#1892)
* No modo de navegação em aplicativos que usam Mozilla Gecko 14 e posteriores (como Firefox 14), a navegação rápida agora funciona para blocos de citação  e objetos embutidos. (#2287) 
* No Internet Explorer 9, o NVDA já não lê conteúdo indesejado quando o foco é movido para dentro de certas marcas ou elementos enfocáveis (especificamente, um elemento div que é enfocável ou possui uma função ARIA de marca).
* O ícone do NVDA para os atalhos da área de trabalho e do menu iniciar agora é mostrado corretamente em edições de 64 bit  do Windows. (#354)

### Alterações Específicas para Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* Devido à substituição do anterior instalador do NVDA NSIS por um instalador integrado escrito em Python, já não se faz necessário aos tradutores manter os arquivos langstrings.txt para o instalador. Todas as strings de localização agora são controladas pelos arquivos gettext po.

## 2012.1

 Os destaques desta versão inclúem recursos para uma leitura mais fluente do braille; indicação da formatação de documentos em braille; acesso a muito mais informações de formatação e melhora na performance no Microsoft Word; e suporte para a loja do iTunes.

### Novas Características

* O NVDA agora pode anunciar o número de tabs e espaços inseridos na linha atual. Isso pode ser abilitado selecionando a opção Anunciar Identação das Linhas no Diálogo de Formatação de Documentos. (#373)
* Agora é possível detectar o pressionamento de teclas efetuado por emulação de entradas de teclado por vias alternativas tais como teclados espostos na tela e softwares para reconhecimento de voz.
* O NVDA agora pode detectar cores em consoles de comandos do Windows.
* Negrito, itálico e sublinhado agora são indicados em braille usando sinais apropriados para a tabela de tradução configurada. (#538)
* Muito mais informações agora são anunciadas em documentos do Microsoft Word, incluindo:
 * Informações nas linhas tais como o número das notas de rodapé e notas de fim, níveis de cabeçalhos, a existência de comentários, tabelas, links e a cor dos textos;
 * Anuncia ao entrar em seções dos documentos tais como o histórico de comentários, notas de rodapé e de fim e cabeçalhos.
* O braille agora indica textos selecionados usando pontos 7 e 8. (#889)
* O braille agora anuncia informação sobre controles presentes em documentos tais como links, botões e cabeçalhos. (#202)
* Suporte para as linhas braille USB ProfiLine e mobilLine da hedo. (#1863, #1897) 
* O NVDA agora evita palavras separadas nas linhas braille quando possível. (#1890)
* Agora é possível ter o braille exibido por parágrafos ao invés de linhas, o que pode permitir uma leitura mais fluente em textos muito extensos. Pode-se configurar essa funcionalidade através da opção Ler por Parágrafos no diálogo de Opções de Braille. (#1891)
* No Modo de Navegação, você agora pode ativar o objeto sob o cursor usando uma linha braille. Isso é feito pressionando a tecla do sensor onde o cursor está posicionado (o que significa que deve-se pressioná-lo duas vezes caso o cursor ainda não esteja neste local). (#1893)
* Suporte básico para áreas da web  em iTunes, tais como na loja. Outros aplicativos que usam WebKit 1 também podem ser suportados. (#734)
* Em edições digitais de livros da Adobe nas versões 1.8.1 e posteriores, as páginas agora são passadas automaticamente quando é efetuada a leitura contínua. (#1978)
* Nova tabela de tradução braile: português grau 2. (#2014)
* Você agora pode configurar o anúncio de frames nos documentos através do Diálogo de Formatação de Documentos. (#1900)
* O modo dormir agora é abilitado automaticamente ao usar o OpenBook. (#1209)
* No Poedit, os tradutores agora podem ler comentários adicionados e automaticamente extraídos. Mensagens não traduzidas ou excluídas são marcadas com um asterisco e um beep é ouvido ao navegar por elas. (#1811)
* Suporte para as linhas braille HumanWare Brailliant BI e B series. (#1990)
* Novo idioma: Noroeguês.

### Alterações

* Os comandos para descrever o atual caractere ou para soletrar a palavra ou linha atual agora os farão no idioma apropriado de acordo com o texto, se a alternância automática de idioma estiver ativada e a informação apropriada do idioma estiver disponível.
* Atualizado o sintetizador eSpeak para a versão 1.46.02.
* O NVDA agora filtra nomes extremamente extensos (de 30 caracteres ou mais) de gráficos e URLs de links uma vez que eles contêm muito provavelmente vestijos desnecessários à leitura. (#1989)
* Algumas informações que são exibidas em braille foram abreviadas. (#1955, #2043)
* Quando o cursor do sistema ou o cursor de exploração é movido, o braille agora é deslocado da mesma forma que quando se lhe desloca manualmente. Isso o torna mais apropriado quando o braille está configurado para ser lido por parágrafos e/ou evitar a quebra de palavras. (#1996)
* Atualização para a nova tabela de tradução braille do espanhol grau 1.
* Atualizado o transcritor braille liblouis para a versão 2.4.0.

### Correção de Falhas

* No Windows 8, o foco já não é incorretamente deslocado para fora do campo de pesquisa do Windows Explorer, o que não permitia que o NVDA interagisse com ele.
* Significativa melhora na performance ao ler e navegar por documentos do Microsoft Word enquanto o anúncio automático da formatação está ativado, tornando agora mais confortável a leitura da formatação, etc. A performance pode também ser melhorada, contudo, por alguns usuários.
* O Modo de Navegação agora é usado para conteúdos de Adobe Flash em tela cheia.
* Corrigida uma deficiência na qualidade de áudio que havia em alguns casos em que eram usadas vozes Microsoft Speech API versão 5 tendo a saída de áudio ajustada para outra que não fosse a padrão (Mapeador de Som da Microsoft). (#749)
* é novamente possível usar o NVDA sem fala a fim de valer-se apenas do braille ou do exibidor de fala. (#1963)
* Os comandos da navegação de objetos já não anunciam "sem filhos" e "sem pais", e em lugar disso, anunciam mensagens em concordância com a documentação. Nota: (Isto foi feito apenas no idioma original, visto que estamos habituados a tais expressões e optamos por mantê-las.)
* Quando o NVDA está configurado para usar outro idioma diferente do inglês, o nome da tecla tab agora é anunciado no idioma correto.
* No Mozilla Gecko, (isto é, Firefox), o NVDA já não alterna ocasionalmente para o modo de navegação quando se navega por menus em documentos. (#2025) 
* Na Calculadora, a tecla backspace agora anuncia o resultado atualizado ao invés de slenciar. (#2030) 
* Em modo de navegação, quando se tem a opção "Modo de foco automático quando o foco muda" ativada, quando uma  barra de ferramentas recebe foco, o modo de foco agora é ativado. (#1339) 
* No modo de navegação, o comando de mover o mouse para o objeto de navegação atual agora desloca-o para o centro do objeto sob o cursor de exploração, em lugar de ir para a parte esquerda do topo, tornando-o mais eficaz em alguns casos. (#2029)
* O comando para anunciar título volta a funcionar apropriadamente no Adobe Reader.
* Com a opção "Modo de foco automático quando o foco muda" ativada, o modo de foco agora é usado corretamente para células de tabelas que recebem foco; isto é, em ARIA grids. (#1763)
* No iTunes, a informação da posição em determinadas listas agora é anunciada corretamente.
* No Adobe Reader, alguns links já não são tratados como se contivessem campos de edição de texto somente leitura.
* As etiquetas de alguns campos de edição de texto já não são incluidas incorretamente ao anunciar o texto de um diálogo. (#1960)
* A descrição de grupos é novamente anunciada se o anúncio de descrições dos objetos estiver abilitado.
* Os tamanhos disponíveis agora são inclusos no diálogo de propriedades das unidades no windows explorer.
* O anúncio duplo de textos en páginas de propriedades foi suprimido en alguns casos. (#218)
* Melhorada a percepção do cursor em campos de edição de texto onde o texto é escrito na própria tela. Em particular, isso melhora a edição no editor de células do Microsoft Excel e no editor de mensagens Eudora. (#1658)
* No Firefox 11, o comando de mover para o buffer virtual que contém objetos embutidos (NVDA+control+espaço) agora funciona como lhe é designado para sair dos objetos embutidos tais como em conteúdo Flash.
* O NVDA agora reinicia automaticamente de forma apropriada (isto é, depois de ser alterado o idioma configurado) quando localizado em uma pasta  cujo nome contém caracteres não ASCII. (#2079)
* O braille respeita apropriadamente as configurações para o anúncio de objetos (teclas de atalho, informação da posição e descrições.
* Em aplicativos da Mozilla, a alternância entre os modos de foco e navegação já não é lenta quando se tem o braille abilitado. (#2095)
* O direcionamento do cursor para o espaço ao fim da linha/paragrafo através das teclas sensor com o cursor braille em alguns campos de edição de texto agora funciona corretamente em lugar de levar ao início do texto. (#2096)
* O NVDA volta a funcionar corretamente com o sintetizador Audiologic Tts3. (#2109)
* Os documentos do Microsoft Word agora são corretamente tratados como multi-linha. Isso possibilita ao braille comportar-se apropriadamente quando um documento está sob o foco.
* No Microsoft Internet Explorer, já não ocorrem erros quando determinados controles pouco comuns recebem foco. (#2121)
* As alterações da pronúncia de pontuação/sinais pelos usuários agora irão fazer efeito imediatamente, em lugar de necessitar que o NVDA seja reiniciado ou que a Alternância automática de idiomas seja desablitada.
* Quando se usa o eSpeak, a voz já não silencia em alguns casos no diálogo gravar como do visualizador de log do NVDA. (#2145)

### Alterações Específicas para  Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* Agora existe um console Python remoto para situações onde seja necessária uma depuração remota. Consulte o Guia do Desenvolvedor para mais detalhes.
* The base path of NVDA's code is now stripped from tracebacks in the log to improve readability. (#1880)
* TextInfo objects now have an activate() method to activate the position represented by the TextInfo.
 * Isto é usado pelo braille para ativar a posição usando a tecla sensor em linhas braille. Todavia, podem existir outras formas de entrada futuramente.
* TreeInterceptors and NVDAObjects which only expose one page of text at a time can support automatic page turns during say all by using the textInfos.DocumentWithPageTurns mix-in. (#1978)
 * Várias constantes de controle ou saída foram renomeadas ou movidas. (#228)
 * speech.REASON_* constants have been moved to controlTypes.
 * In controlTypes, speechRoleLabels and speechStateLabels have been renamed to just roleLabels and stateLabels, respectively.
* A saída braille agora é registrada no log no grau entrada/saída. Primeiro, o texto não traduzido  de todas as regiões é registrado, seguido pelas células braille  da janela que está sendo exibida. (#2102)

## 2011.3

Os destaques desta versão incluem a mudança automática do idioma do sintetizador de voz ao ler documentos que forneçam a informação apropriada do idioma; suporte para Java em 64 bit; anúncio da formatação de texto no modo de navegação para aplicativos da Mozilla; melhoras no controle de falhas e travamentos em aplicativos; resoluções iniciais para o Windows 8.

### Novas Características

* O NVDA agora pode alterar o idioma do sintetizador eSpeak ao ler certos documentos da web/pdf que forneçam a informação apropriada do idioma. A mudança automática do idioma//dialeto pode ser ativada ou desativada através do Diálogo de Opções de Voz. (#845)
* O Java Access Bridge 2.0.2 agora é suportado, o que passa a incluir suporte para Java 64 bit.
* No Mozilla Gecko (isto é, Firefox) os níveis dos cabeçalhos agora são anunciados quando se usa a navegação de objetos.
* A formatação de textos agora é informada quando se usa o modo de navegação no Mozilla Gecko (isto é, Firefox e Thunderbird). (#394)
* Textos com sublinhado e/ou taxado agora podem ser detectados e informados em controles de texto standard IAccessible2 tais como em aplicativos da Mozilla.
* No Adobe Reader, em modo de navegação, a quantidade de linhas e colunas das tabelas agora é anunciada.
* Adicionado suporte para o sintetizador da plataforma de fala da Microsoft. (#1735) 
* O número de páginas e linhas agora é anunciado pelo cursor do sistema no IBM Lotus Symphony. (#1632)  
* A porcentagem da mudança de tom ao anunciar uma letra maiúscula agora é configurável a partir do Diálogo de Opções de Voz. Todavia, esta substituirá a antiga caixa de seleção Aumentar Tom Para Maiúsculas. (portanto para desativar esse recurso, ajuste a porcentagem para 0). (#255)
* Textos e a cor de fundo agora são inclusos no anúncio de formatação de células no Microsoft Excel. (#1655)
* Em aplicativos que usam Java Access Bridge, o comando ativar objeto  de navegação atual agora funciona em controles onde é apropriado. (#1744)
* Novo Idioma: Tâmil
* Suporte Básico para o aplicativo Design Science MathPlayer.

### Alterações

* O NVDA agora irá reiniciar por si próprio caso ele trave.
* Algumas informações exibidas em braille foram abreviadas. (#1288)
* O script ler janela ativa (NVDA+b) foi aprimorado para excluir objetos inúteis e além disso, agora é bem mais fácil cilenciá-lo.
* A automatização da leitura contínua de um documento quando este é carregado no modo de navegação foi tornada opcional mediante uma configuração no Diálogo de Opções do Modo de Navegação. (#414)
* Ao tentar ler a barra de status (Desktop NVDA+end), caso o objeto real da barra de status não possa ser encontrado, o NVDA em seu lugar irá usar a última linha de texto escrita na tela para o aplicativo ativo. (#649)
* Ao efetuar leitura contínua em documentos no modo de navegação, o NVDA agora irá fazer pausa ao fim de cabeçalhos e outros elementos no bloco de seu nível, em lugar de ler o texto junto com  o próximo bloco de texto como uma sentença longa.
* No modo de navegação, ao pressionar enter ou espaço numa guia agora ela é ativada em lugar de altermnar para o modo de foco. (#1760)
* Atualizado o sintetizador eSpeak para a versão 1.45.47.

### Correção de Falhas

* O NVDA já não mostra marcas ou numerações para listas no Internet Explorer e outros controles MSHTML onde o autor tiver indicado que estes não devem ser mostrados (isto é, o estilo da lista é "none"). (#1671)
* Ao reiniciar o NVDA quando este trava, (isto é, pressionando control+alt+n) já não encerra a cópia anterior sem iniciar uma nova logo em seguida.
* Pressionar backspace ou setas em um console de comando do Windows já não causa resultados estranhos em alguns casos. (#1612)
* O item selecionado em caixas de combinação WPF (e possivelmente algumas outras caixas de combinação expostas usando UI Automation) que não permitem edição de texto agora é anunciado corretamente.
* No Adobe Reader em modo de navegação, agora é sempre possível mover para a próxima linha desde o cabeçalho da linha e vice versa usando os comandos mover para a próxima linha e mover a linha anterior. Além disso, o cabeçalho da linha já não é anunciado como linha 0. (#1731) 
* No Adobe Reader em modo de navegação, agora é possível mover para (e portanto passar) células vazias em uma tabela.
* A informação da posição já não é anunciada em braille desnecessariamente (isto é, 0 de 0 nível 0).
* O texto de controles já não é apresentado duas vezes em linhas braille em alguns casos, como ao deslocar a linha do início de documentos do Word Pad.
* Quando o braille está vinculado à exporação, ele agora é capaz de exibir o conteúdo da revisão plana. (#1711)
* No Internet Explorer, em modo de navegação, ao pressionar enter em um botão de upload de arquivo, agora o diálogo é corretamente apresentado em lugar de alternar para o modo de foco. (#1720)
* Alterações nos conteúdos dinâmicos tais como em consoles do Dos já não são anunciados se o Modo Dormir estiver ativado para aquele aplicativo. (#1662)
* No modo de navegação, foi melhorado o comportamento dos comandos alt+seta acima e alt+seta abaixo para recolher e expandir caixas de combinação.
* O NVDA agora recupera-se de muito mais situações tais como aplicativos que cessam de responder, o que anteriormente faziam-no travar por completo. (#1408)
* Em documentos no modo de navegação da Mozilla Gecko (Firefox etc.) o NVDA já não falhará ao expor textos em uma situação muito específica onde um elemento é desenhado como tabela. (#1373)
* O NVDA já não anuncia etiquetas dos controles quando o foco é movido para dentro deles. Eliminado o duplo anúncio de etiquetas para alguns campos de edição no Firefox (Gecko) e Internet Explorer (MSHTML). (#1650)
* O NVDA já não falha ao ler uma célula no Microsoft Excel depois de algo ser colado na mesma usando control+v. (#1781)
* No Adobe Reader, informações estranhas sobre o documento já não são anunciadas ao mover-se para um controle numa página different no modo de foco. (#1659)
* Em aplicativos que usam Mozilla Gecko (tal como o Firefox), em modo de navegação, botões de alternância agora são detectados e anunciados corretamente. (#1757)
* O NVDA agora pode ler corretamente a Barra de Enderesso do Windows Explorer na pré-visualização de desenvolvimento do Windows 8.
* O NVDA já não trava aplicativos tais como winver e wordpad na pré-visualização de desenvolvimento do Windows 8 devido a má tradução de hieróglifos.
* No modo de navegação em aplicativos que usam Mozilla Gecko 10 e posteriores (isto é, Firefox 10), o cursor é posicionado com mais freqüência corretamente ao carregar uma página na qual exista uma âncora. (#360)
* No modo de navegação em aplicativos que usam Mozilla Gecko (Firefox, por exemplo), etiquetas para mapas de imagens agora são espostas.
* Com a captura de mouse ativada, movendo-se o mouse por sobre certos campos de texto editáveis já não faz com que trave o aplicativo. (#672)
* O NVDA agora  funciona corretamente em vários diálogos "sobre" em aplicativos distribuídos com o Windows XP, incluindo o diálogo "sobre" no Notepad e o diálogo "sobre" o Windows. (#1853, #1855)
* Corrigida a revisão por palavra em controles de edição do Windows. (#1877)
* Ao mover-se ppara fora de campos de edição de texto usando as teclas seta a esquerda, seta acima ou pageUp estando em modo de foco, agora alterna corretamente para o modo de navegação se a opção Modo de foco automático quando o cursor da aplicação muda estiver ativada. (#1733)

### Alterações Específicas para Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* O NVDA agora pode instruir aos sintetizadores de voz para alternar o idioma em  seções particulares da fala.
 * Para suportar essa função, os drivers precisam ter controle de speech.LangChangeCommand em seqüências passadas para SynthDriver.speak().
 * Os objetos para SynthDriver devem também fornecer a informação do idioma para OS OBJETOS de VoiceInfo (ou substituir o atributo do idioma para retomar o idioma atual). Caso contrário, o idioma da interface do usuário do NVDA será usado.

### 2011.2

Os destaques desta versão incluem maiores implementações no tocante à  pontuação e sinais, como configuração dos níveis, personalização dos nomes e descrições de caracteres; Leitura contínua sem pausa ao fim das linhas; melhorado o suporte ARIA no Internet Explorer; suporte melhorado para documentos XFA/LiveCycle PDF no Adobe Reader; acesso aos textos escritos na tela em mais aplicativos; e acesso a informações de formatação e cor para os textos escritos na tela.

### Novas Características

* Agora é possível ouvir a descrição para um determinado caractere pressionando o comando anunciar caractere atual duas vezes em rápida sucessão. Para caracteres ingleses esse é o alfabeto fonético standard inglês. Para idiomas pitográficos tais como Chinês tradicional, um ou mais exemplos de uso desse símbolo são fornecidos. Também ao pressionar Rever a Palavra Atual ou rever a linha atual três vezes soletrará a palavra/linha usando descrições de caracteres. (#55)
* Mais textos podem ser lidos  em revisão plana para aplicativos tais como mozilla Thunderbird, os quais escrevem seus textos diretamente para a tela.
* Agora é possível escolher entre vários graus de anúncio de pontuação e sinais. (#332)
* Quando pontuações ou outros sinais são repetidos por mais de 4 vezes, o número de repetições agora é anunciado em lugar de falar o sinal repetido. (#43)
* Novas Tabelas de Tradução braille: braille de Computador Noroeguês de 8 pontos, etíope grau 1, esloveno grau 1, sérvio grau 1. (#1456)
* A fala já não sofre pausas não naturais ao fim de cada linha quando se usa o comando de leitura contínua. (#149)
* O NVDA agora anuncia se algo é classificado  (de acordo com a propriedade de classe Aria) nos navegadores web. (#1500)
* O Unicode braille Patterns agora é exibido corretamente nas linhas braille. (#1505)
* No Internet Explorer e outros controles MSHTML, quando o foco é movido para dentro de um grupo de controles (rodeado por um campo de grupos), o NVDA agora anuncia o nome do grupo (a legenda). (#535)
* No Internet Explorer e outros controles MSHTML, as  propriedades aria-labelledBy e aria-describedBy agora são reconhecidas.
* No Internet Explorer e outros controles MSHTML, foi implementado suporte para listas Aria, gridcell, barras deslizantes e controles de barras de progresso.
* Os usuários agora poderão alterar a pronúncia da pontuação e outros sinais, bem como o grau de sinais em que estes serão falados. (#271, #1516)
* No Microsoft Excel, o nome da planilha ativa agora é anunciada ao mover-se com control+pageUp ou control+pageDown. (#760)
* Ao navegar com a tecla Tab por tabelas no Microsoft Word, o NVDA agora anunciará a célula atual enquanto você se move. (#159)
* Agora é possível configurar se serão ou não anunciadas as coordenadas de células em tabelas através do Diálogo das Opções de Formatação de Documentos. (#719)
* O NVDA agora poderá detectar a formatação e a cor do texto escrito na tela.
* Nas listas de mensagens do Outlook Express/Windows Mail/Windows Live Mail, o NVDA agora anuncia quando uma mensagem é não lida e também se ela está expandida ou recolhida no caso de uma conversação por tópico. (#868)
* O eSpeak agora possui uma opção de aumento de velocidade que triplica sua velocidade de fala.
* Suporte para o controle de calendário encontrado no Diálogo de Informações de Data e hora acessado a partir  do relójio do Windows 7. (#1637)
* Foram adicionadas teclas adicionais vinculadas à linha braille MDV Lilli. (#241)
* Novos idiomas: Búlgaro, Albanês.

### Alterações

* Para mover o cursor do sistema para o cursor de exploração, agora é necessário pressionar o script mover o foco para o objeto de navegação (desktop NVDA+shift+numpadMenos, laptop NVDA+shift+backspace) duas vezes em rápida sucessão. Isso torna livres mais comandos de teclado. (#837)
* Agora para ouvir a representação decimal e hexadecimal do caractere que está sob o cursor de exploração, pressione o comando rever o caractere atual três vezes em lugar de duas, pois duas vezes agora fala a descrição do caractere.
* Atualizado o Sintetizador de Voz eSpeak para a versão 1.45.03. (#1465)
* Tabelas de layout já não são anunciadas em aplicações mozilla Gecko enquanto se move o foco no modo de foco ou para fora de um documento.
* No Internet Explorer e outros controles MSHTML, o modo de navegação agora funciona para documentos dentro de aplicações ARIA. (#1452)
* Atualizado o Transcritor braille Liblouis para a Versão 2.3.0.
* No modo de navegação, ao saltar para um controle usando a navegação rápida ou o foco, a descrição desse controle é agora anunciada, caso ele tenha alguma.
* As Barras de Progresso Agora São Anunciadas no Modo de Navegação.
* Nodes marcadas com uma função ARIA de apresentação no Internet Explorer e outros controles MSHTML agora são  filtradas fora da revisão simples e do foco original.
* A interface do NVDA bem como sua documentação agora referem-se aos buffers virtuais como modo de navegação, pois o termo  "buffer virtual" é inexpressivo para a maioria dos usuários. (#1509)
* Quando o usuário desejar copiar suas configurações para o perfio do sistema a fim de usá-las na tela de logon etc., caso em suas configurações existam plugins personalizados, ele agora será alertado de que isso pode trazer riscos à segurança. (#1426)
* O NVDA service já não inicia e encerra o NVDA em entradas do usuário em desktops.
* No Windows XP e Windows Vista, o NVDA já não usa UI Automation mesmo que ele esteja disponível via platform update. Embora ao usá-lo pudesse ser melhorada a acessibilidade a algumas aplicações modernas, no XP e Vista havia uma série de problemas quando de seu uso. (#1437)
* Em aplicativos que usam mozilla Gecko 2 e posteriores (tais como Firefox 4 e posteriores), agora um documento pode ser lido no modo de navegação antes que seja completamente carregado.
* O NVDA agora anuncia o estado de um recipiente quando o foco é movido para um controle dentro dele (isto é, se o foco é movido para dentro de um documento que ainda está carregando, ele anunciará o mesmo como ocupado).
* A interface do NVDA e sua documentação no idioma original já não usam os termos  "primeiro filho" e "pai" em relação à navegação de objetos, pois esses termos causam confusão para muitos usuários.
* Recolhido já não é anunciado para alguns itens de menu que possuem sub-menus.
* O script reportCurrentFormatting (NVDA+f) agora anuncia a formatação na posição do cursor de exploração em lugar de para o cursor do sistema/foco. Como por padrão o cursor de exploração acompanha o cursor do sistema, maior parte das pessoas não deve notar a diferença. Não obstante, isso agora abilita o usuário para localizar a formatação enquanto se move com o cursor de exploração, como na revisão plana.

### Correção de Falhas

* Quando sob caixas de combinação recolhidas contidas em documentos no modo de navegação o modo de foco é forçado com NVDA+espaço, o NVDA já não retorna automaticamente ao modo de navegação. (#1386)
* Em documentos Gecko (isto é, Firefox) e MSHTML (ou seja, Internet Explorer), o NVDA agora disponibiliza corretamente certos textos na mesma linha que anteriormente eram dispostos em linhas separadas. (#1378)
* Quando o braille está vinculado à exploração e a navegação de objetos é movida para um documento no modo de navegação, seja manualmente ou devido a mudança no foco, o braille mostrará apropriadamente o conteúdo do modo de navegação. (#1406, #1407)
* Quando o anúncio de pontuação está desativado, determinadas pontuações já não são faladas incorretamente ao usar alguns sintetizadores. (#332)
* Já não ocorrem problemas ao carregar a configuração para sintetizadores que não permitem a configuração de voz tais como o Audiologic Tts3. (#1347)
* No Skype, o menu Extras agora é lido corretamente. (#648)n
* Ao marcar a caixa de seleção Brilho controla volume das coordenadas no Diálogo das Opções de Mouse, já não causa um grande atraso dos beeps ao mover o mouse pela tela no Windows Vista/Windows 7 com Aero ativado. (#1183)
* NVDA+delete agora funciona conforme é documentado para anunciar as dimensões do objeto de navegação atual quando o NVDA está configurado para usar o layout de teclado para computadores portáteis. (#1498)
* O NVDA agora reconhece apropriadamente o atributo de aria-selected em documentos no Internet Explorer.
* Quando o NVDA alterna automaticamente para o modo de foco em documentos no modo de navegação, agora ele anuncia a informação sobre o contexto do foco. Por exemplo, se um item como uma caixa de lista recebe o foco, a caixa de lista é anunciada primeiro. (#1491)
* No Internet Explorer e outros controles MSHTML, controles de caixas de lista ARIA agora são tratados como listas, não mais como itens de lista.
* Quando um controle de texto editável somente leitura recebe o foco, o NVDA agora anuncia que o controle é somente leitura. (#1436)
* No modo de navegação, o NVDA agora comporta-se corretamente em relação aos campos de texto editáveis somente leitura.
* Em documentos no modo de navegação, o NVDA já não sai inapropriadamente do modo de foco quando aria-activedescendant é exibido; isto é, quando a lista de  opções aparece em alguns controles que suportam auto-completar.
* No Adobe Reader, o nome dos controles agora é anunciado quando se move o foco ou usando a navegação rápida no modo de navegação.
* Em documentos XFA PDF  no Adobe Reader, botões, links e gráficos agora são corretamente  dispostos.
* Em documentos XFA PDF  no Adobe Reader, todos os elementos agora são espostos em linhas separadas. Essa mudança foi processada porque grandes seções (algumas vezes mesmo o documento completo ) eram espostas sem quebras devido à falta de  estrutura  geral nesses documentos.
* Resolvido o problema de quando se movia o foco para ou saindo de campos de texto editável em documentos XFA PDF no Adobe Reader.
* Em documentos XFA PDF no Adobe Reader, alterações dos valores nas caixas de combinação que recebem o foco agora são anunciadas.
* Caixas de combinação Owner-drawn, tais como as zonas para escolher cores no Outlook Express agora são acessíveis com o NVDA. (#1340)
* Em idiomas que usam espaço como separador para grupos de dígitos  tais como francês e alemão, números em pedaços separados de texto já não são anunciados como um número simples. isso era particularmente problemático para células de tabelas que continham números. (#555)
* No Internet Explorer e outros controles MSHTML, nodes com uma função ARIA de descrição agora são classificados como texto estático, não mais como campos de edição.
* Resolvidos vários problemas de quando Tab era pressionado enquanto o foco estava num documento no modo de navegação, (isto é, tab mover inapropriadamente para a barra de enderessos no Internet Explorer). (#720, #1367)
* Ao entrar em listas durante a leitura de textos, o NVDA agora diz, por exemplo, "lista com 5 itens" em lugar de "listacom 5 itens". (#1515)
* No modo ajuda de entrada, os gestos são registrados no Log mesmo se seus scripts ignorem a ajuda de entrada tais como os comandos mover linha braille para a frente e para trás.
* No modo ajuda de entrada, quando uma tecla modificadora é presa, o NVDA já não anuncia a modificadora como se ela estivesse modificando ela própria; isto é, NVDA+NVDA.
* Em documentos do Adobe Reader, c ou shift+c agora irão funcionar para  navegar para caixas de combinação.
* O estado da seleção de linhas de tabelas selecionáveis agora é anunciado da mesma forma que o é para listas e itens de vista em árvore.
* Controles no Firefox e outras aplicações Gecko podem agora ser ativados no modo de navegação mesmo se seu conteúdo flutua fora da tela. (#801)
* Você já não pode abrir um diálogo de configurações do NVDA enquanto  um diálogo de mensagem está sendo exibido, pois o diálogo de configurações foi bloqueado para esse caso. (#1451)
* NO Microsoft Excel, já não ocorre um atraso quando teclas são presas ou pressionadas rapidamente para mover-se entre ou selecionar células.
* Resolvidas falhas repentinas do NVDA_service que faziam parar a execução do NVDA nas telas de segurança do windows.
* Resolvidos problemas que algumas vezes ocorriam com as linhas braille onde uma mudança fazia desaparecer o texto que estava  sendo mostrado. (#1377)
* A janela de download do Internet Explorer 9 agora pode ser navegada e lida com o NVDA. (#1280)
* Já não é possível ativar acidentalmente várias cópias do NVDA ao mesmo tempo. (#507)
* Em sistemas lentos, o NVDA já não faz com que sua janela seja exibida inapropriadamente a todo instante enquanto é executado. (#726)
* O NVDA já não trava no Windows xP quando é ativada uma aplicação WPF. (#1437)
* A leitura contínua e também a leitura contínua com o cursor de exploração agora podem funcionar em Controles de Texto UI automation que suportem todas as funcionalidades necessárias. Por exemplo, você agora pode usar a leitura contínua com o cursor de exploração em documentos do visualizador XPS.
* O NVDA já não classifica inapropriamente alguns itens de lista  no Diálogo aplicar regras de mensagens agora do Outlook Express / Windows Live Mail como sendo caixas de seleção. (#576)
* As caixas de combinação já não são anunciadas como tendo um sub-menu.
* O NVDA agora pode ler o conteúdo nos campos Para, CC e BCC no Microsoft Outlook. (#421)
* Resolvido o problema no Diálogo de Opções de Voz do NVDA no qual os valores nas barras deslizantes não eram anunciados quando alterados. (#1411)
* O NVDA já não deixa de anunciar a nova célula ao mover-se em uma   apresentação no Excel depois de recortar e colar. (#1567)
* O NVDA já não decai seu desempenho ao deduzir o nome de cores a mais do que anuncia.
* No Internet Explorer e outros controles MSHTML, resolvida a incapacidade para ler partes de páginas incomuns que contém iframes marcadas com uma ARIA função de apresentação. (#1569)
* No Internet Explorer e outros controles MSHTML, resolvido um problema incomum onde  o foco saltava infinitamente entre o documento  e um campo de edição multilinha no modo de foco. (#1566)
* NO Microsoft Word 2010 o NVDA agora lê automaticamente os diálogos de confirmação. (#1538)
* Em campos de edição multilinha  no Internet Explorer e outros controles MSHTML, a seleção de linhas depois da primeira agora é anunciada corretamente. (#1590)
* Melhoras na função de mover-se por palavras em vários casos, incluindo-se modo de navegação e controles Editáveis do Windows. (#1580)
* O instalador do NVDA já não exibe texto danificado em versões para chinês de Hong Kong  do Windows Vista e Windows 7. (#1596)
* O NVDA já não falha ao carregar o sintetizador Microsoft Speech API versão 5 quando a configuração contém opções para o sintetizador mas faltam as opções de voz. (#1599)
* Em campos de  edição de texto no Internet Explorer e outros controles MSHTML, o NVDA já não atrasa ou trava quando o braille  está ativado.
* No modo de navegação do Firefox, o NVDA já não se recusa a incluir conteúdo que se encontra dentro de uma node enfocável com uma função ARIA de apresentação.
* NO Microsoft Word com o braille ativado, as linhas das páginas depois da primeira página agora são anunciadas corretamente. (#1603)
* No Microsoft Word 2003, as linhas de texto da direita para a esquerda voltam a poder ser lidas com o braille ativado. (#627)
* NO Microsoft Word, a leitura contínua agora funciona corretamente quando o documento não termina com um ponto final.
* Ao abrir uma mensagem de texto plana no Windows Live Mail 2011, o NVDA colocará  corretamente o foco sobre o documento permitindo que este seja lido.
* O NVDA já não trava ou se recusa a falar nos diálogos Mover para / Copiar para no  Windows Live Mail. (#574)
* No Outlook 2010, o NVDA agora orienta corretamente o foco na lista de mensagens. (#1285)
* Alguns problemas com a linha braille MDV Lilli referentes à conecção USB foram resolvidos. (#241)
* No Internet Explorer e outros controles MSHTML, espaços já não são ignorados em certos casos no modo de navegação, ex.: depois de um link.
* No Internet Explorer e outros controles MSHTML, elementos de HTML com estilo de exibição de nenhum, já não forçam uma quebra de linha no modo de navegação. (#1685)
* Quando o NVDA não pode ser iniciado, ao tocar o som de parada crítica do Windows, já não é repetida por várias vezes a mensagem de erro crítico no arquivo do log.

### Alterações específicas para Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* A documentação para desenvolvedores agora pode ser gerada usando SCons. Consulte o arquivo readme.txt na  raíiz da distribuição do código para detalhes, incluindo dependências associadas.
* Locales agora podem fornecer descrições para caracteres. Consulte a Seção sobre Descrições de Caracteres no Guia do Desenvolvedor para obter detalhes. (#55)
* Locales agora podem fornecer informações sobre a pronúncia da pontuação e outros sinais específicos. Consulte a seção sobre Pronúncia de Pontuação no Guia do Desenvolvedor para obter detalhes. (#332)
* Você agora pode integrar o NVDAHelper com várias opções de depuração usando a variável nvdaHelperDebugFlags SCons. Consulte o arquivo readme.txt na raíz da distribuição do código para obter detalhes. (#1390)
* Os drivers dos sintetizadores agora transmitem uma sequência de texto e comandos de fala para falar, em lugar de apenas texto e um índice.  - Isso é possível para índices embutidos, mudanças de parâmetros, etc.
 * Os drivers devem implementar SynthDriver.speak() em lugar de SynthDriver.speakText() e SynthDriver.speakCharacter().
 * Os antigos métodos serão usados se SynthDriver.speak() não for implementado, mas eles são reprovados e serão removidos em uma versão futura.
* gui.execute() foi removido. wx.CalhAfter() deve ser usado em seu lugar.
* gui.scriptUI foi removido.
 * Para mensagens de diálogo, use wx.CalhAfter(gui.messageBox, ...).
 * Para todos os outros diálogos, real wx dialogs deve ser usado em seu lugar.
 * A new gui.runScriptModalDialog() function simplifies using modal dialogs from scripts.
* Os drivers de sintetizador agora podem suportar opções boolean. Consulte SynthDriverHandler.BooleanSynthSetting.
* SCons agora aceita a variável certTimestampServer especificando a URL de um servidor timestamping  para usar em assinaturas timestamp authenticode. (#1644)

## 2011.1.1

 Esta versão resolve problemas de segurança entre outros importantes encontrados no NVDA 2011.1.

### Correção de Falhas

* O iten doar, presente no menu do NVDA agora é desabilitado quando de sua execução na tela de logon, logon, UAC e outras telas de segurança do windows, uma vez que isso representa um risco à segurança. (#1419)
* Não é mais possível copiar ou colar dentro da interface do NVDA quando se está nas telas de segurança do windows, pois isso constitui um risco à segurança. (#1421)
* No Firefox 4, o comando mover para o buffer virtual que contém um objeto embutido (NVDA+control+espaço) agora funciona como deveria  para sair de objetos embutidos tais como de conteúdo flash. (#1429)
* Quando a opção falar teclas de comando está ativada, teclas pressionadas em conjunto com shift já não são faladas incorretamente como teclas de comando. (#1422)
* Quando a opção falar teclas de comando está ativada, pressionando-se espaço junto com outras teclas modificadoras que não o shift (tais como control e alt) agora é anunciado como uma  tecla de comando. (#1424)
* O Log agora é completamente desativado quando se executa o NVDA no logon, lock, UAC e outras telas seguras do Windows, visto que isso traz riscos à segurança. (#1435)
* No modo de ajuda de entrada, os Gestos agora são registrados  mesmo que eles não estejam vinculados a um script (conforme o guia do Usuário). (#1425)

## 2011.1

Os destaques desta versão incluem o anúncio de cores para alguns controles; anúncio automático da saída de texto novo em mIRC, PuTTY, Tera Term e SecureCRT; suporte para plugins globais; anúncio de marcas  e numeração no Microsoft Word; combinações de teclas adicionais para linhas braille, incluindo teclas para mover-se para a linha seguinte e anterior; e suporte para várias linhas braille Baum, HumanWare y APH.

### Novas Características

* Agora as cores podem ser anunciadas para alguns controles. O anúncio automático póde ser configurado no Diálogo de Opções de Formatação de Documentos. Também podem ser anunciadas por meio de demanda utilizando o comando de anúncio de formatação de texto (NVDA+f).
* Nos buffers virtuais, agora é possível selecionar por página (utilizando shift+PageDown e shift+PageUp) e por parágrafos  (utilizando shift+control+seta Abaixo e shift+control+seta acima). (#639)
* O NVDA agora anuncia a saída de novos textos em mIRC, PuTTY, Tera Term e SecureCRT. (#936)
* Os usuários agora podem adicionar novas combinações de teclas ou substituir as existentes para qualquer script no NVDA proporcionando um mapa simples de gestos de entrada do usuário. (#194)
* suporte para plugins globais. Os plugins globais podem adicionar novas funcionalidades ao NVDA que funcionam em todas as aplicações. (#281)
* Agora é ouvido um pequeno beep quando se digita caracteres com a tecla shift enquanto o Caps Loc está ativado. Isto pode ser desativado desmarcando a nova opção relacionada no diálogo de Opções de Teclado. (#663)
* Agora são anunciadas as quebras de página quando nos movemos por linhas no Microsoft Word. (#758)
* As marcas e a numeração são agora anunciadas no Microsoft Word quando nos movemos por linhas. (#208)  
* Agora está disponível um comando para ativar ou desativar o modo Dormir para a aplicação atual (NVDA+shift+s). O Modo Dormir (anteriormente conhecido como modo de voz própria) desabilita toda a funcionalidade de leitura da tela no NVDA para uma aplicação em particular. Muito útil para aplicações que possuem voz própria e/ou recurso de leitura de tela. Pressione este comando novamente para desativar o Modo Dormir.
* Adicionadas algumas combinações de teclas adicionais para linhas braille. veja a seção Linhas braille suportadas no Guía do usuário para detalhes. (#209)
* Para a conveniência de desenvolvedores de terceiras partes, os app modules assim como os plugins globais agora pódem ser recarregados sen reiniciar o NVDA. Utilize Ferramentas -> recarregar plugins no menu do NVDA ou NVDA+control+f3. (#544)
* O NVDA agora lembra a posição onde estava quando volta a uma página anteriormente visitada. Isto aplica-se até que o navegador ou o NVDA sejam fechados. (#132)
* As linhas braille Handy Tech agora podem ser utilizadas sen instalar o driver universal da Handy Tech. (#854)
* suporte para várias linhas braille Baum, HumanWare e APH. (#937)

### Alterações

* A informação da posição já não é anunciada por padrão em alguns casos onde era normalmente incorreta; exemplos: a maioría dos menus, a barra de aplicações em execução, a área de notificações, etc. Não obstante, isto pode ativar-se novamente com uma opção adicionada no diálogo de Opções de apresentação de objetos.
* A ajuda de Teclado foi renomeada para ajuda de entrada para atualizar que se trabalha com entradas desde outras fontes além do teclado.
* A localização de um comando no código já não é anunciada na ajuda de entrada posto que é irrelevante e crítica para o usuário.
* quando o NVDA detecta que travou, continúa interceptando  as teclas modificadoras do NVDA, ainda que deixe passar todas as demáis teclas do sistema. Isto previne ao usuário de alternar involuntarianmente o Caps Lock, etc. Caso pressione uma tecla modificadora do NVDA sen saber que o NVDA está travado. (#939)
* Quando as teclas são mantidas pressionadas depois de utilizar o comando de deixar passar, todas as teclas (incluindo repetições de teclas) agora passa-se até que a última tecla  seja solta.
* Se uma tecla modificadora do NVDA é pressionada dúas vezes em sucessão rápida para passá-la e a segunda pressionada está presa, todas as teclas repetidas agora serão passadas também.
* As teclas aumentar, baixar volume e silenciar agora são anunciadas na ajuda de Entrada. Isto pode ser de utilidade caso o usuário não saiba qual a função das mesmas.
* A tecla rápida para o item cursor de exploração no menu Preferências do NVDA foi alterada de r para c a fim de eliminar o conflito com o item de Opções de braille.

### Correção de Falhas

* quando é adicionada uma nova entrada do dicionário, o da fala, o título do diálogo agora é "adicionar Entrada de dicionário" em lugar de "Editar entrada de dicionário". (#924)
* Nos diálogos do dicionário de fala, o conteúdo das colunas da Expressão Regular é sensível às maiúsculas da lista de entradas de dicionário  apresenta-se agora no idioma configurado no NVDA em lugar de sempre em Inglês.
* No AIM, a informação da posição agora é anunciada em árvores.
* A informação de posição já não é anunciada em alguns casos onde normalmente estava incorreta; ex.: a maioría dos menus, a barra de aplicações em execução, a área de notificação, etc.
* Nas barras deslizantes do Diálogo de Opções de Voz, seta acima/PageDown/home agora aumentam a opção e seta abaixo/PageDown/end diminuem.  Anteriormente, ocurría o oposto, o que não é lógico e é inconsistente com as opções do Anel de Opções de Voz. (#221)
* Se uma tecla modificadora do NVDA é pressionada dúas vezes rapidamente mas há uma tecla pressionada intervindo, a tecla modificadora do NVDA já não passa no segundo pressionamento.
* As teclas de pontuação agora são anunciadas na ajuda de entrada quando o anúncio da pontuação está desativado. (#977)
* No diálogo Opções de Teclado, os nomes dos layouts de teclado agora apresentam-se no idioma configurado para o NVDA em lugar de sempre em Inglês. (#558)
* corrigido um problema onde alguns itens eram espostos como vazios em documentos do Adobe Reader; ex.: os links no índice do Guía do usuário do Apple iPhone IOS 4.1.
* O botão "Utilizar opções atuais salvas no logon e outras telas seguras" no diálogo de Opções gerais do NVDA agora funciona quando utilizado inmediatamente depois que o NVDA é instalado novamente mas antes que uma tela segura apareça.  Anteriormente, o NVDA anunciava que a cópia havia sido bem sucedida, porém não tinha efeito. (#1194)
* Já não é possível ter dois diálogos de opções do NVDA abertos simultaneamente. Isso resolve problemas onde um diálogo aberto depend de outro diálogo também aberto; isto é, alterar o sintetizador enquanto o Diálogo de Opções de Voz está aberto. (#603)
* em sistemas com UAC ativado, o botão "Utilizar opções atualmente salvas no logon e outras telas seguras" no diálogo de Opções gerais do NVDA já não falha depois do UAC se o nome da conta do usuário contén um espaço. (#918)
* No Internet Explorer e outros controles MSHTML, o NVDA utiliza agora a URL como um último lugar para determinar o nome de um link, em lugar de apresentar links vazios. (#633)
* O NVDA já não ignora o foco nos menus do AOL Instant Messenger 7. (#655)
* Anúncio da etiqueta correta para erros no diálogo do corretor ortográfico do Microsoft Word (ex.: não existe em dicionário, erro gramatical, pontuação). Anteriormente todos eram anunciados como erro gramatical. (#883)
* Digitar no Microsoft Word enquanto se utiliza uma linha braille já não deve fazer com que seja digitado texto ilegível e um estranho bug quando se pressiona um sensor de linha braille em documentos do Word foi corrigido. (#1212) não obsstante uma limitação é que o texto em árabe pode não ser lido já no Word 2003 e posteriores, enquanto se utiliza uma linha braille. (#627)
* quando se pressiona a tecla delete num campo de edição, o texto/cursor numa linha braille agora deve atualizarse sempre apropriadamente para atualizar a alteração. (#947)
 * As Alterações  em documentos Gecko2 (Ex.: Firefox 4) enquanto se abren múltiplas abas agora é atualizada  adecuadamente pelo NVDA. Anteriormente só as Alterações na primeira aba se atualizavam. (mozilla bug 610985)
 * O NVDA agora pode anunciar apropriadamente as sugestões para erros gramaticais e de pontuação no diálogo do corretor ortográfico do Microsoft Word. (#704)
* no Internet Explorer e outros controles MSHTML, o NVDA já não apresenta âncoras de destino como links vazios em seu buffer virtual. (#633)
* A navegação de objetos sobre e dentro de brupos padrões do Windows já não falha ou é assimétrica.
* no Firefox e outros controles baseados em Gecko, o NVDA já não fica preso a uma subframe se esta terminou seu carregamento antes de outro documento.
* O NVDA agora anuncia apropriadamente o próximo caractere ao ser deletado um caractere com Delete do teclado numérico. (#286)
* Na tela de logon do Windows XP, O nome do usuário volta a ser anunciado uma vez quando o usuário selecionado é alterado.
* corrigidos problemas quando ao ler texto em consoles de comandos do Windows o anúncio de números de linha está ativado.
 * O diálogo de lista de elementos para buffers virtuais agora é utilizável por usuários videntes.  Todos os controles são visíveis em tela. (#1321)
* A lista de entradas no diálogo dicionários de fala, agora é mais legível por usuários videntes.  A lista agora é bastante grande para mostrar todas as suas colunas na tela. (#90)
* em linhas braille ALVA BC640/BC680 o NVDA já não ignora as teclas da linha que aínda estão sendo pressionadas depois que outra tecla é solta.

### Alterações específicas para Desenvolvedores

Alguns itens ou termos desta seção não serão traduzidos, uma vez que são demasiado técnicos e relevantes apenas para desenvolvedores. Todavia, os itens que possam ser relevantes para usuários comuns, serão traduzidos.

* SCons is now used to prepare the source tree and create binary builds, portable archives, installers, etc. See readme.txt at the root of the source distribution for details.
* The key names used by NVDA (including key maps) have been made more friendly/logical; e.g. upArrow instead of extendedUp and numpadPageUp instead of prior. See the vkCodes module for a list.
* All input from the user is now represented by an inputCore.InputGesture instance. (#601)
 * Each source of input subclasses the base InputGesture class.
 * Key presses on the system keyboard are encompassed by the keyboardHandler.KeyboardInputGesture class.
 * Presses of buttons, wheels and other controls on a braille display are encompassed by subclasses of the braille.BrailheDisplayGesture class. These subclasses are provided by each braille display driver.
* Input gestures are bound to ScriptableObjects using the ScriptavelObject.bindGesture() method on an instance or an __gestures dict on the class which maps gesture identifiers to script names. See baseObject.ScriptableObject for details.
* App modules no longer have key map files. All input gesture bindings must be done in the app module itself.
* All scripts now take an InputGesture instance instead of a key press.
 * KeyboardInputGestures can be sent on to the OS using the send() method of the gesture.
* To send an arbitrary key press, you must now create a KeyboardInputGesture using KeyboardInputGesture.fromName() and then use its send() method.
* Locales may now provide an input gesture map file to add new bindings or override existing bindings for scripts anywhere in NVDA. (#810)
 * Os mapas de gestos locais devem ser colocados em locale\LANG\gestures.ini, onde LANG representa o código do idioma.
 * See inputCore.GlobalGestureMap for details of the file format.
* The new LiveText and Terminal NVDAObject behaviors facilitate automatic reporting of new text. See those classes in NVDAObjects.behaviors for details. (#936)
 * The NVDAObjects.window.DisplayModelliveText overlay class can be used for objects which must retrieve text written to the display.
 * See the mirc and putty app modules for usage examples.
* There is no longer an _default app module. App modules should instead subclass appModuleHandler.AppModule (the base AppModule class).
* Support for global plugins which can globally bind scripts, handle NVDAObject events and choose NVDAObject overlay classes. (#281) See globalPluginHandler.GlobalPlugin for details.
* On SynthDriver objects, the available* attributes for string settings (e.g. availableVoices and availableVariants)  are now OrderedDicts keyed by ID instead of lists.
* synthDriverHandler.VoiceInfo now takes an optional language argument which specifies the language of the voice.
* SynthDriver objects now provide a language attribute which specifies the language of the current voice.
 * The base implementation uses the language specified on the VoiceInfo objects in availableVoices. This is suitable for most synthesisers which support one language per voice.
* Os drivers para linhas braille foram melhorados a fim de permitir que botões, rodas e outros controles sejam vinculados a scripts do NVDA:
 * Os mesmos podem fornecer um mapa de gestos de entradas globais para vincular-se a scripts em qualquer lugar do NVDA.
 * Estes podem também proporcionar seus próprios scripts para executar funções específicas da linha.
 * See braille.BrailheDisplayDriver for details and existing braille display drivers for examples.
* The 'selfVoicing' property on AppModule classes has now been renamed to 'sleepMode'.
* the appModule events: event_appLoseFocus and event_appGainFocus have now been renamed to event_appModule_loseFocus and event_appModule_gainFocus respectivly, in order to keep the naming sintax the same between appModules and treeInterceptors etc.
* All braille display drivers should now use braille.BrailheDisplayDriver instead of braille.BrailheDisplayDriverWithCursor.
 * The cursor is now managed outside of the driver.
 * Existing drivers need only change their class statement accordingly and rename their _display method to display.

## 2010.2

As características mais notáveis desta versão incluen uma grande simplificação da navegação de objetos; buffers virtuais para conteúdo de Adobe Flash; acesso a muitos controles anteriormente inacessíveis capturando texto escrito na tela; revisão plana de texto na tela; suporte para documentos do IBM Lotus Symphony; anúncio de cabeçalhos de linhas e colunas das tabelas no mozilla Firefox; uma melhora significativa da documentação do usuário.

### Novas Características

* A navegação de objetos com o cursor de exploração foi muito simplificada. O cursor de exploração agora exclui objetos que não sejam úteis para o usuário; isto é, objetos utilizados apenas para propósitos de desenho e objetos não disponíveis.
* em aplicações que utilizam Java Access Bridge (incluindo OpenOffice.org), a formatação agora pode ser informada nos controles de texto. (#358, #463)
* quando se move o mouse sobre células no Microsoft Excel, o NVDA as anuncia apropriadamente.
* em aplicações que utilizam Java Access Bridge, o texto de um diálogo agora é anunciado quando aparece. (#554)
* Agora pode-se utilizar um buffer virtual para navegar pelo conteúdo do adobe Flash. Navegar por objetos e interagir com os controles diretamente (ativando o modo de foco) já é suportado. (#453)
* Os controles de texto editável no IDE Eclipse, incluindo o editor de código, agora são acessíveis. é necessário utilizar Eclipse 3.6 ou posteriores. (#256, #641)
* O NVDA agora pode captar a maior parte do texto escrito na tela. (#40, #643)

> - isto permite a leitura de controles que não exibem as informações de formas mais diretas/fiáveis.

* Os controles que se tornam acessíveis por esta característica incluem: alguns itens de menu que mostram ícones (ex.: O menu Abrir com em arquivos no windows XP) (#151), campos de texto editáveis em aplicações Windows Live (#200), a lista de erros no Outlook Express (#582), o controle de texto editável no TextPad (#605), listas em Eudora, muitos controles em Australiano E-tax e a barra de fórmulas no Microsoft Excel.
* suporte para o editor de código no Microsoft Visual Studio 2005 e 2008. É exigido pelo menos Visual Studio Standard; isto não funciona nas edições Express. (#457)
* suporte para documentos no IBM Lotus Symphony.
* suporte primário e experimental para o Google Chrome. Por favor tenha em conta que o suporte para leitores de tela do Chrome está longe de compretar-se e exigirá trabalho adicional também no NVDA. Será necessário uma compilação de desenvolvimento recente do Chrome para confirmar isto.
* O estado das teclas alternáveis (Caps Lock, Numlock e Scroll Lock) agora é exibido em braille quando pressionadas. (#620)
* Os balões de ajuda agora são exibidos em braille quando aparecem. (#652)
* adicionado um driver para a linha braille MDV Lilhi. (#241)
* quando se seleciona uma linha ou uma coluna completa em MS Excel com as teclas de atalho shift+espaço e control+espaço, a nova seleção agora é anunciada. (#759)
* Os cabeçalhos de linha e coluna agora podem ser anunciados. isto é configurável desde o diálogo de Opções de formatação de documentos.
 * atualmente, isto é suportado em documentos em aplicações da mozilla como Firefox e Thunderbird. (#361)
* Adicionados comandos para a revisão plana: (#58)
 * NVDA+7 do teclado numérico ativa a revisão plana, colocando o cursor de exploração na posição do objeto atual, lhe permitindo revisar a tela (ou documento se estiver em algum) com os comandos de revisão de texto.
 * NVDA+1 do teclado numérico move o cursor de exploração para o objeto representado pelo texto na posição do cursor de exploração, lhe permitindo navegar por objetos desde esse ponto.
* As opções do usuário atuais do NVDA podem ser copiadas para utilizar nas telas de logon/UAC, pressionando um botão no diálogo Opções gerais. (#730)
* Suporte para o Mozilla Firefox 4.
* Suporte para o Microsoft Internet Explorer 9.

### Alterações

* Ler tudo com a navegação de objetos  (NVDA+mais do teclado numérico), seguinte objeto em fluxo do navegador de objetos (NVDA+shift+6 do teclado numérico) e anterior objeto em fluxo no navegador de objetos (NVDA+shift+4 do teclado numérico) foram removidos de momento, devido a falhas e para liberar as teclas para outras possíveis características.
* No diálogo de sintetizadores do NVDA, agora só se mostra o sintetizador listado. Anteriormente, prefixava-se com nome do driver, que só é relevante internamente.
* quando se está em aplicações embutidas ou buffers virtuais dentro de outro buffer virtual (ex.: Flash), agora pode pressionar nvda+control+espaço para saír da aplicação embutida ou buffer virtual, para o documento principal. Anteriormente, nvda+espaço   era utilizado para isto. Agora nvda+espaço serve específicamente para alternar os modos de navegação/foco no buffer virtual.
* Se o exibidor de fala (ativável no menu Ferramentas) recebeu o foco (ex.: ao clicar) o novo texto não aparecerá no controle até que o foco se mova. isto permite selecionar o texto com maior facilidade (ex.: para copiar).
* O visualizador de Log e o console Python maximizam-se quando são ativados.
* quando se enfoca uma folha de cálculo em MS Excel, e há mais de uma célula selecionada, anuncia-se o alcance da seleção, em lugar de só a célula ativa. (#763)
* Salvar a configuração e a alteração de opções sensíveis em particular, agora desativa-se quando se o executa em modo seguro (nas telas de logon/UAC).
* atualizado o sintetizador de voz eSpeak para a versão 1.44.01.
* Caso o NVDA já esteja sendo executado, ativando o atalho de teclado do NVDA na área de trabalho ( control+alt+n) reiniciará o NVDA.
* Removida a caixa de seleção anunciar texto sob o mouse do Diálogo Opções de Mouse e substituida por uma caixa de seleção abilitar rastreamento do mouse, que melhora o sincronismo da alteração do script de seguimento do mouse (NVDA+m). 
* atualizado o layout de teclado laptop de forma que inclui todos os comandos disponíveis no layout desktop e funciona corretamente em teclados não ingleses. (#798, #800)
* melhoras significativas e atualizações à documentação do usuário, incluindo documentação dos comandos de teclado laptop e sincronização da Referência Rápida de de Teclas de Atalho com a Guía do usuário. (#455)
* atualizado o transcritor braille liblouis para a  versão 2.1.0. Notavelmente, isto corrige alguns problemas relacionados com braille Chinês

### Correção de Falhas

* No µTorrent, o elemento enfocado na lista de torrents já não informa repetidamente ou esconde o foco quando se abre um menu.
* em aplicações da mozilla, agora o foco é corretamente detectado quando é movido para uma tabela vazia ou árvore.
* em aplicações da mozilla, "não marcado" agora informa-se corretamente para controles marcáveis como células de tabela marcáveis. (#571)
* em aplicações da mozilla, o texto de diálogos aria corretamente implementados já não se ignora e agora é informado quando o diálogo aparece.
* no Internet Explorer e outros controles MSHTML, o atributo nível de ARIA agora se cumpre corretamente.
* no Internet Explorer e outros controles MSHTML, a função ARIA agora é escolhido sobre outro tipo de informação para dar uma experiência de ARIA muito mais correta e intuitiva.
* Resolvido um raro bug no Internet Explorer quando se navega por marcas ou iFrames.
* em documentos do Microsoft Word, as linhas da direita para a esquerda (como no texto árabe) podem novamente ser lidas. (#627)
* Significativa redução do atraso que ocorria quando grandes quantidades de texto eram exibidas num console de comandos do Windows em sistemas de 64 bits. (#622)
* em aplicações do Microsoft Office, o NVDA já não trava quando se pressiona falar primeiro plano (NVDA+b) ou quando se navega alguns objetos em barras de ferramentas. (#616)
* Corrigido o anúncio incorreto dos números que contém um 0 depois de um separador; ex.: 1.023. (#593)
* Adobe Acrobat Pro e Reader 9 já não travam quando se fecha um arquivo ou ao executar outras certas tarefas. (#613)
* A seleção agora é anunciada quando se pressiona control+a para selecionar todo o texto em alguns controles de texto editáveis como no Microsoft Word. (#761)
* Nos controles de Scintilla (ex.: Notepad++), O texto já não é selecionado incorretamente quando o NVDA move o cursor do sistema tal como durante leitura contínua. (#746)
* É novamente possível revisar o conteúdo de células no MS Excel com o cursor de exploração.
* O NVDA pode novamente ler por linhas em certos campos de área de texto outrora problemáticos no Internet Explorer 8. (#467)
* O Windows Live Messenger 2009 já não se encerra inmediatamente depois de ser iniciado enquanto o NVDA está em execução. (#677)
* Nos navegadores web, já não é necessário pressionar tab para interagir com um objeto embutido (tal como conteúdo Flash) depois de pressionar enter no objeto embutido ou voltando de outra aplicação. (#775)
* em controles de Scintilla (ex.: Notepad++), o início de linhas longas já não é cortado quando sobrepassam a tela. também, estas linhas longas são mostradas corretamente em braille quando selecionadas.
* No Loudtalks, agora é possível acessar à lista de contatos.
* A URL do documento e "MSAAHTML Registered Handler" já não se anuncia algumas vezes falsamente no Internet Explorer e outros controles MSHTML. (#811)
* em árvores no IDE de Eclipse,  o elemento enfocado anteriormente já não se anuncia incorretamente quando o foco se move para um novo elemento.

## 2010.1

Esta revisão enfóca-se principalmente em Correção de Falhas e melhoras na experiência do usuário, incluindo algumas correções significativas de estabilidade.

### Novas características

* O NVDA já não falha ao ser executado em um sistema sen dispositivos de saída de áudio. Obviamente, será necessário utilizar uma linha braille ou o Display synthesiser para a saída neste caso. (#425)
* Foi adicionada uma caixa de seleção Anunciar Zonas ao diálogo de Opções de formatação de Documentos que lhe permite configurar se o NVDA deve anunciar zonas em documentos web. Para compatibilidade com a versão anterior, a opção está ativada de maneira predeterminada.
* Quando a opção falar teclas de comandos está ativada, o NVDA agora anuncia os nomes das teclas multimedia (ex.: reproduzir, parar, página inicial, etc.) quando são pressionadas. (#472)
* O NVDA agora anuncia a palavra que está sendo apagada quando se pressiona control+backspace em controles que o suportem. (#491)
* As setas agora podem ser utilizadas na janela do formatador Web para navegar e ler o texto. (#452)
* Melhor suporte de documentos embutidos editáveis do NVDA (modo de desenho) no Internet Explorer. (#402)
* um novo comando (nvda+shift+menos do teclado numérico) lhe permite mover o foco do sistema para o navegador de objetos atual.
* Novos comandos para bloquear e desbloquear os botões esquerdo e direito do mouse. Útil para a execução com operações de arrastar e soltar. shift+dividir do teclado numérico para bloquear/desbloquear o esquerdo, shift+multiplicar do teclado numérico para bloquear/desbloquear o direito.
* Novas tabelas de tradução braille: braille de computador Alemão de 8 pontos, Alemão grao 2, braille de computador Finlandês de 8 pontos, Chinês (Hong Kong, Cantonês), Chinês (Taiwan, Mandarim). (#344, #369, #415, #450)
* Agora é possível desativar a criação do atalho da área de trabalho (e assim a tecla de atalho) quando se instala o NVDA. (#518)
* O NVDA agora pode utilizar IAccessible2 quando presente em aplicações de 64 bit. (#479)
* A API NVDA Controller Client proporcionada agora para permitir ás aplicações controlar o NVDA; ex.: para falar texto, silenciar a voz, mostrar uma mensagen em braille, etc.
* As mensagens de informação e erro agora são lidas na tela de logon no Windows Vista e no Windows 7. (#506)
* No Adobe Reader, os formulários PDF interativos desenvolvidos com Adobe LiveCycle agora são suportados. (#475)
* No Miranda IM, o NVDA agora lê automaticamente as mensagens de entrada em janelas de chat se o anúncio de Alterações nos conteúdos dinâmicos estiver ativado. Também foram adicionados os comandos para anunciar as três mensagens mais recentes (NVDA+control+número). (#546)
* Agora são suportados campos de entrada de texto em conteúdo de Adobe Flash. (#461)

### Alterações

* A mensagem de ajuda de teclado de extrema verbosidade no menu iniciar do Windows 7 já não é anunciada.
* O sintetizador Display agora foi substituido por um novo Exibidor de Fala. Para ativá-lo, escolha Exibidor de Fala desde o menu Ferramentas. O Exibidor de Fala pode ser utilizado independentemente de com que outro sintetizador de voz esteja trabalhando.
* As mensagens na linha braille serão rejeitadas automaticamente se o usuário pressionar uma tecla que signifique uma mudança  como o movimento do foco. Anteriormente a mensagem sempre permaneceria segundo o seu tempo configurado.
* A opção para vincular o braille ao foco ou ao cursor de exploração (NVDA+control+t) agora pode ser também configurada desde o diálogo de opções de braille, e agora também pode ser salva nas configurações do usuário.
* atualizado o sintetizador de voz eSpeak para a versão 1.42.04.
* atualizado o transcritor braille liblouis para a versão 1.8.0.
* nos buffers virtuais, o anúncio de elementos quando se move por caracteres ou palavras foi sensivelmente melhorado. Anteriormente, era anunciada uma grande quantidade de informação irrelevante e o anúncio era muito diferente a esse quando se move por linhas. (#490)
* A tecla Control agora simplesmente para a voz como outras teclas, em lugar de pausar a voz. Para pausar/continuar a voz, utilize a tecla shift.
* A quantidade de linhas e colunas das tabelas já não é anunciada quando se anunciam as Alterações do foco, posto que este anúncio é de demasiada verbosidade e normalmente inútil.

### Correção de Falhas

* O NVDA já não falha ao ser executado se o suporte UI Automation parece estár disponível mas por alguma razão falha ao inicializar-se. (#483)
* Todo o conteúdo de uma linha de uma tabela já não é anunciado algumas vezes quando se move o foco entre células em aplicações da mozilla. (#482)
* O NVDA já não se atrasa durante um tempo longo quando se expande itens de vista em árvore que contenham uma quantidade muito grande de sub-itens.
* quando se lista vozes SAPI 5, o NVDA agora tenta detectar vozes defeituosas e excluí-las do diálogo de Opções de Voz e do Anel de Opções de Voz. Anteriormente, quando havia uma voz problemática, o driver SAPI 5 do NVDA falhava algumas vezes ao iniciar-se.
* Os buffers virtuais agora anunciam as teclas de atalho dos objetos, opção que se encontra no diálogo de Apresentação de objetos. (#486)
* Nos buffers virtuais, as coordenadas de linha/coluna já não são lidas incorretamente por cabeçalhos de linha e coluna quando o anúncio de tabelas está desativado.
* nos buffers virtuais, as coordenadas de linha/coluna agora são corretamente lidas quando você abandona uma tabela e logo volta a entrar na mesma célula da tabela sen visitar antes outra célula; ex.: pressionando seta acima e logo seta abaixo sobre a primeira célula de uma tabela. (#378)
* As linhas em branco nos documentos do Microsoft Word e dos controles de edição de Microsoft HTML agora são mostradas apropriadamente em linhas braille. Anteriormente o NVDA mostraba a frase atual na linha, não a linha atual para estas situações. (#420)
* Múltiplas correções de segurança quando se executa o NVDA no Logon do Windows e outras Áreas de Trabalho Seguras.
* A posição do cursor (cursor do sistema) agora atualiza-se corretamente ao fazer uma leitura Completa na qual se passe do final da tela, em campos de edição padrões do Windows e documentos do Microsoft Word. (#418)
* nos buffers virtuais, o texto já não é incluído incorretamente por imagens dentro de links e clicáveis que são marcados como irrelevantes para os leitores de tela. (#423)
* Correções para o layout de teclado laptop. (#517)
* quando o braille está vinculado à exploração, ao enfocar uma janela de console do dos, o cursor de exploração agora pode navegar apropriadamente pelo texto no console.
* enquanto se trabalha com TeamTalk3 ou TeamTalk4 Classic VU a barra de progresso contador na janela principal já não é anunciada conforme se atualiza. Também os caracteres especiais podem ser lidos apropriadamente na janela de entrada do chat.
* Os itens já não são falados dúas vezes no menu iniciar do Windows 7. (#474)
* Ao ativar links para a mesma página no Firefox 3.6 móve-se o cursor apropriadamente no buffer virtual para o lugar correto na página.
* corrigido o problema onde alguns textos não eram disponibilizados no Adobe Reader em certos documentos PDF.
* O NVDA já não fala incorretamente certos números separados por um ifen; ex.: 500-1000. (#547)
* No Windows XP, o NVDA já não faz com que o Internet Explorer trave quando se alterna caixas de seleção no Windows Update. (#477)
* quando se utiliza no sintetizador eSpeak integrado simultaneamente voz e beeps, já não causa travamentos intermitentes em alguns sistemas. Isto era mais evidente, por exemplo, quando se copiava quantidades grandes de dados no Windows Explorer.
* O NVDA já não anuncia que um documento do Firefox está ocupado (ex.: devido a uma atualização ou recarga) quando esse documento está em segundo plano. Isto também fazia com que a barra de status da aplicação em primeiro plano fosse anunciada falsamente.
* quando é alterado o layout de teclado do Windows (com control+shift ou alt+shift), o nome completo do layout é anunciado em voz e braille. Anteriormente só se anunciava em voz, e layouts alternativos (ex.: Dvorak) não eram anunciados.
* Caso o anúncio de tabelas esteja desativado, a informação de tabela já não é anunciada quando o foco muda.
Certos controles de vista em árvore em aplicações de 64 bit (como o conteúdo de vista em árvore no Microsoft HTML Help) são agora acessíveis. (#473)
* Resolvidos alguns problemas com o registro de mensagens que contém caracteres não-ASCII. Isso poderia causar falsos erros em alguns casos em sistemas que não estão em inglês. (#581)
* A informação no Diálogo Sobre o NVDA agora aparece no idioma configurado pelo usuário em lugar de somente em Inglês. (#586)
* Problemas já não são encontrados ao usar o Anel de Opções de Voz depois que a voz é alterada para uma que possui menos opções que a anterior.
* No Skype 4.2, os nomes dos contatos já não são falados duas vezes na lista de contatos.
* :Resolvido um potencial desperdício maior de memória no menu e nos buffers virtuais. (#590, #591)
* Trabalho sobre um desagradável problema em alguns sintetizadores SAPI 4 que causavam erros e travamentos frequentes no NVDA. (#597)

## 2009.1

O mais destacável desta versão inclui o suporte para versões de 64 bit do Windows; suporte significativamente melhorado para os documentos do Microsoft Internet Explorer e do Adobe Reader; suporte para Windows 7; leitura das telas de  logon do Windows, control+alt+delete e o controle de contas de usuário (UAC); e a capacidade para interagir com os conteúdos do Adobe Flash e de Sun Java em páginas web. Também nota-se várias correções significativas de estabilidade e melhoras na experiência do usuário em geral.

### Novas Características

* Suporte oficial para verções de 64 bit do Windows! (#309)
* adicionado um driver para o sintetizador Newfon. Tenha em conta que isto requer uma versão especial do Newfon. (#206)
* nos buffers virtuais, o modo de foco e o modo de navegação agora podem ser anunciados utilizando sons em lugar da voz. isto está ativado por padrão. Pode ser configurado desde o diálogo de Opções do Buffer Virtual. (#244)
* O NVDA já não interrompe a voz quando as teclas de controle do volume são pressionadas no teclado, permitindo ao usuário alterar o volume e ouvir os resultados atuais imediatamente. (#287)
* Reescrito Completamente o suporte para documentos do Microsoft Internet Explorer e Adobe Acrobat. Este suporte foi unificado com suporte interno utilizado pelo mozilla Gecko, assim características como a interpretação mais rápida de páginas, navegação extensa e rápida, lista de links, seleção de texto, modo de foco automático e suporte de braille estão agora disponíveis nestes documentos.
* melhorado o suporte para o controle da seleção de data encontrado no diálogo de propriedades de data/Hora no Windows Vista.
 * melhorado o suporte para o menu iniciar Moderno XP/Vista (específicamente os menus Todos os programas e lugares). A informação de nível apropriada é agora anunciada.
* A quantidade de texto que é anunciada com movimento do mouse, é agora configurável desde o diálogo Opções do mouse. uma escolha de parágrafo, linha, palavra ou caractere pode ser feita.
* Anúncio de erros ortográficos sob o cursor no Microsoft Word.
* suporte para correção ortográfica no Microsoft Word 2007. Suporte Parcial pode estar disponível para versões anteriores do Microsoft Word.
* Suporte melhorado para o Windows Live Mail. Agora mensagens de texto plano podem ser lidas e o editor de mensagens de texto e html são utilizáveis.
* No Windows Vista, quando o usuário se move para a área de trabalho segura (ou porque um diálogo de controle do UAC aparece, ou porque foi pressionado control+alt+delete), o NVDA anunciará o fato de que o usuário agora está na área de trabalho segura.
* O NVDA pode anunciar texto sob o mouse dentro de janelas do console do dos.
* suporte para UI Automation através da API cliente UI Automation disponível no Windows 7, assim como foi melhorada a experiência do NVDA no Windows 7.
* O NVDA pode ser configurado para iniciar automaticamente depois de seu logon no Windows. A opção encontra-se no Diálogo de Opções Gerais.
* O NVDA pode ler telas seguras do Windows como a autentificação do Windows (logon), control+alt+Backspace e telas do UAC no windows XP e posteriores. A leitura das telas de logon do Windows pode ser configurada desde o diálogo de Opções gerais. (#97)
* adicionado um driver para as linhas braille da série Optelec ALVA BC6.
* Ao navegar por documentos web, agora pode pressionar n e shift+n para saltar para frente e para trás passando blocos de links, respectivamente.
* Ao navegar por documentos web, as marcas de ARIA agora são anunciadas, e você pode mover-se para frente e para trás entre eles utilizando d e shift+d, respectivamente. (#192)
* O diálogo de lista de links disponível quando se explora documentos web agora foi convertido num diálogo de Lista de Elementos que pode listar links, cabeçalhos e marcas. Cabeçalhos e marcas são apresentados herárquicamente. (#363)
* O novo diálogo da Lista de Elementos filtra a lista conforme o que você escreve para conter somente aqueles elementos que contém o texto que foi digitado. Pode pressionar Backspace para limpar o filtro de modo que todos os elementos sejam apresentados novamente. (#173)
* As versões portáteis do NVDA agora procuram na pasta "userConfig" dentro da pasta do NVDA, as configurações do usuário. Como a versão do instalador, isto mantén a configuração do usuário separada do NVDA.  
* As app modules personalizadas, os drivers das linhas braille e os drivers de sintetizadores agora podem ser armazenados  na pasta de configurações do usuário. (#337)
* Os buffers virtuais agora são interpretados em segundo plano, permitindo ao usuário interagir com sistema até certo ponto durante o processo de interpretação. O usuário será notificado de que o documento está sendo interpretado se lhe levará mais de um segundo.
* Caso o NVDA detecte que travou por alguma razão, ignorará automaticamente todos os pressionamentos para que o usuário tenha uma maior possibilidade de recuperação do sistema.
* suporte para arrastar e soltar em ARIA no mozilla Gecko. (#239)
* A seleção do título do documento e linha atual agora é falada quando se move o foco dentro de um buffer virtual. Isto faz com que o comportamento quando se move o foco nos buffers virtuais seja consistente como em um documento normal. (#210)

> - nos buffers virtuais, agora é possível interagir com os objetos embutidos (como conteúdos Adobe Flash e Sun Java) pressionando enter sobre o objeto. Se for acessível, pode então moverse com Tab por ele como qualquer outra aplicação. Para voltar o foco para o documento, pressione NVDA+espaço. (#431)

* nos buffers virtuais, o e shift+o moven ao seguinte e ao anterior objeto embutido, respectivamente.
* O NVDA agora pode acessar completamente aplicações executadas como administrador no Windows Vista e posteriores. Você deve instalar uma versão oficial do NVDA  para que isso seja possível. Isso não funciona para versões portáteis e snapshots. (#397)

### Alterações

* O NVDA já não anuncia "NVDA ativado" quando é iniciado.
* Os sons de início e finalização agora são reproduzidos utilizando o dispositivo de saída de áudio configurado no NVDA em lugar do dispositivo de áudio padrão do Windows. (#164)
* o anúncio das barras de progresso foi melhorado. O mais notável é que agora é possível configurar o NVDA para anunciá-las através de voz e beeps ao mesmo tempo.
* algumas funções genéricas, como painel, aplicação e marca, já não são anunciados  no foco a menos que o controle não tenha nome.
* O comando copiar com exploração (NVDA+f10) copia o texto desde em cima da marca de início e inclue a posição atual da exploração, em lugar de excluií-la . isto permite que o último caractere de uma linha seja copiado, o que não era possível anteriormente. (#430)
* O script  navigatorObject_where (ctrl+NVDA+numpad5) foi removido. Esta combinação de teclas não funcionava em alguns teclados, nem o script era considerado útil.
* O script navigatorObject_currentDimentions foi remapeado para NVDA+delete do teclado numérico. A antiga combinação de teclas não funcionava em alguns teclados. Este script agora também anuncia a largura e a altura do objeto em lugar das coordenadas direita/inferior.
* melhorado o rendimento (especialmente em netbooks) quando ocorrem muitos beeps em sucessão rápida; ex.: movimentos rápidos com o mouse com as coordenadas de áudio ativadas. (#396)
* O som de erro do NVDA já não é reproduzido em release candidates e versões finais. Note que os erros continuam sendo registrados no log.

### Correção de Falhas

* quando o NVDA é executado a partir de um caminho de DOS 8.3, mas está instalado no caminho longo relacionado (ex.: progra~1 versus program files) NVDA identifica corretamente que é uma cópia instalada e carrega apropriadamente as opções do usuário.
* O anúncio do título da janela atual em primeiro plano com nvda+t funciona agora corretamente quando se está nos menus.
* O braille já não mostra informações desnecessárias no seu contexto de foco tal como painéis não etiquetados.
* já não se anuncia  algumas informações desnecessárias quando o foco muda como painéis raíz, painéis solapados e painéis deslizantes em aplicações Java ou Lotus.
* Faz-se com que o campo de procurar palavras chave  no visualizador de ajuda do Windows (CHM) seja muito mais usável. Devido à quantidade de falhas nesse controle, a palavra chave atual não poderia ser lida já que estaría continuamente mudando.
* Anuncia-se os números corretos de página no Microsoft Word se a numeração de página foi específicamente configurada  no documento.
* melhor suporte para campos de edição encontrados em diálogos do Microsoft Word (ex.: o diálogo Fontes). agora é possível navegar por estes controles com as setas.
* melhor suporte para consoles do Dos. específicamente: O NVDA agora pode ler o conteúdo de consoles particulares que Sempre se pensava estarem em branco. pressionando control+break já não fecha o NVDA.
* no windows Vista e posteriores, o instalador do NVDA agora o executa com privilégios de usuário normal quando tal é requerido para executar o NVDA  na tela final.
* Backspace agora é controlado corretamente quando se fala palavras ao escrever. (#306)
* Não se anuncia incorretamente "menu iniciar" para certos menus de contexto no Windows Explorer/Windows shell. (#257)
* O NVDA agora processa corretamente etiquetas de ARIA no mozilla Gecko quando não há outro conteúdo útil. (#156)
* O NVDA já não ativa incorretamente o modo de foco automaticamente para campos de texto editável que atualizam seu valor quando o foco muda; ex.: https://tigerdirect.com/. (#220)
* O NVDA agora tentará recuperar-se de algumas situações que anteriormente o fariam travar completamente. Poderá levar cerca de 10 segundos para que o NVDA detecte e se recupere de tais travamentos.
* quando o idioma do NVDA está configurado para "User default", utiliza o idioma do usuário do Windows configurado em lugar do local do Windows.
* O NVDA agora reconhece a existência de controles em AIM 7.
* O comando de deixar passar a tecla já não bloqueia quando uma tecla é mantida pressionada. Anteriormente, o NVDA deixava de aceitar os comandos nesses casos  e precisava ser reiniciado. (#413)
* A barra de tarefas já não é ignorada quando recebe o foco, o que muitas vezes ocorre quando se sae de uma aplicação. Anteriormente, o NVDA comportava-se como se o foco não tivesse mudado.
* Ao ler campos de texto em aplicações que utilizam Java Access Bridge (incluindo OpenOffice.org), o NVDA agora funciona corretamente quando o anúncio de números de linha está ativado.
* O comando de copiar com exploração (NVDA+f10) controla elegantemente o caso onde seja utilizado numa posição antes do marcador de início. Anteriormente, isto podía causar problemas como travamentos no Notepad++.
* Determinado caractere de controle (0x1) já não causa um comportamento extranho no eSpeak (como Alterações  no volume tom) quando encontrado em um texto. (#437)
* O comando anunciar seleção de texto (NVDA+shift+seta acima) agora anuncia perfeitamente que não existe seleção em objetos que não suportam seleção.
* Resolvido o problema no qual pressionando-se a tecla enter em certos botões ou links no Miranda-IM faziam com que o NVDA travasse. (#440)
* A linha ou seleção atual agora é respeitada ao soletrar ou copiar o objeto de navegação atual.
* Realizados trabalhos relativos a um problema do Windows  que fazia com que informações inúteis fossem anunciadas depois do nome de controles com links em diálogos do Windows Explorer e do Internet Explorer. (#451)
* Resolvido um problema com o comando anunciar data e hora (NVDA+f12). Anteriormente, anunciar data  estava truncado em alguns sistemas. (#471)
* Resolvido o problema onde o sinal do leitor de telas para o sistema algumas vezes era limpo inapropriadamente depois de interagir com telas seguras do Windows. Isso poderia causar problemas em aplicações que checam o  sinal do leitor de telas, incluindo Skype, Adobe Reader e Jart. (#462)
* Em caixas de combinação no Internet Explorer 6, o item ativo agora é anunciado quando alterado. (#342)

## 0.6p3

### Novas Características

* Como a barra de fórmulas do Microsoft Excel é inacessível para o NVDA, foi proporcionada uma caixa de diálogo específica do NVDA para editar quando o usuário pressionar f2 sobre uma célula. 
* suporte para formatação em controles de texto IAccessible2, incluindo aplicações da mozilla.
* Erros ortográficos poderão ser anunciados agora onde for possível. Isto é configurável através do diálogo de Opções de Formatação de Documentos.
* O NVDA pode ser configurado para bipar para todas ou apenas para as barras de progresso visíveis. Alternativamente, pode ser configurado para falar os valores das barras de progresso a cada 10%.
* Os links agora podem ser identificados em controles de edição multilinha.
* O mouse agora pode ser movido para o caractere sob o cursor de exploração  na maioría dos controles de texto editáveis. Anteriormente, O mouse só poderia ser movido para o centro do controle.
* Nos buffers virtuais, O cursor de exploração agora revisa o texto do buffer, em lugar de apenas o texto interno do navegador de objetos (o que muitas vezes não é útil para o usuário). Isto significa que pode navegar pelo buffer virtual hierarquicamente utilizando a navegação de objetos e o cursor de exploração moverá para esse ponto  no modo.
* Trabalho em alguns estados adicionais em controles Java.
* Se o comando ler título (NVDA+t) é pressionado dúas vezes rapidamente, soletra o título. Se for pressionada três vezes, este é copiado para a área de Transferência.
* A ajuda de teclado agora lê os nomes das teclas modificadoras quando pressionadas sozinhas.
* Os nomes de teclas anunciados pela ajuda de teclado agora são traduzíveis.
* adicionado suporte para o texto reconhecido em campos de SiRecognizer. (#198)
* Suporte para linhas braille!
* adicionado um comando (NVDA+c) para anunciar o texto  na área de transferência do Windows. (#193)
* agora você pode pressionar escape quando está em modo de foco para voltar ao modo de navegação.
* no modo de navegação, quando o foco muda ou o cursor é movido, o NVDA pode alternar automaticamente para o modo de foco ou modo de navegação segundo proceda para o controle sob o cursor. isto é configurado desde o diálogo de buffer virtual. (#157)
* Reescrito o driver do sintetizador SAPI4, o que substitui aos drivers sapi4serotek e sapi4ativeVoice e deve solucionar os problemas encontrados com os referidos drivers.
* A aplicação NVDA agora inclúi um manifesto, o que significa que não será mais executada em modo de compatibilidade no windows Vista.
* O arquivo de configuração e os dicionários de Fala são agora salvos  na pasta de configurações do usuário caso o NVDA tenha sido instalado utilizando o instalador. Isto é necessário para o Windows Vista e também permite a múltiplos usuários ter configurações individuais para o NVDA.
* adicionado suporte para informação da posição para controles IAccessible2.
* adicionada a capacidade para copiar texto para a área de transferência utilizando o cursor de exploração. NVDA+f9 ajusta a marca do início na posição atual do cursor de exploração. NVDA+f10 recupera o texto entre a marca do início e a posição atual do cursor de exploração e o copia para a área de transferência. (#240)
* adicionado suporte para alguns controles de edição  no programa pinacle tv.
* Ao anunciar texto selecionado para seleções longas (512 caracteres ou mais), o NVDA agora fala o número de caracteres selecionados, em lugar de falar toda a seleção. (#249)

### Alterações

* Se o dispositivo de saída de áudio estiver ajustado para utilizar o dispositivo padrão do Windows (Mapeador de  Som da Microsoft ), o NVDA agora alternará  para o novo dispositivo padrão para o eSpeak e os sons quando o dispositivo alternar. Por exemplo, o NVDA alternará para um dispositivo de áudio USB se este se tornar o dispositivo padrão automaticamente quando conectado.
* Melhorado o rendimento do eSpeak com alguns drivers de áudio no windows Vista.
* o anúncio de links, cabeçalhos, listas e citações em documentos é configurado agora  no Diálogo de Formatação de Documentos. Anteriormente, para configurar essas opções para os buffers virtuais, o Diálogo de Opções do Buffer Virtual era Usado. Agora todos os documentos compartilham essas configurações.
* A velocidade é agora a opção padrão no Anel de opções de voz do sintetizador.
* Melhoras no carregamento e descarga dos appModules.
* O comando ler título (NVDA+t) agora só informa o título em lugar de todo o objeto. Se o objeto em primeiro plano não ten nome, o nome do processo da aplicação é utilizado.
* em lugar de ativar e desativar o passe através do buffer virtual, o NVDA agora anuncia modo de foco (passe pelo buffer virtual ativado) e modo de navegação (passe pelo buffer virtual desativado).
* As vozes agora são salvas  no arquivo de configuração por ID em lugar de por index. isto faz as opções de voz mais seguras através das Alterações dos sistemas e as configurações. A opção de voz não será preservada em todas as configurações e um erro poderá ser mostrado no log na primeira vez que um sintetizador for utilizado. (#19)
* O nível de um item de vista em árvore agora é anunciado primeiro quando alterado desde o elemento enfocado anteriormente para todas as vistas em árvore. Anteriormente, isto só ocurría para vistas em árvore nativas do Windows (SysTreeView32).

### Correção de Falhas

* A última parte do áudio já não é cortada quando o NVDA É utilizado com O eSpeak em um servidor remoto de área de trabalho.
* Corrigidos problemas ocorridos ao salvar dicionários de fala para certas vozes.
* Resolução do atraso quando se move por outras unidades que não sejam caractere (palavra, linha, etc.) para o final dos documentos de texto plano longos no modo de navegação da mozilla Gecko. (#155)
* Se a opção falar palavras digitadas estiver ativada, o NVDA anunciará a palavra quando enter for pressionado.
* corrigidos alguns grupos de sucessões de caracteres em documentos enriquecidos. preferências de Formataçãoo de Documentos. isto inclui buffers virtuais da mozilla Gecko.
* O visualizador de log do NVDA agora utiliza caixas multilinha em lugar de apenas editar para mostrar o log. isto melhora a leitura por palavras com o NVDA e lhe permite ler o texto do log mais além dos 65535 bytes.
* corrigidas algumas falhas relacionadas com os objetos embutidos em controles de edição multilinha.
* O NVDA agora lê os números de página no Microsoft Word. (#120)
* Corrigida a falha onde ao mover-se com Tab para uma caixa de seleção marcada em um buffer virtual da mozilla Gecko e pressionando espaço não anunciava que a caixa de seleção estaba sendo desmarcada.
* Informação correta das caixas de seleção parcialmente marcadas em aplicações da mozilla.
* Se a seleção de texto expande-se ou é contraída em ambas as direções, a seleção é lida como uma parte em lugar de duas.
* quando se lê com o mouse, o texto nos campos de edição da mozilla Gecko agora deve ser lido.
* Ler tudo já não deve fazer com que certos sintetizadores SAPI5 travem.
* corrigida uma falha que significaba que Alterações  na seleção de texto não eram lidas em controles padrões de edição do Windows antes da primeira alteração do foco depois que o NVDA era iniciado.
* corrigido o seguimento do mouse em objetos Java. (#185)
* O NVDA já não anuncia os itens das árvores Java sen filhos como se estivessem recolhidos.
* Anúncio do objeto com foco quando uma janela Java é trazida ao primeiro plano. Anteriormente, apenas o objeto de nível superior Java era anunciado.
* O driver do sintetizador eSpeak já não para completamente enquanto fala depois de um erro simples.
* Corrigida a falha onde ao atualizar parâmetros de voz (velocidade, ton, etc.) estes não eram salvos quando a voz era alterada desde o Anel de Opções de Voz.
* melhorada a fala de caracteres e palavras escritas.
* Alguns textos novos que anteriormente não eram falados em aplicações de console de texto (como alguns texto de jogos conversacionais) são agora falados.
* O NVDA agora ignora Alterações do foco nas janelas em segundo plano. Anteriormente, uma mudança do foco em segundo plano poderia ser tratada como se o foco real tivesse sido alterado.
* melhorada a detecção do foco quando se sai dos menus de contexto. Anteriormente, o NVDA muitas vezes não reagia apropriadamente quando se saía de um menu de contexto.
* O NVDA agora anuncia quando o menu de contexto é ativado  no menu iniciar.
* O menu iniciar clássico agora é anunciado como menu iniciar em lugar de menu Aplicação.
* melhorada a leitura de alertas como aquélas encontradas no mozilla Firefox. O texto já não deve ser lido múltiplas vezes e outra informação extranha já não será lida. (#248)
* O texto enfocável, campos de edição somente leitura já não são  incluídos quando se recolhe o texto de diálogos. isto corrige, por exemplo, a leitura automática de toda a aceitação da licença nos instaladores.
* O NVDA já não anuncia a desseleção de texto quando se abandona alguns controles de edição (exemplo: barra de enderesso do Internet Explorer, campos de enderesso em correio eletrônico no Thunderbird 3 ).
* Ao abrir e-mails em texto plano  no Outlook Express e Windows Mail, o foco é corretamente colocado  na mensagem lista para que o usuário o leia. Anteriormente o usuário tinha que pressionar tab ou clicar sobre a mensagem para utilizar as teclas do cursor para lê-lo.
* corrigidos vários problemas maiores com a funcionalidade "falar Teclas de comando".
* O NVDA agora pode ler textos que passem de 65535 caracteres em controles padrões de edição (ex.: um arquivo grande no Notepad).
* melhorada a leitura de linhas em campos de edição de MSHTML (mensagens editáveis do Outlook Express e campos de entrada de texto no Internet Explorer).
* O NVDA já não trava completamente algumas vezes  quando se edita texto no OpenOffice. (#148, #180)

## 0.6p2

* melhorada a voz padrão do ESpeak no NVDA
* adicionado um esquema de teclado para computadores portáteis. O esquema de teclado pode ser configurado desde o Diálogo de Opções de Teclado do NVDA. (#60)
* suporte para grupos de elementos em controles SysListView32, encontrados principalmente no windows Vista. (#27)
* Informação do estado selecionado de itens de vista em árvore em controles SysTreeview32.
* Adicionadas teclas de atalho para muitos dos diálogos de configuração do NVDA
* Suporte para IAccessible2 habilitado para aplicações como mozilla Firefox quando se executa o NVDA desde um dispositivo portátil, sem ter que registrar nenhum arquivo Dlh em especial.
* corrigido um problema com a lista de links do buffer virtual em aplicações Gecko. (#48)
* O NVDA já não  trava com aplicações mozilla Gecko como Firefox e Thunderbird quando está sendo executado com privilégios mais altos que os da aplicação mozilla Gecko. Ex. o NVDA é executado como Administrador.
* dicionários de fala (anteriormente dicionários do usuário) agora podem ser sensíveis ou não às maiúsculas e os padrões podem ser opcionalmente expressões regulares. (#39)
* agora pode ser configurado si o NVDA utiliza ou não um 'modo de apresentação de tela' para os documentos do buffer virtual  desde um diálogo de opções.
* não são informadas mais sobre ancoragem de etiquetas sen href em documentos Gecko como links. (#47)
* O comando procurar do NVDA agora lembra qual o último texto procurado, para todas as aplicações. (#53)
* corrigidos problemas onde o estado marcado não era anunciado em algumas caixas de seleção e botões de opção no modo de navegação.
* O modo de passe através do buffer virtual é específico agora para cada documento, em lugar de globalmente para o NVDA. (#33)
* Corrigida alguma lentidão com as Alterações do foco e interrupção incorreta da voz que algumas vezes ocurriam quando se utilizava o NVDA em um sistema que estava em espera ou estava muito lento.
* melhoras no suporte para caixas de combinação no mozilla Firefox. Especificamente quando se navega com as setas por elas, seus textos não são repetidos, e ao saltar para fóra deles, os controles originais não são anunciados desnecessariamente. Agora também os comandos do buffer virtual funcionam quando recebem o foco estando num buffer virtual.
* melhorada a precisão da procura da barra de status em muitas aplicações. (#8)
* adicionada a ferramenta de console python interativo do NVDA, para habilitar aos desenvolvedores para consultar e manipular questões internas do NVDA conforme este é executado.
* Os scripts LerTudo, AnunciarSeleção e anunciarLinhaatual agora funcionam apropriadamente quando se está  no modo passar através do buffer virtual. (#52)
* Os scripts Aumentar velocidade e Diminyuir velocidade foram removidos. Os usuários devem utilizar os scripts do Anel de Opções de Voz (control+nvda+setas) ou o diálogo de opções de Voz
* Melhoradas a ordem e a escala dos beeps na barra de progresso 
* adicionadas mais teclas de navegação rápida para o novo buffer virtual:  l para lista, i para iten de lista, e para campo de edição, b para botão, x para caixa de seleção, r para botão de opção, g para gráfico, q para citações, c para caixa de combinação, 1 a 6 para os respectivos níveis de cabeçalho, s para separador, m para marca. (#67, #102, #108)
* O cancelamento do carregamento de um novo documento no mozilla Firefox permite agora ao usuário seguir utilizando o antigo documento do  buffer virtual se o velho documento não foi realmente destruido ainda. (#63)
* A navegação por palavras no modo de navegação é agora mais precisa enquanto as palavras não contenham acidentalmente texto de mais de um campo. (#70)
* melhorada a exatidão do seguimento do foco e a atualização do foco quando se navega em buffers virtuais da mozilla Gecko.
* adicionado um script findNext (shift+NVDA+f3) para utilizar  no novo buffer virtual 
* Corrigida a lentidão em diálogos do mozilla Gecko (no Firefox e Thunderbird). (#66)
* adicionada a capacidade para ver o arquivo log atual para o NVDA. pode ser encontrado no menu NVDA -> Ferramentas
* Scripts como Data e hora levam em conta agora o idioma atual; pontuação e ordenamento das palavras agora se ajustam ao idioma 
* A caixa de combinação do idioma no diálogo de Opções gerais do NVDA mostra agora os nomes dos idiomas completos para facilidade de uso
* quando se revisa texto no objeto de navegação atual, o texto estará sempre atualizado caso seja alterado dinamicamente. Ex.: revisando o texto de um item de lista  na Barra de Tarefas. (#15)
* quando você se move com o mouse, o parágrafo atual de texto sob ele agora é anunciado, em lugar de todo o texto nesse objeto particular ou apenas a palavra atual. também as coordenadas de áudio, e o anúncio das funções do objeto é opcional, são desativados por padrão.
* suporte para leitura de texto com mouse no Microsoft Word
* corrigido um erro onde ao abandonar a barra de menu em aplicações como Wordpad podería fazer com que a seleção de texto não fosse mais anunciada.
* No Winamp, o título da faixa já não é anunciado repetidamente quando se muda de faixa, ou ao pausar/tocar/parar a reprodução.
* No Winamp, adicionada a capacidade para anunciar o estado dos controles Aleatório e repetição conforme sejam ativados. Funciona na janela principal e  no editor de listas de reprodução
* melhorada a capacidade para ativar campos particulares no buffer virtual de mozilla Gecko. Poderá incluir gráficos clicáveis, links que contenham parágrafos, e outras estruturas raras
* corrigido um atraso inicial ao abrir diálogos do NVDA em alguns sistemas. (#65)
* adicionado suporte específico para a aplicação Total Commander
* corrigida uma falha  no driver sapi4serotek onde o tom bloqueava num valor particular, isto é, permanecia alto depois de ler uma letra maiúscula. (#89)
* Anúncio do texto clicável e outros campos como clicáveis nos buffers virtuais da mozilla Gecko. ex.:  a campo que tenha um atributo onclick HTML. (#91)
* quando nos movemos pelos buffers virtuais da mozilla Gecko, desloca-se o campo atual para ver -- útil para que os companheiros videntes tenham uma ideia de onde está o usuário  no documento (#57)
* Adicionado suporte básico para que área de regiões ativas mostre eventos em aplicações habilitadas para IAccessible2 Útil  na aplicação de IRC Chatzilla, as novas mensagens agora serão lidas automaticamente 
* Algumas melhoras pequenas para ajudar a utilizar aplicações web com capacidade de ARIA,  ex.: Google Docs
* Eliminada a adição de linhas em branco extras ao texto ao copiar desde um buffer virtual 
* A tecla espaço deixou de ativar links na lista de links.  agora pode ser utilizado como outras letras para começar a digitação do nome de um link em particular ao qual deseje ir
* O script moveMouseToNavigator (NVDA+barra do teclado numérico) agora move o mouse para o centro do objeto de navegação, em lugar  de o mover para o canto superior esquerdo.
* adicionados comandos para clicar com os botões esquerdo e direito do mouse (barra e asterisco do teclado numérico respectivamente)
* melhorado o acesso à Barra do Sistema do Windows. Com a esperança de que o foco já não deve parecer ficar  para trás em um elemento em particular. Lembrete: para ir à Barra do sistema utilize o comando do Windows Tecla Windows+b. (#10)
* Melhorado o rendimento e eliminado o anúncio de texto adicional quando se mantém pressionada uma tecla de cursor em um campo de edição e é alcançado o final
* Eliminada a capacidade do NVDA para fazer com que o usuário espere enquanto mensagens em particular são faladas. Isto resolve algumas falhas e travamentos com sintetizadores de voz em particular. (#117)
* adicionado suporte para o sintetizador de voz Audiologic Tts3, contribuição de Gianluca Casalino. (#105)
* Possível melhora de rendimento quando se navega por documentos no Microsoft Word
* melhorada a precisão ao ler textos de avisos em aplicações da mozilla Gecko
* Eliminados possíveis travamentos ao tentar salvar a configuração em versões do Windows que não estejam em inglês. (#114)
* Adicionado um diálogo de boas vindas do NVDA. Este diálogo está programado para proporcionar informação essencial para novos usuários e permite ao Caps Loc ser configurado como uma tecla modificadora do NVDA. Este diálogo será mostrado por padrão quando o NVDA for iniciado até que seja desabilitado.
* corrigido o suporte básico para o Adobe Reader de forma que é possível ler documentos nas  versões 8 e 9
* corrigidos alguns erros que podiam ocurrer quando se mantinha pressionadas teclas antes que o NVDA fosse apropriadamente inicializado
* Se o usuário configurou o NVDA para salvar a configuração ao saír, assegura-se de que a configuração é apropriadamente salva quando se desliga ou ao fazer logoff no Windows.
* adicionado um som de logo do NVDA ao iniciar o instalador, contribuição de Victor Tsaran
* O NVDA, tanto ao ser executado através do instalador como de outra forma, deve retirar apropriadamente seu ícone da barra do sistema quando encerrado
* Etiquetas para controles padrões em diálogos do NVDA (como botões Ok e Cancelar) devem ser mostrados agora  no idioma para o qual o NVDA está configurado, em lugar de o ser somente em Inglês.
* O ícone do NVDA deve ser agora utilizado pelas teclas de atalho do NVDA  no menu iniciar e na área de trabalho, em lugar de um ícone de aplicação padrão.
* Ler células no MS Excel quando você se move com tab e shift+tab. (#146)
* Corrigidas algumas verbalizações duplicadas em listas em particular no Skype.
* Melhorado o seguimento do cursor em aplicações IAccessible2 e Java; ex.: no Open Office e Lotus Symphony, o NVDA espera adequadamente que o cursor se mova em documentos em lugar de ler acidentalmente a palavra ou linha incorreta  no final de alguns parágrafos. (#119)
* suporte para controles AkelEdit encontrados no Akelpad 4.0
* O NVDA já não bloqueia no Lotus Synphony quando se move desde o documento à barra de menus.
* O NVDA já não trava nos applets de programas Add/Remove no windows XP quando se executa um desinstalador. (#30)
* O NVDA já não trava quando se abre Spybot Search and Destroy

## 0.6p1

### Acesso ao conteúdo da web com os novos buffers virtuais em processo (até aquí para aplicações Mozilla Gecko incluindo Firefox3 e Thunderbird3)

* Os tempos de carregamento foram melhorados quase por um fator de trinta (já não é preciso esperar em toda ou maior parte das páginas web para serem carregadas  no buffer virtual)
* adicionada uma lista de links (NVDA+f7)
* melhorado o diálogo procurar (control+nvda+f) de forma que se efetua uma procura insensível às maiúsculas, mais resolução de uns poucos problemas com o foco nessa caixa de diálogo.
* agora é possível selecionar e copiar texto nos novos buffers virtuais 
* Os novos buffers virtuais por padrão representam o documento numa apresentação de tela (links e controles não estão em linhas separadas a menos que realmente sejam visualmente assim). pode-se alternar esta característica com NVDA+v.
* É possível mover-se por parágrafos com control+seta acima e control+seta abaixo.
* melhorado o suporte para conteúdos dinâmicos.
* melhorado por cima toda a precisão da leitura de linhas e campos quando se sobe ou dece com as setas. 

### Internacionalização

* agora é possível digitar caracteres acentuados que  dependen de "apenas um caractere", enquanto o NVDA está em execução.
* O NVDA anuncia agora quando a distribuição de teclado é alterada (pressionando-se alt+shift).
* A característica de anúncio de data e hora toma agora as opções regionais e de idioma atuais do sistema.
* adicionada tradução para o Checo (por Tomas Valusek com a ajuda de Jaromir Vit)
* adicionada tradução para o vietnamita por Dang Hoai Phuc
* adicionada ttradução para o Africaans (af_ZA), por Wilhem van der Walt.
* adicionada tradução para o russo por Dmitry Kaslin 
* adicionada tradução para o polonês por DOROTA CZAJKA e amigos.
* adicionada tradução para o japonês por Katsutoshi Tsuji.
* adicionada tradução para o tailandês por Amorn Kiattikhunrat
* adicionada tradução para o idioma croata por Mario Percinic e Hrvoje Katic  
* adicionada tradução para o galego por Juan C. Buño 
* adicionada tradução para o ucraniano por Aleksey Sadovoy 

### Voz

* O NVDA agora ven embalado com o eSpeak 1.33 que contén muitas melhoras. Entre as quais estão idiomas melhorados, variantes nomeadas e capacidade para falar mais rápido.
* O diálogo de opções de voz agora lhe permite alterar a variante de um sintetizador si este o suportar. A variante é normalmente uma ligeira variação da voz atual. (o eSpeak suporta variantes).
* adicionada a capacidade para alterar a inflexão de uma voz  no Diálogo de Opções de Voz caso o sintetizador atual o suporte. (o eSpeak suporta inflexão).
* adicionada a capacidade para desativar o anúncio da posição do objeto (ex.:. 1 de 4). Esta opção pode ser encontrada no Diálogo de Opções de Apresentação de objetos.
* O NVDA agora pode bipar quando verbaliza uma letra maiúscula. isto pode ser ativado e desativado  através de uma caixa de seleção  no Diálogo de Opções de Voz. também foi adicionada uma caixa de seleção de aumento do ton para maiúsculas para configurar se o NVDA atualmente deve ter seu ton aumentado para as maiúsculas. assim, você agora pode escolher entre ter o ton aumentado, dizer CAP, ou bipar, para maiúsculas.
* adicionada a capacidade para pausar a voz no NVDA (como é encontrada no Voice Over para o Mac). quando o NVDA está falando algo, pode pressionar as teclas control ou shift para silenciar a voz normalmente, mas se então pressionar a tecla shift novamente (caso não tenha pressionado qualquer outra tecla) a voz continuará exatamente de onde parou.
* adicionado um driver de sintetizador virtual, o qual extrai texto para uma janela em lugar de falá-lo através de um sintetizador de voz. isto deve ser mais agradável para desenvolvedores videntes que não são usuários de síntese de voz mas queren saber o que o NVDA está DIZENDO. Todavía há provavelmente algumas falhas, então respostas são muito bem vindas.
* O NVDA já não fala a pontuação por padrão. Você pode habilitar o anúncio da pontuação com NVDA+p.
* O eSpeak por padrão agora fala um pouco mais lento, o que deve torná-lo mais simples para pessoas que o utilizarão pela primeira vez, quando instalam ou começam a utilizar o NVDA.
* adicionados dicionários do usuário ao NVDA. Estes lhe permitem fazer com que o NVDA fale determinado texto de forma diferente. há três dicionários: padrão, voz e temporário. As entradas adicionadas ao dicionário padrão servirão a todo o tempo no NVDA. Os dicionários por voz são específicos para o sintetizador atual e a voz que atualmente esteja configurada. O dicionário temporário funciona para aquelas ocasiões em que pretenda fixar rápidamente uma regra enquanto executa uma tarefa em particular, mas não deseja que seja permanente (desaparecerá quando o NVDA for encerrado). Por agora, as regras são expressões regulares, não apenas texto normal.
* Os sintetizadores podem agora utilizar qualquer dispositivo de áudio de saída de seu sistema, configurando a caixa de combinação dispositivo de saída no diálogo Sintetizador antes de selecionar o sintetizador desejado.

### Desempenho

* O NVDA já não toma uma grande quantidade de memória do sistema ao editar mensagens em controles de edição mshtml
* melhorado o desempenho quando se revisa texto dentro de muitos controles que não têm atualmente um cursor real. Ex.: janela de históricos do MSN Messenger, elementos de vistas em árvore, elementos de vista de lista etc.
* melhorado o rendimento em documentos enriquecidos.
* O NVDA já não deve tornar-se lento consumindo demasiada quantidade de memória do sistema sen razão.
* corrigidas falhas de quando se põe o foco numa janela de console do dos três ou mais vezes. O NVDA tinha uma tendência a travar completamente.

### Teclas de comando

* NVDA+shift+numpad6 e NVDA+shift+numpad4 lhe permiten navegar ao seguinte ou ao anterior objeto em fluxo respectivamente. isto significa que pode navegar numa aplicação utilizando apenas estas dúas teclas sen se preocupar em navegar para o pai ou  para o primeiro filho conforme se mova através da hierarquía de objetos. Por exemplo nun navegador web tal como firefox, pode navegar no documento por objetos, utilizando apenas estas dúas teclas. Se o seguinte em fluxo ou o anterior em fluxo lhe coloca e desloca de um objeto, ou abaixo nun objeto, ouvirá beeps indicando a direção.
* agora é possível configurar opções de voz sem abrir o Diálogo correspondente, utilizando o Anel de Opções de Voz. Este é um grupo de opções de voz que permite alternar através do pressionamento de control+NVDA+direita e control+NVDA+esquerda. Para alterar uma opção utilize control+NVDA+acima e control+NVDA+abaixo.
* adicionado um comando para anunciar a seleção atual em campos de edição (NVDA+shift+seta acima).
* Um bom número de comandos do NVDA que anunciam texto (como anunciar linha atual etc) agora podem soletrar o texto se pressionados dúas vezes rápidamente.
* O Caps Loc, insert do teclado numérico e insert extendido podem ser todos utilizados como teclas modificadoras do NVDA. também se uma destas teclas for utilizada, pressionando-a dúas vezes rápidamente sen pressionar nenhuma outra, enviará a tecla ao sistema operacional, como se você a pressionasse sen que o NVDA estivesse sendo executado. Para fazer com que uma destas teclas torne-se modificadora do NVDA, marque súa caixa de seleção  no diálogo de Opções de Teclado (utilizado para ser chamado o diálogo de eco de teclado).

### suporte a aplicações

* Melhorado o suporte para documentos do Firefox e Thunderbird3. Os tempos de carregamento foram melhorados quase que por um fator de trinta, uma apresentação de tela é utilizada por padrão (pressione nvda+v para ativar ou desativar esta apresentação de tela), uma lista de links (nvda+f7 foi adicionada), o diálogo procurar (control+nvda+f) é agora insensível às maiúsculas, muito melhor suporte para conteúdo dinâmico, a seleção e cópia de texto é agora possível.
* nas janelas dos históricos do MSN Messenger e Windows Live Messenger, agora é possível selecionar e copiar texto.
* Melhorado o suporte para a aplicação audacity
* Adicionado suporte para alguns controles edit/text no Skype
* Melhorado o suporte para a aplicação Miranda instant messenger 
* Corrigidos alguns problemas com o foco de quando são abertas mensagens html e de texto planno no Outlook Express. 
* Os campos de mensagens de notícias do Outlook express agora são etiquetados corretamente
* O NVDA agora pode ler os endereços nos campos de mensagens do Outlook Express (para/de/cc etc)
* O NVDA agora deve estár mais preciso ao anunciar a próxima mensagem no outlook express quando é apagada uma mensagem na lista de mensagens.

### APIs e toolkits

* Melhorada a navegação de objetos pelos objetos de MSAA. Se uma janela possui um menu de sistema, barra de título, ou barras de deslocamento, agora é possível navegar por elas.
* Adicionado suporte para a API de acessibilidade IAccessible2. Uma parte da capacidade para anunciar mais tipos de controles, isto também permite ao NVDA acessar o cursor em aplicações como Firefox 3 e Thunderbird 3, lhe permitindo navegar, selecionar ou editar textos.
* Adicionado suporte para controles de edição de Scintilla (tais controles podem ser encontrados no Notepad++ ou no Tortoise SVN).
* adicionado suporte para aplicações Java (através do Java Access Bridge). isto pode oferecer suporte básico para Open Office (se o Java estiver ativado), e qualquer outra aplicação autônoma Java. Tenha em conta que os Applets de java dentro de um navegador web não poderão funcionar aínda.

### mouse

* Melhorado o suporte para a leitura do que esteja sob o ponteiro do mouse conforme se move. Agora é muito mais rápido e também possui a capacidade em alguns controles como campos de edição padrões, controles Java e IAccessible2, para ler a palavra atual, não só o objeto atual. isto poderá ter alguma utilidade a pessoas com deficiência visual que só queiram ler uma parte específica do texto com o mouse.
* Adicionada uma nova opção de configuração, encontrada  no Diálogo Opções do Mouse. Tocar sons de coordenada quando o mouse é movido, quando está selecionada, reproduz um beep de 40 ms cada vez que o mouse se move, com seu ton (entre 220 e 1760 hz) representando o eixo y, e o  volume esquerda/direita, representando o eixo x. isto capacita a uma pessoa cega ter uma idea aproximada de onde está o mouse  na tela conforme se mover. Esta característica também depende de que reportObjectUnderMouse também seja ativado. assim isto significa que é necessário deshabilitar rápidamente tanto o beep como o anúncio de objetos, então apenas pressione NVDA+m. Os beeps também são mais altos ou mais baixos dependendo da intensidade do brilho da tela nesse ponto.

### Apresentação de objetos e interação

* Melhorado o suporte para a maioría dos controles comúns de vista em árvore. O NVDA anuncia agora quantos elementos estão no ramo quando este é expandido. também anuncia o nível quando se move nos ramos e fora deles. E, anuncia a posição do elemento atual e o número de elementos, de acordo com o ramo atual, não toda a árvore.
* Melhora no que é anunciado quando o foco muda conforme você se move por aplicações ou pelo sistema Operacional. Agora em lugar de ouvir apenas o controle no qual se posiciona, é ouvida informação interna acerca de qualquer controle sobre o qual este está posicionado. Por exemplo se ao se mover com Tab para um botão dentro de um grupo, o grupo também será anunciado.
* O NVDA agora tenta falar a mensagem interior de muitas caixas de diálogo conforme apareçam. Isto é perfeito na maior parte das ocasiões, ainda que hája muitos diálogos onde não funciona tão bem como deve ser.
* Adicionada uma caixa de seleção anunciar descrições do objeto ao Diálogo de Opções de Apresentação de Objetos. Os usuários avançados poderão em algumas ocasiões desmarcar isto para parar o anúncio do NVDA de várias descrições extras em controles em particular, como em aplicações Java.
* O NVDA anuncia automaticamente texto selecionado em controles de edição quando o foco se move para eles. Caso não haja nenhum texto selecionado, então anunciará apenas a linha atual como normalmente.
* O NVDA agora é muito mais cuidadoso quando reproduz bipes para indicar Alterações nas barras de progresso em aplicações. Já não o faz descontroladamente em aplicações de Eclipse como Lotus Notes/Symphony, e Accessibility Probe.

### Interface do usuário

* Removida a janela de interface do NVDA e substituida por um menu simples  do NVDA popup.
* O diálogo de Opções de Interface do NVDA é agora chamado Opções Gerais. Também contén uma opção extra: uma caixa de combinação que ajusta o nivel do log, para que as mensagens possam ir para o arquivo de log do NVDA. Tenha em conta que o arquivo de log do NVDA é agora chamado nvda.log não debug.log.
* Removida a caixa de seleção Anunciar nomes de grupos de objetos do diálogo Opções de Apresentação de Objetos, o anúncio de nomes de objetos é agora controlado diferentemente.

## 0.5

* O NVDA ten agora um sintetizador integrado chammado eSpeak, desenvolvido por Jonathan Duddington. É muito ágil e rápido, e ten suporte para muitos idiomas diferentes. Os sintetizadores Sapi todavía podem ser usados, mas o eSpeak será utilizado por padrão.
 * O eSpeak não depende de nenhum software especial para ser instalado, pelo que pode ser utilizado com o NVDA em qualquer computador, nun dispositivo USB ou qualquer outro.
 * Para mais informações sobre o eSpeak, ou para encontrar outras versões, visite https://espeak.sourceforge.net/.
* Correção da falha onde era anunciado o caractere incorreto quando se pressionava Delete em painéis editáveis do Internet Explorer / Outlook Express.
* adicionado suporte para mais campos de edição no Skype.
* Os buffers virtuais agora só são carregados quando o foco está sobre a janela que necessita ser carregada. Isto resolve alguns problemas onde o painel anterior era ativado no Outlook Express.
* Adicionados argumentos de linha de comando ao NVDA:
 * -m, --minimal: não reproduz os sons de início/saír e não mostra a interface ao executar se foi configurada para isso.
 * -q, --quit: abandona qualquer outra instância já em execução do NVDA e logo sae
 * -s, --stderr-file nomearquivo: especifica onde o NVDA deve colocar os erros e exceções 
 * -d, --debug-file nomearquivo: especifica onde o NVDA deve colocar  as mensagens de depuração 
 * -c, --config-file: especifica um arquivo de configuração alternativo  
 * -h, -help: mostra uma mensagem de ajuda listando os argumentos de linha de comando
* Corrigida uma falha onde os sinais de pontuação não eram traduzidos ao idioma apropriado, ao utilizar outro idioma diferente do inglês, e quando falar caracteres digitados estava ativado.
* Adicionados arquivos do idioma eslovaco graças a Peter Vagner.
* Adicionado o diálogo de Opções do buffer virtual e um diálogo de opções de formatação de documentos, por Peter Vagner.
* Adicionada tradução para o francês graças a Michel Such.
* Adicionado um script para ativar e desativar o beep das barras de progresso (insert+u). Colaboração de Peter Vagner.
* Foi possibilitado que mais mensagens no NVDA sejam traduzíveis para outros idiomas. isto inclui descrições de scripts quando se está  na ajuda de teclado.
* Adicionado um diálogo de procura aos buffers virtuais (internet Explorer e Firefox). Ao pressionar control+f numa página abre um diálogo  no qual você pode digitar algum texto a localizar. pressionando enter depois procurará este texto e colocará o cursor do buffer virtual sobre esta linha. Pressionando f3 também procurará a seguinte ocorrência do texto.
* Quando falar caracteres digitados estiver ativado, mais caracteres devem ser falados agora. Tecnicamente, agora os caracteres ascii desde o 32 ao 255 podem ser anunciados.
* Renomeados alguns tipos de controles para uma melhor legibilidade. O Texto editável é agora edição, outline é agora árvore e botão pressionável é agora botão.
* Quando se navega ao longo dos elementos de uma lista, ou elementos de árvore numa árvore, o tipo de controle (elemento de lista, elemento de árvore) já não é falado, para uma navegação rápida.
* Popup (para indicar que um menu ten um submenú) é agora falado como submenú.
* Quando alguns idiomas utilizam control e alt (ou altGR) para introduzir um caractere especial, o NVDA falará agora estes caracteres quando falar caracteres digitados estiver ativado.
* Resolvidos alguns problemas com a exploração em controles de texto estático.
* Adicionada tradução para o Chinês Tradicional, graças a Coscell Kao.
* Reestruturada uma parte importante do código do NVDA, que agora deve corrigir  muitas falhas com a interface do usuário do NVDA (incluindo opções de diálogos).
* Adicionado suporte ao Sapi4 para o NVDA. Atualmente existem dois drivers sapi4, um baseado no código escrito pela Serotek Corporation, e outro utilizando a interface activeVoice.ativeVoice com. Ambos drivers têm problemas, veja como funciona melhor para você.
* Agora quando se trata de executar uma nova cópia do NVDA enquanto uma anterior já está sendo executada a antiga cópia encerrará. Isto resolve um problema maior onde ao executar múltiplas cópias do NVDA o sistema ficava inutilizável.
* Renomeado o título da interface do usuário do NVDA de Interface do NVDA para NVDA. 
* Corrigida uma falha no Outlook Express onde ao pressionar Backspace  no início de uma mensagem edit´ável causava um erro.
* Adicionado um parche de Rui Batista que proporciona um comando para anunciar o atual estado da bateria em computadores portáteis (insert+shift+b).
* Adicionado um driver de sintetizador chamado Silence. Este é um driver de sintetizador que não fala nada, permitindo ao NVDA permanecer completamente silencioso todo o tempo. Eventualmente isto pode ser utilizado junto com suporte braille, caso o tenhamos.
* Adicionada opção capitalPitchChange para sintetizadores graças a J.J. Meddaugh
* Dicionado parche de J.J. Meddaugh que faz com que o script alternar anúncio de objetos sob o mouse seja mais parecido com outros scripts alternáveis (dizendo ativado/desativado em lugar de alternando  todo o estado).
* Adicionada tradução para o espanhol (es) Colaboração de Juan C. Buño.
* Adicionado arquivo do idioma Húngaro por Tamas Gczy.
* Adicionado arquivo do idioma português por Rui Batista.
* A alteração de voz no Diálogo de Opções de Voz agora ajusta os controles de velocidade, ton e volume aos novos de acordo com o sintetizador, em lugar de forçar o sintetizador a ser ajustado aos valores anteriores. Isto resolve problemas de quando um sintetizador como eloquence ou viavoice pareciam falar a uma velocidade muito mais rápida que todos os outros sintetizadores.
* Corrigida uma falha onde o sintetizador de voz parava e o NVDA travava completamente, quando se estaba numa janela de console do Dos.
* Caso haja suporte para um idioma em particular, o NVDA agora pode mostrar automaticamente súa interface e falar suas mensagens  no idioma no qual o Windows esteja configurado. Um idioma particular pode aínda ser escolhido manualmente desde o diálogo de Opções de Interface do usuário.
* Adicionado o script 'toggleReportDynamicContentChanges' (insert+5). Isto alterna se novos textos, ou outras Alterações dinâmicas devem ser anunciados automaticamente. Até aquí isto só funcionava em janelas de console do Dos.
* Adicionado o script 'toggleCaretMovesReviewCursor' (insert+6). Isto lhe permite escolher se o cursor de exploração deve ser reposicionado automaticamente quando o cursor do sistema se move. Recurso útil em janelas de console do Dos quando se trata de ler informação caso a tela esteja sendo atualizada.
* Adicionado o script 'toggleFocusMovesNavigatorObject' (insert+7). Isto permite alternar se o navegador de objetos é posicionado sobre o objeto em foco quando este muda.
* Adicionada documentação traduzida para vários idiomas. Até aqui há Francês, Espanhol e Finlandês.
* Removida a documentação de desenvolvedores da distribuição binária do NVDA, agora esta se encontra apenas na versão das fontes.
* Corrigida uma possível falha no windows Live Messenger e MSN Messenger onde ao navegar para cima e para baixo pela lista de contatos causava erros.
* Novas mensagens são agora anunciadas automaticamente quando se está numa conversação utilizando Windows Live Messenger. (Funciona apenas para versões em Inglês até agora)
* A janela de históricos numa conversação no Windows Live Messenger agora pode ser lida utilizando as setas. (Recurso disponível apenas para versões em Inglês até o momento) 
* adicionado o comando 'passNextKeyThrough' (insert+f2). Pressione esta tecla e então a próxima tecla pressionada será passada diretamente para o Windows. Isto é útil se você precisa pressionar uma tecla numa aplicação mas o NVDA a utiliza para algo.
* O NVDA já não silencia por mais de um minuto ao habrir documentos muito grandes no MS Word.
* Corrigida uma falha de quando se saía de uma tabela no MS Word, e logo se voltava a ela, fazia com que os números da atual linha/coluna não fossem falados caso voltasse exatamente à mesma célula.
* Quando o NVDA for iniciado com um sintetizador que não existe ou não esteja funcionando, o sintetizador sapi5 tratará de ser carregado em seu lugar. Caso sapi5 não funcione, então a voz será ajustada a silence.
* Os scripts de Aumentar e Diminuir a velocidade já não podem tomar a velocidade acima de 100 ou abaixo de 0.
* Caso ocorra um erro com um idioma escolhido no diálogo Opções de Interface do usuário, uma caixa de mensagem alertará ao usuário sobre este fato.
* O NVDA agora pergunta se deve salvar suas configurações e reiniciá-lo quando o usuário altera seu idioma através do Diálogo de Opções da Interface. Para que o novo idioma seja carregado, a configuração tem de ser salva e o NVDA reiniciado.
* Quando um sintetizador não pode ser carregado ao ser escolhido a partir do Diálogo de Sintetizadores, uma caixa de diálogo agora avisa ao usuário desse fato.
* Ao carregar um sintetizador pela primeira vez, o NVDA deixa que ele escolha os parâmetros mais adequados de voz, velocidade e tom, em lugar de forçá-lo a usar os padrões que este supõe estar adequados. Isso resolve um problema com os sintetizadores  Eloquence e Viavoice sapi4 que iniciavam a falar de forma excessivamente rápida para uma primeira vez.
35230


