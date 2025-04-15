# NVDA 변경 이력

## 2025.1

### 중요 참고 사항

### 새로운 기능

* PDF 내 수학식 지원.
이것은 최신 버전의 TeX/LaTeX에서 생성된 일부 파일과 같은 MathML과 관련된 공식에서 작동합니다.
현재 이 기능은 Foxit Reader & Foxit Editor에서만 지원됩니다. (#9288, @NSoiffer)
* NVDA 외에 다른 애플리케이션의 볼륨을 조정하는 명령어가 추가되었습니다.
이 기능을 사용하려면, 오디오 설정에서 "NVDA가 다른 응용프로그램 음량을 제어하도록 허용"을 활성화해야 합니다. (#16052, @mltony, @codeofdusk)
  * `NVDA+alt+pageUp`: NVDA를 제외한 모든 응용프로그램의 음량을 키웁니다.
  * `NVDA+alt+pageDown`: NVDA를 제외한 모든 응용프로그램의 음량을 줄입니다.
  * `NVDA+alt+delete`: NVDA를 제외한 모든 응용프로그램을 음소거합니다.
* Microsoft PowerPiont에서 텍스트 상자를 편집할 때 `alt+upArrow와`alt+downArrow` 키를 통해 문장 단위로 이동할 수 있습니다. (#17015, @LeonarddeR)
* Mozilla Firefox에서 텍스트 조각이 포함된 URL을 방문하면 NVDA가 강조 표시된 텍스트를 보고합니다. (#16910, @jcsteh)
* 이제 NVDA는 대상이 현재 페이지를 가리키는 링크를 알립니다. (#141, @LeonarddeR, @nvdaes)
* 추가 기능 스토어에서 추가 기능 설치하는 도중에 설치를 취소할 수 있는 동작이 추가됩니다. (#15578, @hwf1324)
* 추가 기능 스토어에서 추가 기능 설치에 실패했을 때 재시도할 수 있는 동작이 추가됩니다. (#17090, @hwf1324)
* 이제 NVDA 업데이트와 추가 기능 스토어에 사용할 미러 URL을 지정할 수 있습니다. (#14974, #17151)
* 추가 기능 스토어의 추가 기능 목록을 게시 날짜를 기준으로 오름차순과 내림차순으로 정렬할 수 있습니다. (#15277, #16681, @nvdaes)
* LibreOffice Writer에서 키보드 단축키를 사용하여 글꼴 크기를 줄이거나 늘릴 때, NVDA는 새로운 글꼴 크기를 알립니다. (#6915, @michaelweghorn)
* LibreOffice Writer 25.2 이상에서 해당 키보드 단축키를 사용하여 "본문" 또는 제목 단락 스타일을 적용할 때, NVDA는 새로운 단락 스타일을 알립니다. (#6915, @michaelweghorn)
* LibreOffice Writer에서 해당 키보드 단축키를 사용하여 이중 밑줄 서식을 전환하면 NVDA가 새 상태를 알립니다 ("이중 밑줄 켬"/"이중 밑줄 끔"). (#6915, @michaelweghorn)
* Microsoft Speech API version 5 (SAPI5)와 Microsoft Speech Platform 음성에서 자동 언어 전환을 지원합니다. (#17146, @gexgd0419)
* 이제 NVDA에서 점자 탐색 키로 탐색할 때 현재 줄이나 단락을 말하도록 구성할 수 있습니다. (#17053, @nvdaes)
* Microsoft Word에서 이제 Word 명령(`f8` or `shift+f8`)을 사용하여 선택을 확장하거나 줄일 때 선택 업데이트가 보고됩니다. (#3293, @CyrilleB79)

### 변경 사항

* 링크 대상, 문자 형식 정보 및 말하기 알림 선택 대화 상자에는 이제 사용자 편의를 위해 "닫기" 및 "복사" 버튼이 포함되어 있습니다.
 (#17018, @XLTechie)
* 이제 종료 대화 상자를 통해 추가 기능이 비활성화된 NVDA와 디버그 로깅이 동시에 활성화된 NVDA를 재시작할 수 있습니다. (#11538, @CyrilleB79)
* 유니코드 정규화는 이제 음성 출력에 대해 기본적으로 활성화되어 있습니다. (#17017, @LeonarddeR).
  * NVDA 설정 대화 상자의 음성 카테고리에서 이 기능을 여전히 비활성화할 수 있습니다.
* COM registration 수정 도구의 변경 사항:(#12355, @XLTechie)
  * 이제 경고 대신 사용자 친화적인 목적 설명으로 시작합니다. (#12351)
  * 이제 초기 창을 `escape` 또는 `alt+f4` 키로 종료할 수 있습니다. (#10799)
  * 이제 COM registrations을 다시 등록 시도하는 동안 드물게 Windows 오류가 발생할 경우 오류를 포함한 메시지가 사용자에게 표시됩니다.
* Word와 Outlook에서는 더 많은 글꼴 형식 단축키의 결과를 보고합니다. (#10271, @CyrilleB79)
* 기본 입출력 점자 표는 이제 NVDA 언어를 기반으로 결정될 수 있습니다. (#17306, #16390, #290, @nvdaes)
* Microsoft Word에서는 "초점 객체 알림" 명령을 사용할 때 이해당 정보가 제공되고 객체 설명을 알릴 수 있으면 문서 레이아웃을 알립니다. (#15088, @nvdaes)
* NVDA는 현재 설치된 복사본에 호환되지 않는 추가 기능 API를 가진 버전으로 업데이트할 때만 추가기능 비호환성에 관해 경고합니다. (#17071)
* 리뷰 커서를 선택한 텍스트의 첫 번째 문자와 마지막 문자로 이동하는 명령어가 추가되었으며, 각각 `NVDA+alt+home`과 `NVDA+alt+end`에 할당되었습니다. (#17299, @nvdaes)
* 컴포넌트 업데이트:
  * LibLouis 점역기가 [3.32.0](https://github.com/liblouis/liblouis/releases/tag/v3.32.0) 버전으로 업데이트되었습니다. (#17469, @LeonarddeR)
  * CLDR이 46.0 버전으로 업데이트되었습니다. (#17484, @OzancanKaratas)

### 버그 수정내역

* 일부 웹 요소에서 수학 읽기가 수정되었습니다.
특히, role="math" 속성을 가진 span 및 기타 요소 안의 MathML에서 작동합니다. (#15058)
* Dot Inc의 Dot Pad 촉각 그래픽 기기가 멀티라인 점자 디스플레이로 네이티브 지원됩니다. (#17007)
* Microsoft PowerPoint 개선 사항:
  * 이모지와 같은 넓은 문자를 포함한 텍스트에서 캐럿 알림이 더 이상 중단되지 않습니다. (#17006, @LeonarddeR)
  * 문자 위치 알림이 이제 정확해졌습니다(`NVDA+Delete`를 눌렀을 때). (#9941, @LeonarddeR)
  * 브라우즈 모드 설정 "페이지 로드 시 자동 읽기"가 비활성화된 경우 슬라이드 쇼 시작 시 NVDA가 자동 읽기를 시작하지 않습니다. (#17488, @LeonarddeR)
* Seika Notetaker 사용 시, 공백 및 공백+점 제스처가 입력 제스처 대화 상자에 올바르게 표시됩니다. (#17047, @school510587)
* 구성 프로필:
  * 관련 구성 프로필로 '전체 읽기'를 활성화했을 때 점자 기능이 비활성화되지 않습니다. (#17163, @LeonarddeR)
  * 특정 설정값이 기본 구성값과 동일할 때 활성 구성 프로필에 강제로 저장되지 않는 문제가 수정되었습니다. (#17157, @LeonarddeR)
* Thunderbird 검색 결과 페이지에서 팝업 하위 메뉴 항목을 읽을 수 있습니다. (#4708, @thgcode)
* 점자 디스플레이가 연결되지 않은 상태에서 화면 음성 출력 점자 모드를 사용할 때 오류음이 발생하거나 로그 파일이 스팸되는 문제가 해결되었습니다. (#17092, @Emil-18)
* COM Registration 수정 도구가 실패 시 성공 메시지를 잘못 알리지 않습니다. (#12355, @XLTechie)
* Microsoft Pinyin 입력기의 이전 버전을 사용하는 Pinyin 호환 옵션을 활성화한 상태에서 LibreOffice Writer에서 입력 시 IME 팝업이 표시될 때 더 이상 오류가 발생하지 않습니다. (#17198, @michaelweghorn)
* LibreOffice에서 체크박스의 현재 상태(선택됨/선택되지 않음)가 음성뿐만 아니라 점자로도 알립니다. (#17218, @michaelweghorn)
* 철자 읽기 중 유니코드 정규화가 더욱 적절히 작동합니다:
  * 정규화된 문자를 알린 후, 이후 문자를 잘못 정규화된 것으로 알리지 않습니다. (#17286, @LeonarddeR)
  * 결합 문자(예: é)를 올바르게 알립니다. (#17295, @LeonarddeR)
* Microsoft Word, Outlook, Excel, PowerPoint의 이전 객체 모델에서 링크 대상 URL을 알리는 명령이 예상대로 작동합니다. (#17292, #17362, #17435, @CyrilleB79)
* Windows 11 클립보드 기록 창을 닫을 때 항목이 있어도 NVDA가 이를 알리지 않습니다. (#17308, @josephsl)
* 브라우저 메시지가 열려있는 동안 플러그인이 다시 로드되더라도 이후 초점 이동을 알리지 않는 문제가 해결되었습니다. (#17323, @CyrilleB79)
* Skype, Discord, Signal, Phone Link 등 오디오 통신 앱을 사용할 때 NVDA 음성과 소리가 줄어들지 않습니다. (#17349, @jcsteh)
* 스냅샷 변수를 가져오는 동안 오류가 발생해도 NVDA Python 콘솔이 열리지 않는 문제가 해결되었습니다. (#17391, @CyrilleB79)
* Notepad, UIA 문서, Windows 11의 Notepad++ 문서에서 마지막 줄이 비어 있는 경우 "점자 다음 줄 명령"으로 커서를 마지막 줄로 이동할 수 있습니다.
모든 문서에서 커서가 마지막 줄에 있을 때 이 명령을 사용하면 끝으로 이동합니다. (#17251, #17430, @nvdaes)
* 웹 브라우저에서 편집 가능한 텍스트 컨트롤의 텍스트 선택 변경 사항이 간헐적으로 알리지 않는 문제가 해결되었습니다. (#17501, @jcsteh)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* Note: this is an Add-on API compatibility breaking release.
Add-ons will need to be re-tested and have their manifest updated.
* Component updates:
  * Updated Ruff to 0.8.1. (#17102, #17260, #17473)
  * Updated Comtypes to 1.4.6. (#17061, @LeonarddeR)
  * Updated wxPython to 4.2.2. (#17181, @dpy013)
  * Updated SCons to 4.8.1. (#17254)
  * Updated sphinx to 8.1.2 and sphinx-rtd-theme to 3.0.1. (#17284, @josephsl)
  * Updated Robot Framework to 7.1.1. (#17329, @josephsl)
  * Updated configobj to 5.1.0 commit `8be5462`. (#17328)
  * Updated pre-commit to 4.0.1. (#17260)
  * Updated typing-extensions to 4.12.2. (#17438, @josephsl)
  * Updated licensecheck to 2024.3. (#17440, @josephsl)
  * Updated markdown to 3.7. (#17459, @josephsl)
  * Updated nh3 0.2.19. (#17465, @josephsl)
  * Updated nuitka to 2.5.4. (#17458, @josephsl)
  * Updated schedule to 1.2.2. (#17455, @josephsl)
  * Updated requests to 2.32.3. (#17456, @josephsl)
* `ui.browseableMessage` may now be called with options to present a button for copying to clipboard, and/or a button for closing the window. (#17018, @XLTechie)
* Several additions to identify link types (#16994, @LeonarddeR, @nvdaes)
  * A new `utils.urlUtils` module with different functions to determine link types
  * A new `INTERNAL_LINK` state has been added to `controlTypes.states.State`
  * A new `linkType` property has been added on `NVDAObject`.
  It queries the `treeInterceptor` by default, if any.
  * `BrowseModeTreeInterceptor` object has a new `documentUrl` property
  * `BrowseModeTreeInterceptor` object has a new `getLinkTypeInDocument` method which accepts an URL to check the link type of the object
  * A `toggleBooleanValue` helper function has been added to `globalCommands`.
  It can be used in scripts to report the result when a boolean is toggled in `config.conf`
* Removed the requirement to indent function parameter lists by two tabs from NVDA's Coding Standards, to be compatible with modern automatic linting. (#17126, @XLTechie)
* Added the [VS Code workspace configuration for NVDA](https://nvaccess.org/nvaccess/vscode-nvda) as a git submodule. (#17003)
* In the `brailleTables` module, a `getDefaultTableForCurrentLang` function has been added (#17222, @nvdaes)
* Retrieving the `labeledBy` property now works for:
  * objects in applications implementing the `labelled-by` IAccessible2 relation. (#17436, @michaelweghorn)
  * UIA elements supporting the corresponding `LabeledBy` UIA property. (#17442, @michaelweghorn)
* Added the ability to associate `wx.ComboBox` and a label `wx.StaticText` using `gui.guiHelper.associateElements`. (#17476)
* Added the following extension points (#17428, @ctoth):
  * `inputCore.decide_handleRawKey`: called on each keypress
  * `speech.extensions.post_speechPaused`: called when speech is paused or unpaused

#### API 호환성 변경사항

These are breaking API changes.
Please open a GitHub issue if your add-on has an issue with updating to the new API.

* The `addonStore.network.BASE_URL` constant has been removed.
As the Add-on Store base URL is now configurable directly within NVDA, no replacement is planned. (#17099)
* The `updateCheck.CHECK_URL` constant has been removed.
As the NVDA update check URL is now configurable directly within NVDA, no replacement is planned. (#17151)
* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA` has been removed with no public replacement. (#14047, #16820, @codeofdusk)
* `NVDAObjects.IAccessible.ia2TextMozilla.FakeEmbeddingTextInfo` has been removed. (#16768, @jcsteh)
* The following symbols in `appModules.soffice` have been renamed (#6915, @michaelweghorn):
  * `SymphonyDocument.announceToolbarButtonToggle` to `SymphonyDocument.announceFormattingGestureChange`
  * `SymphonyDocument.script_toggleTextAttribute` to `SymphonyDocument.script_changeTextFormatting`
* The `space` keyword argument for `brailleDisplayDrivers.seikantk.InputGesture` now expects an `int` rather than a `bool`. (#17047, @school510587)
* The `[upgrade]` configuration section including `[upgrade][newLaptopKeyboardLayout]` has been removed. (#17191)
* In `NVDAObjects.window.scintilla.ScintillaTextInfo`, if no text is selected, the `collapse` method is overriden to expand to line if the `end` parameter is set to `True` (#17431, @nvdaes)

#### 지원 종료 예정

* The `braille.filter_displaySize` extension point is deprecated.
Please use `braille.filter_displayDimensions` instead. (#17011)

## 2024.4.1

이번 릴리즈는 기호 발음 사전을 저장할 때 발생하는 버그를 수정하기 위한 것입니다.

### 버그 수정내역

* 기호 발음 사전이 저장되지 않던 버그가 수정되었으며 대화상자가 닫히지 않습니다. (#17344)

## 2024.4

이번 릴리즈는 Microsoft Office, 점자 및 문서 서식 기능 관련 몇 가지 개선사항이 있습니다.

Word나 Excel에서 메모/코멘트 동작을 두 번 눌러 탐색가능한 대화상자 안의 코멘트나 메모를 읽을 수 있습니다.
이제 PowerPoint에서 리뷰 커서 선택 명령을 통해 텍스트를 선택할 수 있습니다.
또한, NVDA는 Word에서 객체 모델을 사용 중에 표 행 및 열 머리글을 표시할 때 필요없는 문자를 점자로 출력하지 않습니다.

이제 NVDA에서 폰트 속성 알림 기능을 말하기와 점자, 각각 분리하여 설정할 수 있습니다.

시간, 날짜 읽기와 같은 여러번 누르기 제스처의 시간 제한을 조절하는 새로운 설정이 추가되었습니다.

이제 NVDA가 점자로 텍스트 형식을 표시하는 방식을 구성하고, 문단의 시작을 점자로 표시하도록 NVDA를 설정할 수 있습니다.
이제 NVDA에서 점자 커서 라우팅 동작을 수행 할 때 커서에 있는 문자를 말할 수 있습니다.
커서 라우팅 신뢰성이 개선되었으며 라우팅 PowerPoint 단축키 지원이 추가되었습니다.
이제 여러줄 점자 디스플레이 사용 시 HID 점자 출력을 통해 모든 라인이 사용됩니다.
점자 디스플레이 자동 검색 중에 NVDA를 제시작한 뒤 불안정적이던 문제가 해결되었습니다.

이제 NVDA에서 동작하는 Poedit의 최소 요구 버전은 3.5 버전입니다.

eSpeak NG가 업데이트되어 페로어 및 Xextan 언어에 대한 지원이 추가되었습니다.

Liblouis 점역기가 업데이트되며, 태국어, 단일 셀 강세 문자가 포함된 그리스어 국제 점자가 추가됩니다.

Firefox의 마우스 추적과 "요청 시" 음성 모드를 포함한 여러 가지 수정 사항도 있습니다.

### 새로운 기능

* 새로운 점자 기능:
  * 이제 NVDA가 특정 텍스트 형식 속성을 점자로 표시하는 방식을 변경할 수 있습니다.
    사용 가능한 옵션 은 다음과 같습니다.
    * Liblouis (기본값): 선택한 점자 테이블에 정의된 서식 지정 마커를 사용합니다.
    * 태그: 시작 태그와 끝 태그를 사용하여 특정 글꼴 속성의 시작과 끝을 나타냅니다. (#16864)
  * "문단 딘위로 읽기" 옵션이 활성화되어 있을 때, NVDA에서 문단의 시작을 표시하도록 설정할 수 있습니다. (#16895, @nvdaes)
  * 점자 커서 라우팅 동작을 수행할 때 NVDA는 커서에 있는 문자를 말할 수 있습니다. (#8072, @LeonarddeR)
    * 이 옵션은 기본적으로 비활성화되어 있습니다.
      점자 설정에서 "텍스트에서 커서 라우팅 사용 시 커서 아래 있는 문자 말하기" 기능을 활성화할 수 있습니다.
* Microsoft Word와 Excel의 코멘트/메모 명령을 두 번 눌러 탐색 가능한 메시지 창을 표시할 수 있습니다. (#16800, #16878, @Cary-Rowen)
* NVDA에서 이제 말하기와 점자에서 폰트 속성 알림을 별도로 설정할 수 있습니다. (#16755)
* 단축키를 여러번 누르는 동작을 수행 할 때 제한 시간을 설정할 수 있습니다. 손 동작에 어려움이 있는 사용자에게 특히 도움이 될 수 있습니다. (#11929, @CyrilleB79)

### 변경 사항

* NVDA에서 업데이트를 실행 중일 때 '-c' 또는 `--config-path`와 `--disable-addons` 명령줄 옵션이 우선됩니다. (#16937)
* 컴포넌트 업데이트:
  * Liblouis 점역기가 [3.31.0](https://github.com/liblouis/liblouis/releases/tag/v3.31.0)으로 업데이트되었습니다. (#17080, @LeonarddeR, @codeofdusk)
    * 스페인어 점자 숫자 번역이 수정되었습니다.
    * 새 점자표:
      * 태국어 1종
      * 그리스어 국제 점자 (단일 셀 강세 문자)
    * 이름이 변경된 점자표:
      * 일관성을 위해 "태국어 6점"을 "태국어 0종"으로 이름을 바꾸었습니다.
      * 기존에 있던 "그리스어 국제 점자" 표는 두 그리스어 시스템의 차이점을 명확히 하기 위해 "그리스어 국제 점자 (2셀 강세 문자)"로 이름이 변경되었습니다.
  * eSpeak NG가 1.52-dev commit `961454ff` 버전으로 업데이트되었습니다. (#16775)
    * 페로어와 Xextan 언어가 추가되었습니다.
* 이제 표준 HID 점자 드라이버로 여러줄 점자 디스플레이를 사용할 때 모든 줄의 셀이 사용됩니다. (#16993, @alexmoon)
* NVDA의 Poedit 지원의 안정성이 향상되었으며, 필요한 최소 버전의 Poedit이 이제 버전 3.5가 되었습니다. (#16889, @LeonarddeR)

### 버그 수정내역

* 점자 관련 수정사항:
  * 이제 PowerPoint에서 점자 디스플레이 라우팅 키를 사용하여 텍스트 커서를 움직일 수 있습니다. (#9101)
  * UI 자동화 없이 Microsoft Word에 접근할 때, NVDA는 더 이상 표 행 및 열 머리글을 지정하면 표 헤더에 있는 쓸모없는 문자를 더 이상 출력하지 않습니다.
  * 세이카 노트테이커 드라이버가 스페이스, 백스페이스, 스페이스/백스페이스 점자 입력 제스처를 올바르게 생성합니다. (#16642, @school510587)
  * 이제 한 줄에 하나 이상의 유니코드 변형 선택자나 분해된 문자가 포함된 경우 커서 라우팅이 훨씬 더 안정적입니다. (#10960, @mltony, @LeonarddeR)
  * NVDA는 일부 빈 편집 컨트롤에서 점자 디스플레이를 앞으로 이동할 때 더 이상 오류를 발생시키지 않습니다. (#12885)
  * NVDA는 더 이상 블루투스 점자 장치를 자동으로 스캔하는 도중 NVDA를 재시작할 때 불안정하지 않습니다. (#16933)
* 이제 Microsoft PowerPoint에서 리뷰 커서 선택 명령을 사용하여 텍스트를 선택할 수 있습니다. (#17004)
* "요청 시" 말하기 모드 상태에서 NVDA는 Outlook에서 메시지가 열리거나, 브라우저에 새 페이지가 로드되거나, PowerPoint 슬라이드쇼에 새 슬라이드를 표시할 때 더 이상 말하지 않습니다. (#16825, @CyrilleB79)
* Mozilla FireFox에서 링크 전후에 마우스를 움직일 때 이제 안정적으로 텍스트를 보고합니다. (#15990, @jcsteh)
* NVDA는 더 이상 가끔 탐색 가능한 메시지를 여는 데 실패하지 않습니다(예: 'NVDA+f'를 두 번 누르는 것). (#16806, @LeonarddeR)
* 추가 기능 업데이트가 보류 중인 동안 NVDA를 업데이트해도 추가 기능이 더 이상 제거되지 않습니다. (#16837)
* 이제 Microsoft Excel 365의 데이터 검증 드롭다운 목록과 상호 작용할 수 있습니다. (#15138)
* NVDA는 VSCode에서 큰 파일을 위아래로 화살표 키로 읽을 때 더 이상 느려지지 않습니다. (#17039)
* 브라우즈 모드, 특히 Microsoft Word와 Microsoft Outlook에서 화살표 키를 오랫동안 누른 후 NVDA가 더 이상 응답을 멈추지 않습니다. (#16812)
* 자바 응용프로그램에서 커서가 멀티라인 편집창의 두 번째 마지막 줄에 있을 때 NVDA는 더 이상 마지막 줄을 읽지 않습니다. (#17027)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* Component updates:
  * Updated py2exe to 0.13.0.2 (#16907, @dpy013)
  * Updated setuptools to 72.0 (#16907, @dpy013)
  * Updated Ruff to 0.5.6. (#16868, @LeonarddeR)
  * Updated nh3 to 0.2.18 (#17020, @dpy013)
* Added a `.editorconfig` file to NVDA's repository in order for several IDEs to pick up basic NVDA code style rules by default. (#16795, @LeonarddeR)
* Added support for custom speech symbol dictionaries. (#16739, #16823, @LeonarddeR)
  * Dictionaries can be provided in locale specific folders in an add-on package, e.g. `locale\en`.
  * Dictionary metadata can be added to an optional `symbolDictionaries` section in the add-on manifest.
  * Please consult the [Custom speech symbol dictionaries section in the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSymbolDictionaries) for more details.
* It is now possible to redirect objects retrieved from on-screen coordinates, by using the `NVDAObject.objectFromPointRedirect` method. (#16788, @Emil-18)
* Running SCons with the parameter `--all-cores` will automatically pick the maximum number of available CPU cores. (#16943, #16868, @LeonarddeR)
* Developer info now includes information on app architecture (such as AMD64) for the navigator object. (#16488, @josephsl)

#### 지원 종료 예정

* The `bool` configuration key `[documentFormatting][reportFontAttributes]` is deprecated for removal in 2025.1, instead use `[fontAttributeReporting]`. (#16748)
  * The new key has an `int` value matching an `OutputMode` `enum` with options for speech, braille, speech and braille and off.
  * API consumers can use the `bool` value as previously, or check the `OutputMode` if handling speech or braille specifically.
  * These keys are currently synchronized until 2025.1.
* `NVDAObjects.UIA.InaccurateTextChangeEventEmittingEditableText` is deprecated with no replacement. (#16817, @LeonarddeR)

## 2024.3.1

This is a patch release to fix a bug with the automatic add-on update notification.

### 버그 수정내역

* When automatically checking for add-on updates, NVDA no longer freezes on poor connections. (#17036)

## 2024.3

이제 NVDA를 시작할 때 추가 기능 스토어에서 업데이트할 수 있는 추가 기능을 알립니다.

이제 유니코드 정규화를 음성 및 점자 출력에 적용할 수 있는 옵션이 있습니다.
이 기능은 특정 음성 합성기나 점자 테이블에서 알 수 없는 문자와 호환 가능한 대체 문자를 읽을 때 유용합니다. 예를 들어, 소셜 미디어에서 흔히 사용되는 굵은 글씨와 이탤릭체 문자가 해당됩니다. 
또한 Microsoft Word의 수식 편집기에서 수식을 읽을 수 있게 합니다.

Help Tech Activator Pro 점자 디스플레이가 이제 지원됩니다.

마우스 휠을 수직 및 수평으로 스크롤하는 할당 가능한 명령이 추가되었습니다.

여러 가지 버그 수정이 이루어졌으며, 특히 Windows 11 이모지 패널과 클립보드 기록에 대한 수정이 포함됩니다.
웹 브라우저의 경우, 오류 메시지 보고, 그림, 캡션, 표 레이블, 체크박스/라디오 버튼 메뉴 항목에 대한 수정이 있습니다.

LibLouis가 업데이트되어 키릴 세르비아어, 이디시어, 여러 고대 언어, 터키어, 국제 음성 기호를 위한 새로운 점자 테이블이 추가되었습니다.
eSpeak가 업데이트되어 카라칼파크어 지원이 추가되었습니다.
유니코드 CLDR도 업데이트되었습니다.

### 새로운 기능

* 새로운 키 명령:
  * 동적 콘텐츠가 있는 웹 페이지 및 앱에서 내비게이션을 향상시키기 위해 마우스 휠을 수직 및 수평으로 스크롤하는 미지정 명령이 추가되었습니다. (Dism++와 같은 앱 포함) (#16462, @Cary-Rowen)
* 음성 및 점자 출력에 유니코드 정규화를 지원하도록 추가했습니다. (#11570, #16466 @LeonarddeR)
  * 특정 음성 합성기나 점자 테이블에서 알 수 없는 문자와 호환 가능한 대체 문자를 읽을 때 유용합니다. 예를 들어 소셜 미디어에서 흔히 사용되는 굵은 글씨와 이탤릭체 문자와 같습니다.
  * 또한 Microsoft Word의 수식 편집기에서 수식을 읽을 수 있게 합니다. (#4631)
  * NVDA 설정 대화 상자의 음성 및 점자 설정 카테고리에서 이 기능을 활성화할 수 있습니다.
* 기본적으로 NVDA 시작 후, 사용 가능한 추가 기능 업데이트가 있으면 알림을 받게 됩니다. (#15035)
  * 이 기능은 "추가 기능 스토어" 설정 카테고리에서 비활성화할 수 있습니다.
  * NVDA는 매일 추가 기능 업데이트를 확인합니다.
  * 동일한 채널 내의 업데이트만 확인됩니다 (예: 설치된 베타 추가 기능은 베타 채널의 업데이트만 알림).
* Help Tech Activator Pro 디스플레이 지원이 추가되었습니다. (#16668)

### 변경사항

* 구성 요소 업데이트:
  * eSpeak NG가 1.52-dev 커밋 `54ee11a79`로 업데이트되었습니다. (#16495)
    * 새로운 언어 카라칼파크어 추가.
  * Unicode CLDR이 45.0 버전으로 업데이트되었습니다. (#16507, @OzancanKaratas)
  * fast_diff_match_patch(터미널 및 기타 동적 콘텐츠의 변경 사항을 감지하는 데 사용)을 2.1.0 버전으로 업데이트했습니다. (#16508, @codeofdusk)
  * LibLouis 점자 번역기가 [3.30.0](https://github.com/liblouis/liblouis/releases/tag/v3.30.0) 버전으로 업데이트되었습니다. (#16652, @codeofdusk)
    * 새로운 점자 테이블:
      * 키릴 세르비아어.
      * 이디시어.
      * 여러 고대 언어: 고전 성경 히브리어, 아카드어, 시리아어, 우가리트어 및 음역된 쐐기문자 텍스트.
      * 터키어 2단계. (#16735)
      * 국제 음성 기호. (#16773)
  * NSIS가 3.10으로 업데이트되었습니다. (#16674, @dpy013)
  * markdown이 3.6으로 업데이트되었습니다. (#16725, @dpy013)
  * nh3이 0.2.17로 업데이트되었습니다. (#16725, @dpy013)
* 기본 점자 입력 테이블이 기본 출력 테이블과 동일하게 통합 영어 점자 코드 1단계로 설정되었습니다. (#9863, @JulienCochuyt, @LeonarddeR)
* NVDA는 접근 가능한 자식이 없는 경우에도 레이블이나 설명이 있는 그림을 보고합니다. (#14514)
* 브라우즈 모드에서 줄 단위로 읽을 때 긴 그림이나 표 캡션의 각 줄에 "캡션"이 더 이상 보고되지 않습니다. (#14874)
* Python 콘솔에서 입력 기록을 이동할 때 마지막으로 실행되지 않은 명령이 더 이상 손실되지 않습니다. (#16653, @CyrilleB79)
* NVDA 사용 통계 수집 옵션의 일부로 고유한 익명 ID가 전송됩니다. (#16266)
* 기본적으로 포터블 복사본을 만들 때 새 폴더가 생성됩니다.
비어 있지 않은 디렉토리에 쓰기를 시도하면 경고 메시지가 표시됩니다. (#16686)

### 버그 수정내역

* Windows 11 수정 사항:
  * NVDA가 클립보드 기록과 이모지 패널을 닫을 때 더 이상 멈추지 않습니다. (#16346, #16347, @josephsl)
  * IME 인터페이스를 열 때 NVDA가 다시 보이는 후보를 발표합니다. (#14023, @josephsl)
  * 이모지 패널 메뉴 항목을 탐색할 때 NVDA가 "클립보드 기록"을 두 번 발표하지 않습니다. (#16532, @josephsl)
  * 이모지 패널에서 카오모지와 기호를 검토할 때 NVDA가 음성과 점자를 중단하지 않습니다. (#16533, @josephsl)
* 웹 브라우저 수정 사항:
  * `aria-errormessage`로 참조된 오류 메시지가 이제 Google Chrome 및 Mozilla Firefox에서 보고됩니다. (#8318)
  * 존재하는 경우 NVDA는 Mozilla Firefox에서 테이블에 접근 가능한 이름을 제공하기 위해 `aria-labelledby`를 사용합니다. (#5183)
  * NVDA가 Google Chrome 및 Mozilla Firefox에서 서브 메뉴에 처음 들어갈 때 라디오 및 체크박스 메뉴 항목을 정확하게 발표합니다. (#14550)
  * 페이지에 이모지가 포함된 경우 NVDA의 브라우즈 모드 찾기 기능이 더 정확해졌습니다. (#16317, @LeonarddeR)
  * Mozilla Firefox에서 커서가 줄 끝 삽입 지점에 있을 때 NVDA가 현재 문자, 단어 및 줄을 정확하게 보고합니다. (#3156, @jcsteh)
    * 문서를 닫거나 Chrome을 종료할 때 Google Chrome이 더 이상 충돌하지 않도록 합니다. (#16893)
* NVDA는 Windows 11에서 Eclipse 및 기타 Eclipse 기반 환경에서 자동 완성 제안을 정확하게 발표합니다. (#16416, @thgcode)
* 특히 터미널 애플리케이션에서 자동 텍스트 읽기 기능의 신뢰성이 향상되었습니다. (#15850, #16027, @Danstiv)
* 구성을 공장 기본값으로 안정적으로 재설정하는 것이 다시 한 번 가능합니다. (#16755, @Emil-18)
* Microsoft Excel에서 셀의 텍스트를 편집할 때 NVDA가 선택 변경 사항을 정확하게 발표합니다. (#15843)
* Java Access Bridge를 사용하는 애플리케이션에서 NVDA는 이제 이전 줄을 반복하지 않고 마지막 빈 줄을 정확하게 읽습니다. (#9376, @dmitrii-drobotov)
* LibreOffice Writer(버전 24.8 이상)에서 텍스트 서식을 전환할 때(굵게, 이탤릭체, 밑줄, 아래첨자/위첨자, 정렬) 해당 키보드 단축키를 사용하면 NVDA가 새로운 서식 속성을 발표합니다(예: "굵게 켜짐", "굵게 꺼짐"). (#4248, @michaelweghorn)
* UI Automation을 사용하는 애플리케이션의 텍스트 상자에서 커서 키로 탐색할 때 NVDA가 더 이상 잘못된 문자, 단어 등을 보고하지 않습니다. (#16711, @jcsteh)
* Windows 10/11 계산기에 붙여넣을 때 NVDA가 붙여넣은 전체 숫자를 정확하게 보고합니다. (#16573, @TristanBurchett)
* 원격 데스크톱 세션에서 연결을 끊고 다시 연결한 후 음성이 더 이상 침묵하지 않습니다. (#16722, @jcsteh)
* Visual Studio Code에서 개체 이름에 대한 텍스트 검토 명령에 대한 지원이 추가되었습니다. (#16248, @Cary-Rowen)
* 모노 오디오 장치에서 NVDA 소리 재생이 더 이상 실패하지 않습니다. (#16770, @jcsteh)
* outlook.com / 모던 아웃룩에서 To/CC/BCC 필드를 화살표 키로 탐색할 때 NVDA가 주소를 보고합니다. (#16856)
* NVDA가 추가 기능 설치 실패를 더 원활하게 처리합니다. (#16704)

### 개발 변경사항(영문)

* NVDA는 이제 린팅을 위해 flake8 대신 Ruff를 사용합니다. (#14817)
* Visual Studio 2022 버전 17.10 이상을 사용할 때 NVDA의 빌드 시스템이 제대로 작동하도록 수정되었습니다. (#16480, @LeonarddeR)
* 고정 폭 글꼴이 로그 뷰어와 NVDA Python 콘솔에서 사용되어 수직 탐색 시 커서가 동일한 열에 남아 있습니다.
이는 특히 추적(back)에서 오류 위치 표시를 읽는 데 유용합니다. (#16321, @CyrilleB79)
* 사용자 정의 점자 테이블에 대한 지원이 추가되었습니다. (#3304, #16208, @JulienCochuyt, @LeonarddeR)
  * 추가 기능 패키지의 `brailleTables` 폴더에 테이블을 제공할 수 있습니다.
  * 테이블 메타데이터는 추가 기능 매니페스트의 선택적 `brailleTables` 섹션이나 스크래치패드 디렉토리의 brailleTables 하위 디렉토리에서 찾을 수 있는 형식의 `.ini` 파일에 추가할 수 있습니다.
  * 자세한 내용은 [개발자 가이드의 점자 번역 테이블 섹션](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#BrailleTables)을 참조하십시오.
* `gainFocus` 이벤트가 유효한 `focusRedirect` 속성을 가진 객체와 함께 큐에 있을 때, 이제 `focusRedirect` 속성이 가리키는 객체가 원래 큐에 있던 객체 대신 `eventHandler.lastQueuedFocusObject`에 의해 유지됩니다. (#15843)
* NVDA는 시작 시 실행 파일 아키텍처(x86)를 로깅합니다. (#16432, @josephsl)
* `wx.CallAfter`가 이제 올바른 `functools.wraps` 표시를 포함하도록 `monkeyPatches/wxMonkeyPatches.py`에 래핑되었습니다. (#16520, @XLTechie)
* 작업 예약을 위한 새로운 모듈 `utils.schedule`이 추가되었습니다. 이는 pip 모듈 `schedule`을 사용합니다. (#16636)
  * `scheduleThread.scheduleDailyJobAtStartUp`을 사용하여 NVDA 시작 후와 그 후 매 24시간마다 발생하는 작업을 자동으로 예약할 수 있습니다.
  작업은 충돌을 피하기 위해 지연되어 예약됩니다.
  * `scheduleThread.scheduleDailyJob` 및 `scheduleJob`을 사용하여 사용자 지정 시간에 작업을 예약할 수 있으며, 예약 충돌이 발생하면 `JobClashError`가 발생합니다.
* Edge WebView2(msedgewebview2.exe) 컨트롤을 호스팅하는 앱에 대한 앱 모듈을 생성할 수 있게 되었습니다. (#16705, @josephsl)

## 2024.2

새로운 기능인 소리 분리가 추가되었습니다.
이 기능을 통해 NVDA 소리를 한 채널(예: 왼쪽)로 분리하고 다른 모든 응용 프로그램의 소리를 다른 채널(예: 오른쪽)로 보낼 수 있습니다.

음성 엔진 설정 고리를 수정하는 새로운 명령이 추가되어 사용자가 첫 번째 또는 마지막 설정으로 이동하고 현재 설정을 더 큰 단계로 증가 또는 감소시킬 수 있습니다.
또한 새로운 빠른 탐색 명령이 추가되어 사용자가 제스처를 할당하여 단락, 세로로 정렬된 문단, 동일 스타일 텍스트, 다른 스타일 텍스트, 메뉴 항목, 전환 버튼, 진행률 막대, 피규어 및 수학 공식 간에 빠르게 이동할 수 있습니다.

여러 가지 새로운 점자 기능과 버그 수정이 많이 있습니다.
"출력 내용 표시"라는 새로운 점자 모드가 추가되었습니다.
활성화되면 점자 디스플레이에 NVDA가 말하는 내용이 정확히 표시됩니다.
BrailleEdgeS2 및 BrailleEdgeS3 디스플레이에 대한 지원도 추가되었습니다.
LibLouis가 업데이트되어 대문자가 표시된 상세한 벨라루스어 및 우크라이나어 점자 테이블, 라오스어 테이블, 그리스어 텍스트를 읽기 위한 스페인어 테이블이 추가되었습니다.

eSpeak가 업데이트되어 새로운 언어인 티그리냐가 추가되었습니다.

Thunderbird, Adobe Reader, 웹 브라우저, Nudi 및 Geekbench와 같은 응용 프로그램의 여러 사소한 버그가 수정되었습니다.

### 새로운 기능

* 새로운 단축키:
  * 이전 또는 다음 텍스트 문단을 탐색하는 새로운 빠른 탐색 키 `p` (#15998, @mltony)
  * 할당되지 않은 새로운 빠른탐색 단축키:
    * 피규어 (#10826)
    * 세로로 정렬된 문단 탐색 (#15999, @mltony)
    * 메뉴 항목 (#16001, @mltony)
    * 전환 버튼 (#16001, @mltony)
    * 진행률 막대 (#16001, @mltony)
    * 수학 공식 (#16001, @mltony)
    * 동일 스타일 텍스트 (#16000, @mltony)
    * 다른 스타일 텍스트 (#16000, @mltony)
  * 음성 엔진 설정 고리를 통해 맨 첫번째, 마지막, 앞으로 및 뒤로 탐색하는 명령. (#13768, #16095, @rmcpantoja)
    * 음성 엔진 설정 고리에서 첫 번째/마지막 설정을 설정하는 것은 할당된 제스처가 없습니다. (#13768)
    * 더 큰 단계에서 음성 엔진 설정 고리의 현재 설정을 감소 및 증가 (#13768):
      * Desktop: `NVDA+control+pageUp` 또는 `NVDA+control+pageDown`.
      * Laptop: `NVDA+control+shift+pageUp` 또는 `NVDA+control+shift+pageDown`.
  * 도형 및 캡션의 알림 여부를 전환하는 새로운 할당되지 않은 제스처를 추가합니다. (#10826, #14349)
* 점자:
  * BrailleEdgeS2와 BrailleEdgeS3 점자 디스플레이 지원 추가. (#16033, #16279, @EdKweon)
  * 점자 모드, "출력 내용 표시"가 추가되었습니다. (#15898, @Emil-18)
    * 활성화 시 점자 디스플레이는 NVDA가 말하는 것을 정확하게 보여줍니다.
    * `NVDA+alt+t`를 눌러 전환하거나 점자 설정 대화상자에서 전환할 수 있습니다.
* 소리 분리: (#12985, @mltony)
  * NVDA 사운드를 하나의 채널(예: 왼쪽)로 분할하는 반면 다른 모든 응용 프로그램의 사운드는 다른 채널(예: 오른쪽)로 향합니다.
  * `NVDA+alt+s`로 전환할 수 있습니다.
* 이제 행 및 열 헤더 알림이 편집 가능한 HTML 요소에서 지원됩니다. (#14113)
* 문서 서식 설정에서 도형 및 캡션의 보고를 비활성 설정하는 옵션을 추가했습니다. (#10826, #14349)
* Windows 11에서, NVDA는 전화번호와 같은 데이터를 클립보드(Windows 11 2022 업데이트 이상)에 복사할 때 음성 입력에서 나오는 경고와 제안된 동작을 발표합니다. (#16009, @josephsl)
* NVDA는 음성이 멈춘 후에도 오디오 장치를 계속 활성 상태로 유지하여, 블루투스 헤드폰과 같은 일부 오디오 장치에서 다음 음성의 시작 부분이 잘리는 것을 방지합니다. (#14386, @jcsteh, @mltony)
* 이제 HP 보안 브라우저를 지원합니다. (#16377)

### 변경사항

* 추가 기능 스토어:
  * 이제 추가 기능에 대한 최소 버전과 마지막으로 테스트된 NVDA 버전이 "기타 세부 정보" 영역에 표시됩니다. (#15776, @Nael-Sayegh)
  * 커뮤니티 리뷰 작업을 사용할 수 있으며 리뷰 웹페이지는 매장의 모든 탭에 있는 세부 정보 패널에 표시됩니다.  (#16179, @nvdaes)
* 컴포넌트 추가:
  * Liblouis 점역기가 [3.29.0](https://github.com/liblouis/liblouis/releases/tag/v3.29.0)로 업데이트되었습니다. (#16259, @codeofdusk)
    * 상세(대문자 표시) 벨라루스어와 우크라이나어 점자표가 새로 추가되었습니다.
    * 그리스어 텍스트를 읽을 수 있는 새로운 스페인어 점자표가 새로 추가되었습니다.
    * 라오어 1종 점자가 추가되었습니다. (#16470)
  * eSpeak가 1.52-dev 커밋 `cb62d93fd7` 버전으로 업데이트되었습니다. (#15913)
    * 티그리냐어가 새로 추가되었습니다.
* 프랑스어 점자표의 문자와 충돌을 피하기 위해 점자 감지 장치에 대한 여러 단축키가 변경되었습니다. (#15306)
  * `alt+leftArrow`가 `dot2+dot7+space`로 변경되었습니다.
  * `alt+rightArrow`가 `dot5+dot7+space`로 변경되었습니다.
  * `alt+upArrow`가 `dot2+dot3+dot7+space`로 변경되었습니다.
  * `alt+downArrow`가 `dot5+dot6+dot7+space`로 변경되었습니다.
* 목차에서 일반적으로 사용되는 여백 점형은 낮은 문장 부호 수준에서는 더 이상 보고되지 않습니다. (#15845, @CyrilleB79)

### 버그 수정내역

* Windows 11 수정 사항:
  * NVDA가 하드웨어 키보드 입력 제안을 다시 발표합니다. (#16283, @josephsl)
  * 버전 24H2 (2024 업데이트 및 Windows Server 2025)에서 마우스 및 터치 상호 작용을 통해 빠른 설정을 사용할 수 있습니다. (#16348, @josephsl)
* 추가 기능 스토어:
  * ctrl+tab을 누르면 초점이 새 현재 탭 제목으로 제대로 이동합니다. (#14986, @ABuffEr)
  * 캐시 파일이 올바르지 않은 경우 NVDA가 다시 시작되지 않습니다. (#16362, @nvdaes)
* UIA를 사용하는 Chromium 기반 브라우저에 대한 수정 사항:
  * NVDA를 멈추게 하는 버그가 수정되었습니다. (#16393, #16394)
  * Gmail 로그인 필드에서 Backspace 키가 이제 올바르게 작동합니다. (#16395)
* NVDA의 "다른 응용 프로그램의 키 처리" 설정이 활성화된 상태에서 Nudi 6.1을 사용할 때 백스페이스가 올바르게 작동합니다. (#15822, @jcsteh)
* "마우스 이동 시 경고음으로 좌표 알림"이 활성화된 상태에서 응용 프로그램이 대기 모드일 때 오디오 좌표가 재생되는 버그가 수정되었습니다. (#8059, @hwf1324)
* Adobe Reader에서 NVDA가 PDF의 수식에 설정된 대체 텍스트를 무시하지 않습니다. (#12715)
* NVDA가 Geekbench 내 리본 및 옵션을 읽지 못하는 버그가 수정되었습니다. (#16251, @mzanm)
* 구성 저장 시 모든 프로필을 저장하지 못할 수 있는 드문 경우가 수정되었습니다. (#16343, @CyrilleB79)
* Firefox 및 Chromium 기반 브라우저에서 편집 가능한 콘텐츠 내에 있는 목록(ul / ol) 내에 위치한 상태에서 Enter 키를 누를 때 NVDA가 올바르게 포커스 모드로 전환됩니다. (#16325)
* Thunderbird 메시지 목록에서 표시할 열을 선택할 때 열 상태 변경이 자동으로 보고됩니다. (#16323)
* `-h`/`--help` 명령줄 전환 기능이 다시 적절하게 동작합니다. (#16522, @XLTechie)
* NVDA의 Poedit 번역 소프트웨어 버전 3.4 이상 지원은 1개 이상의 복수형 언어(예: 중국어, 폴란드어)를 번역할 때 올바르게 작동합니다. (#16318)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* Instantiating `winVersion.WinVersion` objects with unknown Windows versions above 10.0.22000 such as 10.0.25398 returns "Windows 11 unknown" instead of "Windows 10 unknown" for release name. (#15992, @josephsl)
* Make the AppVeyor build process easier for NVDA forks, by adding configurable variables in appveyor.yml to disable or modify NV Access specific portions of the build scripts. (#16216, @XLTechie)
* Added a how-to document, explaining the process of building NVDA forks on AppVeyor. (#16293, @XLTechie)

## 2024.1

"요청 시" 말하기 모드(구, 음성 출력 모드)가 추가되었습니다. 
"요청 시" 말하기 모드를 사용하면 NVDA가 자동으로 내용을 말하지 않습니다(예: 마우스 커서를 움직임) 그러나 무언가를 보고하는 것이 목적인 단축키를 사용할 때 여전히 말합니다(예: 창 제목 말하기).
이제 NVDA 설정 내 "말하기" 카테고리에서 (`NVDA+s`) 단축키로 말하기 모드를 순환 설정할 때 원하지 않는 말하기 모드 항목을 제외할 수 있습니다.

새로운 네이티브 선택 모드(`NVDA+shift+f10`)를 Mozilla Firefox 브라우저 내에서 NVDA 브라우즈 모드로 사용할 수 있습니다.
이 기능을 켜면 브라우즈 모드에서 텍스트를 선택하면 Firefox 고유의 네이티브 선택(마우스 드래그를 통한 선택)도 함께 동작합니다.
`control+c` 단축키를 통한 텍스트 복사가 Firefox에 바로 전달됩니다, 따라서 NVDA의 일반 텍스트 형식이 아닌 리치 콘텐츠(서식 있는 텍스트)를 복사합니다.

이제 추가 기능 스토어에서 다중 선택을 통한 대량 작업을 지원합니다(예: 추가기능 설치, 활성화 등).
선택한 추가 기능에 대한 리뷰 웹 페이지를 여는 새로운 작업이 있습니다.

오디오 출력 장치와 오디오 더킹 모드 옵션이 "음성 엔진 선택" 대화상자에서 삭제되었습니다.
이 두 옵션은 `NVDA+control+u`를 통해 열 수 있는 음향 설정 패널에서 찾을 수 있습니다.

eSpeak-NG, Liblouis 점역기, 유니코드 CLDR가 업데이트되었습니다.
새로운 점자표, 태국어, 필리핀어, 루마니아어를 사용할 수 있습니다.

특히 추가 기능 스토어, 점자, LibreOffice, Microsoft Office의 경우 수많은 버그가 수정되었습니다.

### 중요 참고사항

* 이 릴리즈는 기존 추가 기능과 호환되지 않습니다.
* Windows 7과 Windows 8를 이제 지원하지 않습니다.
이제 Windows 8.1이 최소 Windows 버전입니다.

### 새로운 기능

* 추가 기능 스토어:
  * 추가 기능 스토어가 여러 항목 선택을 통한 대량 작업을 지원합니다(e.g. 설치, 추가 기능 활성화) (#15350, #15623, @CyrilleB79)
  * 선택된 추가 기능의 피드백을 제공하는 전용 웹페이지를 여는 새로운 동작이 추가되었습니다. (#15576, @nvdaes)
* 저전력 블루투스 HID 점자 디스플레이 지원이 추가되었습니다. (#15470)
* 새로운 네이티브 선택 모드(`NVDA+shift+f10`)를 Mozilla Firefox 브라우저 내에서 
NVDA 브라우즈 모드로 사용할 수 있습니다.
이 기능을 켜면 브라우즈 모드에서 텍스트를 선택하면 Firefox 고유의 네이티브 선택(마우스 드래그를 통한 선택)도 함께 동작합니다. `control+c` 단축키를 통한 텍스트 복사가 Firefox에 바로 전달됩니다, 따라서 NVDA의 일반 텍스트 형식이 아닌 리치 콘텐츠(서식 있는 텍스트)를 복사합니다.
그러나 Firefox가 실제 복사 동작을 처리하기 때문에 NVDA는 이 모드에서 "클립보드로 복사" 메시지를 알리지 않습니다. (#15830)
* NVDA 브라우즈 모드가 켜진 상태로 Microsoft Word에서 텍스트를 복사할 때 서식또한 복사됩니다.
이것의 부작용으로 응용 프로그램이 실제 복사 동작을 처리하기 때문에 Microsoft Word/Outlook 찾아보기 모드에서 'control+c'를 누르면 NVDA가 더 이상 "클립보드로 복사" 메시지를 알리지 않습니다. (#16129)
* 새로운 말하기 모드(음성 출력 모드) "요청 시"가 추가되었습니다.
말하기 모드가 "요청 시"로 설정되면 NVDA는 자동으로 내용을 말하지 않습니다(예: 마우스 커서를 움직일 때) 그러나 어떤 것을 알리는 것이 목적인 단축키를 사용할 때 여전히 말합니다(예: 창 제목 말하기). (#481, @CyrilleB79)
* NVDA 설정 내 말하기 설정에서 말하기 모드 순환 설정(`NVDA+s`) 시 원하지 않는 모드를 제외하도록 설정할 수 있습니다. (#15806, @lukaszgo1)
  * NoBeepsSpeechMode 추가 기능을 사용하시는 중이라면 제거하시기 바라며, 설정에서 "비프음"과 "요청 시" 모드를 비활성화하시기 바랍니다.

### 변경사항

* NVDA가 더 이상 Windows 7와 Windows 8를 지원하지 않습니다.
최소 Windows 8.1 이상의 Windows를 사용해야 합니다. (#15544)
* 컴포넌트 업데이트:
  * Liblouis 점역기가 [3.28.0](https://github.com/liblouis/liblouis/releases/tag/v3.28.0)로 업데이트되었습니다. (#15435, #15876, @codeofdusk)
    * 태국어, 루마니아어, 필리핀어 점자표가 추가되었습니다.
  * eSpeak NG가 1.52-dev 커밋 `530bf0abf` 버전으로 업데이트되었습니다. (#15036)
  * CLDR 이모티콘 및 기호가 44.0 버전으로 업데이트되었습니다. (#15712, @OzancanKaratas)
  * Java Access Bridge가 17.0.9+8Zulu (17.46.19) 버전으로 업데이트되었습니다. (#15744)
* 단축키 명령:
  * 이제 다음 명령은 두 번 및 세 번 눌러 읽은 정보의 철자 및 문자 설명을 알릴 수 있습니다: 선택 내용 읽기, 클립보드 텍스트 읽기, 초점 객체 읽기 (#15449, @CyrilleB79)
  * 화면 커튼 켬/끔 전환 기본 단축키가 추가되었습니다: `NVDA+control+escape`. (#10560, @CyrilleB79)
  * 선택 내용 읽기 단축키를 네 번 누르면 이제 선택 항목이 탐색 가능한 메시지로 표시됩니다. (#15858, @Emil-18)
* Microsoft Office:
  * Excel 셀에서 서식 정보를 요청할 때 테두리 및 배경은 해당 서식이 있는 경우에만 보고됩니다. (#15560, @CyrilleB79)
  * NVDA는 더 이상 최신 버전의 Microsoft Office 365 메뉴에서와 같이 레이블이 지정되지 않은 그룹을 보고하지 않습니다. (#15638)
* '음성 엔진 선택' 대화 상자에서 오디오 출력 장치 및 도킹 모드 옵션이 제거되었습니다.
이 두 옵션은 `NVDA+control+u`를 통해 열 수 있는 음향 설정 패널에서 찾을 수 있습니다. (#15512, @codeofdusk)
* 마우스 설정 카테고리 내 "마우스로 객체 진입 시 역할 알림" 옵션이 "객체에 마우스 포인터 접근 시 알림"로 이름이 변경되었습니다.
이제 마우스가 개체를 입력할 때 테이블의 상태(체크/누름) 또는 셀 좌표와 같은 개체에 대한 추가 관련 정보를 알립니다. (#15420, @LeonarddeR)
* 도움말 메뉴에 다음 새로운 항목이 추가 되었습니다: "도움말, 교육 또는 지원 받기", "NVAccess 샵" (#14631)
* NVDA의 [Poedit](https://poedit.net) 지원을 Poedit 버전 3 이상을 위해 재정비했습니다.
Poedit 1 사용자는 번역기 노트 및 코멘트를 읽는 바로 가기와 같이 Poedit에서 향상된 접근성을 지원받고 싶다면 Poedit 3으로 업데이트하는 것이 좋습니다. (#15313, #7303, @LeonarddeR)
* 이제 점자 출력 보기와 음성 출력 보기가 보안 모드에서 비활성화됩니다. (#15680)
* 객체탐색 중, 비활성화됨(사용할 수 없음) 객체를 더 이상 무시하지 않습니다. (#15477, @CyrilleB79)
* 주요 명령 문서에 목차를 추가했습니다. (#16106)

### 버그 수정내역

* 추가 기능 스토어:
  * 추가 기능의 상태가 "다운로드중"에서 "다운로드"로 변경되는 등 초점이 있는 상태에서 변경되면 업데이트된 항목이 이제 올바르게 알립니다. (#15859, @LeonarddeR)
  * 추가 프롬프트를 설치하는 경우 재시작 대화 상자에서 더 이상 겹치지 않습니다. (#15613, @lukaszgo1)
  * 호환되지 않는 추가 기능을 다시 설치하면 더 이상 강제로 비활성화되지 않습니다. (#15584, @lukaszgo1)
  * 비활성화된 추가 기능과 호환되지 않는 추가 기능을 업데이트할 수 있습니다. (#15568, #15029)
  * 이제 NVDA는 추가 기능을 올바르게 다운로드하지 못할 경우 복구하여 오류를 표시합니다. (#15796)
  * 추가 기능 스토어를 열고 닫은 후 NVDA가 더 이상 간헐적으로 다시 시작되지 않습니다. (#16019, @lukaszgo1)
* 음향:
  * NVDA는 여러 소리를 연속적으로 빠르게 재생할 때 더 이상 짧게 프리즈되지 않습니다. (#15311, #15757, @jcsteh)
  * 오디오 출력 장치가 기본값이 아닌 다른 것으로 설정되어 있고 해당 장치를 사용할 수 없게 된 후 다시 사용할 수 있게 되면 NVDA는 이제 기본 장치를 계속 사용하는 대신 구성된 장치로 다시 전환합니다. (#15759, @jcsteh)
  * 이제 NVDA는 출력 장치의 구성이 변경되거나 다른 응용 프로그램이 장치의 독점적 제어를 해제하는 경우 오디오를 재개합니다. (#15758, #15775, @jcsteh)
* 점자:
  * 여러줄 점자 디스플레이는 더 이상 BRLTY 드라이버와 충돌시키지 않으며 하나의 연속 디스플레이로 취급됩니다. (#15386)
  * 유용한 텍스트가 포함된 개체가 더 많이 감지되고 텍스트 내용이 점자로 표시됩니다. (#15605)
  * 점자 단축 입력이 다시 제대로 작동합니다. (#15773, @aaclause)
  * 더 많은 상황에서 테이블 셀 간에 탐색 객체를 이동할 때 점자가 업데이트됩니다. (#15755, @Emil-18)
  * 현재 초점, 현재 탐색 객체 및 현재 선택 명령을 보고한 결과가 점자로 표시됩니다. (#15844, @Emil-18)
  * 알바트로스 점자 드라이버는 더 이상 Esp32 마이크로컨트롤러를 알바트로스 디스플레이로 취급하지 않습니다. (#15671)
* LibreOffice:
  * `control+backspace` 키보드 바로가기를 사용하여 삭제한 단어에 공백(스페이스, 탭 등)이 따라붙을 때도 제대로 알려줍니다. (#15436, @michaelweghorn)
  * `NVDA+end` 키보드 바로가기를 사용한 상태 표시줄의 알림은 LibrOffice 버전 24.2 이후의 대화 상자에서도 작동합니다. (#15591, @michaelweghorn)
  * 이제 LibreOffice 24.2 이상 버전에서 예상되는 모든 텍스트 특성이 지원됩니다.
이것은 작성자에서 한 줄을 발표할 때 철자 오류를 알리는 것을 효과적으로 만듭니다. (#15648, @michaelweghorn)
  * 헤딩 레벨 알림이 LibreOffice 24.2 이상 버전에서도 작동합니다. (#15881, @michaelweghorn)
* Microsoft Office:
  * UIA가 비활성화된 Excel에서 `control+y`, `control+z`, `alt+backspace`를 누르면 점자가 업데이트되고 활성 셀 콘텐츠가 발화됩니다. (#15547)
  * UIA가 비활성화된 Word에서 `control+v`, `control+x`, `control+y`, `control+z`, `alt+backspace`, `backspace`, `control+backspace`를 누르면 점자가 업데이트됩니다.
  또한 텍스트와 점자를 타이핑하여 검토하고 캐럿을 따라 검토할 때 UIA가 활성화된 상태로 업데이트됩니다. (#3276)
  * Word 에서이제 표 탐색을 위해 네이티브 Word 명령, `alt+home`, `alt+end`, `alt+pageUp`와 `alt+pageDown`을 사용할 때 이동된 셀을 올바르게 보고합니다. (#15805, @CyrilleB79)
* 객체 바로 가기 키 읽기 기능이 향상되었습니다. (#10807, #15816, @CyrilleB79)
* SAPI4 음성 엔진는 이제 음성에 내장된 음량, 속도 및 음정 변경사항을 적절하게 지원합니다. (#15271, @LeonarddeR)
* 이제 Java Access Bridge를 사용하는 응용 프로그램에서 멀티라인 상태를 올바르게 보고합니다. (#14609)
* NVDA는 더 많은 Windows 10 및 11 대화 상자에 대한 대화 내용을 알릴 것입니다. (#15729, @josephsl)
* NVDA는 UIA를 사용할 때 Microsoft Edge에서 새로 로드된 페이지를 읽는 데 실패하지 않습니다. (#15736)
* 텍스트를 읽는 전체 읽기 명령어를 사용할 때 문장이나 문자 사이의 발화 간격은 더 이상 시간이 지남에 따라 점진적으로 감소하지 않습니다. (#15739, @jcsteh)
* NVDA는 많은 양의 텍스트를 말할 때 더 이상 프리즈되지 않습니다. (#15752, @jcsteh)
* UIA를 사용하여 Microsoft Edge에 접근할 때 NVDA는 브라우즈 모드에서 더 많은 컨트롤을 활성화할 수 있습니다. (#14612)
* NVDA는 구성 파일이 손상되었을 때 더 이상 시작하지 않지만 이전과 같이 구성을 기본값으로 복원합니다. (#15690, @CyrilleB79)
* Windows Forms 응용 프로그램에서 System List View(`SysListView32`) 컨트롤에 대한 지원을 수정했습니다. (#15283, @LeonarddeR)
* NVDA의 Python 콘솔 기록을 더 이상 덮어쓸 수 없습니다. (#15792, @CyrilleB79)
* NVDA는 많은 UIA 이벤트가 쇄도할 때(예: 큰 텍스트 덩어리가 단말기에 인쇄되거나 WhatsApp 메신저에서 음성 메시지를 들을 때) 응답성을 유지해야 합니다. (#14888, #15169)
  * 이 새 동작은 NVDA의 고급 설정에서 "향상된 이벤트 처리 사용" 설정을 사용하여 비활성화할 수 있습니다.
* NVDA는 WDAG(Windows Defender Application Guard) 내에서 실행되는 애플리케이션의 초점을 다시 추적할 수 있습니다. (#15164)
* 마우스를 음성 출력 뷰어에서 움직일 때 음성 텍스트가 더 이상 업데이트되지 않습니다. (#15952, @hwf1324)
* NVDA가 Firefox나 Chrome에서 `escape` 또는 `alt+upArrow`로 콤보박스를 닫을 때 다시 탐색 모드로 전환합니다. (#15653)
* iTunes의 콤보 상자에서 위아래로 화살표 키를 누르면 더 이상 탐색 모드로 전환되지 않습니다. (#15653)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

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

#### API 호환성 변경사항

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

#### 지원 종료 예정

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

이번 릴리즈는 보안 문제와 설치 파일 문제를 고치는 페치입니다. 
NVDA의 [보안정책](https://github.com/nvaccess/nvda/blob/master/security.md)에 따라 보안 문제를 공개해 주시기 바랍니다.

### 보안 수정

* 보안 모드가 강제되는 동안 사용자 정의 구성을 불러오는 것을 방지합니다. while secure mode is forced.
([GHSA-727q-h8j2-6p45](https://github.com/nvaccess/nvda/security/advisories/GHSA-727q-h8j2-6p45))

### 버그 수정내역

* NVDA 프로세스를 올바르게 종료하지 못하는 원인이 된 버그를 수정했습니다. (#16123)
* 이전 NVDA 프로세스를 올바르게 종료하지 못한 경우 NVDA 설치가 복구할 수 없는 상태가 될 수 있는 버그를 수정했습니다. (#16122)

## 2023.3.3

이번 릴리즈는 보안 문제와 설치 파일 문제를 고치는 페치입니다. 
NVDA의 [보안정책](https://github.com/nvaccess/nvda/blob/master/security.md)에 따라 보안 문제를 공개해 주시기 바랍니다.

### 보안 수정사항

* 임의 코드 실행을 유발하기 위해 조작된 콘텐츠에서 반사된 XSS 공격 가능성을 방지합니다.
([GHSA-xg6w-23rw-39r8](https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8))

## 2023.3.2

이번 릴리즈는 보안 문제와 설치 파일 문제를 고치는 페치입니다.
2023.3.1 보안 패치가 제대로 해결되지 않았었습니다.
NVDA의 [보안정책](https://github.com/nvaccess/nvda/blob/master/security.md)에 따라 보안 문제를 공개해 주시기 바랍니다.

### 보안 수정사항

* 2023.3.1 보안 패치가 제대로 해결되지 않았었습니다.
인증되지 않은 사용자에 대한 시스템 권한으로 시스템 액세스 및 임의 코드 실행을 방지합니다.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3.1

이번 릴리즈는 보안 문제와 설치 파일 문제를 고치는 페치입니다. 
NVDA의 [보안정책](https://github.com/nvaccess/nvda/blob/master/security.md)에 따라 보안 문제를 공개해 주시기 바랍니다.

### 보안 수정

* 인증되지 않은 사용자에 대한 시스템 권한으로 시스템 액세스 및 임의 코드 실행을 방지합니다.
([GHSA-h7pp-6jqw-g3pj](https://github.com/nvaccess/nvda/security/advisories/GHSA-h7pp-6jqw-g3pj))

## 2023.3

이번 릴리즈는 오디오 출력의 성능, 응답성과 안정성 개선사항을 포함합니다.
NVDA의 소리나 비프음 음량을 제어하거나 음량 볼륨에 맞추는 옵션이 추가되었습니다

NVDA는 이제 OCR 결과를 주기적으로 새로 고쳐 새로운 텍스트를 표시할 수 있습니다.
NVDA의 설정 대화상자의 Windows OCR 범주에서 구성할 수 있습니다.

장치 감지 및 관리자 이동을 개선하는 점자 수정이 몇 가지 있었습니다.
이제 자동 감지에서 원하지 않는 드라이버를 선택하여 자동 감지 성능을 향상시킬 수 있습니다.
새로운 BRLTTY 명령도 있습니다.

추가기능 스토어, Microsoft Office, Microsoft Edge의 컨텍스트 메뉴 및 윈도우 계산기에 대한 버그 수정도 있습니다.

### 새로운 기능

* 강화된 사운드 관리:
  * 새로운 음향 설정 패널:
    * `NVDA+control+u`키로 열 수 있습니다. (#15497)
    * 사용 중인 음성의 볼륨 설정에 따라 NVDA 소리와 비프음의 음량을 설정할 수 있는 음향 설정 옵션 추가 (#1409)
    * NVDA 사운드의 볼륨을 별도로 구성하는 음향 설정 옵션 추가 (#1409, #15038)
    * 오디오 출력 장치를 변경하고 오디오 더킹을 전환하기 위한 설정이 '음성 엔진 선택' 대화상자에서 새 음향 설정 패널로 이동되었습니다.
    2024.1 버전에서 이 옵션은 '음성 엔진 선택' 대화상자으로부터 제거될 예정입니다. (#15486, #8711)
  * NVDA가 이제 오디오를 Windows 오디오 세션 API(WASAPI)로 출력하며, NVDA 음성 말하기 및 사운드의 응답성, 성능 및 안정성을 향상시킬 수 있습니다. (#14697, #11169, #11615, #5096, #10185, #11061)
  * 참고: WASAPI가 일부 추가 기능과 호환되지 않습니다.
  Compatible updates are available for these add-ons, please update them before updating NVDA.
  이러한 추가기능의 호환성 업데이트를 사용가 능합니다, NVDA를 업데이트하기 전에, 해당 추가기능들을 먼저 업데이트하세요.
  NVDA를 업데이트할 때 이러한 추가 기능의 호환되지 않는 버전이 사용되지 않도록 설정됩니다:
    * Tony's Enhancements 1.15 이하 버전 (#15402)
    * NVDA global commands extension 12.0.8 이하 버전 (#15443)
* NVDA는 이제 광학 문자 인식(OCR) 기능 사용 시 지속적으로 결과를 업데이트하는 것이 가능합니다. 새로운 텍스트가 나타나면 말합니다. (#2797)
  * 이 기능을 활성화하려면, NVDA 설정 대화상자의 Windows OCR 카테고리에서 "인식된 콘텐츠를 주기적으로 새로고침"을 활성화하세요.
  * 한번 활성화하면 `NVDA+5` 키(자동 변경 알림)를 눌러 전환하여 새로운 텍스트를 읽을 것인지 말 것인지 선택할 수 있습니다.
* 점자 디스플레이 자동 탐색을 사용할 때, 점자 디스플레이 선택 대화상자에서 특정 점자 디스플레이 장치를 탐색에서 제외할 수 있습니다.  (#15196)
* 문서 서식 알림 설정에 새 옵션인 "들여쓰기 빈줄 무시"이 추가되었습니다. (#13394)
* 브라우즈 모드에서 탭컨트롤을 탐색하는 할당되지 않은 제스처가 추가되었습니다. (#15046)

### 변경사항

* 점자:
  * 캐럿 업데이트를 동반하지 않고 텍스트가 변경되었을 때, 점자 디스플레이의 텍스트는 이제 변경된 줄에 위치할 때 적절하게 업데이트됩니다.
  여기에는 검토하기 위해 점자를 묶는 경우가 포함됩니다. (#15115)
  * 추가적인 BRLTTY 키 바인딩이 NVDA 명령에 매핑됨 (#6483):
    * `learn`: NVDA 입력도움말 토글
    * `prefmenu`: NVDA 메뉴 열기
    * `prefload`/`prefsave`: NVDA 환경 불러오기/저장하기
    * `time`: 시간 표시
    * `say_line`: 리뷰 커서의 현재 위치 줄 읽기
    * `say_below`: 리뷰커서로 모두 읽기
  * BRLTTY 드라이버는 오직 BrlAPI가 활성화BRLTTY 인스턴스 is running. (#15335)
  * HID 점자 지원을 가능하게 하는 고급 설정은 새로운 옵션을 선호하여 삭제되었습니다. 이제 점자 표시 선택 대화상자에서 점자 표시 자동 감지를 위해 특정 드라이버를 비활성화할 수 있습니다. (#15196)
* 추가 기능 스토어: 설치된 추가 기능이 스토어에서 사용 가능한 경우 [사용 가능한 추가 기능] 탭에 나열됩니다. (#15374)
* NVDA 메뉴에서 일부 단축키가 업데이트되었습니다. (#15364)

### 버그 수정내역

* Microsoft Office:
  * Microsoft Word에서 "문서 서식 알림"의 "헤딩"과 "주석 및 코멘트"을 비활성화했을 때 충돌이 나는 것을 수정했습니다. (#15019)
  * 워드 및 엑셀에서, 더 많은 상황에서 텍스트 정렬을 적절하게 읽습니다. (#15206, #15220)
  * 특정 셀에 글자 서식 단축키 사용 시 안내를 수정합니다. (#15527)
* Microsoft Edge:
  * NVDA는 더 이상 Microsoft Edge에서 컨텍스트 메뉴를 열었을 때 이전 브라우즈 모드 위치로 돌아가지 않습니다. (#15309)
  * NVDA는 다시 한번 Microsoft Edge의 다운로드 컨텍스트 메뉴를 읽습니다. (#14916)
* 점자:
  * 이제 제스쳐로 각각의 지표를 보여주거나 숨긴 후 점자 커서와 선택 표시기가 항상 적절하게 업데이트됩니다.  (#15115)
  * 알바트로스 점자 디스플레이가 다른 점자 장치를 연결했는데도 초기화를 시도하는 버그가 수정되었습니다. (#15226)
* 추가 기능 스토어:
  * "호환되지 않는 추가 기능 포함"을 선택 취소하면 호환되지 않는 추가 기능이 저장소에 계속 나열되는 오류가 수정되었습니다. (#15411)
  * 호환성 문제로 인해 차단된 추가 기능은 활성화/비활성화 상태의 필터를 전환할 때 올바르게 필터링되어야 합니다. (#15416)
  * 외부 설치 도구를 사용하여 오버라이드된 호환되지 않는 추가 기능을 업그레이드하거나 교체하는 것을 방지하는 오류가 수정되었습니다. (#15417)
  * 추가 기능 설치 후 다시 시작하기 전까지 NVDA가 말을 하지 못하는 버그를 수정했습니다. (#14525)
  * 이전 다운로드가 실패했거나 취소된 경우 추가 기능을 설치할 수 없는 버그를 수정했습니다. (#15469)
  * NVDA를 업그레이드할 때 호환되지 않는 추가 기능을 처리하는 문제가 해결되었습니다. (#15414, #15412, #15437)
* NVDA는 서버, LTSC 및 LTSB 버전의 Windows 32bit 계산기에서 계산 결과를 다시 한 번 알립니다. (#15230)
* NVDA는 중첩된 창이 포커스를 받으면 더 이상 포커스 변경을 무시하지 않습니다. (#15432)
* NVDA 시작 중 충돌의 잠재적 원인을 수정했습니다. (#15517)

### Changes for Developers

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* `braille.handler.handleUpdate` and `braille.handler.handleReviewMove` have been changed in order not to update instantly.
Before this change, when either of these methods was called very often, this would drain many resources.
These methods now queue an update at the end of every core cycle instead.
They should also be thread safe, making it possible to call them from background threads. (#15163)
* Added official support to register custom braille display drivers in the automatic braille display detection process.
Consult the `braille.BrailleDisplayDriver` class documentation for more details.
Most notably, the `supportsAutomaticDetection` attribute must be set to `True` and the `registerAutomaticDetection` `classmethod` must be implemented.  (#15196)

#### 지원 종료 예정

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

이 릴리즈는 추가 기능 관리자를 대체할 추가 기능 스토어를 공개합니다.
추가 기능 스토어에서는 커뮤니티 추가 기능을 둘러보고, 검색하고, 설치 및 업데이트할 수 있습니다.
더 이상 업데이트가 지원되지 않고 호환되지 않는 문제가 있는 추가 기능을 불안정성을 감수하고 수동으로 활성화 할 수 있습니다.

새로운 점자 기능과 명령, 그리고 점자 디스플레이 지원이 추가되었습니다.
또한 OCR과 전체화면 객체 탐색을 위한 새로운 입력 제스처가 추가되었습니다.
Microsoft Office에서 서식 탐색 및 알림이 개선되었습니다.

많은 버그가 수정되었습니다. 특히 웹 브라우저, Windows 11, Microsoft Office, 점자와 관련된 버그가 수정되었습니다.

eSpeak-NG, LibLouis 점역기, 그리고 유니코드 CLDR이 업데이트되었습니다.

### 새로운 기능

* NVDA에 추가 기능 스토어가 추가되었습니다. (#13985)
  * 커뮤니티 추가 기능을 둘러보고, 검색하고, 설치 및 업데이트할 수 있습니다.
  * 오래된 추가 기능의 호환되지 않는 문제를 수동으로 재정의합니다.
  * 추가 기능 관리가 제거되고 추가 기능 스토어로 대체됩니다.
  * 더 많은 정보는 업데이트된 유저 가이드를 확인하세요.
* 새로운 입력 제스처 추가:
  * 사용 가능한 Windows OCR 언어를 순환 설정 제스처(키 할당되지 않음) (#13036)
  * 점자 메시지 표시 설정을 순환하는 제스처 추가(키 할당되지 않음) (#14864)
  * 선택 표시기 표시 여부를 전환하 제스처 추가(키 할당되지 않음) (#14948)
  * 전체 화면에 있는 객체를 탐색하는 기본 단축키가 추가 및 할당되었습니다. (#15053)
    * Desktop: `NVDA+numpad9`와 `NVDA+numpad3`는 각각 이전 객체와 다음 객체를 탐색합니다.
    * Laptop: `shift+NVDA+[`와 `shift+NVDA+]`는 각각 이전 객체와 다음 객체를 탐색합니다.
* 새로운 점자 기능:
  * Help Tech Activator 점자 디스플레이를 지원합니다. (#14917)
  * 선택 표시기(7점과 8점)를 표시할지 여부를 설정하는 옵션이 추가되었습니다. (#14948)
  * 점자 라우팅 키를 사용하여 검토 커서 위치를 변경할 때 시스템 커서 또는 포커스를 선택적으로 이동하는 새로운 옵션이 추가되었습니다. (#14885, #3166)
  * 이제, `numpad2`를 세 번 눌러 리뷰 커서 위치에 있는 문자 수치 값을 읽을 때 점자 디스플레이에서도 정보를 표시합니다. (#14826)
  * ARIA 1.3 속성인 `aria-brailleroledescription` 지원이 추가되었습니다. 웹 작성자가 점자 디스플레이에 표시된 요소 유형을 재정의할 수 있습니다. (#14748)
  * Baum 점자 드라이버: Windows 키+ D, Alt + Tab 등과 같은 일반적인 키보드 명령을 수행하기 위한 몇 가지 점자 코드 제스처를 추가합니다.
  전체 목록은 NVDA 사용자 가이드를 참조하십시오. (#14714)
* 유니코드 기호 추가:
  * "⠐⠣⠃⠗⠇⠐⠜"와 같은 점자 기호가 추가 되었습니다. (#14548)
  * Mac의 옵션 키 기호 "⌥"가 추가되었습니다. (#14682)
* Tivomatic Caiku 알바트로스 점자 디스플레이군을 위한 제스처가 추가됩니다. (#14844, #15002)
  * 점자 설정 대화상자 열기
  * 상태표시줄 접근
  * 점자 커서 모양 순환설정
  * 점자 메시지 표시 순환설정
  * 점자 커서 표시 켬/끔 전환
  * 점자 선택 표시 켬/끔 전환
  * "리뷰 커서를 라우팅중일 시 점자로 시스템 케럿 이동" 모드 순환 설정
* Microsoft Office 기능 추가:
  * 문서 서식 알림에서 강조 표시된 텍스트가 활성화되었을 때, Microsoft Word에서 강조된 색상을 알립니다. (#7396, #12101, #5866)
  * 문서 서식 알림에서 색상이 활성화되었을 때, Microsoft Word에서 배경색을 알립니다. (#5866)
  * Microsoft Excel 셀에 '굵게', '기울임꼴', '밑줄', '취소선'와 같은 글자 서식을 단축키로 지정할 때, 변경된 결과가 보고됩니다. (#14923)
* 강화된 소리 관리 기능(실험적 기능):
  * 이제 Windows Audio Session API (WASAPI)로 NVDA 소리를 출력할 수 있습니다, NVDA 음성 및 사운드의 응답성, 성능 및 안정성을 향상시킬 수 있습니다. (#14697)
  * WASAPI 사용은 고급 설정에서 사용할 수 있습니다.
  추가적으로, WASAPI가 활성화되어 있으면 다음 고급 옵션을 설정할 수 있습니다.
    * 사용 중인 음성의 볼륨 설정에 따라 NVDA 소리와 비프음의 볼륨을 지정하는 옵션을 제공합니다. (#1409)
    * NVDA 소리 음량을 별도로 설정할 수 있는 옵션을 제공합니다. (#1409, #15038)
  * WASAPI를 사용할 때 간헐적으로 충돌하는 알려진 문제가 있습니다. (#15150)
* Mozilla FireFox와 Google Chrome에서, 이제 작성자가 aria-haspopup을 사용하여 대화 상자, 그리드, 목록 또는 트리를 지정한 경우, 해당 열 때 NVDA가 보고합니다. (#14709)
* 이제 NVDA 이동식 복사본을 만들 때 `%temp%`나 `%homepath%` 같은 시스템 환경 변수로 경로를 지정할 수 있습니다. (#14680)
* Windows 2019년 5월 10일 업데이트 이상에서 Windows 2019년 5월 10일 업데이트 이상에서 NVDA가 가상 데스크탑을 열고 닫거나, 지울 때 이름을 안내합니다. (#5641)
* 사용자와 시스템 관리자가 보안 모드에서 NVDA를 강제로 시작할 수 있도록 시스템 전체 매개 변수가 추가되었습니다. (#10018)

### 변경사항

* 컴포넌트 업데이트:
  * eSpeak NG가 1.52-dev commit `ed9a7bcf`으로 업데이트되었습니다. (#15036)
  * LibLouis 점역기가 [3.25.0](https://github.com/liblouis/liblouis/releases/tag/v3.25.0) 버전으로 업데이트되었습니다. (#14719)
  * 유니코드 CLDR이 43.0로 업데이트되었습니다. (#14918)
* 리브레Office 변경사항:
  * 이제 LibreOffice 버전용 LibreOffice Writer 7.6 버전 이하에서 리뷰 커서 위치를 보고할 때 현재 커서/캐럿 위치가 현재 페이지에 맞게 상대적으로 보고됩니다. 이는 Microsoft Word에 대해 적용된 것과 유사합니다. (#11696)
  * LibreOffice에서 상태 표시줄(예: "NVDA+end")의 알림이 작동합니다. (#11698)
  * LibreOffice Calc에서 다른 셀로 이동할 때 NVDA의 설정에서 셀 좌표 알림이 비활성화된 경우 NVDA는 더 이상 이전에 포커싱된 셀의 좌표를 알리지 않습니다. (#15098)
* 점자 변경사항:
  * 표준 HID 점자 드라이버로 점자 디스플레이를 사용할 때 dpad를 사용하여 화살표 키를 에뮬레이트하고 입력할 수 있습니다. 또한 스페이스+1점과 스페이스+4점이 이제 각각 위쪽 및 아래쪽 화살표에 매핑합니다. (#14713)
  * 동적 웹 콘텐츠 업데이트(ARIA 라이브 리전)가 이제 점자 디스플레이에 표시됩니다.
  고급 설정 패널에서 이 기능을 비활성화할 수 있습니다. (#7756)
* 대시 및 앰 대시 기호가 항상 음성합성기로 전송됩니다. (#13830)
* 이제 Microsoft Word에서 보고된 거리는 UIA를 사용하여 Word 문서에 액세스하는 경우에도 Word의 고급 옵션에 정의된 단위를 따릅니다. (#14542)
* 이제 NVDA는 명령과 초점 변경에 조금 더 빠르게 반응합니다. (#14701)
* NVDA는 편집 컨트롤에서 커서를 이동할 때 더 빠르게 응답합니다. (#14708)
* 링크의 대상을 보고하는 스크립트는 이제 탐색 객체가 아닌 캐럿/포커스 위치를 보고합니다. (#14659)
* 휴대용 복사본을 만들 때 드라이브 문자를 절대 경로의 일부로 입력할 필요가 없습니다. (#14681)
* 시스템 트레이 시간에 "초"를 표시하게 구성했다면 `NVDA+f12`키를 사용했을 때 설정된 시간 설정 형식을 따릅니다. (#14742)
* 이제 NVDA는 최신 버전의 Microsoft Office 365 메뉴와 같이 유용한 위치 정보가 있는 레이블이 지정되지 않은 그룹을 보고합니다. (#14878) 

### 버그 수정내역

* 점자:
  * 점자 디스플레이의 입출력과 관련된 여러 안정성 수정사항이 있습니다, NVDA의 오류 및 충돌 빈도가 줄어듭니다. (#14627)
  * NVDA가 자동 탐색 시 더 이상 불필요하게 여러번 "점자 출력 끔"으로 전환하지 않습니다. (#14524)
  * HumanWare Brailliant나 APH Mantis 같은 HID 블루투스 장치인 경우 NVDA가 USB로 다시 전환됩니다. 디바이스가 자동으로 감지되고 USB 연결을 사용할 수 있게 됩니다. 
    이전에는 Bluetooth 직렬 포트에서만 작동했습니다. (#14524)
* 웹 브라우저:
  * NVDA는 더 이상 Mozilla Firefox가 중단되거나 응답을 중지하지 않습니다. (#14647)
  * Mozilla Firefox와 Google Chrome에서 입력한 글자 말하기가 비활성화된 경우에 입력한 문자가 일부 텍스트 상자에 더 이상 보고되지 않습니다. (#14666)
  * 이전에는 불가능했던 Chrome 내장 컨트롤에서의 브라우즈 모드를 사용할 수 있습니다. (#13493, #8553)
  * Mozilla Firefox에서 링크 뒤 텍스트 위로 마우스를 이동하면 텍스트가 안정적으로 보고됩니다. (#9235)
  * Chrome과 Edge에서 그래픽 링크의 목적 URL이 이제 올바르게 표시됩니다. (#14779)
  * href 속성이 없는 링크 URL을 읽으려고 시도할 때, NVDA가 더 이상 침묵하지 않습니다.
  * 브라우즈 모드에서 NVDA가 더 이상 포커스를 부모 또는 자식 컨트롤로 이동하는 것(예: 컨트롤에서 상위 목록 항목 또는 그리드 셀로 이동)을 잘못 무시하지 않습니다. (#14611)
    * 그러나 이 수정 사항은 브라우즈 모드 설정에서 자동으로 포커스를 포커스 가능한 요소로 설정" 옵션이 해제된 경우에만 적용됩니다(기본값).
* Windows 11를 위한 수정사항:
  * 메모장의 최신 릴리스에서 NVDA는 상태 표시줄 내용을 다시 한 번 알릴 수 있습니다. (#14573)
  * 탭을 전환하면 메모장과 파일 탐색기의 새 탭 이름과 위치가 표시됩니다. (#14587, #14388)
  * NVDA는 중국어, 일본어 등의 언어로 텍스트를 입력할 때 후보 항목을 다시 한 번 알립니다. (#14509)
  * NVDA 도움말 메뉴에서 저작권 정보와 개발 공헌자 항목을 다시 열 수 있습니다. (#14725)
* Microsoft Office를 위한 수정사항:
  * Excel에서 셀 사이를 반복적으로 이동할 땜, 이제 NVDA가 잘못된 셀 또는 선택을 보고할 가능성이 줄어듭니다. (#14983, #12200, #12108)
  * 작업 시트 외부에서 엑셀 셀에 접근할 때 점자 및 초점 강조 표시가 이전에 초점을 두었던 객체로 불필요하게 업데이트되지 않습니다(#15136)
  * Microsoft Excel과 Outlook에서 NVDA가 더 이상 초점을 받은 암호 입력 필드 알림을 실패하지 않습니다. (#14839)
* 현재 로케일에 기호 설명이 없는 기호의 경우 기본 영어 기호 수준이 사용됩니다. (#14558, #14417)
* 이제 유형이 정규식으로 설정되지 않은 경우 사전 항목의 바꾸기 필드에서 백슬래시 문자를 사용할 수 있습니다. (#14556)
* Windows 10과 11 일정 앱에서 컴팩트 오버레이 모드에서 표준 계산기에 식을 입력할 때 NVDA의 휴대용 사본은 더 이상 아무것도 하지 않거나 오류 톤을 재생하지 않습니다. (#14679)
대신에 그 링크에 목적 사이트 주소가 없음을 알립니다. (#14723)
* NVDA는 이전에 완전히 중지된 애플리케이션과 같은 더 많은 상황에서 다시 복구됩니다. (#14759) 
* 특정 터미널 및 콘솔에서 UIA 지원을 강제로 실행할 때 프리징 및 로그 파일 스팸을 유발하는 버그가 수정됩니다. (#14689)
* 구성 재설정 후 NVDA가 더 이상 구성 저장을 거부하지 않습니다. (#13187)
* 런처에서 임시 버전을 실행할 때 NVDA는 사용자가 구성을 저장할 수 있다고 잘못 인식하지 않습니다. (#14914)
* 객체 알림 단축키가 개선되었습니다. (#10807)
* NVDA는 이제 일반적으로 명령과 초점 변경에 약간 더 빠르게 반응합니다. (#14928)
* 일부 시스템에서 OCR 설정을 표시하는 데 실패하지 않을 것입니다. (#15017)
* Synthesizer Swticher를 포함한 NVDA 구성을 저장하거나 불러올 때 버그를 수정합니다. (#14760)
* "위로 쓸기" 터치 제스처가 발생시키는 버그를 수정하여 이전 줄로 이동하는 대신 페이지를 이동합니다. (#15127)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

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

#### 지원 종료 예정

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

새로운 옵션인 "문서 탐색"의 "문단 스타일"이 추가되었습니다.
이것은 메모장 및 메모장++와 같이 기본적으로 문단 탐색을 지원하지 않는 텍스트 편집기와 함께 사용할 수 있습니다.

'NVDA+k'로 매핑된 링크의 목적지를 보고하는 새로운 전역 명령이 있습니다.

주석이 달린 웹 콘텐츠(예: 코멘트 및 각주)에 대한 지원이 향상되었습니다.
주석이 보고될 때 요약을 반복하려면 'NVDA+d'를 누릅니다(예: "코멘트 있음, 각주 있음").

Tovimatic Caiku 알바트로스 46/80 점자 디스플레이가 이제 지원됩니다.

ARM64 및 AMD64 버전의 Windows 지원이 개선되었습니다.

많은 버그 수정이 있으며, 특히 Windows 11 수정이 있습니다.

eSpeak, LibLouis, Sonic rate boost 및 Unicode CLDR이 업데이트되었습니다.
새로운 조지아어, 스와힐리어(케냐), 치체와(말라위) 점자 표가 있습니다.

참고:

* 이 릴리즈는 기존 추가 기능과 호환되지 않습니다.

### 새로운 기능

* UI 자동화가 적용된 Microsoft Excel: 표 행과 열 자동 읽기 기능 추가 (#14228)
  * 참고:여기서 말하는 "표"는 리본의 삽입 탭 창에 있는 "표" 단추를 통해 서식화된 표를 말합니다.
  표 스타일 옵션의 "첫 열"과 "머리말 행"은 열 및 열 머리말과 동일하게 취급됩니다.
  -  이는 현재 UIA에서 지원하지 않는 스크린리더를 통해 이름이 정의된 범위의 헤더를 얘기하는 것이 아닙니다.
* 지연된 문자 설명 읽기 사용을 전환하는 키가 할당되지 않은 제스쳐가 추가되었습니다. (#14267)
* Windows 터미널의 UIA 알림 지원을 통해 터미널에서 새 텍스트 또는 변경된 텍스트를 보고하여 안정성과 응답성을 향상시키는 실험적인 옵션이 추가되었습니다. (#13781)
  * 이 실험 옵션의 제한 사항은 사용 설명서를 참조하십시오.
* ARM64용 Windows 11에서 1Password, Chrome, FireFox와 같은 브라우즈 모드를 사용하는 ARM64용 응용프로그램에서 이제 브라우즈 모드를 사용할 수 있습니다. (#14397)
* 새로운 "문서 탐색" 설정에 "문단 탐색 스타일" 옵션이 추가되었습니다. 
한 줄 개행(기본)과 여러줄 개행(블럭) 문단 탐색 스타일을 지원합니다.
이는 내부적으로 문단 탐색을 지원하지 않는 메모장이나 Notepad++와 같은 텍스트 에디터와에서 사용할 수 있습니다. (#13797) (#13797)
* 여러 개의 주석이 있음을 이제 알립니다.
`nvda+d` 단축키는 이제 여러 주석 대상이 있는 요소에 각 주석 대상의 요약을 순환 보고합니다.
예를 들어, 텍스트에 주석 및 각주가 연결된 경우 이를 읽습니다. (#14507, #14480)
* Tivomatic Caiku 알바트로스 46/80 점자 디스플레이의 지원이 추가되었습니다.. (#13045)
* 새로운 전역 제스처: 링크 목적지 알림 (`NVDA+k`).
한 번 누르면 탐색 객체에 있는 링크의 목적지를 말하고 점자로 표시합니다.
두 번 누르면 더 자세히 읽을 수 있도록 위해 창에 표시합니다. (#14583)
* 할당되지 않은 새로운 제스처 (도구 카테고리): 창에 링크 대상 표시하기.
'NVDA+k'를 두 번 누르는 것과 같지만 점자 사용자에게는 더 유용할 수 있습니다. (#14583)

### 변경 사항

* Liblouis 점역기가 [3.24.0](https://github.com/liblouis/liblouis/releases/tag/v3.24.0)버전으로 업데이트되었습니다. (#14436)
  * 헝가리어, 통합 영어 점자(UEB), 중국어 보포모포 점자에 대한 주요 업데이트.
  * 덴마크어 2022년 표준 점자 지원.
  * 새로운 점자 표: 조지아어 문학 점자, 스와힐리어(케냐)와 체와어(말라위).
* Sonic rate boost(음성 속도 부스트) 라이브러리가 `1d70513`로 업데이트되었습니다. (#14180)
* CLDR이 42.0 버전으로 업데이트되었습니다. (#14273)
* eSpeak NG가 1.52-dev commit `a51235aa` 버전으로 업데이트되었습니다.(#14281)
  * 큰 숫자 알림이 수정됐습니다. (#14241)
* 선택 가능한 상태를 사용하는 컨트롤이 있는 Java 응용 프로그램은 항목이 선택된 시점이 아니라 항목이 선택되지 않은 시점을 알립니다. (#14336)

### 버그 수정내역

* Windows 11 관련 수정사항:
  * 시작 메뉴를 열었을 때, NVDA가 검색 하이라이트를 읽을 것입니다. (#13841)
  * ARM 환경에서 x64 응용프로그램을 더 이상 ARM64 응용프로그램으로 식별하지 않습니다. (#14403)
  * 클립보드 목록에서 "항목 고정"과 같은 항목마다 있는 메뉴 항목에 접근할 수 있습니다. (#14508)
  * 11 22H2 이상에서 마우스와 터치 상호작용을 사용하여 시스템 트레이 오버플로 창과 "열기" 대화 상자와 같은 영역과 다시 상호작용할 수 있습니다. (#14538, #14539)
* Microsoft Excel 주석에서 @USER와 깉이 멘션 입력 시 제안사항을 알립니다. (#13764)
* 이제 Google Chrome 주소 표시줄 막대에서 제안 컨트롤(탭으로 전환, 추천 삭제와 같은 기타등등)을 선택 시 알립니다. (#13522)
* 서식 정보를 요청할 때, 워드패드나 로그 뷰어에서 암묵적으로 "기본 색상"만 알립니다. (#13959)
* FireFox에서, 이제 GitHub 이슈 페이지에서 "옵션 표시" 버튼을 활성화하면 안정적으로 작동합니다. (#14269)
* Outlook 2016 / 365 고급 검색 대화상자의 날짜 선택기에서 이제 레이블과 값을 알립니다. (#12726)
* 이제 Chrome, Edge, Firefox 등에서 ARIA swtich 유형 컨트롤을 체크박스 대신 "전환 버튼"으로 읽습니다. (#11310)
* 열 헤더 안에 있는 버튼을 눌러 정렬 상태 변경 시 자동으로 정렬 상태를 알립니다. (#10890)
* 브라우즈 모드에서 빠른 탐색 또는 포커스를 사용하여 외부에서 내부로 접근할 때 랜드마크 또는 영역 이름을 항상 자동으로 알립니다. (#13307)
* 대문자 탐색 시 비프음과 '대문자' 말하기와 지연된 문자 설명이 같이 켜져있을 때, NVDA가 더 이상 '대문자'와 비프음을 두 번 출력하지 않습니다. (#14239)
* Java 응용 프로그램에서 표 안에 있는 컨트롤을 NVDA가 더 정확하게 알립니다. (#14347)
* 몇몇 설정을 여러 프로파일과 함께 사용할 경우 더 이상 예기치 않게 다르게 설정되지 않습니다. (#14170)
  * 다음 설정이 해결되었습니다:
    * 문서 서식 설정의 줄 들여쓰기 설정.
    * 문서 서식 설정의 셀 테두리 설정
    * 점자 설정의 메시지 출력 설정
    * 점자 설정의 점자 연계설정
  * 아주 드믈게 이 버전의 NVDA를 설치할 때 프로필에 사용된 이러한 설정이 예기치 않게 수정될 수 있습니다.
  * 버전 업데이트 시 위 옵션을 확인하시기 바랍니다..
* 이모지가 이제 더 많은 언어로 보고되어야 합니다. (#14433)
* 일부 요소에서는 더 이상 점자에 주석이 누락되지 않습니다. (#13815)
* "기본" 옵션과 "기본" 옵션의 값을 변경할 때 구성 변경 사항이 올바르게 저장되지 않는 문제를 수정했습니다. (#14133)
* NVDA를 설정할 때는 항상 NVDA 키로 정의된 키가 하나 이상 있어야 합니다. (#14527)
* 알림 영역을 통해 NVDA 메뉴에 접근할 때, 업데이트가 없을 때 NVDA는 더 이상 보류 중인 업데이트를 제안하지 않습니다. (#14523)
* 이제 foobar2000에서 하루 동안 오디오 파일의 남은 시간, 경과 시간 및 총 시간이 올바르게 보고합니다. (#14127)
* Chrome과 Firefox와 같은 웹 브라우저에서는 파일 다운로드와 같은 알림이 음성 외에도 점자로 표시됩니다. (#14562)
* Firefox에서 표의 첫 번째 및 마지막 열로 이동할 때의 버그가 수정됩니다. (#14554)
* NVDA가 `--lang=Windows` 매개변수로 실행되었을 때 NVDA의 일반 설정 대화 상자를 다시 열 수 있습니다. (#14407)
* NVDA는 페이지를 넘긴 후 더 이상 Kindle for PC에서 읽기를 계속하지 않습니다. (#14390)

### 개발 변경사항(영문)

참고: 이것은 추가 기능 API 호환성이 께지는 릴리즈입니다.
애드온은 재테스트를 거쳐 매니페스트를 업데이트해야 합니다.
NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.


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

#### API 호환성 변경사항

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

#### 지원 종료 예정

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

이번 릴리즈는 표 전체 읽기 명령을 포함한 여러 개의 새로운 단축키가 포함되어 있습니다.
빠른 시작 가이드 섹션이 사용자 가이드에 추가되었습니다. 또한, 여러 버그가 포함되어 있습니다.

eSpeak가 업데이트되었으며, LibLouis가 업데이트 되었습니다.
이번 LibLouis 업데이트에는 중국어, 스웨덴어, 루간다어와 키냐르완다어 점자표가 추가되었습니다.

### 새로운 기능

* 사용자 가이드에 빠른 시작 가이드 섹션이 추가되었습니다. (#13934)
* 현재 초점 요소의 키보드 단축키를 확인하는 단축키를 도입되었습니다. (#13960)
  * Desktop 단축키: `shift+numpad2`.
  * Laptop 단축키: `NVDA+ctrl+shift+.`.
* 응용프로그램이 지원하는 경우 검토 커서를 페이지별로 이동하기 위한 새 명령이 도입되었습니다. (#14021)
  * 이전 페이지로 이동:
    * Desktop 단축키: `NVDA+pageUp`
    * Laptop 단축키: `NVDA+shift+pageUp`
  * 다음 페이지로 이동:
    * Desktop 단축키: `NVDA+pageDown`
    * Laptop 단축키: `NVDA+shift+pageDown`
* 다음 표 읽기 명령어가 추가되었습니다. (#14070)
  * 열 내의 모든 내용 읽기: `NVDA+control+alt+downArrow`
  * 행 내의 모든 내용 읽기: `NVDA+control+alt+rightArrow`
  * 모둔 열 읽기: `NVDA+control+alt+upArrow`
  * 모든 행 읽기: `NVDA+control+alt+leftArrow`
* UI 자동화가 적용된 Microsoft Excel: 이제 NVDA가 스프래드시트 표 끝에서 밖으로 이동했을 때 밖으로 이동되었음을 알립니다. (#14165)
* 이제 표 머리글 알림 설정을 구성할 수 있습니다. (#14075)

### 변경 사항

* eSpeakNG가 1.52-dev 커밋 `735ecdb8`으로 업데이트되었습니다. (#14060, #14079, #14118, #14203)
  * 표준 중국어를 사용할 때 라틴 알파벳을 알리는 문제가 수정되었습니다. (#12952, #13572, #14197)
* LibLouis가 [3.23.0](https://github.com/liblouis/liblouis/releases/tag/v3.23.0)로 업데이트되었습니다. (#14112)
  * 점자표가 추가되었습니다:
    * 표준 중국어 점자 (간체)
    * 키냐르완다어 정자 점자
    * 루간다어 정자 점자
    * 스웨덴어 1종(비축약형)
    * 스웨덴어 3종(일부 축약형)
    * 스웨덴어 2종(축약형)
    * 중국어 (중국, 표준) 현행 점자체계 (성조 없음) (#14138)
* 이제 NVDA는 사용자 통계 추적의 일부로 운영 체제의 아키텍처 수집을 포함합니다.

### 버그 수정내역

* Windows Package Manager CLI(winget)를 사용하여 NVDA를 업데이트할 때 릴리스된 NVDA 버전이 설치된 알파 버전보다 항상 최신 버전으로 처리되지 않습니다. (#12469)
* Java 응용프로그램에서 이제 그룹 상자를 올바르게 알립니다. (#13962)
* 캐럿이 Bookworm, WordPad 또는 NVDA 로그 뷰어와 같은 응용 프로그램에서 "모두 읽기" 중에 음성 텍스트를 올바르게 따라갑니다. (#13420, #9179)
* UI 자동화를 사용하는 프로그램에서, 일부 선택된 체크상자를 올바르게 알립니다. (#13975)
* Microsoft Visual Studio, Windows Terminal 및 기타 UI 자동화 기반 응용 프로그램의 성능과 안정성이 향상되었습니다. (#11077, #11209)
  * 이 수정사항은 Windows 11 Sun Valley 2 (version 22H2) 이상에서 적용됩니다.
  * UI 자동화 이벤트 및 속성 변경에 대한 선택적 등록이 이제 기본적으로 활성화됩니다.
* 이제 텍스트 알림, 점자 출력, 암호 숨기기가 특정 Windows 임베디드 터미널과 Microsoft Visual Studio 2022에서 작동합니다. (#14194)
* NVDA는 이제 여러 모니터를 사용할 때 DPI를 인식합니다.
100% 이상의 DPI 설정 또는 여러 모니터를 사용하기 위한 몇 가지 수정 사항이 있습니다.
Windows 10 1809 이전 버전의 Windows에서는 여전히 문제가 있을 수 있습니다.
이러한 수정 사항이 제대로 작동하려면 NVDA가 상호 작용하는 애플리케이션도 DPI를 인식해야 합니다.
Chrome 및 Edge에는 여전히 알려진 문제가 있습니다. (#13254)
  * 이제 시각적 강조 표시 프레임이 대부분의 응용 프로그램에 올바르게 배치되어야 합니다. (#13370, #3875, #12070)
  * 이제 터치 스크린 상호 작용이 대부분의 애플리케이션에서 정확해야 합니다. (#7083)
  * 마우스 추적은 이제 대부분의 응용 프로그램에서 작동합니다. (#6722)
* 방향 상태(가로/세로 방향) 변경은 이제 변경 사항이 없을 때(예: 모니터 변경) 올바르게 무시됩니다. (#14035)
* NVDA는 Windows 10 시작 메뉴 타일과 Windows 11의 가상 데스크톱을 재배치하는 것과 같은 위치에 드래그 항목을 화면에 표시합니다. (#12271, #14081)
* 고급 설정에서 "기본값 복원" 단추를 누르면 "로그된 오류에 대해 사운드 재생" 옵션이 기본값으로 올바르게 복원됩니다. (#14149)
* NVDA는 이제 Java 애플리케이션에서 `NVDA+f10` 바로 가기 키를 사용하여 텍스트를 선택할 수 있습니다. (#14163)
* Microsoft Teams에서 스레드 대화를 위 아래 화살표 키로 탐색할 때 NVDA가 더 이상 메뉴에 갇히지 않습니다. (#14355)

### 개발 변경사항(영문)

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* The [NVDA API Announcement mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about) was created. (#13999)
* NVDA no longer processes `textChange` events for most UI Automation applications due to their extreme negative performance impact. (#11002, #14067)

#### 지원 종료 예정

* `core.post_windowMessageReceipt` is deprecated, use `winAPI.messageWindow.pre_handleWindowMessage` instead.
* `winKernel.SYSTEM_POWER_STATUS` is deprecated and usage is discouraged, this has been moved to `winAPI._powerTracking.SystemPowerStatus`.
* `winUser.SM_*` constants are deprecated, use `winAPI.winUser.constants.SystemMetrics` instead.

## 2022.3.3

This is a minor release to fix issues with 2022.3.2, 2022.3.1 and 2022.3.
This also addresses a security issue.

### Security Fixes

* Prevents possible system access (e.g. NVDA Python console) for unauthenticated users.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### Bug Fixes

* Fixed bug where if NVDA freezes when locking, NVDA will allow access to the users desktop while on the Windows lock screen. (#14416)
* Fixed bug where if NVDA freezes when locking, NVDA will not behave correctly, as if the device was still locked. (#14416)
* Fixed accessibility issues with the Windows "forgot my PIN" process and Windows update/install experience. (#14368)
* Fixed bug when trying to install NVDA in some Windows environments, e.g. Windows Server. (#14379)

### Changes for Developers

#### 지원 종료 예정

* `utils.security.isObjectAboveLockScreen(obj)` is deprecated, instead use `obj.isBelowLockScreen`. (#14416)
* The following functions in `winAPI.sessionTracking` are deprecated for removal in 2023.1. (#14416)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`

## 2022.3.2

이 버전은 2022.3.1의 회귀를 수정하고 보안 문제를 해결하기 위한 마이너 릴리스입니다.

### 보안 수정사항

* 인증되지 않은 사용자의 시스템 수준 접근 가능성을 방지합니다.
([GHSA-3jj9-295f-h69w](https://github.com/nvaccess/nvda/security/advisories/GHSA-3jj9-295f-h69w))

### 버그 수정내역

* 보안 화면에서 특정 기능이 비활성화된 2022.3.1의 회귀를 수정합니다. (#14286)
* NVDA가 잠금 화면에서 시작된 경우 로그인 후 특정 기능이 비활성화된 2022.3.1의 회귀를 수정합니다. (#14301)

## 2022.3.1

이것은 여러 보안 문제를 해결하기 위한 릴리즈입니다.
보안 문제를 `<info@nvaccess.org>`에 책임감 있게 공개해 주세요.

### 보안 수정사항

* 사용자 권한에서 시스템 권한으로 승격할 수 있는 고정 익스플로잇.
([GHSA-q7c2-pgqm-vvw5](https://github.com/nvaccess/nvda/security/advisories/GHSA-q7c2-pgqm-vvw5))
* NVDA 시작을 위한 레이스 조건을 통해 잠금 화면에서 파이썬 콘솔에 액세스할 수 있는 보안 문제를 수정했습니다.
([GHSA-72mj-mqhj-qh4w](https://github.com/nvaccess/nvda/security/advisories/GHSA-72mj-mqhj-qh4w))
* Windows를 잠글 때 음성 뷰어 텍스트가 캐시되는 문제를 해결했습니다.
([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

### 버그 수정내역

* 인증되지 않은 사용자가 잠금 화면에서 음성 및 점자 뷰어 설정을 업데이트하지 못하도록 합니다. ([GHSA-grvr-j2h8-3qm4](https://github.com/nvaccess/nvda/security/advisories/GHSA-grvr-j2h8-3qm4))

## 2022.3

이 릴리즈의 상당 부분은 NVDA 개발자 커뮤니티로부터 기여됐습니다.
이번 릴리즈에는 지연된 글자 설명 읽기와 개선된 Windows Console 지원이 포함되었습니다.

이 릴리즈는 여러 버그 수정 또한 포함합니다.
특히, 업데이트된 Adobe Acrobat 또는 Reader에서 PDF 문서를 읽을 때, 더 이상 충돌이 일어나지 않습니다.

eSpeak가 업데이트되어, 3개의 새로운 언어가 추가됐습니다: 벨라루스어, 룩셈부르크어, 그리고 토톤테펙 혼합어.

### 새로운 기능

* 명령 프롬프트, PowerShell, Windows 11 22H2 버전(Sun Valley 2) 이상 리눅스용 Windows 하위시스템으로 사용되는 Windows Console host에서:
  * 안정성과 성능이 매우 개선되었습니다. (#10964)
  -`control+f`를 눌러 텍스트를 찾을 때, 리뷰커서의 위치가 찾은 용어 위치로 업데이트됩니다. (#11172)
  * 입력한 글자가 나타나지 않는 상황(예: 암호 입력)에서 입력 글자 알림이 기본으로 비활성화됩니다. 이 기능은 NVDA 설정의 고급 패널에서 다시 활성화할 수 있습니다.. (#11554)
  * 스크롤되어 보이지 않는 텍스트를 스크롤하지 않고 리뷰할 수 있습니다. (#12669)
  * 더 자세한 텍스트 형식([microsoft/terminal PR 10336](https://github.com/microsoft/terminal/pull/10336))을 사용가능합니다.
* 일정 시간 후 글자 설명을 읽게 하기 위한 새로운 음성출력 설정이 추가되었습니다. (#13509)
* 디스플레이를 앞으로/뒤로 스크롤하면 음성이 중단할지 여부를 결정하기 위한 새로운 점자 설정이 추가되었습니다. (#2124)

### 변경사항

* eSpeak NG가 1.52-dev 커밋 `9de65fcb`로 업데이트 되었습니다.. (#13295)
  * 추가된 언어:
  * 벨라루스어
  * 룩셈부르크어
  * 토텐테펙 혼합어
* UI 자동화를 사용하여 Microsoft Excel 스프레드시트 컨트롤에 접근할 때, 이제 NVDA가 셀이 병합되었을 때 알릴 수 있습니다. (#12843)
* Instead of reporting "has details" the purpose of details is included where possible, for example "has comment". (#13649)
* 가능한 경우 "상세정보 있음"을 보고하는 대신 ""과 같은 세부정보의 목적이 포함됩니다. (#13649)
* The installation size of NVDA is now shown in Windows Programs and Feature section. (#13909)

### 버그 수정내역

* PDF 문서를 읽을 때 Adobe Acrobat과 Reader 64bit가 충돌하지 않습니다. (#12920)
  * 충돌을 방지하려면 해당 Adobe 제품의 최신 버전 업데이트가 필요합니다.
* 글자 크기 단위를 이제 번역할 수 있습니다. (#13573)
* Java 응용프로그램에서 Window Handle을 찾지 못할 때 Java Access Bridge 이벤트를 무시합니다. 
이는 IntelliJ IDEA가 포함된 일부 Java 응용프로그램의 성능을 개선해줍니다. (#13039)
* LibreOffice Calc에서 선택된 셀 알림 더 효율적으로 변경됐으며 셀이 많이 선택되었을 때 더 이상 멈추지 않습니다. (#13232)
* 다른 사용자로 실행 중인 경우 Microsoft Edge에 더 이상 액세스할 수 없습니다. (#13032)
* 음성 속도 증폭이 꺼져 있을 때, eSpeak의 음성속도가 99%와 100% 사이에서 내려가지 않습니다. (#13876)
* 제스쳐 설정 대화상자를 두 개 열 수 있던 버그가 수정되었습니다. (#13854)

### 개발 변경사항(영문)

* Updated Comtypes to version 1.1.11. (#12953)
* In builds of Windows Console (`conhost.exe`) with an NVDA API level of 2 (`FORMATTED`) or greater, such as those included with Windows 11 version 22H2 (Sun Valley 2), UI Automation is now used by default. (#10964)
  * This can be overridden by changing the "Windows Console support" setting in NVDA's advanced settings panel.
  * To find your Windows Console's NVDA API level, set "Windows Console support" to "UIA when available", then check the NVDA+F1 log opened from a running Windows Console instance.
* The Chromium virtual buffer is now loaded even when the document object has the MSAA `STATE_SYSTEM_BUSY` exposed via IA2. (#13306)
* A config spec type `featureFlag` has been created for use with experimental features in NVDA. See `devDocs/featureFlag.md` for more information. (#13859)

#### 지원 종료 예정

There are no deprecations proposed in 2022.3.

## 2022.2.4

보안 문제를 해결하기 위한 패치 릴리스입니다.

### 버그 수정내역

* 잠금 화면의 로그 뷰어를 통해 NVDA 파이썬 콘솔을 열 수 있는 익스플로잇을 수정했습니다.
([GHSA-585m-rpvvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

이번 릴리즈는 2022.2.1에 도입된 실수로 인한 API 손상을 수정하기 위한 패치입니다.

### 버그 수정내역

* NVDA가 보안 데스크톱에 들어갈 때 "보안 데스크톱"을 표시하지 않는 버그를 수정했습니다.
  이로 인해 NVDA Remote가 보안 데스크톱을 인식하지 못했습니다. (#14094)

## 2022.2.2

이것은 2022.2.1에서 입력 제스처 도입으로 인해 생긴 버그를 수정하기 위한 패치 릴리즈입니다.

### Bug Fixes

* 입력 제스처가 항상 작동하지 않는 버그를 수정했습니다. (#14065)

## 2022.2.1

이것은 보안 문제를 해결하기 위한 사소한 릴리스입니다.
보안 문제를 `<info@nvaccess.org>`에 책임감 있게 공개해 주세요.

### 보안 수정사항

* 잠금 화면에서 파이썬 콘솔을 실행할 수 있었던 고정 익스플로잇. (GHSA-rmq3-vvhq-gp32)
* 객체 탐색을 사용하여 잠금 화면을 피할 수 있었던 고정 익스플로잇. (GHSA-rmq3-vvhq-gp32)

### 개발 변경사항(영문)

#### 지원 종료 예정

These deprecations are currently not scheduled for removal.
The deprecated aliases will remain until further notice.
Please test the new API and provide feedback.
For add-on authors, please open a GitHub issue if these changes stop the API from meeting your needs.

* `appModules.lockapp.LockAppObject` should be replaced with `NVDAObjects.lockscreen.LockScreenObject`. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS` should be replaced with `utils.security.getSafeScripts()`. (GHSA-rmq3-vvhq-gp32)

## 2022.2

이번 릴리즈에는 많은 버그 수정이 포함됩니다.
특히, Java 기반의 응용프로그램과 점자 디스플레이, Windows 기능에 매우 큰 개선이 이루어졌습니다.

새로운 표 탐색 기능이 추가되었습니다.
유니코드 CLDR이 업데이트되었습니다.
Liblouis가 새로운 독일어 점자표를 포함하여 업데이트되었습니다.

### 새로운 기능

* Microsoft Office 제품군에서 Microsoft Loop Components에 대한 상호작용을 지원합니다. (#13617)
* 새로운 표 탐색 명령이 추가되었습니다. (#957)
  * `control+alt+home/end` 단축키를 통해 첫 열과 마지막 열에 빠르게 접근할 수 있습니다.
  * `control+alt+pageUp/pageDown` 단축키를 통해 첫 행과 마지막 행에 빠르게 접근할 수 있습니다.
* 언어 및 방언 자동 전환에 대한 모드 순환 단축키가 추가됩니다. 기본적으로 단축키가 할당돼 있지 않습니다. (#10253)

### 변경사항

* NSIS가 3.08버전으로 업데이트되었습니다. (#9134)
* CLDR이 41.0버전으로 업데이트되었습니다. (#13582)
* LibLouis 점역기가 [3.22.0](https://github.com/liblouis/liblouis/releases/tag/v3.22.0)버전으로 업데이트되었습니다. (#13775)
  * 새로운 점자표: 독일어 2종 (상세)
* 새로운 컨트롤 역할, "작업대기 표시기"가 추가되었습니다. (#10644)
* 이제 NVDA가 동작을 수행하지 못할 때 이에 대해 알립니다. (#13500)
  * 다음 상황이 포함됩니다:
    * Microsoft Stroe 버전의 NVDA를 사용 중일 때.
    * 보안 데스크탑 화면일 때.
    * 모달 대화상자가 응답을 기다릴 때.

### 버그 수정내역

* Java 기반의 응용프로그램에 대한 버그 수정:
  * NVDA는 이제 읽기전용 상태정보를 알립니다. (#13692)
  * NVDA는 이제 "사용할 수 없음"과 사용가능 상태정보를 정확하게 알립니다. (#10993)
  * NVDA는 이제 Function키들을 포함한 단축키를 알립니다. (#13643)
  * NVDA는 이제 진행률 막대에서 말하기 또는 비프음으로 진행률을 알릴 수 있습니다. (#13594)
  * NVDA는 사용자에게 표시할 때 더 이상 위젯에서 텍스트를 잘못 제거하지 않습니다. (#13102)
  * NVDA는 이제 전환 버튼에 대한 상태정보를 알립니다. (#9728)
  * NVDA는 이제 여러개의 창이 있는 Java 응용프로그램에서 창을 식별합니다. (#9184)
  * NVDA는 이제 탭 컨트롤에 대한 위치 정보를 알립니다. (#13744)
* 점자 버그 수정:
  * Mozilla ThunderBird에서 초안을 작성하는 것과 같이 특정 텍스트를 Mozilla 리치텍스트 편집창에서 탐색할 때의 점자 출력을 수정합니다. (#12542)
  * 점자 디스플레이가 자동으로 연결되고 마우스 추적을 활성화한 상태에서 마우스를 움직이면,
  텍스트 리뷰 커서 명령은 이제 점자 디스플레이에 발화된 콘텐츠로 업데이트합니다. (#11519)
  * 이제 텍스트 리뷰 명령을 사용한 후 콘텐츠를 점자 디스플레이가 따라갈 수 있습니다. (#8682)
* 이제 NVDA 설치 관리자를 특수한 문자로 된 디렉토리에서 실행 가능합니다. (#13270)
* Firefox에서 aria-rowindex, aria-colindex, aria-rowcount 또는 aria-colcount 속성이 잘못 설정됐을 때 NVDA는 더 이상 항목을 알리는 데에 실패하지 않습니다. (#13405)
* 표 탐색을 사용하여 병합된 셀을 탐색할 때 커서가 행 또는 열을 더 이상 전환하지 않습니다. (#7278)
* 이제 Adobe Reader에서 상호작용할 수 없는 PDF들을 읽을 때, 서식의 유형과 상태(체크상자나 라디오버튼 같은 서식)을 읽습니다. (#13285)
* 이제 "기본 환경설정으로 초기화" 메뉴를 보안 데스크탑에서 접근 가능합니다.. (#13547)
* NVDA가 종료되면 잠긴 마우스 키가 해제됩니다. 기존에는 마우스 버튼이 잠긴 상태로 남겨졌었습니다. (#13410)
* Visual Studio에서 이제 줄 번호를 알립니다. (#13604)
  * 줄 번호 안내에 대해 참고로, 줄 번호 표시와 줄 번호 알림이 Visual Studio와 NVDA에서 모두 켜져있어야 합니다.
* Visual Studio에서 이제 줄 들여쓰기를 정확하게 안내할 것입니다. (#13574)
* Windows 10과 Windows 11 최근 릴리즈에서 NVDA가 다시 시작 메뉴 검색 결과 상세 내용을 다시 한 번 알릴 것입니다. (#13544)
* Windows 10과 11의 계산기 10.1908버전 이상에서, 
NVDA는 공학 모드의 명령 등, 더 많은 명령에 대해 결과를 알립니다. (#13383)
* Windows 11에서 작업표시줄이나 작업보기같은 유저 인터페이스 요소와 마우스 또는 터치 상호작용을 통해 탐색 및 상호작용이 다시 가능해 집니다. (#13506)
* 워드패드와 다른 `richText` 컨트롤에서 숨겨진 텍스트를 더 이상 알리지 않습니다. (#13618)
* Windows 11 메모장에서 상태표시줄 내용을 읽을 것입니다. (#13688)
* 이제 탐색 객체 표시 기능을 활성화하면 강조 표시가 즉시 나타납니다. (#13641)
* 단일 열로 된 목록보기 항목의 읽기 문제을 수정합니다. (#13659, #13735)
* 영어 및 프랑스어를 영국 영어와 프랑스어(프랑스)로 되돌리는 경우에 대한 eSpeak 자동 언어 전환을 수정합니다. (#13727)
* 이전에 설치된 언어로 전환하려고 할 경우에 대한 OneCore의 자동 언어 전환을 수정합니다. (#13732)

### 개발 변경사항(영문)

* Compiling NVDA dependencies with Visual Studio 2022 (17.0) is now supported.
For development and release builds, Visual Studio 2019 is still used. (#13033)
* When retrieving the count of selected children via accSelection,
the case where a negative child ID or an IDispatch is returned by `IAccessible::get_accSelection` is now handled properly. (#13277)
* New convenience functions `registerExecutableWithAppModule` and `unregisterExecutable` were added to the `appModuleHandler` module.
They can be used to use a single App Module with multiple executables. (#13366)

#### 지원 종료 예정

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

이번 릴리즈는 Microsoft Office의 UIA 지원을 포함합니다.
Windows 11 환경의 Microsoft Office 16.0.15000에서 NVDA는 이제 기본으로 UI Automation을 사용하여 Microsoft Word 문서에 접근합니다.
이는 오래된 객체 모델에 접근 시 큰 성능 향상을 제공합니다.

Seika Notetaker, Panenmeier, HID 점자 디스플레이의 점자 디스플레이 드라이버가 향상되었습니다.
또한, 계산기, 콘솔, 터미널, 메일 그리고 이모지 패널 등 응용프로그램의 다양한 Windows 11 버그가 수정되었습니다.

eSpeak-NG와 LibLouis가 업데이트되었으며 일본어와 독일어, 카탈로니아어 점자표가 새로 추가되었습니다.

참고:

 * 이 릴리스는 기존 추가 기능과의 호환성 문제가 있습니다.

### 새로운 기능

* UI 자동화 활성화 시 Windows 11 환경의 Microsoft Excel에서 메모/코멘트를 알립니다. (#12861)
* Windows 11 환경의 UI 자동화를 사용하는 최근 버전의 Microsoft Word에서 존재하는 책갈피, 초안 코맨트, 해결된 코맨트를 이제 점자와 음성을 통해 알립니다.
* 새로운 `--lang` 명령줄 매개변수는 NVDA 사용 언어 설정보다 우선되게끔 허용합니다. (#10044)
* NVDA가 알려지지 않거나 추가기능에서 사용하지 않은 명령줄 매개변수에 대해 경고를 출력합니다. (#12795)
* Microsoft Word를 UI 자동화로 접근했을 때, Microsoft Word UI는 이제 NVDA가 mathPlayer를 사용하여 Office 수학 방정식을 읽고 탐색합니다. (#12946)
  * 이것이 작동하기 위해서는 반드시 Microsoft Word 365/2016 build 14326 이상을 사용해야 합니다. 
  * MathType 방정식은 반드시 컨텍스트 메뉴를 열고, 방정식 옵션을 개별적으로 선택하여 Office 수식으로 변환해야 합니다.
* "상세정보 있음" 알림과 상세정보 요약 관련 제스처가 포커스 모드에서 작동하도록 업데이트되었습니다. (#13106)
* 이제 Seika Notetaker를 USB나 Bluetooth로 입력시 자동으로 인식됩니다. (#13191, #13142)
  * 다음 디바이스에 적용됩니다: MiniSeika (16, 24셀), V6, V6Pro (40 셀)
  * 이제 블루투스 COM 포트를 수동으로 선택하는 것또한 지원됩니다.
* 점자 뷰어를 토글하는 제스처가 추가되었습니다. 연결된 기본 제스처가 없습니다. (#13258)
* 점자 디스플레이를 사용하여 여러 수식자를 동시에 전환하는 명령이 추가되었습니다. (#13152)
* 음성 발음 사전의 새 기능  "모두 제거" 버튼은 발음 사전을 통째로 삭제하는 데 도움을 줍니다 (#11802)
* Windows 11 계산기 지원이 추가됩니다. (#13212)
* UI 자동화가 활성화된 Windows 11 환경의 Microsoft Word에서 줄 수와 선택된 수를 읽을 수 있습니다. (#13283, #13515)
* Windows 11 환경의 16.0.15000 버전 이상 Microsoft Office에서, NVDA가 UI 자동화를 사용하여 Microsoft Word 문서에 접근합니다, 이전 객체 모델에 비해 성능이 크게 향상되었습니다. (#13437)
 * 여기에는 Microsoft Word 자체의 문서와 Microsoft Outlook의 메시지 판독기 및 작성기가 포함됩니다.

### 변경 사항

* Espeak-NG가 1.51-dev commit `7e5457f91e10`로 업데이트 되었습니다. (#12950)
* liblouis 점역기 엔진이 [3.21.0](https://github.com/liblouis/liblouis/releases/tag/v3.21.0)으로 업데이트되었습니다. (#13141, #13438)
  * 새로운 점자표 추가됨: 일본어 한자(Kantenji) 점자.
  * 새로운 점자표 추가됨: 독일어 6점 컴퓨터 점자.
  * 새로운 점자표 추가됨: 카탈로니아어 1종 점자 (#13408)
* LibreOffice Calc 7.3이상에서 NVDA가 선택과 병합된 셀을 알립니다. (#9310, #6897)
* Unicode Common Locale Data Repository (CLDR)가 40.0으로 업데이트되었습니다. (#12999)
* `NVDA+Numpad Delete`가 캐럿 또는 초점객체 위치를 기본으로 알립니다. (#13060)
* `NVDA+Shift+Numpad Delete`가 리뷰 커서 위치를 알립니다. (#13060)
* Freedom Scientific 기기에서 모디 키를 전환하기 위한 기본 제스처 바인딩이 추가되었습니다. (#13152)
* 텍스트 서식 알림 제스처 사용 시 "기본글꼴"을 더 이상 알리지 않습니다. (#11815)
* 긴 설명 활성화 제스처는 더 이상 기본 제스처가 없습니다 (#13380)
* 상세 정보 요약 알림의 기본 제스처가 설정되었습니다(`NVDA+d`). (#13380)
* MathPlayer를 설치 후 NVDA 재시작이 요구됩니다. (#13486)

### 버그 수정내역

* 일부 Office 프로그램을 열고 있을 때 클립보드 목록 창에서 더 이상 부적절하게 초점을 가로체지 않습니다. (#12736)
* 사용자가 기본 마우스 버튼을 왼쪽에서 오른쪽으로 바꾸도록 선택한 시스템에서 NVDA는 웹 브라우저와 같은 응용 프로그램에서 항목을 활성화하는 대신 컨텍스트 메뉴를 더 이상 표시하지 않습니다. (#12642)
* UI Automation을 사용하는 Microsoft Word에서 리뷰 커서를 텍스트 컨트롤의 끝을 넘어 이동을 시도하면 더 많은 상황에서 올바르게 "맨 아래"를 보고됩니다. (#12808)
* 64-bit 버전 Windows를 구동 중에 NVDA가 System32에 배치된 옛 바이너리의 응용 프로그램 이름과 버전을 알릴 수 있습니다. (#12943)
* 터미널에서 출력내용을 읽는 것에 대한 일관성이 향상되었습니다. (#12974)
  * 경우에 따라 행 중간에 문자를 삽입하거나 삭제할 때 캐럿 뒤의 문자를 다시 읽을 수 있습니다.
* UI자동화를 사용하는 Microsoft Word에서: 브라우즈 모드에서 헤딩간 빠른 탐색이 더 이상 막히지 않으며, NVDA 요소 목록 대화상자에 두 번 표시되지 않습니다. (#9540)
* Windows 8 이상에서, 파일 탐색기의 상태표시줄을 표준 제스처인 NVDA+end(desktop 배열)과 NVDA+shift+end (laptop 배열)로 탐색할 수 있습니다. (#12845)
* Skype for Business의 채팅에서 들어오는 메시지를 다시 알립니다. (#9295)
* Windows 11에서 NVDA로 SAPI5 음성엔진 사용 시 다시 오디오 도킹을 사용할 수 있습니다. (#12913)
* Windows 10 계산기에서 NVDA는 계산 기록 및 기억 목록 항목에 대한 레이블을 알립니다. (#11858)
* 스크롤 및 라우팅과 같은 제스처가 HID 점자 장치에서 작동합니다. (#13228)
* Windows 11 메일: 앱 간에 포커스를 전환한 후 긴 이메일을 읽는 동안 NVDA는 더 이상 이메일의 한 줄에 갇히지 않습니다. (#13050)
* HID 점자기기: 스페이스 조합키 (e.g. `space+dot4`)가 점자 디스플레이에서 성공적으로 수행될 수 있습니다. (#13326)
* 동시에 여러개의 설정 대화상자를 열 수 있었던 문제가 수정되었습니다. (#12818)
* 컴퓨터를 절전 모드에서 깨운 후 일부 Focus Blue 점자 디스플레이가 작동을 멈추는 문제를 해결했습니다. (#9830)
* "위첨자/아랫첨자 알림"이 활성화되었을 때 "기본글꼴"을 알리지 않습니다. (#11078)
* Windows 11에서 NVDA가 이모지를 선택할 때 이모지 패널의 탐색을 더 이상 방해하지 않습니다. (#13104)
* Windows 콘솔 및 터미널을 사용할 때 이중 알림를 유발하는 버그가 수정됩니다. (#13261)
* REAPER와 같은 64비트 응용 프로그램에서 목록 항목을 보고할 수 없는 몇 가지 사례를 수정했습니다. (#8175)
* Microsoft Edge 다운로드 관리자에서 가장 최근에 다운로드된 목록 항목에 초점이 이동되면 NVDA가 자동으로 포커스 모드로 전환합니다. (#13221)
* NVDA가 더 이상 64비트 버전의 Notepad++ 8.3 이상과 충돌하지 않습니다.(#13311)
* Adobe Reader가 보호 모드로 시작될 때 충돌하지 않습니다. (#11568)
* Papenmeier 점자 디스플레이 드라이버를 선택하면 NVDA가 충돌하는 오류를 수정했습니다. (#13348)
* UI자동화를 사용하는 Microsoft Word에서: 빈 표 셀에서 내용이 있는 셀로 이동하거나 문서의 끝에서 기존 내용으로 이동할 때 페이지 번호 및 기타 서식을 더 이상 부적절하게 알리지 않습니다. (#13458, #13459)
* Google Chrome 100에서 페이지를 불러올 때, 더 이상 NVDA가 페이지 제목을 알리기와 자동 읽기를 실패하지 않습니다. (#13571)
* NVDA 구성을 초기 기본값으로 되돌릴 때 기능키 말하기가 켜진 상태에서 더 이상 충돌하지 않습니다. (#13634)

### 개발 변경사항(영문)

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

이 릴리즈는 보안 이슈에 대한 추가 마이너 버전입니다.
보안 문제 발견 시, 반드시 info@nvaccess.org에 재보해주세요.

### 보안 수정사항

* 보안 권고사항 `GHSA-xc5m-v23f-pgr7`
  * 이제 보안 모드에서 기호 발음 대화 상자가 비활성화됩니다.

## 2021.3.4

이번 릴리즈는 제기된 여러 보안 문제를 해결하기 위한 추가 마이너 버전입니다.
보안 문제 발견 시, 반드시 info@nvaccess.org에 재보해주세요.

### 보안 수정사항

* 보안 권고사항 `GHSA-354r-wr4v-cx28` (#13488)
  * NVDA가 보안 모드로 실행될 때 디버그 로깅을 활성화한 상태에서 NVDA를 시작하는 기능이 제거합니다.
  * NVDA가 보안 모드에서 실행될 때 NVDA를 업데이트하는 기능을 제거합니다.
* 보안 권고사항 `GHSA-wg65-7r23-h6p9` (#13489)
  * 보안 모드에서 입력 제스처 대화 상자를 여는 기능을 제거합니다.
  * 보안 모드에서 기본, 임시 및 음성 사전 대화 상자를 여는 기능을 제거합니다.
* 보안 권고사항 `GHSA-mvc8-5rv9-w3hx` (#13487)
  * 이제 wx GUI 검사 도구가 보안 모드에서 비활성화됩니다.

## 2021.3.3

이 릴리즈는 2021.3.2와 동일합니다.
NVDA 2021.3.2에서 2021.3.1로 잘못 식별되는 버그가 있었습니다.
이 릴리스는 2021.3.3으로 정확하게 식별됩니다.

## 2021.3.2

이번 릴리즈는 제기된 여러 보안 문제를 해결하기 위한 추가 마이너 버전입니다.
보안 문제 발견 시, 반드시 info@nvaccess.org에 재보해주세요.

### 버그 수정내역

* 보안 수정: Windows 10(윈도우 10) 및 Windows 11(윈도우 11)에서 잠금 화면 외부에 있는 객체에 대한 객체 탐색을 막습니다. (#13328)
* 보안 수정: 보안 화면에서 '추가 기능 관리자' 대화상자가 비활성화됩니다. (#13059)
* 보안 수정: 보안 화면에서 NVDA 컨텍스트 도움말을 더 이상 사용할 수 없습니다. (#13353)

## 2021.3.1

2021.3의 여러 문제를 해결하기 위한 마이너 릴리즈 버전입니다.

### 변경사항

* 다른 점자 드라이버를 사용할 수 있을 대 새로운 HID Braille 규악이 더 이상 우선시되지 않습니다. (#13153)
* 고급 설정 패널을 통해 새로운 HID Braille 규악을 비활성화할 수 있습니다. (#13180)

### 버그 수정내역

* 랜드마크가 다시 점자로 축약됩니다. (#13158)
* Bluetooth 사용 시 Humanware Brailliant 및 APH Mantis Q40 점자 디스플레이에 대한 불안정한 점자 디스플레이 자동 감지가 수정되었습니다. (#13153)

## 2021.3

이번 릴리즈는 새로운 HID 점자 사양 지원을 소개합니다.
이번 사양은 점자 디스플레이를 별도의 드라이버 필요없이 지원하기 위해 표준화하는 것을 목표로 합니다.
eSpeak-NG와 LibLouis 엔진이 업데이트 되었으며, 러시아어와 벤다어 점자표가 포함되었습니다.
NVDA 고급설정의 새로운 옵션을 통해 오류 효과음을 NVDA 안정화 버전에서도 활성화할 수 있습니다.
이제 Word에서 모두 읽기 사용 시, 현재 스크롤 위치에서 보이는 만큼을 읽습니다.
UIA와 Office를 사용할 때의 많은 개선사항이 있습니다. 
UIA의 수정사항 중 한가지로, Outlook의 메시지에서 더 많은 종류의 레이아웃 테이블 무시할 수 있습니다.

중요사항:

NVDA 2021.2에서 보안 인증서의 업데이트로 인해 업데이트를 확인할 때 소수의 사용자에게 오류가 발생합니다.
NVDA는 이제 Windows에 보안 인증서 업데이트를 요청하여 향후 이 오류를 방지할 수 있습니다.
이에 영향을 받는 사용자는 이 업데이트를 수동으로 다운로드해야 합니다.

### 새로운 기능

* 테이블 셀 테두리의 모양 알림을 토글할 수 있는 입력 제스처가 추가됩니다. (#10408)
* 점자디스플레이 표준화를 목표로 지원 새로운 HID 점자 사양을 지원합니다. (#12523)
  * 이 사양을 지원하는 점자 디스플레이를 NVDA에서 자동으로 감지됩니다.
  * NVDA의 이 규격 구현에 대한 기술적 세부 사항은 다음을 확인하세요. https://github.com/nvaccess/nvda/blob/master/devDocs/hidBrailleTechnicalNotes.md
* VisioBraille Vario 4 Braille 기기를 지원을 추가합니다.. (#12607)
* 아무 NVDA 버전에서 오류 알림을 활성화 할 수 있습니다(고급 설정에서). (#12672)
* Windows 10 이상에서, 설정이나 Microsoft Store와 같은 앱에 있는 검색요소에 진입할 때, NVDA가 제안사항 개수를 알립니다.  (#7330, #12758, #12790)
* PowerShell의 Out-GridView cmdlet을 사용하여 만들어진 그리드 컨트롤에서 테이블 탐색을 지원합니다. (#12928)

### 변경사항

* ESpeak-NG가 업데이트되었습니다(버전 1.51-dev commit `74068b91bcd578bd7030a7a6cde2085114b79b44`). (#12665)
* OneCore 음성이 설치되어 있지 않으면 NVDA 기본음성을 eSpeak로 설정합니다. (#10451)
* NVDA 기본 언어를 지원하는 설치된 OneCore 음성이 없을 경우 NVDA는 기본적으로 eSpeak으로 설정됩니다. (#10451) OneCore 음성이 발화에 실패하면 음성엔진을 eSpeak로 설정합니다. (#11544)
* `NVDA+end`로 상태표시줄을 읽을 때, 더 이상 해당 영역으로 리뷰커서를 이동하지 않습니다.
이 기능이 필요하면 제스처 설정 대화상자의 객체 탐색 범주에 있는 해당 스크립트에 제스처를 할당하십시오. (#8600)
* 이미 열려 있는 설정 대화 상자를 열 때 NVDA는 오류가 발생하기 보다는 기존 대화 상자에 초점을 맞춥니다. (#5383)
* Liblouis 점역 엔진이 다음 버전으로 업데이트되었습니다. [3.19.0](https://github.com/liblouis/liblouis/releases/tag/v3.19.0) (#12810)
  * 새 점자표: 러시아어 1종, 벤다어 1종, 벤다어 2종
* 이제 말하기와 점자 출력에서 "표시된 문구"나 "mrkd" 대신에 "하이라이트"나 "hlght"를 출력합니다. (#12892)
* 대화상자가 필요한 작업(예: 확인/취소)을 기다리고 있을 때 NVDA는 더 이상 종료 시도를 하지 않습니다. (#12984)

### 버그 수정내역

* watchdog이 복구 중일 때, 조합키 추적(Control이나 Insert)이 보강됐습니다. (#12609)
* Windows 클린 설치와 같은 특정 시스템에서 NVDA 업데이트를 다시 한 번 확인할 수 있습니다. (#12729)
* Microsoft Word에서 NVDA가 표의 빈 셀을 UI automation 사용 중일 때 정상적으로 알립니다. (#11043)
* 웹의 ARIA 데이터 그리드 셀에서, ESC키가 그리드로 전달되며, 더 이상 어떤 상황에서든 포커스 모드가 꺼지지 않습니다. (#12413)
* Chrome에서 표 제목 셀을 읽을 때, 열 이름을 두번 읽는 문제가 수정됩니다. (#10840)
* NVDA는 값이 텍스트로 정의된 UIA 슬라이더에서 더 이상 숫자 값을 알리지 않습니다. (UIA의 RangeValuePattern보다 ValuePattern이 우선적으로 선호됩니다). (#12724)
* NVDA는 더 이상 슬라이더의 값을 백분율을 기준으로 다루지 않습니다.
* Windows11에서 Microsoft Excel을 UI Automation로 접근했을 때, 테이블 셀 위치 알림이 다시 정상 작동합니다. (#12782)
* NVDA가 더 이상 무효한 Python 로케일을 설정하지 않습니다. (#12753)
* 비활성 상태로 추가기능을 제거했다가 다시 해당 추가기능을 설치하면 활성화 상태로 설치됩니다. (#12792)
* addon 폴더에서 파일이 열려있거나 폴더명이 변경됐을 때 발생하는 업데이트, 제거 관련 버그가 수정되었습니다. (#12792, #12629)
* UI Automation으로 Microsoft Excel 스프레드시트 컨트롤에 접근하여 한 개의 셀을 선택했을 때 NVDA가 더 이상 내요을 중복해서 알리지 않습니다. (#12530)
* LibreOffice Writer에서 확인 대화상자와 같이 더 많은 대화상자 텍스트를 자동으로 읽습니다. (#11687)
* UI Automation와 함게 Microsoft Word를 브라우즈 모드로 읽고 탐색할 때, 현재 브라우즈 모드의 위치가 화면에서 보이는 한에서 항상 스크롤이 따라가며, 브라우즈 모드의 위치가 포커스 모드의 캐럿에 반영됩니다. (#9611)
* UI Automation과 함께 Microsoft Word에서 모두 읽기를 실행했을 때, 이제 문서가 자동으로 스크롤되며, 캐럿 위치가 읽었던 위치와 알맞게 업데이트 됩니다. (#9611)
* UI Automation으로 Outlook에서 이메일을 읽고 NVDA가 메시지에 접근할 때, 특정 테이블이 레이아웃 테이블로 표시됩니다. 즉 더 이상 기본으로 보고되지 않습니다. (#11430)
* 오디오 장치 변경 시 드물게 발생하던 오류가 수정되었습니다. (#12620)
* 편집 필드에서 점자 약자 테이블을 통한 입력이 안정적으로 동작합니다. (#12667)
* Windows 시스템 트레이 달력을 탐색할 때 NVDA는 전체 요일을 알립니다. (#12757)
* Microsoft Word에서 Taiwan - Microsoft Quick과 같은 중국어 입력 방법을 사용할 때 점자 디스플레이를 앞뒤로 잘못 스크롤해도 더 이상 원래 캐럿 위치로 계속 이동하지 않습니다. (#12855)
* UIA로 Microsoft Word 문서에 접근하고 있을 때, 문장 단위로 탐색하기(Alt + 아래 화살표 키 / Alt + 위 화살표 키)가 다시 가능합니다. (#9254)
* UIA가 활성화된 MS Word 문서를 탐색할 때 단락 들여쓰기를 알립니다. (#12899)
* UIA로 Microsoft Word에 액세스할 때 변경 추적 명령과 일부 다른 지역화된 명령이 Word에 보고됩니다. (#12904)
* name이나 content가 description과 일치 할 때의 중복된 점자 및 음성 출력을 수정됐습니다. (#12888)
* UIA가 활성화된 MS Word에서는 입력할 때 철자 오류 소리가 더 정확하게 들립니다. (#12161)
* Windows 11에서 NVDA는 Alt+Tab을 눌러 프로그램 간 전환할 때 더 이상 "창"을 알리지 않습니다. (#12648)
* UIA를 통해 문서에 액세스하지 않을 때 MS Word에서 새로운 Modern Comments 사이드 트랙 창이 지원됩니다. 사이드 트랙 창과 문서 사이를 이동하려면 Alt+f12를 누르십시오. (#12982)

### 개발 변경사항(영문)

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

이번 릴리즈는 Windows 11 지원을 위한 예비 지원이 도입됩니다.
Windows 11은 아직 출시되지 않았지만 이 릴리스는 Windows 11의 미리 보기 버전에서 테스트되었습니다.
또한 스크린 커튼에 대한 중요한 수정사항을 포함합니다(중요사항 섹션을 참고해주세요)
이번 릴리즈에 NVDA 실행중에 'COM Registration 재설정'으로 더 많은 문제를 해결할 수 있게 되었으며, 
eSpeak 음성엔진과 LibLouis 점역엔진에 대한 업데이트가 포함되었습니다.
또한 점자 지원과 Windows 터미널, 계산기, 이모지 패널, 클립보드 목록에 대한 다양한 버그 수정 및 개선이 이루어졌습니다.

### 중요사항

Windows 화면 확대 API의 변경으로 인해, 최신 Windows를 지원하기 위해서는 화면 커튼을 업데이트해야만 했습니다.
NVDA 2021.2에서 스크린커튼을 활성화하려면 Windows 10 21H2 또는 그 이상이 필요합니다.
이는 Windows 10 Insiders와 Windows 11을 포함합니다.
사생활을 보호하기 위해서, 윈도우의 새 버전을 사용할 때는 화면 커튼 기능이 화면을 완전히 검게 가리는지를 시각적으로 확인하십시오.

### 새로운 기능

* ARIA annotations에 대한 실험적인 지원:
  * aria-details가 있는 개체의 세부 정보 summary을 읽는 명령을 추가합니다. (#12364)
  * 브라우즈 모드에서 개체에 세부 정보가 있는 경우 알림 옵션을 고급 설정에 추가합니다. (#12439) 
* Windows 10 버전 1909 이상 (Windows 11 포함)에서 NVDA는 파일 탐색기에서 검색을 수행할 때 제안된 검색어 수를 알립니다. (#10341, #12628)
* Microsoft Word에서 NVDA가 들여쓰기와 내어쓰기 단축키 실행 시 결과를 알립니다. (#6269)

### 변경사항

* Espeak-ng가 1.51-dev commit `ab11439b18238b7a08b965d1d5a6ef31cbb05cbb`로 업데이트 되었습니다.. (#12449, #12202, #12280, #12568)
* 사용자 환경 설정 내 문서 서식 설정에서 아티클이 선택된 경우 NVDA는 콘텐츠 뒤에 "아티클"을 알립니다. (#11103)
* Liblouis 점역 엔진이 [3.18.0](https://github.com/liblouis/liblouis/releases/tag/v3.18.0)로 업데이트되었습니다. (#12526)
  * 새로운 점자 테이블 추가: Bulgarian grade 1, Burmese grade 1, Burmese grade 2, Kazakh grade 1, Khmer grade 1, Northern Kurdish grade 0, Sepedi grade 1, Sepedi grade 2, Sesotho grade 1, Sesotho grade 2, Setswana grade 1, Setswana grade 2, Tatar grade 1, Vietnamese grade 0, Vietnamese grade 2, Southern Vietnamese grade 1, Xhosa grade 1, Xhosa grade 2, Yakut grade 1, Zulu grade 1, Zulu grade 2
* Windows 10 OCR은 Windows OCR로 이름이 변경되었습니다. (#12690)

### 버그 수정내역

* Windows 10 계산기에서, NVDA는 점자 디스플레이에 계산 표현식을 표시합니다. (#12268)
* Windows 10 version 1607 이상의 터미널 프로그램에서 라인 중간에 문자를 삽입하거나 삭제할 때 오른쪽 캐럿 문자가 더 이상 읽히지 않습니다. (#3200)
  * Diff Match Patch는 이제 기본 값으로 활성화되었습니다. (#12485)
* The braille input works properly with the following contracted tables: Arabic grade 2, Spanish grade 2, Urdu grade 2, Chinese (China, Mandarin) grade 2. (#12541)
* COM Registration  수정 도구는 이제 64 bit Windows에서 더 많은 문제를 해결합니다. (#12560)
* Nippon Telesoft의 Seika Notetaker braille 장지의 버튼 처리가 개선되었습니다. (#12598)
* Windows emoji 패널 및 클립보드 기록 알림을 개선했습니다. (#11485)
* Bengali 알파벳 케릭터 설명을 업데이트하였습니다. (#12502)
* NVDA는 새로운 프로세스가 시작될 때 안전하게 종료됩니다. (#12605)
* 점자 디스플레이 선택 대화상자에서 Handy Tech 점자 디스플레이 드라이버를 다시 선택하면 더 이상 오류가 발생하지 않습니다. (#12618)
* Windows version 10.0.22000 이상은 Windows 10이 아닌 Windows 11로 인식됩니다. (#12626)
* 화면 커튼 지원은 Windows 버전 10.0.22000까지 문제가 수정되고 테스트되었습니다. (#12684)
* 입력 제스처를 필터링할 때 결과가 표시되지 않으면, 제스처 설정 대화상자가 예상데로 작동되도록 수정되었습니다. (#12673)
* 특정 컨텍스트 메뉴에서 서브메뉴의 첫 번째 메뉴항목이 알려지지 않는 문제가 수정되었습니다. (#12624)

### 개발 변경사항(영문)

* `characterProcessing.SYMLVL_*` constants should be replaced using their equivalent `SymbolLevel.*` before 2022.1. (#11856, #12636)
* `controlTypes` has been split up into various submodules, symbols marked for deprecation must be replaced before 2022.1. (#12510)
  * `ROLE_*` and `STATE_*` constants should be replaced to their equivalent `Role.*` and `State.*`.
  * `roleLabels`, `stateLabels` and `negativeStateLabels` have been deprecated, usages such as `roleLabels[ROLE_*]` should be replaced to their equivalent `Role.*.displayString` or `State.*.negativeDisplayString`.
  * `processPositiveStates` and `processNegativeStates` have been deprecated for removal.
* On Windows 10 Version 1511 and later (including Insider Preview builds), the current Windows feature update release name is obtained from Windows Registry. (#12509)
* Deprecated: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS` will be removed in 2022.1, there is no direct replacement. (#12544)

## 2021.1

이 버전은 Chromium 기반 브라우저와 Excel에서 선택 가능한 실험적인 UIA를 지원 기능을 포함합니다..
여러 언어 및 점자로 된 링크에 엑세스하기 위한 수정 사항이 있습니다.
eSpeak-NG와 LibLouis에 CLDR 유니코드와 수식기호 문자 업데이트가 있습니다.
많은 버그 수정과 개선이 Office, Visaul Studio, 그리고 몇몇 언어에 포함되었습니다.

참고:

* 추가기능은 다시 테스트되어야 하며, 추가기능의 manifast를 업데이트해야 합니다.
* 또한 이 버전에서는 Adobe Flash 지원을 종료하였습니다.

### 새로운 기능

* Chromium 기반 브라우저에 대한 UIA를 먼저 지원합니다. (Edge 등). (#12025)
* Excel에서 UI Automation을 통해 실험 기능을 선택적으로 지원합니다. 16.0.13522.10000 빌드 버전 이상의 Microsoft Excel만을 사용하기를 권장합니다. (#12210)
* Python 콘솔에서 결과를 탐색하기 쉬워졌습니다. (#9784)
  * Alt + 위/아래 화살표 키로 출력된 이전 또는 다음 결과값을 읽을 수 있습니다. (선택할 때는 Shift 키를 사용할 수 있습니다).
  * Control + I 키를 눌러 출력창을 깨끗이 정리할 수 있습니다.
* 이제 NVDA가 Microsoft Outlook(Microsoft 아웃룩)에서 약속에 할당된 범주를 보고합니다. (#11598)
* Nippon Telesoft의 Seika 점자 디스플레이를 지원합니다. (#11514)

### 변경 사항

* 브라우즈 모드 사용 중, 컨트롤은 이제 설명자에 점자 커서 라우팅을 사용하여 활성화할 수 있습니다 (예 "lnk", 링크). 레이블이 없는 체크박스를 활성화할 때 특히 유용합니다. (#7447)
* NVDA는 이제 화면 커튼이 켜진 상태에서 Windows 10 OCR를 사용할 수 없습니다. (#11911)
* 유니코드 Common Locale Data Repository (CLDR)가 39.0로 업데이트되었습니다. (#11943)
* 더 많은 수식 기호가 구두좀/기호 발음 사전에 추가되었습니다. (#11467)
* 사용 설명서, 변경 이력, NVDA 기능키 목록이 새로 고쳐졌습니다. (#12027)
* 이제 Microsoft Word 같이 화면 레이아웃을 지원하지 않는 프로그램에서 화면 레이아웃 기능을 전환을 시도하면 "지원 안 됨"을 알립니다. (#7297)
* 고급설정에 있는 '포커스 이벤트가 만료되면 발화를 중단합니다' 옵션은 이제 활성화(예)가 기본값으로 설정됩니다. (#10885)
  * 이 기능은 설정에서 "아니오"를 선택하여 비활성화할 수 있습니다.
  * 웹 애플리케이션 (E.G. Gmail) 포커스를 빠르게 이동할 때 더 이상 오래된 정보를 말하지 않습니다..
* Liblouis 점역 엔진이 [3.17.0](https://github.com/liblouis/liblouis/releases/tag/v3.17.0)로 업데이트되었습니다. (#12137)
  * 새로운 점자표: 벨라루스어 점자, 벨라루스어 컴퓨터 점자, 우르두어 1종, 우르두어 2종 점자 추가됨.
* Adobe가 를 사용하지 않아 Adobe Flash 컨텐츠에 대한 지원이 NVDA에서 제거되었습니다. (#11131)
* NVDA 종료 프로세스 중, NVDA의 대화상자, 창이 열려있으면 해당 창을 닫습니다. (#1740)
* 음성 출력 뷰어를 이제 `Alt+F4`로 닫을 수 있으며 포인팅 장치(예: 마우스) 사용자가 쉽게 상호 작용할 수 있는 표준 닫기 버튼이 추가되었습니다. (#12330)
* 점자 뷰어에 이제 포인팅 장치(예: 마우스) 사용자가 쉽게 상호작용할 수 있는 표준 닫기 버튼이 추가되었습니다. (#12328)
* "활성화" 버튼의 바로가기 키가 일부 로케일에서 제거되어 요소 유형의 라디오 버튼 라벨과 충돌하지 않도록 합니다. 사용 가능한 경우 버튼은 여전히 대화상자의 기본값이므로 요소 리스트 자체에서 Enter 키를 눌러 호출할 수 있습니다. (#6167)

### 버그 수정내역

* Outlook 2010의 메시지 목록을 다시 읽을 수 있습니다. (#12241)
* Windows 10 버전 1607 이상의 터미널 프로그램에서 줄 중간에 문자를 삽입하거나 삭제할 때 캐럿 오른쪽에 있는 문자를 더 이상 읽지 않습니다. (#3200)
  * 이 수정내용은 실험적인 것으로서, 직접 NVDA의 고급 설정 패털에 가서 diff 알고리듬을 Diff Match Patch로 바꾸어 활성화 시켜줘야 합니다.
* MS Outlook에서 Shift키와 Tab키를 눌러 메시지 본문에서 제목 창으로 이동할 때 부적절한 거리를 알려주는 (distance reporting) 문제가 수정되었습니다. (#10254)
* Python 콘솔에서, 비어있지 않은 줄의 맨처음에 Tab을 삽입해서 들여쓰기 하거나 입력된 행의 중간에서 Tab을 눌러 자동완성 하는 기능이 이제 지원됩니다. (#11532)
* 스크린 배치가 꺼져 있는 상태에서 양식 정보 등 브라우즈할 수 있는 메시지를 읽을 때 존재하지 않는 빈 줄을 읽지 않습니다. (#12004)
* 이제 MS 워드에서 UIA를 활성화한 채로 노트를 읽을 수 있습니다. (#9285)
* Visual Studio를 사용할 때의 성능이 향상되었습니다. (#12171)
* 오른쪽에서 왼쪽으로 읽어나가는 화면에서 NVDA를 사용할 때 요소를 빼먹는 등의 그래픽적인 버그가 수정되었습니다. (#8859) 
* GUI 배치의 방향성을 시스템 로케일 설정이 아닌 NVDA 언어에 기반하여 이해합니다. (#638)
  * 오른쪽에서 왼쪽으로 읽는 언어를 쓸 때의 버그: 레이블이나 입력양식이 상위 그룹의 오른쪽 모서리에 잘리는 현상 (#12181)
* Python 로케일이 설정에서 선택된 언어와 일관되게 일치하도록 설정되며, 기본 언어설정을 사용할 때에도 마찬가지입니다. (#12214)
* NVDA 로그 보기창 같은 Rich Edit 입력양식에서 TextInfo.getTextInChunks를 실행해도 다운되지 않습니다. (#11613)
* 윈도우즈 10 1803 버전과 1809 버전에서 de_CH 처럼 로케일 이름에 밑줄 문자(underscore)를 포함한 언어를 다시 쓸 수 있습니다. (#12250)
* WordPad에서 윗첨자나 아랫첨자를 보고하는 설정이 제대로 동작합니다. (#12262)
* 웹페이지에서 원래 있던 포커스가 사라졌다가 새로운 포커스가 같은 자리에 생겼을때 NVDA가 새로 포커스된 내용을 읽지 못하던 버그가 수정되었습니다. (#12147) 
* 해당 옵션이 활성화되어 있다면, 이제 엑셀에서 셀 전체에 적용된 취소선, 윗첨자, 아랫첨자를 알려줍니다. (#12264)
* 이동식 사본으로 설치를 하는 경우 대상 설정 폴더가 비어 있을 때 복사 설정을 수정했습니다. (#12071, #12205)
* "대문자 앞에 '대문자' 붙여 읽기" 옵션이 체크되어 있을 때 발음기호가 표시된 문자를 잘못 읽는 문제를 수정했습니다. (#11948)
* SAPI4 음성 합성기에서 높낮이 변화가 안 되는 문제를 수정했습니다. (#12311) 
* NVDA 설치관리자가 이제 설치된 NVDA나 이동식 NVDA 실행본과 마찬가지로 `--minimal` 명령어 변수를 인지하고 시작음을 내지 않습니다. (#12289)
* MS 워드나 Outlook에서, 브라우즈 모드 설정에 "레이아웃 테이블 포함" 옵션이 활성화되어 있다면 빠른 탐색 키로 레이아웃 표로 건너뛸 수 있습니다. (#11899)
* NVDA나 특정 언어에서 "↑↑↑"를 이모지로 읽는 문제가 수정되었습니다. (#11963)
* Espeak가 다시 광동어와 표준 중국어를 지원합니다. (#10418)
* 새로 발표된 Chromium 기반의 Microsoft Edge에서, 주소 창 같은 입력란이 비어있을 경우 이제 이를 알려줍니다. (#12474)
* Seika 점자 드라이버를 고쳤습니다. (#10787)

### 개발 변경사항(영문)

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

이 버전은 새로운 중국어 입력 방법과 Liblouis를 위한 업데이트, 그리고 요소목록(NVDA+F7)이 이제 포커스 모드에서 동작합니다.
NVDA 창에서 F1을 눌러서 그 창에 대한 도움말을 얻는 기능이 추가됐습니다.
기호에 대한 발음, 음성 사전, 점자 메시지, 건너뛰어 읽기 기능이 개선됐습니다.
메일, 아웃룩, Teams, Visual Studio, Azure Data Studio, Foobar2000에 대한 버그가 수정되고 개선됐습니다.
웹 기능에서 Google Docs을 쓸 때의 기능이 개선됐으며, ARIA를 더 많이 지원합니다.
그 외에도 많은 버그 수정과 기능 개선이 있습니다.

### 새로운 기능

* NVDA의 윈도우에서 F1을 누르면 그 상황에 가장 부합하는 도움말 파일을 엽니다. (#7757)
* Microsoft SQL Server Management Studio와 Visual Studio 2017 이후 버전에서의 자동완성 기능(IntelliSense)을 지원합니다. (#7504)
* 기호에 대한 발음: 복잡한 기호 정의에서 그룹 기능을 지원하고, 바꾸기 규칙에서 그룹을 설정할 수 있게 되어 보다 간단하고 강력해졌습니다. (#11107)
* 사용자가 잘못된 정규식 교환조건으로 음성사전에 새 항목을 만드려고 하면 알려줍니다. (#11407)
  * 특히, 이제 그룹 오류를 감지합니다.
* 윈도우 10에서 새로운 중국어 입력방식 Traditional Quick and Pinyin을 지원합니다. (#11562)
* 빠른 탐색 키 F 를 쓰면 이제 탭 헤더가 폼 필드로 인식됩니다. (#10432)
* 표시된 (강조된) 문구를 알려주는 기능을 토글하는 항목이 추가됐습니다. 기본 제스처는 설정되지 않았습니다. (#11807)
* NVDA를 음성안내 없이 설치할 때 자동으로 제공된 설정을 사용자 계정으로 복사하는 --copy-portable-config 변수가 추가됐습니다. (#9676)
* 마우스 사용자가 점자 뷰어를 사용할 때에도 점자 라우팅이 지원됩니다. 점자 셀로 라우트하려면 마우스 커서를 올리세요. (#11804)
* NVDA가 이제 자동으로 Humanware Brailliant BI 40X와 20X 장비와 USB 및 블루투쓰로 통신합니다. (#11819)

### 변경사항

* Liblouis 점역기가 버전 3.16.1으로 업데이트되었습니다.:
 * 여러 충돌 문제 수정
 * 바슈키르어 grade 1 점자 테이블 추가
 * 콥트어 8점 컴퓨터 점자 테이블 추가
 * 러시아 정자 점자와 러시아 정자(상세) 점자표 추가.
 * 아프리칸스어 grade 2 점자 테이블 추가
 * 러시아어 grade 1 점자 테이블 제거
* 브라우즈 모드에서 모두 읽기 사용 도중에 모두 읽기 사용 시 건너뛰어 읽기 사용 설정이 활성화되어있다면 이전 또는 다음 탐색이 더 이상 모두 읽기를 중지하지 않습니다. (#11563)
* HIMS 점자 디스플레이에서 F3이 스페이스 + 148점으로 리매핑되었습니다. (#11710)
* "알림 메시지 출력 시간"과 "점자 메시지를 영구적으로 표시" 옵션에 대한 UX가 개선되었습니다.. (#11602)
* 웹브라우저와 브라우즈 모드를 지원하는 응용 프로그램에서 요소 목록 대화상자 (NVDA+F7)를 포커스 모드에서 불러올 수 있습니다. (#10453)
* 자동 변경 내용 알림이 해제되었을 때 ARIA 라이브 영역의 업데이트 내용을 알리지 않습니다. (#9077)
* NVDA가 복사된 텍스트를 읽기 전에 "클립보드에 복사됨"을 읽습니다. (#6757)
* 디스크 관리의 그래픽으로 보기 테이블의 안내가 개선되었습니다. (#10048)
* 컨트롤 요소가 비활성화일 때, 컨트롤 요소의 레이블이 비활성화되며 흐리게 표시됩니다. (#11809)
* CLDR emoji annotation의 버전이 38로 업데이트되었습니다.. (#11817)
* 내장된 "포커스 표시" 기능이 "시각적 표시"로 변경되었습니다. (#11700)

### 버그 수정내역

* Fast Log Entry 애플리케이션을 사용할 때 편집 영역에서 NVDA가 제대로 동작하도록 수정됐습니다. (#8996)
* Foobar2000 에서 생방송 스트림의 경우와 같이 전체 재생시간이 없는 경우, 재생된 시간을 대신 알려줍니다. (#11337)
* 웹페이지에서 편집 가능한 내용 안에 포함된 요소들에 대해서, aria-roledescription 속성을 제대로 다루도록 수정됐습니다. (#11607)
* Google Chrome 에서 Google Docs 나 다른 편집 가능한 내용을 읽을 때 목록의 모든 항목마다 '목록'이라고 말하지 않게 수정됐습니다. (#7562)
* 웹사이트의 편집 가능한 내용에 포함된 목록에서 문자나 단어 단위로 항목 사이를 이동할 때, 새 목록 항목으로 들어간다는 것을 알려줍니다. (#11569)
* Google Docs 나 다른 편집 가능한 웹 요소에서, 목록 항목 끝에 위치한 링크 끝으로 캐럿을 옮겼을 때 올바른 줄을 읽습니다. (#11606)
* Windows 7의 바탕화면에서 메뉴를 열고 닫았을 때의 초점이 올바르게 설정되었습니다. (#10567)
* 포커스 이벤트 만료 시 발화 중단이 켜져있을 때, Firefox에서 탭을 전환할 때 탭의 제목을 다시 알립니다. (#11397)
* SAPI 5 Ivona 음성을 쓰면서 목록을 편집할 때, 제대로 목록 항목을 알려주도록 수정됐습니다. (#11651)
* Windows 10 Mail 앱 버전 16005.13110 이상에서 이메일을 읽을 때 이제 다시 브라우즈 모드를 사용할 수 있습니다. (#11439)
* NVDA 에서 harposoftware.com 에서 만든 SAPI 5 Ivona 음성을 쓸 때, 이제 설정 내용을 저장하고 음성합성기를 바꿀 수 있습니다. 또한 재시작한 후에 조용해지는 문제를 해결했습니다. (#11650)
* HIMS 디스플레이 장치에서 점자 키보드로 컴퓨터 점자 숫자 6을 입력할 수 없었던 문제가 수정됐습니다. (#11710)
* Azure Data Studio 사용 시 성능이 향상되었습니다. (#11533, #11715)
* "포커스 이벤트 만료 시 발화 중단"이 켜져있을 때, NVDA 찾기 대화상자의 제목을 다시 읽습니다. (#11632)
* 컴퓨터를 켤 때 Microsoft Edge 문서에 포커스가 있으면 동작을 멈추는 문제가 수정됐습니다. (#11576)
* Microsoft Edge에서 컨텍스트 메뉴를 닫은 후 브라우즈 모드를 다시 활성화하려면 Microsoft Edge에서 더 이상 탭을 누르거나 포커스를 이동할 필요가 없습니다. (#11202)
* NVDA가 Tortoise SVN와 같은 64-bit 응용프로그램에서, 목록 보기 항목을 읽는 것에 실패하지 않습니다. (#8175)
* 이제 Firefox와 Google Chrome 모두 ARIA의 트리그리드 요소를 일반 테이블로 안내합니다. (#9715)
* "현재 커서 위치 이전부터 입력된 문자열을 검색" 기능을 기본적으로 NVDA+shift+F3로 사용할 수 있습니다. (#11770)
* NVDA 스크립트가 연달아 실행되는 사이에 관련 없는 키 입력을 있을 경우, 반복되는 스크립트로 다루어지는 문제가 수정됐습니다. (#11388)
* Internet Explorer에서 Strong과 emphasis 태그의 알림을 문서 서식 알림 설정의 글꼴 섹션 안에 있는 "강조" 설정값을 해제하여 다시 안내되지 않도록 할 수 있습니다. (#11808)
* 화살표 키로 셀 간 탐색할 때 일부 유저가 경험했던 몇 초 동안 멈추던 현상이 발생하지 않습니다. (#11818)
* 1.3.00.28 으로 시작하는 버전의 Microsoft Teams 에서, 메뉴 포커스가 올바르지 않다고 해서 NVDA가 채팅이나 팀 채널의 메시지를 못 읽는 문제가 해결했습니다. (#11821)
* Google Chrome 에서 철자 오류와 문법 오류가 함께 표시된 문구에서, NVDA 가 철자와 문법 오류를 둘 다 알려주도록 변경됐습니다. (#11787)
* 프랑스어 로케일 환경에서 Outlook을 사용할 때, '전체 답장' 단축키(control+shift+R)가 다시 작동합니다. (#11196)
* Visual Studio에서 현재 선텍된 IntelliSense 목록 항목의 툴팁을 이제 한 번만 읽습니다. (#11611)
* Windows 10 계산기에서 입력한 글자 알림을 끄면 계산 진행 내용을 NVDA가 안내하지 않습니다. (#9428)
* 커서 위치 단어 정자로 보기 설정이 켜져있고, 영어 (미국) 2종을 사용하는 환경에서 점자로 URL과 같은 특정 콘텐츠를 표시할 때, NVDA가 더 이상 충돌하지 않습니다. (#11754)
* Excel 셀에서 NVDA+F 키를 사용하여 "서식 정보 알림"을 사용할 수 있습니다. (#11914)
* Papenmeier 점자 디스플레이의 QWERTY 입력이 다시 작동하며 더 이상 NVDA가 무작위로 멈추지 않습니다. (#11944)
* Chromium 기반 브라우저에서 표 탐색이 작동하지 않고 NVDA가 표의 행/열 수를 알리지 않는 여러 경우가 해결되었습니다. (#12359)

### 개발 변경사항(영문)

* System tests can now send keys using spy.emulateKeyPress, which takes a key identifier that conforms to NVDA's own key names, and by default also blocks until the action is executed. (#11581)
* NVDA no longer requires the current directory to be the NVDA application directory in order to function. (#6491)
* The aria live politeness setting for live regions can now be found on NVDA Objects using the liveRegionPoliteness property. (#11596)
* It is now possible to define separate gestures for Outlook and Word document. (#11196)

## 2020.3

이 버전에서는 특히 Microsoft Office 어플리케이션에서의 안정성과 성능이 몇가지 점에서 크게 향상되었습니다. 터치스크린 사용을 지원하고 그래픽 내용을 알려주는 기능을 켜고 끌 수 있는 새로운 설정 항목이 생겼습니다.
브라우저에서 표시된 (강조된) 내용이 있다면 알려주도록 했으며, 독일어 점자를 위한 데이터가 추가되었습니다.

### 새로운 기능

* NVDA의 문서 서식 설정에서 그래픽 알림 기능을 켜고 끌 수 있습니다. 이 기능을 비활성화해도 그래픽의 대체 텍스트는 읽어줍니다. (#4837)
* NVDA의 터치스크린 사용 지원을 켜고 끌 수 있습니다. 이 항목은 NVDA의 설정 중 "터치 사용 지원" 패널에 추가되었으며, 기본 제스처는 NVDA + Control + Alt + T 입니다. (#9682)
* 새로운 독일어 점자 데이터가 추가되었습니다. (#11268)
* 읽기 전용 텍스트에 대한 UIA 컨트롤을 인식합니다. (#10494)
* 모든 웹브라우저에서 표시된 (강조된) 내용이 있을 경우 말과 점자 두 방법 모두를 통해 알려줍니다. (#11436)
  * 이 기능은 새로 추가된 NVDA의 문서 서식 항목을 통해서 켜고 끌 수 있습니다.
* 입력 제스처 창에서 모방할 시스템 키보드 입력을 추가할 수 있습니다. (#6060)
  * 이 기능을 사용하려면 시스템 키보드 입력 모방 그룹을 선택한 후에 추가 버튼을 누르세요.
* Handy Tech Active Braille을 이제 조이스틱과 함께 사용할 수 있습니다. (#11655)
* "자동으로 포커스 가능한 요소에 시스템 포커스 이동" 항목이 비활성화되어 있을때에도 "캐럿 이동 시 자동 포커스 모드 전환" 설정을 사용할 수 있습니다. (#11663)

### 변경사항

* 글자 서식 알림(NVDA+F)이 리뷰 커서 위치가 아닌 시스탬 캐럿을 기준으로 텍스트 서식을 알리도록 변경되었습니다. 기존의 리뷰 커서 위치의 텍스트 서식 알림을 들으려면 NVDA+Shift+F를 사용합니다.
* 성능 및 안정성 향상을 위해 NVDA의 브라우즈 모드에서 더 이상 기본적으로 초점을 받을 수 있는 요소에 자동으로 초점을 보내지 않습니다. (#11190)
* CLDR의 버전이 36.1 에서 37 버전으로 업데이트되었습니다. (#11303)
* eSpeak-NG 음성엔진 버전이 1.51-dev 버전으로 업데이트 되었습니다, commit 1fb68ffffea4
* 선택할 수 있는 목록 항목을 가진 목록상자가 여러 개의 열을 갖고 있을 경우, 이제는 표 내비게이션을 사용할 수 있습니다. (#8857)
* 이제 추가 기능 관리에서 추가 기능 제거 확인을 위한 대화상자 창이 표시될 때, "아니오" 버튼에 기본 초점이 제공됩니다. (#10015)
* Microsoft Excel에서 요소목록 대화상자의 수식을 선택된 지역의 형식에 맞춰 출력합니다. (#9144)
* NVDA는 이제 MS Excel의 메모에서 올바른 용어를 사용해서 알려줍니다. (#11311)
* 브라우즈 모드에서 "포커스된 객체로 이동"명령을 사용하면, 이제 리뷰 커서가 가상 캐럿 위치에 설정됩니다. (#9622)
* 이제 브라우즈 모드에서 NVDA+F를 두 번 눌러 서식 정보를 볼 때 화면 중앙에 조금 더 큰 창으로 표시됩니다. (#9910)

### 버그 수정내역

* NVDA가 단어별로 읽기로 설정되어 있고 뒤에 공백이 있는 심볼에 다다르면, 읽기수준 설정에 상관없이 항상 알려줍니다. (#5133)
* QT 5.11 이상의 버전을 사용하는 응용 프로그램에서 객체 설명을 다시 알립니다. (#8604)
* 이제 ctrl + delete 키로 단어 단위로 글자를 지웠을 때 침묵하지 않습니다. (#3298, #11029)
  * 이제 지워진 단어의 오른쪽에 있는 단어를 알립니다.
* 일반 설정 패널에서 언어 목록의 순서가 올바르게 재정렬되었습니다. (#10348)
* 제스처 설정 대화상자에서 명령 검색 중 성능이 향상되었습니다. (#10307)
* 이제 점자 디스플레이에서 U+FFFF 이상의 유니코드 문자를 보낼 수 있습니다.. (#10796)
* 윈도우즈 10 2020년 5월 업데이트에서 "다른 프로그램으로 열기" 대화상자의 내용을 읽습니다. (#11335)
* 고급 설정에 새로 소개된 실험적인 선택항목 "UIA 이벤트와 속성 변화를 일부 적용"을 활성화하면, Microsoft Visual Studio 및 UIAutomation을 사용하는 다른 어플리케이션에 주요한 성능향상이 있을 수 있습니다. (#11077, #11209)
* 체크 가능한 목록 항목의 경우 선택한 상태가 더 이상 중복으로 알리지 않으며, 선택되지 않은 상태를 알립니다. (#8554)
* 2020년 5월 업데이트가 적용된 Windows 10에서 NVDA의 음성엔진 선택 대화상자의 음성 출력 장치 콤보상자 목록으로 Microsoft Sound Mapper가 표시됩니다. (#11349)
* Internet Explorer에서 순서 있는 목록 중, 목록이 1로 시작되지 않는 목록에 대한 숫자 블릿을 올바르게 읽습니다. (#8438)
* Google Chrome에서 선택되지 않은 상태의 체크 가능한 컨트롤에 "해제됨" 상태를 제공합니다(체크상자와 유사한 모든 요소). (#11377)
* NVDA의 언어가 아라곤어로 설정됐을 때 다양한 UI를 사용하는 것이 다시 가능해졌습니다. (#11384)
* Microsoft Word에서 화살표 키를 위 아래로 빠르게 반복 입력하거나, 점자 입력이 활성화된 상태로 문자를 입력할 때 NVDA가 더 이상 멈추지 않습니다. (#11431, #11425, #11414)
* 선택한 탐색 객체를 클립보드로 복사할 때, 더 이상 존재하지도 않는 공백문자를 끝에 추가하지 않습니다. (#11438)
* 읽을 내용이 없으면 NVDA는 더 이상 'Say All' 프로필을 활성화하지 않습니다. (#10899, #9947)
* NVDA가 Internet Information Services (IIS) 관리자에서 기능 목록을 읽지 못했던 버그가 수정됐습니다. (#11468)
* NVDA가 이제 사운드 장치를 열어둔 채로 두어 일부 사운드카드에서의 성능을 향상시킵니다. (#5172, #10721)
* Microsoft Word에서  'ctrl+shift+아래 화살표 키'를 길게 눌러도 더 이상 NVDA가 멈추거나 종료되지 않습니다. (#9463)
* Google Drive(drive.google.com)의 탐색 트리뷰에 있는 경로의 확장/축소 상태를 NVDA가 항상 알립니다. (#11520)
* eReader Humanware 점자 디스플레이가 블루투스를 통해서 NVDA에 연결하면 이제 "NLS eReader Humanware"라는 이름으로 자동 인식합니다. (#11561)
* Visual Studio Code에서의 주요 성능이 개선되었습니다. (#11533)

### 개발 변경사항(영문)

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

이 릴리즈의 주요 변경사항으로는 새로 나온 Nattiq 점자 디스플레이 지원, 그리고 ESET 안티바이러스 제품의 GUI, 윈도우 터미널, 1Password의 성능 개선, 윈도우 OneCore 음성합성기의 연동성능 개선 등입니다. 이외에도 다른 중요한 버그 수정과 개선이 포함되어 있습니다.

### 새로운 기능

* 새로운 점자 디스플레이 지원
  * Nattiq nBraille (#10778)
* NVDA 설정 디렉토리를 여는 스크립트 추가 (디폴트 제스처 없음) (#2214)
* ESET 안티바이러스의 GUI 지원을 개선 (#10894)
* 윈도우 터미널 지원을 추가 (#10305)
* 선택되어 있는 설정 프로필을 알려주는 명령 추가 (디폴트 제스처 없음) (#9325)
* 위첨자와 아래첨자를 알려주는 기능을 켜고 끄는 명령 추가 (디폴트 제스처 없음) (#10985)
* 웹 어플리케이션(예: 지메일)에서 포커스를 빨리 움직일 때 정보가 업데이트되지 않는 문제가 해결되었습니다 (#10885)
  * 이 항목은 실험적으로 수정된 것으로, 고급설정 패널에서 "포커스 이벤트가 만료되면 음성합성 중지" 설정을 이용해서 직접 활성화해야 합니다.
* 기본 심볼 사전에 심볼이 아주 많이 추가되었습니다. (#11105)

### 변경사항

* Liblouis 점자 번역기가 3.12.0에서 [3.14.0](https://github.com/liblouis/liblouis/releases/tag/v3.14.0)로 업데이트되었습니다. (#10832, #11221)
* 위첨자와 아래첨자 알림 기능이 이제 글꼴 속성 알림 기능과 분리되어 조절됩니다. (#10919)
* VS Code의 기능 변동으로 인해 더 이상 브라우즈 모드를 자동으로 비활성화하지 않습니다. (#10888)
* 리뷰 커서를 현재 네비게이터 객체의 첫번째나 마지막 줄로 옮길 때 안내되던 "맨 위"나 "맨 아래" 메시지를 없앴습니다. (#9551)
* 리뷰 커서를 현재 네비게이터 객체의 첫번째나 마지막 문자로 옮길 때 안내되던 "왼쪽"나 "오른쪽" 메시지를 없앴습니다. (#9551)

### 버그 수정내역

* 로그 파일을 생성할 수 없을 경우에도 NVDA가 정상적으로 실행됩니다. (#6330)
* Microsoft Word 365의 최근 릴리즈에서 문서를 편집하던 중에 Control + Backspace를 누르면 NVDA가 "삭제 뒤로가기"라고 말하는 버그가 수정되었습니다. (#10851)
* 윈앰프에서 셔플 및 반복의 토글 상태를 다시 알립니다. (#10945)
* 1Password에서 목록 사이를 움직일 때 극단적으로 느려지는 버그가 수정되었습니다. (#10508)
* 윈도우 OneCore 음성합성기에서 발화 사이에 느려지던 현상이 수정되었습니다. (#10721)
* 시스템 알림 영역에서 1Password의 컨택스트 메뉴를 열었을 때 NVDA가 멈추는 현상이 수정되었습니다. (#11017)
* Office 2013과 그 이전버전에서:
  * 포커스가 리본 메뉴로 처음 옮겨갔을 때 알려줍니다. (#4207)
  * 컨택스트 메뉴 항목을 다시 정상적으로 알려줍니다. (#9252)
  * 리본 영역을 Control + 화살표키로 사용할 때 일관되게 알려줍니다. (#7067)
* 모질라 FireFox와 구글 Chrome에서 브라우즈 모드일 때, 웹 콘텐트의 CSS에 display: inline-flex가 적용되면 다른 줄에 문자가 잘못 나타나는 문제가 수정되었습니다. (#11075)
* 브라우즈 모드에서 자동으로 시스템 포커스 이동 옵션이 비활성화되어 있을 경우, 포커스되지 않는 요소를 활성화하는 게 가능해졌습니다.
* 브라우즈 모드에서 자동으로 시스템 포커스 이동 옵션이 비활성화되어 있을 경우, 탭 키를 눌러 요소를 선택해 활성화하는 게 가능해졌습니다. (#8528)
* 브라우즈 모드에서 자동으로 시스템 포커스 이동 옵션이 비활성화되어 있을 경우, 요소를 활성화시킬 때 정확하지 않은 곳에 클릭이 발생하는 현상이 수정됐습니다. (#9886)
* DevExpress text controls 를 열 때 NVDA 오류 효과음이 들리는 버그가 수정됐습니다. (#10918)- 시스템 트레이에서 아이콘의 이름과 툴팁 내용이 같을 경우, 이름을 두 번 알리지 않기 위해서 이제 툴팁을 읽지 않습니다. (#6656)
* 시스템 트레이에 있는 아이콘의 텍스트가 아이콘의 이름과 같으면 키보드 탐색 시 중복 알림을 피하기 위해 툴팁이 더 이상 보고되지 않습니다. (#6656)
* 브라우즈 모드에서 자동으로 시스템 포커스 이동 옵션이 비활성화되어 있을 경우, NVDA+Space 키를 눌러 포커스 모드로 바꾸면 캐럿 아래에 있는 요소를 포커스합니다. (#11206)
* 일부 시스템에서 NVDA 업데이트를 다시 확인할 수 있게 됐습니다. (예: 초기 설치된 윈도우즈) (#11253)
* 자바 어플리케이션의 포커스되지 않은 트리, 테이블, 목록 등에서 선택항목이 바뀔 때 포커스가 바뀌는 문제가 수정됐습니다. (#5989)

### 개발 변경사항(영문)

* execElevated and hasUiAccess have moved from config module to systemUtils module. Usage via config module is deprecated. (#10493)
* Updated configobj to 5.1.0dev commit f9a265c4. (#10939)
* Automated testing of NVDA with Chrome and a HTML sample is now possible. (#10553)
* IAccessibleHandler has been converted into a package, OrderedWinEventLimiter has been extracted to a module and unit tests added (#10934)
* Updated BrlApi to version 0.8 (BRLTTY 6.1). (#11065)
* Status bar retrieval may now be customized by an AppModule. (#2125, #4640)
* NVDA no longer listens for IAccessible EVENT_OBJECT_REORDER. (#11076)
* A broken ScriptableObject (such as a GlobalPlugin missing a call to its base class' init method) no longer breaks NVDA's script handling. (#5446)

## 2020.1

이 릴리스의 주요 특징으로는 HumanWare 및 APH의 여러 가지 새로운 점자 디스플레이 지원과 MathPlayer / MathType을 사용하여 Microsoft Word에서 수학을 다시 읽을 수 있는 기능과 같은 기타 중요한 버그 수정이 포함됩니다.

### 새로운 기능

* NVDA 2019.1과 유사하게 목록상자에서 현재 선택된 항목이 Chrome에서 브라우즈 모드로 다시 표시됩니다. (#10713)
* 이제 한 손가락으로 길게 눌러 터치 장치에서 마우스 오른쪽 버튼 클릭을 수행할 수 있습니다. (#3886)
* 새로운 점자 디스플레이 지원: APH Chameleon 20, APH Mantis Q40, HumanWare BrailleOne, BrailleNote Touch v2, 및 NLS eReader. (#10830)

### 변경사항

* NVDA는 모두 읽기 시 시스템이 잠기거나 절전 모드 상태가 되는 것을 방지합니다. (#10643)
* Mozilla Firefox에서 out-of-process iframe을 지원합니다. (#10707)
* 점자 번역기 Liblouis를 3.12 버전으로 업데이트했습니다. (#10161)

### 버그 수정내역

* NVDA가 유니코드 빼기 기호 (U+2212)를 알리지 않는 문제가 수정되었습니다. (#10633)
* 추가 기능 관리자에서 추가 기능을 설치할 때 찾아보기 창의 파일 및 폴더 이름이 더 이상 두 번 알려지지 않습니다. (#10620, #2395)
* Firefox에서 고급 웹 인터페이스가 활성화된 상태에서 Mastodon을 로드할 때 이제 모든 타임라인이 브라우즈 모드에서 올바르게 렌더링됩니다. (#10776)
* 브라우즈 모드에서 선택되지 않은 체크상자의 "해제됨"를 알리지 않을 수 있는 문제를 수정했습니다. (#10781)
* ARIA 스위치 컨트롤은 더 이상 "눌리지 않음 선택됨"또는 "누른 선택됨"과 같은 혼동되는 정보를 알리지 않습니다. (#9187)
* SAPI4 음성 사용 시 일부 텍스트를 읽지 않던 문제를 수정했습니다. (#10792)
* NVDA는 다시 Microsoft Word에서 수학 방정식을 읽고 상호작용할 수 있습니다. (#10803)
* 브라우즈 모드에서 텍스트를 선택한 상태에서 화살표 키를 누르면 NVDA는 텍스트가 선택 해제되었음을 다시 알립니다. (#10731)
* eSpeak 초기화 오류가 발생하면 NVDA가 더 이상 종료되지 않습니다. (#10607)
* 바로 가기 키 번역에서 유니코드로 인한 오류가 더 이상 영어 텍스트로 인해 실패하여 NVDA 설치 프로그램을 중지하지 않습니다. (#5166, #6326)
* 모두 읽기 시 건너뛰어 읽기가 활성화된 상태에서 방향키로 목록 및 테이블을 벗어났을 때 더 이상 목록 또는 테이블 종료 메시지를 반복적으로 알리지 않습니다. (#10706)
* Internet Explorer에서 일부 MSHTML 요소의 마우스 추적 문제가 해결되었습니다. (#10736)

### 개발 변경사항(영문)

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

NVDA 2019.3 버전은 내부적으로 많은 변화가 포함된 중요한 버전입니다. 이 버전은 파이썬 버전이 2에서 3으로 업그레이드되었으며, NVDA의 음성 서브시스템에도 주요한 재작업이 포함되어 있습니다.
이런 변화들이 기존의 NVDA 추가 기능에 대한 호환성 문제를 일으키기는 합니다. 하지만 파이썬 3으로의 업그레이드는 보안 개선은 물론, 조만간 벌어질 흥미로운 혁신을 위한 음성 시스템의 변화를 위해 필요한 작업입니다.
그 외에도 이번 버전은 Java VM 에 대한 64비트 지원, 스크린 가리기 기능과 포커스 강조 기능, 점자 디스플레이 및 새로운 점자표시 장치 추가 지원, 그리고 수많은 버그 수정 등의 주요 변경 사항을 포함하고 있습니다.

### 새로운 기능

* Java 응용프로그램의 텍스트 필드에서 탐색 객체 마우스로 이동 기능의 정확성 향상 (#10157)
* 다음 Handy Tech 점자 디스플레이 제품군을 추가 지원 (#8955):
 * Basic Braille Plus 40
 * Basic Braille Plus 32
 * Connect Braille
* 제스처 설정 대화상자에 새로 추가된 <기본 환경설정으로 초기화> 버튼으로 사용자가 변경한 제스처 설정의 모든 값을 기본값으로 초기화할 수 있음. (#10293)
* Microsoft Word에서의 글꼴 알림 중 숨겨진 텍스트 알림이 추가됩니다. (#8713)
* 리뷰커서의 현재 위치를 텍스트 선택 또는 복사할 시작 지점으로 설정하는 단축키: NVDA+shift+F9 가 추가됨. (#1969)
* Internet Explorer, Microsoft Edge, Google Chrome과 Mozilla Firefox의 최근 버전에서 포커스 모드와 객체 탐색을 사용할 때도 랜드마크를 읽도록 함. (#10101)
* Internet Explorer, Google Chrome, Mozilla Firefox에서 빠른 탐색 단축키로 아티클 랜드마크와 그룹을 탐색할 수 있음. 해당 빠른 탐색 단축키는 기본값으로 할당되어 있지 않으며, 제스처 설정 대화상자 목록에서 브라우즈 모드 목록을 통해 단축키를 할당할 수 있음. (#9485, #9227)
 * Figure 요소 또한 탐색이 가능합니다. figure 요소는 객체로 취급되므로 객체 단위 빠른 탐색 키 ' o ' 키를 통해 탐색할 수 있습니다.
* Internet Explorer, Google Chrome, Mozilla Firefox에서 객체 탐색 사용 시 아티클 요소를 읽으며 브라우즈 모드에서는 선택적으로 설정할 수 있음. (#10424)
* 화면 커튼 기능이 추가됨, 활성화할 경우, 전체화면을 검정색으로 가릴 수 있음(Windows 8 이상). (#7857)
 * 화면 커튼 활성화 제스처(한 번 눌러 NVDA 다음 재시작까지 활성화하기, 또는 두 번 눌러 NVDA가 실행 중일 때 항상 활성화하기)가 추가되었습니다. 이 단축키는 기본으로 할당되어있지 않습니다.
 * 화면 커튼 기능은 NVDA의 설정 대화상자의 시각 보조 카테고리에서 설정할 수 있습니다.
* 화면 하이라이트 기능이 NVDA에 추가됨. (#971, #9064)
 * 포커스, 탐색 객체, 그리고 브라우즈 모드의 커서 위치의 강조 기능은 NVDA 설정 대화상자의 '시각 보조' 카테고리에서 활성화하고 설정할 수 있습니다.
 * 참고: 이 기능은 focus highlight 추가 기능과 함깨 사용할 수 없습니다, 그러니 해당 추가 기능을 유지하려면 이 기능을 비활성화 하십시오.
* 점자 뷰어 기능이 추가됨, 화면을 통해 점자 출력을 볼 수 있음. (#7788)

### 변경사항

* 이제 사용자 가이드에서 'Windows 콘솔에서 NVDA 사용하는 방법'을 설명합니다. (#9957)
* nvda.exe 을 실행하면 앞서 실행 중이던 NVDA를 대체하는 방식을 기본 설정으로 바꾸었습니다. -r 혹은 --replace 명령어 파라미터는 여전히 사용할 수 있지만, 실제로는 아무 효력이 없게 됩니다. (#8320)
* 윈도우즈 8 혹은 그 이후의 버전에서, NVDA 는 이제 Microsoft 스토어에서 다운로드 받은 앱들처럼 온라인 서버를 통해서 운용되는 제품의 이름과 버전 정보를 알려줍니다. 이 정보는 앱에서 제공하는 정보를 바탕으로 합니다. (#4259, #10108)
* Microsoft Word에서 키보드로 변경 내용 추적을 켜고 끌 때 NVDA가 설정 상태를 알림 (#942) 
* NVDA 버전 숫자가 앞으로는 로그 파일의 첫번째 문구로 기록됩니다. 이는 GUI에서 로그 기록이 비활성화된 경우에도 해당합니다. (#9803)
* 명령어를 통해 설정한 로그 기록 수준을 설정 대화상자에서 바꿀 수 없습니다. (#10209)
* Microsoft Word를 사용할 때, 인쇄되지 않는 문자의 표시 상태를 알려줍니다. Ctrl+Shift+8 를 눌러서 켜고 끌 수 있습니다. (#10241)
* 점자 번역기 Liblouis를 commit 58d67e63 으로 업데이트했습니다. (#10094)
* CLDR 문자(이모지 포함)에 대한 알림 기능이 활성화되어 있으면, 모든 수준의 문장부호를 알려 줍니다. (#8826)
* Comtypes 같이 외부에서 개발되어 NVDA에 포함된 파이썬 패키지도 경고나 에러 기록을 NVDA 로그에 저장합니다. (#10393)
* 유니코드 협회의 국제 표기양식 기록원(CLDR)에서 정한 이모지의 문자 정보를 36.0 버전으로 업데이트했습니다. (#10426)
* 브라우즈 상태에서 그룹에 포커스를 뒀을 때, 그룹에 대한 설명 정보도 함께 읽습니다. (#10095)
* Java Access Bridge가 이제 NVDA에 포함되어 Java 어플리케이션에 접근할 수 있게 됩니다. 여기에는 64비트 Java VM 도 포함됩니다. (#7724)
* 사용자 시스템에서 Java Access Bridge가 활성화되어 있지 않은 경우, NVDA가 시작할 때 자동적으로 이를 활성화시킵니다. (#7952)
* eSpeak-NG 모듈을 1.51-dev 로 업데이트했습니다. Commit ID는 ca65812ac6019926f2fbd7f12c92d7edd3701e0c 입니다. (#10581)

### 버그 수정내역

* 이모지 및 다른 32비트 유니코드 문자들이 16진수 형식을 사용할 경우 점자 디스플레이에서 차지하는 공간을 줄였습니다. (#6695)
* 객체 표시 대화상자에서 도구설명 알림이 켜져있다면, 윈도우즈 10에서 동작하는 유니버설 앱의 도구설명을 읽습니다. (#8118)
* 윈도우즈 10 Anniversary Update 혹은 그 이후의 버전에서, 이제 Mintty 에서 입력한 문자를 읽습니다. (#1348)
* 윈도우즈 10 Anniversary Update 혹은 그 이후의 버전에서, 윈도우즈 콘솔의 출력 내용이 커서 근처에 있을 때 그 철자를 읽지 않습니다. (#513)
* Audacity 의 압축 대화상자를 이용할 때 조작부를 읽을 수 있습니다. (#10103)
* Notepad++ 같이 Scintilla 기반의 편집기에서 객체 검토 모드에 있을 때 공백을 단어로 다루지 않습니다. (#8295)
* 점자 디스플레이에서 동작으로 문자를 스크롤하고 있을 동안, NVDA는 시스템이 절전 모드에 들어가는 것을 막습니다. (#9175)
* 윈도우즈 10에서, Microsoft Excel 를 사용해서 셀 내용을 편집하거나 다른 UIA 문자 조작 기능을 사용할 때 점자가 뒤쳐지지 않고 맞춰서 따라옵니다. (#9749)
* Microsoft Edge 주소창에서 자동완성 목록을 읽어 주는 기능이 복구됐습니다. (#7554)
* Internet Explorer 에서 HTML 탭 조작 헤더에 초점을 맞추고 있을 때, NVDA 가 내용을 읽습니다. (#8898)
* Edge HTML을 기반으로 한 Microsoft Edge에서, 창이 최대화되어 있는 동안에는 검색 자동완성 효과음을 내지 않습니다. (#9110, #10002)
* 모질라 FireFox와 구글 Chrome 브라우저에서 ARIA 1.1 콤보박스를 지원합니다. (#9616)
* SysListView32 컨트롤 내용 중 화면에서 숨겨진 리스트 항목의 내용을 읽지 않습니다. (#8268)
* 보안 상태에 있는 동안 설정 대화상자에서 현재 로그 수준을 무조건 "정보"로 표시하지 않습니다. (#10209)
* 윈도우즈 10 Anniversary Update 혹은 그 이후 버전의 '시작' 메뉴에서, 검색 결과의 상세 내용을 알려줍니다. (#10232)
* 브라우저 상태에서 커서를 옮기거나 빠른 메뉴를 이용해서 문서가 바뀌는 경우 NVDA가 잘못된 내용을 읽지 않습니다. (#8831, #10343)
* Microsoft Word에서 일부 불릿 명칭이 수정됐습니다. (#10399)
* 윈도우즈 10의 2019년 5월 이후 업데이트에서, 이모지 패널이나 클립보드 기록 창이 열릴 때 처음 선택한 이모지나 클립보드를 정상적으로 읽습니다. (#9204)
* Poedit에서 오른쪽에서 왼쪽으로 읽는 언어로 해석된 내용을 일부 읽지 못했던 것이 수정됐습니다. (#9931)
* 윈도우즈 10의 2018년 4월 이후 업데이트에서 설정 앱을 사용할 때, 시스템/음향 화면에 나타나는 음량 표시기의 진행 정보를 더 이상 읽지 않습니다. (#10284)
* 음성 사전에 포함된 정규식의 형식이 잘못됐을 경우 NVDA의 음성이 완전히 멈추는 현상을 수정했습니다. (#10334)
* Microsoft Word에서 UIA가 활성화된 상태로 불릿 목록을 읽을 때, 다음 목록 항목의 불릿을 잘못 읽는 버그가 수정됐습니다. (#9613)
* Liblouis에서 드물게 나타나는 일부 점자번역 문제와 오류가 수정됐습니다. (#9982)
* NVDA가 시작하기 전에 실행되고 있던 Java 어플리케이션도 이제는 앱을 재실행할 필요 없이 접근할 수 있습니다. (#10296)
* 모질라 FireFox 브라우저에서, 포커스된 요소가 현재 위치(aria-current)로 바뀔 경우 이를 여러 번 읽는 버그가 수정됐습니다. (#8960)
* 문자를 따라 움직일 때 액센트가 붙은 영문자처럼 유니코드의 조합 문자 일부를 하나의 문자로 읽지 못하던 문제가 해결됐습니다. (#10550)
* Spring Tool Suite Version 4에 대한 지원이 추가됐습니다. (#10001)
* aria-labelledby로 특정된 객체가 선택된 객체 내부에 있을 경우 그 이름을 두 번 읽는 버그가 수정됐습니다. (#10552)
* 윈도우즈 10의 1607 이후 버전에서, 점자 키보드에서 입력된 문자를 읽는 기능이 더 많은 경우에 지원됩니다. (#10569)
* 소리 출력 장치를 변경할 때, NVDA의 음향 효과가 이제는 새로 선택된 장치를 통해서 재생됩니다. (#2167)
* 모질라 FireFox의 브라우즈 모드에서 포커스의 움직임이 빨라졌으며, 브라우즈 모드에서 많은 경우 커서의 반응속도가 빨라졌습니다. (#10584)

### 개발 변경사항(영문)

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

이 버전은 2019.2. 버전이 갑자기 동작이 멈추는 몇몇 상황을 수정한 소규모 업데이트입니다. 수정된 항목은 다음과 같습니다.

* FireFox 및 Chrome 브라우저를 이용해서 Gmail에서 필터 생성이나 이메일 설정 등 특정 팝업 메뉴를 사용할 때 동작이 멈추는 현상을 해결했습니다. (#10175, #9402, #8924)
* 윈도우즈 7의 시작 메뉴에서 마우스를 이용할 때 탐색기가 동작을 멈추는 문제를 해결했습니다. (#9435)
* 윈도우즈 7의 탐색기에서 메타데이터 편집 창에 접근할 때 동작을 멈추는 현상을 해결했습니다. (#5337)
* 파이어포스나 Chrome 브라우저에서 base64로 인코딩된 위치에 있는 이미지에 접근할 때 NVDA가 멈추는 문제를 해결했습니다. (#10227)

## 2019.2

이 버전의 주요 변경사항은 Freedom Scientific 사의 점자 디스플레이에 대한 자동 인식, 브라우저 모드에서 포커스가 자동으로 움직이는 (효율 향상을 목적으로 한) 기능 막기 위해서 고급 설정 패널에 추가된 실험적인 설정, Windows OneCore 음성합성기를 매우 빨리 말할 수 있도록 해주는 음성속도 향상 기능, 그리고 그밖에 많은 버그 수정을 포함합니다.

### 새로운 기능

* NVDA가 Miranda NG의 최근 버전 클라이언트와 함께 동작합니다. (#9053)
* 브라우즈 모드 설정에 새로 추가된 "페이지가 로드되면 브라우즈 모드 활성화" 옵션을 비활성화하면, 이제 기본 설정으로 브라우즈 모드를 사용하지 않을 수 있습니다. (#8716)
 * 이 옵션이 비활성화되어 있을 때에도 NVDA+Space 키를 눌러서 수동으로 브라우저 모드를 활성화할 수 있습니다.
* 요소 목록이나 제스처 입력 대화상자의 필터 기능과 비슷한 방식으로, 구두점/기호 발음 설정 대화상자에서 기호 목록에 필터를 적용할 수 있습니다. (#5761)
* 마우스 텍스트 해상도(마우스가 움직일 때 읽어주는 글자는 분량)을 변경하기 위한 명령이 추가됐습니다. 이 명령에는 기본 제스처가 부여되어 있지 않습니다. (#9056)
* Windows OneCore 음성합성기에 음성속도 향상 기능이 추가되어 훨씬 빨리 읽을 수 있게 됐습니다. (#7498)
* 이제 지원하는 음성합성기에 한하여 (현재는 eSpeak-NG 와 Windows OneCore 뿐입니다) 음성엔진 설정에서 음성속도 향상 옵션을 설정할 수 있습니다. (#8934)
* 환경 설정 프로파일을 이제 제스처를 통해 직접 실행할 수 있습니다. (#4209)
 * "제스처 설정" 대화상자를 통해 제스처를 설정해야 합니다.
* Eclipse의 코드 편집창에서 자동완성에 대한 지원이 추가됐습니다. (#5667)
 * 이 외에도, 편집기에서 NVDA+d 단축키로 Javadoc 정보가 표시됐을 때 그 내용을 읽을 수 있습니다.
* 고급 설정 패널에 시스템 포커스가 브라우즈 모드 커서를 자동으로 추적하는 것을 중지하는 실험적인 기능이 추가되었습니다(자동으로 시스템 포커스 이동). (#2039) 모든 웹사이트를 탐색에 이 기능을 해제하는 것이 적합하지 않을 수 있으나 다음과 같은 경우의 문제가 해결될 수 있습니다.
 * NVDA가 가끔 브라우저 모드 키 입력을 무시하고 이전 위치로 튕겨지는 경우 (고무줄 현상)
 * 일부 웹사이트에서 아래 화살표 키를 통해 탐색할 때, 편집창이 시스템 포커스를 가리는 경우
 * 키 입력에 따른 브라우즈 모드 반응속도가 느린 경우
* 이제 지원하는 기기에 한에서 NVDA 설정 대화상자의 점자 카테고리에서 드라이버 설정을 변경할 수 있습니다. (#7452)
* 이제 Freedom Scientific의 점자 디스플레이 제품군의 점자 디스플레이 자동 탐색이 지원됩니다. (#7727)
* 리뷰 커서 아래에 있는 기호를 대신할 이름을 표시하는 명령을 추가했습니다. (#9286)
* 고급 설정에 Microsoft UI Automation API를 사용하여 작업중인 Windows 콘솔을 편집하는 실험적인 기능이 추가되었습니다. (#9614)
* 이제 파이썬 콘솔에서 클립보드로부터 여러줄의 텍스트를 붙여 넣을 수 있습니다. (#9776)

### 변경사항

* 간단 음성 엔진 설정을 사용하여 음성 볼륨을 조절할 때 증가/감소하는 수치가 10에서 5로 조절되었습니다 (#6754)
* NVDA가 --disable-addons 플래그와 함께 실행됐을 때 추가 기능 관리자에 표시되는 메시지를 좀더 명확하게 바꿨습니다. (#9473)
* 유니코드 협회의 국제 표기양식 기록원(CLDR)에 따른 이모지 명칭을 35.0 버전으로 업데이트 했습니다. (#9445)
* 브라우즈 모드에서 나타나는 요소 목록의 필터 양식 단축키가 alt+y로 바뀌었습니다. (#8728)
* 점자 디스플레이가 블루투스를 통해서 자동적으로 인식되어 연결됐을 때, 같은 드라이버가 USB로도 연결이 되어 있는지를 확인하고 가능한 경우 USB로 연결을 전환합니다. (#8853)
* eSpeak-NG를 업데이트 했습니다. commit 67324cc.
* Liblouis 점자 번역기를 3.10.0 버전으로 업데이트 했습니다. (#9439, #9678)
* 사용자가 문자를 선택하면 이제 그 문자를 읽은 후에 '선택됨' 이라는 말을 덧붙입니다. (#9028, #9909)
* Microsoft Visual Studio Code 에서 NVDA의 기본 모드가 포커스 모드로 설정됐습니다. (#9828)

### 버그 수정내역

* 추가 기능 목록이 비어 있을 때 NVDA가 동작을 멈추는 현상이 수정됐습니다. (#7686)
* 점자나 글자별 읽기 모드에서 속성 윈도우에 접근할 때, 더 이상 LTR 이나 RTL 표시를 읽지 않습니다. (#8361)
* 이제는 브라우즈 모드의 빠른 탐색 기능으로 폼 양식에 들어갈 때, 첫 줄만 읽는 대신 폼 양식 전체를 읽습니다. (#9388)
* Windows 10 Mail app 을 나간 후에 NVDA 가 조용해지는 현상을 수정했습니다. (#9341)
* 사용자의 지역 설정이 '영어 (네델란드)'처럼 NVDA가 모르는 항목으로 설정됐을 때 NVDA가 시작되지 않는 문제가 해결됐습니다. (#8726)
* 브라우즈 모드의 Microsoft Excel과 포커스 모드의 웹 브라우저 사이를 오갈 때, 브라우즈 모드 상태를 이제 정상적으로 알립니다. (#8846)
* Notepad++ 나 다른 Scintilla 기반 편집기에서 마우스 커서가 있는 행을 이제 정상적으로 읽습니다. (#5450)
* Google Docs (혹은 다른 웹 기반 편집기) 에서, 커서가 목록 항목의 중간에 있을 때 그 위치 앞에 점자로 "lst end"가 표시되는 현상이 수정되었습니다. (#9477)
* Windows 10의 2019년 5월 업데이트에서, 파일 탐색기에 포커스를 맞춘 채 하드웨어 버튼으로 음량을 바꾸면 NVDA가 음량 알림 메시지를 여러 번 읽는 문제가 해결됐습니다. (#9466)
* 기호 사전에 1000개 이상의 항목이 있는 경우 문장부호/기호 발음 대화상자가 훨씬 빨리 열립니다. (#8790)
* Notepad++ 와 같은 Scintilla 기반 편집기에서 줄바꿈 옵션이 켜있는 경우에도 올바른 행을 읽습니다. (#9424)
* Microsoft Excel에서 Shift+Enter 혹은 Shift+Numpad Enter 제스처로 바뀐 셀 위치를 알려줍니다. (#9499)
* Visual Studio 2017 이후의 버전에서 객체 탐색기 창을 쓸 때, 객체 트리나 멤버 트리에서 선택한 항목이 분류 설정을 갖고 있는 경우에도 이제 정상적으로 읽어줍니다. (#9311)
* 추가 기능 이름들 사이에 대소문자의 차이만 있는 경우에는 더 이상 다른 추가 기능으로 취급하지 않습니다. (#9334)
* Windows OneCore 음성을 사용할 때, Windows 10 음성 설정이 더 이상 NVDA의 말하기 속도 설정에 영향을 미치지 않습니다. (#7498)
* 현재 탐색 객체에 개발자 정보가 없을 때에도 NVDA+F1 을 눌러 로그를 열 수 있습니다. (#8613)
* NVDA의 표 탐색 명령을 다시 Google Docs 에서 쓸 수 있게 됐습니다. FireFox와 Chrome에서 동작합니다. (#9494)
* Freedom Scientific 점자 디스플레이에서 bumper key들이 이제 잘 동작합니다. (#8849)
* Notepad++ 7.7 X64 버전에서 문서의 첫번째 문자를 읽을 때 NVDA가 10초 정도까지 동작을 멈추는 문제가 해결됐습니다. (#9609)
* 이제 NVDA에서 HTCom을 Handy Tech 점자 디스플레이와 함께 쓸 수 있습니다. (#9691)
* 모질라 FireFox에서 실시간 갱신 영역이 백그라운드 탭에 있는 경우에도 그 내용을 업데이트하는 문제가 해결됐습니다. (#1318)
* NVDA의 브라우즈 모드에서 NVDA의 프로그램 정보 대화상자가 백그라운드에 열려 있는 경우 찾기 대화상자가 제대로 동작하지 않던 문제가 해결됐습니다. (#8566)

### 개발 변경사항(영문)

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

NVDA 2019.1.1 버전은 다음 버그를 수정합니다:

* NVDA로 인해 더 이상 Excel 2007이 중단되거나 셀에 수식 있음을 알리지 않음. (#9431)
* Google Chrome에서 특정 목록 상자와 상호작용할 때  더 이상 충돌하지 않음. (#9364)
* 사용자 환경 설정을 시스템 환경 프로파일로 복사하지 못하는 문제 수정. (#9448)
* Microsoft Excel에서 NVDA가 병합된 셀의 위치를 알릴 때 번역된 메시지를 다시 사용함. (#9471)

## 2019.1

이 릴리스에는 Microsoft Word와 Excel에 액세스할 때 성능 향상, 버전 호환성 정보가 포함된 추가 기능 지원 및 기타 버그 수정과 같은 안정성 및 보안 향상 등입니다.

NVDA의 이번 버전 부터 custom appModules, globalPlugins, 점자 디스플레이 드라이버 및 신디사이저 드라이버는 더 이상 NVDA 사용자 커스텀 디렉토리에서 자동으로 로드되지 않습니다.
오히려 이것들은 NVDA 추가 기능의 일부로 설치되어야합니다. 추가 기능 코드를 개발하는 개발자는 NVDA의 새로운 고급 설정 패널에서 개발자 스크래치 패드 옵션이 켜져있는 경우 NVDA 사용자 커스텀 디렉토리의 새로운 개발자 스크래치 패드 디렉토리에 테스트 코드를 넣을 수 있습니다.
이러한 변경 사항은 커스텀 코드의 호환성을 보장하기 위해 필요하므로 이 코드가 최신 릴리스와 호환되지 않을 때 NVDA가 중단되지 않습니다.
이에 대한 자세한 내용과 추가 기능의 버전 관리 방법에 대한 자세한 내용은 변경 목록을 참조하십시오.

### 새로운 기능

* 새로운 점자 테이블: 아프리칸스어, 아랍어 8 점 컴퓨터 점자, 아랍어 grade 2, 스페인어 grade 2. (#4435, #9186)
* NVDA의 마우스 설정에 옵션을 추가하여 NVDA가 다른 응용 프로그램에서 마우스를 제어하는 상황을 처리하도록 함. (#8452)
 * TeamViewer 또는 다른 원격 제어 소프트웨어를 사용하여 원격으로 시스템을 제어 할 때 NVDA가 마우스를 추적할 수 있음.
* `--enable-start-on-logon` 명령줄 매개 변수를 추가하여 NVDA 세트 NVDA의 자동 설치를 Windows 로그온 시 시작할지 여부를 구성할 수 있음. 로그온할 때 시작하려면 true를, 로그온할 때 시작하지 않으려면 false를 지정. --enable-start-on-logon 인수가 전혀 지정되지 않은 경우 이전 설치에서 시작하지 않도록 이미 구성되어 있지 않은 한 NVDA는 로그온 시 기본적으로 시작됨. (#8574)
* 일반 설정 패널에서 로깅 수준을 "사용 안 함"으로 설정하여 NVDA의 로깅 기능을 비활성화할 수 있음. (#8516)
* LibreOffice 및 Apache OpenOffice spreadsheet에 수식이 있으면 알림. (#860)
* Mozilla Firefox 및 Google Chrome의 브라우즈 모드에서 목록 상자 및 트리에서 선택된 항목을 알림.
 * Firefox 66 이상에서 작동함.
 * Chrome의 특정 목록상자 (HTML select 컨트롤)는 작동하지 않음.
* ARM64 (예 : Qualcomm Snapdragon) 프로세서가 장착 된 컴퓨터에서 Mozilla Firefox와 같은 응용 프로그램에 대한 초기 지원 (#9216)
* NVDA 설정 대화상자에 "고급 설정"카테고리가 추가되었습니다. 고급 설정 카테고리에는 Microsoft UI Automation API를 통해 NVDA의 Microsoft Word에 대한 새로운 지원을 시험해 볼 수 있는 옵션을 포함합니다. (#9200)
* Windows 디스크 관리의 그래픽 보기 지원 추가. (#1486)
* Handy Tech Connect Braille 및 Basic Braille 84 지원 추가. (#9249)

### 변경사항

* Liblouis 점자  변환기 version 3.8.0 사용. (#9013)
* 추가 기능 제작자는 이제 추가 기능에 필요한 최소 NVDA 버전을 지정할 수 있습니다. NVDA는 필요한 최소 NVDA 추가 기능이 지정된 값이 현재 NVDA 버전보다 높은 경우 추가 기능을 설치하거나 로드하지 않습니다. (#6275)
* 추가 기능 제작자는 이제 추가 기능을 테스트한 마지막 NVDA 버전을 지정할 수 있습니다. 추가 기능이 현재 NVDA 버전보다 낮은 NVDA 버전에 대해 테스트된 경우 NVDA는 추가 기능을 설치하거나 로드하지 않습니다. (#6275)
* NVDA 2019.1 버전에서는 아직 최소 버전, 마지막 테스트된 NVDA 버전 정보가 포함되지 않은 추가 기능을 설치 및 로드할 수 있지만 향후 NVDA 버전 (예 : 2019.2)로 업그레이드하면 이러한 이전 추가 기능이 자동으로 비활성화될 수 있습니다.
* 마우스를 탐색 개체로 이동 명령을 Microsoft Word 및 UIA 컨트롤, 특히 Microsoft Edge에서 사용할 수 있음. (#7916, #8371)
* 마우스가 위치한 텍스트 알림 기능이 Microsoft Edge 및 기타 UIA 응용 프로그램에서 향상됨. (#8370)
* `--portable-path` 명령 줄 매개 변수로 NVDA를 시작하면 NVDA 메뉴를 사용하여 휴대용 NVDA 버전을 만들 때 제공된 경로가 휴대용 버전 설치 폴더 필드에 자동으로 채워집니다. (#8623)
* 2015년 기준을 반영하여 노르웨이 점자 테이블 경로가 업데이트되었습니다. (#9170)
* 단락 간 이동(control + 위쪽 또는 아래쪽 화살표)로 탐색하거나 테이블 셀 (control + alt + 화살표)로 탐색할 때 NVDA가 자동으로 맞춤법 오류를  알리도록 설정되어 있어도 더 이상 맞춤법 오류를 알리지 않습니다. 단락과 표 셀이 상당히 클 수 있고 일부 응용 프로그램에서 맞춤법 오류를 감지하는 데 성능 저하가 일어날 수 있기 때문입니다. (#9217)
* NVDA는 더 이상 NVDA 사용자 환경 설정 디렉토리에서 사용자 정의 appModules, globalPlugins, 점자 디스플레이, 신디사이저 드라이버를 자동으로 로드하지 않습니다. 이러한 모듈은 적절한 정보를 가지는 추가 기능으로 패키지되어야 합니다. 이러한 변경으로 인해 호환되지 않는 코드가 NVDA에서 실행되는 것을 방지합니다. (#9238)
 - 개발중인 코드를 테스트해야하는 개발자의 경우 NVDA 설정의 고급 카테고리에서 NVDA의 개발자 스크래치 패드 디렉토리 옵션을 활성화해야 합니다. 이 옵션이 활성화되면 NVDA 사용자 환경 설정 디렉토리에 있는 '스크래치 패드'디렉토리에 개발 중인 코드를 복사해야 합니다.

### 버그 수정내역

* Windows 10 2018년 4월 업데이트 이상에서 OneCore 음성 합성기 사용 시 음성 발화 사이에 더 이상 무음이 삽입되지 않도록 함. (#8985)
* 메모장과 같은 일반 텍스트 컨트롤이나 브라우즈 모드에서 문자별로 이동 시 두 개의 UTF-16 코드 포인트 (예 : 🤦)로 구성된 32 비트 이모티콘 문자가 올바르게 읽히도록 수정. (#8782)
* NVDA의 인터페이스 언어를 변경한 후 표시되는 다시 시작 확인 대화상자 개선. 텍스트와 버튼 레이블이보다 간결하고 혼동되지 않음. (#6416)
* 서드파티 음성 합성기 로드에 실패하면 NVDA는 Windows 10에서 espeak 음성이 아닌 Windows OneCore 음성 합성기가 로드되도록 함. (#9025)
* 보안 데스크탑 화면에서 NVDA 메뉴의 "시작 대화상자" 항목 제거. (#8520)
* 브라우즈 모드에서 탭하거나 빠른 탐색을 사용할 때 탭 패널의 legend 속성이  보다 일관되게 알려지도록 수정. (#709)
* NVDA는 이제 Windows 10의 알람 및 시계 앱과 같은 특정 시간 피커의 대한 선택 변경 사항을 알림. (#5231)
* Windows 10의 알림 센터에서 NVDA는 밝기 및 집중 지원과 같은 알림 동작을 전환할 때 상태 메시지를 알림. (#8954)
* Windows 10 2018년 10월 업데이트 및 이전 버전의 알림 센터에서 NVDA는 밝기 빠른 알림 컨트롤을 토글 버튼 대신 버튼으로 인식함. (#8845)
* NVDA는 Microsoft Excel의 이동 대화상자, 찾기 대하상자의 편집 필드에서 커서를 다시 탐색할 수 있고 삭제된 문자를 알림. (#9042)
* Firefox에서 드물게 발생하는 브라우즈 모드 충돌 문제 수정. (#9152)
* NVDA no longer fails to report the focus for some controls in the Microsoft Office 2016 ribbon when collapsed.
* Outlook 2016에서 새 메시지에 주소를 입력할 때 NVDA가 더 이상 제안된 연락처를 알리지 않음. (#8502)
* eurobraille 80 셀 점자 디스플레이에서 마지막 몇 개의 커서 라우팅 키는 더 이상 점자 라인 시작 시점 또는 직후 위치로 커서를 라우팅하지 않음. (#9160)
* Mozilla Thunderbird의 스레드 보기 표 탐색 문제 수정. (#8396)
* Mozilla Firefox 및 Google Chrome에서 특정 목록 상자 및 트리 (목록 상자 / 트리 자체가 초점을 맞출 수 없지만 항목이 있는 경우)에 대해 포커스 모드로 전환 시 탐색 가능. (#3573, #9157)
* NVDA의 실험적인 Word 문서용 UI Automation 지원을 사용하는 경우 Outlook 2016/365에서 메시지를 읽을 때 브라우즈 모드가 기본적으로 설정되도록 함. (#9188)
* NVDA is now less likely to freeze in such a way that the only way to escape is signing out from your current windows session. (#6291)
* Windows 10 2018년 10월 업데이트 이상에서 클립보드가 비어있는 클라우드 클립보드 기록을 열면 NVDA가 클립 보드 상태를 알림. (#9103)
* Windows 10 2018년 10월 업데이트 이상에서 이모티콘 패널에서 이모티콘을 검색하면 NVDA가 이모티콘  검색 결과를 알림. (#9105)
* Oracle VirtualBox 5.2 이상의 기본 창에서 NVDA가 더 이상 정지되지 않음. (#9202)
* 일부 문서에서 줄, 단락 또는 표 셀을 탐색 할 때 Microsoft Word의 응답성이 크게 향상됨. 최상의 성능을 얻으려면 문서를 연 후 alt+w,e를 사용하여 Microsoft Word를 초안보기로 설정 필요. (#9217)
* Mozilla Firefox 및 Chrome에서 빈 알림을 더 이상 알리지 않음. (#5657)
* Microsoft Excel에서 스프레드 시트에 주석 및 유효성 검사 드롭 다운 목록이 포함된 경우  셀을 탐색 할 때 성능이 크게 향상됨. (#7348)
* Excel 2016/365에서 NVDA를 사용하여 셀 편집 컨트롤에 액세스하기 위해 Microsoft Excel 옵션에서 셀에서 직접 편집 허용을 더 이상 해제할 필요가 없습니다. (#8146).
* Enhanced Aria 추가 기능을 사용하는 경우 랜드 마크로 빠르게 탐색 할 때 Firefox에서 가끔 멈추는 현상 수정. (#8980)

### 개발 변경사항(영문)

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

이번 버전에서는 NVDA의 사용자 인터페이스 언어가 아라곤어로 설정된 경우 NVDA 시작 시 충돌 문제가 수정되었습니다. (#9089)

## 2018.4

이번 버전의 주 기능들: 최신 FireFox 버전에서의 탐색 속도 향상; 모든 음성 엔진에서의 이모지 출력 기능; Outlook 사용 시 답장/전달 여부 확인; Microsoft Word에서의 페이지 좌측 상단으로부터의 커서 위치 확인 및 수많은 버그 수정 등입니다.

### 새로운 기능

* 점자 표기법: 중국어(중국 간체) 1종 및 2종 점자 추가. (#5553)
* Microsoft Outlook 메시지 목록 탐색 시 메시지 답장 및 전달 여부가 표시되도록 함. (#6911)
* Unicode Common Locale Data Repository(CLDR)에 등록된 글자(특히 이모지와 특정 글자)에 대한 풀이 출력 기능 추가. (#6523)
* Microsoft Word 사용시 NVDA+numpadDelete를 눌러 페이지 상단 좌측으로부터의 커서 위치를 확인할 수 있음. (#1939)
* Google 스프레드시트에서 점자 모드 사용 시 포커스를 각 셀로 옮길때마다 "선택됨"이 출력되지 않도록 함. (#8879)
* Foxit Reader 및 Foxit Phantom PDF 지원 추가. (#8944)
* DBeaver database tool 지원 추가. (#8905)

### 변경사항

* 객체 알림 설정에 있는 "Report help balloons"를 "Report notifications"로 변경하여 윈도우 8 이상에서의 토스트 알림도 포함하도록 함(한국어 번역에서는 이전 이름 그대로 사용). (#5789)
* 키보드 설정에서 NVDA 기능키 체크박스들을 하나의 목록으로 통합함.
* 특정 윈도우 버전 사용 시 알림 영역 내 시계 정보 출력 시 불필요한 정보가 출력되지 않도록 함. (#4364)
* Liblouis 점자 변환기 3.7.0 버전 사용. (#8697)
* eSpeak NG commit 919f3240cbb 사용.

### 버그 수정내역

* Outlook 2016/365 사용 시 메시지 flag 및 category가 출력되도록 함. (#8603)
* NVDA 언어가 키르키즈스탄어, 몽골어 또는 마세도니아어로 설정된 경우 NVDA 시작 시 윈도우에서의 언어 미지원 메시지가 뜨지 않도록 함. (#8064)
* FireFox, Chrome 및 Acrobat DC 사용 중 마우스를 탐색 객체로 옮길 시 현재 브라우즈 모드 위치로 마우스가 제대로 옮겨지도록 함. (#6460)
* FireFox, Chrome 및 Internet Explorer에서의 콤보박스 조작 정확도가 향상됨. (#8664)
* 일본어판 윈도우 XP 또는 비스타 사용 시 운영 체제 요구사항 관련 메시지가 제대로 출력되도록 함. (#8771)
* FireFox를 통한 대형 페이지(특히 자동 컨텐츠 변경이 많은 페이지) 탐색 속도가 향상됨. (#8678)
* 점자 디스플레이 사용 시 문서 서식에서 해제된 서식 정보가 출력되지 않도록 함. (#7615)
* UI Automation 사용 시 여러 앱이 특정 작업(특히 여러개의 오디오 파일을 변환할 때) 도중 파일 탐색기와 같은 앱에서 포커스 추적이 다운되던 문제 수정. (#7345)
* 웹 브라우저에서 ARIA 메뉴에서 Escape 키를 누를 때 메뉴가 키를 인식하도록 함(이전에는 무조건 포커스 모드를 빠져나갔음). (#3215)
* 최신 업데이트된 Gmail 웹 인터페이스 사용 시 메시지 내용을 읽던 중 한 글자 명령을 사용 시 포커스된 요소를 출력한 후 메시지 내용이 반복되어 출력되던 문제 수정. (#8887)
* NVDA 업데이트 후 FireFox나 Chrome이 다운되거나 현재 탐색중인 페이지의 컨텐츠 변경 내용이 제대로 출력되지 않던 문제 수정. (#7641) 
* 브라우즈 모드 사용 시 클릭 가능한 요소를 만났을 때 클릭 가능 상태가 여러번 출력되던 문제 수정. (#7430)
* baum Vario 40 점자 디스플레이 사용 시 점자 입력 명령이 실행되지 않던 문제 수정. (#8894)
* FireFox에서 Google 프레젠테이션 사용 시 포커스를 옮길 때마다 선택된 내용이 불필요하게 출력되던 문제 수정. (#8964)

### 개발 변경사항(영문)

* gui.nvdaControls now contains two classes to create accessible lists with check boxes. (#7325)
 * CustomCheckListBox is an accessible subclass of wx.CheckListBox.
 * AutoWidthColumnCheckListCtrl adds accessible check boxes to an AutoWidthColumnListCtrl, which itself is based on wx.ListCtrl.
* If you need to make a wx widget accessible which isn't already, it is possible to do so by using an instance of gui.accPropServer.IAccPropServer_impl. (#7491)
 * See the implementation of gui.nvdaControls.ListCtrlAccPropServer for more info.
* Updated configobj to 5.1.0dev commit 5b5de48a. (#4470)
* The config.post_configProfileSwitch action now takes the optional prevConf keyword argument, allowing handlers to take action based on differences between configuration before and after the profile switch. (#8758)

## 2018.3.2

본 버전에서는 Chrome을 사용하여 [www.twitter.com](http://www.twitter.com) 탐색시 발생하던 오류 문제를 수정했습니다. (#8777)

## 2018.3.1

본 버전에서는 FireFox 32비트 사용중 FireFox가 다운되던 문제를 수정하였습니다. (#8759)

## 2018.3

이번 버전의 주 기능들: 점자 디스플레이 자동 인식 및 연결, 이모지 패널과 같은 최신 윈도우 10 입력 기능 지원, 수많은 버그 수정 등입니다.

### 새로운 기능

* FireFox와 Chrome 사용 시 페이지 컨텐츠 내 문법 오류(컨텐츠가 오류 출력 지원 시)가 인식되도록 함. (#8280)
* Chrome 사용 시 웹페이지 컨텐츠 삽입 또는 삭제 내용이 출력되도록 함. (#8558)
* 브레일노트 QT 및 Apex scroll wheel 지원 추가. (#5992, #5993)
* Foobar2000에서 현재 재생 시간 및 전체 재생 시간 확인 명령 추가(핫키는 할당되어 있지 않음). (#6596)
* 음성 엔진에 상관없이 Mac command key 기호(⌘)가 컨텐츠 읽을 시 출력되도록 함. (#8366)
* aria-roledescription 속성이 적용된 기타 요소 역할이 모든 웹브라우저에서 인식되도록 함. (#8448)
* 점자 표기법: 체코어 8점 점자, 중앙 쿠르드어, 에스페란토어, 헝가리어, 스웨덴어 8점 컴퓨터 점자 추가. (#8226, #8437)
* 점자 디스플레이 자동 인식 기능 추가. (#1271)
 * 현재 본 기능을 지원하는 디스플레이: ALVA, Baum/HumanWare/APH/Orbit, Eurobraille, Handy Tech, Hims, SuperBraille 및 HumanWare BrailleNote and Brailliant BI/B.
 * 점자 디스플레이 목록 대화상자에서 "자동 연결" 옵션을 사용하여 본 기능을 사용할 수 있음.
 * 자세한 내용은 사용설명서를 참고바람.
* 최신 윈도우 10 버전에서 추가된 현대식 입력 기능 지원 추가(이모지 패널(Fall Creators Update), 음성 입력(Fall Creators Update), 하드웨어 입력 추천 단어 목록(April 2018 Update),, 클라우드 클립보드 붙여넣기(October 2018 Update) 등). (#7273)
* FireFox 63 사용 시 ARIA로 처리된 인용 문구(blockquote 역할) 탐색 지원 추가. (#8577)

### 변경사항

* 일반 설정 내 언어 목록이 가나다순으로 정렬되어 표시되도록 함(이전에는 ISO 639 코드순으로 정렬됨). (#7284)
* Freedom Scientific 점자 디스플레이 사용 시 alt+shift+tab 및 windows+tab 명령을 실행할 수 있는 핫키 추가. (#7387)
* ALVA BC680 및 protocol converter 디스플레이 사용 시 왼쪽 및 오른쪽 smart pad, thumb 및 etouch 키에 각기 다른 명령을 할당할 수 있음. (#8230)
* ALVA BC6 디스플레이 사용 시 sp2+sp3을 눌러 현재 시각 및 날짜를 확인할 수 있도록 변경(Windows 키 입력은 sp1+sp2로 변경함). (#8230)
* NVDA 2018.3 설치 후 NVDA 실행할 때 추후 자동 업데이트 확인 시 NV Access에 사용 통계 데이터 전송에 참여할 것인지를 묻는 대화상자가 표시되도록 함. (#8217)
* NVDA 업데이트 확인 시 만약 NV Access에 사용 통계 정보 전송을 허용했다면 현재 사용중인 음성 엔진 이름과 점자 디스플레이 이름이 전송되도록 함(본 데이타는 추후 개발 계획에 반영될 수 있음). (#8217)
* Liblouis 점자 변환기 3.6.0 버전 사용. (#8365)
* 러시아어 8점 점자표 경로 변경. (#8446)
* eSpeak NG 1.49.3dev commit 910f4c2 사용. (#8561)

### 버그 수정내역

* Chrome 사용 시 컨텐츠로 인식되지 못한 컨트롤 레이블이 브라우즈 모드에서 인식되도록 함. (#4773)
* Zoom 클라이언트 사용 시 음숙어 및 새 메시지와 같은 알림 컨텐츠 인식 추가. (#7754)
* 브라우즈 모드 사용 중 점자 포커스 내용 설정 변경 시 점자가 브라우즈 모드 커서를 따라가지 못하던 문제 수정. (#7741)
* ALVA BC680 디스플레이 연결 시 초기 연결에 가끔 실패하던 문제 수정. (#8106)
* ALVA BC6 디스플레이 사용 시 sp2+sp3 키를 조합한 키를 눌러 내부 명령 실행 시 시스템 키 입력 명령이 실행되지 않도록 함. (#8230)
* ALVA BC6 디스플레이 사용 시 sp2를 눌러 alt 키 실행 명령이 작동하지 않던 문제 수정. (#8360)
* NVDA가 불필요한 키보드 배열 변경 정보를 출력하던 문제 수정. (#7383, #8419)
* 메못장과 같은 텍스트 컨트롤에서 65535자 이상의 컨텐츠를 불러왔을 때 마우스 추적 정확도가 저하되던 문제 수정. (#8397)
* 윈도우 10 및 모던 앱 사용 시 더 많은 대화상자가 인식되도록 함. (#8405)
* 윈도우 10 October 2018 Update 및 Server 2019 이상 사용 시 사용하던 앱이 다운되었거나 수많은 이벤트를 보낼 때 시스템 포커스 추적이 먹통되던 문제 수정. (#7345, #8535)
* 상태 표시줄 내용이 없을때 내용 탐색 및 복사 명령 실행시 오류 메시지가 출력되도록 함. (#7789)
* 이전에 일부 선택된 컨트롤을 해제한 후 다른 컨트롤을 탐색하다가 이전 컨트롤을 탐색 시 현재 선택 상태가 음성으로 제대로 출력되지 않던 문제 수정. (#6946)
* 윈도우 7 사용 시 NVDA 일반 설정 내 언어 목록에서 버마어가 누락되었던 문제 수정. (#8544)
* Microsoft Edge 사용 시 읽기 모드 사용 및 페이지 열기 진행 정보와 같은 알림 정보가 출력되도록 함. (#8423)
* 웹브라우저에서 목록 탐색 시 웹 개발자가 목록 레이블을 지정했을때 목록 레이블이 출력되도록 함. (#7652)
* 특정 점자 디스플레이에 명령 핫키를 할당할 때 선택된 디스플레이에 핫키가 할당되었음을 표시하도록 함(이전에는 현재 사용중인 디스플레이에 할당되었다고 출력함). (#8108)
* Media Player Classic 64비트 버전 지원 추가. (#6066)
* Microsoft Word에서의 UIA 관련 기능 향상:
 * 다른 다중 편집창과 마찬가지로 점자 커서가 문서 시작에 위치할때 줄 시작 위치 글자가 디스플레이의 맨 왼쪽에 출력되도록 함. (#8406)
 * 문서로 전 환시 불필요한 포커스 정보가 음성이나 점자로 출력되던 문제 수정. (#8407)
 * 문서 내 목록을 점자로 읽을 시 라우팅 명령이 제대로 작동하지 않던 문제 수정. (#7971)
 * 새로 삽입된 bullet/항목 숫자가 음성과 점자로 제대로 출력되도록 함. (#7970)
* 윈도우 10 1803 이상에서 "세계 언어 지원을 위해 Unicode UTF-8 사용" 기능이 선택된 경우 추가 기능을 설치할 수 없던 문제 수정. (#8599)
* iTunes 12.9 지원 관련 여러 문제 수정. (#8744)

### 개발 변경사항(영문)

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

본 버전에서는 2018.2 출시전 새로 추가된 기능에 문제가 발생하여 기능 제거 당시 적용되지 않은 번역 내용이 적용되었습니다.

## 2018.2

이번 버전의 주 기능들: PC Kindle 앱에서의 표 탐색 지원; 휴먼웨어 브레일노트 터치 및 Brailliant BI14 지원 추가; OneCore 및 Sapi5  음성 엔진 지원 향상; Microsoft Outlook 지원 향상 등입니다.

### 새로운 기능

* 행 및 열 병합 정보가 음성 및 점자로 출력되도록 함. (#2642)
* Google Docs 사용 시 점자 지원 모드 사용 중 표 탐색 기능이 작동하도록 함. (#7946)
* PC Kindle 앱 사용 시 표 탐색 기능이 추가됨. (#7977)
* 브레일노트 터치 및 Brailliant BI 14(USB 및 블루투스 연결) 지원 추가. (#6524)
* Windows 10 Fall Creators Update 이상 사용 시 계산기 및 Windows Store 앱 사용 시 앱 알림 텍스트를 확인할 수 있음. (#7984)
* 점자 표기법: 리투아니아어 8점, 우크라이나어 및 몽골어 2종 점자 추가. (#7839)
* 점자 커서 위치의 서식 정보를 알려주는 명령(script) 추가. (#7106)
* NVDA 업데이트 설치 시 업데이트를 미룰 수 있는 기능 추가. (#4263) 
* 새 NVDA 언어: 몽골어, 스위스 독일어 추가..
* 점자 키보드에서 control, shift, alt, windows 및 NVDA 키 토글 및 다른 키들과 조합할 수 있음(예: control+s). (#7306) 
 * 토글키에 대한 단춧키를 할당하려면 단춧키 설정에 있는 시스템 키 점자 입력 항목에서 설정할 수 있음.
* Handy Tech Braillino 및 Modular(옛 펌웨어 사용 시) 디스플레이 지원 복원. (#8016)
* Handy Tech 디스플레이 사용 시 시간 및 날짜를 지원하는 모델(예: Active Braille 및 Active Star)의 시계가 시스템 시계보다 5초 이상 틀린 경우 NVDA가 디스플레이의 시각을 동기화할 수 있음.  (#8016)
* NVDA 환경 프로필을 임시로 해제할 수 있는 명령이 추가됨(단춧키 설정 대화상자에서 핫키 추가 바람). (#4935)

### 변경사항

* 추가 기능 관리자에서 추가 기능 사용 여부 관련 메시지가 변경됨("실행" 대신 "사용"으로 출력되도록 함). (#7929)
* Liblouis 점자 변환기 3.5.0 버전 사용. (#7839)
* 이전 "리투아니아어 점자"표를 "리투아니아어 6점 점자"로 변경하여 8점 점자표와의 혼동을 줄임. (#7839)
* 케나다 프랑스어 1종 및 2종 점자표를 통합 프랑스어 8점 점자 및 2종 점자로 통일함. (#7839)
* Alva BC6, EuroBraille 및 Papenmeier 디스플레이 사용 시 윗줄 라우팅 버튼을 통해 점자 커서 위치의 서식 정보를 보여주도록 함. (#7106)
* 2종 점자표 사용 시 점자 입력을 지원하지 않는 컨트롤(예: 점자 커서가 없거나 브라우즈 모드 사용시)에서 1종 점자 입력 모드로 전환하도록 함. (#7306)
* Outlook 달력에서 시간대 또는 일정이 하루 전체로 설정되었을 때 일정 내용이 이전보다 간략하게 출력되도록 함. (#7949)
* 여러 대화상자에 흩어져 있던 NVDA 설정이 한 곳으로 통합됨(NVDA 메뉴 -> 설정 -> NVDA 설정). (#577)
* Windows 10 사용 시 기본 음성 엔진을 eSpeak에서 Windows oneCore로 변경함. (#8176)

### 버그 수정내역

* Windows 10 사용 시 설정 화면에서 Microsoft 계정으로 전환 시 이메일 주소 입력 후 포커스된 컨트롤을 읽지 못하던 문제 수정. (#7997)
* Microsoft Edge 사용 시 이전 페이지로 이동 후 새 페이지를 읽지 않던 문제 수정. (#7997)
* Windows 10에서 핀을 사용하여 로그인 시 입력된 핀의 마지막 글자를 읽던 문제 수정. (#7908)
* Chrome과 FireFox에서 브라우즈 모드 사용 중 탭 또는 한 글자 명령을 사용하여 체크박스나 라디오 버튼으로 이동 시 컨트롤 레이블이 두번 출력되던 문제 수정. (#7960)
* aria-current false 값이 "false"로 출력되도록 함(이전에는 "true"로 잘못 출력되었음). (#7892).
* Windows OneCore 음성 엔진 사용 시 특정 음성이 제거되었을 때 음성 엔진이 작동하지 않던 문제 수정. (#7553)
* Windows OneCore 음성 엔진 사용 시 음성 변경 반응 속도가 빨라짐. (#7999)
* 덴마크어 8점 약자와 같은 점자표 사용 시 대문자 표기 점형이 이상하게 출력되는 등 점자 출력이 깨지던 문제 수정. (#7526, #7693)
* Microsoft Word 사용 시 더 많은 bullet 글자를 NVDA가 인식하도록 함. (#6778)
* 서식 정보 명령을 여러번 실행 시 리뷰 커서 위치 변경 및 잘못된 정보가 출력되던 문제 수정. (#7869)
* 점자 입력 사용 시 2종 점자를 쓸 수 없는 경우 약자 입력이 쓰이지 않도록 함(예: 편집창 밖에서 약자 단어를 입력하거나 브라우즈 모드 사용 시). (#7306)
* Handy Tech Easy Braille 및 Braille Wave 디스플레이 사용 시 연결 상태가 좋지 않던 문제 수정. (#8016)
* Windows 8 이상 사용 시 quick link menu(Windows+X)를 열 때나 메뉴 항목을 선택 시 "알 수 없음" 메시지가 출력되던 문제 수정. (#8137)
* 힘스 디스플레이 사용 시 모델별 버튼 명령이 사용 설명서에 나열된 대로 동작하도록 함. (#8096)
* Firefox나 Internet Explorer와 같은 프로그램에서 컨텐츠에 접근할 수 없거나 "알 수 없을"를 알릴 때 NVDA는 시스템 COM 등록 문제를 해결할 수 있음. (#2807)
* 작업 관리자 사용 시 프로그램의 버그 때문에 특정 프로세스 정보를 확인할 수 없던 문제 수정. (#8147)
* 최신 Microsoft SAPI5 음성 엔진의 반응 속도(특히 음성 출력 끝부분)가 향상됨(이로 인해 본 음성 엔진을 사용하여 텍스트 읽을 시 NVDA의 반응 속도가 향상됨). (#8174)
* 최신 Windows 버전에서 시스템 시계를 탐색할 때 LTR 또는 RTL 마크가 점자나 음성으로 출력되던 문제 수정. (#5729)
* 힘스 스마트 비틀 스크롤 키 사용 시 명령 인식 정확도가 향상됨. (#6086)
* 일부 텍스트 컨트롤, 특히 Delphi 응용 프로그램에서 편집 및 탐색에 대해 제공된 정보가 안정적으로 동작하도록 개선. (#636, #8102)
* Windows 10 RS5에서 alt+tab을 사용하여 작업 전환 시 불필요한 정보가 출력되지 않도록 함. (#8258)

### 개발 변경사항(영문)

* The developer info for UIA objects now contains a list of the UIA patterns available. (#5712)
* App modules can now force certain windows to always use UIA by implementing the isGoodUIAWindow method. (#7961)
* The hidden boolean flag "outputPass1Only" in the braille section of the configuration has again been removed. Liblouis no longer supports pass 1 only output. (#7839)

## 2018.1.1

본 버전은 윈도우 10 1803에서 발견된 OneCore 엔진 문제(음 높이 및 속도 문제)를 수정한 버전입니다. (#8082)  

## 2018.1

이번 버전의 주 기능들: Microsoft Word 및 파워포인트내 차트 접근 지원; Eurobraille과 구형 Optelec/프로토컬 컨버터 디스플레이 지원 추가; Optelec 및 힘스 디스플레이 지원 향상; FireFox 58 이상에서의 반응 속도 향상 등입니다.

### 새로운 기능

* Microsoft Excel에서만 지원하던 차트 탐색 기능을 Word와 PowerPoint로도 확대함. (#7046)
 * Microsoft Word 사용 시 브라우즈 모드를 사용하여 차트로 이동 후 엔터를 눌러 차트에 접근할 수 있음.
 * Microsoft PowerPoint에서 슬라이드 편집 중 차트 객체로 이동하여 엔터나 스페이스를 눌러 차트에 접근할 수 있음.
 * 차트에서 빠져나가려면 escape 키를 눌러야 함.
* 새 NVDA 언어: 키르기즈스탄어 추가..
* VitalSource Bookshelf 지원 추가. (#7155)
* Alva Braille Voyager/Satellite 디스플레이에 사용되는 프로토콜을 BC6 버전으로 변환하는 장치인 Optelec 프로토콜 컨버터 지원 추가. (#6731)
* ALVA 640 Comfort 디스플레이 사용 시 점자 입력 기능이 작동하도록 함. (#7733) 
 * 이 디스플레이 외 다른 BC6 디스플레이 사용 시 펌웨어 3.0.0 사용 바람.
* Google 시트 점자 모드 지원 추가(기초 단계임). (#7935)
* Eurobraille Esys, Esytime 및 Iris 점자 디스플레이 지원 추가. (#7488)

### 변경사항

* 힘스 한소네/브레일 엣지/스마트 비틀과 힘스 싱크브레일 점자 디스플레이 드라이버를 하나로 통일함. 이로 인해 싱크브레일 사용시 새 드라이버가 동작되도록 함. (#7459) 
 * 이로 인해 특정 명령(특히 스크롤 키 명령)이 통힐됨.
* 터치 키보드 사용하여 글자 입력 시 다른 객체처럼 한 손가락을 두번 태핑해야 함. (#7309)
 * 이전 입력 방식(터치 타이핑)을 사용하려면 NVDA 설정 메뉴에 추가된 터치 기능 설정 대화상자를 통해 설정 바람.
* 점자 연계 커서가 자동으로 포커스 또는 리뷰 모드로 전환될 수 있도록 함. (#2385) 
 * 포커스된 객체에서 객체 탐색 또는 리뷰 명령을 사용 시(단 스크롤 기능은 지원 안 함) 점자가 리뷰 커서에 연계되도록 함.

### 버그 수정내역

* NVDA 설치 경로에 ASCII 이외 글자가 있는 경우 브라우즈 모드를 사용하는 메시지(예: NVDA+f를 두 번 눌러 서식 정보를 출력 시)가 열리지 않던 문제 수정. (#7474)
* 다른 앱에서 Spotify로 전환 시 포커스가 제대로 복원되도록 함. (#7689)
* 윈도우 10 Fall Creators Update 사용 시 폴더 접근 제어(Controlled Folder Access) 사용 시 NVDA가 끝까지 설치되지 않던 문제 수정. (#7696)
* 힘스 스마트 비틀 스크롤 키 사용 시 명령 인식 정확도가 향상됨. (#6086)
* 모질라 FireFox 58 이상 사용 시 대용량 콘텐츠를 탐색 시 NVDA의 반응 속도가 개선됨. (#7719)
* Microsoft Outlook 사용 시 표가 있는 이메일 읽을 시 NVDA가 다운되던 문제 수정. (#6827)
* 점자 입력 사용 시 점자 키보드에 할당된 시스템 기능키와 다른 기능키를 조합한 명령을 사용할 수 있음(모델별로 다름). (#7783)
* 모질라 FireFox 사용 시 LastPass와 bitwarden과 같은 추가 기능 팝업에서 브라우즈 모드가 작동하도록 함. (#7809)
* FireFox나 Chrome 사용 시 프로그램이 다운되었을 때 나타나던 포커스 변경 시 NVDA 반응 속도 저하 문제 수정. (#7818)
* Chicken Nugget와 같은 트위터 앱에서 280자 트위트 읽을 시 마지막 20개 글자가 출력되지 않던 문제 수정. (#7828)
* 텍스트가 선택되었을 때 음성 엔진 언어로 기호가 출력되도록 함. (#7687)
* 최신 Office 365 사용 시 방향키를 이용한 Excel 차트 탐색 기능이 복원됨. (#7046)
* 컨트롤 정보를 음성 및 점자로 출력 시 컨트롤 상태 출력 순서가 통일됨. (#7076)
* 윈도우 10 Mail 앱과 같은 앱 사용 시 backspace를 눌렀을 때 삭제된 글자가 출력되지 않던 문제 수정. (#7456)
* Hims 한소네 5/폴라리스 점자키가 제대로 인식되도록 함. (#7865)
* 윈도우 7 사용 시 다른 앱이 특정 Visual Studio 2017 redistributables를 설치한 경우 NVDA 시작 시 특정 api-ms dll에 대한 오류 메시지가 출력되지 않도록 함. (#7975)

### 개발 변경사항(영문)

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

이번 버전의 주 기능들: 웹 브라우저 지원 향상(특히 웹 대화상자 탐색 지원 향상); 필드 그룹 읽기 향상; Windows Defender Application Guard와 ARM64와 같은 최신 Windows 10 기술 지원; 베터리 및 화면 방향 변경 알림 등입니다.
참고로 이번 버전부터는 Windows XP와 비스타 지원이 중단됩니다. NVDA를 사용하려면 Windows 7 서비스팩 1 이상을 사용하여야 합니다.

### 새로운 기능

* 브라우즈 모드 사용 시 컨테이너 요소의 시작 및 끝 명령(comma/shift+comma)을 사용하여 랜드마크의 시작 또는 끝으로 옮길 수 있음. (#5482)
* FireFox, Chrome 및 인터넷 익스플로러 사용 시 편집창 및 폼 필드 첫 글자 명령을 사용하여 rich edit 편집창(예: contentEditable)으로 이동할 수 있음. (#5534)
* 웹 브라우저 사용 시 요소 목록 대화상자를 통해 폼 필드와 버튼 목록을 확인할 수 있음. (#588)
* ARM64 기반 Windows 10 지원 추가. (#7508)
* Kindle 사용 시 접근 가능한 수학 컨텐츠 읽기 및 탐색이 가능함 (초기 지원 단계임). (#7536)
* Azardi 독서기 앱 지원 추가. (#5848)
* 추가 기능 업데이트 시 추가 기능 버전이 표시되도록 함. (#5324)
* NVDA 실행 명령 목록에 휴대용 버전 생성 관련 명령 추가. (#6329)
* Windows 10 Fall Creators Update/Windows Defender Application Guard/Microsoft Edge 지원 추가. (#7600)
* 노트북 또는 테블릿에서 NVDA 실행 시 전원 연결 및 화면 방향 변경 정보가 출력되도록 함. (#4574, #4612)
* 새 NVDA 언어: 마세도니아어 추가.
* 점자 표기법: 크로아티아어 1종 점자 및 베트남어 1종 점자 추가. (#7518, #7565)
* Handy Tech Actilino 점자디스플레이 지원 추가. (#7590)
* Handy Tech 점자디스플레이 사용시 점자 입력 지원 추가. (#7590)

### 변경사항

* 최소 지원 운영체제가 Windows 7 Service Pack 1 또는 Windows 서버 2008 R2 Service Pack 1로 변경됨. (#7546)
* FireFox 및 Chrome에서 웹 대화상자가 열렸을 때 웹 앱에 위치하지 않는한 브라우즈 모드가 작동하도록 함. (#4493)
* 웹 브라우저 사용 시 효율성을 높이기 위해 탭 또는 첫 글자 명령을 사용하여 사이트 탐색 시 컨테이너 요소(목록, 표 등)의 끝 메시지가 출력되지 않도록 함. (#2591)
* FireFox 및 Chrome에서 브라우즈 모드 사용 시 탭 또는 첫 글자 명령을 사용하여 폼 필드로 옮길시 필드 그룹 이름이 출력되도록 함. (#3321)
* 부라우즈 모드 사용 시 다음 및 이전 임베디드 객체(o/shift+o) 명령을 통해 오디오, 비디오 및 aria 앱 또는 대화상자로 표시된 요소로 이동할 수 있음. (#7239)
* 이스피크 NG 음성 엔진 1.49.2 사용. (#7385)
* 상태 표시줄 명령을 세 번 눌러 표시줄 내용을 클립보드에 복사할 수 있음. (#1785)
* Baum 디스플레이 사용 시 모델(예: VarioUltra 또는 Pronto)별로 단춧키를 설정할 수 있음. (#7517)
* 브라우즈 모드 요소 목록 대화상자 내 요소 이름 검색 핫키가 alt+f에서 alt+e로 변경됨. (#7569)
* 부라우즈 모드 사용시 레이아웃 테이블 인식 토글 명령 추가(명령 할당 안 됨). (#7634)
* Liblouis 점자 변환기 3.3.0 버전 사용. (#7565)
* 발음 사전 내 정규 표현 라디오 버튼 핫키 변경(alt+r에서 alt+e로 변경됨). (#6782)
* 발음 사전 파일 버전 추가 및 'speechDicts/voiceDicts.v1' 폴더로 옮겨짐. (#7592)
* NVDA 임시 버전 사용 시 버전이 할당된 파일(발음 사전, 사용자 설정 등)의 변경된 내용이 저장되지 않도록 함. (#7688)
* Handy Tech Braillino, Bookworm 및 Modular(옛 펌웨어 버전 사용시) 디스플레이를 사용하려면 Handy Tech Universal Driver 및 NVDA 추가 기능을 설치 바람. (#7590)

### 버그 수정내역

* Microsoft Word를 포함한 여러 프로그램 사용 시 링크가 점자로 표기되도록 함. (#6780)
* FireFox 및 Chrome 사용 시 수많은 탭이 열렸을 때 NVDA의 반응 속도가 느려지던 문제 수정. (#3138)
* MDV Lilli 점자 디스플레이 사용 시 라우팅 버튼을 눌렀을때 커서가 점자셀보다 한칸 앞에 위치하던 문제 수정. (#7469)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 입력 필수 폼 필드(특히 HTML5 입력 필수 속성)가 인식되도록 함. (#7321)
* WordPad와 점자 디스플레이 사용 시 왼쪽으로 텍스트가 배치된 문서에서 아랍어 입력 시 입력된 내용이 점자로 출력되지 않던 문제 수정. (#511)
* FireFox에서 브라우즈 모드 사용 시 컨트롤 레이블 컨텐츠가 없을때 접근성 레이블 내용이 출력되도록 함. (#4773)
* Windows 10 Creators Update 사용 시 FireFox 사용 도중 NVDA를 재시작할 때 브라우즈 모드가 작동하지 않던 문제 수정. (#7269)
* FireFox가 포커스된 후 NVDA를 재시작한 후 브라우즈 모드가 작동하지 않던 문제 수정(alt+tab을 눌러 포커스를 FireFox로 옮겨야 함). (#5758)
* FireFox를 설치하지 않고도 Chrome에서 수학 컨텐츠를 읽을 수 있음. (#7308)
* NVDA를 설치한 후 재부팅하기 전 NVDA 사용 시 운영체제 및 여러 앱이 다운되던 문제가 어느 정도 해결됨. (#7563)
* 문자 인식(예: NVDA+r) 도중 탐색 객체가 사라졌을 때 오류 메시지가 출력되도록 함. (#7567)
* 왼쪽 bumper bar가 장착된 Freedom Scientific 점자 디스플레이 사용 시 점자를 뒤로 스크롤할 수 없던 문제 수정. (#7713)

### 개발 변경사항(영문)

* "scons tests" now checks that translatable strings have translator comments. You can also run this alone with "scons checkPot". (#7492)
* There is now a new extensionPoints module which provides a generic framework to enable code extensibility at specific points in the code. This allows interested parties to register to be notified when some action occurs (extensionPoints.Action), to modify a specific kind of data (extensionPoints.Filter) or to participate in deciding whether something will be done (extensionPoints.Decider). (#3393)
* You can now register to be notified about configuration profile switches via the config.configProfileSwitched Action. (#3393)
* Braille display gestures that emulate system keyboard key modifiers (such as control and alt) can now be combined with other emulated system keyboard keys without explicit definition. (#6213)
 * For example, if you have a key on your display bound to the alt key and another display key to downArrow, combining these keys will result in the emulation of alt+downArrow.
* The braille.BrailleDisplayGesture class now has an extra model property. If provided, pressing a key will generate an additional, model specific gesture identifier. This allows a user to bind gestures limited to a specific braille display model.
 * See the baum driver as an example for this new functionality.
* NVDA is now compiled with Visual Studio 2017 and the Windows 10 SDK. (#7568)

## 2017.3

이번 버전의 주 기능들: 점자 약자 입력; 윈도우 10에서 제공하는 OneCore 보이스 지원; 윈도우 10 OCR을 통한 문자 인식; 점자 및 웹 지원 기능 향상 등입니다.

### 새로운 기능

* 점자 설정 대화상자에 "점자 메시지를 영구적으로 표시" 설정 추가. (#6669)
* Microsoft Outlook 메시지 목록 탐색 시 메시지 플래그가 출력되도록 함. (#6374)
* Microsoft PowerPoint에서 슬라이드 편집 시 도형 모양(예: 삼각형, 동그라미, 비디오, 화살표 등)이 출력되도록 함. (#7111)
* 구글 Chrome 사용 시 수학 컨텐츠(특히 MathML로 표기된 내용) 탐색 가능. (#7184)
* 윈도우 10 사용 시 윈도우 OneCore(Mobile) 보이스 지원 추가 및 본 옵션이 음성 엔진 목록에 추가됨. (#6159)
* 레지스트리를 통해 NVDA 설정이 사용자의 local application data 폴더에 저장되도록 설정할 수 있음. 사용 설명서 내 시스템 환경 옵션 섹션을 참조바람. (#6812)
* 웹 브라우저 사용 시 필드의 place holder(aria-placeholder) 값이 인식되도록 함. (#7004)
* Microsoft Word에서 브라우즈 모드 사용 시 w/shift+w를 사용하여 철자 오류 탐색 가능. (#6942)
* Microsoft Outlook 내 일정 대화상자 내 날짜 선택 컨트롤 지원 추가. (#7217)
* 윈도우 10 Mail 받는 사람/CC 필드 및 설정 앱과 같은 컨트롤에서 검색 결과 선택 시 결과가 자동으로 출력되도록 함. (#6241)
* 윈도우 10 사용 시 시작 메뉴, Mail 앱 및 설정 앱과 같은 곳에서 검색 결과가 나타날때 이것을 사운드로 알릴 수 있도록 함. (#6241)
* 스카이프 비지니스 사용 시 특정 알림(예: 상대방에게서 메시지를 받았을 때)이 자동으로 출력되도록 함.  (#7281)
* 스카이프 비지니스 사용 시 체팅 도중 새 메시지가 자동으로 출력되도록 함. (#7286)
* Microsoft Edge 사용 시 파일 다운로드 시작과 같은 알림 내용이 자동으로 출력되도록 함. (#7281)
* 점자 키보드가 장착된 점자 디스플레이 사용 시 키보드를 사용하여 정자 및 약자 점자 입력 가능. 사용설명서 내 점자 입력 섹션을 참조 바람. (#2439)
* 유니코드 점자 코드를 사용하여 유니코드 점형을 입력할 수 있음. (#6449)
* 타이완에서 보급되는 SuperBraille 디스플레이 지원 추가. (#7352)
* 점자 표기법: 덴마크어 8점 컴퓨터 점자, 리투아니아어, 페르시아어 8점 컴퓨터 점자, 페르시아어 1종 점자및 슬로베니아어 8점 컴퓨터 점자 추가. (#6188, #6550, #6773, #7367)
* 미국 영어 8점 컴퓨터 점자 코드 지원 향상(bullet, 유로, 및 엑센트 글자 추가). (#6836)
* 윈도우 10 사용 시 윈도우 10이 제공하는 OCR 기능을 사용하여 이미지나 접근이 불편한 앱에서 문자 인식이 가능. (#7361)
 * 윈도우 10 OCR 설정을 통해 인식 언어를 지정할 수 있음.
 * 현재 객체의 내용을 문자 인식하려면 NVDA+r을 누르기 바람.
 * 사용설명서 내 문자 인식 섹션을 참조바람.
* 점자 설정에 추가된 "포커스 내용 출력" 설정을 통해 점자 디스플레이에 포커스 관련 세부 내용이 어떻게 출렭될 것인지를 설정할 수 있음. (#217)
 * 예를 들어 "포커스 내용 변경 시 출력" 또는 "뒤로 스크롤 시 출력"을 선택하고 목록이나 메뉴를 탐색할 때 내용의 위치가 계속 변경되는 불편함이 어느 정도 해결이 됨.
 * 더 자세한 정보 및 특정 사례에 대해서는 사용설명서 내 "포커스 내용 출력" 섹션을 참고바람.
* FireFox와 Chrome 사용 시 컨텐츠 일부만 보여지는 spreadsheet(특히 ARIA 1.1에 추가된 aria-rowcount, aria-colcount, aria-rowindex 및 aria-colindex 속성이 적용된 complex dynamic grid) 탐색 지원 추가.  (#7410)

### 변경사항

* NVDA를 곧바로 재시작할 수 있는 명령(script_restart, 명령 할당 않됌) 추가. (#6396)
* NVDA 시작 대화상자에서 키보드 레이아웃을 설정할 수 있음. (#6863)
* 점자 사용 시 더 많은 컨트롤, 상태 및 랜드마크 정보 내용이 간소화됨. 사용설명서 내 "점자 사용 시 컨트롤, 상태 및 랜드마크 정보 내용" 섹션 참고 바람. (#7188, #3975)
* 이스피크 NG 음성 엔진 1.49.1 사용. (#7280)
* 점자 설정 대화상자 내 점자 입력 및 출력 표 목록이 가나다순으로 정렬되어 나타나도록 함. (#6113)
* Liblouis 점자 변환기 3.2.0 버전 사용. (#6935)
* 기본 점자 표기법이 영어 통합 점자(UEB) 1종 점자로 변경됨. (#6952)
* 본 버전 이후로 점자 디스플레이 사용 시 포커스된 객체의 내용이 변경되었을 때에만 세부 내용이 출력되도록 함. (#217)
 * 이전에는 같은 종류의 객체(예: 목록 항목)에 포커스된 경우 같은 세부 내용이 출력되었었음.
 * 이전 방식을 사용하려면 점자 설정 내 포커스 내용 출력에서 "항상 출력" 옵션을 선택 바람.
* 점자 사용 시 연계 커서(포커스 또는 리뷰(에 따라 커서 점형을 다르게 표시할 수 있음. (#7122)
* NVDA 로고가 변경됨. 새 로고는 NV Access의 로고에서 사용된 보라색 바탕에 "NVDA"가 붙여진 텍스트가 하얀색 색상으로 표시되도록 하여 어느 색 바탕에서나 찾기 쉽도록 함. (#7446)

### 버그 수정내역

* Chrome에서 브라우즈 모드 사용 시 편집 가능 div 요소명이 요소의 값으로 출력되지 않도록 함. (#7153)
* Microsoft Word에서 빈 문서가 열린 상태에서 브라우즈 모드 사용 시 end 키를 누를 때 RuntimeError가 나지 않도록 함. (#7009)
* Microsoft Edge 사용 시 특정 요소가 ARIA 문서 롤로 표기되었을 때 브라우즈 모드가 제대로 작동하지 않던 문제 수정. (#6998)
* 브라우즈 모드 사용 시 줄 끝에서 shift+end키를 눌러 줄 끝까지 선택(또는 선택 해제)이 가능하도록 함. (#7157)
* 진행률 대화상자에서 진행률이 변경될 때 변경된 컨텐츠가 점자로 출력되도록 함(예: NVDA 업데이트 대화상자 내 다운로드 경과 시간 확인이 가능해짐). (#6862)
* 윈도우 10 사용 시 특정 콤보박스(예: 설정 앱 내 자동 실행 옵션)에서 설정 값 변경 시 새 설정 값이 출력되지 않던 문제 수정. (#6337).
* Microsoft Outlook 사용 시 새 미팅 또는 일정 대화상자 내 필요 없는 정보가 출력되던 문제 수정. (#7216)
* 값이 없는 징행률 막대(예: 업데이트 확인 대화상자)의 값을 출력 시 만약 진행률 출력이 비프음이 아닌 설정이 적용된 경우 비프음이 출력되지 않도록 함. (#6759)
* Microsoft Excel 2003 및 2007 사용 시 방향키로 worksheet 셀을 탐색할 수 없던 문제 수정. (#8243)
* 윈도우 10 크리에이터 업데이트 및 이후 버전의 Mail 앱 사용 시 브라우즈 모드가 작동하지 않던 문제 수정. (#7289)
* 점자 키보드가 탑재된 점자 디스플레이 사용 시 거의 모든 디스플레이에서 7점을 눌러 이전 글자를 삭제하고 8점을 눌러 엔터키를 입력하도록 변경됨. (#6054)
* 편집창에서 캐럿을 옮길 때(예: 방향키 사용 또는 백스페이스를 누를 때) 거의 대부분의 편집창에서(예: Chrome 및 터미널 창) NVDA의 음성 반응이 빨라지도록 함. (#6424)
* Microsoft Outlook 2016 내 signature 대화상자 내용을 탐색할 수 있도록 함. (#7253)
* Java Swing 기반 프로그램 사용 중 표 탐색 시 가끔 사용 중인 프로그램이 다운되던 문제 수정. (#6992)
* 윈도우 10 크리에이터 업데이트 사용 시 토스트 알림 내용이 여러번 반복되어 출력되던 문제 수정. (#7128)
* 윈도우 10 시작 메뉴에서 텍스트 입력 후 엔터키를 눌렀을 때 입력된 검색 텍스트가 출력되지 않도록 함. (#7370)
* Microsoft Edge 사용 시 첫 글자를 이용하여 헤딩 탐색 시 명령 반응 속도가 개선됨.  (#7343)
* Microsoft Edge 브라우즈 모드 사용 시 특정 문서 내용(예: Wordpress 2015 테마)을 탐색할 수 없던 문제 수정. (#7143)
* Microsoft Edge 사용 시 영어 외 타국어 사용 시 랜드마크 이름이 제대로 출력되지 않던 문제 수정. (#7328)
* 점자 디스플레이의 셀 길이보다 긴 텍스트를 선택할 때 선택 내용이 점자로 제대로 표시되도록 함(예: shift+아래 화살표를 눌러 여러줄 선택 시 마지막 줄의 내용이 점자로 표시되도록 함). (#5770)
* FireFox 사용 시 twitter.com에서 트위트를 볼때 "섹션"이 반복되어 출력되던 문제 수정. (#5741)
* 레이아웃 표에서 문서 서식 대화상자 내 레이아웃 표 알림 옵션이 적용되지 않는한 표 셀 탐색 명령을 사용할 수 없도록 변경됨. (#7382)
* FireFox와 Chrome에서 브라우즈 모드를 사용하여 표를 탐색 시 셀 탐색 명령이 표에 표시되지 않은 셀을 건너뛰도록 함. (#6652, #5655)

### 개발 변경사항(영문)

* Timestamps in the log now include milliseconds. (#7163)
* NVDA must now be built with Visual Studio Community 2015. Visual Studio Express is no longer supported. (#7110)
 * The Windows 10 Tools and SDK are now also required, which can be enabled when installing Visual Studio.
 * See the Installed Dependencies section of the readme for additional details.
* Support for content recognizers such as OCR and image description tools can be easily implemented using the new contentRecog package. (#7361)
* The Python json package is now included in NVDA binary builds. (#3050)

## 2017.2

이번 버전의 주 기능들: 윈도우 10 Creators Update 사용 시 오디오 도킹 지원 복원; 브라우즈 모드에서의 텍스트 선택 버그 수정(특히 전체 선택 관련 문제 해결); Edge 브라우저 지원 향상; 브라우저 모드에서의 현재 아이템(aria-current) 인식 지원 등입니다.

### 새로운 기능

* Microsoft Excel 사용 시 NVDA+f 명령을 사용하여 셀 테두리 정보를 확인할 수 있음. (#3044)
* 웹 브라우저 사용 시 aria-current 요소 인식 기능 추가. (#6358)
* Microsoft Edge 사용 시 자동 언어 변경 기능 지원 추가. (#6852)
* 윈도우 10 Enterprise LTSB (Long-Term Servicing Branch)및 서버 버전 윈도우 계산기 앱 지원 추가. (#6914)
* 현재 줄 읽기 명령을 세번 실행 시 줄 철자가 풀이되어 출력되도록 함. (#6893)
* 새 NVDA 언어: 미얀마어 추가.
* Unicode 위/아래 화살표 기호 및 분수 기호들이 음성으로 출력되도록 함. (#3805)

### 변경사항

* 심플 리뷰 모드를 사용하여 UIA가 적용된 앱 탐색 시 탐색 효율성을 높이기 위해 컨텐츠가 없는 컨테이너 요소를 건너뛰도록 함. (#6948, #6950) 

### 버그 수정내역

* 브라우즈 모드 사용 시 웹 페이지 메뉴 아이템일 활성화될 수 있도록 함. (#6735)
* "사용자 프로필 삭제" 대화상자에서 escape를 누를 시 본 대화상자가 닫혀지도록 함. (#6851)
* - 모질라 FireFox와 같은 Gecko 기반 프로그램에서 멀티프로세스 기능 사용 시 NVDA가 다운되던 문제 수정. (#6885)
* 화면 탐색 모드 사용 시 투명한 색 바탕의 텍스트의 배경 색상 정보의 정확도를 높임. (#6467)
* 인터넷 익스플로러 11 사용 시 웹 페이지에서 제공한 컨트롤 설명 내용(특히 iframe내 aria-describedby 및 다중 ID 제공 시)이 제대로 출력되도록 함. (#5784)
* 윈도우 10 Creators Update 내 오디오 도킹()도킹 해제, 음성 출력 시 도킹, 도킹 사용) 기능 복원. (#6933)
* 핫키 정보가 없는 UIA 객체를 탐색할 수 없던 문제 수정. (#6779)
* 특정 UIA 객체 핫키 정보 출력 중 두 공백 문자가 추가되어 출력되던 문제 수정. (#6790)
* 힘스 디스플레이 사용 시 특정 명령(예: space+4점)가 제대로 동작하지 않던 문제 수정. (#3157)
* 영어 외 다른 특정 언어가 설치된 시스템에서 시리얼 포트로 연결된 점자 디스플레이 사용 시 특정 상황에서 디스플레이와의 연결이 실패하던 문제 수정. (#6845)
* 윈도우 종료시 NVDA 설정 파일이 깨지는 확률을 최소화하도록 함. 설정 저장시 설정이 임시 파일에 저장된 후 설정 파일을 덮어씌우도록 함. (#3165)
* 현재 줄 읽기 명령을 두번 실행 시 현재 사용중인 언어를 사용하여 철자가 발음되도록 함. (#6726)
* 윈도우 10 Creators Update/Microsoft Edge 사용 시 줄 단위 이동 속도가 최대 3배 빨라짐. (#6994)
* 윈도우 10 Creators Update/Microsoft Edge 문서에 포커스될 때 "Web Runtime grouping"이 출력되던 문제 수정. (#6948)
* 이전 및 추후 SecureCRT 버전 지원 추가. (#6302)
* Adobe Reader 사용 시 특정 PDF 문서(특히 ActualText 요소가 비었을 때)를 불러올때 Adobe Reader가 다운되던 문제 수정. (#7021, #7034)
* Microsoft Edge내 브라우즈 모드 사용 시 t/shift+t를 사용하여 표를 탐색 시 접근 가능한 표(ARIA grids)가 인식되지 않던 문제 수정. (#6977)
* 브라우즈 모드 사용 시 텍스트 선택후 shift+home을 눌렀을때 줄 처음부터 텍스트가 선택되지 않도록 함. (#5746)
* 브라우즈 모드 사용 시 캐럿이 문서 상단이 아닌 곳에 있을 때 전체 선택(control+a) 실행 시 모든 텍스트가 선택되지 않던 문제 수정. (#6909)
* 브라우즈 모드에서 흖지 않게 나타나던 텍스트 선택 관련 문제 수정. (#7131)

### 개발 변경사항(영문)

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

이번 버전의 주 기능들: Microsoft Word 내 섹션 및 텍스트 열 수 알림; Kindle PC 앱을 통한 책 독서; Edge 브라우저 지원 향상 등입니다.

### 새로운 기능

* Microsoft Word 사용 시 문서 서식 대화상자 내 쪽 수 알림 설정이 선택된 경우 섹션 끝 종류 및 순위가 출력되도록 함. (#5946)
* Microsoft Word 사용 시 문서 서식 대화상자내 쪽 수 알림 설정이 선택된 경우 텍스트 열이 출력되도록 함. (#5946)
* WordPad 사용 시 자동 언어 변경 기능 지원 추가. (#6555)
* Microsoft Edge 브라우즈 모드 사용 시 NVDA의 문자열 찾기 명령(NVDA+control+f) 사용 가능. (#6580)
* Microsoft Edge 브라우즈 모드 사용 시 버튼 탐색 명령(b/shift+b) 사용 가능. (#6577)
* Microsoft Excel에서 sheet를 복사 시 행 및 열 머릿말 정보도 복사되도록 함. (#6628)
* Kindle 앱 1.19 버전 지원(책 독서중 링크, 각주, 그래픽, 텍스트 하이라이트 및 사용자 노트 탐색 가능). 자세한 정보는 NVDA 사용설명서 내 "Kindle PC 앱" 섹션을 참고바람. (#6247, #6638)
* Microsoft Edge 브라우즈 모드에 표 탐색 명령 추가. (#6594)
* Microsoft Excel에서 리뷰 커서 위치 명령(NVDA+numpadDelete (desktop)/NVDA+delete (laptop))을 실행 시 worksheet와 현재 셀 위치가 출력되도록 함. (#6613)
* NVDA 종료 대화상자에 NVDA 재시작 및 디버그 정보 기록 옵션 추가. (#6689)

### 변경사항

* 점자 커서 깜박이 설정이 200 ms 이상으로 설정되도록 함(프로필 업그레이드 시 본 설정이 조정되도록 함). (#6470)
* 점자 설정에 점자 커서 깜박이 체크박스 추가함(이전에는 깜박이 설정을 0으로 설정하면 커서 깜박이가 꺼졌음). (#6470)
* eSpeak NG (commit e095f008, 10 January 2017)으로 업데이트됨. (#6717)
* 윈도우 10 Creators Update 사용 시 운영체제 사양 변경으로 인해 오디오 도킹 사용(always duck) 옵션을 사용할 수 없음(이전 윈도우 10 버전에는 적용되지 않음). (#6684)
* 윈도우 10 Creators Update 사용 시 운영체제 사양 변경으로 인해 음성 출력 시 오디오 도킹 사용 옵션 사양이 변경됨(음성 및 사운드 출력 시 배경음 볼륨이 낮추어지지 않은 상태에서 음성 출력이 되거나 음성 출력 후 곧바로 배경음 볼륨이 높아짐). (#6684)

### 버그 수정내역

* Microsoft Word 내 브라우즈 모드를 사용하여 긴 문서를 문단 단위로 이동 시 NVDA가 다운되던 문제 수정. (#6368)
* Microsoft Excel에서 워드로 표를 복사 시 복사된 표가 구조표(layout table)로 인식되던 문제 수정. (#5927)
* Microsoft Excel에서 보호 모드가 설정된 경우 글자 입력 시 경고음이 출력되도록 함(이전에는 실제로 입력되지 않은 글자가 출력되었음). (#6570)
* Microsoft Excel 사용 중 escape를 눌렀을 때 이전에 브라우즈 모드(NVDA+space)를 사용하다가 폼 필드에서 엔터를 눌러 포커스 모드로 전환한 이상 브라우즈 모드가 활성화되지 않도록 함. (#6569) 
* Microsoft Excel 사용 시 행 또는 열 전체가 병합될 때 NVDA가 다운되던 문제 수정. (#6216)
* Microsoft Excel 셀 텍스트의 잘려진/삐져나온 정보 출력이 향상됨. (#6472)
* 읽기 전용 체크박스가 인식되도록 함. (#6563)
* 오디오 장치가 없는 컴퓨터에 NVDA 설치 파일을 실행 시 오디오 출력 불가로 인한 로고 재생 관련 경고 대화상자가 나타나지 않도록 함. (#6289)
* Microsoft Excel 리본 탐색 시 사용할 수 없는 컨트롤의 사용 여부가 제대로 출력되도록 함. (#6430)
* 모든 창을 최소화할 때 "창"이 출력되던 문제 수정. (#6671)
* 윈도우 10 Creators Update에서 Microsoft Edge와 같은 유니버셜(Universal Windows Platform) 앱 사용 시 입력된 글자가 출력되도록 함. (#6017)
* 마우스 위치 추적 기능이 여러 모니터가 있는 컴퓨터의 모든 화면에서 동작함. (#6598)
* Windows Media Player 슬라이더 컨트롤에 포커스한 후 프로그램 종료 시 NVDA가 다운되던 문제 수정. (#5467)

### 개발 변경사항(영문)

* Profiles and configuration files are now automatically upgraded to meet the requirements of schema modifications. If there is an error during upgrade, a notification is shown, the configuration is reset and the old configuration file is available in the NVDA log at 'Info' level. (#6470)

## 2016.4

이번 버전의 주 기능들: Edge 브라우저 지원 향상; 브라우즈 모드를 통해 윈도우 10 Mail 앱에서 메시지 읽기; NVDA 대화상자 인터페이스 향상 등입니다.

### 새로운 기능

* 비프음을 사용하여 줄 들여쓰기 값을 알 수 있음(문서 서식 대화상자내 줄 들여쓰기 콤보 박스에서 설정 가능). (#5906)
* Orbit Reader 20 점자 디스플레이 지원 추가. (#6007)
* NVDA 시작 시 음성 출력 뷰어 실행 여부를 묻는 옵션 추가(음성 출력 뷰어에 추가된 체크박스를 통해 설정할 수 있음). (#5050)
* 음성 출력 뷰어 창을 열 때 이전에 사용하던 창 위치 및 크기가 적용되도록 함. (#5050)
* Microsoft Word 사용 시 Cross Reference 필드가 링크로 인식되도록 함(다른 링크처럼 동작할 수 있음). (#6102)
* Baum SuperVario2, Baum Vario 340 및 휴먼웨어 Brailliant2 점자 디스플레이 지원 추가. (#6116)
* 윈도우 10 Anniversary Update Edge 지원. (#6271)
* 윈도우 10 Mail 앱에서 이메일을 읽을때 브라우즈 모드가 작동되도록 함. (#6271)
* 새 NVDA 언어: 리투아니아어 추가.

### 변경사항

* Liblouis 점자 변환기 3.0.0 버전 사용. 특히 통합 영어 점자(UEB) 출력이 향상됨. (#6109, #4194, #6220, #6140)
* 추가 기능 관리자 내 추가 기능 사용(alt+e)/사용 않함(alt+d) 버튼 핫키 추가. (#6388)
* 여러 NVDA 대화상자 내 컨트롤 간격 및 배치가 조정됨. (#6317, #5548, #6342, #6343, #6349)
* 문서 서식 대화상자 컨텐츠가 스크롤되도록 변경됨. (#6348)
* 기호 발음 설정 대화상자 내 기호 목록 폭이 확대됨. (#6101)
* 웹브라우저 내에서 브라우즈 모드 사용 시 편집창(e/shift+e) 및 폼 필드(f/shift+f) 명령을 사용하여 읽기 전용 편집창으로 이동 가능. (#4164)
* 문서 서식 정보가 음성 및 점자로 출력되는 까닭에 문서 서식 설정 대화상자내 "Announce formatting 변경사항 after the cursor"을 "Report formatting 변경사항 after the cursor"로 고침(한국어는 이전 레이블 그대로 사용). (#6336)
* NVDA 시작 대화상자 인터페이스가 향상됨. (#6350)
* NVDA 대화상자 내 확인(OK) 및 취소(Cancel) 버튼이 화면 우측 하단에 위치하도록 함. (#6333)
* 숫자 입력을 필요로 하는 설정(예: 보이스 설정 내 대문자 음높이 변경율) 컨트롤이 스핀 컨트롤로 변경됨(원하는 값을 입력하거나 위/아래 방향키로 값을 변경할 수 있음). (#6099)
* 웹브라우저 사용 시 IFrame(문서내 문서) 컨트롤 정보 출력이 통일됨(특히 FireFox에서 IFrame을 "프레임"으로 출력하도록 함). (#6047)

### 버그 수정내역

* 음성 출력 뷰어 사용 중 NVDA 종료 시 특정 상황에서 오류가 발생하던 문제 수정. (#5050)
* 모질라 Firefox에서 브라우즈 모드 사용 시 이미지맵이 제대로 나타나지 않던 문제 수정. (#6051)
* 음성 발음 사전 대화상자에서 엔터를 누를 시 변경된 내용이 저장되고 대화상자가 닫히도록 함. (#6206)
* 입력 모드 변경값(한글/영어, 전값 모드/반값 모드 등)이 점자로도 출력되도록 함. (#5892, #5893)
* 추가 기능을 중지호 곧바로 추가 기능을 사용하도록(또는 반대로) 변경 시 이전 추가 기능 사용 유무 설정이 보이도록 함. (#6299)
* Microsoft Word 사용 시 머리말 내 쪽 수 정보 탐색 가능. (#6004)
* 기호 발음 설정 대화상자에서 마우스를 사용하여 기호 목록과 편집 필드를 오갈 수 있음. (#6312)
* Microsoft Word에서 브라우즈 모드 사용 중 특정 문서에 링크가 잘못 삽입되었을때 요소 목록 대화상자가 나타나지 않던 문제 수정. (#5886)
* 작업 표시줄 또는 alt+F4를 눌러 음성 출력 뷰어를 닫았을때 NVDA 메뉴에 있는 음성 뷰어 체크박스 정보가 뷰어 사용 유무를 제대로 표시하도록 함. (#6340)
* 설정 프로필, 웹 문서 탐색 및 화면 탐색 모드 기능들이 추가 기능 재등록 명령 실행 후 제대로 동작하지 않던 문제 수정. (#2892, #5380)
* 윈도우 10 사용 시 NVDA 일반 설정에 있는 언어 목록내 아라곤어 및 여러 항목이 제대로 표시되도록 함. (#6259)
* 시스템 키 명령(예: 점자 디스플레이를 통해 tab 키를 누를 시) 도움말 및 명령 정보가 현재 사용중인 NVDA 언어로 출력되도록 함(이전까지는 영어로 출력되었음). (#6212)
* 일반 설정을 통해 NVDA 언어 변경 시 NVDA가 재시작하기 전까지 새 언어가 적용되지 않도록 함. (#4561)
* 음성 발음 사전 항목 추가 시 기본값(pattern) 필드에 내용이 입력되어야 항목이 추가되도록 함. (#6412)
* 특정 시스템/상황에서 시리얼 포트 스케닝 도중 여러 점자 디스플레이 드라이버가 다운되던 문제 수정. (#6462)
* Microsoft Word에서  표 셀 이동 명령 사용 시  셀에 위치한 숫자 bullet 목록이 제대로 출력되도록 함. (#6446)
* 단춧키 설정을 통해 Handy Tech 점자 디스플레이에 할당된 명령을 변경할 수 있음. (#6461)
* Microsoft Excel 사용 시 엔터(일반 엔터 또는 numpad 엔터)를 눌렀을때 spreadsheet의 다음 행으로 이동했다는 메시지가 출력되도록 함. (#6500)
* iTunes 사용 시 iTunes Store, Apple Music 등에서 브라우즈 모드 사용 시 프로그램이 다운되던 문제 수정. (#6502)
* 64비트 모질라 및 Chrome 기반 앱 사용 도중 특정 상황에서 사용하던 앱이 다운되던 문제 수정. (#6497)
* FireFox multi-process 사용 시 브라우즈 모드 및 편집창 탐색 명령 사용 가능. (#6380)

### 개발 변경사항(영문)

* It is now possible to provide app modules for executables containing a dot (.) in their names. Dots are replaced with underscores (_). (#5323)
* The new gui.guiHelper module includes utilities to simplify the creation of wxPython GUIs, including automatic management of spacing. This facilitates better visual appearance and consistency, as well as easing creation of new GUIs for blind developers. (#6287)

## 2016.3

이번 버전의 주 기능들: 특정 추가 기능 일시 정지 기능 추가; 엑셀 내 폼 필드 지원; 색상 출력 향상; 여러 점자 디스플레이 관련 버그 수정 및 지원 향상; Microsoft Word 지원 향상 및 여러 버그 수정 등입니다.

### 새로운 기능

* 윈도우 10 Anniversary Update 사용 시 Microsoft Edge 브라우저내에서 브라우즈 모드를 사용하여 PDF 문서를 읽을 수 있음. (#5740)
* Microsoft Word 사용 시 취소선/이중 취소선이 적절하게 출력되도록 함. (#5800)
* Microsoft Word 내 표에 이름이 있는 경우 표 이름이 출력되고 표 설명이 있을 경우 브라우즈 모드의 긴 설명 핫키(NVDA+d)를 사용하여 확인할 수 있음. (#5943)
* Microsoft Word 사용 시 문단 배치 변경(alt+shift+아래쪽 화살표/alt+shift+위쪽 화살표)시 새 위치 정보가 출력되도록 함. (#5945)
* Microsoft Word 사용 시 줄 간격이 인식되도록 함(서식 정보 명령을 통해 확인 가능, 워드 명령을 통해 간격 변경 시 설정이 출력되도록 함, 문서 서식 설정에서 줄 간격 출력이 활성화된 후 각 줄로 이동 시 간격 변경이 출력되도록 함). (#2961)
* 인터넷 익스플로러 사용 시 HTML5 구조 요소가 인식되도록 함. (#5591)
* 문서 서식 대화상자에 추가된 주석 알림 체크박스를 통해 주석(예: Microsoft ㅜ어드내 주석) 출력을 설정할 수 있음. (#5108)
* 추가 기능 관리자를 통해 추가 기능을 일시 정지할 수 있음. (#3090)
* ALVA BC640/680 점자 디스플레이 사용 시 여러 명령 추가. (#5206)
* 점자 디스플레이를 현재 포커스된 객체로 이동할 수 있는 핫키 추가(현재 ALVA BC640/680 디스플레이에만 할당되어 있고 다른 디스플레이 사용자들은 단춧키 설정을 통해 핫키를 설정할 수 있음). (#5250)
* Microsoft Excel 폼 필드 탐색 가능(요소 목록 또는 브라우즈 모드를 사용하여 폼 필드로 이동할 수 있음). (#4953)
* 단춧키 설정을 사용하여 심플 리뷰 토글 핫키를 할당할 수 있음. (#6173)

### 변경사항

* NVDA의 색상 정보 출력 방식이 변경됨(주관적이고 익숙하지 않은 색상명 대신 9개의 잘 알려진 기본 샞조(color hue)와 3개의 색상 셰이드 및 밝기/흐리기가 출력되도록 함). (#6029)
* NVDA+F9/NVDA+F10 사용 시 F10을 한번 눌러 선택후 두번째 눌렀을때 복사하도록 변경됨. (#4636)
* eSpeak NG 음성 엔진 Master 11b1a7b(2016-622) 사용. (#6037)

### 버그 수정내역

* Microsoft Word에서 브라우즈 모드 사용 중 클립보드에 복사시 텍스트 서식이 적용되도록 함. (#5956)
* Microsoft Word 사용 시 워드 자체의 표 탐색 명령(alt+home, alt+end, alt+pageUp, alt+pageDown) 및 설정 명령(shift 추가)을 NVDA가 제대로 인식하도록 함. (#5961)
* Microsoft Word 대화상자에서의 객체 탐색 향상. (#6036)
* 특정 프로그램(예: Visual Studio 2015) 사용 시 핫키(예: control+c (복사))가 출력되지 않던 문제 수정. (#6021)
* 특정 시스템/상황에서 시리얼 포트 스케닝 도중 여러 점자 디스플레이 드라이버가 다운되던 문제 수정. (#6015)
* Microsoft ㅜ어드 사용 시 Office 테마가 색상 출력에 반영되도록 함(이를 통해 색상 출력 정확도가 향상됨). (#5997)
* 2016년 4월 이후 출시된 윈도우 10 빌드에서의 Microsoft Edge 브라우즈 모드 및 시작 메뉴 검색 결과 기능이 동작하도록 함. (#5955)
* Microsoft Word 사용 시 자동으로 표 머릿말 읽기가 설정되어 있고 표에 병합된 cell이 있는 경우 표 머릿말이 제대로 출력되도록 함. (#5926)
* 윈도우 10 Mail 엡 사용 시 NVDA를 사용하여 메시지 내용을 읽을 수 없던 문제 수정. (#5635) 
* 명령 출력 사용 시 lock(예: caps lock)이 반복되어 출력되지 않도록 함. (#5490)
* 윈도우 10 Anniversary Update 내 사용자 계정 컨트롤(UAC) 대화상자 내용이 출력되도록 함. (#5942)
* out-of-sight.net과 같은 사이트에서 사용중인 Web Conference Plugin에서 마이크 입력 관련 진행률 막대 정보 및 비프음이 들리지 않도록 함. (#5888)
* 브라우즈 모드의 다음 및 이전 찾기 기능 사용 시 검색 글자열 대소문자 구별 여부가 반영되도록 함. (#5522)
* 음성 발음 사전 항목 편집 시 잘못된 정규 표현(regular expression) 관련 피드백이 출력되도록 함. 또한 특정 발음 사전 내 정규 표현 관련 오류로 인해 NVDA가 다운되던 문제 수정. (#4834)
* 점자 디스플레이가 음답하지 않는 경우(예: 사용 도중 디스플레이와의 연결이 끊켰을때) 디스플레이 사용이 일시 정지되도록 함. (#1555)
* 특정 상황에서 브라우즈 모드 요소 목록 사용 시 요소 필터링 속도가 향상됨. (#6126)
* Microsoft Excel에서 배경 패턴 레이블 출력 시 NVDA가 엑셀 자체에서 사용하는 레이블을 사용하도록 함. (#6092)
* 윈도우 10 로그인 화면 지원 향상(알림 자동 출력 및 터치를 통해 암호 편집창 접근 가능). (#6010)
* ALVA BC640/680 디스플레이의 보조 라우팅 버튼이 제대로 인식되도록 함. (#5206)
* 최신 윈도우 10 빌드 사용 시 토스트 알림 내용이 출력되지 않던 문제 수정. (#6096)
* Baum/HumanWare Brailliant B 사용 시 가끔 디스플레이 핫키가 인식되지 않던 문제 수정. (#6035)
* 문서 서식 내 줄 수 알림이 활성화된 경우 줄 수가 점자 디스플레이에 출력되도록 함. (#5941)
* 음성 출력 모드가 꺼짐으로 되어있어도 객체 정보 출력 내용(예: NvDA+tab을 눌러 포커스 확인)이 음성 뷰어에 나타나도록 함. (#6049)
* 아웃룩 2016 메시지 목록에서 "연결된 임시 보관함" 정보가 출력되지 않도록 함. (#6219)
* Google Chrome 및 Chrome 기반 브라우저 사용 시 인터페이스 언어가 영어 외 다른 언어로 설정되어 있을 때 브라우즈 모드가 작동하지 않던 문제 수정. (#6249)

### 개발 변경사항(영문)

* Logging information directly from a property no longer results in the property  being called recursively over and over again. (#6122)

## 2016.2.1

이번 버전에서는 Microsoft Word 사용 시 발생하던 여러 문제를 수정하였습니다:

* 윈도우 XP에서 Microsoft Word 실행 시 다운되던 문제 수정. (#6033)
* Microsoft ㅜ어드 사용 시 발생하던 여러 문제의 원인이었던 맞춤법 오류 알림 기능 제거. (#5954, #5877)

## 2016.2

이번 버전의 주 기능들: 입력 시 철자 오류 알림; Microsoft Word 내 문법 오류 인식; Microsoft Office 지원 향상 및 버그 수정 등입니다.

### 새로운 기능

* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 다음 및 이전 주석(a/shift+a) 명령을 사용하여 삽입 또는 삭제된 텍스트로 이동할 수 있음. (#5691)
* Microsoft Excel 사용 시 셀 그룹 레벨 및 그룹 확장 또는 축소 여부가 출력되도록 함. (#5690)
* 텍스트 서식 알림 핫키를 두번 누를 시 서식 정보가 브라우즈 모드로 출력되도록 함. (#4908)
* Microsoft Excel 2010 이상 사용 시 셀 음영 및 채우기 그라데이션이 출력되도록 함(본 기능은 문서 서식 대화상자내 색상 알림 설정을 통해 조절할 수 있음). (#3683)
* 점자 표기법: 코 이네 그리스어 추가. (#5393)
* 로그 뷰어 사용 중 control+s를 눌러 로그를 저장할 수 있음. (#4532)
* 포커스된 컨트롤이 철자 오류 인식을 지원하고 NVDA내 철자 오류 알림이 선택된 경우 텍스트 입력 시 철자 오류 경고음이 출력되도록 함(본 기능은 키보드 설정에 추가된 입력 중 철자 오류 경고음 재생 옵션을 통해 조절 가능). (#2024)
* Microsoft Word 사용 시 맞춤법 오류가 인식되도록 함(본 기능은 문서 서식 대화상자에 추가된 맞춤법 알림 설정을 통해 조절할 수 있음). (#5877)

### 변경사항

* 브라우즈 모드와 편집창에서 키패드 enter 키가 제 기능을 하지 못하던 문제 수정. (#5385)
* NVDA 기본 음성 엔진을 eSpeak NG로 교체함. (#5651)
* Microsoft Excel 사용 시 열 머릿말과 셀 사이에 빈 열이 있을 경우 특정 행 머릿말이 출력되지 않던 문제 수정. (#5396)
* Microsoft Excel 사용 시 셀의 위치가 셀 머릿말에 앞서 출력되도록 하여 머릿말과 콘텐츠간 혼돈을 최소화하도록 함. (#5396)

### 버그 수정내역

* 브라우즈 모드 사용 시 첫 글자 핫키로 문서가 지원하지 않는 요소로 옮기고자 할 때 "다음/이전 요소 없음" 대신 "요소 지원 안함"이라고 출력되도록 함. (#5691)
* Microsoft Excel에서 요소 목록 호출 시 차트만 있는 시트도 시트 목록에 포함되도록 함. (#5698)
* IntelliJ와 Android Studio 등 여러 개의 창을 가진 Java 응용 프로그램에서 창을 전환할 때 NVDA가 불필요한 정보를 알리지 않음. (#5732)
* Notepad ++ 등 Scintilla 기반의 텍스트 편집기에서 점자 디스플레이를 사용하는 경우 커서 이동 시 점자 출력이 제대로 업데이트되도록 함. (#5678)
* 점자 출력을 활성화 할 때 NVDA가 충돌할 수 있는 문제점 수정. (#4457)
* Microsoft Word에서 문단 들여쓰기는 항상 사용자가 지정한 길이의 단위 (센티미터와 인치 등)로 알려지도록 함. (#5804)
* 음성으로 만 출력되던 많은 NVDA 메시지가 점자 디스플레이로 출력되도록 함. (#5557)
* 접근 가능한 Java 응용 프로그램에서 트리 뷰의 항목 수준이 알려지도록 함. (#5766)
* 모질라 FireFox 사용 도중 가끔 Adobe Flash가 다운되던 문제 수정. (#5367)
* 구글 Chrome 및 Chrome 기반 브라우저에서 대화상자나 응용 프로그램에 포함된 문서를 브라우즈 모드에서 읽을 수 있음. (#5818)
* 구글 Chrome 및 Chrome 기반 브라우저에서 웹의 대화상자나 응용 프로그램에서 NVDA를 강제로 브라우즈 모드로 전환할 수 있음. (#5818)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 aria-activedescendant가 사용된 컨트롤(예: Gmail 내 이메일 작성 중 받는이 주소 입력 시 나타나는 검색 결과 목록)에서 브라우즈 모드로 전환되지 않도록 함. (#5676)
* Microsoft Word에서 표 행/렬의 머리말 알림이 활성화된 경우 큰 표에서 NVDA가 정지되던 문제 수정. (#5878)
* Microsoft Word 사용 시 개요 수준 텍스트(개요 텍스트가 헤딩이 아닐 경우)를 헤딩으로 인식하던 문제 수정. (#5186)
* Microsoft Word 내 브라우즈 모드 사용 시 컨테이너 요소 시작 및 끝 명령(comma/shift+comma)을 사용하여 표 시작 및 끝으로 이동할 수 있음. (#5883)

### 개발 변경사항(영문)

* NVDA's C++ components are now built with Microsoft Visual Studio 2015. (#5592)
* You can now present a text or HTML message to the user in browse mode using ui.browseableMessage. (#4908)
* In the User Guide, when a <!-- KC:setting command is used for a setting which has a common key for all layouts, the key may now be placed after a full-width colon (：) as well as the regular colon (:). (#5739) -->

## 2016.1

이번 버전의 주 기능들: 배경음 볼륨 조절; 점자 디스플레이 지원 향상; Microsoft Office 지원 향상; iTunes 브라우즈 모드 관련 여러 문제 수정 등입니다.

### 새로운 기능

* 점자 표기법: 폴란드어 8점 컴퓨터 점자, 몽골리아어 추가. (#5537, #5574)
* 점자 설정에 점자 커서 출력과 커서 모양 설정 추가. (#5198)
* HIMS 스마트 비틀 지원 추가 (블루투스로 연결 가능) (#5607)
* NVDA가 윈도우 8 이상 시스템에 설치되었을때 배경음 볼륨을 줄일 수 있는 옵션 추가(음성 엔진 대화상자내 오디오 도킹 모드 설정 또는 NVDA+shift+d를 눌러 설정값을 변경할 수 있음). (#3830, #5575)
* APH Refreshabraille HID 모드 및 Baum Pronto! 및 VarioUltra USB 연결 지원 추가. (#5609)
* 휴먼웨어 Brailliant BI/B OpenBraille protocol 지원 추가. (#5612)

### 변경사항

* 강조된 텍스트 알림이 비활성화됨. (#4920)
* Microsoft Excel내 요소 목록 대화상자내 공식(formula) 라디오 버튼 핫키를 Alt+R로 변경하여 검색 핫키와 혼돈되지 않도록 함. (#5527)
* Liblouis 점자 변환기 2.6.5 버전 사용. (#5574)
* 포커스나 탐색 객체를 텍스트 객체로 옮길시 "텍스트"(객체 형식)가 출력되지 않도록 함. (#5452)

### 버그 수정내역

* iTunes 12에서 iTunes Store 탐색 중 새 페이지가 열린 후 브라우즈 모드가 업데이트되지 않던 문제 수정. (#5191)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 첫 글자 명령을 사용하여 특정 레벨 헤딩으로 옮길시 접근 향상 목적으로 코딩된 헤딩(예: h tag의 레벨이 aria-level로 코딩된 경우)도 탐색이 가능하도록 함. (#5434)
* Spotify 사용 시 알 수 없는 객체가 포커스되는 문제 수정. (#5439)
* 다른 프로그램에서 Spotify로 옮길시 포커스가 제대로 옮겨지지 않던 문제 수정. (#5439)
* 브라우즈 모드와 포커스 모드 토글시 점자로 토글 설정이 출력되도록 함. (#5239)
* 특정 윈도우 버전에서 시작 버튼이 목록 또는 선택된것처럼 출력되던 문제 수정. (#5178)
* Microsoft 아웃룩에서 이메일 작성시 "삽입됨"과 같은 불필요한 메시지가 출력되던 문제 수정. (#5486)
* 점자 디스플레이 사용 시 같은 줄에 텍스트가 선택될때(예: 편집창에서 같은 줄이지만 다른 위치의 텍스트가 선택될때) 커서가 새 위치로 옮겨지지 않던 문제 수정. (#5410)
* 윈도우 10에서 Alt+F4를 눌러 명령 Prompt 종료시 NVDA가 종료되던 문제 수정. (#5343)
* 브라우즈 모드 사용 시 요소 목록 대화상자에서 요소 변경시 검색창 내용이 삭제되도록 함. (#5511)
* 모질라 기반 프로그램 사용 시 마우스를 편집창으로 옮길때 마우스 설정에서 설정된 텍스트 단위(단어, 줄 등)만 출력되도록 함(이전에는 컨텐츠 전체가 출력되었음). (#5535)
* 모질라 기반 프로그램에서 편집창 내에서 마우스를 옮길시 마우스가 위치한 텍스트 요소(링크 등) 이후 내용이 출력되지 않던 문제 수정. (#2160, #5535)
* 인터넷 익스플로러에서 shoprite.com 웹사이트 접속시 브라우즈 모드가 작동하지 않던 문제 수정(잘못 코딩된 lang 속성 때문에 페이지가 공백으로 처리됨). (#5569)
* Microsoft Word 사용 시 track 마커가 존재하지 않는 경우 "삽입됨"과 같은 track 정보가 출력되지 않도록 함. (#5566)
* 시스템 포커스를 토글 버튼으로 옮길때 토글 활성화 상태가 출력되도록 함. (#5441)
* 변경된 마우스 모양이 출력되지 않던 문제 수정. (#5595)
* 줄 들여쓰기 출력시 비 불리 공백(non-breaking space)가 스페이스로 처리되도록 함(예: non-breaking space 셋이 존재할 경우 "스페이스" 3회 출력 대신 "3 스페이스"가 출력되도록 함). (#5610)
* Modern 입력 구성 후보 목록을 닫을때 입력 구성 편집창이나 문서로 빠져나가지 않던 문제 수정. (#4145)
* Microsoft Office 2013 이상 사용 시 ribbon 탭만 표시된 경우 탭 선택 시 ribbon 아이템이 출력되지 않던 문제 수정. (#5504)
* 터치스크린 명령 실행 및 할당 관련 여러 문제 수정 및 기능 향상. (#5652)
* 입력 도움말 사용 시 터치스크린 hover 동작이 출력되지 않도록 함. (#5652)
* Microsoft Excel내 merged 셀내 주석이 있는 경우 주석 목록이 요소 목록에 뜨지 않던 문제 수정. (#5704)
* 표 행과 열 머릿말 알림 설정이 켜져 있을때 특정 상황에서 Microsoft Excel내 sheet 내용이 출력되지 않던 문제 수정. (#5705)
* 구글 Chrome 사용 시 동아시아 입력 구성창 사용 시 오류가 발생하던 문제 수정. (#4080)
* iTunes내 Apple Music 검색시 검색 결과 문서내 브라우즈 모드가 업데이트되지 않던 문제 수정. (#5659)
* Microsoft Excel에서 shift+f11을 눌러 새 sheet 생성시 새 위치가 출력되도록 함(이전에는 아무런 내용도 출력되지 않았음). (#5689)
* 한글 입력 시 점자가 제대로 출력되지 않던 문제 수정. (#5640)

### 개발 변경사항(영문)

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

이번 버전의 주 기능들: 윈도우 10 지원 향상; 윈도우 8 이상 접근성 센터내 NVDA 추가; 엑셀 지원 향상(sheet 목록 및 이름 변경과 잠겨진 셀로 이동 가능); 모질라 FireFox, 구글 Chrome 및 모질라 썬더버드에서의 rich text 편집 지원 향상 등입니다.

### 새로운 기능

* 윈도우 8이상 사용 시 NVDA가 접근성 센터에 표시되도록 함. (#308)
* Microsoft Excel에서 셀을 옮길때 문서 서식 설정에서 활성화된 서식 정보가 출력되도록 함. (#4878)
* 문서 서식 설정에 "강조 텍스트 알림" 설정(기본적으로 선택되어 있음)을 추가하여 문서내 강조된 텍스트를 자동으로 출력하도록 함(현재 - 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 em 또는 strong 텍스트에서만 적용됨). (#4920)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 문서 변경 추적 알림이 활성화된 경우 삽입 또는 삭제된 텍스트가 알려지도록 함. (#4920)
* Microsoft Word내 요소 목록에 track 변경 나열시 더 많은 정보(예: 서식 변경)가 포함되도록 함. (#4920)
* Microsoft Excel내 요소 목록(NVDA+f7)를 통해 sheet 목록을 보거나 이름 변경을 할 수 있음. (#4630, #4414)
* 기호 발음 설정을 통해 음성 엔진이 기호를 처리할지(예: 띄어 읽기 또는 억양 조절 등)를 조절할 수 있음. (#5234)
* Microsoft Excel 사용 시 sheet 저자가 셀에 입력 메시지를 첨부한 경우 메시지 내용이 출력되도록 함. (#5051)
* Baum Pronto! V4 및 VarioUltra 지원 추가(블루투스로 연결 가능). (#3717)
* 모질라 기반 프로그램에서의 rich text 편집 지원 향상(예: 점자 디스플레이 연결 후 FireFox에서 Google Docs 문서 편집 또는 썬더버드내 HTML 이메일 작성중). (#1668)
* 구글 Chrome 또는 Chrome 기반 브라우저에서의 rich text 편집 지원 향상(예: 점자 디스플레이 연결 후 Google Docs 문서 편집). (#2634)
 * Chrome 47 이상 사용 바람.
* Microsoft Excel에서 브라우즈 모드 사용 시 방향키를 사용하여 보호된 sheet안에 있는 잠겨진 셀로 이동 가능. (#4952)

### 변경사항

* 문서 서식 대화상자내 문서 변경 추적 내용 설정이 기본적으로 선택되도록 변경됨. (#4920)
* 문서 변경 추적 내용 알림이 선택된 상태에서 Microsoft Word에서 글자 단위로 옮길시 효율성을 높이기 위해 track 변경 내용이 덜 출력되도록 함(자세한 track 변경 정보는 요소 목록에서 확인할 수 있음). (#4920)
* Liblouis 점자 변환기 2.6.4 버전 사용. (#5341)
* 기호 발음 설정을 기호(some)로 설정시 더 많은 기호(예: 기본 수학 기호)가 출력되도록 함. (#3799)
* 만약 음성 엔진이 지원할 경우 괄호 및 en dash(–)를 출력시 음성 엔진이 띄어 읽도록 함. (#3799)
* 텍스트 선택 시 선택된 텍스트가 먼저 출력되도록 함. (#1707)

### 버그 수정내역

* 아웃룩 2010/2013 메시지 목록 탐색 속도 향상됨. (#5268)
* Microsoft Excel 차트를 읽다가 특정 키(예: control+pageUp/control+pageDown을 사용하여 sheet 변경)를 누를시 키가 제대로 동작하지 않던 문제 수정. (#5336)
* NVDA 이전 버전 설치 경고 대화상자내 버튼들이 화면에 제대로 나타나지 않던 문제 수정. (#5325)
* 윈도우 8 이상 사용 시 로그인후 NVDA가 실행되도록 설정했을때 NVDA가 일찍 실행되도록 함. (#308)
 * 만약 이전 버전에서 본 설정을 설정했다면 일반 설정에서 본 설정을 해제 후 다시 설정하기 바람. 설정 방법은 다음과 같습니다:
  1. 일반 설정을 호출합니다.
  1. 윈도우 로그인 후 NvDA 자동 시작 설정을 해제합니다.
  1. 확인 버튼을 선택합니다.
  1. 일반 설정을 다시 호출합니다.
  1. 윈도우 로그인 후 NvDA 자동 시작 설정을 선택합니다.
  1. 확인 버튼을 선택합니다.
* UI Automation 지원 속도 향상됨(예: 파일 탐색기, 작업 전환). (#5293)
* 모질라 FireFox와 같은 Gecko 기반 컨트롤에서 읽기 전용 ARIA grid를 만났을때 포커스 모드로 전환되도록 함. (#5118)
* 터치스크린 사용 시 한 손가락으로 왼쪽으로 쓸어내릴때 이전 객체가 없을 경우 "이전 객체 없음"이라고 출력되도록 함.
* 단춧키 설정내 명령 검색창에 여러 단어를 입력 시 오류가 발생하던 문제 수정. (#5426)
* 휴먼웨어 Brailliant BI/B 디스플레이를 USB로 재연결시 특정 상황에서 NVDA가 다운되던 문제 수정. (#5406)
* 특정 인도 언어(특히 합성어가 있는 언어) 사용 시 대문자 영어 글자가 제대로 풀이되어 출력되지 않던 문제 수정. (#5375)
* 윈도우 10 사용 시 시작 메뉴를 열때 NVDA가 다운되던 문제 수정. (#5417)
* Desktop용 스카이프에서 이전 알림이 닫히기 전 새 알림이 뜰때 알림 내용이 출력되지 않던 문제 수정. (#4841)
* Desktop용 스카이프 7.12 이상에서 스카이프 알림이 제대로 출력되도록 함. (#5405)
* 특정 프로그램(예: Jart) 사용중 팝업 메뉴를 닫은 후 포커스된 내용이 제대로 알려지지 않던 문제 수정. (#5302)
* 윈도우 7 이상에서 특정 프로그램(예: Wordpad) 사용 시 색상이 출력되지 않던 문제 수정. (#5352)
* Microsoft PowerPoint에서 문서 편집시 엔터를 눌렀을때 bullet  또는 숫자가 출력되지 않던 문제 수정. (#5360)

## 2015.3

이번 버전의 주 기능들: 윈도우 10 기본 지원; 브라우즈 모드내에서 첫 글자 명령 임시 중지; 인터넷 엑스플로러 지원 향상; 점자 사용 시 발생하던 입력 관련 문제 해결 등입니다.

### 새로운 기능

* 인터넷 익스플로러와 같은 MSHTML 기반 편집창에 있는 철자 오류가 출력되도록 함. (#4174)
* 더 많은 Unicode 수학 기호가 음성으로 출력되도록 함. (#3805)
* 윈도우 10 시작 검색창내 검색 결과가 자동으로 출력되도록 함. (#5049)
* EcoBraille 20, EcoBraille 40, EcoBraille 80 및 EcoBraille Plus 디스플레이 지원 추가. (#4078)
* 브라우즈 모드 사용 시 NVDA+shift+space를 사용하여 첫 글자 명령을 해제할 수 있음(Gmail, Twitter, Facebook과 같은 웹 앱 사용 시 첫 글자를 앱에서 처리할 수 있음). (#3203)
* 점자 표기법: 핀란드어 6점 1종, 아일랜드어 1종과 2종, 2006년 수정본 한국어 정자와 약자 추가. (#5137, #5074, #5097)
* Papenmeier BRAILLEX Live Plus 디스플레이에 장착된 QWERTY 키보드 지원 추가. (#5181)
* 윈도우 10의 Edge 브라우저 및 Edge 기반 컨트롤 지원(기초단계임). (#5212)
* 새 NVDA 언어: 칸나다어 추가.

### 변경사항

* Liblouis 점자 변환기 2.6.3 버전 사용. (#5137)
* 이전 NVDA 버전 설치시 NVDA를 완전 제거후 설치할 것을 권장하는 대화상자가 뜨도록 함. (#5037)

### 버그 수정내역

* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 폼 필드로 이동시 목록 항목이 제외되도록 함. (#4204)
* Firefox에서 ARIA tab 페널내 전체 텍스트가 객체 설명으로 인식되지 않도록 함. (#4638)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 탭으로 섹션, 기사 또는 대화상자로 이동시 컨테이너 내용이 컨트롤 이름으로 인식되지 않도록 함. (#5021, #5025) 
* Baum/HumanWare/APH 디스플레이를 통해 점자 입력 시 다른 디스플레이 키에 의해 점자 입력이 중단되던 문제 수정. (#3541)
* 윈도우 10에서 alt+tab 또는 alt+shift+tab을 사용하여 앱 전환시 불필요한 정보가 출력되던 문제 수정. (#5116)
* 점자 디스플레이 사용 시 특정 프로그램(예: 아웃룩)내에서 글자 입력 시 입력된 텍스트가 깨졌던 문제 수정. (#2953)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 특정 요소가 나타나거나 변경된 후 곧바로 포커스될때 올바른 컨텐츠가 출력되도록 함. (#5040)
* Microsoft Word에서 브라우즈 모드 사용중 첫 글자로 이동시 점자와 리뷰 커서 위치가 업데이트되지 않던 문제 수정. (#4968)
* 점자로 컨트롤이나 서식 정보 출력시 정보 사이 또는 뒤에 불필요한 스페이스가 삽입되지 않도록 함. (#5043)
* 사용중인 프로그램의 응답성이 떨어진 후 다른 프로그램으로 전환시 대부분의 프로그램에서 NVDA의 응답성이 빨라짐. (#3831)
* 윈도우 10 토스트 알림 내용이 출력되지 않던 문제 수정. (#5136)
* 특정(UI Automation 기반) 콤보박스내 옵션 변경시 선택된 옵션이 제대로 출력되지 않던 문제 수정.
* 웹 브라우저에서 브라우즈 모드 사용 시 프레임 문서로 탭한 후 탭 명령이 제대로 작동하지 않던 문제 수정. (#5227)
* 터치스크린 사용 시 윈도우 10 잠금 화면을 닫을 수 없던 문제 수정. (#5220)
* 윈도우 7 이상에서 점자 디스플레이 사용 시 특정 프로그램(예: Wordpad와 Skype) 사용 시 점자로 글자 입력 시 입력된 텍스트가 깨졌던 문제 수정. (#4291)
* 윈도우 10 잠금 화면에서 클립보드 내용 읽기, 리뷰 커서를 통한 다름 프로그램 접근, 설정 저장 등 여러 기능이 실행되지 못하도록 함. (#5269)

### 개발 변경사항(영문)

* You can now inject raw input from a system keyboard that is not handled natively by Windows (e.g. a QWERTY keyboard on a braille display) using the new keyboardHandler.injectRawKeyboardInput function. (#4576)
* eventHandler.requestEvents has been added to request particular events that are blocked by default; e.g. show events from a specific control or certain events even when in the background. (#3831)
* Rather than a single i18nName attribute, synthDriverHandler.SynthSetting now has separate displayNameWithAccelerator and displayName attributes to avoid reporting of the accelerator in the synth settings ring in some languages.
 * For backwards compatibility, in the constructor, displayName is optional and will be derived from displayNameWithAccelerator if not provided. However, if you intend to have an accelerator for a setting, both should be provided.
 * The i18nName attribute is deprecated and may be removed in a future release.

## 2015.2

이번 버전의 주 기능들: Microsoft Excel에 삽입된 차트 읽기 및 수학 컨텐츠 탐색 기능 추가 등입니다.

### 새로운 기능

* Microsoft Word와 아웃룩 사용 시 alt+아래 방향키와 alt+위 방향키를 사용하여 다음 및 이전 문장으로 이동 가능. (#3288)
* 여러 인도 언어 점자 표기법 추가. (#4778)
* Microsoft Excel에서 여러 셀에 걸쳐있는 정보가 인식되도록 함. (#3040)
* Microsoft Excel 사용 시 요소 목록(NVDA+F7)을 사용하여 차트와 공식 또는 주석이 있는 셀 목록을 ㅗ학인할 수 있음. (#1987)
* Microsoft Excel 차트 지원 추가(NvDA+F7을 눌러 요소 목록을 호출하고 타츠를 선택한 후 방향키를 이용하여 데이타 확인 가능). (#1987)
* Design Science MathPlayer 4를 이용하여 웹브라우저, Microsoft Word 및 파워포인트 문서에 삽입된 수학 컨텐츠를 읽거나 집중 탐색할 수 있음(NVDA 사용설명서에 있는 수학 컨텐츠 섹션 참고 바람). (#4673)
* 단춧키 설정을 통해 모든 NvDA 설정 대화상자 및 문서 서식 설정 관련 명령(키보드, 터치 명령 등)을 할당할 수 있음. (#4898)

### 변경사항

* 문서 서식 설정에 있는 글꼴명, 줄, 링크 및 목록 설정 핫키가 변경됨. (#4650)
* 마우스 설정에 있는 마우스 좌표 비프음 출력과 밝기에 대한 비프음 볼륨 설정에 핫키가 추가됨. (#4916)
* 이전보다 더 많은 색상을 인식 및 출력하도록 함. (#4984)
* Liblouis 점자 변환기 2.6.2 버전 사용. (#4777)

### 버그 수정내역

* 특정 인도 언어 사용중 합성어로 된 글자가 제대로 풀이되어 출력되지 않던 문제 수정. (#4582)
* 보이스 설정에 있는 "음성 데이타 사용" 옵션을 선택 시 기호 발음 설정에 나열된 기호를 현재 사용중인 언어로 출력하도록 함. 또한 사용중인 언어가 본 대화상자의 제목표시줄에 표시되도록 함. (#4930)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 편집 콤보 박스(예: 구글 검색창)에 입력된 글자가 출력되던 문제 수정. (#4976)
* Microsoft Office 사용중 색상을 선택 시 선택된 색상이 출력되지 않던 문제 수정. (#3045)
* 댄마크어 점자 출력 기능 복원. (#4986)
* 파워포인트 슬라이드쇼중 page up과 page down을 사용하여 슬라이드로 이동하지 못하던 문제 수정. (#4850)
* Desktop용 Skype 7.2 이후 버전 사용 시 타이핑 알림 출력 및 대화 내용에서 벗어난 후의 포커스 문제 해결. (#4972)
* 단축키 설정에 있는 검색 필드에서 특정 구두점(예: 대괄호) 입력이 처리되지 않던 문제 수정. (#5060)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 g 또는 shift+g를 통해 그래픽을 탐색 시 접근 향상 목적으로 이미지로 처리된 요소도 포함하도록 함(예: ARIA role img). (#5062)

### 개발 변경사항(영문)

* brailleInput.handler.sendChars(mychar) will no longer filter out a character if it is equal to the previous character by ensuring that the key sent is correctly released. (#4139)
* Scripts for changing touch modes will now honor new labeles added to touchHandler.touchModeLabels. (#4699)
* Add-ons can provide their own math presentation implementations. See the mathPres package for details. (#4509)
* Speech commands have been implemented to insert a break between words and to change the pitch, volume and rate. See BreakCommand, PitchCommand, VolumeCommand and RateCommand in the speech module. (#4674)
 * There is also speech.PhonemeCommand to insert specific pronunciation, but the current implementations only support a very limited number of phonemes.

## 2015.1

이번 버전의 주 기능들: Microsoft Word와 아웃룩 문서 및 메시지에서의 브라우즈 모드 기능, Skype 지원 향상 및 인터넷 익스플로러 사용 시 발생하던 여러 중대 버그 수정 등입니다.

### 새로운 기능

* 구두점/기호 발음 설정에 새 기호를 추가할 수 있음. (#4354)
* 단축키 설정에 있는 검색 필드를 사용하여 원하는(검색 문자열이 들어간) 명령을 확인할 수 있음. (#4458)
* mintty 사용 시 새 컨텐츠가 출력되도록 함. (#4588)
* 브라우즈 모드 검색(찾기) 대화상자에 대소문자 구분 검색 옵션 추가. (#4584)
* Microsoft ㅜ어드 사용중 NvDA+SPACE를 눌러 브라우즈 모드로 전환후 첫 글자 명령(예: 헤딩 (H)) 및 요소 목록 (NVDA+F7) 호출 등을 사용할 수 있음. (#2975)
* Microsoft 아웃룩 2007 이상에서 브라우즈 모드를 사용하여 HTML 이메일을 읽을 수 있음(만약 브라우즈 모드가 자동으로 적용되지 않았을 경우 NVDA+SPACE를 눌러 수동으로 브라우즈 모드를 선택바람). (#2975) 
* Microsoft Word 문서 저자가 표 속성 중 열 머릿말 행을 표시한 경우 표의 열 머릿말이 자동으로 출력되도록 함. (#4510) 
 * 그러나 표 행이 중복되는 경우 적용되지 않을 수 있음(이때 NVDA+shift+c를 눌러 열 머릿말을 설정하기 바람).
* Desktop용 스카이프에서 뜨는 알림을 자동으로 출력하도록 함. (#4741)
* Desktop용 스카이프 사용 시 NVDA+control+1부터 NVDA+control+0을 눌러 최근 메시지 리뷰시 메시지를 출력하도록 함(예: NVDA+control+1을 눌러 최근 메시지를 NVDA+control+0을 눌러 최근 열번째 메시지 확인). (#3210)
* Desktop용 스카이프로 메시지를 주고받을때 친구가 타이핑을 하는지를 출력함. (#3506)
* NVDA 실행 명령 목록에 --install-silent 옵션을 통해 NvDA 설치 후 자동으로 실행하는것을 차단할 수 있음. (#4206)
* 페이펀마이어 BRAILLEX Live 20, BRAILLEX Live 및 BRAILLEX Live Plus 디스플레이 지원 추가. (#4614)

### 변경사항

* 문서 서식 알림 설정에 있는 철자 오류 알림 옵션에 핫키(Alt+R) 추가. (#793)
* 자동 언어 변경 설정에 관계없이 현재 사용되는 음성 엔진 언어로 기호 및 구두점을 출력하도록 함(보이스 설정에 추가된 보이스 언어 데이타 사용 설정을 해제하여 NVDA 인터페이스 언어를 사용하도록 할 수 있음). (#4210)
* Newfon 음성 엔진을 추가 기능으로 전환함. (#3184)
* 스카이프 사용 시 스카이프 7 이상 사용 바람. (#4218)
* NVDA 업데이트 다운로드 보안 강화(HTTPS 연결 및 다운로드후 파일 hash 검사 추가). (#4716)
* 이스피크 음성 엔진 1.48.04 사용. (#4325)

### 버그 수정내역

* Microsoft Excel에서 통합된 머릿말 셀(예: A1과 B1이 통합되었을때)의 머릿말이 출력되도록 함(이전엔 아무것도 출력되지 않았음). (#4617)
* 파워포인트 2003에서 편집창의 내용을 편집시 줄 단위 이동이 불편했던 문제 수정(이전에는 다음 및 이전 문단으로 이동시 줄의 오른쪽으로 커서가 이동했었음). (#4619)
* NVDA의 모든 대화상자를 중앙에 고정시켜 시각적 프레즌테이션 및 편의성을 높임. (#3148)
* Desktop용 스카이프에서 친구 추가 메시지 편집시 메시지 읽기 및 편집 기능이 제대로 작동하지 않던 문제 수정. (#3661)
* Eclipse IDE내 체크박스에서 트리뷰 항목으로 옮길때 체크박스가 출력되던 문제 수정. (#4586)
* Microsoft Word의 철자 및 문법 오류 대화상자에서 현재 오류를 변경 또는 무시 후 다음 오류가 알리지 않던 문제 수정. (#1938)
* Tera Term Pro 터미널창 및 Balabolka 문서내 텍스트를 읽을 수 없었던 문제 수정. (#4229)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 프레임 내에 있는 입력창에 한국어 및 다른 동아시아 글자 입력 후 프레임으로 포커스가 되지않던 문제 수정. (#4045)
* 단춧키 설정을 통해 단춧키 추가중 키보드 배열 선택 메뉴에서 ESC를 눌렀을때 메뉴 대신 단춧키 설정 대화상자가 닫히던 문제 수정. (#3617)
* 추가 기능 제거후 추가 기능 폴더가 삭제되도록 함(이전에는 NVDA를 한번 더 재시작한 후 추가 기능 폴더가 삭제되었음). (#3461)
* 스카이프 7 사용 시 존재하던 중대 버그들 수정. (#4218)
* 스카이프에서 메시지 전송시 메시지가 두번 출력되던 문제 수정. (#3616)
* 스카이프 사용중 가끔 메시지 내용(일부분 또는 전체)이 갑자기 출력되던 문제 수정. (#4644)
* 시간 및 날짜 출력시 사용자가 지정한 국가 설정을 반영하지 않던 문제 수정. (#2987) 
* 브라우즈 모드에서 그래픽 텍스트 출력시 여러줄에 걸쳐있는 불필요한 텍스트(특히 Base64로 처리된 그래픽(예: 구글 그룹))가 출력되지 않도록 함. (#4793)
* 일시 중단된 메트로 앱을 빠져나갈때 NVDA가 몇초동안 다운되던 문제 수정. (#4572)
* 모질라 FireFox에서 실시간 구역내 위치한 atomic 요소 변경시 aria-atomic 속성이 반영되도록 함(이전에는 본 요소내 하위 요소에만 적용되었음). (#4794)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤안에 위치한 ARIA 앱에서 브라우즈 모드 사용 시 실시간 정보 업데이트 출력 및 브라우즈 모드에 반영되도록 함. (#4798)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에 위치한 실시간 구역의 텍스트가 병경되었을때 저자가 업데이트 정보가 필요하다고 표시한 텍스트만 출력되도록 함. (#4800)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 필요한 경우 aria-labelledby로 처리된 컨텐츠가 이전에 있던 컨텐츠를 대신하여 출력되도록 함. (#4575)
* Microsoft 아웃룩 2013에서 철자 오류 검사시 철자 오류가 있는 단어가 출력되지 않던 문제 수정. (#4848)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 visibility:hidden로 처리된 요소내 컨텐츠가 브라우즈 모드에 나타나지 않도록 함. (#4839, #3776)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 폼 컨트롤의 title 속성이 다른 레이블 표시를 대신해 출력되지 않도록 함. (#4491)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 aria-activedescendant 속성 때문에 본 컨트롤에 포커스가 가지않던 문제 수정. (#4667)

### 개발 변경사항(영문)

* Updated wxPython to 3.0.2.0. (#3763)
* Updated Python to 2.7.9. (#4715)
* NVDA no longer crashes when restarting after removing or updating an add-on which imports speechDictHandler in its installTasks module. (#4496)

## 2014.4

### 새로운 기능

* 새 NVDA 언어: 콜롬비아 스페인어, 펀자브어 추가.
* NVDA 종료 대화상자에 NVDA 재시작 및 추가 기능 미사용 옵션 추가. (#4057)
 * NVDA 실행 시 --disable-addons 실행 명령을 통해 추가 기능을 일시적으로 정지시킬 수 있음.
* 발음 사전에 단어 입력 시 페턴(이전값)을 단어 단위(즉 단어의 일부분이 아님)로 처리하도록 지정 가능. (#1704)

### 변경사항

* 객체 탐색을 사용하여 브라우즈 모드 문서외 객체에서 문서내 객체로 옮길시 문서 탐색 모드가 자동으로 활성되도록 함 (이전에는 포커스 변경시에만  적용되었음). (#4369)
* 점자 디스플레이 및 음성 엔진 목록이 가나다순(음성 끝/점자 출력 끔은 마지막에 표시)으로 정렬하여 각 설정 대화상제에 나타나도록 함. (#2724)
* Liblouis 점자 변환기 2.6.0 버전 사용. (#4434, #3835)
* 브라우즈 모드 사용 시 E/Shift+E(편집창 이동)를 누를때 편집 콤보 박스로도 이동하도록 함(예: 최신 구글 검색 페이지). (#4436)
* 알림 영역에 있는 NVDA 아이콘을 왼쪽 마우스 버튼으로 클릭시 NVDA 메뉴가 호출되도록 함. (#4459)

### 버그 수정내역

* 포커스를 브라우즈 모드 문서로 옮길시(예: Alt+Tab을 눌러 열려있는 사이트로 옮길때) 리뷰 커서가 포커스된 요소가 아닌(예: 커서 근처의 링크) 가상 캐럿 위치에 위치하도록 함. (#4369)
* 파워포인트 슬라이드쇼중 리뷰 커서가 가상 캐럿을 제대로 따라가도록 함. (#4370)
* 모질라 FireFox와 같은 Gecko 기반 프로그램에서 실시간 구역(live region)을 제공하는 객체의 상위 객체의 ARIA 구역 정보가 다르더라도(예: "polite" 컨텐츠 구역에 "assertive" 컨텐츠가 출력될 경우) 새 내용이 출력되도록 함. (#4169).
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 특정 문서내 문서(예: frameset내 frameset)의 내용을 제대로 접근할 수 없었던 문제 수정. (#4418)
* HandyTech 디스플레이 사용 시 NVDA가 특정 상황에서 다운되던 문제 수정. (#3709)
* 특정 윈도우 비스타 시스템에서 NVDA 실행 시(예: 바탄 화면 아이콘 클릭 또는 동작키 사용) "Entry Point Not Found" 대화상자가 떴던 문제 수정. (#4235)
* 최신 Eclipse 버전에서 대화상자내 편집창에서 일어났던 중대한 문제들 해결. (#3872)
* Outlook 2010에서 일정 및 회의 요청 장소 필드에서 캐럿이 제대로 움직이지 않던 문제 수정. (#4126)
* 라이브 구역내 라이브 구역이 아닌 지역(예: aria-live="off")을 무시하도록 함. (#4405)
* 상태표시줄 내용을 알릴시 상태표시줄 이름이 있는 경우 표시줄 이름과 내용의 첫 글자간 공백을 두어 표시하도록 함. (#4430)
* 입력된 단어를 읽도록 설정한후 암호 편집창에서 새 단어 입력전 별표가 여러번 출력되던 문제 수정. (#4402)
* Outlook 메시지 목록에 있는 항목이 데이타 항목으로 잘못 출력되지 않도록 함. (#4439)
* Eclipse IDE 코드 편집창에서 텍스트를 선택 시 선택된 내용 전부가 출력되던 문제 수정. (#2314)
* Eclipse의 파생본(예: Spring Tool Suite와 앤드로이드 개발 도구)가 Eclipse로 취급되도록 함. (#4360, #4454)
* 고급 DPI와 줌 변경시 인터넷 익스플로러와 같은 MSHTML 컨트롤(예: 윈도우 8 앱들)에서 마우스나 터치 탐색 기능이 제대로 동작하도록 함. (#3494) 
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 마우스나 터치 탐색 사용 시 버튼명이 출력되지 않던 문제 수정. (#4173)
* Papenmeier/BrxCom 사용 시 디스플레이의 키가 동작하지 않던 문제 수정. (#4614)

### 개발 변경사항(영문)

* For executables which host many different apps (e.g. javaw.exe), code can now be provided to load specific app modules for each app instead of loading the same app module for all hosted apps. (#4360)
 * See the code documentation for appModuleHandler.AppModule for details.
 * Support for javaw.exe is implemented.

## 2014.3

### 새로운 기능

* 일반 설정에 NVDA 시작 및 종료음 재생 여부를 설정하는 옵션 추가. (#834)
* 추가 기능이 도움말 기능을 지원하는 경우 추가 기능 관리자를 통하여 특정 추가 기능의 도움말을 열 수 있음. (#2694)
* 아웃룩 달력 지원(아웃룩 2007 이상) (#2943):
 * 방향키를 사용하여 시간대 확인 가능
 * 선택된 시간에 대한 일정 유무 확인 가능
 * 탭을 사용하여 일정 확인 가능
 * 다른 날로 옮길시 선택된 시간대나 일정이 다른 요일에 속할때에만 알리도록 함.
* 아웃룩 2010 이상에서의 inbox 및 메시지 목록 지원 향상 (#3834):
 * 문서 서식 알림에서 표 머릿말 설정을 해제하여 메시지 목록의 머릿말(보낸이, 제목 등) 출력을 정지시킬 수 있음.
 * 표 탐색 명령(Control+Alt+방향키)을 사용하여 각 열 정보를 확인할 수 있음.
* Microsoft Word에서 문서내 이미지에 alt text가 존재하지 않는 경우 문서 저자가 제공한 이미지의 제목을 출력하도록 함. (#4193)
* Microsoft Word 사용 시 서식 정보(NVDA+F) 호출시 문단 들여쓰기 값도 출력하도록 함. 또한 문서 서식 알림 설정에 있는 문단 들여쓰기 알림을 선택한 경우 이 정보를 자동으로 출력하도록 함. (#4165)
* 편집참과 문서에서 엔터를 눌렀을때 자동으로 삽입된 텍스트(예: 새 글 머리 기호 항목(bullet), 숫자, 탭 등)이 출력되도록 함. (#4185)
* Microsoft Word에서 현재 문서 위치에 주석이 존재하는 경우 NvDA+Alt+C를 눌러 주석을 확인할 수 ㅣㅇㅆ음. (#3528)
* Microsoft Excel에서의 행과 열 머릿말 알림 기능 향상 (#3568):
 * 엑셀에서 제공하는 셀 이름 범위 기능을 사용하여 머릿말 셀을 지정할 수 있음 (조스와 호환 가능)
 * 열 머릿말 설정(NVDA+Shift+C)과 행 머릿말 설정(NVDA+Shift+R)값이 문서에 저장되어 후에 문서를 불러올때 적용됨. 또한 타 스크린 리더가 셀 이름 범위 기능 지원시 이를 사용할 수 있음.
 * 위 명령들을 사용하여 한 문서에 구역에 따라 여러 머릿말 행과 열을 설정할 수 있음.
* Microsoft Word에서 행과 열 머릿말 알림 기능 추가 (#3110):
 * 워드에서 제공하는 책갈피 기능을 사용하여 머릿말 셀을 지정할 수 있음 (조스와 호환 가능)
 * 표의 첫 머릿말 셀에서 열 머릿말(NVDA+Shift+C)과 행 머릿말(NVDA+Shift+R) 지정 명령을 사용하여 행 및 열 머릿말을 지정했을때 본 값이  문서에 저장되어 후에 문서를 불러올때 적용됨. 또한 타 스크린 리더가 워드 책갈피 기능 지원시 이를 사용할 수 있음.
* Microsoft Word에서 탭을 누를때 페이지 좌측 가장자리로부터의 간격을 알리도록 함. (#1353)
* Microsoft Word 사용 시 여러 서식(굵게 쓰기, 이태릭, 밑줄, 표시, outline 레벨 등) 변환 명령이 음성과 점자로 출력되도록 함. (#1353)
* Microsoft Excel에서 현재 셀에 주석이 존재하는 경우 NvDA+Alt+C를 눌러 주석을 확인할 수 ㅣㅇㅆ음. (#2920)
* Microsoft Excel에서 Shift+F2를 눌러 주석 편��� 모드를 선택한 후 NVDA가 제공하는 주석 편집 대화상자를 통해 포커스된 셀에 주석을 삽입할 수 있음. (#2920)
* Microsoft Excel 사용 시 더 많은 셀 선택 및 이동 명령에 대한 피드백을 음성 및 점자로 확인 가능 (#4211):
 * 수직으로  페이지 이동 (pageUp/pageDown)
 * 수평으로 페이지 이동 (alt+pageUp/alt+pageDown)
 * 선택 확장 (위 키에 shift를 더함)
 * 현재 영역 선택 (control+shift+8)
* Microsoft Excel에서 서식 정보(NVDA+F) 호출시 셀의 정렬(수직 및 수평 배치)도 출력하도록 함. 또한 문서 서식 알림 설정에 있는 배치 알림을 선택한 경우 이 정보를 자동으로 출력하도록 함. (#4212)
* Microsoft Excel에서 서식 정보(NVDA+F) 호출시 셀의 스타일이 출력되도록 함. 또한 문서 서식 알림 설정에 스타일 알림을 선택한 경우 이 정보를 자동으로 출력하도록 함. (#4213)
* Microsoft PowerPoint에서 방향키를 이용하여 셰이프(shape)를 옮길시 셰이프의 위치가 출력되도록 함 (#4214):
 * 슬라이드내 셰이프의 위치(즉 가장자리로부터의 위치) 출력
 * 한 셰이프가 다른 셰이프를 덮을때 덮이 크기 및 덮어지는 셰이프 출력
 * 위치 정보 명령(NVDA+delete)을 사용하여 셰이프를 옮기지 않고도 위 정보를 확인할 수 있음.
 * 셰이프를 선택할때 다른 셰이프가 이 셰이프를 덮은 경우 덮어졌다고 출력
* 위치 정보 명령(NVDA+delete) 실행 시 상황에 적합한 정보를 알리도록 함 (#4219):
 * 편집창과 브라우즈 모드에서는 현재 커서 위치(퍼센트)와 화면 좌표 출력.
 * 파워포인트에서는 선택된 셰이프가 슬라이드내 위치하는 자리 및 다른 셰이프와의 거리 출력.
 * 본 명령을 두번 누르면 이전처럼 특정 컨트롤이 차지하는 위치를 확인할 수 ㅣㅇㅆ음.
* 새 NVDA 언어: 카탈로니아어 추가.

### 변경사항

* Liblouis 점자 변환기 2.5.4 버전 사용. (#4103)

### 버그 수정내역

* 구글 Chrome이나 Chrome 기반 브라우저 사용 시 경고나 대화상자 텍스트중 특정 텍스트(특히 특정 서식이 적용된 텍스트)가 반복으로 출력되던 문제 수정. (#4066)
* 모질라 프로그램에서 브라우즈 모드 사용 시 특정 버튼(예: 페이스북 사이트 상단에 있는 버튼)에서 엔터를 누를때 버튼이 활성화되지 않거나 다른 버튼이 활성화되던 문제 수정. (#4106)
* iTunes에서 탭을 누를때 필요없는 정보가 출력되지 않도록 함. (#4128)
* iTunes내 특정 목록(예: 음악 목록)에서 객체 탐색을 이용하여 다음 항목으로 이동이 불가능하던 문제 수정. (#4129)
* 인터넷 익스플로러 사용 시 첫 글자 명령을 사용하여 WAI ARIA 코드로 처리된 헤딩 HTML 요소로 접근 가능 및 본 헤딩이 브라우즈 요소 목록에 포함되도록 함. (#4140)
* 최신 인터넷 익스플로러 버전에서 같은 페이지 링크를 활성화할때 링크가 가리키는 위치 출력 및  브라우즈 커서가 본 위치로 움직이도록 함. (#4134)
* Microsoft 아웃룩 2010 이상에서 새 계정 및 이메일 계정 설정과 같은 보안용 대화상자의 접근성이 향상됨. (#4090, #4091, #4095)
* 여러 아웃룩 대화상자에서 불필요한 command toolbar 내용이 출력되지 않도록 함. (#4096, #3407)
* Microsoft Word에서 탭을 이용하여 표의 빈 셀로 옮길때 표 끝이라고 출력되지 않도록 함. (#4151)
* Microsoft Word에서 표 이후 글자(표 밖에 있는 빈칸 등)가 표 내 글자로 인식되던 문제 수정. (#4152)
* Microsoft Word 2010 철자 오류 대화상자에서 철자 오류가 있는 단어 대신 첫 굵게 표시된 단어가 출력되던 문제 수정. (#3431) 
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 탭을 누르거나 글자키로 폼 필드로 이동시 필드 제목(HTML 레이블 요소가 사용된 경우)이 출력되지 않던 문제 수정. (#4170)
* Microsoft Word에서 주석 존재 여부 및 위치 알림 정확도가 향상됨. (#3528)
* Microsoft Office 프로그램(예: 워드, 엑셀, 아웃룩) 사용 시 여러 대화상자에서 불필요한 command toolbar 컨테이너 내용이 출력되지 않도록 함. (#4198)
* Microsoft Word, 엑셀 또는 다른 프로그램 실행 시 클립보드 메니저와 파일 복구와 같은 테스크 페인이 포커스되는 것을 방지하여 사용자가 다른 프로그램으로 전환하다가 돌아오는 것을 최소화하도록 함. (#4199)
* 최신 윈도우 버전 사용 시 사용자 언어가 세르비아 라틴어로 설정되었을때 NVDA가 실행되지 않던 문제 수정. (#4203)
* 입력 도움말 모드 사용중 numlock을 눌렀을때 numlock이 토글되도록 하여 키보드와 운영체제간 numlock 토글에 대한 혼돈을 줄임. (#4226)
* 구글 Chrome에서 탭 전환시 페이지 제목이 출력되지 않던 문제 수정(NVDA 2014.2 사용 시 특정 상황에서 이 문제가 발생했었음). (#4222)
* 구글 Chrome이나 Chrome 기반 브라우저 사용 시 문서 URL(주소)가 문서와 함께 출력되던 문제 수정. (#4223)
* "음성 출력 끔" 음성 엔진을 사용(자동 테스트에 유용함)하여 모두 읽기 실행 시 문서 전체를 읽도록 함(이전에는 몇 줄만 읽었음). (#4225)
* Microsoft 아웃룩 서명 편집창 접근 향상 (커서 이동 및 서식 정보 확인 가능). (#3833) 
* Microsoft Word에서 표 셀의 마지막 줄을 읽을때 표 셀의 내용이 출력되던 문제 수정. (#3421)
* Microsoft Word에서 목차의 첫줄 또는 마지막 줄을 읽을때 목차의 내용이 출력되던 문제 수정. (#3421)
* 입력된 단어 출력 및 여러 상황에서 인도어 모음 또는 virama 글자 입력 시 입력된 단어가 깨지는 문제 수정. (#4254)
* 골드웨이브에서 숫자 입력창을 제대로 처리하지 못하던 문제 수정. (#670)
* Microsoft Word에서 control+아래 방향키 또는 control+위 방향키를 사용하여 다음 및 이전 문단을 읽을때 bullet 또는 숫자 목록에서 본 명령을 두번 눌러야 문단을 이동하던 문제 수정. (#3290)

### 개발 변경사항(영문)

* NVDA now has unified support for add-on documentation. See the Add-on Documentation section of the Developer Guide for details. (#2694)
* When providing gesture bindings on a ScriptableObject via __gestures, it is now possible to provide the None keyword as the script. This unbinds the gesture in any base classes. (#4240)
* It is now possible to change the shortcut key used to start NVDA for locales where the normal shortcut causes problems. (#2209)
 * This is done via gettext.
 * Note that the text for the Create desktop shortcut option in the Install NVDA dialog, as well as the shortcut key in the User Guide, must also be updated.

## 2014.2

### 새로운 기능

* 특정 편집창(특히 디스플레이모델이 사용된 필드)에서 선택된 문자가 출력되도록 함. (#770)
* 자바 기반 프로그램에서 라디오 버튼과 같은 그루핑 컨트롤 값의 위치 정보를 확인할 수 있음. (#3754)
* 자바 기반 프로그램에서 특정 컨트롤에 키보드 핫키가 부여된 경우 이를 확인할 수 있음. (#3881)
* 브라우즈 모드에서 랜드마크 레이블 인식 가능 및 요소 목록에 나타나도록 함. (#1195)
* 브라우즈 모드에서 레이블이 있는 구역이 랜드마크로 처리되도록 함. (#3741)
* 인터넷 익스플로러 기반 프로그램 및 문서내 라이브 구역(W3C ARIA)를 지원함에 따라 웹페이지 저자가 지정한 라이브 구역내 내용이 변경될때마다 이를 자동으로 출력하도록 함. (#1846)

### 변경사항

* 브라우즈 모드 사용 시 웹페이지 대화상자나 앱을 빠져나갈때 브라우즈 모드 문서의 이름과 형식이 출력되지 않도록 함. (#4069)

### 버그 수정내역

* 자바 기반 프로그램 사용 시 일반 윈도우 시스템 메뉴 내용이 출력되도록 함. (#3882)
* 화면 탐색 모드 사용중 텍스트를 복사시 줄 끝이 짤리지 않도록 함. (#3900)
* 특정 프로그램에서 포커스 이동 또는 심플 객체 탐색 사용 시 필요없는 공백 객체를 무시하도록 함. (#3839)
* NVDA의 여러 대화상자가 열릴때 이전 음성 출력이 중지되도록 함.
* 브라우즈 모드에서 링크와 버튼 등의 컨트롤 레이블이 접근성 편의상 웹페이지 저자에 의해 가려졌을때에도(예: aria-label/aria-labelledby 사용 시) 제대로 인식되도록 함. (#1354)
* 인터넷 익스플로러에서 브라우즈 모드 사용 시 ARIA presentation으로 처리된 컨테이너 요소의 내용이 무시되지 않도록 함. (#4031)
* Unikey 소프트웨어를 이용한 베트남어 입력이 불가능하던 문제 수정(키보드 설정에 추가된 다른 프로그램에서의 키보드 입력 처리 옵션을 해제하고 사용 바람). (#4043)
* 브라우즈 모드 사용 시 라디오 버튼 및 체크박스 메뉴 아이템이 컨트롤 대신 클릭 가능 텍스트로 인식되던 문제 수정. (#4092)
* 브라우즈 모드에서 라디오 버튼 및 체크박스 메뉴 아이템에 포커스된 경우 포커스 모드에서 브라우즈 모드로 전환되던 문제 수정. (#4092)
* Microsoft PowerPoint 사용 시 입력된 단어 읽기를 선택한 후 벡스페이스를 누를때 삭제된 글자가 이후 입력된 단어에 이어 출력되지 않도록 함. (#3231)
* Microsoft Office 2010 설정 대화상자에 ㅣㅇㅆ는 콤보박스의 이름이 제대로 출력되도록 함. (#4056)
* 모질라 프로그램에서 브라우즈 모드 사용 시 첫 글자 탐색을 이용하여 다음 및 이전 버튼이나 폼필드로 이동시 토글 버튼으로 접근이 불가능했던 문제 수정. (#4098)
* 모질라 프로그램 사용 시 주의(alert) 내용이 두번 출력되지 않도록 함. (#3481)
* 브라우즈 모드에서 컨테이너나 랜드마크의 내용을 읽는중 페이지 컨텐츠가 변경될때(예: 페이스북과 트위터 사이트 사용 시) 컨테이너나 랭드마크의 내용이 반복으로 출력되던 문제 수정. (#2199)
* 응답하지 않는 프로그램에서 빠져나갈때 NVDA가 가끔 다운되던 문제 수정. (#3825)
* 편집창의 내용이 화면에 표시된(그려진) 경우 모두 읽기시 캐럿(편집 커서)이 업데이트되지 않던 문제 수정.  (#4125)

## 2014.1

### 새로운 기능

* Microsoft PowerPoint 2013 지원 (단 보안 모드는 지원않함). (#3578)
* Microsoft Wordㅗ아 엑셀의 기호 삽입 대화상자에서 삽입하고자 하는 기호가 출력되도록 함. (#3538)
* 문서 서식 알림 설정에 클릭 가능 요소 알림 설정을 추가하여 문서의 클릭 가능한 요소가 알려질지 설정할 수 있도록 함 (기본으로 설정되어 있음). (#3556)
* Widcomm 블루투스 드라이버가 설치된 컴퓨터에서 블루투스 점자 디스플레이 사용 가능. (#2418)
* 파워포인트에서 텍스트를 편집할때 링크 텍스트가 출력되도록 함. (#3416)
* ARIA 앱이나 대화상자에서 NVDA+SPACE를 눌러 브라우즈 모드로 전환 후 일반 웹페이지처럼 앱이나 대화상자내 내용을 읽을 수 있음. (#2023)
* 아웃룩 엑스프레스/Windows Mail/Windows Live Mail에서 메시지가 플래그되었거나 첨부 파일이 있을때 그 정보를 출력하도록 함. (#1594)
* Java 기반 프로그램내 표 이동시 셀의 행 및 열 위치 및 머릿말 정보(머릿말이 있는 경우)가 출력되도록 함. (#3756)

### 변경사항

* 페이펀마이어 디스플레이 명령 중 고정 리뷰/포커스로 이동 명령 삭제함 (필요시 기능키 설정을 사용하여 추가할 수 있음). (#3652)
* Microsoft VC Runtime 11 사용으로 인해 윈도우 XP 서비스팩 2 또는 윈도우 서버 2003 서비스팩 1 이전 시스템에서 NVDA 실행 불가능.
* 별표(*)와 드하기(+) 문자가 기호 발음 출력을 기호 출력으로 설정했을때에도 출력되도록 함. (#3614)
* 이스피크 음성 엔진 1.48.04 사용 및 이에 따른 여러 버그 및 언어 수정. (#3842, #3739)

### 버그 수정내역

* Microsoft Excel에서 셀로 이동 또는 선택할때 엑셀이 다운될때 새 셀이 아닌 이전 셀이 출력되던 문제 수정. (#3558)
* Microsoft Excel에서 셀의 팝업 메뉴를 눌렀을때 나타나는 드랍다운 목록을 제대로 처리하지 않던 문제 수정. (#3586)
* iTunes 11에서 스토어를 처음 열때나 스토어 페이지에서 링크를 선택하였을때 브라우즈 모드를 통해 새 컨텐츠를 읽지못하던 문제 수정. (#3625)
* iTunes 11 스토어에서 송 미리듣기 버튼 레이블이 브라우즈 모드에서 알려지지 않던 문제 수정. (#3638)
* 구글 Chrome에서 브라우즈 모드 사용 시 체크박스와 라디오 버튼의 레이블이 잘못 출력되던 문제 수정.  (#1562)
* 인스턴트버드에서 주소록에서 각 항목으로 이동시 불필요한 정보가 출력되던 문제 수정. (#2667)
* 어도비 리더 문서 읽을때 버튼과 같은 컨트롤의 레이블이 툴팁이나 다른 방법으로 덮더씌워졌들때 컨트롤 레이블이 제대로 출력되도록 함. (#3640)
* 어도비 리더 문서 읽을때 "mc-ref" 텍스트가 있는 그래픽 출력 제외됨. (#3645)
* Microsoft Excel에서 모든 셀의 서식 정보가 밑줄이 적용된 것처럼 출력되는 문제 수정. (#3669)
* 브라우즈 모드에서 불필요한 유니코드 문자가 문서 탐색을 방해하던 문제 수정(이로 인해 레이블에서 불필요한 문자열 출력이 거의 사라졌음). (#2963)
* PuTTY 사용 시 아시아 문자 입력이 제대로 처리되지 않던 문제 수정. (#3432)
* 모두 읽기 정지후 문서를 읽을시 읽고있는 텍스트가 아직 읽지않은 요소(예: 표)의 끝이라고 출력되던 문제 수정. (#3688)
* 브라우즈 모드에서 모두 읽기시 건너뛰어 읽기를 선택하고 모두 읽기를 진행하던 중 첫 글자로 다음 요소로 이동시 요소 텍스트 뿐 아니라 요소명(예: 헤딩이라고 출력)도 출력하도록 함. (#3689)
* 건너뛰어 읽기 도중 컨테이너 전후 이동키가 본 설정에 상관없이 모두 읽기를 중지하던 문제 수정(즉 모두 읽기시 컨테이너 밖의 텍스트로부터 모두 읽기가 진행되도록 함). (#3675)
* 단축키 설정에 나열된 터치스크린 명령이 영어 외 타국어로도 출력되도록 함. (#3624)
* 특정 편집창(TRichEdit)이 있는 프로그램(예: Jarte 5.1, BRfácil) 사용 시 마우스 커서를 편집창으로 옮길때 프로그램이 종료되던 문제 수정. (#3693, #3603, #3581)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 ARIA presentation으로 처리된 컨테이너(예: 표)가 출력되지 않도록 함. (#3713)
* Microsoft Word 사용 시 표 셀의 행 및 열 정보가 반복으로 출력되던 문제 수정. (#3702)
* 프랑스어나 독일어와 같이 공백으로 숫자 그루핑을 나눌때 각 숫자 그루핑이 한 숫자로 출력되던 문제 수정(특히 표 셀에 숫자가 있을 경우 문제가 발생했음). (#3698)
* Microsoft Word 2013에서 시스템 캐럿 이동시 점자 커서가 제대로 움직이지 않던 문제 수정. (#3784)
* Microsoft Word에서 점자 디스플레이 커서가 헤딩 문자열의 첫 글자에 위치한 경우 헤딩 레벨 등과 같은 헤딩 정보가 점자로 출력되지 않던 문제 수정. (#3701)
* 사용자 프로필이 지정된 프로그램이 종료되었을때 프로그램 프로필이 제대로 해제되지 않던 문제 수정. (#3732)
* 여러 NVDA 입력창(예: 브라우즈 모드 문자열 찾기 대화상자)에서 아시아 글자 입력 시 후보 대신 NVDA가 출력되던 문제 수정. (#3726)
* 아웃룩 2013 옵션 대화상자내 탭이 출력되지 않던 문제 수정. (#3826)
* 모질라 FireFox와 같은 Gecko 기반 프로그램에서 ARIA live regions 지원 향상됨:
 * aria-atomic 업데이트 지원 향상 및 aria-busy 업데이트 처리 향상. (#2640)
 * 특정 Alt 텍스트(예: Aria-label) 인식 가능. (#3329)
 * 포커스 이동시 live regiions 텍스트가 업데이트된 경우 업데이트 텍스트도 출력하도록 함. (#3777)
* 모질라 FireFox와 같은 Gecko 기반 프로그램에서 브라우즈 모드 사용 시 특정 presentation 컨트롤(특히 ARIA 포커스 가능)이 더 이상 출력되지 않도록 함. (#3781)
* Microsoft ㅜ어드 사용 시 철자 오류가 ㅣㅇㅆ는 문서를 읽을때 NVDA의 반응 속도가 개선됨. (#3785)
* 여러 Java 기반 프로그램 접근성 관련 문제 해결:
 * 프레임이나 창 내에 위치한 컨트롤이 포커스되어 있는 경우 포커스된 컨트롤이 인식되지 않던 문제 수정. (#3753)
 * 1/1과 같은 불필요한 라디오 버튼 위치 정보가 출력되던 문제 수정. (#3754)
 * JComboBox 컨트롤 정보가 제대로 출력되게 함(컨트롤이 HTML로 인식되던 문제, 확대/축소 정보가 제대로 인식되지 않던 문제 수정). (#3755)
 * 대화상자 텍스트 출력시 이전에 누락되었던 텍스트가 출력되도록 함. (#3757)
 * 포커스된 컨트롤의 이름, 값 및 설명 변경 정보가 더 정확하게 출력되도록 함. (#3770)
* 윈도우 8 사용 시 NVDA 로그 뷰어와 windbg와 같이 여러줄 텍스트가 있는 RichEdit 컨트롤에서 NVDA가 강제 종료되던 문제 수정. (#3867)
* 고급 DPI 값이 설정된 시스템(특히 최근에 출시된 스크린이 장착된 컴퓨터) 사용 시 여러 프로그램에서 마우스 위치가 제대로 추적되지 않던 문제 수정. (#3758, #3703)
* 웹브라우저 사용 시 NVDA가 갑자기 다운되던 문제 수정 (이때 NVDA를 재시작하여야 제대로 동작함). (#3804)
* Papenmeier 점자 디스플레이가 초기에 USB로 연결되지 않아도 본 디스플레이 선택후 사용 가능. (#3712)
* Papenmeier Braillex 구형 모델을 선택하였음에도 디스플레이가 연결되어있지 않을때 NVDA가 다운되던 문제 수정.

### 개발 변경사항(영문)

* AppModules now contain productName and productVersion properties. This info is also now included in Developer Info (NVDA+f1). (#1625)
* In the Python Console, you can now press the tab key to complete the current identifier. (#433)
 * If there are multiple possibilities, you can press tab a second time to choose from a list.

## 2013.3

### 새로운 기능

* Microsoft Word 문서 폼 필드 인식 가능. (#2295)
* Microsoft Word에서 트랙 변경을 설정하고 NVDA 문서 서식 설정에서 문서 리비전 알림을 선택한 경우 리비전이 출력되도록 함 (본 NvDA 설정은 해제되어 있음). (#1670)
* Microsoft Excel 2003-2010 사용 시 드랍다운 목록을 열고 탐색 시 항목이 출력되도록 함. (#3382)
* 키보드 설정의 "모두 읽기 사용 시 건너뛰어 읽기 사용"을 활용하여 모두 읽기 사용중 다음/이전 줄/문단/웹 요소로 건너뛸때 모두 읽기가 계속 실행되도록 함 (기본적으로 본 옵션은 해제되어 있음). (#2766)
* 새 NVDA 단축키 설정을 사용하여 사용자가 손쉽게 NvDA 단축키를 조정할 수 있도록 함 (예: 키보드 명령 조정 등). (#1532)
* 상황에 따라 다른 사용자 환경 프로필을 사용할 수 있음 (수동 또는 프로그램 실행과 같이 자동으로 적용 가능). (#87, #667, #1913)
* Microsoft Excel에서 셀이 링크인 경우 링크로 인식하도록 함. (#3042)
* Microsoft Excel에서 셀에 코멘트가 있는 경우 코멘트 정보도 확인 가능. (#2921)

### 버그 수정내역

* Zend Studio 개발 도구 사용 시 Eclipse 사용할때와 똑같이 NVDA가 작동하도록 함. (#3420)
* Microsoft 아웃룩 2010 사용 시 메시지 규칙 대화상자에 있는 여러 체크박스의 선택 및 해제 상태가 알려지지 않던 문제 수정. (#3063)
* 모질라 FireFox와 같은 프로그램에서 특정 컨트롤이 핀(pinned)된 경우 이를 인식할 수 있음. (#3372)
* Windows 키나 Alt 키를 NVDA 명령 조합키(modifier key)로 할당할 수 있음 (이전 버전에서 만약 이 키들이 명령에 할당되면 명령 실행 시 시작 메뉴나 메뉴바가 간혹 열렸었음). (#3472)
* 여러 키보드 배열이 설치된 컴퓨터에서 브라우즈 모드 문서에서 텍스트 선택 명령(예: Control+Shift+End) 실행 시 키보드 배열이 변경되는 문제 수정. (#3472)
* 인터넷 익스플로러 사용 시 NvDA가 종료된 후 프로그램이 다운되던 문제 수정. (#3397)
* 신형 컴퓨터에서 물리적 컴퓨터 이동 또는 여러 이벤트가 NVDA 명령으로 인식되던 문제 수정 (예전이는 이 이벤트들이 음성을 중지시키거나 다른 NVDA 명령을 실행하였음). (#3468)
* Poedit 1.5.7 사용 시 NVDA가 이전 버전과 동일하게 동작하도록 함 (Poedit 업데이트 권장). (#3485)
* 보안 처리가 된 Microsoft Word 2010 문서를 읽을시 워드가 종료되던 문제 수정. (#1686)
* NVDA 페키지 실행 시 부정확한 명령 스위치를 입력하였을때 연속으로 오류 메시지가 뜨던 문제 수정. (#3463)
* Microsoft Word 사용 시 그래픽이나 객체의 alt tag 텍스트에 따옴표와 같은 특정 문자열이 있는 경우 alt tag 텍스트가 출력되지 않던 문제 수정. (#3579)
* 브라우즈 모드에서 가로로 표시된 목록의 항목수가 어떤때 두배로 알려지던 문제 수정. (#2151)
* Microsoft Excel에서 CTRL+A를 눌렀을때 선택 변경 내용이 제대로 알려지지 않던 문제 수정. (#3043)
* XHTML 문서를 인터넷 익스플로러와 같은 MSHTML 기반 프로그램에서 제대로 읽을 수 있도록 함. (#3542)
* 키보드 설정에서 NVDA 기능키 설정이 모두 해제된 경우 이에 대한 오류 메시지가 뜨도록 함 (기능키를 최소한 하나 이상 설정 바람). (#2871)
* Microsoft Excel에서 다중 선택된 셀과 통합된 셀이 다르게 출력되도록 함. (#3567)
* 브라우즈 모드 사용 시 웹사이트에 표시된 대화상자나 앱에서 빠져나갈때 커서 위치가 다른 곳에 위치하던 문제 수정. (#3145)
* 특정 시스템에서 휴멍웨어 Brailliant B/BI 디스플레이가 USB로 연결되었음에도 NVDA가 인식하지 않던 문제 수정.
* 탐색 객체가 화면(위치)에 존재하지 않을때 화면 탐색 모드로 전환되지 못하는 문제 수정 (이때 리뷰 커서는 화면 상단에 ㅜ이치하게 됨). (#3454)
* 특정 시스템에서 Freedom Scientific 디스플레이가 USB로 연결되었음에도 NVDA가 인식하지 않던 문제 수정. (#3509, #3662)
* Freedom Scientific 디스플레이 사용 시 여러 키들이 동작하지 않던 문제 수정. (#3401, #3662)

### 개발 변경사항(영문)

* AppModules now contain productName and productVersion properties. This info is also now included in Developer Info (NVDA+f1). (#1625)
* In the Python Console, you can now press the tab key to complete the current identifier. (#433)
 * If there are multiple possibilities, you can press tab a second time to choose from a list.

## 2013.2

### 새로운 기능

* Chromium Embedded Framework 컨트롤을 기반으로한 여러 웹 앱 지원. (#3108)
* 새 이스피크 보이스: Iven3.
* 스카이프 체팅창이 포커스된 경우 새 메시지를 자동으로 읽도록 함. (#2298)
* Tween 지원: 탭 이름 및 트위트 읽을시 필요없는 내용 출력하지 않도록 함.
* 점자 설정에서 메시지 알림 시간을 0초로 한 경우 NVDA 메시지가 점자로 출력되지 않도록 함. (#2482)
* 추가 기능 관리자의 추가 기능 탐색 버튼을 사용하여 추가 기능 모음 웹사이트에 접속 및 본 사이트에서 더 많은 추가 기능을 다운받아 설치할 수 있음. (#3209)
* NVDA 시작 대화상자(NVDA가 처음 실행될때 열림)에 NvDA를 윈도우 로그언 후 실행할지를 묻는 체크상자 추가. (#2234)
* Dolphin Cicero 사용 시 NVDA가 임시 종료되도록 함. (#2055)
* Miranda IM/Miranda NG x64 (64 비트 버전) 지원 추가. (#3296)
* 윈도우 8.1 시작 화면의 검색 결과를 자동으로 알림. (#3322)
* 엑셀 2013 지원 (표 탐색 및 셀 데이타를 편집할 수 있음). (#3360)
* 포커스 14 Blue, 80 Blue 및 신형 포커스 40 Blue를 블루투스로 연결하여 사용할 수 있음. (#3307)
* Microsoft 아웃룩 2010에서 자동 끝내기 알림 추가. (#2816)
* 점자 표기법: 영국 영어 컴퓨터 점자, 한국어 2종 (약자) 및 러시아어 컴퓨터용 점자 표기법 추가.
* 새 NVDA 언어: 파르시어 추가. (#1427)

### 변경사항

* 터치스크린 사용 시 객체 탐색 모드에서 한손까락 왼쪽/오른쪽 쓸어내리기를 실행할때 현재 컨테이너 (창)에 있는 객체 뿐 아니라 화면 전체에 있는 객체로도 이동할 수 있음. 이전 방식을 원하면 두손까락 쓸어내리기를 실행바람.
* 브라우즈 모드 설정에 있는 구조 테이블 알림이 구조 테이블 인식으로 변경됨 (즉 첫 글자를 사용하여 읽을때 본 체크박스가 해제되어 있으면 구조 테이블이 인식되지 않도록 함). (#3140)
* 고정 리뷰가 객체, 문서 및 화면 탐색 모드로 세분화됨. (#2996)
 * 객체 탐색 모드는 현 탐색 객체의 내용을, 문서 탐색 모드는 브라우즈 모드 문서가 있을시 문서의 내용을, 화면 탐색 모드는 현 프로그램 화면에 있는 내용을 읽을시 사용.
 * 고정 리뷰를 토글하던 명령은 위 탐색 모드 선택 명령으로 교체됨.
 * 문서 및 화면 탐색 모드 사용 시 탐색 객체는 리뷰 커서 위치에 있는 객체에 위치하게 됨.
 * 화면 탐색 모드로 변경 후 사용자가 객체나 문서 탐색 모드로 변경할때까지 계속 화면 탐색 모드로 유지됨.
 * 브라우즈 모드 문서 유무에 따라 객체 또는 문서 탐색 모드로 자동으로 전환됨.
* Liblouis 점자 변환기 2.5.3 버전 사용. (#3371)

### 버그 수정내역

* 화면 객체를 엑션하기전 엑션을 활성 이전에 알리도록 함 (예: 열리기 전 열림이라고 알림). (#2982)
* 최신 스카이프 버전 사용 시 검색 및 체팇창에서의 커서 따라가기 및 글자 읽기 관련 버그 수정. (#1601, #3036)
* 스카이프 최신 체팅창에서 새 이벤트 수가 표시된 경우 이를 알리도록 함. (#1446)
* 아랍어와 같은 RTL 언어 텍스트 읽기 및 커서 정보 확인 기능이 향상됨 (예: 엑셀에서 RTL 사용이 편리해졌음). (#1601)
* 인터넷 익스플로러에서 버튼이나 폼 필드로 이동할때 사이트 접근성 향상용으로 표시된 버튼 링크도 인식하도록 함. (#2750)
* 브라우즈 모드 사용 시 문서를 읽는데 방해가 되지 않도록 트리뷰 내용이 나타나지 않도록 함 (트리뷰 내용을 보려면 트리뷰에서 엔터를 눌러 확인하기 바람). (#3023)
* 포커스 모드 사용 시 콤보 박스에서 Alt+위나 아래 화살표로 콤보박스를 열시 브라우즈 모드로 전환되던 문제 수정. (#2340)
* 인터넷 익스플로러 10에서 표 셀로 움직일때 사이트 저자에 의해 표 셀이 포커스되지 않도록 한 경우 포커스 모드로 전환되지 않도록 함. (#3248)
* 업데이트 확인 시점보다 시스템 시간이 빠른 경우 NVDA 재시작시 NVDA가 실행되지 않던 문제 수정. (#3260)
* 알림 표시줄의 내용이 점자에 표시되었을때 표시줄 변경값을 점자로도 확인할 수 있음. (#3258)
* 모질라 프로그램에서 브라우즈 모드 사용 시 표에 대한 켑션이 두번 출력되던 문제 수정. 또한 표 켑션과 설명이 있을때 설명도 출력하도록 함. (#3196)
* 윈도우 8에서 키보드 언어 변경시 새 입력 언어명이 출력되도록 함 (예전에는 이전 사용하던 언어명이 출력되었음).
* 윈도우 8에서 IME 변경시 변경값이 제대로 출력되도록 함.
* 구글 일본어 또는 Atok IME 입력 방식 사용 시 바탕 화면에서 필요 없는 내용이 출력되던 문제 수정. (#3234)
* 윈도우 7 이상 사용 시 언어 전환시 음성 인식 또는 터치 입력이 전환 언어로 출력되던 문제 수정.
* 특정 문서 편집기에서 입력한 글자 읽기를 활성화하고 control+backspace를 누를시 NVDA가 특수 문자(0x7f)를 말하던 문제 수정. (#3315)
* 이스피크가 XML이나 특정 컨트롤 글자 읽을때 음성 설정 (크기, 고저 등)이 변경되던 문제 수정. (#3334) (#437 문제 되풀이됨)
* Java 기반 프로그램 사용 시 포커스된 컨트롤의 이름 또는 값의 변경값 알림 및 그 후 확인시 제대로 된 내용이 출력되지 않던 문제 수정. (#3119)
* Scintilla 컨트롤에서 단어 끊기 기능 사용 시 각 줄이 제대로 알려지지 않던 문제 수정. (#885)
* 모질라 프로그램에서 읽기 전용 목록 항목들(예: twitter.com에서 포커스 모드를 사용하여 트위트를 읽을때)이 제대로 출력되도록 함. (#3327)
* Office 2013의 확인 대화상자의 내용이 자동으로 읽지않던 문제 수정.
* Microsoft Word에서 특정 표를 읽을시 다운되던 문제 수정. (#3326)
* Microsoft Word에서 표의 셀이 여러 행에 걸쳐 있는 경우 NVDA의 표 탐색 명령(Control+Alt+방향키) 실행 시 다운되던 문제 수정.
* 추가 기능 관리자는 이미 열려 있고 사용자가 관리자를 재실행할때 (예: NVDA 도구 메뉴에서 선택하거나 추가 기능 파일을 연 경우) 추가 기능 관리자를 닫을 수 없던 문제 수정. (#3351)
* Office 2010 중국어 또는 일본어 IME 사용 시 특정 대화상자에서 NVDA가 다운되던 문제 수정. (#3064)
* 점자 디스플레이 사용 시 여러 빈 칸이 하나의 빈 칸으로 압축되던 문제 수정. (#1366)
* Zend Eclipse PHP 개발 도구 사용 시 Eclipse 사용할때와 똑같이 NVDA가 작동하도록 함. (#3353)
* 인터넷 익스플로러에서 임베디드 객체 (예: 플래시 컨텐츠)에서 엔터를 누른 후 탭을 누르지 않고도 컨텐츠의 기능을 이용할 수 있음. (#3364)
* 파워포인트에서 문서를 편집시 맨 아래 줄이 비어있을때 맨 아래줄로 이동시 이전 줄이 알려지던 문제 수정. (#3403)
* Microsoft PowerPoint에서 특정 객체를 선택 또는 편집할때 객체값이 두번 출력되던 문제 수정. (#3394)
* Adobe Reader 사용 시 서식이 잘못 적용된 문서(특히 표 밖에 표 행이 존재하는 경우)를 읽을때 NVDA가 프로그램을 다운되게 하던 문제 수정. (#3399)
* 파워포인트의 thumbnails view를 사용하여 슬라이드 목록을 편집시 선택된 슬라이드가 삭제된 후 다음 슬라이드에 포커스가 옮겨지도록 함.. (#3415)

### 개발 변경사항(영문)

* windowUtils.findDescendantWindow has been added to search for a descendant window (HWND) matching the specified visibility, control ID and/or class name.
* The remote Python console no longer times out after 10 seconds while waiting for input. (#3126)
* Inclusion of the bisect module in binary builds is deprecated and may be removed in a future release. (#3368)
 * Add-ons which depend on bisect (including the urllib2 module) should be updated to include this module.

## 2013.1.1

본 버전의 주요 특징은 최신 번역본 추가 및 아일랜드어 사용 시 NVDA가 실행되지 않던 문제 수정 및 기타 버그 수정입니다.

### 버그 수정내역

* 한국어나 일본어 입력 방식 사용 시 (특히 본 방식이 기본 입력 방식인 경우) NVDA 인터페이스에서 글자가 제대로 입력되지 않던 문제 수정. (#2909)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 잘못 입력된 필드 정보가 있는 필드가 제대로 처리되지 않던 문제 수정. (#3256)
* 아일랜드어 NVDA 실행 시 실행되지 않던 문제 수정.

## 2013.1

이번 버전의 주 기능들: 더 효율적인 노트북 키보드 레이아웃, 파워포인트 문서 편집 지원, 웹브라우저에서의 긴 설명 확인 및 점자 키보드가 탑제된 디스플레이에서의 문자 입력 등입니다.

### 꼭 읽어주세요

#### 새 노트북 키보드 레이아웃

사용자의 편의와 효율성을 높이기 위해 노트북 레이아웃을 변경하였습니다.
새 레이아웃에서 리뷰 커서 사용 시 NVDA 키 및 다른 명령키와 방향키를 사용하도록 하였습니다.

새 명령키는 다음과 같습니다:

| 이름 |키|
|---|---|
|모두 읽기 |NVDA+a|
|현재 줄 읽기 |NVDA+l|
|현재 선택된 텍스트 읽기 |NVDA+shift+s|
|상태 표시줄 읽기 |NVDA+shift+end|

이 외 객체 탐색, 리뷰 커서, 마우스 조작 및 음성 설정 명령들이 변경되었습니다.
자세한 사항은 [기능키 목록](keyCommands.html) 문서를 참조하십시오.

### 새로운 기능

* Microsoft PowerPoint 문서 읽기 및 편집 기능 지원 (기초단계임) (#501)
* Lotus Notes 8.5에서의 메시지 작성 및 읽기 기능 지원 (기초 단계). (#543)
* 자동 언어 변경 기능을 Microsoft Word 문서 읽을때에도 적용. (#2047) 
* 인터넷 익스플로러와 같은 MSHTML과 Firefox와 같은 Gecko 기반 프로그램에서 긴 설명 (long description) 인식 가능 (NVDA+D를 사용하여 긴 설명을 새창에 띄워 확인할 수 있음). (#809)
* 인터넷 익스플로러 9 이상에서 파일 다운로드 상태와 같은 알림 메시지가 출력되도록 함. (#2343)
* 인터넷 익스플로러와 같은 MSHTML 브라우즈 모드 문서에서 표의 행 및 열 머릿말이 자동으로 출력하도록 함. (#778)
* 새 NVDA 언어: 아라곤어 및 아일랜드어 추가.
* 점자 표기법: 뎀마크어 2종 및 한국어 1종 (정자) 표기법 추가. (#2737)
* 도시바 블루투스 드라이버가 설치된 컴퓨터에서 블루투스 점자 디스플레이 사용 가능. (#2419)
* Freedom Scientific 디스플레이 사용 시 연결 포트 설정 가능 (자동 연결, USB 또는 블루투스 중 선택 가능).
* 휴먼웨어 브레일노트 지원 추가 (브레일노트에서 터미널 모드 진입후 사용 가능). (#2012)
* 구형 페이펀마이어 BRAILLEX 디스플레이 지원 추가. (#2679)
* 점자 디스플레이가 점자 키보드를 탑제한 경우 컴퓨터 점자를 사용하여 텍스트 입력 가능. (#808) 
* 키보드 설정에 텍스트 입력 또는 엔터키 입력 시 음성이 정지할 것인지에 대한 설정 추가. (#698)
* 여러 구글 Chrome을 기반으로 한 웹 브라우저 지원 추가: Rockmelt, BlackHawk, Comodo Dragon, SRWare Iron. (#2236, #2813, #2814, #2815)

### 변경사항

* Liblouis 점자 변환기 2.5.2 버전 사용. (#2737)
* 사용자 편의 및 효율성을 높이기 위해 노트북 키보드 레이아웃 변경됨. (#804)
* 이스피크 음성 엔진 1.47.11 사용. (#2680, #3124, #3132, #3141, #3143, #3172)

### 버그 수정내역

* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 다음과 이전 구분선(separator)으로 움직이는 핫키가 제대로 동작하도록 함. (#2781)
* NVDA 실행 시 사용중이던 음성 엔진 실행이 실패하여 음성 엔진 설정이 eSpeak나 엔진 없음으로 변경된 경우 새로 변경된 설정이 저장되지 않도록 설정 (즉 NVDA가 다시 실행 시 이전에 사용하던 음성 엔진을 실행하도록 함). (#2589)
* NVDA 실행 시 사용중이던 점자 디스플레이와의 연결이 실패하여 점자 디스플레이 설정이 점자 출력 끔으로 변경된 경우 새로 변경된 설정이 저장되지 않도록 설정 (즉 NVDA가 다시 실행 시 이전에 사용하던 디스플레이와 연결을 시도하도록 함). (#2264)
* 모질라 프로그램에서 브라우즈 모드 사용 시 표에 대한 업데이트 정보가 출력되지 않던 문제 수정 (예: 특정 셀이 업데이트되었을 때 행과 열의 좌표가 표시되지 않거나 표 탐색 기능이 제대로 동작하지 않던 문제 수정). (#2784)
* 웹브라우저에서 브라우즈 모드 사용 시 클릭 가능한 그래픽 (특히 레이블이 표시되지 않는 그래픽)이 제대로 표시되도록 함. (#2838)
* SecureCRT: 이전 및 최신 버전 지원. (#2800)
* 윈도우 XP에서 Easy Dots IME과 같은 입력 방식 사용 시 문자열이 처리되지 않던 문제 수정.
* 윈도우 7에서 Microsoft Pinyin 중국어 입력 방식 사용 시 후보자 목록에서 왼쪽 및 오른쪽 화살표로 페이지를 변경하거나 Home을 눌러 후보자를 열때 후보자를 읽지않던 문제 수정.
* 기호 및 구두점 발음 설정에서 특정 기호의 발음 정보를 저장할때 "preserve" 고급 필드가 사라지던 문제 수정. (#2852)
* 자동 업데이트 사용을 해제한 후 NVDA가 재시작하지 않고도 새 설정이 적용되도록 함.
* 추가 기능 삭제중 다른 응용 프로그램이 추가 기능이 설치된 폴더를 엑세스할 경우 NVDA를 재시작하고자 할때 실행이 되지않던 문제 수정. (#2860)
* 고정 리뷰를 사용하여 Dropbox의 설정 대화상자에 있는 탭 레이블을 확인할 수 있음.
* 윈도우 기본값 외 입력 언어 사용 시 명령 및 입력 도움말에서 입력된 글자가 인식되지 않던 문제 수정.
* 독일어와 같이 플러스 (+)키가 키보드 키 중 하나일 경우 "plus" 단어를 사용하여 해당키에도 명령을 할당할 수 있음. (#2898)
* 인터넷 익스플로러와 같은 MSHTML 컨트롤에서 인용 문구 (block quote)가 제데로 알려지지 않던 문제 수정. (#2888)
* 휴먼웨어 Brailliant BI/B 디스플레이가 블루투스로 연결되었을때 USB로 연결하지 않고도 선택하여 사용 가능.
* 브라우즈 모드의 구성 요소 목록에서 대문자가 포함된 요소명을 찾을때 대소문자 관계없이 찾고자 하는 요소명이 뜨도록 함 (이전에는 목록이 비어있었음). (#2951)
* 모질라 브라우저에서 플래시 컨텐츠에서 브라우즈 모드를 사용할 수 없었던 문제 수정. (#2546)
* 약자 점자 사용 시 컴퓨터 점자로 풀이 설정을 선택한 경우 커서 위치에 있는 단어가 여러 셀로 표시될 경우 (예: 대문자 표시) 커서가 제대로 옮겨지도록 함. (#2947)
* Microsoft Word 2003과 인터넷 익스플로러 편집창과 같은 컨트롤에서 선택된 텍스트가 점자로 제대로 표시되도록 함.
* 점자 디스플레이 사용 시 Microsoft Word에서 반대 방향으로 글자 선택이 되지 않던 문제 해결.
* Scintilla 편집창에서 다중 문자를 읽을때나 삭제시 문자가 출력되지 않던 문제 수정. (#2855)
* - 사용자 경로에 다중 글자가 사용된 경우 NVDA가 설치되지 않던 문제 수정. (#2729)
* 64비트 프로그램에서 리스트뷰 (SysListview32) 그루핑을 알릴때 오류가 발생하던 문제 수정.
* 모질라 프로그램에서 브라우즈 모드 사용 시 특정 상황에서 텍스트 컨텐츠가 편집 가능한 텍스트로 잘못 인식되던 문제 수정. (#2959)
* IBM Lotus Symphony와 오픈Office에서 캐럿이 움직일때 리뷰 커서도 움직이도록 함.
* 윈도우 8에서 인터넷 익스플로러 사용 시 어도비 플래시 컨텐츠를 접근할 수 없던 문제 해결. (#2454)
* Papenmeier Braillex Trio 사용 시 나타나던 블루투스 연결 문제 수정. (#2995)
* NVDA에서 특정 SAPI5 엔진 (예: Koba)을 사용할 수 없었던 문제 수정. (#2629)
* 자바 엑세스 브리지 기반 프로그램 사용 시 편집창에서 점자가 캐럿을 제대로 따라가지 않던 문제 수정. (#3107) 
* 랜드마크가 사용된 문서에서 폼 (form) 랜드마크 인식 가능. (#2997) 
* 이스피크를 사용하여 글자 단위로 읽을때 나타나던 문제 (예: 외국어 글자의 이름 대신 소리나 일반 이름이 출력되던 문제) 수정. (#3106)
* 사용자 경로에 ASCII 외 글자가 포함된 경우 사용자 설정을 시스템 설정으로 복사 시도중(예: 로그언 창이나 보안 화면에서 사용하고자 할때) 복사 작업이 실패하던 문제 수정. (#3092)
* 특정 .net 프로그램에서 아시아 글자 입력 시 NVDA가 다운되던 문제 수정. (#3005)
* 인터넷 익스플로러 10 기준 모드(예: [www.gmail.](http://www.gmail.)com의 로그인 페이지)에서 브라우즈 모드를 사용할 수 없었던 문제 수정. (#3151)

### 개발 변경사항(영문)

* Braille display drivers can now support manual port selection. (#426)
 * This is most useful for braille displays which support connection via a legacy serial port.
 * This is done using the getPossiblePorts class method on the BrailleDisplayDriver class.
* Braille input from braille keyboards is now supported. (#808)
 * Braille input is encompassed by the brailleInput.BrailleInputGesture class or a subclass thereof.
 * Subclasses of braille.BrailleDisplayGesture (as implemented in braille display drivers) can also inherit from brailleInput.BrailleInputGesture. This allows display commands and braille input to be handled by the same gesture class.
* You can now use comHelper.getActiveObject to get an active COM object from a normal process when NVDA is running with the UIAccess privilege. (#2483)

## 2012.3

이번 버전의 주 기능들: 아시아 글자 입력 기능; 윈도우 8에서의 기초적인 터치스크린 탐색 지원; Microsoft Excel에서의 행 및 열 제목 설정 기능; 여러 점자 디스플레이 지원 추가 등입니다.

### 새로운 기능

* IME와 TSF 써비스를 이용한 아시아 글자 입력 기능:
 * 후보자 알림 및 탐색
 * 입력 글쇠 알림 및 탐색
 * 읽기 문자열 알림
* 어도비 문서에서 및줄 및 스트라이크 문자 알림 가능 (#2410)
* 스티키 키 작동시 NVDA 기능키도 스티키 키로 사용 가능 (#230)
* Microsoft Excel에서 행과 열 머릿말 알림 기능 추가. NVDA+Shift+C를 눌러 현재 행을 열 머릿말 행으로, NVDA+Shift+R을 눌러 현재 열을 행 머릿말 열로 지정; 이 키들을 두번 눌러 머릿말 설정을 해제할 수 있음. (#1519)
* 힘스 한소네, 브레일 에지 및 싱크브레일 지원 추가 (#1266, #1267)
* 윈도우 8에서 만약 도움말 알림이 설정되었다면 토스트 알림창 읽기 가능 (#2143)
* 윈도우 8에서의 기초적인 터치스크린 탐색 기능 추가:
 * 손가락이 위치한 곳의 문자열 읽기
 * 터치 명령으로 객체 탐색, 텍스트 읽기 및 여러 다른 명령 사용 가능
* VIP Mud 지원 추가 (#1728)
* 어도비 리더 사용 시 만약 테이블에 줄거리가 있는 경우 줄거리 내용 표시. (#2465)
* 어도비 리더에서 테이블 행과 열에 머릿말이 있는 경우 머릿말 읽기 가능. (#2193, #2527, #2528)
* NVDA 번역본: 네팔어, 슬로베니아어, 에디오피아어, 한국어 추가.
* Microsoft 아웃룩 2007에서 이메일 주소 입력 시 자동 끝내기 알림 추가 (#689)
* 새 이스피크 보이스: Gene, Gene2. (#2512)
* 어도비 리더에서 쪽수 알림 가능. (#2534)
 * 어도비 리더 XI 사용 시 쪽수 레이블이 인는 경우 (예: 섹션별로 쪽수가 다를때) 레이블을 인식하도록 함 (예전에는 쪽수가 순차적으로 출력되었음).
* CTRL+NVDA+R을 세번 누르거나 NVDA 메뉴에 있는 "NVDA 환경 설정 초기화"를 사용하여 설정을 초기화할 수 있음. (#2086)
* 니판텔레소프트 Seika 3, 4, 5 및 Seika80 디스플레이 지원 추가 (#2452)
* 포커스나 펙메이트 디스플레이 사용 시 윗줄 라우팅 버튼 중 첫째와 마지막 버튼을 사용하여 디스플레이 이동 가능. (#2556)
* 포커스 디스플레이 지원 향상됨 (advance bar, 스크롤 라커를 사용한 기능키 및 그 외 여러 점자 기능키 추가). (#2516)
* 모질라 프로그램들과 같이 IAccessible2 기술을 사용하는 프로그램에서 브라우즈 모드 외에서도 테이블 행 및 열 머릿말 알림 가능. (#926)
* Microsoft Word 2013에서의 문서 컨트롤 지원 (기본 지원 단계). (#2543)
* 모질라 프로그램과 같은 IAccessible2를 사용하는 프로그램에서 텍스트의 위치 확인 가능. (#2612)
* 여러 열을 지니고 있는 테이블 행이나 윈도우 목록 컨트롤에서 테이블 탐색 키를 사용하여 각 열을 읽을 수 있음. (#828)
* 점자 표기법: 에스토니아어 0종 점자, 포르투갈어 8점 컴퓨터 점자 및 이탈리아어 6점 컴퓨터 점자 표기법 추가. (#2319, #2662)
* NVDA가 시스템에 설치되었다면 NVDA 추가 기능 설치 파일을 실행할때 NVDA가 처리하도록 함 (예: 윈도우 탐색기나 파일 다운로드 후 파일을 실행할 경우). (#2306)
* 신형 페이펀마이어 BRAILLEX 디스플레이 지원 추가. (#1265)
* 윈도우 7 이상의 탐색기나 위치 정보가 있는 컨트롤에서의 위치 정보 알림 가능. (#2643)

### 수정된 기능들

* NVDA 리뷰 커서 설정에 있는 "Follow keyboard focus" 옵션을 "Follow system focus" (한국어: 시스템 포커스 따라가기)로 변경하여 다른 NVDA 메시지들과 용어를 통일함.
* 점자 출력이 리뷰 커서에 연동되어 있고 현재 객체가 텍스트 객체가 아닌 경우 (예: 편집창) 라우팅 키를 눌러 객체를 활성화 가능. (#2386)
* 새 환경 설정을 설정하는 경우 "환경 저장" 옵션이 기본으로 선택되도록 수정.
* 이전 설치된 NVDA를 업데이트하는 경우 만약 사용자가 NVDA 핫키를 변경하였다면 업데이트 시 NVDA 기본 핫키 (CTRL+Alt+N)가 적용되지 않도록 함. (#2572)
* 추가 기능 목록에서 기능 이름이 기능 실행 상태 이전에 표시되도록 함. (#2548)
* 설치하고자 하는 추가 기능이 이미 NVDA에 설치되어 있고 설치할 버전이 설치된 버전과 같거나 이후 버전인 경우 오류 대화상자 대신 업데이트 하겠는지에 대해 질문하도록 함. (#2501)
* 현재 객체 알림 외 다른 객체 탐색 명령 실행 시 알려주던 정보가 축소됨 (더 만읂 정보를 확인하려면 현재 객체 알림 명령을 실행하십시오). (#2560)
* Liblouis 점자 변환기 2.5.1 버전 사용. (#2319, #2480, #2662, #2672)
* 터치스크린 명령어 추가로 인해 "키보드 기능키 목록"이 "기능키 목록"으로 변경됨.
* NVDA 실행 시 두번 이상 요소 목록 대화상자를 연 경우 이전에 검색한 요소의 목록을 보여주도록 함. (#365)
* 거의 모든 윈도우 8의 메트로 프로그램에서 프로그램 전체가 브라우즈 모드로 인식 불가됨.
* Handy Tech BrailleDriver COM-Server 1.4.2.0 버전 사용.

### 버그 수정내역

* 윈도우 비스타 이상에서 Win+L로 컴퓨터를 잠근 후 잠금을 풀때에 윈도우 키가 스티키 키로 처리되던 문제 수정. (#1856)
* 어도비 리더에서 테이블 행이 머릿말로 인식되지 않던 문제 수정 (이로 인해 테이블 탐색 명령을 사용하여 행 머릿말을 읽을 수 있음). (#2444)
* 어도비 리더에서 특정 테이블 셀이 두개 이상의 행이나 열을 차지할때 셀이 제대로 처리되지 않던 문제 수정 (#2437, #2438, #2450)
* NVDA 설치 파일 실행전 설치 프로그램이 파일의 건강 상태를 확인한 후 실행하도록 함. (#2475)
* NVDA 업데이트 다운로드가 실패한 경우 임시 다운로드 파일을 삭제하도록 함. (#2477)
* NVDA 사용자 환경을 시스템 환경으로 복사시 (예: 보안창에서 실행하고자 할 경우) NVDA가 다운되던 문제 수정 (이때 NVDA는 관리자 개정으로 실행됨). (#2485)
* 윈도우 8 시작 화면 타일에서의 음성 및 점자 출력 개선 (타일명이 반복되어 출력되던 문제, 모든 타일이 "선택 해제"로 표시되던 문제 및 현재 날씨와 같은 라이브 정보가 출력되지 않던 문제 수정).
* Microsoft 아웃룩이나 다른 비밀번호 편집창과 같은 비밀번호 입력창에서 비밀번호가 출력되던 문제 수정. (#2021)
* 어도비 리더에서 폼 필드 내 변경된 정보가 브라우즈 모드에서 읽어지도록 수정. (#2529)
* 윈도우 비스타 이상 컴퓨터에 NVDA가 설치된 경우 Microsoft Word의 문법 확인 기능 지원 개선 (예: 문법 오류 표시 향상).
* 거의 대부분의 타국어 추가 기능 (설치 파일 내에 영어 외 타국어로 된 파일명이 있는 파일) 설치 가능. (#2505)
* 어도비 리더에서 문서 탐색 시 특정 언어로 된 텍스트가 읽어지지 않던 문제 수정. (#2544)
* 영어 외 타국어 추가 기능 설치시 확인 대화상자에서 가능하면 타국어로 된 기능명 표시 가능. (#2422)
* .net와 실버라이트와 같은 UI 자동화를 사용하는 프로그램에서 슬라이더와 같은 컨트롤에서의 숫자 값 계산 수정. (#2417)
* 진행률 표시 설정값이 NVDA 설치 및 휴대용 버전 생성 진행률과 같은 미지의 진행률에도 적용되도록 함. (#2574)
* 윈도우 잠금 화면과 같은 보안 화면에서 점자 디스플레이에서의 NVDA 명령 실행 불가. (#2449)
* 브라우즈 모드내 내용이 변경된 경우 점자로도 변경된 내용을 출력하도록 함. (#2074)
* 잠금 화면과 같은 보안 화면에서 NVDA를 사용하여 음성이나 점자를 표시하는 프로그램 메시지 내용을 읽을 수 없음.
* 브라우즈 모드에서 마지막 글자에서 오른쪽 화살표를 누르거나 마지막 컨테이너에서 다음 컨테이너로 이동할때 커서가 문서 외부로 이동되던 문제 수정. (#2463)
* 특정 웹 에플리케이션 대화상자내에서 (특히 ARIA describedby 속성이 없는 경우) 불필요한 내용이 출력되던 문제 수정. (#2390)
* 인터넷 익스플로러와 같은 MSHTML 창에서 만약 ARIA 특정 구성이 설정된 경우 특정 입력창 정보를 알리거나 입력창을 찾던 문제 수정. (#2435)
* 윈도우 컨설창에서 백스페이스를 눌러 입력된 단어 읽을때 백스페이스키가 제대로 처리되지 않던 문제 수정. (#2586)
* Microsoft Excel에서 셀 좌표가 점자로 표시되지 않던 문제 수정.
* Microsoft Word에서 숫자나 리스트로된 문단에서 왼쪽 화살표나 CTRL+왼쪽 화살표를 누를때 이전 문단의 내용이 목록 서식으로 된 내용으로 인식되던 문제 수정. (#2402)
* 모질라 프로그램에서 브라우즈 모드 사용 시 특정 리스트 박스(특히 ARIA 리스트 박스)애에 있는 내용이 잘못 표시되던 문제 수정.
* 모질라 프로그램에서 특정 컨트럴의 레이블이 잘못 출력되거나 공백으로 처리되던 문제 수정.
* 모질라 프로그램에서 브라우즈 모드 사용 시 불필요한 공백이 사라짐.
* 웹브라우저에서 브라우즈 모드 사용 시 특정 그래픽에 얼트태그가 없는 경우 (예: 프레즌테이션형 그림과 같이 alt=""를 사용하여 설명을 추가하지 않았을때) 그래픽을 무시하도록 함.
* 웹브라우저에서 스크린 리더에게서 숨기고자 하는 컨텐츠(ARIA hidden(숨김) 속성 사용)가 있는 경우 출력 않하도록 수정. (#2117)
* 음수로된 화폐값(예: -$123)이 기호 레벨에 상관없이 "마이너스" 화폐값으로 출력되도록 수정. (#2625)
* 모두 읽기 사용 시 특정 줄이 문장 끝이 아닐때 음성 언어가 기본 언어로 변경되던 문제 수정. (#2630)
* 어도비 리더 10.1 이상에서 정확한 폰트 정보가 출력되도록 함. (#2175)
* 어도비 리더 문서 읽을때 특정 내용의 대체 내용이 있을 경우 대체 내용이 출력되도록 함 (불필요한 내용이 출력되지 않도록 수정). (#2174)
* 특정 문서에 에플리케이션이 삽입되어 있을때 모르고 에플리케이션이 진입하지 않도록 브라우즈 모드 탐색에서 제거 (에플리케이션을 사용하려면 임베디드 객체 사용 요령을 참조바람). (#990)
* 모질라 프로그램에서 스핀 버튼의 변경값이 출력되도록 함. (#2653)
* 어도비 디지털 에디션 2.0 지원. (#2688)
* 인터넷 익스플로러와 같은 MSHTML 창에 있는 콤보박스에서 NVDA+위쪽 화살표를 누를때 선택된 항목만 읽도록 함 (예전에는 콤보박스에 있는 모든 항목을 읽었음). (#2337)
* 음성 발음 사전에서 이전값과 변경값에 숫자 기호 (#)가 삽입된 경우 사전이 저장되지 않던 문제 수정. (#961)
* 인터넷 익스플로러와 같은 MSHTML 창에 있는 숨김 내용 중 보여지도록 한 내용을 읽도록 함 (즉 visibility:hidden에 있는 내용중 visibility:visible 내용을 읽도록 함). (#2097)
* 윈도우 XP 보안 센터내 링크 내용후 이상한 글자가 출력되던 문제 수정. (#1331)
* 윈도우 7 시작 검색창과 같은 UI 자동화 컨트롤를 마우스로 탐색할때 내용이 출력되지 않던 문제 수정.
* 문서 모두 읽기 도중 키보드 레이아웃 변경 메시지가 출력되던 문제 수정. (#1676)
* 윈도우 7과 8의 검색창과 같은 UI 자동화 컨트럴내 내용이 변경될때마다 변경 내용이 반복적으로 출력되지 않도록 함.
* 윈도우 8 시작 화면내 타일 그룹끼리 이동할때 그룹명이 없는 경우 첫 타일명이 그룹명으로 출력되던 문제 수정. (#2658)
* 윈도우 8 시작 화면 호출시 루트 타일이 아닌 첫 타일이 포커스되도록 함. (#2720)
* 사용자 경로에 다중 글자(특히 영어 외 타국어 글자)가 사용된 경우 NVDA가 실행되지 않던 문제 수정. (#2729)
* 구글 Chrome에서 브라우즈 모드 사용 시 탭 내용이 잘못 출력되던 문제 수정.
* 브라우즈 모드에서 메뉴 버튼이 제데로 출력되도록 함.
* OpenOffice.org/LibreOffice Calc 사용 시 스프레드 시트 셀 정보가 제대로 출력되지 않던 문제 수정. (#2765)
* 인터넷 익스플로러를 사용하여 이전처럼 Yahoo! 메일 리스트 사용 가능. (#2780)

### 개발 변경사항(영문)

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
